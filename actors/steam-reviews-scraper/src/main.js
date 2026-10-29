import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';
import { createHash } from 'node:crypto';
import { reviewsPageUrl, homeContentUrl, parseReviewsPage } from './reviews_html.js';

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
let apps = (input.apps ?? []).map((a) => String(a).trim()).filter(Boolean);
const searchTerms = (input.searchTerms ?? []).map((t) => String(t).trim()).filter(Boolean);
// Cycle 893 removed the schema-level "default" on "apps" because Apify silently merges it into ANY
// run that omits the field, including a searchTerms-only API call -- polluting billed results with
// an uninvited example game. But Apify's own automated Store quality test calls with a literal `{}`
// body and expects real, non-empty output (see PLAYBOOK.md step 3/4c). Replicate the default here
// instead, but only when the caller supplied NEITHER seed field at all (true `{}` omission, not an
// explicit "apps": []), so a searchTerms-only call is never polluted.
if (input.apps === undefined && input.searchTerms === undefined) {
  apps = ['https://store.steampowered.com/app/1145360/Hades/'];
  log.info('No "apps" or "searchTerms" given: running the example game so this call returns real output.');
}
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
// Gated on dataType:"reviews": sortBy/reviewsAfter/reviewsBefore have no effect at all in
// dataType:"games" (a game row is a store snapshot, not an ordered review list), so forcing
// sortBy to "recent" there would (a) print a confusing warning about an irrelevant date/sort
// interaction and (b) silently erase the buyer's non-default sortBy before the ignoredInGames
// check below ever sees it -- "recent" IS that check's default, so a forced-but-unflagged value
// vanishes from disclosure instead of being named. Found live this cycle: dataType:"games" +
// sortBy:"funny" + reviewsAfter together printed the ignoredInGames list WITHOUT sortBy in it,
// while sortBy:"funny" alone (no date window) correctly named it.
if (dataType === 'reviews' && hasDateWindow && sortBy !== 'recent') {
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
// dayRange had a real HTML path while this Actor used the JSON appreviews API (day_range only
// applied in the most-helpful ordering). Valve retired that API 2026-10-22; the
// steamcommunity.com HTML fallback this Actor now scrapes has no day-range control at all —
// not even in its "most helpful" (toprated) view — so this is now an unconditional no-op,
// not merely conditional on sortBy. Say so once, up front.
// Every input this run accepted but could not act on, as bare field names. The per-warning message
// lists below stay as they are (each is prose aimed at one cause); this is the machine-readable
// aggregate, because a `log.warning` is invisible to a pipeline and to a buyer who reads only the
// run's status message. Collected by `.push()` at each warning site rather than as one literal
// because the sites are spread across the input-parsing block AND the dataType:"games" branch.
const ignoredInputs = [];
if (dayRange && dataType === 'reviews') {
  ignoredInputs.push('dayRange');
  log.warning(
    `"Last N days" (${dayRange}) is ignored — Steam's review HTML page has no day-range control `
    + '(the JSON API this Actor used to call had one, but Valve retired that API 2026-10-22 and the '
    + 'replacement HTML source has no equivalent). Use "Reviews after/before" with sortBy="recent" for a date window instead.',
  );
}
const includeOwnerEstimates = input.includeOwnerEstimates === true;
// Both fields are read only inside the dataType:"games" path below (getPlayerCount/SteamSpy calls) —
// neither has any effect on a review row, so a reviews run that sets either gets charged for rows
// and no signal that the field did nothing. Build the ignored-name list from the already-quoted
// identifiers (not bare prose) so it stays interpolated if a third game-only field joins this group.
const gameOnlyIgnored = dataType !== 'games'
  ? [includePlayerCount && 'includePlayerCount', includeOwnerEstimates && 'includeOwnerEstimates'].filter(Boolean)
  : [];
if (gameOnlyIgnored.length) {
  ignoredInputs.push(...gameOnlyIgnored);
  const plural = gameOnlyIgnored.length > 1;
  log.warning(
    `${gameOnlyIgnored.join(' and ')} ${plural ? 'are' : 'is'} ignored for dataType:"reviews" — `
    + `${plural ? 'these describe' : 'it describes'} a game, not a review. Set dataType:"games" to get them.`,
  );
}
// Valve flags "off-topic review bomb" periods (a controversy, not the game). The dead JSON API's
// review endpoint excluded them by default (filter_offtopic_activity=1) and this input asked for
// the unfiltered set instead — exactly what a buyer studying a backlash wants. Verified
// 2026-09-17 on Total War: ROME II (214950): 88,334 reviews filtered vs 94,228 unfiltered.
const includeOffTopic = input.includeOffTopic === true;
const minPlaytimeHours = input.minPlaytimeHours != null ? Number(input.minPlaytimeHours) : null;
const keyword = String(input.keyword ?? '').normalize('NFC').trim().toLowerCase() || null;

// Valve retired the appreviews JSON API on 2026-10-22 (verified live; see reviews_html.js). Two
// of this Actor's filters have no equivalent anywhere on the steamcommunity.com HTML replacement
// (searched the full rendered page, not just the visible menus, confirmed c2126/c2129): purchase
// type (steam vs non-steam) — dataType:"reviews" only, dataType:"games" already gets its own more
// specific warning below — and the off-topic-activity toggle, which both modes used to honor via
// the dead API's filter_offtopic_activity param and is now an unconditional no-op in either one.
if (dataType === 'reviews' && purchaseType !== 'all') {
  ignoredInputs.push('purchaseType');
  log.warning(`purchaseType ("${purchaseType}") is ignored — Steam's review HTML page has no purchase-type filter (the retired JSON API's steam-vs-non-steam facet has no UI equivalent to port). Every review for the app is scanned regardless.`);
}
if (includeOffTopic) {
  ignoredInputs.push('includeOffTopic');
  log.warning('includeOffTopic is ignored — Steam\'s review HTML page has no off-topic-activity control at all (the retired JSON API\'s default — review-bomb periods excluded — has no UI toggle to port). Every review for the app is scanned regardless.');
}

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
  ignoredInputs.push('watchLabel');
  log.warning(`watchLabel "${watchLabel}" is ignored in dataType:"games" — watch mode only applies to dataType:"reviews" (a game row is a snapshot of the same game on every run, not a stream of new events).`);
  watchMode = false;
}
// A fixed reviewsBefore caps the watch's own match set at a date that gets more stale every day
// the schedule runs. reviewPassesFilters and reviewsUrl's end_date both filter on item.createdAt
// (the review's own post timestamp, never revised after the fact — Steam's "updated" timestamp is
// a separate field this filter does not read), and a brand-new review's createdAt is always "now".
// So once today's real calendar date passes a fixed reviewsBefore, no newly-posted review can ever
// satisfy the filter again, and the watch (identity-based: seenIds/watchSeen, no snapshotOf) goes
// permanently quiet while still returning the reassuring "nothing new" status message every run —
// same class as app-store-reviews-scraper's reviewsBefore, grants-gov's postedTo, eu-ted's
// publicationDateTo.
const watchDeadDateBound = watchMode && !!input.reviewsBefore;
if (watchDeadDateBound) {
  log.warning(
    `watchLabel "${watchLabel}" is combined with a fixed reviewsBefore (${input.reviewsBefore}). `
    + 'Once the real calendar date passes that cutoff, no newly-posted review can ever be dated on or before '
    + 'it anymore, so this watch is now permanently unable to report anything new.',
  );
  log.warning(
    'Drop reviewsBefore from a watched query (reviewsAfter alone is safe to keep), or remove '
    + 'watchLabel if you really do want a fixed historical window instead of an ongoing watch.',
  );
}
// dataType:"games" returns one store snapshot per game; none of the review-selection inputs reach
// that path. The Actor already warns in exactly this situation for includeOwnerEstimates (the
// mirror-image case) and watchLabel, so staying silent about the rest is an inconsistency a buyer
// pays for: "games matching negative reviews that mention grind" is a plausible reading of
// dataType:"games" + reviewType + keyword, and the run answers it with an unfiltered game row and
// no signal at all. language/purchaseType are called out separately because they are not merely
// unused here -- the summary call deliberately overrides both to "all" so reviewScore/totalReviews
// are the game's own totals, which is the opposite of what a buyer who set them expects.
if (dataType === 'games') {
  // Compared against the INPUT SCHEMA DEFAULT, not tested for presence: Apify materializes every
  // schema default into the input object before the Actor reads it, so `input.sortBy != null` is
  // true on every run and a presence check would warn about untouched fields forever (verified
  // live this cycle -- a bare games run warned about sortBy "recent" and maxReviewsPerApp 200).
  // Built as one array literal (not `.push()`), matching gameOnlyIgnored above, so every quoted
  // name sits in the declaration itself rather than arriving via a later mutation. Each entry is
  // [bare field name, prose]: the prose carries the buyer's own value so they recognise which
  // setting is meant, the bare name feeds the machine-readable `ignoredInputs` aggregate. Keeping
  // both in one literal is what stops the two lists drifting apart when a field joins this group.
  const ignoredInGamesPairs = [
    keyword && ['keyword', `keyword ("${keyword}")`],
    minPlaytimeHours != null && ['minPlaytimeHours', `minPlaytimeHours (${minPlaytimeHours})`],
    reviewType !== 'all' && ['reviewType', `reviewType ("${reviewType}")`],
    hasDateWindow && ['reviewsAfter/reviewsBefore', 'reviewsAfter/reviewsBefore'],
    sortBy !== 'recent' && ['sortBy', `sortBy ("${sortBy}")`],
    dayRange && ['dayRange', `dayRange (${dayRange})`],
    perAppReviews !== 200 && ['maxReviewsPerApp', `"maxReviewsPerApp" (${perAppReviews})`],
  ].filter(Boolean);
  const ignoredInGames = ignoredInGamesPairs.map(([, prose]) => prose);
  if (ignoredInGames.length) {
    ignoredInputs.push(...ignoredInGamesPairs.map(([name]) => name));
    log.warning(
      `These review filters are ignored in dataType:"games" — ${ignoredInGames.join(', ')}. A game row is a `
      + 'store snapshot, not a set of reviews, so there is nothing for them to select. Set dataType:"reviews" '
      + 'to filter individual reviews.',
    );
  }
  // Same schema-default rule as above: "english" is the default, so warning whenever language is
  // merely present would fire on every games run. Only a moved-off-default value is news.
  const languageSet = language !== 'english' && language !== 'all';
  if (purchaseType !== 'all' || languageSet) {
    const overridden = [];
    if (purchaseType !== 'all') overridden.push(`purchaseType ("${purchaseType}")`);
    if (languageSet) overridden.push(`language ("${language}")`);
    log.warning(
      `In dataType:"games", ${overridden.join(' and ')} ${overridden.length > 1 ? 'do' : 'does'} not narrow `
      + 'reviewScore/reviewScoreDesc/totalReviews: those are deliberately the game\'s own all-language, '
      + 'all-purchase-type totals so the row describes the game rather than a slice of it. Use '
      + 'dataType:"reviews" if you need a filtered review set.',
    );
  }
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

// Steam keeps a review's recommendationid stable when its author edits it in place — verified live
// 2026-09-26 by sampling real reviews on app 570 where timestamp_updated != timestamp_created
// (e.g. recommendationid 181644785, created and later edited, same id both times). Editing a review
// is exactly how a player flips their own thumbs-up/thumbs-down, so a returning id is not
// necessarily old — same subset-of-filterable-fields gap already fixed on shopify-products-scraper
// (h843), google-play-reviews-scraper (h844) and app-store-reviews-scraper (h845). Steam's reviews
// have no developer-response concept at all (unlike Google Play), so only a recommendation flip is
// worth watching here. Empty = both events, mirroring the rest of the fleet's watchEvents convention.
const WATCH_EVENTS = ['new', 'recommendationChanged'];
const watchEventsInput = (input.watchEvents ?? []).map((e) => String(e).trim()).filter(Boolean);
const unknownWatchEvents = watchEventsInput.filter((e) => !WATCH_EVENTS.includes(e));
if (unknownWatchEvents.length) log.warning(`Ignoring unknown watchEvents value(s): ${unknownWatchEvents.join(', ')}. Valid values: ${WATCH_EVENTS.join(', ')}.`);
const watchEvents = new Set(watchEventsInput.filter((e) => WATCH_EVENTS.includes(e)));
if (!watchEvents.size) for (const e of WATCH_EVENTS) watchEvents.add(e);

let watchStore = null;
let watchKey = null;
let watchRecord = null;
let seeding = false;
let watchSkipped = 0;
let watchChanged = 0; // already-delivered reviews re-delivered this run because voted_up flipped
let watchEventsFiltered = 0; // a real recommendation change (or a brand-new review) excluded by watchEvents
let unidentifiedSkipped = 0; // watch mode only: reviews Steam returned without a recommendationid
const watchSeen = new Set();  // `${appId}:${reviewId}` already delivered under this label+fingerprint
// watchId -> `recommended` (voted_up) the review had when last delivered, or null if unknown (a
// record written before this feature existed). Parallel to seenIds on disk, same order/length.
const watchMeta = new Map();
const META_UNKNOWN = 0;
function encodeMeta(recommended) {
  if (recommended === true) return 1;
  if (recommended === false) return 2;
  return META_UNKNOWN;
}
function decodeMeta(code) {
  if (code === 1) return true;
  if (code === 2) return false;
  return null;
}
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
    const meta = Array.isArray(existing.seenMeta) ? existing.seenMeta : [];
    existing.seenIds.forEach((id, i) => {
      watchSeen.add(String(id));
      // A record written before watchEvents existed has no seenMeta at all; a shorter-than-ids
      // array decodes the missing tail as unknown rather than misaligning ids with the wrong flags.
      watchMeta.set(String(id), decodeMeta(meta[i] ?? META_UNKNOWN));
    });
    for (const a of existing.seededApps ?? []) seededApps.add(String(a));
    const known = [...watchMeta.values()].filter((v) => v != null).length;
    if (known === 0 && watchSeen.size > 0) {
      log.info(
        `Watch baseline for "${watchLabel}" predates change detection, so it holds no recommendation state: `
        + 'this run reports new reviews only and records that state; recommendationChanged starts working '
        + 'from the next run onwards.',
      );
    }
    log.info(
      `Watch mode "${watchLabel}" (${key}): baseline from ${existing.lastRunAt ?? 'an earlier run'} holds `
      + `${watchSeen.size} already-delivered review(s) across ${seededApps.size} app(s). Only reviews NOT in `
      + `that baseline, or already-delivered ones whose thumbs-up/thumbs-down flipped (events: ${[...watchEvents].join(', ')}), `
      + 'will be returned and charged.',
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
  if (!watchEvents.has('new')) {
    log.info('"new" is not in watchEvents: brand-new reviews will be recorded in the baseline but not returned or charged for.');
  }
}
if (!watchMode && watchEventsInput.length) {
  log.warning('"watchEvents" only applies when "watchLabel" is set — this run is a normal one-off scrape and returns every matching review.');
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
    // Parallel to seenIds, same order/length: `recommended` each review had when last delivered.
    // Written even for ids carried over from a pre-watchEvents record (as 0/unknown) so the two
    // arrays never misalign.
    seenMeta: ids.map((id) => encodeMeta(watchMeta.get(String(id)))),
  });
}

