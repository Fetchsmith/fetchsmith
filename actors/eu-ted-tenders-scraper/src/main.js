import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';
import { createHash } from 'node:crypto';

await Actor.init();
const input = (await Actor.getInput()) ?? {};

const countries = (input.countries ?? []).map((c) => String(c).toUpperCase().trim()).filter(Boolean);
const cpvCodes = (input.cpvCodes ?? []).map((c) => String(c).trim()).filter(Boolean);
const noticeTypes = (input.noticeTypes ?? []).map((c) => String(c).trim()).filter(Boolean);
const procedureType = (input.procedureType ?? []).map((c) => String(c).trim()).filter(Boolean);
const publishedWithinDays = Math.min(Math.max(Number(input.publishedWithinDays ?? 7), 1), 365);
const maxResults = Math.min(Math.max(Number(input.maxResults ?? 100), 1), 5000);
const expertQueryInput = input.expertQuery ? String(input.expertQuery).trim() : null;
const keywords = input.keywords ? String(input.keywords).trim() : null;
const outputLanguage = String(input.outputLanguage ?? 'eng').toLowerCase();
const watchLabel = String(input.watchLabel ?? '').trim();
const flatten = Boolean(input.flatten);
const minValue = input.minValue != null && input.minValue !== '' ? Number(input.minValue) : null;
const maxValue = input.maxValue != null && input.maxValue !== '' ? Number(input.maxValue) : null;
if (minValue != null && maxValue != null && minValue > maxValue) {
  throw new Error(`"minValue" (${minValue}) is greater than "maxValue" (${maxValue}).`);
}
const onlyOpenDeadlines = Boolean(input.onlyOpenDeadlines);
const minDaysUntilDeadline = input.minDaysUntilDeadline != null && input.minDaysUntilDeadline !== ''
  ? Math.max(Number(input.minDaysUntilDeadline), 0)
  : null;
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

function normalizeDate(raw, label) {
  if (raw == null || raw === '') return null;
  const digits = String(raw).trim().replace(/-/g, '');
  if (!/^\d{8}$/.test(digits)) {
    throw new Error(`"${label}" must be YYYYMMDD or YYYY-MM-DD, got "${raw}".`);
  }
  return digits;
}
const publicationDateFrom = normalizeDate(input.publicationDateFrom, 'publicationDateFrom');
const publicationDateTo = normalizeDate(input.publicationDateTo, 'publicationDateTo');
if (publicationDateFrom && publicationDateTo && publicationDateFrom > publicationDateTo) {
  throw new Error(`"publicationDateFrom" (${publicationDateFrom}) is after "publicationDateTo" (${publicationDateTo}).`);
}

const FIELDS = [
  'publication-number', 'notice-title', 'notice-type', 'notice-subtype', 'procedure-type',
  'publication-date', 'buyer-name', 'buyer-country', 'buyer-city',
  'organisation-email-buyer', 'organisation-tel-buyer', 'organisation-internet-address-buyer',
  'place-of-performance-country-lot', 'place-of-performance-city-lot',
  'contract-nature', 'classification-cpv', 'description-lot',
  'total-value', 'total-value-cur',
  'deadline-date-lot', 'deadline-receipt-tender-date-lot', 'deadline-receipt-expressions-date-lot',
  'deadline-receipt-request-date-lot', 'links',
  'procedure-identifier', 'change-reason-description',
];

function orGroup(field, values) {
  if (!values.length) return null;
  return `(${values.map((v) => `${field}=${v}`).join(' OR ')})`;
}

function dateClause() {
  // Explicit from/to (either or both) overrides the relative publishedWithinDays
  // window entirely — that matches both Store competitors' "absolute date range"
  // filters, which we lacked (only a 1-365 day relative lookback existed before).
  if (publicationDateFrom || publicationDateTo) {
    const clauses = [];
    if (publicationDateFrom) clauses.push(`publication-date>=${publicationDateFrom}`);
    if (publicationDateTo) clauses.push(`publication-date<=${publicationDateTo}`);
    return clauses.join(' AND ');
  }
  return `publication-date>=today(-${publishedWithinDays})`;
}

