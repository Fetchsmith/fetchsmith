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
const hasShapedFilters = minPrice != null || maxPrice != null || onSaleOnly;
if (!storeUrls.length) await Actor.fail('Provide at least one store URL.');
if (duplicateStoreUrls) log.info(`Skipped ${duplicateStoreUrls} duplicate storeUrls entr${duplicateStoreUrls === 1 ? 'y' : 'ies'} (same endpoint already queued).`);

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
const request = async (url, headers) => gotScraping({ url, timeout: { request: 40000 }, retry: { limit: 2 }, proxyUrl: await proxyUrlFor(), headers: { accept: 'application/json,text/html', ...headers } });
const http = async (url) => {
  try { return await request(url, { 'accept-language': '' }); }
  catch (e) { return request(url, {}); } // a store that rejects the empty header still gets served, just without sale prices
};
const textOf = (html) => (html ? cheerio.load(html).text().replace(/\s+/g, ' ').trim() : null);

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
function shape(p, origin, currency) {
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
  // Unknown (null) rather than false when no variant's availability could be determined at all,
  // for the same reason `totalInventory` does it: a store that doesn't publish stock must stay
  // distinguishable from one whose products are genuinely sold out.
  const availabilityUnknown = variants.length > 0 && variants.every((v) => v.available === null);
  return {
    id: p.id, title: p.title, handle: p.handle, url: `${origin}/products/${p.handle}`, vendor: p.vendor, productType: p.product_type || null, tags: tagsOf(p.tags),
    currency: currency ?? null,
    priceMin, priceMax: prices.length ? Math.max(...prices) : null,
    compareAtPriceMin, compareAtPriceMax: comparePrices[comparePrices.length - 1] ?? null,
    isOnSale: !!(compareAtPriceMin != null && priceMin != null && compareAtPriceMin > priceMin), discountPercent,
    available: availabilityUnknown ? null : variants.some((v) => v.available === true), availableVariantCount: availabilityUnknown ? null : variants.filter((v) => v.available === true).length, variantCount: variants.length,
    totalInventory: totalInventoryOf(variants),
    images: (p.images ?? []).map((i) => ({ src: i.src, alt: i.alt || null })), imageUrl: p.images?.[0]?.src ?? null, imageCount: (p.images ?? []).length,
    options: (p.options ?? []).map((o) => ({ name: o.name, values: o.values })),
    ...(withVariants ? { variants } : {}), ...(withDesc ? { description: textOf(p.body_html), descriptionHtml: p.body_html || null } : {}),
    createdAt: p.created_at, updatedAt: p.updated_at, publishedAt: p.published_at, store: origin, scrapedAt: new Date().toISOString(),
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
  return true;
}
function matchesSearch(p) {
  if (!searchWords.length) return true;
  const haystack = [p.title, p.vendor, p.product_type, ...(p.tags ?? [])].join(' ').normalize('NFC').toLowerCase();
  return searchWords.every((w) => haystack.includes(w));
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
let keepGoing = true;
for (const raw of storeUrls) {
  if (!keepGoing) break;
  if (!timeBudgetOk()) { log.warning('Approaching the run timeout — stopping early and returning what has been collected so far.'); break; }
  let ep; try { ep = endpointFor(raw); } catch { log.warning(`Bad URL: ${raw}`); continue; }
  let got = 0;
  let seenBeforeFilter = 0;
  try {
    const currency = await currencyFor(ep.origin);
    if (ep.kind === 'product') {
      const p = JSON.parse((await http(ep.url)).body).product;
      if (p) {
        seenBeforeFilter = 1;
        if (!onlyAvailable || passesAvailability(p)) {
          const item = shape(p, ep.origin, currency);
          // Price/sale filters run here, before the paid `detailLevel:"full"` fetch and before
          // pushResult() charges — enrichment only writes SEO/rating/subscription fields, never
          // the price fields these read, so evaluating them early cannot change the verdict.
          if (passesShapedFilters(item)) {
            // Unlike inventory fields, subscription/quantity-rule data only lives on the `.js`
            // route, not `.json` — so even a single-product URL (which already has `.json`) still
            // needs the enrichment step's own fetch to pick those up.
            if (detailLevel === 'full') await enrichWithDetail(item, ep.origin, p.handle);
            keepGoing = await pushResult(item); got++;
          }
        }
      }
    } else {
      for (let page = 1; got < perStore && keepGoing; page++) {
        if (!timeBudgetOk()) { log.warning('Approaching the run timeout — stopping early and returning what has been collected so far.'); keepGoing = false; break; }
        const res = await http(`${ep.url}?limit=250&page=${page}`);
        const products = JSON.parse(res.body).products ?? [];
        if (!products.length) break;
        seenBeforeFilter += products.length;
        for (const p of products) {
          if (got >= perStore) break;
          if (onlyAvailable && !passesAvailability(p)) continue;
          if (!matchesSearch(p)) continue;
          const item = shape(p, ep.origin, currency);
          if (!passesShapedFilters(item)) continue; // before enrichment/charging: never bill a filtered-out product
          if (detailLevel === 'full') await enrichWithDetail(item, ep.origin, p.handle);
          keepGoing = await pushResult(item); got++;
          if (!keepGoing) break;
        }
        if (products.length < 250) break;
      }
    }
    if (seenBeforeFilter === 0) {
      emptyStores.push(ep.origin);
      log.warning(`${ep.origin}: Shopify returned zero products for this URL (empty store/collection, or products.json is disabled — not a scrape failure).`);
    } else if (got === 0) {
      filteredOutStores.push(ep.origin);
      // Name every filter that was actually set, so a zero-row run says which input to relax
      // instead of blaming whichever one this message happened to hardcode.
      const activeFilters = [
        ...(onlyAvailable ? ['"onlyAvailable"'] : []),
        ...(searchWords.length ? ['"searchQuery"'] : []),
        ...(minPrice != null ? [`"minPrice" (${minPrice})`] : []),
        ...(maxPrice != null ? [`"maxPrice" (${maxPrice})`] : []),
        ...(onSaleOnly ? ['"onSaleOnly"'] : []),
      ];
      const reason = activeFilters.length === 1
        ? `${activeFilters[0]} removed all of them`
        : `${activeFilters.join(' / ')} removed all of them between them`;
      log.warning(`${ep.origin}: fetched ${seenBeforeFilter} products but ${reason}.`);
    }
  } catch (e) {
    erroredStores.push(ep.origin);
    // got-scraping doesn't throw on 4xx/redirect-to-HTML, so a headless/custom storefront
    // (e.g. Shopify Hydrogen/Oxygen, which has no classic Liquid products.json route) or a
    // bot-check page shows up here as a JSON.parse SyntaxError, not a request-level error —
    // give that its own message instead of surfacing the raw "Unexpected token '<'".
    const reason = e instanceof SyntaxError && /Unexpected token '<'/.test(e.message)
      ? 'this URL returned an HTML page instead of JSON — likely a headless/custom storefront (e.g. Shopify Hydrogen) without the classic products.json endpoint, or a bot-check page. Not a failure on our end.'
      : `${e.message} (store may not be Shopify or has products.json disabled)`;
    log.warning(`${ep.origin}: ${reason}`);
  }
  log.info(`${ep.origin}: ${got} products`);
}
log.info(`Done. Pushed ${pushed} products.`);
const timeBudgetNote = timeBudgetExceeded ? ' Stopped early: approaching the run time limit — reduce storeUrls / maxProductsPerStore to get a complete run.' : '';
if (pushed === 0 && storeUrls.length && !timeBudgetExceeded) {
  const why = erroredStores.length
    ? `fetching products failed for: ${erroredStores.join(', ')} (store may not be Shopify, or products.json is disabled)`
    : filteredOutStores.length && !emptyStores.length
      ? 'products were found but the filters you set ("onlyAvailable"/"searchQuery"/"minPrice"/"maxPrice"/"onSaleOnly") removed all of them'
      : `Shopify returned zero products for: ${emptyStores.join(', ')}`;
  await Actor.setStatusMessage(`No products returned — ${why}. See the log for details.`);
} else if (pushed === 0 && timeBudgetExceeded) {
  await Actor.setStatusMessage(`No products returned before the run approached its time limit.${timeBudgetNote}`);
} else if (emptyStores.length || filteredOutStores.length || erroredStores.length || timeBudgetExceeded) {
  await Actor.setStatusMessage(`Pushed ${pushed} products. Issues: ${[...emptyStores.map((s) => `${s} (empty)`), ...filteredOutStores.map((s) => `${s} (filtered out)`), ...erroredStores.map((s) => `${s} (error)`)].join(', ')}.${timeBudgetNote}`);
}
await Actor.exit();
