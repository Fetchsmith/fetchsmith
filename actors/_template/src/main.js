// TEMPLATE: HTTP-only Apify Actor with pay-per-event charging.
// Rules: no headless browser; charge 'result' only for items actually pushed; stop when the user's budget is hit.
import { Actor, log } from 'apify';
import { gotScraping } from 'got-scraping';
import * as cheerio from 'cheerio';

await Actor.init();
// Soft-deadline guard: a hard platform kill mid-run loses whatever RUN_SUMMARY/watch-baseline
// bookkeeping a source-specific Actor does at the end, and can look like a source failure to the
// buyer. Stop proactively with a safety margin instead. Wire timeBudgetOk() into any retry sleep
// and any per-page/per-item loop (see google-news-scraper or court-records-scraper for the fuller
// pattern, including a distinct `incompleteReason: 'time-budget'` in the run summary).
const timeoutAt = Actor.getEnv().timeoutAt?.getTime() ?? null;
const TIME_BUDGET_MARGIN_MS = 45_000;
function remainingMs() { return timeoutAt == null ? Infinity : timeoutAt - Date.now() - TIME_BUDGET_MARGIN_MS; }
function timeBudgetOk() { return remainingMs() > 0; }

const input = (await Actor.getInput()) ?? {};
const maxResults = Math.min(Number(input.maxResults ?? 50), 5000);

const cm = Actor.getChargingManager();
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

async function fetchHtml(url, opts = {}) {
  const res = await gotScraping({ url, timeout: { request: 30000 }, retry: { limit: 2 }, ...opts });
  return res.body;
}

try {
  // ---- source-specific logic goes here ----
  // Example: iterate pages, parse with cheerio, call pushResult(item) for each row; break when it
  // returns false. Check timeBudgetOk() at the top of each page/item iteration too, not just here.
  if (!timeBudgetOk()) throw new Error('Out of time budget before any work started');
  const html = await fetchHtml('https://example.com/');
  const $ = cheerio.load(html);
  await pushResult({ title: $('title').text().trim(), url: 'https://example.com/' });
} catch (err) {
  log.exception(err, 'Run failed');
  await Actor.fail(`Run failed: ${err.message}`);
}
log.info(`Done. Pushed ${pushed} results.`);
await Actor.exit();
