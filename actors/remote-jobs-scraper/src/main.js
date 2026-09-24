// remote-jobs-scraper — remote job postings from six PUBLIC, documented, no-auth job APIs
// (Remotive, Remote OK, Jobicy, Arbeitnow, Working Nomads, Himalayas), normalized into one
// schema and de-duplicated across boards. HTTP-only, no headless browser, pay-per-event on
// pushed rows only.
//
// House rules honoured here:
//  - a date bound that cannot be parsed THROWS (dropping it would widen the billable set);
//  - de-duplication happens BEFORE charging, so a buyer never pays twice for one job;
//  - every row carries the board it came from and that board's own URL (all four APIs
//    require attribution; see README "Sources and attribution").
import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';

await Actor.init();
const input = (await Actor.getInput()) ?? {};

const UA = 'FetchSmith remote-jobs-scraper (+https://fetchsmith.com)';
const ALL_SOURCES = ['remotive', 'remoteok', 'jobicy', 'arbeitnow', 'workingnomads', 'himalayas'];

const SOURCE_SITE = {
  remotive: 'https://remotive.com',
  remoteok: 'https://remoteok.com',
  jobicy: 'https://jobicy.com',
  arbeitnow: 'https://www.arbeitnow.com',
  workingnomads: 'https://www.workingnomads.com',
  himalayas: 'https://himalayas.app',
};

// ---------------------------------------------------------------- input parsing

// Strict YYYY-MM-DD. Throws on anything else: a bound we silently dropped would return
// (and bill for) jobs outside the window the buyer asked for.
function parseDateBound(raw, label, endOfDay) {
  if (raw === undefined || raw === null) return null;
  const s = String(raw).trim();
  if (s === '') return null;
  if (!/^\d{4}-\d{2}-\d{2}$/.test(s)) {
    throw new Error(
      `${label}: "${s}" is not a valid date. Use YYYY-MM-DD (e.g. 2026-09-01). ` +
      `The date is not accepted as-is because ignoring it would widen the set of jobs returned and charged.`,
    );
  }
  // The regex accepts 2026-02-30, and V8 silently ROLLS those over instead of returning
  // NaN, so the calendar check has to be an ISO round-trip.
  const d = new Date(`${s}T00:00:00.000Z`);
  if (Number.isNaN(d.getTime()) || d.toISOString().slice(0, 10) !== s) {
    throw new Error(
      `${label}: "${s}" is not a real calendar date (check the month/day). Use YYYY-MM-DD, e.g. 2026-09-01.`,
    );
  }
  if (endOfDay) d.setUTCHours(23, 59, 59, 999);
  return d;
}

// Input parsing can throw (bad source name, bad date bound). Route those through
// Actor.fail() so the platform shows the explanatory message instead of a stack trace.
async function failInput(err) {
  log.error(err.message);
  await Actor.fail(err.message);
  process.exit(1);
}

function parseInput() {
  const raw = Array.isArray(input.sources) ? input.sources : ALL_SOURCES;
  const picked = [...new Set(raw.map((s) => String(s).trim().toLowerCase()).filter(Boolean))];
  const bad = picked.filter((s) => !ALL_SOURCES.includes(s));
  if (bad.length) throw new Error(`Unknown source(s): ${bad.join(', ')}. Valid: ${ALL_SOURCES.join(', ')}.`);
  const after = parseDateBound(input.postedAfter, 'postedAfter', false);
  const before = parseDateBound(input.postedBefore, 'postedBefore', true);
  if (after && before && after > before) {
    throw new Error(
      `postedAfter (${after.toISOString().slice(0, 10)}) is later than postedBefore ` +
      `(${before.toISOString().slice(0, 10)}) — that window contains no days.`,
    );
  }
  return {
    sources: picked.length ? picked : ALL_SOURCES,
    maxResults: Math.max(1, Math.min(Number(input.maxResults ?? 100), 5000)),
    maxPagesPerSource: Math.max(1, Math.min(Number(input.maxPagesPerSource ?? 2), 20)),
    searchKeyword: (input.searchKeyword ?? '').trim(),
    titleExcludeKeyword: (input.titleExcludeKeyword ?? '').trim().toLowerCase(),
    companyKeyword: (input.companyKeyword ?? '').trim().toLowerCase(),
    locationKeyword: (input.locationKeyword ?? '').trim().toLowerCase(),
    salaryOnly: input.salaryOnly === true,
    includeDescription: input.includeDescription === true,
    dedupe: input.dedupe !== false,
    postedAfter: after,
    postedBefore: before,
  };
}

