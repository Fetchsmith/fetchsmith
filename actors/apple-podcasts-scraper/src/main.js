import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';
import * as cheerio from 'cheerio';

await Actor.init();
const input = (await Actor.getInput()) ?? {};
const podcasts = (input.podcasts ?? []).map((p) => String(p).trim()).filter(Boolean);
const searchTerms = (input.searchTerms ?? []).map((t) => String(t).trim()).filter(Boolean);
const dataType = ['episodes', 'reviews', 'podcasts', 'charts', 'publisher'].includes(input.dataType) ? input.dataType : 'episodes';
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
const country = String(input.country || 'us').toLowerCase().trim();
// Apple's two chart endpoints have DIFFERENT hard caps, measured live cycle 424: the newer
// rss.marketingtools.apple.com feed 500s for any limit >100 (101/150/199/200 all fail, 100 is
// fine), while the older itunes.apple.com RSS Generator (the genre path) serves up to 200 and
// 400s at 250. Before this was measured, a chartCount of 101-200 on the overall chart made the
// whole run return 0 rows with only a warning, so the cap is now per-endpoint, not global.
const chartCountRequested = Math.max(1, Number(input.chartCount ?? 50));
// "shows" is Apple's Top Shows chart (podcasts.json); "episodes" is the separate Trending
// Episodes chart (podcast-episodes.json) — a genuinely different chart, not a view of the first.
const chartType = input.chartType === 'episodes' ? 'episodes' : 'shows';
if (input.chartType && !['shows', 'episodes'].includes(input.chartType)) {
  log.warning(`Unknown "chartType" value "${input.chartType}" — using "shows" (Apple's Top Shows chart). Valid values: shows, episodes.`);
}
// Only warn for a non-default value: the SDK fills schema defaults into the input, so
// `input.chartType` is "shows" even on a run that never mentioned it.
if (chartType !== 'shows' && input.dataType && input.dataType !== 'charts') {
  log.warning(`"chartType" only applies when "What to scrape" is "charts" — ignored for dataType "${input.dataType}".`);
}
// Apple's newer rss.marketingtools.apple.com chart endpoint has no genre filter (/genre=<id>/
// 404s, ?g= is ignored), but the older itunes.apple.com RSS Generator endpoint still honours
// one — verified live cycle 217 (e.g. genre=1303 returns a Comedy-only chart, distinct from the
// overall top chart). GOTCHA: an unrecognized genre id does NOT error — it silently falls back
// to the overall top chart (HTTP 200), so a typo would read as "genre X's top chart" when it's
// really just the front page. The whitelist below is load-bearing; never pass a raw value through.
const CHART_GENRE_IDS = {
  arts: 1301, business: 1321, comedy: 1303, education: 1304, fiction: 1483,
  government: 1511, healthFitness: 1512, history: 1487, kidsFamily: 1305,
  leisure: 1502, music: 1310, news: 1489, religionSpirituality: 1314,
  science: 1533, societyCulture: 1324, sports: 1545, technology: 1318,
  trueCrime: 1488, tvFilm: 1309,
};
let chartGenre = input.chartGenre && CHART_GENRE_IDS[input.chartGenre] ? input.chartGenre : null;
if (input.chartGenre && !chartGenre) log.warning(`Unknown "chartGenre" value "${input.chartGenre}" — ignored, using the overall top chart. Valid values: ${Object.keys(CHART_GENRE_IDS).join(', ')}.`);
// Only the shows chart has a genre-specific endpoint; there is no per-genre Trending Episodes
// feed. Dropped loudly rather than silently, so nobody pays for an "overall" chart they asked
// to have narrowed (same rule as the federal-register PI desk, cycle 412).
if (chartGenre && chartType === 'episodes') {
  log.warning(`"chartGenre" ("${chartGenre}") is ignored for chartType "episodes" — Apple publishes Trending Episodes only as one overall chart per storefront, with no genre breakdown. Returning the overall episode chart for "${country}".`);
  chartGenre = null;
}
const chartCount = Math.min(chartCountRequested, chartGenre ? 200 : 100);
if (chartCount < chartCountRequested) {
  log.warning(`"chartCount" ${chartCountRequested} exceeds Apple's cap for this chart (${chartGenre ? 200 : 100}) — fetching ${chartCount}. ${chartGenre ? '' : 'Apple\'s overall chart endpoint returns an error, not a shorter list, above 100.'}`);
}
const searchLimit = Math.min(Number(input.searchLimit ?? 10), 200);
// Apple's episode lookup API caps at 200 regardless of what's requested. Enabling
// useRssForFullArchive replaces that call with a direct fetch of the show's own RSS feed, which
// has no such cap (verified live: a real feed returned 2,977 items vs Apple's 200-episode ceiling)
// — so the input cap only needs raising in that mode.
const rssFullArchive = input.useRssForFullArchive === true;
const perPodcastEpisodes = Math.min(Number(input.maxEpisodesPerPodcast ?? 100), rssFullArchive ? 20000 : 200);
const perPodcastReviews = Math.min(Number(input.maxReviewsPerPodcast ?? 200), 500);
const maxPodcastsPerPublisher = Math.min(Number(input.maxPodcastsPerPublisher ?? 200), 200);
const maxResults = Math.min(Number(input.maxResults ?? 2000), 50000);
const sort = input.sort === 'mostHelpful' ? 'mostHelpful' : 'mostRecent';
const includePodcastInfo = input.includePodcastInfo !== false;
const minRating = input.minRating != null ? Number(input.minRating) : null;
const maxRating = input.maxRating != null ? Number(input.maxRating) : null;
const keyword = String(input.keyword ?? '').normalize('NFC').trim().toLowerCase() || null;
const minReleaseDate = input.minReleaseDate ? new Date(input.minReleaseDate) : null;
const maxReleaseDate = input.maxReleaseDate ? new Date(input.maxReleaseDate) : null;
if ((minReleaseDate && Number.isNaN(minReleaseDate.getTime())) || (maxReleaseDate && Number.isNaN(maxReleaseDate.getTime()))) {
  await Actor.fail('"minReleaseDate"/"maxReleaseDate" must be valid dates (YYYY-MM-DD or full ISO).');
}
const minDurationSeconds = input.minDurationSeconds != null ? Number(input.minDurationSeconds) : null;
const explicitFilter = ['all', 'clean', 'explicitOnly'].includes(input.explicitFilter) ? input.explicitFilter : 'all';

