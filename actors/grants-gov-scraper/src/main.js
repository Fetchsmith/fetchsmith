import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';
import { createHash } from 'node:crypto';

await Actor.init();
const input = (await Actor.getInput()) ?? {};

// Grants.gov's own internal search API (no API key, no auth). It is POST + JSON body, unlike
// Federal Register / ClinicalTrials.gov which are both GET — do not reuse a GET helper here.
const API = 'https://api.grants.gov/v1/api';

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// Verified live (cycle 124/125): this API NEVER returns an HTTP error status or a non-zero
// errorcode for a bad parameter or a typo'd enum -- it returns errorcode 0, "Webservice
// Succeeds", and a silently empty (hitCount: 0) result set. There is nothing to catch a mistake,
// so every enum-shaped input below is either constrained by the input schema itself (Apify
// validates enums server-side before the Actor even runs) or resolved against a live value list
// in this file. Only network/5xx failures are retried here.
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
                timeout: { request: 30000 },
                headers: { 'content-type': 'application/json', accept: 'application/json' },
                body: JSON.stringify(body),
            });
        } catch (err) {
            log.warning(`Grants.gov request failed (${err.message}); retrying (${attempt}/4).`);
            await sleep(attempt * 2000);
            continue;
        }
        if (resp.statusCode === 429 || resp.statusCode >= 500) {
            const waitS = Number(resp.headers['retry-after']) || attempt * 5;
            log.warning(`Grants.gov returned ${resp.statusCode}; retrying in ${waitS}s (${attempt}/4).`);
            await sleep(waitS * 1000);
            continue;
        }
        let parsed = null;
        try { parsed = JSON.parse(resp.body); } catch { /* handled below */ }
        if (resp.statusCode !== 200 || !parsed) {
            log.warning(`Grants.gov ${path} returned ${resp.statusCode}, non-JSON or unexpected body: ${String(resp.body).slice(0, 200)}`);
            return null;
        }
        return parsed;
    }
    log.warning(`Grants.gov ${path} kept failing after 4 attempts; stopping early.`);
    return null;
}

const keyword = String(input.keyword ?? '').trim();
const oppStatuses = (Array.isArray(input.oppStatuses) && input.oppStatuses.length ? input.oppStatuses : ['forecasted', 'posted']).join('|');
const eligibilities = (input.eligibilities ?? []).join('|');
const fundingCategories = (input.fundingCategories ?? []).join('|');
const fundingInstruments = (input.fundingInstruments ?? []).join('|');
const cfda = String(input.cfda ?? '').trim();
const oppNum = String(input.oppNum ?? '').trim();
const sortBy = String(input.sortBy ?? '');
const maxResults = Math.min(Math.max(Number(input.maxResults ?? 100), 1), 20000);
const watchLabel = String(input.watchLabel ?? '').trim();

// Verified live: dateRange takes any positive integer number of days (not just the 3/7/14/...
// preset buttons the site's own facet list advertises -- dateRange:"10" returned a real
// in-between count), but like every other param on this API a garbage value is never rejected,
// just silently matches nothing. Validate client-side rather than trust the platform's plain
// "integer" schema type (a caller could still post a negative number via a raw API call).
let postedWithinDays = null;
if (input.postedWithinDays !== undefined && input.postedWithinDays !== null && input.postedWithinDays !== '') {
    const n = Number(input.postedWithinDays);
    if (Number.isFinite(n) && n >= 1) postedWithinDays = Math.floor(n);
    else log.warning(`Ignoring invalid postedWithinDays "${input.postedWithinDays}" (must be a positive number of days).`);
}

