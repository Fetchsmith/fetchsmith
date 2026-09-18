import { createHash } from 'node:crypto';
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
let apps = (input.apps ?? []).map((a) => String(a).trim());
const appNames = (input.appNames ?? []).map((a) => String(a).trim()).filter(Boolean);
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
const includeMacApps = input.includeMacApps === true;
const minRating = input.minRating != null ? Number(input.minRating) : null;
const maxRating = input.maxRating != null ? Number(input.maxRating) : null;
if (minRating != null && maxRating != null && minRating > maxRating) {
  throw new Error(`"minRating" (${minRating}) is greater than "maxRating" (${maxRating}) — no review can ever match. Swap them.`);
}
const keyword = String(input.keyword ?? '').normalize('NFC').trim().toLowerCase() || null;
const minReviewLength = input.minReviewLength != null ? Number(input.minReviewLength) : null;
// Apple only populates im:voteSum/im:voteCount on the "mostHelpful" feed; every review served by
// "mostRecent" carries a flat 0 (verified live 2026-09-18 across 4 apps, both sorts). That is real
// data, not a hole -- recent reviews genuinely have no votes yet -- but a helpfulness floor on the
// mostRecent feed would drop every row, so it is warned about below rather than silently applied.
const minVoteSum = input.minVoteSum != null ? Number(input.minVoteSum) : null;
const minVoteCount = input.minVoteCount != null ? Number(input.minVoteCount) : null;
let reviewsAfterDate = null;
if (input.reviewsAfter) {
  reviewsAfterDate = new Date(input.reviewsAfter);
  if (Number.isNaN(reviewsAfterDate.getTime())) await Actor.fail(`"reviewsAfter" is not a valid date: "${input.reviewsAfter}". Use an ISO date like 2026-01-01.`);
}
let reviewsBeforeDate = null;
if (input.reviewsBefore) {
  reviewsBeforeDate = new Date(input.reviewsBefore);
  if (Number.isNaN(reviewsBeforeDate.getTime())) await Actor.fail(`"reviewsBefore" is not a valid date: "${input.reviewsBefore}". Use an ISO date like 2026-06-01.`);
  // A bare date parses as midnight UTC, which would exclude the whole named day; make the bound
  // inclusive of it, matching how buyers read "reviews before 2026-06-01 .. up to that date".
  if (/^\d{4}-\d{2}-\d{2}$/.test(String(input.reviewsBefore).trim())) reviewsBeforeDate = new Date(reviewsBeforeDate.getTime() + 24 * 60 * 60 * 1000 - 1);
}
if (reviewsAfterDate && reviewsBeforeDate && reviewsAfterDate > reviewsBeforeDate) {
  throw new Error(`"reviewsAfter" (${input.reviewsAfter}) is later than "reviewsBefore" (${input.reviewsBefore}) — no review can ever match. Swap them.`);
}
const watchLabel = String(input.watchLabel ?? '').trim();
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
// Chronological early-stop (below) only works on the date-sorted feed. mostHelpful has no date
// ordering, so a cutoff there is still applied as a plain filter but can't cut pagination short.
if (reviewsAfterDate && requestedSort === 'mostHelpful') log.warning('"reviewsAfter" forces sort to "mostRecent" (Apple\'s "mostHelpful" feed is not date-ordered, so a historical cutoff can\'t be applied to it efficiently).');
const sort = reviewsAfterDate ? 'mostRecent' : requestedSort;
if ((minVoteSum != null || minVoteCount != null) && sort === 'mostRecent') {
  log.warning('"minVoteSum"/"minVoteCount" filter on Apple\'s helpfulness votes, which are only populated on the "mostHelpful" feed — under sort "mostRecent" every review comes back with 0 votes, so a floor above 0 will keep nothing. Set sort to "mostHelpful" (and drop "reviewsAfter", which forces mostRecent) to use them.');
}
if (!apps.length && !appNames.length) await Actor.fail('Provide at least one app URL/ID in "apps" or a name in "appNames".');

