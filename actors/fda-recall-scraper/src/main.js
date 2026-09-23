import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';
import { createHash } from 'node:crypto';

await Actor.init();
const input = (await Actor.getInput()) ?? {};

// openFDA publishes recalls as three separate endpoints, one per product type. There is no
// combined endpoint and no API key is required. Each selected type is its own paginated
// query; rows are merged here and tagged with `productType`.
const ENDPOINTS = {
    food: 'https://api.fda.gov/food/enforcement.json',
    drug: 'https://api.fda.gov/drug/enforcement.json',
    device: 'https://api.fda.gov/device/enforcement.json',
};

// Hard API limits, both verified live (cycle 87):
//   limit=1001 -> 400 "Limit cannot exceed 1000 results for search requests."
//   skip=26000 -> 400 "Skip value must 25000 or less."
// The skip cap is why wide queries are re-chunked into date windows instead of paged straight through.
const MAX_LIMIT = 1000;
const MAX_SKIP = 25000;
const CHUNK_THRESHOLD = 24000; // stay under MAX_SKIP with a page of headroom

const CLASSIFICATIONS = ['Class I', 'Class II', 'Class III'];

const productTypes = (input.productTypes ?? ['food', 'drug', 'device'])
    .map((t) => String(t).toLowerCase().trim())
    .filter((t) => Object.hasOwn(ENDPOINTS, t));
if (!productTypes.length) productTypes.push('food', 'drug', 'device');

const classifications = (input.classifications ?? [])
    .map((c) => String(c).trim())
    .filter((c) => CLASSIFICATIONS.includes(c));

const states = (input.states ?? []).map((s) => String(s).trim().toUpperCase()).filter(Boolean);
const countries = (input.countries ?? []).map((c) => String(c).trim()).filter(Boolean);
const recallNumber = String(input.recallNumber ?? '').trim();
const eventId = String(input.eventId ?? '').trim();
const searchQuery = String(input.searchQuery ?? '').trim();
const status = String(input.status ?? '').trim();
const recallingFirm = String(input.recallingFirm ?? '').trim();
const city = String(input.city ?? '').trim();
// Drug-only cross-referenced fields (see the openfda comment near normalize() below) --
// filterable at zero extra cost since openFDA's own search index already carries them.
const brandName = String(input.brandName ?? '').trim();
const genericName = String(input.genericName ?? '').trim();
const manufacturerName = String(input.manufacturerName ?? '').trim();
const VOLUNTARY_MANDATED = ['Voluntary: Firm initiated', 'FDA Mandated'];
const voluntaryMandated = VOLUNTARY_MANDATED.includes(String(input.voluntaryMandated ?? '').trim())
    ? String(input.voluntaryMandated).trim()
    : '';
const maxResults = Math.min(Math.max(Number(input.maxResults ?? 100), 1), 50000);
const includeRiskScore = input.includeRiskScore !== false;
const includePressReleases = Boolean(input.includePressReleases);
const watchLabel = String(input.watchLabel ?? '').trim();
const watchMode = watchLabel.length > 0;
const watchChanges = Boolean(input.watchChanges);

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

// Which date the reportDateFrom/reportDateTo range and the sort both apply to. report_date
// (FDA publication) is the long-standing default; the other two are real distinct fields on
// all three endpoints (verified live: sort and range both work on food/drug/device for all 3).
const DATE_FIELDS = ['report_date', 'recall_initiation_date', 'termination_date'];
const dateField = DATE_FIELDS.includes(String(input.dateField ?? '').trim())
    ? String(input.dateField).trim()
    : 'report_date';

const compactDay = (d) => d.toISOString().slice(0, 10).replace(/-/g, '');
const today = new Date();
// openFDA's oldest enforcement reports are from 2004; 19000101 is a safe open lower bound.
const EARLIEST = '19000101';
const normDate = (v, fallback) => {
    if (v == null || v === '') return fallback;
    const digits = String(v).replace(/[^0-9]/g, '');
    return digits.length === 8 ? digits : fallback;
};
// An exact recallNumber/eventId lookup can be for any date, so default the window to full
// history instead of the usual rolling year -- cheap even though it looks wide, because
// planWindows' first probe carries the same exact-match clause and comes back tiny (verified
// live), never triggering the date-chunking path.
const lookupMode = Boolean(recallNumber || eventId);
const reportDateFrom = normDate(
    input.reportDateFrom,
    lookupMode ? EARLIEST : compactDay(new Date(today.getTime() - 365 * 86400_000)),
);
const reportDateTo = normDate(input.reportDateTo, compactDay(today));

// The FDA press-release RSS feed (see fetchPressReleases below) has none of the structured
// fields openFDA's enforcement API has -- no classification, state/country, firm, NDC, etc,
// and no product-type split (one feed covers food + drug + device recalls together). A filter
// on any of those fields would silently return zero press-release rows every time rather than
// the buyer's intended "narrow the enforcement rows AND also check press releases" -- so instead
// the whole source is skipped with one clear log line naming why, same policy the openFDA side
// already uses for e.g. brandName on a food-only search (see comment near buildSearch()).
const RSS_UNSUPPORTED_REASONS = [];
if (dateField !== 'report_date') RSS_UNSUPPORTED_REASONS.push(`dateField="${dateField}" (the feed only carries a publish date)`);
if (productTypes.length < 3) RSS_UNSUPPORTED_REASONS.push('productTypes (the feed does not separate food/drug/device)');
if (classifications.length) RSS_UNSUPPORTED_REASONS.push('classifications');
if (states.length) RSS_UNSUPPORTED_REASONS.push('states');
if (countries.length) RSS_UNSUPPORTED_REASONS.push('countries');
if (status) RSS_UNSUPPORTED_REASONS.push('status');
if (recallingFirm) RSS_UNSUPPORTED_REASONS.push('recallingFirm');
if (city) RSS_UNSUPPORTED_REASONS.push('city');
if (voluntaryMandated) RSS_UNSUPPORTED_REASONS.push('voluntaryMandated');
if (brandName) RSS_UNSUPPORTED_REASONS.push('brandName');
if (genericName) RSS_UNSUPPORTED_REASONS.push('genericName');
if (manufacturerName) RSS_UNSUPPORTED_REASONS.push('manufacturerName');
if (lookupMode) RSS_UNSUPPORTED_REASONS.push('recallNumber/eventId');
const runPressReleases = includePressReleases && RSS_UNSUPPORTED_REASONS.length === 0;
if (includePressReleases && !runPressReleases) {
    log.warning(
        `includePressReleases is on but was skipped this run: incompatible with ${RSS_UNSUPPORTED_REASONS.join(', ')} `
        + '(the FDA press-release feed does not carry the field(s) needed to apply that filter). Remove the filter, '
        + 'or turn includePressReleases off, to stop seeing this warning.',
    );
}

