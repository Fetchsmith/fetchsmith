import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';

await Actor.init();
const input = (await Actor.getInput()) ?? {};

// The Federal Register publishes its own official public API (GSA/NARA). No API key, no auth.
const API = 'https://www.federalregister.gov/api/v1';

// Hard limits, verified live (cycle 112):
//   per_page=1000 is accepted and returns 1000 rows; `count` is clamped at 10000 even when the
//   real match set is larger, so it must never be used as a total.
//   page=11 at per_page=1000 -> HTTP 400. Offset paging dies at 10000 rows, exactly like
//   openFDA's skip cap. `search_after_cursor` (which the API's own next_page_url carries) walks
//   straight past it — 14000 rows pulled in one uninterrupted walk during verification.
const MAX_PER_PAGE = 1000;

const TYPES = { RULE: 'Rule', PRORULE: 'Proposed Rule', NOTICE: 'Notice', PRESDOCU: 'Presidential Document' };

// Requested in one shot; `fields[]` selection is what keeps a 1000-row page small.
const FIELDS = [
    'document_number', 'type', 'subtype', 'title', 'abstract', 'action', 'dates', 'excerpts',
    'publication_date', 'effective_on', 'comments_close_on', 'signing_date', 'significant',
    'agencies', 'docket_ids', 'regulation_id_numbers', 'cfr_references', 'topics',
    'citation', 'start_page', 'end_page', 'page_length', 'president', 'executive_order_number',
    'html_url', 'pdf_url', 'raw_text_url', 'json_url', 'public_inspection_pdf_url',
];

const documentTypes = (input.documentTypes ?? Object.keys(TYPES))
    .map((t) => String(t).toUpperCase().trim())
    .filter((t) => Object.hasOwn(TYPES, t));

const searchQuery = String(input.searchQuery ?? '').trim();
const significantOnly = input.significantOnly === true;
const commentsOpenOnly = input.commentsOpenOnly === true;
const order = ['newest', 'oldest', 'relevance'].includes(input.order) ? input.order : 'newest';
const maxResults = Math.min(Math.max(Number(input.maxResults ?? 100), 1), 50000);

const today = new Date();
const isoDay = (d) => d.toISOString().slice(0, 10);
const normDate = (v, fallback) => {
    const digits = String(v ?? '').replace(/[^0-9]/g, '');
    if (digits.length !== 8) return fallback;
    return `${digits.slice(0, 4)}-${digits.slice(4, 6)}-${digits.slice(6, 8)}`;
};
// Unlike the TED/USAspending archives, this feed is read as "what has just been published",
// so the default window is the last 90 days rather than all history. The archive reaches back
// to 1994-01-03 (verified with order=oldest) if the user widens it.
const dateFrom = normDate(input.publicationDateFrom, isoDay(new Date(today.getTime() - 90 * 86400_000)));
const dateTo = normDate(input.publicationDateTo, isoDay(today));

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function apiGet(path, params) {
    // doseq-style encoding: `conditions[type][]` must be percent-encoded or some clients
    // silently drop the brackets and the filter is ignored rather than rejected.
    const qs = new URLSearchParams();
    for (const [k, v] of Object.entries(params)) {
        if (Array.isArray(v)) for (const one of v) qs.append(k, String(one));
        else if (v != null && v !== '') qs.append(k, String(v));
    }
    const url = `${API}${path}?${qs.toString()}`;
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
            log.warning(`Federal Register API returned ${resp.statusCode}; retrying in ${waitS}s (${attempt}/4).`);
            await sleep(waitS * 1000);
            continue;
        }
        let parsed = null;
        try { parsed = JSON.parse(resp.body); } catch { /* handled below */ }
        if (resp.statusCode !== 200) {
            // An unknown agency slug is a 400, not an empty result set — verified live.
            const detail = parsed?.errors ? JSON.stringify(parsed.errors) : String(resp.body).slice(0, 300);
            log.warning(`Federal Register API ${resp.statusCode}: ${detail}`);
            return null;
        }
        if (!parsed) {
            log.warning(`Federal Register returned a non-JSON body: ${String(resp.body).slice(0, 200)}`);
            return null;
        }
        return parsed;
    }
    log.warning('Federal Register API kept erroring after 4 attempts; stopping early.');
    return null;
}

