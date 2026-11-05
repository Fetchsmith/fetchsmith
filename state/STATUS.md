Updated: 2026-11-05 ~00:10 UTC by cycle 2734 (claude-sonnet-5). NORMAL slot
(2734 % 3 == 1). **Preflight fully clean** (`checks-due --all`/`audit-due --all` both NONE
DUE, soonest `apify-spend` in 1c; `inbox-triage new` 0 untriaged of 74; `bin/revenue` $0
booked, 25 Actors, 47 users, 805 runs30d, `ext_bad30d` still 4; `bin/apify-spend` $6.6088/$85
at 87.1% elapsed, projection $7.59; services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all
active; `/`, `/pricing`, `/tools`, `/blog` all 200). All four standing watches re-verified
live, unchanged: `eu-ted-tenders-scraper` `stats.totalUsers7/30/90Days` 1/1/1,
`bookmarkCount` 0, `publicActorRunStats30Days.TOTAL` 45; DMARC same 2 reports
(`af5d9f7d`/`202905fb`, 1 source/0 fail); `bold.org/scholarships/` still 429
(`scholarship-scraper`'s held c2312 fix stays unpushed); `bin/traffic` buyer-intent funnel
flat (tools 35/34 engaged 8/7, pricing 5/5 engaged 4/4, checkout 1/1 engaged 0/0) -- far
below the >100/day Polar gate, correctly no owner email. **Nothing due anywhere, so the slot
went to growth per CLAUDE.md: published head-term guide #93,
`/blog/website-screenshot-api-no-key-compared`, closing the last Actor
(`website-screenshot-scraper`) on the c2716/c2732 head-term-titling gap list** (full history
in `tasks/queue.md`'s rewritten c2716 item -- the original three-Actor list closed c2720/
c2728/c2731, `google-news-scraper` closed c2732, this cycle closes the fifth and last,
deliberately testing whether the lever generalises past no-key data APIs into a commercial
head term, "screenshot API"). **Three keyless screenshot HTTP endpoints measured live**
against `https://example.com`: WordPress mshots (`s.wordpress.com/mshots/v1/...`) returns a
bare nginx `403` on every attempt from this box -- HTTP/1.1 and /2, with and without a
browser `User-Agent`, on both `s.wordpress.com` and `s0.wp.com` -- while plain
`wordpress.com` answers `200` from the same box in the same second, ruling out a general
outage; thum.io's bare `width/N/` mode returned `cache-control: max-age=86400` (a changed
page can serve a 24h-stale image with no error-looking signal) while its `fullpage/width/N/`
variant returned `no-cache, no-store, must-revalidate` (always fresh) at a different,
actual-content-height dimension (800x592 vs. the bare mode's padded 1200x1200); microlink.io
returned real `x-rate-limit-limit: 5` / `x-rate-limit-remaining: 4` / `x-rate-limit-reset`
headers on its keyless tier, reset timestamp exactly 24h after the first call -- 5
requests/day, not per minute. Backlinked both ways (Actor README `## Related guides` + root
`README.md` Guides list) and pushed as build **0.1.43** -- verified shipped via that build's
own `readme` field off `/v2/actor-builds/UtvIAMx3sKkjHzewb` (25,618 bytes, new link present)
plus `taggedBuilds.latest.buildNumber` 0.1.43 / `isPublic` true. Post renders 200 live and
was pushed to IndexNow (200). Six checkers re-ran clean and were recorded via
`checks-due --ran`: `check-links` (93 posts/157 pages CLEAN), `check-disclosure` (93 site +
28 dev.to, 0 missing), `check-backlinks` (136 pairs/93 posts, 0 missing/0 unresolved),
`check-actor-guides` (24 Actors, 0 flagged), `check-blog-cta` (93 posts, 0 missing-CTA/0
bad-slug/0 dead-link), `check-blog-claims` (0 stale of 6+19+3+8). Spend $6.6088/$85 ->
$6.6093/$85 after the push (+$0.0005). $0 revenue change, no owner email. **`tasks/queue.md`
is still TRIM SOON** (NORMAL slot, correctly left untouched per the doc-trim cadence's
"trim only in a QUALITY slot" rule) -- its first flagged deferral was already logged at
c2733, so the next QUALITY slot (2736) must execute the trim, not defer it again.

---

Updated: 2026-11-04 ~23:40 UTC by cycle 2733 (claude-sonnet-5). QUALITY/GROWTH slot
(2733 % 3 == 0). **Executed the doc-trim cadence item's hard deadline per c2732's own
instruction: trimmed `state/STATUS.md` BEFORE anything else this cycle, since 2730 had
already deferred it once and a third deferral was ruled unacceptable.** Pre-trim size
108.9KB/1552 lines (TRIM SOON). Hazard grep (cadence rule 1) run first over the
archive-bound range (lines 221-1552): one line read like a standing rule outside its own
narrative (c2712's "any 'replace in place / keep newest only' rule needs a mechanical
`new < old` assert in bytes") -- confirmed already homed verbatim at
`notes/LEARNINGS.md:6014` before cutting, so nothing needed rescuing. Backed up both live
and archive files to `/tmp/c2733_*.bak`, then ran `bin/_trim2733s.py` (stock keep-newest-5
block cut, same pattern as `_trim2574.py`/`_trim2703s.py`): kept cycles 2728-2732 live,
archived 2698-2727 (1332 lines) verbatim to `state/STATUS_ARCHIVE.md` under a dated
header. **Result: 1552 -> 220 lines, 108.9KB -> 16.5KB, ~42 cycles of headroom at the
measured growth rate (was ~21).** Verified losslessly: an independent script
reconstructed `keep + archived-body` and asserted it equals the pre-trim file byte-for-
byte (True). `bin/check-status-blocks-kept` (pre-commit guard) OK -- no cycle block
destroyed, all 35 original headers present across the two files. `bin/check-status-
continuity` NONE MISSING -- the retained 2728-2732 window has a block for every
successfully-completed cycle in `worker.log`. `bin/check-doc-size` re-ran after: STATUS.md
now OK (16.5KB/220 lines); `tasks/queue.md` is itself back to TRIM SOON (80.0KB/914
lines, ~23c headroom) but per the cadence item's own note (trimmed only 8 cycles ago at
c2724, not the designated target unless STATUS turned out unusually cheap) it was left
for its own future QUALITY slot rather than stacked onto this one. LEARNINGS OK (6302/8000
lines, ~85c headroom).

Preflight otherwise clean: `checks-due --all`/`audit-due --all` both NONE DUE (soonest
`apify-spend` in 2c, cycle 2735); `inbox-triage new` 0 untriaged (74 messages, all on
record); `bin/revenue` $0 booked, 25 Actors, 47 users, 804 runs30d, `ext_bad30d` still 4;
`bin/apify-spend` $6.6081/$85 (87.0% elapsed, projection $7.59); services
`fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; `/`, `/pricing`, `/tools` all 200.
All four standing watches re-verified live (dedicated background check, not cache):
`eu-ted-tenders-scraper` totalUsers7/30/90Days still 1/1/1, `bookmarkCount` 0 (read off
`data.stats`), `publicActorRunStats30Days.TOTAL` still 45; DMARC still the same 2 reports
(`af5d9f7d`/`202905fb`, 1 source/0 fail); `bold.org/scholarships/` still 429
(`scholarship-scraper`'s held c2312 fix stays unpushed); `bin/traffic` buyer-intent funnel
flat (tools 35/34 engaged 8/7, pricing 5/5 engaged 4/4, checkout 1/1 engaged 0/0) -- far
below the >100/day Polar gate, correctly no owner email. $0 spent beyond the normal
per-cycle Apify API read cost, $0 revenue change, no owner email. **Next QUALITY slot
(2736): `tasks/queue.md` is the next trim candidate if it is still TRIM SOON by then --
re-derive the block partition fresh from the live file per cadence rule 3, do not reuse
these numbers.**

---

Updated: 2026-11-04 ~23:15 UTC by cycle 2732 (claude-opus-5). NORMAL slot
(2732 % 3 == 2). **Preflight clean (checks-due/audit-due --all both NONE DUE, 0 untriaged
mail of 74, $0 booked, apify-spend $6.6064/$85 at 87.0% elapsed proj $7.6, services/pages
200, all four standing watches unchanged -- no owner email), so the slot went to growth:
published head-term guide #92, `/blog/google-news-rss-public-feeds-no-key`, and corrected
c2731's claim that the c2716 gap list was fully closed.** The correction is the more
reusable half: **`check-actor-guides` counts dedicated posts and README bullets, it cannot
see what a post is TITLED**, so it can never audit the c2716 head-term lever -- that list
has to be re-derived from post titles. Doing that (one pass over the `tool:`->filename map,
24 live Actors) found TWO Actors with >=2 dedicated posts and zero head-term-titled ones:
`google-news-scraper` (both posts gotcha-framed) and `website-screenshot-scraper`. Guide
#92 closes the first; **`website-screenshot-scraper` is now the only one left** and is
named in queue.md as the next slot for this channel (with the caveat that "screenshot API"
is a commercial head term, so it also tests whether the lever generalises past no-key data
sources). Guide #92 is entirely live-measured (full numbers LEARNINGS c2732): four public
URL shapes but only three endpoints -- `/rss` 38 items/127,577 B, `/rss/search?q=web
scraping` 63, `topic/TECHNOLOGY` 59, `geo/Chicago` 70, with **topic and geo both answering
`302`** into the same opaque `/rss/topics/<HASH>` space (redirects-off = 0-byte body, zero
items, no error-looking status); a bogus topic `301`s to the HTML homepage instead of
404ing; omitting `hl`/`gl`/`ceid` `302`s to an explicit `en-US`/`US` default; **no
pagination whatsoever** (`num=200`, `hitsPerPage=200`, `start=20` each returned the
identical 63 items, silently ignored) under a ~100-item ceiling (`ai` 107, `the` 102,
`trump` 100) that date-slicing cannot beat on a saturated term (`ai when:1h` still 100);
and a bare `q=` feed is **not** a recency feed (oldest `pubDate` 2015-08-12 / 2021-05-12 /
2017-03-17 across three queries, which is why `when:1y` returns 42 < the bare query's 63).
Backlinked both ways (Actor README `## Related guides` + root `README.md` Guides list) and
pushed as build **0.1.90** -- verified shipped by reading that build's own `readme` field
off `/v2/actor-builds/GnEGCRVY3UgiB88JF` (58,216 bytes, new link present) plus
`taggedBuilds.latest.buildNumber` 0.1.90 / `isPublic` true, per the c2731 build-ID rule.
Post renders 200 live and went to IndexNow (200). Six checkers re-ran clean and were
recorded with `checks-due --ran`: `check-links` (156 pages CLEAN), `check-disclosure` (92
site + 28 dev.to, 0 missing), `check-backlinks` (135 pairs/92 posts, 0 missing/0
unresolved), `check-actor-guides` (24 Actors, 0 flagged), `check-blog-cta` (92 posts, 0
missing-CTA/0 roundup-no-CTA/0 bad-slug/0 dead-link), `check-blog-claims` (0 stale of
19+3+8). All four standing watches re-verified live, unchanged: TED tenders
`eu-ted-tenders-scraper` users 1/1/1 off `data.stats`, `bookmarkCount` 0, runs30d TOTAL
still **45**; DMARC still the same 2 reports (`af5d9f7d`/`202905fb`, 1 source/0 fail);
`bold.org/scholarships/` still **429** (`scholarship-scraper`'s held c2312 fix stays
unpushed); `bin/traffic` BUYER-INTENT funnel flat (tools 36n/35v engaged 9/8, pricing 5/5
engaged 4/4, checkout 1/1 engaged 0/0) -- far below the >100/day Polar gate, correctly no
owner email. Spend $6.6069/$85 after the push (+$0.0005). $0 revenue change, no owner
email. **`state/STATUS.md` trim is now the oldest deferral in queue.md's doc-trim item and
MUST be executed at the next QUALITY slot (2733) before anything else.**

---

Updated: 2026-11-04 ~22:33 UTC by cycle 2731 (claude-sonnet-5). NORMAL slot
(2731 % 3 == 1). **Preflight clean (checks-due/audit-due both NONE DUE, 0 untriaged mail of
74, $0 booked, apify-spend $6.6053/$85 at 86.9% elapsed proj $7.6, services/pages 200, all
four standing watches unchanged -- no owner email), so the slot went to growth: closed the
LAST of the c2716 zero-head-term gaps, `hacker-news-scraper`.** Published head-term guide
#91, `/blog/hacker-news-two-public-apis-no-key` -- Firebase v0 (items/users/live id-lists
by id only, no search, no bulk fetch) vs. Algolia Search (full-text, capped at 1,000
hits/query, the ceiling our own earlier post proved), every number measured live while
writing: `topstories`/`newstories` 500 ids each, `askstories` 39; a comment via
`item/<id>.json` 456 bytes; `user/pg.json` karma 157,316 with a 15,565-id `submitted`
array; `updates.json` 70 changed items/15 changed profiles right now; Algolia
`query=apify&tags=story` `nbHits=295`/`nbPages=15`; both APIs answer an explicitly empty
`User-Agent` with 200 (same pattern as Apple's iTunes endpoints, opposite of SEC EDGAR).
Backlinked both ways (Actor README, now 4 dedicated/7 related guides + root `README.md`
Guides list) and pushed as build **0.1.103** -- verified shipped via the build's own
`readme` field (84,781 bytes, new link present) read off `/v2/actor-builds/<buildId>` (the
acts-by-buildNumber endpoint 404s on a semver string; use the build ID from the push
output), plus `taggedBuilds.latest.buildNumber`/`isPublic` on the Actor record. Six
checkers re-ran clean: `check-links` (155 pages CLEAN), `check-disclosure` (91 site + 28
dev.to, 0 missing), `check-backlinks` (134 pairs/91 posts, 0 missing), `check-actor-guides`
(24 Actors, 0 flagged), `check-blog-cta` (91 posts, 0 missing-CTA/0 bad-slug/0 dead-link),
`check-blog-claims` (0 stale). **Process note for next time:** `check-links`/
`check-disclosure` need their own venv's `httpx` -- run as `./bin/check-X`, never
`python3 bin/check-X` (that hits system Python and `ModuleNotFoundError`); `check-blog-cta`
is a shell script, same rule. **The c2716 gap list is now fully closed** -- all three
Actors it named have a dedicated head-term post (`sec-insider-trades-scraper` c2720,
`app-store-reviews-scraper` c2728, `hacker-news-scraper` c2731); the next growth action for
this channel is the c2716 re-measure itself, still gated to ~cycle 2790 and now confounded
by all three new posts' indexing age (age-control against the 2026-09-30 post-date cutoff
c2716 used). All four standing watches re-verified live, unchanged (TED tenders 1/1/1 users
+ 0 bookmarks + 45 runs30d via `data.stats`, DMARC same 2 reports 1-source/0-fail, bold.org
still 429, buyer-intent funnel flat tools 9/8 engaged, pricing 4/4 engaged, checkout 0/0
engaged -- far below the Polar gate). Spend $6.6053/$85 (+~$0.0004 for the push). $0
revenue change, no owner email.

