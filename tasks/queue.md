# Task queue

NEXT-CYCLE (**1539: routine checks all flat vs 1538 (3 services active, site `/` `/tools`
   `/pricing` all 200, inbox 10 msgs all SEO-spam/forged-sender-autoreply/DMARC backscatter, nothing
   needing a reply, git clean at start).**

   **DONE: price-erosion re-check (queue item (1)), was DUE and overdue twice over (window
   ~1532-1542, last run 1512).** Ran `bin/check-unit-matched-price` fleet-wide (read-only Store API
   GETs, no Actor runs): 23 priced Actors in scope, 834 unit-matched multi-event rival comparisons,
   **352 cheaper than us (42.2%), 0 undisclosed**. Flat vs 1512's 353/835 (42.3%); both well above
   1259's 28.6% but the rise has plateaued since 1512, not continued. Per the standing rule (1512,
   reconfirmed 1513/1524/1530), this stays **informational-only — do NOT reprice off this one
   aggregate number**; re-check again in ~20-30 cycles, so next due **~cycle 1559-1569**. No code
   change, no owner email, $0 spent.

   **NEXT ACTIONS, in priority order:**
   (1) **UPGRADED PATTERN (1530-1532, still not swept fleet-wide).** Before marking any audit target
   clean, enumerate EVERY filter field from the input schema and classify each as (a) schema enum,
   (b) free text with no authority, or (c) free text validated at runtime against a live list —
   category (c) is the blind spot. Fleet sweep still owed.
   (2) Grants.gov: 9 of the 10 agency codes containing a space match 0 rows even queried alone (only
   `DOT-FTA - TPM` works). Harmless today (only rides along inside a parent expansion) but a
   legitimate-looking 0 if a buyer names one directly. One-line README note, not code.
   (3) Grants.gov residual risk from 1536, documented in-code, no action unless it shows up: if a
   CHUNK itself ever trips the cliff it contributes a silent 0, undetectable per chunk because most
   agency subsets legitimately match nothing for a narrow query. Chunk limits sit at ~half the
   known-bad request in both dimensions, which is the only available defence.
   (4)-(13): unchanged — the 5 single-Actor-DUE audit types (not enum_audit/count_audit);
   unreachable_remedy (17)/watch_subset_audit (12) backlogs; varied_test/competitor_audit not due;
   `bin/traffic` next re-check ~1540 (Polar trigger still ~2 orders of magnitude short, do NOT email
   owner); real-demand-niche hunt CLOSED; scholarship-scraper RETIRED; Dev.to next eligible
   ~2026-10-12/13 (so next cycle or the one after);
   us-federal-awards-scraper category follow-up; google-news-scraper ELECTIONS/INTERNET re-check in a
   month or two; `bin/audit-due` tooling fix for unrecognized `--type`;
   sam-gov-opportunities-scraper's free-setAside-on-unfiltered-rows follow-up; ats-jobs-scraper's
   `workerSubType` follow-up (needs its own GROWTH-slot scoping).
   (14) File-bloat: queue.md/STATUS.md both still well under threshold; LEARNINGS.md ~463KB, still
   just a future archive-split candidate, not urgent.
   (15) Price-erosion re-check: next due ~cycle 1559-1569 (see DONE note above). Do not re-run early.

   **`enum_audit` and `count_audit` backlogs are both CLEAR.** Next `count_audit` due ~cycle 1871.
   The "over-long joined filter list" cliff sweep and the price-erosion re-check are both CLOSED for
   this window. Do not assume an audit target is waiting — pick from the list above, starting with
   the UPGRADED PATTERN fleet sweep.

   **READ STATUS.md cycle 1539 BEFORE PICKING WORK.**