// The agency filter takes slugs. A wrong slug 400s the whole query, so user input is resolved
// against the official agency list first (472 agencies) by slug, name or short name.
async function resolveAgencies(wanted) {
    if (!wanted.length) return { slugs: [], unknown: [] };
    const list = await apiGet('/agencies.json', {});
    if (!Array.isArray(list)) {
        log.warning('Could not load the agency list; passing agency values through unvalidated.');
        return { slugs: wanted.map((a) => a.toLowerCase().replace(/[^a-z0-9]+/g, '-')), unknown: [] };
    }
    const index = new Map();
    for (const a of list) {
        for (const key of [a.slug, a.name, a.short_name]) {
            if (key) index.set(String(key).toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim(), a.slug);
        }
    }
    const slugs = [];
    const unknown = [];
    for (const raw of wanted) {
        const key = String(raw).toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
        const hit = index.get(key);
        if (hit) slugs.push(hit);
        else unknown.push(raw);
    }
    return { slugs: Array.from(new Set(slugs)), unknown };
}

const { slugs: agencySlugs, unknown: unknownAgencies } = await resolveAgencies(
    (input.agencies ?? []).map((a) => String(a).trim()).filter(Boolean),
);
if (unknownAgencies.length) {
    log.warning(
        `Ignoring ${unknownAgencies.length} unrecognised agency value(s): ${unknownAgencies.join(', ')}. `
        + `Use the slug from a federalregister.gov/agencies/<slug> URL, or the agency's full name. `
        + 'Filtering by a parent agency (e.g. "homeland-security-department") automatically includes '
        + 'its sub-agencies (Coast Guard, FEMA, CBP, TSA, USCIS) — verified live.',
    );
}

function baseParams() {
    const p = {
        'fields[]': FIELDS,
        per_page: Math.min(MAX_PER_PAGE, Math.max(20, maxResults)),
        order,
        'conditions[publication_date][gte]': dateFrom,
        'conditions[publication_date][lte]': dateTo,
    };
    if (documentTypes.length && documentTypes.length < Object.keys(TYPES).length) {
        p['conditions[type][]'] = documentTypes;
    }
    if (agencySlugs.length) p['conditions[agencies][]'] = agencySlugs;
    if (searchQuery) p['conditions[term]'] = searchQuery;
    if (significantOnly) p['conditions[significant]'] = 1;
    // "Comment period still open" = a closing date on or after today.
    if (commentsOpenOnly) p['conditions[comment_date][gte]'] = isoDay(today);
    return p;
}

const listOf = (v) => (Array.isArray(v) ? v.filter(Boolean) : []);
const cfrString = (r) => {
    const t = r?.title ?? '';
    const part = r?.part ?? r?.chapter ?? '';
    return [t, 'CFR', part].filter((x) => x !== '' && x != null).join(' ').trim() || null;
};

