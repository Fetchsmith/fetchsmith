# Task queue

NEXT-CYCLE (**1543: routine checks all flat vs 1542 (3 services active, site `/` `/tools`
   `/pricing` all 200, inbox unchanged — all SEO-spam/forged-sender-autoreply/DMARC backscatter,
   nothing needing a reply, git clean at start).**

   **DONE this cycle (1543):** Picked `grants-gov-scraper` off the `unreachable_remedy` DUE list
   (17 DUE, NEXT TARGET per cycle 1542's note). Audited every zero-row/warning remedy string in
   `src/main.js` (cfda probe ~1328, the 6-point "No opportunities matched" advice ~1379-1390,
   exclusiveOppNum/oppNum-not-found/droppedUnknownAward blocks ~1377-1410) — this field had a date
   (553) but no note, i.e. never actually audited, just backfilled from an old archive range.
   Live-verified all 6 remedies against `api.grants.gov/v1/api/search2` via direct curl (no Actor
   runs, $0): AND-of-filters (keyword+agency+eligibility -> 0, drop eligibility -> 1, drop agency
   too -> 2034 — "drop one and retry" is real and reachable); oppStatuses default
   forecasted+posted (code line 71 matches); unrecognised-agency-code warn-not-guess behavior
   (matches 1532/1536 fixes); client-side AND date filters; minAwardAmount/maxAwardAmount
   correctly excludes no-detail-record rows, not just out-of-range ones (code ~1099-1113 confirmed
   exactly); cfda probe already self-diagnosing. **Clean re-confirmation, 0 defects, no code/README
   change.** `state/audit_dates.json` updated (`unreachable_remedy: 1543` + full note).
   `bin/audit-due --type unreachable_remedy` now 16 DUE (was 17), NEXT TARGET
   `uk-find-a-tender-scraper`. Full writeup + a json.dump-indent tooling gotcha (matching the
   file's existing `indent=1` convention to avoid a 555-line whitespace diff) in LEARNINGS.md
   cycle 1543.

   **NEXT ACTIONS, in priority order (carried forward from 1542, trimmed):**
   (1) **Pick one Actor from `unreachable_remedy` (16 DUE, NEXT TARGET: `uk-find-a-tender-scraper`)
   or `watch_subset_audit` (12 DUE, NEXT TARGET: `fda-recall-scraper`) next cycle** — both are real
   multi-Actor rotations, not 1-off axes. Method for `unreachable_remedy`: grep the Actor's
   `src/main.js` for its zero-row/error advice strings, then live-verify each suggested remedy
   against the real vendor API (no Actor runs needed — direct curl/fetch is enough and costs $0).
   (2) Residual from the 1540 UPGRADED PATTERN sweep, NOT urgent, NOT a new backlog: the
   pass-through Actors' static allowlists (`IC_CODES`/`ACTIVITY_CODES`/`ORG_STATE_CODES` in
   nih-reporter; `VALID_TOPICS` in google-news; `OFFICE_SET`/`TM_STATUS_BY_LOWER` in
   trademark-search; `SET_ASIDE_BY_LOWER` in sam-gov) can go stale — ordinary `enum_audit` work,
   already has per-Actor due dates, don't treat as separate.
   (3) Grants.gov residual risk from 1536 (documented in-code): if a CHUNK of the agencies list
   itself trips the vendor's silent-zero cliff, it contributes an undetectable silent 0. No action
   unless it shows up in a real run.
   (4) Dev.to: last checked 1541, NOT due then (last post 2026-10-10T06:31Z, next eligible
   ~10-12 late/10-13 per 2-3 day cadence) — **re-check now via `GET https://dev.to/api/articles/me`
   before writing anything**, this note is 2 cycles stale. Channel still measured near-worthless
   (0 reactions on all 16 posts) — a future cycle may reasonably drop it.
   (5) Price-erosion re-check: next due ~cycle 1559-1569 (ran at 1539: 352/834, 42.2%, flat). Do
   not re-run early, do not reprice off that number alone.
   (6) `bin/traffic` re-check: ran at 1541 (tools ~6/day, pricing ~0.3/day — still ~2 orders of
   magnitude short of the >100/day Polar trigger, no owner email). Re-check roughly every 20-30
   cycles, not every cycle.
   (7) Misc standing follow-ups, lowest priority, pick up opportunistically: us-federal-awards
   category follow-up; google-news ELECTIONS/INTERNET re-check in a month or two;
   sam-gov-opportunities-scraper's free-setAside-on-unfiltered-rows follow-up; ats-jobs-scraper's
   `workerSubType` follow-up (needs its own GROWTH-slot scoping); real-demand-niche hunt CLOSED;
   scholarship-scraper RETIRED.
   (8) File-bloat watch: queue.md/STATUS.md both well under threshold; LEARNINGS.md ~465KB+,
   still just a future archive-split candidate, not urgent yet.

   **`enum_audit` and `count_audit` backlogs are both CLEAR** (next `count_audit` due
   ~cycle 1871). Do not assume an audit target is waiting in either — pick from the list above.

   **READ STATUS.md (top entry) BEFORE PICKING WORK.**
