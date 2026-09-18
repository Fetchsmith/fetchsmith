import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';
import { createHash } from 'node:crypto';

await Actor.init();
const input = (await Actor.getInput()) ?? {};

// CourtListener (Free Law Project) publishes a public REST API. The *search index* endpoint
// used here needs NO API token, NO registration and NO cookies — verified live from a bare
// curl on cycles 391 and 392. Only the /dockets/ and /opinions/ *detail* endpoints are
// auth-gated (401), which is what an earlier cycle mistook for "the whole API needs a key".
const BASE = 'https://www.courtlistener.com';
const SEARCH = `${BASE}/api/rest/v4/search/`;

// The search index returns ~20 rows per page and pages with an opaque `cursor=` token carried
// on the response's own `next` URL. There is no per_page knob that survives, and no offset
// paging at all, so the walk must follow `next` verbatim rather than rebuild the query.
const TYPE_FOR = { opinions: 'o', dockets: 'r' };

const recordTypeRaw = String(input.recordType ?? 'both').toLowerCase().trim();
let recordTypes = recordTypeRaw === 'both'
    ? ['opinions', 'dockets']
    : (Object.hasOwn(TYPE_FOR, recordTypeRaw) ? [recordTypeRaw] : ['opinions', 'dockets']);
if (!Object.hasOwn(TYPE_FOR, recordTypeRaw) && recordTypeRaw !== 'both') {
    log.warning(`Unknown recordType "${input.recordType}"; falling back to "both".`);
}

let query = String(input.query ?? '').trim();
const maxResults = Math.min(Math.max(Number(input.maxResults ?? 100), 1), 20000);
const watchLabel = String(input.watchLabel ?? '').trim();
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

// CourtListener's opinion index defaults to Published-only when no `stat_*` param is sent —
// verified live cycle 423: a 2024+ "climate" query returned 545 opinions with no stat param
// (identical to `stat_Published=on` alone), 191 with `stat_Unpublished=on` alone, and the
// true total 736 only with both set. So the API's silent default drops ~26% of real matches
// on that query, with nothing in a normal run's output to reveal it — a competitor
// (automation-lab/court-records-scraper) exposes this as a "Status" filter; we already emit
// the underlying `status` field on every opinion row (line below, `normalizeOpinion`) but had
// no way to filter or complete on it. Default "published" reproduces today's exact behavior
// (no existing run's row count changes); "unpublished" and "any" are additive opt-ins.
const OPINION_STAT_PARAM = { published: ['stat_Published'], unpublished: ['stat_Unpublished'], any: ['stat_Published', 'stat_Unpublished'] };
let opinionStatus = String(input.opinionStatus ?? 'published').toLowerCase().trim();
if (!Object.hasOwn(OPINION_STAT_PARAM, opinionStatus)) {
    log.warning(`Unknown opinionStatus "${input.opinionStatus}"; falling back to "published".`);
    opinionStatus = 'published';
}

// CourtListener court IDs are the short slugs in a courtlistener.com/court/<id>/ URL
// ("scotus", "ca9", "cand", "cacb", ...). 400+ exist, so this is free text rather than an
// enum; an unknown id is not an error upstream, it just matches nothing — warned about below.
let courts = (Array.isArray(input.courts) ? input.courts : String(input.courts ?? '').split(','))
    .map((c) => String(c).trim().toLowerCase())
    .filter(Boolean);

// Field searches CourtListener's index supports alongside the free-text `q`. These are real
// server-side fields, not full-text — verified live cycle 456 against the anonymous search
// endpoint (a bogus param leaves the result count untouched; each of these changes it):
// party_name "Google LLC" 6,498 vs 2,110,970 baseline on RECAP, atty_name "Smith" 65,978,
// docket_number "1:20-cv-03590" 6, judge "Posner" 8,411 on opinions.
//
// The catch that shapes the whole design below: an index that does not carry a field does NOT
// reject it, it IGNORES it — `type=o&party_name=...` returns 8,313,056 rows, i.e. the entire
// opinion corpus, because the only filter sent was dropped on the floor. Silently billing a
// buyer for a whole corpus is the worst possible failure here, so a filter that one index
// cannot honour narrows the run to the index that can (below), instead of being sent blind.
let partyName = String(input.partyName ?? '').trim();
let attorneyName = String(input.attorneyName ?? '').trim();
let docketNumber = String(input.docketNumber ?? '').trim();
let judge = String(input.judge ?? '').trim();

