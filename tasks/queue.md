- [ ] **CLOSED c3089 -- Regular/GROWTH slot (3089 % 3 == 2). Preflight all clean:** tree matched HEAD `beac8d8d` (c3088); `inbox-triage new` NONE UNTRIAGED of 78; `bin/revenue` $0 booked, 27 public Actors, 54 users, 1485 runs30d, `ext_bad30d` 31 (still the documented decaying `trademark-search-scraper` baseline, no new Actor name, not re-opened), 0 bookmarks, 0 reviews -- no buyer signal, no owner email owed; `bin/apify-spend` $1.7145/$85 (11.3% elapsed, proj $15.14); services `fetchsmith-web`/`fetchsmith-mail`/`caddy` active, site 200 on `/` and `/tools`; `checks-due --all` NONE DUE (soonest `check-dead-endpoint-docs` in 2c, c3091). **Work: RULE 6b SECOND PASS on `trademark-search-scraper`** (c3088 handoff's first-named candidate by sweep age; first pass c3061, 33 TERMS). Health-gated first (`actor-health --only`, ok=True, 10 items, 0 fail_rows). Read the 4 live `meta.json` fields verbatim, curated 20 NEW n-grams skipping all 33 tracked terms plus the 2 prior screened-out terms (`uspto api`, `applicant data`), batch-priced all 20 in ONE `store-price` call, then individually re-verified EVERY one with `store-rank --why` per the standing c3059 correction. **14/20 matched the batch tool's p1 prediction byte-exact; 6/20 mismatched in rank but were still confirmed real top-60 wins; 1/20 was a true false positive.** **19 keepers shipped (33 -> 52 TERMS)**: `search registered trademarks` (101, p1), `registered trademarks across` (62, p1), `official tmview database` (2, p1), `22 fields` (109, p6), `nice classes applicant` (92, p1), `applicant expiration` (65, p1), `expiration opposition dates` (55, p1), `expiration dates` (1335, p8), `no start fee` (3637, p58 -- **FLAPPING FLAG per c3031**, 50-60 band), `70+ offices` (38, p9), `70+ national and regional offices` (7, p1), `access trademark filing data` (5, p1), `across 70+ offices` (23, p1), `offices via tmview` (10, p5), `status nice classes` (153, p4), `trademark search api with brand protection` (35, p1), `brand protection api and ip monitoring` (47, p1), `filing data trademark registration data` (71, p1), `trademark registration data and trademark classification data` (41, p1). **Screened out 1 false positive**: `start fee` (6813 nbHits, batch pred p1, `--why` confirmed absent from top 60) -- recorded in `bin/store-rank`'s cycle-3089 provenance comment. `ast.parse` clean + `SourceFileLoader` re-import (52 terms, 52 unique, no duplicate); full 52-term probe re-run post-edit, all 19 new terms matched the written (nbHits, rank) exactly, the 33 pre-existing terms byte-identical (append-only). $0 spent, no `meta.json` edit, no build, no publish, no reindex -- doc-only (`bin/store-rank`, `tasks/queue.md`, `state/STATUS.md`). **Blockers: none. Owner email: none owed.** Services/site re-verified 200 post-work. **Next cycle: c3090 is the next QUALITY slot (3090 % 3 == 0)** -- per c3087's `PROGRESS` note on `NEW c3084`, resume the queue.md/STANDING.md split (8 `NEW STANDING*` items, then `METHOD c3084`, then the `STANDING RULES` section, in increasing risk order); re-check `check-doc-size` on both `tasks/queue.md` and `state/STATUS.md` (both flagged TRIM SOON/DUE before this block, which grows both further). Remaining RULE 6b second-pass candidates by sweep age, oldest first: `clinicaltrials-mcp-server` (c3067), `court-records-scraper` (c3070), `fda-recall-scraper` (c3074), `eu-ted-tenders-scraper` (c3076), `apple-podcasts-scraper` (c3077, read its standing audit watch in `notes/STANDING.md` first). `NEW c3088` (5 AGING schema claims) remains open, not yet due to re-flag (checker next due c3568). 2026-11-15 Apify deadline is 3 days out; `NEW (c2478)`'s post-deadline work becomes actionable c3090+.

- [ ] **CLOSED c3088 -- Regular/GROWTH slot (3088 % 3 == 1). Preflight all clean:** tree matched HEAD `92ba4604` (c3087); `inbox-triage new` NONE UNTRIAGED of 78; `bin/revenue` $0 booked, 27 public Actors, 54 users, 1485 runs30d, `ext_bad30d` 31 (the documented decaying `trademark-search-scraper` baseline, no new Actor name, not re-opened), 0 bookmarks, 0 reviews -- no buyer signal, no owner email owed; `bin/apify-spend` $1.6479/$85 (proj $14.65); services/site 200. **`NEW (c2478)`'s 2026-11-15 deadline is 3 days out and its remaining work is explicitly "do this AFTER 2026-11-15" -- re-read, correctly not actionable yet.** **1 check was due and ran: `check-schema-claims` (last c2608, 480-cycle gap) -- CLEAN, 26 schemas, 30 fresh / 5 AGING / 0 STALE, 27 undated (inventory), 8 HISTORY correctly suppressed; recorded via `checks-due --ran`, next due c3568.** The 5 AGING claims are filed below as `NEW c3088`. **Work: RULE 6b SECOND pass on `app-store-reviews-scraper`** (c3087's first-named candidate by sweep age; first pass c3059, 28 TERMS). Health-gated first (`--only`, ok=True, 10 items, 0 fail_rows). Curated 25 new n-grams from the 4 live `meta.json` fields, skipping all 28 tracked terms and both prior screened-out lists (c3059's 6, cycle 554's); batch-priced all 25 in ONE `store-price` call; individually re-verified EVERY one with `store-rank --why`. **All 25 ranked in the top 60 and all 25 matched the batch tool byte-for-byte on rank AND on the full (words, exact, prox, attr) tuple -- 25/25, on the very Actor that produced c3059's worst-ever 6/24 disagreement.** **15 keepers shipped (28 -> 43 TERMS)**, best: `any country` (6632 nbHits, p22 -- highest-volume term this Actor has ever tracked), `store review monitoring` (4593, p5), `per star ratings` (4685, p8), `watch mode monitoring` (4059, p2), `app store review monitoring` (1361, p5). **10 screened out as NOISE, not as unranked -- all 10 ARE live in the top 60**, applying c3059's own `feed rank` rule (output-field/sort-enum names and 6-8 word prose fragments nobody types); their measured ranks are recorded in `bin/store-rank` so no future pass re-shops them. None of the 15 is in the p50-60 FLAPPING band. `ast.parse` clean + `SourceFileLoader` re-import (43 terms, 43 unique, no duplicate); full 43-term probe re-run post-edit, RC=0, 43 rows, every new term re-measured at the rank `--why` gave it. $0 spent, doc-only -- no `meta.json` edit, no build, no publish, no reindex. **Blockers: none. Owner email: none owed.** **Next cycle: c3089 is Regular/GROWTH (3089 % 3 == 2).** Remaining second-pass candidates by sweep age, oldest first: `trademark-search-scraper` (c3061), `clinicaltrials-mcp-server` (c3067), `court-records-scraper` (c3070), `fda-recall-scraper` (c3074), `eu-ted-tenders-scraper` (c3076), `apple-podcasts-scraper` (c3077 -- read its standing audit watch, now in `notes/STANDING.md`, first). c3090 is the next QUALITY slot: resume `NEW c3084`'s split per c3087's `PROGRESS` note, and re-check `check-doc-size` (this block grows both docs). **Note for the next QUALITY slot: c3087 left a `PROGRESS` note on `NEW c3084` but did NOT write its own `CLOSED c3087` cycle block in this file** -- `check-status-blocks-kept`/`check-status-continuity` only guard `state/STATUS.md` (both CLEAN this cycle, 26 blocks, none missing), so queue.md's block series has a one-cycle hole that is invisible to tooling. Not worth back-filling; worth knowing before anyone counts blocks here.

- [ ] **NEW c3088 (LOW/scheduled, NOT a defect -- do this on a BUILD slot, not a doc slot).** `check-schema-claims` ran CLEAN this cycle (0 STALE) but reported **5 AGING measurement claims** in buyer-facing `.actor/input_schema.json` prose, which the checker defines as "go re-measure", never "this is wrong": (a) `remote-jobs-scraper.properties.resultOrder.description`, measured 2026-10-18, 25d old, **crosses the 30d STALE line ~2026-11-17**; (b-e) four `steam-reviews-scraper` claims -- `purchaseType`, `includeOffTopic`, `sortBy`, `dayRange` -- all anchored to the same `2026-10-23 source change`, 20d old, STALE ~2026-11-22. **Why this is not a doc edit:** each claim is a count/behaviour of a LIVE external source, so honouring it means an actual Actor run to re-measure plus an `apify push` to update the prose -- a build-slot task with a small real cost, which is exactly why no doc-only cycle should touch it. **Do NOT "fix" these by rewriting the prose to dodge the checker** -- c2609 and c2611 both burned an `apify push` doing that and the checker's HISTORY-clause rule (c2612) exists specifically to make keeping the old number next to a fresh one the cheap, honest option: re-measure, then write `first measured <old> on <old-date>, re-verified live <new-date> at <new>`. The 4 steam-reviews claims share one anchor, so one re-measure run plus one push settles all four. Checker next due c3568, so nothing will re-flag these automatically before then -- this item is the only reminder.

- [ ] **CLOSED c3086 -- Regular/GROWTH slot (3086 % 3 == 2). Preflight all clean:** tree matched HEAD `689f4c2c` (c3085); `inbox-triage new` NONE UNTRIAGED of 78; `bin/revenue` $0 booked, 27 public Actors, 54 users, 1476 runs30d, `ext_bad30d` 31 (still the documented decaying `trademark-search-scraper` baseline, no new Actor name, not re-opened), 0 bookmarks, 0 reviews -- no buyer signal, no owner email owed; `bin/apify-spend` $1.5974/$85 (11.1% elapsed, proj $14.37); services `fetchsmith-web`/`fetchsmith-mail`/`caddy` active, site 200 on `/` and `/tools`. **1 check was due: `check-source-endpoints`, ran it (50 unique hosts probed, 0 baselines set, 0 DEVIATION, 3 EXEMPT unchanged -- CLEAN), recorded via `checks-due --ran` (next due c3110).** `check-doc-size`: `tasks/queue.md` TRIM DUE at 170.2KB/1407ln (~6c headroom) -- left for c3087 (next QUALITY slot) per the c3024 trap (a GROWTH slot should not spend budget on trim durability checks); `state/STATUS.md` TRIM SOON at 97.9KB/288ln (~23c headroom); `notes/LEARNINGS.md` OK.

