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
// TMview's `fOffices` param is case-sensitive (live-verified: "us"/"de"/"Em" each return 0 rows
// where "US"/"DE"/"EM" return real ones). Every office code TMview publishes is a plain
// ISO-3166-1-alpha-2 country code or WO/EM/BX/OA -- always two uppercase letters, with no
// legitimate mixed-case form -- so a blanket uppercase is safe here.
// Same failure shape as TM_STATUSES/NICE_CLASS_COUNT below, found and fixed this cycle (936's
// enum_audit covered `statuses`, 1012's covered `niceClasses`, neither touched `offices`): a
// brute-force probe of all 676 two-uppercase-letter combinations against TMview's live API, with
// two unrelated broad search terms giving a byte-identical result both times, found exactly 81
// offices that return any rows at all. A code outside that set -- including plausible buyer
// mistakes like "UK" (the real code is GB) or "EU" (the real code is EM) -- silently returns 0
// rows with no warning, indistinguishable from a genuinely empty search.
const OFFICES = [
  'AL', 'AP', 'AR', 'AT', 'AU', 'BA', 'BG', 'BN', 'BR', 'BX', 'BZ', 'CA', 'CH', 'CL', 'CN', 'CO',
  'CR', 'CU', 'CY', 'CZ', 'DE', 'DK', 'DO', 'EE', 'EG', 'EM', 'ES', 'FI', 'FR', 'GB', 'GE', 'GR',
  'HR', 'HU', 'IE', 'IL', 'IN', 'IS', 'IT', 'JO', 'JP', 'KH', 'KR', 'LA', 'LI', 'LT', 'LV', 'MA',
  'MC', 'MD', 'ME', 'MK', 'MT', 'MX', 'MY', 'NO', 'NZ', 'OA', 'PE', 'PH', 'PL', 'PT', 'PY', 'RO',
  'RS', 'RU', 'SE', 'SI', 'SK', 'SM', 'TH', 'TN', 'TR', 'TT', 'UA', 'UG', 'US', 'UY', 'VN', 'WO',
  'ZM',
];
const OFFICE_SET = new Set(OFFICES);
const unknownOffices = [];
const offices = (Array.isArray(input.offices) ? input.offices : [])
  .map((o) => String(o).trim()).filter(Boolean)
  .map((o) => {
    const upper = o.toUpperCase();
    if (upper !== o) log.info(`Trademark office "${o}" matched TMview's "${upper}" — TMview's office codes are case-sensitive, so it was corrected for you.`);
    if (!OFFICE_SET.has(upper)) unknownOffices.push(o);
    return upper;
  });
// Forward-compatible: an unknown value is still sent (TMview may add offices), but say so.
if (unknownOffices.length) {
  log.warning(
    `Trademark office ${unknownOffices.map((o) => `"${o}"`).join(', ')} is not one of the ${OFFICES.length} offices `
    + `TMview currently covers — common mix-ups are "UK" (use "GB") and "EU" (use "EM"). TMview matches no marks at `
    + 'all against an unrecognised code, so this narrows your results rather than widening them. Fix it or drop it.',
  );
}
// The Nice Classification is a closed set of 45 classes (1-34 goods, 35-45 services), so a value
// outside it can never match a mark. Same failure shape as `statuses` below, verified live this
// cycle: `niceClasses:["46"]` returns 0 rows with no explanation, indistinguishable in the Console
// from a genuinely empty search. Zero-padding needs no correction -- TMview normalises it itself
// ("09" and "9" returned byte-identical rows, and a no-filter control returned different rows, so
// the padded form is honoured rather than silently ignored). A mix of valid and invalid values
// still returns the valid branches (`["9","46"]` === `["9"]`), so only an all-invalid list is fatal.
const NICE_CLASS_COUNT = 45;
const unknownNiceClasses = [];
const niceClasses = (Array.isArray(input.niceClasses) ? input.niceClasses : [])
  .map((c) => String(c).trim()).filter(Boolean)
  .map((c) => {
    // Accept anything TMview accepts (plain or zero-padded integer 1-45); flag the rest.
    const n = /^\d+$/.test(c) ? Number(c) : NaN;
    if (!Number.isInteger(n) || n < 1 || n > NICE_CLASS_COUNT) unknownNiceClasses.push(c);
    return c;
  });
