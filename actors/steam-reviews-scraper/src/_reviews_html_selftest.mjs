// Live + fixture checks for reviews_html.js. Run: node src/_reviews_html_selftest.mjs
import { parseReviewsPage, parsePostedDate, steamIdFromMiniprofile, reviewsPageUrl, homeContentUrl } from './reviews_html.js';
let fail = 0;
const ok = (c, m) => { console.log(`${c ? 'PASS' : 'FAIL'}  ${m}`); if (!c) fail++; };
const UA = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)' };
const get = async (u) => { const r = await fetch(u, { headers: UA }); if (!r.ok) throw new Error(`${r.status} ${u}`); return r.text(); };

// --- pure unit checks -------------------------------------------------------
ok(steamIdFromMiniprofile('220218906') === '76561198180484634', 'miniprofile -> steamid64 (live-verified pair)');
ok(steamIdFromMiniprofile('1827962737') === '76561199788228465', 'miniprofile -> steamid64 (second live pair)');
ok(steamIdFromMiniprofile('') === null && steamIdFromMiniprofile('x') === null, 'miniprofile junk -> null');
const now = new Date('2026-10-23T00:00:00Z');
ok(parsePostedDate('Posted: 23 October', now) === Date.UTC(2026, 9, 23) / 1000, 'year-omitted date = current year');
ok(parsePostedDate('Posted: 24 August, 2020', now) === Date.UTC(2020, 7, 24) / 1000, 'explicit past year');
ok(parsePostedDate('Posted: 31 December', new Date('2027-01-01T12:00:00Z')) === Date.UTC(2026, 11, 31) / 1000, 'new-year rollback (no future-dating)');
ok(parsePostedDate('garbage') === null, 'unparseable date -> null');
ok(reviewsPageUrl(1145360, { reviewType: 'positive', sortBy: 'recent', language: 'english' }).includes('/positivereviews/?browsefilter=mostrecent'), 'review_type is a path segment, sort maps to browsefilter');
ok(reviewsPageUrl(1145360, { reviewType: 'negative', sortBy: 'all' }).includes('/negativereviews/?browsefilter=toprated'), 'negative + toprated mapping');

// --- live page 1 ------------------------------------------------------------
const APP = 1145360;
const h1 = await get(reviewsPageUrl(APP, { sortBy: 'recent', language: 'english' }));
const p1 = parseReviewsPage(h1, APP);
ok(p1.cardCount === 10 && p1.idCount === 10, `page1 cards==ids==10 (got ${p1.cardCount}/${p1.idCount})`);
ok(p1.reviews.every((r) => r.recommendationid), 'every page1 row has a recommendationid');
ok(p1.reviews.every((r) => r.author.steamid && /^\d{17}$/.test(r.author.steamid)), 'every page1 row has a 17-digit steamid64');
ok(p1.reviews.every((r) => r.review && r.review.length > 0), 'every page1 row has review text');
ok(p1.reviews.every((r) => r.timestamp_created > 0), 'every page1 row has a parsed date');
ok(p1.reviews.every((r) => r.author.playtime_forever != null && r.author.playtime_forever > 0), 'every page1 row has playtime');
ok(p1.reviews.every((r) => typeof r.voted_up === 'boolean'), 'every page1 row has a recommendation verdict');
ok(!/date_posted|Posted:/.test(p1.reviews.map((r) => r.review).join('')), 'date line stripped out of review text');
ok(p1.next && p1.next.cursor && p1.next.fields.p === '2', `page1 exposes a next cursor (p=${p1.next?.fields?.p})`);

// --- live cursor chain + ordering ------------------------------------------
const h2 = await get(homeContentUrl(APP, p1.next));
const p2 = parseReviewsPage(h2, APP);
const ids1 = new Set(p1.reviews.map((r) => r.recommendationid));
ok(p2.cardCount > 0 && p2.reviews.every((r) => !ids1.has(r.recommendationid)), `page2 is ${p2.cardCount} fully distinct rows (cursor paging works)`);
ok(p2.next != null, 'page2 still exposes a next cursor (form id increments, matched by prefix)');
ok(p2.next && p2.next.cursor !== p1.next.cursor, 'cursor advanced on page2');
ok(p2.next && p2.next.fields.appHubSubSection === '10', 'replayed fields keep appHubSubSection=10 (reviews tab only)');
ok(p2.next && !Object.keys(p2.next.fields).some((k) => /page$/.test(k) && k !== 'p'), 'other tabs\' page counters dropped from the replay');
// A deep chain is the check that actually would have caught the #MoreContentForm1 bug.
let deep = p2, deepIds = new Set([...p1.reviews, ...p2.reviews].map((r) => r.recommendationid)), deepHops = 2, dupes = 0;
while (deep.next && deepHops < 6) {
  deep = parseReviewsPage(await get(homeContentUrl(APP, deep.next)), APP);
  for (const r of deep.reviews) { if (deepIds.has(r.recommendationid)) dupes++; deepIds.add(r.recommendationid); }
  deepHops++;
}
ok(deepHops === 6 && dupes === 0, `6-page chain on a large app yields ${deepIds.size} distinct rows, 0 repeats (hops=${deepHops}, dupes=${dupes})`);
const chain = [...p1.reviews, ...p2.reviews].map((r) => Number(r.recommendationid));
ok(chain.every((v, i) => i === 0 || chain[i - 1] > v), 'sortBy=recent is strictly newest-first across pages (ids strictly decreasing)');

// --- live end-of-feed on a low-review app ----------------------------------
const SMALL = 2721880;
let page = parseReviewsPage(await get(reviewsPageUrl(SMALL, { sortBy: 'recent', language: 'all' })), SMALL);
let total = page.reviews.length, hops = 1;
const smallIds = new Set(page.reviews.map((r) => r.recommendationid));
while (page.next && hops < 12) { page = parseReviewsPage(await get(homeContentUrl(SMALL, page.next)), SMALL); page.reviews.forEach((r) => smallIds.add(r.recommendationid)); total += page.reviews.length; hops++; }
ok(page.next === null, `feed terminates by dropping the Show-More form (${hops} pages, ${total} reviews)`);
ok(total > 0 && total < 50 && smallIds.size === total, `low-review app fully paged (${total} rows, all distinct)`);

// --- live toprated: nonzero helpful/funny vote parsing ---------------------
const ht = parseReviewsPage(await get(reviewsPageUrl(APP, { sortBy: 'all', language: 'english' })), APP);
ok(ht.reviews.some((r) => r.votes_up > 0), `nonzero votes_up parsed (max ${Math.max(...ht.reviews.map((r) => r.votes_up))})`);
ok(ht.reviews.some((r) => r.votes_funny > 0), `nonzero votes_funny parsed (max ${Math.max(...ht.reviews.map((r) => r.votes_funny))})`);
ok(ht.reviews.some((r) => r.written_during_early_access), 'early-access badge detected and stripped from text');
ok(!/Early Access Review/.test(ht.reviews.map((r) => r.review).join('')), 'EA badge text not leaking into review body');

// --- live negative path segment -------------------------------------------
const neg = parseReviewsPage(await get(reviewsPageUrl(APP, { reviewType: 'negative', sortBy: 'recent', language: 'english' })), APP);
ok(neg.cardCount > 0 && neg.reviews.every((r) => r.voted_up === false), `negativereviews path yields only negatives (${neg.cardCount} cards)`);

console.log(fail ? `\n${fail} FAILURE(S)` : '\nALL CHECKS PASSED');
process.exit(fail ? 1 : 0);
