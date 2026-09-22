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
// Storefronts are ISO-3166-1 alpha-2, and "countries" is a free-text list, so the commonest input
// mistake by far is "uk" (the UK storefront is "gb"). Apple's answer to a bad code is silent in
// three different ways -- see the getJson comment below -- so catch the recognisable wrong codes
// here, before any request is made, and name the right one.
const STOREFRONT_FIX = {
  uk: 'gb', usa: 'us', gbr: 'gb', deu: 'de', fra: 'fr', jpn: 'jp', can: 'ca', aus: 'au',
  ind: 'in', bra: 'br', uae: 'ae', esp: 'es', ita: 'it', mex: 'mx', kor: 'kr', chn: 'cn', nld: 'nl',
};
const badStorefronts = countries.filter((c) => STOREFRONT_FIX[c] || !/^[a-z]{2}$/.test(c));
if (badStorefronts.length) {
  await Actor.fail(
    `Not an App Store storefront code: ${badStorefronts.map((c) => `"${c}"`).join(', ')}. `
    + `Storefronts are two-letter ISO-3166-1 alpha-2 codes (us, gb, de, jp, ...)`
    + `${badStorefronts.some((c) => STOREFRONT_FIX[c]) ? ` — you probably want ${badStorefronts.filter((c) => STOREFRONT_FIX[c]).map((c) => `"${STOREFRONT_FIX[c]}" instead of "${c}"`).join(', ')}` : ''}.`,
  );
}
// favorable/critical are not real Apple feed orders -- there is no server-side "sort by rating".
// They mean "scan under mostRecent, then buffer the whole per-pair scan and re-emit it sorted by
// rating before pushing" (see ratingSort below). requestedSort stays mostRecent/mostHelpful only;
// it is the underlying feed order actually requested from Apple.
const RATING_SORTS = new Set(['favorable', 'critical']);
const ratingSort = RATING_SORTS.has(input.sort) ? input.sort : null;
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
// ratingSort always scans under mostRecent: it needs the whole per-pair result set buffered
// anyway, and mostRecent is the only feed order that also supports reviewsAfter's early-stop.
const sort = (reviewsAfterDate || ratingSort) ? 'mostRecent' : requestedSort;
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
// The deepest a seeding walk is ALLOWED to go (10 pages x 50). It is a ceiling, not a promise:
// as of 2026-09-22 Apple's feed usually quits far sooner (often after page 1), so a baseline can
// easily hold only the newest ~50 reviews of a pair. That is why a truncated baseline can no
// longer over-charge — see `pairFloors` below.
const WATCH_SCAN_CAP = 500;
let baselineTruncated = 0; // review ids dropped by WATCH_KEEP this run -- they come back as "new" and get charged
let baselineTruncatedTotal = 0; // same, cumulative over the life of this label

function watchKeyFor(label, criteria) {
  const safe = label.toLowerCase().replace(/[^a-z0-9_.-]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 40) || 'default';
  const fp = createHash('sha1').update(JSON.stringify(criteria, Object.keys(criteria).sort())).digest('hex').slice(0, 10);
  return { key: `watch-${safe}-${fp}`, fingerprint: fp };
}

const watchMode = watchLabel.length > 0;
if (watchMode && ratingSort) {
  await Actor.fail(
    `"sort": "${ratingSort}" cannot be combined with "watchLabel". Rating sort buffers a whole app/country `
    + 'scan and re-orders it before delivery; watchLabel\'s "only what\'s new since last run" semantics depend on '
    + 'scanning and delivering in the feed\'s own order. Drop watchLabel to use rating sort, or use sort '
    + '"mostRecent"/"mostHelpful" with watchLabel.',
  );
}
let watchStore = null;
let watchKey = null;
let watchRecord = null;
let seeding = false;
let watchSkipped = 0;
let unidentifiedSkipped = 0; // watch mode only: reviews Apple returned without a usable id
const watchSeen = new Set(); // `${appId}:${actualCountry}:${reviewId}` already delivered under this label+fingerprint
const seededPairs = new Set(); // `${appId}::${requestedCountry}` pairs already baselined
// Per `${appId}::${actualCountry}` date floor, written ONCE when that pair is baselined: the
// OLDEST review date the baseline walk actually scanned. Any review older than that existed at
// baseline time and was simply out of reach (Apple truncated the walk) — so it is NOT new and must
// never be delivered or charged on a later run, however deep that run happens to get. A genuinely
// new review is posted after the baseline run, hence always newer than the floor, so this can only
// remove false "new", never hide a real one. Deliberately never updated after seeding: lowering it
// on an incremental run would re-expose the very reviews it had just suppressed.
const pairFloors = new Map();
const seedFloors = new Map(); // oldest date scanned per pair DURING this run's seeding walks
let floorSkipped = 0; // reviews suppressed by a pair floor this run (not delivered, not charged)
// Promote the floors measured while baselining this app (its requested storefront and, if it ran,
// its countryFallback storefront) into the persisted record. Called only where the pair is marked
// baselined, i.e. only when its seed walk actually completed — a walk cut short by SEED_CAP has an
// incomplete picture and must not leave a floor behind, same invariant as `seededPairs`.
function commitSeedFloors(appId) {
  for (const [k, v] of seedFloors) {
    if (!k.startsWith(`${appId}::`)) continue;
    if (!pairFloors.has(k)) pairFloors.set(k, v);
    seedFloors.delete(k);
  }
}

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
    // Absent on records written before this was added: those watches keep their old behaviour
    // (id-set only) rather than acquiring a floor retroactively from a walk that never measured one.
    for (const [p, d] of Object.entries(existing.pairFloors ?? {})) pairFloors.set(String(p), String(d));
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
  // An id past the record cap is not forgotten harmlessly: the next run does not find it in the
  // baseline, so it is delivered and CHARGED again even though the buyer already paid for it.
  // Same shape as us-federal-awards-scraper / fec-campaign-finance-scraper (h285).
  baselineTruncated = watchSeen.size - ids.length;
  baselineTruncatedTotal = (watchRecord.truncatedTotal ?? 0) + baselineTruncated;
  if (baselineTruncated > 0) {
    log.warning(
      `The baseline for "${watchLabel}" exceeded the ${WATCH_KEEP}-entry record cap; the ${baselineTruncated} `
      + 'oldest review id(s) were dropped and will be returned and CHARGED as new on a future run '
      + `(${baselineTruncatedTotal} dropped over the life of this label). Narrow the watch (fewer apps/countries `
      + 'or a stricter rating/keyword/length/vote filter) or split it across several labels so each baseline '
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
    seededPairs: Array.from(seededPairs),
    pairFloors: Object.fromEntries(pairFloors),
    seenIds: ids,
  });
}

