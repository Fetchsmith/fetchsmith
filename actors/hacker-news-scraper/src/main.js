import { createHash } from 'crypto';
import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';

await Actor.init();
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
const enrichGithubLinks = input.enrichGithubLinks === true;
const excludeKeywords = [...new Set((input.excludeKeywords ?? []).map((k) => String(k).trim().toLowerCase()).filter((k) => k.length))];
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
const SEED_CAP = 5000; // bound the cost of a baseline run against a very broad query
const WATCH_KEEP = 20000; // bound the record size; oldest ids fall off first

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
const watchSeen = new Set(); // objectIDs already delivered under this label+fingerprint

if (watchMode) {
  const criteria = { queries, tags, sortBy, author, includeComments, numericFilters };
  if (excludeKeywords.length) criteria.excludeKeywords = excludeKeywords;
  watchStore = await Actor.openKeyValueStore(WATCH_STORE);
  const { key, fingerprint } = watchKeyFor(watchLabel, criteria);
  watchKey = key;
  const existing = await watchStore.getValue(key);
  if (existing && Array.isArray(existing.seenIds)) {
    watchRecord = existing;
    for (const id of existing.seenIds) watchSeen.add(String(id));
    log.info(
      `Watch mode "${watchLabel}" (${key}): baseline from ${existing.lastRunAt ?? 'an earlier run'} holds `
      + `${watchSeen.size} already-delivered item(s). Only items NOT in that baseline will be returned and charged.`,
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
    if (r.chargedCount === 0) return false;
    await Actor.pushData(item); pushed += 1;
    if (watchMode && watchId != null) watchSeen.add(String(watchId));
    return !r.eventChargeLimitReached && pushed < maxResults;
  }
  await Actor.pushData(item); pushed += 1;
  if (watchMode && watchId != null) watchSeen.add(String(watchId));
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
const GITHUB_NON_REPO_OWNERS = new Set(['sponsors', 'marketplace', 'topics', 'search', 'orgs', 'settings', 'apps', 'features', 'about', 'pricing']);
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
    });
    const d = res.body;
    const fields = {
      githubStars: d.stargazers_count ?? null,
      githubLanguage: d.language ?? null,
      githubPushedAt: d.pushed_at ?? null,
      githubOpenIssues: d.open_issues_count ?? null,
    };
    githubCache.set(repoFullName, fields);
    Object.assign(item, fields);
  } catch (e) {
    const status = e.response?.statusCode;
    if (status === 403 || status === 429) {
      githubRateLimited = true;
      log.warning('GitHub API rate limit reached -- remaining items in this run keep githubRepo but not star/language/pushed-at data.');
    } else if (status === 404) {
      githubCache.set(repoFullName, null); // repo renamed/deleted/private -- do not retry
    } else {
      log.warning(`GitHub lookup failed for ${repoFullName}: ${e.message}`);
    }
  }
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

const emptyQueries = []; // Algolia matched nothing for this query/tags/filters combo
const erroredQueries = []; // the HTTP request itself failed
const seenIds = new Set(); // dedup across queries — overlapping/duplicate queries return the same objectID from Algolia
let duplicates = 0;
let excluded = 0;
let keepGoing = true;
for (const query of queries) {
  if (!keepGoing) break;
  let page = 0;
  let fetched = 0;
  let requestFailed = false;
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
  const queryCap = watchMode ? SEED_CAP : maxItemsPerQuery;
  while (keepGoing && fetched < queryCap) {
    const url = new URL(`https://hn.algolia.com/api/v1/${sortBy}`);
    if (query) url.searchParams.set('query', query);
    if (wantTags) url.searchParams.set('tags', wantTags);
    if (numericFilters.length) url.searchParams.set('numericFilters', numericFilters.join(','));
    url.searchParams.set('hitsPerPage', String(Math.min(100, queryCap - fetched)));
    url.searchParams.set('page', String(page));
    log.info(`Fetching: ${url.toString()}`);
    let body;
    try {
      const res = await gotScraping({ url: url.toString(), timeout: { request: 30000 }, retry: { limit: 2 }, responseType: 'json' });
      body = res.body;
    } catch (e) {
      log.warning(`Query failed (${query || '<none>'}, page ${page}): ${e.message}`);
      requestFailed = true;
      break;
    }
    const hits = body.hits || [];
    if (!hits.length) break;
    for (const hit of hits) {
      fetched += 1;
      scanned += 1;
      if (seenIds.has(hit.objectID)) { duplicates += 1; continue; }
      seenIds.add(hit.objectID);
      hit._query = query || null;
      const mapped = mapHit(hit);
      if (excludedByKeyword(mapped)) { excluded += 1; continue; }
      // Skip the GitHub lookup for rows that pushResult will drop uncharged anyway
      // (seeding baseline, or already delivered under this watch label) -- those never
      // reach the buyer, so spending part of GitHub's 60/hr unauthenticated budget on them
      // would only starve the rows that actually get returned.
      const willDeliver = !(watchMode && (seeding || watchSeen.has(String(hit.objectID))));
      if (enrichGithubLinks && willDeliver) await enrichGithub(mapped);
      keepGoing = await pushResult(mapped, hit.objectID);
      if (!keepGoing) break;
    }
    page += 1;
    if (page >= (body.nbPages ?? 1)) break;
  }
  if (requestFailed) erroredQueries.push(query || '<empty>');
  else if (fetched === 0) emptyQueries.push(query || '<empty>');
}

