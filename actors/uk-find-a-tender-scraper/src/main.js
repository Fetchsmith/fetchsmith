import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';
import { createHash } from 'node:crypto';

await Actor.init();
const input = (await Actor.getInput()) ?? {};

function uniqStrings(arr) {
    return Array.from(new Set((arr ?? []).filter(Boolean)));
}

const VALID_STAGES = ['planning', 'tender', 'award'];
const stages = (input.stages ?? ['tender'])
    .map((s) => String(s).toLowerCase().trim())
    .filter((s) => VALID_STAGES.includes(s));
const VALID_SOURCES = ['fts', 'cf'];
const sources = uniqStrings((input.sources ?? ['fts', 'cf']).map((s) => String(s).toLowerCase().trim()))
    .filter((s) => VALID_SOURCES.includes(s));
const updatedWithinDays = Math.min(Math.max(Number(input.updatedWithinDays ?? 7), 1), 365);

// Absolute date window. When either bound is given it overrides the relative
// "updatedWithinDays" window. Both portals enforce these server-side and precisely
// (verified live: a 2026-08-10..2026-08-13 window returns only 08-10..08-12 rows on
// both FTS and Contracts Finder), so this is a real filter, not a client-side trim.
function parseBound(raw, label) {
    if (raw == null || String(raw).trim() === '') return null;
    const s = String(raw).trim();
    // Accept YYYY-MM-DD (midnight UTC) or a full ISO datetime.
    const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(s);
    const ms = m ? Date.parse(`${s}T00:00:00Z`) : Date.parse(s);
    if (!Number.isFinite(ms)) {
        throw new Error(`"${label}" is not a valid date: ${JSON.stringify(raw)}. Use YYYY-MM-DD (e.g. 2026-08-01) or a full ISO datetime.`);
    }
    return ms;
}

const dateFromMs = parseBound(input.dateFrom, 'dateFrom');
const dateToMs = parseBound(input.dateTo, 'dateTo');
if (dateFromMs != null && dateToMs != null && dateFromMs > dateToMs) {
    throw new Error(`"dateFrom" (${input.dateFrom}) is after "dateTo" (${input.dateTo}) — the window is empty. Swap them.`);
}
const useAbsoluteWindow = dateFromMs != null || dateToMs != null;
// Lower bound: explicit dateFrom, else now - updatedWithinDays.
const windowFromMs = dateFromMs ?? (Date.now() - updatedWithinDays * 86400_000);
// Upper bound: explicit dateTo, else "now" (which is what both portals already did).
const windowToMs = dateToMs ?? Date.now();
const cpvCodes = (input.cpvCodes ?? []).map((c) => String(c).trim()).filter(Boolean);
// CPV subtree prefix for a wanted code. Trailing zeros are padding, so stripping them
// gives the subtree ("72267000" -> "72267" also matches 72267100/72267200). But a division
// whose second digit is 0 must NOT collapse to one digit: "80000000" -> "8" would match all
// of 80-89, i.e. an education filter returning 85xxxxxx health notices (measured: 9 of 10 rows).
// The division is the shortest meaningful CPV prefix, so never go below 2 digits.
const cpvPrefixes = cpvCodes.map((c) => {
    const stripped = c.replace(/0+$/, '');
    return stripped.length >= 2 ? stripped : c.slice(0, 2);
});
const searchQuery = input.searchQuery ? String(input.searchQuery).normalize('NFC').toLowerCase().trim() : null;
// Narrower than searchQuery on purpose: searchQuery ORs across title/description/CPV/lots too,
// so searchQuery="NHS" also returns council notices that merely mention the NHS.
const buyerNameFilter = input.buyerName ? String(input.buyerName).normalize('NFC').toLowerCase().trim() : null;
// OR-of-phrases variant of searchQuery: searchQuery is AND-of-words within one phrase
// (competitor gap check, cycle 415 — ciel_labs/neverempty both expose a comma/array "any of
// these phrases" mode, which our single AND-only searchQuery can't express: e.g. "software OR
// cyber OR cleaning" needs 3 separate runs today). Each phrase can itself be multi-word (still
// substring-matched as a whole phrase, not split into words) so "IT support" stays one unit.
const keywordsAny = (input.keywordsAny ?? [])
    .map((k) => String(k).normalize('NFC').toLowerCase().trim())
    .filter(Boolean);
// Regions filter (competitor gap, cycle 415 — neverempty's "regions"): OR-match against the
// notice's own deliveryRegions/deliveryLocations arrays, both already computed for free by
// normalize() as output fields but never filterable on until now.
const regionFilter = (input.regions ?? [])
    .map((r) => String(r).normalize('NFC').toLowerCase().trim())
    .filter(Boolean);
const minValueGbp = input.minValueGbp != null ? Number(input.minValueGbp) : null;
const maxValueGbp = input.maxValueGbp != null ? Number(input.maxValueGbp) : null;
if (minValueGbp != null && maxValueGbp != null && minValueGbp > maxValueGbp) {
    throw new Error(`"minValueGbp" (${minValueGbp}) is greater than "maxValueGbp" (${maxValueGbp}) — no notice can ever match. Swap them.`);
}
const openOnly = input.openOnly === true;
const includeRawOcds = input.includeRawOcds === true;
const maxResults = Math.min(Math.max(Number(input.maxResults ?? 100), 1), 5000);
const maxPagesScanned = Math.min(Math.max(Number(input.maxPagesScanned ?? 50), 1), 500);
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

