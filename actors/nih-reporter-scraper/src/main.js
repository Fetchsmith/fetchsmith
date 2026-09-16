import { createHash } from 'node:crypto';
import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';

await Actor.init();
const input = (await Actor.getInput()) ?? {};

// NIH RePORTER's official public API (no API key, no auth). POST + JSON body, like Grants.gov
// and unlike Federal Register / ClinicalTrials.gov -- do not reuse a GET helper here.
const API = 'https://api.reporter.nih.gov/v2';

// Hard limits measured live (cycle 127): limit caps at 500/request (501 -> clean 400), and
// offset + limit may not exceed 15000 with NO cursor of any kind. A single fiscal year already
// holds >83k projects, so anything broad has to be chunked on a categorical dimension and merged
// -- see splitCriteria() below. These are the two numbers the whole pagination design hangs on.
const PAGE_LIMIT = 500;
const OFFSET_WALL = 15000;
const SPLIT_AT = 14500; // leave headroom: `total` drifts slightly between the probe and the walk

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function apiPost(path, body) {
    for (let attempt = 1; attempt <= 4; attempt += 1) {
        let resp;
        try {
            resp = await gotScraping({
                url: `${API}${path}`,
                method: 'POST',
                responseType: 'text',
                throwHttpErrors: false,
                retry: { limit: 0 },
                timeout: { request: 60000 },
                headers: { 'content-type': 'application/json', accept: 'application/json' },
                body: JSON.stringify(body),
            });
        } catch (err) {
            log.warning(`NIH RePORTER request failed (${err.message}); retrying (${attempt}/4).`);
            await sleep(attempt * 2000);
            continue;
        }
        if (resp.statusCode === 429 || resp.statusCode >= 500) {
            const waitS = Number(resp.headers['retry-after']) || attempt * 5;
            log.warning(`NIH RePORTER returned ${resp.statusCode}; retrying in ${waitS}s (${attempt}/4).`);
            await sleep(waitS * 1000);
            continue;
        }
        let parsed = null;
        try { parsed = JSON.parse(resp.body); } catch { /* handled below */ }
        if (resp.statusCode !== 200 || !parsed) {
            log.warning(`NIH RePORTER ${path} returned ${resp.statusCode}: ${String(resp.body).slice(0, 200)}`);
            return null;
        }
        return parsed;
    }
    log.warning(`NIH RePORTER ${path} kept failing after 4 attempts; stopping early.`);
    return null;
}

// THE TRAP (verified live, cycle 127): an unrecognised criteria FIELD NAME is silently ignored,
// not rejected -- {"criteria":{"totally_fake_field":"xyz"}} returns 200 and the entire unfiltered
// 2.97M-row index, i.e. a typo turns "filter by X" into "return everything" while still looking
// like a success. (A bad *value* on a real field does 400 cleanly; only names are silent.) Every
// criteria object is therefore checked against this allowlist before it is ever sent, and an
// unknown key is a hard failure rather than a silent full-index scan the customer pays for.
const CRITERIA_ALLOWLIST = new Set([
    'fiscal_years', 'include_active_projects', 'pi_names', 'po_names', 'pi_profile_ids',
    'org_names', 'org_names_exact_match', 'org_cities', 'org_states', 'org_countries',
    'project_nums', 'project_num_split', 'appl_ids', 'agencies', 'is_agency_admin',
    'is_agency_funding', 'activity_codes', 'award_types', 'dept_types', 'cong_dists',
    'funding_mechanism', 'organization_type', 'advanced_text_search', 'covid_response',
    'date_added', 'project_start_date', 'project_end_date', 'award_notice_date',
    'spending_categories', 'full_study_sections', 'foa', 'exclude_subprojects',
    'sub_project_only', 'multi_pi_only', 'newly_added_projects_only', 'use_relevance',
    'award_amount_range',
]);

