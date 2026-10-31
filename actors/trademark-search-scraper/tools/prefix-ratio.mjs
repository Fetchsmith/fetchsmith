// Free, local (no Actor run, no PPE events) measurement harness for cycle 2504's queued MEDIUM
// question: in `matchMode:"startsWithPrefix"`, how many upstream TMview pages does the Actor have
// to walk per DELIVERED row, and do prefix hits concentrate on the early pages the way TMview's
// relevance ordering suggested on c2504's lucky probes?
//
// It replicates exactly two things from src/main.js and nothing else: the upstream request shape
// (criteria `C` + basicSearch + fOffices) and `stripLead`/the prefix test. It never pushes, never
// charges and never touches a watch state, which is the whole point -- the question is about the
// upstream corpus, not about our delivery path, so it does not need the Actor.
//
// Usage: node tools/prefix-ratio.mjs <term> <office> <maxPages>
import { gotScraping } from 'got-scraping';
import { CookieJar } from 'tough-cookie';

const API = 'https://www.tmdn.org/tmview/api/search/results';
const SEARCH_PAGE = 'https://www.tmdn.org/tmview/';
const PAGE_SIZE = 50;

const [term, office = 'US', maxPagesRaw = '10'] = process.argv.slice(2);
if (!term) { console.error('usage: node tools/prefix-ratio.mjs <term> <office> <maxPages>'); process.exit(2); }
const maxPages = Number(maxPagesRaw);

// identical to src/main.js stripLead (NFKC + leading punct/space strip + lowercase)
const stripLead = (s) => String(s ?? '').normalize('NFKC').replace(/^[\s\p{P}\p{S}]+/u, '').toLowerCase();
const needle = stripLead(term);

const proxyUrl = process.env.TMV_PROXY || undefined;
let cookieJar = new CookieJar();
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function prime() {
  cookieJar = new CookieJar();
  await gotScraping({ url: SEARCH_PAGE, method: 'GET', cookieJar, proxyUrl, throwHttpErrors: false, timeout: { request: 20000 } });
}
await prime();

async function fetchPage(page) {
  const res = await gotScraping({
    url: API,
    method: 'POST',
    cookieJar,
    proxyUrl,
    headers: { referer: SEARCH_PAGE },
    json: { page: String(page), pageSize: String(PAGE_SIZE), criteria: 'C', basicSearch: term, fOffices: [office] },
    responseType: 'json',
    throwHttpErrors: false,
    timeout: { request: 30000 },
  });
  return { status: res.statusCode, body: res.body };
}

// The WAF in front of tmdn.org answers a too-fast page walk with an HTTP 200 HTML "Request
// Rejected" page (not a 4xx), which got-scraping surfaces as a JSON parse error. Re-prime a fresh
// cookie jar and back off rather than treating it as end-of-corpus -- otherwise the measurement
// silently reports a short walk.
async function fetchPageResilient(page) {
  for (let attempt = 0; attempt < 4; attempt += 1) {
    try {
      return await fetchPage(page);
    } catch (e) {
      if (attempt === 3) throw e;
      await sleep(3000 * (attempt + 1));
      await prime();
    }
  }
  throw new Error('unreachable');
}

let scanned = 0;
let kept = 0;
let declared = null;
const perPage = [];
for (let page = 1; page <= maxPages; page += 1) {
  let r;
  try { r = await fetchPageResilient(page); } catch (e) { console.log(`page ${page}: TRANSPORT ${e.message}`); break; }
  if (r.status !== 200) { console.log(`page ${page}: HTTP ${r.status} ${JSON.stringify(r.body).slice(0, 200)}`); break; }
  const rows = r.body?.tradeMarks ?? [];
  if (declared === null) declared = r.body?.totalResults ?? r.body?.total ?? null;
  if (!rows.length) { console.log(`page ${page}: 0 rows -- end of corpus`); break; }
  await sleep(1200);
  const keeps = rows.filter((t) => stripLead(t.tmName).startsWith(needle));
  scanned += rows.length;
  kept += keeps.length;
  perPage.push(keeps.length);
  console.log(
    `page ${String(page).padStart(3)}: rows=${String(rows.length).padStart(2)} keeps=${String(keeps.length).padStart(2)}`
    + `  cum kept=${kept}/${scanned}`
    + `  e.g. ${keeps.slice(0, 2).map((t) => JSON.stringify(t.tmName)).join(', ') || '--'}`,
  );
}

const pagesWalked = perPage.length;
console.log(JSON.stringify({
  term, office, needle, declaredContains: declared, pagesWalked, scanned, kept,
  keepRatePct: scanned ? Number(((kept / scanned) * 100).toFixed(2)) : null,
  pagesPerDeliveredRow: kept ? Number((pagesWalked / kept).toFixed(3)) : null,
  keepsPerPage: perPage,
  firstHalfKeeps: perPage.slice(0, Math.ceil(pagesWalked / 2)).reduce((a, b) => a + b, 0),
  secondHalfKeeps: perPage.slice(Math.ceil(pagesWalked / 2)).reduce((a, b) => a + b, 0),
}, null, 2));
