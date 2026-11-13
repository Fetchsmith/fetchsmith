- [ ] **CLOSED c3144 -- QUALITY slot (3144 % 3 == 0, recomputed by hand). Both owed doc trims, one slot.** Preflight fresh: `checks-due --all` NONE DUE (soonest `check-status-continuity` c3147), `audit-due --all` FLEET ROTATIONS NONE DUE (soonest `competitor_audit` on `eu-ted-tenders-scraper` c3146), inbox routine noise only, `bin/revenue` unchanged ($0, 27 Actors, 54 users, 1462 runs30d), services/site 200, c3143's commits landed.

  **Work 1 -- `queue.md` newest-5 rotation (`bin/_trim3144q.py`), CLOSED.** 6 live blocks counted fresh vs the floor of 5 -- one cycle of ordinary drift, not a backlog (c3141 left 5; only the merged c3142/c3143 landed since). RULE 1/8 hazard grep clean (all hits narrative, in STATUS.md / the `audit_dates.json`+`fleet_checks.json` note strings / `EXECUTED c3141`'s own list of what it left live). RULE 4: nothing free (`NEW c3116`, `NEW c3046`, `NEW (c2478)` guarded to 2026-11-15) -- pure rotation of `CLOSED c3134/c3135`. **RULE 7 held the STRICT way for once** (range has exactly one `- [ ] ` line, its own header -- no adaptation, contrast c3141's 9-header range). **168.4KB/1127ln -> 158.1KB/1121ln, ~8c headroom.** Still TRIM DUE after = documented steady state (MEASURED c3000).

  **Work 2 -- the `state/STATUS.md` cut c3140 and c3143 both deferred to "a future QUALITY slot" (`bin/_trim3144s.py`), CLOSED before it went DUE.** Pure suffix cut (no interleaved open items, so no RULE 7 hazard): cycles <=3134 moved verbatim to `STATUS_ARCHIVE.md`. **114.9KB/351ln -> 34.1KB/97ln, now OK with ~38c headroom.** **Keep this refinement: it kept the newest NINE blocks, not ten** -- the floor is 10 live, but the trimming cycle then prepends its own, so c3126's keep-10 ended at 11; keeping 9 lands exactly 10.

  **Verified.** Both scripts dry-run before `--write`: fresh-derived boundary asserts, Counter partition, full lossless check, survivor/cut asserts with headers matched **anchored to line start** (the same regex `check-status-continuity` uses -- unanchored matching is what made `_recover2136.py` skip c2133). `git diff --stat`: STATUS.md -254/archive +256, queue.md -5/archive +7, STANDING.md 1 line in place, no reformat. Guards clean: `check-status-blocks-kept` 0 destroyed, `check-status-continuity` NONE MISSING (9/9 in the new 3135..3143 window), `check-shell-expansion` 307 files/0 damaged. STANDING.md's doc-trim item: `EXECUTED c3141` replaced in place by `EXECUTED c3144`, old text archived verbatim (newest-execution-only shape).

  **LESSON (c3144, and this block is the evidence).** My first draft of this very block ran **9KB** and took queue.md from 158.1KB straight back to 167.0KB -- a deeper trim than the one it was reporting, undone by the report. Rewritten to ~3KB. **The trim is not the lever; the per-cycle write is** (LEARNINGS c3000 said so, c3084 measured it). Budget a cycle block at <=3KB and put detail in STATUS.md or a persisted dataset, not here.

  **Blockers: none. Owner email: none owed.** $0 spend, doc-only, no build/run/network beyond preflight. Services/site 200 post-work. **Next cycle c3145 is Regular (3145 % 3 == 1, recompute by hand).** **Doc state after this cycle:** queue.md is at its newest-5 floor, STATUS.md OK with ~36c headroom -- but **`notes/LEARNINGS.md` is now ONE line under its cap projection (7519; 24c proj. 7999 vs cap 8000), so the next cycle that appends ANY entry flips it to TRIM DUE.** That is the next owed doc job, and it is a different shape: move the OLDEST contiguous block of the chronological body (never the newest-first highlights at the top) to the END of the archive, and cut **DEEP** -- the checker's own note records c1976 cutting to 7604, instantly re-reading WARN, then recutting to 5928. Target ~5900, not the minimum that clears.

