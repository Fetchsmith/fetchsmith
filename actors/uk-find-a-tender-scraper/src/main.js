import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';

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
const cpvCodes = (input.cpvCodes ?? []).map((c) => String(c).trim()).filter(Boolean);
const searchQuery = input.searchQuery ? String(input.searchQuery).toLowerCase().trim() : null;
const minValueGbp = input.minValueGbp != null ? Number(input.minValueGbp) : null;
const maxValueGbp = input.maxValueGbp != null ? Number(input.maxValueGbp) : null;
const openOnly = input.openOnly === true;
const maxResults = Math.min(Math.max(Number(input.maxResults ?? 100), 1), 5000);
const maxPagesScanned = Math.min(Math.max(Number(input.maxPagesScanned ?? 50), 1), 500);

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
            u.searchParams.set('updatedFrom', isoSeconds(Date.now() - updatedWithinDays * 86400_000));
            if (stages.length) u.searchParams.set('stages', stages.join(','));
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
            u.searchParams.set('publishedFrom', isoSeconds(Date.now() - updatedWithinDays * 86400_000));
            // publishedTo MUST be sent explicitly. Without it, Contracts Finder defaults it to
            // "now" and omits links.next entirely, silently capping every run at 100 rows.
            u.searchParams.set('publishedTo', isoSeconds(Date.now()));
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

function normalize(release, source) {
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
        tenderStartDate: tender.tenderPeriod?.startDate ?? null,
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
    };
}

// Client-side filters. The FTS API only supports stages/updatedFrom/updatedTo server-side,
// so anything else has to be applied to the fetched page.
function matches(row) {
    if (cpvCodes.length) {
        const hit = cpvCodes.some((wanted) => row.cpvCodes.some((have) => have.startsWith(wanted.replace(/0+$/, '')) || have === wanted));
        if (!hit) return false;
    }
    if (searchWords.length) {
        const hay = [row.title, row.description, row.buyerName, row.cpvDescription, ...row.lotTitles].join(' ').toLowerCase();
        if (!searchWords.every((w) => hay.includes(w))) return false;
    }
    if (minValueGbp != null && !(typeof row.valueAmount === 'number' && row.valueAmount >= minValueGbp)) return false;
    if (maxValueGbp != null && !(typeof row.valueAmount === 'number' && row.valueAmount <= maxValueGbp)) return false;
    if (openOnly) {
        if (!row.deadlineDate) return false;
        if (new Date(row.deadlineDate).getTime() <= Date.now()) return false;
    }
    return true;
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
    `Sources=[${sources.join(',') || 'none'}] stages=[${stages.join(',') || 'all'}] `
    + `updatedWithinDays=${updatedWithinDays} maxResults=${maxResults}`,
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

        const resp = await gotScraping({
            url: pageUrl,
            responseType: 'text',
            throwHttpErrors: false,
            headers: { accept: 'application/json' },
            retry: { limit: 0 },
            timeout: { request: 45000 },
        });

        if (resp.statusCode === 429) {
            const retryAfter = Number(resp.headers['retry-after']) || 120;
            log.warning(`Rate-limited by ${source.label} (429). Waiting ${retryAfter}s before retry ${attempt}/4.`);
            await sleep((retryAfter + 2) * 1000);
            continue;
        }
        if (resp.statusCode !== 200) {
            log.warning(`${source.label} API returned ${resp.statusCode}: ${String(resp.body).slice(0, 300)}`);
            return null;
        }
        try {
            return JSON.parse(resp.body);
        } catch {
            log.warning(`${source.label} returned a non-JSON body (${String(resp.body).slice(0, 200)})`);
            return null;
        }
    }
    log.warning(`Still rate-limited by ${source.label} after 4 retries; stopping that source early rather than returning a partial page silently.`);
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

if (!sources.length) {
    log.warning('No valid "sources" selected — pick "fts" (Find a Tender), "cf" (Contracts Finder), or both.');
}

// Row-level round-robin across sources, not page-level. A single Find a Tender page already
// returns up to 100 releases — with both sources on and a small maxResults (the common case),
// draining FTS's first page before ever fetching Contracts Finder meant a "both sources" run
// could come back 100% FTS with no CF rows at all, since FTS is the much thinner feed
// (~7-8 tender-stage notices/day vs CF's ~18+100/day). Buffer each source's current page and
// pop one release at a time round-robin, only fetching a source's next page when its buffer
// empties, so both sources contribute from the very first pushed rows.
const cursors = sources.map((key) => ({ key, source: SOURCES[key], url: SOURCES[key].buildUrl(), buffer: [], pushed: 0, done: false }));
for (const c of cursors) log.info(`${c.source.label}: ${c.url}`);

async function fillBuffer(c) {
    while (!c.buffer.length && c.url && page < maxPagesScanned) {
        const body = await fetchPage(c.url, c.source);
        if (!body) { c.url = null; break; }
        const releases = body.releases ?? [];
        page += 1;
        scanned += releases.length;
        log.info(`${c.source.label} page ${page}: scanned ${releases.length} releases (${scanned} total so far)`);
        c.url = body.links?.next ?? null;
        if (!releases.length) break;
        c.buffer = releases;
    }
    if (!c.buffer.length) c.done = true;
}

while (keepGoing && pushed < maxResults && cursors.some((c) => !c.done)) {
    for (const c of cursors) {
        if (c.done || !keepGoing || pushed >= maxResults) continue;
        if (!c.buffer.length) await fillBuffer(c);
        if (c.done || !c.buffer.length) continue;

        const release = c.buffer.shift();
        // The same OCID can be re-published (amendments); keep the first (newest) copy only.
        const key2 = release.id ?? release.ocid;
        const isDup = (key2 && seen.has(key2)) || (release.ocid && seen.has(release.ocid));
        if (key2) seen.add(key2);
        if (release.ocid) seen.add(release.ocid);
        if (isDup) continue;

        const row = normalize(release, c.source);
        if (!matches(row)) { filtered += 1; continue; }
        keepGoing = await pushResult(row);
        c.pushed += 1;
    }
}
log.info(`Pushed ${pushed}/${maxResults}, filtered out ${filtered}, after ${page} page(s) scanned.`);
for (const c of cursors) perSource[c.key] = c.pushed;

if (pushed === 0) {
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

log.info(
    `Done. Scanned ${scanned} releases over ${page} page(s), pushed ${pushed} `
    + `(${sources.map((s) => `${SOURCES[s].label}: ${perSource[s] ?? 0}`).join(', ')}).`,
);
await Actor.exit();
