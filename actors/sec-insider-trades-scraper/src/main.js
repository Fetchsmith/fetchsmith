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
// Strict YYYY-MM-DD only. `sinceDate` is an `editor: textfield` with no `pattern` in the input
// schema, so the platform cannot reject a malformed date for us (unlike transactionCodes, which
// has an items.enum and 400s before the process starts). A dropped lower bound is the one input
// error that looks like a SUCCESS: the run returns MORE rows than asked for -- unbounded history
// up to maxFilingsPerIssuer -- and bills for them, so warn loudly instead of failing silently.
const sinceDateRaw = typeof input.sinceDate === 'string' ? input.sinceDate.trim() : '';
const sinceDate = /^\d{4}-\d{2}-\d{2}$/.test(sinceDateRaw) ? sinceDateRaw : null;
if (sinceDateRaw && !sinceDate) {
  log.warning(`sinceDate ${JSON.stringify(input.sinceDate)} is not strict YYYY-MM-DD (zero-padded, `
    + 'dash-separated) and has been IGNORED -- this run has no lower date bound and will return '
    + `every matching filing back to maxFilingsPerIssuer=${maxFilingsPerIssuer} per issuer. `
    + 'Re-run with e.g. "2026-01-05" (not "2026-1-5", "2026/01/05" or "01-05-2026") to bound it.');
}
const formTypes = Array.isArray(input.formTypes) && input.formTypes.length
  ? input.formTypes.map(String) : ['4'];
const issuers = (Array.isArray(input.issuers) && input.issuers.length ? input.issuers : ['AAPL', 'NVDA', 'JPM'])
  .map((s) => String(s).trim()).filter(Boolean);


const isPPE = Actor.getChargingManager().getPricingInfo().isPayPerEvent;
let pushed = 0;
// The charge cap is the one truncation cause that leaves no counter behind: `keepGoing` is
// declared inside the try block and is out of scope by the time the status-message branches
// run, so record it here (cycle 2340, for the partial-success message at the end of the file).
let chargeCapReached = false;
async function pushResult(item) {
  if (isPPE) {
    const r = await Actor.charge({ eventName: 'result', count: 1 });
    if (r.chargedCount === 0) { chargeCapReached = true; return false; }
    await Actor.pushData(item); pushed += 1;
    if (r.eventChargeLimitReached) chargeCapReached = true;
    return !r.eventChargeLimitReached && pushed < maxResults;
  }
  await Actor.pushData(item); pushed += 1;
  return pushed < maxResults;
}

// EDGAR identifies an amendment only by its own form string ("4/A") plus a
// <dateOfOriginalSubmission> DATE -- it never names the superseded accession number. The
// submissions index we have already downloaded carries (form, filingDate, accessionNumber) for
// every filing, so an amendment can be mapped back to its original with no extra request: same
// issuer, same base form, filingDate == dateOfOriginalSubmission. That is unique for most
// issuers but NOT for a large one that filed several Form 4s that day (several officers, one
// board event), so we publish the whole candidate set and only fill supersedesAccessionNumber
// when exactly one candidate exists.
const OWNERSHIP_FORMS = new Set(['3', '4', '5', '3/A', '4/A', '5/A']);
function baseForm(form) { return String(form ?? '').replace(/\/A$/, ''); }
function isAmendmentForm(form) { return /\/A$/.test(String(form ?? '')); }

