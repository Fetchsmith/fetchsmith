import { createHash } from 'node:crypto';
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
if (minScore != null && maxScore != null && minScore > maxScore) {
  throw new Error(`"minScore" (${minScore}) is greater than "maxScore" (${maxScore}) — no review can ever match. Swap them.`);
}
const keyword = String(input.keyword ?? '').normalize('NFC').trim().toLowerCase() || null;
const keywords = (input.keywords ?? []).map((s) => String(s).normalize('NFC').trim().toLowerCase()).filter(Boolean);
const ratingFilter = (input.ratingFilter ?? [])
  .map((s) => Number(String(s).trim()))
  .filter((n) => Number.isFinite(n));
const appVersions = (input.appVersions ?? []).map((s) => String(s).trim()).filter(Boolean);
const sinceDate = input.sinceDate ? new Date(input.sinceDate) : null;
const untilDate = input.untilDate ? new Date(input.untilDate) : null;
const watchLabel = String(input.watchLabel ?? '').trim();

function passesFilters(r) {
  if (minScore != null && r.score < minScore) return false;
  if (maxScore != null && r.score > maxScore) return false;
  if (ratingFilter.length && !ratingFilter.includes(Number(r.score))) return false;
  const hay = `${r.title || ''} ${r.text || ''}`.normalize('NFC').toLowerCase();
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

// Watch mode: a stateful "only reviews posted since my last run" filter, as opposed to a plain
// run which re-delivers (and re-charges for) the same top-of-feed reviews every time. The
// baseline (reviewIds already delivered under this label + filter set) lives in a NAMED
// key-value store on the buyer's own account so it survives across runs -- the default KV store
// is per-run and would reset every time.
const WATCH_STORE = 'fetchsmith-google-play-reviews-watch';
const SEED_CAP = 5000; // bound the cost/time of a baseline run across all apps
const SEED_MIN_PER_APP = 1000; // baseline walks deeper than the buyer's fetch cap (see below)
const WATCH_KEEP = 20000; // bound the record size; oldest ids fall off first

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
const watchSeen = new Set(); // reviewIds already delivered under this label+fingerprint
const seededApps = new Set(); // appIds whose existing reviews are already in the baseline
let appSeeding = false; // set per app in the main loop: this app is being baselined, not delivered

if (watchMode) {
  // EVERY filter that decides what gets delivered goes into the fingerprint, including the
  // client-side ones (score/keyword/version/date) -- they are applied in passesFilters() after
  // fetching, so a baseline built under a narrow filter must not be reused when the buyer widens
  // it, or the newly-matching older reviews would be silently treated as "already delivered".
  // Raw input values are fingerprinted, not resolved ones: none of these default to a rolling
  // value today, and raw is what the buyer actually typed.
  const criteria = {
    appIds: input.appIds ?? [], searchTerms: input.searchTerms ?? [], country, lang, sort: sortName,
    minScore, maxScore, ratingFilter, keyword, keywords, appVersions,
    sinceDate: input.sinceDate ?? null, untilDate: input.untilDate ?? null,
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
      + `${watchSeen.size} already-delivered review(s) across ${seededApps.size} app(s). Only reviews NOT in that `
      + 'baseline will be returned and charged.',
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
  if (sortName !== 'NEWEST') {
    log.warning(
      `Watch mode with sort="${sortName}": a brand-new review is not necessarily inside the first `
      + `${maxReviewsPerApp} rows of a ${sortName}-sorted feed, so new reviews can be missed. Use sort="NEWEST" `
      + 'for alerting.',
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

const cm = Actor.getChargingManager();
const isPPE = cm.getPricingInfo().isPayPerEvent;
let pushed = 0;
let stop = false;

// watchId is the review's stable id; app-detail records pass null and are handled by the
// caller (they are deferred in watch mode, see the main loop).
async function pushResult(item, watchId = null) {
  if (watchMode && watchId != null && appSeeding) {
    watchSeen.add(String(watchId));
    if (watchSeen.size >= SEED_CAP) stop = true;
    return !stop;
  }
  if (watchMode && watchId != null && watchSeen.has(String(watchId))) {
    watchSkipped += 1;
    return true; // already delivered under this label: not pushed, not charged, keep scanning
  }
  if (isPPE) {
    const r = await Actor.charge({ eventName: 'result', count: 1 });
    if (r.chargedCount === 0) return false;
    await Actor.pushData(item);
    pushed += 1;
    if (watchMode && watchId != null) watchSeen.add(String(watchId));
    if (r.eventChargeLimitReached || pushed >= maxResults) stop = true;
    return !stop;
  }
  await Actor.pushData(item);
  pushed += 1;
  if (watchMode && watchId != null) watchSeen.add(String(watchId));
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
    // Google Play shows these as per-aspect thumbs on the review itself (e.g. "Ads frequency: 2/5") --
    // present on a real, non-trivial share of reviews (~30% sampled live on a major app), and not
    // exposed by any of the 3 Store leaders checked cycle 303 (none list it in their dataset schema).
    aspectRatings: (r.criterias ?? []).map((c) => ({ criteria: c.criteria, rating: c.rating })),
    url: r.url,
  };
}

const resolvedAppIds = await resolveAppIds();
if (!resolvedAppIds.length) {
  log.warning('No appIds resolved (empty appIds and searchTerms, or all searches failed). Nothing to do.');
}

const emptyApps = []; // Google Play returned zero reviews (wrong country/lang, or genuinely no reviews)
const filteredOutApps = []; // reviews existed but rating/keyword/appVersion/date filters removed all of them
// Apps where maxReviewsPerApp was hit (gplay.reviews() returned exactly that many) while the
// rating/keyword/appVersion/date filters were still dropping some of them -- maxReviewsPerApp
// caps reviews FETCHED, before filtering, so matching reviews may sit further back in Google
// Play's feed and were never fetched at all.
const depthCappedApps = [];
const erroredApps = [];
const invalidApps = []; // app() confirmed the appId doesn't exist -- not a country/language issue
const seenReviewIds = new Set();
let duplicatesSkipped = 0;
let unidentifiedSkipped = 0; // watch mode only: reviews Google Play returned without an id
const saturatedApps = []; // watch mode: every fetched review was new, so older new ones may be out of reach
for (const appId of resolvedAppIds) {
  if (stop) break;
  // An app that is not in the baseline yet is baselined on this run instead of delivered, even
  // on an otherwise incremental run. This only happens when a 'searchTerms' lookup resolves to a
  // different app than last time (editing 'appIds' changes the fingerprint, which starts a whole
  // new baseline) -- without this, that drift would dump the new app's entire back catalogue of
  // reviews as "new" and charge for all of it.
  appSeeding = watchMode && (seeding || !seededApps.has(appId));
  if (watchMode && !seeding && appSeeding) {
    log.info(`${appId}: not in the baseline for "${watchLabel}" yet (search term resolved to a new app) — baselining it this run instead of delivering its existing reviews.`);
  }
  let appIdInvalid = false;
  // In watch mode the app-detail record is held back and pushed only if this app turns out to
  // have at least one new review: an app snapshot is not a discrete new event, and charging for
  // one on every scheduled run would defeat the "nothing new costs nothing" promise.
  let pendingAppRecord = null;
  if (includeAppDetails) {
    try {
      const app = await gplay.app({ appId, lang, country });
      if (watchMode) {
        if (!appSeeding) pendingAppRecord = mapAppDetails(app);
      } else {
        const keepGoing = await pushResult(mapAppDetails(app));
        if (!keepGoing) break;
      }
    } catch (e) {
      // app() throws on an unknown package name; reviews() does not -- it just returns zero
      // rows for the same id, which would otherwise read as "wrong country/language" below.
      appIdInvalid = /not found/i.test(e.message);
      if (appIdInvalid) invalidApps.push(appId);
      log.warning(`app() failed for ${appId}: ${e.message}`);
    }
  }
  if (stop) break;
  // maxReviewsPerApp is an honest FETCH-DEPTH cap (it counts rows fetched, before filtering) and
  // is left exactly as the buyer set it on incremental runs -- with sort=NEWEST the new reviews
  // are at the head of the feed, so depth does not hide them. A BASELINE run is different: it
  // must record what already exists at least as deep as any later run can reach, or those older
  // reviews come back as "new" later, so it walks its own, deeper cap.
  const fetchNum = appSeeding ? Math.min(Math.max(maxReviewsPerApp, SEED_MIN_PER_APP), 5000) : maxReviewsPerApp;
  try {
    const { data } = await gplay.reviews({ appId, lang, country, sort, num: fetchNum });
    const passCount = data.filter(passesFilters).length;
    let newForApp = 0;
    log.info(`${appId}: fetched ${data.length} reviews, ${passCount} pass filters`);
    if (data.length === fetchNum && passCount < data.length) {
      depthCappedApps.push(appId);
      log.warning(
        `${appId}: maxReviewsPerApp (${fetchNum}) was reached and ${data.length - passCount} of the `
        + `fetched reviews were removed by your rating/keyword/appVersion/date filters. The cap counts reviews `
        + `fetched, before filtering -- raise maxReviewsPerApp to search deeper in the feed.`,
      );
    }
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
      if (watchMode && r.id == null) {
        // No stable id means it can be neither recorded in the baseline nor recognised next run,
        // so delivering it would re-charge for the same row on every scheduled run.
        unidentifiedSkipped += 1;
        continue;
      }
      if (watchMode && !appSeeding && watchSeen.has(String(r.id))) {
        // Counted as skipped inside pushResult; short-circuit here so the app record is not
        // pushed for an app whose reviews are all old.
        watchSkipped += 1;
        continue;
      }
      if (pendingAppRecord) {
        const keepGoingApp = await pushResult(pendingAppRecord);
        pendingAppRecord = null;
        if (!keepGoingApp) break;
      }
      const keepGoing = await pushResult(mapReview(appId, r), watchMode ? r.id : null);
      if (!appSeeding) newForApp += 1;
      if (!keepGoing) break;
    }
    // Only record the app as baselined if its walk actually finished -- a walk cut short by the
    // global SEED_CAP has an incomplete picture of what already exists for that app.
    if (appSeeding && !stop) seededApps.add(String(appId));
    // Watch mode: if the whole fetch window was new, reviews older than the window may also be
    // new since the last run and will never be seen again once they fall further back.
    if (watchMode && !appSeeding && data.length === fetchNum && passCount > 0 && newForApp === passCount) {
      saturatedApps.push(appId);
      log.warning(
        `${appId}: all ${passCount} matching reviews in the fetched window of ${fetchNum} were new, so reviews `
        + 'posted before that window may have been missed. Raise maxReviewsPerApp or run the watch more often.',
      );
    }
    if (data.length === 0 && !appIdInvalid) {
      emptyApps.push(appId);
      log.warning(`${appId}: Google Play returned zero reviews for country="${country}" lang="${lang}" (try a different country/language, not a scrape failure).`);
    } else if (data.length > 0 && passCount === 0) {
      filteredOutApps.push(appId);
      log.warning(`${appId}: fetched ${data.length} reviews but your rating/keyword/appVersion/date filters removed all of them.`);
    }
  } catch (e) {
    erroredApps.push(appId);
    log.warning(`reviews() failed for ${appId}: ${e.message}`);
  }
}

if (watchMode) {
  await saveWatchRecord(seeding ? 'seeded' : 'incremental');
  if (seeding) {
    log.info(
      `Baseline saved for watch label "${watchLabel}": ${watchSeen.size} existing review(s) across `
      + `${seededApps.size} app(s) recorded as already-delivered, 0 rows pushed, 0 charged. Run this Actor again `
      + 'on the same label and filters to get only the reviews posted since now.'
      + (watchSeen.size >= SEED_CAP
        ? ` NOTE: the baseline hit the ${SEED_CAP}-review cap. Narrow the filters or watch fewer apps per label, `
          + 'or the reviews beyond the cap will be reported as new later.'
        : ''),
    );
  } else {
    log.info(
      `Watch label "${watchLabel}": ${pushed} new item(s) since the last run (${watchSkipped} already-delivered `
      + `review(s) skipped, not charged); baseline now holds ${watchSeen.size} review(s) across ${seededApps.size} app(s).`,
    );
  }
}

log.info(`Done. Pushed ${pushed} items.${duplicatesSkipped ? ` Skipped ${duplicatesSkipped} duplicate review(s) (not charged).` : ''}${unidentifiedSkipped ? ` Skipped ${unidentifiedSkipped} review(s) with no reviewId (cannot be tracked in watch mode, not charged).` : ''}`);
if (watchMode && seeding) {
  await Actor.setStatusMessage(`Baseline run for watch label "${watchLabel}": ${watchSeen.size} existing review(s) across ${seededApps.size} app(s) recorded, 0 rows returned, 0 charged. Run it again later to get only what's new.`);
} else if (watchMode && pushed === 0) {
  await Actor.setStatusMessage(`Nothing new for watch label "${watchLabel}" since its last run — all ${watchSkipped} matching review(s) had already been delivered. That is the expected result most of the time; you were charged for nothing.`);
} else if (watchMode && saturatedApps.length) {
  await Actor.setStatusMessage(`Pushed ${pushed} new item(s) for watch label "${watchLabel}". Every matching review inside the fetched window was new for: ${saturatedApps.join(', ')} — older new reviews may have been missed; raise maxReviewsPerApp or run more often.`);
} else if (pushed === 0 && resolvedAppIds.length) {
  const why = invalidApps.length
    ? `these appIds don't exist on Google Play: ${invalidApps.join(', ')} (check the package name in the Play Store URL's "?id=" param)`
    : erroredApps.length
    ? `fetching reviews failed for: ${erroredApps.join(', ')} (see log for the error)`
    : depthCappedApps.length && !emptyApps.length
      ? `maxReviewsPerApp (${maxReviewsPerApp}) was reached before any fetched review passed your rating/keyword/appVersion/date filters for: ${depthCappedApps.join(', ')} — raise maxReviewsPerApp to search deeper`
    : filteredOutApps.length && !emptyApps.length
      ? 'reviews were found but every one was removed by your rating/keyword/appVersion/date filters'
      : `Google Play returned zero reviews for: ${emptyApps.join(', ')} (try a different "country"/"language")`;
  await Actor.setStatusMessage(`No reviews returned — ${why}. See the log for details.`);
} else if (depthCappedApps.length) {
  await Actor.setStatusMessage(`Pushed ${pushed} items. maxReviewsPerApp (${maxReviewsPerApp}) was reached while filtering: ${depthCappedApps.join(', ')} — some matching reviews may sit deeper in the feed; raise maxReviewsPerApp to search further.`);
} else if (emptyApps.length || filteredOutApps.length) {
  await Actor.setStatusMessage(`Pushed ${pushed} items. Zero reviews for: ${emptyApps.join(', ') || 'none'}${filteredOutApps.length ? `; filtered out entirely for: ${filteredOutApps.join(', ')}` : ''}.`);
}
await Actor.exit();
