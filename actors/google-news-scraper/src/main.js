import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';
import * as cheerio from 'cheerio';
import { makeArticleFetcher } from './article.js';

await Actor.init();
// Heavy inputs (many queries x maxItemsPerQuery, decodeUrls/fetchArticleBody on) process articles
// strictly sequentially, so a run can approach the platform timeout with real work still queued.
// Getting hard-killed there returns nothing to the customer even though partial results already
// exist in the dataset. Stop proactively with a safety margin and flush what's collected instead.
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
const queries = (input.queries ?? []).map((q) => String(q).trim()).filter(Boolean);
const rssUrls = (input.rssUrls ?? []).map((u) => String(u).trim()).filter(Boolean);
const VALID_TOPICS = ['WORLD', 'NATION', 'BUSINESS', 'TECHNOLOGY', 'ENTERTAINMENT', 'SCIENCE', 'SPORTS', 'HEALTH'];
const topics = (input.topics ?? []).map((t) => String(t).trim().toUpperCase()).filter((t) => VALID_TOPICS.includes(t));
const excludeWords = (input.excludeWords ?? []).map((w) => String(w).trim()).filter(Boolean);
const excludeSuffix = excludeWords.map((w) => ` -${w.includes(' ') ? `"${w}"` : w}`).join('');

