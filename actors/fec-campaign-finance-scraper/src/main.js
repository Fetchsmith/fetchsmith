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
const recipientName = (input.recipientName ?? '').trim();
const payeeName = (input.payeeName ?? '').trim();
const candidateId = (input.candidateId ?? '').trim().toUpperCase();
const committeeIdInput = (input.committeeId ?? '').trim().toUpperCase();
const supportOppose = ['S', 'O'].includes(String(input.supportOppose ?? '').trim().toUpperCase())
  ? String(input.supportOppose).trim().toUpperCase()
  : '';
const minAmount = input.minAmount ? Number(input.minAmount) : undefined;
const maxAmount = input.maxAmount ? Number(input.maxAmount) : undefined;
function parseFecDate(s, label) {
  const trimmed = String(s ?? '').trim();
  if (!trimmed) return undefined;
  if (!/^\d{4}-\d{2}-\d{2}$/.test(trimmed)) {
    log.warning(`Ignoring invalid ${label} "${trimmed}" (expected YYYY-MM-DD).`);
    return undefined;
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
  const ids = Array.from(watchSeen).slice(-WATCH_KEEP);
  await watchStore.setValue(watchKey, {
    ...watchRecord,
    label: watchLabel,
    lastRunAt: new Date().toISOString(),
    lastRunStatus: status,
    runCount: (watchRecord.runCount ?? 0) + 1,
    seenCount: ids.length,
    seenIds: ids,
  });
}

async function pushResult(item, watchId) {
  if (watchMode && watchId != null && seeding) {
    watchSeen.add(String(watchId));
    return watchSeen.size < SEED_CAP;
  }
  if (watchMode && watchId != null && watchSeen.has(String(watchId))) {
    watchSkipped += 1;
    return true;
  }
  if (isPPE) {
    const r = await Actor.charge({ eventName: 'result', count: 1 });
    if (r.chargedCount === 0) return false;
    await Actor.pushData(item); pushed += 1;
    if (watchMode && watchId != null) watchSeen.add(String(watchId));
    return !r.eventChargeLimitReached && pushed < maxResults;
  }
  await Actor.pushData(item); pushed += 1;
  if (watchMode && watchId != null) watchSeen.add(String(watchId));
  return pushed < maxResults;
}

const API_BASE = 'https://api.open.fec.gov/v1';
const API_KEY = process.env.FEC_API_KEY ?? 'DEMO_KEY';

async function fecGet(path, params) {
  const url = new URL(API_BASE + path);
  url.searchParams.set('api_key', API_KEY);
  for (const [k, v] of Object.entries(params)) {
    if (v !== undefined && v !== '') url.searchParams.set(k, v);
  }
  try {
    const res = await gotScraping({
      url: url.toString(),
      timeout: { request: 30000 },
      retry: { limit: 2 },
      responseType: 'json',
    });
    return res.body;
  } catch (err) {
    // The shared DEMO_KEY quota is per egress IP, so exhaustion is a real runtime
    // outcome, not an edge case. Never let it look like "this candidate has no money
    // on file" - the totals endpoint expresses that as HTTP 200 with results: [].
    if (err.response?.statusCode === 429) {
      const e = new Error(
        'FEC API rate limit hit (HTTP 429) on the shared DEMO_KEY, which is throttled per '
        + 'egress IP. Note each result costs 2 requests when includeTotals is on. Retry later, '
        + 'lower maxResults, or set includeTotals to false to halve the request count.',
      );
      e.isRateLimit = true;
      throw e;
    }
    throw err;
  }
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

let watchPageCapHit = false;
try {
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
      log.warning(`Watch mode: stopped scanning after ${WATCH_PAGE_CAP} pages without exhausting the match set -- narrow donorName/donorEmployer/donorOccupation/donorCity/state/minAmount/maxAmount/contributionDateFrom/contributionDateTo so the whole current match set fits in fewer pages.`);
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
    if (results.length === 0) break;

    for (const c of results) {
      let item;
      let watchId;
      if (searchMode === 'disbursements') {
        watchId = c.sub_id ?? null;
        item = {
          committeeId: c.committee_id ?? c.committee?.committee_id ?? null,
          committeeName: c.committee?.name ?? null,
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
          contributorState: c.contributor_state ?? null,
          contributionAmount: c.contribution_receipt_amount ?? null,
          contributionDate: c.contribution_receipt_date ?? null,
          contributorAggregateYtd: c.contributor_aggregate_ytd ?? null,
          committeeId: c.committee_id ?? c.committee?.committee_id ?? null,
          committeeName: c.committee?.name ?? null,
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
      if (!keepGoing) { stop = true; break; }
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
      if (Object.keys(cleaned).length === 0 || JSON.stringify(cleaned) === JSON.stringify(cursor ?? {})) break;
      cursor = cleaned;
    } else {
      if (page >= (pagination.pages ?? 1)) break; // /candidates/ pages normally via `page`
    }
    page += 1;
  }
} catch (err) {
  log.exception(err, 'Run failed');
  await Actor.fail(`Run failed: ${err.message}`);
}

if (watchMode) {
  await saveWatchRecord(seeding ? 'seeded' : 'incremental');
  if (seeding) {
    log.info(
      `Baseline saved for watch label "${watchLabel}": ${watchSeen.size} contribution(s) recorded as already-seen, `
      + '0 results returned, 0 charged. The next run on this label and these filters returns only what is new.'
      + (watchSeen.size >= SEED_CAP
        ? ` NOTE: the baseline hit the ${SEED_CAP}-contribution cap. Narrow donorName/donorEmployer/donorOccupation/donorCity/state/minAmount/maxAmount/contributionDateFrom/contributionDateTo so `
        + 'the whole current match set fits, or the first incremental run may report older contributions past the cap as new.'
        : watchPageCapHit
          ? ` NOTE: the baseline hit the ${WATCH_PAGE_CAP}-page scan cap before exhausting the match set. Narrow the filters.`
          : ''),
    );
    await Actor.setStatusMessage(`Baseline run for watch label "${watchLabel}": ${watchSeen.size} existing contribution(s) recorded, 0 charged. Run again later to get only what's new.`);
  } else {
    log.info(`Watch label "${watchLabel}": ${pushed} new contribution(s) since the last run (${watchSkipped} already-delivered hit(s) skipped, not charged); baseline now holds ${watchSeen.size}.`);
    if (pushed === 0) {
      await Actor.setStatusMessage(`Nothing new for watch label "${watchLabel}" since its last run -- every matching contribution had already been delivered. That is the expected result most of the time; you were charged for nothing.`);
    }
  }
}

log.info(`Done. Pushed ${pushed} results.`);

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
