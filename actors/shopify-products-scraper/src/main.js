import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';
import * as cheerio from 'cheerio';

await Actor.init();
const input = (await Actor.getInput()) ?? {};
const rawStoreUrls = (input.storeUrls ?? []).map((s) => String(s).trim()).filter(Boolean);
// Dedup by the actual endpoint each URL resolves to, not the raw string — catches the common
// mistake of the same store/collection pasted twice with a different protocol/trailing slash,
// which would otherwise fetch and charge for the same products twice.
const seenEndpoints = new Set();
let duplicateStoreUrls = 0;
const storeUrls = rawStoreUrls.filter((raw) => {
  let key;
  try { key = endpointFor(raw).url; } catch { key = raw; }
  if (seenEndpoints.has(key)) { duplicateStoreUrls += 1; return false; }
  seenEndpoints.add(key);
  return true;
});
const perStore = Math.min(Number(input.maxProductsPerStore ?? 500), 100000);
const maxResults = Math.min(Number(input.maxResults ?? 5000), 200000);
const withDesc = input.includeDescription !== false;
const withVariants = input.includeVariants !== false;
const onlyAvailable = !!input.onlyAvailable;
const detailLevel = input.detailLevel === 'full' ? 'full' : 'basic';
const searchQuery = String(input.searchQuery ?? '').normalize('NFC').trim();
const searchWords = searchQuery ? searchQuery.toLowerCase().split(/\s+/).filter(Boolean) : [];
// Price/sale filters work on the SHAPED row (priceMin/priceMax/isOnSale), not on raw Shopify JSON,
// because a product's price is a range across its variants and the sale flag is derived from
// compare-at prices — neither exists as a single field on the raw payload. They therefore run
// after shape() but before charging, so a filtered-out product is never billed.
const numOrNull = (v) => (v == null || v === '' || Number.isNaN(Number(v)) ? null : Number(v));
const minPrice = numOrNull(input.minPrice);
const maxPrice = numOrNull(input.maxPrice);
const onSaleOnly = !!input.onSaleOnly;
// Same "already computed, never filterable" shape as minPrice/maxPrice/onSaleOnly (cycle 416):
// discountPercent is derived per-row today but a buyer wanting "at least 30% off" had no way to
// ask for it except onSaleOnly (any discount at all). Reads the shaped item, so it runs alongside
// the other shaped filters below, not with matchesSearch/matchesVendorType.
const minDiscountPercent = numOrNull(input.minDiscountPercent);
const hasShapedFilters = minPrice != null || maxPrice != null || onSaleOnly || minDiscountPercent != null;
// OR-within-list, AND-with-everything-else — same convention as uk-find-a-tender-scraper's
// keywordsAny/regions (cycle 415). searchQuery is AND-of-words across a combined haystack, so it
// cannot express "vendor is Allbirds or Rothy's"; these read the raw payload (vendor/product_type
// are already on every row) so they run alongside matchesSearch, before shape()/charging.
const vendorsFilter = (input.vendors ?? []).map((v) => String(v).normalize('NFC').toLowerCase().trim()).filter(Boolean);
const productTypesFilter = (input.productTypes ?? []).map((t) => String(t).normalize('NFC').toLowerCase().trim()).filter(Boolean);
if (!storeUrls.length) await Actor.fail('Provide at least one store URL.');
if (duplicateStoreUrls) log.info(`Skipped ${duplicateStoreUrls} duplicate storeUrls entr${duplicateStoreUrls === 1 ? 'y' : 'ies'} (same endpoint already queued).`);

