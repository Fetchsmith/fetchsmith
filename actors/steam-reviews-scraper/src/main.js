import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';
import { createHash } from 'node:crypto';

await Actor.init();
// apps/searchTerms carry no length cap, and each app can cost up to 200 sequential paginated review
// fetches (scrapeReviews' page loop below) -- the same compounding-latency shape as the other
// reviews-scrapers' timeout bug: getting hard-killed mid-walk returns nothing even though rows
// already pushed sit in the dataset, and no status message or truncation note is ever written.
// Stop proactively with a safety margin and report what was collected instead (pattern mirrored
// from google-news/hacker-news/app-store-reviews-scraper/google-play-reviews-scraper).
const timeoutAt = Actor.getEnv().timeoutAt?.getTime() ?? null;
const TIME_BUDGET_MARGIN_MS = 45_000;
let timeBudgetExceeded = false;
// Milliseconds of useful work left before the margin starts. Infinity on a local/dev run, where
// the platform sets no deadline.
function remainingMs() { return timeoutAt == null ? Infinity : timeoutAt - Date.now() - TIME_BUDGET_MARGIN_MS; }
function timeBudgetOk() {
  if (remainingMs() <= 0) { timeBudgetExceeded = true; return false; }
  return true;
}
const TIME_BUDGET_WARNING = 'Approaching the run timeout — stopping early and returning what has been collected so far.';
const input = (await Actor.getInput()) ?? {};
const apps = (input.apps ?? []).map((a) => String(a).trim()).filter(Boolean);
const searchTerms = (input.searchTerms ?? []).map((t) => String(t).trim()).filter(Boolean);
const dataType = ['reviews', 'games'].includes(input.dataType) ? input.dataType : 'reviews';
const country = String(input.country || 'us').toLowerCase().trim();
const language = String(input.language || 'english').toLowerCase().trim();
const reviewType = ['all', 'positive', 'negative'].includes(input.reviewType) ? input.reviewType : 'all';
const purchaseType = ['all', 'steam', 'non_steam_purchase'].includes(input.purchaseType) ? input.purchaseType : 'all';
const reviewsAfter = input.reviewsAfter ? new Date(input.reviewsAfter) : null;
const reviewsBefore = input.reviewsBefore ? new Date(input.reviewsBefore) : null;
const hasDateWindow = (reviewsAfter && !isNaN(reviewsAfter)) || (reviewsBefore && !isNaN(reviewsBefore));
// Reviews-after/before need reviews in strict newest-first order to filter and early-stop correctly.
// "funny" is Steam's own fourth ordering (the "Funny" tab on a store page's review list, ranked by
// votes_funny). Verified live 2026-09-26 that it is a real server-side ordering and not an alias:
// on both Dota 2 (570) and Stardew Valley (413150) it returns a population disjoint from all/recent,
// strictly descending in votes_funny, paginating cleanly over 6 cursor pages with 0 duplicates, and
// composing correctly with review_type/purchase_type. Every value Steam does NOT know (toprated,
// helpful, newest, oldest, random, trending, "") returns a byte-identical list to filter=all with
// HTTP 200 and success:1 — so the vocabulary is exactly these four and nothing else.
const SORTS = ['recent', 'updated', 'all', 'funny'];
// Orderings that are not newest-first, so a scan window is not a time window.
const NON_CHRONOLOGICAL = new Set(['all', 'funny']);
let sortBy = SORTS.includes(input.sortBy) ? input.sortBy : 'recent';
if (hasDateWindow && sortBy !== 'recent') {
  log.warning(`Sort was "${sortBy}" but "Reviews after/before" requires chronological order — using "recent" instead.`);
  sortBy = 'recent';
}
const dayRange = input.dayRange != null ? Math.min(Math.max(Number(input.dayRange), 1), 365) : null;
const perAppReviews = Math.min(Number(input.maxReviewsPerApp ?? 200), 5000);
const searchLimit = Math.min(Number(input.searchLimit ?? 10), 50);
const maxResults = Math.min(Number(input.maxResults ?? 2000), 50000);
const includeGameInfo = input.includeGameInfo !== false;
const includePlayerCount = input.includePlayerCount === true;
// Owner estimates + crowd-voted tags come from SteamSpy, a free public API — Steam's own store API
// exposes neither. Verified live 2026-09-18 across 7 apps (Dota 2, CS:GO, Cyberpunk 2077, Stardew
// Valley, Monster Hunter Wilds, CoD MWII, Schedule I): owners, ccu and the 20-tag vote map are
// populated on all of them, while SteamSpy's playtime fields (average_forever / median_forever /
// *_2weeks) are a flat 0 on every single one — dead since Valve hid profile playtime. So this ships
// owners/peak-CCU/tags and deliberately does NOT claim playtime estimates.
// Steam honours day_range only in its most-helpful ordering, so say so rather than letting the
// buyer believe a window was applied. `recent`/`updated` are already chronological (use
// reviewsAfter/reviewsBefore instead); `funny` is all-time and has no date control at all.
if (dayRange && sortBy !== 'all') {
  log.warning(
    `"Last N days" (${dayRange}) is ignored with sortBy="${sortBy}" — Steam only honours a day range in its `
    + 'most-helpful ordering. '
    + (sortBy === 'funny'
      ? 'The funniest ordering is always all-time and Steam offers no date filter for it; use sortBy="recent" '
        + 'with "Reviews after/before" if you need a date window.'
      : 'This ordering is already newest-first, so use "Reviews after/before" for a date window.'),
  );
}
const includeOwnerEstimates = input.includeOwnerEstimates === true;
if (includeOwnerEstimates && dataType !== 'games') {
  log.warning('includeOwnerEstimates is ignored for dataType:"reviews" — owner estimates and tags describe a game, not a review. Set dataType:"games" to get them.');
}
// Valve flags "off-topic review bomb" periods (a controversy, not the game) and Steam's review
// endpoint excludes them by default (filter_offtopic_activity=1). Turning this on asks for the
// unfiltered set, which is exactly what a buyer studying a backlash wants. Verified 2026-09-17 on
// Total War: ROME II (214950): 88,334 reviews filtered vs 94,228 unfiltered.
const includeOffTopic = input.includeOffTopic === true;
const offTopicParam = includeOffTopic ? '0' : '1';
const minPlaytimeHours = input.minPlaytimeHours != null ? Number(input.minPlaytimeHours) : null;
const keyword = String(input.keyword ?? '').normalize('NFC').trim().toLowerCase() || null;

if (!apps.length && !searchTerms.length) {
  await Actor.fail('Provide at least one game in "apps" (Steam store URL or numeric App ID), or at least one query in "searchTerms".');
}

