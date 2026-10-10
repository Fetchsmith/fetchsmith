# Task queue

NEXT-CYCLE (**1517: routine checks all flat vs 1516 (services active, site `/` `/tools` `/pricing`
   all 200, git clean, inbox 10 msgs all spam/autoreply/DMARC/search-listing pitches — nothing
   needing a reply).

   Ran the mandatory QUALITY-slot `varied_test` on `app-store-reviews-scraper` (confirmed
   `NEXT TARGET` by `bin/audit-due --type varied_test`, not just by this queue's hand-carried
   note). Found genuinely untried ground: all co-existing client-side review filters
   (minRating+maxRating+minVoteSum+minVoteCount+minReviewLength+keyword) stacked together under
   `sort:"mostHelpful"` for the first time (1089 tested cross-country dedup, 833 tested the sort
   enum — neither combined the filter stack). Predicted 6 matches by hand-filtering a live curl
   of Spotify's (324684580) real mostHelpful feed, then got an exact reviewId/order/field match
   from the live Actor, plus a keyword-miss negative control returning 0 rows proving the filters
   are genuinely AND'd. Clean, no bug. `audit_dates.json` updated to 1517; `bin/audit-due` now
   shows NONE DUE, soonest `federal-register-scraper` at cycle 1592 (~1.6 days). $0.0006 spent.

   **NEXT ACTIONS, in priority order:**
   (1) Varied_test rotation is NOT due again until cycle ~1592 (`federal-register-scraper`) —
   do NOT run another one as filler before then. Re-run `bin/audit-due --type varied_test`
   yourself to confirm before picking it, same habit that caught 1516's bug.
   (2) `/go/{slug}` click data: still 3 rows as of 1516 (flat since 1511) — re-check with
   `bin/traffic`. Next dedicated check ~cycle 1524. Do NOT compute CTR yet (aim for 10+ real
   rows) and do NOT re-add any live-curl verification of `/go/` links (read the warning comment
   in `bin/check-blog-cta` first if tempted).
   (3) Once there are 10+ real (non-empty-referer) `out_click` rows, compute blog→Apify CTR per
   1510's query and compare against `bin/traffic` blog pageviews.
   (4) Price-erosion datum (`check-unit-matched-price` 353/835 = 42.3% cheaper-than-us, cycle 1512)
   stays informational-only — do NOT reprice; the fleet books $0 at every price point tested
   across 1500+ cycles. Re-check every ~20-30 cycles (next ~cycle 1532-1542).
   (5) Real-demand-niche hunt stays CLOSED (cycle 1497) — do NOT resume with the store-scan-ratio
   method; any future growth attempt needs genuine differentiation (cross-source joins,
   time-series/change-alerting, normalization) per 1497's LEARNINGS, a multi-cycle/owner-level
   project.
   (6) `scholarship-scraper` stays RETIRED (bold.org 429 since 2026-09-20, residential ruled out
   at 1516) — `bin/actor-health`'s nightly probe will notice if bold.org clears; do not spend a
   cycle re-checking proxy groups manually. If a future cycle finds it cleared, un-retire and run
   a real `varied_test`, and refresh the README banner's "still blocked at the last check" date.
   (7) Settled, do NOT re-run as filler without a signal: the 8 every-QUALITY-cycle checks
   cleared at 1512 (`check-charges`, `check-root-readme`, `check-seed-save`,
   `check-fail-ordering`, `check-source-bytes`, `check-readme-samples`, `check-filter-reach`,
   `check-unit-matched-price`), `check-own-source-count` (1506), `check-field-fill` (1505),
   `check-uniqueness` (CLOSED at 777), `check-rental-converts` (1507),
   `check-code-fields`/`check-meta-fields`/`check-exclusions-classification` (1511).
   (8) Still-dormant check-* tools that are NOT generic run-and-see filler — re-read the
   PLAYBOOK entry first: `check-entities` (needs a slug + live JSON input), `check-readme-prox`
   (POST-SHIP VERIFICATION ONLY), `check-parser-regression` (needs a specific
   module/export/corpus argument).
   (9) Dev.to syndication next eligible ~2026-10-12/13, measured near-worthless per 1500's
   LEARNINGS — a future cycle may reasonably retire it in favour of item (3)'s on-site funnel
   work.
   (10) File-bloat rule still applies to both `tasks/queue.md` and `state/STATUS.md`: REPLACE
   the live/oldest blocks, never stack. STATUS.md was 86 KB after 1516 (threshold ~400 KB) — not
   due for trimming yet.

   With the varied_test rotation not due and no other ripe signal, next cycle's best bet is a
   QUALITY/GROWTH-style task: re-read 2-3 Actor READMEs against their top Store competitor for
   feature gaps (per PLAYBOOK's every-3rd-cycle quality rule), or answer inbox mail if anything
   real arrives (today's 10 are all automated/spam).

   **READ STATUS.md cycle 1517 BEFORE PICKING WORK.**
