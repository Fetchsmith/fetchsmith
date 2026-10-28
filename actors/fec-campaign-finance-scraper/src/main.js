// FEC Campaign Finance Scraper: candidates + financial totals, or individual donor contributions
// (Schedule A), via api.open.fec.gov. Uses a personal api.data.gov key (env var FEC_API_KEY, set as
// a secret Actor env var, not committed) with a DEMO_KEY fallback for local runs.
import { createHash } from 'crypto';
import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';

await Actor.init();
// Soft-deadline guard (same pattern as sam-gov-opportunities-scraper/eu-ted-tenders-scraper,
// 24th Actor on the rollout). Two reachable paths into a hard kill here: the paged walk itself
// (up to 500 maxResults worth of pages, each with got's own retry.limit:2 backoff on a timeout
// or 429/5xx) and, in candidates mode with includeTotals on, a `fetchTotals()` network call for
// EVERY delivered candidate row. A hard kill is not a billing loss (pushResult charges per row
// as it goes) -- it is the writes AFTER the walk: RUN_SUMMARY, and above all the watch-state
// `watchStore.setValue`, so a watch-mode buyer whose run is killed loses their baseline and gets
// re-charged for the whole result set on the next run. Stop proactively with a margin and flush
// instead.
const timeoutAt = Actor.getEnv().timeoutAt?.getTime() ?? null;
const TIME_BUDGET_MARGIN_MS = 45_000;
function remainingMs() { return timeoutAt == null ? Infinity : timeoutAt - Date.now() - TIME_BUDGET_MARGIN_MS; }
function timeBudgetOk() { return remainingMs() > 0; }
let timeBudgetHit = false;
const input = (await Actor.getInput()) ?? {};
const MODES = ['candidates', 'contributions', 'disbursements', 'independentExpenditures'];
const searchMode = MODES.includes(input.searchMode) ? input.searchMode : 'candidates';
// The three transaction schedules (A receipts / B disbursements / E independent expenditures)
// share the same paging, amount-window, date-window and watch machinery -- only the endpoint,
// the query params and the row shape differ.
const isTxnMode = searchMode !== 'candidates';
// The "Warren" demo value is applied further down, once state/office/party/electionYear are
// parsed -- it must NOT be a schema `default` (see the note at that fallback).
let candidateName = (input.candidateName ?? '').trim();
const donorName = (input.donorName ?? '').trim();
const donorEmployer = (input.donorEmployer ?? '').trim();
const donorOccupation = (input.donorOccupation ?? '').trim();
const donorCity = (input.donorCity ?? '').trim();
const donorZip = (input.donorZip ?? '').trim();
const recipientName = (input.recipientName ?? '').trim();
const payeeName = (input.payeeName ?? '').trim();
const candidateId = (input.candidateId ?? '').trim().toUpperCase();
const committeeIdInput = (input.committeeId ?? '').trim().toUpperCase();
const supportOppose = ['S', 'O'].includes(String(input.supportOppose ?? '').trim().toUpperCase())
  ? String(input.supportOppose).trim().toUpperCase()
  : '';
const minAmount = input.minAmount ? Number(input.minAmount) : undefined;
const maxAmount = input.maxAmount ? Number(input.maxAmount) : undefined;
// A bad date bound THROWS (cycle 591). It used to warn and return undefined, which deleted the
// bound from the query entirely: the run then succeeded, returned the whole unfiltered set, and
// billed per result for rows the caller never asked for. Judge a failed parse by whether ignoring
// it narrows or widens the result set -- widening under per-result pricing must stop the run, and
// a log.warning in an otherwise-successful run is not a fix because nobody reads it.
function parseFecDate(s, label) {
  const trimmed = String(s ?? '').trim();
  if (!trimmed) return undefined;
  // The ISO round-trip is what rejects calendar-invalid dates that the regex accepts: V8 silently
  // rolls "2024-02-30" over to March 1 (even in the full ISO form), so comparing the normalized
  // date back to the input is the only cheap check that catches it.
  const shaped = /^\d{4}-\d{2}-\d{2}$/.test(trimmed);
  const d = shaped ? new Date(`${trimmed}T00:00:00.000Z`) : null;
  if (!shaped || Number.isNaN(d.getTime()) || d.toISOString().slice(0, 10) !== trimmed) {
    throw new Error(
      `"${label}" is not a valid date: "${trimmed}". Use YYYY-MM-DD (e.g. 2024-01-31). `
      + 'The run stops instead of ignoring the bound, because dropping it would widen the search '
      + 'to every matching row and charge you for the difference.',
    );
  }
  return trimmed;
}
const contributionDateFrom = parseFecDate(input.contributionDateFrom, 'contributionDateFrom');
const contributionDateTo = parseFecDate(input.contributionDateTo, 'contributionDateTo');
if (contributionDateFrom && contributionDateTo && contributionDateFrom > contributionDateTo) {
  throw new Error(`contributionDateFrom (${contributionDateFrom}) is after contributionDateTo (${contributionDateTo}).`);
}
const state = (input.state ?? '').trim().toUpperCase();
const office = (input.office ?? '').trim().toUpperCase();
const party = (input.party ?? '').trim().toUpperCase();
// The FEC's Schedule A endpoint times out on a full-table scan without this filter, so
// contributions mode always sends one (defaulting to the most recent even year), while
// candidates mode leaves it unset ("all cycles") unless the caller asks for one.
const currentEvenYear = new Date().getUTCFullYear() - (new Date().getUTCFullYear() % 2);
const electionYear = input.electionYear
  ? Number(input.electionYear)
  : (isTxnMode ? currentEvenYear : undefined);

// `candidateName` carried a schema `default: "Warren"` until cycle 1908. Apify merges a schema
// default into EVERY run that omits the field, so `{"state":"MA","office":"S"}` was silently
// searching `q=Warren` on top of those filters and returning 2 rows where the real match set is
// 146 (measured against the FEC API directly) -- the caller never asked for Warren and got no
// warning. Same class as nih-reporter's `keyword` (1904), court-records' `query` (1905),
// clinicaltrials' `conditions` (1906) and hacker-news' `queries`/`tags` (1907). The demo value
// now lives here instead, applied only when the field is genuinely absent AND the run carries no
// other candidates-mode scope -- so a bare `{}` (the Store's "run with default input" path) still
// returns real rows, while any real filter is honoured as written. The `undefined` test is what
// makes this work, so the schema must keep `prefill` and never regain `default`. The sibling
// scope fields are safe to test by truthiness: their schema defaults are empty strings (1907's
// co-defaulted-sibling trap only bites when a sibling's merged default is itself truthy).
// Unlike the four Actors above, this field is read in ONE mode only (`candidates`, as `q`) -- the
// three transaction schedules never send it -- so the gate is scoped to that mode's own filters.
if (input.candidateName === undefined && searchMode === 'candidates'
  && !state && !office && !party && electionYear === undefined) {
  candidateName = 'Warren';
  log.info('No candidateName or state/office/party/electionYear filter set -- searching the demo value "Warren". Set candidateName, or any of those filters, to search for something else.');
}

// `committee_id` is a fast, indexed filter on Schedules B and E but reliably 504s on Schedule A
// (confirmed live in cycle 410 on both a large and a small committee), so it is accepted only
// where it actually works rather than silently producing a failed run.
const committeeId = committeeIdInput && (searchMode === 'disbursements' || searchMode === 'independentExpenditures')
  ? committeeIdInput
  : '';
if (committeeIdInput && !committeeId) {
  log.warning(`Ignoring committeeId "${committeeIdInput}": it is only supported in searchMode "disbursements" and "independentExpenditures" (the FEC's Schedule A endpoint times out on this filter).`);
}
for (const [field, value, modes] of [
  ['recipientName', recipientName, ['disbursements']],
  ['payeeName', payeeName, ['independentExpenditures']],
  ['candidateId', candidateId, ['independentExpenditures']],
  ['supportOppose', supportOppose, ['independentExpenditures']],
  ['donorName', donorName, ['contributions']],
  ['donorEmployer', donorEmployer, ['contributions']],
  ['donorOccupation', donorOccupation, ['contributions']],
  ['donorCity', donorCity, ['contributions']],
  ['donorZip', donorZip, ['contributions']],
  ['office', office, ['candidates']],
  ['party', party, ['candidates']],
  ['candidateName', candidateName, ['candidates']],
  ['state', state, ['candidates', 'contributions', 'disbursements']],
]) {
  if (value && !modes.includes(searchMode)) {
    log.warning(`Ignoring ${field} "${value}": it only applies in searchMode ${modes.map((m) => `"${m}"`).join('/')}, and this run is in "${searchMode}" mode.`);
  }
}
// `includeTotals` is read only in the candidates-mode branch (it fetches each candidate's FEC
// totals, an extra request per row). The comment this replaced claimed checking the raw
// `input.includeTotals !== undefined` would skip an omitted field, but Apify merges the schema
// default (`true`) into `input` on EVERY run that omits it (cycle 2204's trap on
// apple-podcasts-scraper, confirmed live here cycle 2234: a run that never mentioned the field
// still arrived with `input.includeTotals === true`) -- so that check fired on every single
// non-candidates-mode run, which is most of this Actor's traffic. Only an explicit `false`
// (the one value distinguishable from the default) is a real signal.
if (input.includeTotals === false && searchMode !== 'candidates') {
  log.warning(`Ignoring "includeTotals": it only applies in searchMode "candidates" (it fetches financial totals for each candidate found), and this run is in "${searchMode}" mode.`);
}
if (searchMode === 'candidates') {
  // Mirror image of the loop above: these four apply only to the transaction modes (their
  // schema descriptions say so), so a caller setting them in candidates mode gets a silently
  // unfiltered candidate list unless this warns -- same defect shape as the loop above and as
  // steam-reviews-scraper's games-mode filters (cycle 988).
  if (minAmount !== undefined) {
    log.warning(`Ignoring minAmount ${minAmount}: it only applies in searchMode "contributions"/"disbursements"/"independentExpenditures", and this run is in "candidates" mode.`);
  }
  if (maxAmount !== undefined) {
    log.warning(`Ignoring maxAmount ${maxAmount}: it only applies in searchMode "contributions"/"disbursements"/"independentExpenditures", and this run is in "candidates" mode.`);
  }
  if (contributionDateFrom) {
    log.warning(`Ignoring contributionDateFrom "${contributionDateFrom}": it only applies in searchMode "contributions"/"disbursements"/"independentExpenditures", and this run is in "candidates" mode.`);
  }
  if (contributionDateTo) {
    log.warning(`Ignoring contributionDateTo "${contributionDateTo}": it only applies in searchMode "contributions"/"disbursements"/"independentExpenditures", and this run is in "candidates" mode.`);
  }
}
// The FEC's Schedule A endpoint (contributions mode) does a near-full-table scan when none of its
// narrowing filters are set -- confirmed live (run `FDFhr3vZKyXrgJ3Ru`, cycle 856): it 504s on plain
// curl and blows fecGet's 30s request budget on page 1, so an unfiltered run would otherwise fail
// anyway with a bare `Timeout awaiting 'request' for 30000ms` and no hint why. Fail fast with a
// named remedy instead of issuing the doomed request. Kept conditional on this exact emptiness
// test -- an unconditional "narrow your filters" message is the unreachable/unconditional-remedy
// defect shape cycles 836/837 shipped fixes for across 4 Actors.
if (searchMode === 'contributions' && !donorName && !donorEmployer && !donorOccupation && !donorCity
  && !donorZip && !state && minAmount === undefined && maxAmount === undefined
  && !contributionDateFrom && !contributionDateTo) {
  throw new Error(
    'searchMode "contributions" with no narrowing filter set matches roughly 173 million rows -- '
    + "the FEC's own API times out serving page 1 of that scan, so this run would fail anyway after "
    + 'burning its request budget. Set at least one of: donorName, donorEmployer, donorOccupation, '
    + 'donorCity, donorZip, state, minAmount, maxAmount, contributionDateFrom, contributionDateTo.',
  );
}
const includeTotals = input.includeTotals ?? true;
const maxResults = Math.min(Number(input.maxResults ?? 20), 500);
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