// ---------------------------------------------------------------------------
// Watch mode: "only what is new since my last run", per saved query. Same shape as
// grants-gov-scraper (cycle 298) / federal-register-scraper (cycle 297) / nih-reporter-scraper
// (cycle 296) -- copy that design, don't reinvent it.
//
// The baseline is the buyer's own -- the recalls this label has already delivered -- kept in a
// NAMED key-value store on the buyer's own account (the default KV store is per-run and would
// reset the baseline every run, i.e. re-charge the whole result set on every scheduled run).
const WATCH_STORE = 'fetchsmith-fda-recall-watch';
const SEED_CAP = 20000; // our own bound on a seed walk's runtime, not a server limit
const WATCH_KEEP = 60000; // bound the record size; oldest ids fall off first

// reportDateFrom/reportDateTo default to a ROLLING window (last 365 days / today, both computed
// from `today` above) -- this is exactly the federal-register-scraper trap (cycle 297):
// fingerprinting the *resolved* dates would hand a scheduled daily watch a fresh baseline every
// single day (seeding forever, delivering nothing, looking healthy in the log the whole time).
// The fix is the same: fingerprint the buyer's raw input (or null if they left it as the rolling
// default), never the value `normDate()` resolved it to. A sliding default window naturally
// admitting newly-in-range recalls as "new" on a later run is correct watch behaviour, not a bug.
const watchCriteria = {
    productTypes: [...productTypes].sort(),
    dateField,
    reportDateFrom: input.reportDateFrom ? String(input.reportDateFrom).trim() : null,
    reportDateTo: input.reportDateTo ? String(input.reportDateTo).trim() : null,
    classifications: [...classifications].sort(),
    states: [...states].sort(),
    countries: [...countries].sort(),
    recallNumber,
    eventId,
    status,
    recallingFirm,
    city,
    voluntaryMandated,
    searchQuery,
    brandName,
    genericName,
    manufacturerName,
    includePressReleases,
};

function watchKeyFor(label, criteria) {
    const safe = label.toLowerCase().replace(/[^a-z0-9_.-]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 40) || 'default';
    const fp = createHash('sha1').update(JSON.stringify(criteria, Object.keys(criteria).sort())).digest('hex').slice(0, 10);
    return { key: `watch-${safe}-${fp}`, fingerprint: fp };
}

let watchStore = null;
let watchKey = null;
let watchRecord = null;
let seeding = false;
// `${productType}:${recallNumber|event_id:product_description}` -> last-seen snapshot of the 2
// thin fields that can change on an otherwise-already-delivered recall: `status` (Ongoing ->
// Terminated/Completed) and `classification` (FDA sometimes reclassifies a recall's severity,
// e.g. Class II -> Class I). Both come straight off the raw API row with no extra request, so
// tracking them costs nothing. `watchChanges` decides whether a change re-delivers the row; the
// snapshot itself is always kept current so turning watchChanges on later works without a fresh
// baseline. Same shape as grants-gov-scraper's `watchChanges` (cycle 346) -- copy, don't reinvent.
const watchSeen = new Map();
let changedCount = 0;
let baselineTruncated = 0;
let baselineTruncatedTotal = 0;

function truncationNote() {
    return baselineTruncated > 0
        ? ` (baseline cap: ${baselineTruncated} old id(s) dropped this run, ${baselineTruncatedTotal} total -- narrow filters to avoid re-charges)`
        : '';
}

function snapshotOf(row) {
    return { status: row.status ?? null, classification: row.classification ?? null };
}

// A changed recall is re-delivered with these fields describing exactly what moved, so a buyer
// doesn't have to diff the row against their own last-seen copy to find out.
function changesBetween(prev, next) {
    if (!prev) return null;
    const types = [];
    const previous = {};
    for (const field of ['status', 'classification']) {
        if (prev[field] !== undefined && prev[field] !== null && prev[field] !== next[field]) {
            types.push(field);
            previous[field] = prev[field];
        }
    }
    return types.length ? { types, previous } : null;
}

async function saveWatchRecord(status_) {
    const all = Array.from(watchSeen.entries());
    const entries = all.slice(-WATCH_KEEP);
    baselineTruncated = all.length - entries.length;
    if (baselineTruncated > 0) {
        baselineTruncatedTotal = (watchRecord.truncatedTotal ?? 0) + baselineTruncated;
        log.warning(
            `Watch label "${watchLabel}": baseline holds ${all.length} recall id(s), over the ${WATCH_KEEP}-id `
            + `cap -- the oldest ${baselineTruncated} were dropped and will look like NEW (billable) recalls the `
            + 'next time this run happens to see them again. Narrow the filters (productTypes/states/searchQuery) '
            + 'to keep a watch label under the cap.',
        );
    }
    await watchStore.setValue(watchKey, {
        ...watchRecord,
        label: watchLabel,
        criteria: watchCriteria,
        lastRunAt: new Date().toISOString(),
        lastRunStatus: status_,
        runCount: (watchRecord.runCount ?? 0) + 1,
        seenCount: entries.length,
        truncatedLastRun: baselineTruncated,
        truncatedTotal: baselineTruncatedTotal,
        // Compact per-entry shape: id, status, classification. Kept short because WATCH_KEEP
        // can hold up to 60,000 of these in one KV record.
        seenIds: entries.map(([id, snap]) => ({ i: id, s: snap.status, c: snap.classification })),
    });
}

if (watchMode) {
    watchStore = await Actor.openKeyValueStore(WATCH_STORE);
    const { key, fingerprint } = watchKeyFor(watchLabel, watchCriteria);
    watchKey = key;
    const existing = await watchStore.getValue(key);
    if (existing && Array.isArray(existing.seenIds)) {
        watchRecord = existing;
        // Pre-change-tracking records stored `seenIds` as a flat array of plain id strings --
        // handled here so an existing buyer's baseline keeps working unchanged instead of needing
        // a fresh seed the day this feature shipped. Those ids simply have no snapshot yet
        // (nulls), so watchChanges only starts detecting changes from here on, never against a
        // backlog it never captured.
        for (const entry of existing.seenIds) {
            if (entry && typeof entry === 'object') {
                watchSeen.set(String(entry.i), { status: entry.s ?? null, classification: entry.c ?? null });
            } else {
                watchSeen.set(String(entry), { status: null, classification: null });
            }
        }
        log.info(
            `Watch mode "${watchLabel}" (${key}): baseline from ${existing.lastRunAt ?? 'an earlier run'} holds `
            + `${watchSeen.size} already-delivered recall(s). Only recalls NOT in that baseline are returned and charged`
            + (watchChanges ? ', plus any already-delivered recall whose status or classification changed.' : '.'),
        );
    } else {
        watchRecord = { fingerprint, firstSeededAt: new Date().toISOString(), runCount: 0 };
        seeding = true;
        log.info(
            `Watch mode "${watchLabel}" (${key}): FIRST run for this label and filter set, so this is a baseline run. `
            + 'It records which recalls already match and returns ZERO results (you are charged nothing). Run it '
            + 'again on the same label and filters -- on a schedule, typically -- to get only what is new since now.',
        );
    }
}