// Grants.gov's API has no absolute-date filter at all (verified live: posting a
// postedFromDate/postedToDate body param is silently dropped, not echoed back in
// searchParams and not applied). openDate is already present on every thin search2 row
// though (even archived ones), so an absolute range is applied client-side after fetch --
// zero extra requests, same cost as no filter at all. Parsed once here as real Date objects
// so the per-row filter below is a cheap comparison, not a re-parse every iteration.
function parseIsoDate(s, label) {
    if (s === undefined || s === null || s === '') return null;
    const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(s).trim());
    if (!m) {
        log.warning(`Ignoring invalid ${label} "${s}" (expected YYYY-MM-DD).`);
        return null;
    }
    const d = new Date(Date.UTC(Number(m[1]), Number(m[2]) - 1, Number(m[3])));
    if (Number.isNaN(d.getTime())) {
        log.warning(`Ignoring invalid ${label} "${s}" (expected YYYY-MM-DD).`);
        return null;
    }
    return d;
}
function parseUsDate(s) {
    const m = /^(\d{2})\/(\d{2})\/(\d{4})$/.exec(String(s ?? ''));
    if (!m) return null;
    const d = new Date(Date.UTC(Number(m[3]), Number(m[1]) - 1, Number(m[2])));
    return Number.isNaN(d.getTime()) ? null : d;
}
const postedFrom = parseIsoDate(input.postedFrom, 'postedFrom');
const postedTo = parseIsoDate(input.postedTo, 'postedTo');
if (postedFrom !== null && postedTo !== null && postedFrom > postedTo) {
    throw new Error(`postedFrom (${input.postedFrom}) is after postedTo (${input.postedTo}).`);
}
const hasAbsoluteDateFilter = postedFrom !== null || postedTo !== null;
if (hasAbsoluteDateFilter && postedWithinDays !== null) {
    log.warning('Both postedWithinDays and postedFrom/postedTo are set; ignoring postedWithinDays since an absolute range was given.');
}

// awardCeiling only exists on the per-opportunity detail record (search2's thin rows have no
// award data at all), so either bound forces enrich on regardless of the input's own "enrich"
// value -- otherwise the filter would silently have nothing to compare against and every row
// would look like a non-match.
const minAwardAmount = Number.isFinite(Number(input.minAwardAmount)) && input.minAwardAmount !== '' && input.minAwardAmount != null ? Number(input.minAwardAmount) : null;
const maxAwardAmount = Number.isFinite(Number(input.maxAwardAmount)) && input.maxAwardAmount !== '' && input.maxAwardAmount != null ? Number(input.maxAwardAmount) : null;
if (minAwardAmount !== null && maxAwardAmount !== null && minAwardAmount > maxAwardAmount) {
    throw new Error(`minAwardAmount (${minAwardAmount}) is greater than maxAwardAmount (${maxAwardAmount}).`);
}
const enrich = input.enrich !== false || minAwardAmount !== null || maxAwardAmount !== null;
const PAGE_SIZE = 1000; // No row cap was found (5000 verified in one call), but keeping requests
// modest means a mid-run failure loses less already-scanned work.

// Agency codes are validated against the live facet list (fetched below) rather than assumed:
// unlike Federal Register, a PARENT agency code here does not roll up to its sub-agencies
// (verified live: "USDA" alone -> 0 hits even though 26 real USDA-* opportunities exist under
// sub-agency codes like "USDA-NIFA"). A parent code is expanded to itself plus every one of its
// sub-agency codes so a user who reasonably types "USDA" still gets USDA-NIFA/USDA-FS/etc.
async function loadAgencyIndex() {
    const probe = await apiPost('/search2', { rows: 1 });
    const list = probe?.data?.agencies;
    const index = new Map(); // code (upper) -> [expanded codes]
    if (!Array.isArray(list)) return index;
    for (const parent of list) {
        const subCodes = (parent.subAgencyOptions ?? []).map((s) => s.value).filter(Boolean);
        index.set(String(parent.value).toUpperCase(), [parent.value, ...subCodes]);
        for (const sub of parent.subAgencyOptions ?? []) {
            if (sub.value) index.set(String(sub.value).toUpperCase(), [sub.value]);
        }
    }
    return index;
}

