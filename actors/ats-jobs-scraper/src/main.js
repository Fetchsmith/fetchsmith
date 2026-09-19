// ATS Jobs Scraper: pulls live job postings from Greenhouse, Ashby, Lever, Recruitee, Workable,
// SmartRecruiters and Workday company boards and normalizes them into one cross-ATS schema. No
// headless browser — every source is a documented, no-auth, no-login JSON endpoint.
import { createHash } from 'crypto';
import { Actor, log } from 'apify';
import * as cheerio from 'cheerio';
import { gotScraping } from 'got-scraping';

await Actor.init();
const input = (await Actor.getInput()) ?? {};

const SUPPORTED_ATS = ['greenhouse', 'ashby', 'lever', 'recruitee', 'workable', 'smartrecruiters', 'workday'];
// Workday's slug is "<host>/<site>", not a bare company name, so it can't be guessed from a slug
// alone and is excluded from auto-detection. Order is a fixed priority for the rare case where the
// same slug string happens to exist as a real, populated board on more than one platform.
const AUTO_DETECT_ATS = ['greenhouse', 'ashby', 'lever', 'recruitee', 'workable', 'smartrecruiters'];
const DEFAULT_COMPANIES = [
  { ats: 'greenhouse', slug: 'airbnb' },
  { ats: 'ashby', slug: 'ramp' },
  { ats: 'lever', slug: 'leverdemo' },
  { ats: 'recruitee', slug: 'vandebron' },
  { ats: 'workable', slug: 'getresponse' },
  { ats: 'smartrecruiters', slug: 'ElasticBandCompany' },
  { ats: 'workday', slug: 'okgov.wd1.myworkdayjobs.com/okgovjobs' },
];
const seenCompanies = new Set();
const companies = (Array.isArray(input.companies) && input.companies.length ? input.companies : DEFAULT_COMPANIES)
  // Omitted/blank `ats` means "auto" — the buyer doesn't have to know which of the 7 platforms a
  // company uses, only its slug. Workday is excluded from auto-detection (see AUTO_DETECT_ATS).
  .map((c) => ({ ats: String(c.ats || 'auto').toLowerCase().trim(), slug: String(c.slug || '').trim() }))
  .filter((c) => c.slug && (c.ats === 'auto' || SUPPORTED_ATS.includes(c.ats)))
  // dedup exact (ats, slug) repeats — slug case is left as-is (some ATS slugs are case-sensitive
  // in their API URL), so this only catches literal duplicates, not near-duplicates.
  .filter((c) => {
    // Separator is a literal ':' — `ats` always comes from the SUPPORTED_ATS whitelist (lowercase
    // letters only), so the text before the first ':' is unambiguously the ats and no two distinct
    // (ats, slug) pairs can collide. Do NOT use a raw NUL byte here: it is legal in a JS string and
    // the dedup works, but it makes grep/ugrep classify this whole file as binary and silently skip
    // it in every fleet-wide source audit (found cycle 336).
    const key = `${c.ats}:${c.slug}`;
    if (seenCompanies.has(key)) return false;
    seenCompanies.add(key);
    return true;
  });
if (!companies.length) await Actor.fail(`Provide at least one company as {"ats": "auto|${SUPPORTED_ATS.join('|')}", "slug": "<company-slug>"} — omit "ats" or set it to "auto" to auto-detect the platform.`);

const titleKeyword = (input.titleKeyword ?? '').toLowerCase().trim();
const titleExcludeKeyword = (input.titleExcludeKeyword ?? '').toLowerCase().trim();
const locationKeyword = (input.locationKeyword ?? '').toLowerCase().trim();
const locationExcludeKeyword = (input.locationExcludeKeyword ?? '').toLowerCase().trim();
const employmentTypeKeyword = (input.employmentTypeKeyword ?? '').toLowerCase().trim();
const departmentKeyword = (input.departmentKeyword ?? '').toLowerCase().trim();
const descriptionKeyword = (input.descriptionKeyword ?? '').toLowerCase().trim();
const descriptionExcludeKeyword = (input.descriptionExcludeKeyword ?? '').toLowerCase().trim();
const hasSalary = !!input.hasSalary;
// Range-overlap on the salaryMin/salaryMax already emitted on every job (same shape as
// shopify-products-scraper's minPrice/maxPrice): a job posting $80k-$120k matches both
// minSalary:100000 and maxSalary:90000. Deliberately NOT normalized across currency or pay
// interval (salaryCurrency/salaryInterval vary — year/month/week/day/hour, see normalizeInterval
// below) — same "compare what's actually posted, no FX" caveat as shopify's price filters.
// A job with neither bound (no salary posted at all) never matches either filter.
const minSalary = input.minSalary != null && input.minSalary !== '' ? Number(input.minSalary) : null;
const maxSalary = input.maxSalary != null && input.maxSalary !== '' ? Number(input.maxSalary) : null;
const remoteOnly = !!input.remoteOnly;
const postedAfter = input.postedAfter ? new Date(input.postedAfter) : null;
const postedBefore = input.postedBefore ? new Date(input.postedBefore) : null;
const includeDescriptions = input.includeDescriptions !== false;
// A description filter needs the description text even when the buyer does not want it in the
// output, so the fetchers key off this and the description fields are stripped at push time
// instead. Free for the five ATSes that carry the description in the list payload; for
// SmartRecruiters/Workday it means the same per-job detail call includeDescriptions already makes.
const needDescriptions = includeDescriptions || !!descriptionKeyword || !!descriptionExcludeKeyword;
// Workday's per-job detail call is the only source of employmentType, department and publishedAt
// (its list payload has none of them), so a filter on any of those needs the detail call even when
// nobody asked for descriptions — without it the main-loop filter would match against nulls and
// return zero rows for every Workday board. SmartRecruiters' detail call only adds the description
// and the referral-tagged apply URL, so `needDescriptions` is the right gate there.
const workdayNeedsDetail = needDescriptions
  || !!employmentTypeKeyword || !!departmentKeyword || !!postedAfter || !!postedBefore;