const PAGE_SIZE = 100; // hard API cap on both portals: limit=200 returns HTTP 400

// The two official UK procurement portals. Find a Tender carries above-threshold notices
// (a thin feed, ~7-8 tender-stage notices/day); Contracts Finder carries the much larger
// sub-threshold flow (~18 tender-stage and 100+ award notices/day). Both publish the same
// OCDS 1.1 release shape, so one normalizer handles both.
const SOURCES = {
    fts: {
        key: 'fts',
        label: 'Find a Tender',
        api: 'https://www.find-tender.service.gov.uk/api/1.0/ocdsReleasePackages',
        // FTS rate-limits hard: "Rate limit of 12 exceeded. Please retry after 120 seconds."
        rateMax: 10,
        requestTimes: [],
        buildUrl() {
            const u = new URL(this.api);
            u.searchParams.set('limit', String(PAGE_SIZE));
            u.searchParams.set('updatedFrom', isoSeconds(windowFromMs));
            // Only sent when the caller asked for an explicit upper bound. Omitting it (the
            // previous always-on behaviour) means "up to now", which is the same thing.
            if (dateToMs != null) u.searchParams.set('updatedTo', isoSeconds(windowToMs));
            // FTS wants each stage as its own repeated "stages" param — a single comma-joined
            // value (which works fine on Contracts Finder, below) is silently treated as one
            // unrecognized stage string and matches NOTHING, with no error (verified live,
            // cycle 359: stages=tender,award -> 0 releases; stages=tender&stages=award -> 5).
            for (const s of stages) u.searchParams.append('stages', s);
            return u.toString();
        },
        noticeUrl: (release) => (release.id ? `https://www.find-tender.service.gov.uk/Notice/${release.id}` : null),
    },
    cf: {
        key: 'cf',
        label: 'Contracts Finder',
        api: 'https://www.contractsfinder.service.gov.uk/Published/Notices/OCDS/Search',
        rateMax: 20,
        requestTimes: [],
        buildUrl() {
            const u = new URL(this.api);
            u.searchParams.set('limit', String(PAGE_SIZE));
            u.searchParams.set('publishedFrom', isoSeconds(windowFromMs));
            // publishedTo MUST be sent explicitly. Without it, Contracts Finder defaults it to
            // "now" and omits links.next entirely, silently capping every run at 100 rows.
            u.searchParams.set('publishedTo', isoSeconds(windowToMs));
            if (stages.length) u.searchParams.set('stages', stages.join(','));
            return u.toString();
        },
        // The OCDS release id is "<notice guid>-<internal number>"; only the guid resolves.
        // Passing the full id lands on a "You have been signed out" page instead of the notice.
        noticeUrl: (release) => {
            const guid = String(release.id ?? '').replace(/-\d+$/, '');
            return guid ? `https://www.contractsfinder.service.gov.uk/notice/${guid}` : null;
        },
    },
};

const searchWords = searchQuery ? searchQuery.split(/\s+/).filter(Boolean) : [];

function isoSeconds(ms) {
    // Both APIs want YYYY-MM-DDTHH:MM:SS with no timezone suffix.
    return new Date(ms).toISOString().slice(0, 19);
}

function uniq(arr) {
    return Array.from(new Set((arr ?? []).filter((v) => v != null && v !== '')));
}

function party(release, role) {
    return (release.parties ?? []).find((p) => (p.roles ?? []).includes(role)) ?? null;
}

function partiesWithRole(release, role) {
    return (release.parties ?? []).filter((p) => (p.roles ?? []).includes(role));
}

// Collect every CPV code on the notice: the tender-level classification plus each item's
// additionalClassifications (which is where the specific codes actually live).
function allCpv(tender) {
    const out = [];
    if (tender?.classification?.scheme === 'CPV' && tender.classification.id) out.push(String(tender.classification.id));
    for (const item of tender?.items ?? []) {
        if (item.classification?.scheme === 'CPV' && item.classification.id) out.push(String(item.classification.id));
        for (const c of item.additionalClassifications ?? []) {
            if (c.scheme === 'CPV' && c.id) out.push(String(c.id));
        }
    }
    return uniq(out);
}

function deliveryRegions(tender) {
    const out = [];
    for (const item of tender?.items ?? []) {
        for (const addr of item.deliveryAddresses ?? []) {
            if (addr.region) out.push(addr.region);
        }
    }
    return uniq(out);
}

function deliveryLocations(tender) {
    const out = [];
    for (const item of tender?.items ?? []) {
        if (item.deliveryLocation?.description) out.push(item.deliveryLocation.description);
    }
    return uniq(out);
}

// On award notices the money is usually NOT on awards[].value — it sits on contracts[].value,
// with awards[] carrying only id/status/suppliers. Prefer an explicit award value; otherwise
// total the signed contracts (contractCount tells the reader how many were added up).
function awardValue(release) {
    for (const a of release.awards ?? []) {
        if (typeof a.value?.amount === 'number') return [a.value.amount, a.value.currency ?? null, 'award'];
    }
    const withValue = (release.contracts ?? []).filter((c) => typeof c.value?.amount === 'number');
    if (withValue.length) {
        const total = withValue.reduce((s, c) => s + c.value.amount, 0);
        return [total, withValue[0].value.currency ?? null, 'contracts'];
    }
    return [null, null, null];
}

