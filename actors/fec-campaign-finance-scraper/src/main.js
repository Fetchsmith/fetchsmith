// FEC Campaign Finance Scraper: candidates + financial totals, or individual donor contributions
// (Schedule A), via api.open.fec.gov. Uses a personal api.data.gov key (env var FEC_API_KEY, set as
// a secret Actor env var, not committed) with a DEMO_KEY fallback for local runs.
import { createHash } from 'crypto';
import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';

await Actor.init();
const input = (await Actor.getInput()) ?? {};
const searchMode = input.searchMode === 'contributions' ? 'contributions' : 'candidates';
const candidateName = (input.candidateName ?? 'Warren').trim();
const donorName = (input.donorName ?? '').trim();
const donorEmployer = (input.donorEmployer ?? '').trim();
const minAmount = input.minAmount ? Number(input.minAmount) : undefined;
const state = (input.state ?? '').trim().toUpperCase();
const office = (input.office ?? '').trim().toUpperCase();
const party = (input.party ?? '').trim().toUpperCase();
// The FEC's Schedule A endpoint times out on a full-table scan without this filter, so
// contributions mode always sends one (defaulting to the most recent even year), while
// candidates mode leaves it unset ("all cycles") unless the caller asks for one.
const currentEvenYear = new Date().getUTCFullYear() - (new Date().getUTCFullYear() % 2);
const electionYear = input.electionYear
  ? Number(input.electionYear)
  : (searchMode === 'contributions' ? currentEvenYear : undefined);
const includeTotals = input.includeTotals ?? true;
const maxResults = Math.min(Number(input.maxResults ?? 20), 500);
const watchLabel = String(input.watchLabel ?? '').trim();

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
if (watchMode && searchMode !== 'contributions') {
  log.warning(`watchLabel "${watchLabel}" is ignored in candidates mode -- watch mode only applies to searchMode:"contributions" (candidates mode always returns the same fixed roster, not a stream of new events).`);
  watchMode = false;
}
let watchStore = null;
let watchKey = null;
let watchRecord = null;
let seeding = false;
let watchSkipped = 0;
const watchSeen = new Set(); // sub_ids already delivered under this label+fingerprint

if (watchMode) {
  const criteria = { donorName, donorEmployer, state, minAmount: minAmount ?? null, electionYearRaw: input.electionYear ?? null };
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

async function fetchTotals(candidateId) {
  try {
    const body = await fecGet(`/candidate/${candidateId}/totals/`, { per_page: 1, sort: '-candidate_election_year' });
    return body.results?.[0] ?? null;
  } catch (err) {
    if (err.isRateLimit) throw err; // fail loudly rather than emit null money columns
    log.warning(`totals lookup failed for ${candidateId}: ${err.message}`);
    return null;
  }
}

let watchPageCapHit = false;
try {
  let page = 1;
  let stop = false;
  while (!stop) {
    if (watchMode && page > WATCH_PAGE_CAP) {
      // A scan safety valve, not a delivery cap -- it only ever bounds how many pages of an
      // already-mostly-seen result set one run will page through, never how many NEW rows can
      // be delivered (that's maxResults, checked in pushResult). Distinct from the ats-jobs/
      // hacker-news trap (cycle 332/333) where a cost cap was reused for the scan itself: this
      // cap exists only to bound one run's request count against a broad, weakly-filtered watch.
      watchPageCapHit = true;
      log.warning(`Watch mode: stopped scanning after ${WATCH_PAGE_CAP} pages without exhausting the match set -- narrow donorName/donorEmployer/state/minAmount so the whole current match set fits in fewer pages.`);
      break;
    }
    const body = searchMode === 'contributions'
      ? await fecGet('/schedules/schedule_a/', {
        contributor_name: donorName,
        contributor_employer: donorEmployer,
        contributor_state: state,
        min_amount: minAmount,
        two_year_transaction_period: electionYear,
        page,
        per_page: watchMode ? 100 : 20,
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
      if (searchMode === 'contributions') {
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
    if (page >= (pagination.pages ?? 1)) break;
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
        ? ` NOTE: the baseline hit the ${SEED_CAP}-contribution cap. Narrow donorName/donorEmployer/state/minAmount so `
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
await Actor.exit();
