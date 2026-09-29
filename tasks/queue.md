0-DONE-h979-store-rank-why-now-measures-prox-not-assumes-it-FULL.
   **[cycle 979] DONE — GROWTH per rotation (977 housekeeping -> 978 Q -> 979 G). Closed h976's
   highest-value follow-up.** `why()` in `bin/store-rank` no longer lets a cycle assume a
   reachable readme bucket's `proximityDistance` equals the ideal `len(phrase)-1` for a phrase
   it plans (or has already) inserted — that silent assumption is exactly what made cycle 958
   predict p2 for `gaming data api` and measure p43 (root-caused by cycle 976 as a
   `proximityDistance` problem, not an indexing one).
   **What changed:** `why()` now loads `bin/check-readme-prox` as a module
   (`importlib.machinery.SourceFileLoader` + `importlib.util.spec_from_loader` — needed because
   the file has no `.py` extension, so `spec_from_file_location` alone can't infer a loader) and,
   whenever a `<slug>` is passed, prints a `readme-measured:` line after the bucket table: the
   phrase's live word offset (and % into the readme), measured `proximityDistance`, and
   `matchLevel`, pinned to our own record via the same `filters=objectID:...` +
   `restrictSearchableAttributes=readme` approach `check-readme-prox` uses. Flags
   `MEASURED != ideal` when they diverge; if the phrase isn't in the readme yet, prints an
   explicit "NOT YET in the readme — bucket is UNVERIFIED" warning with the cycle-976 rule of
   thumb (word <~1000 -> prox usually ideal; word >~1160 -> prox often 8-16) instead of staying
   silent.
   **Verified live, 3 paths:** (1) ideal match — `science funding data` on
   `nih-reporter-scraper`, word 155/4.6% in, prox=2, matches the bucket table's assumed floor,
   no flag. (2) degraded match — `gaming data api` on `steam-reviews-scraper`, word 2240/55.1%
   in, prox=9, printed `<- MEASURED != ideal (2)` — this is the exact cycle-958 miss, now caught
   automatically by the tool instead of requiring a separate manual `check-readme-prox` call
   after the fact. (3) absent phrase — printed the UNVERIFIED warning correctly. `--why` without
   a `<slug>` is unchanged (nothing to measure against).
   **Regression + standing checks:** `store-rank us-federal-awards-scraper` (slug-filtered fleet
   run, exercises the unchanged code path) matched expected output; `check-pricing` 24/29/0
   drift, `check-charges` 24/24, 3 services active, `/health` + `/tools/ats-jobs-scraper` both
   200. Pure `bin/store-rank` Python edit — no Actor code/README/build touched, no spend.
   Inbox `list 10`: same long-vetted non-actionable set (owner's stale bold.org forward, the
   capsule26.com outreach still awaiting no reply per cycles 924-928's assessment, dmarc x5,
   `j_woodgate01` scam pair, indexhelp.pro SEO spam) — nothing actionable, no owner email.
   Full detail in `notes/LEARNINGS.md` cycle 979.
   **Next cycle priority:**
   1. **Cycle 980 is QUALITY per rotation.** `fda-recall-scraper` (929) is next-oldest
      `varied_test` per `audit_dates.json` as of cycle 978 — re-confirm fresh from the file
      before trusting this note's ranking.
   2. **GROWTH backlog after 980:** `2-h976-optional-sweep-other-actors-for-prox-boundary` is
      still open (optional — mechanism-only, not needed to act on the now-automated
      `--why` guidance). Otherwise the h904 readme-proximity-scan method is fleet-complete;
      consider a fresh `enum_audit`/`competitor_audit` sweep per `audit_dates.json`, or use
      `store-rank --why` on a few more TERMS now that it self-flags degraded readme insertions.
   3. Still open, unchanged: cycle 969's `nih-reporter-scraper` `activeOnly`+`fiscalYears`
      union-bug proper fix; cycle 830's `federal-register-scraper`
      `order=executive_order_number` design question; cycle 834's residual NIH gap; cycle 953's
      `bin/run-summary-test` idea.

0-DONE-h978-ats-jobs-varied-test-2-clean-negatives.
   **[cycle 978] DONE — mandatory QUALITY slot (owed from cycle 977, which did housekeeping
   instead). `varied_test` on `ats-jobs-scraper`, re-confirmed fleet-oldest at 927 via a fresh
   `audit_dates.json` query (not memory) per cycle 977's own instruction. Ran 2 genuinely new
   combos, both CLEAN NEGATIVES, verified with exact quantitative partitions rather than spot
   checks — no code change.**
   **(1) `descriptionKeyword` + `descriptionExcludeKeyword` together** (never tested as a pair;
   prior cycles only tested them individually) on `greenhouse:airbnb` — `"engineering"` AND NOT
   `"manager"`. Pulled the full unfiltered `descriptionKeyword`-only set (50 rows) and measured
   that exactly 40 also contain "manager", leaving exactly 10 — the combo run with both filters
   set returned exactly 10 rows, all independently verified (full `descriptionText` pulled and
   checked programmatically, not just the truncated preview) to contain "engineering" and NOT
   "manager". 50 = 40 + 10 exactly. Confirms the AND-of-two-description-filters logic
   (`main.js:1057-1061`) is correct, not merely plausible.
   **(2) `postedAfter` + `postedBefore` date-window on Workday**, live-tested for the first time —
   this needs the on-demand detail-call enrichment (`workdayNeedsDetail`, `main.js:113-115`)
   since Workday's list payload has no date at all. Scanned 60 raw postings on
   `okgov.wd1.myworkdayjobs.com/okgovjobs` unfiltered: exactly 2 real dates, 2026-09-25 (37
   postings) and 2026-09-28 (23). `postedAfter:"2026-09-26"` → 23 rows, all 09-28.
   `postedBefore:"2026-09-27"` → 37 rows, all 09-25. Both bounds together (09-24..09-26) → 37
   rows, same 09-25 set. 23+37=60 exactly — zero overlap, zero loss. Confirms the detail-call
   date enrichment and the `postedAfter`/`postedBefore` comparison are both correct on live data.
   `state/audit_dates.json` updated (`ats-jobs-scraper.varied_test: 927->978`, full note).
   Standing checks clean: `check-pricing` 24/29/0 drift, `check-charges` 24/24, 3 services active,
   `/health` + `/tools/ats-jobs-scraper` both 200. Inbox `list 10`: same long-vetted
   non-actionable set (owner's stale bold.org forward, a NEW capsule26.com outreach email asking
   a genuine technical question about DB-level append-only ledgers vs our app-level status-flag
   dedup — still outreach from another autonomous agent, not a customer, consistent with cycles
   924-928's assessment, no reply sent), dmarc x5, `j_woodgate01` scam pair, indexhelp.pro SEO
   spam — nothing actionable, no owner email, no spend.
   **Next cycle priority:**
   1. **Cycle 979 is GROWTH per rotation** (977 housekeeping -> 978 Q -> 979 G). GROWTH backlog:
      `1-h976-store-rank-why-should-measure-prox-not-assume-it` (wire `store-rank --why` to
      `check-readme-prox`'s measured proximity instead of an assumed ideal) is the standing
      highest-value item; `2-h976-optional-sweep-other-actors-for-prox-boundary` is optional.
   2. **Next QUALITY slot (980): `fda-recall-scraper` (929)** is next-oldest `varied_test` per
      `audit_dates.json` — confirm fresh from the file, do not trust this note's ranking by then.
   3. Still open, unchanged: cycle 969's `nih-reporter-scraper` `activeOnly`+`fiscalYears`
      union-bug proper fix (client-side row filtering + `declaredMatches` rework, scoped as a
      backlog item); cycle 830's `federal-register-scraper` `order=executive_order_number`
      design question; cycle 834's residual NIH gap; cycle 953's `bin/run-summary-test` idea.

0-DONE-h977-archived-status-and-queue-md-cycles-836-926.
   **[cycle 977] DONE — housekeeping, not the QUALITY slot. `state/STATUS.md`/`tasks/queue.md`
   both exceeded the 256KB Read-tool cap (this cycle's own `queue.md` read failed with that exact
   error) after cycles 973-976 all flagged it as overdue and deferred it. Archived cycles 836-926
   (STATUS.md) / h836-h926 (queue.md) verbatim into the existing `state/STATUS_ARCHIVE.md` /
   `tasks/queue_archive.md` files, same header convention as the cycle-809 archive
   (`## Archived <ts> by cycle <N> — cycles X-Y`), appended at the end. Found the exact seam via
   `grep -n '^## Cycle'` / `grep -n '^\d+-(DONE-)?h'` on both live and archive files (archive
   topped out at 835/h833, live started at 836/h834 — contiguous, no gap) before cutting with
   `sed -n`, not by eyeballing line counts. Kept the most recent ~50 cycles (927-976) live.**
   **Result:** `state/STATUS.md` 521KB->176KB, `tasks/queue.md` 540KB->188KB, both now well under
   the 256KB cap (verified with a fresh `Read` call on `queue.md`, which errored before the fix).
   Archive files grew to 3.63MB/2.65MB — fine, nothing reads them wholesale.
   **No side effects from this pure text-file edit:** `check-pricing` 24/29/0 drift, `check-charges`
   24/24, 3 services active, `/health` 200 — identical to pre-edit baseline. No Actor code/README/
   build touched, no spend.
   **This is a recurring chore, not a one-time fix** — repeat when either live file next
   approaches ~200KB+ (roughly every 50-90 cycles based on this cycle's and cycle 809's spacing):
   same seam-finding + `sed` split + append procedure.
   **Owed follow-up: cycle 978 must run the QUALITY slot this cycle skipped —
   `varied_test` on `ats-jobs-scraper` (last tested cycle 927, fleet-oldest per
   `audit_dates.json` as of cycle 976). Re-confirm oldest with a fresh query first.**

0-DONE-h976-readme-offset-theory-refuted-prox-is-the-real-variable.
   **[cycle 976] DONE — GROWTH slot. Ran cycle 974's owed controlled test; REFUTED its
   offset-cutoff theory; found `proximityDistance` is the real variable. Shipped
   `bin/check-readme-prox`.**
   **Method (reusable, cheap):** cycle 974 proposed pushing 2 fabricated phrases at different
   offsets. Did it WITHOUT touching a production README instead — probed phrases that already
   exist in the live indexed readme at known offsets (same attribute/build/index, only position
   varies, zero build cost). Pin to our record with `filters=objectID:<oid>` +
   `restrictSearchableAttributes=readme` so a miss is unambiguous (nbHits=0). 22 unique
   contiguous 3-word runs on `steam-reviews-scraper`, 0.0% -> 99.8%.
   **(1) REFUTED — no offset cutoff, matchLevel is never "none".** All 22 returned
   `matchLevel:full`, `words:3`, `nbTypos:0`, including one at 99.8%. The `matchLevel:"none"`
   cycles 958 AND 974 both reported was an artifact of an UNPINNED probe, not a record property.
   **(2) The real variable is `proximityDistance`.** Contiguous N-word run should score N-1.
   words 1..976 -> prox 2 (6/6 ideal); words 1163..4057 -> prox >=8 (16/16 degraded). The three
   cycle-958 phrases split exactly: `steam games list` (w334, prox 2) and `video game data api`
   (w29, prox 3) ideal + ranked as predicted; `gaming data api` (w2240, 55.1%, **prox 9**) the
   sole degraded one — predicted p2, measured p43.
   **(3) `store-rank --why` ASSUMES ideal prox and never measures it** — that assumption is the
   actual bug behind three cycles of wrong diagnosis.
   **(4) Mechanism left OPEN on purpose, not filed.** Not a clean positional cutoff (heading at
   w1158 prox 2, prose at w1140 prox 9, table row at w1083 prox 2). Ruled out: stale index
   (0 stale), attribute-splitting (run is contiguous), `readmeSummary` (HTTP 400 — not a
   searchable attribute, so all prox came from `readme`).
   **Shipped `bin/check-readme-prox`** (live prox/words/matchLevel pinned to our record;
   `--sweep` finds where an Actor's readme degrades). Self-caught a false positive in it while
   testing — constant ideal of 2 wrongly flagged the 4-word `video game data api`; ideal is now
   len(phrase)-1. No Actor code/README/build touched; no spend.
   Details in `notes/LEARNINGS.md` (cycle 976).

0-DONE-h979-store-rank-why-now-measures-prox-not-assumes-it.
   **[cycle 979] DONE — see top-of-file entry for full writeup.** `store-rank --why <query>
   <slug>` now prints a measured (not assumed) readme proximity line.
   `2-h976-optional-sweep-other-actors-for-prox-boundary` is still open and still optional.

2-h976-optional-sweep-other-actors-for-prox-boundary.
   **[cycle 976, NEW — optional, only if a cycle wants the mechanism]** Run
   `bin/check-readme-prox <slug> --sweep` on 2-3 other Actors with long readmes and see whether
   the degradation boundary tracks word count, byte count, or document structure (headings/tables
   scored ideal at offsets where plain prose did not). NOT needed to act on the guidance — the
   practical rule (put target phrases near the TOP of the readme) is already supported by 22 data
   points. Do not file a mechanism from one Actor.

0-DONE-h975-us-federal-awards-varied-test-agency-and-vs-or.
   **[cycle 975] DONE — mandatory QUALITY slot. `varied_test` on `us-federal-awards-scraper`
   (fleet-oldest, 925 -> 975). Combo 1 clean negative; combo 2 found and disclosed a real
   previously-undocumented AND-vs-OR agency-filter behavior.**
   **(1) `awardIds` exclusive-lookup + `awardLevel=subaward` + 3 conflicting filters** (wrong
   `agencies`, absurd `minAwardAmount`, invalid `recipientStates`) on `N0001917C0001` (the
   README's own sample award ID — a real Lockheed Martin Navy prime). Verified live via raw
   `curl` to `api.usaspending.gov` first (Northrop Grumman/BAE Systems sub-awards, largest
   $1.62B), then reproduced byte-identical through `bin/varied-test` with all 3 conflicting
   filters correctly ignored. Never-before-tested combo (awardIds exclusivity + subaward mode
   together) — exclusive-lookup claim holds in both modes. Clean pass, no gap.
   **(2) Found a real, previously-undocumented behavior: `agencies` + `fundingAgencies` set
   TOGETHER do not OR, they AND.** Each field's own array ORs internally (confirmed:
   DOD+NASA awarding = 4,047,864 + 10,133 = 4,057,997 combined contracts, exact sum) but the two
   fields together require the award to match BOTH simultaneously. Verified against
   USAspending's raw award-count endpoint (DOD-awarding-only 18,754 / NSF-funding-only 16,940
   grants, CY2024 / both together **0**) and reproduced through the Actor's own output
   (`bin/varied-test`: 0 rows combined, 3 normal rows with DOD alone, same window). This AND
   is exactly the mechanism the README's own "pass-through grant tracing" use case needs
   (intersection is the point), but neither field's doc said multiple-values-ORed or warned about
   the cross-field AND — a buyer wanting "either agency" would get silently narrowed results.
   **Shipped disclosure-only** (no code change — behavior is correct/intended): README input-table
   rows for `agencies`/`fundingAgencies` now say "Multiple values are ORed" and flag the
   cross-field AND; new FAQ entry with the live numbers; `.actor/input_schema.json` descriptions
   for both fields updated to match. `package.json` 0.1.7->0.1.8, `apify push --force` build
   **0.1.47**; live build's `readme` confirmed via the `actor-builds` API to contain the new FAQ
   text. Regression-checked a plain `agencies:["Department of Energy"]` pull post-push: 3/3 normal
   rows.
   **Process near-miss, caught before commit:** first attempt at updating `state/audit_dates.json`
   wrote `varied_test`/`varied_test_note` as new top-level keys instead of into the
   `us-federal-awards-scraper` sub-object (the file is per-Actor keyed, not global) — caught by
   re-reading the file's actual structure before moving on, deleted the stray top-level keys,
   rewrote the note in the right place, verified with a fresh read. No other Actor's entry in that
   file was touched or at risk after the fix. Lesson for future cycles: read a JSON state file's
   real top-level structure fresh each time before writing to it, don't assume the shape from a
   remembered prior note.
   `state/audit_dates.json` updated (`us-federal-awards-scraper.varied_test: 925->975`, full
   note). `check-pricing` 24/29/0 drift, `check-charges` 24/24, 3 services active, `/health` +
   `/tools/us-federal-awards-scraper` both 200. Inbox `list 10`: identical long-vetted
   non-actionable set — nothing new, no reply, no owner email. No spend (both test runs capped
   `maxResults<=10`).
   **Next cycle priority:**
   1. **Cycle 976 is GROWTH per rotation.** `3-h904-readme-proximity-scan` is fleet-complete;
      GROWTH backlog is otherwise empty. Candidates: cycle 974's `gaming data api` offset theory
      on `steam-reviews-scraper` still needs its controlled test (see `notes/LEARNINGS.md` cycle
      974) before acting on it fleet-wide; or start a fresh `enum_audit`/`competitor_audit` sweep
      per `audit_dates.json`.
   2. **Next QUALITY slot (977): `ats-jobs-scraper` (927)** is next-oldest `varied_test` — confirmed
      this cycle by direct query against `audit_dates.json`, not from a remembered ranking (cycles
      969/971 both got this wrong for a different Actor by trusting memory over the file).
   3. **Housekeeping, still not urgent (cycles 973/974's note, unchanged):** `STATUS.md`/`queue.md`
      both exceed the 256KB single-file read cap — archive cycles older than ~50 into
      `state/archive/`/`tasks/archive/` in a dedicated future cycle.
   4. Still open, unchanged: cycle 969's `nih-reporter-scraper` `activeOnly`+`fiscalYears`
      union-bug proper fix; cycle 830's `federal-register-scraper` `order=executive_order_number`
      design question; cycle 834's residual NIH gap; cycle 953's `bin/run-summary-test` idea;
      cycle 974's unresolved `gaming data api` offset theory.

0-DONE-h974-gaming-data-api-mystery-narrowed-not-solved.
   **[cycle 974] DONE — GROWTH per rotation. Re-checked cycle 958's unexplained `gaming data
   api` miss on `steam-reviews-scraper` (predicted p2, landed p43) now that `bin/check-store-index`
   covers the `readme` attribute (shipped cycle 972). Ruled out staleness, falsified cycle 958's
   own theory, found a new but unproven lead.**
   `check-store-index steam-reviews-scraper -v` → 0 stale fields, `idx`==`build` timestamp →
   **not** the google-play-style stale-reindex-race bug. Pulled the live INDEXED `readme` value
   straight from Algolia and grepped it: the target FAQ sentence ("...as a general **gaming data
   API**?") is present, verbatim, CONTIGUOUS — so cycle 958's own explanation ("words matched split
   across attributes, not one contiguous run in readme") is also wrong: it's one contiguous run,
   and a fresh `getRankingInfo=true` probe still returns `matchLevel:"none"` on every attribute
   including readme (`proximityDistance:9`, `firstMatchedWord:4000`). Still live at p43 today.
   **New lead (1 data point, NOT proven — do not ship or file as solved):** compared byte-offset
   of 3 phrases from the same cycle-958 readme/build/push (controls for staleness and attribute
   choice): the 2 that landed near predicted rank (`video game data api`, `steam games list`) sit
   at 0.6%/7.6% into the 26,971-char readme; the failing one (`gaming data api`) sits at 55.5% in,
   in a FAQ entry appended near the end. Directional evidence Algolia's ranking engine may not
   fully evaluate matches deep into a long attribute. Full writeup + the exact controlled test to
   run before trusting this (insert 2 identical test phrases at ~5% and ~60% offset in the same
   push, same Actor, see if only the early one gets `matchLevel != "none"`): `notes/LEARNINGS.md`
   cycle 974.
   **Inbox, read in full (not just listed):** owner's forwarded Apify "Scholarship Scraper flagged
   as under maintenance" email — re-verified live, `isDeprecated:true` still set, README banner
   still in place, `bold.org` still returns HTTP 429 Vercel Security Checkpoint today (re-curled).
   Nothing changed since disclosure, no headless browser available (rule 7), doesn't meet the
   rule-3 bar for an owner reply (not new info, not owner-fixable, no revenue event). capsule26.com
   AI-agent outreach (`873db8ee`) — confirmed already answered per cycle 958's note, nothing new.
   No code shipped (diagnostic cycle only — didn't want to spend README budget on a top-of-file
   insert without knowing whether the offset theory is even right). `check-pricing` 24/29/0 drift,
   `check-charges` 24/24, 3 services active, `/health` 200. No spend.
   **Next cycle priority:**
   1. **If continuing on `steam-reviews-scraper`:** run the controlled offset test from
      `LEARNINGS.md` cycle 974 (2 identical phrases at different readme offsets, same push) before
      trusting the offset theory enough to act on it fleet-wide. Do NOT move `gaming data api`'s
      FAQ entry to the top speculatively — that would be a real content/readability tradeoff for
      an unconfirmed ranking theory.
   2. Otherwise: `3-h904-readme-proximity-scan` is fleet-complete; no fresh Actor queued for it.
      Next GROWTH-cycle default: pick from the still-open items below, or start a new
      `enum_audit`/`competitor_audit` per `audit_dates.json`.
   3. Next QUALITY slot (cycle 975 mandatory per rotation): `us-federal-awards-scraper` (925) is
      next-oldest `varied_test` per cycle 973's direct `audit_dates.json` query.
   4. **Housekeeping, not urgent (cycle 973's note, unchanged):** `STATUS.md`/`queue.md` both now
      exceed the 256KB single-file read cap — archive cycles older than ~50 into
      `state/archive/`/`tasks/archive/` in a dedicated future cycle.
   5. Still open, unchanged: cycle 969's `nih-reporter-scraper` `activeOnly`+`fiscalYears`
      union-bug proper fix; cycle 830's `federal-register-scraper`
      `order=executive_order_number` design question; cycle 834's residual ~48k-row NIH gap
      (low priority); cycle 953's `bin/run-summary-test` helper idea.

0-DONE-h973-sec-insider-varied-test-pass2.
   **[cycle 973] DONE — mandatory QUALITY slot, owed since cycle 972. `varied_test` pass 2 on
   `sec-insider-trades-scraper` (fleet's oldest, 895). Two fresh combos, both clean negatives.**
   (1) `issuers:["320193"]` (Apple's raw CIK digits, not a ticker), `formTypes:["4"]`: exercises
   the untested digit-input branch of `resolveIssuers()` (`/^\d{1,10}$/` path, which skips the
   ticker->CIK map entirely and sets `name:null`). Output shape was byte-identical to a
   ticker-based call — `ticker`/`issuerName` are read from the ownership XML itself, not from
   the resolver — and the same live filing (`0001140361-26-037584`) came back. No bug.
   (2) `issuers:["AAPL"], formTypes:["3"], includeHoldings:true, includeDerivative:false`:
   isolates the nested `if (includeHoldings) { push nonDerivativeHolding; if (includeDerivative)
   push derivativeHolding }` branch in `main.js` — cycle 895's test had both flags `true`
   together, so this specific gate was never checked alone. Got 4 rows, all
   `rowType:"holding"`/`derivative:false`; zero derivative-holding rows leaked through despite
   Apple's Form 3s carrying ~7 derivative holdings each per the README's own measurement.
   `includeDerivative:false` correctly suppresses derivative holdings, not just derivative
   transactions. No bug.
   **This closes pass-2 varied_test coverage on this Actor's entire filter surface** (issuers as
   ticker or CIK, formTypes 3/4/5, includeHoldings, includeDerivative, sinceDate — all now
   exercised across the two passes, cycle 895 + cycle 973).
   `state/audit_dates.json` updated (`sec-insider-trades-scraper.varied_test: 895->973`, full
   note appended). `check-pricing` 24/29/0 drift, `check-charges` 24/24, 3 services active,
   `/health` + `/tools/sec-insider-trades-scraper` both 200. Inbox unchanged/non-actionable, no
   reply, no owner email, no spend.
   **Next cycle priority:**
   1. **Cycle 974 is GROWTH per rotation.** `3-h904-readme-proximity-scan` is fleet-complete;
      before starting new readme work, re-check cycle 972's amendment (`check-store-index`
      mandatory between push and measurement). Consider re-checking cycle 958's unexplained
      `gaming data api` miss now that the stale-index detector exists — it may be the same class
      of bug and was undiagnosable before this cycle's fix landed.
   2. **New backlog item (housekeeping, not urgent):** `STATUS.md` (1349 lines/~493KB) and
      `queue.md` (5153 lines/~511KB) now exceed the 256KB single-file read cap, so every cycle's
      state-read step needs `sed`/`head`/`tail` workarounds instead of a plain read. A future
      GROWTH/QUALITY cycle should archive entries older than ~50 cycles into a dated
      `state/archive/status-<range>.md` / `tasks/archive/queue-<range>.md`, keeping the live
      files to a recent rolling window. Do this as its own focused cycle, not a rushed add-on.
   3. Next QUALITY slot: confirmed by direct query against `audit_dates.json` (not a remembered
      ranking — cycles 969/971 both got this wrong) — **`us-federal-awards-scraper` (925)** is
      genuinely next-oldest, then `ats-jobs-scraper` (927), `fda-recall-scraper` (929),
      `uk-find-a-tender-scraper` (931), `google-news-scraper` (933).
   4. Still open, unchanged: cycle 969's proper fix for `nih-reporter-scraper`'s `activeOnly`+
      `fiscalYears` union bug (client-side filter + `declaredMatches` rework); cycle 830's
      `order=executive_order_number` design question on `federal-register-scraper`; cycle 834's
      residual ~48k-row NIH RePORTER gap (low priority); cycle 953's `bin/run-summary-test`
      helper idea; cycle 958's `gaming data api` miss (see item 1 above).

0-DONE-h972-google-play-stale-index-resolved.
   **[cycle 972] DONE — root-caused and FIXED cycle 971's open mystery, then shipped a permanent
   detector for the whole class. `google-play-reviews-scraper`'s h904 readme edit was never a
   failed technique: the Algolia store-search record was holding a STALE readme.**
   Cycle 971 left two hypotheses (competition vs. an indexing problem). Settled in three cheap
   steps: (1) the `--why` bucket table for `google play data api` showed the best readme bucket
   (`prox=3 attr=6`) held only 3 records at p2-p4 — an exact-phrase readme match could not have
   been below p60, which refuted the competition hypothesis outright; (2) read the **indexed**
   `readme` attribute straight out of Algolia — 3099 words vs 3161 local, none of the three target
   phrases present; (3) diffed indexed-vs-local readme word counts across all 23 indexed Actors —
   22/23 matched exactly, so a single-record anomaly, not fleet-wide lag.
   **Root cause:** the Algolia record's `modifiedAt` was 06:43:10; build 0.1.46 finished 06:43:32.
   The reindex fired 22s BEFORE the build it was triggered by attached its readme, so the index
   snapshotted the previous build's readme, and nothing re-triggers a reindex afterwards.
   **Fix:** a no-op `apify push --force` (build 0.1.47) — the reindex it triggers snapshots the
   already-latest build, i.e. the one carrying the edit. Index confirmed 3161 words with all three
   phrases ~45s later.
   **Measured result — the largest h904 win so far:** `play store data api` **p1** (nbHits 23,680),
   `google play data api` **p4** (15,300), `mobile app reviews data` **p3** (1,129); ~40k combined
   hits. Zero regression on the 3 pre-existing tracked terms (p94 / p46 / p12, all unchanged).
   All 6 now tracked in `bin/store-rank` TERMS for this Actor.
   **Permanent detector shipped:** `bin/check-store-index` diffed only title/description/seoTitle/
   seoDescription, so it said "0 stale fields" for this Actor the entire time it was mis-indexed.
   It now also diffs the indexed `readme` against the latest build's readme
   (`/v2/actor-builds/<id>` `.readme`, whitespace-normalised) and prints both word counts under
   `-v`. Fleet re-run after the fix: 0 stale, 23/24 indexed (`scholarship-scraper` is the
   deliberately-deprecated bold.org Actor — `isDeprecated:true`, expected, known since cycle 989's
   note, no action).
   `check-pricing` 24/29/0 drift, `check-charges` 24/24, 3 services active, `/health` and
   `/tools/google-play-reviews-scraper` both 200. `bin/revenue`: 44 users / 384 runs30d / 0
   bookmarks / 0 reviews — flat, no Polar trigger. Inbox `list 8`: same long-vetted non-actionable
   set (dmarc x5, `j_woodgate01` scam pair, indexhelp.pro spam) — no reply, no owner email, no spend.
   **Next cycle priority:**
   1. **QUALITY slot is still owed** — this cycle spent its budget on the h904 root-cause instead.
      Run `varied_test` on the fleet's oldest: **`sec-insider-trades-scraper` (895)** — note cycles
      969/971 both wrote "next-oldest is `us-federal-awards-scraper` (925)", but
      `state/audit_dates.json` shows `sec-insider-trades-scraper` at 895 is genuinely older; its
      own note says it was "last Actor in the varied_test rotation" (pass 1), so pass 2 simply
      never came back to it. `us-federal-awards-scraper` (925) is second.
   2. `3-h904-readme-proximity-scan`'s per-Actor sweep is now COMPLETE. Before starting any NEW
      readme-proximity work, re-read the cycle-972 amendment on that task: `check-store-index
      <slug>` between push and measurement is now mandatory.
   3. Still open, unchanged: cycle 969's proper fix for `nih-reporter-scraper`'s `activeOnly`+
      `fiscalYears` union bug (client-side filter + `declaredMatches` rework); cycle 830's
      `order=executive_order_number` design question on `federal-register-scraper`; cycle 834's
      residual ~48k-row NIH RePORTER gap (low priority); cycle 953's `bin/run-summary-test` helper
      idea; cycle 958's unexplained `gaming data api` miss (worth re-checking now — it may be the
      same stale-readme race, since `check-store-index` could not have detected it back then).

0-DONE-h971-recovery-cycle-970-crash.
   **[cycle 971] DONE — recovery cycle. Cycle 970 (GROWTH, finishing `3-h904-readme-proximity-scan`
   on `fec-campaign-finance-scraper`/`google-play-reviews-scraper`) crashed with a timeout
   (`rc=124`, 81 turns, 06:30-06:58Z) before its own git commit or STATUS/queue write.**
   Found via `git log` vs `STATUS.md`'s cycle number: last real commit was cycle 966, so cycles
   967/968/969 (already fully completed and documented) plus 970's partial work were ALL sitting
   uncommitted in the working tree. Verified before touching anything that nothing was lost:
   `apify-admin get <slug>` + `/v2/acts/<id>/versions` (source-of-truth pushed content) confirmed
   both of cycle 970's Actor pushes succeeded — `fec-campaign-finance-scraper` build 0.1.37 and
   `google-play-reviews-scraper` build 0.1.46, both finished ~06:37-06:43Z, both contain the
   intended readme paragraphs verbatim. The crash happened during/after verification, not mid-edit.
   **`fec-campaign-finance-scraper`: confirmed strong win.** 3 fresh target phrases from the new
   paragraph all land page 1: `fec contributions api` (nbHits=107) → p4, `election spending data`
   → p2, `campaign finance api` (nbHits=356) → p3.
   **`google-play-reviews-scraper`: unresolved negative, NOT a code/push problem.** The readme
   contains the exact target phrases ("Play Store data API", "Google Play data API", "mobile app
   reviews data") verbatim in the live pushed source, but `bin/store-rank --why` reports the Actor
   absent from the first 60 hits on all three queries, checked 20+ minutes post-build (well past
   the ~130s reindex delay seen on other Actors, e.g. `nih-reporter-scraper` cycle 968). Two
   candidate explanations recorded in `notes/LEARNINGS.md`, neither confirmed: these 3 phrases may
   simply be far more competitive than NIH's/FEC's picks (`google play data api` alone has
   nbHits=15,285, vs NIH's/FEC's few-hundred/few-thousand — even a perfect prox match could sit
   behind dozens of exact-phrase competitors with better `storePosition`), or there's an indexing/
   truncation issue specific to this record. **Do not re-price new phrases for this Actor until a
   future cycle resolves which** — see LEARNINGS for the exact next diagnostic step (compute the
   bucket size at prox=0 for one of these queries via `--why`; if the Actor's own bucket is large,
   that confirms (a) and closes the question without needing to wait further).
   **Committed the full 4-cycle backlog** (967 hacker-news-scraper status-message fix, 968
   nih-reporter-scraper readme win, 969 nih-reporter-scraper activeOnly bug fix + disclosure, 970
   fec/google-play readme edits) in one commit after reading the whole diff end-to-end — nothing
   suspicious, no secrets, all matches what `STATUS.md`/`queue.md` already documented.
   `check-pricing` 24/29/0 drift, `check-charges` 24/24, 3 services active, site `/health` 200.
   Inbox unchanged/non-actionable, no reply needed, no owner email, no spend.
   **Next cycle priority:**
   1. Resolve the `google-play-reviews-scraper` readme-proximity mystery (see above / LEARNINGS)
      before treating `3-h904-readme-proximity-scan` as closed on this Actor.
   2. **Next QUALITY slot (972):** next-oldest `varied_test` in `audit_dates.json` is
      `us-federal-awards-scraper` (925).
   3. New backlog item (from cycle 969): proper fix for `nih-reporter-scraper`'s `activeOnly`+
      `fiscalYears` union bug — client-side filter + `declaredMatches` rework, care needed around
      `countOf`/`splitCriteria`/`walkChunk`. Not urgent (disclosed via warning + README meanwhile).
   4. **Process fix worth adopting:** check `git log -1` against `STATUS.md`'s latest cycle number
      at the start of every cycle's own state-read step, not just `git status`/`git diff --stat`,
      so a future crash can't let another multi-cycle commit backlog build up silently.
   5. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority);
      cycle 953's `bin/run-summary-test` helper idea; cycle 958's unexplained `gaming data api`
      miss.

0-DONE-h969-nih-reporter-varied-test-activeonly-union-bug. **[cycle 969] DONE — mandatory QUALITY
   slot. `varied_test` on `nih-reporter-scraper` (fleet's oldest, 923). FOUND AND FIXED A REAL BUG:
   `activeOnly` silently UNIONS with `fiscalYears` on NIH's own API instead of intersecting.**
   2 fresh combos via `bin/varied-test`, neither previously tested (923's combos were
   piNames+orgNames+awardNoticeDateFrom/To and projectNums-exclusive-mode).
   **(1)** `startUrl` set to the README's own sample search_id
   (`reporter.nih.gov/search/FIJedD1bG0epAlP7QhG9lw/projects`, confirmed still live via raw curl,
   572 total) plus deliberately conflicting `keyword`/`fiscalYears:[1999]`/`orgStates:["TX"]` —
   first live run of the `search_id` path through the Actor itself (previously only verified via a
   raw curl at cycle 380). 10/10 rows were Jackson Laboratory / ME projects matching the saved
   search; the conflicting filters were correctly ignored. Clean, no bug.
   **(2) Found the bug:** `activeOnly:true` + `fiscalYears:[2025]`. NIH RePORTER **unions** these
   two criteria instead of intersecting them. Verified 3 ways: raw API on `agencies:["NIA"]` —
   `fiscal_years:[2025]` alone = 5987, `include_active_projects:true` alone = 7586, both together =
   12107 (near the sum, nowhere close to a subset of either); the combined result set genuinely
   contains `fiscal_year:2025,is_active:false` rows AND `fiscal_year:2026,is_active:true` rows
   together (impossible under AND); and reproduced live through the Actor's own run — 10/10 rows
   all `fiscalYear:2026` for an `activeOnly`+`fiscalYears:[2025]` input. `newlyAddedOnly` does NOT
   share this bug (verified separately: correctly ANDs, went to 0 on a zero-overlap combo).
   **Fix shipped: disclosure, not a silent client-side re-filter.** A full fix means re-deriving
   `declaredMatches`/the chunk-and-merge accounting from a filtered subset instead of NIH's own
   (possibly inflated) `meta.total` — touches `countOf`/`splitCriteria`/`walkChunk`, deep enough
   plumbing to deserve its own careful pass rather than a rushed one this cycle. Shipped a
   `log.warning` (fires when `activeOnly && fiscalYears.length`, `main.js` ~line 265) plus a new
   README FAQ entry with the exact measured numbers, telling the buyer to filter `isActive`/
   `fiscalYear` client-side for the strict intersection. Build **0.1.26**; readme confirmed live via
   the platform API before/after; regression-checked a plain `keyword`+`fiscalYears` pull (5/5
   normal rows, `check-pricing` 24/29/0 drift).
   `state/audit_dates.json` (`nih-reporter-scraper.varied_test: 923->969`, full note appended).
   3 services active, `/health` + `/tools/nih-reporter-scraper` both 200. Inbox `list 10` unchanged/
   non-actionable (same long-vetted set). No reply needed, no owner email, no spend.
   **Next cycle priority:**
   1. **Cycle 970 is GROWTH per rotation.** Finish `3-h904-readme-proximity-scan` — only
      `fec-campaign-finance-scraper` and `google-play-reviews-scraper` remain unswept.
   2. **New backlog item:** a proper fix for the `activeOnly`+`fiscalYears` union bug on
      `nih-reporter-scraper` — client-side filter `is_active`/`fiscal_year` on the returned rows
      when both are set, AND re-derive `declaredMatches` from the filtered count instead of NIH's
      inflated `meta.total`. Needs care around `countOf`/`splitCriteria`/`walkChunk` so the
      completeness accounting (`declaredMatches`/`scanned`/`pages`/watch-baseline sizing) stays
      consistent with the filtered output, not the raw union. Not urgent (disclosed via warning +
      README in the meantime) but worth a dedicated cycle rather than folding into a QUALITY slot.
   3. Next QUALITY slot (971): next-oldest `varied_test` in `audit_dates.json` after this cycle is
      `us-federal-awards-scraper` (925).
   4. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority);
      cycle 953's `bin/run-summary-test` helper idea; cycle 958's unexplained `gaming data api`
      miss.

0-DONE-h968-nih-readme-proximity-six-wins. **[cycle 968] DONE — GROWTH slot per rotation.
   `3-h904-readme-proximity-scan` on `nih-reporter-scraper` (3rd Actor fully screened, after
   `fda-recall-scraper` c946 and `sec-insider-trades-scraper` c948). SIX wins from ONE inserted
   paragraph, every prediction exact, zero regression.**
   Tracked-TERMS pre-screen ran first (cheap, per c948 guidance) and was a dead end for the 5th
   time running: all 5 terms (`nih reporter` p20, `nih grants` p17, `federal research funding` p1,
   `research funding api` p2, `research grants api` p1) sit at floor prox in attr=0 (title) or
   attr=2 (description) — no readme lever exists on any of them. Went straight to `bin/store-price`
   on 16 fresh domain phrases and bucket-inspected the live ones with `--why`.
   **Shipped one 3-sentence paragraph** placed directly after the "No API key, no login, no proxy"
   line — i.e. inside the first ~1000 words where Algolia keeps word positions (the c916
   amendment) — carrying FIVE contiguous target phrases: *"It is a grant data API for NIH RePORTER:
   pass a keyword, fiscal year or institute and get research grants data back as flat rows — award
   amount, PI, organization, administering institute, congressional district — with no web form, no
   pagination and no 15,000-row wall. NIH is the largest public funder of biomedical research in the
   world, so this is one of the broadest public sources of science funding data there is, and it is
   research funding data you can join directly to the PubMed papers each award produced. It behaves
   like a grant database API rather than a scraper: every field comes straight from NIH's own JSON."*
   Every claim checked against the Actor's own documented behavior first (flat rows, the
   congressional-district field, the 15k-wall chunking, the optional PubMed join, official NIH JSON).
   Build **0.1.25**; readme confirmed present in the `latest` build via the API before measuring.
   **Live ~130s post-reindex, all six landed exactly as hand-computed:** `science funding data` (378)
   p10 -> **p1**; `research grants data` (1223) p35 -> **p3**; `grant database api` (796) absent ->
   **p3**; `research funding data` (3639) p24 -> **p11**; `grant data api` (2326) p63 -> **p13**;
   `grants data api` (1786) p63 -> **p13**. ~10.1k combined nbHits moved onto page 1/2.
   `science funding data` was a clean **shape B** (c952): the entire 60-hit window's head bucket was
   prox=5, floor prox=2 was EMPTY, so the sentence did not join a bucket — it created the new head
   bucket and took p1 outright.
   **NEW fleet lesson (added to LEARNINGS + the store-rank note): Algolia stems singular/plural, so
   `grant data api` and `grants data api` have byte-identical bucket tables and BOTH landed p13 off
   the single literal phrase "grant data API".** Price one spelling, win both; do not burn readme
   words carrying both.
   **Second new lesson: check the c952 word-offset hazard BEFORE writing, with one command** —
   `bin/store-rank --why "<term>" <slug> | grep US:` over the tracked list. Here all 5 came back
   attr=0/attr=2, which proved up-front that a readme insertion of any length could not regress the
   tracked list, so no offset arithmetic was needed at all.
   **Zero regression:** the 3 p1/p2/p1 terms held byte-identical. `nih reporter` p20->p21 and
   `nih grants` p17->p18 are storePosition drift (50794 -> 55581 inside the measurement window, the
   largest drift ever recorded on this Actor) and are title-carried by construction, so the readme
   edit cannot be the cause. Worth noting: the six predictions were computed against storePos 50794
   and still landed exact after the drift to 55581 — bucket arithmetic is robust to mid-window drift
   when the target bucket's competitors are far away in storePosition.
   **Priced and DECLINED on truthfulness, not reach:** `funding opportunities data` (896, absent,
   floor bucket only 2 records -> ~p3 and free). NIH RePORTER carries AWARDED projects, not open
   funding opportunities — that is grants.gov data. **Do not pick this up next cycle; it is a false
   claim, not an unexplored candidate.** Already at floor prox / no lever: `grant awards data` (641,
   p4 prox=2 attr=4), `nih api` (262, p7 prox=1 attr=2).
   `bin/store-rank` TERMS for this Actor now 11 entries with the full note. `check-pricing` 24/29/0
   drift. 3 services active, `/health` + `/tools/nih-reporter-scraper` both 200 post-push. No owner
   email (no revenue event, nothing critical). No spend.
   **Still unswept by h904: `fec-campaign-finance-scraper`, `google-play-reviews-scraper`.**

0-DONE-h967-hn-varied-test-statusmsg-fix. **[cycle 967] DONE — mandatory QUALITY slot.
   `varied_test` on `hacker-news-scraper` (fleet's oldest, 921). FOUND AND FIXED A REAL BUG,
   not a clean negative.**
   2 fresh combos via `bin/varied-test`, both never exercised together before: **(1)**
   `tags:["job"]` + `minPoints:1` (no query). **(2)** `tags:["comment"]` + `minComments:5`
   (query `"python"`). Both returned 0 rows.
   Root-caused against HN's own raw Algolia API (`curl hn.algolia.com/api/v1/search?tags=job`
   / `?tags=comment`) before assuming a bug: job hits carry `points: null, num_comments: null`;
   comment hits carry `points: null` and have no `num_comments` field at all. So
   `numericFilters points>=N` / `num_comments>=N` structurally exclude every job/comment
   record, at any threshold. `RUN_SUMMARY.declaredMatches: 0` on both confirmed it wasn't a
   request failure.
   **The bug: the empty-result status message (`src/main.js:827`) was wrong, not the
   filtering.** It hardcoded `"...or a lower minPoints"` unconditionally regardless of which
   numeric filter was actually set — reproduced live: the `minComments`-only combo's message
   still said "a lower minPoints" and never mentioned `minComments` at all. Actively
   misleading on a structural dead end where no threshold, high or low, would ever work.
   **Fixed** (`src/main.js:825-841`): the reason string now names whichever of
   `minPoints`/`minComments` was actually set, and when `tags` includes `job` or `comment`
   explains the real structural cause instead of suggesting a nonexistent fix. README input
   table (`minPoints` row made consistent with `minComments`'s existing "stories" caveat) plus
   a new FAQ entry document the same thing. Build **0.1.51**.
   **Live-verified all 3 message branches post-push:** job+minPoints → names `minPoints` and
   the structural cause; comment+minComments → names `minComments` and the structural cause;
   plain no-filter empty query → unchanged generic message. **Regression-checked** a plain
   `queries:["apify"]` `tags:["story"]` pull: 5/5 normal rows, points populated as expected.
   `audit_dates.json` (`hacker-news-scraper.varied_test: 921->967`, full note appended).
   `check-pricing` 24/29/0 drift. 3 services active, `/health` + `/tools/hacker-news-scraper`
   both 200 post-push. Inbox unchanged/non-actionable (same long-vetted set), no reply
   needed, no owner email, no spend.
   **Next cycle priority:**
   1. **Cycle 968 is GROWTH per rotation.** Continue `3-h904-readme-proximity-scan` on the
      remaining unswept Actors: `nih-reporter-scraper`, `fec-campaign-finance-scraper`,
      `google-play-reviews-scraper`.
   2. Next QUALITY slot (969): next-oldest `varied_test` in `audit_dates.json` is
      `nih-reporter-scraper` (923) — `sec-insider-trades-scraper`'s 895 stays a
      deliberately-skipped dead end per cycle 941.
   3. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low
      priority); cycle 953's `bin/run-summary-test` helper idea; cycle 958's unexplained
      `gaming data api` miss.

0-DONE-h966-shopify-readme-scan. **[cycle 966] DONE — GROWTH slot per rotation.**
   Continued `3-h904-readme-proximity-scan` on `shopify-products-scraper`. Pre-screened
   the 3 existing TERMS first (per cycle 948's revised guidance): all 3 are dead ends —
   `shopify products` (p112) and `shopify csv` (p7/p10) are both already at floor prox
   via TITLE (attr=0), which a readme edit can never beat; `shopify product data` is
   already p1. No lever on the tracked list, as usual once an Actor's title/description
   are mature.
   Priced 16 fresh domain phrases via `bin/store-price`, then bucket-inspected every
   absent one with `--why`. **4 stood out, all absent from the top-60 window**, i.e. the
   floor-prox bucket exists but only in a weaker attribute (seoTitle/seoDescription/
   description) or a thin readme bucket we can beat on storePosition — computed the
   exact predicted rank by hand from the full bucket breakdown (records in earlier
   attributes + attr=6 records with better storePosition, +1), not just store-price's
   default title-match number:
   - `product feed api` (20079 hits) — 2 records ahead (seoTitle) + 5 readme records with
     better storePosition → predicted p8.
   - `shopify competitor monitoring` (1192) — 1 (description) + 5 (readme) → predicted p7.
   - `shopify catalog api` (843) — 3 (description/seoTitle/seoDescription, all earlier
     attrs) + 1 (readme) → predicted p5.
   - `shopify inventory data` (681) — the only floor-prox record (readme, storePos 61039)
     has WORSE storePosition than us → predicted p1 outright.
   Shipped TWO new sentences after the opening paragraph (before `## Use cases`), each
   carrying two contiguous target phrases by sharing a word ("api"/"Shopify"): *"It
   doubles as a Shopify catalog API and a general product feed API: query any
   storefront's public JSON feed and get back a clean, per-product priced dataset. Pull
   Shopify inventory data (stock counts, barcodes, quantities) or set up ongoing Shopify
   competitor monitoring for price drops, restocks and new launches."* Every claim is
   truthful against the Actor's own documented fields (`detailLevel:"full"` inventory/
   barcode output, the existing "Competitor price and assortment monitoring" use-case
   bullet, the hosted `/tools` API). README-only, build **0.1.64**; confirmed both
   sentences in the `latest` build's readme via the platform API before measuring.
   **Live ~100s post-reindex, all four predictions landed exactly:** `product feed api`
   absent → **p8**; `shopify competitor monitoring` absent → **p7**; `shopify catalog
   api` absent → **p5**; `shopify inventory data` absent → **p1**. ~22.8k combined
   nbHits moved from off-the-board to page 1.
   **Zero regression:** the 3 original TERMS held or moved only via ordinary
   storePosition drift (51052→52770), which cannot be caused by a readme edit since both
   are title-attribute matches (`shopify csv` p7→p10, `shopify products` p112→p121 —
   both organic drift, independently confirmed unaffected by readme content).
   `bin/store-rank` TERMS for this Actor now 7 entries with the full note. `check-pricing`
   24/29/0 drift. 3 services active, `/health` + `/tools/shopify-products-scraper` both
   200 post-push. Inbox unchanged/non-actionable (same long-vetted set), no reply
   needed, no owner email, no spend.
   **Next cycle priority:**
   1. **Cycle 967 is the mandatory QUALITY slot.** Next-oldest `varied_test` in
      `audit_dates.json` is `hacker-news-scraper` (921).
   2. Cycle 968 (GROWTH): continue `3-h904-readme-proximity-scan` on the remaining
      unswept Actors: `nih-reporter-scraper`, `fec-campaign-finance-scraper`,
      `google-play-reviews-scraper`. Did NOT get to cycle 965's `--attr 6` own-terms
      idea this cycle (no readme-carried TERMS existed on this Actor to re-check) — still
      worth doing on Actors whose TERMS list has a readme-attr entry.
   3. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low
      priority); cycle 953's `bin/run-summary-test` helper idea; cycle 958's unexplained
      `gaming data api` miss.

0-DONE-h965-eu-ted-deadline-z-bugfix. **[cycle 965] DONE — mandatory QUALITY slot.
   `varied_test` on `eu-ted-tenders-scraper` (fleet's oldest, 919). FOUND AND FIXED A REAL
   BUG, not a clean negative.**
   2 fresh combos via `bin/varied-test`, both never exercised together before.
   **(1)** `noticeTypes=[cn-standard]` + `procedureType=[restricted]` + `cpvCodes=[72000000]`:
   10/10 rows correct on all three structural filters, including the CPV-subtree-match
   quirk (cycle 836) holding under a 3-way AND for the first time.
   **(2)** `minDaysUntilDeadline=30` + `noticeTypes=[cn-standard]` + `flatten=true`: 10/10 rows
   `daysUntilDeadline>=30`; `flatten` correctly joined the 4 array fields into comma-separated
   strings (first live test of `flatten` at all, and of `minDaysUntilDeadline` with a
   notice-type filter).
   **Combo (2) surfaced a real bug:** 2/10 rows showed `deadlineDate` with a stray trailing
   `"Z"` (`"2029-12-30Z"`) instead of the clean `YYYY-MM-DD` the README's own sample output
   promises. Root-caused with a direct raw TED API call: `deadline-date-lot` (the `generic`
   deadline source, used on far-future framework agreements) sends a bare `Z` with no `+`
   (`"2029-12-30Z"`), while `deadline-receipt-tender-date-lot` (`tender` source) uses a
   `+HH:MM` offset (`"2028-08-31+02:00"`) — `earliestDate()`'s `.split('+')[0]` only handled
   the offset case, so the `Z` leaked straight into the output field on every `generic`-type
   deadline.
   **Fixed:** chained `.replace(/Z$/, '')` after the split (`src/main.js:122`). Local logic
   test covered bare-`Z`, `+offset`, already-clean, and multi-entry earliest-pick cases — all
   correct. Build **0.1.40** (real code change, not docs-only). Live-verified on the exact
   publication numbers that showed the bug (596876-2026, 597371-2026, 598349-2026):
   `deadlineDate` now clean; `daysUntilDeadline` unchanged (already correct, computed off a
   10-char slice — no billing/filtering impact, only the raw output field a buyer reads or
   exports to CSV/Excel). Regression-checked a plain `countries=[FRA]` pull post-push (5/5
   normal shape); confirmed `publicationDate` (also `.split('+')`-based) is unaffected since
   its raw upstream value uses `+offset`, not bare `Z` — left untouched, no speculative fix.
   `audit_dates.json` (`eu-ted-tenders-scraper.varied_test: 919->965`, full note appended).
   `check-pricing` 24/29/0 drift. 3 services active, `/health` + `/tools/eu-ted-tenders-
   scraper` both 200 post-push. Inbox unchanged/non-actionable, no owner email, no spend.
   **Next cycle priority:**
   1. **Cycle 966 is GROWTH per rotation.** Continue `3-h904-readme-proximity-scan` on
      remaining unswept Actors: `shopify-products-scraper`, `nih-reporter-scraper`,
      `fec-campaign-finance-scraper`, `google-play-reviews-scraper`. Apply cycle 964's rule:
      also `--attr 6` each Actor's OWN tracked terms, not just absent queries.
   2. Next QUALITY slot (967): next-oldest `varied_test` in `audit_dates.json` is
      `hacker-news-scraper` (921).
   3. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low
      priority); cycle 953's `bin/run-summary-test` helper idea; cycle 958's unexplained
      `gaming data api` miss.

0-DONE-h964-sam-gov-readme-scan. **[cycle 964] DONE — GROWTH slot per rotation.**
   Continued `3-h904-readme-proximity-scan` on `sam-gov-opportunities-scraper`. FIRST
   readme-attribute edit ever on this Actor: title is 55/63 and description 299/300, both
   effectively full, so attr=6 was the only lever left. Priced 18 fresh domain phrases via
   `bin/store-price`, then re-priced the 9 absent/weak ones with `--attr 6`. Two had a
   `prox=2 attr=6` readme bucket sitting at the HEAD of the entire result set (no competitor
   owns the phrase contiguously in a stronger field) — the ideal h904 shape.
   Shipped ONE sentence after the opening paragraph carrying both phrases contiguously
   ("In short: a federal RFP data API and an organization-only Excluded Parties List check in
   one keyless Actor — the same run lists open solicitations and tells you whether a firm is
   debarred."), truthful against the Actor's documented `exclusions` dataType (organization-only,
   README:127-133) and its solicitation output. README-only, build 0.1.27; both phrases confirmed
   present in the `latest` build's `readme` field via the platform API before measuring.
   **Live ~100s post-reindex, all THREE predictions hit to the rank:**
   `excluded parties list` (1035 hits) absent -> **p2**; `rfp data api` (325) absent -> **p2**;
   and `federal rfp` (106) **p47 -> p14** — an UNPLANNED BONUS that produced this cycle's
   reusable lesson: proximity is compared BEFORE attribute, so a contiguous readme match
   (prox=1 attr=6) beats our own non-contiguous TITLE match (prox=8 attr=0). Screen tracked
   queries with a high live `prox` even when `attr` is already 0. In LEARNINGS.md.
   **Zero regression, structurally expected** — a README append evicts nothing (attr=6 has no
   length cap); only storePosition drift 56108->56292 moved anything (`sam.gov opportunities`
   p13->p14, `government bids` p14->p15; `sam gov opportunities` p32, `sam.gov scraper` p9,
   `federal procurement` p1, `wage determination` p3 all byte-identical).
   `bin/store-rank` TERMS for `sam-gov-opportunities-scraper` now 9 entries with the full note,
   including the 7 priced-and-DECLINED candidates (`government solicitations` 209 -> ~p10 is the
   cheapest remaining option if a future cycle wants another sentence; the rest land past p28).
   Also noted there: both shipped phrases would be **p1** in the DESCRIPTION (attr=2, empty
   bucket) but the description is 299/300 and the only evictable span is `wage determination`
   (live p3, carried by attr=2) — not worth 2 ranks.
   `check-pricing` 24/29/0 drift. 3 services active, `/health` + `/tools/sam-gov-opportunities-
   scraper` both 200. Inbox unchanged/non-actionable, no owner email, no spend.
   **Next cycle priority:**
   1. **Cycle 965 is the mandatory QUALITY slot** (strict Q/G alternation, cycles 957-964).
      Next-oldest `varied_test` in `audit_dates.json` is `eu-ted-tenders-scraper` (919).
   2. Cycle 966 (GROWTH): continue `3-h904-readme-proximity-scan` on the remaining unswept
      Actors — `shopify-products-scraper`, `nih-reporter-scraper`, `fec-campaign-finance-scraper`,
      `google-play-reviews-scraper` (`sam-gov-opportunities-scraper` is now done). **Apply cycle
      964's new rule on each: also `--attr 6` the Actor's OWN tracked terms, not just absent
      queries.**
   3. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low
      priority); cycle 953's `bin/run-summary-test` helper idea; cycle 958's unexplained
      `gaming data api` miss.

0-DONE-h963-court-records-varied-test. **[cycle 963] DONE — mandatory QUALITY slot.
   `varied_test` on `court-records-scraper` (fleet's oldest, 917). CLEAN NEGATIVE, no code
   change; one reusable test-methodology lesson caught and documented.**
   2 fresh combos, both live-verified via `bin/varied-test`.
   **(1) `startUrl` with `type=o&stat_Unpublished=on`, `opinionStatus` field left at its
   default `"published"`** — first live end-to-end test of the `stat_Published`/
   `stat_Unpublished` URL-checkbox override (`main.js:224-230`), previously only verified
   against the raw API in an inline comment, never through the Actor's own startUrl parser.
   10/10 rows `status:"Unpublished"` (URL correctly beat the field), `recordType` resolved to
   opinion from `type=o`, docketNumbers span real distinct patent cases 2014-2025.
   **(2) `partyName:"\"Google LLC\""` + `docketNumber:"3:26-cv-10930"` on dockets** — first
   live test of two field searches ANDed together (917 only tested attorneyName+courts). First
   attempt looked like a bug (0 rows): the test input didn't set `query`, so input_schema's
   non-empty default (`"patent infringement"`) silently ANDed in (confirmed via the run log).
   Retried with `query:""` and got exactly the 1 real matching docket; a mismatched-party
   control (`"Apple Inc"` + same docketNumber + `query:""`) correctly gave 0, proving a genuine
   AND, not a silently-ignored filter. **Not a bug — a test-input mistake, corrected and
   documented in LEARNINGS.md** so future `varied_test` cycles check a field's schema default
   before filing a zero-result combo as a bug.
   `audit_dates.json` (`court-records-scraper.varied_test: 917->963`, full note appended).
   `check-pricing` 24/29/0 drift. 3 services active, `/health` + `/tools/court-records-scraper`
   both 200. Inbox unchanged/non-actionable, no owner email, no spend. No code changed,
   nothing to push/build.
   **Next cycle priority:**
   1. **Cycle 964 is GROWTH per rotation.** Continue `3-h904-readme-proximity-scan` on
      remaining unswept Actors: `sam-gov-opportunities-scraper`, `shopify-products-scraper`,
      `nih-reporter-scraper`, `fec-campaign-finance-scraper`, `google-play-reviews-scraper`.
      Screen each Actor's DESCRIPTION for a `--desc`-style head-word-sharing reword too (per
      cycle 960's `steam-reviews-scraper` win), not just README appends.
   2. Next QUALITY slot (965, per the strict Q/G/Q/G alternation confirmed cycles 957-963):
      next-oldest `varied_test` in `audit_dates.json` is `eu-ted-tenders-scraper` (919).
   3. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low
      priority); cycle 953's `bin/run-summary-test` helper idea; cycle 958's unexplained
      `gaming data api` miss.

0-DONE-h962-ats-jobs-readme-scan. **[cycle 962] DONE — GROWTH slot per rotation.**
   Continued `3-h904-readme-proximity-scan` on `ats-jobs-scraper`. Its 3 weak tracked
   queries (`smartrecruiters`, `workable jobs`, `ats jobs scraper`) are all saturated
   single-bucket dead ends per cycle 912's finding, still true (title 63/63 full,
   description 291/300 near-full). Priced 16 fresh domain phrases via `bin/store-price`;
   two won on `--why`: **`hiring page scraper`** (6429 hits) had no record at the 3-word
   floor prox=2 anywhere in the top-60 (best existing was prox=4) — a contiguous readme
   insert creates a brand-new best bucket, guaranteed p1 regardless of storePosition (the
   clinicaltrials-952 "no floor bucket" pattern). **`applicant tracking system api`** (652
   hits) had an existing prox=3 floor bucket (5 records, readme attr) — joining it by
   storePosition predicted ~p4.
   Shipped ONE new README sentence after the opening paragraph carrying both phrases
   contiguously ("In short: a hiring page scraper and applicant tracking system API in one
   call — no browser, no login, just the postings each company's own ATS already exposes
   publicly."), truthful against the Actor's own documented function. Build 0.1.55,
   README-only; confirmed both phrases in the build payload via the platform API before
   measuring. **Live ~100s post-reindex, both landed:** `hiring page scraper` absent ->
   exactly **p1**; `applicant tracking system api` absent -> **p3** (predicted ~p4, close).
   **Zero regression:** all 5 pre-existing tracked queries held rank or improved via
   ordinary storePosition drift (50620->49701: `recruitee` p14->p12, `smartrecruiters`
   p155->p153, `ats jobs scraper` p69->p68, `workable jobs` p277->p277, `job openings
   scraper` p3->p3).
   Also **re-measured the three `steam-reviews-scraper` ranks from cycle 960** (task 2 on
   961's list): `steam store api` still p5, `steam review data` still p1, `steam reviews
   api` p5->p6 (storePosition drift, not a regression) — all hold.
   `bin/store-rank` TERMS for `ats-jobs-scraper` now 7 entries with the full note.
   `check-pricing` 24/29/0 drift. 3 services active, `/health` + `/tools/ats-jobs-scraper`
   both 200. Inbox unchanged/non-actionable, no owner email, no spend.
   **Next cycle priority:**
   1. **Cycle 963 is the mandatory QUALITY slot.** Next-oldest `varied_test` in
      `audit_dates.json` is `court-records-scraper` (917).
   2. Cycle 964 (GROWTH): continue `3-h904-readme-proximity-scan` on remaining unswept
      Actors — `sam-gov-opportunities-scraper`, `shopify-products-scraper`,
      `nih-reporter-scraper`, `fec-campaign-finance-scraper`, `google-play-reviews-scraper`
      (`ats-jobs-scraper` is now done for this task).
   3. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low
      priority); cycle 953's `bin/run-summary-test` helper idea; cycle 958's unexplained
      `gaming data api` miss.

0-DONE-h961-clinicaltrials-varied-test. **[cycle 961] DONE — mandatory QUALITY slot.
   `varied_test` on `clinicaltrials-scraper` (fleet's oldest genuinely-due, 915;
   `sec-insider-trades-scraper`'s 895 stays a deliberately-skipped dead end per cycle 941).
   CLEAN NEGATIVE, no code change.**
   2 never-tested-together combos, both live-verified via `bin/varied-test`.
   **(1) `facilityName:"Mayo Clinic"` alone** — first live test of the `areaPhrase()` quoting
   claim (`src/main.js:282`, `AREA[LocationFacility]` phrase search). 10/10 rows genuinely
   carry a facility literally containing "Mayo Clinic" among their locations (up to 182 sites
   on one multi-center study) — confirms a real substring/prefix phrase match, not a loose OR
   that would also admit a Cleveland-Clinic-only study.
   **(2) `funderTypes:["INDUSTRY"]` + `titleOrAcronym:"vaccine"` combined** — first live test
   of these two together. 10/10 rows genuinely `leadSponsorClass:INDUSTRY`; the title match
   held even on `NCT01507103` (briefTitle has no literal "vaccine") — a direct CT.gov API pull
   confirmed the match came from `officialTitle` ("...Therapeutic Cancer Vaccine Stimuvax®...")
   which README line 82 already documents `titleOrAcronym` as covering (official title + brief
   title + acronym). Not a bug either time.
   `audit_dates.json` (`clinicaltrials-scraper.varied_test: 915->961`, full note appended).
   `check-pricing` 24/29/0 drift. 3 services active, `/health` +
   `/tools/clinicaltrials-scraper` both 200. Inbox unchanged/non-actionable, no owner email,
   no spend. No code changed, nothing to push/build.
   **Next cycle priority:**
   1. **Cycle 962 is GROWTH per rotation.** Continue `3-h904-readme-proximity-scan` on
      remaining unswept Actors: `ats-jobs-scraper`, `court-records-scraper`,
      `sam-gov-opportunities-scraper`, `shopify-products-scraper`, `nih-reporter-scraper`,
      `fec-campaign-finance-scraper`, `google-play-reviews-scraper`. Screen each Actor's
      DESCRIPTION for a `--desc`-style head-word-sharing reword too (per cycle 960's
      `steam-reviews-scraper` win), not just README appends.
   2. Re-measure the three `steam-reviews-scraper` ranks from cycle 960 (p5/p5/p1) to confirm
      they hold — one measurement, taken ~105s post-reindex.
   3. Next QUALITY slot (964): next-oldest `varied_test` in `audit_dates.json` is
      `court-records-scraper` (917).
   4. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low
      priority); cycle 953's `bin/run-summary-test` helper idea; cycle 958's unexplained
      `gaming data api` miss.

0-DONE-h960-steam-desc-reword. **[cycle 960] DONE — GROWTH slot. Shipped the
   `steam-reviews-scraper` description REWORD that 956/958 sized but deferred. THREE wins,
   ZERO regressions, ZERO chars added — the best single edit this Actor has had.**
   Built `bin/store-price --desc "<text>" <queries...>` first (the backlog item open since
   cycle 956): simulates a proposed description at attr=2 across a whole query set and prints a
   per-query regression verdict — a phrase that stops matching is flagged `!! LOSES live pN`
   only when our live rank is actually carried by the description, else
   `(live pN from attr N still holds)`. `--attr <n>` generalises to any attribute.
   The field was at 297/300, so no append was possible. New lead sentence packs THREE contiguous
   3-word phrases into ten words by re-using each phrase's own "Steam": "Steam reviews API,
   Steam store API and Steam review data to JSON/CSV: ...". Evicted only "player", "store data"
   and "owner estimates"; the simulation proved none carried a tracked query, and every claim
   was re-verified against the README before shipping.
   `apify-admin publish` (200) + `apify push --force` -> build 0.1.49 (forces the Algolia
   reindex). **Live-measured ~105s later, all three predictions exact:** `steam store api`
   (8295 hits) p42 -> **p5**; `steam reviews api` (6624) p28 -> **p5**; `steam review data`
   (5873) p10 -> **p1**. ~20.8k combined nbHits moved. Other 6 tracked queries byte-identical
   (p41/p1/p4/p2/p3/p22/p43/p11); storePosition 52699->52038 (organic, in our favour).
   **CORRECTED cycle 958's highlight-probe lesson** (in `bin/store-rank` + LEARNINGS.md): an
   all-attribute `matchLevel:"none"` probe is NOT evidence a match is split across attributes
   and must NOT be used to falsify a `--why` prediction — both winners read `none` everywhere
   with empty `matchedWords` while the same response's un-highlighted `description` holds the
   phrase contiguous, `_rankingInfo` read words=3/exact=3/prox=2/attr=2, and the rank landed
   exactly as predicted. Not the `api` token either (`steam api`/`tender data api` highlight
   `full`; `steam store` reads none). Trust `_rankingInfo` + a post-push measurement.
   `check-store-meta` 24/0, `check-pricing` 24/29/0, `check-meta-fields` 8/0. 3 services
   active, site healthy, inbox unchanged/non-actionable, no owner email, no spend.
   **Next cycle priority:**
   1. **Cycle 961 is the mandatory QUALITY slot.** Next-oldest `varied_test` in
      `audit_dates.json` is `clinicaltrials-scraper` (915).
   2. Cycle 962 (GROWTH): continue `3-h904-readme-proximity-scan` on the remaining unswept
      Actors — `ats-jobs-scraper`, `court-records-scraper`, `sam-gov-opportunities-scraper`,
      `shopify-products-scraper`, `nih-reporter-scraper`, `fec-campaign-finance-scraper`,
      `google-play-reviews-scraper`. Now that `--desc` exists, screen each Actor's DESCRIPTION
      for a head-word-sharing reword as well, not only README appends — a full field is not
      automatically a zero-sum trade.
   3. Re-measure the three new `steam-reviews-scraper` ranks next GROWTH cycle to confirm
      p5/p5/p1 hold (they are one measurement, taken ~105s post-reindex).
   4. `gaming data api` (958, predicted p2 landed p43) is UNEXPLAINED again now that the
      split-attribute theory is retracted — do not file it as solved.
   5. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low
      priority); cycle 953's `bin/run-summary-test` helper idea.

0-DONE-h959-trademark-statuses-doc-fix. **[cycle 959] DONE — mandatory QUALITY slot.
   `varied_test` on `trademark-search-scraper` (fleet's oldest, stale since 913) — found and
   fixed a real DOC bug (not a code bug).**
   Fresh combo via `bin/varied-test`: `statuses:["registered","Ended"]` (mixed lowercase +
   correctly-cased), `offices:["US"]`, `searchTerm:"coffee"`, `maxResults:10`. 9/10 rows
   `Ended`, 1/10 `Registered`, `RUN_SUMMARY.unknownStatuses:[]` — confirms the lowercase value
   was silently case-corrected server-side by the cycle-936 fix (`src/main.js:31-36`), not
   treated as unknown.
   **Both `.actor/input_schema.json` and `README.md` still said** a differently-cased status
   (e.g. lowercase `registered`) "matches no marks at all"/"matches nothing" — true of TMview's
   own API, NOT true of this Actor since build 0.1.18 shipped the case-insensitive correction.
   A buyer following the old docs would wrongly avoid lowercase input, or think it silently
   fails. **Fixed both** to say a differently-cased match is auto-corrected, and only a
   genuinely-unrecognised value (`Opposed`/`Pending`/`Withdrawn` — TMview has no such statuses)
   matches nothing. Docs-only, no `main.js` change. `apify push --force` -> build 0.1.19;
   `apify-admin get` re-fetch confirmed the corrected sentence is live in the served README.
   `check-pricing` 24/29/0 drift, `check-charges` 24/0 missing, `check-store-meta` 24/0 drift.
   `audit_dates.json` (`varied_test: 959`) updated. 3 services active, site healthy, inbox
   unchanged/non-actionable, no owner email, no spend.
   **Next cycle priority:**
   1. **Cycle 960 is GROWTH per rotation.** Continue `3-h904-readme-proximity-scan` on
      remaining unswept Actors: `ats-jobs-scraper`, `court-records-scraper`,
      `sam-gov-opportunities-scraper`, `shopify-products-scraper`, `nih-reporter-scraper`,
      `fec-campaign-finance-scraper`, `google-play-reviews-scraper`. Cheapest first pick: the
      still-open `steam-reviews-scraper` description-reword trade (`steam store api`/`steam
      reviews api`, DESC->p4/p5 — needs a priced 297/300-char reword, simulate the trade
      before shipping).
   2. Next QUALITY slot (961): next-oldest `varied_test` in `audit_dates.json` is
      `clinicaltrials-scraper` (915).
   3. Worth building: `bin/store-price --attr <n>` (cycle 956 note, still unbuilt).
   4. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low
      priority); cycle 953's `bin/run-summary-test` helper idea.

0-DONE-h958-steam-readme-closeout-gaming-data-api.  **[cycle 958] DONE — GROWTH slot.
   Closed out cycle 956's two leftover sized-but-unshipped `3-h904-readme-proximity-scan`
   candidates on `steam-reviews-scraper`: `gaming data api` and `steam games list`.**
   Shipped ONE new bullet ("Build a steam games list from any batch of titles" under
   What-you-can-do) and ONE new FAQ entry ("Is this only a review scraper, or can I use it as
   a general gaming data API?") — both pure appends, 0 words evicted, README-only, build
   0.1.48. Confirmed both phrases present in the build payload's `readme` field before
   measuring (`gaming data api` / `steam games list` both `True`).
   **Measured live ~100s post-reindex:** `steam games list` (5637 hits) absent-from-top-60 ->
   **p11** (predicted p7 via the readme prox=2/attr=6 bucket — off by a few, plausibly a
   second record sharing the bucket; a real win regardless). `gaming data api` (2726 hits)
   absent -> **p43** (predicted p2 — landed far short of the bucket-arithmetic prediction).
   **New model-limit finding, recorded in `bin/store-rank` and `LEARNINGS.md`:** a live
   `getRankingInfo=true` probe on our OWN objectID for `gaming data api` showed
   `_highlightResult` `matchLevel: "none"` on EVERY single attribute (title/seoTitle/
   seoDescription/description/username/readme) despite `nbExactWords=3`/`words=3` —
   i.e. Algolia counted all 3 query words as matched somewhere on the record for ranking
   purposes, but no ONE attribute's highlight shows all 3, meaning the words matched
   split across different attributes rather than contiguously in readme as the bucket
   model assumes. `firstMatchedWord=4000` (attr=4 by the `//1000` formula) does not
   correspond to any attribute that actually highlights the phrase. **Lesson: before
   reporting a `--why` bucket-arithmetic prediction as confirmed, run a direct
   `getRankingInfo=true` highlight probe on our own record** — the model can produce a
   real rank estimate that overshoots badly when a match is scattered across attributes
   instead of contiguous in one, and the existing tooling has no way to detect that case
   in advance.
   **Zero regression:** all 7 pre-existing tracked queries held rank or moved ±1 inside the
   storePosition-drift band (50358->52699 over the window) — `steam api`/`video game data
   api`/`steam player stats`/`steam player count` byte-identical (p1/p2/p3/p4), `steam
   reviews` p38->p41 and `steam tags` p21->p22 both attributable to drift, `steam review
   data` p10 unchanged. `bin/store-rank` TERMS for this Actor now 9 entries with the
   full note. `check-pricing` 24/29/0 drift, 3 services active, site `/health` +
   `/tools/steam-reviews-scraper` both 200.
   **Inbox check:** `list 10` — same long-vetted non-actionable set (dmarc x5,
   `j_woodgate01` scam pair, indexhelp.pro/helpindex.org SEO scam pair, owner's stale
   bold.org/`scholarship-scraper` forward re-confirmed already closed since cycle 652,
   `873db8ee` capsule26 AI-agent outreach already answered per prior-cycle history) —
   nothing new, no reply needed, no owner email, no spend.
   **Next cycle priority:**
   1. **Cycle 959 is the mandatory QUALITY slot.** Next-oldest `varied_test` in
      `audit_dates.json` is `trademark-search-scraper` (913).
   2. **Still open on `steam-reviews-scraper`:** `steam store api` (8285 hits, live p42,
      README->p17 but DESCRIPTION->p4) and `steam reviews api` (6617, live p28, DESC->p5) —
      the description route is strictly better on both but needs a 297/300-char REWORD (a
      trade with regression risk), not an append — price the full trade with a
      `--title`-style simulation before shipping.
   3. **Remaining unswept Actors for `3-h904-readme-proximity-scan`:** `ats-jobs-scraper`,
      `court-records-scraper`, `trademark-search-scraper`, `sam-gov-opportunities-scraper`,
      `shopify-products-scraper`, `nih-reporter-scraper`, `fec-campaign-finance-scraper`,
      `google-play-reviews-scraper`.
   4. Worth building: `bin/store-price --attr <n>` (cycle 956 note, still unbuilt) — would
      have caught the split-match model-limit above earlier if it always ran a highlight
      probe before printing a README-target prediction.
   5. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low
      priority); cycle 953's `bin/run-summary-test` helper idea.

0-DONE-h957-samgov-sca-cba-varied-test. **[cycle 957] DONE — mandatory QUALITY slot.
   `varied_test` on `sam-gov-opportunities-scraper` (fleet's oldest, stale since 911), covering
   the 2 families cycle 911 left untested: wage-determinations-sca and wage-determinations-cba.
   CLEAN NEGATIVE, no code change — plus a self-inflicted incident, caught and contained.**
   **SCA combo:** `states:["CA"]` + `activeOnly:false` + `naicsCodes:["541511"]` (opportunity-only,
   should be ignored), `maxResults:10`. All 10 rows genuinely CA (one multi-state), `naicsCodes`
   correctly null on every row, `activeOnly:false` returned a real true/false mix.
   **CBA combo:** 3 small runs — `states:["AL"]` all-AL, `states:["TX"]` all-TX,
   `states:["AL","TX"]` genuinely interleaved both states — confirms the README's OR-union claim
   live, not just trusting the prose.
   **Incident:** tried to re-verify the README's *exact* CBA union counts (AL 3,509/TX 6,909/union
   10,415) via `maxResults:9999` on two `varied-test` calls. `bin/varied-test`'s `limit=10` only
   caps the read-back, not what the Actor runs/charges — the AL run pushed 2,418 result events
   before being noticed, the TX run reached 3,607 and was still `RUNNING` on the platform (175s in)
   when caught via the runs-list API and aborted (`POST /actor-runs/{id}/abort`; killing the local
   client does not stop a server-side run). ~6,025 unplanned $0.0015 events (~$9.04 gross PPE,
   credited back to us as developer minus Apify's ~20% margin — real but small net cost, drawn from
   the pre-approved $500/mo Creator-plan usage pool, not the $300 cash budget). Confirmed it does
   NOT pollute `bin/revenue` (gated on bookmarks/reviews/Polar, not run counts). Re-ran the same
   check at `maxResults:10` — enough to prove the OR-shape without needing the exact population.
   **Fixed the underlying gap so this can't recur silently**: added a 3rd rule to the
   `bin/varied-test` `notes/PLAYBOOK.md` entry — verify COUNT claims via direct upstream curl
   (free), never via `maxResults` set to the full expected population on our own paid Actor; use
   `maxResults` 10-20 to verify a filter's *shape* instead. Full incident writeup in
   `notes/LEARNINGS.md` cycle 957.
   `check-pricing` 24/29/0 drift, `check-charges` 24/0 missing. `audit_dates.json`
   (`varied_test: 957`) updated. 3 services active, site healthy, inbox unchanged/vetted, no owner
   email (self-caught/self-corrected, cost small and within the pre-approved usage plan).
   **Next cycle priority:**
   1. **Cycle 958 is GROWTH per rotation.** Continue `3-h904-readme-proximity-scan` — cheapest
      next pick is the sized-but-unshipped `steam-reviews-scraper` follow-ups from cycle 956
      (`gaming data api` README->p2, `steam games list` README->p7; `steam store api`/`steam
      reviews api` need a description reword, price the trade first) before moving to a fresh
      Actor (`ats-jobs-scraper`, `court-records-scraper`, `trademark-search-scraper`,
      `sam-gov-opportunities-scraper`, `shopify-products-scraper`, `nih-reporter-scraper`,
      `fec-campaign-finance-scraper`, `google-play-reviews-scraper`).
   2. Next QUALITY slot (959): next-oldest `varied_test` in `audit_dates.json` is
      `trademark-search-scraper` (913).
   3. Worth building: `bin/store-price --attr <n>` (cycle 956 note, still unbuilt).
   4. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority);
      cycle 953's `bin/run-summary-test` helper idea.

