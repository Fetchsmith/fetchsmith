import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';
import { createHash } from 'node:crypto';

await Actor.init();
const input = (await Actor.getInput()) ?? {};

// Grants.gov's own internal search API (no API key, no auth). It is POST + JSON body, unlike
// Federal Register / ClinicalTrials.gov which are both GET — do not reuse a GET helper here.
const API = 'https://api.grants.gov/v1/api';

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// "The API answered and the answer was nothing" and "we never got an answer" both used to
// leave this file as a bare `null`, and every caller below treated them identically: an empty
// search page ended the paging walk as if it were the last page, and a failed detail lookup
// produced a thin row indistinguishable from an opportunity that genuinely has no detail
// record. Recording WHY each null happened is what makes the completeness reporting at the end
// of the run possible.
let lastApiFailure = null;
const apiFail = (reason) => { lastApiFailure = reason; return null; };

// Verified live (cycle 124/125): this API NEVER returns an HTTP error status or a non-zero
// errorcode for a bad parameter or a typo'd enum -- it returns errorcode 0, "Webservice
// Succeeds", and a silently empty (hitCount: 0) result set. There is nothing to catch a mistake,
// so every enum-shaped input below is either constrained by the input schema itself (Apify
// validates enums server-side before the Actor even runs) or resolved against a live value list
// in this file. Only network/5xx failures are retried here.
async function apiPost(path, body) {
    let lastTransport = 'unknown transport failure';
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
            lastTransport = `network error: ${err.message}`;
            await sleep(attempt * 2000);
            continue;
        }
        if (resp.statusCode === 429 || resp.statusCode >= 500) {
            const waitS = Number(resp.headers['retry-after']) || attempt * 5;
            log.warning(`Grants.gov returned ${resp.statusCode}; retrying in ${waitS}s (${attempt}/4).`);
            lastTransport = `HTTP ${resp.statusCode}`;
            await sleep(waitS * 1000);
            continue;
        }
        let parsed = null;
        try { parsed = JSON.parse(resp.body); } catch { /* handled below */ }
        if (resp.statusCode !== 200 || !parsed) {
            log.warning(`Grants.gov ${path} returned ${resp.statusCode}, non-JSON or unexpected body: ${String(resp.body).slice(0, 200)}`);
            return apiFail(`HTTP ${resp.statusCode}${parsed ? '' : ', non-JSON body'}`);
        }
        lastApiFailure = null;
        return parsed;
    }
    log.warning(`Grants.gov ${path} kept failing after 4 attempts; stopping early.`);
    return apiFail(`${lastTransport} (4 attempts)`);
}

const keyword = String(input.keyword ?? '').trim();
const oppStatuses = (Array.isArray(input.oppStatuses) && input.oppStatuses.length ? input.oppStatuses : ['forecasted', 'posted']).join('|');
const eligibilities = (input.eligibilities ?? []).join('|');
const fundingCategories = (input.fundingCategories ?? []).join('|');
const fundingInstruments = (input.fundingInstruments ?? []).join('|');
const cfda = String(input.cfda ?? '').trim();
const oppNum = String(input.oppNum ?? '').trim();
// Batch form of the same lookup, e.g. to enrich a list of opportunity numbers a buyer already
// has. Verified live (curl) before coding: Grants.gov's oppNum param does NOT accept a
// pipe/comma-joined list of numbers the way oppStatuses/agencies/etc. do -- "num1|num2" and
// "num1,num2" both return hitCount:0 -- so a batch lookup MUST be one /search2 call per number,
// not a single joined query. `oppNum` and `oppNums` are merged (deduped) so either or both can
// be set; the single-`oppNum`-only case is byte-identical to before this feature (one entry,
// same API call shape).
const oppNums = Array.from(new Set([oppNum, ...(Array.isArray(input.oppNums) ? input.oppNums : [])]
    .map((v) => String(v ?? '').trim())
    .filter(Boolean)));
const sortBy = String(input.sortBy ?? '');
const maxResults = Math.min(Math.max(Number(input.maxResults ?? 100), 1), 20000);
const watchLabel = String(input.watchLabel ?? '').trim();
const watchChanges = Boolean(input.watchChanges);

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

// Verified live: dateRange takes any positive integer number of days (not just the 3/7/14/...
// preset buttons the site's own facet list advertises -- dateRange:"10" returned a real
// in-between count), but like every other param on this API a garbage value is never rejected,
// just silently matches nothing. Validate client-side rather than trust the platform's plain
// "integer" schema type (a caller could still post a negative number via a raw API call).
let postedWithinDays = null;
if (input.postedWithinDays !== undefined && input.postedWithinDays !== null && input.postedWithinDays !== '') {
    const n = Number(input.postedWithinDays);
    if (Number.isFinite(n) && n >= 1) postedWithinDays = Math.floor(n);
    // Throws rather than warns (cycle 591), same reason as parseIsoDate below: this branch only
    // runs when the caller explicitly set a value, and ignoring it leaves NO date filter at all,
    // so the run would return (and bill for) the whole unfiltered set the caller was narrowing.
    else throw new Error(`"postedWithinDays" is not a valid day count: "${input.postedWithinDays}". Use a positive whole number of days (e.g. 7). The run stops instead of ignoring it, because dropping the window would return every matching opportunity and charge you for the difference.`);
}