function normalize(release, source, includeRaw) {
    const tender = release.tender ?? {};
    const buyer = party(release, 'buyer');
    const awards = release.awards ?? [];
    const contracts = release.contracts ?? [];
    // Suppliers appear either as awards[].suppliers or as parties with the "supplier" role, depending on notice.
    const suppliers = [
        ...awards.flatMap((a) => a.suppliers ?? []),
        ...partiesWithRole(release, 'supplier'),
    ];
    const [awardAmount, awardCurrency, awardValueSource] = awardValue(release);
    const signedDates = contracts.map((c) => c.dateSigned).filter(Boolean).sort();
    const firstAward = awards[0] ?? null;
    const lots = tender.lots ?? [];
    const addr = buyer?.address ?? {};
    const contact = buyer?.contactPoint ?? {};
    const cpv = allCpv(tender);

    return {
        source: source.key,
        sourceName: source.label,
        ocid: release.ocid ?? null,
        noticeId: release.id ?? null,
        noticeUrl: source.noticeUrl(release),
        stage: uniq(release.tag),
        publishedDate: release.date ?? null,
        language: release.language ?? null,

        title: tender.title ?? null,
        description: tender.description ?? release.description ?? null,
        status: tender.status ?? null,
        procurementMethod: tender.procurementMethod ?? null,
        procurementMethodDetails: tender.procurementMethodDetails ?? null,
        mainProcurementCategory: tender.mainProcurementCategory ?? firstAward?.mainProcurementCategory ?? null,
        legalBasis: tender.legalBasis?.id ?? null,

        cpvCode: cpv[0] ?? null,
        cpvDescription: tender.classification?.description ?? null,
        cpvCodes: cpv,

        valueAmount: tender.value?.amount ?? null,
        valueCurrency: tender.value?.currency ?? null,

        deadlineDate: tender.tenderPeriod?.endDate ?? null,
        awardPeriodStart: tender.awardPeriod?.startDate ?? null,
        // Contracts Finder has no lots and carries the period on tender.contractPeriod instead.
        contractStartDate: firstAward?.contractPeriod?.startDate ?? lots[0]?.contractPeriod?.startDate ?? tender.contractPeriod?.startDate ?? null,
        contractEndDate: firstAward?.contractPeriod?.endDate ?? lots[0]?.contractPeriod?.endDate ?? tender.contractPeriod?.endDate ?? null,

        buyerName: buyer?.name ?? release.buyer?.name ?? null,
        buyerId: buyer?.id ?? release.buyer?.id ?? null,
        buyerEmail: contact.email ?? null,
        buyerPhone: contact.telephone ?? null,
        buyerUrl: buyer?.details?.url ?? contact.url ?? null,
        buyerStreet: addr.streetAddress ?? null,
        buyerLocality: addr.locality ?? null,
        buyerPostalCode: addr.postalCode ?? null,
        buyerRegion: addr.region ?? null,
        buyerCountry: addr.countryName ?? addr.country ?? null,

        deliveryRegions: deliveryRegions(tender),
        deliveryLocations: deliveryLocations(tender),

        lotCount: lots.length,
        lotTitles: uniq(lots.map((l) => l.title)),
        // Find a Tender puts suitability per lot; Contracts Finder puts it once on the tender.
        suitableForSme: (tender.suitability?.sme === true || lots.some((l) => l.suitability?.sme === true)) || null,
        suitableForVcse: (tender.suitability?.vcse === true || lots.some((l) => l.suitability?.vcse === true)) || null,

        awardStatus: firstAward?.status ?? null,
        awardValueAmount: awardAmount,
        awardValueCurrency: awardCurrency,
        awardValueSource,
        awardedSuppliers: uniq(suppliers.map((s) => s.name)),
        contractCount: contracts.length,
        contractDateSigned: signedDates[0] ?? null,
        aboveThreshold: firstAward?.aboveThreshold ?? null,

        documentUrls: uniq((tender.documents ?? []).map((d) => d.url)),

        ...(includeRaw ? { rawOcds: release } : {}),
    };
}

// Client-side filters. The FTS API only supports stages/updatedFrom/updatedTo server-side,
// so anything else has to be applied to the fetched page.
function matches(row) {
    if (cpvCodes.length) {
        const hit = cpvPrefixes.some((prefix) => row.cpvCodes.some((have) => have.startsWith(prefix)));
        if (!hit) return false;
    }
    if (searchWords.length || keywordsAny.length) {
        const hay = [row.title, row.description, row.buyerName, row.cpvDescription, ...row.lotTitles].join(' ').normalize('NFC').toLowerCase();
        if (searchWords.length && !searchWords.every((w) => hay.includes(w))) return false;
        if (keywordsAny.length && !keywordsAny.some((k) => hay.includes(k))) return false;
    }
    if (buyerNameFilter && !String(row.buyerName ?? '').normalize('NFC').toLowerCase().includes(buyerNameFilter)) return false;
    if (regionFilter.length) {
        const hay = [...row.deliveryRegions, ...row.deliveryLocations].join(' ').normalize('NFC').toLowerCase();
        if (!regionFilter.some((r) => hay.includes(r))) return false;
    }
    if (minValueGbp != null && !(typeof row.valueAmount === 'number' && row.valueAmount >= minValueGbp)) return false;
    if (maxValueGbp != null && !(typeof row.valueAmount === 'number' && row.valueAmount <= maxValueGbp)) return false;
    if (openOnly) {
        if (!row.deadlineDate) return false;
        if (new Date(row.deadlineDate).getTime() <= Date.now()) return false;
    }
    return true;
}

