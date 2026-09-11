import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';

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
const enrich = input.enrich !== false;
const maxResults = Math.min(Math.max(Number(input.maxResults ?? 100), 1), 20000);
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
    return p;
}

const stripHtml = (html) => (html ? String(html).replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim() : null);
const listOf = (v) => (Array.isArray(v) ? v.filter(Boolean) : []);

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
        awardCeiling: s.awardCeiling ?? null,
        awardFloor: s.awardFloor ?? null,
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
async function pushResults(items) {
    for (const item of items) {
        if (isPPE) {
            const r = await Actor.charge({ eventName: 'result', count: 1 });
            if (r.chargedCount === 0) return false;
            await Actor.pushData(item); pushed += 1;
            if (r.eventChargeLimitReached || pushed >= maxResults) return false;
        } else {
            await Actor.pushData(item); pushed += 1;
            if (pushed >= maxResults) return false;
        }
    }
    return true;
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
        + (sortBy ? ` sortBy=${sortBy}` : ''),
);

let startRecordNum = 0;
let scanned = 0;
let keepGoing = true;

while (keepGoing && pushed < maxResults) {
    const params = { ...baseParams(), startRecordNum };
    const page = await apiPost('/search2', params);
    const hits = listOf(page?.data?.oppHits);
    if (!hits.length) break;
    scanned += hits.length;

    const thin = hits.map(normalizeThin);
    let batch = thin;
    if (enrich) {
        const details = await enrichBatch(hits);
        batch = thin.map((row, i) => (details[i] ? { ...row, ...details[i] } : row));
    }

    keepGoing = await pushResults(batch);
    startRecordNum += hits.length;
    if (hits.length < PAGE_SIZE) break; // last page
}

if (pushed === 0) {
    log.warning(
        exclusiveOppNum
            ? `No opportunity found with number "${oppNum}". Check the exact number on grants.gov/search-grants.`
            : 'No opportunities matched. Most common causes: (1) filters are ANDed -- a narrow '
            + 'keyword plus agency plus eligibility often has zero real matches, drop one and retry; '
            + '(2) oppStatuses defaults to forecasted+posted (open/upcoming only) -- add "closed" or '
            + '"archived" to search history; (3) an unrecognised agency code is dropped with a warning '
            + 'above, not guessed at.',
    );
}

log.info(`Done. Pushed ${pushed} opportunities (scanned ${scanned} rows).`);
await Actor.exit();
