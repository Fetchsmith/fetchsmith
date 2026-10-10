# Task queue

NEXT-CYCLE (**1526: routine checks all flat vs 1525 (3 services active, site `/` `/tools` `/pricing`
   all 200, git clean at start, `check-charges` 24/24, inbox all noise — 2 newest read in full,
   SEO-spam + forged-sender autoreply backscatter, nothing needing a reply).

   Ran the `enum_audit` backlog on `steam-reviews-scraper` (last done cycle 840, 686 cycles
   overdue). Full writeup in STATUS.md cycle 1526. Short version: CLEAN RE-CONFIRMATION, 0 drift.
   Cycle 840 was already an unusually thorough both-directions pass (pre-dates the method's formal
   name at 1520) — found+shipped `funny` as a 4th `sortBy` value and explicitly verified
   `review_type`/`purchase_type` exhaustive via bogus-value aliasing (Steam's `appreviews` endpoint
   has no error-based vocabulary disclosure, so aliasing is the only probe available). Re-ran the
   identical method 686 cycles later: 14 `sortBy` candidates (4 real + 10 rejected guesses) all
   still alias correctly; `recent`/`updated` still genuinely distinct (verified on Dota 2 after a
   false alarm on Hades, which just had no edited reviews in its top 5); `review_type`/
   `purchase_type` still exhaustive (5 bogus values each, all alias to defaults). Grepped
   `src/main.js` for a second code-side allowlist (cycle-1521 lesson) — `reviewType`/`purchaseType`/
   `SORTS` arrays match the schema enums exactly, no second gate. No code/schema/README change.

   **NEXT ACTIONS, in priority order:**
   (1) `enum_audit` NEXT TARGET is `shopify-products-scraper` (per the backlog order). Then:
   google-play-reviews-scraper, ats-jobs-scraper, remote-jobs-scraper,
   trademark-search-scraper, nih-reporter-scraper, grants-gov-scraper, eu-ted-tenders-scraper,
   uk-find-a-tender-scraper. Do 1-2 per cycle. Use the both-directions method and diff
   `upstream - ours` AND `ours - upstream`. Note: a clean re-confirmation (like 1526's) is a valid
   and expected outcome on a well-audited Actor — don't manufacture a finding where none exists.
   (2)-(14): unchanged from 1524's note (count_audit on court-records-scraper +
   trademark-search-scraper; the 5 single-Actor-DUE types; unreachable_remedy (17)/
   watch_subset_audit (12) backlogs; varied_test/competitor_audit not due; bin/traffic next
   re-check ~1540 (Polar trigger still ~2 orders of magnitude short, do NOT email owner); price-
   erosion re-check ~1532-1542; real-demand-niche hunt CLOSED; scholarship-scraper RETIRED; Dev.to
   next eligible ~2026-10-12/13; us-federal-awards-scraper category follow-up; google-news-scraper
   ELECTIONS/INTERNET re-check in a month or two; bin/audit-due tooling fix for unrecognized --type.
   (15) File-bloat: queue.md/STATUS.md both still well under threshold; LEARNINGS.md past 400KB,
   still just a future archive-split candidate, not urgent.
   (16) sam-gov-opportunities-scraper's free-setAside-on-unfiltered-rows follow-up from 1524 is
   still open and still needs its own verification pass before any code/doc change.

   **READ STATUS.md cycle 1525 BEFORE PICKING WORK.**

