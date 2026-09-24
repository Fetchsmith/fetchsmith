// FEC Campaign Finance Scraper: candidates + financial totals, or individual donor contributions
// (Schedule A), via api.open.fec.gov. Uses a personal api.data.gov key (env var FEC_API_KEY, set as
// a secret Actor env var, not committed) with a DEMO_KEY fallback for local runs.
import { createHash } from 'crypto';
import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';

await Actor.init();
const input = (await Actor.getInput()) ?? {};
const MODES = ['candidates', 'contributions', 'disbursements', 'independentExpenditures'];
const searchMode = MODES.includes(input.searchMode) ? input.searchMode : 'candidates';
// The three transaction schedules (A receipts / B disbursements / E independent expenditures)
// share the same paging, amount-window, date-window and watch machinery -- only the endpoint,
// the query params and the row shape differ.
const isTxnMode = searchMode !== 'candidates';
const candidateName = (input.candidateName ?? 'Warren').trim();
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
]) {
  if (value && !modes.includes(searchMode)) {
    log.warning(`Ignoring ${field} "${value}": it only applies in searchMode ${modes.map((m) => `"${m}"`).join('/')}, and this run is in "${searchMode}" mode.`);
  }
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

async function fecGet(path, params) {
  const url = new URL(API_BASE + path);
  url.searchParams.set('api_key', API_KEY);
  for (const [k, v] of Object.entries(params)) {
    if (v !== undefined && v !== '') url.searchParams.set(k, v);
  }
  // got-scraping defaults to throwHttpErrors:false (verified live 2026-09-24: a 403/422/404
  // arrives as an ordinary RESOLVED response, never a thrown error). Set explicitly because the
  // status check below depends on it. Until cycle 752 this function relied on got throwing and
  // inspected `err.response?.statusCode` in a catch -- code that could never run, so every 4xx/5xx
  // was returned to the caller as a normal body. The page walk reads `body.results ?? []`, sees an
  // empty page and `break`s, so a mid-walk 429 ended the run as "complete" with partial data and
  // no warning; `fetchTotals` turned one into "no money on file". Check the status directly.
  const res = await gotScraping({
    url: url.toString(),
    timeout: { request: 30000 },
    retry: { limit: 2 },
    responseType: 'json',
    throwHttpErrors: false,
  });
  if (res.statusCode >= 400) {
    // Two distinct upstream error shapes, both measured live 2026-09-24 -- neither one alone is
    // enough to detect a failure, which is why the status code is the authority here:
    //  - api.data.gov gateway (auth + RATE LIMITS): {"error":{"code","message"}}, NO `status` key.
    //  - FEC app validation: {"message":"Invalid committee_id...","status":422}.
    const body = res.body;
    const detail = body?.error?.message
      ?? (typeof body?.message === 'string' ? body.message : null)
      ?? (typeof body === 'string' ? body.slice(0, 200) : null);
    // The shared DEMO_KEY quota is per egress IP, so exhaustion is a real runtime outcome, not an
    // edge case. Never let it look like "this candidate has no money on file" - the totals
    // endpoint expresses that as HTTP 200 with results: [].
    if (res.statusCode === 429) {
      const e = new Error(
        'FEC API rate limit hit (HTTP 429) on the shared DEMO_KEY, which is throttled per '
        + 'egress IP. Note each result costs 2 requests when includeTotals is on. Retry later, '
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
      let item;
      let watchId;
      if (searchMode === 'disbursements') {
        watchId = c.sub_id ?? null;
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
          candidateName: c.candidate_name ?? null,
          electionCycle: c.two_year_transaction_period ?? null,
          imageNumber: c.image_number ?? null,
          pdfUrl: c.pdf_url ?? null,
        };
      } else if (searchMode === 'independentExpenditures') {
        watchId = c.sub_id ?? null;
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
          electionCycle: c.election_year ?? null,
          imageNumber: c.image_number ?? null,
          pdfUrl: c.pdf_url ?? null,
        };
      } else if (searchMode === 'contributions') {
        watchId = c.sub_id ?? null;
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
          candidateId: c.candidate_id ?? c.committee?.candidate_ids?.[0] ?? null,
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
      // `sort_null_only` is a flag the API returns inside last_indexes, not a cursor value;
      // echoing it back would ask for null-sorted rows only, so drop it.
      const cleaned = next
        ? Object.fromEntries(Object.entries(next).filter(([k, v]) => k !== 'sort_null_only' && v !== null && v !== undefined))
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
  // Deliberately NOT Actor.fail() here (cycle 676): Actor.fail exits the process immediately, so
  // the watch baseline was never saved on a failed incremental run -- every row this run had
  // already pushed AND CHARGED for was missing from the baseline and got delivered and charged a
  // second time on the next run. Record the error, let the tail of the script persist the
  // baseline and RUN_SUMMARY, and fail at the very end instead.
  log.exception(err, 'Run failed');
  runError = err.message;
  markIncomplete('upstream-error', `the FEC API call on page ${pages + 1} failed: ${err.message}`);
}

// Empty unless WATCH_KEEP actually dropped something, so it can never add noise to a healthy run.
function truncationNote() {
  if (baselineTruncated <= 0) return '';
  return ` WARNING: the baseline hit its ${WATCH_KEEP}-entry cap and ${baselineTruncated} oldest id(s) were`
    + ' dropped -- those will be delivered and charged again as "new". Narrow the query or split it across labels.';
}

// First cause wins, so these run in the order the buyer can act on: an upstream failure was
// already recorded in the catch above and outranks every cap below it. `max-results` is only a
// shortfall when something was demonstrably left behind -- a query with exactly maxResults
// matches is complete, and saying otherwise would cry wolf on the commonest healthy run.
if (watchPageCapHit) markIncomplete('watch-page-cap', `the watch scan stopped after ${WATCH_PAGE_CAP} page(s) without exhausting the match set`);
if (seedCapHit) markIncomplete('seed-cap', `the baseline stopped at the ${SEED_CAP}-row cap; matches past the cap will be reported as new (and charged) on a later incremental run`);
if (chargeLimitReached) markIncomplete('charge-limit', `the run's pay-per-event charge limit was reached${rowsNotReached ? `; ${rowsNotReached} already-fetched row(s) were not delivered` : ''}`);
if (maxResultsReached && moreAvailable) markIncomplete('max-results', `maxResults=${maxResults} reached${rowsNotReached ? `; ${rowsNotReached} already-fetched row(s) were not delivered` : ''}`);

// A failed SEEDING run must NOT leave a partial baseline behind: a half-written baseline turns
// the next run into an "incremental" one that charges for every match the seed walk never
// reached. No record at all is the cheap outcome -- the next run simply re-seeds for free.
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
      + truncationNote(),
    );
  } else {
    log.info(`Watch label "${watchLabel}": ${pushed} new contribution(s) since the last run (${watchSkipped} already-delivered hit(s) skipped, not charged); baseline now holds ${watchSeen.size}.`);
    if (pushed === 0) {
      await Actor.setStatusMessage(
        `Nothing new for watch label "${watchLabel}" since its last run -- every matching contribution had already been delivered. That is the expected result most of the time; you were charged for nothing.`
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