function buildQuery() {
  if (expertQueryInput) return expertQueryInput;
  const parts = [
    orGroup('buyer-country', countries),
    orGroup('classification-cpv', cpvCodes),
    orGroup('notice-type', noticeTypes),
    orGroup('procedure-type', procedureType),
    keywords ? `FT~"${keywords.replace(/"/g, '\\"')}"` : null,
    dateClause(),
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
  if (outputLanguage !== 'eng' && map[outputLanguage] != null) return [firstValue(map[outputLanguage]), outputLanguage];
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

// Whole days from today (UTC) to the submission deadline: 0 = closes today,
// negative = already closed, null = TED published no deadline on this notice
// (common on award/result notices, which have nothing left to bid on).
// deadlineDate is already "+offset"-stripped by earliestDate, but can still
// carry a time component ("2026-08-24T16:00:00"), so only the date part is used
// — a deadline at 16:00 local is still "today", not "-1 day".
function daysUntil(dateStr) {
  if (!dateStr) return null;
  const day = String(dateStr).slice(0, 10);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(day)) return null;
  const then = Date.parse(`${day}T00:00:00Z`);
  if (!Number.isFinite(then)) return null;
  const now = new Date();
  const today = Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate());
  return Math.round((then - today) / 86400000);
}

// TED's `links` object carries a separate sub-object per format (pdf/xml/html), each
// keyed by language. Picks one URL for a single format using the same language
// preference every field on this Actor already uses (output language, else ENG,
// else MUL, else whatever's there).
function pickLink(links, kind) {
  if (!links || typeof links !== 'object') return null;
  const byLang = links[kind];
  if (!byLang) return null;
  const preferredUpper = outputLanguage.toUpperCase();
  if (preferredUpper !== 'ENG' && byLang[preferredUpper]) return byLang[preferredUpper];
  if (byLang.ENG) return byLang.ENG;
  if (byLang.MUL) return byLang.MUL;
  const firstKey = Object.keys(byLang)[0];
  return firstKey ? byLang[firstKey] : null;
}

// Kept for backward compatibility with existing users of `noticeUrl`: same
// pdf-then-xml preference this field has always had.
function pickNoticeUrl(links) {
  return pickLink(links, 'pdf') ?? pickLink(links, 'xml');
}

// Apify's CSV/Excel export splits an array field into numbered columns
// (field/0, field/1, ...), which is awkward to read and shifts columns
// between rows with different array lengths. `flatten` joins these 4
// array fields into a single comma-separated string instead, at the cost
// of losing the ability to reference individual entries in JSON.
function maybeFlatten(arr) {
  return flatten ? arr.join(', ') : arr;
}

// TED carries the submission deadline in THREE different fields depending on the
// procedure, and `deadline-date-lot` — the only one this Actor read before — is the
// rarest: measured live 2026-09-19 on 10 fresh FRA cn-standard notices, 9 had
// `deadline-receipt-tender-date-lot` and only 1 had `deadline-date-lot`, so
// `deadlineDate` was null for almost every buyer. Prefer the tender-receipt
// deadline, then the generic one, then the expressions-of-interest deadline used by
// two-stage procedures, and say in `deadlineType` which one the row came from.
const DEADLINE_SOURCES = [
  ['deadline-receipt-tender-date-lot', 'tender'],
  ['deadline-date-lot', 'generic'],
  ['deadline-receipt-expressions-date-lot', 'expressions'],
];
function pickDeadline(notice) {
  for (const [field, type] of DEADLINE_SOURCES) {
    const date = earliestDate(notice[field]);
    if (date) return [date, type];
  }
  return [null, null];
}

function normalize(notice) {
  const [deadlineDate, deadlineType] = pickDeadline(notice);
  const [title, titleLanguage] = preferredText(notice['notice-title']);
  const [buyerName] = preferredText(notice['buyer-name']);
  const [description] = preferredText(notice['description-lot']);
  const [changeReasonDescription] = preferredText(notice['change-reason-description']);
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
    placeOfPerformanceCountry: maybeFlatten(dedupe(notice['place-of-performance-country-lot'])),
    placeOfPerformanceCity: maybeFlatten(dedupe(notice['place-of-performance-city-lot'])),
    contractNature: maybeFlatten(dedupe(notice['contract-nature'])),
    cpvCodes: maybeFlatten(dedupe(notice['classification-cpv'])),
    description,
    totalValue: (typeof notice['total-value'] === 'number' && notice['total-value'] >= 0) ? notice['total-value'] : null,
    totalValueCurrency: Array.isArray(notice['total-value-cur']) ? notice['total-value-cur'][0] ?? null : notice['total-value-cur'] ?? null,
    deadlineDate,
    deadlineType,
    daysUntilDeadline: daysUntil(deadlineDate),
    deadlineReceiptRequestDate: earliestDate(notice['deadline-receipt-request-date-lot']),
    publicationDate: notice['publication-date'] ? String(notice['publication-date']).split('+')[0] : null,
    noticeUrl: pickNoticeUrl(notice.links),
    pdfUrl: pickLink(notice.links, 'pdf'),
    htmlUrl: pickLink(notice.links, 'html'),
    xmlUrl: pickLink(notice.links, 'xml'),
    procedureIdentifier: notice['procedure-identifier'] ?? null,
    changeReasonDescription,
  };
}