// SECOND-ORDER FORM OF THE SAME TRAP (verified live, cycle 136): award_amount_range is a real
// field, but a HALF-FILLED one is silently ignored the same way an unknown field name is --
// {"min_amount":5000000} alone returned the full unfiltered 83531-row FY2024 total, byte-identical
// to the fake-field control, while {"min_amount":5000000,"max_amount":999999999} correctly returned
// 599. So the allowlist above is not enough here: the object must always be sent with BOTH bounds
// or not at all, or a "grants over $5M" request silently becomes "every grant" that the customer
// pays per result for. Missing bounds are filled with these sentinels; max_amount is capped at
// int32 (2147483647 works, 999999999999 makes the API 500).
const AMOUNT_MIN_SENTINEL = 0;
const AMOUNT_MAX_SENTINEL = 2147483647;

function assertCriteria(criteria) {
    const bad = Object.keys(criteria).filter((k) => !CRITERIA_ALLOWLIST.has(k));
    if (bad.length) throw new Error(`Refusing to send unknown NIH RePORTER criteria field(s): ${bad.join(', ')}. The API would silently ignore them and return the entire unfiltered index.`);
    return criteria;
}

// Administering agency / NIH Institute & Center codes, used both as a user filter and as the
// chunking dimension that walks past the 15000-row offset wall. NIH ICs plus the other HHS
// agencies whose awards appear in RePORTER.
const IC_CODES = [
    'NCI', 'NIAID', 'NHLBI', 'NIGMS', 'NIDDK', 'NINDS', 'NIMH', 'NIA', 'NICHD', 'NIDA',
    'NIAMS', 'NEI', 'NIEHS', 'NIDCD', 'NIDCR', 'NIAAA', 'NIBIB', 'NHGRI', 'NIMHD', 'NINR',
    'NLM', 'NCATS', 'NCCIH', 'FIC', 'OD', 'CC', 'CIT', 'CSR', 'NIOSH',
    'AHRQ', 'CDC', 'FDA', 'HRSA', 'SAMHSA', 'ACF', 'ACL', 'ASPR', 'VA', 'OASH',
];

const listOf = (v) => (Array.isArray(v) ? v.filter((x) => x !== null && x !== undefined && x !== '') : []);
const strList = (v) => listOf(v).map((x) => String(x).trim()).filter(Boolean);

const keyword = String(input.keyword ?? '').trim();
const includePublications = input.includePublications !== false;
const includeAbstract = input.includeAbstract !== false;
const maxResults = Math.min(Math.max(Number(input.maxResults ?? 100), 1), 20000);

const fiscalYears = listOf(input.fiscalYears).map((y) => Number(y)).filter((y) => Number.isInteger(y) && y >= 1985 && y <= 2100);
const agencyIcCodes = strList(input.agencyIcCodes).map((c) => c.toUpperCase());
const activityCodes = strList(input.activityCodes).map((c) => c.toUpperCase());
const awardTypes = strList(input.awardTypes);
const orgNames = strList(input.orgNames);
const orgStates = strList(input.orgStates).map((s) => s.toUpperCase());
const piNames = strList(input.piNames);
const projectNums = strList(input.projectNums);
const watchLabel = String(input.watchLabel ?? '').trim();
const watchChanges = Boolean(input.watchChanges);

const amountNum = (v) => {
    const n = Number(v);
    return Number.isFinite(n) && n >= 0 ? Math.min(Math.floor(n), AMOUNT_MAX_SENTINEL) : null;
};
const minAwardAmount = amountNum(input.minAwardAmount);
const maxAwardAmount = amountNum(input.maxAwardAmount);
if (minAwardAmount !== null && maxAwardAmount !== null && minAwardAmount > maxAwardAmount) {
    throw new Error(`minAwardAmount (${minAwardAmount}) is greater than maxAwardAmount (${maxAwardAmount}); no project can match that band.`);
}

