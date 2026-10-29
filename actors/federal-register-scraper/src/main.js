import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';
import { createHash } from 'node:crypto';

await Actor.init();
const input = (await Actor.getInput()) ?? {};

const timeoutAt = Actor.getEnv().timeoutAt?.getTime() ?? null;
const TIME_BUDGET_MARGIN_MS = 45_000;
function remainingMs() { return timeoutAt == null ? Infinity : timeoutAt - Date.now() - TIME_BUDGET_MARGIN_MS; }
function timeBudgetOk() { return remainingMs() > 0; }
let timeBudgetExceeded = false;

// Apify silently truncates `statusMessage` at 500 chars with no " ..." marker (c1760 LEARNING,
// first ported to this fleet's note-suffix pattern on sec-insider-trades-scraper c2428). Declared
// here, above Actor.init()'s own validation throws (c2437/c2442), because the very first
// Actor.fail() in this file fires during input validation, before any walk has even started.
const STATUS_MESSAGE_MAX = 500;
// `suffix` is RESERVED out of the budget rather than appended after clamping (same reasoning as
// sec-insider-trades-scraper c2428): the suffix carries the one disclosure worth keeping intact,
// so the base truncates first. Guards budget at 0 in case a future suffix ever grows unbounded.
const clampStatusMessage = (msg, suffix = '') => {
    const budget = Math.max(STATUS_MESSAGE_MAX - suffix.length, 0);
    if (msg.length <= budget) return msg + suffix;
    const cut = msg.slice(0, Math.max(budget - 4, 0));
    const lastSpace = cut.lastIndexOf(' ');
    return `${(lastSpace > 0 ? cut.slice(0, lastSpace) : cut).trimEnd()} ...${suffix}`;
};
// Raw caller-supplied text echoed into a note must be capped independently of the backstop above:
// the backstop reserves room FOR the suffix, which only works if the suffix itself is bounded.
const echoCap = (s, max = 60) => (s.length > max ? `${s.slice(0, max)}...` : s);

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

const PRESIDENTIAL_DOCUMENT_TYPES = new Set([
    'executive_order', 'proclamation', 'memorandum', 'notice', 'determination', 'presidential_order', 'other',
]);
const presidentialDocumentTypes = (input.presidentialDocumentTypes ?? [])
    .map((t) => String(t).toLowerCase().trim())
    .filter((t) => PRESIDENTIAL_DOCUMENT_TYPES.has(t));

const searchQuery = String(input.searchQuery ?? '').trim();
const significantOnly = input.significantOnly === true;
const commentsOpenOnly = input.commentsOpenOnly === true;
const order = ['newest', 'oldest', 'relevance', 'executive_order_number'].includes(input.order)
    ? input.order : 'newest';
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