// Forward-compatible: an unknown value is still sent (same call as `statuses` below), but say so.
if (unknownNiceClasses.length) {
  log.warning(
    `Nice class ${unknownNiceClasses.map((c) => `"${c}"`).join(', ')} is not a valid Nice Classification class `
    + `(1-${NICE_CLASS_COUNT}: 1-34 goods, 35-45 services) — no trademark carries it, so this narrows your results `
    + 'rather than widening them. Fix it or drop it.',
  );
}
// TMview's `fTMStatus` vocabulary is exactly these four, and it matches them case-sensitively
// (verified cycle 936 against the live API: a 1000-row sample spanning 59 offices produced only
// these four values, and each one on its own returns rows; every other plausible value --
// including `Withdrawn`, which this Actor's own schema/README used to offer as an example, plus
// `Opposed` and `Pending`, which the watch-mode copy suggested -- makes TMview declare 0 matches
// even on the broadest possible search, as does a lowercase `registered`). An unrecognised value
// is therefore not "no marks match it": it silently voids that branch of the filter, and before
// this guard the run just finished with an empty dataset and nothing to tell the buyer apart from
// a genuinely empty result set.
const TM_STATUSES = ['Registered', 'Filed', 'Ended', 'Expired'];
const TM_STATUS_BY_LOWER = new Map(TM_STATUSES.map((s) => [s.toLowerCase(), s]));
const unknownStatuses = [];
const statuses = (Array.isArray(input.statuses) ? input.statuses : [])
  .map((s) => String(s).trim()).filter(Boolean)
  .map((s) => {
    const canonical = TM_STATUS_BY_LOWER.get(s.toLowerCase());
    if (!canonical) { unknownStatuses.push(s); return s; }
    if (canonical !== s) log.info(`Trademark status "${s}" matched TMview's "${canonical}" — TMview compares these case-sensitively, so it was corrected for you.`);
    return canonical;
  });
// Forward-compatible: an unknown value is still sent (TMview may add statuses), but say so loudly,
// and say it twice when EVERY value is unknown, because then the run cannot return anything at all.
if (unknownStatuses.length) {
  log.warning(
    `Trademark status ${unknownStatuses.map((s) => `"${s}"`).join(', ')} is not one of the values TMview recognises `
    + `(${TM_STATUSES.join(', ')}) — TMview matches no marks at all against it, so this narrows your results to nothing `
    + 'rather than widening them. Fix the spelling or drop it.',
  );
}
const maxResults = Math.min(Number(input.maxResults ?? 50), 5000);
const watchLabel = String(input.watchLabel ?? '').trim();
const watchChanges = Boolean(input.watchChanges);
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

// TMview times out/resets on requests from Apify's default datacenter egress (verified cycle 513:
// works from this box directly, fails 3/3 on-platform without a proxy) — route through Apify Proxy.
let proxyConfiguration;
let proxyUrl;
try {
  proxyConfiguration = await Actor.createProxyConfiguration(input.proxyConfiguration ?? { useApifyProxy: true });
  if (proxyConfiguration) {
    proxyUrl = await proxyConfiguration.newUrl();
    log.info('Using Apify Proxy for TMview requests.');
  }
} catch (e) { log.warning(`Proxy unavailable (${e.message}) — continuing with a direct connection.`); }

// A single exit node that cannot reach TMview kills the whole run: measured 2026-09-21, every
// request came back `The proxy responded with 590 UPSTREAM502` (a CONNECT-level failure, so
// `throwHttpErrors:false` does not catch it and the run died on a raw stack trace) while the SAME
// query answered HTTP 200 directly from outside Apify — i.e. TMview was up, that exit node was not.
// So a transport failure now rotates to a fresh exit node before giving up, and only after every
// node has failed do we try direct (cycle 513 measured direct as unreliable from Apify's own
// egress, so it is a last resort, not the default).
const PROXY_ROTATIONS = 3;
async function rotateProxy() {
  if (!proxyConfiguration) return false;
  try {
    proxyUrl = await proxyConfiguration.newUrl(`s${Date.now()}${Math.floor(Math.random() * 1e6)}`);
    return true;
  } catch (e) { log.warning(`Could not get another proxy session (${e.message}).`); return false; }
}

