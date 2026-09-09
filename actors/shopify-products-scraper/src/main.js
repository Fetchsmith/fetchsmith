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
if (!storeUrls.length) await Actor.fail('Provide at least one store URL.');

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
const http = (url) => gotScraping({ url, timeout: { request: 40000 }, retry: { limit: 2 }, headers: { accept: 'application/json,text/html' } });
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
function shape(p, origin) {
  const variants = (p.variants ?? []).map((v) => ({ id: v.id, title: v.title, sku: v.sku || null, price: Number(v.price), compareAtPrice: v.compare_at_price ? Number(v.compare_at_price) : null, available: v.available ?? null, option1: v.option1, option2: v.option2, option3: v.option3, grams: v.grams, requiresShipping: v.requires_shipping }));
  const prices = variants.map((v) => v.price).filter((n) => !Number.isNaN(n));
  return {
    id: p.id, title: p.title, handle: p.handle, url: `${origin}/products/${p.handle}`, vendor: p.vendor, productType: p.product_type || null, tags: p.tags ?? [],
    priceMin: prices.length ? Math.min(...prices) : null, priceMax: prices.length ? Math.max(...prices) : null,
    compareAtPriceMin: variants.map((v) => v.compareAtPrice).filter((x) => x != null).sort((a, b) => a - b)[0] ?? null,
    available: variants.some((v) => v.available), variantCount: variants.length,
    images: (p.images ?? []).map((i) => i.src), imageUrl: p.images?.[0]?.src ?? null,
    options: (p.options ?? []).map((o) => ({ name: o.name, values: o.values })),
    ...(withVariants ? { variants } : {}), ...(withDesc ? { description: textOf(p.body_html) } : {}),
    createdAt: p.created_at, updatedAt: p.updated_at, publishedAt: p.published_at, store: origin, scrapedAt: new Date().toISOString(),
  };
}

let keepGoing = true;
for (const raw of storeUrls) {
  if (!keepGoing) break;
  let ep; try { ep = endpointFor(raw); } catch { log.warning(`Bad URL: ${raw}`); continue; }
  let got = 0;
  try {
    if (ep.kind === 'product') {
      const p = JSON.parse((await http(ep.url)).body).product;
      if (p && (!onlyAvailable || (p.variants ?? []).some((v) => v.available))) { keepGoing = await pushResult(shape(p, ep.origin)); got++; }
    } else {
      for (let page = 1; got < perStore && keepGoing; page++) {
        const res = await http(`${ep.url}?limit=250&page=${page}`);
        const products = JSON.parse(res.body).products ?? [];
        if (!products.length) break;
        for (const p of products) {
          if (got >= perStore) break;
          if (onlyAvailable && !(p.variants ?? []).some((v) => v.available)) continue;
          keepGoing = await pushResult(shape(p, ep.origin)); got++;
          if (!keepGoing) break;
        }
        if (products.length < 250) break;
      }
    }
  } catch (e) {
    log.warning(`${raw}: ${e.message} (store may not be Shopify or has products.json disabled)`);
  }
  log.info(`${ep.origin}: ${got} products`);
}
log.info(`Done. Pushed ${pushed} products.`);
await Actor.exit();