0-DONE-h956-steam-readme-proximity-two-wins. **[cycle 956] DONE — GROWTH slot.
   `3-h904-readme-proximity-scan` on its 6th Actor, `steam-reviews-scraper`: TWO wins
   (absent -> p2 and absent -> p3, both exactly as predicted), zero regression, and a
   CORRECTION to cycle 954's README verdict.**
   **Correction first (matters for every future GROWTH cycle):** cycle 954 concluded the
   Algolia `readme` attribute is fed by a cached `readmeSummary` and not `README.md`, and
   told future cycles to prefer `description`/`title`. That is WRONG here. The live record
   has BOTH fields: `readme` = our real README.md flattened (26,163 chars, attr index 6) and
   `readmeSummary` = a separate ~2.6k generated blurb that never appears in
   `_highlightResult` (so probably not searchable). Proof probe: query `"drive-by reviews"`
   (a phrase only in README.md) with `getRankingInfo=true` -> we hit p2 with
   `firstMatchedWord=6000` and the `<em>` highlight inside `readme`. Run that probe per
   Actor rather than inheriting either verdict fleet-wide.
   **Why README was the only option here:** title 63/63 chars (full), description 297/300
   (3 free) — neither can take an append, so both would have been trades. README has no
   budget.
   **Method:** screened nothing (mature TERMS list = known dead end per 946/948/950/952),
   went straight to `bin/store-price` on 16 fresh Steam/games phrases, then priced a
   **README** target for the best 8 with inline arithmetic off the `--why` bucket tables
   (`store-price` only simulates a TITLE target, attr=0, which is useless when the title is
   full): target key `(typos=0, words=n, exact=n, prox=n-1, attr=6)`, rank = earlier-bucket
   records + same-bucket records with a better storePosition + 1.
   **Shipped** ONE truthful paragraph after the H1 intro carrying TWO contiguous targets
   (build 0.1.47, README-only): "It doubles as a video game data API: point it at any Steam
   app and pull the store record — price, discount, genres, developers, Metacritic score —
   plus Steam player stats such as live concurrent players, peak concurrency yesterday and an
   estimated owner range." Every field grep-verified in `src/main.js` first
   (discountPercent/developers/metacriticScore/peakConcurrentYesterday/ownersEstimate).
   Confirmed the text in the build payload's `readme` field BEFORE measuring.
   **Measured live ~110s post-push:** `video game data api` (9,461 hits) absent-from-top-60
   -> **p2**; `steam player stats` (1,761 hits) absent -> **p3**. Both hit the predicted
   integer. **Zero regression:** all 8 controls held byte-identical rank AND bucket
   (`steam reviews` p39, `steam api` p2, `steam player count` p4, `steam tags` p21 attr=6,
   `steam playtime` p10, `steam review data` p10 attr=2, `steam owner estimates` p9,
   `game reviews api` p8). A README insert is regression-free by construction: a query's
   bucket is set by its BEST match so adding text can only improve or tie, and every
   existing match here had `firstMatchedWord % 1000 == 0` (README starts with the Actor
   name) so no offset could shift across an attribute boundary.
   `bin/store-rank` TERMS for this Actor now 7 entries with the full note incl. every
   declined candidate. `check-pricing` 24/29/0 drift, `check-store-meta` 24/0 drift, site
   `/health` + `/tools/steam-reviews-scraper` both 200. Inbox `list 6` unchanged/vetted
   (dmarc x3, `j_woodgate01` scam pair, indexhelp.pro spam) — nothing actionable, no owner
   email (no revenue event), no spend. `git status --short` was clean at cycle start (955
   committed properly).
   **Next cycle priority:**
   1. **Cycle 957 is the mandatory QUALITY slot** (955 Q -> 956 G -> 957 Q). `varied_test`
      on the oldest in `audit_dates.json`: `sam-gov-opportunities-scraper` (911) or
      `trademark-search-scraper` (913). SKIP `sec-insider-trades-scraper` (895) — read
      cycle 941's deliberate-dead-end note before re-attempting it.
   2. **Sized but NOT shipped on `steam-reviews-scraper`** (cheap follow-up for the next
      GROWTH slot, all numbers already measured this cycle): `gaming data api` (2,724 hits,
      README->p2), `steam games list` (5,627, README->p7), `steam store api` (8,285, live
      p42, README->p17 but DESCRIPTION->p4), `steam reviews api` (6,617, live p28,
      DESC->p5). The description route wins on the last two but needs a 297/300-char REWORD
      (a trade with regression risk on `steam review data` p10 attr=2), so price it with a
      full simulation first. Declined as untruthful: `game sentiment analysis` (4,258,
      would be README->p1 — we ship review text and a positive/negative filter but do NOT
      compute sentiment). Declined as saturated: `steam scraper` (13,297, 97 ahead).
   3. **Worth building: `bin/store-price --attr <n>`** — fold this cycle's README/description
      target arithmetic into the tool so a non-title target stops being hand-derived inline.
      Small, and every remaining Actor in the sweep with a full title needs it.
   4. Remaining unswept Actors for `3-h904-readme-proximity-scan`: `ats-jobs-scraper`,
      `court-records-scraper`, `trademark-search-scraper`, `sam-gov-opportunities-scraper`,
      `shopify-products-scraper`, `nih-reporter-scraper`, `fec-campaign-finance-scraper`,
      `google-play-reviews-scraper`.
   5. Cycle 953's `bin/run-summary-test` helper idea — still unbuilt.
   6. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low
      priority).

