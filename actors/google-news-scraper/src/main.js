import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';
import * as cheerio from 'cheerio';

await Actor.init();
const input = (await Actor.getInput()) ?? {};
const queries = (input.queries ?? []).map((q) => String(q).trim()).filter(Boolean);
const rssUrls = (input.rssUrls ?? []).map((u) => String(u).trim()).filter(Boolean);
const hl = input.language || 'en-US';
const gl = (input.country || 'US').toUpperCase();
const ceid = `${gl}:${hl.split('-')[0]}`;
const perQuery = Math.min(Number(input.maxItemsPerQuery ?? 100), 100);
const maxResults = Math.min(Number(input.maxResults ?? 500), 5000);
const decode = input.decodeUrls !== false;
if (!queries.length && !rssUrls.length) { await Actor.fail('Provide at least one query or RSS URL.'); }

let pushed = 0;
const seen = new Set();
const isPPE = Actor.getChargingManager().getPricingInfo().isPayPerEvent;
async function pushResult(item) {
  if (isPPE) {
    const r = await Actor.charge({ eventName: 'result', count: 1 });
    if (r.chargedCount === 0) return false; // user's budget exhausted: never push unpaid items
    await Actor.pushData(item); pushed += 1;
    return !r.eventChargeLimitReached && pushed < maxResults;
  }
  await Actor.pushData(item); pushed += 1; // non-PPE run (e.g. developer test): no charging
  return pushed < maxResults;
}
const http = (url, opts = {}) => gotScraping({ url, timeout: { request: 30000 }, retry: { limit: 2 }, headers: { 'accept-language': hl }, ...opts });

function parseRss(xml) {
  const $ = cheerio.load(xml, { xml: true });
  return $('item').map((_, el) => {
    const $el = $(el);
    const descHtml = $el.find('description').text();
    const $d = cheerio.load(descHtml || '');
    return {
      title: $el.find('title').text().trim(),
      googleNewsUrl: $el.find('link').text().trim(),
      guid: $el.find('guid').text().trim(),
      publishedAt: new Date($el.find('pubDate').text().trim()).toISOString(),
      source: $el.find('source').text().trim() || null,
      sourceUrl: $el.find('source').attr('url') || null,
      snippet: $d('a').first().text().trim() || null,
    };
  }).get();
}

// Decode Google News redirect URL -> publisher URL (batchexecute method).
async function decodeUrl(gnUrl) {
  try {
    const id = gnUrl.split('/articles/')[1]?.split('?')[0];
    if (!id) return null;
    const page = await http(`https://news.google.com/articles/${id}`);
    const $ = cheerio.load(page.body);
    const div = $('c-wiz > div').first();
    const sg = div.attr('data-n-a-sg'); const ts = div.attr('data-n-a-ts');
    if (!sg || !ts) return null;
    const payload = ['Fbv4je', `["garturlreq",[["X","X",["X","X"],null,null,1,1,"US:en",null,1,null,null,null,null,null,0,1],"X","X",1,[1,1,1],1,1,null,0,0,null,0],"${id}",${ts},"${sg}"]`];
    const res = await http('https://news.google.com/_/DotsSplashUi/data/batchexecute', {
      method: 'POST', headers: { 'content-type': 'application/x-www-form-urlencoded;charset=UTF-8' },
      body: `f.req=${encodeURIComponent(JSON.stringify([[payload]]))}`,
    });
    const chunk = res.body.split('\n\n')[1];
    const parsed = JSON.parse(chunk);
    const inner = JSON.parse(parsed[0][2]);
    return inner[1] || null;
  } catch (e) { log.debug(`decode failed: ${e.message}`); return null; }
}

const feeds = [
  ...queries.map((q) => ({ query: q, url: `https://news.google.com/rss/search?q=${encodeURIComponent(q)}&hl=${hl}&gl=${gl}&ceid=${ceid}` })),
  ...rssUrls.map((u) => ({ query: null, url: u })),
];
const emptyFeeds = []; // Google News RSS returned zero <item>s for this query/URL
const erroredFeeds = []; // the RSS request itself failed
const dedupedFeeds = []; // items existed but were all duplicates of an earlier feed's guid
let keepGoing = true;
for (const feed of feeds) {
  if (!keepGoing) break;
  log.info(`Fetching feed: ${feed.url}`);
  let items = [];
  try { items = parseRss((await http(feed.url)).body).slice(0, perQuery); }
  catch (e) { log.warning(`Feed failed (${feed.url}): ${e.message}`); erroredFeeds.push(feed.query || feed.url); continue; }
  log.info(`${items.length} items`);
  if (!items.length) { emptyFeeds.push(feed.query || feed.url); continue; }
  const pushedBefore = pushed;
  let allDuped = true;
  for (const it of items) {
    if (seen.has(it.guid)) continue; seen.add(it.guid);
    allDuped = false;
    const url = decode ? (await decodeUrl(it.googleNewsUrl)) : null;
    keepGoing = await pushResult({ ...it, url, query: feed.query, feedUrl: feed.url, language: hl, country: gl, scrapedAt: new Date().toISOString() });
    if (!keepGoing) break;
  }
  if (allDuped && pushed === pushedBefore) dedupedFeeds.push(feed.query || feed.url);
}
log.info(`Done. Pushed ${pushed} articles.`);
if (pushed === 0 && feeds.length) {
  const why = erroredFeeds.length
    ? `the RSS request failed for: ${erroredFeeds.join(', ')} (see log for the error)`
    : dedupedFeeds.length && !emptyFeeds.length
      ? `every item found was a duplicate already returned by another query/RSS URL: ${dedupedFeeds.join(', ')}`
      : `Google News returned zero results for: ${emptyFeeds.join(', ')} (try a broader query, different "country"/"language", or check the RSS URL)`;
  await Actor.setStatusMessage(`No articles returned — ${why}.`);
} else if (emptyFeeds.length || erroredFeeds.length) {
  await Actor.setStatusMessage(`Pushed ${pushed} items. No results for: ${emptyFeeds.join(', ') || 'none'}${erroredFeeds.length ? `; request failed for: ${erroredFeeds.join(', ')}` : ''}.`);
}
await Actor.exit();
