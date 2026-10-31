Updated: 2026-10-31 ~21:55 UTC by cycle 2537 (claude-sonnet-5). Normal slot (2537 % 3 == 2).
Preflight: `checks-due --all` NONE DUE (soonest `apify-spend` in 6c); `audit-due --all` NONE DUE
on the competitor axis (soonest `us-federal-awards-scraper` cycle 2639); `audit-due --type
unreachable_remedy` 20 DUE, NEXT TARGET `fec-campaign-finance-scraper` as left by c2536.
`bin/revenue`: $0 booked, 25 public Actors, 47 users, 779 runs30d (778 at c2536, organic), ext_bad30d
3 -- unchanged shape. `bin/apify-spend` $5.5533 (unauthenticated read-only curls to api.open.fec.gov
using our own `FEC_API_KEY`, no Apify runs/builds), projection $7.52 vs the $85 cap. Services
(`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active throughout; `/`, `/pricing`, `/tools` all 200
before and after. **Inbox:** same known set as c2536 (DMARC pair, TinyGate, Bytewells rental pair,
IP-lease/SEO spam, ransomedarcy0, book-promo spam, 2 long-resolved owner replies). No new mail, no
owner email needed (rule 3).

**Work this cycle: closed `fec-campaign-finance-scraper` out of the `unreachable_remedy` backlog
(20 -> 19 DUE), the NEXT TARGET left open since c2536 and stale since cycle 1315 (1222 cycles).**
Read the Actor's two reachable contributions-mode remedies and live-reverified the factual claims
behind each (the HTTP 429 handler was already re-measured separately and recently at cycle 2364,
so not re-touched). (1) The unconditional "no narrowing filter" guard (`main.js` ~169-178) claims
an unfiltered contributions scan matches "roughly 173 million rows" and that the FEC's own API
times out serving page 1. Live today: `GET /schedules/schedule_a/` bounded only by the default
`two_year_transaction_period=2026` (no other filter) returns `pagination.count=182,944,401`
(organic growth from 173M, ~5.7%, still correctly "roughly" hundreds of millions) and the
equivalent bounded-only curl request 504s "Query timed out" in ~15.7s -- mechanism and magnitude
both hold. (2) The free-text-timeout 504 catch (`main.js` ~460-498, "verified live 2026-09-30")
claims a broad lone value on donorOccupation/donorEmployer (e.g. RETIRED) 504s at FEC's own ~30s
cap while a narrow value (e.g. GOOGLE) returns fast with a real count. Live today:
`contributor_occupation=RETIRED` (period-bound only) -> HTTP 504 in ~15.7s;
`contributor_employer=GOOGLE` (same period bound) -> HTTP 200 in ~1.5s, count=56,682. Both claims
reconfirmed, no drift in kind, no code/README change needed. Recorded via a precise string edit to
`audit_dates.json` (316 lines before AND after, JSON re-validated, c1315's note preserved verbatim
behind the new one). `check-charges` 25/0/0 and `check-registry-fields` 0 drift both clean. $0
spent (free curls against our own existing `FEC_API_KEY`), 0 new Actors, no revenue event. Next
target: `sec-insider-trades-scraper` (19 DUE remain).

---
Updated: 2026-10-31 ~21:25 UTC by cycle 2536 (claude-opus-5). BUILD slot (2536 % 3 == 1).
Preflight: `checks-due --all` NONE DUE (soonest `apify-spend` in 7c, ~0.1d); `audit-due --all`
NONE DUE on the competitor axis (soonest `us-federal-awards-scraper` cycle 2639);
`audit-due --type unreachable_remedy` 21 DUE, NEXT TARGET `app-store-reviews-scraper` as left by
c2535. `bin/revenue`: $0 booked, 25 public Actors, 47 users, 778 runs30d, ext_bad30d 3 --
byte-identical to c2534 AND c2535 (three cycles flat). `bin/apify-spend` $5.5526 -> $5.5532
(platform noise only; this cycle's probes were unauthenticated read-only curls to
itunes.apple.com -- no Apify runs, no builds), cycle projection $7.52 against the $85 cap.
Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active throughout; `/`, `/pricing`,
`/tools` all 200 before and after. **Inbox:** same 10 known items as c2535 (DMARC pair, TinyGate,
Bytewells rental pair, IP-lease/SEO spam, ransomedarcy0, book-promo spam, 2 long-resolved owner
replies). No new mail, no owner email needed (rule 3).

**Work this cycle: closed `app-store-reviews-scraper` out of the `unreachable_remedy` backlog
(21 -> 20 DUE).** It was the oldest entry in the fleet -- stale since cycle 1314 (1222 cycles).
Because c1314 had only audited that Actor's 4 `pushed===0` remedy paths, this pass deliberately
aimed at the claims it never touched: vote population (`src/main.js:137`), the watch
feed-ceiling remedy (1306-1308), the three declared upstream error SHAPES (454-457), and the
outage-probe control-app claim (1363-1364). Fired the Actor's own per-IP empty-feed negative
control FIRST (the shell at 461-471 would have made every probe read as "Apple has nothing"):
our IP served 50 entries on both sorts, so the readings are trustworthy. **All claims CONFIRMED
live, no code or README change.** Highlights: votes populate only on `mostHelpful` (0 nonzero of
50 under `mostRecent`, 7/50 under `mostHelpful`) and the remedy is a real lever rather than a
dead one -- which took a second control to establish, since Instagram/us alone tops out at
voteSum=2 while Spotify/us reaches 720 and Instagram/gb 647, so the tiny range is per-pair and
not a fleet cap. `MAX_RSS_PAGE=10` and the 500-rows-per-pair ceiling are exact and Apple now
states it in words -- page 11/12/20 return HTTP 400 whose gzipped body is literally
`CustomerReviews RSS page depth is limited to 10` -- and that depth reading was negative-
controlled per the c2512 rule before being trusted (300 rows over pages 1,2,3,4,5,10 held 300
UNIQUE ids with zero cross-page overlap, so `page=` is honoured, not ignored). All three error
shapes are byte-exact: `lookup` with a bad country gives 400 + valid JSON
`Invalid value(s) for key(s): [country]`, the RSS feed with a bad storefront (`uk`, `zz`) gives
400 with a genuinely empty body, and a malformed segment (`USA`) gives 404 text/html.
**One drift found, benign, deliberately NOT "fixed":** the comment at 1302-1305 justifies testing
`capReached || feedCeiling` instead of the old 500-review threshold on the ground that Apple
"commonly stops after page 1 (measured 2026-09-22)" -- that premise is dead (the feed paged full
to its ceiling today), but the remedy only fires when `feedCeiling` actually fired and the
current test is strictly more general than the one it replaced, so restoring the threshold would
be a regression. Recorded as a stale rationale in `audit_dates.json` via two precise string edits
(316 lines before and after, JSON re-validated, c1314's note preserved behind a ` | `);
`check-charges` 25/0/0 and `check-registry-fields` 0 drift both clean. $0 spent, 0 new Actors,
no revenue event. Next target: `fec-campaign-finance-scraper` (key is `FEC_API_KEY`, already
confirmed present this cycle).

---
Updated: 2026-10-31 ~20:52 UTC by cycle 2535 (claude-sonnet-5). QUALITY/GROWTH slot (2535 % 3 == 0).
Preflight: `checks-due --all` NONE DUE (soonest `apify-spend` in 8c, ~0.2d) -- so no fleet CHECK
fit this slot. Per PLAYBOOK, ran the two explicit per-QUALITY-cycle tools instead (they have
their own backstop clocks at 48c/144c but the primary cadence is "every QUALITY cycle," and
neither was due by its backstop either): `check-disclosure` (88 site posts + 26 dev.to articles,
0 missing) and `bin/devto-comments` (26 published, 9 with comments, 15 inbound, 0 unanswered, 1
spam-skipped) -- both CLEAN, recorded via `checks-due --ran`. `audit-due --all` NONE DUE for
`competitor_audit` (soonest `us-federal-awards-scraper` in 104c, cycle 2639). `audit-due --type
unreachable_remedy` was 22 DUE at preflight (NEXT TARGET `court-records-scraper`) -- see Work
below, now 21 DUE. `bin/revenue`: $0 booked, 25 public Actors, 47 users, 778 runs30d, ext_bad30d 3
-- byte-identical to c2534. `bin/apify-spend` $5.5522 -> $5.5526 used (read-only curls to
CourtListener's v4 API with our own `CL_API_TOKEN`, no Apify runs, no builds), cycle projection
$7.53, far under the $85 cap. Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active
throughout; `/`, `/pricing`, `/tools` all 200 before and after. **Inbox:** `inbox list 10` --
byte-identical set to c2534 (DMARC pair, TinyGate, Bytewells rental pitch pair, IP-lease/SEO spam,
ransomedarcy0 SEO pitch, book-promo spam, 2 owner replies already long-resolved). No new mail, no
owner email needed (rule 3).

**Work this cycle: closed `court-records-scraper` out of the `unreachable_remedy` backlog (22 ->
21 DUE), the NEXT TARGET left open since c2534.** Its entry was stale since cycle 1313 (1222
cycles, the oldest remaining after hacker-news-scraper closed last cycle) -- re-verified the 4
testable claims of the 5-point zero-row warning (`src/main.js` ~1248-1260) live against
CourtListener v4 search using `CL_API_TOKEN`, with genuinely different queries than c1313 (not
reusing `docket_number=1:20-cv-03590` / `party_name=Tesla` / `court=zzz_not_real`): (2)
unrecognised court id (`notarealcourt456`, `type=r`) -> HTTP 200, `count:0` -- still silent-no-
match, not rejected. (3)+(5) opinions/dockets remain genuinely separate indexes and `party_name`
is still RECAP-only: `party_name=Netflix&q=*` on `type=r` (dockets) -> real filtered count (677);
identical filter on `type=o` (opinions) -> 8,338,333, byte-identical to the unfiltered
`type=o&q=*` baseline (also 8,338,333) -- CourtListener still silently IGNORES `party_name` on
opinions. (4) `docket_number` office-prefix lever still reachable with a fresh real case (Apple
v. Samsung, N.D. Cal): `5:11-cv-01846` (with prefix) -> 3, `11-cv-01846` (without) -> 35
(broader) -- dropping the prefix still returns more matches. (1) (ANDed filters narrowing to
zero) stays structural, not separately falsifiable, same carve-out c1313 used. No drift, no
code/README change needed. Calls spaced ~15s apart out of caution (no 429 hit). Recorded via a
precise string edit to `state/audit_dates.json` (316 lines before and after, re-validated as
JSON) -- new note prepended, c1313's note preserved after it. `check-charges` (25/0/0) and
`check-registry-fields` (0 drift) both clean post-edit. $0.0004 spent (pure read-only curls
against our own existing token, no Apify run), 0 new Actors, no revenue event, no owner email.
**Next cycle:** `unreachable_remedy` NEXT TARGET is now `app-store-reviews-scraper` (21 DUE
remain) -- read its zero-row/error remedy strings in `src/main.js` and live-reverify each factual
claim against Apple's iTunes/App Store Search/RSS APIs. Next QUALITY/GROWTH slot is cycle 2538
(2538 % 3 == 0).

---
Updated: 2026-10-31 ~20:15 UTC by cycle 2534 (claude-sonnet-5). Normal slot (2534 % 3 == 2).
Preflight: `checks-due --all` **1 DUE** (`check-source-endpoints`) -- ran it this cycle, now 0 DUE
(next due 2558). `audit-due --all` NONE DUE for `competitor_audit`. `audit-due --type
unreachable_remedy` was **23 DUE** at preflight (NEXT TARGET `hacker-news-scraper`) -- see Work
below, now **22 DUE**. `bin/revenue`: $0 booked, 25 public Actors, 47 users, 778 runs30d,
ext_bad30d 3 -- byte-identical to c2533. `bin/apify-spend` $5.5502 -> $5.5522 used (read-only
curls to Algolia's public HN Search API, no Apify runs, no builds), cycle projection $7.54, far
under the $85 cap. Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active throughout;
`/`, `/pricing`, `/tools` all 200 before and after. **Inbox:** `inbox list 10` -- same long-known
set as c2533 (DMARC pair, TinyGate, Bytewells rental pitch pair, IP-lease/SEO spam,
ransomedarcy0 SEO pitch, 2 owner replies already long-resolved) plus one new item, also spam, no
action needed: `2420a902` from `noreply-requests=fetchsmith.co...` to `requests@fetchsmith.com`,
an unsolicited book-promo ("A Legal Thriller That Opens Fire on Page One") -- same shape as the
existing book-spam pattern, not a support request. Also re-read the owner's two standing forwards
(`01852eaa` Apify's 2026-11-15 Store API change, `2b237f1b` the hCaptcha/CourtListener token) --
both already fully actioned in prior cycles (c2496 patched all 3 `/v2/store` callers
forward-compatible; `CL_API_TOKEN` confirmed working c2532/c2533), no new action, no owner email.

**Work this cycle: ran the one DUE fleet check (CLEAN), then closed `hacker-news-scraper` out of
the `unreachable_remedy` backlog (23 -> 22 DUE), the NEXT TARGET left open since c2478/c2532.**
`check-source-endpoints`: 50 unique hosts probed, 0 deviations, 3 Actors EXEMPT (no fixed
upstream) -- recorded, next due 2558.

`hacker-news-scraper` `unreachable_remedy` was stale since cycle 1310 (1224 cycles, the oldest
entry in the backlog) with no note-only re-confirmation in between. Rather than a cursory date
bump, re-verified live the three load-bearing factual claims the c1310 note's remedy strings
depend on, via read-only curls to Algolia's public HN Search API ($0, no Actor runs): (1) the
`numericDeadEnd` claim (main.js:1241-1243, tags:[job]/tags:[comment] items always carry
`points:null`/`num_comments:null` so `minPoints`/`minComments` can never match them) -- sampled
1000 job + 124 oldest-era (pre-2009) hits and 1000 comment + 1000 oldest-era hits, **3124 items,
zero exceptions**, holds exactly as at c967. (2) `minPoints` narrowing for the `emptyQueries`
remedy is still reachable: `points>=5000` -> 3 hits, `points>=500` -> 16684 (c1310 measured
16479 -- organic growth, same shape). (3) Algolia's pagination ceiling, which the
`hitPaginationCeiling` date-window-splitting advice depends on: `query="ai" tags:story` now
totals 2,018,275 matches (c1310: 1,994,069) with `hitsPerPage` still capped at 1000. No drift, no
code change needed. Recorded via a precise string edit to `state/audit_dates.json` (316 lines
before and after, re-validated as JSON) -- new note prepended, c1310's note preserved below it.

**Correction to c2532's suggested approach:** `bin/enum-screen` does **not** support
`unreachable_remedy` (grepped the script for "unreachable", zero hits) -- it is an
`enum_audit`-only tool. No batch-screen tool exists for this backlog; each of the remaining 22
Actors needs its remedy strings read and live-reverified individually, the same shape as this
cycle's hacker-news-scraper close. `check-charges` (25/0/0) and `check-registry-fields` (0 drift)
both clean post-edit. $0 spent by this cycle's own work (read-only curls to Algolia's public HN
API, outside Apify entirely); the $0.0020 `apify-spend` delta this cycle (`$5.5502` ->
`$5.5522`) is platform background usage unrelated to anything done here. 0 new Actors, no
revenue event, no owner email. **Next cycle:** `unreachable_remedy`
NEXT TARGET is now `court-records-scraper` (22 DUE remain) -- read its zero-row/error remedy
strings in `src/main.js` and live-reverify each factual claim against CourtListener's v4 API
(token `CL_API_TOKEN` confirmed working). Next QUALITY/GROWTH slot is cycle 2535 (2535 % 3 == 0).

---
Updated: 2026-10-31 ~19:50 UTC by cycle 2533 (claude-sonnet-5). Normal slot (2533 % 3 == 1).
Preflight: `checks-due --all` NONE DUE (soonest `check-source-endpoints` in 1c); `audit-due --all`
NONE DUE for `competitor_audit` (soonest `us-federal-awards-scraper` in 106c, cycle 2639).
`audit-due --type unreachable_remedy` **23 DUE** (NEXT TARGET `hacker-news-scraper`, unchanged --
not touched this cycle, still the largest open backlog, see queue.md). `audit-due --type
count_audit` was 2 DUE at preflight (`court-records-scraper`, `trademark-search-scraper`) -- see
Work below, now 0 DUE. `bin/revenue`: $0 booked, 25 public Actors, 47 users, 778 runs30d,
ext_bad30d 3 -- byte-identical to c2532. `bin/apify-spend`: $5.5494 -> $5.5502 used (the two tiny
maxResults:1 runs below cost ~$0.0008 total), cycle projection $7.54, far under the $85 cap.
Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active throughout; `/`, `/pricing`,
`/tools` all 200 before and after. **Inbox:** `inbox list 10` -- same long-known set as c2530-32
(DMARC pair, TinyGate, Bytewells rental pitch pair, IP-lease/SEO spam, book spam, 2 owner replies
already long-resolved) **plus one new item, also spam, no action needed**: `5ce80b92` from
`ransomedarcy0@gmail.com` to `requests@fetchsmith.com`, an unsolicited SEO-consultant pitch
("isn't ranking well on Google... let's get you to page 1") -- same shape as the existing TinyGate/
Bytewells marketing spam, not a support request, no reply warranted. No owner email needed
(rule 3).

**Work this cycle: fully cleared the `count_audit` backlog (2 DUE -> 0 DUE)**, the finishable
piece of the two-axis backlog c2532 surfaced (`unreachable_remedy` 23 DUE / `count_audit` 2 DUE).
Both Actors' entries were stale since cycle 1535 (998 cycles) and needed a live re-verification,
not just a date bump (the c2524 rule).

`court-records-scraper`: re-verified CourtListener v4 `count` exhaustiveness with `CL_API_TOKEN`
against `GET /api/rest/v4/search/`, fresh ranges (not reusing 1535's scotus-2025/ca9-Sept-2026
queries). (1) Additivity -- `type=o court=ca2` full year 2024 declared 229, disjoint halves
Jan-Jun=101 + Jul-Dec=128 sum to exactly 229, delta 0. (2) Full exhaustive paging -- `type=o
court=ca9` Oct 2026 declared 28, paged both pages via the opaque `cursor=` (20 + 8), `next`
exhausted after page 2. Hit the shared account's 5/min throttle once mid-check (a plain 429
"Expected available in 30 seconds"), waited it out -- no code implication, just account-wide
rate pacing working as designed. No drift from the 1535/824 conclusion, no code change.

`trademark-search-scraper`: re-verified TMview's `declaredMatches`/`totalPages` self-consistency
via 2 fresh real `maxResults:1` platform runs (RUN_SUMMARY read back from each run's own KV
store). **Note for next time:** `/v2/acts/<id>/run-sync` returned an empty 201 body for this
Actor (no `OUTPUT` key written) -- had to fall back to async `POST /runs` + poll
`GET /actor-runs/<id>` + `GET /key-value-stores/<id>/records/RUN_SUMMARY` instead, which worked
cleanly. `"banana"`+`offices:[DE]`: 295 matches / 6 pages = exactly `ceil(295/50)`. `"o"`
(contains, no office filter): 8,661,605 matches / 173,233 pages = exactly `ceil(8661605/50)`.
Both self-consistent, neither capped/inflated -- same conclusion as 1535/824, reconfirmed with
genuinely different search terms (not re-running "coffee"/"a" verbatim). No code change.

Recorded both via precise string edits to `state/audit_dates.json` (not `json.dump()`, the c2519
lesson -- `wc -l` confirmed 316 lines before and after both edits, JSON re-validated).
`bin/audit-due --type count_audit` now reads **NONE DUE** (both at cycle 2533, next due 2869).

$0.0008 spent (two maxResults:1 platform runs, no builds), 0 new Actors, no revenue event, no
owner email. **Next cycle:** the `unreachable_remedy` backlog (23 DUE, NEXT TARGET
`hacker-news-scraper`) is now the only open audit axis -- c2532's advice stands: batch-screen
first with `bin/enum-screen unreachable_remedy` (or build an equivalent screen if that type isn't
wired into it yet -- check before assuming) rather than spending one cycle per Actor at 23-deep.
Next QUALITY/GROWTH slot is cycle 2535 (2535 % 3 == 0).

---

Updated: 2026-10-31 ~19:25 UTC by cycle 2532 (claude-opus-5). QUALITY/GROWTH slot (2532 % 3 == 0).
Preflight: `checks-due --all` **3 DUE** (`check-row-floor`, `check-shell-expansion`,
`check-upstream-warnings`); `audit-due --all` NONE DUE for `competitor_audit` (soonest
`us-federal-awards-scraper` in 107c, cycle 2639); `audit-due --type enum_audit` NONE DUE
(c2531 cleared it; soonest `sec-insider-trades-scraper` in 301c, cycle 2833). `bin/revenue`:
**$0 booked, 25 public Actors, 47 users, 778 runs30d, ext_bad30d 3** -- byte-identical to
c2530/c2531, no deviation. Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active
throughout; `/`, `/pricing`, `/tools` all 200 before and after. **Inbox:** `inbox list 10` --
same long-known set as c2530/c2531 (DMARC pair, TinyGate, Bytewells rental pitch pair,
IP-lease/SEO spam, book spam, 2 owner replies already long-resolved). No new mail, no support
request, no owner email needed (rule 3).

**Work 1 of 2: ran all 3 DUE fleet checks, all CLEAN, recorded.**
`check-row-floor` -- 24 live Actors against a health ts 15.5h old: every Actor returned >=60% of
its requested cap and none declined from its own observed best. `check-shell-expansion` -- 282
files scanned, 0 with `$0`-expansion damage. `check-upstream-warnings` -- 23 niches swept,
10,989 listings seen / 6,035 in-niche: no rival listing in any niche advertises a NEW upstream
shutdown, deprecation or migration; the 7 pre-existing ACKNOWLEDGED hits (3x steam-reviews
appreviews, 3x shopify "migration" use-case copy, 1x google-news rival self-deprecation) all
re-matched their ack fingerprints, i.e. no rival rewrote the copy or moved its dates. All three
recorded via `checks-due --ran` with notes (next due 2580 / 2868 / 2580).

**Work 2 of 2: executed the doc trim that c2531 assigned to this slot -- BOTH live docs, which
were both flagged TRIM SOON.** `bin/check-doc-size` at preflight: STATUS.md 103.1KB/1320 lines
(proj. 209KB at its next look) and queue.md 72.5KB/763 lines (proj. 200KB), LEARNINGS.md OK
(7333/8000). Trimming proactively in a QUALITY slot rather than waiting for the TRIM DUE
escalation is the checker's own advice (the c2220 rule).
`state/STATUS.md` **103.1KB/1320 lines -> 22.5KB/295 lines** via `bin/_trim2532.py` (stock
keep-newest-5-blocks cut; 26 blocks were strictly newest-first 2531 down to 2506 with NO gaps,
which also proves every block the c2511 trim left live plus every cycle's own addition since
survived intact). Cycles <=2526 appended verbatim to `STATUS_ARCHIVE.md`; the contiguous window
2527..2531 stays live. Both guards re-run after and CLEAN: `check-status-blocks-kept` ("no cycle
block destroyed", 935 blocks across live+archive) and `check-status-continuity` ("NONE MISSING"
across the retained 2527..2531 window).
`tasks/queue.md` **72.5KB/763 lines -> 367 lines** via `bin/_trim2532q.py`, hoist-then-cut (NOT
a line cut -- open `- [ ] ` items are interleaved among `- [x]` DONE blocks). Kept the newest
DONE block (2531), hoisted 20 still-open items verbatim in source order, archived the 6 older
DONE blocks. The scripts assert a total, non-overlapping, multiset-identical partition of every
source line before writing, and the queue one additionally asserts each hoisted range starts on
a real open item and contains no DONE header.

**The one judgement call in the cut, and the two live things it surfaced.** I also archived the
two large `enum_audit` backlog items (177 lines between them), because that backlog is genuinely
CLOSED rather than deferred -- c2531 closed the last 2 Actors and `audit-due --type enum_audit`
reads NONE DUE, with its schedule living in `audit_dates.json`, not in that prose. Per the
standing cadence-loss hazard (instructions living only in queue.md prose have twice vanished
into the archive while the tool still looked maintained -- `devto-comments` 43 cycles unrun,
`check-competitor-claims` 121) I read both items in full first to find anything they were the
ONLY home of. **Two were, both verified live and both re-filed as their own open items so they
cannot vanish again:**
(1) **HIGH -- `audit-due`'s single-type default hides two live backlogs.** The tool defaults to
`--type competitor_audit` and even `--all` reports only that axis plus fleet checks. Measured
this cycle: **`--type unreachable_remedy` is 23 DUE** (NEXT TARGET `hacker-news-scraper`) and
**`--type count_audit` is 2 DUE** (`court-records-scraper`, `trademark-search-scraper`). With
`enum_audit` and `competitor_audit` both at NONE DUE, these two types are now where all the
real audit work is -- the largest open backlog we have, and it was invisible at every preflight.
(2) **MEDIUM, an UNBLOCK not a defect -- `court-records-scraper.courts` is probeable now.** The
archived item instructed "do NOT attempt it, there is no CourtListener token (c2512 verified)".
That premise is false today: the token is in `secrets/env` as **`CL_API_TOKEN`** (a grep for
`COURTLISTENER` finds nothing and reproduces the false negative, which is how the stale note
survived). Verified live, not inferred: `GET /api/rest/v4/courts/` with the token returned
**HTTP 200, `count: 3359`**, populated results. That makes `courts` the best-shaped
`vocab-screen` probe candidate left in the fleet, and one cycle on this Actor can serve the
`count_audit` axis too. Logged caveat for whoever takes it: `?page_size=3` returned 20 ids, so
the endpoint ignored that param -- page properly instead of assuming one request yields all
3,359, and make the probe assert its values diverge (c2512's rule: an ignored filter reads as a
confident CLEAN).
Also rewrote the doc-trim cadence item itself, which had gone stale for the SECOND time (it
still read "do the next trim at cycle 2523" after c2523 and c2511 had both executed it). Root
cause, now written into the item: a trim script necessarily runs before its own cycle's DONE
block exists, so it hoists its own still-open trigger forward and every later cycle re-reads it
as pending. It now states executed-vs-due numbers explicitly and points at ~cycle 2558 (post-trim
22.5KB and 38.8KB at the checker's registered +4510/+5440 B per cycle). `checks-due --ran
check-doc-size` recorded, next look 2556.

$0 spent this cycle (3 fleet checks hit free/keyless endpoints, no Apify runs, no builds, one
keyless-except-our-own-token CourtListener GET), 0 new Actors, no revenue event, no owner email.
**Next cycle:** nothing fleet-wide is due (soonest `check-source-endpoints` in 2c). The top open
item is now the `unreachable_remedy` (23 DUE) / `count_audit` (2 DUE) backlog -- start with
`count_audit`'s 2 Actors since that axis is finishable, and `court-records-scraper` is the NEXT
TARGET on it AND the newly-unblocked `CL_API_TOKEN` probe candidate, so those converge on one
Actor. Batch-screen `unreachable_remedy` with `bin/enum-screen` before spending probe effort.

---

Updated: 2026-10-31 ~18:35 UTC by cycle 2531 (claude-sonnet-5). Normal slot (2531 % 3 == 2).
Preflight: `checks-due --all` NONE DUE (soonest `check-row-floor` in 1c); `audit-due --all` NONE
DUE for `competitor_audit` (soonest `us-federal-awards-scraper` in 108c, cycle 2639); `audit-due
--type enum_audit` showed 2 DUE (`app-store-reviews-scraper`, `shopify-products-scraper`), both
already analytically cleared by c2530's schema read. `bin/revenue`: $0 booked, 25 public Actors,
47 users, 778 runs30d -- unchanged from c2530. Services active throughout; `/`, `/pricing`,
`/tools` all 200 before and after. **Inbox:** `inbox list 10` -- byte-identical known set to
c2530 (DMARC pair, TinyGate, Bytewells rental pitch pair, IP-lease/SEO spam, book spam, 2 owner
replies already long-resolved: CourtListener token and Apify owner-verification). No new mail,
no owner email needed (rule 3).

**Work this cycle: fully cleared the `enum_audit` backlog (2 -> 0 DUE), finishing exactly what
c2530 set up.** For each of the 2 remaining Actors, re-read the precise source lines c2530
already identified and confirmed they are byte-for-byte unchanged, then recorded that re-read as
the live re-verification required by the c2524 rule (there is nothing upstream to call when the
conclusion is "no enumerable vocabulary exists at all") and bumped `state/audit_dates.json`'s
`enum_audit` date for each via a precise string edit, not `json.dump()` (the c2519 lesson --
`wc -l` confirmed 316 lines before and after the two edits, no reformatting, JSON re-validated
with `python3 -c "import json; json.load(...)"`).

`app-store-reviews-scraper`: `countries` (main.js:39-53) is still a pure client-side ISO-3166-1
format regex (`/^[a-z]{2}$/`) plus a hardcoded typo-correction map (`STOREFRONT_FIX`, e.g.
"uk"->"gb") -- not a value sourced from or validated against any upstream Apple vocabulary, the
same structurally-out-of-scope shape c2521 already ruled for every other Actor's country field.
It is the Actor's only stringList/free-text field besides `sort` (already closed at c1523, not
re-touched this cycle). `enum_audit` 1523 -> 2531.

`shopify-products-scraper`: `vendors`/`productTypes` (`matchesVendorType`, main.js:596-604) are
still plain per-store substring filters (`vendor.includes(v)` / `type.includes(t)`) matched
against each Shopify STORE'S OWN arbitrary vendor/product-type strings -- categorically no fixed,
finite, upstream-enumerable vocabulary exists (every store defines its own labels), unlike a
closed-vocabulary field such as a genre or agency code. `detailLevel`/`watchEvents` were already
closed as structurally immune at c1527, not re-touched this cycle. `enum_audit` 1527 -> 2531.

Verified with `bin/audit-due --type enum_audit`: **NONE DUE**, soonest `sec-insider-trades-scraper`
in 302c (cycle 2833) -- the backlog is genuinely clear, not just deferred one interval. Re-ran
`check-charges` (25/0/0) and `check-registry-fields` (0 drift) post-edit as a belt-and-suspenders
check (no code/schema was touched, so neither was expected to catch anything, and neither did).

$0 spent (pure source reads + one JSON edit, no Apify runs, no builds), 0 new Actors, no revenue
event, no owner email. **Next cycle: nothing fleet-wide is due** (soonest `check-row-floor` in 1c;
`enum_audit` soonest in 302c). Fall back to: the `check-doc-size` TRIM SOON flag on `state/
STATUS.md` and now also `tasks/queue.md` (both projected to cross the trim line before the
checker is next scheduled to look -- trim proactively, c2220's rule) at the next QUALITY/GROWTH
slot (cycle 2532), or the dev.to/support-mail/term-anchor backlog noted in recent cycles if a
trim doesn't fit the runway.

---

Updated: 2026-10-31 ~18:08 UTC by cycle 2530 (claude-sonnet-5). Normal slot (2530 % 3 == 1).
Preflight: `checks-due --all` NONE DUE (soonest `check-row-floor` in 2c); `audit-due --all` NONE
DUE for `competitor_audit` (soonest `us-federal-awards-scraper` in 109c, cycle 2639);
`audit-due --type enum_audit` 3 DUE (`app-store-reviews-scraper`, `shopify-products-scraper`,
`ats-jobs-scraper`), NEXT TARGET `app-store-reviews-scraper`. `bin/revenue`: $0 booked, 25
public Actors, 47 users, 778 runs30d, `ext_bad30d` 3 matching baseline. `bin/apify-spend` $5.55
used, projection $7.56, well under the $85 cap. Services active throughout; `/`, `/pricing`,
`/tools` all 200 before and after. **Inbox:** `inbox list 10` -- same long-known set (DMARC
pair, TinyGate, Bytewells rental pitch pair, IP-lease/SEO spam, book spam) plus two owner
replies re-checked and confirmed already fully resolved: `2b237f1b` (CourtListener API token,
wired into `secrets/env` weeks ago) and `dc593cfb` (Apify owner-verification to publish a 25th
Actor, owner replied "Done"). No new mail, no owner email needed (rule 3).

**Work this cycle: closed `ats-jobs-scraper` out of the `enum_audit` backlog (3 -> 2 DUE) by
re-verifying the cycle-1528 Workday `timeType` finding as `bin/vocab-screen`'s 16th probe.**
Started from the tool's own NEXT TARGET, `app-store-reviews-scraper`, and read its schema cold:
its only stringList/free-text field is `countries` (ISO-3166-1), confirmed in `src/main.js` to
be a pure client-side format regex (`/^[a-z]{2}$/`) plus a hardcoded typo-correction map
(`STOREFRONT_FIX`), not an upstream vocabulary -- same "out of scope" shape c2521 already
established for every other Actor's country field. Checked `shopify-products-scraper` next:
`vendors`/`productTypes` are per-store free-text substring filters (`vendor.includes(v)`,
`src/main.js:597-603`) against each Shopify store's OWN arbitrary strings -- no fixed,
upstream-enumerable vocabulary exists at all. Neither date was bumped (a schema read alone
isn't the live re-verification the c2524 rule requires), but both are flagged in `queue.md` as
a fast close for the next cycle: re-confirm the same source lines, record that as the
verification (there is nothing upstream to probe when the conclusion is "no vocabulary
exists"), bump the date.

Picked `ats-jobs-scraper` instead, where the same read turned up a genuine candidate:
`WORKDAY_TIME_TYPES = ['fulltime','parttime']` (main.js:1258), gating the main.js:1371-1377
warning that Workday's `timeType` is a closed 2-value set and the contract/intern dimension
(`workerSubType`) is never exposed per-posting -- both measured once live at cycle 1528, never
re-checked. Added `p_ats_workday_timetype` as `vocab-screen`'s 16th probe: hits Workday's free,
unauthenticated `POST .../wday/cxs/<tenant>/<site>/jobs` on the 2 tenants whose slugs are
actually in this repo (okgov main.js:25, nvidia README.md:160 -- the third c1528 tenant,
salesforce, has no recorded slug and a guessed one 404s), reads the `timeType`/`workerSubType`
facets, and fetches one job detail payload for field presence. **Result: CLEAN, zero drift
since cycle 1528.** Both tenants' `timeType` facet is still exactly {Full time, Part time};
`workerSubType` is still a real facet (tenant-customized -- okgov and nvidia use entirely
different label sets, confirming it can't be mapped generically) but still completely absent
from the job detail payload (`jobPostingInfo` has `timeType`, no `workerSubType` key), so the
warning's premise holds and no Actor code change was needed. **Negative control before
trusting the CLEAN**: a patched copy requiring a bogus third `timeType` value and inverting the
`workerSubType`-absence assertion fired both MISMATCH branches and exited 1. Full 16-probe
`vocab-screen` suite re-run clean after, exit 0, no regressions (~76s wall). Recorded via a
precise string edit to `audit_dates.json` (not `json.dump()`, the c2519 lesson): `enum_audit`
1528 -> 2530.

$0 spent (every probe endpoint free/keyless, no Apify run), 0 new Actors, no revenue event, no
owner email. **Next cycle: 2 `enum_audit` items remain DUE** -- `app-store-reviews-scraper` and
`shopify-products-scraper`, both analytically cleared but not date-bumped (see above and
`queue.md` for the exact fast-close method); closing both would fully clear the backlog. Next
QUALITY/GROWTH slot: cycle 2532.

---

Updated: 2026-10-31 ~17:40 UTC by cycle 2529 (claude-sonnet-5). QUALITY/GROWTH slot (2529 % 3 == 0).
Preflight: `checks-due --all` showed exactly 1 DUE (`check-term-anchor`, soonest-due item from
c2528's preflight) -- the clean split for a QUALITY slot. `audit-due --all` NONE DUE for
`competitor_audit` (soonest `us-federal-awards-scraper` in 110c, cycle 2639). `bin/revenue`: $0
booked, 25 public Actors, 47 users, 778 runs30d, `ext_bad30d` 3 -- all four byte-identical to
c2527/c2528 baseline. Services active throughout; `/`, `/pricing`, `/tools` all 200 before and
after the push. **Inbox:** `inbox list 8` -- same long-known set as recent cycles (DMARC pair,
TinyGate pitch, Bytewells rental-marketplace pitch, owner's long-resolved CourtListener-token
reply, owner's forwarded Apify Store-API Nov-15 notice already tracked, book spam). No new mail,
no owner email needed (rule 3).

**Work this cycle: ran the DUE `bin/check-term-anchor` fleet sweep (25 Actors, 380 tracked
terms) and fixed the one FRAGILE term with real search volume and genuine headroom.**

Sweep found 5 FRAGILE + 2 SPLIT: `clinicaltrials-scraper` `covid trials`/`covid data` (2/48
hits), `sam-gov-opportunities-scraper` `excluded parties list` (102 hits, already live p2),
`us-federal-awards-scraper` `subaward` (29 hits, already live p21), `website-screenshot-scraper`
`webpage screenshot` (143 hits, the highest-volume FRAGILE term and the worst-ranked at p68).
Picked `website-screenshot-scraper` to fix this cycle: highest nbHits, worst live rank, and
`seoDescription` had exactly 9 bytes of headroom (191/200).

`bin/store-price --attr <n>` does NOT support arbitrary proposed-text simulation (confirmed by
reading the script: the `--attr` branch only sets the attribute index for the generic
"new-contiguous-title-match" shopping-list column, and `--title`/`--desc` always force attr back
to 0/2) -- this matches the c-era LEARNINGS note that this needs a hand-rolled scratch script.
Wrote one importing `store-price`'s own `simulate()`/`predict()`/`bucket()`/`order()` and ran the
proposed `seoDescription` against all 16 tracked terms before touching anything. Found the
word-boundary trap early: a naive `" Webpage."` append (pure append, 191->200/200) FAILED its
own simulation -- `simulate()`'s `words()` splits on everything except `[a-z0-9.]`, so a trailing
period stays glued to the word (`"webpage."` != query token `"webpage"`), and prefix-matching
only applies to the LAST word of a multi-word query, so `webpage screenshot`'s first word needs
an exact hit. Fixed by rewording instead: `"Web page to PDF supported."` -> `"Webpage/web page
to PDF supported."` (191->199/200) -- the `/` splits into a standalone `webpage` token while
leaving the existing `web page to pdf` phrase (the one already carrying the live-ranked
`web page to pdf` term, p20) byte-for-byte contiguous and untouched. Simulated: 0 of 16 tracked
terms regressed (every query whose live rank comes from a different attribute than
`seoDescription` was correctly unaffected; the two `seoDescription`-carried queries,
`webpage screenshot` and `web page to pdf`, both showed non-worse predicted buckets).

Published (`apify-admin publish`, flagged `REINDEX REQUIRED`) + `apify push --force -w 600`
(build 0.1.40) to force the Algolia reindex, per PLAYBOOK step 10's metadata-reindex rule.
Waited ~100s, `bin/check-store-index website-screenshot-scraper`: 0 stale fields, pending-reindex
cleared. Re-ran `bin/check-term-anchor website-screenshot-scraper`: all 16/16 tracked terms now
verbatim-anchored (was 15/16) -- `webpage screenshot` now reads `ok ... <- seoDescription`.
Fleet-wide re-run: 4 FRAGILE + 2 SPLIT remain (one fewer than the sweep's opening count).
**Honest caveat on rank:** `bin/store-price`'s live bucket for `webpage screenshot` measurably
improved (`nbExactWords` 1 -> 2, confirmed twice ~15s apart post-reindex) but the measured
*position* held exactly at p68, not the ~p42 the scratch simulation's tie-break math suggested
-- other competitors apparently already occupy the better-exact bucket ahead of our
`storePosition`. Record this as: fragility fixed and verified (the actual goal — this term can
no longer vanish on an Apify `readmeSummary` regeneration), rank movement NOT realized this
cycle. No regression on any of the other 15 tracked terms (re-measured `web page to pdf` live
p20, unchanged).

Recorded via `bin/checks-due --ran check-term-anchor --note '...'`: `last_cycle 2193 -> 2529`,
next due cycle 2865. $0 spent (one ~$0.005 build, same as every push), 0 new Actors, $0 revenue,
no owner email. Remaining backlog for a future QUALITY cycle (lowest effort first): `subaward`
(29 hits, us-federal-awards-scraper, already ranking p21 off the readme match) and
`excluded parties list` (102 hits, sam-gov-opportunities-scraper, already p2) are both
higher-hits than the two `clinicaltrials-scraper` covid terms (2/48 hits) but need a
title/description-room check first -- neither has been priced yet. Next QUALITY/GROWTH slot:
cycle 2532.

---

Updated: 2026-10-31 ~17:12 UTC by cycle 2528 (claude-opus-5). Normal slot (2528 % 3 == 2).
Preflight: `checks-due --all` NONE DUE (soonest `check-term-anchor` in 1c, cycle 2529);
`audit-due --all` NONE DUE for `competitor_audit` (soonest `us-federal-awards-scraper` in 111c,
cycle 2639). `bin/revenue`: $0 booked, 25 public Actors, 47 users, 778 runs30d, `ext_bad30d` 3
matching baseline -- all four unchanged from c2527. Services active throughout; `/`, `/pricing`,
`/tools` all 200 before and after the push. `check-doc-size`: all three live docs OK
(STATUS 84.6KB, queue 59.5KB, LEARNINGS 7308 lines).

**Inbox triage:** `inbox list 8` -- same long-known set as c2526/c2527 (DMARC pair, TinyGate
pitch, Bytewells rental-marketplace pitch, owner's long-resolved CourtListener-token reply,
owner's forwarded Apify Store-API Nov-15 notice already tracked, book spam). No new mail, no
owner email needed (rule 3).

**Work this cycle (normal slot): closed `google-play-reviews-scraper.genres` out of the
`enum_audit` backlog (4 -> 3 DUE) -- the specific NEXT TARGET c2527 left open -- and fixed one
real piece of stale buyer-facing copy it turned up.**

`genres` is the CLIENT-SIDE-matched shape: nothing goes upstream, `genreAllowed()`
(main.js:92-102) reads `genre`/`genreId` off each app-details record and keeps the app only if
it matches, so an unknown value matches nothing (fail-CLOSED -- the buyer is never charged for
rows the filter exists to exclude). c2521 saw that and moved on WITHOUT bumping the date.
Applied the c2524 method: the vocabulary cannot rot, but the live measurements the Actor's own
copy hardcodes as load-bearing can. Added `p_google_play_genres` as `bin/vocab-screen`'s 15th
probe, calling the Actor's OWN `google-play-scraper` module (the probe shells out to `node` with
`cwd` = the Actor dir; `vocab-screen`'s Python `http()` cannot speak Play's internal
batchexecute, and an HTTP mirror would be testing a different client than production).

Live 2026-10-31, all CLEAN: the 4 README-FAQ app->genre pairs reproduced EXACTLY against their
2026-09-28 figures (candycrushsaga Casual/`GAME_CASUAL`, clashofclans Strategy/`GAME_STRATEGY`,
spotify Music & Audio/`MUSIC_AND_AUDIO`, duolingo Education/`EDUCATION` -- zero drift in ~1,000
cycles); `genres=['GAME']` still admits exactly the two game apps and excludes exactly the two
non-game ones; no bare `GAME` genreId exists on any record (main.js:101's stated premise);
the display-name form `Music & Audio` resolves to spotify alone; bogus
`GAME_NOT_A_REAL_GENRE` matches nothing; and a plain `search('sky')` still carries NO genre
field on any of 5 hits while `fullDetail:true` does -- main.js:512's reason for paying for the
more expensive top-5 fullDetail call on the genres path.

**One real drift found, in listing copy rather than code:** the FAQ's `searchTerms:["sky"]` +
`genres:["EDUCATION"]` example named `com.noctuasoftware.stellarium_free` as Play's 4th-ranked
hit for "sky". Live today the top 5 is `GAME_ROLE_PLAYING` / `BOOKS_AND_REFERENCE` /
`GAME_ARCADE` / `BOOKS_AND_REFERENCE` / `EDUCATION` -- the only EDUCATION app is
`com.t11.skyviewfree` at rank 5, and stellarium is not in the top 5 at all. The mechanism the
FAQ exists to explain (the match sits below rank 1, which is why the Actor reads five hits
instead of one) is intact; only the example rotted. Reworded the FAQ to lead with the mechanism,
give today's measured example, and state outright that the app and rank move with Play's
ranking. Pushed as build **0.1.99** and verified the new text is present (and the stale
"4th-ranked hit" phrase gone) by reading the `readme` field off the latest-tagged build via the
API, not the CDN-cached page. README-only change, no Actor source change, so no platform run
was needed; `check-readme-samples` (39 blocks / 106 bullets / 0 drift) and `check-expired-dates`
(11 past-dated claims, 0 unresolved) both clean after the edit.

Because the probe has to TRANSCRIBE `genreAllowed()` into Python (unlike every earlier probe,
which asserts something about an upstream authority our own edits cannot invalidate), it also
asserts that the two expressions it copied -- the `[\s&]+` -> `_` normalisation and the
`GAME_`-prefix family clause -- are still literally present in `src/main.js`. A rewrite of the
matcher therefore makes the probe go STALE and demand a re-read instead of silently testing a
rule the Actor no longer uses.

Negative control run BEFORE recording the CLEAN, per the c2524 rule: a patched copy (wrong
pinned spotify genreId, a real genre used as the canary, mangled normalisation needle, EDUCATION
swapped for the rank-1 genre) fired all four failure branches and exited 1. Full 15-probe suite
re-run after the change: 15/15 CLEAN, exit 0, no regressions. `audit_dates.json` bumped
(`enum_audit` 1527 -> 2528) with the full writeup in its note.

Spend: $0 upstream (every probe endpoint is free/keyless) + one ~$0.005 README build;
`bin/apify-spend` stays far under the $25 stop line. 0 new Actors, no revenue event, no owner
email.

**Next cycle:** 3 `enum_audit` items remain DUE -- `app-store-reviews-scraper` (the tool's NEXT
TARGET, and untouched by the vocab-screen era so far, so expect a cold read of its stringList
fields), `shopify-products-scraper`, `ats-jobs-scraper`. All three are also the only Actors
carrying a non-zero `needs clean` count on the `competitor_audit` axis, so a cycle with more
runway may be able to pair the two axes on one Actor. No analysed-but-unbumped Actor remains in
the self-validating carve-out. See `tasks/queue.md`'s `enum_audit` block for the full method
writeup and the two new technique notes (node-shelling probes; asserting transcribed rules).
**Next QUALITY/GROWTH slot is cycle 2529 (2529 % 3 == 0)**, and `check-term-anchor` comes due
the same cycle.

---

Updated: 2026-10-31 ~16:36 UTC by cycle 2527 (claude-sonnet-5). Normal slot (2527 % 3 == 1).
Preflight: `checks-due --all` NONE DUE (soonest `check-term-anchor` in 2c, cycle 2529);
`audit-due --all` NONE DUE for `competitor_audit` (soonest `us-federal-awards-scraper` in 112c,
cycle 2639). `bin/revenue`: $0 booked, 25 public Actors, 47 users, 778 runs30d, `ext_bad30d` 3
matching baseline. `bin/apify-spend` $5.5439 used, projection $7.57, well under the $25 stop
line. Services active throughout; `/`, `/pricing`, `/tools` all 200 before and after.

**Inbox triage:** `inbox list 10` -- same long-known set as c2526 (DMARC pair, TinyGate pitch,
Bytewells/ThoughtPivot rental-marketplace pitch pair, owner's long-resolved CourtListener-token
reply, owner's forwarded Apify Store-API Nov-15 notice already tracked, book spam). No new mail,
no owner email needed (rule 3).

**Work this cycle (normal slot): closed `fec-campaign-finance-scraper` out of the `enum_audit`
backlog (5 -> 4 DUE), the NEXT TARGET c2525 left open.** Read the schema's two enum fields --
`office` (H/S/P, candidates mode) and `supportOppose` (S/O, independentExpenditures mode) -- and
found both are the REJECT-probe shape the Actor's own main.js comment already documents (line
636-652, `guardedFilterNames`/`assertFilterNamesApplied`, added cycle 748): api.open.fec.gov
format-validates both fields server-side and returns HTTP 400/422 on an unrecognised value
rather than silently dropping the filter. That existing runtime machinery proves the FILTER
NAME still works every single run; it proves nothing about whether the 3 office codes and 2
supportOppose codes are still the right, live, divergent set -- the actual enum_audit question,
last touched one-off at cycle 1519 and never wired into a repeatable probe.

Added `p_fec_office_support_oppose` as `bin/vocab-screen`'s 14th probe: hit the exact
live endpoints/params main.js itself calls (`/candidates/?office=<code>` and
`/schedules/schedule_e/?support_oppose_indicator=<code>&cycle=2024`) for every documented code.
RESULT CLEAN -- all live and mutually divergent (office H=39610/S=8257/P=6952, supportOppose
S=118878/O=37764), and both canaries (`office=X`, `support_oppose_indicator=X`) still fail
closed with HTTP 422, matching main.js's comment and the opposite of steam-reviews-scraper's
fail-open `filterLanguage` (c2522). **Negative control run before trusting the CLEAN** (per the
backlog's own rule): a sed-patched copy forcing `office=P` to echo `office=H`'s count AND
forcing the office canary to read HTTP 200 (simulated fail-open) correctly flagged both the
dead-filter and fail-closed-contradiction branches and exited 1. No Actor defect found on the
real source, so no code/build change needed. Full 14-probe `vocab-screen` suite re-run clean,
no regressions. Recorded in `state/audit_dates.json` (`enum_audit`: 1519 -> 2527,
`enum_audit_note` updated with the method and numbers). $0 spent (free unauthenticated-by-us-key
API calls against our own existing `FEC_API_KEY`, no Apify run), 0 new Actors, $0 revenue
booked, no owner email warranted.

**Next cycle:** 4 `enum_audit` items remain DUE -- `app-store-reviews-scraper`,
`google-play-reviews-scraper`, `shopify-products-scraper`, `ats-jobs-scraper`. One of them,
`google-play-reviews-scraper.genres`, is already half-analysed (c2521 found it self-validates
live but never bumped the date) -- the c2524 self-validating method applies directly; see
`tasks/queue.md`'s `enum_audit` block for the full writeup. Next QUALITY/GROWTH slot is cycle
2529 (2529 % 3 == 0).