const isPPE = Actor.getChargingManager().getPricingInfo().isPayPerEvent;
let pushed = 0;
// Completeness bookkeeping (cycle 676, h250 class). Before this the Actor could stop early for
// five different reasons -- charge limit, maxResults, SEED_CAP, WATCH_PAGE_CAP, an API error --
// and a pipeline reading the dataset could not tell "that is all there is" from "that is all we
// fetched". `scanned`/`pages`/`declaredMatches` are what make the shortfall measurable.
let scanned = 0;              // raw rows read off the wire, watch-seed walk included
let pages = 0;                // pages actually fetched
let declaredMatches = null;   // pagination.count -- what the FEC says matches these filters. null
                              // means the API never answered with a count; never read it as 0.
let declaredExact = null;     // FEC's own `is_count_exact` flag on that number
let chargeLimitReached = false;
let seedCapHit = false;
let maxResultsReached = false;
let rowsNotReached = 0;       // rows already fetched on the page the walk stopped on, never delivered
let moreAvailable = false;    // a cursor/page was still outstanding when the walk stopped
let runError = null;          // set instead of failing immediately, so the baseline still gets saved
let complete = true;
let incompleteReason = null;
let incompleteDetail = null;

// First cause wins: a walk that stopped because the FEC stopped answering and THEN also hit
// maxResults must keep reporting the upstream failure -- that is the cause the buyer can act on.
function markIncomplete(reason, detail = null) {
  if (!complete) return;
  complete = false;
  incompleteReason = reason;
  incompleteDetail = detail;
}

// Watch mode: a stateful "only new contributions since my last run" filter, scoped to
// contributions mode only -- candidates mode returns the same fixed roster of people, not a
// stream of discrete new events, so "new since last time" has no natural meaning there. The
// baseline (sub_ids already delivered under this label+filter set) lives in a NAMED
// key-value store on the buyer's own account so it survives across runs (the default KV
// store is per-run and would reset every time). electionYear defaults to a rolling
// "current even year" when left empty (see the comment above); the fingerprint uses the
// buyer's RAW input for it, not the resolved value, so a watch set up without an explicit
// year doesn't silently re-seed every two years when the default rolls forward.
const WATCH_STORE = 'fetchsmith-fec-watch';
const SEED_CAP = 5000; // bound the cost of a baseline run against a broad donor/employer filter
const WATCH_KEEP = 20000; // bound the record size; oldest ids fall off first
const WATCH_PAGE_CAP = 1000; // safety valve: a broad/unfiltered watch could otherwise page through the whole multi-hundred-thousand-row Schedule A table every run
let baselineTruncated = 0; // ids dropped by WATCH_KEEP this run -- they come back as "new" and get charged
let baselineTruncatedTotal = 0; // same, cumulative over the life of this label

function watchKeyFor(label, criteria) {
  const safe = label.toLowerCase().replace(/[^a-z0-9_.-]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 40) || 'default';
  const fp = createHash('sha1').update(JSON.stringify(criteria, Object.keys(criteria).sort())).digest('hex').slice(0, 10);
  return { key: `watch-${safe}-${fp}`, fingerprint: fp };
}

let watchMode = watchLabel.length > 0;
if (watchMode && !isTxnMode) {
  log.warning(`watchLabel "${watchLabel}" is ignored in candidates mode -- watch mode only applies to the transaction modes ("contributions", "disbursements", "independentExpenditures"), which return a stream of discrete new filings; candidates mode always returns the same fixed roster.`);
  watchMode = false;
}
let watchStore = null;
let watchKey = null;
let watchRecord = null;
let seeding = false;
let watchSkipped = 0;
const watchSeen = new Set(); // sub_ids already delivered under this label+fingerprint

if (watchMode) {
  const criteria = {
    // Unconditional, deliberately bumped this cycle (not gated behind a filter check like the
    // fields below): v0.1.6 re-keys watchId from `sub_id` to `committeeId:transactionId` (see
    // README "Dedup key change"), and the two key spaces share no ids at all -- an old
    // `sub_id`-keyed baseline treated as still-valid under the new key would see every one of
    // its own already-seen rows as "new" and charge for the whole thing again. Bumping this
    // forces every pre-v0.1.6 baseline onto a fresh fingerprint, so its first post-upgrade run is
    // a free re-seed (0 charged) instead of a full incremental re-delivery.
    dedupKeyVersion: 2,
    donorName, donorEmployer, state, minAmount: minAmount ?? null, electionYearRaw: input.electionYear ?? null,
    // Added cycle 459. Only present when set, same rule as maxAmount/contributionDate* below --
    // a watch baseline saved before this cycle keeps its fingerprint instead of silently re-seeding.
    ...(donorOccupation ? { donorOccupation } : {}),
    ...(donorCity ? { donorCity } : {}),
    // Added cycle 461. Only present when set, same rule as donorOccupation/donorCity above.
    ...(donorZip ? { donorZip } : {}),
    ...(maxAmount !== undefined ? { maxAmount } : {}),
    ...(contributionDateFrom ? { contributionDateFrom } : {}),
    ...(contributionDateTo ? { contributionDateTo } : {}),
    // Added cycle 428. Only present when NOT the original contributions mode, so every watch
    // baseline saved before this cycle keeps its fingerprint instead of silently re-seeding
    // (same rule as maxAmount/contributionDate* above and steam's includeOffTopic, cycle 404).
    ...(searchMode !== 'contributions' ? { searchMode } : {}),
    ...(recipientName ? { recipientName } : {}),
    ...(payeeName ? { payeeName } : {}),
    ...(candidateId ? { candidateId } : {}),
    ...(committeeId ? { committeeId } : {}),
    ...(supportOppose ? { supportOppose } : {}),
  };
  watchStore = await Actor.openKeyValueStore(WATCH_STORE);
  const { key, fingerprint } = watchKeyFor(watchLabel, criteria);
  watchKey = key;
  const existing = await watchStore.getValue(key);
  if (existing && Array.isArray(existing.seenIds)) {
    watchRecord = existing;
    for (const id of existing.seenIds) watchSeen.add(String(id));
    log.info(
      `Watch mode "${watchLabel}" (${key}): baseline from ${existing.lastRunAt ?? 'an earlier run'} holds `
      + `${watchSeen.size} already-delivered contribution(s). Only ones NOT in that baseline will be returned and charged.`,
    );
  } else {
    watchRecord = { fingerprint, firstSeededAt: new Date().toISOString(), runCount: 0 };
    seeding = true;
    log.info(
      `Watch mode "${watchLabel}" (${key}): FIRST run for this label and filter set, so this is a baseline `
      + 'run. It records which contributions already match and returns ZERO results (you are charged nothing). '
      + 'Run it again on the same label and filters -- on a schedule, typically -- to get only what is new since now.',
    );
  }
}