// ---- watch mode -----------------------------------------------------------
// A Shopify catalog is a SNAPSHOT, not a stream of events (unlike reviews/tenders, where the
// house watch pattern can key on "id we have never delivered"). Re-running the same store daily
// returns the same rows and re-charges for all of them, so the useful watch here is a DIFF: what
// is new, what changed price, what came back in stock. The baseline therefore stores a small
// value per product (price + availability), not just an id.
const watchLabel = String(input.watchLabel ?? '').trim();
const watchMode = watchLabel.length > 0;
const WATCH_EVENTS = ['new', 'priceDrop', 'priceIncrease', 'backInStock', 'outOfStock', 'delisted'];
const watchEventsInput = (input.watchEvents ?? []).map((e) => String(e).trim()).filter(Boolean);
const unknownWatchEvents = watchEventsInput.filter((e) => !WATCH_EVENTS.includes(e));
if (unknownWatchEvents.length) log.warning(`Ignoring unknown watchEvents value(s): ${unknownWatchEvents.join(', ')}. Valid values: ${WATCH_EVENTS.join(', ')}.`);
const watchEvents = new Set(watchEventsInput.filter((e) => WATCH_EVENTS.includes(e)));
if (!watchEvents.size) for (const e of WATCH_EVENTS) watchEvents.add(e);
if (!watchMode && watchEventsInput.length) log.warning('"watchEvents" only applies when "watchLabel" is set — this run is a normal one-off scrape and returns every matching product.');
const webhookUrlRaw = String(input.webhookUrl ?? '').trim();
let webhookUrl = null;
if (webhookUrlRaw) {
  try {
    const parsed = new URL(webhookUrlRaw);
    if (parsed.protocol === 'http:' || parsed.protocol === 'https:') webhookUrl = parsed.toString();
    else log.warning(`webhookUrl "${webhookUrlRaw}" is not http(s); ignoring.`);
  } catch {
    log.warning(`webhookUrl "${webhookUrlRaw}" is not a valid URL; ignoring.`);
  }
}
const WATCH_STORE = 'fetchsmith-shopify-products-watch';
const WATCH_KEEP = 30000; // bound the record size; least-recently-seen products fall off first
// Only the filters that decide WHICH products a run can see belong in the fingerprint. Changing
// one of them means a different watched set, so it must start its own baseline; detailLevel /
// includeDescription / includeVariants only change the shape of a delivered row and must not
// reset anyone's baseline. storeUrls is deliberately NOT in here — adding a store to an existing
// label baselines that one store (below) instead of throwing away the whole history.
function watchKeyFor(label) {
  const criteria = JSON.stringify([onlyAvailable, searchQuery, vendorsFilter, productTypesFilter, minPrice, maxPrice, onSaleOnly, minDiscountPercent]);
  let h = 5381;
  for (let i = 0; i < criteria.length; i++) h = ((h * 33) ^ criteria.charCodeAt(i)) >>> 0;
  const fp = h.toString(36);
  const safe = label.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 40) || 'watch';
  return { key: `watch-${safe}-${fp}`, fingerprint: fp };
}
// Overlapping input URLs are normal, not a mistake: "/collections/all" plus "/collections/mens",
// or two categories that share products, put the SAME product in two feeds. Each result is a
// billable event, so a product must be returned — and charged — once per run. Keyed by
// origin + id, never by id alone: two different stores are two different products even in the
// (practically impossible) case that Shopify hands them the same id.
const seenProducts = new Map(); // `${origin}\n${id}` -> the input URL that delivered it first
const productKey = (origin, id) => `${origin}\n${id}`;
let duplicateProducts = 0;
const rawForEndpoint = new Map(); // endpoint URL -> the input URL the buyer actually typed
let watchStore = null;
let watchKey = null;
let watchRecord = null;
const watchPrev = new Map(); // productId -> { price, avail, store, handle } as of the last run under this label
const watchNow = new Map(); // productId -> { price, avail, store, handle } seen in THIS run
const seededStores = new Set(); // endpoint URLs already baselined under this label
// A product missing from this run is only "delisted" if the run can PROVE it walked that store's
// whole feed — otherwise a scan cap, a maxResults stop, the time budget or a mid-sweep error would
// bill the buyer for a catalog that is still there. Populated only for stores whose paged sweep ran
// to the end of the feed: endpoint URL -> every product id the feed returned, BEFORE any filter (a
// product that is still on the store but no longer matches "maxPrice" is not delisted).
const watchStoreSweeps = new Map();
// Guard against the one benign case that looks exactly like a mass delist: a collection emptied or
// re-scoped. Above this share (and above the floor, so a genuinely tiny store can still fully
// close) the run reports nothing and charges nothing rather than guessing.
const DELIST_SUSPICIOUS_SHARE = 0.5;
const DELIST_SUSPICIOUS_MIN = 25;
const watchDeliveredDelisted = new Set(); // reported gone -> dropped from the baseline so it is not re-reported
let watchUnchanged = 0;
let watchEventsFiltered = 0; // a real change the buyer's watchEvents list excluded
let watchSeededThisRun = 0; // rows recorded as baseline instead of delivered
const watchCounts = Object.fromEntries(WATCH_EVENTS.map((e) => [e, 0]));
if (watchMode) {
  watchStore = await Actor.openKeyValueStore(WATCH_STORE);
  const { key, fingerprint } = watchKeyFor(watchLabel);
  watchKey = key;
  const existing = await watchStore.getValue(key);
  if (existing && Array.isArray(existing.products)) {
    watchRecord = existing;
    // storeIdx/handle (elements 4 and 5) were added later: records written before that are
    // 3-element tuples, so their products have no store attribution and can never be reported as
    // delisted. They pick attribution up the first time this run sees them again.
    const storeList = (existing.seededStores ?? []).map(String);
    for (const [id, price, avail, storeIdx, handle] of existing.products) {
      const watchBaselineEntry = { // bookkeeping, not a dataset row (see bin/check-code-fields)
        price: price ?? null,
        avail: avail == null ? null : !!avail,
        store: typeof storeIdx === 'number' ? storeList[storeIdx] ?? null : null,
        handle: handle ?? null,
      };
      watchPrev.set(String(id), watchBaselineEntry);
    }
    for (const s of storeList) seededStores.add(s);
    log.info(
      `Watch mode "${watchLabel}" (${key}): baseline from ${existing.lastRunAt ?? 'an earlier run'} holds `
      + `${watchPrev.size} product(s) across ${seededStores.size} store URL(s). This run returns only products that are new `
      + `or whose price/availability changed (events: ${[...watchEvents].join(', ')}); unchanged products are not pushed and not charged.`,
    );
  } else {
    watchRecord = { fingerprint, firstSeededAt: new Date().toISOString(), runCount: 0 };
    log.info(
      `Watch mode "${watchLabel}" (${key}): FIRST run for this label and filter set, so this is a baseline run. `
      + 'It records each product\'s price and availability and returns NOTHING (nothing is charged). The next run under '
      + 'the same label returns the differences.',
    );
  }
}
async function saveWatchRecord() {
  if (!watchMode || !watchStore) return;
  // Products not seen this run (deeper than the scan cap, or filtered out) keep their old baseline
  // — a truncated sweep must not make the next run re-announce them as "new". The exception is a
  // product already DELIVERED as delisted: keeping it would re-report it on every later run.
  const storeList = [...seededStores];
  const storeIdxOf = new Map(storeList.map((s, i) => [s, i]));
  const row = (id, v) => {
    const idx = v.store != null ? storeIdxOf.get(v.store) : undefined;
    return [id, v.price, v.avail == null ? null : v.avail ? 1 : 0, idx ?? null, v.handle ?? null];
  };
  const merged = [];
  for (const [id, v] of watchPrev) if (!watchNow.has(id) && !watchDeliveredDelisted.has(id)) merged.push(row(id, v));
  for (const [id, v] of watchNow) merged.push(row(id, v));
  const kept = merged.slice(-WATCH_KEEP);
  await watchStore.setValue(watchKey, {
    ...watchRecord,
    label: watchLabel,
    fingerprint: watchRecord.fingerprint,
    lastRunAt: new Date().toISOString(),
    runCount: (watchRecord.runCount ?? 0) + 1,
    seededStores: storeList,
    productCount: kept.length,
    products: kept,
  });
  if (merged.length > kept.length) log.warning(`Watch baseline capped at ${WATCH_KEEP} products — ${merged.length - kept.length} least-recently-seen product(s) dropped; they may be reported as "new" if they reappear.`);
}
// Records the product in this run's baseline and decides whether it is a deliverable change.
// Returns null for "record it, do not push and do not charge".
function watchVerdict(item, storeSeeding, storeUrl) {
  const id = String(item.id);
  const watchBaselineEntry = { price: item.priceMin, avail: item.available, store: storeUrl, handle: item.handle ?? null }; // bookkeeping, not a dataset row
  watchNow.set(id, watchBaselineEntry);
  if (storeSeeding) { watchSeededThisRun += 1; return null; }
  const prev = watchPrev.get(id);
  const changes = [];
  if (!prev) changes.push('new');
  else {
    // Unknown price or unknown availability (null) is "we could not tell", never an event —
    // same rule the rest of this Actor uses for null availability.
    if (prev.price != null && item.priceMin != null && prev.price !== item.priceMin) changes.push(item.priceMin < prev.price ? 'priceDrop' : 'priceIncrease');
    if (prev.avail === false && item.available === true) changes.push('backInStock');
    if (prev.avail === true && item.available === false) changes.push('outOfStock');
  }
  if (!changes.length) { watchUnchanged += 1; return null; }
  const wanted = changes.filter((c) => watchEvents.has(c));
  if (!wanted.length) { watchEventsFiltered += 1; return null; }
  for (const c of wanted) watchCounts[c] += 1;
  return {
    watchLabel,
    watchChange: wanted[0],
    watchChanges: wanted,
    previousPriceMin: prev?.price ?? null,
    previousAvailable: prev ? prev.avail : null,
    priceChange: prev?.price != null && item.priceMin != null ? Math.round((item.priceMin - prev.price) * 100) / 100 : null,
  };
}

// Some storefronts rate-limit or geo-gate products.json by IP, and the platform's shared egress
// IPs get hit first. Route through Apify Proxy when the run has access to it; if the account has
// no proxy access the run must still work, so fall back to a direct connection instead of failing.
let proxyUrlFor = async () => undefined;
try {
  const proxyConfiguration = await Actor.createProxyConfiguration(input.proxyConfiguration ?? { useApifyProxy: true });
  if (proxyConfiguration) {
    proxyUrlFor = (sessionId) => proxyConfiguration.newUrl(sessionId);
    log.info('Using Apify Proxy for storefront requests.');
  }
} catch (e) {
  log.warning(`Proxy unavailable (${e.message}) — continuing with a direct connection.`);
}

// Many stores x many pages is strictly sequential (each request up to 40s + 2 retries), so a run
// can approach the platform timeout with stores still queued. A hard kill there returns nothing
// to the customer even though partial results already exist in the dataset. Stop proactively with
// a safety margin and flush what's collected instead — same pattern as google-news-scraper.
const timeoutAt = Actor.getEnv().timeoutAt?.getTime() ?? null;
const TIME_BUDGET_MARGIN_MS = 45_000;
let timeBudgetExceeded = false;
function timeBudgetOk() {
  if (timeoutAt == null) return true;
  if (Date.now() >= timeoutAt - TIME_BUDGET_MARGIN_MS) { timeBudgetExceeded = true; return false; }
  return true;
}

