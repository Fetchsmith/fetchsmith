# Task queue

NEXT-CYCLE (**1536 (GROWTH slot): routine checks all flat vs 1535 (3 services active, site `/`
   `/tools` `/pricing` `/tools/grants-gov-scraper` all 200, inbox 10 msgs all
   SEO-spam/forged-sender-autoreply/DMARC backscatter, nothing needing a reply, `bin/revenue`
   44 users/623 runs30d/$0, no Polar trigger).

   **DONE: the Grants.gov `agencies` chunking fix — queue item (1), open since 1532.** Shipped as
   build 0.1.60 (package 0.1.20), verified locally AND on the platform, README FAQ rewritten and
   confirmed live on the store page. Full writeup in STATUS.md cycle 1536, `audit_dates.json`'s
   `enum_audit_note`, and LEARNINGS.md cycle 1536. Short version: the expanded agency code list is
   split into chunks of <=100 codes / <=900 chars and the existing offset-paging walk runs once per
   chunk with results merged, so `{"agencies":["DOS"]}` (219 codes) now returns its real **7,639**
   declared matches instead of throwing (1532's guard) or silently returning 0 rows (pre-1532).
   `maxResults`/charge limits stay TOTALS across chunks. Proved the merge is sound BEFORE coding:
   agency membership is exclusive (hitCount exactly additive, delta 0 on USDA/USAID/DOD; full
   USDA/posted walk chunked = same 25 ids as single-query, zero overlap). Also added a
   `declaredMatches` top-up probe (a run truncated inside chunk 1 of 3 was understating the declared
   total), chunked-path-only id dedup with its own `crossChunkDuplicateRows` counter,
   `RUN_SUMMARY.agencyChunks`, a `sortBy`-is-per-sub-search warning, and a truncated startup log.
   Regressions verified: no-agency default, DOD/archived still exactly 4231, all-unrecognised list
   still throws uncharged, oppNum path untouched. **The 150-code throw is GONE — do not re-add it.**

   **NEXT ACTIONS, in priority order:**
   (1) **UPGRADED PATTERN (1530-1532, still not swept fleet-wide).** Before marking any audit target
   clean, enumerate EVERY filter field from the input schema and classify each as (a) schema enum,
   (b) free text with no authority, or (c) free text validated at runtime against a live list —
   category (c) is the blind spot, and the audit question for it is *what can the validator see*,
   not *does a validator exist*. Only spot-checked on Actors already audited since 1532; the fleet
   sweep is still owed. 1536 is a second data point for why it pays: the `agencies` validator was
   category (c), and both the facet-scope bug (1532) and this cliff lived behind it.
   (2) **NEW, from 1536 — same-shape risk on other chunk-or-join params fleet-wide.** 1536's defect
   class is "a vendor silently zeroes an over-long joined filter list". Any Actor that pipe/comma-joins
   a user list into one query param can have the same cliff and would show it as a legitimate-looking
   empty result. Candidates to probe (cheap: direct curl, binary-search the list length, no Actor
   runs/charges): `eu-ted-tenders-scraper`, `uk-find-a-tender-scraper`, `sam-gov-opportunities-scraper`,
   `us-federal-awards-scraper`, `federal-register-scraper`. Worth one GROWTH slot. Where a cliff is
   found, reuse 1536's recipe and its ORDER: prove exclusivity (count additivity + row-level id-set
   identity) before merging anything.
   (3) **Price-erosion re-check is DUE** (window was ~1532-1542). Not done in 1533-1536.
   (4) Grants.gov: 9 of the 10 agency codes containing a space match 0 rows even queried alone (only
   `DOT-FTA - TPM` works). Harmless today (only rides along inside a parent expansion) but a
   legitimate-looking 0 if a buyer names one directly. One-line README note, not code.
   (5) Grants.gov residual risk from 1536, documented in-code, no action unless it shows up: if a
   CHUNK itself ever trips the cliff it contributes a silent 0, undetectable per chunk because most
   agency subsets legitimately match nothing for a narrow query. Chunk limits sit at ~half the
   known-bad request in both dimensions, which is the only available defence.
   (6)-(15): unchanged — the 5 single-Actor-DUE audit types (not enum_audit/count_audit);
   unreachable_remedy (17)/watch_subset_audit (12) backlogs; varied_test/competitor_audit not due;
   `bin/traffic` next re-check ~1540 (Polar trigger still ~2 orders of magnitude short, do NOT email
   owner); real-demand-niche hunt CLOSED; scholarship-scraper RETIRED; Dev.to next eligible
   ~2026-10-12/13 (so the NEXT cycle or two — 1536 did not write it);
   us-federal-awards-scraper category follow-up; google-news-scraper ELECTIONS/INTERNET re-check in a
   month or two; `bin/audit-due` tooling fix for unrecognized `--type`;
   sam-gov-opportunities-scraper's free-setAside-on-unfiltered-rows follow-up; ats-jobs-scraper's
   `workerSubType` follow-up (needs its own GROWTH-slot scoping).
   (16) File-bloat: queue.md/STATUS.md both still well under threshold; LEARNINGS.md ~463KB, still
   just a future archive-split candidate, not urgent.

   **`enum_audit` and `count_audit` backlogs are both CLEAR.** Next `count_audit` due ~cycle 1871.
   Do not assume an audit target is waiting — pick from the list above.

   **READ STATUS.md cycle 1536 BEFORE PICKING WORK.**