// contributionDateTo is an UPPER bound on the transaction date and is sent to the FEC as its own
// `max_date` param (see buildParams below) in all three transaction modes -- confirmed live
// 2026-10-11 against api.open.fec.gov (contributor_employer=GOOGLE, min_date=2026-09-01: 7 rows
// through 2026-09-30 unbounded vs 4 rows through 2026-09-10 with max_date=2026-09-10 set, the two
// newest rows dropped). A watch's whole purpose is to catch activity AS IT HAPPENS, and real-world
// contribution/disbursement/expenditure dates keep advancing with real time -- so once today's
// date moves past contributionDateTo, every genuinely current transaction is excluded by the FEC's
// own API before this Actor ever sees it, and the watch goes quiet for good. Unlike an upper bound
// on a podcast's release date, this is not ABSOLUTELY dead: a transaction can be filed late (an
// original filing, not an amendment -- amendments keep the same transaction_id and would already
// be in watchSeen) with a date at or before the cutoff, and that would still be caught. But the
// watch's main promise -- alerting on new activity going forward -- stops working permanently once
// real time passes the bound. contributionDateFrom is safe in a watch run: a lower bound only
// limits how far back the first baseline reaches (same rule as minReleaseDate in
// apple-podcasts-scraper).
const watchPastDateBound = watchMode && contributionDateTo != null;
if (watchPastDateBound) {
  log.warning(
    `watchLabel "${watchLabel}" is set together with contributionDateTo "${input.contributionDateTo}". `
    + 'contributionDateTo is an UPPER bound on the transaction date, sent to the FEC as `max_date`, so once '
    + "today's date moves past it, every genuinely new contribution/disbursement/expenditure is excluded "
    + 'before this Actor ever sees it -- the watch will go quiet and stay quiet. (A late-filed original '
    + 'transaction dated at or before the cutoff can still be caught; ongoing new activity cannot.)',
  );
  log.warning(
    'What to do: drop contributionDateTo from the watch run -- watch mode already returns only what is new, '
    + 'so an upper date bound adds nothing but a future dead end. contributionDateFrom is safe to keep (a '
    + 'lower bound only limits how far back the first baseline reaches).',
  );
}

async function saveWatchRecord(status) {
  const all = Array.from(watchSeen);
  const ids = all.slice(-WATCH_KEEP);
  // An id past the record cap is not forgotten harmlessly: the next run does not find it in the
  // baseline, so it is delivered and CHARGED again even though the buyer already paid for it.
  // The dropped end is oldest-FIRST-SEEN (re-seeing an id is a Set no-op and doesn't move it).
  baselineTruncated = all.length - ids.length;
  baselineTruncatedTotal = (watchRecord.truncatedTotal ?? 0) + baselineTruncated;
  if (baselineTruncated > 0) {
    log.warning(
      `The baseline for "${watchLabel}" exceeded the ${WATCH_KEEP}-entry record cap; the ${baselineTruncated} `
      + 'oldest contribution/disbursement/expenditure id(s) were dropped and will be returned and CHARGED as '
      + `new on a future run (${baselineTruncatedTotal} dropped over the life of this label). Narrow `
      + 'donorName/donorEmployer/donorOccupation/donorCity/donorZip/state/minAmount/maxAmount/'
      + 'contributionDateFrom/contributionDateTo, or split it across several labels, so the baseline stays under the cap.',
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
    seenIds: ids,
  });
}

// OpenFEC reissues a brand-new sub_id for every row on a report -- even an unchanged one --
// the moment the report is amended in any way, so sub_id is unsafe as a watch dedup key (it
// would re-deliver, and re-charge for, the whole report on every amendment). transaction_id is
// the filer's own id and is documented (and confirmed live) to stay stable across amendments of
// the same transaction; committee_id disambiguates in the rare case two committees reuse one.
function watchKeyOf(c) {
  const committeeId = c.committee_id ?? c.committee?.committee_id ?? null;
  if (committeeId == null || c.transaction_id == null) return null;
  return `${committeeId}:${c.transaction_id}`;
}

async function pushResult(item, watchId) {
  if (watchMode && watchId != null && seeding) {
    watchSeen.add(String(watchId));
    if (watchSeen.size >= SEED_CAP) { seedCapHit = true; return false; }
    return true;
  }
  if (watchMode && watchId != null && watchSeen.has(String(watchId))) {
    watchSkipped += 1;
    return true;
  }
  if (isPPE) {
    const r = await Actor.charge({ eventName: 'result', count: 1 });
    // chargedCount 0 and eventChargeLimitReached are both the charge limit, not the end of the
    // data -- without this flag the run stops at the same place a complete run would and the
    // dataset looks finished.
    if (r.chargedCount === 0) { chargeLimitReached = true; return false; }
    await Actor.pushData(item); pushed += 1;
    if (watchMode && watchId != null) watchSeen.add(String(watchId));
    if (r.eventChargeLimitReached) { chargeLimitReached = true; return false; }
    if (pushed >= maxResults) { maxResultsReached = true; return false; }
    return true;
  }
  await Actor.pushData(item); pushed += 1;
  if (watchMode && watchId != null) watchSeen.add(String(watchId));
  if (pushed >= maxResults) { maxResultsReached = true; return false; }
  return true;
}

const API_BASE = 'https://api.open.fec.gov/v1';
const API_KEY = process.env.FEC_API_KEY ?? 'DEMO_KEY';
// Cycle 2362 flagged that this secret has never been confirmed end-to-end to reach the running
// container (the `?? 'DEMO_KEY'` fallback would mask that failure identically, same shape as the
// CL_API_TOKEN gotcha that cycle found). Log which one is active -- cheap, permanent, and lets any
// future cycle check a run's log instead of re-deriving this.
log.info(API_KEY === 'DEMO_KEY'
  ? 'FEC_API_KEY env var not set -- using the public DEMO_KEY fallback (x-ratelimit-limit 10, per egress IP, measured 2026-10-28).'
  : 'Using FEC_API_KEY (this Actor\'s own personal api.data.gov key).');

async function fecGet(path, params) {
  const url = new URL(API_BASE + path);
  url.searchParams.set('api_key', API_KEY);
  for (const [k, v] of Object.entries(params)) {
    if (v === undefined || v === '') continue;
    // OpenFEC's own convention for "match any of these" is a repeated query param
    // (candidate_id=A&candidate_id=B), not a comma-joined value -- verified live against
    // /v1/candidates/ (cycle 1937, resolving a committee's multi-candidate_ids list).
    if (Array.isArray(v)) { for (const item of v) url.searchParams.append(k, item); } else url.searchParams.set(k, v);
  }
  // got-scraping defaults to throwHttpErrors:false (verified live 2026-09-24: a 403/422/404
  // arrives as an ordinary RESOLVED response, never a thrown error). Set explicitly because the
  // status check below depends on it. Until cycle 752 this function relied on got throwing and
  // inspected `err.response?.statusCode` in a catch -- code that could never run, so every 4xx/5xx
  // was returned to the caller as a normal body. The page walk reads `body.results ?? []`, sees an
  // empty page and `break`s, so a mid-walk 429 ended the run as "complete" with partial data and
  // no warning; `fetchTotals` turned one into "no money on file". Check the status directly.
  let res;
  // Capped at remainingMs() (never below a 1s floor so the request can still be attempted once)
  // so neither the request itself nor got's own retry backoff below can run the clock past the
  // margin -- without this, a single timed-out call plus its 2 built-in retries could burn up to
  // ~90s (3 x 30s), more than the whole margin. Kept outside the gotScraping call so the catch
  // below can tell whether IT, not FEC, is what cut the request short.
  const requestTimeoutMs = Math.max(Math.min(30000, remainingMs()), 1000);
  try {
    res = await gotScraping({
      url: url.toString(),
      timeout: { request: requestTimeoutMs },
      retry: {
        limit: 2,
        // enforceRetryRules defaults to false, so computedValue 0 (the default rules already
        // said "don't retry" -- e.g. attempt limit reached, non-retriable error) must still be
        // honoured here, not overridden into a retry just because time remains.
        calculateDelay: ({ computedValue }) => (
          computedValue === 0 || !timeBudgetOk() ? 0 : Math.min(computedValue, Math.max(remainingMs(), 0))
        ),
      },
      responseType: 'json',
      throwHttpErrors: false,
    });
  } catch (err) {
    // A single broad free-text value on contributor_employer/contributor_occupation (schedule_a)
    // or the equivalent schedule_b/e fields, with no other narrowing filter, makes OpenFEC scan
    // enough rows that ITS OWN server-side query enforces a ~30s cap and 504s -- verified live
    // 2026-09-30 directly against api.open.fec.gov for donorOccupation values as ordinary as
    // "PHYSICIAN"/"ATTORNEY"/"RETIRED"/"TEACHER" and donorEmployer "SELF-EMPLOYED"/"RETIRED"/
    // "NONE" (all four, alone, 504 "Query timed out" consistently at ~30.7s; a specific employer
    // like "GOOGLE" -- 129,917 matches -- returns in ~4s, so it is query BREADTH, not the field,
    // that decides this). Our client `timeout.request` is also 30000ms, so got's own TimeoutError
    // fires first (a bare, unhandled "Timeout awaiting 'request' for 30000ms" stack trace) before
    // the 504 body would ever be readable, and `retry.limit:2` then repeats the SAME doomed
    // request twice more (~90s total) since the cause is deterministic, not transient. Give this
    // its own actionable message instead of an opaque crash -- there is no reliable way to predict
    // in advance which values are "too broad" (a COUNT probe would hit the identical timeout), so
    // this is caught after the fact rather than guarded before the request.
    if (err.name === 'TimeoutError' || err.code === 'ETIMEDOUT') {
      // A real defect caught locally while testing the time-budget guard: capping
      // `requestTimeoutMs` below the full 30s means a perfectly ordinary FEC response (1-3s) can
      // now also time out, purely because WE shortened the budget, not because the filter is
      // broad. Without this check that run reported "employer too broad, narrow your search" --
      // actively wrong advice for a clock stop, and the opposite of what the buyer should do
      // (the real fix is a longer run timeout, not a narrower query).
      if (requestTimeoutMs < 30000) {
        const e = new Error('stopped before the run time budget ran out (request timeout was shortened to fit the remaining budget)');
        e.isTimeBudget = true;
        throw e;
      }
      const e = new Error(
        `The FEC API took too long to respond and timed out. This usually means a free-text `
        + `filter value (donorEmployer, donorOccupation, donorName, recipientName or payeeName) `
        + `matches too many rows on its own for the FEC's own database to search within its time `
        + `limit -- e.g. a common occupation like "RETIRED" or "ATTORNEY", or an employer like `
        + `"SELF-EMPLOYED". Narrow the search by adding another filter alongside it: donorCity, `
        + `donorZip, state, minAmount, maxAmount, or a contributionDateFrom/contributionDateTo `
        + `window, then retry.`,
      );
      e.httpStatus = 504;
      throw e;
    }
    throw err;
  }
  if (res.statusCode >= 400) {
    // Two distinct upstream error shapes, both measured live 2026-09-24 -- neither one alone is
    // enough to detect a failure, which is why the status code is the authority here:
    //  - api.data.gov gateway (auth + RATE LIMITS): {"error":{"code","message"}}, NO `status` key.
    //  - FEC app validation: {"message":"Invalid committee_id...","status":422}.
    const body = res.body;
    const detail = body?.error?.message
      ?? (typeof body?.message === 'string' ? body.message : null)
      ?? (typeof body === 'string' ? body.slice(0, 200) : null);
    // This Actor runs on FEC_API_KEY, its own personal api.data.gov key (confirmed live 2026-10-06
    // as a secret Actor env var in the published version), NOT the DEMO_KEY fallback at line 332
    // (that only ever fires on a local run with no env var set).
    // CEILINGS -- measured live 2026-10-28 (cycle 2364) off `x-ratelimit-limit`, NOT off the 429
    // body prose. This text used to quote "1,000/hour vs 40/hour", which came from the FEC's own
    // 429 error body ("40 calls per hour for the DEMO_KEY, 1000 calls per hour for a personal key,
    // or 120 calls per minute for an upgraded key") -- but the fec-campaign-finance-json-api-demo-key
    // blog post ALREADY established, from a live capture, that that prose is decoration and the
    // header is the only number actually enforced (body said 40, header said 10). Our own text was
    // quoting the decoration. What the header really says on api.open.fec.gov:
    //   this Actor's registered key -> x-ratelimit-limit: 60
    //   DEMO_KEY                    -> x-ratelimit-limit: 10 (per egress IP)
    // WINDOW: short, NOT the hour the body prose claims. Measured by burning the registered key
    // down to remaining=56, idling 165s with zero requests, then re-requesting: remaining came back
    // 59, i.e. the budget had fully refilled to 60. (DEMO_KEY behaves the opposite way -- its
    // counter kept declining 8 -> 7 across minutes, consistent with api.data.gov's documented
    // per-hour/per-day per-IP window at a FEC-lowered ceiling.) api.data.gov's documented DEFAULTS
    // -- 1,000/hr per key, 30/hr + 50/day for DEMO_KEY -- do not apply here; its own docs say
    // "rate limits may vary by service" and the FEC has clearly overridden both.
    // The ceiling is enforced PER KEY, not per caller/IP, so it is shared
    // across every concurrent run of this Actor by every buyer, not "the public DEMO_KEY". Getting
    // this right matters: the README's "you don't need your own FEC API key" section claims we
    // are not falling back to DEMO_KEY, and a 429 message that blames DEMO_KEY would flatly
    // contradict that claim the one time a buyer actually sees this error.
    // Never let a rate-limit 429 look like "this candidate has no money on file" - the totals
    // endpoint expresses that as HTTP 200 with results: [].
    if (res.statusCode === 429) {
      const e = new Error(
        'FEC API rate limit hit (HTTP 429). This Actor uses its own registered api.data.gov key '
        + '(api.open.fec.gov budgets it at 60 requests, per its x-ratelimit-limit header) rather '
        + 'than the public DEMO_KEY (10) -- but that budget is enforced per key, not per caller, '
        + "so it's shared across every buyer running this Actor at the same moment, and a busy "
        + 'burst can occasionally 429 your run too. The good news: the budget refills in about a '
        + 'minute (measured), so this is not an hour-long lockout despite what the FEC error body '
        + 'says. Each result costs 2 requests when includeTotals is on. Retry in a minute or two, '
        + 'lower maxResults, or set includeTotals to false to halve the request count.',
      );
      e.isRateLimit = true;
      e.httpStatus = 429;
      throw e;
    }
    const e = new Error(`FEC API returned HTTP ${res.statusCode}${detail ? `: ${detail}` : ''}`);
    e.httpStatus = res.statusCode;
    throw e;
  }
  return res.body;
}

