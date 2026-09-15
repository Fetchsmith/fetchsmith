import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';
import { createHash } from 'node:crypto';

await Actor.init();
const input = (await Actor.getInput()) ?? {};

// ClinicalTrials.gov's own official API v2 (NIH/NLM). No API key, no auth, no proxy.
const API = 'https://clinicaltrials.gov/api/v2/studies';

// Verified live (cycle 120): pageSize=1000 works, pageSize=1001 returns HTTP 200 with only
// 1000 rows — a SILENT cap, not a 400 like the Federal Register / openFDA APIs. Never pass a
// caller-supplied pageSize straight through; always clamp to this.
const MAX_PAGE_SIZE = 1000;

const STATUSES = new Set([
    'RECRUITING', 'NOT_YET_RECRUITING', 'ENROLLING_BY_INVITATION', 'ACTIVE_NOT_RECRUITING',
    'COMPLETED', 'TERMINATED', 'WITHDRAWN', 'SUSPENDED', 'UNKNOWN', 'WITHHELD', 'AVAILABLE',
    'NO_LONGER_AVAILABLE', 'APPROVED_FOR_MARKETING', 'TEMPORARILY_NOT_AVAILABLE',
]);
const STUDY_TYPES = new Set(['INTERVENTIONAL', 'OBSERVATIONAL', 'EXPANDED_ACCESS']);
const PHASES = new Set(['EARLY_PHASE1', 'PHASE1', 'PHASE2', 'PHASE3', 'PHASE4', 'NA']);

const cleanList = (v, allowed) => (Array.isArray(v) ? v : [])
    .map((x) => String(x).toUpperCase().trim())
    .filter((x) => !allowed || allowed.has(x));

const NCT_RE = /^NCT\d{8}$/;
const nctIdsRaw = String(input.nctIds ?? '').split(/[\s,]+/).map((s) => s.trim().toUpperCase()).filter(Boolean);
const nctIds = [...new Set(nctIdsRaw.filter((id) => NCT_RE.test(id)))];
const nctIdsBadFormat = nctIdsRaw.filter((id) => !NCT_RE.test(id));
if (nctIdsBadFormat.length) {
    log.warning(`Dropped ${nctIdsBadFormat.length} nctIds with bad format (expected NCT + 8 digits): ${nctIdsBadFormat.join(', ')}`);
}

const conditions = String(input.conditions ?? '').trim();
const interventions = String(input.interventions ?? '').trim();
const sponsors = String(input.sponsors ?? '').trim();
const locations = String(input.locations ?? '').trim();
const searchQuery = String(input.searchQuery ?? '').trim();
const overallStatus = cleanList(input.overallStatus, STATUSES);
const studyTypes = cleanList(input.studyTypes, STUDY_TYPES);
const phases = cleanList(input.phases, PHASES);
const hasResultsOnly = input.hasResultsOnly === true;
// `resultsAvailability` supersedes the older boolean `hasResultsOnly`; the boolean is kept as a
// legacy fallback so saved inputs / scheduled runs from before this field existed keep working.
const RESULTS_AVAILABILITY = new Set(['with', 'without']);
const resultsAvailability = RESULTS_AVAILABILITY.has(String(input.resultsAvailability ?? '').trim())
    ? String(input.resultsAvailability).trim()
    : (hasResultsOnly ? 'with' : '');