// A bare `sort` is rejected unless the field exists on the endpoint; all 3 dateField choices
// are valid sort fields on all three endpoints (verified live).
const order = input.order === 'asc' ? 'asc' : 'desc';
const SORT = `${dateField}:${order}`;

// Lucene-ish query syntax: openFDA ANDs space-separated clauses and needs quoted phrases.
const quote = (v) => `"${String(v).replace(/"/g, '')}"`;
const orClause = (field, values) => `${field}:(${values.map(quote).join('+OR+')})`;

function buildSearch(from, to) {
    const clauses = [`${dateField}:[${from}+TO+${to}]`];
    if (classifications.length) clauses.push(orClause('classification', classifications));
    if (states.length) clauses.push(orClause('state', states));
    if (countries.length) clauses.push(orClause('country', countries));
    if (recallNumber) clauses.push(`recall_number:${quote(recallNumber)}`);
    if (eventId) clauses.push(`event_id:${quote(eventId)}`);
    if (status) clauses.push(`status:${quote(status)}`);
    if (recallingFirm) clauses.push(`recalling_firm:${quote(recallingFirm)}`);
    if (city) clauses.push(`city:${quote(city)}`);
    // Valid on all three endpoints' index mappings but only ever populated on drug rows --
    // food/device rows simply never match, same as any other filter with no data behind it,
    // verified live (not a 400, a normal empty match set).
    if (brandName) clauses.push(`openfda.brand_name:${quote(brandName)}`);
    if (genericName) clauses.push(`openfda.generic_name:${quote(genericName)}`);
    if (manufacturerName) clauses.push(`openfda.manufacturer_name:${quote(manufacturerName)}`);
    if (voluntaryMandated) clauses.push(`voluntary_mandated:${quote(voluntaryMandated)}`);
    if (searchQuery) {
        // Free text spans the three fields a buyer actually searches on.
        const q = quote(searchQuery);
        clauses.push(`(product_description:${q}+OR+reason_for_recall:${q}+OR+recalling_firm:${q})`);
    }
    return clauses.join('+AND+');
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// `search` is pre-encoded with `+` separators the way openFDA documents it, so the URL is
// assembled by hand rather than through URLSearchParams (which would escape the `+` and the
// bracket range into something the API rejects).
async function fetchPage(productType, search, limit, skip) {
    const url = `${ENDPOINTS[productType]}?search=${search}&limit=${limit}&skip=${skip}&sort=${SORT}`;
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
            log.warning(`openFDA ${productType} request failed (${err.message}); retrying in ${waitS}s (${attempt}/4).`);
            await sleep(waitS * 1000);
            continue;
        }
        if (resp.statusCode === 429 || resp.statusCode >= 500) {
            const waitS = Number(resp.headers['retry-after']) || attempt * 10;
            log.warning(`openFDA ${productType} returned ${resp.statusCode}; retrying in ${waitS}s (${attempt}/4).`);
            await sleep(waitS * 1000);
            continue;
        }
        let parsed = null;
        try { parsed = JSON.parse(resp.body); } catch { /* handled below */ }
        // A query matching nothing is a 404 with error.code NOT_FOUND, not an empty 200.
        if (resp.statusCode === 404) return { results: [], total: 0 };
        if (resp.statusCode !== 200) {
            const detail = parsed?.error?.message ?? String(resp.body).slice(0, 300);
            log.warning(`openFDA ${productType} API ${resp.statusCode}: ${detail}`);
            lastApiFailure = `HTTP ${resp.statusCode}: ${detail}`;
            return null;
        }
        if (!parsed) {
            log.warning(`openFDA ${productType} returned a non-JSON body: ${String(resp.body).slice(0, 200)}`);
            lastApiFailure = 'non-JSON response body';
            return null;
        }
        return { results: parsed.results ?? [], total: parsed.meta?.results?.total ?? 0 };
    }
    log.warning(`openFDA ${productType} kept erroring after 4 attempts; stopping this product type early.`);
    lastApiFailure = 'request kept failing after 4 attempts';
    return null;
}

// ---------------------------------------------------------------------------
// Run completeness (cycle 645). `fetchPage` returns `null` for BOTH "openFDA
// answered with nothing" and "we never got an answer", and every caller used to
// collapse the two into the same silent stop: a dead product type was `continue`d
// out of the plan, a failed window probe truncated the window plan, and a failed
// page ended a walk through the same `break` as a genuine last page. All of those
// produced a SUCCEEDED run whose dataset is indistinguishable from a complete one
// -- and in watch-seed mode an under-seeded baseline makes the NEXT run deliver
// and CHARGE pre-existing recalls as "new".
//
// Everything below exists to say that in a field rather than in English: openFDA
// hands us `meta.results.total` on every page, so this Actor always knows how many
// recalls matched and can state delivered-vs-declared per product type.
// `complete` is deliberately kept OUT of `status` -- a type can be `ok` AND
// truncated at once, which is exactly the case this record exists for.
// ---------------------------------------------------------------------------
let lastApiFailure = null;
// Set when the press-release RSS feed could not be read. It is NOT a product-type failure
// (press releases have no typeSummaries entry), so it needs its own flag: during a seed walk
// an unread feed means zero press-release guids in the baseline, which would make the first
// incremental run deliver and CHARGE the whole feed as "new" (h289).
let pressReleaseFetchFailed = null;
const typeSummaries = new Map();
function summaryFor(productType) {
    let s = typeSummaries.get(productType);
    if (!s) {
        s = {
            productType,
            // Sum of openFDA's own `meta.results.total` over the planned windows.
            // null = we never got a usable plan, which is NOT the same as 0 matches.
            declaredMatches: null,
            // What paging can actually reach: a window bigger than MAX_SKIP is
            // permanently truncated by openFDA, not by us.
            reachableMatches: null,
            windowsPlanned: null,
            windowsScanned: 0,
            scanned: 0,
            delivered: 0,
            skippedSeen: 0,
            status: 'ok',
            complete: true,
            incompleteReason: null,
            incompleteDetail: null,
        };
        typeSummaries.set(productType, s);
    }
    return s;
}
function markIncomplete(productType, reason, detail) {
    const s = summaryFor(productType);
    // First cause wins: it is the one that actually stopped the walk. A later
    // `max-results` stop must never overwrite the upstream failure above it.
    if (s.incompleteReason !== null) return;
    s.complete = false;
    s.incompleteReason = reason;
    s.incompleteDetail = detail;
    log.warning(`[${productType}] ${detail}`);
}

