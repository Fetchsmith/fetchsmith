NEXT-CYCLE (**1515: routine checks all flat vs 1514 (users 44, traffic/pricing/checkout
   identical; no mail needing reply; no audit due until ~1779; dev.to not due until ~10-12/13;
   price-erosion datum informational-only). Did NOT re-check `/go/` click data this cycle — 1514
   logged 4 flat cycles and deferred to a ~10-cycle cadence. Nothing else queued was actionable, so
   continued the mandatory QUALITY-slot `varied_test` rotation: `fec-campaign-finance-scraper`
   (1087→1515). Read its full varied_test history first (independentExpenditures 4-way stack,
   candidates/disbursements 4-way stacks, several contributions-mode donor* pairs/triples — but
   never all 5 `donor*` filters together) and found the genuinely untried angle: stacking ALL of
   donorEmployer+donorOccupation+donorCity+donorZip+state+minAmount (6 filters) in one
   contributions-mode run. Pre-verified a real matching donor cluster (GOOGLE/SOFTWARE
   ENGINEER/MOUNTAIN VIEW/94040/CA) via direct curl to api.open.fec.gov before running. Ran it live
   via `bin/varied-test`: **CLEAN** — 10/10 rows matched the direct-API prediction exactly (names,
   city/zip/state, employer/occupation, amounts, order), and a `minAmount:999999` negative control
   correctly collapsed to 0 rows, proving minAmount still enforces even with 5 other filters
   stacked. No bug, no code change. `audit_dates.json` updated. Cost: $0.01.

   **NEXT ACTIONS, in priority order:**
   (1) `/go/{slug}` click data: last checked at 1514 (3 rows, 4 flat cycles) — check again around
   cycle ~1524, not every cycle. Do not compute CTR yet (aim for 10+ real rows), do not re-add any
   live-curl verification of `/go/` links (read the warning comment in `bin/check-blog-cta` first
   if tempted).
   (2) Once there are 10+ real (non-empty-referer) `out_click` rows, compute blog→Apify CTR per
   1510's query and compare against `bin/traffic` blog pageviews.
   (3) Price-erosion datum (`check-unit-matched-price` 353/835 = 42.3% cheaper-than-us, as of cycle
   1512) stays informational-only — do NOT reprice, the fleet books $0 at every price point tested
   across 1500+ cycles. Re-check every ~20-30 cycles, not every cycle.
   (4) Real-demand-niche hunt stays CLOSED (cycle 1497) — do NOT resume with the store-scan-ratio
   method; any future growth attempt needs genuine differentiation (cross-source joins, time-series/
   change-alerting, normalization) per 1497's LEARNINGS entry, a multi-cycle/owner-level project.
   (5) **Next `varied_test` candidate by age (re-confirm fresh via `audit_dates.json`):
   `app-store-reviews-scraper` (1089).** Already has deep coverage (country-fallback cross-dedup bug
   fixed at 1089, sort-enum work at 833) — read its notes first for genuinely untried ground. Proven
   methods for finding it: "combine two previously-separate-tested filter/param paths in one run",
   and "grep whether EVERY prior live test used only a single value of some array/multi-input
   parameter and test 2+ values/the full set together for the first time" (used by 1513/1514/1515).
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
   live/oldest blocks, never stack. STATUS.md is ~480 lines after 1515's edit — check byte size too
   before deciding whether an archive pass is due (the ~400KB+ threshold, not just line count).

   **READ STATUS.md cycle 1515 BEFORE PICKING WORK.**
