import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';
import { createHash } from 'node:crypto';

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
const watchLabel = String(input.watchLabel ?? '').trim();
const watchChanges = Boolean(input.watchChanges);

log.info('Starting SAM.gov opportunity search', {
    keyword, naicsCodes, setAsideTypes, noticeTypes, states, organizationId, activeOnly, maxResults, enrichDetail, watchLabel,
});

function buildSearchUrl(page, size) {
    // `mode=search` truncates `descriptions[0].content` to 250 chars server-side -- confirmed by
    // diffing identical queries with/without it (cycle 567): same `totalElements`, same row ids
    // per page (intra-page order can differ on relevance ties, never drops/adds a row), but content
    // length caps at exactly 250 with the param and runs up to 37k+ chars without it. Omitting it
    // is a zero-new-request way to deliver the FULL solicitation description text.
    const params = new URLSearchParams({
        index: 'opp', responseType: 'json',
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

// ---------------------------------------------------------------------------
// Watch mode: "only what is new since my last run", per saved query. Same shape as
// grants-gov-scraper/federal-register-scraper (cycle 297+) -- copy that design, don't reinvent it.
//
// The baseline is the buyer's own -- the opportunity ids this label has already delivered -- kept
// in a NAMED key-value store so it survives across runs (the default per-run KV store would reset
// the baseline every run, i.e. re-charge the whole result set every time). `opportunityId` (SAM's
// `_id`) is the stable identity: it's what the detail endpoint and the public /opp/<id>/view URL
// key off, whereas `solicitationNumber` is an agency-entered label that can in principle repeat.
const WATCH_STORE = 'fetchsmith-samgov-watch';
const SEED_CAP = 10000; // same as SAM.gov's own hard backend depth cap -- a seed walk can never
// need to go deeper than the platform itself allows for one query.
const WATCH_KEEP = 60000; // bound the KV record size; oldest ids fall off first

const watchMode = watchLabel.length > 0;

// Apify KV keys allow [a-zA-Z0-9!-_.'()] only, so the label is sanitised rather than trusted. The
// criteria fingerprint is part of the key on purpose: if the buyer edits a filter, that's a
// different question and gets its own baseline, instead of dumping every opportunity the old
// narrower filter happened to exclude as if it were brand new. `enrichDetail` is deliberately left
// out -- it changes output richness, not which opportunities match, same reasoning as `enrich` on
// grants-gov-scraper's watchCriteria.
function watchKeyFor(label, criteria) {
    const safe = label.toLowerCase().replace(/[^a-z0-9_.-]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 40) || 'default';
    const fp = createHash('sha1').update(JSON.stringify(criteria, Object.keys(criteria).sort())).digest('hex').slice(0, 10);
    return { key: `watch-${safe}-${fp}`, fingerprint: fp };
}

const watchCriteria = {
    keyword, naicsCodes: [...naicsCodes].sort(), setAsideTypes: [...setAsideTypes].sort(),
    noticeTypes: [...noticeTypes].sort(), states: [...states].sort(), organizationId, activeOnly,
};

// Snapshot of the fields that can change on an already-delivered opportunity: `isActive`/
// `noticeTypeCode` (the presolicitation -> solicitation -> award lifecycle transition SAM.gov's
// own demand data flags as the single most valuable alert in this niche), `responseDate` (a
// deadline extension -- the highest-frequency real change), `modifiedDate` (SAM's own "this
// notice was edited" stamp), `modificationsCount` and `awardeeName` (null -> set is the award
// landing). `description` is now the FULL solicitation text (cycle 567, can run 10k+ chars) -- the
// fleet rule is never to store free text in a watch snapshot, so only an 8-char md5 fingerprint of
// it is kept, enough to detect an edit without risking the KV record's size budget (WATCH_KEEP
// holds up to 60,000 of these).
function descHashOf(desc) {
    return desc ? createHash('md5').update(desc).digest('hex').slice(0, 8) : null;
}
function snapshotOf(item) {
    return {
        isActive: item.isActive ?? null,
        noticeTypeCode: item.noticeTypeCode ?? null,
        responseDate: item.responseDate ?? null,
        modifiedDate: item.modifiedDate ?? null,
        modificationsCount: typeof item.modificationsCount === 'number' ? item.modificationsCount : null,
        awardeeName: item.awardeeName ?? null,
        descHash: descHashOf(item.description),
    };
}

// A changed opportunity is re-delivered tagged with exactly what moved, so a buyer doesn't have to
// diff the row against their own last-seen copy to find out. descHash is compared separately since
// its "previous" value (a hash) isn't meaningful to show a buyer.
function changesBetween(prev, next) {
    if (!prev) return null;
    const types = [];
    const previous = {};
    for (const field of ['isActive', 'noticeTypeCode', 'responseDate', 'modifiedDate', 'modificationsCount', 'awardeeName']) {
        if (prev[field] !== undefined && prev[field] !== null && prev[field] !== next[field]) {
            types.push(field);
            previous[field] = prev[field];
        }
    }
    if (prev.descHash !== undefined && prev.descHash !== null && prev.descHash !== next.descHash) {
        types.push('description');
        previous.description = '(changed; only a fingerprint of the description is retained, not the previous text)';
    }
    return types.length ? { types, previous } : null;
}

let watchStore = null;
let watchKey = null;
let watchRecord = null;
let seeding = false;
const watchSeen = new Map(); // opportunityId -> last-seen snapshot
let changedCount = 0;
let skippedSeen = 0;

async function saveWatchRecord(status) {
    const entries = Array.from(watchSeen.entries()).slice(-WATCH_KEEP);
    await watchStore.setValue(watchKey, {
        ...watchRecord,
        label: watchLabel,
        criteria: watchCriteria,
        lastRunAt: new Date().toISOString(),
        lastRunStatus: status,
        seenCount: entries.length,
        // Compact per-entry shape so WATCH_KEEP's 60,000 entries stay inside the KV record's size
        // budget: i(d), a(isActive), n(noticeTypeCode), r(responseDate), m(modifiedDate),
        // c(modificationsCount), w(awardeeName), h(descHash).
        seenIds: entries.map(([id, snap]) => ({
            i: id, a: snap.isActive, n: snap.noticeTypeCode, r: snap.responseDate, m: snap.modifiedDate,
            c: snap.modificationsCount, w: snap.awardeeName, h: snap.descHash,
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
        // Backward-compatible reader: a record from before this feature existed would only ever
        // be a fresh baseline (this is the Actor's first watch-mode build), but kept defensive the
        // same way the fleet's other watch actors are, in case a future field is added later and
        // an older record is missing it -- missing fields just have no snapshot yet.
        for (const entry of existing.seenIds) {
            if (entry && typeof entry === 'object') {
                watchSeen.set(String(entry.i), {
                    isActive: entry.a ?? null, noticeTypeCode: entry.n ?? null, responseDate: entry.r ?? null,
                    modifiedDate: entry.m ?? null,
                    modificationsCount: typeof entry.c === 'number' ? entry.c : null,
                    awardeeName: entry.w ?? null, descHash: entry.h ?? null,
                });
            } else {
                watchSeen.set(String(entry), {
                    isActive: null, noticeTypeCode: null, responseDate: null, modifiedDate: null,
                    modificationsCount: null, awardeeName: null, descHash: null,
                });
            }
        }
        log.info(
            `Watch mode "${watchLabel}" (${key}): baseline from ${existing.lastRunAt ?? 'an earlier run'} holds `
            + `${watchSeen.size} already-delivered opportunity(ies). Only opportunities NOT in that baseline are returned and charged`
            + (watchChanges ? ', plus any already-delivered opportunity whose active/notice-type status, response deadline, modified date, modification count, awardee or description changed.' : '.'),
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

// This Actor is published PAY_PER_EVENT ($0.0015/row, single "result" event, see meta.json) but
// until this fix it only ever called Actor.pushData(results) in one bulk call at the end -- never
// Actor.charge(). Every other PPE Actor in the fleet routes pushes through a pushResult() that
// calls Actor.charge() first (federal-register-scraper/grants-gov-scraper/etc. all use this exact
// pattern); this one was published (cycle 540) without it, so every real buyer since would have
// gotten every row for free. Found and fixed cycle 542, before any paying run occurred (0 revenue
// booked fleet-wide as of this cycle, so no refund owed). `isPPE` guards local/non-PPE test runs,
// same as the sibling Actors.
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

const PAGE_SIZE = 100;

// Pulled out so the real run and a watch-mode baseline seed walk share the exact same paging
// logic and can never drift out of sync -- only the `limit` differs (maxResults vs. SEED_CAP).
async function fetchRows(limit) {
    const rows = [];
    let page = 0;
    let total = Infinity;
    while (rows.length < limit && rows.length < total) {
        const url = buildSearchUrl(page, PAGE_SIZE);
        const data = await apiGet(url);
        if (!data) { log.warning(`Page ${page} failed after retries; stopping.`); break; }
        total = Math.min(data.page?.totalElements ?? 0, 10000);
        const pageRows = data._embedded?.results ?? [];
        if (pageRows.length === 0) break;
        for (const row of pageRows) {
            rows.push(normalizeRow(row));
            if (rows.length >= limit) break;
        }
        log.info(`Page ${page}: +${pageRows.length} rows (total so far ${rows.length}/${Math.min(total, limit)})`);
        page += 1;
        if (page * PAGE_SIZE >= 10000) { log.warning('Hit SAM.gov\'s 10,000-row backend depth cap; narrow keyword/filters for more.'); break; }
        await sleep(300); // stay well under any rate limit; verified spacing from the feasibility check
    }
    return rows;
}

// Seeding only needs ids + the watched fields, both already on the thin search row, so it never
// needs enrichDetail on -- unlike grants-gov-scraper's award-amount filter, nothing this Actor
// watches lives only on the detail record. It walks the WHOLE match set (up to SEED_CAP, the same
// as SAM.gov's own hard depth cap), unbounded by maxResults -- a baseline that stopped early would
// report every opportunity past the stopping point as "new" on the first incremental run.
if (watchMode && seeding) {
    const baselineRows = await fetchRows(SEED_CAP);
    for (const row of baselineRows) {
        if (row.opportunityId) watchSeen.set(row.opportunityId, snapshotOf(row));
    }
    log.info(`Baseline walk: ${watchSeen.size} opportunity id(s) recorded.`);
}

let results = [];
if (!seeding) {
    results = await fetchRows(maxResults);
    if (enrichDetail) {
        log.info(`Enriching ${results.length} rows with detail-call fields (naics, set-aside, place of performance, contacts)...`);
        for (const item of results) {
            await enrichOne(item);
            await sleep(200);
        }
    }

    let beforePush = 0;
    for (const item of results) {
        if (watchMode && item.opportunityId && watchSeen.has(item.opportunityId)) {
            const id = item.opportunityId;
            const nextSnap = snapshotOf(item);
            // Already delivered under this watch label. Normally dropped before any charge, so an
            // opportunity is never paid for twice -- UNLESS watchChanges is on and one of the
            // watched fields moved since we last saw it, in which case it's re-delivered (charged
            // like a new row) tagged with exactly what changed.
            const change = watchChanges ? changesBetween(watchSeen.get(id), nextSnap) : null;
            if (!change) {
                // Snapshot is kept current either way, so turning watchChanges on later detects
                // only drift from that point, not a backlog since the baseline.
                watchSeen.set(id, nextSnap);
                skippedSeen += 1;
                continue;
            }
            const cont = await pushResult({ ...item, _watchChangeType: change.types, _watchPrevious: change.previous });
            if (pushed > beforePush) { watchSeen.set(id, nextSnap); changedCount += 1; }
            beforePush = pushed;
            if (!cont) break;
            continue;
        }
        const cont = await pushResult(item);
        // Recorded as delivered only after the charge actually succeeded -- anything dropped by
        // maxResults or a charge limit stays "new" for the next run.
        if (watchMode && item.opportunityId && pushed > beforePush) watchSeen.set(item.opportunityId, snapshotOf(item));
        beforePush = pushed;
        if (!cont) break; // maxResults reached or a per-run charge limit hit
    }
}

if (watchMode) {
    await saveWatchRecord(seeding ? 'seeded' : 'incremental');
    if (seeding) {
        log.info(
            `Baseline saved for watch label "${watchLabel}": ${watchSeen.size} opportunity(ies) recorded as already-seen, `
            + '0 results returned, 0 charged. The next run on this label and these filters returns only new opportunities.'
            + (watchSeen.size >= SEED_CAP
                ? ` NOTE: the baseline stopped at the ${SEED_CAP}-opportunity cap. Narrow the query (a keyword, a `
                + 'NAICS code, a set-aside/notice type) so the whole result set fits, or the first incremental run '
                + 'will report opportunities past the cap as new.'
                : ''),
        );
    } else {
        log.info(
            `Watch label "${watchLabel}": ${pushed - changedCount} new opportunity(ies)`
            + (watchChanges ? ` and ${changedCount} changed opportunity(ies) (active/notice-type status, response deadline, modified date, modification count, awardee or description)` : '')
            + ` since the last run (${skippedSeen} already-delivered, unchanged row(s) skipped, uncharged); baseline now holds ${watchSeen.size}.`,
        );
    }
}

log.info(`Done. Pushed ${pushed} opportunities.`);

await Actor.exit();
