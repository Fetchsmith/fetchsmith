import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';
import { createHash } from 'node:crypto';

await Actor.init();
const input = (await Actor.getInput()) ?? {};

// SAM.gov's OFFICIAL developer API (api.sam.gov/opportunities/v2/search) requires a free
// registered API key (confirmed against open.gsa.gov's own docs, cycle 538). This Actor instead
// uses the same undocumented, unauthenticated backend that powers sam.gov's own public search
// PAGE -- verified live cycle 538/539 with 5+ spaced requests (all 200, ~0.2s, no block/challenge)
// and real pagination/filters. Same class of finding as trademark-search-scraper's TMview
// endpoint (cycle 512): a public government site's own search-UI backend, not its registered
// developer API, no ToS click-through, no login, no key.
const SEARCH_API = 'https://sam.gov/api/prod/sgs/v1/search/';
const DETAIL_API = 'https://sam.gov/api/prod/opps/v2/opportunities';

// The SAME keyless backend multiplexes several of SAM.gov's public data types behind `index=`
// (cycle 703's rule, cycle 704's build). Probed live cycle 704/707, all 200 OK with no key/login:
//   index=opp  -> contract opportunities (what this Actor shipped with)
//   index=dbra -> Davis-Bacon Act construction wage determinations (`_type: wdDBRA`, 85,426)
//   index=wd   -> Collective Bargaining Agreement wage determinations (`_type: wdCBA`, 107,580)
//   index=sca  -> Service Contract Act wage determinations (`_type: wdSCA`, 2,666)
//   index=cfda -> CFDA assistance listings -- grants/loans/direct-payment programs
//                 (`_type: assistanceListing`, 7,392, ~2,871 active)
// `index=dbra` was NOT in cycle 703's scoping (it guessed `dba`/`wdol`/`davisbacon`, all 400) --
// `wd` alone is CBA-only, so shipping just `wd` would have silently omitted the Davis-Bacon set,
// which is the one construction contractors actually need. One index per run on purpose: the
// completeness machinery below measures ONE `page.totalElements` per run, and merging two indices
// would make `declaredMatches` unreadable.
const DATA_TYPES = {
    'opportunities': { index: 'opp', noun: 'opportunity', nounPlural: 'opportunities' },
    'wage-determinations-dbra': { index: 'dbra', noun: 'wage determination', nounPlural: 'wage determinations' },
    'wage-determinations-cba': { index: 'wd', noun: 'wage determination', nounPlural: 'wage determinations' },
    'wage-determinations-sca': { index: 'sca', noun: 'wage determination', nounPlural: 'wage determinations' },
    'assistance-listings': { index: 'cfda', noun: 'assistance listing', nounPlural: 'assistance listings' },
};
// A 3rd distinct row family (opp / wd / cfda) needs its own dispatch, not a 2-way `isWd` boolean
// (cycle 706's note) -- one map from dataType to family, `isWd`/`isCfda` derived from it below.
const DATA_TYPE_FAMILY = {
    'opportunities': 'opp',
    'wage-determinations-dbra': 'wd',
    'wage-determinations-cba': 'wd',
    'wage-determinations-sca': 'wd',
    'assistance-listings': 'cfda',
};

// Confirmed live cycle 539: `notice_type` takes SAM's own single-letter codes (matches the
// codes SAM shows in the UI dropdown / that come back on each row's `type.code`).
const NOTICE_TYPE_CODES = {
    p: 'Presolicitation', o: 'Solicitation', k: 'Combined Synopsis/Solicitation',
    r: 'Sources Sought', a: 'Award Notice', s: 'Special Notice', g: 'Sale of Surplus',
    i: 'Intent to Bundle', u: 'Justification',
};

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// ---------------------------------------------------------------------------
// Run-level completeness (cycle 649, h250 class). Before this, EVERY way this Actor could come up
// short was invisible to a pipeline: a page that 500s mid-walk just `break`s out of fetchRows(),
// SAM's 10,000-row backend depth cap only produced an English log line, maxResults and the PPE
// charge limit stopped the push loop silently, and `totalElements` -- the only number that says how
// many opportunities actually matched -- was never written anywhere the buyer can read. 200 rows of
// a 12,297-match query looked exactly like exhausting a 200-match query. Same contract as
// nih-reporter-scraper / fda-recall-scraper / clinicaltrials-scraper: a RUN_SUMMARY key-value
// record, a status message, and the same object on the webhook payload.
let declaredMatches = null;   // SAM's own page.totalElements for this query; null = never answered, NEVER 0
let scanned = 0;              // raw search rows read back from the API
let pages = 0;
let pagesFailed = 0;
let duplicateRowsDropped = 0; // rows SAM.gov served more than once; dropped before any charge
let complete = true;
let incompleteReason = null;
let incompleteDetail = null;
let lastApiError = null;      // WHY the most recent null happened, carried into RUN_SUMMARY

// First cause wins: a walk that stopped because SAM stopped answering and THEN also hit maxResults
// must keep reporting the upstream failure -- that is the cause the buyer can act on.
function markIncomplete(reason, detail = null) {
    if (!complete) return;
    complete = false;
    incompleteReason = reason;
    incompleteDetail = detail;
}

async function apiGet(url) {
    for (let attempt = 1; attempt <= 4; attempt += 1) {
        let resp;
        try {
            resp = await gotScraping({
                url,
                method: 'GET',
                responseType: 'text',
                throwHttpErrors: false,
                retry: { limit: 0 },
                timeout: { request: 30000 },
                headers: { accept: 'application/hal+json' }, // required: plain application/json 406s (cycle 539)
            });
        } catch (err) {
            lastApiError = `request error: ${err.message}`;
            log.warning(`SAM.gov request failed (${err.message}); retrying (${attempt}/4).`);
            await sleep(attempt * 2000);
            continue;
        }
        if (resp.statusCode === 429 || resp.statusCode >= 500) {
            lastApiError = `HTTP ${resp.statusCode}`;
            log.warning(`SAM.gov returned ${resp.statusCode}; retrying (${attempt}/4).`);
            await sleep(attempt * 3000);
            continue;
        }
        if (resp.statusCode === 404) { lastApiError = 'HTTP 404'; return null; }
        let parsed = null;
        try { parsed = JSON.parse(resp.body); } catch { /* handled below */ }
        if (resp.statusCode !== 200 || !parsed) {
            lastApiError = `HTTP ${resp.statusCode}, non-JSON or unexpected body`;
            log.warning(`SAM.gov ${url} returned ${resp.statusCode}, non-JSON or unexpected body: ${String(resp.body).slice(0, 200)}`);
            return null;
        }
        return parsed;
    }
    lastApiError = lastApiError ?? 'exhausted 4 attempts';
    log.warning(`SAM.gov ${url} kept failing after 4 attempts; skipping.`);
    return null;
}

