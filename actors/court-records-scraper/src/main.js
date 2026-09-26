import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';

// courtId -> human-readable jurisdiction label ("Federal District", "State Supreme", ...).
// Harvested from CourtListener's own /courts/?in_use=true (all 472 in-use courts) with the
// code->label table taken from the OPTIONS endpoint's jurisdiction choices, so both halves
// are the API's own values rather than hand-written. Courts absent from the map (historical
// / not-in-use) stay null by design. readFileSync + import.meta.url rather than an import
// attribute: the apify/actor-node:20 image's exact patch level isn't guaranteed >= 20.10.
const JURISDICTIONS = JSON.parse(readFileSync(new URL('./court-jurisdictions.json', import.meta.url), 'utf8'));

function jurisdictionFor(courtId) {
    if (!courtId) return null;
    return JURISDICTIONS.codes[JURISDICTIONS.courts[courtId]] ?? null;
}

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
//
// Re-measured cycle 743 across 4 fresh topic queries: the drop is NOT a constant ~26% — it
// ranged 5.7% ("patent infringement") to 37.2% ("immigration") to 18.8%/13.7% on two others.
// Also found `any` (published+unpublished) was itself silently incomplete: CourtListener's
// opinion `status` field has 5 more real values beyond those two (`stat_Errata`, `stat_Separate`,
// `stat_In-chambers`, `stat_Relating-to`, `stat_Unknown`) — confirmed live, e.g. on "immigration"
// `stat_Unknown=on` alone matched 31,096 real, dated opinions (2023-2025 district-court rows,
// not junk/placeholders) that "any" was dropping on the floor, ~17.7% on top of published+
// unpublished. Widened `any` to all 7 real status flags so it matches its own name.
const OPINION_STAT_PARAM = {
    published: ['stat_Published'],
    unpublished: ['stat_Unpublished'],
    any: ['stat_Published', 'stat_Unpublished', 'stat_Errata', 'stat_Separate', 'stat_In-chambers', 'stat_Relating-to', 'stat_Unknown'],
};
let opinionStatus = String(input.opinionStatus ?? 'published').toLowerCase().trim();
if (!Object.hasOwn(OPINION_STAT_PARAM, opinionStatus)) {
    log.warning(`Unknown opinionStatus "${input.opinionStatus}"; falling back to "published".`);
    opinionStatus = 'published';
}