let pushed = 0;
const isPPE = Actor.getChargingManager().getPricingInfo().isPayPerEvent;
async function pushResult(item) {
  if (isPPE) {
    const r = await Actor.charge({ eventName: 'result', count: 1 });
    if (r.chargedCount === 0) return false; // user's budget exhausted: never push unpaid items
    await Actor.pushData(item); pushed += 1;
    return !r.eventChargeLimitReached && pushed < maxResults;
  }
  await Actor.pushData(item); pushed += 1; // non-PPE run (e.g. developer test): no charging
  return pushed < maxResults;
}
// Shopify's localization layer strips `compare_at_price` out of the JSON endpoints when the
// request carries an Accept-Language header (some stores only: brooklinen.com returns 760
// variants with a compare price without it and 0 with it; allbirds/rothys are unaffected).
// got-scraping's header generator always adds one, so send an explicit empty value to suppress
// it — omitting the key lets the generator put its own back. Without this, `compareAtPrice`
// and `isOnSale` are silently wrong (null/false) on affected stores.
// got's own `retry` only fires for a fixed errorCodes list that does not include the
// connection-establishment faults (ERR_HTTP2_ERROR / HPE_INVALID_CONSTANT) measured live on
// this same got-scraping version in cycle 616 — about 1 in 4 fresh connections. Without an
// outer retry, one blip drops the rest of a store's pages (see fetchProductsPage), silently
// truncating a paid catalog instead of erroring loudly. Retry connection-level throws a
// handful of times before giving up; a thrown storefront HTTP status (throwIfStorefrontError,
// called by the caller after this resolves) is a separate, later step and is never retried here.
const request = async (url, headers) => {
  let lastErr;
  for (let attempt = 1; attempt <= 3; attempt += 1) {
    try {
      return await gotScraping({ url, timeout: { request: 40000 }, retry: { limit: 2 }, proxyUrl: await proxyUrlFor(), headers: { accept: 'application/json,text/html', ...headers } });
    } catch (e) {
      lastErr = e;
      if (attempt < 3) {
        log.warning(`${url}: attempt ${attempt}/3 failed (${e.message}) — retrying.`);
        await new Promise((r) => setTimeout(r, attempt * 1000));
      }
    }
  }
  throw lastErr;
};
const http = async (url) => {
  try { return await request(url, { 'accept-language': '' }); }
  catch (e) { return request(url, {}); } // a store that rejects the empty header still gets served, just without sale prices
};
const textOf = (html) => (html ? cheerio.load(html).text().replace(/\s+/g, ' ').trim() : null);

// A 200 carrying `{"products":[]}` is ambiguous: it is exactly what a genuinely empty store or a
// disabled endpoint returns, but Shopify's edge also serves it transiently (stale empty page cache,
// or a rate-limited datacenter IP answered 200-with-nothing instead of 429). The nightly health
// check hit that on allbirds.com — a store with 250+ live products — and the run told the customer
// "empty store". Only page 1 is ambiguous (a later page legitimately runs out), so re-confirm zero
// there before believing it. Costs nothing on the normal path, and each attempt gets a fresh proxy
// IP because proxyUrlFor() is called per request with no session id.
const EMPTY_PAGE_RETRIES = 2;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// ...but a zero-product result is only ambiguous on a 2xx. Measured 2026-09-21 against real hosts:
// Shopify's status code already says exactly what is wrong, and got-scraping does NOT throw on 4xx.
// Two of those bodies are valid JSON with no `products` key (402 -> `{"errors":"Unavailable Shop"}`,
// 404 -> `{"errors":"Not Found"}`), so they used to parse cleanly, yield [], and reach the customer
// as "Shopify returned zero products ... empty store/collection ... not a scrape failure" — after
// two pointless retries and 6s of sleeps. A typo'd domain was reported as an empty store. A 401
// sends an EMPTY body, which surfaced as a raw "Unexpected end of JSON input". Check the status
// first and say the actual reason.
const STOREFRONT_STATUS = {
  401: 'this storefront is password-protected (Shopify 401) — the merchant has an "Opening soon"/password page up, so products.json is not public. Ask them for the storefront password, or drop this URL.',
  402: 'this store is frozen or closed (Shopify 402 "Unavailable Shop") — the merchant\'s plan lapsed. There is nothing to scrape, and this is not a failure on our end.',
  403: 'this storefront refused the request (403) — a bot check or a geo/IP block, not a missing endpoint. Re-run with proxyConfiguration enabled (residential group) to get a different IP.',
  404: 'there is no Shopify store at this URL (404 "Not Found") — check the domain/handle for a typo, or the store has been deleted.',
  429: 'this storefront rate-limited us (429). Re-run with fewer storeUrls, or with proxyConfiguration enabled so each request comes from a different IP.',
};
const throwIfStorefrontError = (res) => {
  const code = res.statusCode;
  if (code >= 200 && code < 300) return res;
  const e = new Error(STOREFRONT_STATUS[code] ?? `this storefront answered HTTP ${code} instead of product JSON.`);
  e.storefrontStatus = code;
  throw e;
};
const fetchProductsPage = async (ep, page) => {
  for (let attempt = 0; ; attempt++) {
    const products = JSON.parse(throwIfStorefrontError(await http(`${ep.url}?limit=250&page=${page}`)).body).products ?? [];
    if (products.length || page !== 1 || attempt >= EMPTY_PAGE_RETRIES) return products;
    log.warning(`${ep.origin}: zero products on page 1 — re-checking (attempt ${attempt + 2}/${EMPTY_PAGE_RETRIES + 1}) in case Shopify served a transient empty response.`);
    await sleep(2000 * (attempt + 1));
  }
};