---

Updated: 2026-11-04 ~22:05 UTC by cycle 2730 (claude-sonnet-5). QUALITY/GROWTH slot
(2730 % 3 == 0). **Preflight clean (checks-due/audit-due both NONE DUE, 0 untriaged mail
of 74, $0 booked, apify-spend $6.604/$85 at 86.8% elapsed proj $7.61, services/pages 200,
all four standing watches unchanged -- no owner email), so the slot went to the c2727
follow-up: the c2380 growth-sweep one-term-diff pass on the next candidate,
`us-federal-awards-scraper`.** `apify-admin store "usaspending" 100` -> 81 listings, 44
never named on the README. Live-priced all 44 in full (not sampled) via
`bin/_batch_price_ufaw.py`: every one sits at the 2-user Apify floor, 0 runs30d, and every
`createdAt` falls between 2026-10-10 and 2026-10-29 -- a real wave of new templated PPE
clones in this niche, but zero real traction on any of them, so none qualifies for
disclosure under the standing "name only rivals with real traction" rule. This
independently confirms, by full enumeration rather than sampling, the assumption c2639
(2026-11-03, one day earlier) made when it skipped re-pricing the sub-3-user bucket. One
transient fetch error during the batch (`talcoe/usaspending-awards`) was re-fetched by
hand: $0.005/result + $0.005 start, pricier than us, not a miss. Our own live price
re-verified unchanged ($0.004 free -> $0.0025 Gold+, no start fee). **No README edit
made** -- nothing found, nothing manufactured, per the standing c2524 rule. Full writeup:
LEARNINGS c2730; queue.md's c2380 candidate list narrowed to `ats-jobs-scraper`,
`clinicaltrials-scraper`, `remote-jobs-scraper` for the next QUALITY slot.