function passesFilters(item) {
  if (minRating != null && item.rating < minRating) return false;
  if (maxRating != null && item.rating > maxRating) return false;
  if (keyword && !`${item.title || ''} ${item.content || ''}`.normalize('NFC').toLowerCase().includes(keyword)) return false;
  if (reviewsAfterDate && item.updatedAt && new Date(item.updatedAt) < reviewsAfterDate) return false;
  if (reviewsBeforeDate && item.updatedAt && new Date(item.updatedAt) > reviewsBeforeDate) return false;
  // Body text only: the title is a separate field and padding one short line with a long headline
  // is not the "substantial review" buyers are filtering for.
  if (minReviewLength != null && (item.content || '').trim().length < minReviewLength) return false;
  if (minVoteSum != null && item.voteSum < minVoteSum) return false;
  if (minVoteCount != null && item.voteCount < minVoteCount) return false;
  return true;
}

// Watch mode: a stateful "only reviews posted since my last run" filter. Unlike the other
// watchLabel ports, this Actor already merges app metadata into every review row (see `info`
// spread below) rather than pushing a separate app-snapshot record, so there is no deferred-
// snapshot problem here — every pushed row is a genuine review with a stable id.
const WATCH_STORE = 'fetchsmith-app-store-reviews-watch';
const SEED_CAP = 20000; // bound the cost/time of a baseline run across all (app,country) pairs
const WATCH_KEEP = 40000; // bound the record size; oldest ids fall off first
const WATCH_SCAN_CAP = 500; // Apple's own hard ceiling (10 pages x 50) — always safe to use for seeding

function watchKeyFor(label, criteria) {
  const safe = label.toLowerCase().replace(/[^a-z0-9_.-]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 40) || 'default';
  const fp = createHash('sha1').update(JSON.stringify(criteria, Object.keys(criteria).sort())).digest('hex').slice(0, 10);
  return { key: `watch-${safe}-${fp}`, fingerprint: fp };
}

const watchMode = watchLabel.length > 0;
let watchStore = null;
let watchKey = null;
let watchRecord = null;
let seeding = false;
let watchSkipped = 0;
let unidentifiedSkipped = 0; // watch mode only: reviews Apple returned without a usable id
const watchSeen = new Set(); // `${appId}:${actualCountry}:${reviewId}` already delivered under this label+fingerprint
const seededPairs = new Set(); // `${appId}::${requestedCountry}` pairs already baselined

if (watchMode) {
  // EVERY filter that decides what gets delivered goes into the fingerprint, including the
  // client-side ones (rating/keyword/length/votes/date) — Apple's RSS feed takes no such params
  // server-side, so passesFilters() is the only filter layer, same rule as every other
  // client-side-filtered port. Raw "apps"/"appNames"/"sort" are fingerprinted (not the resolved
  // app ids or the reviewsAfter-forced sort) since those are exactly what the buyer typed and
  // neither has a rolling default.
  const criteria = {
    apps: input.apps ?? [], appNames: input.appNames ?? [], countries, countryFallback,
    sort: input.sort ?? null, minRating, maxRating, keyword, reviewsAfter: input.reviewsAfter ?? null,
    // Added only when set, for the same reason includeMacApps is: spelling these out as nulls on
    // the default path would change the fingerprint of every watch that already exists.
    ...(input.reviewsBefore ? { reviewsBefore: input.reviewsBefore } : {}),
    ...(minReviewLength != null ? { minReviewLength } : {}),
    ...(minVoteSum != null ? { minVoteSum } : {}),
    ...(minVoteCount != null ? { minVoteCount } : {}),
    // Added only when ON, never as `false`: it changes which app a name resolves to, so it must
    // separate baselines — but spelling it out on the default path would change the fingerprint of
    // every watch that already exists and reset all of them once for no reason.
    ...(includeMacApps ? { includeMacApps: true } : {}),
  };
  watchStore = await Actor.openKeyValueStore(WATCH_STORE);
  const { key, fingerprint } = watchKeyFor(watchLabel, criteria);
  watchKey = key;
  const existing = await watchStore.getValue(key);
  if (existing && Array.isArray(existing.seenIds)) {
    watchRecord = existing;
    for (const id of existing.seenIds) watchSeen.add(String(id));
    for (const p of existing.seededPairs ?? []) seededPairs.add(String(p));
    log.info(
      `Watch mode "${watchLabel}" (${key}): baseline from ${existing.lastRunAt ?? 'an earlier run'} holds `
      + `${watchSeen.size} already-delivered review(s) across ${seededPairs.size} app/country pair(s). Only `
      + 'reviews NOT in that baseline will be returned and charged.',
    );
  } else {
    watchRecord = { fingerprint, firstSeededAt: new Date().toISOString(), runCount: 0 };
    seeding = true;
    log.info(
      `Watch mode "${watchLabel}" (${key}): FIRST run for this label and filter set, so this is a baseline run. `
      + 'It records which reviews already exist and returns ZERO rows (you are charged nothing). Run it again on '
      + 'the same label and filters -- on a schedule, typically -- to get only the reviews posted since now.',
    );
  }
  if (sort === 'mostHelpful') {
    log.warning(
      `Watch mode with sort="mostHelpful": that feed is not date-ordered, so a brand-new review is not `
      + `necessarily inside the first ${perApp} rows scanned. Use sort="mostRecent" for reliable alerting.`,
    );
  }
}