const normDate = (v) => {
    const digits = String(v ?? '').replace(/[^0-9]/g, '');
    if (digits.length !== 8) return null;
    return `${digits.slice(0, 4)}-${digits.slice(4, 6)}-${digits.slice(6, 8)}`;
};
let filedAfter = normDate(input.filedAfter);
let filedBefore = normDate(input.filedBefore);

// Optional shortcut: paste a CourtListener search (or API) URL and its filters replace the
// ones above. Both URL shapes use the identical param vocabulary — verified live cycle 393:
// the search UI's own <input name="q"|"type"|"court"|"filed_after"|"filed_before"> fields
// post straight to this page's own query string, which is the same one /api/rest/v4/search/
// accepts. Only "type=o" (Opinions) and "type=r" (RECAP) are supported, matching the two
// indexes this Actor covers; CourtListener's other type values (oa/p/d/pa — oral arguments,
// judges, RECAP-dockets-only, parentheticals) are different entity shapes this schema does
// not model, so a URL carrying one of those is a clear warning, not a silent misparse.
const startUrlRaw = String(input.startUrl ?? '').trim();
if (startUrlRaw) {
    let parsedUrl = null;
    try { parsedUrl = new URL(startUrlRaw); } catch { /* parsedUrl stays null */ }
    if (!parsedUrl || !/(^|\.)courtlistener\.com$/.test(parsedUrl.hostname)) {
        throw new Error(`startUrl must be a courtlistener.com search or API URL; got "${startUrlRaw}".`);
    }
    const qp = parsedUrl.searchParams;
    const ignored = [];

    if (qp.has('q')) { query = qp.get('q') ?? ''; } else { ignored.push('query'); }

    const rawType = qp.get('type');
    if (rawType === 'o' || rawType === 'r') {
        recordTypes = rawType === 'o' ? ['opinions'] : ['dockets'];
    } else if (rawType) {
        log.warning(
            `startUrl has type="${rawType}", which this Actor does not support (only Opinions `
            + '"o" and RECAP "r" are). Using the "Record type" field below instead.',
        );
    } else {
        ignored.push('recordType');
    }

    // `court` is submitted as one space-joined value (our own firstUrl() builds it the same
    // way) but the form also allows repeats, so both shapes are collected and flattened.
    const courtValues = qp.getAll('court')
        .flatMap((v) => v.split(/\s+/))
        .map((c) => c.trim().toLowerCase())
        .filter(Boolean);
    if (courtValues.length) { courts = courtValues; } else { ignored.push('courts'); }

    // The advanced-search form posts these under the same names the API reads them under.
    if (qp.has('party_name')) { partyName = (qp.get('party_name') ?? '').trim(); } else { ignored.push('partyName'); }
    if (qp.has('atty_name')) { attorneyName = (qp.get('atty_name') ?? '').trim(); } else { ignored.push('attorneyName'); }
    if (qp.has('docket_number')) { docketNumber = (qp.get('docket_number') ?? '').trim(); } else { ignored.push('docketNumber'); }
    if (qp.has('judge')) { judge = (qp.get('judge') ?? '').trim(); } else { ignored.push('judge'); }

    if (qp.has('filed_after')) { filedAfter = normDate(qp.get('filed_after')); } else { ignored.push('filedAfter'); }
    if (qp.has('filed_before')) { filedBefore = normDate(qp.get('filed_before')); } else { ignored.push('filedBefore'); }

    const wantsPub = qp.get('stat_Published') === 'on';
    const wantsUnpub = qp.get('stat_Unpublished') === 'on';
    if (wantsPub || wantsUnpub) {
        opinionStatus = wantsPub && wantsUnpub ? 'any' : (wantsUnpub ? 'unpublished' : 'published');
    } else {
        ignored.push('opinionStatus');
    }

    log.info(
        `startUrl parsed: party=${partyName || '(none)'} attorney=${attorneyName || '(none)'} `
        + `docketNumber=${docketNumber || '(none)'} judge=${judge || '(none)'}.`,
    );
    log.info(
        `startUrl parsed: query=${JSON.stringify(query)} recordTypes=${JSON.stringify(recordTypes)} `
        + `courts=${JSON.stringify(courts)} filedAfter=${filedAfter ?? '(none)'} filedBefore=${filedBefore ?? '(none)'} `
        + `opinionStatus=${opinionStatus}.`,
    );
    if (ignored.length) {
        log.info(
            `The pasted URL did not mention: ${ignored.join(', ')} — the matching field(s) below were used instead. `
            + 'maxResults and watchLabel always apply regardless of startUrl.',
        );
    }
}