// Restrict/exclude results by publisher domain via Google's own `site:` search operator — verified
// live (2026-09-18) that a single `site:nytimes.com`, an OR-group `(site:a.com OR site:b.com)` for
// multiple sites, and `-site:x.com` for exclusion all genuinely narrow the RSS feed (checked against
// the returned `<source>` per item, not just result-count deltas — the noise-floor trap from cycle
// 407's `lr`/`cr`/`nfpr` probe). Client-side domain filtering was considered and rejected: it would
// silently under-deliver `maxItemsPerQuery` (Google already applies the restriction server-side, at
// no extra cost, before results are even paged).
const cleanDomain = (d) => String(d).trim().toLowerCase().replace(/^https?:\/\//, '').replace(/^www\./, '').replace(/\/.*$/, '');
const siteFilter = (input.siteFilter ?? []).map(cleanDomain).filter(Boolean);
const excludeSites = (input.excludeSites ?? []).map(cleanDomain).filter(Boolean);
let siteSuffix = '';
if (siteFilter.length === 1) siteSuffix += ` site:${siteFilter[0]}`;
else if (siteFilter.length > 1) siteSuffix += ` (${siteFilter.map((d) => `site:${d}`).join(' OR ')})`;
siteSuffix += excludeSites.map((d) => ` -site:${d}`).join('');
if (siteSuffix && !queries.length) log.warning('siteFilter/excludeSites were set but there are no search queries — they do not apply to topics or custom RSS URLs, which are fixed feeds.');

// Date filtering is done by Google itself, via search operators appended to the query — no extra
// requests and no client-side discarding of articles the customer already paid to fetch.
// Only the h/d/y units work on the RSS search endpoint: `when:1m` and `when:12m` return an EMPTY
// feed rather than an error (verified live, cycle 204), so the enum below deliberately offers 30d
// and 1y instead of "1 month"/"1 year in months".
const VALID_PERIODS = ['1h', '6h', '12h', '1d', '7d', '30d', '90d', '1y'];
const rawPeriod = String(input.timePeriod ?? '').trim().toLowerCase();
const timePeriod = VALID_PERIODS.includes(rawPeriod) ? rawPeriod : '';
if (rawPeriod && !timePeriod) log.warning(`Ignoring unsupported timePeriod "${rawPeriod}" — use one of: ${VALID_PERIODS.join(', ')}.`);
const isDate = (v) => /^\d{4}-\d{2}-\d{2}$/.test(v);
const normDate = (v, name) => {
  const s = String(v ?? '').trim().slice(0, 10);
  if (!s) return '';
  if (!isDate(s)) { log.warning(`Ignoring ${name} "${s}" — expected YYYY-MM-DD.`); return ''; }
  return s;
};
const publishedAfter = normDate(input.publishedAfter, 'publishedAfter');
const publishedBefore = normDate(input.publishedBefore, 'publishedBefore');
// Explicit dates win: Google applies the narrower of the two inconsistently, so never send both.
let timeSuffix = '';
if (publishedAfter || publishedBefore) {
  if (timePeriod) log.warning('Both timePeriod and publishedAfter/publishedBefore were set — using the explicit dates and ignoring timePeriod.');
  if (publishedAfter) timeSuffix += ` after:${publishedAfter}`;
  if (publishedBefore) timeSuffix += ` before:${publishedBefore}`;
} else if (timePeriod) {
  timeSuffix = ` when:${timePeriod}`;
}
// These operators only exist on the search endpoint. Topic sections and user-supplied RSS URLs are
// fixed feeds, so a date filter set with only those inputs would silently do nothing — say so.
if (timeSuffix && !queries.length) log.warning('A date filter was set but there are no search queries — it does not apply to topics or custom RSS URLs, which are fixed feeds.');

// Backstop for a measured Google bug (cycle 788): `after:`/`before:` are honoured on their own, with
// `-word` exclusions and with a positive `site:` (0 far-out-of-window items in 100 on each), but
// combining them with a `-site:` exclusion — i.e. setting `excludeSites` together with an explicit
// date window — makes the feed leak articles months to YEARS outside the window (7 in 100 measured,
// incl. a 2011 item). `when:Nd` + `-site:` does not leak, so this is specific to the explicit-date
// operators. Those rows are pay-per-result items that flatly contradict the filter the customer set,
// so drop them before decoding/charging rather than bill for them.
// The tolerance is deliberately a full day, not zero: Google evaluates `after:`/`before:` in its own
// (US Pacific) timezone while `publishedAt` is UTC, so up to ~8h of legitimately in-window articles
// sit just outside the UTC window at each edge (7-15 in 100 on every query shape, including the ones
// with no leak at all). A zero-tolerance client-side filter would throw those away as "violations".
const dropAfterMs = publishedAfter ? Date.parse(`${publishedAfter}T00:00:00Z`) - 86_400_000 : null;
const dropBeforeMs = publishedBefore ? Date.parse(`${publishedBefore}T00:00:00Z`) + 86_400_000 : null;
const enforceDates = dropAfterMs != null || dropBeforeMs != null;
let outOfWindowDropped = 0;
function farOutsideWindow(publishedAt) {
  if (!enforceDates) return false;
  const t = Date.parse(publishedAt);
  if (!Number.isFinite(t)) return false; // unparseable pubDate: not evidence of a violation
  return (dropAfterMs != null && t < dropAfterMs) || (dropBeforeMs != null && t >= dropBeforeMs);
}
// Don't double-apply if the customer already typed the operator into the query themselves.
const hasOwnTimeOp = (q) => /\b(when|after|before):/i.test(q);
const hl = input.language || 'en-US';
const gl = (input.country || 'US').toUpperCase();
const ceid = `${gl}:${hl.split('-')[0]}`;
const perQuery = Math.min(Number(input.maxItemsPerQuery ?? 100), 100);
const maxResults = Math.min(Number(input.maxResults ?? 500), 5000);
const fetchBody = input.fetchArticleBody === true;
const extractTickers = input.extractTickers === true;
const decode = input.decodeUrls !== false || fetchBody; // the body lives on the publisher's page, so it needs the real URL
const bodyMaxChars = Math.min(Math.max(Number(input.articleBodyMaxChars ?? 20000), 500), 200000);
if (!queries.length && !rssUrls.length && !topics.length) { await Actor.fail('Provide at least one query, RSS URL or topic.'); }
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
// Google rate-limits the URL-decoding endpoint per source IP (see decodeUrl below); rotating
// proxy IPs is the actual fix, not just a race against the rate limiter. Runs without proxy
// access must still work, so fall back to a direct connection instead of failing the run.
let proxyUrlFor = async () => undefined;
try {
  const proxyConfiguration = await Actor.createProxyConfiguration(input.proxyConfiguration ?? { useApifyProxy: true });
  if (proxyConfiguration) {
    proxyUrlFor = () => proxyConfiguration.newUrl(); // no session id: a fresh IP each call
    log.info('Using Apify Proxy for Google/publisher requests.');
  }
} catch (e) { log.warning(`Proxy unavailable (${e.message}) — continuing with a direct connection.`); }
// got's own `retry` only fires for a fixed errorCodes list that does not include the
// connection-establishment faults (ERR_HTTP2_ERROR / HPE_INVALID_CONSTANT) measured live on
// this same got-scraping version in cycle 616 — about 1 in 4 fresh connections. Without an
// outer retry, one blip on a feed request drops that whole feed into `erroredFeeds` (see the
// feed loop below), silently under-delivering a paid run instead of erroring loudly. Retry
// connection-level throws a handful of times before giving up.
// The between-feed/between-item budget checks below are necessary but NOT sufficient on their own:
// they can pass with ~45s of margin left and then hand control to a call chain worth minutes. One
// article with `fetchArticleBody` on costs up to 3 page variants x 3 outer attempts x got's own
// retries x a 25-30s request timeout, so a single item can overshoot the deadline many times over
// and the platform hard-kills the run as TIMED-OUT — exactly the outcome the guard exists to avoid
// (one such external run observed in the 30-day public stats, cycle 712). Clamp every request to
// the time actually left, including got's internal retries, so no single call can outlive the run.
const MIN_REQUEST_MS = 3000; // below this a request is not worth starting; stop instead
const http = async (url, opts = {}) => {
  let lastErr;
  for (let attempt = 1; attempt <= 3; attempt += 1) {
    const left = remainingMs();
    if (left <= MIN_REQUEST_MS) {
      timeBudgetExceeded = true;
      throw lastErr ?? new Error('run time budget exhausted before the request could be made');
    }
    const wantedMs = opts.timeout?.request ?? 30000;
    const wantedRetries = opts.retry?.limit ?? 2;
    const perRequest = Math.max(MIN_REQUEST_MS, Math.min(wantedMs, left));
    // got applies `timeout.request` per attempt, so `limit: 2` is worth 3x that wall-clock.
    // Allow only as many attempts as fit in what's left.
    const retryLimit = Math.max(0, Math.min(wantedRetries, Math.floor(left / perRequest) - 1));
    try {
      return await gotScraping({
        url, headers: { 'accept-language': hl }, proxyUrl: await proxyUrlFor(), ...opts,
        timeout: { ...(opts.timeout ?? {}), request: perRequest }, retry: { ...(opts.retry ?? {}), limit: retryLimit },
      });
    } catch (e) {
      lastErr = e;
      if (attempt < 3 && remainingMs() > MIN_REQUEST_MS) {
        log.warning(`${url}: attempt ${attempt}/3 failed (${e.message}) — retrying.`);
        await new Promise((r) => setTimeout(r, Math.min(attempt * 1000, Math.max(0, remainingMs() - MIN_REQUEST_MS))));
      }
    }
  }
  throw lastErr;
};

// Google News RSS titles always arrive as "Headline - Publisher" (verified live on 204/204 items
// across two search feeds, cycle 264), which is noise once `source` already carries the publisher.
const stripSourceSuffix = (title, source) => (source && title.endsWith(` - ${source}`) ? title.slice(0, -(source.length + 3)).trim() : null);
const hostOf = (u) => { try { return new URL(u).hostname.replace(/^www\./, ''); } catch { return null; } };

function parseRss(xml) {
  const $ = cheerio.load(xml, { xml: true });
  return $('item').map((_, el) => {
    const $el = $(el);
    const descHtml = $el.find('description').text();
    const $d = cheerio.load(descHtml || '');
    const title = $el.find('title').text().trim();
    const source = $el.find('source').text().trim() || null;
    const sourceUrl = $el.find('source').attr('url') || null;
    // The <description> is not a summary: it is either a single <a> holding the headline again, or
    // an <ol> of the same story as covered by several publishers, each <a> paired with a grey
    // <font> naming that publisher. Entries after the first are therefore genuinely new data.
    const $links = $d('a');
    const $fonts = $d('font');
    const related = $links.slice(1).map((i, a) => ({
      title: $d(a).text().trim() || null,
      source: $fonts.eq(i + 1).text().trim() || null,
      googleNewsUrl: $d(a).attr('href') || null,
    })).get().filter((r) => r.title);
    return {
      title,
      // Google's own clean headline, with the " - Publisher" suffix removed.
      titleClean: stripSourceSuffix(title, source) || $links.first().text().trim() || title,
      googleNewsUrl: $el.find('link').text().trim(),
      guid: $el.find('guid').text().trim(),
      publishedAt: new Date($el.find('pubDate').text().trim()).toISOString(),
      source,
      sourceUrl,
      sourceDomain: hostOf(sourceUrl),
      // Kept for backward compatibility with existing customer pipelines, but Google News RSS ships
      // no real article summary — this always mirrors the headline. Turn on "Extract full article
      // text" and use `articleDescription` for an actual summary.
      snippet: $links.first().text().trim() || null,
      relatedArticles: related,
    };
  }).get();
}

const fetchArticle = makeArticleFetcher({ http, bodyMaxChars, log });

// Cheap, rule-based ticker extraction (no extra HTTP request) — deliberately narrow: only
// explicit financial notation, never a bare capitalized word. Blind "any 2-5 uppercase letters"
// matching floods results with false positives (WSJ, IPO, FSD, EV, AI, ...). Three signals, all
// verified live against real Google News headlines (cycle 323): a cashtag ($TSLA), an exchange
// prefix/suffix (NASDAQ:AAPL, AAPL:NASDAQ), or a capitalized name immediately followed by
// "(TICKER)" (the single most common real convention, e.g. "Tesla, Inc. (TSLA)") — the third one
// needs a blocklist since plenty of non-ticker acronyms follow the same shape ("United Nations
// (UN)", "the Fed (Fed)"); the list below is common real offenders, not exhaustive.
const EXCHANGES = 'NASDAQ|NYSE|AMEX|LSE|TSX|ASX|HKEX|NSE|BSE|SSE|SZSE|TSE|FWB|EPA|ETR';
const NON_TICKER_ACRONYMS = new Set([
  'CEO', 'CFO', 'COO', 'CTO', 'CMO', 'LLC', 'INC', 'LTD', 'LLP', 'PLC',
  'USA', 'USD', 'EUR', 'GBP', 'UK', 'EU', 'UN', 'US', 'AI', 'EV', 'IPO',
  'FDA', 'SEC', 'FTC', 'DOJ', 'FBI', 'CIA', 'NASA', 'GDP', 'ESG', 'API',
  'FAQ', 'PDF', 'URL', 'HR', 'IT', 'PR', 'VP', 'OK', 'TV', 'UFO', 'WHO',
  'ECB', 'FED', 'IMF', 'WTO', 'NATO', 'NYT', 'WSJ', 'BBC', 'CNN', 'CNBC', 'OPEC',
]);
const TICKER_CASHTAG_RE = /\$([A-Z]{1,5})\b/g;
const TICKER_EXCHANGE_RE = new RegExp(`\\b(?:(${EXCHANGES})\\s*:\\s*([A-Z]{1,5})|([A-Z]{1,5})\\s*:\\s*(?:${EXCHANGES}))\\b`, 'g');
const TICKER_PAREN_RE = /\b[A-Z][\w&.'-]*\s\(([A-Z]{2,5})\)/g;
function extractTickersFrom(text) {
  if (!text) return [];
  const out = new Set();
  let m;
  TICKER_CASHTAG_RE.lastIndex = 0;
  while ((m = TICKER_CASHTAG_RE.exec(text))) out.add(m[1]);
  TICKER_EXCHANGE_RE.lastIndex = 0;
  while ((m = TICKER_EXCHANGE_RE.exec(text))) out.add(m[2] || m[3]);
  TICKER_PAREN_RE.lastIndex = 0;
  while ((m = TICKER_PAREN_RE.exec(text))) { if (!NON_TICKER_ACRONYMS.has(m[1])) out.add(m[1]); }
  return [...out];
}

// Decode Google News redirect URL -> publisher URL (batchexecute method).
// Google rate-limits this endpoint per source IP (429) once you decode a lot in a short window;
// when that happens every article comes back with url:null, so count it and say so at the end
// instead of leaving the user with a silently empty column.
// Once the endpoint starts 429ing for this IP it generally stays that way for the
// whole run, so backing off per article just burns the user's compute minutes to
// produce url:null anyway (seen live 2026-09-11: 100 articles x ~18s of backoff =
// ~30 min run, every url null). Give the burst a few chances to recover, then stop
// decoding for the rest of the run and finish fast with googleNewsUrl only.
const DECODE_GIVE_UP_AFTER = 4;
let decodeRateLimited = 0; let decodeFailed = 0; let decodeDisabled = false; let consecutive429 = 0;
async function decodeUrl(gnUrl) {
  if (decodeDisabled) return null;
  try {
    const id = gnUrl.split('/articles/')[1]?.split('?')[0];
    if (!id) { decodeFailed += 1; return null; }
    const page = await http(`https://news.google.com/articles/${id}`, { throwHttpErrors: false });
    if (page.statusCode === 429) {
      decodeRateLimited += 1; consecutive429 += 1;
      if (consecutive429 >= DECODE_GIVE_UP_AFTER) {
        decodeDisabled = true;
        log.warning(`Google News rate-limited the URL-decoding endpoint (429) ${consecutive429} times in a row — giving up on decoding for this run. Every article still gets googleNewsUrl (which redirects to the publisher in a browser); url will be null.`);
        return null;
      }
      log.warning('Google News rate-limited the URL-decoding endpoint (429) — this article keeps its googleNewsUrl but url will be null.');
      // Back off so a burst can recover — but never sleep past the run's deadline.
      await new Promise((r) => setTimeout(r, Math.max(0, Math.min(2000 * decodeRateLimited, 15000, remainingMs()))));
      return null;
    }
    consecutive429 = 0; // the burst recovered; don't trip the breaker on scattered 429s
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
  ...queries.map((q) => ({ query: q, topic: null, url: `https://news.google.com/rss/search?q=${encodeURIComponent(q + excludeSuffix + siteSuffix + (hasOwnTimeOp(q) ? '' : timeSuffix))}&hl=${hl}&gl=${gl}&ceid=${ceid}` })),
  ...rssUrls.map((u) => ({ query: null, topic: null, url: u })),
  ...topics.map((t) => ({ query: null, topic: t, url: `https://news.google.com/rss/headlines/section/topic/${t}?hl=${hl}&gl=${gl}&ceid=${ceid}` })),
];
const emptyFeeds = []; // Google News RSS returned zero <item>s for this query/URL
const erroredFeeds = []; // the RSS request itself failed
const dedupedFeeds = []; // items existed but were all duplicates of an earlier feed's guid
let bodiesOk = 0; let bodiesFailed = 0; // only counted when fetchArticleBody is on
let keepGoing = true;
for (const feed of feeds) {
  if (!keepGoing) break;
  if (!timeBudgetOk()) { log.warning('Approaching the run timeout — stopping early and returning what has been collected so far.'); break; }
  log.info(`Fetching feed: ${feed.url}`);
  let items = [];
  try { items = parseRss((await http(feed.url)).body).slice(0, perQuery); }
  catch (e) {
    // A feed we ran out of time to even request is not an errored feed — reporting it as one would
    // blame Google for our own deadline. Stop instead and let the status message say "ran out of time".
    if (timeBudgetExceeded) { log.warning('Approaching the run timeout — stopping early and returning what has been collected so far.'); break; }
    log.warning(`Feed failed (${feed.url}): ${e.message}`); erroredFeeds.push(feed.query || feed.topic || feed.url); continue;
  }
  log.info(`${items.length} items`);
  if (!items.length) { emptyFeeds.push(feed.query || feed.topic || feed.url); continue; }
  const pushedBefore = pushed;
  let allDuped = true;
  for (const [idx, it] of items.entries()) {
    if (!timeBudgetOk()) { log.warning('Approaching the run timeout — stopping early and returning what has been collected so far.'); keepGoing = false; break; }
    if (seen.has(it.guid)) continue; seen.add(it.guid);
    allDuped = false;
    // Only search feeds carry our date operators; topics/custom RSS URLs are fixed feeds, and a query
    // with the customer's own when:/after:/before: never got our suffix, so neither is ours to police.
    if (feed.query && !hasOwnTimeOp(feed.query) && farOutsideWindow(it.publishedAt)) { outOfWindowDropped += 1; continue; }
    const url = decode ? (await decodeUrl(it.googleNewsUrl)) : null;
    let article = {};
    if (fetchBody) {
      article = url ? await fetchArticle(url) : { articleFetchStatus: 'no-url' };
      if (article.articleFetchStatus === 'ok') bodiesOk += 1; else bodiesFailed += 1;
    }
    // Rank as Google ordered it within this feed (1-based), so relevance/recency order survives
    // into the dataset even after export or sorting.
    // Enrichment (decode/body) ran out of runway rather than finishing: don't charge the buyer for a
    // row whose url/articleBody is blank only because the clock stopped us mid-item. Drop it and stop.
    if (timeBudgetExceeded) { log.warning('Approaching the run timeout — stopping early and returning what has been collected so far.'); keepGoing = false; break; }
    const tickers = extractTickers ? { tickers: extractTickersFrom(`${it.title} ${article.articleBody ?? ''}`) } : {};
    keepGoing = await pushResult({ ...it, url, ...article, ...tickers, position: idx + 1, query: feed.query, topic: feed.topic, feedUrl: feed.url, language: hl, country: gl, scrapedAt: new Date().toISOString() });
    if (!keepGoing) break;
  }
  if (allDuped && pushed === pushedBefore) dedupedFeeds.push(feed.query || feed.topic || feed.url);
}
log.info(`Done. Pushed ${pushed} articles.`);
if (fetchBody) log.info(`Article bodies: ${bodiesOk} extracted, ${bodiesFailed} unavailable (paywall/blocked/no text).`);
const bodyNote = fetchBody ? ` Article bodies: ${bodiesOk} extracted, ${bodiesFailed} unavailable (paywalled or publisher-blocked — see articleFetchStatus).` : '';
const decodeNote = decodeRateLimited
  ? ` Google rate-limited URL decoding for ${decodeRateLimited} article(s)${decodeDisabled ? ', so decoding was switched off for the rest of the run' : ''} (url is null; googleNewsUrl still works) — Apify Proxy is already on by default; if it's off, turn it on, or reduce articles per run.`
  : decodeFailed ? ` ${decodeFailed} article URL(s) could not be decoded (url is null; googleNewsUrl still works).` : '';
if (outOfWindowDropped) log.info(`Dropped ${outOfWindowDropped} article(s) Google returned outside the requested publishedAfter/publishedBefore window.`);
const windowNote = outOfWindowDropped
  ? ` Dropped ${outOfWindowDropped} article(s) that Google returned well outside your publishedAfter/publishedBefore window (a known Google quirk when a date window is combined with "Exclude these domains") — you were not charged for them.`
  : '';
const timeBudgetNote = timeBudgetExceeded
  ? ` Stopped before finishing all queries because the run was approaching its time limit — the ${pushed} article(s) already found are complete and charged normally; re-run with fewer queries, a lower "Max articles per query", or "Extract full article text" off to cover the rest.`
  : '';
if (pushed === 0 && feeds.length && !timeBudgetExceeded) {
  const why = erroredFeeds.length
    ? `the RSS request failed for: ${erroredFeeds.join(', ')} (see log for the error)`
    : dedupedFeeds.length && !emptyFeeds.length
      ? `every item found was a duplicate already returned by another query/RSS URL: ${dedupedFeeds.join(', ')}`
      : !emptyFeeds.length && outOfWindowDropped
        // Items came back, but every one of them fell outside the requested date window. Saying
        // "Google returned zero results" here would send the customer off to widen a query that
        // is not the problem.
        ? `every article Google returned fell outside your publishedAfter/publishedBefore window (try widening the dates)`
        : `Google News returned zero results for: ${emptyFeeds.join(', ')} (try a broader query, different "country"/"language", or check the RSS URL)`;
  await Actor.setStatusMessage(`No articles returned — ${why}.${windowNote}`);
} else if (pushed === 0 && timeBudgetExceeded) {
  await Actor.setStatusMessage(`No articles returned before the run approached its time limit.${timeBudgetNote}`);
} else if (emptyFeeds.length || erroredFeeds.length || timeBudgetExceeded) {
  await Actor.setStatusMessage(`Pushed ${pushed} items. No results for: ${emptyFeeds.join(', ') || 'none'}${erroredFeeds.length ? `; request failed for: ${erroredFeeds.join(', ')}` : ''}.${bodyNote}${decodeNote}${windowNote}${timeBudgetNote}`);
} else if ((fetchBody && bodiesFailed) || decodeNote || windowNote) {
  await Actor.setStatusMessage(`Pushed ${pushed} items.${bodyNote}${decodeNote}${windowNote}`);
}
await Actor.exit();
