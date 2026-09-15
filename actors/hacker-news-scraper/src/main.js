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

if (!queries.length) queries.push(''); // empty query = browse by tag/date (e.g. front page, Ask HN, Who's Hiring)

const cm = Actor.getChargingManager();
const isPPE = cm.getPricingInfo().isPayPerEvent;
let pushed = 0;

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

function mapHit(hit) {
  const isComment = (hit._tags || []).includes('comment');
  const storyId = hit.story_id ?? hit.objectID;
  return {
    id: hit.objectID,
    type: isComment ? 'comment' : (hit._tags || []).find((t) => ['story', 'job', 'poll', 'ask_hn', 'show_hn'].includes(t)) || 'story',
    title: hit.title || hit.story_title || null,
    url: hit.url || (isComment ? null : `https://news.ycombinator.com/item?id=${hit.objectID}`) || hit.story_url || null,
    hnUrl: `https://news.ycombinator.com/item?id=${hit.objectID}`,
    author: hit.author || null,
    points: hit.points ?? null,
    numComments: hit.num_comments ?? null,
    storyId: storyId ?? null,
    storyTitle: hit.story_title || null,
    storyUrl: hit.story_url || null,
    text: hit.comment_text || hit.story_text || null,
    createdAt: hit.created_at || null,
    query: hit._query ?? null,
    karma: null,
    about: null,
    accountCreatedAt: null,
  };
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
  };
}

const emptyQueries = []; // Algolia matched nothing for this query/tags/filters combo
const erroredQueries = []; // the HTTP request itself failed
const seenIds = new Set(); // dedup across queries — overlapping/duplicate queries return the same objectID from Algolia
let duplicates = 0;
let keepGoing = true;
for (const query of queries) {
  if (!keepGoing) break;
  let page = 0;
  let fetched = 0;
  let requestFailed = false;
  const tagParts = [...tags];
  if (author) tagParts.push(`author_${author}`);
  const wantTags = tagParts.length ? tagParts.join(',') : undefined;
  if (!query && !wantTags) {
    // No query and no tags means Algolia's search endpoint matches its entire ~46M-item
    // history ranked by relevance — a silent runaway bill, not a legitimate "browse" request.
    log.warning('No query and no tags for this iteration — skipping (set tags, e.g. ["story"], or a search query; use "usernames" alone for user-profile-only runs).');
    emptyQueries.push(query || '<empty>');
    continue;
  }
  // A seeding run needs the whole current match set (up to SEED_CAP), not just the
  // buyer's usual maxItemsPerQuery slice, or the baseline would under-record and the
  // first incremental run would misreport old matches as new.
  const queryCap = seeding ? SEED_CAP : maxItemsPerQuery;
  while (keepGoing && fetched < queryCap) {
    const url = new URL(`https://hn.algolia.com/api/v1/${sortBy}`);
    if (query) url.searchParams.set('query', query);
    if (wantTags) url.searchParams.set('tags', includeComments ? wantTags : wantTags.split(',').filter((t) => t !== 'comment').join(','));
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
      if (seenIds.has(hit.objectID)) { duplicates += 1; continue; }
      seenIds.add(hit.objectID);
      hit._query = query || null;
      keepGoing = await pushResult(mapHit(hit), hit.objectID);
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

log.info(`Done. Pushed ${pushed} items.${duplicates ? ` Skipped ${duplicates} duplicate hit(s) already returned by an earlier query (not charged).` : ''}`);
if (pushed === 0 && watchMode && !seeding) {
  await Actor.setStatusMessage(`Nothing new for watch label "${watchLabel}" since its last run -- every matching item had already been delivered. That is the expected result most of the time; you were charged for nothing.`);
} else if (pushed === 0 && seeding) {
  await Actor.setStatusMessage(`Baseline run for watch label "${watchLabel}": ${watchSeen.size} existing item(s) recorded, 0 charged. Run again later to get only what's new.`);
} else if (pushed === 0 && (queries.length || usernames.length)) {
  const reasons = [];
  if (erroredQueries.length) reasons.push(`the request to Algolia's HN Search API failed for: ${erroredQueries.join(', ')} (see log for the error)`);
  if (emptyQueries.length) reasons.push(`no stories/comments matched: ${emptyQueries.join(', ')} — try different tags, a wider postedAfter/postedBefore range, or a lower minPoints`);
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