const agencyIndex = await loadAgencyIndex();
const wantedAgencies = (input.agencies ?? []).map((a) => String(a).trim()).filter(Boolean);
const resolvedAgencies = [];
const unknownAgencies = [];
for (const raw of wantedAgencies) {
    const hit = agencyIndex.get(raw.toUpperCase());
    if (hit) resolvedAgencies.push(...hit);
    else unknownAgencies.push(raw);
}
if (unknownAgencies.length) {
    log.warning(
        `Ignoring ${unknownAgencies.length} unrecognised agency code(s): ${unknownAgencies.join(', ')}. `
        + 'Use a code from https://www.grants.gov/search-grants (e.g. "NSF", "USDA-NIFA", "DOD-AMC"); '
        + 'a parent code like "USDA" or "DOD" is automatically expanded to its sub-agencies.',
    );
}
const agencies = Array.from(new Set(resolvedAgencies)).join('|');

// Exclusive lookup mode. Verified live: oppNum is ANDed with every other filter INCLUDING the
// server's own default oppStatuses ("forecasted|posted"), so a bare {"oppNum": "..."} lookup of
// a CLOSED or ARCHIVED opportunity silently returns zero rows -- indistinguishable from a typo.
// Same class of bug as clinicaltrials-scraper's nctIds + schema-default "cancer" interaction
// (cycle 123): when oppNum is set, every other filter is dropped and oppStatuses is forced to
// all four values so status can never hide the exact opportunity the user asked for by number.
const exclusiveOppNum = oppNum.length > 0;

// ---------------------------------------------------------------------------
// Watch mode: "only what is new since my last run", per saved query. Same shape as
// federal-register-scraper (cycle 297) and nih-reporter-scraper (cycle 296) -- copy that
// design, don't reinvent it.
//
// The baseline is the buyer's own -- the opportunity `id`s this label has already delivered --
// kept in a NAMED key-value store so it survives across runs. The default KV store is per-run
// and would reset the baseline every time, i.e. re-charge the whole result set on every
// scheduled run. `id` (not `opportunityNumber`) is the stable identity: it's what
// `/fetchOpportunity` and the public detail URL key off, whereas `opportunityNumber` is a
// human-facing label an agency could in principle reuse or amend.
const WATCH_STORE = 'fetchsmith-grants-watch';
const SEED_CAP = 20000; // Grants.gov's own startRecordNum paging has no wall (cycle 124: rows:5000
// returned in one call, deep offsets page fine) -- this is our own bound on a seed walk's runtime,
// not a server limit.
const WATCH_KEEP = 60000; // bound the record size; oldest ids fall off first

if (watchLabel && exclusiveOppNum) {
    log.warning('watchLabel is ignored when Opportunity number (oppNum) is set -- an exact single-opportunity lookup has no "new since last run" to track.');
}
const watchMode = watchLabel.length > 0 && !exclusiveOppNum;

// Apify KV keys allow [a-zA-Z0-9!-_.'()] only, so the label is sanitised rather than trusted.
// The criteria fingerprint is part of the key on purpose: if the buyer edits a filter, that is
// a different question and gets its own baseline, instead of dumping every opportunity the old
// narrower filter happened to exclude as if it were brand new.
//
// postedWithinDays IS in the fingerprint, unlike a resolved date -- its raw value (an integer
// day count) never changes on its own, only the window it resolves to at run time does. The
// federal-register-scraper trap (cycle 297) was fingerprinting a *computed absolute date* from a
// rolling default; here there is no such computed value in the criteria at all (postedWithinDays
// is passed to the API as a raw day count, and postedFrom/postedTo are the buyer's own literal
// strings), so there is nothing relative to accidentally bake in.
function watchKeyFor(label, criteria) {
    const safe = label.toLowerCase().replace(/[^a-z0-9_.-]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 40) || 'default';
    const fp = createHash('sha1').update(JSON.stringify(criteria, Object.keys(criteria).sort())).digest('hex').slice(0, 10);
    return { key: `watch-${safe}-${fp}`, fingerprint: fp };
}

