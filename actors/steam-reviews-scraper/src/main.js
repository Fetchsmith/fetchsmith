import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';
import { createHash } from 'node:crypto';

await Actor.init();
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
let sortBy = ['recent', 'updated', 'all'].includes(input.sortBy) ? input.sortBy : 'recent';
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
let watchMode = watchLabel.length > 0;
if (watchMode && dataType === 'games') {
  log.warning(`watchLabel "${watchLabel}" is ignored in dataType:"games" — watch mode only applies to dataType:"reviews" (a game row is a snapshot of the same game on every run, not a stream of new events).`);
  watchMode = false;
}
const WATCH_STORE = 'fetchsmith-steam-reviews-watch';
const SEED_CAP = 20000;   // bound the cost/time of a baseline run across all apps
const WATCH_KEEP = 40000; // bound the record size; oldest ids fall off first

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
  if (sortBy === 'all') {
    log.warning(
      'Watch mode with sortBy="all": that is Steam\'s most-helpful ordering, not a chronological one, so a '
      + `brand-new review is not necessarily inside the ${perAppReviews} review(s) scanned per app and can be `
      + 'missed. Use sortBy="recent" for reliable alerting.',
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
    seededApps: Array.from(seededApps),
    seenIds: ids,
  });
}

let pushed = 0;
let keepGoing = true;
const isPPE = Actor.getChargingManager().getPricingInfo().isPayPerEvent;
async function pushResult(item, watchId = null, appSeeding = false) {
  if (watchMode && watchId != null && appSeeding) {
    watchSeen.add(watchId); // baseline run (or a newly-appeared app): record, never deliver, never charge
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

function gameRow(appId, d, summary, players) {
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

async function getPlayerCount(appId) {
  try {
    const r = await getJson(`https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid=${appId}`);
    return r?.response?.result === 1 ? r.response.player_count ?? null : null;
  } catch (e) { log.debug(`player count failed for ${appId}: ${e.message}`); return null; }
}

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
  if (dayRange && sortBy === 'all') p.set('day_range', String(dayRange));
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
if (dataType === 'games') {
  for (const id of ids) {
    if (!keepGoing) break;
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
    keepGoing = await pushResult({ ...gameRow(id, d, summary, players), scrapedAt: new Date().toISOString() });
  }
} else {
  for (const id of ids) {
    if (!keepGoing) break;
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

log.info(`Done. Pushed ${pushed} ${dataType === 'games' ? 'games' : 'reviews'}.${unidentifiedSkipped ? ` Skipped ${unidentifiedSkipped} review(s) with no reviewId (cannot be tracked in watch mode, not charged).` : ''}`);
// An upstream fault that produced nothing is a failed run, not an empty one: surfacing it as a
// success would tell the user their games have no reviews, which is the opposite of the truth.
if (pushed === 0 && upstreamDegraded.length) {
  await Actor.fail(
    `Steam's review API returned incomplete responses (success, but no reviews and no review totals) `
    + `for: ${upstreamDegraded.join(', ')} — after 2 retries each. This is an upstream Steam fault, `
    + `not a problem with your input; please re-run later.`,
  );
}
// The watch record is written only AFTER the upstream-fault check above, and never when that check
// fails the run: a baseline that recorded "app seeded, 0 reviews" during a degenerate Steam window
// would deliver — and charge for — that app's entire back catalogue on the next run.
if (watchMode) await saveWatchRecord(seeding ? 'seeded' : 'incremental');

// A watch status message still has to carry the upstream-fault notice when only SOME apps were
// degraded (a fully-degraded run already failed above) — those apps were not baselined and their
// reviews were never scanned, so "nothing new" would be a misleading thing to leave unqualified.
const baselinedSuffix = baselinedInPlace.length
  ? ` Newly-watched app(s) ${baselinedInPlace.join(', ')} were baselined this run instead of having their whole review history delivered — you will get their new reviews from the next run on.`
  : '';
const degradedSuffix = upstreamDegraded.length
  ? ` Steam's review API returned incomplete responses for: ${upstreamDegraded.join(', ')} — an upstream fault, not your input; those apps were skipped, re-run them later.`
  : '';
if (watchMode && seeding) {
  await Actor.setStatusMessage(`Baseline run for watch label "${watchLabel}": ${watchSeen.size} existing review(s) across ${seededApps.size} app(s) recorded, 0 rows returned, 0 charged. Run it again later to get only what's new.${degradedSuffix}`);
} else if (watchMode && pushed === 0) {
  await Actor.setStatusMessage(`Nothing new for watch label "${watchLabel}" since its last run — all ${watchSkipped} matching review(s) had already been delivered. That is the expected result most of the time; you were charged for nothing.${baselinedSuffix}${degradedSuffix}`);
} else if (watchMode && saturatedApps.length) {
  await Actor.setStatusMessage(`Pushed ${pushed} new review(s) for watch label "${watchLabel}". Every matching review in the scanned window was new for: ${saturatedApps.join(', ')} — older new reviews may have been missed; raise maxReviewsPerApp or run the watch more often.${baselinedSuffix}${degradedSuffix}`);
} else if (watchMode) {
  await Actor.setStatusMessage(`Watch label "${watchLabel}": ${pushed} new review(s) since the last run (${watchSkipped} already-delivered review(s) skipped, not charged).${baselinedSuffix}${degradedSuffix}`);
} else if (pushed === 0) {
  const why = emptyIds.length
    ? `Steam returned nothing for: ${emptyIds.join(', ')} (language "${language}", country "${country}")`
    : emptySearches.length
      ? `your search terms matched no Steam games: ${emptySearches.join(', ')}`
      : depthCapped.length
        ? `maxReviewsPerApp (${perAppReviews}) was hit before any review passed your keyword/minPlaytimeHours filter for: ${depthCapped.join(', ')} — raise maxReviewsPerApp to search deeper`
        : keyword || minPlaytimeHours != null || hasDateWindow
          ? 'every review Steam returned was removed by your keyword / minimum-playtime / date-window filters'
          : 'no valid Steam App IDs could be parsed from your input';
  await Actor.setStatusMessage(`No results — ${why}. See the log for details.`);
} else if (upstreamDegraded.length) {
  // Partial success: other apps produced rows, so the run is not a failure, but the user still
  // needs to know these specific apps are missing for an upstream reason and are worth re-running.
  await Actor.setStatusMessage(`Pushed ${pushed} results. Steam's review API returned incomplete responses for: ${upstreamDegraded.join(', ')} — an upstream fault, not your input; re-run those later.`);
} else if (depthCapped.length) {
  await Actor.setStatusMessage(`Pushed ${pushed} results. maxReviewsPerApp (${perAppReviews}) was hit while filtering: ${depthCapped.join(', ')} — some matching reviews may sit deeper in the feed; raise maxReviewsPerApp to search further.`);
} else if (emptyIds.length) {
  await Actor.setStatusMessage(`Pushed ${pushed} results. Steam returned nothing for: ${emptyIds.join(', ')}.`);
}
await Actor.exit();