if (minAwardAmount !== null || maxAwardAmount !== null) {
    log.warning(
        'Award-amount filtering is active. NIH RePORTER drops projects that have no award amount recorded '
        + 'from any amount-filtered query (~3% of rows in a measured FY2024 sample), so those will not appear '
        + 'in the results even if they match every other filter.',
    );
}

const unknownIcs = agencyIcCodes.filter((c) => !IC_CODES.includes(c));
if (unknownIcs.length) {
    log.warning(
        `Unrecognised agency/IC code(s): ${unknownIcs.join(', ')}. They are still sent as-is, but NIH RePORTER `
        + `will simply match nothing for them. Valid codes: ${IC_CODES.join(', ')}.`,
    );
}

// Exclusive lookup mode, same rule as grants-gov's oppNum and clinicaltrials' nctIds (cycles
// 123/125): when the user asks for specific project numbers, every other filter -- including a
// fiscal-year default -- is dropped, so a narrowing filter can never silently hide the exact
// project that was asked for by number.
const exclusiveProjectNums = projectNums.length > 0;

function buildCriteria() {
    if (exclusiveProjectNums) return assertCriteria({ project_nums: projectNums });
    const c = {};
    if (keyword) {
        c.advanced_text_search = {
            operator: 'and',
            search_field: 'projecttitle,abstracttext,terms',
            search_text: keyword,
        };
    }
    if (fiscalYears.length) c.fiscal_years = fiscalYears;
    if (agencyIcCodes.length) c.agencies = agencyIcCodes;
    if (activityCodes.length) c.activity_codes = activityCodes;
    if (awardTypes.length) c.award_types = awardTypes;
    if (orgNames.length) c.org_names = orgNames;
    if (orgStates.length) c.org_states = orgStates;
    if (piNames.length) c.pi_names = piNames.map((n) => ({ any_name: n }));
    if (minAwardAmount !== null || maxAwardAmount !== null) {
        c.award_amount_range = {
            min_amount: minAwardAmount ?? AMOUNT_MIN_SENTINEL,
            max_amount: maxAwardAmount ?? AMOUNT_MAX_SENTINEL,
        };
    }
    if (input.activeOnly === true) c.include_active_projects = true;
    if (input.newlyAddedOnly === true) c.newly_added_projects_only = true;
    if (input.excludeSubprojects !== false) c.exclude_subprojects = true;
    return assertCriteria(c);
}

async function countOf(criteria) {
    const page = await apiPost('/projects/search', { criteria: assertCriteria(criteria), limit: 1, offset: 0 });
    return Number(page?.meta?.total ?? 0);
}

// Chunking: pick the next unused categorical dimension and fan the query out across it, then
// merge and dedupe on appl_id. Fiscal year first (cheapest, and the user usually supplies several),
// then administering IC (a bounded ~40-value list), then award type. Returns null when there is
// nothing left to split on -- the caller then warns instead of silently truncating.
function splitCriteria(c) {
    if (Array.isArray(c.fiscal_years) && c.fiscal_years.length > 1) {
        return c.fiscal_years.map((y) => assertCriteria({ ...c, fiscal_years: [y] }));
    }
    if (!c.agencies) return IC_CODES.map((ic) => assertCriteria({ ...c, agencies: [ic] }));
    if (Array.isArray(c.agencies) && c.agencies.length > 1) {
        return c.agencies.map((a) => assertCriteria({ ...c, agencies: [a] }));
    }
    if (!c.award_types) return ['1', '2', '3', '4', '5', '6', '7', '8', '9'].map((t) => assertCriteria({ ...c, award_types: [t] }));
    return null;
}

const stripTerms = (t) => (t ? String(t).replace(/></g, '; ').replace(/^<|>$/g, '').trim() : null);