// ---------------------------------------------------------------------------
// Watch mode: "only what is new since my last run", per saved query. Same
// design as federal-register-scraper/grants-gov-scraper/eu-ted-tenders-scraper:
// baseline (notice ids already delivered) kept in a NAMED key-value store so
// it survives across scheduled runs; the default KV store is per-run and
// would reset the baseline every time.
const WATCH_STORE = 'fetchsmith-uk-tender-watch';
const SEED_CAP = 20000; // bound a seed walk against an unfiltered/very broad query
const SEED_PAGE_CAP = 1000; // pages scanned (combined across sources) during a seed walk — well above maxPagesScanned's own 500 schema max, so seeding is never less thorough than the widest normal run could be
const WATCH_KEEP = 60000; // bound the record size; oldest ids fall off first

// updatedWithinDays is a ROLLING window (its resolved value changes every day),
// so it is deliberately excluded from the fingerprint — same trap cycles
// 297/298 found the hard way on other Actors. dateFromMs/dateToMs are only
// non-null when the buyer set an explicit bound (see parseBound above), so
// including them is safe: an explicit absolute window is a real criteria
// choice, not a moving target. searchQuery/buyerNameFilter are stored in
// their already-normalized (NFC-folded, lowercased) form since that is what
// actually drives matching, not the buyer's raw input casing.
const watchCriteria = {
    sources: [...sources].sort(),
    stages: [...stages].sort(),
    cpvCodes: [...cpvCodes].sort(),
    searchQuery,
    buyerName: buyerNameFilter,
    minValueGbp,
    maxValueGbp,
    openOnly,
    dateFromMs,
    dateToMs,
    // keywordsAny/regionFilter (cycle 415) join the fingerprint only when set, so every watch
    // baseline saved before this cycle keeps its existing key (same rule as every other
    // new-filter cycle in this fleet, e.g. ats-jobs-scraper cycle 408, steam cycle 404).
    ...(keywordsAny.length ? { keywordsAny: [...keywordsAny].sort() } : {}),
    ...(regionFilter.length ? { regionFilter: [...regionFilter].sort() } : {}),
};

// Apify KV keys allow [a-zA-Z0-9!-_.'()] only, so the label is sanitised rather than trusted directly.
function watchKeyFor(label, criteria) {
    const safe = label.toLowerCase().replace(/[^a-z0-9_.-]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 40) || 'default';
    const fp = createHash('sha1').update(JSON.stringify(criteria, Object.keys(criteria).sort())).digest('hex').slice(0, 10);
    return { key: `watch-${safe}-${fp}`, fingerprint: fp };
}

const watchMode = watchLabel.length > 0;
let watchStore = null;
let watchKey = null;
let watchRecord = null;
let seeding = false;
let skippedSeen = 0;
const watchSeen = new Set(); // notice ids (ocid, falling back to noticeId) already delivered under this label+fingerprint

// Ids evicted by the WATCH_KEEP cap on THIS run, and cumulatively over the life of the record.
// Set by saveWatchRecord(), so read them only after it has been awaited.
let baselineTruncated = 0;
let baselineTruncatedTotal = 0;

async function saveWatchRecord(status) {
    const ids = Array.from(watchSeen).slice(-WATCH_KEEP);
    // The slice above silently drops the OLDEST ids once the baseline passes WATCH_KEEP. Those
    // notices were already delivered and paid for, but the next run no longer recognises them and
    // will hand them over -- and charge for them -- a second time. Count it and say so.
    baselineTruncated = watchSeen.size - ids.length;
    baselineTruncatedTotal = (watchRecord.truncatedTotal ?? 0) + baselineTruncated;
    if (baselineTruncated > 0) {
        log.warning(
            `Baseline size cap reached: ${baselineTruncated.toLocaleString('en-US')} of the oldest already-delivered `
            + `notice id(s) were dropped to keep the watch record at ${WATCH_KEEP.toLocaleString('en-US')} `
            + `(${baselineTruncatedTotal.toLocaleString('en-US')} dropped in total so far). Those notices are no longer `
            + 'recognised as seen, so a later run will deliver and CHARGE for them again. Narrow the watch (a CPV code, '
            + 'a buyer name, a shorter "updatedWithinDays", one portal in "sources") so the result set stays under the cap.',
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
        seenIds: ids,
        truncatedLastRun: baselineTruncated,
        truncatedTotal: baselineTruncatedTotal,
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
            + `${watchSeen.size} already-delivered notice(s). Only notices NOT in that baseline are returned and charged.`,
        );
    } else {
        watchRecord = { fingerprint, firstSeededAt: new Date().toISOString(), runCount: 0 };
        seeding = true;
        log.info(
            `Watch mode "${watchLabel}" (${key}): FIRST run for this label and filter set, so this is a baseline run. `
            + 'It records which notices already match and returns ZERO results (you are charged nothing). Run it '
            + 'again on the same label and filters — on a schedule, typically — to get only what is new since now.',
        );
    }
}

// First FREE_PER_RUN matching records of every run are free (matches the leading
// competitor's trial hook) so a buyer can see real data shape before paying for any of it.
const FREE_PER_RUN = 25;
let pushed = 0;
let freeGiven = 0;
const isPPE = Actor.getChargingManager().getPricingInfo().isPayPerEvent;
async function pushResult(item) {
    if (isPPE) {
        if (freeGiven < FREE_PER_RUN) {
            freeGiven += 1;
            await Actor.pushData(item); pushed += 1;
            return pushed < maxResults;
        }
        const r = await Actor.charge({ eventName: 'result', count: 1 });
        // Both of these end the walk; only the charge limit is a cause the buyer set on the RUN
        // rather than in the input, so RUN_SUMMARY has to tell them apart.
        if (r.chargedCount === 0) { chargeLimitReached = true; return false; }
        await Actor.pushData(item); pushed += 1;
        if (r.eventChargeLimitReached) chargeLimitReached = true;
        return !r.eventChargeLimitReached && pushed < maxResults;
    }
    await Actor.pushData(item); pushed += 1;
    return pushed < maxResults;
}

