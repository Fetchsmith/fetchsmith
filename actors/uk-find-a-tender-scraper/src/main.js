import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';

await Actor.init();
const input = (await Actor.getInput()) ?? {};

const VALID_STAGES = ['planning', 'tender', 'award'];
const stages = (input.stages ?? ['tender'])
    .map((s) => String(s).toLowerCase().trim())
    .filter((s) => VALID_STAGES.includes(s));
const updatedWithinDays = Math.min(Math.max(Number(input.updatedWithinDays ?? 7), 1), 365);
const cpvCodes = (input.cpvCodes ?? []).map((c) => String(c).trim()).filter(Boolean);
const searchQuery = input.searchQuery ? String(input.searchQuery).toLowerCase().trim() : null;
const minValueGbp = input.minValueGbp != null ? Number(input.minValueGbp) : null;
const maxValueGbp = input.maxValueGbp != null ? Number(input.maxValueGbp) : null;
const openOnly = input.openOnly === true;
const maxResults = Math.min(Math.max(Number(input.maxResults ?? 100), 1), 5000);
const maxPagesScanned = Math.min(Math.max(Number(input.maxPagesScanned ?? 50), 1), 500);

const API = 'https://www.find-tender.service.gov.uk/api/1.0/ocdsReleasePackages';
const PAGE_SIZE = 100; // hard API cap: limit=200 returns HTTP 400

const searchWords = searchQuery ? searchQuery.split(/\s+/).filter(Boolean) : [];

function isoSecondsAgo(days) {
    const d = new Date(Date.now() - days * 86400_000);
    return d.toISOString().slice(0, 19); // API wants YYYY-MM-DDTHH:MM:SS, no timezone suffix
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

function normalize(release) {
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
        ocid: release.ocid ?? null,
        noticeId: release.id ?? null,
        noticeUrl: release.id ? `https://www.find-tender.service.gov.uk/Notice/${release.id}` : null,
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
        contractStartDate: firstAward?.contractPeriod?.startDate ?? lots[0]?.contractPeriod?.startDate ?? null,
        contractEndDate: firstAward?.contractPeriod?.endDate ?? lots[0]?.contractPeriod?.endDate ?? null,

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
        suitableForSme: lots.some((l) => l.suitability?.sme === true) || null,
        suitableForVcse: lots.some((l) => l.suitability?.vcse === true) || null,

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

const startUrl = new URL(API);
startUrl.searchParams.set('limit', String(PAGE_SIZE));
startUrl.searchParams.set('updatedFrom', isoSecondsAgo(updatedWithinDays));
if (stages.length) startUrl.searchParams.set('stages', stages.join(','));

log.info(`Find a Tender: stages=[${stages.join(',') || 'all'}] updatedFrom=${startUrl.searchParams.get('updatedFrom')} maxResults=${maxResults}`);

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// Find a Tender rate-limits hard ("Rate limit of 12 exceeded. Please retry after 120 seconds.")
// and answers with a PLAIN-TEXT body, so responseType:'json' must not be used — an unparsed
// error body would otherwise look like an empty page and end the run with 0 rows silently.
const RATE_WINDOW_MS = 60_000;
const RATE_MAX = 10;
const requestTimes = [];

async function fetchPage(pageUrl) {
    for (let attempt = 1; attempt <= 4; attempt += 1) {
        const now = Date.now();
        while (requestTimes.length && now - requestTimes[0] > RATE_WINDOW_MS) requestTimes.shift();
        if (requestTimes.length >= RATE_MAX) {
            const waitMs = RATE_WINDOW_MS - (now - requestTimes[0]) + 500;
            log.info(`Self-throttling to stay under the API rate limit: waiting ${Math.ceil(waitMs / 1000)}s`);
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
            log.warning(`Rate-limited by Find a Tender (429). Waiting ${retryAfter}s before retry ${attempt}/4.`);
            await sleep((retryAfter + 2) * 1000);
            continue;
        }
        if (resp.statusCode !== 200) {
            log.warning(`Find a Tender API returned ${resp.statusCode}: ${String(resp.body).slice(0, 300)}`);
            return null;
        }
        try {
            return JSON.parse(resp.body);
        } catch {
            log.warning(`Find a Tender returned a non-JSON body (${String(resp.body).slice(0, 200)})`);
            return null;
        }
    }
    log.warning('Still rate-limited after 4 retries; stopping early rather than returning a partial page silently.');
    return null;
}

let url = startUrl.toString();
let page = 0;
let scanned = 0;
let filtered = 0;
const seen = new Set();
let keepGoing = true;

while (url && keepGoing && pushed < maxResults && page < maxPagesScanned) {
    const body = await fetchPage(url);
    if (!body) break;

    const releases = body.releases ?? [];
    if (!releases.length) break;
    page += 1;
    scanned += releases.length;

    for (const release of releases) {
        // The same OCID can be re-published (amendments); keep the first (newest) copy only.
        const key = release.id ?? release.ocid;
        if (key && seen.has(key)) continue;
        if (key) seen.add(key);

        const row = normalize(release);
        if (!matches(row)) { filtered += 1; continue; }
        keepGoing = await pushResult(row);
        if (!keepGoing) break;
    }

    log.info(`page ${page}: scanned ${releases.length} releases (${scanned} total), pushed ${pushed}/${maxResults}, filtered out ${filtered}`);
    url = body.links?.next ?? null;
}

if (pushed === 0) {
    log.warning(
        `No notices matched. Scanned ${scanned} releases over ${page} page(s) and filtered out ${filtered}. `
        + 'Most common causes, in order: (1) "searchQuery" is too specific — every word must appear in the title, '
        + 'description, buyer name or lot titles; try one word. (2) "cpvCodes" does not match — Find a Tender uses '
        + '8-digit CPV codes and a trailing-zero code like 72000000 is matched as a prefix (72...). '
        + '(3) "openOnly" is true but the notices found are award notices, which have no future deadline — set '
        + '"stages" to ["tender"]. (4) "updatedWithinDays" is too short. Filtered rows are never charged.',
    );
}

log.info(`Done. Scanned ${scanned} releases over ${page} page(s), pushed ${pushed}.`);
await Actor.exit();