function normalize(row) {
    const org = row.organization ?? {};
    const ic = row.agency_ic_admin ?? {};
    const out = {
        applId: row.appl_id ?? null,
        projectNum: row.project_num ?? null,
        coreProjectNum: row.core_project_num ?? null,
        subprojectId: row.subproject_id ?? null,
        fiscalYear: row.fiscal_year ?? null,
        projectTitle: row.project_title ?? null,
        activityCode: row.activity_code ?? null,
        awardType: row.award_type ?? null,
        fundingMechanism: row.funding_mechanism ?? null,
        awardAmount: row.award_amount ?? null,
        directCostAmt: row.direct_cost_amt ?? null,
        indirectCostAmt: row.indirect_cost_amt ?? null,
        isActive: typeof row.is_active === 'boolean' ? row.is_active : null,
        isNew: typeof row.is_new === 'boolean' ? row.is_new : null,
        projectStartDate: row.project_start_date ?? null,
        projectEndDate: row.project_end_date ?? null,
        budgetStart: row.budget_start ?? null,
        budgetEnd: row.budget_end ?? null,
        awardNoticeDate: row.award_notice_date ?? null,
        dateAdded: row.date_added ?? null,
        agencyCode: row.agency_code ?? null,
        icCode: ic.code ?? null,
        icAbbreviation: ic.abbreviation ?? null,
        icName: ic.name ?? null,
        icFundings: listOf(row.agency_ic_fundings).map((f) => ({
            fiscalYear: f.fy ?? null,
            abbreviation: f.abbreviation ?? null,
            totalCost: f.total_cost ?? null,
        })),
        opportunityNumber: row.opportunity_number ?? null,
        cfdaCode: row.cfda_code ?? null,
        studySection: row.full_study_section?.name ?? null,
        spendingCategoriesDesc: row.spending_categories_desc ?? null,
        // PII check (CLAUDE.md rule 1), done live before this Actor was written and unusually for
        // this family the verdict was "ship as-is": the schema has NO email and NO phone field
        // anywhere. PI and program-officer names are the same class of already-public statutory
        // disclosure as a federal contract awardee's name -- reporter.nih.gov publishes them on
        // every project page. Nothing is dropped here because there is nothing personal to drop.
        contactPiName: row.contact_pi_name ?? null,
        principalInvestigators: listOf(row.principal_investigators).map((p) => ({
            fullName: p.full_name ?? null,
            title: p.title ?? null,
            isContactPi: typeof p.is_contact_pi === 'boolean' ? p.is_contact_pi : null,
            profileId: p.profile_id ?? null,
        })),
        programOfficers: listOf(row.program_officers).map((p) => p.full_name).filter(Boolean),
        orgName: org.org_name ?? null,
        orgCity: org.org_city ?? null,
        orgState: org.org_state ?? null,
        orgCountry: org.org_country ?? null,
        orgZip: org.org_zipcode ?? null,
        orgDeptType: org.dept_type ?? null,
        orgUei: org.primary_uei ?? null,
        orgType: row.organization_type?.name ?? null,
        congDist: row.cong_dist ?? null,
        latitude: row.geo_lat_lon?.lat ?? null,
        longitude: row.geo_lat_lon?.lon ?? null,
        terms: row.pref_terms ? String(row.pref_terms).split(';').map((t) => t.trim()).filter(Boolean) : stripTerms(row.terms)?.split('; ') ?? [],
        url: row.project_detail_url ?? (row.appl_id ? `https://reporter.nih.gov/project-details/${row.appl_id}` : null),
    };
    if (includeAbstract) {
        out.abstractText = row.abstract_text || null;
        out.publicHealthRelevance = row.phr_text || null;
    }
    return out;
}