// ---- watch mode ------------------------------------------------------------
// A stateful "only reviews posted since my last run" filter. A Steam review is an event with a
// stable id (recommendationid), so "new" is well defined for dataType:"reviews". dataType:"games"
// returns one row per game — the same snapshot every run, not a stream of events — so watch mode
// does not apply there and is ignored with a warning rather than silently pretending to work.
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
let watchMode = watchLabel.length > 0;
if (watchMode && dataType === 'games') {
  log.warning(`watchLabel "${watchLabel}" is ignored in dataType:"games" — watch mode only applies to dataType:"reviews" (a game row is a snapshot of the same game on every run, not a stream of new events).`);
  watchMode = false;
}
const WATCH_STORE = 'fetchsmith-steam-reviews-watch';
const SEED_CAP = 20000;   // bound the cost/time of a baseline run across all apps
const WATCH_KEEP = 40000; // bound the record size; oldest ids fall off first
let baselineTruncated = 0; // review ids dropped by WATCH_KEEP this run -- they come back as "new" and get charged
let baselineTruncatedTotal = 0; // same, cumulative over the life of this label

function watchKeyFor(label, criteria) {
  const safe = label.toLowerCase().replace(/[^a-z0-9_.-]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 40) || 'default';
  const fp = createHash('sha1').update(JSON.stringify(criteria, Object.keys(criteria).sort())).digest('hex').slice(0, 10);
  return { key: `watch-${safe}-${fp}`, fingerprint: fp };
}

let watchStore = null;
let watchKey = null;
let watchRecord = null;
let seeding = false;
let watchSkipped = 0;
let unidentifiedSkipped = 0; // watch mode only: reviews Steam returned without a recommendationid
const watchSeen = new Set();  // `${appId}:${reviewId}` already delivered under this label+fingerprint
const seededApps = new Set(); // appIds already baselined under this label+fingerprint

if (watchMode) {
  // Everything that decides WHICH reviews get delivered goes into the fingerprint: Steam's
  // server-side filters (language/review_type/purchase_type/day_range/filter) and the client-side
  // ones (keyword/minPlaytimeHours/date window) alike. Raw `input.sortBy` is fingerprinted rather
  // than the date-window-forced value, since that is what the buyer actually typed. Deliberately
  // NOT fingerprinted: maxReviewsPerApp/maxResults (scan and delivery budgets, not filters) and
  // includeGameInfo/includePlayerCount (they change a row's contents, never its identity).
  const criteria = {
    apps: input.apps ?? [], searchTerms: input.searchTerms ?? [], searchLimit,
    country, language, reviewType, purchaseType, sortBy: input.sortBy ?? null, dayRange,
    keyword, minPlaytimeHours,
    reviewsAfter: input.reviewsAfter ?? null, reviewsBefore: input.reviewsBefore ?? null,
    // Only written when true: spelling it as `false` on the default path would change every
    // existing watch fingerprint and reset all live baselines once, for no behaviour change.
    ...(includeOffTopic ? { includeOffTopic: true } : {}),
  };
  watchStore = await Actor.openKeyValueStore(WATCH_STORE);
  const { key, fingerprint } = watchKeyFor(watchLabel, criteria);
  watchKey = key;
  const existing = await watchStore.getValue(key);
  if (existing && Array.isArray(existing.seenIds)) {
    watchRecord = existing;
    for (const id of existing.seenIds) watchSeen.add(String(id));
    for (const a of existing.seededApps ?? []) seededApps.add(String(a));
    log.info(
      `Watch mode "${watchLabel}" (${key}): baseline from ${existing.lastRunAt ?? 'an earlier run'} holds `
      + `${watchSeen.size} already-delivered review(s) across ${seededApps.size} app(s). Only reviews NOT in `
      + 'that baseline will be returned and charged.',
    );
  } else {
    watchRecord = { fingerprint, firstSeededAt: new Date().toISOString(), runCount: 0 };
    seeding = true;
    log.info(
      `Watch mode "${watchLabel}" (${key}): FIRST run for this label and filter set, so this is a baseline run. `
      + 'It records which reviews already exist and returns ZERO rows (you are charged nothing). Run it again on '
      + 'the same label and filters — on a schedule, typically — to get only the reviews posted since now.',
    );
  }
  if (NON_CHRONOLOGICAL.has(sortBy)) {
    const which = sortBy === 'all' ? 'most-helpful' : 'funniest';
    log.warning(
      `Watch mode with sortBy="${sortBy}": that is Steam's ${which} ordering, not a chronological one, so a `
      + `brand-new review is not necessarily inside the ${perAppReviews} review(s) scanned per app and can be `
      + 'missed. Use sortBy="recent" for reliable alerting.',
    );
  }
}

async function saveWatchRecord(status) {
  const ids = Array.from(watchSeen).slice(-WATCH_KEEP);
  // An id past the record cap is not forgotten harmlessly: the next run does not find it in the
  // baseline, so it is delivered and CHARGED again even though the buyer already paid for it.
  // Same shape as us-federal-awards-scraper / app-store-reviews-scraper (h285).
  baselineTruncated = watchSeen.size - ids.length;
  baselineTruncatedTotal = (watchRecord.truncatedTotal ?? 0) + baselineTruncated;
  if (baselineTruncated > 0) {
    log.warning(
      `The baseline for "${watchLabel}" exceeded the ${WATCH_KEEP}-entry record cap; the ${baselineTruncated} `
      + 'oldest review id(s) were dropped and will be returned and CHARGED as new on a future run '
      + `(${baselineTruncatedTotal} dropped over the life of this label). Narrow the watch (fewer apps `
      + 'or a stricter keyword/playtime/date filter) or split it across several labels so each baseline '
      + 'stays under the cap.',
    );
  }
  await watchStore.setValue(watchKey, {
    ...watchRecord,
    label: watchLabel,
    lastRunAt: new Date().toISOString(),
    lastRunStatus: status,
    runCount: (watchRecord.runCount ?? 0) + 1,
    seenCount: ids.length,
    truncatedLastRun: baselineTruncated,
    truncatedTotal: baselineTruncatedTotal,
    seededApps: Array.from(seededApps),
    seenIds: ids,
  });
}

let pushed = 0;
let keepGoing = true;
let chargeLimitReached = false; // Actor.charge()'s own per-event charge limit, not maxResults (h250)
let seedCapHit = false;         // watch seeding stopped at SEED_CAP before the whole match set was recorded
const isPPE = Actor.getChargingManager().getPricingInfo().isPayPerEvent;
async function pushResult(item, watchId = null, appSeeding = false) {
  if (watchMode && watchId != null && appSeeding) {
    watchSeen.add(watchId); // baseline run (or a newly-appeared app): record, never deliver, never charge
    if (watchSeen.size >= SEED_CAP) { keepGoing = false; seedCapHit = true; }
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
    if (r.eventChargeLimitReached) chargeLimitReached = true;
    return !r.eventChargeLimitReached && pushed < maxResults;
  }
  await Actor.pushData(item); pushed += 1; // non-PPE run (e.g. developer test): no charging
  if (watchMode && watchId != null) watchSeen.add(watchId);
  return pushed < maxResults;
}

