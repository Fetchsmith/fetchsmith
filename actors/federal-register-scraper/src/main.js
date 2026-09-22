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

// The Public Inspection desk is a genuinely different endpoint, not a filter: documents that
// agencies have FILED but that have not been published yet (they publish on the next business
// day or two). It is the only place the text exists before it is law-of-record, which is the
// whole reason a regulatory-affairs buyer watches it. Verified live (cycle 412): its rows carry
// a different, smaller field set than /documents.json, and it rejects an unknown `fields[]`
// entry with a clean HTTP 400 rather than silently ignoring it.
const PI_FIELDS = [
    'document_number', 'type', 'title', 'excerpts', 'filed_at', 'filing_type', 'publication_date',
    'agencies', 'docket_numbers', 'editorial_note', 'num_pages', 'last_public_inspection_issue',
    'html_url', 'pdf_url', 'raw_text_url',
];
const dataset = input.dataset === 'publicInspection' ? 'publicInspection' : 'published';
const publicInspection = dataset === 'publicInspection';

const documentTypes = (input.documentTypes ?? Object.keys(TYPES))
    .map((t) => String(t).toUpperCase().trim())
    .filter((t) => Object.hasOwn(TYPES, t));

const searchQuery = String(input.searchQuery ?? '').trim();
const significantOnly = input.significantOnly === true;
const commentsOpenOnly = input.commentsOpenOnly === true;
const order = ['newest', 'oldest', 'relevance'].includes(input.order) ? input.order : 'newest';
const maxResults = Math.min(Math.max(Number(input.maxResults ?? 100), 1), 50000);
const watchLabel = String(input.watchLabel ?? '').trim();

// Convenience completion ping (same shape as grants-gov-scraper, cycle 421). A bad value is
// warned and ignored rather than thrown -- this is a notification nicety, not core function.
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