// Narrow the indexes to the ones that can actually honour the field searches that are set —
// see the note above `partyName`: the other index would ignore the filter and return its whole
// corpus, which the buyer would be charged for row by row.
const docketOnlyFilters = [partyName && 'partyName', attorneyName && 'attorneyName'].filter(Boolean);
const opinionOnlyFilters = [judge && 'judge'].filter(Boolean);
if (docketOnlyFilters.length && opinionOnlyFilters.length) {
    throw new Error(
        `Cannot combine ${docketOnlyFilters.join('/')} (RECAP dockets only — the opinion index has no party or `
        + `attorney data) with ${opinionOnlyFilters.join('/')} (opinions only — the docket index has no authoring `
        + 'judge). No single CourtListener index carries both, so this combination can never match anything. '
        + 'Run it as two separate runs, or drop one of the two filters.',
    );
}
if (docketOnlyFilters.length && recordTypes.includes('opinions')) {
    if (recordTypes.length === 1) {
        throw new Error(
            `${docketOnlyFilters.join('/')} searches RECAP dockets, but recordType is "opinions" — CourtListener's `
            + 'opinion index carries no party or attorney data and would silently ignore the filter (returning the '
            + 'entire opinion corpus). Set recordType to "dockets" or "both".',
        );
    }
    recordTypes = recordTypes.filter((t) => t !== 'opinions');
    log.warning(
        `${docketOnlyFilters.join('/')} is set, so this run covers RECAP dockets only. CourtListener's opinion index `
        + 'has no party/attorney data and ignores the filter entirely — searching it anyway would return (and charge '
        + 'for) every opinion matching the remaining filters, so it is skipped.',
    );
}
if (opinionOnlyFilters.length && recordTypes.includes('dockets')) {
    if (recordTypes.length === 1) {
        throw new Error(
            'judge searches the opinion index, but recordType is "dockets" — the RECAP docket index has no authoring-'
            + 'judge field and would silently ignore the filter (returning the entire docket corpus). Set recordType '
            + 'to "opinions" or "both".',
        );
    }
    recordTypes = recordTypes.filter((t) => t !== 'dockets');
    log.warning(
        'judge is set, so this run covers opinions only. The RECAP docket index has no authoring-judge field and '
        + 'ignores the filter entirely — searching it anyway would return (and charge for) every docket matching the '
        + 'remaining filters, so it is skipped.',
    );
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// No X-RateLimit-* headers are exposed to anonymous callers, so the real anonymous ceiling is
// unknown. A fixed inter-page delay keeps a long walk well under any plausible limit — the same
// caution applied to every other public API in this fleet.
const PAGE_DELAY_MS = 1200;

async function apiGet(url) {
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
            log.warning(`CourtListener request failed (${err.message}); retrying in ${waitS}s (${attempt}/4).`);
            await sleep(waitS * 1000);
            continue;
        }
        if (resp.statusCode === 429 || resp.statusCode >= 500) {
            const waitS = Number(resp.headers['retry-after']) || attempt * 10;
            log.warning(`CourtListener returned ${resp.statusCode}; retrying in ${waitS}s (${attempt}/4).`);
            await sleep(waitS * 1000);
            continue;
        }
        let parsed = null;
        try { parsed = JSON.parse(resp.body); } catch { /* handled below */ }
        if (resp.statusCode !== 200) {
            const detail = parsed ? JSON.stringify(parsed).slice(0, 300) : String(resp.body).slice(0, 300);
            log.warning(`CourtListener ${resp.statusCode}: ${detail}`);
            return null;
        }
        if (!parsed) {
            log.warning(`CourtListener returned a non-JSON body: ${String(resp.body).slice(0, 200)}`);
            return null;
        }
        return parsed;
    }
    log.warning('CourtListener kept erroring after 4 attempts; stopping this walk early.');
    return null;
}

