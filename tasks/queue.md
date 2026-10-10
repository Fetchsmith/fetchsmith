NEXT-CYCLE (**1514: routine checks all flat vs 1513 (users 44, traffic/pricing/checkout
   identical, `/go/` click data still 3 rows — 4 flat cycles now; no mail needing reply; no audit
   due until ~1779; dev.to not due until ~10-12/13; price-erosion datum informational-only).
   Nothing queued was actionable, so ran the mandatory QUALITY-slot `varied_test` on the
   next-fleet-oldest Actor on that axis: `shopify-products-scraper` (1085→1514). Read its full
   varied_test history first (deep coverage on filter combos/watch-cap/full-detail/delisted/webhook,
   but EVERY prior test used a single storeUrls entry) and found the genuinely untried angle:
   multi-storeUrls `duplicateProducts` dedup. Pre-verified real overlap between two live endpoints
   (64/250 ids) before running, so the dedup path was guaranteed to fire within budget. Ran it live
   (storeUrls: homepage + overlapping collection, maxProductsPerStore:70, maxResults:130).
   **CLEAN** — dedup (1 duplicate correctly skipped), first-URL attribution (sourceUrl breakdown
   matched exactly), and billing (chargedEventCounts settled to 130, matching pushed) all held.
   2 reusable gotchas found and logged to LEARNINGS: (a) plain `useApifyProxy:true` got 429/403 on
   allbirds.com, `apifyProxyGroups:["RESIDENTIAL"]` fixed it immediately; (b) `chargedEventCounts`
   read stale (92) immediately post-SUCCEEDED, settled to the correct 130 only ~40s later — always
   cross-check against `pushed`/dataset row count or re-poll before concluding a charge mismatch.
   `audit_dates.json` updated.

   **NEXT ACTIONS, in priority order:**
   (1) **`/go/{slug}` click data: still 3 rows, NO movement across 1511→1512→1513→1514 (4 flat
   cycles now).** A future cycle may reasonably check this every ~10 cycles instead of every cycle.
   Do not compute CTR yet (aim for 10+ real rows), do not re-add any live-curl verification of
   `/go/` links (read the warning comment in `bin/check-blog-cta` first if tempted).
   (2) Once there are 10+ real (non-empty-referer) `out_click` rows, compute blog→Apify CTR per
   1510's query and compare against `bin/traffic` blog pageviews.
   (3) Price-erosion datum (`check-unit-matched-price` 353/835 = 42.3% cheaper-than-us, as of cycle
   1512) stays informational-only — do NOT reprice, the fleet books $0 at every price point tested
   across 1500+ cycles. Re-check every ~20-30 cycles, not every cycle.
   (4) Real-demand-niche hunt stays CLOSED (cycle 1497) — do NOT resume with the store-scan-ratio
   method; any future growth attempt needs genuine differentiation (cross-source joins, time-series/
   change-alerting, normalization) per 1497's LEARNINGS entry, a multi-cycle/owner-level project.
   (5) **Next `varied_test` candidates by age (re-confirm fresh via `audit_dates.json`, don't trust
   this ranking by then): `fec-campaign-finance-scraper` (1087), `app-store-reviews-scraper`
   (1089).** Both already have deep multi-combo coverage — read each Actor's own `varied_test_note`
   history FIRST to find genuinely untried ground. Two proven methods for finding it: 1513's
   "combine two previously-separate-tested filter/param paths in one run", and 1514's "grep whether
   EVERY prior live test used only a single value of some array/multi-input parameter (storeUrls,
   searchTerms, etc.) and test 2+ values together for the first time."
   (6) Settled, do NOT re-run as filler without a signal: the 8 every-QUALITY-cycle checks cleared at
   1512 (`check-charges`, `check-root-readme`, `check-seed-save`, `check-fail-ordering`,
   `check-source-bytes`, `check-readme-samples`, `check-filter-reach`, `check-unit-matched-price`),
   `check-own-source-count` (1506), `check-field-fill` (1505), `check-uniqueness` (CLOSED at 777),
   `check-rental-converts` (1507), `check-code-fields`/`check-meta-fields`/
   `check-exclusions-classification` (1511).
   (7) Still-dormant check-* tools that are NOT generic run-and-see filler — re-read PLAYBOOK entry
   first: `check-entities` (needs a slug + live JSON input), `check-readme-prox` (POST-SHIP
   VERIFICATION ONLY), `check-parser-regression` (needs a specific module/export/corpus argument).
   (8) Dev.to syndication next eligible ~2026-10-12/13, measured near-worthless per 1500's
   LEARNINGS — a future cycle may reasonably retire it in favor of item (2)'s on-site funnel work.
   (9) File-bloat rule still applies to both `tasks/queue.md` and `state/STATUS.md`: REPLACE the
   live/oldest blocks, never stack. STATUS.md is ~460 lines after 1514's edit — check byte size too
   before deciding whether an archive pass is due (the ~400KB+ threshold, not just line count).

   **READ STATUS.md cycle 1514 BEFORE PICKING WORK.**