// Differentiator: join each project to the PubMed papers it produced, via the sibling
// /publications/search endpoint. Verified live that core_project_nums accepts a BATCH -- two
// project numbers in one call returned both projects' papers -- so this costs roughly one extra
// request per 25 projects rather than one per project.
const PUB_BATCH = 25;
async function fetchPublications(coreNums) {
    const map = new Map();
    for (let i = 0; i < coreNums.length; i += PUB_BATCH) {
        const batch = coreNums.slice(i, i + PUB_BATCH);
        let offset = 0;
        for (;;) {
            const page = await apiPost('/publications/search', {
                criteria: { core_project_nums: batch },
                limit: PAGE_LIMIT,
                offset,
            });
            const rows = listOf(page?.results);
            for (const r of rows) {
                if (!r.coreproject || !r.pmid) continue;
                if (!map.has(r.coreproject)) map.set(r.coreproject, new Set());
                map.get(r.coreproject).add(r.pmid);
            }
            offset += rows.length;
            if (rows.length < PAGE_LIMIT || offset + PAGE_LIMIT > OFFSET_WALL) break;
        }
    }
    return map;
}

// ---------------------------------------------------------------------------
// Watch mode: a stateful "only what is new since my last run" filter, scoped to
// ONE saved query. Distinct from `newlyAddedOnly`, which reads NIH's own stateless
// "recently added to the index" flag and therefore still re-returns the same rows on
// every run until they age out of that flag. Here the baseline is the buyer's own:
// the appl_ids this label has already delivered, kept in a NAMED key-value store so it
// survives across runs (the default KV store is per-run and would reset every time).
const WATCH_STORE = 'fetchsmith-nih-watch';
const SEED_CAP = 15000; // == OFFSET_WALL: the most ids one un-split query can even reach
const WATCH_KEEP = 60000; // bound the record size; oldest ids fall off first

// `watchChanges`: an already-delivered appl_id is not frozen. NIH's own no-cost-extension
// process (verified live, cycle 355, against era.nih.gov's NCE documentation) updates the
// SAME award record's project period end date in eRA Commons -- no new appl_id is minted for
// an NCE, unlike a non-competing renewal which always gets a fresh appl_id (cycle 354). An
// administrative supplement or a status change (active -> closed) can likewise land on the
// same appl_id. These 4 fields are always present on a full (non-seeding) record, so tracking
// them costs no extra API calls beyond what a normal run already fetches.
function snapshotOf(row) {
    return {
        projectEndDate: row.project_end_date ?? null,
        budgetEnd: row.budget_end ?? null,
        awardAmount: row.award_amount ?? null,
        isActive: typeof row.is_active === 'boolean' ? row.is_active : null,
    };
}

// Same shape as snapshotOf(), read off an already-normalized item instead of a raw API row --
// used after pushResults() delivers an item, since by then only the normalized shape is in hand.
function snapshotFromItem(item) {
    return { projectEndDate: item.projectEndDate, budgetEnd: item.budgetEnd, awardAmount: item.awardAmount, isActive: item.isActive };
}

function changesBetween(prev, next) {
    if (!prev) return null;
    const types = [];
    const previous = {};
    for (const field of ['projectEndDate', 'budgetEnd', 'awardAmount', 'isActive']) {
        if (prev[field] !== undefined && prev[field] !== null && prev[field] !== next[field]) {
            types.push(field);
            previous[field] = prev[field];
        }
    }
    return types.length ? { types, previous } : null;
}

// Apify KV keys allow [a-zA-Z0-9!-_.'()] only, so the label is sanitised rather than
// trusted. The criteria fingerprint is part of the key on purpose: if the buyer edits a
// filter, that is a different question and gets its own baseline, instead of dumping
// every row the old narrower filter happened to exclude as if it were brand new.
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
let changedCount = 0;
// appl_id -> last-seen snapshot (or null, when watchChanges has never run for this label) of
// the 4 fields that can change on an otherwise-already-delivered project.
const watchSeen = new Map();