function firstUrl(kind) {
    const qs = new URLSearchParams();
    qs.set('type', TYPE_FOR[kind]);
    if (query) qs.set('q', query);
    // `court` takes a space-separated list of court ids; repeating the param only keeps the last.
    if (courts.length) qs.set('court', courts.join(' '));
    if (filedAfter) qs.set('filed_after', filedAfter);
    if (filedBefore) qs.set('filed_before', filedBefore);
    // Field searches, each sent only to the index that carries the field (see the narrowing
    // block above — by this point the other index has already been dropped from the run).
    if (docketNumber) qs.set('docket_number', docketNumber);
    if (kind === 'dockets') {
        if (partyName) qs.set('party_name', partyName);
        if (attorneyName) qs.set('atty_name', attorneyName);
    }
    if (kind === 'opinions') {
        if (judge) qs.set('judge', judge);
        for (const p of OPINION_STAT_PARAM[opinionStatus]) qs.set(p, 'on');
    }
    return `${SEARCH}?${qs.toString()}`;
}

if (opinionStatus !== 'published' && !recordTypes.includes('opinions')) {
    log.warning(`opinionStatus "${opinionStatus}" is set but recordType "${recordTypeRaw}" does not include opinions — ignored.`);
}

const listOf = (v) => (Array.isArray(v) ? v.filter((x) => x != null && x !== '') : []);
const blankToNull = (v) => (v === '' || v === undefined ? null : v);
const abs = (p) => (p ? `${BASE}${p}` : null);
// RECAP PDFs live on a public bucket, not behind the API's auth. `filepath_local` is the key.
const PDF_BASE = 'https://storage.courtlistener.com/';
const pdfUrl = (p) => (typeof p === 'string' && p.trim() ? `${PDF_BASE}${p.trim()}` : null);

// One superset dataset shape covers both record types, the way both incumbent listings do it:
// a buyer searching "both" gets one sortable table instead of two schemas to reconcile.
// Fields that only exist on one side are null on the other, never omitted.
function normalizeOpinion(r) {
    const opinions = listOf(r.opinions);
    return {
        recordType: 'opinion',
        id: r.cluster_id != null ? `o-${r.cluster_id}` : null,
        caseName: blankToNull(r.caseName) ?? null,
        caseNameFull: blankToNull(r.caseNameFull) ?? null,
        court: blankToNull(r.court) ?? null,
        courtId: blankToNull(r.court_id) ?? null,
        courtCitationString: blankToNull(r.court_citation_string) ?? null,
        docketNumber: blankToNull(r.docketNumber) ?? null,

        dateFiled: r.dateFiled ?? null,
        dateArgued: r.dateArgued ?? null,
        dateTerminated: null,

        // Reported citations ("310 F. Supp. 3d 149"). citeCount is how many later opinions cite
        // this one — the cheapest available proxy for how load-bearing a precedent is.
        citations: listOf(r.citation),
        citeCount: r.citeCount ?? null,
        lexisCite: blankToNull(r.lexisCite) ?? null,
        neutralCite: blankToNull(r.neutralCite) ?? null,

        judge: blankToNull(r.judge) ?? null,
        panelNames: listOf(r.panel_names),
        // Opinions expose `attorney` as one free-text block (with reporter page markers),
        // dockets expose it as a clean array. Kept in the same column, shapes differ by side.
        attorneys: blankToNull(r.attorney) ? [String(r.attorney)] : [],
        parties: [],
        firms: [],

        status: blankToNull(r.status) ?? null,
        posture: blankToNull(r.posture) ?? null,
        proceduralHistory: blankToNull(r.procedural_history) ?? null,
        syllabus: blankToNull(r.syllabus) ?? null,
        suitNature: blankToNull(r.suitNature) ?? null,
        cause: null,
        jurisdictionType: blankToNull(r.court_jurisdiction) ?? null,
        juryDemand: null,
        chapter: null,

        // First lines of the lead opinion's text — enough to triage a hit without a detail fetch.
        snippet: blankToNull(opinions[0]?.snippet) ?? null,
        opinionCount: opinions.length,
        // Where the PDF/text actually lives when CourtListener has it; null on many older rows.
        downloadUrl: opinions.find((o) => o.download_url)?.download_url ?? null,

        docketId: r.docket_id ?? null,
        clusterId: r.cluster_id ?? null,
        pacerCaseId: null,
        documentCount: null,
        documents: [],

        url: abs(r.absolute_url),
        dateCreated: r.meta?.date_created ?? null,
    };
}