**Work: RULE 6b SECOND PASS on `federal-register-scraper`** -- the c3085 handoff's first-named candidate, the fleet's oldest-swept Actor with no second pass yet (first pass c3058, 22 TERMS). Confirmed healthy via `bin/actor-health` first (ok=True, 10 items, 0 fail_rows). Read the 4 live `meta.json` fields verbatim, curated 12 NEW n-grams not already in the 22 tracked terms or the 6 already screened out by c3058, batch-priced all 12 in one `store-price` call, then individually re-verified **every** candidate via `store-rank --why` per the standing c3059 correction. **12/12 batch-vs-`--why` agreement** (tied with c3068's 24/24 for best rate recorded, on a smaller sample). **8 true keepers shipped (22 -> 30 TERMS)**, applying the SAME >=49-nbHits keep bar c3058 itself established: `regulatory monitoring api` (1122 nbHits, p1 -- highest-nbHits keeper on this Actor to date), `proposed rules` (335, p6), `us federal register` (317, p50 -- **FLAPPING FLAG per c3031**, p50-60 horizon), `us federal register api` (198, p5), `federal register regulatory monitoring` (187, p1), `federal register rulemaking api` (86, p1), `rulemaking api` (97, p2), `scrape the us federal register` (69, p4). **4 screened out, all below the 49-nbHits bar**: `comment close deadline` (27, p1), `rin and cfr refs` (23, p1 -- a direct superset of c3058's own screened-out `rin and cfr` at 24 hits, confirming the trivial call generalizes), `filings not yet published` (4, p1), `public inspection filings not yet published` (1, p1). Full numbers durably homed in `bin/store-rank`'s own cycle-3086 provenance comment. $0 spent, no `meta.json` edit, no build/publish/reindex -- doc-only (`bin/store-rank` append). Edit verified: `ast.parse` clean; full 30-term `store-rank federal-register-scraper` probe re-run post-edit, all 8 new terms matched the written (nbHits, rank) exactly, the 22 pre-existing terms byte-identical (append-only, no existing string touched).

**Blockers: none. Owner email: none owed.** Services/site re-verified 200 post-work. **Next cycle: c3087 is the next QUALITY slot (3087 % 3 == 0)** -- `tasks/queue.md` is TRIM DUE (~6c headroom, re-check `check-doc-size` and trim per the standing cadence) and `state/STATUS.md` is TRIM SOON (~23c headroom, not yet due but growing -- the c3084 handoff flagged this). No fleet checks due until c3110 (`check-source-endpoints`). Remaining RULE 6b second-pass candidates by sweep age, oldest first: `app-store-reviews-scraper` (c3059), `trademark-search-scraper` (c3061), `clinicaltrials-mcp-server` (c3067), `court-records-scraper` (c3070), `fda-recall-scraper` (c3074), `eu-ted-tenders-scraper` (c3076), `apple-podcasts-scraper` (c3077, read its standing audit watch `NEW watch c2816` first).

- [ ] **CLOSED c3085 -- Regular/GROWTH slot (3085 % 3 == 1). Preflight all clean:** tree matched HEAD `0c9b76ef` (c3084); `inbox-triage new` NONE UNTRIAGED of 78; `bin/revenue` $0 booked, 27 public Actors, 54 users (up from 52), 1476 runs30d, `ext_bad30d` 31 (still the documented decaying `trademark-search-scraper` baseline, no new Actor name, not re-opened), 0 bookmarks, 0 reviews -- no buyer signal, no owner email owed; `bin/apify-spend` $1.5459/$85 (11.0% elapsed, proj $14.0); services `fetchsmith-web`/`fetchsmith-mail`/`caddy` active, site 200 on `/` and `/tools`; `checks-due --all` NONE DUE (soonest `check-source-endpoints` in 1c, c3086). **Work: picked a fresh lever per `NEW c3046` option (d)'s handoff (no named RULE 6b candidate remained after `METHOD c3084`) -- a RULE 6b THIRD sweep on `grants-gov-scraper`, the fleet's oldest-swept Actor (first 6b pass c3056) with no second pass yet, since the named 3-Actor second-pass round (c3079/c3082/c3083) only covered the 3 lowest first-pass payouts, not every Actor.** Confirmed healthy via `bin/actor-health` first (ok=True, 0 fail_rows). Read the 4 live `meta.json` fields verbatim, curated 18 NEW contiguous n-grams not already in the 33 tracked terms or the 9 previously screened-out ones, batch-priced all 18 in one `store-price` call, then individually re-verified EVERY candidate via `store-rank --why` per the standing c3059 correction: 14/15 ranked candidates matched the batch tool byte-for-byte (1 false positive). **14 true keepers shipped (33 -> 47 TERMS)**: `search and enrich` (18167 nbHits, p20 -- highest-volume keeper this Actor has had), `enriched result` (6343, p8), `thin rows` (5364, p1), `enrich the official` (1482, p1), `official grants.gov` (137, p37), `ceiling floor` (192, p32), `official grants.gov api` (125, p23), `award ceiling floor` (115, p31), `text and full synopsis` (114, p1), `grants data api exports` (178, p1), `eligibility award` (251, p1), `grant opportunities api nofos` (17, p1), `nonprofit grants.gov database` (42, p1), `eligibility text and full synopsis` (31, p1). Screened out `data api exports` (12428 hits, batch false-positive, not actually in top 60) and declined 3 unranked-already candidates (`no start fee`, `api exports`, `federal grant` -- would need an edit, out of scope for a $0 pass). None in the p50-60 FLAPPING band. Full numbers in `bin/store-rank`'s own cycle-3085 provenance comment. **Confirms a second 6b pass is viable even on an Actor whose first pass was itself already labeled a second pass** -- reusable finding for future GROWTH slots: pick the oldest-swept Actor with no dedicated second 6b pass yet, not just the 3 named lowest-first-pass-payout ones. `ast.parse` clean; full 47-term `store-rank grants-gov-scraper` probe re-run post-edit, all 33 pre-existing terms byte-identical (append-only). $0 spent, no `meta.json` edit, no build/publish/reindex -- doc-only (`bin/store-rank` append). **Blockers: none. Owner email: none owed.** Services/site re-verified 200 post-work. **Next cycle: c3086 is also Regular/GROWTH (3086 % 3 == 2; c3087 is the next QUALITY slot -- `check-source-endpoints` is due c3086).** Next second-pass candidates by sweep age (oldest first-pass without a second pass): `federal-register-scraper` (c3058), `app-store-reviews-scraper` (c3059), `trademark-search-scraper` (c3061), `clinicaltrials-mcp-server` (c3067), `court-records-scraper` (c3070), `fda-recall-scraper` (c3074), `eu-ted-tenders-scraper` (c3076), `apple-podcasts-scraper` (c3077, but read its standing audit watch `NEW watch c2816` first). `tasks/queue.md` is 170.6KB, approaching `TRIM DUE` again -- re-check `check-doc-size` at the next QUALITY slot (c3087).**

- [ ] **CLOSED c3084 -- QUALITY slot (3084 % 3 == 0). Preflight all clean:** tree clean at HEAD `959bab38` (c3083); `inbox-triage new` NONE UNTRIAGED of 78; `bin/revenue` $0 booked, 27 public Actors, 52 users, 1476 runs30d, `ext_bad30d` 31 (still the documented decaying `trademark-search-scraper` baseline, no new Actor name, not re-opened), 0 bookmarks, 0 reviews -- no buyer signal, no owner email owed; `bin/apify-spend` $1.5455/$85 (11.0% elapsed, projection $14.08); services `fetchsmith-web`/`fetchsmith-mail`/`caddy` active, site 200 on `/` and `/tools`; `checks-due --all` NONE DUE (soonest `check-source-endpoints` in 2c, c3086). **Work: the due queue.md doc-trim, which c3081/c3082/c3083 each named for this slot -- ran BOTH levers (`bin/_trim3084q.py`, self-verifying one-shot, dry-run before writing).** (1) **Newest-5-floor rotation, and the floor had silently drifted: TEN live cycle blocks, double the floor**, because the last three QUALITY slots rotated one block each while GROWTH slots add one per cycle. Archived the oldest five (c3077/c3076/c3075/c3074/c3073) at once -> 5 live, 6 with this block. (2) **Rule 4 said that was not enough** (~14.5KB off a 181KB file lands ~167KB, still WARN), so compressed the largest line in the file in the same cycle: **`NEW c3056` (11,103B) -> `METHOD c3084` (~4KB)**. Its 12-Actor RULE 6b backlog has been FULLY RESOLVED since c3077 and all three follow-on second passes are done (c3079/c3082/c3083), yet the live text still read "now 3 named Actors left" and "Remaining 1: apple-podcasts-scraper" -- genuinely superseded. Kept every method step, the c3059 verify-every-candidate correction, the measured batch-vs-`--why` range (25/25 best, 3/25 worst), the c3073/c3074 generic-word blind spot, the c3068 measured-and-declined pattern and every caveat; archived the ~7KB per-Actor roll-call verbatim. **The archive was pre-authorized by the `- [x] CLOSED c3077` record itself, conditional on a durable-home check -- condition VERIFIED before writing a byte:** all 12 swept Actors' terms are live in `bin/store-rank`'s `TERMS` (grants-gov 33 ... apple-podcasts 38) and all 15 sweep cycles have their own `cycle NNNN` provenance comments there, so the roll-call was narrative, not the home. That record's own load-bearing instruction (do not hunt another unswept Actor; pick a fresh lever per `NEW c3046`) was folded into the rewrite before the record was archived. **Result: 185,602B/1406ln -> 164,639B/1393ln, 20,963B saved, headroom 4c -> 7c**; lossless (multiset identity over live+archive), 6 rule-1 hazard hits all inside archived cycle blocks, structural asserts green (5 CLOSED blocks live, 94 -> 88 items, do-not-archive STANDING RULES section intact, no stale backlog claim live). $0 spent, no `meta.json`, no build, no publish, no reindex -- doc-only. **It is STILL `TRIM DUE` at 160.8KB afterwards, and that is the real finding -- see `NEW c3084` below.**

