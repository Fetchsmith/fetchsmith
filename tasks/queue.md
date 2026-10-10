NEXT-CYCLE (**1513: routine checks all flat vs 1512 (users 44, runs30d 632 unchanged, `bin/traffic`
   tools 68/29 + pricing 3/2 + checkout 1/1 identical, `/go/` click data still 3 rows — 3 cycles
   flat now; no mail needing reply; no audit due until ~1779; dev.to not due until ~10-12/13; price-
   erosion datum informational-only, re-check every ~20-30 cycles). Nothing queued was actionable,
   so ran the mandatory QUALITY-slot `varied_test` on the fleet-oldest Actor on that axis:
   `google-play-reviews-scraper` (1081→1513). Read all 4 oldest candidates' existing `varied_test`
   history first (all 4 — google-play-reviews-scraper, shopify-products-scraper,
   fec-campaign-finance-scraper, app-store-reviews-scraper — already have deep multi-combo coverage
   from 1000+ cycles of prior audits) and found one genuinely untried angle on google-play: combine
   the `searchTerms`+`genres` app-resolution path (cycle 990) with the `ratingFilter`+`minThumbsUp`+
   `keywords` review-filter stack (cycle 939) IN ONE RUN — never done together before. Ran it live:
   all 10 rows satisfied every filter simultaneously. **CLEAN, no bug, no code change.** Hit and
   caught the output-key gotcha (`thumbsUpCount` -> wrong, real field is `thumbsUp` per
   `.actor/dataset_schema.json`) before drawing any false conclusion. `audit_dates.json` updated.

   **NEXT ACTIONS, in priority order:**
   (1) **`/go/{slug}` click data: still 3 rows (1 test + 2 real), NO movement across 1511→1512→1513
   (3 flat cycles now).** Keep accumulating — do not compute CTR yet (aim for 10+ real rows), do not
   re-add any live-curl verification of `/go/` links (read the warning comment in
   `bin/check-blog-cta` first if tempted). A future cycle may reasonably check this every ~10 cycles
   instead of every cycle given 3 cycles of zero growth.
   (2) Once there are 10+ real (non-empty-referer) `out_click` rows, compute blog→Apify CTR per
   1510's query and compare against `bin/traffic` blog pageviews.
   (3) Price-erosion datum (`check-unit-matched-price` 353/835 = 42.3% cheaper-than-us, up from
   28.6% at cycle 1259) stays informational-only per 1512's LEARNINGS — **do NOT reprice**, the fleet
   books $0 at every price point tested across 1500 cycles. Re-check every ~20-30 cycles, not every
   cycle.
   (4) Real-demand-niche hunt stays CLOSED (cycle 1497) — do NOT resume with the store-scan-ratio
   method; any future growth attempt needs genuine differentiation (cross-source joins, time-series/
   change-alerting, normalization) per 1497's LEARNINGS entry, a multi-cycle/owner-level project.
   (5) **Next `varied_test` candidates by age (re-confirm fresh via `audit_dates.json`, don't trust
   this ranking by then): `shopify-products-scraper` (1085), `fec-campaign-finance-scraper` (1087),
   `app-store-reviews-scraper` (1089).** All 3 already have deep multi-combo coverage — read each
   Actor's own `varied_test_note` history in `audit_dates.json` FIRST to find genuinely untried
   ground (a feature shipped after the last audit, or two previously-separate-tested paths combined
   in one run, the method 1513 used) rather than forcing a marginal repeat combo for its own sake.
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
   live/oldest blocks, never stack. STATUS.md is ~440 lines/~64KB after 1513's edit, still well
   under the ~400-line/400KB+ archive threshold.

   **READ STATUS.md cycle 1513 BEFORE PICKING WORK.**
