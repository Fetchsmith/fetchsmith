// ATS Jobs Scraper: pulls live job postings from Greenhouse, Ashby, Lever, Recruitee, Workable,
// SmartRecruiters and Workday company boards and normalizes them into one cross-ATS schema. No
// headless browser — every source is a documented, no-auth, no-login JSON endpoint.
import { Actor, log } from 'apify';
import * as cheerio from 'cheerio';
import { gotScraping } from 'got-scraping';

await Actor.init();
const input = (await Actor.getInput()) ?? {};

const SUPPORTED_ATS = ['greenhouse', 'ashby', 'lever', 'recruitee', 'workable', 'smartrecruiters', 'workday'];
const DEFAULT_COMPANIES = [
  { ats: 'greenhouse', slug: 'airbnb' },
  { ats: 'ashby', slug: 'ramp' },
  { ats: 'lever', slug: 'leverdemo' },
  { ats: 'recruitee', slug: 'vandebron' },
  { ats: 'workable', slug: 'getresponse' },
  { ats: 'smartrecruiters', slug: 'ElasticBandCompany' },
  { ats: 'workday', slug: 'okgov.wd1.myworkdayjobs.com/okgovjobs' },
];
const companies = (Array.isArray(input.companies) && input.companies.length ? input.companies : DEFAULT_COMPANIES)
  .map((c) => ({ ats: String(c.ats || '').toLowerCase().trim(), slug: String(c.slug || '').trim() }))
  .filter((c) => c.slug && SUPPORTED_ATS.includes(c.ats));
if (!companies.length) await Actor.fail(`Provide at least one company as {"ats": "${SUPPORTED_ATS.join('|')}", "slug": "<company-slug>"}.`);

const titleKeyword = (input.titleKeyword ?? '').toLowerCase().trim();
const locationKeyword = (input.locationKeyword ?? '').toLowerCase().trim();
const remoteOnly = !!input.remoteOnly;
const postedAfter = input.postedAfter ? new Date(input.postedAfter) : null;
const includeDescriptions = input.includeDescriptions !== false;
const maxJobsPerCompany = Math.min(Number(input.maxJobsPerCompany ?? 500), 5000);
const maxResults = Math.min(Number(input.maxResults ?? 2000), 100000);

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
async function pushResult(item) {
  if (isPPE) {
    const r = await Actor.charge({ eventName: 'job', count: 1 });
    if (r.chargedCount === 0) return false; // user's budget exhausted: never push unpaid items
    await Actor.pushData(item); pushed += 1;
    return !r.eventChargeLimitReached && pushed < maxResults;
  }
  await Actor.pushData(item); pushed += 1;
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
      const html = includeDescriptions ? decodeEntities(j.content) : null;
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
        descriptionHtml: html ?? null, descriptionText: includeDescriptions ? textOf(html) : null,
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
      descriptionHtml: includeDescriptions ? (j.descriptionHtml ?? null) : null,
      descriptionText: includeDescriptions ? textOf(j.descriptionHtml) : null,
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
      descriptionHtml: includeDescriptions ? (j.description ?? null) : null,
      descriptionText: includeDescriptions ? (j.descriptionPlain ?? textOf(j.description)) : null,
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
      descriptionHtml: includeDescriptions ? (o.description ?? null) : null,
      descriptionText: includeDescriptions ? textOf(o.description) : null,
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
      descriptionHtml: includeDescriptions ? (j.description ?? null) : null,
      descriptionText: includeDescriptions ? textOf(j.description) : null,
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
  const rawCap = Math.min(Math.max(maxJobsPerCompany * 3, pageSize), 2000);
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
    if (!passesFilters(job)) continue;
    kept.push(job);
    if (kept.length >= maxJobsPerCompany) break;
  }
  if (includeDescriptions) {
    for (const job of kept) {
      if (!timeBudgetOk()) break;
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
  const rawCap = Math.min(Math.max(maxJobsPerCompany * 3, pageSize), 2000);
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
    if (!passesFilters(job)) continue;
    kept.push(job);
    if (kept.length >= maxJobsPerCompany) break;
  }
  if (includeDescriptions) {
    for (const job of kept) {
      if (!timeBudgetOk()) break;
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

function passesFilters(job) {
  if (titleKeyword && !(job.title ?? '').toLowerCase().includes(titleKeyword)) return false;
  if (locationKeyword) {
    const haystack = `${job.location ?? ''} ${(job.secondaryLocations ?? []).join(' ')} ${job.city ?? ''} ${job.country ?? ''}`.toLowerCase();
    if (!haystack.includes(locationKeyword)) return false;
  }
  if (remoteOnly && !job.isRemote) return false;
  if (postedAfter && job.publishedAt) {
    const d = new Date(job.publishedAt);
    if (!Number.isNaN(d.getTime()) && d < postedAfter) return false;
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
      result = await FETCHERS[ats](slug);
    } catch (e) {
      log.warning(`${ats}:${slug} — fetch failed (${e.message}), skipping this company.`);
      erroredCompanies.push({ ats, slug, error: e.message });
      continue;
    }
    if (result.notFound) { notFoundCompanies.push({ ats, slug }); continue; }
    let keptForCompany = 0;
    for (const job of result.jobs) {
      if (keptForCompany >= maxJobsPerCompany) break;
      if (!passesFilters(job)) continue;
      keptForCompany += 1;
      job.scrapedAt = new Date().toISOString();
      const keepGoing = await pushResult(job);
      if (!keepGoing) break;
    }
    log.info(`${ats}:${slug} — ${result.jobs.length} postings, ${keptForCompany} kept after filters.`);
    if (pushed >= maxResults) break;
  }
  if (notFoundCompanies.length) log.warning(`Not found / not on this ATS (skipped, run not failed): ${notFoundCompanies.map((c) => `${c.ats}:${c.slug}`).join(', ')}`);
  if (erroredCompanies.length) log.warning(`Fetch errors (skipped, run not failed): ${erroredCompanies.map((c) => `${c.ats}:${c.slug}`).join(', ')}`);
} catch (err) {
  log.exception(err, 'Run failed');
  await Actor.fail(`Run failed: ${err.message}`);
}

log.info(`Done. Pushed ${pushed} job postings from ${companies.length} companies.`);
await Actor.exit();