if (dataType !== 'charts' && !podcasts.length && !searchTerms.length) {
  await Actor.fail('Provide at least one podcast or publisher (Apple Podcasts show/artist URL, or numeric ID) in "podcasts", or at least one query in "searchTerms".');
}

// Many podcasts x many episodes/review-pages is strictly sequential (each request up to 30s +
// 2 retries, plus review-fingerprint retries), so a run can approach the platform timeout with
// work still queued. A hard kill there returns nothing to the customer even though partial
// results already exist in the dataset. Stop proactively with a safety margin and flush what's
// collected instead — same pattern as google-news-scraper / shopify-products-scraper.
const timeoutAt = Actor.getEnv().timeoutAt?.getTime() ?? null;
const TIME_BUDGET_MARGIN_MS = 45_000;
let timeBudgetExceeded = false;
function timeBudgetOk() {
  if (timeoutAt == null) return true;
  if (Date.now() >= timeoutAt - TIME_BUDGET_MARGIN_MS) { timeBudgetExceeded = true; return false; }
  return true;
}

let pushed = 0;
let unknownDurationKept = 0;
let unenrichedChartEntries = 0;
let rssItemsWithoutExplicit = 0;
let keepGoing = true;
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

const getJson = async (url, opts = {}) => JSON.parse((await gotScraping({ url, timeout: { request: 30000 }, retry: { limit: 2 }, ...opts })).body);

// Apple's review RSS is served by shards that disagree: for a given id the SAME url returns
// 50 reviews under one header fingerprint and an empty feed under another (see
// app-store-reviews-scraper / LEARNINGS cycle 8 — same endpoint, same behaviour for podcasts).
// So on an empty feed we retry the request under other fingerprints before believing there are
// no reviews. The lookup/search endpoints do NOT need this and are left as plain requests.
const RSS_VARIANTS = [
  {},
  { headers: { 'user-agent': 'curl/8.5.0' } },
  { headerGeneratorOptions: { browsers: ['firefox'], devices: ['desktop'], operatingSystems: ['windows'] } },
  { headerGeneratorOptions: { browsers: ['safari'], devices: ['mobile'], operatingSystems: ['ios'] } },
];
let preferredVariant = 0; // the fingerprint that last worked; tried first to keep requests at 1/page
async function fetchEntries(url, rotate = true) {
  const order = rotate
    ? [preferredVariant, ...RSS_VARIANTS.keys()].filter((v, i, a) => a.indexOf(v) === i)
    : [preferredVariant]; // mid-pagination an empty feed just means "no more reviews"
  let lastError = null;
  for (const i of order) {
    try {
      let entries = (await getJson(url, RSS_VARIANTS[i])).feed?.entry ?? [];
      if (!Array.isArray(entries)) entries = [entries];
      if (entries.length) { preferredVariant = i; return entries; }
    } catch (e) { lastError = e; }
  }
  if (lastError) throw lastError;
  return [];
}

const lbl = (o) => (o && typeof o === 'object' && 'label' in o ? o.label : o ?? null);
// Apple Podcasts URLs and App Store URLs share the /id<digits> shape, so does a bare ID.
// Publisher/artist URLs (…/artist/the-new-york-times/121664449) have no "id" prefix, just a
// trailing numeric segment — checked last so it never overrides the "id<digits>" show-URL match.
// GOTCHA (found cycle 401, adding direct-RSS-feed support): that trailing-numeric-segment
// fallback used to run on ANY string, so a non-Apple feed URL with a numeric path segment (e.g.
// https://feeds.npr.org/500005/podcast.xml) was silently misread as Apple ID 500005 instead of
// being treated as a feed URL. It's gated to apple.com hosts now.
const parseId = (s) => (s.match(/id(\d{6,})/)?.[1] || s.match(/^\d{6,}$/)?.[0] || (/apple\.com/i.test(s) ? s.match(/\/(\d{6,})(?:[/?]|$)/)?.[1] : null) || null);

