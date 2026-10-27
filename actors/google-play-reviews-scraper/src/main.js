import { createHash } from 'node:crypto';
import { Actor, log } from 'apify';
import gplay from 'google-play-scraper';
import { gotScraping } from 'got-scraping';

await Actor.init();
// appIds/searchTerms carry no length cap, and each entry costs 1-2 sequential network calls
// (gplay.search() per term, then gplay.app()+gplay.reviews() per app) -- a large list is the same
// compounding-latency shape as the other reviews-scrapers' timeout bug: getting hard-killed
// mid-walk returns nothing even though rows already pushed sit in the dataset, and no status
// message or truncation note is ever written. Stop proactively with a safety margin and report
// what was collected instead (pattern mirrored from google-news/hacker-news/app-store-reviews-scraper).
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

let appIds = (input.appIds ?? []).map(toAppId).filter(Boolean);
const searchTerms = (input.searchTerms ?? []).map((s) => String(s).trim()).filter(Boolean);
// "appIds" used to carry a schema-level "default": ["com.spotify.music"] so Apify's automated
// Store quality test (a bare `{}` API call) had real output to check. But Apify silently merges a
// schema default into ANY run that omits the field, including a searchTerms-only API call, mixing
// an uninvited Spotify review batch into billed results with no warning (same bug class fixed on
// apple-podcasts-scraper/google-news-scraper/steam-reviews-scraper, cycle 893). Fix: no schema
// default; replicate it here instead, but only when the caller supplied NEITHER seed field at all
// (true `{}` omission, not an explicit "appIds": []), so a searchTerms-only call is never polluted.
if (input.appIds === undefined && input.searchTerms === undefined) {
  appIds = ['com.spotify.music'];
  log.info('No "appIds" or "searchTerms" given: running the example app so this call returns real output.');
}
const country = String(input.country ?? 'us').toLowerCase();
const lang = String(input.language ?? 'en').toLowerCase();
const sortName = String(input.sort ?? 'NEWEST').toUpperCase();
const sort = gplay.sort[sortName] ?? gplay.sort.NEWEST;
const maxReviewsPerApp = Math.min(Number(input.maxReviewsPerApp ?? 100), 5000);
const includeAppDetails = input.includeAppDetails !== false;
// Structural app-category filter. Google Play gives every app a genre pair on its details record
// -- a display name ("Strategy", "Education") and a stable id ("GAME_STRATEGY", "EDUCATION",
// verified live 2026-09-28) -- so this is a real field on the source, not a guess from the title.
// Accepted forms are the id, the display name, or the family shorthand "GAME" (every GAME_* id),
// all case-insensitive; a value that matches nothing simply keeps every app out, which is the
// fail-CLOSED direction (you are never charged for rows a mistyped genre let through).
const genres = (input.genres ?? []).map((s) => String(s).trim()).filter(Boolean);
const genresWanted = new Set(genres.map((s) => s.toUpperCase().replace(/[\s&]+/g, '_')));
const genreFamilyWanted = new Set([...genresWanted].filter((g) => !g.includes('_')));
function genreAllowed(app) {
  if (!genresWanted.size) return true;
  const id = String(app?.genreId ?? '').toUpperCase();
  const name = String(app?.genre ?? '').toUpperCase().replace(/[\s&]+/g, '_');
  if (genresWanted.has(id) || genresWanted.has(name)) return true;
  // "GAME" matches GAME_STRATEGY/GAME_CASUAL/...; Play has no bare "GAME" id on an app record.
  return [...genreFamilyWanted].some((fam) => id.startsWith(`${fam}_`));
}
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
const minThumbsUp = input.minThumbsUp != null ? Number(input.minThumbsUp) : null;
const replyFilter = String(input.replyFilter ?? 'any').trim();
const minReviewLength = input.minReviewLength != null ? Number(input.minReviewLength) : null;
// Both date bounds are schema type `string` with no `pattern`, so Apify's input validation hands
// "last week" or "06/01/2026" through untouched. `new Date(junk)` is an *Invalid Date*, which is
// TRUTHY, so the `sinceDate && ...` guards in keep() below still pass while every comparison
// against it is false (NaN semantics) — the bound is silently defeated for every review that HAS
// a date, and the `!d` branch then drops every undated one. A typo therefore both widens the
// filter and hides rows, and this Actor is PPE: the buyer is charged per result for the widened
// set. `editor: datepicker` only protects Console users; API callers (the volume path) are not
// covered. Throw instead — the same widen-and-bill class substack-scraper's parseDateBound and
// uk-find-a-tender-scraper's parseBound already guard, and which both name `sinceDate` here as
// the exemplar. Validity-based rather than a YYYY-MM-DD regex on purpose: the schema documents
// the wider "ISO 8601" contract, so `2026-01-01T12:00:00Z` must keep working.
function parseDateBound(raw, fieldName) {
  const s = String(raw ?? '').trim();
  if (!s) return null;
  const d = new Date(s);
  if (Number.isNaN(d.getTime())) {
    throw new Error(`"${fieldName}" is not a parseable date (got ${JSON.stringify(raw)}). Use ISO 8601, e.g. "2026-01-01". An unparseable value here used to be ignored silently, matching every review regardless of this filter.`);
  }
  return d;
}
const sinceDate = parseDateBound(input.sinceDate, 'sinceDate');
const untilDate = parseDateBound(input.untilDate, 'untilDate');
// Symmetric with the minScore/maxScore guard above: an inverted window can never match a review,
// and without this it is an indistinguishable silent-zero-rows run.
if (sinceDate && untilDate && sinceDate > untilDate) {
  throw new Error(`"sinceDate" (${input.sinceDate}) is after "untilDate" (${input.untilDate}) — the window is empty, so no review can ever match. Swap them.`);
}
const watchLabel = String(input.watchLabel ?? '').trim();
// Watch-mode change events. "new" is the original behaviour (a review id never delivered under
// this label); the other three are MUTATIONS of an already-delivered review -- Google Play keeps
// the review id stable when a reviewer edits their own star rating and when a developer adds or
// deletes a reply, so an id-only baseline can never see either (see LEARNINGS cycle 844).
const WATCH_EVENTS = ['new', 'scoreChanged', 'developerReplied', 'replyRemoved'];
const watchEventsInput = (input.watchEvents ?? []).map((e) => String(e).trim()).filter(Boolean);
const unknownWatchEvents = watchEventsInput.filter((e) => !WATCH_EVENTS.includes(e));
if (unknownWatchEvents.length) log.warning(`Ignoring unknown watchEvents value(s): ${unknownWatchEvents.join(', ')}. Valid values: ${WATCH_EVENTS.join(', ')}.`);
const watchEvents = new Set(watchEventsInput.filter((e) => WATCH_EVENTS.includes(e)));
if (!watchEvents.size) for (const e of WATCH_EVENTS) watchEvents.add(e);
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