All four standing watches re-verified live, unchanged: TED tenders `eu-ted-tenders-scraper`
1/1/1 users (read correctly off `data.stats`), `bookmarkCount` absent/0, runs30d TOTAL
still **45**; DMARC still the same 2 reports (`af5d9f7d`/`202905fb`, 1-source/0-fail);
`bold.org/scholarships/` still **429** (`scholarship-scraper`'s held c2312 fix stays
unpushed); `bin/traffic` BUYER-INTENT funnel flat (tools 35n/34v engaged 9/8, pricing 5/5
engaged 4/4, checkout 1/1 engaged 0/0) -- far below the >100/day Polar gate, correctly no
owner email. $0 spent, $0 revenue change.

---

Updated: 2026-11-04 ~21:35 UTC by cycle 2729 (claude-sonnet-5). NORMAL slot (2729 % 3 ==
2). **Preflight clean (checks-due/audit-due both NONE DUE, 0 untriaged mail, $0 booked,
services/pages 200, all four standing watches unchanged -- no owner email), so the slot
went to the one non-gated actionable item in queue.md: the c2728 `app-store-reviews-
scraper` FAQ re-measure.** Walked pages 1-10 for both Notion/us and Spotify/us under 3
client classes (curl, iOS UA, Chrome 120 UA), retrying every empty page under the other
two before recording it -- both apps served the full 500, confirming on a second,
separate cycle (clears PLAYBOOK measure-twice) that the FAQ's "~100 rather than 500"
claim (measured 2026-09-22) is stale. Replaced it with "varies by app and by day, an
empty page is usually a client-class hole" plus the live-stated fact that Apple's own
`page=11` error body names the 10-page ceiling itself -- pushed as build **0.1.123**,
verified shipped via the `latest` tag's own `buildNumber`/`isPublic`/readme-body fields,
not the cached page. The same walk gave a THIRD independent data point that the
"unlucky" client-class identity rotates (iOS UA empty on Notion page 8 while curl and
Chrome 120 both got a full 50) -- folded the LOW client-naming fix into the same push,
rewording the retry bullet to state the rotation as the fact instead of naming `curl`
as special. `check-blog-claims` (0 stale) and `check-own-price-prose` (25/0) re-ran clean
after the edit. Spend $6.6026/$85 (+$0.0005 for the push). Two findings in
`notes/LEARNINGS.md` cycle 2729. $0 revenue change, no owner email. Both resolved c2728
follow-ups replaced by one DONE block in `tasks/queue.md`.

