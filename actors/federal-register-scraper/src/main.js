import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';
import { createHash } from 'node:crypto';

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
const watchLabel = String(input.watchLabel ?? '').trim();

// Verified live: the API itself validates this pair cleanly (400 "CFR title must be between
// 1 and 50" on a part given without a title, or on a title outside 1-50) — no silent-ignore
// trap here, so we only need to fail loudly on the one combination the API can't express:
// a part with no title at all, which 400s the whole request instead of being ignored.
const cfrTitleRaw = input.cfrTitle;
const cfrTitle = cfrTitleRaw == null || cfrTitleRaw === '' ? null : Number(cfrTitleRaw);
const cfrPart = String(input.cfrPart ?? '').trim() || null;
if (cfrTitle != null && (!Number.isInteger(cfrTitle) || cfrTitle < 1 || cfrTitle > 50)) {
    throw new Error(`cfrTitle must be an integer from 1 to 50 (got ${cfrTitleRaw}).`);
}
if (cfrPart && cfrTitle == null) {
    throw new Error('cfrPart requires cfrTitle to also be set — the CFR API has no title-less part lookup.');
}

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
    if (cfrTitle != null) p['conditions[cfr][title]'] = cfrTitle;
    if (cfrPart) p['conditions[cfr][part]'] = cfrPart;
    return p;
}

// ---------------------------------------------------------------------------
// Watch mode: "only what is new since my last run", per saved query.
//
// The baseline is the buyer's own — the document_numbers this label has already delivered —
// kept in a NAMED key-value store so it survives across runs. The default KV store is
// per-run and would reset the baseline every time, i.e. re-charge the whole result set on
// every scheduled run.
const WATCH_STORE = 'fetchsmith-fedreg-watch';
const SEED_CAP = 20000; // bound a seed walk; cursor paging itself has no wall
const WATCH_KEEP = 60000; // bound the record size; oldest ids fall off first

// Apify KV keys allow [a-zA-Z0-9!-_.'()] only, so the label is sanitised rather than trusted.
// The criteria fingerprint is part of the key on purpose: if the buyer edits a filter, that is
// a different question and gets its own baseline, instead of dumping every document the old
// narrower filter happened to exclude as if it were brand new.
//
// The publication-date window is in the fingerprint ONLY when the buyer set it explicitly.
// Its default is a rolling "last 90 days", which changes every single day — fingerprinting the
// resolved value would give a scheduled watch a brand-new baseline on every run, i.e. seed
// forever and never deliver anything.
function watchKeyFor(label, criteria) {
    const safe = label.toLowerCase().replace(/[^a-z0-9_.-]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 40) || 'default';
    const fp = createHash('sha1').update(JSON.stringify(criteria, Object.keys(criteria).sort())).digest('hex').slice(0, 10);
    return { key: `watch-${safe}-${fp}`, fingerprint: fp };
}

const watchCriteria = {
    documentTypes: [...documentTypes].sort(),
    agencies: [...agencySlugs].sort(),
    searchQuery,
    significantOnly,
    commentsOpenOnly,
    cfrTitle,
    cfrPart,
    // explicit-only, see above
    publicationDateFrom: normDate(input.publicationDateFrom, null),
    publicationDateTo: normDate(input.publicationDateTo, null),
};

const watchMode = watchLabel.length > 0;
let watchStore = null;
let watchKey = null;
let watchRecord = null;
let seeding = false;
const watchSeen = new Set(); // document_numbers already delivered under this label+fingerprint

async function saveWatchRecord(status) {
    const ids = Array.from(watchSeen).slice(-WATCH_KEEP);
    await watchStore.setValue(watchKey, {
        ...watchRecord,
        label: watchLabel,
        fingerprint: watchRecord.fingerprint,
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
            + `${watchSeen.size} already-delivered document(s). Only documents NOT in that baseline are returned and charged.`,
        );
    } else {
        watchRecord = { fingerprint, firstSeededAt: new Date().toISOString(), runCount: 0 };
        seeding = true;
        log.info(
            `Watch mode "${watchLabel}" (${key}): FIRST run for this label and filter set, so this is a baseline run. `
            + 'It records which documents already match and returns ZERO results (you are charged nothing). Run it '
            + 'again on the same label and filters — on a schedule, typically — to get only what is new since now.',
        );
    }
}

// Seeding only needs the ids, so it asks for one field instead of 29. Same filters, same
// cursor walk, a fraction of the bytes — and it never normalizes, pushes or charges.
async function seedBaseline() {
    // per_page is pinned to the maximum, not to maxResults: the baseline has to cover the
    // WHOLE match set, not one page of it. A baseline that stops early would report every
    // document past the stopping point as "new" on the first incremental run.
    const params = { ...baseParams(), 'fields[]': ['document_number'], per_page: MAX_PER_PAGE };
    let pagesSeeded = 0;
    while (watchSeen.size < SEED_CAP) {
        const page = await apiGet('/documents.json', params);
        if (!page) break;
        const results = listOf(page.results);
        if (!results.length) break;
        pagesSeeded += 1;
        for (const row of results) {
            if (row.document_number) watchSeen.add(String(row.document_number));
        }
        if (!applyNext(params, page.next_page_url)) break;
    }
    log.info(`Baseline walk: ${watchSeen.size} document id(s) over ${pagesSeeded} id-only page(s).`);
}

