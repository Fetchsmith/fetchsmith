// TEMPLATE: HTTP-only Apify Actor with pay-per-event charging.
// Rules: no headless browser; charge 'result' only for items actually pushed; stop when the user's budget is hit.
import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';
import * as cheerio from 'cheerio';

await Actor.init();
const input = (await Actor.getInput()) ?? {};
const maxResults = Math.min(Number(input.maxResults ?? 50), 5000);

const cm = Actor.getChargingManager();
let pushed = 0;

async function pushResult(item) {
  const r = await Actor.charge({ eventName: 'result', count: 1 });
  if (r.chargedCount === 0) return false;            // budget exhausted; do not push unpaid items
  await Actor.pushData(item);
  pushed += 1;
  return !r.eventChargeLimitReached && pushed < maxResults;
}

async function fetchHtml(url, opts = {}) {
  const res = await gotScraping({ url, timeout: { request: 30000 }, retry: { limit: 2 }, ...opts });
  return res.body;
}

try {
  // ---- source-specific logic goes here ----
  // Example: iterate pages, parse with cheerio, call pushResult(item) for each row; break when it returns false.
  const html = await fetchHtml('https://example.com/');
  const $ = cheerio.load(html);
  await pushResult({ title: $('title').text().trim(), url: 'https://example.com/' });
} catch (err) {
  log.exception(err, 'Run failed');
  await Actor.fail(`Run failed: ${err.message}`);
}
log.info(`Done. Pushed ${pushed} results.`);
await Actor.exit();