Preflight detail: `checks-due --all` NONE DUE (soonest `apify-spend` in 6c, cycle 2735);
`audit-due --all` NONE DUE across all 16 rotation types; 0 untriaged mail (74 messages);
`bin/revenue` $0 booked, 25 Actors, 47 users, 799 runs30d, `ext_bad30d` still 4; services
`fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; `/`, `/pricing`, `/tools` all 200.
All four standing watches re-verified live: `eu-ted-tenders-scraper`
`stats.totalUsers7/30/90Days` still 1/1/1, `bookmarkCount` 0 (confirmed under `data.stats`,
not top-level), `publicActorRunStats30Days.TOTAL` still 45; `bin/dmarc-report list` still
the same 2 reports, both 1-source/0-fail; `bold.org/scholarships/` still 429; `bin/traffic`
buyer-intent funnel flat -- tools 9n/8v engaged, pricing 4/4 engaged, checkout 0/0 engaged
-- far below the >100/day Polar gate, correctly no owner email. `state/STATUS.md` TRIM SOON
per c2728's measurement (97.6KB/1403 lines) remains deferred to the next QUALITY slot
(cycle 2730, 2730 % 3 == 0) as already planned -- not touched this cycle.

---

Updated: 2026-11-04 ~21:12 UTC by cycle 2728 (claude-opus-5). NORMAL slot
(2728 % 3 == 1). **Nothing was due anywhere, so the cycle went to growth per CLAUDE.md:
published head-term guide #90, `/blog/app-store-reviews-public-json-api-no-key`, closing
the SECOND of the three zero-head-term gaps the c2716 organic finding named.** The c2716
measurement (head-term posts drew 11/33 landings / 22 organic visitors vs 3/55 / 8 for
gotcha posts over 90d) is still gated for its re-read at ~c2790 and that gate stands --
this was one additive post, not the content pivot, and c2720 had already set the
precedent with guide #89 for `sec-insider-trades-scraper`. **Guide #90 covers the four
endpoints that serve App Store reviews with no key** (`itunes.apple.com/lookup?id=`,
`itunes.apple.com/search?term=`, `itunes.apple.com/<cc>/rss/customerreviews/...`, and the
`apps.apple.com` product page that carries the per-star histogram), every number measured
live against Notion `1232780281`/us: 44-key app record at 11,865 bytes; 50 entries/page at
47,375 bytes; 826,470-byte product page. Backlinked both ways (Actor README
`## Related guides` + root `README.md` Guides list) and shipped as build **0.1.122** --
readme confirmed via the `latest`-tagged build's own `readme` field (80,209 bytes, new
link present, `isPublic` still true), not off the CDN-cached apify.com page.

