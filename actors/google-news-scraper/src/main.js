import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';
import * as cheerio from 'cheerio';
import { makeArticleFetcher } from './article.js';

await Actor.init();
const input = (await Actor.getInput()) ?? {};
const queries = (input.queries ?? []).map((q) => String(q).trim()).filter(Boolean);
const rssUrls = (input.rssUrls ?? []).map((u) => String(u).trim()).filter(Boolean);
const hl = input.language || 'en-US';
const gl = (input.country || 'US').toUpperCase();
const ceid = `${gl}:${hl.split('-')[0]}`;
const perQuery = Math.min(Number(input.maxItemsPerQuery ?? 100), 100);
const maxResults = Math.min(Number(input.maxResults ?? 500), 5000);
const fetchBody = input.fetchArticleBody === true;
const decode = input.decodeUrls !== false || fetchBody; // the body lives on the publisher's page, so it needs the real URL
const bodyMaxChars = Math.min(Math.max(Number(input.articleBodyMaxChars ?? 20000), 500), 200000);
if (!queries.length && !rssUrls.length) { await Actor.fail('Provide at least one query or RSS URL.'); }
if (fetchBody && input.decodeUrls === false) log.warning('fetchArticleBody needs the publisher URL, so decodeUrls was turned back on.');

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

const fetchArticle = makeArticleFetcher({ http, bodyMaxChars, log });

// Decode Google News redirect URL -> publisher URL (batchexecute method).
// Google rate-limits this endpoint per source IP (429) once you decode a lot in a short window;
// when that happens every article comes back with url:null, so count it and say so at the end
// instead of leaving the user with a silently empty column.
let decodeRateLimited = 0; let decodeFailed = 0;
async function decodeUrl(gnUrl) {
  try {
    const id = gnUrl.split('/articles/')[1]?.split('?')[0];
    if (!id) { decodeFailed += 1; return null; }
    const page = await http(`https://news.google.com/articles/${id}`, { throwHttpErrors: false });
    if (page.statusCode === 429) {
      decodeRateLimited += 1;
      log.warning('Google News rate-limited the URL-decoding endpoint (429) — this article keeps its googleNewsUrl but url will be null.');
      await new Promise((r) => setTimeout(r, Math.min(2000 * decodeRateLimited, 15000))); // back off so a burst can recover
      return null;
    }
    const $ = cheerio.load(page.body);
    const div = $('c-wiz > div').first();
    const sg = div.attr('data-n-a-sg'); const ts = div.attr('data-n-a-ts');
    if (!sg || !ts) { decodeFailed += 1; return null; }
    const payload = ['Fbv4je', `["garturlreq",[["X","X",["X","X"],null,null,1,1,"US:en",null,1,null,null,null,null,null,0,1],"X","X",1,[1,1,1],1,1,null,0,0,null,0],"${id}",${ts},"${sg}"]`];
    const res = await http('https://news.google.com/_/DotsSplashUi/data/batchexecute', {
      method: 'POST', headers: { 'content-type': 'application/x-www-form-urlencoded;charset=UTF-8' },
      body: `f.req=${encodeURIComponent(JSON.stringify([[payload]]))}`,
    });
    const chunk = res.body.split('\n\n')[1];
    const parsed = JSON.parse(chunk);
    const inner = JSON.parse(parsed[0][2]);
    return inner[1] || null;
  } catch (e) { log.debug(`decode failed: ${e.message}`); decodeFailed += 1; return null; }
}

const feeds = [
  ...queries.map((q) => ({ query: q, url: `https://news.google.com/rss/search?q=${encodeURIComponent(q)}&hl=${hl}&gl=${gl}&ceid=${ceid}` })),
  ...rssUrls.map((u) => ({ query: null, url: u })),
];
const emptyFeeds = []; // Google News RSS returned zero <item>s for this query/URL
const erroredFeeds = []; // the RSS request itself failed
const dedupedFeeds = []; // items existed but were all duplicates of an earlier feed's guid
let bodiesOk = 0; let bodiesFailed = 0; // only counted when fetchArticleBody is on
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
    let article = {};
    if (fetchBody) {
      article = url ? await fetchArticle(url) : { articleFetchStatus: 'no-url' };
      if (article.articleFetchStatus === 'ok') bodiesOk += 1; else bodiesFailed += 1;
    }
    keepGoing = await pushResult({ ...it, url, ...article, query: feed.query, feedUrl: feed.url, language: hl, country: gl, scrapedAt: new Date().toISOString() });
    if (!keepGoing) break;
  }
  if (allDuped && pushed === pushedBefore) dedupedFeeds.push(feed.query || feed.url);
}
log.info(`Done. Pushed ${pushed} articles.`);
if (fetchBody) log.info(`Article bodies: ${bodiesOk} extracted, ${bodiesFailed} unavailable (paywall/blocked/no text).`);
const bodyNote = fetchBody ? ` Article bodies: ${bodiesOk} extracted, ${bodiesFailed} unavailable (paywalled or publisher-blocked — see articleFetchStatus).` : '';
const decodeNote = decodeRateLimited
  ? ` Google rate-limited URL decoding for ${decodeRateLimited} article(s) (url is null; googleNewsUrl still works) — re-run with a proxy or fewer articles per run.`
  : decodeFailed ? ` ${decodeFailed} article URL(s) could not be decoded (url is null; googleNewsUrl still works).` : '';
if (pushed === 0 && feeds.length) {
  const why = erroredFeeds.length
    ? `the RSS request failed for: ${erroredFeeds.join(', ')} (see log for the error)`
    : dedupedFeeds.length && !emptyFeeds.length
      ? `every item found was a duplicate already returned by another query/RSS URL: ${dedupedFeeds.join(', ')}`
      : `Google News returned zero results for: ${emptyFeeds.join(', ')} (try a broader query, different "country"/"language", or check the RSS URL)`;
  await Actor.setStatusMessage(`No articles returned — ${why}.`);
} else if (emptyFeeds.length || erroredFeeds.length) {
  await Actor.setStatusMessage(`Pushed ${pushed} items. No results for: ${emptyFeeds.join(', ') || 'none'}${erroredFeeds.length ? `; request failed for: ${erroredFeeds.join(', ')}` : ''}.${bodyNote}${decodeNote}`);
} else if ((fetchBody && bodiesFailed) || decodeNote) {
  await Actor.setStatusMessage(`Pushed ${pushed} items.${bodyNote}${decodeNote}`);
}
await Actor.exit();
