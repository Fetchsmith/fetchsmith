import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';

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
const searchQuery = String(input.searchQuery ?? '').trim();
const status = String(input.status ?? '').trim();
const maxResults = Math.min(Math.max(Number(input.maxResults ?? 100), 1), 50000);

const compactDay = (d) => d.toISOString().slice(0, 10).replace(/-/g, '');
const today = new Date();
// openFDA's oldest enforcement reports are from 2004; 19000101 is a safe open lower bound.
const EARLIEST = '19000101';
const normDate = (v, fallback) => {
    if (v == null || v === '') return fallback;
    const digits = String(v).replace(/[^0-9]/g, '');
    return digits.length === 8 ? digits : fallback;
};
const reportDateFrom = normDate(
    input.reportDateFrom,
    compactDay(new Date(today.getTime() - 365 * 86400_000)),
);
const reportDateTo = normDate(input.reportDateTo, compactDay(today));

// A bare `sort` is rejected unless the field exists on the endpoint; report_date is on all three.
const order = input.order === 'asc' ? 'asc' : 'desc';
const SORT = `report_date:${order}`;

// Lucene-ish query syntax: openFDA ANDs space-separated clauses and needs quoted phrases.
const quote = (v) => `"${String(v).replace(/"/g, '')}"`;
const orClause = (field, values) => `${field}:(${values.map(quote).join('+OR+')})`;

function buildSearch(from, to) {
    const clauses = [`report_date:[${from}+TO+${to}]`];
    if (classifications.length) clauses.push(orClause('classification', classifications));
    if (states.length) clauses.push(orClause('state', states));
    if (status) clauses.push(`status:${quote(status)}`);
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
            return null;
        }
        if (!parsed) {
            log.warning(`openFDA ${productType} returned a non-JSON body: ${String(resp.body).slice(0, 200)}`);
            return null;
        }
        return { results: parsed.results ?? [], total: parsed.meta?.results?.total ?? 0 };
    }
    log.warning(`openFDA ${productType} kept erroring after 4 attempts; stopping this product type early.`);
    return null;
}

const yearOf = (d) => Number(String(d).slice(0, 4));

// Splits [from,to] into windows each under CHUNK_THRESHOLD rows. Year-boundary ranges are
// inclusive and were live-verified to sum exactly to the unsplit total (no overlap, no gaps).
async function planWindows(productType, from, to) {
    const probe = await fetchPage(productType, buildSearch(from, to), 1, 0);
    if (!probe) return null;
    if (probe.total === 0) return [];
    if (probe.total <= CHUNK_THRESHOLD) return [{ from, to, total: probe.total }];

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
        if (!r) return windows.length ? windows : null;
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
            log.warning(
                `${productType} window ${w.from}..${w.to} has ${r.total} rows and cannot be split further; `
                + `only the first ${MAX_SKIP} are reachable. Narrow reportDateFrom/reportDateTo to see the rest.`,
            );
        }
        windows.push({ from: w.from, to: w.to, total: r.total });
    }
    log.info(`${productType}: split into ${windows.length} date windows (skip cap workaround).`);
    return windows;
}

const isoOf = (v) => {
    const d = String(v ?? '').replace(/[^0-9]/g, '');
    return d.length === 8 ? `${d.slice(0, 4)}-${d.slice(4, 6)}-${d.slice(6, 8)}` : null;
};

function normalize(r, productType) {
    // `openfda` is populated on drug rows only — verified 5/5 drug rows populated and 5/5
    // food and device rows empty on a live sample. These flattened fields are therefore
    // advertised for drug recalls only; they come back null elsewhere.
    const o = r.openfda ?? {};
    const first = (v) => (Array.isArray(v) ? (v[0] ?? null) : (v ?? null));
    const list = (v) => (Array.isArray(v) ? Array.from(new Set(v.filter(Boolean))) : []);
    return {
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
    `openFDA recalls: productTypes=[${productTypes.join(',')}] report_date ${reportDateFrom}..${reportDateTo} `
    + `sort=${SORT} maxResults=${maxResults}`
    + (classifications.length ? ` classifications=[${classifications.join(', ')}]` : '')
    + (states.length ? ` states=[${states.join(',')}]` : '')
    + (searchQuery ? ` searchQuery="${searchQuery}"` : ''),
);

// One page-buffered reader per product type. Rows are emitted round-robin (one per type per
// round) rather than draining one type before the next: a single page holds up to 1000 rows,
// so sequential draining would make any maxResults under a page size return 100% food and
// 0% drug/device.
const pageSize = Math.min(MAX_LIMIT, Math.max(20, Math.min(maxResults, 200)));
const readers = [];
for (const productType of productTypes) {
    const windows = await planWindows(productType, reportDateFrom, reportDateTo);
    if (windows === null) continue; // API failed for this type; others still run
    readers.push({ productType, windows, windowIdx: 0, skip: 0, buffer: [], done: !windows.length, pushed: 0 });
}

async function refill(reader) {
    while (!reader.buffer.length && !reader.done) {
        const w = reader.windows[reader.windowIdx];
        if (!w) { reader.done = true; return; }
        if (reader.skip >= Math.min(w.total, MAX_SKIP)) {
            reader.windowIdx += 1;
            reader.skip = 0;
            continue;
        }
        const limit = Math.min(pageSize, MAX_SKIP - reader.skip);
        const page = await fetchPage(reader.productType, buildSearch(w.from, w.to), limit, reader.skip);
        if (!page) { reader.done = true; return; }
        reader.skip += limit;
        if (!page.results.length) { reader.windowIdx += 1; reader.skip = 0; continue; }
        reader.buffer = page.results;
    }
}

const seen = new Set();
let scanned = 0;
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
        // recall_number is unique per recall; event_id groups several products in one event.
        const key = `${reader.productType}:${row.recall_number ?? `${row.event_id}:${row.product_description}`}`;
        if (seen.has(key)) continue;
        seen.add(key);
        reader.pushed += 1;
        keepGoing = await pushResult(normalize(row, reader.productType));
    }
    if (!emitted) break;
}

for (const reader of readers) log.info(`${reader.productType}: pushed ${reader.pushed} recalls.`);

if (pushed === 0) {
    log.warning(
        `No recalls matched. Scanned ${scanned} rows. Most common causes, in order: `
        + '(1) the filters are ANDed — a searchQuery plus a state plus a classification over a short '
        + 'report_date window often has zero real matches; drop one filter and retry. '
        + '(2) reportDateFrom/reportDateTo filter on report_date (when FDA published the enforcement '
        + 'report), which can be months after recall_initiation_date — widen the window. '
        + '(3) "states" must be the 2-letter code of the RECALLING FIRM\'s state, not where the '
        + 'product was distributed; use distributionPattern in the output for distribution instead. '
        + '(4) searchQuery is a phrase match over product description, recall reason and firm name — '
        + 'a long phrase rarely matches; try one distinctive word.',
    );
}

log.info(`Done. Pushed ${pushed} recalls from ${readers.length} product type(s) (scanned ${scanned} rows).`);
await Actor.exit();
