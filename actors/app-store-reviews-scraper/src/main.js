import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';

await Actor.init();
const input = (await Actor.getInput()) ?? {};
const apps = (input.apps ?? []).map(String);
const countries = (input.countries?.length ? input.countries : ['us']).map((c) => c.toLowerCase().trim());
const sort = input.sort === 'mostHelpful' ? 'mostHelpful' : 'mostRecent';
const perApp = Math.min(Number(input.maxReviewsPerApp ?? 200), 500);
const maxResults = Math.min(Number(input.maxResults ?? 2000), 50000);
const includeInfo = input.includeAppInfo !== false;
const countryFallback = input.countryFallback === true;
const minRating = input.minRating != null ? Number(input.minRating) : null;
const maxRating = input.maxRating != null ? Number(input.maxRating) : null;
const keyword = input.keyword ? String(input.keyword).toLowerCase() : null;
if (!apps.length) await Actor.fail('Provide at least one app URL or ID.');

function passesFilters(item) {
  if (minRating != null && item.rating < minRating) return false;
  if (maxRating != null && item.rating > maxRating) return false;
  if (keyword && !`${item.title || ''} ${item.content || ''}`.toLowerCase().includes(keyword)) return false;
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
const getJson = async (url, opts = {}) => JSON.parse((await gotScraping({ url, timeout: { request: 30000 }, retry: { limit: 2 }, ...opts })).body);

// Apple's review RSS has holes: for a given (app, country, sortBy) some page numbers return a
// well-formed but EMPTY feed while later pages return a full 50 (verified 2026-09-10 — Spotify/us
// mostHelpful yields 50,50,0,0,0,0,50,0,0,0 across pages 1-10, reproducibly). An empty page
// therefore does NOT mean "end of reviews", so we scan the whole 1..10 page range and skip holes.
// Header fingerprint makes no difference (same URL, same result under curl/Chrome/Safari UAs), so
// there is nothing to rotate — retries are for network errors only, handled by got-scraping.
const MAX_RSS_PAGE = 10; // Apple serves no page beyond 10
async function fetchEntries(url) {
  let entries = (await getJson(url)).feed?.entry ?? [];
  if (!Array.isArray(entries)) entries = [entries];
  return entries;
}
const lbl = (o) => (o && typeof o === 'object' && 'label' in o ? o.label : o ?? null);
const parseId = (s) => (s.match(/id(\d{6,})/)?.[1] || s.match(/^\d{6,}$/)?.[0] || null);

// Apple's RSS feed is populated per storefront: an app can have plenty of reviews in one
// country and an empty feed in another. Probe a few popular storefronts so an empty result
// tells the user where to look instead of just returning nothing. Diagnostics only, never charged.
const PROBE_COUNTRIES = ['us', 'gb', 'ca', 'au', 'de'];
let probesLeft = 5;
async function probeStorefronts(appId, skip) {
  if (probesLeft <= 0) return null;
  probesLeft -= 1;
  const found = [];
  for (const c of PROBE_COUNTRIES) {
    if (c === skip) continue;
    // Page 1 alone is not enough evidence — it is often one of Apple's empty holes — so sample a
    // couple of pages under both sorts and stop at the first hit.
    for (const [sortBy, page] of [['mostHelpful', 1], ['mostRecent', 1], ['mostHelpful', 2], ['mostRecent', 2]]) {
      try {
        const e = await fetchEntries(`https://itunes.apple.com/${c}/rss/customerreviews/id=${appId}/sortBy=${sortBy}/page=${page}/json`);
        if (e.length) { found.push(c); break; }
      } catch { /* probe is best-effort */ }
    }
  }
  return found;
}

async function getAppInfo(appId, country) {
  if (!includeInfo) return null;
  try {
    const a = (await getJson(`https://itunes.apple.com/lookup?id=${appId}&country=${country}`)).results?.[0];
    if (a) return { appName: a.trackName, developer: a.artistName, bundleId: a.bundleId, averageRating: a.averageUserRating ?? null, ratingCount: a.userRatingCount ?? null, currentVersion: a.version, primaryGenre: a.primaryGenreName, appUrl: a.trackViewUrl };
  } catch (e) { log.debug(`lookup failed: ${e.message}`); }
  return null;
}

// Scrapes one app in one storefront under one sort order. Returns how many reviews Apple actually
// served (before filters); `pushed` tracks how many were kept and charged. `seen` de-duplicates by
// review id, because scanning past empty pages (and the sort fallback below) can re-serve a review.
async function scrapeAppCountrySort(appId, country, sortBy, seen, extra = {}) {
  const info = await getAppInfo(appId, country);
  let got = 0;
  for (let page = 1; page <= MAX_RSS_PAGE && got < perApp && keepGoing; page++) {
    let entries = [];
    try {
      const url = `https://itunes.apple.com/${country}/rss/customerreviews/id=${appId}/sortBy=${sortBy}/page=${page}/json`;
      entries = await fetchEntries(url);
    } catch (e) { log.warning(`page ${page} failed for ${appId}/${country}: ${e.message}`); continue; }
    if (!entries.length) continue; // a hole in Apple's feed, not the end of it — keep paging
    for (const e of entries) {
      if (got >= perApp) break;
      const reviewId = lbl(e.id);
      if (reviewId != null && seen.has(reviewId)) continue;
      if (reviewId != null) seen.add(reviewId);
      const item = {
        reviewId, appId, country, title: lbl(e.title), content: lbl(e.content), rating: Number(lbl(e['im:rating'])) || null,
        version: lbl(e['im:version']), author: lbl(e.author?.name), authorUrl: lbl(e.author?.uri), updatedAt: lbl(e.updated),
        voteSum: Number(lbl(e['im:voteSum'])) || 0, voteCount: Number(lbl(e['im:voteCount'])) || 0, sortUsed: sortBy,
        ...(info || {}), ...extra, scrapedAt: new Date().toISOString(),
      };
      got += 1;
      if (!passesFilters(item)) continue;
      keepGoing = await pushResult(item);
      if (!keepGoing) break;
    }
  }
  return got;
}

// Apple's feed holes are per (app, country, sortBy): an app can be completely empty under
// "mostRecent" yet serve hundreds of reviews under "mostHelpful" (Spotify/us, 2026-09-10). Both
// sorts return the same review pool, so if the requested one comes back empty we fall back to the
// other rather than telling the user there are no reviews. Rows always carry `sortUsed`.
async function scrapeAppCountry(appId, country, extra = {}) {
  const seen = new Set();
  let got = await scrapeAppCountrySort(appId, country, sort, seen, extra);
  if (got === 0 && keepGoing) {
    const alt = sort === 'mostRecent' ? 'mostHelpful' : 'mostRecent';
    log.info(`${appId}/${country}: Apple's "${sort}" feed is empty; retrying under "${alt}".`);
    got = await scrapeAppCountrySort(appId, country, alt, seen, extra);
  }
  return got;
}

const emptyPairs = [];
const filteredOutPairs = [];
let keepGoing = true;
for (const app of apps) {
  if (!keepGoing) break;
  const appId = parseId(app);
  if (!appId) { log.warning(`Cannot parse app id from "${app}"`); continue; }
  for (const country of countries) {
    if (!keepGoing) break;
    const pushedBefore = pushed;
    const got = await scrapeAppCountry(appId, country);
    log.info(`${appId}/${country}: ${got} reviews fetched, ${pushed - pushedBefore} kept after filters`);
    if (got === 0) {
      const alt = await probeStorefronts(appId, country);
      if (countryFallback && alt?.length) {
        // Opt-in: pull the same app from a storefront that does have reviews. Rows carry the
        // storefront they really came from plus `requestedCountry`, so nothing is mislabelled.
        const fb = alt[0];
        log.info(`countryFallback: "${country}" is empty for ${appId}, retrieving reviews from "${fb}" instead.`);
        const fbGot = await scrapeAppCountry(appId, fb, { requestedCountry: country, fallbackUsed: true });
        log.info(`${appId}/${fb} (fallback): ${fbGot} reviews fetched, ${pushed - pushedBefore} kept after filters`);
        if (fbGot > 0) continue;
      }
      emptyPairs.push(`${appId}/${country}`);
      const hint = alt?.length
        ? ` Apple does return reviews for this app in: ${alt.join(', ')} — set "countries" to one of those${countryFallback ? '' : ', or enable "countryFallback"'}.`
        : '';
      log.warning(`Apple's review feed for app ${appId} in storefront "${country}" is empty (this is Apple's data, not a scrape failure).${hint}`);
    } else if (pushed === pushedBefore) {
      filteredOutPairs.push(`${appId}/${country}`);
      log.warning(`${appId}/${country}: fetched ${got} reviews but your minRating/maxRating/keyword filters removed all of them.`);
    }
  }
}
log.info(`Done. Pushed ${pushed} reviews.`);
if (pushed === 0) {
  const why = filteredOutPairs.length && !emptyPairs.length
    ? 'reviews were found but every one was removed by your minRating/maxRating/keyword filters'
    : `Apple's review feed returned nothing for: ${emptyPairs.join(', ')} (try another storefront in "countries")`;
  await Actor.setStatusMessage(`No reviews returned — ${why}. See the log for details.`);
} else if (emptyPairs.length) {
  await Actor.setStatusMessage(`Pushed ${pushed} reviews. Empty Apple feed for: ${emptyPairs.join(', ')}.`);
}
await Actor.exit();