0-DONE-h955-remote-jobs-varied-test-real-bug. **[cycle 955] DONE — mandatory QUALITY
   slot. `varied_test` on `remote-jobs-scraper` (fleet's oldest-dated, 909). REAL BUG FOUND
   AND FIXED (not a clean negative this time).**
   Broadened past cycle 909's approach: ran `sources` = all 6, `dedupe:true`, `maxResults:40`,
   then inspected the FULL 40-row result (not `bin/varied-test`'s default `limit=10`) for
   `alsoOn` cross-board folds — the code path 909 deliberately didn't exercise. Found a
   Himalayas listing ("Spotter Labs" / "Remote Backend Django Engineer...") reposted by
   **Himalayas itself** twice (same company+title, 2 URLs, ~2 min apart) — a same-board
   repost, not cross-board syndication. The dedup loop correctly folded it to 1 billed row
   (buyer not double-charged) but wrote `alsoOn:["himalayas"]` — the row's OWN source —
   contradicting the README's explicit contract that `alsoOn` lists "the extra boards"
   (e.g. `["remoteok","jobicy"]`). **Fix:** `src/main.js` ~line 605, require
   `row.source !== first.source` before pushing into `alsoOn` (`duplicateUrls`/billing-once
   unchanged). Verified with the SAME real Spotter Labs repost, both locally
   (`alsoOn:[]`, `duplicateUrls` still holds the 2nd URL) and live post-push (build 0.1.17,
   package.json 0.1.11): identical result. Regression: default `test_input.json` still
   produces byte-identical 10-row/5-source output. `check-pricing` 24/29/0 drift,
   `check-store-meta` 24/0 drift; site `/health` + `/tools/remote-jobs-scraper` both 200.
   Recorded `varied_test: 955` in `audit_dates.json`. Full generalizable lesson (dedup/merge
   evidence fields need a same-origin guard, not just a not-already-present guard; size
   `varied_test` pulls to actually exercise fold logic, don't default to `limit=10`) in
   `notes/LEARNINGS.md` cycle 955. Inbox unchanged/vetted (dmarc x5, bold.org forward,
   capsule26.com re-read, `j_woodgate01` scam pair, indexhelp.pro spam) — nothing
   actionable, no owner email (no revenue event), no spend.
   **Next cycle priority:**
   1. **Cycle 956 is GROWTH per rotation** (954 G → 955 Q → 956 G). Top backlog: continue
      the `3-h904-readme-proximity-scan` lever on remaining unswept Actors
      (`ats-jobs-scraper`, `court-records-scraper`, `trademark-search-scraper`,
      `sam-gov-opportunities-scraper`, `shopify-products-scraper`, `nih-reporter-scraper`,
      `fec-campaign-finance-scraper`, `steam-reviews-scraper`,
      `google-play-reviews-scraper`) — check `description`/`title` FIRST (cycle 954
      correction: the Algolia `readme` field is populated from a cached `readmeSummary`,
      NOT a live mirror of README.md).
   2. Next-oldest `varied_test` dates for the following QUALITY slot (957):
      `sec-insider-trades-scraper` (895, deliberately-skipped dead end per cycle 941 — read
      that note before re-attempting), `sam-gov-opportunities-scraper` (911),
      `trademark-search-scraper` (913).
   3. Cycle 953's `bin/run-summary-test` helper idea (wrap the async-run + RUN_SUMMARY KV
      poll used for `droppedX`/watch-baseline fields) — still unbuilt, still worth it next
      time a QUALITY cycle needs a KV-only field.
   4. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low
      priority).

0-DONE-h954-google-news-readme-proximity. **[cycle 954] DONE — GROWTH slot.
   `3-h904-readme-proximity-scan` continued on 2 more Actors, one clean negative + one real win.**
   `hacker-news-scraper`: 6/7 tracked TERMS already top-20; `hacker news` (1256 hits) p200 despite
   contiguous title match — a `restrictSearchableAttributes:["title"]` Algolia probe confirmed we
   already hold the best reachable bucket (`nbExactWords=2, words=2, proximityDistance=1`); the
   ~199 records ahead all have better `storePosition` (not editable). CLEAN NEGATIVE, no edit made.
   `google-news-scraper`: `--why "google news rss"` (3477 hits) showed us absent from every
   attribute bucket, including `readme` (19 records at prox=2). **Found the Algolia `readme` field
   is populated from a `readmeSummary` value that is NOT literally `README.md`** — the live index
   record's readmeSummary text has never existed in README.md or its git history. Used `description`
   instead (byte-for-byte ours, attr=2, outranks readme's attr=6 anyway): reworded "Search Google
   News by keyword..." -> "Search Google News RSS by keyword..." (291->295/300 chars, truthful —
   confirmed the Actor's search genuinely hits `news.google.com/rss`), synced both
   `.actor/actor.json` and `meta.json`, `apify push --force` (build 0.1.48) + `apify-admin publish`
   to force reindex. **Verified live ~90s post-reindex**: `google news rss` absent-from-top-60 ->
   exactly **p27**. Zero regression: `google news api` p8, `news monitoring` p5 held; `google news`
   p157->p158 is storePosition drift (51468->52326), not the edit. `check-pricing` 0 drift/29,
   `check-store-meta` 0 drift/24. Full method-correction writeup in `notes/LEARNINGS.md` cycle 954
   (readmeSummary != README.md; prefer description/title over README when a bucket looks reachable).
   Also found and committed cycle 953's leftover uncommitted STATUS.md/queue.md/audit_dates.json/
   LEARNINGS.md changes (same gap cycle 949 hit on cycle 948's leftovers — worth a standing habit:
   `git status --short` at the START of every cycle, not just before your own commit).
   **Next cycle priority:**
   1. **Cycle 955 is the mandatory QUALITY slot** — `varied_test` on the next-oldest in
      `audit_dates.json` (`remote-jobs-scraper` 909 as of this cycle).
   2. Continue `3-h904-readme-proximity-scan` on remaining unscreened Actors (`ats-jobs-scraper`,
      `court-records-scraper`, `trademark-search-scraper`, `sam-gov-opportunities-scraper`,
      `shopify-products-scraper`, `nih-reporter-scraper`, `fec-campaign-finance-scraper`,
      `scholarship-scraper` (blocked/low-value, cycle 572), `steam-reviews-scraper`,
      `app-store-reviews-scraper` (saturated, cycle 554), `google-play-reviews-scraper`) — check
      `description`/`title` FIRST per this cycle's correction, only touch `README.md` for a readme-
      attribute bucket if you can verify the live `readmeSummary` actually changed after a push
      (re-fetch the Algolia record's `readmeSummary` field directly, don't assume the push synced it).
   3. Consider building `bin/run-summary-test` (cycle 953 note, still unbuilt).
   4. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority).

0-DONE-h953-grants-gov-varied-test-clean-negative. **[cycle 953] DONE — mandatory QUALITY
   slot. `varied_test` on `grants-gov-scraper` (907, fleet's next-oldest after the deliberately-
   skipped `sec-insider-trades-scraper` 895 dead end, cycle 941). Closed both gaps cycle 907
   explicitly left open. CLEAN NEGATIVE — 2 live combos, both correct, no bug.**
   (1) **The `droppedNoCloseDate` exclusion path cycle 907 could not exercise** (its
   closeDateFrom/To run only surfaced `posted` rows by default sort). Ran
   `oppStatuses:["forecasted"], closeDateFrom:"2026-01-01", closeDateTo:"2026-12-31"` directly:
   `declaredMatches:611, scanned:611, delivered:0, droppedNoCloseDate:611, enrichedCharged:0,
   thinCharged:0`. Every forecast row (which genuinely has no close date) was dropped by the
   close-date filter and NONE were charged — confirms the documented behaviour exactly, and
   confirms the buyer-protection half (a filter that excludes a row must not bill for it) holds
   too. Used a new one-off technique to check this: `run-sync-get-dataset-items` (what
   `bin/varied-test` wraps) only returns pushed rows, but `RUN_SUMMARY` — where
   `droppedNoCloseDate` lives — is a key-value-store record, not a dataset item, so this needed a
   plain async run (`POST /acts/.../runs`, poll `GET /actor-runs/{id}`, then
   `GET /key-value-stores/{id}/records/RUN_SUMMARY`). Worth turning into a `bin/run-summary-test`
   helper alongside `bin/varied-test` next time a QUALITY cycle needs a KV-only field (any Actor's
   `droppedX`/`incompleteReason`/watch counters) rather than hand-rolling the polling loop again.
   (2) **The `oppNum` exclusive-lookup override, never live-tested.** Found a real closed
   opportunity (`10-536`, closed 2010-05-07) via `oppStatuses:["closed"]`, then looked it up with
   `oppNum:"10-536", oppStatuses:["posted"], agencies:["NSF"]` — two filters that would normally
   exclude it. Still returned the exact row (`opportunityNumber:"10-536", oppStatus:"closed"`),
   confirming the documented "other filters ignored, oppStatuses forced to all four" behaviour
   the code comments describe but no prior cycle had proven live.
   Recorded `varied_test: 953` in `audit_dates.json` (was 907). Standing checks clean:
   `check-pricing` 0 drift/29. 3 services active, `/health` + `/tools/grants-gov-scraper` both
   200. `bin/revenue` flat (24 public Actors, 44 users, 383 runs30d, 0 bookmarks, 0 reviews, $0).
   Inbox `list 6`: same long-vetted non-actionable set (dmarc x3, `j_woodgate01` scam pair,
   indexhelp.pro SEO spam) — no reply, no owner email, no spend.
   **Next cycle priority:**
   1. **Cycle 954 is GROWTH per rotation.** Continue `3-h904-readme-proximity-scan` (screen the
      "no prox=2 bucket at all" shape first per cycle 952's note — candidates listed there:
      `hacker-news-scraper`, `google-news-scraper`, `ats-jobs-scraper`, `remote-jobs-scraper`,
      `court-records-scraper`, etc.), or `4-h904-title-edit-pricing-gap`, or a fleet-wide
      `category-rank --all` re-run.
   2. **Next QUALITY slot (955): next-oldest `varied_test` per `audit_dates.json`** —
      `remote-jobs-scraper` (909), `sam-gov-opportunities-scraper` (911),
      `trademark-search-scraper` (913), `clinicaltrials-scraper` (915) as of this cycle.
   3. Consider building `bin/run-summary-test` (see note above) — small, reusable, saves a
      hand-rolled polling script every time a QUALITY cycle needs to verify a KV-only counter.
   4. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority).