const dataTypeRaw = String(input.dataType ?? 'opportunities').trim();
const dataType = Object.hasOwn(DATA_TYPES, dataTypeRaw) ? dataTypeRaw : 'opportunities';
if (dataType !== dataTypeRaw) {
    log.warning(`dataType "${dataTypeRaw}" is not one of ${Object.keys(DATA_TYPES).join(', ')}; falling back to "opportunities".`);
}
const { index: SEARCH_INDEX, noun: ROW_NOUN, nounPlural: ROW_NOUN_PLURAL } = DATA_TYPES[dataType];
const recordFamily = DATA_TYPE_FAMILY[dataType];
const isWd = recordFamily === 'wd';
const isCfda = recordFamily === 'cfda';

// Cycle 96 seed rule: never ship a default that makes the very first test run return 0 rows.
// On the wage-determination indices a keyword is the WRONG default: `q` there matches the
// determination's reference number, not the trades inside it (measured cycle 704: `q=roofing`
// returns 0 against 85,426 live Davis-Bacon rows), so defaulting to "contract" would hand a first
// run an empty dataset. Seed those modes with no keyword instead -- an unfiltered wd query is
// itself a valid, large result set. `q=contract` on the cfda index is technically non-zero
// (176/7,392, measured cycle 707) but is a construction/procurement term that has nothing to do
// with grant programs and would bias a first-run sample toward an unrepresentative slice --
// same "no keyword" treatment as wd, for a different reason (irrelevance, not a zero-match trap).
const keyword = String(input.keyword ?? (isWd || isCfda ? '' : 'contract')).trim();
const naicsCodes = (Array.isArray(input.naicsCodes) ? input.naicsCodes : []).map((v) => String(v).trim()).filter(Boolean);
const setAsideTypes = (Array.isArray(input.setAsideTypes) ? input.setAsideTypes : []).map((v) => String(v).trim()).filter(Boolean);
const noticeTypes = (Array.isArray(input.noticeTypes) ? input.noticeTypes : [])
    .map((v) => String(v).toLowerCase().trim())
    .filter((v) => Object.hasOwn(NOTICE_TYPE_CODES, v));
const states = (Array.isArray(input.states) ? input.states : []).map((v) => String(v).toUpperCase().trim()).filter(Boolean);
const organizationId = String(input.organizationId ?? '').trim();
const activeOnly = input.activeOnly !== false; // default true
let enrichDetail = input.enrichDetail === true;

// Filters that only exist on the opportunity index. Silently ignoring them in a wage-determination
// run would return a full 10,000-row unfiltered set that LOOKS filtered -- and every row is billed.
if (isWd) {
    const ignored = [];
    if (naicsCodes.length) ignored.push('naicsCodes');
    if (setAsideTypes.length) ignored.push('setAsideTypes');
    if (noticeTypes.length) ignored.push('noticeTypes');
    if (organizationId) ignored.push('organizationId');
    if (ignored.length) {
        log.warning(
            `${ignored.join(', ')} ${ignored.length === 1 ? 'is' : 'are'} only supported for dataType "opportunities" `
            + `and ${ignored.length === 1 ? 'was' : 'were'} IGNORED for "${dataType}". SAM.gov's wage-determination `
            + 'indices are filterable by state (`states`), active status (`activeOnly`) and reference-number keyword '
            + '(`keyword`) only -- your results are NOT narrowed by the ignored filter(s).',
        );
    }
    if (enrichDetail) {
        // Probed cycle 704: only CBA has a keyless per-record detail endpoint
        // (sam.gov/api/prod/wdol/v1/cba/<id>); the dbra/sca equivalents 404 on every guessed path.
        // Rather than enrich one of three modes asymmetrically, enrichment is opportunity-only.
        log.warning(`enrichDetail is only supported for dataType "opportunities"; ignored for "${dataType}".`);
        enrichDetail = false;
    }
}
// The cfda index shares `organization_id` with opportunities (confirmed live cycle 707:
// `organization_id=100000000` -> 189 programs, same param name), so it is NOT ignored here.
// `states`/`state` are confirmed NO-OPs on this index (both return the unfiltered 7,392 total --
// assistance-listing programs are nationwide, not place-of-performance filtered), so silently
// accepting them would look filtered while charging for the full unfiltered set.
if (isCfda) {
    const ignored = [];
    if (naicsCodes.length) ignored.push('naicsCodes');
    if (setAsideTypes.length) ignored.push('setAsideTypes');
    if (noticeTypes.length) ignored.push('noticeTypes');
    if (states.length) ignored.push('states');
    if (ignored.length) {
        log.warning(
            `${ignored.join(', ')} ${ignored.length === 1 ? 'is' : 'are'} only supported for dataType "opportunities" `
            + `and ${ignored.length === 1 ? 'was' : 'were'} IGNORED for "assistance-listings". SAM.gov's assistance-listing `
            + 'index is filterable by keyword (`keyword`, matches title/objective/program number), active status '
            + '(`activeOnly`) and organization (`organizationId`) only -- your results are NOT narrowed by the ignored filter(s).',
        );
    }
    if (enrichDetail) {
        // No keyless per-record detail endpoint probed for cfda (cycle 707) -- the search row
        // already carries the full record (financial/eligibility/contacts), so there is nothing a
        // detail call would add. Opportunity-only, same reasoning as the wd branch above.
        log.warning(`enrichDetail is only supported for dataType "opportunities"; ignored for "${dataType}".`);
        enrichDetail = false;
    }
}
const maxResults = Math.min(Math.max(Number(input.maxResults ?? 200), 1), 10000); // 10k = confirmed backend depth cap (cycle 538)
const watchLabel = String(input.watchLabel ?? '').trim();
const watchChanges = Boolean(input.watchChanges);
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

log.info(`Starting SAM.gov ${ROW_NOUN} search (dataType=${dataType}, index=${SEARCH_INDEX})`, {
    keyword, naicsCodes, setAsideTypes, noticeTypes, states, organizationId, activeOnly, maxResults, enrichDetail, watchLabel,
});