// got-scraping does NOT throw on 4xx/5xx, so without a status check an error page reaches
// JSON.parse and the customer gets a raw `Unexpected token '<'` (HTML) or `Unexpected end of JSON
// input` (empty body) with no idea which host failed. Measured 2026-09-21: Steam itself is
// forgiving on bad INPUT (an unknown appid, a non-numeric appid and a bogus language all answer
// 200 with an empty/`{"success":2}` body, handled downstream), so what this guard is really for is
// the transport-level failures a long review pull does hit — 429 rate-limiting and Steam's HTML
// maintenance/error pages. Same defect class as the 0.1.43 Shopify fix.
// got's own retry:{limit:2} only covers a fixed errorCodes list that excludes ERR_HTTP2_ERROR and
// HPE_INVALID_CONSTANT — a connection-establishment fault measured cycle 616 at ~1-in-4 fresh
// connections on this fleet's got-scraping version. Every getJson call site degrades gracefully on
// a thrown error (null field, warning, or loop break) rather than failing the run, so an unretried
// blip here doesn't crash anything — it silently ships a thinner row or a shorter review page and
// the run still SUCCEEDS. requestWithRetry closes that gap the same way as the other Pattern-B fixes
// (apple-podcasts-scraper, app-store-reviews-scraper, shopify-products-scraper, ats-jobs-scraper,
// hacker-news-scraper, google-news-scraper, remote-jobs-scraper): retry thrown/connection errors up
// to 3 attempts with backoff; a resolved HTTP response (including 4xx/5xx) is not retried here — that
// stays getJson's job below.
const requestWithRetry = async (url, opts, attempts = 3) => {
  for (let attempt = 1; ; attempt++) {
    try {
      return await gotScraping({ url, timeout: { request: 30000 }, retry: { limit: 2 }, ...opts });
    } catch (e) {
      if (attempt >= attempts) throw e;
      await sleep(attempt * 1000);
    }
  }
};
const getJson = async (url, opts = {}) => {
  const resp = await requestWithRetry(url, opts);
  const host = new URL(url).hostname;
  if (resp.statusCode >= 400) {
    const hint = resp.statusCode === 429
      ? ` ${host} is rate-limiting this run; wait a few minutes, or lower "maxResults"/the number of apps per run.`
      : (resp.statusCode >= 500 ? ` ${host} is having a server-side problem; this is usually temporary.` : '');
    throw new Error(`${host} returned HTTP ${resp.statusCode}.${hint}`);
  }
  try {
    return JSON.parse(resp.body);
  } catch {
    throw new Error(`${host} returned HTTP ${resp.statusCode} with a body that is not JSON (${resp.body ? `starts with ${JSON.stringify(String(resp.body).slice(0, 60))}` : 'empty body'}) — usually a Steam error or maintenance page.`);
  }
};
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// Steam serves a COMPLETE query_summary (review_score_desc / total_reviews / total_positive / …) on
// the first review page whenever review_type and purchase_type are both unfiltered — including when
// the honest answer is "no reviews", which comes back as total_reviews:0. So under those defaults a
// first page of success:1 + reviews:[] + a summary with NO total_reviews key is Steam handing back a
// degenerate body, not a real empty result. (Observed 2026-09-15 for ~hours across two apps with
// 142k/1.5M real reviews and two different IPs; recovered on its own.) With review_type or
// purchase_type set, Steam trims the summary to {num_reviews} even on legitimate empty answers, so
// the signal is unavailable and this check correctly stays off.
const unfilteredQuery = reviewType === 'all' && purchaseType === 'all';
const looksDegenerate = (body) => unfilteredQuery && body?.success === 1
  && !(body.reviews?.length) && body?.query_summary?.total_reviews === undefined;

// Steam store URLs are /app/<appid>/<slug>/; a bare numeric ID is also accepted.
const parseAppId = (s) => (s.match(/\/app\/(\d+)/)?.[1] || s.match(/^\d{1,8}$/)?.[0] || s.match(/[?&]appids?=(\d+)/)?.[1] || null);

const iso = (t) => (t ? new Date(Number(t) * 1000).toISOString() : null);
const cents = (v) => (typeof v === 'number' ? Math.round(v) / 100 : null);

function gameRow(appId, d, summary, players, owners) {
  const price = d?.price_overview ?? null;
  return {
    type: 'game',
    appId: Number(appId),
    name: d?.name ?? null,
    appType: d?.type ?? null,
    storeUrl: `https://store.steampowered.com/app/${appId}/`,
    isFree: d?.is_free ?? null,
    priceCurrency: price?.currency ?? null,
    price: cents(price?.final),
    priceInitial: cents(price?.initial),
    discountPercent: price?.discount_percent ?? null,
    releaseDate: d?.release_date?.date ?? null,
    comingSoon: d?.release_date?.coming_soon ?? null,
    developers: d?.developers ?? null,
    publishers: d?.publishers ?? null,
    genres: d?.genres?.map?.((g) => g.description) ?? null,
    categories: d?.categories?.map?.((c) => c.description) ?? null,
    platforms: d?.platforms ? Object.keys(d.platforms).filter((k) => d.platforms[k]) : null,
    metacriticScore: d?.metacritic?.score ?? null,
    requiredAge: d?.required_age ?? null,
    shortDescription: d?.short_description ?? null,
    website: d?.website ?? null,
    headerImage: d?.header_image ?? null,
    supportedLanguages: d?.supported_languages ?? null,
    dlcCount: d?.dlc?.length ?? null,
    // review score summary comes from the reviews endpoint, not appdetails
    reviewScore: summary?.review_score ?? null,
    reviewScoreDesc: summary?.review_score_desc ?? null,
    totalReviews: summary?.total_reviews ?? null,
    totalPositive: summary?.total_positive ?? null,
    totalNegative: summary?.total_negative ?? null,
    positivePercent: summary?.total_reviews
      ? Math.round((summary.total_positive / summary.total_reviews) * 1000) / 10
      : null,
    currentPlayers: players ?? null,
    // SteamSpy enrichment (includeOwnerEstimates). Present as explicit nulls when the flag is on but
    // SteamSpy had no data, absent entirely when the flag is off, so an unenriched row keeps its
    // existing shape exactly.
    ...(includeOwnerEstimates
      ? {
        ownersEstimate: owners?.ownersEstimate ?? null,
        ownersMin: owners?.ownersMin ?? null,
        ownersMax: owners?.ownersMax ?? null,
        peakConcurrentYesterday: owners?.peakConcurrentYesterday ?? null,
        steamSpyTags: owners?.steamSpyTags ?? null,
        steamSpyTagVotes: owners?.steamSpyTagVotes ?? null,
      }
      : {}),
    country,
  };
}

