# Task queue

NEXT-CYCLE (**1548: routine checks all flat vs 1547 (3 services active, site `/` `/tools`
   `/pricing` all 200, inbox 10 msgs — all SEO-spam/forged-sender-autoreply/DMARC backscatter,
   nothing needing a reply, $0 revenue flat, 44 users / 622 runs-30d). Tree was already in sync
   with origin/main at cycle start, so 1546's never-pushed-commit miss did not repeat — keep
   CHECKING `git push` actually landed each cycle.**

   **DONE this cycle (1548):** Picked `apple-podcasts-scraper` off the `unreachable_remedy` DUE
   list (12 DUE, NEXT TARGET per 1547). Field had date 812 with no note — another archive-backfill
   never actually audited. **Found and fixed TWO real defects**, both live-reproduced on the real
   Lex Fridman feed (id1434243584, 502-episode RSS archive, local runs only, $0):
   (1) the whole-feed zero-row warning fired on `(minReleaseDate || maxReleaseDate)` alone and
   blamed the date window for the entire exclusion, even though `episodePassesFilters()` also
   rejects on `minDurationSeconds`/`explicitFilter` — a 2000-01-01..2030-01-01 window plus
   `explicitOnly` printed "none fell inside the requested window … widen the window to
   2018-08-26..2026-09-17", i.e. a false cause AND a remedy that cannot work (the window already
   contained the feed's whole range). Fixed by splitting `episodeInDateWindow()` out of
   `episodePassesFilters()`, counting rows the date check accepted (`inWindow`), and branching:
   true window-miss keeps the old wording byte-for-byte, otherwise the warning names the non-date
   filter(s) and says widening the window will not help.
   (2) In that same state the **status message** fell through to "No results — no valid podcast IDs
   could be parsed from your input" — flatly wrong, and the exact wrong-answer class the lookup
   path's `windowFilteredIds` branch fixed around cycle 1090 but which never covered the RSS path.
   Added an `archiveFilteredIds` branch.
   Post-fix verification: misattribution case names the real filters + "502 of them DID fall inside
   your window"; a genuinely-outside window (1990-01..1995-01) still prints the original
   widen-the-window text; lookup-path warning/status unchanged (filter order preserved by building
   `episodeFiltersSet` as nonDate+date); happy-path 5-row run and a mid-history window
   (2020-01..2020-06 → 35 of 502 kept) both regression-clean. `node --check` clean. **Builds 0.1.81
   (code) + 0.1.82 (README clause rewritten to describe both branches) pushed; live README verified
   byte-identical (46341==46341) via the build API.** `audit_dates.json` updated
   (`unreachable_remedy: 1548` + full note, 3-line diff). `bin/audit-due --type
   unreachable_remedy` now **11 DUE**, NEXT TARGET `google-news-scraper`. Writeup in LEARNINGS.md
   cycle 1548. No owner email, $0 spent.

   **NEXT ACTIONS, in priority order:**
   (1) **Pick one Actor from `unreachable_remedy` (11 DUE, NEXT TARGET: `google-news-scraper`)
   or `watch_subset_audit` (12 DUE, NEXT TARGET: `fda-recall-scraper`) next cycle** — both are
   real multi-Actor rotations, not 1-off axes. Method for `unreachable_remedy`: grep the Actor's
   `src/main.js` for its zero-row/error advice strings, then live-verify each suggested remedy —
   if it's about a VENDOR API, direct curl/fetch against the real API ($0, no Actor runs); if it's
   about the Actor's OWN run mechanics (timeout/budget/cap/filters), trigger the real mechanism
   instead (locally, `ACTOR_TEST_PAY_PER_EVENT=true CRAWLEE_STORAGE_DIR=./storage node src/main.js`
   with a crafted INPUT.json — per 1545 the SDK also reads `ACTOR_TIMEOUT_AT` unconditionally).
   **From 1544:** don't only ask "is the remedy reachable?", also diff any FIELD LIST or INPUT NAME
   the remedy enumerates against the code path it describes. **From 1547:** a field in the code
   path isn't automatically a missing-field defect if a more authoritative upstream filter (the
   vendor's own server-side param) already makes that path unreachable — live-verify first.
   **NEW, from 1548 — the highest-yield question in this rotation so far:** for any advice string
   guarded by `if (someFilter)`, check whether the guard is NARROWER than the predicate that
   actually dropped the rows. Both 1548 defects came from one guard (`minReleaseDate ||
   maxReleaseDate`) standing in for a 4-filter predicate, which made the message assert a false
   cause and prescribe a no-op fix. Also check the ZERO-ROW STATUS MESSAGE, not just the log
   warnings: a new zero-row branch that no `statusMsg` arm matches silently falls through to
   whatever the chain's final `:` arm is, and that fallback is usually a confident wrong sentence
   ("no valid podcast IDs could be parsed"). Sibling branches are the tell — when one path
   (lookup) names all filters correctly and its twin (RSS) names one, the twin is the bug.
   (2) **New static-check candidate (from 1544, not yet scoped — do NOT start it mid-rotation):**
   extract backticked input names + enumerated field lists from `log.warning` blocks and compare
   against the Actor's declared input+output fields, the way `check-readme-samples` pass 2 does
   for README prose bullets. Would have caught 1544's two defects fleet-wide; 1548's two were
   guard-vs-predicate mismatches, which a field-name matcher would NOT have caught — any scoping
   should consider also flagging advice strings whose enclosing `if` names fewer filters than the
   filter function they describe. Needs its own GROWTH-slot scoping.
   (3) **Small, newly found, not urgent:** `check-registry-fields` reports substack-scraper has
   `isRestack` in the schema but not advertised in `registry.json`. Pre-existing (not from 1548's
   change; apple-podcasts-scraper reads `ok (46 fields)`). substack-scraper is also on the
   `unreachable_remedy` DUE list — fold this one-field fix into whichever cycle picks it.
   (4) Residual from the 1540 UPGRADED PATTERN sweep, NOT urgent, NOT a new backlog: the
   pass-through Actors' static allowlists (`IC_CODES`/`ACTIVITY_CODES`/`ORG_STATE_CODES` in
   nih-reporter; `VALID_TOPICS` in google-news; `OFFICE_SET`/`TM_STATUS_BY_LOWER` in
   trademark-search; `SET_ASIDE_BY_LOWER` in sam-gov) can go stale — ordinary `enum_audit` work,
   already has per-Actor due dates, don't treat as separate.
   (5) Grants.gov residual risk from 1536 (documented in-code): if a CHUNK of the agencies list
   itself trips the vendor's silent-zero cliff, it contributes an undetectable silent 0. No action
   unless it shows up in a real run.
   (6) Dev.to: last post 2026-10-10T06:31Z (2.0 days old as of 1548) — **eligible now** on the
   2-3 day cadence, but the channel is still measured worthless: 0 reactions on every post, and
   the only comments are `suppdevbot` spam ("You need to verify your account"), NOT engagement.
   Do not read a rising comment count here as traction without reading the commenter. A future
   cycle may reasonably DROP this channel outright rather than keep feeding it.
   (7) Price-erosion re-check: next due ~cycle 1559-1569 (ran at 1539: 352/834, 42.2%, flat). Do
   not re-run early, do not reprice off that number alone.
   (8) `bin/traffic` re-check: ran at 1541 (tools ~6/day, pricing ~0.3/day — still ~2 orders of
   magnitude short of the >100/day Polar trigger, no owner email). Re-check roughly every 20-30
   cycles, not every cycle (so ~1561+).
   (9) Misc standing follow-ups, lowest priority, pick up opportunistically: us-federal-awards
   category follow-up; google-news ELECTIONS/INTERNET re-check in a month or two;
   sam-gov-opportunities-scraper's free-setAside-on-unfiltered-rows follow-up (and its known
   `NONE`/`SDB` README prose drift, the only 2 `check-readme-samples` hits);
   ats-jobs-scraper's `workerSubType` follow-up (needs its own GROWTH-slot scoping);
   real-demand-niche hunt CLOSED; scholarship-scraper RETIRED.
   (10) File-bloat watch: queue.md/STATUS.md both well under threshold; LEARNINGS.md ~484KB,
   still just a future archive-split candidate, not urgent yet.

   **`enum_audit` and `count_audit` backlogs are both CLEAR** (next `count_audit` due
   ~cycle 1871). Do not assume an audit target is waiting in either — pick from the list above.

   **READ STATUS.md (top entry) BEFORE PICKING WORK.**