function buildSearchUrl(page, size) {
    if (isWd) {
        const params = new URLSearchParams({
            index: SEARCH_INDEX, responseType: 'json',
            page: String(page), size: String(size),
        });
        if (keyword) params.set('q', keyword);
        if (activeOnly) params.set('is_active', 'true');
        // The state param is `state`, NOT the opportunity index's `pop_state` -- measured live
        // cycle 704: `state=AL` -> 3,509 and `state=TX` -> 6,909 on index=wd, while `pop_state=AL`
        // returns 0 (applied, matches nothing) and an unrecognised name like `wd_state=AL` returns
        // the unfiltered 107,580. Comma-join is a true OR, same as the opportunity filters:
        // `state=AL,TX` -> 10,415, i.e. 3,509 + 6,909 minus the 3 determinations covering both;
        // repeating the key (`state=AL&state=TX`) first-wins at 3,509 and fails OPEN, so never do it.
        if (states.length) params.set('state', states.join(','));
        return `${SEARCH_API}?${params.toString()}`;
    }
    if (isCfda) {
        const params = new URLSearchParams({
            index: SEARCH_INDEX, responseType: 'json',
            page: String(page), size: String(size),
        });
        if (keyword) params.set('q', keyword);
        if (activeOnly) params.set('is_active', 'true');
        if (organizationId) params.set('organization_id', organizationId);
        return `${SEARCH_API}?${params.toString()}`;
    }
    // `mode=search` truncates `descriptions[0].content` to 250 chars server-side -- confirmed by
    // diffing identical queries with/without it (cycle 567): same `totalElements`, same row ids
    // per page (intra-page order can differ on relevance ties, never drops/adds a row), but content
    // length caps at exactly 250 with the param and runs up to 37k+ chars without it. Omitting it
    // is a zero-new-request way to deliver the FULL solicitation description text.
    const params = new URLSearchParams({
        index: 'opp', responseType: 'json',
        page: String(page), size: String(size),
    });
    if (keyword) params.set('q', keyword);
    if (activeOnly) params.set('is_active', 'true');
    if (organizationId) params.set('organization_id', organizationId);
    // Multi-value params must be COMMA-JOINED, not repeated. Measured live cycle 540 by
    // result-count arithmetic: `naics=541511`->607 and `naics=541512`->312, but repeating the key
    // (`naics=541511&naics=541512`) returns 607 -- silently first-wins, dropping the rest -- while
    // `naics=541511,541512` returns exactly 919 = 607+312, a true OR. Same confirmed for
    // pop_state (TX 592 + CA 767 = TX,CA 1359) and notice_type (p 4016 + o 8281 = p,o 12297).
    // Repeating the key fails OPEN (plausible-looking under-count, no error), so never go back.
    if (naicsCodes.length) params.set('naics', naicsCodes.join(','));
    if (setAsideTypes.length) params.set('set_aside', setAsideTypes.join(','));
    if (noticeTypes.length) params.set('notice_type', noticeTypes.join(','));
    if (states.length) params.set('pop_state', states.join(','));
    return `${SEARCH_API}?${params.toString()}`;
}

function orgField(hierarchy, type) {
    const row = (hierarchy ?? []).find((h) => h.type === type);
    return row ? row.name : null;
}

function normalizeRow(row) {
    const id = row._id;
    return {
        opportunityId: id,
        title: row.title ?? null,
        solicitationNumber: row.solicitationNumber ?? null,
        noticeTypeCode: row.type?.code ?? null,
        noticeType: row.type?.value ?? null,
        isActive: row.isActive ?? null,
        isCanceled: row.isCanceled ?? null,
        publishDate: row.publishDate ?? null,
        modifiedDate: row.modifiedDate ?? null,
        responseDate: row.responseDate ?? null,
        responseDateActual: row.responseDateActual ?? null,
        responseTimeZone: row.responseTimeZone ?? null,
        department: orgField(row.organizationHierarchy, 'DEPARTMENT'),
        agency: orgField(row.organizationHierarchy, 'AGENCY'),
        office: orgField(row.organizationHierarchy, 'OFFICE'),
        description: row.descriptions?.[0]?.content ?? null,
        awardeeName: row.award?.awardee?.name ?? null,
        awardeeUeiSAM: row.award?.awardee?.ueiSAM ?? null,
        modificationsCount: row.modifications?.count ?? 0,
        sourceUrl: id ? `https://sam.gov/opp/${id}/view` : null,
        // Detail-only fields, filled in only when enrichDetail is on (extra HTTP call per row).
        naicsCodes: null,
        setAside: null,
        placeOfPerformanceState: null,
        placeOfPerformanceCountry: null,
        pointOfContact: null,
    };
}

// The three wage-determination indices describe the same thing in three different location shapes,
// all confirmed against live rows (cycle 704):
//   wdDBRA  location.state  = { code, name, counties: [{code, value}] }      (singular object)
//   wdCBA   location.states = [{ code, name, counties: [{code, value}] }]    (array)
//   wdSCA   location.states = [{ code, name, isStateWide, counties: { include: [...], exclude: [...] } }]
// Flattened to one `coverage` array so a buyer writes one parser, not three. SCA's `exclude` list is
// kept as its own field rather than folded into the county list -- an excluded county is the exact
// opposite of a covered one, and silently merging them would be a wrong answer, not a lossy one.
function countyNames(counties) {
    if (Array.isArray(counties)) return counties.map((c) => c?.value ?? null).filter(Boolean);
    if (Array.isArray(counties?.include)) return counties.include.map((c) => c?.value ?? null).filter(Boolean);
    return [];
}
function excludedCountyNames(counties) {
    return Array.isArray(counties?.exclude) ? counties.exclude.map((c) => c?.value ?? null).filter(Boolean) : [];
}
function coverageOf(location) {
    const states = Array.isArray(location?.states) ? location.states : (location?.state ? [location.state] : []);
    return states.map((s) => ({
        stateCode: s?.code ?? null,
        stateName: s?.name ?? null,
        isStateWide: s?.isStateWide ?? null,
        counties: countyNames(s?.counties),
        excludedCounties: excludedCountyNames(s?.counties),
    }));
}

// `publishDate` comes back as an ISO string on wdCBA but as epoch MILLISECONDS on wdDBRA/wdSCA
// (measured live cycle 704: 1789617600000). Emitting both shapes under one field name would make
// every downstream date parse a coin flip, so normalise to ISO here.
function toIso(value) {
    if (value === null || value === undefined) return null;
    if (typeof value === 'number') return new Date(value).toISOString();
    return String(value);
}

function normalizeWdRow(row) {
    const id = row._id;
    const coverage = coverageOf(row.location);
    return {
        wageDeterminationId: id === null || id === undefined ? null : String(id),
        // wdDBRA/wdSCA carry `fullReferenceNumber` (e.g. "AK20260001", "2014-0333"); wdCBA carries
        // `cbaNumber` (e.g. "CBA-2003-2"). `title` mirrors whichever exists on all three.
        referenceNumber: row.fullReferenceNumber ?? row.cbaNumber ?? row.title ?? null,
        shortReferenceNumber: row.shortReferenceNumber ?? null,
        title: row.title ?? null,
        actCode: row.type?.code ?? null,       // DBA | SCA | CBA
        actName: row.type?.value ?? null,      // Davis-Bacon Act | Service Contract Act | Collective Bargaining Agreement
        recordType: row._type ?? null,         // wdDBRA | wdSCA | wdCBA
        isActive: row.isActive ?? null,
        isLatest: row.isLatest ?? null,
        isStandard: row.isStandard ?? null,
        revisionNumber: typeof row.revisionNumber === 'number' ? row.revisionNumber : null,
        year: typeof row.year === 'number' ? row.year : null,
        publishDate: toIso(row.publishDate),
        modifiedDate: toIso(row.modifiedDate),
        // DBRA only: which kinds of construction the schedule applies to (Building/Heavy/Highway/
        // Residential). SCA only: the service categories it covers.
        constructionTypes: Array.isArray(row.constructionTypes) ? row.constructionTypes : null,
        services: Array.isArray(row.services)
            ? row.services.map((s) => ({ code: s?.code ?? null, name: s?.value ?? null, description: s?.description ?? null }))
            : null,
        coverage,
        stateCodes: coverage.map((c) => c.stateCode).filter(Boolean),
        countyCount: coverage.reduce((n, c) => n + c.counties.length, 0),
        // Per-occupation wage RATE schedules are not on the search row for any of the three
        // indices, and only wdCBA has a keyless per-record detail endpoint (cycle 704), so this
        // Actor delivers the determination index -- which determination applies where, and whether
        // it is current -- not the rate tables. Said plainly here and in the README so nobody buys
        // rows expecting hourly rates.
        wageRates: null,
    };
}