// Grants.gov's API has no absolute-date filter at all (verified live: posting a
// postedFromDate/postedToDate body param is silently dropped, not echoed back in
// searchParams and not applied). openDate is already present on every thin search2 row
// though (even archived ones), so an absolute range is applied client-side after fetch --
// zero extra requests, same cost as no filter at all. Parsed once here as real Date objects
// so the per-row filter below is a cheap comparison, not a re-parse every iteration.
// A bad date bound THROWS (cycle 591). It used to warn and return null, and null means "no bound"
// everywhere downstream -- so a typo deleted the filter, flipped `hasAbsoluteDateFilter` false
// (silently re-arming postedWithinDays, or leaving no date filter at all), and billed per result
// for the whole unfiltered set. Judge a failed parse by whether ignoring it narrows or widens the
// result set: widening under per-result pricing must stop the run, and a log.warning inside an
// otherwise-successful run is not a fix because nobody reads it.
function parseIsoDate(s, label) {
    if (s === undefined || s === null || s === '') return null;
    const trimmed = String(s).trim();
    if (!trimmed) return null;
    const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(trimmed);
    const d = m ? new Date(Date.UTC(Number(m[1]), Number(m[2]) - 1, Number(m[3]))) : null;
    // Date.UTC does NOT reject an out-of-range month or day, it rolls it over (2024-02-30 becomes
    // March 1, 2024-13-01 becomes 2025-01-01), so the ISO round-trip back to the input string is
    // the check that actually catches a calendar-invalid date.
    if (!m || Number.isNaN(d.getTime()) || d.toISOString().slice(0, 10) !== trimmed) {
        throw new Error(
            `"${label}" is not a valid date: "${trimmed}". Use YYYY-MM-DD (e.g. 2024-01-31). `
            + 'The run stops instead of ignoring the bound, because dropping it would widen the '
            + 'result set to every matching opportunity and charge you for the difference.',
        );
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

// Deadline (close date) range. Same client-side mechanism and the same zero-extra-request cost as
// postedFrom/postedTo -- closeDate is on every thin search2 row too -- but a DIFFERENT missing-value
// story, measured live before writing this: `closeDate` is the empty string (not null, not absent)
// on 100% of `docType:"forecast"` rows (a forecast has no firm deadline yet) AND on a material
// slice of posted ones (18/100 on an unfiltered posted sample -- continuous/rolling announcements,
// RFIs, standing notices). Since the default oppStatuses include forecasted, a naive close-date
// filter would silently delete roughly half the default result set, so rows with no deadline are
// dropped with their own named counter in the final summary rather than folded into the
// postedFrom/postedTo one.
const closeDateFrom = parseIsoDate(input.closeDateFrom, 'closeDateFrom');
const closeDateTo = parseIsoDate(input.closeDateTo, 'closeDateTo');
if (closeDateFrom !== null && closeDateTo !== null && closeDateFrom > closeDateTo) {
    throw new Error(`closeDateFrom (${input.closeDateFrom}) is after closeDateTo (${input.closeDateTo}).`);
}
const hasCloseDateFilter = closeDateFrom !== null || closeDateTo !== null;

// closesWithinDays -- relative convenience filter on top of the absolute closeDateFrom/closeDateTo
// range above, for the common cron use case ("what closes in the next 30 days?") without the buyer
// computing today's date themselves. Resolved to [today, today+N] client-side, same mechanism and
// missing-value handling as closeDateFrom/closeDateTo (they share the same filter loop below), and
// dropped entirely -- same precedence rule as postedWithinDays vs postedFrom/postedTo -- when an
// absolute range is also given, rather than trying to intersect the two.
let closesWithinDays = null;
if (input.closesWithinDays !== undefined && input.closesWithinDays !== null && input.closesWithinDays !== '') {
    const n = Number(input.closesWithinDays);
    if (Number.isFinite(n) && n >= 1) closesWithinDays = Math.floor(n);
    // Throws for the same reason as postedWithinDays above: a dropped deadline window widens the
    // billable result set instead of narrowing it.
    else throw new Error(`"closesWithinDays" is not a valid day count: "${input.closesWithinDays}". Use a positive whole number of days (e.g. 30). The run stops instead of ignoring it, because dropping the window would return every matching opportunity and charge you for the difference.`);
}
if (hasCloseDateFilter && closesWithinDays !== null) {
    log.warning('Both closesWithinDays and closeDateFrom/closeDateTo are set; ignoring closesWithinDays since an absolute range was given.');
    closesWithinDays = null;
}
// Raw day count only goes into the watch fingerprint (see watchCriteria below), never a resolved
// date -- same cycle-297-trap avoidance as postedWithinDays, since "today" moves every run.
const todayUtc = new Date(Date.UTC(new Date().getUTCFullYear(), new Date().getUTCMonth(), new Date().getUTCDate()));
// closesWithinDays is only ever non-null when hasCloseDateFilter is false (nulled out above
// otherwise), so it's safe to treat the two as mutually exclusive here.
const effectiveCloseDateFrom = closesWithinDays !== null ? todayUtc : closeDateFrom;
const effectiveCloseDateTo = closesWithinDays !== null ? new Date(todayUtc.getTime() + closesWithinDays * 86400000) : closeDateTo;
const hasEffectiveCloseDateFilter = effectiveCloseDateFrom !== null || effectiveCloseDateTo !== null;

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
// (cycle 123): when oppNum/oppNums is set, every other filter is dropped and oppStatuses is
// forced to all four values so status can never hide the exact opportunity the user asked for.
const exclusiveOppNum = oppNums.length > 0;

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
    log.warning('watchLabel is ignored when Opportunity number (oppNum) or Opportunity numbers (oppNums) is set -- an exact opportunity-number lookup has no "new since last run" to track.');
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
    // Literal buyer-supplied strings, same as postedFrom/postedTo -- no computed absolute date
    // goes into the fingerprint, so the cycle-297 rolling-default trap does not apply here either.
    closeDateFrom: input.closeDateFrom ? String(input.closeDateFrom).trim() : null,
    closeDateTo: input.closeDateTo ? String(input.closeDateTo).trim() : null,
    closesWithinDays,
    minAwardAmount,
    maxAwardAmount,
};

let watchStore = null;
let watchKey = null;
let watchRecord = null;
let seeding = false;
// opportunity `id` -> last-seen snapshot of the fields that can change on an otherwise-
// already-delivered opportunity: closing date (deadline amendment), docType (forecast turning
// into a real posted opportunity), oppStatus (posted -> closed/archived/withdrawn early),
// awardCeiling/awardFloor (funding range revised) and lastUpdatedDate (Grants.gov's own
// "something on this synopsis/forecast changed" timestamp -- the generic catch-all for document
// edits we have no more specific field for). closeDate/docType/oppStatus are thin fields, always
// present regardless of `enrich`, so tracking them costs no extra API calls; the other 3 (plus
// applicantEligibilityDesc, hashed below) only populate -- and therefore only get watched -- when
// `enrich` is on, which is the default, so this costs no extra calls either in the common case.
// `watchChanges` decides whether a change re-delivers the row; the snapshot itself is always kept
// current so turning watchChanges on later works without a fresh baseline.
const watchSeen = new Map();
let changedCount = 0;
let baselineTruncated = 0;
let baselineTruncatedTotal = 0;

function truncationNote() {
    return baselineTruncated > 0
        ? ` (baseline cap: ${baselineTruncated} old id(s) dropped this run, ${baselineTruncatedTotal} total -- narrow filters to avoid re-charges)`
        : '';
}

// applicantEligibilityDesc can be a multi-KB free-text field and WATCH_KEEP persists up to 60,000
// snapshots in one KV record, so the full text is never stored -- only an 8-char md5 fingerprint,
// enough to detect that the text changed without risking the record's size budget.
function eligHashOf(desc) {
    return desc ? createHash('md5').update(desc).digest('hex').slice(0, 8) : null;
}

function snapshotOf(item) {
    return {
        closeDate: item.closeDate ?? null,
        docType: item.docType ?? null,
        oppStatus: item.oppStatus ?? null,
        awardCeiling: typeof item.awardCeiling === 'number' ? item.awardCeiling : null,
        awardFloor: typeof item.awardFloor === 'number' ? item.awardFloor : null,
        lastUpdatedDate: item.lastUpdatedDate ?? null,
        eligHash: eligHashOf(item.applicantEligibilityDesc),
    };
}

// A changed opportunity is re-delivered with these fields describing exactly what moved, so a
// buyer doesn't have to diff the row against their own last-seen copy to find out. eligHash is
// compared separately since its "previous" value (a hash) isn't meaningful to show a buyer.
function changesBetween(prev, next) {
    if (!prev) return null;
    const types = [];
    const previous = {};
    for (const field of ['closeDate', 'docType', 'oppStatus', 'awardCeiling', 'awardFloor', 'lastUpdatedDate']) {
        if (prev[field] !== undefined && prev[field] !== null && prev[field] !== next[field]) {
            types.push(field);
            previous[field] = prev[field];
        }
    }
    if (prev.eligHash !== undefined && prev.eligHash !== null && prev.eligHash !== next.eligHash) {
        types.push('applicantEligibilityDesc');
        previous.applicantEligibilityDesc = '(changed; only a fingerprint of the eligibility text is retained, not the previous text)';
    }
    return types.length ? { types, previous } : null;
}

async function saveWatchRecord(status) {
    const all = Array.from(watchSeen.entries());
    const entries = all.slice(-WATCH_KEEP);
    baselineTruncated = all.length - entries.length;
    if (baselineTruncated > 0) {
        baselineTruncatedTotal = (watchRecord.truncatedTotal ?? 0) + baselineTruncated;
        log.warning(
            `Watch label "${watchLabel}": baseline holds ${all.length} opportunity id(s), over the ${WATCH_KEEP}-id `
            + `cap -- the oldest ${baselineTruncated} were dropped and will look like NEW (billable) opportunities the `
            + 'next time this label runs, even though they were already delivered. Narrow the filters (a keyword, '
            + 'agency, or date window) so the whole match set fits under the cap.',
        );
    } else {
        baselineTruncatedTotal = watchRecord.truncatedTotal ?? 0;
    }
    await watchStore.setValue(watchKey, {
        ...watchRecord,
        label: watchLabel,
        criteria: watchCriteria,
        lastRunAt: new Date().toISOString(),
        lastRunStatus: status,
        seenCount: entries.length,
        truncatedLastRun: baselineTruncated,
        truncatedTotal: baselineTruncatedTotal,
        // Compact per-entry shape: id, closeDate, docType, oppStatus, awardCeiling, awardFloor,
        // lastUpdatedDate, eligHash. Kept as short keys because WATCH_KEEP can hold up to 60,000
        // of these in one KV record; eligHash is already an 8-char fingerprint, not the full text.
        seenIds: entries.map(([id, snap]) => ({
            i: id, c: snap.closeDate, d: snap.docType, s: snap.oppStatus,
            ac: snap.awardCeiling, af: snap.awardFloor, lu: snap.lastUpdatedDate, eh: snap.eligHash,
        })),
        runCount: (watchRecord.runCount ?? 0) + 1,
    });
}

if (watchMode) {
    watchStore = await Actor.openKeyValueStore(WATCH_STORE);
    const { key, fingerprint } = watchKeyFor(watchLabel, watchCriteria);
    watchKey = key;
    const existing = await watchStore.getValue(key);
    if (existing && Array.isArray(existing.seenIds)) {
        watchRecord = existing;
        // Pre-change-tracking records stored `seenIds` as a flat array of id strings (or
        // numbers), and records from before the funding/eligibility/lastUpdatedDate fields
        // existed only carry `c`/`d`/`s` -- both handled here so an existing buyer's baseline
        // keeps working unchanged instead of needing a fresh seed each time this feature grows.
        // Missing fields simply have no snapshot yet (nulls/undefined), so watchChanges only
        // starts detecting changes on those fields from here on, same pattern as the original.
        for (const entry of existing.seenIds) {
            if (entry && typeof entry === 'object') {
                watchSeen.set(String(entry.i), {
                    closeDate: entry.c ?? null, docType: entry.d ?? null, oppStatus: entry.s ?? null,
                    awardCeiling: typeof entry.ac === 'number' ? entry.ac : null,
                    awardFloor: typeof entry.af === 'number' ? entry.af : null,
                    lastUpdatedDate: entry.lu ?? null,
                    eligHash: entry.eh ?? null,
                });
            } else {
                watchSeen.set(String(entry), {
                    closeDate: null, docType: null, oppStatus: null,
                    awardCeiling: null, awardFloor: null, lastUpdatedDate: null, eligHash: null,
                });
            }
        }
        log.info(
            `Watch mode "${watchLabel}" (${key}): baseline from ${existing.lastRunAt ?? 'an earlier run'} holds `
            + `${watchSeen.size} already-delivered opportunity(ies). Only opportunities NOT in that baseline are returned and charged`
            + (watchChanges ? ', plus any already-delivered opportunity whose closing date, forecast/posted status, opportunity status, award ceiling/floor, last-updated date or eligibility text changed.' : '.'),
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
    // exclusiveOppNum never reaches here -- it uses walkOppNums (one /search2 call per number,
    // since the API has no batch/joined form), not this filtered-search path.
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

// Grants.gov double-encodes its free text: the API returns HTML entities even in fields that
// carry no tags at all. Measured live (cycle 556) on a 10-row enriched sample: 131 entities,
// `&nbsp;` x120 plus `&amp;`/`&rsquo;`/`&ldquo;`/`&rdquo;`, and ZERO tags in synopsisText /
// applicantEligibilityDesc. stripHtml removed tags but never decoded, so every enriched row has
// been shipping `&nbsp;` noise into a field the README documents as plain prose. Decode after
// tag removal, before the whitespace collapse, so a decoded `&nbsp;` folds into normal spacing.
const ENTITIES = {
    nbsp: ' ', amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", ndash: '–', mdash: '—',
    rsquo: '’', lsquo: '‘', ldquo: '“', rdquo: '”', hellip: '…',
    bull: '•', middot: '·', deg: '°', reg: '®', copy: '©', trade: '™',
};
const decodeEntities = (s) => String(s).replace(/&(#x[0-9a-fA-F]+|#\d+|[a-zA-Z][a-zA-Z0-9]{1,9});/g, (m, e) => {
    if (e[0] === '#') {
        const cp = e[1] === 'x' || e[1] === 'X' ? parseInt(e.slice(2), 16) : parseInt(e.slice(1), 10);
        // Reject non-characters/out-of-range rather than throwing out of String.fromCodePoint.
        return Number.isFinite(cp) && cp > 0 && cp <= 0x10ffff ? String.fromCodePoint(cp) : m;
    }
    const key = e.toLowerCase();
    return Object.prototype.hasOwnProperty.call(ENTITIES, key) ? ENTITIES[key] : m; // unknown entity: leave verbatim
});
// Plain-text cleanup for a free-text field: drop tags, decode entities, collapse whitespace.
const cleanText = (v) => (v ? decodeEntities(String(v).replace(/<[^>]+>/g, ' ')).replace(/\s+/g, ' ').trim() || null : null);
const stripHtml = cleanText;
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
        title: cleanText(row.title),
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
// live detail response before writing this function: the detail API's synopsis/forecast
// .agencyName / .agencyPhone / .agencyAddressDesc / .agencyContactName / .agencyContactPhone /
// .agencyContactDesc / .agencyContactEmail / .agencyContactEmailDesc, and the top-level
// publisherUid, are agency-entered free text that is INCONSISTENT -- sometimes a department name
// (NSF), sometimes a named individual program officer with a direct phone/email ("Andrew Day,
// Grants/Agreements Officer", verified live on opportunity 332894; forecast opportunity 355824
// carries the identical field names with a named "Stacey Williams" + direct phone/email too).
// Because it cannot be reliably told apart per-row, ALL eight of those fields plus publisherUid
// are dropped entirely, never just filtered -- and since this function never reads them by name
// (from either sub-object below), that holds automatically for forecast rows with no extra code.
// The clean, always-organizational replacement is agencyDetails/topAgencyDetails (code + name),
// which stayed a department/bureau name on every sample checked, synopsis or forecast.
//
// `sub` is `detail.synopsis` for a posted/closed/archived opportunity or `detail.forecast` for a
// forecasted one -- verified live (opportunity 355824) that Grants.gov uses the SAME field names
// for postingDate/costSharing/awardCeiling/awardFloor/applicantTypes/fundingInstruments/
// fundingActivityCategories/lastUpdatedDate/modComments on both sub-objects, so one generic read
// covers both docTypes for those fields. Only `responseDate`/`archiveDate`/
// `applicantEligibilityDesc`/`fundingDescLinkUrl` have no forecast equivalent (a forecast has no
// firm deadline or eligibility writeup yet) and stay null on forecast rows; `forecastDesc` maps
// onto the same `synopsisText` output field as `synopsisDesc` since they serve the same purpose
// (the free-text description). Forecast-only fields (estimated dates/funding/award count) are
// additive and null on synopsis rows.
function normalizeEnriched(detail) {
    const isForecast = !detail.synopsis && !!detail.forecast;
    const sub = detail.synopsis ?? detail.forecast ?? {};
    const ad = detail.agencyDetails ?? {};
    const tad = detail.topAgencyDetails ?? {};
    return {
        agencyName: ad.agencyName ?? null,
        agencyCode: ad.agencyCode ?? null,
        topAgencyName: tad.agencyName ?? null,
        topAgencyCode: tad.agencyCode ?? null,
        opportunityCategory: detail.opportunityCategory?.description ?? null,
        postingDate: sub.postingDate ?? null,
        responseDate: sub.responseDate ?? null,
        archiveDate: sub.archiveDate ?? null,
        costSharing: typeof sub.costSharing === 'boolean' ? sub.costSharing : null,
        awardCeiling: parseMoney(sub.awardCeiling),
        awardFloor: parseMoney(sub.awardFloor),
        applicantEligibilityDesc: cleanText(sub.applicantEligibilityDesc),
        applicantTypes: listOf(sub.applicantTypes).map((t) => t.description).filter(Boolean),
        fundingInstruments: listOf(sub.fundingInstruments).map((t) => t.description).filter(Boolean),
        fundingActivityCategories: listOf(sub.fundingActivityCategories).map((t) => t.description).filter(Boolean),
        synopsisText: stripHtml(sub.synopsisDesc ?? sub.forecastDesc),
        cfdas: listOf(detail.cfdas).filter((c) => c.cfdaNumber).map((c) => ({ number: c.cfdaNumber, title: c.programTitle ?? null })),
        fundingDescLinkUrl: sub.fundingDescLinkUrl || null,
        synopsisDocumentURLs: listOf(detail.synopsisDocumentURLs).map((d) => ({ url: d.docUrl ?? null, description: d.description ?? null })).filter((d) => d.url),
        // The actual announcement files (the NOFO PDF/DOCX a grant researcher is really after).
        // Found cycle 624 via check-field-fill: `synopsisDocumentURLs` -- the only document field
        // this Actor shipped -- is filled on just 1/20 live opportunities, but 8/20 carry real
        // attachments under `synopsisAttachmentFolders[].synopsisAttachments[]`, so ~35% of rows
        // were silently losing their full announcement. The two are NOT the same list (opportunity
        // 332894 has one docUrl AND five attachments). Forecast rows use this same key -- there is
        // no `forecastAttachmentFolders` (checked on 8 live forecasts) -- so one read covers both
        // docTypes. The download URL is not in the API response; it is built from the attachment
        // id and was verified live on two files (887,949 B PDF and 57,716 B DOCX, both exactly
        // matching `fileLobSize`). Agency-entered file names/descriptions are document metadata,
        // not personal data, so the PII rule above does not apply to them.
        attachments: listOf(detail.synopsisAttachmentFolders).flatMap((f) => listOf(f.synopsisAttachments).map((a) => ({
            fileName: a.fileName ?? null,
            description: cleanText(a.fileDescription),
            mimeType: a.mimeType ?? null,
            sizeBytes: Number.isFinite(a.fileLobSize) ? a.fileLobSize : null,
            folderName: f.folderName ?? null,
            folderType: f.folderType ?? null,
            postedDate: a.createdDate ?? null,
            downloadUrl: a.id ? `https://www.grants.gov/grantsws/rest/opportunity/att/download/${a.id}` : null,
        }))).filter((a) => a.downloadUrl),
        assistURL: detail.assistURL || null,
        lastUpdatedDate: sub.lastUpdatedDate ?? null,
        modComments: cleanText(sub.modComments),
        // Forecast-only: Grants.gov's own estimate of when the real NOFO posts, the application
        // deadline, the award date, and project start -- all genuinely new information not
        // derivable from anything else on a forecast's thin row. null on synopsis-based rows.
        numberOfAwards: isForecast ? parseMoney(sub.numberOfAwards) : null,
        estimatedFunding: isForecast ? parseMoney(sub.estimatedFunding) : null,
        estSynopsisPostingDate: isForecast ? (sub.estSynopsisPostingDate ?? null) : null,
        estApplicationResponseDate: isForecast ? (sub.estApplicationResponseDate ?? null) : null,
        estAwardDate: isForecast ? (sub.estAwardDate ?? null) : null,
        estProjectStartDate: isForecast ? (sub.estProjectStartDate ?? null) : null,
        fiscalYear: isForecast ? (sub.fiscalYear ?? null) : null,
    };
}

// Detail lookups measured at ~0.35s each; run a small concurrent pool rather than one at a time
// so enrich:true stays usable for a few hundred rows without hammering the API.
//
// BUG FIXED cycle 325: this guard used to require `detail.data.synopsis`, so every
// `docType:"forecast"` row (roughly half of the default oppStatuses=[forecasted,posted] result
// set) silently fell through to the thin fallback below even with enrich:true -- no warning, no
// error, just 11 fields instead of the enriched set, AND (worse) a silent correctness bug in the
// minAwardAmount/maxAwardAmount filter, which requires a numeric awardCeiling that a thin row
// never has, so 100% of forecasts were dropped from any amount-filtered run. Forecasts carry
// `detail.data.forecast` instead of `.synopsis` -- accept either.
// Every element is `{ fields, status }`, never a bare null, because the three ways a row can
// come back without enriched fields are NOT the same thing to a buyer and used to be
// indistinguishable on the row:
//   ok               -- the detail record was fetched and merged
//   no-detail-record -- Grants.gov answered, and has no synopsis/forecast for this id
//                       (archived opportunities); the enriched fields genuinely do not exist
//   fetch-failed     -- we never got an answer (retries exhausted / 5xx / non-JSON). The
//                       enriched fields may well exist; we simply did not get them. An empty
//                       `attachments` here means "not asked", not "no attachments", and a
//                       missing `awardCeiling` here is not evidence the agency set none.
const ENRICH_CONCURRENCY = 5;
let detailFetchFailures = 0;
let detailNoRecord = 0;
async function enrichBatch(rows) {
    const out = new Array(rows.length).fill(null);
    let next = 0;
    async function worker() {
        for (;;) {
            const i = next; next += 1;
            if (i >= rows.length) return;
            const detail = await apiPost('/fetchOpportunity', { opportunityId: rows[i].id });
            if (detail?.data && !detail.data.errorMessages?.length && (detail.data.synopsis || detail.data.forecast)) {
                out[i] = { fields: normalizeEnriched(detail.data), status: 'ok' };
            } else if (detail === null) {
                detailFetchFailures += 1;
                out[i] = { fields: null, status: 'fetch-failed' };
            } else {
                detailNoRecord += 1;
                out[i] = { fields: null, status: 'no-detail-record' };
            }
        }
    }
    await Promise.all(Array.from({ length: Math.min(ENRICH_CONCURRENCY, rows.length) }, worker));
    return out;
}

// A row that never cost us a /fetchOpportunity call is cheaper to serve, so it is cheaper to
// buy: the price forks per row, not per run. `ENRICHED` is a Symbol so the marker can ride on
// the row object itself without ever reaching the dataset (JSON.stringify drops symbol keys,
// and Actor.pushData serializes as JSON). Two ways a row ends up thin: the buyer set
// enrich:false, or enrichment was attempted and Grants.gov had no detail record for it
// (archived opportunities with no synopsis) -- in both cases the buyer gets the 11 thin fields
// and is charged the thin price, never the full one for data we failed to deliver.
const ENRICHED = Symbol('enriched');
const THIN_EVENT = 'opportunity-thin';

let pushed = 0;
let thinCharged = 0;
const isPPE = Actor.getChargingManager().getPricingInfo().isPayPerEvent;
async function pushResult(item) {
    const eventName = item[ENRICHED] ? 'result' : THIN_EVENT;
    // Both of these end the walk with matching opportunities still unvisited, so both are
    // truncation causes the buyer needs named -- `maxResults` is their own choice and benign,
    // the charge limit is not, and until now neither was distinguishable from a finished run.
    const stopNote = () => {
        if (pushed >= maxResults) markIncomplete('max-results', `Stopped at maxResults=${maxResults}; matching opportunities past this point were not returned.`);
    };
    if (isPPE) {
        const r = await Actor.charge({ eventName, count: 1 });
        if (r.chargedCount === 0) {
            markIncomplete('charge-limit', 'Stopped by the run\'s maximum-cost limit before the match set was exhausted; raise it to get the rest.');
            return false;
        }
        if (eventName === THIN_EVENT) thinCharged += 1;
        await Actor.pushData(item); pushed += 1;
        if (r.eventChargeLimitReached) markIncomplete('charge-limit', 'Stopped by the run\'s maximum-cost limit before the match set was exhausted; raise it to get the rest.');
        stopNote();
        return !r.eventChargeLimitReached && pushed < maxResults;
    }
    if (eventName === THIN_EVENT) thinCharged += 1;
    await Actor.pushData(item); pushed += 1;
    stopNote();
    return pushed < maxResults;
}

log.info(
    exclusiveOppNum
        ? `Grants.gov: exact opportunity-number lookup, ${oppNums.length} number(s): ${oppNums.join(', ')} (all statuses, other filters ignored).`
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
        + (closeDateFrom !== null ? ` closeDateFrom=${input.closeDateFrom}` : '')
        + (closeDateTo !== null ? ` closeDateTo=${input.closeDateTo}` : '')
        + (closesWithinDays !== null ? ` closesWithinDays=${closesWithinDays}` : '')
        + (minAwardAmount !== null ? ` minAwardAmount=${minAwardAmount}` : '')
        + (maxAwardAmount !== null ? ` maxAwardAmount=${maxAwardAmount}` : '')
        + (watchMode ? ` watchLabel="${watchLabel}"` : ''),
);
if (minAwardAmount !== null || maxAwardAmount !== null) {
    log.info(
        'Award-amount filtering drops any opportunity with no usable award ceiling: opportunities '
        + '(synopsis or forecast) whose detail record literally has no ceiling set (Grants.gov spells '
        + 'this as the string "none", measured live at roughly a third to half of posted opportunities '
        + 'depending on the agency/category mix) -- a real, common case, not a rare edge case -- plus '
        + 'the rare id with no detail record returned at all.',
    );
}
if (hasEffectiveCloseDateFilter && oppStatuses.split('|').includes('forecasted')) {
    log.warning(
        'closeDateFrom/closeDateTo (or closesWithinDays) is set while "forecasted" is in oppStatuses. '
        + 'A forecast has no firm deadline yet -- Grants.gov returns an empty closeDate on every '
        + 'forecast row -- so ALL forecasts will be dropped by the deadline filter (they are counted '
        + 'separately in the final summary). Drop "forecasted" from oppStatuses to make this explicit.',
    );
}

let scanned = 0;
let droppedNoAward = 0;
let droppedUnknownAward = 0;
let droppedOutOfRange = 0;
let droppedNoCloseDate = 0;
let skippedSeen = 0;

// Run-level completeness, written to the key-value store as RUN_SUMMARY at the end of the run
// (and onto the webhook payload). `complete` is deliberately NOT folded into a status string: a
// run can be perfectly successful AND truncated at the same time -- that is precisely the case
// this record exists to make machine-readable, and collapsing the two loses it.
let declaredMatches = null;
let incompleteReason = null;
let incompleteDetail = null;
function markIncomplete(reason, detail) {
    // First cause wins: it is the one that actually stopped the walk; anything after it is a
    // consequence. A later maxResults stop must not overwrite a real upstream failure.
    if (incompleteReason !== null) return;
    incompleteReason = reason;
    incompleteDetail = detail;
    log.warning(detail);
}

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
        // A failed search page used to arrive as `null`, produce zero hits, and end the walk
        // through the SAME `break` as a genuine last page -- so a 5xx on page 3 of 9 returned a
        // third of the match set, said "Done. Pushed N", and the run SUCCEEDED. In watch seeding
        // that also under-seeds the baseline, and the next incremental run then delivers and
        // CHARGES everything past the failure point as "new".
        if (page === null) {
            markIncomplete('search-request-failed', `Grants.gov search failed at offset ${startRecordNum} (${lastApiFailure}).`);
            break;
        }
        // The upstream's own count of everything that matched, read from the first page only:
        // it is what makes "we delivered 40" checkable against "Grants.gov says 2,113 match".
        if (declaredMatches === null && Number.isFinite(page?.data?.hitCount)) declaredMatches = page.data.hitCount;
        const hits = listOf(page?.data?.oppHits);
        if (!hits.length) break;
        scanned += hits.length;

        const thin = hits.map(normalizeThin);
        let batch = thin;
        if (needsEnrich) {
            const details = await enrichBatch(hits);
            batch = thin.map((row, i) => (details[i].fields
                ? { ...row, ...details[i].fields, enrichment: 'ok', [ENRICHED]: true }
                : { ...row, enrichment: details[i].status }));
        } else {
            batch = thin.map((row) => ({ ...row, enrichment: 'not-requested' }));
        }
        if (minAwardAmount !== null || maxAwardAmount !== null) {
            batch = batch.filter((row) => {
                if (typeof row.awardCeiling !== 'number') {
                    // Two very different reasons, and only one of them is the buyer's filter
                    // doing its job. A row whose detail lookup failed is dropped because we
                    // do not KNOW its ceiling -- counting that as "agency set no ceiling"
                    // would assert a cause we never observed.
                    if (row.enrichment === 'fetch-failed') droppedUnknownAward += 1;
                    else droppedNoAward += 1;
                    return false;
                }
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
        if (hasEffectiveCloseDateFilter && !exclusiveOppNum) {
            batch = batch.filter((row) => {
                const closes = parseUsDate(row.closeDate);
                if (closes === null) { droppedNoCloseDate += 1; return false; }
                if (effectiveCloseDateFrom !== null && closes < effectiveCloseDateFrom) return false;
                if (effectiveCloseDateTo !== null && closes > effectiveCloseDateTo) return false;
                return true;
            });
        }

        keepGoing = await onBatch(batch);
        startRecordNum += hits.length;
        if (hits.length < PAGE_SIZE) break; // last page
    }
}

const notFoundOppNums = [];
const failedOppNums = [];

// Batch form of the exact-number lookup: one /search2 call per number in `oppNums`, since (see
// the note by `oppNums` above) the API has no batch/joined form for this param. Each call is an
// exact-match lookup across all four statuses, same as the single-oppNum path used to run
// through walkMatches -- this reproduces that path's filtering exactly (amount filter still
// applies, date filters never did for an exclusive lookup) so a single oppNum with no oppNums
// set behaves byte-identically to before this feature.
async function walkOppNums(onBatch) {
    const needsEnrich = minAwardAmount !== null || maxAwardAmount !== null ? true : enrich;
    for (const num of oppNums) {
        const page = await apiPost('/search2', {
            resultType: 'json', oppNum: num, oppStatuses: 'forecasted|posted|closed|archived', rows: PAGE_SIZE, startRecordNum: 0,
        });
        // Same distinction as in walkMatches, and it matters more here: "this number had no
        // match" is a claim about Grants.gov's index that a failed request cannot support, and
        // it is reported to the buyer by number in the warning below.
        if (page === null) {
            markIncomplete('search-request-failed', `Lookup of opportunity number ${num} failed (${lastApiFailure}); it is NOT reported as "no match" because we never got an answer.`);
            failedOppNums.push(num);
            continue;
        }
        const hits = listOf(page?.data?.oppHits);
        if (!hits.length) { notFoundOppNums.push(num); continue; }
        scanned += hits.length;

        const thin = hits.map(normalizeThin);
        let batch = thin;
        if (needsEnrich) {
            const details = await enrichBatch(hits);
            batch = thin.map((row, i) => (details[i].fields
                ? { ...row, ...details[i].fields, enrichment: 'ok', [ENRICHED]: true }
                : { ...row, enrichment: details[i].status }));
        } else {
            batch = thin.map((row) => ({ ...row, enrichment: 'not-requested' }));
        }
        if (minAwardAmount !== null || maxAwardAmount !== null) {
            batch = batch.filter((row) => {
                if (typeof row.awardCeiling !== 'number') {
                    // Two very different reasons, and only one of them is the buyer's filter
                    // doing its job. A row whose detail lookup failed is dropped because we
                    // do not KNOW its ceiling -- counting that as "agency set no ceiling"
                    // would assert a cause we never observed.
                    if (row.enrichment === 'fetch-failed') droppedUnknownAward += 1;
                    else droppedNoAward += 1;
                    return false;
                }
                if (minAwardAmount !== null && row.awardCeiling < minAwardAmount) return false;
                if (maxAwardAmount !== null && row.awardCeiling > maxAwardAmount) return false;
                return true;
            });
        }

        const keepGoing = await onBatch(batch);
        if (!keepGoing) break;
    }
}

// Seeding only needs the ids, so (outside an amount filter) it skips enrichment entirely.
// It walks the WHOLE match set, unbounded by maxResults -- a baseline that stopped early would
// report every opportunity past the stopping point as "new" on the first incremental run.
async function seedBaseline() {
    await walkMatches(async (batch) => {
        for (const row of batch) {
            if (row.id != null) watchSeen.set(String(row.id), snapshotOf(row));
            if (watchSeen.size >= SEED_CAP) {
                markIncomplete('seed-cap', `The watch baseline stopped at the ${SEED_CAP}-opportunity cap; opportunities past it would be reported as new on the first incremental run.`);
                return false;
            }
        }
        return true;
    }, { thinOnly: true });
    log.info(`Baseline walk: ${watchSeen.size} opportunity id(s) recorded.`);
}

if (watchMode && seeding) await seedBaseline();

let beforePush = 0;
if (!seeding) {
    const walker = exclusiveOppNum ? walkOppNums : walkMatches;
    await walker(async (batch) => {
        for (const row of batch) {
            // Already delivered under this watch label. Normally dropped before any charge, so
            // an opportunity is never paid for twice -- UNLESS watchChanges is on and its
            // closing date, docType or oppStatus moved since we last saw it, in which case it
            // is re-delivered (charged like a new row) tagged with exactly what changed.
            if (watchMode && row.id != null && watchSeen.has(String(row.id))) {
                const id = String(row.id);
                const nextSnap = snapshotOf(row);
                const change = watchChanges ? changesBetween(watchSeen.get(id), nextSnap) : null;
                if (!change) {
                    // Snapshot is kept current either way, so turning watchChanges on later
                    // detects only drift from that point, not a backlog since the baseline.
                    watchSeen.set(id, nextSnap);
                    skippedSeen += 1;
                    continue;
                }
                const cont = await pushResult({ ...row, _watchChangeType: change.types, _watchPrevious: change.previous });
                if (pushed > beforePush) { watchSeen.set(id, nextSnap); changedCount += 1; }
                beforePush = pushed;
                if (!cont) return false;
                continue;
            }
            const cont = await pushResult(row);
            // Recorded as delivered only after the charge actually succeeded -- anything
            // dropped by maxResults or a charge limit stays "new" for the next run.
            if (watchMode && row.id != null && pushed > beforePush) watchSeen.set(String(row.id), snapshotOf(row));
            beforePush = pushed;
            if (!cont) return false;
        }
        return true;
    });
}

// A seed walk that never got an answer from Grants.gov for one page is not a smaller baseline,
// it is a WRONG one: every opportunity past the failure point would read as "new" (and be
// charged) on the first incremental run. `seed-cap` is deliberately excluded -- that is the
// buyer's own query being too broad, already surfaced in RUN_SUMMARY, and a capped baseline is
// still strictly better than none. Seeding never charges, so refusing to save costs nothing but
// a re-run.
const seedFailure = seeding && incompleteReason === 'search-request-failed' ? incompleteDetail : null;

if (watchMode && seedFailure) {
    log.warning(
        `Baseline walk for watch label "${watchLabel}" was cut short (${seedFailure}), so NO baseline was saved. `
        + 'Re-run with the same watchLabel to seed again once Grants.gov is answering -- saving a truncated baseline '
        + 'would make every opportunity past the failure point look "new" (and billable) on the first incremental run.',
    );
} else if (watchMode) {
    await saveWatchRecord(seeding ? 'seeded' : 'incremental');
    if (seeding) {
        log.info(
            `Baseline saved for watch label "${watchLabel}": ${watchSeen.size} opportunity(ies) recorded as already-seen, `
            + '0 results returned, 0 charged. The next run on this label and these filters returns only new opportunities.'
            + (watchSeen.size >= SEED_CAP
                ? ` NOTE: the baseline stopped at the ${SEED_CAP}-opportunity cap. Narrow the query (a keyword, an `
                + 'agency, a shorter posted-date window) so the whole result set fits, or the first incremental run '
                + 'will report opportunities past the cap as new.'
                : '') + truncationNote(),
        );
    } else {
        log.info(
            `Watch label "${watchLabel}": ${pushed - changedCount} new opportunity(ies)`
            + (watchChanges ? ` and ${changedCount} changed opportunity(ies) (deadline/status/forecast/funding/eligibility/last-updated)` : '')
            + ` since the last run (${skippedSeen} already-delivered, unchanged row(s) skipped, uncharged); baseline now holds ${watchSeen.size}.${truncationNote()}`,
        );
    }
}

if (pushed === 0 && watchMode && !seeding) {
    log.warning(
        `Nothing new for watch label "${watchLabel}" since its last run -- all ${skippedSeen} matching opportunity(ies) `
        + 'had already been delivered. That is the expected result most of the time; you were charged for nothing.',
    );
} else if (pushed === 0 && !seeding && exclusiveOppNum) {
    log.warning(`No opportunity found for any of ${oppNums.length} number(s): ${oppNums.join(', ')}. Check the exact number(s) on grants.gov/search-grants.`);
} else if (pushed === 0 && !seeding) {
    log.warning(
        'No opportunities matched. Most common causes: (1) filters are ANDed -- a narrow '
        + 'keyword plus agency plus eligibility often has zero real matches, drop one and retry; '
        + '(2) oppStatuses defaults to forecasted+posted (open/upcoming only) -- add "closed" or '
        + '"archived" to search history; (3) an unrecognised agency code is dropped with a warning '
        + 'above, not guessed at; (4) postedWithinDays/postedFrom/postedTo are hard AND filters -- a '
        + 'small window plus a narrow keyword can easily have zero real matches; (5) '
        + 'minAwardAmount/maxAwardAmount excludes any row with no detail record at all, not just '
        + 'rows outside the range.',
    );
} else if (exclusiveOppNum && notFoundOppNums.length > 0) {
    // Some numbers matched (pushed > 0) but not all -- a partial batch miss is easy to overlook
    // silently if only the total-pushed count is checked, so it gets its own always-shown line.
    log.warning(`${notFoundOppNums.length} of ${oppNums.length} number(s) had no match: ${notFoundOppNums.join(', ')}. Check the exact number(s) on grants.gov/search-grants.`);
}
if (failedOppNums.length > 0) {
    log.warning(`${failedOppNums.length} of ${oppNums.length} number(s) could not be looked up at all (Grants.gov did not answer): ${failedOppNums.join(', ')}. They are absent from the results but are NOT known to be missing from Grants.gov -- re-run those numbers.`);
}
if (droppedUnknownAward) {
    log.warning(
        `${droppedUnknownAward} row(s) were dropped by the award-amount filter because their detail lookup FAILED, `
        + 'not because the agency set no ceiling. Those opportunities may well be inside your range -- re-run to get them.',
    );
}
if (detailFetchFailures) {
    log.warning(
        `${detailFetchFailures} row(s) carry enrichment:"fetch-failed" -- Grants.gov did not answer their detail lookup, `
        + 'so their synopsis text, award amounts and attachments are missing because we could not ask, not because they '
        + 'are empty. Rows where Grants.gov answered and genuinely has no detail record carry enrichment:"no-detail-record".',
    );
}

// The whole point of this record: everything above is English in a log, and a pipeline reads
// neither. 40 rows against a declared 2,113 matches looks exactly like a complete result set in
// the dataset. Written to the run's key-value store so it is readable with no webhook
// configured: GET /v2/actor-runs/<runId>/key-value-store/records/RUN_SUMMARY
const runSummary = {
    finishedAt: new Date().toISOString(),
    declaredMatches,
    scanned,
    delivered: pushed,
    // A buyer asking "did I get everything that matched?" needs the answer to be a field, not a
    // sentence. Seeding runs deliver 0 rows BY DESIGN, so they are judged on the baseline walk.
    complete: incompleteReason === null,
    incompleteReason,
    incompleteDetail,
    mode: seeding ? 'watch-seed' : (watchMode ? 'watch-incremental' : 'search'),
    enrichedCharged: pushed - thinCharged,
    thinCharged,
    detailFetchFailures,
    detailNoRecord,
    droppedNoAward,
    droppedUnknownAward,
    droppedOutOfRange,
    droppedNoCloseDate,
    skippedSeen,
    // Written down explicitly rather than left out: the ABSENCE of a number from the results
    // would otherwise read as "Grants.gov has no such opportunity", which is the one thing a
    // failed lookup does not prove.
    notFoundOppNums: exclusiveOppNum ? notFoundOppNums : [],
    failedOppNums,
    baselineSize: watchMode ? watchSeen.size : null,
    baselineTruncated: watchMode ? baselineTruncated : null,
    baselineTruncatedTotal: watchMode ? baselineTruncatedTotal : null,
};
await Actor.setValue('RUN_SUMMARY', runSummary);

if (incompleteReason !== null) {
    await Actor.setStatusMessage(
        `INCOMPLETE (${incompleteReason}): delivered ${pushed} row(s)`
        + (declaredMatches !== null ? ` of ${declaredMatches} declared match(es)` : '')
        + `. ${incompleteDetail} See the RUN_SUMMARY key-value record for the machine-readable detail.`,
    );
} else if (baselineTruncated > 0) {
    await Actor.setStatusMessage(
        `Complete, but the watch baseline exceeded its ${WATCH_KEEP}-id cap and dropped ${baselineTruncated} old `
        + `id(s) this run (${baselineTruncatedTotal} total) -- those may be re-delivered and re-charged as "new" `
        + 'on a future run. Narrow the filters to keep the whole match set under the cap.',
    );
}

log.info(
    `Done. Pushed ${pushed} opportunities (scanned ${scanned} rows).`
    + (pushed
        ? ` Charged ${pushed - thinCharged} as enriched "result" and ${thinCharged} at the cheaper "${THIN_EVENT}" rate.`
        : '')
    + (declaredMatches !== null ? ` Grants.gov declared ${declaredMatches} total match(es) for these filters.` : '')
    + (incompleteReason !== null ? ` RESULT IS INCOMPLETE (${incompleteReason}).` : '')
    + (droppedNoAward ? ` Dropped ${droppedNoAward} row(s) whose agency set no award ceiling to compare against the amount filter.` : '')
    + (droppedUnknownAward ? ` Dropped ${droppedUnknownAward} row(s) whose award ceiling is UNKNOWN because their detail lookup failed.` : '')
    + (droppedOutOfRange ? ` Dropped ${droppedOutOfRange} row(s) outside the postedFrom/postedTo range.` : '')
    + (droppedNoCloseDate ? ` Dropped ${droppedNoCloseDate} row(s) with no close date (forecasts and rolling/continuous announcements have none) against the closeDateFrom/closeDateTo filter.` : ''),
);

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
        enrichedCharged: pushed - thinCharged,
        thinCharged,
        watchLabel: watchMode ? watchLabel : null,
        watchNewCount: watchMode && !seeding ? pushed - changedCount : null,
        watchChangedCount: watchMode && !seeding ? changedCount : null,
        // Same object as the RUN_SUMMARY key-value record, so a webhook consumer and a
        // dataset-polling consumer cannot end up with different ideas of what the run delivered.
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

if (watchMode && seedFailure) {
    await Actor.fail(
        `The watch baseline could not be completed: ${seedFailure.replace(/[.\s]*$/, '')}. No baseline was saved `
        + `for watch label "${watchLabel}" -- re-run with the same watchLabel to seed again.`,
    );
}

await Actor.exit();