log.info(
    `Sources=[${sources.join(',') || 'none'}] stages=[${stages.join(',') || 'all'}] `
    + (useAbsoluteWindow
        ? `window=${isoSeconds(windowFromMs)}..${isoSeconds(windowToMs)} (absolute, overrides updatedWithinDays) `
        : `updatedWithinDays=${updatedWithinDays} `)
    + `maxResults=${maxResults}`,
);

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// Both portals rate-limit and answer errors with a PLAIN-TEXT body, so responseType:'json'
// must not be used — an unparsed error body would otherwise look like an empty page and end
// the run with 0 rows silently. Each source carries its own request-time window.
const RATE_WINDOW_MS = 60_000;

async function fetchPage(pageUrl, source) {
    const { requestTimes, rateMax } = source;
    for (let attempt = 1; attempt <= 4; attempt += 1) {
        const now = Date.now();
        while (requestTimes.length && now - requestTimes[0] > RATE_WINDOW_MS) requestTimes.shift();
        if (requestTimes.length >= rateMax) {
            const waitMs = RATE_WINDOW_MS - (now - requestTimes[0]) + 500;
            log.info(`Self-throttling ${source.label} to stay under its rate limit: waiting ${Math.ceil(waitMs / 1000)}s`);
            await sleep(waitMs);
        }
        requestTimes.push(Date.now());

        let resp;
        try {
            resp = await gotScraping({
                url: pageUrl,
                responseType: 'text',
                throwHttpErrors: false,
                headers: { accept: 'application/json' },
                retry: { limit: 0 },
                timeout: { request: 45000 },
            });
        } catch (err) {
            // A network-level failure (timeout, ECONNRESET, DNS) throws instead of resolving with
            // a status code — without this catch it crashes the whole run instead of retrying like
            // a 429/5xx does, even though the same backoff is exactly as valid here.
            const waitS = attempt * 10;
            log.warning(`${source.label} request failed (${err.message}); retrying in ${waitS}s (${attempt}/4).`);
            await sleep(waitS * 1000);
            continue;
        }

        if (resp.statusCode === 429) {
            const retryAfter = Number(resp.headers['retry-after']) || 120;
            log.warning(`Rate-limited by ${source.label} (429). Waiting ${retryAfter}s before retry ${attempt}/4.`);
            await sleep((retryAfter + 2) * 1000);
            continue;
        }
        if (resp.statusCode !== 200) {
            log.warning(`${source.label} API returned ${resp.statusCode}: ${String(resp.body).slice(0, 300)}`);
            // WHY this source died, carried into RUN_SUMMARY. Without it the record could only
            // say "fts stopped early", which is the same sentence for a 500 and a bad filter.
            source.lastError = `HTTP ${resp.statusCode}: ${String(resp.body).slice(0, 120).replace(/\s+/g, ' ').trim()}`;
            return null;
        }
        try {
            return JSON.parse(resp.body);
        } catch {
            log.warning(`${source.label} returned a non-JSON body (${String(resp.body).slice(0, 200)})`);
            source.lastError = `non-JSON body: ${String(resp.body).slice(0, 120).replace(/\s+/g, ' ').trim()}`;
            return null;
        }
    }
    // Reached after 4 failed attempts from either cause — a 429 or a network-level error — so the
    // wording must not claim rate-limiting specifically.
    log.warning(`${source.label} kept rate-limiting/failing after 4 retries; stopping that source early rather than returning a partial page silently.`);
    source.lastError = 'rate-limited or unreachable after 4 retries';
    return null;
}

let page = 0;
let scanned = 0;
let filtered = 0;
// Deduped across both portals: a contract can legitimately appear on each, and OCIDs are
// portal-prefixed, so the ocid is the only key that could collide — check it as well as the id.
const seen = new Set();
const perSource = {};
let keepGoing = true;

// ---------------------------------------------------------------------------
// Completeness contract (cycle 651), same shape as sam-gov-opportunities-scraper /
// nih-reporter-scraper / clinicaltrials-scraper: a RUN_SUMMARY key-value record, a status
// message, and the same object on the webhook payload.
//
// This Actor's version of the defect was worse than the fleet's because it merges TWO portals.
// `fetchPage` returns null on a 4xx/5xx, a non-JSON body, or four failed retries; `fillBuffer`
// then drops that cursor and the run carries on with the OTHER portal, ends SUCCEEDED, and the
// final log line reads "Find a Tender: 0, Contracts Finder: 47". Find a Tender is a genuinely
// thin feed (~7-8 tender-stage notices/day), so "0" is a completely ordinary number — a dead
// portal and an empty portal were indistinguishable, in the log and in the dataset alike. The
// shared `page < effectivePageCap` budget and `maxResults` end the walk just as quietly.
//
// Neither portal declares a match count (both are pure cursor walks over `links.next` — no
// totalElements/hitCount anywhere in the OCDS package, verified live), so there is no "N of M"
// to report. The completeness question here is per-source and binary: did this source's walk
// reach its natural end (`links.next` absent), or did something stop it early?
let complete = true;
let incompleteReason = null;
let incompleteDetail = null;
let chargeLimitReached = false;

