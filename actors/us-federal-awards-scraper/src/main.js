import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';

await Actor.init();
const input = (await Actor.getInput()) ?? {};

const API = 'https://api.usaspending.gov/api/v2/search/spending_by_award/';
const PAGE_SIZE = 100; // API max for this endpoint

// award_type_codes must come from ONE group per request — mixing contract and grant codes
// returns HTTP 400 "must only contain types from one group". So each selected category is
// its own paginated query and the results are merged here.
const CATEGORIES = {
    contracts: { codes: ['A', 'B', 'C', 'D'], kind: 'contract' },
    idvs: { codes: ['IDV_A', 'IDV_B', 'IDV_B_A', 'IDV_B_B', 'IDV_B_C', 'IDV_C', 'IDV_D', 'IDV_E'], kind: 'contract' },
    grants: { codes: ['02', '03', '04', '05'], kind: 'assistance' },
    direct_payments: { codes: ['06', '10'], kind: 'assistance' },
    other_financial_assistance: { codes: ['09', '11', '-1'], kind: 'assistance' },
    loans: { codes: ['07', '08'], kind: 'loan' },
};

// Every award kind has its own field mapping on the API. These are the fields verified to
// come back with data; asking for a field outside its kind's mapping is a 400.
const BASE_FIELDS = [
    'Award ID', 'Recipient Name', 'Recipient UEI', 'recipient_id',
    'Awarding Agency', 'Awarding Sub Agency', 'Funding Agency', 'Funding Sub Agency',
    'Description', 'Last Modified Date', 'Base Obligation Date',
    'Place of Performance State Code', 'Place of Performance Country Code', 'Place of Performance Zip5', 'pop_city_name',
    'recipient_location_city_name', 'recipient_location_state_code', 'recipient_location_country_name',
    'recipient_location_address_line1', 'generated_internal_id', 'def_codes',
];
const KIND_FIELDS = {
    contract: ['Award Amount', 'Total Outlays', 'Start Date', 'End Date', 'Contract Award Type', 'NAICS', 'PSC'],
    assistance: ['Award Amount', 'Total Outlays', 'Start Date', 'End Date', 'Award Type', 'Assistance Listings'],
    loan: ['Loan Value', 'Subsidy Cost', 'Issued Date', 'Award Type', 'Assistance Listings'],
};
// The API rejects any `sort` value that is not also in `fields` — so sorts are per-kind too.
const SORTS = {
    awardAmount: { contract: 'Award Amount', assistance: 'Award Amount', loan: 'Loan Value' },
    lastModifiedDate: { contract: 'Last Modified Date', assistance: 'Last Modified Date', loan: 'Last Modified Date' },
    startDate: { contract: 'Start Date', assistance: 'Start Date', loan: 'Issued Date' },
    recipientName: { contract: 'Recipient Name', assistance: 'Recipient Name', loan: 'Recipient Name' },
};

const categories = (input.awardCategories ?? ['contracts'])
    .map((c) => String(c).toLowerCase().trim())
    .filter((c) => Object.hasOwn(CATEGORIES, c));
if (!categories.length) categories.push('contracts');

const today = new Date();
const isoDay = (d) => d.toISOString().slice(0, 10);
// The API refuses time_period start dates before 2007-10-01.
const EARLIEST = '2007-10-01';
const endDate = input.endDate ? String(input.endDate).slice(0, 10) : isoDay(today);
const startDate = input.startDate
    ? String(input.startDate).slice(0, 10)
    : isoDay(new Date(today.getTime() - 365 * 86400_000));
const effectiveStart = startDate < EARLIEST ? EARLIEST : startDate;

const keywords = (input.keywords ?? []).map((k) => String(k).trim()).filter(Boolean);
const agencies = (input.agencies ?? []).map((a) => String(a).trim()).filter(Boolean);
const fundingAgencies = (input.fundingAgencies ?? []).map((a) => String(a).trim()).filter(Boolean);
const recipients = (input.recipients ?? []).map((r) => String(r).trim()).filter(Boolean);
const awardIds = (input.awardIds ?? []).map((a) => String(a).trim()).filter(Boolean);
const states = (input.placeOfPerformanceStates ?? []).map((s) => String(s).trim().toUpperCase()).filter(Boolean);
const recipientStates = (input.recipientStates ?? []).map((s) => String(s).trim().toUpperCase()).filter(Boolean);
const minAwardAmount = input.minAwardAmount != null ? Number(input.minAwardAmount) : null;
const maxAwardAmount = input.maxAwardAmount != null ? Number(input.maxAwardAmount) : null;
const sortBy = Object.hasOwn(SORTS, input.sortBy) ? input.sortBy : 'awardAmount';
const order = input.order === 'asc' ? 'asc' : 'desc';
const maxResults = Math.min(Math.max(Number(input.maxResults ?? 100), 1), 10000);
const maxPagesPerCategory = Math.min(Math.max(Number(input.maxPagesPerCategory ?? 50), 1), 200);

