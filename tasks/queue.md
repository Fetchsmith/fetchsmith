- [x] **CLOSED c3313 -- regular slot (3313 % 3 == 1, verified with `echo $((3313 % 3))`). Preflight fully clean on arrival** (tree clean, c3312's `015287e2` present in `git log`; `checks-due --all` **NONE DUE** (soonest `git-maintain` in 3c); `audit-due --all` **FLEET ROTATIONS NONE DUE** (only informational one-off/experimental axes, c1304 rule); `inbox-triage new` **NONE UNTRIAGED** (82 msgs, including the 2 owner Apify-token-rotation forwards re-confirmed stale yet again, resolved c3062-3064); `bin/revenue` unchanged -- **$0 booked, 27 Actors, 54 users, no buyer signal**). With no fleet checks/audits due and no support mail pending, continued the standing `NEW c3162` vendor-catalogue triage at rows 233-238 (indices 232-237) -- wrote `bin/_triage3313.py` (clone of `bin/_triage3304.py`'s pattern, deleted after use), same method (`cps.effective(pricingInfos, now)` for the live tier, every charge event and tier rung expanded). **All 6 handles genuinely new (exact-handle grep across `actors/*/README.md`, `site/`, `notes/`: 0 hits for all 6). 1 of 6 real: `factpipe/website-screenshot`** (3u) ties our flat $0.002/result at FREE but tiers down to $0.0018/$0.0016/$0.0014 at BRONZE/SILVER/GOLD+ with no start fee -- a genuine, if smaller-magnitude, undercut past the FREE plan, plus a built-in cookie-banner-hiding feature we have no no-selector equivalent for. The other 5: `devilscrapes/workday-jobs-scraper` (Workday-only scope exclusion AND dearer at every tier, double non-issue), `devilscrapes/hacker-news-scraper` (10-17x dearer), `everyotherfriday/google-play` (broader app-details/search/developer-catalog product but 2x dearer per review, non-issue), `feedforge/weworkremotely-scraper` (WWR-only scope exclusion, same bucket as prior single-board rulings despite a cheaper in-scope rate), `feedforge/steam-games-scraper` (games-catalog product, 4-8x dearer, no reviews). **Disclosed and shipped same-cycle** (established practice, not deferred to a rotation): new dated paragraph in `website-screenshot-scraper/README.md` (after the `locaihost` paragraph, before `## FAQ`), `package.json` 0.1.4 -> 0.1.5, pushed (`apify push --force -w 600`, build 0.1.50), live README verified byte-identical via `GET /v2/actor-builds/{id}` (32,672 chars both sides, `factpipe` present in the live copy). Tracker now at 238/1,485 rows; resume pointer in `NEW c3162` updated to rows 239-244. No owner email owed ($0 revenue unchanged, no buyer signal). **Spend this cycle: ~$0.005** (1 billable Apify platform build for the push; 12 own-token Apify metadata GETs, free). All 3 services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`); `/`, `/tools`, `/pricing` all 200. **Pace: 0 new Actors built today (2026-11-17).** **Next cycle should run `checks-due`/`audit-due`/`inbox-triage new` fresh first as always; if no higher-priority backlog item is open, resume triage at rows 239-244.**

- [ ] **CLOSED c3312 -- QUALITY/GROWTH slot (3312 % 3 == 0, verified with `echo $((3312 % 3))`). Preflight fully clean on arrival:** tree clean, c3311's `314449a2` present in `git log`; `checks-due --all` **NONE DUE** (soonest `git-maintain` in 4c); `audit-due --all` **FLEET ROTATIONS NONE DUE** (only informational one-off/experimental axes, c1304 rule); `inbox-triage new` **NONE UNTRIAGED** (82 msgs); `bin/revenue` unchanged -- **$0 booked, 27 Actors, 54 users, 1573 runs30d, 31 ext_bad30d, 0 bookmarks/reviews, polar {}, no buyer signal**.

  **Deliberately did NOT trim `tasks/queue.md` even though `check-doc-size` printed `TRIM DUE` (176.4KB/1055ln, ~4 cycles of headroom).** `STANDING c3280`'s written decision rule is re-trim only when headroom drops **below ~3 cycles** (it names c3320-c3325); the `TRIM DUE` banner fires at any size above ~70KB because the checker projects 24 cycles ahead, and the item says in so many words that this *is not a failed trim and is not a reason to re-trim*. Recording the non-action so a future cycle does not read the banner and re-derive the decision. **Next trim still c3320-c3325.**

  **Work -- the CLAUDE.md QUALITY mandate taken literally ("re-run platform tests on 2-3 existing Actors with different inputs"), on the two stalest `varied_test` rotations in the fleet.** Picked by sorting `state/audit_dates.json` on `varied_test`: **`clinicaltrials-scraper` had NEVER had one on record (null)** and **`ats-jobs-scraper` was the oldest at c2666 (646 cycles stale)**. Both came back **CLEAN -- 0 defects, 0 code/README changes needed.**

  **(1) `clinicaltrials-scraper`, 6 filters verified against live rows (2 runs, 10 rows each).** Input `{conditions:"breast cancer", phases:["PHASE3"], overallStatus:["RECRUITING"], studyTypes:["INTERVENTIONAL"], sex:"FEMALE", funderTypes:["INDUSTRY"], sortBy:"LastUpdatePostDate:desc", maxResults:10}`. All 10/10 rows: `overallStatus=RECRUITING`, `studyType=INTERVENTIONAL`, `sex=FEMALE`, every `conditions` entry breast-cancer-related, and `lastUpdatePostDate` **strictly descending** (2026-11-12, 10-27, 10-02, 09-30, 09-09, 08-25, 08-18, 06-04, 06-02, 05-26) so `sortBy` is genuinely honored, not ignored. **`phases` returned two rows as `["PHASE2","PHASE3"]` -- that is CORRECT, not a filter leak:** a PHASE2/PHASE3 study *is* a phase-3 study and ClinicalTrials.gov tags it with both; do not "fix" this. **`funderTypes` needed a SECOND run to verify** -- the first asked for output key `leadSponsorName`, which is **NOT A FIELD** (the varied-test guard caught it; real fields are `leadSponsor` / `leadSponsorClass`), and `it.get()` would have read the absent key as a null and looked like "the Actor returns nothing here". Re-run with the right keys: **10/10 `leadSponsorClass=INDUSTRY`** (Genentech, Sichuan Baili, Shandong Suncadia, MediLink, ...). Filter confirmed.

  **(2) `ats-jobs-scraper`, cross-platform parser sweep over 4 of the 12 ATS platforms (2 runs, 10 + 8 rows).** Run A `{companies:[greenhouse:airbnb, ashby:ramp, teamtailor:oatly, workable:getresponse], titleKeyword:"engineer", includeDescriptions:false, maxJobsPerCompany:5, maxResults:10}`: `titleKeyword` held 10/10, `maxJobsPerCompany=5` held exactly (5 airbnb + 5 ramp). **But `maxResults=10` was fully consumed by the first two companies, so teamtailor and workable were never fetched at all** -- so run A exercised only 2 of the 4 parsers. **This is NOT a bug and NOT a doc gap: `README.md:43` and the FAQ at `README.md:274` already document it precisely**, including that the skipped companies get their own named line in the status message ("companies are fetched in the order you list them, and once `maxResults` is reached the run stops immediately"). Live behaviour matched the written docs exactly -- a positive confirmation, nothing to file. Run B therefore re-ran with **only** `[teamtailor:oatly, workable:getresponse]`, `maxJobsPerCompany:4, maxResults:8`: **both parsers clean, 4+4 rows exactly**, `jobUrl` well-formed on both platforms (`oatly.teamtailor.com/jobs/8707696-...`, `apply.workable.com/j/E0D8082BC0`), `location` parsed on both (Ritthem / Ogden / Brussels; Gdansk / Poland / Spain), and **`isRemote` genuinely varies** (False on the teamtailor rows, True on 3 of 4 workable rows) rather than being hardcoded. **`descriptionText`/`descriptionHtml` were null in every row and the varied-test guard flagged them `REAL NULLS -- worth investigating`: that flag is a FALSE POSITIVE here, it is exactly what `includeDescriptions:false` is supposed to do.** Do not re-investigate it on an `includeDescriptions:false` run.

  **Recorded `varied_test: 3312` for both Actors in `state/audit_dates.json`** (`clinicaltrials-scraper` null -> 3312, `ats-jobs-scraper` 2666 -> 3312). Also ran the two PLAYBOOK every-QUALITY-cycle items: **`bin/devto-comments`** -- 34 published articles, 12 with comments, **19 inbound, 0 unanswered** (the `danorie` question `check-blog-claims` flagged as unanswered at c3297 has since been answered), 1 spam-skipped; and **`bin/check-disclosure`** -- 95 site posts + 34 dev.to articles, **0 missing disclosure**. Both recorded via `checks-due --ran`. **`bin/actor-health`: 24/24 scrapers ok (status 201, 0 fail_rows each), both MCP standby servers ok (list 200 / tool_listed / call 200), `scholarship-scraper` still RETIRED-429 as expected** -- so the standing `ext_bad30d=31` is NOT live breakage. Guards clean: `check-charges` 27 priced / 0 missing / 0 drift; `check-registry-fields` 0 drift. All 3 services active; `/`, `/tools`, `/pricing`, `/tools/clinicaltrials-scraper` all **200**. **Spend this cycle: ~$0.04** (4 capped 8-10-row billable runs; `apify-spend` $3.38 -> $3.4168, projection $12.73 vs the $85 hard cap). **Blockers: none. Owner email: none owed.** **Pace: 0 new Actors built today (2026-11-17).**

- [ ] **NEW c3311 (LOW-MEDIUM -- one genuine price-undercut find, to be folded into `ats-jobs-scraper`'s next `competitor_audit` rotation, NOT published as an off-cycle README edit).** Found at row 231 of the c3162 catalogue. `deepmine/workable-jobs` (1 user, 42 public30d) is a **new handle** (0 exact-handle hits fleet-wide) and is a genuine per-unit undercut for its scope, even though it is also a scope exclusion (Workable only, 1/12 of our ATS platforms). Its single charge event (`apify-default-dataset-item`, "Job") is tiered **$0.00059 FREE -> $0.00049 BRONZE -> $0.00039 SILVER -> $0.00035 GOLD+**, no start fee, against our flat-across-platforms `job` event at **$0.001 FREE -> $0.00085 BRONZE -> $0.00075 SILVER -> $0.0007 GOLD+** -- it undercuts us by **~41-50% at every tier, no crossover threshold** (unlike the c3308/c3310 start-fee-masked thin-conditional cases, this is a clean full-range undercut). A buyer who only needs Workable jobs (not the other 11 platforms) gets both narrower scope AND a materially lower price from them today. Worth a real line in the next `ats-jobs-scraper` competitor_audit (either a per-platform pricing note, or confirm there's no easy way to match it without discounting the other 11 platforms) rather than silent -- `check-price-superiority`'s whole-Actor comparison will never surface a single-platform-scoped rival like this.

- [x] **CLOSED c3311 -- regular slot (3311 % 3 == 2, verified with `echo $((3311 % 3))`). Preflight fully clean on arrival** (tree clean, c3310's `0f95a26e` present in `git log`; `checks-due --all` **1 DUE -- `apify-spend`**; `audit-due --all` **FLEET ROTATIONS NONE DUE** (only informational one-off/experimental axes, c1304 rule); `inbox-triage new` **NONE UNTRIAGED** (the 2 owner Apify-token-rotation forwards from 2026-11-11 reconfirmed stale yet again, resolved c3062-3064; rest is dmarc reports + 3 unsolicited marketing/"added to directory"/backlink-spam emails, no action needed); `bin/revenue` unchanged -- **$0 booked, 27 Actors, 54 users, 1573 runs30d, 31 ext_bad30d, 0 bookmarks/reviews, polar {}, no buyer signal**). **Ran the one due check: `apify-spend` -- $3.38 used this cycle ($2.38 above the $1 included credit), 26.7% into the 2026-11-09..12-08 billing cycle, projection $12.63 -- in line with the prior cycle's actual ($12.23) and well under the $85 hard cap. No anomaly, no action.** Recorded (`last_cycle` 3215 -> 3311, next due c3407). With no other backlog open, continued the standing `NEW c3162` vendor-catalogue triage at rows 227-232 (indices 226-231) -- wrote `bin/_triage3311.py` (clone of `bin/_triage3304.py`, deleted after use), same method (`cps.effective(pricingInfos, now)` for the live tier, every charge event and tier rung expanded). **All 6 handles genuinely new (exact-handle grep across `actors/*/README.md`, `site/`, `notes/`: 0 hits for all 6).** Row by row: (1) `datalantern/ats-jobs` (3u) covers only Greenhouse/Lever/Ashby/SmartRecruiters/Workable (5/12 platforms) -- scope exclusion -- AND charges a $0.005 one-time start fee plus flat $0.0015/job vs our $0.001->$0.0007 with no start fee, dearer at every tier before the fee even counts, double non-issue, same bucket as `datadesk-io`/`cryptosignals`. (2) `datapilot/ai-tool-launch-tracker-scraper` (3u) is a curated AI-product-launch monitor off Show HN (category/pricing-model classification, dedup) at flat $0.002/result vs our raw Hacker News export at $0.0002->$0.0001 -- 10-20x dearer AND a different product shape (classified monitoring digest, not a raw item export), same bucket as `constant_quadruped/steam-review-monitor` (c3310). (3) `datapilot/export-intelligence-monitor` (3u) aggregates World Bank trade indicators + UN Comtrade + Google News regulatory coverage into export-market intelligence at flat $0.003/record vs our plain Google News RSS export at $0.002->$0.001 -- dearer AND a different, much broader product shape (multi-source trade intelligence vs single-source news export), category mismatch. (4) `datapilot/franchise-expansion-tracker` (3u) is a Google-News-RSS franchise-expansion vertical (structured fields: expansion units, investment amounts, countries) at flat $0.002/item -- **ties our FREE-tier $0.002 exactly but we go cheaper at every tier above it** ($0.0018/$0.0015/$0.001), same tied-at-best-dearer-overall shape as `cirkit`'s siblings (c3310). (5) `deepmine/workable-jobs` -- see `NEW c3311` above, a genuine price-undercut find for its single-platform scope. (6) `devilscrapes/multi-ats-jobs-scraper` (3u) covers only Greenhouse/Lever/Ashby (3/12 platforms) -- scope exclusion -- AND tiered $0.0015->$0.00132/job vs our $0.001->$0.0007, dearer at every tier, double non-issue. Tracker now at 232/1,485 rows; resume pointer in `NEW c3162` updated to rows 233-238. No README/code changes this cycle (the one genuine find filed as `NEW c3311` for the next rotation instead), no owner email owed, $0 spent (apify-spend's 4 GETs + 9 own-token triage metadata GETs only). All 3 services active, `/`, `/tools`, `/pricing` all 200. **Next cycle should run `checks-due`/`audit-due`/`inbox-triage new` fresh first as always; if no higher-priority backlog item is open, resume triage at rows 233-238.**

- [x] **CLOSED c3310 -- regular slot (3310 % 3 == 1, verified with `echo $((3310 % 3))`). Preflight fully clean on arrival** (tree clean, c3309's `eb2c3bb0` present in `git log`; `checks-due --all` **NONE DUE** (soonest `apify-spend` at c3311, 1c out); `audit-due --all` **FLEET ROTATIONS NONE DUE** (only informational one-off/experimental axes, c1304 rule); `inbox-triage new` **NONE UNTRIAGED** (the 2 owner Apify-token-rotation forwards from 2026-11-11 reconfirmed stale, resolved c3062-3064; rest is dmarc reports + 3 unsolicited marketing/"added to directory" emails, no action needed); `bin/revenue` unchanged -- **$0 booked, 27 Actors, 54 users, 1573 runs30d, 31 ext_bad30d, 0 bookmarks/reviews, polar {}, no buyer signal**). With no fleet checks/audits due and no support mail pending, continued the standing `NEW c3162` vendor-catalogue triage at rows 221-226 (indices 220-225) -- wrote `bin/_triage3310.py` (clone of `bin/_triage3304.py`, deleted after use), same method (`cps.effective(pricingInfos, now)` for the live tier, never `[-1]`; every charge event and tier rung expanded). **All 6 handles genuinely new (exact-handle grep across `actors/*/README.md`, `site/`, `notes/`: 0 hits for all 6), 0 of 6 price undercutters.** Row by row: (1) `cirkit/shopify-store-catalog-scraper` (3u) flat $0.001/product + a $0.00005 one-time start fee -- ties our FREE-tier $0.001 but dearer at every tier above it ($0.00095->$0.00085) plus the fee we don't charge, same tied-at-best-dearer-overall shape as `sync-network`/`bgfc97`/`cirkit`'s siblings. (2) `cliqtomedia/google-play-reviews-scraper` (3u) charges a **$0.0035 one-time start fee** + $0.0001 FREE -> $0.00007 DIAMOND per review vs our flat $0.0001 with no start fee -- ties our per-unit rate at FREE/BRONZE and only undercuts it at SILVER+ ($0.00008/$0.00007 < $0.0001), but the start fee dominates at realistic volumes: crossover (their total < ours) requires **>175 reviews/run at their SILVER tier or >117 reviews/run at GOLD+**, so at the common case (new user, low-to-mid volume) they are strictly dearer; a thin conditional case, not a real undercutter, but worth recording precisely (same partial-crossover shape as `chimerical_quicklime/remotive-scraper`, c3308). (3) `constant_quadruped/steam-review-monitor` (3u) is flat $0.004 per game-x-run intelligence record (reviews + score delta + live player count + diff digest) vs our $0.000575->$0.0003 per raw review/game record -- 7-13x dearer AND a different product shape (aggregated monitoring digest, not a raw per-review export), same bucket as the `zinin`/`pintostudio` store-level-aggregate exclusions. (4) `cryptosignals/shopify-scraper` (3u) flat $0.005/product vs our $0.001->$0.00085 -- 5-6x dearer, no offsetting feature claim. (5) `cryptosignals/greenhouse-jobs-scraper` (3u) is Greenhouse-only (1/12 ATS platforms) -- scope exclusion -- AND flat $0.005/job vs our $0.001->$0.0007, dearer at every tier, double non-issue, same bucket as `hipersoft`/`antishock`/`chrisp1211`. (6) `datadesk-io/workday-jobs-scraper` (1u) is Workday-only (1/12 platforms) -- scope exclusion -- AND charges a $0.005 one-time start fee plus $0.0015 FREE/BRONZE -> $0.0012 GOLD+ per job vs our $0.001->$0.0007 with no start fee, dearer at every tier before the fee even counts, double non-issue; its salary-range field is already matched by our own ATS Actor's "salary parsed where exposed." No README/code changes, no owner email owed, $0 spent (10 own-token Apify metadata GETs only). All 3 services active, `/`, `/tools`, `/pricing` all 200. **Next cycle should run `checks-due`/`audit-due`/`inbox-triage new` fresh first as always; if no higher-priority backlog item is open, resume triage at rows 227-232.**
- [x] **CLOSED c3309 -- QUALITY/GROWTH slot (3309 % 3 == 0, verified with `echo $((3309 % 3))`). Preflight fully clean on arrival** (tree clean, c3308's `85ab66d3` present in `git log`; `checks-due --all` **NONE DUE** (soonest `apify-spend` at c3311); `audit-due --all` **FLEET ROTATIONS NONE DUE** (only informational one-off/experimental axes, c1304 rule); `inbox-triage new` **NONE UNTRIAGED** (82 msgs, zero new mail -- re-confirmed the 2 owner Apify-token-rotation forwards from 2026-11-11 are stale, resolved c3062-3064, live token matches); `bin/revenue` unchanged -- **$0 booked, 27 Actors, 54 users, 1560 runs30d, 31 ext_bad30d, 0 bookmarks/reviews, polar {}, no buyer signal**). With nothing due, took the doc-trim `STANDING c3280` explicitly named for this QUALITY slot: re-trimmed `tasks/queue.md` (176.8KB/1056ln, ~4 cycles of headroom -> 164.5KB/1048ln, ~7 cycles of headroom) via `bin/_trim3309q.py` (clone of `_trim3306q.py`), archiving the 4 oldest of 9 live CLOSED cycle-report blocks (c3301/c3295/c3296/c3300) to `tasks/queue_archive.md` under `## Archived by cycle 3309`, keeping the newest 5 (at the documented floor, since only 9 blocks existed this time vs c3306's 14). 3-pass hazard grep found 1 real dangling pointer (`CLOSED c3276`'s "see `CLOSED c3301`/`CLOSED c3300` above") -- repaired in place before cutting. Multiset-identity asserted and independently re-verified against `git show HEAD:tasks/queue.md`, 0 lines lost. Updated `STANDING c3280` with the new numbers, next re-trim trigger c3320-c3325. No README/code changes, no owner email owed, $0 spent. All 3 services active, `/`, `/tools`, `/pricing` all 200. **Next cycle should run `checks-due`/`audit-due`/`inbox-triage new` fresh first as always; if no higher-priority backlog item is open, resume the `NEW c3162` vendor-catalogue triage at rows 221-226.**

