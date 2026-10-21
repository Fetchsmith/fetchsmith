import { Actor, log } from 'apify';
import { chromium } from 'playwright';
import pngjs from 'pngjs'; // CJS: named import would depend on cjs-lexer detection, destructure instead
import pixelmatch from 'pixelmatch';

const { PNG } = pngjs;

await Actor.init();

const timeoutAt = Actor.getEnv().timeoutAt?.getTime() ?? null;
const TIME_BUDGET_MARGIN_MS = 45_000;
function remainingMs() { return timeoutAt == null ? Infinity : timeoutAt - Date.now() - TIME_BUDGET_MARGIN_MS; }
function timeBudgetOk() { return remainingMs() > 0; }

const input = (await Actor.getInput()) ?? {};
const urls = Array.isArray(input.urls) && input.urls.length ? input.urls : ['https://example.com'];
const html = typeof input.html === 'string' && input.html.trim() ? input.html : null;
const compareUrl = typeof input.compareUrl === 'string' && input.compareUrl.trim() ? input.compareUrl.trim() : null;
// Pixel diffing needs lossless input, so compare mode always captures PNG regardless of `format`.
const format = compareUrl ? 'png' : (['jpeg', 'png', 'pdf'].includes(input.format) ? input.format : 'jpeg');
const quality = Math.min(Math.max(Number(input.quality ?? 80), 10), 100);
const fullPage = input.fullPage !== false;
const selector = typeof input.selector === 'string' && input.selector.trim() ? input.selector.trim() : null;
const ogCard = input.ogCard === true;
const waitUntil = ['load', 'domcontentloaded', 'networkidle'].includes(input.waitUntil) ? input.waitUntil : 'load';
const delayMs = Math.min(Math.max(Number(input.delayMs ?? 0), 0), 15000);
const waitForSelector = typeof input.waitForSelector === 'string' && input.waitForSelector.trim() ? input.waitForSelector.trim() : null;
const diffThreshold = Math.min(Math.max(Number(input.diffThreshold ?? 0.1), 0), 1);

if (compareUrl && input.format && input.format !== 'png') {
  log.info(`Compare mode: forcing PNG output (requested '${input.format}' is lossy/non-raster, which would corrupt the pixel diff).`);
}

const DEVICE_PRESETS = {
  desktop: { width: 1920, height: 1080, deviceScaleFactor: 1, isMobile: false },
  iphone: { width: 390, height: 844, deviceScaleFactor: 3, isMobile: true },
  pixel: { width: 412, height: 915, deviceScaleFactor: 2.6, isMobile: true },
  ipad: { width: 820, height: 1180, deviceScaleFactor: 2, isMobile: true },
};
function resolveViewport() {
  if (ogCard) return { width: 1200, height: 630, deviceScaleFactor: 1, isMobile: false };
  const preset = DEVICE_PRESETS[input.devicePreset];
  if (preset) return preset;
  return {
    width: Math.min(Math.max(Number(input.viewportWidth ?? 1920), 200), 3840),
    height: Math.min(Math.max(Number(input.viewportHeight ?? 1080), 200), 3840),
    deviceScaleFactor: 1,
    isMobile: false,
  };
}
const viewport = resolveViewport();

const cm = Actor.getChargingManager();
const isPPE = cm.getPricingInfo().isPayPerEvent;
let pushed = 0;
async function pushResult(item) {
  if (isPPE) {
    const r = await Actor.charge({ eventName: 'result', count: 1 });
    if (r.chargedCount === 0) return false;
    await Actor.pushData(item); pushed += 1;
    return !r.eventChargeLimitReached;
  }
  await Actor.pushData(item); pushed += 1;
  return true;
}
async function pushError(url, message, extra = {}) {
  await Actor.pushData({ url: url ?? null, format, success: false, error: message, imageUrl: null, screenshotKey: null, contentType: null, byteSize: null, capturedAt: new Date().toISOString(), ...extra });
}

const kvStore = await Actor.openKeyValueStore();
const extFor = { jpeg: 'jpg', png: 'png', pdf: 'pdf' };
const contentTypeFor = { jpeg: 'image/jpeg', png: 'image/png', pdf: 'application/pdf' };

// Render one target to a buffer. `fmt` overrides the run-level format (compare mode needs PNG).
async function renderBuffer(browser, { url, rawHtml }, fmt = format) {
  const context = await browser.newContext({
    viewport: { width: viewport.width, height: viewport.height },
    deviceScaleFactor: viewport.deviceScaleFactor,
    isMobile: viewport.isMobile,
  });
  const page = await context.newPage();
  try {
    if (rawHtml) {
      await page.setContent(rawHtml, { waitUntil, timeout: 30000 });
    } else {
      await page.goto(url, { waitUntil, timeout: 30000 });
    }
    if (waitForSelector) await page.waitForSelector(waitForSelector, { state: 'visible', timeout: 10000 });
    if (delayMs > 0) await page.waitForTimeout(delayMs);

    if (fmt === 'pdf') return await page.pdf({ printBackground: true });
    if (selector) {
      const el = await page.waitForSelector(selector, { state: 'attached', timeout: 10000 });
      return await el.screenshot({ type: fmt, ...(fmt === 'jpeg' ? { quality } : {}) });
    }
    return await page.screenshot({ type: fmt, fullPage: !ogCard && fullPage, ...(fmt === 'jpeg' ? { quality } : {}) });
  } finally {
    await context.close();
  }
}