const yearOf = (d) => Number(String(d).slice(0, 4));

// Splits [from,to] into windows each under CHUNK_THRESHOLD rows. Year-boundary ranges are
// inclusive and were live-verified to sum exactly to the unsplit total (no overlap, no gaps).
async function planWindows(productType, from, to) {
    const probe = await fetchPage(productType, buildSearch(from, to), 1, 0);
    if (!probe) {
        // Not "this product type has no matching recalls" -- we never got an answer.
        // The old code returned null here and the caller `continue`d, dropping the
        // entire product type from the run with nothing but a log line to show it.
        markIncomplete(
            productType,
            'plan-request-failed',
            `openFDA never answered the initial ${productType} count query (${lastApiFailure}), so NOT ONE `
            + `${productType} recall was scanned. This is not evidence that no ${productType} recall matched.`,
        );
        summaryFor(productType).status = 'not-scanned';
        return null;
    }
    if (probe.total === 0) { summaryFor(productType).declaredMatches = 0; summaryFor(productType).reachableMatches = 0; summaryFor(productType).windowsPlanned = 0; return []; }
    if (probe.total <= CHUNK_THRESHOLD) return recordPlan(productType, [{ from, to, total: probe.total }], true);

    const windows = [];
    const queue = [];
    for (let y = yearOf(from); y <= yearOf(to); y += 1) {
        const wFrom = y === yearOf(from) ? from : `${y}0101`;
        const wTo = y === yearOf(to) ? to : `${y}1231`;
        queue.push({ from: wFrom, to: wTo, depth: 0 });
    }
    while (queue.length) {
        const w = queue.shift();
        const r = await fetchPage(productType, buildSearch(w.from, w.to), 1, 0);
        if (!r) {
            // A failed probe mid-plan used to return a PARTIAL window list that the
            // caller could not tell from a finished one: every remaining date window
            // (often whole years) was then never scanned, and the run still said
            // "Done. Pushed N".
            markIncomplete(
                productType,
                'plan-request-failed',
                `Planning the ${productType} date windows failed at ${w.from}..${w.to} (${lastApiFailure}); `
                + `${queue.length + 1} window(s) of that range were never scanned and their recalls are missing `
                + 'from this run.',
            );
            if (!windows.length) { summaryFor(productType).status = 'not-scanned'; return null; }
            return recordPlan(productType, windows, false);
        }
        if (r.total === 0) continue;
        // A single year still over the cap is halved by month; depth guards against a
        // pathological range that can never be split small enough.
        if (r.total > CHUNK_THRESHOLD && w.depth < 2) {
            const y = yearOf(w.from);
            queue.push({ from: w.from, to: `${y}0630`, depth: w.depth + 1 });
            queue.push({ from: `${y}0701`, to: w.to, depth: w.depth + 1 });
            continue;
        }
        if (r.total > CHUNK_THRESHOLD) {
            markIncomplete(
                productType,
                'skip-ceiling',
                `${productType} window ${w.from}..${w.to} has ${r.total} rows and cannot be split further; `
                + `only the first ${MAX_SKIP} are reachable (openFDA refuses skip>${MAX_SKIP}). Narrow `
                + 'reportDateFrom/reportDateTo to see the rest.',
            );
        }
        windows.push({ from: w.from, to: w.to, total: r.total });
    }
    log.info(`${productType}: split into ${windows.length} date windows (skip cap workaround).`);
    return recordPlan(productType, windows, true);
}

// Records what the plan says is out there, so delivered-vs-declared is a number the
// dataset's consumer can read. `planComplete=false` means the window list itself was
// cut short by a failure, so `declaredMatches` is a floor, not the match count.
function recordPlan(productType, windows, planComplete) {
    const s = summaryFor(productType);
    s.windowsPlanned = windows.length;
    s.declaredMatches = windows.reduce((n, w) => n + w.total, 0);
    s.reachableMatches = windows.reduce((n, w) => n + Math.min(w.total, MAX_SKIP), 0);
    s.declaredMatchesIsFloor = !planComplete;
    return windows;
}

const isoOf = (v) => {
    const d = String(v ?? '').replace(/[^0-9]/g, '');
    return d.length === 8 ? `${d.slice(0, 4)}-${d.slice(4, 6)}-${d.slice(6, 8)}` : null;
};

// A deterministic, documented 0-100 severity/recency/scope score — not a machine-learning
// model, just a transparent weighted formula (see README). Built as an answer to competitor
// `benthepythondev/fda-recall-intelligence`'s "AI-powered intelligence score": we do not call
// an LLM for customer-facing inference (standing rule), and a made-up "AI" label on a formula
// like this would be misleading, so this ships as a plainly-explained risk score instead.
const CLASS_SEVERITY = { 'Class I': 100, 'Class II': 60, 'Class III': 25 };
const US_STATES = new Set(
    'AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC'.split(' '),
);

function severityPoints(classification) {
    return CLASS_SEVERITY[classification] ?? 50; // unclassified/unknown: neutral, not zero
}

// Linear decay from 100 (today) to 0 at two years old. Recalls are actionable news; a two-year-old
// one is mostly historical record-keeping, which is why the floor is 0 rather than some non-zero base.
function recencyPoints(isoDate) {
    if (!isoDate) return 50; // no usable date: neutral
    const days = (today - new Date(isoDate)) / 86_400_000;
    if (!Number.isFinite(days)) return 50;
    return Math.max(0, Math.min(100, Math.round(100 - (days / 730) * 100)));
}

// `distribution_pattern` is free text (verified live sample: "New York.", "NY, NJ, PA",
// "Product was shipped to the following states: KY, NC..."). Detecting explicit nationwide/
// international language is reliable; short of that, the number of distinct US state codes
// found in the text is a reasonable proxy for how many people were exposed.
function scopePoints(pattern) {
    if (!pattern) return 40; // unknown: neutral-low, don't reward missing data
    if (/nationwide|worldwide|international/i.test(pattern)) return 100;
    const codes = new Set((pattern.match(/\b[A-Z]{2}\b/g) ?? []).filter((c) => US_STATES.has(c)));
    if (codes.size === 0) return 30; // no recognizable multi-state code: reads as one state/city
    if (codes.size === 1) return 30;
    if (codes.size <= 5) return 55;
    if (codes.size <= 15) return 75;
    return 90;
}

function riskScore(classification, isoDate, distributionPattern) {
    const s = severityPoints(classification);
    const r = recencyPoints(isoDate);
    const d = scopePoints(distributionPattern);
    return Math.round(0.45 * s + 0.3 * r + 0.25 * d);
}