// First cause wins: a walk that lost a portal and THEN also hit maxResults must keep reporting
// the dead portal — that is the cause the buyer can act on.
function markIncomplete(reason, detail = null) {
    if (!complete) return;
    complete = false;
    incompleteReason = reason;
    incompleteDetail = detail;
}

if (!sources.length) {
    log.warning('No valid "sources" selected — pick "fts" (Find a Tender), "cf" (Contracts Finder), or both.');
    markIncomplete('no-sources', 'the "sources" input selected neither "fts" nor "cf", so nothing was searched');
}

// Row-level round-robin across sources, not page-level. A single Find a Tender page already
// returns up to 100 releases — with both sources on and a small maxResults (the common case),
// draining FTS's first page before ever fetching Contracts Finder meant a "both sources" run
// could come back 100% FTS with no CF rows at all, since FTS is the much thinner feed
// (~7-8 tender-stage notices/day vs CF's ~18+100/day). Buffer each source's current page and
// pop one release at a time round-robin, only fetching a source's next page when its buffer
// empties, so both sources contribute from the very first pushed rows.
const cursors = sources.map((key) => ({
    key,
    source: SOURCES[key],
    url: SOURCES[key].buildUrl(),
    buffer: [],
    pushed: 0,
    done: false,
    // Per-source completeness state. `exhausted` means this portal answered until it ran out of
    // `links.next` — the only state in which "0 notices" honestly means "this portal has none".
    pages: 0,
    scanned: 0,
    exhausted: false,
    failed: false,
}));
for (const c of cursors) log.info(`${c.source.label}: ${c.url}`);

// During a seed walk the loop is bounded by SEED_CAP/SEED_PAGE_CAP, not the buyer's
// own maxPagesScanned — see the watch-mode block above for why (a baseline that
// stopped early would report every notice past the stopping point as "new" on
// the first incremental run, the cycle 297/298 trap).
const effectivePageCap = seeding ? Math.max(maxPagesScanned, SEED_PAGE_CAP) : maxPagesScanned;

async function fillBuffer(c) {
    while (!c.buffer.length && c.url && page < effectivePageCap) {
        const body = await fetchPage(c.url, c.source);
        if (!body) {
            // The run does NOT abort — the other portal's rows are real and already charged —
            // but this portal's contribution is now unknown, not zero.
            c.failed = true;
            c.url = null;
            markIncomplete(
                'source-failed',
                `${c.source.label} stopped answering after ${c.pages} page(s) (${c.source.lastError ?? 'unknown error'}); `
                + `its notices are missing from this run, and "0 from ${c.source.label}" here does NOT mean it had none`,
            );
            break;
        }
        const releases = body.releases ?? [];
        page += 1;
        c.pages += 1;
        scanned += releases.length;
        c.scanned += releases.length;
        log.info(`${c.source.label} page ${page}: scanned ${releases.length} releases (${scanned} total so far)`);
        c.url = body.links?.next ?? null;
        // Natural end of this portal's walk: no cursor left to follow. Recorded before the
        // empty-page break so a final empty page still counts as exhausted, not as a stop.
        if (!c.url) c.exhausted = true;
        if (!releases.length) break;
        c.buffer = releases;
    }
    // Ran out of the shared page budget with a cursor still to follow — more notices exist and
    // this run will not see them.
    if (!c.buffer.length && c.url && page >= effectivePageCap) {
        markIncomplete(
            'page-cap',
            `the ${effectivePageCap}-page scan budget (maxPagesScanned) ran out with ${c.source.label} still paging`,
        );
    }
    if (!c.buffer.length) c.done = true;
}

while (keepGoing && cursors.some((c) => !c.done) && (seeding ? watchSeen.size < SEED_CAP : pushed < maxResults)) {
    for (const c of cursors) {
        if (c.done || !keepGoing) continue;
        if (seeding ? watchSeen.size >= SEED_CAP : pushed >= maxResults) continue;
        if (!c.buffer.length) await fillBuffer(c);
        if (c.done || !c.buffer.length) continue;

        const release = c.buffer.shift();
        // The same OCID can be re-published (amendments); keep the first (newest) copy only.
        const key2 = release.id ?? release.ocid;
        const isDup = (key2 && seen.has(key2)) || (release.ocid && seen.has(release.ocid));
        if (key2) seen.add(key2);
        if (release.ocid) seen.add(release.ocid);
        if (isDup) continue;

        const row = normalize(release, c.source, includeRawOcds);
        if (!matches(row)) { filtered += 1; continue; }

        // Per-publication id, not ocid: neither portal ever mutates a published release in
        // place (verified live, cycle 359) — an award or amendment always ships as a NEW
        // release id under the SAME ocid as the original tender notice. Keying watch identity
        // on ocid (the pre-cycle-359 behaviour) meant that once a procurement's tender notice
        // had been delivered once, every later award/update/amendment notice sharing that ocid
        // was silently swallowed forever, since its ocid already looked "seen". noticeId is
        // per-publication, so each new release event is correctly treated as new — matching
        // eu-ted-tenders-scraper's precedent (keyed on publication-number, not procedure-id).
        const watchId = watchMode ? (row.noticeId ?? row.ocid) : null;
        if (watchMode && !seeding && watchId && watchSeen.has(watchId)) {
            skippedSeen += 1;
            continue;
        }
        if (seeding) {
            if (watchId) watchSeen.add(watchId);
            continue;
        }
        const beforePush = pushed;
        keepGoing = await pushResult(row);
        c.pushed += 1;
        // Recorded as delivered only after the charge actually succeeded — anything
        // dropped by maxResults or a charge limit stays "new" for the next run.
        if (watchMode && watchId && pushed > beforePush) watchSeen.add(watchId);
    }
}
log.info(`Pushed ${pushed}/${maxResults}, filtered out ${filtered}, after ${page} page(s) scanned.`);
for (const c of cursors) perSource[c.key] = c.pushed;

