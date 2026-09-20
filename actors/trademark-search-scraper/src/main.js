// Trademark Search Scraper — TMview (EUIPO/TMDN) public search API, 70+ national offices.
// HTTP-only JSON API, no headless browser. Charges 'result' per pushed row.
import { createHash } from 'crypto';
import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';

await Actor.init();
const input = (await Actor.getInput()) ?? {};

const API = 'https://www.tmdn.org/tmview/api/search/results';
const PAGE_SIZE = 50; // verified server-side: pageSize 50 returns 50 rows

const searchTerm = String(input.searchTerm ?? '').trim();
const offices = Array.isArray(input.offices) ? input.offices.filter(Boolean) : [];
const niceClasses = (Array.isArray(input.niceClasses) ? input.niceClasses : [])
  .map((c) => String(c).trim()).filter(Boolean);
const statuses = (Array.isArray(input.statuses) ? input.statuses : []).filter(Boolean);
const maxResults = Math.min(Number(input.maxResults ?? 50), 5000);
const watchLabel = String(input.watchLabel ?? '').trim();

// TMview times out/resets on requests from Apify's default datacenter egress (verified cycle 513:
// works from this box directly, fails 3/3 on-platform without a proxy) — route through Apify Proxy.
let proxyUrl;
try {
  const proxyConfiguration = await Actor.createProxyConfiguration(input.proxyConfiguration ?? { useApifyProxy: true });
  if (proxyConfiguration) {
    proxyUrl = await proxyConfiguration.newUrl();
    log.info('Using Apify Proxy for TMview requests.');
  }
} catch (e) { log.warning(`Proxy unavailable (${e.message}) — continuing with a direct connection.`); }

const isPPE = Actor.getChargingManager().getPricingInfo().isPayPerEvent;
let pushed = 0;

// Watch mode: "only what's new since my last run on this label+search" -- distinct from a
// plain search, which returns the same matching marks every time. Baseline (ST13 ids already
// delivered under this label+criteria) lives in a NAMED key-value store on the buyer's own
// account so it survives across runs (the default KV store is per-run and would reset).
// Same pattern as hacker-news-scraper/eu-ted-tenders-scraper etc. No watchChanges here (unlike
// fda-recall-scraper/grants-gov-scraper): TMview's own status field can move Pending->Registered,
// but tracking that transition needs re-querying every known id, out of scope for this pass --
// new-matches-only is still the core "opposition watch" value (catching new filings early).
const WATCH_STORE = 'fetchsmith-trademark-watch';
const SEED_CAP = 5000;
const WATCH_KEEP = 20000;

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
const watchSeen = new Set();

if (watchMode) {
  const criteria = { searchTerm, offices, niceClasses, statuses };
  watchStore = await Actor.openKeyValueStore(WATCH_STORE);
  const { key, fingerprint } = watchKeyFor(watchLabel, criteria);
  watchKey = key;
  const existing = await watchStore.getValue(key);
  if (existing && Array.isArray(existing.seenIds)) {
    watchRecord = existing;
    for (const id of existing.seenIds) watchSeen.add(String(id));
    log.info(
      `Watch mode "${watchLabel}" (${key}): baseline from ${existing.lastRunAt ?? 'an earlier run'} holds `
      + `${watchSeen.size} already-delivered mark(s). Only marks NOT in that baseline will be returned and charged.`,
    );
  } else {
    watchRecord = { fingerprint, firstSeededAt: new Date().toISOString(), runCount: 0 };
    seeding = true;
    log.info(
      `Watch mode "${watchLabel}" (${key}): FIRST run for this label and search, so this is a baseline run. `
      + 'It records which marks already match and returns ZERO results (charged nothing). Run it again on the '
      + 'same label/search -- on a schedule, typically -- to get only marks that are new since now.',
    );
  }
}

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

async function pushResult(item, watchId) {
  if (watchMode && watchId != null && seeding) {
    watchSeen.add(String(watchId));
    return watchSeen.size < SEED_CAP;
  }
  if (watchMode && watchId != null && watchSeen.has(String(watchId))) {
    watchSkipped += 1;
    return true;
  }
  if (isPPE) {
    const r = await Actor.charge({ eventName: 'result', count: 1 });
    if (r.chargedCount === 0) return false; // budget exhausted: never push unpaid items
    await Actor.pushData(item); pushed += 1;
    if (watchMode && watchId != null) watchSeen.add(String(watchId));
    return !r.eventChargeLimitReached && pushed < maxResults;
  }
  await Actor.pushData(item); pushed += 1;
  if (watchMode && watchId != null) watchSeen.add(String(watchId));
  return pushed < maxResults;
}

// TMview returns dates as ISO timestamps at midday UTC; buyers want a plain calendar date.
function toDate(v) {
  if (!v) return null;
  const s = String(v);
  return /^\d{4}-\d{2}-\d{2}/.test(s) ? s.slice(0, 10) : null;
}