- [ ] **CLOSED c3083 -- Regular/GROWTH slot (3083 % 3 == 2). Preflight all clean:** tree matched HEAD `e5463e2a` (c3082); `inbox-triage new` NONE UNTRIAGED of 78; `bin/revenue` transient `JSONDecodeError` on first call (one `acts/<id>` fetch returned a non-JSON body), succeeded clean on 2 immediate retries with identical numbers both times -- $0 booked, 27 public Actors, 52 users, 1476 runs30d, `ext_bad30d` 31 (still the documented decaying baseline), 0 bookmarks, 0 reviews -- no buyer signal, no owner email owed; `bin/apify-spend` $1.4553/$85 (10.9% elapsed, proj $13.34); services `fetchsmith-web`/`fetchsmith-mail`/`caddy` active, site 200 on `/` and `/tools`; `checks-due --all` NONE DUE (soonest `check-source-endpoints` in 3c, c3086). **Also checked the 3 owner-thread mail items flagged by `inbox list` in case they were new/unactioned: all three (`f11632f7` Apify-token replacement, `9be9604c` Apify's security-incident forward, `01852eaa` the Nov-15 Store-API ranking-change forward) are already fully resolved/triaged by prior cycles** -- `STATUS.md` line 211 shows the new token was installed and verified (`GET /v2/users/me` -> 200) the same cycle the owner replied, and I independently re-confirmed it live again this cycle (200). No action needed, no owner email owed. **Work: RULE 6b SECOND PASS on `ats-jobs-scraper`** (`CLOSED c3082` handoff's named candidate -- the last of the three original-backlog Actors with an un-taken second pass; first pass was c3073's 9 keepers, 17 -> 26 TERMS). Confirmed healthy via `bin/actor-health` first (ok=True, 10 items, 0 fail_rows). Curated 25 NEW n-grams from the same 4 live `meta.json` fields (title/description/seoTitle/seoDescription), skipping the 26 already-tracked and 15 already-screened-out terms from c3073; batch-priced all 25 in one `store-price` call, then individually re-verified EVERY candidate via `store-rank --why` per the standing c3059 correction. **13 true keepers shipped (26 -> 39 TERMS)**: `hiring page` (6203, p8), `job openings` (3132, p9), `employment data` (6406, p55 -- **FLAPPING**, p50-60 band per c3031), `recruiting data` (5001, p11), `recruitment data` (3604, p29), `roles api` (7273, p10), `10 ats platforms one schema` (15, p1), `department team city` (506, p1), `team city region` (1460, p1), `city region country salary` (884, p1), `tracking system api` (2092, p1), `ats and applicant tracking system` (876, p1), `jobs from 10 platforms` (60, p1). Screened out 12, all confirmed absent from the top 60 by `--why` despite batch predicting p1-p35 for most: `hiring data`, `data feed`, `open roles`, `hiring trends`, `trends data`, `jobs api`, `ats jobs api`, `ats jobs data`, `ats jobs feed`, `live ats jobs`, `salary parsed data`, `pay range`. Full numbers durably homed in `bin/store-rank`'s own cycle-3083 provenance comment. **DATA POINT: batch-vs-`--why` agreement was 9/25**, mid-spectrum and close to this Actor's own first-pass rate (c3073: 6/24) -- another confirmation the c3059 rule (verify every candidate regardless of nbHits, agreement is Actor-dependent) must stay in force. **Confirms a second 6b pass on the MOST heavily pre-shopped Actor in the fleet (c1820's 10-phrase SEO rewrite, c2023's description-field cap) is still not exhausted** -- bare 2-word stems (`hiring page`, `job openings`, `recruiting data`, `recruitment data`, `roles api`) and 3-4-word geographic/role combinations were real, previously-missed wins. Edit verified: `ast.parse` clean; full 39-term `store-rank ats-jobs-scraper` probe re-run post-edit, all terms resolve matching the written (nbHits, rank) exactly (minor single-digit nbHits drift on 2 terms is ordinary live competitor churn between measurement and re-probe, same as every prior cycle's experience -- ranks unaffected), the 26 pre-existing terms byte-identical (append-only, no existing string touched). **This closes out the three-Actor RULE-6b second-pass round that began at c3079** (`us-federal-awards-scraper` 19 keepers, `remote-jobs-scraper` 14 keepers, `ats-jobs-scraper` 13 keepers) -- no more named second-pass candidates remain on file; the next GROWTH slot should pick a fresh lever per `NEW c3046`'s option list (option (d): re-examine eviction candidates on RULE-6-closed Actors) or scan the fleet for an Actor whose first pass is thin/old enough to be worth a third look. $0 spent, no `meta.json` edit, no build/publish/reindex -- doc-only (`bin/store-rank`, `tasks/queue.md`, `state/STATUS.md`).

**Blockers: none. Owner email: none owed** ($0 booked, no buyer signal, 0/78 untriaged mail, all 3 owner-thread items already resolved). Services/site re-verified 200 post-work. **Next cycle: c3084 is the next QUALITY slot (3084 % 3 == 0).** `tasks/queue.md` was TRIM DUE as of c3082 and has grown further this cycle -- c3084 should run `bin/check-doc-size` and trim per the standing cadence; the ~140-file `bin/_trimNNNN*.py` clutter batch-delete (flagged since c3075) remains unclaimed if a different QUALITY lever is wanted. No fleet checks due until c3086 (`check-source-endpoints`).

- [ ] **CLOSED c3082 -- Regular/GROWTH slot (3082 % 3 == 1). Preflight all clean:** tree matched HEAD (`29102593`, c3081); `inbox-triage new` NONE UNTRIAGED of 78; `bin/revenue` $0 booked, 27 public Actors, 52 users, 1476 runs30d, `ext_bad30d` 31 (still the documented decaying baseline), 0 bookmarks, 0 reviews -- no buyer signal, no owner email owed; `bin/apify-spend` $1.4062/$85 (10.8% elapsed, proj $12.98); services `fetchsmith-web`/`fetchsmith-mail`/`caddy` active, site 200 on `/` and `/tools`; `checks-due --all` NONE DUE (soonest `check-source-endpoints` in 4c, c3086). **Work: RULE 6b SECOND PASS on `remote-jobs-scraper`** (`NEW c3080`/`CLOSED c3081` handoff's named candidate, lowest first-pass payout at 6 keepers from c3068). Confirmed healthy via `bin/actor-health` first (ok=True, 10 items, 0 fail_rows). Curated 25 NEW n-grams from the same 4 live `meta.json` fields (title/description/seoTitle/seoDescription), skipping the 21 already-tracked and 18 already-screened-out terms from c3068's first pass; batch-priced all 25 in one `store-price` call, then individually re-verified EVERY candidate via `store-rank --why` per the c3059 correction. **14 true keepers shipped (21 -> 35 TERMS)**: `seven public boards` (630, p2), `billed twice` (13, p7), `never billed twice` (11, p6), `job never billed twice` (2, p1), `filter by keyword company` (6302, p21), `keyword company location` (8210, p37), `remote hiring` (5524, p24), `recruitment data` (3603, p34), `employment data` (6398, p58 -- **FLAPPING**, p50-60 band per c3031), `job monitoring api alerts` (1249, p1), `monitoring api alerts` (6319, p6), `aggregator api` (14239, p34 -- the highest-nbHits keeper on this Actor to date), `job aggregator api on seven boards` (256, p1), `postings dataset` (10191, p5). Full numbers and the 11 screened-out false positives are in `bin/store-rank`'s own cycle-3082 provenance comment (the durable home). **DATA POINT: batch-vs-`--why` agreement was only 3/25 exact matches, the worst rate recorded on this backlog yet** (prior worst c3073's 6/24) -- reconfirms the c3059 CORRECTED rule (verify every candidate regardless of nbHits) must stay in force. **Confirms a second 6b pass on a Actor whose FIRST pass was thin (6 keepers) is also not exhausted** -- different compound phrasing (`seven public boards` vs the tracked `seven job boards`, `job never billed twice` vs the screened `de-duplicated`) found real wins c3068 missed. $0 spent, no `meta.json` edit, no build/publish/reindex -- doc-only (`bin/store-rank` append). `ast.parse` clean (via explicit `SourceFileLoader`, the extensionless-file import gotcha); full 35-term `store-rank remote-jobs-scraper` probe re-run post-edit, all terms resolve matching the written (nbHits, rank) exactly, the 21 pre-existing terms byte-identical (append-only, no existing string touched). **Blockers: none. Owner email: none owed.** Services/site re-verified 200 post-work. **Next cycle: c3083 is also Regular/GROWTH (3083 % 3 == 2; c3084 is the next QUALITY slot).** Remaining second-pass candidate: `ats-jobs-scraper` (9 keepers first pass, c3073) -- or pick a fresh lever per `NEW c3046`'s option list (option (d): re-examine eviction candidates on RULE-6-closed Actors). `tasks/queue.md` is TRIM DUE again (confirm via `check-doc-size` at the next QUALITY slot, c3084); the ~140-file `bin/_trimNNNN*.py` clutter batch-delete (flagged since c3075) remains unclaimed.

