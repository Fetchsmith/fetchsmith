import { createHash } from 'crypto';
import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';

await Actor.init();
// A run with many queries and enrichGithubLinks on does up to GITHUB_LOOKUP_CAP sequential
// per-item GitHub calls nested inside a per-query outer loop -- the same compounding-latency
// shape as the google-news-scraper timeout bug. Getting hard-killed there returns nothing to
// the customer even though partial results already exist in the dataset. Stop proactively with
// a safety margin and flush what's collected instead (pattern mirrored from google-news-scraper).
const timeoutAt = Actor.getEnv().timeoutAt?.getTime() ?? null;
const TIME_BUDGET_MARGIN_MS = 45_000;
let timeBudgetExceeded = false;
// Milliseconds of useful work left before the margin starts. Infinity on a local/dev run, where
// the platform sets no deadline.
function remainingMs() { return timeoutAt == null ? Infinity : timeoutAt - Date.now() - TIME_BUDGET_MARGIN_MS; }
function timeBudgetOk() {
  if (remainingMs() <= 0) { timeBudgetExceeded = true; return false; }
  return true;
}
const input = (await Actor.getInput()) ?? {};

const queries = (input.queries ?? []).map((q) => String(q).trim()).filter((q) => q.length);
const tags = (input.tags ?? ['story']).filter(Boolean);
const sortBy = input.sortBy === 'date' ? 'search_by_date' : 'search';
const maxItemsPerQuery = Math.min(Number(input.maxItemsPerQuery ?? 100), 1000);
const maxResults = Math.min(Number(input.maxResults ?? 200), 5000);
const includeComments = input.includeComments !== false;
const numericFilters = [];
if (input.postedAfter) numericFilters.push(`created_at_i>${Math.floor(new Date(input.postedAfter).getTime() / 1000)}`);
if (input.postedBefore) numericFilters.push(`created_at_i<${Math.floor(new Date(input.postedBefore).getTime() / 1000)}`);
if (input.minPoints) numericFilters.push(`points>=${Number(input.minPoints)}`);
if (input.minComments) numericFilters.push(`num_comments>=${Number(input.minComments)}`);
const author = input.author ? String(input.author).trim() : null;
const usernames = [...new Set((input.usernames ?? []).map((u) => String(u).trim()).filter((u) => u.length))];
const watchLabel = String(input.watchLabel ?? '').trim();
// Watch-mode change alerts. HN points/comments are NOT the kind of rare one-time flip the rest of
// the fleet's watchChanges options diff (a recall's status, a docket's dateTerminated, a listing
// going closed) -- they are counters that tick up on nearly every poll of an active story. A bare
// "previous !== current" diff would therefore re-deliver AND RE-CHARGE for the same trending story
// on run after run, which is worse for the buyer than the gap it closes. So the event fires only
// when a count CROSSES a milestone the previous snapshot hadn't reached yet: each threshold pays
// out at most once per item, so a story climbing 51 -> 99 points over 20 runs stays silent and
// bills once, at 100.
const watchChanges = input.watchChanges === true;
// Blank (not merely absent) disables that ladder, so a buyer who only wants comment milestones can
// clear the points field rather than needing a separate on/off toggle per ladder.
function parseMilestones(raw, fallback) {
  const src = raw === undefined || raw === null ? fallback : raw;
  return [...new Set(
    String(src).split(/[,;\s]+/).map((v) => Number(v))
      .filter((n) => Number.isFinite(n) && n > 0).map((n) => Math.floor(n)),
  )].sort((a, b) => a - b);
}
const pointMilestones = parseMilestones(input.watchPointMilestones, '25,50,100,250,500,1000,2500,5000');
const commentMilestones = parseMilestones(input.watchCommentMilestones, '25,50,100,250,500,1000');
const enrichGithubLinks = input.enrichGithubLinks === true;
const excludeKeywords = [...new Set((input.excludeKeywords ?? []).map((k) => String(k).trim().toLowerCase()).filter((k) => k.length))];
const domainFilter = [...new Set((input.domainFilter ?? []).map((d) => String(d).trim().toLowerCase().replace(/^https?:\/\//, '').replace(/^www\./, '').replace(/\/.*$/, '')).filter((d) => d.length))];
const maxCommentDepth = input.maxCommentDepth ? Math.max(1, Math.floor(Number(input.maxCommentDepth))) : null;
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

if (!queries.length) queries.push(''); // empty query = browse by tag/date (e.g. front page, Ask HN, Who's Hiring)

const cm = Actor.getChargingManager();
const isPPE = cm.getPricingInfo().isPayPerEvent;
let pushed = 0;
// Hits read off Algolia this run (including ones watch mode drops before charging) -- the
// webhook's "how much did we look at" number, distinct from `pushed` ("how much did you pay for").
let scanned = 0;

// Watch mode: a stateful "only what is new since my last run" filter over the query/tag
// search, distinct from a plain search which returns the same matches every time. The
// baseline (objectIDs already delivered under this label+filter set) lives in a NAMED
// key-value store on the buyer's own account so it survives across runs -- the default KV
// store is per-run and would reset every time. Scoped to queries/tags only: 'usernames'
// profile lookups are a snapshot, not a discrete new item, so they run/charge normally
// regardless of watch mode (see the usage note below).
const WATCH_STORE = 'fetchsmith-hn-watch';
// Algolia's HN index is `paginationLimitedTo` 1000: past hit 1000 the API returns 200 with an
// EMPTY hits array and a `message` explaining the cap, and `nbPages` is already clamped to
// 1000/hitsPerPage so the page loop just ends. `nbHits` is NOT that cap -- it is the true match
// count (query "ai" declares 1,971,890 against a 1,000-hit window, measured cycle 643). Any cap
// above this is a number no run can ever reach, which is how SEED_CAP=5000 turned into an
// unfirable warning below (same bug class as the app-store WATCH_SCAN_CAP, h264).
const ALGOLIA_MAX_HITS = 1000;
const SEED_CAP = 5000; // bound the cost of a baseline run ACROSS queries (per query, ALGOLIA_MAX_HITS binds first)
// /search (relevance ranking, the "sortBy":"relevance" default) only computes an EXHAUSTIVE
// nbHits when a text query anchors the ranking. For tag-only browsing -- the documented "leave
// queries empty to browse by tag/date only" pattern -- on a large-volume tag it silently falls
// back to an approximate estimate that overshoots the true count by 3-12x (verified live, cycle
// 823: tags=ask_hn declared 2,262,034 vs the real 179,272 [12.6x]; tags=show_hn 1,941,371 vs
// 544,193 [3.6x]; story/comment similarly inflated; small tags like job/poll/front_page stay
// exact). /search_by_date's nbHits for the same tags/filters is always the accurate one
// (cross-checked against the corpus total). So when this run is on /search with no text query,
// re-derive declaredMatches from search_by_date instead of trusting the possibly-inflated number.
async function accurateNbHits(wantTags, filters) {
  const url = new URL('https://hn.algolia.com/api/v1/search_by_date');
  if (wantTags) url.searchParams.set('tags', wantTags);
  if (filters.length) url.searchParams.set('numericFilters', filters.join(','));
  url.searchParams.set('hitsPerPage', '0');
  try {
    const res = await gotScraping({ url: url.toString(), timeout: { request: 30000 }, retry: { limit: 2 }, responseType: 'json' });
    return typeof res.body.nbHits === 'number' ? res.body.nbHits : null;
  } catch {
    return null; // best-effort correction only; caller falls back to the original (possibly inflated) count
  }
}
const WATCH_KEEP = 20000; // bound the record size; oldest ids fall off first
// Set inside saveWatchRecord() when the WATCH_KEEP slice above actually drops ids -- distinct
// from `truncatedSummaries` (an Algolia SCAN that stopped short this run). This is the RECORD
// itself losing already-charged ids: on the next run they look "new" again and get charged a
// second time (h285, the same defect found across the rest of the fleet's watch-mode Actors).
let baselineTruncated = 0;
let baselineTruncatedTotal = 0;

function watchKeyFor(label, criteria) {
  const safe = label.toLowerCase().replace(/[^a-z0-9_.-]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 40) || 'default';
  const fp = createHash('sha1').update(JSON.stringify(criteria, Object.keys(criteria).sort())).digest('hex').slice(0, 10);
  return { key: `watch-${safe}-${fp}`, fingerprint: fp };
}

const watchMode = watchLabel.length > 0;
if (watchChanges && !watchMode) {
  log.warning('watchChanges is on but no watchLabel is set — it only applies to watch mode and does nothing here. Set a watchLabel to use it.');
} else if (watchChanges && !pointMilestones.length && !commentMilestones.length) {
  log.warning('watchChanges is on but BOTH milestone ladders are empty, so nothing can ever re-fire. Set watchPointMilestones and/or watchCommentMilestones (comma-separated numbers) or turn watchChanges off.');
}
let watchStore = null;
let watchKey = null;
let watchRecord = null;
let seeding = false;
let watchSkipped = 0;
let watchChangedCount = 0;
// objectID -> engagement snapshot `{ p: points, c: numComments }` at the moment we last SAW it
// (not last delivered it -- see pushResult). An entry with no `p` key means "seen but never
// captured": that is how pre-0.1.x flat-string baselines decode, and it deliberately never fires a
// milestone, because "we don't know where it was" cannot be distinguished from "it was at 0" and
// guessing 0 would re-charge for every already-popular story the day this option shipped. Key
// PRESENCE, not a null value, is the marker -- `p: null` is the real, legitimate snapshot of a
// comment hit (Algolia attaches no points to comments), same trap court-records-scraper hit with
// `dateTerminated: null` on an open docket.
const watchSeen = new Map();

function snapshotOf(item) {
  return { p: item.points ?? null, c: item.numComments ?? null };
}

// Highest ladder rung strictly above where we last saw the item and at or below where it is now,
// or null if it hasn't cleared a new rung. Returning only the HIGHEST means a story that jumps
// 10 -> 600 points in one run fires once (at 500), not four times.
function crossedMilestone(prevVal, nextVal, ladder) {
  if (!ladder.length || nextVal == null) return null;
  const base = prevVal ?? 0;
  if (nextVal <= base) return null;
  let crossed = null;
  for (const m of ladder) if (m > base && m <= nextVal) crossed = m;
  return crossed;
}

// A re-delivered item carries exactly what moved and which rung it cleared, so a buyer doesn't
// have to diff the row against their own last-seen copy to find out why they were charged.
function changesBetween(prev, next) {
  if (!prev || !Object.hasOwn(prev, 'p')) return null;
  const types = [];
  const previous = {};
  const milestone = {};
  const p = crossedMilestone(prev.p, next.p, pointMilestones);
  if (p != null) { types.push('pointsMilestone'); previous.points = prev.p; milestone.points = p; }
  const c = crossedMilestone(prev.c, next.c, commentMilestones);
  if (c != null) { types.push('commentsMilestone'); previous.numComments = prev.c; milestone.numComments = c; }
  return types.length ? { types, previous, milestone } : null;
}

if (watchMode) {
  const criteria = { queries, tags, sortBy, author, includeComments, numericFilters };
  if (excludeKeywords.length) criteria.excludeKeywords = excludeKeywords;
  if (domainFilter.length) criteria.domainFilter = domainFilter;
  watchStore = await Actor.openKeyValueStore(WATCH_STORE);
  const { key, fingerprint } = watchKeyFor(watchLabel, criteria);
  watchKey = key;
  const existing = await watchStore.getValue(key);
  if (existing && Array.isArray(existing.seenIds)) {
    watchRecord = existing;
    // Entries are `{ i, p, c }` objects from 0.1.x on; a baseline seeded before that is a flat
    // array of id strings, decoded here to the no-snapshot marker so an existing buyer's watch
    // keeps working unchanged instead of needing a fresh seed. Those ids resync to a real snapshot
    // the first incremental run that touches them, so the blind spot is one run wide per id.
    for (const entry of existing.seenIds) {
      if (entry && typeof entry === 'object') {
        watchSeen.set(String(entry.i), Object.hasOwn(entry, 'p') ? { p: entry.p, c: entry.c ?? null } : {});
      } else {
        watchSeen.set(String(entry), {});
      }
    }
    log.info(
      `Watch mode "${watchLabel}" (${key}): baseline from ${existing.lastRunAt ?? 'an earlier run'} holds `
      + `${watchSeen.size} already-delivered item(s). Only items NOT in that baseline will be returned and charged`
      + (watchChanges
        ? `, plus any already-delivered item that crossed a points milestone (${pointMilestones.join('/') || 'disabled'}) `
          + `or comment milestone (${commentMilestones.join('/') || 'disabled'}) since we last saw it.`
        : '.'),
    );
  } else {
    watchRecord = { fingerprint, firstSeededAt: new Date().toISOString(), runCount: 0 };
    seeding = true;
    log.info(
      `Watch mode "${watchLabel}" (${key}): FIRST run for this label and filter set, so this is a baseline `
      + 'run. It records which items already match and returns ZERO results (you are charged nothing). '
      + 'Run it again on the same label and filters -- on a schedule, typically -- to get only what is new since now.',
    );
  }
}

async function saveWatchRecord(status) {
  const ids = Array.from(watchSeen.entries()).slice(-WATCH_KEEP);
  baselineTruncated = watchSeen.size - ids.length;
  baselineTruncatedTotal = (watchRecord.truncatedTotal ?? 0) + baselineTruncated;
  if (baselineTruncated > 0) {
    log.warning(
      `Watch label "${watchLabel}": the baseline record hit its ${WATCH_KEEP}-id cap and dropped `
      + `${baselineTruncated} of the oldest already-delivered id(s) this run (${baselineTruncatedTotal} total `
      + 'across all runs). Those ids are no longer in the baseline, so the NEXT run will return AND CHARGE FOR '
      + 'them again as if they were new. Narrow the query/tags (tighter keywords, a postedAfter window, or a '
      + 'higher minPoints/minComments) to keep the baseline under the cap, or split this watch across more '
      + 'specific labels.',
    );
  }
  await watchStore.setValue(watchKey, {
    ...watchRecord,
    label: watchLabel,
    lastRunAt: new Date().toISOString(),
    lastRunStatus: status,
    runCount: (watchRecord.runCount ?? 0) + 1,
    seenCount: ids.length,
    // An id whose snapshot was never captured is written back WITHOUT `p`/`c` keys rather than
    // with nulls -- that omission is the "unknown" marker changesBetween() checks for, and a null
    // would read as a real "was at no points" reading and mis-fire a milestone.
    seenIds: ids.map(([id, snap]) => (Object.hasOwn(snap, 'p') ? { i: id, p: snap.p, c: snap.c } : { i: id })),
    truncatedLastRun: baselineTruncated,
    truncatedTotal: baselineTruncatedTotal,
  });
}

// Appended to the seeding/incremental log lines AFTER saveWatchRecord() has run (it sets the
// two module-scope counters above) -- computing it before that call would read stale zeros.
function evictionNote() {
  if (!baselineTruncated) return '';
  return ` NOTE: the baseline record dropped ${baselineTruncated} of the oldest already-delivered id(s) this run `
    + `(${baselineTruncatedTotal} total) to stay under its ${WATCH_KEEP}-id cap -- those will be treated as new `
    + 'and CHARGED FOR again next run unless you narrow the query/tags. See the RUN_SUMMARY key-value record.';
}

// True when an already-delivered item is about to be re-delivered because it cleared a milestone.
// Read BEFORE pushResult() by the GitHub-enrichment gate, which has to decide whether the row is
// worth spending a lookup on; pushResult() re-derives it rather than trusting a passed-in flag.
function isMilestoneRedelivery(watchId, item) {
  if (!watchMode || !watchChanges || seeding || watchId == null) return false;
  const wid = String(watchId);
  return watchSeen.has(wid) && changesBetween(watchSeen.get(wid), snapshotOf(item)) != null;
}

async function pushResult(item, watchId) {
  const wid = watchId == null ? null : String(watchId);
  if (watchMode && wid != null && seeding) {
    watchSeen.set(wid, snapshotOf(item));
    return watchSeen.size < SEED_CAP;
  }
  let change = null;
  if (watchMode && wid != null && watchSeen.has(wid)) {
    const nextSnap = snapshotOf(item);
    change = watchChanges ? changesBetween(watchSeen.get(wid), nextSnap) : null;
    if (!change) {
      // Snapshot kept current even with watchChanges off, so turning it on later alerts on drift
      // from that point rather than dumping every milestone crossed since the baseline was seeded.
      // This is also what stops a climbing story from re-firing: the base moves up every run it is
      // scanned, so only a genuinely new rung can ever clear it.
      watchSeen.set(wid, nextSnap);
      watchSkipped += 1;
      return true;
    }
    item = { ...item, _watchChangeType: change.types, _watchPrevious: change.previous, _watchMilestone: change.milestone };
  }
  if (isPPE) {
    const r = await Actor.charge({ eventName: 'result', count: 1 });
    // Not charged => not delivered => snapshot deliberately NOT advanced, so the milestone is
    // still pending and fires on the next run instead of being silently consumed by a charge cap.
    if (r.chargedCount === 0) return false;
    await Actor.pushData(item); pushed += 1;
    if (watchMode && wid != null) watchSeen.set(wid, snapshotOf(item));
    if (change) watchChangedCount += 1;
    return !r.eventChargeLimitReached && pushed < maxResults;
  }
  await Actor.pushData(item); pushed += 1;
  if (watchMode && wid != null) watchSeen.set(wid, snapshotOf(item));
  if (change) watchChangedCount += 1;
  return pushed < maxResults;
}

// A transparent, documented engagement score (points + weighted comment count) for
// sorting/filtering results within a batch. Deliberately NOT decayed by age: an
// age-decayed "HN front-page style" score collapses to ~0 for anything older than a
// few days, which would make it useless on the common case (relevance/all-time search,
// or `sortBy:"date"` results spanning years) — the exact case most queries return.
// null for comments, which the Algolia index never attaches points/num_comments to.
function engagementScore(points, numComments) {
  if (points == null) return null;
  return Math.round((points + (numComments ?? 0) * 0.5) * 10) / 10;
}

function mapHit(hit) {
  const isComment = (hit._tags || []).includes('comment');
  const storyId = hit.story_id ?? hit.objectID;
  const points = hit.points ?? null;
  const numComments = hit.num_comments ?? null;
  const createdAt = hit.created_at || null;
  return {
    id: hit.objectID,
    type: isComment ? 'comment' : (hit._tags || []).find((t) => ['story', 'job', 'poll', 'ask_hn', 'show_hn'].includes(t)) || 'story',
    title: hit.title || hit.story_title || null,
    url: hit.url || (isComment ? null : `https://news.ycombinator.com/item?id=${hit.objectID}`) || hit.story_url || null,
    hnUrl: `https://news.ycombinator.com/item?id=${hit.objectID}`,
    author: hit.author || null,
    points,
    numComments,
    engagementScore: engagementScore(points, numComments),
    storyId: storyId ?? null,
    storyTitle: hit.story_title || null,
    storyUrl: hit.story_url || null,
    parentId: isComment ? (hit.parent_id ?? null) : null,
    commentDepth: null,
    text: hit.comment_text || hit.story_text || null,
    createdAt,
    query: hit._query ?? null,
    karma: null,
    about: null,
    accountCreatedAt: null,
    githubRepo: null,
    githubStars: null,
    githubLanguage: null,
    githubPushedAt: null,
    githubOpenIssues: null,
  };
}

// Matches a GitHub repo reference (owner/repo) out of a URL or free text, skipping
// GitHub's own non-repo paths (github.com/sponsors/x, /marketplace/x, etc. are not repos).
const GITHUB_REPO_RE = /github\.com\/([A-Za-z0-9](?:[A-Za-z0-9-]){0,38})\/([A-Za-z0-9_.-]+?)(?=[/?#\s"'.)]|$)/i;
const GITHUB_NON_REPO_OWNERS = new Set([
  'sponsors', 'marketplace', 'topics', 'search', 'orgs', 'settings', 'apps', 'features', 'about', 'pricing',
  'blog', 'security', 'enterprise', 'readme', 'collections', 'events', 'login', 'logout', 'join', 'contact',
  'customer-stories', 'dashboard', 'explore', 'gist', 'home', 'issues', 'new', 'notifications', 'org',
  'pages', 'personal', 'plans', 'press', 'pulls', 'site', 'stars', 'trending', 'watching', 'account',
]);
const githubCache = new Map(); // ownerRepo -> enrichment fields, or null once known-missing (avoid refetching the same repo twice in one run)
const GITHUB_LOOKUP_CAP = 200; // bound cost against GitHub's unauthenticated 60/hr rate limit
let githubLookups = 0;
let githubRateLimited = false;

function extractGithubRepo(item) {
  for (const haystack of [item.url, item.storyUrl, item.text, item.title]) {
    if (!haystack) continue;
    const m = GITHUB_REPO_RE.exec(haystack);
    if (m && !GITHUB_NON_REPO_OWNERS.has(m[1].toLowerCase())) {
      return `${m[1]}/${m[2].replace(/\.git$/i, '')}`;
    }
  }
  return null;
}

async function enrichGithub(item) {
  const repoFullName = extractGithubRepo(item);
  if (!repoFullName) return;
  item.githubRepo = repoFullName;
  if (githubCache.has(repoFullName)) {
    Object.assign(item, githubCache.get(repoFullName) || {});
    return;
  }
  if (githubRateLimited || githubLookups >= GITHUB_LOOKUP_CAP) return;
  githubLookups += 1;
  try {
    const res = await gotScraping({
      url: `https://api.github.com/repos/${repoFullName}`,
      timeout: { request: 15000 },
      retry: { limit: 0 },
      responseType: 'json',
      headers: { 'User-Agent': 'fetchsmith-hacker-news-scraper' },
      throwHttpErrors: false,
    });
    // got-scraping defaults to throwHttpErrors:false (verified live 2026-09-24), so GitHub's
    // 403/429/404 all arrive here as ordinary resolved responses. Until cycle 752 the status was
    // read off `e.response` in the catch below, which could never run: a 404 fell through to the
    // mapping and wrote four null enrichment columns instead of the "do not retry" sentinel, and
    // a rate limit never set `githubRateLimited`, so the run kept spending its lookup budget on
    // calls that could only return nulls. Read the status off the response instead.
    const status = res.statusCode;
    if (status === 403 || status === 429) {
      githubRateLimited = true;
      log.warning('GitHub API rate limit reached -- remaining items in this run keep githubRepo but not star/language/pushed-at data.');
      return;
    }
    if (status === 404) {
      githubCache.set(repoFullName, null); // repo renamed/deleted/private -- do not retry
      return;
    }
    const d = res.body;
    if (status !== 200 || !d || typeof d !== 'object') {
      log.warning(`GitHub lookup failed for ${repoFullName}: HTTP ${status}.`);
      return;
    }
    const fields = {
      githubStars: d.stargazers_count ?? null,
      githubLanguage: d.language ?? null,
      githubPushedAt: d.pushed_at ?? null,
      githubOpenIssues: d.open_issues_count ?? null,
    };
    githubCache.set(repoFullName, fields);
    Object.assign(item, fields);
  } catch (e) {
    // Only a genuine transport failure (DNS/TLS/timeout) reaches this now.
    log.warning(`GitHub lookup failed for ${repoFullName}: ${e.message}`);
  }
}

// Algolia's search hits carry `parent_id` (the comment's immediate parent) but never a depth --
// to know "how many replies deep is this" we have to walk the parent chain up to the story one
// hop at a time via the Items API, since nothing in the search index states it directly.
// Memoized across the whole run: `depthCache` maps an item id -> its depth once known, so two
// comments in the same thread only pay for the hops that are not already resolved by an earlier
// one (a comment-heavy run on one popular story converges to near-zero extra lookups after the
// first few comments from it).
const depthCache = new Map(); // id -> depth (1 = direct reply to the story), or id -> storyId sentinel never stored
const DEPTH_LOOKUP_CAP = 300; // bound added latency/requests the same way GITHUB_LOOKUP_CAP bounds GitHub calls
const DEPTH_WALK_CAP = 60; // HN threads do not nest this deep in practice; guards against an unexpected cycle/bug
let depthLookups = 0;
let depthLookupCapped = false;

async function fetchParentId(id) {
  const res = await gotScraping({
    url: `https://hn.algolia.com/api/v1/items/${id}`,
    timeout: { request: 15000 },
    retry: { limit: 1 },
    responseType: 'json',
  });
  return res.body?.parent_id ?? null;
}

// Returns the comment's depth (1 = direct reply to the story) or null if it could not be
// determined (lookup failure or DEPTH_LOOKUP_CAP/DEPTH_WALK_CAP reached) -- callers treat null as
// "unknown, do not filter it out" rather than dropping data because OUR lookup failed.
async function computeCommentDepth(objectId, parentId, storyId) {
  if (depthCache.has(objectId)) return depthCache.get(objectId);
  const chain = [objectId];
  let cur = parentId;
  while (cur != null && cur !== storyId && !depthCache.has(cur)) {
    if (chain.length >= DEPTH_WALK_CAP) return null;
    if (depthLookups >= DEPTH_LOOKUP_CAP) {
      if (!depthLookupCapped) { depthLookupCapped = true; log.warning(`Reached the ${DEPTH_LOOKUP_CAP}-lookup cap for comment-depth resolution -- remaining comments this run keep commentDepth:null and are not filtered by maxCommentDepth.`); }
      return null;
    }
    chain.push(cur);
    depthLookups += 1;
    try {
      cur = await fetchParentId(cur);
    } catch (e) {
      log.warning(`Comment-depth lookup failed for item ${cur}: ${e.message} -- leaving commentDepth null for this comment.`);
      return null;
    }
  }
  const base = depthCache.has(cur) ? depthCache.get(cur) : 0; // cur === storyId, or null/unresolved ancestor -- either way treat as story-level
  for (let i = chain.length - 1; i >= 0; i -= 1) depthCache.set(chain[i], base + (chain.length - i));
  return depthCache.get(objectId);
}

function mapUser(username, data) {
  return {
    id: data.id ?? username,
    type: 'user',
    title: null,
    url: null,
    hnUrl: `https://news.ycombinator.com/user?id=${encodeURIComponent(username)}`,
    author: data.id ?? username,
    points: null,
    numComments: null,
    storyId: null,
    storyTitle: null,
    storyUrl: null,
    parentId: null,
    commentDepth: null,
    text: null,
    createdAt: null,
    query: null,
    karma: data.karma ?? null,
    about: data.about ?? null,
    accountCreatedAt: data.created ? new Date(data.created * 1000).toISOString() : null,
    githubRepo: null,
    githubStars: null,
    githubLanguage: null,
    githubPushedAt: null,
    githubOpenIssues: null,
  };
}

// Algolia's `query` param ranks by relevance, it has no negative-term syntax, so a buyer who
// wants "rust but not cryptocurrency" has no way to express that server-side. Both `title` and
// `text` are already mapped fields (mapHit), so this is the same zero-cost "filter what we
// already fetched" pattern as the shaped-field filters on shopify-products-scraper.
function excludedByKeyword(mapped) {
  if (!excludeKeywords.length) return false;
  const haystack = `${mapped.title || ''} ${mapped.text || ''}`.toLowerCase();
  return excludeKeywords.some((k) => haystack.includes(k));
}

// A comment has no URL of its own in Algolia's data (mapHit leaves `url` null for comments), so
// it is matched on its PARENT STORY's `storyUrl` instead -- the same "comment inherits the
// story's shape" choice enrichGithub() already makes for repo links.
function hostnameOf(urlStr) {
  if (!urlStr) return null;
  try { return new URL(urlStr).hostname.toLowerCase().replace(/^www\./, ''); } catch { return null; }
}
function matchesDomainFilter(mapped) {
  if (!domainFilter.length) return true;
  const host = hostnameOf(mapped.url) || hostnameOf(mapped.storyUrl);
  if (!host) return false; // no resolvable URL (text-only Ask HN post, job) -- can't match a domain, so drop it
  return domainFilter.some((d) => host === d || host.endsWith(`.${d}`));
}

const emptyQueries = []; // Algolia matched nothing for this query/tags/filters combo
const erroredQueries = []; // the HTTP request itself failed
const seenIds = new Set(); // dedup across queries — overlapping/duplicate queries return the same objectID from Algolia
let duplicates = 0;
let excluded = 0;
let domainFiltered = 0;
let commentDepthFiltered = 0;
let keepGoing = true;
// One record per query, written to the RUN_SUMMARY key-value record and posted on the webhook.
// The DATASET is the only surface a pipeline reads, and there a full 100 rows for a query
// declaring 60,108 matches is indistinguishable from the complete match set -- the log and the
// status message say so in prose, i.e. in English, which no program can read (h250/h271 class).
const summaries = [];
// `notReached`: the run stopped (maxResults or the PPE charge limit) before this query was ever
// searched. Written down explicitly, because otherwise its ABSENCE from the summary reads as
// "nothing matched there" rather than "we never looked" (cycle 642 lesson).
const summaryFor = (query) => ({
  query: query || null,
  declaredMatches: null, // Algolia nbHits: the true match count, independent of the 1000-hit window
  scanned: 0,
  delivered: 0,
  filteredOut: 0,
  status: 'notReached',
  complete: false,
  incompleteReason: null,
  hitPaginationCeiling: false,
  scanCap: null,
});
for (const query of queries) {
  const querySummary = summaryFor(query);
  summaries.push(querySummary);
  if (!keepGoing || timeBudgetExceeded) continue; // keep walking so every unsearched query gets a `notReached` record
  let page = 0;
  let fetched = 0;
  let requestFailed = false;
  const deliveredBefore = pushed;
  const filteredBefore = excluded + duplicates + domainFiltered + commentDepthFiltered;
  // Algolia's tag syntax: a COMMA between tags means AND, parentheses mean OR. `tags` is a
  // multi-select of content types, and the combinations a buyer actually picks are mutually
  // exclusive — comma-joining them matched NOTHING, forever, with a 200 and no warning
  // (verified live, cycle 360: tags=story,comment -> nbHits 0, tags=ask_hn,show_hn -> 0;
  // tags=(story,comment) -> 545,027). So OR the content-type tags with each other, and AND
  // the author refinement on top of that group: `author_pg,(story,comment)`.
  // `includeComments:false` drops 'comment' HERE, before the group is built — the old code
  // stripped it out of the joined string afterwards, which for tags:["comment"] left an empty
  // `tags=` (i.e. no tag filter at all) instead of no query at all.
  const typeTags = (includeComments ? tags : tags.filter((t) => t !== 'comment')).filter(Boolean);
  const tagParts = [];
  if (author) tagParts.push(`author_${author}`);
  if (typeTags.length) tagParts.push(typeTags.length > 1 ? `(${typeTags.join(',')})` : typeTags[0]);
  const wantTags = tagParts.length ? tagParts.join(',') : undefined;
  // Second half of the condition: every tag the buyer asked for was dropped (they asked for
  // "comment" only and then set includeComments:false). Widening that to "search every content
  // type" is the expensive wrong answer — it charges per result for rows they did not ask for —
  // so skip the iteration and say why instead.
  if ((!query && !wantTags) || (tags.length && !typeTags.length)) {
    // No query and no tags means Algolia's search endpoint matches its entire ~46M-item
    // history ranked by relevance — a silent runaway bill, not a legitimate "browse" request.
    log.warning(
      tags.length && !typeTags.length
        ? 'Only tag "comment" was requested but includeComments is false, so every requested tag was '
          + 'dropped and there is nothing left to search for — skipping this iteration rather than '
          + 'silently returning (and charging for) every other content type. '
          + 'Set includeComments:true, or add another tag such as "story".'
        : 'No query and no tags for this iteration — skipping (set tags, e.g. ["story"], or a search query; use "usernames" alone for user-profile-only runs).',
    );
    emptyQueries.push(query || '<empty>');
    querySummary.status = 'skipped';
    querySummary.incompleteReason = tags.length && !typeTags.length ? 'all-tags-dropped' : 'no-query-and-no-tags';
    continue;
  }
  // A seeding run needs the whole current match set (up to SEED_CAP), not just the
  // buyer's usual maxItemsPerQuery slice, or the baseline would under-record and the
  // first incremental run would misreport old matches as new. An incremental run needs
  // the same reach, not just the seed: in watch mode almost everything scanned is
  // already-delivered, so capping the scan at maxItemsPerQuery (default 100, a per-query
  // COST cap for plain runs) means a query with more than 100 matches only ever surfaces
  // a new item if it happens to sort within the first 100 -- a silent, permanent miss
  // that still looks like a clean "nothing new" run (the ats-jobs-scraper trap, cycle 332).
  // maxItemsPerQuery only means "cost cap" when there's no baseline to scan past; once
  // watchLabel is set, seeding or not, the scan cap is SEED_CAP and maxResults alone
  // governs what's actually delivered and charged.
  const queryCap = Math.min(watchMode ? SEED_CAP : maxItemsPerQuery, ALGOLIA_MAX_HITS);
  querySummary.scanCap = queryCap;
  while (keepGoing && !timeBudgetExceeded && fetched < queryCap) {
    if (!timeBudgetOk()) { log.warning('Approaching the run timeout — stopping early and returning what has been collected so far.'); break; }
    const url = new URL(`https://hn.algolia.com/api/v1/${sortBy}`);
    if (query) url.searchParams.set('query', query);
    if (wantTags) url.searchParams.set('tags', wantTags);
    if (numericFilters.length) url.searchParams.set('numericFilters', numericFilters.join(','));
    url.searchParams.set('hitsPerPage', String(Math.min(100, queryCap - fetched)));
    url.searchParams.set('page', String(page));
    log.info(`Fetching: ${url.toString()}`);
    let body;
    let lastErr;
    // got's own `retry` only fires for a fixed errorCodes list that does not include the
    // connection-establishment faults (ERR_HTTP2_ERROR / HPE_INVALID_CONSTANT) measured live on
    // this same got-scraping version in cycle 616 — about 1 in 4 fresh connections. Without an
    // outer retry, one blip drops the rest of this query's pages, distinguishable from
    // "genuinely 0 hits" only by the erroredQueries note. Retry a handful of times before giving up.
    for (let attempt = 1; attempt <= 3; attempt += 1) {
      try {
        const res = await gotScraping({ url: url.toString(), timeout: { request: 30000 }, retry: { limit: 2 }, responseType: 'json' });
        body = res.body;
        lastErr = null;
        break;
      } catch (e) {
        lastErr = e;
        if (attempt < 3) {
          log.warning(`Query failed (${query || '<none>'}, page ${page}), attempt ${attempt}/3: ${e.message} — retrying.`);
          await new Promise((r) => setTimeout(r, attempt * 1000));
        }
      }
    }
    if (lastErr) {
      log.warning(`Query failed (${query || '<none>'}, page ${page}) after 3 attempts: ${lastErr.message}`);
      requestFailed = true;
      break;
    }
    // Read nbHits from page 0 only: it is the same number on every page, and past the
    // 1000-hit window Algolia answers with an empty-hits page whose nbHits is the exhaustive
    // recount (exhaustiveNbHits flips true) -- overwriting the real figure with it would
    // understate exactly the shortfall this record exists to report.
    if (page === 0 && typeof body.nbHits === 'number') {
      querySummary.declaredMatches = (sortBy === 'search' && !query)
        ? (await accurateNbHits(wantTags, numericFilters)) ?? body.nbHits
        : body.nbHits;
    }
    const hits = body.hits || [];
    if (!hits.length) {
      // 200 + zero hits at a page we asked for past hit 1000 is Algolia's pagination cap, not
      // the end of the match set; it carries an explanatory `message` the plain end-of-results
      // response does not have.
      if (fetched >= ALGOLIA_MAX_HITS || body.message) querySummary.hitPaginationCeiling = true;
      break;
    }
    for (const hit of hits) {
      fetched += 1;
      scanned += 1;
      if (seenIds.has(hit.objectID)) { duplicates += 1; continue; }
      seenIds.add(hit.objectID);
      hit._query = query || null;
      const mapped = mapHit(hit);
      if (excludedByKeyword(mapped)) { excluded += 1; continue; }
      if (!matchesDomainFilter(mapped)) { domainFiltered += 1; continue; }
      // Skip the GitHub lookup for rows that pushResult will drop uncharged anyway
      // (seeding baseline, or already delivered under this watch label) -- those never
      // reach the buyer, so spending part of GitHub's 60/hr unauthenticated budget on them
      // would only starve the rows that actually get returned.
      const willDeliver = !(watchMode && (seeding || watchSeen.has(String(hit.objectID))))
        || isMilestoneRedelivery(hit.objectID, mapped);
      if (enrichGithubLinks && willDeliver) {
        if (!timeBudgetOk()) { log.warning('Approaching the run timeout — stopping early and returning what has been collected so far.'); break; }
        await enrichGithub(mapped);
      }
      // Same willDeliver gate as GitHub enrichment above, for the same reason: the parent-chain
      // walk costs one request per not-yet-cached ancestor, so skip it for rows pushResult would
      // drop uncharged anyway. Unlike GitHub enrichment this one can also DROP the row (depth
      // too deep) -- which is exactly right here, since a row we would skip computing depth for
      // was never going to be charged either way.
      if (mapped.type === 'comment' && maxCommentDepth != null && willDeliver) {
        if (!timeBudgetOk()) { log.warning('Approaching the run timeout — stopping early and returning what has been collected so far.'); break; }
        mapped.commentDepth = await computeCommentDepth(hit.objectID, mapped.parentId, mapped.storyId);
        if (mapped.commentDepth != null && mapped.commentDepth > maxCommentDepth) { commentDepthFiltered += 1; continue; }
      }
      keepGoing = await pushResult(mapped, hit.objectID);
      if (!keepGoing) break;
    }
    page += 1;
    // nbPages is already clamped to the 1000-hit window, so running out of pages while the
    // index declares more matches than we scanned IS the ceiling, not the end of the results.
    if (page >= (body.nbPages ?? 1)) {
      if (fetched >= ALGOLIA_MAX_HITS && (querySummary.declaredMatches ?? 0) > fetched) querySummary.hitPaginationCeiling = true;
      break;
    }
  }
  querySummary.scanned = fetched;
  querySummary.delivered = pushed - deliveredBefore;
  querySummary.filteredOut = (excluded + duplicates + domainFiltered + commentDepthFiltered) - filteredBefore;
  if (requestFailed) {
    erroredQueries.push(query || '<empty>');
    querySummary.status = 'error';
    querySummary.incompleteReason = 'request-failed';
  } else if (fetched === 0) {
    emptyQueries.push(query || '<empty>');
    querySummary.status = 'empty';
    querySummary.complete = true; // nothing matched, and that is the whole truth about this query
  } else {
    querySummary.status = querySummary.delivered === 0 ? 'filteredOut' : 'ok';
    // `complete` is deliberately NOT folded into `status`: a query can be `ok` and truncated at
    // the same time, which is the exact case this record exists to expose (cycle 642 lesson).
    const declared = querySummary.declaredMatches;
    if (querySummary.hitPaginationCeiling) querySummary.incompleteReason = 'algolia-pagination-ceiling';
    else if (fetched >= queryCap && (declared == null || declared > fetched)) querySummary.incompleteReason = watchMode ? 'seed-cap' : 'max-items-per-query';
    else if (timeBudgetExceeded) querySummary.incompleteReason = 'time-budget';
    else if (!keepGoing) querySummary.incompleteReason = pushed >= maxResults ? 'max-results' : 'charge-limit';
    else if (declared != null && declared > fetched) querySummary.incompleteReason = 'scan-short-of-declared';
    querySummary.complete = querySummary.incompleteReason == null;
  }
}
// Truncated queries in a baseline run are the expensive case: the un-scanned tail is NOT in the
// baseline, so the next incremental run sees those items for the first time and DELIVERS AND
// CHARGES pre-existing matches as "new" (h264, in the app-store Actor, was this same bug).
const truncatedSummaries = summaries.filter((s) => s.status !== 'notReached' && s.incompleteReason != null);
const notReachedSummaries = summaries.filter((s) => s.status === 'notReached');

const notFoundUsers = [];
const erroredUsers = [];
const notReachedUsers = []; // the run stopped before we looked these up -- say so, don't just omit them
for (const username of usernames) {
  if (!keepGoing || !timeBudgetOk()) { notReachedUsers.push(username); continue; }
  let data;
  try {
    const res = await gotScraping({
      url: `https://hacker-news.firebaseio.com/v0/user/${encodeURIComponent(username)}.json`,
      timeout: { request: 30000 },
      retry: { limit: 2 },
      responseType: 'json',
    });
    data = res.body;
  } catch (e) {
    log.warning(`User lookup failed (${username}): ${e.message}`);
    erroredUsers.push(username);
    continue;
  }
  if (!data) {
    log.warning(`No such HN user: ${username}`);
    notFoundUsers.push(username);
    continue;
  }
  keepGoing = await pushResult(mapUser(username, data));
}

// A seed walk that never got an answer from Algolia for one query is not a smaller baseline, it
// is a WRONG one: every hit past the failure point would read as "new" (and be charged) on the
// first incremental run. Structural truncation (seed-cap, algolia-pagination-ceiling, etc.) is
// deliberately excluded -- that is a capped-but-real baseline, already surfaced above, and still
// strictly better than none. Seeding never charges, so refusing to save costs nothing but a
// re-run.
const seedFailure = seeding && erroredQueries.length ? erroredQueries.join(', ') : null;

if (watchMode && seedFailure) {
  log.warning(
    `Baseline walk for watch label "${watchLabel}" was cut short (Algolia request(s) failed for: ${seedFailure}), `
    + 'so NO baseline was saved. Re-run with the same watchLabel to seed again once Algolia is answering -- saving '
    + 'a truncated baseline would make every item past the failure point look "new" (and billable) on the first '
    + 'incremental run.',
  );
} else if (watchMode) {
  await saveWatchRecord(seeding ? 'seeded' : 'incremental');
  if (seeding) {
    log.info(
      `Baseline saved for watch label "${watchLabel}": ${watchSeen.size} item(s) recorded as already-seen, `
      + '0 results returned, 0 charged. The next run on this label and these filters returns only new items.'
      // The old test here was `watchSeen.size >= SEED_CAP` (5000) -- unreachable, because Algolia
      // stops at 1000 hits per query, so the warning could never fire on the case it was written
      // for. Key it to the measured per-query truncation instead.
      + (truncatedSummaries.length
        ? ` WARNING: the baseline is INCOMPLETE for ${truncatedSummaries.length} of ${summaries.length} query/queries `
        + `(${truncatedSummaries.map((s) => `"${s.query ?? '<empty>'}" scanned ${s.scanned}`
          + `${s.declaredMatches != null ? ` of ${s.declaredMatches} declared matches` : ''} [${s.incompleteReason}]`).join('; ')}). `
        + 'Matches past that point are NOT in the baseline, so the first incremental run will return and CHARGE FOR '
        + 'them as if they were new. Narrow each query (tighter keywords, tags, or a postedAfter/minPoints threshold) '
        + `until its declared match count fits under ${ALGOLIA_MAX_HITS}, then re-seed with a fresh watchLabel.`
        : '')
      + evictionNote(),
    );
  } else {
    log.info(
      `Watch label "${watchLabel}": ${pushed - watchChangedCount} new item(s) since the last run`
      + (watchChanges ? ` and ${watchChangedCount} already-delivered item(s) re-charged for crossing a milestone` : '')
      + ` (${watchSkipped} already-delivered hit(s) skipped, not charged); baseline now holds ${watchSeen.size}.${evictionNote()}`,
    );
  }
}

log.info(`Done. Pushed ${pushed} items.${duplicates ? ` Skipped ${duplicates} duplicate hit(s) already returned by an earlier query (not charged).` : ''}${excluded ? ` Dropped ${excluded} hit(s) matching excludeKeywords (not charged).` : ''}${domainFiltered ? ` Dropped ${domainFiltered} hit(s) outside domainFilter (not charged).` : ''}${commentDepthFiltered ? ` Dropped ${commentDepthFiltered} comment(s) deeper than maxCommentDepth (not charged).` : ''}`);

for (const s of truncatedSummaries) {
  log.warning(
    `Query "${s.query ?? '<empty>'}" is INCOMPLETE: scanned ${s.scanned}`
    + `${s.declaredMatches != null ? ` of ${s.declaredMatches} match(es) Hacker News declares` : ''}`
    + `, delivered ${s.delivered} (${s.incompleteReason}).`
    + (s.hitPaginationCeiling
      ? ` Algolia's HN index never serves more than ${ALGOLIA_MAX_HITS} hits for one query, whatever maxItemsPerQuery says`
        + ' -- split the query by date window (postedAfter/postedBefore) or raise minPoints to get the rest.'
      : ''),
  );
}
if (notReachedSummaries.length || notReachedUsers.length) {
  log.warning(
    `The run stopped before ${notReachedSummaries.length} query/queries${notReachedUsers.length ? ` and ${notReachedUsers.length} username(s)` : ''} `
    + `were searched at all (${timeBudgetExceeded ? 'approaching the run timeout' : pushed >= maxResults ? `maxResults ${maxResults} reached` : 'charge limit reached'}): `
    + `${[...notReachedSummaries.map((s) => `"${s.query ?? '<empty>'}"`), ...notReachedUsers].join(', ')}. `
    + (timeBudgetExceeded ? 'Narrow the input (fewer queries, lower maxItemsPerQuery, or enrichGithubLinks:false) so the run finishes within the platform timeout, or run them separately.' : 'Raise maxResults (or the charge limit) to cover them, or run them separately.'),
  );
}

// A key-value record, not just a webhook field: it is readable with no webhook configured, via
// GET /v2/actor-runs/<runId>/key-value-store/records/RUN_SUMMARY.
await Actor.setValue('RUN_SUMMARY', {
  actorRunId: Actor.getEnv().actorRunId ?? null,
  finishedAt: new Date().toISOString(),
  pushed,
  scanned,
  maxResults,
  paginationCeiling: ALGOLIA_MAX_HITS,
  complete: truncatedSummaries.length === 0 && notReachedSummaries.length === 0 && notReachedUsers.length === 0,
  timeBudgetExceeded,
  queries: summaries,
  queriesIncomplete: truncatedSummaries.length,
  queriesNotReached: notReachedSummaries.length,
  usersNotReached: notReachedUsers,
  usersNotFound: notFoundUsers,
  usersErrored: erroredUsers,
  watchLabel: watchMode ? watchLabel : null,
  watchSeeding: watchMode ? seeding : null,
  watchChanges: watchMode ? watchChanges : null,
  watchChangedCount: watchMode && !seeding && watchChanges ? watchChangedCount : null,
  baselineTruncated: watchMode ? baselineTruncated : null,
  baselineTruncatedTotal: watchMode ? baselineTruncatedTotal : null,
});

// Fires after every row is already pushed and charged, so a slow or failing webhook can never
// affect the result set or the bill -- best-effort only, one attempt, short timeout, failures are
// a warning not a thrown error. Watch mode drops already-seen hits before they are charged, so
// `watchNewCount` counts only first-time items; `watchChangedCount` is the separate re-delivery
// count (already-seen items that cleared a milestone), and the two sum to `pushed`.
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
    watchNewCount: watchMode && !seeding ? pushed - watchChangedCount : null,
    watchChangedCount: watchMode && !seeding && watchChanges ? watchChangedCount : null,
    watchSkippedCount: watchMode && !seeding ? watchSkipped : null,
    baselineTruncated: watchMode ? baselineTruncated : null,
    baselineTruncatedTotal: watchMode ? baselineTruncatedTotal : null,
    complete: truncatedSummaries.length === 0 && notReachedSummaries.length === 0 && notReachedUsers.length === 0,
    queries: summaries,
    queriesIncomplete: truncatedSummaries.length,
    queriesNotReached: notReachedSummaries.length,
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

if (pushed === 0 && watchMode && !seeding) {
  await Actor.setStatusMessage(`Nothing new for watch label "${watchLabel}" since its last run -- every matching item had already been delivered. That is the expected result most of the time; you were charged for nothing.`);
} else if (pushed === 0 && seeding) {
  await Actor.setStatusMessage(`Baseline run for watch label "${watchLabel}": ${watchSeen.size} existing item(s) recorded, 0 charged. Run again later to get only what's new.`);
} else if (pushed === 0 && (queries.length || usernames.length)) {
  const reasons = [];
  if (erroredQueries.length) reasons.push(`the request to Algolia's HN Search API failed for: ${erroredQueries.join(', ')} (see log for the error)`);
  if (emptyQueries.length) {
    // job and comment hits carry points:null / num_comments:null in HN's own Algolia data (verified
    // live, varied_test cycle 967) -- no minPoints/minComments threshold, however low, ever matches
    // them, so the old generic "try a lower minPoints" advice was both wrong (there is no working
    // threshold) and silent about minComments even when that was the filter actually set.
    const numericDeadEnd = (input.minPoints || input.minComments) && tags.some((t) => t === 'job' || t === 'comment');
    let advice;
    if (numericDeadEnd) {
      const culprits = [input.minPoints ? 'minPoints' : null, input.minComments ? 'minComments' : null].filter(Boolean).join('/');
      advice = `job and comment items never have a points or comment count in HN's own data (both are always null), so ${culprits} can never match tags:["job"] or tags:["comment"] at any threshold — remove that filter or search tags:["story"] instead`;
    } else if (input.minPoints || input.minComments) {
      const culprits = [input.minPoints ? 'minPoints' : null, input.minComments ? 'minComments' : null].filter(Boolean).join('/');
      advice = `try different tags, a wider postedAfter/postedBefore range, or a lower ${culprits}`;
    } else {
      advice = 'try different tags or a wider postedAfter/postedBefore range';
    }
    reasons.push(`no stories/comments matched: ${emptyQueries.join(', ')} — ${advice}`);
  }
  if (excluded) reasons.push(`excludeKeywords (${excludeKeywords.join(', ')}) removed all ${excluded} otherwise-matching item(s)`);
  if (domainFiltered) reasons.push(`domainFilter (${domainFilter.join(', ')}) removed all ${domainFiltered} otherwise-matching item(s)`);
  if (commentDepthFiltered) reasons.push(`maxCommentDepth (${maxCommentDepth}) removed all ${commentDepthFiltered} otherwise-matching comment(s)`);
  if (erroredUsers.length) reasons.push(`the user lookup failed for: ${erroredUsers.join(', ')} (see log for the error)`);
  if (notFoundUsers.length) reasons.push(`no such HN user: ${notFoundUsers.join(', ')}`);
  if (timeBudgetExceeded) reasons.push('the run stopped early, approaching the platform run timeout, before any result could be delivered — narrow the input (fewer queries, lower maxItemsPerQuery, or enrichGithubLinks:false) and try again');
  await Actor.setStatusMessage(`No items returned — ${reasons.join('; ') || 'no queries or usernames provided'}.`);
} else if (emptyQueries.length || notFoundUsers.length || truncatedSummaries.length || notReachedSummaries.length || notReachedUsers.length) {
  // Until cycle 643 this branch fired ONLY on emptyQueries/notFoundUsers, so a run that
  // delivered a full 100 rows against 60,108 declared matches -- or that stopped at maxResults
  // and never searched half the queries -- ended with no status message at all, i.e. looking
  // exactly like a complete one.
  const notes = [];
  if (truncatedSummaries.length) {
    const worst = truncatedSummaries
      .filter((s) => s.declaredMatches != null)
      .sort((a, b) => (b.declaredMatches - b.scanned) - (a.declaredMatches - a.scanned))[0];
    notes.push(
      `${truncatedSummaries.length} of ${summaries.length} query/queries returned only PART of their matches`
      + (worst ? ` (worst: "${worst.query ?? '<empty>'}" -- ${worst.scanned} scanned of ${worst.declaredMatches} declared, ${worst.incompleteReason})` : '')
      + '; see the RUN_SUMMARY key-value record for the per-query numbers',
    );
  }
  if (notReachedSummaries.length || notReachedUsers.length) {
    notes.push(
      `the run stopped at ${timeBudgetExceeded ? 'the platform run timeout' : pushed >= maxResults ? `maxResults=${maxResults}` : 'the charge limit'} before `
      + `${notReachedSummaries.length} query/queries${notReachedUsers.length ? ` and ${notReachedUsers.length} username(s)` : ''} were searched at all`,
    );
  }
  if (emptyQueries.length) notes.push(`no matches for: ${emptyQueries.join(', ')}`);
  if (notFoundUsers.length) notes.push(`no such HN user: ${notFoundUsers.join(', ')}`);
  await Actor.setStatusMessage(`Pushed ${pushed} items. ${notes.join('; ')}.`);
} else if (watchMode && !seeding && baselineTruncated > 0) {
  // Otherwise-clean delivering run: none of the branches above fire, so without this the
  // baseline-eviction re-charge risk would be invisible in the Console (same gap found and
  // closed across the rest of the h285 arc).
  await Actor.setStatusMessage(
    `Pushed ${pushed} new item(s). WARNING: the baseline record dropped ${baselineTruncated} of the oldest `
    + `already-delivered id(s) this run (${baselineTruncatedTotal} total) to stay under its ${WATCH_KEEP}-id `
    + 'cap -- those will be charged for again as "new" on a future run unless you narrow the query/tags. '
    + 'See the RUN_SUMMARY key-value record.',
  );
}

if (watchMode && seedFailure) {
  await Actor.fail(
    `The watch baseline could not be completed: Algolia request(s) failed for: ${seedFailure}. No baseline was `
    + `saved for watch label "${watchLabel}" -- re-run with the same watchLabel to seed again.`,
  );
}

await Actor.exit();