// FEC's own official committee classification, straight off the `committee` sub-object the
// transaction schedules already embed -- e.g. "Super PAC (Independent Expenditure-Only)",
// "PAC - Qualified", "House" (a candidate's principal campaign committee). Not a heuristic:
// these are the FEC's own committee_type/designation codes, spelled out.
function committeeClassification(c) {
  const committee = c.committee ?? {};
  return {
    committeeType: committee.committee_type_full ?? null,
    committeeDesignation: committee.designation_full ?? null,
  };
}

async function fetchTotals(id) {
  try {
    const body = await fecGet(`/candidate/${id}/totals/`, { per_page: 1, sort: '-candidate_election_year' });
    return body.results?.[0] ?? null;
  } catch (err) {
    if (err.isRateLimit) throw err; // fail loudly rather than emit null money columns
    log.warning(`totals lookup failed for ${id}: ${err.message}`);
    return null;
  }
}

// Cycle 1937: a committee's `candidate_ids` having 2+ entries does NOT mean a joint
// fundraising committee splitting money across several people (the v0.1.68/0.1.70 assumption).
// A full registry scan found 430/20,903 (2.06%) cycle-2026 committees with 2+ ids, of which
// only 4 are JFCs (`designation:"J"`) -- the bulk (P=334, A=28) is ONE PERSON who holds
// several FEC candidate ids at once (a House id and a Senate id, e.g. Durbin's
// `H2IL20026`/`S6IL00151`), verified by resolving ids to names on two random samples (12/12,
// then 8/8, same human). Exact name-string equality under-reports this: the FEC spells the
// same person differently across ids ("DURBIN, RICHARD JOSEPH" vs "DURBIN, RICHARD J."), so
// the match below is surname + first-initial, not strict equality.
function normPerson(name) {
  if (!name) return null;
  const cleaned = name.toUpperCase()
    .replace(/\b(MR|MRS|MS|DR|HON|JR|SR|I{1,3}|IV)\b\.?/g, '')
    .replace(/[^A-Z, ]/g, ' ');
  const parts = cleaned.split(',').map((p) => p.trim()).filter(Boolean);
  if (!parts.length) return null;
  const surname = parts[0].split(/\s+/)[0] ?? '';
  const first = parts.length > 1 ? (parts[1].split(/\s+/)[0] ?? '') : '';
  return `${surname}|${first.slice(0, 1)}`;
}

const candidateNameCache = new Map(); // candidate_id -> name|null, resolved at most once per run
const committeeCandidateCache = new Map(); // committee_id -> { candidateId, candidateIds }

// Decides what `candidateId`/`candidateIds` should be for a committee, given its own
// `candidate_ids` list. 0 or 1 ids: unambiguous, no lookup needed. 2+ ids: resolve names
// (cached per candidate id, decision cached per committee, so a popular committee's rows
// only pay for this once per run) and check whether every id is the SAME person. If so,
// `candidateId` is still populated (prefer the id whose office letter matches this
// committee's own `committee_type`, e.g. "S" -> an "S"-prefixed id) because there is only one
// real-world candidate to name; only genuinely different people (the real JFC case) null it.
async function resolveCandidateIds(committee) {
  const ids = committee?.candidate_ids ?? [];
  if (ids.length <= 1) return { candidateId: ids[0] ?? null, candidateIds: null };
  const committeeId = committee.committee_id ?? null;
  if (committeeId && committeeCandidateCache.has(committeeId)) return committeeCandidateCache.get(committeeId);
  const missing = ids.filter((id) => !candidateNameCache.has(id));
  if (missing.length) {
    try {
      const body = await fecGet('/candidates/', { candidate_id: missing, per_page: 100 });
      for (const cand of body.results ?? []) candidateNameCache.set(cand.candidate_id, cand.name ?? null);
    } catch (err) {
      if (err.isRateLimit) throw err;
      log.warning(`candidate name lookup failed for committee ${committeeId}: ${err.message}`);
    }
    for (const id of missing) if (!candidateNameCache.has(id)) candidateNameCache.set(id, null);
  }
  const people = new Set(ids.map((id) => normPerson(candidateNameCache.get(id))).filter(Boolean));
  const samePerson = people.size === 1;
  const preferredId = ids.find((id) => committee.committee_type && id.startsWith(committee.committee_type)) ?? ids[0];
  const decision = { candidateId: samePerson ? preferredId : null, candidateIds: ids };
  if (committeeId) committeeCandidateCache.set(committeeId, decision);
  return decision;
}

// FEC fails CLOSED on some unrecognised filter VALUES (format-validated fields -- committee_id,
// candidate_id, min_amount/max_amount, office -- each reject a canary with HTTP 400/422) but
// OPEN on an unrecognised filter NAME -- silently dropped, full unfiltered index returned at
// HTTP 200. Measured live 2026-09-24: schedule_b `recipient_name`->`recipiant_name` (typo)
// 19,810,455 -> 157,249,937 matches (7.9x); schedule_a `contributor_employer`->`contributer_employer`
// 129,917 -> 264,070,913 (2032x); candidates `office`->`offce` returns all 127 unfiltered "Warren"
// rows instead of erroring. Same class as the sam-gov/OpenFEC/USAspending fail-open trap
// documented in /blog/government-apis-fail-open-on-a-dropped-filter-name. Two probe shapes,
// mirroring sam-gov's guardedFilterNames()/assertFilterNamesApplied() (cycle 748):
//  - COUNT probe (free-text/exact fields: contributor_name/employer/occupation/city/state,
//    recipient_name/state, payee_name, candidates state/party): a canary VALUE can't match
//    anything real, so a recognised name returns count 0; a dropped name returns the full
//    unfiltered count (>0).
//  - REJECT probe (format-validated fields: committee_id, candidate_id, min_amount, max_amount,
//    support_oppose_indicator, office): a canary VALUE fails the API's own format check
//    (HTTP 400/422) only if the name is still recognised; a dropped name skips validation
//    entirely and returns a normal HTTP 200.
// contributor_zip is deliberately NOT probed: it format-validates like the others, but "00000"
// (the obvious non-matching placeholder) turned out to have 40,703 real contributions attached
// to it, so there is no value that is both valid-format and guaranteed to match nothing.
const FILTER_CANARY = '__fetchsmith_canary_no_such_value__';