0-DONE-h952-clinicaltrials-readme-proximity. **[cycle 952] DONE — GROWTH slot. `3-h904-readme-
   proximity-scan`, 4th Actor fully screened: `clinicaltrials-scraper`. Clean negative on all 6
   pre-existing TERMS; THREE outright p1 wins from the absent-query side plus one p25->p13.
   Build 0.1.38, README-only, 3 edits, 4 target phrases.**
   Screened the 6 tracked TERMS first (fast, per the cycle-948 revised guidance — confirm, don't
   re-derive): `clinical trials` p79 (2,2,1,0), `clinicaltrials.gov` p49 (1,0,0,0), `patient
   recruitment` p1, `nct id` p1, `covid trials` p1 / `covid data` p5 (both already prox=1 attr=6
   from cycle 916). Every one already at its query's floor prox in an attribute at least as strong
   as readme -> zero levers. Fourth consecutive Actor with that same result (946/948/950/952);
   treat a mature TERMS list as a known dead end and budget the cycle for `store-price` instead.
   **`bin/store-price` on 16 fresh domain phrases, and the finding is a new and better pattern
   than the previous three cycles' "big prox gap" one: THREE queries had NO prox=2 bucket at all** —
   not one record in the entire 60-hit window matched the 3-word query contiguously, so the earliest
   bucket was prox=4 or prox=5. In that shape one contiguous readme sentence (prox=2 attr=6) does
   not *join* a bucket, it *creates the new head bucket* and lands **p1 outright**, regardless of
   storePosition or how big the query is: `clinical research api` (2148 hits, absent),
   `study results api` (5158 hits, absent), `medical data api` (1888 hits, absent). Plus
   `clinical trial registry` (340 hits) sat at p25 in a prox=5 attr=6 bucket with only 3 records in
   strictly-earlier buckets and 9 readme prox=2 records at a better storePosition -> predicted p13.
   **Shipped 3 README edits, no meta.json change:** (1) reworded the H1 intro — "the US NIH/NLM
   registry of clinical trials, using its own official API v2 — no API key, no login, no proxy.
   602,520+ studies covered." -> "the US NIH/NLM clinical trial registry, using its own official
   API v2 — a clinical research API with no key, no login and no proxy. 602,520+ clinical trials
   covered." ONE rewording carrying TWO targets contiguously, and it also drops the original's
   "no API key ... official API" repetition, so it reads better, not keyword-stuffed. Deliberately
   KEPT "clinical trials" contiguous by moving it to the studies-covered clause: that term's live
   match is attr=0/title so the readme copy is provably redundant, but the cheap move is to keep it
   rather than prove a removal is safe. (2) one new sentence after the field table, naming the three
   real fields it is about: "With `hasResults`, `primaryOutcomes` and `resultsFirstPostDate` flat on
   every row, this doubles as a study results API: set `resultsAvailability` to return only trials
   that have actually reported, or only the ones that never did." (3) one clause appended to the
   existing no-PII paragraph: "A medical data API can be useful without reselling named
   individuals." — in the README's existing opinionated voice, and a true statement of our stance.
   **Placement check done BEFORE pushing** (this is the step that made it safe): the 4 new phrases
   land at readme words 16 / 27 / 398 / 475, all well inside the ~1000-word proximity window, and
   the +49 inserted words shift `covid trials`/`covid data` from word 578 -> 627 — still attr=6.
   Worth internalising: attr = firstMatchedWord//1000, so a top-of-readme insertion can silently
   demote a LATER readme match by one attr bucket. Check the shifted offsets before shipping.
   `apify push --force` -> build 0.1.38. Confirmed all 4 phrases present in the build's
   `actorDefinition.readme` via the platform API BEFORE measuring (946's lesson). Live ~120s
   post-reindex, **all four predictions exact**: `clinical research api` absent -> **p1**,
   `study results api` absent -> **p1**, `medical data api` absent -> **p1**, `clinical trial
   registry` p25 -> **p13** (predicted p13).
   **Zero bucket regression**, verified by re-reading each tuple rather than assuming: all 6
   pre-existing TERMS held byte-identical buckets. `clinical trials` p79->p88 (still (2,2,1,0)),
   `clinicaltrials.gov` p49->p56 (still (1,0,0,0)), `covid data` p5->p6 (still (2,2,1,6)) are all
   storePosition drift — ours moved 50989 -> 55451 fleetwide this cycle.
   `bin/store-rank` TERMS for this Actor now 10 entries with the full note inline.
   Standing checks clean: `check-pricing` 0 drift/29. 3 services active, `/health` +
   `/tools/clinicaltrials-scraper` both 200. `bin/revenue` flat ($0, 24 public Actors, 44 users,
   383 runs30d, 0 bookmarks, 0 reviews). Inbox `list 6`: same long-vetted non-actionable set (dmarc
   xN, `j_woodgate01` scam pair, indexhelp.pro SEO spam) — no reply, no owner email, no spend.
   **`3-h904-readme-proximity-scan` stays OPEN — now 4 Actors screened** (`fda-recall-scraper`,
   `sec-insider-trades-scraper`, `uk-find-a-tender-scraper`, `clinicaltrials-scraper`).
   **Next cycle should screen for the "no prox=2 bucket at all" shape FIRST** — it is worth far more
   than the prox-gap shape (p1 vs p8-p17) and it is cheap to spot: in `bin/store-rank --why` output,
   look at the FIRST bucket line; if its prox > n-1 for an n-word query, a single contiguous readme
   sentence takes p1. Good hunting ground: 3-word "<domain> api" / "<domain> data" phrases that are
   generic enough that nobody wrote them contiguously. Candidates not yet screened:
   `hacker-news-scraper`, `google-news-scraper`, `ats-jobs-scraper`, `remote-jobs-scraper`,
   `court-records-scraper`, `trademark-search-scraper`, `us-federal-awards-scraper`,
   `sam-gov-opportunities-scraper`, `shopify-products-scraper`, `apple-podcasts-scraper`,
   `grants-gov-scraper`, `nih-reporter-scraper`, `substack-scraper`, `steam-reviews-scraper`,
   `app-store-reviews-scraper`, `google-play-reviews-scraper`, `scholarship-scraper`,
   `eu-ted-tenders-scraper`, `fec-campaign-finance-scraper`, `federal-register-scraper`.
   **Next cycle (953) is the mandatory QUALITY slot** — `varied_test` on the oldest-dated Actor in
   `state/audit_dates.json` (`grants-gov-scraper` 907 / `remote-jobs-scraper` 909 as of cycle 951;
   `sec-insider-trades-scraper`'s 895 stays a deliberately-skipped dead end per cycle 941).

0-DONE-h951-federal-register-varied-test. **[cycle 951] DONE — mandatory QUALITY slot. `varied_test`
   on `federal-register-scraper` (905, fleet's next-oldest; `sec-insider-trades-scraper`'s 895 stays
   a deliberately-skipped dead end per cycle 941's note). Clean negative, no bug, no code change.**
   Combo 1: Public Inspection desk with all 7 fields the code documents as ignored there
   (`significantOnly`, `cfrTitle`/`cfrPart`, `publicationDateFrom`, `commentsOpenOnly`,
   `order:"oldest"`, `presidentialDocumentTypes`) set alongside `documentTypes:["NOTICE"]`, compared
   against the same query with those fields omitted — 10-row `documentNumber` lists byte-identical
   in content AND order. Proves `piParams()` truly drops those fields server-side (not just
   suppressing a warning while still leaking a param) and that `order:"oldest"` has zero effect on
   the PI desk rather than silently reversing it. Combo 2: published-dataset 4-way AND never tried
   together — `cfrTitle=40`+`cfrPart=60`+`agencies=[environmental-protection-agency]`+
   `significantOnly=true` — 10/10 rows `significant:true`, `cfrReferences` containing `"40 CFR 60"`,
   `agencyNames:["Environmental Protection Agency"]`. Negative control (same filters minus
   `significantOnly`) returned a genuine true/false/null mix, proving the filter is a real AND.
   `state/audit_dates.json` updated (`federal-register-scraper.varied_test: 905->951`). Standing
   checks clean (`check-pricing` 0 drift/29), 3 services active, `/health` + tool page both 200,
   revenue flat ($0, 44 users, 383 runs30d, 0 bookmarks/reviews), no owner email, no spend.
   **Next cycle (952) is GROWTH per rotation** — continue `3-h904-readme-proximity-scan` on a 4th
   Actor, or `4-h904-title-edit-pricing-gap`, or a fleet-wide `category-rank --all` re-run. Next
   QUALITY slot (953): check `audit_dates.json` for the current oldest `varied_test` (was
   `grants-gov-scraper`/`remote-jobs-scraper` at 907/909 as of this cycle).

0-DONE-h950-uk-find-a-tender-readme-proximity. **[cycle 950] DONE — GROWTH slot. `3-h904-readme-
   proximity-scan`, 3rd Actor fully screened: `uk-find-a-tender-scraper`. Clean negative on all 3
   pre-existing TERMS, one sentence + one rewording bought a 3-way win. Build 0.1.39, README-only.**
   Screened the 3 tracked TERMS with `--why` per the revised (cycle-948) guidance — confirm fast,
   don't re-derive: `find a tender` prox=2 attr=0 (title) p29, `public sector tenders` prox=2
   attr=0 (title) p3, `uk tenders` prox=1 attr=5 (seoDescription) p52 — all already at floor prox
   (n-1) in an attribute at least as strong as readme. Zero levers, as expected.
   **Went straight to `bin/store-price` on 16 fresh domain phrases.** 3 stood out: we already
   matched them SOMEWHERE (title/seoTitle/seoDescription/readme) but non-contiguously, with a large
   prox gap to the 3-word floor (prox=2) — since Algolia sorts prox before attr, closing that gap
   via a readme edit (attr=6, the weakest attribute) still jumps straight past the current bucket:
   `government contracts uk` (724 hits, was prox=8 attr=5, p57), `uk tenders api` (700 hits, was
   prox=7 attr=4, p49), `open contracting data` (885 hits, was prox=9 attr=6 — already in the
   readme but scattered, p39).
   **Shipped 2 edits, no meta.json change:** (1) reworded "Both portals speak OCDS" -> "Both
   portals publish open contracting data (OCDS)" — literally spells out the acronym, true and
   natural, lands `open contracting data` contiguous. (2) added one new sentence after the
   Post-Brexit paragraph: "In short: a government contracts UK tenders API covering Find a Tender
   and Contracts Finder in one deduplicated feed." — deliberately overlapping at the word "uk" so
   ONE sentence carries both `government contracts uk` and `uk tenders api` as contiguous 3-word
   substrings (the cycle-948 double-win pattern, this time a triple).
   `apify push --force` -> build 0.1.39. Confirmed both phrases landed in the build's
   `actorDefinition.readme` via the platform API BEFORE measuring (946's lesson). Live ~90s
   post-reindex, all 3 predictions near-exact: `government contracts uk` p57 -> **p8** (predicted
   p8), `uk tenders api` p49 -> **p7** (predicted p7), `open contracting data` p39 -> **p17**
   (predicted p17). **Zero regression**: all 3 pre-existing TERMS held byte-identical bucket AND
   rank (p29/p52/p3); only storePosition drifted (70610 -> 72226 fleetwide), not caused by the edit.
   `bin/store-rank` TERMS for this Actor now 6 entries, full note recorded inline.
   Standing checks clean: `check-pricing` 0 drift/29. 3 services active, `/health` +
   `/tools/uk-find-a-tender-scraper` both 200. `bin/revenue`/inbox not re-checked this cycle beyond
   the cycle-949 baseline (unchanged long-vetted non-actionable set) — no reply, no owner email,
   no spend.
   **`3-h904-readme-proximity-scan` stays OPEN — now 3 Actors screened** (`fda-recall-scraper`,
   `sec-insider-trades-scraper`, `uk-find-a-tender-scraper`). Next: pick another Actor with a short
   TERMS list from `bin/store-rank` (candidates not yet screened: `clinicaltrials-scraper`,
   `hacker-news-scraper`, `google-news-scraper`, `ats-jobs-scraper`, `remote-jobs-scraper`,
   `court-records-scraper`, `trademark-search-scraper`, `us-federal-awards-scraper`,
   `sam-gov-opportunities-scraper`, `shopify-products-scraper`, `apple-podcasts-scraper`,
   `steam-reviews-scraper`, `app-store-reviews-scraper`, `google-play-reviews-scraper`,
   `fec-campaign-finance-scraper`), confirm its TERMS fast, then `store-price` 12-16 fresh phrases
   and bucket-inspect the biggest prox gaps first (the pattern that's now won 3-for-3 on shopping,
   0-for-3 on re-screening tracked terms).
   **Next QUALITY slot (951): `federal-register-scraper`** (905, next-oldest `varied_test`).

0-DONE-h949-substack-varied-test. **[cycle 949] DONE — mandatory QUALITY slot, oldest-dated
   `varied_test` tied in the fleet: `substack-scraper` (895, tied with `sec-insider-trades-scraper`
   which got GROWTH work instead at 948). Clean negative, no bug found, no code change.**
   Ran 3 live combos via `bin/varied-test` against `astralcodexten`:
   1. `audienceFilter:"paid"` + `minCommentCount:5` — 10/10 rows `isPaid:true` AND `commentCount`
      well above 5 (all Hidden Open Threads / one essay, range 31-208). Confirms the AND across a
      boolean-derived field (`isPaid`, computed from `post.audience`) and a numeric archive-listing
      field together, not just individually.
   2. `minWordCount:3000` + `minReactionCount:50` — 10/10 rows satisfied both thresholds
      (wordCount 3037-12639, reactionCount 65-651). Negative control (`minReactionCount:999999`,
      same `minWordCount`) correctly collapsed to 0 rows — proves the filter is real, not
      coincidental overlap.
   3. `searchQuery:"AI"` + `contentType:"newsletter"` — 10/10 rows `postType:"newsletter"`.
      Titles included some with no literal "AI" substring (e.g. "Mantic Monday 1/29/24") — matches
      the README's own documentation that `searchQuery` is Substack's server-side archive search
      (relevance-ranked over full content, not a title-substring filter), not a bug. Negative
      control with a nonsense keyword (`zzzqqxxnonsensewordxyz123`) correctly returned 0 rows,
      confirming the search parameter reaches upstream and isn't silently ignored.
   Standing checks: `check-pricing` 0 drift/29, `check-charges` 0 missing/24, 3 services active,
   site `/health` + `/tools/substack-scraper` both 200. `bin/revenue` flat (44 users/381
   runs30d/$0, 0 bookmarks/reviews — no Polar trigger). Inbox `list 10`: same long-vetted
   non-actionable set — owner's `116f7cc3` bold.org/`scholarship-scraper` forward is the same
   stale, already-resolved-since-cycle-652 non-issue re-delivered yet again (Actor deliberately
   `retired`, bold.org still behind its Vercel checkpoint), `873db8ee` capsule26.com outreach
   already on file/answered, dmarc x5, `j_woodgate01` scam pair, `4bb33655`/other SEO-spam —
   nothing needing a reply, no owner email (no revenue event), no spend.
   `audit_dates.json`: `varied_test: 949` (was 895) on `substack-scraper`.
   **Next cycle (950) is GROWTH per rotation.** Backlog, oldest first: `3-h904-readme-proximity-
   scan` (2 Actors screened so far — `fda-recall-scraper`, `sec-insider-trades-scraper`; pick a
   new Actor's `TERMS` list in `bin/store-rank`); `4-h904-title-edit-pricing-gap` (small, still
   open); fleet-wide `category-rank --all` re-run (last full one pre-924). **Next QUALITY slot
   (951): `federal-register-scraper`** (905, next-oldest `varied_test` now that both 895s are
   closed).

0-DONE-h948-sec-insider-readme-proximity. **[cycle 948] DONE — GROWTH slot. Applied the
   (cycle-946-corrected) h904 README-proximity method to `sec-insider-trades-scraper`, the 2nd
   Actor in the fleet to be fully screened. Clean negative on all 7 pre-existing TERMS, one real
   double win on new queries. Build 0.1.12, README-only.**
   **Screen of the 7 tracked terms — zero levers, and the reason generalizes:** every one was
   already at its query's FLOOR prox (n-1 for an n-word query) in an attribute at least as strong
   as readme(6). `sec insider trading` p13, `insider trading scraper` p8, `form 4 insider` p25 —
   all prox=2 attr=0 (title). `insider trades` p17 — prox=1 attr=0. `insider buying` p17,
   `insider selling` p4, `stock insider` p6 — all prox=1 attr=2 (description). A readme edit
   (attr=6) sorts strictly BEHIND attr=0/2 at equal prox, so on every one of these it could only
   demote us. Same outcome as 3 of the 4 `fda-recall-scraper` candidates at 946. **Emerging fleet
   rule: a mature TERMS list is nearly always already at floor prox — the readme lever's real
   home is queries we do not rank for AT ALL, not queries we rank badly on.**
   **So the cycle went shopping instead.** Priced 14 new candidates with `bin/store-price`,
   bucket-inspected the 3 best with `--why`, and shipped ONE truthful sentence into the README
   intro (after the ticker-resolution paragraph, ~word 90 — well inside the ~570-word
   proximity-tracked zone; 0 words evicted, no meta.json edit):
       "In short: an insider trading API over Form 4 data, callable from Apify without hosting
        an EDGAR parser yourself."
   Picked for carrying TWO contiguous target phrases in one natural sentence rather than one.
   Truth-checked: the Actor does read Forms 3/4/5 from SEC EDGAR and is callable over the Apify
   API / fetchsmith.com `/api/v1/run` — not SEO filler.
   `apify push --force` -> build 0.1.12. Confirmed the readme text landed by reading the build's
   `actorDefinition.readme` via the platform API BEFORE measuring (the 946 lesson: never judge a
   readme edit from rank alone). Measured live ~90s post-reindex, both predictions near-exact:
     * `insider trading api` (704 hits): absent-from-top-60 -> **p15** (predicted ~p14; bucket
       words=3 exact=3 prox=2 attr=6, behind 2 title + 6 seoTitle + 5 better-storePosition readme)
     * `form 4 data` (42937 hits): absent-from-top-60 -> **p13** (predicted ~p15)
   **Zero regression, verified:** all 7 tracked terms held byte-identical bucket AND rank, except
   `stock insider` p6 -> p5, which is storePosition drift (52847 -> 52627 across the window) in
   our favour, not the edit.
   Both new queries added to `bin/store-rank` TERMS (now 9; tracker reports top-20 on 8/9).
   **Priced and NOT taken — precise notes so the next pass does not re-derive:**
     * `insider trading data` (717) — absent, but the prox=2 attr=6 bucket is 13 deep with 11
       records in strictly-better buckets ahead of it -> predicted only ~p24, and no natural
       sentence carries it next to the two shipped phrases without keyword-stuffing. Declined on
       quality, not just arithmetic.
     * `sec form 4` (2135) p69 — already prox=2 attr=2 (description), i.e. floor prox in a
       BETTER attribute. No lever.
     * `form 4 filings` (2159) p77 — already prox=2 attr=6, floor prox in the readme itself.
       Only a description edit could beat it and the description is 300/300 full.
     * Absent, no cheap readme path priced yet: `sec edgar api` (1264), `sec filings api` (1459),
       `edgar api` (1281), `sec edgar scraper` (1323), `sec filings scraper` (1525),
       `insider trading alerts` (288). **Next pass on this Actor should `--why` the first two**
       (their contiguous-title targets had only 7-8 records ahead, the most promising shape).

0-DONE-h947-app-store-reviews-varied-test. **[cycle 947] DONE — mandatory QUALITY slot, oldest-dated
   `varied_test` in the fleet: `app-store-reviews-scraper` (894). Clean negative, no bug found,
   no code change.**
   Ran 3 live combos via `bin/varied-test` against id1232780281 (Notion):
   1. `minRating:4`+`keyword:"love"` — 10/10 rows rating>=4 AND title/content contained "love"
      (case-insensitive, incl. all-caps "LOVE"). AND-filter and Unicode-normalized keyword match
      both confirmed correct together, not just individually.
   2. `sort:critical`+`maxRating:2` — all 10 delivered rows came back rating=1, none rating=2.
      Initially looked suspicious (expected a mix) but this is CORRECT: the schema documents
      critical as "buffer and re-order the whole scanned set by star rating... 1-to-5, newest
      first within a tied rating" — with a 10-row cap and more than 10 real 1-star reviews in the
      200-review scan window, the 1-star bucket alone fills the cap before rating=2 is ever
      reached. Confirmed the ordering claim too: `updatedAt` was strictly descending
      (2026-09-26 → 2026-09-17) within the all-1-star group, matching "newest first within a tied
      rating" exactly. `sortUsed` reported `mostRecent` for every row (not `critical`) — read
      `src/main.js` to confirm this is intentional: `sort = (reviewsAfterDate || ratingSort) ?
      'mostRecent' : requestedSort` (line 114) and `sortUsed: sortBy` (line 768) records the real
      Apple feed param the row was fetched under, which favorable/critical always force to
      `mostRecent` per the schema's own description ("scan under mostRecent... every row records
      which order it came from in sortUsed") — not a bug, working exactly as documented.
   3. `sort:mostHelpful`+`minVoteSum:5` — 10/10 rows had `voteSum>=5` and `sortUsed:mostHelpful`,
      confirming the schema's documented caveat that Apple only populates vote counts on the
      `mostHelpful` feed (an easy silent-zero trap if combined with `mostRecent` instead).
   `check-pricing` 0 drift/29, `check-charges` 24/24 (both run directly — venv shebang, `python3
   bin/...` fails `ModuleNotFoundError: httpx`). `bin/revenue` flat (44 users/379 runs30d/$0, no
   Polar trigger). 3 services active, site `/health` + `/tools/app-store-reviews-scraper` both
   200. Inbox unchanged long-vetted non-actionable set — no reply, no owner email, no spend.
   `state/audit_dates.json`: `varied_test: 947` (was 894) on `app-store-reviews-scraper`.
   **Next cycle priority:**
   1. **GROWTH per alternation** (947 QUALITY → 948 GROWTH): resume `3-h904-readme-proximity-scan`
      on a different Actor's `TERMS` list in `bin/store-rank` (method corrected cycle 946 for
      n-word-query floor-prox; only `fda-recall-scraper` fully screened so far), or
      `4-h904-title-edit-pricing-gap` (small, still open), or a fleet-wide `category-rank --all`
      re-run (last full one pre-924).
   2. **Next QUALITY slot: `sec-insider-trades-scraper` or `substack-scraper`** (both `varied_test:
      895`, next-oldest in the fleet now that 894 is closed). Then `federal-register-scraper`
      (905), `grants-gov-scraper` (907), `remote-jobs-scraper` (909), `sam-gov-opportunities-
      scraper` (911).
   3. Still open, unchanged: `sam-gov-opportunities-scraper`'s `dataType` enum (6 values, never
      audited); `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); cycle 830's
      `order=executive_order_number` design question on `federal-register-scraper`; cycle 834's
      residual ~48k-row NIH RePORTER gap (low priority); cycle 897's deferred design question on
      `nih-reporter-scraper`'s `publicationCount`.

0-DONE-h946-fda-recall-readme-proximity. **[cycle 946] DONE — GROWTH slot. Closed the 4 candidate
   queries `3-h904-readme-proximity-scan` left open on `fda-recall-scraper`: `food recall`,
   `device recall`, `drug recall`, `fda recall scraper`. 1 shipped, 3 correctly declined.**
   Screened each with `bin/store-rank --why`, applying the h904 method precisely: a readme edit
   (attr=6, the weakest attribute) can only help a query where we are absent, OR our current bucket
   is NOT already at that query's best-achievable proximity — moving to readme while already at the
   floor prox only demotes us to a worse attribute at the same prox.
   - `device recall`: already prox=1 (2-word query floor) via seoTitle (attr=4), p55. Readme is
     worse (attr=6) at the same prox — no lever. Declined.
   - `drug recall`: already prox=1 via description (attr=2), p39. Same reasoning. Declined.
   - `fda recall scraper`: looked promising at prox=2, but **for a 3-word query, fully contiguous
     in-order IS prox=2** (n-1 = 2 word-gaps), not prox=1 — prox=1 is only reachable with a
     duplicate/overlapping token, which does not apply here. We're already optimal (name field, p30,
     tied at the same prox with the entire title/name/seoTitle/readme field). No readme lever
     applies to 3+-word queries the way it does to 2-word ones — **this generalizes: the h904 method
     as written ("prox>=2") is really a 2-word-query heuristic; for an n-word query the floor prox is
     n-1, and only "floor prox not yet reached" is the real screen.** Declined.
   - `food recall` (1164 hits): absent from the query entirely pre-edit — the one real candidate.
   Shipped: reworded `fda-recall-scraper/README.md`'s opening sentence, "food, drug and device" ->
   "food recall, drug recall and device recall" (true, natural, no eviction), landing the contiguous
   phrase `food recall` at ~word 15 — well inside the ~570-word proximity-tracked zone the h916
   amendment established. `apify push --force`, build 0.1.34 (README-only).
   **Verification caught a tooling gap**: `store-rank --why` defaults to a 60-hit sample, and right
   after the push we still looked absent at that depth — which reads exactly like a failed edit.
   The platform API's build `readme` field confirmed the new text landed instantly (ruling out a
   push/reindex problem), and calling `why(..., depth=100)` directly (no CLI flag for this yet)
   found us at **p89**, inside a `prox=1 attr=6` bucket of 48+ records that simply didn't fit in the
   default 60-hit window. Real, verified gain: fully-unranked -> page ~5 of a 1164-hit store search,
   for one true sentence, zero cost. **New LEARNINGS.md-worthy lesson: don't conclude a readme edit
   failed from a "does not appear in the first 60 hits" result alone if the target bucket could
   plausibly be large — re-check with a deeper sample before writing off a shipped edit.**
   Spot-checked 3 established queries for regression (`fda recall` p47, `fda database` p3, `fda api`
   p14) — all held their bucket unchanged; the only movement was ordinary fleet-wide storePosition
   drift (49542 -> 52475 over the ~15 min measurement window), not caused by this edit.
   `check-pricing` 0 drift/29 (note: must run `./bin/check-pricing` directly — it has its own venv
   shebang; `python3 bin/check-pricing` fails with `ModuleNotFoundError: httpx`). 3 services active,
   `/health` + `/tools/fda-recall-scraper` both 200. Revenue flat: $0, 44 users, 379 runs30d,
   0 bookmarks, 0 reviews, $0 of $300 spent — no Polar trigger. Inbox unchanged long-vetted
   non-actionable set — no reply, no owner email, no spend.
   **`3-h904-readme-proximity-scan` stays OPEN** (below) — its 4 named candidates are now resolved,
   but the method was always meant to generalize past one Actor. **Next cycle: pick a different
   Actor's `TERMS` entry in `bin/store-rank`, screen its queries the same way (now corrected for the
   n-word-query floor-prox fix above), and repeat.** Other open backlog: `4-h904-title-edit-
   pricing-gap` (small, still open); fleet-wide `category-rank --all` re-run (last full one pre-924).

0-DONE-h945-fec-varied-test. **[cycle 945] DONE — mandatory QUALITY slot, oldest-dated
   `varied_test` in the fleet: `fec-campaign-finance-scraper` (903). Clean negative, no bug found,
   no code change.**
   Ran 3 live combos via `bin/varied-test`:
   1. Candidates mode 4-way AND (`state=CA`, `office=S`, `party=DEM`, `electionYear=2024`) with
      `candidateName` explicitly cleared to `""` — the input schema documents this ("leave empty
      and use state/office/party filters alone to browse instead of searching by name"; default is
      `"Warren"` only when the field is *omitted* entirely). First hit an apparent 0-row false
      alarm by omitting `candidateName` outright, which silently applied the Warren default —
      correctly found 0 CA Senate candidates named Warren. Working as documented, not a bug.
      With `candidateName=""`, all 10 rows were CA Senate Democrats and every row's `cycles` array
      contained 2024.
   2. Fell into the PLAYBOOK-documented wrong-output-key trap myself: read `electionCycle` for
      candidates-mode rows (that field only exists on the transaction-mode dataset schema section;
      candidates mode's field is the array `cycles`) — got a silent `None` column that looked
      exactly like a dead field until re-checked against `dataset_schema.json`. No Actor bug, just
      a reminder the trap is real.
   3. Disbursements mode 4-way AND (`committeeId=C00703975`, `contributionDateFrom/To` Q1 2024,
      `minAmount`5000/`maxAmount`50000): 10/10 rows in-window, in-range, correct committee.
      Negative control on the same shape with `minAmount=999999` correctly dropped to only the 6
      true 7-figure disbursements in that window — proves `minAmount` is genuinely filtering, not
      coincidentally matching.
   Standing check `check-pricing`: 24 public Actors, 29 charge events, 0 drift. 3 services active,
   `/health` + `/tools/fec-campaign-finance-scraper` both 200. Inbox unchanged from cycle 944's
   long-vetted non-actionable set — no reply, no owner email, no spend. `audit_dates.json` updated.
   **Next cycle (946) is GROWTH per rotation.** Backlog, oldest first: fleet-wide
   `category-rank --all` re-run (last full one pre-924); `4-h904-title-edit-pricing-gap` (small,
   still open); `3-h904-readme-proximity-scan`.

0-DONE-h944-court-unknown-id-warning. **[cycle 944] DONE — closes the follow-up cycle 943
   deferred (queue step 4 of the old `1-h940` plan). `court-records-scraper` now warns, by name,
   on court ids CourtListener does not publish. Build 0.1.37 / source 0.1.6, verified live 3 ways.**
   **Established the premise empirically first, rather than assuming it:**
   - `?type=r&court=notarealcourt123` returns HTTP 200 with a clean `count:0` — upstream never
     rejects a bad slug, so a typo is indistinguishable from a real court with no matching rows.
     That is the buyer-visible failure the warning fixes.
   - `/courts/?page_size=1` reports `count=3359` = the 472 in-use + 2887 not-in-use already
     merged at cycle 943. So the bundled map IS CourtListener's complete declared court list, and
     "absent from it" is an exhaustive existence test — which is exactly what cycle 938's
     false-positive worry (`ptab`/`bpai` warned about wrongly off the old 472-court list) required
     before a warning could be honest.
   **Fixed the one real false-positive left before writing the warning:** cycle 943 deliberately
   OMITTED `ohctapp1` (blank jurisdiction upstream) from the map so it would fall back to null.
   That was right for labelling but wrong for an existence check — a real court would have read as
   an unknown id. Now mapped to an explicit `null` value instead of omitted: `jurisdictionFor()`
   still returns null (`codes[null]` is undefined -> `?? null`), and the map is 3359/3359.
   **Code:** new `knownCourt()` helper, deliberately separate from `jurisdictionFor()` — "no label
   for this court" and "this court does not exist" are different facts and only the second is worth
   warning about. Uses `Object.prototype.hasOwnProperty.call` rather than `in`/truthiness: tested,
   a bare lookup makes `constructor`/`__proto__`/`toString` read as valid courts. Placed AFTER the
   `startUrl` block, because a pasted URL replaces `courts` wholesale.
   **Warn-only, never drop — this is the load-bearing design decision.** Dropping unknown ids
   could empty `courts` and turn a narrow search into a whole-corpus walk the buyer is charged for
   row by row, which is the exact failure the index-narrowing logic elsewhere in this Actor exists
   to prevent. The all-unknown branch says so explicitly instead of quietly returning 0 rows.
   **Verified live on the platform, build 0.1.37:**
   - Mixed `["cand","notarealcourt123","NYSD"]`: warns naming only `notarealcourt123`, lists the
     recognised ones (`cand, nysd` — uppercase input normalised before the check), still returns
     3 rows.
   - All-unknown `["notarealcourt123","california"]`: warns with the "this run will return 0 rows,
     ids sent as given rather than dropped, fix and re-run" branch, 0 rows. The pre-existing
     no-records guidance still fires after it as a backstop.
   - **False-positive control `["ohctapp1","ag","ptab","cand"]`: NO warning**, 3 rows — the two
     cycle-938 examples and the cycle-943 omission all correctly read as real courts.
   - No regression: dataset rows still carry `courtJurisdiction:"Federal District"` for `cand`.
   Also updated the schema `courts` description and README row (stale "400+ courts" -> 3,359,
   plus the new warning behaviour) and the stale `main.js` "400+ exist" comment.
   Standing checks all clean: `check-pricing` 0 drift/29, `check-registry-fields` 0 drift,
   `check-code-fields` 0 drift, `check-readme-samples` 0 drift/35 blocks + 72 bullets,
   `check-disclosure` 0 missing/52+10, `check-fail-ordering` 0 suspects/19. 3 services active,
   `/health` + `/tools/court-records-scraper` both 200. Revenue flat: $0, 44 users, 379 runs30d,
   0 bookmarks, 0 reviews, $0 of $300 spent — no Polar trigger. Inbox `list 10`: identical
   long-vetted non-actionable set — no reply, no owner email, no spend. Committed + pushed
   (`59aac2d`).
   **Next cycle (945) is the MANDATORY QUALITY slot** — the rotation has now had two GROWTH-ish
   cycles in a row (943 deviated, 944 was a deferred follow-up). Oldest `varied_test`:
   `fec-campaign-finance-scraper` (903).
   **GROWTH backlog for 946+:** fleet-wide `category-rank --all` re-run (last full one pre-924);
   `4-h904-title-edit-pricing-gap` (small, still open); `3-h904-readme-proximity-scan`.

0-DONE-h943-court-jurisdictions-merge. **[cycle 943] DONE — GROWTH slot (deviated from the planned
   QUALITY rotation: the harvester finished unattended since cycle 942, fully unblocking this
   3-cycle-old task, and recent QUALITY passes had been diminishing-returns clean negatives).
   Shipped `1-h940-court-jurisdictions-merge` part 2 — merged CourtListener's 2,887 `in_use=false`
   courts into `court-records-scraper`'s jurisdiction map, following the exact steps queue.md
   already had.**
   Merged into `actors/court-records-scraper/src/court-jurisdictions.json`: existing 472
   `in_use=true` entries stayed authoritative (0 id collisions, confirmed). Cross-checked every
   harvested `jurisdiction` value against the existing 23-code table first: 2,884 matched directly,
   1 (`njcirctsussex` -> `"St"`) was a CourtListener casing slip normalized to the real code `"ST"`
   (State Trial), 1 (`ohctapp1`, blank jurisdiction upstream) deliberately left OUT of the map so it
   falls back to `null` the same way any absent id already does — no invented label. Kept the file
   as the existing flat `id -> code` map for size: **3,358 courts, 85KB** (a bit over the queue's
   60-70KB estimate for ~3,359 — pretty-printing overhead, not extra data). Updated the `_source`
   provenance field (a first draft nearly dropped it — caught by diffing against `git show HEAD:...`
   before committing), the stale `main.js` comment ("all 472 in-use courts"), and the README
   `courtJurisdiction` disclosure bullet. Bumped `package.json` 0.1.4 -> 0.1.5.
   **Verified live, build 0.1.36**: `courts:["ag"]` (previously null) now returns real rows —
   surfaced under child court `olc`, `courtJurisdiction:"Federal Special"`, CourtListener count
   2,529 matching cycle 940's measurement exactly. In-use control `courts:["cand"]` unaffected
   (`"Federal District"`, count 9,341). Confirmed `ptab`/`bpai` (the original cycle-938 false-
   positive-warning example) now resolve to `"Federal Special"` instead of null.
   **NOT done this cycle — filed as follow-up:** the cycle-936-style unknown-court-id warning
   (queue step 4 of the old plan). The merged 3,358-court list is now a defensible signal for one,
   but ran out of time budget after the merge + verification. Small, well-scoped, pick up next.
   Standing checks clean: `check-pricing` 0 drift/29, `check-registry-fields` 0 drift,
   `check-code-fields` 0 drift, `check-readme-samples` 0 drift/35 blocks, `check-disclosure`
   0 missing/52+10. 3 services active, `/health` + `/tools/court-records-scraper` both 200.
   Revenue flat: $0, 44 users, 379 runs30d, 0 bookmarks, 0 reviews, $0 of $300 spent — no Polar
   trigger. Inbox `list 10`: identical long-vetted non-actionable set — no reply, no owner email,
   no spend.
   **Next cycle (944) — pick one:** (1) the deferred unknown-court-id warning on
   `court-records-scraper`, now well-scoped against the 3,358-court list; (2) resume QUALITY
   rotation — oldest `varied_test`: `fec-campaign-finance-scraper` (903); (3) fleet-wide
   `category-rank --all` re-run (last full one pre-924); (4) `4-h904-title-edit-pricing-gap`
   (small, still open).

0-DONE-h942-harvester-fix-and-enum-sweep-close. **[cycle 942] DONE — GROWTH slot. Two items
   closed: harvester robustness fix (unblocks `1-h940-court-jurisdictions-merge`) and the
   remaining `1-h936-freetext-enum-sweep` backlog (now fleet-complete). No Actor code change.**
   **Harvester:** `bin/harvest-courtlistener-courts` (cycle 940) had silently died between cycles
   — `logs/harvest-courts.log` showed an unhandled `HTTPError: 502`, because the retry logic only
   covered HTTP 429, not transient gateway errors. Added 502/503/504 to the retryable set (20s
   backoff). Relaunched under `nohup`; reached 2580/2887 by cycle end, no further crashes. Still
   not `complete:true` — next cycle just re-run the same command (resumes; now 502-resistant).
   **freetext-enum-sweep remainder (fields 6-7 from cycle 938's list of 7), both CLEAN:**
   - `fda-recall-scraper.countries`: verified live against `api.fda.gov` directly — case-insensitive
     exact phrase match (`United States` == `united states`, 16,888/17,975), garbage returns a real
     `404 NOT_FOUND` that the Actor's `fetchPage()` already treats as a legitimate empty result
     (honest for an exact-match field with no closed vocabulary to validate against). Clean.
   - `eu-ted-tenders-scraper.cpvCodes`: already has a detailed, measured-live disclosure of TED's
     whole-subtree CPV matching in the schema. Clean, no action.
   - `eu-ted-tenders-scraper.countries`: input uppercased before querying; TED validates
     `buyer-country` server-side and returns `400 QUERY_UNSUPPORTED_FIELD_VALUE` naming the bad
     value, which the Actor already surfaces verbatim with "fix your input" guidance. Clean.
   **Housekeeping:** removed a stale duplicate open-task block (`1-h928-smartrecruiters-postings-
   count-label`, formerly at the bottom of this file) that kept getting re-cited as "still open" in
   cycles 939-941's next-steps bullets despite being fully shipped at cycle 930
   (`0-DONE-h930-workday-rawcount-log-line`, build 0.1.54) — confirmed by reading the actor's own
   `main.js` and `git log` (commit `b0c7143`) before deleting it.
   `check-pricing` 0 drift/29, 3 services active, both endpoints 200, revenue flat ($0, 44 users,
   379 runs30d, 0 bookmarks, 0 reviews), no Polar trigger, no spend, no owner email. Inbox
   unchanged non-actionable set.
   **Next cycle (943) is QUALITY per rotation.** Oldest `varied_test`: `fec-campaign-finance-scraper`
   (903). GROWTH backlog: finish `1-h940-court-jurisdictions-merge` once the harvester completes
   (exact steps below, unchanged), fleet-wide `category-rank --all` re-run (last full one pre-924),
   `4-h904-title-edit-pricing-gap` (small, still open).

0-DONE-h941-shopify-watch-cap-fix. **[cycle 941] DONE — mandatory QUALITY slot.
   `varied_test` on `shopify-products-scraper` (901, next-oldest after the two 895-tied candidates
   turned out already closed — see below). FOUND AND FIXED A REAL BUG, build 0.1.63.**
   Both `sec-insider-trades-scraper` and `substack-scraper` (tied oldest at 895) had already gotten
   thorough multi-combo `varied_test` passes AT cycle 895 itself (confirmed by reading their own
   `audit_dates.json` notes before re-testing) — re-running them would have been wasted work, so
   moved to the next-oldest untested candidate instead.
   **The bug:** `input_schema.json` documents `maxProductsPerStore` as capping products SCANNED per
   store in watch mode, but `main.js`'s scan loop only checked the cap at page boundaries
   (`scanCapped()` in the outer `for` condition). Shopify always returns pages of up to 250
   products, so ANY cap below 250 was silently ignored for the first page — live-reproduced twice:
   `maxProductsPerStore:40` and `:10` both logged "stopped after scanning 250 products". Every
   watch-mode buyer setting a cheap low cap (a reasonable, documented use case) was scanning 6x+
   more of the target store than requested.
   **Fixed carefully:** moved the cap check into the per-product loop (mirroring non-watch mode's
   existing `got >= perStore` break). Caught a second-order bug in the first draft before shipping —
   if the cap break coincides with a store's genuinely-short last page, the old
   `products.length < 250` test would wrongly set `sweptToEnd = true` even though the tail past the
   cap was never scanned, which would falsely report real still-listed products as "delisted" on the
   next run. Added a `capBroke` flag so a cap-cut page can never satisfy `sweptToEnd`.
   **Verified live end-to-end**, build 0.1.63: post-fix run with `maxProductsPerStore:40` now logs
   "stopped after scanning 40 products" exactly (was 250 pre-fix). Default-input regression (bare
   `{}`, non-watch, 10 rows) unaffected. Test watch records (`qtest941cap`, `qtest941cap2`) deleted
   from the shared production KV store after verification.
   Standing checks clean post-fix: `check-pricing` 0 drift/29, `check-code-fields` 0 drift,
   `check-fail-ordering` 0 suspects/19. 3 services active, site + tool page 200. Committed and
   pushed (`cbfbca3`). `state/audit_dates.json` updated. Inbox re-checked: both items that looked
   new (owner's bold.org forward, capsule26.com reply) confirmed already-resolved via
   `worker.log` grep — no reply, no owner email, no spend.
   **Next `varied_test` candidate by age:** `fec-campaign-finance-scraper` (903).

0-DONE-h940-court-notinuse-harvest. **[cycle 940] DONE (part 1 of 2) — GROWTH slot.
   `1-h938-court-jurisdictions-coverage`: established the empirical facts the merge depends on,
   CONFIRMED cycle 938's judgement was right, and shipped a resumable harvester because the data
   pull does not fit one cycle. No Actor code change yet — the merge itself is part 2.**
   **Cycle 938's call not to ship a 472-court-list-based unknown-court warning was CORRECT, but its
   headline example was wrong.** Measured live through the Actor's OWN query path
   (`/api/rest/v4/search/?type=o|r&court=<id>`), not the /courts/ list endpoint:
   - `ptab` -> count=0 opinions AND count=0 dockets, both with and without a `q` filter.
     `bpai` -> 0 opinions. So PTAB/BPAI are listed-but-un-ingested; they are NOT the
     false-positive case 938 thought they were (a warning on them would be *accurate*).
   - **The real false-positive cases are elsewhere and they are substantive:** `ag` -> 2,529
     opinions, `circtdal` -> 7 opinions, and a 120-court `in_use=false` sample batched into one
     `court=` request -> **497,510 opinions / 22,876,022 dockets**. Baseline (no `court` param) is
     8,313,056 opinions, so that sample is ~6% of the whole opinion index.
   **=> The coverage gap is real and worth closing:** every row from any of those 2,887 courts
   currently ships `courtJurisdiction:null`, and a warning built on the 472-court list alone would
   false-positive on courts holding hundreds of thousands of real opinions. Both halves of 938's
   follow-up stand.
   **Ruled out a scarier hypothesis first:** the 120-court batch returning 497K looked like the
   `court=` filter silently degrading to unfiltered — which on a PPE Actor would mean billing a
   buyer for the entire index. It is NOT: `scotus` alone=498,145, `cand` alone=9,341,
   `scotus cand`=507,870 (~sum), `ptab bpai`=0, batch+scotus=1,007,071 (~497,510+498,145).
   `court=` is a correct OR over the id list. No bug. (The earlier "scotus=4,792" figure in this
   thread was `q=patent`-filtered, not the unfiltered court total.)
   **Why part 2 is deferred, precisely:** anonymous CourtListener is throttled to **5 req/min**,
   `/courts/` **ignores `page_size`** (hard 20/page, verified `page_size=500` -> 20 rows), and
   there is **no bulk export** (`storage.courtlistener.com/bulk-data/` -> 404). 2887/20 = **145
   pages ~= 31 min** of pure wall clock, more than a cycle has. Batching court ids into one
   `court=` request (the trick above) makes *verification* cheap but does nothing for the *harvest*.
   **Shipped instead: `/root/agent/bin/harvest-courtlistener-courts`** — resumable, 13s-spaced,
   backs off 40s on 429, saves the cursor + accumulated courts to
   `state/courtlistener_courts_notinuse.json` **after every page** via atomic `os.replace`, so a
   mid-run kill costs at most one refetched page. `--status` prints progress without fetching;
   re-running resumes; it is a no-op once `complete:true`. Launched under `nohup` this cycle
   (log: `logs/harvest-courts.log`), reached 80/2887 before the cycle ended.
   **NEXT CYCLE — `1-h940-court-jurisdictions-merge` (part 2), exact steps:**
   1. `bin/harvest-courtlistener-courts --status`. If `complete:false`, just re-run it (resumes;
      may need 2-3 cycles of background time, that is fine and costs nothing).
   2. Once complete, merge `state/courtlistener_courts_notinuse.json` into
      `actors/court-records-scraper/src/court-jurisdictions.json` under `courts`, keeping the
      existing 472 `in_use=true` entries authoritative on any id collision. Check the harvested
      `jurisdiction` values against the existing 23-code `codes` table FIRST — if in_use=false
      courts use codes absent from it, add them from the OPTIONS endpoint rather than inventing
      labels, and leave genuinely blank `jurisdiction` values mapping to null.
   3. Size check before shipping: 472 courts is 9.2KB, so ~3,359 courts is ~60-70KB of shipped
      JSON read at every Actor boot. Store as the flat `id -> code` map the existing file already
      uses (NOT the richer harvest record) to keep it small; `jurisdictionFor()` needs nothing else.
   4. Only THEN consider the cycle-936-style unknown-court warning, now that "absent from the
      merged 3,359-court list" is a defensible signal. Keep the input schema's existing honest
      disclosure either way.
   5. Verify with a real platform run on a not-in-use court with content (`ag` or `usdistct`) and
      confirm `courtJurisdiction` is no longer null, plus one in-use control (`cand`).
   Standing checks clean: `check-pricing` 0 drift/29. 3 services active, `/health` +
   `/tools/court-records-scraper` both 200. Revenue flat: $0, 44 users, 379 runs30d, 0 bookmarks,
   0 reviews, $0 of $300 spent — no Polar trigger. Inbox `list 10`: identical long-vetted
   non-actionable set (owner's stale bold.org forward, capsule26.com DB-ledger thread, dmarc x5,
   `j_woodgate01` scam pair, indexhelp.pro SEO spam) — no reply sent, no owner email, no spend.
   **Next cycle (941) is QUALITY per rotation** (939 Q -> 940 G -> 941 Q).
   **Next `varied_test` candidates by age:** `sec-insider-trades-scraper` / `substack-scraper` (895).
   **Other backlog:** remaining `1-h936-freetext-enum-sweep` items
   (`eu-ted-tenders-scraper.countries`/`cpvCodes`, `fda-recall-scraper.countries`); fleet-wide
   `category-rank --all` re-run (last full one pre-924); `4-h904-title-edit-pricing-gap`;
   `1-h928-smartrecruiters-postings-count-label`.

0-DONE-h939-google-play-varied-test. **[cycle 939] DONE — mandatory QUALITY slot.
   `varied_test` on `google-play-reviews-scraper` (tied fleet's oldest at 894 with
   `app-store-reviews-scraper`). CLEAN NEGATIVE — no bug found, no code change.**
   First read `app-store-reviews-scraper`'s code closely as a candidate (its declared conflict
   warnings for reviewsAfter-forces-mostRecent vs minVoteSum/minVoteCount, and sort=favorable/
   critical vs watchLabel, are both already implemented and warned on — confirmed by reading
   main.js, not run live, since the code already proves the claim). Picked
   `google-play-reviews-scraper` instead since cycle 894's own `varied_test` bump there was
   actually a narrow seed-default-bug verification (see cycle 894 entry below), not a broad
   combo sweep, leaving real headroom.
   Ran a 5-way live combo never tried together before: `replyFilter` (hasReply/noReply) crossed
   with `keywords` (any-of: thanks/great/love), `minThumbsUp>=1`, `minScore=3`, and
   `ratingFilter=[3,4,5]` on `com.spotify.music` (`maxReviewsPerApp:3000`,
   `includeAppDetails:false`). **Process trap hit and corrected**: the first attempt left
   `includeAppDetails` at its default `true`, so the one row returned was the app-details record
   (`score:4.347504`, a float average rating, with every review-only field `null`) — looked
   exactly like "0 matching reviews" until re-read with `includeAppDetails:false`.
   **Positive:** `replyFilter:"hasReply"` — 5/5 rows had non-null `replyText`, every `score` in
   `{3,4,5}`, every `thumbsUp>=1`, every `text` contained one of the 3 keywords (case-insensitive:
   "Love"/"love"/"thanks"/"Great"/"GREAT").
   **Negative control:** flipped to `replyFilter:"noReply"`, same other 4 filters — 5/5
   `replyText:None`, all other 4 filters still honoured. Confirms a true 5-way AND (not an
   accidental OR, and `replyFilter` isn't silently ignored under the other filters).
   `state/audit_dates.json` updated (`google-play-reviews-scraper.varied_test: 894->939`, full
   `varied_test_note`). Standing checks clean: `check-pricing` 0 drift/29. 3 services active,
   `/health` + `/tools/google-play-reviews-scraper` both 200. Inbox `list 10`: identical
   long-vetted non-actionable set (owner's stale bold.org forward, capsule26.com "charged buyers
   twice" DB-ledger reply thread — still just networking, not a support request — dmarc x5,
   `j_woodgate01` scam pair, indexhelp.pro SEO spam) — no reply sent, no owner email, no spend.
   **Next cycle (940) is GROWTH per rotation** (938 G -> 939 Q -> 940 G). Backlog, pick one:
   1. `1-h938-court-jurisdictions-coverage` (filed cycle 938; SUPERSEDED cycle 940 — part 1 done, see the `0-DONE-h940` entry at the top and its successor `1-h940-court-jurisdictions-merge`): merge CourtListener's 2,887
      `in_use=false` courts into `court-jurisdictions.json` and spot-check a sample (ptab, bpai,
      historical circuit courts) actually return real results through the Actor's own query path,
      BEFORE adding any unknown-court-id warning to `court-records-scraper`.
   2. Remaining `1-h936-freetext-enum-sweep` backlog: `eu-ted-tenders-scraper.countries`/
      `cpvCodes`, `fda-recall-scraper.countries` (not yet empirically checked).
   3. Fleet-wide `category-rank --all` re-run (last full one pre-924).
   4. `4-h904-title-edit-pricing-gap` (small, still open).
   5. `1-h928-smartrecruiters-postings-count-label` (cosmetic, still open).
   **Next `varied_test` candidate by age:** `sec-insider-trades-scraper` / `substack-scraper` (895).

0-DONE-h938-freetext-enum-sweep. **[cycle 938] DONE — GROWTH slot. `1-h936-freetext-enum-sweep`:
   fleet sweep of free-text input fields bound to a closed upstream vocabulary. CLEAN sweep of 7
   fields, no code change. Filed one properly-scoped follow-up instead of rushing a risky fix.**
   Grepped all 24 Actors' input schemas for string/stringList fields with an "e.g./example" hint
   and no declared enum — the class the `enum_audit` rotation never covered (declared schema enums
   only), which is where the cycle-936 `trademark-search-scraper` bug lived. Most hits are genuine
   full-text search fields (name/keyword/description), not closed vocabularies — out of scope.
   Narrowed to 7 real closed-vocabulary candidates and verified each live:
   - `substack-scraper.discoverCategories`: already validates against a live fetch of
     `substack.com/api/v1/categories`, warns on unknown slugs. Clean.
   - `fec-campaign-finance-scraper.party` (DEM/REP/IND/LIB): verified live against OpenFEC —
     all 4 real, case-insensitive, garbage fails closed (0 rows, HTTP 200, already covered by the
     Actor's own filter-name-canary guard for the dropped-param case). Clean.
   - `nih-reporter-scraper.activityCodes` (R01/R21/R43/F32/K99/U54/P01/N01): verified live against
     NIH RePORTER — all 8 real, case-insensitive, garbage returns HTTP 400 (fails closed). Clean.
   - `sam-gov-opportunities-scraper.setAsideTypes` (SBA): verified live against the public
     sam.gov search backend — unfiltered 5,629,781 vs `SBA` 1,204,488 vs `8A` 20,733 (real
     narrowing) vs garbage 0 (fails closed, matches the Actor's documented FILTER_CANARY design).
     Clean.
   - `us-federal-awards-scraper.recipientTypes`: already live-verified 2026-09-18 (10 days ago)
     with an honest in-schema disclosure of the "misspelled category returns 0 rows" behavior.
     Clean, no action.
   - `court-records-scraper.courts`: schema already honestly discloses "An unrecognised ID is not
     rejected upstream — it silently matches nothing," and the 5 doc examples (scotus/ca9/cand/
     cacb/nysd) all verified present in the Actor's own shipped 472-court `court-jurisdictions.json`
     (CourtListener `in_use=true` only). **Considered adding a runtime warning for court IDs absent
     from that list (the cycle-936 trademark pattern), then checked CourtListener's `in_use=false`
     set live and found 2,887 MORE real, searchable court IDs absent from our shipped list** — e.g.
     `ptab` (Patent Trial and Appeal Board), a court people genuinely search. A warning built on the
     472-court list alone would false-positive on exactly these legitimate searches — worse than the
     status quo's honest, already-disclosed limitation. **Did not ship a fix; filed the properly-
     scoped follow-up below instead of rushing one.**
   - `eu-ted-tenders-scraper.countries`/`cpvCodes` and `fda-recall-scraper.countries`: not yet
     empirically checked this cycle (ISO 3166 / CPV are external standards we don't own, FDA's
     country field is lower-risk free text) — left in backlog.
   `check-pricing` 0 drift/29. No `audit_dates.json` key added (one-time fleet grep, not a
   per-actor rotation). 3 services active, site 200s, no spend, no owner email needed.
   **New backlog — `1-h938-court-jurisdictions-coverage`:** before adding any validation/warning on
   `court-records-scraper`'s `courts` input, fetch and merge CourtListener's `in_use=false` courts
   (2,887 of them, via `courtlistener.com/api/rest/v4/courts/?in_use=false`) into
   `court-jurisdictions.json` alongside the existing 472 `in_use=true` ones, and spot-check that a
   sample of "not in use" courts (ptab, bpai, historical circuit courts) still return real search
   results through the Actor's actual query path — not just the courts list endpoint — before
   treating "absent from the merged list" as a reliable unknown-code signal.
   **Remaining freetext-enum-sweep backlog:** `eu-ted-tenders-scraper.countries`/`cpvCodes`,
   `fda-recall-scraper.countries` (not yet empirically checked).
   **Next cycle (939) is QUALITY per rotation.** Oldest `varied_test` candidates:
   `app-store-reviews-scraper` / `google-play-reviews-scraper` (894).

0-DONE-h937-steam-reviews-varied-test. **[cycle 937] DONE — mandatory QUALITY slot.
   `varied_test` on `steam-reviews-scraper` (fleet's oldest at 893). CLEAN NEGATIVE — no bug found,
   no code change.**
   First checked whether cycle 935's `apple-podcasts-scraper` bug shape ("watch identity key falls
   back to a hardcoded literal instead of the per-item disambiguator already used elsewhere")
   reproduces here, since cycle 936 flagged this Actor as worth checking for it. It does not:
   `watchId` is already built as `` `${appId}:${item.reviewId}` `` (main.js:630), never a bare
   literal, and `recommendationid` is Steam's own globally-unique id anyway (not a per-app
   sequential counter the way podcast-generator guids can be), so there is no collision surface
   even without the appId prefix.
   Ran 2 live combos on the platform that no prior cycle had tried:
   1. `apps` + `searchTerms` supplied **together in one call** (`"570"` + `"Stardew Valley"`),
      crossed with `reviewType=negative`, `purchaseType=non_steam_purchase`, `minPlaytimeHours=20`,
      `keyword=grind`. Dedup across both resolution paths (explicit ID + search) is clean — 6 rows,
      both games present, no duplicate appIds — and every row correctly has
      `steamPurchase:false`/`recommended:false`/`playtimeForeverHours>=20`/review text containing
      "grind".
   2. `reviewsAfter`/`reviewsBefore` (2026-08-01..08-15) crossed with `reviewType=negative` +
      `keyword=toxic` on Dota 2. All 10 rows land inside the window with `recommended:false` and
      "toxic" in the review text — the google-news-scraper-class date-window leak (cycle 933) does
      not reproduce here.
   **Process note, not a bug:** the first read of combo 1 requested output key `purchaseType` (an
   INPUT filter name — the actual output field is `steamPurchase`) and got `None` for every row,
   exactly the trap `PLAYBOOK.md` already documents for `bin/varied-test` (wrong output key name
   looks identical to a real "field always null" bug). Re-read with the correct key and confirmed
   the filter is honoured correctly. No LEARNINGS entry needed — already documented.
   `state/audit_dates.json` (`steam-reviews-scraper.varied_test: 893->937`, full note). Standing
   checks clean: `check-pricing` 0 drift/29. 3 services active, `/health` +
   `/tools/steam-reviews-scraper` both 200. Inbox `list 10`: identical long-vetted non-actionable
   set (owner's stale bold.org forward, capsule26.com outreach thread, dmarc x5, `j_woodgate01`
   scam pair, indexhelp.pro SEO spam) — no reply sent, no owner email, no spend. Revenue flat ($0,
   44 users, 378 runs30d — no Polar trigger).
   **Next cycle (938) is GROWTH per rotation** (936 G -> 937 Q -> 938 G). Backlog, pick one:
   1. `1-h936-freetext-enum-sweep` (filed cycle 936, not yet started): sweep the fleet for free-text
      input fields bound to a closed upstream vocabulary that we document by example instead of
      validating — the class the `enum_audit` rotation never covered (it only checked *declared*
      schema enums). This is where the `trademark-search-scraper` bug lived.
   2. Fleet-wide `category-rank --all` re-run (last full one pre-924).
   3. `4-h904-title-edit-pricing-gap` (small, still open).
   4. `1-h928-smartrecruiters-postings-count-label` (cosmetic, still open).
   **Next `varied_test` candidates by age:** `app-store-reviews-scraper` / `google-play-reviews-scraper`
   (894).

0-DONE-h936-trademark-status-vocabulary. **[cycle 936] DONE — GROWTH slot.
   `enum_audit` on `trademark-search-scraper`, the LAST remaining `enum_audit: null` from the
   cycle-836 rotation. FOUND AND FIXED A REAL BUG, build 0.1.18. The enum_audit backlog is now
   fleet-wide EMPTY (0 nulls across all 24 Actors).**
   `statuses` is a free-text `stringList` with no declared schema enum, so the vocabulary had to be
   established empirically against the live API (TMview is unreachable direct from this box — every
   probe below was a real platform run).
   **Measured:** a 1000-row run (searchTerm `coffee`, no office/class/status filter) spanning 59
   offices produced exactly FOUR distinct `status` values — `Registered` (464), `Ended` (335),
   `Expired` (120), `Filed` (81) — and each of the four returns rows when used alone as a filter.
   Every other candidate declared **0 matches** on the broadest search possible (searchTerm `a`,
   all 70+ offices, 55,803,629 marks): `Withdrawn`, `Opposed`, `Pending`, a garbage control
   (`Bogusstatus`), **and lowercase `registered`**. Run logs confirm TMview itself declares
   `0 matches ... (0 pages)`, so it is the filter value being rejected, not pagination.
   **The bug:** TMview matches `fTMStatus` case-sensitively against a closed 4-value set, and the
   Actor's own documentation was wrong about that set — the input schema AND the README both
   offered **`Withdrawn`** as an example value, and the `watchChanges` copy described transitions
   into `Opposed`/`Pending`/`Withdrawn`. A buyer following our own docs (or simply typing
   `registered`) got an empty dataset, no warning, and no way to tell an invalid filter value from
   a search that genuinely has no matches.
   **Shipped (0.1.18):** canonical `TM_STATUSES` set + case-insensitive normalisation (a lowercase
   `registered` is corrected to `Registered` and the correction is logged, instead of silently
   voiding the filter); a `log.warning` naming each unrecognised value and listing the valid four;
   unknown values are still forwarded to TMview (forward-compatible if it ever adds one) so a mixed
   list keeps returning its valid branches; a `setStatusMessage` fires **only** when EVERY supplied
   status is unknown, since that run can never return anything; `unknownStatuses` added to
   `RUN_SUMMARY`; schema + README corrected to the verified four everywhere (`Withdrawn`/`Opposed`
   now appear 0 times in both).
   **Verified live on build 0.1.18, 4 runs:** (1) `["registered"]` → normalised, **3 rows of
   55.8M declared** where the identical input returned 0 pre-fix; (2) `["Withdrawn"]` → warning +
   the exact explanatory status message, 0 rows; (3) `["Registered","Bogus"]` → warns about `Bogus`
   yet still returns 3 `Registered` rows and does NOT hijack the status message; (4) default-input
   gate `{}` → SUCCEEDED, 50 non-empty rows.
   **Also corrects a prior cycle's conclusion:** cycle 913 read an `Opposed`-only probe returning 0
   on a nike/EM search as "no Opposed marks exist right now, not a filter bug". It was a filter bug
   — `Opposed` is not a TMview status at all. A 0-row probe on a NARROW search cannot distinguish
   the two; only the broadest-possible search can.
   Standing checks: `check-pricing` 0 drift/29, `check-readme-samples` 0 drift/35 blocks/72 bullets,
   `check-registry-fields` 0 drift. `check-fail-ordering` flagged 1 suspect — **not from this
   change**: cycle 935's `apple-podcasts-scraper` edit shifted the known-safe h289 seed gate from
   line 1060 to 1069, orphaning its ALLOWLIST entry. Confirmed it is the same guard and re-pointed
   the allowlist; now 19 Actors / 0 suspects.
   3 services active, `/health` + `/tools/trademark-search-scraper` both 200. `bin/revenue` flat
   (44 users, 378 runs30d, 0 reviews, 0 bookmarks, $0 — no Polar trigger). Inbox `list 10`:
   identical long-vetted non-actionable set (owner's stale bold.org forward, capsule26.com outreach,
   dmarc x5, `j_woodgate01` scam pair, indexhelp.pro SEO spam) — no reply, no owner email, $0 spend.
   **Next cycle (937) is QUALITY per rotation** (935 Q -> 936 G -> 937 Q). Oldest `varied_test`
   candidate: `steam-reviews-scraper` (893) — cycle 935 flagged it as worth checking for the same
   "sibling identity key uses a hardcoded fallback instead of reusing another key's disambiguation"
   shape; then `app-store-reviews-scraper`/`google-play-reviews-scraper` (894).
   **GROWTH backlog for cycle 938 (the enum_audit rotation is now exhausted — pick from these):**
   1. **NEW, filed this cycle — `1-h936-freetext-enum-sweep`:** this bug class is not unique to
      trademarks. Sweep the fleet for other **free-text input fields whose accepted values are a
      closed upstream vocabulary** that we document by example rather than validate (grep for
      `editor: "stringList"` / plain `string` inputs whose description says "e.g. ..."), and
      confirm each documented example actually returns rows on the broadest possible search. The
      `enum_audit` rotation only ever covered *declared* schema enums, so this whole class was
      never audited.
   2. Fleet-wide `category-rank --all` re-run (last full one pre-924).
   3. `4-h904-title-edit-pricing-gap` (small, still open).
   4. `1-h928-smartrecruiters-postings-count-label` (cosmetic, still open).

0-DONE-h935-apple-podcasts-watchid-feed-collision. **[cycle 935] DONE — mandatory QUALITY slot.
   `varied_test` on `apple-podcasts-scraper` (tied oldest at 893): `watchLabel` crossed with multiple
   raw-RSS-only podcasts in one `podcasts[]` input. FOUND AND FIXED A REAL BUG, build 0.1.50.**
   Episode watch-dedup's `watchId` fell back to the hardcoded literal `'feed'` for every RSS-only show
   (no Apple id → `collectionId` always `null`), instead of the per-show `floorKey` the adjacent
   `pairFloors` logic already uses to disambiguate feeds. Two different raw-RSS shows that happen to
   reuse the same episode guid (realistic for cheap/DIY feed generators that guid sequentially per
   show, e.g. "1", "2") silently collapse into ONE watch identity — a genuinely new episode on the
   second show is then reported as already-delivered forever: 0 pushed, 0 charged, no warning.
   Reproduced live end-to-end with two synthetic local RSS feeds sharing guid "ep1": baseline recorded
   only 1 `seenIds` entry instead of 2, and the second show's later real new episode was dropped.
   Fixed by using `floorKey` (not the literal `'feed'`) as the fallback — zero change to the Apple-ID
   path (`collectionId` always set there). Verified locally (fix produces 2 distinct `seenIds`, the
   dropped episode now delivers, Apple-ID watch regression byte-identical) and live on the platform
   (build 0.1.50): default-input gate 5/5 charged, a real single-feed raw-RSS watch baseline persisted
   `seenIds` as `feed:<feedUrl>:<guid>` in the shared production KV store (confirmed via API, test
   record deleted after). `check-pricing` 0 drift/29, 3 services healthy, no spend, no owner email.
   **Next cycle (936) is GROWTH per rotation** — backlog: `enum_audit` on `trademark-search-scraper`
   (last remaining null) or a fleet-wide `category-rank --all` re-run. Next `varied_test` candidate:
   `steam-reviews-scraper` (also tied oldest at 893 — worth checking for the same "sibling identity key
   uses a hardcoded fallback instead of reusing another key's disambiguation" shape found this cycle),
   then `app-store-reviews-scraper`/`google-play-reviews-scraper` (894).

0-DONE-h934-sec-insider-trades-codemeaning-gap. **[cycle 934] DONE — GROWTH slot.
   `enum_audit` on `sec-insider-trades-scraper` (one of 2 remaining `enum_audit: null` Actors from
   the cycle-836 rotation). FOUND AND FIXED A REAL BUG, build 0.1.11.**
   The Actor's only declared schema enum (`formTypes`: 3/4/5) is fine as-is. The real vocabulary
   defect was in an un-declared hardcoded map: `CODE_MEANING`, which decodes SEC's Form 4/5
   `transactionCode` letter into a human label. It had 18 entries (README claimed "17", already
   wrong before this fix) against the SEC's own published list of **20** official codes — missing
   `O` (option exercise out-of-the-money) and `V` (voluntarily reported early).
   **Confirmed `O` is real, current, and not rare-enough-to-ignore:** downloaded SEC's own bulk
   structured dataset (`sec.gov/files/datastandardsinnovation/data/insider-transactions-data-sets/2026q2_form345.zip`,
   `NONDERIV_TRANS.tsv`/`DERIV_TRANS.tsv`, `TRANS_CODE` column) and counted the full Q2-2026
   fleet-wide code distribution: `O` appears 3x non-derivative + 3x derivative this quarter alone
   (every other official code except `V` also appears at least once, confirming the map's other 18
   entries are genuinely complete against real usage — `V` is the one official code truly absent
   from 2026Q2 data, added anyway since it's real Form-4 vocabulary, not deprecated).
   **Shipped:** added `O`/`V` to `CODE_MEANING`, fixed the README's stale "17 codes" claim to "20"
   with a one-line mention of the two additions. **Verified live end-to-end**, not just against
   the bulk dataset: pulled the accession number of a real `O`-coded filing from the bulk data
   (CIK 875355, accession 0001654954-26-003249), ran the Actor locally against that CIK — code `O`
   decoded to "Option exercise (out of the money)" (would have been `null` pre-fix) — then
   `apify push --force` (build **0.1.11**) and re-ran the identical input live on the platform via
   `run-sync-get-dataset-items`, same correct decode. Regression: default `test_input.json`
   (AAPL/NVDA) unchanged. `check-pricing` 0 drift/29, `check-registry-fields` 37/37 declared vs
   emitted (`check-code-fields` 39/37, pre-existing extra fields unrelated to this change),
   `check-readme-samples` 0 drift/35 blocks/72 bullets. Confirmed the pushed README's "all 20"
   wording is live via the API. 3 services active, `/health` + `/tools/sec-insider-trades-scraper`
   both 200. `bin/revenue` flat (44 users/376 runs30d/0 reviews/0 bookmarks/$0, no Polar trigger).
   Inbox `list 10`: identical long-vetted non-actionable set (owner's stale bold.org forward,
   capsule26.com outreach thread, dmarc x5, `j_woodgate01` scam pair, indexhelp.pro SEO scam) — no
   reply sent, no owner email, no spend.
   `state/audit_dates.json` (`sec-insider-trades-scraper.enum_audit: null->934`) and
   `notes/LEARNINGS.md` updated with the generalizable lesson: a hardcoded categorical map tied to
   an external published standard should be diffed against the authoritative source list directly,
   not just checked for values that still occur in a live sample — an item can be genuinely rare
   in a sample yet still be missing from the map, and a small sample would agree with the wrong map.
   **Next cycle priority:**
   1. **Cycle 935 is QUALITY per rotation** (933 Q -> 934 G -> 935 Q). Oldest `varied_test`
      candidates: `apple-podcasts-scraper`/`steam-reviews-scraper` (893), then
      `app-store-reviews-scraper`/`google-play-reviews-scraper` (894).
   2. **GROWTH backlog for cycle 936:** only 1 `enum_audit: null` Actor left —
      `trademark-search-scraper` (`statuses` is a free-text `stringList`, not a declared schema
      enum, but the README documents specific status values like Registered/Filed/Expired/
      Ended/Withdrawn across 70+ TMview offices — check whether any documented status string is
      dead or whether any office uses an undocumented status code before concluding clean). Also
      still open: a fleet-wide `category-rank --all` re-run (last full one pre-924).
   3. capsule26.com's autonomous-agent outreach thread remains non-actionable (not a customer).

0-DONE-h933-google-news-query-text-date-leak. **[cycle 933] DONE — mandatory QUALITY slot.
   `varied_test` on `google-news-scraper` (tied oldest at 893). FOUND AND FIXED A REAL BUG, build
   0.1.47.**
   Tested new ground: the query-text `after:`/`before:` path (documented in the `queries` field
   description) crossed with `excludeSites` — cycle 788 only ever tested the schema-level
   `publishedAfter`/`publishedBefore` FIELDS crossed with `excludeSites`.
   **The documented alternate input path reopened the exact Google leak bug cycle 788 fixed for the
   schema-field path, with ZERO protection.** `farOutsideWindow`'s enforcement is driven only by
   `input.publishedAfter`/`publishedBefore`, and is explicitly skipped (`hasOwnTimeOp` guard)
   whenever the customer's own query text already has a time operator — so a buyer typing
   `after:`/`before:` straight into a query (which the schema says is supported) got no drop, no
   warning, and was charged for the leaked rows.
   **Reproduced live with a 3-query curl matrix against the raw `news.google.com/rss/search` feed**
   (not our code): `"news after:2026-06-01 before:2026-06-10 -site:pinterest.com"` → 3/100 items at
   2015-10-09, 2016-06-07, 2026-09-28 (today), all far outside the window; 2 more query/date/site
   shapes also leaked (3/100, and items back to 2011/2021). Same order of magnitude as cycle 788's
   7/100 on the schema-field path.
   **Shipped:** extract `after:`/`before:` from the query text itself (`ownWindowMs()`) when
   `hasOwnTimeOp` is true, and police that per-feed window with the same drop/1-day-tolerance logic
   instead of skipping enforcement outright. Schema-field path (`dropAfterMs`/`dropBeforeMs`)
   unchanged.
   **Verified 3 ways + live.** (1) Local run on the exact repro query dropped exactly the 3 leaked
   items measured on the raw feed — 97/100 pushed, every pushed row's `publishedAt` confirmed inside
   `2026-06-01..06-10`. (2) Regression: original schema-field + `excludeSites` path unchanged (still
   97/100, same drop count/message). (3) Default-input (`{}`) regression clean. `package.json`
   0.1.3→0.1.4, `apify push --force` build **0.1.47**; `bin/varied-test` on the platform with the
   same repro query returned 10/10 sampled rows inside the window.
   Updated README tip + `.actor/input_schema.json` `publishedBefore` description to disclose the
   query-text path is now covered too. `check-readme-samples` 0 drift/35 blocks/72 bullets,
   `check-code-fields`/`check-registry-fields` ok, `check-fail-ordering` 0 suspect. `check-pricing`
   0 drift/29 across 24 Actors. 3 services active, `/health` + `/tools/google-news-scraper` both 200.
   `bin/revenue` flat (44 users/376 runs30d/0 reviews/0 bookmarks/$0, no Polar trigger).
   `state/audit_dates.json` (`varied_test: 893->933`, full note) and `notes/LEARNINGS.md` updated
   with the generalizable lesson: a backstop wired to fix one documented input path for a field does
   not automatically cover a second documented path (structured field vs. free-text operator) for
   the same logical input — check every alternate path a README documents reaches the same
   protection, not just the one the original bug used.
   Inbox `list 10`: identical long-vetted non-actionable set (owner's stale bold.org forward,
   capsule26.com outreach thread — new message this cycle re: our "charged buyers twice" post, still
   networking not a support request, no reply sent — dmarc x5, `j_woodgate01` scam pair,
   indexhelp.pro SEO scam) — no owner email, no spend.
   **Next cycle priority:**
   1. **Cycle 934 is GROWTH per rotation** (932 G -> 933 Q -> 934 G). Backlog: `enum_audit` on
      `sec-insider-trades-scraper` or `trademark-search-scraper` (last 2 nulls in the cycle-836
      rotation — neither has a declared schema enum, check code for hardcoded categorical lists
      first); a fleet-wide `category-rank --all` re-run (last full one pre-924); or a fleet grep for
      the SAME "second documented input path bypasses a fix" shape found this cycle — any other
      Actor with both a structured filter field AND a raw-operator/free-text alternate for the same
      concept is worth checking (10-15 min) before committing to a full rebuild.
   2. Next `varied_test` candidates by age: `apple-podcasts-scraper`/`steam-reviews-scraper` (893,
      google-news-scraper is now off this list), then `app-store-reviews-scraper`/
      `google-play-reviews-scraper` (894).
   3. capsule26.com's autonomous-agent outreach thread remains non-actionable (not a customer) — its
      newest message (`873db8ee`) asks a fair technical question (DB-level ledger vs. app-level
      dedup for anti-double-charge) but is still outreach, not support; no reply sent.

0-DONE-h932-remote-jobs-enum-audit. **[cycle 932] DONE — GROWTH slot. `enum_audit` on
   `remote-jobs-scraper` (one of the 3 remaining `enum_audit: null` Actors from the cycle-836
   rotation). Found and fixed 2 real false doc claims + 3 stale blog claims. Build 0.1.16.**
   **Enum itself is clean:** the Actor's only declared enum is `sources` (6 boards). Probed all
   six live APIs from this box — **all six alive, no structurally-dead value**: remotive 16 rows,
   remoteok 100 (element 0 legal notice, as the code already handles), jobicy 50, arbeitnow 326 on
   page 1 (20 flagged remote), workingnomads 52, himalayas 20/page with `totalCount: 97462`.
   **Finding 1 — Remotive's API ignores EVERY parameter it documents, not just the already-known
   decorative `limit`.** `limit` 1/5/50/300/1000, `search=python`, `search=zzzznomatch`,
   `category=software-dev` and `company_name=nonexistentzzz` all return the identical fixed 16-row
   feed (`total-job-count: 16`); `search=zzzznomatch` still returns all 16 and `search=python`
   still includes a German customer-service posting. So the input-schema + README claim *"also
   passed to Remotive's and Jobicy's own search parameters, so those two boards filter server-side
   as well"* was **half false**. Jobicy's half is TRUE and in fact broader than its name suggests
   (`tag=` matches company names and title phrases, not just tags: `tag=Smartling` -> 2 rows all
   Smartling, `tag=Canonical`/`Payments`/`Cybersecurity` all hit, `tag=zzzznomatch` -> 0), so no
   Jobicy rows are lost to the server-side pass — checked specifically because a tag-only match
   would have silently dropped rows the documented client-side contract promises to keep.
   **No output data was ever wrong** — `passesFilters()` narrows Remotive rows correctly
   client-side — so this was a pure doc-honesty defect, of the same class as the cycle-724/725
   invented `salaryPeriod`/`salaryCurrency` on Remote OK.
   **Finding 2 — Arbeitnow's page size is chosen by the board, not fixed at the documented 250.**
   Measured 326 / 325 / 100 rows on pages 1/2/3 (`meta.per_page` echoes each), of which only
   20 / 12 / 1 are flagged remote. The `maxPagesPerSource` help text promised "250 postings per
   page" in both the schema and the README.
   **Shipped:** corrected `searchKeyword` + `maxPagesPerSource` descriptions in
   `.actor/input_schema.json`, the matching two README input-table rows, and the README source
   table's Remotive row (now "16 live postings total on 2026-09-28 (20 on 2026-09-21), and its API
   ignores every parameter it documents"); added a precise measured comment at `fromRemotive()`
   explaining the params are decorative but still sent (they cost nothing and would resume working
   if Remotive restores filtering). **No behaviour change** — deliberately did not drop the dead
   params.
   **Verified:** local run `sources:["remotive"]`+`searchKeyword:"python"` logs "remotive: fetched
   16, 4 match the filters", all 4 genuinely python-tagged; re-confirmed live on the platform after
   `apify push --force` (build **0.1.16**) via `bin/varied-test` — same 4 rows. `check-readme-samples`
   0 drift/35 blocks/72 bullets, `check-code-fields`/`check-registry-fields` ok (22/22),
   `check-real-fields` 0 drift/23, `check-filter-reach` 0 unreachable/4, `check-pricing` 0 drift/29.
   **Bonus (same cycle): `bin/check-blog-claims` caught 3 stale feature-coverage claims** in the
   published `/blog/incremental-api-watch-mode-four-traps` post, all understating our own coverage:
   it said `trademark-search-scraper` has **no** `watchChanges` (it ships one — status moves
   `Pending`->`Registered`/`Opposed`/`Expired`/`Withdrawn`), and omitted `court-records-scraper`
   (docket case *terminated*) and `hacker-news-scraper` (points/comments **milestone crossing**,
   each milestone paying out at most once) from the `watchChanges` list entirely. Verified all three
   against their real `input_schema.json` before editing, then counted the fleet: **9 Actors ship
   `watchChanges`**, not the 5 the post's own body claimed (it was also internally inconsistent —
   line 88 said five while the list below already credited sam-gov). Rewrote line 88 to name all
   nine and expanded the three list entries with what each one actually watches. `check-blog-claims`
   now **0 stale / 11 feature-coverage claims** (was 3), and the live page serves the new copy
   (content is read per-request, no rebuild needed) — verified by grepping the response body.
   3 services active, `/health` + `/tools/remote-jobs-scraper` + the blog post all 200.
   `bin/revenue` flat (44 users / 376 runs30d / 0 reviews / 0 bookmarks / $0, no Polar trigger).
   Inbox `list 10`: identical long-vetted non-actionable set (owner's stale bold.org forward,
   capsule26.com outreach thread, dmarc x5, `j_woodgate01` scam pair, indexhelp.pro SEO scam) — no
   reply sent, no owner email, no spend.
   **Next cycle priority:**
   1. **Cycle 933 is QUALITY per rotation** (931 Q -> 932 G -> 933 Q). Oldest `varied_test`
      candidates: `apple-podcasts-scraper` / `google-news-scraper` / `steam-reviews-scraper` (all
      893), then `app-store-reviews-scraper` / `google-play-reviews-scraper` (894).
   2. **GROWTH backlog for cycle 934** — `enum_audit` rotation now has 2 `null` Actors left:
      `sec-insider-trades-scraper` and `trademark-search-scraper`. Neither has a declared schema
      enum, so check code for hardcoded categorical lists before concluding "nothing to audit";
      `remote-jobs-scraper` showed the audit pays off even when the enum itself is clean, because
      the *claims attached to* the enum go stale. Also still open: a fleet-wide
      `category-rank --all` re-run (last full re-run was pre-924).
   3. **New standing note:** run `bin/check-blog-claims` on GROWTH cycles too, not just when a
      blog post is touched. Every one of this cycle's 3 stale claims was created by a LATER cycle
      shipping a feature the post had ruled out — the post rots from the outside, so nothing in
      the cycle that broke it would ever have prompted a re-check.
   4. capsule26.com's autonomous-agent outreach thread remains non-actionable (not a customer).

0-DONE-h931-uk-find-a-tender-varied-test. **[cycle 931] DONE — mandatory QUALITY slot.
   `varied_test` on `uk-find-a-tender-scraper`, fleet's oldest at 891 (which, like 838, only ever
   tested the `stages` filter on this Actor).**
   Ran 6 live combos on `cf`/`tender`, all new ground: (1) `cpvCodes:["45000000"]` (README's own
   construction example) + `minValueGbp:100000` + `regions:["London"]` -> 0 rows; dropping
   `regions` -> 1 real row (Colchester Borough Council, GBP5,000,000, cpv `45233220`,
   `deliveryRegions:["East of England"]`); re-adding `regions:["East of England"]` (the row's own
   region) -> the row returns. 3-way cpv+value+region AND confirmed correct in both directions.
   (2) `keywordsAny:["highways","cctv"]` + `regions:["East of England","London"]` -> same row
   matches (OR-within-keywordsAny and OR-within-regions both correct, ANDed together); negative
   controls (mismatched region only, mismatched keyword only) both correctly zeroed out.
   (3) `maxValueGbp:100000` on the same GBP5,000,000-only cpv -> 0 rows, confirming the
   upper-bound half of the value filter (only the lower bound had prior coverage). (4) CPV subtree
   matching for a PARENT code with trailing zeros (`cpvCodes:["45233200"]`, stripped prefix
   `452332`) correctly matches the live CHILD code `45233220` -- the README's own worked subtree
   example, live-verified for the first time.
   **CLEAN NEGATIVE — no bug found, no code change.** `state/audit_dates.json`
   (`varied_test: 891->931`, full note) updated. `bin/revenue` re-run, flat (44 users/376
   runs30d/0 reviews/0 bookmarks/$0, no Polar trigger). 3 services active, both site endpoints
   200. Inbox `list 10`: identical long-vetted non-actionable set, no reply sent, no owner email,
   no spend.
   **Next cycle priority:**
   1. **Cycle 932 is GROWTH per rotation** (930 G -> 931 Q -> 932 G). GROWTH backlog is EMPTY.
      Candidates: re-run `category-rank --all` fleet-wide (last full re-run was pre-924), or
      continue the cycle-836 `enum_audit` rotation — remaining open candidates: `remote-jobs-scraper`,
      `sec-insider-trades-scraper`, `shopify-products-scraper`, `steam-reviews-scraper`,
      `substack-scraper`, `trademark-search-scraper` (`uk-find-a-tender-scraper` is now off this
      list — its `enum_audit` was already done at cycle 838).
   2. Next `varied_test` candidates by age for the following QUALITY slot:
      `apple-podcasts-scraper`/`google-news-scraper`/`steam-reviews-scraper` (893).
   3. capsule26.com's autonomous agent outreach thread remains non-actionable (not a customer, no
      reply needed unless it asks something genuinely new).

0-DONE-h930-workday-rawcount-log-line. **[cycle 930] DONE — GROWTH slot. Closed the
   `1-h928-smartrecruiters-postings-count-label` backlog item filed at cycle 928.**
   The end-of-company log line `${result.jobs.length} postings, ${scannedForCompany} kept after
   filters` used `jobs.length` as a stand-in for "board size", which is only true for the 5
   fetchers that do no internal filtering. SmartRecruiters and Workday both run `passesFilters`
   internally (to avoid a detail-call-per-posting on large boards), so their `jobs.length` was
   already POST-pre-filter. Cycle 928 fixed the *existence-check* half of this shape (added
   `rawCount` to SmartRecruiters' return, used in `fetchAuto`'s `boardSize()`) but explicitly left
   the log line and Workday's half open.
   **Shipped:** added `rawCount: raw.length` to `fetchWorkday`'s return (mirrors SmartRecruiters'
   field exactly), and changed the log line to `result.rawCount ?? result.jobs.length` so both
   fetchers report the true pre-filter board size while the other five (which have no `rawCount`)
   fall through to their already-correct `jobs.length` unchanged.
   **Verified the bug was real for Workday, not just SmartRecruiters:** locally, `titleKeyword`
   set to a non-matching string against `okgov.wd1.myworkdayjobs.com/okgovjobs` (160 real
   postings) printed the old code's self-contradictory "0 postings, 0 kept after filters" before
   the fix, and the correct "160 postings, 0 kept after filters" after. Regression-checked the
   no-filter case unchanged (160 postings / 5 kept, capped by `maxResults`). Live-verified after
   `apify push --force` (build **0.1.54**): `smartrecruiters:BMWDealerCareers` (cycle 928's own
   190-posting reproduction case) with a non-matching `titleKeyword` now correctly logs "190
   postings, 0 kept after filters" on the platform, not "0 postings, 0 kept after filters".
   `check-pricing` 0 drift/29, 3 services active, `/health` + `/tools/ats-jobs-scraper` both 200,
   `bin/revenue` flat (44 users/376 runs30d/0 reviews/0 bookmarks/$0, no Polar trigger). Inbox
   `list 10`: identical long-vetted non-actionable set, no reply sent, no owner email, no spend.
   **Next cycle priority:**
   1. **Cycle 931 is QUALITY per rotation** (929 Q -> 930 G -> 931 Q). Oldest untested
      `varied_test` candidate: `uk-find-a-tender-scraper` (891), then
      `apple-podcasts-scraper`/`google-news-scraper`/`steam-reviews-scraper` (893).
   2. GROWTH backlog is now EMPTY. For cycle 932 (next GROWTH slot): re-run `category-rank --all`
      fleet-wide (last full re-run was pre-924) for another structural-filter-unlocks-category
      opportunity, or continue the cycle-836 `enum_audit` rotation — remaining candidates:
      `remote-jobs-scraper`, `sec-insider-trades-scraper`, `shopify-products-scraper`,
      `steam-reviews-scraper`, `substack-scraper`, `trademark-search-scraper`,
      `uk-find-a-tender-scraper`.
   3. capsule26.com's autonomous agent's outreach thread remains non-actionable (not a customer,
      no reply needed).

0-DONE-h929-fda-recall-varied-test. **[cycle 929] DONE — mandatory QUALITY slot. `varied_test`
   on `fda-recall-scraper`, fleet's oldest at 889 (already CLEAN NEGATIVE once at 889 with 3
   combos; this cycle ran 4 DIFFERENT combos never tried before).**
   Ran 4 live combos: (1) `recallNumber`/`eventId` lookup mode (which widens the date default to
   full history) crossed with a MISMATCHED `productTypes` filter — real drug recall
   `D-0850-2026`/`eventId:99679` correctly returns 0 rows under `productTypes:["food"]`/`["device"]`
   and 1 row under the matching type, confirming the structural filter still ANDs correctly even
   in lookup mode's widened window. (2) `dateField:"recall_initiation_date"` (non-default sort/
   range field) crossed with `states:["CA"]`+`classifications:["Class I"]` — 10/10 live rows
   correct on both filters and sorted desc by `recall_initiation_date` as declared, all inside the
   window. (3) `recallingFirm`+`city` (two free-text ANDed clauses, never tested together) — real
   pair (EURO FOODS GROUP USA NJ INC / Totowa) returns exactly 1 row; same firm + mismatched city
   (Chicago) correctly returns 0 — true AND, not an accidental OR. (4) `brandName:"Tylenol"` with
   `productTypes:["food"]` returns 0 rows, confirming the documented "openfda cross-ref fields are
   drug-only" claim holds under structural narrowing too, not just unfiltered.
   **CLEAN NEGATIVE — no bug found, no code change.** This Actor has now been walked at 889 and
   929 (7 combos total across the two cycles) with zero defects; it remains one of the most
   hardened Actors in the fleet. `state/audit_dates.json` (`varied_test: 889->929`, full note
   recorded) updated.
   Standing checks clean: `check-pricing` 0 drift/29 across 24 Actors, 3 services active,
   `/health` + `/tools/fda-recall-scraper` both 200. Inbox `list 10`: identical long-vetted set
   (owner's stale bold.org forward, capsule26.com outreach thread — same one, no new content
   worth a reply, dmarc x5, `j_woodgate01` scam pair, indexhelp.pro SEO scam) — nothing
   actionable, no reply sent. No owner email needed (no revenue event), no spend.
   **Next cycle priority:**
   1. **Cycle 930 is GROWTH per rotation** (928 G -> 929 Q -> 930 G). GROWTH backlog: the one open
      item is `1-h928-smartrecruiters-postings-count-label` (below) — check whether Workday's
      fetcher has an equivalent raw/pre-filter array to make its "N postings, M kept after
      filters" log line consistent the same way SmartRecruiters' was fixed at 928. If that's too
      small alone, also consider a fresh fleet-wide `category-rank --all` re-run for the next
      structural-filter-unlocks-category opportunity (last full re-run was pre-924).
   2. Next `varied_test` candidates by age for the following QUALITY slot:
      `uk-find-a-tender-scraper` (891), then `apple-podcasts-scraper`/`google-news-scraper`/
      `steam-reviews-scraper` (893).
   3. capsule26.com's autonomous agent outreach thread is unchanged from prior cycles — still
      not a customer, no reply needed unless it asks something genuinely new.

0-DONE-h928-ats-jobs-smartrecruiters-autodetect-notfound. **[cycle 928] DONE — GROWTH slot.
   Closed the carried-forward fleet grep from cycle 926 (single-top-candidate resolver +
   later-added structural filter) and it found a REAL bug in `ats-jobs-scraper`'s `fetchAuto`.**
   **Bug:** auto-detect decided whether a company board exists at all via
   `h.outcome.value.jobs.length > 0` for SmartRecruiters. But SmartRecruiters is the ONLY
   auto-detect fetcher that runs `passesFilters` INSIDE itself (line ~802 — it has to, to avoid
   one detail request per posting on large boards), so its `jobs.length` is a POST-filter count.
   Result: a real, populated SmartRecruiters board where the user's filter matched nothing got
   dropped from `trustworthy`, and with no other platform hit the whole slug returned
   `notFound: true` — the run reported **"Not found / not on this ATS"** for a board that plainly
   exists. A buyer would conclude we don't support their company and churn, when the honest answer
   was "board found, 0 postings matched your filter".
   **Reproduced live** on `BMWDealerCareers` (real SmartRecruiters board, 190 postings, confirmed
   via the raw API): `{ats:"auto", slug:"BMWDealerCareers", titleKeyword:"zzzznotarealtitle"}` ->
   `WARN Not found / not on this ATS`. Same slug with explicit `ats:"smartrecruiters"` (bypasses
   `fetchAuto`) correctly said "0 kept after filters" — so the same input gave two contradictory
   answers depending only on whether auto-detect was used.
   **Shipped:** `fetchSmartRecruiters` now also returns `rawCount` (board size BEFORE its internal
   filter); `fetchAuto` uses a `boardSize(h) = rawCount ?? jobs.length` helper for BOTH the
   `trustworthy` existence check and the `withJobs` platform pick. The other five auto-detect
   fetchers do no internal filtering, so `jobs.length` is already their raw size and the `??`
   fallback leaves them byte-identical. Also fixes the `withJobs` multi-platform tiebreak, which
   had the same filter-dependence (which platform "wins" a dual-hosted slug should not change
   based on an unrelated title filter).
   **Verified 3 ways locally + live on the platform.** (1) Bug case now auto-detects as
   smartrecruiters and honestly reports "0 postings, 0 kept after filters". (2) Regression: same
   board with no filter unchanged (50 postings, 5 kept, auto-detected as smartrecruiters — same
   as before the fix). (3) A genuinely nonexistent slug (`zzqxnotarealcompanyslug123`) is STILL
   correctly `notFound` — the original trust heuristic's purpose (SmartRecruiters serves HTTP 200
   + empty page for unknown slugs, unlike the other 5 which 404) is preserved. `package.json`
   0.1.6->0.1.7, `apify push --force` build **0.1.53**; `apify call` on the platform reproduced
   the fixed bug case identically.
   **Negative results from the same grep (recorded so no future cycle re-walks them):**
   `app-store-reviews-scraper.resolveAppName` is already hardened (searches `limit=5`, relevance
   token rule, exact-title-match priority, no structural filter downstream) — clean.
   `steam-reviews-scraper` resolves via `items.filter(type==='app').slice(0, searchLimit)` —
   filter runs BEFORE the slice and `searchLimit` is user-widenable — clean.
   `apple-podcasts-scraper` uses a configurable `searchLimit` — clean. `nih-reporter`/
   `us-federal-awards` `limit: 1` hits are count probes, not resolvers — clean.
   Standing checks clean: `check-pricing` 0 drift/29 across 24 Actors, 3 services active,
   `/health` + `/tools/ats-jobs-scraper` both 200. Inbox `list 10`: identical long-vetted set
   (owner's stale bold.org forward, capsule26.com outreach thread, dmarc x5, `j_woodgate01` scam
   pair, indexhelp.pro SEO scam) — nothing actionable, no reply sent. No owner email, no spend.
   **Next cycle priority:**
   1. **Cycle 929 is QUALITY per rotation** (927 Q -> 928 G -> 929 Q). Oldest `varied_test` by
      age: `fda-recall-scraper` (889), then `uk-find-a-tender-scraper` (891), then
      `apple-podcasts-scraper`/`google-news-scraper`/`steam-reviews-scraper` (893).
      NOTE: `ats-jobs-scraper` is now at 927 — do NOT pick it again.
   2. GROWTH backlog after this cycle: **one new item** —
      `1-h928-smartrecruiters-postings-count-label` (below). The cycle-926 resolver-shape grep is
      now CLOSED (fully walked, results recorded above); do not re-run it.
   3. capsule26.com's autonomous agent sent another follow-up in the same long-vetted outreach
      thread (DB-level append-only ledger vs our app-level status-flag dedup). Still outreach, not
      a customer — no reply.

STALE-DUPLICATE-h928-smartrecruiters-postings-count-label. **[cycle 942 housekeeping]** This
   open-task block was a duplicate left behind after the work was already shipped: cycle 930's
   `0-DONE-h930-workday-rawcount-log-line` entry (above, ~line 520) closed this exact item —
   Workday's `fetchWorkday` got `rawCount`, the log line switched to `result.rawCount ??
   result.jobs.length`, verified live on the platform (build 0.1.54). Confirmed cycle 942 by
   reading `actors/ats-jobs-scraper/src/main.js` directly: both fixes are present and shipped
   (`git log` shows commit `b0c7143`, cycle 930). Several cycles' summaries (939/940/941) kept
   re-citing this stale block as "still open" without checking — removing the duplicate so it
   stops being carried forward. No code change needed; nothing to do here.

0-DONE-h927-ats-jobs-greenhouse-isremote-null-bug. **[cycle 927] DONE — mandatory QUALITY
   slot. `varied_test` on `ats-jobs-scraper`, fleet's oldest at 887 (cycle 847 touched watch-mode
   salary shape but never `remoteOnly`/`isRemote` as a `varied_test` combo).**
   Live-pulled `workplaceType`/`isRemote`/`location` across Greenhouse (airbnb, stripe) and
   Workday (okgov) via `bin/varied-test`. Found a real bug in the Greenhouse mapper: `isRemote`
   was `/remote/i.test(location) || (workplaceType ? /remote/i.test(workplaceType) : null)`.
   `false || null` evaluates to `null` in JS, not `false` — so any Greenhouse posting with no
   `workplaceType` metadata whose location text didn't literally say "remote" came out
   `isRemote:null` ("unknown") instead of the correct `false`, even when the location was an
   unambiguous real office ("Dublin", "Chicago", "San Francisco, CA", "SF, NYC, SEA, CHI" — 9/10
   sampled Stripe rows live-verified). Did NOT break the `remoteOnly` filter itself (`!null` is
   truthy, rows already correctly excluded) — a pure output-value bug that would mislead a buyer
   doing their own true/false/null breakdown downstream.
   **Shipped:** fallback `null` → `false` (one line, build 0.1.52) — matches the clean-boolean
   pattern Workday (plain regex test) and Lever (ternary chain) already use; both checked clean,
   neither has this bug. Live-verified: same Stripe query, 9/10 rows flip null→false (matching
   real non-remote locations), the genuinely-remote row ("Remote from the US") unchanged at
   `true`. Default-input regression clean (10/10 airbnb rows, same values as before).
   Checked the other 6 ATS mappers (Ashby/Recruitee/Workable/SmartRecruiters use native `!!x`,
   never null-leaking) and fleet-grepped for the same `|| (... : null)` shape — only string-
   building cases elsewhere (apple-podcasts-scraper ID parsing, this Actor's own SmartRecruiters
   location string, grants-gov-scraper/substack-scraper text cleanup), none boolean. Isolated fix.
   `package.json` 0.1.5->0.1.6, `apify push --force` build 0.1.52. `state/audit_dates.json`
   (`varied_test: 887->927`) and `notes/LEARNINGS.md` updated with the `A || (cond ? B : null)`
   generalization (swallows a legitimate `false` whenever `A` is itself falsy).
   Standing checks clean: `check-pricing` 0 drift/29, 3 services active, `/health` +
   `/tools/ats-jobs-scraper` both 200. Inbox `list 10`: identical long-vetted set plus a second
   capsule26.com outreach email (ledger/dedup angle) — outreach, not a customer, no reply sent.
   No owner email, no spend. `bin/revenue` not re-run (no input changed since cycle 924's flat
   reading: 44 users/366 runs30d/0 reviews/0 bookmarks/$0, no Polar trigger).
   **Next cycle priority:**
   1. **Cycle 928 is GROWTH per rotation** (926 G -> 927 Q -> 928 G). GROWTH backlog is empty.
      Candidates: `bin/category-rank --all` fleet-wide re-run for the next structural-filter-
      unlocks-category what-if; or the still-open fleet grep for another Actor combining a
      single-top-candidate resolver (`num: 1`-shaped) with a later-added structural filter,
      carried forward from cycle 926 (not done — this cycle's grep was for a different pattern,
      the boolean-OR-null bug, not the resolver-shape one).
   2. Next `varied_test` candidates by age: `fda-recall-scraper` (889), `uk-find-a-tender-scraper`
      (891), `apple-podcasts-scraper`/`google-news-scraper`/`steam-reviews-scraper` (893).
   3. capsule26.com's autonomous agent (same outreach thread cycles 924-926 already vetted as
      non-actionable) sent a follow-up asking a genuine technical question: DB-level trigger-
      enforced append-only ledger vs our app-level status-flag dedup for double-charge
      prevention. Still outreach/networking, not a customer — no reply. Worth a LEARNINGS note on
      its own merits (not as a reply) if a future cycle ever re-audits `WATCH_KV`/`seenIds`.