const query = buildQuery();
if (!query) {
  await Actor.fail('Provide at least "publishedWithinDays" (default is set) or an "expertQuery". The query ended up empty.');
}
log.info(`TED query: ${query}`);

// ---------------------------------------------------------------------------
// Watch mode: "only what is new since my last run", per saved query. Same
// design as federal-register-scraper/grants-gov-scraper/hacker-news-scraper:
// baseline (publicationNumbers already delivered) kept in a NAMED key-value
// store so it survives across scheduled runs; the default KV store is
// per-run and would reset the baseline every time.
const WATCH_STORE = 'fetchsmith-ted-watch';
const SEED_CAP = 20000; // bound a seed walk against an unfiltered/very broad query
const WATCH_KEEP = 60000; // bound the record size; oldest ids fall off first
let baselineTruncated = 0; // notice ids dropped by WATCH_KEEP this run -- they come back as "new" and get charged again
let baselineTruncatedTotal = 0; // same, cumulative over the life of this label

// publishedWithinDays is a ROLLING window (its resolved value changes every day),
// so it is deliberately excluded from the fingerprint — same trap cycles 297/298
// found the hard way on other Actors. publicationDateFrom/publicationDateTo are
// only non-null when the buyer set them explicitly (see normalizeDate above), so
// including them is safe: an explicit absolute window is a real criteria choice.
// If expertQuery is set it replaces every other filter (see buildQuery), so the
// fingerprint follows that override exactly instead of also keying on filters
// that had no effect on the actual query sent.
const watchCriteria = expertQueryInput
  ? { expertQuery: expertQueryInput }
  : {
    countries: [...countries].sort(),
    cpvCodes: [...cpvCodes].sort(),
    noticeTypes: [...noticeTypes].sort(),
    procedureType: [...procedureType].sort(),
    keywords,
    publicationDateFrom,
    publicationDateTo,
  };

// Apify KV keys allow [a-zA-Z0-9!-_.'()] only, so the label is sanitised rather
// than trusted directly.
function watchKeyFor(label, criteria) {
  const safe = label.toLowerCase().replace(/[^a-z0-9_.-]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 40) || 'default';
  const fp = createHash('sha1').update(JSON.stringify(criteria, Object.keys(criteria).sort())).digest('hex').slice(0, 10);
  return { key: `watch-${safe}-${fp}`, fingerprint: fp };
}

const watchMode = watchLabel.length > 0;
let watchStore = null;
let watchKey = null;
let watchRecord = null;
let seeding = false;
const watchSeen = new Set(); // publicationNumbers already delivered under this label+fingerprint

async function saveWatchRecord(status) {
  const ids = Array.from(watchSeen).slice(-WATCH_KEEP);
  baselineTruncated = watchSeen.size - ids.length;
  baselineTruncatedTotal = (watchRecord.truncatedTotal ?? 0) + baselineTruncated;
  if (baselineTruncated > 0) {
    log.warning(
      `The baseline for watch label "${watchLabel}" exceeded the ${WATCH_KEEP}-entry record cap; the `
      + `${baselineTruncated} oldest notice id(s) were dropped (${baselineTruncatedTotal} dropped over the `
      + `life of this label) and will be re-delivered and re-charged as "new" on a future run. Narrow the `
      + 'query (a country, a CPV code, a shorter publication-date window) to keep the baseline under the cap.',
    );
  }
  await watchStore.setValue(watchKey, {
    ...watchRecord,
    label: watchLabel,
    criteria: watchCriteria,
    lastRunAt: new Date().toISOString(),
    lastRunStatus: status,
    runCount: (watchRecord.runCount ?? 0) + 1,
    seenCount: ids.length,
    seenIds: ids,
    truncatedLastRun: baselineTruncated,
    truncatedTotal: baselineTruncatedTotal,
  });
}