function endpointFor(raw) {
  const u = new URL(raw.startsWith('http') ? raw : `https://${raw}`);
  const origin = `${u.protocol}//${u.host}`;
  const col = u.pathname.match(/\/collections\/([^/]+)/)?.[1];
  const prod = u.pathname.match(/\/products\/([^/]+)/)?.[1];
  if (prod) return { origin, kind: 'product', url: `${origin}/products/${prod}.json` };
  if (col) return { origin, kind: 'collection', url: `${origin}/collections/${col}/products.json` };
  return { origin, kind: 'store', url: `${origin}/products.json` };
}
// The bulk `/products.json` endpoint omits these per-variant fields entirely, but the
// per-product `/products/<handle>.js` AJAX route carries them (same variant ids, so they merge
// cleanly — verified id-for-id on allbirds). Whether a store exposes them at all is a
// store-level setting, not an endpoint difference: allbirds returns real quantities and UPC
// barcodes, brooklinen a barcode but no quantity, rothys omits all four. `barcode` is whatever
// the merchant typed into that field — a GTIN/UPC on some stores, an internal SKU on others.
// `quantity_rule` is always present on `.js` with a `{min:1,max:null,increment:1}` default even
// on stores with no real rule, so only a non-default rule counts as "real" B2B/case-pack data —
// otherwise every enrichment would report a meaningless rule and always look "found".
const isMeaningfulQuantityRule = (qr) => !!qr && (qr.min > 1 || qr.max != null || qr.increment > 1);
const inventoryFieldsOf = (v) => ({
  barcode: v.barcode || null,
  inventoryQuantity: v.inventory_quantity ?? null,
  inventoryManagement: v.inventory_management ?? null,
  // Named predicate for "is this variant's stock actually tracked", so the 999999 sentinel stays
  // safe to spot after the row is flattened. `inventoryManagement: null` already carries that
  // meaning inside the nested row, but a CSV export of `variants[]` loses an implicit null far
  // more easily than a named boolean — and a dropped column there reintroduces the bad aggregate
  // (summing sentinels) that `totalInventoryOf` exists to prevent. Three-state on purpose: `null`
  // means the variant carries no inventory data at all (a `detailLevel:"basic"` row, where the
  // bulk feed strips these fields), which must not read as a confident "not tracked".
  inventoryTracked: hasInventoryData(v) ? !!v.inventory_management : null,
  inventoryPolicy: v.inventory_policy ?? null,
  quantityRule: isMeaningfulQuantityRule(v.quantity_rule) ? { min: v.quantity_rule.min ?? null, max: v.quantity_rule.max ?? null, increment: v.quantity_rule.increment ?? null } : null,
});
const hasInventoryData = (v) => !!(v.barcode || v.inventory_quantity != null || v.inventory_management || v.inventory_policy || isMeaningfulQuantityRule(v.quantity_rule));
// Sum of the quantities the store actually tracks; null (not 0) when it tracks none, so "out of
// stock" stays distinguishable from "this store doesn't publish stock levels". Untracked variants
// (`inventoryManagement: null`, usually paired with `inventoryPolicy: continue`) report a sentinel
// quantity rather than a real one — allbirds' "Free Returns Coverage" comes back as 999999 per
// variant, which summed to 1,981,856 before this filter — so they are excluded from the total.
// Per-variant `inventoryQuantity` is still passed through verbatim; only the roll-up is filtered.
// The filter stays on `inventoryManagement` rather than the derived `inventoryTracked` flag: both
// read the same source field, and keeping the roll-up on the raw value means a future change to
// the flag's three-state shape can never silently change what the total counts.
function totalInventoryOf(variants) {
  const qs = variants.filter((v) => v.inventoryManagement).map((v) => v.inventoryQuantity).filter((n) => typeof n === 'number');
  return qs.length ? qs.reduce((a, b) => a + b, 0) : null;
}
// A single product URL resolves to `/products/<handle>.json`, which uses a DIFFERENT serializer
// from the bulk `/products.json` list route for the very same product: it returns `tags` as one
// comma-separated STRING instead of an array, and omits the per-variant `available` flag
// entirely. Both differences were silent and both were real bugs — a string `tags` is rejected by
// our own dataset schema (`array|null`), which failed the push for the whole store (surfacing as
// `WARN <origin>: Schema validation failed` + 0 products on every single-product-URL run,
// regardless of detailLevel), and a missing `available` made every single-product row read as out
// of stock and be dropped outright under `onlyAvailable`. Normalize both here so a product URL
// yields exactly the same row as the same product fetched from the list route.
const tagsOf = (t) => (Array.isArray(t) ? t : typeof t === 'string' ? t.split(',').map((s) => s.trim()).filter(Boolean) : []);
// Shopify's own availability rule, applied only when the route didn't ship the flag: a variant
// whose stock isn't tracked is always purchasable, a tracked one is available while it has stock
// or the store allows overselling. A tracked variant on a store that hides quantities stays
// unknown (null) — "we can't tell" must not silently become "sold out".
function availableOf(v) {
  if (typeof v.available === 'boolean') return v.available;
  if (!v.inventory_management) return true;
  if (v.inventory_policy === 'continue') return true;
  if (typeof v.inventory_quantity === 'number') return v.inventory_quantity > 0;
  return null;
}
// Unknown availability must not be filtered out as "not available" — the list route always ships
// the flag, so this is identical to the old `some((v) => v.available)` there.
const passesAvailability = (p) => (p.variants ?? []).some((v) => availableOf(v) !== false);
function shape(p, origin, currency, sourceUrl) {
  const variants = (p.variants ?? []).map((v) => ({ id: v.id, title: v.title, sku: v.sku || null, price: Number(v.price), compareAtPrice: v.compare_at_price ? Number(v.compare_at_price) : null, available: availableOf(v), option1: v.option1, option2: v.option2, option3: v.option3, grams: v.grams, requiresShipping: v.requires_shipping, taxable: v.taxable ?? null, position: v.position ?? null, featuredImage: v.featured_image?.src ?? null, ...inventoryFieldsOf(v) }));
  const prices = variants.map((v) => v.price).filter((n) => !Number.isNaN(n));
  const priceMin = prices.length ? Math.min(...prices) : null;
  const comparePrices = variants.map((v) => v.compareAtPrice).filter((x) => x != null).sort((a, b) => a - b);
  const compareAtPriceMin = comparePrices[0] ?? null;
  // Percentage off the list price, from the cheapest variant's own compare-at price (not the
  // catalog-wide min/max, which would mix two different variants and overstate the discount).
  const cheapest = variants.filter((v) => v.price === priceMin).sort((a, b) => (b.compareAtPrice ?? 0) - (a.compareAtPrice ?? 0))[0];
  const discountPercent = cheapest?.compareAtPrice > priceMin
    ? Math.round(((cheapest.compareAtPrice - priceMin) / cheapest.compareAtPrice) * 1000) / 10
    : null;
  // Same rule as discountPercent, applied to the boolean: a product is on sale when SOME single
  // variant is marked down, never when the catalog-wide min compare-at happens to sit above the
  // catalog-wide min price — those two numbers can belong to different variants, so that form can
  // report a sale no variant is actually running (a stale compare-at left below a raised price).
  // Strict > is required: stores do ship variants with compare_at_price EQUAL to price.
  const onSaleVariants = variants.filter((v) => v.compareAtPrice != null && v.compareAtPrice > v.price);
  // Unknown (null) rather than false when no variant's availability could be determined at all,
  // for the same reason `totalInventory` does it: a store that doesn't publish stock must stay
  // distinguishable from one whose products are genuinely sold out.
  const availabilityUnknown = variants.length > 0 && variants.every((v) => v.available === null);
  return {
    id: p.id, title: p.title, handle: p.handle, url: `${origin}/products/${p.handle}`, vendor: p.vendor, productType: p.product_type || null, tags: tagsOf(p.tags),
    currency: currency ?? null,
    priceMin, priceMax: prices.length ? Math.max(...prices) : null,
    compareAtPriceMin, compareAtPriceMax: comparePrices[comparePrices.length - 1] ?? null,
    isOnSale: onSaleVariants.length > 0, discountPercent,
    available: availabilityUnknown ? null : variants.some((v) => v.available === true), availableVariantCount: availabilityUnknown ? null : variants.filter((v) => v.available === true).length, variantCount: variants.length,
    totalInventory: totalInventoryOf(variants),
    images: (p.images ?? []).map((i) => ({ src: i.src, alt: i.alt || null })), imageUrl: p.images?.[0]?.src ?? null, imageCount: (p.images ?? []).length,
    options: (p.options ?? []).map((o) => ({ name: o.name, values: o.values })),
    ...(withVariants ? { variants } : {}), ...(withDesc ? { description: textOf(p.body_html), descriptionHtml: p.body_html || null } : {}),
    createdAt: p.created_at, updatedAt: p.updated_at, publishedAt: p.published_at, store: origin,
    // Which input URL this row came from. With several collections of one store in `storeUrls`,
    // `store` is the same for every row, so this is the only way to tell them apart. A product
    // that appears in more than one of them is returned once, under the FIRST URL that yielded it.
    sourceUrl: sourceUrl ?? null,
    scrapedAt: new Date().toISOString(),
  };
}
// Shopify's public products.json has no full-text query param — there is no server-side
// "search this store's catalog" endpoint that works without an admin token, and the one public
// candidate (predictive /search/suggest.json) caps results at ~10 and is theme-dependent. So a
// keyword search is applied client-side against products already fetched for pagination — zero
// extra requests, works on every store this Actor can already reach, at the cost of still walking
// the full catalog (same request budget as an unfiltered run of the same store).
// A multi-variant product is a price RANGE, not a price, so "between minPrice and maxPrice" means
// the product's range intersects the requested window (a $40-$120 hoodie matches maxPrice:50 —
// there is a buyable variant at $40). Products whose price could not be determined at all
// (priceMin/priceMax null: no variants, or every variant's price unparseable) are dropped when
// either bound is set rather than passed through, so a price-filtered run never returns a row the
// filter could not actually be evaluated against. Prices are in the store's own currency (see the
// `currency` output field) — this Actor does no FX conversion, so a window means different things
// on a USD and a EUR store.
function passesShapedFilters(item) {
  if (onSaleOnly && item.isOnSale !== true) return false;
  if (minPrice != null && !(item.priceMax != null && item.priceMax >= minPrice)) return false;
  if (maxPrice != null && !(item.priceMin != null && item.priceMin <= maxPrice)) return false;
  // Products with no compare-at price have discountPercent:null, not 0 — dropped when a floor is
  // set rather than treated as "0% off passes >=0", so a filtered run never returns a row that
  // isn't actually on sale at all.
  if (minDiscountPercent != null && !(item.discountPercent != null && item.discountPercent >= minDiscountPercent)) return false;
  return true;
}
function matchesSearch(p) {
  if (!searchWords.length) return true;
  const haystack = [p.title, p.vendor, p.product_type, ...(p.tags ?? [])].join(' ').normalize('NFC').toLowerCase();
  return searchWords.every((w) => haystack.includes(w));
}
function matchesVendorType(p) {
  if (vendorsFilter.length) {
    const vendor = String(p.vendor ?? '').normalize('NFC').toLowerCase();
    if (!vendorsFilter.some((v) => vendor.includes(v))) return false;
  }
  if (productTypesFilter.length) {
    const type = String(p.product_type ?? '').normalize('NFC').toLowerCase();
    if (!productTypesFilter.some((t) => type.includes(t))) return false;
  }
  return true;
}
async function currencyFor(origin) {
  try {
    const res = await http(`${origin}/meta.json`);
    return JSON.parse(res.body)?.currency ?? null;
  } catch { return null; }
}

