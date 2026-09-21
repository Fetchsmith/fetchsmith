// remote-jobs-scraper — remote job postings from four PUBLIC, documented, no-auth job APIs
// (Remotive, Remote OK, Jobicy, Arbeitnow), normalized into one schema and de-duplicated
// across boards. HTTP-only, no headless browser, pay-per-event on pushed rows only.
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
const ALL_SOURCES = ['remotive', 'remoteok', 'jobicy', 'arbeitnow'];

const SOURCE_SITE = {
  remotive: 'https://remotive.com',
  remoteok: 'https://remoteok.com',
  jobicy: 'https://jobicy.com',
  arbeitnow: 'https://www.arbeitnow.com',
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

async function fetchJson(url) {
  const res = await gotScraping({
    url,
    responseType: 'json',
    headers: { 'User-Agent': UA, Accept: 'application/json' },
    timeout: { request: 45000 },
    retry: { limit: 2 },
  });
  return res.body;
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
      salaryPeriod: num(j.salary_min) || num(j.salary_max) ? 'yearly' : null,
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

const FETCHERS = {
  remotive: fromRemotive,
  remoteok: fromRemoteOk,
  jobicy: fromJobicy,
  arbeitnow: fromArbeitnow,
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
      const rows = await FETCHERS[src]();
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
    const key = `${norm(row.company)}|${norm(row.title)}`;
    if (dedupe && norm(row.company) && norm(row.title) && byKey.has(key)) {
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