- [ ] **CLOSED c3142/c3143 -- Regular/GROWTH slot (3142 % 3 == 2, recomputed by hand). Preflight re-run fresh:** `checks-due --all` **NONE DUE** (soonest `check-status-continuity` in 5c, c3147). `audit-due --all` showed `competitor_audit` **DUE on `grants-gov-scraper`** (per c3140's forecast of "in 2c"). `inbox list 10` same routine noise (backlink/guest-post solicitations, TinyGate pitch, DMARC reports, the two already-resolved owner Apify-incident emails) -- no actionable mail, no owner email owed. `bin/revenue` unchanged ($0 booked, 27 public Actors, 54 users, 1462 runs30d, 0 bookmarks, 0 reviews). Services active, site 200 on `/`/`/tools`; `git log --oneline -3` confirmed c3141's two commits (`67b0ed71`/`f1c79381`) landed, tree clean apart from `bin/revenue`'s own timestamp writes.

  **Work -- `competitor_audit` on `grants-gov-scraper`, cycle A (sweep only, NOT closed -- `audit_dates.json` deliberately NOT bumped, per the steam-reviews/hacker-news two-cycle precedent).** Own price re-verified first: `check-own-price-freshness` 0 drift on this Actor (fleet flagged only `uk-find-a-tender-scraper`, unrelated, left for its own audit). Fresh `niche-size`/`niche-unnamed` sweep: **3455 seen / 179 matched** (up from 167 at c2806) **/ 98 unnamed** (95 NONE + 3 OWNER, up from 96 at c2806; README now names 78 handles). `niche-size` flagged its own standing **truncation WARNING on all 15 search terms** (items returned < `total` reported) -- a pre-existing, already-documented Store API caveat, not a new finding; counts above are a floor.

  **Priced the >=3-user NONE-bucket cohort (the standing method's first cut): 2 genuinely new handles.** `taroyamada/procurement-intel-actor` (20 users; TED+SAM.gov+Grants.gov combo, thinner fields) -- live primary event (resolved via `check-price-superiority`'s own `effective()` picker, not the raw `pricingInfos` array naively, since it carries 2 historical price records) is `apify-default-dataset-item` at a flat **$0.008/row**, no start fee -- 5.3x our $0.0015 enriched rate, dearer at every volume. `seibs.co/grant-funding-intel` (4 users; Grants.gov + IRS 990-PF combo) -- primary `funder_record` at a flat **$0.006/row** -- 4x ours, also dearer throughout. **Also checked 2 same-owner `taroyamada` satellite listings below the 3-user floor** (same-owner-cluster convention this README already applies to `nexgenwatch`): `grants-gov-funding-digest` (2u, $0.008/row) and `government-tender-grants-monitor` (2u, $0.006/row primary + several $0.08-7 alert/report events) -- both dearer too. **0 undercutters found in this cohort; no README change needed/made.** Full dataset persisted to `state/audit_data/c3142_ggs_prices.json`.

  **NOT done this cycle, carried to cycle B: the remaining ~93 unnamed handles (all <3 users, the NONE tail below taroyamada/seibs.co, plus the 3 OWNER-bucket candidates) are not yet priced.** Next cycle on this Actor should run `bin/niche-unnamed grants-gov-scraper` fresh (re-derive, don't trust 93), price that tail event-by-event/tier-by-tier the same way prior full sweeps did (c2806's note in `audit_dates.json` is the template), write the dated README disclosure paragraph for anything that undercuts, ship the build, re-run fleet-wide `check-price-superiority`, THEN bump `audit_dates.json`'s `grants-gov-scraper.competitor_audit` to that cycle's number with a fresh note (prepending, not overwriting, per this file's `[prior note preserved]` convention). $0 spend this cycle (read-only GETs only). Services/site re-verified 200 post-work.

  **Cycle B (c3143, Regular/GROWTH slot, 3143 % 3 == 1), CLOSED.** Re-derived the unnamed tail fresh rather than trusting c3142's "~93" estimate: `niche-unnamed` now shows 99 unnamed of 180 matched (up from 98/179 -- minor drift). Excluded the 4 handles c3142 already priced, leaving **95 handles (all 1-2 users)** to price via `bin/_batch_price_ggs2.py`. **Result: 5 genuine every-tier undercutters, no meaningful start fee on 4 of them.** `bepolabs/us-grants` bills a flat $0.00075/opportunity with no start fee at all. `best_celerytop/grants-gov-scraper` (agency contact email/phone + attachments beyond our own fields) bills a flat $0.001 behind a negligible $0.00005 start. `plotpointtech/grants-gov-federal-grants` (forecasted-grant + daily-alert features matching our own forecast/watch scope) tiers $0.001->$0.00062 behind the same negligible $0.00005 start. `owlabee/grants-gov-api` (broader SAM.gov+USAspending combo with new/updated flags and webhooks -- a real watch-mode equivalent) tiers $0.001->$0.0008 behind a negligible $0.00005 start; its separate `opportunity-detail` enrichment event is dearer than us. `datadesk-io/grants-gov-opportunities-scraper` tiers $0.001->$0.0008 behind a real $0.005 Actor-start fee -- crossover ~10 rows FREE/BRONZE, ~7 GOLD+. **One ambiguous multi-event listing was hand-read and resolved as a genuine partial undercutter:** `dennydevelops/grants-gov-watcher` (an only-new/daily-alert watch product) has no primary-event flag across two recurring events, `grant` ($0.0012) and `query` ($0.0003); its own description makes `grant` the comparable per-opportunity unit -- undercuts our $0.0015 by $0.0003/row, but carries a real $0.001 Actor Start fee, so crossover is ~4 rows per run; the separate `query` charge was left uncounted. Remaining 89 of 95 priced dearer than our enriched rate at every tier they offer, and none of the 95 is on Apify's FREE model.

  **Verified, not assumed.** Own ladder re-verified live first via `check-own-price-freshness`: 0 drift on this Actor (fleet-wide only `uk-find-a-tender-scraper` flagged, unrelated, pre-existing). `git diff --stat` on the README: 1 file, +2 lines, one new dated paragraph before the closing run-log sentence, no reformat. `apify push --force -w 600` -> build **0.1.88 SUCCEEDED**, confirmed live via `taggedBuilds.latest.buildId` (`D4yMpsMyYHBQlcF0H`) matching the push log's Build ID. `check-price-superiority` re-run fleet-wide: **2753 named-rival prices compared, 0 undisclosed anywhere**, no new flag on this Actor (all printed advisories were pre-existing UNIT-MISMATCH/GONE/RUNFEE items on other Actors). `state/audit_dates.json`'s `grants-gov-scraper.competitor_audit` hand-updated (2806 -> 3143) via a surgical Python string-replace (never `json.load`/`json.dump` reformat, per the c3129 lesson) -- `git diff --stat` confirmed exactly 2 lines changed, JSON re-parsed clean, prior c2806 note preserved verbatim. Full 95-handle dataset persisted to `state/audit_data/c3143_ggs_prices.json`. `audit-due --type competitor_audit` re-run: **NONE DUE fleet-wide**, soonest `eu-ted-tenders-scraper` in 3c (c3146). Commit `09c3f52f` landed, pre-commit hooks green, tree clean post-commit.

  **Blockers: none. Owner email: none owed.** $0 spend -- one Actor build (README-only), 95 read-only pricing GETs. Services/site re-verified 200 on `/` and `/tools/grants-gov-scraper` post-work.

- [ ] **CLOSED c3140 -- Regular slot (3140 % 3 == 2, recomputed by hand). Preflight re-run fresh:** `inbox list 10` same routine noise as c3139 (backlink/guest-post solicitations, a TinyGate pitch, a "My Slop" mention, DMARC reports, the two already-resolved owner Apify-incident emails) -- zero actionable new mail, no owner email owed. `bin/revenue` unchanged ($0 booked, 27 public Actors, 54 users, 1462 runs30d, 0 bookmarks, 0 reviews). `checks-due --all` **NONE DUE** (soonest `check-status-continuity` in 7c, c3147). `audit-due --all` showed `competitor_audit` **DUE on `hacker-news-scraper`** -- it rolled in this cycle (last audited c2804, 336c gap exactly), so despite c3139 reporting the backlog empty there WAS a fleet rotation item; took it as the cycle's work. Services active, site 200 on `/`, `/tools`, `/tools/hacker-news-scraper`; `git log --oneline -3` confirmed c3139's commit (`d22c11e4`) landed, tree clean at start.

  **Work -- `competitor_audit` on `hacker-news-scraper` (eighteenth sweep), CLOSED in one cycle as a deliberate INCREMENTAL sweep.** The judgement call that shaped the whole cycle: `c3103` (2026-11-12, ONE DAY / 37 cycles earlier) had already run a genuine full 322-handle rung-for-rung sweep of this exact niche as part of a `check-competitor-claims` resweep, with the dataset persisted at `state/audit_data/c3103_hn_prices.json`. Repeating ~316 GETs would have bought nothing, so this sweep priced the **set-difference** instead. Own price re-verified LIVE first from raw `pricingInfos` (never carried): unchanged since 2026-09-26, FREE $0.0002 / BRONZE $0.00017 / SILVER $0.00013 / GOLD+ $0.0001, single `result` event, no start fee. Fresh cohort via `niche-size` + `niche-unnamed`: **772 seen / 502 matched / 372 unnamed (316 NONE, 56 OWNER)** vs c3103's 762/498/377 (322 NONE, 55 OWNER).

  **STANDING RULE c2812 sign check tripped, and the explanation is the interesting part: matched +4 but unnamed -5 -- OPPOSITE signs, which the rule says normally indicates screen decay.** It is NOT decay here, and the cause is mechanical: c3103's own README edit named 3 new $0 substitutes and 5 new undercutters, which MOVED those handles out of the unnamed tail into the OWNER/named bucket (OWNER 55 -> 56 confirms the direction). **Generalizable: the c2812 sign check produces a false decay signal whenever the IMMEDIATELY PRECEDING sweep on the same Actor shipped new disclosures -- our own naming is a second force on the unnamed count, independent of niche growth. Check `git log`/the previous sweep's disclosure count before reading opposite signs as decay.**

  **Result: 6 genuinely new handles, all priced, and the first sweep in this niche's history to find NOTHING new.** All 6 live-priced rung-for-rung via `bin/_batch_price_hn3.py` with both args explicit (0 unresolvable, 0 in the AMBIGUOUS/hand-read bucket). **All 6 are dearer than us at every one of our six rungs, and all 6 also carry an Actor-start fee we do not:** `lx112/hacker-news-scraper` (2u, $0.0003/item +$0.00005), `consequential_programmer/hacker-news-scraper` (2u, $0.0005/story +$0.00005), `lowcountrytech/hacker-news-scraper` (2u, $0.0005/story +$0.00005), `felixgoldwin/hacker-news-scraper` (1u, $0.001/row +$0.005), `dabooti/hacker-news-scraper` (1u, $0.0003/item +$0.00005), `tenfoldfleet/brand-mentions-monitor` (1u, $0.0025/mention +$0.00005 -- a Bluesky/HN/Mastodon brand monitor, not an HN scraper). Undercutter list UNCHANGED: nothing added, nothing retracted. **Cross-checked the disclosure surface a second, independent way rather than trusting the unnamed-tail sweep alone:** `niche-size`'s top-10-by-users -- `gentle_cloud` 261u, `epctex` 203u, `ryanclinton` 181u, `nomad-agent` 96u, `logiover` 73u, `miccho27` 65u, `shahidirfan` 58u, `nexgendata` 51u, `automation-lab` 33u, `constructive_calm` 29u -- **every one already named in our README** (grepped, not assumed); the whole unnamed tail now tops out at 10 users (`lokki/news-finder-monitor`, $0.005->$0.0035 +$0.02 start, dearer than us everywhere).

  **Verified, not assumed.** `git diff --stat` on the README: 1 file, **+2 lines** (one new dated `Eighteenth sweep` paragraph before `## What we do not claim`, no reformat). `apify push --force -w 600` -> build **0.1.110 SUCCEEDED**, confirmed live via `taggedBuilds.latest.buildId == sY7JaMaU7fdckgexz` matching the push log's Build ID (not just trusting the log). `check-price-superiority` re-run fleet-wide: **2745 named-rival prices compared, 0 UNDISCLOSED anywhere**; the count is itself an exact internal cross-check -- 2738 at c3139 **+ the 7 handles this paragraph newly names** = 2745. Zero new flags on this Actor (its RUNFEE lines all read `disclosed`). `state/audit_dates.json`'s `hacker-news-scraper.competitor_audit` hand-updated 2804 -> 3140 via a surgical Python string-replace (never `json.load`/`json.dump`, per the c3129 reformat hazard) -- `git diff --stat` confirmed exactly 2 lines, JSON re-parsed clean, prior c2804 note preserved verbatim. Datasets persisted: `state/audit_data/c3140_hn_prices.json` + `c3140_hn_unnamed.txt`. `audit-due --type competitor_audit` re-run: **NONE DUE fleet-wide**, soonest `grants-gov-scraper` in 2c (c3142).

  **Blockers: none. Owner email: none owed.** $0 spend -- one README-only build, 7 read-only pricing GETs for the sweep plus `check-price-superiority`'s own pool. Services/site re-verified 200 post-work.

- [ ] **NEW c3140 (TRIVIAL/checker precision -- a KNOWN FALSE POSITIVE, do NOT "fix" the README).** `check-price-superiority` reports two `GONE ... is 404 on Apify but still named here` lines against `hacker-news-scraper/README.md:123`: **`omcljs/om` and `reagent-project/reagent`**. Neither is an Apify handle -- they are **GitHub repo paths** in that Actor's GitHub-enrichment example output (ClojureScript repos), and `owner/name` is the same shape as an Apify handle, so c2832's "non-handle tokens such as repo paths are no longer counted" filter does not catch them. **Bias is SAFE** (it over-reports dead rivals; it can never hide a live undercutter), so do not rush. If a future cycle does tighten it, the fix is a scope guard on the GitHub-enrichment section, not a README edit -- removing the repo names would damage real buyer-facing example output. Same class as the `check-competitor-claims` user-count gap in `NEW note c2816`.

- [ ] **CLOSED c3139 -- Regular/GROWTH slot (3139 % 3 == 1, recomputed by hand). Preflight re-run fresh:** `inbox list 10` same routine noise as c3138 (backlink/guest-post solicitations, a TinyGate pitch, a "My Slop" mention, DMARC reports, the two already-resolved owner Apify-incident emails) -- re-confirmed `secrets/env`'s `APIFY_TOKEN` byte-matches the token the owner sent in `f11632f7`, zero actionable new mail, no owner email owed. `bin/revenue` unchanged ($0 booked, 27 public Actors, 54 users, 1462 runs30d, 0 bookmarks, 0 reviews). `checks-due --all` **DUE NOW (1): `check-dead-endpoint-docs`** -- ran it first (cheap, network-free): 1 retired endpoint found in Actor source (steampowered `appreviews`), 4 blog mentions checked, **0 undisclosed**, recorded (`last_cycle` 3115 -> 3139, next due c3163). `audit-due --all` then showed `competitor_audit` DUE on `substack-scraper` (the sole remaining backlog item per c3138's handoff) -- took it as this cycle's main work. Services active, site 200 on `/` and `/tools`; `git log --oneline -3` confirmed c3138's commit (`994a4991`) landed, tree clean at start.

  **Work -- `competitor_audit` on `substack-scraper`, incremental sweep (fourteenth), CLOSED in one cycle (not split A/B -- small enough cohort).** Own price re-verified live first: unchanged since c2800 (result $0.002->$0.00078, metadata $0.00112->$0.00039, leaderboard-row $0.0015->$0.0005, comment $0.00056->$0.00019, no start fee). `niche-size`: 363 matched (up from 338 at c2800). `niche-unnamed`: 233 unnamed of 363 (223 NONE, 10 OWNER) vs c2800's 231 of 338 -- small growth (+25 matched, +2 unnamed), so rather than redo the full 230-handle resweep, priced only the fresh **>=3-user unnamed cohort (15 handles)** via `bin/_batch_price_substack2.py /tmp/substack_handles_ge3_c3139.txt` (0 unresolvable). Rung-for-rung pass: 0 every-tier undercutters in this small cohort (legacy scalar-vs-FREE would have over-flagged 5). Found **5 genuine partial undercutters** (cheaper on Free/Bronze/Silver, we win Gold+): `zinin/substack-publication-scraper` (5u, $0.001->$0.0008 + $0.004 start fee), `clearpath/substack-scraper` (5u, $0.00199->$0.00139 + $0.005 start fee, broader-scope whole-archive/Notes/profiles), `adaptive_nightmare/substack-scraper` (3u, flat $0.001, no start fee), `kamerozkan/substack-scraper-posts-notes` (3u, $0.0012->$0.00096, no start fee, also scrapes Notes), `s-r/substack-scraper` (3u, flat $0.001, no start fee found). One decoy-FREE-tier case disclosed too: `neronbaez/substack-scraper` (3u) reads $0.00001 on Free then jumps to a flat $0.002 from Bronze up -- only genuinely cheaper than us on the Free plan itself. Excluded as non-substitutes (not priced against our core events): `aurenic/newsletter-author-contacts` + `matidepa22/newsletter-sponsor-finder` (contact/lead-gen, not content), `clearpath/newsletter-list-cleaner` (subscriber validation), 4x `data_direct/substack-*-scraper` (narrow single-endpoint wrappers -- one note/profile/post-comments/user-posts -- not bulk publication scraping, all dearer than us anyway), `delectable_incubator/substack-people-scraper-low-cost` (3u, creator profiles not posts, dearer than our Free tier $0.00238 vs $0.002), `juryless_lens/ai-training-data-scraper` (3u, LLM-training-data buyer intent, flat $0.03 + $0.01 start, dearer everywhere).

  **Verified, not assumed.** `git diff --stat` on the README edit: 1 file, +2 lines only (1 new dated paragraph before `## FAQ`, no reformat). `apify push --force -w 600` -> build **0.1.102 SUCCEEDED**; confirmed live via `taggedBuilds.latest.buildId` matching the push log's Build ID (not just trusting the log). `check-price-superiority` re-run fleet-wide: **2738 named-rival prices checked, 0 undisclosed anywhere**, no new flag on this Actor (unrelated pre-existing UNIT-MISMATCH/GONE/RUNFEE advisories on other Actors, none new). Hand-updated `state/audit_dates.json`'s `substack-scraper.competitor_audit` (2800 -> 3139) via a surgical Python string-replace (never `json.load`/`json.dump`, per the c3129 reformat-hazard lesson) -- `git diff --stat` confirmed exactly 2 lines changed, JSON re-parsed clean. Full 15-handle dataset persisted to `state/audit_data/c3139_substack_prices.json` (the batch script's own `persist_sweep`, not a manual save). `audit-due --type competitor_audit` re-run: **NONE DUE anywhere in the fleet** -- this was the last item in the backlog, soonest next is `hacker-news-scraper` in 1 cycle (its own independent per-Actor cadence, not a backlog item).

  **Blockers: none. Owner email: none owed.** $0 spend -- one Actor build (README-only, no code change), pricing sweep is 15 read-only `GET /v2/acts` calls. Services/site re-verified 200 post-work (`/tools/substack-scraper` -- not `/actors/substack-scraper`, which 404s; the site's URL pattern is `/tools/<slug>`). **`tasks/queue.md` is now badly TRIM DUE: 178.3KB, 10 live `CLOSED c3`/`PROGRESS c3` blocks (this entry makes it 10) against the floor of 5** -- carried forward from c3135/c3138 without a rotation in between; next QUALITY slot (**c3141**, 3141 % 3 == 0) should make this its first priority: count live blocks fresh, hazard-grep before cutting (RULE 1/8), check RULE 4, then archive the oldest contiguous range. No GROWTH-shaped `competitor_audit` backlog remains fleet-wide as of this cycle -- next GROWTH slot should pick a different lever (re-run `bin/widened-candidates` fresh, or check `audit-due --all` for a newly-due one-off axis).

- [ ] **CLOSED c3136 -- Regular/BUILD slot (3136 % 3 == 1, recomputed by hand). Preflight re-run fresh:** `inbox list 10` same routine noise as c3135 -- zero actionable mail, no owner email owed. `bin/revenue` unchanged ($0 booked, 27 public Actors, 54 users, 1459 runs30d, 0 bookmarks, 0 reviews). `checks-due --all` **DUE NOW (1): `devto-post`** -- taken as the cycle's work (its cadence is externally dated and cannot slip without breaking the 2-day publish beat). Services active, site 200 on `/` and `/tools`; c3135's commit `796ffa84` confirmed landed, tree clean at start.
  **Work -- `devto-post` (article 33), CLOSED. The c2656 re-measure-before-republishing rule paid for itself twice over: 2 of the 3 findings in the post being syndicated were FALSE.** Picked `website-screenshot-api-no-key-compared` (2026-11-05) from the 63 unsynced site posts precisely because every claim in it is 3 curls away. Published as dev.to **id 5028684** (tags `webscraping,api,screenshot,devops`; canonical -> `/blog/website-screenshot-api-no-key-compared`; `ai_disclosure_level: fully_autonomous`; `HTTP 201`, article page 200). Findings: **(1) the post's HEADLINE claim was wrong** -- it said mshots is "blocked outright from a hosting IP, every variation 403'd"; live from the same box mshots serves a real **1280x960 JPEG, 88,881 B, HTTP 200, `image/jpeg`**, byte-identical with NO `User-Agent`, with `curl/8.0` and with a Chrome UA. mshots is an **async renderer behind a per-IP rate limiter**, 3 states on one url (`403` 146B nginx Forbidden / `429` 564B nginx Too-Many-Requests + 6 MSIE-padding comments served `text/html` / `200` JPEG); UA, hostname (`s.wordpress.com` vs `s0.wp.com`) and query params were each tested and each produced BOTH codes, so none of them is the axis -- volume + render state is (after ~60 req in 5 min, six never-requested cache-buster urls all 429'd with `x-nc: MISS` while the one rendered url kept serving its cached 200). Its 200 also carried `last-modified` 15.6h old under `max-age=43200`. **(2) thum.io's `fullpage/` no-cache trick is GONE** -- both forms now return `cache-control: max-age=86400` (post claimed `no-cache, no-store, must-revalidate` for `fullpage`). **(3) Controls that HELD byte-identical 8 days on:** thum.io 64,861B PNG 1200x1200 and 58,070B PNG 800x592; microlink 2560x1600 PNG size 168630, `x-rate-limit-limit` 5. The **site post was corrected, not left stale**: dated `> Correction, 2026-11-13` blockquote naming both failed claims + linking the re-measurement, verified rendered live. Verification: dry-run first; authenticated `GET /api/articles/5028684` confirmed canonical + 4 tags + disclosure + **0 relative links in the live body**; 7 outbound links probed (6x200, 1x `/go/` 302); `state/devto_syndicated.json` re-derived whole-file with a LOST-ROW abort check (**32->33 synced, 63->62 unsynced, 0 unmatched, 0 lost, exactly 1 added**); recorded `checks-due --ran devto-post` (3040 -> 3136, next due **c3232**).
  **Blockers: none. Owner email: none owed.** $0 spend -- no Actor build, no paid API, read-only public endpoints only.

- [ ] **CLOSED c3137/c3138 -- Regular/GROWTH slot (3137 % 3 == 2, recomputed by hand). Preflight re-run fresh:** `inbox list 10` same routine noise as c3136 (backlink/guest-post solicitations, a "My Slop" mention, a TinyGate pitch, DMARC reports, the two already-resolved owner Apify-incident emails) -- zero actionable new mail, no owner email owed. `bin/revenue` unchanged ($0 booked, 27 public Actors, 54 users, 1460 runs30d, 0 bookmarks, 0 reviews). `checks-due --all` **NONE DUE** (soonest `check-dead-endpoint-docs` in 2c, c3139). `audit-due --all` confirmed the carried-forward backlog: `competitor_audit` DUE on `steam-reviews-scraper`/`substack-scraper`; took `steam-reviews-scraper` (older gap, already named by c3135/c3136 as next). Services active, site 200 on `/` and `/tools`; `git log --oneline -3` confirmed c3136's commit (`561e03ee`) landed, tree clean apart from `bin/revenue`'s own timestamp writes.

  **Work -- `competitor_audit` on `steam-reviews-scraper`, cycle A of the c3134/c3135 two-cycle shape (prep + full live-pricing sweep). README disclosure write-up NOT done, left as a precise cycle-B task below.** Own price re-verified live FIRST via the Actor's raw `pricingInfos`: tiered **$0.000575 FREE / $0.0005 BRONZE / $0.00039 SILVER / $0.0003 GOLD/PLATINUM/DIAMOND**, no start fee -- **zero drift since c2796** (341 cycles). `bin/niche-size steam-reviews-scraper`: 222 matched (up from 206 at c2796, +16/+7.8% in 341 cycles; tool's own WARNING that several of the 15 search terms are possibly page-capped still applies, so 222 is a floor not a ceiling). `bin/niche-unnamed steam-reviews-scraper`: **123 unnamed of 222** (110 NONE, 13 OWNER) vs c2796's 112 of 206 (99 NONE, 13 OWNER). **STANDING RULE c2812 sign check: matched delta +16, unnamed-cohort delta +11 -- SAME sign, no screen decay.** Priced the **FULL 123-handle cohort** (no user-count cut at all, the STANDING RULE c2812 part-2 preference over any cut, since the whole cohort was $0 / ~1 min / 123 `GET /v2/acts` calls) -- extracted the handle list fresh from this cycle's own `niche-unnamed` output (never reused a stale `/tmp` file, per STANDING RULE c2907/c2796) to `/tmp/c3137_steam_unnamed.txt` (123 lines, exact match to the tool's own banner), then ran `bin/_batch_price_steam2.py /tmp/c3137_steam_unnamed.txt /tmp/c3137_steam_prices.json` with **both args explicit** (never bare -- the c2796/c2907 trap). **123/123 resolved, 0 unresolvable.**

  **Findings, all at 1-2 users (same pattern as c2796 -- every undercutter here has no buyers):** 3 `every_tier_below_floor` genuine threats by the pricer's own classification -- `wulfcare/steam-reviews-scraper` (2u, tiered $0.0001 FREE -> $0.00008 GOLD+, no start fee, a real review-scraper scope match, our deepest tier is $0.0003 so this undercuts at every rung); `trusted_tech_spot/steam-games-reviews-deals-scraper` (2u, no `pricingInfos` at all -> $0, review-sentiment is one of several features); `recordsdata/steam-games-player-stats` (1u, Apify FREE model, reviews are one of several features alongside price/genres/achievements/player-count). 1 partial (`hyperbach/steam-reviews-scraper`, 2u, genuine review-scraper scope match, undercuts only GOLD/PLATINUM/DIAMOND at $0.000287 but carries a **$0.003 start fee** we don't charge). 1 AMBIGUOUS needing hand judgment (`bepolabs/steam`, 2u, two recurring events with no primary flag: `game` $0.00116 vs `review` $0.00029 -- its own description sells itself as a general game-metadata-plus-feedback scraper, not review-focused, so whether `review` is the comparable per-row unit is a real judgment call, not automatable; if it is, $0.00029 < our $0.0003 floor by a hair). 1 flagged `runfee` (`loving_lovecraft/game-streamer-finder`, $0.50005/run) that on reading its description is **NOT a review/data scraper at all** -- it's a YouTube-creator-finder for a Steam game, almost certainly a false match off a generic niche term, so cycle B should **EXCLUDE it entirely, not disclose it as a competitor**. Full 123-row dataset (desc, title, users, tiers, events, runfee, every/any-below-floor flags) persisted to **`state/audit_data/c3137_steam_prices.json`** via `_unit_price.persist_sweep` -- cycle B should load this directly, no re-fetch needed.

  **Cycle B (precise next-cycle task): read `wulfcare`/`hyperbach`/`trusted_tech_spot`/`recordsdata`'s `desc` fields from the persisted JSON (already fetched, don't re-type from titles), write README disclosure paragraphs naming `wulfcare` (every-tier undercutter) and `hyperbach` (partial, GOLD+ only, start-fee caveat) as genuine substitutes, one summarizing sentence for `trusted_tech_spot`/`recordsdata` as broader-scope FREE-model listings named for completeness, resolve `bepolabs`'s ambiguity by hand (read its own listing page/input schema if the two-event split still isn't clear) and disclose only if `review` really is its comparable unit, explicitly do NOT touch/disclose `loving_lovecraft` (out of scope). Then `apify push --force`, fleet-wide `check-price-superiority` re-run (confirm 0 undisclosed, no new flag on this Actor), hand-update `state/audit_dates.json`'s `steam-reviews-scraper.competitor_audit` (2796 -> shipping cycle) with a 2-line surgical diff per the c3129 lesson (never a full `json.dump` reformat). Do NOT mark it done before the README edit actually ships. `substack-scraper`'s `competitor_audit` (last 2800, now due) is still fully untouched after that -- next in the backlog once steam-reviews-scraper's disclosure ships. Already-named leaders in this niche (`automation-lab` 135u, `easyapi` 64u, `logiover` 62u, `memo23` 57u, `danek` 55u, `shahidirfan` 47u) were correctly excluded from this cohort by `niche-unnamed` (already disclosed) and not re-examined -- their README-prose user counts may have drifted since c2797's last refresh; a quick live re-check while in the file during cycle B would be cheap but is not required.

  **Cycle B (c3138, QUALITY slot, took this precisely-specified GROWTH-finishing task over the queue.md rotation per the c3134/c3135 precedent), CLOSED.** Wrote the README disclosure exactly per the handoff above: named `wulfcare/steam-reviews-scraper` (every-tier undercutter) and `hyperbach/steam-reviews-scraper` (partial -- ties FREE/SILVER, real threat only on GOLD/PLATINUM/DIAMOND past ~231 rows/run once its $0.003 start fee is amortized, below that our no-start-fee pricing wins even there); disclosed `recordsdata/steam-games-player-stats` (FREE-model, up to 100 reviews/game bundled into a wider tool) for completeness; excluded `trusted_tech_spot/steam-games-reviews-deals-scraper` on scope (its own description promises a sentiment *score*, not review text -- same exclusion class as `glasswing`/`fortuitous_pirate` above); resolved `bepolabs/steam`'s ambiguity by reading its own title ("game prices, details and Steam reviews" names reviews as a co-equal third deliverable, not a side attachment) and disclosed it as a GOLD+-only undercutter at $0.00029 vs our $0.0003; left `loving_lovecraft/game-streamer-finder` untouched and out of scope as instructed. `git diff --stat`: 1 file, 6 lines, README only (plus `state/revenue.json`'s own preflight timestamp writes). `apify push --force -w 600` -> build **0.1.106 SUCCEEDED**, confirmed live via `taggedBuilds.latest.buildId` match (not just the push log). `check-price-superiority` re-run fleet-wide: **2727 named-rival prices checked, 0 undisclosed anywhere**, no new flag on this Actor. Hand-updated `state/audit_dates.json`'s `steam-reviews-scraper.competitor_audit` (2796 -> 3138) via a surgical Python string-replace (never `json.load`/`json.dump`, per the c3129 reformat-hazard lesson) -- `python3 -c "json.load(...)"` re-confirmed valid, `git diff --stat` confirmed exactly 2 lines changed. `audit-due --all` re-run: `substack-scraper` (last audited c2305, now the oldest gap in this backlog type by far) is the sole remaining `competitor_audit` item. **Blockers: none. Owner email: none owed.** $0 spend -- one Actor build, no billable runs. Services/site re-verified 200 post-work. **queue.md is still TRIM DUE** (carried forward from c3135, 160.6KB/7 live blocks there) -- next QUALITY slot or any cycle with a free time box should run the newest-5 rotation before it grows further; this cycle deliberately didn't, same precedent as c3135 choosing the GROWTH-finishing task over its own slot's maintenance task.

  **Blockers: none. Owner email: none owed.** $0 spend -- 123+1 read-only `GET /v2/acts` calls, no Actor runs, no builds. Services/site re-verified 200 post-work.

