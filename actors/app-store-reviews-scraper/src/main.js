import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';

await Actor.init();
const input = (await Actor.getInput()) ?? {};
// The schema's "apps" field carries a default (Notion) so the Store's bare-{} auto-test has
// something real to run. Verified live on the platform 2026-09-11 that this default gets silently
// merged back in even when a caller sends {"appNames":[...]} and omits "apps" entirely — same class
// of trap as cycle 123/127/136/138's default-field-injection bugs. A caller who only wants
// name-resolved apps would otherwise get an uninvited, unpaid-for Notion review batch mixed in. Since
// we can't tell "user genuinely wants exactly the default app" from "field was silently defaulted",
// treat an unmodified default as unset whenever appNames is also present.
const DEFAULT_APPS = ['https://apps.apple.com/us/app/notion-notes-docs-tasks/id1232780281'];
let apps = (input.apps ?? []).map(String);
const appNames = (input.appNames ?? []).map(String).filter(Boolean);
if (appNames.length && apps.length === DEFAULT_APPS.length && apps.every((a, i) => a === DEFAULT_APPS[i])) {
  log.info('appNames given without an explicit "apps" list: ignoring the schema\'s default Notion app rather than mixing it in.');
  apps = [];
}
const countries = (input.countries?.length ? input.countries : ['us']).map((c) => c.toLowerCase().trim());
const requestedSort = input.sort === 'mostHelpful' ? 'mostHelpful' : 'mostRecent';
const perApp = Math.min(Number(input.maxReviewsPerApp ?? 200), 500);
const maxResults = Math.min(Number(input.maxResults ?? 2000), 50000);
const includeInfo = input.includeAppInfo !== false;
const countryFallback = input.countryFallback === true;
const minRating = input.minRating != null ? Number(input.minRating) : null;
const maxRating = input.maxRating != null ? Number(input.maxRating) : null;
const keyword = input.keyword ? String(input.keyword).toLowerCase() : null;
let reviewsAfterDate = null;
if (input.reviewsAfter) {
  reviewsAfterDate = new Date(input.reviewsAfter);
  if (Number.isNaN(reviewsAfterDate.getTime())) await Actor.fail(`"reviewsAfter" is not a valid date: "${input.reviewsAfter}". Use an ISO date like 2026-01-01.`);
}
// Chronological early-stop (below) only works on the date-sorted feed. mostHelpful has no date
// ordering, so a cutoff there is still applied as a plain filter but can't cut pagination short.
if (reviewsAfterDate && requestedSort === 'mostHelpful') log.warning('"reviewsAfter" forces sort to "mostRecent" (Apple\'s "mostHelpful" feed is not date-ordered, so a historical cutoff can\'t be applied to it efficiently).');
const sort = reviewsAfterDate ? 'mostRecent' : requestedSort;
if (!apps.length && !appNames.length) await Actor.fail('Provide at least one app URL/ID in "apps" or a name in "appNames".');