async function saveWatchRecord(status) {
    const entries = Array.from(watchSeen.entries()).slice(-WATCH_KEEP);
    await watchStore.setValue(watchKey, {
        ...watchRecord,
        label: watchLabel,
        fingerprint: watchRecord.fingerprint,
        criteria: rootCriteria,
        lastRunAt: new Date().toISOString(),
        lastRunStatus: status,
        runCount: (watchRecord.runCount ?? 0) + 1,
        seenCount: entries.length,
        // Compact per-entry shape: id plus the 4 snapshot fields (short keys because WATCH_KEEP
        // can hold up to 60,000 of these in one KV record). snap is null when watchChanges has
        // never run for this label -- stored as a bare id in that case, same as pre-this-feature
        // records, so a label that never turns watchChanges on keeps the smaller old format.
        seenIds: entries.map(([id, snap]) => (snap
            ? { i: id, e: snap.projectEndDate, b: snap.budgetEnd, a: snap.awardAmount, x: snap.isActive }
            : id)),
    });
}

let pushed = 0;
const seen = new Set(); // appl_id, so chunked queries can never double-charge for one project
const isPPE = Actor.getChargingManager().getPricingInfo().isPayPerEvent;

async function pushResults(items) {
    for (const item of items) {
        if (isPPE) {
            const r = await Actor.charge({ eventName: 'result', count: 1 });
            if (r.chargedCount === 0) return false;
            await Actor.pushData(item); pushed += 1;
            // Only a row the buyer was actually charged for counts as delivered: anything left
            // behind by maxResults or the charge limit stays "new" and comes back next run.
            if (watchMode && item.applId != null) {
                watchSeen.set(String(item.applId), watchChanges ? snapshotFromItem(item) : null);
                if (item._watchChangeType) changedCount += 1;
            }
            if (r.eventChargeLimitReached || pushed >= maxResults) return false;
        } else {
            await Actor.pushData(item); pushed += 1;
            if (watchMode && item.applId != null) {
                watchSeen.set(String(item.applId), watchChanges ? snapshotFromItem(item) : null);
                if (item._watchChangeType) changedCount += 1;
            }
            if (pushed >= maxResults) return false;
        }
    }
    return true;
}

// Walk one criteria object page by page, up to the offset wall. Returns false when the caller
// should stop entirely (charge limit or maxResults reached).
async function walkChunk(criteria, total) {
    let offset = 0;
    while (offset < Math.min(total, OFFSET_WALL) && (seeding || pushed < maxResults)) {
        if (seeding && watchSeen.size >= SEED_CAP) return false;
        // Never over-fetch: the publications join runs on whatever a page returns, so pulling a
        // full 500 rows to satisfy a maxResults of 100 would cost ~16 pointless extra requests.
        // A seeding run is the exception -- it wants ids only, so it always takes full pages and
        // asks the API for just the two id fields instead of the whole ~60-field project record.
        const limit = seeding
            ? Math.min(PAGE_LIMIT, OFFSET_WALL - offset)
            : Math.min(PAGE_LIMIT, OFFSET_WALL - offset, Math.max(maxResults - pushed, 1));
        const body = { criteria: assertCriteria(criteria), limit, offset };
        // watchChanges needs the 4 snapshot fields even during seeding (still far lighter than
        // the ~60-field full record); plain watchLabel keeps the original 2-field seed.
        if (seeding) {
            body.include_fields = watchChanges
                ? ['ApplId', 'ProjectNum', 'ProjectEndDate', 'BudgetEnd', 'AwardAmount', 'IsActive']
                : ['ApplId', 'ProjectNum'];
        }
        const page = await apiPost('/projects/search', body);
        const rows = listOf(page?.results);
        if (!rows.length) return true;

        const fresh = rows.filter((r) => r.appl_id == null || !seen.has(r.appl_id));
        for (const r of fresh) if (r.appl_id != null) seen.add(r.appl_id);

        if (seeding) {
            for (const r of fresh) if (r.appl_id != null) watchSeen.set(String(r.appl_id), watchChanges ? snapshotOf(r) : null);
            offset += rows.length;
            if (rows.length < limit) return true;
            continue;
        }

        // Watch mode: drop anything this label has already delivered BEFORE normalising or
        // joining publications, so a suppressed row costs neither an extra request nor a charge --
        // UNLESS watchChanges is on and the project's end date, budget end, award amount or
        // active flag moved since we last saw it, in which case it is kept and tagged with
        // exactly what changed. An unchanged already-seen row still gets its snapshot refreshed
        // here (uncharged) so drift is only ever measured from the most recent state.
        const changeById = new Map();
        const wanted = [];
        for (const r of fresh) {
            const id = r.appl_id != null ? String(r.appl_id) : null;
            if (id == null || !watchMode || !watchSeen.has(id)) { wanted.push(r); continue; }
            const change = watchChanges ? changesBetween(watchSeen.get(id), snapshotOf(r)) : null;
            if (change) { changeById.set(id, change); wanted.push(r); } else { watchSeen.set(id, snapshotOf(r)); }
        }
        if (!wanted.length) {
            offset += rows.length;
            if (rows.length < limit) return true;
            continue;
        }

        let items = wanted.map((r) => {
            const it = normalize(r);
            const change = it.applId != null ? changeById.get(String(it.applId)) : null;
            if (change) { it._watchChangeType = change.types; it._watchPrevious = change.previous; }
            return it;
        });
        if (includePublications && items.length) {
            const coreNums = Array.from(new Set(items.map((i) => i.coreProjectNum).filter(Boolean)));
            const pubs = await fetchPublications(coreNums);
            items = items.map((i) => {
                const pmids = i.coreProjectNum ? Array.from(pubs.get(i.coreProjectNum) ?? []) : [];
                return { ...i, publicationCount: pmids.length, pubmedIds: pmids };
            });
        }

        if (!(await pushResults(items))) return false;
        offset += rows.length;
        if (rows.length < limit) return true;
    }
    return true;
}