// RATING sort walks the feed highest-star-first, and maxReviewsPerApp caps reviews FETCHED (before
// any filter), so a rating filter that excludes 5★ spends the whole walk inside the 5★ block. On a
// high-volume app that block is far larger than the 5000-review schema maximum: verified 2026-09-25
// on com.spotify.music, sort=RATING + ratingFilter=[1,2] fetched all 5000 and kept 0. "Raise
// maxReviewsPerApp" — what the depth-cap warning otherwise advises — is therefore unreachable
// advice here, not a deeper walk away. The remedy is sort=NEWEST.
function ratingAllowed(score) {
  if (minScore != null && score < minScore) return false;
  if (maxScore != null && score > maxScore) return false;
  if (ratingFilter.length && !ratingFilter.includes(score)) return false;
  return true;
}
// Google Play only ever emits integer star ratings 1-5, so the reachable set is finite and the
// rating filters can be proven contradictory BEFORE a single review is fetched. Without this the
// run fetches its whole maxReviewsPerApp budget, keeps 0 rows, and then advises "raise
// maxReviewsPerApp to search deeper" -- unreachable advice, because no review at any depth can
// match (same class as clinicaltrials-scraper's resultsAvailability x resultsFirstPostedDate
// contradiction, LEARNINGS cycle 1028). Two ways in: an empty intersection between
// minScore/maxScore and ratingFilter (e.g. minScore 4 + ratingFilter [1,2]), or a ratingFilter
// holding only out-of-range values (the schema's stringList editor cannot constrain its items,
// so ratingFilter [0] / [6] arrives validated).
const STAR_RATINGS = [1, 2, 3, 4, 5];
const reachableStars = STAR_RATINGS.filter(ratingAllowed);
if (!reachableStars.length) {
  const parts = [];
  if (minScore != null) parts.push(`"minScore" (${minScore})`);
  if (maxScore != null) parts.push(`"maxScore" (${maxScore})`);
  if (ratingFilter.length) parts.push(`"ratingFilter" ([${ratingFilter.join(', ')}])`);
  const offRange = ratingFilter.filter((n) => !STAR_RATINGS.includes(n));
  throw new Error(
    `${parts.join(' + ')} ${parts.length > 1 ? 'leave' : 'leaves'} no reachable star rating — Google Play reviews only carry 1-5 stars, `
    + 'so no review can ever match this combination and every run would fetch its whole '
    + `maxReviewsPerApp budget and return 0 reviews.${
      offRange.length === ratingFilter.length && ratingFilter.length
        ? ` "ratingFilter" contains only values outside 1-5 (${offRange.join(', ')}); use whole star ratings.`
        : ' "ratingFilter" is applied ON TOP OF minScore/maxScore (an AND, not an override), so the two must overlap — drop one of them, or widen the range to include a value in the list.'
    }`,
  );
}

const topStarExcluded = !ratingAllowed(5);
const ratingSortUnreachable = sortName === 'RATING' && topStarExcluded;
const RATING_SORT_HINT = ' — with sort="RATING" the feed is walked highest-star-first, so the fetch '
  + 'cap fills with 5★ reviews before reaching lower ones; use sort="NEWEST" (the default) instead, '
  + 'as raising maxReviewsPerApp cannot help past its 5000 maximum';