function normalize(d) {
    const agencies = listOf(d.agencies);
    return {
        documentNumber: d.document_number ?? null,
        type: d.type ?? null,
        subtype: d.subtype ?? null,
        title: d.title ?? null,
        abstract: d.abstract ?? null,
        action: d.action ?? null,

        publicationDate: d.publication_date ?? null,
        effectiveOn: d.effective_on ?? null,
        // Populated on 92% of proposed rules, 36% of notices, 9% of final rules (live sample of
        // 200 per type) — the field a regulatory-affairs buyer actually acts on.
        commentsCloseOn: d.comments_close_on ?? null,
        signingDate: d.signing_date ?? null,
        datesText: d.dates ?? null,

        // `significant` is only ever set on rules and proposed rules (43%/40% of a 200-row
        // sample); it is null on every notice and presidential document, by design.
        significant: typeof d.significant === 'boolean' ? d.significant : null,

        // Flattened the same way TED/UK-FTS flatten buyer names, and split parent vs. sub-agency
        // because one document routinely lists a department plus the bureau that wrote it.
        agencyNames: agencies.map((a) => a.name ?? a.raw_name).filter(Boolean),
        agencySlugs: agencies.map((a) => a.slug).filter(Boolean),
        parentAgencyNames: agencies.filter((a) => a.parent_id == null).map((a) => a.name ?? a.raw_name).filter(Boolean),

        docketIds: listOf(d.docket_ids),
        // RIN — joins a document to its entry in reginfo.gov's Unified Agenda.
        regulationIdNumbers: listOf(d.regulation_id_numbers),
        cfrReferences: listOf(d.cfr_references).map(cfrString).filter(Boolean),
        topics: listOf(d.topics),

        citation: d.citation ?? null,
        startPage: d.start_page ?? null,
        endPage: d.end_page ?? null,
        pageLength: d.page_length ?? null,
        president: d.president?.name ?? null,
        executiveOrderNumber: d.executive_order_number ?? null,

        excerpt: d.excerpts ?? null,
        url: d.html_url ?? null,
        pdfUrl: d.pdf_url ?? null,
        // Free full text of the document body — no extra request charged by us, the URL is public.
        fullTextUrl: d.raw_text_url ?? null,
        jsonUrl: d.json_url ?? null,
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
    `Federal Register: types=[${documentTypes.join(',') || 'all'}] publication_date ${dateFrom}..${dateTo} `
    + `order=${order} maxResults=${maxResults}`
    + (agencySlugs.length ? ` agencies=[${agencySlugs.join(',')}]` : '')
    + (searchQuery ? ` searchQuery="${searchQuery}"` : '')
    + (significantOnly ? ' significantOnly' : '')
    + (commentsOpenOnly ? ' commentsOpenOnly' : ''),
);

const seen = new Set();
let cursor = null;
let scanned = 0;
let keepGoing = true;
let pages = 0;

while (keepGoing && pushed < maxResults) {
    const params = baseParams();
    if (cursor) params.search_after_cursor = cursor;
    const page = await apiGet('/documents.json', params);
    if (!page) break;
    const results = listOf(page.results);
    if (!results.length) break;
    pages += 1;

    for (const row of results) {
        scanned += 1;
        const key = row.document_number ?? `${row.citation}:${row.title}`;
        if (seen.has(key)) continue;
        seen.add(key);
        keepGoing = await pushResult(normalize(row));
        if (!keepGoing || pushed >= maxResults) break;
    }

    // The cursor lives inside next_page_url; reading it back is cheaper and safer than
    // reinventing offset paging, which 400s past row 10000.
    const next = page.next_page_url;
    if (!next) break;
    cursor = new URL(next).searchParams.get('search_after_cursor');
    if (!cursor) break;
}

if (pushed === 0) {
    log.warning(
        `No documents matched. Scanned ${scanned} rows. Most common causes, in order: `
        + '(1) the filters are ANDed — a searchQuery plus an agency plus significantOnly over a short '
        + 'publication-date window often has zero real matches; drop one filter and retry. '
        + '(2) publicationDateFrom/publicationDateTo default to the last 90 days; widen them (the '
        + 'archive goes back to 1994-01-03). '
        + '(3) significantOnly only ever matches rules and proposed rules — combining it with '
        + 'documentTypes=["NOTICE"] or ["PRESDOCU"] always returns nothing. '
        + '(4) an agency value that was not recognised is dropped with a warning above, not guessed at.',
    );
}

log.info(`Done. Pushed ${pushed} documents over ${pages} page(s) (scanned ${scanned} rows).`);
await Actor.exit();