- [ ] **NEW c3136 (TRIVIAL/method -- cost ~8 minutes this cycle, will cost the same again).** On a rate-limited or async HTTP endpoint, **`curl -D -` and `curl -s -w "%{http_code}"` are two SEPARATE REQUESTS and will disagree with each other.** c3136 spent ~8 minutes deriving a confident, completely false rule ("a browser `User-Agent` turns mshots' 403 into a 429", then "query params do it", then "it alternates per url") purely because the header dump and the status-code probe were different calls landing in different states of the same endpoint -- and each wrong rule reproduced 3-5 times in a tight loop, because the state was sticky for ~30-60s. **Rule: when characterising an endpoint that might be stateful, capture status + content-type + size + headers + body magic bytes in ONE call** (`curl -s -D /tmp/h -o /tmp/b -w "%{http_code}|%{content_type}|%{size_download}"`, then read `/tmp/h` and `xxd -p -l 4 /tmp/b`) before forming any hypothesis. The tell that something was wrong: a "429" that reported `content_type: text/html` at 564 B in one call and `200 image/jpeg` at 564 B in another -- two different statuses on the same byte count is never a real rule, it is two requests.

- [ ] **NEW c3136 (LOW/content, a reusable angle rather than a defect).** The strongest dev.to article this channel has produced was not new research -- it was **re-measuring our own 8-day-old post and publishing the two ways it had gone wrong**. That shape is repeatable and cheap (3 curls), it is honest in a way the channel rewards, and it doubles as maintenance of the site post. **62 unsynced site posts remain**, and the ones whose claims are a handful of unauthenticated HTTP calls are the best syndication candidates for exactly this reason -- prefer them over posts whose claims need an Actor run to re-verify. Standing durable lesson from this one (already in LEARNINGS): **a keyless endpoint's REFUSAL is not a stable property of your IP.** A single measurement of a `403` is worth far less than the same measurement of a `200`, so never generalise a point-in-time refusal into "this endpoint blocks cloud IPs" -- re-hit it a day later before writing that sentence anywhere buyer-facing.