// cfda's organizationHierarchy entries carry NO `type` field (unlike opp's, which orgField()
// above reads) -- only `level` (1 = department, 2 = agency, checked live cycle 707 against real
// records; a 3rd level was never observed in samples but the accessor stays general). Do NOT
// reuse orgField() for cfda rows -- it would silently return null for every one of them.
function orgFieldByLevel(hierarchy, level) {
    const row = (hierarchy ?? []).find((h) => h.level === level);
    return row ? row.name : null;
}

// CFDA (Catalog of Federal Domestic Assistance) rows describe grant/loan/direct-payment programs,
// a structurally richer family than opp/wd -- confirmed live cycle 707. `_id` is a stable 32-char
// hex id (same role as opp's `_id`). `programNumber` (e.g. "12.103") is the reference number
// buyers actually search by, same role as wd's `referenceNumber`. `publishDate`/`modifiedDate` are
// ISO strings on every sample checked (unlike wd's epoch-ms DBRA/SCA split) -- no toIso() needed.
// `contacts` is the agency's own published program contact, same PII-safe reasoning already
// applied to opp's `pointOfContact` (statutory public notice, not a person's private profile).
// `financial.obligations` is shipped as raw pass-through, not normalized: the one sample read had
// only a `flag` per year (no numeric `amount`), and cycle 707's time budget did not allow reading
// enough records to enumerate the full flag vocabulary -- honest raw data beats a half-guessed enum.
function normalizeCfdaRow(row) {
    const id = row._id;
    return {
        assistanceListingId: id === null || id === undefined ? null : String(id),
        programNumber: row.programNumber ?? null,
        title: row.title ?? null,
        alternativeNames: Array.isArray(row.alternativeNames) ? row.alternativeNames : null,
        objective: row.objective ?? null,
        isActive: row.isActive ?? null,
        isFunded: row.isFunded ?? null,
        isLatest: row.isLatest ?? null,
        publishDate: row.publishDate ?? null,
        modifiedDate: row.modifiedDate ?? null,
        department: orgFieldByLevel(row.organizationHierarchy, 1),
        agency: orgFieldByLevel(row.organizationHierarchy, 2),
        assistanceTypes: Array.isArray(row.assistanceTypes)
            ? row.assistanceTypes.map((t) => (t?.hierarchy ?? []).map((h) => h?.value ?? null).filter(Boolean))
            : null,
        eligibleApplicants: row.eligibility?.applicant?.types?.map((t) => t?.value ?? null).filter(Boolean) ?? null,
        eligibleApplicantsNote: row.eligibility?.applicant?.additionalInfo ?? null,
        eligibleBeneficiaries: row.eligibility?.beneficiary?.types?.map((t) => t?.value ?? null).filter(Boolean) ?? null,
        eligibleBeneficiariesNote: row.eligibility?.beneficiary?.additionalInfo ?? null,
        obligations: Array.isArray(row.financial?.obligations) ? row.financial.obligations : null,
        contacts: Array.isArray(row.contacts)
            ? row.contacts.map((c) => ({ name: c?.name ?? null, title: c?.title ?? null, phone: c?.phone ?? null, address: c?.address?.streetAddress ?? null }))
            : null,
        relatedPrograms: Array.isArray(row.relatedPrograms) ? row.relatedPrograms.map((p) => p?.programNumber ?? null).filter(Boolean) : null,
        website: row.website ?? null,
        historicalIndexCount: Array.isArray(row.historicalIndex) ? row.historicalIndex.length : null,
        sourceUrl: id ? `https://sam.gov/fal/${id}/view` : null,
    };
}

// One identity accessor for all three row shapes, so the dedupe set, the watch baseline and the
// push loop can never disagree about what "the id of this row" means.
function idOf(item) {
    return item.opportunityId ?? item.wageDeterminationId ?? item.assistanceListingId ?? null;
}

let detailLookupsFailed = 0;

async function enrichOne(item) {
    if (!item.opportunityId) return item;
    const detail = await apiGet(`${DETAIL_API}/${item.opportunityId}`);
    if (!detail?.data2) { detailLookupsFailed += 1; return item; }
    const d = detail.data2;
    item.naicsCodes = Array.isArray(d.naics) ? d.naics.flatMap((n) => n.code ?? []) : null;
    item.setAside = d.solicitation?.setAside ?? d.award?.setAside ?? null;
    item.placeOfPerformanceState = d.placeOfPerformance?.state?.code ?? null;
    item.placeOfPerformanceCountry = d.placeOfPerformance?.country?.code ?? null;
    // Government office contacts, published by the agency itself as part of the statutory
    // public notice (same disclosure class already reviewed for nih-reporter-scraper /
    // eu-ted-tenders-scraper) -- not scraped from a person's private profile, not aggregated
    // across sources, not resold as a people-lookup product. PII-safe to include as-is.
    item.pointOfContact = Array.isArray(d.pointOfContact)
        ? d.pointOfContact.map((c) => ({ name: c.fullName ?? null, email: c.email ?? null, phone: c.phone ?? null, type: c.type ?? null }))
        : null;
    return item;
}

// ---------------------------------------------------------------------------
// Watch mode: "only what is new since my last run", per saved query. Same shape as
// grants-gov-scraper/federal-register-scraper (cycle 297+) -- copy that design, don't reinvent it.
//
// The baseline is the buyer's own -- the opportunity ids this label has already delivered -- kept
// in a NAMED key-value store so it survives across runs (the default per-run KV store would reset
// the baseline every run, i.e. re-charge the whole result set every time). `opportunityId` (SAM's
// `_id`) is the stable identity: it's what the detail endpoint and the public /opp/<id>/view URL
// key off, whereas `solicitationNumber` is an agency-entered label that can in principle repeat.
const WATCH_STORE = 'fetchsmith-samgov-watch';
const SEED_CAP = 10000; // same as SAM.gov's own hard backend depth cap -- a seed walk can never
// need to go deeper than the platform itself allows for one query.
const WATCH_KEEP = 60000; // bound the KV record size; oldest ids fall off first

const watchMode = watchLabel.length > 0;

// Apify KV keys allow [a-zA-Z0-9!-_.'()] only, so the label is sanitised rather than trusted. The
// criteria fingerprint is part of the key on purpose: if the buyer edits a filter, that's a
// different question and gets its own baseline, instead of dumping every opportunity the old
// narrower filter happened to exclude as if it were brand new. `enrichDetail` is deliberately left
// out -- it changes output richness, not which opportunities match, same reasoning as `enrich` on
// grants-gov-scraper's watchCriteria.
function watchKeyFor(label, criteria) {
    const safe = label.toLowerCase().replace(/[^a-z0-9_.-]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 40) || 'default';
    const fp = createHash('sha1').update(JSON.stringify(criteria, Object.keys(criteria).sort())).digest('hex').slice(0, 10);
    return { key: `watch-${safe}-${fp}`, fingerprint: fp };
}