if (ratingSortUnreachable) {
  log.warning(
    'sort="RATING" combined with a rating filter that excludes 5★ reviews: Google Play returns '
    + `RATING-sorted reviews highest-first, and maxReviewsPerApp (${maxReviewsPerApp}) counts reviews `
    + 'fetched BEFORE filtering, so this run will likely spend its whole fetch budget on 5★ reviews '
    + 'and return 0 rows. On a popular app even the 5000 maximum is not enough. Use sort="NEWEST" '
    + '(the default) to hunt for specific star ratings.',
  );
}

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
  if (minThumbsUp != null && Number(r.thumbsUp ?? 0) < minThumbsUp) return false;
  if (replyFilter === 'hasReply' && !r.replyText) return false;
  if (replyFilter === 'noReply' && r.replyText) return false;
  if (minReviewLength != null && String(r.text ?? '').length < minReviewLength) return false;
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
// A fixed UPPER date bound kills a watch dead (11th instance of this fleet class). With the
// default sort="NEWEST" (verified live 2026-10-12 on com.spotify.music: top-of-feed reviews
// dated within the last day), a brand-new review's own `date` IS its post time, so once the
// real calendar date passes a fixed `untilDate`, no newly-posted review can ever fall on or
// before that cutoff again -- the watch reports "nothing new" forever while still looking
// healthy. Gated on the schema's literal input name, not the parsed `untilDate` local, so the
// static check-change-blind checker can see the guard.
const watchDeadDateBound = watchMode && !!input.untilDate;
if (watchDeadDateBound) {
  log.warning(
    `watchLabel "${watchLabel}" is combined with a fixed untilDate (${input.untilDate}). `
    + 'Once the real calendar date passes that cutoff, no newly-posted review can ever be dated on or '
    + 'before it anymore, so this watch is now permanently unable to report anything new.',
  );
  log.warning(
    'Drop untilDate from a watched query (sinceDate alone is safe to keep), or remove '
    + 'watchLabel if you really do want a fixed historical window instead of an ongoing watch.',
  );
}
let watchStore = null;
let watchKey = null;
let watchRecord = null;
let seeding = false;
let watchSkipped = 0;
const watchSeen = new Set(); // reviewIds already delivered under this label+fingerprint
// reviewId -> the mutable state that review had when it was last delivered, encoded as one small
// int so the persisted record grows ~10% rather than doubling: score * 2 + (hasDeveloperReply ?
// 1 : 0), i.e. 2..11. 0 means "recorded before this feature existed" -> unknown, never fires an
// event. Kept as a parallel array aligned to seenIds on disk.
const watchMeta = new Map();
const META_UNKNOWN = 0;
function encodeMeta(r) {
  const s = Number(r.score);
  if (!Number.isInteger(s) || s < 1 || s > 5) return META_UNKNOWN;
  return s * 2 + (r.replyText ? 1 : 0);
}
function decodeMeta(code) {
  const c = Number(code);
  if (!Number.isInteger(c) || c < 2 || c > 11) return null;
  return { score: Math.floor(c / 2), hasReply: c % 2 === 1 };
}
let watchEventsFiltered = 0; // a real change the buyer's watchEvents list excluded
let watchChanged = 0; // already-delivered reviews re-delivered this run because they changed
// Genuinely new reviews delivered this run -- counted directly rather than derived as
// `pushed - watchChanged`, because `pushed` also includes the per-app app-detail snapshot
// (pendingAppRecord below) when includeAppDetails is set, and that snapshot is not a review at
// all. The derived form silently counted one phantom "new review" per app that had any
// delivery, inflating both the status message and the webhookUrl payload.
let watchNewDelivered = 0;
let baselineTruncated = 0; // reviewIds dropped by WATCH_KEEP this run -- they come back as "new" and get charged again
let baselineTruncatedTotal = 0; // same, cumulative over the life of this label
const seededApps = new Set(); // appIds whose existing reviews are already in the baseline
let appSeeding = false; // set per app in the main loop: this app is being baselined, not delivered

// Per-label lock against OVERLAPPING RUNS of the same watch label (h288, cycle 2325). The baseline
// below is read once at the top of a run and written once near the bottom, so two runs sharing a
// label+fingerprint both read the same `seenIds`, both decide the same reviews are new, and both
// charge for them -- a real cross-run double charge, distinct from the within-run dedupe gap.
// Kept as a SEPARATE KV record (`${key}__lock`) so a lock write can never corrupt or truncate the
// real baseline. Taken BEFORE the baseline getValue, so a blocked run exits having read nothing and
// charged nothing. This narrows the race from "the whole run's duration" to the few KV round-trips
// between the check and the write -- not true compare-and-swap (the Apify KV API exposes no
// If-Match to the SDK), but a 100-1000x tighter window is the realistic ceiling without platform
// support. This Actor has the simplest exit shape of the watch-enabled fleet: every validation
// throw happens ABOVE this point (before the store is even opened), every per-app scrape error is
// caught into `erroredApps` rather than ending the run, and there is no Actor.fail() anywhere -- so
// the baseline write has exactly ONE call site and the lock has exactly ONE release point, with no
// mid-run exit able to skip it. A run that throws somewhere truly uncaught (the KV write itself
// failing, say) still leaves the lock to expire via TTL rather than wedging the label forever --
// same scope and tradeoff as apple-podcasts-scraper's and trademark-search-scraper's fixes.
const WATCH_LOCK_TTL_MS = 2 * 60 * 60 * 1000;
let watchLockKey = null;
let watchLockHeld = false;