const watchCriteria = {
    keyword,
    oppStatuses: oppStatuses.split('|').sort(),
    agencies: wantedAgencies.map((a) => a.toUpperCase()).sort(),
    eligibilities: eligibilities.split('|').filter(Boolean).sort(),
    fundingCategories: fundingCategories.split('|').filter(Boolean).sort(),
    fundingInstruments: fundingInstruments.split('|').filter(Boolean).sort(),
    cfda,
    postedWithinDays,
    postedFrom: input.postedFrom ? String(input.postedFrom).trim() : null,
    postedTo: input.postedTo ? String(input.postedTo).trim() : null,
    minAwardAmount,
    maxAwardAmount,
};

let watchStore = null;
let watchKey = null;
let watchRecord = null;
let seeding = false;
const watchSeen = new Set(); // opportunity `id`s already delivered under this label+fingerprint

async function saveWatchRecord(status) {
    const ids = Array.from(watchSeen).slice(-WATCH_KEEP);
    await watchStore.setValue(watchKey, {
        ...watchRecord,
        label: watchLabel,
        criteria: watchCriteria,
        lastRunAt: new Date().toISOString(),
        lastRunStatus: status,
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
            + `${watchSeen.size} already-delivered opportunity(ies). Only opportunities NOT in that baseline are returned and charged.`,
        );
    } else {
        watchRecord = { fingerprint, firstSeededAt: new Date().toISOString(), runCount: 0 };
        seeding = true;
        log.info(
            `Watch mode "${watchLabel}" (${key}): FIRST run for this label and filter set, so this is a baseline run. `
            + 'It records which opportunities already match and returns ZERO results (you are charged nothing). Run it '
            + 'again on the same label and filters -- on a schedule, typically -- to get only what is new since now.',
        );
    }
}

function baseParams() {
    if (exclusiveOppNum) {
        return { resultType: 'json', oppNum, oppStatuses: 'forecasted|posted|closed|archived', rows: PAGE_SIZE };
    }
    const p = {
        resultType: 'json',
        rows: PAGE_SIZE,
        oppStatuses,
        keyword,
        keywordEncoded: false,
    };
    if (agencies) p.agencies = agencies;
    if (eligibilities) p.eligibilities = eligibilities;
    if (fundingCategories) p.fundingCategories = fundingCategories;
    if (fundingInstruments) p.fundingInstruments = fundingInstruments;
    if (cfda) p.cfda = cfda;
    if (sortBy) p.sortBy = sortBy;
    if (postedWithinDays !== null && !hasAbsoluteDateFilter) p.dateRange = String(postedWithinDays);
    return p;
}

const stripHtml = (html) => (html ? String(html).replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim() : null);
const listOf = (v) => (Array.isArray(v) ? v.filter(Boolean) : []);

// awardCeiling/awardFloor come back as STRINGS, not numbers, and -- found while testing the new
// award-amount filter below -- the literal string "none" (not null, not "0", not omitted) is how
// the API spells "no ceiling set" whenever there is one: measured live on a 60-opportunity sample,
// 19/60 (~32%) had a literal "none" awardCeiling. Every enriched row has been shipping this raw,
// inconsistently-typed string since the Actor's first build; parse it into a real number (or null)
// here so both the output and the new amount filter below get a consistent type.
function parseMoney(v) {
    if (typeof v !== 'string') return null;
    const n = Number(v);
    return Number.isFinite(n) ? n : null; // covers "none" and any other non-numeric string
}

function normalizeThin(row) {
    return {
        id: row.id ?? null,
        opportunityNumber: row.number ?? null,
        title: row.title ?? null,
        agencyCode: row.agencyCode ?? null,
        agency: row.agency ?? null,
        openDate: row.openDate || null,
        closeDate: row.closeDate || null,
        oppStatus: row.oppStatus ?? null,
        docType: row.docType ?? null,
        cfdaList: listOf(row.cfdaList),
        url: row.id ? `https://www.grants.gov/search-results-detail/${row.id}` : null,
    };
}