function normalize(tm) {
  const st13 = tm.ST13 ?? null;
  return {
    id: st13,
    st13,
    url: tm.tmOfficeURL ?? null,
    trademarkName: tm.tmName ?? null,
    office: tm.tmOffice ?? null,
    status: tm.tradeMarkStatus ?? null,
    trademarkType: tm.tradeMarkType ?? null,
    applicationNumber: tm.applicationNumber ?? null,
    registrationNumber: tm.registrationNumber ?? null,
    applicationDate: toDate(tm.applicationDate),
    registrationDate: toDate(tm.registrationDate),
    expirationDate: toDate(tm.expirationDate),
    oppositionPeriodStart: toDate(tm.oppositionPeriodStart),
    oppositionDeadline: toDate(tm.oppositionDeadLine),
    seniorityClaimed: typeof tm.seniorityClaimed === 'boolean' ? tm.seniorityClaimed : null,
    applicantNames: Array.isArray(tm.applicantName) ? tm.applicantName.map(String) : [],
    niceClasses: Array.isArray(tm.niceClass) ? tm.niceClass.map(String) : [],
    viennaCodes: Array.isArray(tm.viennaCodes) ? tm.viennaCodes.map(String) : [],
    territories: Array.isArray(tm.tProtection) ? tm.tProtection.map(String) : [],
    markImageUrl: tm.markImageURI ?? null,
    detailImageUrl: tm.detailImageURI ?? null,
    ...(watchLabel ? { watchLabel } : {}),
  };
}

async function fetchPage(page) {
  const body = {
    page: String(page),
    pageSize: String(PAGE_SIZE),
    criteria: 'C', // "contains" — the API rejects unknown criteria codes with HTTP 400
    basicSearch: searchTerm,
  };
  if (offices.length) body.fOffices = offices;
  if (niceClasses.length) body.fNiceClass = niceClasses;
  if (statuses.length) body.fTMStatus = statuses;

  const res = await gotScraping({
    url: API,
    method: 'POST',
    json: body,
    responseType: 'json',
    timeout: { request: 30000 },
    retry: { limit: 2 },
    throwHttpErrors: false,
    proxyUrl,
  });
  if (res.statusCode !== 200) {
    throw new Error(`TMview returned HTTP ${res.statusCode}: ${JSON.stringify(res.body).slice(0, 300)}`);
  }
  return res.body ?? {};
}

try {
  if (!searchTerm) {
    log.warning('No searchTerm provided — nothing to search. Finishing with 0 results.');
  } else {
    const first = await fetchPage(1);
    const total = Number(first.totalResults ?? 0);
    const totalPages = Number(first.totalPages ?? 0);
    log.info(`TMview: ${total} matches for "${searchTerm}"${offices.length ? ` in ${offices.join(', ')}` : ''} (${totalPages} pages).`);

    let keepGoing = true;
    let batch = first.tradeMarks ?? [];
    let page = 1;

    while (keepGoing && batch.length) {
      for (const tm of batch) {
        keepGoing = await pushResult(normalize(tm), tm.ST13 ?? null);
        if (!keepGoing) break;
      }
      if (!keepGoing || page >= totalPages) break;
      page += 1;
      const next = await fetchPage(page);
      batch = next.tradeMarks ?? [];
    }
  }
} catch (err) {
  log.exception(err, 'Run failed');
  await Actor.fail(`Run failed: ${err.message}`);
}

if (watchMode) {
  await saveWatchRecord(seeding ? 'seeded' : 'incremental');
  if (seeding) {
    log.info(
      `Baseline saved for watch label "${watchLabel}": ${watchSeen.size} mark(s) recorded as already-seen, `
      + '0 results returned, 0 charged. The next run on this label and search returns only new marks.'
      + (watchSeen.size >= SEED_CAP
        ? ` NOTE: the baseline hit the ${SEED_CAP}-mark cap. Narrow the search (tighter term, offices, class or `
        + 'status) so the whole current match set fits, or the first incremental run may report older marks past the cap as new.'
        : ''),
    );
    await Actor.setStatusMessage(`Baseline run for watch label "${watchLabel}": ${watchSeen.size} existing mark(s) recorded, 0 charged. Run again later to get only what's new.`);
  } else {
    log.info(`Watch label "${watchLabel}": ${pushed} new mark(s) since the last run (${watchSkipped} already-delivered mark(s) skipped, not charged); baseline now holds ${watchSeen.size}.`);
    if (pushed === 0) {
      await Actor.setStatusMessage(`Nothing new for watch label "${watchLabel}" since its last run -- every matching mark had already been delivered. That is the expected result most of the time; you were charged for nothing.`);
    }
  }
}

log.info(`Done. Pushed ${pushed} results.${watchLabel ? ` Watch label: ${watchLabel}` : ''}`);
await Actor.exit();