const rootCriteria = buildCriteria();

if (watchMode) {
    watchStore = await Actor.openKeyValueStore(WATCH_STORE);
    const { key, fingerprint } = watchKeyFor(watchLabel, rootCriteria);
    watchKey = key;
    const existing = await watchStore.getValue(key);
    if (existing && Array.isArray(existing.seenIds)) {
        watchRecord = existing;
        // Pre-watchChanges records stored `seenIds` as a flat array of ids -- handled here so an
        // existing buyer's baseline keeps working unchanged instead of needing a fresh seed the
        // day this feature shipped. Those ids simply have no snapshot yet (null), so watchChanges
        // only starts detecting drift from this point forward, not an artificial backlog.
        for (const entry of existing.seenIds) {
            if (entry && typeof entry === 'object') {
                watchSeen.set(String(entry.i), { projectEndDate: entry.e ?? null, budgetEnd: entry.b ?? null, awardAmount: entry.a ?? null, isActive: entry.x ?? null });
            } else {
                watchSeen.set(String(entry), null);
            }
        }
        log.info(
            `Watch mode "${watchLabel}" (${key}): baseline from ${existing.lastRunAt ?? 'an earlier run'} holds `
            + `${watchSeen.size} already-delivered project(s). Only projects NOT in that baseline are returned and charged`
            + (watchChanges ? ', plus any already-delivered project whose end date, budget end, award amount or active flag changed.' : '.'),
        );
    } else {
        watchRecord = { fingerprint, firstSeededAt: new Date().toISOString(), runCount: 0 };
        seeding = true;
        log.info(
            `Watch mode "${watchLabel}" (${key}): FIRST run for this label and filter set, so this is a baseline `
            + 'run. It records which projects already match and returns ZERO results (you are charged nothing). '
            + 'Run it again on the same label and filters -- on a schedule, typically -- to get only what is new since now.',
        );
    }
}

