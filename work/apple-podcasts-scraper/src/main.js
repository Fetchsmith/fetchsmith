import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';

await Actor.init();
const input = (await Actor.getInput()) ?? {};
const podcasts = (input.podcasts ?? []).map(String).filter(Boolean);
const searchTerms = (input.searchTerms ?? []).map(String).filter(Boolean);
const dataType = ['episodes', 'reviews', 'podcasts'].includes(input.dataType) ? input.dataType : 'episodes';
const country = String(input.country || 'us').toLowerCase().trim();
const searchLimit = Math.min(Number(input.searchLimit ?? 10), 200);
const perPodcastEpisodes = Math.min(Number(input.maxEpisodesPerPodcast ?? 100), 200);
const perPodcastReviews = Math.min(Number(input.maxReviewsPerPodcast ?? 200), 500);
const maxResults = Math.min(Number(input.maxResults ?? 2000), 50000);
const sort = input.sort === 'mostHelpful' ? 'mostHelpful' : 'mostRecent';
const includePodcastInfo = input.includePodcastInfo !== false;
const minRating = input.minRating != null ? Number(input.minRating) : null;
const maxRating = input.maxRating != null ? Number(input.maxRating) : null;
const keyword = input.keyword ? String(input.keyword).toLowerCase() : null;

if (!podcasts.length && !searchTerms.length) {
  await Actor.fail('Provide at least one podcast (Apple Podcasts URL or numeric ID) in "podcasts", or at least one query in "searchTerms".');
}

let pushed = 0;
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
const parseId = (s) => (s.match(/id(\d{6,})/)?.[1] || s.match(/^\d{6,}$/)?.[0] || null);

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
    ...(info || {}),
  };
}

function reviewPassesFilters(item) {
  if (minRating != null && item.rating < minRating) return false;
  if (maxRating != null && item.rating > maxRating) return false;
  if (keyword && !`${item.title || ''} ${item.content || ''}`.toLowerCase().includes(keyword)) return false;
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

async function scrapeEpisodes(id) {
  // One call returns the podcast record plus up to `limit` most recent episodes.
  const url = `https://itunes.apple.com/lookup?id=${id}&country=${country}&entity=podcastEpisode&limit=${perPodcastEpisodes}`;
  let results = [];
  try { results = (await getJson(url)).results ?? []; }
  catch (e) { log.warning(`Episode lookup failed for ${id}: ${e.message}`); return 0; }
  const eps = results.filter((r) => r.wrapperType === 'podcastEpisode');
  const info = includePodcastInfo ? await getPodcastInfo(id) : null;
  let got = 0;
  for (const e of eps) {
    if (!keepGoing || got >= perPodcastEpisodes) break;
    got += 1;
    keepGoing = await pushResult({ ...episodeRow(e, info), scrapedAt: new Date().toISOString() });
  }
  return got;
}

async function scrapeReviews(id) {
  const info = await getPodcastInfo(id);
  let got = 0;
  for (let page = 1; page <= 10 && got < perPodcastReviews && keepGoing; page++) {
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
      if (!reviewPassesFilters(item)) continue;
      keepGoing = await pushResult(item);
      if (!keepGoing) break;
    }
  }
  return got;
}

// ---- resolve targets -------------------------------------------------------
const ids = [];
const seenIds = new Set();
const addId = (id) => { if (id && !seenIds.has(id)) { seenIds.add(id); ids.push(id); } };
for (const p of podcasts) {
  const id = parseId(p);
  if (id) addId(id);
  else log.warning(`Cannot parse a podcast ID from "${p}" — use an Apple Podcasts URL (…/id1434243584) or the numeric ID.`);
}

const searchHits = [];
const emptySearches = [];
for (const term of searchTerms) {
  if (!keepGoing) break;
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
if (dataType === 'podcasts') {
  // Search results already carry the full podcast record; explicit IDs need one lookup each.
  const pushedFromSearch = new Set();
  for (const { term, p } of searchHits) {
    if (!keepGoing) break;
    pushedFromSearch.add(String(p.collectionId));
    keepGoing = await pushResult({ ...podcastRow(p), searchTerm: term, scrapedAt: new Date().toISOString() });
  }
  for (const id of ids) {
    if (!keepGoing) break;
    if (pushedFromSearch.has(id)) continue;
    try {
      const p = (await getJson(`https://itunes.apple.com/lookup?id=${id}&country=${country}`)).results?.[0];
      if (!p) { emptyIds.push(id); log.warning(`No podcast found for ID ${id} in storefront "${country}".`); continue; }
      keepGoing = await pushResult({ ...podcastRow(p), scrapedAt: new Date().toISOString() });
    } catch (e) { log.warning(`Lookup failed for ${id}: ${e.message}`); }
  }
} else {
  for (const id of ids) {
    if (!keepGoing) break;
    const before = pushed;
    const got = dataType === 'reviews' ? await scrapeReviews(id) : await scrapeEpisodes(id);
    log.info(`${id}: ${got} ${dataType} fetched, ${pushed - before} kept after filters.`);
    if (got === 0) {
      emptyIds.push(id);
      log.warning(dataType === 'reviews'
        ? `Apple's review feed for podcast ${id} in storefront "${country}" is empty (that is Apple's data, not a scrape failure) — try another "country", or check the ID is an Apple Podcasts ID.`
        : `Apple returned no episodes for podcast ${id} in storefront "${country}" — check the ID is an Apple Podcasts ID and that the show is available in that storefront.`);
    }
  }
}

log.info(`Done. Pushed ${pushed} ${dataType === 'podcasts' ? 'podcasts' : dataType}.`);
if (pushed === 0) {
  const why = emptyIds.length
    ? `Apple returned nothing for: ${emptyIds.join(', ')} in storefront "${country}"`
    : emptySearches.length
      ? `your search terms matched no podcasts in storefront "${country}": ${emptySearches.join(', ')}`
      : 'no valid podcast IDs could be parsed from your input';
  await Actor.setStatusMessage(`No results — ${why}. See the log for details.`);
} else if (emptyIds.length) {
  await Actor.setStatusMessage(`Pushed ${pushed} results. Apple returned nothing for: ${emptyIds.join(', ')}.`);
}
await Actor.exit();
