import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';

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

const conditions = String(input.conditions ?? '').trim();
const interventions = String(input.interventions ?? '').trim();
const sponsors = String(input.sponsors ?? '').trim();
const locations = String(input.locations ?? '').trim();
const searchQuery = String(input.searchQuery ?? '').trim();
const overallStatus = cleanList(input.overallStatus, STATUSES);
const studyTypes = cleanList(input.studyTypes, STUDY_TYPES);
const phases = cleanList(input.phases, PHASES);
const hasResultsOnly = input.hasResultsOnly === true;
const rowsPerStudy = input.rowsPerStudy === 'site' ? 'site' : 'study';
const maxResults = Math.min(Math.max(Number(input.maxResults ?? 100), 1), 50000);

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function apiGet(params) {
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
            const detail = parsed?.errors ? JSON.stringify(parsed.errors) : String(resp.body).slice(0, 300);
            log.warning(`ClinicalTrials.gov API ${resp.statusCode}: ${detail}`);
            return null;
        }
        if (!parsed) {
            log.warning(`ClinicalTrials.gov returned a non-JSON body: ${String(resp.body).slice(0, 200)}`);
            return null;
        }
        return parsed;
    }
    log.warning('ClinicalTrials.gov API kept erroring after 4 attempts; stopping early.');
    return null;
}

function baseParams() {
    const p = { pageSize: MAX_PAGE_SIZE };
    if (conditions) p['query.cond'] = conditions;
    if (interventions) p['query.intr'] = interventions;
    if (sponsors) p['query.spons'] = sponsors;
    if (locations) p['query.locn'] = locations;
    if (searchQuery) p['query.term'] = searchQuery;
    if (overallStatus.length) p['filter.overallStatus'] = overallStatus;
    // Verified live: `filter.hasResults` is rejected as unknown; `aggFilters=results:with` is
    // the real parameter name for this.
    if (hasResultsOnly) p.aggFilters = 'results:with';
    // studyType/phase are AREA-scoped fields, not top-level filters — combine into filter.advanced.
    const advanced = [];
    if (studyTypes.length) advanced.push(`AREA[StudyType](${studyTypes.join(' OR ')})`);
    if (phases.length) advanced.push(`AREA[Phase](${phases.join(' OR ')})`);
    if (advanced.length) p['filter.advanced'] = advanced.join(' AND ');
    return p;
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

log.info(
    `ClinicalTrials.gov: conditions="${conditions}" interventions="${interventions}" sponsors="${sponsors}" `
    + `locations="${locations}" searchQuery="${searchQuery}" overallStatus=[${overallStatus.join(',')}] `
    + `studyTypes=[${studyTypes.join(',')}] phases=[${phases.join(',')}] hasResultsOnly=${hasResultsOnly} `
    + `rowsPerStudy=${rowsPerStudy} maxResults=${maxResults}`,
);

let pageToken = null;
let scanned = 0;
let pages = 0;
let keepGoing = true;

while (keepGoing) {
    const params = baseParams();
    if (pageToken) params.pageToken = pageToken;
    const page = await apiGet(params);
    if (!page) break;
    const studies = listOf(page.studies);
    if (!studies.length) break;
    pages += 1;

    for (const study of studies) {
        scanned += 1;
        const row = normalizeStudy(study);
        if (rowsPerStudy === 'site') {
            const sites = row.locations.length ? row.locations : [null];
            for (const site of sites) {
                const { locations: _drop, locationCount: _drop2, ...studyFields } = row;
                keepGoing = await pushResult({ ...studyFields, site });
                if (!keepGoing) break;
            }
        } else {
            keepGoing = await pushResult(row);
        }
        if (!keepGoing) break;
    }

    pageToken = page.nextPageToken ?? null;
    if (!pageToken) break;
}

if (pushed === 0) {
    log.warning(
        `No studies matched. Scanned ${scanned} rows. Most common causes, in order: `
        + '(1) conditions/interventions/sponsors/locations/searchQuery are ANDed — combining several '
        + 'narrow filters often genuinely matches nothing; drop one and retry. '
        + '(2) phases only applies to interventional studies with a phase assigned; pairing it with '
        + 'studyTypes=["OBSERVATIONAL"] always returns nothing. '
        + '(3) hasResultsOnly is true on a small minority of studies — combine with a broad condition first.',
    );
}

log.info(`Done. Pushed ${pushed} rows over ${pages} page(s) (scanned ${scanned} studies, mode=${rowsPerStudy}).`);
await Actor.exit();
