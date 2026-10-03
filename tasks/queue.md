NEXT-CYCLE (1155): per rotation (1152 QUALITY -> 1153 GROWTH/BUILD -> 1154 QUALITY -> 1155 **GROWTH/BUILD**).
   **The court-records watch item (item 1 below) is DUE 2026-10-04 — do it in the first cycle on or after
   that date, AHEAD of the audit rotation** (`parseforge/harris-county-court-records-scraper` start fee
   $0.005 -> $0.02 plus a new $0.005 "case-details" event; re-verify live and update
   `court-records-scraper`'s README). Otherwise resume the fleet-oldest `competitor_audit` rotation at
   **`federal-register-scraper` (1124, now sole fleet-oldest)**, then `remote-jobs-scraper` (1126),
   `grants-gov-scraper` (1128), `scholarship-scraper` (1129).
   **DONE at 1154 (QUALITY slot): fleet-oldest `competitor_audit` on `substack-scraper`** (1123 -> 1154).
   `niche-size` one-word sweep ("substack", safe base term): 220 seen / 159 matched. All 6 named rivals
   re-verified live, 0 meaningful drift (two sub-1%/sub-10% deltas on `sourabhbgp` u30d and `brilliant_gum`
   total users left unedited per standing tolerance). **Two real inaccuracies fixed, no retraction:**
   `automation-lab/substack-scraper`'s tier floor was wrongly attributed to "Gold and above" when live
   Gold is $0.0012 and only Diamond is $0.00056 (our OWN tiers plateau at Gold, which is presumably where
   the mix-up came from — theirs don't); `fatihtahta/substack-scraper` was called "flat $0.00199 at every
   tier" when live Free is actually $0.0025, only Bronze+ is the flat $0.00199. Both reworded; same
   competitive conclusion (both still dearer than us everywhere) either way. **One new rival disclosed
   for completeness:** `cryptosignals/substack-scraper` (72u, 6u30d, never named) at flat $0.005/result, no
   start fee — dearer than us at every tier. Three easyapi sibling listings (leaderboard-only/
   publications-only/Notes-only, all $0.00299+$0.09 start) checked and deliberately left unnamed — scope
   judgment (single-purpose products, dearer than our equivalent mode wherever we offer the same feature),
   not an oversight. **Flagged but NOT acted on (see LEARNINGS cycle 1154 and item 12 below):**
   `brilliant_gum/substack-insights-scraper`'s live `pricingInfos` marks its own per-entity charge event
   `isOneTimeEvent: true` (same flag as its start fee) — if Apify enforces that literally, its real price
   is a flat ~$0.025/run, not "$0.015/entity" as published, which would make it far cheaper than our README
   currently states ("7x-19x our rate"). Confirming needs a paid test run (no `BUDGET.md` line for probing
   a competitor's Actor) or Apify docs on the flag's runtime behavior — neither done this cycle; see
   LEARNINGS cycle 1154 for the full writeup, revisit if `substack-scraper` comes up again. Build 0.1.49 verified
   live via the build's own `readme` field. All 6 standing checks clean: `check-competitor-claims` 315/0
   stale + 74/0 undated, `check-comparison-breadth` 23/0 narrow, `check-price-superiority` 380/100/0
   undisclosed, `check-pricing` 24/29/0, `check-charges` 24/24, `check-disclosure` 0 missing.
   `audit_dates.json` -> 1154. $0 spent (read-only Store/Actor API reads, 1 README-only build, no Actor
   runs). **New fleet-oldest `competitor_audit` is `federal-register-scraper` (1124).**
   **ALSO NOTE for 1154+: two `jungle_synthesizer` TED listings have a pricing change scheduled for
   2026-10-04** (`eu-national-procurement-portals-scraper` and `ted-eu-procurement-full-scraper`, both
   currently $0.10 start + $0.001/record). Read live on 2026-10-03 the future `pricingInfos` entry was
   byte-identical to the current one (same $0.10 start, same $0.001 primary, `reasonForChange: null`),
   so no README change is expected — but re-read it on/after 2026-10-04 while doing the court-records
   item, since both handles are named in `eu-ted-tenders-scraper`'s README.
   **DONE at 1153 (GROWTH/BUILD slot): fleet-oldest `competitor_audit` on `app-store-reviews-scraper`**
   (1122 -> 1153). This README was already thorough (last touched 1122, verified live 2026-10-02) so this
   audit came back largely clean rather than a retraction. `niche-size` 11-term sweep: 399 seen / 169
   matched. All 9 previously-named rivals (thewolves 2371u, theagents 818u, easyapi 545u, johnvc 484u,
   sourabhbgp 141u, jdtpnjtp 163u, brilliant_gum 160u, code-node-tools 158u, scriptbase 59u) re-verified
   live, **zero price drift**. **One real inaccuracy fixed:** `benthepythondev/appstore-reviews-scraper`
   (152u) was described as "$0.002/review flat" — live `pricingInfos` shows it's actually tiered $0.002
   (FREE) down to $0.0014 (Diamond); reworded, still 14x-20x our rate, no competitive-position change.
   **Three new dearer rivals disclosed for completeness** (none undercut us): `fatihtahta/app-store-
   global-reviews-scraper` (59u, tied with scriptbase, $0.0004/review, 4x ours), `powerai/app-store-
   reviews-scraper-ppr` (34u, 0 new/30d, tiered $0.00499->$0.00199 + a $0.09 start fee), `nexgendata/
   ios-app-store-reviews-scraper` (32u, flat $0.1/review + $0.005 start, ~1,000x our rate, dearest found
   in this niche). Build 0.1.74 verified live via the build's own `readme` field. All 6 standing checks
   clean: `check-competitor-claims` 314/0 stale + 74/0 undated, `check-comparison-breadth` 23/0 narrow,
   `check-price-superiority` 379/100/0 undisclosed, `check-pricing` 24/29/0, `check-charges` 24/24,
   `check-disclosure` 0 missing. `audit_dates.json` -> 1153. $0 spent (read-only Store/Actor API reads,
   1 README-only build, no Actor runs). Committed and pushed (`b54343c`). **New fleet-oldest
   `competitor_audit` is `substack-scraper` (1123).**
   -11. **DONE at 1152 (QUALITY slot): fleet-oldest `competitor_audit` on `eu-ted-tenders-scraper`** (1121 -> 1152).
   **Biggest claim retraction of the rotation so far, and it lands one day after a price cut made on the
   bad data.** Cycle 1151's auto `niche-size` sweep of this niche returned 158 listings / 91 matches; a
   hand-curated 12-term sweep returned **364 listings / 228 matches**, and **all 186 TED/EU-specific ones
   were price-checked live**. Root cause, exactly the item-4 class: the base phrase `"eu ted tenders"` is
   THREE contiguous words that essentially never appear verbatim in a listing's copy, so the niche was
   matching on its two synonyms (`ted europa`, `public procurement`) and nothing else — a listing titled
   "EU Tenders Scraper" whose description says "contract notices from TED" matched neither.
   **Finding: we are NOT the cheapest TED Actor — ~15 listings undercut $0.0015/notice**, most never named.
   Cheaper at EVERY run size: `bikram07/eu-tenders-feed` (1u, Apify **FREE** model, $0/row — the cycle-1104
   lesson again), `westerly_breaker/ted-tender-monitor` (2u, $0.00001/row, ~150x below us),
   `highbrow_qualification_z7w/eu-tenders-monitor` (2u, $0.0001/row, DACH-only scope),
   `getascraper/eu-ted-tender-monitor` (2u, $0.00053 -> $0.0004), `thriftykiwi/eu-ted-tenders-scraper`
   (2u, flat $0.001, **no start fee, no minimum**). Cheaper past a few rows: `vhsgreed/eu-ted-tenders-api-fresh`
   (~2 rows), `guyweitzman/eu-tenders-scraper` and `rod_analytics/ted-tenders` (~3), `soilair/ted-eu-tenders-api`
   + `rigelbytes/eu-tenders-scraper` + `koalastuff/eu-ted-tender-monitor` (~1), `8tp/eu-ted-tender-lot-award-collector`
   (~5), `deriverge/eu-tenders-scraper` (~14, $0.02 run minimum), `logiover/global-public-tenders-scraper`
   (8u, ~14 rows on Gold+), `jungle_synthesizer/eu-national-procurement-portals-scraper` (past ~200 rows),
   `steadydata/eu-tenders` (2u, no start fee, beats us from Gold up). **Published conclusion is now
   "we are not the cheapest EU TED Actor at any run size and we do not intend to compete on price here"**
   — differentiation rests on the documented CPV-subtree behaviour, the complete 22-notice-type/17-procedure-type
   dropdowns, measured fill rates, deadline filtering, watch mode and the duplicate-row charge guard.
   **Explicit decision recorded: do NOT cut this Actor's price again.** The 2026-10-02 $0.003 -> $0.0015 cut
   was made against the 7-rival view; the real distribution has rivals at $0 and $0.00001/row, so no price wins here.
   **Also newly named (not price threats):** `parseforge/ted-eu-procurement-scraper` (15u, the niche's
   5th-biggest listing, never named before, $0.006 -> $0.0055 = ~4x us) and `lofomachines/public-tenders-scraper`
   (74u, 5 new/30d — the **biggest** listing in the broadened sweep, but a 7-country aggregator, not a TED
   reader, and dearer at every tier), plus 14 checked-and-dearer handles (alwaysprimedev, nerdrx, scrapepilot,
   parseforge x2, ikoles, straightforward_hydra, alex_r_ai, siccscha, pappy-dev, euroscrape, mtellez23,
   fuyuki0, nexgendata, omarchydev). All 9 previously-named rivals (foxlabs, dltik, artificially, adobeflex,
   scrapers_lat, memo23, jungle_synthesizer, publicmoney, maximedupre) re-verified live with **0 price drift**.
   **Structural finding worth carrying: this niche is being flooded.** Every undercutter found set its current
   price between 2026-07-06 and 2026-09-29 and has 1-2 users — new cheap entrants are arriving faster than any
   of them gains customers. Expect the same shape in other government-API niches.
   **Tooling improved (verified by re-run):** promoted `eu-ted-tenders-scraper` into `bin/niche-size`
   `TERM_VARIANTS` (12 hand-read terms) AND widened its `MATCH_SYNONYMS` (+`tenders electronic daily`,
   `eu tender`, `european tender`, `eu procurement`, `european procurement`, `ted eu`, `cpv`): 91 -> 228
   matched (119 `--strict`). `federal-register-scraper` re-run as a regression check, unchanged at 90.
   Build **0.1.49** verified live via the build's own `readme` field (all new handles + both retraction
   sentences present; 0.1.48 was the first push, 0.1.49 added `lofomachines` after the widened re-run
   surfaced it). **Incidental fix on an unrelated Actor:** `shopify-products-scraper`'s
   `apivault_labs/shopify-product-scraper` 8 -> 10 users, build 0.1.71 verified live.
   All 6 standing checks clean: `check-competitor-claims` **311**/0 stale + 73/0 undated,
   `check-comparison-breadth` 23/0 narrow, `check-price-superiority` **376**/100/0 undisclosed,
   `check-pricing` 24/29/0, `check-charges` 24/24, `check-disclosure` 0 missing. `audit_dates.json` -> 1152.
   $0 spent (read-only Store/Actor API reads, 3 README-only builds, no Actor runs). Services verified:
   3 systemd units active, `/health` + `/tools/eu-ted-tenders-scraper` + `/pricing` all 200 before and after.
   Inbox unchanged (same 10 spam/backscatter/vendor-pitch items as 1140-1151) — nothing actionable, no reply
   owed, no owner email (revenue flat at $0). **New fleet-oldest `competitor_audit` is
   `app-store-reviews-scraper` (1122).**
   **DONE at 1151 (GROWTH/BUILD slot): fleet-oldest `competitor_audit` on `google-news-scraper`** (1118 -> 1151).
   `niche-size` auto sweep ("google news", 11 queries) surfaced 372 listings, 214 matching. Headline find:
   **`epctex/google-news-scraper` (599 users, 885 builds, 8 reviews/5 stars, 25 bookmarks — bigger than
   both `automation-lab` and `crawlerbros`, already-named undercutters, and never named before) was
   automatically migrated to Apify's FREE pricing model on 2026-10-02 (Apify's rental-sunset
   auto-migration, not a deliberate price cut)** — $0/result at any volume, undercutting this Actor at
   every tier. Its input schema is materially narrower (no topic/section codes, no excludeWords/
   siteFilter/excludeSites, no full-article-text extraction, no ticker extraction, no leaked-date-window
   protection) but it does resolve publisher URLs. Flagged for re-check next audit since an auto-migrated
   FREE price could change if the owner sets their own tiers. Also disclosed 3 more checked-but-not-a-
   threat listings: `solidcode/google-news-scraper` (121u) advertises "$0.9/1K" but that excludes URL
   resolution — resolving (the equivalent of our default `decodeUrls`) doubles its price to above ours at
   every tier; `george.the.developer/google-news-monitor` (144u, 21 new in 30d — fastest-growing listing
   found in this niche) brands itself "real-time alerts" but is a flat $0.003/article Actor, pricier than
   us at every tier, different marketing not different tech; `data_xplorer/google-news-scraper` (142u, a
   second, smaller listing from the same vendor as the already-named 2,156-user `-fast` one) adds a
   $0.005/GB start fee that makes it strictly dearer than us at every tier including the ones where its
   sibling ties us. All previously-named rivals (easyapi, data_xplorer-fast, automation-lab, crawlerbros,
   scrapestorm, memo23) re-verified live with 0 price drift. Build 0.1.57 verified live via the build's
   own `readme` field (all 4 new handles + the auto-migration sentence present). All 6 standing checks
   clean: `check-competitor-claims` 282/0 stale + 71/0 undated, `check-comparison-breadth` 23/0 narrow,
   `check-price-superiority` 344/87/0 undisclosed, `check-pricing` 24/29/0, `check-charges` 24/24,
   `check-disclosure` 0 missing. `audit_dates.json` -> 1151. $0 spent (read-only Store/Actor API reads,
   1 README-only build, no Actor runs). Services verified: 3 systemd units active, `/health` +
   `/tools/google-news-scraper` + `/pricing` all 200 before and after. Inbox unchanged (same 10
   spam/backscatter/vendor-pitch items as 1140-1150) — nothing actionable, no reply owed, no owner email
   (revenue flat at $0). **New fleet-oldest `competitor_audit` is `eu-ted-tenders-scraper` (1121).**
   **DONE at 1150 (QUALITY slot): fleet-oldest `competitor_audit` on `hacker-news-scraper`** (1116 -> 1150).
   11-query niche-size sweep ("hacker news", 253 matches) found 5 never-named live rivals. Headline:
   `ryanclinton/hackernews-search` (131u, 26 new in 30d, 31-input-field schema — the most feature-rich
   rival in the niche: author-influence score, GitHub freshness/maturity classifier, sentiment/trend/
   compare heuristics, and automatic date-bucketed splitting past Algolia's 1,000-hit ceiling — a real
   gap vs our own FAQ's manual-slicing workaround) but also the dearest priced rival found ($0.005/item
   Free -> $0.0009 Platinum/Diamond, 9x-25x our rate) — disclosed in both Pricing and "What we do not
   claim". Also disclosed `logiover/hacker-news-who-is-hiring-scraper` (60u, narrower+pricier) and
   checked-but-not-named `mrbridge/latest-news-mcp-server` (108u), `miccho27/trends-aggregator` (63u,
   both multi-source aggregators bundling HN, different product shape) and `nexgendata/hacker-news-
   scraper` (51u, aggregate analytics output, not per-item rows). All 5 previously-named rivals
   re-verified with 0 price drift. Build 0.1.57 verified live via the build's own `readme` field. All
   standing checks clean: `check-competitor-claims` 278/0 stale + 70/0 undated, `check-comparison-
   breadth` 23/0 narrow, `check-price-superiority` 340/85/0 undisclosed, `check-pricing` 24/29/0,
   `check-charges` 24/24. `audit_dates.json` -> 1150. $0 spent. **New fleet-oldest `competitor_audit`
   is `google-news-scraper` (1118).**
   **DONE at 1149 (GROWTH/BUILD slot): fleet-oldest `competitor_audit` on `steam-reviews-scraper`**
   (1114 -> 1149). 4-term Store sweep ("steam reviews", "steam game reviews", "steam player reviews",
   "steam api scraper"). All 5 previously-named rivals re-verified live with **0 price drift**:
   `automation-lab` (78->81u, same per-row price + $0.003 start fee, input schema re-checked against
   its live build and confirmed unchanged since 2026-09-02 — no feature drift despite the user growth),
   `memo23` (18->19u, still 100% joined in the last 30 days, $0.005 start + flat $0.001/review, 8-property
   schema confirmed unchanged against its latest build despite a same-day version bump), `easyapi` (60u),
   `logiover` (54u), `danek` (52u) all byte-identical on price and user count. **Disclosed one genuinely-
   missed rival with real traction**: `shahidirfan/steam-reviews-scraper` (14 users, never named before)
   charges a flat $0.00099/review + $0.0005 start — pricier than this Actor's $0.000575-$0.00014 tiered
   rate at every plan, no search-by-name/keyword/playtime/`games`-mode/watch/webhook. Checked and named
   three smaller listings for completeness, none a threat: `scrapestorm/steam-reviews-scraper---cheap`
   (8u, ironically $0.00299/review — over 5x our rate despite the name), `crawlerbros/steam-review-scraper`
   (6u, $0.003->$0.002 tiered + $0.005 start), `powerai/steam-reviews-scraper` (4u, $0.00499/review +
   a **$0.09** start fee, the dearest start fee found in this niche). **No claim retraction needed this
   cycle** — unlike most recent audits in this rotation, the README's "we are the cheapest in the niche"
   claim survived the widened sweep intact; every new rival found is dearer. Build 0.1.56 verified live
   via the build's own `readme` field (all 4 new handles + updated user counts present). All standing
   checks clean: `check-competitor-claims` 274/0 stale + 68/0 undated, `check-comparison-breadth` 23/0
   narrow, `check-price-superiority` 335/85/0 undisclosed, `check-pricing` 24/29/0, `check-charges` 24/24.
   `audit_dates.json` updated (`steam-reviews-scraper` -> 1149). $0 spent (read-only Store/Actor API reads,
   1 README-only build, no Actor runs). Services/site verified: 3 systemd units active, `/health` +
   `/tools/steam-reviews-scraper` + `/pricing` all 200. Inbox unchanged (same 10 spam/backscatter/vendor-
   pitch items as 1140-1148) — nothing actionable, no reply owed, no owner email (revenue flat at $0).
   **New fleet-oldest `competitor_audit` is `hacker-news-scraper` (1116).**
   -10b. **DONE at 1148 (QUALITY slot): fleet-oldest `competitor_audit` on `fda-recall-scraper`** (1114 -> 1148).
   Swept **10 terms instead of the single "fda recall" term** cycle 1114 used: 288 distinct listings
   (285 mentioning FDA or recalls) against the 20-result read 1114 made, and priced **29 plausibly
   head-on rivals live**. All 7 previously-named rivals re-verified live with **0 price drift**
   (benthepythondev 11u $0.05->$0.035 + $0.00005 start; scrapers_lat $0.008->$0.006154 + details
   $0.009231->$0.007385, still no start fee; bikram07 FREE; maximedupre $0.00001; copious_atoll
   $0.001+$0.00005; ryanclinton/fda-food-recall-monitor $0.002+$0.00005; inexhaustible_glass
   $0.005+$0.005). **Two published claims retracted, both caused by sweep DEPTH rather than drift:**
   (1) "a fresh Store sweep of 20 listings found no new entrant with meaningful traction" was false —
   `nexgendata/us-government-records-api` (9u), `logiover/fda-data-scraper` (8u, titled "openFDA
   Recalls & Events", head-on and never named), `gabrielaxy/product-recall-aggregator` (6u),
   `constant_quadruped/fda-catalyst-alerts` (6u, **3 new in 30d = fastest-growing in the niche**) and
   `martc03/us-safety-recalls-mcp` (4u) each have MORE users than any of the five 3-user rivals the
   README does name; (2) "three genuine undercutters, all food-only" was false — **four rivals
   undercut us on all three recall types, our exact scope**: `gabrielaxy/product-recall-aggregator`
   (FDA+CPSC+NHTSA), `martc03/us-safety-recalls-mcp` (MCP over FDA+NHTSA+CFPB) and
   `constant_quadruped/fda-catalyst-alerts` are all on Apify's **FREE** model ($0/row — the cycle-1104
   lesson for the 5th+ time), and `martc03/fda-recalls` (2u) is the single closest product match in the
   niche (openFDA drug/food/device enforcement, filter by type/class/date) at **$0.00001/result +
   $0.00005 start, ~350x below our $0.0035 free-plan rate**. Also newly disclosed: 2 partial
   undercutters (`carranza-tech/fda-recall-monitor` $0.003 no start fee — under our Free rate, over our
   Gold+ $0.0024; `tictechid/vanzi-us-recall-intelligence` $0.005 Free -> **$0.0015 Gold+**, beats us
   there from row 1), 4 cheaper-but-scope-narrow (`ryanclinton/fda-device-recalls` 6u and
   `pink_comic/fda-device-recall-enforcement` device-only at $0.002; `cloud9_ai/openfda-drug-scraper`
   and `pink_comic/openfda-drug-adverse-events-recalls` drug-only at $0.002), 1 adjacent cheap
   (`fiery_dream/healthcare-intel` 9u, $0.00001+start, but sells trials/approvals/news not enforcement
   reports), and 8 dearer-for-completeness (logiover, maydit $0.004->$0.0024 + a start fee we do not
   charge, ponderable_hydrometer, johnatan029, nexgendata, datapilot $0.003/row but a $0.035 Free start
   fee so dearer below ~70 rows/run, zentrafoundry/compliance-risk-tool, parseforge/fda-warning-letters).
   **The README's bottom line is now "we are not the cheapest FDA recall Actor at any scope"** —
   differentiation rests on `includePressReleases`, documented `riskScore`, `watchChanges`/`_watchPrevious`,
   the 50k-row ceiling and `declaredMatches`/`declaredMatchesIsFloor`, not price.
   **Also softened a negative superlative before it broke (item-5 class, repeat #13):** the README said
   "a 2026-09-20 audit found EVERY FDA-recall Actor on the Store ... reads only the same lagging openFDA
   enforcement API". That audit was a 20-result sweep; with 285 candidate listings now visible the
   quantifier cannot be supported, so it is scoped to "every listing we have checked" with the limit
   stated inline. Nothing about `includePressReleases` itself changed — no rival checked has it.
   **Tooling improved (both verified by re-run):** promoted `fda-recall-scraper` into `bin/niche-size`
   `TERM_VARIANTS` (10 hand-read terms) AND added the missing `MATCH_SYNONYMS` entry
   (`openfda`/`fda enforcement`/`recall`) — the two-contiguous-word base phrase "fda recall" was
   matching 47 listings and **structurally could not see `logiover/fda-data-scraper` or any of the
   multi-agency recall rivals**; now 270 (237 `--strict`). `federal-register-scraper` re-run as a
   regression check, unchanged. Build **0.1.42** verified live via the build's own `readme` field (all
   9 new handles + both retraction sentences present). All standing checks clean after the edit:
   `check-competitor-claims` **270**/0 stale + 67/0 undated (claim count 260 -> 270 confirms the new
   paragraphs are visible to the freshness checker), `check-comparison-breadth` 23/0 narrow,
   `check-price-superiority` **331**/84/0 undisclosed. `audit_dates.json` -> 1148. $0 spent (read-only
   Store/Actor API reads, 1 README-only build, no Actor runs). Services: 3 systemd units active,
   `/health` + `/tools/fda-recall-scraper` + `/pricing` all 200. Inbox unchanged (same 10
   spam/backscatter/vendor-pitch items as 1140-1147) — nothing actionable, no reply owed, no owner
   email (revenue flat at $0).
   **`check-competitor-claims` `live_users()` transient has now RECURRED (2nd sighting, 1145 -> 1148)**:
   it flagged `eu-ted-tenders-scraper/README.md:141` `maximedupre/eu-funding-tenders-scraper` as "gone
   from the Store". Two direct `GET /v2/acts/...` reads returned 200 / isPublic=true / **18 users,
   exactly the number the README publishes**, and a second checker run came back 270/**0** stale. Still
   a flake, not a stale claim — but it is no longer a one-off, so **if it recurs a 3rd time, add a
   retry-once around `live_users()`'s "gone from the Store" verdict** rather than re-confirming by hand
   each cycle. Do NOT edit that README on this signal alone.
   -9. **DONE at 1147 (GROWTH/BUILD slot)** — record as written that cycle:
   **DONE at 1147 (GROWTH/BUILD slot): fleet-oldest `competitor_audit` on `apple-podcasts-scraper`**
   (1113 -> 1147, 34 cycles stale). `niche-size` auto sweep ("apple podcasts", 11 queries) surfaced
   97 matches and caught the README's own biggest-listing superlative going stale again: it had said
   (as recently as 1113) that `coder_zoro/apple-podcast-episodes-scraper` (66u) was "the niche's
   actual biggest listing...never been named until now" — false, `ryanclinton/podcast-directory-
   scraper` (182u, 26 u30d, fastest-growing in the niche) and `automation-lab/podcast-scraper` (117u,
   17 u30d) are both bigger. **Same claim-fragility class as item 5 below, repeat #12+ of the
   negative/exclusive-superlative lesson.** `ryanclinton` is a different-angle product (Spotify+Apple
   search plus host-email/contact extraction) priced 50x ours ($0.05/podcast + $0.00005 start) — named
   for the record, not a price threat. **`automation-lab/podcast-scraper` IS a real, previously
   undisclosed undercutter**: FREE-plan $0.005 start + $0.00115/podcast + $0.000575/episode (tiered
   down to $0.00028/$0.00014 on Diamond) vs our flat $0.001/row, no start fee — crosses over past
   ~12 episodes/run on Free (sooner on higher tiers), past ~7-9 podcasts/run on Platinum/Diamond; it
   has no reviews/charts/publisher lookup/RSS-full-archive/watch mode. Checked and deliberately left
   unnamed: `benthepythondev/podcast-intelligence-aggregator` (61u, 0 u30d — stale, no growth — and
   21-30x dearer at $0.03-0.021/result tiered, not a threat) and `parseforge/podchaser-scraper` /
   `hgservices/podcast-transcriber` (different source platform / transcription-focused, not head-on
   rivals — a scope judgment, not an oversight). All 4 previously-named rivals (sourabhbgp, logiover,
   coder_zoro, taroyamada) re-verified live, **0 price drift**. Build 0.1.60 verified live via the
   build's own `readme` field (all 4 new handles + "Verified live 2026-10-02" present on every edited
   paragraph — the first push (0.1.59) tripped `check-competitor-claims`'s UNDATED check on my own two
   new paragraphs, fixed and re-pushed, same gotcha item 6 already documents). **Incidental fix caught
   by the same checker run, unrelated Actor:** `uk-find-a-tender-scraper`'s `parseforge/uk-contracts-
   finder-scraper` (5->6u) and `parseforge/uk-gov-tenders-scraper` (3->4u), both first-time 1-user
   flaps (not the repeat-flap pattern item 9 tracks) — edited normally, build 0.1.50 verified live.
   All standing checks clean after both edits: `check-competitor-claims` 260/0 stale + 67/0 undated,
   `check-comparison-breadth` 23/0 narrow, `check-price-superiority` 315/76/0 undisclosed. `audit_dates.json`
   updated (`apple-podcasts-scraper` -> 1147). $0 spent (read-only API/Store reads, 2 README-only
   builds, no Actor runs). Site/services verified: 3 systemd units active, `/health`/`/tools/apple-
   podcasts-scraper`/`/pricing` all 200. **New fleet-oldest `competitor_audit` is `fda-recall-scraper`
   / `steam-reviews-scraper` (1114, tied).**
   Next cycle (1148, QUALITY slot per rotation) should resume the fleet-oldest `competitor_audit`
   rotation at `fda-recall-scraper` / `steam-reviews-scraper` (1114) using the same method (Store
   sweep + live `pricingInfos` re-read on every named rival, FREE-model rivals as $0, watch for
   misleadingly-named "cheapest"/"low-cost" listings). **The court-records watch item (item 1 below)
   comes due 2026-10-04 — 2 days away. Do it in the first cycle on or after that date, ahead of the
   audit rotation.**
   -10. **DONE at 1146 (QUALITY slot): fleet-oldest `competitor_audit` on `google-play-reviews-scraper`**
   (1112 -> 1146, 34 cycles stale). 2-term Store sweep ("google play reviews", "play store reviews")
   priced 33 live listings beyond the 11 already named. Re-verified all 11 named rivals with **0 price
   drift** (incl. confirming `code-node-tools/google-play-reviews-scraper`'s 2026-08-08 price cut was
   fully REVERTED 2026-08-22 back to the README's published numbers -- never actually stale). 5 small
   user-count deltas (thewolves +18, theagents +4, neatrat +15, apihq +2, easyapi +24) all inside the
   10% tolerance, left unedited. **Found and disclosed two genuine new undercutters:**
   `x.com/google-playstore-review-scraper` (17u, flat $0.00001/review + $0.00005 start -- ~90% below
   our $0.0001, cheapest in the niche) and `delectable_incubator/google-play-store-reviews-scraper-
   low-cost` (2u, flat $0.00009/review + $0.00005 start). Rewrote the "what we do not claim" paragraph
   to rank all three undercutters (x.com, apihq, delectable_incubator) cheapest-first instead of
   naming apihq alone. Also disclosed `fetchcraftlabs/playstore-reviews-scraper` (133u) as a genuine
   narrow VOLUME crossover (its $0.05 flat start fee makes it dearer than us below ~1,700 reviews/run
   even at its cheapest GOLD+ tier, cheaper above that) and `scrapesmith/...` (18u, ties our per-review
   rate but a $0.01 start fee makes it strictly dearer at any real volume). Checked two misleadingly-
   named listings (`scrapestorm/...---cheapest`, bundled App Store+Google Play scrapers `brilliant_gum`
   /`code-node-tools/app-reviews-scraper`) and found no real threat -- all dearer than us, deliberately
   left unnamed to avoid bloating the pricing section with non-threats. Build 0.1.53 verified live via
   the build's own `readme` field (all 4 new handles present). All 6 standing checks clean (258/0
   claims, 67/0 undated, 24/29/0 pricing, 24/24 charges, 23/0 breadth, 313/75/0 price-superiority, 65/0
   disclosure). `audit_dates.json` updated (`google-play-reviews-scraper` -> 1146). $0 spent
   (read-only Store/Actor API reads, 1 README-only build, no Actor runs). **New fleet-oldest
   `competitor_audit` is `apple-podcasts-scraper` (1113).**
   Next cycle (1147, GROWTH/BUILD slot per rotation) should resume the fleet-oldest `competitor_audit`
   rotation at `apple-podcasts-scraper` (1113) if no open build item is queued, using the same method
   (Store sweep + live `pricingInfos` re-read on every named rival, FREE-model rivals as $0, watch for
   misleadingly-named "cheapest"/"low-cost" listings that may or may not actually be cheap). **The
   court-records watch item (item 1 below) comes due 2026-10-04 -- 2 days away. Do it in the first
   cycle on or after that date, ahead of the audit rotation.**
   -8. **DONE at 1145 (GROWTH/BUILD slot): fleet-oldest `competitor_audit` on `sec-insider-trades-scraper`**
   (1112 -> 1145; the tied twin `google-play-reviews-scraper` is still at 1112 and is now fleet-oldest
   -- do it next). 2-term Store sweep ("sec form 4", "insider trading") priced 20 live listings beyond
   the 4 already named. Re-verified all 4 named rivals (ryanclinton 52u, scrapemint 13u, scrapers_lat,
   parseforge) live with **0 price drift**. Found and disclosed `jweninger16/insider-trading-monitor`
   (3 users, `pricingInfos` is `null` = Apify FREE model, $0/row at any volume -- the cycle-1104 lesson
   repeating, genuinely cheaper than us at any run size) plus `entrepreneurial_lens_ehi/openinsider-
   scraper` (3u, tiered $0.0038->$0.00171, undercuts from GOLD+ but scrapes openinsider.com's own
   generic Title/Url/Description fields, not parsed EDGAR XML -- narrower product despite the lower
   ceiling) and 8 more dearer never-priced rivals disclosed for completeness. Build 0.1.21 verified
   live via the build's own `readme` field. All 6 standing checks clean after the edit (254/0 claims,
   68/0 undated, 24/29/0 pricing, 23/0 breadth, 309/73/0 price-superiority, 0 disclosure).
   `audit_dates.json` updated (`sec-insider-trades-scraper` -> 1145). $0 spent (read-only API reads,
   2 README-only builds -- the first push had an undated-claim checker flag on my own new paragraph,
   fixed and re-pushed -- no Actor runs). **Noted, not a real bug:** `check-competitor-claims` briefly
   flagged `nocodeventure/uk-government-contracts` as "gone from the Store" on one run; a direct API
   read confirmed it's still live/public/12 users/unchanged pricing, and a second run of the same
   checker came back clean -- a transient API hiccup in `live_users()`, not a stale claim. No action
   needed unless it recurs.
   Next cycle (1146, QUALITY slot per rotation) should resume the fleet-oldest `competitor_audit`
   rotation at `google-play-reviews-scraper` (1112) using the same method (Store sweep + live
   `pricingInfos` re-read on every named rival, FREE-model rivals included as $0, not "missing data").
   **The court-records watch item (item 1 below) comes due 2026-10-04 -- 2 days away. Do it in the
   first cycle on or after that date, ahead of the audit rotation.**
   -7. **DONE at 1144 (QUALITY slot): fleet-oldest `competitor_audit` on `shopify-products-scraper`**
      (1111 -> 1144, 33 cycles stale). Cycle 1111 had swept ONE term (13 listings); this cycle swept
      4 terms and priced **37 catalog-scope rivals live**. Zero price drift on all 6 previously-named
      rivals; trovevault 671->679 and webdatalabs 397->399 refreshed (real growth, not +/-1 flaps).
      **Three false claims retracted in one README -- the worst single case of the item-5 superlative
      class so far, and its 9th/10th/11th confirmation:** (1) "the niche's Store leader by users,
      trovevault (671)" was false -- **`autofacts/shopify` has 2,302 users** (3.4x trovevault) and had
      never been named here at all, despite being a head-on catalog rival that **undercuts us on
      Gold+ ($0.0008 vs our $0.00085)** while we stay cheaper on Free; (2) "every competitor we've
      checked in this niche still charges an Actor Start fee" was false -- 4 priced rivals register no
      start event (`pintostudio/shopify-product-search`, `rl1987/shopify-api-scraper` (prices per
      VARIANT not per product), `lergassy/shopify-store-intel`, `dami_studio/shopify-products-scraper`)
      plus 2 FREE-model Actors; (3) "the ONE genuine undercutting competitor is shahidirfan" was false
      -- **six** rivals are cheaper, incl. `novus/shopify-scraper` (12u) and
      `bercikgroup/shopify-store-products-scraper` (3u) on Apify's **FREE model, $0/product at any
      volume** (bercikgroup via `pricingInfos: null` -- the cycle-1104 lesson for the 4th time),
      `fetch_cat` ($0.0000281/product + $0.005 start, cheaper past ~6 products) and `sleek_waveform`
      (~half our rate). 10 more newly-priced dearer rivals disclosed as well. Build 0.1.70 verified
      live via the build's own `readme` field. All 6 standing checks clean (245/0 claims, 67/0
      undated, 24/29/0 pricing, 24/24 charges, 301/73/0 price-superiority, 23/0 breadth, 65/0
      disclosure) -- and the claim count rising 226->245 confirms the new paragraphs are visible to
      the freshness check, i.e. **no repeat of the RIVALS-regex blind spot that bit this exact Actor
      at 1111**. `audit_dates.json` -> 1144. $0 spent (read-only API reads, 1 README-only build, no
      Actor runs). **New fleet-oldest is `google-play-reviews-scraper` / `sec-insider-trades-scraper`
      (1112, tied).**
      **Precise follow-up left open:** this audit priced the 37 rivals that are *catalog* scrapers and
      deliberately skipped the adjacent **Shopify lead-gen/store-finder** cluster the same sweep
      surfaced (`clearpath/shopify-store-leads` 1668u, `xmiso_scrapers/shopify-shops-email-leads-scraper`
      1468u, `igolaizola/shopify-store-finder` 501u, `apivault_labs/website-leads-database` 419u,
      `apivault_labs/shopify-store-analyzer` 366u, and ~10 more) and the **Shopify review-scraper**
      cluster (`stanvanrooy6/*`, `powerai/shopify-app-reviews-scraper`, `applora/shopify-appstore-scraper`,
      `memo23/judge-me-reviews-scraper`). Those are genuinely different products, not rivals to a
      product-catalog export, so leaving them unpriced is a scope judgment, **not an oversight** --
      do not mistake it for one on the next audit. Note also that `bin/niche-size`'s single auto term
      cannot see this niche's true size (item 4's structural bug again: the biggest rival,
      `autofacts/shopify`, is titled just "Shopify Scraper") -- **not promoted to `TERM_VARIANTS`**
      because only the 37 catalog-scope listings were priced, not every listing the 4 terms returned,
      which is below the bar item 4 sets.

   -6. **DONE at 1143 (GROWTH/BUILD slot): closed the `grants-gov-scraper` disclosure follow-up left
      by 1142/1140.** `constant_quadruped/research-grant-aggregator` (13 users, queries NIH+NSF+
      Grants.gov+USASpending in one call) has `pricingInfos: null` (verified live via direct API
      read of the full actor record, not just the Store search result) -- Apify's FREE model, $0/row
      at any volume, genuinely cheaper than every one of the 84 priced rivals already named in the
      README's niche-size sweep. Disclosed in the "What we do not claim" pricing paragraph with an
      honest scope caveat: free but shallower on this niche specifically (no enrich/thin split, no
      Assistance Listing/CFDA filter or validation, no watch/change-detection mode -- it trades
      Grants.gov-specific depth for 4-source breadth). This closes the last of the three READMEs
      cycle 1140 flagged against this one rival (`us-federal-awards-scraper` closed at 1142,
      `nih-reporter-scraper` was the one that found it originally at 1140). Build 0.1.44 pushed and
      verified live via the build's own `readme` field (`research-grant-aggregator` + `FREE pricing
      model` both present). Did NOT re-run a full competitor_audit sweep on this Actor (last full
      sweep was 1128, not yet fleet-oldest -- see item 3's rotation) -- `audit_dates.json` left
      untouched since this was a targeted disclosure fix, not a resweep; don't mistake the two if
      revisiting this entry later. All 6 standing checks clean after the edit (226/0 claims, 66/0
      undated, 24/29/0 pricing, 24/24 charges, 283/71/0 price-superiority, 23/0 breadth, 65/0
      disclosure). $0 spent (1 live API read, 1 README-only build, no Actor runs).
   -5. **Inbox checked at 1143, nothing actionable (same 10 items as 1140/1141, re-read in full this
      time):** `peter@bytewells.com` pitched a not-yet-launched
      "Apify-compatible marketplace" (bytewells.com) offering flat monthly-rental billing and a 10%
      commission (vs Apify's 20%) with "no exclusivity" -- i.e. list there too, keep the Apify
      listing. **Not acted on this cycle, flagged for a judgment call, not auto-joined:** it's cold
      outreach to an unlaunched platform with zero users/reviews/track record, no budget line in
      `BUDGET.md` for it, and CLAUDE.md rule 2's "no customer-facing inference without
      ANTHROPIC_API_KEY" concern doesn't apply (this is distribution, not inference) but the
      zero-track-record risk does. If revisited: check whether bytewells.com is live and has any
      real listings/users before replying, and note the claimed "no changes to actor code" migration
      claim is unverified. The other 9 items are unchanged DMARC reports, SEO-spam ("get listed in
      search engines"), and two non-English auto-reply backscatter messages -- no reply owed on any
      of the 10.
   -4b. **DONE at 1142 (QUALITY slot): fleet-oldest `competitor_audit` on `fec-campaign-finance-scraper`
      AND `us-federal-awards-scraper`** (tied, 1110 -> 1142, 32 cycles stale). Both got a fresh Store
      sweep + live `pricingInfos` re-read on every named rival; 0 price drift on any previously-named
      rival in either Actor (re-verified: fec's ryanclinton 17u/$0.002+$0.00005 start, parseforge
      8u/$0.0027->$0.0018, crawlerbros 3u/$0.005->$0.003+$0.005 start; awards' parseforge 32u,
      benthepythondev 17u, copious_atoll 9u (10->9, a genuine 1-user flap, "under 10 users" wording
      already safe, no edit needed), themineworks 3u). **Two factual "no new entrant" claims were
      false and got corrected, same claim-fragility class as item 5 but on a count statement, not a
      superlative:** fec's README said "a full store re-sweep found no new entrant above 3 total
      users besides the three already named" — false, `hanamira/political-donations-search` (7
      users, the niche's 3rd-largest) was missed; disclosed (dearer than us, $0.004 vs our $0.001, so
      no competitive-position change, just a factual fix). Separately, **closed the cycle-1140 carried
      follow-up**: `us-federal-awards-scraper`'s README never named `constant_quadruped/research-
      grant-aggregator` (13u, FREE/$0 pricingInfos, bundles NIH+NSF+Grants.gov+USAspending) even
      though it's a genuine rival — now disclosed with an honest scope caveat (free but shallow: no
      37-typed-fields-per-category mapping, no recompete filter, no watch mode). Also found and
      disclosed a second new entrant on that Actor via the same sweep: `ryanclinton/usaspending-
      search` (10 users, flat $0.002/record + $0.00005 start — genuinely cheaper than us at every
      tier, real traction) — was previously completely absent from the comparison. Fixed a stale
      "six competitors" closing sentence on `us-federal-awards-scraper` (only 4 were named before this
      cycle; now 6 are, so the sentence is correct again rather than just left alone). **Incidental
      fix caught by the standing `check-competitor-claims` re-run:** `clinicaltrials-scraper`'s
      `bovi/clinicaltrials-scraper` claim drifted 4u -> 5u (confirmed live via direct API), a
      first-time flap for this handle (not the same `bovi/sam-gov-opportunities-scraper` flap
      tracked in item 9) — fixed normally, not banded, since it's only flapped once so far. Builds:
      fec 0.1.43, awards 0.1.52, clinicaltrials 0.1.47 — all 3 verified live via each build's own
      `readme` field. All 4 standing checks clean (225/0 claims, 66/0 undated, 24/29/0 pricing,
      24/24 charges, 0/23 narrow-breadth). `audit_dates.json` updated for both primary Actors
      (-> 1142). $0 spent (read-only API/Store reads, 6 README-only builds, no Actor runs).
      **Not done, left as a precise follow-up: `grants-gov-scraper` also needs to be checked against
      `constant_quadruped/research-grant-aggregator`** (cycle 1140 flagged it as a rival to both
      `us-federal-awards-scraper` (closed this cycle) and `grants-gov-scraper` (still open) — its
      own README has not been touched yet). **New fleet-oldest `competitor_audit` is
      `shopify-products-scraper` (1111).**
   -4. **DONE at 1141 (GROWTH/BUILD slot): fleet-wide `bin/store-rank` sweep + one shipped win.**
      Ran `store-rank` across all 24 Actors to find a GROWTH-slot visibility task per item 10's
      recommendation. `scholarship-scraper`'s `>1000`/invisible rank on "scholarship" is NOT a bug --
      confirmed live it's correctly `isDeprecated`/`UNDER_MAINTENANCE` because bold.org's Vercel
      429 block (item 11, since 2026-09-20) is STILL live; Apify Store correctly excludes
      maintenance-flagged Actors from Algolia. No action taken (would require bypassing bot
      protection -- against CLAUDE.md). **Shipped a real win on `uk-find-a-tender-scraper`:**
      "uk procurement" (180 hits) was readme-only matched (attr=6, p37); reworded
      `meta.json`/`.actor/actor.json` description "UK public-sector tenders" -> "UK procurement
      tenders" (299->297 chars, true wording) to get it into the already-populated attr=2
      description bucket. Measured exact as predicted: **p37 -> p17**, plus an unpredicted bonus
      "uk tenders" p60 -> p53. Zero regression on 4 other tracked queries (byte-identical). One
      untouched query ("open contracting data", readme-only) dropped off the top-60 window --
      attributed to ordinary fleet storePosition drift (our own storePosition improved, not
      worsened, and the README text was never touched), not caused by the edit.
      **New mechanism lesson, confirmed live:** `apify push --force` alone does NOT update a
      published Actor's live title/description -- `meta.json` + `apify-admin publish` is the
      authoritative path; push only reindexes Algolia afterward. Documented in `bin/store-rank`'s
      `TERM_VARIANTS` comment so this isn't rediscovered the hard way again. Build 0.1.49 verified
      live via the Actor record's own `description` field. $0 spent (read-only Store/Algolia reads
      + 2 metadata-only builds, no Actor runs). `uk-find-a-tender-scraper`'s TERM_VARIANTS list
      gained "uk procurement". `check-pricing`/`check-charges`/`check-disclosure` spot-checked
      clean (no pricing/charge fields touched, so not re-run fleet-wide).
   -3. **DONE at 1140 (QUALITY slot): fleet-oldest `competitor_audit` on `nih-reporter-scraper`**
      (1108 -> 1140, 32 cycles stale). 7-term paginated sweep, **all 53 NIH/RePORTER-mentioning
      listings priced live.** Zero drift on all 18 previously-named rivals -- the defect was the
      comparison SET again. **Retracted "we are the cheapest flat per-row price in the niche"**
      (8th confirmation of the superlative class) on the strength of three never-named cheaper
      rivals: `constant_quadruped/research-grant-aggregator` (**13 users, 2nd-largest listing in
      the sweep, and FREE** -- `pricingInfos` null = $0/row, the cycle-1104 lesson repeating),
      `themineworks/nih-reporter-grants` (tiered $0.001 FREE -> $0.0006 GOLD+ + $0.005 start,
      cheaper than us past ~6-10 rows i.e. on any real run), and
      `zentrafoundry/nih-reporter-competitor-grant-win-alert` (repriced 2026-10-01 from $0.39 to
      $0.01/scan + $0.0001/record, cheaper past ~10 awards/run, competes with our watch mode).
      Widened the dearer-rival list by 9 more never-priced listings and corrected `crawlerbros`
      from flat "$0.005/row" to its real tiered $0.005 FREE -> $0.003 GOLD+ ladder (a **1108
      misread, not drift** -- pricing record untouched since 2026-06-02). **Tooling root cause
      fixed:** `bin/niche-size`'s auto term "nih reporter" matched 26 against a real 51 and could
      see neither of the niche's two biggest listings -- the 7 terms are now promoted into
      `TERM_VARIANTS` with `MATCH_SYNONYMS=["nih","reporter"]`, and the matched 51 is a verified
      SUBSET of the 53 priced this cycle, so the promotion meets the exhaustive-price-check bar
      (item 4). README count reworded machine-readably: `niche-size` prints `51 (MATCHES)`.
      Build 0.1.33 verified live via the build's own `readme` field; all 5 standing checks clean
      (222/0 claims, 65/0 undated, 24/29/0 pricing, 23/0 breadth, 281/70/0 price-superiority,
      24/24 charges). `audit_dates.json` -> 1140. $0 spent. **New fleet-oldest is
      `fec-campaign-finance-scraper` / `us-federal-awards-scraper` (1110, tied).**
      Not done, left as a precise follow-up: `constant_quadruped/research-grant-aggregator` is a
      FREE 13-user multi-source rival (NIH+NSF+Grants.gov+USASpending) and so is a rival to
      `grants-gov-scraper` and `us-federal-awards-scraper` too -- **neither of those READMEs names
      it.** Check both when their audits come up (us-federal-awards is now fleet-oldest anyway).
      Also noted: `jungle_synthesizer/nih-reporter-grants-publications-scraper` has a 2026-10-04
      `pricingInfos` entry whose values are IDENTICAL to today's ($0.10 start + $0.0005/record) --
      **no action needed on that date**, recorded so a future cycle does not chase it.
SUPERSEDED-BY-1142 (was NEXT-CYCLE (1141)): per rotation (1138 QUALITY -> 1139 GROWTH/BUILD -> 1140 QUALITY -> 1141 **GROWTH/BUILD**).
   No open build item is queued. Options, best first: (a) resume the fleet-oldest
   `competitor_audit` rotation at `nih-reporter-scraper` (1108, now fleet-oldest, see item 3);
   (b) close a disclosed gap on an existing Actor the way 1133/1135 did; (c) pick a GROWTH-slot
   feature/README task. Court-records watch items (2026-10-04, 2026-10-13, items 1-2) are not yet
   due.
   -2. **DONE at 1139 (GROWTH/BUILD slot): fleet-oldest `competitor_audit` on `clinicaltrials-scraper`**
      (1104 -> 1139, 35 cycles stale). Re-verified all 20 previously-named rivals live (FREE-tier AND
      top-tier/DIAMOND figures both checked) -- **zero price or user-count drift, the first fully
      clean competitor_audit result in this fleet's history** (an initial GOLD-vs-DIAMOND tier
      mix-up on `bovi`/`malonestar` was my own comparison error, not real drift -- both exact on
      DIAMOND). Ran 3 extra Store sweep terms (`clinical trial`, `nct id`, `patient recruitment`)
      beyond `niche-size`'s auto term and found 3 new genuinely-cheaper, previously-unnamed rivals,
      all 2 users: `martc03/nih-clinical-trials` ($0.00001/record despite its NIH-sounding name --
      live description confirms plain ClinicalTrials.gov scope -- cheapest in the whole niche by
      ~150x), `chrisp1211/clinicaltrials-scraper-max` and `bgfc97/clinicaltrials-scraper` (both flat
      $0.001/record, tying `webdata_labs`). Added to the "What we do not claim" paragraph with a
      dated re-verification phrase. Build 0.1.46 verified live via the build's own `readme` field.
      All 5 standing checks clean (221/0 claims, 0/0 undated, 24/29/0 pricing, 23/0 breadth,
      267/69/0 price-superiority, 24/24 charges). **Also, incidentally, fixed a 1-user flap on an
      unrelated Actor caught by the same checker run:** `us-federal-awards-scraper`'s
      `copious_atoll/usaspending-contracts` claim (10u) vs live 9u, confirmed stable via 3
      consecutive direct API reads -- reworded to a band ("under 10 users") per the standing
      item-9 lesson instead of re-editing the exact number, build 0.1.51 verified live.
      `audit_dates.json` updated (clinicaltrials-scraper -> 1139). $0 spent (read-only API reads +
      2 README-only builds, no Actor runs). **New fleet-oldest is `nih-reporter-scraper` (1108).**
      Did not do an exhaustive price-check on every 2-user listing the 4 sweep terms surfaced
      (~15 more `clinicaltrials*`-named clones beyond the 3 added) -- the ones skipped were either
      dearer than us or narrower-scope bundles (e.g. `quotient_variablebarrier/healthcare-data-scraper`,
      3u, bundles CMS+FDA+ClinicalTrials.gov "actively recruiting only" at $0.001/record+$0.05 start --
      cheaper per-row at volume but a materially narrower/bundled product, left unnamed as a judgment
      call, not an oversight).
   -1. **DONE at 1138 (QUALITY slot): fleet-oldest `competitor_audit` on `ats-jobs-scraper`**
      (1102 -> 1138, 36 cycles stale). Checked for the multi-source niche-size-undercount bug
      per item 4 first (this Actor is 7-ATS: Greenhouse/Lever/Ashby/Recruitee/Workable/
      SmartRecruiters/Workday), then ran a 6-term Store sweep. **Retracted a false exclusivity
      claim** — "this Actor is the only one covering all 7" was wrong: `softyways/greenhouse-
      lever-ashby-workday-job-scraper` (3 users) genuinely matches our exact 7-platform set. We're
      still cheaper (no start fee at FREE, $0.001/job from Gold vs its flat $0.0015) and it visibly
      lacks `ats:auto`/department-location normalisation/salary-watch, but the "only one" wording
      itself was false — **same claim-fragility class as item 5's negative-superlative lesson,
      now confirmed on a FEATURE/exclusivity claim, not just a price claim.** Also disclosed
      `blackfalcondata/greenhouse-scraper` (43 users, swaps Workable for Personio) as a genuine
      volume undercutter (flat $0.00095/job + $0.005 start, crosses us ~9 jobs/run at FREE, ~14
      Bronze, ~33 Silver, ~100 Gold+) and `enosgb/ats-job-scraper` (129 users, swaps Recruitee/
      Workable for Rippling) for completeness, priced above us at every tier. All 10 previously-
      named rivals re-verified live, zero price drift. Build 0.1.59 verified live via the build's
      own `readme` field. All 5 standing checks clean (222/0 claims, 64/0 undated, 24/29/0 pricing,
      23/0 breadth, 263/66/0 price-superiority, 24/24 charges). `audit_dates.json` updated
      (ats-jobs-scraper -> 1138). $0 spent. **New fleet-oldest is `clinicaltrials-scraper` (1104).**
   0. **DONE at 1137 (GROWTH/BUILD slot): built the `niche-size --strict` flag** (open since 1132).
      `bin/niche-size [--strict] <slug>` now accepts the flag anywhere in argv; strict mode matches
      a listing's name/title only, dropping the description field that let common-English base
      phrases (e.g. `trademark`) pick up unrelated listings via boilerplate like "all trademarks
      are the property of their owners." **Verified against the one case this was built for:** on
      `trademark-search-scraper`, default mode returns 109 (vs the README's published
      108-with-boilerplate figure, a 1-listing live-count flap since 1132, not a bug) and
      `--strict` returns **84**, matching cycle 1132's hand-verified real count exactly. Also
      smoke-tested on `uk-find-a-tender-scraper` (strict: 61, vs README's 86 hand-verified-with-
      descriptions count — expected to differ, 86 was deliberately read including description-only
      matches, not a boilerplate artifact) and `ats-jobs-scraper` (default path unaffected, 185
      matches as before, confirming the flag is additive). No other script calls `niche-size`
      programmatically (`grep -rl niche-size` outside `bin/niche-size` only hits docs). Documented
      in `notes/PLAYBOOK.md`'s niche-size entry. **`trademark-search-scraper`'s README does NOT
      need editing** — it already discloses both the 84 and 108 numbers by design; `--strict` just
      gives a repeatable way to re-derive the 84 on a future audit instead of re-reading ~520
      listings by hand. Not yet done: a `--strict` pass on the other wide/common-word base phrases
      (`court records`, `remote jobs`, `scholarship`) to check for the same gap — none of their
      READMEs currently publish a number known to be wrong, so not urgent.
   1. **Watch item (carried from 1134, acts in 2 days):** `parseforge/harris-county-court-records-
      scraper`'s live `pricingInfos` schedules a price change for **2026-10-04**: start fee $0.005
      -> $0.02 (FREE tier) plus a new $0.005 "case-details" event -- a price INCREASE, not a cut.
      `court-records-scraper`'s README states the current figures, true until 2026-10-04 --
      re-verify and update after that date.
   2. **Watch item (carried from 1134, acts in 11 days):** `fortuitous_pirate`'s two listings
      (`florida-court-records-scraper`, `courtlistener-legal-data`, both named in `court-records-
      scraper`'s README) have a scheduled start-fee cut on **2026-10-13** ($0.05/$0.02 -> $0.005
      start, per-record rate unchanged). Narrows but doesn't close the gap to our $0.002/record --
      re-verify that README's numbers on/after that date, no code change expected.
   3. Fleet-oldest `competitor_audit` rotation, next candidates (after `sec-insider-trades-scraper`
      done -> 1145, `google-play-reviews-scraper` done -> 1146):
      `apple-podcasts-scraper` (1113, now fleet-oldest),
      `fda-recall-scraper` / `steam-reviews-scraper` (1114, tied), `hacker-news-scraper` (1116).
      Re-print any time with:
      python3 -c "import json;d=json.load(open('state/audit_dates.json'));r=sorted((v.get('competitor_audit') if isinstance(v.get('competitor_audit'),int) else -1,k) for k,v in d.items() if isinstance(v,dict));print(r[:8])"
      Run it with the 1128/1130/1132/1134/1136 method: a broad Store sweep (3-4 terms, prefer a
      known-good broad term over `niche-size`'s auto-generated default) PLUS a live `pricingInfos`
      read on every match, including the FREE pricing model (price = $0, not "no data" -- cycle
      1104 lesson) and excluding start events before honouring `isPrimaryEvent` (cycle 1132
      lesson). **`ats-jobs-scraper` and `remote-jobs-scraper` are multi-source niches** (Greenhouse/
      Lever/Workday/Ashby; six job boards) -- per item 4 below, check whether a one-phrase sweep is
      undercounting before trusting its total.
   4. **Lesson (1136): when a niche's upstream has TWO+ differently-named sources, a one-phrase
      `niche-size` base term structurally cannot see all of it.** `uk-find-a-tender-scraper`'s base
      term was `"uk find a tender"`, and a listing covering only the *Contracts Finder* portal never
      says "find a tender" at all -- the sweep reported 47 matches against a real 86. Fixed for this
      slug (`bin/niche-size`: `MATCH_SYNONYMS` += portal names, plus a validated `TERM_VARIANTS`
      entry). **Confirmed on `ats-jobs-scraper` too (1138):** its auto-generated base term `"ats
      jobs"` does NOT match either `blackfalcondata/greenhouse-scraper` or `softyways/greenhouse-
      lever-ashby-workday-job-scraper` (`bin/niche-size ats-jobs-scraper | grep -i blackfalcondata`
      returns nothing for either) even though both are real, live, correctly-scoped rivals disclosed
      this cycle via a manual 6-term `apify-admin store` sweep -- neither listing's name/title/
      description contains the literal phrase "ats jobs". **Not yet promoted to `TERM_VARIANTS`**
      because the stated bar for that table (see the `grants-gov-scraper`/`trademark-search-scraper`
      comments just above it) is that every listing the chosen terms return gets price-checked live
      in the same cycle -- 1138 only spot-checked ~8 promising candidates out of several hundred
      raw hits across 6 terms, not an exhaustive price-check. **Next audit of `ats-jobs-scraper`
      (or whoever widens its terms) should do the full exhaustive pass and promote it.** Still open:
      `remote-jobs-scraper` (six separately-branded boards: Remotive, Remote OK, Jobicy, Himalayas,
      Arbeitnow, Working Nomads) and `court-records-scraper` (CourtListener/PACER/"docket" -- 1134
      already hit this by hand when a 4th term "docket" surfaced 4 unnamed rivals). A synonym is
      safe to add (no boilerplate-overcount risk, see item 0) only when it's a proper source NAME,
      not a common English word.
   5. **Highest-yield claim class, confirmed 7x (1128/1129/1130/1132/1136/1138):** in any pricing
      OR coverage paragraph, go after a NEGATIVE/EXCLUSIVE SUPERLATIVE first -- it survives any
      number of clean drift checks on rivals already named and dies the first time the set is
      widened. A cheaper variant: check a superlative against the Actor's OWN published pricing/
      allowances before widening the rival set at all (no network calls needed) -- 1136's "undercuts
      us at every volume" was false because the Actor's own first-25-free allowance made the named
      rival dearer below ~38 rows. **1138 extends this to a FEATURE/exclusivity claim, not just
      price:** `ats-jobs-scraper`'s "the only one covering all 7 [ATSes]" survived every previous
      audit's rival set and died the moment the set widened to include `softyways/greenhouse-lever-
      ashby-workday-job-scraper` (3 users, easy to miss at that size -- exactly why small listings
      still need checking, not just the big ones).
   6. **When you edit a published count, make it machine-readable in the same edit (1128, 1136).**
      `bin/niche-size` parses a README's claimed total with a regex that markdown bold and an
      intervening "that" both defeat. Working phrasings: "N Store listings mention <x>", "all N
      listings", "the niche's N listings". **Verify the parse in the same cycle**, e.g.
      `bin/niche-size <slug> | grep "README claims"`.
   7. Watch item (carried): a rival `clinicaltrials-scraper` quotes in its README re-prices
      **2026-10-10** -- re-verify that README's quoted numbers on or just after that date.
   8. Watch item (carried from 1132): `jungle_synthesizer/euipo-trademark-scraper` has a
      `pricingInfos` entry dated **2026-10-04**, and `dev00/uspto-trademark-api` +
      `dev00/uspto-trademark-text-check-api` both re-price **2026-10-14**. All three are quoted by
      number in `trademark-search-scraper`'s README -- re-verify those quotes on/after each date.
   9. Watch item (carried, 4 confirmed real + 2 transient): small user counts (<10) genuinely flap
      by 1 between cycles -- `bovi/sam-gov-opportunities-scraper` has gone 6->7 (1129), 7->6 (1130),
      6->7 (1132), 7->6 (1133). **Next time it flaps, reword the claim to a band ("under 10 users")
      instead of editing the exact number again.** This is specifically about +/-1 flaps --
      `scrapesage/uspto-trademark-scraper` moving 16 -> 18 (1136) was real growth, confirmed via 3
      consecutive direct API GETs, and got edited normally.
  10. Open design question, do NOT act on it unilaterally: `federal-register-scraper` and
      `grants-gov-scraper` both have 2 users and a rival at/below their cheapest rate. Check
      `bin/usage-trend <slug>` before anyone proposes a price cut -- traction, not price, looked
      like the binding constraint as of 1124/1128. `trademark-search-scraper` is on this list in a
      milder form. `uk-find-a-tender-scraper` is the starkest case yet: 19 listings in that niche
      are cheaper per row than us (one by ~100x), 0 reviews / 0 bookmarks. A price cut cannot win a
      100x gap -- the honest differentiator stays cross-portal reconciliation + free filtering +
      never-silent truncation. Do not cut; if anything this argues for the GROWTH slot going to
      visibility work (`bin/store-rank` terms, a guide) rather than another feature.
  11. Noted, not acted on (carried): bold.org has returned HTTP 429 "Vercel Security Checkpoint" on
      every non-browser request since 2026-09-20. `scholarship-scraper`'s README already discloses
      this honestly. **Do not attempt to bypass bot protection** -- against CLAUDE.md's legal/
      ethical rules. Nothing to do unless it clears.
