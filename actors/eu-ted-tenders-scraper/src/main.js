import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';

await Actor.init();
const input = (await Actor.getInput()) ?? {};

const countries = (input.countries ?? []).map((c) => String(c).toUpperCase().trim()).filter(Boolean);
const cpvCodes = (input.cpvCodes ?? []).map((c) => String(c).trim()).filter(Boolean);
const noticeTypes = (input.noticeTypes ?? []).map((c) => String(c).trim()).filter(Boolean);
const publishedWithinDays = Math.min(Math.max(Number(input.publishedWithinDays ?? 7), 1), 365);
const maxResults = Math.min(Math.max(Number(input.maxResults ?? 100), 1), 5000);
const expertQueryInput = input.expertQuery ? String(input.expertQuery).trim() : null;

const FIELDS = [
  'publication-number', 'notice-title', 'notice-type', 'notice-subtype', 'procedure-type',
  'publication-date', 'buyer-name', 'buyer-country', 'buyer-city',
  'organisation-email-buyer', 'organisation-tel-buyer', 'organisation-internet-address-buyer',
  'place-of-performance-country-lot', 'place-of-performance-city-lot',
  'contract-nature', 'classification-cpv', 'description-lot',
  'total-value', 'total-value-cur',
  'deadline-date-lot', 'deadline-receipt-request-date-lot', 'links',
];

function orGroup(field, values) {
  if (!values.length) return null;
  return `(${values.map((v) => `${field}=${v}`).join(' OR ')})`;
}

function buildQuery() {
  if (expertQueryInput) return expertQueryInput;
  const parts = [
    orGroup('buyer-country', countries),
    orGroup('classification-cpv', cpvCodes),
    orGroup('notice-type', noticeTypes),
    `publication-date>=today(-${publishedWithinDays})`,
  ].filter(Boolean);
  return parts.join(' AND ');
}

// TED sends multilingual maps whose values are either a plain string (e.g. notice-title)
// or an array of strings (e.g. buyer-name, description-lot). Prefer English, else the first language present.
function firstValue(v) {
  if (Array.isArray(v)) return v.length ? v[0] : null;
  return v ?? null;
}
function preferredText(map) {
  if (!map || typeof map !== 'object') return [null, null];
  if (map.eng != null) return [firstValue(map.eng), 'eng'];
  if (map.mul != null) return [firstValue(map.mul), 'mul'];
  const lang = Object.keys(map)[0];
  if (!lang) return [null, null];
  return [firstValue(map[lang]), lang];
}

function dedupe(arr) {
  if (!Array.isArray(arr)) return [];
  return Array.from(new Set(arr.filter((v) => v != null)));
}

// deadline-date-lot etc. come back as one entry per lot, often the same date repeated. Take the earliest.
function earliestDate(arr) {
  const uniq = dedupe(arr);
  if (!uniq.length) return null;
  const sorted = uniq.map((d) => String(d).split('+')[0]).sort();
  return sorted[0];
}

function pickNoticeUrl(links) {
  if (!links || typeof links !== 'object') return null;
  for (const kind of ['pdf', 'xml']) {
    const byLang = links[kind];
    if (!byLang) continue;
    if (byLang.ENG) return byLang.ENG;
    if (byLang.MUL) return byLang.MUL;
    const firstKey = Object.keys(byLang)[0];
    if (firstKey) return byLang[firstKey];
  }
  return null;
}

function normalize(notice) {
  const [title, titleLanguage] = preferredText(notice['notice-title']);
  const [buyerName] = preferredText(notice['buyer-name']);
  const [description] = preferredText(notice['description-lot']);
  const buyerCountryRaw = notice['buyer-country'];
  const buyerCityRaw = notice['buyer-city'];
  return {
    publicationNumber: notice['publication-number'] ?? null,
    noticeType: notice['notice-type'] ?? null,
    procedureType: notice['procedure-type'] ?? null,
    title,
    titleLanguage,
    buyerName,
    buyerCountry: Array.isArray(buyerCountryRaw) ? buyerCountryRaw[0] ?? null : buyerCountryRaw ?? null,
    buyerCity: preferredText(buyerCityRaw)[0],
    noticeSubtype: notice['notice-subtype'] ?? null,
    buyerEmail: firstValue(notice['organisation-email-buyer']),
    buyerPhone: firstValue(notice['organisation-tel-buyer']),
    buyerUrl: firstValue(notice['organisation-internet-address-buyer']),
    placeOfPerformanceCountry: dedupe(notice['place-of-performance-country-lot']),
    placeOfPerformanceCity: dedupe(notice['place-of-performance-city-lot']),
    contractNature: dedupe(notice['contract-nature']),
    cpvCodes: dedupe(notice['classification-cpv']),
    description,
    totalValue: (typeof notice['total-value'] === 'number' && notice['total-value'] >= 0) ? notice['total-value'] : null,
    totalValueCurrency: Array.isArray(notice['total-value-cur']) ? notice['total-value-cur'][0] ?? null : notice['total-value-cur'] ?? null,
    deadlineDate: earliestDate(notice['deadline-date-lot']),
    deadlineReceiptRequestDate: earliestDate(notice['deadline-receipt-request-date-lot']),
    publicationDate: notice['publication-date'] ? String(notice['publication-date']).split('+')[0] : null,
    noticeUrl: pickNoticeUrl(notice.links),
  };
}