- [ ] **NEW c3116 (MEDIUM, the live GROWTH-slot default -- supersedes c3115's `api`-only framing of the same backlog; do NOT re-run the narrow scan).** The RULE 6b sub-phrase lever (c3112 found it, c3115 generalised it fleet-wide) was framed too narrowly: both cycles generated candidates only as *the 2-gram prefix of a tracked 3-gram ending in `api`*. c3116 widened it to **any tracked 3-gram-or-longer whose FIRST or LAST word is a generic head** -- the head set that measured well is `api, data, database, databases, reports, projects, research, feed, json, search, monitoring, tracking, alerts, scraper` -- taking both the prefix (drop the trailing head) and the suffix (drop the leading head). On `nih-reporter-scraper` that turned 7 candidates into 16 and **9 of the 13 keepers came from the widened part**, so c3115's per-Actor counts are a FLOOR on the payout, not its size. Fleet-wide the widened generator finds **211 candidates across 26 Actors** (point-in-time; re-derive, don't trust the number). **Named next pick: `us-federal-awards-scraper` (24, the largest).** Then `clinicaltrials-scraper` 14, `google-play-reviews-scraper`/`fec-campaign-finance-scraper`/`ats-jobs-scraper` 12 each. **Follow METHOD c3084 unchanged** -- health-gate, live-vs-local `meta.json` identity, ONE batch `store-price`, read `live` and apply the top-60 cutoff yourself, 3-5 `--why` spot-checks (highest-nbHits keeper / anything in the p50-65 FLAPPING band / one screen-out), then an append-only TERMS edit with a dated provenance comment carrying BOTH the keepers' (nbHits, rank, attr) and the screened-out list with reasons. **Two cautions earned c3116:** (i) a widened candidate is NOT automatically better than the longer term it came from -- `funding data` (live 68) is worse than its own tracked `funding data api`, so the cutoff must still be applied per-term and the screen-outs still recorded; (ii) the generator produces near-duplicates that are separately-ranked real queries (`grant data` p46 and `grants data` p46; `grant database` p11 and `grants database` p11) -- price both, do not dedupe singular/plural by hand.

- [ ] **NEW c3108 (TRIVIAL/method, earned the cheap way -- 30 seconds of prevention).** Editing a buyer-facing `.actor/input_schema.json` by round-tripping it through `json.dumps(indent=N)` reformats the WHOLE file for a one-line content change: c3108's first attempt turned a 1-line prose fix into `164 insertions / 136 deletions` (this fleet hand-formats these files at 2-space indent with inline `items` objects, which no serialiser reproduces). Caught by reading `git diff --stat` before pushing, reverted, redone as a surgical replace against the RAW escaped text (`\"Global newest-first\"`, note the backslashes) for a `1 insertion / 1 deletion` diff. **Rule: never serialise a hand-formatted `.actor/*.json`; string-replace it, and `git diff --stat` every schema edit before `apify push`.** A whole-file reformat would also have made the live-vs-local byte-identity check pass while burying the real change, so the usual verification would NOT have caught it.

- [ ] **NEW note c3104 (LOW, checker precision -- bias is SAFE, do NOT rush, and do NOT "fix" it before reading the second paragraph).** `bin/_unit_price.py`'s `is_start_fee(key, ev)` does **not** classify `lanternlab318/hacker-news`'s `run-start` event ($0.0005) as a start fee -- c3104's rung-for-rung re-verification printed it as `[per-row]`. The listing's own README and the event title describe a once-per-run charge, and the sibling listings this cycle re-priced show the two shapes the helper DOES catch: Apify's canonical `apify-actor-start` key (`plotpointtech`, `tidelane`, `informed_almandine_vzb`) and a custom key carrying `isOneTimeEvent: true` (`rowfeed`'s `apify-actor-start`). `lanternlab318` uses a custom key (`run-start`) **without** the `isOneTimeEvent` flag, which is the one combination that falls through.

  **The bias is safe and that is why this is LOW.** Read as a per-ROW rate, a $0.0005 run fee looks 2.5x DEARER than our $0.0002 Free rung, so the mistake can only ever make a rival look more expensive than it is -- it cannot hide an undercutter, which is the failure direction that matters. It also did not affect c3104's write-up: `lanternlab318`'s Free+Bronze undercut verdict comes from its separate `story` event ($0.000149), which is correctly classified. **If picked up, do not widen `is_start_fee` on the key name alone** (`run-start`, `start`, `run` as substrings will collide with legitimate per-row event names like `job-post`/`search-term` in neighbouring niches); the honest fix is the `runfee_price` path in `check-price-superiority` (which already reasons about run-scoped events as a SET) plus a hand-read list, the same shape c2466 chose for the ambiguous multi-event bucket. Worth noting the detection cost was ~0: it surfaced only because c3104 printed the start-fee classification per event instead of trusting the resolved unit price.

- [ ] **NEW c3103 -- closed the dedicated `hacker-news-scraper` resweep c3102 left as the last backlog item; `check-competitor-claims` is now 0 undated/stale fleet-wide.** Root cause of the 2 flagged paragraphs (README.md:165/175, "last verified 2026-09-26, 47d") was NOT niche staleness -- it was a paragraph-join artifact: `check-competitor-claims` chunks by blank-line-separated markdown paragraphs, and the 14th/15th sweep write-ups (unlike the 11th-13th, which keep intro+bullets+`Verified live <date>` in one block) split their own `Verified live 2026-10-23`/`2026-10-30` sentence into a separate bullet-list paragraph below the intro, so the intro paragraph's only in-block date was the much older "our price unchanged since 2026-09-26" clause. Per the standing "not just a date bump" rule, did NOT just stamp today's date on those 2 paragraphs -- confirmed their already-true sweep dates (2026-10-23, 2026-10-30) from the adjacent bullet paragraphs that cite them and appended those exact, already-documented dates to the intro sentences instead (zero new claims, just completing an existing record) -- **and separately ran a genuine new resweep** (own price re-verified unchanged live; Store search re-swept 762 seen/498 matched/377 unnamed, up from the 16th sweep's 708/469/351; all 322 no-owner-mention listings live-priced rung-for-rung via `bin/_batch_price_hn3.py`) to produce a real **Seventeenth sweep** section rather than relying on the join-fix alone. Findings: 3 new genuine $0 substitutes (`extas_corp/hackernews-scraper` -- broadest-scoped FREE listing found in this niche yet; `exuberantal/hackernews-showhn-launches-scraper`; `adaptive_labs/hacker-news-launches-monitor`), running $0 count 27/26 -> 30/29; 1 new partial undercutter with broad scope (`tidelane/hacker-news`, cheaper at Free/Bronze/Silver, dearer Gold+); 4 Free-and-Bronze-only flat-rate undercutters (`rowfeed`, `lanternlab318`, `topapi`, `informed_almandine_vzb` -- the last one a $0.00001-Free/$0.001-paid-tier shape, Apify's unconfigured-paid-tier default rather than a real ladder); 2 ambiguous multi-event listings (`flets_sv`, `datasetworks`) resolved as dearer-either-way without needing the primary-event flag, so no listing had to be dropped from the count. Re-run `check-competitor-claims --only hacker-news-scraper`: **0 undated/stale (was 2), 66 user-count claims checked (was 56), 0 stale/disagreement.** Pushed (`apify push --force -w 600`, build 0.1.108) and verified byte-identical live via the build API (95044 chars, exact match). Post-push `check-readme-samples`/`check-comparison-breadth`/`check-own-price-freshness` all clean fleet-wide. ~$0 spend (README-only push, no PPE run). **Follow-up filed, not done this cycle (scope creep risk, time-boxed out) -- DONE c3104, see `CLOSED c3104` at the top of this file (build 0.1.109, tallies now 30 found/29 live, undercutter list extended through the 17th sweep, all 9 asserted handles re-verified live rung-for-rung; do not re-do it):** the Actor's closing "What we do not claim" rollup paragraph still cites the 2026-10-30 sweep's $0/undercutter tallies verbatim and was never updated after the 16th OR 17th sweep -- next cycle touching this README should refresh that paragraph's running counts to match the 17th sweep's 30/29 and the new undercutter list, same convention as every other sweep's own paragraph.
- [ ] **NEW c3100 -- two real content findings fell out of the c3100 claim refresh; both are now fixed in the pushed READMEs, recorded here because the CLASS will recur in the 5 remaining files.** (1) **A supporting usage figure can rot much harder than the user count next to it, and only the user count is checked.** `unfenced-group/google-play-store-scraper` was cited in `google-play-reviews-scraper` from 2026-10-05 onward as '3 users but 153 successful runs in the last 30 days' -- the whole point of the sentence being that a low user count was hiding real usage. Live 2026-11-12: 6 users and **1** successful run in 30d (`stats.publicActorRunStats30Days.SUCCEEDED`). `check-competitor-claims` flagged only the 3->6, because run counts are not a claim class it reads; the retraction of the much louder 153 came from reading the sentence. Its PRICE was re-verified live and is unchanged (flat $0.00005/review at all six tiers, $0.00069/app row on FREE), so the undercutter claim itself stands and was kept. **When fixing a flagged count, re-fetch the OTHER live figures in the same sentence too** -- runs30d, users30d, delisted-ness. Same class caught `code-node-tools` '101 in the last 30 days' -> 109 (`totalUsers30Days`, not runs -- check which field a '30 days' figure actually means). (2) **Two different Actors each held an unqualified 'fastest-growing in the niche' superlative in the same README** (`apple-podcasts-scraper` lines 179/181: `logiover` and `ryanclinton`). Live they are fastest-growing on DIFFERENT measures -- logiover by rate (20 new users in 30d on a base of 78, ~26%), ryanclinton by absolute new users (28 on 221, ~13%) -- so both are now qualified by measure rather than stated bare. No checker covers 'two bare superlatives of the same kind in one file'; it surfaced only because `check-competitor-claims`' superlative GUARD forced a human read of those paragraphs, which is the guard working as designed. **Possible cheap follow-up: a `check-dup-superlative` that flags the same superlative phrase asserted of 2+ different handles in one file.** Not built this cycle.
- [ ] **NEW c3088 (LOW/scheduled, NOT a defect -- do this on a BUILD slot, not a doc slot).** `check-schema-claims` ran CLEAN this cycle (0 STALE) but reported **5 AGING measurement claims** in buyer-facing `.actor/input_schema.json` prose, which the checker defines as "go re-measure", never "this is wrong": (a) `remote-jobs-scraper.properties.resultOrder.description`, measured 2026-10-18, 25d old, **crosses the 30d STALE line ~2026-11-17**; (b-e) four `steam-reviews-scraper` claims -- `purchaseType`, `includeOffTopic`, `sortBy`, `dayRange` -- all anchored to the same `2026-10-23 source change`, 20d old, STALE ~2026-11-22. **Why this is not a doc edit:** each claim is a count/behaviour of a LIVE external source, so honouring it means an actual Actor run to re-measure plus an `apify push` to update the prose -- a build-slot task with a small real cost, which is exactly why no doc-only cycle should touch it. **Do NOT "fix" these by rewriting the prose to dodge the checker** -- c2609 and c2611 both burned an `apify push` doing that and the checker's HISTORY-clause rule (c2612) exists specifically to make keeping the old number next to a fresh one the cheap, honest option: re-measure, then write `first measured <old> on <old-date>, re-verified live <new-date> at <new>`. The 4 steam-reviews claims share one anchor, so one re-measure run plus one push settles all four. Checker next due c3568, so nothing will re-flag these automatically before then -- this item is the only reminder.

- [x] **DECIDED c3081 -- DEFER, no `meta.json` edit. Do not re-open without one of the two triggers named below.** Read `meta.json`, the `watchLabel` README row, and the full FAQ/Pricing sections before deciding (`actors/trademark-search-scraper/README.md` lines 20, 78-82, 106-111, 131, 135, 139). Four reasons the reprice loses on balance, not one: (1) **the live README already states the zero-charge behaviour as an unconditional per-run promise**, not just a first-run baseline -- line 20 ("every later run on the same label + search returns and charges only marks not already delivered") and line 131 ("watch-mode baseline runs return and charge nothing") -- a new `watch-check` fee charged on a quiet run contradicts live buyer-facing text on our ONLY page-1 listing, not a doc nobody reads. (2) **This is already our stated differentiator against the exact two rivals cited as the reason to reprice**: README line 139 already discloses `nexgendata/uspto-trademark-search` and `nexgendata/euipo-esearch-trademarks` charge $0.05/watch-check (25-50x ours) and line 135 says plainly "Our `watchLabel` mode charges only the $0.002 row rate, and only on marks you have not already been given" -- the gap `NEW c3080` found is not an unmarketed gap, it is an already-marketed asymmetry; repricing would delete the very thing being advertised. (3) **Zero signal there is any revenue to capture**: 0 bookmarks, 0 reviews, $0 booked on this Actor -- we do not know a single real buyer runs `watchLabel` at all, let alone on a schedule frequent enough for the $0 compute exposure to matter. (4) **The exposure being guarded against is small by construction**: a no-change watch run is one HTTP-only TMview page fetch plus a KVS baseline read/write, not a browser session -- sub-cent ACTOR_COMPUTE_UNITS cost (see `bin/apify-spend`'s per-service breakdown), nothing like the data-transfer or proxy cost a result-heavy run carries. **Re-open only if either:** (a) real buyer signal appears on this Actor specifically (a bookmark, a review, or a booked-revenue event tied to it), making the upside non-speculative; or (b) a future `bin/usage-trend`-style check shows sustained high-volume scheduled `watchLabel` runs at zero rows, showing the compute exposure is no longer trivial. Neither test re-run (`check-price-superiority`, `check-unit-matched-price`) was needed since no price changed. $0 spent, no build, no push. Full prior research (rival prices, the tension, the suggested shape if ever shipped) stays below, superseded but kept for context on re-open.
  **Why this Actor and not another:** c3080's `store-anon-rank` run put it at **#8 of 249** (5 users, runs30d 636) -- our only top-10 rank on any buyer query, vs #29-#501 for all 26 others. It is the one listing that actually gets buyer impressions, so it is the only one where conversion/monetization work can pay (see LEARNINGS c3080).
  **The gap (verified, not assumed):** we ALREADY ship watch mode -- `watchLabel` / `watchChanges` / `webhookUrl`, documented in `actors/trademark-search-scraper/README.md` lines 20-22, with `_watchChangeType`/`_watchPrevious` change fields. But `meta.json` prices exactly ONE event: `result` @ $0.002 ("Result item"). So a scheduled watch run that finds nothing new returns 0 rows and bills **$0** while still costing us compute + dataset/KVS writes. Rivals price exactly this event: **#1 `nexgendata/uspto-trademark-search` `watch-check` @ $0.05**, **#9 `nexgendata/euipo-esearch-trademarks` `watch-check` @ $0.05**, #4 `trev0n/tmview-scraper` `trademark-details` @ $0.002 (plus a $0.005 `apify-actor-start` on #1/#3/#4/#7/#9, which we do not charge at all).
  **The tension that makes this a DECIDE, not a do:** (a) our published README promises "the first run under a label seeds a baseline (0 rows returned, **0 charged**)" -- adding a charge silently contradicts live buyer-facing docs and must be a doc change too; (b) "From $0.002/result, no start fee" in `meta.json`'s description is our stated differentiator and we are **the cheapest in the whole top 9** (#1/#9 charge $0.05/record, #3 $0.007+$0.005 start) -- check `check-price-superiority` / `check-unit-matched-price` before touching it; (c) 0 bookmarks / 0 reviews / $0 booked means there may be no watch-mode users to monetize yet, so the upside is speculative while the positioning loss is real.
  **Suggested shape if it goes ahead:** a small `watch-check` event (well under the rivals' $0.05 -- we undercut on purpose) charged ONLY on a run with `watchLabel` set that returns 0 new rows, leaving plain searches at $0.002/result with no start fee and the "no start fee" claim intact. Update README lines 20-22 and the FAQ in the same commit. Re-run `actor-health` + the default-input gate after `apify push`.

- [x] **CLOSED c3105 -- split COMPLETE, all 3 slices shipped (c3087/c3090/c3105).** (original text follows)
**NEW c3084 (HIGH, structural -- the doc-trim cadence can no longer clear `tasks/queue.md`, and no amount of running it harder will fix that. Take this on a QUALITY slot INSTEAD of a routine trim.)** c3084 ran both available levers in one slot (newest-5 rotation of five blocks at once + an 11KB compression of the largest line) and still landed at **160.8KB / `TRIM DUE` with ~7c headroom**. The arithmetic is now unarguable: the checker wants post-trim size under ~70KB to clear its own 24c look interval, and **the live content floor is ~160KB**, so the gap is not a trim backlog, it is the file's composition. **Measured c3084, this is the lever:** of 88 live items / 160.8KB, only **4 items (7.2KB) are actionable `NEW cNNNN` tasks**. The other 84 are reference material filed in a task queue -- 22 `NEW follow-up` (30.0KB), 12 `NEW note` (9.6KB), 8 `NEW standing` (14.4KB), 5 `NEW watch` (5.5KB), 2 `NEW tripwire` (2.4KB), plus the CLOSED/COMPRESSED/MERGED/RETIRED/SHIPPED/DECIDED/RESOLVED closed records (~58KB). **Proposed split, which attacks the growth RATE the way STANDING RULE 6 intended rather than re-cutting the stock:** move the standing rules / tripwires / watches / method records to a `notes/STANDING.md` (read on demand, not every cycle) and leave `queue.md` as an actual prioritized queue of open tasks plus the newest-5 cycle blocks. That plausibly takes queue.md under 70KB in one slot and keeps it there, because the recurring per-cycle growth is cycle blocks (rotated) and new follow-ups (which would land in notes). **Do NOT start this without budgeting a full QUALITY slot** -- it is a hazard-grep-heavy move (every cross-item `see NEW cNNNN` pointer has to be re-aimed at the new file, and STANDING RULE 1 says grep first, then cut), and the `STANDING RULES` section in the doc-trim item plus the guarded `c2478` (live 2026-11-15 deadline) and `c2336` (live triage tripwire) must stay reachable. **Interim rule for any QUALITY slot that does a routine trim before this lands: COUNT the live cycle blocks rather than assuming the floor held** -- c3084 found ten, double the floor, because rotating one block per QUALITY slot does not keep up with one block added per cycle, and the drift is invisible unless counted.

**PROGRESS c3087: first slice of the split shipped.** Created `notes/STANDING.md` and moved the 7 lowest-risk items -- the 5 `NEW watch` + 2 `NEW tripwire` items (~7.9KB) -- verbatim, chosen because a hazard grep over `bin actors site notes state tasks` for each item's cycle-label found zero live functional cross-references (only narrative mentions inside other cycle blocks, which describe history and don't break). Verified lossless by multiset diff (every non-blank line from the pre-edit file is findable in queue.md + STANDING.md + queue_archive.md). Also ran the routine newest-5-floor rotation in the same slot (8 live blocks -> 5, archived `CLOSED c3080`/`c3079`/`c3078` to `queue_archive.md` under `## Archived by cycle 3087`). **Result: 166.2KB -> 155.0KB, still TRIM DUE (6c -> 8c headroom) -- as this item predicted, neither lever alone clears it.**

**PROGRESS c3090: second slice shipped, with a correction to the c3087 plan.** Re-read all 8 `NEW STANDING RULE/NOTE/PREFLIGHT/WATCH` items (the slice c3087 deferred) before moving anything and found **2 of the 8 are every-cycle preflight checks, not read-on-demand reference material** -- `NEW STANDING PREFLIGHT STEP (c3020)` ("add to the cycle-protocol step-1 skim... read the LAST `post-cycle commit:` line") and `NEW STANDING TRIPWIRE (c2336)` ("re-diff `ext_bad30d`... at the start of every cycle") are both things this and every recent cycle's preflight actually does (confirmed: this cycle's own preflight re-diffed `ext_bad30d` and checked the post-cycle commit line). Moving either into `notes/STANDING.md`, which its own header says is explicitly "NOT read every cycle," would silently drop them from the cycle protocol -- the opposite of the split's goal. **So the split is not "8 items minus the guarded c2336," it's 6: `c2336` and `c3020` both stay live in queue.md permanently, not just for this slot.** Hazard-grepped the remaining 6 (`c2952`, `c2904`, `c2812`, `c2792`, `c2688`, `c2664`) for live cross-references over `bin actors site notes state tasks`: all hits were either dead one-off `bin/_trimNNNN*.py` scripts or narrative mentions in `notes/LEARNINGS.md`/`notes/PLAYBOOK.md`/`state/fleet_checks.json`/`state/audit_dates.json` that name the cycle label in a history note, not a `see queue.md item cXXXX` pointer that would go stale -- safe to move. Cut via a self-verifying script (`bin/_trim3090q.py`, dry-run multiset-diff before writing, modeled on `bin/_trim1836.py`/`bin/_trim3048q.py`). **Result: queue.md 164.9KB -> 156.1KB (verified via `check-doc-size` post-edit), STANDING.md 8.8KB -> 17.8KB.** Structural asserts green: both `c3020` and `c2336` still present as top-level `- [ ]` bullets in queue.md, all 6 moved labels present in STANDING.md, none of the 6 still present as a `NEW STANDING` bullet in queue.md. **Still NOT moved** (left for a future QUALITY slot, in increasing order of risk/size): the `METHOD c3084` record (~4KB) and the `STANDING RULES` section inside the doc-trim-cadence item itself -- those carry more cross-references and deserve their own hazard-grep pass. `notes/STANDING.md` is NOT read every cycle; it's referenced from its own header for when a `competitor_audit`/RULE-6b sweep touches an Actor named in one of its items, or when the cycle protocol/queue.md explicitly points there.

**PROGRESS c3105: final slice shipped, split COMPLETE.** Moved the last 2 pieces c3090 deferred -- the `METHOD c3084` record (L62, the RULE 6b SEO method/lessons) and the full `doc-trim cadence` item (L747-878: method + STANDING RULES 1-8) -- to `notes/STANDING.md` via a self-verifying script (`bin/_trim3105q.py`, modeled on `bin/_trim3090q.py`: lossless multiset diff, plus a RULE-7 assert that each cut span contains exactly one top-level `- [ ] ` line, its own head). **Hazard grep first** (`grep -rln` for the two labels/section names over `bin actors site notes state`, excluding dead `bin/_trimNNNNq.py` one-shots): every hit (`bin/store-rank`, `notes/LEARNINGS.md`, `state/STATUS.md`, `state/STATUS_ARCHIVE.md`, `state/fleet_checks.json`) was a narrative mention of the c3084 label in a past cycle's write-up, not a `see queue.md item cXXXX`/file-path pointer -- safe to move, since the label itself is unchanged by the file it lives in. **Result: queue.md 173.7KB -> 148.9KB** (verified via `check-doc-size` post-edit; `TRIM DUE` still shows per the forward-looking 24c projection, 148.9KB -> proj. 276KB, since the checker wants ~70KB headroom and cycle-block growth continues independent of this split -- but the live floor this split was fighting is now gone: the two moved items alone were ~15KB of permanent reference mass that a cycle-block rotation could never touch). **STANDING.md: 18.7KB -> 40.7KB.** Structural asserts green: `NEW (c2478)` and `NEW STANDING TRIPWIRE (c2336)` both still live in queue.md untouched, `METHOD c3084` and `doc-trim cadence` (with `STANDING RULE 8`) both present in STANDING.md, neither still present as a top-level bullet in queue.md. Left a 1-line `NEW note (c3105)` pointer at the end of queue.md so a future trim or RULE 6b sweep knows to read `notes/STANDING.md` first. **`NEW c3084`'s split is now fully executed across all 3 slices -- do not re-open it; any further queue.md size pressure is ordinary cycle-block growth, handled by the routine newest-5 rotation, not a structural problem.**

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

- [ ] **NEW note (c3105, TRIVIAL -- a pointer, not a task).** The RULE 6b SEO method (`METHOD c3084`) and the `doc-trim cadence` item's method + STANDING RULES 1-8 (grep-first, QUALITY-slot-only, re-derive partitions fresh, margin arithmetic, DONE-block rules, the c3048 whole-repo-citation hazard grep) moved to `notes/STANDING.md` this cycle (`NEW c3084`'s split, final slice after c3087/c3090's first two). **Read `notes/STANDING.md` before: (a) any `tasks/queue.md` trim, (b) any RULE 6b SEO sweep.** Both are now read-on-demand, not every-cycle, by design -- that is the point of the split.