function normalizeDocket(r) {
    const docs = listOf(r.recap_documents);
    return {
        recordType: 'docket',
        id: r.docket_id != null ? `r-${r.docket_id}` : null,
        caseName: blankToNull(r.caseName) ?? null,
        caseNameFull: blankToNull(r.case_name_full) ?? null,
        court: blankToNull(r.court) ?? null,
        courtId: blankToNull(r.court_id) ?? null,
        courtCitationString: blankToNull(r.court_citation_string) ?? null,
        docketNumber: blankToNull(r.docketNumber) ?? null,

        dateFiled: r.dateFiled ?? null,
        dateArgued: r.dateArgued ?? null,
        dateTerminated: r.dateTerminated ?? null,

        citations: [],
        citeCount: null,
        lexisCite: null,
        neutralCite: null,

        judge: blankToNull(r.assignedTo) ?? null,
        panelNames: blankToNull(r.referredTo) ? [String(r.referredTo)] : [],
        attorneys: listOf(r.attorney),
        parties: listOf(r.party),
        firms: listOf(r.firm),

        status: null,
        posture: null,
        proceduralHistory: null,
        syllabus: null,
        suitNature: blankToNull(r.suitNature) ?? null,
        cause: blankToNull(r.cause) ?? null,
        jurisdictionType: blankToNull(r.jurisdictionType) ?? null,
        juryDemand: blankToNull(r.juryDemand) ?? null,
        // Bankruptcy chapter (7/11/13) — present only on bankruptcy dockets.
        chapter: blankToNull(r.chapter) ?? null,

        snippet: blankToNull(docs.find((d) => d.snippet)?.snippet) ?? null,
        opinionCount: null,
        // Same meaning as on opinions: where the PDF actually lives. For dockets that is the
        // RECAP archive copy of the first filing that has one (storage.courtlistener.com is
        // public — no token, unlike the /recap-documents/ detail endpoint).
        downloadUrl: docs.map((d) => pdfUrl(d.filepath_local)).find(Boolean) ?? null,

        docketId: r.docket_id ?? null,
        clusterId: null,
        pacerCaseId: blankToNull(r.pacer_case_id) ?? null,
        documentCount: docs.length,
        // Per-filing metadata the search index already returns. `isAvailable` is the honest part:
        // it is false whenever CourtListener has the docket entry but not the PDF behind it, which
        // is common — do not assume every row comes with a downloadable document.
        // `textSnippet` is the OCR'd text of the filing as the index holds it (~500 chars, only on
        // available documents); `pdfUrl` is the full document itself. Both come free with the search
        // response — full plain text needs CourtListener's token-gated /recap-documents/ endpoint.
        documents: docs.map((d) => ({
            documentId: d.id ?? null,
            entryNumber: d.entry_number ?? null,
            attachmentNumber: d.attachment_number ?? null,
            description: blankToNull(d.short_description) ?? blankToNull(d.description) ?? null,
            entryDateFiled: d.entry_date_filed ?? null,
            pageCount: d.page_count ?? null,
            documentType: blankToNull(d.document_type) ?? null,
            isAvailable: d.is_available === true,
            textSnippet: blankToNull(d.snippet) ?? null,
            pdfUrl: pdfUrl(d.filepath_local),
            url: abs(blankToNull(d.absolute_url)),
        })),

        url: abs(r.docket_absolute_url),
        dateCreated: r.meta?.date_created ?? null,
    };
}

// ---------------------------------------------------------------------------
// Watch mode: "only what is new since my last run", per saved query.
// Same design as federal-register/grants-gov: the baseline lives in a NAMED key-value store so
// it survives across runs (the default store is per-run and would re-charge the whole set every
// time), and the filter fingerprint is part of the key so editing a filter starts a new baseline
// instead of dumping everything the older, narrower filter had excluded.
const WATCH_STORE = 'fetchsmith-courtlistener-watch';
const SEED_CAP = 20000;
const WATCH_KEEP = 60000;