async function storeBuffer(buffer, name, index, fmt = format) {
  const key = `${name}-${Date.now()}-${index}.${extFor[fmt]}`;
  await kvStore.setValue(key, buffer, { contentType: contentTypeFor[fmt] });
  return { key, imageUrl: kvStore.getPublicUrl(key) };
}

async function captureOne(browser, { url, rawHtml }, index) {
  try {
    const buffer = await renderBuffer(browser, { url, rawHtml });
    const { key, imageUrl } = await storeBuffer(buffer, 'screenshot', index);
    return pushResult({
      url: url ?? null,
      format,
      success: true,
      error: null,
      imageUrl,
      screenshotKey: key,
      contentType: contentTypeFor[format],
      byteSize: buffer.length,
      capturedAt: new Date().toISOString(),
    });
  } catch (err) {
    log.warning(`Capture failed for ${url ?? 'raw HTML'}: ${err.message}`);
    await pushError(url, err.message);
    return true; // not a budget stop, just a per-item failure; keep going
  }
}

// Crop an RGBA buffer down to w x h from the top-left corner. Returns `src` untouched when it
// already matches, so the equal-size path (the common one) copies nothing.
function cropRGBA(src, srcW, srcH, w, h) {
  if (srcW === w && srcH === h) return src;
  const out = Buffer.alloc(w * h * 4);
  for (let y = 0; y < h; y++) src.copy(out, y * w * 4, (y * srcW) * 4, (y * srcW + w) * 4);
  return out;
}

async function compareOne(browser, url, index) {
  try {
    const baseBuf = await renderBuffer(browser, { url, rawHtml: null }, 'png');
    const cmpBuf = await renderBuffer(browser, { url: compareUrl, rawHtml: null }, 'png');
    const basePng = PNG.sync.read(baseBuf);
    const cmpPng = PNG.sync.read(cmpBuf);

    // Two different pages (or the same page before/after a deploy) rarely render to identical
    // heights with fullPage on, and pixelmatch requires equal dimensions. Diff the overlapping
    // top-left region and say so in the row rather than failing the comparison outright.
    const w = Math.min(basePng.width, cmpPng.width);
    const h = Math.min(basePng.height, cmpPng.height);
    const sizeMismatch = basePng.width !== cmpPng.width || basePng.height !== cmpPng.height;
    const a = cropRGBA(basePng.data, basePng.width, basePng.height, w, h);
    const b = cropRGBA(cmpPng.data, cmpPng.width, cmpPng.height, w, h);

    const diffPng = new PNG({ width: w, height: h });
    const diffPixels = pixelmatch(a, b, diffPng.data, w, h, { threshold: diffThreshold, includeAA: true });
    const diffBuf = PNG.sync.write(diffPng);

    const base = await storeBuffer(baseBuf, 'screenshot', index, 'png');
    const cmp = await storeBuffer(cmpBuf, 'compare', index, 'png');
    const diff = await storeBuffer(diffBuf, 'diff', index, 'png');

    const comparedPixels = w * h;
    return pushResult({
      url: url ?? null,
      format: 'png',
      success: true,
      error: null,
      imageUrl: base.imageUrl,
      screenshotKey: base.key,
      contentType: 'image/png',
      byteSize: baseBuf.length,
      capturedAt: new Date().toISOString(),
      compareUrl,
      compareImageUrl: cmp.imageUrl,
      compareScreenshotKey: cmp.key,
      diffImageUrl: diff.imageUrl,
      diffScreenshotKey: diff.key,
      diffPixels,
      comparedPixels,
      diffPercent: comparedPixels ? Number(((diffPixels / comparedPixels) * 100).toFixed(4)) : null,
      changed: diffPixels > 0,
      baselineWidth: basePng.width,
      baselineHeight: basePng.height,
      compareWidth: cmpPng.width,
      compareHeight: cmpPng.height,
      sizeMismatch,
    });
  } catch (err) {
    log.warning(`Comparison failed for ${url} vs ${compareUrl}: ${err.message}`);
    await pushError(url, err.message, { compareUrl, diffPixels: null, diffPercent: null, changed: null, diffImageUrl: null });
    return true;
  }
}

try {
  if (!timeBudgetOk()) throw new Error('Out of time budget before any work started');
  const browser = await chromium.launch({ headless: true, args: ['--disable-dev-shm-usage'] });
  try {
    if (html && !compareUrl) {
      await captureOne(browser, { url: null, rawHtml: html }, 0);
    } else {
      if (html && compareUrl) log.warning('Compare mode ignores raw `html` input: a diff needs two fetched URLs.');
      for (let i = 0; i < urls.length; i++) {
        if (!timeBudgetOk()) { log.warning('Time budget exhausted, stopping early.'); break; }
        const keepGoing = compareUrl
          ? await compareOne(browser, urls[i], i)
          : await captureOne(browser, { url: urls[i], rawHtml: null }, i);
        if (!keepGoing) { log.info('Charge limit reached, stopping.'); break; }
      }
    }
  } finally {
    await browser.close();
  }
} catch (err) {
  log.exception(err, 'Run failed');
  await Actor.fail(`Run failed: ${err.message}`);
}
log.info(`Done. Pushed ${pushed} results.`);
await Actor.exit();