// Sort order. `order_by=dateFiled asc|desc` is a real server-side sort — verified live cycle
// 458 against the anonymous search endpoint on BOTH indexes: same total count as unsorted,
// just reordered (an opinion from 1746 first vs. one from today first). `citeCount` sort,
// tempting since we already emit `citeCount`, is opinions-only and returned an Internal Server
// Error (not a 400, not a silent ignore) when sent to the docket index — confirmed twice, not
// a fluke — so it is deliberately not exposed; only the field proven safe on both indexes is.
const SORT_PARAM = { relevance: null, datefileddesc: 'dateFiled desc', datefiledasc: 'dateFiled asc' };
let sortByRaw = String(input.sortBy ?? 'relevance').toLowerCase().trim();
if (!Object.hasOwn(SORT_PARAM, sortByRaw)) {
    log.warning(`Unknown sortBy "${input.sortBy}"; falling back to "relevance".`);
    sortByRaw = 'relevance';
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

// A filed-date bound that fails to parse must never be dropped silently. Unlike the
// opinionStatus fallback above — which NARROWS the run and is therefore safe — losing a date
// bound WIDENS it to the whole corpus, and every extra row is billed at the per-result price.
// Measured on build x4edIEyelG6c0JR4A (cycle 589) with the old digit-counting parser:
// filedAfter "2024-6-5" / filedBefore "2024-6-9" stripped to 6 digits each, both returned null,
// both filters vanished, and the run returned 10/10 SCOTUS opinions filed 1795-1831. The same
// parser turned the US-style "06/15/2024" into the nonsense "0615-20-24", which CourtListener
// answers with HTTP 400 ("The date entered has an invalid format") — so the buyer saw a
// retry-then-give-up failure naming a date they never typed.
//
// So: accept every unambiguous spelling of an ISO date, and abort loudly on anything else
// rather than guessing. Day-first vs. month-first ("06/15/2024") is deliberately NOT guessed.
const normDate = (v, field) => {
    const s = String(v ?? '').trim();
    if (!s) return null;
    // YYYY-MM-DD, YYYY-M-D, YYYY/M/D, YYYY.M.D and bare YYYYMMDD. The leading 4-digit year is
    // what makes this unambiguous: "06/15/2024" cannot match it and is rejected below.
    const m = /^(\d{4})\D?(\d{1,2})\D?(\d{1,2})$/.exec(s);
    const bad = (why) => new Error(
        `${field} "${s}" ${why}. Use an ISO date, YYYY-MM-DD — for example "2024-06-05". `
        + 'Stopping instead of ignoring the filter: a filed-date bound that is dropped widens '
        + 'the search to the whole archive (back to the 1700s) and you would be charged for '
        + 'every one of those rows. US-style dates like "06/15/2024" are rejected on purpose, '
        + 'because 06/15 and 15/06 cannot be told apart.',
    );
    if (!m) throw bad('is not a date I can read');
    const [y, mo, d] = [m[1], m[2].padStart(2, '0'), m[3].padStart(2, '0')];
    const iso = `${y}-${mo}-${d}`;
    // Calendar-validate by round-trip: "2024-06-31" parses fine above but CourtListener
    // answers it with HTTP 400, so catch it here where the message can be useful.
    const dt = new Date(`${iso}T00:00:00Z`);
    if (Number.isNaN(dt.getTime()) || dt.toISOString().slice(0, 10) !== iso) {
        throw bad('is not a real calendar date');
    }
    return iso;
};
let filedAfter = normDate(input.filedAfter, 'filedAfter');
let filedBefore = normDate(input.filedBefore, 'filedBefore');

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

    if (qp.has('filed_after')) { filedAfter = normDate(qp.get('filed_after'), 'startUrl filed_after'); } else { ignored.push('filedAfter'); }
    if (qp.has('filed_before')) { filedBefore = normDate(qp.get('filed_before'), 'startUrl filed_before'); } else { ignored.push('filedBefore'); }

    const wantsPub = qp.get('stat_Published') === 'on';
    const wantsUnpub = qp.get('stat_Unpublished') === 'on';
    if (wantsPub || wantsUnpub) {
        opinionStatus = wantsPub && wantsUnpub ? 'any' : (wantsUnpub ? 'unpublished' : 'published');
    } else {
        ignored.push('opinionStatus');
    }

    if (qp.has('order_by')) {
        const norm = (qp.get('order_by') ?? '').toLowerCase().replace(/\s+/g, '');
        if (norm === 'scoredesc' || norm === '') {
            sortByRaw = 'relevance';
        } else if (Object.hasOwn(SORT_PARAM, norm)) {
            sortByRaw = norm;
        } else {
            log.warning(
                `startUrl has order_by="${qp.get('order_by')}", which this Actor does not support (only Filing date `
                + 'asc/desc, or the default relevance sort). Using the "Sort by" field below instead.',
            );
        }
    } else {
        ignored.push('sortBy');
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

// `state` (when given) records WHY a null came back, since the caller only sees null either
// way — without this a permanent 500 and a genuinely exhausted index are indistinguishable to
// everything downstream of apiGet, which is exactly the h250 gap this cycle closes.
// A 400/404/422 is CourtListener rejecting the request itself (e.g. a malformed field
// combination) -- retrying the identical input will fail identically. 429/5xx/network errors
// are the only ones worth telling a buyer to "re-run in a few minutes" for (h836 TED class bug).
const INPUT_ERROR_STATUS = new Set([400, 404, 422]);

async function apiGet(url, state = null) {
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
            if (state) state.lastError = `request failed: ${err.message}`;
            await sleep(waitS * 1000);
            continue;
        }
        if (resp.statusCode === 429 || resp.statusCode >= 500) {
            const waitS = Number(resp.headers['retry-after']) || attempt * 10;
            log.warning(`CourtListener returned ${resp.statusCode}; retrying in ${waitS}s (${attempt}/4).`);
            if (state) { state.lastError = `HTTP ${resp.statusCode}`; state.lastErrorStatus = resp.statusCode; }
            await sleep(waitS * 1000);
            continue;
        }
        let parsed = null;
        try { parsed = JSON.parse(resp.body); } catch { /* handled below */ }
        if (resp.statusCode !== 200) {
            const detail = parsed ? JSON.stringify(parsed).slice(0, 300) : String(resp.body).slice(0, 300);
            log.warning(`CourtListener ${resp.statusCode}: ${detail}`);
            if (state) { state.lastError = `HTTP ${resp.statusCode}: ${detail.slice(0, 120)}`; state.lastErrorStatus = resp.statusCode; }
            return null;
        }
        if (!parsed) {
            log.warning(`CourtListener returned a non-JSON body: ${String(resp.body).slice(0, 200)}`);
            if (state) state.lastError = `non-JSON body: ${String(resp.body).slice(0, 120).replace(/\s+/g, ' ').trim()}`;
            return null;
        }
        return parsed;
    }
    log.warning('CourtListener kept erroring after 4 attempts; stopping this walk early.');
    if (state) state.lastError = state.lastError ? `${state.lastError} (after 4 retries)` : 'unreachable after 4 retries';
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
    if (SORT_PARAM[sortByRaw]) qs.set('order_by', SORT_PARAM[sortByRaw]);
    return `${SEARCH}?${qs.toString()}`;
}