let cfg;
try {
  cfg = parseInput();
} catch (err) {
  await failInput(err);
}
const {
  sources, maxResults, maxPagesPerSource, searchKeyword, titleExcludeKeyword,
  companyKeyword, locationKeyword, salaryOnly, includeDescription, dedupe,
  postedAfter, postedBefore,
} = cfg;

// ---------------------------------------------------------------- charging

const isPPE = Actor.getChargingManager().getPricingInfo().isPayPerEvent;
let pushed = 0;

async function pushResult(item) {
  if (isPPE) {
    const r = await Actor.charge({ eventName: 'job', count: 1 });
    if (r.chargedCount === 0) return false; // budget exhausted: never push an unpaid row
    await Actor.pushData(item); pushed += 1;
    return !r.eventChargeLimitReached && pushed < maxResults;
  }
  await Actor.pushData(item); pushed += 1;
  return pushed < maxResults;
}

// ---------------------------------------------------------------- helpers

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// got only retries a fixed list of network error codes (ETIMEDOUT, ECONNRESET, ...). Remote OK's
// edge intermittently kills the HTTP/2 stream (ERR_HTTP2_ERROR) or answers a fresh connection with
// a non-HTTP preamble (HPE_INVALID_CONSTANT) — measured at ~1 fresh request in 4, cycle 616 — and
// neither code is on that list, so a single blip used to drop that whole source for the run with
// only a WARN. Retry every transport-level failure ourselves, dropping to HTTP/1.1 after the first
// attempt. 4xx (other than 429) fails fast — retrying our own bad request never helps.
async function fetchJson(url) {
  let lastErr;
  for (let attempt = 0; attempt < 3; attempt += 1) {
    try {
      const res = await gotScraping({
        url,
        responseType: 'json',
        headers: { 'User-Agent': UA, Accept: 'application/json' },
        timeout: { request: 45000 },
        retry: { limit: 2 },
        ...(attempt > 0 ? { http2: false } : {}),
      });
      // got-scraping sets throwHttpErrors:false, so a 404/500 arrives here as an ordinary body and
      // the source would report "fetched 0" — a dead feed looking exactly like an empty one
      // (measured cycle 616). Surface it instead, and only retry the statuses worth retrying.
      if (res.statusCode >= 400) {
        const err = new Error(`HTTP ${res.statusCode} from ${url}`);
        err.statusCode = res.statusCode;
        if (res.statusCode < 500 && res.statusCode !== 429) throw err;
        throw Object.assign(err, { retryable: true });
      }
      return res.body;
    } catch (err) {
      if (err.statusCode && !err.retryable) throw err;
      lastErr = err;
      if (attempt < 2) {
        log.warning(`${url}: ${err.code || err.name} (${err.message}). Retrying over HTTP/1.1.`);
        await sleep(500 * (attempt + 1));
      }
    }
  }
  throw lastErr;
}

function toIso(value) {
  if (value === undefined || value === null || value === '') return null;
  // Remotive sends a naive "2026-09-18T16:43:22" (UTC); Arbeitnow sends a unix epoch.
  if (typeof value === 'number' || /^\d{9,11}$/.test(String(value))) {
    const d = new Date(Number(value) * 1000);
    return Number.isNaN(d.getTime()) ? null : d.toISOString();
  }
  const s = String(value).trim();
  const d = new Date(/^\d{4}-\d{2}-\d{2}T[\d:.]+$/.test(s) ? `${s}Z` : s);
  return Number.isNaN(d.getTime()) ? null : d.toISOString();
}

