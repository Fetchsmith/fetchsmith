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
const colorScheme = ['light', 'dark', 'no-preference'].includes(input.colorScheme) ? input.colorScheme : 'light';
const locale = typeof input.locale === 'string' && input.locale.trim() ? input.locale.trim() : undefined;
const timezoneId = typeof input.timezoneId === 'string' && input.timezoneId.trim() ? input.timezoneId.trim() : undefined;
const geolocation = (input.geolocation && typeof input.geolocation === 'object' && !Array.isArray(input.geolocation))
  ? input.geolocation : null;

// Both are for pages you already have a right to reach with your OWN credentials (e.g. an
// API-key-gated embed, or your own logged-in session cookie) -- not a login/paywall bypass.
// Validated upfront so a typo fails the whole run with one clear message instead of a cryptic
// per-URL Playwright error repeated across every item.
const extraHeaders = (input.headers && typeof input.headers === 'object' && !Array.isArray(input.headers))
  ? input.headers : null;
const cookies = Array.isArray(input.cookies) && input.cookies.length ? input.cookies : null;
try {
  if (extraHeaders) {
    for (const [k, v] of Object.entries(extraHeaders)) {
      if (typeof v !== 'string') throw new Error(`headers["${k}"] must be a string, got ${typeof v}.`);
    }
  }
  if (cookies) {
    for (const c of cookies) {
      if (!c || typeof c.name !== 'string' || !c.name || typeof c.value !== 'string') {
        throw new Error(`every cookies[] entry needs a string "name" and "value" (got ${JSON.stringify(c)}).`);
      }
    }
  }
  if (geolocation) {
    const { latitude, longitude, accuracy } = geolocation;
    if (typeof latitude !== 'number' || latitude < -90 || latitude > 90) {
      throw new Error(`geolocation.latitude must be a number in [-90, 90], got ${JSON.stringify(latitude)}.`);
    }
    if (typeof longitude !== 'number' || longitude < -180 || longitude > 180) {
      throw new Error(`geolocation.longitude must be a number in [-180, 180], got ${JSON.stringify(longitude)}.`);
    }
    if (accuracy !== undefined && (typeof accuracy !== 'number' || accuracy < 0)) {
      throw new Error(`geolocation.accuracy must be a non-negative number, got ${JSON.stringify(accuracy)}.`);
    }
  }
} catch (err) {
  await Actor.fail(`Input error: ${err.message}`);
  throw err;
}

// Returns undefined when the caller left the proxy off (or picked `useApifyProxy: false` with no
// custom URLs), which is the default. A bad group name / an Apify group this account cannot use
// throws here rather than at capture time, so fail the run with the SDK's own message instead of
// letting every URL produce an identical cryptic error row.
let proxyConfiguration;
try {
  proxyConfiguration = await Actor.createProxyConfiguration(input.proxyConfiguration);
} catch (err) {
  await Actor.fail(`Proxy configuration rejected: ${err.message}`);
  throw err;
}

// A session id is NOT optional here. `newUrl()` with no session returns a session-less Apify Proxy
// URL, and the proxy then picks an exit IP per CONNECTION -- measured live (cycle 2036): the two
// captures of one compare pair came back through 107.172.69.119 and 107.175.80.80 and diffed at
// 146 px purely because the page echoed the caller's IP. Keying the session on the item index
// pins one IP per URL, and lets a compare pair ask for the same index twice and get one IP.
const runSalt = (Actor.getEnv().actorRunId ?? `local${Date.now()}`).replace(/[^\w-]/g, '');
// Playwright wants the credentials split out of the URL; it does not read user:pass from `server`.
async function proxyFor(index) {
  if (!proxyConfiguration) return null;
  const u = new URL(await proxyConfiguration.newUrl(`${runSalt}_${index}`.slice(0, 50)));
  return {
    server: `${u.protocol}//${u.host}`,
    ...(u.username ? { username: decodeURIComponent(u.username) } : {}),
    ...(u.password ? { password: decodeURIComponent(u.password) } : {}),
  };
}

if (compareUrl && input.format && input.format !== 'png') {
  log.info(`Compare mode: forcing PNG output (requested '${input.format}' is lossy/non-raster, which would corrupt the pixel diff).`);
}