// products.json/product.json never carry SEO tags or a rating summary — Shopify only renders
// those into the live product page's <head> (og/twitter meta) and into a ld+json script (rating
// apps like Judge.me/Yotpo inject their own <script type="application/ld+json"> block alongside
// Shopify's ProductGroup one, so scan all of them for `aggregateRating` rather than assuming
// position). Charged separately since it's a second request per product; only charged when it
// actually finds something, matching the "no data, no charge" rule the base scrape already uses.
//
// The second request hits `/products/<handle>.js` (the storefront AJAX route), not `.json` —
// verified id-for-id on allbirds that `.js` is a strict superset of `.json` for our purposes: it
// carries every stock field `.json` does (barcode/inventory_quantity/management/policy) PLUS
// `quantity_rule` (min/max/increment purchase quantity — real B2B/case-pack data) and top-level
// `selling_plan_groups`/`requires_selling_plan` (subscription plans, via Shopify's native
// subscriptions or an app like Recharge) that `.json` never exposes at all — confirmed live on
// magicspoon.com (native "Subscribe & Save") and cometeer.com (Recharge-backed). Same one request
// either way, just a richer response.
let detailBudgetOk = true;
async function enrichWithDetail(item, origin, handle) {
  if (!detailBudgetOk || !timeBudgetOk()) return;
  let seoTitle = null, seoDescription = null, ratingValue = null, reviewCount = null;
  let detailVariants = [];
  let detailAvailability = []; // every `.js` variant (not just the ones with stock fields) — it always carries `available`
  let hasSubscriptionOption = false, subscriptionPlans = null;
  // Two different routes are needed — the rendered page for <head>/ld+json, the `.js` route for
  // stock/subscription fields — so fire them together. The rest of the run is strictly
  // sequential and full-detail runs are the ones closest to the time budget, so the second
  // request costs no extra wall-clock this way. Settled (not all-or-nothing): a store that serves
  // one route but not the other still gets whatever it does serve.
  const [pageRes, jsRes] = await Promise.allSettled([
    // `request()`'s default Accept header prefers application/json, and Shopify's product route
    // honors that and serves the raw product JSON instead of the rendered page — override it here
    // since the whole point of this request is the page's <head>/ld+json, not the JSON again.
    request(`${origin}/products/${handle}`, { accept: 'text/html,application/xhtml+xml' }),
    request(`${origin}/products/${handle}.js`, { accept: 'application/json' }),
  ]);
  if (pageRes.status === 'rejected') {
    log.warning(`${origin}/products/${handle}: detail fetch failed (${pageRes.reason.message}) — seoTitle/seoDescription/rating left null for this product.`);
  } else {
    try {
      const $ = cheerio.load(pageRes.value.body);
      seoTitle = $('title').first().text().trim() || null;
      seoDescription = $('meta[name="description"]').attr('content')?.trim() || null;
      $('script[type="application/ld+json"]').each((_, el) => {
        if (ratingValue != null) return;
        let data;
        try { data = JSON.parse($(el).contents().text()); } catch { return; }
        const rating = data?.aggregateRating ?? (Array.isArray(data) ? data.find((d) => d?.aggregateRating)?.aggregateRating : null);
        if (rating) {
          ratingValue = rating.ratingValue != null ? Number(rating.ratingValue) : null;
          reviewCount = rating.reviewCount != null ? Number(rating.reviewCount) : (rating.ratingCount != null ? Number(rating.ratingCount) : null);
        }
      });
    } catch (e) {
      log.warning(`${origin}/products/${handle}: could not parse the product page (${e.message}) — seoTitle/seoDescription/rating left null for this product.`);
    }
  }
  if (jsRes.status === 'rejected') {
    log.warning(`${origin}/products/${handle}.js: stock/subscription fields unavailable (${jsRes.reason.message}).`);
  } else if (jsRes.value) {
    try {
      const productJs = JSON.parse(jsRes.value.body);
      detailVariants = (productJs.variants ?? []).filter(hasInventoryData);
      detailAvailability = (productJs.variants ?? []).filter((v) => typeof v.available === 'boolean');
      hasSubscriptionOption = !!productJs.requires_selling_plan || !!productJs.selling_plan_groups?.length;
      if (productJs.selling_plan_groups?.length) {
        subscriptionPlans = productJs.selling_plan_groups.map((g) => ({
          name: g.name,
          plans: (g.selling_plans ?? []).map((sp) => ({
            name: sp.name,
            recurringDeliveries: !!sp.recurring_deliveries,
            discountPercent: sp.price_adjustments?.find((a) => a.value_type === 'percentage')?.value ?? null,
          })),
        }));
      }
    } catch (e) { log.warning(`${origin}/products/${handle}.js: stock/subscription fields unavailable (${e.message}).`); }
  }
  if (seoTitle == null && seoDescription == null && ratingValue == null && !detailVariants.length && !hasSubscriptionOption) return; // nothing found, nothing charged
  if (isPPE) {
    const r = await Actor.charge({ eventName: 'productDetail', count: 1 });
    if (r.chargedCount === 0) { detailBudgetOk = false; return; } // budget exhausted: stop enriching, keep scraping base data
  }
  item.seoTitle = seoTitle; item.seoDescription = seoDescription; item.ratingValue = ratingValue; item.reviewCount = reviewCount;
  item.hasSubscriptionOption = hasSubscriptionOption; item.subscriptionPlans = subscriptionPlans;
  // The `.js` route always carries a real `available` flag, so a full-detail run can resolve what
  // the base route left unknown (stores that hide inventory quantities) at no extra request. Only
  // fills in nulls — a flag the base route did ship is never overridden.
  if (item.available === null && detailAvailability.length) {
    item.available = detailAvailability.some((v) => v.available === true);
    item.availableVariantCount = detailAvailability.filter((v) => v.available === true).length;
    const availById = new Map(detailAvailability.map((v) => [v.id, v.available]));
    for (const v of item.variants ?? []) if (v.available === null && availById.has(v.id)) v.available = availById.get(v.id);
  }
  if (detailVariants.length) {
    const byId = new Map(detailVariants.map((v) => [v.id, v]));
    for (const v of item.variants ?? []) { // absent when includeVariants is off — totalInventory still lands
      const d = byId.get(v.id);
      if (d) Object.assign(v, inventoryFieldsOf(d));
    }
    item.totalInventory = totalInventoryOf(detailVariants.map(inventoryFieldsOf));
  }
}

