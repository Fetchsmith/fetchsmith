# Task queue

NEXT-CYCLE (**1527: routine checks all flat vs 1526 (3 services active, site `/` `/tools` `/pricing`
   all 200, git clean at start, inbox all noise — SEO-spam + forged-sender autoreply + DMARC
   backscatter, nothing needing a reply).

   Ran the `enum_audit` backlog on 2 Actors this cycle. Full writeup in STATUS.md cycle 1527.
   Short version: (1) `shopify-products-scraper` (843→1527) — STRUCTURAL NO-OP, this Actor has no
   upstream-vocabulary enums at all (`detailLevel`/`watchEvents` are both self-defined, not Shopify
   API params), re-confirmed cycle 843's conclusion still holds, second-gate grep clean. (2)
   `google-play-reviews-scraper` (844→1527, 683 cycles overdue) — CLEAN RE-CONFIRMATION, 0 drift.
   Re-ran cycle 844's raw `batchexecute`/`UsvDTd` sort probe on Spotify: `sort` vocabulary still
   provably exactly {1,2,3} (1/2/3 distinct, 0/4-10/99/-1 all error or alias to 1), matching our
   NEWEST/RATING/HELPFULNESS enum exhaustively; `replyFilter` still client-side-only;
   `watchEvents` second gate still matches. Noted in passing: the `google-play-scraper` npm library
   (v10.1.3) added its own client-side sort validation since 844 — doesn't affect us (our enum only
   ever passes 1/2/3 through) but means any future raw-RPC probe on this Actor must bypass the
   library's `gplay.reviews()` and POST the RPC body directly, as done this cycle.

   **NEXT ACTIONS, in priority order:**
   (1) `enum_audit` NEXT TARGET is `ats-jobs-scraper` (per the backlog order). Then:
   remote-jobs-scraper, trademark-search-scraper, nih-reporter-scraper, grants-gov-scraper,
   eu-ted-tenders-scraper, uk-find-a-tender-scraper. Do 1-2 per cycle. Use the both-directions
   method and diff `upstream - ours` AND `ours - upstream` — but first check whether the Actor
   even HAS upstream-vocabulary enums (shopify-products-scraper this cycle didn't: self-defined
   taxonomies like `watchEvents`/`detailLevel` aren't upstream vocabulary and a clean structural
   no-op is a valid, fast outcome, not a thing to force a finding on). A clean re-confirmation
   (like 1527's google-play-reviews-scraper) is likewise a valid and expected outcome on a
   well-audited Actor — don't manufacture a finding where none exists.
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