function guardedFilterNames() {
  const countProbe = [];
  const rejectProbe = [];
  if (searchMode === 'candidates') {
    if (state) countProbe.push('state');
    if (party) countProbe.push('party');
    if (office) rejectProbe.push('office');
  } else if (searchMode === 'contributions') {
    if (donorName) countProbe.push('contributor_name');
    if (donorEmployer) countProbe.push('contributor_employer');
    if (donorOccupation) countProbe.push('contributor_occupation');
    if (donorCity) countProbe.push('contributor_city');
    if (state) countProbe.push('contributor_state');
  } else if (searchMode === 'disbursements') {
    if (recipientName) countProbe.push('recipient_name');
    if (state) countProbe.push('recipient_state');
    if (committeeId) rejectProbe.push('committee_id');
  } else if (searchMode === 'independentExpenditures') {
    if (payeeName) countProbe.push('payee_name');
    if (candidateId) rejectProbe.push('candidate_id');
    if (committeeId) rejectProbe.push('committee_id');
    if (supportOppose) rejectProbe.push('support_oppose_indicator');
  }
  if (isTxnMode) {
    if (minAmount !== undefined) rejectProbe.push('min_amount');
    if (maxAmount !== undefined) rejectProbe.push('max_amount');
  }
  return { countProbe, rejectProbe };
}

async function assertFilterNamesApplied() {
  const { countProbe, rejectProbe } = guardedFilterNames();
  const base = searchMode === 'candidates' ? '/candidates/'
    : searchMode === 'disbursements' ? '/schedules/schedule_b/'
    : searchMode === 'independentExpenditures' ? '/schedules/schedule_e/'
    : '/schedules/schedule_a/';
  // Schedule A/B/E refuse a query with NO recognised filter at all ("please choose a single
  // two_year_transaction_period or add one of the following filters"), and not every field this
  // Actor guards is itself on that allow-list (contributor_state/recipient_state are not) --
  // probed alone they get that generic 400 instead of a real per-filter signal. The real query
  // always carries the period bound in txn mode (electionYear defaults to the current cycle, see
  // above), so echoing it into the probe keeps the probe representative of the real request.
  const periodParam = !isTxnMode ? {}
    : searchMode === 'independentExpenditures' ? { cycle: electionYear }
    : { two_year_transaction_period: electionYear };
  for (const name of countProbe) {
    let data;
    try {
      data = await fecGet(base, { ...periodParam, [name]: FILTER_CANARY, per_page: 1 });
    } catch (err) {
      // A rate limit is not an "upstream blip" to shrug off: the real request is about to hit the
      // same wall, and skipping the guard is exactly how an unverified filter reaches a billable
      // page. Fail loudly instead.
      if (err.isRateLimit) throw err;
      // An upstream blip is not evidence of a dropped filter -- do not fail the run on it.
      log.warning(`Could not verify that the FEC API still honours the "${name}" filter (probe request failed: ${err.message}); continuing.`);
      continue;
    }
    const total = data?.pagination?.count;
    if (typeof total !== 'number') {
      log.warning(`Could not verify that the FEC API still honours the "${name}" filter (no usable count in probe response); continuing.`);
      continue;
    }
    if (total > 0) {
      throw new Error(
        `The FEC API no longer recognises the "${name}" search filter: a probe request with `
        + `${name}=${FILTER_CANARY} returned ${total} matches instead of 0, which means the `
        + 'parameter is now being silently ignored and this search would return the entire '
        + 'unfiltered dataset instead of your filtered subset. Stopping before any unfiltered '
        + 'rows are delivered or charged. This is an upstream FEC API change -- please report it '
        + 'so the Actor can be updated.',
      );
    }
    log.info(`Verified the FEC API still honours the "${name}" filter (canary value returned 0 matches).`);
  }
  for (const name of rejectProbe) {
    let rejected = false;
    let count = null;
    let data;
    try {
      data = await fecGet(base, { ...periodParam, [name]: FILTER_CANARY, per_page: 1 });
    } catch (err) {
      // Since cycle 752 fecGet throws on any 4xx/5xx, so THIS is where a healthy rejection now
      // lands -- and it is a strictly better signal than the old body sniff, which only ever
      // matched FEC's app-level {"message","status"} shape and would have read a gateway-shaped
      // 400 as "not rejected" and aborted a perfectly good run. 400/422 is FEC's validation
      // range; anything else (429, 5xx, network) is not evidence about this filter.
      if (err.isRateLimit) throw err;
      if (err.httpStatus === 400 || err.httpStatus === 422) {
        rejected = true;
      } else {
        // An upstream blip is not evidence of a dropped filter -- do not fail the run on it.
        log.warning(`Could not verify that the FEC API still honours the "${name}" filter (probe request failed: ${err.message}); continuing.`);
        continue;
      }
    }
    if (!rejected) {
      count = data?.pagination?.count ?? null;
      throw new Error(
        `The FEC API no longer recognises the "${name}" search filter: a probe request with an `
        + `invalid ${name}=${FILTER_CANARY} was NOT rejected (expected HTTP 400/422${count !== null ? `, got HTTP 200 with ${count} matches instead` : ''}), `
        + 'which means the parameter is now being silently ignored and this search would return '
        + 'unfiltered results instead of your filtered subset. Stopping before any unfiltered rows '
        + 'are delivered or charged. This is an upstream FEC API change -- please report it so the '
        + 'Actor can be updated.',
      );
    }
    log.info(`Verified the FEC API still honours the "${name}" filter (canary value was correctly rejected).`);
  }
}