function reviewRow(appId, r, info) {
  const a = r.author ?? {};
  return {
    type: 'review',
    appId: Number(appId),
    reviewId: r.recommendationid ?? null,
    review: r.review ?? null,
    language: r.language ?? null,
    recommended: r.voted_up ?? null,
    createdAt: iso(r.timestamp_created),
    updatedAt: iso(r.timestamp_updated),
    votesUp: r.votes_up ?? 0,
    votesFunny: r.votes_funny ?? 0,
    weightedVoteScore: r.weighted_vote_score != null ? Number(r.weighted_vote_score) : null,
    commentCount: r.comment_count ?? 0,
    steamPurchase: r.steam_purchase ?? null,
    receivedForFree: r.received_for_free ?? null,
    writtenDuringEarlyAccess: r.written_during_early_access ?? null,
    refunded: r.refunded ?? null,
    steamDeck: r.primarily_steam_deck ?? null,
    playtimeForeverHours: a.playtime_forever != null ? Math.round(a.playtime_forever / 6) / 10 : null,
    playtimeAtReviewHours: a.playtime_at_review != null ? Math.round(a.playtime_at_review / 6) / 10 : null,
    playtimeLastTwoWeeksHours: a.playtime_last_two_weeks != null ? Math.round(a.playtime_last_two_weeks / 6) / 10 : null,
    authorSteamId: a.steamid ?? null,
    authorName: a.personaname ?? null,
    authorProfileUrl: a.profile_url ?? null,
    authorNumGamesOwned: a.num_games_owned ?? null,
    authorNumReviews: a.num_reviews ?? null,
    authorLastPlayedAt: iso(a.last_played),
    reviewUrl: r.recommendationid ? `https://steamcommunity.com/profiles/${a.steamid}/recommended/${appId}/` : null,
    hardwareOs: r.hardware?.os ?? null,
    hardwareCpu: r.hardware?.cpu_name?.trim() ?? null,
    hardwareGpu: r.hardware?.adapter_description ?? null,
    hardwareRamMb: r.hardware?.system_ram != null ? Number(r.hardware.system_ram) : null,
    hardwareVramMb: r.hardware?.vram_size ?? null,
    ...(info || {}),
  };
}

function reviewPassesFilters(item) {
  if (minPlaytimeHours != null && !(item.playtimeForeverHours >= minPlaytimeHours)) return false;
  if (keyword && !(item.review || '').normalize('NFC').toLowerCase().includes(keyword)) return false;
  if (reviewsAfter && !isNaN(reviewsAfter) && new Date(item.createdAt) < reviewsAfter) return false;
  if (reviewsBefore && !isNaN(reviewsBefore) && new Date(item.createdAt) >= reviewsBefore) return false;
  return true;
}

// Game-level metadata attached to every review row when includeGameInfo is on.
const infoCache = new Map();
async function getGameInfo(appId) {
  if (!includeGameInfo) return null;
  if (infoCache.has(appId)) return infoCache.get(appId);
  let info = null;
  const d = await getAppDetails(appId);
  if (d) {
    info = {
      gameName: d.name ?? null,
      developers: d.developers ?? null,
      publishers: d.publishers ?? null,
      genres: d.genres?.map?.((g) => g.description) ?? null,
      releaseDate: d.release_date?.date ?? null,
      storeUrl: `https://store.steampowered.com/app/${appId}/`,
    };
  }
  infoCache.set(appId, info);
  return info;
}

const detailsCache = new Map();
async function getAppDetails(appId) {
  if (detailsCache.has(appId)) return detailsCache.get(appId);
  let d = null;
  try {
    const url = `https://store.steampowered.com/api/appdetails?appids=${appId}&cc=${country}&l=english`;
    const body = await getJson(url);
    // Steam answers { "<appid>": { success: false } } for delisted/region-locked/nonexistent apps.
    d = body?.[String(appId)]?.success ? body[String(appId)].data : null;
  } catch (e) { log.warning(`appdetails failed for ${appId}: ${e.message}`); }
  detailsCache.set(appId, d);
  return d;
}

// SteamSpy asks for at most 1 appdetails request per second; the games loop paces itself with a
// sleep between calls. A failure here degrades the row to null estimate fields, it never fails the
// run — the Steam-sourced half of the row is still complete and worth delivering.
const OWNERS_RE = /^\s*([\d,]+)\s*\.\.\s*([\d,]+)\s*$/;
async function getOwnerEstimates(appId) {
  try {
    const s = await getJson(`https://steamspy.com/api.php?request=appdetails&appid=${appId}`);
    // SteamSpy answers 200 for an appid it does not know, echoing the appid back with name:null and
    // a FABRICATED owners:"0 .. 20,000" floor (verified live on appid 99999999). Delivering that as
    // an estimate would be selling a made-up number, so name:null is the "no data" signal.
    if (!s || s.appid == null || !s.name) return null;
    const m = OWNERS_RE.exec(String(s.owners ?? ''));
    const tagVotes = (s.tags && !Array.isArray(s.tags) && typeof s.tags === 'object') ? s.tags : null;
    return {
      ownersEstimate: s.owners || null,
      ownersMin: m ? Number(m[1].replace(/,/g, '')) : null,
      ownersMax: m ? Number(m[2].replace(/,/g, '')) : null,
      peakConcurrentYesterday: typeof s.ccu === 'number' ? s.ccu : null,
      steamSpyTags: tagVotes ? Object.keys(tagVotes).sort((a, b) => tagVotes[b] - tagVotes[a]) : null,
      steamSpyTagVotes: tagVotes,
    };
  } catch (e) {
    log.warning(`SteamSpy owner estimates failed for ${appId}: ${e.message} — ownersEstimate/steamSpyTags will be null in this row.`);
    return null;
  }
}

async function getPlayerCount(appId) {
  try {
    const r = await getJson(`https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid=${appId}`);
    return r?.response?.result === 1 ? r.response.player_count ?? null : null;
  } catch (e) { log.debug(`player count failed for ${appId}: ${e.message}`); return null; }
}