const sex = ['FEMALE', 'MALE'].includes(String(input.sex ?? '').toUpperCase()) ? String(input.sex).toUpperCase() : '';
const acceptsHealthyVolunteers = input.acceptsHealthyVolunteers === true;
const DATE_RE = /^\d{4}-\d{2}-\d{2}$/;
// Every date filter is the same shape: two ISO dates that become one AREA[<field>]RANGE[from,to]
// clause (MIN/MAX for an open bound). `area` is the ClinicalTrials.gov advanced-filter area name;
// all six were verified live against the real API before being wired up — a wrong area name is a
// hard 400 ("Unknown area name"), never a silently-ignored filter, so a typo here cannot ship as
// "filter had no effect".
const DATE_FILTERS = [
    { from: 'lastUpdatePostedDateFrom', to: 'lastUpdatePostedDateTo', area: 'LastUpdatePostDate' },
    { from: 'studyStartDateFrom', to: 'studyStartDateTo', area: 'StartDate' },
    { from: 'primaryCompletionDateFrom', to: 'primaryCompletionDateTo', area: 'PrimaryCompletionDate' },
    { from: 'studyCompletionDateFrom', to: 'studyCompletionDateTo', area: 'CompletionDate' },
    { from: 'firstPostedDateFrom', to: 'firstPostedDateTo', area: 'StudyFirstPostDate' },
    { from: 'resultsFirstPostedDateFrom', to: 'resultsFirstPostedDateTo', area: 'ResultsFirstPostDate' },
];
const dateRanges = [];
const dateCriteria = {};
for (const { from, to, area } of DATE_FILTERS) {
    const f = DATE_RE.test(input[from]) ? input[from] : '';
    const t = DATE_RE.test(input[to]) ? input[to] : '';
    if (f && t && f > t) {
        throw new Error(`"${from}" (${f}) is after "${to}" (${t}) — the window is empty. Swap them.`);
    }
    if (f || t) dateRanges.push(`AREA[${area}]RANGE[${f || 'MIN'},${t || 'MAX'}]`);
    dateCriteria[from] = f || null;
    dateCriteria[to] = t || null;
}
// Kept as named bindings because the run-summary log line below reports them explicitly.
const lastUpdatePostedDateFrom = DATE_RE.test(input.lastUpdatePostedDateFrom) ? input.lastUpdatePostedDateFrom : '';
const lastUpdatePostedDateTo = DATE_RE.test(input.lastUpdatePostedDateTo) ? input.lastUpdatePostedDateTo : '';
const FUNDER_TYPES = new Set(['NIH', 'FED', 'OTHER_GOV', 'INDUSTRY', 'NETWORK', 'INDIV', 'OTHER', 'UNKNOWN', 'AMBIG']);
const funderTypes = cleanList(input.funderTypes, FUNDER_TYPES);
// Verified live: AREA[MinimumAge]/AREA[MaximumAge] RANGE take "<n> Years" (or MIN/MAX for an
// open bound) — same RANGE syntax as the date fields above, just a different unit string.
const ageRangeFromYears = Number.isInteger(input.ageRangeFromYears) && input.ageRangeFromYears >= 0 ? input.ageRangeFromYears : null;
const ageRangeToYears = Number.isInteger(input.ageRangeToYears) && input.ageRangeToYears >= 0 ? input.ageRangeToYears : null;
if (ageRangeFromYears !== null && ageRangeToYears !== null && ageRangeFromYears > ageRangeToYears) {
    // Verified live: a study's own MaximumAge must be >= its own MinimumAge, so requiring
    // MinimumAge >= ageRangeFromYears AND MaximumAge <= ageRangeToYears with from > to is a
    // contradiction no study can ever satisfy — confirmed empty on a real API call, not just reasoned.
    throw new Error(
        `"ageRangeFromYears" (${ageRangeFromYears}) is greater than "ageRangeToYears" (${ageRangeToYears}) — no study's eligibility range can ever satisfy both. Swap them.`,
    );
}
// Verified live: AREA[StdAge](CHILD OR OLDER_ADULT) returns exactly the same totalCount as the
// UI's `aggFilters=ages:child older` (119,295 on query.cond=cancer) — same filter, and the AREA
// form composes with AND inside the existing filter.advanced string, so no extra param needed.
const AGE_GROUPS = new Set(['CHILD', 'ADULT', 'OLDER_ADULT']);
const ageGroups = cleanList(input.ageGroups, AGE_GROUPS);
// Study-document filter. Values are the UI's lowercase codes, OR-ed by SPACE inside one
// aggFilters pair (`docs:sap prot`); a comma there is a 400, and an unknown code is NOT an
// error — it silently returns 0 rows — so this list must stay a strict whitelist.
const DOCUMENT_TYPES = new Set(['prot', 'sap', 'icf']);
const documentTypes = (Array.isArray(input.documentTypes) ? input.documentTypes : [])
    .map((x) => String(x).toLowerCase().trim())
    .filter((x) => DOCUMENT_TYPES.has(x));