const DEVICE_PRESETS = {
  desktop: { width: 1920, height: 1080, deviceScaleFactor: 1, isMobile: false, hasTouch: false },
  iphone: { width: 390, height: 844, deviceScaleFactor: 3, isMobile: true, hasTouch: true },
  pixel: { width: 412, height: 915, deviceScaleFactor: 2.6, isMobile: true, hasTouch: true },
  ipad: { width: 820, height: 1180, deviceScaleFactor: 2, isMobile: true, hasTouch: true },
};
function resolveViewport() {
  const base = ogCard
    ? { width: 1200, height: 630, deviceScaleFactor: 1, isMobile: false, hasTouch: false }
    : DEVICE_PRESETS[input.devicePreset] ?? {
        width: Math.min(Math.max(Number(input.viewportWidth ?? 1920), 200), 3840),
        height: Math.min(Math.max(Number(input.viewportHeight ?? 1080), 200), 3840),
        deviceScaleFactor: 1,
        isMobile: false,
        hasTouch: false,
      };
  // Preset/custom picks a sensible hasTouch default (true for the phone/tablet presets); let the
  // caller override it explicitly either way, e.g. a touch-capable desktop kiosk or a non-touch iPad.
  return { ...base, hasTouch: typeof input.hasTouch === 'boolean' ? input.hasTouch : base.hasTouch };
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
// `proxy` is per-context (not per-browser) so a URL list rotates IPs without relaunching Chromium.
async function renderBuffer(browser, { url, rawHtml }, fmt = format, proxy = null) {
  const context = await browser.newContext({
    viewport: { width: viewport.width, height: viewport.height },
    deviceScaleFactor: viewport.deviceScaleFactor,
    isMobile: viewport.isMobile,
    hasTouch: viewport.hasTouch,
    colorScheme,
    ...(locale ? { locale } : {}),
    ...(timezoneId ? { timezoneId } : {}),
    ...(proxy ? { proxy } : {}),
    // `geolocation` alone is inert: Playwright denies the Geolocation API by default (there's no
    // browser chrome to click "Allow" in headless mode), so any page calling getCurrentPosition()
    // gets a silent PERMISSION_DENIED and the input would do nothing -- measured offline before
    // shipping. `permissions: ['geolocation']` is the headless equivalent of granting that prompt;
    // it only unlocks the coordinates the caller themselves supplied, nothing about anyone else.
    ...(geolocation ? { geolocation, permissions: ['geolocation'] } : {}),
  });
  try {
    if (extraHeaders) await context.setExtraHTTPHeaders(extraHeaders);
    // A cookie needs either an explicit domain/path or a `url` to derive them from -- only
    // meaningful when we're actually navigating to a URL (not raw HTML).
    if (cookies && url) {
      await context.addCookies(cookies.map((c) => ({
        name: c.name,
        value: c.value,
        ...(c.domain ? { domain: c.domain, path: c.path || '/' } : { url }),
      })));
    }
    // `newPage()` can throw on a bad user-supplied `timezoneId` -- keep it inside the try so an
    // invalid value still reaches the `finally` below instead of leaking the context.
    const page = await context.newPage();
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

// Every other scraper in this fleet retries a transient upstream hiccup before giving up; this
// Actor had zero retries anywhere, so a single dropped connection or a page that was merely slow
// to answer (not broken) permanently failed that URL. Only retry error shapes that are plausibly
// transient (timeout, connection reset/closed, empty response) -- NOT DNS failure, connection
// refused, or a bad cert, which are the same outcome on attempt 2 and would just double the
// compute cost for nothing.
const TRANSIENT_RENDER_ERROR_RE = /Timeout.*exceeded|ERR_CONNECTION_RESET|ERR_CONNECTION_CLOSED|ERR_EMPTY_RESPONSE|ERR_HTTP2_PROTOCOL_ERROR|ERR_TIMED_OUT|ERR_NETWORK_CHANGED|ERR_SOCKET_NOT_CONNECTED/;
const RENDER_RETRY_DELAY_MS = 1500;
async function renderWithRetry(browser, target, fmt, proxy) {
  try {
    return await renderBuffer(browser, target, fmt, proxy);
  } catch (err) {
    if (!TRANSIENT_RENDER_ERROR_RE.test(err.message) || !timeBudgetOk()) throw err;
    log.warning(`Transient failure rendering ${target.url ?? 'raw HTML'} (${err.message}) — retrying once.`);
    await new Promise((r) => setTimeout(r, RENDER_RETRY_DELAY_MS));
    return renderBuffer(browser, target, fmt, proxy);
  }
}

async function storeBuffer(buffer, name, index, fmt = format) {
  const key = `${name}-${Date.now()}-${index}.${extFor[fmt]}`;
  await kvStore.setValue(key, buffer, { contentType: contentTypeFor[fmt] });
  return { key, imageUrl: kvStore.getPublicUrl(key) };
}

async function captureOne(browser, { url, rawHtml }, index) {
  try {
    const buffer = await renderWithRetry(browser, { url, rawHtml }, format, await proxyFor(index));
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
    // One IP for BOTH sides of the pair: a geo-routed or per-IP-personalised page rendered through
    // two different exit nodes would diff as "changed" when nothing actually changed.
    const pairProxy = await proxyFor(index);
    const baseBuf = await renderWithRetry(browser, { url, rawHtml: null }, 'png', pairProxy);
    const cmpBuf = await renderWithRetry(browser, { url: compareUrl, rawHtml: null }, 'png', pairProxy);
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