function normalize(r, productType) {
    // `openfda` is populated on drug rows only — verified 5/5 drug rows populated and 5/5
    // food and device rows empty on a live sample. These flattened fields are therefore
    // advertised for drug recalls only; they come back null elsewhere.
    const o = r.openfda ?? {};
    const first = (v) => (Array.isArray(v) ? (v[0] ?? null) : (v ?? null));
    const list = (v) => (Array.isArray(v) ? Array.from(new Set(v.filter(Boolean))) : []);
    return {
        source: 'enforcement',
        productType,
        recallNumber: r.recall_number ?? null,
        eventId: r.event_id != null ? String(r.event_id) : null,
        status: r.status ?? null,
        classification: r.classification ?? null,
        voluntaryMandated: r.voluntary_mandated ?? null,
        initialFirmNotification: r.initial_firm_notification ?? null,

        recallingFirm: r.recalling_firm ?? null,
        city: r.city ?? null,
        state: r.state ?? null,
        country: r.country ?? null,

        productDescription: r.product_description ?? null,
        productQuantity: r.product_quantity ?? null,
        reasonForRecall: r.reason_for_recall ?? null,
        distributionPattern: r.distribution_pattern ?? null,
        codeInfo: r.code_info ?? null,
        moreCodeInfo: r.more_code_info ?? null,

        // openFDA stores every date as a YYYYMMDD string; these are ISO for spreadsheet sanity.
        reportDate: isoOf(r.report_date),
        recallInitiationDate: isoOf(r.recall_initiation_date),
        centerClassificationDate: isoOf(r.center_classification_date),
        terminationDate: isoOf(r.termination_date),

        riskScore: includeRiskScore
            ? riskScore(r.classification, isoOf(r.recall_initiation_date) ?? isoOf(r.report_date), r.distribution_pattern)
            : null,

        // drug-only, see comment above
        brandName: first(o.brand_name),
        genericName: first(o.generic_name),
        manufacturerName: first(o.manufacturer_name),
        substanceName: list(o.substance_name),
        productNdc: list(o.product_ndc),
        packageNdc: list(o.package_ndc),
        upc: list(o.upc),
        applicationNumber: first(o.application_number),
        drugRoute: list(o.route),
        rxcui: list(o.rxcui),
        unii: list(o.unii),
        splSetId: first(o.spl_set_id),

        // Only ever populated on source:"press_release" rows -- see normalizePressRelease below.
        pressReleaseTitle: null,
        sourceUrl: null,
    };
}

// ---------------------------------------------------------------------------
// Optional 2nd source: FDA's own recall press-release RSS feed. openFDA's enforcement API (the
// only source above, and every other FDA-recall Actor on the Store) lags real recall announcements
// by over a week -- measured live 2026-09-20: newest enforcement report_date was 11 days stale,
// while this feed already had an item from 9 days ahead of that. It is a rolling ~20-item window
// (roughly 3 weeks), not an archive, so it complements the enforcement history rather than
// replacing it -- hence includePressReleases defaults to false and is purely additive.
const PRESS_RELEASE_RSS_URL = 'https://www.fda.gov/about-fda/contact-fda/stay-informed/rss-feeds/recalls/rss.xml';

function decodeXmlEntities(s) {
    return String(s ?? '')
        .replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, '$1')
        .replace(/&lt;/g, '<')
        .replace(/&gt;/g, '>')
        .replace(/&quot;/g, '"')
        .replace(/&apos;/g, "'")
        .replace(/&#(\d+);/g, (_, d) => String.fromCodePoint(Number(d)))
        .replace(/&amp;/g, '&')
        .trim();
}

// Deliberately a small hand-rolled regex parser, not a real XML library: the feed's shape is
// fixed and simple (verified live, cycle 528/529 -- exactly title/link/description/pubDate/
// dc:creator/guid per <item>, no nesting), and this box avoids extra dependencies where a few
// lines of regex do the job (see standing memory-budget rule).
function parseRssItems(xml) {
    const items = [];
    const itemRe = /<item>([\s\S]*?)<\/item>/g;
    let m;
    while ((m = itemRe.exec(xml))) {
        const block = m[1];
        const grab = (tag) => {
            const r = new RegExp(`<${tag}[^>]*>([\\s\\S]*?)<\\/${tag}>`).exec(block);
            return r ? decodeXmlEntities(r[1]) : null;
        };
        const title = grab('title');
        const link = grab('link');
        const description = grab('description');
        const pubDateRaw = grab('pubDate');
        const guid = grab('guid') ?? link;
        if (!title || !link) continue; // malformed item; skip rather than emit a broken row
        // RFC-822 with an EDT/EST zone abbreviation -- Node's Date parser resolves these to the
        // correct UTC offset natively (verified live: "...17:48:00 EDT" -> ...21:48:00.000Z).
        const pubDateMs = pubDateRaw ? Date.parse(pubDateRaw) : NaN;
        items.push({
            title,
            link,
            description,
            guid,
            pubDateIso: Number.isFinite(pubDateMs) ? new Date(pubDateMs).toISOString() : null,
        });
    }
    return items;
}

async function fetchPressReleases() {
    let resp;
    try {
        resp = await gotScraping({
            url: PRESS_RELEASE_RSS_URL,
            responseType: 'text',
            throwHttpErrors: false,
            retry: { limit: 1 },
            timeout: { request: 20000 },
            headers: { accept: 'application/rss+xml, application/xml, text/xml' },
        });
    } catch (err) {
        pressReleaseFetchFailed = `the FDA press-release RSS feed request failed (${err.message})`;
        log.warning(`FDA press-release RSS feed request failed (${err.message}); skipping press releases this run.`);
        return [];
    }
    if (resp.statusCode !== 200) {
        pressReleaseFetchFailed = `the FDA press-release RSS feed returned HTTP ${resp.statusCode}`;
        log.warning(`FDA press-release RSS feed returned ${resp.statusCode}; skipping press releases this run.`);
        return [];
    }
    const items = parseRssItems(resp.body);
    if (!items.length) log.warning('FDA press-release RSS feed returned 200 but no parseable <item> entries.');
    return items;
}

// classification is always null for these rows (the feed doesn't carry one), so severityPoints
// has no input to score -- riskScore is left null rather than silently scoring press releases on
// a different, undocumented scale than enforcement rows.
function normalizePressRelease(item) {
    const reportDate = item.pubDateIso ? item.pubDateIso.slice(0, 10) : null;
    return {
        source: 'press_release',
        productType: null,
        recallNumber: null,
        eventId: null,
        status: null,
        classification: null,
        voluntaryMandated: null,
        initialFirmNotification: null,
        recallingFirm: null,
        city: null,
        state: null,
        country: null,
        productDescription: item.title,
        productQuantity: null,
        reasonForRecall: item.description,
        distributionPattern: null,
        codeInfo: null,
        moreCodeInfo: null,
        reportDate,
        recallInitiationDate: null,
        centerClassificationDate: null,
        terminationDate: null,
        riskScore: null,
        brandName: null,
        genericName: null,
        manufacturerName: null,
        substanceName: [],
        productNdc: [],
        packageNdc: [],
        upc: [],
        applicationNumber: null,
        drugRoute: [],
        rxcui: [],
        unii: [],
        splSetId: null,
        pressReleaseTitle: item.title,
        sourceUrl: item.link,
    };
}