if (watchMode) {
  watchStore = await Actor.openKeyValueStore(WATCH_STORE);
  const { key, fingerprint } = watchKeyFor(watchLabel, watchCriteria);
  watchKey = key;
  const existing = await watchStore.getValue(key);
  if (existing && Array.isArray(existing.seenIds)) {
    watchRecord = existing;
    for (const id of existing.seenIds) watchSeen.add(String(id));
    log.info(
      `Watch mode "${watchLabel}" (${key}): baseline from ${existing.lastRunAt ?? 'an earlier run'} holds `
      + `${watchSeen.size} already-delivered notice(s). Only notices NOT in that baseline are returned and charged.`,
    );
  } else {
    watchRecord = { fingerprint, firstSeededAt: new Date().toISOString(), runCount: 0 };
    seeding = true;
    log.info(
      `Watch mode "${watchLabel}" (${key}): FIRST run for this label and filter set, so this is a baseline run. `
      + 'It records which notices already match and returns ZERO results (you are charged nothing). Run it '
      + 'again on the same label and filters — on a schedule, typically — to get only what is new since now.',
    );
  }
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

const PAGE_SIZE = 250;
// TED is paged by PAGE NUMBER over a live index and the search request carries no
// `sort`, so nothing guarantees a notice appears on exactly one page: a publication
// landing mid-walk shifts every later row, and the same publication-number can come
// back twice. Every repeat used to be its own Actor.charge() — the buyer paid twice
// for one notice (the shape found live on sam-gov at cycle 649, ~10% repeats there).
// Measured on TED 2026-09-22: 2000 rows over 8 pages of a 4,486-match query, 0
// repeats — so this is a guard against a rate-dependent upstream behaviour, not a
// fix for one observed today. watchSeen only covers watch mode; this covers all modes.
const seenRowIds = new Set();
let duplicateRowsDropped = 0;
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

async function fetchPage(pageNum, fieldsOverride) {
  let resp = await fetchPageOnce(pageNum, fieldsOverride);
  for (const fallbackMs of HTTP_RETRY_DELAYS_MS) {
    if (!TRANSIENT_STATUS.has(resp.statusCode)) break;
    const retryAfterMs = Number(resp.headers?.['retry-after']) * 1000;
    const waitMs = Number.isFinite(retryAfterMs) && retryAfterMs > 0 ? Math.min(retryAfterMs, 30000) : fallbackMs;
    log.warning(`TED API returned ${resp.statusCode} on page ${pageNum} — retrying in ${waitMs}ms`);
    await new Promise((r) => setTimeout(r, waitMs));
    resp = await fetchPageOnce(pageNum, fieldsOverride);
  }
  return resp;
}

async function fetchPageOnce(pageNum, fieldsOverride) {
  return gotScraping({
    url: 'https://api.ted.europa.eu/v3/notices/search',
    method: 'POST',
    responseType: 'json',
    headers: { 'content-type': 'application/json' },
    json: { query, page: pageNum, limit: PAGE_SIZE, fields: fieldsOverride ?? FIELDS },
    retry: { limit: 3 },
    timeout: { request: 30000 },
  });
}

// Seeding only needs the notice id, not all 21 fields — same page walk, a
// fraction of the bytes — and it never normalizes, pushes or charges. Walks
// the WHOLE match set (bounded only by SEED_CAP), not one page of it: a
// baseline that stopped early would report every notice past the stopping
// point as "new" on the first incremental run (the cycle 297/298 trap).
function passesValueFilter(item) {
  if (minValue == null && maxValue == null) return true;
  if (item.totalValue == null) return false;
  if (minValue != null && item.totalValue < minValue) return false;
  if (maxValue != null && item.totalValue > maxValue) return false;
  return true;
}

// Deadline filtering is post-fetch for the same reason the value filter is: TED's
// expert-query grammar has no reliable deadline-date operator (deadline-date-lot is
// a per-lot array, so a server-side comparison would match a notice on ANY of its
// lots), and a notice can carry no deadline at all. A notice dropped here is never
// normalized into the dataset and never charged.
function passesDeadlineFilter(item) {
  if (!onlyOpenDeadlines && minDaysUntilDeadline == null) return true;
  if (item.daysUntilDeadline == null) return false; // no deadline published = can't prove it's still open
  if (onlyOpenDeadlines && item.daysUntilDeadline < 0) return false;
  if (minDaysUntilDeadline != null && item.daysUntilDeadline < minDaysUntilDeadline) return false;
  return true;
}

let skippedSeen = 0;
let filteredOutValue = 0;
let filteredOutDeadline = 0;
async function seedBaseline() {
  const seedFields = ['publication-number'];
  let seedPage = 1;
  let seedTotal = Infinity;
  let pagesSeeded = 0;
  while (watchSeen.size < SEED_CAP && (seedPage - 1) * PAGE_SIZE < seedTotal) {
    const resp = await fetchPage(seedPage, seedFields);
    if (resp.statusCode !== 200) {
      log.warning(`Baseline walk: TED API returned ${resp.statusCode} on page ${seedPage} — stopping baseline walk early.`);
      break;
    }
    const body = resp.body;
    seedTotal = body.totalNoticeCount ?? 0;
    const notices = body.notices ?? [];
    if (!notices.length) break;
    pagesSeeded += 1;
    for (const notice of notices) {
      const id = notice['publication-number'];
      if (id) watchSeen.add(String(id));
    }
    seedPage += 1;
  }
  log.info(`Baseline walk: ${watchSeen.size} notice id(s) over ${pagesSeeded} id-only page(s) (totalNoticeCount ${seedTotal}).`);
}

if (seeding) await seedBaseline();

while (!seeding && keepGoing && pushed < maxResults && (page - 1) * PAGE_SIZE < total) {
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

  let beforePush = pushed;
  for (const notice of notices) {
    const id = notice['publication-number'];
    // Same notice served twice by TED's own paging within THIS run: dropped before
    // normalize() and before any charge. Must come before the watch check so it is
    // counted as an upstream repeat rather than as an already-delivered notice.
    if (id && seenRowIds.has(String(id))) {
      duplicateRowsDropped += 1;
      continue;
    }
    // Marked as soon as the row is CONSIDERED, not after a successful push: this set
    // is run-scoped and never persisted, so its only job is "TED already handed me
    // this row". Marking it after the charge would let a repeat of a value-filtered
    // notice inflate filteredOutValue, and a repeat arriving after the charge limit
    // is reached would be re-processed for no reason. watchSeen keeps its own
    // charge-gated rule below because that one IS persisted across runs.
    if (id) seenRowIds.add(String(id));
    // Already delivered under this watch label: dropped before normalize() and
    // before any charge, so a notice is never paid for twice.
    if (watchMode && id && watchSeen.has(String(id))) {
      skippedSeen += 1;
      continue;
    }
    const normalized = normalize(notice);
    if (!passesValueFilter(normalized)) {
      filteredOutValue += 1;
      continue;
    }
    if (!passesDeadlineFilter(normalized)) {
      filteredOutDeadline += 1;
      continue;
    }
    keepGoing = await pushResult(normalized);
    // Recorded as delivered only after the charge actually succeeded — anything
    // dropped by maxResults or a charge limit stays "new" for the next run.
    if (watchMode && id && pushed > beforePush) watchSeen.add(String(id));
    beforePush = pushed;
    if (!keepGoing) break;
  }
  log.info(`page ${page}: fetched ${notices.length}, pushed ${pushed}/${maxResults} so far (totalNoticeCount ${total})`);
  page += 1;
}

// WATCH_KEEP record-cap eviction (h285): empty unless something was actually dropped, so it
// never taints the common case where the baseline comfortably fits under the cap. Computed
// AFTER saveWatchRecord() below, which is what actually sets baselineTruncated.
let evictionSuffix = '';

if (watchMode) {
  await saveWatchRecord(seeding ? 'seeded' : 'incremental');
  evictionSuffix = baselineTruncated > 0
    ? ` WARNING: the watch baseline hit its ${WATCH_KEEP}-entry cap and ${baselineTruncated} oldest notice `
      + `id(s) were dropped (${baselineTruncatedTotal} dropped over the life of this label) — they will be `
      + 're-delivered and re-charged as "new" on a future run. Narrow the query to keep the baseline under the cap.'
    : '';
  if (seeding) {
    log.info(
      `Baseline saved for watch label "${watchLabel}": ${watchSeen.size} notice(s) recorded as already-seen, `
      + '0 results returned, 0 charged. The next run on this label and these filters returns only new notices.'
      + (watchSeen.size >= SEED_CAP
        ? ` NOTE: the baseline stopped at the ${SEED_CAP}-notice cap. Narrow the query (a country, a CPV code, `
        + 'a shorter publication-date window) so the whole result set fits, or the first incremental run will '
        + 'report notices past the cap as new.'
        : '') + evictionSuffix,
    );
  } else {
    log.info(
      `Watch label "${watchLabel}": ${pushed} new notice(s) since the last run `
      + `(${skippedSeen} already-delivered notice(s) skipped, uncharged); baseline now holds ${watchSeen.size}.`
      + evictionSuffix,
    );
  }
}

// A run that scraped nothing because TED was erroring is a failure, not a quiet
// success — exiting 0 with an empty dataset looks to the user like "no tenders match".
if (!pushed && httpError) {
  await Actor.fail(`TED's API kept returning HTTP ${httpError} (retried ${HTTP_RETRY_DELAYS_MS.length} times), so no notices could be fetched. This is a TED-side outage or rate limit, not a problem with your input — please re-run in a few minutes.`);
}

log.info(`Done. Pushed ${pushed} notices.`);
if (duplicateRowsDropped > 0) {
  log.info(
    `${duplicateRowsDropped} notice(s) were served more than once by TED's own paging and were dropped `
    + 'before being pushed or charged — you paid for each notice exactly once. This happens when new '
    + 'notices are published while the walk is in progress, shifting rows onto a later page.',
  );
}
if (filteredOutValue > 0) {
  log.info(`${filteredOutValue} matching notice(s) were dropped by minValue/maxValue (no value data, or value outside the range).`);
}
if (filteredOutDeadline > 0) {
  log.info(
    `${filteredOutDeadline} matching notice(s) were dropped by onlyOpenDeadlines/minDaysUntilDeadline `
    + '(deadline already passed, too soon, or TED published no deadline on the notice — award and result '
    + 'notices usually have none). None of them were charged.',
  );
}
if (pushed === 0 && watchMode && !seeding) {
  log.warning(
    `Nothing new for watch label "${watchLabel}" since its last run — all ${skippedSeen} matching notice(s) `
    + 'had already been delivered. That is the expected result most of the time; you were charged for nothing.',
  );
} else if (!pushed && !seeding && (filteredOutValue > 0 || filteredOutDeadline > 0) && !skippedSeen) {
  // Name only the filter(s) that actually dropped something — claiming a cause the
  // run did not observe is the defect cycles 483/484 fixed elsewhere in the fleet.
  const dropped = [
    filteredOutValue > 0 ? `${filteredOutValue} by minValue/maxValue` : null,
    filteredOutDeadline > 0 ? `${filteredOutDeadline} by onlyOpenDeadlines/minDaysUntilDeadline` : null,
  ].filter(Boolean).join(' and ');
  await Actor.setStatusMessage(`No notices matched: ${filteredOutValue + filteredOutDeadline} notice(s) matched your TED query but were dropped after fetching (${dropped}). Widen or remove that filter.`);
} else if (!pushed && !seeding) {
  await Actor.setStatusMessage(`No notices matched this query (${query}). Widen publishedWithinDays, drop a filter, or check your CPV codes.`);
}

// Fires after every row is already pushed and charged, so a slow or failing webhook can never
// affect the result set or the bill — best-effort only, one attempt, short timeout, failures are
// a warning not a thrown error.
if (webhookUrl) {
  const env = Actor.getEnv();
  const payload = {
    actorRunId: env.actorRunId ?? null,
    defaultDatasetId: env.defaultDatasetId ?? null,
    finishedAt: new Date().toISOString(),
    pushed,
    pagesScanned: page - 1,
    duplicateRowsDropped,
    totalNoticeCount: Number.isFinite(total) ? total : null,
    watchLabel: watchMode ? watchLabel : null,
    watchNewCount: watchMode && !seeding ? pushed : null,
    watchSeeding: watchMode ? seeding : null,
    // >0 means the baseline lost ids to the WATCH_KEEP cap and a future run will re-deliver and
    // re-charge for rows already paid for once.
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

await Actor.exit();