// PII rule (CLAUDE.md rule 1), decided before any code was written and RE-VERIFIED against the
// live detail response before writing this function: the detail API's synopsis.agencyName /
// agencyPhone / agencyAddressDesc / agencyContactName / agencyContactPhone / agencyContactDesc /
// agencyContactEmail / agencyContactEmailDesc, and the top-level publisherUid, are agency-entered
// free text that is INCONSISTENT -- sometimes a department name (NSF), sometimes a named
// individual program officer with a direct phone/email ("Andrew Day, Grants/Agreements Officer",
// verified live on opportunity 332894). Because it cannot be reliably told apart per-row, ALL
// eight of those synopsis fields plus publisherUid are dropped entirely, never just filtered.
// The clean, always-organizational replacement is agencyDetails/topAgencyDetails (code + name),
// which stayed a department/bureau name on every sample checked.
function normalizeEnriched(detail) {
    const s = detail.synopsis ?? {};
    const ad = detail.agencyDetails ?? {};
    const tad = detail.topAgencyDetails ?? {};
    return {
        agencyName: ad.agencyName ?? null,
        agencyCode: ad.agencyCode ?? null,
        topAgencyName: tad.agencyName ?? null,
        topAgencyCode: tad.agencyCode ?? null,
        opportunityCategory: detail.opportunityCategory?.description ?? null,
        postingDate: s.postingDate ?? null,
        responseDate: s.responseDate ?? null,
        archiveDate: s.archiveDate ?? null,
        costSharing: typeof s.costSharing === 'boolean' ? s.costSharing : null,
        awardCeiling: parseMoney(s.awardCeiling),
        awardFloor: parseMoney(s.awardFloor),
        applicantEligibilityDesc: s.applicantEligibilityDesc || null,
        applicantTypes: listOf(s.applicantTypes).map((t) => t.description).filter(Boolean),
        fundingInstruments: listOf(s.fundingInstruments).map((t) => t.description).filter(Boolean),
        fundingActivityCategories: listOf(s.fundingActivityCategories).map((t) => t.description).filter(Boolean),
        synopsisText: stripHtml(s.synopsisDesc),
        cfdas: listOf(detail.cfdas).filter((c) => c.cfdaNumber).map((c) => ({ number: c.cfdaNumber, title: c.programTitle ?? null })),
        fundingDescLinkUrl: s.fundingDescLinkUrl || null,
        synopsisDocumentURLs: listOf(detail.synopsisDocumentURLs).map((d) => ({ url: d.docUrl ?? null, description: d.description ?? null })).filter((d) => d.url),
        assistURL: detail.assistURL || null,
        lastUpdatedDate: s.lastUpdatedDate ?? null,
        modComments: s.modComments || null,
    };
}

// Detail lookups measured at ~0.35s each; run a small concurrent pool rather than one at a time
// so enrich:true stays usable for a few hundred rows without hammering the API.
const ENRICH_CONCURRENCY = 5;
async function enrichBatch(rows) {
    const out = new Array(rows.length).fill(null);
    let next = 0;
    async function worker() {
        for (;;) {
            const i = next; next += 1;
            if (i >= rows.length) return;
            const detail = await apiPost('/fetchOpportunity', { opportunityId: rows[i].id });
            if (detail?.data && !detail.data.errorMessages?.length && detail.data.synopsis) {
                out[i] = normalizeEnriched(detail.data);
            } else {
                out[i] = null; // detail not available (e.g. archived without a synopsis) -- keep the thin row
            }
        }
    }
    await Promise.all(Array.from({ length: Math.min(ENRICH_CONCURRENCY, rows.length) }, worker));
    return out;
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
    exclusiveOppNum
        ? `Grants.gov: exact opportunity-number lookup "${oppNum}" (all statuses, other filters ignored).`
        : `Grants.gov: keyword="${keyword || '(none)'}" oppStatuses=[${oppStatuses}] enrich=${enrich} maxResults=${maxResults}`
        + (agencies ? ` agencies=[${agencies}]` : '')
        + (eligibilities ? ` eligibilities=[${eligibilities}]` : '')
        + (fundingCategories ? ` fundingCategories=[${fundingCategories}]` : '')
        + (fundingInstruments ? ` fundingInstruments=[${fundingInstruments}]` : '')
        + (cfda ? ` cfda=${cfda}` : '')
        + (sortBy ? ` sortBy=${sortBy}` : '')
        + (postedWithinDays !== null && !hasAbsoluteDateFilter ? ` postedWithinDays=${postedWithinDays}` : '')
        + (postedFrom !== null ? ` postedFrom=${input.postedFrom}` : '')
        + (postedTo !== null ? ` postedTo=${input.postedTo}` : '')
        + (minAwardAmount !== null ? ` minAwardAmount=${minAwardAmount}` : '')
        + (maxAwardAmount !== null ? ` maxAwardAmount=${maxAwardAmount}` : '')
        + (watchMode ? ` watchLabel="${watchLabel}"` : ''),
);
if (minAwardAmount !== null || maxAwardAmount !== null) {
    log.info(
        'Award-amount filtering drops any opportunity with no usable award ceiling: unposted '
        + '"forecast" listings with no detail record at all (~3% of the index), AND opportunities '
        + 'whose detail record literally has no ceiling set (Grants.gov spells this as the string '
        + '"none", measured live at roughly a third to half of posted opportunities depending on the '
        + 'agency/category mix) -- a real, common case, not a rare edge case.',
    );
}