log.info(
    exclusiveProjectNums
        ? `NIH RePORTER: exact project-number lookup [${projectNums.join(', ')}] (all other filters ignored).`
        : `NIH RePORTER: keyword="${keyword || '(none)'}" fiscalYears=[${fiscalYears.join(',') || 'all'}]`
        + (agencyIcCodes.length ? ` agencies=[${agencyIcCodes.join(',')}]` : '')
        + (activityCodes.length ? ` activityCodes=[${activityCodes.join(',')}]` : '')
        + (orgStates.length ? ` orgStates=[${orgStates.join(',')}]` : '')
        + ` includePublications=${includePublications} maxResults=${maxResults}`,
);

const rootTotal = await countOf(rootCriteria);
log.info(`Matched ${rootTotal} project records before paging.`);

if (rootTotal > SPLIT_AT) {
    // Past the 15000-row wall: fan out across a categorical dimension and merge on appl_id.
    const chunks = splitCriteria(rootCriteria);
    if (!chunks) {
        log.warning(
            `${rootTotal} matches but no dimension left to split on -- NIH RePORTER caps offset+limit at ${OFFSET_WALL} `
            + 'and has no cursor, so only the first 15000 are reachable. Narrow the query (add a fiscal year, IC or state) to see the rest.',
        );
        await walkChunk(rootCriteria, rootTotal);
    } else {
        log.info(`Over the ${OFFSET_WALL}-row offset wall; splitting into ${chunks.length} sub-queries and merging on appl_id.`);
        for (const chunk of chunks) {
            if (pushed >= maxResults) break;
            const total = await countOf(chunk);
            if (!total) continue;
            if (total > SPLIT_AT) {
                const sub = splitCriteria(chunk);
                if (sub) {
                    for (const s of sub) {
                        if (pushed >= maxResults) break;
                        const t = await countOf(s);
                        if (!t) continue;
                        if (!(await walkChunk(s, t))) break;
                    }
                    continue;
                }
                log.warning(`A sub-query still has ${total} matches and cannot be split further; taking its first ${OFFSET_WALL}.`);
            }
            if (!(await walkChunk(chunk, total))) break;
        }
    }
} else {
    await walkChunk(rootCriteria, rootTotal);
}

if (watchMode) {
    await saveWatchRecord(seeding ? 'seeded' : 'incremental');
    if (seeding) {
        log.info(
            `Baseline saved for watch label "${watchLabel}": ${watchSeen.size} project(s) recorded as already-seen, `
            + '0 results returned, 0 charged. The next run on this label and these filters returns only new projects.'
            + (watchSeen.size >= SEED_CAP
                ? ` NOTE: the baseline hit the ${SEED_CAP}-project cap, which is also NIH RePORTER's own paging wall. `
                + 'Narrow the query (a fiscal year, IC or state) so the whole result set fits, or the first incremental '
                + 'run will report older projects past the cap as new.'
                : ''),
        );
    } else {
        log.info(
            `Watch label "${watchLabel}": ${pushed - changedCount} new project(s)`
            + (watchChanges ? ` and ${changedCount} changed project(s) (end date/budget end/award amount/active flag)` : '')
            + ` since the last run; baseline now holds ${watchSeen.size}.`,
        );
    }
}

if (pushed === 0 && !seeding) {
    log.warning(
        watchMode
            ? `Nothing new for watch label "${watchLabel}" since its last run -- every matching project had already been `
            + 'delivered. That is the expected result most of the time; you were charged for nothing.'
            : exclusiveProjectNums
            ? `No project found for [${projectNums.join(', ')}]. Use a full project number (5R01CA234538-06) or a core number (R01CA234538) exactly as shown on reporter.nih.gov.`
            : 'No projects matched. Most common causes: (1) all filters are ANDed -- a narrow keyword plus IC plus '
            + 'activity code often has zero real matches, drop one and retry; (2) an IC code that is not a real NIH '
            + 'institute matches nothing (a warning above lists any); (3) fiscal years before 1985 have no data.',
    );
}

log.info(`Done. Pushed ${pushed} project records.`);
await Actor.exit();