let watchPageCapHit = false;
try {
  // Before spending a single billable page: confirm the FEC API still honours every filter name
  // we are about to send. Deliberately inside this try, not before it -- a thrown guard error
  // still needs to fall through to the catch below so the watch baseline and RUN_SUMMARY get
  // persisted the same way an upstream API failure does (see the comment on that catch).
  await assertFilterNamesApplied();
  let page = 1;
  let stop = false;
  // The FEC's three transaction schedules (A/B/E) are KEYSET-paginated, not offset-paginated:
  // `page` is accepted and then ignored, so asking for page 2, 3, ... returns page 1's rows
  // again (verified live cycle 428 on all three schedules -- identical sub_ids). The real
  // cursor is `pagination.last_indexes`, whose keys (`last_index` plus a per-schedule sort
  // key such as `last_contribution_receipt_date`) must be echoed back as query params on the
  // next request. Only `/candidates/` uses normal `page` paging.
  let cursor = null;
  while (!stop) {
    if (!timeBudgetOk()) {
      timeBudgetHit = true;
      log.warning(
        `Run time budget reached; stopping before fetching page ${page} so the ${pushed} row(s) `
        + `already collected${watchMode ? ' and the watch baseline' : ''} are saved instead of lost to a hard kill.`,
      );
      break;
    }
    if (watchMode && page > WATCH_PAGE_CAP) {
      // A scan safety valve, not a delivery cap -- it only ever bounds how many pages of an
      // already-mostly-seen result set one run will page through, never how many NEW rows can
      // be delivered (that's maxResults, checked in pushResult). Distinct from the ats-jobs/
      // hacker-news trap (cycle 332/333) where a cost cap was reused for the scan itself: this
      // cap exists only to bound one run's request count against a broad, weakly-filtered watch.
      watchPageCapHit = true;
      log.warning(`Watch mode: stopped scanning after ${WATCH_PAGE_CAP} pages without exhausting the match set -- narrow donorName/donorEmployer/donorOccupation/donorCity/donorZip/state/minAmount/maxAmount/contributionDateFrom/contributionDateTo so the whole current match set fits in fewer pages.`);
      break;
    }
    const perPage = watchMode ? 100 : 20;
    const body = searchMode === 'disbursements'
      ? await fecGet('/schedules/schedule_b/', {
        recipient_name: recipientName,
        recipient_state: state,
        committee_id: committeeId,
        min_amount: minAmount,
        max_amount: maxAmount,
        min_date: contributionDateFrom,
        max_date: contributionDateTo,
        two_year_transaction_period: electionYear,
        ...cursor,
        per_page: perPage,
        sort: '-disbursement_date',
        // Postgres sorts NULLs FIRST on a DESC sort, so without this a match set containing any
        // dateless row (F3X filers routinely omit the date) starts with a block of dateless rows
        // instead of the newest ones -- and worse, that block's cursor carries no date value, so
        // the walk terminates at the end of it and never reaches the dated rows at all (proved
        // live cycle 856 on schedule_a: 320 dateless rows delivered, 13,693 dated rows silently
        // never reached). schedule_e has always had this; A and B were missing it.
        sort_nulls_last: 'true',
      })
      : searchMode === 'independentExpenditures'
      ? await fecGet('/schedules/schedule_e/', {
        payee_name: payeeName,
        candidate_id: candidateId,
        committee_id: committeeId,
        support_oppose_indicator: supportOppose,
        min_amount: minAmount,
        max_amount: maxAmount,
        min_date: contributionDateFrom,
        max_date: contributionDateTo,
        cycle: electionYear,
        ...cursor,
        per_page: perPage,
        sort: '-expenditure_date',
        sort_nulls_last: 'true',
      })
      : searchMode === 'contributions'
      ? await fecGet('/schedules/schedule_a/', {
        contributor_name: donorName,
        contributor_employer: donorEmployer,
        contributor_occupation: donorOccupation,
        contributor_city: donorCity,
        contributor_zip: donorZip,
        contributor_state: state,
        min_amount: minAmount,
        max_amount: maxAmount,
        min_date: contributionDateFrom,
        max_date: contributionDateTo,
        two_year_transaction_period: electionYear,
        ...cursor,
        per_page: perPage,
        sort: '-contribution_receipt_date',
        sort_nulls_last: 'true', // see the schedule_b note above -- same NULLs-first defect
      })
      : await fecGet('/candidates/', {
        q: candidateName,
        state,
        office,
        party,
        cycle: electionYear,
        page,
        per_page: 20,
        sort: 'name',
      });
    const results = body.results ?? [];
    pages += 1;
    scanned += results.length;
    // `pagination.count` is the FEC's own match total for these filters. Captured on the first
    // page only: the keyset-paginated schedules recompute it per request and it drifts as new
    // filings land, so a late page's count would silently restate the baseline mid-walk.
    if (declaredMatches === null && typeof body.pagination?.count === 'number') {
      declaredMatches = body.pagination.count;
      declaredExact = body.pagination.is_count_exact ?? null;
    }
    if (results.length === 0) break;

    let rowIndex = -1;
    for (const c of results) {
      rowIndex += 1;
      // Checked before this row's own work starts (including `fetchTotals()` below, the other
      // network call this Actor makes), not after -- so a time-budget stop here can never be
      // confused with `chargeLimitReached`/`maxResultsReached`/`seedCapHit`, which are only ever
      // set inside `pushResult()`, never reached for this row if this check fires first.
      if (!timeBudgetOk()) {
        timeBudgetHit = true;
        rowsNotReached = results.length - rowIndex;
        stop = true;
        break;
      }
      let item;
      let watchId;
      if (searchMode === 'disbursements') {
        // Keyed on committee_id+transaction_id, not sub_id: OpenFEC reissues a brand-new sub_id
        // for every itemization on a report -- including byte-identical, amendment_indicator:"N"
        // rows -- the moment the report gets ANY amendment, so a sub_id-keyed watch baseline
        // re-delivers (and re-charges for) the whole report on every amendment. transaction_id is
        // the filer's own id and stays stable across amendments (confirmed live, see README).
        watchId = watchKeyOf(c);
        // CORRECTED cycle 1937 -- 0.1.70's fallback to `committee.candidate_ids` when
        // `candidate_id` was null is REMOVED, not extended, after live verification showed it was
        // built on a false premise. In schedule_b the embedded `committee` is always the PAYING
        // committee, never the recipient, so falling back to its candidate_ids attributes the
        // payment to WHOEVER OWNS THE PAYING COMMITTEE, regardless of who actually got paid --
        // verified live on Durbin's own leadership PAC (C00148999, candidate_ids
        // [H2IL20026, S6IL00151]): a real disbursement to "MELISSA BEAN FOR CONGRESS" has
        // `candidate_id: null` but came out of the old code as `candidateId: "S6IL00151"`
        // (Durbin), a flatly wrong attribution. It also wasn't needed: FEC already tags each
        // disbursement with its OWN `candidate_id`/`candidate_name` when one specific candidate is
        // the payment's subject -- verified live on the real multi-candidate JFC this README cites
        // (`CASSIDY PERDUE SULLIVAN TILLIS VICTORY FUND`, C00568055): its disbursements to Tillis,
        // Sullivan, Perdue and Cassidy each arrive individually tagged with that candidate's own
        // id, never null. The only rows where both are null are genuine non-candidate spending
        // (e.g. a vendor invoice) -- correctly unattributed, not ambiguous.
        item = {
          committeeId: c.committee_id ?? c.committee?.committee_id ?? null,
          committeeName: c.committee?.name ?? null,
          ...committeeClassification(c),
          recipientName: c.recipient_name ?? null,
          recipientCity: c.recipient_city ?? null,
          recipientState: c.recipient_state ?? null,
          disbursementAmount: c.disbursement_amount ?? null,
          disbursementDate: c.disbursement_date ?? null,
          disbursementDescription: c.disbursement_description ?? null,
          disbursementPurposeCategory: c.disbursement_purpose_category ?? null,
          disbursementCategory: c.category_code_full ?? null,
          lineNumberLabel: c.line_number_label ?? null,
          candidateId: c.candidate_id ?? null,
          candidateIds: null,
          candidateName: c.candidate_name ?? null,
          electionCycle: c.two_year_transaction_period ?? null,
          // The FEC's own per-transaction identity. Emitted (cycle 772) because without it two
          // legitimately-repeated transactions -- same payee, amount, date and filing -- are
          // byte-identical in our output, so a customer cannot tell them apart, dedup them, or
          // join a row back to the FEC. `subId` is the FEC's row id; `transactionId` is the
          // filer's own id, stable across amendments of the same transaction.
          transactionId: c.transaction_id ?? null,
          subId: c.sub_id ?? null,
          imageNumber: c.image_number ?? null,
          pdfUrl: c.pdf_url ?? null,
        };
      } else if (searchMode === 'independentExpenditures') {
        watchId = watchKeyOf(c);
        item = {
          committeeId: c.committee_id ?? c.committee?.committee_id ?? null,
          committeeName: c.committee?.name ?? null,
          ...committeeClassification(c),
          candidateId: c.candidate_id ?? null,
          candidateName: c.candidate_name ?? null,
          candidateOffice: c.candidate_office ?? null,
          candidateOfficeState: c.candidate_office_state ?? null,
          candidateParty: c.candidate_party ?? null,
          supportOppose: c.support_oppose_indicator === 'S' ? 'support' : c.support_oppose_indicator === 'O' ? 'oppose' : null,
          payeeName: c.payee_name ?? null,
          expenditureAmount: c.expenditure_amount ?? null,
          expenditureDate: c.expenditure_date ?? null,
          disseminationDate: c.dissemination_date ?? null,
          expenditureDescription: c.expenditure_description ?? null,
          expenditureCategory: c.category_code_full ?? null,
          officeTotalYtd: c.office_total_ytd ?? null,
          electionType: c.election_type_full ?? c.election_type ?? null,
          filingForm: c.filing_form ?? null,
          isNotice: c.is_notice ?? null,
          // Schedule E has no `election_year` field at all (unlike schedule_b's
          // `two_year_transaction_period`) -- that key was always undefined, so every
          // independentExpenditures row silently shipped `electionCycle: null` regardless of the
          // `cycle` filter applied. `report_year` is the field that actually carries it (verified
          // live: filtering `cycle=2024` returns rows with `report_year: 2024`) but the FEC sends
          // it as a STRING here (unlike schedule_b's real int `two_year_transaction_period`) --
          // the dataset schema declares `electionCycle` integer|null, so an un-coerced string
          // fails Actor.pushData's schema validation and drops the whole run (reproduced live).
          electionCycle: c.report_year != null ? Number(c.report_year) : null,
          transactionId: c.transaction_id ?? null,
          subId: c.sub_id ?? null,
          imageNumber: c.image_number ?? null,
          pdfUrl: c.pdf_url ?? null,
        };
      } else if (searchMode === 'contributions') {
        watchId = watchKeyOf(c);
        // schedule_a's own `candidate_id` is always null on every row we've observed (verified
        // live on both a joint fundraising committee and a plain principal campaign committee)
        // -- the receiving committee's `candidate_ids` is the only real source. 2+ ids does NOT
        // mean a JFC splitting money across several people (cycle 1937 correction, see
        // resolveCandidateIds): the bulk of multi-id committees are one person holding both a
        // House and a Senate id, so only genuinely different people (a real multi-candidate
        // "Victory Fund") null `candidateId` -- see `candidateIds` for the full list either way.
        const aCandidate = c.candidate_id
          ? { candidateId: c.candidate_id, candidateIds: null }
          : await resolveCandidateIds(c.committee ?? {});
        item = {
          contributorName: c.contributor_name ?? null,
          contributorEmployer: c.contributor_employer ?? null,
          contributorOccupation: c.contributor_occupation ?? null,
          contributorCity: c.contributor_city ?? null,
          contributorZip: c.contributor_zip ?? null,
          contributorState: c.contributor_state ?? null,
          contributionAmount: c.contribution_receipt_amount ?? null,
          contributionDate: c.contribution_receipt_date ?? null,
          contributorAggregateYtd: c.contributor_aggregate_ytd ?? null,
          committeeId: c.committee_id ?? c.committee?.committee_id ?? null,
          committeeName: c.committee?.name ?? null,
          ...committeeClassification(c),
          ...aCandidate,
          transactionId: c.transaction_id ?? null,
          subId: c.sub_id ?? null,
          imageNumber: c.image_number ?? null,
          pdfUrl: c.pdf_url ?? null,
        };
      } else {
        const totals = includeTotals ? await fetchTotals(c.candidate_id) : null;
        item = {
          candidateId: c.candidate_id,
          name: c.name,
          party: c.party_full ?? c.party ?? null,
          office: c.office_full ?? c.office ?? null,
          state: c.state ?? null,
          district: c.district ?? null,
          incumbentChallenge: c.incumbent_challenge_full ?? null,
          candidateStatus: c.candidate_status ?? null,
          electionYears: c.election_years ?? [],
          cycles: c.cycles ?? [],
          firstFileDate: c.first_file_date ?? null,
          fecUrl: `https://www.fec.gov/data/candidate/${c.candidate_id}/`,
          receipts: totals?.receipts ?? null,
          disbursements: totals?.disbursements ?? null,
          cashOnHandEnd: totals?.last_cash_on_hand_end_period ?? null,
          individualContributions: totals?.individual_contributions ?? null,
          individualItemizedContributions: totals?.individual_itemized_contributions ?? null,
          individualUnitemizedContributions: totals?.individual_unitemized_contributions ?? null,
          refundedIndividualContributions: totals?.refunded_individual_contributions ?? null,
          coverageStartDate: totals?.coverage_start_date ?? null,
          coverageEndDate: totals?.coverage_end_date ?? null,
        };
      }
      const keepGoing = await pushResult(item, watchId);
      if (!keepGoing) {
        // Rows the run had already paid to fetch and then never delivered. This is the number
        // that proves the stop was a cap, not the end of the data -- `results.length === 0`
        // (the natural end) can never produce it.
        rowsNotReached = results.length - (rowIndex + 1);
        stop = true;
        break;
      }
    }

    const pagination = body.pagination ?? {};
    if (isTxnMode) {
      const next = pagination.last_indexes ?? null;
      // `sort_null_only: true` means "the rows after this point have a NULL sort field" -- with
      // `sort_nulls_last` set (below) that can only be the trailing null block, which is real
      // remaining data. It MUST be echoed back: the FEC rejects a cursor carrying only
      // `last_index` with HTTP 422 ("both values from the previous page's `last_indexes` object
      // are needed"), which used to fail the whole run (cycle 856, reproduced live). Normalised to
      // the string 'true' so the cursor-equality exhaustion test below compares stable JSON, and
      // `false` is dropped rather than sent as the truthy string "false".
      const cleaned = next
        ? Object.fromEntries(Object.entries(next)
          .filter(([, v]) => v !== null && v !== undefined && v !== false)
          .map(([k, v]) => [k, v === true ? 'true' : v]))
        : {};
      // No cursor, or a cursor identical to the one we just used, means the result set is
      // exhausted. Without this guard the old `page`-based loop silently re-fetched (and
      // re-charged for) the first page until maxResults was reached.
      const exhausted = Object.keys(cleaned).length === 0 || JSON.stringify(cleaned) === JSON.stringify(cursor ?? {});
      // Was anything left behind the cap? Asked with the SAME exhaustion test the walk itself
      // uses, so "stopped on a cap" and "ran out of data" can never be confused -- a stop that
      // lands exactly on a page boundary is still short if the cursor was live.
      if (stop) { moreAvailable = rowsNotReached > 0 || !exhausted; break; }
      if (exhausted) break;
      cursor = cleaned;
    } else {
      const morePages = page < (pagination.pages ?? 1);
      if (stop) { moreAvailable = rowsNotReached > 0 || morePages; break; }
      if (!morePages) break; // /candidates/ pages normally via `page`
    }
    page += 1;
  }
} catch (err) {
  // A `fecGet` call that timed out ONLY because its own request timeout was shortened to fit the
  // remaining time budget (see the check above requestTimeoutMs<30000) is a soft time-budget
  // stop, not an upstream failure -- it must NOT set `runError`/`upstream-error`, or it would
  // both fail the run (losing the rows already pushed and charged from the baseline, same as any
  // other runError) and tell the buyer to narrow their query when the real fix is a longer
  // timeout. Falls through to the generic `timeBudgetHit` handling below instead.
  if (err.isTimeBudget) {
    timeBudgetHit = true;
    log.warning(
      `Run time budget reached while waiting on the FEC API; stopping so the ${pushed} row(s) `
      + `already collected${watchMode ? ' and the watch baseline' : ''} are saved instead of lost to a hard kill.`,
    );
  } else {
    // Deliberately NOT Actor.fail() here (cycle 676): Actor.fail exits the process immediately, so
    // the watch baseline was never saved on a failed incremental run -- every row this run had
    // already pushed AND CHARGED for was missing from the baseline and got delivered and charged a
    // second time on the next run. Record the error, let the tail of the script persist the
    // baseline and RUN_SUMMARY, and fail at the very end instead.
    log.exception(err, 'Run failed');
    runError = err.message;
    markIncomplete('upstream-error', `the FEC API call on page ${pages + 1} failed: ${err.message}`);
  }
}