// Steam's own start_date/end_date/date_range_type=include filters at the source instead of paging
// back from "now" and discarding everything newer than the window client-side — verified live that
// it holds across cursor pages (0 overlap, strictly decreasing timestamps, clean termination) when
// combined with filter="recent" (forced above whenever a date window is set). filter="all" + this
// combo is NOT safe: measured live, it gets stuck returning the same cursor/page forever. Also:
// start_date=0 is silently treated as absent and drops end_date filtering too, so a window with only
// "reviewsBefore" needs a real nonzero placeholder rather than 0 — Steam review IDs don't predate 2010.
const NO_LOWER_BOUND_SENTINEL = 1;
function reviewsUrl(appId, cursor) {
  const p = new URLSearchParams({
    json: '1',
    filter: sortBy,
    language,
    review_type: reviewType,
    purchase_type: purchaseType,
    filter_offtopic_activity: offTopicParam,
    num_per_page: '100',
    cursor,
  });
  // day_range only applies to filter=all (Steam's "most helpful over the last N days" mode).
  // Verified live 2026-09-26 that filter=funny ignores it outright: day_range 7 vs 365 vs absent all
  // return the byte-identical page, and funny is all-time by default (unlike `all`, which Steam caps
  // to 30 days). Sending it anyway would be a silent no-op, so it is withheld and warned about below.
  if (dayRange && sortBy === 'all') p.set('day_range', String(dayRange));
  if (hasDateWindow) {
    p.set('date_range_type', 'include');
    const start = reviewsAfter && !isNaN(reviewsAfter) ? Math.floor(reviewsAfter.getTime() / 1000) : NO_LOWER_BOUND_SENTINEL;
    p.set('start_date', String(start));
    if (reviewsBefore && !isNaN(reviewsBefore)) p.set('end_date', String(Math.floor(reviewsBefore.getTime() / 1000)));
  }
  return `https://store.steampowered.com/appreviews/${appId}?${p.toString()}`;
}

const summaries = new Map();
async function scrapeReviews(appId) {
  const info = await getGameInfo(appId);
  // An app absent from the baseline is seeded in place rather than having its whole back
  // catalogue delivered as "new" — this covers a searchTerms query resolving to a different game
  // than last run, which changes the watched target set without changing the fingerprint.
  const appSeeding = watchMode && (seeding || !seededApps.has(String(appId)));
  if (watchMode && !seeding && appSeeding) {
    log.info(`App ${appId}: not in the baseline for "${watchLabel}" yet — baselining it this run instead of delivering its existing reviews.`);
  }
  let cursor = '*';
  let got = 0;
  let filteredOut = 0;
  let newForApp = 0;
  const seen = new Set();
  let degenerate = false;
  for (let page = 0; page < 200 && got < perAppReviews && keepGoing; page++) {
    if (!timeBudgetOk()) { keepGoing = false; log.warning(TIME_BUDGET_WARNING); break; }
    let body;
    try { body = await getJson(reviewsUrl(appId, cursor)); } // URLSearchParams below already encodes the cursor — do not encode it twice
    catch (e) { log.warning(`review page ${page + 1} failed for ${appId}: ${e.message}`); break; }
    // An incomplete first page is usually a short-lived Steam hiccup, so give it two spaced retries
    // before believing it — got-scraping's own retries fire too fast to outlast one.
    for (let attempt = 1; attempt <= 2 && page === 0 && looksDegenerate(body); attempt++) {
      log.warning(`Steam returned an incomplete review response for app ${appId} (no reviews and no review totals) — retrying in ${attempt * 5}s (attempt ${attempt}/2).`);
      await sleep(attempt * 5000);
      try { body = await getJson(reviewsUrl(appId, cursor)); }
      catch (e) { log.warning(`retry ${attempt} failed for ${appId}: ${e.message}`); break; }
    }
    if (page === 0 && looksDegenerate(body)) { degenerate = true; break; }
    if (body?.success !== 1) { log.warning(`Steam refused the review query for app ${appId} (success=${body?.success}).`); break; }
    if (page === 0 && body.query_summary) summaries.set(appId, body.query_summary);
    const reviews = body.reviews ?? [];
    if (!reviews.length) break;
    let pastWindow = false;
    for (const r of reviews) {
      if (got >= perAppReviews || !keepGoing) break;
      if (seen.has(r.recommendationid)) continue; // Steam repeats the last page when the cursor runs out
      seen.add(r.recommendationid);
      got += 1;
      const item = { ...reviewRow(appId, r, info), scrapedAt: new Date().toISOString() };
      // sort=recent is strictly newest-created-first, so once we're older than "reviewsAfter"
      // every review from here on (this page and all later pages) is also too old — stop paging.
      if (reviewsAfter && !isNaN(reviewsAfter) && new Date(item.createdAt) < reviewsAfter) { pastWindow = true; break; }
      if (!reviewPassesFilters(item)) { filteredOut += 1; continue; }
      if (watchMode && !item.reviewId) {
        // No stable id means it can be neither recorded in the baseline nor recognised next run,
        // so delivering it would re-charge for the same row on every scheduled watch run.
        unidentifiedSkipped += 1;
        continue;
      }
      const watchId = watchMode ? `${appId}:${item.reviewId}` : null;
      // Counts reviews that passed the filters AND were not already in the baseline — the
      // saturation signal below. Distinct from pushResult's own watchSkipped bookkeeping.
      if (!(watchMode && !appSeeding && watchSeen.has(watchId))) newForApp += 1;
      keepGoing = await pushResult(item, watchId, appSeeding);
    }
    if (pastWindow) break;
    const next = body.cursor;
    if (!next || next === cursor) break; // same cursor twice = end of feed
    cursor = next;
  }
  // maxReviewsPerApp caps reviews SCANNED, before keyword/minPlaytimeHours filtering — if the cap
  // was hit and some scanned reviews were dropped by a filter, matching reviews may still sit
  // deeper in the feed and were never looked at.
  const capReached = got >= perAppReviews;
  return { got, filteredOut, capReached, degenerate, newForApp, appSeeding };
}

// ---- resolve targets -------------------------------------------------------
const ids = [];
const seenIds = new Set();
const addId = (id) => { if (id && !seenIds.has(id)) { seenIds.add(id); ids.push(id); } };
for (const a of apps) {
  const id = parseAppId(a);
  if (id) addId(id);
  else log.warning(`Cannot parse an App ID from "${a}" — use a Steam store URL (…/app/1145360/Hades/) or the numeric App ID.`);
}

const emptySearches = [];
for (const term of searchTerms) {
  if (!keepGoing) break;
  if (!timeBudgetOk()) { keepGoing = false; log.warning(TIME_BUDGET_WARNING); break; }
  try {
    const url = `https://store.steampowered.com/api/storesearch/?term=${encodeURIComponent(term)}&l=english&cc=${country}`;
    const items = (await getJson(url)).items ?? [];
    const games = items.filter((i) => i.type === 'app').slice(0, searchLimit);
    if (!games.length) { emptySearches.push(term); log.warning(`Search "${term}" matched no Steam games in country "${country}".`); continue; }
    log.info(`Search "${term}": ${games.length} games (${games.map((g) => g.name).join(', ')}).`);
    for (const g of games) addId(String(g.id));
  } catch (e) { log.warning(`Search "${term}" failed: ${e.message}`); }
}

