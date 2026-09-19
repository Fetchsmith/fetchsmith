// Trademark Search Scraper — TMview (EUIPO/TMDN) public search API, 70+ national offices.
// HTTP-only JSON API, no headless browser. Charges 'result' per pushed row.
import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';

await Actor.init();
const input = (await Actor.getInput()) ?? {};

const API = 'https://www.tmdn.org/tmview/api/search/results';
const PAGE_SIZE = 50; // verified server-side: pageSize 50 returns 50 rows

const searchTerm = String(input.searchTerm ?? '').trim();
const offices = Array.isArray(input.offices) ? input.offices.filter(Boolean) : [];
const niceClasses = (Array.isArray(input.niceClasses) ? input.niceClasses : [])
  .map((c) => String(c).trim()).filter(Boolean);
const statuses = (Array.isArray(input.statuses) ? input.statuses : []).filter(Boolean);
const maxResults = Math.min(Number(input.maxResults ?? 50), 5000);
const watchLabel = String(input.watchLabel ?? '').trim();

// TMview times out/resets on requests from Apify's default datacenter egress (verified cycle 513:
// works from this box directly, fails 3/3 on-platform without a proxy) — route through Apify Proxy.
let proxyUrl;
try {
  const proxyConfiguration = await Actor.createProxyConfiguration(input.proxyConfiguration ?? { useApifyProxy: true });
  if (proxyConfiguration) {
    proxyUrl = await proxyConfiguration.newUrl();
    log.info('Using Apify Proxy for TMview requests.');
  }
} catch (e) { log.warning(`Proxy unavailable (${e.message}) — continuing with a direct connection.`); }

const isPPE = Actor.getChargingManager().getPricingInfo().isPayPerEvent;
let pushed = 0;

async function pushResult(item) {
  if (isPPE) {
    const r = await Actor.charge({ eventName: 'result', count: 1 });
    if (r.chargedCount === 0) return false; // budget exhausted: never push unpaid items
    await Actor.pushData(item); pushed += 1;
    return !r.eventChargeLimitReached && pushed < maxResults;
  }
  await Actor.pushData(item); pushed += 1;
  return pushed < maxResults;
}

// TMview returns dates as ISO timestamps at midday UTC; buyers want a plain calendar date.
function toDate(v) {
  if (!v) return null;
  const s = String(v);
  return /^\d{4}-\d{2}-\d{2}/.test(s) ? s.slice(0, 10) : null;
}

function normalize(tm) {
  const st13 = tm.ST13 ?? null;
  return {
    id: st13,
    st13,
    url: tm.tmOfficeURL ?? null,
    trademarkName: tm.tmName ?? null,
    office: tm.tmOffice ?? null,
    status: tm.tradeMarkStatus ?? null,
    trademarkType: tm.tradeMarkType ?? null,
    applicationNumber: tm.applicationNumber ?? null,
    registrationNumber: tm.registrationNumber ?? null,
    applicationDate: toDate(tm.applicationDate),
    registrationDate: toDate(tm.registrationDate),
    applicantNames: Array.isArray(tm.applicantName) ? tm.applicantName.map(String) : [],
    niceClasses: Array.isArray(tm.niceClass) ? tm.niceClass.map(String) : [],
    viennaCodes: Array.isArray(tm.viennaCodes) ? tm.viennaCodes.map(String) : [],
    territories: Array.isArray(tm.tProtection) ? tm.tProtection.map(String) : [],
    markImageUrl: tm.markImageURI ?? null,
    detailImageUrl: tm.detailImageURI ?? null,
    ...(watchLabel ? { watchLabel } : {}),
  };
}

async function fetchPage(page) {
  const body = {
    page: String(page),
    pageSize: String(PAGE_SIZE),
    criteria: 'C', // "contains" — the API rejects unknown criteria codes with HTTP 400
    basicSearch: searchTerm,
  };
  if (offices.length) body.fOffices = offices;
  if (niceClasses.length) body.fNiceClass = niceClasses;
  if (statuses.length) body.fTMStatus = statuses;

  const res = await gotScraping({
    url: API,
    method: 'POST',
    json: body,
    responseType: 'json',
    timeout: { request: 30000 },
    retry: { limit: 2 },
    throwHttpErrors: false,
    proxyUrl,
  });
  if (res.statusCode !== 200) {
    throw new Error(`TMview returned HTTP ${res.statusCode}: ${JSON.stringify(res.body).slice(0, 300)}`);
  }
  return res.body ?? {};
}

try {
  if (!searchTerm) {
    log.warning('No searchTerm provided — nothing to search. Finishing with 0 results.');
  } else {
    const first = await fetchPage(1);
    const total = Number(first.totalResults ?? 0);
    const totalPages = Number(first.totalPages ?? 0);
    log.info(`TMview: ${total} matches for "${searchTerm}"${offices.length ? ` in ${offices.join(', ')}` : ''} (${totalPages} pages).`);

    let keepGoing = true;
    let batch = first.tradeMarks ?? [];
    let page = 1;

    while (keepGoing && batch.length) {
      for (const tm of batch) {
        keepGoing = await pushResult(normalize(tm));
        if (!keepGoing) break;
      }
      if (!keepGoing || page >= totalPages) break;
      page += 1;
      const next = await fetchPage(page);
      batch = next.tradeMarks ?? [];
    }
  }
} catch (err) {
  log.exception(err, 'Run failed');
  await Actor.fail(`Run failed: ${err.message}`);
}

log.info(`Done. Pushed ${pushed} results.${watchLabel ? ` Watch label: ${watchLabel}` : ''}`);
await Actor.exit();