const notFoundUsers = [];
const erroredUsers = [];
for (const username of usernames) {
  if (!keepGoing) break;
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

if (watchMode) {
  await saveWatchRecord(seeding ? 'seeded' : 'incremental');
  if (seeding) {
    log.info(
      `Baseline saved for watch label "${watchLabel}": ${watchSeen.size} item(s) recorded as already-seen, `
      + '0 results returned, 0 charged. The next run on this label and these filters returns only new items.'
      + (watchSeen.size >= SEED_CAP
        ? ` NOTE: the baseline hit the ${SEED_CAP}-item cap. Narrow the query (tighter keywords, tags, or `
        + 'a date/point/comment threshold) so the whole current match set fits, or the first incremental run may '
        + 'report older items past the cap as new.'
        : ''),
    );
  } else {
    log.info(`Watch label "${watchLabel}": ${pushed} new item(s) since the last run (${watchSkipped} already-delivered hit(s) skipped, not charged); baseline now holds ${watchSeen.size}.`);
  }
}

log.info(`Done. Pushed ${pushed} items.${duplicates ? ` Skipped ${duplicates} duplicate hit(s) already returned by an earlier query (not charged).` : ''}${excluded ? ` Dropped ${excluded} hit(s) matching excludeKeywords (not charged).` : ''}`);

// Fires after every row is already pushed and charged, so a slow or failing webhook can never
// affect the result set or the bill -- best-effort only, one attempt, short timeout, failures are
// a warning not a thrown error. Watch mode here drops already-seen hits BEFORE the push loop, so
// `watchNewCount` is `pushed` and there is no change-detection counter to report (cycle 441 lesson,
// same shape as trademark-search-scraper).
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

if (pushed === 0 && watchMode && !seeding) {
  await Actor.setStatusMessage(`Nothing new for watch label "${watchLabel}" since its last run -- every matching item had already been delivered. That is the expected result most of the time; you were charged for nothing.`);
} else if (pushed === 0 && seeding) {
  await Actor.setStatusMessage(`Baseline run for watch label "${watchLabel}": ${watchSeen.size} existing item(s) recorded, 0 charged. Run again later to get only what's new.`);
} else if (pushed === 0 && (queries.length || usernames.length)) {
  const reasons = [];
  if (erroredQueries.length) reasons.push(`the request to Algolia's HN Search API failed for: ${erroredQueries.join(', ')} (see log for the error)`);
  if (emptyQueries.length) reasons.push(`no stories/comments matched: ${emptyQueries.join(', ')} — try different tags, a wider postedAfter/postedBefore range, or a lower minPoints`);
  if (excluded) reasons.push(`excludeKeywords (${excludeKeywords.join(', ')}) removed all ${excluded} otherwise-matching item(s)`);
  if (erroredUsers.length) reasons.push(`the user lookup failed for: ${erroredUsers.join(', ')} (see log for the error)`);
  if (notFoundUsers.length) reasons.push(`no such HN user: ${notFoundUsers.join(', ')}`);
  await Actor.setStatusMessage(`No items returned — ${reasons.join('; ') || 'no queries or usernames provided'}.`);
} else if (emptyQueries.length || notFoundUsers.length) {
  const notes = [];
  if (emptyQueries.length) notes.push(`no matches for: ${emptyQueries.join(', ')}`);
  if (notFoundUsers.length) notes.push(`no such HN user: ${notFoundUsers.join(', ')}`);
  await Actor.setStatusMessage(`Pushed ${pushed} items. ${notes.join('; ')}.`);
}
await Actor.exit();
