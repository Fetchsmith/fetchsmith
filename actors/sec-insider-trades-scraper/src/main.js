// SEC EDGAR insider trades (Forms 3/4/5) -> one flat row per reported transaction.
// HTTP-only, no headless browser. Source: SEC's own keyless endpoints
//   https://www.sec.gov/files/company_tickers.json   (ticker -> CIK)
//   https://data.sec.gov/submissions/CIK##########.json (filing index per issuer)
//   https://www.sec.gov/Archives/edgar/data/<cik>/<acc>/<doc>.xml (raw ownership XML)
// PII: the ownership XML carries the insider's HOME/BUSINESS street address. We deliberately
// never emit the address block -- names, CIKs, roles and titles are the public disclosure;
// the address is personal data and is not part of this product (same fail-closed rule as
// sam-gov-opportunities-scraper's Individual-classified exclusions).
import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';
import * as cheerio from 'cheerio';

await Actor.init();
const input = (await Actor.getInput()) ?? {};

const UA = 'FetchSmith Actor (contact: support@fetchsmith.com)';
const TIME_BUDGET_MARGIN_MS = 15000;
const MIN_REQUEST_MS = 6000;
const timeoutAt = Actor.getEnv().timeoutAt?.getTime() ?? null;
function remainingMs() { return timeoutAt == null ? Infinity : timeoutAt - Date.now() - TIME_BUDGET_MARGIN_MS; }
let timeBudgetExceeded = false;
function haveTime() {
  if (remainingMs() <= 0) { timeBudgetExceeded = true; return false; }
  return true;
}

const maxResults = Math.min(Number(input.maxResults ?? 100), 5000);
const maxFilingsPerIssuer = Math.min(Number(input.maxFilingsPerIssuer ?? 20), 200);
const includeDerivative = input.includeDerivative !== false;
// Opt-in (default off) so an existing Form 4 caller's row count -- and therefore their
// bill -- does not change: Form 4s often carry holdings rows alongside the transactions.
const includeHoldings = input.includeHoldings === true;
const sinceDate = typeof input.sinceDate === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(input.sinceDate)
  ? input.sinceDate : null;
const formTypes = Array.isArray(input.formTypes) && input.formTypes.length
  ? input.formTypes.map(String) : ['4'];
const issuers = (Array.isArray(input.issuers) && input.issuers.length ? input.issuers : ['AAPL', 'NVDA', 'JPM'])
  .map((s) => String(s).trim()).filter(Boolean);

const isPPE = Actor.getChargingManager().getPricingInfo().isPayPerEvent;
let pushed = 0;
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

// SEC asks for <=10 req/s with a declared UA; we stay well under.
let lastRequestAt = 0;
async function secGet(url, { json = false } = {}) {
  const gap = 150 - (Date.now() - lastRequestAt);
  if (gap > 0) await new Promise((r) => setTimeout(r, gap));
  for (let attempt = 1; attempt <= 3; attempt += 1) {
    lastRequestAt = Date.now();
    try {
      const res = await gotScraping({
        url,
        timeout: { request: 30000 },
        retry: { limit: 0 },
        throwHttpErrors: false,
        headers: { 'user-agent': UA, 'accept-encoding': 'gzip, deflate' },
        responseType: json ? 'json' : 'text',
      });
      if (res.statusCode === 404) return null;
      if (res.statusCode === 200) return res.body;
      log.warning(`HTTP ${res.statusCode} for ${url}`);
    } catch (err) {
      log.warning(`Request error for ${url}: ${err.message}`);
    }
    if (attempt < 3 && remainingMs() > MIN_REQUEST_MS) {
      await new Promise((r) => setTimeout(r, Math.min(attempt * 1000, Math.max(0, remainingMs() - MIN_REQUEST_MS))));
    } else break;
  }
  return null;
}

const val = ($, el, sel) => {
  const n = $(el).find(sel).first();
  if (!n.length) return null;
  const v = n.find('value').first();
  const t = (v.length ? v.text() : n.text()).trim();
  return t === '' ? null : t;
};
const num = (s) => (s == null || s === '' || Number.isNaN(Number(s)) ? null : Number(s));
const bool = (s) => (s == null ? false : s === 'true' || s === '1');

// Transaction codes that actually matter to a buyer, spelled out so a row is readable
// without the Form 4 instructions open in another tab.
const CODE_MEANING = {
  P: 'Open-market purchase', S: 'Open-market sale', A: 'Grant/award', D: 'Disposition to issuer',
  F: 'Shares withheld for taxes', M: 'Option exercise/conversion', C: 'Conversion of derivative',
  G: 'Gift', X: 'Option exercise (in the money)', J: 'Other (see footnotes)', K: 'Equity swap',
  I: 'Discretionary transaction', H: 'Expiration (long derivative)', E: 'Expiration (short derivative)',
  U: 'Tender of shares', L: 'Small acquisition', W: 'Will or laws of descent', Z: 'Voting trust',
};