const watchCriteria = {
    // dataType is part of the fingerprint: opportunities and wage determinations are different
    // questions with disjoint id spaces, so they must never share a baseline.
    dataType,
    keyword, naicsCodes: [...naicsCodes].sort(), setAsideTypes: [...setAsideTypes].sort(),
    noticeTypes: [...noticeTypes].sort(), states: [...states].sort(), organizationId, activeOnly,
};

// Snapshot of the fields that can change on an already-delivered opportunity: `isActive`/
// `noticeTypeCode` (the presolicitation -> solicitation -> award lifecycle transition SAM.gov's
// own demand data flags as the single most valuable alert in this niche), `responseDate` (a
// deadline extension -- the highest-frequency real change), `modifiedDate` (SAM's own "this
// notice was edited" stamp), `modificationsCount` and `awardeeName` (null -> set is the award
// landing). `description` is now the FULL solicitation text (cycle 567, can run 10k+ chars) -- the
// fleet rule is never to store free text in a watch snapshot, so only an 8-char md5 fingerprint of
// it is kept, enough to detect an edit without risking the KV record's size budget (WATCH_KEEP
// holds up to 60,000 of these).
function descHashOf(desc) {
    return desc ? createHash('md5').update(desc).digest('hex').slice(0, 8) : null;
}
const WATCHED_FIELDS_TEXT = isCfda
    ? 'active or funded status, modified date, or historical-index entry count'
    : isWd
    ? 'revision number, active status or modified date'
    : 'active/notice-type status, response deadline, modified date, modification count, awardee or description';

function snapshotOf(item) {
    return {
        isActive: item.isActive ?? null,
        noticeTypeCode: item.noticeTypeCode ?? null,
        responseDate: item.responseDate ?? null,
        modifiedDate: item.modifiedDate ?? null,
        modificationsCount: typeof item.modificationsCount === 'number' ? item.modificationsCount : null,
        awardeeName: item.awardeeName ?? null,
        descHash: descHashOf(item.description),
        // Wage determinations have no notice lifecycle or response deadline; what moves on them is
        // a REVISION (Davis-Bacon schedules are revised many times a year) and isActive flipping
        // when a newer revision supersedes them. Always null on an opportunity row.
        revisionNumber: typeof item.revisionNumber === 'number' ? item.revisionNumber : null,
        // Assistance listings have no revision number either; what moves is funded status
        // (isFunded flips as budgets are appropriated) and the historical-index log growing when
        // SAM.gov records a title/agency change (not yet observed live over time as of cycle 707 --
        // treated as a candidate signal, not a confirmed one; harmless if it never fires). Always
        // null on an opp/wd row.
        isFunded: typeof item.isFunded === 'boolean' ? item.isFunded : null,
        historicalIndexCount: typeof item.historicalIndexCount === 'number' ? item.historicalIndexCount : null,
    };
}

// A changed opportunity is re-delivered tagged with exactly what moved, so a buyer doesn't have to
// diff the row against their own last-seen copy to find out. descHash is compared separately since
// its "previous" value (a hash) isn't meaningful to show a buyer.
function changesBetween(prev, next) {
    if (!prev) return null;
    const types = [];
    const previous = {};
    for (const field of ['isActive', 'noticeTypeCode', 'responseDate', 'modifiedDate', 'modificationsCount', 'awardeeName', 'revisionNumber', 'isFunded', 'historicalIndexCount']) {
        if (prev[field] !== undefined && prev[field] !== null && prev[field] !== next[field]) {
            types.push(field);
            previous[field] = prev[field];
        }
    }
    if (prev.descHash !== undefined && prev.descHash !== null && prev.descHash !== next.descHash) {
        types.push('description');
        previous.description = '(changed; only a fingerprint of the description is retained, not the previous text)';
    }
    return types.length ? { types, previous } : null;
}

let watchStore = null;
let watchKey = null;
let watchRecord = null;
let seeding = false;
const watchSeen = new Map(); // opportunityId -> last-seen snapshot
let changedCount = 0;
let skippedSeen = 0;

let baselineTruncated = 0; // ids dropped by WATCH_KEEP -- they come back as "new" and get charged

async function saveWatchRecord(status) {
    const all = Array.from(watchSeen.entries());
    const entries = all.slice(-WATCH_KEEP);
    baselineTruncated = all.length - entries.length;
    if (baselineTruncated > 0) {
        log.warning(
            `The baseline for "${watchLabel}" exceeded the ${WATCH_KEEP}-entry record cap; the ${baselineTruncated} `
            + 'oldest opportunity id(s) were dropped and will be returned and CHARGED as new on a future run. '
            + 'Narrow the watch query (keyword, NAICS, notice type) or split it across labels.',
        );
    }
    await watchStore.setValue(watchKey, {
        ...watchRecord,
        label: watchLabel,
        criteria: watchCriteria,
        lastRunAt: new Date().toISOString(),
        lastRunStatus: status,
        seenCount: entries.length,
        // Compact per-entry shape so WATCH_KEEP's 60,000 entries stay inside the KV record's size
        // budget: i(d), a(isActive), n(noticeTypeCode), r(responseDate), m(modifiedDate),
        // c(modificationsCount), w(awardeeName), h(descHash), v(revisionNumber), f(isFunded),
        // x(historicalIndexCount).
        seenIds: entries.map(([id, snap]) => ({
            i: id, a: snap.isActive, n: snap.noticeTypeCode, r: snap.responseDate, m: snap.modifiedDate,
            c: snap.modificationsCount, w: snap.awardeeName, h: snap.descHash, v: snap.revisionNumber,
            f: snap.isFunded, x: snap.historicalIndexCount,
        })),
        runCount: (watchRecord.runCount ?? 0) + 1,
    });
}