// ---- run -------------------------------------------------------------------
const emptyIds = [];
// Apps where Steam itself served an incomplete review response (see looksDegenerate) — kept apart
// from emptyIds so an upstream fault is never reported to the user as "no reviews match".
const upstreamDegraded = [];
// Apps where maxReviewsPerApp was hit while the keyword/minPlaytimeHours filter was still
// discarding reviews — reviews deeper in Steam's feed were never scanned.
const depthCapped = [];
// Watch mode: apps where the whole scanned window was new, i.e. the scan may not reach back far
// enough to cover everything posted since the last run.
const saturatedApps = [];
// Watch mode: apps that appeared in an already-established watch (e.g. a searchTerms query that
// now resolves to a different game) and were baselined this run instead of being delivered.
const baselinedInPlace = [];
let ownersCalls = 0;
const ownersMissing = [];
// Ids the loop actually got to. Everything in ids but NOT in here was abandoned by an early stop
// (time budget, maxResults, charge limit) and contributed zero rows -- the silent-shortfall case
// the end-of-run report needs to name instead of leaving unexplained.
const idsAttempted = new Set();
if (dataType === 'games') {
  for (const id of ids) {
    if (!keepGoing) break;
    if (!timeBudgetOk()) { keepGoing = false; log.warning(TIME_BUDGET_WARNING); break; }
    idsAttempted.add(String(id));
    const d = await getAppDetails(id);
    if (!d) {
      emptyIds.push(id);
      log.warning(`Steam returned no store data for app ${id} in country "${country}" — the app may be delisted, region-locked, or the ID may not be a Steam App ID.`);
      continue;
    }
    let summary = null;
    try {
      // Language/purchase filters are deliberately left off so the totals are the game's own, but
      // the off-topic flag follows the run's setting: a row whose reviewScore silently excluded a
      // review bomb the buyer explicitly asked to include would contradict its own reviews.
      const body = await getJson(`https://store.steampowered.com/appreviews/${id}?json=1&num_per_page=0&language=all&purchase_type=all&filter_offtopic_activity=${offTopicParam}`);
      summary = body?.query_summary ?? null;
      // Nothing here can legitimately return an empty set, so a missing total_reviews is
      // unambiguously Steam serving an incomplete body — say so instead of shipping a row with
      // silently null review scores.
      if (summary && summary.total_reviews === undefined) {
        log.warning(`Steam returned an incomplete review summary for app ${id} — reviewScore/totalReviews will be null in this row. Upstream fault; re-run later for those fields.`);
        summary = null;
      }
    } catch (e) { log.debug(`review summary failed for ${id}: ${e.message}`); }
    const players = includePlayerCount ? await getPlayerCount(id) : null;
    let owners = null;
    if (includeOwnerEstimates) {
      if (ownersCalls > 0) await sleep(1100); // SteamSpy: max 1 appdetails request/second
      ownersCalls += 1;
      owners = await getOwnerEstimates(id);
      if (!owners) ownersMissing.push(id);
    }
    keepGoing = await pushResult({ ...gameRow(id, d, summary, players, owners), scrapedAt: new Date().toISOString() });
  }
} else {
  for (const id of ids) {
    if (!keepGoing) break;
    if (!timeBudgetOk()) { keepGoing = false; log.warning(TIME_BUDGET_WARNING); break; }
    idsAttempted.add(String(id));
    const before = pushed;
    const { got, filteredOut, capReached, degenerate, newForApp, appSeeding } = await scrapeReviews(id);
    log.info(appSeeding
      ? `${id}: ${got} reviews fetched, ${newForApp} recorded in the watch baseline (0 delivered, 0 charged).`
      : watchMode
        ? `${id}: ${got} reviews fetched, ${pushed - before} new since the last run (the rest were already delivered or filtered out).`
        : `${id}: ${got} reviews fetched, ${pushed - before} kept after filters.`);
    // Only mark an app baselined if its seed walk actually finished — one cut short by SEED_CAP or
    // by a degenerate upstream response must be re-seeded, not treated as a complete baseline.
    if (watchMode && appSeeding && keepGoing && !degenerate) {
      seededApps.add(String(id));
      if (!seeding) baselinedInPlace.push(id);
    }
    // Watch mode: every matching review inside the scanned window was new, so reviews posted since
    // the last run may sit deeper in the feed and were never looked at.
    if (watchMode && !appSeeding && capReached && newForApp > 0 && newForApp === got - filteredOut) {
      saturatedApps.push(id);
      log.warning(`App ${id}: every matching review in the ${perAppReviews} scanned was new, so reviews posted since the last run may have been missed further back — raise maxReviewsPerApp or run the watch more often.`);
    }
    if (capReached && filteredOut > 0) {
      log.warning(
        `App ${id}: scanned the maxReviewsPerApp limit of ${perAppReviews} review(s) and ${filteredOut} of them `
        + `were excluded by the keyword/minPlaytimeHours filter. The cap counts reviews scanned, before filtering `
        + `— raise maxReviewsPerApp to search deeper.`,
      );
      depthCapped.push(id);
    }
    if (degenerate) {
      upstreamDegraded.push(id);
      log.warning(
        `Steam's review API kept returning an incomplete response for app ${id} after 2 retries — `
        + `success, but no reviews and no review totals. This is an upstream Steam fault, not a filter `
        + `problem and not a sign that the app has no reviews; re-run this input later.`,
      );
    } else if (got === 0) {
      emptyIds.push(id);
      const s = summaries.get(id);
      log.warning(s && s.total_reviews === 0
        ? `App ${id} has no Steam reviews at all yet (that is Steam's data, not a scrape failure).`
        : `Steam returned no reviews for app ${id} with language="${language}", review_type="${reviewType}", purchase_type="${purchaseType}" — try language "all" or a different filter.`);
    }
  }
}

if (ownersMissing.length) {
  log.warning(`SteamSpy had no owner estimates for ${ownersMissing.length} app(s): ${ownersMissing.slice(0, 10).join(', ')}${ownersMissing.length > 10 ? ', …' : ''}. Those rows still carry every Steam-sourced field; ownersEstimate/peakConcurrentYesterday/steamSpyTags are null. SteamSpy typically lacks unreleased apps, non-game items (DLC, soundtracks, software) and very new releases.`);
}
log.info(`Done. Pushed ${pushed} ${dataType === 'games' ? 'games' : 'reviews'}.${unidentifiedSkipped ? ` Skipped ${unidentifiedSkipped} review(s) with no reviewId (cannot be tracked in watch mode, not charged).` : ''}`);