// Stop causes that can only be judged once the walk is over. A cursor that still has buffered
// releases or a `links.next` to follow is a portal with more notices we never delivered.
//
// `exhausted` deliberately does NOT suppress this. The two flags answer different questions:
// `exhausted` is "did we read this portal's feed to its end", which is what makes a per-source
// `delivered: 0` trustworthy; this check is "did the buyer get every matching notice". Both
// portals routinely fit a short window in one page, so a run can read both feeds to the end and
// STILL be 30 notices short because maxResults cut it off — caught by live run H4J3c67eIEWyYKd33,
// which read all 42 available notices, delivered 12, and reported itself complete. The offline
// fixture could not catch it (its row count was below maxResults, so the buffers drained).
const stoppedShort = cursors.filter((c) => !c.failed && (c.buffer.length || c.url));
// Only meaningful when every source ran out of pages: then nothing is left unread upstream and
// the leftover buffers are the exact count of matching notices the run did not hand over.
const undelivered = cursors.every((c) => c.exhausted || c.failed)
    ? cursors.reduce((n, c) => n + c.buffer.length, 0)
    : null;
if (stoppedShort.length) {
    const rest = stoppedShort.map((c) => c.source.label).join(' and ');
    const short = undelivered ? `; ${undelivered} already-fetched matching notice(s) were not delivered` : '';
    if (chargeLimitReached) {
        markIncomplete('charge-limit', `the run's pay-per-event charge limit was reached with ${rest} still to read${short}`);
    } else if (seeding && watchSeen.size >= SEED_CAP) {
        markIncomplete('seed-cap', `the baseline stopped at the ${SEED_CAP}-notice cap with ${rest} still to read${short}`);
    } else if (!seeding && pushed >= maxResults) {
        markIncomplete('max-results', `maxResults=${maxResults} was reached with ${rest} still to read${short}`);
    } else {
        // No known bound fired but a cursor survived the loop — should be unreachable; say so
        // rather than letting it report as complete.
        markIncomplete('stopped-early', `the walk ended with ${rest} still to read${short} for no recorded reason`);
    }
}

// A seed walk that lost a portal mid-way is not a smaller baseline, it is a WRONG one: every
// notice past the failure point would read as "new" (and be charged) on the first incremental
// run. `page-cap`/`seed-cap` are deliberately excluded -- those are the buyer's own query/budget
// being too broad, already surfaced in RUN_SUMMARY, and a capped-but-real baseline is still
// strictly better than none. Seeding never charges, so refusing to save costs nothing but a re-run.
const seedFailure = seeding && incompleteReason === 'source-failed' ? incompleteDetail : null;

if (watchMode && seedFailure) {
    log.warning(
        `Baseline walk for watch label "${watchLabel}" was cut short (${seedFailure}), so NO baseline was saved. `
        + 'Re-run with the same watchLabel to seed again once the portal is answering -- saving a truncated baseline '
        + 'would make every notice past the failure point look "new" (and billable) on the first incremental run.',
    );
} else if (watchMode) {
    await saveWatchRecord(seeding ? 'seeded' : 'incremental');
    // Computed only AFTER saveWatchRecord() has run -- it is the call that sets baselineTruncated.
    const truncationNote = () => (baselineTruncated > 0
        ? ` WARNING: ${baselineTruncated.toLocaleString('en-US')} of the oldest seen id(s) were dropped at the `
          + `${WATCH_KEEP.toLocaleString('en-US')}-notice baseline cap, so they will be delivered and charged again. `
          + 'Narrow the watch filters.'
        : '');
    if (seeding) {
        log.info(
            `Baseline saved for watch label "${watchLabel}": ${watchSeen.size} notice(s) recorded as already-seen, `
            + '0 results returned, 0 charged. The next run on this label and these filters returns only new notices.'
            + (watchSeen.size >= SEED_CAP
                ? ` NOTE: the baseline stopped at the ${SEED_CAP}-notice cap. Narrow the query (a CPV code, a buyer `
                + 'name, a shorter date window) so the whole result set fits, or the first incremental run will '
                + 'report notices past the cap as new.'
                : '')
            + truncationNote(),
        );
    } else {
        log.info(
            `Watch label "${watchLabel}": ${pushed} new notice(s) since the last run `
            + `(${skippedSeen} already-delivered notice(s) skipped, uncharged); baseline now holds ${watchSeen.size}.`
            + truncationNote(),
        );
    }
}

if (pushed === 0 && !seeding) {
    if (watchMode) {
        log.warning(
            `Nothing new for watch label "${watchLabel}" since its last run — all ${skippedSeen} matching notice(s) `
            + 'had already been delivered. That is the expected result most of the time; you were charged for nothing.',
        );
    } else {
        log.warning(
            `No notices matched. Scanned ${scanned} releases over ${page} page(s) and filtered out ${filtered}. `
            + 'Most common causes, in order: (1) "searchQuery" is too specific — every word must appear in the title, '
            + 'description, buyer name or lot titles; try one word. (2) "cpvCodes" does not match — both portals use '
            + '8-digit CPV codes and a trailing-zero code like 72000000 is matched as a prefix (72...). '
            + '(3) "openOnly" is true but the notices found are award notices, which have no future deadline — set '
            + '"stages" to ["tender"]. (4) "updatedWithinDays" is too short. (5) "sources" excludes the portal your '
            + 'notices are on — Find a Tender is above-threshold only and is a thin feed; Contracts Finder carries the '
            + 'much larger sub-threshold flow. Filtered rows are never charged.',
        );
    }
}