// Verified live against the full 1994-2026 archive (both conditions alone, and together): a
// Presidential Document never carries a comments-close date or an EO-12866 significance flag at
// all (0 matches in FR's entire history for either pairing), unlike RULE/PRORULE/NOTICE which all
// have real — if sometimes rare — matches. Only PRESDOCU-only selections are unreachable; mixing
// PRESDOCU with any other type still returns whatever the other type(s) match.
const presdocuOnly = documentTypes.length > 0 && documentTypes.every((t) => t === 'PRESDOCU');
if (!publicInspection && presdocuOnly && commentsOpenOnly) {
    throw new Error(
        'commentsOpenOnly can never match when documentTypes is limited to PRESDOCU (Presidential Documents) — '
        + 'executive orders, proclamations and memoranda are never opened for public comment (verified live: 0 '
        + "matches across the Federal Register's entire 1994-2026 history). Drop commentsOpenOnly, or include "
        + 'RULE, PRORULE or NOTICE in documentTypes.',
    );
}
if (!publicInspection && presdocuOnly && significantOnly) {
    throw new Error(
        'significantOnly can never match when documentTypes is limited to PRESDOCU (Presidential Documents) — '
        + 'the EO 12866 significance flag is never assigned to presidential documents (verified live: 0 matches '
        + "across the Federal Register's entire 1994-2026 history). Drop significantOnly, or include RULE, "
        + 'PRORULE or NOTICE in documentTypes.',
    );
}
// Verified live: conditions[presidential_document_type] only ever matches rows of type Presidential
// Document, regardless of what else is in conditions[type] — a documentTypes list that does NOT
// include PRESDOCU, combined with presidentialDocumentTypes, is therefore a guaranteed zero-row
// query (RULE alone: 2318 matches over a window; the same window + RULE + presidential_document_type
// EO: 0). Mixing PRESDOCU with other types works fine (the result is just the presidential subset),
// and leaving documentTypes unset (all types) also works, so the only unreachable shape is an
// EXPLICIT non-empty documentTypes that excludes PRESDOCU.
if (!publicInspection && presidentialDocumentTypes.length && documentTypes.length && !documentTypes.includes('PRESDOCU')) {
    throw new Error(
        'presidentialDocumentTypes can never match when documentTypes is set and does not include PRESDOCU — '
        + 'the presidential-document-type filter only ever matches Presidential Documents, and every other type '
        + "has no such field at all (verified live: identical window, RULE alone returns real matches, RULE plus "
        + 'presidentialDocumentTypes returns 0). Include PRESDOCU in documentTypes (alone or mixed with others), '
        + 'leave documentTypes unset, or drop presidentialDocumentTypes.',
    );
}