if (opinionStatus !== 'published' && !recordTypes.includes('opinions')) {
    log.warning(`opinionStatus "${opinionStatus}" is set but recordType "${recordTypeRaw}" does not include opinions — ignored.`);
}

// Each index is sorted independently; the two streams are never merged into one combined
// order. With recordType "both" the walk already visits opinions to their share of maxResults
// before starting dockets (see roundTarget below), so a non-default sort just reorders within
// each of those two chunks, not across the whole output — worth a heads-up since a buyer might
// otherwise expect a single globally-sorted table.
if (sortByRaw !== 'relevance' && recordTypes.length > 1) {
    log.info(
        `sortBy "${sortByRaw}" applies within each index separately — recordType "both" returns opinions `
        + '(sorted) up to their share of maxResults, then dockets (sorted), not one table sorted end to end.',
    );
}

const listOf = (v) => (Array.isArray(v) ? v.filter((x) => x != null && x !== '') : []);
const blankToNull = (v) => (v === '' || v === undefined ? null : v);
const abs = (p) => (p ? `${BASE}${p}` : null);
// RECAP PDFs live on a public bucket, not behind the API's auth. `filepath_local` is the key.
const PDF_BASE = 'https://storage.courtlistener.com/';
const pdfUrl = (p) => (typeof p === 'string' && p.trim() ? `${PDF_BASE}${p.trim()}` : null);