// Only `violation:y` is a real value (`violation:n` silently returns 0), so this is a boolean.
const fdaRegulationViolation = input.fdaRegulationViolation === true;
const titleOrAcronym = String(input.titleOrAcronym ?? '').trim();
const outcomeMeasure = String(input.outcomeMeasure ?? '').trim();
// An AREA(...) term is parsed as a query expression, so a multi-word value has to be quoted to
// stay one phrase (verified live: AREA[LocationFacility](Mayo Clinic) = 3,717 hits on cond=cancer
// vs AREA[LocationFacility]("Mayo Clinic") = 3,708 — the unquoted form is two loose terms, not the
// facility name). Double quotes and backslashes inside the value are dropped rather than escaped:
// neither is ever part of a real facility or sponsor name, and leaving them in can unbalance the
// quoting and turn a narrow search into a 400 or a wrong-filter result.
const areaPhrase = (s) => `"${s.replace(/["\\]/g, ' ').replace(/\s+/g, ' ').trim()}"`;
const facilityName = String(input.facilityName ?? '').trim();
const leadSponsorName = String(input.leadSponsorName ?? '').trim();
const SORT_VALUES = new Set(['LastUpdatePostDate:desc', 'StudyFirstPostDate:desc', 'EnrollmentCount:desc']);
const sortBy = SORT_VALUES.has(input.sortBy) ? input.sortBy : '';
const rowsPerStudy = input.rowsPerStudy === 'site' ? 'site' : 'study';
const maxResults = Math.min(Math.max(Number(input.maxResults ?? 100), 1), 50000);
const watchLabel = String(input.watchLabel ?? '').trim();
const watchMode = watchLabel.length > 0 && nctIds.length === 0;
if (input.watchLabel && nctIds.length) {
    log.warning(
        'watchLabel is ignored when nctIds is set -- direct-lookup mode always returns exactly the ids you '
        + 'asked for, so there is no "new since last run" concept to track for it.',
    );
}

// ---------------------------------------------------------------------------
// Watch mode: "only what is new since my last run", per saved query. Same shape as
// fda-recall-scraper (cycle 299) / grants-gov-scraper (cycle 298) / federal-register-scraper
// (cycle 297) / nih-reporter-scraper (cycle 296) -- copy that design, don't reinvent it.
//
// The baseline is the buyer's own -- the nctIds this label has already delivered -- kept in a
// NAMED key-value store on the buyer's own account (the default KV store is per-run and would
// reset the baseline every run, i.e. re-charge the whole result set on every scheduled run).
const WATCH_STORE = 'fetchsmith-clinicaltrials-watch';
const SEED_CAP = 20000; // our own bound on a seed walk's runtime, not a server limit
const WATCH_KEEP = 60000; // bound the record size; oldest ids fall off first

// None of the six date-range pairs above resolve a rolling/relative default (verified against
// `.actor/input_schema.json`: no `default` on any of them, unlike federal-register-scraper's
// last-90-days or fda-recall-scraper's last-365-days) -- `dateCriteria` already holds the buyer's
// own explicit input (or null), never a computed value, so fingerprinting it directly is safe.
const watchCriteria = {
    conditions, interventions, sponsors, locations, searchQuery, titleOrAcronym, outcomeMeasure,
    overallStatus: [...overallStatus].sort(),
    studyTypes: [...studyTypes].sort(),
    phases: [...phases].sort(),
    resultsAvailability,
    documentTypes: [...documentTypes].sort(),
    fdaRegulationViolation,
    sex,
    acceptsHealthyVolunteers,
    funderTypes: [...funderTypes].sort(),
    ageGroups: [...ageGroups].sort(),
    ageRangeFromYears,
    ageRangeToYears,
    facilityName,
    leadSponsorName,
    ...dateCriteria,
};

