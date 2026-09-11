import { Actor, log } from 'apify';
import gplay from 'google-play-scraper';

await Actor.init();
const input = (await Actor.getInput()) ?? {};

// Accept either a bare package name or a full Play Store URL -- users paste the URL far more
// often than the package name, and both top competitors take a URL.
function toAppId(raw) {
  const s = String(raw).trim();
  if (!s) return null;
  if (!/^https?:\/\//i.test(s)) return s;
  try {
    const u = new URL(s);
    const id = u.searchParams.get('id');
    if (id) return id.trim();
    log.warning(`Play Store URL has no "?id=" param, skipping: ${s}`);
  } catch {
    log.warning(`Not a valid URL or package name, skipping: ${s}`);
  }
  return null;
}

const appIds = (input.appIds ?? []).map(toAppId).filter(Boolean);
const searchTerms = (input.searchTerms ?? []).map((s) => String(s).trim()).filter(Boolean);
const country = String(input.country ?? 'us').toLowerCase();
const lang = String(input.language ?? 'en').toLowerCase();
const sortName = String(input.sort ?? 'NEWEST').toUpperCase();
const sort = gplay.sort[sortName] ?? gplay.sort.NEWEST;
const maxReviewsPerApp = Math.min(Number(input.maxReviewsPerApp ?? 100), 5000);
const includeAppDetails = input.includeAppDetails !== false;
const maxResults = Math.min(Number(input.maxResults ?? 500), 20000);
const minScore = input.minScore != null ? Number(input.minScore) : null;
const maxScore = input.maxScore != null ? Number(input.maxScore) : null;
const keyword = input.keyword ? String(input.keyword).toLowerCase() : null;
const keywords = (input.keywords ?? []).map((s) => String(s).trim().toLowerCase()).filter(Boolean);
const ratingFilter = (input.ratingFilter ?? [])
  .map((s) => Number(String(s).trim()))
  .filter((n) => Number.isFinite(n));
const appVersions = (input.appVersions ?? []).map((s) => String(s).trim()).filter(Boolean);
const sinceDate = input.sinceDate ? new Date(input.sinceDate) : null;
const untilDate = input.untilDate ? new Date(input.untilDate) : null;

function passesFilters(r) {
  if (minScore != null && r.score < minScore) return false;
  if (maxScore != null && r.score > maxScore) return false;
  if (ratingFilter.length && !ratingFilter.includes(Number(r.score))) return false;
  const hay = `${r.title || ''} ${r.text || ''}`.toLowerCase();
  if (keyword && !hay.includes(keyword)) return false;
  if (keywords.length && !keywords.some((k) => hay.includes(k))) return false;
  // Google Play leaves `version` null on many reviews; a version filter must drop those
  // rather than silently letting them through as "unknown".
  if (appVersions.length && !appVersions.includes(String(r.version ?? ''))) return false;
  const d = r.date ? new Date(r.date) : null;
  if (sinceDate && (!d || d < sinceDate)) return false;
  if (untilDate && (!d || d > untilDate)) return false;
  return true;
}

const cm = Actor.getChargingManager();
const isPPE = cm.getPricingInfo().isPayPerEvent;
let pushed = 0;
let stop = false;

async function pushResult(item) {
  if (isPPE) {
    const r = await Actor.charge({ eventName: 'result', count: 1 });
    if (r.chargedCount === 0) return false;
    await Actor.pushData(item);
    pushed += 1;
    if (r.eventChargeLimitReached || pushed >= maxResults) stop = true;
    return !stop;
  }
  await Actor.pushData(item);
  pushed += 1;
  if (pushed >= maxResults) stop = true;
  return !stop;
}

async function resolveAppIds() {
  const resolved = [...appIds];
  for (const term of searchTerms) {
    try {
      const results = await gplay.search({ term, num: 1, lang, country });
      if (results.length) {
        log.info(`Search "${term}" -> ${results[0].appId}`);
        resolved.push(results[0].appId);
      } else {
        log.warning(`No app found for search term "${term}"`);
      }
    } catch (e) {
      log.warning(`Search failed for "${term}": ${e.message}`);
    }
  }
  return [...new Set(resolved)];
}

function mapAppDetails(app) {
  return {
    recordType: 'app',
    appId: app.appId,
    title: app.title,
    developer: app.developer,
    developerId: app.developerId,
    summary: app.summary,
    description: app.description,
    score: app.score,
    ratings: app.ratings,
    reviewsCount: app.reviews,
    histogram: app.histogram,
    installs: app.installs,
    minInstalls: app.minInstalls,
    price: app.price,
    free: app.free,
    currency: app.currency,
    androidVersionText: app.androidVersionText,
    genre: app.genre,
    genreId: app.genreId,
    contentRating: app.contentRating,
    released: app.released,
    updated: app.updated ? new Date(app.updated).toISOString() : null,
    version: app.version,
    url: app.url,
  };
}

function mapReview(appId, r) {
  return {
    recordType: 'review',
    appId,
    reviewId: r.id,
    userName: r.userName,
    reviewerProfileImageUrl: r.userImage || null,
    score: r.score,
    title: r.title || null,
    text: r.text,
    date: r.date,
    language: lang,
    thumbsUp: r.thumbsUp,
    version: r.version || null,
    replyText: r.replyText || null,
    replyDate: r.replyDate || null,
    url: r.url,
  };
}

const resolvedAppIds = await resolveAppIds();
if (!resolvedAppIds.length) {
  log.warning('No appIds resolved (empty appIds and searchTerms, or all searches failed). Nothing to do.');
}

const emptyApps = []; // Google Play returned zero reviews (wrong country/lang, or genuinely no reviews)
const filteredOutApps = []; // reviews existed but rating/keyword/appVersion/date filters removed all of them
const erroredApps = [];
const invalidApps = []; // app() confirmed the appId doesn't exist -- not a country/language issue
const seenReviewIds = new Set();
let duplicatesSkipped = 0;
for (const appId of resolvedAppIds) {
  if (stop) break;
  let appIdInvalid = false;
  if (includeAppDetails) {
    try {
      const app = await gplay.app({ appId, lang, country });
      const keepGoing = await pushResult(mapAppDetails(app));
      if (!keepGoing) break;
    } catch (e) {
      // app() throws on an unknown package name; reviews() does not -- it just returns zero
      // rows for the same id, which would otherwise read as "wrong country/language" below.
      appIdInvalid = /not found/i.test(e.message);
      if (appIdInvalid) invalidApps.push(appId);
      log.warning(`app() failed for ${appId}: ${e.message}`);
    }
  }
  if (stop) break;
  const pushedBefore = pushed;
  try {
    const { data } = await gplay.reviews({ appId, lang, country, sort, num: maxReviewsPerApp });
    log.info(`${appId}: fetched ${data.length} reviews, ${data.filter(passesFilters).length} pass filters`);
    for (const r of data) {
      if (!passesFilters(r)) continue;
      // Never push (and under pay-per-result, never charge for) the same reviewId twice --
      // Google Play's paginated review endpoint can repeat a row across page boundaries.
      // (Duplicate *apps* are already collapsed in resolveAppIds().)
      if (r.id != null && seenReviewIds.has(r.id)) {
        duplicatesSkipped += 1;
        continue;
      }
      if (r.id != null) seenReviewIds.add(r.id);
      const keepGoing = await pushResult(mapReview(appId, r));
      if (!keepGoing) break;
    }
    if (data.length === 0 && !appIdInvalid) {
      emptyApps.push(appId);
      log.warning(`${appId}: Google Play returned zero reviews for country="${country}" lang="${lang}" (try a different country/language, not a scrape failure).`);
    } else if (data.length > 0 && pushed === pushedBefore) {
      filteredOutApps.push(appId);
      log.warning(`${appId}: fetched ${data.length} reviews but your rating/keyword/appVersion/date filters removed all of them.`);
    }
  } catch (e) {
    erroredApps.push(appId);
    log.warning(`reviews() failed for ${appId}: ${e.message}`);
  }
}

log.info(`Done. Pushed ${pushed} items.${duplicatesSkipped ? ` Skipped ${duplicatesSkipped} duplicate review(s) (not charged).` : ''}`);
if (pushed === 0 && resolvedAppIds.length) {
  const why = invalidApps.length
    ? `these appIds don't exist on Google Play: ${invalidApps.join(', ')} (check the package name in the Play Store URL's "?id=" param)`
    : erroredApps.length
    ? `fetching reviews failed for: ${erroredApps.join(', ')} (see log for the error)`
    : filteredOutApps.length && !emptyApps.length
      ? 'reviews were found but every one was removed by your rating/keyword/appVersion/date filters'
      : `Google Play returned zero reviews for: ${emptyApps.join(', ')} (try a different "country"/"language")`;
  await Actor.setStatusMessage(`No reviews returned — ${why}. See the log for details.`);
} else if (emptyApps.length || filteredOutApps.length) {
  await Actor.setStatusMessage(`Pushed ${pushed} items. Zero reviews for: ${emptyApps.join(', ') || 'none'}${filteredOutApps.length ? `; filtered out entirely for: ${filteredOutApps.join(', ')}` : ''}.`);
}
await Actor.exit();