let pushed = 0;
let chargeLimitHit = false; // the buyer's own pay-per-event charge limit was exhausted mid-run
const isPPE = Actor.getChargingManager().getPricingInfo().isPayPerEvent;
// ratingSort buffers one (app,country) pair's whole passing-filter scan here instead of pushing
// immediately, so it can be re-ordered by rating before delivery. Reset per pair (see the main
// pair loop below) -- buffering globally would let one huge app dominate memory/ordering.
let pairBuffer = [];
async function chargeAndPush(item, watchId = null) {
  if (isPPE) {
    const r = await Actor.charge({ eventName: 'result', count: 1 });
    if (r.chargedCount === 0) return false; // user's budget exhausted: never push unpaid items
    await Actor.pushData(item); pushed += 1;
    if (watchMode && watchId != null) watchSeen.add(watchId);
    if (r.eventChargeLimitReached) chargeLimitHit = true;
    return !r.eventChargeLimitReached && pushed < maxResults;
  }
  await Actor.pushData(item); pushed += 1; // non-PPE run (e.g. developer test): no charging
  if (watchMode && watchId != null) watchSeen.add(watchId);
  return pushed < maxResults;
}
// Sorts everything currently buffered for one (app,country) pair by rating and charges/pushes it
// in that order, then empties the buffer. Ties keep newest-first, matching the mostRecent scan
// order used underneath. Called right after each scrapeAppCountry() call (primary and, if it
// runs, the countryFallback retry) -- BEFORE the "N kept after filters" log line that follows, so
// `pushed` is accurate by the time that line reads it.
async function flushPairBuffer() {
  if (!pairBuffer.length) return;
  const buffered = pairBuffer;
  pairBuffer = [];
  buffered.sort((a, b) => {
    const ra = a.item.rating ?? 0;
    const rb = b.item.rating ?? 0;
    const byRating = ratingSort === 'favorable' ? rb - ra : ra - rb;
    if (byRating !== 0) return byRating;
    return new Date(b.item.updatedAt || 0) - new Date(a.item.updatedAt || 0);
  });
  for (const { item, watchId } of buffered) {
    keepGoing = await chargeAndPush(item, watchId);
    if (!keepGoing) break;
  }
}
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
  // Older than everything the baseline walk managed to scan for this pair => it existed back then
  // and Apple simply did not serve it, so it is not "since the last run". Not pushed, not charged.
  if (watchMode && watchId != null) {
    const floor = pairFloors.get(`${item.appId}::${item.country}`);
    if (floor && item.updatedAt && new Date(item.updatedAt) < new Date(floor)) {
      floorSkipped += 1;
      return true;
    }
  }
  if (ratingSort) {
    // Not charged/pushed yet -- just buffered. maxReviewsPerApp/reviewsAfter early-stop still
    // apply to the SCAN (tally.got / canEarlyStop in scrapeAppCountrySort, both unaffected by
    // this), so the scan depth is identical to a non-rating-sort run; only the push order defers.
    pairBuffer.push({ item, watchId });
    return true;
  }
  return chargeAndPush(item, watchId);
}
// got-scraping does NOT throw on 4xx, and Apple's error bodies parse as three different kinds of
// nonsense (all measured live 2026-09-21 with the storefront code "uk", which is not a storefront):
//   - lookup/search: 400 with VALID JSON `{"errorMessage":"Invalid value(s) for key(s): [country]"}`
//     and no `results` key, so it parsed fine and read downstream as "app not found";
//   - review RSS feed: 400 with an EMPTY body -> raw `Unexpected end of JSON input`;
//   - a malformed storefront segment (e.g. "USA"): 404 HTML -> `Unexpected token '<'`.
// So the customer's own typo surfaced as a missing app or a JSON stack trace. Check the status
// before parsing and say what is actually wrong. Same defect class as the 0.1.43 Shopify fix.
const storefrontOf = (url) => url.match(/[?&]country=([^&]*)/)?.[1] ?? url.match(/itunes\.apple\.com\/([^/]+)\/rss/)?.[1] ?? null;
// got's own `retry` only covers a fixed errorCodes list that excludes the connection-establishment
// faults (ERR_HTTP2_ERROR / HPE_INVALID_CONSTANT) measured live on this got-scraping version in
// cycle 616 — about 1 in 4 fresh connections. Without an outer retry a single blip reads as
// "Apple has nothing": a review page throws and the app is recorded as failed, and the ratings
// histogram quietly comes back null. The run still SUCCEEDS, just with less than the buyer paid to
// query. Retry connection-level throws before believing them. Only exceptions reach here — an HTTP
// 4xx/5xx is a returned response (got-scraping does not throw on status) and is classified by
// getJson below, so a wrong storefront code still fails on attempt 1 instead of looping.
const requestWithRetry = async (url, opts = {}) => {
  let lastErr;
  for (let attempt = 1; attempt <= 3; attempt += 1) {
    try {
      return await gotScraping({ url, timeout: { request: 30000 }, retry: { limit: 2 }, ...opts });
    } catch (e) {
      lastErr = e;
      if (attempt < 3) {
        log.warning(`${url}: attempt ${attempt}/3 failed (${e.message}) — retrying.`);
        await new Promise((r) => setTimeout(r, attempt * 1000));
      }
    }
  }
  throw lastErr;
};

