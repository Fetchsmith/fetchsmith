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
import { createHash } from 'crypto';
import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';
import * as cheerio from 'cheerio';

await Actor.init();
const input = (await Actor.getInput()) ?? {};

const UA = 'FetchSmith remote-jobs-scraper (+https://fetchsmith.com)';
const ALL_SOURCES = ['remotive', 'remoteok', 'jobicy', 'arbeitnow', 'workingnomads', 'himalayas', 'wwr'];

// Arbeitnow and Himalayas paginate up to `maxPagesPerSource` (max 20) sequential requests each,
// on top of up to 6 sources and fetchJson's own 3 retry attempts per call — a slow run can
// otherwise get hard-killed by the platform mid-collection with zero rows pushed, since pushing
// only starts after every source has been walked (see the final loop below). Stopping early and
// returning whatever was already collected is strictly better than that.
const timeoutAt = Actor.getEnv().timeoutAt?.getTime() ?? null;
const TIME_BUDGET_MARGIN_MS = 45_000;
let timeBudgetExceeded = false;
function remainingMs() { return timeoutAt == null ? Infinity : timeoutAt - Date.now() - TIME_BUDGET_MARGIN_MS; }
function timeBudgetOk() {
  if (remainingMs() <= 0) { timeBudgetExceeded = true; return false; }
  return true;
}