const erroredStores = []; // products.json fetch failed (not Shopify, or endpoint disabled)
const emptyStores = []; // request succeeded but Shopify returned zero products for this URL
const filteredOutStores = []; // products existed but onlyAvailable removed all of them
// One structured record per input URL, so a machine reading this run can tell the outcomes apart
// WITHOUT parsing the English status message. Zero rows has at least six different causes here —
// endpoint disabled, genuinely empty collection, filters removed everything, every product already
// returned by an earlier URL, a watch run with no changes, a fetch failure — and collapsing them
// into one empty dataset is exactly the bug this Actor's own docs warn buyers about. A later
// successful retry must not look like "inventory suddenly appeared", so status, scanned and
// delivered are three separate fields, never re-derived from the row count.
const sourceOutcomes = [];
// One shape for every outcome (KV-store/webhook bookkeeping, never a dataset row), so a URL that
// was never fetched carries the same keys as one that succeeded — a consumer can read `status`
// without first checking which keys exist.
const sourceSummary = (url, store, status, extra = {}) => ({
  url, store, status, scanned: 0, delivered: 0, duplicates: 0, complete: false, reason: null, ...extra,
});
let keepGoing = true;
for (const raw of storeUrls) {
  if (!keepGoing) break;
  if (!timeBudgetOk()) { log.warning('Approaching the run timeout — stopping early and returning what has been collected so far.'); break; }
  let ep;
  try { ep = endpointFor(raw); } catch {
    log.warning(`Bad URL: ${raw}`);
    sourceOutcomes.push(sourceSummary(raw, null, 'badUrl', { reason: 'not a parseable http(s) URL' }));
    continue;
  }
  rawForEndpoint.set(ep.url, raw);
  let outcome = 'ok';
  let outcomeReason = null;
  let got = 0;
  let dupThisUrl = 0; // products this URL returned that an earlier URL in this run already delivered
  let seenBeforeFilter = 0;
  // A store URL that isn't in this label's baseline yet (first run, or a URL added to an existing
  // label) is recorded, not delivered — otherwise adding one store to a watch would bill the
  // buyer for that store's entire catalog as "new products".
  const storeSeeding = watchMode && !seededStores.has(ep.url);
  if (storeSeeding && watchRecord?.runCount) log.info(`${ep.origin}: not in the baseline for "${watchLabel}" yet — baselining this store this run instead of reporting its whole catalog as new.`);
  // Every product id this store's feed returned, before any filter, plus whether the sweep actually
  // reached the end of the feed. Only both together license a "delisted" verdict below.
  const seenAllIds = new Set();
  let sweptToEnd = false;
  try {
    const currency = await currencyFor(ep.origin);
    if (ep.kind === 'product') {
      const p = JSON.parse(throwIfStorefrontError(await http(ep.url)).body).product;
      if (p && seenProducts.has(productKey(ep.origin, p.id))) {
        // The product exists — it was just already delivered by an earlier URL. Count it as seen,
        // or this URL would be reported as an empty store ("products.json disabled") instead.
        seenBeforeFilter = 1;
        duplicateProducts += 1; dupThisUrl += 1;
        log.info(`${raw}: already returned by ${seenProducts.get(productKey(ep.origin, p.id))} in this run — not returned again, not charged again.`);
      } else if (p) {
        seenBeforeFilter = 1;
        seenProducts.set(productKey(ep.origin, p.id), raw);
        if (!onlyAvailable || passesAvailability(p)) {
          const item = shape(p, ep.origin, currency, raw);
          // Price/sale filters run here, before the paid `detailLevel:"full"` fetch and before
          // pushResult() charges — enrichment only writes SEO/rating/subscription fields, never
          // the price fields these read, so evaluating them early cannot change the verdict.
          if (passesShapedFilters(item)) {
            // Watch mode runs on the shaped row (it compares priceMin/available) but before the
            // paid `detailLevel:"full"` fetch and before pushResult() charges, so an unchanged
            // product costs the buyer nothing at all.
            const verdict = watchMode ? watchVerdict(item, storeSeeding, ep.url) : {};
            if (verdict) {
              Object.assign(item, verdict);
              // Unlike inventory fields, subscription/quantity-rule data only lives on the `.js`
              // route, not `.json` — so even a single-product URL (which already has `.json`) still
              // needs the enrichment step's own fetch to pick those up.
              if (detailLevel === 'full') await enrichWithDetail(item, ep.origin, p.handle);
              keepGoing = await pushResult(item); got++;
            }
          }
        }
      }
    } else {
      // In watch mode almost every product is unchanged, so `got` (rows delivered) stops being a
      // usable page cap — the sweep has to walk the catalog to find the changes. maxProductsPerStore
      // therefore caps products SCANNED per store in watch mode, and products RETURNED otherwise.
      const scanCapped = () => (watchMode ? seenBeforeFilter >= perStore : got >= perStore);
      for (let page = 1; !scanCapped() && keepGoing; page++) {
        if (!timeBudgetOk()) { log.warning('Approaching the run timeout — stopping early and returning what has been collected so far.'); keepGoing = false; break; }
        const products = await fetchProductsPage(ep, page);
        // An empty page after page 1 is the end of the feed (page 1 is re-confirmed inside
        // fetchProductsPage), so the sweep is complete — that is exactly the "store emptied" case.
        if (!products.length) { sweptToEnd = true; break; }
        seenBeforeFilter += products.length;
        for (const p of products) {
          seenAllIds.add(String(p.id)); // coverage is measured BEFORE the filters, never after
          if (!watchMode && got >= perStore) break;
          // Before every filter, before watch mode and before charging: a product an earlier URL
          // in this run already delivered is skipped outright, so overlapping collections cost
          // one result per product, not one per collection it appears in.
          const key = productKey(ep.origin, p.id);
          if (seenProducts.has(key)) { duplicateProducts += 1; dupThisUrl += 1; continue; }
          seenProducts.set(key, raw);
          if (onlyAvailable && !passesAvailability(p)) continue;
          if (!matchesSearch(p)) continue;
          if (!matchesVendorType(p)) continue;
          const item = shape(p, ep.origin, currency, raw);
          if (!passesShapedFilters(item)) continue; // before enrichment/charging: never bill a filtered-out product
          const verdict = watchMode ? watchVerdict(item, storeSeeding, ep.url) : {};
          if (!verdict) continue; // watch mode: recorded in the baseline, never pushed, never charged
          Object.assign(item, verdict);
          if (detailLevel === 'full') await enrichWithDetail(item, ep.origin, p.handle);
          keepGoing = await pushResult(item); got++;
          if (!keepGoing) break;
        }
        if (!keepGoing) break; // maxResults / PPE budget stopped us mid-page: the sweep is NOT complete
        if (products.length < 250) { sweptToEnd = true; break; }
      }
      if (watchMode && seenBeforeFilter >= perStore) log.warning(`${ep.origin}: stopped after scanning ${seenBeforeFilter} products (maxProductsPerStore = ${perStore}). In watch mode that cap limits how deep the diff looks — raise it to cover the whole catalog, or changes to products further down the feed will be missed.`);
    }
    if (seenBeforeFilter === 0) {
      emptyStores.push(ep.origin);
      outcome = 'empty';
      outcomeReason = 'Shopify returned zero products (empty store/collection, or products.json is disabled)';
      // Only the paged store/collection route re-confirms an empty first page; don't claim retries
      // that the single-product route never made.
      const attempts = ep.kind === 'product' ? '' : ` on ${EMPTY_PAGE_RETRIES + 1} separate attempts`;
      log.warning(`${ep.origin}: Shopify returned zero products for this URL${attempts} (empty store/collection, or products.json is disabled — not a scrape failure).`);
    } else if (got === 0 && watchMode) {
      // The normal, healthy watch outcome — not a filter problem, so it must not be reported as one.
      outcome = storeSeeding ? 'watchBaselined' : 'watchNoChanges';
      log.info(storeSeeding
        ? `${ep.origin}: recorded ${seenBeforeFilter} products as the baseline for "${watchLabel}" (nothing delivered, nothing charged).`
        : `${ep.origin}: scanned ${seenBeforeFilter} products, no changes matching "${[...watchEvents].join(', ')}" since the last run under "${watchLabel}".`);
    } else if (got === 0 && dupThisUrl >= seenBeforeFilter) {
      // Every product behind this URL was already delivered by an earlier URL in this run. That is
      // a correct and complete result for this URL, so it must not be reported as "filters removed
      // everything" (which would send the buyer off relaxing filters that did nothing).
      outcome = 'duplicate';
      outcomeReason = 'every product behind this URL was already returned by an earlier URL in this run';
      log.info(`${ep.origin}: every product for this URL (${seenBeforeFilter}) was already returned by an earlier URL in this run — nothing new to return or charge.`);
    } else if (got === 0) {
      filteredOutStores.push(ep.origin);
      outcome = 'filteredOut';
      // Name every filter that was actually set, so a zero-row run says which input to relax
      // instead of blaming whichever one this message happened to hardcode.
      const activeFilters = [
        ...(onlyAvailable ? ['"onlyAvailable"'] : []),
        ...(searchWords.length ? ['"searchQuery"'] : []),
        ...(vendorsFilter.length ? [`"vendors" (${vendorsFilter.join(', ')})`] : []),
        ...(productTypesFilter.length ? [`"productTypes" (${productTypesFilter.join(', ')})`] : []),
        ...(minPrice != null ? [`"minPrice" (${minPrice})`] : []),
        ...(maxPrice != null ? [`"maxPrice" (${maxPrice})`] : []),
        ...(onSaleOnly ? ['"onSaleOnly"'] : []),
        ...(minDiscountPercent != null ? [`"minDiscountPercent" (${minDiscountPercent})`] : []),
      ];
      const reason = activeFilters.length === 1
        ? `${activeFilters[0]} removed all of them`
        : `${activeFilters.join(' / ')} removed all of them between them`;
      outcomeReason = reason;
      log.warning(`${ep.origin}: fetched ${seenBeforeFilter} products but ${reason}.`);
    }
  } catch (e) {
    erroredStores.push(ep.origin);
    outcome = 'error';
    // got-scraping doesn't throw on 4xx/redirect-to-HTML, so a headless/custom storefront
    // (e.g. Shopify Hydrogen/Oxygen, which has no classic Liquid products.json route) or a
    // bot-check page shows up here as a JSON.parse SyntaxError, not a request-level error —
    // give that its own message instead of surfacing the raw "Unexpected token '<'".
    const reason = e.storefrontStatus
      ? e.message // already a customer-ready sentence naming the real cause; don't bolt "may not be Shopify" onto it
      : e instanceof SyntaxError && /Unexpected token '<'/.test(e.message)
        ? 'this URL returned an HTML page instead of JSON — likely a headless/custom storefront (e.g. Shopify Hydrogen) without the classic products.json endpoint, or a bot-check page. Not a failure on our end.'
        : `${e.message} (store may not be Shopify or has products.json disabled)`;
    outcomeReason = reason;
    log.warning(`${ep.origin}: ${reason}`);
  }
  // `complete` = "this URL's feed was read to the end", which licenses a delisted verdict and
  // tells a consumer the counts are the whole picture. The paged route only earns it by seeing a
  // short final page (`sweptToEnd`); a single-product URL earns it by answering at all, since one
  // product IS its whole feed — reusing `sweptToEnd` there would report every healthy
  // single-product run as truncated.
  const complete = ep.kind === 'product' ? outcome !== 'error' && seenBeforeFilter > 0 : sweptToEnd;
  sourceOutcomes.push(sourceSummary(raw, ep.origin, outcome, { scanned: seenBeforeFilter, delivered: got, duplicates: dupThisUrl, complete, reason: outcomeReason }));
  // Only a store that actually answered joins the baseline. A store that errored stays unseeded,
  // so the next run baselines it properly instead of announcing its whole catalog as "new".
  if (watchMode && seenBeforeFilter > 0) seededStores.add(ep.url);
  // A store this run both walked end-to-end AND already had a baseline for can be asked "what is
  // gone". A store being seeded this run cannot (it has no prior baseline of its own), and neither
  // can a capped, truncated or errored sweep — sweptToEnd stays false in every one of those.
  if (watchMode && sweptToEnd && !storeSeeding) watchStoreSweeps.set(ep.url, seenAllIds);
  log.info(`${ep.origin}: ${got} products`);
}
// A URL the run stopped before reaching (time budget, maxResults, or the PPE budget) has no
// outcome at all — leaving it out of `sourceOutcomes` would let a consumer read its absence as
// "nothing there" rather than "never looked".
for (const raw of storeUrls.slice(sourceOutcomes.length)) {
  sourceOutcomes.push(sourceSummary(raw, null, 'notReached', { reason: 'the run stopped before this URL (time limit, maxResults, or charge budget)' }));
}
if (sourceOutcomes.some((s) => s.status === 'notReached')) {
  log.warning(`${sourceOutcomes.filter((s) => s.status === 'notReached').length} of your ${storeUrls.length} storeUrls were never fetched — this run stopped early. They are reported as "notReached", not as empty.`);
}
// ---- delisted: products that were in the baseline and are no longer in a COMPLETE sweep ---------
// Runs after every store so it can compare against the finished coverage picture. Each row is a
// normal billable result, so the bar for producing one is coverage proof, not absence.
if (watchMode && watchEvents.has('delisted') && watchStoreSweeps.size && keepGoing) {
  for (const [storeUrl, seen] of watchStoreSweeps) {
    if (!keepGoing) break;
    const origin = new URL(storeUrl).origin;
    const gone = [];
    let baselineForStore = 0;
    for (const [id, v] of watchPrev) {
      if (v.store !== storeUrl) continue; // incl. legacy records with no attribution yet
      baselineForStore += 1;
      // Missing from THIS URL's feed but returned by another URL of the same store this run means
      // it left a collection, not the store — reporting that as "delisted" would be a wrong (and
      // billed) verdict. Its attribution stays with the URL that saw it this run.
      if (!seen.has(id) && !seenProducts.has(productKey(origin, id))) gone.push([id, v]);
    }
    if (!gone.length) continue;
    if (gone.length > DELIST_SUSPICIOUS_MIN && gone.length > baselineForStore * DELIST_SUSPICIOUS_SHARE) {
      log.warning(
        `${origin}: ${gone.length} of ${baselineForStore} baselined products are missing from a complete sweep. That is too large a share `
        + 'to call "delisted" — a collection being emptied or re-scoped looks identical — so no delisted rows were produced and nothing was '
        + 'charged for them. They stay in the baseline; if they are genuinely gone they will still be missing next run.',
      );
      continue;
    }
    for (const [id, v] of gone) {
      const numericId = Number(id);
      const delistedRow = {
        id: Number.isFinite(numericId) ? numericId : null,
        title: null,
        handle: v.handle ?? null,
        // The baseline keeps the handle, not the title, so a delisted row is still clickable (the
        // URL 404s by definition — it is there to identify the product, not to visit).
        url: v.handle ? `${origin}/products/${v.handle}` : null,
        store: origin,
        sourceUrl: rawForEndpoint.get(storeUrl) ?? storeUrl,
        priceMin: null,
        available: null,
        watchLabel,
        watchChange: 'delisted',
        watchChanges: ['delisted'],
        previousPriceMin: v.price,
        previousAvailable: v.avail,
        priceChange: null,
        scrapedAt: new Date().toISOString(),
      };
      const before = pushed;
      keepGoing = await pushResult(delistedRow);
      // Only a row that actually landed leaves the baseline — pushResult also returns false when
      // the buyer's PPE budget is exhausted and NOTHING was pushed, and dropping it then would
      // lose the product silently.
      if (pushed > before) { watchCounts.delisted += 1; watchDeliveredDelisted.add(id); }
      if (!keepGoing) break;
    }
    log.info(`${origin}: ${watchCounts.delisted} product(s) reported as delisted so far (${gone.length} missing from a complete sweep of ${baselineForStore} baselined).`);
  }
}
if (watchMode) {
  await saveWatchRecord();
  const breakdown = WATCH_EVENTS.filter((e) => watchCounts[e]).map((e) => `${e}: ${watchCounts[e]}`).join(', ') || 'none';
  log.info(`Watch "${watchLabel}": ${breakdown}. Unchanged and not charged: ${watchUnchanged}.${watchEventsFiltered ? ` Changed but excluded by watchEvents: ${watchEventsFiltered}.` : ''}${watchSeededThisRun ? ` Baselined this run: ${watchSeededThisRun}.` : ''}`);
}
if (duplicateProducts) {
  log.info(
    `${duplicateProducts} product(s) appeared in more than one of your storeUrls (e.g. a product in both `
    + '"/collections/all" and a category collection). Each product is returned once per run, under the first URL that '
    + 'returned it (see the "sourceUrl" field) — the repeats were not pushed and not charged.',
  );
}
log.info(`Done. Pushed ${pushed} products.`);
const timeBudgetNote = timeBudgetExceeded ? ' Stopped early: approaching the run time limit — reduce storeUrls / maxProductsPerStore to get a complete run.' : '';
if (watchMode && pushed === 0 && !erroredStores.length && !timeBudgetExceeded) {
  await Actor.setStatusMessage(watchSeededThisRun
    ? `Baseline run for watch "${watchLabel}": recorded ${watchSeededThisRun} products, returned 0, charged 0. Re-run under the same label to get only what changed.`
    : `Watch "${watchLabel}": no changes since the last run (${watchUnchanged} products unchanged, 0 charged).`);
} else if (pushed === 0 && storeUrls.length && !timeBudgetExceeded) {
  const why = erroredStores.length
    ? `fetching products failed for: ${erroredStores.join(', ')} (store may not be Shopify, or products.json is disabled)`
    : filteredOutStores.length && !emptyStores.length
      ? 'products were found but the filters you set ("onlyAvailable"/"searchQuery"/"vendors"/"productTypes"/"minPrice"/"maxPrice"/"onSaleOnly"/"minDiscountPercent") removed all of them'
      : `Shopify returned zero products for: ${emptyStores.join(', ')}`;
  await Actor.setStatusMessage(`No products returned — ${why}. See the log for details.`);
} else if (pushed === 0 && timeBudgetExceeded) {
  await Actor.setStatusMessage(`No products returned before the run approached its time limit.${timeBudgetNote}`);
} else if (emptyStores.length || filteredOutStores.length || erroredStores.length || timeBudgetExceeded) {
  await Actor.setStatusMessage(`Pushed ${pushed} products. Issues: ${[...emptyStores.map((s) => `${s} (empty)`), ...filteredOutStores.map((s) => `${s} (filtered out)`), ...erroredStores.map((s) => `${s} (error)`)].join(', ')}.${timeBudgetNote}`);
}