const getJson = async (url, opts = {}) => {
  const resp = await requestWithRetry(url, opts);
  if (resp.statusCode >= 400) {
    let detail = '';
    try { detail = String(JSON.parse(resp.body)?.errorMessage ?? ''); } catch { /* empty or HTML body */ }
    const cc = storefrontOf(url);
    const hint = resp.statusCode === 429
      ? ' Apple is rate-limiting this run; try again in a few minutes or lower "maxResults".'
      : (cc && (resp.statusCode === 400 || resp.statusCode === 404)
        ? ` The storefront code in this request was "${cc}" — storefronts are two-letter ISO-3166-1 alpha-2 codes (the UK is "gb", not "uk").`
        : '');
    // Tagged so callers can tell a permanent input fault (4xx: this storefront/app will never
    // answer) from a transient one (429/5xx: retrying the other client class is worth it).
    throw Object.assign(new Error(`Apple returned HTTP ${resp.statusCode}${detail ? ` (${detail})` : ''}.${hint}`), { httpStatus: resp.statusCode });
  }
  try {
    return JSON.parse(resp.body);
  } catch {
    throw Object.assign(
      new Error(`Apple returned HTTP ${resp.statusCode} with a body that is not JSON (${resp.body ? `starts with ${JSON.stringify(String(resp.body).slice(0, 60))}` : 'empty body'}).`),
      { httpStatus: resp.statusCode },
    );
  }
};