if (watchMode) {
    watchStore = await Actor.openKeyValueStore(WATCH_STORE);
    const { key, fingerprint } = watchKeyFor(watchLabel, watchCriteria);
    watchKey = key;
    const existing = await watchStore.getValue(key);
    if (existing && Array.isArray(existing.seenIds)) {
        watchRecord = existing;
        // Backward-compatible reader: a record from before this feature existed would only ever
        // be a fresh baseline (this is the Actor's first watch-mode build), but kept defensive the
        // same way the fleet's other watch actors are, in case a future field is added later and
        // an older record is missing it -- missing fields just have no snapshot yet.
        for (const entry of existing.seenIds) {
            if (entry && typeof entry === 'object') {
                watchSeen.set(String(entry.i), {
                    isActive: entry.a ?? null, noticeTypeCode: entry.n ?? null, responseDate: entry.r ?? null,
                    modifiedDate: entry.m ?? null,
                    modificationsCount: typeof entry.c === 'number' ? entry.c : null,
                    awardeeName: entry.w ?? null, descHash: entry.h ?? null,
                    revisionNumber: typeof entry.v === 'number' ? entry.v : null,
                    isFunded: typeof entry.f === 'boolean' ? entry.f : null,
                    historicalIndexCount: typeof entry.x === 'number' ? entry.x : null,
                });
            } else {
                watchSeen.set(String(entry), {
                    isActive: null, noticeTypeCode: null, responseDate: null, modifiedDate: null,
                    modificationsCount: null, awardeeName: null, descHash: null, revisionNumber: null,
                    isFunded: null, historicalIndexCount: null,
                });
            }
        }
        log.info(
            `Watch mode "${watchLabel}" (${key}): baseline from ${existing.lastRunAt ?? 'an earlier run'} holds `
            + `${watchSeen.size} already-delivered ${ROW_NOUN}(s). Only ${ROW_NOUN_PLURAL} NOT in that baseline are returned and charged`
            + (watchChanges ? `, plus any already-delivered ${ROW_NOUN} whose ${WATCHED_FIELDS_TEXT} changed.` : '.'),
        );
    } else {
        watchRecord = { fingerprint, firstSeededAt: new Date().toISOString(), runCount: 0 };
        seeding = true;
        log.info(
            `Watch mode "${watchLabel}" (${key}): FIRST run for this label and filter set, so this is a baseline run. `
            + `It records which ${ROW_NOUN_PLURAL} already match and returns ZERO results (you are charged nothing). Run it `
            + 'again on the same label and filters -- on a schedule, typically -- to get only what is new since now.',
        );
    }
}

// This Actor is published PAY_PER_EVENT ($0.0015/row, single "result" event, see meta.json) but
// until this fix it only ever called Actor.pushData(results) in one bulk call at the end -- never
// Actor.charge(). Every other PPE Actor in the fleet routes pushes through a pushResult() that
// calls Actor.charge() first (federal-register-scraper/grants-gov-scraper/etc. all use this exact
// pattern); this one was published (cycle 540) without it, so every real buyer since would have
// gotten every row for free. Found and fixed cycle 542, before any paying run occurred (0 revenue
// booked fleet-wide as of this cycle, so no refund owed). `isPPE` guards local/non-PPE test runs,
// same as the sibling Actors.
let pushed = 0;
let chargeLimitReached = false;
const isPPE = Actor.getChargingManager().getPricingInfo().isPayPerEvent;
async function pushResult(item) {
    if (isPPE) {
        const r = await Actor.charge({ eventName: 'result', count: 1 });
        if (r.chargedCount === 0) { chargeLimitReached = true; return false; }
        await Actor.pushData(item); pushed += 1;
        if (r.eventChargeLimitReached) chargeLimitReached = true;
        return !r.eventChargeLimitReached && pushed < maxResults;
    }
    await Actor.pushData(item); pushed += 1;
    return pushed < maxResults;
}

const PAGE_SIZE = 100;

// Pulled out so the real run and a watch-mode baseline seed walk share the exact same paging
// logic and can never drift out of sync -- only the `limit` differs (maxResults vs. SEED_CAP).
const DEPTH_CAP = 10000; // SAM.gov's own hard backend paging depth, confirmed cycle 538

// How many of the declared matches this backend will actually hand over. null while SAM has not
// answered with a count -- never collapsed to 0, which is what made a failed count read as
// "nothing matched your filters" everywhere it was used.
function reachable() {
    return declaredMatches === null ? null : Math.min(declaredMatches, DEPTH_CAP);
}

async function fetchRows(limit) {
    const rows = [];
    // Measured live cycle 649 on a 19,834-match query: a full 100-page walk read 10,000 rows but
    // only 8,990 DISTINCT opportunity ids -- ~10% of rows repeat across pages, because SAM.gov
    // pages by offset over a live, relevance-sorted index that shifts under the walk. Every repeat
    // used to be pushed AND CHARGED again as a separate result. Dedupe inside the walk.
    const seenIds = new Set();
    let page = 0;
    while (rows.length < limit) {
        const reach = reachable();
        if (reach !== null && rows.length >= reach) break; // delivered everything SAM will serve
        const url = buildSearchUrl(page, PAGE_SIZE);
        const data = await apiGet(url);
        if (!data) {
            pagesFailed += 1;
            markIncomplete('upstream-error', `page ${page} failed after 4 attempts (${lastApiError ?? 'unknown error'})`);
            log.warning(`Page ${page} failed after retries; stopping short.`);
            break;
        }
        pages += 1;
        // A 200 whose body carries no usable total is NOT "0 matches" -- the walk keeps paging blind
        // until SAM returns an empty page, instead of ending on the first page looking complete.
        const declared = Number.isFinite(data.page?.totalElements) ? Number(data.page.totalElements) : null;
        // FIRST answer wins. Measured live cycle 649: walking a 911-match query to exhaustion, the
        // one-past-the-end page comes back 200 with an empty `results` AND `totalElements: 0`, so
        // re-assigning on every page clobbered the real count with 0 on the very last read --
        // RUN_SUMMARY would have published `declaredMatches: 0` for a 911-match query and the
        // duplicate/short-page checks (`rows.length < 0`) could never fire. The declared count is a
        // property of the query, measured once, not a per-page field.
        if (declared !== null && declaredMatches === null) declaredMatches = declared;
        const pageRows = data._embedded?.results ?? [];
        if (pageRows.length === 0) {
            // Empty page before SAM's own declared total is reached = the backend quit early, which
            // is not the same fact as "the result set ended here".
            const reachNow = reachable();
            if (reachNow !== null && rows.length < reachNow) {
                // Distinguish "SAM.gov quit early" from "SAM.gov served its whole set but repeated
                // rows, so there were fewer distinct opportunities than it declared". Both come up
                // short of the declared total; only the first is an upstream failure.
                if (rows.length + duplicateRowsDropped >= reachNow) {
                    markIncomplete('duplicate-rows', `SAM.gov served ${reachNow} row(s) for this query but only ${rows.length} were distinct opportunities (${duplicateRowsDropped} repeat(s) dropped, uncharged)`);
                } else {
                    markIncomplete('short-page', `SAM.gov returned an empty page ${page} after ${rows.length} of ${reachNow} reachable match(es)`);
                }
            }
            break;
        }
        scanned += pageRows.length;
        for (const row of pageRows) {
            const item = isWd ? normalizeWdRow(row) : isCfda ? normalizeCfdaRow(row) : normalizeRow(row);
            const rowId = idOf(item);
            if (rowId) {
                if (seenIds.has(rowId)) { duplicateRowsDropped += 1; continue; }
                seenIds.add(rowId);
            }
            rows.push(item);
            if (rows.length >= limit) break;
        }
        const target = reachable() === null ? limit : Math.min(reachable(), limit);
        log.info(`Page ${page}: +${pageRows.length} rows (total so far ${rows.length}/${target})`);
        page += 1;
        if (page * PAGE_SIZE >= DEPTH_CAP) {
            // Only a shortfall if there was actually more to get and the caller still wanted it.
            if (rows.length < limit && (declaredMatches === null || declaredMatches > DEPTH_CAP)) {
                markIncomplete(
                    'depth-cap',
                    `SAM.gov serves at most ${DEPTH_CAP} rows per query`
                    + `${declaredMatches === null ? '' : `; ${declaredMatches - DEPTH_CAP} of ${declaredMatches} match(es) sit past it`}`,
                );
            }
            log.warning('Hit SAM.gov\'s 10,000-row backend depth cap; narrow keyword/filters for more.');
            break;
        }
        await sleep(300); // stay well under any rate limit; verified spacing from the feasibility check
    }
    return rows;
}