// An upstream fault that produced nothing is a failed run, not an empty one: surfacing it as a
// success would tell the user their games have no reviews, which is the opposite of the truth.
// Deliberately NOT Actor.fail() here (h250, same shape as fec-campaign-finance-scraper cycle 676):
// Actor.fail() exits the process immediately, which would skip the watch-baseline save below and the
// RUN_SUMMARY record entirely. Record the error, let the tail of the script persist state, and fail
// at the very end instead.
let runError = null;
if (pushed === 0 && upstreamDegraded.length) {
  runError = `Steam's review API returned incomplete responses (success, but no reviews and no review `
    + `totals) for: ${upstreamDegraded.join(', ')} — after 2 retries each. This is an upstream Steam `
    + `fault, not a problem with your input; please re-run later.`;
  log.error(runError);
}

// A failed SEEDING run must NOT leave a partial baseline behind: an app the seed walk never reached
// would look already-baselined to the next run and instead has its whole review history delivered
// and CHARGED as "new". No record at all is the cheap outcome — the next run simply re-seeds for free.
const skipBaselineSave = watchMode && seeding && runError !== null;
if (skipBaselineSave) {
  log.warning(
    `The baseline run for "${watchLabel}" failed before it finished, so NO baseline was saved. `
    + 'Re-run on the same label and filters to seed again (a baseline run charges nothing). Saving '
    + 'a partial baseline would have made the next run treat the un-reached app(s) as freshly '
    + 'baselined and charge for every one of their existing reviews.',
  );
}
if (watchMode && !skipBaselineSave) await saveWatchRecord(runError ? 'failed-incremental' : (seeding ? 'seeded' : 'incremental'));

// An early time-budget stop silently truncates the id list, not just the row count: ids after the
// stopping point were never fetched at all, and none of the per-id buckets below (emptyIds,
// upstreamDegraded, depthCapped) know about them, so without this the run reads as a complete one
// that simply found less.
const idsNotReached = ids.map(String).filter((id) => !idsAttempted.has(id));

// Completeness bookkeeping (h250, same shape as fec-campaign-finance-scraper cycle 676). First
// cause wins: report whichever stopping reason the buyer can act on first.
let complete = true;
let incompleteReason = null;
let incompleteDetail = null;
function markIncomplete(reason, detail = null) {
  if (!complete) return;
  complete = false;
  incompleteReason = reason;
  incompleteDetail = detail;
}
if (runError) markIncomplete('upstream-error', runError);
// Top priority ahead of chargeLimitHit/maxResults/seed-cap (fleet convention, cycles 767-769): a
// timeout is our own clock, not something the other reasons' advice ("raise maxResults") would fix.
if (timeBudgetExceeded) markIncomplete('time-budget', idsNotReached.length
  ? `the run was approaching the platform run timeout and stopped before finishing the id list — ${idsNotReached.length} id(s) were never fetched: ${idsNotReached.join(', ')}`
  : 'the run was approaching the platform run timeout and stopped early to return what it had');
if (chargeLimitReached) markIncomplete('charge-limit', "the run's pay-per-event charge limit was reached");
if (pushed >= maxResults) markIncomplete('max-results', `maxResults=${maxResults} reached; more reviews may exist`);
if (watchMode && seeding && seedCapHit) markIncomplete('seed-cap', `the baseline stopped at the ${SEED_CAP}-review cap; reviews past the cap will be delivered and charged as new on a later incremental run`);
if (upstreamDegraded.length) markIncomplete('upstream-degraded', `Steam returned incomplete responses for: ${upstreamDegraded.join(', ')}`);
if (depthCapped.length) markIncomplete('depth-cap', `maxReviewsPerApp (${perAppReviews}) was hit while filtering for: ${depthCapped.join(', ')} — matching reviews may sit deeper in the feed`);
if (watchMode && !seeding && saturatedApps.length) markIncomplete('watch-saturated', `every scanned review was new for: ${saturatedApps.join(', ')} — older new reviews may have been missed`);

// A watch status message still has to carry the upstream-fault notice when only SOME apps were
// degraded (a fully-degraded run already failed above) — those apps were not baselined and their
// reviews were never scanned, so "nothing new" would be a misleading thing to leave unqualified.
const baselinedSuffix = baselinedInPlace.length
  ? ` Newly-watched app(s) ${baselinedInPlace.join(', ')} were baselined this run instead of having their whole review history delivered — you will get their new reviews from the next run on.`
  : '';
const degradedSuffix = upstreamDegraded.length
  ? ` Steam's review API returned incomplete responses for: ${upstreamDegraded.join(', ')} — an upstream fault, not your input; those apps were skipped, re-run them later.`
  : '';
// WATCH_KEEP record-cap eviction (h285): empty unless something was actually dropped, so it
// never adds noise to a healthy run.
const evictionSuffix = baselineTruncated > 0
  ? ` WARNING: the watch baseline hit its ${WATCH_KEEP}-entry cap and ${baselineTruncated} oldest review `
    + `id(s) were dropped (${baselineTruncatedTotal} dropped over the life of this label) — they will be `
    + 'returned and charged again as "new" on a future run. Narrow the watch (fewer apps or a stricter '
    + 'filter) so the baseline stays under the cap.'
  : '';
// Placed before watch mode's reassuring "nothing new" / "baseline recorded" messages, which would
// otherwise misreport a timeout-truncated run as a clean, complete one (same lie class fixed in
// app-store-reviews-scraper cycle 768 and google-play-reviews-scraper cycle 769).
const timeoutSuffix = idsNotReached.length
  ? ` The run was approaching the platform run timeout and stopped before finishing the id list — ${idsNotReached.length} id(s) were never fetched: ${idsNotReached.join(', ')}. Narrow the input (fewer apps/search terms, or a lower "maxReviewsPerApp"), raise the Actor's run timeout, or run the rest separately.`
  : '';