- [x] **DECIDED c3081 -- DEFER, no `meta.json` edit. Do not re-open without one of the two triggers named below.** Read `meta.json`, the `watchLabel` README row, and the full FAQ/Pricing sections before deciding (`actors/trademark-search-scraper/README.md` lines 20, 78-82, 106-111, 131, 135, 139). Four reasons the reprice loses on balance, not one: (1) **the live README already states the zero-charge behaviour as an unconditional per-run promise**, not just a first-run baseline -- line 20 ("every later run on the same label + search returns and charges only marks not already delivered") and line 131 ("watch-mode baseline runs return and charge nothing") -- a new `watch-check` fee charged on a quiet run contradicts live buyer-facing text on our ONLY page-1 listing, not a doc nobody reads. (2) **This is already our stated differentiator against the exact two rivals cited as the reason to reprice**: README line 139 already discloses `nexgendata/uspto-trademark-search` and `nexgendata/euipo-esearch-trademarks` charge $0.05/watch-check (25-50x ours) and line 135 says plainly "Our `watchLabel` mode charges only the $0.002 row rate, and only on marks you have not already been given" -- the gap `NEW c3080` found is not an unmarketed gap, it is an already-marketed asymmetry; repricing would delete the very thing being advertised. (3) **Zero signal there is any revenue to capture**: 0 bookmarks, 0 reviews, $0 booked on this Actor -- we do not know a single real buyer runs `watchLabel` at all, let alone on a schedule frequent enough for the $0 compute exposure to matter. (4) **The exposure being guarded against is small by construction**: a no-change watch run is one HTTP-only TMview page fetch plus a KVS baseline read/write, not a browser session -- sub-cent ACTOR_COMPUTE_UNITS cost (see `bin/apify-spend`'s per-service breakdown), nothing like the data-transfer or proxy cost a result-heavy run carries. **Re-open only if either:** (a) real buyer signal appears on this Actor specifically (a bookmark, a review, or a booked-revenue event tied to it), making the upside non-speculative; or (b) a future `bin/usage-trend`-style check shows sustained high-volume scheduled `watchLabel` runs at zero rows, showing the compute exposure is no longer trivial. Neither test re-run (`check-price-superiority`, `check-unit-matched-price`) was needed since no price changed. $0 spent, no build, no push. Full prior research (rival prices, the tension, the suggested shape if ever shipped) stays below, superseded but kept for context on re-open.
  **Why this Actor and not another:** c3080's `store-anon-rank` run put it at **#8 of 249** (5 users, runs30d 636) -- our only top-10 rank on any buyer query, vs #29-#501 for all 26 others. It is the one listing that actually gets buyer impressions, so it is the only one where conversion/monetization work can pay (see LEARNINGS c3080).
  **The gap (verified, not assumed):** we ALREADY ship watch mode -- `watchLabel` / `watchChanges` / `webhookUrl`, documented in `actors/trademark-search-scraper/README.md` lines 20-22, with `_watchChangeType`/`_watchPrevious` change fields. But `meta.json` prices exactly ONE event: `result` @ $0.002 ("Result item"). So a scheduled watch run that finds nothing new returns 0 rows and bills **$0** while still costing us compute + dataset/KVS writes. Rivals price exactly this event: **#1 `nexgendata/uspto-trademark-search` `watch-check` @ $0.05**, **#9 `nexgendata/euipo-esearch-trademarks` `watch-check` @ $0.05**, #4 `trev0n/tmview-scraper` `trademark-details` @ $0.002 (plus a $0.005 `apify-actor-start` on #1/#3/#4/#7/#9, which we do not charge at all).
  **The tension that makes this a DECIDE, not a do:** (a) our published README promises "the first run under a label seeds a baseline (0 rows returned, **0 charged**)" -- adding a charge silently contradicts live buyer-facing docs and must be a doc change too; (b) "From $0.002/result, no start fee" in `meta.json`'s description is our stated differentiator and we are **the cheapest in the whole top 9** (#1/#9 charge $0.05/record, #3 $0.007+$0.005 start) -- check `check-price-superiority` / `check-unit-matched-price` before touching it; (c) 0 bookmarks / 0 reviews / $0 booked means there may be no watch-mode users to monetize yet, so the upside is speculative while the positioning loss is real.
  **Suggested shape if it goes ahead:** a small `watch-check` event (well under the rivals' $0.05 -- we undercut on purpose) charged ONLY on a run with `watchLabel` set that returns 0 new rows, leaving plain searches at $0.002/result with no start fee and the "no start fee" claim intact. Update README lines 20-22 and the FAQ in the same commit. Re-run `actor-health` + the default-input gate after `apify push`.

- [ ] **NEW c3084 (HIGH, structural -- the doc-trim cadence can no longer clear `tasks/queue.md`, and no amount of running it harder will fix that. Take this on a QUALITY slot INSTEAD of a routine trim.)** c3084 ran both available levers in one slot (newest-5 rotation of five blocks at once + an 11KB compression of the largest line) and still landed at **160.8KB / `TRIM DUE` with ~7c headroom**. The arithmetic is now unarguable: the checker wants post-trim size under ~70KB to clear its own 24c look interval, and **the live content floor is ~160KB**, so the gap is not a trim backlog, it is the file's composition. **Measured c3084, this is the lever:** of 88 live items / 160.8KB, only **4 items (7.2KB) are actionable `NEW cNNNN` tasks**. The other 84 are reference material filed in a task queue -- 22 `NEW follow-up` (30.0KB), 12 `NEW note` (9.6KB), 8 `NEW standing` (14.4KB), 5 `NEW watch` (5.5KB), 2 `NEW tripwire` (2.4KB), plus the CLOSED/COMPRESSED/MERGED/RETIRED/SHIPPED/DECIDED/RESOLVED closed records (~58KB). **Proposed split, which attacks the growth RATE the way STANDING RULE 6 intended rather than re-cutting the stock:** move the standing rules / tripwires / watches / method records to a `notes/STANDING.md` (read on demand, not every cycle) and leave `queue.md` as an actual prioritized queue of open tasks plus the newest-5 cycle blocks. That plausibly takes queue.md under 70KB in one slot and keeps it there, because the recurring per-cycle growth is cycle blocks (rotated) and new follow-ups (which would land in notes). **Do NOT start this without budgeting a full QUALITY slot** -- it is a hazard-grep-heavy move (every cross-item `see NEW cNNNN` pointer has to be re-aimed at the new file, and STANDING RULE 1 says grep first, then cut), and the `STANDING RULES` section in the doc-trim item plus the guarded `c2478` (live 2026-11-15 deadline) and `c2336` (live triage tripwire) must stay reachable. **Interim rule for any QUALITY slot that does a routine trim before this lands: COUNT the live cycle blocks rather than assuming the floor held** -- c3084 found ten, double the floor, because rotating one block per QUALITY slot does not keep up with one block added per cycle, and the drift is invisible unless counted.

**PROGRESS c3087: first slice of the split shipped.** Created `notes/STANDING.md` and moved the 7 lowest-risk items -- the 5 `NEW watch` + 2 `NEW tripwire` items (~7.9KB) -- verbatim, chosen because a hazard grep over `bin actors site notes state tasks` for each item's cycle-label found zero live functional cross-references (only narrative mentions inside other cycle blocks, which describe history and don't break). Verified lossless by multiset diff (every non-blank line from the pre-edit file is findable in queue.md + STANDING.md + queue_archive.md). Also ran the routine newest-5-floor rotation in the same slot (8 live blocks -> 5, archived `CLOSED c3080`/`c3079`/`c3078` to `queue_archive.md` under `## Archived by cycle 3087`). **Result: 166.2KB -> 155.0KB, still TRIM DUE (6c -> 8c headroom) -- as this item predicted, neither lever alone clears it.** **NOT yet moved** (left for a future QUALITY slot, in increasing order of risk/size): the 8 `NEW STANDING RULE/NOTE/PREFLIGHT/WATCH` items (~14.4KB, excluding the guarded `c2336` triage tripwire which must stay reachable per this item's own instruction), then the `METHOD c3084` record (~4KB) and the `STANDING RULES` section inside the doc-trim-cadence item itself -- those carry more cross-references and deserve their own hazard grep pass before cutting. `notes/STANDING.md` is NOT read every cycle; it's referenced from its own header for when a `competitor_audit`/RULE-6b sweep touches an Actor named in one of its items.

- [ ] **METHOD c3084 (was `NEW c3056`, the 12-Actor RULE 6b first-pass backlog -- that backlog is FULLY RESOLVED and this item is now the METHOD + LESSONS record only; the 11KB per-Actor roll-call it used to carry is archived verbatim under `## Archived by cycle 3084` in `queue_archive.md`).** **There is NO named candidate left: all 12 first passes closed by c3077** (grants-gov c3056, federal-register c3058, app-store-reviews c3059, trademark-search c3061, clinicaltrials-mcp c3067, remote-jobs c3068, court-records c3070, us-federal-awards c3071, ats-jobs c3073, fda-recall c3074, eu-ted-tenders c3076, apple-podcasts c3077; `scholarship-scraper` SKIPPED -- `bin/actor-health` shows it retired/429-blocked since 2026-09-20, **do not re-pick until the block clears**), **and the three follow-on SECOND passes are done too** (us-federal-awards c3079 19 keepers, remote-jobs c3082 14, ats-jobs c3083 13). **Next GROWTH slot: do NOT hunt for another unswept Actor here -- pick a fresh lever from `NEW c3046`'s option list** (option (d): re-examine eviction candidates on RULE-6-closed Actors, or find a genuinely new lever). **Durable home for every number this backlog produced is `bin/store-rank` itself** -- each sweep wrote a dated `cycle NNNN` provenance comment carrying its keepers with (nbHits, rank, attr) and its screened-out list, and the terms are live in that file's `TERMS` dict; verified c3084 before archiving the narrative. **THE METHOD (~8-10 tool calls, ~15-20 min, $0, no build/publish/reindex -- `bin/store-rank` is a local tracking script, not a live listing):** (1) check `bin/actor-health` FIRST for retired/paused/blocked status (the scholarship-scraper lesson) and read the live `actors/<slug>/meta.json`, taking ONLY title/description/seoTitle/seoDescription -- never README, cycle-1468 paraphrase hazard; (2) curate ~20-25 contiguous and near-contiguous n-grams from that vocabulary that a buyer would actually type, skipping anything already in TERMS and anything a prior pass already screened out; (3) batch-price all of them in ONE `bin/store-price <slug> "q1" "q2" ...` call (c3044: the 4th element of `liveBucket` IS the anchoring attr, so no per-term `--why` is needed for the RULE 6 anchor-map step); (4) note which look like keepers at p60-or-better with non-trivial nbHits, but do NOT stop there; **(5) STANDING CORRECTION c3059, reconfirmed by every sweep since -- re-verify EVERY candidate with `store-rank --why "<q>" <slug>`, including ones the batch tool ranked deep or screened out, NOT just the apparent keepers, and NOT only the high-nbHits ones;** (6) keep anything `--why` confirms in the top 60 with non-trivial nbHits, flag p50-60 as FLAPPING per c3031; (7) append to TERMS with a dated provenance comment carrying the measured (nbHits, rank) per term AND the screened-out list with their ranks/reasons -- the screened-out list is what stops the next cycle re-shopping the same dead phrases; (8) `ast.parse` + module re-import (needs an explicit `SourceFileLoader`, c3082: `bin/store-rank` has no `.py` extension so plain `spec_from_file_location` fails to infer a loader), then re-run the full `bin/store-rank <slug>` probe -- note an append-only edit CANNOT regress an existing term's live rank, so phrase it as "no existing term's string was touched", not as a re-measured byte-identical claim, unless you actually captured a pre-edit baseline. **WHY STEP 5 IS NON-NEGOTIABLE (the single most expensive lesson here): batch-vs-`--why` agreement is ACTOR-dependent, not nbHits-dependent, and cannot be known before you spend the calls.** Measured range across the sweep: best 25/25 byte-exact (c3076 `eu-ted-tenders`, including every high-nbHits query) and 24/24 (c3068 `remote-jobs`); worst 3/25 (c3082 `remote-jobs` second pass) and 4/22 (c3070 `court-records`, 3 outright false positives where batch predicted p1-p3 and the real rank was outside the top 60); mid 6/24, 15/23, 19/25. c3067 found a false positive at only **187 nbHits**, so c3059's original "~1000 nbHits" framing is NOT a safe bound -- there is no threshold below which you may skip the call. **KNOWN BLIND SPOT (c3073/c3074), also Actor-dependent:** single bare generic words that are already present in our own live description (ATS brand names greenhouse/ashby/lever/workable/workday; `openfda`) get batch-predicted p1-p2 yet `--why` finds them absent from the top 60 entirely, because they are common words with thousands of unrelated competitors -- but c3076 saw batch screen generic phrases correctly, so **do NOT use this pattern as a pre-screen to skip `--why` calls**, only as a prior on what will turn out to be a false positive. **REUSABLE PATTERN (c3068): grep the Actor's own older provenance comments for phrases a past cycle MEASURED and then DECLINED to act on** -- `remote job postings` (6689 hits) had been measured at p27 by c1820, never added to TERMS, and sat untracked ~1250 cycles; a declined EDIT is not a reason to leave a live rank untracked. **A SECOND pass is NOT exhausted after the first** (c3079/c3082/c3083 shipped 19/14/13 keepers on already-swept Actors), and **a thin payout is pre-shopping, not method failure** -- expect low single digits on Actors the c1816-c1852 SEO sweep already worked. **CAVEAT on any future "unswept Actor" scan:** it keys on the literal string `RULE 6b`, which only entered the vocabulary around c3002, so an Actor can read "unswept" while an older cycle shopped some of its phrases under a different name -- approach any such candidate as "re-shop with the mature method", not virgin ground. **`apple-podcasts-scraper` carries a standing audit watch of its own (`NEW watch c2816`, due ~c3152) -- read that item before editing anything but `TERMS` on it.**

- [x] **RESOLVED same-cycle c3070 -- transient read glitch, not a real regression.** The post-edit `bin/store-rank court-records-scraper` probe briefly showed the pre-existing tracked term `case search api` reading `rank=>1000 storePosition=None`. Re-ran `store-rank --why "case search api" court-records-scraper` immediately after: nbHits=30875, `US: p7` attr=5 -- normal, matches the term's usual top-60 rank. The plain-probe command's single HTTP call must have hit a transient blip (rate limit or index read lag); `--why`'s independent call came back clean seconds later. No action needed, no drift confirmed.

- [ ] **NEW c3046 (HIGH -- the RULE 6 anchor-map sweep that has been the default GROWTH-slot pick since c3004 is now DONE; every future GROWTH slot needs a different default, not "find the next unmapped Actor"). CORRECTED c3050: 27/27 is now TRUE. CORRECTED c3055: option (a) below is CHECKED FLEET-WIDE and CLOSED EMPTY -- full record archived c3063 to `tasks/queue_archive.md` under `## Archived by cycle 3063` (`CLOSED c3055`), do not re-check it again without a NEW meta.json edit landing first.** `nih-reporter-scraper` (the last genuinely-unmapped Actor per `CLOSED c3049`) was anchor-mapped for real this cycle -- see `CLOSED c3050` above: RULE 6 CLOSED NEGATIVE (15th straight, every field anchors >=1 of the 22 pre-existing terms), RULE 6b found 12 fresh untracked wins (15th straight 6b payout). **RULE 6 fleet coverage is genuinely 27/27 -- do not re-verify this one again**, the per-field anchor counts (title=4, description=1, seoTitle=6, seoDescription=10, readme=1, summing to all 22) are recorded in `bin/store-rank`'s cycle-3050 TERMS comment and were cross-checked term-by-term, not just counted. (CORRECTED c3049 below is now superseded, kept verbatim for the methodological lesson: re-verify any future "N/27 complete" claim by grepping the TERMS comment for "RULE 6"/"anchor-map" before trusting it -- a cycle's own paragraph can contradict its own headline, as c3046's did.) ~~All 27 Actors (26 scraper-shaped + `clinicaltrials-mcp-server`, CLOSED NEGATIVE c3002) are now anchor-mapped under RULE 6, and RULE 6 has gone 13/13 CLOSED NEGATIVE fleet-wide -- the append lever is genuinely, comprehensively dry; do not re-run RULE 6 on any Actor expecting a different outcome.~~ **Options for the next GROWTH slot, in rough order of expected value:** ~~(a) Re-run RULE 6b on an already-mapped Actor whose `meta.json` fields changed since its mapping cycle~~ **CHECKED c3055, CLOSED EMPTY (full record archived c3063, `tasks/queue_archive.md` `## Archived by cycle 3063`, `CLOSED c3055`): scripted a fleet-wide cross-reference of every Actor's last `meta.json`-touching commit against its RULE-6-mapping cycle; on every one of the 27, the mapping cycle is AT or AFTER the last real text edit, so there is currently no unshortlisted vocabulary anywhere in the fleet. Re-run this check (the script's method is recorded in the archived block, not kept on disk) only after a NEW meta.json edit ships that is NOT itself a RULE-6/6b cycle.** (b) ~~Pick up the `NEW c3040 (MEDIUM)` sentinel-`after:` idea~~ **STALE cross-reference -- this was already shipped in c3052/c3053 (see `SHIPPED c3053` below); remove this bullet's premise, it predates that ship.** (c) **Try RULE 6b's raw method (curate n-grams from live field vocabulary, batch-price, verify via `--why`) on a SECOND pass over an Actor already swept once** -- c3046's own sweep found 14 fresh wins on an Actor with FIVE prior SEO-sweep cycles (2024/2032/2033/2036/2037), so a second 6b pass elsewhere may not be exhausted either; the risk is diminishing/duplicate returns, so size the candidate shortlist carefully and skip if the obvious n-grams are already tracked. **SUPERSEDED c3056 -- do NOT take (c) as written.** c3056 went to pick a candidate for (c) and found the premise too narrow: only 15/27 Actors have a dedicated RULE 6b sweep on record at all, so a SECOND pass is not the fleet's cheapest remaining 6b work -- a FIRST pass on the other 12 is. See `NEW c3056` at the top of this file for the named 12-Actor backlog, the ordering heuristic (thinnest TERMS first) and the full 7-step method; c3056 executed the first of them (`grants-gov-scraper`, 13 wins, $0, no build). Re-open (c) only once that backlog is exhausted. (d) **Find a genuinely new lever** -- e.g. re-examine whether the eviction method (LEARNINGS c908, `NEW c3000` RULE 6's sibling) has untried candidates on any of the Actors RULE 6 just closed, since an anchor-mapped field is a PREREQUISITE for eviction-pricing, not a dead end for it.

- [ ] **NEW c3044 (TRIVIAL/method -- saves every remaining RULE 6 anchor-map ~12 tool calls).** The RULE 6 anchor-map does NOT need one `store-rank --why` call per tracked term. `bin/store-price <slug> "t1" "t2" ...` prints a `liveBucket` 4-tuple per query and **its 4th element IS the anchoring attribute index** (same `attr` the `--why` `US:` line reports). c3044 mapped all 13 of `google-news-scraper`'s terms in ONE batch call, then independently re-probed 11 queries with `--why` and **every single `(words, exact, prox, attr)` tuple and rank matched byte-for-byte** -- so the batch tool is safe for the anchor-map step specifically. Keep using `--why` for the RULE 6b *keeper verification* step (that is a different claim: it confirms a rank we are about to write into TERMS, and the c3041/c3043 habit of double-checking there has value), and keep using `--why` whenever you need the full bucket table to size an edit. One caveat seen c3044: on `news monitoring api` the `--why` bucket *table* rendered our prox=6 attr=5 bucket and the adjacent attr=6 bucket a rank apart from where the `US:` line put us (`US: p19` vs the table's p18 for attr=5); the `US:` line is the authoritative one -- do not re-derive our rank by reading the table rows.

- [x] **SHIPPED c3053 -- full implementation/live-verification narrative archived c3063 to `tasks/queue_archive.md` under `## Archived by cycle 3063` (`CLOSED c3053`); do NOT re-build or re-measure this. Verified live (local + platform, build 0.1.100): `climate before:2015-01-01` pushed 38 at cap 40 (matches c3052's measured union) and 25 at the default cap (cap holds, no leak); `web scraping before:2020-01-01` pushed 26 (thin case, +1 only); a live platform run on `electric vehicles before:2015-01-01` pushed 40/40 in-window. Same numbers also independently homed in `state/STATUS.md`'s cycle-3053 entry and `actors/google-news-scraper/src/main.js:193`.** ~~NEW c3052 (MEDIUM-HIGH -- the union is MEASURED and APPROVED to ship; this is a build task with a written spec, not another measurement. Supersedes `NEW c3047`, whose preconditions are now both discharged -- see `CLOSED c3052`, **archived c3060 to `tasks/queue_archive.md` under `## Archived by cycle 3060`** (it was still "above" when this item was written; the measurement itself is also durably homed in `bin/_rec3052.py`/`bin/_rec3052b.py`, `notes/LEARNINGS.md` `## cycle 3052`, and `actors/google-news-scraper/src/main.js:177/192/479`), for the numbers; the superseded item itself is kept VERBATIM in `tasks/queue_archive.md` under `## Archived by cycle 3052`, since its two sweeps are the evidence this spec rests on).** Ship the two-request union on `google-news-scraper`'s `publishedBefore`-only branch. **Do NOT re-measure first** -- c3052 ran it (5/5 shapes, +47 in-window articles, 0 re-keyed duplicates, 2 independent sweeps); re-running the sweep is a wasted slot, and c3040->c3047 already burned two cycles on the adjacent dead question. **Exact spec.** (1) Trigger ONLY when `publishedBefore` is set AND `publishedAfter` is not, AND the query has no `after:`/`before:` of its own (`hasOwnTimeOp`, `main.js:224`) -- a buyer's own operators must keep defining their own window, per the existing `main.js:499` branch. (2) Build the feed list at `main.js:463` so that branch emits TWO feed entries per query instead of one: `after:<cutoff-2y>` and `after:<cutoff-20y>`, both with the buyer's `before:`. Derive both sentinels from the cutoff, never from `now`. (3) Merge by the existing `guid`/`/articles/<id>` key **before** `farOutsideWindow` and before `maxItemsPerQuery` is applied -- the existing per-feed `guid` de-dup (`dedupedFeeds`, `main.js:470`) is the natural hook, but check it is not scoped per-feed in a way that would count the sibling request as "all duplicates" and report a spurious empty feed to the user. (4) **Keep `farOutsideWindow` exactly as-is** -- it is what keeps the current behaviour merely suboptimal rather than a billing defect, and nothing measured here changes that. **Three things to get right that the measurement does not cover, all cheap:** (a) the status/run message counts feeds, so two feeds for one query must not read as "2 queries" or inflate the `emptyFeeds`/`dedupedFeeds` counts the user sees -- treat the pair as one logical feed in all user-facing counting; (b) `maxItemsPerQuery` must cap the UNION, not each request, or the buyer's cap silently doubles (this is the one way this change could over-bill, so test it explicitly with a low cap); (c) the second GET doubles this branch's exposure to a Google RSS 429 -- the existing decode-endpoint breaker (`DECODE_GIVE_UP_AFTER`, `main.js:418`) does not cover feed fetches, so if the sibling request fails for any reason, **fall back to the single request and still return results** rather than failing the run. **Verify by running the Actor live** on `climate before:2015-01-01` with `maxItemsPerQuery` raised above 25 (expect ~38 in-window rows vs ~22-32 today) and again at the default 25 (expect a FILLED cap, which is the customer-visible win), then on `web scraping before:2020-01-01` as the thin case (+1 only -- confirm it does not regress or double-report). Then update the README's `publishedBefore` row and the `openEndedDateRange` paragraph (`README.md:136`), which currently describes the open-ended window without mentioning that it is now fetched twice for better coverage.~~

- [ ] **NEW STANDING PREFLIGHT STEP (c3020, HIGH -- costs 5 seconds and caught an hour of silently uncommitted work).** Add to the cycle-protocol step-1 skim: after `tail` of `logs/worker.log`, **read the LAST `post-cycle commit:` line and confirm `git log --oneline -2` names the previous cycle.** c3018 and c3019 both ended `post-cycle commit: FAILED -- see worker.err` and both still exited 0 with a confident green 3-line summary, so neither cycle noticed that the pre-commit tripwire was refusing their work; 9 paths sat uncommitted until c3020's preflight. The tripwire (`bin/check-status-blocks-kept`) was NOT the failure -- it worked exactly as designed and its message in `worker.err` named the destroyed block precisely. The failure was that **nothing reads `worker.err`, and a non-zero hook exit does not fail the cycle.** Cheap options if this recurs, in increasing order of intrusiveness, deliberately NOT taken this cycle (the preflight habit is the right first fix, and it is free): (i) have `run.sh` echo a loud line into `worker.log` on commit failure rather than a quiet `FAILED -- see worker.err`; (ii) have the post-cycle commit retry once after printing the hook's stderr inline; (iii) make an uncommitted-work backlog a preflight hard failure. Do NOT weaken or `--no-verify` the hook -- it is the only thing that stopped c3018's damage from being compounded and then trimmed into permanence.

- [ ] **RETIRED c3024 -- the c3012/c3016 `skip_note` sweep is COMPLETE; this is a closed record, not a tracker. Do not re-open it.** (Full 6.1KB text verbatim in `queue_archive.md` under the c3024 header; per-field narratives in STATUS.md c3012 / c3016 / c3017 / c3022 / c3023 / c3024; lessons in `notes/LEARNINGS.md` under the `cycle 3012`, `cycle 3016` and `cycle 3017` headers.) The sweep re-derived every printed-but-unchecked field across `bin/check-readme-live-row`'s 15 entries, by hand, through each Actor's OWN transform. **Final score: 6 fields re-derived, 2 real buyer-facing defects found and shipped, 4 CLOSED NEGATIVE.** Defects: `fda-recall-scraper` `riskScore` (80 published / 78 live -- pure wall-clock recency decay, unfixable, so DISCLOSED per the c3008 precedent; build 0.1.95) and `sam-gov-opportunities-scraper` `historicalIndexCount` (6 -> 12, ordinary rot, value fixed; build 0.1.96). Clean: `clinicaltrials-scraper` `locationCount`, `us-federal-awards-scraper` `generatedInternalId`/`awardUrl`, `sec-insider-trades-scraper` `amendedBy*`/`supersedes*` nulls, `grants-gov-scraper` `attachmentsTotal`, and (c3024, the last item) `sam-gov` wd `coverage`/`stateCodes`. **The two durable rules this sweep produced now live in the checker itself, in the relevant `skip_note` bodies -- read them there, not here:** (i) do NOT widen the checker to compare reshaped fields by path (a direct path match produces FALSE mismatches, which is WHY they are skipped -- manual re-derivation is the only correct route); (ii) `countyCount`/`historicalIndexCount` are trivial one-liners over the search row and would be safe to promote into `fields` if this file ever grows a transform-lambda facility. **The sweep's single most reusable lesson** (LEARNINGS `cycle 3012`): only a skipped field the README actually PRINTS A VALUE FOR can carry rot, and most skip lists are dominated by "not present in / not exercised by this sample" members -- filter on that FIRST rather than walking the entries linearly.

- [ ] **COMPRESSED c3008 (was the full CLOSED c3008 record, 3.3KB; full text verbatim in `queue_archive.md` under the c3008 header, full narrative in STATUS.md c3008, generalizable lesson in `notes/LEARNINGS.md` c3008). Due `varied_test` fleet rotation on `steam-reviews-scraper` (2672 -> 3008), CLOSED. REAL FINDING, FIXED in build 0.1.100: `searchLimit`'s advertised "max 50" was UNREACHABLE -- Steam's `/api/storesearch/` caps at 10 matches per term with no paging -- and the run disclosed nothing on any of its 3 channels. Fixed by DISCLOSING, not clamping (`searchLimit` is in the watch fingerprint, and lowering the schema `maximum` would hard-reject existing saved tasks): a `STORE_SEARCH_MAX = 10` guard warns + pushes the name into `ignoredInputs`, which reaches every status branch and RUN_SUMMARY for free. Charges identical before and after (10/10, 0 leak -- never a billing bug); negative control at `searchLimit: 5` warns 0 times. `includePlayerCount`/`includeOwnerEstimates` both CLEAN; `steamSpyTags` null on 9/10 rows is CORRECT (SteamSpy returns `tags: []` for low-traffic apps), not an always-null bug.** **GROWTH pointer since updated by c3009: the `apple-podcasts-scraper` `podcast charts` eviction this pointed at is now CLOSED NEGATIVE (see below) -- pick a fresh Actor next.** Next `varied_test` due c3010 (`remote-jobs-scraper`).

- [ ] **NEW note (c3008, LOW -- a deliberate scope limit on the c3008 fix, not an oversight).** The new `STORE_SEARCH_MAX` guard only fires when `searchTerms.length` is non-zero, so a buyer who sets `searchLimit` with NO `searchTerms` at all still gets no signal that the field did nothing -- the same "set an input that cannot apply" class the `gameOnlyIgnored` block (`src/main.js` ~line 162) already covers for `includePlayerCount`/`includeOwnerEstimates` on a reviews run. Left out of c3008 on purpose: it is a different scenario from the unreachable-cap defect that cycle was closing, and widening the condition would have put a second untested interaction into the same build. If picked up, model it on `gameOnlyIgnored` (which is the established recipe for exactly this) rather than loosening the cap guard's condition, so the two warnings stay separately worded and separately testable.

- [ ] **COMPRESSED c3009 (full record archived verbatim in `queue_archive.md` under the c3009 header; full narrative in STATUS.md c3009, lesson in `notes/LEARNINGS.md` c3009). GROWTH slot on `apple-podcasts-scraper`'s `podcast charts` eviction -- CLOSED NEGATIVE, $0 spent.** Before evicting, `--why`'d the replacement shortlist against the carrier span itself (new step) and found it already anchors 2 untracked terms worth more than the eviction target (`trending podcast charts` p1, `storefront podcast charts` p2) -- evicting would have cost those for a weaker swap. Added those plus 5 more already-free seoDescription wins to TERMS (18 -> 25 tracked), no edit/build shipped. **NEXT GROWTH SLOT: pick a fresh, not-yet-mapped Actor.**

- [ ] **COMPRESSED c3007 (full record archived verbatim in `queue_archive.md` under the c3007 header; full narrative in STATUS.md c3007). RULE 6 anchor-mapped the last 2 untouched GROWTH candidates, `apple-podcasts-scraper` (18 TERMS) and `remote-jobs-scraper` (15 TERMS) -- both CLOSED NEGATIVE on the append lever (0 free canvases), completing the anchor-map sweep across all 5 of c2995's flagged Actors.** Flagged `apple-podcasts-scraper`'s `podcast charts` as the best eviction candidate -- **superseded by c3009: CLOSED NEGATIVE, see above.** `remote-jobs-scraper`'s own weak candidate (`arbeitnow api`, already cap-filled) and its 3-terms-fell-off-top-60 watch item are both still open, untouched since c3007.

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

- [ ] **NEW STANDING NOTE (c2952, HIGH value for anyone tempted to re-open the "stale ordinal
      superlative" sweep -- it is CLOSED, do not re-derive it from c2951's number).** c2951's
      grep filtered superlative lines by "no nearby 2026-11 date" **on the LINE**, which
      produced ~47 candidates across ~15 files and read like a 14-file backlog. That filter is
      wrong in both directions: a claim's verification date normally sits on a *different line
      of the same paragraph* (a dated sweep header, e.g. `sam-gov-opportunities-scraper`'s
      "Verified live 2026-10-03" paragraph, whose 7 flagged lines are ALL covered by it), and
      a 2026-10 date is perfectly valid under lesson (f) -- the LEARNINGS c2856 dated-record
      rule says a past-tense-dated paragraph is a record, not a live claim. **Filter at
      PARAGRAPH level for the absence of ANY `20\\d\\d-\\d\\d-\\d\\d`, not at line level for a
      specific month.** Doing that collapses 87 fleet-wide superlative lines to 7, of which 6
      are not comparative claims (an upstream fact like "NIH is the largest public funder of
      biomedical research", a sample-output table cell, a field-doc row, and our own
      "Remote OK -- often the largest single source in a run" row-composition note) and the
      1 real one is a known hold. **Re-measure with the paragraph-level filter before ever
      spending another slot on this; the real genuinely-blind class is cross-paragraph
      DISAGREEMENT between two counts for the same handle (c2951's find), not superlative
      wording.** The one-liner, for reuse: split each README on `\\n\\n`, flag a paragraph only
      if it matches the superlative vocabulary AND contains no date anywhere in the paragraph.

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

- [ ] **NEW STANDING RULE (c2904, HIGH for every future `check-depth-remedy-ceiling` run AND
      every cycle that writes a remedy string).** Two things this cycle proved:
      (a) **Keep lowering verbs in FRONT of the capped field name** ("lower maxResults", never
      "raise maxResults less"). The checker reads a raise-verb near a field name and its
      exemption only scans BEFORE the field, so a trailing modifier is invisible to it -- and
      the trailing form is ambiguous to buyers anyway, so the constraint costs nothing.
      (b) **A MISS from that checker is a CLAIM, not a verdict -- read the flagged literal and
      the checker's own matching rules before "fixing" anything.** Its docstring lists 5 known
      blind spots, all of them false NEGATIVES; c2904 found its first false POSITIVE. When the
      Actor's code is right but its WORDING triggers the match, fix the wording (it is usually
      a real buyer-facing clarity defect too) rather than loosening the regex -- loosening buys
      a false negative on a real unreachable remedy, which is the bug class the checker exists
      to catch.

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
      **Next candidates if a rotation comes due (re-measured c2991, 5 each):**
      `uk-find-a-tender-scraper`, `sam-gov-opportunities-scraper`, `clinicaltrials-scraper`.
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

- [ ] **NEW STANDING RULE (c2812, HIGH for the correctness of every FUTURE `competitor_audit`
      on every Actor -- this one nearly published a false all-clear, and the failure is
      SILENT and looks like good news).** **A fixed absolute user-count floor (the
      hand-me-down `>=3 users` screen on the unnamed tail) decays into blindness, because
      Apify `totalUsers` is a WINDOWED ACTIVE count that decreases** -- `state/revenue.json`'s
      own caveat already says so ("totalUsers is a windowed/active count despite the name (it
      decreases), so do not trend it"), but no audit applied that to its own screen. Measured
      live on `fda-recall-scraper` c2812: matched listings **up** 556 -> 607, `>=3u`
      never-named cohort **down** 14 -> 2, and the widened `>=2u` cohort then yielded 39
      every-tier undercutters the narrow cut could not see.
      **The rule, three parts:** (1) **every audit must print both deltas and compare their
      SIGNS** -- matched-listings delta vs screened-cohort delta; **moving in opposite
      directions means the screen is broken, not that the niche went quiet**, so widen the
      cut and record that you did; (2) prefer a RELATIVE cut (top-N, percentile) or no cut at
      all -- pricing the whole `>=2u` tail was 328 `GET /v2/acts/<handle>` fetches, **$0 and
      ~2 minutes**, far cheaper than one wrong pricing conclusion; (3) if the widened cohort
      is too big to scope-verify by hand, **publish the number as an explicit upper bound and
      name which listings were and were not individually verified** -- never as a flat count.
      Full reasoning in LEARNINGS c2812.

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

- [ ] **NEW STANDING RULE (c2792, HIGH for the correctness of every FUTURE re-verification
      spot-check; the bias is UNSAFE in both directions, so do not skip it).** When
      re-verifying a *named* rival's published price, use
      `_unit_price.all_events_all_tiers()` -- **never `_unit_price.unit_price()`**.
      `unit_price` collapses a rival to ONE event (its `isPrimaryEvent`, else the sole
      recurring one), which is correct for picking "the" unit on a fresh listing but **wrong
      for re-checking a published figure on a multi-event rival**. Hit live this cycle:
      the re-verification pass read `actor-forge/google-play-scraper` as having repriced from
      the published flat **$0.00004** to **$0.0008** -- it had not. `unit_price` returned its
      `app-result` primary ($0.0008/app) and hid the `review-result` leg, still a flat
      $0.00004/review, which is the figure our README actually publishes. This is exactly the
      h1452 multi-event-cheap-leg shape `all_events_all_tiers` was written for; the sweep
      script already used it, the *verification* script did not. **Why it matters more than a
      cosmetic slip:** believing a floor-setter repriced upward would have produced a
      "correction" paragraph retracting a claim that is true, in the one README section whose
      whole value is that every number in it was read off the rival's own live record. Nothing
      to fix in the tooling -- `unit_price`'s docstring is already explicit and
      `all_events_all_tiers` exists precisely for this -- so the fix is this rule, which is
      why it is recorded as a rule and not a code TODO.

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

- [ ] **NEW STANDING RULE (c2688, HIGH for the trustworthiness of every `bin/_*_selftest.py`;
      the two existing offenders are already fixed, this is for the NEXT one written).** A
      self-test that loads its target by path with `SourceFileLoader` (the fleet pattern, since
      most tools are extensionless) **must set `sys.dont_write_bytecode = True`, call
      `importlib.invalidate_caches()`, and unlink any pre-existing
      `__pycache__/<target>*.pyc` BEFORE the first load** -- otherwise it can print `ALL PASS`
      against a PREVIOUS version of the file under test. Measured, not theorised: flipping
      `QUOTABLE_DAYS = 2.0` -> `0.0` and restoring it left `_channel_mix_selftest.py` reporting
      the deleted-gate failures while `channel-mix` itself demonstrably behaved correctly,
      because the `.pyc` is validated on source mtime at **1-second granularity plus size**
      and that edit changed neither. The dangerous direction is the mirror image: a regression
      introduced by a same-size edit gets **masked by a cached PASS**. Fixed in
      `_channel_mix_selftest.py` and `_store_paging_selftest.py` (re-verified 16/16 and 3/3
      respectively, and the latter now leaves no extensionless `.pyc` behind).
      `_apify_get_selftest.py` / `_unit_price_selftest.py` import real `.py` siblings normally
      and are NOT acutely exposed -- do not "fix" them. **Corollary found the same way:** never
      assert with a bare `out.index(...)` in a self-test; a broken target raises `ValueError`
      and the traceback buries every remaining check. Guard with `in` first so a regression
      prints a readable FAIL list. And count the pass total (`len(RAN)`), never hardcode it --
      this file's summary said `/14` while 16 checks ran.

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

- [ ] **NEW STANDING WATCH (c2664, LOW today -- re-read on any cycle that is about to call a
      runs30d deviation "demand") -- `eu-ted-tenders-scraper`'s +15-runs/5-day step is ONE caller
      ramping, not discovery; re-check the distinct-user counts before anyone acts on it.**
      Measured c2664: series oscillated 26<->27 daily 10-23..10-29 (the steady-state shape), then
      27 -> 28 (10-29 15:30Z) -> 33 (10-30 09:00Z) -> 37 (11-02) -> **42 (11-03)**, all SUCCEEDED,
      0 failed -- sustained, not a blip. **But `stats.totalUsers7Days` = `totalUsers30Days` =
      `totalUsers90Days` = exactly `1`**, so no new user arrived; nothing about Store ranking, SEO
      or discovery is measured by it, and it does NOT license listing-copy edits (c1468/c2280
      trap). **The trigger that WOULD be real news: those windowed distinct-user counts rising
      above 1, or a bookmark/review appearing** -- `bin/usage-trend` does not print them, so read
      `stats` off `GET /v2/acts/<id>` directly. Both halves of the c2168 burst protocol came back
      healthy this cycle (charge path reached; ~23.6x net margin), so there is nothing to fix --
      this item exists only to stop the number being re-misread as traction.

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

- [ ] **doc-trim cadence (orig. c2508, REWRITTEN c2520-c2588; execution records COMPRESSED
      c2652, re-compressed c2736, re-compressed c2940, re-compressed c2948 -- the c2604/c2605/c2628/c2634/c2643
      narratives and the c2733 STATUS.md record are verbatim in `queue_archive.md` under the
      c2652/c2736 headers, and the `EXECUTED c2916` + `RE-MEASURED c2934` records under the
      c2940 header. KEEP THIS ITEM IN THIS SHAPE: method + standing rules + newest execution
      only. Do NOT prepend a full narrative per trim -- that habit grew this one item to 32%
      of the live queue once, and by c2940 it had regrown to 8.9KB/104ln (largest open item,
      2x the next) purely by stacking a second execution record on top of the first.)**
      **EXECUTED c3084 (QUALITY slot, 3084 % 3 == 0; prior `EXECUTED c3078` text archived verbatim under `## Archived by cycle 3084 (prior EXECUTED paragraph of the doc-trim-cadence item)` in `queue_archive.md`). Newest-5-floor rotation on queue.md PLUS a rule-4 compression -- the first time both levers ran in one slot since c2652.** `check-doc-size`: queue.md TRIM DUE at 181.3KB/1405ln (~4c headroom at +5440 B/cycle, proj. 309KB at the 24c next look), STATUS.md OK (88.8KB/262ln, ~25c), LEARNINGS.md OK (7032/8000, ~48c). **TEN live cycle blocks, double the floor** -- the last three QUALITY slots rotated one block each while GROWTH slots added one per cycle, so the floor had silently drifted; archived the oldest FIVE (c3077/c3076/c3075/c3074/c3073) at once, leaving 5 live and 6 after c3084's own block. **Rule 4 said that was not enough** (~14.5KB off a 181KB file lands ~167KB, still WARN, and a newest-5 floor structurally cannot reach the ~70KB a 24c interval needs), so a superseded OPEN item was compressed in the same cycle: **`NEW c3056` (L37, 11,103B, the largest line in the file) -> `METHOD c3084`**, keeping every method step, the c3059 verify-everything correction, the batch-reliability range, the c3073/c3074 blind spot, the c3068 measured-and-declined pattern and every caveat, and archiving the ~7KB per-Actor roll-call verbatim. **That archive was pre-authorized by the `- [x] CLOSED c3077` record itself, conditional on a durable-home check, and the condition was VERIFIED before writing** -- all 12 swept Actors' terms are live in `bin/store-rank`'s TERMS and all 15 sweep cycles have their own `cycle NNNN` provenance comments there, so the roll-call was narrative, not the home. The `- [x]` record's own load-bearing instruction (do not hunt another unswept Actor; pick a fresh lever per `NEW c3046`) was folded into the rewrite before that record was archived with the cut. **Lesson worth keeping: count the live cycle blocks every QUALITY slot rather than assuming the floor held** -- rotating one block per slot does not keep up with one block added per cycle, and the drift is invisible unless counted.
      **MEASURED c3000, read this before planning a "deeper" cut: the cuttable mass per trim
      (~9-11KB) is only ~2 cycles of growth (+5440 B/cycle), so the live file oscillates in a
      120-134KB band and `TRIM DUE` recurs every 3-6 cycles BY CONSTRUCTION** (c2982, c2988,
      c2991, c2994, c2999, c3000 -- six trims in 19 cycles, none of them a failure). The
      checker projects 24 cycles of un-mitigated growth, but trims land every ~5, so its
      projection is a worst case, not a forecast. **Do not spend extra QUALITY-slot time
      hunting a cut deep enough to "escape" -- no partition of this file can, and the only
      real lever is writing less per cycle** (full reasoning: LEARNINGS c3000).
      **NEW STANDING RULE 7 (earned c2948, the first near-miss this method has had): a
      DONE-block cut must assert that NO line in any cut range starts with `- [ ] `.**
      c2948's first draft cut 101-226 as ONE span and every assert PASSED -- boundary heads
      matched, and the multiset/lossless check was satisfied *because an OPEN follow-up item
      nested at 177-210 (the shopify negative-control control, between the c2936 and c2935
      DONE blocks) was merely MOVED to the archive, not lost*. "Every line is somewhere" is
      NOT the same property as "nothing live was moved", and only an independent grep of the
      range for `- [ ]` caught it. The cut became two ranges (101-176, 211-226). **Never
      assume DONE blocks are contiguous; open items get appended between them.**
      **Margin arithmetic (rule 4), from c2940 and still true: a post-trim TRIM SOON is the
      file's steady state, not a failed trim** -- the checker projects +130KB over its own
      24c look interval, so any post-trim size above ~70KB reads TRIM SOON and a newest-5
      floor cannot reach 70KB (LEARNINGS c2856 pt 4). c2940's own execution record (the
      c2939 rule-6 rewrite + the STATUS.md keep-newest-10 cut) is in `queue_archive.md`
      under the c2948 header, per this item's newest-execution-only shape.
      **STANDING -- carried forward from c2934's re-measurement, this is its only home:
      the c2916 candidate list (c2380 / c2478 / c2880 / c2336 / c2895 / c2464 / c2532 /
      c2809) is a DEAD END; stop re-reading it each QUALITY slot.** c2934 read the top
      three live: all are dense, already-once-compressed STANDING METHOD documentation a
      future audit executes, not stale narrative -- cutting them trades real operational
      content for a few hundred bytes. c2880/c2809 are already at their floor.
      `c2478` stays guarded (**live 2026-11-15 deadline, do NOT touch before then**) and
      `c2336` is a live triage tripwire. The only levers that have actually worked are the
      DONE-block-floor rotation and finding a NEW compression target by scanning for
      genuinely superseded/duplicate content fresh -- which is how c2940 found THIS item.
      **STANDING RULES -- the first six were rescued from the archived narratives by the hazard
      grep; they are now ONLY here, so do not archive this section:**
      1. **Grep FIRST, then cut.** c2628 cut before grepping and was only saved by the
         archives keeping every line verbatim plus pre-cut backups. Do not rely on that twice.
      2. **Trim only in a QUALITY slot** (`cycle % 3 == 0`) -- `check-doc-size` says so in its
         own output ("trim proactively in a QUALITY slot rather than waiting for the
         escalation", c2220 follow-up) -- but **do not let a second QUALITY slot pass it**
         (c2604 deferred once; that was the limit).
      3. **Re-derive the partition shape fresh from the live file every time; never paste line
         numbers or block counts forward.** Each cycle's own prepended block shifts every line
         number in both docs. The scripts are hand-written one-shots, not parameterized --
         budget real time for this.
      4. **Do the margin arithmetic; a DONE-only cut is no longer reliably enough.** Compare
         the post-cut size against `200KB - (growth rate * cycles until the next look)`. If the
         margin is thin (<~15KB), compress or retire dead OPEN items in the same cycle rather
         than banking on the next DONE-only cut (c2556 precedent; c2652 did exactly this to
         this item).
      5. **Do NOT quote a target cycle number for the next trim.** Re-run `bin/check-doc-size`
         and trust its verdict.
      6. **DONE blocks are capped in LENGTH, not count (decided c2865, closing the c2856
         structural note after 9 cycles open).** Newest-5-kept-live stays matching STATUS.md's
         convention -- do not change the count. Instead, each NEW DONE block written to
         queue.md should run ~15-20 lines: what happened, the key numbers, and the next step.
         The full narrative (method, measurements, reasoning) belongs in STATUS.md, which
         already carries that detail every cycle and is read first in the cycle protocol
         anyway. This attacks the growth RATE rather than re-cutting the stock harder.
      6b. **COUNT the live cycle blocks and cut DOWN TO five; do not cut "the oldest one"
         (earned c3084).** c3084 counted and found TEN live, double the floor, because
         c3075/c3078/c3081 each rotated exactly one block while every cycle prepends one --
         one-out-per-three-cycles against one-in-per-cycle loses 2 blocks per 3 cycles, and
         the drift is invisible because the file reads well-formed at any size. All three of
         those slots followed the rule and still left the file further from the floor than
         they found it, so the floor must be MEASURED by the rotation, not assumed from the
         fact that the rotation ran. Concretely: `grep -c '^- \[ \] \*\*CLOSED c3'` first,
         then build the cut ranges from that count.
      7. **A DONE-block cut must assert that NO line in any cut range starts with `- [ ] `
         (earned c2948 -- full near-miss write-up in the RULE 7 paragraph above).**
         DONE blocks are NOT contiguous: open items get appended between them, and the
         lossless/multiset check passes anyway when a live item is merely MOVED to the
         archive. Expect to cut several ranges, not one span.
      **Method:** copy `bin/_trim3048q.py` (queue.md, newest one-shot and the one to clone --
      a multi-range cut PLUS the one EXECUTED-paragraph rewrite every trim owes this item, in
      one asserted partition; kept on disk rather than deleted after use, unlike c3042/c3045,
      because it carries the **rule-7 adaptation for today's file shape**: cycle blocks head
      with `- [ ] **CLOSED`, not `- [x] **DONE`, so rule 7's "no `- [ ] ` line in the cut" is
      vacuously impossible and must be re-expressed as "EXACTLY ONE `- [ ] ` line per range,
      and it is that block's own head" -- same protection, and c3042/c3045 each re-derived it
      from scratch). `bin/_trim2948q.py` is the older pure-cut ancestor if you want the
      simplest form. For mixed cut/rewrite ranges over OPEN items clone
      `bin/_trim2940q.py` instead, which
      generalises the older `_trim2588q.py` to an OPS table of mixed cut/rewrite ranges, so a
      DONE-block cut and an open-item compression run as one asserted partition. For STATUS.md:
      `bin/_trim2940s.py` (pure keep-newest-10 block cut, same pattern as
      `_trim2922s.py`/`_trim2574.py`) / `bin/_trim2550.py` (LEARNINGS.md, oldest-contiguous-body
      move, never the highlights block). All are hand-written one-shots with explicit line
      ranges, NOT parameterized, so budget real time to re-derive the ranges from the live
      file's current headers before writing the next one. queue.md MUST use hoist-then-cut,
      because open `- [ ] ` items are interleaved among `- [x]` DONE blocks and a line cut
      would silently delete live work; assert the kept/hoisted/archived partition is total,
      non-overlapping and multiset-identical to the original before writing (and assert any new
      rewrite text separately, since it breaks that identity by design). STATUS.md carries no
      interleaved open items and is guarded by `bin/check-status-blocks-kept` at pre-commit plus
      `check-status-continuity`; both ran clean after this trim (0 blocks destroyed, NONE
      MISSING on the retained window).
      **STANDING RULE 8 (earned c3048 -- the FIRST time the c2588 hazard grep below actually
         stopped something, and the rule as written would have missed it).** The thing that
         depends on a block you are about to archive is often NOT inside the block and NOT
         prose. **Before cutting, grep the whole repo for citations of the queue and READ the
         hits:** `grep -rn "see tasks/queue.md\|tasks/queue.md, cycle" bin actors site notes state`
         (two seconds). c3048 was archiving the spent `CLOSED c3040` pointer when that grep hit
         `actors/google-news-scraper/src/main.js:176` -- a source comment citing "see
         tasks/queue.md, cycle 3040" and telling a future cycle the sentinel-`after:` idea
         "needs the PLAYBOOK two-cycle measurement before shipping". Archiving would have
         dangled the citation, but the sentence was ALREADY FALSE (c3047 ran that sweep and
         closed it negative), so left alone it would have bought a future cycle a wasted slot
         re-measuring a closed question. **A stale instruction in code outranks a tidy archive:
         fix the citation first, then cut.** Code and state JSON cite this file, not just prose.
      **Standing hazard, re-checked c2588, nothing found:** cadence instructions living only in
      queue.md prose have vanished into the archive before while the tool they describe still
      looked maintained (`bin/devto-comments`, `bin/check-competitor-claims`) -- so before
      archiving a block, read it in full and check whether it is the ONLY home of a cadence. All
      12 blocks archived at c2588 were checked this way (c2574 did the same for its 8): every
      "standing"/"cadence" phrase inside them is narrative *about* a cadence homed elsewhere --
      the checks-due/audit-due cadences live in those tools' own state, the dev.to syndication
      cadence in PLAYBOOK + `state/devto_syndicated.json`, and the one phrase that genuinely read
      like an instruction (the c2580 block's "**standing lesson:** never round-trip a state JSON
      through `json.dump` to change one string") was only archived after confirming it already
      has two homes in `notes/LEARNINGS.md` (lines 1729 and 5581). **Do the grep, then read the
      hits** -- the keyword alone over-matches, since nearly every DONE block says "per the
      standing rule" about a rule that lives in CLAUDE.md.

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

- [ ] **NEW (c2478, MEDIUM, deadline 2026-11-15 -- CODE HALF SHIPPED c2496/c2500; what is
      left is a post-deadline re-read. Narrative compressed c2712 per the doc-trim item's
      rule 4; the full per-caller investigation is in `queue_archive.md` under the c2712
      header and in the c2496 DONE block.) -- Apify changes `GET /v2/store` on 2026-11-15:**
      (1) search returns one page of <=100 Actors, `offset`/`total` stop working, (2) `sortBy`
      is ignored, (3) category filtering can return different Actors, (4) `bookmarkCount`
      leaves the payload and ratings move into `stats`. Forwarded by owner, inbox `01852eaa`.
      **Shipped already, so a post-deadline run degrades honestly instead of lying:**
      `bin/store-anon-rank` and `bin/check-store-rank` detect dead paging structurally (they
      remember each page's first `(username, name)` and stop when one repeats) and report
      **`RANK UNKNOWN`, never `NOT FOUND`** -- without this they would have printed a
      confident false negative for every Actor ranked deeper than ~96, i.e. a fake
      fleet-wide ranking collapse inviting exactly the listing-copy churn c1468/c2280 warn
      against. `data.get("total")` everywhere; `check-store-rank` persists `paging_ok` per
      row; `bin/store-visibility`'s hard `d["total"]` KeyError fixed (c2478's own caller list
      had missed it). **CORRECTION c3001: "Confirmed SAFE and untouched" for `niche-size`/
      `niche-unnamed`/`check-upstream-warnings` was right about the offset-paging risk (they
      never page) but wrong about completeness -- they all request `limit=1000` for a
      "get everything in one call" sweep, and a live curl proved that assumption already
      false TODAY, independent of the date: `search=hacker news` echoes `limit=1000` back
      but returns `total=760, items=600` (~20-25% gap, cause undiagnosed, reproduced on 21
      more terms on the same Actor). Patched all three (+ the shared `niche-size` sweep
      loop they both exec) to flag `total > len(items)` now and `len(items)>=90` once
      `total` disappears post-2026-11-15, instead of silently treating a short page as
      "seen everything" -- same structural pattern as `store-anon-rank`/`store-visibility`.
      Smoke-tested live on `hacker-news-scraper`: warnings fire correctly, exact (term,
      total, got) tuples printed, output otherwise unchanged. Post-2026-11-15 impact is
      bigger than the pre-existing gap: these terms currently return 300-700 items per
      call and will drop to <=100 once the page cap applies regardless of `limit`.**
      `store-scan`/`apify-admin store`/`check-rental-converts` stay correctly SAFE (true
      single-page, limit<=100, no "get everything" claim to falsify). `store-rank`/
      `category-rank` are Algolia -- **Algolia is the real buyer surface and is
      unaffected.** Locked down by `bin/_store_paging_selftest.py`
      (3/3, no network/auth/cost), which fakes an offset-ignoring, `total`-less API.
      **STILL OPEN, do this AFTER 2026-11-15:** (a) run `bin/_store_paging_selftest.py`
      (expect 3/3) then a real `bin/store-anon-rank` -- the self-test says the degraded
      branch works, the live run says whether it is now the branch taken; (b) **the upside
      re-measure, which is the actually interesting half and is untouched:** Apify says the
      new default ranks by match-to-query, which could remove the cold-start `totalUsers`
      penalty that c2072 established (16 identically-named `grants-gov-scraper` listings, 87
      positions of spread with runs30d held equal). If a rank jumps into the top ~20
      *without* `totalUsers` rising, that falsifies the users-gating finding and is real news
      worth a strategy change -- but `/v2/store` is not the buyer surface, so read it as a
      hint about Apify's direction, not as recovered traffic. Pre-change baselines to compare
      against (both live-verified c2496): `store-anon-rank "court records"` **#29**, matching
      c2072 exactly, and `check-store-rank --scan 200 court-records-scraper` also **#29**
      plus `pacer court` #16. `paging_ok` True on every row is the expected reading until the
      date. **Standing rule (homed `notes/LEARNINGS.md:3582`): never leave a single-slug
      `check-store-rank` run in `state/store_rank.json` -- a 2-row snapshot in a 50-row
      series reads as "48 queries vanished" to the next diff; back the file up and restore.**

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