async function resolveIssuers(list) {
  const map = await secGet('https://www.sec.gov/files/company_tickers.json', { json: true });
  const byTicker = new Map();
  if (map && typeof map === 'object') {
    for (const row of Object.values(map)) {
      if (row && row.ticker) byTicker.set(String(row.ticker).toUpperCase(), { cik: String(row.cik_str), name: row.title });
    }
  }
  const out = [];
  for (const raw of list) {
    if (/^\d{1,10}$/.test(raw)) { out.push({ cik: String(Number(raw)), name: null, input: raw }); continue; }
    const hit = byTicker.get(raw.toUpperCase());
    if (hit) out.push({ ...hit, input: raw });
    else log.warning(`Ticker "${raw}" not found in SEC's ticker->CIK map; skipping.`);
  }
  return out;
}

function rowsFromXml(xml, ctx) {
  const $ = cheerio.load(xml, { xmlMode: true });
  const doc = $('ownershipDocument').first();
  if (!doc.length) return [];

  const issuerName = val($, doc, 'issuer > issuerName');
  const ticker = val($, doc, 'issuer > issuerTradingSymbol');
  const periodOfReport = val($, doc, 'periodOfReport');
  const documentType = val($, doc, 'documentType');

  const owners = doc.find('reportingOwner').toArray().map((o) => ({
    insiderName: val($, o, 'rptOwnerName'),
    insiderCik: val($, o, 'rptOwnerCik'),
    isDirector: bool(val($, o, 'isDirector')),
    isOfficer: bool(val($, o, 'isOfficer')),
    isTenPercentOwner: bool(val($, o, 'isTenPercentOwner')),
    isOther: bool(val($, o, 'isOther')),
    officerTitle: val($, o, 'officerTitle'),
  }));
  const owner = owners[0] ?? {};
  // A filing can be made jointly by several reporting persons; keep the extra names
  // visible rather than silently attributing the trade to the first one only.
  const coFilers = owners.slice(1).map((o) => o.insiderName).filter(Boolean);

  const footnotes = {};
  doc.find('footnotes > footnote').each((_, f) => { footnotes[$(f).attr('id')] = $(f).text().trim(); });
  const footnoteText = (el) => {
    const ids = $(el).find('footnoteId').toArray().map((n) => $(n).attr('id'));
    const seen = [...new Set(ids)].map((id) => footnotes[id]).filter(Boolean);
    return seen.length ? seen.join(' ') : null;
  };

  // A Form 3 (and the holdings section of a Form 4/5) carries only *Holding elements —
  // no transaction is ever reported there — so without includeHoldings a Form-3-only run
  // returns exactly zero rows even though the position data is sitting in the same XML.
  const selectors = [{ sel: 'nonDerivativeTable > nonDerivativeTransaction', derivative: false, holding: false }];
  if (includeDerivative) selectors.push({ sel: 'derivativeTable > derivativeTransaction', derivative: true, holding: false });
  if (includeHoldings) {
    selectors.push({ sel: 'nonDerivativeTable > nonDerivativeHolding', derivative: false, holding: true });
    if (includeDerivative) selectors.push({ sel: 'derivativeTable > derivativeHolding', derivative: true, holding: true });
  }

  const rows = [];
  for (const { sel, derivative, holding } of selectors) {
    doc.find(sel).each((idx, tx) => {
      // Holdings have no transactionCoding/transactionAmounts block at all: leaving these
      // null (rather than 0) keeps "no trade was reported" distinct from "traded at $0".
      const code = holding ? null : val($, tx, 'transactionCoding > transactionCode');
      const shares = holding ? null : num(val($, tx, 'transactionAmounts > transactionShares'));
      const price = holding ? null : num(val($, tx, 'transactionAmounts > transactionPricePerShare'));
      const acqDisp = holding ? null : val($, tx, 'transactionAcquiredDisposedCode');
      rows.push({
        id: `${ctx.accessionNumber}-${derivative ? 'd' : 'n'}${holding ? 'h' : ''}${idx}`,
        rowType: holding ? 'holding' : 'transaction',
        accessionNumber: ctx.accessionNumber,
        formType: documentType,
        filingDate: ctx.filingDate,
        periodOfReport,
        issuerName,
        issuerCik: ctx.issuerCik,
        ticker,
        ...owner,
        coFilers,
        derivative,
        securityTitle: val($, tx, 'securityTitle'),
        transactionDate: val($, tx, 'transactionDate'),
        transactionCode: code,
        transactionCodeMeaning: code ? (CODE_MEANING[code] ?? null) : null,
        acquiredOrDisposed: acqDisp,
        shares,
        pricePerShare: price,
        // Derived because every buyer computes it anyway and gets the sign wrong:
        // negative on a disposition, positive on an acquisition.
        transactionValueUsd: shares != null && price != null
          ? Number(((acqDisp === 'D' ? -1 : 1) * shares * price).toFixed(2)) : null,
        sharesOwnedAfter: num(val($, tx, 'postTransactionAmounts > sharesOwnedFollowingTransaction')),
        directOrIndirect: val($, tx, 'ownershipNature > directOrIndirectOwnership'),
        indirectOwnershipNature: val($, tx, 'ownershipNature > natureOfOwnership'),
        exercisePrice: derivative ? num(val($, tx, 'conversionOrExercisePrice')) : null,
        expirationDate: derivative ? val($, tx, 'expirationDate') : null,
        underlyingSecurityTitle: derivative ? val($, tx, 'underlyingSecurity > underlyingSecurityTitle') : null,
        underlyingShares: derivative ? num(val($, tx, 'underlyingSecurity > underlyingSecurityShares')) : null,
        rule10b5_1Plan: bool(val($, doc, 'aff10b5One')),
        footnotes: footnoteText(tx),
        filingUrl: ctx.filingUrl,
        url: ctx.indexUrl,
      });
    });
  }
  return rows;
}

