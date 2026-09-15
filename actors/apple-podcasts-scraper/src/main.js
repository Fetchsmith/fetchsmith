import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';

await Actor.init();
const input = (await Actor.getInput()) ?? {};
const podcasts = (input.podcasts ?? []).map(String).filter(Boolean);
const searchTerms = (input.searchTerms ?? []).map(String).filter(Boolean);
const dataType = ['episodes', 'reviews', 'podcasts', 'charts', 'publisher'].includes(input.dataType) ? input.dataType : 'episodes';
const country = String(input.country || 'us').toLowerCase().trim();
const chartCount = Math.min(Number(input.chartCount ?? 50), 200);
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
const chartGenre = input.chartGenre && CHART_GENRE_IDS[input.chartGenre] ? input.chartGenre : null;
if (input.chartGenre && !chartGenre) log.warning(`Unknown "chartGenre" value "${input.chartGenre}" — ignored, using the overall top chart. Valid values: ${Object.keys(CHART_GENRE_IDS).join(', ')}.`);
const searchLimit = Math.min(Number(input.searchLimit ?? 10), 200);
const perPodcastEpisodes = Math.min(Number(input.maxEpisodesPerPodcast ?? 100), 200);
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
const parseId = (s) => (s.match(/id(\d{6,})/)?.[1] || s.match(/^\d{6,}$/)?.[0] || s.match(/\/(\d{6,})(?:[/?]|$)/)?.[1] || null);

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
    const row = episodeRow(e, info);
    if (minDurationSeconds != null && row.durationMs == null) unknownDurationKept += 1;
    if (!episodePassesFilters(row)) continue;
    keepGoing = await pushResult({ ...row, scrapedAt: new Date().toISOString() });
  }
  return got;
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
for (const p of podcasts) {
  const id = parseId(p);
  if (id) addId(id);
  else log.warning(`Cannot parse a podcast ID from "${p}" — use an Apple Podcasts URL (…/id1434243584) or the numeric ID.`);
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
  // Rank comes from array order in both cases.
  const url = chartGenre
    ? `https://itunes.apple.com/${country}/rss/toppodcasts/limit=${chartCount}/genre=${CHART_GENRE_IDS[chartGenre]}/json`
    : `https://rss.marketingtools.apple.com/api/v2/${country}/podcasts/top/${chartCount}/podcasts.json`;
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
}

if (unknownDurationKept > 0) {
  log.warning(`minDurationSeconds is set: ${unknownDurationKept} episode(s) had no duration in Apple's own data and were kept rather than dropped, since an unknown duration is not evidence of a short episode.`);
}
log.info(`Done. Pushed ${pushed} ${dataType === 'podcasts' || dataType === 'publisher' ? 'podcasts' : dataType}.`);
const timeBudgetNote = timeBudgetExceeded
  ? ' Stopped early: approaching the run time limit — reduce the number of podcasts/searchTerms or maxEpisodesPerPodcast/maxReviewsPerPodcast to get a complete run.'
  : '';
if (pushed === 0 && timeBudgetExceeded) {
  await Actor.setStatusMessage(`No results before the run approached its time limit.${timeBudgetNote}`);
} else if (pushed === 0) {
  const why = emptyIds.length
    ? `Apple returned nothing for: ${emptyIds.join(', ')} in storefront "${country}"`
    : emptySearches.length
      ? `your search terms matched no podcasts in storefront "${country}": ${emptySearches.join(', ')}`
      : depthCapped.length
        ? `maxReviewsPerPodcast (${perPodcastReviews}) was hit before any review passed your minRating/maxRating/keyword filter for: ${depthCapped.join(', ')} — raise maxReviewsPerPodcast to search deeper`
        : dataType === 'reviews' && (keyword || minRating != null || maxRating != null)
          ? 'every review Apple returned was removed by your minRating/maxRating/keyword filters'
          : 'no valid podcast IDs could be parsed from your input';
  await Actor.setStatusMessage(`No results — ${why}. See the log for details.`);
} else if (depthCapped.length) {
  await Actor.setStatusMessage(`Pushed ${pushed} results. maxReviewsPerPodcast (${perPodcastReviews}) was hit while filtering: ${depthCapped.join(', ')} — some matching reviews may sit deeper in the feed; raise maxReviewsPerPodcast to search further.${timeBudgetNote}`);
} else if (emptyIds.length || timeBudgetExceeded) {
  await Actor.setStatusMessage(`Pushed ${pushed} results.${emptyIds.length ? ` Apple returned nothing for: ${emptyIds.join(', ')}.` : ''}${timeBudgetNote}`);
}
await Actor.exit();