function asArray(v) {
  if (Array.isArray(v)) return v.map((x) => String(x).trim()).filter(Boolean);
  if (typeof v === 'string' && v.trim()) return [v.trim()];
  return [];
}

function num(v) {
  const n = Number(v);
  return Number.isFinite(n) && n > 0 ? n : null;
}

const norm = (s) => String(s ?? '').toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();

// Cross-board dedup match key for company names. The same employer is routinely listed as
// "Acme Inc" on one board and "Acme" on another (verified live: "Sanctuary Computer Inc" on
// Remotive vs "Sanctuary Computer" on Remote OK, same posting, missed by a bare norm() match),
// so strip common legal-entity suffixes before comparing. Never used for the displayed
// `company` field, only for matching.
const LEGAL_SUFFIXES = /\b(inc|incorporated|llc|ltd|limited|corp|corporation|co|gmbh|plc|llp|pty|pte|srl|bv|ag|sa)\b$/;
const normCompany = (s) => norm(s).replace(LEGAL_SUFFIXES, '').trim();

// ---------------------------------------------------------------- salary normalization
// Every board publishes salary in exactly one shape and leaves the other empty: Remotive
// gives a free-text range only ("$90k - $105k"), Remote OK and Jobicy give numbers only.
// Untranslated, that means `salaryText` is structurally null on 3 of 4 sources and
// `salaryMin`/`salaryMax` are structurally null on Remotive, even when the board plainly
// published the figure. Both directions are filled below; a value the board itself sent is
// never overwritten.

const CURRENCY_SYMBOLS = { $: 'USD', '€': 'EUR', '£': 'GBP', '₹': 'INR', '¥': 'JPY' };
const SYMBOL_FOR = { USD: '$', EUR: '€', GBP: '£', INR: '₹', JPY: '¥' };

// Only periods the text states outright. We deliberately do NOT infer a period from the
// magnitude ("$90k" is almost certainly annual, but "almost certainly" is not a fact we
// are willing to sell), so salaryPeriod stays null unless the board said it.
// NB: these must not be wrapped in a leading \b — the "/hour" form starts with a
// non-word character, so a \b in front of the alternation can never match it.
const PERIOD_PATTERNS = [
  [/(\bper\s*hour\b|\ban\s*hour\b|\bhourly\b|\/\s*hours?\b|\/\s*hr\b|\bp\/h\b)/i, 'hourly'],
  [/(\bper\s*day\b|\ba\s*day\b|\bdaily\b|\/\s*days?\b)/i, 'daily'],
  [/(\bper\s*week\b|\ba\s*week\b|\bweekly\b|\/\s*weeks?\b|\/\s*wk\b)/i, 'weekly'],
  [/(\bper\s*month\b|\ba\s*month\b|\bmonthly\b|\/\s*months?\b|\/\s*mo\b)/i, 'monthly'],
  [/(\bper\s*year\b|\ba\s*year\b|\byearly\b|\bannually\b|\bannual\b|\bper\s*annum\b|\/\s*years?\b|\/\s*yr\b)/i, 'yearly'],
];

// "up to $90k" is a ceiling and "from $90k" is a floor; reading either as an exact figure
// would misreport the posting.
const CEILING_RE = /\b(up\s*to|at\s*most|maximum|max|under|below)\b/i;
const FLOOR_RE = /\b(from|starting\s*at|start(s|ing)?\s*from|at\s*least|minimum|min)\b/i;

// "105,000" is a thousands separator; "31,2" is a European decimal comma. The digit count
// after the comma is what tells them apart.
function amountFromToken(digits, kSuffix) {
  const cleaned = digits.replace(/,(\d{3})\b/g, '$1').replace(/,(\d{1,2})\b/g, '.$1').replace(/\s/g, '');
  let n = Number(cleaned);
  if (!Number.isFinite(n) || n <= 0) return null;
  if (kSuffix) n *= 1000;
  return Math.round(n);
}

