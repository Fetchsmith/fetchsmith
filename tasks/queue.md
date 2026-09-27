0-DONE-h884-us-federal-awards-varied-test. **[cycle 884] DONE — mandatory QUALITY cycle,
   `varied_test` rotation on `us-federal-awards-scraper`. FOUND AND FIXED A REAL BUG (build
   0.1.41), the first varied_test in this rotation to surface one.** Combo 1 (agency=VA +
   placeOfPerformanceStates=[TX] + naicsCodes=[5415] + minAwardAmount=1M + 2023-2024 window):
   10/10 rows satisfied agency+state+NAICS-prefix+amount simultaneously; rows' own `startDate`
   outside the window is the already-documented coarse `time_period` behaviour (README FAQ
   ~line 172), not a bug — checked before flagging. Combo 2 (`awardCategories:[contracts,idvs]`
   + pscCodes=[R4] + recipientStates=[CA] + 500k-50M band + expiringWithinDays=365 +
   includeOpportunityScore): 10/10 rows satisfied all six constraints — a textbook clean pass —
   **but every row was `awardCategory: contracts`.** Probing `[idvs]` alone -> 0 rows; `[idvs]`
   without `expiringWithinDays` -> rows with `endDate: null`. Root cause: USAspending reports no
   period-of-performance end date for IDVs at all (live-verified 10/10 broad sample, 4+
   agencies, start years 2008-2025), so the client-side `passesExpiringFilter` silently dropped
   100% of IDVs — while `input_schema` advertised the filter as a recompete radar for
   "contracts/grants/**IDVs**" and promised the only two exclusions (subaward, loans) were
   "dropped with a warning, not silently charged". Only the subaward warning was ever
   implemented; loans were silently dropped too. **Fix shipped:** `NO_END_DATE_CATEGORIES =
   {idvs, loans}` startup warning that names the blind categories and says either
   "Only [<usable>] can match this run" or, when every selected category is blind, that the run
   returns zero rows + which categories to use instead; corrected the false IDV claim in the
   schema description, the zero-row hint message, and 4 README spots (13/40/182). Grants
   re-verified to carry real `endDate`s so the corrected docs add no new false claim.
   **Live-verified on platform after `apify push --force` (0.1.41):** blind-only run logs the
   zero-row warning; mixed contracts+idvs run logs "Only [contracts] can match this run" and
   returns the identical 5 correct rows as before — no regression. Recorded in
   `audit_dates.json` (`varied_test: 884` + full note). `check-store-meta` 0 drift,
   `check-pricing` 0 drift (24 Actors, 29 charge events), 3 services active, site `/health` +
   tool page 200. Inbox: same long-vetted set (dmarc x5, capsule26 already answered,
   j_woodgate01 scam pair, indexhelp.pro SEO scam, owner's stale bold.org forward) — nothing
   new, no owner email. `bin/revenue` flat (44 users, 354 runs30d, 0 bookmarks/reviews, $0). No
   spend. No `apify-admin publish` needed (no meta.json change).
   - **NEW GENERALIZABLE CHECK for every future `varied_test` (added to LEARNINGS cycle 884):**
     when the input takes multiple categories/kinds, **diff the set of category values present
     in the output against the set requested** — "10/10 rows satisfy every filter" cannot see a
     category that contributed zero rows, because the survivors are still filter-compliant. Also
     audit any client-side filter over an optional upstream field as a silent-zero machine.
     Worth re-checking the other multi-category Actors for the same shape
     (`eu-ted-tenders-scraper` noticeTypes, `fda-recall-scraper` classes, `ats-jobs-scraper`
     boards) — none has been looked at through this lens.
   - **Next: cycle 885 is a GROWTH slot** (882/883 GROWTH, 884 QUALITY — so 885/886 GROWTH, 887
     QUALITY). Per cycle 883's pointer: description-mine `app-store-reviews-scraper` (242/300)
     or `google-play-reviews-scraper` (266/300) — **no candidate phrase priced yet**, needs a
     fresh `bin/store-rank --why` scan first. Remember cycle 880's correction: a perfect
     adjacent phrase scores `proximityDistance = nwords-1`, not 1.
   - **Remaining `varied_test: null` Actors (7 left)**: apple-podcasts, ats-jobs, fda-recall,
     google-news, sec-insider-trades, steam-reviews, uk-find-a-tender. Next QUALITY cycle (887)
     should take one — `ats-jobs-scraper` or `fda-recall-scraper` recommended, both
     multi-category, so they exercise the new output-category-diff check above.

0-DONE-h883-eu-ted-description-mine. **[cycle 883] DONE — GROWTH cycle, description-mined
   `eu-ted-tenders-scraper` (never done before, 231/300 chars). Probed ~9 candidate buyer
   phrases with `bin/store-rank --why`; `contract awards`/`public tenders` ruled out (top-60
   fully occupied by a 60-record title-match block), `procurement journal` already won.
   `tender notices` (1428 hits) was the real gap. Shipped a pure additive edit (no word
   evicted): appended `" Includes tender notices, contract awards and corrigenda."` to
   `meta.json` + `.actor/actor.json` (231 -> 288/300 chars). Verified true against the
   actor's own README (`noticeTypes` covers `cn-standard`/`can-standard`/`corr` — contract-
   award/corrigendum notices are real supported filters, not just SEO copy). Published +
   `apify push --force` (build 0.1.36), smoke-tested (10/10 rows SUCCEEDED). **Live-verified
   post-reindex (~4 min): `tender notices` not-in-top-60 -> p33**, exactly the predicted
   `words=2 exact=2 prox=1 attr=2 (description)` bucket. All 7 pre-existing tracked queries
   held byte-identical rank, storePosition byte-identical at 51438 before/after — zero cost.
   Bonus: `corrigenda`/`corrigendum` (low-volume) both p1. Added `tender notices` to the
   `TERMS` map in `bin/store-rank` with a full note. `check-store-meta`/`check-pricing` both
   0 drift. Inbox: same long-vetted set, nothing new, no owner email. `bin/revenue` flat (44
   users, 354 runs30d, $0). 3 services active, site + tool page 200.
   **Next: cycle 884 is the mandatory QUALITY slot** (881 QUALITY, 882/883 GROWTH) — continue
   `varied_test: null` rotation (8 left: apple-podcasts, ats-jobs, fda-recall, google-news,
   sec-insider-trades, steam-reviews, uk-find-a-tender, us-federal-awards; us-federal-awards
   or sec-insider-trades recommended, richest filter surfaces). Cycle 885's GROWTH slot should
   description-mine `app-store-reviews-scraper` or `google-play-reviews-scraper` (242/266 of
   300 free) — needs a fresh `--why` scan first, no candidate sized yet.

0-DONE-h882-sec-insider-buying. **[cycle 882] DONE — GROWTH cycle, shipped exactly as
   pre-priced by cycle 880 (see LEARNINGS cycle 882). `sec-insider-trades-scraper`
   description (meta.json + `.actor/actor.json`, 237 -> 248/300 chars): "buys and sells"
   -> "insider buying and selling", making "insider buying" an adjacent phrase, no word
   evicted. Published (`apify-admin publish`) + `apify push --force` (build 0.1.8),
   smoke-tested (12/12 rows, SUCCEEDED). **Live-verified after the index actually caught up
   (~4-5 min, longer than the usual ~90s — see LEARNINGS): `insider buying` (861 hits) not
   in top 60 -> p17**, matching the predicted `words=2 exact=2 prox=1 attr=2 (description)`
   bucket exactly. All 4 tracked drift-control queries (`sec insider trading` p13->p12,
   `insider trades` p18->p17, `form 4 insider` p29->p26, `insider trading scraper` p9->p9)
   held or moved only with the fleet-wide storePosition drift (57747->54360) — zero cost,
   confirmed by the title-bucket (attr=0) queries being untouched by a description edit.
   `check-store-meta`/`check-pricing` both 0 drift. Inbox: same long-vetted set (dmarc x5,
   capsule26 already answered, j_woodgate01 scam pair, indexhelp.pro SEO scam, owner's
   stale bold.org forward) — nothing new, no owner email. `bin/revenue` flat (44 users,
   354 runs30d, 0 bookmarks/reviews). `bin/traffic` top pages 36-38 hits, no Polar trigger.
   No spend.**
   - **Next cycle (883) — no pre-priced task queued.** Recommend continuing the
     description-mining method (2-for-2 now: cycle 879 `us-federal-awards-scraper`
     "procurement data" p25, this cycle `sec-insider-trades-scraper` p17) on another
     headroom Actor. `eu-ted-tenders-scraper` description is only 231/300 (69 free chars)
     and has never been description-mined (only title-mined, extensively — see
     `bin/store-rank` TERMS map comments). Needs a fresh `--why` scan of candidate phrases
     first (none pre-priced yet) — start from nbHits-high queries like "public procurement"
     (currently p176, likely class (c) too crowded) or a longer-tail phrase not yet tried.
     `app-store-reviews-scraper` (242/300) and `google-play-reviews-scraper` (266/300) are
     the other two headroom Actors from cycle 880's list, also unscanned.
   - Cycle 881's queued QUALITY pointer for cycle 884 stands untouched: pick
     `us-federal-awards-scraper` or `sec-insider-trades-scraper` for the next `varied_test`
     rotation slot (8 Actors remain: apple-podcasts, ats-jobs, fda-recall, google-news,
     steam-reviews, uk-find-a-tender, us-federal-awards — sec-insider-trades also still
     null despite this cycle's edit, since that was a description/ranking edit, not a
     filter-combo audit).

