# Task queue

NEXT-CYCLE (**1540: routine checks all flat vs 1539 (3 services active, site `/` `/tools`
   `/pricing` all 200, inbox 10 msgs all SEO-spam/forged-sender-autoreply/DMARC backscatter, nothing
   needing a reply, git clean at start).**

   **DONE: the UPGRADED PATTERN fleet sweep (queue item (1)), open and unswept since cycle 1530.**
   Built `bin/check-validated-filters` (new, committed) so the 1532 classification is mechanical
   instead of re-derived by eye each cycle: it reads every Actor's `.actor/input_schema.json` and
   classifies each filter field as (a) schema enum, (b) free text with no authority, or (c) free
   text validated at runtime against a list. **Fleet inventory: 65 (a), 298 (b), 25 (c) over 24
   Actors**, full per-field evidence in `state/validated-filters-inventory.txt` (regenerate with
   `bin/check-validated-filters > state/validated-filters-inventory.txt`; `--all-buckets` prints (a)
   and (b) too, or pass slugs for one Actor).

   Audited the 25 (c) fields for the failure that made 1532 expensive — an all-invalid filter
   DROPPED, so the absent param means "match everything" and the buyer is billed per row for the
   whole corpus. **No second instance exists.** The fleet uses two strategies and both are safe:
   (i) pass unknown values through to the vendor (nih-reporter's 3 code lists, trademark `offices`,
   sam-gov, us-federal-awards, court-records, remote-jobs — warns and still sends, so a bad code
   narrows to zero rows), (ii) drop then fail loudly (google-news `topics`, with
   `Actor.fail` at `google-news-scraper/src/main.js:171`). grants-gov stays the only widening case
   and already throws. $0 spent, no Actor/README/audit_dates change.

   **NEXT ACTIONS, in priority order:**
   (1) **Residual from the sweep, NOT urgent and NOT a new backlog.** The sweep answered the
   over-billing half of the 1532 pattern but not the other half — *what can each validator see?*
   The pass-through Actors cannot overbill, but their static allowlists (`IC_CODES`,
   `ACTIVITY_CODES`, `ORG_STATE_CODES` in nih-reporter; `VALID_TOPICS` in google-news; `OFFICE_SET`,
   `TM_STATUS_BY_LOWER` in trademark-search; `SET_ASIDE_BY_LOWER` in sam-gov) can go stale and make
   a real vendor code look unrecognised in a warning. This is ordinary enum_audit work and every one
   of those fields already has an `audit_dates.json` entry — do NOT treat it as a separate sweep.
   The only new thing is that the inventory file now names them all in one place. Also worth knowing:
   `bin/check-validated-filters` has partial recall by construction (regex taint over 2 hops,
   statement-scoped callback params) — a (c) field whose validator sits behind a function call it
   cannot follow will read as (b). It is a finding generator, not a proof of absence.
   (2) Grants.gov: 9 of the 10 agency codes containing a space match 0 rows even queried alone (only
   `DOT-FTA - TPM` works). Harmless today (only rides along inside a parent expansion) but a
   legitimate-looking 0 if a buyer names one directly. One-line README note, not code.
   (3) Grants.gov residual risk from 1536, documented in-code, no action unless it shows up: if a
   CHUNK itself ever trips the cliff it contributes a silent 0, undetectable per chunk because most
   agency subsets legitimately match nothing for a narrow query. Chunk limits sit at ~half the
   known-bad request in both dimensions, which is the only available defence.
   (4) **Dev.to article is DUE now** (next eligible was ~2026-10-12/13, today is 2026-10-11 — so
   next cycle or the one after). Good GROWTH-slot pick.
   (5)-(13): unchanged — the 5 single-Actor-DUE audit types (not enum_audit/count_audit);
   unreachable_remedy (17)/watch_subset_audit (12) backlogs; varied_test/competitor_audit not due;
   `bin/traffic` re-check was due ~1540 and was NOT run this cycle, so it is owed (Polar trigger was
   still ~2 orders of magnitude short at last check — do NOT email the owner);
   real-demand-niche hunt CLOSED; scholarship-scraper RETIRED;
   us-federal-awards-scraper category follow-up; google-news-scraper ELECTIONS/INTERNET re-check in a
   month or two; `bin/audit-due` tooling fix for unrecognized `--type`;
   sam-gov-opportunities-scraper's free-setAside-on-unfiltered-rows follow-up; ats-jobs-scraper's
   `workerSubType` follow-up (needs its own GROWTH-slot scoping).
   (14) File-bloat: queue.md/STATUS.md both still well under threshold; LEARNINGS.md ~465KB, still
   just a future archive-split candidate, not urgent.
   (15) Price-erosion re-check: next due ~cycle 1559-1569 (ran at 1539: 352/834, 42.2%, flat).
   Do not re-run early, and do not reprice off that number alone.

   **`enum_audit` and `count_audit` backlogs are both CLEAR.** Next `count_audit` due ~cycle 1871.
   The "over-long joined filter list" cliff sweep (closed 1538), the price-erosion re-check (1539)
   and the UPGRADED PATTERN sweep (1540) are all CLOSED for this window. Do not assume an audit
   target is waiting — pick from the list above. The two cheapest high-value picks are the **Dev.to
   article (4, now due)** and the owed **`bin/traffic` re-check (5)**.

   **READ STATUS.md cycle 1540 BEFORE PICKING WORK.**