let scanned = 0;
let droppedNoAward = 0;
let droppedOutOfRange = 0;
let skippedSeen = 0;

// Walks the full startRecordNum offset paging exactly once, applying enrichment and the
// amount/date filters in one place, so the real run and the watch-mode seed walk can never
// drift out of sync. `onBatch` receives the filtered, normalized rows for one page and
// returns whether to keep paging.
//
// `thinOnly` skips enrichment -- and therefore the amount filter, which needs it -- UNLESS the
// buyer's own amount filter forces it anyway. That's what keeps a watch-mode seed cheap: for
// the common case (no amount filter), no enrich-only field (agency name, synopsis text, etc.)
// can ever change whether an opportunity is in the match set, so seeding has no reason to pay
// for a per-row detail fetch across the WHOLE result set. When an amount filter is set, an
// opportunity's award ceiling can genuinely change between seed time and a later run (an agency
// raises/sets a ceiling), so skipping enrichment there would let a newly-matching opportunity
// get wrongly baked into the "already seen" baseline and never surface as new -- enrichment
// stays on in that case even during seeding.
async function walkMatches(onBatch, { thinOnly = false } = {}) {
    const needsEnrich = minAwardAmount !== null || maxAwardAmount !== null ? true : (thinOnly ? false : enrich);
    let startRecordNum = 0;
    let keepGoing = true;
    while (keepGoing) {
        const params = { ...baseParams(), startRecordNum };
        const page = await apiPost('/search2', params);
        const hits = listOf(page?.data?.oppHits);
        if (!hits.length) break;
        scanned += hits.length;

        const thin = hits.map(normalizeThin);
        let batch = thin;
        if (needsEnrich) {
            const details = await enrichBatch(hits);
            batch = thin.map((row, i) => (details[i] ? { ...row, ...details[i] } : row));
        }
        if (minAwardAmount !== null || maxAwardAmount !== null) {
            batch = batch.filter((row) => {
                if (typeof row.awardCeiling !== 'number') { droppedNoAward += 1; return false; }
                if (minAwardAmount !== null && row.awardCeiling < minAwardAmount) return false;
                if (maxAwardAmount !== null && row.awardCeiling > maxAwardAmount) return false;
                return true;
            });
        }
        if (hasAbsoluteDateFilter && !exclusiveOppNum) {
            batch = batch.filter((row) => {
                const opened = parseUsDate(row.openDate);
                if (opened === null) { droppedOutOfRange += 1; return false; }
                if (postedFrom !== null && opened < postedFrom) return false;
                if (postedTo !== null && opened > postedTo) return false;
                return true;
            });
        }

        keepGoing = await onBatch(batch);
        startRecordNum += hits.length;
        if (hits.length < PAGE_SIZE) break; // last page
    }
}