// Form 3 is a holdings snapshot: it never contains a transaction element, so asking for it
// without includeHoldings can only ever return zero rows. Say so up front rather than
// letting the buyer read "no transaction rows" once per filing and assume the feed is empty.
if (formTypes.includes('3') && !includeHoldings) {
  log.warning('formTypes includes "3" but includeHoldings is off: Form 3 filings report holdings '
    + 'only (no transactions), so they will yield 0 rows. Enable includeHoldings to get those positions.');
}

try {
  const resolved = await resolveIssuers(issuers);
  if (!resolved.length) log.warning('No issuers resolved from input; finishing with 0 results.');
  let keepGoing = true;

  for (const iss of resolved) {
    if (!keepGoing || !haveTime()) break;
    const padded = iss.cik.padStart(10, '0');
    const sub = await secGet(`https://data.sec.gov/submissions/CIK${padded}.json`, { json: true });
    if (!sub) { log.warning(`No submissions index for CIK ${padded} (${iss.input}).`); continue; }
    const recent = sub.filings?.recent ?? {};
    const forms = recent.form ?? [];

    const picked = [];
    for (let i = 0; i < forms.length && picked.length < maxFilingsPerIssuer; i += 1) {
      if (!formTypes.includes(forms[i])) continue;
      if (sinceDate && recent.filingDate[i] < sinceDate) break; // index is newest-first
      picked.push({
        accessionNumber: recent.accessionNumber[i],
        filingDate: recent.filingDate[i],
        primaryDocument: recent.primaryDocument[i],
      });
    }
    log.info(`${iss.input} (CIK ${iss.cik}): ${picked.length} ${formTypes.join('/')} filings selected.`);

    for (const f of picked) {
      if (!keepGoing || !haveTime()) break;
      const accNoDash = f.accessionNumber.replace(/-/g, '');
      const base = `https://www.sec.gov/Archives/edgar/data/${Number(iss.cik)}/${accNoDash}`;
      // primaryDocument points at the XSL-rendered HTML view ("xslF345X06/form4.xml");
      // stripping that directory prefix yields the raw machine-readable XML.
      const rawDoc = f.primaryDocument.replace(/^xsl[^/]*\//, '');
      const xml = await secGet(`${base}/${rawDoc}`);
      if (!xml) { log.warning(`Could not fetch ownership XML for ${f.accessionNumber}.`); continue; }
      const rows = rowsFromXml(xml, {
        accessionNumber: f.accessionNumber,
        filingDate: f.filingDate,
        issuerCik: iss.cik,
        filingUrl: `${base}/${rawDoc}`,
        indexUrl: `${base}/${f.accessionNumber}-index.htm`,
      });
      if (!rows.length) log.warning(`${f.accessionNumber}: no transaction rows (holdings-only filing?).`);
      for (const row of rows) {
        keepGoing = await pushResult(row);
        if (!keepGoing) break;
      }
    }
  }
  if (timeBudgetExceeded) log.warning(`Stopped early: run time budget reached after ${pushed} results.`);
} catch (err) {
  log.exception(err, 'Run failed');
  await Actor.fail(`Run failed: ${err.message}`);
}
log.info(`Done. Pushed ${pushed} results.`);
await Actor.exit();
