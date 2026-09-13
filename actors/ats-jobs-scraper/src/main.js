// ATS Jobs Scraper: pulls live job postings from Greenhouse, Ashby, Lever and Recruitee
// company boards and normalizes them into one cross-ATS schema. No headless browser — every
// source is a documented, no-auth, no-login JSON endpoint.
import { Actor, log } from 'apify';
import * as cheerio from 'cheerio';
import { gotScraping } from 'got-scraping';

await Actor.init();
const input = (await Actor.getInput()) ?? {};

const DEFAULT_COMPANIES = [
  { ats: 'greenhouse', slug: 'airbnb' },
  { ats: 'ashby', slug: 'ramp' },
  { ats: 'lever', slug: 'leverdemo' },
  { ats: 'recruitee', slug: 'vandebron' },
];
const companies = (Array.isArray(input.companies) && input.companies.length ? input.companies : DEFAULT_COMPANIES)
  .map((c) => ({ ats: String(c.ats || '').toLowerCase().trim(), slug: String(c.slug || '').trim() }))
  .filter((c) => c.slug && ['greenhouse', 'ashby', 'lever', 'recruitee'].includes(c.ats));
if (!companies.length) await Actor.fail('Provide at least one company as {"ats": "greenhouse|ashby|lever|recruitee", "slug": "<company-slug>"}.');

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
        salaryMin: null, salaryMax: null, salaryCurrency: null,
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
    jobs: body.jobs.map((j) => ({
      company: slug, atsSource: 'ashby', jobId: j.id, title: j.title?.trim() ?? null,
      department: j.department ?? null, team: j.team ?? null,
      employmentType: j.employmentType ?? null, workplaceType: j.workplaceType ?? null, isRemote: j.isRemote ?? null,
      location: j.location ?? null,
      secondaryLocations: (j.secondaryLocations ?? []).map((l) => l.location).filter(Boolean),
      country: j.address?.postalAddress?.addressCountry ?? null,
      region: j.address?.postalAddress?.addressRegion ?? null,
      city: j.address?.postalAddress?.addressLocality ?? null,
      // Ashby's compensation payload shape is not confirmed against a real numeric example yet
      // (shouldDisplayCompensationOnJobPostings was false on every board checked cycle 197) —
      // leave null rather than guess a field path; revisit if a board with real numbers turns up.
      salaryMin: null, salaryMax: null, salaryCurrency: null,
      publishedAt: j.publishedAt ?? null, updatedAt: null,
      jobUrl: j.jobUrl ?? null, applyUrl: j.applyUrl ?? null,
      descriptionHtml: includeDescriptions ? (j.descriptionHtml ?? null) : null,
      descriptionText: includeDescriptions ? textOf(j.descriptionHtml) : null,
    })),
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
      publishedAt: o.published_at ?? null, updatedAt: o.updated_at ?? null,
      jobUrl: o.careers_url ?? null, applyUrl: o.careers_apply_url ?? o.careers_url ?? null,
      descriptionHtml: includeDescriptions ? (o.description ?? null) : null,
      descriptionText: includeDescriptions ? textOf(o.description) : null,
    })),
  };
}

const FETCHERS = { greenhouse: fetchGreenhouse, ashby: fetchAshby, lever: fetchLever, recruitee: fetchRecruitee };

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