const SOURCE_SITE = {
  remotive: 'https://remotive.com',
  remoteok: 'https://remoteok.com',
  jobicy: 'https://jobicy.com',
  arbeitnow: 'https://www.arbeitnow.com',
  workingnomads: 'https://www.workingnomads.com',
  himalayas: 'https://himalayas.app',
  wwr: 'https://weworkremotely.com',
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

// A floor the buyer typed wrong must fail loudly, not silently become "no filter" (which
// would widen, not narrow, the billable set — same reasoning as parseDateBound above).
function parseMinSalaryAnnual(raw) {
  if (raw === undefined || raw === null || String(raw).trim() === '') return null;
  const n = Number(raw);
  if (!Number.isFinite(n) || n <= 0) {
    throw new Error(`minSalaryAnnual: "${raw}" must be a positive number (an annualized salary floor, e.g. 100000).`);
  }
  return n;
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
    jobTypeKeyword: (input.jobTypeKeyword ?? '').trim().toLowerCase(),
    seniorityKeyword: (input.seniorityKeyword ?? '').trim().toLowerCase(),
    salaryOnly: input.salaryOnly === true,
    minSalaryAnnual: parseMinSalaryAnnual(input.minSalaryAnnual),
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
  companyKeyword, locationKeyword, jobTypeKeyword, seniorityKeyword, salaryOnly, minSalaryAnnual, includeDescription, dedupe,
  postedAfter, postedBefore,
} = cfg;

// ---------------------------------------------------------------- watch mode
// A stateful "only postings that are new since my last run" filter — the job-alert shape a
// plain run cannot offer (the same open roles come back every time). The baseline (identities
// already delivered) lives in a NAMED key-value store on the buyer's own account so it survives
// across runs. Same pattern as ats-jobs-scraper (h1042+), nih-reporter/federal-register/
// grants-gov/fda-recall/clinicaltrials/hacker-news.
const watchLabel = String(input.watchLabel ?? '').trim();

const webhookUrlRaw = String(input.webhookUrl ?? '').trim();
let webhookUrl = null;
if (webhookUrlRaw) {
  try {
    const parsed = new URL(webhookUrlRaw);
    if (parsed.protocol === 'http:' || parsed.protocol === 'https:') webhookUrl = parsed.toString();
    else log.warning(`webhookUrl "${webhookUrlRaw}" is not http(s); ignoring.`);
  } catch {
    log.warning(`webhookUrl "${webhookUrlRaw}" is not a valid URL; ignoring.`);
  }
}

const WATCH_STORE = 'fetchsmith-remote-jobs-watch';
const SEED_CAP = 5000;
const WATCH_KEEP = 20000; // bound the record size; oldest ids fall off first
let baselineTruncated = 0;
let baselineTruncatedTotal = 0;

function watchKeyFor(label, criteria) {
  const safe = label.toLowerCase().replace(/[^a-z0-9_.-]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 40) || 'default';
  const fp = createHash('sha1').update(JSON.stringify(criteria, Object.keys(criteria).sort())).digest('hex').slice(0, 10);
  return { key: `watch-${safe}-${fp}`, fingerprint: fp };
}

const WATCH_EVENTS = ['new', 'salaryAdded'];
const watchEventsInput = (input.watchEvents ?? []).map((e) => String(e).trim()).filter(Boolean);
const unknownWatchEvents = watchEventsInput.filter((e) => !WATCH_EVENTS.includes(e));
if (unknownWatchEvents.length) log.warning(`Ignoring unknown watchEvents value(s): ${unknownWatchEvents.join(', ')}. Valid values: ${WATCH_EVENTS.join(', ')}.`);
const watchEvents = new Set(watchEventsInput.filter((e) => WATCH_EVENTS.includes(e)));
if (!watchEvents.size) for (const e of WATCH_EVENTS) watchEvents.add(e);
let watchEventsFiltered = 0;
let watchChanged = 0;
const watchMeta = new Map(); // watchId -> hasSalary the row carried when last delivered
const META_UNKNOWN = 0;
const encodeMeta = (hasSalary) => (hasSalary === true ? 1 : hasSalary === false ? 2 : META_UNKNOWN);
const decodeMeta = (code) => (code === 1 ? true : code === 2 ? false : null);

const watchMode = watchLabel.length > 0;
let watchStore = null;
let watchKey = null;
let watchRecord = null;
let seeding = false;
let watchSkipped = 0;
const watchSeen = new Set();

if (watchMode) {
  // Fingerprint the buyer's own match criteria AND anything that changes how DEEP the crawl
  // reaches, because a baseline is only valid for the reach that produced it.
  //
  // `maxPagesPerSource` is in here despite looking like a pure cost cap (cycle 1052). It does not
  // change which postings *match*, but it absolutely changes which postings are *reached*, and a
  // baseline seeded at depth 1 therefore never recorded the postings sitting on pages 2+. Raising
  // the depth later made every one of those OLDER postings look brand new: measured live on
  // arbeitnow, seed at depth 1 recorded 23, an immediate re-run at depth 3 delivered and CHARGED
  // for 24 postings whose publishedAt all predated the baseline run (oldest by 3 days). Fresh
  // baseline (free, zero rows) is the correct answer to a reach change, exactly as it already is
  // for a filter change.
  //
  // `maxResults` stays OUT: it is a delivery cap, not a reach cap. Seeding ignores it (SEED_CAP
  // gates the baseline instead) and pushResult only baselines an id when the row actually got
  // pushed, so a maxResults cutoff defers new postings to the next run rather than swallowing
  // them. The one place it touches a request is Remotive's `limit`, whose query params are
  // measured-inert. If Remotive ever restores server-side filtering, maxResults starts affecting
  // reach and must move into this fingerprint.
  const criteria = {
    sources: [...sources].sort(), searchKeyword, titleExcludeKeyword, companyKeyword,
    locationKeyword, jobTypeKeyword, seniorityKeyword, salaryOnly, minSalaryAnnual,
    postedAfter: input.postedAfter ?? null, postedBefore: input.postedBefore ?? null,
    maxPagesPerSource,
  };
  watchStore = await Actor.openKeyValueStore(WATCH_STORE);
  const { key, fingerprint } = watchKeyFor(watchLabel, criteria);
  watchKey = key;
  const existing = await watchStore.getValue(key);
  if (existing && Array.isArray(existing.seenIds)) {
    watchRecord = existing;
    const meta = Array.isArray(existing.seenMeta) ? existing.seenMeta : [];
    existing.seenIds.forEach((id, i) => {
      watchSeen.add(String(id));
      watchMeta.set(String(id), decodeMeta(meta[i] ?? META_UNKNOWN));
    });
    log.info(
      `Watch mode "${watchLabel}" (${key}): baseline from ${existing.lastRunAt ?? 'an earlier run'} holds `
      + `${watchSeen.size} already-delivered posting(s). Only postings NOT in that baseline, or already-delivered `
      + `ones that gained a salary (events: ${[...watchEvents].join(', ')}), will be returned and charged.`,
    );
  } else {
    watchRecord = { fingerprint, firstSeededAt: new Date().toISOString(), runCount: 0 };
    seeding = true;
    log.info(
      `Watch mode "${watchLabel}" (${key}): FIRST run for this label and filter set, so this is a baseline `
      + 'run. It records which postings are already open and returns ZERO results (you are charged nothing). '
      + 'Run it again on the same label and filters — on a schedule, typically — to get only the new postings since now.',
    );
  }
}

async function saveWatchRecord(status) {
  const ids = Array.from(watchSeen).slice(-WATCH_KEEP);
  baselineTruncated = watchSeen.size - ids.length;
  baselineTruncatedTotal = (watchRecord.truncatedTotal ?? 0) + baselineTruncated;
  if (baselineTruncated > 0) {
    log.warning(
      `The baseline for watch label "${watchLabel}" exceeded the ${WATCH_KEEP}-entry record cap; the `
      + `${baselineTruncated} oldest posting id(s) were dropped (${baselineTruncatedTotal} dropped over the `
      + 'life of this label) and will be re-delivered and re-charged as "new" on a future run. Narrow the '
      + 'filters to keep the baseline under the cap.',
    );
  }
  await watchStore.setValue(watchKey, {
    ...watchRecord,
    label: watchLabel,
    lastRunAt: new Date().toISOString(),
    lastRunStatus: status,
    runCount: (watchRecord.runCount ?? 0) + 1,
    seenCount: ids.length,
    seenIds: ids,
    seenMeta: ids.map((id) => encodeMeta(watchMeta.get(id))),
    truncatedLastRun: baselineTruncated,
    truncatedTotal: baselineTruncatedTotal,
  });
}

// ---------------------------------------------------------------- charging

const isPPE = Actor.getChargingManager().getPricingInfo().isPayPerEvent;
let pushed = 0;

async function chargeAndPush(item) {
  if (isPPE) {
    const r = await Actor.charge({ eventName: 'job', count: 1 });
    if (r.chargedCount === 0) return false; // budget exhausted: never push an unpaid row
    await Actor.pushData(item); pushed += 1;
    return !r.eventChargeLimitReached && pushed < maxResults;
  }
  await Actor.pushData(item); pushed += 1;
  return pushed < maxResults;
}

async function pushResult(item, watchId) {
  if (!watchMode || watchId == null) return chargeAndPush(item);
  const idStr = String(watchId);
  const hasSalary = item.salaryMin != null || item.salaryMax != null;
  if (seeding) {
    watchSeen.add(idStr);
    watchMeta.set(idStr, hasSalary);
    return watchSeen.size < SEED_CAP;
  }
  if (watchSeen.has(idStr)) {
    // A posting commonly gains a salary after first publish (a board back-fills it, or the
    // employer edits the listing) with no id change, so a returning id is diffed against its
    // recorded salary state rather than skipped unconditionally.
    const previous = watchMeta.get(idStr) ?? null;
    const salaryAdded = previous === false && hasSalary === true;
    watchMeta.set(idStr, hasSalary);
    if (salaryAdded && watchEvents.has('salaryAdded')) {
      item.watchEvent = 'salaryAdded';
      item.previousHasSalary = false;
      watchChanged += 1;
      return chargeAndPush(item);
    }
    if (salaryAdded) watchEventsFiltered += 1;
    watchSkipped += 1;
    return true;
  }
  if (!watchEvents.has('new')) {
    watchSeen.add(idStr);
    watchMeta.set(idStr, hasSalary);
    watchEventsFiltered += 1;
    watchSkipped += 1;
    return true;
  }
  item.watchEvent = 'new';
  item.previousHasSalary = null;
  const before = pushed;
  const keepGoing = await chargeAndPush(item);
  if (pushed > before) { watchSeen.add(idStr); watchMeta.set(idStr, hasSalary); }
  return keepGoing;
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

// Same transport-retry shape as fetchJson, but for the one source (We Work Remotely) that has
// no JSON API at all — only a public RSS feed, which arrives as XML text.
async function fetchText(url) {
  let lastErr;
  for (let attempt = 0; attempt < 3; attempt += 1) {
    try {
      const res = await gotScraping({
        url,
        responseType: 'text',
        headers: { 'User-Agent': UA, Accept: 'application/rss+xml, application/xml, text/xml' },
        timeout: { request: 45000 },
        retry: { limit: 2 },
        ...(attempt > 0 ? { http2: false } : {}),
      });
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
// gives a free-text range only ("$90k - $105k"), Remote OK, Jobicy and Himalayas give
// numbers only, and Arbeitnow and Working Nomads publish no salary at all. Untranslated,
// that means `salaryText` is structurally null on 3 of the 4 sources that carry salary and
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

// A board that publishes its own period field does not have to use our vocabulary for it.
// Himalayas says "annual" where Remotive's parsed text and Jobicy's field both say "yearly"
// — the same concept under a different word, on 19 of 26 salaried rows in a 100-row sample
// (cycle 1004). Left raw it broke the column two ways: `salaryPeriod` stopped being the
// normalized enum README sells, so `salaryPeriod === 'yearly'` silently missed every annual
// row on the largest board here, and formatSalary()'s `PERIOD_WORDS[period] ?? period`
// fell through to render "$132,232 - $193,940 annual" instead of "... per year".
// Reuses PERIOD_PATTERNS so the board words and our own text parser share one vocabulary.
// An unrecognised word is passed through UNCHANGED rather than guessed at or dropped — the
// same no-inference rule as the Remote OK period fix in cycle 724.
function canonPeriod(value) {
  if (value === undefined || value === null || value === '') return null;
  const s = String(value).trim();
  if (!s) return null;
  for (const [re, name] of PERIOD_PATTERNS) {
    if (re.test(s)) return name;
  }
  return s;
}

const PERIOD_WORDS = {
  hourly: 'per hour', daily: 'per day', weekly: 'per week',
  monthly: 'per month', yearly: 'per year',
};

// For `minSalaryAnnual`: an hourly row at $85/hr is not below a $100k floor, so the floor must be
// compared against an annualized figure, not the raw number. Full-time-equivalent assumptions
// (2080 paid hours/year, 260 paid days/year), stated in the README and schema as assumptions, not
// facts — a part-time hourly/daily rate would overstate its annual equivalent under this math.
// `canonPeriod` only ever returns one of these five words or an unrecognised raw string (an
// unrecognised period, like a missing one, cannot be honestly annualized).
const PERIOD_ANNUAL_MULTIPLIER = { yearly: 1, monthly: 12, weekly: 52, daily: 260, hourly: 2080 };
function annualizeSalary(amount, period) {
  if (amount == null) return null;
  const mult = PERIOD_ANNUAL_MULTIPLIER[period];
  return mult ? amount * mult : null;
}

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
  // Remotive's public API ignores EVERY query parameter it documents, not just `limit`.
  // Re-measured live cycle 932 (2026-09-28): `limit` 1/5/50/300/1000, `search=python`,
  // `search=zzzznomatch`, `category=software-dev` and `company_name=nonexistentzzz` all
  // return the same fixed feed (16 rows, `total-job-count: 16`) — `search=zzzznomatch`
  // still returns all 16, and `search=python` still includes a German customer-service
  // posting. So these params are decorative: keyword narrowing on Remotive rows comes
  // entirely from this Actor's own passesFilters(). They are still sent because they cost
  // nothing and would start working again if Remotive restores server-side filtering;
  // nothing downstream may assume they did anything.
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
    seniorityLevel: null,
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
      seniorityLevel: null,
      salaryText: null,
      salaryMin: num(j.salary_min),
      salaryMax: num(j.salary_max),
      // Remote OK's payload carries no currency field at all either (same dump as the period
      // check below: only salary_min/salary_max) — 'USD' here until cycle 725 was the same
      // shape of invented value as the salaryPeriod bug below, just never proven wrong by a
      // sampled row because most Remote OK postings genuinely are USD. Per the fleet's
      // standing no-inference rule (LEARNINGS cycle 605: "read the ISO code the board
      // prints; if there is none, leave salaryCurrency null"), stop guessing. formatSalary()
      // renders bare digits with no $ prefix when currency is null, which is the honest
      // output for a board that never told us the unit.
      salaryCurrency: null,
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
    // Jobicy's API carries no freeform tags field at all (verified live 2026-10-02: a full
    // job object has no "tags" key), so this slot stayed populated with jobLevel as a
    // placeholder until now. jobLevel is a real, clean seniority enum ("Any", "Entry-Level,
    // Junior", "Senior", "Director") -- the only one of the six boards that publishes one --
    // so it gets its own field below instead of overloading tags.
    tags: [],
    seniorityLevel: asArray(j.jobLevel).join(', ') || null,
    salaryText: null,
    salaryMin: num(j.salaryMin),
    salaryMax: num(j.salaryMax),
    salaryCurrency: (num(j.salaryMin) || num(j.salaryMax)) ? (j.salaryCurrency || null) : null,
    salaryPeriod: (num(j.salaryMin) || num(j.salaryMax)) ? canonPeriod(j.salaryPeriod) : null,
    publishedAt: toIso(j.pubDate),
    descriptionHtml: includeDescription ? (j.jobDescription ?? null) : undefined,
  }));
}

async function fromArbeitnow() {
  const out = [];
  let url = 'https://www.arbeitnow.com/api/job-board-api';
  for (let page = 0; page < maxPagesPerSource && url; page += 1) {
    if (!timeBudgetOk()) {
      log.warning(`arbeitnow: approaching the run timeout — stopping pagination early at page ${page} of ${maxPagesPerSource}.`);
      break;
    }
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
        seniorityLevel: null,
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
      seniorityLevel: null,
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
    if (!timeBudgetOk()) {
      log.warning(`himalayas: approaching the run timeout — stopping pagination early at page ${page} of ${maxPagesPerSource}.`);
      break;
    }
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
        // Himalayas' categories are role-title slugs ("Senior-Valuation-Analyst",
        // "Software-Engineer"), not a clean seniority enum -- a seniority word sometimes
        // rides along inside the slug, but there is no separate field to read it from, so
        // this stays null rather than regex-guessing a level out of a job title.
        seniorityLevel: null,
        salaryText: null,
        salaryMin: num(j.minSalary),
        salaryMax: num(j.maxSalary),
        salaryCurrency: (num(j.minSalary) || num(j.maxSalary)) ? (j.currency || null) : null,
        salaryPeriod: (num(j.minSalary) || num(j.maxSalary)) ? canonPeriod(j.salaryPeriod) : null,
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

// We Work Remotely publishes no JSON API, only a public RSS feed of its whole open-roles list
// (~89 items live 2026-10-06, no pagination, no server-side filtering params at all — every
// filter here comes from this Actor's own passesFilters(), same situation as Remotive).
// Verified live: every one of 89 sampled titles follows "Company: Job title" with no exception
// (0 missing the ": " separator), so splitting on the FIRST ": " recovers both fields cleanly —
// a title containing ":" again past that point (e.g. a role with a subtitle) still splits
// correctly since only the first occurrence is used as the boundary.
async function fromWWR() {
  const xml = await fetchText('https://weworkremotely.com/remote-jobs.rss');
  const $ = cheerio.load(xml, { xml: true });
  const out = [];
  $('item').each((_, el) => {
    const $el = $(el);
    const rawTitle = $el.find('title').text().trim();
    const sep = rawTitle.indexOf(': ');
    const company = sep > -1 ? rawTitle.slice(0, sep).trim() : null;
    const title = sep > -1 ? rawTitle.slice(sep + 2).trim() : rawTitle;
    const url = $el.find('link').text().trim() || null;
    // No separate id field in this feed; the posting's own permalink is the only stable
    // per-posting key published, same gap-filling as Working Nomads' and Himalayas' sourceJobId.
    const sourceJobId = $el.find('guid').text().trim() || url || '';
    // region/country/state are each sometimes blank and sometimes carry real data (verified
    // live: 19/89 sampled rows had a non-empty country, 14/89 a non-empty state) — WWR does not
    // consistently fill all three for every posting, so this joins whichever ones it actually
    // sent rather than guessing at the others.
    const region = $el.find('region').text().trim();
    const country = $el.find('country').text().trim();
    const state = $el.find('state').text().trim();
    const location = [region, country, state].filter(Boolean).join(', ') || null;
    out.push({
      source: 'wwr',
      sourceJobId,
      title: title || null,
      company,
      companyLogo: $el.find('media\\:content').attr('url') || null,
      url,
      location,
      remote: true,
      jobType: $el.find('type').text().trim() || null,
      category: $el.find('category').text().trim() || null,
      tags: asArray($el.find('skills').text().trim() ? $el.find('skills').text().split(',') : []),
      seniorityLevel: null,
      // WWR's RSS feed publishes no salary field at all (verified live: no <salary>-shaped tag
      // anywhere in a 89-item feed), same gap as Arbeitnow and Working Nomads.
      salaryText: null,
      salaryMin: null,
      salaryMax: null,
      salaryCurrency: null,
      salaryPeriod: null,
      publishedAt: toIso($el.find('pubDate').text().trim()),
      descriptionHtml: includeDescription ? ($el.find('description').text().trim() || null) : undefined,
    });
  });
  return out;
}

const FETCHERS = {
  remotive: fromRemotive,
  remoteok: fromRemoteOk,
  jobicy: fromJobicy,
  arbeitnow: fromArbeitnow,
  workingnomads: fromWorkingNomads,
  himalayas: fromHimalayas,
  wwr: fromWWR,
};

// ---------------------------------------------------------------- filters

function keep(row) {
  // seniorityLevel is included here so moving Jobicy's jobLevel out of `tags` (see fromJobicy)
  // does not narrow what searchKeyword already matched before this field existed.
  const hay = `${row.title ?? ''} ${row.company ?? ''} ${row.category ?? ''} ${(row.tags ?? []).join(' ')} ${row.seniorityLevel ?? ''}`.toLowerCase();
  if (searchKeyword && !hay.includes(searchKeyword.toLowerCase())) return false;
  if (titleExcludeKeyword && String(row.title ?? '').toLowerCase().includes(titleExcludeKeyword)) return false;
  if (companyKeyword && !String(row.company ?? '').toLowerCase().includes(companyKeyword)) return false;
  if (locationKeyword && !String(row.location ?? '').toLowerCase().includes(locationKeyword)) return false;
  // jobType is null on remoteok/workingnomads rows (neither board publishes an employment-type
  // field at all — see README), so a null row never matches a non-empty jobTypeKeyword rather
  // than being silently kept or guessed at.
  if (jobTypeKeyword && !String(row.jobType ?? '').toLowerCase().includes(jobTypeKeyword)) return false;
  // seniorityLevel is only ever non-null on Jobicy rows (see fromJobicy) -- every other
  // board's row has it null and therefore never matches a non-empty filter, dropped rather
  // than guessed at, same rule as jobTypeKeyword above.
  if (seniorityKeyword && !String(row.seniorityLevel ?? '').toLowerCase().includes(seniorityKeyword)) return false;
  if (salaryOnly && !(row.salaryText || row.salaryMin || row.salaryMax)) return false;
  if (minSalaryAnnual != null) {
    // No currency conversion is performed anywhere in this Actor (see README "Salary fields"), so
    // a floor can only be honestly applied to a row stated in USD. A null currency (most Remote OK
    // rows) is "unknown", not "assume USD" — comparing an unconverted GBP/EUR number against a USD
    // floor would silently misapply it either way, so both unknown and non-USD rows are dropped.
    if (row.salaryCurrency !== 'USD') return false;
    // salaryMin is the stated floor; a ceiling-only row ("Up to $90k") has no known floor to
    // compare, so it is dropped rather than assumed to clear the bar.
    const annual = annualizeSalary(row.salaryMin, row.salaryPeriod);
    if (annual == null || annual < minSalaryAnnual) return false;
  }
  if (postedAfter || postedBefore) {
    if (!row.publishedAt) return false; // no date means we cannot honour the window
    const t = new Date(row.publishedAt);
    if (postedAfter && t < postedAfter) return false;
    if (postedBefore && t > postedBefore) return false;
  }
  return true;
}

// ---------------------------------------------------------------- main

const sourcesNotReached = [];
let runError = null;
try {
  const collected = [];
  for (const src of sources) {
    // Checked before starting each board, not just inside the paginated ones' own loops: a run
    // can also run low on budget between single-fetch sources (Remotive/Remote OK/Jobicy/Working
    // Nomads), and skipping the rest here is what lets `sourcesNotReached` name the true reason
    // instead of leaving a source silently missing with no explanation.
    if (!timeBudgetOk()) { sourcesNotReached.push(src); continue; }
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
      // A board occasionally reposts its own listing (same title+company, new URL/timestamp) --
      // that must still fold into one row (the buyer is billed once either way), but it is a
      // same-board repost, not evidence the job is on another board, so it must not land in
      // `alsoOn` (documented as "the extra boards", e.g. alsoOn:["remoteok","jobicy"]).
      if (row.source !== first.source && !first.alsoOn.includes(row.source)) first.alsoOn.push(row.source);
      first.duplicateUrls.push(row.url);
      continue;
    }
    // Watch-mode identity: the same cross-board key used for de-duplication above (so a job
    // posted to two boards is ONE watched identity, matching what a de-duplicated row already
    // looks like), falling back to a per-source id when company or title is missing (too weak
    // to identify a posting on its own — see normCompany/norm guard on the fold check above).
    // Used regardless of the "De-duplicate across boards" input: watch mode always tracks one
    // identity per real-world posting.
    const watchId = (normCompany(row.company) && norm(row.title))
      ? `job:${key}`
      : (row.sourceJobId ? `src:${row.source}:${row.sourceJobId}` : null);
    const enriched = { ...row, alsoOn: [], duplicateUrls: [], watchId };
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
      seniorityLevel: row.seniorityLevel,
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
    if (!(await pushResult(item, watchMode ? row.watchId : null))) break;
  }
} catch (err) {
  // NOT Actor.fail() here (h287; fixed the same way on fec-campaign-finance, ats-jobs,
  // trademark-search and eu-ted-tenders in cycles 676-680, caught here by bin/check-fail-ordering
  // in cycle 1061): Actor.fail() exits the process immediately, which skipped the
  // saveWatchRecord() below — so an INCREMENTAL run that had already pushed and CHARGED rows
  // before erroring never recorded them in the baseline, and the next run re-delivered and
  // re-charged for those same rows. The `runError ? 'failed-incremental' : ...` argument below was
  // already written for this shape; it was simply unreachable. Fail at the very end instead.
  log.exception(err, 'Run failed');
  runError = err;
}

// A failed SEEDING run must not leave a partial baseline: a board the run never reached (or
// died mid-collection) would look already-baselined next run and have its whole current board
// delivered and charged as "new". No record at all is the cheap outcome — the next run re-seeds
// for free.
const skipBaselineSave = watchMode && seeding && runError !== null;
if (skipBaselineSave) {
  log.warning(
    `The baseline run for "${watchLabel}" failed before it finished, so NO baseline was saved. `
    + 'Re-run on the same label and filters to seed again (a baseline run charges nothing).',
  );
}

let evictionSuffix = '';
if (watchMode && !skipBaselineSave) {
  await saveWatchRecord(runError ? 'failed-incremental' : (seeding ? 'seeded' : 'incremental'));
  evictionSuffix = baselineTruncated > 0
    ? ` WARNING: the watch baseline hit its ${WATCH_KEEP}-entry cap and ${baselineTruncated} oldest posting `
      + `id(s) were dropped (${baselineTruncatedTotal} dropped over the life of this label) — they will be `
      + 're-delivered and re-charged as "new" on a future run. Narrow the filters to keep the baseline under the cap.'
    : '';
  if (seeding) {
    log.info(
      `Baseline saved for watch label "${watchLabel}": ${watchSeen.size} posting(s) recorded as already-seen, `
      + '0 results returned, 0 charged. The next run on this label and these filters returns only postings '
      + `that appeared after now.${evictionSuffix}`,
    );
  } else {
    log.info(`Watch label "${watchLabel}": ${pushed} posting(s) since the last run (${watchSkipped} already-delivered posting(s) skipped, not charged`
      + `${watchChanged ? `; ${watchChanged} of the pushed item(s) were a salary appearing on an already-delivered posting, not a brand-new one` : ''}`
      + `${watchEventsFiltered ? `; ${watchEventsFiltered} change(s)/new posting(s) excluded by your watchEvents list` : ''}); baseline now holds ${watchSeen.size}.${evictionSuffix}`);
  }
}

if (watchMode && seeding) {
  await Actor.setStatusMessage(`Baseline run for watch label "${watchLabel}": ${watchSeen.size} currently-open posting(s) recorded, 0 charged. Run again later to get only what's new.${evictionSuffix}`);
} else if (watchMode && pushed === 0) {
  await Actor.setStatusMessage(`Nothing new for watch label "${watchLabel}" since its last run — that is the expected result most of the time; you were charged for nothing.${evictionSuffix}`);
} else if (watchMode) {
  await Actor.setStatusMessage(`Pushed ${pushed} new job posting(s) for watch label "${watchLabel}".${evictionSuffix}`);
}

// Fires after every row is already pushed and charged, so a slow or failing webhook can never
// affect the result set or the bill.
if (webhookUrl) {
  const env = Actor.getEnv();
  const payload = {
    actorRunId: env.actorRunId ?? null,
    defaultDatasetId: env.defaultDatasetId ?? null,
    finishedAt: new Date().toISOString(),
    pushed,
    watchLabel: watchMode ? watchLabel : null,
    watchSeeding: watchMode ? seeding : null,
    watchNewCount: watchMode && !seeding ? pushed : null,
    watchSkippedCount: watchMode && !seeding ? watchSkipped : null,
    watchEvents: watchMode ? [...watchEvents] : null,
    watchChangedCount: watchMode && !seeding ? watchChanged : null,
    watchEventsFilteredCount: watchMode && !seeding ? watchEventsFiltered : null,
    baselineTruncated: watchMode ? baselineTruncated : null,
    baselineTruncatedTotal: watchMode ? baselineTruncatedTotal : null,
  };
  try {
    const resp = await gotScraping({
      url: webhookUrl,
      method: 'POST',
      responseType: 'text',
      throwHttpErrors: false,
      retry: { limit: 0 },
      timeout: { request: 10000 },
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (resp.statusCode >= 400) log.warning(`webhookUrl POST returned ${resp.statusCode}; run result is unaffected.`);
    else log.info(`Posted completion summary to webhookUrl (${resp.statusCode}).`);
  } catch (err) {
    log.warning(`webhookUrl POST failed (${err.message}); run result is unaffected.`);
  }
}

// A timeout-triggered stop must not read like a clean, complete run — the boards named here
// were never even queried, which is a materially different situation from "these six boards had
// nothing matching your filters".
if (timeBudgetExceeded) {
  log.warning(`Approaching the run timeout — stopped collecting early. Board(s) not reached: ${
    sourcesNotReached.length ? sourcesNotReached.join(', ') : '(all boards were started, but pagination on one or more was cut short — see warnings above)'
  }. Narrow the input (fewer sources, or a lower "maxPagesPerSource") or raise the Actor's run timeout to see the rest.`);
}
log.info(`Done. Pushed ${pushed} results.${timeBudgetExceeded ? ' (incomplete: time-budget)' : ''}`);
// Last thing in the run, so the watch baseline above is already persisted: Actor.fail() both marks
// the run FAILED and overwrites whatever status message the success branches set.
if (runError) await Actor.fail(`Run failed: ${runError.message}`);
await Actor.exit();