// Seeding only needs ids + the watched fields, both already on the thin search row, so it never
// needs enrichDetail on -- unlike grants-gov-scraper's award-amount filter, nothing this Actor
// watches lives only on the detail record. It walks the WHOLE match set (up to SEED_CAP, the same
// as SAM.gov's own hard depth cap), unbounded by maxResults -- a baseline that stopped early would
// report every opportunity past the stopping point as "new" on the first incremental run.
if (watchMode && seeding) {
    const baselineRows = await fetchRows(SEED_CAP);
    for (const row of baselineRows) {
        if (idOf(row)) watchSeen.set(idOf(row), snapshotOf(row));
    }
    // Backstop, keyed on rows READ not rows kept: if the seed asks for exactly SEED_CAP distinct
    // rows and SAM.gov happens to serve no duplicates, the walk exits on `rows.length >= limit`
    // before fetchRows' own depth-cap branch is reached. A baseline that stopped at the cap is the
    // same over-charge as one that stopped on an error, so it is marked either way. Same
    // `depth-cap` reason on purpose -- one name per fact; `mode: "watch-seed"` says it was a seed.
    if (scanned >= SEED_CAP && (declaredMatches === null || declaredMatches > SEED_CAP)) {
        markIncomplete(
            'depth-cap',
            `the baseline walk stopped at SAM.gov's ${SEED_CAP}-row depth cap`
            + `${declaredMatches === null ? '' : `; ${(declaredMatches - SEED_CAP).toLocaleString('en-US')} of ${declaredMatches.toLocaleString('en-US')} match(es) were never seen`}`,
        );
    }
    log.info(`Baseline walk: ${watchSeen.size} ${ROW_NOUN} id(s) recorded.`);
}

let results = [];
let rowsNotReached = 0; // fetched rows the push loop never got to (charge limit / maxResults)
if (!seeding) {
    results = await fetchRows(maxResults);
    // The walk delivered all it was asked for, but SAM says there is more behind it. That is a
    // legitimate, buyer-chosen shortfall -- it still has to be SAID, because a pipeline cannot tell
    // "200 of 200 matches" from "200 of 12,297" by looking at the dataset.
    const reach = reachable();
    if (results.length >= maxResults && reach !== null && reach > maxResults) {
        markIncomplete('max-results', `maxResults=${maxResults} of ${reach} reachable match(es)`);
    }
    if (enrichDetail) {
        log.info(`Enriching ${results.length} rows with detail-call fields (naics, set-aside, place of performance, contacts)...`);
        for (const item of results) {
            await enrichOne(item);
            await sleep(200);
        }
        // A detail call that failed leaves naicsCodes/setAside/pointOfContact at null -- the same
        // null a genuinely contact-less notice has. The buyer turned enrichment ON and paid for
        // those fields, so a silent miss is a shortfall, not a detail.
        if (detailLookupsFailed) {
            markIncomplete('enrich-failed', `${detailLookupsFailed} of ${results.length} detail lookup(s) failed; their naics/set-aside/place-of-performance/contact fields are null for that reason, not because SAM.gov has none`);
        }
    }

    let beforePush = 0;
    let index = 0;
    for (const item of results) {
        index += 1;
        if (watchMode && idOf(item) && watchSeen.has(idOf(item))) {
            const id = idOf(item);
            const nextSnap = snapshotOf(item);
            // Already delivered under this watch label. Normally dropped before any charge, so an
            // opportunity is never paid for twice -- UNLESS watchChanges is on and one of the
            // watched fields moved since we last saw it, in which case it's re-delivered (charged
            // like a new row) tagged with exactly what changed.
            const change = watchChanges ? changesBetween(watchSeen.get(id), nextSnap) : null;
            if (!change) {
                // Snapshot is kept current either way, so turning watchChanges on later detects
                // only drift from that point, not a backlog since the baseline.
                watchSeen.set(id, nextSnap);
                skippedSeen += 1;
                continue;
            }
            const cont = await pushResult({ ...item, _watchChangeType: change.types, _watchPrevious: change.previous });
            if (pushed > beforePush) { watchSeen.set(id, nextSnap); changedCount += 1; }
            beforePush = pushed;
            if (!cont) { rowsNotReached = results.length - index; break; }
            continue;
        }
        const cont = await pushResult(item);
        // Recorded as delivered only after the charge actually succeeded -- anything dropped by
        // maxResults or a charge limit stays "new" for the next run.
        if (watchMode && idOf(item) && pushed > beforePush) watchSeen.set(idOf(item), snapshotOf(item));
        beforePush = pushed;
        if (!cont) { rowsNotReached = results.length - index; break; } // maxResults reached or a per-run charge limit hit
    }

    // The push loop abandoning rows it had already fetched is invisible in the dataset: the run
    // SUCCEEDS with a plausible-looking row count. Charge limit is reported ahead of maxResults --
    // it is the cause the buyer did not choose.
    if (chargeLimitReached) {
        markIncomplete('charge-limit', `the run's pay-per-event charge limit was reached${rowsNotReached ? `; ${rowsNotReached} already-fetched row(s) were not delivered` : ''}`);
    } else if (rowsNotReached > 0) {
        markIncomplete('max-results', `maxResults=${maxResults} reached; ${rowsNotReached} already-fetched row(s) were not delivered`);
    }
}

// A SEED walk cut short by SAM.gov not answering (`upstream-error`) or quitting early before its
// own declared total, unexplained by duplicates (`short-page`), is not a smaller baseline, it is a
// WRONG one: every opportunity past the failure point would read as "new" (and charged) on the
// first incremental run. `depth-cap` and `duplicate-rows` are deliberately excluded -- both mean
// SAM.gov answered IN FULL (its own hard 10,000-row limit, or repeats within what it did serve),
// so a capped-but-real baseline is still strictly better than none. Seeding never charges, so
// refusing to save costs nothing but a re-run. Before this fix the save was unconditional and only
// the status label read `'seeded-incomplete'` -- cosmetic, since neither load path (line ~751)
// reads `.status` back, so the truncated baseline was consumed exactly like a complete one.
const SEED_UPSTREAM_FAILURES = new Set(['upstream-error', 'short-page']);
const seedFailure = seeding && incompleteReason && SEED_UPSTREAM_FAILURES.has(incompleteReason)
    ? `${incompleteReason}${incompleteDetail ? `: ${incompleteDetail}` : ''}`
    : null;