// Empty unless WATCH_KEEP actually dropped something, so it can never add noise to a healthy run.
function truncationNote() {
  if (baselineTruncated <= 0) return '';
  return ` WARNING: the baseline hit its ${WATCH_KEEP}-entry cap and ${baselineTruncated} oldest id(s) were`
    + ' dropped -- those will be delivered and charged again as "new". Narrow the query or split it across labels.';
}

const STATUS_MESSAGE_MAX = 500;
// Apify silently truncates `statusMessage` at 500 chars (found cycle 1760 on other Actors in this
// fleet) -- donorName/donorEmployer/donorOccupation/donorCity have no schema maxLength, so a long
// caller-supplied value could overflow the message built below. Word-boundary cut, not a hard slice.
const clampStatusMessage = (msg) => {
  if (msg.length <= STATUS_MESSAGE_MAX) return msg;
  const cut = msg.slice(0, STATUS_MESSAGE_MAX - 4);
  const lastSpace = cut.lastIndexOf(' ');
  return `${(lastSpace > 0 ? cut.slice(0, lastSpace) : cut).trimEnd()} ...`;
};

// Names only the filters actually applied in the active mode, so a plain no-match message never
// mentions a filter the search ignored. electionYear is always applied (defaults are set above),
// so it is unconditional in every mode.
function appliedFilterSummary() {
  const parts = [];
  if (searchMode === 'candidates') {
    parts.push(`candidateName="${candidateName}"`);
    if (state) parts.push(`state=${state}`);
    if (office) parts.push(`office=${office}`);
    if (party) parts.push(`party=${party}`);
    if (electionYear) parts.push(`electionYear=${electionYear}`);
  } else if (searchMode === 'contributions') {
    if (donorName) parts.push(`donorName="${donorName}"`);
    if (donorEmployer) parts.push(`donorEmployer="${donorEmployer}"`);
    if (donorOccupation) parts.push(`donorOccupation="${donorOccupation}"`);
    if (donorCity) parts.push(`donorCity="${donorCity}"`);
    if (donorZip) parts.push(`donorZip=${donorZip}`);
    if (state) parts.push(`state=${state}`);
    if (minAmount !== undefined) parts.push(`minAmount=${minAmount}`);
    if (maxAmount !== undefined) parts.push(`maxAmount=${maxAmount}`);
    if (contributionDateFrom) parts.push(`from=${contributionDateFrom}`);
    if (contributionDateTo) parts.push(`to=${contributionDateTo}`);
    parts.push(`electionYear=${electionYear}`);
  } else if (searchMode === 'disbursements') {
    if (recipientName) parts.push(`recipientName="${recipientName}"`);
    if (state) parts.push(`state=${state}`);
    if (committeeId) parts.push(`committeeId=${committeeId}`);
    if (minAmount !== undefined) parts.push(`minAmount=${minAmount}`);
    if (maxAmount !== undefined) parts.push(`maxAmount=${maxAmount}`);
    if (contributionDateFrom) parts.push(`from=${contributionDateFrom}`);
    if (contributionDateTo) parts.push(`to=${contributionDateTo}`);
    parts.push(`electionYear=${electionYear}`);
  } else {
    if (payeeName) parts.push(`payeeName="${payeeName}"`);
    if (candidateId) parts.push(`candidateId=${candidateId}`);
    if (committeeId) parts.push(`committeeId=${committeeId}`);
    if (supportOppose) parts.push(`supportOppose=${supportOppose}`);
    if (minAmount !== undefined) parts.push(`minAmount=${minAmount}`);
    if (maxAmount !== undefined) parts.push(`maxAmount=${maxAmount}`);
    if (contributionDateFrom) parts.push(`from=${contributionDateFrom}`);
    if (contributionDateTo) parts.push(`to=${contributionDateTo}`);
    parts.push(`electionYear=${electionYear}`);
  }
  return parts.join(', ');
}

const SEARCH_MODE_NOUN = {
  candidates: 'candidates',
  contributions: 'contributions',
  disbursements: 'disbursements',
  independentExpenditures: 'independent expenditures',
};

// First cause wins, so these run in the order the buyer can act on: an upstream failure was
// already recorded in the catch above and outranks every cap below it. `max-results` is only a
// shortfall when something was demonstrably left behind -- a query with exactly maxResults
// matches is complete, and saying otherwise would cry wolf on the commonest healthy run.
// `timeBudgetHit` is set in exactly two places, both of which break the walk immediately before
// any of the other four causes below can be set for the same stop -- so in practice at most one
// of these five is ever true, and the order here is for readability, not tie-breaking.
if (timeBudgetHit) markIncomplete('time-budget', `${pushed.toLocaleString('en-US')} row(s) delivered over ${pages} page(s); the run approached its platform time limit and stopped itself so what was already collected${watchMode ? ' (and the watch baseline)' : ''} would be saved instead of lost to a hard kill. Give the run a longer timeout in its run options, or narrow the query.`);
if (watchPageCapHit) markIncomplete('watch-page-cap', `the watch scan stopped after ${WATCH_PAGE_CAP} page(s) without exhausting the match set`);
if (seedCapHit) markIncomplete('seed-cap', `the baseline stopped at the ${SEED_CAP}-row cap; matches past the cap will be reported as new (and charged) on a later incremental run`);
if (chargeLimitReached) markIncomplete('charge-limit', `the run's pay-per-event charge limit was reached${rowsNotReached ? `; ${rowsNotReached} already-fetched row(s) were not delivered` : ''}`);
if (maxResultsReached && moreAvailable) markIncomplete('max-results', `maxResults=${maxResults} reached${rowsNotReached ? `; ${rowsNotReached} already-fetched row(s) were not delivered` : ''}`);

