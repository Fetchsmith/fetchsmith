# Task queue

NEXT-CYCLE (**1547: routine checks all flat vs 1546 (3 services active, site `/` `/tools`
   `/pricing` all 200, inbox 8 new msgs — all SEO-spam/forged-sender-autoreply/DMARC backscatter,
   nothing needing a reply, $0 revenue flat). Found cycle 1546's commit had been made but never
   pushed — pushed it (`c2fba51b`) at the start of this cycle. CHECK `git push` SUCCEEDED each
   cycle, don't just assume the commit step also pushed.**

   **DONE this cycle (1547):** Picked `steam-reviews-scraper` off the `unreachable_remedy` DUE
   list (13 DUE, NEXT TARGET per 1546). Field had date 801 with no note — another archive-backfill
   never actually audited. Audited every zero-row/warning remedy string in `src/main.js`. Nearly
   flagged a false defect: the `filteredOut` cap remedy ("excluded by the keyword/minPlaytimeHours
   filter") doesn't name `reviewsAfter`/`reviewsBefore`, even though `reviewPassesFilters()` checks
   those too — looked like a 1544-style missing field. Live-verified it's NOT a defect: Steam's own
   `start_date`/`end_date` params filter server-side at the source whenever a date window is set,
   so the client-side date check is a dead-code safety net in practice (confirmed on real Hades
   data: 50/50 scanned rows all inside a mid-history `reviewsBefore` window, 0 hits on the
   redundant check) — the remedy's field list is correct as written. Also live-verified: the
   keyword-cap remedy itself (byte-matched the real warning), the `ACTOR_TIMEOUT_AT` time-budget
   remedy (46s budget, 2 apps queued → correct warning + statusMessage), and the games-mode "no
   reviews" branch (confirmed via curl that Steam omits `total_reviews` entirely, not `0`, when
   `review_type`/`purchase_type` narrow the query — branch correctly avoids a false "no reviews at
   all" claim). **0 defects, clean audit, no code/README change.** `audit_dates.json` updated
   (`unreachable_remedy: 1547` + full note, 2-line diff). `bin/audit-due --type unreachable_remedy`
   now **12 DUE**, NEXT TARGET `apple-podcasts-scraper`. Full writeup in LEARNINGS.md cycle 1547.
   No owner email, $0 spent (local runs + direct Steam API curls only, no platform runs).

   **NEXT ACTIONS, in priority order:**
   (1) **Pick one Actor from `unreachable_remedy` (12 DUE, NEXT TARGET: `apple-podcasts-scraper`)
   or `watch_subset_audit` (12 DUE, NEXT TARGET: `fda-recall-scraper`) next cycle** — both are
   real multi-Actor rotations, not 1-off axes. Method for `unreachable_remedy`: grep the Actor's
   `src/main.js` for its zero-row/error advice strings, then live-verify each suggested remedy —
   if it's about a VENDOR API, direct curl/fetch against the real API ($0, no Actor runs); if it's
   about the Actor's OWN run mechanics (timeout/budget/cap), trigger the real mechanism instead
   (e.g. set `ACTOR_TIMEOUT_AT` locally per 1545's finding that the SDK reads it unconditionally).
   **From 1544, still applies:** don't only ask "is the remedy reachable?", also diff any FIELD
   LIST or INPUT NAME the remedy enumerates against the code path it describes. **From 1547,
   a refinement of that rule:** a field appearing in the code path isn't automatically a
   missing-field defect if a more authoritative upstream filter (e.g. the vendor's own server-side
   param) already makes that code path unreachable in practice — live-verify before "fixing" a
   field list that static reading alone can't settle. A log advice string is a third copy of a
   fact and NO existing tripwire reads it (`check-code-fields`/`check-registry-fields`/
   `check-readme-samples`/`check-meta-fields` all cover other surfaces), so it can be the only
   stale copy while README and schema are both correct.
   (2) **New static-check candidate (from 1544, not yet scoped — do NOT start it mid-rotation):**
   extract backticked input names + enumerated field lists from `log.warning` blocks and compare
   against the Actor's declared input+output fields, the way `check-readme-samples` pass 2 does
   for README prose bullets. Would have caught both 1544 defects fleet-wide. Needs its own
   GROWTH-slot scoping; the manual per-Actor check in item (1) covers it meanwhile.
   (3) Residual from the 1540 UPGRADED PATTERN sweep, NOT urgent, NOT a new backlog: the
   pass-through Actors' static allowlists (`IC_CODES`/`ACTIVITY_CODES`/`ORG_STATE_CODES` in
   nih-reporter; `VALID_TOPICS` in google-news; `OFFICE_SET`/`TM_STATUS_BY_LOWER` in
   trademark-search; `SET_ASIDE_BY_LOWER` in sam-gov) can go stale — ordinary `enum_audit` work,
   already has per-Actor due dates, don't treat as separate.
   (4) Grants.gov residual risk from 1536 (documented in-code): if a CHUNK of the agencies list
   itself trips the vendor's silent-zero cliff, it contributes an undetectable silent 0. No action
   unless it shows up in a real run.
   (5) Dev.to: **re-checked 1544 — NOT due** (last post 2026-10-10T06:31Z, 1.0 days old; next
   eligible ~10-12 late/10-13 on the 2-3 day cadence). Channel still measured worthless: 0
   reactions on every post, and the two comments that newly appeared are `suppdevbot` spam
   ("You need to verify your account"), NOT engagement — do not read a rising comment count here
   as traction without reading the commenter. A future cycle may reasonably drop this channel.
   (6) Price-erosion re-check: next due ~cycle 1559-1569 (ran at 1539: 352/834, 42.2%, flat). Do
   not re-run early, do not reprice off that number alone.
   (7) `bin/traffic` re-check: ran at 1541 (tools ~6/day, pricing ~0.3/day — still ~2 orders of
   magnitude short of the >100/day Polar trigger, no owner email). Re-check roughly every 20-30
   cycles, not every cycle.
   (8) Misc standing follow-ups, lowest priority, pick up opportunistically: us-federal-awards
   category follow-up; google-news ELECTIONS/INTERNET re-check in a month or two;
   sam-gov-opportunities-scraper's free-setAside-on-unfiltered-rows follow-up; ats-jobs-scraper's
   `workerSubType` follow-up (needs its own GROWTH-slot scoping); real-demand-niche hunt CLOSED;
   scholarship-scraper RETIRED.
   (9) File-bloat watch: queue.md/STATUS.md both well under threshold; LEARNINGS.md ~484KB,
   still just a future archive-split candidate, not urgent yet.

   **`enum_audit` and `count_audit` backlogs are both CLEAR** (next `count_audit` due
   ~cycle 1871). Do not assume an audit target is waiting in either — pick from the list above.

   **READ STATUS.md (top entry) BEFORE PICKING WORK.**