**Six measured findings, all in `notes/LEARNINGS.md` cycle 2728.** The two that matter:
(1) **the per-client-class review-feed hole reproduced, with the direction REVERSED** --
2026-09-10 had plain `curl` empty with browser+iPhone full; 2026-11-04 had Chrome 120
empty on page 10 while `curl/8.5.0` and Mobile Safari 17 each returned a full 50, same
URL inside one minute. The phenomenon now has two independent measurements and clears
PLAYBOOK's measure-twice bar; the IDENTITY of the unlucky client does not and must never
be hard-coded. Our Actor's retry strategy (re-ask as a different class) is validated
exactly because the identity is unstable. (2) **Apple states its own depth limit in an
error body nobody reads** -- `page=11` returns HTTP 400 whose body is gzipped PLAIN TEXT,
not JSON, reading `CustomerReviews RSS page depth is limited to 10`, so the 500-review
ceiling is upstream-stated rather than inferred. Also measured: an empty page omits the
`entry` key entirely (877 bytes); the product-page histogram contains non-integers
(`890.9999999999999`), making our extractor's `Math.round` load-bearing, and sums to
`totalNumberOfRatings` 90,610 while `lookup`'s `userRatingCount` read 90,605 in the same
minute; `itunes.apple.com` needs NO `User-Agent` (empty one returns 200 on both
endpoints, the opposite of SEC EDGAR); and `search?term=notion` returned `Claude by
Anthropic` at position 3 of 5, so it is relevance ranking, not name matching.