function podcastRow(p) {
  return {
    type: 'podcast',
    collectionId: p.collectionId ?? null,
    podcastName: p.collectionName ?? p.trackName ?? null,
    artistName: p.artistName ?? null,
    podcastUrl: p.collectionViewUrl ?? p.trackViewUrl ?? null,
    feedUrl: p.feedUrl ?? null,
    primaryGenre: p.primaryGenreName ?? null,
    genres: p.genres?.map?.((g) => (typeof g === 'string' ? g : g.name)) ?? null,
    episodeCount: p.trackCount ?? null,
    latestReleaseDate: p.releaseDate ?? null,
    explicit: p.collectionExplicitness === 'explicit' || p.trackExplicitness === 'explicit',
    contentAdvisoryRating: p.contentAdvisoryRating ?? null,
    artworkUrl: p.artworkUrl600 ?? p.artworkUrl100 ?? null,
    country: p.country ?? null,
  };
}

function episodeRow(e, info) {
  return {
    type: 'episode',
    collectionId: e.collectionId ?? null,
    podcastName: e.collectionName ?? null,
    episodeId: e.trackId ?? null,
    title: e.trackName ?? null,
    episodeNumber: e.episodeNumber ?? null,
    seasonNumber: e.seasonNumber ?? null,
    releaseDate: e.releaseDate ?? null,
    durationMs: e.trackTimeMillis ?? null,
    durationMinutes: e.trackTimeMillis ? Math.round(e.trackTimeMillis / 60000) : null,
    description: e.description ?? null,
    shortDescription: e.shortDescription ?? null,
    episodeUrl: e.episodeUrl ?? null, // direct audio file
    episodeFileExtension: e.episodeFileExtension ?? null,
    episodeContentType: e.episodeContentType ?? null,
    episodeGuid: e.episodeGuid ?? null,
    explicit: e.contentAdvisoryRating === 'Explicit',
    artworkUrl: e.artworkUrl600 ?? e.artworkUrl160 ?? null,
    episodePageUrl: e.trackViewUrl ?? null,
    feedUrl: e.feedUrl ?? null,
    episodeType: null,
    showNotesHtml: null,
    audioFileSize: null,
    keywords: null,
    transcriptUrl: null,
    source: 'itunes',
    ...(info || {}),
  };
}

// itunes:explicit is "yes"/"no" in the spec but "true"/"false"/"explicit"/"clean" all appear in
// real feeds. Returns null (not false) when the tag is absent, so a missing per-episode tag can
// fall back to the show-level one instead of silently reading as "not explicit" — see the
// channelExplicit argument of rssEpisodeRow.
function parseItunesExplicit(s) {
  const t = String(s || '').trim().toLowerCase();
  if (!t) return null;
  return ['yes', 'true', 'explicit'].includes(t);
}

// itunes:duration is "HH:MM:SS", "MM:SS", or bare seconds — all three appear in real feeds.
function parseItunesDuration(s) {
  const t = String(s || '').trim();
  if (!t) return null;
  if (/^\d+$/.test(t)) return Number(t) * 1000;
  const parts = t.split(':').map(Number);
  if (!parts.length || parts.some(Number.isNaN)) return null;
  return parts.reduce((secs, p) => secs * 60 + p, 0) * 1000;
}

// Built from a show's own RSS 2.0 / Podcast-namespace feed (useRssForFullArchive), not Apple's
// lookup API — this is the only way to get episodes beyond Apple's ~200-episode cap, plus fields
// Apple's JSON never exposes at all (episodeType, full HTML show notes, file size, transcript).
function rssEpisodeRow($, el, collectionId, info, channelExplicit = null) {
  const $el = $(el);
  const itemExplicit = parseItunesExplicit($el.find('itunes\\:explicit').text());
  if (itemExplicit == null) rssItemsWithoutExplicit += 1;
  const enclosure = $el.find('enclosure');
  const episodeUrl = enclosure.attr('url')?.split('?')[0] || enclosure.attr('url') || null;
  const durationMs = parseItunesDuration($el.find('itunes\\:duration').text());
  const pubDateRaw = $el.find('pubDate').text().trim();
  const releaseDate = pubDateRaw ? new Date(pubDateRaw) : null;
  return {
    type: 'episode',
    collectionId,
    podcastName: info?.podcastName ?? null,
    episodeId: null,
    title: $el.find('title').text().trim() || null,
    episodeNumber: $el.find('itunes\\:episode').text().trim() || null,
    seasonNumber: $el.find('itunes\\:season').text().trim() || null,
    releaseDate: releaseDate && !Number.isNaN(releaseDate.getTime()) ? releaseDate.toISOString() : null,
    durationMs,
    durationMinutes: durationMs ? Math.round(durationMs / 60000) : null,
    description: $el.find('description').text().trim() || null,
    shortDescription: $el.find('itunes\\:subtitle').text().trim() || null,
    episodeUrl: enclosure.attr('url') || null,
    episodeFileExtension: episodeUrl ? (episodeUrl.split('.').pop() || null) : null,
    episodeContentType: enclosure.attr('type') || null,
    episodeGuid: $el.find('guid').text().trim() || null,
    explicit: itemExplicit ?? channelExplicit ?? false,
    artworkUrl: $el.find('itunes\\:image').attr('href') || info?.artworkUrl || null,
    episodePageUrl: $el.find('link').text().trim() || null,
    feedUrl: info?.feedUrl ?? null,
    episodeType: $el.find('itunes\\:episodeType').text().trim() || null,
    showNotesHtml: $el.find('content\\:encoded').text().trim() || $el.find('description').text().trim() || null,
    audioFileSize: Number(enclosure.attr('length')) || null,
    keywords: $el.find('itunes\\:keywords').text().trim() || null,
    transcriptUrl: $el.find('podcast\\:transcript').attr('url') || null,
    source: 'rss',
  };
}