function watchKeyFor(label, criteria) {
    const safe = label.toLowerCase().replace(/[^a-z0-9_.-]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 40) || 'default';
    const fp = createHash('sha1').update(JSON.stringify(criteria, Object.keys(criteria).sort())).digest('hex').slice(0, 10);
    return { key: `watch-${safe}-${fp}`, fingerprint: fp };
}

let watchStore = null;
let watchKey = null;
let watchRecord = null;
let seeding = false;
const watchSeen = new Set(); // nctIds already delivered under this label

async function saveWatchRecord(status_) {
    const ids = Array.from(watchSeen).slice(-WATCH_KEEP);
    await watchStore.setValue(watchKey, {
        ...watchRecord,
        label: watchLabel,
        criteria: watchCriteria,
        lastRunAt: new Date().toISOString(),
        lastRunStatus: status_,
        runCount: (watchRecord.runCount ?? 0) + 1,
        seenCount: ids.length,
        seenIds: ids,
    });
}

if (watchMode) {
    watchStore = await Actor.openKeyValueStore(WATCH_STORE);
    const { key, fingerprint } = watchKeyFor(watchLabel, watchCriteria);
    watchKey = key;
    const existing = await watchStore.getValue(key);
    if (existing && Array.isArray(existing.seenIds)) {
        watchRecord = existing;
        for (const id of existing.seenIds) watchSeen.add(String(id));
        log.info(
            `Watch mode "${watchLabel}" (${key}): baseline from ${existing.lastRunAt ?? 'an earlier run'} holds `
            + `${watchSeen.size} already-delivered stud(y/ies). Only studies NOT in that baseline are returned and charged.`,
        );
    } else {
        watchRecord = { fingerprint, firstSeededAt: new Date().toISOString(), runCount: 0 };
        seeding = true;
        log.info(
            `Watch mode "${watchLabel}" (${key}): FIRST run for this label and filter set, so this is a baseline run. `
            + 'It records which studies already match and returns ZERO results (you are charged nothing). Run it '
            + 'again on the same label and filters -- on a schedule, typically -- to get only what is new since now.',
        );
    }
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function apiGet(params, { quiet = false } = {}) {
    const qs = new URLSearchParams();
    for (const [k, v] of Object.entries(params)) {
        if (Array.isArray(v)) { if (v.length) qs.set(k, v.join(',')); }
        else if (v != null && v !== '') qs.set(k, String(v));
    }
    const url = `${API}?${qs.toString()}`;
    for (let attempt = 1; attempt <= 4; attempt += 1) {
        const resp = await gotScraping({
            url,
            responseType: 'text',
            throwHttpErrors: false,
            retry: { limit: 0 },
            timeout: { request: 60000 },
            headers: { accept: 'application/json' },
        });
        if (resp.statusCode === 429 || resp.statusCode >= 500) {
            const waitS = Number(resp.headers['retry-after']) || attempt * 10;
            log.warning(`ClinicalTrials.gov API returned ${resp.statusCode}; retrying in ${waitS}s (${attempt}/4).`);
            await sleep(waitS * 1000);
            continue;
        }
        let parsed = null;
        try { parsed = JSON.parse(resp.body); } catch { /* handled below */ }
        if (resp.statusCode !== 200) {
            if (!quiet) {
                const detail = parsed?.errors ? JSON.stringify(parsed.errors) : String(resp.body).slice(0, 300);
                log.warning(`ClinicalTrials.gov API ${resp.statusCode}: ${detail}`);
            }
            return null;
        }
        if (!parsed) {
            if (!quiet) log.warning(`ClinicalTrials.gov returned a non-JSON body: ${String(resp.body).slice(0, 200)}`);
            return null;
        }
        return parsed;
    }
    if (!quiet) log.warning('ClinicalTrials.gov API kept erroring after 4 attempts; stopping early.');
    return null;
}

function baseParams() {
    const p = { pageSize: MAX_PAGE_SIZE };
    if (conditions) p['query.cond'] = conditions;
    if (interventions) p['query.intr'] = interventions;
    if (sponsors) p['query.spons'] = sponsors;
    if (locations) p['query.locn'] = locations;
    if (searchQuery) p['query.term'] = searchQuery;
    if (titleOrAcronym) p['query.titles'] = titleOrAcronym;
    if (outcomeMeasure) p['query.outc'] = outcomeMeasure;
    if (overallStatus.length) p['filter.overallStatus'] = overallStatus;
    // Verified live: `filter.hasResults` is rejected as unknown; `aggFilters=results:with` is
    // the real parameter name for this. Multiple aggFilters pairs are COMMA-separated and AND-ed
    // (`docs:sap,results:with` verified live: 9,559 vs 10,597 / 18,341 for each alone).
    const agg = [];
    if (resultsAvailability) agg.push(`results:${resultsAvailability}`);
    if (documentTypes.length) agg.push(`docs:${documentTypes.join(' ')}`);
    if (fdaRegulationViolation) agg.push('violation:y');
    if (agg.length) p.aggFilters = agg.join(',');
    // studyType/phase/sex/healthyVolunteers/date-range are AREA-scoped fields, not top-level
    // filters — combine into filter.advanced. Verified live (this cycle): AREA[Sex](FEMALE),
    // AREA[HealthyVolunteers](true) and AREA[<field>]RANGE[from,to] (MIN/MAX for an open bound)
    // all work against the real API.
    const advanced = [];
    if (studyTypes.length) advanced.push(`AREA[StudyType](${studyTypes.join(' OR ')})`);
    if (phases.length) advanced.push(`AREA[Phase](${phases.join(' OR ')})`);
    if (sex) advanced.push(`AREA[Sex](${sex})`);
    if (acceptsHealthyVolunteers) advanced.push('AREA[HealthyVolunteers](true)');
    advanced.push(...dateRanges);
    if (facilityName) advanced.push(`AREA[LocationFacility](${areaPhrase(facilityName)})`);
    if (leadSponsorName) advanced.push(`AREA[LeadSponsorName](${areaPhrase(leadSponsorName)})`);
    if (ageRangeFromYears !== null) advanced.push(`AREA[MinimumAge]RANGE[${ageRangeFromYears} Years,MAX]`);
    if (ageRangeToYears !== null) advanced.push(`AREA[MaximumAge]RANGE[MIN,${ageRangeToYears} Years]`);
    if (funderTypes.length) advanced.push(`AREA[LeadSponsorClass](${funderTypes.join(' OR ')})`);
    if (ageGroups.length) advanced.push(`AREA[StdAge](${ageGroups.join(' OR ')})`);
    if (advanced.length) p['filter.advanced'] = advanced.join(' AND ');
    if (sortBy) p.sort = sortBy;
    return p;
}

// Verified live: `filter.ids=NCT1,NCT2,...` works, but if ANY id in the batch is malformed or
// doesn't exist, ClinicalTrials.gov 400s the WHOLE request (not a partial/ignore-bad-ones
// response) — a single typo silently makes an otherwise-correct batch return zero rows unless
// handled explicitly. Bisect on failure so one bad id can't take out an entire good batch.
// nctIds deliberately does NOT combine with the search filters below (conditions/interventions/
// sponsors/locations/searchQuery/overallStatus/studyTypes/phases/hasResultsOnly): `conditions`
// carries a schema `default` of "cancer" that Apify applies server-side to any input missing the
// field (verified cycle 96/121), so an API caller who sends only `nctIds` would otherwise get an
// invisible `AND query.cond=cancer` and silently lose every non-cancer trial they asked for.
async function resolveIdsChunk(ids) {
    const params = { 'filter.ids': ids, pageSize: Math.min(MAX_PAGE_SIZE, Math.max(ids.length, 1)) };
    const page = await apiGet(params, { quiet: ids.length > 1 });
    if (page) return { studies: listOf(page.studies), notFound: [] };
    if (ids.length === 1) return { studies: [], notFound: ids };
    const mid = Math.ceil(ids.length / 2);
    const [a, b] = await Promise.all([resolveIdsChunk(ids.slice(0, mid)), resolveIdsChunk(ids.slice(mid))]);
    return { studies: [...a.studies, ...b.studies], notFound: [...a.notFound, ...b.notFound] };
}

const listOf = (v) => (Array.isArray(v) ? v.filter(Boolean) : []);

// Every field/location contact carries a real person's name, phone and/or personal email
// (verified live, incl. an @gmail.com in the sample) — CLAUDE.md rule 1 bans shipping PII, so
// contacts[] is deliberately never read. Location rows keep only facility/geo/status data.
function normalizeStudy(study) {
    const p = study.protocolSection ?? {};
    const id = p.identificationModule ?? {};
    const status = p.statusModule ?? {};
    const sponsor = p.sponsorCollaboratorsModule ?? {};
    const design = p.designModule ?? {};
    const desc = p.descriptionModule ?? {};
    const cond = p.conditionsModule ?? {};
    const arms = p.armsInterventionsModule ?? {};
    const elig = p.eligibilityModule ?? {};
    const locs = listOf(p.contactsLocationsModule?.locations);

    const facilities = locs.map((l) => ({
        facility: l.facility ?? null,
        status: l.status ?? null,
        city: l.city ?? null,
        state: l.state ?? null,
        country: l.country ?? null,
        lat: l.geoPoint?.lat ?? null,
        lon: l.geoPoint?.lon ?? null,
    }));

    return {
        nctId: id.nctId ?? null,
        briefTitle: id.briefTitle ?? null,
        officialTitle: id.officialTitle ?? null,
        acronym: id.acronym ?? null,
        overallStatus: status.overallStatus ?? null,
        studyType: design.studyType ?? null,
        // Populated on ~81% of studies (measured live sample of 50) — absent for many
        // observational studies. Never advertised as guaranteed.
        phases: listOf(design.phases),
        enrollmentCount: design.enrollmentInfo?.count ?? null,
        startDate: status.startDateStruct?.date ?? null,
        primaryCompletionDate: status.primaryCompletionDateStruct?.date ?? null,
        completionDate: status.completionDateStruct?.date ?? null,
        studyFirstPostDate: status.studyFirstPostDateStruct?.date ?? null,
        lastUpdatePostDate: status.lastUpdatePostDateStruct?.date ?? null,
        leadSponsor: sponsor.leadSponsor?.name ?? null,
        leadSponsorClass: sponsor.leadSponsor?.class ?? null,
        // Populated on ~24% of studies (measured live sample of 50) — most trials have none.
        collaborators: listOf(sponsor.collaborators).map((c) => c.name).filter(Boolean),
        conditions: listOf(cond.conditions),
        keywords: listOf(cond.keywords),
        interventions: listOf(arms.interventions).map((i) => ({ type: i.type ?? null, name: i.name ?? null })),
        briefSummary: desc.briefSummary ?? null,
        sex: elig.sex ?? null,
        minimumAge: elig.minimumAge ?? null,
        // Populated on ~48% of studies (measured live sample of 50) — many trials have no
        // upper age bound.
        maximumAge: elig.maximumAge ?? null,
        healthyVolunteers: typeof elig.healthyVolunteers === 'boolean' ? elig.healthyVolunteers : null,
        hasResults: study.hasResults === true,
        locationCount: facilities.length,
        // Site facility/city/state/country/geo only — no contact person, phone or email, ever.
        locations: facilities,
        studyUrl: id.nctId ? `https://clinicaltrials.gov/study/${id.nctId}` : null,
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

log.info(nctIds.length
    ? `ClinicalTrials.gov: direct-lookup mode, nctIds=[${nctIds.join(',')}] (other search filters ignored) `
      + `rowsPerStudy=${rowsPerStudy} maxResults=${maxResults}`
    : `ClinicalTrials.gov: conditions="${conditions}" interventions="${interventions}" sponsors="${sponsors}" `
      + `locations="${locations}" searchQuery="${searchQuery}" overallStatus=[${overallStatus.join(',')}] `
      + `studyTypes=[${studyTypes.join(',')}] phases=[${phases.join(',')}] hasResultsOnly=${hasResultsOnly} `
      + `sex="${sex}" acceptsHealthyVolunteers=${acceptsHealthyVolunteers} `
      + `lastUpdatePostedDateFrom="${lastUpdatePostedDateFrom}" lastUpdatePostedDateTo="${lastUpdatePostedDateTo}" `
      + `ageRangeFromYears=${ageRangeFromYears} ageRangeToYears=${ageRangeToYears} funderTypes=[${funderTypes.join(',')}] `
      + `titleOrAcronym="${titleOrAcronym}" outcomeMeasure="${outcomeMeasure}" sortBy="${sortBy}" `
      + `facilityName="${facilityName}" leadSponsorName="${leadSponsorName}" `
      + `dateRanges=[${dateRanges.join(' AND ')}] `
      + `rowsPerStudy=${rowsPerStudy} maxResults=${maxResults}`
      + (watchMode ? ` watchLabel="${watchLabel}"` : ''));

let scanned = 0;
let pages = 0;
let keepGoing = true;
let skippedSeen = 0;

// Seeding only needs ids, so it walks the search with the exact same `baseParams()`/`apiGet()`
// pagination the real run below uses -- they can never page the underlying API differently.
// `baseParams()` always requests `pageSize: MAX_PAGE_SIZE` (1000) regardless of `maxResults`, so
// (unlike federal-register-scraper cycle 297 / fda-recall-scraper cycle 299) there is no separate
// small-page-size trap to work around here; the only thing this function does differently from
// the real run is not stop early at `maxResults` -- a baseline that stopped early would report
// every study past the stopping point as "new" on the first incremental run.
async function seedBaseline() {
    let pageToken = null;
    for (;;) {
        const params = baseParams();
        if (pageToken) params.pageToken = pageToken;
        const page = await apiGet(params);
        if (!page) break;
        const studies = listOf(page.studies);
        if (!studies.length) break;
        pages += 1;
        for (const study of studies) {
            scanned += 1;
            const nctId = study.protocolSection?.identificationModule?.nctId ?? null;
            if (nctId) watchSeen.add(nctId);
            if (watchSeen.size >= SEED_CAP) {
                log.warning(
                    `Watch label "${watchLabel}" seed hit the ${SEED_CAP}-study cap before scanning the whole `
                    + 'match set. Narrow the query (fewer conditions/locations, a shorter date window) so the '
                    + 'whole result set fits, or the first incremental run will report studies past the cap as new.',
                );
                log.info(`Baseline walk: ${watchSeen.size} stud(y/ies) recorded.`);
                return;
            }
        }
        pageToken = page.nextPageToken ?? null;
        if (!pageToken) break;
    }
    log.info(`Baseline walk: ${watchSeen.size} stud(y/ies) recorded.`);
}

async function emitStudy(study) {
    scanned += 1;
    const row = normalizeStudy(study);
    if (rowsPerStudy === 'site') {
        const sites = row.locations.length ? row.locations : [null];
        for (const site of sites) {
            const { locations: _drop, locationCount: _drop2, ...studyFields } = row;
            keepGoing = await pushResult({ ...studyFields, site });
            if (!keepGoing) return;
        }
    } else {
        keepGoing = await pushResult(row);
    }
}

if (nctIds.length) {
    // Direct-lookup mode: fetch specific trials by NCT id (what most competitor Actors call
    // "search by direct URL"). Exclusive of the search filters below — see the note on
    // resolveIdsChunk for why they are not ANDed in here.
    const CHUNK = 500; // keeps each top-level request well under MAX_PAGE_SIZE / URL-length limits
    const notFound = [];
    for (let i = 0; i < nctIds.length && keepGoing; i += CHUNK) {
        const { studies, notFound: nf } = await resolveIdsChunk(nctIds.slice(i, i + CHUNK));
        notFound.push(...nf);
        pages += 1;
        for (const study of studies) {
            await emitStudy(study);
            if (!keepGoing) break;
        }
    }
    if (notFound.length) {
        log.warning(`${notFound.length} of ${nctIds.length} nctIds were not found on ClinicalTrials.gov: ${notFound.join(', ')}`);
    }
} else if (watchMode && seeding) {
    await seedBaseline();
} else {
    let pageToken = null;
    while (keepGoing) {
        const params = baseParams();
        if (pageToken) params.pageToken = pageToken;
        const page = await apiGet(params);
        if (!page) break;
        const studies = listOf(page.studies);
        if (!studies.length) break;
        pages += 1;

        for (const study of studies) {
            const nctId = study.protocolSection?.identificationModule?.nctId ?? null;
            // Already delivered under this watch label: dropped before any charge, so a study
            // is never paid for twice.
            if (watchMode && nctId && watchSeen.has(nctId)) {
                scanned += 1;
                skippedSeen += 1;
                continue;
            }
            const before = pushed;
            await emitStudy(study);
            // Recorded as delivered only after the charge actually succeeded -- anything dropped
            // by maxResults or a charge limit stays "new" for the next run.
            if (watchMode && nctId && pushed > before) watchSeen.add(nctId);
            if (!keepGoing) break;
        }

        pageToken = page.nextPageToken ?? null;
        if (!pageToken) break;
    }
}

if (watchMode) {
    await saveWatchRecord(seeding ? 'seeded' : 'incremental');
    if (seeding) {
        log.info(
            `Baseline saved for watch label "${watchLabel}": ${watchSeen.size} stud(y/ies) recorded as `
            + 'already-seen, 0 results returned, 0 charged. The next run on this label and these filters '
            + 'returns only new studies.',
        );
    } else {
        log.info(
            `Watch label "${watchLabel}": ${pushed} new stud(y/ies) since the last run (${skippedSeen} `
            + `already-delivered stud(y/ies) skipped, uncharged); baseline now holds ${watchSeen.size}.`,
        );
    }
}

if (pushed === 0 && watchMode && !seeding) {
    log.warning(
        `Nothing new for watch label "${watchLabel}" since its last run -- all ${skippedSeen} matching `
        + 'stud(y/ies) had already been delivered under this label. That is the expected result most of the '
        + 'time; you were charged for nothing.',
    );
} else if (pushed === 0 && !seeding) {
    log.warning(
        nctIds.length
            ? 'No studies matched. Every requested nctId was either malformed or not found on ClinicalTrials.gov — check the id list above.'
            : `No studies matched. Scanned ${scanned} rows. Most common causes, in order: `
              + '(1) conditions/interventions/sponsors/locations/searchQuery are ANDed — combining several '
              + 'narrow filters often genuinely matches nothing; drop one and retry. '
              + '(2) phases only applies to interventional studies with a phase assigned; pairing it with '
              + 'studyTypes=["OBSERVATIONAL"] always returns nothing. '
              + '(3) hasResultsOnly is true on a small minority of studies — combine with a broad condition first.',
    );
}

log.info(`Done. Pushed ${pushed} rows over ${pages} page(s) (scanned ${scanned} studies, mode=${rowsPerStudy}).`);
await Actor.exit();
