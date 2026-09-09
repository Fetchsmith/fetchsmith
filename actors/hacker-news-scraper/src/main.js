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

if (!queries.length) queries.push(''); // empty query = browse by tag/date (e.g. front page, Ask HN, Who's Hiring)

const cm = Actor.getChargingManager();
const isPPE = cm.getPricingInfo().isPayPerEvent;
let pushed = 0;

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
  };
}

const emptyQueries = []; // Algolia matched nothing for this query/tags/filters combo
const erroredQueries = []; // the HTTP request itself failed
let keepGoing = true;
for (const query of queries) {
  if (!keepGoing) break;
  let page = 0;
  let fetched = 0;
  let requestFailed = false;
  const wantTags = tags.length ? tags.join(',') : undefined;
  while (keepGoing && fetched < maxItemsPerQuery) {
    const url = new URL(`https://hn.algolia.com/api/v1/${sortBy}`);
    if (query) url.searchParams.set('query', query);
    if (wantTags) url.searchParams.set('tags', includeComments ? wantTags : wantTags.split(',').filter((t) => t !== 'comment').join(','));
    if (numericFilters.length) url.searchParams.set('numericFilters', numericFilters.join(','));
    url.searchParams.set('hitsPerPage', String(Math.min(100, maxItemsPerQuery - fetched)));
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
      hit._query = query || null;
      keepGoing = await pushResult(mapHit(hit));
      fetched += 1;
      if (!keepGoing) break;
    }
    page += 1;
    if (page >= (body.nbPages ?? 1)) break;
  }
  if (requestFailed) erroredQueries.push(query || '<empty>');
  else if (fetched === 0) emptyQueries.push(query || '<empty>');
}

log.info(`Done. Pushed ${pushed} items.`);
if (pushed === 0 && queries.length) {
  const why = erroredQueries.length
    ? `the request to Algolia's HN Search API failed for: ${erroredQueries.join(', ')} (see log for the error)`
    : `no stories/comments matched: ${emptyQueries.join(', ')} — try different tags, a wider postedAfter/postedBefore range, or a lower minPoints`;
  await Actor.setStatusMessage(`No items returned — ${why}.`);
} else if (emptyQueries.length) {
  await Actor.setStatusMessage(`Pushed ${pushed} items. No matches for: ${emptyQueries.join(', ')}.`);
}
await Actor.exit();