function parseSalaryText(text) {
  const s = String(text ?? '').trim();
  if (!s) return null;

  let currency = null;
  for (const [sym, code] of Object.entries(CURRENCY_SYMBOLS)) {
    if (s.includes(sym)) { currency = code; break; }
  }
  // A spelled-out code wins over a bare symbol ("CAD $80k" is Canadian, not US).
  const code = s.match(/\b(USD|EUR|GBP|CAD|AUD|NZD|CHF|SEK|NOK|DKK|PLN|INR|JPY|SGD|BRL|ZAR|MXN)\b/i);
  if (code) currency = code[1].toUpperCase();

  let period = null;
  for (const [re, name] of PERIOD_PATTERNS) {
    if (re.test(s)) { period = name; break; }
  }

  const tokens = [...s.matchAll(/(\d[\d.,\s]*)\s*(k\b|k(?=\W)|k$)?/gi)]
    .map((m) => amountFromToken(m[1].trim(), Boolean(m[2])))
    .filter((n) => n !== null);
  if (!tokens.length) return null;

  // A range is the first two figures; anything beyond that (a "401k", a year) is noise we
  // do not guess at. A lone figure is an exact value unless the text marks it as a bound.
  const [a, b] = tokens;
  if (b === undefined) {
    if (CEILING_RE.test(s)) return { min: null, max: a, currency, period };
    if (FLOOR_RE.test(s)) return { min: a, max: null, currency, period };
    return { min: a, max: a, currency, period };
  }
  const min = Math.min(a, b);
  const max = Math.max(a, b);
  return { min, max, currency, period };
}

const PERIOD_WORDS = {
  hourly: 'per hour', daily: 'per day', weekly: 'per week',
  monthly: 'per month', yearly: 'per year',
};

function formatSalary({ min, max, currency, period }) {
  if (!min && !max) return null;
  const sym = currency ? (SYMBOL_FOR[currency] ?? null) : null;
  const money = (n) => {
    const digits = Number(n).toLocaleString('en-US');
    if (sym) return `${sym}${digits}`;
    return currency ? `${digits} ${currency}` : digits;
  };
  let body;
  if (min && max && min !== max) body = `${money(min)} - ${money(max)}`;
  else if (min && max) body = money(min);
  else if (min) body = `From ${money(min)}`;
  else body = `Up to ${money(max)}`;
  const suffix = period ? ` ${PERIOD_WORDS[period] ?? period}` : '';
  return `${body}${suffix}`;
}

// Fills whichever half of the salary picture the board left empty. Never overwrites a
// value the board actually sent.
function normalizeSalary(row) {
  if (!row.salaryText && (row.salaryMin || row.salaryMax)) {
    row.salaryText = formatSalary({
      min: row.salaryMin,
      max: row.salaryMax,
      currency: row.salaryCurrency,
      period: row.salaryPeriod,
    });
  } else if (row.salaryText && !row.salaryMin && !row.salaryMax) {
    const parsed = parseSalaryText(row.salaryText);
    if (parsed) {
      row.salaryMin = parsed.min;
      row.salaryMax = parsed.max;
      row.salaryCurrency = row.salaryCurrency ?? parsed.currency;
      row.salaryPeriod = row.salaryPeriod ?? parsed.period;
    }
  }
  return row;
}

// ---------------------------------------------------------------- per-source fetchers
// Each returns an array of rows already in our normalized shape.