let pushed = 0;
let keepGoing = true;
let chargeLimitReached = false; // Actor.charge()'s own per-event charge limit, not maxResults (h250)
let seedCapHit = false;         // watch seeding stopped at SEED_CAP before the whole match set was recorded
const isPPE = Actor.getChargingManager().getPricingInfo().isPayPerEvent;
// Charges and pushes with no "already delivered" guard — used both by pushResult (a genuinely new
// id, never seen before) and directly by the recommendationChanged branch above (an id that IS
// already in watchSeen on purpose, because it's a real change on an already-delivered review).
async function chargeAndPush(item, watchId = null, metaCode = META_UNKNOWN) {
  if (isPPE) {
    const r = await Actor.charge({ eventName: 'result', count: 1 });
    if (r.chargedCount === 0) return false; // user's budget exhausted: never push unpaid items
    await Actor.pushData(item); pushed += 1;
    if (watchMode && watchId != null) { watchSeen.add(watchId); watchMeta.set(watchId, decodeMeta(metaCode)); }
    if (r.eventChargeLimitReached) chargeLimitReached = true;
    return !r.eventChargeLimitReached && pushed < maxResults;
  }
  await Actor.pushData(item); pushed += 1; // non-PPE run (e.g. developer test): no charging
  if (watchMode && watchId != null) { watchSeen.add(watchId); watchMeta.set(watchId, decodeMeta(metaCode)); }
  return pushed < maxResults;
}
async function pushResult(item, watchId = null, appSeeding = false, metaCode = META_UNKNOWN) {
  if (watchMode && watchId != null && appSeeding) {
    watchSeen.add(watchId); // baseline run (or a newly-appeared app): record, never deliver, never charge
    watchMeta.set(watchId, decodeMeta(metaCode));
    if (watchSeen.size >= SEED_CAP) { keepGoing = false; seedCapHit = true; }
    return keepGoing;
  }
  if (watchMode && watchId != null && watchSeen.has(watchId)) {
    watchSkipped += 1;
    return true; // already delivered under this label: not pushed, not charged, keep scanning
  }
  return chargeAndPush(item, watchId, metaCode);
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
// Same transport as getJson, but for the steamcommunity.com HTML pages (reviews_html.js) — the
// body is markup, not JSON, so it must NOT go through JSON.parse.
const getHtml = async (url, opts = {}) => {
  const resp = await requestWithRetry(url, opts);
  const host = new URL(url).hostname;
  if (resp.statusCode >= 400) {
    const hint = resp.statusCode === 429
      ? ` ${host} is rate-limiting this run; wait a few minutes, or lower "maxResults"/the number of apps per run.`
      : (resp.statusCode >= 500 ? ` ${host} is having a server-side problem; this is usually temporary.` : '');
    throw new Error(`${host} returned HTTP ${resp.statusCode}.${hint}`);
  }
  return resp.body;
};
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// appreviewhistogram is aggregate-only (no review text/author/playtime — confirmed c2124) but it
// is NOT part of the retired appreviews API and is still live, so it is repurposed here as the
// review-total source both the games-mode summary and the reviews-mode degenerate check used to
// get from query_summary on the dead API's first page. Sums every weekly rollup's up/down counts;
// `weeks` (the current partial week) is included alongside `rollups` (completed weeks) since Steam
// splits them into two separate arrays rather than one.
const histogramCache = new Map();
async function getReviewTotals(appId) {
  if (histogramCache.has(appId)) return histogramCache.get(appId);
  let totals = null;
  try {
    const body = await getJson(`https://store.steampowered.com/appreviewhistogram/${appId}?l=english`);
    if (body?.success === 1) {
      const buckets = [...(body.results?.rollups ?? []), ...(body.results?.weeks ?? [])];
      const totalPositive = buckets.reduce((s, b) => s + (b.recommendations_up || 0), 0);
      const totalNegative = buckets.reduce((s, b) => s + (b.recommendations_down || 0), 0);
      totals = { totalReviews: totalPositive + totalNegative, totalPositive, totalNegative };
    }
  } catch (e) { log.debug(`review histogram failed for ${appId}: ${e.message}`); }
  histogramCache.set(appId, totals);
  return totals;
}

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

// sortBy=recent is the only chronological ordering (forced above whenever a date window is set),
// and reviewsAfter/reviewsBefore are enforced client-side against each row's parsed createdAt —
// the dead JSON API's server-side start_date/end_date/date_range_type=include is gone, so this is
// no longer a source-side filter and date resolution is now DAY, not exact-timestamp (see
// reviews_html.js's parsePostedDate). The pastWindow early-stop below still holds because
// recommendationid is strictly decreasing under sort=recent across pages (verified c2128).

async function scrapeReviews(appId) {
  const info = await getGameInfo(appId);
  // An app absent from the baseline is seeded in place rather than having its whole back
  // catalogue delivered as "new" — this covers a searchTerms query resolving to a different game
  // than last run, which changes the watched target set without changing the fingerprint.
  const appSeeding = watchMode && (seeding || !seededApps.has(String(appId)));
  if (watchMode && !seeding && appSeeding) {
    log.info(`App ${appId}: not in the baseline for "${watchLabel}" yet — baselining it this run instead of delivering its existing reviews.`);
  }
  let got = 0;
  let filteredOut = 0;
  let newForApp = 0;
  const seen = new Set();
  let degenerate = false;
  let next = null; // homecontent's replayed form fields for page 2+; unused on page 0
  // numperpage is 10 here, not the dead API's 100 — a given maxReviewsPerApp now costs ~10x the
  // page fetches, so the page-count ceiling scales with it instead of a flat 200.
  const maxPages = Math.max(30, Math.ceil(perAppReviews / 10) + 5);
  for (let page = 0; page < maxPages && got < perAppReviews && keepGoing; page++) {
    if (!timeBudgetOk()) { keepGoing = false; log.warning(TIME_BUDGET_WARNING); break; }
    let html;
    try {
      html = await getHtml(page === 0
        ? reviewsPageUrl(appId, { reviewType, sortBy, language })
        : homeContentUrl(appId, next));
    } catch (e) { log.warning(`review page ${page + 1} failed for ${appId}: ${e.message}`); break; }
    const parsed = parseReviewsPage(html, appId);
    if (page === 0 && parsed.cardCount === 0) {
      // Unlike the dead JSON API, the HTML page has no query_summary to distinguish "really no
      // reviews" from an upstream glitch on its own — 0 cards looks identical either way. The
      // still-live aggregate histogram disambiguates: a nonzero total alongside 0 cards here is a
      // fetch fault, not Steam's honest answer.
      const totals = await getReviewTotals(appId);
      if (totals && totals.totalReviews > 0) degenerate = true;
      break;
    }
    const reviews = parsed.reviews;
    if (!reviews.length) break;
    let pastWindow = false;
    for (const r of reviews) {
      if (got >= perAppReviews || !keepGoing) break;
      // Defensive only: a clean multi-page chain measured 0 duplicate ids live (c2128), unlike the
      // dead API, which really did repeat its last page once the cursor ran out.
      if (r.recommendationid != null && seen.has(r.recommendationid)) continue;
      if (r.recommendationid != null) seen.add(r.recommendationid);
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
      const metaCode = encodeMeta(item.recommended);
      // Watch mode, incremental run: an id already in the baseline is not automatically old. Steam
      // keeps a review's recommendationid stable when its author edits it in place (verified live,
      // see the comment at WATCH_EVENTS above), so a returning id must be diffed against the
      // recorded recommendation rather than skipped unconditionally — same gap as
      // google-play-reviews-scraper h844 / app-store-reviews-scraper h845.
      if (watchMode && !appSeeding && watchId != null && watchSeen.has(watchId)) {
        const previous = watchMeta.get(watchId) ?? null;
        const changed = previous != null && item.recommended != null && previous !== item.recommended;
        if (changed && watchEvents.has('recommendationChanged')) {
          item.watchEvent = 'recommendationChanged';
          item.previousRecommended = previous;
          watchChanged += 1;
          newForApp += 1;
          // chargeAndPush, not pushResult: pushResult's own "already delivered" guard would
          // unconditionally skip this id since it IS already in watchSeen — that guard exists to
          // stop a genuinely-unchanged repeat from being re-charged, not to block a real change.
          keepGoing = await chargeAndPush(item, watchId, metaCode);
        } else {
          // Record the new recommendation anyway: an excluded change must not be re-reported later
          // as a change from the stale pre-change state.
          if (changed) watchEventsFiltered += 1;
          watchMeta.set(watchId, decodeMeta(metaCode));
          watchSkipped += 1;
        }
        continue;
      }
      if (watchMode && !appSeeding && watchId != null && !watchEvents.has('new')) {
        // "new" deselected: record it (and its recommendation) in the baseline so a later change
        // can still be detected, but do not deliver or charge for it.
        watchSeen.add(watchId);
        watchMeta.set(watchId, decodeMeta(metaCode));
        watchEventsFiltered += 1;
        watchSkipped += 1;
        continue;
      }
      if (watchMode && !appSeeding && watchId != null) { item.watchEvent = 'new'; item.previousRecommended = null; }
      // Counts reviews that passed the filters AND were not already in the baseline — the
      // saturation signal below. Distinct from pushResult's own watchSkipped bookkeeping.
      newForApp += 1;
      keepGoing = await pushResult(item, watchId, appSeeding, metaCode);
    }
    if (pastWindow) break;
    // End of feed is the Show-More form being ABSENT from the response, never "the page came back
    // short" — Steam silently clamps/repeats instead of signalling an empty page (verified c2128).
    if (!parsed.next) break;
    next = parsed.next;
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
// Entries of `apps` that are not a Steam store URL or a numeric App ID — e.g. a game NAME, which
// belongs in `searchTerms`. Kept as a bucket rather than a log line only (h988 covered the
// ALL-unparseable run, which falls through to its own "no valid Steam App IDs" message below; the
// PARTIAL case was silent): with 1 of 2 apps unparseable the run pushed the other app's rows, hit
// none of the per-id buckets, set NO status message at all, and reported appsRequested as the
// resolved count — so a buyer pasting a mixed list of URLs and names was charged for a subset and
// told nothing. Same silent-drop class as emptySearches in the partial branch (cycle 1592).
const unparsedApps = [];
for (const a of apps) {
  const id = parseAppId(a);
  if (id) addId(id);
  else {
    unparsedApps.push(a);
    log.warning(`Cannot parse an App ID from "${a}" — use a Steam store URL (…/app/1145360/Hades/) or the numeric App ID.`);
  }
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
// Apps that DID return reviews but had every single one removed by the active filters. Kept apart
// from emptyIds (Steam returned nothing at all) and depthCapped (the cap was hit mid-filter): all
// three are different things for the buyer to do, and a run over several apps can hit them at once.
const allFilteredIds = [];
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
      // The dead appreviews API's query_summary gave an all-language, all-purchase-type total plus
      // Valve's own review_score/review_score_desc bucket (e.g. "Overwhelmingly Positive"). The
      // still-live appreviewhistogram gives the same up/down totals (summed below) but has no score
      // bucket at all — gameRow() below sets reviewScore/reviewScoreDesc to null rather than
      // inventing an approximation of Valve's own algorithm with no ground truth to check it
      // against. filter_offtopic_activity has no histogram equivalent either, so totals here are
      // always the all-activity (off-topic-included) count regardless of includeOffTopic.
      const totals = await getReviewTotals(id);
      summary = totals ? { total_reviews: totals.totalReviews, total_positive: totals.totalPositive, total_negative: totals.totalNegative } : null;
      if (!summary) {
        log.warning(`Steam returned no review histogram for app ${id} — reviewScore/totalReviews/totalPositive/totalNegative will be null in this row. Upstream fault; re-run later for those fields.`);
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
    // Every review this app returned was rejected by the filters (filteredOut counts only filter
    // rejects). Watch mode is excluded because there "nothing delivered" is normally the
    // already-seen baseline, not the filters, and watch runs use their own status branches.
    if (!watchMode && got > 0 && filteredOut === got) allFilteredIds.push(id);
    if (degenerate) {
      upstreamDegraded.push(id);
      log.warning(
        `App ${id}: the review page came back with 0 review cards, but the review histogram says it has `
        + `reviews. This is an upstream Steam fault, not a filter problem and not a sign that the app has `
        + `no reviews; re-run this input later.`,
      );
    } else if (got === 0) {
      emptyIds.push(id);
      const totals = await getReviewTotals(id);
      log.warning(totals && totals.totalReviews === 0
        ? `App ${id} has no Steam reviews at all yet (that is Steam's data, not a scrape failure).`
        : `Steam returned no reviews for app ${id} with language="${language}", review_type="${reviewType}" — try language "all" or a different filter.`);
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
// Why a run delivered nothing, as an ACCUMULATED list rather than a first-match-wins chain: the
// per-id buckets are filled independently inside one loop over the id list (plus a separate loop
// for searchTerms), so a multi-app run routinely hits two or three of these at once and an
// else-if/ternary cascade names the first and silently drops the rest. Same cascade-hides-
// independent-cause defect fixed in google-play-reviews-scraper's two status branches (cycles 1559
// and 1591). Order is most-specific-first; every entry names the apps/terms it applies to so the
// buyer can act per app instead of guessing which cause covers which id.
const zeroCauses = [];
// One wording, used by the zero-row, partial-success and watch branches alike, so the three paths
// cannot drift apart the way emptySearches did before cycle 1592.
const unparsedCause = unparsedApps.length
  ? `no Steam App ID could be parsed from ${unparsedApps.length} "apps" entr${unparsedApps.length > 1 ? 'ies' : 'y'}: `
    // No internal semicolon, deliberately: zeroCauses/partialCauses are joined with '; ', so one
    // inside a cause string would read as a cause boundary (same trap fixed at cycle 1592).
    + `${unparsedApps.map((a) => JSON.stringify(a)).join(', ')} — those entries were skipped, and "apps" takes `
    + 'a store URL (…/app/1145360/Hades/) or a numeric App ID, so game NAMES belong in "searchTerms"'
  : null;
// Gated on something else having been seeded: with apps ALL unparseable and no searchTerms there is
// nothing else to report, and the `why` chain below must keep falling through to h988's dedicated
// "no valid Steam App IDs could be parsed from your input" message (verified live, cycle 1592).
if (unparsedCause && (ids.length > 0 || searchTerms.length > 0)) {
  zeroCauses.push(unparsedCause);
}
if (emptyIds.length) {
  zeroCauses.push(`Steam returned nothing for: ${emptyIds.join(', ')} (language "${language}", country "${country}")`);
}
if (emptySearches.length) {
  zeroCauses.push(`your search terms matched no Steam games: ${emptySearches.join(', ')}`);
}
if (depthCapped.length) {
  zeroCauses.push(`maxReviewsPerApp (${perAppReviews}) was hit before any review passed your keyword/minPlaytimeHours filter for: ${depthCapped.join(', ')} — raise maxReviewsPerApp to search deeper`);
}
// Deduped against depthCapped, which is the more specific statement of the same shortfall for an
// app that hit the cap (raise the cap) versus one whose whole feed was scanned and rejected
// (loosen the filter) — naming an app under both causes would give contradictory advice.
const filteredOutOnly = allFilteredIds.filter((id) => !depthCapped.includes(id));
if (filteredOutOnly.length) {
  zeroCauses.push(`every review Steam returned was removed by your keyword / minimum-playtime / date-window filters for: ${filteredOutOnly.join(', ')}`);
}

let runError = null;
if (pushed === 0 && upstreamDegraded.length) {
  runError = `Steam's review API returned incomplete responses (success, but no reviews and no review `
    + `totals) for: ${upstreamDegraded.join(', ')} — after 2 retries each. This is an upstream Steam `
    + `fault, not a problem with your input; please re-run later.`;
  // The other causes have to survive into the FAILED run's status message too: Actor.fail(runError)
  // at the tail overwrites whatever status message the block below set, so without this a run where
  // one app was degraded AND another genuinely has no reviews reads as a pure upstream fault and the
  // buyer re-runs the hopeless app forever waiting for Steam to recover.
  if (zeroCauses.length) {
    runError += ` Separately, and not fixable by re-running: ${zeroCauses.join('; ')}.`;
  }
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
// Coverage of the REQUESTED input was incomplete even if every id that parsed answered fully, so a
// pipeline reading `complete` must not treat a mixed URL/name list as a full delivery.
if (unparsedApps.length) markIncomplete('unparsed-apps', unparsedCause);
if (watchMode && !seeding && saturatedApps.length) markIncomplete('watch-saturated', `every scanned review was new for: ${saturatedApps.join(', ')} — older new reviews may have been missed`);

// A watch status message still has to carry the upstream-fault notice when only SOME apps were
// degraded (a fully-degraded run already failed above) — those apps were not baselined and their
// reviews were never scanned, so "nothing new" would be a misleading thing to leave unqualified.
const baselinedSuffix = baselinedInPlace.length
  ? ` Newly-watched app(s) ${baselinedInPlace.join(', ')} were baselined this run instead of having their whole review history delivered — you will get their new reviews from the next run on.`
  : '';
// Watch-mode branches build their message from suffixes, not from partialCauses, so without this
// an unparseable entry vanishes from every watch run's status line.
const unparsedSuffix = unparsedCause ? ` Also: ${unparsedCause}.` : '';
const degradedSuffix = upstreamDegraded.length
  ? ` Steam's review API returned incomplete responses for: ${upstreamDegraded.join(', ')} — an upstream fault, not your input; those apps were skipped, re-run them later.`
  : '';
// Inputs this run accepted but could not act on (dead upstream facet, or wrong dataType). Until
// now these were `log.warning` only, so a buyer who set `purchaseType` or `dayRange`, read a green
// "Succeeded" beside a full dataset and never opened the log believed a filter had been applied
// that was not -- the worst shape of silence, because the rows look right. Deduped because a
// field can be named by both a reviews-mode and a games-mode warning in principle.
const ignoredUnique = [...new Set(ignoredInputs)];
const ignoredSuffix = ignoredUnique.length
  ? ` NOTE: ${ignoredUnique.length} input(s) you set had no effect on this run and were ignored: `
    + `${ignoredUnique.join(', ')} — see the log for why each one cannot be honored, and RUN_SUMMARY.ignoredInputs.`
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
// The suffix has to name the reason the id list was actually truncated, not assume the clock:
// idsNotReached is non-empty whenever the loop stopped early for ANY reason, so gating only on it
// blamed "approaching the platform run timeout" for a list cut short by maxResults or the charge
// limit (reproduced live on a real platform run, cycle 1592) and sent the buyer to raise a run
// timeout that was never the constraint. Each variant ends with the advice that fixes ITS cause.
// Capitalized at source: the suffix always starts a new sentence, and upper-casing it afterwards
// would mangle the field name in the maxResults variant ("MaxResults=5").
const truncationCause = timeBudgetExceeded
  ? 'The run was approaching the platform run timeout and stopped before finishing the id list'
  : chargeLimitReached
    ? "The run's pay-per-event charge limit was reached before the id list was finished"
    : pushed >= maxResults
      ? `The "maxResults" limit of ${maxResults} was reached before the id list was finished`
      : 'The run stopped before finishing the id list';
const truncationAdvice = timeBudgetExceeded
  ? ' Narrow the input (fewer apps/search terms, or a lower "maxReviewsPerApp"), raise the Actor\'s run timeout, or run the rest separately.'
  : chargeLimitReached
    ? ' Raise the run\'s charge limit, or run the remaining id(s) separately.'
    : pushed >= maxResults
      ? ' Raise "maxResults" to cover the whole id list, or run the remaining id(s) separately.'
      : ' Re-run the remaining id(s) separately. See the log and RUN_SUMMARY for the stopping reason.';
const timeoutSuffix = idsNotReached.length
  ? ` ${truncationCause} — ${idsNotReached.length} id(s) were never fetched: ${idsNotReached.join(', ')}.${truncationAdvice}`
  : '';
if (timeBudgetExceeded && pushed === 0 && watchMode && seeding) {
  await Actor.setStatusMessage(`Baseline run for watch label "${watchLabel}" did not finish — the run was approaching the platform run timeout.${timeoutSuffix} ${watchSeen.size} review(s) across ${seededApps.size} app(s) were recorded before it stopped; 0 rows returned, 0 charged. Re-run to finish seeding before switching to incremental runs.${unparsedSuffix}${ignoredSuffix}`);
} else if (timeBudgetExceeded && pushed === 0 && watchMode) {
  await Actor.setStatusMessage(`No new reviews delivered for watch label "${watchLabel}" — the run was approaching the platform run timeout, not confirmation that nothing is new.${timeoutSuffix}${unparsedSuffix}${ignoredSuffix}`);
} else if (watchMode && seeding) {
  await Actor.setStatusMessage(`Baseline run for watch label "${watchLabel}": ${watchSeen.size} existing review(s) across ${seededApps.size} app(s) recorded, 0 rows returned, 0 charged. Run it again later to get only what's new.${degradedSuffix}${evictionSuffix}${unparsedSuffix}${ignoredSuffix}`);
} else if (watchMode && pushed === 0) {
  await Actor.setStatusMessage(`Nothing new for watch label "${watchLabel}" since its last run — all ${watchSkipped} matching review(s) had already been delivered and none of them changed. That is the expected result most of the time; you were charged for nothing.${watchEventsFiltered ? ` (${watchEventsFiltered} review(s) did change, or were new, but the event was excluded by your watchEvents list.)` : ''}${baselinedSuffix}${degradedSuffix}${evictionSuffix}${unparsedSuffix}${ignoredSuffix}`);
} else if (watchMode && saturatedApps.length) {
  await Actor.setStatusMessage(`Pushed ${pushed} new review(s) for watch label "${watchLabel}". Every matching review in the scanned window was new for: ${saturatedApps.join(', ')} — older new reviews may have been missed; raise maxReviewsPerApp or run the watch more often.${baselinedSuffix}${degradedSuffix}${evictionSuffix}${unparsedSuffix}${ignoredSuffix}`);
} else if (watchMode) {
  await Actor.setStatusMessage(`Watch label "${watchLabel}": ${pushed} item(s) since the last run (${watchSkipped} already-delivered review(s) skipped, not charged${watchChanged ? `; ${watchChanged} of the pushed item(s) were a thumbs-up/thumbs-down change on an already-delivered review, not a brand-new one` : ''}${watchEventsFiltered ? `; ${watchEventsFiltered} change(s)/new review(s) excluded by your watchEvents list` : ''}).${baselinedSuffix}${degradedSuffix}${evictionSuffix}${unparsedSuffix}${ignoredSuffix}`);
} else if (pushed === 0) {
  // timeBudgetExceeded checked FIRST: without it, timing out before any id was even attempted falls
  // into the final default below ("no valid Steam App IDs could be parsed from your input") -- a
  // false claim about the input when the real cause is our own clock (idsAttempted stays empty, so
  // emptyIds/emptySearches/depthCapped are all empty too, not because nothing matched).
  // zeroCauses (built above, next to runError) accumulates every independently-populated cause
  // instead of reporting only the first match. The filter cause is carried there as a per-app
  // bucket (allFilteredIds), which also keeps the h988 guarantee that drove the old `idsAttempted`
  // gate: an `apps` list where nothing parses as an App ID never reaches either fetch loop, so no
  // bucket is filled, no cause is claimed, and the run falls through to the parse message instead
  // of blaming a filter for a query Steam was never asked.
  const why = timeBudgetExceeded && idsAttempted.size === 0
    ? 'the run was approaching the platform run timeout and stopped before any id could be checked'
    : zeroCauses.length
      ? zeroCauses.join('; ')
      // Ids were attempted and no per-id cause fired, so the stop was ours, not the data's: saying
      // "no valid App IDs" there would blame an input that parsed fine.
      : idsAttempted.size > 0
        ? (chargeLimitReached
          ? "the run's pay-per-event charge limit was reached before any review could be returned — raise the limit"
          : 'the run stopped before any review could be returned; see the log and RUN_SUMMARY for the stopping reason')
        : 'no valid Steam App IDs could be parsed from your input';
  await Actor.setStatusMessage(`No results — ${why}.${timeBudgetExceeded ? timeoutSuffix : ' See the log for details.'}${ignoredSuffix}`);
} else if (upstreamDegraded.length || depthCapped.length || allFilteredIds.length
  || emptyIds.length || emptySearches.length || unparsedApps.length) {
  // Partial success: other apps produced rows, so the run is not a failure, but the buyer still
  // needs to know which specific apps fell short and why. Accumulated for the same reason as
  // zeroCauses above — these buckets are filled independently per id in one loop, so a run where
  // one app was degraded, another hit the depth cap and a third has no reviews hits all three at
  // once, and the else-if chain this replaced reported only the upstream fault and silently dropped
  // the other two (cascade class, cycles 1559/1591).
  const partialCauses = [];
  // Listed first: it is the only cause here the buyer can fix by editing the input alone.
  if (unparsedCause) partialCauses.push(unparsedCause);
  if (upstreamDegraded.length) {
    partialCauses.push(`Steam's review API returned incomplete responses for: ${upstreamDegraded.join(', ')} — an upstream fault, not your input, so re-run those later`);
  }
  if (depthCapped.length) {
    partialCauses.push(`maxReviewsPerApp (${perAppReviews}) was hit while filtering: ${depthCapped.join(', ')} — some matching reviews may sit deeper in the feed, so raise maxReviewsPerApp to search further`);
  }
  // Same depthCapped dedupe as zeroCauses: raise-the-cap and loosen-the-filter are different advice.
  const partialFilteredOnly = allFilteredIds.filter((id) => !depthCapped.includes(id));
  if (partialFilteredOnly.length) {
    partialCauses.push(`every review Steam returned was removed by your keyword / minimum-playtime / date-window filters for: ${partialFilteredOnly.join(', ')}`);
  }
  if (emptyIds.length) {
    partialCauses.push(`Steam returned nothing for: ${emptyIds.join(', ')}`);
  }
  // emptySearches was never named in this branch at all before (not merely cascaded away): a run
  // where one search term resolved to games and another matched nothing reported full success and
  // left the buyer believing the dead term had been covered.
  if (emptySearches.length) {
    partialCauses.push(`your search term(s) matched no Steam games: ${emptySearches.join(', ')}`);
  }
  // '; ' join, same as zeroCauses — no cause string contains a semicolon of its own, so each
  // separator is unambiguously a cause boundary.
  // Em-dash prefix, matching the "No results — ..." style, so the lower-cased cause strings (which
  // start with field names like `maxReviewsPerApp`) read as a continuation instead of a new sentence.
  await Actor.setStatusMessage(`Pushed ${pushed} results — ${partialCauses.join('; ')}.${timeoutSuffix}${ignoredSuffix}`);
} else if (timeBudgetExceeded) {
  await Actor.setStatusMessage(`Pushed ${pushed} results.${timeoutSuffix}${unparsedSuffix}${ignoredSuffix}`);
} else if (!complete) {
  // Reaches here only for a non-watch run that hit maxResults or the charge limit cleanly (no
  // upstream/depth/empty issue), which none of the branches above cover.
  await Actor.setStatusMessage(`Pushed ${pushed} results — incomplete: ${incompleteReason}${incompleteDetail ? ` (${incompleteDetail})` : ''}. See RUN_SUMMARY for details.${ignoredSuffix}`);
} else if (ignoredSuffix) {
  // Last branch on purpose: a run that is otherwise complete and clean sets no status message at
  // all by this Actor's convention (verified c2408 on website-screenshot-scraper's equivalent), so
  // without this branch the ignored-input NOTE would be dropped on exactly the runs where it is the
  // only thing the buyer needs to know -- full dataset, nothing wrong, one dead filter.
  await Actor.setStatusMessage(`Pushed ${pushed} results.${ignoredSuffix}`);
}

// RUN_SUMMARY: this run's completeness, in a form a pipeline can read (h250, same shape as
// fec-campaign-finance-scraper cycle 676). Fetch with
//   GET /v2/actor-runs/<runId>/key-value-store/records/RUN_SUMMARY
// which needs no webhook.
const runSummary = {
  mode: watchMode ? (seeding ? 'watch-seed' : 'watch-incremental') : dataType,
  dataType,
  // Resolved ids only — an "apps" entry that is not a store URL or numeric App ID never becomes an
  // id, so this UNDERCOUNTS what the buyer asked for. `unparsedApps` carries the difference.
  appsRequested: ids.length,
  delivered: pushed,
  // Verbatim "apps" entries no App ID could be parsed from (a game name belongs in searchTerms).
  unparsedApps,
  emptySearches,
  emptyIds,
  upstreamDegraded,
  depthCapped,
  // Apps whose whole returned feed was rejected by the filters — distinct from emptyIds and
  // depthCapped so a pipeline can tell "loosen the filter" from "no data" and "raise the cap".
  allFiltered: allFilteredIds,
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
  watchEvents: watchMode ? [...watchEvents] : null,
  watchChanged: watchMode && !seeding ? watchChanged : null,
  watchEventsFiltered: watchMode && !seeding ? watchEventsFiltered : null,
  watchDeadDateBound: watchMode ? watchDeadDateBound : null,
  // Bare names of inputs this run accepted but could not act on (dead upstream facet, or a field
  // that only applies to the other dataType). Always an array, [] on a run that set none, so a
  // pipeline can assert on it without a presence check.
  ignoredInputs: ignoredUnique,
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