const maxJobsPerCompany = Math.min(Number(input.maxJobsPerCompany ?? 500), 5000);
const maxResults = Math.min(Number(input.maxResults ?? 2000), 100000);
const watchLabel = String(input.watchLabel ?? '').trim();

// Convenience completion ping (same shape as grants-gov-scraper, cycle 421). A bad value is
// warned and ignored rather than thrown — this is a notification nicety, not core function.
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

// Watch mode: a stateful "only postings that are new since my last run" filter — the job-alert
// shape. A plain run returns the same open roles every time; a watched run returns only what
// appeared on those boards since the previous run under the same label and filters. The baseline
// (per-posting ids already delivered) lives in a NAMED key-value store on the buyer's own account
// so it survives across runs — the default KV store is per-run and would reset every time.
// Same pattern as nih-reporter/federal-register/grants-gov/fda-recall/clinicaltrials/hacker-news.
const WATCH_STORE = 'fetchsmith-ats-watch';
const SEED_CAP = 5000; // bound the cost of a baseline run against a very broad company list
const WATCH_KEEP = 20000; // bound the record size; oldest ids fall off first

// A posting id is only unique within one board, so the baseline key is (ats, company, jobId).
// Workday's list payload can omit the requisition id, so fall back to the job URL, which is
// always built deterministically from the board host + externalPath.
function watchIdFor(job) {
  const id = job.jobId ?? job.jobUrl;
  return id ? `${job.atsSource}:${job.company}:${id}` : null;
}

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
let watchSkipped = 0;
const watchSeen = new Set(); // ats:company:jobId already delivered under this label+fingerprint