async function scrapeRssFeed(feedUrl, collectionId, info) {
  const res = await gotScraping({ url: feedUrl, timeout: { request: 30000 }, retry: { limit: 2 } });
  const $ = cheerio.load(res.body, { xml: true });
  const channelExplicit = parseItunesExplicit($('channel').first().find('> itunes\\:explicit').first().text());
  return $('item').map((_, el) => rssEpisodeRow($, el, collectionId, info, channelExplicit)).get();
}

function reviewPassesFilters(item) {
  if (minRating != null && item.rating < minRating) return false;
  if (maxRating != null && item.rating > maxRating) return false;
  if (keyword && !`${item.title || ''} ${item.content || ''}`.normalize('NFC').toLowerCase().includes(keyword)) return false;
  return true;
}

// Apple's episode lookup only ever returns the most recent `maxEpisodesPerPodcast` (hard cap
// 200) episodes — these filters narrow *within* that recent window, they cannot reach further
// back into a show's archive than Apple already handed us. Documented in the README/schema.
function episodePassesFilters(e) {
  if (minReleaseDate || maxReleaseDate) {
    const d = e.releaseDate ? new Date(e.releaseDate) : null;
    if (!d || Number.isNaN(d.getTime())) return false;
    if (minReleaseDate && d < minReleaseDate) return false;
    if (maxReleaseDate && d > maxReleaseDate) return false;
  }
  // Apple's own lookup API omits trackTimeMillis for a large, seemingly random share of
  // episodes regardless of actual length (measured ~50% null on a real 20-episode sample,
  // full-length flagship episodes included, not just short ones) — so an unknown duration is
  // NOT treated as "short" here. Filtering nulls out would silently drop about half of a show's
  // real full-length episodes under the "exclude trailers" feature. Unknown durations are kept
  // and reported once via a status message instead.
  if (minDurationSeconds != null && e.durationMs != null && e.durationMs < minDurationSeconds * 1000) return false;
  if (explicitFilter === 'clean' && e.explicit) return false;
  if (explicitFilter === 'explicitOnly' && !e.explicit) return false;
  return true;
}

// Podcast-level metadata attached to every episode/review row when includePodcastInfo is on.
const infoCache = new Map();
async function getPodcastInfo(id) {
  if (!includePodcastInfo) return null;
  if (infoCache.has(id)) return infoCache.get(id);
  let info = null;
  try {
    const p = (await getJson(`https://itunes.apple.com/lookup?id=${id}&country=${country}`)).results?.[0];
    if (p) {
      info = {
        podcastName: p.collectionName ?? p.trackName ?? null,
        artistName: p.artistName ?? null,
        podcastUrl: p.collectionViewUrl ?? p.trackViewUrl ?? null,
        feedUrl: p.feedUrl ?? null,
        primaryGenre: p.primaryGenreName ?? null,
        episodeCount: p.trackCount ?? null,
      };
    }
  } catch (e) { log.debug(`lookup failed for ${id}: ${e.message}`); }
  infoCache.set(id, info);
  return info;
}

// Needed for useRssForFullArchive when includePodcastInfo is off, since the feed URL still has
// to come from somewhere — getPodcastInfo already carries it when podcast info is on.
const feedUrlCache = new Map();
async function getFeedUrlOnly(id) {
  if (feedUrlCache.has(id)) return feedUrlCache.get(id);
  let feedUrl = null;
  try { feedUrl = (await getJson(`https://itunes.apple.com/lookup?id=${id}&country=${country}`)).results?.[0]?.feedUrl ?? null; }
  catch (e) { log.debug(`Feed URL lookup failed for ${id}: ${e.message}`); }
  feedUrlCache.set(id, feedUrl);
  return feedUrl;
}

async function pushEpisodeRows(rows) {
  let got = 0;
  for (const row of rows) {
    if (!keepGoing || got >= perPodcastEpisodes) break;
    got += 1;
    if (minDurationSeconds != null && row.durationMs == null) unknownDurationKept += 1;
    if (!episodePassesFilters(row)) continue;
    keepGoing = await pushResult({ ...row, scrapedAt: new Date().toISOString() });
  }
  return got;
}

// Trending-Episodes chart support. The chart feed itself carries only name/artist/artwork/url,
// so each entry is enriched from Apple's lookup API. The episode ID is NOT independently
// addressable there (verified live cycle 424: lookup?id=<episodeId> returns resultCount 0, with
// or without entity=podcastEpisode) — the only way in is to look up the parent SHOW and match on
// trackId. One request per show, cached, because a single show can hold several chart slots
// (The Daily held #1 and #8 on the 2026-09-17 US chart).
const showEpisodesCache = new Map();
async function getShowEpisodeBundle(showId) {
  if (showEpisodesCache.has(showId)) return showEpisodesCache.get(showId);
  const bundle = { info: null, episodes: new Map() };
  try {
    const url = `https://itunes.apple.com/lookup?id=${showId}&country=${country}&entity=podcastEpisode&limit=200`;
    const results = (await getJson(url)).results ?? [];
    const show = results.find((r) => r.wrapperType === 'track' && r.kind === 'podcast') ?? null;
    if (show && includePodcastInfo) {
      bundle.info = {
        podcastName: show.collectionName ?? show.trackName ?? null,
        artistName: show.artistName ?? null,
        podcastUrl: show.collectionViewUrl ?? show.trackViewUrl ?? null,
        feedUrl: show.feedUrl ?? null,
        primaryGenre: show.primaryGenreName ?? null,
        episodeCount: show.trackCount ?? null,
      };
    }
    for (const r of results) {
      if (r.wrapperType === 'podcastEpisode' && r.trackId != null) bundle.episodes.set(String(r.trackId), r);
    }
  } catch (e) { log.debug(`Episode lookup failed for chart show ${showId}: ${e.message}`); }
  showEpisodesCache.set(showId, bundle);
  return bundle;
}