function watchKeyFor(label, criteria) {
    const safe = label.toLowerCase().replace(/[^a-z0-9_.-]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 40) || 'default';
    const fp = createHash('sha1').update(JSON.stringify(criteria, Object.keys(criteria).sort())).digest('hex').slice(0, 10);
    return { key: `watch-${safe}-${fp}`, fingerprint: fp };
}

const watchCriteria = {
    query,
    recordTypes: [...recordTypes].sort(),
    courts: [...courts].sort(),
    filedAfter,
    filedBefore,
    ...(opinionStatus !== 'published' ? { opinionStatus } : {}),
    // Each of these changes what the server returns, exactly like `query`/`courts`, so a run
    // that edits one must start a fresh baseline rather than inherit the old filter's "seen"
    // set. Omitted when empty so existing watch labels keep their current key.
    ...(partyName ? { partyName } : {}),
    ...(attorneyName ? { attorneyName } : {}),
    ...(docketNumber ? { docketNumber } : {}),
    ...(judge ? { judge } : {}),
};

const watchMode = watchLabel.length > 0;
let watchStore = null;
let watchKey = null;
let watchRecord = null;
let seeding = false;
const watchSeen = new Set();

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
            + `${watchSeen.size} already-delivered record(s). Only records NOT in that baseline are returned and charged.`,
        );
    } else {
        watchRecord = { fingerprint, firstSeededAt: new Date().toISOString(), runCount: 0 };
        seeding = true;
        log.info(
            `Watch mode "${watchLabel}" (${key}): FIRST run for this label and filter set, so this is a baseline run. `
            + 'It records which records already match and returns ZERO results (you are charged nothing). Run it again '
            + 'on the same label and filters — on a schedule, typically — to get only what is new since now.',
        );
    }
}

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
    `CourtListener: recordType=${recordTypes.join('+')} query="${query || '(none)'}" maxResults=${maxResults}`
    + (courts.length ? ` courts=[${courts.join(',')}]` : '')
    + (filedAfter ? ` filedAfter=${filedAfter}` : '')
    + (filedBefore ? ` filedBefore=${filedBefore}` : '')
    + (recordTypes.includes('opinions') ? ` opinionStatus=${opinionStatus}` : ''),
);

const seenIdsThisRun = new Set();
let scanned = 0;
let pages = 0;
let skippedSeen = 0;
let totalReported = 0;
let stop = false;

// Walk one index until the run's cumulative `pushed` reaches `target` (or the index runs out).
// Returns the cursor URL to resume from, or null when that index is exhausted.
async function walk(state, target) {
    let first = state.started !== true;
    state.started = true;
    while (state.url && !stop && pushed < target) {
        if (!first) await sleep(PAGE_DELAY_MS);
        const page = await apiGet(state.url);
        first = false;
        if (!page) { state.url = null; break; }
        const results = listOf(page.results);
        if (typeof page.count === 'number' && !state.counted) {
            totalReported += page.count;
            state.counted = true;
        }
        if (!results.length) { state.url = null; break; }
        pages += 1;

        for (const row of results) {
            scanned += 1;
            const item = state.kind === 'opinions' ? normalizeOpinion(row) : normalizeDocket(row);
            const key = item.id ?? `${state.kind}:${item.caseName}:${item.dateFiled}`;
            if (seenIdsThisRun.has(key)) continue;
            seenIdsThisRun.add(key);

            if (seeding) {
                watchSeen.add(key);
                if (watchSeen.size >= SEED_CAP) { stop = true; break; }
                continue;
            }
            // Already delivered under this watch label: dropped before any charge, so a record
            // is never paid for twice.
            if (watchMode && watchSeen.has(key)) { skippedSeen += 1; continue; }

            const before = pushed;
            const keepGoing = await pushResult(item);
            if (watchMode && pushed > before) watchSeen.add(key);
            if (!keepGoing || pushed >= maxResults) { stop = true; break; }
            if (pushed >= target) break;
        }
        // Follow the API's own cursor link rather than rebuilding it: the cursor token is opaque
        // and there is no offset paging to fall back on.
        state.url = typeof page.next === 'string' && page.next ? page.next : null;
    }
    return state.url;
}