// PACER's `jurisdictionType` free-text field comes back with inconsistent casing across courts
// for what is otherwise the same value — e.g. "Federal Question" (nysd) vs "Federal question"
// (ilnd), confirmed live cycle 494 (429 rows / 20 courts: also "U.S. Government Defendant" vs
// "Government plaintiff"). Title-case every word so a buyer grouping on this field doesn't get
// split buckets for a casing accident. This does NOT merge genuinely different upstream text
// (e.g. "Diversity" vs "Diversity of citizenship", or the presence/absence of a "U.S." prefix)
// — those are real content differences, left as-is rather than guessed at.
const normalizeJurisdictionTypeCasing = (v) => {
    if (typeof v !== 'string' || !v.trim()) return null;
    const LOWER_WORDS = new Set(['of', 'the', 'and']);
    return v
        .trim()
        .split(/\s+/)
        .map((word, i) => {
            if (/^u\.s\.?$/i.test(word)) return 'U.S.';
            const lower = word.toLowerCase();
            if (i > 0 && LOWER_WORDS.has(lower)) return lower;
            return lower.charAt(0).toUpperCase() + lower.slice(1);
        })
        .join(' ');
};

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
        courtJurisdiction: jurisdictionFor(blankToNull(r.court_id)),
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
        proceduralHistory: blankToNull(r.procedural_history) ?? null,
        syllabus: blankToNull(r.syllabus) ?? null,
        suitNature: blankToNull(r.suitNature) ?? null,
        cause: null,
        // Docket-only, like `cause`/`juryDemand`/`chapter` above. This used to pass through the
        // opinion index's `court_jurisdiction`, but that is a different concept wearing the same
        // name: on dockets `jurisdictionType` is PACER's basis for the CASE's federal jurisdiction
        // ("Diversity", "Federal Question"); `court_jurisdiction` classifies the COURT ("F" =
        // Federal Appellate). Measured 20/140 filled across 8 court slices (cycle 492) and 21/240
        // (cycle 488) — effectively scotus-only — so it was a sparse column of the wrong quantity.
        jurisdictionType: null,
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
        courtJurisdiction: jurisdictionFor(blankToNull(r.court_id)),
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
        proceduralHistory: null,
        syllabus: null,
        suitNature: blankToNull(r.suitNature) ?? null,
        cause: blankToNull(r.cause) ?? null,
        jurisdictionType: normalizeJurisdictionTypeCasing(blankToNull(r.jurisdictionType)),
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
let baselineTruncated = 0; // ids dropped by WATCH_KEEP this run -- they come back as "new" and get charged
let baselineTruncatedTotal = 0; // same, cumulative over the life of this label

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
    // sortBy is deliberately NOT here: it reorders the same match set, it never changes WHICH
    // records match, so editing it should not throw away a baseline (unlike everything above).
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
    if (!seeding && sortByRaw === 'datefiledasc') {
        // Filing-date-ascending walks from the OLDEST match forward. On an established watch
        // label most of that oldest end is already in the baseline, so an incremental run can
        // spend its whole page budget skipping long-delivered records before it ever reaches
        // anything genuinely new near the recent end — wasted API calls, not a billing risk
        // (skipped rows are never charged), but a real reason to prefer "newest first" here.
        log.warning(
            'sortBy is "Filing date, oldest first" together with Watch label: an incremental run walks from the '
            + 'oldest match forward, so on a large result set it may page through a long run of already-delivered '
            + 'records before reaching anything new. "Filing date, newest first" or the default relevance sort do '
            + 'not have this problem, since a newly-added record is far more likely to appear near the front either way.',
        );
    }
}