let pushed = 0;
let chargeLimitHit = false;
const isPPE = Actor.getChargingManager().getPricingInfo().isPayPerEvent;
async function pushResult(item) {
    if (isPPE) {
        const r = await Actor.charge({ eventName: 'result', count: 1 });
        if (r.chargedCount === 0) { chargeLimitHit = true; return false; }
        await Actor.pushData(item); pushed += 1;
        if (r.eventChargeLimitReached) chargeLimitHit = true;
        return !r.eventChargeLimitReached && pushed < maxResults;
    }
    await Actor.pushData(item); pushed += 1;
    return pushed < maxResults;
}

log.info(
    `openFDA recalls: productTypes=[${productTypes.join(',')}] ${dateField} ${reportDateFrom}..${reportDateTo} `
    + `sort=${SORT} maxResults=${maxResults}`
    + (classifications.length ? ` classifications=[${classifications.join(', ')}]` : '')
    + (states.length ? ` states=[${states.join(',')}]` : '')
    + (countries.length ? ` countries=[${countries.join(',')}]` : '')
    + (recallNumber ? ` recallNumber="${recallNumber}"` : '')
    + (eventId ? ` eventId="${eventId}"` : '')
    + (recallingFirm ? ` recallingFirm="${recallingFirm}"` : '')
    + (city ? ` city="${city}"` : '')
    + (voluntaryMandated ? ` voluntaryMandated="${voluntaryMandated}"` : '')
    + (searchQuery ? ` searchQuery="${searchQuery}"` : '')
    + (watchMode ? ` watchLabel="${watchLabel}"` : '')
    + (includePressReleases ? ` includePressReleases=${runPressReleases}${runPressReleases ? '' : ' (skipped, see warning above)'}` : ''),
);

// recall_number is unique per recall; event_id groups several products in one event and is the
// fallback identity when a row has no recall_number. Shared by the real push loop AND the
// watch-mode seed walk below so the two can never disagree on what a recall's stable id is.
function dedupKeyOf(productType, row) {
    return `${productType}:${row.recall_number ?? `${row.event_id}:${row.product_description}`}`;
}

// One page-buffered reader per product type. Rows are emitted round-robin (one per type per
// round) rather than draining one type before the next: a single page holds up to 1000 rows,
// so sequential draining would make any maxResults under a page size return 100% food and
// 0% drug/device.
const pageSize = Math.min(MAX_LIMIT, Math.max(20, Math.min(maxResults, 200)));
const readers = [];
if (!(watchMode && seeding)) {
    for (const productType of productTypes) {
        const windows = await planWindows(productType, reportDateFrom, reportDateTo);
        // API failed for this type; the others still run -- but the failure is now on
        // the record (markIncomplete inside planWindows) instead of vanishing here.
        if (windows === null) continue;
        readers.push({ productType, windows, windowIdx: 0, skip: 0, buffer: [], done: !windows.length, pushed: 0 });
    }
}

async function refill(reader) {
    while (!reader.buffer.length && !reader.done) {
        const w = reader.windows[reader.windowIdx];
        if (!w) { reader.done = true; return; }
        if (reader.skip >= Math.min(w.total, MAX_SKIP)) {
            reader.windowIdx += 1;
            reader.skip = 0;
            summaryFor(reader.productType).windowsScanned += 1;
            continue;
        }
        const limit = Math.min(pageSize, MAX_SKIP - reader.skip);
        const page = await fetchPage(reader.productType, buildSearch(w.from, w.to), limit, reader.skip);
        if (!page) {
            // Was: silently identical to "this product type is exhausted".
            markIncomplete(
                reader.productType,
                'search-request-failed',
                `The ${reader.productType} walk stopped at window ${w.from}..${w.to} offset ${reader.skip} because `
                + `openFDA did not answer (${lastApiFailure}); the rest of that window and every window after it `
                + 'was not scanned.',
            );
            reader.done = true;
            return;
        }
        reader.skip += limit;
        if (!page.results.length) { reader.windowIdx += 1; reader.skip = 0; summaryFor(reader.productType).windowsScanned += 1; continue; }
        reader.buffer = page.results;
    }
}

// Seeding only needs ids, so it walks every window at the API's own max page size (1000, not the
// smaller `pageSize` the real run uses) rather than reusing the `readers` structure above -- the
// federal-register-scraper trap (cycle 297) was a seed silently inheriting a small per-page size
// tied to maxResults and stopping short of the full match set. This still calls the exact same
// `planWindows`/`fetchPage`/`buildSearch` functions the real run uses, so the two walks can never
// page the underlying API differently -- only how many rows they keep differs (ids vs full rows).
// Unbounded by maxResults on purpose: a baseline that stopped early would report every recall past
// the stopping point as "new" on the first incremental run.
async function seedBaseline() {
    for (const productType of productTypes) {
        const windows = await planWindows(productType, reportDateFrom, reportDateTo);
        if (windows === null) continue;
        for (const w of windows) {
            let skip = 0;
            for (;;) {
                if (skip >= Math.min(w.total, MAX_SKIP)) break;
                const limit = Math.min(MAX_LIMIT, MAX_SKIP - skip);
                const page = await fetchPage(productType, buildSearch(w.from, w.to), limit, skip);
                // Split apart: a failed request is NOT a finished window. Collapsing the
                // two under-seeds the baseline, and every recall past the failure point
                // is then delivered and CHARGED as "new" on the next incremental run.
                if (!page) {
                    markIncomplete(
                        productType,
                        'search-request-failed',
                        `The ${productType} baseline walk stopped at window ${w.from}..${w.to} offset ${skip} because `
                        + `openFDA did not answer (${lastApiFailure}). Recalls past that point are NOT in the baseline, `
                        + 'so the next incremental run on this watch label would deliver and charge them as new. '
                        + 'Re-run the seed (delete nothing; seeding overwrites the baseline) before relying on it.',
                    );
                    break;
                }
                if (!page.results.length) break;
                for (const row of page.results) watchSeen.set(dedupKeyOf(productType, row), snapshotOf(row));
                summaryFor(productType).scanned += page.results.length;
                skip += limit;
                if (watchSeen.size >= SEED_CAP) {
                    markIncomplete(
                        productType,
                        'seed-cap',
                        `Watch label "${watchLabel}" seed hit the ${SEED_CAP}-recall cap before scanning the whole `
                        + 'match set. Narrow the query (a shorter date window, a classification, a state) so the '
                        + 'whole result set fits, or the first incremental run will report recalls past the cap as new.',
                    );
                    log.info(`Baseline walk: ${watchSeen.size} recall id(s) recorded.`);
                    return;
                }
                if (page.results.length < limit) break; // last page of this window
            }
            summaryFor(productType).windowsScanned += 1;
        }
    }
    if (runPressReleases) {
        const items = await fetchPressReleases();
        for (const item of items) watchSeen.set(`press_release:${item.guid}`, { status: null, classification: null });
        log.info(`Baseline walk: +${items.length} FDA press release(s) recorded.`);
    }
    log.info(`Baseline walk: ${watchSeen.size} recall id(s) recorded.`);
}

