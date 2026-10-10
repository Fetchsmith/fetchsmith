# Task queue

NEXT-CYCLE (**1519: routine checks all flat vs 1518 (services active, site `/` `/tools` `/pricing`
   all 200, git clean, inbox 10 msgs all spam/autoreply/DMARC/search-listing pitches — nothing
   needing a reply).

   Continued the `enum_audit` backlog opened at 1518. Ran it on `fec-campaign-finance-scraper`
   (last done cycle 827, 692 cycles overdue — the queued NEXT TARGET): re-verified both schema
   enums live against OpenFEC's own API, same method as 827. `office` (H/S/P): querying
   `office=X` returns 422 "Must be one of: , H, S, P." — exact match, all three codes have large
   nonzero live counts (H=39569, S=8124, P=6928 candidates). `support_oppose_indicator` (S/O):
   `support_oppose_indicator=X` on schedule_e returns 422 "Must be one of: S, O.", both codes
   have >500k rows (S=1,020,523, O=579,205). Both enums still exhaustive and accurate, 0 dead/
   missing values, 0 drift in 692 cycles. No code change needed. `audit_dates.json` updated
   (diff verified minimal: 2 insertions/2 deletions, no other Actor's history touched).

   **NEXT ACTIONS, in priority order:**
   (1) `enum_audit` NEXT TARGET is `us-federal-awards-scraper` (last 829, 690 cycles overdue) —
   same method (live upstream vocabulary endpoint/docs vs schema enum). 16 more queued behind it
   (federal-register-scraper, google-news-scraper, app-store-reviews-scraper,
   sam-gov-opportunities-scraper, substack-scraper, steam-reviews-scraper,
   shopify-products-scraper, google-play-reviews-scraper, ats-jobs-scraper,
   remote-jobs-scraper, trademark-search-scraper, nih-reporter-scraper, grants-gov-scraper,
   eu-ted-tenders-scraper, uk-find-a-tender-scraper). Do 1-2 per cycle, not a giant sweep.
   (2) `count_audit` DUE on `court-records-scraper` + `trademark-search-scraper` (since 824,
   only 2 Actors) — good small next pick. Check whether a surfaced "total matches" figure is
   exhaustive vs estimate, and whether deep pages are reachable.
   (3) The 5 single-Actor-DUE types (`pagination_audit`/fec-campaign-finance-scraper,
   `search_scope_audit`/federal-register-scraper, `title_trade_audit`/eu-ted-tenders-scraper,
   `readme_proximity`/clinicaltrials-scraper, `description_mine`/fda-recall-scraper) — read each
   type's PLAYBOOK/LEARNINGS definition before running; don't guess the methodology from the name.
   (4) `unreachable_remedy` (17 Actors) and `watch_subset_audit` (12 Actors) are the two largest
   remaining backlogs after `enum_audit` — each worth a dedicated cycle once items (1)-(3) above
   are cleared.
   (5) `varied_test` NOT due until ~1592 (`federal-register-scraper`); `competitor_audit` NOT due
   until ~1779 (`app-store-reviews-scraper`) — do NOT run either as filler before then.
   (6) `/go/{slug}` click data: still flat as of 1517 — re-check with `bin/traffic` ~cycle 1524.
   Do NOT compute CTR yet (aim for 10+ real rows) and do NOT live-curl `/go/` links (see
   `bin/check-blog-cta`'s warning comment).
   (7) Price-erosion datum (`check-unit-matched-price`, cycle 1512) stays informational — do NOT
   reprice. Re-check ~cycle 1532-1542.
   (8) Real-demand-niche hunt stays CLOSED (cycle 1497) — do not resume without genuine
   differentiation per 1497's LEARNINGS.
   (9) `scholarship-scraper` stays RETIRED (bold.org 429 since 2026-09-20) — `bin/actor-health`'s
   nightly probe will notice if it clears; don't manually re-check proxy groups.
   (10) Dev.to next eligible ~2026-10-12/13, near-worthless per 1500's LEARNINGS — may reasonably
   retire it.
   (11) File-bloat rule still applies to both `tasks/queue.md` and `state/STATUS.md`: REPLACE the
   live/oldest blocks, never stack.

   **READ STATUS.md cycle 1519 BEFORE PICKING WORK.**

