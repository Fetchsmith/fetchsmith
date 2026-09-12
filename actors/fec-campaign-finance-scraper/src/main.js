// FEC Campaign Finance Scraper: candidates + financial totals via api.open.fec.gov (no key required, DEMO_KEY tier).
import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';

await Actor.init();
const input = (await Actor.getInput()) ?? {};
const candidateName = (input.candidateName ?? 'Warren').trim();
const state = (input.state ?? '').trim().toUpperCase();
const office = (input.office ?? '').trim().toUpperCase();
const party = (input.party ?? '').trim().toUpperCase();
const electionYear = input.electionYear ? Number(input.electionYear) : undefined;
const includeTotals = input.includeTotals ?? true;
const maxResults = Math.min(Number(input.maxResults ?? 20), 500);

const isPPE = Actor.getChargingManager().getPricingInfo().isPayPerEvent;
let pushed = 0;

async function pushResult(item) {
  if (isPPE) {
    const r = await Actor.charge({ eventName: 'result', count: 1 });
    if (r.chargedCount === 0) return false;
    await Actor.pushData(item); pushed += 1;
    return !r.eventChargeLimitReached && pushed < maxResults;
  }
  await Actor.pushData(item); pushed += 1;
  return pushed < maxResults;
}

const API_BASE = 'https://api.open.fec.gov/v1';
const API_KEY = 'DEMO_KEY';

async function fecGet(path, params) {
  const url = new URL(API_BASE + path);
  url.searchParams.set('api_key', API_KEY);
  for (const [k, v] of Object.entries(params)) {
    if (v !== undefined && v !== '') url.searchParams.set(k, v);
  }
  const res = await gotScraping({
    url: url.toString(),
    timeout: { request: 30000 },
    retry: { limit: 2 },
    responseType: 'json',
  });
  return res.body;
}

async function fetchTotals(candidateId) {
  try {
    const body = await fecGet(`/candidate/${candidateId}/totals/`, { per_page: 1, sort: '-candidate_election_year' });
    return body.results?.[0] ?? null;
  } catch (err) {
    log.warning(`totals lookup failed for ${candidateId}: ${err.message}`);
    return null;
  }
}

try {
  let page = 1;
  let stop = false;
  while (!stop) {
    const body = await fecGet('/candidates/', {
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
      const totals = includeTotals ? await fetchTotals(c.candidate_id) : null;
      const item = {
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
        coverageStartDate: totals?.coverage_start_date ?? null,
        coverageEndDate: totals?.coverage_end_date ?? null,
      };
      const keepGoing = await pushResult(item);
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
log.info(`Done. Pushed ${pushed} results.`);
await Actor.exit();