// The API hands back next_page_url in TWO different shapes, verified live (cycle 297):
// a `search_after_cursor` link once the walk is big enough to need it, and a plain `page=N`
// link for small result sets. Reading only the cursor silently stops the walk after page 1
// whenever the set is small — harmless for a plain run (per_page is always >= maxResults, so
// one page already satisfies it) but wrong in watch mode, where most rows are skipped as
// already-seen and the walk has to keep going to find the new ones.
function applyNext(params, nextUrl) {
    if (!nextUrl) return false;
    const q = new URL(nextUrl).searchParams;
    const cursor = q.get('search_after_cursor');
    if (cursor) { params.search_after_cursor = cursor; delete params.page; return true; }
    const page = q.get('page');
    if (page) { params.page = page; delete params.search_after_cursor; return true; }
    return false;
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
    + (commentsOpenOnly ? ' commentsOpenOnly' : '')
    + (cfrTitle != null ? ` cfr=${cfrTitle}${cfrPart ? `/${cfrPart}` : ''}` : ''),
);

const seen = new Set();
const walkParams = baseParams();
let scanned = 0;
let keepGoing = true;
let pages = 0;
let skippedSeen = 0;
let beforePush = 0;

if (seeding) await seedBaseline();

while (!seeding && keepGoing && pushed < maxResults) {
    const page = await apiGet('/documents.json', walkParams);
    if (!page) break;
    const results = listOf(page.results);
    if (!results.length) break;
    pages += 1;

    for (const row of results) {
        scanned += 1;
        const key = row.document_number ?? `${row.citation}:${row.title}`;
        if (seen.has(key)) continue;
        seen.add(key);
        // Already delivered under this watch label: dropped before normalize() and before
        // any charge, so a document is never paid for twice.
        if (watchMode && row.document_number && watchSeen.has(String(row.document_number))) {
            skippedSeen += 1;
            continue;
        }
        keepGoing = await pushResult(normalize(row));
        // Recorded as delivered only after the charge actually succeeded — anything dropped by
        // maxResults or a charge limit stays "new" for the next run.
        if (watchMode && row.document_number && pushed > beforePush) watchSeen.add(String(row.document_number));
        beforePush = pushed;
        if (!keepGoing || pushed >= maxResults) break;
    }

    // Following the API's own next_page_url is cheaper and safer than reinventing offset
    // paging, which 400s past row 10000.
    if (!applyNext(walkParams, page.next_page_url)) break;
}

if (watchMode) {
    await saveWatchRecord(seeding ? 'seeded' : 'incremental');
    if (seeding) {
        log.info(
            `Baseline saved for watch label "${watchLabel}": ${watchSeen.size} document(s) recorded as already-seen, `
            + '0 results returned, 0 charged. The next run on this label and these filters returns only new documents.'
            + (watchSeen.size >= SEED_CAP
                ? ` NOTE: the baseline stopped at the ${SEED_CAP}-document cap. Narrow the query (an agency, a `
                + 'document type, a shorter publication-date window) so the whole result set fits, or the first '
                + 'incremental run will report documents past the cap as new.'
                : ''),
        );
    } else {
        log.info(
            `Watch label "${watchLabel}": ${pushed} new document(s) since the last run `
            + `(${skippedSeen} already-delivered row(s) skipped, uncharged); baseline now holds ${watchSeen.size}.`,
        );
    }
}

if (pushed === 0 && watchMode && !seeding) {
    log.warning(
        `Nothing new for watch label "${watchLabel}" since its last run — all ${skippedSeen} matching document(s) `
        + 'had already been delivered. That is the expected result most of the time; you were charged for nothing.',
    );
} else if (pushed === 0 && !seeding) {
    log.warning(
        `No documents matched. Scanned ${scanned} rows. Most common causes, in order: `
        + '(1) the filters are ANDed — a searchQuery plus an agency plus significantOnly over a short '
        + 'publication-date window often has zero real matches; drop one filter and retry. '
        + '(2) publicationDateFrom/publicationDateTo default to the last 90 days; widen them (the '
        + 'archive goes back to 1994-01-03). '
        + '(3) significantOnly only ever matches rules and proposed rules — combining it with '
        + 'documentTypes=["NOTICE"] or ["PRESDOCU"] always returns nothing. '
        + '(4) an agency value that was not recognised is dropped with a warning above, not guessed at. '
        + '(5) cfrTitle/cfrPart is an AND with every other filter — a narrow CFR part combined with '
        + 'a short date window or a significantOnly flag often has zero real matches.',
    );
}

log.info(`Done. Pushed ${pushed} documents over ${pages} page(s) (scanned ${scanned} rows).`);
await Actor.exit();