// `state`, when passed, records the terminal cause of a `null` return (h250 class: a permanent
// upstream failure otherwise looks identical to a genuinely exhausted index — both just stop the
// walk with no page). See `runState`/`markIncomplete` near the bottom of the file.
async function apiGet(path, params, state = null) {
    // doseq-style encoding: `conditions[type][]` must be percent-encoded or some clients
    // silently drop the brackets and the filter is ignored rather than rejected.
    const qs = new URLSearchParams();
    for (const [k, v] of Object.entries(params)) {
        if (Array.isArray(v)) for (const one of v) qs.append(k, String(one));
        else if (v != null && v !== '') qs.append(k, String(v));
    }
    const url = `${API}${path}?${qs.toString()}`;
    for (let attempt = 1; attempt <= 4; attempt += 1) {
        let resp;
        try {
            resp = await gotScraping({
                url,
                responseType: 'text',
                throwHttpErrors: false,
                retry: { limit: 0 },
                timeout: { request: 60000 },
                headers: { accept: 'application/json' },
            });
        } catch (err) {
            // A network-level failure (timeout, ECONNRESET, DNS) throws instead of resolving with
            // a status code — without this catch it crashes the whole run instead of retrying like
            // a 429/5xx does, even though the same backoff is exactly as valid here.
            const waitS = attempt * 10;
            log.warning(`Federal Register API request failed (${err.message}); retrying in ${waitS}s (${attempt}/4).`);
            if (state) state.lastError = `request failed: ${err.message}`;
            await sleep(waitS * 1000);
            continue;
        }
        if (resp.statusCode === 429 || resp.statusCode >= 500) {
            const waitS = Number(resp.headers['retry-after']) || attempt * 10;
            log.warning(`Federal Register API returned ${resp.statusCode}; retrying in ${waitS}s (${attempt}/4).`);
            if (state) state.lastError = `HTTP ${resp.statusCode}`;
            await sleep(waitS * 1000);
            continue;
        }
        let parsed = null;
        try { parsed = JSON.parse(resp.body); } catch { /* handled below */ }
        if (resp.statusCode !== 200) {
            // An unknown agency slug is a 400, not an empty result set — verified live.
            const detail = parsed?.errors ? JSON.stringify(parsed.errors) : String(resp.body).slice(0, 300);
            log.warning(`Federal Register API ${resp.statusCode}: ${detail}`);
            if (state) state.lastError = `HTTP ${resp.statusCode}: ${detail.slice(0, 120)}`;
            return null;
        }
        if (!parsed) {
            log.warning(`Federal Register returned a non-JSON body: ${String(resp.body).slice(0, 200)}`);
            if (state) state.lastError = `non-JSON body: ${String(resp.body).slice(0, 120).replace(/\s+/g, ' ').trim()}`;
            return null;
        }
        return parsed;
    }
    log.warning('Federal Register API kept erroring after 4 attempts; stopping early.');
    if (state) state.lastError = state.lastError ? `${state.lastError} (after 4 retries)` : 'unreachable after 4 retries';
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

// Filters that exist on /documents.json but have no counterpart on the Public Inspection desk.
// They are dropped with a loud warning rather than passed through: verified live (cycle 412),
// `conditions[available_on]` does not narrow a Public Inspection query, it REPLACES it — asking
// for available_on=2026-09-17 plus agencies=environmental-protection-agency returned all 116
// rows of that issue, not the 1 EPA row. A silently-ignored filter is the worst outcome here
// (the buyer pays per result for rows they filtered out), so say so instead.
function piParams() {
    const p = {
        'fields[]': PI_FIELDS,
        per_page: Math.min(MAX_PER_PAGE, Math.max(20, maxResults)),
    };
    if (documentTypes.length && documentTypes.length < Object.keys(TYPES).length) {
        p['conditions[type][]'] = documentTypes;
    }
    if (agencySlugs.length) p['conditions[agencies][]'] = agencySlugs;
    if (searchQuery) p['conditions[term]'] = searchQuery;
    return p;
}

function baseParams() {
    if (publicInspection) return piParams();
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
let baselineTruncated = 0; // ids dropped by WATCH_KEEP this run -- they come back as "new" and get charged
let baselineTruncatedTotal = 0; // same, cumulative over the life of this label

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
    // In the fingerprint because a Public Inspection row and its later published row share the
    // SAME document_number. Without this, watching the desk under a label and then switching that
    // label to dataset="published" would silently suppress every document as already-delivered —
    // exactly the publication the buyer switched modes to catch.
    dataset,
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
    const all = Array.from(watchSeen);
    const ids = all.slice(-WATCH_KEEP);
    // An id past the record cap is not forgotten harmlessly: the next run does not find it in the
    // baseline, so it is delivered and CHARGED again even though the buyer already paid for it.
    // The dropped end is oldest-FIRST-SEEN (re-seeing an id is a Set no-op and doesn't move it).
    // Distinct from SEED_CAP/seedCapped above, which bounds one baseline WALK, not this record.
    baselineTruncated = all.length - ids.length;
    baselineTruncatedTotal = (watchRecord.truncatedTotal ?? 0) + baselineTruncated;
    if (baselineTruncated > 0) {
        log.warning(
            `The baseline for "${watchLabel}" exceeded the ${WATCH_KEEP}-entry record cap; the ${baselineTruncated} `
            + 'oldest document id(s) were dropped and will be returned and CHARGED as new on a future run '
            + `(${baselineTruncatedTotal} dropped over the life of this label). Narrow the query (an agency, a `
            + 'document type, a shorter publication-date window) or split it across several labels so the baseline stays under the cap.',
        );
    }
    await watchStore.setValue(watchKey, {
        ...watchRecord,
        label: watchLabel,
        fingerprint: watchRecord.fingerprint,
        criteria: watchCriteria,
        lastRunAt: new Date().toISOString(),
        lastRunStatus: status,
        runCount: (watchRecord.runCount ?? 0) + 1,
        seenCount: ids.length,
        truncatedLastRun: baselineTruncated,
        truncatedTotal: baselineTruncatedTotal,
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
async function seedBaseline(state) {
    // per_page is pinned to the maximum, not to maxResults: the baseline has to cover the
    // WHOLE match set, not one page of it. A baseline that stops early would report every
    // document past the stopping point as "new" on the first incremental run.
    const params = { ...baseParams(), 'fields[]': ['document_number'], per_page: MAX_PER_PAGE };
    let pagesSeeded = 0;
    while (watchSeen.size < SEED_CAP) {
        const page = await apiGet(publicInspection ? '/public-inspection-documents.json' : '/documents.json', params, state);
        // A permanent upstream failure mid-seed must not read the same as "the archive has no
        // more matches" — the baseline would be saved as complete, and every document past the
        // failure point would be charged as "new" on the very first incremental run.
        if (!page) { state.failed = true; break; }
        const results = listOf(page.results);
        if (!results.length) { state.exhausted = true; break; }
        pagesSeeded += 1;
        for (const row of results) {
            if (row.document_number) watchSeen.add(String(row.document_number));
        }
        if (!applyNext(params, page.next_page_url)) { state.exhausted = true; break; }
    }
    if (watchSeen.size >= SEED_CAP) state.seedCapped = true;
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

// A "Correction"/"Extension of comment period"/"Postponement of effective date" document never
// mutates the original document's own record (verified live, cycle 351: refetching
// document_number 2026-03798 shows the same effective_on/comments_close_on it was published
// with — Federal Register treats a published document as an immutable historical record). The
// amendment instead ships as a brand-new document whose own `dates`/`action` text cites the
// original by its Federal Register citation, e.g. "extended to March 2, 2026" for "the December
// 23, 2025 proposed rule (90 FR 60432)". So a snapshot-diff watchChanges (the shape used on
// grants-gov/fda-recall/us-federal-awards) cannot work here — there is nothing on the original
// row to diff. What IS extractable today, cheaply, from fields already fetched: which earlier
// citations a new document references, so a buyer can link a correction/extension back to the
// original without re-reading the free-text `dates` field by hand.
const CITATION_RE = /\b(\d{2,3})\s+FR\s+(\d{1,6})\b/g;
function extractCitations(...texts) {
    const found = new Set();
    for (const t of texts) {
        if (!t) continue;
        for (const m of String(t).matchAll(CITATION_RE)) found.add(`${m[1]} FR ${m[2]}`);
    }
    return Array.from(found);
}

// The Federal Register API hands back GPO typesetting markup inside otherwise-plain free text —
// the README sells `abstract`/`title`/`action`/`datesText` as prose, so shipping it raw is a data
// defect (same class as grants-gov's undecoded entities, cycle 556). Measured live over 1000 docs
// across 5 agencies (cycle 560): 88 tags, ALL of them in `abstract`, and only two kinds —
// `<INF>`/`</INF>` (86, subscript) and `<bullet>` (2). No entities appeared in that sample.
// `<INF>` sits INSIDE a word ("NO<INF>X</INF>" = NOx), so grants-gov's blanket tag -> space rule
// would corrupt it into "NO X". Inline formatting tags therefore drop to the empty string and
// everything else drops to a space; `<bullet>` is block-level, so a space is right for it.
const INLINE_TAGS = new Set(['inf', 'sup', 'sub', 'e', 'i', 'b', 'em', 'strong', 'span']);
const ENTITIES = {
    amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ', ndash: '–', mdash: '—',
    lsquo: '‘', rsquo: '’', ldquo: '“', rdquo: '”', hellip: '…',
    bull: '•', deg: '°', plusmn: '±', micro: 'µ', times: '×',
    frac12: '½', reg: '®', copy: '©', trade: '™', sect: '§',
};
const decodeEntities = (s) => String(s).replace(/&(#x[0-9a-fA-F]+|#\d+|[a-zA-Z][a-zA-Z0-9]{1,9});/g, (m, e) => {
    if (e[0] === '#') {
        const cp = e[1] === 'x' || e[1] === 'X' ? parseInt(e.slice(2), 16) : parseInt(e.slice(1), 10);
        return Number.isFinite(cp) && cp > 0 && cp <= 0x10ffff ? String.fromCodePoint(cp) : m;
    }
    const key = e.toLowerCase();
    return Object.prototype.hasOwnProperty.call(ENTITIES, key) ? ENTITIES[key] : m; // unknown: verbatim
});
// Plain-text cleanup for one free-text field: drop markup, decode entities, collapse whitespace.
const cleanText = (v) => {
    if (v == null || v === '') return null;
    const stripped = String(v).replace(/<\/?([a-zA-Z][a-zA-Z0-9]*)(?:\s[^<>]*)?\/?>/g,
        (m, tag) => (INLINE_TAGS.has(tag.toLowerCase()) ? '' : ' '));
    return decodeEntities(stripped).replace(/\s+/g, ' ').trim() || null;
};

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
        title: cleanText(d.title),
        abstract: cleanText(d.abstract),
        action: cleanText(d.action),

        publicationDate: d.publication_date ?? null,
        effectiveOn: d.effective_on ?? null,
        // Populated on 92% of proposed rules, 36% of notices, 9% of final rules (live sample of
        // 200 per type) — the field a regulatory-affairs buyer actually acts on.
        commentsCloseOn: d.comments_close_on ?? null,
        signingDate: d.signing_date ?? null,
        datesText: cleanText(d.dates),

        // Non-null only on rules/proposed rules, and even there it's null more often than not:
        // live sample of 200 RULE + 200 PRORULE (2025-01 to 2026-09) measured true/false present
        // on only ~45%/40% of them — a null on a rule is NOT "not significant", most rules are
        // simply never submitted for EO 12866 review. Always null on notices/presidential docs.
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

        // Other Federal Register documents this one's own text cites by "NN FR NNNNN" citation —
        // in practice almost always the earlier document a correction, extension, or postponement
        // amends. Self-citation excluded (a document doesn't reference its own citation, but a
        // reprint/republication occasionally repeats it in `dates`). Empty on the ~90% of
        // documents that don't amend anything.
        referencedCitations: extractCitations(d.dates, d.action).filter((c) => c !== d.citation),

        excerpt: cleanText(d.excerpts),
        url: d.html_url ?? null,
        pdfUrl: d.pdf_url ?? null,
        // Free full text of the document body — no extra request charged by us, the URL is public.
        fullTextUrl: d.raw_text_url ?? null,
        jsonUrl: d.json_url ?? null,

        // Public-Inspection-only facts (dataset="publicInspection"). Declared here as nulls so
        // both modes emit the identical key set and a CSV/Excel export never shifts columns.
        filedAt: null,
        filingType: null,
        lastPublicInspectionIssue: null,
        numPages: null,
        editorialNote: null,
        onPublicInspection: false,
    };
}

// A Public Inspection row is the same document seen one step earlier, so it keeps the same field
// names wherever the same fact exists (documentNumber/type/title/agency*/pdfUrl/fullTextUrl/url),
// and `publicationDate` is the date it is SCHEDULED to publish — in a live check it was tomorrow's
// date on every regular filing. Everything the desk doesn't know yet (effectiveOn,
// commentsCloseOn, citation, page numbers, topics, CFR references, significant) is null rather
// than absent, so a dataset mixing both modes stays one rectangle.
function normalizePI(d) {
    const agencies = listOf(d.agencies);
    return {
        ...normalize({}),
        documentNumber: d.document_number ?? null,
        type: d.type ?? null,
        title: cleanText(d.title),
        publicationDate: d.publication_date ?? null,
        agencyNames: agencies.map((a) => a.name ?? a.raw_name).filter(Boolean),
        agencySlugs: agencies.map((a) => a.slug).filter(Boolean),
        parentAgencyNames: agencies.filter((a) => a.parent_id == null).map((a) => a.name ?? a.raw_name).filter(Boolean),
        docketIds: listOf(d.docket_numbers),
        excerpt: cleanText(d.excerpts),
        url: d.html_url ?? null,
        pdfUrl: d.pdf_url ?? null,
        fullTextUrl: d.raw_text_url ?? null,

        // Public-Inspection-only facts, null on every /documents.json row.
        filedAt: d.filed_at ?? null,
        // "regular" = filed on the normal schedule; "special" = filed out of band because the
        // agency asked for early public availability (5 of 116 in a live sample).
        filingType: d.filing_type ?? null,
        lastPublicInspectionIssue: d.last_public_inspection_issue ?? null,
        numPages: d.num_pages ?? null,
        // Free-text note from the Office of the Federal Register, e.g. a withdrawal request
        // received after the document was placed on public inspection. Rare but decisive.
        editorialNote: d.editorial_note ?? null,
        onPublicInspection: true,
    };
}

let pushed = 0;
let chargeLimitReached = false;
const isPPE = Actor.getChargingManager().getPricingInfo().isPayPerEvent;
async function pushResult(item) {
    if (isPPE) {
        const r = await Actor.charge({ eventName: 'result', count: 1 });
        if (r.chargedCount === 0) return false;
        await Actor.pushData(item); pushed += 1;
        if (r.eventChargeLimitReached) chargeLimitReached = true;
        return !r.eventChargeLimitReached && pushed < maxResults;
    }
    await Actor.pushData(item); pushed += 1;
    return pushed < maxResults;
}

if (publicInspection) {
    const ignored = [
        input.publicationDateFrom ? 'publicationDateFrom' : null,
        input.publicationDateTo ? 'publicationDateTo' : null,
        significantOnly ? 'significantOnly' : null,
        commentsOpenOnly ? 'commentsOpenOnly' : null,
        cfrTitle != null ? 'cfrTitle' : null,
        cfrPart ? 'cfrPart' : null,
        input.order && input.order !== 'newest' ? 'order' : null,
    ].filter(Boolean);
    if (ignored.length) {
        log.warning(
            `dataset="publicInspection" ignores ${ignored.join(', ')} — the Public Inspection desk holds only `
            + 'the documents currently on file (today\'s issue plus anything filed early), so there is no date '
            + 'range, no significance flag, no comment-close date, no CFR index and no sort order to apply. '
            + 'It supports documentTypes, agencies, searchQuery and maxResults only. Switch to '
            + 'dataset="published" to use the filters above.',
        );
    }
    log.info(
        `Federal Register PUBLIC INSPECTION desk (filed, not yet published): `
        + `types=[${documentTypes.join(',') || 'all'}] maxResults=${maxResults}`
        + (agencySlugs.length ? ` agencies=[${agencySlugs.join(',')}]` : '')
        + (searchQuery ? ` searchQuery="${searchQuery}"` : ''),
    );
} else {
    log.info(
        `Federal Register: types=[${documentTypes.join(',') || 'all'}] publication_date ${dateFrom}..${dateTo} `
        + `order=${order} maxResults=${maxResults}`
        + (agencySlugs.length ? ` agencies=[${agencySlugs.join(',')}]` : '')
        + (searchQuery ? ` searchQuery="${searchQuery}"` : '')
        + (significantOnly ? ' significantOnly' : '')
        + (commentsOpenOnly ? ' commentsOpenOnly' : '')
        + (cfrTitle != null ? ` cfr=${cfrTitle}${cfrPart ? `/${cfrPart}` : ''}` : ''),
    );
}

const seen = new Set();
const walkParams = baseParams();
let scanned = 0;
let keepGoing = true;
let pages = 0;
let skippedSeen = 0;
let beforePush = 0;

// h250 class (same shape closed on court-records-scraper, uk-find-a-tender-scraper and
// sam-gov-opportunities-scraper): `apiGet` returning null after 4 retries and a next_page_url
// simply running out both end the walk the same way, but only one of them means the buyer got
// everything. `failed`/`exhausted` tell those two apart for RUN_SUMMARY below.
const runState = { failed: false, exhausted: false, seedCapped: false };

if (seeding) await seedBaseline(runState);

while (!seeding && keepGoing && pushed < maxResults) {
    const page = await apiGet(publicInspection ? '/public-inspection-documents.json' : '/documents.json', walkParams, runState);
    if (!page) { runState.failed = true; break; }
    const results = listOf(page.results);
    if (!results.length) { runState.exhausted = true; break; }
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
        keepGoing = await pushResult(publicInspection ? normalizePI(row) : normalize(row));
        // Recorded as delivered only after the charge actually succeeded — anything dropped by
        // maxResults or a charge limit stays "new" for the next run.
        if (watchMode && row.document_number && pushed > beforePush) watchSeen.add(String(row.document_number));
        beforePush = pushed;
        if (!keepGoing || pushed >= maxResults) break;
    }

    // Following the API's own next_page_url is cheaper and safer than reinventing offset
    // paging, which 400s past row 10000. No next page really does mean the walk is exhausted,
    // even if maxResults/a charge limit was also hit on this same last page.
    if (!applyNext(walkParams, page.next_page_url)) { runState.exhausted = true; break; }
}

// Empty unless WATCH_KEEP actually dropped something, so it can never add noise to a healthy run.
function truncationNote() {
    if (baselineTruncated <= 0) return '';
    return ` WARNING: the baseline hit its ${WATCH_KEEP}-entry cap and ${baselineTruncated} oldest id(s) were`
        + ' dropped -- those will be delivered and charged again as "new". Narrow the query or split it across labels.';
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
        await Actor.setStatusMessage(
            `Baseline run for watch label "${watchLabel}": ${watchSeen.size} existing document(s) recorded, 0 charged. Run again later to get only what's new.`
            + truncationNote(),
        );
    } else {
        log.info(
            `Watch label "${watchLabel}": ${pushed} new document(s) since the last run `
            + `(${skippedSeen} already-delivered row(s) skipped, uncharged); baseline now holds ${watchSeen.size}.`,
        );
        if (pushed > 0 && baselineTruncated > 0) {
            // A run that delivered rows would otherwise leave the default status message in
            // place and the truncation would only be visible in the log.
            await Actor.setStatusMessage(`Watch label "${watchLabel}": ${pushed} document(s) delivered.` + truncationNote());
        }
    }
}

if (pushed === 0 && watchMode && !seeding) {
    log.warning(
        `Nothing new for watch label "${watchLabel}" since its last run — all ${skippedSeen} matching document(s) `
        + 'had already been delivered. That is the expected result most of the time; you were charged for nothing.',
    );
    await Actor.setStatusMessage(
        `Nothing new for watch label "${watchLabel}" since its last run -- every matching document had already been delivered. That is the expected result most of the time; you were charged for nothing.`
        + truncationNote(),
    );
} else if (pushed === 0 && !seeding && publicInspection) {
    log.warning(
        `No documents are on the Public Inspection desk for these filters. Scanned ${scanned} rows. The desk is `
        + 'small by design — it holds one issue at a time (about 100-150 documents, mostly notices), so a narrow '
        + 'agency or searchQuery legitimately returns nothing on most days. It is also empty on weekends and '
        + 'federal holidays. Run it on a daily schedule with watchLabel rather than expecting a hit on any one run, '
        + 'or switch to dataset="published" to search the full archive back to 1994.',
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

// ---------------------------------------------------------------------------
// RUN_SUMMARY: this run's completeness, in a form a pipeline can read without a webhook
// (GET /v2/actor-runs/<runId>/key-value-store/records/RUN_SUMMARY). `complete` is kept out of
// the run STATUS on purpose — a run can SUCCEED and still be short, and that pair is exactly
// what this record exists for. No `declaredMatches` field: the API's own `count` is clamped at
// 10000 regardless of the true match size (see the MAX_PER_PAGE comment above), so it would
// misreport a large archive as "10000 matches" rather than telling the truth, which is "unknown".
let complete = true;
let incompleteReason = null;
let incompleteDetail = null;
function markIncomplete(reason, detail = null) {
    if (!complete) return;
    complete = false;
    incompleteReason = reason;
    incompleteDetail = detail;
}
if (seeding) {
    if (runState.failed) {
        markIncomplete('source-error', `baseline seed API error: ${runState.lastError ?? 'unknown'}`);
    } else if (runState.seedCapped) {
        markIncomplete(
            'seed-cap',
            `the baseline stopped at the ${SEED_CAP.toLocaleString('en-US')}-document cap; narrow the query `
            + '(an agency, a document type, a shorter publication-date window) or the rest will be charged as new '
            + 'on the first incremental run',
        );
    }
} else {
    if (runState.failed) {
        markIncomplete('source-error', `API error: ${runState.lastError ?? 'unknown'}`);
    } else if (chargeLimitReached) {
        markIncomplete('charge-limit', "the run's pay-per-event charge limit was reached before the walk reached the end of the result set");
    } else if (!runState.exhausted && pushed >= maxResults) {
        markIncomplete('max-results', `maxResults=${maxResults} was reached before the walk reached the end of the result set`);
    } else if (!runState.exhausted) {
        markIncomplete('stopped-early', 'the walk ended with no recorded reason');
    }
}

const runSummary = {
    mode: watchMode ? (seeding ? 'watch-seed' : 'watch-incremental') : (publicInspection ? 'public-inspection' : 'search'),
    scanned,
    delivered: pushed,
    pages,
    exhausted: runState.exhausted,
    failed: runState.failed,
    lastApiError: runState.lastError ?? null,
    complete,
    incompleteReason,
    incompleteDetail,
    maxResults,
    chargeLimitReached,
    watchLabel: watchMode ? watchLabel : null,
    watchSeeding: watchMode ? seeding : null,
    baselineSize: watchMode ? watchSeen.size : null,
    // seedCapped: this SEED walk stopped at the SEED_CAP document limit (a one-time baseline
    // depth cap). baselineTruncated/baselineTruncatedTotal: the SAVED RECORD exceeded WATCH_KEEP
    // and dropped ids -- a different cap, and the one that causes a future re-charge. Was a single
    // misnamed `baselineTruncated: runState.seedCapped` field before cycle 657 (h285 naming
    // collision with us-federal-awards-scraper, which uses the same field name for the real thing).
    seedCapped: watchMode ? runState.seedCapped : null,
    baselineTruncated: watchMode ? baselineTruncated : null,
    baselineTruncatedTotal: watchMode ? baselineTruncatedTotal : null,
    skippedSeen: watchMode && !seeding ? skippedSeen : null,
};
await Actor.setValue('RUN_SUMMARY', runSummary);

// A short run still SUCCEEDS (the rows it did get are real and already charged), so the status
// message is the only place the Apify console itself shows the shortfall. There was no
// setStatusMessage call anywhere in this Actor before cycle 654.
if (!complete) {
    await Actor.setStatusMessage(
        seeding
            ? `Baseline INCOMPLETE: ${watchSeen.size.toLocaleString('en-US')} document(s) recorded — ${incompleteReason}`
              + `${incompleteDetail ? ` (${incompleteDetail})` : ''}. Re-seed before scheduling, or the rest will be charged as new. See RUN_SUMMARY.`
            : `Incomplete: ${pushed.toLocaleString('en-US')} document(s) delivered — ${incompleteReason}`
              + `${incompleteDetail ? ` (${incompleteDetail})` : ''}. See RUN_SUMMARY for details.`,
    );
}

// Fires after every row is already pushed and charged, so a slow or failing webhook can never
// affect the result set or the bill -- best-effort only, one attempt, short timeout, failures are
// a warning not a thrown error.
if (webhookUrl) {
    const env = Actor.getEnv();
    const payload = {
        actorRunId: env.actorRunId ?? null,
        defaultDatasetId: env.defaultDatasetId ?? null,
        finishedAt: new Date().toISOString(),
        pushed,
        scanned,
        pages,
        watchLabel: watchMode ? watchLabel : null,
        watchSeeding: watchMode ? seeding : null,
        watchNewCount: watchMode && !seeding ? pushed : null,
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

await Actor.exit();
