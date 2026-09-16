import { createHash } from 'crypto';
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

// Sub-award rows come from the same endpoint with `subawards: true`, but they have their own
// field mapping — asking for a prime-award field (e.g. "Award Amount") there is a 400. This
// list is the API's own Sub-Award mapping, taken verbatim from its 400 error text.
const SUB_FIELDS = [
    'Sub-Award ID', 'Sub-Award Type', 'Sub-Awardee Name', 'Sub-Award Date', 'Sub-Award Amount',
    'Sub-Award Description', 'Sub-Recipient UEI',
    'Awarding Agency', 'Awarding Sub Agency',
    'Prime Award ID', 'Prime Recipient Name', 'Prime Award Recipient UEI', 'prime_award_recipient_id',
];
// Sub-awards carry no "last modified" date; that sort falls back to the sub-award action date.
const SUB_SORTS = {
    awardAmount: 'Sub-Award Amount',
    lastModifiedDate: 'Sub-Award Date',
    startDate: 'Sub-Award Date',
    recipientName: 'Sub-Awardee Name',
};

const isSubaward = String(input.awardLevel ?? 'prime').toLowerCase().trim() === 'subaward';

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
const naicsCodes = (input.naicsCodes ?? []).map((c) => String(c).trim()).filter(Boolean);
// The API rejects anything but 1-4 uppercase alphanumerics with a 422, so uppercase here
// (buyers type "r425") and fail fast on the rest with a message that names the bad code.
const pscCodes = (input.pscCodes ?? []).map((c) => String(c).trim().toUpperCase()).filter(Boolean);
const badPsc = pscCodes.find((c) => !/^[A-Z0-9]{1,4}$/.test(c));
if (badPsc) {
  throw new Error(`"pscCodes" entry ${JSON.stringify(badPsc)} is not a PSC code — must be 1 to 4 letters/digits, e.g. "R425" (leaf), "R4" or "10" (prefix group), "R" (whole category).`);
}
const minAwardAmount = input.minAwardAmount != null ? Number(input.minAwardAmount) : null;
const maxAwardAmount = input.maxAwardAmount != null ? Number(input.maxAwardAmount) : null;
if (minAwardAmount != null && maxAwardAmount != null && minAwardAmount > maxAwardAmount) {
  throw new Error(`"minAwardAmount" (${minAwardAmount}) is greater than "maxAwardAmount" (${maxAwardAmount}) — no award can ever match. Swap them.`);
}
const sortBy = Object.hasOwn(SORTS, input.sortBy) ? input.sortBy : 'awardAmount';
const order = input.order === 'asc' ? 'asc' : 'desc';
const maxResults = Math.min(Math.max(Number(input.maxResults ?? 100), 1), 10000);
const maxPagesPerCategory = Math.min(Math.max(Number(input.maxPagesPerCategory ?? 50), 1), 200);
const watchLabel = String(input.watchLabel ?? '').trim();

// Watch mode: a stateful "only new awards/sub-awards since my last run" filter. Both prime
// and sub-award mode have a real "new since last time" concept (new awards get made, new
// sub-awards get filed), unlike FEC's candidates mode which returns a fixed roster. The
// baseline (award/sub-award ids already delivered under this label+filter set) lives in a
// NAMED key-value store on the buyer's own account so it survives across runs.
const WATCH_STORE = 'fetchsmith-usaspending-watch';
const SEED_CAP = 20000; // bound the cost of a baseline run against a broad/unfiltered category
const WATCH_KEEP = 20000; // bound the record size; oldest ids fall off first
// Per-category page cap used only while seeding, independent of the buyer's own
// maxPagesPerCategory cost cap -- same fix as eu-ted-tenders/uk-find-a-tender: the buyer's
// own scan-depth budget must never also bound how comprehensive a baseline is, or an
// incremental run would report older, merely-unscanned awards as "new".
const SEED_PAGE_CAP = 1000;

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
const watchSeen = new Set(); // award/sub-award ids already delivered under this label+fingerprint

