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
// EDGAR inlines only a WINDOW of filings under `filings.recent` -- the larger of ~1000 entries
// or the trailing 12 months -- and pushes everything older into paginated `filings.files` pages.
// For a prolific filer that window can be very shallow in time: JPMorgan has 26k filings in
// `recent` spanning only one year, so reading `recent` alone silently truncates any sinceDate
// reaching further back. Bounded so one issuer cannot spend the whole run on index pages.
const MAX_INDEX_PAGES = 30;
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

// Scan one index page's parallel arrays (newest-first) into `picked`.
// Returns true when selection is finished -- either the cap is full or we have passed sinceDate,
// in which case no older page can contribute and the caller stops paging.
function selectFilings(idx, picked, cap) {
  const forms = idx.form ?? [];
  for (let i = 0; i < forms.length && picked.length < cap; i += 1) {
    if (sinceDate && idx.filingDate[i] < sinceDate) return true;
    if (!formTypes.includes(forms[i])) continue;
    picked.push({
      accessionNumber: idx.accessionNumber[i],
      filingDate: idx.filingDate[i],
      primaryDocument: idx.primaryDocument[i],
    });
  }
  return picked.length >= cap;
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
  O: 'Option exercise (out of the money)', V: 'Voluntarily reported early',
};

// --- Row filters (cycle 1064) -------------------------------------------------------------
// Applied BEFORE pushResult, so a filtered-out row is never pushed and never charged: on a
// per-row PPE price the whole point of "only open-market buys over $100k" is not paying for
// the grants and tax withholdings that make up most of a Form 4 feed.
const ROLE_FLAGS = { officer: 'isOfficer', director: 'isDirector', tenPercentOwner: 'isTenPercentOwner', other: 'isOther' };
// No "unknown code" validation here on purpose: transactionCodes declares an `items.enum` of the
// 20 real codes, and the platform rejects anything else (including a lowercase "s") with a 400
// before the Actor process starts -- verified live, cycle 1064. Any in-Actor check would be
// unreachable. Dedupe only, so a doubled selection cannot skew the dropped-row count.
const transactionCodes = Array.isArray(input.transactionCodes)
  ? [...new Set(input.transactionCodes.map((c) => String(c).trim()).filter(Boolean))] : [];
const minTransactionValue = Number.isFinite(Number(input.minTransactionValue))
  ? Math.abs(Number(input.minTransactionValue)) : 0;
const insiderRoles = Array.isArray(input.insiderRoles)
  ? [...new Set(input.insiderRoles.map((r) => String(r).trim()).filter((r) => r in ROLE_FLAGS))] : [];
const filtersActive = transactionCodes.length > 0 || minTransactionValue > 0 || insiderRoles.length > 0;
let dropped = 0;

// A holding row has no transactionCode and no value at all, so a code or value filter can only
// ever exclude it -- say that once instead of returning a silently empty dataset.
if (includeHoldings && (transactionCodes.length || minTransactionValue > 0)) {
  log.warning('includeHoldings is on together with transactionCodes/minTransactionValue: holding '
    + 'rows carry neither a transaction code nor a value, so those filters exclude all of them.');
}

// Codes that SEC's Form 4/5 instructions only ever report in Table II (the derivative table):
// conversions, option exercises in/out of the money, derivative expirations and equity swaps.
// With includeDerivative off, the derivativeTransaction selector is never added, so selecting
// one of these alone yields a silently empty dataset -- the same trap the includeHoldings
// warning above covers. Verified live (cycle 1304): the enum values themselves are reachable
// with includeDerivative on (an M and an A both came back on derivative rows).
const DERIVATIVE_ONLY_CODES = ['C', 'X', 'O', 'E', 'H', 'K'];
if (!includeDerivative && transactionCodes.length) {
  const blocked = transactionCodes.filter((c) => DERIVATIVE_ONLY_CODES.includes(c));
  if (blocked.length) {
    log.warning(`includeDerivative is off but transactionCodes selects ${blocked.join('/')}, which SEC `
      + 'only reports on derivative rows: those codes cannot match anything while derivative rows are '
      + 'excluded. Turn includeDerivative on, or drop those codes.');
  }
}

