import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';

await Actor.init();
const input = (await Actor.getInput()) ?? {};
const apps = (input.apps ?? []).map(String).filter(Boolean);
const searchTerms = (input.searchTerms ?? []).map(String).filter(Boolean);
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
const minPlaytimeHours = input.minPlaytimeHours != null ? Number(input.minPlaytimeHours) : null;
const keyword = input.keyword ? String(input.keyword).toLowerCase() : null;

if (!apps.length && !searchTerms.length) {
  await Actor.fail('Provide at least one game in "apps" (Steam store URL or numeric App ID), or at least one query in "searchTerms".');
}

let pushed = 0;
let keepGoing = true;
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
    playtimeForeverHours: a.playtime_forever != null ? Math.round(a.playtime_forever / 6) / 10 : null,
    playtimeAtReviewHours: a.playtime_at_review != null ? Math.round(a.playtime_at_review / 6) / 10 : null,
    playtimeLastTwoWeeksHours: a.playtime_last_two_weeks != null ? Math.round(a.playtime_last_two_weeks / 6) / 10 : null,
    authorSteamId: a.steamid ?? null,
    authorName: a.personaname ?? null,
    authorProfileUrl: a.profile_url ?? null,
    authorNumGamesOwned: a.num_games_owned ?? null,
    authorNumReviews: a.num_reviews ?? null,
    reviewUrl: r.recommendationid ? `https://steamcommunity.com/profiles/${a.steamid}/recommended/${appId}/` : null,
    ...(info || {}),
  };
}

function reviewPassesFilters(item) {
  if (minPlaytimeHours != null && !(item.playtimeForeverHours >= minPlaytimeHours)) return false;
  if (keyword && !(item.review || '').toLowerCase().includes(keyword)) return false;
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
  let cursor = '*';
  let got = 0;
  const seen = new Set();
  for (let page = 0; page < 200 && got < perAppReviews && keepGoing; page++) {
    let body;
    try { body = await getJson(reviewsUrl(appId, cursor)); } // URLSearchParams below already encodes the cursor — do not encode it twice
    catch (e) { log.warning(`review page ${page + 1} failed for ${appId}: ${e.message}`); break; }
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
      if (!reviewPassesFilters(item)) continue;
      keepGoing = await pushResult(item);
    }
    if (pastWindow) break;
    const next = body.cursor;
    if (!next || next === cursor) break; // same cursor twice = end of feed
    cursor = next;
  }
  return got;
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
      const body = await getJson(`https://store.steampowered.com/appreviews/${id}?json=1&num_per_page=0&language=all&purchase_type=all`);
      summary = body?.query_summary ?? null;
    } catch (e) { log.debug(`review summary failed for ${id}: ${e.message}`); }
    const players = includePlayerCount ? await getPlayerCount(id) : null;
    keepGoing = await pushResult({ ...gameRow(id, d, summary, players), scrapedAt: new Date().toISOString() });
  }
} else {
  for (const id of ids) {
    if (!keepGoing) break;
    const before = pushed;
    const got = await scrapeReviews(id);
    log.info(`${id}: ${got} reviews fetched, ${pushed - before} kept after filters.`);
    if (got === 0) {
      emptyIds.push(id);
      const s = summaries.get(id);
      log.warning(s && s.total_reviews === 0
        ? `App ${id} has no Steam reviews at all yet (that is Steam's data, not a scrape failure).`
        : `Steam returned no reviews for app ${id} with language="${language}", review_type="${reviewType}", purchase_type="${purchaseType}" — try language "all" or a different filter.`);
    }
  }
}

log.info(`Done. Pushed ${pushed} ${dataType === 'games' ? 'games' : 'reviews'}.`);
if (pushed === 0) {
  const why = emptyIds.length
    ? `Steam returned nothing for: ${emptyIds.join(', ')} (language "${language}", country "${country}")`
    : emptySearches.length
      ? `your search terms matched no Steam games: ${emptySearches.join(', ')}`
      : keyword || minPlaytimeHours != null || hasDateWindow
        ? 'every review Steam returned was removed by your keyword / minimum-playtime / date-window filters'
        : 'no valid Steam App IDs could be parsed from your input';
  await Actor.setStatusMessage(`No results — ${why}. See the log for details.`);
} else if (emptyIds.length) {
  await Actor.setStatusMessage(`Pushed ${pushed} results. Steam returned nothing for: ${emptyIds.join(', ')}.`);
}
await Actor.exit();
