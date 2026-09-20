import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';

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

// Confirmed live cycle 539: `notice_type` takes SAM's own single-letter codes (matches the
// codes SAM shows in the UI dropdown / that come back on each row's `type.code`).
const NOTICE_TYPE_CODES = {
    p: 'Presolicitation', o: 'Solicitation', k: 'Combined Synopsis/Solicitation',
    r: 'Sources Sought', a: 'Award Notice', s: 'Special Notice', g: 'Sale of Surplus',
    i: 'Intent to Bundle', u: 'Justification',
};

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

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
            log.warning(`SAM.gov request failed (${err.message}); retrying (${attempt}/4).`);
            await sleep(attempt * 2000);
            continue;
        }
        if (resp.statusCode === 429 || resp.statusCode >= 500) {
            log.warning(`SAM.gov returned ${resp.statusCode}; retrying (${attempt}/4).`);
            await sleep(attempt * 3000);
            continue;
        }
        if (resp.statusCode === 404) return null;
        let parsed = null;
        try { parsed = JSON.parse(resp.body); } catch { /* handled below */ }
        if (resp.statusCode !== 200 || !parsed) {
            log.warning(`SAM.gov ${url} returned ${resp.statusCode}, non-JSON or unexpected body: ${String(resp.body).slice(0, 200)}`);
            return null;
        }
        return parsed;
    }
    log.warning(`SAM.gov ${url} kept failing after 4 attempts; skipping.`);
    return null;
}

// Cycle 96 seed rule: never ship a default that makes the very first test run return 0 rows.
const keyword = String(input.keyword ?? 'contract').trim();
const naicsCodes = (Array.isArray(input.naicsCodes) ? input.naicsCodes : []).map((v) => String(v).trim()).filter(Boolean);
const setAsideTypes = (Array.isArray(input.setAsideTypes) ? input.setAsideTypes : []).map((v) => String(v).trim()).filter(Boolean);
const noticeTypes = (Array.isArray(input.noticeTypes) ? input.noticeTypes : [])
    .map((v) => String(v).toLowerCase().trim())
    .filter((v) => Object.hasOwn(NOTICE_TYPE_CODES, v));
const states = (Array.isArray(input.states) ? input.states : []).map((v) => String(v).toUpperCase().trim()).filter(Boolean);
const organizationId = String(input.organizationId ?? '').trim();
const activeOnly = input.activeOnly !== false; // default true
const enrichDetail = input.enrichDetail === true;
const maxResults = Math.min(Math.max(Number(input.maxResults ?? 200), 1), 10000); // 10k = confirmed backend depth cap (cycle 538)

log.info('Starting SAM.gov opportunity search', {
    keyword, naicsCodes, setAsideTypes, noticeTypes, states, organizationId, activeOnly, maxResults, enrichDetail,
});

function buildSearchUrl(page, size) {
    const params = new URLSearchParams({
        index: 'opp', mode: 'search', responseType: 'json',
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

async function enrichOne(item) {
    if (!item.opportunityId) return item;
    const detail = await apiGet(`${DETAIL_API}/${item.opportunityId}`);
    if (!detail?.data2) return item;
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

const PAGE_SIZE = 100;
const results = [];
let page = 0;
let total = Infinity;

while (results.length < maxResults && results.length < total) {
    const url = buildSearchUrl(page, PAGE_SIZE);
    const data = await apiGet(url);
    if (!data) { log.warning(`Page ${page} failed after retries; stopping.`); break; }
    total = Math.min(data.page?.totalElements ?? 0, 10000);
    const rows = data._embedded?.results ?? [];
    if (rows.length === 0) break;
    for (const row of rows) {
        results.push(normalizeRow(row));
        if (results.length >= maxResults) break;
    }
    log.info(`Page ${page}: +${rows.length} rows (total so far ${results.length}/${Math.min(total, maxResults)})`);
    page += 1;
    if (page * PAGE_SIZE >= 10000) { log.warning('Hit SAM.gov\'s 10,000-row backend depth cap; narrow keyword/filters for more.'); break; }
    await sleep(300); // stay well under any rate limit; verified spacing from the feasibility check
}

if (enrichDetail) {
    log.info(`Enriching ${results.length} rows with detail-call fields (naics, set-aside, place of performance, contacts)...`);
    for (const item of results) {
        await enrichOne(item);
        await sleep(200);
    }
}

if (results.length) await Actor.pushData(results);
log.info(`Done. Pushed ${results.length} opportunities.`);

await Actor.exit();