// Apple's review RSS has holes: for a given (app, country, sortBy) some page numbers return a
// well-formed but EMPTY feed while later pages return a full 50 (verified 2026-09-10 — Spotify/us
// mostHelpful yields 50,50,0,0,0,0,50,0,0,0 across pages 1-10, reproducibly). An empty page
// therefore does NOT mean "end of reviews", so we scan the whole 1..10 page range and skip holes.
const MAX_RSS_PAGE = 10; // Apple serves no page beyond 10
// One full page of Apple's review RSS. A page returning fewer than this is the last one the app
// actually has; a FULL page followed by nothing means Apple cut the feed off (see the post-loop
// feedCeiling check in scrapeAppCountrySort).
const RSS_PAGE_SIZE = 50;

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
    const html = (await requestWithRetry(`https://apps.apple.com/${country}/app/id${appId}`, { retry: { limit: 1 } })).body;
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
// A 4xx that is not a rate limit is a permanent fault in the REQUEST (a storefront code that is
// well-formed but not a real Apple storefront, e.g. "zz", or an app id that does not exist there):
// no client class and no later page will ever answer it, so it is rethrown immediately instead of
// being warned about 20 times while the sweep walks pages 1-10 under both classes. `tolerateAll`
// keeps reviewFeedIsDown()'s control probes on the old behaviour — an outage probe must be allowed
// to come back empty rather than throwing out of the run.
async function fetchPage(url, primary = 'default', tolerateAll = false) {
  for (const clientClass of [primary, primary === 'default' ? 'ios' : 'default']) {
    let entries;
    try {
      entries = await fetchEntries(url, clientClass);
    } catch (e) {
      if (!tolerateAll && e.httpStatus >= 400 && e.httpStatus < 500 && e.httpStatus !== 429) throw e;
      log.warning(`${url} failed (${clientClass}): ${e.message}`);
      continue;
    }
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
        const { entries } = await fetchPage(`https://itunes.apple.com/${cc}/rss/customerreviews/id=${id}/sortBy=${sortBy}/page=1/json`, 'default', true);
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
// `getInfo` is a memoised thunk, not a resolved value: the app-level metadata (itunes lookup +
// ratings histogram, 2 requests) is only worth buying once this pair has proven it answers at all.
// It is called after the first page that actually returned entries, so a storefront Apple refuses
// (`zz`, or an app absent from that storefront) now costs 1 request instead of 3.
async function scrapeAppCountrySort(appId, country, sortBy, seen, getInfo, tally, extra = {}, pairSeeding = false) {
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
  // True when the buyer's own scan cap cut a page short, i.e. the run stopped wanting more before
  // Apple stopped serving. Distinguishes "raise maxReviewsPerApp" from "Apple has no page 11".
  let capBrokeMidPage = false;
  // The deepest page Apple actually answered with reviews, and whether that page came back FULL.
  // A full last page followed by nothing is the calibration-free tell that Apple truncated the
  // feed rather than the app running out of reviews — an app that really ran out ends on a
  // PARTIAL page. Used below for the early-dry case; see the comment at the post-loop check.
  let lastServedPage = 0;
  let lastPageFull = false;
  for (let page = 1; page <= MAX_RSS_PAGE && tally.got < scanCap && keepGoing && !hitCutoff; page++) {
    const url = `https://itunes.apple.com/${country}/rss/customerreviews/id=${appId}/sortBy=${sortBy}/page=${page}/json`;
    let entries;
    let clientClass;
    try {
      ({ entries, clientClass } = await fetchPage(url));
    } catch (e) {
      // Permanent 4xx (see fetchPage): end this (app, country) pair here rather than requesting
      // the remaining pages, the other client class and the alternate sort, all of which are
      // guaranteed to fail the same way. The caller reports the message verbatim.
      tally.storefrontError = e.message;
      log.warning(`${appId}/${country} ${sortBy}: ${e.message} Stopping this app/storefront pair instead of requesting the remaining pages.`);
      break;
    }
    if (!entries.length) continue; // a real hole in Apple's feed, not the end of it — keep paging
    lastServedPage = page;
    lastPageFull = entries.length >= RSS_PAGE_SIZE;
    if (clientClass !== 'default') log.info(`${appId}/${country} ${sortBy} page ${page}: empty for the default client, recovered ${entries.length} reviews under the iOS client.`);
    // Memoised: one fetch per (app, country) across both sorts, resolved value reused every page.
    const info = await getInfo();
    for (const e of entries) {
      if (tally.got >= scanCap) { capBrokeMidPage = true; break; }
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
      // Floor measurement runs BEFORE the filters on purpose: a review this walk looked at and
      // discarded still proves the feed reached that date, and the filter set is part of the watch
      // fingerprint anyway, so a deeper (older) floor here is both safe and more useful.
      if (watchMode && pairSeeding && item.updatedAt) {
        const fk = `${appId}::${country}`;
        const prev = seedFloors.get(fk);
        if (!prev || new Date(item.updatedAt) < new Date(prev)) seedFloors.set(fk, item.updatedAt);
      }
      if (!passesFilters(item)) { tally.filteredOut += 1; continue; }
      const watchId = watchMode ? `${appId}:${country}:${reviewId}` : null;
      // Counts every matching review considered "new" this scan (not already in the baseline) --
      // used only to detect a saturated scan window (see the saturatedPairs check below), separate
      // from pushResult's own watchSkipped bookkeeping.
      if (!(watchMode && !pairSeeding && watchId != null && watchSeen.has(watchId))) tally.newForPair = (tally.newForPair || 0) + 1;
      keepGoing = await pushResult(item, watchId, pairSeeding);
      if (!keepGoing) break;
    }
    // Apple's LAST page came back full and we consumed all of it while still willing to take more:
    // the walk ended because Apple serves no page 11, not because the buyer asked for less.
    // Verified live 2026-09-22 — Spotify/us page 10 = 50 entries, page 11 = empty, while a 115-
    // rating app runs dry long before page 10. So a full page 10 means reviews exist behind the
    // ceiling that this feed will never serve, and no input change can reach them.
    if (page === MAX_RSS_PAGE && entries.length && !hitCutoff && keepGoing && !capBrokeMidPage) {
      tally.feedCeiling = true;
      tally.feedStopPage = page;
    }
  }
  // Apple also stops serving LONG before page 10, and as of 2026-09-22 that is the common case.
  // Measured that day: raw probes (plain curl AND an iPhone-Safari UA, sequential, two passes 10
  // minutes apart, identical both times) got a populated page 1 for only 6 of 36 (app, storefront)
  // pairs across 6 popular apps x 6 storefronts, and an EMPTY page 2 onwards for every pair that
  // did answer. This Actor's own client-class retry recovers a lot of that — the same Spotify/gb
  // and Notion/us pairs that read 0-or-50 to a raw probe both deliver 100 reviews here — but the
  // walk still ends far short, on a FULL page followed by nothing, for apps declaring millions of
  // ratings. Only the page-10 rule above used to catch that shape, and it no longer fires when the
  // feed quits at page 2 or 7. Same consequence for the buyer as the 500 ceiling: reviews exist
  // that this feed will not serve, and no input change reaches them.
  if (!tally.feedCeiling && lastPageFull && tally.got < scanCap && !hitCutoff && keepGoing
      && !capBrokeMidPage && !tally.storefrontError) {
    tally.feedCeiling = true;
    tally.feedStopPage = lastServedPage;
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
  // Deferred until a page actually returns reviews (see scrapeAppCountrySort), and memoised so the
  // alternate-sort retry below reuses the same metadata rather than buying it twice.
  let infoPromise;
  const getInfo = () => (infoPromise ??= getAppInfo(appId, country));
  await scrapeAppCountrySort(appId, country, sort, seen, getInfo, tally, extra, pairSeeding);
  // The alternate-sort fallback exists for Apple's per-sort feed HOLES; a 4xx is not a hole, it is
  // the whole (app, storefront) being unanswerable, so the other sort would only repeat the fault.
  if (tally.got === 0 && keepGoing && !tally.storefrontError) {
    const alt = sort === 'mostRecent' ? 'mostHelpful' : 'mostRecent';
    log.info(`${appId}/${country}: Apple's "${sort}" feed is empty; retrying under "${alt}".`);
    await scrapeAppCountrySort(appId, country, alt, seen, getInfo, tally, extra, pairSeeding);
  }
  // maxReviewsPerApp (perApp) caps reviews SCANNED, before review filtering (rating/keyword/length/votes/date)
  // -- if the cap was hit and some scanned reviews were dropped by a filter, matching reviews may
  // still sit deeper in Apple's feed and were never looked at.
  const scanCap = pairSeeding ? WATCH_SCAN_CAP : perApp;
  // How many reviews Apple SAYS this app has in this storefront, for the delivered-vs-declared
  // pair record below. Read off the already-memoised lookup only — never a fresh request: if
  // includeInfo is off (or the lookup failed, or no page ever served) this stays null rather than
  // costing the buyer a request they did not ask for, and null must never be read as zero.
  let declaredRatingCount = null;
  if (infoPromise) {
    const info = await infoPromise.catch(() => null);
    declaredRatingCount = info?.ratingCount ?? info?.totalRatings ?? null;
  }
  return {
    got: tally.got, filteredOut: tally.filteredOut, capReached: tally.got >= scanCap,
    newForPair: tally.newForPair || 0, storefrontError: tally.storefrontError || null,
    feedCeiling: tally.feedCeiling === true, feedStopPage: tally.feedStopPage ?? null,
    declaredRatingCount, scanCap,
  };
}

if (appNames.length) {
  const resolved = (await Promise.all(appNames.map(resolveAppName))).filter(Boolean);
  apps.push(...resolved);
}
if (!apps.length) await Actor.fail('None of the given "apps"/"appNames" resolved to a usable app id — see the warnings above.');

const emptyPairs = [];
// Pairs Apple answered with a permanent 4xx (bad storefront code, or an app id absent from that
// storefront). Distinct from emptyPairs: those are real Apple data, these are a rejected request.
const storefrontErrorPairs = [];
const storefrontErrorMessages = [];
const filteredOutPairs = [];
// Pairs where maxReviewsPerApp was hit while the review filters still discarded scanned
// reviews -- reviews deeper in Apple's feed were never scanned.
const depthCappedPairs = [];
// Watch mode: every matching review inside the scanned window was new, so older new reviews
// (posted since the last run but sorting past the window) may have been missed.
const saturatedPairs = [];
// Pairs where Apple's own hard feed ceiling (MAX_RSS_PAGE x 50 = 500 reviews per app/storefront)
// ended the walk: the last page Apple serves came back full and we were still taking reviews.
// Unlike every other shortfall here this one is NOT fixable from the input — it is the public RSS
// feed's limit — so it has to be SAID rather than hinted at with a "raise the cap" suggestion.
const feedCeilingPairs = [];
// One machine-readable record per (app, storefront) pair, written to the run's key-value store as
// RUN_SUMMARY and posted on the webhook. Every shortfall this Actor knows about is already SAID —
// in the log and in the status message — but both are English prose, so the only surface a
// PROGRAM can read is the dataset, where a run that delivered 500 of an app's 1.8M reviews and a
// run that delivered an app's complete review history arrive as the same thing: N rows and no
// disagreement anywhere. `delivered` next to `declaredRatingCount`, plus `complete` and the reason
// that made it false, answers that at the level the shortfall actually happens — the pair, not the
// run. Same shape and same lesson as shopify-products-scraper's sourceOutcomes (cycle 639).
const pairOutcomes = [];
// `complete` is deliberately NOT folded into `status`: a pair can deliver reviews perfectly
// normally (status "ok") and still have been cut short by Apple's feed ceiling, and collapsing the
// two would lose exactly the case this record exists for. `null` (never false, never 0) wherever
// we did not observe the answer — a refused pair has no completeness to report.
function recordPair(appId, country, res, delivered, status, extra = {}) {
  const truncatedByRun = !keepGoing; // the run stopped during THIS pair (recorded immediately after it)
  const incompleteReason = res.storefrontError ? null
    : res.feedCeiling ? 'apple-feed-ceiling'
    : res.capReached ? 'max-reviews-per-app'
    : truncatedByRun ? (chargeLimitHit ? 'charge-limit' : (watchMode && seeding ? 'baseline-cap' : 'max-results'))
    : null;
  const pairSummary = {
    app: appId,
    country,
    status,
    scanned: res.got,
    delivered,
    filteredOut: res.filteredOut,
    // What Apple says the app has in this storefront. Only present when the metadata lookup was
    // already made for this pair (includeInfo); null means "not asked", NOT "no ratings".
    declaredRatingCount: res.declaredRatingCount,
    complete: res.storefrontError ? null : incompleteReason === null,
    incompleteReason,
    scanDepthCap: res.scanCap ?? null,
    feedStopPage: res.feedStopPage ?? null,
    reason: res.storefrontError ?? null,
    ...extra,
  };
  pairOutcomes.push(pairSummary);
}
// Reviews Apple served this run across every pair, BEFORE filters and before watch-mode
// de-duplication -- i.e. how much data the upstream feed produced at all. Zero here (with pairs
// actually attempted) is what triggers the upstream-outage probe below.
let feedServed = 0;
let pairsAttempted = 0;
// Every (app,country) pair this run is supposed to visit, and the ones it actually reached. An
// early stop (maxResults / the buyer's charge limit / SEED_CAP) breaks out of both loops and leaves
// the rest of these pairs in NO per-pair bucket, so only this difference can report them.
const plannedPairs = apps
  .map(parseId)
  .filter(Boolean)
  .flatMap((id) => countries.map((c) => `${id}/${c}`));
const attemptedPairs = new Set();
let keepGoing = true;
for (const app of apps) {
  if (!keepGoing) break;
  const appId = parseId(app);
  if (!appId) {
    log.warning(`Cannot parse app id from "${app}"`);
    // Recorded, not just logged: an unreadable input is the one shortfall that leaves no trace
    // anywhere else — it never reaches plannedPairs, so "notReached" below cannot report it either.
    const pairSummary = {
      app: String(app), country: null, status: 'badAppId', scanned: 0, delivered: 0, filteredOut: 0,
      declaredRatingCount: null, complete: null, incompleteReason: null, scanDepthCap: null,
      feedStopPage: null, reason: 'could not parse an App Store app id from this input value',
    };
    pairOutcomes.push(pairSummary);
    continue;
  }
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
    attemptedPairs.add(`${appId}/${country}`);
    const res = await scrapeAppCountry(appId, country, {}, pairSeeding);
    const { got, filteredOut, capReached, newForPair, storefrontError, feedCeiling, feedStopPage } = res;
    if (ratingSort) await flushPairBuffer();
    if (storefrontError) {
      // Apple refused this (app, storefront) outright. Report the fault verbatim and move on: do
      // NOT run probeStorefronts, do NOT count it as "Apple's feed is empty" (it is not), and —
      // same invariant as the errored-store rule in shopify-products-scraper — never mark the pair
      // baselined, or the next watch run would treat its whole review history as already delivered.
      storefrontErrorPairs.push(`${appId}/${country}`);
      if (!storefrontErrorMessages.includes(storefrontError)) storefrontErrorMessages.push(storefrontError);
      feedServed += got;
      recordPair(appId, country, res, pushed - pushedBefore, 'error');
      continue;
    }
    log.info(`${appId}/${country}: ${got} reviews fetched, ${pushed - pushedBefore} kept after filters`);
    if (feedCeiling && !watchMode) {
      feedCeilingPairs.push(`${appId}/${country}`);
      log.warning(
        `${appId}/${country}: Apple's public review RSS stopped serving at page ${feedStopPage} after a FULL page, so `
        + `this pair returned ${got} review(s) and no more. That is the feed's own limit, not this app running out of `
        + `reviews — older reviews exist that Apple does not expose here, and raising "maxReviewsPerApp" cannot reach `
        + `them. Add more storefronts to "countries" for wider coverage, or schedule the Actor in watchMode to collect `
        + `new reviews over time.`,
      );
    }
    if (feedCeiling && watchMode && pairSeeding) {
      // A baseline that Apple truncated is not a broken baseline — the date floor recorded above
      // keeps the reviews it could not reach from coming back as "new" — but the buyer should know
      // their watch only covers reviews newer than the ones it managed to scan.
      log.warning(
        `${appId}/${country}: Apple's review feed stopped serving at page ${feedStopPage} after a FULL page, so this `
        + `baseline holds the newest ${got} review(s) only. Reviews older than that are recorded as pre-existing and `
        + `will never be delivered or charged as "new" — only reviews posted from now on will be.`,
      );
    }
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
        if (ratingSort) await flushPairBuffer();
        totalNewForPair += fb2.newForPair;
        totalGot += fb2.got;
        log.info(`${appId}/${fb} (fallback): ${fb2.got} reviews fetched, ${pushed - pushedBefore} kept after filters`);
        if (fb2.feedCeiling && !watchMode) {
          feedCeilingPairs.push(`${appId}/${fb}`);
          log.warning(`${appId}/${fb} (fallback): Apple's public review RSS stopped serving at page ${fb2.feedStopPage} after a full page, so this pair returned ${fb2.got} review(s) — older reviews exist but Apple's public feed does not serve them.`);
        }
        if (fb2.capReached && fb2.filteredOut > 0) {
          depthCappedPairs.push(`${appId}/${fb}`);
          log.warning(
            `${appId}/${fb} (fallback): scanned the maxReviewsPerApp limit of ${perApp} review(s) and ${fb2.filteredOut} `
            + `of them were excluded by the review filters (rating/keyword/length/votes/date) — raise maxReviewsPerApp to search deeper.`,
          );
        }
        if (fb2.got > 0) {
          feedServed += totalGot;
          if (watchMode && pairSeeding && keepGoing) { seededPairs.add(pairKey); commitSeedFloors(appId); }
          // The record is keyed to the storefront that ACTUALLY answered, with the requested one
          // alongside — otherwise a `de` row in the summary would claim coverage `de` never gave.
          recordPair(appId, fb, fb2, pushed - pushedBefore, pairSeeding ? 'watchBaselined' : 'ok', { requestedCountry: country, fallbackUsed: true });
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
    if (watchMode && pairSeeding && keepGoing) { seededPairs.add(pairKey); commitSeedFloors(appId); }
    // "The scan window was saturated": every review it looked at was new, AND the window was cut
    // short by something rather than running out of reviews — the buyer's own cap (capReached) or
    // Apple quitting mid-feed (feedCeiling). This used to test `totalGot >= WATCH_SCAN_CAP`, i.e.
    // 500 reviews in one pair, which Apple's feed can no longer deliver (measured 2026-09-22: it
    // commonly stops after page 1), so the warning had become unfirable exactly when the feed
    // ceiling made it most likely to be true — same class as the h255/h257 silent shortfall.
    if (watchMode && !pairSeeding && (capReached || feedCeiling) && totalNewForPair > 0 && totalNewForPair === totalGot) {
      saturatedPairs.push(pairKey);
      log.warning(`${pairKey}: every matching review in the scanned window was new, so reviews posted since the last run may have been missed further back — ${feedCeiling ? "Apple's feed stopped serving mid-walk, so run the watch more often (raising maxReviewsPerApp cannot reach deeper)" : 'run the watch more often, or raise maxReviewsPerApp'}.`);
    }
    const delivered = pushed - pushedBefore;
    // "empty" and "filteredOut" are kept apart for the same reason the status message keeps them
    // apart: both deliver zero rows, but one means Apple has nothing and the other means the
    // buyer's own filters removed everything — and only the second is fixable from the input.
    // "watchNoChanges" is a third zero: reviews were there and had already been delivered.
    const status = totalGot === 0 ? 'empty'
      : watchMode && pairSeeding ? 'watchBaselined'
      : delivered === 0 ? (watchMode ? 'watchNoChanges' : 'filteredOut')
      : 'ok';
    recordPair(appId, country, res, delivered, status, watchMode && saturatedPairs.includes(pairKey) ? { watchWindowSaturated: true } : {});
  }
}
// Every pair we tried was REFUSED by Apple (not empty — refused). That is always the input, so say
// so by name and fail, instead of falling through to the outage probe (which would spend ~12 more
// requests on control apps that are fine) or reporting it to the buyer as "no reviews found".
if (pairsAttempted > 0 && storefrontErrorPairs.length === pairsAttempted) {
  await Actor.fail(
    `Apple refused every app/storefront pair in this run (${storefrontErrorPairs.join(', ')}): ${storefrontErrorMessages.join(' ')} `
    + 'Nothing was scraped and nothing was charged. Check "countries" (two-letter ISO-3166-1 alpha-2 storefront '
    + 'codes — the UK is "gb", not "uk") and that the app ids really exist in those storefronts.',
  );
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
// WATCH_KEEP record-cap eviction (h285) -- kept as its own note, deliberately not folded into
// `truncationNote` below: that one is about THIS run's own early stop (maxResults/charge-limit/
// SEED_CAP), a different failure that happens to want a similar name. Empty unless something was
// actually dropped, so it never adds noise to a healthy run.
let evictionNote = '';
if (baselineTruncated > 0) {
  evictionNote = ` WARNING: the watch baseline hit its ${WATCH_KEEP}-entry cap and ${baselineTruncated} oldest `
    + `review id(s) were dropped (${baselineTruncatedTotal} dropped over the life of this label) — they will `
    + 'be returned and charged again as "new" on a future run. Narrow the watch (fewer apps/countries or a '
    + 'stricter filter) so the baseline stays under the cap.';
}
if (floorSkipped) {
  log.info(
    `${floorSkipped} review(s) were older than the deepest review this watch's baseline could scan, so they already `
    + `existed when the baseline was taken and were NOT delivered or charged as new. This happens when Apple's feed `
    + `serves deeper on a later run than it did at baseline time.`,
  );
}
log.info(`Done. Pushed ${pushed} items.${unidentifiedSkipped ? ` Skipped ${unidentifiedSkipped} review(s) with no reviewId (cannot be tracked in watch mode, not charged).` : ''}`);
// An early stop (maxResults, the buyer's pay-per-event charge limit, or the baseline SEED_CAP)
// `break`s out of the pair loops. The pairs left behind are in none of the per-pair buckets
// (emptyPairs/storefrontErrorPairs/filteredOutPairs/depthCappedPairs/saturatedPairs), so without
// this note the run reads as a complete one that simply found less. Same defect and same fix as
// google-play-reviews-scraper (cycle 630). Appended to whatever status message applies.
const pairsNotReached = plannedPairs.filter((p) => !attemptedPairs.has(p));
// A pair the run never got to has no bucket and no log line of its own. Omitting it from the
// summary would let its ABSENCE read as "nothing there" — the same zero-is-ambiguous trap this
// record exists to close — so it is written down explicitly with complete: null.
for (const p of pairsNotReached) {
  const [app, country] = p.split('/');
  const pairSummary = {
    app, country, status: 'notReached', scanned: 0, delivered: 0, filteredOut: 0,
    declaredRatingCount: null, complete: null, incompleteReason: null, scanDepthCap: null,
    feedStopPage: null, reason: 'the run stopped before reaching this app/storefront pair',
  };
  pairOutcomes.push(pairSummary);
}
let truncationNote = '';
if (!keepGoing) {
  const cause = chargeLimitHit
    ? 'your pay-per-event charge limit was reached'
    : pushed >= maxResults
      ? `the maxResults cap (${maxResults}) was reached`
      : watchMode && seeding
        ? `the baseline cap (${SEED_CAP} reviews) was reached`
        : 'the run stopped early';
  // Only claim the pair list was abandoned when it actually was. Hitting the cap on the very last
  // row of the last pair is the common, harmless case and must not be reported as missing pairs.
  truncationNote = ` MAY BE INCOMPLETE: ${cause}.`
    + (pairsNotReached.length
      ? ` The run stopped before finishing the app/storefront list — ${pairsNotReached.length} pair(s) were never fetched and returned nothing: ${pairsNotReached.join(', ')}.`
      : ' Every requested app/storefront pair was fetched, but the last one may have been cut short.')
    + (chargeLimitHit
      ? ' Raise the Actor\'s charge limit and re-run to get the rest.'
      : ` Raise "maxResults" (currently ${maxResults}) and re-run to get the rest.`);
  log.warning(truncationNote.trim());
}

// Apple's 500/app/storefront ceiling, said in the status message rather than only in the log. It
// is deliberately phrased WITHOUT a "raise the cap" suggestion: unlike maxReviewsPerApp/maxResults
// truncation this one cannot be undone from the input, so the honest advice is more storefronts or
// watchMode. Appended (not a branch of its own) so it never displaces an emptier/refused report.
const ceilingNote = feedCeilingPairs.length
  ? ' Apple\'s public review feed stopped serving mid-walk (a full page followed by nothing) for:'
    + ` ${feedCeilingPairs.join(', ')}`
    + ' — these apps have older reviews Apple does not expose here, and no "maxReviewsPerApp" value can reach them.'
    + ' Add more storefronts to "countries" for wider coverage, or schedule this Actor with "watchMode" to collect new reviews as they are posted.'
  : '';

let statusMsg;
if (watchMode && storefrontErrorPairs.length) {
  // Said first in watch mode: a scheduled run whose storefront is broken must not be summarised as
  // the reassuring "nothing new since the last run" — those pairs delivered nothing because Apple
  // refused them, and they were deliberately left out of the baseline.
  statusMsg = (
    `Apple refused ${storefrontErrorPairs.length} app/storefront pair(s) in this run (${storefrontErrorPairs.join(', ')}) — they were NOT baselined and nothing was charged for them. `
    + `${storefrontErrorMessages.join(' ')} Watch label "${watchLabel}": ${pushed} item(s) returned from the pairs that did answer.`
  );
} else if (watchMode && seeding) {
  statusMsg = (`Baseline run for watch label "${watchLabel}": ${watchSeen.size} existing review(s) across ${seededPairs.size} app/country pair(s) recorded, 0 rows returned, 0 charged. Run it again later to get only what's new.`);
} else if (watchMode && pushed === 0) {
  statusMsg = (`Nothing new for watch label "${watchLabel}" since its last run — all ${watchSkipped + floorSkipped} matching review(s) had already been delivered or pre-dated the baseline. That is the expected result most of the time; you were charged for nothing.`);
} else if (watchMode && saturatedPairs.length) {
  statusMsg = (`Pushed ${pushed} new item(s) for watch label "${watchLabel}". ${saturatedPairs.join(', ')}: every matching review in the scanned window was new — older new reviews may have been missed; run the watch more often.`);
} else if (watchMode) {
  statusMsg = (`Watch label "${watchLabel}": ${pushed} new item(s) since the last run (${watchSkipped} already-delivered review(s) skipped, not charged${floorSkipped ? `; ${floorSkipped} older than the baseline scan, treated as pre-existing and not charged` : ''}).`);
} else if (pushed === 0) {
  const why = storefrontErrorPairs.length && !emptyPairs.length
    ? `Apple refused these app/storefront pairs: ${storefrontErrorPairs.join(', ')} — ${storefrontErrorMessages.join(' ')}`
    : depthCappedPairs.length && !emptyPairs.length
    ? `maxReviewsPerApp (${perApp}) was hit before any review passed your review filters (rating/keyword/length/votes/date) for: ${depthCappedPairs.join(', ')} — raise maxReviewsPerApp to search deeper`
    : filteredOutPairs.length && !emptyPairs.length
    ? 'reviews were found but every one was removed by your review filters (rating/keyword/length/votes/date)'
    : `Apple's review feed returned nothing for: ${emptyPairs.join(', ')} (try another storefront in "countries")`;
  statusMsg = (`No reviews returned — ${why}. See the log for details.`);
} else if (depthCappedPairs.length) {
  statusMsg = (`Pushed ${pushed} reviews. maxReviewsPerApp (${perApp}) was hit while filtering: ${depthCappedPairs.join(', ')} — some matching reviews may sit deeper in the feed; raise maxReviewsPerApp to search further.`);
} else if (emptyPairs.length || storefrontErrorPairs.length) {
  statusMsg = (
    `Pushed ${pushed} reviews.${emptyPairs.length ? ` Empty Apple feed for: ${emptyPairs.join(', ')}.` : ''}`
    + `${storefrontErrorPairs.length ? ` Apple refused: ${storefrontErrorPairs.join(', ')} (check the storefront code and the app id).` : ''}`
  );
} else if (truncationNote || ceilingNote) {
  // A clean run that nothing else had to report, EXCEPT that it stopped early or that Apple's own
  // feed ceiling cut it off — previously both cases set no status message at all and a run that
  // returned 500 of an app's 1.8M reviews read exactly like a complete one.
  statusMsg = `Pushed ${pushed} reviews.`;
}
if (statusMsg) await Actor.setStatusMessage((statusMsg + truncationNote + ceilingNote + evictionNote).slice(0, 1000));

// The pair records, on a surface every run has whether or not the buyer configured a webhook:
// GET /v2/actor-runs/<runId>/key-value-store/records/RUN_SUMMARY. Best-effort — a failure here
// must never fail a run whose rows are already delivered and charged.
// Run-level completeness, so a consumer can read `complete` here exactly as it does on the other
// RUN_SUMMARY Actors in the fleet instead of having to know this one reports per pair. Derived
// only from the pair records below -- no new claim is made here that `pairs` does not already
// carry. Any pair that is not `complete === true` makes the RUN incomplete: an unknown pair
// (storefront error, never reached) means reviews the buyer asked for are definitively absent
// from the dataset, which is incompleteness, not uncertainty.
const runComplete = pairOutcomes.length ? pairOutcomes.every((p) => p.complete === true) : null;
// First-cause-wins, same convention as the rest of the fleet: report the FIRST pair that fell
// short, not the last one to be noticed. Pairs whose own `incompleteReason` is null (refused or
// never attempted) get a reason derived from their status, because "no reason recorded" must not
// read as "nothing wrong".
const firstShort = runComplete === false ? pairOutcomes.find((p) => p.complete !== true) : null;
const STATUS_REASON = { error: 'storefront-error', badAppId: 'bad-app-id', notReached: 'not-reached' };
const runIncompleteReason = !firstShort ? null
  : (firstShort.incompleteReason ?? STATUS_REASON[firstShort.status] ?? 'pair-incomplete');
const shortPairs = pairOutcomes.filter((p) => p.complete !== true).length;
const runSummary = {
  finishedAt: new Date().toISOString(),
  pushed,
  pairsPlanned: plannedPairs.length,
  pairsAttempted,
  // `pairsIncomplete` counts only pairs we KNOW fell short (complete === false). `pairsUnknown`
  // counts the ones with no completeness to report at all (complete === null) -- without it, a run
  // in which every pair was refused reads as `pairsIncomplete: 0`, i.e. "nothing wrong".
  pairsIncomplete: pairOutcomes.filter((p) => p.complete === false).length,
  pairsUnknown: pairOutcomes.filter((p) => p.complete === null).length,
  complete: runComplete,
  incompleteReason: runIncompleteReason,
  incompleteDetail: firstShort
    ? `${firstShort.app}/${firstShort.country}: ${firstShort.incompleteReason ?? firstShort.reason ?? firstShort.status}`
      + (shortPairs > 1 ? ` (and ${shortPairs - 1} other pair(s); see \`pairs\`)` : '')
    : null,
  watchLabel: watchMode ? watchLabel : null,
  watchSeeding: watchMode ? seeding : null,
  // >0 means the baseline lost ids to the WATCH_KEEP cap and a future run will re-deliver and
  // re-charge them as "new" (h285). null outside watch mode, where there is no baseline.
  baselineTruncated: watchMode ? baselineTruncated : null,
  baselineTruncatedTotal: watchMode ? baselineTruncatedTotal : null,
  pairs: pairOutcomes,
};
try {
  await Actor.setValue('RUN_SUMMARY', runSummary);
} catch (err) {
  log.warning(`Could not write RUN_SUMMARY to the key-value store (${err.message}); run result is unaffected.`);
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
    watchPreBaselineSkipped: watchMode ? floorSkipped : null,
    watchSeeding: watchMode ? seeding : null,
    baselineTruncated: runSummary.baselineTruncated,
    baselineTruncatedTotal: runSummary.baselineTruncatedTotal,
    pairsIncomplete: runSummary.pairsIncomplete,
    pairsUnknown: runSummary.pairsUnknown,
    complete: runSummary.complete,
    incompleteReason: runSummary.incompleteReason,
    incompleteDetail: runSummary.incompleteDetail,
    pairs: pairOutcomes,
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