// A failed SEEDING run must NOT leave a partial baseline behind: a half-written baseline turns
// the next run into an "incremental" one that charges for every match the seed walk never
// reached. No record at all is the cheap outcome -- the next run simply re-seeds for free. Gated
// on `runError` specifically, not on `!complete` -- a cap-triggered seed shortfall (seedCapHit,
// watchPageCapHit, and now timeBudgetHit) is a soft, anticipated stopping point that still saves
// the partial baseline with a warning (same as seedCapHit's own wording above), not a refusal;
// only a genuine thrown failure discards it, because only then is the baseline's state unknown
// rather than merely incomplete.
const skipBaselineSave = watchMode && seeding && runError !== null;
if (skipBaselineSave) {
  log.warning(
    `The baseline run for "${watchLabel}" failed before it finished, so NO baseline was saved. `
    + 'Re-run on the same label and filters to seed again (a baseline run charges nothing). Saving '
    + 'the partial baseline would have made the next run an incremental one and charged you for '
    + 'every match the failed seed walk never reached.',
  );
}

if (watchMode && !skipBaselineSave) {
  await saveWatchRecord(runError ? 'failed-incremental' : (seeding ? 'seeded' : 'incremental'));
  if (runError) {
    // The rows this run pushed were already charged; recording them is what stops the next run
    // delivering and charging for them a second time.
    log.info(`Watch baseline for "${watchLabel}" saved despite the failure: the ${pushed} row(s) already delivered and charged this run will not be charged again.`);
  } else if (seeding) {
    log.info(
      `Baseline saved for watch label "${watchLabel}": ${watchSeen.size} contribution(s) recorded as already-seen, `
      + '0 results returned, 0 charged. The next run on this label and these filters returns only what is new.'
      + (watchSeen.size >= SEED_CAP
        ? ` NOTE: the baseline hit the ${SEED_CAP}-contribution cap. Narrow donorName/donorEmployer/donorOccupation/donorCity/donorZip/state/minAmount/maxAmount/contributionDateFrom/contributionDateTo so `
        + 'the whole current match set fits, or the first incremental run may report older contributions past the cap as new.'
        : watchPageCapHit
          ? ` NOTE: the baseline hit the ${WATCH_PAGE_CAP}-page scan cap before exhausting the match set. Narrow the filters.`
          : ''),
    );
    await Actor.setStatusMessage(
      (complete
        ? `Baseline run for watch label "${watchLabel}": ${watchSeen.size} existing contribution(s) recorded, 0 charged. Run again later to get only what's new.`
        // An INCOMPLETE baseline is the costliest quiet outcome this Actor has: everything the
        // seed walk never reached is "new" to the first incremental run and gets charged.
        : `Baseline INCOMPLETE for watch label "${watchLabel}": ${watchSeen.size} contribution(s) recorded, 0 charged — ${incompleteReason}`
          + `${incompleteDetail ? ` (${incompleteDetail})` : ''}. Narrow the filters and re-seed before scheduling, or the rest will be charged as new. See RUN_SUMMARY.`)
      + (watchPastDateBound
        ? ` NOTE: once today's date passes contributionDateTo (${input.contributionDateTo}), this watch can no longer report ongoing new activity (see the warnings in the log). Drop it.`
        : '')
      + truncationNote(),
    );
  } else {
    log.info(`Watch label "${watchLabel}": ${pushed} new contribution(s) since the last run (${watchSkipped} already-delivered hit(s) skipped, not charged); baseline now holds ${watchSeen.size}.`);
    if (pushed === 0 && complete) {
      await Actor.setStatusMessage(
        `Nothing new for watch label "${watchLabel}" since its last run -- every matching contribution had already been delivered. That is the expected result most of the time; you were charged for nothing.`
        + (watchPastDateBound
          ? ` NOTE: this run can no longer report ongoing new activity while contributionDateTo (${input.contributionDateTo}) is set and today's date is past it -- it is an upper bound on the transaction date, and current activity is newer than that. Drop it (see the warnings in the log).`
          : '')
        + truncationNote(),
      );
    } else if (pushed === 0) {
      // NOT the same claim as the branch above: the scan stopped (charge-limit/time-budget/
      // watch-page-cap) before it could tell whether anything new exists -- "0 delivered" here is
      // NOT evidence of "nothing new". A tight run-level charge limit is the sharpest case: it can
      // make chargeLimitReached fire on the very first genuinely-new row, before pushed ever moves
      // off 0, which previously fell into the confident "already delivered" message above and told
      // the buyer their watch was quiet when a new contribution was in fact sitting there unbilled.
      await Actor.setStatusMessage(
        `Watch label "${watchLabel}": 0 row(s) delivered, but the scan did NOT finish -- ${incompleteReason}${incompleteDetail ? ` (${incompleteDetail})` : ''}. `
        + 'This is NOT a confirmed "nothing new": the scan may not have reached every matching contribution. See RUN_SUMMARY.'
        + truncationNote(),
      );
    } else if (baselineTruncated > 0 || !complete) {
      // A run that delivered rows would otherwise leave the default status message in place and
      // the truncation -- or a scan that stopped on a cap with new contributions still unread --
      // would only be visible in the log.
      await Actor.setStatusMessage(
        `Watch label "${watchLabel}": ${pushed} row(s) delivered.`
        + (complete ? '' : ` Scan INCOMPLETE — ${incompleteReason}${incompleteDetail ? ` (${incompleteDetail})` : ''}; more new contributions may be waiting. See RUN_SUMMARY.`)
        + truncationNote(),
      );
    }
  }
}

log.info(`Done. Pushed ${pushed} results (scanned ${scanned} row(s) over ${pages} page(s)).`);

// ---------------------------------------------------------------------------
// RUN_SUMMARY: this run's completeness, in a form a pipeline can read. Fetch with
//   GET /v2/actor-runs/<runId>/key-value-store/records/RUN_SUMMARY
// which needs no webhook. `complete` is deliberately kept OUT of the run status: a run can be
// SUCCEEDED and short at the same time, and that pair is exactly what this record exists for.
const runSummary = {
  mode: watchMode ? (seeding ? 'watch-seed' : 'watch-incremental') : searchMode,
  searchMode,
  // What the FEC itself says matches these filters (pagination.count, first page). `null` means
  // the API never answered with a count -- never read it as 0. `declaredMatchesExact` is the
  // FEC's own is_count_exact flag: on the big schedules the count can be an estimate.
  declaredMatches,
  declaredMatchesExact: declaredExact,
  scanned,
  delivered: pushed,
  rowsNotReached,
  pages,
  complete,
  incompleteReason,
  incompleteDetail,
  runError,
  maxResults,
  maxResultsReached,
  chargeLimitReached,
  timeBudgetHit,
  seedCap: watchMode && seeding ? SEED_CAP : null,
  seedCapHit: watchMode && seeding ? seedCapHit : null,
  watchPageCap: watchMode ? WATCH_PAGE_CAP : null,
  watchPageCapHit: watchMode ? watchPageCapHit : null,
  watchLabel: watchMode ? watchLabel : null,
  watchSeeding: watchMode ? seeding : null,
  baselineSaved: watchMode ? !skipBaselineSave : null,
  baselineSize: watchMode ? watchSeen.size : null,
  // >0 means the baseline lost ids to the WATCH_KEEP cap and a future run will re-deliver and
  // re-charge them; the cumulative figure is the drift over the whole life of the label.
  baselineTruncated: watchMode ? baselineTruncated : null,
  baselineTruncatedTotal: watchMode ? baselineTruncatedTotal : null,
  skippedSeen: watchMode && !seeding ? watchSkipped : null,
  watchPastDateBound: watchMode ? watchPastDateBound : null,
};
await Actor.setValue('RUN_SUMMARY', runSummary);

// A short run still SUCCEEDS (the rows it did get are real and already charged), so outside the
// watch-mode branches above -- which set their own, more specific messages -- the status message
// is the only place the Apify console itself shows the shortfall.
if (!complete && !runError && !watchMode) { // watch mode sets its own, more specific message above
  const of = declaredMatches === null ? '' : ` of ${declaredMatches.toLocaleString('en-US')}${declaredExact === false ? '+' : ''} declared match(es)`;
  await Actor.setStatusMessage(
    `Incomplete: ${pushed.toLocaleString('en-US')} row(s)${of} — ${incompleteReason}`
    + `${incompleteDetail ? ` (${incompleteDetail})` : ''}. See RUN_SUMMARY for details.`,
  );
} else if (complete && !watchMode && declaredMatches !== null) {
  log.info(`Complete: delivered every one of the ${declaredMatches.toLocaleString('en-US')} row(s) the FEC declared for these filters.`);
  // A plain, non-watch search that genuinely matches nothing used to leave the default "Succeeded"
  // status in place (same null-statusMessage bug the 1752-1759 fleet audit fixed on every OTHER
  // Actor that had a reachable zero-row branch -- this one was missed because it had no pre-existing
  // log-only message to find by grep for "pushed === 0").
  if (pushed === 0) {
    await Actor.setStatusMessage(clampStatusMessage(
      `No ${SEARCH_MODE_NOUN[searchMode]} matched (${appliedFilterSummary()}). The FEC confirms 0 `
      + 'results for these filters -- not an error. Narrow or drop a filter to broaden the search.',
    ));
  }
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
    // >0 means the baseline lost ids to the WATCH_KEEP cap and a future run will re-deliver and
    // re-charge them; the cumulative figure is the drift over the whole life of the label.
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

// The failure signal itself is unchanged -- the run still ends FAILED. It just happens here,
// after the baseline, RUN_SUMMARY and webhook have been persisted, instead of inside the catch
// where Actor.fail's immediate exit skipped all three.
if (runError) await Actor.fail(`Run failed: ${runError}`);

await Actor.exit();