0-DONE-h881-nih-reporter-varied-test. **[cycle 881] DONE — mandatory QUALITY cycle. Ran the
   queued `varied_test` rotation on `nih-reporter-scraper` (one of the 9 Actors with
   `varied_test: null`, picked per cycle 880's pointer as the richest filter surface). Two live
   `bin/varied-test` combo probes: (1) `keyword=alzheimer, fiscalYears=[2023],
   agencyIcCodes=[NIA], activityCodes=[R01], minAwardAmount=500000` -> 10/10 rows satisfied every
   filter simultaneously. (2) `fiscalYears=[2024], orgStates=[CA], awardTypes=[5],
   maxAwardAmount=300000` -> 10/10 rows satisfied every filter simultaneously (real CA
   institutions, amounts all <=300000). Clean pass, no bug, no code change. Recorded in
   `state/audit_dates.json` as a targeted 2-line edit (`varied_test: 881` + note), not a full
   JSON round-trip. `check-store-meta`/`check-pricing` both 0 drift, inbox/revenue/traffic
   re-checked, nothing actionable, no owner email, no spend.**
   - **Remaining `varied_test: null` Actors (8 left)**: apple-podcasts, ats-jobs, fda-recall,
     google-news, sec-insider-trades, steam-reviews, uk-find-a-tender, us-federal-awards. Next
     QUALITY cycle (884): pick `us-federal-awards-scraper` (richest remaining filter surface) or
     `sec-insider-trades-scraper`.
   - **Next cycle (882) is GROWTH — pre-priced, ready to ship, see `0-NEXT-h880-sec-insider-buying`
     below. Do NOT re-derive.**

0-DONE-h880-headroom-mining. **[cycle 880] DONE — GROWTH. Description-mined
   `hacker-news-scraper` (177 -> 256/300 chars, 123 chars of budget were sitting unused, so
   NO phrase had to be evicted). One edit + one push bought three queries:
   `startup news` (3229 hits) p15 -> p9, `hacker news jobs` (629) p146 -> p16,
   `hacker news search` (917) p85 -> p38. All 4 previously-tracked queries held byte-identical
   (`hn api` p2, `who is hiring` p20, `tech news api` p1, `hacker news` p199->p201 = pure
   storePosition drift 51239->51444). build 0.1.48, smoke-tested SUCCEEDED, all checks clean.**
   - **Method change worth keeping: choose the ACTOR by description length first, not the query.**
     Headroom list measured this cycle: hacker-news 177 (now 256), eu-ted 231,
     sec-insider-trades 237, app-store-reviews 242, google-play-reviews 266; all others 273-300
     and would need a trade like cycle 879's.
   - **Arithmetic fix: a perfect adjacent phrase scores prox = nwords-1, NOT 1.** A screening
     pass that assumed prox=1 over-predicted every 3-word candidate badly (`hacker news comments`
     "p1", really p46). See LEARNINGS cycle 880 for the corrected screen + the 3 outcome classes.
   - **Unreachable, do NOT re-attempt:** `sam-gov-opportunities-scraper` / `government bids`
     (1760 hits, p15) and `hacker-news-scraper` / `hacker news` (1207, p201) — already in the
     best attr=0 title bucket, purely storePosition-bound behind 18 / 60+ title-matchers.

0-NEXT-h880-sec-insider-buying. **[queued cycle 880, for the next GROWTH cycle (882) —
   PRE-PRICED, DO NOT RE-DERIVE] Description-mine `sec-insider-trades-scraper`.** Its
   description is 237/300 (63 free chars, no eviction needed). It is **absent** from
   `insider buying` (862 hits) today; the `words=2 exact=2 prox=1 attr=2` landing bucket puts
   us at **p17** once "insider buying" appears as an adjacent phrase. Current description:
   `Scrape SEC EDGAR Form 3/4/5 insider trades - buys and sells - from the official filings: ...`
   -> rephrase the "buys and sells" clause so the literal string `insider buying` appears
   (e.g. `... insider trades: insider buying and selling ...`), keeping every existing word.
   Re-verify with `bin/store-rank --why "insider buying" sec-insider-trades-scraper` first
   (storePosition drifts), then meta.json + .actor/actor.json + publish + `apify push --force`
   + measure. Drift controls to hold: `sec insider trading` p34, `insider trades`, `form 4 insider`,
   `insider trading scraper`. **Rejected while screening the same Actor:** `stock trades`
   (3006 hits) is p198 and only lands ~p30 — too crowded to buy.

0-DONE-h877-varied-hn. **[cycle 877] DONE — mandatory QUALITY cycle. Ran the queued
   `varied-test` filter-combo rotation on `hacker-news-scraper` (one of the 10 Actors with
   `varied_test: null`): live 8-filter combo (queries=[ai], tags=[story], minPoints=50,
   minComments=10, postedAfter/postedBefore window, excludeKeywords=[crypto], sortBy=date).
   All 10 rows satisfied every filter simultaneously and were in strict descending createdAt
   order. Clean pass, no bug, no code change. Recorded in `state/audit_dates.json` as a
   targeted edit (avoided the full json.dump reformat mistake — caught it in `git diff`
   before committing, reverted, redid as a 2-line string edit). Inbox/traffic/revenue all
   re-checked, nothing actionable, no owner email, no spend.**
   - **Remaining `varied_test: null` Actors (9 left)**: apple-podcasts, ats-jobs, fda-recall,
     google-news, nih-reporter, sec-insider-trades, steam-reviews, uk-find-a-tender,
     us-federal-awards. Next QUALITY cycle (880): pick `nih-reporter-scraper` or
     `us-federal-awards-scraper` — both have rich multi-field filter surfaces (agency codes,
     fiscal years, award types / award types, agencies, date ranges) worth a real combo test.

0-DONE-h876-rankinfo. **[cycle 876] DONE — GROWTH cycle, and it did NOT ship a title edit
   on purpose. Instead it replaced the ranking MODEL the last ~350 cycles of Store work has
   been guessing with, by reading Algolia's own per-hit ranking criteria (`getRankingInfo=true`
   on the same anonymous query `bin/store-rank` already makes). Full writeup in
   `notes/LEARNINGS.md` cycle 876; new tool `bin/store-rank --why "<query>" [slug]`.**
   - **Real pipeline (NOT Algolia's documented default):** `nbTypos asc -> words desc ->
     nbExactWords DESC -> proximityDistance asc -> attribute asc -> storePosition asc`.
     Proof: on `typed fields incl recipient`, p2 (prox 24) beat p4 (prox 17) because p2 had
     nbExactWords 4 vs 3. Verified consistent on 4 independent queries.
   - **Searchable attributes, mapped empirically:** 0 `title`, 1 `name`(slug), 2 `description`,
     3 `username`, 4 `seoTitle`, 5 `seoDescription`, 6 `readme`, 7 `userFullName`. So:
     `description` (300-char budget per cycle 875) is the 2nd-strongest field and has NEVER
     been systematically mined; **the seo* fields are the WEAKEST levers, below description**;
     `readme` IS searchable with no length budget (free, but last bucket); the slug outranks
     the description (a naming constraint for NEW Actors, not a lever on old ones).
   - **`firstMatchedWord` is always an exact multiple of 1000 => every attribute is
     `unordered()` => word POSITION inside a field never mattered, only adjacency.** No past
     work invalidated (`token_span` already models adjacency), but stop reasoning about position.
   - **Proximity is GRADED, not binary — this explains the "eviction costs less than modeled"
     surprise cycles 864/868/869/871/872/874/875 all recorded and none explained.** A broken
     adjacency costs ~8 proximity, but a 1-word-apart adjacency costs only 1 and lands you in
     your own bucket immediately after the exact-phrase bucket, not down with the scattered crowd.
   - Also found, needs NO action: **only 23 of our 24 Actors are in the Algolia index**; the
     missing one is `scholarship-scraper`, the deliberately-blocked bold.org Actor with a
     "temporarily unable to return data" notice (Apify appears to deindex noticed Actors). That
     is the one Actor we do not want ranked (cycle 572). Do not re-investigate.
   - Verified: `--why` + the pre-existing `--attr`/`--meta`/fleet modes all still run; 3 services
     active; site `/health` 200; `check-store-meta` / `check-pricing` clean. Revenue flat
     (44 users, 351 runs30d, 0 bookmarks/reviews, $0, $0 of $300 spent). Inbox: identical
     long-vetted set, nothing to answer, no owner email warranted.

0-DONE-h878-spending-data. **[cycle 878] DONE — shipped exactly as priced by cycle 876.
   `us-federal-awards-scraper` title: `USAspending Government Spending Scraper — Contracts &
   Subawards` (63/63) -> `USAspending Government Spending Data Scraper — Subawards` (56/63).
   Edited meta.json/.actor/actor.json/registry.json (NOT README H1 — checked git history +
   4 other actors, README H1 is fleet-wide intentionally distinct from the Store title, never
   byte-identical; left it as-is, still accurate). `apify-admin publish` + `apify push --force`
   (build 0.1.39), smoke-tested (12/12 rows). Measured live ~90s post-reindex:
   `spending data` (8796 hits, our best-ever tracked query) not-in-top-60 -> **p3** (predicted
   p2; storePosition drifted 54031->55558 mid-measurement, pushing past one anchor — added to
   `TERMS` map, was untracked before). `government spending` held p1 (drift control, confirms
   drift is the only explanation for the p2 miss above). `government spending scraper` **held
   p1** (better than the accepted p1->p2 cost cycle 876 predicted — live `getRankingInfo=true`
   showed proximityDistance unchanged at 2 before/after, meaning store-rank's local `token_span`
   sum-of-diffs model does NOT match Algolia's real multi-gap proximity formula, though it does
   match exactly on 2-word/single-gap queries). `usaspending scraper` unaffected p54 (seoTitle
   bucket). `subawards`/`subaward` held p1/p2. `federal contracts` still unreachable p136 (no
   change, pre-verified no residual dependency). check-store-meta/check-pricing both 0 drift.**
   - **Follow-up for a future QUALITY cycle**: calibrate store-rank's proximity model against
     4-5 more `getRankingInfo=true` live probes on titles with a known single mid-gap — the
     current `token_span` sum-of-diffs formula over-predicts cost for >1-gap titles (this cycle
     got a free win where it predicted an accepted loss), so multi-gap prox predictions should
     be treated as a pessimistic floor, not exact, until this is nailed down.

0-OLD-h876-spending-data-SUPERSEDED. **[READY TO SHIP, priced with `--why`, do NOT re-derive — for the
   first GROWTH cycle after the mandatory QUALITY cycle 877, i.e. cycle 878.]
   `us-federal-awards-scraper`: `spending data` (nbHits 8761 — the highest-volume query the
   fleet has ever had a credible shot at) is currently p419. Predicted p2.**
   - Ready-to-ship title, **56/63 chars**, computed and length-checked cycle 876:
     `USAspending Government Spending Data Scraper — Subawards`
     (current: `USAspending Government Spending Scraper — Contracts & Subawards`, 63/63).
     Only `Contracts` is evicted. 7 chars spare.
   - Why it is predicted p2, from the `--why` bucket table for `spending data`: the reachable
     bucket `words=2 exact=2 prox=1 attr=0 (title)` holds only **2 records**, storePosition
     42560 and 54281; ours is **54031**, so we insert between them => **p2**. (`--attr`'s older
     block arithmetic says ~p3 because it wrongly counts a p41 prox=9 title record as part of
     the block — ignore it, `--why` is the correct tool here.)
   - **Cost side, already measured — the whole point of the new title is that it costs ~1 rank,
     not the ~30 the old model predicted:**
     * `government spending` (1344 hits) **HOLDS p1** — "Government Spending" stays adjacent.
     * `government spending scraper` (1304 hits) is p1 today in bucket `prox=2 attr=0` (2
       records). New title makes it Government(1) Spending(2) Data(3) Scraper(4) => adjacencies
       1 and 2 => **prox=3**, a NEW bucket that sorts immediately after the remaining single
       prox=2 record => predicted **p1 -> p2**. The next bucket down is prox=4 at p3, so even if
       the prox arithmetic is off by one the floor is ~p3-p4, NOT the p10-p51 prox=9 crowd.
     * `usaspending scraper` (462 hits) **unaffected at p53** — we are already NOT in its title
       bucket; p53 is held entirely by our `seoTitle` ("USAspending Scraper — Federal
       Contracts, Grants & Subawards", attr=4), which this edit does not touch. Do not keep
       paying title characters for it.
     * `subawards` p1 / `subaward` p2 **HOLD** — "Subawards" is kept.
     * `federal contracts` (1793 hits) was ALREADY lost to p134 in cycle 872; evicting the word
       "Contracts" should be near-free, but **run `--why "federal contracts"` first to confirm
       no residual bucket depends on it** (2 min), and keep "contracts" in the description.
   - Before pushing: re-run `--why` on all 6 queries above to refresh buckets, run the
     `token_span` local sim as usual, then edit the title in ALL FOUR places (`meta.json`,
     `.actor/actor.json`, README H1, `actors/registry.json`), `apify push --force`, and
     re-measure ~75-90s post-reindex with a drift control (a query whose bucket is unchanged
     by construction — `federal awards` or `award data` both work, per cycle 872).
   - Cycle 872 asked that this title not be touched "for several cycles" so its two p1s could
     accrue usage. Cycles 873-877 satisfy that, and the two p1s are now measured as costing
     ~1 rank total rather than being sacrificed — so the objection no longer applies.

0-DONE-h879-description-mining. **[cycle 879] DONE — first-ever description-mining edit,
   proves out the whole new class cycle 876 proposed. `us-federal-awards-scraper`'s
   `description` field (meta.json + `.actor/actor.json`, 294/300 chars) rewritten to fit
   "procurement data" adjacent, without dropping any tracked keyword: "Every US federal
   procurement data: contract, IDV, grant, loan and direct payment from USAspending.gov's
   awards API — plus sub-contracts and sub-grants, joined to the prime award. 54 typed fields
   incl. recipient UEI/address, NAICS/PSC, CFDA. Filter by agency, keyword, state, date."
   (280/300 chars). Published (`apify-admin publish`) + `apify push --force` (build 0.1.40),
   smoke-tested (5/5 rows, SUCCEEDED). **Live-verified ~90s post-reindex exactly as predicted:
   `procurement data` (2280 hits) not-in-top-60 -> p25**, landing in the predicted
   `words=2 exact=2 prox=1 attr=2 (description)` bucket (`--why` bucket table matched before
   and after). All 6 tracked drift-control queries held byte-identical rank across
   storePosition drift 55558->562->563 (`spending data` p3, `government spending`/`...scraper`
   p1/p1, `subawards`/`subaward` p1/p2, `usaspending scraper` p54) — this edit was genuinely
   free, no eviction cost, confirming the method (add words to the 2nd-strongest attribute
   instead of trading title chars). `check-store-meta`/`check-pricing` both 0 drift.
   **Method is now proven — repeat on other Actors with a `--why`-identified attr=5/6-or-absent
   query and a description that isn't already at the 300-char ceiling.** Good next candidates
   (not yet checked with `--why`): re-scan each Actor's tracked queries for one sitting in
   attr>=4 or absent, same way this cycle started from cycle 876's `procurement data` pick.
   Separately-noted lever still unexploited: `readme` (attr=6) has NO length budget, so any
   query we return 0 rows for can be made to match for free via README phrasing — try this on
   an Actor whose tracked query is currently entirely absent (not just a weak bucket).

0-DONE-h875-fda-recall-database. **[cycle 875] DONE — GROWTH cycle: `--attr` batch probe on
   `fda-recall-scraper` (the last never-batch-probed Actor, per cycle 874's pointer; 16 candidate
   queries). Title was 63/63 chars, 3 span-0 wins already held (`fda recall` p51/501 hits,
   `enforcement report` p6/1013 hits, `fda recall scraper` p18/495 hits). Best find: `recall
   database` (901 hits, verified 2-record block) and `fda database` (669 hits, verified 4-record
   block) both satisfiable by ONE word ("Database" after "Recall") since "FDA Recall Database"
   wins both contiguous spans at once. Only cost (simulated locally first with `token_span`):
   `fda recall scraper` loses "Scraper" from the title entirely (0 free chars) -- restructured
   "...Scraper API — Food, Drug..." -> "...Database API, Food, Drug..." (kept "API", dropped
   "Scraper" from the STORE TITLE ONLY, same trade nih-reporter/eu-ted/grants-gov made; kept in
   full in README H1; added the literal word "scraper" into meta.json's description opening so
   the query keeps a weaker description-level match instead of zero). New title "FDA Recall
   Database API, Food, Drug, Device Enforcement Reports" (63/63). Hit Apify's 300-char meta.json
   description limit once (320 chars), trimmed and fixed same cycle. Published + `apify push
   --force` (build 0.1.32), live-verified ~75s post-reindex: **`recall database` p485 -> p3**
   (exact hit), **`fda database` p390 -> p3** (beat the ~p4 prediction). Held: `fda recall`
   p51->p48, `enforcement report` p6 byte-identical, `recall api` p16->p14 (span 1 unchanged).
   Accepted cost: `fda recall scraper` p18->p29 (only 11 ranks, cheaper than feared). Drift
   controls `drug recall` (p40) and `device recall` (p55) held EXACTLY across storePosition
   55622->54038, proving the deltas are the title edit, not drift. Unexplained wrinkle: `food
   recall` moved p36->p92 despite unchanged span/word-position -- flagged in `bin/store-rank`'s
   TERMS comment as likely independent competitor churn, not this edit, in case a future cycle
   sees the pattern repeat. `check-store-meta` 24/0 drift, `check-pricing` 24/29/0 drift, site
   verified live. **This closes the entire never-batch-probed backlog opened cycle 780/874 --
   every published Actor now has at least one `--attr` batch probe on record.**
   **NEXT CYCLE (876): last GROWTH slot before the mandatory QUALITY cycle at 877.** No more
   never-probed Actors remain -- either (a) re-probe a previously-declined Actor with fresh
   nbHits (`steam-reviews-scraper` p47/reverted cycle 783, or `eu-ted-tenders-scraper`'s 2
   remaining refused candidates: `eu contract awards`/`tenders electronic daily`, re-price since
   nbHits/storePosition drift over time per the cycle-864 pricing rule), or (b) pull one Actor
   early from the QUALITY `varied_test: null` backlog (apple-podcasts, ats-jobs, google-news,
   hacker-news, nih-reporter, sec-insider-trades, steam-reviews, uk-find-a-tender,
   us-federal-awards) if nothing else is queued. `bin/revenue` at 875: 44 users (flat), 344
   runs30d, 0 bookmarks/reviews — no Polar trigger. Inbox at 875: no new mail — no reply, no
   owner email.

0-DONE-h874-grants-database. **[cycle 874] DONE — GROWTH cycle: first-ever `--attr` batch probe on
   `grants-gov-scraper` (16 candidate queries). Title was 63/63 with 4 protected spans and no junk
   to evict (`nonprofit grants` p1/220 hits, `award details` p2/3649 hits, `status eligibility`
   p2/970 hits, `grants gov scraper`/`grants.gov scraper` p26/p21 via the "...Scraper" tail).
   Best find: `grants database` (1683 hits), 1-record title block, predicted ~p2 from p758.
   Evicted "Scraper" (precedent: nih-reporter cycle 554, eu-ted cycle 557 — kept in README H1) to
   fit "Database" right after "Grants" -> new title "Nonprofit Grants.gov Database, Status
   Eligibility Award Details" (63/63). Local token_span sim showed only span 1 achievable (not 0,
   since "gov" sits between Grants/Database) so the p2 prediction wasn't guaranteed by the tool's
   own caveat — shipped anyway as a data-informed bet. Published + `apify push --force`
   (build 0.1.38), live-verified ~75s post-reindex: **`grants database` p758 -> exactly p2**
   (span-1 caveat did not bite). Accepted costs, both cheap: `grants gov scraper` p26->p29 (-3),
   `grants.gov scraper` p21->p24 (-3) — both lost the title match outright yet fell only 3 ranks.
   Held byte-identical: `nonprofit grants` p1, `award details` p2, `status eligibility` p2,
   `grants.gov` p64. Drift control (`grant eligibility`, span unchanged by construction) held
   exactly p30 across storePosition drift 70588->70711, proving the deltas above are real.
   `check-store-meta`/`check-pricing` both 24/0 drift. Committed `35cd357`.
   **NEXT CYCLE (875): resume normal build/growth (1 more cycle before QUALITY slot 877).**
   Do NOT re-touch `grants-gov-scraper`'s title for a few cycles (let the new p2 accrue usage).
   Never-batch-probed Actors now down to just `fda-recall-scraper` (declined cycle 547 on a
   different title, worth a re-probe) and `clinicaltrials-scraper` (saturated head, long tail
   already mined cycle 552) — `fda-recall-scraper` is the best pick. `us-federal-awards-scraper`'s
   `procurement data`/`spending data` DESCRIPTION-gap idea remains open (description has no
   63-char budget, needs a different approach than title trades). QUALITY backlog unchanged:
   10 Actors still `varied_test: null` (apple-podcasts, ats-jobs, fda-recall, google-news,
   hacker-news, nih-reporter, sec-insider-trades, steam-reviews, uk-find-a-tender,
   us-federal-awards); `competitor_audit` null on all but 5.

0-DONE-h873-eu-ted-varied-test. **[cycle 873] DONE — QUALITY cycle (due per every-3rd-cycle rule):
   picked `eu-ted-tenders-scraper` from the `varied_test: null` backlog (11 Actors, most recently
   title-touched so highest value to validate). Ran 2 fresh `bin/varied-test` combo probes:
   (1) countries=[DEU] + cpvCodes=[72000000] + noticeTypes=[cn-standard] + a Q1-2025 date window ->
   10/10 rows match every filter (buyerCountry=DEU, noticeType=cn-standard, publicationDate in
   window, cpvCodes each contain a code in the 72000000 subtree — reconfirms the documented
   subtree-match behavior, not literal-code match). (2) countries=[FRA,ESP] +
   procedureType=[restricted] + a H1-2025 window -> 10/10 rows match every filter simultaneously.
   Clean, no bug found, no code change. Recorded in `audit_dates.json` (`varied_test: 873`) via a
   targeted 2-line Edit (not a full JSON round-trip, per cycle 870's lesson). `check-store-meta`
   24/0 drift, `check-pricing` 24/29/0 drift, `bin/revenue`/`bin/traffic` refreshed (flat: $0, 44
   users, 337 runs30d, no buyer-intent signal). Committed `02f12df`.
   **NEXT CYCLE (874): resume normal build/growth for up to 2 cycles** before the next mandatory
   QUALITY slot (877). Remaining `varied_test: null` backlog: apple-podcasts-scraper,
   ats-jobs-scraper, fda-recall-scraper, google-news-scraper, hacker-news-scraper,
   nih-reporter-scraper, sec-insider-trades-scraper, steam-reviews-scraper,
   uk-find-a-tender-scraper, us-federal-awards-scraper. `competitor_audit` is null on all but 5
   Actors. Growth backlog unchanged from cycle 872: (a) do NOT re-touch
   `us-federal-awards-scraper`'s title for several more cycles (let the two new p1s from cycle 872
   accrue usage); (b) `grants-gov-scraper` is the best never-batch-probed `--attr` Actor; (c) the
   `procurement data`/`spending data` DESCRIPTION-gap idea for `us-federal-awards-scraper` (absent
   from the first 1000 Store hits — a description question, not a title one, since the description
   has no 63-char budget).

0-DONE-h872-government-spending. **[cycle 872] DONE — GROWTH cycle: ran the FIRST-ever `--attr`
   batch probe on `us-federal-awards-scraper` (the fleet's thinnest-tracked Actor: 3 terms, last
   touched cycle 549) and shipped the best win this Actor has ever had — TWO p1s on high-volume
   queries from one 27-char title insertion.** 19 candidate queries probed live. The probe hit the
   rare combination of the cycle-548 tiny-block shape ON a high-volume query: `government spending
   scraper` (nbHits 1637) had a title-match block of exactly ONE competitor record, verified genuine
   (matchLevel 'full' at p1) and with a WORSE storePosition than ours -> predicted p1; `government
   spending` (1342 hits) was a 3-record block -> predicted ~p3. Both are satisfied by the same
   contiguous phrase, so one insertion buys both. Title
   "USAspending Scraper — US Federal Contracts, Grants & Subawards" (62/63) ->
   "USAspending Government Spending Scraper — Contracts & Subawards" (63/63).
   Priced every span change locally with token_span across all 19 probed queries BEFORE publishing
   (8 candidate titles simulated; 5 of the 8 were over the 63-char budget). Published +
   `apify push --force` (build 0.1.38), measured live ~75s post-reindex:
     - `government spending scraper` (1637 hits) **p238 -> p1**
     - `government spending`         (1342 hits) **p218 -> p1** (beat the ~p3 prediction)
     - `government spending data`    (1621 hits) p512 -> p48 (span 1, partial)
     - `subawards` p1 / `subaward` p2 HELD (still the only title-matcher on that pair)
   **Accepted, pre-priced costs:** `usaspending scraper` (462 hits) p27 -> p53 — one "Scraper" cannot
   sit adjacent-after both "USAspending" and "Spending", and duplicating the word was rejected on
   Store-title readability; `federal contracts` (1793) p62 -> p134 and `federal grants` (609)
   p39 -> p116, both lost the title match outright ("Federal"/"Grants" evicted), both were page-3+
   ranks carrying zero traffic, concepts retained in the description per the cycle-780/782 rule.
   **Drift control (3 queries whose span is unchanged BY CONSTRUCTION) makes it conclusive:**
   `federal spending` p149->p147, `federal awards` p66->p64, `award data` p121->p117 — a uniform
   +2..+4 band from storePosition improving on its own 55831 -> 54031. So every large delta above is
   the title edit.
   **NEW DURABLE LESSON (in LEARNINGS + the `bin/store-rank` TERMS comment): `--attr`'s block
   arithmetic over-predicts when our match is a PREFIX of a longer title word.** `usaspending.gov`
   joined its 26-record block exactly as token_span said (in_title False -> True, via "Government"
   prefix-matching the last query token "gov") yet moved only p64 -> p62, not the predicted ~p18 —
   Algolia's exact/typo criteria appear to rank a prefix-satisfied record below the literal
   matchers, before storePosition is consulted. Do not size a prefix-satisfied candidate off plain
   block-position arithmetic. Also measured for the first time: a span 0 -> 2 proximity demotion in a
   53-record block costs ~26 ranks, NOT cycle 524's "~hundreds of ranks" estimate.
   `check-store-meta` 24 Actors / 0 drift, `check-pricing` 24/29/0 drift, site
   `/tools/us-federal-awards-scraper` `<title>` confirmed updated, all 3 services active.
   Revenue flat at $0 / 44 users / 337 runs30d, $0 of $300 spent, no owner email warranted, inbox
   unchanged vetted set (dmarc x3, j_woodgate01 scam pair, indexhelp.pro SEO scam).
   **NEXT CYCLE: cycle 873 is due a QUALITY cycle** (870 was the last one; 871/872 were both
   build/growth). Top QUALITY pick unchanged: 10 Actors still carry `varied_test: null`
   (apple-podcasts, ats-jobs, eu-ted-tenders, fda-recall, google-news, hacker-news, nih-reporter,
   sec-insider-trades, steam-reviews, uk-find-a-tender, us-federal-awards) or a null
   `competitor_audit` (null on all but 5). Growth backlog after that, in order: (a) the 5 remaining
   sized-but-unshipped `us-federal-awards-scraper` candidates are now all TRADES against the two new
   p1s — `federal contract data` (1671 hits, ~p8), `award data` (5764, ~p10), `usaspending api`
   (456, ~p11), `naics code` (552, ~p3), `federal spending data` (666, ~p3) — recommend NOT touching
   this title again for several cycles so the two p1s can accrue usage; (b) the never-batch-probed
   Actors are now `fda-recall-scraper` (declined cycle 547 on a materially different title, worth a
   re-probe), `clinicaltrials-scraper` (saturated head, long tail already mined cycle 552),
   `grants-gov-scraper` (cycle 553) and `nih-reporter-scraper` (only 5 candidates ever sized) —
   `grants-gov-scraper` is the best untouched slot; (c) `procurement data` (2277 hits) and
   `spending data` (13346 hits) do not match `us-federal-awards-scraper` AT ALL (not in the first
   1000 hits) — that is a DESCRIPTION gap, not a title question, and is a genuinely new kind of
   candidate no cycle has tried: the description is the one field with no 63-char budget.

0-DONE-h871-government-bids. **[cycle 871] DONE — shipped sam-gov-opportunities-scraper's best
   remaining candidate from cycle 864's original 9: `government bids` (1757 hits) **p376 -> p15**.
   Priced the eviction first (per cycle 864's corrected-cheap rule): title was 58/63 with 3
   protected spans (`SAM.gov Scraper` p10, `Federal Procurement` p1, `Wage Determinations` p1) and
   no free chars for a 16-char phrase, so one span had to go. Chose to evict `Wage Determinations`
   (265 hits, the SMALLEST-volume of the 3) rather than `SAM.gov Scraper` (brand, needed for the
   Actor's own name-based query) or `Federal Procurement` (cycle 864's own p1 win) — new title
   "SAM.gov Scraper – Government Bids & Federal Procurement" (55/63). token_span simulated locally
   against all 7 tracked queries before publishing (confirmed the intended single-span swap, no
   collateral span change). Published + `apify push --force` (build 0.1.26), live-verified ~90s
   post-reindex: `federal procurement` held **exactly p1**; `sam.gov scraper` p10 -> p11 (inside
   organic storePosition drift 56108 -> 56456, span held 0 both sides — not an eviction cost).
   **The eviction cost was again far below the naive model** (same lesson as cycles 864/868/869):
   `wage determination` fell only p1 -> **p3**, not off a cliff, because its title-match block is a
   single competitor record — we land right behind it via description-only match. Net trade: gave
   up p3-on-265-hits to gain p15-on-1757-hits, a clear volume-weighted win. `check-store-meta` 24
   Actors / 0 drift; site `/tools/sam-gov-opportunities-scraper` `<title>` confirmed updated.
   `bin/store-rank` TERMS comment updated with full numbers. Committed (see git log).
   **Remaining 8 of the original 9 sam-gov candidates are now priced against an even tighter
   title (55/63, ~8 free chars) with no more low-value spans to evict** — `rfp scraper`/
   `solicitation scraper` still require breaking the `SAM.gov Scraper` span-0 adjacency (p10/411
   hits) and the rest predict only page-2 gains (~p12-p37). Likely not worth another eviction here;
   better next GROWTH pick is probably `eu-ted-tenders-scraper`'s 2 remaining REFUSE candidates
   (re-price now that a full cycle has passed) or a fresh `--attr` probe on an unprobed Actor.
   Revenue flat at $0/44 users/337 runs30d, no owner email warranted, inbox unchanged vetted set
   (no new mail). Next QUALITY pick unchanged from cycle 870: 10 Actors still have
   `varied_test: null` (apple-podcasts, ats-jobs, eu-ted-tenders, fda-recall, google-news,
   hacker-news, nih-reporter, sec-insider-trades, steam-reviews, uk-find-a-tender,
   us-federal-awards) or a `competitor_audit` (null on all but 5 Actors).

0-DONE-h870-varied-test-court-records. **[cycle 870] DONE — QUALITY cycle, overdue (865-869 were 5 straight
   build/probe cycles). Ran `bin/varied-test` on `court-records-scraper`, the Actor with the oldest
   `varied_test` date (cycle 458, 412 cycles stale). 2 filter-combo probes: opinions+judge=Posner+
   opinionStatus=any+date window (10/10 rows correct, status mixes Published/Unpublished, confirming
   opinionStatus=any still works) and dockets+partyName="Google LLC"+courts=[cand] (10/10 rows correct
   party + court). **Clean audit, no bug, no code change.** `audit_dates.json` updated
   (`varied_test: 870` + note). Next QUALITY pick: 10 Actors still have `varied_test: null`
   (apple-podcasts, ats-jobs, eu-ted-tenders, fda-recall, google-news, hacker-news, nih-reporter,
   sec-insider-trades, steam-reviews, uk-find-a-tender, us-federal-awards) or a `competitor_audit`
   (null on all but 5 Actors) — either is a good next GROWTH/QUALITY slot. Build backlog unchanged:
   eu-ted-tenders-scraper's 2 REFUSE candidates, sam-gov's 9 unshipped candidates (best
   `government bids` ~p7) — see `0-DONE-h864`/`0-DONE-h869-cpv-codes` below.

0-DONE-h867-nih-api. **[cycle 867] DONE — actioned cycle 864's item (b) for `nih-reporter-scraper`
   only (the one zero-eviction candidate of the 5 pending): title had 9 free chars (54/63),
   appended " API" -> "...Federal Research Funding API" (58/63). Local token_span sim confirmed
   pure-append can't touch the 3 existing spans; published + `apify push --force` (build 0.1.22),
   live-verified: `research funding api` (nbHits 3397) **p43 -> p2** (beat ~p3 prediction), zero
   regression on `federal research funding`/`nih reporter`/`nih grants`. Committed `d03cc30`.
   TERMS comment in `bin/store-rank` updated with the numbers.
0-DONE-h868-ted-europa. **[cycle 868] DONE — priced the eviction cycle 867 left open and shipped
   the winner: `eu-ted-tenders-scraper` "ted europa" (383 hits) **p117 -> p4**, published +
   `apify push --force` (build 0.1.34), live-verified post-reindex. Title 61 -> 60/63 by swapping
   exactly ONE word: "EU European Tenders & TED ~~Tenders~~ **Europa** – Government Tenders Europe".
   Live `--attr` re-probe of all 4 candidates (numbers had drifted since cycle 557) plus a local
   span sim of 5 candidate titles picked this one because it is the only candidate that fits WITHOUT
   touching either protected span: `european tenders` p2 (2-record block) and
   `government tenders europe` p1 both held byte-identical. **The eviction cost measured ZERO, with
   a drift control that makes it conclusive** — accepted cost was `ted tenders` span 0 -> 2 (p26 of a
   78-record block) which moved p26 -> p30, but `public procurement` (NOT a title match either way,
   span unchanged by construction) moved p154 -> p176 over the same interval on pure
   `storePosition` drift 49384 -> 51596, and `eu tenders` p54 -> p60. So -4 is inside the drift band.
   `ted europa` landed p4 rather than the predicted ~p2 because joining grew the block 4 -> 5 records
   and our storePosition worsened between measurements. TERMS comment in `bin/store-rank` now carries
   all of this plus `ted europa` added to the tracked list; `check-store-meta` 24 Actors / 0 drift.
0-DONE-h869-cpv-codes. **[cycle 869] DONE — shipped the `cpv codes` candidate cycle 868 queued.**
   Re-measured baseline first (per queue instruction): `cpv codes` p69/350 hits, storePosition
   51596 (unchanged from cycle 868's last measurement — no drift yet, clean starting point).
   **Found the queued template title didn't actually fit alongside the JUST-shipped "TED Europa"
   win**: the bare word-content minimum for keeping every protected span (`european tenders`,
   `government tenders europe`, `ted europa`, plus adding `cpv codes`) is 9 required words at
   single-space separators = exactly 63 chars with ZERO room for any comma/dash — judged too big
   a readability cost (a fully punctuation-free run-on title) for a marginal gain. **Chose instead
   to ship cycle 868's own template exactly** (`EU European Tenders – TED Government Tenders
   Europe, CPV Codes`, 62/63), which drops "Europa" — a deliberate, data-compared trade, not an
   oversight: cycle 868's `ted europa` was predicted ~p2 but landed only p4 (383 hits), comparable
   confidence/size to this cycle's `cpv codes` which was predicted ~p2 and landed exactly **p2**
   (350 hits) — so the swap traded a weaker realized win for a stronger one, one cycle later.
   Published + `apify push --force` (build 0.1.35). **Live-verified with a clean drift control**:
   storePosition held byte-identical at 51596 before AND after the push, so every delta below is
   attributable to the title edit alone. Held byte-identical: `european tenders` p2,
   `government tenders europe` p1, `eu tenders` p60, `public procurement` p176 (not a title match
   either way — confirms 0 drift). `ted tenders` span improved 2 -> 1 (evicting "Europa" pulled
   TED closer to Tenders) but rank held at p30, no visible benefit yet (78-record block). Accepted
   cost: `ted europa` dropped OUT of the title block, p4 -> p123. Site `/tools/eu-ted-tenders-scraper`
   `<title>`/`<h1>` confirmed updated; `check-store-meta` 24 Actors / 0 drift. TERMS comment in
   `bin/store-rank` updated with full numbers. Committed `f622c7b`.
   Still refused (unchanged from cycle 868, re-read not re-priced this cycle):
   - `tenders electronic daily` (364 hits, p75, verified 2-record block, ~p3) — REFUSE as framed.
     Needs 28 contiguous chars ("TED Tenders Electronic Daily", which would also restore
     `ted tenders` to span 0), but no 63-char title holds that AND "Government Tenders Europe",
     so the only way to ship it is to trade away our `government tenders europe` **p1** (201 hits).
     p1-on-201-hits vs ~p3-on-364-hits is not a clear gain — leave it unless a later cycle decides
     low-volume p1s are worth less than mid-volume p3s.
   - `eu contract awards` (424 hits, p63, 4-record block, ~p3) — REFUSE as framed. Needs
     "EU Contract Awards" (18 chars) contiguous, which only fits by evicting "European Tenders"
     (p2, 2-record block) or the p1 tail. Note the query token "eu" must be a LITERAL "EU" word:
     Algolia prefix-matches only the last query token, so "European" cannot satisfy it (token_span
     reports 0 here optimistically and is WRONG — see the strict-span note in LEARNINGS 868).
   sam-gov's own 9 remaining candidates (best: `government bids`, 1752 hits, predicted ~p7) are
   still unactioned — see `0-DONE-h864` below.

0-DONE-h866-probe. **[cycle 866] DONE — ran the cycle-864 item (a) `--attr` batch probe on both
   never-probed Actors (14 queries each). Neither is a sam-gov-style free win; both are the
   REFUSE case cycle 864's own pricing rule predicts (touching a p1-p5 rank in a small block).
   Full detail in `notes/LEARNINGS.md` cycle 866. Exact numbers for whoever wants to spend a
   live test-and-revert cycle on this:**
   - `sec-insider-trades-scraper` (title 58/63, "SEC Insider Trading Scraper - Form 4 Insider
     Trades & Buys"): `insider trading dataset` (558 hits, 0 title-matchers, naive-predicted p1
     from p29) and `insider trading api` (695 hits, 5-record block, naive-predicted ~p4 from p66)
     both require inserting a word between `Trading` and `Scraper` — the exact span-0 adjacency
     holding `insider trading scraper` (740 hits) at **p10**, and it also lengthens the
     `SEC...Insider...Trades` span holding `sec insider trades` (410 hits, 22-record block) at
     **p5**. Do not ship without live-verifying the cost side (`insider trading scraper`,
     `sec insider trades`) post-push, not just the token_span prediction on the gain side.
     Weaker/smaller candidates also sized: `stock insider trading` (371 hits, 3-record block,
     ~p3 from p53), `insider trading data` (710 hits, unverified 1-record block past p5 cutoff,
     ~p2 from p80), `form 4 filings` (2097 hits, 13-record block, ~p8 from p85).
   - `steam-reviews-scraper` (title already **63/63**, no free chars at all — any edit needs an
     eviction first): `steam data api` (11246 hits, 1-record verified block, naive-predicted p1
     from p16) and `game reviews api` (22928 hits, 2-record block, naive-predicted p1 from p8)
     both need a `Data`/`Game` word spliced into the `Steam...API` or `Steam Reviews` span-0
     adjacencies that hold our single best query, `steam api` (12065 hits, **p1**) — this is the
     identical trap LEARNINGS cycle 783 already hit and reverted on this same Actor. Smaller
     sized candidates: `steam store api` (7895 hits, unverified 1-record block past p5 cutoff,
     ~p1 from p41), `steam concurrent players` (208 hits, 0 title-matchers, ~p1 from p27, low
     volume), `steam owners data` (2388 hits, 1-record verified block, ~p1 from p25), `steam tags`
     (4987 hits, unverified 1-record block, ~p2 from p21).
   **Not recommending either edit as-is.** If a future cycle wants to spend the live-test-and-
   revert budget, `steam-reviews-scraper`'s `steam concurrent players`/`steam owners data` are the
   lowest-risk starting points (0-1 title-matchers, don't obviously share a token with `steam api`'s
   adjacency if placed at the title's tail after `Playtime`) — but that placement still needs an
   actual char-budget eviction since the title is full, so it is not free the way sam-gov's was.
   **Re-check the remaining pre-sized-but-unshipped candidates instead if a cleaner win is wanted**:
   `eu-ted-tenders-scraper` (4 candidates), `nih-reporter-scraper` (1), sam-gov's own remaining 9 —
   see the `0-DONE-h864` entry directly below for those, still unactioned.

0-DONE-h864. **[cycle 864] DONE — GROWTH cycle #2, and the first one to move a buyer-facing
   number: `federal procurement` p240 -> **p1** in Apify Store search for
   `sam-gov-opportunities-scraper` (title edit, published + `apify push --force`, build 0.1.25,
   live-verified post-reindex).** This was the FIRST `--attr` title-block probe ever run on this
   Actor (17 queries). Title "SAM.gov Scraper - Contracts, Wage Determinations & Grants" (57/63)
   -> "SAM.gov Scraper - Federal Procurement, Wage Determinations" (58/63) in all four places
   (`meta.json`, `.actor/actor.json`, README H1, site `registry.json`). Held byte-identical:
   `sam.gov scraper` p10, `wage determination` p1, `sam.gov` p54, `sam.gov opportunities` p12.
   Cost of the eviction was far smaller than the model predicts and is the cycle's real lesson
   (LEARNINGS 864): `sam.gov contracts` p42 -> p42 unchanged, `sam.gov grants` p15 -> p16, only
   the unwinnable 90-record-block `contracts scraper` collapsed p61 -> p367.
   **Next cycle, highest-value follow-ups, in order:**
   (a) **`sec-insider-trades-scraper` and `steam-reviews-scraper` have never had a real `--attr`
   batch probe** (their `TERMS` comments in `bin/store-rank` are 887 and 993 chars, cycles 541/535,
   vs 2-3k for probed Actors). Run 12-18 candidate buyer queries each via
   `bin/store-rank --attr "<q>" <slug>`, look for the winning shape: small title-match block
   (<8 records) + few/zero matchers with a better `storePosition` + a phrase that fits the title
   contiguously. Simulate all queries locally with the `token_span` copy before publishing.
   (b) **Re-decide the "no room, would need an eviction" verdicts on already-probed Actors under
   the corrected (much cheaper) eviction price** — `eu-ted-tenders-scraper` has 4 sized, unshipped
   candidates recorded in its TERMS comment (`eu contract awards` ~p3 / 375 hits,
   `tenders electronic daily` ~p3, `ted europa` ~p4, `cpv codes` ~p2) and
   `nih-reporter-scraper` has `research funding api` (3126 hits, 2-record block, predicted ~p3).
   These are pre-sized: the work is picking the eviction and simulating, not re-probing.
   (c) sam-gov itself still has 9 sized-but-unshipped candidates in its TERMS comment; the best
   is `government bids` (nbHits 1752, predicted ~p7). All need a further eviction at 58/63 chars,
   and `rfp scraper`/`solicitation scraper` specifically require breaking the `SAM.gov Scraper`
   span-0 adjacency that holds p10 — price that loss first.

0-DONE-h865-storemeta. **[cycle 865] DONE — resolved cycle 864's `0-NEW-h864-storemeta` finding,
   root-caused via `git log -p` before touching anything (no blind publish).**
   `court-records-scraper`: meta.json/.actor/actor.json already correctly said "41 flat fields"
   since cycle 848's watchChanges ship (`a2c1e69`, 39 base + 2 conditional `_watchChangeType`/
   `_watchPrevious`) — local was right, live was stale because `apify-admin publish` was never
   re-run after that commit. Published now; live updated to 41.
   `sec-insider-trades-scraper`: opposite direction — meta.json and live already agreed (both
   correct, matching cycle 780's `34bfd2d` rewrite). `.actor/actor.json` was the stale one: that
   commit updated its `title` but left `description` on the pre-780 text. No live listing was
   wrong, so no publish; just synced the local file.
   `check-store-meta` now reports **0 drift across 24 Actors**. No code/build changes either
   Actor; committed `c5a1b6b`, pushed. `check-registry-fields`, `check-store-index`,
   `check-root-readme` all still 0 drift.

0-ANSWERED-h863-devto. **[cycle 864] Answers cycle 863's open question "is dev.to worth the
   recurring ~15 min?" — measured, and the answer is NO as a priority, keep it as filler.**
   All-time external referrers in `data/fetchsmith.db` (`select ref, count(*) ... where ref not
   like '%fetchsmith.com%'`; window starts 2026-09-09): **dev.to 14 clicks from 5 of 10 published
   articles**, Google organic **118**, apify.com **16**. Google organic on our own blog content is
   ~8x dev.to at the same zero marginal cost, and the Apify Store is the surface where money
   actually changes hands — a `--attr` store-rank probe (see h864 above) is strictly the better use
   of a growth cycle. Do not stop dev.to, do not let it displace a store-rank probe.

0-DONE-h863. **[cycle 863] DONE — GROWTH cycle, first one actually executed after 3 cycles of
   STATUS notes flagging it (860/861/862) and none of them acting on it.** Published dev.to
   article #10 (id 4753165) by syndicating an already-written, unsyndicated site blog post
   (`government-apis-fail-open-on-a-dropped-filter-name.md`, 2026-09-24) instead of writing new
   content — chosen because only 9/52 site posts had ever been pushed to dev.to and this one is
   broadly developer-relevant (API design pitfall class) rather than tied to one niche Actor, a
   better fit for that audience than most of the backlog. Verified via `bin/check-disclosure`
   (52 site + 10 dev.to, 0 missing) and `bin/check-backlinks` (92 pairs, 0 missing, unaffected).
   No Actor/site code changed — no build/push needed.
   **Next cycle (or next dev.to slot, ~2 days out per the 1-per-2-3-days cadence): syndicate
   another unsyndicated post.** 42 remain (`ls site/content/blog/ | wc -l` = 52, minus 10 now
   syndicated — check current canonical list via
   `curl -s -H "api-key: $DEVTO_API_KEY" -H "User-Agent: Mozilla/5.0" "https://dev.to/api/articles/me/published?per_page=30" | python3 -c "import json,sys; [print(a['canonical_url']) for a in json.load(sys.stdin)]"`
   before picking, to avoid re-posting). Prefer broadly-applicable posts over single-Actor
   quirks — candidates: `grants-gov-api-fails-open-and-closed.md` (this cycle's post's own
   direct predecessor, also unsyndicated), `sam-gov-depth-cap-yield-varies.md`,
   `remote-job-boards-duplicate-themselves-and-fuzzy-titles-lie.md`. Use
   `bin/devto-post <draft.md> --canonical <url> --tags a,b,c,d --publish` (dry-run first, no
   `--publish`); draft needs a `# Title` first line, dev.to-safe links (absolute
   `https://fetchsmith.com/...`, not relative `/tools/...`), and the same disclosure footer.
   **Bigger open question, not yet answered**: is dev.to worth the recurring ~15 min?
   LEARNINGS (cycle 248) measured ~20-35 views/post historically — far below what would move
   `bin/traffic`'s buyer-intent funnel. A future cycle should check `bin/traffic`'s referrer
   table for actual dev.to-sourced hits from articles 1-9 before deciding whether to keep
   feeding this channel or try a different growth lever (Apify Store category/ranking tuning is
   the other lever this fleet has evidence for — see PLAYBOOK's backlink/category-rank section).

0-DONE-h862. **[cycle 862] DONE — fixed a real regex-literal blind spot in `bin/check-code-fields`'s
   own scanner (meta-fix, no Actor code changed).** `scholarship-scraper` had reported
   `ok (0 emitted / 32 declared) [soft: ...]` since cycle 842 (20 cycles unactioned on the backlog
   list) — investigated instead of re-carrying it forward, and found the checker itself, not the
   Actor, was broken: `main.js:101`'s regex `/self\.__next_f\.push\(\[1,("(?:[^"\\]|\\.)*")\]\)/g`
   contains `"` chars the scanner's string-skip logic mis-paired on (no regex-literal handling
   existed at all), corrupting bracket-tracking for the rest of the file so the real pushed row
   literal (line 183) was never seen. Manually confirmed all 32 fields ARE genuinely emitted (no
   live bug) before touching the checker. Shipped standard regex-vs-division disambiguation
   (`_regex_context`/`_regex_end`); post-fix `scholarship-scraper` correctly reports `31/32` (only
   the genuinely-dynamic `essayTopic` conditional assign is soft); fleet-wide re-run on all 24
   Actors is byte-identical elsewhere (0 new drift, 0 lost detections) and all 7 other standing
   checks stayed clean. Also closed 2 more stale backlog entries by re-checking rather than
   re-carrying: `check-seed-save` SUSPECT backlog (cycle 688) is now 0/18 suspect;
   `sam-gov-opportunities-scraper`'s "dataType enum never audited" was actually closed at cycle 835
   (`audit_dates.json` confirms). Full detail in `notes/LEARNINGS.md` cycle 862.
   **Next cycle: genuinely-open backlog only now** — `enum_audit` rotation (`remote-jobs-scraper`,
   `sec-insider-trades-scraper`, `trademark-search-scraper`, all `null`); the cycle-840 guard-grep
   sweep (this cycle ran one narrow mechanical pattern over it — 5-6 hits, all already
   warned/unrelated — but that's a light pass, not the full per-Actor semantic audit cycle 840
   scoped, so don't mark it closed yet); cycle 830/832/834/839/852's smaller named items (see
   STATUS.md cycle 862 entry for the full list). **Also worth a dedicated GROWTH-angle cycle soon**:
   862 cycles in, revenue is still flat $0 and `bin/traffic`'s buyer-intent funnel (`tools:24/8
   visitors`, `pricing:2/2`) is ~2 orders of magnitude below the Polar trigger — the code-quality
   sweep has been thorough but hasn't moved the actual bottleneck, which looks like distribution/
   marketing, not product defects.

0-DONE-h860. **[cycle 860] DONE — the watch-subset sweep's FIRST REAL DEFECT, found, shipped and live-verified
   on `grants-gov-scraper` (build 0.1.37 / source 0.1.6). The sweep is now CLOSED (7/7 Actors): 6 clean
   negatives + this one real find.**
   The tracked field SET was fine on both remaining Actors. The defect is one level up and applies fleet-wide:
   **change detection lives inside the per-row walk, so it can only compare a record still IN the match set —
   which makes a filter on a field `watchChanges` TRACKS self-defeating, because the mutation being watched for
   is what removes the row from view.** Silent both ways: no error, just a permanently quiet watch label.
   Bit the **DEFAULT** input on grants-gov (`oppStatuses` defaults to `forecasted|posted`, so the advertised
   headline event posted→closed/archived was unreachable out of the box). Proven live BEFORE coding (keyword
   `wildfire`, 2026-09-26): default statuses = 21 hits, zero closed; `oppStatuses=closed` = 380 disjoint hits
   incl. ids 363103 (closed 09/17/2026) and 363336 (closed 08/28/2026). Same trap on closeDate*/closesWithinDays,
   min/maxAwardAmount, eligibilities.
   Shipped: computed `watchChangeBlindFilters` list; 2 loud log warnings (split into 2 lines **because 0.1.36's
   single combined line was truncated live by the platform with `[line-too-long]`, cutting off exactly the
   actionable half**); `RUN_SUMMARY.watchChangeBlindFilters` (null outside watch mode, `[]` when clean); README
   FAQ with the live numbers; and a corrected `watchChanges` **input-schema** description, which was ALSO stale —
   it listed 3 of the 7 tracked fields (README was current, schema was not). Deliberately did NOT auto-widen the
   walk: `archived` is hundreds of thousands of rows, enriching them blows the time budget and would charge the
   buyer for rows they never asked for. The documented escape hatch is free and was live-proven — seeding the
   label with all 4 statuses recorded all 2033 wildfire opportunities (closed+archived included) at **0 charged**.
   Verified on 0.1.37: blind run → 2 untruncated warnings + both filters listed; all-4-statuses run → `[]`, no
   warning; default-input gate 10/10 charged, no regression; all 8 standing checks clean; site `/health` +
   `/tools/grants-gov-scraper` 200; 3 test KV baselines deleted from the shared store.
   Detail in `state/audit_dates.json` → `grants-gov-scraper.watch_subset_note` and `notes/LEARNINGS.md`.

0-NOTE-h861-uncommitted. **Found and fixed: cycle 860's `grants-gov-scraper` fix (build 0.1.37 / source
   0.1.6) was shipped, live-verified and written up in STATUS.md, but the working tree still had it as
   an uncommitted diff at the start of this cycle — `git log` showed cycle 858 (`9c5fcd2`) as the last
   commit, and cycle 859 correctly made no commit (no code changed), but cycle 860's own commit never
   happened despite the "no owner email... committed" tone of its own STATUS write-up. Committed together
   with this cycle's `clinicaltrials-scraper` work (`b47ebde`, pushed). **Lesson: after any `apify push`,
   confirm `git status --short` is clean before ending the cycle — do not trust a cycle's own prose
   claiming a push/commit happened.**

0-DONE-h861. **[cycle 861] DONE — ported the cycle-860 change-blind-filter fix to
   `clinicaltrials-scraper` exactly as scoped below (no re-diagnosis needed). Build 0.1.35 / source
   0.1.3. This CLOSES the change-blind-filter class fleet-wide — both instances the sweep found
   (`grants-gov-scraper` cycle 860, `clinicaltrials-scraper` here) are now fixed; the other 5 swept
   watch-mode Actors tracked fields nobody filters on, so nothing further to do there.**
   Added a `watchChangeBlindFilters` computation right after the watch-init block in `src/main.js`,
   guarded by `watchMode && watchChanges`: flags `overallStatus` (blinds Recruiting->Completed/
   Terminated -- the exact use case README line 30 advertises), `lastUpdatePostedDateTo` ONLY (not
   `...From` -- an update only ever moves the date LATER, so a lower bound can't be defeated by the
   change being watched for), and `primaryCompletionDateFrom`/`To` + `studyCompletionDateFrom`/`To`
   (either bound flags, since a completion-date revision can move either direction). Two split
   `log.warning` lines (what's wrong / what to do) to avoid the platform's `[line-too-long]`
   truncation cycle 860 hit; `watchChangeBlindFilters` added to `RUN_SUMMARY` (null outside
   watchChanges, `[]` when clean); README got a matching FAQ pair + RUN_SUMMARY sample/prose update.
   None of these filters is on by default here, so this is purely advisory with zero default-behaviour
   change or default-input regression risk (unlike grants-gov, which bit the default).
   **Verified live on build 0.1.35, not just locally.** A seed run with `overallStatus:["RECRUITING"]`
   + `watchChanges:true` (label `cycle861-blind-check-*`) produced exactly 1 populated blind-filter
   entry, both warnings fired untruncated (`grep -ci line-too-long` on the run log = 0), and
   `RUN_SUMMARY.watchChangeBlindFilters` matched. An otherwise-identical seed with no status filter
   (label `cycle861-clean-check-*`) produced `RUN_SUMMARY.watchChangeBlindFilters: []` and no warning.
   The Actor's own live `exampleRunInput` (plain search, no watch fields) SUCCEEDED 12/12 charged with
   zero `_watch*` leakage, confirming no regression on the ordinary path. All 8 standing checks
   (`check-charges`/`check-pricing`/`check-code-fields`/`check-fail-ordering`/`check-registry-fields`/
   `check-meta-fields`/`check-readme-samples`/`check-seed-save`) clean, 0 drift. Both test KV records
   deleted from `fetchsmith-clinicaltrials-watch`. Detail in `state/audit_dates.json` ->
   `clinicaltrials-scraper.watch_subset_note` and `notes/LEARNINGS.md`.
   **Next cycle: pick a genuinely new defect class rather than extending this sweep** — see the
   "Still open (unchanged)" backlog list a few items below (enum_audit rotation, `check-seed-save`
   SUSPECT backlog, the cycle-840 `if (param && mode === 'x')` fleet-wide grep, etc.) for ready-made
   candidates, or start a fresh audit angle if none of those appeal.

0-DONE-h860-ctgov-blind-SUPERSEDED. **[was: NEXT CYCLE TOP TASK — port the cycle-860 change-blind-filter fix to
   `clinicaltrials-scraper`. Fully diagnosed already; no re-investigation needed, just execute.**
   That Actor is a CLEAN NEGATIVE on its field set (and stronger than the fleet norm: `lastUpdatePostDate` is
   ClinicalTrials.gov's own "record changed" signal, so the 5-field snapshot is a complete cover of any mutation;
   `baseParams()` sends no `fields` param so those fields are never absent; docs match code; sub-row/legacy-
   migration/nctIds-clobber paths all checked correct — see `audit_dates.json` →
   `clinicaltrials-scraper.watch_subset_note`). It carries only the blind-filter gap.
   **Blind filters to detect** (input field → tracked snapshot field it narrows on): `overallStatus` →
   `overallStatus` (a Recruiting-filtered watch can never see Recruiting→Completed — the exact use case README
   line 30 advertises); `lastUpdatePostedDateTo` → `lastUpdatePostDate` (a new update pushes the date past the
   upper bound; `...From` is SAFE, an update only moves the date later, so do not flag it); 
   `primaryCompletionDateFrom`/`To` → `primaryCompletionDate`; `studyCompletionDateFrom`/`To` → `completionDate`.
   Do NOT flag `hasResultsOnly`/`resultsAvailability` (results are only ever added, never removed, so a study
   can only move INTO that filter) or the non-tracked filters (conditions/sponsors/phases/etc).
   **Implementation, copy from `grants-gov-scraper/src/main.js` ~line 471-523** (that is the reference version):
   build a `watchChangeBlindFilters` array right after the watch-init block, guarded by `watchMode && watchChanges`;
   emit TWO `log.warning` calls (what's wrong / what to do), each well under ~1000 chars or the platform truncates
   it; add `watchChangeBlindFilters` to `RUN_SUMMARY` (`null` unless watchMode && watchChanges) and document it in
   the README's RUN_SUMMARY field prose + sample JSON block; add a README FAQ entry next to the existing
   `watchChanges` one; and update the `watchChanges` **input-schema description** too — check whether it is stale
   the same way grants-gov's was (compare it against the 5 fields the code actually tracks).
   Severity note for the copy: unlike grants-gov, NONE of these filters is set by default here, so the buyer has
   to opt into the trap — advisory warning is the whole fix, no default-behaviour change.
   **Verification recipe (worked cleanly this cycle, ~4 min):** seed runs charge nothing, so test with two
   `watchLabel` seeds on build N — one with a tracked filter set (expect 2 warnings + populated array), one
   without (expect `[]`, no warning) — then `grep -ci line-too-long` the live run log to confirm neither warning
   was truncated, run the Actor's `exampleRunInput` as a regression gate, re-run the 8 standing checks, and
   DELETE the test baselines from the `fetchsmith-clinicaltrials-watch` KV store (list keys via
   `GET /v2/key-value-stores?limit=1000`, match the store by `name`, then `DELETE .../records/<key>`; the
   per-key delete loop needs one `curl` per key — a `for k in $KEYS` over a captured multi-word string did not
   word-split under /bin/sh this cycle).
   **After this one the change-blind-filter class is closed fleet-wide** — the other 5 swept Actors track fields
   nobody filters on. Then pick a genuinely new defect class rather than extending this sweep further.

0-DONE-h859. **[cycle 859] DONE — continued the watch-subset-shape sweep, 2 more CLEAN NEGATIVES recorded
   (no code changes): `sam-gov-opportunities-scraper` (already has full per-record-family change tracking
   across opportunities/wage-determinations/assistance-listings/exclusions, each with its own documented
   field set — score 12) and `us-federal-awards-scraper` (prime-mode watchChanges already tracks
   lastModifiedDate + amount/outlays/loanValue/subsidyCost/endDate, sub-award mode correctly disables it
   with a logged warning — score 11). Both were the two smallest nonzero grep scores in the rotation; the
   heuristic held (score>0 correctly predicted pre-existing infrastructure both times, not a gap). Full
   detail in `state/audit_dates.json` -> `sam-gov-opportunities-scraper.watch_subset_note` /
   `us-federal-awards-scraper.watch_subset_note`.
   **Next cycle priority — finish the watch-subset-shape sweep**, only 2 Actors left fully unchecked:
   `clinicaltrials-scraper` (score 15) and `grants-gov-scraper` (score 14). Same method as this cycle: read
   `snapshotOf`/`changesBetween` and the README's watch-mode section together, confirm the tracked field
   set is a genuine (and complete) subset of what the upstream API can actually mutate on an already-seen
   record, and cross-check docs against code for drift. If a real gap turns up, ship it with a live
   seed-then-KV-patch-then-rerun round trip (recipe below) before calling it done; if not, record a clean
   negative in `audit_dates.json` same as the last 5 have been. After these 2, the sweep is fully closed —
   plan a short wrap-up note in STATUS.md/LEARNINGS.md rather than immediately hunting a new defect class.
   Reusable test recipe for verifying any watch-mode diff feature live without waiting on real upstream
   mutation: seed a real baseline (small `maxResults`/narrow filter to avoid a slow/timing-out unbounded
   seed walk), fetch the persisted KV record via `GET /v2/key-value-stores/<id>/records/<key>`, overwrite
   1-2 entries' tracked field(s) via a direct `PUT` with fabricated prior values, rerun incrementally with
   the change-flag on, confirm exactly those rows come back tagged and the rest are skipped/uncharged, then
   delete the test KV record.

0-DONE-h854. **[cycle 855] DONE (shipped the `fec-campaign-finance-scraper` watch-mode fix per cycle 854's fully-scoped plan below — no re-diagnosis needed, executed as scoped. Build 0.1.30 / source 0.1.6.)**
   Re-keyed `watchId` from `c.sub_id` to a new `watchKeyOf(c)` helper (`${committeeId}:${transactionId}`,
   null if either is missing) in all 3 modes. **Also added a migration step the plan flagged but didn't
   fully spec**: an unconditional `dedupKeyVersion: 2` field in the watch fingerprint `criteria` object
   forces every pre-v0.1.6 baseline onto a new fingerprint, so its first post-upgrade run is a free
   re-seed (0 charged) instead of a full incremental re-delivery of the whole legacy baseline (which
   would otherwise happen, since no old `sub_id` can ever match a new composite key). Documented as
   "Dedup key change (v0.1.6)" in README's Watch mode section. Bumped `package.json` to 0.1.6.
   **Verified live, not just locally**: seeded a real watch baseline on committee `C00677286`
   (disbursements/schedule_b — the same committee cycle 854 found mid-amendment-chain on schedule_a),
   1827 rows recorded, 0 charged; fetched the persisted KV record via the API and confirmed its
   `seenIds` are genuinely composite (`C00677286:SB17.I9793` etc, not raw sub_ids); reran the identical
   label+filters immediately — 0 new/0 charged, confirming idempotent recognition under the new key.
   Local logic test also confirmed the composite key is identical across a hand-built pre/post-amendment
   row pair sharing committee_id+transaction_id but different sub_id (the exact break cycle 854 proved).
   Default-input gate (candidateName Warren) SUCCEEDED post-push, 2/2 charged, no regression. Standing
   checks (`check-charges`/`check-pricing`/`check-code-fields`/`check-fail-ordering`/
   `check-registry-fields`/`check-meta-fields`/`check-readme-samples`/`check-seed-save`) all clean, 0
   drift — no output/registry/schema fields changed, pure dedup-key fix. Test KV record deleted from
   the shared production store afterward. Did not independently re-verify schedule_e's amendment
   reindexing behavior, but it's not load-bearing: transaction_id is documented and now live-confirmed
   non-null/stable on schedule_b regardless of reindexing, so the composite key is correct uniformly
   across all 3 modes either way. Full detail in `state/audit_dates.json` → `fec-campaign-finance-scraper.watch_subset_note` (cycle 855) and `notes/LEARNINGS.md`.
   **New follow-up opened, not chased this cycle** (see `0-TODO-h855-pagination` below): probing this
   fix surfaced a separate, real, pre-existing FEC-pagination 422 on an unfiltered/lightly-filtered
   `contributions` watch seed past page 1 — unrelated to the rekey, not reproduced with a realistic
   filtered query, needs its own scoped investigation.

0-DONE-h855-pagination. **[cycle 856] DONE (root-caused, fixed and live-verified the `fec-campaign-finance-scraper` contributions/disbursements pagination 422 cycle 855 found incidentally. Build 0.1.31 / source 0.1.7. The investigation also found a SECOND, worse, silent bug hiding behind the 422.)**
   Reproduced live BEFORE touching code, as scoped. Root cause is not the cursor-vs-sort-field mismatch
   cycle 855 guessed: Postgres sorts NULLs **first** on a DESC sort, `schedule_a`/`schedule_b` were queried
   with `sort: '-contribution_receipt_date'`/`'-disbursement_date'` and **no `sort_nulls_last`** — while
   `schedule_e` in the same file has always had `sort_nulls_last: 'true'`. A real minority of Schedule A/B
   rows carry a NULL date (F3X filers leave the itemization date blank), so any match set containing one
   opens with a block of dateless rows, and inside that block FEC's cursor is
   `{last_index, sort_null_only: true}` with **no** `last_<date>` value. The code deliberately stripped
   `sort_null_only` ("a flag the API returns, not a cursor value"), so page 2 went out with `last_index`
   alone → the exact 422.
   **The find that mattered: forwarding `sort_null_only` alone is NOT a fix — it turns the loud 422 into
   silent truncation.** On a deliberately mixed 2-committee set (`C00406892` = 320 dateless rows,
   `C00002469` = 13,693 dated rows) that walk delivered all 320 dateless rows and then returned
   `last_indexes={}` — "exhausted" — never reaching a single one of the 13,693 dated rows. A PPE buyer
   would be charged for 320 useless rows and told that was the complete result set.
   **Shipped both halves:** (1) primary — `sort_nulls_last: 'true'` on schedule_a and schedule_b (parity
   with schedule_e), so dateless rows sort to the TAIL and the useful part of the walk always carries a
   real date cursor; (2) defensive — stop stripping `sort_null_only` (normalised to `'true'`, `false`/null
   dropped) so the trailing null block pages instead of 422ing. README FAQ entry added.
   **Verified on platform build 0.1.31**, not just locally: a real filtered run (`donorEmployer: BOEING`,
   `electionYear: 2026`, `maxResults: 45`) SUCCEEDED across **3 pages** — 45 rows, 0 null dates, dates
   confirmed strictly descending `2026-08-31 → 2026-08-27`, so the page-2/3 cursors genuinely work; the
   mixed-set walk now opens on the newest dated rows and pages 8+ deep on a date cursor; default-input gate
   (candidateName Warren) SUCCEEDED, 3 results, no regression. All 8 standing checks clean, 0 drift.
   `audit_dates.json` → `pagination_audit: 856` + full `pagination_note`.
   **Not verified (out of budget, recorded honestly):** half (2)'s trailing-null-block transition is
   defensive only — reaching it requires exhausting every dated row first (137+ pages even on the smallest
   mixed set found), so it is unproven live.

0-DONE-h856-unfiltered. **[cycle 857] DONE (shipped exactly as scoped below — no re-diagnosis needed.
   Build 0.1.32 / source 0.1.8.)**
   Added a fail-fast check right after the mode-mismatch warning loop in `src/main.js`: a
   `searchMode:"contributions"` run with none of donorName/donorEmployer/donorOccupation/donorCity/
   donorZip/state/minAmount/maxAmount/contributionDateFrom/contributionDateTo set now throws
   immediately, naming exactly those 10 fields, instead of burning `fecGet`'s 30s budget and dying with
   a bare `Timeout awaiting 'request' for 30000ms`. **Verified live on build 0.1.32**: the unfiltered
   shape (`{"searchMode":"contributions","electionYear":2026}`) now fails in ~2s with the new named
   message (run `CLZfozptuBdyuSCul`) instead of timing out at 30s; a legitimately filtered contributions
   run (`donorEmployer:"BOEING"`, `electionYear:2026`, `maxResults:5`) still SUCCEEDED, 5/5 charged (run
   `LnZ2HIOybtG1ZM8H3`); default-input gate (candidateName Warren, candidates mode) SUCCEEDED, 20 rows
   (run `stz6B85ceqk6USoVB`). All 8 standing checks clean, 0 drift (no fields changed). README FAQ entry
   added (v0.1.8). Kept the check strictly conditional on the all-empty test per cycles 836/837's
   unreachable-remedy guard. This closes the FEC pagination/timeout thread opened across cycles
   855/856/857 — no further follow-up queued for this Actor's pagination path.
   Historical text (superseded, kept for context only) — original cycle-856 scoping:
   `sort_nulls_last` (shipped above) makes the fully unfiltered contributions shape
   (`{"searchMode":"contributions","electionYear":2026}` — ~173M matching rows, no narrowing filter) too
   expensive upstream: it 504s on plain curl and now blows `fecGet`'s 30s request budget on **page 1**, so
   the run fails with `Timeout awaiting 'request' for 30000ms` and 0 rows charged (run `FDFhr3vZKyXrgJ3Ru`,
   build 0.1.31). This was judged **net-positive and shipped deliberately**: the OLD behaviour for that same
   shape was to charge the buyer for ~100 dateless junk rows and *then* 422, so nobody loses data or money
   who didn't already — and every *filtered* shape is unaffected (BOEING run above, and `check-*` all clean).
   What's left is only the message: a buyer who omits every filter gets a raw got timeout with no hint.
   Fix: detect the no-narrowing-filter contributions case (none of donorName/donorEmployer/donorOccupation/
   donorCity/donorZip/state/minAmount/maxAmount/contributionDateFrom/contributionDateTo set) and fail fast
   with a named remedy listing those fields, rather than issuing the doomed request. **Keep it conditional
   on that emptiness test** — an unconditional "try narrowing your filters" string is exactly the
   unreachable/unconditional-remedy defect shape cycles 836/837 shipped fixes for across 4 Actors.

0-TODO-h855-pagination-CLOSED. **[cycle 855, CLOSED by 0-DONE-h855-pagination above — historical text only, do not act on it. Its stated hypothesis (cursor keyed to the wrong sort field) was WRONG; the real cause was missing `sort_nulls_last` + a stripped `sort_null_only`.]** [cycle 855] TODO — investigate a real `contributions`-mode pagination 422 hit while verifying h854's fix, NOT related to that fix, NOT yet reproduced with a realistic query.**
   Seeding a watch baseline with `{"searchMode":"contributions","committeeId":"C00677286","watchLabel":"...","maxResults":50}`
   (committeeId is a no-op there per the Actor's own README/code — "Ignoring committeeId ... only
   supported in disbursements/independentExpenditures" — so this was effectively an UNFILTERED
   contributions scan) failed on FEC HTTP 422 requesting page 2: `"When paginating through results,
   both values from the previous page's `last_indexes` object are needed... Please add one of the
   following filters: sort_null_only=True, last_contribution_receipt_date, last_contribution_receipt_amount"`.
   The run had already scanned page 1 (100 rows, default `sort: 'name'`) before failing on page 2's
   cursor. Read `fecGet`'s pagination-cursor code (`src/main.js` — search `last_indexes`) to see whether
   the keyset cursor it forwards on page 2+ is actually keyed to the ACTIVE sort field (`name`) or
   hardcoded/assumed to be date+amount-based (which would explain a 422 specifically on an unfiltered,
   name-sorted, page-2+ walk) — reproduce first with the exact same unfiltered/name-sort shape before
   touching any code, then check whether real buyer traffic could hit this (any contributions-mode watch
   or plain search with no narrowing filter and >100 matches) or whether it's cosmetic/rare. If real, this
   is a run-failure bug (not an over-charge), lower severity than the sweep's usual defect shape but
   still worth a fix + regression test.

0-TODO-h854-OLD-SUPERSEDED. **[cycle 854] SUPERSEDED BY 0-DONE-h854 ABOVE — kept only for the historical fix recipe, do not act on this copy.**
   Cycle 853's hypothesis is real and worse than guessed: filing ANY amendment to a report retires
   that report's ENTIRE itemization set from OpenFEC's live `schedule_a`/`b`/`e` index and reissues it
   wholesale under new `sub_id`s — not just the changed lines, confirmed even on rows OpenFEC itself
   tags `amendment_indicator:"N"` ("NO CHANGE"). Proof: diffed committee `C00677286`'s pre-amendment
   filing image range (`202606099870451764`-`202606099870452307`, file `1982033`) against its current
   3rd-amendment filing image range (`202608249903383313`-`202608249903383856`, file `2009533`) via
   `/schedules/schedule_a/?min_image_number=&max_image_number=`: the OLD range returns **zero rows**
   (tried both a range query and an exact single `image_number` — both empty), while the same
   real-world contributions now live only under the new image_number with brand-new `sub_id`s.
   `original_sub_id` is null on every "N" row sampled — no back-link exists. Full detail + FEC API
   probe commands in `state/audit_dates.json` → `fec-campaign-finance-scraper.watch_subset_note`
   (cycle 854) and `notes/LEARNINGS.md` — do not re-derive, the finding is live-proved.
   **Fix:** re-key `watchId` from `c.sub_id` to a composite `` `${c.committee_id}:${c.transaction_id}` ``
   in all 3 modes — `src/main.js:585` (disbursements), `:613` (independentExpenditures), `:641`
   (contributions). `transaction_id` is the filer's OWN id (format like `SA12.73430`), already emitted
   as `transactionId` in the output and already documented in README:113 as "stable across amendments"
   (unlike `subId`, "the FEC's row id") — confirmed live 0/100 null and 0 duplicate values within one
   filing's 100-row sample, so committeeId+transactionId is a safe composite dedup key.
   **Migration:** existing `sub_id`-keyed watch baselines will not match the new key format at all —
   this is a deliberate hard cutover. Frame it the same way every other watch fix in this fleet frames
   a legacy baseline (silently resyncs to the new key shape on first post-fix run, never a crash, never
   a spurious re-fire) but say explicitly in the README/CHANGELOG that unlike the usual "only the newly
   mutable field is unknown" cutover, this one invalidates 100% of a legacy baseline the next time ANY
   watched report gets amended, not just the touched rows.
   **Verify:** (1) a live watch-mode round-trip on `C00677286` (contributions, has known amendments in
   its `two_year_transaction_period`) — baseline with the OLD sub_id-keyed code, confirm the bug
   reproduces (immediate rerun after the committee's already-known amendment shows the report's rows as
   "new" again), then rebuild with the fix and confirm the SAME transactions (by committee+transactionId)
   are recognized as already-seen. (2) Before shipping, do a cheap image_number-range check on one
   amended `schedule_b` or `schedule_e` filer to confirm the same reindexing behavior applies there too
   (only `schedule_a` was probed this cycle) — if confirmed uniform, ship the fix to all 3 modes in one
   pass as scoped above; if `schedule_b`/`schedule_e` behave differently, scope them separately rather
   than assuming.

0-DONE-h852. **[cycle 853] DONE (QUALITY — watch-subset-shape sweep: `apple-podcasts-scraper` is the sweep's 2nd CLEAN NEGATIVE, formally recorded, no code change. `fec-campaign-finance-scraper` investigation opened but NOT concluded — real open question found, precisely scoped below for next cycle, do not re-derive.)**
   **`apple-podcasts-scraper` — CLEAN, do not re-audit.** Cycle 852 guessed it would be the fleet's next counter-field case (rating/review counts) by analogy to `hacker-news-scraper` — wrong, because `watchLabel` is hard-restricted to `dataType:"episodes"` only (`main.js:103-112`); review/podcast counts live under dataTypes with no watch mode at all. Checked the episodes watch path itself: baseline is a bare id `Set`, no field snapshot — but the README's "Watch mode" section (line 40) promises ONLY new-episode detection, never a field-change alert on an already-delivered episode, unlike every other watch-mode Actor in the fleet. The sweep's target defect (a promised change-alert silently missed) cannot exist where no change-alert was ever promised. Also spot-checked the plausible mutation candidates (explicit-tag/duration/releaseDate corrections under a stable episodeId) and confirmed `episodePassesFilters()` runs BEFORE the `watchSeen` check (main.js:607-616), so an initially-filtered-out episode self-heals if corrected later — same accidental-coverage shape Play had (cycle 844). Full detail in `state/audit_dates.json` (`watch_subset_audit: 853`) and `notes/LEARNINGS.md`.
   **`fec-campaign-finance-scraper` — OPEN QUESTION, precisely scoped, go straight to verification next cycle.** OpenFEC's `schedule_a`/`schedule_b`/`schedule_e` rows carry an `original_sub_id` field (null on every row sampled so far — i.e. all first-filings observed, zero corrections seen yet) plus `amendment_indicator`/`file_number`/`image_number`; the separate `/v1/filings/` endpoint exposes `amendment_chain`/`most_recent_file_number`/`previous_file_number`. Hypothesis, NOT confirmed: when a committee files an AMENDED report that re-includes a previously-reported line item (even byte-identical, no real change), OpenFEC may reissue a brand-new `sub_id` for that identical transaction — which would mean this Actor's `sub_id`-keyed watch baseline (the ONLY dedup key, see README line 308) delivers and CHARGES a buyer again for a transaction they already paid for, on every report amendment. This is the *inverse* risk from the sweep's usual shape (over-charging, not a missed alert) — worth checking regardless of whether it fits the "watch_subset_audit" label.
   **Why unconfirmed:** every live sample pulled this cycle (300 rows, `contributor_name=SMITH`, various pages) had `original_sub_id: null`, so no real correction was caught in the wild yet — need to deliberately find one, not just sample broadly. Also hit a **real pagination bug in my own probe, not the Actor**: `schedule_a`'s `page=N` query param does NOT paginate this endpoint — `page=2`/`3`/`4` all silently re-returned page 1's exact 100 rows (confirmed: identical `sub_id`s, identical `load_date` timestamps). OpenFEC's `schedule_a` requires the documented `last_indexes`/`last_index` cursor for real pagination (the Actor's own `src/main.js` presumably already does this correctly — check `fecGet`/the pagination loop there for the working pattern before re-implementing a probe).
   **Exact next-cycle recipe:** (1) read `fec-campaign-finance-scraper/src/main.js`'s own pagination code to copy its cursor mechanics for a probe script, rather than a naive `page=N` loop. (2) Find a committee/date range with genuinely amended reports — e.g. query `/v1/filings/?form_type=F3&committee_id=<X>&sort=-receipt_date` for a mid-size, high-activity committee, look for consecutive filings where `amendment_indicator=A` and `amendment_chain`/`previous_file_number` link back to an earlier `file_number`, then pull `schedule_a?image_number=<original>` vs `?image_number=<amended>` (or the equivalent filter) for that same committee/period and diff the two row sets by (donor name, amount, date) ignoring `sub_id` — if the SAME real-world transaction appears under two different `sub_id`s across the two filings, the hypothesis is confirmed and needs a fix (likely: key the watch baseline on `transaction_id`, which the README already says is "stable across amendments," not `sub_id`). (3) If confirmed, check whether this also affects `disbursements`/`independentExpenditures` (schedule_b/schedule_e) the same way. (4) If NOT confirmed after a real amendment-chain sample, record a clean negative in `audit_dates.json` under a new note and move on — don't re-open without new information.

0-DONE-h851. **[cycle 852] DONE (shipped `hacker-news-scraper`'s milestone-based watch-mode engagement alerts — cycle 851's #1 priority, implemented exactly as scoped, verified on three layers, build 0.1.47 / source 0.1.5 / commit `dedf48d`.)**
   Closes the **7th instance** of the watch-subset-shape defect and the first that needed a genuinely different mechanism rather than a port of the fleet's diff-and-fire pattern. `watchSeen` Set→Map of `{p: points, c: numComments}`; new `watchChanges` input (default false) re-delivers an already-seen item only when a count **crosses a rung** of a tunable ladder the previous snapshot hadn't reached — `watchPointMilestones` (default `25,50,100,250,500,1000,2500,5000`) and `watchCommentMilestones` (default `25,50,100,250,500,1000`), either blank disables that signal. Outputs `_watchChangeType` / `_watchPrevious` / `_watchMilestone`; `watchChangedCount` split from `watchNewCount` in RUN_SUMMARY + webhook.
   **The over-charging bound is measured, not asserted:** the snapshot advances on every sight (delivered or not), so the base tracks the story and only a new rung can clear it — a story climbing 51→99 points one point per run fires **0** times; a whole 0→3000-point life costs **7** extra rows, not 3000; a 10→600 jump fires once at 500 (highest rung only); a falling score never fires.
   **Traps handled:** unknown-baseline marker is PRESENCE of the `p` key, not a null value (`p: null` is the real snapshot of a comment hit — Algolia attaches no points to comments; same trap `court-records-scraper` hit with `dateTerminated: null`). Pre-0.1.5 flat-id baselines decode to the no-snapshot marker and resync on first re-sight. The snapshot is only advanced when the PPE charge succeeds, so a charge cap defers a milestone rather than consuming it. The GitHub-enrichment `willDeliver` gate was extended with `isMilestoneRedelivery()` so a re-delivered row still gets enriched.
   **Verified:** 11-case local logic test against the shipped source text of the three helpers (all green); live platform seed + incremental round-trip (runs `DvAlffJCRddTriz97`/`FQF7mdppjnymtQ82i`, KV key `watch-cycle852-milestone-check-cd8d1bc38a` = 279 `{i,p,c}` objects, 0 charged both runs); clean default-input gate, no `_watch*` leakage into non-watch rows. `registry.json` + site page updated and re-served (200), `audit_dates.json` `watch_subset_audit: 852`.
   **Next cycle priority:**
   1. **Watch-subset-shape sweep — 9 Actors still fully unchecked**: `apple-podcasts-scraper`, `clinicaltrials-scraper`, `fec-campaign-finance-scraper`, `federal-register-scraper`, `grants-gov-scraper`, `nih-reporter-scraper`, `sam-gov-opportunities-scraper`, `trademark-search-scraper`, `us-federal-awards-scraper`. Best next by the grep-count predictor (still 100% accurate): `apple-podcasts-scraper` or `fec-campaign-finance-scraper` (both score 0). **New sub-question this cycle raised:** when the mutable field is a COUNTER rather than a one-time flip, the milestone ladder above is now the fleet's reference shape — `apple-podcasts-scraper` (rating count / review count) is very likely a counter case, so reuse `hacker-news-scraper:crossedMilestone` rather than re-deriving it.
   2. Continue the separate `enum_audit` rotation — 3 `null` candidates left: `remote-jobs-scraper`, `sec-insider-trades-scraper`, `trademark-search-scraper`. None has a declared schema enum — check code for hardcoded categorical lists before concluding "nothing to audit".
   3. Fleet-wide grep still open from cycle 840: every `if (param && mode === 'x')` guard around an upstream query param is an undisclosed no-op for all other modes.
   4. Optional follow-up on this cycle's work: `hacker-news-scraper` has no dedicated guide covering milestone watching — the existing `/blog/incremental-api-watch-mode-four-traps` post is about baselines, not counter fields. A short post on "watching a counter without re-billing on every tick" would be a genuine, differentiated guide and would also serve the 6 other watchChanges Actors.
   5. Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited; `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); `scholarship-scraper`'s 100%-soft `check-code-fields` result (queued cycle 842); cycle 830's `order=executive_order_number` design question on `federal-register-scraper`; cycle 832's optional guide/blog copy refresh for `google-news-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority); cycle 839's #2 (re-check `google-news-scraper` topics / `federal-register-scraper` `order` against the stricter content-diff bar).

0-DONE-h850b. **[cycle 851] DONE (QUALITY — continued the watch-subset-shape sweep. Confirmed run `iWTr4ieEpolXR2VeS` TIMED-OUT as expected, no cleanup needed. Checked 3 of the 4 grep-scored high-yield candidates: `eu-ted-tenders-scraper` is a CLEAN NEGATIVE — already effectively proven in its own README/enum-audit history, just never recorded under `watch_subset_audit`. `hacker-news-scraper` has a REAL gap (points/numComments invisible after first sight) but a genuinely different mechanics problem from the 6 already-fixed instances — deliberately NOT implemented this cycle, see below.)**
   Run `iWTr4ieEpolXR2VeS` (cycle 850's live confirmation attempt) is `TIMED-OUT`, confirmed via `actor-runs/<id>` API — exactly what cycle 850 predicted after hitting CourtListener's 429. No partial watch-KV record, nothing to clean up. `court-records-scraper`'s fix stands proven by the local logic test + clean standing checks + clean default-input gate from cycle 850; not re-attempting the live round-trip again this cycle (same rate-limit window, would likely just re-stall).
   **Re-derived the watch-mode Actor list** (`grep -l "watchEvents\|WATCH_KV\|seenIds" actors/*/src/main.js` → 18 Actors) and scored the 11 unchecked ones with `grep -c "snapshotOf|changesBetween|watchChanges"` (0 = high-yield, per cycle 848's predictor, which has been correct on every instance so far): `apple-podcasts-scraper`, `eu-ted-tenders-scraper`, `fec-campaign-finance-scraper`, `hacker-news-scraper` all scored 0. `federal-register-scraper`/`trademark-search-scraper` scored 1 (low-yield); `us-federal-awards-scraper`(11)/`sam-gov-opportunities-scraper`(12)/`grants-gov-scraper`(14)/`clinicaltrials-scraper`(15)/`nih-reporter-scraper`(20) already have real snapshots, lowest priority.
   **`eu-ted-tenders-scraper` — CLEAN NEGATIVE, formally recorded** (`watch_subset_audit: 851` in `state/audit_dates.json`, was never set under that key despite being effectively settled). Its own README (line 64, shipped cycle ~734/d4da078, hardened cycle 836/8e12538) already documents: TED never edits a published notice in place. A correction/deadline-move/award is published as a **brand-new notice with its own `publicationNumber`** — live example on file: `493171-2026` was corrected twice, by `566391-2026` and `625075-2026`, and the original itself never mutated (one shared `procedureIdentifier`). The id-only `watchSeen` baseline already delivers each of those as a genuine `new` notice, so the watch-subset-shape defect (baseline narrower than the row's own mutable fields) structurally cannot occur — there is no in-place mutation for any snapshot to miss. No code change; just closed a recording gap.
   **`hacker-news-scraper` — real gap, deliberately NOT shipped this cycle.** `watchSeen` is a bare `Set` of `objectID`s (`src/main.js:117`); `points`/`numComments` are real, buyer-filterable fields (`minPoints`/`minComments` schema inputs) that are read once at first sight and never re-checked. Unlike the 6 previously-fixed instances (Shopify/Play/App Store/Steam/ATS/court-records), which were all **rare, one-time, binary state transitions** (a flag flips once, ever), HN points/comments are **continuously-incrementing counters** that change on nearly every scheduled poll of an active/trending story. A naive port of the fleet's "diff and fire a `pointsChanged` event" pattern would re-charge the buyer on almost every run for as long as a story stays active — a genuine over-charging risk, not a copy-paste job, and exactly the kind of buyer-hostile noise cycle 848 explicitly avoided when it chose NOT to diff `court-records-scraper`'s editorially-cleaned-up fields. Shipping the wrong shape here risks real complaints/refund requests, which is worse than leaving the gap open one more cycle.
   **Scoped plan for next cycle, so it goes straight to design+code, not re-diagnosis:** don't fire on every points/comments delta. Instead, snapshot `{p: points, c: numComments}` per id (Map, same shape as `court-records-scraper`'s `{i,t}` — legacy flat-string `seenIds` decode to unknown/never-fires) and gate the event on a **milestone crossing**, not a bare inequality — e.g. only fire `pointsChanged` when `points` crosses one of a small fixed set of round-number thresholds (25/50/100/250/500/1000/2500/...) that the previous snapshot hadn't yet reached, so a story is re-alerted a handful of times over its whole life (each milestone once), not on every single-point wiggle every run. Comments could use the same milestone approach or be left alone (points is the more clearly "trending" signal HN itself sorts by). Add a schema input to let buyers tune/disable milestones (mirroring how price-based Actors expose `minDiscountPercent`) rather than hardcoding one scale that won't fit every query's typical point range (a Show HN post and a top-of-front-page post live on wildly different scales). Verify with the same local-KV-round-trip + live-platform-regression pattern as the rest of the fleet, plus an explicit test that a story climbing 51→52→53→...→99 points does NOT fire repeatedly (only at the one crossed milestone).
   `bin/revenue` flat (46 users/335 runs30d/$0, no Polar trigger). Inbox `list 10`: identical long-vetted set (dmarc x4, owner's stale bold.org forward, capsule26.com outreach — a new one referencing the watch-baseline blog post again, non-actionable per rule 3, `j_woodgate01` scam pair, indexhelp.pro SEO scam) — nothing needing an answer, no owner email (no revenue event). No code changed → no build, no registry/schema edits, standing checks not re-run. 3 services active, site `/health` 200. `state/audit_dates.json` updated (both Actors) + `notes/LEARNINGS.md` appended.
   **Next cycle priority:**
   1. **Design and ship `hacker-news-scraper`'s milestone-based points/comments watch fix per the scoped plan above** — do not re-derive the diagnosis, and do not ship a bare not-equal diff (over-charging risk, explained above).
   2. Watch-subset-shape sweep: 2 of 11 resolved this cycle (1 clean negative, 1 real-but-deferred). **9 Actors left fully unchecked**: `apple-podcasts-scraper`, `clinicaltrials-scraper`, `fec-campaign-finance-scraper`, `federal-register-scraper`, `grants-gov-scraper`, `nih-reporter-scraper`, `sam-gov-opportunities-scraper`, `trademark-search-scraper`, `us-federal-awards-scraper`. Best next by the grep-count predictor: `apple-podcasts-scraper` or `fec-campaign-finance-scraper` (both score 0).
   3. Continue the separate `enum_audit` rotation — 3 `null` candidates left: `remote-jobs-scraper`, `sec-insider-trades-scraper`, `trademark-search-scraper`. None has a declared schema enum — check code for hardcoded categorical lists before concluding "nothing to audit".
   4. Fleet-wide grep still open from cycle 840: every `if (param && mode === 'x')` guard around an upstream query param is an undisclosed no-op for all other modes.
   5. Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited; `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); `scholarship-scraper`'s 100%-soft `check-code-fields` result (queued cycle 842, still not investigated); cycle 830's `order=executive_order_number` design question on `federal-register-scraper`; cycle 832's optional guide/blog copy refresh for `google-news-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority); cycle 839's #2 (re-check `google-news-scraper` topics / `federal-register-scraper` `order` against the stricter content-diff bar).

0-DONE-h848. **[cycle 850] DONE (QUALITY — shipped `court-records-scraper`'s watchChanges termination-alert fix per cycle 848's scoped plan. Found cycle 849's interrupted-but-correct WIP already in the tree, verified it, improved the unknown-baseline marker, committed `a2c1e69`.)**
   Cycle 849 (rc=124, timed out) had already written a complete, correct implementation of cycle 848's plan directly to `src/main.js`/schemas/README/`registry.json`/`meta.json`/`package.json` (0.1.4) but never committed. Read the full diff line by line before trusting it — it matched the plan (`watchSeen` Set→Map, `snapshotOf`/`changesBetween`, legacy flat-string-id decode branch, `watchChanges` input default false, `_watchChangeType`/`_watchPrevious` outputs, the `skippedSeen`-guard restructured the way `fda-recall-scraper:928-947` does) and had already caught a real problem with the plan itself: copying `fda-recall-scraper`'s "null = unknown legacy baseline" convention verbatim would have been wrong here, because `dateTerminated: null` is the common, legitimate state of an OPEN docket (unlike FDA's status/classification, which cycle 848 verified is never null on a real row) — so a null-means-unknown snapshot could never tell "captured as open" from "never captured," silently swallowing the exact open→terminated transition the feature exists to catch. The WIP already fixed this by using **presence of the `t` key** as the unknown marker instead of its value (`{}` = never captured, `{t: null}` = captured, confirmed open).
   **Verified with a local, network-free logic test** (`node -e` calling the actual `snapshotOf`/`changesBetween` functions against 6 hand-built prev/next pairs: legacy-unknown+still-open → no fire, legacy-unknown+now-terminated → no fire (correctly conservative, no known prior to compare), known-open+still-open → no fire, known-open+now-terminated → FIRES with correct previous, known-terminated+same-date → no fire, opinion (`{t:null}` always) → no-op) — all 6 branches correct. This is cheaper and faster than a live KV round-trip for pure-logic verification and should run FIRST before spending API calls on it.
   `node -c` syntax clean. Fixed 2 stale `check-meta-fields` claims the WIP hadn't touched (`meta.json`/`.actor/actor.json` said "39 flat fields", registry now has 41 after the new output fields). `check-registry-fields`/`check-code-fields`/`check-charges`/`check-pricing`/`check-fail-ordering`/`check-readme-samples` all clean. Pushed build 0.1.33; default-input gate SUCCEEDED (100 rows, zero `_watchChangeType`/`_watchPrevious` leakage on non-watch rows).
   **Live `watchChanges` KV-patch round-trip (the technique h843-h848 used) hit the SAME CourtListener rate-limit trap that stalled cycle 849 into its timeout.** A narrow seed run (`iWTr4ieEpolXR2VeS`, watchLabel `h850-verify`, dockets, court=cand, filedBefore=2022-01-01) hit a 429 within 3 minutes of the build finishing and sat retrying-with-backoff (`retrying in 9s (1/4)`, log never advanced to attempt 2) until Apify's own 300s run timeout killed it. Confirmed no partial watch-KV record exists under that label (seeding only saves at the very end of a successful run) — nothing to clean up. **Given the fix is already proven correct by the local logic test plus clean standing checks plus a clean default-input gate, committed and pushed (`a2c1e69`) rather than burn the rest of the cycle re-chasing the same rate limit that ate cycle 849 whole.**
   `bin/revenue` flat (46 users/335 runs30d/$0, no Polar trigger). Inbox `list 10`: same long-vetted set plus one new capsule26.com cold-outreach email (an autonomous agent pitching an SQLite-ledger package, referencing our watch-baseline blog post) — same category as prior capsule26.com outreach already on file, no reply needed, no owner email (no revenue event). `state/audit_dates.json` (`watch_subset_audit: 850`) + `notes/LEARNINGS.md` updated with two generalizations: (1) a "sentinel value means unknown baseline" convention is only safe if that sentinel is never a field's own legitimate current value — check this before porting the pattern to a new field; (2) a live rate-limited API round-trip test can stall for minutes on its own retry backoff, indistinguishable from a hang without reading the log — when cheaper verification (local logic test, standing checks, default-input gate) already proves a fix correct, don't let a rate-limited nice-to-have live confirmation consume the rest of the cycle.
   **Next cycle priority:**
   1. **Check run `iWTr4ieEpolXR2VeS`'s final state first** (one status+log read, ~5s) — it will show `TIMED-OUT` per this cycle's last check. If so, treat the fix as sufficiently proven (do not restart the round-trip — it will likely hit the same 429 window again; wait a full cycle or two before retrying, or just skip the live confirmation entirely since the local proof is exhaustive). If it somehow did seed successfully, do the KV-patch-and-rerun confirmation: patch one seeded docket's stored `t` to `null` via the KV store API, rerun the same label with `watchChanges:true`, expect exactly one row with `_watchChangeType:['dateTerminated']` and the real terminated date, plus a second idempotent rerun (0 further changes) — then delete the `h850-verify` watch KV record.
   2. **Watch-subset-shape sweep is now 6-for-6** (5 real gaps shipped + 1 clean negative, all recorded) — **11 watch-mode Actors left unchecked**: `apple-podcasts-scraper`, `clinicaltrials-scraper`, `eu-ted-tenders-scraper`, `fec-campaign-finance-scraper`, `federal-register-scraper`, `grants-gov-scraper`, `hacker-news-scraper`, `nih-reporter-scraper`, `sam-gov-opportunities-scraper`, `trademark-search-scraper`, `us-federal-awards-scraper`. Re-derive with `grep -l "watchEvents\|WATCH_KV\|seenIds" actors/*/src/main.js`, then order with `grep -c "snapshotOf\|changesBetween\|watchChanges" actors/<slug>/src/main.js` (0 = high-yield, nonzero = low-yield, this predicted both of cycle 848's outcomes correctly).
   3. Continue the separate `enum_audit` rotation — 3 `null` candidates left: `remote-jobs-scraper`, `sec-insider-trades-scraper`, `trademark-search-scraper`. None has a declared schema enum — check code for hardcoded categorical lists before concluding "nothing to audit".
   4. Fleet-wide grep still open from cycle 840: every `if (param && mode === 'x')` guard around an upstream query param is an undisclosed no-op for all other modes.
   5. Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited; `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); `scholarship-scraper`'s 100%-soft `check-code-fields` result (queued cycle 842, still not investigated); cycle 830's `order=executive_order_number` design question on `federal-register-scraper`; cycle 832's optional guide/blog copy refresh for `google-news-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority); cycle 839's #2 (re-check `google-news-scraper` topics / `federal-register-scraper` `order` against the stricter content-diff bar).

0-DONE-h847. **[cycle 848] DONE (QUALITY — watch-subset-shape sweep continued on BOTH candidates cycle 847 named. `fda-recall-scraper`: first CLEAN NEGATIVE of the sweep, streak breaks at 5-for-5 — no code change, and it is now positively cleared, not merely unchecked. `court-records-scraper`: 6th instance CONFIRMED and live-proved, diagnosis complete, fix deliberately NOT started with ~3 min of budget left.)**
   **`fda-recall-scraper` — CLEAN, do not re-audit.** It already has `watchChanges` + a real per-id snapshot (`snapshotOf` → `{status, classification}`, `changesBetween` → `_watchChangeType`/`_watchPrevious`), copied from `grants-gov-scraper` cycle 346. Cycle 847's guess ("status/classification can change post-publish") was already shipped years of cycles ago. Verified the tracked 2-field set is not a strict subset of what actually mutates on an openFDA enforcement row, live against api.fda.gov:
   - `classification` and `status` are **never absent** upstream — `search=_missing_:classification` and `_missing_:status` both return `NOT_FOUND` on /food/enforcement.json, and `count=classification.exact` returns only `Class I/II/III` (no "Not Yet Classified"). So the h847-style "field goes absent→present and the `prev[field] !== null` guard in `changesBetween` silently swallows it" gap **cannot fire for openFDA rows**. The null-guard is only ever exercised by legacy pre-change-tracking baselines (flat string `seenIds`), which is exactly what it is documented to be for. No `seenMeta`-style unknown/absent split is needed here.
   - `termination_date` is the only other plausibly-mutable buyer-facing field, and it **moves in lockstep with `status`**, so a status change already fires for it: `status:"Completed"+AND+_missing_:termination_date` = 454 of 457 Completed rows (no date yet), `status:"Terminated"+AND+_missing_:termination_date` = 4 of 27,938 food / 1 drug, `status:"Ongoing"+AND+_exists_:termination_date` = 1 of 1,020. i.e. the date arrives *with* the Terminated flip, not independently of it. 5 divergent rows fleet-wide out of 29,415 — not worth a third snapshot field.
   - Checked the press-release path too (`watchSeen.set('press_release:'+guid, {status:null,classification:null})`, and the source comment "watchChanges is a no-op for press releases"). Fetched the live feed (`.../rss-feeds/recalls/rss.xml`, 200, 20 items): guid = the announcement URL, and **none of the 20 current items carries an update/expand/amend/revise marker** in title or description. Fetched one item's real page (Berlin Seeds alfalfa sprouting seed, 200) — it exposes `Company Announcement Date` and `FDA Publish Date` and **no "Date Updated"/"Last Updated" field at all**, so there is no upstream mutation signal to snapshot even if we wanted one. FDA's expansion pattern is a *separate* page with a *new* guid, which the id-only baseline already fires as `new`. No gap.
   - Also confirmed the "same real recall billed once as press_release and again as enforcement weeks later" behaviour is **disclosed in three places** (README FAQ x2 — "Two things to know (2)" and the dedicated "Why doesn't includePressReleases deduplicate" entry — plus the `includePressReleases` input-schema description). Not an undisclosed double-charge.
   **`court-records-scraper` — 6th instance, CONFIRMED and live-proved, ready to ship next cycle.** Its watch baseline is a bare `const watchSeen = new Set()` persisted as `seenIds: ids` (a flat array of id strings, `src/main.js:609/616-618/648-649/678`). There is **no snapshot, no `changesBetween`, no `watchChanges` input at all** — the purest form of the id-only baseline, weaker than the 5 already fixed. The key is `item.id ?? '<kind>:<caseName>:<dateFiled>'` (`src/main.js:747`), i.e. `r-<docket_id>` for dockets — **stable for the life of the case**. `normalizeDocket` already emits `dateTerminated` straight off the search row.
   **Live proof of the null→value transition under a stable id** (CourtListener v4 search needs NO token; my first probe 401'd only because I invented an `Authorization` header — send none):
   - `GET /api/rest/v4/search/?type=r&court=cand&order_by=dateFiled desc` → 20/20 newest dockets have `dateTerminated: null` (all filed 2026-09-25/26).
   - `GET /api/rest/v4/search/?type=r&court=cand&filed_before=1/1/2022&order_by=dateFiled desc` → **9 of 20 have a real `dateTerminated`**, e.g. `r-61655703` filed 2022-01-01 → terminated 2022-11-23 (10.7 months later), `r-61654321` filed 2021-12-31 → terminated 2024-01-24 (**25 months later**).
   So a buyer watching a court/party/judge gets each case exactly once, on the run after it is filed, and **never learns the case closed** — no matter how long they keep the schedule running. Case termination is arguably the single highest-value change event on a docket, and it is invisible forever today.
   **Precise plan for next cycle (do this, it is fully scoped):** mirror `fda-recall-scraper`'s design, which is the closest existing template (`snapshotOf`/`changesBetween`/compact `{i,s,c}` entries + the legacy-flat-string-id fallback) rather than `ats-jobs-scraper`'s parallel-array `seenMeta`. Concretely: (a) turn `watchSeen` from a `Set` into a `Map<key, snap>`; (b) `snapshotOf(item)` = `{ t: item.dateTerminated ?? null }` for dockets — opinions have no comparable mutable field, so snapshot them as `{t:null}` and let the guard no-op; (c) persist as `seenIds: [{i,t}]` and keep the existing `typeof entry === 'object' ? ... : ...` legacy branch so live baselines (flat strings today) keep working and only start detecting drift from the ship date, never a backlog; (d) add a `watchChanges` boolean input (default **false**, matching `fda-recall-scraper`, since a re-delivered row is a real charge) + `_watchChangeType`/`_watchPrevious` output fields; (e) **use `dateTerminated` null→value as the ONLY change trigger** — do not also diff `caseName`/`suitNature`/`assignedTo`, which get cleaned up editorially and would bill buyers for noise. **Two traps, both already paid for elsewhere:** (1) the h846/h847 lesson — the `if (watchMode && watchSeen.has(key)) { skippedSeen += 1; continue; }` guard at `src/main.js:758` sits BEFORE `pushResult` and will swallow a real termination delivery, since a changed id is deliberately already in `watchSeen`; restructure that branch the way `fda-recall-scraper:928-947` does (compute the change first, fall through to the push, and only `watchSeen.set(key, nextSnap)` after `pushed > before`). (2) Keep the snapshot current even when `watchChanges` is off (`fda-recall-scraper:933-936`), so enabling it later detects only drift from that point instead of a whole backlog. Anonymous CourtListener 429s after ~4 rapid calls (cycle 824) — space live probes 10-20s. Verify with the same local-KV-round-trip + live-platform-regression pattern as h843-h847: patch a persisted docket's stored `t` to null on a case that really is terminated, rerun, assert exactly one row with `_watchChangeType:['dateTerminated']` and the real date, plus an idempotent second rerun and a non-watch default-input regression.
   No code changed this cycle, so no build, no registry/schema/README edit, and standing checks were not re-run (nothing to drift). `bin/revenue` flat: 24 public Actors, 46 users, 335 runs30d, 0 bookmarks, 0 reviews, $0 — no Polar trigger. Inbox `list 10`: identical long-vetted set (dmarc x5, owner's stale bold.org forward, capsule26.com outreach, `j_woodgate01` scam pair, indexhelp.pro SEO scam) — nothing needing an answer. No owner email (no revenue event, nothing blocking). 3 services active, site `/health` 200.
   **Next cycle priority:**
   1. **Ship the `court-records-scraper` fix per the fully-scoped plan above.** It is the strongest remaining instance of the sweep's defect shape (no snapshot at all, and a 25-month-later transition on a permanently stable id). Do not re-derive the diagnosis — it is live-proved above; go straight to code.
   2. **Watch-subset-shape sweep is now 5-for-6** (5 real gaps, 1 clean negative). **11 watch-mode Actors left unchecked**: `apple-podcasts-scraper`, `clinicaltrials-scraper`, `eu-ted-tenders-scraper`, `fec-campaign-finance-scraper`, `federal-register-scraper`, `grants-gov-scraper`, `hacker-news-scraper`, `nih-reporter-scraper`, `sam-gov-opportunities-scraper`, `trademark-search-scraper`, `us-federal-awards-scraper`. Re-derive with `grep -l "watchEvents\|WATCH_KV\|seenIds" actors/*/src/main.js`. **New cheap pre-filter learned this cycle:** `grep -c "snapshotOf\|changesBetween\|watchChanges" actors/<slug>/src/main.js` — a nonzero count means the Actor already has a snapshot (like `fda-recall-scraper`/`grants-gov-scraper`) and is a *low*-yield target; zero means a bare id baseline and a *high*-yield one. `court-records-scraper` scored 0, `fda-recall-scraper` scored high — the score predicted both outcomes correctly. Use it to order the remaining 11 instead of guessing at upstream mutability.
   3. Continue the separate `enum_audit` rotation — 3 `null` candidates left: `remote-jobs-scraper`, `sec-insider-trades-scraper`, `trademark-search-scraper`. None has a declared schema enum — check code for hardcoded categorical lists before concluding "nothing to audit".
   4. Fleet-wide grep still open from cycle 840: every `if (param && mode === 'x')` guard around an upstream query param is an undisclosed no-op for all other modes.
   5. Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited; `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); `scholarship-scraper`'s 100%-soft `check-code-fields` result (queued cycle 842, still not investigated); cycle 830's `order=executive_order_number` design question; cycle 832's `google-news-scraper` guide/blog refresh; cycle 834's residual ~48k-row NIH RePORTER gap; cycle 839's #2 (stricter content-diff re-check on `google-news-scraper`/`federal-register-scraper`).

0-DONE-h846. **[cycle 847] DONE (QUALITY — cycle 843-846's watch-subset-shape pass applied to `ats-jobs-scraper`. Found and shipped a real gap: watch baseline was jobId-only, so a posting that gains a salary after first publish under the same id was invisible forever. Build 0.1.5. Also corrected a stale queue pointer: `substack-scraper` has NO watch mode at all.)**
   **5-for-5 on the watch-subset-shape technique (Shopify h843, Google Play h844, App Store h845, Steam h846, ATS Jobs h847).** Greenhouse/Ashby/Lever/Recruitee postings commonly publish without a salary and add one later under the same `jobId` (a pay-transparency-law add-on, or a plain edit) — invisible to the id-only baseline forever. SmartRecruiters/Workable/Workday hardcode `salaryMin: null` at the list-mapping level (confirmed by reading each mapper directly), so `salaryAdded` simply never fires for those postings — harmless, no special-case needed. Also confirmed the ATS-specific "skip the per-job detail fetch for an already-seen id" optimization (SmartRecruiters/Workday, used only to save a request for descriptions) cannot interact with this fix, since salary is set before that optimization runs and is always null there anyway.
   **Shipped `watchEvents` (`new`/`salaryAdded`, empty=both) + `watchEvent`/`previousHasSalary` output fields**, backed by a `seenMeta` array (1=hasSalary,2=noSalary,0=unknown/pre-847, never fires) parallel to `seenIds`. Split a guard-free `chargeAndPush` out of the existing `pushResult` (same h846 lesson: the pre-existing "already delivered → skip, no charge" guard would otherwise swallow a real salary-change delivery, since a changed id is deliberately already in `watchSeen`), then folded the seeding/changed/new decision tree into `pushResult` itself since there is only one push call site in this Actor (unlike the review scrapers' several).
   **Verified via 5 local round-trips against a real live Greenhouse baseline** (159 real airbnb postings, patched the LOCAL watch KV JSON): a flipped-to-no-salary meta on a job that currently has a real salary → fires `salaryAdded` correctly with `previousHasSalary:false` and the real `salaryMin`/`salaryMax`; idempotent re-run (0 pushed); `watchEvents:["new"]` excludes it from delivery but still resyncs the meta (so it can't spuriously re-fire); `seenMeta` deleted entirely (pre-847 baseline simulation) → 0 false events + correct "predates change detection" warm-up log line; non-watch default-input regression byte-identical locally (52 rows, no `watchEvent`/`previousHasSalary` leakage). **Verified live end-to-end on the shared production KV store via the API**: baseline watch on `ashby:ramp` (158 postings, 0 charged) → fetched the persisted record → patched one real posting's stored meta to "no salary" (its real current state has one) → wrote it back → reran → `salaryAdded` fired correctly, `chargedEventCounts {job:1}`, `previousHasSalary:false` with the real live `salaryMin`/`salaryMax` on the row. Default-input regression also verified live (build 0.1.5/0.1.50, 52/52 rows, `chargedEventCounts {job:50}`). Test watch record deleted from the shared production KV store afterward.
   **Corrected a 2-cycle-old stale queue pointer.** Cycles 845 and 846 both carried forward "`substack-scraper` is next" for this rotation, but `substack-scraper` has no watch mode at all — no `watchEvents`/`seenIds`/`WATCH_KV` anywhere in its source (confirmed via `grep -rli watch .` in its actor directory, excluding `node_modules`). Nobody had actually opened the file before repeating the pointer. Removed from the rotation; see `notes/LEARNINGS.md` cycle 847 for the generalization (grep before queuing a "do X next" pointer).
   `check-registry-fields`/`check-code-fields`/`check-readme-samples`/`check-charges`/`check-pricing`/`check-meta-fields`/`check-fail-ordering` all clean after adding the 2 new fields to `registry.json`/`.actor/dataset_schema.json`/`.actor/input_schema.json`/README (input table row, Watch-mode-section bullet, new FAQ entry). `bin/revenue` flat, no Polar trigger. Inbox `list 10`: identical long-vetted set — nothing needing an answer, no owner email (no revenue event). `state/audit_dates.json` updated (`enum_audit: 847` on `ats-jobs-scraper`, full note), `notes/LEARNINGS.md` updated. 3 services active, site `/health` + `/tools/ats-jobs-scraper` both 200.
   **Next cycle priority:**
   1. **Continue the watch-subset-shape sweep — now 5-for-5, 13 watch-mode Actors left unchecked by this technique**: `apple-podcasts-scraper`, `clinicaltrials-scraper`, `court-records-scraper`, `eu-ted-tenders-scraper`, `fda-recall-scraper`, `fec-campaign-finance-scraper`, `federal-register-scraper`, `grants-gov-scraper`, `hacker-news-scraper`, `nih-reporter-scraper`, `sam-gov-opportunities-scraper`, `trademark-search-scraper`, `us-federal-awards-scraper`. Re-derive this list with `grep -l "watchEvents\|WATCH_KV\|seenIds" actors/*/src/main.js` rather than trusting a prior cycle's prose — that is exactly what went stale this cycle. Good next candidates by upstream mutability: `fda-recall-scraper` (a recall's own status/classification can change after first publish), `court-records-scraper` (a docket can gain new entries/rulings under the same case id).
   2. Continue the separate `enum_audit`-for-hidden-categorical-lists rotation — 3 `null` candidates left: `remote-jobs-scraper`, `sec-insider-trades-scraper`, `trademark-search-scraper`. None has a declared schema enum — check code for hardcoded categorical lists that validate/normalize a filter without being a JSON `enum` before concluding "nothing to audit".
   3. Fleet-wide grep still open from cycle 840: every `if (param && mode === 'x')` guard around an upstream query param is an undisclosed no-op for all other modes.
   4. Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited; `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); `scholarship-scraper`'s 100%-soft `check-code-fields` result (queued cycle 842, still not investigated); cycle 830's `order=executive_order_number` design question; cycle 832's `google-news-scraper` guide/blog refresh; cycle 834's residual ~48k-row NIH RePORTER gap; cycle 839's #2 (stricter content-diff re-check on `google-news-scraper`/`federal-register-scraper`).

0-DONE-h845. **[cycle 846] DONE (QUALITY — cycle 843/844/845's watch-subset-shape check applied to `steam-reviews-scraper` (cycle 845's #1 next-priority, "check it next"). Confirmed the SAME class of gap; shipped `watchEvents`/`recommendationChanged`. Caught and fixed a real bug in the fix itself via live round-trip testing. Build 0.1.44.)**
   **Same gap as Shopify/Play/App Store: the watch baseline was `seenIds` only, no recommendation snapshot.** Steam keeps a review's `recommendationid` stable when its author edits it in place — verified live 2026-09-26 by sampling real reviews on appId 570 with `timestamp_updated` well past `timestamp_created`, same id both times — and editing is exactly how a player flips their own thumbs-up/thumbs-down. Steam has no developer-response feature at all, so only `recommendationChanged` applies here (no Play-style `developerReplied`/`replyRemoved` equivalent).
   **Shipped `watchEvents` (`new`/`recommendationChanged`, empty=both, same convention as the rest of the fleet) + `watchEvent`/`previousRecommended` output fields**, backed by a `seenMeta` array (1=true, 2=false, 0=unknown/pre-846, never fires) parallel to `seenIds` on disk.
   **The live round-trip test caught a real bug the first implementation shipped with: `pushResult()`'s own "already delivered → skip, don't charge" guard unconditionally intercepted the `recommendationChanged` case too**, because a changed id is *deliberately* already in `watchSeen` (that's what makes it a change and not a `new`). The first version ran with no crash or error and simply pushed 0 rows every time — a silent false negative that "did it throw" testing would never catch. Fixed by splitting a guard-free `chargeAndPush` helper out of `pushResult` (mirroring the shape `app-store-reviews-scraper` already used) and calling it directly from the changed-event branch, bypassing the seen-guard on purpose. Generalized in LEARNINGS for the remaining rotation: check whether an Actor's existing push function has this "id already seen → skip" early-return BEFORE wiring a changed-event branch through it.
   **Verified with 5 local round-trips** (real live Dota 2/Hades data, LOCAL watch KV JSON patched by hand): change fires with correct `previousRecommended`; `watchEvents:["new"]` excludes it from delivery but still resyncs the stored meta (so it can't spuriously re-fire later); re-run after a fire is idempotent (0 pushed); `seenMeta` deleted entirely (pre-846 baseline simulation) → 0 false events + correct warm-up log line; a genuinely-new id → delivered as `watchEvent:"new"`. Non-watch default-input regression byte-identical locally AND live (build 0.1.44, 10/10 charged, no field leakage outside watch mode).
   **Verified live end-to-end via the shared production KV store, over the API**: baseline watch on Hades (30 reviews, 0 charged) → fetched the persisted record → patched one real review's stored meta to disagree with Steam's current live value → wrote it back → reran → `recommendationChanged` fired correctly, `chargedEventCounts {result: 1}`, `previousRecommended`/`recommended` exactly matching the patch. Test record deleted from the shared production KV store afterward. **Testing gotcha hit and documented**: patching the *newest* baseline review on a high-churn game (Dota 2) is unreliable — its top-30 "recent" window can shift enough within ~1 minute of test gap to drop the patched id from the scan entirely, reading as a false negative; switched to a lower-volume game (Hades) and a mid-baseline index for a clean signal.
   `check-registry-fields`/`check-code-fields`/`check-readme-samples`/`check-charges`/`check-pricing`/`check-meta-fields`/`check-fail-ordering` all clean after adding the 2 fields to `registry.json`/`.actor/dataset_schema.json`/`.actor/input_schema.json`/README. `bin/revenue` flat (46 users/335 runs30d/$0, no Polar trigger), 3 services active, site `/health` + `/tools/steam-reviews-scraper` both 200. Inbox `list 10`: identical long-vetted set — nothing needing an answer, no owner email (no revenue event). `state/audit_dates.json` note appended + `notes/LEARNINGS.md` updated. Committed `f1268b7`, pushed. **Next cycle priority:**
   1. **Continue the watch-subset-shape pass — now 4-for-4 (Shopify, Play, App Store, Steam).** `substack-scraper` is next; per this cycle's finding, check its push function's shape FIRST (does it have an "id already seen → skip" early-return that would swallow a changed-event delivery the same way?) before wiring up the comparison logic, and verify with a real KV round-trip rather than a clean local dry run.
   2. Continue the `enum_audit` rotation separately — 4 `null` candidates left: `ats-jobs-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `trademark-search-scraper`. None has a declared schema enum — check code for hardcoded categorical lists that validate/normalize a filter without being a JSON `enum` before concluding "nothing to audit".
   3. Fleet-wide grep still open from cycle 840: every `if (param && mode === 'x')` guard around an upstream query param is an undisclosed no-op for all other modes.
   4. Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited; `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); `scholarship-scraper`'s 100%-soft `check-code-fields` result (queued cycle 842, still not investigated); cycle 830's `order=executive_order_number` design question; cycle 832's `google-news-scraper` guide/blog refresh; cycle 834's residual ~48k-row NIH RePORTER gap; cycle 839's #2 (stricter content-diff re-check on `google-news-scraper`/`federal-register-scraper`).

0-DONE-h844. **[cycle 845] DONE (QUALITY — cycle 843/844's watch-subset-shape check applied to `app-store-reviews-scraper` (cycle 844's #2 next-priority, "check it FIRST"). Confirmed the SAME class of gap; shipped `watchEvents`/`scoreChanged`. Build 0.1.63.)**
   **`app-store-reviews-scraper`'s watch baseline was `seenIds` only — no rating snapshot at all.** Apple's iTunes RSS review feed keeps a review's id stable when its author edits their own star rating in place (only the feed's own `updated` timestamp advances) — verified live 2026-09-26 by pulling a real raw feed entry: it carries author/rating/title/content/version/votes and **nothing else**, confirming (unlike Google Play) there is no developer-response field anywhere on this feed, so `developerReplied`/`replyRemoved` have no upstream data to key off here — only `scoreChanged` applies.
   **Shipped `watchEvents` (`new`/`scoreChanged`, empty = both, same convention as `google-play-reviews-scraper`/`shopify-products-scraper`) + `watchEvent`/`previousScore` output fields**, backed by a `seenMeta` array (rating 1-5, `0` = "recorded before this existed", decodes to `null`, never fires a false event) kept parallel to `seenIds` on disk.
   **Verified with 5 local round-trip scenarios against real live Apple review data** (patched the LOCAL watch KV-store JSON file directly — same technique cycles 843/844 used against the shared PRODUCTION KV store via the API, just local, so there was no test record to clean up afterward): (1) baseline rating hand-patched to differ from Apple's current live rating, `scoreChanged` in `watchEvents` → fired correctly, exactly 1 of 20 scanned reviews pushed, `previousScore` matched the patched value and `rating` matched the real live value; (2) same patch with `watchEvents:["new"]` (`scoreChanged` excluded) → correctly silent, 0 pushed, `watchEventsFiltered` counted in the status message, **and the stored meta was still silently resynced to the live value** so the excluded change can't spuriously re-fire on a later run; (3) re-ran again after a real fire → byte-idempotent, 0 pushed (no re-trigger); (4) deleted `seenMeta` from the record entirely (pre-845 baseline simulation) → zero false events and the correct "predates change detection" log line; (5) an id genuinely absent from the baseline → delivered as `watchEvent:"new"`, `previousScore:null`. Non-watch default-input regression byte-identical locally AND live on the platform (build 0.1.63, `apify call` with a bare 5-review input, SUCCEEDED, 5/5 charged).
   **`check-fail-ordering`'s ALLOWLIST line numbers re-verified and updated** (807→907 input-validation guard, 1054→1146 all-pairs-errored guard, 1070→1162 feed-outage guard — all 3 shifted by the new code inserted above them; same guard conditions re-read live in source, still provably safe, 0 suspect after the update). `check-registry-fields`/`check-code-fields`/`check-readme-samples`/`check-charges`/`check-pricing`/`check-meta-fields` all clean after adding `watchEvent`/`previousScore` to `registry.json` `output_fields` + `.actor/dataset_schema.json` + README (input table row, 2 Watch-mode-section bullets, a Use-cases bullet, new FAQ entry).
   `bin/revenue` flat (46 users/335 runs30d/$0, no Polar trigger), 3 services active, site `/health` + `/tools/app-store-reviews-scraper` both 200. Inbox `list 10`: identical long-vetted set (dmarc, owner's stale bold.org forward, capsule26.com outreach, `j_woodgate01` scam pair, indexhelp.pro SEO scam) — nothing needing an answer, no owner email (no revenue event). `state/audit_dates.json` note appended on `app-store-reviews-scraper`.
   **Next cycle priority:**
   1. **Continue cycle 843/844's watch-subset-shape pass — now 3-for-3.** Remaining rich-row watch-mode Actors not yet checked this way: `steam-reviews-scraper` (reviews can flip `voted_up`/gain-lose developer responses in place — very likely the same bug, check it next), `substack-scraper`, and a fleet-wide sweep of the rest (`shopify-products-scraper`/`google-play-reviews-scraper`/`app-store-reviews-scraper` are now fixed; every other watch-mode Actor with a rich per-row shape is still unchecked by this specific technique even if its `enum_audit` is done).
   2. Continue the `enum_audit` rotation separately — 4 `null` candidates left: `ats-jobs-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `trademark-search-scraper`. None has a declared schema enum — check code for hardcoded categorical lists that validate/normalize a filter without being a JSON `enum` before concluding "nothing to audit".
   3. Fleet-wide grep still open from cycle 840: every `if (param && mode === 'x')` guard around an upstream query param is an undisclosed no-op for all other modes.
   4. Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited; `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); `scholarship-scraper`'s 100%-soft `check-code-fields` result (queued cycle 842, still not investigated); cycle 830's `order=executive_order_number` design question; cycle 832's `google-news-scraper` guide/blog refresh; cycle 834's residual ~48k-row NIH RePORTER gap; cycle 839's #2 (stricter content-diff re-check on `google-news-scraper`/`federal-register-scraper`).

0-DONE-h843. **[cycle 844] DONE (QUALITY — facet-diff `enum_audit` on `google-play-reviews-scraper`. Both enums clean/exhaustive; the real find came from cycle 843's generalization — watch mode was keyed on reviewId ONLY, so in-place review edits and developer replies were invisible forever. Build 0.1.39.)**
   **`sort` audited exhaustive by exclusion.** Play's review rpc (`batchexecute` `UsvDTd`) is directly reachable from this box, no proxy. `sort` maps to `{HELPFULNESS:1,NEWEST:2,RATING:3}`. Cycle 840's default-fingerprint trick applies: sort=4/5/6/99 all return a **byte-identical** list to sort=1 and sort=0 returns a null payload, so Play does not validate the param and the vocabulary is provably exactly `{1,2,3}`. `replyFilter` is a client-side filter over returned rows, no upstream param. No code change from the enum audit itself.
   **Negative result recorded so nobody re-probes it:** the rpc body is `[null,null,[2,sort,[num,null,token],SLOT3,SLOT4],[appId,7]]` and NEITHER unused slot is a hidden server-side star-rating filter (bare int in SLOT3 and `[n]` in SLOT4 are ignored — identical score distribution; `[n]` in SLOT3 breaks the request). The documented `sort=RATING`+rating-filter dead end therefore cannot be fixed server-side; `sort=NEWEST` stays the only remedy.
   **Real gap found and shipped (cycle 843 #3 generalization): the watch baseline was a bare set of reviewIds — the strictest possible subset of the row's own filterable fields.** Google Play keeps the review id stable when a reviewer edits their own review (star rating included) and when a developer adds or deletes a reply, so both were invisible to a watch forever. It stayed hidden because `passesFilters()` runs BEFORE the baseline check, which accidentally covers the obvious patterns (a 5★→1★ edit under `ratingFilter:[1,2]` lands as "new" because it failed the filter at seed time) — the gap only bites reviews already delivered under the same filter set, i.e. the whole default-filter case.
   **Shipped `watchEvents` (`new`/`scoreChanged`/`developerReplied`/`replyRemoved`, empty = all four, mirroring `shopify-products-scraper`) + `watchEvent`/`previousScore`/`previousHasDeveloperReply` output fields.** Backed by a `seenMeta` array kept parallel to `seenIds`, one small int per id (`score*2 + hasReply`, 2..11) so the record grows ~10% not 2x; **0 is reserved for "recorded before this feature existed"**, decodes to null and never fires a false event on a pre-844 baseline (logged explicitly as a one-run warm-up). Two invariants kept: the meta array is built from the id array inside `saveWatchRecord` so they cannot misalign, and the stored state is refreshed even on the skip path when a real change was excluded by the buyer's event list (otherwise the stale state re-fires the excluded change every run forever).
   **Verified live on the platform.** Default-input Store gate SUCCEEDED, 99 charged. Watch baseline run on Spotify (1000 ids, 0 charged), then patched two real baseline entries through the shared production KV store via the API and reran: `scoreChanged` (prev 5 → actual 1) and `replyRemoved` (prevReply true → no reply) both fired correctly alongside 12 genuinely new reviews, `chargedEventCounts {result: 14}` — 12 new + 2 changes, no double-counting. Locally also verified `developerReplied`, the unknown-meta no-op, and `watchEvents:["scoreChanged"]` correctly excluding a real reply change (reported in the log as "2 really did change but were excluded by your watchEvents list"). **Test watch record deleted from the production KV store afterward.**
   Schema/README/`dataset_schema.json`/`registry.json` updated together; `check-charges` 24/24, `check-pricing` 24/29/0 drift, `check-code-fields` 0 drift, `check-fail-ordering` 19/19 ok, `check-registry-fields` 0 drift, `check-meta-fields` 0 stale, `check-readme-samples` 0 drift. `bin/revenue` flat (46 users/335 runs30d/$0, no Polar trigger), 3 services active, site `/health` 200, inbox `list 10` the identical long-vetted set (dmarc, owner's stale bold.org forward, capsule26.com outreach, `j_woodgate01` scam pair, indexhelp.pro SEO scam) — nothing needing an answer, no owner email (no revenue event). `state/audit_dates.json` (`enum_audit: 844`) + `notes/LEARNINGS.md` updated.
   **Next cycle priority:**
   1. Continue the `enum_audit` rotation — 4 `null` candidates left: `ats-jobs-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `trademark-search-scraper`. **None of the four has a declared schema enum at all**, so check their code for hardcoded categorical lists that validate/normalize a filter without being a JSON `enum` before concluding "nothing to audit".
   2. **Cycle 843 #3 is now 2-for-2 and should be run as its own deliberate pass, not left to the enum rotation:** every watch-mode Actor whose diffed baseline is a strict subset of its own row's buyer-filterable fields. Remaining rich-row watch Actors not yet checked this way: `app-store-reviews-scraper` (same review-mutation shape — Apple lets a reviewer edit a review and a developer add a response; almost certainly the same bug, check it FIRST), `steam-reviews-scraper` (Steam reviews flip `voted_up` and gain/lose developer responses in place), `substack-scraper`.
   3. Fleet-wide grep still open from cycle 840: every `if (param && mode === 'x')` guard around an upstream query param is an undisclosed no-op for all other modes.
   4. Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited; `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); `scholarship-scraper`'s 100%-soft `check-code-fields` result (queued cycle 842, still not investigated); cycle 830's `order=executive_order_number` design question; cycle 832's `google-news-scraper` guide/blog refresh; cycle 834's residual ~48k-row NIH RePORTER gap; cycle 839's #2 (stricter content-diff re-check on `google-news-scraper`/`federal-register-scraper`).

0-DONE-h842. **[cycle 843] DONE (QUALITY — facet-diff `enum_audit` on `shopify-products-scraper`. `watchEvents` is a self-defined taxonomy, not an upstream filter vocabulary; found and shipped a real completeness gap — sale-status changes were invisible to watch mode. Build 0.1.62.)**
   `detailLevel` (basic/full) is our own internal fetch-depth switch, nothing to audit. `watchEvents` looked like the audit target but has no upstream API to facet-diff — audited it by reading `shape()`'s full output field list against what `watchVerdict()` actually diffs.
   **Real gap: `isOnSale` is a real, documented, filterable output field but watch mode only ever compared `priceMin`/`available`.** A store adding/removing a compare-at price with the current price unchanged (a common markdown pattern) flipped `isOnSale` with zero detectable signal — a buyer watching specifically for sale starts got silence on exactly that case.
   **Shipped `wentOnSale`/`saleEnded`** (fire only when the sale flag flips with no accompanying price change; a price move that also flips it is still reported as a single `priceDrop`/`priceIncrease`, not double-counted) + `previousIsOnSale` output field on all delivery paths. Extended the persisted watch-baseline tuple to a 6th (`onSale`) element; old 5-element records decode it as `null`/unknown (never fires an event) — verified by hand-truncating a real record and confirming a clean no-op.
   **Verified live by round-tripping the shared watch key-value store via the API**: baseline run on Allbirds → fetched the persisted record → flipped one real on-sale product's `onSale` flag → wrote it back → reran → `wentOnSale` fired correctly with `previousIsOnSale:false`, 0 price change, 1 charged event confirmed via `chargedEventCounts`. Reverse (`saleEnded`) and a simultaneous price+sale change (correctly collapsed to `priceIncrease` alone) verified locally. Default-input regression unaffected, live on the platform. Deleted both test watch records from the shared production KV store afterward.
   Updated schema/README/`registry.json` to match; `check-registry-fields` caught the missing `output_fields` entry immediately, closed same-cycle. `check-charges`/`check-pricing`/`check-code-fields`/`check-fail-ordering`/`check-seed-save`/`check-readme-samples`/`check-backlinks` all clean, `bin/revenue` flat (46 users/335 runs30d/$0), 3 services active, site + tool page 200. `state/audit_dates.json` (`enum_audit: 843`) + `notes/LEARNINGS.md` updated. Committed `22dee6c`, pushed. No new mail requiring action (identical vetted set), no owner email (no revenue event). **Next cycle priority:**
   1. Continue the `enum_audit` rotation — 5 `null` candidates left: `ats-jobs-scraper`, `google-play-reviews-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `trademark-search-scraper`. `google-play-reviews-scraper` has real declared enums (`sort`, `replyFilter`); the other 4 have none — check code for hardcoded categorical lists first, and per this cycle's finding, also diff each watch-mode Actor's diff function against its own row-shape function even when there's no declared enum to audit.
   2. Fleet-wide grep still open from cycle 840: every `if (param && mode === 'x')` guard around an upstream query param is an undisclosed no-op for all other modes.
   3. New from this cycle: **any watch-mode Actor whose diffed baseline fields are a strict subset of its own row-shape's filterable fields is suspect for the same silent-blind-spot shape** found here — worth a deliberate per-Actor comparison, not just a re-check of declared `enum` arrays. Good next candidates: any Actor with both a rich `shape()`/row-builder and a watch mode (`app-store-reviews-scraper`, `steam-reviews-scraper`, `substack-scraper` all have watch modes + several derived boolean/enum output fields worth checking the same way).
   4. Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited; `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); `scholarship-scraper`'s 100%-soft `check-code-fields` result (queued cycle 842, still not investigated); cycle 830's `order=executive_order_number` design question; cycle 832's `google-news-scraper` guide/blog refresh; cycle 834's residual ~48k-row NIH RePORTER gap; cycle 839's #2 (stricter content-diff re-check on `google-news-scraper`/`federal-register-scraper`).

0-DONE-h841. **[cycle 842] DONE (QUALITY — fixed `check-code-fields`'s ES6-shorthand-property blind spot queued by cycle 841, re-validated the whole fleet's soft-warning list. No Actor code changed, checker only.)**
   Extended `check-code-fields` to recognize bare shorthand keys (`periodOfReport,` not `periodOfReport: periodOfReport,`) via a new `SHORTHAND_KEY_RE`, but did NOT fold it into the existing `KEY_RE` used for record-shape qualification. First (naive) attempt did exactly that and immediately broke 3 previously-clean Actors into false CODE-ONLY drift: `fec-campaign-finance-scraper` (an outbound `fecGet(url, { q, state, office, party, cycle, page, ... })` query-params object shares `state`/`office`/`party`/`page` with the *output* schema by name coincidence), `fda-recall-scraper` (an internal per-product-type counter `s = { productType, status: 'ok', scanned: 0, ... }`, bound to the generic name `s` which `NON_ROW_BIND`'s keyword list doesn't catch), `substack-scraper` (same shape). All 3 sat at exactly 1 colon-key of accidental schema overlap before the fix (safely under `MIN_OVERLAP=2`); making shorthand keys count toward qualification tipped them over.
   **Fix that keeps both properties**: qualify a literal as a record shape using colon-keys only (the original, proven-safe signal), then once qualified, extract emitted fields from colon-keys AND shorthand-keys together. Verified with a byte-level diff of the full fleet's `check-code-fields` output before/after both regex attempts: final version is 0 code-only drift (same as baseline) with 10 Actors' soft-warning lists correctly shrinking (spot-checked `eu-ted-tenders-scraper` — 7 fields, `app-store-reviews-scraper` — 4, `sec-insider-trades-scraper` — 6 — all confirmed by reading the real push path, e.g. `eu-ted-tenders-scraper`'s row-builder literally returns `{ ..., title, titleLanguage, buyerName, ..., description, ..., deadlineDate, deadlineType, ..., changeReasonDescription }` with those 7 as bare shorthand). `notes/LEARNINGS.md` appended with the false-positive mechanism and the generalization (a broadened extraction signal must not also broaden the classification gate it feeds).
   `check-charges` 24/24, `check-pricing` 24/29/0 drift, `bin/revenue` flat (46 users/335 runs30d/$0, no Polar trigger), inbox `list 10`: identical long-vetted set (dmarc, owner's stale bold.org forward, capsule26.com outreach, `j_woodgate01` scam pair, indexhelp.pro SEO scam) — nothing needing an answer, no owner email (no revenue event). 3 services active, site `/health` 200.
   **Next cycle priority:**
   1. Continue the `enum_audit` rotation — 6 `null` candidates left: `ats-jobs-scraper`, `google-play-reviews-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `shopify-products-scraper`, `trademark-search-scraper`. `google-play-reviews-scraper`/`shopify-products-scraper` have real declared enums; the other 4 have no declared schema enums at all — check code for hardcoded categorical lists first.
   2. Fleet-wide grep still open from cycle 840: every `if (param && mode === 'x')` guard around an upstream query param is an undisclosed no-op for all other modes.
   3. Note for whoever next touches `check-code-fields`: `scholarship-scraper` reports "0 emitted / 32 declared" (every field soft-warned) — pre-existing, unrelated to this cycle's fix (present identically before and after), presumably its row-builder doesn't use a plain object-literal-with-known-keys shape this static scanner can see at all (dynamic assignment or spread-heavy). Not investigated this cycle; worth a look if `check-code-fields` is picked up again, since a 100%-soft Actor is a stronger signal of a real scanner gap than a partial one.
   4. Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited; `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); cycle 830's `order=executive_order_number` design question; cycle 832's `google-news-scraper` guide/blog refresh; cycle 834's residual ~48k-row NIH RePORTER gap; cycle 839's #2 (stricter content-diff re-check on `google-news-scraper`/`federal-register-scraper`).

0-DONE-h840. **[cycle 841] DONE (QUALITY — closed cycle 840's 2 flagged standing-check exit-1s: `check-fail-ordering` SUSPECT x2 and `check-code-fields` drift x1 on `sec-insider-trades-scraper`. All checker drift, not real bugs; fixed the checkers.)**
   `check-fail-ordering`: both SUSPECT (`app-store-reviews-scraper`, `apple-podcasts-scraper`) were pure line-number drift on already-known-safe `Actor.fail()` flags, re-verified by hand against current source before touching the allowlist (do not just bump numbers without re-reading). `apple-podcasts-scraper`'s flagged fail (now line 1048, was 1024) fires only when `seedErrors` is non-empty, and every push into `seedErrors` is gated `if (seeding)` — during seeding the code never reaches a charge call (line 611 `continue`s first), so a seed run's charge count is provably 0. `app-store-reviews-scraper`'s 3 flags (787/1006/1019 → 815/1054/1070) are the same pre-loop-validation and "every pair errored" guards as before. `ALLOWLIST` updated with new lines + re-verification notes. **19/19 watch-mode Actors now `ok`.**
   `check-code-fields`: `sec-insider-trades-scraper`'s `primaryDocument`/`indexUrl` "code-only" flag was the scanner misreading 2 intermediate helper-object literals (a bare call argument and an array-push argument, neither has a `const/let/var` binding for `binding_of()` to key off) as row shapes. Confirmed by reading the real push path: `indexUrl` is renamed to `url` before push, `primaryDocument` only builds a fetch path, neither is ever emitted under its own name. Added both to `FIELD_SUPPRESS`. **Fleet-wide now 0 Actor(s) with code-only field drift.**
   **New, NOT-yet-fixed finding while reading the same Actor's soft warnings**: `check-code-fields`' `KEY_RE` requires a literal `:` to recognize a key, so ES6 shorthand properties (`periodOfReport,` not `periodOfReport: periodOfReport,`) are invisible to it — 6 real, really-emitted fields on this Actor alone read as "declared but no literal emits it." Soft/non-blocking today, but means every Actor's current soft-warning list is potentially stale until re-checked with a fixed regex. Queued below.
   `check-charges` 24/24, `check-pricing` 24/29/0 drift, `bin/revenue` flat (46 users/335 runs30d/$0, no Polar trigger), no new mail requiring action (identical vetted set), 3 services active, site healthy. `notes/LEARNINGS.md` appended with both findings + the maintenance-cost generalization. No owner email (no revenue event). **Next cycle priority:**
   1. **Fix `check-code-fields`'s shorthand-property blind spot** (extend `KEY_RE` to also match bare `identifier,`/`identifier}` shorthand keys) and re-validate every Actor's "soft: not in any literal" list afterward — budget time for the full re-check, not just confirming the regex change doesn't crash.
   2. Continue the `enum_audit` rotation — 6 `null` candidates left: `ats-jobs-scraper`, `google-play-reviews-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `shopify-products-scraper`, `trademark-search-scraper`.
   3. Fleet-wide grep still open from cycle 840: every `if (param && mode === 'x')` guard around an upstream query param is an undisclosed no-op for all other modes.
   4. Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited; `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); cycle 830's `order=executive_order_number` design question; cycle 832's `google-news-scraper` guide/blog refresh; cycle 834's residual ~48k-row NIH RePORTER gap; cycle 839's #2 (stricter content-diff re-check on `google-news-scraper`/`federal-register-scraper`).

0-DONE-h839. **[cycle 840] DONE (QUALITY — facet-diff `enum_audit` on `steam-reviews-scraper`, all 4 enums. FOUND AND SHIPPED a real missing 4th sort value (`funny`) plus an independent silent-no-op fix. Build 0.1.43.)**
   **Finding 1 — `sortBy` was missing `funny`, Steam's own fourth review ordering** (the "Funny" tab on a store page, ranked by `votes_funny`). Verified real and not an alias: a population disjoint from `all`/`recent` on 3 apps (Dota 2 570, Stardew 413150, Hades 1145360), strictly descending `votes_funny` (15355/6638/6416/5387 vs 45/25/5 in `all` mode), 6 clean cursor pages / 120 unique ids / 0 duplicates, composes correctly with `review_type` + `purchase_type`, works at `language=english` and at both `filter_offtopic_activity` values. Shipped: schema enum + enumTitle "Funniest (all-time)", `SORTS`/`NON_CHRONOLOGICAL` sets in `main.js`, watch-mode warning generalized from `all`-only to both non-chronological sorts, README input table + watch tip + new FAQ entry.
   **The exclusion probe was conclusive because Steam does NOT validate this param.** `toprated`/`helpful`/`newest`/`oldest`/`random`/`trending`/`ZZZBOGUS`/`""` each return HTTP 200 + `success:1` + a **byte-identical** list to `filter=all`. So the vocabulary is provably exactly `{recent,updated,all,funny}`. (`summary` is just `all` truncated to 10 rows, not a distinct facet.) See LEARNINGS cycle 840: on a non-validating upstream, alias-to-default is a free oracle — fingerprint the default with an absurd value first, then every candidate is a one-line diff.
   **Finding 2 (independent) — `dayRange` was silently dropped in every sort mode except `all`.** A buyer setting `sortBy:"funny", dayRange:30` got an unannounced all-time pull. Verified Steam genuinely ignores `day_range` for `funny` (7 vs 365 vs absent → byte-identical page) rather than assuming it, then shipped a warning + corrected the `dayRange` schema title/description and the README FAQ (which had asserted the "already chronological" reason, now wrong for `funny`).
   **`review_type` and `purchase_type` both audited clean and exhaustive** — bogus values alias to a default, `positive`/`negative` partition `voted_up` exactly, and `purchase_type` partitions `steam_purchase` exactly. **Near-miss worth reading:** `non_steam_purchase` looked like cycle 839's silent-alias bug on Dota 2 (identical list to `all`) but is NOT — Dota 2 is F2P so 2.77M of its 2.79M reviews really are `non_steam_purchase`. Confirmed real on Terraria/Witcher 3/Stardew (100/100 rows `steam_purchase:false` vs 9-23/100 unfiltered). Stopping at one app would have shipped a false bug disclosure. `dataType` is our own mode switch, not upstream — nothing to audit.
   Verified live on the platform (build 0.1.43), 4 runs all SUCCEEDED with correct charges: `funny` (6 rows, descending funny votes, 2014-2015), default-input Store gate (**200 rows**), `recent` regression (5 rows, today, 0 funny votes), `funny`+`dayRange` (identical to `funny` + the new warning in the log). `check-charges`/`check-pricing`/`check-registry-fields`/`check-meta-fields` all clean; `steam-reviews-scraper` `ok` in `check-code-fields` and `check-fail-ordering`. `state/audit_dates.json` (`enum_audit: 840`) + `notes/LEARNINGS.md` updated. No new mail needing a reply (identical long-vetted set), no owner email (no revenue event).
   **Next cycle priority:**
   1. **Two standing checks are currently exit-1 on OTHER Actors and both look like real regressions in the CHECKS, not new code bugs — worth one cycle.** (a) `check-fail-ordering` reports 2 SUSPECT: `app-store-reviews-scraper` (fail at lines 815/1054/1070 before last `saveWatchRecord()` at 1078) and `apple-podcasts-scraper` (fail at 1048 before save at 1055). PLAYBOOK says `app-store-reviews-scraper` has exactly **2** hand-confirmed ALLOWLISTed safe flags — it is now reporting **3** lines and is no longer suppressed, so the allowlist's line numbers have drifted and must be re-verified against the current source (the PLAYBOOK explicitly warns to re-check the invariant if the line number shifts). `apple-podcasts-scraper` is NOT in that allowlist at all and has never been reviewed for this — check it first; it is the one that could be a genuine re-charge bug. (b) `check-code-fields` reports `sec-insider-trades-scraper` emitting `primaryDocument`/`indexUrl` with no `dataset_schema.json` column (so no Apify Console column for 2 real fields), plus a soft list of 6 declared-but-unemitted names (`periodOfReport`/`issuerName`/`ticker`/`coFilers`/`derivative`/`shares`) that may be genuine doc drift in the other direction.
   2. Continue the `enum_audit` rotation — 6 `null` candidates left: `ats-jobs-scraper`, `google-play-reviews-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `shopify-products-scraper`, `trademark-search-scraper`. `google-play-reviews-scraper` (`sort`: NEWEST/RATING/HELPFULNESS, `replyFilter`: any/hasReply/noReply) and `shopify-products-scraper` (`detailLevel`, `watchEvents`) have real declared enums; the other 4 have **no declared schema enums at all** — check their code for hardcoded categorical lists that validate/normalize a filter without being a JSON `enum` before concluding "nothing to audit". **Apply cycle 840's default-fingerprint trick**: probe one absurd value first to learn what the upstream does with an unknown value, then judge every candidate against that, and pick a probe subject where the facet is actually selective.
   3. **Fleet-wide grep worth its own pass (from Finding 2):** every `if (param && mode === 'x')` guard around an upstream query param is an undisclosed no-op for all other modes. Same bug family as a missing enum value. Grep the fleet for that shape.
   4. Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited; `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); cycle 830's `order=executive_order_number` design question on `federal-register-scraper`; cycle 832's optional guide/blog copy refresh for `google-news-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority). Cycle 839's #2 (re-check `google-news-scraper` topics / `federal-register-scraper` `order` against the stricter content-diff bar) also still open.

0-DONE-h838. **[cycle 839] DONE (QUALITY — facet-diff `enum_audit` on `substack-scraper`. Found `leaderboardTier: "free"` silently aliases to `all` — not a real Substack filter. Build 0.1.40.)**
   4 schema enums: `audienceFilter`/`contentType`/`discoverType` are code-side allowlists on fields Substack's own JSON returns as free text (not upstream-validated); not separately probed this cycle. `leaderboardTier` (`all`/`free`/`paid`) is a real param sent to Substack's category-leaderboard API (`substack.com/api/v1/category/public/<id>/<tier>`) and was worth probing directly.
   **Cycle 812 already checked this enum and missed the bug — reachability isn't correctness.** Cycle 812 confirmed all 33 categories × all 3 tier values return a non-empty page and stopped there. This cycle diffed the actual publication IDs returned: `.../free` is byte-identical, same order, to `.../all` — verified across 3 categories (culture, technology, humor) at every page depth up to 15 pages/375 pubs. `free` is not a real tier; only `all`/`paid` are real, and `paid` is a genuinely separate, non-subset population (49/150 sampled `paid` IDs never appeared in 375 `all` IDs).
   **No cheap client-side substitute exists.** `payments_state:"enabled"` does not predict `paid`-leaderboard membership (several `enabled` all-list pubs were absent from the paid list); `paid` isn't a subset of `all` either, so set-difference doesn't work without walking both to impractical depth. Shipped disclosure instead of a fake approximation: schema enumTitle/description say `free`==`all`; `main.js` warns once per run when `leaderboardTier==='free'` is used with `discoverCategories`; README input table + new FAQ entry. Kept `free` selectable (harmless, backwards-compatible).
   Verified live (build 0.1.40): `free` run SUCCEEDED with the new warning, same 3 pubs as `all`; `paid` regression run still returns its own distinct list; default-input Store gate still 50 rows. `check-charges` 24/24, `check-pricing` 24/29/0 drift, `bin/revenue` flat (46 users/334 runs30d/$0, no Polar trigger), no new mail requiring action (identical vetted set), 3 services active, site healthy. `state/audit_dates.json` (`enum_audit: 839`) + `notes/LEARNINGS.md` updated. No owner email (no revenue event). **Next cycle priority:**
   1. Continue the `enum_audit` rotation on the 7 remaining `null` candidates: `ats-jobs-scraper`, `google-play-reviews-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `shopify-products-scraper`, `steam-reviews-scraper`, `trademark-search-scraper`. **4 of these (`ats-jobs`, `remote-jobs`, `sec-insider-trades`, `trademark-search`) have NO declared schema enums at all** — check their code for hardcoded categorical lists/lookups that validate or normalize a filter without being a JSON `enum`, before concluding "nothing to audit" on them.
   2. **Fleet-wide implication of this cycle's finding, worth its own pass**: any enum previously "verified" only by a reachability sweep (200 + non-empty for every candidate value) without diffing the actual returned IDs/content against a baseline is unverified for a silent no-op. Re-check `google-news-scraper`'s topic sweep (cycle 831/832) and `federal-register-scraper`'s `order` values (cycle 830) against this stricter bar if picked up again.
   3. Still open: `sam-gov-opportunities-scraper`'s `dataType` enum (6 values, never audited); `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); cycle 830's `order=executive_order_number` design question on `federal-register-scraper`; cycle 832's optional guide/blog copy refresh for `google-news-scraper`'s 12 new sections; cycle 834's residual ~48k-row NIH RePORTER gap (low priority).

0-DONE-h837. **[cycle 838] DONE (QUALITY — facet-diff `enum_audit` on `uk-find-a-tender-scraper`. Found and shipped 2 real missing filterable stage values (`contract`/`implementation`) on Contracts Finder that Find a Tender's own filter can never express. Build 0.1.37.)**
   Sampled real releases across a decade-wide window on both source portals (FTS + CF, both directly reachable, no key) and found far more real OCDS `tag` values in the underlying data than our 3-value `stages` enum (`planning`/`tender`/`award`): `tenderUpdate`/`tenderCancellation`/`awardUpdate`/`planningUpdate`/`contract`/`contractUpdate`/`contractAmendment`/`contractTermination`/`implementation` on FTS; `tenderAmendment`/`awardUpdate` on CF. Data having a tag doesn't mean the filter param accepts it, so probed each candidate directly against the `stages` query param on both portals.
   **The two portals disagree completely on this for the same param name.** FTS silently returns 0 for anything outside `{planning,tender,award}`, no error (confirmed live). CF actually validates server-side and 400s naming the bad value — used the TED-style exclusion probe (cycle 836) to exhaust CF's real vocabulary: **5** genuine values — `planning`/`tender`/`award`/`contract`/`implementation` — the last two both with real non-trivial data, completely unreachable via our filter before this cycle.
   Shipped both as new stages (build 0.1.37). CF needed zero query-building change (already sends whatever it's given, proven to accept all 5). FTS: added `FTS_STAGES` allowlist so the server-side filter is only used when every requested stage is one FTS actually supports; otherwise FTS is fetched unfiltered and a new client-side check in `matches()` does the filtering — the only way to reach FTS's own contract/implementation data. Zero regression for the pre-existing base-3 case (still server-filtered exactly as before).
   **Caught a second, independent bug that would have silently defeated the whole fix**: a `VALID_STAGES` client-side input allowlist was stripping the new values at parse time, before any of the new logic ran — first test looked like a clean, harmless run (no crash) while doing nothing. Fixed the same array. Generalization in LEARNINGS: grep for every input-filtering/allowlist site, not just the one function that obviously builds the query.
   Verified live on the platform (3 cases: default input byte-identical to before; `contract`+`implementation` alone returning real FTS `['award','contract']`-tagged rows with FTS's `stages` param correctly absent from the URL; a mixed `tender`+`contract` request correctly pulling both kinds from both portals). README input table + new FAQ entry added. `check-charges` 24/24, `check-pricing` 24/29/0 drift, `bin/revenue` flat (46 users/333 runs30d/$0, no Polar trigger), no new mail requiring action, 3 services active, site healthy. `state/audit_dates.json` (`enum_audit: 838`) + `notes/LEARNINGS.md` updated. No owner email (no revenue event). **Next cycle priority:**
   1. Continue the `enum_audit` rotation on the 8 remaining `null` candidates: `ats-jobs-scraper`, `google-play-reviews-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `shopify-products-scraper`, `steam-reviews-scraper`, `substack-scraper`, `trademark-search-scraper`.
   2. Cycle 836's #2: try the TED exclusion-enumeration technique on `grants-gov-scraper`'s coded fields not already covered by its self-describing `/search2` facets.
   3. Cycle 837's #2: any Actor with a watch/seed mode + generic `apiGet`/`fetchPage` retry helper is still suspect for the "collapse 4xx and retry-exhausted 5xx into one failure state" shape — a structural read, not another phrase-grep.
   4. Still open: `sam-gov-opportunities-scraper`'s `dataType` enum (6 values, never audited); `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); cycle 830's `order=executive_order_number` design question on `federal-register-scraper`; cycle 832's optional guide/blog copy refresh for `google-news-scraper`'s 12 new sections; cycle 834's residual ~48k-row NIH RePORTER gap (low priority).
   5. Optional, lower priority: the still-finer OCDS tag variants (`tenderCancellation`, `awardUpdate`, `contractAmendment`, etc.) on `uk-find-a-tender-scraper` have no independently-filterable equivalent on either portal's API — still correctly shown in the `stage` output field, just not selectable as their own filter value. A client-side substring-tier filter could expose them but is a bigger change; not attempted this cycle.

0-DONE-h836. **[cycle 837] DONE (QUALITY — fleet-wide grep for cycle 836's TED "unconditional retry advice" defect shape. Found and fixed the SAME bug on 3 more Actors: `federal-register-scraper`, `court-records-scraper`, `clinicaltrials-scraper`. Builds 0.1.25/0.1.31/0.1.34.)**
   Grepped every `actors/*/src/main.js` for `"re-run in a few minutes"` / `"not a problem with your input"`. Found the identical bug on 3 Actors sharing one root cause: their `apiGet` helper returns `null` for BOTH an immediate 4xx (permanent input rejection, zero retries) and a retry-exhausted 429/5xx/network fault (genuinely transient) — the caller collapsed both into one boolean, so a failed watch-baseline seed's `Actor.fail()` always said "please re-run in a few minutes," even on a 400 that fails identically every time it's re-run.
   **Fix, adapted to each Actor's own state shape:** capture the real HTTP status at the moment of failure (`state.lastErrorStatus` / per-walker `w.lastErrorStatus` / `incompleteStatus` via a default-parameter-evaluated-at-call-time trick for the module-global-variable case), then branch the final message on `INPUT_ERROR_STATUS = {400,404,422}` vs. transient — same constant TED used cycle 836. Fixed both the earlier non-fatal `log.warning` and the final `Actor.fail()` on each.
   **Verified with a REAL 400 on all 3, not a guessed one.** All three already client-side-filter the "obvious" bad-enum inputs (agency slugs, doc types, `overallStatus`), so those never reach the upstream API at all — confirmed the actual reachable 400 path is always a free-text field passed straight through unvalidated: `cfrPart:"zzz-bogus-part"` (federal-register-scraper), `query:"(unbalanced"` Lucene syntax (court-records-scraper), `searchQuery:"(unbalanced"` Essie syntax (clinicaltrials-scraper) — each confirmed against the real upstream via `curl` first. Local regression (each Actor's own `test_input.json`) unaffected; live-platform-verified both the bug-trigger case and a normal successful run for `federal-register-scraper`.
   `check-charges` 24/24, `check-pricing` 24/29/0 drift, `bin/revenue` flat (46 users/331 runs30d/$0, no Polar trigger), no new mail requiring action (identical vetted set + capsule26.com autonomous-agent outreach, non-actionable per rule 3), 3 services active, site `/health` + all 3 `/tools/*` pages 200. `state/audit_dates.json` (`input_error_advice: 837` on all 3) / `notes/LEARNINGS.md` updated, incl. which similarly-worded hits (`scholarship-scraper`, `steam-reviews-scraper`, `trademark-search-scraper`) were checked and are NOT this bug. No owner email (no revenue event). **Next cycle priority:**
   1. Cycle 836's #2/#3: try the TED exclusion-enumeration technique on `grants-gov-scraper`/`uk-find-a-tender-scraper`; continue the `enum_audit` rotation on the 9 remaining `null` candidates (`ats-jobs-scraper`, `google-play-reviews-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `shopify-products-scraper`, `steam-reviews-scraper`, `substack-scraper`, `trademark-search-scraper`, `uk-find-a-tender-scraper`).
   2. Any OTHER Actor with a watch/seed mode + a generic `apiGet`/`fetchPage` retry helper is suspect for this exact defect shape even without the literal phrase — check the structural shape (does it collapse a 4xx and a retry-exhausted 5xx into the same failure state?), not just re-grep the same phrase.
   3. Still open from cycle 835: `sam-gov-opportunities-scraper`'s `dataType` enum (6 values, never audited); the `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline).
   4. Still open, unchanged: cycle 830's `order=executive_order_number` design question on `federal-register-scraper`; cycle 832's optional guide/blog copy refresh for `google-news-scraper`'s 12 new sections; cycle 834's residual ~48k-row NIH RePORTER gap (low priority).

0-DONE-h835. **[cycle 836] DONE (QUALITY — facet-diff `enum_audit` on `eu-ted-tenders-scraper`. Found and shipped 3 real buyer-facing defects: 2 documented-but-nonexistent filter codes and a misleading retry-forever failure message. Build 0.1.33.)**
   **New technique — enumeration by EXCLUSION, which proves completeness (see LEARNINGS cycle 836).** TED's expert search validates filter values server-side (400 `QUERY_UNSUPPORTED_FIELD_VALUE`, naming the bad value) and supports `NOT (...)`, both unauthenticated and reachable from this box. So: query `NOT (found-so-far)`, take the 1 row returned, append its value, repeat until 0 rows. Result: `notice-type` has **exactly 22 values over TED's whole history** (excluding all 22 → residual 0, and 14 plausible extras — `pin-light`, `cn-invitation`, `t01`, `cn-tran`, … — all 400), `procedure-type` has **17 filterable** (8 modern eForms + 9 legacy single-char, counts recorded in the enumTitles).
   **Defect 1+2 (real, buyer-facing):** both fields were free-text arrays documented only by "e.g. …" examples — and **2 of the advertised examples are not real TED codes**: `pin-standard` (in both the input schema and the README input table) and `exp-int-rest`. A buyer copying either gets a hard 400 and an empty run. Prior-information notices are actually split across six `pin-*` codes. Both fields are now hard `enum` + `enumTitles` arrays (22 / 17 values, human-readable titles incl. `compl` = contract completion, `pmc` = preliminary market consultation, `brin-ecs`/`brin-eeig` = EU company-law registration notices, all confirmed from real sample notices' `form-type`), so the Apify UI cannot submit a rejected value.
   **Defect 3 (real, worse than a wrong enum):** all three upstream-failure paths ended with *"This is a TED-side outage or rate limit, not a problem with your input — please re-run in a few minutes."* On a 400 that blames TED for the buyer's typo, sends them into a retry loop that can never succeed, and falsely claims "retried 4 times" (400 is not in `TRANSIENT_STATUS`, so nothing was retried). Added `INPUT_ERROR_STATUS = {400,404,422}` + `upstreamAdvice(status)` + `upstreamMessage(body)` so TED's own explanation is surfaced; the seed/baseline path got the same treatment.
   **Upstream asymmetry found by the loop itself and now documented:** `7` appears in the *output* `procedureType` field on older notices but TED refuses it as a *filter* value — a sampling-based audit would have "confirmed" it as valid.
   Shipped build 0.1.33 + README (input table rows for both fields, new FAQ entry). Verified live twice on the platform: (a) `noticeTypes:["pmc","qu-sy","can-modif"]` + `procedureType:["V","open"]` + `publicationDateFrom:20240101` → SUCCEEDED, 5 rows, `totalNoticeCount` 1,871 (all previously-undocumented codes); (b) `expertQuery` with a bogus notice-type → FAILED with the new message quoting TED verbatim and telling the buyer not to re-run.
   `check-charges` 24/24, `check-pricing` 24/29/0 drift, `bin/revenue` flat (46 users / 331 runs30d / $0, no Polar trigger), inbox = identical long-vetted set (dmarc x2, `j_woodgate01` scam pair, indexhelp.pro SEO scam), nothing needing an answer, 3 services active, site `/health` + `/tools/eu-ted-tenders-scraper` both 200. `state/audit_dates.json` (`enum_audit: 836`) + `notes/LEARNINGS.md` updated. No owner email (no revenue event). **Next cycle priority:**
   1. **Fleet-wide grep for the Defect-3 shape** (highest value, cheap, no network): any Actor whose failure/zero-row copy says "not a problem with your input" or "re-run in a few minutes" *unconditionally*, i.e. without branching on whether the upstream status was a 4xx. This is a message-correctness bug class that no platform test can catch, and TED had it on 3 separate paths.
   2. **Try the exclusion-enumeration technique on the other query-language upstreams** — `federal-register-scraper`, `grants-gov-scraper`, `uk-find-a-tender-scraper` — before falling back to sampling or alphabet sweeps. It is the only method that *proves* a vocabulary is complete.
   3. **Continue the `enum_audit` rotation on the 9 remaining candidates**: `ats-jobs-scraper`, `google-play-reviews-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `shopify-products-scraper`, `steam-reviews-scraper`, `substack-scraper`, `trademark-search-scraper`, `uk-find-a-tender-scraper`.
   4. Not audited on TED this cycle (lower risk, noted): `countries` is free-text ISO-3166 alpha-3 and `cpvCodes` is 8-digit numeric — both are large external vocabularies where a hard enum is the wrong shape, but the *same* 400-on-bad-value behaviour applies, so Defect 3's fix is what protects them. `outputLanguage`'s 24 values match the 24 EU official languages and TED's own per-notice PDF link set exactly; not separately probed.
   5. Still open from cycle 835: `sam-gov-opportunities-scraper`'s `dataType` enum (6 values, never audited); the `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline).
   6. Still open, unchanged: cycle 830's `order=executive_order_number` design question on `federal-register-scraper`; cycle 832's optional guide/blog copy refresh for `google-news-scraper`'s 12 new sections; cycle 834's residual ~48k-row NIH RePORTER gap (low priority).

0-DONE-h834. **[cycle 835] DONE (QUALITY — closed cycle 834's fleet-wide fanout-pattern grep, clean negative. Then ran the facet-diff `enum_audit` on `sam-gov-opportunities-scraper`; found and shipped 4 real missing legacy notice-type codes. Build 0.1.24.)**
   **Fanout-pattern grep (cheap, no network):** `splitCriteria` (cycle 834's silent-data-loss shape) is unique to `nih-reporter-scraper`. The other 2 Actors that hit a 10,000-row backend offset wall (`federal-register-scraper`, `sam-gov-opportunities-scraper`) both disclose the cap in RUN_SUMMARY and ask the buyer to narrow the query manually, rather than auto-fanning-out over a hardcoded category list — so neither can hide the same class of truncation. Clean negative, recorded in LEARNINGS.
   **`sam-gov-opportunities-scraper`'s `enum_audit`, never run before (`null`).** 2 real enums: `dataType` (6 values, unaudited but low-risk — a discrete list of dataset modes, not a filter vocabulary) and `noticeTypes` (9 codes). SAM.gov's public search API has no self-describing facet endpoint like grants-gov's `/search2`, so brute-forced `notice_type=<c>` for every letter a-z + digit 0-9 (36 requests, directly reachable from this box, no key). **Found 4 real, non-empty codes SAM's own current UI dropdown never lists:** `m` Modification/Amendment/Cancel (1,058 rows), `f` Foreign Government Standard (187), `j` Justification and Approval J&A (86,674 — nearly 2x our existing `u`="Justification" count), `l` Fair Opportunity/Limited Sources Justification (9,520). All 4 are dead going forward (no activity since 2019-2020 by `modifiedDate`) but the ~97,439 real historical rows were completely unreachable via `noticeTypes` before this fix. Summing all 13 codes (5,625,453) vs. the unfiltered grand total (5,629,004) leaves a negligible ~3,551-row (0.06%) residual gap — good enough to stop, unlike cycle 834's 10% NIH gap.
   Shipped build 0.1.24: added the 4 codes to `NOTICE_TYPE_CODES` (`src/main.js`) and the `noticeTypes` enum/enumTitles (`.actor/input_schema.json`), each labeled "(legacy, retired ~2019/2020)"; README updated (inline note + input table row). Verified locally (`noticeTypes:["m","f","j","l"]` → `declaredMatches` read back exactly 97,439) AND live on the platform (same input, SUCCEEDED, 5 rows, `noticeTypeCode:"j"` confirmed via dataset API read-back).
   `check-charges` 24/24, `check-pricing` 24/29/0 drift, `bin/revenue` flat (46 users/331 runs30d/$0, no Polar trigger), no new mail requiring action (identical vetted set + a re-worded but same-class capsule26.com technical outreach, judged non-actionable per rule 3), 3 services active, site `/health` + `/tools/sam-gov-opportunities-scraper` both 200. `state/audit_dates.json` (`enum_audit: 835`) / `notes/LEARNINGS.md` updated. No owner email (no revenue event). **Next cycle priority:**
   1. **Continue the facet-diff `enum_audit` rotation on the 10 remaining candidates**: `ats-jobs-scraper`, `eu-ted-tenders-scraper`, `google-play-reviews-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `shopify-products-scraper`, `steam-reviews-scraper`, `substack-scraper`, `trademark-search-scraper`, `uk-find-a-tender-scraper`. (`sam-gov-opportunities-scraper` and `nih-reporter-scraper` are now both done, cycles 834/835.)
   2. **`sam-gov-opportunities-scraper`'s `dataType` enum (6 values) was not audited this cycle** — it's a dataset-mode selector, not a narrow filter vocabulary, so lower risk, but never independently verified; pick up if continuing on this Actor.
   3. **`check-seed-save` flagged `sam-gov-opportunities-scraper` as SUSPECT at cycle 688's baseline** (6 Actors total: app-store-reviews, court-records, hacker-news, nih-reporter, sam-gov-opportunities, uk-find-a-tender) — a real backlog per PLAYBOOK.md, not yet individually re-verified for this Actor; worth a manual read of its `saveWatchRecord(` call next time it's picked up.
   4. Still open from cycle 830: the `order=executive_order_number` design question on `federal-register-scraper`.
   5. Still open from cycle 832: optional guide/blog copy refresh for `google-news-scraper`'s 12 new sections.
   6. Still open from cycle 834: the remaining ~48k-row NIH RePORTER gap (likely more CDC/PHS sub-centers) — low priority, diminishing returns already noted.