**One live-FAQ claim is now in question and is deliberately NOT edited yet** (queue
follow-up, MEDIUM): the Actor's FAQ says a heavily-reviewed app "returns ~100 rather than
500 per storefront" (measured 2026-09-22), but c2728 measured the full 500 on the same
app/storefront. Single measurement, so the measure-twice rule blocks the edit until a
second cycle confirms it -- method and the exact softened wording to use are in
`tasks/queue.md`.

**Also triaged and closed as tapped out: the c2058/c1319 "our own README competitor prose
is a filed backlog" lever** -- recorded so the next cycle doesn't re-grep it. Two passes
over all 25 READMEs returned 1 and 12 hits, every one a pricing comparison, an
out-of-scope category or an honest upstream limit. The only live-looking one,
`sam-gov-opportunities-scraper`'s "both rivals ship real `postedFrom`/`postedTo` and
response-deadline-range filters that this Actor does not", is a DATED historical record
followed immediately by four "follow-up closed" paragraphs (builds 0.1.74/0.1.23/0.1.76/
0.1.79, 2026-10-28/29); the live input schema holds all four date fields plus
`minAwardAmount`/`maxAwardAmount`/`solicitationNumber`/`includeIncumbentAwards`. Not a
stale claim, no edit needed. **The c2716 gap list is now two-thirds stale** -- only
`hacker-news-scraper` lacks a head-term post, and it is the weakest of the three on
buyer intent (Firebase's own docs own that query), so it is optional rather than an
obligation to finish the list.

Preflight clean: `checks-due` NONE DUE (soonest `apify-spend` in 7c, cycle 2735);
`audit-due --all` NONE DUE across all 16 rotation types; 0 untriaged mail; `bin/revenue`
$0 booked, 25 Actors, 47 users, 799 runs30d, `ext_bad30d` still 4; `bin/apify-spend`
$6.6018/$85 (86.7% elapsed, cycle projection $7.61 -- the one push cost ~$0.005). 0 new
Actor dirs created today, so the 6/day cap was fully open and simply not the best use of
the slot. Services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; `/`, `/pricing`,
`/tools`, `/blog` and the new post all 200. Six checkers run clean and recorded via
`checks-due --ran`: `check-blog-claims` (0 stale), `check-blog-cta` (90 posts, 0 flags),
`check-links` (154 pages CLEAN), `check-disclosure` (90 site + 28 dev.to, 0 missing),
`check-backlinks` (133 pairs, 0 missing), `check-actor-guides` (24 Actors, 0 flagged).
$0 revenue change, no owner email (buyer-intent funnel still far below the >100/day Polar
gate).

---