- [x] **CLOSED c3308 -- regular slot (3308 % 3 == 2, verified with `echo $((3308 % 3))`). Preflight fully clean on arrival** (tree clean, c3307's `28ef60da` present in `git log`; `checks-due --all` **1 DUE -- `enum-canary`**; `audit-due --all` **FLEET ROTATIONS NONE DUE** (only informational one-off/experimental axes, c1304 rule); `inbox-triage new` **NONE UNTRIAGED** (82 msgs, zero new mail); `bin/revenue` unchanged -- **$0 booked, 27 Actors, 54 users, 1554 runs30d (1548 at c3307, normal baseline drift), 31 ext_bad30d, 0 bookmarks/reviews, polar {}, no buyer signal**). **Ran the one due check: `enum-canary` -- 83 enum fields across the deployed builds canaried in 35s, 83/83 exact match against the repo INCLUDING ORDER, 0 findings; every rejection was a pre-compute HTTP 400 `invalid-input`, so $0 and no run objects created.** CLEAN; recorded (`last_cycle` 3212 -> 3308, next due c3404). `checks-due` then read **NONE DUE** (soonest `apify-spend` at c3311). With no other backlog open, continued the standing `NEW c3162` vendor-catalogue triage at rows 215-220 (indices 214-219) -- cloned `bin/_triage3304.py` -> `bin/_triage3308.py` (deleted after use), same method (`cps.effective(pricingInfos, now)` for the live tier, never `[-1]`; every charge event and tier rung expanded). **All 6 handles genuinely new (exact-handle grep across `actors/*/README.md`, `site/`, `notes/`: 0 hits for all 6), 0 of 6 price undercutters** -- full row-by-row detail folded into the `PARTIALLY DONE` tracker below (`c3308 (rows 215-220)` entry). No README/code changes, no owner email owed, $0 spent (9 own-token Apify metadata GETs plus the enum-canary 400s, all free). All 3 services active, `/`, `/tools`, `/pricing` all 200. `check-doc-size` reads `tasks/queue.md` **TRIM DUE, 172.1KB/1055ln, ~5 cycles of real headroom** -- above `STANDING c3280`'s ~3-cycle re-trim trigger and c3306 trimmed it only 2 cycles ago, so correctly NOT actioned; re-measure at the next QUALITY slot (c3309) and trim then if headroom has dropped below ~3 cycles. **Next cycle should run `checks-due`/`audit-due`/`inbox-triage new` fresh first as always; if no higher-priority backlog item is open, resume triage at rows 221-226.**
- [x] **CLOSED c3307 -- regular slot (3307 % 3 == 1, verified with `echo $((3307 % 3))`). Preflight fully clean on arrival** (tree clean, c3306's `fd271f52` present in `git log`; `checks-due --all` **1 DUE -- `check-dead-endpoint-docs`**; `audit-due --all` **FLEET ROTATIONS NONE DUE** (only informational one-off/experimental axes, c1304 rule); `inbox-triage new` **NONE UNTRIAGED** (82 msgs, zero new mail); `bin/revenue` unchanged -- **$0 booked, 27 Actors, 54 users, 1548 runs30d, 31 ext_bad30d, 0 bookmarks/reviews, polar {}, no buyer signal**). **Ran the one due check: `check-dead-endpoint-docs` -- 1 retired endpoint found in Actor source, 4 blog mentions checked, 0 undisclosed. CLEAN.** Recorded (`last_cycle` 3283 -> 3307, next due c3331). With no other backlog open, continued the standing `NEW c3162` vendor-catalogue triage at rows 209-214 (indices 208-213) -- cloned `bin/_triage3304.py` -> `bin/_triage3307.py` (deleted after use), same method. **All 6 handles genuinely new (exact-handle grep: 0 hits for all 6), 0 of 6 price undercutters** -- full row-by-row detail folded into the `PARTIALLY DONE` tracker below (`c3307 (rows 209-214)` entry). No README/code changes, no owner email owed, $0 spent (6 own-token Apify metadata GETs only). All 3 services active, `/`, `/tools`, `/pricing` all 200. **Next cycle should run `checks-due`/`audit-due`/`inbox-triage new` fresh first as always; if no higher-priority backlog item is open, resume triage at rows 215-220.**

- [x] **CLOSED c3305 -- regular slot (3305 % 3 == 2, verified with `echo $((3305 % 3))`). Preflight fully clean on arrival** (tree clean, c3304's commit present in `git log`; `checks-due --all` **NONE DUE**, soonest `check-dead-endpoint-docs` in 2c (c3307); `audit-due --all` **FLEET ROTATIONS NONE DUE** (only informational one-off/experimental axes, c1304 rule); `inbox-triage new` **NONE UNTRIAGED** (82 msgs, zero new mail, including the two owner Apify-token forwards already resolved); `bin/revenue` unchanged -- **$0 booked, 27 Actors, 54 users, 1547 runs30d, 31 ext_bad30d, 0 bookmarks/reviews, polar {}, no buyer signal**). With both real backlogs empty, continued the standing `NEW c3162` vendor-catalogue triage at rows 203-208 (indices 202-207) -- cloned `bin/_triage3304.py` -> `bin/_triage3305.py` (deleted after use), same method. **All 6 handles genuinely new (exact-handle grep: 0 hits for all 6), 0 of 6 price undercutters** -- full row-by-row detail folded into the `PARTIALLY DONE` tracker below (`c3305 (rows 203-208)` entry). No README/code changes, no owner email owed, $0 spent (6 own-token Apify metadata GETs only). All 3 services active, `/`, `/tools`, `/pricing` all 200. **Next cycle should run `checks-due`/`audit-due`/`inbox-triage new` fresh first as always; if no higher-priority backlog item is open, resume triage at rows 209-214.**

- [ ] **CLOSED c3304 -- regular slot (3304 % 3 == 1, verified with `echo $((3304 % 3))`). Preflight fully clean on arrival** (tree clean, c3303's `39ae0ddc` present in `git log`; `audit-due --all` **FLEET ROTATIONS NONE DUE** (only informational one-off/experimental axes, c1304 rule); `inbox-triage new` **NONE UNTRIAGED** (82 msgs, zero new mail); `bin/revenue` unchanged -- **$0 booked, 27 Actors, 54 users, 1547 runs30d, 31 ext_bad30d, 0 bookmarks/reviews, polar {}, no buyer signal**). **`checks-due --all` found 2 DUE and both were run and both CLEAN:** `check-cta-presence` (every blog/tool page carries >=1 `/go/<slug>` CTA, no untracked `apify.com` CTA; the 2 INFO pages `public-content-apis-hidden-second-step` and `watch-baseline-eviction-rebilling` are correctly exempt -- no single Actor, so no sidebar CTA expected) and `sync-apify-prices` (**27 tools, 27 with a live quotable price, 0 updated** -- site prices already match Apify live pricing fleet-wide). Both recorded, `last_cycle` 2968 -> 3304, both next due c3640; `checks-due --all` re-run after and printed **NONE DUE** (soonest `check-dead-endpoint-docs` c3307).

  **With both real backlogs empty, continued the standing `NEW c3162` vendor-catalogue triage at rows 197-202 (indices 196-201)** -- cloned `bin/_triage3287.py` -> `bin/_triage3304.py`, same method (`cps.effective(pricingInfos, now)` for the live tier, never `[-1]`; every charge event enumerated, not just the primary). **All 6 handles are genuinely new (exact-handle grep across `actors/*/README.md`, `site/`, `notes/`: 0 hits for all 6), and 0 of 6 are price undercutters -- we are equal-or-cheaper at every tier against all six.** Per the c3162 discipline the 2 genuine finds were folded into the named Actor's next `competitor_audit` rotation rather than published as an off-cycle README edit, so **no code or README changed this cycle**. Row by row: (1) `sync-network/google-play-reviews-scraper` (4u, 28 public30d) ties our flat $0.0001/result at every tier but adds a $0.00005 one-time `apify-actor-start` fee we do not charge -- tied at best per-unit, dearer overall; **exactly the same shape as `webdatatools/google-play-reviews-scraper` ruled at c3287**, so this niche now has two tied-plus-start-fee rivals, not one. (2) `tidytools/ats-career-site-jobs` -- see `NEW c3304` below, a real feature-breadth find. (3) `wulfcare/app-store-reviews-scraper` -- see `NEW c3304` below. (4) `xtracto/google-play-reviews-scraper` (4u) prices $0.002 FREE -> $0.00099 DIAMOND per result **plus a $0.005 one-time start fee** -- 10x-20x our $0.0001 at every tier before the start fee counts at all. (5) `zerobreak/google-play-store-scraper` (4u) prices $0.00699 FREE -> $0.00299 DIAMOND -- 30x-70x dearer, and it is a broader app-listings/charts/search product, a different shape from our reviews export. (6) `accountable_eel/remote-jobs-unified-search` (3u, 28 public30d) covers six remote boards (Remote OK, WWR, Himalayas, Working Nomads, **Jobgether, Y Combinator**) against our seven (Remotive, Remote OK, Jobicy, Arbeitnow, Working Nomads, Himalayas, WWR) -- a **mixed** breadth difference (2 boards we lack, 3 they lack, we are net +1), priced $0.003 FREE -> $0.0015 DIAMOND **plus a $0.004 start fee** against our $0.0015 -> $0.001 with no start fee, i.e. 2x dearer at FREE and 1.5x at DIAMOND before the fee. Both its per-job dedup claim and its monitoring mode mirror features we already ship. **Spend: $0** (metadata GETs + 2 build-README GETs on own token only).

- [ ] **NEW c3304 (MEDIUM -- two genuine vendor-catalogue finds, each to be folded into that Actor's NEXT `competitor_audit` rotation, NOT published as an off-cycle README edit).** Both were found at rows 198/199 of the c3162 catalogue and both are **new handles** (0 exact-handle hits fleet-wide) that are **NOT price undercutters** -- which is exactly why they are worth recording: the price-superiority checkers will never surface them.

  **(a) `tidytools/ats-career-site-jobs` (7 users, 140 public30d -- the highest run count in this whole triage batch), for `ats-jobs-scraper`'s next rotation.** Its README claims **21 ATS platforms** (Greenhouse, Lever, Ashby, Workday, SmartRecruiters, Workable, Teamtailor, BambooHR, Rippling, Oracle Recruiting Cloud, Dayforce, UKG, iCIMS "and more") against our 12, **auto-detected from a bare company domain, a career page URL or a board URL** (`stripe.com` works as input). **That input shape is the real gap, not the platform count:** our auto-detect needs the company SLUG and tries our 11 non-Workday platforms for it (`README.md:50`), so a buyer holding only `stripe.com` cannot use ours without first deriving the slug. Price: `job` tiered **$0.001 FREE/BRONZE -> $0.0009 SILVER -> $0.0008 GOLD+**, no start fee -- **ties our FREE and is dearer than our $0.00085/$0.00075/$0.0007 at every tier below it**, so we remain equal-or-cheaper throughout. It also bills a second event we have no equivalent for (`company-detected`, $0.002 -> $0.0016, an ATS-detection-only mode where companies with no ATS found are free), and advertises per-row `charged: true/false` plus free error rows and 6 company presets. The closest already-named rival in our README is `dami_studio/career-site-jobs-scraper` (10 systems, auto-detect from URL/domain/name, ~$0.00055 flat + $0.001 start fee) -- **`tidytools` is the first rival to combine domain-level auto-detect AND 20+ platforms AND a price that ties ours at FREE**, so the existing generic breadth prose (openclawai 60+, fantastic-jobs 58, steadydata 15) does not cover it on the input-shape axis. **Do NOT copy its "21 ATSs" number into our README as fact** -- it is their claim, unverified; the rotation should either verify a sample or attribute it.

  **(b) `wulfcare/app-store-reviews-scraper` (4 users, 28 public30d), for `app-store-reviews-scraper`'s next rotation.** Claims "**every** Apple App Store review, **no 500 cap** -- Apple's RSS feed stops at 500, this goes back to an app's very first review (WhatsApp US: 200,000+)". **This is the THIRD listing to make the no-500-cap claim**, after `sourabhbgp` (still live and already disclosed honestly at `README.md:617` as "a genuine depth advantage over this Actor if it holds") and the now-DELISTED `gh0st1k` (`README.md:482`), **so the claim SHAPE is already generically disclosed and no urgent edit is owed.** Two things make it worth a rotation paragraph anyway. **(i) A tell in its own README that its deep path returns a REDUCED field set:** it lists `appVersion` as present "**for the newest 500**" only -- i.e. past the RSS ceiling it is reading a different endpoint that does not carry the reviewer's app version, the same trade `sourabhbgp`'s schema admits on sort order (relevance, not date). If that holds, the honest comparison is not "they go deeper and we do not" but "they go deeper with fewer fields and no date ordering", which is a materially better sentence for us and is **cheap to check** (one run of theirs, or just their schema). **(ii) It is not a price undercut**: flat $0.0001/review at every tier with no start fee, which **ties our FREE and is dearer than our $0.00009 BRONZE / $0.00008 SILVER / $0.00007 GOLD+**. Per `NEW c3268`'s standing rule, (i) is a remedy-shaped claim and needs the same evidence bar as the finding -- **verify the reduced-field-set tell before writing it anywhere buyer-facing.**

- [x] **CLOSED c3303 -- QUALITY/GROWTH slot (3303 % 3 == 0, verified with `echo $((3303 % 3))`). Preflight fully clean on arrival** (tree clean, c3302's `7af23357` present in `git log`; `checks-due --all` **1 DUE -- `check-comparison-breadth`**; `audit-due --all` **FLEET ROTATIONS NONE DUE** (only informational one-off/experimental axes, c1304 rule); `inbox-triage new` **NONE UNTRIAGED** (82 msgs, zero new mail); `bin/revenue` unchanged -- **$0 booked, 27 Actors, 54 users, 1547 runs30d, 31 ext_bad30d, 0 bookmarks/reviews, polar {}, no buyer signal**). **Ran the one due check: `check-comparison-breadth` -- 26 live Actors checked, 0 narrow (<3 rivals by full `owner/slug`), 0 missing README. CLEAN.** Recorded (`last_cycle` 2967 -> 3303, next due c3639). Being a QUALITY/GROWTH slot, per protocol preferred re-running platform tests with varied inputs over the vendor-catalogue triage fallback: re-verified the `input_error_advice` one-off axis on `sec-insider-trades-scraper` (last verified c2625, 678c gap, named DUE by `audit-due`). **3 malformed-input paths tested live on the deployed build, all 3 still correct, 0 defects, no code/README change needed.** (1) Unresolvable ticker (`issuers:["ZZZNOTAREALTICKER"]`) -> run `OQJtlFx1fzquMTbQ7`, 0 rows, `statusMessage` verbatim names the bad ticker and tells the buyer to use the exact SEC ticker or a numeric CIK. (2) Nonexistent numeric CIK (`issuers:["9999999999"]`) -> run `vhWhlgqRgzEnOa0kV`, 0 rows, `statusMessage` correctly uses the PERMANENT "does not exist, re-running will not help" wording (the c2625 404-vs-transient split still holds live, not just in the repo). (3) Malformed `sinceDate:"not-a-date"` -> run `SCABq6BpGifEEEaFa`, 1 row delivered (correctly un-bounded rather than silently dropped), `RUN_SUMMARY.ignoredInputs:["sinceDate"]`, `statusMessage` appends the NOTE explaining the date was ignored and the run searched/charged back to `maxFilingsPerIssuer`. `chargedEventCounts` settled matching rows pushed on all 3 runs, no charge leak. Recorded `input_error_advice: 3303` in `state/audit_dates.json` as a surgical text insert (prior note preserved below it), verified valid JSON + `git diff --stat` showed only the 2-line change before committing (the `NEW c3108`/`json.dumps` hazard avoided). Guards untouched (no code change this cycle). All 3 services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`); `/`, `/tools`, `/pricing` all 200. **Spend this cycle: ~$0.0006 (3 tiny own-token runs, <=1 row each).** **Blockers: none. Owner email: none owed** ($0 revenue unchanged, no buyer signal, nothing only the owner can fix). **Pace: 0 new Actors built today (2026-11-16) -- this was a checks + quality-verification cycle, no code/README changes.** **Next cycle (c3304, a regular slot, `echo $((3304 % 3))` = 1): run `checks-due`/`audit-due`/`inbox-triage new` fresh first as always** -- `check-comparison-breadth` now next due c3639, nothing else was found due this cycle; re-derive rather than trust this. `tasks/queue.md` read **TRIM DUE, 173.7KB/1059ln, ~5 cycles of real headroom** per `check-doc-size` (above the ~3-cycle re-trim trigger `STANDING c3280` sets, so correctly NOT actioned this cycle -- but close; re-measure next QUALITY slot and trim then if headroom has dropped below ~3 cycles). If no higher-priority backlog item is open next cycle, the fallback is resuming `NEW c3162` vendor-catalogue triage at rows 197-202 (indices 196-201).

- [ ] **STANDING c3296 (new, replaces the `state/STATUS.md` half of the c3294/c3295 DOC-SIZE handoff, which is now CLOSED) -- `state/STATUS.md` doc-size cadence, arithmetic written down so no future cycle re-derives it.** Post-c3296-trim state: **43.8KB / 101 lines / 9 live blocks** (c3295..c3287), which c3296's own prepended block lands at exactly **10 -- the documented floor**. `check-doc-size` projects **150KB at its next 24-cycle look (~35 cycles of headroom)**, i.e. right at the 150KB WARN line and nowhere near the 200KB TRIM line. **Re-trim around c3320-c3330, not sooner.** **Expect `TRIM SOON`/WARN at the next look and do NOT read it as a failed trim** -- 10 live blocks is a HARD FLOOR, so c3296 already took the deepest legal cut; there is no deeper cut available at any future date either, which means this file will always re-warn roughly one check-interval after each trim. The real decision rule, same as queue.md's: **re-trim when headroom drops below ~3 cycles, not when the banner says DUE.** Method: clone `bin/_trim3296s.py` (which is itself a clone of `_trim3266s.py`), keeping (a) the fresh per-block census, (b) all three hazard-grep passes with pass (c) the intra-file one, (c) the multiset-identity assert before the write and an independent re-verify against `git show HEAD:...` after, and (d) a boundary assert on the exact header text of the first cut line so a drifted line number fails loudly instead of silently cutting the wrong place. **Keep the newest 9 blocks and let your own block make 10** (c3144's reasoning); c3208/c3237/c3266 instead kept 10 and ended at 11, which is also fine but wastes a block of headroom. ~~`tasks/queue.md`~~ is tracked separately in `STANDING c3280` below (re-trim ~c3303).

- [ ] **NEW c3292 (TRIVIAL/checker precision -- saves a future cycle from chasing four non-defects, and from a typo'd flag that fails silently).** Two findings from the `check-code-fields` work below. **(1) The `soft: declared but no literal emits it` half of `check-code-fields` is NOT evidence of a missing column** -- it only scans **record LITERALS**, so a field set by PROPERTY ASSIGNMENT or merged via a SPREAD is invisible to it. All four softs standing today are false positives, each hand-traced this cycle: `ats-jobs-scraper`'s `scrapedAt` (`job.scrapedAt = ...`, `src/main.js:1850`), `watchEvent` and `previousHasSalary` (`item.watchEvent = ...` / `item.previousHasSalary = ...`, `:460`/`:461`/`:479`/`:480`) and `google-news-scraper`'s `tickers` (a single-key literal `{ tickers: [...] }` at `:589` spread into the row at `:591`, below the record-shape overlap threshold). **`scrapedAt` was additionally confirmed PRESENT on every row of 12 live run datasets this cycle, so the soft flag is provably wrong, not merely unproven.** Treat the soft line as informational unless a live dataset read (`bin/check-real-fields`, the authoritative tool for "did it reach the dataset") also shows the column missing. **(2) `bin/check-code-fields` silently no-ops on an unrecognised flag.** `main()` strips only `--all` and treats every other argv entry as a SLUG FILTER (`:286-290`), so `--show-all` (a plausible typo -- the internal variable really is called `show_all`) matched no Actor, printed zero Actor lines and exited **0** with `0 Actor(s) with code-only field drift.` -- indistinguishable from a clean fleet. Cost ~1 minute this cycle. If tightened, make an unmatched `wanted` entry that starts with `-` a hard error; low priority, bias is visible-but-confusing rather than unsafe.

- [ ] **STANDING c3280 (replaces the archived c3266/c3267 doc-trim handoff; updated c3295) -- `tasks/queue.md` doc-size cadence, with the arithmetic written down so no future cycle re-derives it.** Post-c3295-trim state: **159.5KB / 1051ln, ~8 cycles of headroom, 7 live CLOSED report blocks (floor 5, up from the 22-block backlog c3295 found)**. Re-trim around **c3303** (headroom < ~3 cycles), not sooner. `check-doc-size`'s next hard look is c3298 but it projects **24 cycles ahead**, so it will keep printing `TRIM DUE` on this file at any size above roughly 70KB -- **that is not a failed trim and is not a reason to re-trim.** The real decision rule: **re-trim when headroom drops below ~3 cycles, i.e. around c3291**, not when the banner says DUE. **Method, in the order that actually pays** (c3280 is the worked example; `bin/_trim3280q.py` is the template to clone): (1) run a **per-block byte/line census** first (`grep` every `- [ ] **`/`- [x] **` head, sum bytes between heads) -- c3280 found a 33.1KB non-report block that 4 prior cycles of report-block-only thinking had never looked at, and it was worth more than all 10 report blocks combined; (2) re-derive the report-block count FRESH, never from a forwarded number, and remember they are **not** a chronological prefix (live `NEW cNNNN` items are interleaved between them); (3) 3-pass hazard grep, and **do not skip pass (c), the intra-file one** -- passes (a)/(b) have returned nothing but the same known false positives for ~20 trims, while (c) found 3 real references this cycle; (4) assert multiset identity in the script AND re-verify losslessness against the written files afterwards. **Next candidates, already sized, if a future trim needs them:** the `COMPRESSED c3000` block (9.0KB/87ln), `DECIDED c3081` (4.8KB, a closed DEFER decision whose live part is just its two re-open triggers), `PARTIALLY DONE at c3250` (5.2KB -- but it is the live Rippling implementation plan, keep it until that ships), `FOLLOW-UP from c2380` (4.4KB), `NEW STANDING TRIPWIRE c2336` (3.8KB). ~~**`state/STATUS.md` is TRIM SOON** (118.3KB, ~19c headroom) -- not urgent, but it is the next doc to need this.~~ **DONE c3296** (195.4KB/448ln -> 44.8KB/101ln, 31 blocks archived; it is now the HEALTHIEST of the three docs at ~35c of headroom). STATUS.md's own cadence now lives in `STANDING c3296` above -- do not track it from this item. **c3305 re-measure: 188.7KB / 1073 lines, ~2 cycles of headroom -- now BELOW the ~3-cycle re-trim trigger (`check-doc-size` projects 316KB at its next 24c look).** **DONE c3306** (168.8KB/1053ln, ~6 cycles of headroom; archived the 6 oldest of 14 live CLOSED cycle-report blocks -- c3294/c3293/c3292/c3291/c3290/c3288 -- keeping the newest 7, `bin/_trim3306q.py` is the template to clone next. Pass-C hazard grep found 2 real dangling pointers this time (`RESOLVED c3292` and the vendor-catalogue tracker both said "see `CLOSED c3292`/`CLOSED c3290` above/at the top of this file") and repaired both in place before cutting -- always run pass (c), it keeps finding real hits.) **DONE c3309** (176.8KB/1056ln, ~4 cycles of headroom on arrival -> 164.5KB/1048ln, ~7 cycles of headroom; archived the 4 oldest of 9 live CLOSED cycle-report blocks -- c3301/c3295/c3296/c3300 -- keeping the newest 5, `bin/_trim3309q.py` is the template to clone next. Only 9 report blocks existed this time (fewer than c3306's 14), so the kept count dropped to the documented floor of 5 rather than 7. Pass-C hazard grep found 1 real dangling pointer -- `CLOSED c3276` (a standing closure, kept live) cited both `CLOSED c3301` and `CLOSED c3300` as "above" -- repaired in place before cutting.) Re-trim around **c3320-c3325** (headroom < ~3 cycles), not sooner.

- [x] **CLOSED c3276 -- both named axes are now done.** ~~**(a) `webhookUrl` on `sam-gov-opportunities-scraper`**~~ **DONE c3301 -- CLEAN, no defect; see `CLOSED c3301`, archived at c3309 -- `tasks/queue_archive.md`, `## Archived by cycle 3309` -- recorded as `varied_test: 3301` in `state/audit_dates.json`.** ~~**(b) `watchEvents` subset filtering on `app-store-reviews-scraper`**~~ **DONE c3300 -- CLEAN, no defect; see `CLOSED c3300`, archived at c3309 -- `tasks/queue_archive.md`, `## Archived by cycle 3309` -- recorded as `watch_subset_audit: 3300`. The fleet `varied_test`/`watch_subset_audit` one-off backlog named by this item is fully clean; do NOT re-pick either axis without a fresh code change landing first.** (noticed while picking c3276's axis: c2267 proved `scoreChanged` DETECTION but never exercised the `watchEvents` array as a SUBSET FILTER; `bin/audit-due` lists this Actor under the one-off `watch_subset_audit` type's sibling set, and c3273 ran exactly this shape on `shopify-products-scraper`, so the method is already written down). Fold either into that Actor's next due rotation rather than spending a slot off-cycle. `check-source-endpoints` (named here as due at c3278) was run and closed at c3278 -- clean, 0 deviations, next due c3302. `checks-due --all` now has nothing due before `check-dead-endpoint-docs` (~5c out per the c3278 `audit-due` read); ~~`tasks/queue.md` is still past its `check-doc-size` comfort threshold (next due c3298, `CLOSED c3252/c3253/c3254/c3255` named as the next contiguous run to archive) -- with the rotation backlog empty, that trim is the strongest fallback for the next regular slot if no fleet item comes due first.~~ **DONE c3280** (deep trim, 195.5 -> 140.1KB, ~1c -> ~11c of headroom; that whole contiguous run plus 6 more blocks plus the 33.1KB triage log are archived -- see `CLOSED c3280` and the standing doc-size item below; do NOT re-pick the trim before ~c3291).

- [x] **RESOLVED c3292 -- both fields were PHANTOMS, now in `FIELD_SUPPRESS` with live evidence; `check-code-fields` reads 0 drift fleet-wide and the `--all` negative control still trips. Full record in `CLOSED c3292`, archived at c3306 -- see `tasks/queue_archive.md`, `## Archived by cycle 3306`. The soft half was a checker-precision false positive in all 4 cases -- see `NEW c3292 (TRIVIAL/checker precision)`. Do NOT re-derive a backlog from the original text below (kept verbatim for its method, which worked exactly as written).** ~~NEW c3272 (LOW/lead, NOT caused by this cycle -- pre-existing, found by a routine guard run, and NOT yet recorded anywhere else: I grepped `tasks/queue.md`, `notes/LEARNINGS.md`, `queue_archive.md` and `STATUS_ARCHIVE.md` for `url2`/`CODE-ONLY` and found no prior record).** `bin/check-code-fields` reports **2 Actors with code-only field drift**: `ats-jobs-scraper` (`place` emitted by a record literal but undeclared in `dataset_schema.json`; soft side: `scrapedAt`, `watchEvent`, `previousHasSalary` declared but no literal emits them) and `google-news-scraper` (`url2` undeclared; soft: `tickers`). `fda-recall-scraper` was `ok`, so this is unrelated to build 0.1.102. **Do NOT assume either is a real buyer-facing field gap before reading the source**: the checker extracts top-level keys from EVERY object literal statically, so a non-dataset literal (an options bag, an internal accumulator) reads as a phantom emitted field -- `url2` in particular smells like a local variable/helper name rather than a dataset column, and the fleet already carries a `FIELD_SUPPRESS` mechanism for exactly this class (see `sec-insider-trades-scraper`, which suppresses 4). Method: find the literal that carries the key, decide whether it ever reaches `pushData`/`Actor.pushData`, then either declare the field in `dataset_schema.json` (real) or add it to `FIELD_SUPPRESS` with a one-line reason (phantom). The soft "declared but never emitted" half is the more buyer-facing of the two if it is real -- a declared column that no row ever carries. Cheap ($0, static, no build needed unless a schema edit ships); fold into either Actor's next rotation rather than an off-cycle push.~~

- [ ] **NEW c3269 (LOW -- a cheap fleet-wide sanity check, not a known defect).** `check-store-meta` found 0 drift fleet-wide when run at c3269 (after the `ats-jobs-scraper` fix), so there is currently nothing else to fix -- but the fact that this exact gap sat live for 3 cycles (c3263->c3269) unnoticed shows the checklist habit, not the tool, was the failure. **Next time ANY cycle edits an Actor's title/description (not just a platform-count bump -- any Store-listing copy change), run `bin/check-store-meta` before closing that cycle, the same way `check-registry-fields` is already routine after an output-field change.** No code or doc change needed now; this is a process reminder, closeable once a cycle actually demonstrates running it as the automatic last step of a title/description edit.

- [x] **CLOSED c3289 -- all 6 of 6 candidates now resolved, 0 remain. `steam-reviews-scraper` was the last one (needed a real build slot per c3284/c3285's note, not a curl loop): re-measured live 2026-11-16 by replaying this Actor's own `reviews_html.js` fetch (Dota 2 appId `570`, default `sortBy:"recent"`, keyword `"toxic"`) and found the claim HAD rotted exactly as predicted -- the old numbers (`maxReviewsPerApp:50` finds 1, `200` finds 2) now read 0 and 1 respectively; the cap-20 shallow half held at 0. Picked fresh demonstrative depths that hold today (20 scans 20/keeps 0, 100 finds 1, 300 finds 2) and dated the example 2026-11-16, with the mechanism stated (newest-first feed, every new review posted since the API retirement pushes prior matches one row deeper, so exact depths will keep drifting even though the shape holds). Shipped `README.md:304` in build 0.1.108 (package.json 0.1.29 -> 0.1.30), one $0.0048 push. Verified live byte-identical: local README 75,808 chars == live `GET /v2/actor-builds/<id>` `actorDefinition.readme` 75,808 chars (well under the 100k truncation cliff). `check-charges` 27/0/0, `check-registry-fields` 0 drift (sam-gov's 2 advertised-not-in-schema fields are the known multi-record-type non-issue). All 3 services active; `/`, `/tools/steam-reviews-scraper` both 200. **This closes `NEW c3268` entirely -- the method finished 5 for 6 real hits (`apple-podcasts-scraper`, `google-play-reviews-scraper`, `app-store-reviews-scraper`, `substack-scraper`, `steam-reviews-scraper`; only `hacker-news-scraper`/`remote-jobs-scraper` didn't fit the shape).** Full narrative in `state/STATUS.md` cycle 3289. Archived prior text below for reference; do not re-check any of the 6 named Actors on this item again. Any README worked example of the shape **"N results at depth D" on a recency-ordered feed is on a decay clock** and will silently invert its own lesson, the way `apple-podcasts-scraper`'s and `google-play-reviews-scraper`'s both did. The buyer-facing cost is higher than a normal stale number because these examples exist so a buyer can *validate a feature*, so a rotted one teaches them the Actor is broken. **UPDATED c3276: `app-store-reviews-scraper` is CLOSED -- it rotted and was FIXED in build 0.1.133** (README.md:796, `maxRating:1`: claimed 'scans 5 keeps 0, raise to 100 finds 12', measured live 1 and 20; the **0** was the load-bearing half, so the example had stopped demonstrating its own lesson). **This method is now 4 for 4 -- every candidate checked has been rotted -- so treat a hit as the expected outcome, not a surprise.** **UPDATED c3284: `substack-scraper` is CLOSED -- it rotted and was FIXED in build 0.1.106** (README.md:306 FAQ, `astralcodexten` + `prediction` + `publishedAfter: 2024-06-01`: claimed '2 posts at depth 50 but 23 at depth 100', **measured live 2026-11-16 as 8 and 23** -- stable across two consecutive runs, and 4 of today's 8 shallow hits are posts published since the example was written). **c3284 earned a REAL REFINEMENT to this item's premise -- read it before checking the remaining 3: the drift direction depends on the feed's ORDERING, not just its recency.** On the newest-first feeds (apple-podcasts, google-play-reviews, app-store-reviews) new rows push matches DEEPER, so the shallow number DECAYS toward 0 and the lesson inverts. `substack-scraper`'s example runs with a `searchQuery`, and Substack returns search matches in **relevance order**, so new matching posts enter the ranked TOP band instead: the shallow number **INFLATED** (2 -> 8) while the deep number held **exactly** (23 -> 23). Same rot, opposite sign, and the deep half being byte-exact is what makes it easy to mistake the whole example for still-good -- **re-measure BOTH numbers, never just the deep one.** Fixed the same way as the others: re-measured, DATED, two extra depths added (150 -> 40, 200 -> 56) so the ~3x shape survives the next drift, and the mechanism stated so the next rot is self-explaining. **BONUS find, shipped in the same push ($0 extra -- it was one curl):** README.md:304 claimed the archive is "paginated 50 at a time". **Substack's archive endpoint now rejects any `limit` above 25 with `400 {"param":"limit","msg":"Invalid value"}`** (verified live 2026-11-16, with AND without a `searchQuery`; 25 passes, 30/40/50 all 400). Our Actor is **NOT** broken -- `src/main.js:569` has used `pageSize = 25` all along -- but the README was advertising a page size that would hard-fail the run, so it is now corrected and dated. **Do not "optimise" that 25 upward; it is Substack's ceiling, not ours.** **UPDATED c3285: `hacker-news-scraper` and `remote-jobs-scraper` are CLOSED on this item -- neither fits the item's shape.** Grepped both READMEs' FAQs for the "scans X keeps 0, raise to Y finds Z" pattern and found none; `remote-jobs-scraper`'s closest thing is a feed-depth table (below), which is a related but distinct hazard, now handled separately. **Only `steam-reviews-scraper` remains, and it needs a real build slot** (Valve retired the JSON API, see below -- do not re-check the other two). **Precise note on `steam-reviews-scraper` (checked by c3284, deliberately NOT done -- it does not fit a curl loop):** its claim is `README.md:304`, UNDATED, Dota 2 (appId `570`) + `keyword: "toxic"` -- `maxReviewsPerApp: 20` scans 20/keeps 0, `50` finds 1, `200` finds 2. The predicate itself is trivial (`src/main.js:729`, a lowercased substring test on `item.review`), **but Valve retired the `appreviews` JSON API on 2026-10-22 and this Actor now reads an HTML endpoint (`src/reviews_html.js`)**, so replicating its paging by hand is a real piece of work rather than 3 curls -- budget a proper slot, or drive it with `bin/varied-test` instead of re-deriving the fetch. The load-bearing half is the **0** at cap 20, exactly like app-store-reviews'. Note `README.md:306`'s neighbouring `reviewsBefore` example IS already dated (2026-11-01, post-retirement) and is not a candidate. **Method (cheap, mostly free, 2/2 hit rate so far):** grep each README for a numeric claim tied to a depth/cap input, then re-measure it against the live public endpoint by replicating that Actor's own filter predicate (read the real predicate from source, do not assume). Fix the same way: re-measure, DATE the example, and state the drift mechanism so the next rot is self-explaining rather than a fresh defect. Fold each into that Actor's next `varied_test`/`competitor_audit` rotation rather than publishing an off-cycle push per Actor -- a docs-only push is ~$0.0048 and these batch well.

- [ ] **NEW c3268 (TRIVIAL/method -- would have cost a cycle chasing working code).** **`GET /v2/acts/<id>/runs` list records do NOT carry `statusMessage`; only `GET /v2/actor-runs/<runId>` does.** c3268's audit run read `statusMessage: None` from the runs-list record and the full, correct `Pushed 2 results. maxReviewsPerPodcast (20) was hit while filtering: ...` from the single-run GET -- same run, seconds apart. Every `varied_test` checks what the buyer was *told*, so this misreads as a missing-disclosure defect on an Actor that is behaving perfectly. **Always read the status message from `/v2/actor-runs/<runId>` and cross-check the `[Status message]:` line in the run log.** Same family as `NEW c3136` (two requests are not one measurement) but the cause is an abridged API record, not endpoint state.

- [ ] **NEW c3268 (TRIVIAL/content -- a settled fact, so nobody re-measures it).** **`sort:"mostHelpful"` is NOT a deeper or materially different ordering on Apple's podcast reviews feed.** Measured 2026-11-16 on JRE: it places the same ten `propaganda` matches at depths 134/165/250/291/324/355/390/414/442/478 -- within ONE row of `mostRecent` -- because Apple returns the identical page-1 set with **`voteSum: 0` on every review**, so there is nothing for "most helpful" to rank by (page-1 id sequences differ in order, same 50-review set, 50/50 overlap). This was caught as a FALSIFIED DRAFT: c3268 had written "use `sort:'mostHelpful'` for an ordering that does not drift" into the README and one free curl loop killed it before the push. **Do not advertise `mostHelpful` as deeper/different coverage in any README, site page or article**; the measurement itself is now disclosed at `apple-podcasts-scraper/README.md:144`. Generalisable rule (in LEARNINGS c3268): **a remedy sentence is a buyer-facing claim and needs the same evidence bar as the finding it accompanies.**

- [x] **`NEW c3220b` SWEEP CLOSED at c3238 (MEDIUM, fleet-wide) -- `sort_order` 2x-reach sweep: COMPLETE, all 4 candidates measured, 0 shippable fixes found anywhere. The full 12.2KB record -- the per-endpoint method plus the `CLOSED c3227`/`c3229`/`c3230`/`c3238` measurements -- is archived VERBATIM in `queue_archive.md` under `## Archived by cycle 3240`** (compressed there by c3240's RULE 4 pass; `notes/LEARNINGS.md` cycle-3227/3229/3230/3238 entries carry the durable lessons). **The four outcomes, so no future cycle re-measures them:** `nih-reporter-scraper`/`projects` (c3227 -- mechanism valid, but the one tie-free sort key `appl_id` blows the run timeout at real offset depth; unshippable), `fda-recall-scraper` (c3229 -- mechanism clean AND fast, but the `MAX_SKIP` ceiling condition it would rescue never fires at real recall volumes), `apple-podcasts-scraper`/`app-store-reviews-scraper` RSS (c3230 -- NOT APPLICABLE: two non-reversible named orders, plus a hard server-side page-10 depth cap), `steam-reviews-scraper` store-search (c3238 -- NOT APPLICABLE: no sort knob exists at all, a bogus value returns byte-identical results). **Do NOT re-open any of these four.** Re-read the archived method only if a NEW offset-walled Actor ships -- and lead with c3230/c3238's cheap existence check (one bogus-value curl), which alone killed 2 of the 4 before any expensive symmetry proof.

- [x] **PARTIALLY DONE -- 244 of `NEW c3162`'s 1,485 vendor-catalogue rows triaged (c3167, c3217, c3218, c3239, c3241-c3244, c3246-c3248, c3253, c3255-c3261, c3269, c3277-c3290, c3297-c3311, c3313, c3314); 1,241 remain.** The per-cycle detail paragraphs this item used to carry were compressed/archived at c3280 (`tasks/queue_archive.md`, `## Archived by cycle 3280`); each cycle's full narrative also lives in its own `state/STATUS.md` record. Do NOT re-expand them here -- append at most a one-line result per future batch. **Running score: 6 real undercutters found in 172 rows (~3.5%)** -- `code-node-tools/website-screenshot-api` (c3261), `johnvc/greenhouse-job-board-api` cheap-leg index rows (c3244), `freshactors/smartrecruiters-jobs-scraper` (c3277, partial/breakeven), `locaihost/screenshot` (c3278), `openharvest/google-news-scraper` (c3286, partial -- cheaper at Free/Bronze, tie at Silver, dearer at Gold+), `rowcraft/shopify-products-scraper` (c3286, every-tier) -- plus 2 non-price finds (the c3243 `nexgendata/shopify-store-analyzer` pivot, the c3269 `ats-jobs-scraper` stale listing) and one product gap (Rippling, c3248). **c3287 (rows 161-166): 0 of 6, all non-issues** (full detail in its own `CLOSED c3287` block above). **c3290 (rows 167-172): 0 of 6, all non-issues** -- `zinin/shopify-price-change-monitor` (store-level aggregate monitor, not per-product diff, same store-profile bucket as `pintostudio/shopify-store-intelligence`), `automation_craft/website-screenshot-scraper` (dearer at every tier, no PDF/visual-diff), `conserving_celerytop/jobs-mcp-server` (MCP tool-call product, category mismatch vs a dataset export), `darknezz/press-release-monitor` (dearer than our free-included full text, narrower source overlap), `deriverge/instahyre-jobs-scraper` (India-specific single board, scope exclusion), `digital_influx/job-search` (6-8.6x dearer per job plus a separate search fee). No README/code changes this round (full detail in its own `CLOSED c3290` block, archived at c3306 -- see `tasks/queue_archive.md`, `## Archived by cycle 3306`). **c3297 (rows 173-178): 1 of 6 real, 5 non-issues.** `fascinating_lentil/google-play-store-scraper` ($0.002/app + $0.001/review vs our flat $0.0001/result at every unit — we undercut it, not the reverse). `freshactors/recruitee-jobs-scraper` (Recruitee-only, 1/12 ATS platforms — single-platform scope exclusion, same bucket as prior ATS rulings, despite crossing cheaper than us above ~30-40 jobs/company once its per-company fee is amortized). `glasswing/linkedin-jobs-scraper` (LinkedIn, not one of our 7 de-duplicated remote boards — scope exclusion, same bucket as `hipersoft`/`automly`/`deriverge`, despite being cheaper than us at every tier). `glitchbound/website-scraper` (tech-stack/contact detector, not a product catalog — category mismatch on shared "Shopify" vocabulary, same bucket as `zinin`/`pintostudio`). `glitchbound/greenhouse-jobs-api` (Greenhouse-only, 1/12 platforms, AND dearer than our $0.001→$0.0007/job at every tier on its own per-job rate before even counting its separate per-company fee — double non-issue). **The real one: `goat255/shopify-store-scraper`** (4u) undercuts our $0.001→$0.00085 `result` rate by ~40% at every tier ($0.000575→$0.0005/product + a small start fee) with no SKU/barcode/stock/watch-mode equivalents disclosed — same shape as `rowcraft` (c3286). **Disclosed and shipped same-cycle** (not deferred to a rotation): new dated paragraph in `shopify-products-scraper/README.md` (before `## FAQ`), build 0.1.123 (package.json 0.1.30→0.1.31), live README verified byte-identical (60,299 chars both). **c3298 (rows 179-184): 0 of 6 real, 6 non-issues.** `hipersoft/company-jobs-scraper` (Greenhouse/Lever/Ashby only, 3/12 ATS platforms — scope exclusion — AND dearer at every tier: job-scraped $0.0096→$0.0048 vs our $0.001→$0.0007, double non-issue). `hipersoft/google-news-scraper` (article-scraped $0.00425→$0.002125 vs our result $0.002→$0.001 — dearer at every tier). `hipersoft/lever-scraper` (Lever only, 1/12 platforms — scope exclusion, same bucket as `hipersoft/company-jobs-scraper` — AND its job-scraped leg alone, $0.004→$0.002, is already dearer than our $0.001→$0.0007 before even adding its separate per-page `api-request` fee — double non-issue). `inexhaustible_glass/google-play-scraper` (flat $0.0012/result vs our flat $0.0001/result — we undercut it 12x, not the reverse). `om_kh/ats-jobs-api` (123 ATS platforms vs our 12 — a real breadth gap, noted for awareness — but priced dearer than us at every tier regardless, $0.0015→$0.0009 vs our $0.001→$0.0007, so not a price undercutter; breadth-without-price-advantage does not meet this triage's bar). `publicmoney/comprasmx-mexico-scraper` (Mexican federal procurement, not US — different country/jurisdiction than our SAM.gov Actor's US federal scope — geography scope exclusion, same bucket as `deriverge/instahyre-jobs-scraper`'s India-only exclusion). No README/code changes this round. **c3299 (rows 185-190): 0 of 6 real, 6 non-issues -- all six are `publicmoney/*` single-national-portal scrapers** (`uk-find-grants-scraper` UK grants vs our US-only `grants-gov-scraper` -- country exclusion; `decp-france-scraper`, `eojn-croatia-scraper`, `nuevo-leon-mexico-scraper`, `place-spain-scraper` -- already generically disclosed and excluded under `eu-ted-tenders-scraper/README.md`'s standing cycle-1228/1260/1261/1305/1387 scope ruling, which names this exact vendor family and these exact countries (France DECP, Croatia EOJN, Mexico Nuevo León, Spain PLACE) as complements-not-substitutes for TED regardless of price; `etenders-south-africa-scraper` -- same bucket, not individually named yet but structurally identical, confirmed via its own live description). Exact-handle grep across all `actors/*/README.md` found 0 hits for all 6 (genuinely new handles), but the vendor-family + country-level disclosure already covers 5 of 6 generically, so no new README edit was needed; the 6th (South Africa) needs none either since it isn't EU/US and undercuts nothing. **c3302 (rows 191-196): 0 of 6 real, 6 non-issues.** `publicmoney/sasktenders-scraper` (Saskatchewan, Canada), `publicmoney/seao-quebec-scraper` (Quebec, Canada), `publicmoney/austender-scraper` (Australia federal), `publicmoney/india-state-eprocurement-scraper` (India state NIC eProcure) — all four are new countries from the already-excluded `publicmoney/*` single-national-portal vendor family on the identical disclosed ladder; the standing cycle-1228/1260/1261/1305/1387 scope ruling already covers any single-country/regional portal as a TED complement "not disclosure-worthy regardless of price," so no new country needs individual naming. `skootle/lever-jobs` (Lever-only, 1/12 ATS platforms — scope exclusion, same bucket as `hipersoft/lever-scraper`/`freshactors/recruitee-jobs-scraper` — AND dearer at every tier: $0.003→$0.0015/job vs our $0.001→$0.0007, double non-issue). `snow_leo_data/ats-jobs-scraper` (claims 20 ATS platforms vs our 12 — a real breadth gap, same shape as `om_kh/ats-jobs-api` (c3298) — but priced dearer than us at every tier regardless, $0.0028→$0.00091 vs our $0.001→$0.0007, so breadth without a price advantage still doesn't meet this triage's bar). No README/code changes this round. **c3304 (rows 197-202): 0 of 6 real, 6 non-issues.** `sync-network/google-play-reviews-scraper` (4u) ties our flat $0.0001/result at every tier but adds a $0.00005 one-time start fee we don't charge -- tied-at-best, dearer overall, same shape as `webdatatools/google-play-reviews-scraper` (c3287); this niche now has two tied-plus-start-fee rivals. `tidytools/ats-career-site-jobs` (non-price breadth find: auto-detects 21 ATSs from a bare company domain, where ours needs the slug -- folded into that Actor's next `competitor_audit` rotation, not a README edit). `wulfcare/app-store-reviews-scraper` (non-price find: third no-500-cap claimant, tell that its deep path drops `appVersion` -- also folded into the next rotation). `xtracto/google-play-reviews-scraper` (4u) $0.002→$0.00099/result plus a $0.005 start fee -- 10-20x dearer. `zerobreak/google-play-store-scraper` (4u) $0.00699→$0.00299/result -- 30-70x dearer, and a broader listings/charts product, different shape from our reviews export. `accountable_eel/remote-jobs-unified-search` (3u) covers 6 boards (2 we lack, 3 it lacks, net +1 for us) at $0.003→$0.0015/result plus a $0.004 start fee vs our $0.0015→$0.001 with none -- 1.5-2x dearer before the fee. **c3305 (rows 203-208): 0 of 6 real, 6 non-issues.** `accountable_eel/workday-public-careers-monitor` (3u) is Workday-only (1/12 ATS platforms) -- scope exclusion, same bucket as prior single-platform ATS rulings, despite its $0.001 start + $0.0005/job GOLD+ rate beating our $0.0007/job flat at high volume (e.g. 40 jobs/run: theirs $0.021 vs our $0.028) -- cheaper-at-volume-within-scope-exclusion does not override the scope ruling, per `freshactors/recruitee-jobs-scraper` (c3297) and `glasswing/linkedin-jobs-scraper` (c3297) precedent. `accountable_eel/shopify-store-lookup` (3u) is a bulk domain-list Shopify-detector + lead-gen lookup tool ($0.003 start + $0.004→$0.002/lookup), a different product shape from our per-product catalog scraper -- category mismatch, same bucket as `zinin`/`pintostudio` store-level tools. `agentictools/hacker-news-search` (3u) is flat $0.0005/item vs our tiered $0.0002→$0.0001 -- we undercut it 2.5-5x. `alexmorain/ats-jobs-scraper` (3u, 61 public30d) is a direct rival (9/12 of our ATS platforms, missing Teamtailor/Breezy/BambooHR) priced at $0.01 one-time start + $0.002→$0.0015/job vs our $0.001→$0.0007/job with no start fee -- we are cheaper at every tier even before its start fee, and broader. `andok/shopify-intelligence` (3u) prices a $0.023-0.05 start fee plus $0.0047-0.01/item vs our $0.00085-0.001/item -- 5-10x dearer plus a sizable start fee. `andrew_avina/patentsview-mcp` (3u, USPTO patent search, MCP-native) is a category mismatch -- we have no patent-search Actor, and it's an MCP tool-call product like `conserving_celerytop/jobs-mcp-server` (c3298), not a dataset export. Exact-handle grep: 0 hits for all 6 (genuinely new handles). No README/code changes this round. **c3307 (rows 209-214): 0 of 6 real, 6 non-issues.** `antishock/greenhouse-ats-jobs-scraper` (3u, 30 public30d) is Greenhouse-only (1/12 ATS platforms) -- scope exclusion -- AND charges $0.002 flat per job plus a separate $0.002 `apify-actor-start` fee, dearer than our $0.001→$0.0007/job at every tier even before the start fee, double non-issue. `apivault_labs/shopify-store-leads-scraper` (3u, 30 public30d) is a lead-gen contact-discovery tool (emails/phones/ratings by keyword, store-row priced at $0.004 + a $0.00005 start fee) -- category mismatch vs our per-product catalog scraper, same bucket as `zinin`/`pintostudio`/`accountable_eel/shopify-store-lookup`/`andok` store-level tools. `automly/hacker-news-trends-api` (3u, 32 public30d) is flat $0.0005/item vs our tiered $0.0002→$0.0001 -- we undercut it 2.5-5x. `bgfc97/domain-availability-checker` (3u, 29 public30d) is an RDAP bulk domain-availability/expiry checker, not a trademark search product -- category mismatch on shared "brand protection" vocabulary vs our `trademark-search-scraper`, same bucket as `glitchbound/website-scraper`'s shared-vocab mismatch. `bgfc97/hacker-news-scraper` (3u, 29 public30d) is flat $0.0005/item vs our tiered $0.0002→$0.0001 -- we undercut it 2.5-5x. `bgfc97/shopify-store-products-scraper` (3u, 29 public30d) is flat $0.001/product -- ties our FREE-tier $0.001 but we are cheaper at every tier above it ($0.00095→$0.00085), same tied-at-best-dearer-overall shape as `sync-network`/`webdatatools`/`bgfc97`'s hacker-news sibling. Exact-handle grep: 0 hits for all 6 (genuinely new handles). No README/code changes this round. **c3308 (rows 215-220): 0 of 6 real, 6 non-issues.** `bgfc97/ats-jobs-aggregator` (3u, 29 public30d) covers Greenhouse/Lever/Ashby/Workable only (4/12 ATS platforms) -- breadth exclusion -- AND is flat $0.001/job, which ties our FREE rung but is dearer at every tier above it ($0.00085 BRONZE -> $0.0007 GOLD+), double non-issue; same flat-$0.001 house style as the three `bgfc97` rows ruled at c3307. `bgfc97/google-play-scraper` (3u) is flat $0.001/record vs our flat $0.0001/result -- we undercut it 10x. `brilliant_gum/jobs-aggregator` (3u) spans Indeed + LinkedIn + 56 employer boards (a real breadth gap, and Indeed/LinkedIn are outside our ATS scope per the c3297 `glasswing` ruling) but charges a $0.01 one-time start fee plus $0.008/job -- 8-11x our $0.001->$0.0007 before the start fee counts, so breadth-without-price-advantage again fails the bar (c3298 `om_kh`, c3302 `snow_leo_data` precedent). `chimerical_quicklime/remotive-scraper` (3u, 30 public30d) is the closest call of the batch: Remotive ONLY (1 of our 7 de-duplicated boards, no merge/dedup) at a $0.001 start fee + $0.001163/result, which on a 100-row run ($0.1173) beats our FREE ($0.15) and BRONZE ($0.13) but LOSES to our SILVER ($0.11) and GOLD+ ($0.10) -- a partial low-tier undercutter inside an established scope exclusion, and `remote-jobs-scraper/README.md`'s standing cycle-1271/1312 paragraphs already concede exactly this bucket generically (and already name `canadesk/remotive-jobs`, flat $0.001 on Remotive alone, as a harder case), so no new README edit is warranted -- same ruling shape as `accountable_eel/workday-public-careers-monitor` (c3305). Side note worth recording: its own title and description still advertise "$0.93 per 1,000 records" while its LIVE ladder (effective 2026-11-10) is $0.001163/record = $1.163/1k -- a stale self-claim on the rival's listing, the mirror image of our own c3263 `ats-jobs-scraper` stale-title bug, and a reminder never to price a rival from its title. `chimerical_quicklime/google-play-scraper` (3u, 30 public30d) charges a $0.005 start fee + $0.0005/result vs our flat $0.0001 -- 5x dearer per row before the fee -- and is an app-search/details/top-charts product rather than a reviews export, so it is dearer AND partly a category mismatch. `chrisp1211/ats-jobs-scraper-max` (3u, 29 public30d) is Greenhouse/Lever/Ashby only (3/12 platforms) -- scope exclusion, same bucket as `hipersoft/company-jobs-scraper` (c3298) -- AND flat $0.002/job, 2-2.9x our ladder with no start fee on either side, double non-issue. Exact-handle grep: 0 hits for all 6 (genuinely new handles). No README/code changes this round. **c3310 (rows 221-226): 0 of 6 real, 6 non-issues** (full detail in its own `CLOSED c3310` block above) -- `cirkit/shopify-store-catalog-scraper` (tied-at-best-dearer-overall, same bucket as `sync-network`/`bgfc97`), `cliqtomedia/google-play-reviews-scraper` ($0.0035 start fee masks a SILVER+/GOLD+ per-unit edge; thin conditional crossover at >117-175 reviews/run, dearer at the common case), `constant_quadruped/steam-review-monitor` (7-13x dearer AND a different aggregate-monitoring shape), `cryptosignals/shopify-scraper` (5-6x dearer), `cryptosignals/greenhouse-jobs-scraper` (Greenhouse-only scope exclusion AND dearer, double non-issue), `datadesk-io/workday-jobs-scraper` (Workday-only scope exclusion AND dearer at every tier, double non-issue). **c3311 (rows 227-232): 0 of 6 full-range real, 1 partial scope-exclusion find, 5 non-issues** (full detail in its own `CLOSED c3311` block above) -- `datalantern/ats-jobs` (5/12 ATS platforms scope exclusion AND dearer, double non-issue), `datapilot/ai-tool-launch-tracker-scraper` (10-20x dearer AND category mismatch), `datapilot/export-intelligence-monitor` (dearer AND category mismatch), `datapilot/franchise-expansion-tracker` (tied-at-best-dearer-overall), `deepmine/workable-jobs` (Workable-only scope exclusion but a genuine ~41-50% full-range per-unit undercut within that scope -- filed as its own `NEW c3311` item above for `ats-jobs-scraper`'s next `competitor_audit` rotation), `devilscrapes/multi-ats-jobs-scraper` (3/12 platforms scope exclusion AND dearer, double non-issue). **c3313 (rows 233-238): 1 of 6 real, 5 non-issues.** `devilscrapes/workday-jobs-scraper` (3u) is Workday-only (1/12 ATS platforms) -- scope exclusion -- AND flat-ish $0.0015→$0.00132/job, dearer than our $0.001→$0.0007 at every tier, double non-issue. `devilscrapes/hacker-news-scraper` (3u) is $0.002→$0.00176/item vs our $0.0002→$0.0001 -- we undercut it 10-17x. `everyotherfriday/google-play` (3u) is a broader app-details/search/developer-catalog product charging a flat $0.0002/review -- 2x our $0.0001, dearer despite the extra scope, non-issue. `feedforge/weworkremotely-scraper` (3u) is WWR-only (1 of our 7 de-duplicated remote boards) -- scope exclusion, same bucket as prior single-board rulings (`glasswing`/`accountable_eel`), despite its $0.0002/job rate being cheaper than our $0.001-0.0015/job within that narrow scope. `feedforge/steam-games-scraper` (3u) charges $0.0024/record (games catalog: top-sellers/prices/discounts/genres, no reviews) vs our $0.000575→$0.0003 -- 4-8x dearer. **The real one: `factpipe/website-screenshot`** (3u) ties our flat $0.002/result at FREE but tiers down to $0.0018/$0.0016/$0.0014 at BRONZE/SILVER/GOLD+ against our flat $0.002 -- a smaller-magnitude but genuine undercut past the FREE plan, with a built-in cookie-banner-hiding feature we don't have a no-selector equivalent for. **Disclosed and shipped same-cycle**: new dated paragraph in `website-screenshot-scraper/README.md` (after the `locaihost` paragraph, before `## FAQ`), package.json 0.1.4→0.1.5, pushed (build 0.1.50), live README verified byte-identical via `GET /v2/actor-builds/{id}` (32,672 chars both, `factpipe` present). **c3314 (rows 239-244): 1 of 6 real, 5 non-issues.** `foo121/google-play-reviews-scraper` (3u, 29 public30d) is flat $0.0002/result-item vs our flat $0.0001 -- we undercut it 2x. `foo121/federal-register-scraper` (3u, 29 public30d) is flat $0.004/result-item vs our flat $0.0008 -- we undercut it 5x. `freshactors/workable-jobs-scraper` (3u, 29 public30d) is Workable-only (1/12 ATS platforms) -- scope exclusion -- and its $0.0005/job rate undercuts our $0.0007-0.001/job once its per-company `company-jobs-fetched` fee ($0.02 Free/Bronze -> $0.006 Diamond, one-time per board) is amortized past 30-40 jobs/company, but cheaper-at-volume-within-scope-exclusion does not override the scope ruling, per `accountable_eel/workday-public-careers-monitor` (c3305) and `chimerical_quicklime/remotive-scraper` (c3308) precedent. `gazidev/hacker-news-data` (3u, 30 public30d) is flat $0.0002/item plus a $0.00005 one-time start fee vs our tiered $0.0002->$0.0001 with no start fee -- we tie at Free and undercut it 2x at Gold+, non-issue. `gazidev/greenhouse-jobs` (3u, 36 public30d) is Greenhouse-only (1/12 ATS platforms) -- scope exclusion -- AND flat $0.001/job (plus an optional $0.01 directory-scan fee and $0.00005 start fee) ties our Free rung but is dearer at every tier above it ($0.0007 Gold+), double non-issue, same tied-at-best-dearer-overall shape as `bgfc97/shopify-store-products-scraper` (c3307). **The real one: `gazidev/shopify-products-monitor`** (1u, but 45 public30d) is a flat **$0.0003/product** behind only a $0.00005 start fee -- the niche's deepest every-tier undercut yet, ~70% below our $0.001 Free rate and 65% below our $0.00085 Gold+ rate (past `glidepath`'s prior-deepest 24%-below-Gold+ gap), reading the same public `products.json` endpoint and shipping its own monitor mode (`change-detected`/`store-summary`) parallel to our `watchLabel`. **Disclosed and shipped same-cycle**: new dated paragraph in `shopify-products-scraper/README.md` (after the `rowcraft` paragraph, before `## FAQ`), package.json 0.1.31->0.1.32, pushed (build 0.1.124), live README verified byte-identical (61,556 chars both, `gazidev` present). **NEXT: rows 245-250, none read yet.** Method is fixed: clone the most recent surviving `_triageNNNN.py` (deleted after use each time; re-clone from `bin/_triage3304.py`'s pattern if none survive), price via `check-price-superiority.effective(pricingInfos, now)` (NOT `pricingInfos[-1]`, the c3244 future-dated rule), expand EVERY charge event and tier rung (the c3244 cheap-leg rule), read each live README past the title for scope exclusions, and exact-string-grep our own READMEs for the slug before calling anything new. **When a real undercutter is found, disclose it the same cycle (dated README paragraph + version bump + push + byte-identical live verify) rather than deferring to the next `competitor_audit` rotation** -- c3261/c3277/c3278/c3286/c3297/c3313/c3314 all shipped same-cycle; that is the established practice, not the c3162-era "fold into next rotation" text this supersedes. At 6 rows/cycle the tail is ~207 cycles; it is a FALLBACK for cycles with no real backlog, never a reason to skip one.**

- [ ] **RESOLVED c3228 -- the `NEW c3168` competitor-claims backlog is EMPTY fleet-wide: 1,044 user-count claims / 299 paragraphs checked, 0 STALE / 0 UNDATED / 0 DISAGREE / 0 unresolvable (2026-11-15), the first fully clean fleet reading on record -- and fault-injection-proven in BOTH directions (the count guard and the paragraph/date guard each tripped on a local-only README edit; both reverted, both re-ran clean, no build, READMEs byte-identical to HEAD). The 5.0KB record -- the four-rule hand-edit method, the 10 expected informational `DISCLOSED` lines, and the fault-injection detail -- is archived VERBATIM in `queue_archive.md` under `## Archived by cycle 3240`** (compressed there by c3240's RULE 4 pass). **Cadence: `check-competitor-claims` `last_cycle 3228`, next due c3372.** If you run it FLEET-WIDE, record it with `--ran` -- the tracker sat 129 cycles pessimistic because the real fleet runs at c3182/c3190/c3191 never did, and `--only` runs correctly do not count. **Re-open trigger: a fresh fleet-wide sweep flagging a non-`DISCLOSED` line. Nothing else -- do not re-derive a backlog from this stub or from archived handoff prose, run the checker.** The standing rule this item earned (also homed in `notes/LEARNINGS.md`, cycle 3228): never act on a competitor-claims target named in a handoff without re-confirming it via `--only <slug>` first (seconds, read-only) -- this file's pointers rot faster than its content, because content is written by the cycle that owns it while pointers are written by cycles that do not.

- [x] **PARTIALLY DONE at c3250 -- the ONE OPEN ITEM c3248 flagged (needed 2-3 real third-party Rippling slugs before writing code) is now RESOLVED, no code changed yet.** BUILD slot (3250 % 3 == 1); preflight fresh (`checks-due --all` NONE DUE, soonest `check-row-floor` in 4c; `audit-due --all` FLEET ROTATIONS NONE DUE; `inbox-triage new` NONE UNTRIAGED, 81 msgs; `bin/revenue` unchanged -- $0 booked, 27 Actors, 54 users, 1485 runs30d, 31 ext_bad30d, 0 bookmarks/reviews, no buyer signal). Used `WebSearch` (`site:ats.rippling.com jobs`) and got **9 real company slugs** in one query, no guessing needed: `skillable-careers`, `findhelp`, `capacity`, `joinroot` (Root Insurance), `rts`, `agencycyber`, `elevate`, `closinglock`, `nocd`. Live-verified the public API (not the SPA) on **5 of them**: `GET https://api.rippling.com/platform/api/ats/v1/board/<slug>/jobs` returned **200 with a bare JSON array on all 5** (`findhelp`=36 jobs, `joinroot`=24, `nocd`=103, `capacity`=1, `skillable-careers`=6), every row carrying the same 5 keys c3248 measured on `rippling` itself (`uuid`,`name`,`department`,`url`,`workLocation`). Pulled one real `uuid` from `findhelp` and hit its **detail** endpoint live too: 200, same key set c3248 documented (`createdOn`,`workLocations[]`,`employmentType`,`companyName`,`payRangeDetails`,...) -- `payRangeDetails` was `[]` on this specific job (confirms the field is universal but not always populated, matching c3248's own "4 of 5 populated" note, not a shape change). **This settles c3248's open question: the list/detail shape is NOT `rippling`-tenant-specific, it is the real cross-tenant Rippling ATS API.** Did not check `src/location.js` for Remote(...)/Hybrid(...)-unwrapping support -- confirmed by reading the file that this handling does NOT exist yet (grepped for `Remote (` / `Hybrid (`, 0 hits), so that part of c3248's note still stands as a real gap to close in the build. Ran out of cycle time budget after this verification + the write-up below, so **no `src/main.js`/`input_schema.json`/`registry.json`/README edits were made this cycle** -- left for the next BUILD slot with the exact steps below so it doesn't re-derive anything. Guards untouched (no code changed), all 3 services active, site 200 on `/`, `/tools`, `/pricing`, `/tools/ats-jobs-scraper`. Spend $0 (5 keyless public GETs to `api.rippling.com`, 2 WebSearch calls). Blockers: none. Owner email: none owed.
  - **Next BUILD slot, implement in this order:** (1) add `rippling` to `SUPPORTED_ATS` (`src/main.js:13`) and to `AUTO_DETECT_ATS` (`src/main.js:17`) -- a quick collision check first: none of the other 9 auto-detected slugs are literally `rippling`/`findhelp`/`joinroot`/etc, so this should be clean, but re-run the check rather than assume. (2) Write `fetchRippling(slug)` next to `fetchPersonio` (`src/main.js:~1006`), two-step like `fetchSmartRecruiters`/`fetchWorkday` (`src/main.js:1088`, `:1179`): list call maps `uuid`->jobId, `name.trim()`->title, `department.label`->department, `url`->jobUrl/applyUrl, `workLocation.label`->location (strip the `Remote (...)`/`Hybrid (...)` wrapper before feeding `parseLocation`, see open gap above -- `isRemote`/`workplaceType` should key off the wrapper word itself, not just the parsed city). (3) Gate the per-job detail call the same way `workdayNeedsDetail` does (`src/main.js:128`, pattern to copy, name it e.g. `ripplingNeedsDetail`): `needDescriptions || hasSalary || minSalary != null || maxSalary != null || !!postedAfter || !!postedBefore || !!employmentTypeKeyword` -- NOT `departmentKeyword`/`locationKeyword` since those two are already on the list row, unlike Workday where nothing but title/url is. Detail call fills `descriptionHtml`/`descriptionText` (from `description.company`, HTML), `publishedAt` (`createdOn`, already full ISO-8601 -- no `new Date().toISOString()` round-trip needed, unlike Workday's `startDate`), `employmentType.label`, `secondaryLocations` (from `workLocations[]`, minus the already-used primary), and `salaryMin/salaryMax/salaryCurrency/salaryInterval` from the FIRST `payRangeDetails[]` entry whose `isRemote` matches the job's remote-ness if ambiguous, else the first entry -- do NOT average or sum across geo tiers, and Rippling must NOT be added to `SALARY_BLIND_ATS` (`src/main.js:1416`). (4) Register in `FETCHERS` (`src/main.js:~1323`). (5) Add one real row to `DEFAULT_COMPANIES`/the example corpus (`src/main.js:~26`) using one of the 5 now-confirmed-live slugs above (e.g. `{ ats: 'rippling', slug: 'findhelp' }` -- NOT `rippling` itself, keep that for ad-hoc manual testing only since it's the vendor's own tenant, not a buyer-representative one). (6) Update `.actor/input_schema.json` ATS enum + its title/description string, `registry.json`, and the README's platform-count strings -- this is the moment to also fix the 9 stale "N of our 7 platforms" lines (199, 209, 211, 213, 215, 217, 219, 221) to "11" at the same time, per c3248's note, plus the two "10 ATS platforms" lines (3, 8). (7) Test live against `findhelp`/`joinroot`/`nocd` (not just `rippling`) before pushing, then push per PLAYBOOK and live-verify the README byte-identical, same discipline as c3244/c3245/c3243's builds this week.

- [ ] **NEW c3167 (handoff, ONLY option 1 is still OPEN -- option 2 is CLOSED c3228, see below) -- run `checks-due`/`audit-due` fresh first as always.**
  1. **Continue `NEW c3162` triage** (1,463 rows left in `state/audit_data/c3162_vendor_catalogue.json`, sorted by users) -- next 6 listed just above (in the `PARTIALLY DONE` block). Same method as c3167/c3217/c3218/c3239: for each row, `GET /v2/acts/<handle with / -> ~>` live, read `description` for actual scope (watch for store-level/lead-gen/B2B-contact products AND outright niche-vocabulary false matches -- 2 of 6 at c3218 and 2 of 6 at c3239 were false matches on shared vocabulary alone, e.g. "funding"/"screenshot"/generic "IP search"), read full `pricingInfos` history (`data.pricingInfos[-1]`, not `currentPricingInfo` which reads `None` via this field name) for the real tiered/flat ladder and compare against our own live price (`GET /v2/acts/fetchsmith~<our-slug>?token=...`, same field path), then either fold into the relevant Actor's README (if genuine undercutter or large enough to warrant a scope-exclusion mention) or skip silently (if a clear non-issue, no mention needed -- precedent in `CLOSED c3167`/c3217/c3218/c3239 above).
  2. ~~**Fix the `check-competitor-claims` backlog c3167 surfaced**: 12 stale competitor user-counts + 8 undated competitor comparisons across 11 Actors.~~ **CLOSED c3228 -- that entire backlog is now cleared and the fleet reads 0 STALE / 0 UNDATED / 0 DISAGREE over 1,044 claims, fault-injection-proven. See `CLOSED c3228` above; do NOT re-derive a list from this bullet's Actor names, they were all closed between c3177 and c3215.** Next sweep due c3372.

- [ ] **NEW c3162 (MEDIUM) -- triage `state/audit_data/c3162_vendor_catalogue.json` (1,485 rows, already sorted by `users` descending) top-down.** Read each row's own live README/pricing (same discipline as the c3160 `rbbscrap` triage: confirm it is actually public/not-deprecated, read past the title for scope exclusions, check whether the owner's existing generic prose in our README already covers it before calling it "new"). Do NOT try to clear the whole file in one cycle -- start with the top 20-30 by users (the highest-signal, already skimmed as plausible-real at c3162: `clearpath/shopify-store-leads` 2007u, `fantastic-jobs/workday-jobs-api` 961u, `automation-lab/apple-app-store-scraper` 942u, `apivault_labs/shopify-store-analyzer` 472u, `fantastic-jobs/lever-co-jobs-api` 353u lead the list) and fold genuine finds into that Actor's next `competitor_audit` rotation rather than publishing an off-cycle README edit. **RESUME POINTER (updated c3314): rows 1-244 (indices 0-243) are DONE; next cycle starts at rows 245-250 (indices 244-249)** -- clone the most recent surviving `_triageNNNN.py` (deleted after use, same as every prior triage script), keep the `cps.effective(pricingInfos, now)` method. Expect a high false-positive rate from the OWNER-bucket gap documented in CLOSED c3162 (archived to `tasks/queue_archive.md` by the c3172 trim) -- many rows are probably already disclosed generically, just not under their exact slug.

- [ ] **NEW c3148 -- `fda-recall-scraper` has joined the versions-route-only README verification set.** Its README crossed 95k this cycle (90,512 -> 95,467 bytes). `GET /v2/actor-builds/{id}`'s `actorDefinition.readme` truncates at ~100k, so from the next push onward it would silently report a false match. **Verify this Actor's pushes via `GET /v2/acts/{id}/versions` -> `items[].sourceFiles[]` -> the `README.md` entry's `content`, same as `remote-jobs-scraper` and `sam-gov-opportunities-scraper`.** PLAYBOOK line 88 already states the rule generically; this is the third Actor to hit it, and competitor-audit paragraphs are what push these READMEs over, so expect more.

- [ ] **NEW c3140 (TRIVIAL/checker precision -- a KNOWN FALSE POSITIVE, do NOT "fix" the README).** `check-price-superiority` reports two `GONE ... is 404 on Apify but still named here` lines against `hacker-news-scraper/README.md:123`: **`omcljs/om` and `reagent-project/reagent`**. Neither is an Apify handle -- they are **GitHub repo paths** in that Actor's GitHub-enrichment example output (ClojureScript repos), and `owner/name` is the same shape as an Apify handle, so c2832's "non-handle tokens such as repo paths are no longer counted" filter does not catch them. **Bias is SAFE** (it over-reports dead rivals; it can never hide a live undercutter), so do not rush. If a future cycle does tighten it, the fix is a scope guard on the GitHub-enrichment section, not a README edit -- removing the repo names would damage real buyer-facing example output. Same class as the `check-competitor-claims` user-count gap in `NEW note c2816`.

- [ ] **NEW c3136 (TRIVIAL/method -- cost ~8 minutes this cycle, will cost the same again).** On a rate-limited or async HTTP endpoint, **`curl -D -` and `curl -s -w "%{http_code}"` are two SEPARATE REQUESTS and will disagree with each other.** c3136 spent ~8 minutes deriving a confident, completely false rule ("a browser `User-Agent` turns mshots' 403 into a 429", then "query params do it", then "it alternates per url") purely because the header dump and the status-code probe were different calls landing in different states of the same endpoint -- and each wrong rule reproduced 3-5 times in a tight loop, because the state was sticky for ~30-60s. **Rule: when characterising an endpoint that might be stateful, capture status + content-type + size + headers + body magic bytes in ONE call** (`curl -s -D /tmp/h -o /tmp/b -w "%{http_code}|%{content_type}|%{size_download}"`, then read `/tmp/h` and `xxd -p -l 4 /tmp/b`) before forming any hypothesis. The tell that something was wrong: a "429" that reported `content_type: text/html` at 564 B in one call and `200 image/jpeg` at 564 B in another -- two different statuses on the same byte count is never a real rule, it is two requests.

- [ ] **NEW c3136 (LOW/content, a reusable angle rather than a defect).** The strongest dev.to article this channel has produced was not new research -- it was **re-measuring our own 8-day-old post and publishing the two ways it had gone wrong**. That shape is repeatable and cheap (3 curls), it is honest in a way the channel rewards, and it doubles as maintenance of the site post. **62 unsynced site posts remain**, and the ones whose claims are a handful of unauthenticated HTTP calls are the best syndication candidates for exactly this reason -- prefer them over posts whose claims need an Actor run to re-verify. Standing durable lesson from this one (already in LEARNINGS): **a keyless endpoint's REFUSAL is not a stable property of your IP.** A single measurement of a `403` is worth far less than the same measurement of a `200`, so never generalise a point-in-time refusal into "this endpoint blocks cloud IPs" -- re-hit it a day later before writing that sentence anywhere buyer-facing.

- [ ] **NEW c3108 (TRIVIAL/method, earned the cheap way -- 30 seconds of prevention).** Editing a buyer-facing `.actor/input_schema.json` by round-tripping it through `json.dumps(indent=N)` reformats the WHOLE file for a one-line content change: c3108's first attempt turned a 1-line prose fix into `164 insertions / 136 deletions` (this fleet hand-formats these files at 2-space indent with inline `items` objects, which no serialiser reproduces). Caught by reading `git diff --stat` before pushing, reverted, redone as a surgical replace against the RAW escaped text (`\"Global newest-first\"`, note the backslashes) for a `1 insertion / 1 deletion` diff. **Rule: never serialise a hand-formatted `.actor/*.json`; string-replace it, and `git diff --stat` every schema edit before `apify push`.** A whole-file reformat would also have made the live-vs-local byte-identity check pass while burying the real change, so the usual verification would NOT have caught it.

- [ ] **NEW note c3104 (LOW, checker precision -- bias is SAFE, do NOT rush, and do NOT "fix" it before reading the second paragraph).** `bin/_unit_price.py`'s `is_start_fee(key, ev)` does **not** classify `lanternlab318/hacker-news`'s `run-start` event ($0.0005) as a start fee -- c3104's rung-for-rung re-verification printed it as `[per-row]`. The listing's own README and the event title describe a once-per-run charge, and the sibling listings this cycle re-priced show the two shapes the helper DOES catch: Apify's canonical `apify-actor-start` key (`plotpointtech`, `tidelane`, `informed_almandine_vzb`) and a custom key carrying `isOneTimeEvent: true` (`rowfeed`'s `apify-actor-start`). `lanternlab318` uses a custom key (`run-start`) **without** the `isOneTimeEvent` flag, which is the one combination that falls through.

  **The bias is safe and that is why this is LOW.** Read as a per-ROW rate, a $0.0005 run fee looks 2.5x DEARER than our $0.0002 Free rung, so the mistake can only ever make a rival look more expensive than it is -- it cannot hide an undercutter, which is the failure direction that matters. It also did not affect c3104's write-up: `lanternlab318`'s Free+Bronze undercut verdict comes from its separate `story` event ($0.000149), which is correctly classified. **If picked up, do not widen `is_start_fee` on the key name alone** (`run-start`, `start`, `run` as substrings will collide with legitimate per-row event names like `job-post`/`search-term` in neighbouring niches); the honest fix is the `runfee_price` path in `check-price-superiority` (which already reasons about run-scoped events as a SET) plus a hand-read list, the same shape c2466 chose for the ambiguous multi-event bucket. Worth noting the detection cost was ~0: it surfaced only because c3104 printed the start-fee classification per event instead of trusting the resolved unit price.

- [x] **DECIDED c3081 -- DEFER, no `meta.json` edit. Do not re-open without one of the two triggers named below.** Read `meta.json`, the `watchLabel` README row, and the full FAQ/Pricing sections before deciding (`actors/trademark-search-scraper/README.md` lines 20, 78-82, 106-111, 131, 135, 139). Four reasons the reprice loses on balance, not one: (1) **the live README already states the zero-charge behaviour as an unconditional per-run promise**, not just a first-run baseline -- line 20 ("every later run on the same label + search returns and charges only marks not already delivered") and line 131 ("watch-mode baseline runs return and charge nothing") -- a new `watch-check` fee charged on a quiet run contradicts live buyer-facing text on our ONLY page-1 listing, not a doc nobody reads. (2) **This is already our stated differentiator against the exact two rivals cited as the reason to reprice**: README line 139 already discloses `nexgendata/uspto-trademark-search` and `nexgendata/euipo-esearch-trademarks` charge $0.05/watch-check (25-50x ours) and line 135 says plainly "Our `watchLabel` mode charges only the $0.002 row rate, and only on marks you have not already been given" -- the gap `NEW c3080` found is not an unmarketed gap, it is an already-marketed asymmetry; repricing would delete the very thing being advertised. (3) **Zero signal there is any revenue to capture**: 0 bookmarks, 0 reviews, $0 booked on this Actor -- we do not know a single real buyer runs `watchLabel` at all, let alone on a schedule frequent enough for the $0 compute exposure to matter. (4) **The exposure being guarded against is small by construction**: a no-change watch run is one HTTP-only TMview page fetch plus a KVS baseline read/write, not a browser session -- sub-cent ACTOR_COMPUTE_UNITS cost (see `bin/apify-spend`'s per-service breakdown), nothing like the data-transfer or proxy cost a result-heavy run carries. **Re-open only if either:** (a) real buyer signal appears on this Actor specifically (a bookmark, a review, or a booked-revenue event tied to it), making the upside non-speculative; or (b) a future `bin/usage-trend`-style check shows sustained high-volume scheduled `watchLabel` runs at zero rows, showing the compute exposure is no longer trivial. Neither test re-run (`check-price-superiority`, `check-unit-matched-price`) was needed since no price changed. $0 spent, no build, no push. Full prior research (rival prices, the tension, the suggested shape if ever shipped) stays below, superseded but kept for context on re-open.
  **Why this Actor and not another:** c3080's `store-anon-rank` run put it at **#8 of 249** (5 users, runs30d 636) -- our only top-10 rank on any buyer query, vs #29-#501 for all 26 others. It is the one listing that actually gets buyer impressions, so it is the only one where conversion/monetization work can pay (see LEARNINGS c3080).
  **The gap (verified, not assumed):** we ALREADY ship watch mode -- `watchLabel` / `watchChanges` / `webhookUrl`, documented in `actors/trademark-search-scraper/README.md` lines 20-22, with `_watchChangeType`/`_watchPrevious` change fields. But `meta.json` prices exactly ONE event: `result` @ $0.002 ("Result item"). So a scheduled watch run that finds nothing new returns 0 rows and bills **$0** while still costing us compute + dataset/KVS writes. Rivals price exactly this event: **#1 `nexgendata/uspto-trademark-search` `watch-check` @ $0.05**, **#9 `nexgendata/euipo-esearch-trademarks` `watch-check` @ $0.05**, #4 `trev0n/tmview-scraper` `trademark-details` @ $0.002 (plus a $0.005 `apify-actor-start` on #1/#3/#4/#7/#9, which we do not charge at all).
  **The tension that makes this a DECIDE, not a do:** (a) our published README promises "the first run under a label seeds a baseline (0 rows returned, **0 charged**)" -- adding a charge silently contradicts live buyer-facing docs and must be a doc change too; (b) "From $0.002/result, no start fee" in `meta.json`'s description is our stated differentiator and we are **the cheapest in the whole top 9** (#1/#9 charge $0.05/record, #3 $0.007+$0.005 start) -- check `check-price-superiority` / `check-unit-matched-price` before touching it; (c) 0 bookmarks / 0 reviews / $0 booked means there may be no watch-mode users to monetize yet, so the upside is speculative while the positioning loss is real.
  **Suggested shape if it goes ahead:** a small `watch-check` event (well under the rivals' $0.05 -- we undercut on purpose) charged ONLY on a run with `watchLabel` set that returns 0 new rows, leaving plain searches at $0.002/result with no start fee and the "no start fee" claim intact. Update README lines 20-22 and the FAQ in the same commit. Re-run `actor-health` + the default-input gate after `apify push`.

- [ ] **NEW c3046 (HIGH -- the RULE 6 anchor-map sweep that has been the default GROWTH-slot pick since c3004 is now DONE; every future GROWTH slot needs a different default, not "find the next unmapped Actor"). CORRECTED c3050: 27/27 is now TRUE. CORRECTED c3055: option (a) below is CHECKED FLEET-WIDE and CLOSED EMPTY -- full record archived c3063 to `tasks/queue_archive.md` under `## Archived by cycle 3063` (`CLOSED c3055`), do not re-check it again without a NEW meta.json edit landing first.** `nih-reporter-scraper` (the last genuinely-unmapped Actor per `CLOSED c3049`) was anchor-mapped for real this cycle -- see `CLOSED c3050` above: RULE 6 CLOSED NEGATIVE (15th straight, every field anchors >=1 of the 22 pre-existing terms), RULE 6b found 12 fresh untracked wins (15th straight 6b payout). **RULE 6 fleet coverage is genuinely 27/27 -- do not re-verify this one again**, the per-field anchor counts (title=4, description=1, seoTitle=6, seoDescription=10, readme=1, summing to all 22) are recorded in `bin/store-rank`'s cycle-3050 TERMS comment and were cross-checked term-by-term, not just counted. (CORRECTED c3049 below is now superseded, kept verbatim for the methodological lesson: re-verify any future "N/27 complete" claim by grepping the TERMS comment for "RULE 6"/"anchor-map" before trusting it -- a cycle's own paragraph can contradict its own headline, as c3046's did.) ~~All 27 Actors (26 scraper-shaped + `clinicaltrials-mcp-server`, CLOSED NEGATIVE c3002) are now anchor-mapped under RULE 6, and RULE 6 has gone 13/13 CLOSED NEGATIVE fleet-wide -- the append lever is genuinely, comprehensively dry; do not re-run RULE 6 on any Actor expecting a different outcome.~~ **Options for the next GROWTH slot, in rough order of expected value:** ~~(a) Re-run RULE 6b on an already-mapped Actor whose `meta.json` fields changed since its mapping cycle~~ **CHECKED c3055, CLOSED EMPTY (full record archived c3063, `tasks/queue_archive.md` `## Archived by cycle 3063`, `CLOSED c3055`): scripted a fleet-wide cross-reference of every Actor's last `meta.json`-touching commit against its RULE-6-mapping cycle; on every one of the 27, the mapping cycle is AT or AFTER the last real text edit, so there is currently no unshortlisted vocabulary anywhere in the fleet. Re-run this check (the script's method is recorded in the archived block, not kept on disk) only after a NEW meta.json edit ships that is NOT itself a RULE-6/6b cycle.** (b) ~~Pick up the `NEW c3040 (MEDIUM)` sentinel-`after:` idea~~ **STALE cross-reference -- this was already shipped in c3052/c3053 (see `CLOSED c3053` / `SHIPPED c3053` in `tasks/queue_archive.md`, archived by cycle 3204); remove this bullet's premise, it predates that ship.** (c) **Try RULE 6b's raw method (curate n-grams from live field vocabulary, batch-price, verify via `--why`) on a SECOND pass over an Actor already swept once** -- c3046's own sweep found 14 fresh wins on an Actor with FIVE prior SEO-sweep cycles (2024/2032/2033/2036/2037), so a second 6b pass elsewhere may not be exhausted either; the risk is diminishing/duplicate returns, so size the candidate shortlist carefully and skip if the obvious n-grams are already tracked. **SUPERSEDED c3056 -- do NOT take (c) as written.** c3056 went to pick a candidate for (c) and found the premise too narrow: only 15/27 Actors have a dedicated RULE 6b sweep on record at all, so a SECOND pass is not the fleet's cheapest remaining 6b work -- a FIRST pass on the other 12 is. See `NEW c3056` at the top of this file for the named 12-Actor backlog, the ordering heuristic (thinnest TERMS first) and the full 7-step method; c3056 executed the first of them (`grants-gov-scraper`, 13 wins, $0, no build). Re-open (c) only once that backlog is exhausted. (d) **Find a genuinely new lever** -- e.g. re-examine whether the eviction method (LEARNINGS c908, `NEW c3000` RULE 6's sibling) has untried candidates on any of the Actors RULE 6 just closed, since an anchor-mapped field is a PREREQUISITE for eviction-pricing, not a dead end for it.

- [ ] **NEW c3044 (TRIVIAL/method -- saves every remaining RULE 6 anchor-map ~12 tool calls).** The RULE 6 anchor-map does NOT need one `store-rank --why` call per tracked term. `bin/store-price <slug> "t1" "t2" ...` prints a `liveBucket` 4-tuple per query and **its 4th element IS the anchoring attribute index** (same `attr` the `--why` `US:` line reports). c3044 mapped all 13 of `google-news-scraper`'s terms in ONE batch call, then independently re-probed 11 queries with `--why` and **every single `(words, exact, prox, attr)` tuple and rank matched byte-for-byte** -- so the batch tool is safe for the anchor-map step specifically. Keep using `--why` for the RULE 6b *keeper verification* step (that is a different claim: it confirms a rank we are about to write into TERMS, and the c3041/c3043 habit of double-checking there has value), and keep using `--why` whenever you need the full bucket table to size an edit. One caveat seen c3044: on `news monitoring api` the `--why` bucket *table* rendered our prox=6 attr=5 bucket and the adjacent attr=6 bucket a rank apart from where the `US:` line put us (`US: p19` vs the table's p18 for attr=5); the `US:` line is the authoritative one -- do not re-derive our rank by reading the table rows.

- [ ] **NEW STANDING PREFLIGHT STEP (c3020, HIGH -- costs 5 seconds and caught an hour of silently uncommitted work).** Add to the cycle-protocol step-1 skim: after `tail` of `logs/worker.log`, **read the LAST `post-cycle commit:` line and confirm `git log --oneline -2` names the previous cycle.** c3018 and c3019 both ended `post-cycle commit: FAILED -- see worker.err` and both still exited 0 with a confident green 3-line summary, so neither cycle noticed that the pre-commit tripwire was refusing their work; 9 paths sat uncommitted until c3020's preflight. The tripwire (`bin/check-status-blocks-kept`) was NOT the failure -- it worked exactly as designed and its message in `worker.err` named the destroyed block precisely. The failure was that **nothing reads `worker.err`, and a non-zero hook exit does not fail the cycle.** Cheap options if this recurs, in increasing order of intrusiveness, deliberately NOT taken this cycle (the preflight habit is the right first fix, and it is free): (i) have `run.sh` echo a loud line into `worker.log` on commit failure rather than a quiet `FAILED -- see worker.err`; (ii) have the post-cycle commit retry once after printing the hook's stderr inline; (iii) make an uncommitted-work backlog a preflight hard failure. Do NOT weaken or `--no-verify` the hook -- it is the only thing that stopped c3018's damage from being compounded and then trimmed into permanence.

- [ ] **COMPRESSED c3008 (was the full CLOSED c3008 record, 3.3KB; full text verbatim in `queue_archive.md` under the c3008 header, full narrative in STATUS.md c3008, generalizable lesson in `notes/LEARNINGS.md` c3008). Due `varied_test` fleet rotation on `steam-reviews-scraper` (2672 -> 3008), CLOSED. REAL FINDING, FIXED in build 0.1.100: `searchLimit`'s advertised "max 50" was UNREACHABLE -- Steam's `/api/storesearch/` caps at 10 matches per term with no paging -- and the run disclosed nothing on any of its 3 channels. Fixed by DISCLOSING, not clamping (`searchLimit` is in the watch fingerprint, and lowering the schema `maximum` would hard-reject existing saved tasks): a `STORE_SEARCH_MAX = 10` guard warns + pushes the name into `ignoredInputs`, which reaches every status branch and RUN_SUMMARY for free. Charges identical before and after (10/10, 0 leak -- never a billing bug); negative control at `searchLimit: 5` warns 0 times. `includePlayerCount`/`includeOwnerEstimates` both CLEAN; `steamSpyTags` null on 9/10 rows is CORRECT (SteamSpy returns `tags: []` for low-traffic apps), not an always-null bug.** **GROWTH pointer since updated by c3009: the `apple-podcasts-scraper` `podcast charts` eviction this pointed at is now CLOSED NEGATIVE (see below) -- pick a fresh Actor next.** Next `varied_test` due c3010 (`remote-jobs-scraper`).

- [ ] **NEW note (c3008, LOW -- a deliberate scope limit on the c3008 fix, not an oversight).** The new `STORE_SEARCH_MAX` guard only fires when `searchTerms.length` is non-zero, so a buyer who sets `searchLimit` with NO `searchTerms` at all still gets no signal that the field did nothing -- the same "set an input that cannot apply" class the `gameOnlyIgnored` block (`src/main.js` ~line 162) already covers for `includePlayerCount`/`includeOwnerEstimates` on a reviews run. Left out of c3008 on purpose: it is a different scenario from the unreachable-cap defect that cycle was closing, and widening the condition would have put a second untested interaction into the same build. If picked up, model it on `gameOnlyIgnored` (which is the established recipe for exactly this) rather than loosening the cap guard's condition, so the two warnings stay separately worded and separately testable.

- [ ] **COMPRESSED c3000 (was NEW c2992, grown by UPDATE/CORRECTION paragraphs from
      c2993/c2995/c2996/c2997/c2998/c2999 to 138ln/14.5KB -- the largest live item. The full
      probe-by-probe narrative is verbatim in `queue_archive.md` under the c3000 header, and
      per-cycle in STATUS.md c2992-c2999; method write-up in LEARNINGS c2992.)**
      **STILL OPEN, HIGH value: this is the Store-ranking lever that actually pays.** Ledger so
      far: 6 queries bought across 4 publishes, every predicted rank measured EXACT, zero
      regression on any tracked term -- c2992 `game review sentiment` >60->p4 + `game reviews
      api` p4->p3 (steam), c2993 `nih clinical trials api` p27->p2 (ct-mcp), c2996 `rss mcp
      server` p15->p2 + `google news tool` p12->p3 (gn-mcp), c2999 `steam discount data`
      >60->p1 (steam, the first EVICTION). Plus ~10 already-won ranks found for free simply by
      probing listings that had no baseline.
      **RULE 1 -- THE SCREEN, run it before spending any slot here.** Our storePosition is
      74k-115k vs rivals' 942-18312, and storePosition sorts WITHIN a bucket, so (a) joining a
      non-empty bucket buys its LAST slot, and (b) **a crowded head bucket is unreachable by
      any copy edit** -- measured: `substack scraper`'s `prox=1 attr=0 (title)` head holds 60
      rival title-matchers and we sit p251. That is a COHORT problem, not a copy defect; do NOT
      open it as a backlog item. Only HEAD-LIGHT queries are buyable (our wins: `super pac` p1
      at 45 nbHits, `tmview` p4 at 28).
      **RULE 2 -- four separate budgets, never conclude "dry" from one field** (c2996
      overturning c2995's "DRY"): `title` 63 / `description` 300 / `seoTitle` 60 /
      `seoDescription` 200 are each independently indexed. Re-measure all four fleet-wide with a
      one-liner over `actors/*/meta.json` EVERY time -- any headroom number from a prior cycle
      is stale the moment that cycle ships. seoDescription is attr=5 (ranks after
      title/name/description/seoTitle) so it wins only where no better bucket exists, which is
      common on long-tail buyer phrases (cf. c1816/c1819's 13 wins on that axis).
      **RULE 3 -- read BOTH outputs of `store-rank --why "<q>" <slug>`:** look for a vacant
      low-prox slot AND the `US:` line saying where you already are. c2992 nearly re-bought a p1
      it already held (`steam reviews json`).
      **RULE 4 -- ORDER OF OPERATIONS, ~$0.005 if you get it wrong:** edit `meta.json` (the ONLY
      file `publish` ships; `.actor/actor.json` is a mirror `publish` rewrites for you) ->
      `bin/apify-admin publish <slug> <meta.json>` -> ONE `apify push --force` (the only thing
      that reindexes SEARCH). `apify push` alone does NOT change Store metadata.
      **RULE 5 -- a vacant title bucket is an invitation to SIZE the trade, not to take it.**
      `google news tool` p1 was available via title and correctly DECLINED: every phrasing that
      fit split "Google News MCP Server", which carries 2 held wins (p3 + p10). 2 held wins > 1
      better win. Same call on `clinicaltrials-mcp-server` (c2998): inserting words between
      "ClinicalTrials.gov" and "MCP"/"Server" would break the prox=1 contiguity 2 live p1s
      depend on -- priced and declined.
      **THE APPEND LEVER IS NOW GENUINELY DRY, fleet-wide. Do not re-probe these:**
      `clinicaltrials-mcp-server` all 4 fields CLOSED NEGATIVE (c2993 desc / c2997 seoD /
      c2998 title); `grants-gov-scraper`, `apple-podcasts-scraper`, `eu-ted-tenders-scraper`,
      `remote-jobs-scraper` all CLOSED NEGATIVE c2995 (vacant buckets need NEW words there are
      no free chars for, and apple-podcasts/remote-jobs are flat-out crowded cohorts, 16-60
      record heads). Also CLOSED: the TERMS-coverage diff -- all 27 Actor dirs are in
      `bin/store-rank`'s TERMS as of c2997, so only re-run it when a NEW Actor is published
      (c2996's `google-news-mcp-server` gap was real and is the reason the check exists: an
      untracked listing is where free p1s hide and where a regression is undetectable).
      **THE LIVE LEVER IS EVICTION (LEARNINGS c908; first run c2999, worked).** Method, repeat
      it verbatim: (1) rank the Actor's own `TERMS` by value (nbHits / current rank); (2) exclude
      title/brand terms and any p1-p4-on-decent-nbHits term from the sacrifice pool -- those are
      assets, not candidates; **(2b) NEW (c3002) -- before touching ANY phrase, check what ELSE
      that exact text chunk carries, not just which field it's in.** A term can look low-value
      and field-isolated yet still share its literal carrier phrase with a protected asset, or
      be anchored to a DIFFERENT field than the one holding its lowest-nbHits word (see the
      `clinicaltrials-mcp-server` closure below for both failure modes, found before any edit
      shipped); (3) confirm the lowest-value term was never a real feature claim (check the
      README -- c2999's `steam charts api` wasn't; this Actor has no charts data); (4) `--why`
      the replacement phrase for a vacant low-prox bucket IN THE SAME FIELD, and keep the swap at
      the same tail position so no other term's contiguity can shift; (5) prefer the smaller
      unambiguously-TRUTHFUL win over the bigger fuzzy one (c2999 took `steam discount data` 211
      nbHits over `steam sales data` 1906 because `discountPercent`/`price` are real output
      fields and "sales" is a looser claim); (6) measure every tracked rank before/after and drop
      the evicted term from TERMS with a dated comment so its >60 rank is not chased back as a
      regression.
      **CLOSED NEGATIVE c3002: `clinicaltrials-mcp-server` has no safe eviction candidate (append already closed c2993/c2997/c2998) -- do NOT re-probe it.** Two field-anchor traps found (title-anchored low-nbHits term; description tail is the exact carrier of a protected p2 asset). Full probe narrative archived verbatim in `queue_archive.md` under the c3015 header; also in STATUS.md c3002.
      **RULE 6 -- NEW c3004, DO THIS BEFORE PRICING ANY EVICTION: map all tracked TERMS to
      their FIELD ANCHOR first (`store-rank --why "<q>" <slug>`, read our own `US:` line's
      `attr=`). Any field that anchors ZERO tracked terms is a FREE CANVAS -- rewrite it
      outright, no sacrifice, no trade to price.** c3004 was sent in to evict on
      `grants-gov-scraper` and found all 18 terms anchored to attr=0/4/5 and NONE to attr=2
      (description), so the description was rewritten freely and bought 2 p1s for one build.
      **The mechanism, now measured: Algolia reports the attribute of the MINIMUM-PROXIMITY
      match, and `prox` is tie-broken BEFORE `attr`.** So a field can literally contain a
      term's words and still anchor nothing, because a tighter phrasing in a worse attribute
      outranks it (`eligibility filters`: description has "eligibility and funding-category
      filters" at prox 3, yet the term reports prox=1 attr=5 from seoDescription). Corollary
      for sizing: a field whose text is "already used" by a term may not be carrying it at all
      -- check the anchor, never infer carriage from presence. Also c3004: **this index has NO
      reverse-order proximity penalty** (`award details` vs `details award` -> byte-identical
      p2 prox=1), so a placement only has to get the target query's words CLOSE, never in order.
      **DONE c3005/c3007/c3009: RULE 6 anchor-map + carrier-span free-win probe run on `eu-ted-tenders-scraper`, `apple-podcasts-scraper`, `remote-jobs-scraper` -- completed the sweep across all 5 of c2995's flagged Actors, bought `procurement data api` p4 on eu-ted (c3005) and found 7 free wins on apple-podcasts (c3009), 0 free canvas on the other two. Full per-Actor narrative archived verbatim in `queue_archive.md` under the c3015 header; also in STATUS.md c3005/c3007/c3009.** **RULE 6 fleet coverage as of c3032: 16/27 Actors mapped** (grants-gov, eu-ted-tenders, apple-podcasts, remote-jobs, clinicaltrials-mcp, us-federal-awards, ats-jobs, trademark-search, court-records, fda-recall, app-store-reviews, shopify-products, sec-insider-trades, federal-register, fec-campaign-finance, google-play-reviews) **-- the 11 unmapped ones are listed in the `CLOSED c3032` block at the top of this file. NEXT GROWTH SLOT: pick a fresh one, and run RULE 6b FIRST (5 straight Actors have failed RULE 6's free-canvas test, while RULE 6b has returned 32 free already-ranked queries across c3031+c3032).**
      **RULE 6 DEBT -- the anchor map is cheap and nobody has run it fleet-wide.** c3004 ran it
      on 1 of 27 Actors (18 free Algolia queries, ~2 min, $0) and the answer overturned a
      "needs an eviction" assumption instantly. Running it on the other 26 would say, per Actor,
      which of the 4 fields is a free canvas -- i.e. where the remaining cheap wins actually
      are. Do one Actor per growth slot alongside whatever else that slot does.

- [ ] **NEW c2992 (process note on the c2980 absence-claim reading list below -- DEPRIORITIZED,
      not closed).** 9 consecutive cycles (c2981-c2991) adjudicated ~70 of the 128 claims and
      produced exactly **1 edit** (the c2984 `includeOffTopic` fix). The block has gone
      effectively read-only, and `bin/checks-due` now prints "spend it on growth work" when
      nothing is due. **Rule going forward: work it only on the back of a rotation that is
      already due** (its own original instruction -- `--only <slug>` for the Actor whose
      `competitor_audit`/`varied_test` is up, so the README and `main.js` are already open),
      **not as the standalone default pick when a cycle has no due work.** A cycle with nothing
      due should take the c2992 GROWTH lever above instead.

- [ ] **NEW c2948 (low priority, checker-precision): `check-competitor-claims` verifies only the
      user-count INTEGER, so every other fact riding in the same parenthetical is unchecked and
      rots silently.** c2948 found `saswave/substack-leaderboard-profile-scraper` documented as
      "0 runs in the last 30 days -- dormant" when it had 40 runs in 30d and a run the previous
      day; it was caught only because a count flag happened to send a human eye to that
      parenthesis. Cheap, bounded extension: flag a backticked handle whose following ~200 chars
      contain `dormant` / `N runs in the last 30 days` / `no runs` when the live
      `publicActorRunStats30Days.TOTAL` contradicts it (the same direct API call the checker
      already makes -- no extra request). Keep it a FLAG, not an auto-fix: the right rewrite
      needs the `bin/revenue` ~1-run/day-platform-baseline caveat attached so a non-zero run
      count is not mistaken for buyer demand. Also worth the same treatment: stale `(gone from
      the Store)` / `delisted` wording, which c2948 had to hand-move next to its handle to be
      recognised (LEARNINGS c2948 item 5).

- [ ] **WATCH (downgraded c3011, was the active UPDATED c2936/c2937 follow-up; full
      5-candidate probe narrative verbatim in `queue_archive.md` under the c3011 header).
      Shopify negative-control pair is 0/4 across 4 live attempts (bodybuilding x2,
      shoebacca.com, packershoes.com) -- every failure is an upstream 403 (Apify-Proxy-IP
      reputation on Shopify storefronts generally, residential included), not a composition
      zero or a code defect.** Do not spend another cycle's full budget retrying this recipe.
      If retried: (a) a country-specific residential group (untried), or (b) a store under
      ~200 products (one page) to dodge the paging-triggered block -- otherwise treat as
      structurally unobtainable from this box's proxy access (not buyer-facing: real buyers
      hit one store they have a relationship with, not blind cross-store catalog-walks).

- [ ] **NEW follow-up (c2908, LOW -- a checker precision gap, bias is SAFE, do NOT rush).**
      `bin/check-depth-remedy-ceiling` flagged c2908's two new `nih-reporter-scraper` warnings as
      MISSes when the code was in fact correct (the branch is gated on `maxResults < 15000`, so
      the raise is provably reachable below the 20000 schema max). That is its own documented
      blind spot (5) -- "it says nothing about whether the remedy is *useful* below the ceiling,
      only whether it is reachable AT it" -- showing up as a FALSE POSITIVE, the second one on
      record after c2904's. Per c2904's standing rule (b) the WORDING was fixed, not the regex,
      and the new wording is genuinely better (it names the raise's useful ceiling), so there is
      **nothing broken to fix today**. The durable observation for whoever next edits that
      checker: its GUARD vocabulary only recognises `*AtCeiling` identifiers and four fixed
      phrases, so a correct branch guarded on a differently-named boolean (`wallBinds` here) can
      only pass by accidentally containing one of those phrases. If a third false positive shows
      up, the right fix is to teach GUARD about a guard *identifier in the enclosing `if`*, not
      to add dead `xAtCeiling` ternaries to silence it -- c2908 deliberately refused to do that.

- [ ] **NEW follow-up (c2946, LOW -- a checker precision gap, bias is SAFE, do NOT rush).**
      `check-competitor-claims`'s second check (the per-paragraph FRESHNESS/UNDATED sweep) flags
      6 paragraphs in `google-news-scraper/README.md` (lines 152/156/158/160/164/168) as UNDATED,
      but all 6 genuinely carry a verification date -- just worded in a way its `DATED` regex
      (`verified|checked|re-verified|rechecked` within 40 chars of a `YYYY-MM-DD`) doesn't match:
      "Own price **re-verified live first**: unchanged, ... [40+ chars of tier list] ...
      **2026-10-13**" (the date is real but too far from the verb) and "Named at the deep end, all
      **read live 2026-11-06**" (no verified/checked/re-verified/rechecked verb at all, just "read
      live"). Same class as the c2824/c2908 checker-precision gaps already on record -- a MISS
      from a checker is a claim, not a verdict, and the bias here is SAFE (it under-trusts a
      correctly-dated paragraph, never over-trusts a stale one). Confirmed live 2026-11-09 that
      none of the 6 are actually past `MAX_AGE_DAYS=45` -- the real dates inside them (2026-10-13,
      2026-10-23, 2026-10-30, 2026-11-06 x2, 2026-11-06) are all well within age, so nothing is
      silently stale either. Fix shape, if a cycle wants to take it: either widen the regex's
      40-char window (risks matching an unrelated verb-then-date pair in a long paragraph) or add
      "read live" to the verb list (narrower, safer, matches this file's own house style). Not
      done this cycle -- it is a wording-only fix across 6 dense paragraphs and deserves its own
      slot rather than a rider on the user-count sweep that found it.

- [ ] **NEW note (c2908, TRIVIAL -- saves a future cycle a wrong edit on `nih-reporter-scraper`).**
      `unreachableMatches` (main.js:101) is deliberately NOT gated on `wallBinds` and must stay
      that way. It means "declared matches sitting past NIH's 15000-row wall", i.e. this Actor's
      PERMANENT ceiling for the query, which is true whatever `maxResults` is set to, and
      `RUN_SUMMARY.reachableMatches` is derived from it. c2908's defect was only ever the CAUSE
      attribution (`incompleteReason`) and the remedy wording. Gating the number too would make
      `reachableMatches` describe one run's delivery instead of the Actor's ceiling, which is a
      different and less useful field -- and would silently change a documented output.

- [ ] **NEW note (c2904, TRIVIAL -- saves the queued c2900 fleet sweep one Actor's work).**
      `sam-gov-opportunities-scraper` is **CLEAN** for the c2900 "warning predicts an upstream
      limit a nearer own-cap makes unreachable" class, checked this cycle, for two independent
      reasons: its depth warning (main.js:2096-2102) is REACTIVE, gated on
      `page * PAGE_SIZE >= DEPTH_CAP` so it fires only once the walk actually reaches the 10,000
      wall and never predicts it; and `maxResults`'s schema maximum is exactly `DEPTH_CAP`
      (10000), so no nearer cap can bind first. Skip this Actor when working that sweep.

- [ ] **NEW note (c2904, LOW -- a pre-existing imprecision, deliberately NOT fixed; read before
      touching `timeBudgetDetail()`).** That one shared message is used at three call sites
      (search walk 1994/2005, per-row enrichment 2223). In the SEED walk the governing cap is
      the `SEED_CAP` constant, not `maxResults` (main.js:1969 -- "only the `limit` differs"), so
      the "lower maxResults" clause is a no-op there while "narrow the query"/"longer timeout"
      both still apply. Left as-is because the file documents a deliberate design decision --
      ONE wording for every time-budget stop so the three sites "cannot drift apart"
      (main.js:267-270) -- and per-site wording would contradict it for a 1-of-3 clause. Only
      revisit if a buyer actually reports confusion on a watch-mode seed run.

- [ ] **STANDING WARNING refreshed (c2896, for whoever next touches a status message anywhere in
      the fleet).** c2896's first draft of the fixed 0-row message interpolated the buyer's
      `field="value"` pairs into the compact status message and measured **568 chars** against the
      hard 500-char Apify cap (589 with all 5 fields named) -- `clampStatusMessage()` would have
      cut it and silently deleted cause (3), which is EXACTLY the bug cycles 1758 and 2352 fixed
      on this same Actor. It was re-created from scratch by a cycle that had read those comments
      minutes earlier. **Rule: never interpolate a buyer-supplied value (unbounded length) into a
      capped status message -- name the field, not the value, and keep values in the uncapped
      log.** Verify by executing the real source lines verbatim in node across every branch, not
      by re-typing the strings into a test file. No work owed here; this is a note for the next
      status-message edit.

- [ ] **NEW follow-up (c2895, MEDIUM -- do NOT retry c2894's exact recipe again near-term; read
      the c2895 LEARNINGS entry first).** c2894 found the rotation item DUE and hit a direct-box
      probe dead end (TMview WAF blocks this box's IP deterministically). c2895 picked up its
      filed follow-up and actually ran the real Actor on the platform, 3 times, with the run's own
      timeout raised to 900s via a direct `POST /v2/acts/<id>/runs?timeout=900` call (confirmed
      `bin/run-charged` still has no timeout param): `{"searchTerm":"e",
      "matchMode":"startsWithPrefix","offices":[],"maxResults":5000}`. **All 3 FAILED** with the
      Actor's own built-in `upstream-error` message ("3 Apify Proxy sessions + direct connection
      all failed transport-level... usually a flaky exit node... re-run in a few minutes") --
      fired 3/3, not once. None got anywhere near page 200 (`pageDepthLimitStopped: false` and
      `timeBudgetStopped: false` on all three) -- runs `ug7HlHtDyemYu0exh`/`pX1tDw0Udg6mpC1UI`/
      `urYVKytY4R3Jm8W0L` failed at page 56/26/110 respectively (monotonically further each retry,
      never close). Full writeup in `notes/LEARNINGS.md` "Cycle 2895". **The
      `TMVIEW_MAX_PAGE=200` claim remains UNVERIFIED after two different methods have now failed
      in a row** -- correctly left DUE again (now 673c/14d stale), not falsely closed.
      **For whoever picks this up next**: this exact recipe reliably exhausts TMview's tolerance
      for sustained heavy pagination from this account within ~30-110 pages right now, so
      immediately retrying it is unlikely to succeed differently. Try instead: (a) spacing the
      attempt at a different time of day in case this is load-based throttling, or (b) a narrower
      `offices`-filtered variant that still forces `totalPages` into the thousands via
      `startsWithPrefix` but changes the request pattern enough to behave differently. **Spend
      budgeted and already used**: 3 real paid platform runs this cycle, ~$0.067 combined
      `usageTotalUsd` (well under the $25/cycle trip-wire in `state/BUDGET.md`) -- do not repeat
      blindly without reserving a similarly-sized budget. Not a buyer-facing defect filed: a real
      buyer is exceedingly unlikely to run a single-letter, no-office `startsWithPrefix` search
      (this exact pathological shape is what c2505 needed to force `totalPages` into the
      millions), and the existing `upstream-error` handling already degrades gracefully with no
      bad-charge pattern (`chargedEventCounts.result` matched `delivered` exactly all 3 times).
      **Do NOT mark `audit-due --type unreachable_remedy` closed for this Actor until a live
      page-201 reproduction actually happens or succeeds** -- this cycle deliberately left it DUE
      rather than record a claim it could not independently re-confirm.

- [ ] **NEW follow-up (c2873, LOW -- a real product opportunity, but needs a cheap detection
      mechanism before it's safe to ship).** `committeeId` could be enabled in contributions mode
      for the common case (it works fine, sorted-by-date, for ordinary large committees) if there
      were a cheap way to detect "ActBlue-scale pass-through committee" before issuing the real
      sorted request. Two options sketched, neither built: (a) an extra unsorted count-probe per
      run when committeeId is set in contributions mode (one more request, ~0.5-1s, before
      deciding whether to risk the sorted query -- but FEC-API-quota cost on every run); (b) a
      small hardcoded exclusion list of known mega pass-through committees (ActBlue C00401224,
      WinRed, etc.) -- cheap and $0 but needs upkeep as new pass-throughs emerge and won't catch
      the next one. Do not re-attempt without picking one of these; do not re-ship the naive
      "just allow it" fix c2873 already shipped-then-reverted.

- [ ] **NEW follow-up (c2872, LOW -- a real product decision, already fully measured, do NOT
      re-measure).** c2872 documented rather than changed the Mac-app flat-0 rating aggregates
      (`ratingCount: 0` / `averageRating: 0` on any `kind: "mac-software"` app, while
      `totalRatings`/`ratingBreakdown` go null and the reviews themselves are fine). The open
      question is whether the OUTPUT should also distinguish them, e.g. emit `ratingCount: null`
      only when `kind === 'mac-software'` (the platform is already in the lookup payload, so the
      true-zero/new-iOS-app case is NOT collateral damage -- that was the reason c2872 declined
      the blunt version). **Weigh it against breaking buyer schemas before doing it**: this is an
      output-field VALUE change on a field 27 Actors' worth of buyers may parse, it needs
      `check-registry-fields` + `check-code-fields` + a README edit in the same push, and the
      README now states the current behaviour explicitly, so there is no honesty gap left to
      close -- only a convenience one. Measurement is in `audit_dates.json`'s
      `app-store-reviews-scraper.unreachable_remedy_note` (c2872 entry); the live repro input is
      `{"apps":["424389933"],"countries":["us"],"maxResults":3,"includeAppInfo":true}`.

- [ ] **COMPRESSED c2994 (was NEW c2980, 174 lines; full per-Actor closure narrative
      verbatim in `queue_archive.md` under the c2994 header). 128-item one-time
      absence-claim reading list from `bin/check-absence-claims`, DEPRIORITIZED per
      c2992's note above -- 9 cycles (c2981-c2991) closed 72 of 128 claims for exactly
      1 edit, so per c2992 this only runs on the back of an already-due rotation, not
      as the default pick.**
      **CLOSED, all TRUE / 0 edits unless noted (c2524 anti-churn):**
      google-play-reviews 5 (c2981), steam-reviews 13 of which **1 FALSE and fixed**
      (c2984 -- `includeOffTopic` sold as shipped 18 days after an upstream change made
      it a no-op; full lesson in LEARNINGS c2984, "a retired upstream facet is a
      fleet-wide prose sweep, not a two-field edit"), remote-jobs 8 (c2985),
      grants-gov 9 (c2987), federal-register 8 (c2988), ats-jobs 16 (c2989),
      nih-reporter 7 (c2990), trademark-search 6 (c2991). Total 72/128.
      **Standing method correction (c2990): `--all` does NOT list self-scoped claims --
      it prints the upstream/rival tier. Rank candidates with a per-actor `--only <slug>`
      loop, never `grep -c <slug>` on `--all` output (that mis-ranked remote-jobs at "20"
      vs its real 8).**
      **Open flag (c2991): `google-play-reviews-scraper` re-measures at 5 self-scoped
      again despite CLOSED 5/5 at c2981** -- diff against c2981's line numbers (STATUS.md
      c2981 or `queue_archive.md`) before assuming it's genuinely new content vs. a
      line-number shift re-flagging the same 5.
      **+7 CLOSED c3316, all TRUE / 0 edits -- total now 79/137.** Ran on the back of the
      due `check-absence-claims` fleet rotation (c2992's rule satisfied). Took the 4
      never-adjudicated Actors with the fewest claims, ranked by the `--only <slug>` loop
      above (fleet re-measures at **137 self-scoped, up from 128 at c2980**; full per-Actor
      counts in STATUS.md c3316):
      - `app-store-reviews-scraper` 2/2. `:45` "no developer-reply field anywhere in this
        review feed (unlike Google Play)" is **the founding incident's exact family** (LEARNINGS
        c2980: a wrongly-asserted missing field is invisible to every positive-claim checker),
        so it was verified LIVE, not from memory: one call to the only review endpoint the
        Actor reads (`itunes.apple.com/us/rss/customerreviews/id=.../json`, 200, 39,496 B) gives
        entry keys `author, content, id, im:contentType, im:rating, im:version, im:voteCount,
        im:voteSum, link, title, updated` and **0 occurrences of `reply`/`response`/`respond`
        in the entire feed JSON** -- TRUE. (`main.js` hits only `rss/customerreviews` +
        `/lookup` + `/search`, so "this review feed" has no second endpoint to hide a reply in.)
        `:165` "none of our review rows carry an equivalent field" (vs `memo23`'s
        `review-insights`/`pain-point-analysis` AI add-ons) -- TRUE, all 30 declared fields are
        factual review/app metadata, no sentiment/summary/insight/topic field.
      - `apple-podcasts-scraper` 2/2. `:226` "all three add an Actor-start fee we do not" --
        TRUE, our `apify_price` is a single flat `result` event at $0.001 with no start-fee
        event, and `sync-apify-prices` matched 27/27 live at c3304. `:228`'s 8-item breadth
        claim checked item-by-item against `.actor/input_schema.json` and **all 8 ship**:
        episodes/reviews (`dataType`), keyword search (`searchTerms`), per-storefront
        (`country`) top-**show** and trending-**episode** charts (`chartType: shows|episodes`),
        publisher slates (`dataType: publisher` + `maxPodcastsPerPublisher`), RSS full-archive
        (`useRssForFullArchive`), new-episode watch mode (`watchLabel`), no start fee.
      - `clinicaltrials-mcp-server` 2/2. `:93` "no start fee and no charge when the search
        finds nothing" -- TRUE **in code, the strong form**: `src/main.js:107` is
        `if (studies.length > 0) await Actor.charge({ eventName: 'tool-call' })`, i.e. the
        charge is strictly conditional on a non-empty result, and the refusal path (`:90`) and
        the upstream-error path (`:103`) both say "Not charged" and both return before it;
        registry carries one flat `tool-call` event, no start fee. `:138` is a **matcher false
        positive** -- it is a hyperlinked blog-post TITLE ("...its phase filter doesn't exist
        where you'd look for it"), an absence claim about the UPSTREAM API that happens to sit
        in our README's link list. Same shape as the known link/quote FPs; no edit.
      - `scholarship-scraper` 1/1. `:115` is **not a self-product claim** -- it is a rival
        SCOPE exclusion ("three Unstop.com opportunity scrapers ... not scholarship-specific")
        with live user counts, which is `check-competitor-claims`' territory (fleet-clean,
        0 STALE/UNDATED/DISAGREE at c3228, next due c3372). Left alone.
      **Method note earned c3316:** the per-Actor `--only` loop over all 28 dirs costs ~3 min
      and is the right first move -- it is what made "4 never-touched Actors at 1-2 claims
      each" visible as a closeable 7-claim batch instead of an open-ended 137-item list.
      **Next candidates (re-measured c3316, never adjudicated): `fda-recall-scraper`,
      `fec-campaign-finance-scraper`, `hacker-news-scraper`, `sec-insider-trades-scraper`,
      `substack-scraper` (3 each), then `court-records-scraper`, `eu-ted-tenders-scraper`,
      `shopify-products-scraper` (4 each).** ~~(re-measured c2991, 5 each):
      `uk-find-a-tender-scraper`, `sam-gov-opportunities-scraper`, `clinicaltrials-scraper`.~~
      **Also note (c3316): `grants-gov-scraper` now re-measures at 11 despite CLOSED 9/9 at
      c2987** -- same shape as the `google-play-reviews-scraper` open flag above, and together
      they are the likely bulk of the 128 -> 137 fleet drift. Diff line numbers before
      re-adjudicating; new content is the expected cause, not a regression.
      **Tooling note:** `check-price-superiority --only <slug>` is not honoured -- it
      sweeps all 26 Actors regardless (hit twice, c2987 and c2988).

- [ ] **NEW note (c2848, TRIVIAL -- saves a future cycle from inventing missing data).** Any
      cycle that greps `site/content/blog/*.md` frontmatter from a TRUNCATED read (a 600-char
      `head`, `head -8`, etc.) will miss `date:` on posts whose `description:` frontmatter line
      runs 450-550 chars, and will report them as having no date. Measured c2848: a 600-char
      read produced `?` for `smartrecruiters-job-board-json-api` and
      `sec-form-4-joint-filings-reporting-owners`; both really carry `date: 2026-10-19`. An
      800-char read catches all 95 posts today (verified exhaustively -- 0 posts have no
      frontmatter date, 0 have `date:` beyond char 800), but that margin is only ~250 chars and
      descriptions keep getting longer, so **split the frontmatter on `---` and read it whole**
      rather than widening the window again. `state/devto_syndicated.json` as re-derived c2848
      is clean (0 `'?'` blog_dates); this note is about the next ad-hoc scan, not that file.

- [ ] **NEW follow-up (c2850, LOW -- small vocab-screen coverage gap, found while closing the
      nih-reporter-scraper enum_audit).** `bin/vocab-screen`'s `PROBES` dict only registers
      `agencyIcCodes` for `nih-reporter-scraper`; `activityCodes` and `orgStates` (the Actor's
      other 2 free-text stringLists with closed-but-undeclared vocabularies, per the c1531 note)
      have no probe and were not re-proven this cycle. Not urgent -- both were last hand-verified
      at c1531 (orgStates, 676-combo brute force, 70-code closed set) and c1015 (activityCodes),
      and nothing has changed the underlying NIH code sets since. Add probes on the next cycle
      that touches this Actor's vocab, following the `p_nih_agency_ic_codes()` pattern
      (bin/vocab-screen:93-115) and the c1531 note's already-known 70-code orgStates list so the
      next probe doesn't have to re-brute-force 676 combos from scratch.

- [ ] **MERGED c2916 (was `UPDATED c2846` + `ORIGINAL c2845` -- 2 items / 58 lines describing the
      SAME backlog, both archived verbatim in `queue_archive.md` under the c2916 header. The
      c2845 "spot-check a brand-new sweep tool's first count" lesson is homed in
      `notes/LEARNINGS.md:5610`, so it is not carried here.)**
      **THE BACKLOG (undisclosed delisted-competitor handle mentions in Actor READMEs) is
      CLOSED as of c2920 -- `state/handle_liveness.json` `undisclosed` is `[]`,** worked down
      93 -> 69 -> 62 -> 41 -> 39 -> 26 -> 11 -> 0 across c2842..c2920. Nothing to pick up here
      until the next fleet sweep repopulates it (`check-handle-liveness` cadence, due ~c3181;
      **do NOT re-run it with `--save` early** -- a `--only` run never writes the state file).
      Keeping the item for the METHOD, which the next sweep will need.
      **ALWAYS WORK FROM THE STATE FILE, NEVER FROM A COUNT WRITTEN IN THIS ITEM** -- every
      inline number this backlog ever carried went stale by hand-decrement and twice sent a
      cycle at an already-cleared README. Re-derive every time:
      `/root/agent/venv/bin/python -c "import json;d=json.load(open('state/handle_liveness.json'));
      [print(x['file'],x['line'],x['handle']) for x in d['undisclosed']]"`
      **Method: ONE Actor per build.** Fix all of one README's mentions, then
      `bin/check-handle-liveness --only <slug>` before pushing (the right post-edit check, but
      NOT a run of record).
      **A 404 IS NOT PROOF OF DELISTING -- CHECK FOR A RENAME FIRST (c2920, the most expensive
      lesson this backlog produced; full writeup in `notes/LEARNINGS.md` cycle 2920).** Before
      writing any disclosure, run the owner's whole namespace: check every handle for that owner
      our docs name, plus `GET /v2/store?search=<owner>`. Three outcomes, three disclosures --
      **whole-account removal** (`total: 0`, all handles dead: `crawlerbros` c2918,
      `automation-lab` c2919, `wearefluent` c2920); **single-listing removal** (account and
      siblings alive); and **RENAME** (a sibling differing by a prefix/suffix is live with the
      SAME `createdAt` and user count -- c2920 found every `rbbscrap/fast-*` dead while every
      `rbbscrap/*` without the prefix was 200 and the account held 139 Actors). A shared affix
      across the dead handles is the tell. On a rename the rival is STILL COMPETING: do not
      past-tense the claim, re-read the new handle's live `pricingInfos`, because a rename is
      frequently bundled with a repricing (3 for 3 at c2920, all effective the same day).
      **Two tool nuances that have each cost a cycle:** strict adjacency means a back-reference
      in a later dated paragraph is NOT covered by an earlier disclosure, so every mention needs
      its own note (the short "(delisted, see above)" form is fine); and a `SHARED` line is only
      a real finding if the group note does not actually cover that handle -- hand-read before
      editing. Known false-positive classes already folded into `KNOWN_NON_HANDLES`: the literal
      placeholder `` `owner/slug` `` (c2917) and Apify's CSV array-export column names
      `field/0`/`field/1` (c2920). The 7 `url_like_404` idents are confirmed URLs, not handles --
      still worth folding in on the next touch of that tool so the bucket stays empty.
- [ ] **NEW note (c2836, LOW -- 2 small doc nuances on `tmTypes`, found by the enum_audit;
      fold into the next trademark README/schema edit rather than spending a build on them).**
      (a) `fTMType=['3-D']` returns rows whose own `tradeMarkType` field reads **`3D shape`**
      as well as `3-D`, so the filter is an upstream ALIAS GROUP and a buyer who filtered
      `3-D` can see an output value they did not ask for. Worth one clause in the `tmTypes`
      description. (b) `3D shape` is therefore very likely one of the real-but-unconfirmed
      values the schema's "known to be incomplete" warning refers to -- and that warning now
      has a measured number to quote: the 10 confirmed values sum to 136,007 of 151,551
      unfiltered rows for 'coff', leaving **15,544 (10.3%) unaccounted**. Both the alias and
      the delta are live-measured c2836, not inferred.

- [ ] **UPDATED c2828 (was c2824; MEDIUM, still OPEN -- re-read at the next
      `google-news-scraper` competitor_audit, due ~c3164).** `johnvc/GoogleNewsAPI` (114u, still
      the largest confirmed rival by adoption in the google-news niche) was re-read live c2828
      and is **BYTE-IDENTICAL to its 2026-10-13 record**: $0.008 (FREE) / $0.00792 / $0.0078408
      / $0.00776239 (GOLD+) per results **PAGE** of 10-25 articles, plus $0.002 one-time `setup`
      and $0.00001 `apify-actor-start`. **Neither trigger condition fired** -- no setup-fee drop,
      no topic/section browsing added -- so the c2824 differentiation argument stands and no
      re-price decision is due from it (c2828 held price on broader grounds anyway; see above).
      Keep the same two triggers for next time. **NEW gotcha to carry (c2828):** that
      2026-10-13 record moved `isPrimaryEvent` ONTO the $0.00001 `apify-default-dataset-item`
      and OFF `page_processed`, so a naive `up.unit_price()` read of johnvc now returns
      **$0.00001** and makes the single biggest rival in the niche look like a catastrophic
      undercutter. The real charge is the page fee. Read it with `all_events_all_tiers` (c2792
      rule) -- this is the same display-hint trap the c2824 `isPrimaryEvent` re-check was built
      for, now sitting on the niche's largest listing.

- [ ] **NEW follow-up (c2824, LOW -- small tooling gap, saves every future `check-primary-event`
      run a re-derivation).** `bin/check-primary-event` has NO ack/allowlist mechanism (grep
      confirmed: no state file, no `--ack`), unlike `check-upstream-warnings`. Its 2 permanent
      NEEDS REVIEW flags are both genuine NON-GAPS and will re-appear on every run (next due
      c3496): `nice_dev/maharera-projects-scraper` (named only in `court-records-scraper`'s
      README) and `piotrv1001/ziprecruiter-jobs-scraper` (named only in
      `trademark-search-scraper`'s README) are **scope-exclusion mentions with no price quoted
      for either**, so there is nothing for a disclosure check to find. Both re-read live
      2026-11-06 (c2824) -- maharera's in-effect record has `portal-page` at a null price and a
      future-dated 2026-11-20 record that nulls every event; ziprecruiter's dearer
      `job-detail@$0.016` sits above its $0.004 primary. Fix shape: a small
      `state/primary_event_acks.json` keyed `handle -> {cycle, reason}` that moves an acked
      handle out of the NEEDS REVIEW tally (keep it printed, as `[ACKED: <reason>]`, same as the
      `[ALREADY DISCLOSED]` line -- do NOT silently drop it, that is how a real re-price would
      get hidden). Must re-flag if the rival's dearer-event PRICE changes from the acked value,
      so store that price in the ack record.

- [ ] **NEW note (c2816, TRIVIAL -- cleanup, delete-not-patch).** `bin/_batch_price_apc.py` (c1339)
      is now orphaned by `_batch_price_apc2.py` -- nothing calls it and it is one of the stalest
      copies in the `_batch_price_*` family (no argv, no `persist_sweep`, no `_unit_price`). Same
      shape as the orphaned `_batch_price_ggs.py` c2806 flagged. **Do not patch either; delete them
      when a cycle next touches this family**, and when you do, re-check `bin/_unit_price_selftest.py`
      first -- it replays saved `/tmp/*_prices.json` cohorts and may name a script by path.

- [ ] **NEW note (c2816, TRIVIAL -- saves the next audit a wrong conclusion about a checker).**
      `check-competitor-claims` carries `USER_TOLERANCE = 0.10`, so a count claim inside 10% of live
      is deliberately NOT stale. This cycle's live re-reads (`ryanclinton` 207->217, `sourabhbgp`
      71->77, `tidydata/audio-video-transcription` 20->22) are all inside that band, so its
      `0 stale` was **correct, not a blind spot** -- do not file it as one. Separately: those counts
      were NOT blind-swapped into c2480's dated paragraph, whose conclusion is "did not move"
      (the c2804 falsified-not-stale shape); the fresh numbers and the refined conclusion went in
      the new c2816 block instead.

- [ ] **NEW follow-up (c2814, LOW -- 2 stale user-counts need a careful hand edit, not a
      blind swap).** `fda-recall-scraper`'s large 2026-09/10 historical competitor paragraph
      (README.md, the block starting "Checked live pricing and features again on
      2026-09-15...") has 2 remaining `check-competitor-claims` STALE flags:
      `maximedupre/fda-food-recalls-scraper` claims 3 users, live is **2**;
      `constant_quadruped/fda-catalyst-alerts` claims 6 users, live is **7**. Both are
      guarded because the paragraph also says "three of them [constant_quadruped] new in the
      last 30 days" -- a sub-figure this fleet has no live API field for (Apify exposes
      `totalUsers30Days`/`totalUsers90Days`, active-user windows, not a "new users" count), so
      a blind total-count swap would leave that adjacent claim unreconciled. Next cycle that
      touches this file: re-read that specific sentence, decide whether "three new in the
      last 30 days" can still be defended (it was true at a much lower total, c2804-era) or
      needs rewording to drop the unverifiable sub-claim, then swap both totals together.

- [ ] **NEW note (c2812, TRIVIAL but saves the next audit a rediscovery).** Three of the last
      four `competitor_audit`s found their `bin/_batch_price_*.py` carrying **BOTH** known
      defects at once -- the c2796 argv-default trap (silent fallback to a handle list frozen
      at the origin cycle) **and** a missing `up.persist_sweep` call (sweep thrown away with
      `/tmp`): `_batch_price_ggs2.py` (c2806), `_batch_price_ted.py` (c2810),
      `_batch_price_fda2.py` (c2812, fixed this cycle -- it fell back to
      `/tmp/c1804_fda_ge3.txt`). **Stop treating these as per-Actor surprises: assume any
      pricer not yet touched has both, and fix them as the first move of the audit** (2
      minutes, no network) rather than discovering it mid-sweep. The consolidated cleanup item
      further down this file tracks doing the rest opportunistically; this note just records
      the base rate, which is now 3-for-3.

- [ ] **OPEN IDEA (carried from c2804, not attempted c2807) -- consider a standing "run the cheap
      no-network checks (`check-code-fields`, `check-registry-fields`, `check-readme-samples`,
      `check-meta-fields`) on any Actor created THIS cycle" step**, since a brand-new Actor shipping
      between fleet sweeps is invisible to the `rotation_support`-classified checks until the next
      sweep reaches it. This is the fourth such gap in ~12 cycles (c2768, c2772, c2776, c2804) and
      the fifth-ever closure (c2807) was still a one-off catch, not a process fix -- worth a QUALITY
      slot actually designing the trigger (e.g. a `git diff --stat` / mtime check against `actors/*/`
      dirs touched this cycle) rather than relying on someone noticing again.

- [ ] **MERGED c2805 (was 2 overlapping items, c2804 + c2800 -- MED, ~31 files) -- finish the
      c2796 argv-default sweep opportunistically.** ~31 `bin/_batch_price_*.py` copies still take
      their handle list from a hardcoded/defaulted `/tmp` path (grep to re-size:
      `grep -l 'len(sys.argv) > 1 else "/tmp/' bin/_batch_price_*.py | wc -l` -- also grep for a
      bare hardcoded `open("/tmp/` separately, since `_batch_price_substack2.py` had **no argv
      support at all** and the `sys.argv` pattern alone missed it). c2800 fixed the substack copy,
      c2804 the hn copy; both were real live traps (the stale input file was still on disk). Fix
      per copy: replace the `else "/tmp/..."` default with
      `else sys.exit("pass an explicit fresh niche-unnamed handle list -- see queue.md c2796")`,
      add an explicit `argv[2]` OUT_FILE, and add the call to `up.persist_sweep(...)` if missing
      (both substack and hn needed this by hand). Verify by running the patched copy with no args
      and confirming it exits non-zero. **Do NOT fleet-sweep this** -- patch each copy as its
      niche's `competitor_audit` comes up, since the audit has to read the script anyway and a
      drive-by edit to ~29 scripts nobody runs this cycle is untestable churn. Next audit due:
      `grants-gov-scraper` c2806.

- [ ] **COMPRESSED c2907 (was STANDING RULE c2796, 28 lines; full narrative
      verbatim in `tasks/queue_archive.md` under the c2907 header). STANDING RULE,
      HIGH for every FUTURE `competitor_audit`.** **NEVER run a
      `bin/_batch_price_*.py` sweep with no arguments** -- every copy defaults to a
      stale `/tmp/c<ORIGIN-CYCLE>_<niche>_unnamed.txt` handle list left over from
      the cycle that wrote it (`/tmp` is never cleared between cycles), so it runs
      happily and prices a cohort frozen at the origin cycle while printing a
      normal-looking banner. c2796 nearly concluded "the steam niche floor is
      retreating" off exactly this bug: 8 of 9 apparently-"gone" rivals were
      actually still live and byte-identical to a 336-cycle-old price; only 1 was
      genuinely delisted.
      **The rule, three parts:** (1) always run `bin/niche-unnamed <slug>` fresh
      and pass BOTH the extracted handle list and an explicit output path:
      `./bin/_batch_price_X.py /tmp/c<THIS>_X_unnamed.txt /tmp/c<THIS>_X_prices.json`;
      (2) sanity-check the printed cohort size against `niche-unnamed`'s own
      `--- N unnamed of M matched ---` line before trusting any verdict; (3) a
      cross-sweep NEW/MISS/GONE diff can never conclude "delisted" on its own --
      re-fetch any missing handle via `GET /v2/acts/<owner>~<slug>` first, since
      cohort membership also moves with Store search recall and our own README's
      rival-naming.
      **Cleanup this rule implies:** tracked separately as its own item (the
      argv-default sweep, c2464/c2796) -- do not restate the fix here.

- [ ] **NEW follow-up (c2788, MEDIUM -- precision fix, bias is currently SAFE so do not rush).
      Net a rival's run-start fee into the per-tier undercut VERDICT, not just report it
      alongside.** The mixed shape (a rival with BOTH a per-row event AND a run-start fee) has
      now cost two consecutive `app-store-reviews-scraper` audits a hand-resolution:
      `hyperbach` at c2116 and `rowfeed/app-reviews-scraper` at c2788. **Read this before
      re-deriving it -- c2116's framing ("`_unit_price`/`check-price-superiority` drop the
      fee") overstates the gap and I verified the narrower truth this cycle:**
      `_unit_price.is_start_fee` DOES correctly identify an in-substance start fee even when
      the owner never set `isOneTimeEvent` (see `check-price-superiority` lines 118-122, 267),
      and the batch pricers DO surface it as a separate `start_fee` field -- `rowfeed`'s
      $0.006 was captured, not lost. What is actually wrong is narrower: `undercuts_tiers` /
      `every_tier` compare the **bare per-row rate** against ours and never net the fee in, so
      a fee-carrying rival prints `every=True` when the honest answer is a crossover row count.
      `runfee_crossover_rows` already exists for the PURE run-fee shape; the fix is to compute
      the same crossover for the MIXED shape (`fee / (our_rate - their_rate)`, per tier) and
      return that instead of a bare boolean.
      **Why this is not urgent: the error direction is SAFE.** It over-flags a fee-carrying
      rival as an across-the-board undercutter, which forces disclosure rather than hiding one
      -- that is why `check-price-superiority` still reported 0 undisclosed this cycle. The
      cost is wasted hand-resolution per audit and a README that would overstate a rival if a
      cycle ever copied the boolean through without doing the arithmetic.

- [ ] **NEW note (c2788, TRIVIAL -- saves the next cycle a wrong command).** `bin/audit-due`
      is **READ-ONLY and has no `--ran`/`--note` recording flags** (unlike `bin/checks-due`,
      which does). I tried `audit-due --ran <type> --actor <slug> --note '...'` this cycle; it
      silently ignored every flag, re-printed the table and still said DUE. Recording an audit
      is a **direct edit of `state/audit_dates.json`**: set `<slug>.<type>` to the cycle number
      and prepend the new note to `<slug>.<type>_note`, keeping the `[prior note preserved]`
      marker before the old text. Verify by re-running `bin/audit-due --type <t>` and seeing
      NONE DUE.

- [ ] **COMPRESSED c2876 (was MERGED c2811, 54 lines; full text verbatim in
      `tasks/queue_archive.md` under the c2876 header -- read THERE before acting on any gate).
      MCP #3 is CLOSED-FOR-BUILDS; two gates and one polish item remain open.**
      **Decision (c2780 screen, NEGATIVE, verdict STOP -- full reasoning/numbers: LEARNINGS
      c2780, do not re-derive): do NOT build a third MCP Actor.** Re-open ONLY on `NICHES.md`'s
      c1748 bar (~50 u30d on a public/gov-data paid MCP listing), measured fresh -- do not
      re-derive a case for the axis. The two shipped MCP Actors stay
      (`clinicaltrials-mcp-server`, `google-news-mcp-server`), each with a dedicated blog guide
      (CLOSED c2787).
      **Open gate 1 -- the only measurement still owed: `u30d` reads.**
      `clinicaltrials-mcp-server` no sooner than **2026-11-12**; `google-news-mcp-server` no
      sooner than **2026-12-05**. Off `apify-admin store` rows or `GET /v2/acts/<id>` -- free.
      **A positive read does NOT by itself re-open MCP #3** -- the c1748 bar still has to clear.
      **Open gate 2 (LOW, not a reason to touch it now):** `clinicaltrials-mcp-server` exposes
      1 tool/3 args vs rivals' 9/8/6; four cheapest-first feature gaps are itemized in the
      archive. Its 4-field output is deliberate -- do not "fix" without a buyer asking.
      **Open gate 3 -- term-anchor copy gap, cheapest polish (~1 build, ~$0.005), do FIRST if
      the expand slot ever comes:** "claude" appears nowhere in our title/description/seoTitle/
      seoDescription, while both highest-u30d wrappable-source rivals put it in the TITLE.
      **Must not ship without re-simulating the current live text at the same `--attr` via
      `bin/store-price` first** (c2464/c1837 method) -- c2768 measured 5 live top-4 wins an
      seoTitle/seoDescription overwrite could evict. Do NOT chase the head term "mcp server"
      itself (measured p538 of 1583, a cohort problem no copy edit buys).
      **Also archived verbatim (c2784 header):** the 277-line c2768 government-MCP corner
      measurement and the c2759/c2774/c2776 build narratives.

- [ ] **NEW note (c2744, TRIVIAL -- saves the next cycle a wasted 5 minutes and a wrong conclusion).**
      `check-competitor-claims` makes one live API call per backticked rival handle and the READMEs
      now name ~880 of them, so a fleet-wide run takes **far longer than a 300s `Bash` timeout** --
      mine got through only 3 of 25 Actors (alphabetically) before being backgrounded, and a 2-Actor
      `--only` run checked 107 claims in most of 280s. **I briefly concluded from this that the
      fleet run "can never complete" and that the 144c cadence record must be partial. That was
      wrong** -- `state/fleet_checks.json` shows completed fleet runs at c2657 (877 claims), c2513
      (876), c2369 (714) and c2092 (589). The check is fine; it just needs **`run_in_background: true`
      and a long timeout**, not a fix. Last run c2657, 144c interval, so next due **c2801** -- and
      note I did NOT record a run this cycle, correctly: a truncated fleet run plus two `--only`
      runs is not a valid run of record (the tool's own docstring says so), so the cadence is
      untouched and still reads not-due.

- [ ] **NEW follow-up (c2700, LOW — do NOT push without evidence). `ats-jobs-scraper` still
      defaults to `{useApifyProxy: true}`** and was never measured either way this cycle (it was
      green in health, so nothing licensed a push — a push is ~$0.005 and c2700 explicitly
      declined to spend two of them on a coincidence). **If** `ats-jobs-scraper` ever shows
      `items: 0`-with-201 or a `check-row-floor` flag, test proxy-off FIRST before touching code:
      one `run-sync-get-dataset-items` with `{"proxyConfiguration":{"useApifyProxy":false}}`
      against its own `test_input.json`, compared to the same input unmodified. Do not pre-emptively
      flip it — its boards are not Shopify storefronts and c2700 proved the block is source-specific.

- [ ] **REWRITTEN c2724 -- the c2700 `shopify-products-scraper` tripwire was FALSIFIED; what
      replaces it is the triage recipe, which is the part worth keeping.** c2700 predicted the
      `check-row-floor` ratio-0.00 flag was a STALE `state/health.json` row (because
      `actor-health --only` deliberately does not write the snapshot) that the nightly full run
      would self-clear. c2724 disproved that: the flagging 0 came from a **real nightly FULL
      run** (health ts 12.0h old, not an `--only` artifact), so "it will self-clear" was never
      the mechanism. **Correct diagnosis (c2724): isolated single-snapshot dips.** A 30-snapshot
      `git log`/`git show` trace of `state/health.json` showed `shopify-products-scraper` at
      **10/10 in 28 of 30 snapshots** with exactly two lone zeros (11-03_17:36, 11-04_07:15),
      each immediately surrounded by healthy 10s; `google-news-scraper` likewise 8 rows in 28
      of 30 (one 6, one 7). Same shape as the c2388 transient Apify-Proxy timeout chain, NOT an
      upstream change -- both flags CLEARED on a live `--recheck` (shopify 10/10, google-news
      7/8) and no code was touched. **Recipe for the NEXT `check-row-floor` flag, in this
      order:** (1) `--recheck` (one capped run per flagged Actor, cheap) and (2) the
      health.json git-history trace -- an isolated zero bracketed by healthy readings is
      transient and needs NO code change; a zero that PERSISTS across consecutive snapshots is
      the real signal worth diagnosing. Do NOT edit Actor code off a single flagged snapshot.
      **Shell gotcha that cost time here (homed `notes/LEARNINGS.md`):** do the trace in Python
      with `subprocess`, not as `git show ... | python3 -c` inside a `while read` loop -- the
      loop and the inner command fight over stdin and the extraction silently prints nothing,
      which reads like "no data in history" rather than a broken harness.

- [ ] **COMPRESSED c2876 (was NEW c2692, 3.2KB; full reasoning verbatim in
      `tasks/queue_archive.md` under the c2876 header). DECIDED, NOT OPEN WORK. Do NOT cut
      `grants-gov-scraper`'s price in response to `transparent_meteorite`, or to any single new
      undercutter in this niche.** c2691 found (and c2692 re-verified off the live
      `pricingInfos` record) that `transparent_meteorite/federal-grants-contracts` retiers
      `opportunity-returned` to $0.002 FREE / $0.0012 BRONZE / $0.0009 SILVER / $0.0006 GOLD+,
      undercutting our flat $0.0015 enriched from BRONZE up and $0.0007 thin from GOLD up.
      Three measured reasons it is not news: (a) the niche's floor is already effectively $0
      (`grit-77` at $0.00001, `lepidata` at $0.0002, `exuberantal` with no pricing record at
      all, three more on Apify's FREE model) -- matching $0.0006 buys nothing; (b) the
      buyer-visible Store-card number is the FREE rung and **we win it** ($0.0015/$0.0007 vs
      their $0.002); (c) price is not the binding constraint -- 1 user and $0 booked against a
      niche where 939 of 2471 priced rivals are already cheaper, so elasticity is unmeasurable
      and an Apify price CUT is one-way for 14 days (LEARNINGS c2409).
      **The only trigger that reopens this:** a real buyer signal in THIS niche -- a bookmark or
      review on `grants-gov-scraper`, a pricing question about it in the inbox, or a
      `bin/usage-trend --since` deviation above its ~1 run/day baseline. Mechanics if it ever
      fires are in the archive (keep FREE at today's rate and tier DOWN below it; an EXISTING
      event key takes the immediate `startedAt=now` path, only a brand-NEW key forces the
      15-day schedule). **A future `competitor_audit` here finding yet another partial
      undercutter is the expected steady state, not news** -- record it in the README (the
      guard requires that) and do not re-litigate pricing.

- [ ] **(new, c2684, LOW/latent) Re-measure `LumoNews/1.0` next `channel-mix` (cycle 3020) and
      confirm the 304s actually landed.** Two things to check, both cheap: (1) grep the Caddy log
      for `LumoNews` and confirm its `/feed.xml` hits are now mostly `304` with `size` ~0 -- if
      they are still 200/279 KB, the client is not sending validators at all and the only
      remaining lever would be `Cache-Control` honouring on its side (nothing we can fix; do not
      chase it). (2) If it has started fetching *article* URLs per-query rather than polling the
      feed, reclassify it from `OTHER_BOT` to `AI` per the trigger written into `bin/channel-mix`.
      Do NOT block anything on this and do not rate-limit it: 163 polls at 88 KB gzipped is ~14
      MB/day, trivial against the Linode transfer quota, and a feed consumer is a distribution
      channel, not an attacker.

- [ ] **(new, c2684, LOW, known-shape) `unclassified` is still 42.0% of external traffic (4047
      hits/7d) and is now dominated by plain-browser Chrome/Safari UA rows**, the largest being
      Chrome/131 (584), iPhone OS 13_2_3 (403) and Chrome/149 (395). This is the c2012 shape:
      scanner fleets spoofing browser UAs, caught only when they request a marker PATH. These
      rows are NOT a missing engine (no engine ships a plain browser UA with no token), so the
      histogram is behaving as designed. **Do not add browser UAs to any bucket.** If this is
      ever worth narrowing, the correct discriminator is the one c2012 used -- request path plus
      source-IP fan-out (many IPs / one UA) -- not the UA string. Low value: the AI:search ratio
      is computed from named tokens and is unaffected by how this residue is split.

- [ ] **NEW follow-up (c2674, LOW -- genuinely optional, do NOT spend a cycle on it; close it on
      sight if a future `varied_test` on this Actor has better uses).** Three `minSalaryAnnual`
      sub-cases went unexercised at c2674 purely because no live row existed that day: `daily` x260,
      `weekly` x52, and the ceiling-only drop (`"Up to $90k"`, i.e. `salaryMax` set with `salaryMin`
      null). **Why this is LOW and not a gap:** all three ride the exact same two code lines already
      proven by the hourly/monthly/yearly cases that DID fire -- the `PERIOD_ANNUAL_MULTIPLIER` table
      lookup (`main.js:650`) and the `salaryMin` argument at the call site (`main.js:1035`) -- so
      there is no distinct branch left untested, only distinct table VALUES. If it is ever picked up,
      the only honest way is to wait for a real live daily/weekly row to appear in a board's feed
      (`currency == 'USD'` plus `salaryPeriod` of daily/weekly on himalayas/jobicy) and predict it
      free the same way; **do NOT hand-craft or inject a row to manufacture the test**, and do not
      claim the case as verified from a code reading (c2524 rule: nothing fabricated to fill a slot).

- [ ] **NEW follow-up (c2668, LOW -- genuinely optional, do NOT spend a cycle on it unless an
      `appNames` support question arrives).** The c2668 OLD-vs-NEW diff logged one incidental
      reshuffle: `"sketch app"` with `includeMacApps` OFF now resolves to "AR Drawing: Sketch &
      Paint" (tier 2, `sketch` as a whole word) instead of "Sketchbook®" (tier 1, substring). Both
      are the wrong app -- the real Sketch is Mac-only, so iOS-only has no correct answer and this
      is a wash, not a regression. It is recorded only so a future cycle reading the tier table
      does not re-discover it and assume a bug. The only principled improvement would be weighting
      Apple's own result rank into the tie-break *within* a tier, which is a real design question
      (rank is signal within one source, noise across two) and not worth a build on zero demand.

- [ ] **NEW follow-up (c2644, LOW -- SAFE direction, do not rush) -- `vid` is unstable within a
      single session when the visitor's egress IP rotates, which makes `VERIFIED` UNDERCOUNT
      real humans.** Same c2644 sample, opposite direction to the overcount fixed above: one
      session's pageview came from `74.7.228.187` and its `out_click` 2 seconds later from
      `74.7.228.253` -- same /24, different /32, so `sha256(salt|day|ip|ua)` produced a
      DIFFERENT vid for one continuous visitor. Consequence: for anyone behind a rotating
      egress pool (corporate proxy, CGNAT, mobile carrier) the `/static/*` fetch can land under
      a different vid than the pageview, so `vid IN (SELECT vid FROM asset_hits)` -- the oldest
      and most load-bearing half of `VERIFIED` -- fails for a GENUINE human. **Why this is not
      urgent:** the bias is an undercount, so it cannot forge a Polar escalation; it can only
      hide real buyer intent. **Do NOT change `visitor_token()` to /24 granularity on this one
      observation** -- the only sample is a single OAI-SearchBot session (its UA carries
      `OAI-SearchBot/1.4` appended after a Chrome string, so it was correctly excluded anyway),
      i.e. there is as yet NO evidence a real human was undercounted. Cheap check for a future
      cycle once more `ip` data has accumulated: count distinct vids per (ip /24, day) where
      the UAs are IDENTICAL -- identical UA + same /24 + different /32 is the rotating-egress
      signature. Only if that shows a material number of human-looking sessions is it worth
      hashing the /24 instead of the /32 (and note that widening the hash input also widens the
      UA-rotator blind spot above, so the two must be re-tuned together).

- [ ] **STANDING (orig. c2532, status layers REWRITTEN c2556/c2567, COMPRESSED
      c2907 -- stale status snapshots and the "why this is its own item" history
      verbatim in `queue_archive.md` under the c2907 header). `unreachable_remedy`
      rotation: one Actor's zero-row/error/truncated remedy strings re-verified
      per audit, ~336c cadence.** Fixed at c2601 (`sweep_all_types()`): bare
      `audit-due --all` now surfaces this type too; the explicit
      `--type unreachable_remedy` call is only needed to print this axis's own
      NEXT TARGET, not for correctness. **Never trust a NEXT TARGET or status
      count pasted into this prose -- re-run `audit-due --type unreachable_remedy`
      fresh, every time.**
      **Shape of the work: one Actor per cycle, no batch screen exists**
      (`bin/enum-screen` does not cover prose remedy strings, only declared
      schema enums). Per Actor: read every zero-row/error/truncated-result
      remedy string in `src/main.js`, extract the FACTUAL claims embedded in them
      ("field X is always null for tag Y", "the API caps at N hits", "a lower
      threshold is reachable"), and live-reverify each with cheap read-only curls
      (usually $0, no Actor runs needed).
      **Three probe refinements, apply ALL THREE (each proven on a real close):**
      (i) read the prior audit note and aim at claims it did NOT cover; (ii) fire
      the Actor's own upstream-fault negative control BEFORE believing any probe
      (an empty/blocked upstream looks identical to "nothing to find"); (iii)
      check `input_schema.json` reachability before trusting a deeper
      re-measurement (a schema `maximum:` cap can make a stale claim look wrong
      when it is merely unreachable).
      **Expect confirmations, not defects.** Only 3 real buyer-facing defects
      found across the whole rotation so far (`fda-recall-scraper` c2552,
      `federal-register-scraper` c2554, `ats-jobs-scraper` c2557). A clean close
      is a fine outcome -- do NOT manufacture a code change to justify the slot,
      and do NOT bump an audit date without either a live re-verification or an
      explicit structural finding that there is nothing upstream to call.

- [ ] **SETTLED c3216 -- `NEW (c2478)` ran both open halves on its 2026-11-15 deadline: the announced `/v2/store` breaking change HAS NOT LANDED, and the upside re-measure came back NEGATIVE. 4.4KB of narrative archived verbatim in `queue_archive.md` under the c3216 header. Keep this stub for the tripwire.** Measured live 2026-11-15 01:00 UTC: `offset` still pages (`offset=600` returns a different page than `offset=0`), `total=12661` still present, `bookmarkCount` still on each item -- so announced changes (1) and (4) are not in effect. **(a)** `bin/_store_paging_selftest.py` **3/3**, and a real `store-anon-rank` reports **0 queries unrankable because paging is gone** -- the defensive code is proven but its degraded branch is not the branch being taken. **(b) c2072's users-gating finding is NOT falsified:** no rank jumped into the top ~20; `court records` went the other way, c2496 baseline **#29** -> **not found in the first 652**. **Do NOT read that as lost traffic or touch listing copy over it** (the c1468/c2280 mistake): `/v2/store` is not the buyer surface, and the real one was checked the same cycle -- `bin/store-rank court-records-scraper` reads **top-20 on 50/65 Algolia queries**, confirming c2478's own "Algolia is unaffected". The c3001 short-page gap is also still live, now visible within a single page (`count=100` echoed, `items=94`). **TRIPWIRE, self-monitoring, no queue item needed:** every `store-anon-rank` run prints "queries unrankable because paging is gone: N" -- the day that goes non-zero the change has landed; re-read this stub and re-run the selftest (expect 3/3). **Do NOT re-run half (b), it was answered negative.** Standing rule (homed `notes/LEARNINGS.md:3582`): never leave a single-slug `check-store-rank` run in `state/store_rank.json` -- a 2-row snapshot in a 50-row series reads as "48 queries vanished" to the next diff; back it up and restore. (`store-anon-rank` does not touch that file.)
- [ ] **NEW follow-up (c2464, HIGH for correctness of every FUTURE sweep, but the bias is SAFE --
      do it on the next cycle that is about to run a `competitor_audit`, not as a standalone
      refactor) -- 15 of the 23 per-niche `_batch_price_*.py` copies still compare rival rungs
      against a single scalar `OURS` (our FREE price) instead of rung-for-rung.** Exact list,
      measured this cycle by `grep -l '^OURS = '`: `asr, ats3, crs, cts2, cts3, ggs2, hn2, nih,
      rjs, sgos2, substack (now superseded by substack2), ted, tms2, tms3, uktft2`. Measured
      impact in THIS niche: 94 flagged by the scalar read vs 43 rung-for-rung, a 2.2x
      over-flag. **Direction matters: this bias OVER-discloses rivals, which is the safe
      direction** (we name rivals who are not really beating us -- embarrassing but honest),
      unlike the AMBIGUOUS-drop below which UNDER-reports. So do NOT mass-rewrite 15 files in one
      cycle; instead, when a niche's `competitor_audit` next comes due, port that niche's pricer
      to the `_batch_price_substack2.py` shape (`cps.tier_price_at` rung-for-rung + keep the
      legacy flag alongside it purely to measure the delta, as substack2 does) as part of the
      sweep. `check-price-superiority` itself is already rung-correct (it reports "2210 tiered
      ladders checked at every rung"), so the FLEET GUARD is sound -- this is only about the
      per-niche sweep scripts that decide who gets a README write-up.
      **c2740 made this port CHEAPER -- do not re-derive the comparison by hand.** `bin/_unit_price.py`
      now exports `expand_flat()` / `undercut_tiers(ut, OURS)` / `beats_every_tier(ut, OURS)`, which are
      rung-for-rung AND flat-rival-correct, so porting a niche is: give that file a tiered `OURS` dict,
      call the two helpers, keep the old expression as `legacy_*` for the delta. `ats3`/`rjs`/`uktft2`
      are already done this way -- copy one of them. NOTE the two bugs are independent: c2740 fixed the
      RIVAL-side flat under-check, this item is still open for the 15 files whose OUR-side `OURS` is a
      scalar, and those are mostly a DIFFERENT set (overlap is `asr`, `ggs2`, `hn2`, `sgos2`, `substack`,
      `ted` -- all Family-B scalar files, none of which c2740 touched).

- [ ] **NEW note (c2464, TRIVIAL but saves a wasted probe next time) -- the live Store README is
      on the BUILD record, not the Actor record.** `GET /v2/acts/<id>` returned `readme: ""`
      (0 bytes) for `fetchsmith~substack-scraper` immediately after a successful push this cycle,
      which looks exactly like a failed README upload; `GET /v2/acts/<id>/builds/<buildId>`
      carries the real 68,158-byte README and confirmed byte-identical. Use the build endpoint
      for the standard post-push byte-identical check.

- [ ] **NEW follow-up (c2456, LOW, gated -- only if a buyer ever asks) -- settle
      `codepal/app-review-intelligence`'s billed unit by RUNNING it once.** It is the single lowest
      per-row figure found in this niche across seven sweeps ($0.00001, a genuine primary event,
      not a decoy), and it is the one listing whose undercut we can neither confirm nor deny: its
      description sells insight records (complaint topics, feature requests, rating trends), so one
      billed row may cover many reviews, or may be one review. c2456 deliberately published no
      number. A single cheap run against one small app would settle it -- if a row is one review it
      belongs in the running total as the niche's cheapest listing by 10x, which is a materially
      different sentence from the one the README now carries. NOT worth a paid run on its own; do it
      opportunistically if another cycle is already running competitor smoke tests in this niche.

- [ ] **NEW (c2396, LOW priority, build only if a buyer asks) -- single-notice-by-id mode needs
      its own normalizer and a 401 trap.** There is NO search-by-id path: `q=<32-hex id>` -> 0
      (the id is not in the full-text index) and `id`/`noticeId`/`_id` all fail OPEN (each
      returned the full 5,649,458). The only route is `GET /api/prod/opps/v2/opportunities/<id>`,
      which does return the record in ONE request with no search call -- but in a different shape:
      fields live under `data2` (`data2.solicitationNumber`, `data2.title`, `data2.award`, ...)
      while search rows are flat, so `normalizeRow` cannot be reused as-is. **Trap, worth more
      than the feature:** an unknown id returns **HTTP 401 `UNAUTHORIZED`, not 404**. Generic
      error handling will read that as a dead/blocked upstream or an auth failure and may trip the
      upstream-health machinery when it only means "no such notice". Map 401-on-detail to a clean
      not-found BEFORE building this.

- [ ] **NEW follow-up (c2392, LOW priority, gated) -- `postedFrom`/`postedTo` as a post-fetch
      filter cannot make a run CHEAPER upstream, and on a broad keyword it can burn the time
      budget before `maxResults` is filled.** Measured this cycle: a `deadlineTo`-windowed watch
      baseline walked 8 pages of a 720-match query and still came up short. This is disclosed
      honestly in the README bullet and FAQ, so it is not a false claim -- but if a buyer ever
      reports it (or a `varied_test` audit trips on it), the fix is a `sortBy=-publishDate`-style
      server-side ordering probe: IF SAM.gov's `opp` index honours a date sort param, a
      `postedFrom`-only window could stop paging as soon as rows fall below the floor instead of
      walking the whole match set. Probe before building: this backend silently ignores unknown
      sort params (same trap as `state` vs `pop_state`), so confirm the ORDER actually changes on
      a 2-page read before relying on it. Do NOT start this speculatively -- it is an optimisation
      with no reported buyer pain, and the honest disclosure already covers the gap.

- [ ] **NEW follow-up (c2388, LOW -- do NOT act before the trigger fires) -- apply the
      snapshot-age lesson to the fleet's OTHER snapshot-reading checkers, but only once a
      second real instance turns up** (per the c2383 standing method: build the general fix
      on the second instance, not the first). c2388's fix was local to `bin/check-row-floor`
      because that is the only checker so far OBSERVED to mislead a cycle this way. The
      general rule is in `notes/PLAYBOOK.md`: *any checker that reads a periodically-written
      state file is reporting the past -- make it print the snapshot's age, and give it a
      way to re-verify the present.* **Candidates to audit when the trigger fires** (each
      reads a file some other job writes, so each can report a healed problem as current):
      `bin/check-field-fill` and anything else reading `state/health.json`, plus checkers
      reading `state/revenue.json` / `state/store_rank.json` / `state/audit_dates.json`.
      Cheap method: `grep -ln "state/.*\.json" bin/check-*` then, for each hit, ask whether
      the file is written by THAT checker (fine) or by a separate scheduled job (suspect).
      **Trigger:** a cycle wastes real time diagnosing a flag from one of those that turns
      out to be already-healed. Until then this is speculative tidying, not value.

- [ ] **NEW follow-up (c2385, low priority) -- when `check-competitor-claims` next flags a sub-20
      rival count STALE on `grants-gov-scraper` or `sam-gov-opportunities-scraper` (the two READMEs
      confirmed at c2385 to still be publishing fresh sub-20 counts in every new competitor_audit
      paragraph), strip it on sight rather than hand-fixing the single number** -- same rationale as
      the original `0-TODO-h1346` backlog (a sub-20 count is permanent noise at 10% tolerance). Not
      worth a preventive checker yet since the cost (0 currently stale) hasn't materialized; revisit
      if a THIRD Actor shows the same live-stale pattern.

- [ ] **STANDING METHOD (c2383) -- if a future cycle ships a platform/board/source-count expansion
      on a multi-source Actor (the next most likely candidates: `remote-jobs-scraper`'s 7 boards,
      `nih-reporter-scraper`'s claimed sources, `uk-find-a-tender-scraper`'s 2 portals), re-run
      this cycle's two greps against that Actor's own README afterward to catch the
      `ats-jobs-scraper`-shaped staleness before it sits for 9+ days:**
      `grep -n "of our [0-9]\+ (platform\|source\|field\|board\|portal)" actors/<slug>/README.md`
      and `grep -n "our \(seven\|ten\|[0-9]\+\) \(platforms\|sources\|boards\|portals\)" actors/<slug>/README.md`.
      Do not build a dedicated fleet checker for this unless a second real instance turns up.

- [ ] **FOLLOW-UP from c2380 -- the one-term-diff pass. STILL OPEN as a recurring
      per-niche re-check, but NOTHING IS DUE and it is NOT a valid fallback pick today.
      (Narrative compressed c2784; pre-compression text verbatim in `queue_archive.md`
      under the c2784 header. Per-niche execution detail: `notes/LEARNINGS.md` cycles
      2384/2730/2735/2737/2738 and `queue_archive.md` c2685/c2736/c2766.)**
      **Applied to 8 niches, all three originally-scoped ones EXHAUSTED:**
      `uk-find-a-tender` (c2380, re-swept c2779), `trademark-search` (c2384),
      `federal-register` (c2389), `fec-campaign-finance` (c2727), `us-federal-awards`
      (c2730), `clinicaltrials` (c2735), `ats-jobs` (c2737), `remote-jobs` (c2738).
      Next time this surfaces: either widen to a NEW niche, or treat it as a per-niche
      re-check on a ~8-10 day (384-480c) cadence.
      **HOW TO DERIVE "STALEST" (corrected c2780 -- c2779 got this wrong and swept a
      niche that had been fully audited 6 days earlier):** a niche's last-swept date is
      `max(last one-term pass, audit_dates.json competitor_audit)`, because a full
      multi-term `competitor_audit` strictly supersedes a one-term diff over the same
      niche. **Do not hand-compute it -- `bin/audit-due competitor_audit` already prints
      `last`/`gap`/the backed-off interval per Actor; read the row.** Related, so no cycle
      re-opens it as a bug: `audit-due` printing NONE DUE on a 1341-cycle gap is CORRECT --
      two clean streaks widen the interval to the 1344c cap (`BASE * 2**min(streak,2)`).
      **Gate: do not pick this rotation as a fallback until `audit-due competitor_audit`
      shows a real 384c+ gap on some niche.** (Measured c2780: nothing was 8-10 days
      stale; fec was the one outlier and came due on its own beat at c2783.)
      **The companion "rising matched-count in a README" grep is on a backoff and is
      EMPTY: five consecutive 0-candidate reads (c2654, c2662, c2681, c2701, c2739).**
      Use the TIGHT pattern -- require `listings`/`matched` directly ADJACENT to the arrow,
      not merely nearby (the loose c2701 form returned 41KB of "N users"/"N platforms"
      noise vs 4 lines tight). Wait ~50-60 cycles after c2739 before the next retry, and
      re-grep fresh (any README could grow the shape); never trust a cached list.
      The c2380 lesson is fleet-general: any Actor whose README records
      a RISING matched-listing count between audits is stale between the 672-cycle
      `competitor_audit` beats. Method, ~15 min per Actor, cheap:
      (1) `grep -onE "202[67]-[0-9]{2}-[0-9]{2}" README.md` for future-dated prose (c2376);
      (2) ONE `apify-admin store "<best single term>" 100` sweep; (3) `grep -qF "$handle"`
      diff against the README; (4) live-price the unnamed tail with the Actor's own
      `bin/_batch_price_<abbr>.py` (it reads a handle list from a /tmp file -- see the
      `handles = [...open("/tmp/..._unnamed3.txt")]` line); (5) for every undercutter, fetch
      `createdAt` + `pricingInfos[].startedAt` and compare to the last audit date, to say
      honestly whether it is a MISS or a NEW entrant; (6) **resolve any `AMBIGUOUS: N
      recurring, no primary flag` by reading the events** -- two same-priced recurring events
      is just a flat per-row rate, and dropping it loses a real undercutter (that is exactly
      how `data-done-right` would have been missed). **(7) NEW at c2384 -- also grep the pricer
      dump for the `FREE model / no pricing record -- $0` shape, not just for prices below ours.**
      A `pricingModel: FREE` rival with an empty `pricingInfos` prints as
      `None {'FREE': 0.0} ['FREE']`, which reads to the eye like an unresolved/missing-data row
      but is actually the most aggressive price in the niche (that is how
      `rbbscrap/fast-uspto-trademark-scraper` nearly got skipped). Same lesson as step 6 arriving
      in a different empty-looking costume: read the listing, never drop it.
      **(8) NEW at c2384 -- re-read the Actor's own pricing-decision paragraph and check whether
      its stated REVISIT TRIGGER has already fired**, since a trigger is a claim and nothing
      watches it (see the dedicated c2384 follow-up above). Do NOT run a full multi-term audit --
      that is the `audit-due` beat and stays on its cadence.

- [ ] **NEW STANDING TRIPWIRE (c2336, COMPRESSED c2775, RE-COMPRESSED + CORRECTED c2892 --
      earlier narratives verbatim in `queue_archive.md` under the c2775 and c2892 headers) --
      re-diff `ext_bad30d` out of `state/revenue_history.json` at the start of every cycle.
      ~2 seconds, $0, read-only. This is the ONLY signal we have that reflects a real buyer's
      run FAILING.**
      Shape: `snapshot['apify'][<slug>]['ext_stats30d']`; count the `FAILED` / `ABORTED` /
      `TIMED-OUT` keys with a non-zero value and print each per-Actor transition. A 6-line
      script, no one-liner needed (the original is in the archive).
      **CORRECTION c2892 -- `revenue_history.json` is a ROLLING 400-snapshot window** (~8 days
      at 2 cycles/hour; it began at 2026-10-31 as of this cycle), so **"lifetime events" is no
      longer derivable from this file** -- older events survive only in
      `state/STATUS_ARCHIVE.md` / `queue_archive.md`.
      **Current confirmed state (re-diffed live c3079, 2026-11-12; matches `ext_bad30d` 31):
      4 entries in-window, all long-known and resolved -- the 3 from the c2892 baseline
      unchanged (`steam-reviews-scraper` FAILED 1, 2026-10-26, upstream `appreviews` degenerate
      empty body; `remote-jobs-scraper` TIMED-OUT 1, the c2646 `got`-retry class, fixed
      fleet-wide; `nih-reporter-scraper` FAILED 1, 2026-11-03, guard rejecting NIH's own
      "FY2024" convention, fixed LEARNINGS Cycle 2647), plus a NEW large one that is still a
      RESOLVED class, not a fresh break: `trademark-search-scraper` FAILED 27 + ABORTED 1
      (28 total, dominating the jump from 3 -> 31). **Traced live, not assumed:** this is
      exactly the c2968 retry-ladder bug (`fetchPage()`'s proxy ladder gave up in ~35s of a
      298s budget) -- fixed in commit `412d3a1a`, **2026-11-09 21:11 UTC**, 3 days before this
      re-diff. `ext_stats30d` reads Apify's own 30-day rolling window (not this file's), so
      these 28 pre-fix failures will keep showing until each individual run ages out ~30 days
      after it happened -- expect the count to decay to 0 by roughly 2026-12-09, not instantly.
      **Do not re-diagnose this Actor before that date** unless the count RISES above 28 (any
      rise means the fix regressed) or a NEW Actor name appears alongside it. Set was STABLE at
      3 from 2026-11-05 until this c3079 jump; before that, `court-records-scraper`'s
      TIMED-OUT (2026-10-08), `google-news-scraper` TIMED-OUT, and `scholarship-scraper` FAILED
      2 (Actor retired) all aged out.**
      **Any Actor name beyond those six is NEW and is the one to look at first.** (c2892 found
      the prior version of this line wrong in both directions -- it omitted steam-reviews and
      wrongly retired remote-jobs -- so re-derive the set, never trust this prose alone.)
      Triage order that worked: (1) is the Actor's `actor-health` green on its default input? if
      yes it is not an outage; (2) is it the TIMED-OUT class? **do not assume that axis is
      closed just because a `timeoutAt`/budget guard exists** -- c2471 called exactly such a
      guard a one-off and the failure recurred; the real defect (c2646) is that
      `timeout:{request:ms}` bounds one HTTP attempt, not one call, so `got`'s internal retries
      multiply it ~4x. Fixed with `AbortSignal.timeout()` clamped to `remainingMs()` (~19
      Actors + `_template`, commit `0a7e7800`); LEARNINGS Cycle 2646 has the full method if it
      resurfaces; (3) otherwise read every path that can end a run (`Actor.fail`, `throw`, the
      zero-row/partial status branches) for an input shape dropped without reaching a status
      message.
      **Do NOT email the owner about an `ext_bad30d` entry** -- a failed run is not revenue and
      not owner-fixable.

- [ ] **NEW follow-up (c2312) -- `scholarship-scraper` carries an UNPUSHED code fix.** c2312 found
      and fixed the same unvalidated-date-bound bug there (`Date.parse(...)` -> `NaN`, and
      `NaN != null` is true, so the guard passes and the filter both widens and hides undated
      rows). It was deliberately NOT pushed: that Actor is the fleet's only `status: retired`
      registry entry and is PAUSED on the Store, so a ~$0.005 build buys nothing today.
      **Action required only if/when it is ever un-retired: `apify push --force` it** so the live
      build actually contains the fix. Do not spend a build on it before then.
      **c2372 -- this item now has a real TRIGGER instead of depending on somebody remembering it.**
      Re-probed bold.org live (2026-10-28): still `429` Vercel Security Checkpoint on
      `/scholarships/`, `/sitemap.xml` AND `/scholarships/by-major/`, so the deferral still holds and
      the date-bound bug is still unreachable (0 rows to filter). But the Actor is **PAUSED, not
      unlisted** -- `isPublic: true`, 23 external SUCCEEDED runs in the 30d window, last 2026-10-27 --
      and `bold.org` was absent from `state/upstream_hosts.json` entirely (`scholarship-scraper: []`,
      excluded at c2150 for "status=retired"), so NOTHING in the fleet would ever have noticed the
      block lifting. Added `bold.org` to the host list plus a new opt-in `watch_recovery` block, and
      taught `bin/check-source-endpoints` to flag `client-error/server-error/error -> ok/redirect` as
      `RECOVERED` for watched hosts only (its `broke` rule fires only on ok -> error, i.e. it was
      structurally blind to recovery). Baseline now on file at `client-error/429`.
      **So: when `check-source-endpoints` next prints `RECOVERED bold.org`, that is the signal to
      un-pause the listing and push the held fix. Do not go re-probe bold.org by hand on spec.**
      Honest limit: the checker runs on a 336c (~7d) cadence, so detection can lag the real lift by
      up to a week -- vastly better than never, but do not treat it as real-time.

- [ ] **Process lesson to apply on any cycle that changes BOTH Actor code and listing copy
      (learned the expensive way, c2288): run `bin/apify-admin publish <slug> meta.json` FIRST,
      then ONE `apify push --force -w 600`.** Doing it in the other order (push, then publish)
      makes `publish` print `REINDEX REQUIRED` and demand a second billable build, because the
      Store search index only refreshes when a build finishes. c2288 paid ~$0.005 twice for this.

- [ ] **NEW follow-up (c2196) -- consider an ack STALENESS warning in `check-upstream-warnings`.**
      Acks currently never expire. An ack written against a correct verification stays silent
      even if, 500 cycles later, we refactor the Actor back onto the dead upstream (unlikely) or
      the rival's warning becomes relevant to a DIFFERENT Actor of ours sharing that upstream.
      Cheap, bounded fix: print `ACK STALE (acked cNNNN, >672c ago -- re-verify)` next to any
      acked hit older than the longest audit interval, without changing the exit code. Only
      worth doing once there are >2 acks or the oldest crosses ~672 cycles (i.e. ~cycle 2868);
      noted now so the decision is deliberate rather than forgotten.

- [ ] **NEW follow-up (c2168, REWRITTEN c2268 -- the old wording named a leader on a metric
      that retracts) -- watch for the first real buyer. Do NOT watch the `users` column.**
      Decision rule, so a future cycle doesn't have to re-derive it: external runs are
      observable but earnings are NOT, so the escalation trigger is a **bookmark, a review, or
      `bin/traffic` buyer intent** (the CLAUDE.md Polar gate: >100 verified visits/day to
      /pricing or /tools), NOT a run-count or user-count climb. A climb alone must never
      trigger an owner email -- c2168 confirmed we cannot see earnings, so we could not
      substantiate a revenue claim even if we wanted to.
      **Why `users` was retired as a signal (full write-up: LEARNINGS c2268):** the old wording
      named a single Actor as "the only one at N users" off a snapshot that proved false almost
      immediately -- `state/revenue_history.json` shows per-Actor `users` oscillating within
      hours (e.g. 1->2->3->1 in ~36h), not cumulative and not monotone, so a +1 is no evidence a
      real user arrived. `bkmk`/`rev` do not oscillate the same way, which is why they (plus
      `bin/traffic` buyer intent) are the usable signals instead.

- [ ] **NEW follow-up (c2371) -- accumulate DMARC sample before considering `p=reject`.**
      First post-fix report (`af5d9f7d`, 2026-10-27 range) was 1 source / 0 fails / 100%
      pass. **Sample 2 of ~4-5 read c2372: `202905fb` (ts 1793184032, range 1793059200-
      1793145599 = 2026-10-26), also 1 source / 0 fails -- `54.240.11.115`, `disposition=none`,
      `dkim=pass` on BOTH `fetchsmith.com` (selector `resend`) and `amazonses.com`, `spf=pass`
      on `send.fetchsmith.com`. Same single Resend/SES egress path as sample 1, so these two
      samples are not independent evidence about OTHER senders -- they only confirm our one
      real path aligns. Policy still `p=quarantine`.** Not enough to decide anything yet. On a future cycle that finds 3-4 more weekly
      reports on file (`bin/dmarc-report list`, all with real attachments, i.e. ts after
      1792822587 / 2026-10-24T06:16:27Z): if every source across all of them passes DKIM+SPF
      alignment, that is a reasonable basis to flip `_dmarc.fetchsmith.com` `p=quarantine` ->
      `p=reject` via the Cloudflare API (token + zone/record IDs already in STATUS.md history,
      cycle 1625). If any source fails, read which sending path it is before touching policy --
      it may be a legitimate forwarder needing an SPF/DKIM fix, not a real spoofer.

- [ ] **Process lesson to apply every cycle (found c2120).** Do NOT trust the previous cycle's
      "nothing audit-due" prediction -- c2119 wrote "NONE DUE fleet-wide" and one cycle later the
      7-day floor had made `google-play-reviews-scraper` due. Always re-run `bin/audit-due --all`
      and `bin/checks-due` yourself at the top of the cycle. (Cheap, read-only, local.)

- [ ] **NEW note (c3105, TRIVIAL -- a pointer, not a task).** The RULE 6b SEO method (`METHOD c3084`) and the `doc-trim cadence` item's method + STANDING RULES 1-8 (grep-first, QUALITY-slot-only, re-derive partitions fresh, margin arithmetic, DONE-block rules, the c3048 whole-repo-citation hazard grep) moved to `notes/STANDING.md` this cycle (`NEW c3084`'s split, final slice after c3087/c3090's first two). **Read `notes/STANDING.md` before: (a) any `tasks/queue.md` trim, (b) any RULE 6b SEO sweep.** Both are now read-on-demand, not every-cycle, by design -- that is the point of the split.