async function fromRemotive() {
  const qs = new URLSearchParams({ limit: String(Math.min(maxResults * 3, 1000)) });
  if (searchKeyword) qs.set('search', searchKeyword);
  const body = await fetchJson(`https://remotive.com/api/remote-jobs?${qs}`);
  return (body?.jobs ?? []).map((j) => ({
    source: 'remotive',
    sourceJobId: String(j.id ?? ''),
    title: j.title ?? null,
    company: j.company_name ?? null,
    companyLogo: j.company_logo || null,
    url: j.url ?? null,
    location: j.candidate_required_location || null,
    remote: true,
    jobType: j.job_type || null,
    category: j.category || null,
    tags: asArray(j.tags),
    salaryText: j.salary || null,
    salaryMin: null,
    salaryMax: null,
    salaryCurrency: null,
    salaryPeriod: null,
    publishedAt: toIso(j.publication_date),
    descriptionHtml: includeDescription ? (j.description ?? null) : undefined,
  }));
}

async function fromRemoteOk() {
  const body = await fetchJson('https://remoteok.com/api');
  const rows = Array.isArray(body) ? body : [];
  return rows
    .filter((j) => j && j.id && j.position) // element 0 is Remote OK's legal notice, not a job
    .map((j) => ({
      source: 'remoteok',
      sourceJobId: String(j.id),
      title: j.position ?? null,
      company: j.company ?? null,
      companyLogo: j.company_logo || j.logo || null,
      url: j.url || j.apply_url || null,
      location: j.location || null,
      remote: true,
      jobType: null,
      category: null,
      tags: asArray(j.tags),
      salaryText: null,
      salaryMin: num(j.salary_min),
      salaryMax: num(j.salary_max),
      salaryCurrency: num(j.salary_min) || num(j.salary_max) ? 'USD' : null,
      // Remote OK's payload carries no period field at all (verified cycle 724: the API's
      // only salary keys are salary_min/salary_max), so there is nothing here to read a
      // period from. This said 'yearly' until cycle 724, which is precisely the
      // magnitude-based guess the salary-normalization block above refuses to make — and it
      // published a false figure: a live posting paying 30-36/hour (Tessera Labs, 1 of the
      // 18 salaried rows that day) was rendered "$30 - $36 per year". Numbers still ship;
      // only the unsourced period claim is dropped.
      salaryPeriod: null,
      publishedAt: toIso(j.date ?? j.epoch),
      descriptionHtml: includeDescription ? (j.description ?? null) : undefined,
    }));
}

async function fromJobicy() {
  const qs = new URLSearchParams({ count: '50' });
  if (searchKeyword) qs.set('tag', searchKeyword);
  const body = await fetchJson(`https://jobicy.com/api/v2/remote-jobs?${qs}`);
  return (body?.jobs ?? []).map((j) => ({
    source: 'jobicy',
    sourceJobId: String(j.id ?? ''),
    title: j.jobTitle ?? null,
    company: j.companyName ?? null,
    companyLogo: j.companyLogo || null,
    url: j.url ?? null,
    location: Array.isArray(j.jobGeo) ? j.jobGeo.join(', ') : (j.jobGeo || null),
    remote: true,
    jobType: asArray(j.jobType).join(', ') || null,
    category: asArray(j.jobIndustry).join(', ') || null,
    tags: asArray(j.jobLevel),
    salaryText: null,
    salaryMin: num(j.salaryMin),
    salaryMax: num(j.salaryMax),
    salaryCurrency: (num(j.salaryMin) || num(j.salaryMax)) ? (j.salaryCurrency || null) : null,
    salaryPeriod: (num(j.salaryMin) || num(j.salaryMax)) ? (j.salaryPeriod || null) : null,
    publishedAt: toIso(j.pubDate),
    descriptionHtml: includeDescription ? (j.jobDescription ?? null) : undefined,
  }));
}