function keepRow(row) {
  if (transactionCodes.length && !transactionCodes.includes(row.transactionCode)) return false;
  // Compare on the ABSOLUTE value: transactionValueUsd is signed (negative on a disposition),
  // so a raw >= test would drop every sale. A null value cannot be shown to meet the
  // threshold (holdings, or a grant with no price on the wire) and is excluded fail-closed.
  if (minTransactionValue > 0
    && !(row.transactionValueUsd != null && Math.abs(row.transactionValueUsd) >= minTransactionValue)) return false;
  // Roles come from the FIRST reporting owner (the one whose flags this row carries); a
  // joint filing's co-filers are names only (see coFilers) and are not role-matched.
  if (insiderRoles.length && !insiderRoles.some((r) => row[ROLE_FLAGS[r]] === true)) return false;
  return true;
}

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
  // Filings from before EDGAR's June 2003 electronic-filing mandate (and a handful of other
  // oddities) are plain SGML/HTML, not the <ownershipDocument> XML schema this parser expects --
  // verified live against AAPL's own 2003-03-21 Form 4 (accession 0001104659-03-004723, primaryDocument
  // "j8739_4.htm"), which is an <html> table with no XML tag anywhere. `doc.length === 0` here means
  // "not parseable as ownership XML at all", which is a different condition from a holdings-only
  // filing that parses fine but has no <*Transaction> elements -- the caller must not conflate them.
  if (!doc.length) return null;

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

    const picked = [];
    let done = selectFilings(recent, picked, maxFilingsPerIssuer);

    // Follow the older index pages when the `recent` window did not satisfy the request.
    // Pages are newest-first and carry their own date range, so a page entirely older than
    // sinceDate ends the walk without being fetched.
    let pagesRead = 0;
    if (!done) {
      for (const pg of sub.filings?.files ?? []) {
        if (!haveTime()) break;
        if (sinceDate && pg.filingTo < sinceDate) break;
        if (pagesRead >= MAX_INDEX_PAGES) {
          log.warning(`${iss.input}: stopped after ${MAX_INDEX_PAGES} older index pages (reached `
            + `${picked[picked.length - 1]?.filingDate ?? 'n/a'}). Narrow sinceDate for full coverage.`);
          break;
        }
        const older = await secGet(`https://data.sec.gov/submissions/${pg.name}`, { json: true });
        pagesRead += 1;
        if (!older) continue;
        done = selectFilings(older, picked, maxFilingsPerIssuer);
        if (done) break;
      }
    }
    log.info(`${iss.input} (CIK ${iss.cik}): ${picked.length} ${formTypes.join('/')} filings selected`
      + `${pagesRead ? ` (${pagesRead} older index page(s) read)` : ''}.`);

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
      if (rows === null) {
        log.warning(`${f.accessionNumber}: not machine-readable ownership XML -- likely a pre-June-2003 `
          + 'legacy filing (EDGAR mandated the XML ownership schema from mid-2003); skipped, not a '
          + 'holdings-only filing.');
      } else if (!rows.length) {
        log.warning(`${f.accessionNumber}: no transaction rows (holdings-only filing?).`);
      }
      for (const row of rows ?? []) {
        if (!keepRow(row)) { dropped += 1; continue; }
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
if (filtersActive) {
  // maxFilingsPerIssuer caps FILINGS fetched, not rows surviving the filters, so a narrow
  // filter can exhaust the filing budget long before maxResults -- make that visible rather
  // than letting a small row count read as "this insider barely trades".
  log.info(`Filters dropped ${dropped} row(s) before charging `
    + `(codes=${transactionCodes.join('/') || 'any'}, minValue=${minTransactionValue || 'none'}, `
    + `roles=${insiderRoles.join('/') || 'any'}).`);
  if (!pushed && dropped) {
    log.warning('Every parsed row was filtered out. The filters apply to the filings that '
      + 'maxFilingsPerIssuer already selected -- raise it (or widen sinceDate) to look further back.');
  }
}
log.info(`Done. Pushed ${pushed} results.`);
await Actor.exit();