const query = buildQuery();
if (!query) {
  await Actor.fail('Provide at least "publishedWithinDays" (default is set) or an "expertQuery". The query ended up empty.');
}
log.info(`TED query: ${query}`);

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

const PAGE_SIZE = 250;
let page = 1;
let total = Infinity;
let keepGoing = true;
let httpError = null;

// gotScraping runs with throwHttpErrors:false, so got's own `retry` never fires on a
// non-2xx — a single TED 429 used to end the run instantly (seen live 2026-09-11: the
// default input 429'd on page 1 at 277ms and the Actor still exited SUCCEEDED with 0
// notices). Retry transient statuses here, honouring Retry-After when TED sends one.
const TRANSIENT_STATUS = new Set([408, 425, 429, 500, 502, 503, 504]);
const HTTP_RETRY_DELAYS_MS = [2000, 5000, 10000, 20000];

async function fetchPage(pageNum) {
  let resp = await fetchPageOnce(pageNum);
  for (const fallbackMs of HTTP_RETRY_DELAYS_MS) {
    if (!TRANSIENT_STATUS.has(resp.statusCode)) break;
    const retryAfterMs = Number(resp.headers?.['retry-after']) * 1000;
    const waitMs = Number.isFinite(retryAfterMs) && retryAfterMs > 0 ? Math.min(retryAfterMs, 30000) : fallbackMs;
    log.warning(`TED API returned ${resp.statusCode} on page ${pageNum} — retrying in ${waitMs}ms`);
    await new Promise((r) => setTimeout(r, waitMs));
    resp = await fetchPageOnce(pageNum);
  }
  return resp;
}

async function fetchPageOnce(pageNum) {
  return gotScraping({
    url: 'https://api.ted.europa.eu/v3/notices/search',
    method: 'POST',
    responseType: 'json',
    headers: { 'content-type': 'application/json' },
    json: { query, page: pageNum, limit: PAGE_SIZE, fields: FIELDS },
    retry: { limit: 3 },
    timeout: { request: 30000 },
  });
}

while (keepGoing && pushed < maxResults && (page - 1) * PAGE_SIZE < total) {
  let resp = await fetchPage(page);

  if (resp.statusCode !== 200) {
    log.warning(`TED API returned ${resp.statusCode} on page ${page}: ${JSON.stringify(resp.body).slice(0, 300)}`);
    httpError = resp.statusCode;
    break;
  }

  let body = resp.body;
  if (body.message) {
    await Actor.fail(`TED API error: ${body.message}`);
  }
  total = body.totalNoticeCount ?? 0;
  let notices = body.notices ?? [];

  // A page can come back with 0 notices even though totalNoticeCount says
  // there are more (seen live: transient empty page 1 with totalNoticeCount > 0).
  // A single 2s retry (cycle 102) was not always enough — cycle 103 saw the
  // exact same input fail on the platform, then succeed instantly seconds
  // later on a fresh manual call — so retry up to 3 times with backoff before
  // treating it as real end-of-results.
  const RETRY_DELAYS_MS = [2000, 5000, 10000];
  for (const delayMs of RETRY_DELAYS_MS) {
    if (notices.length || total <= (page - 1) * PAGE_SIZE) break;
    log.warning(`page ${page}: 0 notices but totalNoticeCount ${total} says there should be more — retrying in ${delayMs}ms`);
    await new Promise((r) => setTimeout(r, delayMs));
    resp = await fetchPage(page);
    if (resp.statusCode === 200) {
      body = resp.body;
      total = body.totalNoticeCount ?? total;
      notices = body.notices ?? [];
    }
  }
  if (!notices.length) break;

  for (const notice of notices) {
    keepGoing = await pushResult(normalize(notice));
    if (!keepGoing) break;
  }
  log.info(`page ${page}: fetched ${notices.length}, pushed ${pushed}/${maxResults} so far (totalNoticeCount ${total})`);
  page += 1;
}

// A run that scraped nothing because TED was erroring is a failure, not a quiet
// success — exiting 0 with an empty dataset looks to the user like "no tenders match".
if (!pushed && httpError) {
  await Actor.fail(`TED's API kept returning HTTP ${httpError} (retried ${HTTP_RETRY_DELAYS_MS.length} times), so no notices could be fetched. This is a TED-side outage or rate limit, not a problem with your input — please re-run in a few minutes.`);
}

log.info(`Done. Pushed ${pushed} notices.`);
if (!pushed) await Actor.setStatusMessage(`No notices matched this query (${query}). Widen publishedWithinDays, drop a filter, or check your CPV codes.`);
await Actor.exit();