if (watchMode) {
  // Fingerprint the buyer's own filter inputs, never a resolved/derived value: none of these
  // has a computed default (postedAfter is an explicit ISO string or absent), so the rolling-
  // default trap that bit federal-register in cycle 297 doesn't apply here. maxJobsPerCompany /
  // maxResults are deliberately excluded — they are cost caps, not match criteria.
  const criteria = {
    companies: companies.map((c) => `${c.ats}:${c.slug}`).sort(),
    titleKeyword, titleExcludeKeyword, locationKeyword, locationExcludeKeyword,
    employmentTypeKeyword, hasSalary, remoteOnly, includeDescriptions,
    postedAfter: input.postedAfter ?? null,
  };
  // The filters added in cycle 408 join the fingerprint ONLY when actually set, so every baseline
  // saved before them keeps its existing key instead of silently resetting to a fresh seed run
  // (same rule as steam-reviews-scraper's includeOffTopic). A run that does set one of them is a
  // different match set and correctly gets its own baseline.
  if (departmentKeyword) criteria.departmentKeyword = departmentKeyword;
  if (descriptionKeyword) criteria.descriptionKeyword = descriptionKeyword;
  if (descriptionExcludeKeyword) criteria.descriptionExcludeKeyword = descriptionExcludeKeyword;
  if (input.postedBefore) criteria.postedBefore = input.postedBefore;
  if (minSalary != null) criteria.minSalary = minSalary;
  if (maxSalary != null) criteria.maxSalary = maxSalary;
  watchStore = await Actor.openKeyValueStore(WATCH_STORE);
  const { key, fingerprint } = watchKeyFor(watchLabel, criteria);
  watchKey = key;
  const existing = await watchStore.getValue(key);
  if (existing && Array.isArray(existing.seenIds)) {
    watchRecord = existing;
    for (const id of existing.seenIds) watchSeen.add(String(id));
    log.info(
      `Watch mode "${watchLabel}" (${key}): baseline from ${existing.lastRunAt ?? 'an earlier run'} holds `
      + `${watchSeen.size} already-delivered posting(s). Only postings NOT in that baseline will be returned and charged.`,
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

// Watch mode splits the one per-company cap into two, because they stop meaning the same thing:
//  - the SCAN cap bounds how many matching postings a run looks at. A seeding run must record the
//    WHOLE current match set, not just the buyer's usual page of it, or every posting it missed
//    comes back as "new" (and billable) next run (cycles 297/298). An incremental run needs the
//    same reach: most of what it scans is already-delivered, so a scan cap of, say, 5 would let a
//    board with 40 open roles surface a new one only if it happened to sort into the first 5.
//  - the DELIVERY cap bounds what the buyer actually receives and pays for, and stays theirs.
const scanCapPerCompany = watchMode ? SEED_CAP : maxJobsPerCompany;
const deliverCapPerCompany = maxJobsPerCompany;

async function saveWatchRecord(status) {
  const ids = Array.from(watchSeen).slice(-WATCH_KEEP);
  await watchStore.setValue(watchKey, {
    ...watchRecord,
    label: watchLabel,
    lastRunAt: new Date().toISOString(),
    lastRunStatus: status,
    runCount: (watchRecord.runCount ?? 0) + 1,
    seenCount: ids.length,
    seenIds: ids,
  });
}

// Same reasoning as shopify-products-scraper (cycle 176) and google-news-scraper (cycle 191):
// route through Apify Proxy when available, but never fail a run just because the account has
// no proxy access — fall back to a direct connection.
let proxyUrlFor = async () => undefined;
try {
  const proxyConfiguration = await Actor.createProxyConfiguration(input.proxyConfiguration ?? { useApifyProxy: true });
  if (proxyConfiguration) {
    proxyUrlFor = (sessionId) => proxyConfiguration.newUrl(sessionId);
    log.info('Using Apify Proxy for ATS board requests.');
  }
} catch (e) {
  log.warning(`Proxy unavailable (${e.message}) — continuing with a direct connection.`);
}

// Sequential per-company loop over an unbounded company list, same risk class as the
// shopify/google-news multi-target loops (cycles 173-176, 191): stop proactively before the
// platform kills the run so partial results are still flushed.
const timeoutAt = Actor.getEnv().timeoutAt?.getTime() ?? null;
const TIME_BUDGET_MARGIN_MS = 45_000;
function timeBudgetOk() {
  if (timeoutAt == null) return true;
  return Date.now() < timeoutAt - TIME_BUDGET_MARGIN_MS;
}

let pushed = 0;
const isPPE = Actor.getChargingManager().getPricingInfo().isPayPerEvent;
async function pushResult(item, watchId) {
  // Seeding: record the id, push and charge nothing.
  if (watchMode && watchId != null && seeding) {
    watchSeen.add(String(watchId));
    return watchSeen.size < SEED_CAP;
  }
  // Already delivered under this label: dropped before any charge, so a repeat costs nothing.
  if (watchMode && watchId != null && watchSeen.has(String(watchId))) {
    watchSkipped += 1;
    return true;
  }
  if (isPPE) {
    const r = await Actor.charge({ eventName: 'job', count: 1 });
    if (r.chargedCount === 0) return false; // user's budget exhausted: never push unpaid items
    await Actor.pushData(item); pushed += 1;
    // Recorded as delivered only after the charge succeeded.
    if (watchMode && watchId != null) watchSeen.add(String(watchId));
    return !r.eventChargeLimitReached && pushed < maxResults;
  }
  await Actor.pushData(item); pushed += 1;
  if (watchMode && watchId != null) watchSeen.add(String(watchId));
  return pushed < maxResults;
}

async function getJson(url) {
  const res = await gotScraping({ url, timeout: { request: 30000 }, retry: { limit: 2 }, proxyUrl: await proxyUrlFor(), responseType: 'json' });
  return { status: res.statusCode, body: res.body };
}

// Greenhouse's `content` field comes back HTML-entity-encoded (e.g. "&lt;div&gt;") rather than
// raw HTML — decode it once so descriptionHtml is actually usable HTML, not escaped text.
function decodeEntities(s) {
  if (!s) return s;
  return s.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&amp;/g, '&');
}
function textOf(html) {
  if (!html) return null;
  return cheerio.load(html).text().replace(/\s+/g, ' ').trim() || null;
}

// The three ATSes that expose a pay period each spell it differently — Ashby "1 YEAR"/"1 HOUR",
// Recruitee "yearly"/"monthly", Lever "per-year-salary" (all four observed live, cycle 212).
// A normalized schema should not hand the buyer three vocabularies, so collapse to a bare unit.
function normalizeInterval(raw) {
  if (!raw) return null;
  const s = String(raw).toLowerCase();
  for (const unit of ['year', 'month', 'week', 'day', 'hour']) {
    if (s.includes(unit)) return unit;
  }
  return s === 'none' ? null : s;
}

// Ashby publishes structured pay when a board turns compensation on: `compensation.summaryComponents[]`
// (and the same shape nested under `compensationTiers[].components[]`) carries real numeric
// `minValue`/`maxValue` plus `currencyCode` and `interval`. Several component types share the array
// (`EquityPercentage`, `Commission`, ...) with null values — only the `Salary` one is a pay range.
// Measured live on jobs.ashbyhq.com/ramp (cycle 212): 138 of 145 postings carried a Salary component.
function ashbySalary(comp) {
  const pools = [comp?.summaryComponents, ...(comp?.compensationTiers ?? []).map((t) => t?.components)];
  for (const pool of pools) {
    if (!Array.isArray(pool)) continue;
    const salary = pool.find((c) => c?.compensationType === 'Salary' && (c.minValue != null || c.maxValue != null));
    if (salary) {
      return {
        min: salary.minValue ?? null,
        max: salary.maxValue ?? null,
        currency: salary.currencyCode ?? null,
        interval: normalizeInterval(salary.interval),
      };
    }
  }
  return { min: null, max: null, currency: null, interval: null };
}

async function fetchGreenhouse(slug) {
  const { status, body } = await getJson(`https://boards-api.greenhouse.io/v1/boards/${encodeURIComponent(slug)}/jobs?content=true`);
  if (status === 404) return { jobs: [], notFound: true };
  const jobs = body?.jobs ?? [];
  return {
    jobs: jobs.map((j) => {
      const html = needDescriptions ? decodeEntities(j.content) : null;
      const workplaceType = j.metadata?.find((m) => /workplace type/i.test(m.name || ''))?.value ?? null;
      return {
        company: slug, atsSource: 'greenhouse', jobId: String(j.id), title: j.title?.trim() ?? null,
        department: j.departments?.[0]?.name ?? null, team: null, employmentType: null,
        workplaceType, isRemote: /remote/i.test(j.location?.name ?? '') || (workplaceType ? /remote/i.test(workplaceType) : null),
        location: j.location?.name ?? null, secondaryLocations: (j.offices ?? []).slice(1).map((o) => o.name),
        country: null, region: null, city: null,
        salaryMin: null, salaryMax: null, salaryCurrency: null, salaryInterval: null,
        publishedAt: j.first_published ?? null, updatedAt: j.updated_at ?? null,
        jobUrl: j.absolute_url ?? null, applyUrl: j.absolute_url ?? null,
        descriptionHtml: html ?? null, descriptionText: needDescriptions ? textOf(html) : null,
      };
    }),
  };
}

async function fetchAshby(slug) {
  const { status, body } = await getJson(`https://api.ashbyhq.com/posting-api/job-board/${encodeURIComponent(slug)}?includeCompensation=true`);
  if (status === 404 || !body?.jobs) return { jobs: [], notFound: true };
  return {
    jobs: body.jobs.map((j) => {
      const pay = ashbySalary(j.compensation);
      return {
      company: slug, atsSource: 'ashby', jobId: j.id, title: j.title?.trim() ?? null,
      department: j.department ?? null, team: j.team ?? null,
      employmentType: j.employmentType ?? null, workplaceType: j.workplaceType ?? null, isRemote: j.isRemote ?? null,
      location: j.location ?? null,
      secondaryLocations: (j.secondaryLocations ?? []).map((l) => l.location).filter(Boolean),
      country: j.address?.postalAddress?.addressCountry ?? null,
      region: j.address?.postalAddress?.addressRegion ?? null,
      city: j.address?.postalAddress?.addressLocality ?? null,
      salaryMin: pay.min, salaryMax: pay.max, salaryCurrency: pay.currency, salaryInterval: pay.interval,
      publishedAt: j.publishedAt ?? null, updatedAt: null,
      jobUrl: j.jobUrl ?? null, applyUrl: j.applyUrl ?? null,
      descriptionHtml: needDescriptions ? (j.descriptionHtml ?? null) : null,
      descriptionText: needDescriptions ? textOf(j.descriptionHtml) : null,
      };
    }),
  };
}

async function fetchLever(slug) {
  const res = await gotScraping({ url: `https://api.lever.co/v0/postings/${encodeURIComponent(slug)}?mode=json`, timeout: { request: 30000 }, retry: { limit: 2 }, proxyUrl: await proxyUrlFor(), throwHttpErrors: false, responseType: 'json' });
  // Most well-known "Lever companies" have migrated to another ATS and now 404 here — that is
  // expected, not a failure, and must not fail the whole run (confirmed cycle 196: plaid, brex,
  // ramp, figma, huggingface, cohere, eventbrite, kickstarter all 404).
  if (res.statusCode === 404 || !Array.isArray(res.body)) return { jobs: [], notFound: true };
  return {
    jobs: res.body.map((j) => ({
      company: slug, atsSource: 'lever', jobId: j.id, title: j.text?.trim() ?? null,
      department: j.categories?.department ?? null, team: j.categories?.team ?? null,
      employmentType: j.categories?.commitment ?? null, workplaceType: j.workplaceType ?? null,
      isRemote: j.workplaceType ? /remote/i.test(j.workplaceType) : (j.categories?.location ? /remote/i.test(j.categories.location) : null),
      location: j.categories?.location ?? null, secondaryLocations: (j.categories?.allLocations ?? []).slice(1),
      country: j.country ?? null, region: null, city: null,
      salaryMin: j.salaryRange?.min ?? null, salaryMax: j.salaryRange?.max ?? null, salaryCurrency: j.salaryRange?.currency ?? null,
      salaryInterval: normalizeInterval(j.salaryRange?.interval),
      publishedAt: j.createdAt ? new Date(j.createdAt).toISOString() : null, updatedAt: null,
      jobUrl: j.hostedUrl ?? null, applyUrl: j.applyUrl ?? j.hostedUrl ?? null,
      descriptionHtml: needDescriptions ? (j.description ?? null) : null,
      descriptionText: needDescriptions ? (j.descriptionPlain ?? textOf(j.description)) : null,
    })),
  };
}

async function fetchRecruitee(slug) {
  const res = await gotScraping({ url: `https://${encodeURIComponent(slug)}.recruitee.com/api/offers/`, timeout: { request: 30000 }, retry: { limit: 2 }, proxyUrl: await proxyUrlFor(), throwHttpErrors: false, responseType: 'json' });
  if (res.statusCode !== 200 || !Array.isArray(res.body?.offers)) return { jobs: [], notFound: true };
  return {
    jobs: res.body.offers.map((o) => ({
      company: slug, atsSource: 'recruitee', jobId: String(o.id), title: o.title?.trim() ?? null,
      department: o.department ?? null, team: null, employmentType: o.employment_type_code ?? null,
      workplaceType: o.remote ? 'remote' : (o.on_site ? 'onsite' : (o.hybrid ? 'hybrid' : null)), isRemote: !!o.remote,
      location: o.location ?? null,
      secondaryLocations: (Array.isArray(o.locations) ? o.locations : []).slice(1).map((l) => (typeof l === 'string' ? l : (l?.city ?? l?.name))).filter(Boolean),
      country: o.country ?? null, region: o.state_name ?? null, city: o.city ?? null,
      // Recruitee serves salary.min/max as numeric strings (e.g. "2600"), not numbers — coerce or
      // the dataset schema's declared `number` type rejects the push (found live, cycle 197).
      salaryMin: o.salary?.min != null ? Number(o.salary.min) : null,
      salaryMax: o.salary?.max != null ? Number(o.salary.max) : null,
      salaryCurrency: o.salary?.currency ?? null,
      // Recruitee's `salary.period` ("yearly"/"monthly"/...) was being dropped, so a monthly
      // EUR 2600 and an annual USD 211400 landed in the same column with nothing to tell them
      // apart. Surface it (cycle 212).
      salaryInterval: normalizeInterval(o.salary?.period),
      publishedAt: o.published_at ?? null, updatedAt: o.updated_at ?? null,
      jobUrl: o.careers_url ?? null, applyUrl: o.careers_apply_url ?? o.careers_url ?? null,
      descriptionHtml: needDescriptions ? (o.description ?? null) : null,
      descriptionText: needDescriptions ? textOf(o.description) : null,
    })),
  };
}

async function fetchWorkable(slug) {
  const { status, body } = await getJson(`https://apply.workable.com/api/v1/widget/accounts/${encodeURIComponent(slug)}?details=true`);
  if (status === 404 || !Array.isArray(body?.jobs)) return { jobs: [], notFound: true };
  return {
    jobs: body.jobs.map((j) => ({
      company: slug, atsSource: 'workable', jobId: j.shortcode ?? null, title: j.title?.trim() ?? null,
      department: j.department ?? null, team: null, employmentType: j.employment_type ?? null,
      workplaceType: j.telecommuting ? 'remote' : null, isRemote: !!j.telecommuting,
      location: [j.city, j.state, j.country].filter(Boolean).join(', ') || null,
      secondaryLocations: (j.locations ?? []).slice(1)
        .map((l) => [l.city, l.region, l.country].filter(Boolean).join(', ')).filter(Boolean),
      country: j.country || null, region: j.state || null, city: j.city || null,
      // No compensation field anywhere in the widget payload across the boards checked cycle 198
      // (getresponse, automattic) — same "leave null, don't guess" call as ashby's compensation.
      salaryMin: null, salaryMax: null, salaryCurrency: null, salaryInterval: null,
      publishedAt: j.published_on ? new Date(j.published_on).toISOString() : null, updatedAt: null,
      jobUrl: j.url ?? null, applyUrl: j.application_url ?? j.url ?? null,
      descriptionHtml: needDescriptions ? (j.description ?? null) : null,
      descriptionText: needDescriptions ? textOf(j.description) : null,
    })),
  };
}

// SmartRecruiters' list endpoint (`/postings`) does not carry the job description — that only
// comes back from a per-job detail call (`/postings/<id>`, `jobAd.sections`). To avoid one HTTP
// request per posting on large boards (BMWDealerCareers alone has 194), filter on the cheap
// list-level fields first and only fetch full detail for the jobs that already pass and are
// within maxJobsPerCompany.
async function fetchSmartRecruitersDetail(slug, id) {
  try {
    const { status, body } = await getJson(`https://api.smartrecruiters.com/v1/companies/${encodeURIComponent(slug)}/postings/${encodeURIComponent(id)}`);
    return status === 200 ? body : null;
  } catch {
    return null;
  }
}

async function fetchSmartRecruiters(slug) {
  const pageSize = 100;
  const rawCap = Math.min(Math.max(scanCapPerCompany * 3, pageSize), watchMode ? SEED_CAP : 2000);
  const raw = [];
  let offset = 0;
  let notFoundFlag = false;
  while (raw.length < rawCap && timeBudgetOk()) {
    const { status, body } = await getJson(`https://api.smartrecruiters.com/v1/companies/${encodeURIComponent(slug)}/postings?limit=${pageSize}&offset=${offset}`);
    if (status === 404) { notFoundFlag = true; break; }
    const content = body?.content ?? [];
    if (!content.length) break;
    raw.push(...content);
    offset += pageSize;
    if (offset >= (body?.totalFound ?? 0)) break;
  }
  if (notFoundFlag) return { jobs: [], notFound: true };

  const mapped = raw.map((p) => {
    const loc = p.location ?? {};
    return {
      company: slug, atsSource: 'smartrecruiters', jobId: String(p.id), title: p.name?.trim() ?? null,
      department: p.department?.label ?? p.function?.label ?? null, team: null,
      employmentType: p.typeOfEmployment?.label ?? null,
      workplaceType: loc.remote ? 'remote' : (loc.hybrid ? 'hybrid' : (loc.city ? 'onsite' : null)),
      isRemote: !!loc.remote,
      location: [loc.city, loc.region, loc.country].filter(Boolean).join(', ') || (loc.remote ? 'Remote' : null),
      secondaryLocations: [],
      country: loc.country || null, region: loc.region || null, city: loc.city || null,
      // No compensation field observed on any real posting checked cycle 198 — leave null.
      salaryMin: null, salaryMax: null, salaryCurrency: null, salaryInterval: null,
      publishedAt: p.releasedDate ?? null, updatedAt: null,
      // The list endpoint (`/postings`) never carries postingUrl/applyUrl — confirmed live cycle
      // 198 (both fields absent on every raw posting checked). The URL format is deterministic
      // (`jobs.smartrecruiters.com/<company>/<id>`, slug suffix optional, confirmed 200 without
      // it), so build it rather than leave it null; the detail call below overwrites applyUrl
      // with the real referral-tagged link when includeDescriptions fetches it anyway.
      jobUrl: `https://jobs.smartrecruiters.com/${encodeURIComponent(slug)}/${encodeURIComponent(p.id)}`,
      applyUrl: `https://jobs.smartrecruiters.com/${encodeURIComponent(slug)}/${encodeURIComponent(p.id)}`,
      descriptionHtml: null, descriptionText: null,
      _rawId: p.id,
    };
  });

  const kept = [];
  for (const job of mapped) {
    if (!passesFilters(job, SMARTRECRUITERS_DEFERRED)) continue;
    kept.push(job);
    if (kept.length >= scanCapPerCompany) break;
  }
  if (needDescriptions) {
    for (const job of kept) {
      if (!timeBudgetOk()) break;
      // An already-delivered posting will be dropped before any push/charge, so spending a
      // detail request on it is pure waste — most of an incremental watch run is exactly that.
      if (watchMode && !seeding && watchSeen.has(String(watchIdFor(job)))) continue;
      const detail = await fetchSmartRecruitersDetail(slug, job._rawId);
      if (detail?.applyUrl) job.applyUrl = detail.applyUrl;
      if (detail?.postingUrl) job.jobUrl = detail.postingUrl;
      const sections = detail?.jobAd?.sections;
      if (sections) {
        const order = ['companyDescription', 'jobDescription', 'qualifications', 'additionalInformation'];
        const html = order.filter((k) => sections[k]?.text).map((k) => `<h3>${sections[k].title}</h3>${sections[k].text}`).join('');
        job.descriptionHtml = html || null;
        job.descriptionText = textOf(html);
      }
    }
  }
  kept.forEach((j) => { delete j._rawId; });
  return { jobs: kept };
}

// Workday's slug is not a single company identifier like the other five ATSes — its public
// career-board API is namespaced by tenant *and* wdN host *and* site (e.g. Walmart's board lives
// at `walmart.wd5.myworkdayjobs.com/WalmartExternal`), so the slug format here is
// `"<host>/<site>"`, e.g. `"okgov.wd1.myworkdayjobs.com/okgovjobs"`. Verified live (cycle 262):
// `POST https://<host>/wday/cxs/<tenant>/<site>/jobs` with body `{appliedFacets:{}, limit, offset,
// searchText:""}` returns `{total, jobPostings:[...]}`, no auth needed — `tenant` is the host's
// first label. `limit` caps at 20 per page (21+ returns HTTP 400); `total` is only meaningful on
// the offset-0 page (later pages return `total: 0` on some tenants — a real, reproducible quirk,
// not a bug in this code), so it's captured once and reused as the pagination stop condition.
async function fetchWorkdayDetail(host, tenant, site, externalPath) {
  try {
    const { status, body } = await getJson(`https://${host}/wday/cxs/${tenant}/${site}${externalPath}`);
    return status === 200 ? body : null;
  } catch {
    return null;
  }
}

async function fetchWorkday(slug) {
  const slashAt = slug.indexOf('/');
  const host = slashAt === -1 ? slug : slug.slice(0, slashAt);
  const site = slashAt === -1 ? '' : slug.slice(slashAt + 1);
  if (!site || !/\.myworkdayjobs\.com$/i.test(host)) return { jobs: [], notFound: true };
  const tenant = host.split('.')[0];
  const pageSize = 20;
  const rawCap = Math.min(Math.max(scanCapPerCompany * 3, pageSize), watchMode ? SEED_CAP : 2000);
  const raw = [];
  let offset = 0;
  let total = null;
  let notFoundFlag = false;
  while (raw.length < rawCap && timeBudgetOk()) {
    const res = await gotScraping({
      url: `https://${host}/wday/cxs/${tenant}/${site}/jobs`, method: 'POST',
      json: { appliedFacets: {}, limit: pageSize, offset, searchText: '' },
      timeout: { request: 30000 }, retry: { limit: 2 }, proxyUrl: await proxyUrlFor(),
      throwHttpErrors: false, responseType: 'json',
    });
    if (res.statusCode !== 200) { if (offset === 0) notFoundFlag = true; break; }
    if (offset === 0) total = res.body?.total ?? null;
    const postings = res.body?.jobPostings ?? [];
    if (!postings.length) break;
    raw.push(...postings);
    offset += pageSize;
    if (total != null && total > 0 && offset >= total) break;
  }
  if (notFoundFlag) return { jobs: [], notFound: true };

  // List-level fields only (title, locationsText, a relative "Posted N Days Ago" string, and the
  // requisition id in bulletFields) — no department, employment type, exact date or description
  // without a per-job detail call, same tradeoff `fetchSmartRecruiters` already makes above.
  const mapped = raw.map((p) => ({
    company: tenant, atsSource: 'workday', jobId: (p.bulletFields ?? [])[0] || p.externalPath || null,
    title: p.title?.trim() ?? null,
    department: null, team: null, employmentType: null, workplaceType: null,
    isRemote: /remote/i.test(p.locationsText ?? ''),
    location: p.locationsText ?? null, secondaryLocations: [],
    country: null, region: null, city: null,
    salaryMin: null, salaryMax: null, salaryCurrency: null, salaryInterval: null,
    publishedAt: null, updatedAt: null,
    jobUrl: `https://${host}/${site}${p.externalPath}`, applyUrl: `https://${host}/${site}${p.externalPath}`,
    descriptionHtml: null, descriptionText: null,
    _externalPath: p.externalPath,
  }));

  const kept = [];
  for (const job of mapped) {
    if (!passesFilters(job, WORKDAY_DEFERRED)) continue;
    kept.push(job);
    if (kept.length >= scanCapPerCompany) break;
  }
  if (workdayNeedsDetail) {
    for (const job of kept) {
      if (!timeBudgetOk()) break;
      if (watchMode && !seeding && watchSeen.has(String(watchIdFor(job)))) continue;
      const detail = await fetchWorkdayDetail(host, tenant, site, job._externalPath);
      const info = detail?.jobPostingInfo;
      if (info) {
        job.descriptionHtml = info.jobDescription ?? null;
        job.descriptionText = textOf(info.jobDescription);
        job.employmentType = info.timeType ?? null;
        job.location = info.jobRequisitionLocation?.descriptor ?? info.location ?? job.location;
        job.country = info.country?.descriptor ?? null;
        job.publishedAt = info.startDate ? new Date(info.startDate).toISOString() : null;
        job.jobUrl = info.externalUrl ?? job.jobUrl;
        job.applyUrl = info.externalUrl ?? job.applyUrl;
        // Workday has no dedicated "department" field in the public postings API; the hiring
        // organization name (e.g. "131 DEPARTMENT OF CORRECTIONS") is the closest real substitute
        // and matches what boards actually render as the owning org — verified live, cycle 262.
        job.department = detail?.hiringOrganization?.name ?? null;
      }
    }
  }
  kept.forEach((j) => { delete j._externalPath; });
  return { jobs: kept };
}

const FETCHERS = {
  greenhouse: fetchGreenhouse, ashby: fetchAshby, lever: fetchLever, recruitee: fetchRecruitee,
  workable: fetchWorkable, smartrecruiters: fetchSmartRecruiters, workday: fetchWorkday,
};

// Tries every auto-detectable platform for one slug in parallel and keeps the first (in
// AUTO_DETECT_ATS priority order) that actually found a board there. A slug existing as an empty
// board on one platform and a populated one on another (rare, but real — generic slugs like "demo")
// resolves to whichever platform has jobs; if none do, the first non-404 board wins so an existing-
// but-currently-empty board is still reported honestly rather than as "not found anywhere".
async function fetchAuto(slug) {
  const settled = await Promise.allSettled(AUTO_DETECT_ATS.map((ats) => FETCHERS[ats](slug)));
  const hits = AUTO_DETECT_ATS
    .map((ats, i) => ({ ats, outcome: settled[i] }))
    .filter((h) => h.outcome.status === 'fulfilled' && !h.outcome.value.notFound);
  // SmartRecruiters' postings endpoint returns 200 with an empty page for a company slug that
  // doesn't exist at all (no 404, unlike the other 5) — so an empty SmartRecruiters hit alone isn't
  // trustworthy evidence the slug is a real board there versus not on any platform. Only count it
  // when it actually has jobs; the other 5 fetchers all 404/non-200 on a truly unknown slug, so an
  // empty hit from one of those is a genuine (real board, zero current openings) signal.
  const trustworthy = hits.filter((h) => h.ats !== 'smartrecruiters' || h.outcome.value.jobs.length > 0);
  if (!trustworthy.length) return { jobs: [], notFound: true };
  const withJobs = trustworthy.find((h) => h.outcome.value.jobs.length > 0);
  const chosen = withJobs ?? trustworthy[0];
  if (trustworthy.length > 1) {
    log.info(`${slug} — auto-detect matched on multiple platforms (${trustworthy.map((h) => h.ats).join(', ')}), using ${chosen.ats}.`);
  }
  return { ...chosen.outcome.value, detectedAts: chosen.ats };
}

// SmartRecruiters and Workday only carry a subset of the schema in their list payload; the rest
// arrives from the per-job detail call, which runs AFTER their in-fetcher pre-filter. Checking a
// not-yet-populated field there would drop every posting on a value the detail call was about to
// fill (a real bug before cycle 408: employmentTypeKeyword/postedAfter silently returned zero rows
// for every Workday board). The pre-filter therefore skips those fields and the main loop's
// unrestricted passesFilters applies them once the job is enriched.
const SMARTRECRUITERS_DEFERRED = ['description'];
const WORKDAY_DEFERRED = ['description', 'employmentType', 'department', 'published'];

function passesFilters(job, deferred = []) {
  const ready = (field) => !deferred.includes(field);
  if (titleKeyword && !(job.title ?? '').toLowerCase().includes(titleKeyword)) return false;
  if (titleExcludeKeyword && (job.title ?? '').toLowerCase().includes(titleExcludeKeyword)) return false;
  if (locationKeyword || locationExcludeKeyword) {
    const haystack = `${job.location ?? ''} ${(job.secondaryLocations ?? []).join(' ')} ${job.city ?? ''} ${job.country ?? ''}`.toLowerCase();
    if (locationKeyword && !haystack.includes(locationKeyword)) return false;
    if (locationExcludeKeyword && haystack.includes(locationExcludeKeyword)) return false;
  }
  if (ready('employmentType') && employmentTypeKeyword
    && !(job.employmentType ?? '').toLowerCase().includes(employmentTypeKeyword)) return false;
  if (ready('department') && departmentKeyword
    && !(job.department ?? '').toLowerCase().includes(departmentKeyword)) return false;
  if (ready('description') && (descriptionKeyword || descriptionExcludeKeyword)) {
    // Match the plain text, not the HTML, so a keyword can't be satisfied by a tag/class name.
    const body = (job.descriptionText ?? '').toLowerCase();
    if (descriptionKeyword && !body.includes(descriptionKeyword)) return false;
    if (descriptionExcludeKeyword && body.includes(descriptionExcludeKeyword)) return false;
  }
  if (hasSalary && job.salaryMin == null && job.salaryMax == null) return false;
  if ((minSalary != null || maxSalary != null)) {
    if (job.salaryMin == null && job.salaryMax == null) return false;
    const jobMin = job.salaryMin ?? job.salaryMax;
    const jobMax = job.salaryMax ?? job.salaryMin;
    if (minSalary != null && jobMax < minSalary) return false;
    if (maxSalary != null && jobMin > maxSalary) return false;
  }
  if (remoteOnly && !job.isRemote) return false;
  if (ready('published') && (postedAfter || postedBefore) && job.publishedAt) {
    const d = new Date(job.publishedAt);
    if (!Number.isNaN(d.getTime())) {
      if (postedAfter && d < postedAfter) return false;
      if (postedBefore && d > postedBefore) return false;
    }
  }
  return true;
}

const notFoundCompanies = [];
const erroredCompanies = [];

try {
  for (const { ats, slug } of companies) {
    if (!timeBudgetOk()) { log.warning('Time budget nearly exhausted — stopping before remaining companies.'); break; }
    let result;
    try {
      result = ats === 'auto' ? await fetchAuto(slug) : await FETCHERS[ats](slug);
    } catch (e) {
      log.warning(`${ats}:${slug} — fetch failed (${e.message}), skipping this company.`);
      erroredCompanies.push({ ats, slug, error: e.message });
      continue;
    }
    if (result.notFound) { notFoundCompanies.push({ ats, slug }); continue; }
    if (result.detectedAts) log.info(`${slug} — auto-detected as ${result.detectedAts}.`);
    let scannedForCompany = 0;
    let deliveredForCompany = 0;
    for (const job of result.jobs) {
      if (scannedForCompany >= scanCapPerCompany) break;
      if (!seeding && deliveredForCompany >= deliverCapPerCompany) break;
      if (!passesFilters(job)) continue;
      scannedForCompany += 1;
      // A description fetched only to filter on (or, on Workday, only because the detail call had
      // to run anyway) never reaches the dataset when the buyer asked for rows without it.
      if (!includeDescriptions) { job.descriptionHtml = null; job.descriptionText = null; }
      job.scrapedAt = new Date().toISOString();
      const before = pushed;
      const keepGoing = await pushResult(job, watchMode ? watchIdFor(job) : null);
      if (pushed > before) deliveredForCompany += 1;
      if (!keepGoing) break;
    }
    log.info(`${ats}:${slug} — ${result.jobs.length} postings, ${scannedForCompany} kept after filters`
      + (watchMode ? `, ${deliveredForCompany} new.` : '.'));
    if (pushed >= maxResults) break;
    // A seeding run pushes nothing, so the maxResults stop above can never fire for it.
    if (seeding && watchSeen.size >= SEED_CAP) break;
  }
  if (notFoundCompanies.length) log.warning(`Not found / not on this ATS (skipped, run not failed): ${notFoundCompanies.map((c) => `${c.ats}:${c.slug}`).join(', ')}`);
  if (erroredCompanies.length) log.warning(`Fetch errors (skipped, run not failed): ${erroredCompanies.map((c) => `${c.ats}:${c.slug}`).join(', ')}`);
} catch (err) {
  log.exception(err, 'Run failed');
  await Actor.fail(`Run failed: ${err.message}`);
}

if (watchMode) {
  await saveWatchRecord(seeding ? 'seeded' : 'incremental');
  if (seeding) {
    log.info(
      `Baseline saved for watch label "${watchLabel}": ${watchSeen.size} posting(s) recorded as already-seen, `
      + '0 results returned, 0 charged. The next run on this label and these filters returns only postings '
      + 'that appeared after now.'
      + (watchSeen.size >= SEED_CAP
        ? ` NOTE: the baseline hit the ${SEED_CAP}-posting cap. Narrow the filters (title/location keyword, `
          + 'fewer companies) or postings beyond the cap will be reported as new next run.'
        : ''),
    );
    // A board that failed to answer during the seed contributes nothing to the baseline, so its
    // entire current board would come back as "new" (and billable) on the next run. Say so.
    if (erroredCompanies.length) {
      log.warning(
        `Baseline is INCOMPLETE for: ${erroredCompanies.map((c) => `${c.ats}:${c.slug}`).join(', ')} — those boards `
        + 'failed to respond during this seeding run, so their currently-open postings are not in the baseline and '
        + 'will be returned as new next run. Re-run the baseline (delete the record above from the '
        + `"${WATCH_STORE}" key-value store) if you want a clean start.`,
      );
    }
  } else {
    log.info(`Watch label "${watchLabel}": ${pushed} new posting(s) since the last run (${watchSkipped} already-delivered posting(s) skipped, not charged); baseline now holds ${watchSeen.size}.`);
  }
}

log.info(`Done. Pushed ${pushed} job postings from ${companies.length} companies.`);

if (watchMode && seeding) {
  await Actor.setStatusMessage(`Baseline run for watch label "${watchLabel}": ${watchSeen.size} currently-open posting(s) recorded, 0 charged. Run again later to get only what's new.`);
} else if (watchMode && pushed === 0) {
  await Actor.setStatusMessage(`Nothing new for watch label "${watchLabel}" since its last run -- every matching posting had already been delivered. That is the expected result most of the time; you were charged for nothing.`);
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
    companiesScanned: companies.length,
    companiesErrored: erroredCompanies.length,
    watchLabel: watchMode ? watchLabel : null,
    watchSeeding: watchMode ? seeding : null,
    watchNewCount: watchMode && !seeding ? pushed : null,
    watchSkippedCount: watchMode && !seeding ? watchSkipped : null,
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
