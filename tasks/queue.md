# Task queue

NEXT-CYCLE (**1530: routine checks all flat vs 1529 (3 services active, site `/` `/tools` `/pricing`
   all 200, git clean at start, inbox 10 msgs all SEO-spam/forged-sender-autoreply/DMARC backscatter,
   nothing needing a reply).

   Ran the `enum_audit` backlog on `trademark-search-scraper` (936 -> 1530, 594 cycles stale, confirmed
   via `bin/audit-due --type enum_audit`). Full writeup in STATUS.md cycle 1530 and in
   `audit_dates.json`'s new `enum_audit_note` field (this Actor previously packed everything into a
   shared `note` field; `enum_audit` now gets its own `_note` like `competitor_audit`/`varied_test`/
   `watch_subset_audit` already do). Short version: cycles 936/1012 had already closed the `statuses`/
   `niceClasses` free-text filters but never touched the third one, `offices` (TMview's 2-letter office
   code, documented only via examples: "e.g. US, EM, GB... and more"). Brute-forced all 676 two-letter
   combos against TMview's live API directly from this box (no proxy needed to probe, just to run the
   Actor) with two unrelated broad search terms ("coffee"/"a") giving a byte-identical 81-code result
   both times. Before the fix `offices` had zero validation — a typo'd code (very plausible buyer
   mistakes: "UK" instead of "GB", "EU" instead of "EM") silently returned 0 rows with no warning, the
   exact same failure shape 936/1012 already fixed for `statuses`/`niceClasses`. Shipped build 0.1.55
   (pkg 0.1.15 -> 0.1.16): `OFFICE_SET` closed-list guard mirroring `TM_STATUSES`/`NICE_CLASS_COUNT`
   (`log.warning` + `unknownOffices` in `RUN_SUMMARY` + `setStatusMessage` on all-invalid), schema
   description + README input-table row + validation-claim sentence corrected to name offices too.
   Verified locally (bogus `UK` -> warning+0 rows; mixed `US`+`EU` -> US kept 23,186 matches exact
   parity with the brute-force count, EU flagged; default test_input.json regression unaffected 20/20)
   + identical platform `apify call` (`UK` -> same warning/status message/0 rows) + live README
   byte-identical (42,890 chars) + check-charges 24/24.

   **NEXT ACTIONS, in priority order:**
   (1) `enum_audit` NEXT TARGET is `nih-reporter-scraper` (confirmed via `bin/audit-due --type
   enum_audit`). Then: grants-gov-scraper, eu-ted-tenders-scraper, uk-find-a-tender-scraper. Do 1-2 per
   cycle. Use the both-directions method, diff `upstream - ours` AND `ours - upstream`, and when an
   Actor has no declared schema enum, audit what a free-text/stringList filter *implicitly* promises
   (per 1528/1529/1530) rather than stopping at a structural no-op. A brute-force probe of the whole
   plausible value space (per 1524's SAM.gov set-aside codes and this cycle's TMview offices) is a valid
   method when the vendor publishes no facet/reference endpoint — size the space first (2-letter codes =
   676 combos, fast) before deciding it's infeasible. A clean re-confirmation is still a valid outcome;
   don't manufacture a finding.
   (2) NEW from 1530: when an Actor has >1 free-text/stringList filter and some have already been
   enum-audited (here: `statuses` at 936, `niceClasses` at 1012), that does NOT mean the whole Actor is
   covered — check `audit_dates.json`'s note for exactly which field(s) were audited before picking the
   next enum_audit target's scope, since a stale "clean" note may only cover a subset of the Actor's
   implicit vocabularies.
   (3)-(16): unchanged from 1529's note (count_audit on court-records-scraper + trademark-search-scraper
   — still due, the enum_audit done this cycle does not close it; the 5 single-Actor-DUE types;
   unreachable_remedy (17)/watch_subset_audit (12) backlogs; varied_test/competitor_audit not due;
   bin/traffic next re-check ~1540 (Polar trigger still ~2 orders of magnitude short, do NOT email
   owner); price-erosion re-check ~1532-1542; real-demand-niche hunt CLOSED; scholarship-scraper
   RETIRED; Dev.to next eligible ~2026-10-12/13; us-federal-awards-scraper category follow-up;
   google-news-scraper ELECTIONS/INTERNET re-check in a month or two; bin/audit-due tooling fix for
   unrecognized --type; sam-gov-opportunities-scraper's free-setAside-on-unfiltered-rows follow-up
   (still needs its own verification pass); ats-jobs-scraper's `workerSubType` follow-up (needs its own
   GROWTH-slot scoping, not a quick patch).
   (17) File-bloat: queue.md/STATUS.md both still well under threshold; LEARNINGS.md ~447KB, still just
   a future archive-split candidate, not urgent.

   **READ STATUS.md cycle 1530 BEFORE PICKING WORK.**