// The rotation loop above is only useful if the run lives long enough to reach it. Measured on run
// bAeFGpiApFJl7u085 (2026-10-01, nightly health check, 180s budget): ONE 590 UPSTREAM502 attempt
// burned 128s — because `retry: { limit: 2 }` made got re-try the SAME dead exit node twice more
// inside a single attempt, each with its own 30s request timeout — and the platform then killed the
// container at 180s, part-way through rotation 1 of 3. TIMED-OUT is the worst outcome for a buyer:
// the container is killed, so they get no error message, no `setStatusMessage`, no RUN_SUMMARY and
// no watch-baseline save (h826). So: the per-request timeout is now the ONLY retry layer inside an
// attempt (`retry: { limit: 0 }` — a fresh exit node is a strictly better retry than hammering the
// broken one), and each attempt is sized to fit the time the run actually has left.
const REQUEST_TIMEOUT_MS = 30000;
// Reserve for the finishing work after the last attempt (push, charge, baseline save, webhook).
const DEADLINE_RESERVE_MS = 15000;
// Below this there is no point starting another attempt — stop and report instead of being killed.
const MIN_ATTEMPT_MS = 5000;
const RUN_DEADLINE_MS = (() => {
  const t = Actor.getEnv().timeoutAt;
  const ms = t instanceof Date ? t.getTime() : (t ? Date.parse(t) : NaN);
  return Number.isFinite(ms) ? ms : null; // null = no run timeout set; behave exactly as before
})();
// Infinity when the run has no timeout, so every comparison below is a no-op in that case.
const remainingBudgetMs = () => (RUN_DEADLINE_MS === null
  ? Infinity
  : RUN_DEADLINE_MS - Date.now() - DEADLINE_RESERVE_MS);

const isPPE = Actor.getChargingManager().getPricingInfo().isPayPerEvent;
let pushed = 0;
// Marks read off TMview this run (including ones dropped by watch mode) -- the webhook's
// "how much did we look at" number, distinct from `pushed` ("how much did you pay for").
let scanned = 0;

// Watch mode: "only what's new since my last run on this label+search" -- distinct from a
// plain search, which returns the same matching marks every time. Baseline (ST13 ids already
// delivered under this label+criteria, plus a snapshot of each mark's status) lives in a NAMED
// key-value store on the buyer's own account so it survives across runs (the default KV store is
// per-run and would reset). Same pattern as hacker-news-scraper/eu-ted-tenders-scraper etc.
// `watchChanges` (added after launch -- see below) re-delivers an already-seen mark when TMview's
// own status field moves (e.g. Pending -> Registered, or into Opposed/Expired) -- the core
// "opposition watch" value is catching a status transition, not just a brand-new filing.
const WATCH_STORE = 'fetchsmith-trademark-watch';
const SEED_CAP = 5000;
const WATCH_KEEP = 20000;

function watchKeyFor(label, criteria) {
  const safe = label.toLowerCase().replace(/[^a-z0-9_.-]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 40) || 'default';
  const fp = createHash('sha1').update(JSON.stringify(criteria, Object.keys(criteria).sort())).digest('hex').slice(0, 10);
  return { key: `watch-${safe}-${fp}`, fingerprint: fp };
}

// Snapshot is just `status` today -- the one TMview field the pre-watchChanges code flagged as
// worth tracking. Kept as its own function (rather than inlined) so a second tracked field later
// only touches this, changesBetween, and the two seenIds map/unmap sites.
function snapshotOf(item) {
  return { status: item.status ?? null };
}

// null unless a snapshot actually existed to compare against (a mark seen before watchChanges was
// ever turned on for this label has no prior status recorded, so its first post-upgrade sighting
// cannot be a "change" -- same undetectable-until-now-onward rule as grants-gov-scraper).
function changesBetween(prev, next) {
  if (!prev || prev.status === undefined || prev.status === null || prev.status === next.status) return null;
  return { types: ['status'], previous: { status: prev.status } };
}