async function saveWatchRecord(status) {
  const ids = Array.from(watchSeen).slice(-WATCH_KEEP);
  await watchStore.setValue(watchKey, {
    ...watchRecord,
    label: watchLabel,
    lastRunAt: new Date().toISOString(),
    lastRunStatus: status,
    runCount: (watchRecord.runCount ?? 0) + 1,
    seenCount: ids.length,
    seededPairs: Array.from(seededPairs),
    seenIds: ids,
  });
}

let pushed = 0;
const isPPE = Actor.getChargingManager().getPricingInfo().isPayPerEvent;
async function pushResult(item, watchId = null, pairSeeding = false) {
  if (watchMode && watchId != null && pairSeeding) {
    watchSeen.add(watchId);
    if (watchSeen.size >= SEED_CAP) keepGoing = false;
    return keepGoing;
  }
  if (watchMode && watchId != null && watchSeen.has(watchId)) {
    watchSkipped += 1;
    return true; // already delivered under this label: not pushed, not charged, keep scanning
  }
  if (isPPE) {
    const r = await Actor.charge({ eventName: 'result', count: 1 });
    if (r.chargedCount === 0) return false; // user's budget exhausted: never push unpaid items
    await Actor.pushData(item); pushed += 1;
    if (watchMode && watchId != null) watchSeen.add(watchId);
    return !r.eventChargeLimitReached && pushed < maxResults;
  }
  await Actor.pushData(item); pushed += 1; // non-PPE run (e.g. developer test): no charging
  if (watchMode && watchId != null) watchSeen.add(watchId);
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
// Mac App Store apps are NOT in `entity=software` — that entity is iOS-only. Verified live
// 2026-09-17: searching "final cut pro" under `entity=software` returns Final Cut Camera/iMovie/
// CapCut and never the Mac app, while `entity=macSoftware` returns it as id 424389933 with
// `kind: "mac-software"`. Everything downstream already works for Mac apps unchanged (the review
// RSS feed and the lookup API are both id-based, not platform-scoped — the same id returns a full
// 50-entry feed), so `includeMacApps` only has to widen NAME RESOLUTION, nothing else.
async function searchEntity(entity, name) {
  try {
    const data = await getJson(`https://itunes.apple.com/search?entity=${entity}&country=${searchCountry}&limit=5&term=${encodeURIComponent(name)}`);
    return data.results || [];
  } catch (e) { log.warning(`appNames: ${entity} search for "${name}" failed: ${e.message}`); return null; }
}
async function resolveAppName(name) {
  const iosResults = await searchEntity('software', name);
  // A failed iOS search is only fatal when it is the only search we were going to run.
  if (iosResults === null && !includeMacApps) return null;
  const results = [...(iosResults || [])];
  if (includeMacApps) results.push(...((await searchEntity('macSoftware', name)) || []));
  if (!results.length) return null;
  const qTokens = name.toLowerCase().replace(/[^a-z0-9\s]/g, ' ').split(/\s+/).filter((t) => t.length >= 3);
  const norm = (s) => String(s || '').toLowerCase();
  const isRelevant = (r) => {
    const hay = `${norm(r.trackName)} ${norm(r.bundleId)} ${norm(r.artistName)}`;
    return qTokens.length ? qTokens.some((t) => hay.includes(t)) : hay.includes(norm(name));
  };
  // Exact title match wins over the loose token rule. Without this, "final cut pro" with
  // includeMacApps on would still resolve to the iOS "Final Cut Camera" (it shares the token
  // "final" and comes first), which is exactly the app the caller did not ask for.
  const match = results.find((r) => norm(r.trackName) === norm(name)) || results.find(isRelevant);
  if (!match) {
    const top = results[0]?.trackName ? ` (Apple's closest hit was the unrelated "${results[0].trackName}")` : '';
    const where = includeMacApps ? 'iOS and Mac App Store' : 'iOS App Store';
    log.warning(`appNames: NO real match found for "${name}"${top} — searched the ${where} in the "${searchCountry}" storefront. Apple's search API returns some app for almost any input, so an unrelated top hit is treated as no match rather than guessed.${includeMacApps ? '' : ' If this is a Mac-only app, set "includeMacApps": true.'} Use a numeric app id or App Store URL instead.`);
    return null;
  }
  const platform = match.kind === 'mac-software' ? 'Mac App Store' : `"${searchCountry}" storefront`;
  log.info(`appNames: resolved "${name}" -> "${match.trackName}" (id ${match.trackId}) in the ${platform}.`);
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

// The per-star ratings histogram ("how many 1-star vs 5-star ratings") is NOT in the iTunes lookup
// API (that only carries the average and the total) and not in the review RSS feed either. It IS
// embedded in the public App Store web page, inside the <script id="serialized-server-data"> JSON
// that Apple server-renders for every listing, as a node with "$kind": "Ratings".
// Verified live 2026-09-14 on 5 apps across the us/gb/de storefronts (Instagram, Threads, Spotify,
// YouTube, WhatsApp): "ratingCounts" is always a 5-element array ordered 5* -> 1*, always sums
// exactly to "totalNumberOfRatings", and its descending-weighted mean reproduces Apple's own
// "ratingAverage" to within rounding. Counts arrive as floats (2000234.9999999998), hence Math.round.
// This is app-level, not review-level: one fetch per (app, country), only when includeAppInfo is on.
async function getRatingBreakdown(appId, country) {
  try {
    const html = (await gotScraping({ url: `https://apps.apple.com/${country}/app/id${appId}`, timeout: { request: 30000 }, retry: { limit: 1 } })).body;
    const m = html.match(/<script type="application\/json" id="serialized-server-data">(.*?)<\/script>/s);
    if (!m) return null;
    let node = null;
    (function walk(o) {
      if (node || !o || typeof o !== 'object') return;
      if (!Array.isArray(o) && o.$kind === 'Ratings' && Array.isArray(o.ratingCounts)) { node = o; return; }
      for (const v of Array.isArray(o) ? o : Object.values(o)) walk(v);
    })(JSON.parse(m[1]));
    if (!node || node.ratingCounts.length !== 5) return null;
    const c = node.ratingCounts.map((n) => Math.round(Number(n) || 0));
    const total = c.reduce((a, b) => a + b, 0);
    if (!total) return null;
    // Guard the 5*->1* ordering assumption instead of trusting it silently: if Apple ever flips the
    // array, the weighted mean stops matching their own average and we say so rather than shipping
    // a breakdown that is exactly backwards.
    const mean = c.reduce((a, n, i) => a + n * (5 - i), 0) / total;
    if (node.ratingAverage != null && Math.abs(mean - Number(node.ratingAverage)) > 0.15) {
      log.warning(`${appId}/${country}: ratings histogram failed its sanity check (computed ${mean.toFixed(2)} vs Apple's ${node.ratingAverage}) — omitting ratingBreakdown for this app rather than reporting a possibly mis-ordered one.`);
      return null;
    }
    return { totalRatings: total, ratingBreakdown: { five: c[0], four: c[1], three: c[2], two: c[3], one: c[4] } };
  } catch (e) { log.debug(`ratings histogram failed for ${appId}/${country}: ${e.message}`); return null; }
}

async function getAppInfo(appId, country) {
  if (!includeInfo) return null;
  // Both requests are app-level metadata for the same (app, country); run them together so the
  // histogram costs no extra wall-clock on top of the lookup we already do.
  const [lookup, breakdown] = await Promise.allSettled([
    getJson(`https://itunes.apple.com/lookup?id=${appId}&country=${country}`),
    getRatingBreakdown(appId, country),
  ]);
  const extra = breakdown.status === 'fulfilled' && breakdown.value ? breakdown.value : { totalRatings: null, ratingBreakdown: null };
  if (lookup.status !== 'fulfilled') {
    log.debug(`lookup failed: ${lookup.reason?.message}`);
    return extra.ratingBreakdown ? extra : null;
  }
  const a = lookup.value.results?.[0];
  if (!a) return extra.ratingBreakdown ? extra : null;
  return {
    appName: a.trackName, developer: a.artistName, bundleId: a.bundleId, averageRating: a.averageUserRating ?? null,
    ratingCount: a.userRatingCount ?? null, currentVersion: a.version, primaryGenre: a.primaryGenreName, appUrl: a.trackViewUrl,
    ...extra,
  };
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

// An empty feed for one app/storefront is normal Apple behaviour (see the hole comments above),
// but the whole customer-review RSS can also go dark for the CALLER: measured 2026-09-16, every
// request to itunes.apple.com/<cc>/rss/customerreviews/... returned HTTP 200 with
// `feed.entry: null` for every app id, storefront (us/gb/de/jp), page, sort, URL shape and client
// class — yet the SAME three app ids fetched from Apify's network in the same minute returned full
// feeds. So this is Apple emptying the feed per source network (rate-limit/blocklist shaped), not
// a global Apple outage, and either way it is invisible in a single app's response: it looks
// exactly like "this app has no reviews". When a run ends up with nothing at all we therefore
// probe control apps that always carry hundreds of thousands of reviews; if THEY are empty too,
// nothing that reaches this run can produce reviews, so the run is FAILED by name instead of being
// reported to the buyer as "no reviews match your filters" / "nothing new since the last run".
// Same shape as the steam-reviews-scraper upstream-fault check.
const CONTROL_APPS = [
  ['389801252', 'us'], // Instagram
  ['324684580', 'us'], // Spotify
];
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let feedDown = null; // cached: at most one probe sweep per run
async function reviewFeedIsDown() {
  if (feedDown !== null) return feedDown;
  // Spaced retries so a momentary blip is never announced as an outage (fetchPage itself already
  // retries each request under the other client class).
  for (let attempt = 1; attempt <= 3; attempt += 1) {
    for (const [id, cc] of CONTROL_APPS) {
      for (const sortBy of ['mostRecent', 'mostHelpful']) {
        const { entries } = await fetchPage(`https://itunes.apple.com/${cc}/rss/customerreviews/id=${id}/sortBy=${sortBy}/page=1/json`);
        if (entries.length) { feedDown = false; return false; }
      }
    }
    log.warning(`Apple's review feed returned nothing for the control apps (attempt ${attempt}/3) — retrying before calling it an upstream outage.`);
    if (attempt < 3) await sleep(5000);
  }
  feedDown = true;
  return true;
}

// Scrapes one app in one storefront under one sort order. Returns how many NEW reviews Apple
// served (before filters); `pushed` tracks how many were kept and charged. `seen` de-duplicates by
// review id across pages and sorts — scanning past empty pages, the sort fallback and the
// client-class retry can all re-serve the same review.
async function scrapeAppCountrySort(appId, country, sortBy, seen, info, tally, extra = {}, pairSeeding = false) {
  let got = 0;
  let hitCutoff = false;
  // Only "mostRecent" is date-ordered (verified live 2026-09-11: strictly descending across pages,
  // no reset at page boundaries) — so pagination can only be safely cut short under that sort.
  const canEarlyStop = reviewsAfterDate && sortBy === 'mostRecent';
  // maxReviewsPerApp is an honest scan-depth cap on incremental runs (with sort=mostRecent new
  // reviews sort at the head, so the buyer's own cap does not hide them there — same precedent as
  // us-federal-awards' maxPagesPerCategory). A BASELINE walk must see at least as deep as any later
  // run can reach, or older reviews return as "new" later — Apple's own hard ceiling is only 500
  // reviews (10 pages x 50), so seeding simply always uses that ceiling, never less.
  const scanCap = pairSeeding ? WATCH_SCAN_CAP : perApp;
  for (let page = 1; page <= MAX_RSS_PAGE && tally.got < scanCap && keepGoing && !hitCutoff; page++) {
    const url = `https://itunes.apple.com/${country}/rss/customerreviews/id=${appId}/sortBy=${sortBy}/page=${page}/json`;
    const { entries, clientClass } = await fetchPage(url);
    if (!entries.length) continue; // a real hole in Apple's feed, not the end of it — keep paging
    if (clientClass !== 'default') log.info(`${appId}/${country} ${sortBy} page ${page}: empty for the default client, recovered ${entries.length} reviews under the iOS client.`);
    for (const e of entries) {
      if (tally.got >= scanCap) break;
      const reviewId = lbl(e.id);
      if (reviewId != null && seen.has(reviewId)) continue;
      if (reviewId != null) seen.add(reviewId);
      if (watchMode && reviewId == null) {
        // No stable id means it can be neither recorded in the baseline nor recognised next run,
        // so delivering it would re-charge for the same row on every scheduled watch run.
        unidentifiedSkipped += 1;
        continue;
      }
      const item = {
        reviewId, appId, country, title: lbl(e.title), content: lbl(e.content), rating: Number(lbl(e['im:rating'])) || null,
        version: lbl(e['im:version']), author: lbl(e.author?.name), authorUrl: lbl(e.author?.uri), updatedAt: lbl(e.updated),
        // Apple's own "related" link for the review. It is app+storefront scoped, not per-review
        // (every entry in a feed carries the same href) — kept verbatim rather than synthesised.
        reviewUrl: (Array.isArray(e.link) ? e.link[0] : e.link)?.attributes?.href ?? null,
        voteSum: Number(lbl(e['im:voteSum'])) || 0, voteCount: Number(lbl(e['im:voteCount'])) || 0, sortUsed: sortBy,
        clientClass, ...(info || {}), ...extra, scrapedAt: new Date().toISOString(),
      };
      if (canEarlyStop && item.updatedAt && new Date(item.updatedAt) < reviewsAfterDate) {
        hitCutoff = true;
        log.info(`${appId}/${country}: reached a review older than "reviewsAfter" (${item.updatedAt}) — stopping pagination early instead of scanning the rest of the (chronologically-sorted) feed.`);
        break;
      }
      got += 1; tally.got += 1;
      if (!passesFilters(item)) { tally.filteredOut += 1; continue; }
      const watchId = watchMode ? `${appId}:${country}:${reviewId}` : null;
      // Counts every matching review considered "new" this scan (not already in the baseline) --
      // used only to detect a saturated scan window (see the saturatedPairs check below), separate
      // from pushResult's own watchSkipped bookkeeping.
      if (!(watchMode && !pairSeeding && watchId != null && watchSeen.has(watchId))) tally.newForPair = (tally.newForPair || 0) + 1;
      keepGoing = await pushResult(item, watchId, pairSeeding);
      if (!keepGoing) break;
    }
  }
  return got;
}

// Apple's feed holes are per (app, country, sortBy): an app can be completely empty under
// "mostRecent" yet serve hundreds of reviews under "mostHelpful" (Spotify/us, 2026-09-10). Both
// sorts return the same review pool, so if the requested one comes back empty we fall back to the
// other rather than telling the user there are no reviews. Rows always carry `sortUsed`.
async function scrapeAppCountry(appId, country, extra = {}, pairSeeding = false) {
  const seen = new Set();
  const tally = { got: 0, filteredOut: 0 };
  const info = await getAppInfo(appId, country);
  await scrapeAppCountrySort(appId, country, sort, seen, info, tally, extra, pairSeeding);
  if (tally.got === 0 && keepGoing) {
    const alt = sort === 'mostRecent' ? 'mostHelpful' : 'mostRecent';
    log.info(`${appId}/${country}: Apple's "${sort}" feed is empty; retrying under "${alt}".`);
    await scrapeAppCountrySort(appId, country, alt, seen, info, tally, extra, pairSeeding);
  }
  // maxReviewsPerApp (perApp) caps reviews SCANNED, before review filtering (rating/keyword/length/votes/date)
  // -- if the cap was hit and some scanned reviews were dropped by a filter, matching reviews may
  // still sit deeper in Apple's feed and were never looked at.
  const scanCap = pairSeeding ? WATCH_SCAN_CAP : perApp;
  return {
    got: tally.got, filteredOut: tally.filteredOut, capReached: tally.got >= scanCap,
    newForPair: tally.newForPair || 0,
  };
}

if (appNames.length) {
  const resolved = (await Promise.all(appNames.map(resolveAppName))).filter(Boolean);
  apps.push(...resolved);
}
if (!apps.length) await Actor.fail('None of the given "apps"/"appNames" resolved to a usable app id — see the warnings above.');

const emptyPairs = [];
const filteredOutPairs = [];
// Pairs where maxReviewsPerApp was hit while the review filters still discarded scanned
// reviews -- reviews deeper in Apple's feed were never scanned.
const depthCappedPairs = [];
// Watch mode: every matching review inside the scanned window was new, so older new reviews
// (posted since the last run but sorting past the window) may have been missed.
const saturatedPairs = [];
// Reviews Apple served this run across every pair, BEFORE filters and before watch-mode
// de-duplication -- i.e. how much data the upstream feed produced at all. Zero here (with pairs
// actually attempted) is what triggers the upstream-outage probe below.
let feedServed = 0;
let pairsAttempted = 0;
let keepGoing = true;
for (const app of apps) {
  if (!keepGoing) break;
  const appId = parseId(app);
  if (!appId) { log.warning(`Cannot parse app id from "${app}"`); continue; }
  for (const country of countries) {
    if (!keepGoing) break;
    const pairKey = `${appId}::${country}`;
    // A pair not yet in the baseline is seeded in place instead of delivered, even on an otherwise
    // incremental run. This only happens when "appNames" resolves to a different app id than last
    // time (editing "apps"/"countries" directly changes the fingerprint, starting a fresh baseline
    // for everything) -- without this, the newly-appearing pair would dump its whole review history
    // as "new" and charge for all of it. Same drift guard as the google-play-reviews-scraper port.
    const pairSeeding = watchMode && (seeding || !seededPairs.has(pairKey));
    if (watchMode && !seeding && pairSeeding) {
      log.info(`${pairKey}: not in the baseline for "${watchLabel}" yet (appNames resolved to a new app) — baselining it this run instead of delivering its existing reviews.`);
    }
    const pushedBefore = pushed;
    pairsAttempted += 1;
    const { got, filteredOut, capReached, newForPair } = await scrapeAppCountry(appId, country, {}, pairSeeding);
    log.info(`${appId}/${country}: ${got} reviews fetched, ${pushed - pushedBefore} kept after filters`);
    if (capReached && filteredOut > 0) {
      depthCappedPairs.push(`${appId}/${country}`);
      log.warning(
        `${appId}/${country}: scanned the maxReviewsPerApp limit of ${perApp} review(s) and ${filteredOut} of them `
        + `were excluded by the review filters (rating/keyword/length/votes/date). The cap counts reviews scanned, before `
        + `filtering — raise maxReviewsPerApp to search deeper.`,
      );
    }
    let totalNewForPair = newForPair;
    let totalGot = got;
    if (got === 0) {
      const alt = await probeStorefronts(appId, country);
      if (countryFallback && alt?.length) {
        // Opt-in: pull the same app from a storefront that does have reviews. Rows carry the
        // storefront they really came from plus `requestedCountry`, so nothing is mislabelled.
        const fb = alt[0];
        log.info(`countryFallback: "${country}" is empty for ${appId}, retrieving reviews from "${fb}" instead.`);
        const fb2 = await scrapeAppCountry(appId, fb, { requestedCountry: country, fallbackUsed: true }, pairSeeding);
        totalNewForPair += fb2.newForPair;
        totalGot += fb2.got;
        log.info(`${appId}/${fb} (fallback): ${fb2.got} reviews fetched, ${pushed - pushedBefore} kept after filters`);
        if (fb2.capReached && fb2.filteredOut > 0) {
          depthCappedPairs.push(`${appId}/${fb}`);
          log.warning(
            `${appId}/${fb} (fallback): scanned the maxReviewsPerApp limit of ${perApp} review(s) and ${fb2.filteredOut} `
            + `of them were excluded by the review filters (rating/keyword/length/votes/date) — raise maxReviewsPerApp to search deeper.`,
          );
        }
        if (fb2.got > 0) {
          feedServed += totalGot;
          if (watchMode && pairSeeding && keepGoing) seededPairs.add(pairKey);
          continue;
        }
      }
      emptyPairs.push(`${appId}/${country}`);
      const hint = alt?.length
        ? ` Apple does return reviews for this app in: ${alt.join(', ')} — set "countries" to one of those${countryFallback ? '' : ', or enable "countryFallback"'}.`
        : '';
      log.warning(`Apple's review feed for app ${appId} in storefront "${country}" is empty (this is Apple's data, not a scrape failure).${hint}`);
    } else if (pushed === pushedBefore && !watchMode) {
      filteredOutPairs.push(`${appId}/${country}`);
      log.warning(`${appId}/${country}: fetched ${got} reviews but your review filters (rating/keyword/length/votes/date) removed all of them.`);
    }
    feedServed += totalGot;
    // Only mark a pair baselined if its seed walk actually finished -- one cut short by the global
    // SEED_CAP (keepGoing=false) has an incomplete picture of what already exists for that pair.
    if (watchMode && pairSeeding && keepGoing) seededPairs.add(pairKey);
    if (watchMode && !pairSeeding && totalGot >= WATCH_SCAN_CAP && totalNewForPair > 0 && totalNewForPair === totalGot) {
      saturatedPairs.push(pairKey);
      log.warning(`${pairKey}: every matching review in the scanned window was new, so reviews posted since the last run may have been missed further back — run the watch more often.`);
    }
  }
}
// Nothing at all came out of Apple for any pair: before reporting that as an ordinary empty
// result, check whether the feed itself is down (see reviewFeedIsDown). This runs BEFORE the watch
// record is written on purpose — a seeding run that recorded "baselined, 0 reviews" during an
// outage would treat the app's entire back catalogue as new on the next run and charge for it.
if (pairsAttempted > 0 && feedServed === 0 && await reviewFeedIsDown()) {
  await Actor.fail(
    "Apple's customer-review RSS feed (itunes.apple.com/.../rss/customerreviews) returned an empty feed for "
    + 'every app tried, including control apps that have hundreds of thousands of reviews — checked over 3 '
    + 'spaced attempts. That is an Apple-side fault (an outage, or Apple refusing this run\'s network), not '
    + 'your input and not a scrape failure: no filter, storefront or date change will help it, and nothing '
    + 'was charged for this run. It normally clears on its own — re-run later.',
  );
}
if (watchMode) await saveWatchRecord(seeding ? 'seeded' : 'incremental');
log.info(`Done. Pushed ${pushed} items.${unidentifiedSkipped ? ` Skipped ${unidentifiedSkipped} review(s) with no reviewId (cannot be tracked in watch mode, not charged).` : ''}`);
if (watchMode && seeding) {
  await Actor.setStatusMessage(`Baseline run for watch label "${watchLabel}": ${watchSeen.size} existing review(s) across ${seededPairs.size} app/country pair(s) recorded, 0 rows returned, 0 charged. Run it again later to get only what's new.`);
} else if (watchMode && pushed === 0) {
  await Actor.setStatusMessage(`Nothing new for watch label "${watchLabel}" since its last run — all ${watchSkipped} matching review(s) had already been delivered. That is the expected result most of the time; you were charged for nothing.`);
} else if (watchMode && saturatedPairs.length) {
  await Actor.setStatusMessage(`Pushed ${pushed} new item(s) for watch label "${watchLabel}". ${saturatedPairs.join(', ')}: every matching review in the scanned window was new — older new reviews may have been missed; run the watch more often.`);
} else if (watchMode) {
  await Actor.setStatusMessage(`Watch label "${watchLabel}": ${pushed} new item(s) since the last run (${watchSkipped} already-delivered review(s) skipped, not charged).`);
} else if (pushed === 0) {
  const why = depthCappedPairs.length && !emptyPairs.length
    ? `maxReviewsPerApp (${perApp}) was hit before any review passed your review filters (rating/keyword/length/votes/date) for: ${depthCappedPairs.join(', ')} — raise maxReviewsPerApp to search deeper`
    : filteredOutPairs.length && !emptyPairs.length
    ? 'reviews were found but every one was removed by your review filters (rating/keyword/length/votes/date)'
    : `Apple's review feed returned nothing for: ${emptyPairs.join(', ')} (try another storefront in "countries")`;
  await Actor.setStatusMessage(`No reviews returned — ${why}. See the log for details.`);
} else if (depthCappedPairs.length) {
  await Actor.setStatusMessage(`Pushed ${pushed} reviews. maxReviewsPerApp (${perApp}) was hit while filtering: ${depthCappedPairs.join(', ')} — some matching reviews may sit deeper in the feed; raise maxReviewsPerApp to search further.`);
} else if (emptyPairs.length) {
  await Actor.setStatusMessage(`Pushed ${pushed} reviews. Empty Apple feed for: ${emptyPairs.join(', ')}.`);
}

// Fires after every row is already pushed and charged, so a slow or failing webhook can never
// affect the result set or the bill — best-effort only, one attempt, short timeout, failures are
// a warning not a thrown error.
if (webhookUrl) {
  const env = Actor.getEnv();
  const payload = {
    actorRunId: env.actorRunId ?? null,
    defaultDatasetId: env.defaultDatasetId ?? null,
    finishedAt: new Date().toISOString(),
    pushed,
    watchLabel: watchMode ? watchLabel : null,
    watchNewCount: watchMode && !seeding ? pushed : null,
    watchSkipped: watchMode ? watchSkipped : null,
    watchSeeding: watchMode ? seeding : null,
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