if (watchMode && seedFailure) {
    log.warning(
        `Baseline walk for watch label "${watchLabel}" was cut short (${seedFailure}), so NO baseline was saved. `
        + 'Re-run with the same watchLabel to seed again once SAM.gov is answering -- saving a truncated baseline '
        + 'would make every opportunity past the failure point look "new" (and billable) on the first incremental run.',
    );
} else if (watchMode) {
    await saveWatchRecord(
        seeding
            ? (complete ? 'seeded' : 'seeded-incomplete')
            : (complete ? 'incremental' : 'incremental-incomplete'),
    );
    if (seeding) {
        // An incomplete-but-saved baseline here means depth-cap/duplicate-rows only -- SAM.gov
        // answered in full, so this is a real (if capped) baseline, not the over-charge risk above.
        if (!complete) {
            log.warning(
                `BASELINE INCOMPLETE (${incompleteReason}${incompleteDetail ? `: ${incompleteDetail}` : ''}). Only `
                + `${watchSeen.size} ${ROW_NOUN}(s) were recorded as already-seen out of `
                + `${declaredMatches === null ? 'an unknown number of' : declaredMatches.toLocaleString('en-US')} match(es). `
                + `Re-run this seed before scheduling incremental runs, or the missing ${ROW_NOUN_PLURAL} will be returned and CHARGED as new.`,
            );
        }
        log.info(
            `Baseline saved for watch label "${watchLabel}": ${watchSeen.size} ${ROW_NOUN}(s) recorded as already-seen, `
            + `0 results returned, 0 charged. The next run on this label and these filters returns only new ${ROW_NOUN_PLURAL}.`
            + (watchSeen.size >= SEED_CAP
                ? ` NOTE: the baseline stopped at the ${SEED_CAP}-record cap. Narrow the query (a keyword`
                + `${isCfda ? ', an organization' : isWd ? ', a state' : ', a NAICS code, a set-aside/notice type'}) so `
                + `the whole result set fits, or the first incremental run will report ${ROW_NOUN_PLURAL} past the cap as new.`
                : ''),
        );
    } else {
        log.info(
            `Watch label "${watchLabel}": ${pushed - changedCount} new ${ROW_NOUN}(s)`
            + (watchChanges ? ` and ${changedCount} changed ${ROW_NOUN}(s) (${WATCHED_FIELDS_TEXT})` : '')
            + ` since the last run (${skippedSeen} already-delivered, unchanged row(s) skipped, uncharged); baseline now holds ${watchSeen.size}.`,
        );
    }
}

log.info(`Done. Pushed ${pushed} ${ROW_NOUN_PLURAL} (scanned ${scanned} row(s) over ${pages} page(s)).`);

// ---------------------------------------------------------------------------
// RUN_SUMMARY: this run's completeness, in a form a pipeline can read. Fetch with
//   GET /v2/actor-runs/<runId>/key-value-store/records/RUN_SUMMARY
// which needs no webhook. `complete` is deliberately kept OUT of the status string: a run can be
// SUCCEEDED and short at the same time, and that pair is exactly what this record exists for.
const runSummary = {
    dataType,
    searchIndex: SEARCH_INDEX,
    mode: watchMode ? (seeding ? 'watch-seed' : 'watch-incremental') : 'search',
    // What SAM.gov itself says matches this query (page.totalElements). `null` means the search
    // never answered with a count -- never read it as 0.
    declaredMatches,
    // Of those, how many this backend will actually serve, given its 10,000-row depth cap.
    reachableMatches: reachable(),
    unreachableMatches: declaredMatches === null ? null : Math.max(declaredMatches - DEPTH_CAP, 0),
    depthCap: DEPTH_CAP,
    scanned,
    delivered: pushed,
    rowsNotReached,
    pages,
    pagesFailed,
    // Distinct is what you are charged for: `scanned` counts raw rows off the wire,
    // `scanned - duplicateRowsDropped` is how many distinct opportunities that actually was.
    duplicateRowsDropped,
    complete,
    incompleteReason,
    incompleteDetail,
    lastApiError,
    maxResults,
    chargeLimitReached,
    detailLookupsFailed: enrichDetail ? detailLookupsFailed : null,
    watchLabel: watchMode ? watchLabel : null,
    watchSeeding: watchMode ? seeding : null,
    baselineSize: watchMode ? watchSeen.size : null,
    baselineTruncated: watchMode ? baselineTruncated : null,
    changedRedelivered: watchMode && !seeding ? changedCount : null,
    skippedSeen: watchMode && !seeding ? skippedSeen : null,
};
await Actor.setValue('RUN_SUMMARY', runSummary);

// A short run still SUCCEEDS (the rows it did get are real and already charged), so the status
// message is the only place the Apify console itself shows the shortfall. There was no
// setStatusMessage call anywhere in this Actor before cycle 649.
if (!complete) {
    const of = reachable() === null ? '' : ` of ${reachable().toLocaleString('en-US')} reachable`;
    await Actor.setStatusMessage(
        seeding
            ? `Baseline INCOMPLETE: ${watchSeen.size.toLocaleString('en-US')} ${ROW_NOUN}(s) recorded${of} — ${incompleteReason}`
              + `${incompleteDetail ? ` (${incompleteDetail})` : ''}. Re-seed before scheduling, or the rest will be charged as new. See RUN_SUMMARY.`
            : `Incomplete: ${pushed.toLocaleString('en-US')} row(s)${of} — ${incompleteReason}`
              + `${incompleteDetail ? ` (${incompleteDetail})` : ''}. See RUN_SUMMARY for details.`,
    );
} else if (declaredMatches !== null && !watchMode) {
    log.info(`Complete: delivered every one of the ${declaredMatches.toLocaleString('en-US')} ${ROW_NOUN}(s) SAM.gov declared for these filters.`);
}

// Fires after every row is already pushed and charged, so a slow or failing webhook can never
// affect the result set or the bill -- best-effort only, one attempt, short timeout, failures are
// a warning not a thrown error. `watchNewCount` is `pushed - changedCount` because this Actor
// pushes new AND changed rows through the same counter (cycle 441 lesson).
if (webhookUrl) {
    const env = Actor.getEnv();
    const payload = {
        actorRunId: env.actorRunId ?? null,
        defaultDatasetId: env.defaultDatasetId ?? null,
        finishedAt: new Date().toISOString(),
        pushed,
        rowsScanned: scanned, // raw rows read from SAM.gov, seed walk included -- `results.length`
        // was 0 on every baseline run no matter how many thousands it walked.
        watchLabel: watchMode ? watchLabel : null,
        watchSeeding: watchMode ? seeding : null,
        watchNewCount: watchMode && !seeding ? pushed - changedCount : null,
        watchChangedCount: watchMode && !seeding && watchChanges ? changedCount : null,
        watchSkippedCount: watchMode && !seeding ? skippedSeen : null,
        // Same object as the RUN_SUMMARY key-value record, so a webhook consumer and a
        // console/API consumer read the identical completeness facts.
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

if (watchMode && seedFailure) {
    await Actor.fail(
        `The watch baseline could not be completed: ${seedFailure.replace(/[.\s]*$/, '')}. No baseline was saved `
        + `for watch label "${watchLabel}" -- re-run with the same watchLabel to seed again.`,
    );
}

await Actor.exit();