// Index EVERY ownership filing on a page, independent of formTypes and of maxFilingsPerIssuer:
// the original behind an amendment is older than the amendment (so further down this
// newest-first page) and is usually a form the caller did not select, which means the capped
// selection in selectFilings() would miss it. Walking the arrays again is free -- the JSON is
// already in hand. Keyed on the EXACT form string so that a 4/A amending a 4 is never offered
// another 4/A filed the same day as its "original".
function indexOwnershipFilings(idx, map) {
  const forms = idx.form ?? [];
  for (let i = 0; i < forms.length; i += 1) {
    if (!OWNERSHIP_FORMS.has(forms[i])) continue;
    const key = `${forms[i]}|${idx.filingDate[i]}`;
    (map[key] ??= []).push(idx.accessionNumber[i]);
  }
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
// Set when every selected transactionCode is structurally unreachable with includeDerivative
// off -- the zero-row remedy below must not blame maxFilingsPerIssuer/sinceDate in that case,
// since no amount of widening either one can ever produce a match (verified live, cycle 1637).
let derivativeCodesBlocked = false;
// Set when SOME but not all selected codes are dead (cycle 2423): that run still pushes rows
// from the live codes, so it never reaches the zero-row branch above and this would otherwise
// only ever surface in the log -- a buyer reading a non-empty, correctly-filtered dataset has no
// reason to suspect one of their codes silently contributed nothing on every run, forever.
let mixedBlockedCodes = [];
if (!includeDerivative && transactionCodes.length) {
  const blocked = transactionCodes.filter((c) => DERIVATIVE_ONLY_CODES.includes(c));
  if (blocked.length) {
    derivativeCodesBlocked = blocked.length === transactionCodes.length;
    if (!derivativeCodesBlocked) mixedBlockedCodes = blocked;
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
  // Matched against the UNION of every reporting owner on the filing: the first owner's
  // flags are on the row itself, and each co-filer carries its own flags in row.coFilers
  // (cycle 1927 — previously only the first owner was checked, which silently dropped a
  // joint filing whose role-holding owner was not listed first; rare but real, see README
  // "Narrowing the feed" and LEARNINGS 1924/1927 for the two-day measurement).
  if (insiderRoles.length) {
    const onFirstOwner = insiderRoles.some((r) => row[ROLE_FLAGS[r]] === true);
    const onCoFiler = (row.coFilers ?? []).some((cf) => insiderRoles.some((r) => cf[ROLE_FLAGS[r]] === true));
    if (!onFirstOwner && !onCoFiler) return false;
  }
  return true;
}

// Zero-row bookkeeping (cycle 1756): the statusMessage chain at the bottom may only name a
// cause this particular run actually observed, so each cause needs its own observed-count.
const unresolvedTickers = [];
let missingSubmissionIndex = 0;
let filingsSelected = 0;
let legacyFilings = 0;
let holdingsOnlyFilings = 0;
let unfetchableFilings = 0;

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
    else {
      unresolvedTickers.push(raw);
      log.warning(`Ticker "${raw}" not found in SEC's ticker->CIK map; skipping.`);
    }
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
  // A filing can be made jointly by several reporting persons; keep each co-filer's own
  // role flags (not just their name) so a buyer can see who actually held the role being
  // filtered on, and keepRow below can match insiderRoles against every owner, not just
  // the first.
  const coFilers = owners.slice(1).filter((o) => o.insiderName);

  // --- amendment linkage (see indexOwnershipFilings above) ---
  const isAmendment = isAmendmentForm(documentType);
  // EDGAR's own field, present on every amendment we checked; it is the ORIGINAL's filing date,
  // not its period or accession. Verified live on TSLA 0000899243-22-021041 (period 2022-05-02,
  // original filed 2022-05-04) and AAPL 0000320193-22-000078 (period 2022-08-17, original filed
  // 2022-08-19) -- note the original's FILING date is after the period in both, so this date
  // must never be compared against periodOfReport.
  const amendsOriginalFilingDate = isAmendment ? val($, doc, 'dateOfOriginalSubmission') : null;
  // issuer + reporting owner + period + base form identifies the same reported event across an
  // original and its amendment; both worked examples above share period and reporting owner with
  // the filing they correct.
  const eventKey = `${ctx.issuerCik}|${owner.insiderCik ?? ''}|${periodOfReport ?? ''}|${baseForm(documentType)}`;
  let supersedesCandidateAccessions = [];
  if (isAmendment && amendsOriginalFilingDate) {
    supersedesCandidateAccessions = (ctx.ownershipIndex?.[`${baseForm(documentType)}|${amendsOriginalFilingDate}`] ?? [])
      .filter((a) => a !== ctx.accessionNumber);
    ctx.amendmentsByEvent?.set(eventKey, {
      accessionNumber: ctx.accessionNumber,
      candidates: supersedesCandidateAccessions,
    });
  }
  const supersedesAccessionNumber = supersedesCandidateAccessions.length === 1
    ? supersedesCandidateAccessions[0] : null;
  // Reverse link. EDGAR's index is newest-first, so an amendment is always processed BEFORE the
  // filing it corrects: if that original turns up later in this run, mark its rows as superseded
  // instead of dropping them -- a buyer auditing history needs to see both the wrong number and
  // the correction, and silently dropping either is worse than today's blanket exclusion. The
  // eventKey hit (issuer+owner+period+form) disambiguates most of the cases where the date-based
  // candidate set had several members -- e.g. of the three Form 4s Tesla filed on 2022-05-04,
  // one is Baglino's and is correctly excluded from Denholm's amendment.
  // KNOWN LIMIT, verified live, do not "fix" by narrowing on filingDate (it is already equal):
  // the same insider can file two Form 4s on one day for one period -- Denholm filed BOTH
  // 0000899243-22-016670 and -016671 (period 2022-05-02) -- and EDGAR publishes no superseded-
  // accession pointer anywhere, so this flag then marks both originals. It therefore means "a
  // correction touching this issuer/owner/period exists", not "this exact row was restated".
  // That is still strictly better than excluding amendments outright, which is today's behaviour.
  const pendingAmendment = !isAmendment ? ctx.amendmentsByEvent?.get(eventKey) : null;
  const amendedByAccessionNumber = pendingAmendment
    && (!pendingAmendment.candidates.length || pendingAmendment.candidates.includes(ctx.accessionNumber))
    ? pendingAmendment.accessionNumber : null;

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
        isAmendment,
        amendsOriginalFilingDate,
        supersedesAccessionNumber,
        supersedesCandidateAccessions,
        amendedByAccessionNumber,
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
// `form3Mixed` (cycle 2423) is true only when formTypes also includes a non-"3" form: a
// formTypes:["3"]-only request is already forced through the zero-row branch below (nothing
// else could ever push a row), so only the MIXED case needs its own disclosure here -- that's
// the one where the other form(s) push real rows and a buyer has no reason to open the log to
// learn that Form 3 alone silently contributed none of them, on every run, forever.
const form3Requested = formTypes.some((f) => baseForm(f) === '3');
const form3Mixed = form3Requested && !includeHoldings && !formTypes.every((f) => baseForm(f) === '3');
if (form3Requested && !includeHoldings) {
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
    if (!sub) {
      missingSubmissionIndex += 1;
      log.warning(`No submissions index for CIK ${padded} (${iss.input}).`);
      continue;
    }
    const recent = sub.filings?.recent ?? {};

    // Per-issuer, so both maps are freed between issuers; the eventKey already carries the CIK.
    const ownershipIndex = {};
    const amendmentsByEvent = new Map();
    indexOwnershipFilings(recent, ownershipIndex);

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
        indexOwnershipFilings(older, ownershipIndex);
        done = selectFilings(older, picked, maxFilingsPerIssuer);
        if (done) break;
      }
    }
    filingsSelected += picked.length;
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
      if (!xml) {
        unfetchableFilings += 1;
        log.warning(`Could not fetch ownership XML for ${f.accessionNumber}.`);
        continue;
      }
      const rows = rowsFromXml(xml, {
        accessionNumber: f.accessionNumber,
        filingDate: f.filingDate,
        issuerCik: iss.cik,
        filingUrl: `${base}/${rawDoc}`,
        indexUrl: `${base}/${f.accessionNumber}-index.htm`,
        ownershipIndex,
        amendmentsByEvent,
      });
      if (rows === null) {
        legacyFilings += 1;
        log.warning(`${f.accessionNumber}: not machine-readable ownership XML -- likely a pre-June-2003 `
          + 'legacy filing (EDGAR mandated the XML ownership schema from mid-2003); skipped, not a '
          + 'holdings-only filing.');
      } else if (!rows.length) {
        holdingsOnlyFilings += 1;
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
  if (!pushed && dropped && !derivativeCodesBlocked) {
    log.warning('Every parsed row was filtered out. The filters apply to the filings that '
      + 'maxFilingsPerIssuer already selected -- raise it (or widen sinceDate) to look further back.');
  }
}

const STATUS_MESSAGE_MAX = 500;
// Apify silently truncates `statusMessage` at 500 chars (found cycle 1760 on other Actors in this
// fleet, see LEARNINGS). The new cycle-1766 accumulating zeroRowMessage below can join up to 4
// independent causes in one run (e.g. a derivativeCodesBlocked list plus an unresolved-tickers
// list, both caller-supplied and unbounded), so the joined message needs the same word-boundary
// backstop other Actors in the fleet already carry. The log keeps the full, unclamped text.
const clampStatusMessage = (msg) => {
  if (msg.length <= STATUS_MESSAGE_MAX) return msg;
  const cut = msg.slice(0, STATUS_MESSAGE_MAX - 4);
  const lastSpace = cut.lastIndexOf(' ');
  return `${(lastSpace > 0 ? cut.slice(0, lastSpace) : cut).trimEnd()} ...`;
};

// --- Zero-row explanation (cycle 1756) ----------------------------------------------------
// Until now a complete run that delivered 0 rows set no statusMessage at all, so the Console
// and the API both showed a bare "Succeeded" against an empty dataset and every cause above
// lived only in the run log. Name the cause THIS run observed, most specific first -- claiming
// an unobserved cause is the defect cycles 483/484 fixed elsewhere in the fleet. Only causes
// reachable on a run that gets this far are listed: the catch block exits via `Actor.fail()`,
// so a thrown error never arrives here (same structure as eu-ted-tenders-scraper, cycle 1755).
if (!pushed) {
  // Two fragments, not one shared phrase: the sentences below put the word "filing(s)" in
  // different places, and a single `form 4 for AAPL` blob reads as "2 form 4 for AAPL filing(s)"
  // in half of them. Keep the noun with its own sentence.
  const forms = `form ${formTypes.join('/')}`;
  const who = issuers.join(', ');
  let zeroRowMessage;
  // These four are checked independently, not as an else-if chain: each is a deterministic
  // "this input can never match" cause unrelated to the others (derivativeCodesBlocked turns on
  // transactionCodes/includeDerivative, the formTypes one on formTypes/includeHoldings, the
  // issuers pair on issuers/unresolvedTickers), so a run can trigger more than one at once (e.g.
  // formTypes: ["3"] with includeHoldings off AND an unresolved ticker) -- an else-if chain here
  // would silently report only the first and hide the rest, the same defect class fixed on
  // google-play-reviews/steam-reviews/ats-jobs/trademark-search (cycles 1559/1591/1592). Only
  // the last two are mutually exclusive by construction (unresolvedTickers.length === issuers.length
  // requires issuers.length > 0, so it cannot also be empty) and stay a nested if/else for that reason.
  const causes = [];
  if (derivativeCodesBlocked) {
    // Structurally impossible, so it outranks the time budget below: no amount of extra time or
    // wider dates can match a derivative-only code while derivative rows are excluded.
    causes.push(`every transactionCode you selected (${transactionCodes.join('/')}) is one SEC reports only `
      + 'on derivative rows, but includeDerivative is off, so nothing can ever match. Turn includeDerivative '
      + 'on, or drop those codes.');
  }
  if (formTypes.every((f) => baseForm(f) === '3') && !includeHoldings) {
    causes.push('formTypes is Form 3 only, which reports holdings and never transactions, while '
      + 'includeHoldings is off. Enable includeHoldings to get those positions, or add form 4/5.');
  }
  if (!issuers.length) {
    causes.push('the issuers list was empty after trimming blanks. Pass at least one ticker '
      + "(e.g. \"AAPL\") or numeric CIK.");
  } else if (unresolvedTickers.length && unresolvedTickers.length === issuers.length) {
    causes.push(`none of the issuers you asked for resolved to a CIK (${unresolvedTickers.join(', ')}). `
      + "Use the ticker exactly as SEC lists it in company_tickers.json, or pass the issuer's numeric CIK instead.");
  }
  if (causes.length) {
    zeroRowMessage = `0 rows: ${causes.join(' Also, ')}`;
  } else if (timeBudgetExceeded) {
    // Not a "no match" answer -- the walk never finished, so say that instead of advising a widen.
    zeroRowMessage = `0 rows: the run hit its time budget before any row was delivered (${filingsSelected} filing(s) `
      + 'selected). Raise the run timeout, or narrow the request (fewer issuers, lower maxFilingsPerIssuer).';
  } else if (missingSubmissionIndex && missingSubmissionIndex === issuers.length - unresolvedTickers.length) {
    zeroRowMessage = `0 rows: SEC returned no submissions index for any of the ${missingSubmissionIndex} issuer(s) `
      + 'resolved. That is usually a transient EDGAR error -- please re-run in a few minutes.';
  } else if (!filingsSelected) {
    zeroRowMessage = `0 rows: no ${forms} filings for ${who} exist in the window searched`
      + (sinceDate ? ` (sinceDate ${sinceDate} or later)` : '')
      + '. Widen sinceDate (or drop it), check the issuer really files that form, or raise maxFilingsPerIssuer.';
  } else if (dropped && filtersActive) {
    const active = [
      transactionCodes.length ? `transactionCodes=${transactionCodes.join('/')}` : null,
      minTransactionValue > 0 ? `minTransactionValue=${minTransactionValue}` : null,
      insiderRoles.length ? `insiderRoles=${insiderRoles.join('/')}` : null,
    ].filter(Boolean).join(', ');
    zeroRowMessage = `0 rows: all ${dropped} row(s) parsed from ${filingsSelected} ${forms} filing(s) for ${who} were dropped by `
      + `your filters (${active}). Those filters apply only to the filings maxFilingsPerIssuer already selected, so `
      + 'raise it (or widen sinceDate) to look further back'
      + (includeHoldings && (transactionCodes.length || minTransactionValue > 0)
        ? '. Note holding rows carry neither a transaction code nor a value, so those two filters exclude all of them'
        : '')
      + '.';
  } else if (legacyFilings || holdingsOnlyFilings || unfetchableFilings) {
    const why = [
      holdingsOnlyFilings ? `${holdingsOnlyFilings} carried holdings only (no transaction rows)` : null,
      legacyFilings ? `${legacyFilings} are pre-June-2003 legacy filings with no machine-readable XML` : null,
      unfetchableFilings ? `${unfetchableFilings} could not be fetched from EDGAR` : null,
    ].filter(Boolean).join('; ');
    zeroRowMessage = `0 rows: all ${filingsSelected} ${forms} filing(s) selected for ${who} yielded no transaction rows -- ${why}.`
      + (holdingsOnlyFilings && !includeHoldings ? ' Enable includeHoldings to return those positions.' : '');
  } else {
    zeroRowMessage = `0 rows: the ${filingsSelected} ${forms} filing(s) searched for ${who} reported no transactions. `
      + 'Widen sinceDate, raise maxFilingsPerIssuer, or add form 5 / enable includeHoldings.';
  }
  log.warning(zeroRowMessage);
  await Actor.setStatusMessage(clampStatusMessage(zeroRowMessage));
} else {
  // --- Partial-success explanation (cycle 2340) ---------------------------------------------
  // Until now ONLY the zero-row branch above ever set a statusMessage, so a buyer who asked for
  // 3 issuers and silently got rows for 2 (bad ticker, transient EDGAR miss, charge cap, time
  // budget) read a bare "Succeeded" against a short dataset and had to open the run log to find
  // out why -- or, worse, read the short count as the real answer. Same construction as the
  // zero-row branch: accumulate every cause THIS run actually observed as INDEPENDENT ifs, never
  // an else-if chain (that is the cascade-hides-independent-causes defect already fixed once in
  // this very file, see the comment at the top of the !pushed branch -- a run can easily hit an
  // unresolved ticker AND the time budget AND a legacy filing at once). Stay SILENT when nothing
  // applies, so a clean full-success run sets no message and the message keeps meaning something
  // (fleet convention, cf. google-play-reviews-scraper's pushed>0 branch, cycle 2339).
  // Every counter read below is module-scope and accumulates across the whole run, so each is as
  // valid here as in the zero-row branch -- re-checked per variable this cycle, not inherited.
  // Deliberately NOT reported: `dropped`/`filtersActive`. On a run that delivered rows, filters
  // removing the rest is the feature working exactly as asked, not a partial failure; it is
  // already logged at line ~512 and would fire on almost every filtered run, which is precisely
  // how a status message stops being read. No internal `;` in any cause (the cycle-1592 trap).
  const causes = [];
  if (unresolvedTickers.length && unresolvedTickers.length < issuers.length) {
    causes.push(`${unresolvedTickers.length} of the ${issuers.length} issuer(s) you asked for did not resolve to a `
      + `CIK (${unresolvedTickers.join(', ')}) and contributed no rows. Use the ticker exactly as SEC lists it in `
      + "company_tickers.json, or pass that issuer's numeric CIK instead.");
  }
  if (missingSubmissionIndex) {
    causes.push(`SEC returned no submissions index for ${missingSubmissionIndex} resolved issuer(s), which therefore `
      + 'contributed no rows. That is usually a transient EDGAR error -- re-run in a few minutes to pick them up.');
  }
  if (chargeCapReached) {
    causes.push(`the run stopped at its pay-per-event charge limit after ${pushed} row(s), so these results are `
      + 'truncated. Raise the charge limit for the run to get the rest.');
  }
  if (pushed >= maxResults) {
    causes.push(`the run reached maxResults (${maxResults}), so these results are truncated. Raise maxResults for more.`);
  }
  if (timeBudgetExceeded) {
    causes.push(`the run hit its time budget after ${pushed} row(s), so later issuers or filings may be missing. Raise `
      + 'the run timeout, or narrow the request (fewer issuers, lower maxFilingsPerIssuer).');
  }
  if (unfetchableFilings) {
    causes.push(`${unfetchableFilings} selected filing(s) could not be fetched from EDGAR and are missing from these `
      + 'results. Re-run to retry just those.');
  }
  if (legacyFilings) {
    causes.push(`${legacyFilings} selected filing(s) are pre-June-2003 legacy filings with no machine-readable XML, so `
      + 'they yielded no rows.');
  }
  if (holdingsOnlyFilings && !includeHoldings) {
    causes.push(`${holdingsOnlyFilings} selected filing(s) carried holdings only (no transactions) and yielded no rows. `
      + 'Enable includeHoldings to return those positions.');
  }
  // These two (cycle 2423) are a different class from the deliberately-excluded dropped/
  // filtersActive case above: they are not "filters removed some rows this run", they are
  // "this specific code/form can never contribute a row under the current settings, on any
  // run" -- the same structural-deadness the zero-row branch already treats specially via
  // derivativeCodesBlocked/the formTypes==="3" check, just surfaced here for the mixed case
  // where enough OTHER codes/forms still pushed rows to avoid ever reaching that branch.
  if (mixedBlockedCodes.length) {
    causes.push(`transactionCode(s) ${mixedBlockedCodes.join('/')} you asked for can never match: SEC reports them `
      + 'only on derivative rows, and includeDerivative is off. Turn includeDerivative on, or drop those codes.');
  }
  if (form3Mixed) {
    causes.push('form "3" in your formTypes can never match: it reports holdings only (no transactions), and '
      + 'includeHoldings is off. Enable includeHoldings to include those positions.');
  }
  if (causes.length) {
    const partialMessage = `${pushed} row(s) delivered, but: ${causes.join(' Also, ')}`;
    log.warning(partialMessage);
    await Actor.setStatusMessage(clampStatusMessage(partialMessage));
  }
}

log.info(`Done. Pushed ${pushed} results.`);
await Actor.exit();
