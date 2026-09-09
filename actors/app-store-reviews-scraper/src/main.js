import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';

await Actor.init();
const input = (await Actor.getInput()) ?? {};
const apps = (input.apps ?? []).map(String);
const countries = (input.countries?.length ? input.countries : ['us']).map((c) => c.toLowerCase().trim());
const sort = input.sort === 'mostHelpful' ? 'mostHelpful' : 'mostRecent';
const perApp = Math.min(Number(input.maxReviewsPerApp ?? 200), 500);
const maxResults = Math.min(Number(input.maxResults ?? 2000), 50000);
const includeInfo = input.includeAppInfo !== false;
const minRating = input.minRating != null ? Number(input.minRating) : null;
const maxRating = input.maxRating != null ? Number(input.maxRating) : null;
const keyword = input.keyword ? String(input.keyword).toLowerCase() : null;
if (!apps.length) await Actor.fail('Provide at least one app URL or ID.');

function passesFilters(item) {
  if (minRating != null && item.rating < minRating) return false;
  if (maxRating != null && item.rating > maxRating) return false;
  if (keyword && !`${item.title || ''} ${item.content || ''}`.toLowerCase().includes(keyword)) return false;
  return true;
}

let pushed = 0;
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
const getJson = async (url) => JSON.parse((await gotScraping({ url, timeout: { request: 30000 }, retry: { limit: 2 } })).body);
const lbl = (o) => (o && typeof o === 'object' && 'label' in o ? o.label : o ?? null);
const parseId = (s) => (s.match(/id(\d{6,})/)?.[1] || s.match(/^\d{6,}$/)?.[0] || null);

let keepGoing = true;
for (const app of apps) {
  const appId = parseId(app);
  if (!appId) { log.warning(`Cannot parse app id from "${app}"`); continue; }
  for (const country of countries) {
    if (!keepGoing) break;
    let info = null;
    if (includeInfo) {
      try {
        const d = await getJson(`https://itunes.apple.com/lookup?id=${appId}&country=${country}`);
        const a = d.results?.[0];
        if (a) info = { appName: a.trackName, developer: a.artistName, bundleId: a.bundleId, averageRating: a.averageUserRating ?? null, ratingCount: a.userRatingCount ?? null, currentVersion: a.version, primaryGenre: a.primaryGenreName, appUrl: a.trackViewUrl };
      } catch (e) { log.debug(`lookup failed: ${e.message}`); }
    }
    let got = 0;
    for (let page = 1; page <= 10 && got < perApp && keepGoing; page++) {
      let entries = [];
      try {
        const d = await getJson(`https://itunes.apple.com/${country}/rss/customerreviews/id=${appId}/sortBy=${sort}/page=${page}/json`);
        entries = d.feed?.entry ?? [];
        if (!Array.isArray(entries)) entries = [entries];
      } catch (e) { log.warning(`page ${page} failed for ${appId}/${country}: ${e.message}`); break; }
      if (!entries.length) break;
      for (const e of entries) {
        if (got >= perApp) break;
        const item = {
          reviewId: lbl(e.id), appId, country, title: lbl(e.title), content: lbl(e.content), rating: Number(lbl(e['im:rating'])) || null,
          version: lbl(e['im:version']), author: lbl(e.author?.name), authorUrl: lbl(e.author?.uri), updatedAt: lbl(e.updated),
          voteSum: Number(lbl(e['im:voteSum'])) || 0, voteCount: Number(lbl(e['im:voteCount'])) || 0, ...(info || {}), scrapedAt: new Date().toISOString(),
        };
        got += 1;
        if (!passesFilters(item)) continue;
        keepGoing = await pushResult(item);
        if (!keepGoing) break;
      }
    }
    log.info(`${appId}/${country}: ${got} reviews`);
  }
}
log.info(`Done. Pushed ${pushed} reviews.`);
await Actor.exit();