function buildFilters(codes) {
    const filters = {
        award_type_codes: codes,
        time_period: [{ start_date: effectiveStart, end_date: endDate }],
    };
    // Exact-ID lookup is exclusive: every other filter is dropped and the date window is
    // widened to the API's full supported range, so an award_ids match can never be silently
    // hidden by an unrelated filter — same trap class as grants-gov's oppNum, clinicaltrials'
    // nctIds and nih-reporter's projectNums.
    if (awardIds.length) {
        filters.award_ids = awardIds;
        filters.time_period = [{ start_date: EARLIEST, end_date: isoDay(today) }];
        return filters;
    }
    if (keywords.length) filters.keywords = keywords;
    if (recipients.length) filters.recipient_search_text = recipients;
    if (agencies.length || fundingAgencies.length) {
        filters.agencies = [
            ...agencies.map((name) => ({ type: 'awarding', tier: 'toptier', name })),
            ...fundingAgencies.map((name) => ({ type: 'funding', tier: 'toptier', name })),
        ];
    }
    if (states.length) {
        filters.place_of_performance_locations = states.map((state) => ({ country: 'USA', state }));
    }
    if (recipientStates.length) {
        filters.recipient_locations = recipientStates.map((state) => ({ country: 'USA', state }));
    }
    if (minAwardAmount != null || maxAwardAmount != null) {
        const bound = {};
        if (minAwardAmount != null) bound.lower_bound = minAwardAmount;
        if (maxAwardAmount != null) bound.upper_bound = maxAwardAmount;
        filters.award_amounts = [bound];
    }
    return filters;
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function postPage(body) {
    for (let attempt = 1; attempt <= 4; attempt += 1) {
        const resp = await gotScraping({
            url: API,
            method: 'POST',
            json: body,
            responseType: 'text', // error bodies are not always JSON; parse explicitly
            throwHttpErrors: false,
            retry: { limit: 0 },
            timeout: { request: 60000 },
            headers: { accept: 'application/json', 'content-type': 'application/json' },
        });

        if (resp.statusCode === 429 || resp.statusCode >= 500) {
            const waitS = Number(resp.headers['retry-after']) || attempt * 10;
            log.warning(`USAspending returned ${resp.statusCode}; retrying in ${waitS}s (${attempt}/4).`);
            await sleep(waitS * 1000);
            continue;
        }
        let parsed = null;
        try { parsed = JSON.parse(resp.body); } catch { /* handled below */ }
        if (resp.statusCode !== 200) {
            const detail = parsed?.detail ?? parsed?.message ?? String(resp.body).slice(0, 300);
            log.warning(`USAspending API ${resp.statusCode}: ${detail}`);
            return null;
        }
        if (!parsed) {
            log.warning(`USAspending returned a non-JSON body: ${String(resp.body).slice(0, 200)}`);
            return null;
        }
        return parsed;
    }
    log.warning('USAspending kept rate-limiting/erroring after 4 attempts; stopping this category early.');
    return null;
}

function uniq(arr) {
    return Array.from(new Set((arr ?? []).filter((v) => v != null && v !== '')));
}

function normalize(r, category, kind) {
    const gid = r.generated_internal_id ?? null;
    const listings = r['Assistance Listings'] ?? [];
    return {
        awardId: r['Award ID'] ?? null,
        awardUrl: gid ? `https://www.usaspending.gov/award/${encodeURIComponent(gid)}` : null,
        generatedInternalId: gid,
        awardCategory: category,
        awardType: r['Contract Award Type'] ?? r['Award Type'] ?? null,

        recipientName: r['Recipient Name'] ?? null,
        recipientUei: r['Recipient UEI'] ?? null,
        recipientId: r.recipient_id ?? null,
        recipientAddress: r.recipient_location_address_line1 ?? null,
        recipientCity: r.recipient_location_city_name ?? null,
        recipientState: r.recipient_location_state_code ?? null,
        recipientCountry: r.recipient_location_country_name ?? null,

        awardingAgency: r['Awarding Agency'] ?? null,
        awardingSubAgency: r['Awarding Sub Agency'] ?? null,
        fundingAgency: r['Funding Agency'] ?? null,
        fundingSubAgency: r['Funding Sub Agency'] ?? null,

        description: r.Description ?? null,

        // Loans report money as face value + subsidy cost instead of obligated/outlayed amounts.
        awardAmount: typeof r['Award Amount'] === 'number' ? r['Award Amount'] : null,
        totalOutlays: typeof r['Total Outlays'] === 'number' ? r['Total Outlays'] : null,
        loanValue: typeof r['Loan Value'] === 'number' ? r['Loan Value'] : null,
        subsidyCost: typeof r['Subsidy Cost'] === 'number' ? r['Subsidy Cost'] : null,

        startDate: r['Start Date'] ?? r['Issued Date'] ?? null,
        endDate: r['End Date'] ?? null,
        baseObligationDate: r['Base Obligation Date'] ?? null,
        lastModifiedDate: r['Last Modified Date'] ?? null,

        placeOfPerformanceCity: r.pop_city_name ?? null,
        placeOfPerformanceState: r['Place of Performance State Code'] ?? null,
        placeOfPerformanceZip: r['Place of Performance Zip5'] ?? null,
        placeOfPerformanceCountry: r['Place of Performance Country Code'] ?? null,

        naicsCode: r.NAICS?.code ?? null,
        naicsDescription: r.NAICS?.description ?? null,
        pscCode: r.PSC?.code ?? null,
        pscDescription: r.PSC?.description ?? null,
        cfdaNumbers: uniq(listings.map((l) => l.cfda_number)),
        cfdaProgramTitles: uniq(listings.map((l) => l.cfda_program_title)),
        disasterEmergencyFundCodes: uniq(r.def_codes),

        kind,
    };
}

let pushed = 0;
const isPPE = Actor.getChargingManager().getPricingInfo().isPayPerEvent;
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

if (awardIds.length) {
    log.info(`USAspending: exact award-ID lookup awardIds=[${awardIds.join(', ')}] (all other filters ignored) maxResults=${maxResults}`);
} else {
    log.info(
        `USAspending: categories=[${categories.join(',')}] ${effectiveStart}..${endDate} `
        + `sort=${sortBy} ${order} maxResults=${maxResults}`
        + (keywords.length ? ` keywords=[${keywords.join(', ')}]` : '')
        + (recipients.length ? ` recipients=[${recipients.join(', ')}]` : '')
        + (agencies.length ? ` agencies=[${agencies.join(', ')}]` : '')
        + (fundingAgencies.length ? ` fundingAgencies=[${fundingAgencies.join(', ')}]` : ''),
    );
}

const seen = new Set();
let scanned = 0;
let keepGoing = true;

for (const category of categories) {
    if (!keepGoing || pushed >= maxResults) break;
    const { codes, kind } = CATEGORIES[category];
    const fields = [...BASE_FIELDS, ...KIND_FIELDS[kind]];
    const sort = SORTS[sortBy][kind];
    const filters = buildFilters(codes);

    let page = 1;
    let categoryRows = 0;
    while (keepGoing && pushed < maxResults && page <= maxPagesPerCategory) {
        const body = await postPage({ filters, fields, page, limit: PAGE_SIZE, sort, order, subawards: false });
        if (!body) break;
        const results = body.results ?? [];
        if (!results.length) break;
        scanned += results.length;

        for (const row of results) {
            const key = row.generated_internal_id ?? `${category}:${row.internal_id}`;
            if (seen.has(key)) continue;
            seen.add(key);
            categoryRows += 1;
            keepGoing = await pushResult(normalize(row, category, kind));
            if (!keepGoing) break;
        }
        log.info(`${category} page ${page}: ${results.length} awards (pushed ${pushed}/${maxResults})`);
        if (!body.page_metadata?.hasNext) break;
        page += 1;
    }
    log.info(`${category}: pushed ${categoryRows} awards.`);
}

if (pushed === 0) {
    log.warning(
        `No awards matched. Scanned ${scanned} rows. Most common causes, in order: `
        + '(1) the filters are ANDed — a keyword plus a state plus a minimum amount over a short date window '
        + 'often has zero real matches; drop one filter and retry. '
        + '(2) "agencies" must be the exact top-tier agency name as USAspending spells it '
        + '(e.g. "Department of Energy", not "DOE" or "Energy"). '
        + '(3) the date window filters on award action date — widen "startDate"/"endDate" '
        + '(dates before 2007-10-01 are not supported by the API and are clamped). '
        + '(4) state codes must be 2-letter USPS codes (CA, TX). Rows that match nothing are never charged.',
    );
}

log.info(`Done. Scanned ${scanned} awards, pushed ${pushed}.`);
await Actor.exit();
