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

while (keepGoing && pushed < maxResults && (page - 1) * PAGE_SIZE < total) {
  const resp = await gotScraping({
    url: 'https://api.ted.europa.eu/v3/notices/search',
    method: 'POST',
    responseType: 'json',
    headers: { 'content-type': 'application/json' },
    json: { query, page, limit: PAGE_SIZE, fields: FIELDS },
    retry: { limit: 3 },
    timeout: { request: 30000 },
  });

  if (resp.statusCode !== 200) {
    log.warning(`TED API returned ${resp.statusCode} on page ${page}: ${JSON.stringify(resp.body).slice(0, 300)}`);
    break;
  }

  const body = resp.body;
  if (body.message) {
    await Actor.fail(`TED API error: ${body.message}`);
  }
  total = body.totalNoticeCount ?? 0;
  const notices = body.notices ?? [];
  if (!notices.length) break;

  for (const notice of notices) {
    keepGoing = await pushResult(normalize(notice));
    if (!keepGoing) break;
  }
  log.info(`page ${page}: fetched ${notices.length}, pushed ${pushed}/${maxResults} so far (totalNoticeCount ${total})`);
  page += 1;
}

log.info(`Done. Pushed ${pushed} notices.`);
await Actor.exit();