const today = new Date();
// Every date the Federal Register publishes is an EASTERN calendar date: issues go live at
// 8:45 a.m. ET and a comment period closes at 11:59 p.m. ET on its `comments_close_on` day.
// Actor runs execute in UTC, which is 4-5 hours AHEAD of ET, so between 00:00 and 04:00 UTC
// (05:00 in EST) `new Date().toISOString()` already reads as the NEXT Eastern day. Deriving
// "today" that way silently shifts every date bound by one day for those hours -- verified
// live 2026-09-29: `conditions[comment_date][gte]=2026-09-30` drops document 2026-18943,
// whose comment period was still open for another 6 hours in ET. Anchor to ET instead.
// (`en-CA` formats as YYYY-MM-DD; the Actor base image ships full ICU.)
const ET_DAY = new Intl.DateTimeFormat('en-CA', { timeZone: 'America/New_York' });
const etDay = (d) => ET_DAY.format(d);
// Round-trip through Date.UTC rather than just checking "8 digits": a digit-count-only check
// (the pre-cycle-2315 version of this function) passed "99999999" and silently fell back to the
// default window with no warning -- same for a calendar-impossible but well-formed-looking date
// like "20260230". Date.UTC normalizes overflow (Feb 30 -> Mar 2) instead of rejecting it, so the
// fix has to compare the normalized date back against what was asked for.
const isValidYmd = (y, m, d) => {
    if (!(m >= 1 && m <= 12)) return false;
    const dt = new Date(Date.UTC(y, m - 1, d));
    return dt.getUTCFullYear() === y && dt.getUTCMonth() === m - 1 && dt.getUTCDate() === d;
};
const normDate = (v, fallback, field) => {
    if (v == null || v === '') return fallback;
    const digits = String(v).replace(/[^0-9]/g, '');
    const valid = digits.length === 8
        && isValidYmd(Number(digits.slice(0, 4)), Number(digits.slice(4, 6)), Number(digits.slice(6, 8)));
    if (!valid) {
        throw new Error(`"${field}" is not a real calendar date: ${JSON.stringify(v)}. Use YYYY-MM-DD, e.g. 2026-08-01.`);
    }
    return `${digits.slice(0, 4)}-${digits.slice(4, 6)}-${digits.slice(6, 8)}`;
};
// Unlike the TED/USAspending archives, this feed is read as "what has just been published",
// so the default window is the last 90 days rather than all history. The archive reaches back
// to 1994-01-03 (verified with order=oldest) if the user widens it.
const dateFrom = normDate(input.publicationDateFrom, etDay(new Date(today.getTime() - 90 * 86400_000)), 'publicationDateFrom');
const dateTo = normDate(input.publicationDateTo, etDay(today), 'publicationDateTo');
if (dateFrom > dateTo) {
    throw new Error(`"publicationDateFrom" (${dateFrom}) is after "publicationDateTo" (${dateTo}) — the window is empty. Swap them.`);
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// `state`, when passed, records the terminal cause of a `null` return (h250 class: a permanent
// upstream failure otherwise looks identical to a genuinely exhausted index — both just stop the
// walk with no page). See `runState`/`markIncomplete` near the bottom of the file.
// A 400/404/422 is the Federal Register API rejecting the request itself (e.g. an unknown
// agency slug) -- retrying the identical input will fail identically. 429/5xx/network errors
// are the only ones worth telling a buyer to "re-run in a few minutes" for (h836 TED class bug).
const INPUT_ERROR_STATUS = new Set([400, 404, 422]);

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
        if (!timeBudgetOk()) {
            timeBudgetExceeded = true;
            if (state) { state.lastError = 'run-timeout budget exceeded'; state.lastErrorStatus = null; }
            return null;
        }
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
            const waitMs = Math.min(waitS * 1000, Math.max(remainingMs(), 0));
            log.warning(`Federal Register API request failed (${err.message}); retrying in ${Math.round(waitMs / 1000)}s (${attempt}/4).`);
            if (state) state.lastError = `request failed: ${String(err.message).slice(0, 120)}`;
            await sleep(waitMs);
            continue;
        }
        if (resp.statusCode === 429 || resp.statusCode >= 500) {
            // A server Retry-After has no upper bound of its own -- never let it sleep past this
            // run's own timeout (same exposure closed on every other Actor in the timeout-guard rollout).
            const waitS = Number(resp.headers['retry-after']) || attempt * 10;
            const waitMs = Math.min(waitS * 1000, Math.max(remainingMs(), 0));
            log.warning(`Federal Register API returned ${resp.statusCode}; retrying in ${Math.round(waitMs / 1000)}s (${attempt}/4).`);
            if (state) { state.lastError = `HTTP ${resp.statusCode}`; state.lastErrorStatus = resp.statusCode; }
            await sleep(waitMs);
            continue;
        }
        let parsed = null;
        try { parsed = JSON.parse(resp.body); } catch { /* handled below */ }
        if (resp.statusCode !== 200) {
            // An unknown agency slug is a 400, not an empty result set — verified live.
            const detail = parsed?.errors ? JSON.stringify(parsed.errors) : String(resp.body).slice(0, 300);
            log.warning(`Federal Register API ${resp.statusCode}: ${detail}`);
            if (state) { state.lastError = `HTTP ${resp.statusCode}: ${detail.slice(0, 120)}`; state.lastErrorStatus = resp.statusCode; }
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
// against the official agency list first (473 agencies, live-checked 2026-09-26) by slug, name or short name.
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

const rawAgencies = (input.agencies ?? []).map((a) => String(a).trim()).filter(Boolean);
const { slugs: agencySlugs, unknown: unknownAgencies } = await resolveAgencies(rawAgencies);
// Verified live (cycle 2355): dropping the agency filter entirely does not return zero rows, it
// returns EVERY document in the date window -- the default 90-day window alone has ~6,381 rows
// vs ~216 for a single real agency (EPA), a ~30x widening. Unlike the partial-miss case below
// (kept and warned, since the rest of the list still narrows the query correctly), letting EVERY
// value fail silently selects a materially different, much larger result set and charges for it
// in full under PPE pricing -- the only warning for this is the log-only one just below, which a
// buyer never sees. Same shape as the nih-reporter-scraper `fiscalYears` and clinicaltrials-scraper
// `nctIds` bugs (c2352/c2353): throw before any charge happens instead of silently widening.
if (rawAgencies.length && !agencySlugs.length) {
    // Actor.fail() (not a bare throw) so the Console's statusMessage actually carries this reason --
    // a bare throw lands only in the run log as a stack trace (verified empty statusMessage on the
    // sibling sam-gov-opportunities-scraper fix's own FAILED run, cycle 2357).
    // `agencies` is a stringList with no maxLength/item-count cap (same gap as unknownAgencyNote()
    // below), so the echoed list is capped independently and the remediation -- the only
    // actionable part -- is RESERVED as a clampStatusMessage suffix (c2442), not just appended
    // after Apify's own silent 500-char cut.
    await Actor.fail(clampStatusMessage(
        `None of the agenc(ies) you listed could be matched: ${echoCap(unknownAgencies.join(', '), 60)}.`,
        ' Running anyway would silently drop the agency filter and search the ENTIRE Federal Register instead '
        + '(no agency restriction at all), charging you for unrelated documents under a filter that looks '
        + "honored but was not. Use the slug from a federalregister.gov/agencies/<slug> URL, or the agency's "
        + 'full name.',
    ));
}
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
    if (presidentialDocumentTypes.length) p['conditions[presidential_document_type][]'] = presidentialDocumentTypes;
    if (searchQuery) p['conditions[term]'] = searchQuery;
    if (significantOnly) p['conditions[significant]'] = 1;
    // "Comment period still open" = a closing date on or after today IN EASTERN TIME, because
    // that is the clock the deadline itself runs on (11:59 p.m. ET). See the etDay() note above:
    // using the UTC day here dropped every document closing on the current ET day for any run
    // between 00:00 and 04:00 UTC -- 15-35 real documents a day, and the most urgent ones.
    if (commentsOpenOnly) p['conditions[comment_date][gte]'] = etDay(today);
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
    presidentialDocumentTypes: [...presidentialDocumentTypes].sort(),
    agencies: [...agencySlugs].sort(),
    searchQuery,
    significantOnly,
    commentsOpenOnly,
    cfrTitle,
    cfrPart,
    // explicit-only, see above
    publicationDateFrom: normDate(input.publicationDateFrom, null, 'publicationDateFrom'),
    publicationDateTo: normDate(input.publicationDateTo, null, 'publicationDateTo'),
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

// A fixed publicationDateTo caps the watch's own match set at a date that gets more stale every
// day the schedule runs. `publication_date` is immutable once assigned (same fact the comment
// above `extractCitations` verified live: a correction ships as a brand-new document, never an
// edit to the original's own publication_date) and a NEW document entering the feed is always
// dated the current-or-a-just-announced day, never earlier -- verified live 2026-10-11:
// `conditions[publication_date][lte]=2026-09-01` maxes out exactly at publication_date 2026-09-01,
// while the real unbounded feed's newest document that same day was dated 2026-10-13. So once
// today's Eastern date passes a fixed publicationDateTo, this watch can never see a new document
// again -- while the pushed===0 branch below keeps emitting the reassuring "nothing new" message
// forever (the 1556 monitor rule: the buyer schedules it and stops looking). Public Inspection
// already drops publicationDateTo with its own "ignored" warning above, so it is excluded here.
// Advisory only: publicationDateTo defaults to today's date on every run when left unset, which is
// the common case and is unaffected -- this only fires when the buyer pins it to a fixed date.
const watchDeadDateBound = watchMode && !publicInspection && watchCriteria.publicationDateTo != null;
if (watchDeadDateBound) {
    log.warning(
        `watchLabel "${watchLabel}" is combined with a fixed publicationDateTo (${watchCriteria.publicationDateTo}). `
        + "Once today's Eastern date passes that cutoff, no document can ever have a publication_date on or before "
        + 'it anymore, so this watch is now permanently unable to report anything new.',
    );
    log.warning(
        'Drop publicationDateTo from a watched query so each run defaults it to "today", or remove watchLabel if '
        + 'you really do want a fixed historical window instead of an ongoing watch.',
    );
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
const decodeEntitiesOnce = (s) => String(s).replace(/&(#x[0-9a-fA-F]+|#\d+|[a-zA-Z][a-zA-Z0-9]{1,9});/g, (m, e) => {
    if (e[0] === '#') {
        const cp = e[1] === 'x' || e[1] === 'X' ? parseInt(e.slice(2), 16) : parseInt(e.slice(1), 10);
        return Number.isFinite(cp) && cp > 0 && cp <= 0x10ffff ? String.fromCodePoint(cp) : m;
    }
    const key = e.toLowerCase();
    return Object.prototype.hasOwnProperty.call(ENTITIES, key) ? ENTITIES[key] : m; // unknown: verbatim
});
// cycle 1607: decode to a fixpoint, same reason as grants-gov-scraper (cycle 1606) — a single
// pass only resolves one layer, and a tag hidden behind entity-encoding (e.g. `&amp;lt;INF&amp;gt;`)
// would never have been stripped because strip ran first. No double-encoded row has been observed
// here yet (cycle 560's 1000-doc sample was single-layer), but the fix is defensive and free.
const decodeEntities = (s) => {
    let prev = String(s);
    for (let i = 0; i < 5; i += 1) {
        const next = decodeEntitiesOnce(prev);
        if (next === prev) break;
        prev = next;
    }
    return prev;
};
// Plain-text cleanup for one free-text field: decode entities (to a fixpoint) FIRST so any
// entity-hidden tag becomes a real tag, THEN drop markup, then collapse whitespace.
const cleanText = (v) => {
    if (v == null || v === '') return null;
    const decoded = decodeEntities(String(v));
    const stripped = decoded.replace(/<\/?([a-zA-Z][a-zA-Z0-9]*)(?:\s[^<>]*)?\/?>/g,
        (m, tag) => (INLINE_TAGS.has(tag.toLowerCase()) ? '' : ' '));
    return stripped.replace(/\s+/g, ' ').trim() || null;
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

// order="executive_order_number" is a real, working sort key the API accepts but only assigns to
// Executive Orders. Verified live (cycle 830/991): every non-EO row -- and even a "Correction" row
// filed against an EO -- comes back with a null executive_order_number, so outside the narrow scope
// below the sort degenerates to whatever arbitrary tiebreak the API applies to a tied null key
// (reproduced: an unscoped query returned rows from four different decades in one "sorted" page).
if (!publicInspection && order === 'executive_order_number'
    && !(documentTypes.length === 1 && documentTypes[0] === 'PRESDOCU'
        && presidentialDocumentTypes.length === 1 && presidentialDocumentTypes[0] === 'executive_order')) {
    log.warning(
        'order="executive_order_number" only sorts meaningfully within the Executive Order subset -- '
        + 'every other document (including non-EO presidential documents and corrections filed against '
        + 'an EO) has no EO number and the sort is effectively arbitrary for them. Set '
        + 'documentTypes=["PRESDOCU"] and presidentialDocumentTypes=["executive_order"] for a clean '
        + 'ascending walk by EO number.',
    );
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
        presidentialDocumentTypes.length ? 'presidentialDocumentTypes' : null,
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
        + (presidentialDocumentTypes.length ? ` presidentialDocumentTypes=[${presidentialDocumentTypes.join(',')}]` : '')
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

// STATUS_MESSAGE_MAX/clampStatusMessage/echoCap moved above Actor.init() (c2442) so the input-
// validation Actor.fail() near the top of the file can use them too -- see that declaration for
// the full rationale. This Actor has 5 setStatusMessage call sites plus 2 Actor.fail() sites that
// all need the same reservation.

// Empty unless WATCH_KEEP actually dropped something, so it can never add noise to a healthy run.
function truncationNote() {
    if (baselineTruncated <= 0) return '';
    return ` WARNING: the baseline hit its ${WATCH_KEEP}-entry cap and ${baselineTruncated} oldest id(s) were`
        + ' dropped -- those will be delivered and charged again as "new". Narrow the query or split it across labels.';
}

// Empty unless some (not all -- that throws above, before any charge) of the agencies list failed
// to match. Previously this only ever reached a `log.warning` (console-only, not buyer-visible) on
// every path including a delivering run -- this surfaces it on the actual statusMessage instead.
// `agencies` is a stringList with no maxLength and no item-count cap, so the joined list is capped
// via echoCap: an unresolved list alone can otherwise run past the whole 500-char budget before
// truncationNote even joins.
function unknownAgencyNote() {
    if (!unknownAgencies.length) return '';
    return ` NOTE: ${unknownAgencies.length} agency value(s) you listed could not be matched and were ignored `
        + `(not guessed at): ${echoCap(unknownAgencies.join(', '), 60)}.`;
}

// A SEED walk cut short by an upstream error must save NOTHING (h287, 3rd variant, first fixed
// on eu-ted-tenders-scraper cycle 680): saving the partial id set as the baseline would make the
// first incremental run treat every document past the failure point as "new" and charge for it.
// A seed charges nothing, so re-seeding later is free -- unlike an incremental run, there is
// nothing lost by not persisting here.
if (watchMode && seeding && runState.failed) {
    const isInputError = INPUT_ERROR_STATUS.has(runState.lastErrorStatus);
    log.warning(
        `Baseline walk for watch label "${watchLabel}" was cut short (${runState.lastError ?? 'unknown API error'}), `
        + 'so NO baseline was saved. A partial baseline would have caused every document past the stopping '
        + `point to be delivered and charged as "new" on your next run. ${isInputError
            ? 'This is the Federal Register API rejecting the input itself -- fix the filter values and re-run.'
            : 'Re-run the same label and filters once the source recovers.'}`,
    );
} else if (watchMode) {
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
        await Actor.setStatusMessage(clampStatusMessage(
            `Baseline run for watch label "${watchLabel}": ${watchSeen.size} existing document(s) recorded, 0 charged. Run again later to get only what's new.`,
            truncationNote()
            + unknownAgencyNote()
            + (watchDeadDateBound ? ' NOTE: publicationDateTo is fixed, so this watch will stop finding anything new once today passes that date -- see the warning above.' : ''),
        ));
    } else {
        log.info(
            `Watch label "${watchLabel}": ${pushed} new document(s) since the last run `
            + `(${skippedSeen} already-delivered row(s) skipped, uncharged); baseline now holds ${watchSeen.size}.`,
        );
        if (pushed > 0 && (baselineTruncated > 0 || unknownAgencies.length)) {
            // A run that delivered rows would otherwise leave the default status message in
            // place and the truncation/unknown-agency note would only be visible in the log.
            await Actor.setStatusMessage(clampStatusMessage(`Watch label "${watchLabel}": ${pushed} document(s) delivered.`, truncationNote() + unknownAgencyNote()));
        }
    }
}

if (pushed === 0 && watchMode && !seeding) {
    log.warning(
        `Nothing new for watch label "${watchLabel}" since its last run — all ${skippedSeen} matching document(s) `
        + 'had already been delivered. That is the expected result most of the time; you were charged for nothing.',
    );
    await Actor.setStatusMessage(clampStatusMessage(
        `Nothing new for watch label "${watchLabel}" since its last run -- every matching document had already been delivered. That is the expected result most of the time; you were charged for nothing.`,
        truncationNote()
        + unknownAgencyNote()
        + (watchDeadDateBound ? ' NOTE: publicationDateTo is fixed on this watch, so "nothing new" may mean the date cutoff has made it permanently blind rather than the normal quiet result -- see the warning above.' : ''),
    ));
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
        + '(3) significantOnly is overwhelmingly rules and proposed rules — Notices are a rare but real match '
        + '(about 6-16 a year, verified live), so a zero result there over a short date window is most likely '
        + 'cause (2), not this. documentTypes limited to PRESDOCU alone throws before reaching this message. '
        + '(4) an agency value that was not recognised is dropped with a warning above, not guessed at. '
        + '(5) cfrTitle/cfrPart is an AND with every other filter — a narrow CFR part combined with '
        + 'a short date window or a significantOnly flag often has zero real matches. '
        + '(6) commentsOpenOnly adds a SEPARATE AND condition (comment period still open as of today) on top of '
        + 'publicationDateFrom/To — most comment periods close within 30-90 days of publication, so pairing '
        + 'commentsOpenOnly with a publication-date window more than a couple of months in the past often has '
        + 'few or zero real matches even though the window itself is correct (verified live: a 1,003-document '
        + 'window from ~90 days ago narrowed to 3 with commentsOpenOnly). presidentialDocumentTypes set without '
        + 'PRESDOCU in documentTypes throws before reaching this message.',
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
        markIncomplete(
            timeBudgetExceeded ? 'time-budget' : 'source-error',
            `baseline seed API error: ${runState.lastError ?? 'unknown'}`,
        );
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
        markIncomplete(
            timeBudgetExceeded ? 'time-budget' : 'source-error',
            `API error: ${runState.lastError ?? 'unknown'}`,
        );
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
    watchDeadDateBound: watchMode ? watchDeadDateBound : null,
};
await Actor.setValue('RUN_SUMMARY', runSummary);

// A short run still SUCCEEDS (the rows it did get are real and already charged), so the status
// message is the only place the Apify console itself shows the shortfall. There was no
// setStatusMessage call anywhere in this Actor before cycle 654.
if (!complete) {
    await Actor.setStatusMessage(clampStatusMessage(
        seeding
            ? `Baseline INCOMPLETE: ${watchSeen.size.toLocaleString('en-US')} document(s) recorded — ${incompleteReason}`
              + `${incompleteDetail ? ` (${incompleteDetail})` : ''}. Re-seed before scheduling, or the rest will be charged as new. See RUN_SUMMARY.`
            : `Incomplete: ${pushed.toLocaleString('en-US')} document(s) delivered — ${incompleteReason}`
              + `${incompleteDetail ? ` (${incompleteDetail})` : ''}. See RUN_SUMMARY for details.`,
        unknownAgencyNote(),
    ));
} else if (!watchMode && pushed > 0 && unknownAgencies.length) {
    // The only remaining gap: an ordinary (non-watch) run that completed cleanly and delivered
    // rows had no status-message branch at all before this -- `unknownAgencies` only ever
    // reached bullet (4) of the pushed===0 cause list above, never a delivering run.
    await Actor.setStatusMessage(clampStatusMessage(`Pushed ${pushed.toLocaleString('en-US')} document(s).`, unknownAgencyNote()));
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

// Deferred to the very last statement on purpose (h287): failing any earlier would skip the
// RUN_SUMMARY write and the webhook above. Nothing was charged this run (a seed pushes no
// rows), so failing is free -- and failing loudly, instead of exiting 0 with an unsaved
// baseline, stops a scheduled run from quietly reading "seeded" and moving on to incremental.
if (watchMode && seeding && runState.failed) {
    const isInputError = INPUT_ERROR_STATUS.has(runState.lastErrorStatus);
    // Measured at 511 chars under a full-length upstream detail (c2437) -- the silent 500-char cut
    // landed inside the "No baseline was saved / nothing was charged" disclosure and the
    // remediation clause. Both are reserved as the clampStatusMessage suffix (c2442); the upstream
    // detail (already capped at 120 chars on the HTTP-body paths, see `lastError` assignments
    // above) is the base that truncates first if anything still has to give.
    await Actor.fail(clampStatusMessage(
        `The watch baseline could not be completed: ${runState.lastError ?? 'unknown API error'}.`,
        ' No baseline was saved (a partial one would cause you to be charged twice for the same documents '
        + `later) and nothing was charged. ${isInputError
            ? 'This is the Federal Register API rejecting your input (e.g. an unrecognised agency, CFR title or '
                + 'document type) — re-running with the same input will fail the same way; fix the filter values '
                + 'above and re-run.'
            : 'Please re-run in a few minutes.'}`,
    ));
}

await Actor.exit();
