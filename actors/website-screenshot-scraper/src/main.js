import { Actor, log } from 'apify';
import { chromium } from 'playwright';

await Actor.init();

const timeoutAt = Actor.getEnv().timeoutAt?.getTime() ?? null;
const TIME_BUDGET_MARGIN_MS = 45_000;
function remainingMs() { return timeoutAt == null ? Infinity : timeoutAt - Date.now() - TIME_BUDGET_MARGIN_MS; }
function timeBudgetOk() { return remainingMs() > 0; }

const input = (await Actor.getInput()) ?? {};
const urls = Array.isArray(input.urls) && input.urls.length ? input.urls : ['https://example.com'];
const html = typeof input.html === 'string' && input.html.trim() ? input.html : null;
const format = ['jpeg', 'png', 'pdf'].includes(input.format) ? input.format : 'jpeg';
const quality = Math.min(Math.max(Number(input.quality ?? 80), 10), 100);
const fullPage = input.fullPage !== false;
const selector = typeof input.selector === 'string' && input.selector.trim() ? input.selector.trim() : null;
const ogCard = input.ogCard === true;
const waitUntil = ['load', 'domcontentloaded', 'networkidle'].includes(input.waitUntil) ? input.waitUntil : 'load';
const delayMs = Math.min(Math.max(Number(input.delayMs ?? 0), 0), 15000);

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
async function pushError(url, message) {
  await Actor.pushData({ url: url ?? null, format, success: false, error: message, imageUrl: null, screenshotKey: null, contentType: null, byteSize: null, capturedAt: new Date().toISOString() });
}

const kvStore = await Actor.openKeyValueStore();
const extFor = { jpeg: 'jpg', png: 'png', pdf: 'pdf' };
const contentTypeFor = { jpeg: 'image/jpeg', png: 'image/png', pdf: 'application/pdf' };

async function captureOne(browser, { url, rawHtml }, index) {
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
    if (delayMs > 0) await page.waitForTimeout(delayMs);

    let buffer;
    if (format === 'pdf') {
      buffer = await page.pdf({ printBackground: true });
    } else if (selector) {
      const el = await page.waitForSelector(selector, { state: 'attached', timeout: 10000 });
      buffer = await el.screenshot({ type: format, ...(format === 'jpeg' ? { quality } : {}) });
    } else {
      buffer = await page.screenshot({ type: format, fullPage: !ogCard && fullPage, ...(format === 'jpeg' ? { quality } : {}) });
    }

    const key = `screenshot-${Date.now()}-${index}.${extFor[format]}`;
    await kvStore.setValue(key, buffer, { contentType: contentTypeFor[format] });
    const imageUrl = kvStore.getPublicUrl(key);

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
  } finally {
    await context.close();
  }
}

try {
  if (!timeBudgetOk()) throw new Error('Out of time budget before any work started');
  const browser = await chromium.launch({ headless: true, args: ['--disable-dev-shm-usage'] });
  try {
    if (html) {
      await captureOne(browser, { url: null, rawHtml: html }, 0);
    } else {
      for (let i = 0; i < urls.length; i++) {
        if (!timeBudgetOk()) { log.warning('Time budget exhausted, stopping early.'); break; }
        const keepGoing = await captureOne(browser, { url: urls[i], rawHtml: null }, i);
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