if (watchMode) {
  // When awardIds is set every other filter is dropped by buildFilters (exact-ID lookup), so
  // the fingerprint follows that override instead of also keying on filters with no effect on
  // the actual query sent -- same rule eu-ted-tenders applies to its expertQuery override.
  const criteria = awardIds.length
    ? { awardLevel: isSubaward ? 'subaward' : 'prime', awardIds: [...awardIds].sort() }
    : {
      awardLevel: isSubaward ? 'subaward' : 'prime',
      categories: [...categories].sort(),
      keywords: [...keywords].sort(),
      agencies: [...agencies].sort(),
      fundingAgencies: [...fundingAgencies].sort(),
      recipients: [...recipients].sort(),
      states: [...states].sort(),
      recipientStates: [...recipientStates].sort(),
      naicsCodes: [...naicsCodes].sort(),
      pscCodes: [...pscCodes].sort(),
      minAwardAmount: minAwardAmount ?? null,
      maxAwardAmount: maxAwardAmount ?? null,
      // Raw buyer input, not the resolved value -- startDate/endDate default to "one year
      // ago"/"today" and roll forward every single day, so fingerprinting the resolved value
      // would force a fresh baseline daily (a daily version of the cycle-297 FEC electionYear
      // trap, which only rolls every two years).
      startDateRaw: input.startDate ?? null,
      endDateRaw: input.endDate ?? null,
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
      + `${watchSeen.size} already-delivered award(s)/sub-award(s). Only ones NOT in that baseline will be returned and charged.`,
    );
  } else {
    watchRecord = { fingerprint, firstSeededAt: new Date().toISOString(), runCount: 0 };
    seeding = true;
    log.info(
      `Watch mode "${watchLabel}" (${key}): FIRST run for this label and filter set, so this is a baseline `
      + 'run. It records which awards/sub-awards already match and returns ZERO results (you are charged nothing). '
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
    // 2/4/6-digit NAICS prefixes are all accepted and ORed by the API; grants/loans have no
    // NAICS so this filter just returns nothing for those categories rather than erroring.
    if (naicsCodes.length) filters.naics_codes = { require: naicsCodes };
    // PSC takes the flat-list form (NOT the tiered ["Service","R","R4","R425"] paths the
    // filter-tree endpoint returns — those only work inside `require`). 1-4 char prefixes are
    // all accepted and ORed, verified: R425 17,465 + R499 71,409 = 88,874 for the pair, exactly.
    // Only contracts/IDVs carry a PSC, so grants/loans/direct payments return nothing here.
    if (pscCodes.length) filters.psc_codes = pscCodes;
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

function normalizeSub(r, category) {
    const primeGid = r.prime_award_generated_internal_id ?? null;
    return {
        awardLevel: 'subaward',
        subAwardId: r['Sub-Award ID'] ?? null,
        subAwardType: r['Sub-Award Type'] ?? null,
        subAwardDate: r['Sub-Award Date'] ?? null,
        subAwardAmount: typeof r['Sub-Award Amount'] === 'number' ? r['Sub-Award Amount'] : null,
        subAwardDescription: r['Sub-Award Description'] ?? null,

        subRecipientName: r['Sub-Awardee Name'] ?? null,
        subRecipientUei: r['Sub-Recipient UEI'] ?? null,

        primeAwardId: r['Prime Award ID'] ?? null,
        primeRecipientName: r['Prime Recipient Name'] ?? null,
        primeRecipientUei: r['Prime Award Recipient UEI'] ?? null,
        primeRecipientId: r.prime_award_recipient_id ?? null,
        primeAwardGeneratedInternalId: primeGid,
        // Same URL shape as a prime row's awardUrl, so a sub-award row can be joined straight
        // back to the prime award page (or to a prime-level run of this Actor).
        primeAwardUrl: primeGid ? `https://www.usaspending.gov/award/${encodeURIComponent(primeGid)}` : null,

        awardingAgency: r['Awarding Agency'] ?? null,
        awardingSubAgency: r['Awarding Sub Agency'] ?? null,

        awardCategory: category,
        kind: 'subaward',
    };
}

let pushed = 0;
const isPPE = Actor.getChargingManager().getPricingInfo().isPayPerEvent;
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

if (awardIds.length) {
    log.info(
        `USAspending: exact award-ID lookup awardIds=[${awardIds.join(', ')}] (all other filters ignored) maxResults=${maxResults}`
        + (isSubaward ? ' — in subaward mode these are PRIME award IDs; every sub-award under them is returned' : ''),
    );
} else {
    log.info(
        `USAspending: level=${isSubaward ? 'subaward' : 'prime'} categories=[${categories.join(',')}] ${effectiveStart}..${endDate} `
        + `sort=${sortBy} ${order} maxResults=${maxResults}`
        + (keywords.length ? ` keywords=[${keywords.join(', ')}]` : '')
        + (recipients.length ? ` recipients=[${recipients.join(', ')}]` : '')
        + (agencies.length ? ` agencies=[${agencies.join(', ')}]` : '')
        + (fundingAgencies.length ? ` fundingAgencies=[${fundingAgencies.join(', ')}]` : '')
        + (naicsCodes.length ? ` naicsCodes=[${naicsCodes.join(', ')}]` : '')
        // Log the codes as actually sent (uppercased): an unrecognised PSC returns zero rows
        // instead of erroring, so this line is what makes an empty run diagnosable.
        + (pscCodes.length ? ` pscCodes=[${pscCodes.join(', ')}]` : ''),
    );
}

const seen = new Set();
let scanned = 0;
let keepGoing = true;

for (const category of categories) {
    if (!keepGoing || pushed >= maxResults) break;
    const { codes, kind } = CATEGORIES[category];
    const fields = isSubaward ? SUB_FIELDS : [...BASE_FIELDS, ...KIND_FIELDS[kind]];
    const sort = isSubaward ? SUB_SORTS[sortBy] : SORTS[sortBy][kind];
    const filters = buildFilters(codes);
    // While seeding a watch baseline, scan deeper than the buyer's own maxPagesPerCategory so
    // the baseline reflects the whole current match set, not just its first N pages. Incremental
    // runs keep the buyer's own cap unchanged: it's an honest scan-depth cost control here (see
    // its schema description), not a delivery limit doing double duty as one (unlike the
    // ats-jobs/hacker-news traps), so it's the buyer's own choice for a normal run either way.
    const pageCap = seeding ? Math.max(maxPagesPerCategory, SEED_PAGE_CAP) : maxPagesPerCategory;

    let page = 1;
    let categoryRows = 0;
    while (keepGoing && pushed < maxResults && page <= pageCap) {
        const body = await postPage({ filters, fields, page, limit: PAGE_SIZE, sort, order, subawards: isSubaward });
        if (!body) break;
        const results = body.results ?? [];
        if (!results.length) break;
        scanned += results.length;

        for (const row of results) {
            const key = isSubaward
                ? `sub:${row.internal_id ?? row['Sub-Award ID']}`
                : row.generated_internal_id ?? `${category}:${row.internal_id}`;
            if (seen.has(key)) continue;
            seen.add(key);
            categoryRows += 1;
            keepGoing = await pushResult(isSubaward ? normalizeSub(row, category) : normalize(row, category, kind), key);
            if (!keepGoing) break;
        }
        log.info(`${category} page ${page}: ${results.length} ${isSubaward ? 'sub-awards' : 'awards'} (pushed ${pushed}/${maxResults})`);
        if (!body.page_metadata?.hasNext) break;
        page += 1;
    }
    log.info(`${category}: pushed ${categoryRows} ${isSubaward ? 'sub-awards' : 'awards'}.`);
}

if (watchMode) {
    await saveWatchRecord(seeding ? 'seeded' : 'incremental');
    if (seeding) {
        log.info(
            `Baseline saved for watch label "${watchLabel}": ${watchSeen.size} award(s)/sub-award(s) recorded as `
            + 'already-seen, 0 results returned, 0 charged. The next run on this label and these filters returns '
            + 'only what is new.'
            + (watchSeen.size >= SEED_CAP
                ? ` NOTE: the baseline hit the ${SEED_CAP}-record cap. Narrow the filters so the whole current match `
                    + 'set fits, or the first incremental run may report older, merely-unscanned awards as new.'
                : ''),
        );
        await Actor.setStatusMessage(`Baseline run for watch label "${watchLabel}": ${watchSeen.size} existing award(s)/sub-award(s) recorded, 0 charged. Run again later to get only what's new.`);
    } else {
        log.info(`Watch label "${watchLabel}": ${pushed} new award(s)/sub-award(s) since the last run (${watchSkipped} already-delivered hit(s) skipped, not charged); baseline now holds ${watchSeen.size}.`);
        if (pushed === 0) {
            await Actor.setStatusMessage(`Nothing new for watch label "${watchLabel}" since its last run -- every matching award/sub-award had already been delivered. That is the expected result most of the time; you were charged for nothing.`);
        }
    }
}

if (pushed === 0 && !watchMode) {
    log.warning(
        `No awards matched. Scanned ${scanned} rows. Most common causes, in order: `
        + '(1) the filters are ANDed — a keyword plus a state plus a minimum amount over a short date window '
        + 'often has zero real matches; drop one filter and retry. '
        + '(2) "agencies" must be the exact top-tier agency name as USAspending spells it '
        + '(e.g. "Department of Energy", not "DOE" or "Energy"). '
        + '(3) the date window filters on award action date — widen "startDate"/"endDate" '
        + '(dates before 2007-10-01 are not supported by the API and are clamped). '
        + '(4) state codes must be 2-letter USPS codes (CA, TX). Rows that match nothing are never charged.'
        + (isSubaward
            ? ' (5) awardLevel="subaward" only covers prime awards whose recipient filed FSRS sub-award reports — '
                + 'small awards and most loans/direct payments have none; try awardLevel="prime" to confirm the prime award exists.'
            : ''),
    );
}

log.info(`Done. Scanned ${scanned} ${isSubaward ? 'sub-awards' : 'awards'}, pushed ${pushed}.`);
await Actor.exit();