const walkers = recordTypes.map((kind) => ({ kind, url: firstUrl(kind), started: false, counted: false }));

// With recordType "both" the two indexes are walked to a fair share of maxResults each, not
// first-come-first-served. The opinion index is far larger than the RECAP one for most queries,
// so a naive sequential walk spends the entire budget on opinions and a buyer who asked for
// "both" never sees a single docket — measured, not assumed (40/40 opinions on the first draft).
const shareCap = Math.ceil(maxResults / walkers.length);
// A baseline walk must cover the WHOLE match set of every selected index, not a share of it:
// a baseline that stopped early would report everything past the stopping point as "new".
const roundTarget = (i) => (seeding ? maxResults : Math.min(maxResults, shareCap * (i + 1)));

for (const [i, state] of walkers.entries()) {
    if (stop) break;
    await walk(state, roundTarget(i));
}
// Second round: whatever share one index left unused goes to the others, so an exhausted or
// empty index never silently shrinks the result set below maxResults.
while (!stop && pushed < maxResults && walkers.some((s) => s.url)) {
    const before = pushed;
    for (const state of walkers) {
        if (stop || pushed >= maxResults || !state.url) continue;
        await walk(state, maxResults);
    }
    if (pushed === before) break;
}

if (watchMode) {
    await saveWatchRecord(seeding ? 'seeded' : 'incremental');
    if (seeding) {
        log.info(
            `Baseline saved for watch label "${watchLabel}": ${watchSeen.size} record(s) recorded as already-seen, `
            + '0 results returned, 0 charged. The next run on this label and these filters returns only new records.'
            + (watchSeen.size >= SEED_CAP
                ? ` NOTE: the baseline stopped at the ${SEED_CAP}-record cap. Narrow the query (a court, a shorter `
                + 'filed-date window) so the whole result set fits, or the first incremental run will report records '
                + 'past the cap as new.'
                : ''),
        );
    } else {
        log.info(
            `Watch label "${watchLabel}": ${pushed} new record(s) since the last run `
            + `(${skippedSeen} already-delivered row(s) skipped, uncharged); baseline now holds ${watchSeen.size}.`,
        );
    }
}

if (pushed === 0 && watchMode && !seeding) {
    log.warning(
        `Nothing new for watch label "${watchLabel}" since its last run — all ${skippedSeen} matching record(s) had `
        + 'already been delivered. That is the expected result most of the time; you were charged for nothing.',
    );
} else if (pushed === 0 && !seeding) {
    log.warning(
        `No records matched. Scanned ${scanned} rows. Most common causes, in order: `
        + '(1) every filter is ANDed — a query plus a court plus a narrow filed-date window often has zero real '
        + 'matches; drop one and retry. '
        + '(2) a court id must be CourtListener\'s own short slug, the one in a courtlistener.com/court/<id>/ URL '
        + '("scotus", "ca9", "cand", "cacb") — an unrecognised id is not rejected upstream, it silently matches nothing. '
        + '(3) recordType matters: RECAP dockets ("dockets") and published opinions ("opinions") are separate indexes, '
        + 'and a case present in one is often absent from the other. Use "both" when unsure. '
        + '(4) the query is a full-text search over case text and metadata, not a case-number lookup — use the '
        + 'dedicated docketNumber field for a case number, and if that returns nothing try it without the office '
        + 'prefix ("20-cv-03590" rather than "1:20-cv-03590"), since the format varies by court. '
        + '(5) partyName/attorneyName match the parties and attorneys recorded on a RECAP docket — a name that only '
        + 'appears in the body text of an opinion will not match; put that in the query instead.',
    );
}

log.info(
    `Done. Pushed ${pushed} record(s) over ${pages} page(s) (scanned ${scanned} rows; `
    + `CourtListener reported ${totalReported} total matches across the selected index(es)).`,
);

// Fires after every row is already pushed and charged, so a slow or failing webhook can never
// affect the result set or the bill — best-effort only, one attempt, short timeout, failures are
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
        totalReported,
        watchLabel: watchMode ? watchLabel : null,
        watchNewCount: watchMode && !seeding ? pushed : null,
        watchSeeding: watchMode ? seeding : null,
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