log.info(
    `Done. Scanned ${scanned} releases over ${page} page(s), pushed ${pushed} `
    + `(${sources.map((s) => `${SOURCES[s].label}: ${perSource[s] ?? 0}`).join(', ')}).`,
);

// ---------------------------------------------------------------------------
// RUN_SUMMARY: this run's completeness, in a form a pipeline can read. Fetch with
//   GET /v2/actor-runs/<runId>/key-value-store/records/RUN_SUMMARY
// which needs no webhook. `complete` is deliberately kept out of the run STATUS: a run can be
// SUCCEEDED and short at the same time, and that pair is exactly what this record exists for.
// `sources` is per-portal on purpose — a fleet-standard single `complete` flag would still leave
// "which of the two portals is this number missing?" unanswered.
const runSummary = {
    mode: watchMode ? (seeding ? 'watch-seed' : 'watch-incremental') : 'search',
    // Neither portal publishes a match count, so there is no declaredMatches field here. Present
    // and null would read as "we asked and got nothing"; absent says "this API cannot be asked".
    sources: Object.fromEntries(cursors.map((c) => [c.key, {
        label: c.source.label,
        pages: c.pages,
        scanned: c.scanned,
        delivered: c.pushed,
        // TRUE only if this portal answered until it ran out of `links.next`. When it is false,
        // `delivered: 0` means "unknown", not "this portal had nothing".
        exhausted: c.exhausted,
        failed: c.failed,
        lastError: c.source.lastError ?? null,
    }])),
    sourcesRequested: sources,
    sourcesFailed: cursors.filter((c) => c.failed).map((c) => c.key),
    scanned,
    delivered: pushed,
    filteredOut: filtered,
    pages: page,
    pageCap: effectivePageCap,
    // Matching notices that were fetched but never handed over (maxResults/charge limit cut the
    // run short). `null` means at least one portal still had pages left, so no total is knowable.
    undelivered,
    complete,
    incompleteReason,
    incompleteDetail,
    maxResults,
    chargeLimitReached,
    freeRowsGiven: freeGiven,
    watchLabel: watchMode ? watchLabel : null,
    watchSeeding: watchMode ? seeding : null,
    baselineSize: watchMode ? watchSeen.size : null,
    // Already-delivered ids evicted by the WATCH_KEEP cap: this run, and cumulatively. Anything
    // above 0 means a later run will re-deliver and re-charge those notices.
    baselineTruncated: watchMode ? baselineTruncated : null,
    baselineTruncatedTotal: watchMode ? baselineTruncatedTotal : null,
    skippedSeen: watchMode && !seeding ? skippedSeen : null,
};
await Actor.setValue('RUN_SUMMARY', runSummary);

// A short run still SUCCEEDS (the rows it did get are real and already charged), so the status
// message is the only place the Apify console itself shows the shortfall. There was no
// setStatusMessage call anywhere in this Actor before cycle 651.
if (!complete) {
    await Actor.setStatusMessage(
        seeding
            ? `Baseline INCOMPLETE: ${watchSeen.size.toLocaleString('en-US')} notice(s) recorded — ${incompleteReason}`
              + `${incompleteDetail ? ` (${incompleteDetail})` : ''}. Re-seed before scheduling, or the rest will be charged as new. See RUN_SUMMARY.`
            : `Incomplete: ${pushed.toLocaleString('en-US')} notice(s) delivered — ${incompleteReason}`
              + `${incompleteDetail ? ` (${incompleteDetail})` : ''}. See RUN_SUMMARY for details.`,
    );
} else if (baselineTruncated > 0) {
    // A COMPLETE run can still have evicted ids at the baseline cap, and that costs the buyer money
    // on the NEXT run. Without this branch the console would show nothing at all for it.
    await Actor.setStatusMessage(
        seeding
            ? `Baseline capped: ${baselineTruncated.toLocaleString('en-US')} oldest id(s) dropped at the `
              + `${WATCH_KEEP.toLocaleString('en-US')}-notice limit — they will be charged again as new. Narrow the watch filters. See RUN_SUMMARY.`
            : `${pushed.toLocaleString('en-US')} new notice(s) — but ${baselineTruncated.toLocaleString('en-US')} `
              + `already-delivered id(s) were dropped at the ${WATCH_KEEP.toLocaleString('en-US')}-notice baseline limit `
              + 'and will be charged again. Narrow the watch filters. See RUN_SUMMARY.',
    );
} else {
    log.info(
        `Complete: every notice both portal(s) (${cursors.map((c) => c.source.label).join(', ')}) had for these `
        + 'filters was read to the end of its feed.',
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
        filtered,
        pagesScanned: page,
        watchLabel: watchMode ? watchLabel : null,
        watchSeeding: watchMode ? seeding : null,
        watchNewCount: watchMode && !seeding ? pushed : null,
        // Same object as the RUN_SUMMARY key-value record, so a webhook consumer and a
        // polling consumer read the identical completeness facts.
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