async function acquireWatchLock(store, storeKey, label) {
  watchLockKey = `${storeKey}__lock`;
  const existingLock = await store.getValue(watchLockKey);
  if (existingLock && typeof existingLock.lockedAt === 'string') {
    const age = Date.now() - new Date(existingLock.lockedAt).getTime();
    if (age >= 0 && age < WATCH_LOCK_TTL_MS) {
      await Actor.fail(
        `Watch label "${label}" is already being processed by another run (started ${existingLock.lockedAt}`
        + `${existingLock.runId ? `, run ${existingLock.runId}` : ''}). Running the same watch label concurrently `
        + 'would read the same baseline twice and charge you twice for the same new reviews, so this run stopped '
        + 'before reading or charging anything. Wait for the other run to finish and try again (a stuck lock from a '
        + `crashed run self-expires after ${Math.round(WATCH_LOCK_TTL_MS / 60000)} minutes).`,
      );
    }
  }
  await store.setValue(watchLockKey, { lockedAt: new Date().toISOString(), runId: Actor.getEnv().actorRunId ?? null });
  watchLockHeld = true;
}

async function releaseWatchLock(store) {
  if (watchLockHeld && watchLockKey) {
    await store.setValue(watchLockKey, null);
    watchLockHeld = false;
  }
}

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
    // Only added when set, so every watch baseline saved before this cycle keeps its key.
    ...(minThumbsUp != null ? { minThumbsUp } : {}),
    ...(replyFilter !== 'any' ? { replyFilter } : {}),
    ...(minReviewLength != null ? { minReviewLength } : {}),
    ...(genres.length ? { genres } : {}),
  };
  watchStore = await Actor.openKeyValueStore(WATCH_STORE);
  const { key, fingerprint } = watchKeyFor(watchLabel, criteria);
  watchKey = key;
  await acquireWatchLock(watchStore, key, watchLabel);
  const existing = await watchStore.getValue(key);
  if (existing && Array.isArray(existing.seenIds)) {
    watchRecord = existing;
    const meta = Array.isArray(existing.seenMeta) ? existing.seenMeta : [];
    existing.seenIds.forEach((id, i) => {
      watchSeen.add(String(id));
      // A record written before watchEvents existed has no seenMeta at all; a shorter-than-ids
      // array (should not happen, but a hand-edited or truncated record could) decodes the
      // missing tail as unknown rather than misaligning.
      watchMeta.set(String(id), decodeMeta(meta[i] ?? META_UNKNOWN));
    });
    const known = [...watchMeta.values()].filter(Boolean).length;
    if (known === 0 && watchSeen.size > 0) {
      log.info(
        `Watch baseline for "${watchLabel}" predates change detection, so it holds no star-rating/reply state: `
        + 'this run reports new reviews only and records that state, and scoreChanged/developerReplied/replyRemoved '
        + 'start working from the next run onwards.',
      );
    }
    for (const a of existing.seededApps ?? []) seededApps.add(String(a));
    log.info(
      `Watch mode "${watchLabel}" (${key}): baseline from ${existing.lastRunAt ?? 'an earlier run'} holds `
      + `${watchSeen.size} already-delivered review(s) across ${seededApps.size} app(s). Only reviews NOT in that `
      + `baseline, or already-delivered ones whose star rating or developer reply changed (events: ${[...watchEvents].join(', ')}), `
      + 'will be returned and charged.',
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
}
if (!watchMode && watchEventsInput.length) {
  log.warning('"watchEvents" only applies when "watchLabel" is set — this run is a normal one-off scrape and returns every matching review.');
}
if (watchMode) {
  if (!watchEvents.has('new')) {
    log.info('"new" is not in watchEvents: brand-new reviews will be recorded in the baseline but not returned or charged for.');
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
  baselineTruncated = watchSeen.size - ids.length;
  baselineTruncatedTotal = (watchRecord.truncatedTotal ?? 0) + baselineTruncated;
  if (baselineTruncated > 0) {
    log.warning(
      `The baseline for watch label "${watchLabel}" exceeded the ${WATCH_KEEP}-entry record cap; the `
      + `${baselineTruncated} oldest review id(s) were dropped (${baselineTruncatedTotal} dropped over the `
      + 'life of this label) and will be re-delivered and re-charged as "new" on a future run. Narrow the '
      + 'filters (rating/keyword/date, fewer apps per label) to keep the baseline under the cap.',
    );
  }
  await watchStore.setValue(watchKey, {
    ...watchRecord,
    label: watchLabel,
    lastRunAt: new Date().toISOString(),
    lastRunStatus: status,
    runCount: (watchRecord.runCount ?? 0) + 1,
    seenCount: ids.length,
    seededApps: Array.from(seededApps),
    seenIds: ids,
    // Parallel to seenIds, same order, same length: the star-rating/reply state each review had
    // when it was last delivered. Written even for ids carried over from a pre-watchEvents
    // record (as 0/unknown) so the two arrays never misalign.
    seenMeta: ids.map((id) => {
      const m = watchMeta.get(String(id));
      return m ? m.score * 2 + (m.hasReply ? 1 : 0) : META_UNKNOWN;
    }),
    truncatedLastRun: baselineTruncated,
    truncatedTotal: baselineTruncatedTotal,
  });
}

const cm = Actor.getChargingManager();
const isPPE = cm.getPricingInfo().isPayPerEvent;
let pushed = 0;
let stop = false;
// Why the run stopped early, if it did. `stop` abandons the REST OF THE APP LIST (see the main
// loop's `if (stop) break`), so a run that hits any of these delivers a dataset covering only the
// apps it got to -- which is indistinguishable from a complete run unless we say so. Tracked
// separately from `stop` because the three causes need different advice.
let chargeLimitHit = false; // the buyer's own pay-per-event charge limit was exhausted mid-run

// watchId is the review's stable id; app-detail records pass null and are handled by the
// caller (they are deferred in watch mode, see the main loop). metaCode is the encoded
// star-rating/reply state to record alongside the id so the NEXT run can diff against it; the
// caller has already decided (via watchVerdict) that this row is worth delivering, so the
// "already seen" short-circuit below only catches rows the caller did not classify.
async function pushResult(item, watchId = null, metaCode = META_UNKNOWN) {
  if (watchMode && watchId != null && appSeeding) {
    watchSeen.add(String(watchId));
    watchMeta.set(String(watchId), decodeMeta(metaCode));
    if (watchSeen.size >= SEED_CAP) stop = true;
    return !stop;
  }
  if (isPPE) {
    const r = await Actor.charge({ eventName: 'result', count: 1 });
    if (r.chargedCount === 0) return false;
    await Actor.pushData(item);
    pushed += 1;
    if (watchMode && watchId != null) { watchSeen.add(String(watchId)); watchMeta.set(String(watchId), decodeMeta(metaCode)); }
    if (r.eventChargeLimitReached) chargeLimitHit = true;
    if (r.eventChargeLimitReached || pushed >= maxResults) stop = true;
    return !stop;
  }
  await Actor.pushData(item);
  pushed += 1;
  if (watchMode && watchId != null) { watchSeen.add(String(watchId)); watchMeta.set(String(watchId), decodeMeta(metaCode)); }
  if (pushed >= maxResults) stop = true;
  return !stop;
}

async function resolveAppIds() {
  const resolved = [...appIds];
  // A plain search() result carries no genre field (verified live 2026-09-28: undefined on every
  // hit) -- only fullDetail:true does. With a "genres" filter set, taking just the top hit (num: 1)
  // meant a search term whose #1 result was the wrong genre yielded ZERO apps for that term, even
  // when its #2-#5 hits matched -- the filter was silently killing search terms instead of merely
  // narrowing them. When "genres" is set we instead pull the top 5 with fullDetail and keep the
  // first one that already passes genreAllowed(); if none of the 5 match, we fall back to the top
  // hit so the existing downstream genreSkippedApps/status-message reporting still explains why.
  for (const [i, term] of searchTerms.entries()) {
    if (!timeBudgetOk()) {
      log.warning(`Approaching the run timeout — skipping the remaining ${searchTerms.length - i} search-term lookup(s).`);
      break;
    }
    try {
      const results = genres.length
        ? await gplay.search({ term, num: 5, lang, country, fullDetail: true })
        : await gplay.search({ term, num: 1, lang, country });
      if (results.length) {
        const picked = genres.length ? (results.find((r) => genreAllowed(r)) ?? results[0]) : results[0];
        const matched = genres.length && genreAllowed(picked);
        log.info(`Search "${term}" -> ${picked.appId}${genres.length ? (matched ? ` (genre match: ${picked.genre})` : ' (no genre match in top 5, falling back to top hit; the "genres" filter will skip it downstream)') : ''}`);
        resolved.push(picked.appId);
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
const filteredOutApps = []; // reviews existed but rating/keyword/appVersion/thumbsUp/reply/length/date filters removed all of them
// Apps where maxReviewsPerApp was hit (gplay.reviews() returned exactly that many) while the
// rating/keyword/appVersion/thumbsUp/reply/length/date filters were still dropping some of them -- maxReviewsPerApp
// caps reviews FETCHED, before filtering, so matching reviews may sit further back in Google
// Play's feed and were never fetched at all.
const depthCappedApps = [];
const erroredApps = [];
const invalidApps = []; // app() confirmed the appId doesn't exist -- not a country/language issue
const genreSkippedApps = []; // the "genres" filter excluded the app before any review was fetched
const genreUnknownApps = []; // "genres" set but app() failed, so the app was skipped, not guessed
const seenReviewIds = new Set();
let duplicatesSkipped = 0;
let unidentifiedSkipped = 0; // watch mode only: reviews Google Play returned without an id
const saturatedApps = []; // watch mode: every fetched review was new, so older new ones may be out of reach
// Apps the loop actually got to. Everything in resolvedAppIds but NOT in here was abandoned by an
// early stop and contributed zero rows -- the silent-shortfall case the end-of-run note reports.
const appsAttempted = new Set();
for (const appId of resolvedAppIds) {
  if (stop) break;
  if (!timeBudgetOk()) { stop = true; log.warning(TIME_BUDGET_WARNING); break; }
  appsAttempted.add(String(appId));
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
  // A "genres" filter needs the app-details record even when the buyer did not ask for one in the
  // output: the genre only exists there, not on a review row.
  if (includeAppDetails || genresWanted.size) {
    try {
      const app = await gplay.app({ appId, lang, country });
      if (!genreAllowed(app)) {
        genreSkippedApps.push(`${appId} (${app.genreId ?? 'unknown'})`);
        log.info(`${appId}: genre "${app.genre}" (${app.genreId}) is not in your "genres" filter — skipping this app, no reviews fetched or charged.`);
        continue;
      }
      if (includeAppDetails) {
        if (watchMode) {
          if (!appSeeding) pendingAppRecord = mapAppDetails(app);
        } else {
          const keepGoing = await pushResult(mapAppDetails(app));
          if (!keepGoing) break;
        }
      }
    } catch (e) {
      // app() throws on an unknown package name; reviews() does not -- it just returns zero
      // rows for the same id, which would otherwise read as "wrong country/language" below.
      appIdInvalid = /not found/i.test(e.message);
      if (appIdInvalid) invalidApps.push(appId);
      log.warning(`app() failed for ${appId}: ${e.message}`);
      // With a "genres" filter set there is no genre to check against, so the app is skipped
      // rather than scraped: failing OPEN here would bill for exactly the rows the filter exists
      // to exclude.
      if (genresWanted.size) {
        genreUnknownApps.push(appId);
        log.warning(`${appId}: cannot read its genre, and a "genres" filter is set — skipping this app instead of scraping it unfiltered.`);
        continue;
      }
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
        + `fetched reviews were removed by your rating/keyword/appVersion/thumbsUp/reply/length/date filters. The cap counts reviews `
        + `fetched, before filtering${ratingSortUnreachable ? RATING_SORT_HINT : ' -- raise maxReviewsPerApp to search deeper in the feed'}.`,
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
      // Watch mode, incremental run: an id already in the baseline is not automatically "old".
      // Google Play keeps the review id stable when the reviewer edits their own star rating and
      // when the developer adds or deletes a reply, so diff the recorded state before skipping.
      let verdict = 'new';
      let previous = null;
      if (watchMode && !appSeeding && watchSeen.has(String(r.id))) {
        previous = watchMeta.get(String(r.id)) ?? null;
        const changes = [];
        if (previous) {
          if (previous.score !== Number(r.score)) changes.push('scoreChanged');
          if (!previous.hasReply && r.replyText) changes.push('developerReplied');
          if (previous.hasReply && !r.replyText) changes.push('replyRemoved');
        }
        const wanted = changes.filter((c) => watchEvents.has(c));
        if (!wanted.length) {
          // Counted as skipped inside pushResult; short-circuit here so the app record is not
          // pushed for an app whose reviews are all old. A real change the buyer's watchEvents
          // list excluded is tracked separately so it is not silently invisible in the log.
          if (changes.length) watchEventsFiltered += 1;
          watchSkipped += 1;
          // Record the new state anyway: an excluded change must not be re-reported later as a
          // change from the stale pre-change state.
          watchMeta.set(String(r.id), decodeMeta(encodeMeta(r)));
          continue;
        }
        // A score edit that also added a reply is one delivery, reported by its primary change
        // (the score), not two charges.
        verdict = wanted[0];
        watchChanged += 1;
      } else if (watchMode && !appSeeding && !watchEvents.has('new')) {
        // "new" deselected: record the review in the baseline so a later change can be detected,
        // but do not deliver or charge for it.
        watchSeen.add(String(r.id));
        watchMeta.set(String(r.id), decodeMeta(encodeMeta(r)));
        watchEventsFiltered += 1;
        watchSkipped += 1;
        continue;
      }
      if (pendingAppRecord) {
        const keepGoingApp = await pushResult(pendingAppRecord);
        pendingAppRecord = null;
        if (!keepGoingApp) break;
      }
      const row = mapReview(appId, r);
      if (watchMode && !appSeeding) {
        row.watchEvent = verdict;
        row.previousScore = previous ? previous.score : null;
        row.previousHasDeveloperReply = previous ? previous.hasReply : null;
      }
      const keepGoing = await pushResult(row, watchMode ? r.id : null, encodeMeta(r));
      if (!appSeeding) newForApp += 1;
      if (watchMode && !appSeeding && verdict === 'new') watchNewDelivered += 1;
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
      log.warning(`${appId}: fetched ${data.length} reviews but your rating/keyword/appVersion/thumbsUp/reply/length/date filters removed all of them.`);
    }
  } catch (e) {
    erroredApps.push(appId);
    log.warning(`reviews() failed for ${appId}: ${e.message}`);
  }
}

// WATCH_KEEP record-cap eviction (h285): empty unless something was actually dropped, so it
// never taints the common case where the baseline comfortably fits under the cap. Computed
// AFTER saveWatchRecord() below, which is what actually sets baselineTruncated.
let evictionSuffix = '';

if (watchMode) {
  await saveWatchRecord(seeding ? 'seeded' : 'incremental');
  evictionSuffix = baselineTruncated > 0
    ? ` WARNING: the watch baseline hit its ${WATCH_KEEP}-entry cap and ${baselineTruncated} oldest review `
      + `id(s) were dropped (${baselineTruncatedTotal} dropped over the life of this label) — they will be `
      + 're-delivered and re-charged as "new" on a future run. Narrow the filters to keep the baseline under the cap.'
    : '';
  if (seeding) {
    log.info(
      `Baseline saved for watch label "${watchLabel}": ${watchSeen.size} existing review(s) across `
      + `${seededApps.size} app(s) recorded as already-delivered, 0 rows pushed, 0 charged. Run this Actor again `
      + 'on the same label and filters to get only the reviews posted since now.'
      + (watchSeen.size >= SEED_CAP
        ? ` NOTE: the baseline hit the ${SEED_CAP}-review cap. Narrow the filters or watch fewer apps per label, `
          + 'or the reviews beyond the cap will be reported as new later.'
        : '') + evictionSuffix,
    );
  } else {
    log.info(
      `Watch label "${watchLabel}": ${pushed} item(s) since the last run — ${watchNewDelivered} new review(s) and `
      + `${watchChanged} already-delivered review(s) whose star rating or developer reply changed (${watchSkipped} `
      + `unchanged/already-delivered review(s) skipped, not charged`
      + `${watchEventsFiltered ? `, of which ${watchEventsFiltered} really did change but were excluded by your watchEvents list` : ''}); `
      + `baseline now holds ${watchSeen.size} review(s) across ${seededApps.size} app(s).`
      + evictionSuffix,
    );
  }
  // Released only after the baseline is durably written: releasing earlier would let a queued run
  // start from the OLD baseline and re-charge everything this run just delivered.
  await releaseWatchLock(watchStore);
}

log.info(`Done. Pushed ${pushed} items.${genreSkippedApps.length + genreUnknownApps.length ? ` Skipped ${genreSkippedApps.length + genreUnknownApps.length} app(s) on the "genres" filter (no reviews fetched or charged).` : ''}${duplicatesSkipped ? ` Skipped ${duplicatesSkipped} duplicate review(s) (not charged).` : ''}${unidentifiedSkipped ? ` Skipped ${unidentifiedSkipped} review(s) with no reviewId (cannot be tracked in watch mode, not charged).` : ''}`);

// An early stop silently truncates the APP LIST, not just the row count: apps after the stopping
// point were never fetched at all, and none of the per-app buckets below (emptyApps,
// filteredOutApps, depthCappedApps, erroredApps) know about them, so without this note the run
// reads as a complete one that simply found less. Appended to whatever status message applies.
const appsNotReached = resolvedAppIds.map(String).filter((a) => !appsAttempted.has(a));
let truncationNote = '';
if (stop) {
  const cause = timeBudgetExceeded
    ? 'the run was approaching the platform run timeout and stopped early to return what it had'
    : chargeLimitHit
    ? 'your pay-per-event charge limit was reached'
    : pushed >= maxResults
      ? `the maxResults cap (${maxResults}) was reached`
      : watchMode && seeding
        ? `the baseline cap (${SEED_CAP} reviews) was reached`
        : 'the run stopped early';
  // Only claim the app list was abandoned when it actually was. Hitting the cap on the very last
  // row of the last app is the common, harmless case (the default input does exactly that) and
  // must not be reported as missing apps we never looked at.
  truncationNote = ` MAY BE INCOMPLETE: ${cause}.`
    + (appsNotReached.length
      ? ` The run stopped before finishing the app list — ${appsNotReached.length} app(s) were never fetched and returned nothing: ${appsNotReached.join(', ')}.`
      : ' Every requested app was fetched, but the last one may have been cut short.')
    + (timeBudgetExceeded
      ? ' Narrow the input (fewer apps/search terms, or a lower "maxReviewsPerApp") so the run finishes inside the'
        + " platform run timeout, raise the Actor's run timeout, or run the remaining apps separately."
      : chargeLimitHit
      ? ' Raise the Actor\'s charge limit and re-run to get the rest.'
      : ` Raise "maxResults" (currently ${maxResults}) and re-run to get the rest.`);
  log.warning(truncationNote.trim());
}

let statusMsg;
if (watchMode && seeding) {
  statusMsg = (`Baseline run for watch label "${watchLabel}": ${watchSeen.size} existing review(s) across ${seededApps.size} app(s) recorded, 0 rows returned, 0 charged. Run it again later to get only what's new.`);
} else if (watchMode && pushed === 0) {
  statusMsg = (`Nothing new for watch label "${watchLabel}" since its last run — all ${watchSkipped} matching review(s) had already been delivered and none of them changed. That is the expected result most of the time; you were charged for nothing.${watchEventsFiltered ? ` (${watchEventsFiltered} review(s) did change but the event was excluded by your watchEvents list.)` : ''}`);
} else if (watchMode && saturatedApps.length) {
  statusMsg = (`Pushed ${pushed} item(s) (${watchChanged} of them changed re-deliveries) for watch label "${watchLabel}". Every matching review inside the fetched window was new for: ${saturatedApps.join(', ')} — older new reviews may have been missed; raise maxReviewsPerApp or run more often.`);
} else if (pushed === 0 && resolvedAppIds.length) {
  // Without this branch, timing out before any app was even queried fell into the final default
  // below with an empty emptyApps list, asserting "Google Play returned zero reviews for: " (blank)
  // -- a false claim about Google Play's data when the real cause is our own clock.
  let why;
  if (timeBudgetExceeded && appsAttempted.size === 0) {
    why = 'the run was approaching the platform run timeout and stopped before any app could be checked';
  } else if (genreSkippedApps.length + genreUnknownApps.length > 0
    && genreSkippedApps.length + genreUnknownApps.length >= appsAttempted.size) {
    // Checked before the per-app causes below: when the "genres" filter took every app out, no
    // review was ever fetched, so blaming any of those causes would point at an app list none of
    // this run's apps actually reached.
    why = `your "genres" filter (${genres.join(', ')}) excluded every app${genreSkippedApps.length ? `: ${genreSkippedApps.join(', ')}` : ''}${genreUnknownApps.length ? `; genre unreadable (skipped) for: ${genreUnknownApps.join(', ')}` : ''}`;
  } else {
    // Each of these is an INDEPENDENT per-app cause -- a multi-app run can have one app that
    // doesn't exist, another whose fetch errored, another that hit maxReviewsPerApp before any
    // passing review, and another with reviews that were simply all filtered out, all in the same
    // run. The old code picked the first true cause via an if/else-if chain (and fully suppressed
    // the depth-cap/filtered-out causes whenever ANY app came back with zero reviews at all), so a
    // buyer following the one remedy shown would still see 0 rows from every app it never named.
    // Live-reproduced ($0, local): com.spotify.music (hits the 5-review cap, 0 pass) +
    // com.adelyons.upright (1 review total, cap NOT hit, 0 pass) with a non-matching keyword --
    // old message named only spotify and said "raise maxReviewsPerApp", advice that cannot help
    // upright at all (it already returned every review it has).
    const depthCappedSet = new Set(depthCappedApps);
    const filteredOutOnlyApps = filteredOutApps.filter((a) => !depthCappedSet.has(a));
    const causes = [];
    if (invalidApps.length) causes.push(`these appIds don't exist on Google Play: ${invalidApps.join(', ')} (check the package name in the Play Store URL's "?id=" param)`);
    if (erroredApps.length) causes.push(`fetching reviews failed for: ${erroredApps.join(', ')} (see log for the error)`);
    if (depthCappedApps.length) causes.push(`maxReviewsPerApp (${maxReviewsPerApp}) was reached before any fetched review passed your rating/keyword/appVersion/thumbsUp/reply/length/date filters for: ${depthCappedApps.join(', ')}${ratingSortUnreachable ? RATING_SORT_HINT : ' — raise maxReviewsPerApp to search deeper'}`);
    if (filteredOutOnlyApps.length) causes.push(`reviews were found but every one was removed by your rating/keyword/appVersion/thumbsUp/reply/length/date filters for: ${filteredOutOnlyApps.join(', ')}`);
    if (emptyApps.length) causes.push(`Google Play returned zero reviews for: ${emptyApps.join(', ')} (try a different "country"/"language")`);
    why = causes.length ? causes.join('; ') : 'no reviews were charged (check the log for the reason)';
  }
  statusMsg = (`No reviews returned — ${why}. See the log for details.`);
} else {
  // Same cascade-hides-independent-cause shape as the pushed===0 branch above (fixed cycle 1559),
  // found live in THIS branch at cycle 1591: depthCappedApps/filteredOutApps+emptyApps/
  // genreSkippedApps+genreUnknownApps/erroredApps/invalidApps are each populated per-app,
  // independently, so a multi-app run that still pushed rows (from OTHER apps) could have two or
  // more of these simultaneously non-empty -- the old if/else-if chain reported only the first and
  // silently dropped the rest, and erroredApps/invalidApps were not named in any pushed>0 branch at
  // all, not even partially. Accumulate every applicable cause instead of picking one.
  const depthCappedSet = new Set(depthCappedApps);
  const filteredOutOnlyApps = filteredOutApps.filter((a) => !depthCappedSet.has(a));
  const causes = [];
  if (invalidApps.length) causes.push(`these appIds don't exist on Google Play: ${invalidApps.join(', ')} (check the package name in the Play Store URL's "?id=" param)`);
  if (erroredApps.length) causes.push(`fetching reviews failed for: ${erroredApps.join(', ')} (see log for the error)`);
  if (depthCappedApps.length) causes.push(`maxReviewsPerApp (${maxReviewsPerApp}) was reached while filtering: ${depthCappedApps.join(', ')} — some matching reviews may sit deeper in the feed${ratingSortUnreachable ? RATING_SORT_HINT : '; raise maxReviewsPerApp to search further'}`);
  if (filteredOutOnlyApps.length) causes.push(`reviews were found but every one was removed by your filters for: ${filteredOutOnlyApps.join(', ')}`);
  if (emptyApps.length) causes.push(`zero reviews for: ${emptyApps.join(', ')}`);
  if (genreSkippedApps.length || genreUnknownApps.length) causes.push(`your "genres" filter skipped ${genreSkippedApps.length + genreUnknownApps.length} app(s)${genreSkippedApps.length ? `: ${genreSkippedApps.join(', ')}` : ''}${genreUnknownApps.length ? `; genre unreadable (skipped) for: ${genreUnknownApps.join(', ')}` : ''}`);
  if (causes.length) {
    statusMsg = `Pushed ${pushed} items. ${causes.join('; ')}.`;
  } else if (truncationNote) {
    // A clean run that nothing else had to report, EXCEPT that it stopped early -- previously this
    // was the case that set no status message at all and read as a complete run.
    statusMsg = `Pushed ${pushed} items.`;
  } else if (watchMode && baselineTruncated > 0) {
    // Same gap, other cause: an otherwise-clean delivering watch run whose baseline just lost ids
    // to the record cap had no status message at all, so the re-charge risk stayed invisible.
    statusMsg = `Pushed ${pushed} new item(s) for watch label "${watchLabel}".`;
  }
}
if (statusMsg) await Actor.setStatusMessage((statusMsg + truncationNote + evictionSuffix).slice(0, 1000));

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
    watchNewCount: watchMode && !seeding ? watchNewDelivered : null,
    watchSkipped: watchMode ? watchSkipped : null,
    watchChangedCount: watchMode && !seeding ? watchChanged : null,
    watchSeeding: watchMode ? seeding : null,
    baselineTruncated: watchMode ? baselineTruncated : null,
    baselineTruncatedTotal: watchMode ? baselineTruncatedTotal : null,
    // true means this watch is pinned to a fixed untilDate and can no longer report anything
    // new once today passes it — a "nothing new" result from such a run is meaningless.
    watchDeadDateBound: watchMode ? watchDeadDateBound : null,
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