async function fromArbeitnow() {
  const out = [];
  let url = 'https://www.arbeitnow.com/api/job-board-api';
  for (let page = 0; page < maxPagesPerSource && url; page += 1) {
    const body = await fetchJson(url);
    for (const j of body?.data ?? []) {
      // Arbeitnow is a general (mostly German) board, so keep only the remote rows —
      // this Actor's contract is remote jobs.
      if (j.remote !== true) continue;
      out.push({
        source: 'arbeitnow',
        sourceJobId: String(j.slug ?? ''),
        title: j.title ?? null,
        company: j.company_name ?? null,
        companyLogo: null,
        url: j.url ?? null,
        location: j.location || null,
        remote: true,
        jobType: asArray(j.job_types).join(', ') || null,
        category: null,
        tags: asArray(j.tags),
        salaryText: null,
        salaryMin: null,
        salaryMax: null,
        salaryCurrency: null,
        salaryPeriod: null,
        publishedAt: toIso(j.created_at),
        descriptionHtml: includeDescription ? (j.description ?? null) : undefined,
      });
    }
    url = body?.links?.next || null;
  }
  return out;
}

async function fromWorkingNomads() {
  const body = await fetchJson('https://www.workingnomads.com/api/exposed_jobs/');
  const rows = Array.isArray(body) ? body : [];
  return rows
    .filter((j) => j && j.url && j.title)
    // No stable job id field in this feed; the job's own permalink URL is the only
    // per-posting identifier the API exposes, so it doubles as sourceJobId here.
    .map((j) => ({
      source: 'workingnomads',
      sourceJobId: String(j.url ?? ''),
      title: j.title ?? null,
      company: j.company_name ?? null,
      companyLogo: null,
      url: j.url ?? null,
      location: j.location || null,
      remote: true,
      jobType: null,
      category: j.category_name || null,
      tags: String(j.tags ?? '').split(',').map((t) => t.trim()).filter(Boolean),
      salaryText: null,
      salaryMin: null,
      salaryMax: null,
      salaryCurrency: null,
      salaryPeriod: null,
      publishedAt: toIso(j.pub_date),
      descriptionHtml: includeDescription ? (j.description ?? null) : undefined,
    }));
}

async function fromHimalayas() {
  const out = [];
  let cursor = null;
  for (let page = 0; page < maxPagesPerSource; page += 1) {
    // Fixed page size (the API ignores ?limit=, verified live: always returns 20 regardless
    // of the value requested), so depth is capped purely by maxPagesPerSource like Arbeitnow.
    const qs = cursor ? `?cursor=${encodeURIComponent(cursor)}` : '';
    const body = await fetchJson(`https://himalayas.app/jobs/api${qs}`);
    const jobs = Array.isArray(body?.jobs) ? body.jobs : [];
    for (const j of jobs) {
      out.push({
        source: 'himalayas',
        // No separate id field; guid is the job's own permalink and the only stable
        // per-posting key the API exposes (same gap-filling as Working Nomads' url).
        sourceJobId: String(j.guid ?? ''),
        title: j.title ?? null,
        company: j.companyName ?? null,
        companyLogo: j.companyLogo || null,
        url: j.applicationLink || j.guid || null,
        location: Array.isArray(j.locationRestrictions) && j.locationRestrictions.length
          ? j.locationRestrictions.join(', ') : null,
        remote: true,
        jobType: j.employmentType || null,
        category: asArray(j.parentCategories).join(', ') || null,
        tags: asArray(j.categories),
        salaryText: null,
        salaryMin: num(j.minSalary),
        salaryMax: num(j.maxSalary),
        salaryCurrency: (num(j.minSalary) || num(j.maxSalary)) ? (j.currency || null) : null,
        salaryPeriod: (num(j.minSalary) || num(j.maxSalary)) ? (j.salaryPeriod || null) : null,
        publishedAt: toIso(j.pubDate),
        descriptionHtml: includeDescription ? (j.description ?? null) : undefined,
      });
    }
    // Stop on an empty page rather than a missing nextCursor — with ~102k total jobs the
    // last page was never reached live, so whether nextCursor is omitted there is unverified.
    if (jobs.length === 0 || !body.nextCursor) break;
    cursor = body.nextCursor;
  }
  return out;
}