async function saveWatchRecord(status) {
    const all = Array.from(watchSeen);
    const ids = all.slice(-WATCH_KEEP);
    // An id past the record cap is not forgotten harmlessly: the next run does not find it in the
    // baseline, so the opinion/docket is delivered and CHARGED again even though the buyer already
    // paid for it. The dropped end is oldest-FIRST-SEEN (re-seeing an id does not move it in the
    // Set), so on CourtListener -- where a docket keeps matching the same court/party filter for
    // years -- the ids that fall off are exactly the long-lived records that will match again on
    // the very next run. The cap itself is deliberate (KV record size budget); the bug this fixes
    // was that it applied in silence.
    baselineTruncated = all.length - ids.length;
    baselineTruncatedTotal = (watchRecord.truncatedTotal ?? 0) + baselineTruncated;
    if (baselineTruncated > 0) {
        log.warning(
            `The baseline for "${watchLabel}" exceeded the ${WATCH_KEEP}-entry record cap; the ${baselineTruncated} `
            + 'oldest record id(s) were dropped and will be returned and CHARGED as new on a future run '
            + `(${baselineTruncatedTotal} dropped over the life of this label). Narrow the watch query `
            + '(a court, fewer record types, a shorter filed-date window) or split it across several labels so '
            + 'each baseline stays under the cap.',
        );
    }
    await watchStore.setValue(watchKey, {
        ...watchRecord,
        label: watchLabel,
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

// Empty unless WATCH_KEEP actually dropped something, so it can never add noise to a healthy run.
function truncationNote() {
    if (baselineTruncated <= 0) return '';
    return ` WARNING: the baseline hit its ${WATCH_KEEP}-entry cap and ${baselineTruncated} oldest record id(s) were`
        + ' dropped — those will be delivered and charged again as "new". Narrow the query or split it across labels.';
}

let pushed = 0;
let chargeLimitReached = false;
const isPPE = Actor.getChargingManager().getPricingInfo().isPayPerEvent;
async function pushResult(item) {
    if (isPPE) {
        const r = await Actor.charge({ eventName: 'result', count: 1 });
        // Both of these end the walk; only the charge limit is a cause the buyer set on the RUN
        // rather than in the input, so RUN_SUMMARY has to tell them apart from maxResults.
        if (r.chargedCount === 0) { chargeLimitReached = true; return false; }
        await Actor.pushData(item); pushed += 1;
        if (r.eventChargeLimitReached) chargeLimitReached = true;
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
    + (recordTypes.includes('opinions') ? ` opinionStatus=${opinionStatus}` : '')
    + (sortByRaw !== 'relevance' ? ` sortBy=${sortByRaw}` : ''),
);

const seenIdsThisRun = new Set();
let scanned = 0;
let pages = 0;
let skippedSeen = 0;
let totalReported = 0;
let stop = false;

// Walk one index until the run's cumulative `pushed` reaches `target` (or the index runs out).
// Returns the cursor URL to resume from, or null when that index is exhausted OR failed —
// `state.exhausted`/`state.failed` are what tell those two apart afterwards (see the
// completeness contract below); before this cycle nothing recorded the difference at all.
async function walk(state, target) {
    let first = state.started !== true;
    state.started = true;
    while (state.url && !stop && pushed < target) {
        if (!first) await sleep(PAGE_DELAY_MS);
        const page = await apiGet(state.url, state);
        first = false;
        if (!page) { state.failed = true; state.url = null; break; }
        const results = listOf(page.results);
        if (typeof page.count === 'number' && state.declaredMatches === null) {
            state.declaredMatches = page.count;
            totalReported += page.count;
        }
        if (!results.length) { state.exhausted = true; state.url = null; break; }
        pages += 1;
        state.pages += 1;

        for (const row of results) {
            scanned += 1;
            state.scanned += 1;
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
            if (pushed > before) state.delivered += 1;
            if (watchMode && pushed > before) watchSeen.add(key);
            if (!keepGoing || pushed >= maxResults) { stop = true; break; }
            if (pushed >= target) break;
        }
        // Follow the API's own cursor link rather than rebuilding it: the cursor token is opaque
        // and there is no offset paging to fall back on.
        state.url = typeof page.next === 'string' && page.next ? page.next : null;
        if (!state.url) state.exhausted = true;
    }
    return state.url;
}

const walkers = recordTypes.map((kind) => ({
    kind,
    url: firstUrl(kind),
    started: false,
    pages: 0,
    scanned: 0,
    delivered: 0,
    declaredMatches: null,
    exhausted: false,
    failed: false,
    lastError: null,
}));

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

// ---------------------------------------------------------------------------
// Completeness contract (cycle 653), same shape as sam-gov-opportunities-scraper /
// uk-find-a-tender-scraper: a RUN_SUMMARY key-value record, a status message, and the same
// object on the webhook payload. This was the h250 scan's last untouched target, and the gap
// was in `walk()`'s stop path: `if (!page) { state.url = null; break; }` treated a permanent
// upstream failure (4 failed retries, a non-200, a non-JSON body) exactly like a natural end
// of the index (`!results.length` or no `next` cursor) — both just set `state.url = null` and
// the run ended "Done. Pushed N record(s)..." either way. A buyer searching a court with
// ongoing litigation who got "0 dockets" could not tell a genuinely empty court from a
// mid-walk 500; `walk()` now records `exhausted`/`failed`/`lastError` per index instead.
let complete = true;
let incompleteReason = null;
let incompleteDetail = null;
function markIncomplete(reason, detail = null) {
    if (!complete) return;
    complete = false;
    incompleteReason = reason;
    incompleteDetail = detail;
}

const failedWalkers = walkers.filter((w) => w.failed);
// True when at least one failed walker's last error was CourtListener rejecting the request
// itself (400/404/422), not a transient 429/5xx/network fault -- re-running with the same
// input would fail identically (h836 TED class bug).
const seedFailureIsInputError = failedWalkers.some((w) => INPUT_ERROR_STATUS.has(w.lastErrorStatus));
if (failedWalkers.length) {
    markIncomplete(
        'source-error',
        `${failedWalkers.map((w) => w.kind).join(' and ')} stopped answering `
        + `(${failedWalkers.map((w) => `${w.kind}: ${w.lastError ?? 'unknown error'}`).join('; ')}); its remaining `
        + 'matches are missing from this run, and a low or zero delivered count for it does NOT mean the index had that few',
    );
}
// A walker that still has a cursor to follow only happens because the shared `stop` flag fired
// (maxResults, a charge limit, or the watch seed cap) — the redistribution loop above only ends
// early via `stop`; otherwise it keeps rotating budget until every walker's `url` is null
// (exhausted or failed), so this is checked after both rounds, not per-round.
const stillOpen = walkers.filter((w) => w.url);
if (stillOpen.length) {
    const rest = stillOpen.map((w) => w.kind).join(' and ');
    if (chargeLimitReached) {
        markIncomplete('charge-limit', `the run's pay-per-event charge limit was reached with ${rest} still to read`);
    } else if (seeding && watchSeen.size >= SEED_CAP) {
        markIncomplete('seed-cap', `the baseline stopped at the ${SEED_CAP}-record cap with ${rest} still to read`);
    } else if (!seeding && pushed >= maxResults) {
        markIncomplete('max-results', `maxResults=${maxResults} was reached with ${rest} still to read`);
    } else {
        // Should be unreachable given the loop structure above — say so rather than reporting
        // a false "complete".
        markIncomplete('stopped-early', `the walk ended with ${rest} still to read for no recorded reason`);
    }
}

// A seed walk cut short by a genuine upstream failure (`source-error`) or the unreachable
// `stopped-early` fallback must NOT save its partial id set as the baseline: the next incremental
// run would then deliver and CHARGE every record past the failure point as "new", even though
// the buyer already paid nothing for this run. `seed-cap` is deliberately excluded — that is the
// buyer's own query being broader than WATCH_KEEP, already surfaced above, and a capped-but-real
// baseline beats none (same policy as the rest of the fleet's h289 fixes).
const seedFailure = seeding && (incompleteReason === 'source-error' || incompleteReason === 'stopped-early');

if (watchMode && seedFailure) {
    log.warning(
        `Baseline NOT saved for watch label "${watchLabel}": ${incompleteReason} — ${incompleteDetail}. `
        + 'Saving a partial baseline here would cause every record past the failure point to be delivered '
        + `and CHARGED as "new" on the next incremental run. ${seedFailureIsInputError
            ? 'This is CourtListener rejecting the input itself -- fix the filter values and re-run.'
            : 'Re-run the seed once the source recovers.'}`,
    );
} else if (watchMode) {
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

// RUN_SUMMARY: this run's completeness, in a form a pipeline can read. Fetch with
//   GET /v2/actor-runs/<runId>/key-value-store/records/RUN_SUMMARY
// which needs no webhook. `complete` is deliberately kept out of the run STATUS: a run can be
// SUCCEEDED and short at the same time, and that pair is exactly what this record exists for.
// `recordTypes` is per-index on purpose — a single fleet-standard `complete` flag would still
// leave "which index, opinions or dockets, is this number missing from?" unanswered.
// `declaredMatches` is null (not summed as 0) unless EVERY requested index returned its own
// count at least once — present-and-0 would read as "we asked and the archive has none",
// which is a different fact than "one index failed before it ever told us its total".
const allDeclared = walkers.every((w) => w.declaredMatches !== null);
const declaredMatchesTotal = allDeclared ? walkers.reduce((n, w) => n + w.declaredMatches, 0) : null;
const runSummary = {
    mode: watchMode ? (seeding ? 'watch-seed' : 'watch-incremental') : 'search',
    recordTypes: Object.fromEntries(walkers.map((w) => [w.kind, {
        pages: w.pages,
        scanned: w.scanned,
        delivered: w.delivered,
        declaredMatches: w.declaredMatches,
        // TRUE only if this index answered until it ran out of results/cursor. When false,
        // `delivered` for it is unknown, not "this index had that few".
        exhausted: w.exhausted,
        failed: w.failed,
        lastError: w.lastError,
    }])),
    recordTypesRequested: recordTypes,
    declaredMatches: declaredMatchesTotal,
    scanned,
    delivered: pushed,
    pages,
    complete,
    incompleteReason,
    incompleteDetail,
    maxResults,
    chargeLimitReached,
    watchLabel: watchMode ? watchLabel : null,
    watchSeeding: watchMode ? seeding : null,
    baselineSize: watchMode ? watchSeen.size : null,
    // Ids the WATCH_KEEP record cap dropped this run / over the life of this label. A dropped id
    // is re-delivered and re-charged later, so this is a billing signal, not just a size stat.
    baselineTruncated: watchMode ? baselineTruncated : null,
    baselineTruncatedTotal: watchMode ? baselineTruncatedTotal : null,
    skippedSeen: watchMode && !seeding ? skippedSeen : null,
};
await Actor.setValue('RUN_SUMMARY', runSummary);

// A short run still SUCCEEDS (the rows it did get are real and already charged), so the status
// message is the only place the Apify console itself shows the shortfall. There was no
// setStatusMessage call anywhere in this Actor before cycle 653.
if (!complete) {
    await Actor.setStatusMessage(
        (seeding
            ? `Baseline INCOMPLETE: ${watchSeen.size.toLocaleString('en-US')} record(s) recorded — ${incompleteReason}`
              + `${incompleteDetail ? ` (${incompleteDetail})` : ''}. Re-seed before scheduling, or the rest will be charged as new. See RUN_SUMMARY.`
            : `Incomplete: ${pushed.toLocaleString('en-US')} record(s) delivered — ${incompleteReason}`
              + `${incompleteDetail ? ` (${incompleteDetail})` : ''}. See RUN_SUMMARY for details.`)
        + truncationNote(),
    );
} else if (baselineTruncated > 0) {
    // A complete run that evicted baseline ids would otherwise show nothing in the console at all
    // — the shortfall lands in a future bill, not in this run's row count.
    await Actor.setStatusMessage(
        (seeding
            ? `Baseline run for watch label "${watchLabel}": ${watchSeen.size.toLocaleString('en-US')} record(s) recorded, 0 charged.`
            : `Watch label "${watchLabel}": ${pushed.toLocaleString('en-US')} record(s) delivered.`)
        + truncationNote(),
    );
} else {
    log.info(`Complete: every selected index (${recordTypes.join(', ')}) was read to the end of its matches for these filters.`);
}

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
        // Same object as the RUN_SUMMARY key-value record, so a webhook consumer and a polling
        // consumer read the identical completeness facts.
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

// Deferred to the very last statement on purpose (h287/h289): failing any earlier would skip the
// RUN_SUMMARY write and the webhook above. A seed pushes no rows, so nothing was charged and
// failing is free -- and failing loudly, instead of exiting 0 with no baseline saved, stops a
// scheduled run from quietly reading "seeded" and moving on to incremental.
if (seedFailure) {
    await Actor.fail(
        `The watch baseline could not be completed: ${incompleteDetail ?? incompleteReason}. No baseline was saved `
        + '(a partial one would cause you to be charged twice for the same records later) and nothing was '
        + `charged. ${seedFailureIsInputError
            ? 'This is CourtListener rejecting your input (an unrecognised court id or a malformed filter) — '
                + 're-running with the same input will fail the same way; fix the filter values above and re-run.'
            : 'Please re-run in a few minutes.'}`,
    );
}

await Actor.exit();