let scanned = 0;
let skippedSeen = 0;

if (watchMode && seeding) {
    await seedBaseline();
} else {
    const seen = new Set();
    let keepGoing = true;

    while (keepGoing && pushed < maxResults && readers.some((r) => !r.done || r.buffer.length)) {
        let emitted = false;
        for (const reader of readers) {
            if (!keepGoing || pushed >= maxResults) break;
            await refill(reader);
            const row = reader.buffer.shift();
            if (!row) continue;
            emitted = true;
            scanned += 1;
            summaryFor(reader.productType).scanned += 1;
            const key = dedupKeyOf(reader.productType, row);
            if (seen.has(key)) continue;
            seen.add(key);
            // Already delivered under this watch label: normally dropped before any charge, so a
            // recall is never paid for twice -- UNLESS watchChanges is on and its status or
            // classification moved since we last saw it, in which case it is re-delivered
            // (charged like a new row) tagged with exactly what changed.
            if (watchMode && watchSeen.has(key)) {
                const nextSnap = snapshotOf(row);
                const change = watchChanges ? changesBetween(watchSeen.get(key), nextSnap) : null;
                if (!change) {
                    // Snapshot kept current either way, so turning watchChanges on later detects
                    // only drift from that point, not a backlog since the baseline.
                    watchSeen.set(key, nextSnap);
                    skippedSeen += 1;
                    summaryFor(reader.productType).skippedSeen += 1;
                    continue;
                }
                reader.pushed += 1;
                const before = pushed;
                keepGoing = await pushResult({
                    ...normalize(row, reader.productType),
                    _watchChangeType: change.types,
                    _watchPrevious: change.previous,
                });
                if (pushed > before) { watchSeen.set(key, nextSnap); changedCount += 1; summaryFor(reader.productType).delivered += 1; }
                continue;
            }
            reader.pushed += 1;
            const before = pushed;
            keepGoing = await pushResult(normalize(row, reader.productType));
            // Recorded as delivered only after the charge actually succeeded -- anything dropped
            // by maxResults or a charge limit stays "new" for the next run.
            if (pushed > before) summaryFor(reader.productType).delivered += 1;
            if (watchMode && pushed > before) watchSeen.set(key, snapshotOf(row));
        }
        if (!emitted) break;
    }

    // An early stop leaves every product type short of its declared match set, and
    // until now it was recorded nowhere at all -- the run just said "Done. Pushed N".
    if (!keepGoing || pushed >= maxResults) {
        const reason = chargeLimitHit ? 'charge-limit' : 'max-results';
        const detail = chargeLimitHit
            ? 'Stopped by the run\'s maximum-cost limit before the match set was exhausted; raise it to get the rest.'
            : `Stopped at maxResults=${maxResults}; matching recalls past this point were not returned.`;
        for (const reader of readers) {
            if (!reader.done || reader.buffer.length) markIncomplete(reader.productType, reason, detail);
        }
    }
    // A type whose reader never ran out of windows is short regardless of why the
    // round-robin left it behind.
    for (const reader of readers) {
        const s = summaryFor(reader.productType);
        if (!reader.done && s.complete) markIncomplete(reader.productType, 'not-reached', `The ${reader.productType} walk ended before its windows were exhausted.`);
    }

    for (const reader of readers) log.info(`${reader.productType}: pushed ${reader.pushed} recalls.`);

    if (runPressReleases && pushed < maxResults) {
        const items = await fetchPressReleases();
        scanned += items.length;
        let prPushed = 0;
        for (const item of items) {
            if (pushed >= maxResults) break;
            if (searchQuery) {
                const hay = `${item.title} ${item.description ?? ''}`.toLowerCase();
                if (!hay.includes(searchQuery.toLowerCase())) continue;
            }
            const day = item.pubDateIso ? item.pubDateIso.slice(0, 10).replace(/-/g, '') : null;
            if (day && (day < reportDateFrom || day > reportDateTo)) continue;
            const key = `press_release:${item.guid}`;
            // watchChanges is a no-op for press releases (spec: they have no status/classification
            // to change), so an already-seen guid is always just skipped, never re-delivered.
            if (watchMode && watchSeen.has(key)) {
                skippedSeen += 1;
                continue;
            }
            const before = pushed;
            const keep = await pushResult(normalizePressRelease(item));
            if (pushed > before) {
                prPushed += 1;
                if (watchMode) watchSeen.set(key, { status: null, classification: null });
            }
            if (!keep) break;
        }
        log.info(`press_release: pushed ${prPushed} FDA press release(s) (${items.length} fetched from the feed).`);
    }
}

// A SEED walk cut short by an upstream error must save NOTHING (h289, first fixed on
// federal-register-scraper cycle 683): saving the partial id set as the baseline makes the first
// incremental run treat every recall past the failure point as "new" and CHARGE for it. A seed
// charges nothing, so re-seeding later is free -- there is nothing lost by not persisting here.
// Deliberately NOT gated on `seed-cap`/`skip-ceiling`: those are the buyer's query being too
// broad, are reported in RUN_SUMMARY and the status message, and a capped baseline is still
// strictly better than none. Only a source that never answered gets the no-save treatment.
const SEED_UPSTREAM_FAILURES = new Set(['plan-request-failed', 'search-request-failed']);
const seedFailure = seeding
    ? ([...typeSummaries.values()].find((s) => SEED_UPSTREAM_FAILURES.has(s.incompleteReason))?.incompleteDetail
        ?? pressReleaseFetchFailed
        ?? null)
    : null;

if (watchMode && seedFailure) {
    log.warning(
        `Baseline walk for watch label "${watchLabel}" was cut short (${seedFailure}), so NO baseline was saved. `
        + 'A partial baseline would have caused every recall past the stopping point to be delivered and charged '
        + 'as "new" on your next run. Re-run the same label and filters once the source recovers.',
    );
} else if (watchMode) {
    await saveWatchRecord(seeding ? 'seeded' : 'incremental');
    if (seeding) {
        log.info(
            `Baseline saved for watch label "${watchLabel}": ${watchSeen.size} recall(s) recorded as already-seen, `
            + `0 results returned, 0 charged. The next run on this label and these filters returns only new recalls.${truncationNote()}`,
        );
    } else {
        log.info(
            `Watch label "${watchLabel}": ${pushed - changedCount} new recall(s)`
            + (watchChanges ? ` and ${changedCount} changed recall(s) (status/classification)` : '')
            + ` since the last run (${skippedSeen} already-delivered, unchanged row(s) skipped, uncharged); baseline now holds ${watchSeen.size}.${truncationNote()}`,
        );
    }
}