async function scrapeEpisodes(id) {
  const info = includePodcastInfo ? await getPodcastInfo(id) : null;
  let rows = null;
  if (rssFullArchive) {
    const feedUrl = info?.feedUrl ?? await getFeedUrlOnly(id);
    if (feedUrl) {
      try { rows = await scrapeRssFeed(feedUrl, Number(id), info ?? { feedUrl }); }
      catch (e) { log.warning(`RSS full-archive fetch failed for podcast ${id} (${feedUrl}): ${e.message} — falling back to Apple's lookup API (max 200 episodes).`); }
    } else {
      log.warning(`No RSS feed URL found for podcast ${id} — falling back to Apple's lookup API (max 200 episodes).`);
    }
  }
  if (rows == null) {
    // One call returns the podcast record plus up to `limit` most recent episodes (hard cap 200).
    const url = `https://itunes.apple.com/lookup?id=${id}&country=${country}&entity=podcastEpisode&limit=${Math.min(perPodcastEpisodes, 200)}`;
    let results = [];
    try { results = (await getJson(url)).results ?? []; }
    catch (e) { log.warning(`Episode lookup failed for ${id}: ${e.message}`); return 0; }
    rows = results.filter((r) => r.wrapperType === 'podcastEpisode').map((e) => episodeRow(e, info));
  }
  return pushEpisodeRows(rows);
}

// Podcast shows without an Apple presence (or with one the caller didn't bother looking up) can
// still be scraped by pasting the RSS feed URL directly into "podcasts" — the feed is the only
// source of truth needed for episodes, so no Apple lookup happens at all. Only dataType
// "episodes" is supported this way: reviews/charts/search/publisher all require an Apple ID.
async function scrapeEpisodesFromFeed(feedUrl) {
  let $;
  try {
    const res = await gotScraping({ url: feedUrl, timeout: { request: 30000 }, retry: { limit: 2 } });
    $ = cheerio.load(res.body, { xml: true });
  } catch (e) {
    log.warning(`Could not fetch RSS feed "${feedUrl}": ${e.message}`);
    return 0;
  }
  const channel = $('channel').first();
  const info = includePodcastInfo ? {
    podcastName: channel.find('> title').first().text().trim() || null,
    artistName: channel.find('itunes\\:author').first().text().trim() || null,
    podcastUrl: channel.find('> link').first().text().trim() || null,
    feedUrl,
    primaryGenre: null,
    episodeCount: null,
    artworkUrl: channel.find('itunes\\:image').attr('href') || null,
  } : null;
  const channelExplicit = parseItunesExplicit(channel.find('> itunes\\:explicit').first().text());
  const rows = $('item').map((_, el) => rssEpisodeRow($, el, null, info, channelExplicit)).get();
  return pushEpisodeRows(rows);
}

async function scrapeReviews(id) {
  const info = await getPodcastInfo(id);
  let got = 0;
  let filteredOut = 0;
  for (let page = 1; page <= 10 && got < perPodcastReviews && keepGoing; page++) {
    if (!timeBudgetOk()) { log.warning('Approaching the run timeout — stopping early and returning what has been collected so far.'); keepGoing = false; break; }
    let entries = [];
    try {
      const url = `https://itunes.apple.com/${country}/rss/customerreviews/id=${id}/sortBy=${sort}/page=${page}/json`;
      entries = await fetchEntries(url, got === 0);
    } catch (e) { log.warning(`review page ${page} failed for ${id}: ${e.message}`); break; }
    if (!entries.length) break;
    for (const e of entries) {
      if (got >= perPodcastReviews) break;
      const item = {
        type: 'review',
        collectionId: Number(id),
        reviewId: lbl(e.id),
        title: lbl(e.title),
        content: lbl(e.content),
        rating: Number(lbl(e['im:rating'])) || null,
        author: lbl(e.author?.name),
        authorUrl: lbl(e.author?.uri),
        updatedAt: lbl(e.updated),
        voteSum: Number(lbl(e['im:voteSum'])) || 0,
        voteCount: Number(lbl(e['im:voteCount'])) || 0,
        country,
        ...(info || {}),
        scrapedAt: new Date().toISOString(),
      };
      got += 1;
      if (!reviewPassesFilters(item)) { filteredOut += 1; continue; }
      keepGoing = await pushResult(item);
      if (!keepGoing) break;
    }
  }
  const capReached = got >= perPodcastReviews;
  return { got, filteredOut, capReached };
}