if (timeBudgetExceeded && pushed === 0 && watchMode && seeding) {
  await Actor.setStatusMessage(`Baseline run for watch label "${watchLabel}" did not finish — the run was approaching the platform run timeout.${timeoutSuffix} ${watchSeen.size} review(s) across ${seededApps.size} app(s) were recorded before it stopped; 0 rows returned, 0 charged. Re-run to finish seeding before switching to incremental runs.`);
} else if (timeBudgetExceeded && pushed === 0 && watchMode) {
  await Actor.setStatusMessage(`No new reviews delivered for watch label "${watchLabel}" — the run was approaching the platform run timeout, not confirmation that nothing is new.${timeoutSuffix}`);
} else if (watchMode && seeding) {
  await Actor.setStatusMessage(`Baseline run for watch label "${watchLabel}": ${watchSeen.size} existing review(s) across ${seededApps.size} app(s) recorded, 0 rows returned, 0 charged. Run it again later to get only what's new.${degradedSuffix}${evictionSuffix}`);
} else if (watchMode && pushed === 0) {
  await Actor.setStatusMessage(`Nothing new for watch label "${watchLabel}" since its last run — all ${watchSkipped} matching review(s) had already been delivered. That is the expected result most of the time; you were charged for nothing.${baselinedSuffix}${degradedSuffix}${evictionSuffix}`);
} else if (watchMode && saturatedApps.length) {
  await Actor.setStatusMessage(`Pushed ${pushed} new review(s) for watch label "${watchLabel}". Every matching review in the scanned window was new for: ${saturatedApps.join(', ')} — older new reviews may have been missed; raise maxReviewsPerApp or run the watch more often.${baselinedSuffix}${degradedSuffix}${evictionSuffix}`);
} else if (watchMode) {
  await Actor.setStatusMessage(`Watch label "${watchLabel}": ${pushed} new review(s) since the last run (${watchSkipped} already-delivered review(s) skipped, not charged).${baselinedSuffix}${degradedSuffix}${evictionSuffix}`);
} else if (pushed === 0) {
  // timeBudgetExceeded checked FIRST: without it, timing out before any id was even attempted falls
  // into the final default below ("no valid Steam App IDs could be parsed from your input") -- a
  // false claim about the input when the real cause is our own clock (idsAttempted stays empty, so
  // emptyIds/emptySearches/depthCapped are all empty too, not because nothing matched).
  const why = timeBudgetExceeded && idsAttempted.size === 0
    ? 'the run was approaching the platform run timeout and stopped before any id could be checked'
    : emptyIds.length
    ? `Steam returned nothing for: ${emptyIds.join(', ')} (language "${language}", country "${country}")`
    : emptySearches.length
      ? `your search terms matched no Steam games: ${emptySearches.join(', ')}`
      : depthCapped.length
        ? `maxReviewsPerApp (${perAppReviews}) was hit before any review passed your keyword/minPlaytimeHours filter for: ${depthCapped.join(', ')} — raise maxReviewsPerApp to search deeper`
        : keyword || minPlaytimeHours != null || hasDateWindow
          ? 'every review Steam returned was removed by your keyword / minimum-playtime / date-window filters'
          : 'no valid Steam App IDs could be parsed from your input';
  await Actor.setStatusMessage(`No results — ${why}.${timeBudgetExceeded ? timeoutSuffix : ' See the log for details.'}`);
} else if (upstreamDegraded.length) {
  // Partial success: other apps produced rows, so the run is not a failure, but the user still
  // needs to know these specific apps are missing for an upstream reason and are worth re-running.
  await Actor.setStatusMessage(`Pushed ${pushed} results. Steam's review API returned incomplete responses for: ${upstreamDegraded.join(', ')} — an upstream fault, not your input; re-run those later.${timeoutSuffix}`);
} else if (depthCapped.length) {
  await Actor.setStatusMessage(`Pushed ${pushed} results. maxReviewsPerApp (${perAppReviews}) was hit while filtering: ${depthCapped.join(', ')} — some matching reviews may sit deeper in the feed; raise maxReviewsPerApp to search further.${timeoutSuffix}`);
} else if (emptyIds.length) {
  await Actor.setStatusMessage(`Pushed ${pushed} results. Steam returned nothing for: ${emptyIds.join(', ')}.${timeoutSuffix}`);
} else if (timeBudgetExceeded) {
  await Actor.setStatusMessage(`Pushed ${pushed} results.${timeoutSuffix}`);
} else if (!complete) {
  // Reaches here only for a non-watch run that hit maxResults or the charge limit cleanly (no
  // upstream/depth/empty issue), which none of the branches above cover.
  await Actor.setStatusMessage(`Pushed ${pushed} results — incomplete: ${incompleteReason}${incompleteDetail ? ` (${incompleteDetail})` : ''}. See RUN_SUMMARY for details.`);
}

// RUN_SUMMARY: this run's completeness, in a form a pipeline can read (h250, same shape as
// fec-campaign-finance-scraper cycle 676). Fetch with
//   GET /v2/actor-runs/<runId>/key-value-store/records/RUN_SUMMARY
// which needs no webhook.
const runSummary = {
  mode: watchMode ? (seeding ? 'watch-seed' : 'watch-incremental') : dataType,
  dataType,
  appsRequested: ids.length,
  delivered: pushed,
  emptySearches,
  emptyIds,
  upstreamDegraded,
  depthCapped,
  timeBudgetExceeded,
  idsNotReached,
  saturatedApps: watchMode ? saturatedApps : null,
  unidentifiedSkipped: watchMode ? unidentifiedSkipped : null,
  maxResults,
  maxResultsReached: pushed >= maxResults,
  chargeLimitReached,
  seedCap: watchMode && seeding ? SEED_CAP : null,
  seedCapHit: watchMode && seeding ? seedCapHit : null,
  complete,
  incompleteReason,
  incompleteDetail,
  runError,
  watchLabel: watchMode ? watchLabel : null,
  watchSeeding: watchMode ? seeding : null,
  baselineSaved: watchMode ? !skipBaselineSave : null,
  baselineSize: watchMode ? watchSeen.size : null,
  // >0 means the baseline lost ids to the WATCH_KEEP cap and a future run will re-deliver and
  // re-charge them as "new" (h285). null outside watch mode, where there is no baseline.
  baselineTruncated: watchMode ? baselineTruncated : null,
  baselineTruncatedTotal: watchMode ? baselineTruncatedTotal : null,
  skippedSeen: watchMode && !seeding ? watchSkipped : null,
};
await Actor.setValue('RUN_SUMMARY', runSummary);

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
    // >0 means the baseline lost ids to the WATCH_KEEP cap and a future run will re-deliver and
    // re-charge them as "new" (h285). null outside watch mode, where there is no baseline.
    baselineTruncated: watchMode ? baselineTruncated : null,
    baselineTruncatedTotal: watchMode ? baselineTruncatedTotal : null,
    // Same object as the RUN_SUMMARY key-value record, so a webhook consumer and a console/API
    // consumer read the identical completeness facts.
    summary: runSummary,
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

// The failure signal itself is unchanged — the run still ends FAILED. It just happens here, after
// the baseline, RUN_SUMMARY and webhook have been persisted, instead of where Actor.fail's
// immediate exit would have skipped all three.
if (runError) await Actor.fail(runError);

await Actor.exit();