if (pushed === 0 && watchMode && !seeding) {
    log.warning(
        `Nothing new for watch label "${watchLabel}" since its last run -- all ${skippedSeen} matching recall(s) `
        + 'had already been delivered. That is the expected result most of the time; you were charged for nothing.',
    );
} else if (pushed === 0 && !seeding) {
    log.warning(
        `No recalls matched. Scanned ${scanned} rows. Most common causes, in order: `
        + '(1) the filters are ANDed — a searchQuery plus a state plus a classification over a short '
        + 'report_date window often has zero real matches; drop one filter and retry. '
        + `(2) reportDateFrom/reportDateTo currently filter on ${dateField} — if that's report_date `
        + '(when FDA published the enforcement report), it can be months after the recall actually '
        + 'started; try dateField="recall_initiation_date" or widen the window. '
        + '(3) "states" must be the 2-letter code of the RECALLING FIRM\'s state, not where the '
        + 'product was distributed; use distributionPattern in the output for distribution instead. '
        + '(4) searchQuery is a phrase match over product description, recall reason and firm name — '
        + 'a long phrase rarely matches; try one distinctive word. '
        + '(5) brandName/genericName/manufacturerName only ever match drug recalls (openFDA cross-'
        + 'references those fields for drugs only) — they will zero out a food- or device-only search.',
    );
}

// The whole point of this record: everything above is English in a log, and a pipeline
// reads neither. 40 rows against a declared 12,431 matches is byte-identical to a
// complete result set in the dataset. Written to the run's key-value store so it is
// readable with no webhook configured:
//   GET /v2/actor-runs/<runId>/key-value-store/records/RUN_SUMMARY
for (const productType of productTypes) summaryFor(productType);
const types = [...typeSummaries.values()];
const typeIncomplete = types.find((s) => !s.complete) ?? null;
// The press-release feed is a source in its own right, not a product type, so a feed failure has
// no typeSummaries entry to mark incomplete -- without this the run reports complete:true while
// silently missing every press release the buyer asked for (and, on a seed, leaves them out of
// the baseline so they are all charged as "new" later).
const feedIncomplete = runPressReleases && pressReleaseFetchFailed
    ? {
        incompleteReason: 'press-release-feed-failed',
        incompleteDetail: `Press releases were requested but ${pressReleaseFetchFailed}, so none are in this run.`
            + (seeding ? ' No baseline was saved for this label.' : ''),
    }
    : null;
const firstIncomplete = typeIncomplete ?? feedIncomplete;
const runSummary = {
    finishedAt: new Date().toISOString(),
    mode: seeding ? 'watch-seed' : (watchMode ? 'watch-incremental' : 'search'),
    // Sum over product types. null when NO type produced a usable plan -- which is not
    // the same claim as "0 recalls matched", and the difference is the whole point.
    declaredMatches: types.some((s) => s.declaredMatches !== null)
        ? types.reduce((n, s) => n + (s.declaredMatches ?? 0), 0)
        : null,
    // In watch-seed mode the global counter stays 0 (nothing is delivered by design),
    // so the seed walk's own row count is what "scanned" has to mean there.
    scanned: seeding ? types.reduce((n, s) => n + s.scanned, 0) : scanned,
    delivered: pushed,
    // A buyer asking "did I get everything that matched?" needs the answer to be a
    // field, not a sentence. Seeding runs deliver 0 rows BY DESIGN and are judged on
    // the baseline walk instead.
    complete: firstIncomplete === null,
    incompleteReason: firstIncomplete?.incompleteReason ?? null,
    incompleteDetail: firstIncomplete?.incompleteDetail ?? null,
    skippedSeen,
    changedCount: watchMode && !seeding ? changedCount : null,
    baselineSize: watchMode ? watchSeen.size : null,
    baselineTruncated: watchMode ? baselineTruncated : null,
    baselineTruncatedTotal: watchMode ? baselineTruncatedTotal : null,
    pressReleasesRequested: includePressReleases,
    pressReleasesIncluded: runPressReleases,
    pressReleaseFeedError: pressReleaseFetchFailed,
    productTypes: types,
};
await Actor.setValue('RUN_SUMMARY', runSummary);

if (firstIncomplete) {
    const short = [
        ...types.filter((s) => !s.complete).map((s) => `${s.productType}:${s.incompleteReason}`),
        ...(feedIncomplete ? [`press_release:${feedIncomplete.incompleteReason}`] : []),
    ].join(', ');
    await Actor.setStatusMessage(
        `INCOMPLETE (${short}): delivered ${pushed} row(s)`
        + (runSummary.declaredMatches !== null ? ` of ${runSummary.declaredMatches} declared match(es)` : '')
        + `. ${firstIncomplete.incompleteDetail} See the RUN_SUMMARY key-value record for the machine-readable detail.`,
    );
} else if (baselineTruncated > 0) {
    await Actor.setStatusMessage(
        `Complete, but the watch baseline exceeded its ${WATCH_KEEP}-id cap and dropped ${baselineTruncated} old `
        + `id(s) this run (${baselineTruncatedTotal} total) -- those may be re-delivered and re-charged as "new" `
        + 'later. Narrow the filters to keep this label under the cap.',
    );
}

log.info(`Done. Pushed ${pushed} recalls from ${productTypes.length} product type(s) (scanned ${scanned} rows).`);

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
        watchLabel: watchMode ? watchLabel : null,
        watchSeeding: watchMode ? seeding : null,
        watchNewCount: watchMode && !seeding ? pushed - changedCount : null,
        watchChangedCount: watchMode && !seeding ? changedCount : null,
        // Same object as the RUN_SUMMARY key-value record, so a webhook consumer and a
        // polling consumer can never be told two different stories about one run.
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
// RUN_SUMMARY write and the webhook above. A seed pushes no rows, so nothing was charged and
// failing is free -- and failing loudly, instead of exiting 0 with no baseline saved, stops a
// scheduled run from quietly reading "seeded" and moving on to incremental.
if (watchMode && seedFailure) {
    await Actor.fail(
        `The watch baseline could not be completed: ${seedFailure.replace(/[.\s]*$/, '')}. No baseline was saved `
        + '(a partial one would '
        + 'cause you to be charged twice for the same recalls later) and nothing was charged. Please re-run in '
        + 'a few minutes.',
    );
}

await Actor.exit();