// Seeding only needs the ids, so (outside an amount filter) it skips enrichment entirely.
// It walks the WHOLE match set, unbounded by maxResults -- a baseline that stopped early would
// report every opportunity past the stopping point as "new" on the first incremental run.
async function seedBaseline() {
    await walkMatches(async (batch) => {
        for (const row of batch) {
            if (row.id != null) watchSeen.add(String(row.id));
            if (watchSeen.size >= SEED_CAP) return false;
        }
        return true;
    }, { thinOnly: true });
    log.info(`Baseline walk: ${watchSeen.size} opportunity id(s) recorded.`);
}

if (watchMode && seeding) await seedBaseline();

let beforePush = 0;
if (!seeding) {
    await walkMatches(async (batch) => {
        for (const row of batch) {
            // Already delivered under this watch label: dropped before any charge, so an
            // opportunity is never paid for twice.
            if (watchMode && row.id != null && watchSeen.has(String(row.id))) {
                skippedSeen += 1;
                continue;
            }
            const cont = await pushResult(row);
            // Recorded as delivered only after the charge actually succeeded -- anything
            // dropped by maxResults or a charge limit stays "new" for the next run.
            if (watchMode && row.id != null && pushed > beforePush) watchSeen.add(String(row.id));
            beforePush = pushed;
            if (!cont) return false;
        }
        return true;
    });
}

if (watchMode) {
    await saveWatchRecord(seeding ? 'seeded' : 'incremental');
    if (seeding) {
        log.info(
            `Baseline saved for watch label "${watchLabel}": ${watchSeen.size} opportunity(ies) recorded as already-seen, `
            + '0 results returned, 0 charged. The next run on this label and these filters returns only new opportunities.'
            + (watchSeen.size >= SEED_CAP
                ? ` NOTE: the baseline stopped at the ${SEED_CAP}-opportunity cap. Narrow the query (a keyword, an `
                + 'agency, a shorter posted-date window) so the whole result set fits, or the first incremental run '
                + 'will report opportunities past the cap as new.'
                : ''),
        );
    } else {
        log.info(
            `Watch label "${watchLabel}": ${pushed} new opportunity(ies) since the last run `
            + `(${skippedSeen} already-delivered row(s) skipped, uncharged); baseline now holds ${watchSeen.size}.`,
        );
    }
}

if (pushed === 0 && watchMode && !seeding) {
    log.warning(
        `Nothing new for watch label "${watchLabel}" since its last run -- all ${skippedSeen} matching opportunity(ies) `
        + 'had already been delivered. That is the expected result most of the time; you were charged for nothing.',
    );
} else if (pushed === 0 && !seeding) {
    log.warning(
        exclusiveOppNum
            ? `No opportunity found with number "${oppNum}". Check the exact number on grants.gov/search-grants.`
            : 'No opportunities matched. Most common causes: (1) filters are ANDed -- a narrow '
            + 'keyword plus agency plus eligibility often has zero real matches, drop one and retry; '
            + '(2) oppStatuses defaults to forecasted+posted (open/upcoming only) -- add "closed" or '
            + '"archived" to search history; (3) an unrecognised agency code is dropped with a warning '
            + 'above, not guessed at; (4) postedWithinDays/postedFrom/postedTo are hard AND filters -- a '
            + 'small window plus a narrow keyword can easily have zero real matches; (5) '
            + 'minAwardAmount/maxAwardAmount excludes any row with no detail record at all, not just '
            + 'rows outside the range.',
    );
}

log.info(
    `Done. Pushed ${pushed} opportunities (scanned ${scanned} rows).`
    + (droppedNoAward ? ` Dropped ${droppedNoAward} row(s) with no award ceiling to compare against the amount filter.` : '')
    + (droppedOutOfRange ? ` Dropped ${droppedOutOfRange} row(s) outside the postedFrom/postedTo range.` : ''),
);
await Actor.exit();