// The same per-URL outcomes as the webhook, written to the run's default key-value store so a
// consumer that polls runs (rather than receiving a webhook) can read them too:
// GET /v2/actor-runs/<runId>/key-value-store/records/RUN_SUMMARY. This is the only machine-readable
// way to tell an empty dataset's causes apart — the status message is prose for humans.
const runSummary = {
  finishedAt: new Date().toISOString(),
  pushed,
  duplicateProducts,
  storesRequested: storeUrls.length,
  timeBudgetExceeded,
  watchLabel: watchMode ? watchLabel : null,
  watchSeeding: watchMode ? watchSeededThisRun > 0 : null,
  sources: sourceOutcomes,
};
await Actor.setValue('RUN_SUMMARY', runSummary);

// Fires after every row is already pushed and charged, so a slow or failing webhook can never
// affect the result set or the bill — best-effort only, one attempt, short timeout, failures are
// a warning not a thrown error. A run that ends in Actor.fail() sends nothing, so this answers
// "what did this run find", not "did it run".
if (webhookUrl) {
  const env = Actor.getEnv();
  const payload = {
    actorRunId: env.actorRunId ?? null,
    defaultDatasetId: env.defaultDatasetId ?? null,
    finishedAt: new Date().toISOString(),
    pushed,
    duplicateProducts,
    storesScraped: storeUrls.length,
    erroredStores,
    emptyStores,
    filteredOutStores,
    sources: sourceOutcomes,
    watchLabel: watchMode ? watchLabel : null,
    watchSeeding: watchMode ? watchSeededThisRun > 0 : null,
    watchChangeCounts: watchMode ? watchCounts : null,
    watchUnchanged: watchMode ? watchUnchanged : null,
  };
  try {
    const resp = await gotScraping({
      url: webhookUrl,
      method: 'POST',
      responseType: 'text',
      throwHttpErrors: false,
      retry: { limit: 0 },
      timeout: { request: 10000 },
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (resp.statusCode >= 400) log.warning(`webhookUrl POST returned ${resp.statusCode}; run result is unaffected.`);
    else log.info(`Posted completion summary to webhookUrl (${resp.statusCode}).`);
  } catch (err) {
    log.warning(`webhookUrl POST failed (${err.message}); run result is unaffected.`);
  }
}

await Actor.exit();