// ---- resolve targets -------------------------------------------------------
const ids = [];
const seenIds = new Set();
const addId = (id) => { if (id && !seenIds.has(id)) { seenIds.add(id); ids.push(id); } };
// A string that isn't an Apple Podcasts URL/ID but does look like a URL is treated as a direct
// RSS feed link (verified live cycle 401: competitors' `rssFeeds`-style input is a real, requested
// feature for shows not indexed by Apple, or when the caller already has the feed URL in hand).
const rawFeeds = [];
const seenFeeds = new Set();
for (const p of podcasts) {
  const id = parseId(p);
  if (id) { addId(id); continue; }
  if (/^https?:\/\//i.test(p)) { if (!seenFeeds.has(p)) { seenFeeds.add(p); rawFeeds.push(p); } }
  else log.warning(`Cannot parse a podcast ID from "${p}" — use an Apple Podcasts URL (…/id1434243584), the numeric ID, or a direct RSS feed URL.`);
}
if (rawFeeds.length && dataType !== 'episodes') {
  log.warning(`${rawFeeds.length} direct RSS feed URL(s) given, but "What to scrape" is "${dataType}" — a raw feed only contains episode data, so direct feed URLs are only usable with dataType "episodes". Skipping: ${rawFeeds.slice(0, 3).join(', ')}${rawFeeds.length > 3 ? ', …' : ''}`);
  rawFeeds.length = 0;
}

const searchHits = [];
const emptySearches = [];
for (const term of searchTerms) {
  if (!keepGoing) break;
  if (!timeBudgetOk()) { log.warning('Approaching the run timeout — stopping early and returning what has been collected so far.'); break; }
  try {
    const url = `https://itunes.apple.com/search?term=${encodeURIComponent(term)}&media=podcast&country=${country}&limit=${searchLimit}`;
    const results = (await getJson(url)).results ?? [];
    if (!results.length) { emptySearches.push(term); log.warning(`Search "${term}" returned no podcasts in storefront "${country}".`); continue; }
    log.info(`Search "${term}": ${results.length} podcasts.`);
    for (const p of results) { searchHits.push({ term, p }); addId(String(p.collectionId)); }
  } catch (e) { log.warning(`Search "${term}" failed: ${e.message}`); }
}

// ---- run -------------------------------------------------------------------
const emptyIds = [];
const depthCapped = [];
if (dataType === 'charts') {
  // Rank comes from array order in all cases.
  const url = chartGenre
    ? `https://itunes.apple.com/${country}/rss/toppodcasts/limit=${chartCount}/genre=${CHART_GENRE_IDS[chartGenre]}/json`
    : `https://rss.marketingtools.apple.com/api/v2/${country}/podcasts/top/${chartCount}/${chartType === 'episodes' ? 'podcast-episodes' : 'podcasts'}.json`;
  let results = [];
  try {
    if (chartGenre) {
      const entries = (await getJson(url)).feed?.entry ?? [];
      // Normalize the older endpoint's Atom-ish shape to the same {id, name, artistName, url,
      // genres, contentAdvisoryRating, artworkUrl100} shape the marketingtools endpoint returns,
      // so the rest of this loop (including the includePodcastInfo lookup) is untouched below.
      results = entries.map((e) => ({
        id: e.id?.attributes?.['im:id'] ?? null,
        name: e['im:name']?.label ?? null,
        artistName: e['im:artist']?.label ?? null,
        url: e.link?.attributes?.href ?? null,
        genres: e.category?.attributes?.label ? [{ name: e.category.attributes.label }] : [],
        contentAdvisoryRating: null,
        artworkUrl100: e['im:image']?.[e['im:image'].length - 1]?.label ?? null,
      }));
    } else {
      results = (await getJson(url)).feed?.results ?? [];
    }
  } catch (e) {
    const msg = e instanceof SyntaxError
      ? `storefront "${country}" is not a valid Apple Podcasts country code (Apple returned an HTML error page, not chart data) — use a 2-letter code like "us", "gb", "de".`
      : `Chart fetch failed for storefront "${country}": ${e.message}`;
    log.warning(msg);
  }
  for (let i = 0; i < results.length; i++) {
    if (!keepGoing) break;
    if (!timeBudgetOk()) { log.warning('Approaching the run timeout — stopping early and returning what has been collected so far.'); break; }
    const r = results[i];
    const chartRank = i + 1;
    if (chartType === 'episodes') {
      // Chart entry URLs look like …/podcast/<slug>/id<showId>?i=<episodeId>.
      const showId = r.url?.match(/\/id(\d{6,})/)?.[1] ?? null;
      const episodeId = r.url?.match(/[?&]i=(\d+)/)?.[1] ?? null;
      const bundle = showId ? await getShowEpisodeBundle(showId) : { info: null, episodes: new Map() };
      const hit = episodeId ? bundle.episodes.get(episodeId) : null;
      // Apple-exclusive shows (e.g. "Apple News Today", feedUrl null) expose NO episodes through
      // the lookup API at all, so a chart slot can't always be enriched — measured 19/20 enriched
      // on the 2026-09-17 US chart. The unenriched entry is still emitted, with the same key
      // rectangle and the chart's own name/artwork/page URL, so chart ranks never have holes.
      // Keep the key rectangle identical whether or not the lookup succeeded: when podcast info
      // is on but the show wasn't in the index, every info key is still present (null), with
      // artistName filled from the chart entry, which always carries it.
      const fallbackInfo = includePodcastInfo
        ? (bundle.info ?? { podcastName: null, artistName: r.artistName ?? null, podcastUrl: null, feedUrl: null, primaryGenre: null, episodeCount: null })
        : null;
      const row = hit ? episodeRow(hit, bundle.info) : {
        ...episodeRow({}, fallbackInfo),
        collectionId: showId ? Number(showId) : null,
        episodeId: episodeId ? Number(episodeId) : null,
        title: r.name ?? null,
        artworkUrl: r.artworkUrl100 ?? null,
        episodePageUrl: r.url ?? null,
        source: 'chart',
      };
      if (!hit) unenrichedChartEntries += 1;
      // Same filters as a normal episode run, applied before charging so nobody pays for rows
      // they asked to exclude. Ranks can therefore have gaps — documented in the README.
      if (minDurationSeconds != null && row.durationMs == null) unknownDurationKept += 1;
      if (!episodePassesFilters(row)) continue;
      keepGoing = await pushResult({ ...row, chartRank, scrapedAt: new Date().toISOString() });
      continue;
    }
    let full = null;
    if (includePodcastInfo) {
      try { full = (await getJson(`https://itunes.apple.com/lookup?id=${r.id}&country=${country}`)).results?.[0] ?? null; }
      catch (e) { log.debug(`lookup failed for chart entry ${r.id}: ${e.message}`); }
    }
    const row = full ? podcastRow(full) : {
      type: 'podcast',
      collectionId: Number(r.id) || null,
      podcastName: r.name ?? null,
      artistName: r.artistName ?? null,
      podcastUrl: r.url ?? null,
      feedUrl: null,
      primaryGenre: r.genres?.[0]?.name ?? null,
      genres: r.genres?.map?.((g) => g.name) ?? null,
      episodeCount: null,
      latestReleaseDate: null,
      explicit: r.contentAdvisoryRating === 'Explict' || r.contentAdvisoryRating === 'Explicit',
      contentAdvisoryRating: r.contentAdvisoryRating ?? null,
      artworkUrl: r.artworkUrl100 ?? null,
      country,
    };
    keepGoing = await pushResult({ ...row, chartRank, scrapedAt: new Date().toISOString() });
  }
  if (!results.length) emptyIds.push(country);
} else if (dataType === 'podcasts') {
  // Search results already carry the full podcast record; explicit IDs need one lookup each.
  const pushedFromSearch = new Set();
  for (const { term, p } of searchHits) {
    if (!keepGoing) break;
    pushedFromSearch.add(String(p.collectionId));
    keepGoing = await pushResult({ ...podcastRow(p), searchTerm: term, scrapedAt: new Date().toISOString() });
  }
  for (const id of ids) {
    if (!keepGoing) break;
    if (!timeBudgetOk()) { log.warning('Approaching the run timeout — stopping early and returning what has been collected so far.'); break; }
    if (pushedFromSearch.has(id)) continue;
    try {
      const p = (await getJson(`https://itunes.apple.com/lookup?id=${id}&country=${country}`)).results?.[0];
      if (!p) { emptyIds.push(id); log.warning(`No podcast found for ID ${id} in storefront "${country}".`); continue; }
      keepGoing = await pushResult({ ...podcastRow(p), scrapedAt: new Date().toISOString() });
    } catch (e) { log.warning(`Lookup failed for ${id}: ${e.message}`); }
  }
} else if (dataType === 'publisher') {
  // One lookup per publisher/artist ID returns every podcast they publish (no per-show ID needed).
  for (const id of ids) {
    if (!keepGoing) break;
    if (!timeBudgetOk()) { log.warning('Approaching the run timeout — stopping early and returning what has been collected so far.'); break; }
    try {
      const url = `https://itunes.apple.com/lookup?id=${id}&country=${country}&entity=podcast&limit=${maxPodcastsPerPublisher}`;
      const results = (await getJson(url)).results ?? [];
      const shows = results.filter((r) => r.wrapperType === 'track' && r.kind === 'podcast');
      if (!shows.length) {
        emptyIds.push(id);
        log.warning(`No podcasts found for publisher ID ${id} in storefront "${country}" — check this is an Apple Podcasts artist/publisher ID, not a show ID.`);
        continue;
      }
      for (const p of shows) {
        if (!keepGoing) break;
        keepGoing = await pushResult({ ...podcastRow(p), publisherId: Number(id), scrapedAt: new Date().toISOString() });
      }
    } catch (e) { log.warning(`Publisher lookup failed for ${id}: ${e.message}`); }
  }
} else {
  for (const id of ids) {
    if (!keepGoing) break;
    if (!timeBudgetOk()) { log.warning('Approaching the run timeout — stopping early and returning what has been collected so far.'); break; }
    const before = pushed;
    let got;
    if (dataType === 'reviews') {
      const r = await scrapeReviews(id);
      got = r.got;
      if (r.capReached && r.filteredOut > 0) {
        log.warning(
          `Podcast ${id}: scanned the maxReviewsPerPodcast limit of ${perPodcastReviews} review(s) and ${r.filteredOut} of them `
          + `were excluded by the minRating/maxRating/keyword filter. The cap counts reviews scanned, before filtering `
          + `— raise maxReviewsPerPodcast to search deeper.`,
        );
        depthCapped.push(id);
      }
    } else {
      got = await scrapeEpisodes(id);
    }
    log.info(`${id}: ${got} ${dataType} fetched, ${pushed - before} kept after filters.`);
    if (got === 0) {
      emptyIds.push(id);
      log.warning(dataType === 'reviews'
        ? `Apple's review feed for podcast ${id} in storefront "${country}" is empty (that is Apple's data, not a scrape failure) — try another "country", or check the ID is an Apple Podcasts ID.`
        : `Apple returned no episodes for podcast ${id} in storefront "${country}" — check the ID is an Apple Podcasts ID and that the show is available in that storefront.`);
    }
  }
  if (dataType === 'episodes') {
    for (const feedUrl of rawFeeds) {
      if (!keepGoing) break;
      if (!timeBudgetOk()) { log.warning('Approaching the run timeout — stopping early and returning what has been collected so far.'); break; }
      const before = pushed;
      const got = await scrapeEpisodesFromFeed(feedUrl);
      log.info(`${feedUrl}: ${got} episodes fetched, ${pushed - before} kept after filters.`);
      if (got === 0) {
        emptyIds.push(feedUrl);
        log.warning(`RSS feed "${feedUrl}" returned no episodes — check it's a valid podcast RSS feed URL.`);
      }
    }
  }
}

if (unknownDurationKept > 0) {
  log.warning(`minDurationSeconds is set: ${unknownDurationKept} episode(s) had no duration in Apple's own data and were kept rather than dropped, since an unknown duration is not evidence of a short episode.`);
}
if (rssItemsWithoutExplicit > 0 && explicitFilter !== 'all') {
  log.warning(`explicitFilter is set while "useRssForFullArchive" is on: ${rssItemsWithoutExplicit} episode(s) carried no per-episode <itunes:explicit> tag, so the show-level flag from the feed was used (or false when the feed has none). A feed's own flag can disagree with Apple's Store rating for the same episode — if this run returned fewer rows than expected, turn "useRssForFullArchive" off to filter on Apple's rating instead.`);
}
if (unenrichedChartEntries > 0) {
  log.warning(`${unenrichedChartEntries} chart entry/entries could not be enriched from Apple's lookup API (typically Apple-exclusive or subscriber-only shows, which expose no episode list). They are still in the dataset with chartRank, title and episodePageUrl, and source "chart" instead of "itunes".`);
}
log.info(`Done. Pushed ${pushed} ${dataType === 'podcasts' || dataType === 'publisher' ? 'podcasts' : dataType}.`);
const timeBudgetNote = timeBudgetExceeded
  ? ' Stopped early: approaching the run time limit — reduce the number of podcasts/searchTerms or maxEpisodesPerPodcast/maxReviewsPerPodcast to get a complete run.'
  : '';
const episodeFiltersSet = [
  explicitFilter !== 'all' ? `explicitFilter ("${explicitFilter}")` : null,
  minDurationSeconds != null ? `minDurationSeconds (${minDurationSeconds})` : null,
  input.minReleaseDate ? `minReleaseDate (${input.minReleaseDate})` : null,
  input.maxReleaseDate ? `maxReleaseDate (${input.maxReleaseDate})` : null,
].filter(Boolean);
const emptySourceLabel = (list) => (list.some((x) => /^https?:\/\//i.test(x))
  ? `no episodes found for: ${list.join(', ')}`
  : `Apple returned nothing for: ${list.join(', ')} in storefront "${country}"`);
if (pushed === 0 && timeBudgetExceeded) {
  await Actor.setStatusMessage(`No results before the run approached its time limit.${timeBudgetNote}`);
} else if (pushed === 0) {
  const why = emptyIds.length
    ? emptySourceLabel(emptyIds)
    : emptySearches.length
      ? `your search terms matched no podcasts in storefront "${country}": ${emptySearches.join(', ')}`
      : depthCapped.length
        ? `maxReviewsPerPodcast (${perPodcastReviews}) was hit before any review passed your minRating/maxRating/keyword filter for: ${depthCapped.join(', ')} — raise maxReviewsPerPodcast to search deeper`
        : dataType === 'reviews' && (keyword || minRating != null || maxRating != null)
          ? 'every review Apple returned was removed by your minRating/maxRating/keyword filters'
          : dataType === 'charts' && chartType === 'episodes' && episodeFiltersSet.length
            ? `every entry on the Trending Episodes chart for storefront "${country}" was removed by your ${episodeFiltersSet.join(' / ')} filter(s)`
            : 'no valid podcast IDs could be parsed from your input';
  await Actor.setStatusMessage(`No results — ${why}. See the log for details.`);
} else if (depthCapped.length) {
  await Actor.setStatusMessage(`Pushed ${pushed} results. maxReviewsPerPodcast (${perPodcastReviews}) was hit while filtering: ${depthCapped.join(', ')} — some matching reviews may sit deeper in the feed; raise maxReviewsPerPodcast to search further.${timeBudgetNote}`);
} else if (emptyIds.length || timeBudgetExceeded) {
  await Actor.setStatusMessage(`Pushed ${pushed} results.${emptyIds.length ? ` ${emptySourceLabel(emptyIds)}.` : ''}${timeBudgetNote}`);
}

// Fires after every row is already pushed and charged, so a slow or failing webhook can never
// affect the result set or the bill — best-effort only, one attempt, short timeout, failures are
// a warning not a thrown error.
if (webhookUrl) {
  const env = Actor.getEnv();
  const payload = {
    actorRunId: env.actorRunId ?? null,
    defaultDatasetId: env.defaultDatasetId ?? null,
    finishedAt: new Date().toISOString(),
    dataType,
    pushed,
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

await Actor.exit();
