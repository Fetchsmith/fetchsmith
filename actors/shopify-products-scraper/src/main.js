import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';
import * as cheerio from 'cheerio';

await Actor.init();
const input = (await Actor.getInput()) ?? {};
const storeUrls = (input.storeUrls ?? []).map((s) => String(s).trim()).filter(Boolean);
const perStore = Math.min(Number(input.maxProductsPerStore ?? 500), 100000);
const maxResults = Math.min(Number(input.maxResults ?? 5000), 200000);
const withDesc = input.includeDescription !== false;
const withVariants = input.includeVariants !== false;
const onlyAvailable = !!input.onlyAvailable;
const detailLevel = input.detailLevel === 'full' ? 'full' : 'basic';
const searchQuery = String(input.searchQuery ?? '').trim();
const searchWords = searchQuery ? searchQuery.toLowerCase().split(/\s+/).filter(Boolean) : [];
if (!storeUrls.length) await Actor.fail('Provide at least one store URL.');

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
function shape(p, origin, currency) {
  const variants = (p.variants ?? []).map((v) => ({ id: v.id, title: v.title, sku: v.sku || null, price: Number(v.price), compareAtPrice: v.compare_at_price ? Number(v.compare_at_price) : null, available: v.available ?? null, option1: v.option1, option2: v.option2, option3: v.option3, grams: v.grams, requiresShipping: v.requires_shipping, taxable: v.taxable ?? null, position: v.position ?? null, featuredImage: v.featured_image?.src ?? null }));
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
  return {
    id: p.id, title: p.title, handle: p.handle, url: `${origin}/products/${p.handle}`, vendor: p.vendor, productType: p.product_type || null, tags: p.tags ?? [],
    currency: currency ?? null,
    priceMin, priceMax: prices.length ? Math.max(...prices) : null,
    compareAtPriceMin, compareAtPriceMax: comparePrices[comparePrices.length - 1] ?? null,
    isOnSale: !!(compareAtPriceMin != null && priceMin != null && compareAtPriceMin > priceMin), discountPercent,
    available: variants.some((v) => v.available), availableVariantCount: variants.filter((v) => v.available).length, variantCount: variants.length,
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
function matchesSearch(p) {
  if (!searchWords.length) return true;
  const haystack = [p.title, p.vendor, p.product_type, ...(p.tags ?? [])].join(' ').toLowerCase();
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
let detailBudgetOk = true;
async function enrichWithDetail(item, origin, handle) {
  if (!detailBudgetOk || !timeBudgetOk()) return;
  let seoTitle = null, seoDescription = null, ratingValue = null, reviewCount = null;
  try {
    // `request()`'s default Accept header prefers application/json, and Shopify's product route
    // honors that and serves the raw product JSON instead of the rendered page — override it here
    // since the whole point of this request is the page's <head>/ld+json, not the JSON again.
    const res = await request(`${origin}/products/${handle}`, { accept: 'text/html,application/xhtml+xml' });
    const $ = cheerio.load(res.body);
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
    log.warning(`${origin}/products/${handle}: detail fetch failed (${e.message}) — seoTitle/seoDescription/rating left null for this product.`);
    return;
  }
  if (seoTitle == null && seoDescription == null && ratingValue == null) return; // nothing found, nothing charged
  if (isPPE) {
    const r = await Actor.charge({ eventName: 'productDetail', count: 1 });
    if (r.chargedCount === 0) { detailBudgetOk = false; return; } // budget exhausted: stop enriching, keep scraping base data
  }
  item.seoTitle = seoTitle; item.seoDescription = seoDescription; item.ratingValue = ratingValue; item.reviewCount = reviewCount;
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
        if (!onlyAvailable || (p.variants ?? []).some((v) => v.available)) {
          const item = shape(p, ep.origin, currency);
          if (detailLevel === 'full') await enrichWithDetail(item, ep.origin, p.handle);
          keepGoing = await pushResult(item); got++;
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
          if (onlyAvailable && !(p.variants ?? []).some((v) => v.available)) continue;
          if (!matchesSearch(p)) continue;
          const item = shape(p, ep.origin, currency);
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
      const reason = onlyAvailable && searchWords.length ? '"onlyAvailable" and/or "searchQuery" removed all of them' : onlyAvailable ? '"onlyAvailable" removed all of them (none are in stock)' : '"searchQuery" matched none of them';
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
      ? 'products were found but "onlyAvailable"/"searchQuery" removed all of them'
      : `Shopify returned zero products for: ${emptyStores.join(', ')}`;
  await Actor.setStatusMessage(`No products returned — ${why}. See the log for details.`);
} else if (pushed === 0 && timeBudgetExceeded) {
  await Actor.setStatusMessage(`No products returned before the run approached its time limit.${timeBudgetNote}`);
} else if (emptyStores.length || filteredOutStores.length || erroredStores.length || timeBudgetExceeded) {
  await Actor.setStatusMessage(`Pushed ${pushed} products. Issues: ${[...emptyStores.map((s) => `${s} (empty)`), ...filteredOutStores.map((s) => `${s} (filtered out)`), ...erroredStores.map((s) => `${s} (error)`)].join(', ')}.${timeBudgetNote}`);
}
await Actor.exit();