const FETCHERS = {
  remotive: fromRemotive,
  remoteok: fromRemoteOk,
  jobicy: fromJobicy,
  arbeitnow: fromArbeitnow,
  workingnomads: fromWorkingNomads,
  himalayas: fromHimalayas,
};

// ---------------------------------------------------------------- filters

function keep(row) {
  const hay = `${row.title ?? ''} ${row.company ?? ''} ${row.category ?? ''} ${(row.tags ?? []).join(' ')}`.toLowerCase();
  if (searchKeyword && !hay.includes(searchKeyword.toLowerCase())) return false;
  if (titleExcludeKeyword && String(row.title ?? '').toLowerCase().includes(titleExcludeKeyword)) return false;
  if (companyKeyword && !String(row.company ?? '').toLowerCase().includes(companyKeyword)) return false;
  if (locationKeyword && !String(row.location ?? '').toLowerCase().includes(locationKeyword)) return false;
  if (salaryOnly && !(row.salaryText || row.salaryMin || row.salaryMax)) return false;
  if (postedAfter || postedBefore) {
    if (!row.publishedAt) return false; // no date means we cannot honour the window
    const t = new Date(row.publishedAt);
    if (postedAfter && t < postedAfter) return false;
    if (postedBefore && t > postedBefore) return false;
  }
  return true;
}

// ---------------------------------------------------------------- main

try {
  const collected = [];
  for (const src of sources) {
    try {
      const rows = (await FETCHERS[src]()).map(normalizeSalary);
      const kept = rows.filter(keep);
      log.info(`${src}: fetched ${rows.length}, ${kept.length} match the filters.`);
      collected.push(...kept);
    } catch (err) {
      // One dead board must not kill a multi-board run.
      log.warning(`${src}: fetch failed (${err.message}). Continuing with the other sources.`);
    }
  }

  // De-duplicate BEFORE charging: the same job is routinely syndicated to several boards
  // and the buyer must not be billed once per copy.
  collected.sort((a, b) => String(b.publishedAt ?? '').localeCompare(String(a.publishedAt ?? '')));
  const byKey = new Map();
  const ordered = [];
  for (const row of collected) {
    const key = `${normCompany(row.company)}|${norm(row.title)}`;
    if (dedupe && normCompany(row.company) && norm(row.title) && byKey.has(key)) {
      const first = byKey.get(key);
      if (!first.alsoOn.includes(row.source)) first.alsoOn.push(row.source);
      first.duplicateUrls.push(row.url);
      continue;
    }
    const enriched = { ...row, alsoOn: [], duplicateUrls: [] };
    byKey.set(key, enriched);
    ordered.push(enriched);
  }
  const dupes = collected.length - ordered.length;
  log.info(`${collected.length} matching rows, ${ordered.length} unique after de-duplication (${dupes} cross-board duplicates folded).`);

  for (const row of ordered) {
    const item = {
      source: row.source,
      sourceSite: SOURCE_SITE[row.source],
      sourceJobId: row.sourceJobId || null,
      title: row.title,
      company: row.company,
      companyLogo: row.companyLogo,
      url: row.url,
      location: row.location,
      remote: row.remote,
      jobType: row.jobType,
      category: row.category,
      tags: row.tags,
      salaryText: row.salaryText,
      salaryMin: row.salaryMin,
      salaryMax: row.salaryMax,
      salaryCurrency: row.salaryCurrency,
      salaryPeriod: row.salaryPeriod,
      publishedAt: row.publishedAt,
      alsoOn: row.alsoOn,
      duplicateUrls: row.duplicateUrls,
      scrapedAt: new Date().toISOString(),
    };
    if (includeDescription) item.descriptionHtml = row.descriptionHtml ?? null;
    if (!(await pushResult(item))) break;
  }
} catch (err) {
  log.exception(err, 'Run failed');
  await Actor.fail(`Run failed: ${err.message}`);
}

log.info(`Done. Pushed ${pushed} results.`);
await Actor.exit();