function passesFilters(item) {
  if (minRating != null && item.rating < minRating) return false;
  if (maxRating != null && item.rating > maxRating) return false;
  if (keyword && !`${item.title || ''} ${item.content || ''}`.toLowerCase().includes(keyword)) return false;
  if (reviewsAfterDate && item.updatedAt && new Date(item.updatedAt) < reviewsAfterDate) return false;
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
const MAX_RSS_PAGE = 10; // Apple serves no page beyond 10

// Whether a page is a hole depends on the CLIENT CLASS of the request, and the split is
// curl-vs-real-browser, not Apple-device-vs-not (measured 2026-09-10, interleaved, 4/4 rounds:
// Notion/us mostRecent page 4 returned 0 to `curl/8.5.0` every single time while an iPhone Safari
// UA, a macOS Chrome UA and got-scraping's own generated headers all returned a full 50 — same 50
// reviews, so it is one index, not two). Our default requests already use got-scraping's generated
// browser headers, i.e. the good side of the split. But holes still hit browser-class requests
// sometimes (Spotify/gb page 4, same session), and a hole is 50 lost reviews, so when a page comes
// back empty we re-request it under the OTHER client class before accepting it as a real hole.
// That costs extra requests only on holes, unlike sweeping every page twice.
const CLIENT_CLASSES = {
  default: undefined, // let got-scraping generate its normal desktop-browser header set
  ios: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1',
};
async function fetchEntries(url, clientClass = 'default') {
  const ua = CLIENT_CLASSES[clientClass];
  // useHeaderGenerator:false so got-scraping's generated desktop UA cannot override ours — the
  // whole point of this call is which class of UA Apple sees.
  const opts = ua ? { headers: { 'user-agent': ua, accept: '*/*' }, useHeaderGenerator: false } : {};
  let entries = (await getJson(url, opts)).feed?.entry ?? [];
  if (!Array.isArray(entries)) entries = [entries];
  return entries;
}
const lbl = (o) => (o && typeof o === 'object' && 'label' in o ? o.label : o ?? null);
const parseId = (s) => (s.match(/id(\d{6,})/)?.[1] || s.match(/^\d{6,}$/)?.[0] || null);

// Apple's search API is a real trap for "resolve this name" features: it almost NEVER returns zero
// results, even for pure gibberish — verified live 2026-09-11 with random keyboard-mash strings and
// emoji, every one came back with 1-3 completely unrelated apps (e.g. "xqzzptmwvbnjklasdfgh..." ->
// an Arabic math-quiz game). A naive "take the first hit" implementation would silently resolve a
// typo'd app name to a random unrelated app instead of failing loudly. So a match is only accepted
// if at least one significant word (>=3 chars) of the query appears in the candidate's name, bundle
// id or developer name; otherwise this is treated as NO MATCH FOUND, not a guess.
const searchCountry = countries[0] || 'us';
async function resolveAppName(name) {
  let data;
  try {
    data = await getJson(`https://itunes.apple.com/search?entity=software&country=${searchCountry}&limit=5&term=${encodeURIComponent(name)}`);
  } catch (e) { log.warning(`appNames: search for "${name}" failed: ${e.message}`); return null; }
  const results = data.results || [];
  const qTokens = name.toLowerCase().replace(/[^a-z0-9\s]/g, ' ').split(/\s+/).filter((t) => t.length >= 3);
  const norm = (s) => String(s || '').toLowerCase();
  const isRelevant = (r) => {
    const hay = `${norm(r.trackName)} ${norm(r.bundleId)} ${norm(r.artistName)}`;
    return qTokens.length ? qTokens.some((t) => hay.includes(t)) : hay.includes(norm(name));
  };
  const match = results.find(isRelevant);
  if (!match) {
    const top = results[0]?.trackName ? ` (Apple's closest hit was the unrelated "${results[0].trackName}")` : '';
    log.warning(`appNames: NO real match found for "${name}"${top} — searched the "${searchCountry}" storefront. Apple's search API returns some app for almost any input, so an unrelated top hit is treated as no match rather than guessed. Use a numeric app id or App Store URL instead.`);
    return null;
  }
  log.info(`appNames: resolved "${name}" -> "${match.trackName}" (id ${match.trackId}) in the "${searchCountry}" storefront.`);
  return String(match.trackId);
}

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
    // few pages spread across both sorts AND both client classes, and stop at the first hit.
    for (const [sortBy, page, cls] of [['mostHelpful', 1, 'default'], ['mostRecent', 1, 'ios'], ['mostHelpful', 2, 'ios'], ['mostRecent', 2, 'default']]) {
      try {
        const e = await fetchEntries(`https://itunes.apple.com/${c}/rss/customerreviews/id=${appId}/sortBy=${sortBy}/page=${page}/json`, cls);
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

// Fetches one page, retrying an empty result under the other client class (see CLIENT_CLASSES).
// Returns the entries plus the class that actually served them, so rows are never mislabelled.
async function fetchPage(url, primary = 'default') {
  for (const clientClass of [primary, primary === 'default' ? 'ios' : 'default']) {
    let entries;
    try {
      entries = await fetchEntries(url, clientClass);
    } catch (e) { log.warning(`${url} failed (${clientClass}): ${e.message}`); continue; }
    if (entries.length) return { entries, clientClass };
  }
  return { entries: [], clientClass: primary };
}

// Scrapes one app in one storefront under one sort order. Returns how many NEW reviews Apple
// served (before filters); `pushed` tracks how many were kept and charged. `seen` de-duplicates by
// review id across pages and sorts — scanning past empty pages, the sort fallback and the
// client-class retry can all re-serve the same review.
async function scrapeAppCountrySort(appId, country, sortBy, seen, info, tally, extra = {}) {
  let got = 0;
  let hitCutoff = false;
  // Only "mostRecent" is date-ordered (verified live 2026-09-11: strictly descending across pages,
  // no reset at page boundaries) — so pagination can only be safely cut short under that sort.
  const canEarlyStop = reviewsAfterDate && sortBy === 'mostRecent';
  for (let page = 1; page <= MAX_RSS_PAGE && tally.got < perApp && keepGoing && !hitCutoff; page++) {
    const url = `https://itunes.apple.com/${country}/rss/customerreviews/id=${appId}/sortBy=${sortBy}/page=${page}/json`;
    const { entries, clientClass } = await fetchPage(url);
    if (!entries.length) continue; // a real hole in Apple's feed, not the end of it — keep paging
    if (clientClass !== 'default') log.info(`${appId}/${country} ${sortBy} page ${page}: empty for the default client, recovered ${entries.length} reviews under the iOS client.`);
    for (const e of entries) {
      if (tally.got >= perApp) break;
      const reviewId = lbl(e.id);
      if (reviewId != null && seen.has(reviewId)) continue;
      if (reviewId != null) seen.add(reviewId);
      const item = {
        reviewId, appId, country, title: lbl(e.title), content: lbl(e.content), rating: Number(lbl(e['im:rating'])) || null,
        version: lbl(e['im:version']), author: lbl(e.author?.name), authorUrl: lbl(e.author?.uri), updatedAt: lbl(e.updated),
        voteSum: Number(lbl(e['im:voteSum'])) || 0, voteCount: Number(lbl(e['im:voteCount'])) || 0, sortUsed: sortBy,
        clientClass, ...(info || {}), ...extra, scrapedAt: new Date().toISOString(),
      };
      if (canEarlyStop && item.updatedAt && new Date(item.updatedAt) < reviewsAfterDate) {
        hitCutoff = true;
        log.info(`${appId}/${country}: reached a review older than "reviewsAfter" (${item.updatedAt}) — stopping pagination early instead of scanning the rest of the (chronologically-sorted) feed.`);
        break;
      }
      got += 1; tally.got += 1;
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
  const tally = { got: 0 };
  const info = await getAppInfo(appId, country);
  await scrapeAppCountrySort(appId, country, sort, seen, info, tally, extra);
  if (tally.got === 0 && keepGoing) {
    const alt = sort === 'mostRecent' ? 'mostHelpful' : 'mostRecent';
    log.info(`${appId}/${country}: Apple's "${sort}" feed is empty; retrying under "${alt}".`);
    await scrapeAppCountrySort(appId, country, alt, seen, info, tally, extra);
  }
  return tally.got;
}

if (appNames.length) {
  const resolved = (await Promise.all(appNames.map(resolveAppName))).filter(Boolean);
  apps.push(...resolved);
}
if (!apps.length) await Actor.fail('None of the given "apps"/"appNames" resolved to a usable app id — see the warnings above.');

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