const watchMode = watchLabel.length > 0;
let watchStore = null;
let watchKey = null;
let watchRecord = null;
let seeding = false;
let watchSkipped = 0;
let changedCount = 0;
let baselineTruncated = 0; // mark ids dropped by WATCH_KEEP this run -- they come back as "new" and get charged again
let baselineTruncatedTotal = 0; // same, cumulative over the life of this label
const watchSeen = new Map(); // ST13 id -> last-seen snapshot ({status})

if (watchMode) {
  const criteria = { searchTerm, offices, niceClasses, statuses };
  watchStore = await Actor.openKeyValueStore(WATCH_STORE);
  const { key, fingerprint } = watchKeyFor(watchLabel, criteria);
  watchKey = key;
  const existing = await watchStore.getValue(key);
  if (existing && Array.isArray(existing.seenIds)) {
    watchRecord = existing;
    // Pre-watchChanges records stored `seenIds` as a flat array of id strings -- handled here so
    // an existing buyer's baseline keeps working unchanged (no forced re-seed) and simply has no
    // status snapshot yet, so watchChanges only starts detecting drift from this run onward.
    for (const entry of existing.seenIds) {
      if (entry && typeof entry === 'object') watchSeen.set(String(entry.i), { status: entry.s ?? null });
      else watchSeen.set(String(entry), { status: null });
    }
    log.info(
      `Watch mode "${watchLabel}" (${key}): baseline from ${existing.lastRunAt ?? 'an earlier run'} holds `
      + `${watchSeen.size} already-delivered mark(s). Only marks NOT in that baseline will be returned and charged`
      + (watchChanges ? ', plus any already-delivered mark whose status has changed since last seen.' : '.'),
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
  const all = Array.from(watchSeen.entries());
  const entries = all.slice(-WATCH_KEEP);
  baselineTruncated = all.length - entries.length;
  baselineTruncatedTotal = (watchRecord.truncatedTotal ?? 0) + baselineTruncated;
  if (baselineTruncated > 0) {
    log.warning(
      `The baseline for watch label "${watchLabel}" exceeded the ${WATCH_KEEP}-entry record cap; the `
      + `${baselineTruncated} oldest mark id(s) were dropped (${baselineTruncatedTotal} dropped over the `
      + 'life of this label) and will be re-delivered and re-charged as "new" on a future run. Narrow the '
      + 'search (tighter term, fewer offices, specific Nice classes or statuses) to keep the baseline under the cap.',
    );
  }
  await watchStore.setValue(watchKey, {
    ...watchRecord,
    label: watchLabel,
    lastRunAt: new Date().toISOString(),
    lastRunStatus: status,
    runCount: (watchRecord.runCount ?? 0) + 1,
    seenCount: entries.length,
    // Compact shape: id + status only. WATCH_KEEP can hold up to 20,000 of these in one KV record.
    seenIds: entries.map(([id, snap]) => ({ i: id, s: snap.status })),
    truncatedLastRun: baselineTruncated,
    truncatedTotal: baselineTruncatedTotal,
  });
}

async function pushResult(item, watchId) {
  if (watchMode && watchId != null && seeding) {
    watchSeen.set(String(watchId), snapshotOf(item));
    return watchSeen.size < SEED_CAP;
  }
  let change = null;
  if (watchMode && watchId != null && watchSeen.has(String(watchId))) {
    const id = String(watchId);
    const nextSnap = snapshotOf(item);
    change = watchChanges ? changesBetween(watchSeen.get(id), nextSnap) : null;
    if (!change) {
      // Snapshot is kept current either way, so turning watchChanges on later detects only drift
      // from that point, not a backlog of status moves since the baseline.
      watchSeen.set(id, nextSnap);
      watchSkipped += 1;
      return true;
    }
    item = { ...item, _watchChangeType: change.types, _watchPrevious: change.previous };
  }
  if (isPPE) {
    const r = await Actor.charge({ eventName: 'result', count: 1 });
    if (r.chargedCount === 0) return false; // budget exhausted: never push unpaid items
    await Actor.pushData(item); pushed += 1;
    if (watchMode && watchId != null) {
      watchSeen.set(String(watchId), snapshotOf(item));
      if (change) changedCount += 1;
    }
    return !r.eventChargeLimitReached && pushed < maxResults;
  }
  await Actor.pushData(item); pushed += 1;
  if (watchMode && watchId != null) {
    watchSeen.set(String(watchId), snapshotOf(item));
    if (change) changedCount += 1;
  }
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

  // attempt 0 uses the session we already have; each later attempt rotates to a fresh exit node,
  // and the final one drops the proxy entirely.
  let lastErr;
  let outOfTime = false;
  for (let attempt = 0; attempt <= PROXY_ROTATIONS; attempt += 1) {
    const budget = remainingBudgetMs();
    if (budget < MIN_ATTEMPT_MS) { outOfTime = true; break; }
    if (attempt > 0) {
      const rotated = attempt < PROXY_ROTATIONS && await rotateProxy();
      if (!rotated) {
        if (!proxyUrl) break; // already direct and it still failed — nothing left to try
        log.warning('Every Apify Proxy session tried failed to reach TMview — retrying once on a direct connection.');
        proxyUrl = undefined;
      } else {
        log.warning(`TMview request failed through the proxy (${lastErr.message}) — retrying on a different proxy session (${attempt}/${PROXY_ROTATIONS}).`);
      }
    }
    let res;
    try {
      res = await gotScraping({
        url: API,
        method: 'POST',
        json: body,
        responseType: 'json',
        timeout: { request: Math.min(REQUEST_TIMEOUT_MS, budget) },
        retry: { limit: 0 },
        throwHttpErrors: false,
        proxyUrl,
      });
    } catch (e) {
      // Transport-level (proxy CONNECT refused/590, socket reset, DNS, timeout): no statusCode
      // exists, so this never reaches the check below. Rotate and try again.
      lastErr = e;
      continue;
    }
    if (res.statusCode !== 200) {
      throw new Error(`TMview returned HTTP ${res.statusCode}: ${JSON.stringify(res.body).slice(0, 300)}`);
    }
    return res.body ?? {};
  }
  // Deliberately a plain throw, not Actor.fail() (h287, same class as ats-jobs-scraper cycle
  // 678): Actor.fail() exits the process immediately, which — on a page-2+ failure — would skip
  // the watch-baseline save below and lose the record of rows this run already pushed and
  // charged for. Let the outer catch record the error and fail at the very end instead.
  if (outOfTime) {
    throw new Error(
      `This run's own time limit ran out while fetching page ${page} from TMview`
      + `${lastErr ? ` (last network error: ${lastErr.message})` : ''}. `
      + 'TMview behind Apify Proxy has spells of transient 590 UPSTREAM502 errors, and each retry on a '
      + 'fresh proxy session costs up to 30s. Raise the run timeout (Input > Run options; 300s+ is a '
      + 'safe default for this Actor), or re-run in a few minutes — the proxy route usually clears.',
    );
  }
  throw new Error(
    'Could not reach TMview (tmdn.org) through any network path this run: '
    + `${PROXY_ROTATIONS} Apify Proxy session(s) and a direct connection all failed transport-level — last error: ${lastErr?.message}. `
    + 'TMview itself is frequently reachable when this happens, so it is usually the proxy route rather than an outage: '
    + 're-run in a few minutes, or set "proxyConfiguration" to a residential group.',
  );
}

let runError = null;
// null unless TMview actually answered page 1 with its own total -- distinguishes "TMview
// declared 0 matches" from "we errored before ever getting a total" (h826).
let declaredMatches = null;
let totalPages = null;
let pagesFetched = 0;
// True only if the walk stopped before totalPages because THIS run's own maxResults or Apify
// cost limit was hit -- never because TMview refused a page (h824/h826: two platform runs, 60
// and then 100 pages -- the code's own ceiling -- both walked to completion with every row
// unique, so there is no observed "TMview cut us off early" case to distinguish from this one).
let stoppedByCap = false;

try {
  if (!searchTerm) {
    log.warning('No searchTerm provided — nothing to search. Finishing with 0 results.');
  } else {
    const first = await fetchPage(1);
    declaredMatches = Number(first.totalResults ?? 0);
    totalPages = Number(first.totalPages ?? 0);
    log.info(`TMview: ${declaredMatches} matches for "${searchTerm}"${offices.length ? ` in ${offices.join(', ')}` : ''} (${totalPages} pages).`);

    let keepGoing = true;
    let batch = first.tradeMarks ?? [];
    let page = 1;
    pagesFetched = 1;

    while (keepGoing && batch.length) {
      for (const tm of batch) {
        scanned += 1;
        keepGoing = await pushResult(normalize(tm), tm.ST13 ?? null);
        if (!keepGoing) break;
      }
      if (!keepGoing) { stoppedByCap = page < totalPages; break; }
      if (page >= totalPages) break;
      page += 1;
      const next = await fetchPage(page);
      batch = next.tradeMarks ?? [];
      pagesFetched += 1;
    }
  }
} catch (err) {
  // Deliberately NOT Actor.fail() here (h287, same class as fec-campaign-finance-scraper cycle
  // 676 / ats-jobs-scraper cycle 678): Actor.fail() exits the process immediately, so the watch
  // baseline save below would never run and every mark this run already pushed and CHARGED for
  // would be missing from the baseline and re-delivered/re-charged next run. Record the error,
  // let the tail of the script persist the baseline, and fail at the very end instead.
  log.exception(err, 'Run failed');
  runError = err.message;
}

// WATCH_KEEP record-cap eviction (h285): empty unless something was actually dropped, so it
// never taints the common case where the baseline comfortably fits under the cap. Computed
// AFTER saveWatchRecord() below, which is what actually sets baselineTruncated.
let evictionSuffix = '';

// A failed SEEDING run must NOT leave a partial baseline behind: an office/search-slice the seed
// walk never reached would look already-baselined to the next run and have its whole current
// match set delivered and CHARGED as "new". No record at all is the cheap outcome — the next run
// simply re-seeds for free.
const skipBaselineSave = watchMode && seeding && runError !== null;
if (skipBaselineSave) {
  log.warning(
    `The baseline run for "${watchLabel}" failed before it finished, so NO baseline was saved. `
    + 'Re-run on the same label and search to seed again (a baseline run charges nothing). Saving '
    + 'a partial baseline would have made the next run treat the un-reached mark(s) as freshly '
    + 'baselined and charge for the entire current match set.',
  );
}

if (watchMode && !skipBaselineSave) {
  await saveWatchRecord(runError ? 'failed-incremental' : (seeding ? 'seeded' : 'incremental'));
  evictionSuffix = baselineTruncated > 0
    ? ` WARNING: the watch baseline hit its ${WATCH_KEEP}-entry cap and ${baselineTruncated} oldest mark `
      + `id(s) were dropped (${baselineTruncatedTotal} dropped over the life of this label) -- they will be `
      + 're-delivered and re-charged as "new" on a future run. Narrow the search to keep the baseline under the cap.'
    : '';
  if (seeding) {
    log.info(
      `Baseline saved for watch label "${watchLabel}": ${watchSeen.size} mark(s) recorded as already-seen, `
      + '0 results returned, 0 charged. The next run on this label and search returns only new marks.'
      + (watchSeen.size >= SEED_CAP
        ? ` NOTE: the baseline hit the ${SEED_CAP}-mark cap. Narrow the search (tighter term, offices, class or `
        + 'status) so the whole current match set fits, or the first incremental run may report older marks past the cap as new.'
        : '') + evictionSuffix,
    );
    await Actor.setStatusMessage(`Baseline run for watch label "${watchLabel}": ${watchSeen.size} existing mark(s) recorded, 0 charged. Run again later to get only what's new.${evictionSuffix}`);
  } else {
    log.info(
      `Watch label "${watchLabel}": ${pushed - changedCount} new mark(s)`
      + (watchChanges ? ` and ${changedCount} changed mark(s) (status)` : '')
      + ` since the last run (${watchSkipped} already-delivered mark(s) skipped, not charged); baseline now holds ${watchSeen.size}.${evictionSuffix}`,
    );
    if (pushed === 0) {
      await Actor.setStatusMessage(`Nothing new for watch label "${watchLabel}" since its last run -- every matching mark had already been delivered. That is the expected result most of the time; you were charged for nothing.${evictionSuffix}`);
    } else if (baselineTruncated > 0) {
      await Actor.setStatusMessage(`Pushed ${pushed} new mark(s) for watch label "${watchLabel}".${evictionSuffix}`);
    }
  }
}

// RUN_SUMMARY: this run's completeness against TMview's own declared total, in a form a
// pipeline can read without parsing log lines. Fetch with
//   GET /v2/actor-runs/<runId>/key-value-store/records/RUN_SUMMARY
// Unlike court-records-scraper's exhausted/failed pair, there is no "TMview refused depth" state
// here to report (h824/h826 finding above) -- `complete` is false only for a buyer-imposed stop
// (maxResults/cost limit, `stoppedByCap`) or a transport failure (`error`), never a silent
// upstream cutoff.
const complete = runError === null && !stoppedByCap;
await Actor.setValue('RUN_SUMMARY', {
  searchTerm: searchTerm || null,
  declaredMatches,
  totalPages,
  pagesFetched,
  scanned,
  delivered: pushed,
  maxResults,
  complete,
  stoppedByCap,
  error: runError,
  unknownStatuses,
  unknownNiceClasses,
  unknownOffices,
  watchLabel: watchMode ? watchLabel : null,
  watchSeeding: watchMode ? seeding : null,
  watchNewCount: watchMode && !seeding ? pushed - changedCount : null,
  watchChangedCount: watchMode && !seeding ? changedCount : null,
});
// An empty dataset caused purely by an unrecognised status filter looks identical, from the
// Console, to a search that genuinely has no matches -- so name the cause there, not just in the
// log. Only when EVERY supplied status is unknown: a mixed list still returns its valid branches.
if (pushed === 0 && statuses.length > 0 && unknownStatuses.length === statuses.length) {
  await Actor.setStatusMessage(
    `0 results because the status filter ${unknownStatuses.map((s) => `"${s}"`).join(', ')} matches nothing in TMview — `
    + `it only recognises ${TM_STATUSES.join(', ')} (case-sensitive). This is a filter-value problem, not an empty search.`,
  );
} else if (pushed === 0 && niceClasses.length > 0 && unknownNiceClasses.length === niceClasses.length) {
  await Actor.setStatusMessage(
    `0 results because the Nice class filter ${unknownNiceClasses.map((c) => `"${c}"`).join(', ')} matches nothing — `
    + `the Nice Classification only has classes 1-${NICE_CLASS_COUNT} (1-34 goods, 35-45 services). `
    + 'This is a filter-value problem, not an empty search.',
  );
} else if (pushed === 0 && offices.length > 0 && unknownOffices.length === offices.length) {
  await Actor.setStatusMessage(
    `0 results because the office filter ${unknownOffices.map((o) => `"${o}"`).join(', ')} matches nothing in TMview — `
    + `it only covers ${OFFICES.length} offices (common mix-ups: "UK" should be "GB", "EU" should be "EM"). `
    + 'This is a filter-value problem, not an empty search.',
  );
} else if (stoppedByCap) {
  await Actor.setStatusMessage(
    `Pushed ${pushed.toLocaleString('en-US')} of ${declaredMatches?.toLocaleString('en-US') ?? '?'} matches TMview declared for this search — `
    + 'stopped early because of this run\'s own maxResults or Apify cost limit, not because TMview ran out of results. '
    + 'Raise maxResults (or the run\'s cost limit) to get more. See RUN_SUMMARY.',
  );
}

log.info(`Done. Pushed ${pushed} results.${watchLabel ? ` Watch label: ${watchLabel}` : ''}`);

// Fires after every row is already pushed and charged, so a slow or failing webhook can never
// affect the result set or the bill -- best-effort only, one attempt, short timeout, failures are
// a warning not a thrown error.
if (webhookUrl) {
  const env = Actor.getEnv();
  const payload = {
    actorRunId: env.actorRunId ?? null,
    defaultDatasetId: env.defaultDatasetId ?? null,
    finishedAt: new Date().toISOString(),
    pushed,
    scanned,
    watchLabel: watchMode ? watchLabel : null,
    watchSeeding: watchMode ? seeding : null,
    watchNewCount: watchMode && !seeding ? pushed - changedCount : null,
    watchChangedCount: watchMode && !seeding ? changedCount : null,
    watchSkippedCount: watchMode && !seeding ? watchSkipped : null,
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

// The failure signal itself is unchanged — the run still ends FAILED. It just happens here, after
// the baseline and webhook have been persisted, instead of where Actor.fail's immediate exit would
// have skipped both.
if (runError) await Actor.fail(`Run failed: ${runError}`);

await Actor.exit();
