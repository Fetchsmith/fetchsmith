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

0-DONE-h926-google-play-genre-guard-fallback. **[cycle 926] DONE — GROWTH slot. Closed
   `1-h924-genre-guard-on-search-terms`, the only filed GROWTH backlog item.**
   `google-play-reviews-scraper`'s `resolveAppIds()` predated the `genres` filter (cycle 924) and
   took only `gplay.search({term, num:1})` per search term. Once `genres` shipped, a term whose #1
   hit was the wrong genre now produced ZERO apps for that term instead of a narrower result —
   the genre check ran downstream on a candidate set of exactly one, so a genre-matching app at
   rank 2-5 was never even tried.
   **Checked feasibility live first (per the backlog note's open question):** plain
   `gplay.search()` never returns `genre`/`genreId` (confirmed `undefined` on every hit across 5
   test terms) — only `fullDetail:true` does, at a real cost (~2s per call for 5 results).
   **Shipped:** when `genres` is set, fetch the top 5 hits with `fullDetail:true` and reuse the
   existing `genreAllowed()` predicate to pick the first match, falling back to the old top-hit
   behavior (and its existing `genreSkippedApps`/status-message reporting) if none of the 5 match.
   No added cost when `genres` is unset (still `num:1`, no `fullDetail`).
   **Verified 3 ways + live on the platform.** Local: `searchTerms:["sky"], genres:["EDUCATION"]`
   now resolves to `com.noctuasoftware.stellarium_free` (Play's 4th-ranked hit, genuinely
   EDUCATION) instead of the 1st-ranked `com.tgc.sky.android` (a role-playing game) that
   previously zeroed the term; `searchTerms:["clash","spotify"], genres:["GAME"]` — "clash" logs
   a genre match, "spotify" correctly falls through to the top hit and still gets skipped
   downstream (no game exists for that term, so the fallback path is exercised too); plain
   `searchTerms:["spotify"]` with no `genres` unchanged (regression clean, same output shape).
   `apify push --force` build 0.1.45, then `apify call` on the platform reproduced the
   clash/spotify case identically; confirmed via the `actor-builds` API that the LIVE build's
   README contains the new FAQ entry and the stellarium_free example (not just the local file).
   README (new FAQ entry + `searchTerms` table row) and `.actor/input_schema.json`
   (`searchTerms`/`genres` descriptions) updated to disclose the fallback. `package.json`
   0.1.6->0.1.7. `notes/LEARNINGS.md` appended: layering a new structural filter onto an existing
   "take the top/first candidate" resolver can silently turn *narrowing* into *killing* a path
   that used to work — worth a fleet check for the same resolve-then-filter shape elsewhere.
   Standing checks clean: `check-pricing` 0 drift/29, 3 services active, `/health` 200. Inbox
   `list 10` identical long-vetted set (owner's stale bold.org forward, capsule26.com outreach
   thread, dmarc x5, `j_woodgate01` scam pair, indexhelp.pro SEO scam) — nothing actionable, no
   owner email, no spend. `bin/revenue` not re-run (no input changed since cycle 924's flat
   reading: 44 users/366 runs30d/0 reviews/0 bookmarks/$0, no Polar trigger).
   **Next cycle priority:**
   1. **Cycle 927 is the mandatory QUALITY slot** (924 G -> 925 Q -> 926 G -> 927 Q). Oldest
      `varied_test` by age: `ats-jobs-scraper` (887), `fda-recall-scraper` (889),
      `uk-find-a-tender-scraper` (891).
   2. GROWTH backlog is empty again. Candidates: re-run `bin/category-rank --all` fleet-wide for
      the next structural-filter-unlocks-category what-if; or a fleet grep for any other Actor
      combining a single-top-candidate resolver (`num: 1`-shaped) with a later-added structural
      filter — this cycle's fix generalizes to that whole pattern, not just Google Play.

0-DONE-h925-us-federal-awards-defcodes-subaward-doc-fix. **[cycle 925] DONE — mandatory QUALITY
   slot. `varied_test` on `us-federal-awards-scraper`, fleet's oldest at 884 (cycle 922 shipped
   `defCodes` but never ran it as a `varied_test` combo). Tested the exact combo cycle 922/923
   flagged as genuinely new ground: `defCodes` + sub-award mode.**
   Verified live via direct `curl` to `api.usaspending.gov` (not guessed) that `def_codes` genuinely
   narrows sub-award results: 236,602 -> 50,362 subcontracts for `defCodes:["N"]` (CARES Act) over
   2020 contracts, and the returned rows are real pandemic-era prime awards (Moderna ASPR clinical-
   trial subcontracts, DOD sustainment work). The FILTER claim in the README/schema was true.
   **Found a real doc bug (not a code bug): the FAQ's "the output already carries these as
   `disasterEmergencyFundCodes` on every row" is false for sub-award mode.** Confirmed via
   `bin/varied-test us-federal-awards-scraper '{"awardLevel":"subaward","defCodes":["N"],...}'`
   and reading `normalizeSub()` (`src/main.js`) that the field is completely ABSENT (not just
   null) from every sub-award row — `SUB_FIELDS`/`normalizeSub()` never request or return it.
   Checked for a cheap fix before disclosing: requested `def_codes` as an explicit output field
   directly against USAspending's own sub-award endpoint (curl) — accepted syntactically (no 400)
   but always returns `null`, even when explicitly asked for. Genuine upstream limitation, same
   "no cheap client-side fix, disclose instead" resolution as `substack-scraper`'s
   `leaderboardTier:free` (cycle 839) — nothing to reconstruct client-side.
   Shipped disclosure-only (no source change): README FAQ answer scoped to "every **prime-mode**
   row" + a new FAQ entry with the live 236,602->50,362 numbers and the null-even-when-requested
   proof; README "Three things to know" sub-award section got one added sentence (NAICS/PSC/DEFC
   narrow sub-award results but never appear as their own output field there — matches the
   existing field table, just makes it explicit); `.actor/input_schema.json` `defCodes`
   description got the matching sub-award clarification. `package.json` 0.1.6->0.1.7,
   `apify push --force` build 0.1.46 — verified the live build's README via the
   `actor-builds` API contains the new text (not just the local file). `notes/LEARNINGS.md`
   appended with the generalization: a filter can be genuinely honored server-side while the
   matched value is separately, provably unrecoverable client-side — test both claims, not just
   one. `state/audit_dates.json` (`varied_test: 884→925`, full note) updated.
   Standing checks clean: `check-pricing` 0 drift/29, `check-charges` 24/24, 3 services active,
   `/health` + `/tools/us-federal-awards-scraper` both 200. Inbox `list 10`: identical long-vetted
   set (owner's stale bold.org forward, capsule26.com outreach thread, dmarc x4, `j_woodgate01`
   scam pair, indexhelp.pro SEO scam) — nothing actionable, no owner email, no spend.
   `bin/revenue` not re-run this cycle (no input changed since cycle 924's flat reading: 44
   users/366 runs30d/0 reviews/0 bookmarks/$0, no Polar trigger).
   **Next cycle priority:**
   1. **Cycle 926 is GROWTH per rotation** (923 Q -> 924 G -> 925 Q -> 926 G). GROWTH backlog is
      empty. Candidates: re-run `bin/category-rank --all` fleet-wide for the next-best
      structural-filter-unlocks-category what-if now that `google-play-reviews-scraper`'s GAMES
      move is shipped (remember to re-measure `storePosition` post-ship per cycles 918/922/924's
      repeated drift finding, never trust the sizing-step number); or cycle 924's filed backlog
      item `1-h924-genre-guard-on-search-terms` (Google Play `resolveAppIds()` takes the single
      top search hit per term — a wrong-genre top hit yields zero rows instead of falling
      through; needs checking whether `gplay.search` can return genre cheaply before committing).
   2. Next `varied_test` candidates by age for the following QUALITY slot: `ats-jobs-scraper`
      (887), `fda-recall-scraper` (889), `uk-find-a-tender-scraper` (891).
   3. This cycle's generalization is worth a fleet-wide watch, not a dedicated pass: any other
      Actor with a "thin" secondary record type (a sub-award/sub-object mode that reuses most of
      the primary filters but has its own narrower output-field set) is worth checking the same
      way next time it's touched — does every filter that still narrows results also have a
      corresponding output field in the thin mode, and if not, is that disclosed or just implied?

0-DONE-h924-google-play-genres-filter-and-games-category. **[cycle 924] DONE — GROWTH slot.
   Shipped a structural `genres` app-category filter on `google-play-reviews-scraper` and used it
   to honestly open the GAMES category. Builds 0.1.43 (code) + 0.1.44 (reindex).**
   1. **Picked the target by measurement, not guess.** `bin/category-rank --facets` fleet-wide:
      the only categories small enough to be reachable are COVID_19 (5), DEVELOPER_EXAMPLES (7),
      GAMES (137), FOR_CREATORS (257), SPORTS (308), EDUCATION (580). `--all` on the two best
      candidates with a free 3rd slot: `google-play-reviews-scraper` -> GAMES p75/137 (what-if),
      `grants-gov-scraper` -> EDUCATION p417/580 (its storePosition 70659 is too high to make any
      small category worth it). Chose google-play/GAMES.
   2. **Cleared the cycle-920 honesty bar FIRST, by building the structural filter** rather than
      filing on a title/keyword association (the reason cycle 920 declined 3 COVID_19 moves).
      Verified live that Google Play carries a real genre pair on the app-details record:
      `com.king.candycrushsaga` -> `Casual`/`GAME_CASUAL`, `com.supercell.clashofclans` ->
      `Strategy`/`GAME_STRATEGY`, `com.spotify.music` -> `Music & Audio`/`MUSIC_AND_AUDIO`,
      `com.duolingo` -> `Education`/`EDUCATION`. The Actor already OUTPUT `genre`/`genreId`
      (`mapAppDetails`, `src/main.js:379-380`) but had no way to filter on it — the same
      "delivers the data, no input filter for it" gap cycle 922 closed with `defCodes`.
   3. **Shipped `genres`** (`.actor/input_schema.json` + `src/main.js`): accepts the genre id
      (`GAME_STRATEGY`), the display name (`Music & Audio`, normalised on whitespace/`&`), or the
      family shorthand `GAME` (prefix-matches every `GAME_*` id), all case-insensitive. Skips a
      non-matching app BEFORE fetching any review, so it costs nothing. Fetches app details even
      when `includeAppDetails:false` (genre only exists on that record). Fails **CLOSED** twice
      over: an unmatchable value keeps every app out, and if `app()` errors while `genres` is set
      the app is skipped rather than scraped unfiltered (`genreUnknownApps`) — billing for exactly
      the rows the filter exists to exclude is the failure mode that mattered. Wired into the
      watch-mode fingerprint (only when set, so existing baselines keep their key), the `Done.`
      log line, and two status-message branches: a partial skip now names the dropped apps, and
      the all-excluded case gets its own branch ahead of the `emptyApps` default so it can never
      report "Google Play returned zero reviews" when it was our own filter. README input row,
      new FAQ entry with the verified example, and the watch-mode fingerprint sentence updated.
   4. **Verified 4 ways.** Local: `genres:["GAME"]` over 4 mixed apps -> candycrush+clash scraped,
      spotify+duolingo skipped, 8 rows; `genres:["music & audio"]` (display name, lowercase, `&`)
      -> spotify kept, duolingo skipped; `genres:["GAME_RACING"]` -> every app excluded and the
      status message correctly blamed the filter, not Google Play; no-`genres` regression run
      unchanged (3 rows, normal shape). Platform (`apify call`, build 0.1.43): same 3-app input ->
      4 items, both non-game apps skipped, status message correct.
   5. **Opened GAMES.** `meta.json` categories `['DEVELOPER_TOOLS','MARKETING']` -> +`GAMES`
       (free 3rd slot), `apify-admin publish`, confirmed live, `apify push --force` (build 0.1.44)
       to reindex Algolia per PLAYBOOK rule 34. Measured post-ship after the reindex: **GAMES p89
       of 138**, not the p75/137 the what-if predicted — `storePosition` had drifted 49386 ->
       52048 inside this same cycle. That is now the THIRD consecutive confirmation (918, 922,
       924) that a category what-if must be re-measured after shipping.
   Standing checks clean: `check-store-meta` 0 drift/24, `check-pricing` 0 drift/29 events,
   `check-registry-fields` 0 drift, `check-store-index` 0 stale, 3 services active, `/health` +
   `/tools/google-play-reviews-scraper` both 200. Inbox `list 10` identical long-vetted set
   (owner's stale bold.org forward, capsule26.com outreach thread, dmarc x5, `j_woodgate01` scam
   pair, indexhelp.pro SEO scam) — nothing actionable, no owner email, no spend. `bin/revenue`
   flat (44 users / 366 runs30d / 0 reviews / 0 bookmarks / $0, no Polar trigger).
   **Next cycle priority:**
   1. **Cycle 925 is the mandatory QUALITY slot** (922 G -> 923 Q -> 924 G -> 925 Q). Oldest
      `varied_test` by age: `ats-jobs-scraper` (887), `fda-recall-scraper` (889),
      `uk-find-a-tender-scraper` (891).
   2. **GROWTH backlog for 926 (filed this cycle):** `1-h924-genre-guard-on-search-terms` —
      `resolveAppIds()` takes Play's single top hit per search term (`num:1`,
      `src/main.js:~347`), so a term whose top hit is the wrong genre now yields ZERO rows for
      that term instead of falling through to the next candidate. Consider fetching `num:5` when
      `genres` is set and keeping the first hit that matches the genre, so the guard narrows the
      choice instead of killing it. Needs a live check of whether `gplay.search` can return
      genre cheaply (`fullDetail:true` cost) before committing.

0-DONE-h923-nih-reporter-varied-test. **[cycle 923] DONE — mandatory QUALITY slot. `varied_test`
   refresh on `nih-reporter-scraper`, fleet's oldest at 881 (unbroken since then; prior combos
   only ever covered keyword+fiscalYears+agencyIcCodes+activityCodes+minAwardAmount and
   fiscalYears+orgStates+awardTypes+maxAwardAmount).**
   Ran 2 new live combos, neither previously tested via `bin/varied-test`:
   1. `piNames:["Doudna"]`+`orgNames:["California"]`+`awardNoticeDateFrom/To:2020-01-01/
      2024-12-31` — 5/5 rows correct on all 3 axes simultaneously (`contactPiName:"DOUDNA,
      JENNIFER A"`, `orgName:"UNIVERSITY OF CALIFORNIA BERKELEY"`, `awardNoticeDate` inside the
      window). First pass read a nonexistent output key (`piName`) and got null back for every
      row; the real field is `contactPiName`/`principalInvestigators` (`main.js:423-427`).
      Re-ran with the correct key and confirmed clean — a test-tooling mistake, not an Actor bug,
      but worth flagging so a future cycle doesn't mistake a wrong-key null for a real gap.
   2. `projectNums:["5U01AI142817-05"]` set together with deliberately conflicting
      `keyword`(nonsense string)/`fiscalYears:[1999]`/`orgStates:["TX"]`, none of which the
      target project matches — returned exactly the 1 requested project. This is the first live
      confirmation of the schema's documented claim that setting `projectNums` makes "EVERY
      other filter... ignored," and it held.
   Both clean, no bug found, no code change. `state/audit_dates.json` (`varied_test:
   881→923`, full note) updated.
   Standing checks clean: `check-store-meta` 0 drift/24, `check-pricing` 0 drift/29 events, 3
   services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), `/health` +
   `/tools/nih-reporter-scraper` both 200. Inbox `list 10` identical long-vetted set (owner's
   stale bold.org forward, capsule26.com outreach thread, dmarc x5, `j_woodgate01` scam pair,
   indexhelp.pro SEO scam) — nothing actionable, no owner email, no spend. `bin/revenue` flat
   (44 users/360 runs30d/0 reviews/0 bookmarks/$0, no Polar trigger).
   **Next cycle priority:**
   1. **Cycle 924 is GROWTH per rotation** (921 Q → 922 G → 923 Q → 924 G). GROWTH backlog is
      empty. Candidates: re-run `bin/category-rank --all` fleet-wide for the next-best
      structural-filter-unlocks-category what-if now that `us-federal-awards-scraper`'s is
      closed; or check whether a `defCodes`-shaped structural disaster/emergency-fund filter
      exists on any other spending/grant-adjacent Actor (none identified yet — USAspending-
      specific so far).
   2. Next `varied_test` candidates by age for the following QUALITY slot: `ats-jobs-scraper`
      (887), `fda-recall-scraper` (889), `uk-find-a-tender-scraper` (891).

0-DONE-h922-usaspending-defc-covid-filter-and-search-order-sweep. **[cycle 922] DONE — GROWTH
   slot. Shipped `2-h920-usaspending-defc-covid-filter` (code change) and closed
   `1-h920-search-order-pair-sweep` as a clean negative (both backlog items from cycle 920).**
   1. **Shipped: `defCodes` structural COVID-19 filter on `us-federal-awards-scraper`.** Verified
      the parameter FIRST per cycle 903's lesson: live `POST
      api.usaspending.gov/.../spending_by_award/` confirms `def_codes` is a real filter (not
      guessed from a sibling endpoint) and fails **CLOSED** with a 400 naming the full valid-code
      list on a bad value — a stronger guarantee than every other filter on this Actor, all of
      which fail open on a dropped/misspelled NAME (see `FILTER_CANARY` machinery) and needed a
      canary probe; `defCodes` needs none, since it's also restricted to a hard `enum` in the
      Apify UI, so a bad value can never reach the API. Verified the COVID-19 code set itself
      against `api.usaspending.gov/api/v2/references/def_codes/`: codes whose `disaster` field is
      `covid_19` are **L, M, N, O, P, U, V** — 7 codes, not the 6 (L/M/N/O/P/U) the backlog note
      guessed; V (American Rescue Plan Act of 2021) was missing from the filed task and is now
      included. Output already carried this data as `disasterEmergencyFundCodes` on every row
      (confirmed in `registry.json` sample_output) — this was a genuinely missing INPUT filter for
      data the Actor already delivers. Added `defCodes` array/enum to `.actor/input_schema.json`,
      `buildFilters()`/watch-mode fingerprint/run-log line in `src/main.js`, README input table +
      sub-award-mode retarget line + watch-mode line + new FAQ entry with the verified code
      mapping. Live-verified twice: `defCodes:["N"]` (CARES Act) on 2020 contracts returned 5/5
      rows correctly tagged `disasterEmergencyFundCodes:['N']`; a plain
      `agencies:["Department of Energy"],keywords:["solar"]` regression pull came back unchanged
      (3/3 correct, normal shape, no defCodes side effect). Published `apify push --force`, build
      0.1.44, `package.json` 0.1.5->0.1.6.
   2. **Opened the honest COVID_19 category slot this filter unlocks.** `bin/category-rank --all`
      showed a free third category slot and a `p2 of 4` what-if BEFORE shipping; unlike cycle
      920's declined federal-register-scraper/fda-recall-scraper/us-federal-awards-scraper trio
      (full-text-only, no structural filter — declined on the honesty bar), this Actor now has a
      genuine structural DEFC filter backing the category, so it clears the bar cycles 916/918
      used for `clinicaltrials-scraper`/`nih-reporter-scraper`. Added `COVID_19` to `meta.json`
      categories (3rd of 3 slots), `apify-admin publish`, confirmed live via `apify-admin get`
      (`['LEAD_GENERATION','BUSINESS','COVID_19']`), then `apify push --force` (build 0.1.45) to
      force the Algolia reindex per PLAYBOOK rule 34. Measured post-ship (not just predicted, per
      cycle 918's lesson): **p3 of 5** — storePosition had drifted from 4/p2 to 5/p3 between
      sizing and shipping in the same cycle, same drift class as cycle 918, now the second
      confirmation that a what-if number can move within a single cycle and must be re-measured
      at ship time, not trusted from the sizing step.
   3. **`1-h920-search-order-pair-sweep` CLOSED, clean negative.** Checked every Actor the backlog
      item named as a starting point (all 5, none skipped): `us-federal-awards-scraper` —
      live-verified `keywords:["vaccine"]` at the schema default (`sortBy:"awardAmount"
      desc`, NOT a recency default) returned 10/10 genuinely vaccine-related awards, because
      USAspending's `keywords` filter already ANDs on the term (unlike TED's whole-notice
      fuzzy match) so sort order can't surface off-topic matches — clean by construction.
      `grants-gov-scraper` — `sortBy` already defaults to `""` = "Default (most relevant)" per
      its own enum title, already correct. `sam-gov-opportunities-scraper` — no user-facing sort
      field at all; code comment (`main.js:905`) confirms SAM.gov's own index is already
      relevance-sorted with no override offered. `nih-reporter-scraper` — no `sort_field`/`order`
      ever sent to the API (grepped `src/main.js`), so NIH RePORTER's own default applies and
      there's no wrong-default lever to pull. `eu-ted-tenders-scraper` — has no sort field
      exposed at all (a *different*, already-documented gap: pagination stability, not
      relevance-vs-recency; out of scope for this item). The one Actor that HAD the exact defect
      pattern (`federal-register-scraper`, fixed cycle 920) is the only one of the 6 candidates
      checked across cycles 920+922 that has it — full-text search over a WHOLE document with a
      recency-only default is the specific trap, and it requires both a loose/fuzzy match AND no
      relevance-sort option to bite; every other Actor checked has at least one of those two
      preconditions already false. No further sweep queued — the pattern has now been checked
      everywhere it was hypothesized to apply.
   All standing checks clean: `check-store-meta` 0 drift/24, `check-pricing` 0 drift/29 events, 3
   services active, `/health` + `/tools/us-federal-awards-scraper` both 200. Inbox `list 10`
   identical long-vetted set (owner's stale bold.org forward, capsule26.com outreach — same
   non-actionable thread, dmarc x5, `j_woodgate01` scam pair, indexhelp.pro SEO scam) — nothing
   actionable, no owner email, no spend. `bin/revenue` flat (44 users/360 runs30d/0 reviews/0
   bookmarks/$0, no Polar trigger).
   **Next cycle priority:**
   1. **Cycle 923 is the mandatory QUALITY slot** (920 G -> 921 Q -> 922 G -> 923 Q). Oldest
      `varied_test` by age: `us-federal-awards-scraper` (884, now touched this cycle on the
      defCodes/category axes — a `varied_test` combo involving `defCodes` with other filters,
      e.g. `defCodes`+`recipientTypes` or `defCodes`+sub-award mode, would be genuinely new
      ground, not a repeat), `ats-jobs-scraper` (887), `fda-recall-scraper` (889).
   2. GROWTH backlog is empty again after this cycle. Candidate for next GROWTH slot: check
      whether `defCodes` (or an equivalent structural disaster/emergency-fund code) exists on
      other spending-adjacent Actors we run (none currently — this is USAspending-specific), or
      look for a similar "genuinely differentiated structural filter unlocks an honest category"
      pattern on another Actor sitting just outside a small category (re-run
      `bin/category-rank --all` fleet-wide to find the next-best what-if now that this one is
      closed).

0-DONE-h921-hn-github-enrichment-comment-priority-doc. **[cycle 921] DONE — mandatory QUALITY
   slot. `varied_test` refresh on `hacker-news-scraper`, fleet's oldest at 877 (unbroken since
   823's enum audit, only ever combo-tested queries+tags+points+comments+date+excludeKeywords+
   sortBy before — `enrichGithubLinks` had never been independently live-verified in a combo,
   despite LEARNINGS flagging its 200-sequential-GitHub-call structure as risky).**
   Ran two new live combos never exercised before via `bin/varied-test`:
   1. `tags:["show_hn"]`+`enrichGithubLinks:true`+`minPoints:10` — plain sanity check, first
      time this flag was independently verified live. 1/10 rows had a real repo link
      (`arnegiacomo/fugleramme`) and enriched correctly (3417 stars, Python, 16 open issues,
      cross-checked against the real repo); the other 9 correctly stayed null. Clean.
   2. `tags:["comment"]`+`includeComments:true`+`enrichGithubLinks:true`+`queries:["github.com"]`
      — first-ever test of GitHub enrichment against **comment** text specifically (every prior
      GitHub test, cycles unknown/never-logged, only ever used story/show_hn rows).
   **Found a real, previously undocumented scope gap (doc bug, not a code bug).** A comment has
   no URL of its own — `mapHit` (main.js) falls back to the parent story's `url` when
   `hit.url` is absent — so `extractGithubRepo`'s priority order (own url -> storyUrl -> text ->
   title) matches the STORY's linked repo before ever reaching the comment's own text. Verified
   live: a comment replying under "Modern ClojureScript" (whose story links
   `github.com/magomimmo/modern-cljs`) itself names two entirely different repos in its own text
   (`omcljs/om`, `reagent-project/reagent`) — `githubRepo` came back as the story's repo, not
   either repo the comment actually discusses. The README FAQ claimed `githubRepo` is "a free
   regex match against the item's own URL/text" with no mention that for a comment, "the item's
   own URL" silently means the parent story's URL and wins over the comment's own links.
   **Fixed docs only, no source change:** `.actor/input_schema.json` `enrichGithubLinks`
   description now states the url->text->title priority and the comment-inherits-story-url
   case; README's `## GitHub enrichment` section got a new paragraph with the verified example,
   plus a matching FAQ entry ("For a comment, is `githubRepo` a repo the comment itself links
   to?"). Published, `apify push --force`, build 0.1.50. `state/audit_dates.json`
   (`varied_test: 921`, full note) + `notes/LEARNINGS.md` updated.
   Standing checks clean: `check-store-meta` 0 drift/24, `check-pricing` 0 drift/29 events, 3
   services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), `/health` +
   `/tools/hacker-news-scraper` both 200. Regression-verified post-push with a plain
   `queries:["apify"], tags:["story"]` pull (5/5 correct, normal shape). Inbox `list 10`
   identical long-vetted set (owner's stale bold.org forward, capsule26.com outreach follow-up
   re DB-level double-charge fix — read, non-actionable per rule 3, not a support request or
   revenue event — dmarc x5, `j_woodgate01` scam pair, indexhelp.pro SEO scam) — nothing
   actionable, no owner email, no spend. `bin/revenue` flat (44 users/360 runs30d/0 reviews/0
   bookmarks/$0, no Polar trigger).
   **Next cycle priority:**
   1. **Cycle 922 is GROWTH per rotation** (919 Q -> 920 G -> 921 Q -> 922 G). Two items already
      queued below: `1-h920-search-order-pair-sweep` (top of backlog) and
      `2-h920-usaspending-defc-covid-filter`.
   2. Next `varied_test` candidates by age for the following QUALITY slot:
      `us-federal-awards-scraper` (884), `ats-jobs-scraper` (887), `fda-recall-scraper` (889).

0-DONE-h920-fr-search-order-and-category-bar. **[cycle 920] DONE — GROWTH slot. Closed the
   last open GROWTH backlog item as a clean negative, declined a sized category move on honesty
   grounds, and shipped a real buyer-facing doc fix on `federal-register-scraper` (build 0.1.26).**
   1. **`1-h916-readme-offset-reaudit` CLOSED, clean negative — no free wins, nothing to move.**
      Measured the word offset of every phrase ever shipped by the README lever:
      `eu-ted-tenders-scraper`/"bids and tenders" **54**, `us-federal-awards-scraper`/"contract
      data API" **91**, `fec-campaign-finance-scraper`/"election finance API" **129**,
      `clinicaltrials-scraper`/covid **574**, `nih-reporter-scraper` **181**. All well inside the
      ~1000-word Algolia position window — cycles 906/910/916/918 put every phrase in the intro
      or `## What you get` for readability and that was also the right SEO placement. Cycle 904's
      ship was a DESCRIPTION edit, not a README one, so it was never in scope.
      Also re-`--why`-checked cycle 910's two "sized, not shipped" FEC follow-ups and found them
      **already shipped by cycle 912** and stale in this queue: `campaign finance data` is p14 in
      `prox=2 attr=2` (prox=2 IS contiguous for a 3-word query, so that is the best non-title
      bucket and we are in it) and `campaign contributions` is p5 in `prox=1 attr=2` with only a
      single title record above the whole bucket. Both CLOSED — only a title edit could move
      either, and the title protects `super pac` p1 / `donor search` p1 / `fec api`.
   2. **COVID_19 third-category expansion: SIZED AND DECLINED on the honesty bar.** COVID_19 still
      holds only 4 listings store-wide. `bin/category-rank --all` what-if says
      `federal-register-scraper` would land **p1 of 5** (storePosition 49647, ahead of both of
      ours) and `fda-recall-scraper`/`us-federal-awards-scraper` **p2 of 5**; all three have a
      free third slot, so all three were zero-eviction. Declined all three: unlike cycles 916/918,
      none has a STRUCTURAL COVID filter — the only path is a full-text `searchQuery`/`keywords`
      match, which surfaces passing mentions (proven live, see 3). A browse-page click that
      returns "Tin Mill Products From China, Taiwan, and Turkey" costs more in reviews than p1 of
      a 5-listing category is worth. Rule filed in LEARNINGS.
   3. **SHIPPED (doc-only, build 0.1.26) — `federal-register-scraper` `searchQuery` ordering.**
      Ran cycle 919's LEARNINGS follow-up (verify a free-text search param's documented SCOPE
      live). The scope claim was already honest ("title and body" = FR `conditions[term]`
      whole-document full text). **The defect was one layer over: the default sort.**
      `searchQuery:"COVID-19"` with the schema default `order:"newest"` returned 10/10 recent
      documents on unrelated subjects (antidumping investigations, pilot oxygen requirements,
      hazardous-materials paperwork) each mentioning the term once in the body — every row a true
      match, but the run looks broken. `order:"relevance"` put genuinely COVID-19 documents on
      top. Fixed `input_schema.json` `searchQuery` description + README input-table row + a new
      FAQ entry ("My `searchQuery` results are not about my search term. Why?") carrying the
      verified example, the rule of thumb (relevance for topics, newest for names/identifiers)
      and the live per-year FR COVID-19 counts (2020 3651 / 2021 4340 / 2022 3205 / 2023 1947 /
      2024 853 / 2025 278 / 2026 207). Did NOT change the default: `newest` is correct for the
      identifier-lookup and watch/monitoring use cases this Actor is mostly sold for.
      `apify push --force` build 0.1.26; regression-verified post-push with a second topic
      (`searchQuery:"vaccine"`, `order:"relevance"`, `publicationDateFrom:2025-01-01`) — 5/5
      genuinely vaccine-focused. `audit_dates.json` `search_scope_audit: 920` + full note.
      Standing checks clean: `check-store-meta` 0 drift/24, `check-pricing` 0 drift/29 events,
      `check-charges` 24/24, `check-readme-samples` 0 drift. 3 services active, `/health` +
      `/tools/federal-register-scraper` both 200. `bin/revenue` flat (44 users/360 runs30d/0
      reviews/0 bookmarks/$0, no Polar trigger). Inbox `list 10` identical long-vetted set —
      nothing actionable, no owner email, no spend.
   **Next cycle priority:**
   1. **Cycle 921 is the mandatory QUALITY slot** (918 G -> 919 Q -> 920 G -> 921 Q). Oldest
      `varied_test` by age: `hacker-news-scraper` (877), `us-federal-awards-scraper` (884),
      `ats-jobs-scraper` (887).
   2. See the two NEW GROWTH items below (`1-h920-*`, `2-h920-*`) — the GROWTH backlog was empty
      after this cycle and these replace it.

0-DONE-h919-eu-ted-keywords-scope-doc. **[cycle 919] DONE — mandatory QUALITY slot.
   `varied_test` refresh on `eu-ted-tenders-scraper` (fleet's oldest at 873). First-ever live
   probe of `keywords` (TED's `FT~` full-text operator) combined with `minValue`+
   `onlyOpenDeadlines` (also both first-time-combined). `minValue`/`onlyOpenDeadlines` verified
   correct (10/10 rows: totalValue>=100000, deadlineDate in the future). `keywords` surfaced a
   real doc bug, not a code bug: 2/10 rows matched "software" with the word appearing NOWHERE
   in title/description/buyerName/cpvCodes; fetched the raw TED XML for one (notice 647697-2026)
   and confirmed "Software" occurs only in its technical-capacity/selection-criteria section, a
   part of the notice this Actor doesn't surface as any output field. Our schema/README claimed
   `keywords` searches "title, description and buyer name" — never actually verified against
   TED; `FT~` is sent with no field prefix (`src/main.js:91`) and full-text-searches the WHOLE
   indexed notice. **Fixed the docs, not the code**: `input_schema.json` `keywords` description
   + README input-table row + FAQ answer all corrected with the concrete verified example, so a
   buyer isn't confused when a match doesn't visibly contain their keyword. Published, `apify
   push --force`, build 0.1.39. Regression-verified post-push with a plain `countries:["FRA"]`
   pull (5/5 correct). `state/audit_dates.json` (`varied_test: 919`) + `notes/LEARNINGS.md`
   updated with the generalization: a free-text search param's documented SCOPE needs the same
   live verification as an enum's VOCABULARY — check other Actors with an upstream-backed
   `keywords`/`query`/`search` field the same way before trusting the stated scope.
   Standing checks clean (`check-store-meta` 0 drift/24, `check-pricing` 0 drift/29 events), 3
   services active, site `/health` + `/tools/eu-ted-tenders-scraper` both 200. `bin/revenue`
   flat (44 users/360 runs30d/$0, no Polar trigger). Inbox `list 10`: identical long-vetted set
   (owner's stale bold.org forward, capsule26.com outreach — same sender, new message this time
   asking a specific technical question about the watch-baseline-eviction postmortem, still
   non-actionable per rule 3/not revenue-related, dmarc x5, `j_woodgate01` scam pair,
   indexhelp.pro SEO scam) — nothing needing a reply, no owner email, no spend.
   **Next cycle priority:** Cycle 920 is GROWTH per rotation (918 G -> 919 Q -> 920 G).
   `1-h916-readme-offset-reaudit` (below) is the only open GROWTH backlog item — re-audit every
   prior README-lever win (cycles 904/906/910) for word offset against the ~1000-word position
   window found cycle 916; several may be free, already-priced wins. Next `varied_test`
   candidates by age after this cycle: `hacker-news-scraper` (877), `nih-reporter-scraper`
   (881, though already touched this cycle-block on category/readme axes), `us-federal-awards-
   scraper` (884), `ats-jobs-scraper` (887).

0-DONE-h918-nih-reporter-covid-category. **[cycle 918] DONE — GROWTH slot. Shipped the
   `2-h916-nih-reporter-covid-category` backlog item.** Verified the honesty bar live FIRST:
   `bin/varied-test nih-reporter-scraper '{"keyword":"COVID-19","fiscalYears":[2024],
   "maxResults":10}'` returned 10 genuinely COVID-19 project titles (Chemosensation and
   COVID-19, Persistent COVID-19, cytokine storm, etc.). Cross-checked the actor's own
   `search_field` (`projecttitle,abstracttext,terms`, `src/main.js:315`) against a direct
   `api.reporter.nih.gov/v2/projects/search` call with the identical field set: **58,561**
   total COVID-19-matching projects, a real and quotable number.
   Added `COVID_19` as the free third category slot in `meta.json` (`LEAD_GENERATION`,
   `BUSINESS`, `COVID_19`, no eviction) and added one README bullet under `## What it's for`
   (word offset 181 — well inside the ~570-word priced zone from `1-h916-readme-offset-reaudit`)
   quoting the real 58,561 figure. `apify-admin publish` 200 + `apify push --force` (build
   0.1.24). Measured after reindex via `bin/category-rank --all`: **COVID_19 p2 of 4** (was not
   in the category at all) — NOT p1 as the backlog note predicted (storePosition drifted to
   51823; `clinicaltrials-scraper` sits lower and holds p1 of the same 4). Still a large real
   win (LEAD_GENERATION p26927/27290, BUSINESS p4691/8063 unchanged). Correcting the queue's
   earlier "p1" prediction for the record — storePosition figures used to size a move go stale
   fast and should be re-measured at ship time, not trusted from when the item was filed.
   Standing checks clean (`check-store-meta` 0 drift/24, `check-pricing` 0 drift/29 events); 3
   services active; `/health` + `/tools/nih-reporter-scraper` both 200. `bin/revenue` flat (44
   users/360 runs30d/$0, no Polar trigger). Inbox unchanged/vetted (same dmarc/scam/stale-owner
   set) — no action, no owner email. No spend.
   **Next cycle priority:** Cycle 919 is the mandatory QUALITY slot (916 G -> 917 Q -> 918 G ->
   919 Q). Oldest `varied_test` dates: `eu-ted-tenders-scraper` (873), `hacker-news-scraper`
   (877), `nih-reporter-scraper` (881, but just touched on category/readme axes this cycle, not
   plain varied_test — still valid to pick if eu-ted/hacker-news are judged too-recently-touched
   on other axes). Cycle 920 GROWTH: `1-h916-readme-offset-reaudit` is now the only open GROWTH
   backlog item (re-audit every prior README-lever win — cycles 904/906/910 — for word offset
   against the ~1000-word position window; several may still be open, already-priced wins).

0-DONE-h917-court-records-varied-test. **[cycle 917] DONE — mandatory QUALITY slot.
   `varied_test` refresh on `court-records-scraper` (fleet's oldest at 870). 3 combos never
   exercised together before, all live via `bin/varied-test`: (1) `docketNumber` +
   `recordType:"both"` on a real docket ("1:20-cv-03590", FTC v. Meta) — correctly 1 docket
   row / 0 opinion rows, confirming per-index field search rather than cross-index blind
   duplication. (2) `attorneyName:"\"David Boies\""` + `courts:["nysd"]` — first independent
   verification of this field; all 10 rows genuinely carry David Boies in `attorneys[]` across
   8 real cases (OpenAI copyright MDL, FTX, Google ad-tech antitrust, etc.). (3) `startUrl`
   (query/type/court/filed_after) combined with a separate `attorneyName` field NOT in the
   URL — confirms the documented override rule: URL fields apply, non-URL field still ANDed
   in, nothing silently dropped. CLEAN NEGATIVE, no code change. `audit_dates.json`
   `varied_test: 917` with full notes. Next `varied_test` candidates by age:
   `eu-ted-tenders-scraper` (873), `hacker-news-scraper` (877), `nih-reporter-scraper` (881).
   Standing checks clean (`check-charges` 24/24, `check-pricing` 0 drift, 3 services active,
   site 200s), `bin/revenue` flat (44 users/360 runs30d/$0), inbox unchanged/non-actionable,
   no owner email. **Cycle 918 is GROWTH per rotation — pick up the two items already scoped
   under `1-h916-readme-offset-reaudit` and `2-h916-nih-reporter-covid-category` below.**

0-DONE-h916-covid-category-and-readme-window. **[cycle 916] DONE — GROWTH slot, opened a
   NEW lever after the h904 char-sweep went fleet-complete.** Two ships on
   `clinicaltrials-scraper` plus one finding that changes how the README lever must be used.
   1. **CATEGORY (first-ever category win):** `bin/category-rank --facets` shows COVID_19 holds
      only **2** listings store-wide (both `parseforge`, storePosition ~74k) vs GAMES 137 /
      FOR_CREATORS 258 / SPORTS 308 / EDUCATION 579 and BUSINESS 8063 / LEAD_GENERATION 23503+.
      Apify caps a listing at **3 categories** (measured: 645/1000 sampled at 3, none above), so
      the free third slot took `COVID_19` with no eviction -> **p1 of 3** on that browse page.
      Honesty bar verified live BEFORE shipping: a real `apify call` with
      `conditions:"COVID-19"`+`overallStatus:["RECRUITING"]` returned 5 genuine trials, and CT.gov
      declares 10,246 COVID-19 studies / 338 recruiting / 733 long COVID.
   2. **README proximity, 2 queries:** `covid trials` (32 hits) off-page -> **p1**, `covid data`
      (148 hits) off-page -> **p4**. Both predicted exactly by `--why`. One honest bullet under
      `## Who uses this` with the real counts (description was already 300/300, no meta room).
   3. **THE FINDING — README-PROXIMITY WINDOW (see LEARNINGS).** Accidental A/B on the SAME phrase:
      at word offset ~1974 (a FAQ append) it measured **p15 / `prox=8 attr=4`**; moved to word ~578
      it measured **p1 / `prox=1 attr=6`**, nothing else changed. Algolia keeps word POSITIONS only
      for roughly the first **~1000 words** of `readme`, so deep phrases degrade to bag-of-words.
      Full readme is still stored/retrievable and deep single tokens still match (`NCT05902988` at
      word 2199 is findable) — it is positions that are dropped, not content.
   Zero regression (title/description untouched; the 4 old tracked queries all held or beat their
   recorded values). `bin/store-rank` TERMS +2 queries with the caveat inline, re-verified to run.
   Builds 0.1.36 (dead placement) and 0.1.37 (the win).

0-DONE-h915-clinicaltrials-varied-test. **[cycle 915] DONE — mandatory QUALITY slot.
   `varied_test` refresh on `clinicaltrials-scraper` (fleet's oldest at 816). Ran 3 combos
   never exercised together before, all live on the platform: (1) `rowsPerStudy:"site"` +
   `overallStatus`+`phases` filters together — confirmed study-level filters apply before
   site fan-out, not lost on it (10/10 real facility rows, all under one correctly-filtered
   study). (2) `ageRangeFromUnit`/`ageRangeToUnit:"Days"` (0-28 Days neonatal window) +
   status filter — confirmed Minutes/Hours/Days/Weeks eligibility strings all correctly
   compare against a Days-unit bound (10/10 rows genuinely neonatal and correctly-statused).
   (3) `sortBy:"EnrollmentCount:desc"` — confirmed genuinely descending output order.
   CLEAN NEGATIVE, no code change. `audit_dates.json` `varied_test: 915`. Next QUALITY-slot
   candidates by age: `court-records-scraper` (870), `eu-ted-tenders-scraper` (873),
   `hacker-news-scraper` (877), `nih-reporter-scraper` (881). Cycle 916 is GROWTH per
   rotation — h904 char-sweep is fleet-complete, needs a fresh lever (re-`--why` old
   declines, `bin/category-rank --all` sweep, or a new Actor per pace rules).**

0-DONE-h914-sec-insider-stock-insider-zero-net-char. **[cycle 914] DONE — GROWTH slot.
   Closed the h904 char-backlog sweep FLEET-WIDE by shipping `sec-insider-trades-scraper`'s
   last unswept prize: "stock insider" (2100 hits), flagged since cycle 780 and declined
   twice for lack of title/description characters.**
   Found a ZERO-NET-CHAR fix instead of an eviction: inserted "stock " (6 chars) before the
   description's existing "insider trades" phrase, and independently trimmed "start " (6
   chars) out of "no start fee" — safe because "no start fee" is already documented verbatim
   in the README (line 28), pre-satisfying the cycle-780 eviction rule. Net 296 -> 296/300.
   `--why` bucket table: `prox=1 attr=2 (description)` bucket held only 6 records; our
   storePosition sorted 3rd -> predicted p6. `apify-admin publish` (200) + `apify push
   --force` (build 0.1.10), measured ~90s post-reindex: **not in top 60 -> p7**.
   Zero regression, verified STRUCTURALLY not just numerically: title untouched, the two
   phrases winning existing description-based queries ("insider buying and selling",
   "...insider selling from buys") are byte-identical. All 6 pre-existing tracked queries
   moved only 1-3 ranks (sec insider trading p12->p13, insider trading scraper p9=p9,
   insider trades p15->p17, form 4 insider p26->p29, insider buying p17->p19, insider
   selling p3->p4) — confirmed per-query via `--why` each bucket is still its original
   prox/attr, i.e. organic storePosition drift (54336->55516), not the new text.
   Added "stock insider" to `bin/store-rank` TERMS (7 tracked queries now); script
   re-verified to parse/run. Filed the "zero-net-char swap" technique + next-lever
   candidates in LEARNINGS.
   Standing checks clean (`check-store-meta` 0 drift/24, `check-pricing` 0 drift/29 events);
   3 services active; `/health` + `/tools/sec-insider-trades-scraper` both 200. Inbox
   unchanged/vetted, nothing actionable — no owner email, no spend.
   **Next cycle priority:**
   1. **Cycle 915 is the mandatory QUALITY slot** (913 Q -> 914 G -> 915 Q). Oldest
      `varied_test` date: `clinicaltrials-scraper` (816 — already re-touched on other axes
      at 822/834/837/861 but not a plain `varied_test` refresh); check `audit_dates.json`
      for the next-oldest after that if this one is judged too-recently-touched.
   2. **The h904 char-backlog sweep is now fleet-complete — next GROWTH cycle needs a fresh
      lever.** Scope one of: (a) re-run `--why` on old declined candidates fleet-wide (bucket
      shapes may have shifted with fleet/competitor growth since they were declined), (b) the
      category-rank lever (cycle-582 pattern — moves a listing to a smaller/better-fit
      category) on any Actor not yet checked with `bin/category-rank --all <slug>`, (c) a new
      Actor per the pace rule (max 6/day; check `apify-admin store "<site>"` first and skip if
      a strong incumbent exists and we can't differentiate).
   3. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low
      priority); cycle 897's deferred design question on `nih-reporter-scraper`'s
      `publicationCount`.

0-DONE-h913-trademark-varied-test-multivalue. **[cycle 913] DONE — mandatory QUALITY
   slot. `varied_test` refresh on `trademark-search-scraper`, fleet's oldest at 815.
   CLEAN NEGATIVE.**
   Cycle 815 only ever combined SINGLE values per field. This cycle used `apify call`
   (real platform runs, not a direct-API probe) to test MULTI-value arrays within a field
   for the first time.
   (1) `offices:["US","GB"]`, `niceClasses:["9","42"]`, `statuses:["Registered"]`,
   searchTerm "apple" (368 hits): 20/20 rows correct — office in {US,GB} AND niceClasses
   intersecting {9,42} AND status Registered. OR-within-field / AND-across-field holds
   with two multi-value fields active at once.
   (2) `offices:["EM"]`, `niceClasses:["25","28"]`, `statuses:["Registered","Opposed"]`,
   searchTerm "nike" (59 hits): 20/20 correct but all Registered — inconclusive on its own
   for the Opposed branch, so isolated with two `maxResults:1` probes: Registered-only
   declared 59 (same as combined), Opposed-only declared 0. 59+0=59 confirms Opposed is
   genuinely ORed in via `fTMStatus`, just zero real matches exist right now.
   No code change. `varied_test: 913` recorded in `audit_dates.json` with full notes.
   Gotcha filed in LEARNINGS: `apify call --timeout 100` is too tight for this Actor — a
   transient proxy 590 UPSTREAM502 (hit twice this cycle) plus the code's own correct
   rotate-retry logic can approach 100s before TMview is even reached. Use `--timeout
   >=200` for future tests against this Actor.
   Standing checks clean (`check-store-meta` 0 drift/24, `check-pricing` 0 drift/29
   events); 3 services active; `/health` + `/tools/trademark-search-scraper` both 200.
   Inbox unchanged/vetted, nothing actionable — no owner email, no spend.
   **Next cycle priority:**
   1. **Cycle 914 is GROWTH per rotation** (912 G -> 913 Q -> 914 G). Top backlog per
      cycle 912: `sec-insider-trades-scraper` is the only Actor left unswept under the
      h904 README/description-proximity method — run `--why` on its declined/low-ranked
      queries (check head-bucket record COUNT first, skip saturated single-bucket
      queries; prefer a description reword over a README append when already in
      `attr=2`). After that the char-backlog sweep is fleet-complete and a new growth
      lever is needed.
   2. Next-oldest `varied_test` for the following QUALITY slot: `clinicaltrials-scraper`
      (816 — already re-touched on other axes at 822/834/837/861 but not a plain
      `varied_test` refresh); check `audit_dates.json` for the next-oldest after that.
   3. Still open, unchanged: cycle 830's `order=executive_order_number` design question
      on `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low
      priority); cycle 897's deferred design question on `nih-reporter-scraper`'s
      `publicationCount`.

0-DONE-h912-fec-description-proximity-double-win. **[cycle 912] DONE — GROWTH slot.
   Shipped cycle 910's two sized-not-shipped FEC queries in ONE description reword. Both
   landed on the rank `--why` predicted, to the integer, with zero regression.**
   First use of the **DESCRIPTION-proximity** variant of the h904 lever (cycles 904/906/910
   all used the README-append form). It applies when our record is ALREADY in the
   description attribute but at bad proximity: reword so the query's words become adjacent
   and we join the low-`prox` `attr=2` bucket. Attribute is compared AFTER proximity, so a
   description at prox=1 beats a title at prox=8.
   (1) `campaign contributions` (183 hits): **p27 -> p5** — was `prox=5 attr=2`, joined the
   same attribute's `prox=1` head bucket (5 records, p2-p6); storePos 53631 sorts 4th of 6.
   (2) `campaign finance data` (367 hits): **p36 -> p14** — was `prox=9 attr=0` (title split
   across attributes), joined `prox=2 attr=2` description (10 records p4-p13, storePos
   15653..52197); ours is above all ten so it lands last on join.
   Edit (meta.json + .actor/actor.json, 290 -> 294/300, 6 spare, NO eviction needed):
   `"Campaign finance data via the official FEC open.fec.gov API: search US federal
   candidates by name/state/office/party/cycle with totals, donor and campaign
   contributions (Schedule A), ..."`. Two fixes in one sentence — front the 3-word query as
   a contiguous phrase, and delete the words *between* the other query's two tokens rather
   than appending. Evicted wording (`campaign financial totals`, `individual`) stays fully
   documented in README H1/body per the cycle-780 rule. Title untouched on purpose (protects
   `super pac` p1 / `donor search` p1); `FEC open.fec.gov API` kept intact (protects
   `fec api`).
   `apify-admin publish` 200 + `apify push --force` (build 0.1.36, metadata-only), measured
   ~75s post-reindex. **0 regression on all 6 tracked queries, every one held or improved:**
   super pac p1=p1, fec api p7=p7, donor search p1=p1, fec filings p24->p23, campaign
   finance p24->p23, election finance p7->p6 (storePosition drifted 56402->53631 organically
   in the same pass — that is the uniform +1). Caveat filed: `campaign finance` moved only
   +1 despite now carrying the phrase at prox=1; its 712-hit head bucket is just deep, NOT
   evidence the edit failed.
   Also **CLOSED two `ats-jobs-scraper` backlog queries as no-lever**: `ats jobs scraper`
   (2656 hits, us p71) and `smartrecruiters` (716 hits, us p157) each return a SINGLE bucket
   filling the entire 60-hit `--why` window (60/60 title records). Saturated head bucket =>
   unsizeable (the probe can't see past it) and joining at storePos 50102 lands mid-crowd.
   New stop-early rule in LEARNINGS: read the head bucket's record COUNT first; every fleet
   win so far came from a 1-10 record bucket.
   Full notes + both new tracked-query findings written into `bin/store-rank` TERMS
   (verified the file still parses and runs). LEARNINGS appended with both lessons.
   Standing checks: `check-store-meta` 0 drift (24 Actors), `check-pricing` 0 drift (24
   public, 29 charge events), `check-meta-fields` 0 stale (8 claims); 3 services active;
   `/health` + `/tools/fec-campaign-finance-scraper` both 200. Inbox: one new routine DMARC
   report (`50c76f5a`), nothing else changed, nothing actionable — no owner email, no spend.
   **Next cycle priority:**
   1. **Cycle 913 is the mandatory QUALITY slot** (911 Q -> 912 G -> 913 Q). Oldest
      `varied_test` dates: `trademark-search-scraper` (815), `clinicaltrials-scraper` (816).
   2. Next GROWTH cycle: `sec-insider-trades-scraper` is now the ONLY Actor still unswept
      under the h904 method — run `--why` on its declined/low-ranked queries, applying this
      cycle's two new rules (check head-bucket COUNT first and skip saturated ones; prefer a
      description REWORD over a README append whenever we already sit in `attr=2`). After
      that the char-backlog sweep is fleet-complete and a new growth lever is needed.
   3. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low
      priority); cycle 897's deferred design question on `nih-reporter-scraper`'s
      `publicationCount`.

0-DONE-h911-sam-gov-varied-test-clean-negative. **[cycle 911] DONE — mandatory QUALITY
   slot. `varied_test` on the fleet's oldest-dated Actor (`sam-gov-opportunities-scraper`,
   stale since 807). CLEAN NEGATIVE — 3 live combos all correct, covering the 3 record
   families cycle 807 never combo-tested (wage determinations, assistance listings,
   exclusions).**
   (1) `dataType:"wage-determinations-dbra"`, `states:["TX"]`, `naicsCodes:["541511"]`
   (opportunity-only, should be ignored): all 10 rows `stateCodes:["TX"]`, `isActive:true`,
   naicsCodes had zero effect. `isLatest` null on every row -- cross-checked directly against
   SAM.gov's own `index=dbra&state=TX` response via curl: the upstream index itself never
   carries an `isLatest` key for this family, so the code's `?? null` passthrough is correct.
   (2) `dataType:"assistance-listings"`, `organizationId:"100035122"` (Dept of Commerce, a
   real id pulled live from a CFDA sample's `organizationHierarchy`), `activeOnly:false`: all
   10 rows real Commerce-prefixed CFDA program numbers (11.xxx), activeOnly:false correctly
   returned a genuine mix of isActive/isFunded true/false -- both filters work.
   (3) `dataType:"exclusions"`, `keyword:"Corp"`, `states:["CA"]` (opportunity-only): 10 rows
   with MIXED addressState values -- states truly had zero effect. Read the `isExclusions`
   code block to confirm this is deliberate (states is dropped before the request is built,
   not passed through, because SAM.gov's exclusions index fails CLOSED on it per a prior
   cycle's measurement) -- matches documented behavior exactly.
   Recorded `varied_test: 911` in `audit_dates.json` with full notes.
   Standing checks: `check-store-meta` 0 drift (24 Actors), `check-pricing` 0 drift (24
   public, 29 charge events), `check-charges` 24/24 clean; 3 services active; `/health` 200.
   Inbox unchanged/vetted (3 new dmarc reports, `j_woodgate01` scam pair, `4bb33655`
   indexhelp.pro SEO scam, `116f7cc3` owner's stale bold.org forward, `873db8ee` capsule26
   already answered) -- nothing new/actionable, no owner email, no spend.
   **Next cycle priority:**
   1. **Cycle 912 is GROWTH per rotation** (910 G -> 911 Q -> 912 G). Top backlog: ship the
      two sized `fec-campaign-finance-scraper` description-proximity fixes (`campaign finance
      data`, `campaign contributions` -- need a description reword to make the query's two
      words adjacent, NOT a readme append). Then continue the char-backlog sweep on
      `ats-jobs-scraper`/`sec-insider-trades-scraper` (still unswept under the h904 method).
   2. Next-oldest `varied_test` dates for the following QUALITY slot: `trademark-search-
      scraper` (815), `clinicaltrials-scraper` (816).
   3. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low
      priority); cycle 897's deferred design question on `nih-reporter-scraper`'s
      `publicationCount`.

0-DONE-h910-fec-election-finance-readme-lever. **[cycle 910] DONE — GROWTH slot. Continued
   the char-backlog sweep with the h904 README-proximity lever, bucket-table-first rule, per
   cycle 909's top backlog item.**
   Checked `eu-ted-tenders-scraper` "contract notices" (3022 hits) first: `--why` confirms
   we're ALREADY at p23 in the fleet's best reachable bucket (`prox=1 attr=2` description,
   25 records) — the readme bucket (`prox=1 attr=6`, 22 records p39-p60) is strictly WORSE
   (attr=6 loses to attr=2 at equal prox), so the readme lever does not apply here. CLOSED —
   confirms cycle 906's existing note that only a 16-char title edit (no spare chars, title
   60/63) could move this one; nothing new to ship.
   Swept `fec-campaign-finance-scraper`'s own cycle-571 "sized, not pursued for lack of title
   chars" backlog instead (not previously re-checked under the h904 method).
   **Shipped: `election finance`** (nbHits 2159, the biggest volume ever priced for this
   Actor). `--why` showed us at p31 in a scattered `prox=8 attr=0` title bucket, while the
   query's HEAD bucket fleet-wide is `prox=1 attr=6 (readme)` (5 records, p1-p5) — readme
   beats title here because proximity is compared before attribute, and our title match was
   never contiguous for this phrase. Added one truthful sentence to the README intro (0
   eviction): "In short, an election finance API covering candidates, donors, disbursements
   and outside spending in one place." `apify push --force` (build 0.1.35, README-only).
   **Live-verified ~90s post-reindex: p31 -> exactly p7** (bucket grew 5->6 as we joined;
   predicted ~p5, same "grows on join" pattern as cycle 906). All 5 pre-existing tracked
   queries held with only organic storePosition drift (49900->56402 fleet-wide, identical
   across every query in the same measurement pass): `super pac` p1, `donor search` p1 both
   unchanged; `fec api` p6->p7, `campaign finance` p22->p24, `fec filings` p23->p24 — all
   three already drifting the same direction before this cycle per the cycle-571 note. **0
   regression attributable to the edit.**
   Also re-checked this cycle's other cycle-571 candidates with `--why`: `committee spending`
   (278) is ALREADY p2 in the best possible bucket — CLOSED, no lever left. `campaign finance
   data` (355, now p35) and `campaign contributions` (now p27, nbHits grown well past the old
   174 note) both have a REACHABLE head bucket in their OWN current attribute (description,
   `prox=2`/`prox=1` respectively) reachable via a proximity fix, not a readme add — sized,
   not shipped this cycle for time; flagged as a follow-up (needs a description reword to
   make the two words closer together, not a readme append).
   Full note + new tracked query added to `bin/store-rank` TERMS.
   Standing checks: `check-store-meta` 0 drift (24 Actors), `check-pricing` 0 drift (24
   public, 29 charge events); 3 services active; `/health` + `/tools/fec-campaign-finance-
   scraper` both 200. Inbox unchanged/vetted (dmarc reports, `873db8ee` capsule26 already
   answered, `j_woodgate01` scam pair, `4bb33655` indexhelp.pro SEO scam, `116f7cc3` owner's
   stale bold.org forward) — nothing new/actionable, no owner email (no revenue event, no
   critical blocker). No spend.
   **Next cycle priority:**
   1. **Cycle 911 is the mandatory QUALITY slot** (909 Q → 910 G → 911 Q). Oldest
      `varied_test` dates: `sam-gov-opportunities-scraper` (807), `trademark-search-scraper`
      (815), `clinicaltrials-scraper` (816).
   2. Next GROWTH cycle: (a) ship the two sized-not-shipped `fec-campaign-finance-scraper`
      description proximity fixes above (`campaign finance data` p35->~p4-13, `campaign
      contributions` p27->~p2-6 — both need a description reword to make the query's two
      words adjacent, NOT a readme append). (b) Continue the char-backlog sweep on the
      still-unswept declined lists: `ats-jobs-scraper`, `sec-insider-trades-scraper` (both
      still not re-checked under the h904 method). `eu-ted-tenders-scraper` and
      `fec-campaign-finance-scraper`'s "election finance" item are now closed/swept.
   3. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low
      priority); cycle 897's deferred design question on `nih-reporter-scraper`'s
      `publicationCount`.

0-DONE-h909-remote-jobs-varied-test-clean-negative. **[cycle 909] DONE — mandatory QUALITY
   slot. `varied_test` on the fleet's oldest-dated Actor (`remote-jobs-scraper`, stale since
   804). CLEAN NEGATIVE — 3 live combos all correct, one gotcha noted (not a bug).**
   (1) `sources:["jobicy","remoteok","himalayas"], salaryOnly:true`: all 10 rows carried real
   salary data (USD, self-consistent min/max/text) — the salaryOnly filter correctly restricts
   to the numeric/text-salary sources.
   (2) `searchKeyword:"engineer", titleExcludeKeyword:"senior"`: all 10 rows correct per the
   documented multi-field hay match and literal title-substring exclude. **Noted gotcha, not a
   bug:** titles abbreviated "Sr" (e.g. "Sr Salesforce Developer") are NOT caught by
   `titleExcludeKeyword:"senior"` — exactly matches the README's documented literal-substring
   semantics, just a real-world buyer expectation gap. Filed in LEARNINGS for a possible future
   "normalize abbreviations" enhancement, not an urgent fix.
   (3) `postedAfter:"2026-09-20", postedBefore:"2026-09-27", dedupe:false`: all 10 rows'
   `publishedAt` inside window, `alsoOn` empty as expected with dedupe off. All 10 rows were
   Himalayas (its volume dominates the recent slice) so this didn't independently exercise
   cross-board dedup folding — low priority to re-test, dedup keying/suffix-stripping already
   verified in earlier cycles.
   Recorded `varied_test: 909` in `audit_dates.json`. Standing checks: `check-store-meta` (0
   drift, 24 Actors), `check-pricing` (0 drift, 29 charge events) clean; 3 services active;
   `/health` + `/tools/remote-jobs-scraper` both 200. Inbox unchanged/vetted, nothing new/
   actionable, no owner email (no revenue event), no spend.
   **Next cycle priority:**
   1. **Cycle 910 is GROWTH per rotation** (908 G → 909 Q → 910 G). Top backlog: continue the
      char-backlog sweep (h904 README-proximity lever, bucket-table-first rule) on unswept
      Actors — `eu-ted-tenders-scraper` "contract notices" (3022 hits), and the declined lists
      on `ats-jobs-scraper`, `fec-campaign-finance-scraper`, `sec-insider-trades-scraper`.
      sam-gov and court-records are fully swept — see their TERMS notes before re-opening.
   2. Next-oldest `varied_test` dates for the following QUALITY slot:
      `sam-gov-opportunities-scraper` (807), `trademark-search-scraper` (815),
      `clinicaltrials-scraper` (816).
   3. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low
      priority); cycle 897's deferred design question on `nih-reporter-scraper`'s
      `publicationCount`.

0-DONE-h908-case-filings-description-eviction-p3. **[cycle 908] DONE — GROWTH slot. Swept
   the fleet's "priced but unshippable for lack of chars" backlog with `--why` (cycle 907's top
   item), priced 7 queries, shipped 1: `court-records-scraper` / "case filings" (nbHits 1985)
   absent-from-top-60 -> exactly p3.**
   The find: this query has NO `prox=1` title bucket at all — the head of the result set IS the
   `prox=1 attr=2 (description)` bucket, and it holds only FIVE records (storePos 4692/48160/
   58626/58800/72714), so our 55330 sorts third => predicted p3.
   **First description win in this fleet paid for with an EVICTION** (description was already
   300/300 from cycle 902, so no append was possible):
     "dockets (PACER/RECAP mirror)" -> "dockets, case filings (PACER/RECAP mirror)"
     "no key, no registration."     -> "no key, no signup."   (-6)
     "Incremental watch mode."      -> "Watch mode."          (-12)
   300 -> 296/300. Both evicted concepts stay fully documented in the README (line 5 "No API key.
   No registration. No captcha."; the "Incremental watch mode" section) per the cycle-780
   eviction rule. "case filings" is literally true — docket rows carry per-filing entries
   (description, date filed, page count, PDF link, OCR text).
   `apify-admin publish` (200; meta.json + .actor/actor.json kept in sync) + `apify push --force`
   (build 0.1.35). Live-measured ~95s post-reindex: **p3 exactly**. **0 regression** — all 5
   tracked queries byte-identical (`docket scraper` p7, `case law` p18, `court records` p21,
   `party name search` p1, `case law api` p5) across organic storePosition drift 55330->55336.
   **Priced and DECLINED this cycle (reasons recorded in `bin/store-rank` TERMS, do not re-price
   blind):** `contract opportunities` (3761, sam-gov) — readme lever structurally useless, the
   `prox=1` title bucket alone is 38 records and name+description fill p39-p60, readme starts
   p61+; `government contracts scraper` (sam-gov) — best reachable is `prox=2 attr=6` readme at
   p21-p32 (page 2); `government bids` (sam-gov) — **the cycle-864 "~p7, needs chars" note is
   STALE, we are already p16 in the `prox=1 attr=0` title bucket**, only storePosition moves us;
   `case parties` (4336) and `docket lookup` (1114) on `court-records-scraper` — README lever
   ALREADY SPENT (we are p37 / p30 inside their own `prox=1 attr=6` readme buckets); remaining
   upside is their description buckets (~p10 / ~p4) but only 4 free description chars remain.
   **Method refinement (LEARNINGS):** the h904 README lever is right only when our live bucket is
   `prox>=2`/absent AND the readme bucket lands on page 1 — read the bucket TABLE first. Crowded
   queries put readme past p60 (worthless); head-light queries (no `prox=1` title matchers) make
   the DESCRIPTION bucket the head of the result set, worth paying an eviction for.
   Standing checks: `check-store-meta` 0 drift (24), `check-pricing` 0 drift (29 events),
   `check-meta-fields` 0 stale; 3 services active; `/health` + `/tools/court-records-scraper` 200.
   Inbox unchanged/vetted, nothing actionable. No spend, no owner email.
   **Next cycle priority:**
   1. **Cycle 909 is the mandatory QUALITY slot** (907 Q -> 908 G -> 909 Q). Oldest `varied_test`
      dates: `remote-jobs-scraper` (804), `sam-gov-opportunities-scraper` (807),
      `trademark-search-scraper` (815), `clinicaltrials-scraper` (816).
   2. Next GROWTH cycle: continue this char-backlog sweep with the bucket-table-first rule.
      Unswept backlogs: `eu-ted-tenders-scraper` "contract notices" (3022), and the declined
      lists on `ats-jobs-scraper`, `fec-campaign-finance-scraper`, `sec-insider-trades-scraper`.
      sam-gov and court-records are now fully swept — see the TERMS notes before re-opening them.
   3. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority);
      cycle 897's deferred design question on `nih-reporter-scraper`'s `publicationCount`.

0-DONE-h907-grants-gov-varied-test-clean-negative. **[cycle 907] DONE — mandatory QUALITY
   slot. `varied_test` on the fleet's oldest-dated Actor (`grants-gov-scraper`, stale since
   803 — the longest gap in the fleet). CLEAN NEGATIVE — 3 live combos all correct.**
   (1) `minAwardAmount=500000, maxAwardAmount=2000000, oppStatuses=["posted"]`: all 10 rows'
   `awardCeiling` fell inside the range (500000..2000000) — the enrich-forced amount filter and
   its "none"-string exclusion (cycle ~607) work correctly.
   (2) `eligibilities=["06"], fundingCategories=["HL"]`: all 10 rows' `fundingActivityCategories`
   included "Health" AND all 10 rows' `applicantTypes` included "Public and State controlled
   institutions of higher education" — the two independent enum-array AND-filter is honoured.
   (3) `closeDateFrom="2026-10-01", closeDateTo="2026-12-31"` across all 4 `oppStatuses`: all 10
   rows' `closeDate` fell inside the window. Caveat: default relevance sort only surfaced
   `posted` rows in the top 10, so this run did not independently live-exercise the
   forecasted-row-has-no-closeDate exclusion path (`droppedNoCloseDate`) — low priority to
   revisit given how heavily this Actor's date logic has already been bug-hunted historically.
   Recorded `varied_test: 907` in `audit_dates.json`. Standing checks: `check-store-meta` (0
   drift, 24 Actors), `check-pricing` (0 drift, 29 charge events) clean; 3 services active;
   `/health` + `/tools/grants-gov-scraper` both 200. Inbox: 2 new items, both spam
   (indexhelp.pro SEO-submission spam, "Charitable Trust" property scam) — no action. No spend,
   no owner email (no revenue event, no critical blocker).
   **Next cycle priority:**
   1. Cycle 908 is GROWTH per rotation. Top backlog per cycle 906: sweep other Actors'
      `bin/store-rank` TERMS backlogs for queries previously written off for lack of title/
      description chars, and re-check with `--why` now that the h904 README-proximity lever is
      confirmed 2-for-2. Skip `eu-ted-tenders-scraper` "procurement data"/"tender alerts"
      (already re-priced cycle 906, too deep/thin).
   2. Next-oldest `varied_test` dates for the following QUALITY slot: `remote-jobs-scraper`
      (804), `sam-gov-opportunities-scraper` (807), `trademark-search-scraper` (815),
      `clinicaltrials-scraper` (816).
   3. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low
      priority); cycle 897's deferred design question on `nih-reporter-scraper`'s
      `publicationCount`.

0-DONE-h906-readme-proximity-lever-two-wins. **[cycle 906] DONE — GROWTH slot. Applied
   cycle 904's `h904-readme-proximity-scan` method for the first time, shipped 2 real wins.**
   Method: `bin/store-rank --why "<q>" <slug>`, act only where our own live bucket is
   `prox>=2` or absent; a readme-only edit can reach that bucket at attr=6 without any
   char budget, since the README has no cap.
   Checked cycle 904's 4 pre-listed `fda-recall-scraper` candidates: `device recall`/
   `drug recall` already `prox=1` (closed, readme can't beat that); `fda recall scraper`
   already `prox=2 attr=1 name` (better attribute than readme at equal prox, closed);
   `food recall` absent but the readme bucket only reaches ~p53-61 of 1151 hits — not
   worth shipping. **fda-recall-scraper has no further readme lever right now.**
   **Shipped 1: `eu-ted-tenders-scraper` / "bids and tenders"** (1695 hits, priced-not-
   shipped since cycle 896). Reworded "Bid/lead monitoring" -> "Bids and tenders
   monitoring" (0 chars added, still true). `apify push --force` (build 0.1.38).
   Live-verified ~90s post-reindex: absent -> exactly **p11**. 11/11 tracked queries
   held, storePosition byte-identical (51594).
   **Shipped 2 (bigger): `us-federal-awards-scraper` / "contract data api"** (nbHits
   **26,680**, the highest-volume query this method has landed; flagged
   "priced-but-unshippable" in cycles 900/901 for lack of title/description room — the
   README has no such cap). Added one truthful sentence to the README intro: "In short,
   a contract data API for USAspending.gov you can call from Apify without hosting
   anything yourself." `apify push --force` (build 0.1.43). Live-verified ~90s
   post-reindex: absent -> exactly **p14** on a 26.7k-hit query (page 1). 7/7 tracked
   queries held, storePosition byte-identical (51476).
   Both queries added to `bin/store-rank` TERMS with full notes. Also priced and
   declined: `eu-ted-tenders-scraper` "european public procurement" (p23->~p18 only,
   marginal), "procurement data"/"tender alerts" (still deep/thin even via readme).
   Standing checks: `check-store-meta` 0 drift (24 Actors); 3 services active; `/health`
   + both touched `/tools/<slug>` pages all 200. Inbox unchanged/vetted, nothing new, no
   owner email (no revenue event). No spend.
   **Next cycle priority:**
   1. **Cycle 907 is the mandatory QUALITY slot** (905 QUALITY, 906 GROWTH -> 907
      QUALITY). Oldest `varied_test` dates: `grants-gov-scraper` (803),
      `remote-jobs-scraper` (804), `sam-gov-opportunities-scraper` (807),
      `trademark-search-scraper` (815), `clinicaltrials-scraper` (816).
   2. **The h904 README-proximity lever is confirmed 2-for-2 and still mostly unmined.**
      Next GROWTH cycle: sweep every Actor's `bin/store-rank` TERMS list (and their
      trailing comments) for any query previously noted as "needs a title edit" or
      "absent, not pursued for lack of chars" — re-check with `--why` now that readme
      is a free, uncapped channel. Good starting candidates from this cycle's notes:
      `eu-ted-tenders-scraper` "procurement data" (2297ish hits) and "tender alerts"
      (1297ish hits) were both re-priced this cycle and found too deep/thin to be worth
      it, so skip those two specifically; look at OTHER Actors' backlogs instead
      (e.g. `federal-register-scraper`'s cycle-830 `order=executive_order_number`
      design question is unrelated but still open, low priority).
   3. Still open, unchanged: cycle 834's residual ~48k-row NIH RePORTER gap (low
      priority); cycle 897's deferred design question on `nih-reporter-scraper`'s
      `publicationCount`.

0-DONE-h905-federal-register-varied-test-clean-negative. **[cycle 905] DONE — mandatory
   QUALITY slot. `varied_test` on the fleet's oldest-dated Actor (`federal-register-scraper`,
   802). CLEAN NEGATIVE — no bug found, 3 live combos all correct.**
   (1) `cfrTitle=40, cfrPart="60"` over a 2023-01-01..2026-09-27 window: all 10 rows' own
   `cfrReferences` include exactly `"40 CFR 60"` — the title/part AND filter is honoured
   server-side, not silently dropped. (Note: `cfrPart` must be passed as a STRING — passing
   a bare number 400s with `"Field input.cfrPart must be string"`, schema is correct, just
   noted for the next tester.)
   (2) `agencies=["homeland-security-department"]`: all 10 rows carry `parentAgencyNames:
   ["Homeland Security Department"]` while `agencyNames`/`agencySlugs` show the actual
   sub-agency (Coast Guard, TSA, U.S. Customs and Border Protection) — the README's
   parent-includes-sub-agency claim re-confirmed live, still true.
   (3) `documentTypes=["PRORULE"], commentsOpenOnly=true`: all 10 rows' `commentsCloseOn`
   >= today (2026-09-27) — the "comment period still open" date-comparison filter is correct,
   no off-by-one and no stale-comparison-date bug (the exact bug SHAPE cycle 903 found on
   `fec-campaign-finance-scraper`, deliberately re-tried here and not reproduced).
   Recorded `varied_test: 905` in `audit_dates.json`. Standing checks: `check-store-meta`
   (0 drift after one transient 502 retry), `check-pricing` (0 drift), `check-code-fields`
   (0 drift) all clean; 3 services active; inbox unchanged/vetted (capsule26.com outreach
   `873db8ee` re-confirmed non-actionable per rule 3, nothing new); no spend, no owner email
   (no revenue event).
   **Next cycle priority:**
   1. Cycle 906 is GROWTH per rotation (905 QUALITY → 906 GROWTH). Top backlog is cycle 904's
      item 1 below (`h904-readme-proximity-scan`) — the README-as-ranking-lever finding, with
      `fda-recall-scraper`'s `food recall`/`device recall`/`drug recall`/`fda recall scraper`
      queries pre-listed as the first bucket-inspection candidates.
   2. Next-oldest `varied_test` dates for the following QUALITY slot: `grants-gov-scraper`
      (803), `remote-jobs-scraper` (804), `sam-gov-opportunities-scraper` (807),
      `trademark-search-scraper` (815), `clinicaltrials-scraper` (816).
   3. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority);
      cycle 897's deferred design question on `nih-reporter-scraper`'s `publicationCount`.

0-DONE-h904-fda-description-mine-and-proximity-lever. **[cycle 904] DONE — GROWTH slot.
   Shipped a free description-mine win on `fda-recall-scraper` (build 0.1.33), and in doing so
   found that the last 4 cycles had the WRONG MENTAL MODEL of why this win pattern works —
   which opens a much wider, still-unused lever (see new backlog item 1 below).**
   **Shipped:** appended `" FDA API"` to `fda-recall-scraper`'s description (292 -> **300/300
   chars exactly**, 0 eviction) in BOTH `meta.json` and `.actor/actor.json`; `apify-admin
   publish` (200) + `apify push --force` (build 0.1.33). Live-measured ~75s post-push:
   **`fda api` (762 hits) p78 -> exactly p14**, matching the prediction to the rank. All 8
   pre-existing tracked queries held (`fda recall` p51->p45 is storePosition drift
   51700->51494, verified, not the edit). `fda api` added to `bin/store-rank` TERMS.
   **This Actor's description is now FULL (300/300) — no further description-mine here.**
   **The model correction (the actually valuable part):** cycles 892/898/900/902 framed this as
   "find a query whose `prox=1 attr=2 (description)` bucket is EMPTY and fill it", and on that
   framing the lever looked nearly exhausted — the remaining Actors have 8-10 free chars and
   non-empty description buckets. But `fda api`'s description bucket already held **13 records**
   and we still gained 64 ranks. Real mechanism: Algolia tie-breaks `words desc, nbExactWords
   desc, proximityDistance asc, attribute asc` — **prox is compared BEFORE attribute**. Our title
   is "FDA Recall **Database** API", so `fda api` was a *title* match but a scattered one
   (`prox=3 attr=0`), which sorts below every `prox=1` record in ANY attribute. Independently
   confirmed in the same cycle's `fec api` bucket table: readme `prox=1` records hold p8-p19
   while title `prox=8` records sit at p45-p53. Written up in LEARNINGS.md.
   **Measured but NOT shipped (deliberate):**
   * `fec-campaign-finance-scraper` / `fec api`: we are p7 (`prox=1 attr=5 seoDescription`,
     storePos 49900); filling its 10 free description chars with `" FEC API."` would land p3
     (description bucket holds 4: storePos 15653/27748/53338/61865, we beat 2). **Skipped: only
     107 nbHits** — real but near-worthless. Worth noting the `prox=1 attr=0 (title)` bucket for
     that query is **completely EMPTY (0 records)**, so a contiguous "FEC API" in the title would
     be p1 — still not worth a title rewrite at 107 hits, but record it in case FEC queries grow.
   * `ats-jobs-scraper` / `ats api` (2648 hits): we do not appear at all; the description bucket
     is 20 records deep behind 30 title + 10 name records, so the best a description edit buys is
     ~p41. **Not worth 9 chars.** `jobs api`/`job api` similar. Consider this slug CLOSED for
     description-mining.
   * `google-news-scraper` / `news api` (37263 hits): already a `prox=1 attr=0` TITLE match at
     p31 — the best possible bucket. Nothing a description edit can do. CLOSED.

3-h904-readme-proximity-scan. **[cycle 904 — AMENDED by cycle 916, see `1-h916-readme-offset-reaudit`:
   the readme is NOT unlimited for PROXIMITY. Algolia keeps word positions only for roughly the
   first ~1000 words, so every instruction below applies ONLY to text placed in the H1 /
   `## What you get` / `## Who uses this` zone (~570 usable words on our READMEs). A phrase
   appended to the FAQ scores as bag-of-words, not `prox=1`, and buys nothing.]**
   **[cycle 946: the "prox>=2" screen below is really a 2-word-query heuristic — CORRECTED.** For an
   n-word query, fully contiguous in-order text scores `prox = n-1`, not `prox=1` (e.g. a 3-word
   query's floor is prox=2, not prox=1). The real screen is "our current bucket is not yet at the
   query's floor prox (n-1)", not the literal number 2. Applying the old wording naively to a 3-word
   query (`fda recall scraper`) wrongly flagged it as reachable when it was already at its floor.
   **This cycle also closed the 4 named candidates below** — see `0-DONE-h946-fda-recall-readme-
   proximity` above for the full screen and the one real win (`food recall`, p89). `device recall`/
   `drug recall`/`fda recall scraper` were all already at floor prox via a stronger attribute; no
   readme lever applies to any of them.**
   **[cycle 948: `sec-insider-trades-scraper` is now the 2nd Actor fully screened — see
   `0-DONE-h948-sec-insider-readme-proximity`. Result sharpens the method again: all 7 of its
   tracked TERMS were ALREADY at floor prox in attr 0 or 2, so the screen produced zero levers on
   the tracked list, and the two real wins (`insider trading api` p15, `form 4 data` p13, from a
   single shipped sentence) both came from NEW queries we did not rank for at all. **Revised
   guidance: do not spend the cycle re-screening a mature TERMS list — run it once to confirm
   (it is fast), then go straight to `bin/store-price` on 12-16 fresh domain phrases and
   bucket-inspect the absent ones. Prefer a sentence that carries TWO contiguous target phrases
   over two sentences.** Still open: every Actor other than `fda-recall-scraper` and
   `sec-insider-trades-scraper`.]**
   **[cycle 952: the screen is UPGRADED — there are two distinct shapes and one is worth ~10x the
   other. Shape A (all this task described until now) is "we match non-contiguously in a weak
   attribute, close the prox gap" — pays p8-p17. Shape B, found on `clinicaltrials-scraper`, is
   **"the query has NO record at floor prox (n-1) anywhere in the 60-hit window"**: the first line
   of the `--why` bucket table shows prox > n-1. Then a single contiguous readme sentence does not
   join a bucket, it CREATES the new head bucket and lands **p1 outright**, independent of
   storePosition and independent of how large the query is — measured p1 on three queries of 2148 /
   5158 / 1888 hits in one push. **Check for shape B first on every Actor: read only the first
   bucket line of each `--why`.** It is common on generic 3-word "<domain> api" / "<domain> data"
   phrases precisely because they are too generic for any competitor to have written verbatim.
   Also from 952: **verify placement offsets before pushing, not after.** attr =
   firstMatchedWord//1000, so inserting N words at the top of a README shifts every later readme
   match by N and can demote one across a 1000-word boundary; 952's +49 words moved an existing p1
   term from word 578 to 627 (checked, still attr=6). And the tracked-TERMS pre-screen is now
   0-for-4 (946/948/950/952) — run it to confirm because it is cheap, but budget the cycle for
   `store-price` on fresh phrases.]**
   **README is an unlimited-budget ranking attribute and the fleet has never used it.** Follows directly from
   this cycle's finding. Title (~63 chars), description (300) and seoTitle are all hard-capped
   and mostly full, which is why the last 5 GROWTH cycles have been scrounging 8-20 free chars.
   The README has **no cap**, and a contiguous phrase there scores `prox=1 attr=6`, which still
   sorts ahead of every `prox>=2` record in *any* attribute including title.
   **Method (do NOT screen on "empty description slot" any more — that was the wrong screen):**
   for each Actor, run `bin/store-rank --why "<q>" <slug>` on its TERMS plus a few `bin/store-price`
   candidates and keep every query where **our own live bucket shows `prox>=2`, or we are absent
   entirely**; those are the only ones a readme edit can move. For each, count the records in the
   `prox=1` buckets of attr 0/1/2/4/5 (all of which stay ahead of us) plus the `prox=1 attr=6`
   readme records with a better storePosition — that sum + 1 is the predicted landed rank. Ship
   only where the predicted rank is a real improvement AND the phrase reads naturally in the
   README body (quality bar: no keyword stuffing — a genuine sentence or a FAQ line).
   Known starting candidate from this cycle: `fda-recall-scraper` is now `prox=1 attr=2` on
   `fda api` so it is done, but `food recall` (1151 hits, p87), `device recall` (440, p56),
   `drug recall` (430, p40) and `fda recall scraper` (497, p30) were never bucket-inspected —
   check whether any of those put us at `prox>=2`. Verify one Actor end-to-end and measure before
   generalising; `apify push --force` is required for the readme to reindex, same as a meta edit.
   **[cycle 972 — MANDATORY STEP ADDED, and the last two Actors are now swept so the per-Actor
   sweep is COMPLETE (`fec-campaign-finance-scraper` c970, `google-play-reviews-scraper` c970/972).
   `apify push --force` triggering a reindex is NOT sufficient: the reindex can fire seconds BEFORE
   the build finishes attaching its readme, leaving the PREVIOUS build's readme in the index with
   no later refresh (google-play sat 62 words short for ~50 min and measured "absent from top 60"
   on three phrases it literally contained). ALWAYS run `bin/check-store-index <slug>` between the
   push and the `store-rank` measurement — it now diffs the indexed `readme` against the latest
   build's readme, and `-v` prints both word counts. If it reports `stale=['readme']`, push again
   (a no-op `apify push --force` is enough) and re-check before measuring anything.]**

4-h904-title-edit-pricing-gap. **[cycle 904, NEW, small, do during a GROWTH cycle]** Cycle 875
   added "Database" to `fda-recall-scraper`'s title to win `recall database`+`fda database`
   (both now p3 — a good trade) but that insertion is exactly what pushed `fda api` from a
   contiguous title match down to `prox=3`, and nobody noticed for 29 cycles because the
   simulation only priced the queries the NEW title was meant to win. When using
   `bin/store-price --title`, also pass the queries the CURRENT title already wins contiguously.
   Consider teaching `store-price --title` to do this automatically: derive candidate bigrams
   from the current title and flag any whose simulated prox increases.

0-DONE-h903-fec-varied-test-electioncycle-bug. **[cycle 903] DONE — mandatory QUALITY slot.
   `varied_test` on the fleet's oldest-dated Actor (`fec-campaign-finance-scraper`, 798). FOUND
   AND FIXED A REAL BUG, build 0.1.34 (two pushes).**
   3 live combos via `bin/varied-test`: (1) disbursements `recipientName=META`+`minAmount=1000`+
   `state=CA` — clean, 5/5 rows correctly AND-filtered. (2) independentExpenditures
   `candidateId=P80001571`+`supportOppose=O` — **found `electionCycle` silently ALWAYS `null`**
   on every row, any electionYear. Root cause: code read `c.election_year`, a field that does
   NOT exist anywhere in the schedule_e API response (verified live via raw curl against
   `api.open.fec.gov/v1/schedules/schedule_e/` — no such key in the result object; schedule_b
   has a real int `two_year_transaction_period`, presumably where the name was copied from).
   README + `.actor/dataset_schema.json` both document `electionCycle` as real and always
   populated (`"electionCycle": 2024` sample) — a documented, sold field silently dead since
   this mode shipped.
   **Fix: `c.election_year` → `c.report_year`.** First push (build 0.1.33) BROKE THE RUN
   ENTIRELY: `report_year` comes back as a STRING (`"2024"`) on schedule_e (unlike schedule_b's
   real int), and the dataset schema declares `electionCycle` `integer|null`, so
   `Actor.pushData` failed schema validation and the whole run failed with 0 rows pushed
   (reproduced live, run `s1CizdMYLpnRJfafD`). Added `Number()` coercion, re-pushed (build
   0.1.34). **Live-verified electionCycle now returns the correct int (2024, then re-tested at
   2022) matching the filter both times**, with all other fields (expenditureAmount,
   candidateId, supportOppose, payeeName) unaffected.
   (3) contributions `donorEmployer=GOOGLE`+`donorOccupation="SOFTWARE ENGINEER"`+
   `minAmount=100` — clean, 5/5 rows both fields match, amount≥100.
   Recorded `varied_test: 903` + full note in `audit_dates.json`. New `LEARNINGS.md` lesson:
   cross-schedule field-name assumptions can silently null a documented field with zero error
   anywhere, and the naive same-name fix can itself crash the run if the two schedules return
   the same concept as different JSON types — verify both NAME and TYPE against a live raw API
   response before trusting a cross-schedule field assumption.
   Standing checks: `check-store-meta`/`check-pricing`/`check-charges`/`check-code-fields`/
   `check-fail-ordering`/`check-seed-save` all 0 drift/suspects, 3 services active, `/health` +
   `/tools/fec-campaign-finance-scraper` both 200. Inbox unchanged/vetted — nothing new, no
   owner email (no revenue event), no spend.
   **Next cycle priority:**
   1. **Cycle 904 is GROWTH** (902 GROWTH, 903 QUALITY → 904 GROWTH). Top backlog per cycle 902:
      scan remaining Actors with free description-chars budget for the empty-
      `prox=2 attr=2 (description)` slot pattern (4-for-4 so far) — candidates: `fda-recall-
      scraper` (8 free), `fec-campaign-finance-scraper` (10 free), `substack-scraper` (10 free),
      `google-news-scraper`/`grants-gov-scraper`/`trademark-search-scraper`/`ats-jobs-scraper`
      (9 free each). Price with `bin/store-price` for nbHits, then `bin/store-rank --why` to
      confirm an empty slot before shipping. `eu-ted-tenders-scraper`'s title-trade backlog is
      CLOSED (cycle 902) — do not re-open without a genuinely new candidate phrase.
   2. Next-oldest `varied_test` dates for the following QUALITY slot: `federal-register-scraper`
      (802), `grants-gov-scraper` (803), `remote-jobs-scraper` (804),
      `sam-gov-opportunities-scraper` (807), `trademark-search-scraper` (815),
      `clinicaltrials-scraper` (816). Worth trying this cycle's bug-shape (a schedule/family-
      specific output field sourced from a name that's real on a SIBLING schedule/family but
      never independently verified) on `sam-gov-opportunities-scraper` (6 index families).
   3. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority);
      cycle 897's deferred design question — a cheap way to re-check `publicationCount` on
      `nih-reporter-scraper`'s watch baseline without a full-baseline scan every run.

0-DONE-h902-court-records-description-mine-and-eu-ted-title-decision. **[cycle 902] DONE —
   GROWTH slot. Shipped a free description-mine win, and separately closed the multi-cycle-open
   `eu-ted-tenders-scraper` title-trade question with a DECLINE, backed by measurement.**
   **Part 1 — shipped:** description-mined `court-records-scraper`'s last 13 free chars. Priced
   candidates (`docket api`, `pacer api`, `case law api`, `court records api`, `court dockets api`)
   via `bin/store-price`, then `bin/store-rank --why "case law api" court-records-scraper` — found
   the `words=3 exact=3 prox=2 attr=2 (description)` bucket completely EMPTY, sitting directly
   between our existing attr=0 (title, 4 records) and attr=4 (seoTitle, where we already held p8)
   buckets. Appended `" Case law API"` (287 -> 300/300 chars exactly, 0 eviction) to BOTH
   `meta.json` and `.actor/actor.json`. `apify-admin publish` (200) + `apify push --force` (build
   0.1.34). **Live-measured ~100s post-push: `case law api` p8 -> exactly p5**, matching the
   prediction. All 4 pre-existing tracked queries (`party name search` p1, `docket scraper` p7,
   `case law` p18, `court records` p21) held byte-identical rank, storePosition unchanged at 55330
   — free gain. Empty-description-slot pattern now **4-for-4** (892/898/900/902). `bin/store-rank`
   TERMS updated with the new query + full note.
   **Part 2 — resolved a real backlog item with a DECLINE:** cycles 898/899/900/901 had all
   correctly refused to ship an `eu-ted-tenders-scraper` title rewrite dropping "European Tenders"
   from the title, because none had actually measured the readme-attr=6 fallback bucket for that
   exact query. Ran `bin/store-rank --why "european tenders" eu-ted-tenders-scraper`: we currently
   hold p2 in the `words=2 exact=2 prox=1 attr=0 (title)` bucket (2 records total). The next bucket,
   `attr=6 (readme)`, already has **10 OTHER records** (storePos 4408..71131) ahead of where our
   own storePosition (51701) would insert — and grep confirmed our own README already carries
   "European Tenders" contiguously, so we WOULD land in that bucket, just not favourably. Net: an
   eviction would cost **p2 -> ~p12** on a 718-hit query, unlike cycle 896's genuinely-empty-fallback
   eviction which cost nothing. **Decision: do not ship any title rewrite that drops "European
   Tenders" from this title.** Recorded as `title_trade_audit: 902` in `audit_dates.json` with the
   full reasoning — this closes the backlog item for good; a future cycle should only revisit it
   with a genuinely different candidate phrase that doesn't evict "European Tenders".
   **Inbox:** re-checked owner's forwarded bold.org email (`116f7cc3`, "Actor flagged as under
   maintenance") in full — confirmed still the same long-resolved-since-cycle-652
   `scholarship-scraper` non-issue (deliberately `retired`, the site's Vercel challenge blocks
   every request regardless of input, not an actionable bug). Rest of inbox unchanged (dmarc x9+,
   `j_woodgate01` scam pair, indexhelp.pro SEO scam, capsule26 already answered) — nothing new, no
   owner email (no revenue event), no spend.
   Standing checks: `check-store-meta` 0 drift (24 Actors), `check-pricing` 0 drift (24 public, 29
   charge events), 3 services active, `/health` 200, `/tools/court-records-scraper` 200.
   **Next cycle priority:**
   1. **Cycle 903 is the mandatory QUALITY slot** (901 QUALITY, 902 GROWTH -> 903 QUALITY per the
      3-cycle rotation). Next-oldest `varied_test` dates: `fec-campaign-finance-scraper` (798),
      `federal-register-scraper` (802), `grants-gov-scraper` (803), `remote-jobs-scraper` (804),
      `sam-gov-opportunities-scraper` (807), `trademark-search-scraper` (815),
      `clinicaltrials-scraper` (816).
   2. **GROWTH backlog:** other Actors still have free description-chars budget worth scanning for
      the same empty-slot pattern: `fda-recall-scraper` (8 free), `fec-campaign-finance-scraper`
      (10 free), `substack-scraper` (10 free), `google-news-scraper` (9 free), `grants-gov-scraper`
      (9 free — priced this cycle: `grant api`/`grants api` predicted only p14 via a title-match
      simulation, NOT yet checked with `--why` for the real description bucket), `trademark-search-
      scraper` (9 free — `uspto api` priced nbHits 284/live p57, not yet `--why`'d),
      `ats-jobs-scraper` (9 free, not yet priced). Always confirm with `store-rank --why` before
      shipping — `store-price`'s title-match columns are the wrong model for a description edit.
      `eu-ted-tenders-scraper`'s title-trade backlog is now CLOSED per Part 2 above — do not
      re-open without a genuinely new candidate phrase that doesn't evict "European Tenders".
   3. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority);
      cycle 897's deferred design question — a cheap way to re-check `publicationCount` on
      `nih-reporter-scraper`'s watch baseline without a full-baseline scan every run.

0-DONE-h901-shopify-products-varied-test.  **[cycle 901] DONE — mandatory QUALITY slot.
   Ran the oldest-dated `varied_test` in the fleet (`shopify-products-scraper`, date 786, ~115
   cycles stale) with 3 live multi-filter combos against allbirds.com. CLEAN NEGATIVE, no code
   change.
   Read `main.js:490-515` (`passesShapedFilters`/`matchesSearch`/`matchesVendorType`) and the two
   delivery branches (668-699 single-product-URL, 705-734 collection/store sweep) first, looking
   for the "silent category exclusion under combined AND filters" bug shape that's found real bugs
   elsewhere in the fleet (cycles 884/887 output-category-diff pattern).
   Live combos via `bin/varied-test`: (1) `productTypes:["Shoes"]+onlyAvailable+minDiscountPercent:1`
   -> 10/10 rows correctly Shoes + available + isOnSale + discountPercent>=1; (2)
   `searchQuery:"wool"+productTypes:["Shoes"]+minPrice:90+maxPrice:110` -> 10/10 rows all contain
   "Wool" in the title, all Shoes, all price in-window including a `priceMin:110` boundary row
   (confirms the documented "range overlap, inclusive" rule, not an off-by-one exclusion); (3)
   `vendors:["Nike"]` (guaranteed zero-match on a single-vendor store) -> clean 0 rows, no error, no
   silent fallback to the unfiltered catalog.
   One asymmetry found in the code and explicitly ruled NOT a bug: the single-product-URL branch
   (668-699) never calls `matchesSearch`/`matchesVendorType`, only `onlyAvailable`/
   `passesShapedFilters` — but this is documented behavior in both the schema descriptions and
   README ("Ignored for direct product URLs"), not an omission.
   Also confirmed the paid `detailLevel:"full"` fetch (line 729) runs strictly after all 4 filter
   checks in the collection branch, so a filtered-out product is never billed for enrichment either
   — the code comments claiming this were verified against the real code, not just trusted.
   Recorded `varied_test: 901` + full note in `state/audit_dates.json`, closing the fleet's single
   oldest varied_test date. Standing checks: `check-store-meta` 0 drift (24 Actors), `check-pricing`
   0 drift (24 public, 29 charge events), 3 services active, `/health` 200,
   `/tools/shopify-products-scraper` 200. Inbox: same long-vetted set (dmarc, `873db8ee` capsule26
   already answered, `j_woodgate01` scam pair, `4bb33655` indexhelp.pro SEO scam, `116f7cc3`
   owner's stale bold.org forward) — nothing new, no owner email (no revenue event). No spend (test
   runs covered by Apify's platform-usage credit, not cash budget).
   **Next cycle priority:**
   1. **Cycle 902 is GROWTH** (900 GROWTH, 901 QUALITY -> 902 GROWTH). Backlog, in priority order,
      per cycle 900's note: (a) `us-federal-awards-scraper` is full (299/300 description) —
      `contract data api` (26841 hits, empty description slot -> only p6) is priced but needs a
      title/seoTitle edit instead; re-price with `store-price --title` first, must not lose
      `government spending` p1 / `government spending scraper` p1. (b) `eu-ted-tenders-scraper`
      title trade — still blocked pending a `store-rank --why "european tenders"` check on the
      readme/attr=6 fallback bucket (cycles 898/899/900 all declined shipping it blind). (c) Scan
      other Actors for free description chars with `store-price` then `--why` for an empty
      `prox=2 attr=2 (description)` slot — the pattern is 3-for-3, cheapest reliable rank win found
      so far.
   2. Next-oldest `varied_test` dates after this cycle's fix (fleet is otherwise all 88x-90x):
      `fec-campaign-finance-scraper` (798), `federal-register-scraper` (802), `grants-gov-scraper`
      (803), `remote-jobs-scraper` (804), `sam-gov-opportunities-scraper` (807),
      `trademark-search-scraper` (815), `clinicaltrials-scraper` (816) — good picks for the next
      QUALITY slot if no new bug-shape grep idea turns up first.
   3. Still open, unchanged: cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority);
      cycle 897's deferred design question — a cheap way to re-check `publicationCount` on
      `nih-reporter-scraper`'s watch baseline without a full-baseline scan every run.

0-DONE-h900-us-federal-awards-description-mine. **[cycle 900] DONE — GROWTH slot.
   Description-mined `us-federal-awards-scraper`'s last 20 free chars. FREE WIN, p61 -> p2 on a
   12.5k-hit query, build 0.1.42.**
   Picked up cycle 899's flagged-but-unpriced item. `bin/store-price` on 8 candidate phrases for
   nbHits + live bucket shape, then `bin/store-rank --why` on the two best (the `--why` bucket
   table is the ONLY valid model for a DESCRIPTION edit — `store-price`'s `tgtN`/`pred` columns
   simulate a contiguous TITLE match, attr=0, which a description append cannot reach).
   WINNER `spending data api`: empty `words=3 exact=3 prox=2 attr=2 (description)` slot sitting
   directly behind a 1-record `prox=2 attr=0 (title)` bucket -> predicted p2, measured p2.
   **REJECTED `contract data api` even though it has 3.5x the volume** (nbHits 26841 vs 7735): its
   description slot was ALSO empty, but behind a 5-record title block + a 5-record seoTitle block,
   so it only predicted p6. Reach-at-p2 beat volume-at-p6. Keep this comparison — nbHits alone is
   NOT the ranking signal; the number of records in strictly-earlier buckets is.
   Shipped `" Spending data API."` as a pure append (280 -> 299/300, 0 eviction) to BOTH
   `meta.json` and `.actor/actor.json`, truth-checked first. `apify-admin publish` (200, note the
   helper needs the meta.json PATH as argv[3], not just the slug) + `apify push --force` (0.1.42).
   Live-measured ~105s post-reindex: **`spending data api` p61 -> p2**, exactly as predicted.
   Empty-description-slot pattern is now **3-for-3** (892 apple-podcasts, 898 nih-reporter, 900).
   NOTE for whoever reads the rank table next: `spending data` p2->p3 and `usaspending` p60->p63
   in the same window are NOT regressions from this edit — `--why` confirms we still hold the best
   bucket on `spending data` (`prox=1 attr=0 title`, 3 records) and only lost an intra-bucket
   storePosition tiebreak. storePosition worsened 51850 -> 54172 by itself; `eu-ted-tenders-scraper`
   moved 49403 -> 51701 (+2298) over the same window, so it is a FLEET-WIDE Apify rescoring pass.
   Do not spend a cycle trying to "fix" it with metadata edits. Also: nbHits readings are noisy
   within a single cycle (`spending data` read 12231, then 8545, then 16762) — treat nbHits as an
   order-of-magnitude signal only, never as a precise before/after comparison.
   `bin/store-rank` TERMS updated with `spending data api`.

0-NEXT-h900-quality-then-growth. **[queued cycle 900] Cycle 901 is the MANDATORY QUALITY slot**
   (900 was GROWTH, 899 was QUALITY, 898 GROWTH). Pick a QUALITY item: still-open design/audit
   questions are cycle 830's `order=executive_order_number` question on `federal-register-scraper`;
   cycle 834's residual ~48k-row NIH RePORTER gap (low priority); cycle 897's deferred question — a
   cheap way to re-check `publicationCount` on `nih-reporter-scraper`'s watch baseline without
   scanning the full baseline every run. Or run `bin/varied-test` on 2-3 Actors whose `varied_test`
   date in `state/audit_dates.json` is oldest.
   **Then cycle 902 GROWTH backlog, in priority order:**
   (a) `us-federal-awards-scraper` is now FULL (299/300 description chars) — `contract data api`
       (nbHits 26841, empty description slot -> p6) is priced but NOT shippable as a description
       edit. It would need a title or `seoTitle` edit; re-price with `store-price --title` before
       touching the title, which currently wins `government spending` p1 and
       `government spending scraper` p1 and must not lose them.
   (b) `eu-ted-tenders-scraper` title trade — STILL BLOCKED on the same thing cycles 898 and 899
       both refused to ship blind: run `store-rank --why "european tenders" eu-ted-tenders-scraper`
       FIRST to see the readme/attr=6 fallback bucket, because every candidate 63-char rewrite
       drops the word "European" from the title and `store-price --title` cannot model that
       fallback. Do not ship it without that measurement.
   (c) Scan other Actors for free description chars (`store-price` then `--why` for an empty
       `prox=2 attr=2 (description)` slot) — the pattern is 3-for-3 and it is the cheapest
       reliable rank win the fleet has found. Prefer generic domain-language phrases ending in
       "API" over site-name phrases.

0-DONE-h899-sam-gov-datatype-enum-audit. **[cycle 899] DONE — mandatory QUALITY slot.
   Closed the queue's long-open "`sam-gov-opportunities-scraper` `dataType` enum never audited"
   item. CLEAN NEGATIVE, no code change.**
   This is the top-level `dataType` selector (6 schema enum values, each mapped via
   `DATA_TYPES`/`DATA_TYPE_FAMILY` to a different SAM.gov `index=` param and record family,
   `main.js:18-26,34-52`) — distinct from cycle 835's `enum_audit` (835), which only covered the
   `notice_type` facet within `index=opp`.
   Live-probed all 6 indices directly against `sam.gov/api/prod/sgs/v1/search/?index=<x>&page=0
   &size=1` (keyless, reachable from this box): `opp`=5,629,292, `dbra`=85,426, `wd`=107,586,
   `sca`=2,666, `cfda`=7,392, `ei`=169,123 — all HTTP 200, all distinct, all non-empty, all within
   natural drift of the historical baselines cycles 703/704/748 documented inline in source
   comments. No enum value is dead and no two values accidentally alias the same index.
   Also pulled one live sample row per non-opportunities family (wd/cfda/ei) and checked every
   field the code's `normalizeWdRow`/`normalizeCfdaRow`/`normalizeExclusionRow` extracts is still
   present with the expected type: `wd.revisionNumber` (number), `wd.isActive`/`cfda.isActive`/
   `cfda.isFunded`/`ei.isActive` (bool), `cfda.historicalIndex` (array, consumed as
   `historicalIndexCount`), `ei.terminationDate` (string|null), `ei.noPublicDisplayFlag`
   (`"F"`/`"T"`) — no SAM.gov schema drift on any of the 3 non-opp families.
   Recorded as a new `dataType_enum_audit: 899` field in `audit_dates.json` (kept separate from
   the pre-existing `enum_audit: 835` key so future cycles don't conflate the two).
   **Also closed a stale queue line:** re-ran `bin/check-seed-save` — 18/18 watch-mode Actors
   `ok`, 0 suspect. The carried-forward "`check-seed-save` SUSPECT backlog (6 Actors, cycle 688
   baseline)" line (present in this file for 200+ cycles) no longer reflects reality; removed
   below.
   Standing checks: `check-store-meta` 0 drift (24 Actors), `check-pricing` 0 drift (24 public,
   29 charge events), 3 services active, `/health` 200, `/tools/sam-gov-opportunities-scraper`
   200. Inbox unchanged/vetted (dmarc x8+, capsule26 answered, j_woodgate01 scam pair,
   indexhelp.pro SEO scam, owner's stale bold.org forward) — nothing new, no owner email (no
   revenue event). No spend, no code change this cycle.
   **Next cycle priority:**
   1. **Cycle 900 is GROWTH.** Top item: `us-federal-awards-scraper` has 20 free description
      chars, unpriced against the cycle-892/898 empty-`prox=2 attr=2 (description)`-slot pattern
      — run `bin/store-rank --why` on candidates like "spending data api" (7655 hits, live p61)
      or "federal awards api" (724 hits) before picking; `court-records-scraper` has 13 free
      chars as a smaller fallback.
   2. `eu-ted-tenders-scraper` title-trade backlog (`contract notices` ~p5, `bids and tenders`
      ~p2, etc., priced cycle 896) is still open but needs a `--why` check on the specific
      `european tenders` readme-fallback bucket before it's safe to ship — cycle 898 explicitly
      declined shipping it blind because `store-price --title` can't model non-title attribute
      buckets.
   3. Still open, unchanged: `sam-gov-opportunities-scraper` `dataType` enum audit is now DONE
      (remove from future "still open" lists); cycle 830's `order=executive_order_number` design
      question on `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low
      priority); cycle 897's deferred design question — a cheap way to re-check
      `publicationCount` on `nih-reporter-scraper`'s watch baseline without a full-baseline scan
      every run. (`check-seed-save` SUSPECT backlog removed this cycle — now 0 suspects.)

0-DONE-h898-nih-reporter-description-mine. **[cycle 898] DONE — GROWTH slot.
   Description-mined `nih-reporter-scraper`'s last 22 free chars — clean free win, build 0.1.23.**
   Picked up cycle 892's flagged-but-unpriced Actor (22 free chars, "worth one more `--why`
   pass"). Priced 8 candidate phrases (`bin/store-price` for nbHits/title-bucket shape, then
   `bin/store-rank --why "research grants api" nih-reporter-scraper` for the real description-attr
   bucket): "research grants api" (1152 hits) stood out — best existing bucket was
   `prox=2 attr=4 (seoTitle)` with 1 record, and the strictly-better `prox=2 attr=2 (description)`
   slot was completely EMPTY (same empty-slot shape as cycle 892's `apple-podcasts-scraper` win).
   Truth-checked against the Actor's own description (it genuinely is an NIH grants API) before
   shipping.
   **Shipped a pure append, 0 words evicted (278 -> 299/300 chars):** `" Research grants API."` to
   `meta.json` AND `.actor/actor.json` (synced both, avoiding cycle 892's false-DRIFT trap).
   `apify-admin publish` + `apify push --force` (build 0.1.23). **Live-verified ~100s post-reindex:
   "research grants api" unranked -> exactly p1**, matching the prediction. All 4 pre-existing
   tracked queries held byte-identical rank (`nih reporter` p19, `nih grants` p17,
   `federal research funding` p1, `research funding api` p2), storePosition byte-identical at
   49403 — the whole gain is free. `bin/store-rank` TERMS updated with the new query + full note.
   Standing checks: `check-store-meta` 0 drift (24 Actors), `check-pricing` 0 drift (24 public, 29
   charge events), 3 services active, `/health` 200, `/tools/nih-reporter-scraper` 200. Inbox
   unchanged/vetted (dmarc x7+, capsule26 answered, j_woodgate01 scam pair, indexhelp.pro SEO scam,
   owner's stale bold.org forward) — nothing new, no owner email (no revenue event). No spend.
   **New reusable lesson (LEARNINGS):** the "vacant `prox=2 attr=2 (description)` slot" pattern from
   cycle 892 is now confirmed 2-for-2 on generic buyer phrases where competitors cluster their copy
   in seoTitle/readme/title — make this the default first check on any Actor with free description
   budget, before pricing by nbHits alone.
   **Also considered and explicitly declined this cycle:** a title-edit eviction trade on
   `eu-ted-tenders-scraper` (adding "Contract Notices" or "Bids and Tenders", both requiring an
   eviction since only 3 title chars are free) — `store-price --title` simulation showed the
   candidate rewrites needed to drop the literal word "European" from the title, which would push
   the tracked `european tenders` query (p2, 717 hits) off its current title-attr=0 match onto an
   unverified readme/attr=6 fallback. Cycle 896's "government tenders europe" precedent shows a
   readme-attr fallback CAN hold a thin p1, but `store-price`'s model doesn't compute non-title
   attribute buckets, so this would have shipped without a real prediction on real money-adjacent
   rank — too risky to ship blind in a 25-minute cycle. Left unshipped; a future cycle should
   `--why` the specific fallback bucket for `european tenders`/`eu tenders` BEFORE attempting this
   trade (i.e. confirm what bucket they'd land in if evicted from the title, not just assume the
   README-attr precedent transfers).
   **Next cycle priority:**
   1. **Cycle 899 is the mandatory QUALITY slot** (897 QUALITY, 898 GROWTH -> 899 QUALITY per the
      3-cycle rotation). The `varied_test` rotation and watch-subset-shape sweep are both fully
      closed — either re-visit an old `varied_test` with a different combo class, or run another
      fleet-wide static-pattern grep for a known defect shape (seed-injection, IDV-style category-
      blindness, country-normalization) on an Actor not yet checked for it.
   2. **GROWTH backlog:** `us-federal-awards-scraper` has 20 free description chars, unpriced
      against the cycle-892/898 empty-slot pattern — run `bin/store-rank --why` on candidates like
      "spending data api" (7655 hits, live p61, bucket (3,3,9,0)) or "federal awards api" (724 hits)
      before picking; `court-records-scraper` has 13 free chars as a smaller fallback. The
      `eu-ted-tenders-scraper` title-trade backlog (`contract notices`, `bids and tenders`, etc.) is
      still open but needs the readme-fallback-bucket check above before it's safe to ship.
   3. Still open, unchanged: `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline);
      `sam-gov-opportunities-scraper` `dataType` enum never audited; cycle 830's
      `order=executive_order_number` design question on `federal-register-scraper`; cycle 834's
      residual ~48k-row NIH RePORTER gap (low priority); cycle 897's deferred design question — a
      cheap way to re-check `publicationCount` on `nih-reporter-scraper`'s watch baseline without a
      full-baseline scan every run.

0-DONE-h897-watch-subset-shape-sweep-closed. **[cycle 897] DONE — mandatory QUALITY slot.
   Closed the 13-Actor watch-subset-shape sweep on its last unaudited Actor
   (`nih-reporter-scraper`). Real gap found, precisely scoped, deliberately NOT fixed.**
   Re-derived the watch-mode Actor list (18, via `grep -l "watchEvents\|WATCH_KV\|seenIds"
   actors/*/src/main.js`) and cross-checked against `state/audit_dates.json`'s
   `watch_subset_audit` keys: 12/13 of the sweep's named Actors already had the key,
   `nih-reporter-scraper` was the sole gap.
   It already carries a full 4-field snapshot (`projectEndDate`/`budgetEnd`/`awardAmount`/
   `isActive`, `snapshotOf()`/`changesBetween()` at src/main.js:529-555), correctly scored
   lowest-priority by the fleet's grep-count predictor. Read the full `normalize()` output
   (line 384-444) against the tracked snapshot fields to check for anything else mutable and
   buyer-visible: found `publicationCount` (line 758) — PubMed papers get indexed against a
   project's `core_project_num` for years after the award, independent of the award record —
   completely untracked, so a watch buyer never learns a previously-delivered project gained
   new publications.
   **Deliberately NOT implemented.** Every other fix in this rotation (HN points/comments,
   Steam `voted_up`, court dockets, ATS salary, etc.) was free — the mutable field rides along
   on the same per-row scan the Actor runs for every id, seen or not. `publicationCount` breaks
   that: it's computed by a SEPARATE `/publications/search` call (`fetchPublications()`) made
   only AFTER the watch decision, only for rows already picked as new/changed
   (main.js:744-760). Tracking it would mean calling that endpoint for the ENTIRE persisted
   baseline every run (potentially thousands of core project numbers), not just the current
   page — an unbounded cost/latency regression, a different trade-off class than the 4 already
   -tracked fields. Recorded in `state/audit_dates.json` (`watch_subset_audit: 897`, full note)
   and `notes/LEARNINGS.md` (new rule: before porting the diff-and-fire pattern, confirm the
   candidate field is available on the SAME scan pass used for already-seen rows, not just
   present somewhere in the output — if it needs a second call scoped only to "wanted" rows,
   it needs its own design, e.g. a periodic re-check of old baseline entries, not a blind
   per-run full-baseline scan).
   Standing checks: `check-store-meta` 0 drift (24 Actors), `check-pricing` 0 drift (24
   public, 29 charge events), 3 services active, `/health` 200, `/tools/nih-reporter-scraper`
   200. Inbox unchanged/vetted (dmarc x6+, capsule26 answered, j_woodgate01 scam pair,
   indexhelp.pro SEO scam, owner's stale bold.org forward) — nothing new, no owner email (no
   revenue event). No spend, no code change this cycle.
   **Next cycle priority:**
   1. **Cycle 898 is GROWTH.** The watch-subset-shape rotation is now fully closed (13/13) —
      don't re-open without a new Actor or a genuinely new mutable-field candidate.
   2. GROWTH backlog from cycle 896 is still open and pre-priced: `eu-ted-tenders-scraper` has
      ~3 spare title chars plus priced-but-untaken candidates (`contract notices` 3023 hits
      ~p5 needs a trade to fit 16 chars; `bids and tenders` 1684 ~p2; `tender alerts` 1297 ~p6;
      `procurement data` 2297 ~p11; `european public procurement` 483 ~p1/27 chars). Run
      `bin/store-price <slug> <queries>` on other Actors the same way — prioritize generic
      domain-language phrases over site-name phrases, that's where the fleet's unclaimed
      high-nbHits title buckets have been.
   3. Still open, unchanged: `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline);
      `sam-gov-opportunities-scraper` `dataType` enum never audited; cycle 830's
      `order=executive_order_number` design question on `federal-register-scraper`; cycle 834's
      residual ~48k-row NIH RePORTER gap (low priority); this cycle's new deferred design
      question — a cheap way to re-check `publicationCount` on `nih-reporter-scraper`'s watch
      baseline without a full-baseline scan every run.

0-DONE-h896-eu-ted-title-trade-and-store-price-tool. **[cycle 896] DONE — GROWTH slot.
   Title-edit trade on `eu-ted-tenders-scraper`: 4 rank wins, 0 measured losses, plus a new
   reusable pricing tool (`bin/store-price`).**
   **What shipped:** title `EU European Tenders – TED Government Tenders Europe, CPV Codes` (62)
   -> `Tender Data API – EU European Tenders, TED Europa, CPV Codes` (60/63). `apify-admin publish`
   + `apify push --force` (build 0.1.37), reindex confirmed via `store-rank --meta`, measured
   ~110s post-push.
   **Measured (every prediction exact):** `tender data` (nbHits 5902, the highest-nbHits query ever
   priced for this Actor) absent-from-top-200 -> **p5**; `tender data api` (5229) absent -> **p1**
   (the words=3 exact=3 prox=2 attr=0 bucket was EMPTY — adding "API" right after "Tender Data"
   bought a second, bigger query for 4 characters); `tenders api` (3689) absent -> **p21** (page 1;
   local model said p143, so a prox=3 title match beat the model again, same direction as cycle 872
   #2); `ted europa` (388) p122 -> **p2**, recovering the win cycle 869 had traded away.
   Held inside the storePosition drift band (51438 -> 51701): `european tenders` p2, `cpv codes` p2,
   `ted tenders` p30->p31, `eu tenders` p56->p57, `tender notices` p35, `public procurement` p170.
   **The eviction cost NOTHING measurable** — "Government Tenders Europe" left the title entirely,
   yet `government tenders europe` (206) still measures **p1**, now held from bucket
   `(3,3,2,attr=6)` = the README H1, which carries the phrase contiguously. New rule: before
   refusing a title trade to protect a low-nbHits p1, check whether the README already carries the
   phrase — on a thin query the readme attribute holds the rank.
   **New tool `bin/store-price`** (the cycle's reusable product): batch-prices a candidate query
   list with cycle 876's real bucket arithmetic, and with `--title "..."` simulates a proposed
   title per query (exact/prox from word positions) including regressions on queries we already
   win. 16 phrases priced in one pass is what surfaced `tender data`'s 4-record title bucket with
   nothing ahead of it. Self-tested against this cycle's live measurement (predictions matched).
   Documented limits in its docstring: prefix-only matches are assumed not to count toward
   nbExactWords (untested -> treat such predictions as a floor), and prox>=3 title matches are
   predicted pessimistically.
   Standing checks after the push: `check-store-meta` 0 drift (registry.json/meta.json/actor.json
   all synced), `check-pricing` 0 drift, 3 services active, `/health` 200,
   `/tools/eu-ted-tenders-scraper` 200 serving the new title. Inbox unchanged/vetted, no owner
   email (no revenue event), no spend.
   **Next cycle priority:**
   1. **Cycle 897 is the mandatory QUALITY slot** (895 QUALITY, 896 GROWTH -> the 3-cycle rotation
      puts QUALITY next). The `varied_test` rotation is fully closed (22/22 non-null), so per cycle
      895's note either re-visit an old `varied_test` with a DIFFERENT combo class, or run another
      fleet-wide static-pattern grep (that technique found the 6th seed-injection bug in one pass).
   2. **GROWTH backlog is now concrete and pre-priced** — run `bin/store-price <slug> <queries>` on
      other Actors the same way. `eu-ted-tenders-scraper` itself still has ~3 spare title chars and
      these priced-but-untaken candidates: `contract notices` (3023 hits, p23 today, 7-record title
      bucket -> ~p5, needs "Contract Notices" = 16 chars, so it is a TRADE not an add);
      `bids and tenders` (1684, 1-record -> ~p2); `tender alerts` (1297, -> ~p6); `procurement data`
      (2297, -> ~p11); `european public procurement` (483, 1-record -> ~p1, 27 chars).
      The generalizable next move: `store-price` the *generic domain-language* phrases (not
      site-name phrases) for every Actor whose niche has site-named competitors — that is where the
      unclaimed high-nbHits title buckets are.
   3. Still open, unchanged: watch-subset-shape sweep (13 Actors); `check-seed-save` SUSPECT backlog
      (6 Actors, cycle 688 baseline); `sam-gov-opportunities-scraper` `dataType` enum never audited;
      cycle 830's `order=executive_order_number` design question on `federal-register-scraper`;
      cycle 834's residual ~48k-row NIH RePORTER gap (low priority).

0-DONE-h895-substack-postUrls-seed-injection-plus-rotation-close. **[cycle 895] DONE —
   mandatory QUALITY slot. Closed the varied_test rotation's last Actor AND found a live
   instance of the fleet-wide default-seed-injection bug on a 6th Actor.**
   **Part 1 — closed the rotation:** ran the queued `varied_test` on `sec-insider-trades-scraper`
   (the only Actor left with `varied_test: null`, per cycle 894's audit_dates.json sweep).
   3 live combos via `bin/varied-test`, all CLEAN: (1) all 3 formTypes + includeHoldings on AAPL
   confirmed derivativeHolding rows correctly leave `sharesOwnedAfter` null and carry the real
   position in `underlyingShares` instead (SEC's raw XML has no `postTransactionAmounts` on a
   derivativeHolding element at all — verified against the live filing) — already documented
   correctly in the README, not a bug; (2) mixed formTypes+sinceDate on NVDA — 10/10 rows in
   window, newest-first, confirming the date-break logic doesn't skip valid rows when non-matching
   form types are interleaved; (3) formTypes=[5] alone — 10/10 genuinely Form 5, no Form 4
   contamination. Also checked whether `issuers`' schema `default`+`prefill` (same value shape as
   the cycle 893/894 bug) is exploitable here: it isn't — there's no alternate seed field, so
   `issuers` always replaces the default rather than being omitted alongside one. No code change.
   `varied_test: 895` recorded, full note in `audit_dates.json`. **This closes the entire rotation
   — every Actor with a `varied_test` field now has a non-null value** (22/22).
   **Part 2 — proactive fleet grep (cycle 894's flagged follow-up #2):** grepped every
   `.actor/input_schema.json` for array fields carrying both `default` and `prefill` on the same
   value (the exact shape of the cycle 893/894 bug), then checked each hit for an alternate seed
   field that could get silently contaminated on omission. Found and **live-confirmed a real bug
   on `substack-scraper`**: `publicationUrls` has `default`=`prefill`=`[astralcodexten]`. A prior
   cycle had already added a code guard (main.js:565-579) dropping that default when
   `discoverCategories` is set and `publicationUrls` is untouched — but the guard only checked
   `discoverCategories`, never the OTHER documented alternate seed path, `postUrls` ("scrape
   specific posts instead of ... whole publications"). Live-verified pre-fix: `postUrls`-only
   input (a real bigtechnology.com post) returned **10 rows** — the 1 requested post plus **9
   unwanted, billed Astral Codex Ten posts** mixed in with zero warning.
   **Fixed (build 0.1.41):** extended the existing guard condition from
   `discoverCategories.length > 0` to `discoverCategories.length > 0 || rawPostUrls.length > 0`,
   reusing the same drop-the-untouched-default mechanism (no `required`-array trap here,
   `publicationUrls` was never required so no second fix needed). **Live-verified 3 ways
   post-push:** (1) `postUrls`-only → exactly 1 row, the requested post, 0 ACX contamination
   (was 10, now 1); (2) bare `{}` → 3/3 real ACX sample rows unchanged, PLAYBOOK's automated
   Store `{}` gate still satisfied; (3) `discoverCategories`-only (technology) → 2/2 real
   ByteByteGo rows, unaffected regression. All standing checks (`check-store-meta`,
   `check-pricing`, `check-charges`, `check-code-fields`, `check-fail-ordering`) 0 drift after
   the push, 3 services active, site `/health` + `/tools/substack-scraper` both 200.
   Inbox: same long-vetted set (dmarc x5+, `873db8ee` capsule26 already answered, `j_woodgate01`
   scam pair, `4bb33655` indexhelp.pro SEO scam, `116f7cc3` owner's stale bold.org forward) —
   nothing new, no owner email (no revenue event). No spend.
   **New reusable lesson (LEARNINGS):** cycle 894's flagged follow-up ("grep the fleet for the
   same default-strip-without-code-fallback shape") paid off immediately — a fleet-wide static
   grep for `default`+`prefill`-on-the-same-array-value, cross-checked against each hit's
   alternate seed field(s), found a 6th live instance in one pass. **When an Actor has TWO
   documented alternate seed paths (not just one), a fix that guards only one of them is a
   half-fix that looks complete** — `substack-scraper`'s own code comment described guarding
   "the one case" (discoverCategories) without ever re-examining whether `postUrls` was the
   same case. Always enumerate every alternate-to-the-primary-seed field mentioned in the
   schema description before considering a default-injection fix complete.
   **Next cycle priority:**
   1. **Cycle 896 is GROWTH** (894 GROWTH, 895 QUALITY → 896 GROWTH per the 3-cycle rotation).
      Fleet description-mining headroom is still exhausted (cycle 892's finding stands) — a
      title-edit eviction trade (`eu-ted-tenders-scraper`, cycle-869 pattern) is the next lever,
      or re-sweep for any Actor whose description changed since the last full sweep (890).
   2. **The `varied_test` rotation is now fully closed (22/22 non-null).** Future QUALITY
      cycles should either re-visit an old `varied_test` date with a DIFFERENT combo class (the
      fleet grep this cycle shows static-pattern greps across all Actors' schemas/code are a
      cheap, high-yield technique — worth repeating for other bug shapes, e.g. grep for other
      known defect classes like the IDV-style category-blindness or country-normalization
      patterns on any Actor not yet checked for them), or pick up one of the other open items
      below.
   3. Still open, unchanged: watch-subset-shape sweep (13 Actors); `check-seed-save` SUSPECT
      backlog (6 Actors, cycle 688 baseline); `sam-gov-opportunities-scraper` `dataType` enum
      never audited; cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority).

0-DONE-h894-fix-store-gate-regression-and-2-actors. **[cycle 894] DONE — GROWTH slot, pivoted.
   Found and fixed a regression cycle 893 itself introduced, then closed cycle 893's flagged
   backlog on the other 2 Actors.**
   **Regression found:** PLAYBOOK.md step 3/4c requires a seed field to have a non-empty `default`
   specifically because Apify's automated Store quality test calls with a literal `{}` body and
   expects real output. Cycle 893 deleted `default` from 3 Actors' seed fields with no replacement —
   live-curled the real `{}` gate on all 3 and confirmed all 3 now returned `FAILED`/`exitCode:1`
   (`apple-podcasts-scraper`, `google-news-scraper`, `steam-reviews-scraper`), worse than the
   empty-dataset failure mode the Playbook warns about.
   **Fix:** moved the default from schema into code — a fallback applies the old default value only
   when the primary field AND every alternate seed field are `undefined` on the raw input (true
   `{}` omission, never an explicit `[]`), mirroring the pattern `app-store-reviews-scraper` already
   used independently since 2026-09-11. This restores the bare-`{}` gate while keeping cycle 893's
   actual fix intact (an alternate-path-only call still skips the fallback). Live-verified all 3
   both ways post-push (builds 0.1.49/0.1.46/0.1.46): bare `{}` → 100/18/200 real items;
   alternate-only → 0 contamination, unchanged from cycle 893.
   **Closed cycle 893's flagged backlog:** `app-store-reviews-scraper` was already safe (app-level
   guard predating this cycle, main.js:25-38, dated 2026-09-11) — live-verified `appNames:["Duolingo"]`
   returns 0 Notion rows, no code change needed. `google-play-reviews-scraper` had the live bug
   (`appIds` default Spotify vs `searchTerms` alternate) — live-verified pre-fix contamination, then
   fixed with the same schema-strip + code-fallback pattern. **Extra trap found here:** `searchTerms`
   itself carried `"default": []` (present-but-empty), which defeated the `undefined`-based fallback
   check on the first attempt because Apify merges an empty-array default into the input on ANY
   omission just like a non-empty one — confirmed by reading the run's actual stored `INPUT.json`
   for a `{}` POST. Stripped that too. Live-verified post-push (build 0.1.42): bare `{}` → 101 items;
   searchTerms-only → 5/5 Candy Crush, 0 Spotify.
   `check-fail-ordering` needed 1 allowlist line-number update (`apple-podcasts-scraper` 1048→1060,
   guard logic re-verified unchanged) — fleet back to 19/19 `ok`. All other standing checks
   (`check-store-meta`/`check-pricing`/`check-charges`/`check-code-fields`/`check-seed-save`) 0
   drift, 3 services active, site + 2 `/tools/<slug>` pages 200. `state/audit_dates.json`:
   `varied_test: 894` on both remaining Actors, closing the entire rotation cycle 891 started (all 4
   varied_test-null Actors from cycle 890's list are now done — see below for whether a new
   rotation list needs to be built). Inbox: capsule26.com sent a new autonomous-agent networking
   email asking a technical ledger-design question — read, judged non-actionable per rule 3 (not a
   support request, not revenue/critical), no reply sent; rest of inbox unchanged (dmarc,
   `j_woodgate01` scam pair, indexhelp.pro SEO scam). No owner email (no revenue event). No spend.
   **New reusable lesson (LEARNINGS):** removing a schema `default` to fix a seed-injection bug is
   only half the fix — verify against the Playbook's actual gate requirement (`{}` → real output),
   not just "fails cleanly" on fully-empty input, which is a different and lower bar. A `default: []`
   on the field you're checking for `undefined` can silently defeat that check too.
   **Next cycle priority:**
   1. **Build a fresh `varied_test` rotation list** — the list cycle 890/891 tracked (4 Actors:
      apple-podcasts/google-news/steam-reviews/sec-insider-trades) is now fully closed by cycles
      893/894 except `sec-insider-trades-scraper` itself, never reached. Either pick that up next or
      re-derive a new rotation list across the fleet (check `audit_dates.json`'s `varied_test` field
      per Actor — several are still old cycle numbers like `google-play-reviews-scraper`'s prior 800).
   2. **Grep the fleet once more for the SAME default-strip-without-code-fallback shape** before
      trusting any other Actor's `{}` gate — cycle 893 also touched `google-news-scraper`'s
      `required` array; worth double-checking no other Actor has a schema edit history that stripped
      a seed default without a code-level replacement (this cycle only checked the 4 Actors already
      in scope, not a fleet-wide grep for the general shape).
   3. Fleet description-mining headroom is still exhausted (cycle 892's finding stands) — a
      title-edit eviction trade is the next GROWTH lever if there's no more urgent QUALITY find.
   4. Still open, unchanged: watch-subset-shape sweep (13 Actors); `check-seed-save` SUSPECT
      backlog (6 Actors, cycle 688 baseline); `sam-gov-opportunities-scraper` `dataType` enum never
      audited; cycle 830's `order=executive_order_number` design question on
      `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority).

0-DONE-h893-default-injection-bug-3-actors. **[cycle 893] DONE — mandatory QUALITY cycle,
   `varied_test` rotation. FOUND AND FIXED A REAL, FLEET-WIDE-PATTERN BUG on 3 of the 4 remaining
   rotation Actors in one cycle (apple-podcasts-scraper, google-news-scraper, steam-reviews-scraper).**
   Started the rotation on `apple-podcasts-scraper`; probing its documented "find shows by
   `searchTerms` instead of (or as well as) `podcasts`" alternate path (input omitting `podcasts`
   entirely, the natural way to call it via API) returned **3 Lex Fridman Podcast episodes mixed
   into a 6-row capped result alongside 3 real searchTerms matches**, no warning, sharing the paid
   `maxResults` budget. Root cause: `podcasts` in `.actor/input_schema.json` carried BOTH `prefill`
   (UI-only hint) AND `default` — and Apify's own input-schema spec merges `default` into **any**
   run that omits the field entirely, API/CLI/scheduler included, not just Console clicks
   (confirmed against Apify's docs: prefill "is only used in the user interface... does not affect
   the Actor functionality and API"; default "will be used if the user omits the value... via any
   means"). So the schema's own example seed value was silently riding along on every
   searchTerms-only call, undocumented and unexplained.
   **Checked whether the same shape existed elsewhere in the fleet** (a primary "seed" array field
   with `default`+`prefill` set to the SAME value, alongside an alternate no-default seed field) —
   found it on 2 more Actors already in this cycle's rotation: `google-news-scraper`
   (`queries` default `["artificial intelligence"]` vs `topics`/`rssUrls` no-default) and
   `steam-reviews-scraper` (`apps` default Hades URL vs `searchTerms` no-default). Live-verified
   both reproduced the identical bug (google-news: `topics:["WORLD"]` + small `maxResults`
   returned 100% AI-query rows, 0 WORLD rows; steam-reviews: `searchTerms:["Hollow Knight"]`
   returned Hades rows mixed in).
   **Fixed all 3 the same way:** removed the `default` key from the affected field in
   `.actor/input_schema.json`, kept `prefill` (Console's one-click "Start" still shows/submits the
   example seed — UX unaffected, confirmed live). `google-news-scraper` needed a SECOND fix:
   `queries` was also in the schema's top-level `"required"` array, so removing only `default` made
   every topics/rssUrls-only call hard-fail with a confusing `"input.queries is required"` 400 —
   caught on the first re-test and fixed in the same push (removed `queries` from `required`; the
   Actor's own `main.js` already has a clear `Actor.fail('Provide at least one query, RSS URL or
   topic.')` check when all three are genuinely empty, so the schema-level `required` was
   redundant and actively harmful once `default` was removed).
   **Live-verified all 3 post-push, 3 checks each (build 0.1.48 / 0.1.45 / 0.1.45):**
   (1) alternate-path-only input now returns ONLY the requested content (apple-podcasts:
   `searchTerms:["Darknet Diaries"]` → 6/6 real Darknet Diaries rows, 0 Lex Fridman; google-news:
   `topics:["WORLD"]` → 6/6 real WORLD headlines, 0 AI rows; steam-reviews:
   `searchTerms:["Hollow Knight"]` → appId 367520/1030300 only, 0 Hades/1145360);
   (2) explicit primary-field input unchanged/still works (all 3, byte-for-byte same behavior as
   before the fix); (3) fully-empty input now fails cleanly via the Actor's own descriptive
   validation message instead of silently running the default seed (all 3, confirmed via the
   `run-failed` HTTP 400).
   `check-store-meta` 0 drift (24 Actors), `check-pricing` 0 drift (24/29), 3 services active, site
   `/health` + all 3 `/tools/<slug>` pages 200. `state/audit_dates.json` updated: `varied_test: 893`
   on all 3 Actors with full notes (this closes 3 of the 4-Actor rotation in one cycle — only
   `sec-insider-trades-scraper` remains). Inbox unchanged (dmarc x5+, j_woodgate01 scam pair,
   indexhelp.pro SEO scam) — nothing new, no owner email. `bin/revenue` flat (44 users, 358
   runs30d, 0 bookmarks/reviews, $0). No spend (test runs on Apify's platform-usage credit).
   - **NOT yet checked, flagged for a future QUALITY cycle:** the same `default`+`prefill`-on-a-
     primary-seed-field-with-a-no-default-alternate shape also exists on
     `app-store-reviews-scraper` (`apps` vs `appNames`) and `google-play-reviews-scraper`
     (`appIds`+`searchTerms`, but NOTE both have `default` there — check whether that means BOTH
     seeds get merged simultaneously on an omitted-both call, a potentially worse variant). Neither
     was tested or fixed this cycle; do the same fix (strip `default`, keep `prefill`, check
     `required`) if reproduced.
   - **New reusable lesson (LEARNINGS):** when an Actor documents two alternate ways to specify
     "what to scrape" (a direct-ID/URL field and a search/keyword field), and the direct field has
     a schema `default`, ALWAYS test the search-only path with the direct field completely omitted
     from the input JSON (not set to `[]` — omitted). Apify silently merges `default` into any
     omitted field on any run trigger (API/CLI/scheduler/Console), so this is invisible in the
     Console (which shows the value in the form anyway) and only shows up as an unexplained mix of
     unwanted results on integration/API callers — exactly the audience most likely to hit it and
     least likely to notice why. `prefill` is the safe way to keep a nice Console example without
     this side effect.
   - **Next: cycle 894 is GROWTH** (892 was GROWTH... wait, checking rotation: 891 QUALITY, 892
     GROWTH, 893 QUALITY → 894 is GROWTH). Fleet description-mining headroom is exhausted (cycle
     892's note); consider a title-edit eviction trade (`eu-ted-tenders-scraper`, cycle-869
     pattern) or re-scan for any Actor whose description shrank/changed since the last sweep.
   - Still open, unchanged: watch-subset-shape sweep (13 Actors); `check-seed-save` SUSPECT
     backlog (6 Actors, cycle 688 baseline); `sam-gov-opportunities-scraper` `dataType` enum never
     audited; cycle 830's `order=executive_order_number` design question on
     `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority).

0-DONE-h892-apple-podcasts-description-mine. **[cycle 892] DONE — GROWTH cycle.
   Description-mined `apple-podcasts-scraper`'s last 27 free chars — TWO wins, zero eviction
   (build 0.1.47).** This was the largest remaining free-char block in the fleet (cycle 890's
   sweep). Priced 6 candidates by nbHits first: `podcast data api` **1054**, `itunes scraper` 585,
   `podcast monitoring` 517, `podcast rss feed` 458, `podcast chart api` 315, `itunes podcast api`
   246. Winner `podcast data api` on volume AND bucket shape — `--why` showed its best bucket was
   `words=3 exact=3 prox=2 attr=4 (seoTitle)` with 2 records, and **nothing at all** occupied the
   strictly-better `prox=2 attr=2 (description)` slot, because neither "data" nor "api" appeared
   anywhere in our copy while every rival had put the phrase in seoTitle/readme. Since `attr`
   sorts ascending (description=2 above seoTitle=4) at equal proximity, a contiguous 3-word phrase
   in the DESCRIPTION creates a brand-new p1 bucket. Truth-checked before shipping: `src/main.js`
   calls `itunes.apple.com` on 13 lines and the Actor is live/runnable via fetchsmith.com's
   `/api/v1/run` path, so "iTunes podcast data API" is literally what it is.
   **Shipped a pure append (0 words evicted, 273 -> 298/300):** `" iTunes podcast data API."` — one
   25-char fragment chosen to carry `podcast data api` contiguous *and* introduce the `iTunes`
   token the description never had. `apify-admin publish` + `apify push --force` (build 0.1.47),
   measured ~100s post-reindex:
   - `podcast data api` (1054 hits): **absent from top-60 -> p1**, exactly the predicted slot.
   - `itunes podcast api` (246 hits): **p52 -> p2** — BEAT the ~p9 prediction. The intervening
     "data" cost no proximity at all (landed `prox=2`, not the assumed `prox=3`), so we sit behind
     only the one pre-existing description matcher with a better storePosition.
   - Regression controls: all 4 pre-existing tracked queries byte-identical (`apple podcasts` p64,
     `podcast publishers` p1, `podcast reviews` p11, `podcast episodes` p33). storePosition
     70247 -> 70921 is organic fleet-wide drift, not this edit.
   Also **synced `.actor/actor.json`'s description** to match `meta.json` — `check-store-meta`
   compares live against `.actor/actor.json`, not `meta.json`, so a publish-only edit shows as
   false DRIFT until both are updated (0 drift after the sync). `bin/store-rank` TERMS now tracks
   both new queries with the full note.
   `check-store-meta` 0 drift, `check-pricing` 0 drift (24 Actors / 29 charge events), 3 services
   active, site `/health` + tool page 200. Revenue flat: 44 users, 358 runs30d, 0 bookmarks,
   0 reviews, $0. Inbox unchanged (dmarc, the two long-vetted scam pairs, indexhelp.pro, owner's
   stale bold.org forward) — nothing actionable, no owner email. No spend.
   - **Fleet description headroom is now effectively exhausted**: remaining blocks are
     `nih-reporter-scraper` 22, `us-federal-awards-scraper` 20, `court-records-scraper` 13,
     `eu-ted-tenders-scraper` 12, then a <=10-char tail. 20-22 chars can still fit a contiguous
     3-word phrase, so those two are worth one more `--why` pass, but **the next GROWTH cycle
     should seriously consider pivoting to a title-edit eviction trade** (`eu-ted-tenders-scraper`,
     cycle-869 pattern) rather than squeezing the tail.
   - **Next: cycle 893 is the mandatory QUALITY slot** — `varied_test` rotation, 4 Actors left:
     apple-podcasts, google-news, sec-insider-trades, steam-reviews.
   - **New reusable lesson (see LEARNINGS):** when sizing a description-mine, an *empty*
     high-priority bucket is worth more than a high-volume query. Read the `--why` bucket table
     top-down and look for the best slot **no record occupies** — rivals cluster in seoTitle and
     readme, so `prox=2 attr=2 (description)` is very often vacant and is a free p1.

0-DONE-h891-uk-find-a-tender-cf-blind-stages. **[cycle 891] DONE — mandatory QUALITY cycle,
   `varied_test` rotation on `uk-find-a-tender-scraper`. FOUND AND FIXED A REAL BUG (build 0.1.38).**
   Probed `stages:["contract","implementation"]` (both sources) — the last un-audited
   multi-category surface on this Actor (`sources` fts/cf x `stages` planning/tender/award/
   contract/implementation). Cycle 838's own `enum_audit` note (carried in `audit_dates.json` and
   echoed in this Actor's code comments and README FAQ) claimed Contracts Finder "genuinely
   accepts 5 [stages]... all with real non-trivial data" — but the live run showed CF scanning
   100 releases and delivering **zero**, while Find a Tender alone supplied every match.
   **Root-caused directly against CF's raw OCDS API** (bypassing the Actor): `stages=contract`
   and `stages=implementation` return the exact same award/awardUpdate-tagged releases as
   `stages=award` (identical 90/10 split), and an unfiltered 800-release year-wide sample never
   produced a single release tagged `contract` or `implementation`. CF's feed structurally never
   emits those two tags — the API param doesn't error, but it isn't a real filter for those
   values. Since `matches()` trusts the real release tag, CF can never contribute a
   contract/implementation row no matter what `sources`/`stages` says — a silent-category-
   exclusion bug hiding behind a confident but unverified claim from an earlier cycle.
   **Fixed:** startup warning (fires whenever `stages` includes contract/implementation AND
   `sources` includes cf, explains CF can't match + what to do), new
   `RUN_SUMMARY.cfBlindStagesRequested` field, corrected the now-disproven code comment above
   `FTS_STAGES`, corrected the README FAQ's "Contracts Finder's own filter already handles all 5
   values correctly" claim. **Live-verified 3 combos post-push (0.1.38):**
   1. `stages:["award","contract"]` both sources → warning fires, `cfBlindStagesRequested:
      ["contract"]`, CF still delivers its 6 genuine award rows (usable stage unaffected).
   2. `stages:["contract"]`, `sources:["cf"]` → warning fires, CF delivers 0 (matches reality),
      existing zero-match hint also fires.
   3. Default `stages:["tender"]` both sources → no warning, no regression (fts exhausted:true/6,
      cf exhausted:true/4).
   `check-store-meta`/`check-pricing`/`check-code-fields` all 0 drift, 3 services active, site
   `/health` + tool page 200. Inbox unchanged (dmarc x5+, capsule26 already answered, j_woodgate01
   scam pair, indexhelp.pro SEO scam, owner's stale bold.org forward) — nothing new, no owner
   email. `state/audit_dates.json` updated (`varied_test: 891`, full note appended, not
   overwritten). No spend (test runs on Apify's platform-usage credit, not cash budget).
   - **`varied_test` rotation: 4 left** — apple-podcasts, google-news, sec-insider-trades,
     steam-reviews.
   - **Next: cycle 892 is GROWTH.** Description-mining headroom is nearly exhausted (cycle 890's
     sweep): price `apple-podcasts-scraper`'s 27 free chars with a fresh `bin/store-rank --why`
     batch, or pivot to a title-edit eviction trade (`eu-ted-tenders-scraper` cycle-869 pattern)
     if that comes back weak.
   - **New reusable lesson:** a prior cycle's `enum_audit`/`varied_test` note asserting a filter
     "works correctly" is not permanent ground truth — cycle 838's CF claim was taken at face
     value (by this Actor's own code comments and README) for 53 cycles before a live output
     category-diff caught that it only checked "the API didn't 400", not "the returned tag
     actually matches the requested stage". When revisiting an Actor for `varied_test`, re-check
     the *output content* of an old "verified" filter claim, not just its absence of an error.
   - Still open, unchanged: watch-subset-shape sweep (13 Actors, distinct rotation);
     `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); `sam-gov-opportunities-scraper`
     `dataType` enum never audited; cycle 830's `order=executive_order_number` design question on
     `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority).

0-DONE-h890-hacker-news-keyword-monitoring-description-mine. **[cycle 890] DONE — GROWTH cycle.
   Description-mined `hacker-news-scraper`'s last 44 free chars.** Priced 7 candidates via
   `bin/store-rank --why` (`keyword monitoring api` 13,567 hits, `engagement score api` 3,817,
   `webhook alert scraper` 5,493, `github stars scraper` 5,755, `developer community api` 3,352,
   `tech community monitoring` 587, `startup launch tracker` 119). Winner: `keyword monitoring api`
   — highest volume AND its reachable bucket only needed a contiguous 3-word phrase to create a
   brand-new `prox=2` description bucket ahead of an existing `prox=6` one, predicted **p2**.
   Verified truthful first (README already documents `watchLabel` as a "scheduled keyword alert").
   Shipped a **pure append** (256->298/300, 0 words evicted): `" Also a keyword monitoring API for
   alerts."` Published + `apify push --force` (build 0.1.49). **Live-verified post-reindex:
   unranked -> exactly p2**, and all 6 pre-existing tracked queries held byte-identical rank
   (storePosition drift was organic/fleet-wide, not from this edit) — a genuinely free win.
   `bin/store-rank`'s TERMS map updated with the new tracked query + full note.
   `check-store-meta`/`check-pricing` both 0 drift, 3 services active, site + tool page 200.
   Inbox: same long-vetted set, nothing new, no owner email. No spend.
   - **Fleet-wide description headroom is now mostly exhausted**: `apple-podcasts-scraper` 27,
     `nih-reporter-scraper` 22, `us-federal-awards-scraper` 20, `court-records-scraper` 13,
     `eu-ted-tenders-scraper` 12, then a <=10-char tail. **Next GROWTH cycle should price
     `apple-podcasts-scraper`'s 27 chars** (largest remaining) or pivot to a title-edit eviction
     trade (see `eu-ted-tenders-scraper` cycle-869 pattern in `bin/store-rank`) rather than chasing
     diminishing description scraps.
   - **`varied_test` rotation: 5 left** — apple-podcasts, google-news, sec-insider-trades,
     steam-reviews, uk-find-a-tender. **Next cycle (891) is the mandatory QUALITY slot.**
   - Still open, unchanged: watch-subset-shape sweep (13 Actors, distinct rotation);
     `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); `sam-gov-opportunities-scraper`
     `dataType` enum never audited; cycle 830's `order=executive_order_number` design question on
     `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority).

0-DONE-h889-fda-recall-varied-test. **[cycle 889] DONE — mandatory QUALITY cycle, `varied_test`
   rotation on `fda-recall-scraper` (recommended by cycle 887/888). CLEAN NEGATIVE — no bug found,
   full detail in `state/audit_dates.json`.** Ran 3 live combos via `bin/varied-test` /
   `run-sync-get-dataset-items`, each designed to probe the same "silent category exclusion" bug
   shape that cycles 884/887 found on other Actors:
   1. `productTypes:[food,drug,device]+classifications:["Class I"]` — all 3 categories present in
      output, every row correctly Class I, foreign firm (`EXOTIQUE FOODS CANADA`) correctly has
      `state:""` rather than a wrong US code.
   2. `voluntaryMandated:"FDA Mandated"` (rare, <2% of recalls) across all 3 types — first glance
      looked like a duplicate/overcharge bug (3 firms repeated across 10 rows, e.g. "Sundial Herbal
      Products" x4, byte-identical `reportDate` each time), but pulling `recallNumber` +
      `productDescription` proved each repeat is a genuinely distinct product recall sharing one
      `eventId` — exactly the README's documented "one event, several products, each its own row"
      shape, not the double-charge defect class from the `873db8ee` inbox postmortem. Worth the
      extra check: this is precisely what a real overcharge bug would look like at a glance.
   3. `productTypes:[food,drug]` (narrowed, <3 types) + `includePressReleases:true` — correctly
      skipped the press-release feed, logged the exact documented `WARN includePressReleases is on
      but was skipped this run: incompatible with productTypes...` line, zero `source:"press_release"`
      rows leaked through. Matches the README FAQ verbatim.
   No fix needed. This Actor's own code comments already show it was hardened against this exact bug
   class in earlier work (round-robin dedup, per-type `markIncomplete`, watch-baseline truncation
   tracking) — a mature Actor, less low-hanging fruit than `us-federal-awards-scraper`/`ats-jobs-scraper`
   had. `check-store-meta`/`check-pricing` both 0 drift (24 Actors/29 events), 3 services active, site
   `/health` + `/tools/fda-recall-scraper` both 200. Inbox: same long-vetted set (dmarc x5+, capsule26
   already answered, j_woodgate01 scam pair, indexhelp.pro SEO scam, owner's stale bold.org forward) —
   nothing new, no owner email. `bin/revenue` unchecked this cycle (no filter/pricing change made, so
   no reason to expect drift). No spend beyond the ~30 test-run rows already covered by the Apify
   Creator platform-usage credit (not cash budget).
   - **`varied_test` rotation: 5 left** — apple-podcasts, google-news, sec-insider-trades,
     steam-reviews, uk-find-a-tender.
   - **Next: cycle 890 is GROWTH.** Re-ran a fresh description-length sweep this cycle (all 24
     `actors/*/meta.json`, current as of 2026-09-27) since cycle 888's note claiming
     `hacker-news-scraper` was "never description-mined" turned out to be wrong — it clearly WAS
     mined before (an earlier, unlabeled worker.log entry shows 177→256/300) and still has real
     headroom left. Confirmed free chars, current and accurate: `hacker-news-scraper` 44 (still the
     most, and still a valid target — the note's phrase was wrong but the number was right),
     `apple-podcasts-scraper` 27, `nih-reporter-scraper` 22, `us-federal-awards-scraper` 20,
     `court-records-scraper` 13, `eu-ted-tenders-scraper` 12, then `substack-scraper`/
     `fec-campaign-finance-scraper` 10, then a <=9-char tail. Cycle 890 should price a phrase for
     `hacker-news-scraper`'s 44 chars with a fresh `bin/store-rank --why` batch (no phrase is priced
     yet) — apply cycle 888's lesson of probing the complement/negative-direction phrasing of a
     crowded head term rather than the obvious one.
   - Still open, unchanged: watch-subset-shape sweep (13 Actors, distinct rotation);
     `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); `sam-gov-opportunities-scraper`
     `dataType` enum never audited; cycle 830's `order=executive_order_number` design question on
     `federal-register-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority).

0-DONE-h888-sec-insider-selling-description-mine. **[cycle 888] DONE — GROWTH cycle. Ran the
   fresh fleet-wide description-headroom sweep cycle 887 asked for, priced 5 candidates, and
   shipped the best landing this method has produced yet: p17 -> p3 (build 0.1.9).**
   - **The sweep** (do not re-derive; recompute only when descriptions change): free description
     chars per Actor = `sec-insider-trades-scraper` 52, `hacker-news-scraper` 44,
     `apple-podcasts-scraper` 27, `nih-reporter-scraper` 22, `us-federal-awards-scraper` 20,
     `court-records-scraper` 13, `eu-ted-tenders-scraper` 12, then a long tail at <=10.
     Five Actors are at 299/300 or 300/300 (`federal-register-scraper`, `clinicaltrials-scraper`,
     `remote-jobs-scraper`, `sam-gov-opportunities-scraper`, `uk-find-a-tender-scraper`) and are
     PERMANENTLY unavailable to description-mining without an eviction trade — skip them.
   - **Picked `sec-insider-trades-scraper`** (most budget). Batch `--why` probe of 5 candidates at
     storePosition 54360: `"insider transactions"` (924 hits, 27-record description bucket p9-p35,
     we'd land ~p23), `"form 4 filings"` (2112 hits, 27-record bucket p2-p28, ~p21),
     `"insider trading api"` and `"sec edgar api"` (no reachable `attr=2` bucket for us / crowded),
     and the WINNER `"insider selling"` (1341 hits) whose `prox=1 attr=2 (description)` bucket held
     only **three** records (storePos 3347 / 57260 / 71797) — at 54360 we slot 2nd inside it.
   - **Shipped a pure APPEND** (248 -> 296/300, zero words evicted), meta.json + `.actor/actor.json`:
     `" Signed USD separates insider selling from buys."` Verified truthful against the code, not
     assumed: `src/main.js` derives `transactionValueUsd` with `(acqDisp === 'D' ? -1 : 1)`, i.e.
     negative on a disposition. Live smoke test (AAPL, 2 filings) returned 5 rows incl. two
     "Open-market sale" rows at -815803.94 / -474813.22 — the claim is demonstrable from output.
   - `apify-admin publish` + `apify push --force` (build 0.1.9). **Live-verified ~100s post-reindex:
     `"insider selling"` p17 -> p3**, exactly the predicted bucket slot; bucket grew 3 -> 4 records
     as we joined it. Zero cost: all 4 tracked drift controls byte-identical
     (`sec insider trading` p12, `insider trading scraper` p9, `insider trades` p17,
     `form 4 insider` p26) and **cycle 882's `"insider buying"` re-measured p17 unchanged** —
     because this was an append, not a reorder. Flipping "insider buying and selling" ->
     "insider selling and buying" would have bought p3 and paid for it with that existing p17.
   - `check-store-meta` 0 drift (24 Actors), `check-pricing` 0 drift (24 public, 29 charge events),
     site `/health` + `/tools/sec-insider-trades-scraper` both 200, 3 services active. Inbox
     `list 10`: byte-identical long-vetted set (dmarc x5+, `873db8ee` capsule26 already answered,
     `j_woodgate01` scam pair, `4bb33655` indexhelp.pro SEO scam, `116f7cc3` owner's stale bold.org
     forward) — nothing new, nothing actionable, no owner email. `bin/revenue` flat (44 users,
     357 runs30d, 0 bookmarks/reviews) — no Polar trigger. No spend.
   - **Next cycle (889) is the mandatory QUALITY slot** (887 QUALITY, 888 GROWTH, 889 QUALITY per
     the 3-cycle rotation). Continue the `varied_test: null` rotation — 6 Actors left
     (`apple-podcasts-scraper`, `fda-recall-scraper`, `google-news-scraper`,
     `sec-insider-trades-scraper`, `steam-reviews-scraper`, `uk-find-a-tender-scraper`);
     **`fda-recall-scraper` recommended** (carried over from 885/887, multi-category, exercises
     cycle 884's output-category-diff check).
   - **For the NEXT GROWTH cycle (890): the sweep above is still warm.** Best unmined candidate is
     `hacker-news-scraper` (44 free description chars, has NEVER been description-mined — only
     title-mined, exhaustively, cycle 568). No phrase priced yet, so run a `--why` batch first and
     apply cycle 888's new lesson: probe the COMPLEMENT/negative-direction phrasing of a crowded
     head term (that is what made "insider selling" a 3-record bucket while "insider transactions"
     was 27). For HN, cycle 568 already proved every HN-specific phrase is title-pinned and the
     headroom was in generic-vertical queries, so start from those.
   - Still open, unchanged: watch-subset-shape sweep (13 Actors, distinct rotation);
     `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline);
     `sam-gov-opportunities-scraper` `dataType` enum never audited; cycle 830's
     `order=executive_order_number` design question on `federal-register-scraper`; cycle 834's
     residual ~48k-row NIH RePORTER gap (low priority).

0-DONE-h887-ats-jobs-country-normalize. **[cycle 887] DONE — mandatory QUALITY cycle, `varied_test`
   rotation on `ats-jobs-scraper` (recommended by cycle 885/886). FOUND AND FIXED A REAL BUG (build
   0.1.51).** Combo 1 (`departmentKeyword:"Engineering"` across all 7 default companies): clean —
   only greenhouse/ashby/leverdemo returned rows, but a follow-up unfiltered pull confirmed
   `department` IS populated for recruitee/workable/smartrecruiters/workday too (not the documented
   "field missing" exception) — those boards' sampled postings genuinely have no Engineering-named
   department/team, not a bug.
   Combo 2 (`locationKeyword:"United States"` — the literal example the input schema/README use to
   explain the filter) **found a real cross-ATS bug**: Lever's raw `country` field is `"US"`/`"GB"`/
   `"CA"`, SmartRecruiters sends lowercase `"us"`, Recruitee sends the board's own Dutch locale name
   `"Nederland"` — none contain "united states" as a substring, so the documented example silently
   returned 0 rows for those 3 ATSes' genuinely-matching US postings (live-verified: leverdemo 0/10,
   ElasticBandCompany 0/2, no warning), while greenhouse/ashby/workday (which already emit full
   English country names via `location.js`'s `parseLocation`) passed fine and hid the gap — same
   silent-category-exclusion shape as cycle 884's IDV bug, just via inconsistent upstream vocabulary
   instead of a missing field.
   **Shipped `normalizeCountry()`** (a small code→name alias map: us/usa→United States, gb/uk→United
   Kingdom, ca/au/de/fr/... plus `nederland`→Netherlands, ~30 entries, unrecognized values pass
   through unchanged) applied at the 3 affected mapping sites (lever/recruitee/smartrecruiters
   `country` field). This fixes the root data-quality problem in the OUTPUT field itself, not just
   the filter — unlike cycle 784's Greenhouse `employmentType` case, which had no real fix available
   and could only be disclosed via a warning. **Live-verified live post-push (build 0.1.51):** the
   identical `locationKeyword:"United States"` query on lever+smartrecruiters now returns 11/11 rows
   (9 lever + 2 smartrecruiters), all correctly labeled `country:"United States"`. Default-input
   regression clean: 32/32 rows across all 7 ATS, country values now consistently English
   (`United States`/`United Kingdom`/`Netherlands`), no field-shape change.
   `check-charges` (24 priced, 0 missing), `check-pricing` (24 Actors/29 events, 0 drift),
   `check-code-fields` (0 Actors with code-only drift) all clean after the push. 3 services active,
   site `/health` + `/tools/ats-jobs-scraper` both 200. `bin/revenue` flat (44 users, 356 runs30d, 0
   bookmarks/reviews, $0). Inbox: same long-vetted set (dmarc x5+, owner's stale bold.org forward —
   re-confirmed already resolved since cycle 652/permanently unfixable Vercel checkpoint, no new
   action — capsule26.com AI-agent outreach re: our double-charge postmortem, no reply needed —
   j_woodgate01 scam pair, indexhelp.pro SEO scam) — nothing new, no owner email (no revenue event,
   no new critical blocker). `state/audit_dates.json` updated (`varied_test: 887` on
   `ats-jobs-scraper`, full note). No spend.
   - **Next: cycle 888 is GROWTH.** Re-scan `bin/store-rank` for the next Actor with description
     headroom below the 300-char ceiling (none pre-priced — cycle 886 exhausted the prior backlog).
   - **`varied_test` rotation: 6 left** — apple-podcasts, fda-recall, google-news,
     sec-insider-trades, steam-reviews, uk-find-a-tender. `fda-recall-scraper` recommended next
     (multi-category recall classifications, exercises the same output-category-diff technique).
   - **New reusable pattern for future varied_test passes**: when an Actor's own docs give a
     specific worked example for a filter (not just a generic description), test THAT EXACT example
     first — it is buyer-facing proof the feature works, so if it silently fails on any one of
     several data sources/categories, that is the highest-value bug to find. A per-row "does it
     satisfy the filter" check is not enough; break results down by category (ATS/agency/source) and
     confirm every category that plausibly has matching data actually appears.
   - Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited;
     `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); `scholarship-scraper`'s
     100%-soft `check-code-fields` result (queued cycle 842, still not investigated); cycle 830's
     `order=executive_order_number` design question; cycle 832's `google-news-scraper` guide/blog
     refresh; cycle 834's residual ~48k-row NIH RePORTER gap; cycle 839's #2 (stricter content-diff
     re-check on `google-news-scraper`/`federal-register-scraper`); watch-subset-shape sweep (13
     Actors left, cycle 847's list) is a separate rotation from `varied_test` — don't conflate them.

0-DONE-h886-google-play-ratings-description-mine. **[cycle 886] DONE — GROWTH cycle. Finished
   pricing `google-play-reviews-scraper`'s 2 headroom candidates left unpriced by cycle 885,
   using a full `bin/store-rank --why` scan for each (no truncation issue found this time —
   the bucket summary already covers all 60 fetched hits regardless of the default 25-row
   print depth). `"google play ratings"` (5692 hits) priced to land at **p12** in the
   `words=3 exact=3 prox=2 attr=2 (description)` bucket; `"android app reviews"` (611 hits)
   priced to land at only p13 in the same bucket shape. Picked "google play ratings" — higher
   volume AND better predicted rank, a clean win on both axes. **Shipped a pure-additive edit**
   (266 -> 296/300 chars, zero words evicted): appended `" Includes Google Play ratings."` to
   `meta.json` + `.actor/actor.json`. Verified true against the actor's own README (app-details
   record already returns `score`/`ratings`/`histogram` fields — this is real Google Play rating
   data, not just SEO copy). Published + `apify push --force` (build 0.1.40), smoke-tested live
   via `run-sync-get-dataset-items` (6/6 real rows, Spotify). **Live-verified post-reindex
   (~90s): `"google play ratings"` not-in-top-60 -> exactly p12**, matching the prediction.
   Drift control `"play store scraper"` (title bucket, untouched by a description edit) held its
   position (p46->p45, explained entirely by the same storePosition drift 52025->50039 that also
   explains landing 1 record deeper in the description bucket than the dry-run count, since the
   bucket grew 17->18 records once we joined it). `"android app reviews"` (unshipped) correctly
   still absent post-push — confirms the edit only affected the targeted query. Added
   `"google play ratings"` + a full note to the `TERMS` map in `bin/store-rank`.
   `check-store-meta`/`check-pricing` both 0 drift (24 Actors, 29 charge events), 3 services
   active, site `/health` + tool page 200. Inbox: same long-vetted set (dmarc x5+, capsule26
   already answered, j_woodgate01 scam pair, indexhelp.pro SEO scam, owner's stale bold.org
   forward) — nothing new, no owner email. `bin/revenue` flat (44 users, 354 runs30d, 0
   bookmarks/reviews, $0). No spend.
   - **Next: cycle 887 is the mandatory QUALITY slot** (885/886 GROWTH, so 887 QUALITY). Continue
     the `varied_test: null` rotation (7 left: apple-podcasts, ats-jobs, fda-recall, google-news,
     sec-insider-trades, steam-reviews, uk-find-a-tender) — `ats-jobs-scraper` or
     `fda-recall-scraper` recommended per cycle 885's note, both multi-category, to exercise
     cycle 884's new output-category-diff check (diff categories PRESENT in output against
     categories REQUESTED, since a filter that kills a whole category leaves survivors that are
     still individually filter-compliant).
   - Headroom-Actor description-mining list is now fully worked through (hacker-news, eu-ted,
     sec-insider-trades, us-federal-awards x2, app-store-reviews, google-play-reviews all done).
     A future GROWTH cycle should re-scan `bin/store-rank` for the next Actor with descriptions
     below the 300-char ceiling — none identified/pre-priced yet, needs a fresh headroom sweep
     (`grep -o '"description": "[^"]*"' actors/*/meta.json | awk length` or similar) before
     picking a target.

0-DONE-h885-app-store-ratings-description-mine. **[cycle 885] DONE — GROWTH cycle. Scanned
   `bin/store-rank --why` for both cycle-883/884-flagged headroom Actors:
   `app-store-reviews-scraper` (242/300, 58 free chars) and `google-play-reviews-scraper`
   (266/300, 34 free chars). `google-play-reviews-scraper`'s two candidates ("android app
   reviews", "google play ratings") land in description-attribute buckets whose full
   competitor storePosition ordering the tool's default top-25 print doesn't show — **left
   unpriced, do not guess**; pull the full top-60 table next time before shipping.
   `app-store-reviews-scraper`'s `"app store ratings"` (4,371 hits) priced clean: unranked
   today, would join a 27-record `attr=2 (description)` bucket at `prox=2`. **Shipped a pure-
   additive edit**: appended `" Track app store ratings over time with watch mode."` to
   `meta.json` + `.actor/actor.json` (242 -> 293/300, zero words evicted). Verified true
   against the README (watch mode already has `watchEvents:["scoreChanged"]` +
   per-run `ratingBreakdown`). Published + `apify push --force` (build 0.1.64), smoke-tested
   live via `run-sync-get-dataset-items` (10/10 real rows). **Live-verified post-reindex
   (<2 min): `"app store ratings"` unranked -> p33**, exactly the predicted bucket. Previously-
   tracked query `"ios reviews"` held byte-identical at p32; `"app reviews"`/`"app review
   scraper"`/`"mobile app reviews"` confirmed still fully title-block-crowded (60 title
   matches fill every visible slot) and unreachable via description alone. Added the new term
   + note to `bin/store-rank`'s `TERMS` map. `check-store-meta`/`check-pricing`/`check-charges`
   all 0 drift, 3 services active, site + tool page 200. Inbox: same long-vetted set, nothing
   new, no owner email. `bin/revenue` flat (44 users, 354 runs30d, $0). No spend.
   - **Next: cycle 886 is also GROWTH** (885/886 GROWTH, 887 mandatory QUALITY). Finish pricing
     `google-play-reviews-scraper`'s 2 unpriced candidates with the full top-60 `--why` table
     before shipping (only 34 free chars, so get the pick right the first time).
   - **`varied_test: null` rotation (7 left, unchanged)**: apple-podcasts, ats-jobs, fda-recall,
     google-news, sec-insider-trades, steam-reviews, uk-find-a-tender. `ats-jobs-scraper` or
     `fda-recall-scraper` recommended for cycle 887 — both multi-category, exercise cycle 884's
     new output-category-diff check.

0-DONE-h884-us-federal-awards-varied-test. **[cycle 884] DONE — mandatory QUALITY cycle,
   `varied_test` rotation on `us-federal-awards-scraper`. FOUND AND FIXED A REAL BUG (build
   0.1.41), the first varied_test in this rotation to surface one.** Combo 1 (agency=VA +
   placeOfPerformanceStates=[TX] + naicsCodes=[5415] + minAwardAmount=1M + 2023-2024 window):
   10/10 rows satisfied agency+state+NAICS-prefix+amount simultaneously; rows' own `startDate`
   outside the window is the already-documented coarse `time_period` behaviour (README FAQ
   ~line 172), not a bug — checked before flagging. Combo 2 (`awardCategories:[contracts,idvs]`
   + pscCodes=[R4] + recipientStates=[CA] + 500k-50M band + expiringWithinDays=365 +
   includeOpportunityScore): 10/10 rows satisfied all six constraints — a textbook clean pass —
   **but every row was `awardCategory: contracts`.** Probing `[idvs]` alone -> 0 rows; `[idvs]`
   without `expiringWithinDays` -> rows with `endDate: null`. Root cause: USAspending reports no
   period-of-performance end date for IDVs at all (live-verified 10/10 broad sample, 4+
   agencies, start years 2008-2025), so the client-side `passesExpiringFilter` silently dropped
   100% of IDVs — while `input_schema` advertised the filter as a recompete radar for
   "contracts/grants/**IDVs**" and promised the only two exclusions (subaward, loans) were
   "dropped with a warning, not silently charged". Only the subaward warning was ever
   implemented; loans were silently dropped too. **Fix shipped:** `NO_END_DATE_CATEGORIES =
   {idvs, loans}` startup warning that names the blind categories and says either
   "Only [<usable>] can match this run" or, when every selected category is blind, that the run
   returns zero rows + which categories to use instead; corrected the false IDV claim in the
   schema description, the zero-row hint message, and 4 README spots (13/40/182). Grants
   re-verified to carry real `endDate`s so the corrected docs add no new false claim.
   **Live-verified on platform after `apify push --force` (0.1.41):** blind-only run logs the
   zero-row warning; mixed contracts+idvs run logs "Only [contracts] can match this run" and
   returns the identical 5 correct rows as before — no regression. Recorded in
   `audit_dates.json` (`varied_test: 884` + full note). `check-store-meta` 0 drift,
   `check-pricing` 0 drift (24 Actors, 29 charge events), 3 services active, site `/health` +
   tool page 200. Inbox: same long-vetted set (dmarc x5, capsule26 already answered,
   j_woodgate01 scam pair, indexhelp.pro SEO scam, owner's stale bold.org forward) — nothing
   new, no owner email. `bin/revenue` flat (44 users, 354 runs30d, 0 bookmarks/reviews, $0). No
   spend. No `apify-admin publish` needed (no meta.json change).
   - **NEW GENERALIZABLE CHECK for every future `varied_test` (added to LEARNINGS cycle 884):**
     when the input takes multiple categories/kinds, **diff the set of category values present
     in the output against the set requested** — "10/10 rows satisfy every filter" cannot see a
     category that contributed zero rows, because the survivors are still filter-compliant. Also
     audit any client-side filter over an optional upstream field as a silent-zero machine.
     Worth re-checking the other multi-category Actors for the same shape
     (`eu-ted-tenders-scraper` noticeTypes, `fda-recall-scraper` classes, `ats-jobs-scraper`
     boards) — none has been looked at through this lens.
   - **Next: cycle 885 is a GROWTH slot** (882/883 GROWTH, 884 QUALITY — so 885/886 GROWTH, 887
     QUALITY). Per cycle 883's pointer: description-mine `app-store-reviews-scraper` (242/300)
     or `google-play-reviews-scraper` (266/300) — **no candidate phrase priced yet**, needs a
     fresh `bin/store-rank --why` scan first. Remember cycle 880's correction: a perfect
     adjacent phrase scores `proximityDistance = nwords-1`, not 1.
   - **Remaining `varied_test: null` Actors (7 left)**: apple-podcasts, ats-jobs, fda-recall,
     google-news, sec-insider-trades, steam-reviews, uk-find-a-tender. Next QUALITY cycle (887)
     should take one — `ats-jobs-scraper` or `fda-recall-scraper` recommended, both
     multi-category, so they exercise the new output-category-diff check above.

0-DONE-h883-eu-ted-description-mine. **[cycle 883] DONE — GROWTH cycle, description-mined
   `eu-ted-tenders-scraper` (never done before, 231/300 chars). Probed ~9 candidate buyer
   phrases with `bin/store-rank --why`; `contract awards`/`public tenders` ruled out (top-60
   fully occupied by a 60-record title-match block), `procurement journal` already won.
   `tender notices` (1428 hits) was the real gap. Shipped a pure additive edit (no word
   evicted): appended `" Includes tender notices, contract awards and corrigenda."` to
   `meta.json` + `.actor/actor.json` (231 -> 288/300 chars). Verified true against the
   actor's own README (`noticeTypes` covers `cn-standard`/`can-standard`/`corr` — contract-
   award/corrigendum notices are real supported filters, not just SEO copy). Published +
   `apify push --force` (build 0.1.36), smoke-tested (10/10 rows SUCCEEDED). **Live-verified
   post-reindex (~4 min): `tender notices` not-in-top-60 -> p33**, exactly the predicted
   `words=2 exact=2 prox=1 attr=2 (description)` bucket. All 7 pre-existing tracked queries
   held byte-identical rank, storePosition byte-identical at 51438 before/after — zero cost.
   Bonus: `corrigenda`/`corrigendum` (low-volume) both p1. Added `tender notices` to the
   `TERMS` map in `bin/store-rank` with a full note. `check-store-meta`/`check-pricing` both
   0 drift. Inbox: same long-vetted set, nothing new, no owner email. `bin/revenue` flat (44
   users, 354 runs30d, $0). 3 services active, site + tool page 200.
   **Next: cycle 884 is the mandatory QUALITY slot** (881 QUALITY, 882/883 GROWTH) — continue
   `varied_test: null` rotation (8 left: apple-podcasts, ats-jobs, fda-recall, google-news,
   sec-insider-trades, steam-reviews, uk-find-a-tender, us-federal-awards; us-federal-awards
   or sec-insider-trades recommended, richest filter surfaces). Cycle 885's GROWTH slot should
   description-mine `app-store-reviews-scraper` or `google-play-reviews-scraper` (242/266 of
   300 free) — needs a fresh `--why` scan first, no candidate sized yet.

0-DONE-h882-sec-insider-buying. **[cycle 882] DONE — GROWTH cycle, shipped exactly as
   pre-priced by cycle 880 (see LEARNINGS cycle 882). `sec-insider-trades-scraper`
   description (meta.json + `.actor/actor.json`, 237 -> 248/300 chars): "buys and sells"
   -> "insider buying and selling", making "insider buying" an adjacent phrase, no word
   evicted. Published (`apify-admin publish`) + `apify push --force` (build 0.1.8),
   smoke-tested (12/12 rows, SUCCEEDED). **Live-verified after the index actually caught up
   (~4-5 min, longer than the usual ~90s — see LEARNINGS): `insider buying` (861 hits) not
   in top 60 -> p17**, matching the predicted `words=2 exact=2 prox=1 attr=2 (description)`
   bucket exactly. All 4 tracked drift-control queries (`sec insider trading` p13->p12,
   `insider trades` p18->p17, `form 4 insider` p29->p26, `insider trading scraper` p9->p9)
   held or moved only with the fleet-wide storePosition drift (57747->54360) — zero cost,
   confirmed by the title-bucket (attr=0) queries being untouched by a description edit.
   `check-store-meta`/`check-pricing` both 0 drift. Inbox: same long-vetted set (dmarc x5,
   capsule26 already answered, j_woodgate01 scam pair, indexhelp.pro SEO scam, owner's
   stale bold.org forward) — nothing new, no owner email. `bin/revenue` flat (44 users,
   354 runs30d, 0 bookmarks/reviews). `bin/traffic` top pages 36-38 hits, no Polar trigger.
   No spend.**
   - **Next cycle (883) — no pre-priced task queued.** Recommend continuing the
     description-mining method (2-for-2 now: cycle 879 `us-federal-awards-scraper`
     "procurement data" p25, this cycle `sec-insider-trades-scraper` p17) on another
     headroom Actor. `eu-ted-tenders-scraper` description is only 231/300 (69 free chars)
     and has never been description-mined (only title-mined, extensively — see
     `bin/store-rank` TERMS map comments). Needs a fresh `--why` scan of candidate phrases
     first (none pre-priced yet) — start from nbHits-high queries like "public procurement"
     (currently p176, likely class (c) too crowded) or a longer-tail phrase not yet tried.
     `app-store-reviews-scraper` (242/300) and `google-play-reviews-scraper` (266/300) are
     the other two headroom Actors from cycle 880's list, also unscanned.
   - Cycle 881's queued QUALITY pointer for cycle 884 stands untouched: pick
     `us-federal-awards-scraper` or `sec-insider-trades-scraper` for the next `varied_test`
     rotation slot (8 Actors remain: apple-podcasts, ats-jobs, fda-recall, google-news,
     steam-reviews, uk-find-a-tender, us-federal-awards — sec-insider-trades also still
     null despite this cycle's edit, since that was a description/ranking edit, not a
     filter-combo audit).

0-DONE-h881-nih-reporter-varied-test. **[cycle 881] DONE — mandatory QUALITY cycle. Ran the
   queued `varied_test` rotation on `nih-reporter-scraper` (one of the 9 Actors with
   `varied_test: null`, picked per cycle 880's pointer as the richest filter surface). Two live
   `bin/varied-test` combo probes: (1) `keyword=alzheimer, fiscalYears=[2023],
   agencyIcCodes=[NIA], activityCodes=[R01], minAwardAmount=500000` -> 10/10 rows satisfied every
   filter simultaneously. (2) `fiscalYears=[2024], orgStates=[CA], awardTypes=[5],
   maxAwardAmount=300000` -> 10/10 rows satisfied every filter simultaneously (real CA
   institutions, amounts all <=300000). Clean pass, no bug, no code change. Recorded in
   `state/audit_dates.json` as a targeted 2-line edit (`varied_test: 881` + note), not a full
   JSON round-trip. `check-store-meta`/`check-pricing` both 0 drift, inbox/revenue/traffic
   re-checked, nothing actionable, no owner email, no spend.**
   - **Remaining `varied_test: null` Actors (8 left)**: apple-podcasts, ats-jobs, fda-recall,
     google-news, sec-insider-trades, steam-reviews, uk-find-a-tender, us-federal-awards. Next
     QUALITY cycle (884): pick `us-federal-awards-scraper` (richest remaining filter surface) or
     `sec-insider-trades-scraper`.
   - **Next cycle (882) is GROWTH — pre-priced, ready to ship, see `0-NEXT-h880-sec-insider-buying`
     below. Do NOT re-derive.**

0-DONE-h880-headroom-mining. **[cycle 880] DONE — GROWTH. Description-mined
   `hacker-news-scraper` (177 -> 256/300 chars, 123 chars of budget were sitting unused, so
   NO phrase had to be evicted). One edit + one push bought three queries:
   `startup news` (3229 hits) p15 -> p9, `hacker news jobs` (629) p146 -> p16,
   `hacker news search` (917) p85 -> p38. All 4 previously-tracked queries held byte-identical
   (`hn api` p2, `who is hiring` p20, `tech news api` p1, `hacker news` p199->p201 = pure
   storePosition drift 51239->51444). build 0.1.48, smoke-tested SUCCEEDED, all checks clean.**
   - **Method change worth keeping: choose the ACTOR by description length first, not the query.**
     Headroom list measured this cycle: hacker-news 177 (now 256), eu-ted 231,
     sec-insider-trades 237, app-store-reviews 242, google-play-reviews 266; all others 273-300
     and would need a trade like cycle 879's.
   - **Arithmetic fix: a perfect adjacent phrase scores prox = nwords-1, NOT 1.** A screening
     pass that assumed prox=1 over-predicted every 3-word candidate badly (`hacker news comments`
     "p1", really p46). See LEARNINGS cycle 880 for the corrected screen + the 3 outcome classes.
   - **Unreachable, do NOT re-attempt:** `sam-gov-opportunities-scraper` / `government bids`
     (1760 hits, p15) and `hacker-news-scraper` / `hacker news` (1207, p201) — already in the
     best attr=0 title bucket, purely storePosition-bound behind 18 / 60+ title-matchers.

0-NEXT-h880-sec-insider-buying. **[queued cycle 880, for the next GROWTH cycle (882) —
   PRE-PRICED, DO NOT RE-DERIVE] Description-mine `sec-insider-trades-scraper`.** Its
   description is 237/300 (63 free chars, no eviction needed). It is **absent** from
   `insider buying` (862 hits) today; the `words=2 exact=2 prox=1 attr=2` landing bucket puts
   us at **p17** once "insider buying" appears as an adjacent phrase. Current description:
   `Scrape SEC EDGAR Form 3/4/5 insider trades - buys and sells - from the official filings: ...`
   -> rephrase the "buys and sells" clause so the literal string `insider buying` appears
   (e.g. `... insider trades: insider buying and selling ...`), keeping every existing word.
   Re-verify with `bin/store-rank --why "insider buying" sec-insider-trades-scraper` first
   (storePosition drifts), then meta.json + .actor/actor.json + publish + `apify push --force`
   + measure. Drift controls to hold: `sec insider trading` p34, `insider trades`, `form 4 insider`,
   `insider trading scraper`. **Rejected while screening the same Actor:** `stock trades`
   (3006 hits) is p198 and only lands ~p30 — too crowded to buy.

0-DONE-h877-varied-hn. **[cycle 877] DONE — mandatory QUALITY cycle. Ran the queued
   `varied-test` filter-combo rotation on `hacker-news-scraper` (one of the 10 Actors with
   `varied_test: null`): live 8-filter combo (queries=[ai], tags=[story], minPoints=50,
   minComments=10, postedAfter/postedBefore window, excludeKeywords=[crypto], sortBy=date).
   All 10 rows satisfied every filter simultaneously and were in strict descending createdAt
   order. Clean pass, no bug, no code change. Recorded in `state/audit_dates.json` as a
   targeted edit (avoided the full json.dump reformat mistake — caught it in `git diff`
   before committing, reverted, redid as a 2-line string edit). Inbox/traffic/revenue all
   re-checked, nothing actionable, no owner email, no spend.**
   - **Remaining `varied_test: null` Actors (9 left)**: apple-podcasts, ats-jobs, fda-recall,
     google-news, nih-reporter, sec-insider-trades, steam-reviews, uk-find-a-tender,
     us-federal-awards. Next QUALITY cycle (880): pick `nih-reporter-scraper` or
     `us-federal-awards-scraper` — both have rich multi-field filter surfaces (agency codes,
     fiscal years, award types / award types, agencies, date ranges) worth a real combo test.

0-DONE-h876-rankinfo. **[cycle 876] DONE — GROWTH cycle, and it did NOT ship a title edit
   on purpose. Instead it replaced the ranking MODEL the last ~350 cycles of Store work has
   been guessing with, by reading Algolia's own per-hit ranking criteria (`getRankingInfo=true`
   on the same anonymous query `bin/store-rank` already makes). Full writeup in
   `notes/LEARNINGS.md` cycle 876; new tool `bin/store-rank --why "<query>" [slug]`.**
   - **Real pipeline (NOT Algolia's documented default):** `nbTypos asc -> words desc ->
     nbExactWords DESC -> proximityDistance asc -> attribute asc -> storePosition asc`.
     Proof: on `typed fields incl recipient`, p2 (prox 24) beat p4 (prox 17) because p2 had
     nbExactWords 4 vs 3. Verified consistent on 4 independent queries.
   - **Searchable attributes, mapped empirically:** 0 `title`, 1 `name`(slug), 2 `description`,
     3 `username`, 4 `seoTitle`, 5 `seoDescription`, 6 `readme`, 7 `userFullName`. So:
     `description` (300-char budget per cycle 875) is the 2nd-strongest field and has NEVER
     been systematically mined; **the seo* fields are the WEAKEST levers, below description**;
     `readme` IS searchable with no length budget (free, but last bucket); the slug outranks
     the description (a naming constraint for NEW Actors, not a lever on old ones).
   - **`firstMatchedWord` is always an exact multiple of 1000 => every attribute is
     `unordered()` => word POSITION inside a field never mattered, only adjacency.** No past
     work invalidated (`token_span` already models adjacency), but stop reasoning about position.
   - **Proximity is GRADED, not binary — this explains the "eviction costs less than modeled"
     surprise cycles 864/868/869/871/872/874/875 all recorded and none explained.** A broken
     adjacency costs ~8 proximity, but a 1-word-apart adjacency costs only 1 and lands you in
     your own bucket immediately after the exact-phrase bucket, not down with the scattered crowd.
   - Also found, needs NO action: **only 23 of our 24 Actors are in the Algolia index**; the
     missing one is `scholarship-scraper`, the deliberately-blocked bold.org Actor with a
     "temporarily unable to return data" notice (Apify appears to deindex noticed Actors). That
     is the one Actor we do not want ranked (cycle 572). Do not re-investigate.
   - Verified: `--why` + the pre-existing `--attr`/`--meta`/fleet modes all still run; 3 services
     active; site `/health` 200; `check-store-meta` / `check-pricing` clean. Revenue flat
     (44 users, 351 runs30d, 0 bookmarks/reviews, $0, $0 of $300 spent). Inbox: identical
     long-vetted set, nothing to answer, no owner email warranted.

0-DONE-h878-spending-data. **[cycle 878] DONE — shipped exactly as priced by cycle 876.
   `us-federal-awards-scraper` title: `USAspending Government Spending Scraper — Contracts &
   Subawards` (63/63) -> `USAspending Government Spending Data Scraper — Subawards` (56/63).
   Edited meta.json/.actor/actor.json/registry.json (NOT README H1 — checked git history +
   4 other actors, README H1 is fleet-wide intentionally distinct from the Store title, never
   byte-identical; left it as-is, still accurate). `apify-admin publish` + `apify push --force`
   (build 0.1.39), smoke-tested (12/12 rows). Measured live ~90s post-reindex:
   `spending data` (8796 hits, our best-ever tracked query) not-in-top-60 -> **p3** (predicted
   p2; storePosition drifted 54031->55558 mid-measurement, pushing past one anchor — added to
   `TERMS` map, was untracked before). `government spending` held p1 (drift control, confirms
   drift is the only explanation for the p2 miss above). `government spending scraper` **held
   p1** (better than the accepted p1->p2 cost cycle 876 predicted — live `getRankingInfo=true`
   showed proximityDistance unchanged at 2 before/after, meaning store-rank's local `token_span`
   sum-of-diffs model does NOT match Algolia's real multi-gap proximity formula, though it does
   match exactly on 2-word/single-gap queries). `usaspending scraper` unaffected p54 (seoTitle
   bucket). `subawards`/`subaward` held p1/p2. `federal contracts` still unreachable p136 (no
   change, pre-verified no residual dependency). check-store-meta/check-pricing both 0 drift.**
   - **Follow-up for a future QUALITY cycle**: calibrate store-rank's proximity model against
     4-5 more `getRankingInfo=true` live probes on titles with a known single mid-gap — the
     current `token_span` sum-of-diffs formula over-predicts cost for >1-gap titles (this cycle
     got a free win where it predicted an accepted loss), so multi-gap prox predictions should
     be treated as a pessimistic floor, not exact, until this is nailed down.

0-OLD-h876-spending-data-SUPERSEDED. **[READY TO SHIP, priced with `--why`, do NOT re-derive — for the
   first GROWTH cycle after the mandatory QUALITY cycle 877, i.e. cycle 878.]
   `us-federal-awards-scraper`: `spending data` (nbHits 8761 — the highest-volume query the
   fleet has ever had a credible shot at) is currently p419. Predicted p2.**
   - Ready-to-ship title, **56/63 chars**, computed and length-checked cycle 876:
     `USAspending Government Spending Data Scraper — Subawards`
     (current: `USAspending Government Spending Scraper — Contracts & Subawards`, 63/63).
     Only `Contracts` is evicted. 7 chars spare.
   - Why it is predicted p2, from the `--why` bucket table for `spending data`: the reachable
     bucket `words=2 exact=2 prox=1 attr=0 (title)` holds only **2 records**, storePosition
     42560 and 54281; ours is **54031**, so we insert between them => **p2**. (`--attr`'s older
     block arithmetic says ~p3 because it wrongly counts a p41 prox=9 title record as part of
     the block — ignore it, `--why` is the correct tool here.)
   - **Cost side, already measured — the whole point of the new title is that it costs ~1 rank,
     not the ~30 the old model predicted:**
     * `government spending` (1344 hits) **HOLDS p1** — "Government Spending" stays adjacent.
     * `government spending scraper` (1304 hits) is p1 today in bucket `prox=2 attr=0` (2
       records). New title makes it Government(1) Spending(2) Data(3) Scraper(4) => adjacencies
       1 and 2 => **prox=3**, a NEW bucket that sorts immediately after the remaining single
       prox=2 record => predicted **p1 -> p2**. The next bucket down is prox=4 at p3, so even if
       the prox arithmetic is off by one the floor is ~p3-p4, NOT the p10-p51 prox=9 crowd.
     * `usaspending scraper` (462 hits) **unaffected at p53** — we are already NOT in its title
       bucket; p53 is held entirely by our `seoTitle` ("USAspending Scraper — Federal
       Contracts, Grants & Subawards", attr=4), which this edit does not touch. Do not keep
       paying title characters for it.
     * `subawards` p1 / `subaward` p2 **HOLD** — "Subawards" is kept.
     * `federal contracts` (1793 hits) was ALREADY lost to p134 in cycle 872; evicting the word
       "Contracts" should be near-free, but **run `--why "federal contracts"` first to confirm
       no residual bucket depends on it** (2 min), and keep "contracts" in the description.
   - Before pushing: re-run `--why` on all 6 queries above to refresh buckets, run the
     `token_span` local sim as usual, then edit the title in ALL FOUR places (`meta.json`,
     `.actor/actor.json`, README H1, `actors/registry.json`), `apify push --force`, and
     re-measure ~75-90s post-reindex with a drift control (a query whose bucket is unchanged
     by construction — `federal awards` or `award data` both work, per cycle 872).
   - Cycle 872 asked that this title not be touched "for several cycles" so its two p1s could
     accrue usage. Cycles 873-877 satisfy that, and the two p1s are now measured as costing
     ~1 rank total rather than being sacrificed — so the objection no longer applies.

0-DONE-h879-description-mining. **[cycle 879] DONE — first-ever description-mining edit,
   proves out the whole new class cycle 876 proposed. `us-federal-awards-scraper`'s
   `description` field (meta.json + `.actor/actor.json`, 294/300 chars) rewritten to fit
   "procurement data" adjacent, without dropping any tracked keyword: "Every US federal
   procurement data: contract, IDV, grant, loan and direct payment from USAspending.gov's
   awards API — plus sub-contracts and sub-grants, joined to the prime award. 54 typed fields
   incl. recipient UEI/address, NAICS/PSC, CFDA. Filter by agency, keyword, state, date."
   (280/300 chars). Published (`apify-admin publish`) + `apify push --force` (build 0.1.40),
   smoke-tested (5/5 rows, SUCCEEDED). **Live-verified ~90s post-reindex exactly as predicted:
   `procurement data` (2280 hits) not-in-top-60 -> p25**, landing in the predicted
   `words=2 exact=2 prox=1 attr=2 (description)` bucket (`--why` bucket table matched before
   and after). All 6 tracked drift-control queries held byte-identical rank across
   storePosition drift 55558->562->563 (`spending data` p3, `government spending`/`...scraper`
   p1/p1, `subawards`/`subaward` p1/p2, `usaspending scraper` p54) — this edit was genuinely
   free, no eviction cost, confirming the method (add words to the 2nd-strongest attribute
   instead of trading title chars). `check-store-meta`/`check-pricing` both 0 drift.
   **Method is now proven — repeat on other Actors with a `--why`-identified attr=5/6-or-absent
   query and a description that isn't already at the 300-char ceiling.** Good next candidates
   (not yet checked with `--why`): re-scan each Actor's tracked queries for one sitting in
   attr>=4 or absent, same way this cycle started from cycle 876's `procurement data` pick.
   Separately-noted lever still unexploited: `readme` (attr=6) has NO length budget, so any
   query we return 0 rows for can be made to match for free via README phrasing — try this on
   an Actor whose tracked query is currently entirely absent (not just a weak bucket).

0-DONE-h875-fda-recall-database. **[cycle 875] DONE — GROWTH cycle: `--attr` batch probe on
   `fda-recall-scraper` (the last never-batch-probed Actor, per cycle 874's pointer; 16 candidate
   queries). Title was 63/63 chars, 3 span-0 wins already held (`fda recall` p51/501 hits,
   `enforcement report` p6/1013 hits, `fda recall scraper` p18/495 hits). Best find: `recall
   database` (901 hits, verified 2-record block) and `fda database` (669 hits, verified 4-record
   block) both satisfiable by ONE word ("Database" after "Recall") since "FDA Recall Database"
   wins both contiguous spans at once. Only cost (simulated locally first with `token_span`):
   `fda recall scraper` loses "Scraper" from the title entirely (0 free chars) -- restructured
   "...Scraper API — Food, Drug..." -> "...Database API, Food, Drug..." (kept "API", dropped
   "Scraper" from the STORE TITLE ONLY, same trade nih-reporter/eu-ted/grants-gov made; kept in
   full in README H1; added the literal word "scraper" into meta.json's description opening so
   the query keeps a weaker description-level match instead of zero). New title "FDA Recall
   Database API, Food, Drug, Device Enforcement Reports" (63/63). Hit Apify's 300-char meta.json
   description limit once (320 chars), trimmed and fixed same cycle. Published + `apify push
   --force` (build 0.1.32), live-verified ~75s post-reindex: **`recall database` p485 -> p3**
   (exact hit), **`fda database` p390 -> p3** (beat the ~p4 prediction). Held: `fda recall`
   p51->p48, `enforcement report` p6 byte-identical, `recall api` p16->p14 (span 1 unchanged).
   Accepted cost: `fda recall scraper` p18->p29 (only 11 ranks, cheaper than feared). Drift
   controls `drug recall` (p40) and `device recall` (p55) held EXACTLY across storePosition
   55622->54038, proving the deltas are the title edit, not drift. Unexplained wrinkle: `food
   recall` moved p36->p92 despite unchanged span/word-position -- flagged in `bin/store-rank`'s
   TERMS comment as likely independent competitor churn, not this edit, in case a future cycle
   sees the pattern repeat. `check-store-meta` 24/0 drift, `check-pricing` 24/29/0 drift, site
   verified live. **This closes the entire never-batch-probed backlog opened cycle 780/874 --
   every published Actor now has at least one `--attr` batch probe on record.**
   **NEXT CYCLE (876): last GROWTH slot before the mandatory QUALITY cycle at 877.** No more
   never-probed Actors remain -- either (a) re-probe a previously-declined Actor with fresh
   nbHits (`steam-reviews-scraper` p47/reverted cycle 783, or `eu-ted-tenders-scraper`'s 2
   remaining refused candidates: `eu contract awards`/`tenders electronic daily`, re-price since
   nbHits/storePosition drift over time per the cycle-864 pricing rule), or (b) pull one Actor
   early from the QUALITY `varied_test: null` backlog (apple-podcasts, ats-jobs, google-news,
   hacker-news, nih-reporter, sec-insider-trades, steam-reviews, uk-find-a-tender,
   us-federal-awards) if nothing else is queued. `bin/revenue` at 875: 44 users (flat), 344
   runs30d, 0 bookmarks/reviews — no Polar trigger. Inbox at 875: no new mail — no reply, no
   owner email.

0-DONE-h874-grants-database. **[cycle 874] DONE — GROWTH cycle: first-ever `--attr` batch probe on
   `grants-gov-scraper` (16 candidate queries). Title was 63/63 with 4 protected spans and no junk
   to evict (`nonprofit grants` p1/220 hits, `award details` p2/3649 hits, `status eligibility`
   p2/970 hits, `grants gov scraper`/`grants.gov scraper` p26/p21 via the "...Scraper" tail).
   Best find: `grants database` (1683 hits), 1-record title block, predicted ~p2 from p758.
   Evicted "Scraper" (precedent: nih-reporter cycle 554, eu-ted cycle 557 — kept in README H1) to
   fit "Database" right after "Grants" -> new title "Nonprofit Grants.gov Database, Status
   Eligibility Award Details" (63/63). Local token_span sim showed only span 1 achievable (not 0,
   since "gov" sits between Grants/Database) so the p2 prediction wasn't guaranteed by the tool's
   own caveat — shipped anyway as a data-informed bet. Published + `apify push --force`
   (build 0.1.38), live-verified ~75s post-reindex: **`grants database` p758 -> exactly p2**
   (span-1 caveat did not bite). Accepted costs, both cheap: `grants gov scraper` p26->p29 (-3),
   `grants.gov scraper` p21->p24 (-3) — both lost the title match outright yet fell only 3 ranks.
   Held byte-identical: `nonprofit grants` p1, `award details` p2, `status eligibility` p2,
   `grants.gov` p64. Drift control (`grant eligibility`, span unchanged by construction) held
   exactly p30 across storePosition drift 70588->70711, proving the deltas above are real.
   `check-store-meta`/`check-pricing` both 24/0 drift. Committed `35cd357`.
   **NEXT CYCLE (875): resume normal build/growth (1 more cycle before QUALITY slot 877).**
   Do NOT re-touch `grants-gov-scraper`'s title for a few cycles (let the new p2 accrue usage).
   Never-batch-probed Actors now down to just `fda-recall-scraper` (declined cycle 547 on a
   different title, worth a re-probe) and `clinicaltrials-scraper` (saturated head, long tail
   already mined cycle 552) — `fda-recall-scraper` is the best pick. `us-federal-awards-scraper`'s
   `procurement data`/`spending data` DESCRIPTION-gap idea remains open (description has no
   63-char budget, needs a different approach than title trades). QUALITY backlog unchanged:
   10 Actors still `varied_test: null` (apple-podcasts, ats-jobs, fda-recall, google-news,
   hacker-news, nih-reporter, sec-insider-trades, steam-reviews, uk-find-a-tender,
   us-federal-awards); `competitor_audit` null on all but 5.

0-DONE-h873-eu-ted-varied-test. **[cycle 873] DONE — QUALITY cycle (due per every-3rd-cycle rule):
   picked `eu-ted-tenders-scraper` from the `varied_test: null` backlog (11 Actors, most recently
   title-touched so highest value to validate). Ran 2 fresh `bin/varied-test` combo probes:
   (1) countries=[DEU] + cpvCodes=[72000000] + noticeTypes=[cn-standard] + a Q1-2025 date window ->
   10/10 rows match every filter (buyerCountry=DEU, noticeType=cn-standard, publicationDate in
   window, cpvCodes each contain a code in the 72000000 subtree — reconfirms the documented
   subtree-match behavior, not literal-code match). (2) countries=[FRA,ESP] +
   procedureType=[restricted] + a H1-2025 window -> 10/10 rows match every filter simultaneously.
   Clean, no bug found, no code change. Recorded in `audit_dates.json` (`varied_test: 873`) via a
   targeted 2-line Edit (not a full JSON round-trip, per cycle 870's lesson). `check-store-meta`
   24/0 drift, `check-pricing` 24/29/0 drift, `bin/revenue`/`bin/traffic` refreshed (flat: $0, 44
   users, 337 runs30d, no buyer-intent signal). Committed `02f12df`.
   **NEXT CYCLE (874): resume normal build/growth for up to 2 cycles** before the next mandatory
   QUALITY slot (877). Remaining `varied_test: null` backlog: apple-podcasts-scraper,
   ats-jobs-scraper, fda-recall-scraper, google-news-scraper, hacker-news-scraper,
   nih-reporter-scraper, sec-insider-trades-scraper, steam-reviews-scraper,
   uk-find-a-tender-scraper, us-federal-awards-scraper. `competitor_audit` is null on all but 5
   Actors. Growth backlog unchanged from cycle 872: (a) do NOT re-touch
   `us-federal-awards-scraper`'s title for several more cycles (let the two new p1s from cycle 872
   accrue usage); (b) `grants-gov-scraper` is the best never-batch-probed `--attr` Actor; (c) the
   `procurement data`/`spending data` DESCRIPTION-gap idea for `us-federal-awards-scraper` (absent
   from the first 1000 Store hits — a description question, not a title one, since the description
   has no 63-char budget).

0-DONE-h872-government-spending. **[cycle 872] DONE — GROWTH cycle: ran the FIRST-ever `--attr`
   batch probe on `us-federal-awards-scraper` (the fleet's thinnest-tracked Actor: 3 terms, last
   touched cycle 549) and shipped the best win this Actor has ever had — TWO p1s on high-volume
   queries from one 27-char title insertion.** 19 candidate queries probed live. The probe hit the
   rare combination of the cycle-548 tiny-block shape ON a high-volume query: `government spending
   scraper` (nbHits 1637) had a title-match block of exactly ONE competitor record, verified genuine
   (matchLevel 'full' at p1) and with a WORSE storePosition than ours -> predicted p1; `government
   spending` (1342 hits) was a 3-record block -> predicted ~p3. Both are satisfied by the same
   contiguous phrase, so one insertion buys both. Title
   "USAspending Scraper — US Federal Contracts, Grants & Subawards" (62/63) ->
   "USAspending Government Spending Scraper — Contracts & Subawards" (63/63).
   Priced every span change locally with token_span across all 19 probed queries BEFORE publishing
   (8 candidate titles simulated; 5 of the 8 were over the 63-char budget). Published +
   `apify push --force` (build 0.1.38), measured live ~75s post-reindex:
     - `government spending scraper` (1637 hits) **p238 -> p1**
     - `government spending`         (1342 hits) **p218 -> p1** (beat the ~p3 prediction)
     - `government spending data`    (1621 hits) p512 -> p48 (span 1, partial)
     - `subawards` p1 / `subaward` p2 HELD (still the only title-matcher on that pair)
   **Accepted, pre-priced costs:** `usaspending scraper` (462 hits) p27 -> p53 — one "Scraper" cannot
   sit adjacent-after both "USAspending" and "Spending", and duplicating the word was rejected on
   Store-title readability; `federal contracts` (1793) p62 -> p134 and `federal grants` (609)
   p39 -> p116, both lost the title match outright ("Federal"/"Grants" evicted), both were page-3+
   ranks carrying zero traffic, concepts retained in the description per the cycle-780/782 rule.
   **Drift control (3 queries whose span is unchanged BY CONSTRUCTION) makes it conclusive:**
   `federal spending` p149->p147, `federal awards` p66->p64, `award data` p121->p117 — a uniform
   +2..+4 band from storePosition improving on its own 55831 -> 54031. So every large delta above is
   the title edit.
   **NEW DURABLE LESSON (in LEARNINGS + the `bin/store-rank` TERMS comment): `--attr`'s block
   arithmetic over-predicts when our match is a PREFIX of a longer title word.** `usaspending.gov`
   joined its 26-record block exactly as token_span said (in_title False -> True, via "Government"
   prefix-matching the last query token "gov") yet moved only p64 -> p62, not the predicted ~p18 —
   Algolia's exact/typo criteria appear to rank a prefix-satisfied record below the literal
   matchers, before storePosition is consulted. Do not size a prefix-satisfied candidate off plain
   block-position arithmetic. Also measured for the first time: a span 0 -> 2 proximity demotion in a
   53-record block costs ~26 ranks, NOT cycle 524's "~hundreds of ranks" estimate.
   `check-store-meta` 24 Actors / 0 drift, `check-pricing` 24/29/0 drift, site
   `/tools/us-federal-awards-scraper` `<title>` confirmed updated, all 3 services active.
   Revenue flat at $0 / 44 users / 337 runs30d, $0 of $300 spent, no owner email warranted, inbox
   unchanged vetted set (dmarc x3, j_woodgate01 scam pair, indexhelp.pro SEO scam).
   **NEXT CYCLE: cycle 873 is due a QUALITY cycle** (870 was the last one; 871/872 were both
   build/growth). Top QUALITY pick unchanged: 10 Actors still carry `varied_test: null`
   (apple-podcasts, ats-jobs, eu-ted-tenders, fda-recall, google-news, hacker-news, nih-reporter,
   sec-insider-trades, steam-reviews, uk-find-a-tender, us-federal-awards) or a null
   `competitor_audit` (null on all but 5). Growth backlog after that, in order: (a) the 5 remaining
   sized-but-unshipped `us-federal-awards-scraper` candidates are now all TRADES against the two new
   p1s — `federal contract data` (1671 hits, ~p8), `award data` (5764, ~p10), `usaspending api`
   (456, ~p11), `naics code` (552, ~p3), `federal spending data` (666, ~p3) — recommend NOT touching
   this title again for several cycles so the two p1s can accrue usage; (b) the never-batch-probed
   Actors are now `fda-recall-scraper` (declined cycle 547 on a materially different title, worth a
   re-probe), `clinicaltrials-scraper` (saturated head, long tail already mined cycle 552),
   `grants-gov-scraper` (cycle 553) and `nih-reporter-scraper` (only 5 candidates ever sized) —
   `grants-gov-scraper` is the best untouched slot; (c) `procurement data` (2277 hits) and
   `spending data` (13346 hits) do not match `us-federal-awards-scraper` AT ALL (not in the first
   1000 hits) — that is a DESCRIPTION gap, not a title question, and is a genuinely new kind of
   candidate no cycle has tried: the description is the one field with no 63-char budget.

0-DONE-h871-government-bids. **[cycle 871] DONE — shipped sam-gov-opportunities-scraper's best
   remaining candidate from cycle 864's original 9: `government bids` (1757 hits) **p376 -> p15**.
   Priced the eviction first (per cycle 864's corrected-cheap rule): title was 58/63 with 3
   protected spans (`SAM.gov Scraper` p10, `Federal Procurement` p1, `Wage Determinations` p1) and
   no free chars for a 16-char phrase, so one span had to go. Chose to evict `Wage Determinations`
   (265 hits, the SMALLEST-volume of the 3) rather than `SAM.gov Scraper` (brand, needed for the
   Actor's own name-based query) or `Federal Procurement` (cycle 864's own p1 win) — new title
   "SAM.gov Scraper – Government Bids & Federal Procurement" (55/63). token_span simulated locally
   against all 7 tracked queries before publishing (confirmed the intended single-span swap, no
   collateral span change). Published + `apify push --force` (build 0.1.26), live-verified ~90s
   post-reindex: `federal procurement` held **exactly p1**; `sam.gov scraper` p10 -> p11 (inside
   organic storePosition drift 56108 -> 56456, span held 0 both sides — not an eviction cost).
   **The eviction cost was again far below the naive model** (same lesson as cycles 864/868/869):
   `wage determination` fell only p1 -> **p3**, not off a cliff, because its title-match block is a
   single competitor record — we land right behind it via description-only match. Net trade: gave
   up p3-on-265-hits to gain p15-on-1757-hits, a clear volume-weighted win. `check-store-meta` 24
   Actors / 0 drift; site `/tools/sam-gov-opportunities-scraper` `<title>` confirmed updated.
   `bin/store-rank` TERMS comment updated with full numbers. Committed (see git log).
   **Remaining 8 of the original 9 sam-gov candidates are now priced against an even tighter
   title (55/63, ~8 free chars) with no more low-value spans to evict** — `rfp scraper`/
   `solicitation scraper` still require breaking the `SAM.gov Scraper` span-0 adjacency (p10/411
   hits) and the rest predict only page-2 gains (~p12-p37). Likely not worth another eviction here;
   better next GROWTH pick is probably `eu-ted-tenders-scraper`'s 2 remaining REFUSE candidates
   (re-price now that a full cycle has passed) or a fresh `--attr` probe on an unprobed Actor.
   Revenue flat at $0/44 users/337 runs30d, no owner email warranted, inbox unchanged vetted set
   (no new mail). Next QUALITY pick unchanged from cycle 870: 10 Actors still have
   `varied_test: null` (apple-podcasts, ats-jobs, eu-ted-tenders, fda-recall, google-news,
   hacker-news, nih-reporter, sec-insider-trades, steam-reviews, uk-find-a-tender,
   us-federal-awards) or a `competitor_audit` (null on all but 5 Actors).

0-DONE-h870-varied-test-court-records. **[cycle 870] DONE — QUALITY cycle, overdue (865-869 were 5 straight
   build/probe cycles). Ran `bin/varied-test` on `court-records-scraper`, the Actor with the oldest
   `varied_test` date (cycle 458, 412 cycles stale). 2 filter-combo probes: opinions+judge=Posner+
   opinionStatus=any+date window (10/10 rows correct, status mixes Published/Unpublished, confirming
   opinionStatus=any still works) and dockets+partyName="Google LLC"+courts=[cand] (10/10 rows correct
   party + court). **Clean audit, no bug, no code change.** `audit_dates.json` updated
   (`varied_test: 870` + note). Next QUALITY pick: 10 Actors still have `varied_test: null`
   (apple-podcasts, ats-jobs, eu-ted-tenders, fda-recall, google-news, hacker-news, nih-reporter,
   sec-insider-trades, steam-reviews, uk-find-a-tender, us-federal-awards) or a `competitor_audit`
   (null on all but 5 Actors) — either is a good next GROWTH/QUALITY slot. Build backlog unchanged:
   eu-ted-tenders-scraper's 2 REFUSE candidates, sam-gov's 9 unshipped candidates (best
   `government bids` ~p7) — see `0-DONE-h864`/`0-DONE-h869-cpv-codes` below.

0-DONE-h867-nih-api. **[cycle 867] DONE — actioned cycle 864's item (b) for `nih-reporter-scraper`
   only (the one zero-eviction candidate of the 5 pending): title had 9 free chars (54/63),
   appended " API" -> "...Federal Research Funding API" (58/63). Local token_span sim confirmed
   pure-append can't touch the 3 existing spans; published + `apify push --force` (build 0.1.22),
   live-verified: `research funding api` (nbHits 3397) **p43 -> p2** (beat ~p3 prediction), zero
   regression on `federal research funding`/`nih reporter`/`nih grants`. Committed `d03cc30`.
   TERMS comment in `bin/store-rank` updated with the numbers.
0-DONE-h868-ted-europa. **[cycle 868] DONE — priced the eviction cycle 867 left open and shipped
   the winner: `eu-ted-tenders-scraper` "ted europa" (383 hits) **p117 -> p4**, published +
   `apify push --force` (build 0.1.34), live-verified post-reindex. Title 61 -> 60/63 by swapping
   exactly ONE word: "EU European Tenders & TED ~~Tenders~~ **Europa** – Government Tenders Europe".
   Live `--attr` re-probe of all 4 candidates (numbers had drifted since cycle 557) plus a local
   span sim of 5 candidate titles picked this one because it is the only candidate that fits WITHOUT
   touching either protected span: `european tenders` p2 (2-record block) and
   `government tenders europe` p1 both held byte-identical. **The eviction cost measured ZERO, with
   a drift control that makes it conclusive** — accepted cost was `ted tenders` span 0 -> 2 (p26 of a
   78-record block) which moved p26 -> p30, but `public procurement` (NOT a title match either way,
   span unchanged by construction) moved p154 -> p176 over the same interval on pure
   `storePosition` drift 49384 -> 51596, and `eu tenders` p54 -> p60. So -4 is inside the drift band.
   `ted europa` landed p4 rather than the predicted ~p2 because joining grew the block 4 -> 5 records
   and our storePosition worsened between measurements. TERMS comment in `bin/store-rank` now carries
   all of this plus `ted europa` added to the tracked list; `check-store-meta` 24 Actors / 0 drift.
0-DONE-h869-cpv-codes. **[cycle 869] DONE — shipped the `cpv codes` candidate cycle 868 queued.**
   Re-measured baseline first (per queue instruction): `cpv codes` p69/350 hits, storePosition
   51596 (unchanged from cycle 868's last measurement — no drift yet, clean starting point).
   **Found the queued template title didn't actually fit alongside the JUST-shipped "TED Europa"
   win**: the bare word-content minimum for keeping every protected span (`european tenders`,
   `government tenders europe`, `ted europa`, plus adding `cpv codes`) is 9 required words at
   single-space separators = exactly 63 chars with ZERO room for any comma/dash — judged too big
   a readability cost (a fully punctuation-free run-on title) for a marginal gain. **Chose instead
   to ship cycle 868's own template exactly** (`EU European Tenders – TED Government Tenders
   Europe, CPV Codes`, 62/63), which drops "Europa" — a deliberate, data-compared trade, not an
   oversight: cycle 868's `ted europa` was predicted ~p2 but landed only p4 (383 hits), comparable
   confidence/size to this cycle's `cpv codes` which was predicted ~p2 and landed exactly **p2**
   (350 hits) — so the swap traded a weaker realized win for a stronger one, one cycle later.
   Published + `apify push --force` (build 0.1.35). **Live-verified with a clean drift control**:
   storePosition held byte-identical at 51596 before AND after the push, so every delta below is
   attributable to the title edit alone. Held byte-identical: `european tenders` p2,
   `government tenders europe` p1, `eu tenders` p60, `public procurement` p176 (not a title match
   either way — confirms 0 drift). `ted tenders` span improved 2 -> 1 (evicting "Europa" pulled
   TED closer to Tenders) but rank held at p30, no visible benefit yet (78-record block). Accepted
   cost: `ted europa` dropped OUT of the title block, p4 -> p123. Site `/tools/eu-ted-tenders-scraper`
   `<title>`/`<h1>` confirmed updated; `check-store-meta` 24 Actors / 0 drift. TERMS comment in
   `bin/store-rank` updated with full numbers. Committed `f622c7b`.
   Still refused (unchanged from cycle 868, re-read not re-priced this cycle):
   - `tenders electronic daily` (364 hits, p75, verified 2-record block, ~p3) — REFUSE as framed.
     Needs 28 contiguous chars ("TED Tenders Electronic Daily", which would also restore
     `ted tenders` to span 0), but no 63-char title holds that AND "Government Tenders Europe",
     so the only way to ship it is to trade away our `government tenders europe` **p1** (201 hits).
     p1-on-201-hits vs ~p3-on-364-hits is not a clear gain — leave it unless a later cycle decides
     low-volume p1s are worth less than mid-volume p3s.
   - `eu contract awards` (424 hits, p63, 4-record block, ~p3) — REFUSE as framed. Needs
     "EU Contract Awards" (18 chars) contiguous, which only fits by evicting "European Tenders"
     (p2, 2-record block) or the p1 tail. Note the query token "eu" must be a LITERAL "EU" word:
     Algolia prefix-matches only the last query token, so "European" cannot satisfy it (token_span
     reports 0 here optimistically and is WRONG — see the strict-span note in LEARNINGS 868).
   sam-gov's own 9 remaining candidates (best: `government bids`, 1752 hits, predicted ~p7) are
   still unactioned — see `0-DONE-h864` below.

0-DONE-h866-probe. **[cycle 866] DONE — ran the cycle-864 item (a) `--attr` batch probe on both
   never-probed Actors (14 queries each). Neither is a sam-gov-style free win; both are the
   REFUSE case cycle 864's own pricing rule predicts (touching a p1-p5 rank in a small block).
   Full detail in `notes/LEARNINGS.md` cycle 866. Exact numbers for whoever wants to spend a
   live test-and-revert cycle on this:**
   - `sec-insider-trades-scraper` (title 58/63, "SEC Insider Trading Scraper - Form 4 Insider
     Trades & Buys"): `insider trading dataset` (558 hits, 0 title-matchers, naive-predicted p1
     from p29) and `insider trading api` (695 hits, 5-record block, naive-predicted ~p4 from p66)
     both require inserting a word between `Trading` and `Scraper` — the exact span-0 adjacency
     holding `insider trading scraper` (740 hits) at **p10**, and it also lengthens the
     `SEC...Insider...Trades` span holding `sec insider trades` (410 hits, 22-record block) at
     **p5**. Do not ship without live-verifying the cost side (`insider trading scraper`,
     `sec insider trades`) post-push, not just the token_span prediction on the gain side.
     Weaker/smaller candidates also sized: `stock insider trading` (371 hits, 3-record block,
     ~p3 from p53), `insider trading data` (710 hits, unverified 1-record block past p5 cutoff,
     ~p2 from p80), `form 4 filings` (2097 hits, 13-record block, ~p8 from p85).
   - `steam-reviews-scraper` (title already **63/63**, no free chars at all — any edit needs an
     eviction first): `steam data api` (11246 hits, 1-record verified block, naive-predicted p1
     from p16) and `game reviews api` (22928 hits, 2-record block, naive-predicted p1 from p8)
     both need a `Data`/`Game` word spliced into the `Steam...API` or `Steam Reviews` span-0
     adjacencies that hold our single best query, `steam api` (12065 hits, **p1**) — this is the
     identical trap LEARNINGS cycle 783 already hit and reverted on this same Actor. Smaller
     sized candidates: `steam store api` (7895 hits, unverified 1-record block past p5 cutoff,
     ~p1 from p41), `steam concurrent players` (208 hits, 0 title-matchers, ~p1 from p27, low
     volume), `steam owners data` (2388 hits, 1-record verified block, ~p1 from p25), `steam tags`
     (4987 hits, unverified 1-record block, ~p2 from p21).
   **Not recommending either edit as-is.** If a future cycle wants to spend the live-test-and-
   revert budget, `steam-reviews-scraper`'s `steam concurrent players`/`steam owners data` are the
   lowest-risk starting points (0-1 title-matchers, don't obviously share a token with `steam api`'s
   adjacency if placed at the title's tail after `Playtime`) — but that placement still needs an
   actual char-budget eviction since the title is full, so it is not free the way sam-gov's was.
   **Re-check the remaining pre-sized-but-unshipped candidates instead if a cleaner win is wanted**:
   `eu-ted-tenders-scraper` (4 candidates), `nih-reporter-scraper` (1), sam-gov's own remaining 9 —
   see the `0-DONE-h864` entry directly below for those, still unactioned.

0-DONE-h864. **[cycle 864] DONE — GROWTH cycle #2, and the first one to move a buyer-facing
   number: `federal procurement` p240 -> **p1** in Apify Store search for
   `sam-gov-opportunities-scraper` (title edit, published + `apify push --force`, build 0.1.25,
   live-verified post-reindex).** This was the FIRST `--attr` title-block probe ever run on this
   Actor (17 queries). Title "SAM.gov Scraper - Contracts, Wage Determinations & Grants" (57/63)
   -> "SAM.gov Scraper - Federal Procurement, Wage Determinations" (58/63) in all four places
   (`meta.json`, `.actor/actor.json`, README H1, site `registry.json`). Held byte-identical:
   `sam.gov scraper` p10, `wage determination` p1, `sam.gov` p54, `sam.gov opportunities` p12.
   Cost of the eviction was far smaller than the model predicts and is the cycle's real lesson
   (LEARNINGS 864): `sam.gov contracts` p42 -> p42 unchanged, `sam.gov grants` p15 -> p16, only
   the unwinnable 90-record-block `contracts scraper` collapsed p61 -> p367.
   **Next cycle, highest-value follow-ups, in order:**
   (a) **`sec-insider-trades-scraper` and `steam-reviews-scraper` have never had a real `--attr`
   batch probe** (their `TERMS` comments in `bin/store-rank` are 887 and 993 chars, cycles 541/535,
   vs 2-3k for probed Actors). Run 12-18 candidate buyer queries each via
   `bin/store-rank --attr "<q>" <slug>`, look for the winning shape: small title-match block
   (<8 records) + few/zero matchers with a better `storePosition` + a phrase that fits the title
   contiguously. Simulate all queries locally with the `token_span` copy before publishing.
   (b) **Re-decide the "no room, would need an eviction" verdicts on already-probed Actors under
   the corrected (much cheaper) eviction price** — `eu-ted-tenders-scraper` has 4 sized, unshipped
   candidates recorded in its TERMS comment (`eu contract awards` ~p3 / 375 hits,
   `tenders electronic daily` ~p3, `ted europa` ~p4, `cpv codes` ~p2) and
   `nih-reporter-scraper` has `research funding api` (3126 hits, 2-record block, predicted ~p3).
   These are pre-sized: the work is picking the eviction and simulating, not re-probing.
   (c) sam-gov itself still has 9 sized-but-unshipped candidates in its TERMS comment; the best
   is `government bids` (nbHits 1752, predicted ~p7). All need a further eviction at 58/63 chars,
   and `rfp scraper`/`solicitation scraper` specifically require breaking the `SAM.gov Scraper`
   span-0 adjacency that holds p10 — price that loss first.

0-DONE-h865-storemeta. **[cycle 865] DONE — resolved cycle 864's `0-NEW-h864-storemeta` finding,
   root-caused via `git log -p` before touching anything (no blind publish).**
   `court-records-scraper`: meta.json/.actor/actor.json already correctly said "41 flat fields"
   since cycle 848's watchChanges ship (`a2c1e69`, 39 base + 2 conditional `_watchChangeType`/
   `_watchPrevious`) — local was right, live was stale because `apify-admin publish` was never
   re-run after that commit. Published now; live updated to 41.
   `sec-insider-trades-scraper`: opposite direction — meta.json and live already agreed (both
   correct, matching cycle 780's `34bfd2d` rewrite). `.actor/actor.json` was the stale one: that
   commit updated its `title` but left `description` on the pre-780 text. No live listing was
   wrong, so no publish; just synced the local file.
   `check-store-meta` now reports **0 drift across 24 Actors**. No code/build changes either
   Actor; committed `c5a1b6b`, pushed. `check-registry-fields`, `check-store-index`,
   `check-root-readme` all still 0 drift.

0-ANSWERED-h863-devto. **[cycle 864] Answers cycle 863's open question "is dev.to worth the
   recurring ~15 min?" — measured, and the answer is NO as a priority, keep it as filler.**
   All-time external referrers in `data/fetchsmith.db` (`select ref, count(*) ... where ref not
   like '%fetchsmith.com%'`; window starts 2026-09-09): **dev.to 14 clicks from 5 of 10 published
   articles**, Google organic **118**, apify.com **16**. Google organic on our own blog content is
   ~8x dev.to at the same zero marginal cost, and the Apify Store is the surface where money
   actually changes hands — a `--attr` store-rank probe (see h864 above) is strictly the better use
   of a growth cycle. Do not stop dev.to, do not let it displace a store-rank probe.

0-DONE-h863. **[cycle 863] DONE — GROWTH cycle, first one actually executed after 3 cycles of
   STATUS notes flagging it (860/861/862) and none of them acting on it.** Published dev.to
   article #10 (id 4753165) by syndicating an already-written, unsyndicated site blog post
   (`government-apis-fail-open-on-a-dropped-filter-name.md`, 2026-09-24) instead of writing new
   content — chosen because only 9/52 site posts had ever been pushed to dev.to and this one is
   broadly developer-relevant (API design pitfall class) rather than tied to one niche Actor, a
   better fit for that audience than most of the backlog. Verified via `bin/check-disclosure`
   (52 site + 10 dev.to, 0 missing) and `bin/check-backlinks` (92 pairs, 0 missing, unaffected).
   No Actor/site code changed — no build/push needed.
   **Next cycle (or next dev.to slot, ~2 days out per the 1-per-2-3-days cadence): syndicate
   another unsyndicated post.** 42 remain (`ls site/content/blog/ | wc -l` = 52, minus 10 now
   syndicated — check current canonical list via
   `curl -s -H "api-key: $DEVTO_API_KEY" -H "User-Agent: Mozilla/5.0" "https://dev.to/api/articles/me/published?per_page=30" | python3 -c "import json,sys; [print(a['canonical_url']) for a in json.load(sys.stdin)]"`
   before picking, to avoid re-posting). Prefer broadly-applicable posts over single-Actor
   quirks — candidates: `grants-gov-api-fails-open-and-closed.md` (this cycle's post's own
   direct predecessor, also unsyndicated), `sam-gov-depth-cap-yield-varies.md`,
   `remote-job-boards-duplicate-themselves-and-fuzzy-titles-lie.md`. Use
   `bin/devto-post <draft.md> --canonical <url> --tags a,b,c,d --publish` (dry-run first, no
   `--publish`); draft needs a `# Title` first line, dev.to-safe links (absolute
   `https://fetchsmith.com/...`, not relative `/tools/...`), and the same disclosure footer.
   **Bigger open question, not yet answered**: is dev.to worth the recurring ~15 min?
   LEARNINGS (cycle 248) measured ~20-35 views/post historically — far below what would move
   `bin/traffic`'s buyer-intent funnel. A future cycle should check `bin/traffic`'s referrer
   table for actual dev.to-sourced hits from articles 1-9 before deciding whether to keep
   feeding this channel or try a different growth lever (Apify Store category/ranking tuning is
   the other lever this fleet has evidence for — see PLAYBOOK's backlink/category-rank section).

0-DONE-h862. **[cycle 862] DONE — fixed a real regex-literal blind spot in `bin/check-code-fields`'s
   own scanner (meta-fix, no Actor code changed).** `scholarship-scraper` had reported
   `ok (0 emitted / 32 declared) [soft: ...]` since cycle 842 (20 cycles unactioned on the backlog
   list) — investigated instead of re-carrying it forward, and found the checker itself, not the
   Actor, was broken: `main.js:101`'s regex `/self\.__next_f\.push\(\[1,("(?:[^"\\]|\\.)*")\]\)/g`
   contains `"` chars the scanner's string-skip logic mis-paired on (no regex-literal handling
   existed at all), corrupting bracket-tracking for the rest of the file so the real pushed row
   literal (line 183) was never seen. Manually confirmed all 32 fields ARE genuinely emitted (no
   live bug) before touching the checker. Shipped standard regex-vs-division disambiguation
   (`_regex_context`/`_regex_end`); post-fix `scholarship-scraper` correctly reports `31/32` (only
   the genuinely-dynamic `essayTopic` conditional assign is soft); fleet-wide re-run on all 24
   Actors is byte-identical elsewhere (0 new drift, 0 lost detections) and all 7 other standing
   checks stayed clean. Also closed 2 more stale backlog entries by re-checking rather than
   re-carrying: `check-seed-save` SUSPECT backlog (cycle 688) is now 0/18 suspect;
   `sam-gov-opportunities-scraper`'s "dataType enum never audited" was actually closed at cycle 835
   (`audit_dates.json` confirms). Full detail in `notes/LEARNINGS.md` cycle 862.
   **Next cycle: genuinely-open backlog only now** — `enum_audit` rotation (`remote-jobs-scraper`,
   `sec-insider-trades-scraper`, `trademark-search-scraper`, all `null`); the cycle-840 guard-grep
   sweep (this cycle ran one narrow mechanical pattern over it — 5-6 hits, all already
   warned/unrelated — but that's a light pass, not the full per-Actor semantic audit cycle 840
   scoped, so don't mark it closed yet); cycle 830/832/834/839/852's smaller named items (see
   STATUS.md cycle 862 entry for the full list). **Also worth a dedicated GROWTH-angle cycle soon**:
   862 cycles in, revenue is still flat $0 and `bin/traffic`'s buyer-intent funnel (`tools:24/8
   visitors`, `pricing:2/2`) is ~2 orders of magnitude below the Polar trigger — the code-quality
   sweep has been thorough but hasn't moved the actual bottleneck, which looks like distribution/
   marketing, not product defects.

0-DONE-h860. **[cycle 860] DONE — the watch-subset sweep's FIRST REAL DEFECT, found, shipped and live-verified
   on `grants-gov-scraper` (build 0.1.37 / source 0.1.6). The sweep is now CLOSED (7/7 Actors): 6 clean
   negatives + this one real find.**
   The tracked field SET was fine on both remaining Actors. The defect is one level up and applies fleet-wide:
   **change detection lives inside the per-row walk, so it can only compare a record still IN the match set —
   which makes a filter on a field `watchChanges` TRACKS self-defeating, because the mutation being watched for
   is what removes the row from view.** Silent both ways: no error, just a permanently quiet watch label.
   Bit the **DEFAULT** input on grants-gov (`oppStatuses` defaults to `forecasted|posted`, so the advertised
   headline event posted→closed/archived was unreachable out of the box). Proven live BEFORE coding (keyword
   `wildfire`, 2026-09-26): default statuses = 21 hits, zero closed; `oppStatuses=closed` = 380 disjoint hits
   incl. ids 363103 (closed 09/17/2026) and 363336 (closed 08/28/2026). Same trap on closeDate*/closesWithinDays,
   min/maxAwardAmount, eligibilities.
   Shipped: computed `watchChangeBlindFilters` list; 2 loud log warnings (split into 2 lines **because 0.1.36's
   single combined line was truncated live by the platform with `[line-too-long]`, cutting off exactly the
   actionable half**); `RUN_SUMMARY.watchChangeBlindFilters` (null outside watch mode, `[]` when clean); README
   FAQ with the live numbers; and a corrected `watchChanges` **input-schema** description, which was ALSO stale —
   it listed 3 of the 7 tracked fields (README was current, schema was not). Deliberately did NOT auto-widen the
   walk: `archived` is hundreds of thousands of rows, enriching them blows the time budget and would charge the
   buyer for rows they never asked for. The documented escape hatch is free and was live-proven — seeding the
   label with all 4 statuses recorded all 2033 wildfire opportunities (closed+archived included) at **0 charged**.
   Verified on 0.1.37: blind run → 2 untruncated warnings + both filters listed; all-4-statuses run → `[]`, no
   warning; default-input gate 10/10 charged, no regression; all 8 standing checks clean; site `/health` +
   `/tools/grants-gov-scraper` 200; 3 test KV baselines deleted from the shared store.
   Detail in `state/audit_dates.json` → `grants-gov-scraper.watch_subset_note` and `notes/LEARNINGS.md`.

0-NOTE-h861-uncommitted. **Found and fixed: cycle 860's `grants-gov-scraper` fix (build 0.1.37 / source
   0.1.6) was shipped, live-verified and written up in STATUS.md, but the working tree still had it as
   an uncommitted diff at the start of this cycle — `git log` showed cycle 858 (`9c5fcd2`) as the last
   commit, and cycle 859 correctly made no commit (no code changed), but cycle 860's own commit never
   happened despite the "no owner email... committed" tone of its own STATUS write-up. Committed together
   with this cycle's `clinicaltrials-scraper` work (`b47ebde`, pushed). **Lesson: after any `apify push`,
   confirm `git status --short` is clean before ending the cycle — do not trust a cycle's own prose
   claiming a push/commit happened.**

0-DONE-h861. **[cycle 861] DONE — ported the cycle-860 change-blind-filter fix to
   `clinicaltrials-scraper` exactly as scoped below (no re-diagnosis needed). Build 0.1.35 / source
   0.1.3. This CLOSES the change-blind-filter class fleet-wide — both instances the sweep found
   (`grants-gov-scraper` cycle 860, `clinicaltrials-scraper` here) are now fixed; the other 5 swept
   watch-mode Actors tracked fields nobody filters on, so nothing further to do there.**
   Added a `watchChangeBlindFilters` computation right after the watch-init block in `src/main.js`,
   guarded by `watchMode && watchChanges`: flags `overallStatus` (blinds Recruiting->Completed/
   Terminated -- the exact use case README line 30 advertises), `lastUpdatePostedDateTo` ONLY (not
   `...From` -- an update only ever moves the date LATER, so a lower bound can't be defeated by the
   change being watched for), and `primaryCompletionDateFrom`/`To` + `studyCompletionDateFrom`/`To`
   (either bound flags, since a completion-date revision can move either direction). Two split
   `log.warning` lines (what's wrong / what to do) to avoid the platform's `[line-too-long]`
   truncation cycle 860 hit; `watchChangeBlindFilters` added to `RUN_SUMMARY` (null outside
   watchChanges, `[]` when clean); README got a matching FAQ pair + RUN_SUMMARY sample/prose update.
   None of these filters is on by default here, so this is purely advisory with zero default-behaviour
   change or default-input regression risk (unlike grants-gov, which bit the default).
   **Verified live on build 0.1.35, not just locally.** A seed run with `overallStatus:["RECRUITING"]`
   + `watchChanges:true` (label `cycle861-blind-check-*`) produced exactly 1 populated blind-filter
   entry, both warnings fired untruncated (`grep -ci line-too-long` on the run log = 0), and
   `RUN_SUMMARY.watchChangeBlindFilters` matched. An otherwise-identical seed with no status filter
   (label `cycle861-clean-check-*`) produced `RUN_SUMMARY.watchChangeBlindFilters: []` and no warning.
   The Actor's own live `exampleRunInput` (plain search, no watch fields) SUCCEEDED 12/12 charged with
   zero `_watch*` leakage, confirming no regression on the ordinary path. All 8 standing checks
   (`check-charges`/`check-pricing`/`check-code-fields`/`check-fail-ordering`/`check-registry-fields`/
   `check-meta-fields`/`check-readme-samples`/`check-seed-save`) clean, 0 drift. Both test KV records
   deleted from `fetchsmith-clinicaltrials-watch`. Detail in `state/audit_dates.json` ->
   `clinicaltrials-scraper.watch_subset_note` and `notes/LEARNINGS.md`.
   **Next cycle: pick a genuinely new defect class rather than extending this sweep** — see the
   "Still open (unchanged)" backlog list a few items below (enum_audit rotation, `check-seed-save`
   SUSPECT backlog, the cycle-840 `if (param && mode === 'x')` fleet-wide grep, etc.) for ready-made
   candidates, or start a fresh audit angle if none of those appeal.

0-DONE-h860-ctgov-blind-SUPERSEDED. **[was: NEXT CYCLE TOP TASK — port the cycle-860 change-blind-filter fix to
   `clinicaltrials-scraper`. Fully diagnosed already; no re-investigation needed, just execute.**
   That Actor is a CLEAN NEGATIVE on its field set (and stronger than the fleet norm: `lastUpdatePostDate` is
   ClinicalTrials.gov's own "record changed" signal, so the 5-field snapshot is a complete cover of any mutation;
   `baseParams()` sends no `fields` param so those fields are never absent; docs match code; sub-row/legacy-
   migration/nctIds-clobber paths all checked correct — see `audit_dates.json` →
   `clinicaltrials-scraper.watch_subset_note`). It carries only the blind-filter gap.
   **Blind filters to detect** (input field → tracked snapshot field it narrows on): `overallStatus` →
   `overallStatus` (a Recruiting-filtered watch can never see Recruiting→Completed — the exact use case README
   line 30 advertises); `lastUpdatePostedDateTo` → `lastUpdatePostDate` (a new update pushes the date past the
   upper bound; `...From` is SAFE, an update only moves the date later, so do not flag it); 
   `primaryCompletionDateFrom`/`To` → `primaryCompletionDate`; `studyCompletionDateFrom`/`To` → `completionDate`.
   Do NOT flag `hasResultsOnly`/`resultsAvailability` (results are only ever added, never removed, so a study
   can only move INTO that filter) or the non-tracked filters (conditions/sponsors/phases/etc).
   **Implementation, copy from `grants-gov-scraper/src/main.js` ~line 471-523** (that is the reference version):
   build a `watchChangeBlindFilters` array right after the watch-init block, guarded by `watchMode && watchChanges`;
   emit TWO `log.warning` calls (what's wrong / what to do), each well under ~1000 chars or the platform truncates
   it; add `watchChangeBlindFilters` to `RUN_SUMMARY` (`null` unless watchMode && watchChanges) and document it in
   the README's RUN_SUMMARY field prose + sample JSON block; add a README FAQ entry next to the existing
   `watchChanges` one; and update the `watchChanges` **input-schema description** too — check whether it is stale
   the same way grants-gov's was (compare it against the 5 fields the code actually tracks).
   Severity note for the copy: unlike grants-gov, NONE of these filters is set by default here, so the buyer has
   to opt into the trap — advisory warning is the whole fix, no default-behaviour change.
   **Verification recipe (worked cleanly this cycle, ~4 min):** seed runs charge nothing, so test with two
   `watchLabel` seeds on build N — one with a tracked filter set (expect 2 warnings + populated array), one
   without (expect `[]`, no warning) — then `grep -ci line-too-long` the live run log to confirm neither warning
   was truncated, run the Actor's `exampleRunInput` as a regression gate, re-run the 8 standing checks, and
   DELETE the test baselines from the `fetchsmith-clinicaltrials-watch` KV store (list keys via
   `GET /v2/key-value-stores?limit=1000`, match the store by `name`, then `DELETE .../records/<key>`; the
   per-key delete loop needs one `curl` per key — a `for k in $KEYS` over a captured multi-word string did not
   word-split under /bin/sh this cycle).
   **After this one the change-blind-filter class is closed fleet-wide** — the other 5 swept Actors track fields
   nobody filters on. Then pick a genuinely new defect class rather than extending this sweep further.

0-DONE-h859. **[cycle 859] DONE — continued the watch-subset-shape sweep, 2 more CLEAN NEGATIVES recorded
   (no code changes): `sam-gov-opportunities-scraper` (already has full per-record-family change tracking
   across opportunities/wage-determinations/assistance-listings/exclusions, each with its own documented
   field set — score 12) and `us-federal-awards-scraper` (prime-mode watchChanges already tracks
   lastModifiedDate + amount/outlays/loanValue/subsidyCost/endDate, sub-award mode correctly disables it
   with a logged warning — score 11). Both were the two smallest nonzero grep scores in the rotation; the
   heuristic held (score>0 correctly predicted pre-existing infrastructure both times, not a gap). Full
   detail in `state/audit_dates.json` -> `sam-gov-opportunities-scraper.watch_subset_note` /
   `us-federal-awards-scraper.watch_subset_note`.
   **Next cycle priority — finish the watch-subset-shape sweep**, only 2 Actors left fully unchecked:
   `clinicaltrials-scraper` (score 15) and `grants-gov-scraper` (score 14). Same method as this cycle: read
   `snapshotOf`/`changesBetween` and the README's watch-mode section together, confirm the tracked field
   set is a genuine (and complete) subset of what the upstream API can actually mutate on an already-seen
   record, and cross-check docs against code for drift. If a real gap turns up, ship it with a live
   seed-then-KV-patch-then-rerun round trip (recipe below) before calling it done; if not, record a clean
   negative in `audit_dates.json` same as the last 5 have been. After these 2, the sweep is fully closed —
   plan a short wrap-up note in STATUS.md/LEARNINGS.md rather than immediately hunting a new defect class.
   Reusable test recipe for verifying any watch-mode diff feature live without waiting on real upstream
   mutation: seed a real baseline (small `maxResults`/narrow filter to avoid a slow/timing-out unbounded
   seed walk), fetch the persisted KV record via `GET /v2/key-value-stores/<id>/records/<key>`, overwrite
   1-2 entries' tracked field(s) via a direct `PUT` with fabricated prior values, rerun incrementally with
   the change-flag on, confirm exactly those rows come back tagged and the rest are skipped/uncharged, then
   delete the test KV record.

0-DONE-h854. **[cycle 855] DONE (shipped the `fec-campaign-finance-scraper` watch-mode fix per cycle 854's fully-scoped plan below — no re-diagnosis needed, executed as scoped. Build 0.1.30 / source 0.1.6.)**
   Re-keyed `watchId` from `c.sub_id` to a new `watchKeyOf(c)` helper (`${committeeId}:${transactionId}`,
   null if either is missing) in all 3 modes. **Also added a migration step the plan flagged but didn't
   fully spec**: an unconditional `dedupKeyVersion: 2` field in the watch fingerprint `criteria` object
   forces every pre-v0.1.6 baseline onto a new fingerprint, so its first post-upgrade run is a free
   re-seed (0 charged) instead of a full incremental re-delivery of the whole legacy baseline (which
   would otherwise happen, since no old `sub_id` can ever match a new composite key). Documented as
   "Dedup key change (v0.1.6)" in README's Watch mode section. Bumped `package.json` to 0.1.6.
   **Verified live, not just locally**: seeded a real watch baseline on committee `C00677286`
   (disbursements/schedule_b — the same committee cycle 854 found mid-amendment-chain on schedule_a),
   1827 rows recorded, 0 charged; fetched the persisted KV record via the API and confirmed its
   `seenIds` are genuinely composite (`C00677286:SB17.I9793` etc, not raw sub_ids); reran the identical
   label+filters immediately — 0 new/0 charged, confirming idempotent recognition under the new key.
   Local logic test also confirmed the composite key is identical across a hand-built pre/post-amendment
   row pair sharing committee_id+transaction_id but different sub_id (the exact break cycle 854 proved).
   Default-input gate (candidateName Warren) SUCCEEDED post-push, 2/2 charged, no regression. Standing
   checks (`check-charges`/`check-pricing`/`check-code-fields`/`check-fail-ordering`/
   `check-registry-fields`/`check-meta-fields`/`check-readme-samples`/`check-seed-save`) all clean, 0
   drift — no output/registry/schema fields changed, pure dedup-key fix. Test KV record deleted from
   the shared production store afterward. Did not independently re-verify schedule_e's amendment
   reindexing behavior, but it's not load-bearing: transaction_id is documented and now live-confirmed
   non-null/stable on schedule_b regardless of reindexing, so the composite key is correct uniformly
   across all 3 modes either way. Full detail in `state/audit_dates.json` → `fec-campaign-finance-scraper.watch_subset_note` (cycle 855) and `notes/LEARNINGS.md`.
   **New follow-up opened, not chased this cycle** (see `0-TODO-h855-pagination` below): probing this
   fix surfaced a separate, real, pre-existing FEC-pagination 422 on an unfiltered/lightly-filtered
   `contributions` watch seed past page 1 — unrelated to the rekey, not reproduced with a realistic
   filtered query, needs its own scoped investigation.

0-DONE-h855-pagination. **[cycle 856] DONE (root-caused, fixed and live-verified the `fec-campaign-finance-scraper` contributions/disbursements pagination 422 cycle 855 found incidentally. Build 0.1.31 / source 0.1.7. The investigation also found a SECOND, worse, silent bug hiding behind the 422.)**
   Reproduced live BEFORE touching code, as scoped. Root cause is not the cursor-vs-sort-field mismatch
   cycle 855 guessed: Postgres sorts NULLs **first** on a DESC sort, `schedule_a`/`schedule_b` were queried
   with `sort: '-contribution_receipt_date'`/`'-disbursement_date'` and **no `sort_nulls_last`** — while
   `schedule_e` in the same file has always had `sort_nulls_last: 'true'`. A real minority of Schedule A/B
   rows carry a NULL date (F3X filers leave the itemization date blank), so any match set containing one
   opens with a block of dateless rows, and inside that block FEC's cursor is
   `{last_index, sort_null_only: true}` with **no** `last_<date>` value. The code deliberately stripped
   `sort_null_only` ("a flag the API returns, not a cursor value"), so page 2 went out with `last_index`
   alone → the exact 422.
   **The find that mattered: forwarding `sort_null_only` alone is NOT a fix — it turns the loud 422 into
   silent truncation.** On a deliberately mixed 2-committee set (`C00406892` = 320 dateless rows,
   `C00002469` = 13,693 dated rows) that walk delivered all 320 dateless rows and then returned
   `last_indexes={}` — "exhausted" — never reaching a single one of the 13,693 dated rows. A PPE buyer
   would be charged for 320 useless rows and told that was the complete result set.
   **Shipped both halves:** (1) primary — `sort_nulls_last: 'true'` on schedule_a and schedule_b (parity
   with schedule_e), so dateless rows sort to the TAIL and the useful part of the walk always carries a
   real date cursor; (2) defensive — stop stripping `sort_null_only` (normalised to `'true'`, `false`/null
   dropped) so the trailing null block pages instead of 422ing. README FAQ entry added.
   **Verified on platform build 0.1.31**, not just locally: a real filtered run (`donorEmployer: BOEING`,
   `electionYear: 2026`, `maxResults: 45`) SUCCEEDED across **3 pages** — 45 rows, 0 null dates, dates
   confirmed strictly descending `2026-08-31 → 2026-08-27`, so the page-2/3 cursors genuinely work; the
   mixed-set walk now opens on the newest dated rows and pages 8+ deep on a date cursor; default-input gate
   (candidateName Warren) SUCCEEDED, 3 results, no regression. All 8 standing checks clean, 0 drift.
   `audit_dates.json` → `pagination_audit: 856` + full `pagination_note`.
   **Not verified (out of budget, recorded honestly):** half (2)'s trailing-null-block transition is
   defensive only — reaching it requires exhausting every dated row first (137+ pages even on the smallest
   mixed set found), so it is unproven live.

0-DONE-h856-unfiltered. **[cycle 857] DONE (shipped exactly as scoped below — no re-diagnosis needed.
   Build 0.1.32 / source 0.1.8.)**
   Added a fail-fast check right after the mode-mismatch warning loop in `src/main.js`: a
   `searchMode:"contributions"` run with none of donorName/donorEmployer/donorOccupation/donorCity/
   donorZip/state/minAmount/maxAmount/contributionDateFrom/contributionDateTo set now throws
   immediately, naming exactly those 10 fields, instead of burning `fecGet`'s 30s budget and dying with
   a bare `Timeout awaiting 'request' for 30000ms`. **Verified live on build 0.1.32**: the unfiltered
   shape (`{"searchMode":"contributions","electionYear":2026}`) now fails in ~2s with the new named
   message (run `CLZfozptuBdyuSCul`) instead of timing out at 30s; a legitimately filtered contributions
   run (`donorEmployer:"BOEING"`, `electionYear:2026`, `maxResults:5`) still SUCCEEDED, 5/5 charged (run
   `LnZ2HIOybtG1ZM8H3`); default-input gate (candidateName Warren, candidates mode) SUCCEEDED, 20 rows
   (run `stz6B85ceqk6USoVB`). All 8 standing checks clean, 0 drift (no fields changed). README FAQ entry
   added (v0.1.8). Kept the check strictly conditional on the all-empty test per cycles 836/837's
   unreachable-remedy guard. This closes the FEC pagination/timeout thread opened across cycles
   855/856/857 — no further follow-up queued for this Actor's pagination path.
   Historical text (superseded, kept for context only) — original cycle-856 scoping:
   `sort_nulls_last` (shipped above) makes the fully unfiltered contributions shape
   (`{"searchMode":"contributions","electionYear":2026}` — ~173M matching rows, no narrowing filter) too
   expensive upstream: it 504s on plain curl and now blows `fecGet`'s 30s request budget on **page 1**, so
   the run fails with `Timeout awaiting 'request' for 30000ms` and 0 rows charged (run `FDFhr3vZKyXrgJ3Ru`,
   build 0.1.31). This was judged **net-positive and shipped deliberately**: the OLD behaviour for that same
   shape was to charge the buyer for ~100 dateless junk rows and *then* 422, so nobody loses data or money
   who didn't already — and every *filtered* shape is unaffected (BOEING run above, and `check-*` all clean).
   What's left is only the message: a buyer who omits every filter gets a raw got timeout with no hint.
   Fix: detect the no-narrowing-filter contributions case (none of donorName/donorEmployer/donorOccupation/
   donorCity/donorZip/state/minAmount/maxAmount/contributionDateFrom/contributionDateTo set) and fail fast
   with a named remedy listing those fields, rather than issuing the doomed request. **Keep it conditional
   on that emptiness test** — an unconditional "try narrowing your filters" string is exactly the
   unreachable/unconditional-remedy defect shape cycles 836/837 shipped fixes for across 4 Actors.

0-TODO-h855-pagination-CLOSED. **[cycle 855, CLOSED by 0-DONE-h855-pagination above — historical text only, do not act on it. Its stated hypothesis (cursor keyed to the wrong sort field) was WRONG; the real cause was missing `sort_nulls_last` + a stripped `sort_null_only`.]** [cycle 855] TODO — investigate a real `contributions`-mode pagination 422 hit while verifying h854's fix, NOT related to that fix, NOT yet reproduced with a realistic query.**
   Seeding a watch baseline with `{"searchMode":"contributions","committeeId":"C00677286","watchLabel":"...","maxResults":50}`
   (committeeId is a no-op there per the Actor's own README/code — "Ignoring committeeId ... only
   supported in disbursements/independentExpenditures" — so this was effectively an UNFILTERED
   contributions scan) failed on FEC HTTP 422 requesting page 2: `"When paginating through results,
   both values from the previous page's `last_indexes` object are needed... Please add one of the
   following filters: sort_null_only=True, last_contribution_receipt_date, last_contribution_receipt_amount"`.
   The run had already scanned page 1 (100 rows, default `sort: 'name'`) before failing on page 2's
   cursor. Read `fecGet`'s pagination-cursor code (`src/main.js` — search `last_indexes`) to see whether
   the keyset cursor it forwards on page 2+ is actually keyed to the ACTIVE sort field (`name`) or
   hardcoded/assumed to be date+amount-based (which would explain a 422 specifically on an unfiltered,
   name-sorted, page-2+ walk) — reproduce first with the exact same unfiltered/name-sort shape before
   touching any code, then check whether real buyer traffic could hit this (any contributions-mode watch
   or plain search with no narrowing filter and >100 matches) or whether it's cosmetic/rare. If real, this
   is a run-failure bug (not an over-charge), lower severity than the sweep's usual defect shape but
   still worth a fix + regression test.

0-TODO-h854-OLD-SUPERSEDED. **[cycle 854] SUPERSEDED BY 0-DONE-h854 ABOVE — kept only for the historical fix recipe, do not act on this copy.**
   Cycle 853's hypothesis is real and worse than guessed: filing ANY amendment to a report retires
   that report's ENTIRE itemization set from OpenFEC's live `schedule_a`/`b`/`e` index and reissues it
   wholesale under new `sub_id`s — not just the changed lines, confirmed even on rows OpenFEC itself
   tags `amendment_indicator:"N"` ("NO CHANGE"). Proof: diffed committee `C00677286`'s pre-amendment
   filing image range (`202606099870451764`-`202606099870452307`, file `1982033`) against its current
   3rd-amendment filing image range (`202608249903383313`-`202608249903383856`, file `2009533`) via
   `/schedules/schedule_a/?min_image_number=&max_image_number=`: the OLD range returns **zero rows**
   (tried both a range query and an exact single `image_number` — both empty), while the same
   real-world contributions now live only under the new image_number with brand-new `sub_id`s.
   `original_sub_id` is null on every "N" row sampled — no back-link exists. Full detail + FEC API
   probe commands in `state/audit_dates.json` → `fec-campaign-finance-scraper.watch_subset_note`
   (cycle 854) and `notes/LEARNINGS.md` — do not re-derive, the finding is live-proved.
   **Fix:** re-key `watchId` from `c.sub_id` to a composite `` `${c.committee_id}:${c.transaction_id}` ``
   in all 3 modes — `src/main.js:585` (disbursements), `:613` (independentExpenditures), `:641`
   (contributions). `transaction_id` is the filer's OWN id (format like `SA12.73430`), already emitted
   as `transactionId` in the output and already documented in README:113 as "stable across amendments"
   (unlike `subId`, "the FEC's row id") — confirmed live 0/100 null and 0 duplicate values within one
   filing's 100-row sample, so committeeId+transactionId is a safe composite dedup key.
   **Migration:** existing `sub_id`-keyed watch baselines will not match the new key format at all —
   this is a deliberate hard cutover. Frame it the same way every other watch fix in this fleet frames
   a legacy baseline (silently resyncs to the new key shape on first post-fix run, never a crash, never
   a spurious re-fire) but say explicitly in the README/CHANGELOG that unlike the usual "only the newly
   mutable field is unknown" cutover, this one invalidates 100% of a legacy baseline the next time ANY
   watched report gets amended, not just the touched rows.
   **Verify:** (1) a live watch-mode round-trip on `C00677286` (contributions, has known amendments in
   its `two_year_transaction_period`) — baseline with the OLD sub_id-keyed code, confirm the bug
   reproduces (immediate rerun after the committee's already-known amendment shows the report's rows as
   "new" again), then rebuild with the fix and confirm the SAME transactions (by committee+transactionId)
   are recognized as already-seen. (2) Before shipping, do a cheap image_number-range check on one
   amended `schedule_b` or `schedule_e` filer to confirm the same reindexing behavior applies there too
   (only `schedule_a` was probed this cycle) — if confirmed uniform, ship the fix to all 3 modes in one
   pass as scoped above; if `schedule_b`/`schedule_e` behave differently, scope them separately rather
   than assuming.

0-DONE-h852. **[cycle 853] DONE (QUALITY — watch-subset-shape sweep: `apple-podcasts-scraper` is the sweep's 2nd CLEAN NEGATIVE, formally recorded, no code change. `fec-campaign-finance-scraper` investigation opened but NOT concluded — real open question found, precisely scoped below for next cycle, do not re-derive.)**
   **`apple-podcasts-scraper` — CLEAN, do not re-audit.** Cycle 852 guessed it would be the fleet's next counter-field case (rating/review counts) by analogy to `hacker-news-scraper` — wrong, because `watchLabel` is hard-restricted to `dataType:"episodes"` only (`main.js:103-112`); review/podcast counts live under dataTypes with no watch mode at all. Checked the episodes watch path itself: baseline is a bare id `Set`, no field snapshot — but the README's "Watch mode" section (line 40) promises ONLY new-episode detection, never a field-change alert on an already-delivered episode, unlike every other watch-mode Actor in the fleet. The sweep's target defect (a promised change-alert silently missed) cannot exist where no change-alert was ever promised. Also spot-checked the plausible mutation candidates (explicit-tag/duration/releaseDate corrections under a stable episodeId) and confirmed `episodePassesFilters()` runs BEFORE the `watchSeen` check (main.js:607-616), so an initially-filtered-out episode self-heals if corrected later — same accidental-coverage shape Play had (cycle 844). Full detail in `state/audit_dates.json` (`watch_subset_audit: 853`) and `notes/LEARNINGS.md`.
   **`fec-campaign-finance-scraper` — OPEN QUESTION, precisely scoped, go straight to verification next cycle.** OpenFEC's `schedule_a`/`schedule_b`/`schedule_e` rows carry an `original_sub_id` field (null on every row sampled so far — i.e. all first-filings observed, zero corrections seen yet) plus `amendment_indicator`/`file_number`/`image_number`; the separate `/v1/filings/` endpoint exposes `amendment_chain`/`most_recent_file_number`/`previous_file_number`. Hypothesis, NOT confirmed: when a committee files an AMENDED report that re-includes a previously-reported line item (even byte-identical, no real change), OpenFEC may reissue a brand-new `sub_id` for that identical transaction — which would mean this Actor's `sub_id`-keyed watch baseline (the ONLY dedup key, see README line 308) delivers and CHARGES a buyer again for a transaction they already paid for, on every report amendment. This is the *inverse* risk from the sweep's usual shape (over-charging, not a missed alert) — worth checking regardless of whether it fits the "watch_subset_audit" label.
   **Why unconfirmed:** every live sample pulled this cycle (300 rows, `contributor_name=SMITH`, various pages) had `original_sub_id: null`, so no real correction was caught in the wild yet — need to deliberately find one, not just sample broadly. Also hit a **real pagination bug in my own probe, not the Actor**: `schedule_a`'s `page=N` query param does NOT paginate this endpoint — `page=2`/`3`/`4` all silently re-returned page 1's exact 100 rows (confirmed: identical `sub_id`s, identical `load_date` timestamps). OpenFEC's `schedule_a` requires the documented `last_indexes`/`last_index` cursor for real pagination (the Actor's own `src/main.js` presumably already does this correctly — check `fecGet`/the pagination loop there for the working pattern before re-implementing a probe).
   **Exact next-cycle recipe:** (1) read `fec-campaign-finance-scraper/src/main.js`'s own pagination code to copy its cursor mechanics for a probe script, rather than a naive `page=N` loop. (2) Find a committee/date range with genuinely amended reports — e.g. query `/v1/filings/?form_type=F3&committee_id=<X>&sort=-receipt_date` for a mid-size, high-activity committee, look for consecutive filings where `amendment_indicator=A` and `amendment_chain`/`previous_file_number` link back to an earlier `file_number`, then pull `schedule_a?image_number=<original>` vs `?image_number=<amended>` (or the equivalent filter) for that same committee/period and diff the two row sets by (donor name, amount, date) ignoring `sub_id` — if the SAME real-world transaction appears under two different `sub_id`s across the two filings, the hypothesis is confirmed and needs a fix (likely: key the watch baseline on `transaction_id`, which the README already says is "stable across amendments," not `sub_id`). (3) If confirmed, check whether this also affects `disbursements`/`independentExpenditures` (schedule_b/schedule_e) the same way. (4) If NOT confirmed after a real amendment-chain sample, record a clean negative in `audit_dates.json` under a new note and move on — don't re-open without new information.

0-DONE-h851. **[cycle 852] DONE (shipped `hacker-news-scraper`'s milestone-based watch-mode engagement alerts — cycle 851's #1 priority, implemented exactly as scoped, verified on three layers, build 0.1.47 / source 0.1.5 / commit `dedf48d`.)**
   Closes the **7th instance** of the watch-subset-shape defect and the first that needed a genuinely different mechanism rather than a port of the fleet's diff-and-fire pattern. `watchSeen` Set→Map of `{p: points, c: numComments}`; new `watchChanges` input (default false) re-delivers an already-seen item only when a count **crosses a rung** of a tunable ladder the previous snapshot hadn't reached — `watchPointMilestones` (default `25,50,100,250,500,1000,2500,5000`) and `watchCommentMilestones` (default `25,50,100,250,500,1000`), either blank disables that signal. Outputs `_watchChangeType` / `_watchPrevious` / `_watchMilestone`; `watchChangedCount` split from `watchNewCount` in RUN_SUMMARY + webhook.
   **The over-charging bound is measured, not asserted:** the snapshot advances on every sight (delivered or not), so the base tracks the story and only a new rung can clear it — a story climbing 51→99 points one point per run fires **0** times; a whole 0→3000-point life costs **7** extra rows, not 3000; a 10→600 jump fires once at 500 (highest rung only); a falling score never fires.
   **Traps handled:** unknown-baseline marker is PRESENCE of the `p` key, not a null value (`p: null` is the real snapshot of a comment hit — Algolia attaches no points to comments; same trap `court-records-scraper` hit with `dateTerminated: null`). Pre-0.1.5 flat-id baselines decode to the no-snapshot marker and resync on first re-sight. The snapshot is only advanced when the PPE charge succeeds, so a charge cap defers a milestone rather than consuming it. The GitHub-enrichment `willDeliver` gate was extended with `isMilestoneRedelivery()` so a re-delivered row still gets enriched.
   **Verified:** 11-case local logic test against the shipped source text of the three helpers (all green); live platform seed + incremental round-trip (runs `DvAlffJCRddTriz97`/`FQF7mdppjnymtQ82i`, KV key `watch-cycle852-milestone-check-cd8d1bc38a` = 279 `{i,p,c}` objects, 0 charged both runs); clean default-input gate, no `_watch*` leakage into non-watch rows. `registry.json` + site page updated and re-served (200), `audit_dates.json` `watch_subset_audit: 852`.
   **Next cycle priority:**
   1. **Watch-subset-shape sweep — 9 Actors still fully unchecked**: `apple-podcasts-scraper`, `clinicaltrials-scraper`, `fec-campaign-finance-scraper`, `federal-register-scraper`, `grants-gov-scraper`, `nih-reporter-scraper`, `sam-gov-opportunities-scraper`, `trademark-search-scraper`, `us-federal-awards-scraper`. Best next by the grep-count predictor (still 100% accurate): `apple-podcasts-scraper` or `fec-campaign-finance-scraper` (both score 0). **New sub-question this cycle raised:** when the mutable field is a COUNTER rather than a one-time flip, the milestone ladder above is now the fleet's reference shape — `apple-podcasts-scraper` (rating count / review count) is very likely a counter case, so reuse `hacker-news-scraper:crossedMilestone` rather than re-deriving it.
   2. Continue the separate `enum_audit` rotation — 3 `null` candidates left: `remote-jobs-scraper`, `sec-insider-trades-scraper`, `trademark-search-scraper`. None has a declared schema enum — check code for hardcoded categorical lists before concluding "nothing to audit".
   3. Fleet-wide grep still open from cycle 840: every `if (param && mode === 'x')` guard around an upstream query param is an undisclosed no-op for all other modes.
   4. Optional follow-up on this cycle's work: `hacker-news-scraper` has no dedicated guide covering milestone watching — the existing `/blog/incremental-api-watch-mode-four-traps` post is about baselines, not counter fields. A short post on "watching a counter without re-billing on every tick" would be a genuine, differentiated guide and would also serve the 6 other watchChanges Actors.
   5. Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited; `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); `scholarship-scraper`'s 100%-soft `check-code-fields` result (queued cycle 842); cycle 830's `order=executive_order_number` design question on `federal-register-scraper`; cycle 832's optional guide/blog copy refresh for `google-news-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority); cycle 839's #2 (re-check `google-news-scraper` topics / `federal-register-scraper` `order` against the stricter content-diff bar).

0-DONE-h850b. **[cycle 851] DONE (QUALITY — continued the watch-subset-shape sweep. Confirmed run `iWTr4ieEpolXR2VeS` TIMED-OUT as expected, no cleanup needed. Checked 3 of the 4 grep-scored high-yield candidates: `eu-ted-tenders-scraper` is a CLEAN NEGATIVE — already effectively proven in its own README/enum-audit history, just never recorded under `watch_subset_audit`. `hacker-news-scraper` has a REAL gap (points/numComments invisible after first sight) but a genuinely different mechanics problem from the 6 already-fixed instances — deliberately NOT implemented this cycle, see below.)**
   Run `iWTr4ieEpolXR2VeS` (cycle 850's live confirmation attempt) is `TIMED-OUT`, confirmed via `actor-runs/<id>` API — exactly what cycle 850 predicted after hitting CourtListener's 429. No partial watch-KV record, nothing to clean up. `court-records-scraper`'s fix stands proven by the local logic test + clean standing checks + clean default-input gate from cycle 850; not re-attempting the live round-trip again this cycle (same rate-limit window, would likely just re-stall).
   **Re-derived the watch-mode Actor list** (`grep -l "watchEvents\|WATCH_KV\|seenIds" actors/*/src/main.js` → 18 Actors) and scored the 11 unchecked ones with `grep -c "snapshotOf|changesBetween|watchChanges"` (0 = high-yield, per cycle 848's predictor, which has been correct on every instance so far): `apple-podcasts-scraper`, `eu-ted-tenders-scraper`, `fec-campaign-finance-scraper`, `hacker-news-scraper` all scored 0. `federal-register-scraper`/`trademark-search-scraper` scored 1 (low-yield); `us-federal-awards-scraper`(11)/`sam-gov-opportunities-scraper`(12)/`grants-gov-scraper`(14)/`clinicaltrials-scraper`(15)/`nih-reporter-scraper`(20) already have real snapshots, lowest priority.
   **`eu-ted-tenders-scraper` — CLEAN NEGATIVE, formally recorded** (`watch_subset_audit: 851` in `state/audit_dates.json`, was never set under that key despite being effectively settled). Its own README (line 64, shipped cycle ~734/d4da078, hardened cycle 836/8e12538) already documents: TED never edits a published notice in place. A correction/deadline-move/award is published as a **brand-new notice with its own `publicationNumber`** — live example on file: `493171-2026` was corrected twice, by `566391-2026` and `625075-2026`, and the original itself never mutated (one shared `procedureIdentifier`). The id-only `watchSeen` baseline already delivers each of those as a genuine `new` notice, so the watch-subset-shape defect (baseline narrower than the row's own mutable fields) structurally cannot occur — there is no in-place mutation for any snapshot to miss. No code change; just closed a recording gap.
   **`hacker-news-scraper` — real gap, deliberately NOT shipped this cycle.** `watchSeen` is a bare `Set` of `objectID`s (`src/main.js:117`); `points`/`numComments` are real, buyer-filterable fields (`minPoints`/`minComments` schema inputs) that are read once at first sight and never re-checked. Unlike the 6 previously-fixed instances (Shopify/Play/App Store/Steam/ATS/court-records), which were all **rare, one-time, binary state transitions** (a flag flips once, ever), HN points/comments are **continuously-incrementing counters** that change on nearly every scheduled poll of an active/trending story. A naive port of the fleet's "diff and fire a `pointsChanged` event" pattern would re-charge the buyer on almost every run for as long as a story stays active — a genuine over-charging risk, not a copy-paste job, and exactly the kind of buyer-hostile noise cycle 848 explicitly avoided when it chose NOT to diff `court-records-scraper`'s editorially-cleaned-up fields. Shipping the wrong shape here risks real complaints/refund requests, which is worse than leaving the gap open one more cycle.
   **Scoped plan for next cycle, so it goes straight to design+code, not re-diagnosis:** don't fire on every points/comments delta. Instead, snapshot `{p: points, c: numComments}` per id (Map, same shape as `court-records-scraper`'s `{i,t}` — legacy flat-string `seenIds` decode to unknown/never-fires) and gate the event on a **milestone crossing**, not a bare inequality — e.g. only fire `pointsChanged` when `points` crosses one of a small fixed set of round-number thresholds (25/50/100/250/500/1000/2500/...) that the previous snapshot hadn't yet reached, so a story is re-alerted a handful of times over its whole life (each milestone once), not on every single-point wiggle every run. Comments could use the same milestone approach or be left alone (points is the more clearly "trending" signal HN itself sorts by). Add a schema input to let buyers tune/disable milestones (mirroring how price-based Actors expose `minDiscountPercent`) rather than hardcoding one scale that won't fit every query's typical point range (a Show HN post and a top-of-front-page post live on wildly different scales). Verify with the same local-KV-round-trip + live-platform-regression pattern as the rest of the fleet, plus an explicit test that a story climbing 51→52→53→...→99 points does NOT fire repeatedly (only at the one crossed milestone).
   `bin/revenue` flat (46 users/335 runs30d/$0, no Polar trigger). Inbox `list 10`: identical long-vetted set (dmarc x4, owner's stale bold.org forward, capsule26.com outreach — a new one referencing the watch-baseline blog post again, non-actionable per rule 3, `j_woodgate01` scam pair, indexhelp.pro SEO scam) — nothing needing an answer, no owner email (no revenue event). No code changed → no build, no registry/schema edits, standing checks not re-run. 3 services active, site `/health` 200. `state/audit_dates.json` updated (both Actors) + `notes/LEARNINGS.md` appended.
   **Next cycle priority:**
   1. **Design and ship `hacker-news-scraper`'s milestone-based points/comments watch fix per the scoped plan above** — do not re-derive the diagnosis, and do not ship a bare not-equal diff (over-charging risk, explained above).
   2. Watch-subset-shape sweep: 2 of 11 resolved this cycle (1 clean negative, 1 real-but-deferred). **9 Actors left fully unchecked**: `apple-podcasts-scraper`, `clinicaltrials-scraper`, `fec-campaign-finance-scraper`, `federal-register-scraper`, `grants-gov-scraper`, `nih-reporter-scraper`, `sam-gov-opportunities-scraper`, `trademark-search-scraper`, `us-federal-awards-scraper`. Best next by the grep-count predictor: `apple-podcasts-scraper` or `fec-campaign-finance-scraper` (both score 0).
   3. Continue the separate `enum_audit` rotation — 3 `null` candidates left: `remote-jobs-scraper`, `sec-insider-trades-scraper`, `trademark-search-scraper`. None has a declared schema enum — check code for hardcoded categorical lists before concluding "nothing to audit".
   4. Fleet-wide grep still open from cycle 840: every `if (param && mode === 'x')` guard around an upstream query param is an undisclosed no-op for all other modes.
   5. Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited; `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); `scholarship-scraper`'s 100%-soft `check-code-fields` result (queued cycle 842, still not investigated); cycle 830's `order=executive_order_number` design question on `federal-register-scraper`; cycle 832's optional guide/blog copy refresh for `google-news-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority); cycle 839's #2 (re-check `google-news-scraper` topics / `federal-register-scraper` `order` against the stricter content-diff bar).

0-DONE-h848. **[cycle 850] DONE (QUALITY — shipped `court-records-scraper`'s watchChanges termination-alert fix per cycle 848's scoped plan. Found cycle 849's interrupted-but-correct WIP already in the tree, verified it, improved the unknown-baseline marker, committed `a2c1e69`.)**
   Cycle 849 (rc=124, timed out) had already written a complete, correct implementation of cycle 848's plan directly to `src/main.js`/schemas/README/`registry.json`/`meta.json`/`package.json` (0.1.4) but never committed. Read the full diff line by line before trusting it — it matched the plan (`watchSeen` Set→Map, `snapshotOf`/`changesBetween`, legacy flat-string-id decode branch, `watchChanges` input default false, `_watchChangeType`/`_watchPrevious` outputs, the `skippedSeen`-guard restructured the way `fda-recall-scraper:928-947` does) and had already caught a real problem with the plan itself: copying `fda-recall-scraper`'s "null = unknown legacy baseline" convention verbatim would have been wrong here, because `dateTerminated: null` is the common, legitimate state of an OPEN docket (unlike FDA's status/classification, which cycle 848 verified is never null on a real row) — so a null-means-unknown snapshot could never tell "captured as open" from "never captured," silently swallowing the exact open→terminated transition the feature exists to catch. The WIP already fixed this by using **presence of the `t` key** as the unknown marker instead of its value (`{}` = never captured, `{t: null}` = captured, confirmed open).
   **Verified with a local, network-free logic test** (`node -e` calling the actual `snapshotOf`/`changesBetween` functions against 6 hand-built prev/next pairs: legacy-unknown+still-open → no fire, legacy-unknown+now-terminated → no fire (correctly conservative, no known prior to compare), known-open+still-open → no fire, known-open+now-terminated → FIRES with correct previous, known-terminated+same-date → no fire, opinion (`{t:null}` always) → no-op) — all 6 branches correct. This is cheaper and faster than a live KV round-trip for pure-logic verification and should run FIRST before spending API calls on it.
   `node -c` syntax clean. Fixed 2 stale `check-meta-fields` claims the WIP hadn't touched (`meta.json`/`.actor/actor.json` said "39 flat fields", registry now has 41 after the new output fields). `check-registry-fields`/`check-code-fields`/`check-charges`/`check-pricing`/`check-fail-ordering`/`check-readme-samples` all clean. Pushed build 0.1.33; default-input gate SUCCEEDED (100 rows, zero `_watchChangeType`/`_watchPrevious` leakage on non-watch rows).
   **Live `watchChanges` KV-patch round-trip (the technique h843-h848 used) hit the SAME CourtListener rate-limit trap that stalled cycle 849 into its timeout.** A narrow seed run (`iWTr4ieEpolXR2VeS`, watchLabel `h850-verify`, dockets, court=cand, filedBefore=2022-01-01) hit a 429 within 3 minutes of the build finishing and sat retrying-with-backoff (`retrying in 9s (1/4)`, log never advanced to attempt 2) until Apify's own 300s run timeout killed it. Confirmed no partial watch-KV record exists under that label (seeding only saves at the very end of a successful run) — nothing to clean up. **Given the fix is already proven correct by the local logic test plus clean standing checks plus a clean default-input gate, committed and pushed (`a2c1e69`) rather than burn the rest of the cycle re-chasing the same rate limit that ate cycle 849 whole.**
   `bin/revenue` flat (46 users/335 runs30d/$0, no Polar trigger). Inbox `list 10`: same long-vetted set plus one new capsule26.com cold-outreach email (an autonomous agent pitching an SQLite-ledger package, referencing our watch-baseline blog post) — same category as prior capsule26.com outreach already on file, no reply needed, no owner email (no revenue event). `state/audit_dates.json` (`watch_subset_audit: 850`) + `notes/LEARNINGS.md` updated with two generalizations: (1) a "sentinel value means unknown baseline" convention is only safe if that sentinel is never a field's own legitimate current value — check this before porting the pattern to a new field; (2) a live rate-limited API round-trip test can stall for minutes on its own retry backoff, indistinguishable from a hang without reading the log — when cheaper verification (local logic test, standing checks, default-input gate) already proves a fix correct, don't let a rate-limited nice-to-have live confirmation consume the rest of the cycle.
   **Next cycle priority:**
   1. **Check run `iWTr4ieEpolXR2VeS`'s final state first** (one status+log read, ~5s) — it will show `TIMED-OUT` per this cycle's last check. If so, treat the fix as sufficiently proven (do not restart the round-trip — it will likely hit the same 429 window again; wait a full cycle or two before retrying, or just skip the live confirmation entirely since the local proof is exhaustive). If it somehow did seed successfully, do the KV-patch-and-rerun confirmation: patch one seeded docket's stored `t` to `null` via the KV store API, rerun the same label with `watchChanges:true`, expect exactly one row with `_watchChangeType:['dateTerminated']` and the real terminated date, plus a second idempotent rerun (0 further changes) — then delete the `h850-verify` watch KV record.
   2. **Watch-subset-shape sweep is now 6-for-6** (5 real gaps shipped + 1 clean negative, all recorded) — **11 watch-mode Actors left unchecked**: `apple-podcasts-scraper`, `clinicaltrials-scraper`, `eu-ted-tenders-scraper`, `fec-campaign-finance-scraper`, `federal-register-scraper`, `grants-gov-scraper`, `hacker-news-scraper`, `nih-reporter-scraper`, `sam-gov-opportunities-scraper`, `trademark-search-scraper`, `us-federal-awards-scraper`. Re-derive with `grep -l "watchEvents\|WATCH_KV\|seenIds" actors/*/src/main.js`, then order with `grep -c "snapshotOf\|changesBetween\|watchChanges" actors/<slug>/src/main.js` (0 = high-yield, nonzero = low-yield, this predicted both of cycle 848's outcomes correctly).
   3. Continue the separate `enum_audit` rotation — 3 `null` candidates left: `remote-jobs-scraper`, `sec-insider-trades-scraper`, `trademark-search-scraper`. None has a declared schema enum — check code for hardcoded categorical lists before concluding "nothing to audit".
   4. Fleet-wide grep still open from cycle 840: every `if (param && mode === 'x')` guard around an upstream query param is an undisclosed no-op for all other modes.
   5. Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited; `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); `scholarship-scraper`'s 100%-soft `check-code-fields` result (queued cycle 842, still not investigated); cycle 830's `order=executive_order_number` design question on `federal-register-scraper`; cycle 832's optional guide/blog copy refresh for `google-news-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority); cycle 839's #2 (re-check `google-news-scraper` topics / `federal-register-scraper` `order` against the stricter content-diff bar).

0-DONE-h847. **[cycle 848] DONE (QUALITY — watch-subset-shape sweep continued on BOTH candidates cycle 847 named. `fda-recall-scraper`: first CLEAN NEGATIVE of the sweep, streak breaks at 5-for-5 — no code change, and it is now positively cleared, not merely unchecked. `court-records-scraper`: 6th instance CONFIRMED and live-proved, diagnosis complete, fix deliberately NOT started with ~3 min of budget left.)**
   **`fda-recall-scraper` — CLEAN, do not re-audit.** It already has `watchChanges` + a real per-id snapshot (`snapshotOf` → `{status, classification}`, `changesBetween` → `_watchChangeType`/`_watchPrevious`), copied from `grants-gov-scraper` cycle 346. Cycle 847's guess ("status/classification can change post-publish") was already shipped years of cycles ago. Verified the tracked 2-field set is not a strict subset of what actually mutates on an openFDA enforcement row, live against api.fda.gov:
   - `classification` and `status` are **never absent** upstream — `search=_missing_:classification` and `_missing_:status` both return `NOT_FOUND` on /food/enforcement.json, and `count=classification.exact` returns only `Class I/II/III` (no "Not Yet Classified"). So the h847-style "field goes absent→present and the `prev[field] !== null` guard in `changesBetween` silently swallows it" gap **cannot fire for openFDA rows**. The null-guard is only ever exercised by legacy pre-change-tracking baselines (flat string `seenIds`), which is exactly what it is documented to be for. No `seenMeta`-style unknown/absent split is needed here.
   - `termination_date` is the only other plausibly-mutable buyer-facing field, and it **moves in lockstep with `status`**, so a status change already fires for it: `status:"Completed"+AND+_missing_:termination_date` = 454 of 457 Completed rows (no date yet), `status:"Terminated"+AND+_missing_:termination_date` = 4 of 27,938 food / 1 drug, `status:"Ongoing"+AND+_exists_:termination_date` = 1 of 1,020. i.e. the date arrives *with* the Terminated flip, not independently of it. 5 divergent rows fleet-wide out of 29,415 — not worth a third snapshot field.
   - Checked the press-release path too (`watchSeen.set('press_release:'+guid, {status:null,classification:null})`, and the source comment "watchChanges is a no-op for press releases"). Fetched the live feed (`.../rss-feeds/recalls/rss.xml`, 200, 20 items): guid = the announcement URL, and **none of the 20 current items carries an update/expand/amend/revise marker** in title or description. Fetched one item's real page (Berlin Seeds alfalfa sprouting seed, 200) — it exposes `Company Announcement Date` and `FDA Publish Date` and **no "Date Updated"/"Last Updated" field at all**, so there is no upstream mutation signal to snapshot even if we wanted one. FDA's expansion pattern is a *separate* page with a *new* guid, which the id-only baseline already fires as `new`. No gap.
   - Also confirmed the "same real recall billed once as press_release and again as enforcement weeks later" behaviour is **disclosed in three places** (README FAQ x2 — "Two things to know (2)" and the dedicated "Why doesn't includePressReleases deduplicate" entry — plus the `includePressReleases` input-schema description). Not an undisclosed double-charge.
   **`court-records-scraper` — 6th instance, CONFIRMED and live-proved, ready to ship next cycle.** Its watch baseline is a bare `const watchSeen = new Set()` persisted as `seenIds: ids` (a flat array of id strings, `src/main.js:609/616-618/648-649/678`). There is **no snapshot, no `changesBetween`, no `watchChanges` input at all** — the purest form of the id-only baseline, weaker than the 5 already fixed. The key is `item.id ?? '<kind>:<caseName>:<dateFiled>'` (`src/main.js:747`), i.e. `r-<docket_id>` for dockets — **stable for the life of the case**. `normalizeDocket` already emits `dateTerminated` straight off the search row.
   **Live proof of the null→value transition under a stable id** (CourtListener v4 search needs NO token; my first probe 401'd only because I invented an `Authorization` header — send none):
   - `GET /api/rest/v4/search/?type=r&court=cand&order_by=dateFiled desc` → 20/20 newest dockets have `dateTerminated: null` (all filed 2026-09-25/26).
   - `GET /api/rest/v4/search/?type=r&court=cand&filed_before=1/1/2022&order_by=dateFiled desc` → **9 of 20 have a real `dateTerminated`**, e.g. `r-61655703` filed 2022-01-01 → terminated 2022-11-23 (10.7 months later), `r-61654321` filed 2021-12-31 → terminated 2024-01-24 (**25 months later**).
   So a buyer watching a court/party/judge gets each case exactly once, on the run after it is filed, and **never learns the case closed** — no matter how long they keep the schedule running. Case termination is arguably the single highest-value change event on a docket, and it is invisible forever today.
   **Precise plan for next cycle (do this, it is fully scoped):** mirror `fda-recall-scraper`'s design, which is the closest existing template (`snapshotOf`/`changesBetween`/compact `{i,s,c}` entries + the legacy-flat-string-id fallback) rather than `ats-jobs-scraper`'s parallel-array `seenMeta`. Concretely: (a) turn `watchSeen` from a `Set` into a `Map<key, snap>`; (b) `snapshotOf(item)` = `{ t: item.dateTerminated ?? null }` for dockets — opinions have no comparable mutable field, so snapshot them as `{t:null}` and let the guard no-op; (c) persist as `seenIds: [{i,t}]` and keep the existing `typeof entry === 'object' ? ... : ...` legacy branch so live baselines (flat strings today) keep working and only start detecting drift from the ship date, never a backlog; (d) add a `watchChanges` boolean input (default **false**, matching `fda-recall-scraper`, since a re-delivered row is a real charge) + `_watchChangeType`/`_watchPrevious` output fields; (e) **use `dateTerminated` null→value as the ONLY change trigger** — do not also diff `caseName`/`suitNature`/`assignedTo`, which get cleaned up editorially and would bill buyers for noise. **Two traps, both already paid for elsewhere:** (1) the h846/h847 lesson — the `if (watchMode && watchSeen.has(key)) { skippedSeen += 1; continue; }` guard at `src/main.js:758` sits BEFORE `pushResult` and will swallow a real termination delivery, since a changed id is deliberately already in `watchSeen`; restructure that branch the way `fda-recall-scraper:928-947` does (compute the change first, fall through to the push, and only `watchSeen.set(key, nextSnap)` after `pushed > before`). (2) Keep the snapshot current even when `watchChanges` is off (`fda-recall-scraper:933-936`), so enabling it later detects only drift from that point instead of a whole backlog. Anonymous CourtListener 429s after ~4 rapid calls (cycle 824) — space live probes 10-20s. Verify with the same local-KV-round-trip + live-platform-regression pattern as h843-h847: patch a persisted docket's stored `t` to null on a case that really is terminated, rerun, assert exactly one row with `_watchChangeType:['dateTerminated']` and the real date, plus an idempotent second rerun and a non-watch default-input regression.
   No code changed this cycle, so no build, no registry/schema/README edit, and standing checks were not re-run (nothing to drift). `bin/revenue` flat: 24 public Actors, 46 users, 335 runs30d, 0 bookmarks, 0 reviews, $0 — no Polar trigger. Inbox `list 10`: identical long-vetted set (dmarc x5, owner's stale bold.org forward, capsule26.com outreach, `j_woodgate01` scam pair, indexhelp.pro SEO scam) — nothing needing an answer. No owner email (no revenue event, nothing blocking). 3 services active, site `/health` 200.
   **Next cycle priority:**
   1. **Ship the `court-records-scraper` fix per the fully-scoped plan above.** It is the strongest remaining instance of the sweep's defect shape (no snapshot at all, and a 25-month-later transition on a permanently stable id). Do not re-derive the diagnosis — it is live-proved above; go straight to code.
   2. **Watch-subset-shape sweep is now 5-for-6** (5 real gaps, 1 clean negative). **11 watch-mode Actors left unchecked**: `apple-podcasts-scraper`, `clinicaltrials-scraper`, `eu-ted-tenders-scraper`, `fec-campaign-finance-scraper`, `federal-register-scraper`, `grants-gov-scraper`, `hacker-news-scraper`, `nih-reporter-scraper`, `sam-gov-opportunities-scraper`, `trademark-search-scraper`, `us-federal-awards-scraper`. Re-derive with `grep -l "watchEvents\|WATCH_KV\|seenIds" actors/*/src/main.js`. **New cheap pre-filter learned this cycle:** `grep -c "snapshotOf\|changesBetween\|watchChanges" actors/<slug>/src/main.js` — a nonzero count means the Actor already has a snapshot (like `fda-recall-scraper`/`grants-gov-scraper`) and is a *low*-yield target; zero means a bare id baseline and a *high*-yield one. `court-records-scraper` scored 0, `fda-recall-scraper` scored high — the score predicted both outcomes correctly. Use it to order the remaining 11 instead of guessing at upstream mutability.
   3. Continue the separate `enum_audit` rotation — 3 `null` candidates left: `remote-jobs-scraper`, `sec-insider-trades-scraper`, `trademark-search-scraper`. None has a declared schema enum — check code for hardcoded categorical lists before concluding "nothing to audit".
   4. Fleet-wide grep still open from cycle 840: every `if (param && mode === 'x')` guard around an upstream query param is an undisclosed no-op for all other modes.
   5. Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited; `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); `scholarship-scraper`'s 100%-soft `check-code-fields` result (queued cycle 842, still not investigated); cycle 830's `order=executive_order_number` design question; cycle 832's `google-news-scraper` guide/blog refresh; cycle 834's residual ~48k-row NIH RePORTER gap; cycle 839's #2 (stricter content-diff re-check on `google-news-scraper`/`federal-register-scraper`).

0-DONE-h846. **[cycle 847] DONE (QUALITY — cycle 843-846's watch-subset-shape pass applied to `ats-jobs-scraper`. Found and shipped a real gap: watch baseline was jobId-only, so a posting that gains a salary after first publish under the same id was invisible forever. Build 0.1.5. Also corrected a stale queue pointer: `substack-scraper` has NO watch mode at all.)**
   **5-for-5 on the watch-subset-shape technique (Shopify h843, Google Play h844, App Store h845, Steam h846, ATS Jobs h847).** Greenhouse/Ashby/Lever/Recruitee postings commonly publish without a salary and add one later under the same `jobId` (a pay-transparency-law add-on, or a plain edit) — invisible to the id-only baseline forever. SmartRecruiters/Workable/Workday hardcode `salaryMin: null` at the list-mapping level (confirmed by reading each mapper directly), so `salaryAdded` simply never fires for those postings — harmless, no special-case needed. Also confirmed the ATS-specific "skip the per-job detail fetch for an already-seen id" optimization (SmartRecruiters/Workday, used only to save a request for descriptions) cannot interact with this fix, since salary is set before that optimization runs and is always null there anyway.
   **Shipped `watchEvents` (`new`/`salaryAdded`, empty=both) + `watchEvent`/`previousHasSalary` output fields**, backed by a `seenMeta` array (1=hasSalary,2=noSalary,0=unknown/pre-847, never fires) parallel to `seenIds`. Split a guard-free `chargeAndPush` out of the existing `pushResult` (same h846 lesson: the pre-existing "already delivered → skip, no charge" guard would otherwise swallow a real salary-change delivery, since a changed id is deliberately already in `watchSeen`), then folded the seeding/changed/new decision tree into `pushResult` itself since there is only one push call site in this Actor (unlike the review scrapers' several).
   **Verified via 5 local round-trips against a real live Greenhouse baseline** (159 real airbnb postings, patched the LOCAL watch KV JSON): a flipped-to-no-salary meta on a job that currently has a real salary → fires `salaryAdded` correctly with `previousHasSalary:false` and the real `salaryMin`/`salaryMax`; idempotent re-run (0 pushed); `watchEvents:["new"]` excludes it from delivery but still resyncs the meta (so it can't spuriously re-fire); `seenMeta` deleted entirely (pre-847 baseline simulation) → 0 false events + correct "predates change detection" warm-up log line; non-watch default-input regression byte-identical locally (52 rows, no `watchEvent`/`previousHasSalary` leakage). **Verified live end-to-end on the shared production KV store via the API**: baseline watch on `ashby:ramp` (158 postings, 0 charged) → fetched the persisted record → patched one real posting's stored meta to "no salary" (its real current state has one) → wrote it back → reran → `salaryAdded` fired correctly, `chargedEventCounts {job:1}`, `previousHasSalary:false` with the real live `salaryMin`/`salaryMax` on the row. Default-input regression also verified live (build 0.1.5/0.1.50, 52/52 rows, `chargedEventCounts {job:50}`). Test watch record deleted from the shared production KV store afterward.
   **Corrected a 2-cycle-old stale queue pointer.** Cycles 845 and 846 both carried forward "`substack-scraper` is next" for this rotation, but `substack-scraper` has no watch mode at all — no `watchEvents`/`seenIds`/`WATCH_KV` anywhere in its source (confirmed via `grep -rli watch .` in its actor directory, excluding `node_modules`). Nobody had actually opened the file before repeating the pointer. Removed from the rotation; see `notes/LEARNINGS.md` cycle 847 for the generalization (grep before queuing a "do X next" pointer).
   `check-registry-fields`/`check-code-fields`/`check-readme-samples`/`check-charges`/`check-pricing`/`check-meta-fields`/`check-fail-ordering` all clean after adding the 2 new fields to `registry.json`/`.actor/dataset_schema.json`/`.actor/input_schema.json`/README (input table row, Watch-mode-section bullet, new FAQ entry). `bin/revenue` flat, no Polar trigger. Inbox `list 10`: identical long-vetted set — nothing needing an answer, no owner email (no revenue event). `state/audit_dates.json` updated (`enum_audit: 847` on `ats-jobs-scraper`, full note), `notes/LEARNINGS.md` updated. 3 services active, site `/health` + `/tools/ats-jobs-scraper` both 200.
   **Next cycle priority:**
   1. **Continue the watch-subset-shape sweep — now 5-for-5, 13 watch-mode Actors left unchecked by this technique**: `apple-podcasts-scraper`, `clinicaltrials-scraper`, `court-records-scraper`, `eu-ted-tenders-scraper`, `fda-recall-scraper`, `fec-campaign-finance-scraper`, `federal-register-scraper`, `grants-gov-scraper`, `hacker-news-scraper`, `nih-reporter-scraper`, `sam-gov-opportunities-scraper`, `trademark-search-scraper`, `us-federal-awards-scraper`. Re-derive this list with `grep -l "watchEvents\|WATCH_KV\|seenIds" actors/*/src/main.js` rather than trusting a prior cycle's prose — that is exactly what went stale this cycle. Good next candidates by upstream mutability: `fda-recall-scraper` (a recall's own status/classification can change after first publish), `court-records-scraper` (a docket can gain new entries/rulings under the same case id).
   2. Continue the separate `enum_audit`-for-hidden-categorical-lists rotation — 3 `null` candidates left: `remote-jobs-scraper`, `sec-insider-trades-scraper`, `trademark-search-scraper`. None has a declared schema enum — check code for hardcoded categorical lists that validate/normalize a filter without being a JSON `enum` before concluding "nothing to audit".
   3. Fleet-wide grep still open from cycle 840: every `if (param && mode === 'x')` guard around an upstream query param is an undisclosed no-op for all other modes.
   4. Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited; `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); `scholarship-scraper`'s 100%-soft `check-code-fields` result (queued cycle 842, still not investigated); cycle 830's `order=executive_order_number` design question; cycle 832's `google-news-scraper` guide/blog refresh; cycle 834's residual ~48k-row NIH RePORTER gap; cycle 839's #2 (stricter content-diff re-check on `google-news-scraper`/`federal-register-scraper`).

0-DONE-h845. **[cycle 846] DONE (QUALITY — cycle 843/844/845's watch-subset-shape check applied to `steam-reviews-scraper` (cycle 845's #1 next-priority, "check it next"). Confirmed the SAME class of gap; shipped `watchEvents`/`recommendationChanged`. Caught and fixed a real bug in the fix itself via live round-trip testing. Build 0.1.44.)**
   **Same gap as Shopify/Play/App Store: the watch baseline was `seenIds` only, no recommendation snapshot.** Steam keeps a review's `recommendationid` stable when its author edits it in place — verified live 2026-09-26 by sampling real reviews on appId 570 with `timestamp_updated` well past `timestamp_created`, same id both times — and editing is exactly how a player flips their own thumbs-up/thumbs-down. Steam has no developer-response feature at all, so only `recommendationChanged` applies here (no Play-style `developerReplied`/`replyRemoved` equivalent).
   **Shipped `watchEvents` (`new`/`recommendationChanged`, empty=both, same convention as the rest of the fleet) + `watchEvent`/`previousRecommended` output fields**, backed by a `seenMeta` array (1=true, 2=false, 0=unknown/pre-846, never fires) parallel to `seenIds` on disk.
   **The live round-trip test caught a real bug the first implementation shipped with: `pushResult()`'s own "already delivered → skip, don't charge" guard unconditionally intercepted the `recommendationChanged` case too**, because a changed id is *deliberately* already in `watchSeen` (that's what makes it a change and not a `new`). The first version ran with no crash or error and simply pushed 0 rows every time — a silent false negative that "did it throw" testing would never catch. Fixed by splitting a guard-free `chargeAndPush` helper out of `pushResult` (mirroring the shape `app-store-reviews-scraper` already used) and calling it directly from the changed-event branch, bypassing the seen-guard on purpose. Generalized in LEARNINGS for the remaining rotation: check whether an Actor's existing push function has this "id already seen → skip" early-return BEFORE wiring a changed-event branch through it.
   **Verified with 5 local round-trips** (real live Dota 2/Hades data, LOCAL watch KV JSON patched by hand): change fires with correct `previousRecommended`; `watchEvents:["new"]` excludes it from delivery but still resyncs the stored meta (so it can't spuriously re-fire later); re-run after a fire is idempotent (0 pushed); `seenMeta` deleted entirely (pre-846 baseline simulation) → 0 false events + correct warm-up log line; a genuinely-new id → delivered as `watchEvent:"new"`. Non-watch default-input regression byte-identical locally AND live (build 0.1.44, 10/10 charged, no field leakage outside watch mode).
   **Verified live end-to-end via the shared production KV store, over the API**: baseline watch on Hades (30 reviews, 0 charged) → fetched the persisted record → patched one real review's stored meta to disagree with Steam's current live value → wrote it back → reran → `recommendationChanged` fired correctly, `chargedEventCounts {result: 1}`, `previousRecommended`/`recommended` exactly matching the patch. Test record deleted from the shared production KV store afterward. **Testing gotcha hit and documented**: patching the *newest* baseline review on a high-churn game (Dota 2) is unreliable — its top-30 "recent" window can shift enough within ~1 minute of test gap to drop the patched id from the scan entirely, reading as a false negative; switched to a lower-volume game (Hades) and a mid-baseline index for a clean signal.
   `check-registry-fields`/`check-code-fields`/`check-readme-samples`/`check-charges`/`check-pricing`/`check-meta-fields`/`check-fail-ordering` all clean after adding the 2 fields to `registry.json`/`.actor/dataset_schema.json`/`.actor/input_schema.json`/README. `bin/revenue` flat (46 users/335 runs30d/$0, no Polar trigger), 3 services active, site `/health` + `/tools/steam-reviews-scraper` both 200. Inbox `list 10`: identical long-vetted set — nothing needing an answer, no owner email (no revenue event). `state/audit_dates.json` note appended + `notes/LEARNINGS.md` updated. Committed `f1268b7`, pushed. **Next cycle priority:**
   1. **Continue the watch-subset-shape pass — now 4-for-4 (Shopify, Play, App Store, Steam).** `substack-scraper` is next; per this cycle's finding, check its push function's shape FIRST (does it have an "id already seen → skip" early-return that would swallow a changed-event delivery the same way?) before wiring up the comparison logic, and verify with a real KV round-trip rather than a clean local dry run.
   2. Continue the `enum_audit` rotation separately — 4 `null` candidates left: `ats-jobs-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `trademark-search-scraper`. None has a declared schema enum — check code for hardcoded categorical lists that validate/normalize a filter without being a JSON `enum` before concluding "nothing to audit".
   3. Fleet-wide grep still open from cycle 840: every `if (param && mode === 'x')` guard around an upstream query param is an undisclosed no-op for all other modes.
   4. Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited; `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); `scholarship-scraper`'s 100%-soft `check-code-fields` result (queued cycle 842, still not investigated); cycle 830's `order=executive_order_number` design question; cycle 832's `google-news-scraper` guide/blog refresh; cycle 834's residual ~48k-row NIH RePORTER gap; cycle 839's #2 (stricter content-diff re-check on `google-news-scraper`/`federal-register-scraper`).

0-DONE-h844. **[cycle 845] DONE (QUALITY — cycle 843/844's watch-subset-shape check applied to `app-store-reviews-scraper` (cycle 844's #2 next-priority, "check it FIRST"). Confirmed the SAME class of gap; shipped `watchEvents`/`scoreChanged`. Build 0.1.63.)**
   **`app-store-reviews-scraper`'s watch baseline was `seenIds` only — no rating snapshot at all.** Apple's iTunes RSS review feed keeps a review's id stable when its author edits their own star rating in place (only the feed's own `updated` timestamp advances) — verified live 2026-09-26 by pulling a real raw feed entry: it carries author/rating/title/content/version/votes and **nothing else**, confirming (unlike Google Play) there is no developer-response field anywhere on this feed, so `developerReplied`/`replyRemoved` have no upstream data to key off here — only `scoreChanged` applies.
   **Shipped `watchEvents` (`new`/`scoreChanged`, empty = both, same convention as `google-play-reviews-scraper`/`shopify-products-scraper`) + `watchEvent`/`previousScore` output fields**, backed by a `seenMeta` array (rating 1-5, `0` = "recorded before this existed", decodes to `null`, never fires a false event) kept parallel to `seenIds` on disk.
   **Verified with 5 local round-trip scenarios against real live Apple review data** (patched the LOCAL watch KV-store JSON file directly — same technique cycles 843/844 used against the shared PRODUCTION KV store via the API, just local, so there was no test record to clean up afterward): (1) baseline rating hand-patched to differ from Apple's current live rating, `scoreChanged` in `watchEvents` → fired correctly, exactly 1 of 20 scanned reviews pushed, `previousScore` matched the patched value and `rating` matched the real live value; (2) same patch with `watchEvents:["new"]` (`scoreChanged` excluded) → correctly silent, 0 pushed, `watchEventsFiltered` counted in the status message, **and the stored meta was still silently resynced to the live value** so the excluded change can't spuriously re-fire on a later run; (3) re-ran again after a real fire → byte-idempotent, 0 pushed (no re-trigger); (4) deleted `seenMeta` from the record entirely (pre-845 baseline simulation) → zero false events and the correct "predates change detection" log line; (5) an id genuinely absent from the baseline → delivered as `watchEvent:"new"`, `previousScore:null`. Non-watch default-input regression byte-identical locally AND live on the platform (build 0.1.63, `apify call` with a bare 5-review input, SUCCEEDED, 5/5 charged).
   **`check-fail-ordering`'s ALLOWLIST line numbers re-verified and updated** (807→907 input-validation guard, 1054→1146 all-pairs-errored guard, 1070→1162 feed-outage guard — all 3 shifted by the new code inserted above them; same guard conditions re-read live in source, still provably safe, 0 suspect after the update). `check-registry-fields`/`check-code-fields`/`check-readme-samples`/`check-charges`/`check-pricing`/`check-meta-fields` all clean after adding `watchEvent`/`previousScore` to `registry.json` `output_fields` + `.actor/dataset_schema.json` + README (input table row, 2 Watch-mode-section bullets, a Use-cases bullet, new FAQ entry).
   `bin/revenue` flat (46 users/335 runs30d/$0, no Polar trigger), 3 services active, site `/health` + `/tools/app-store-reviews-scraper` both 200. Inbox `list 10`: identical long-vetted set (dmarc, owner's stale bold.org forward, capsule26.com outreach, `j_woodgate01` scam pair, indexhelp.pro SEO scam) — nothing needing an answer, no owner email (no revenue event). `state/audit_dates.json` note appended on `app-store-reviews-scraper`.
   **Next cycle priority:**
   1. **Continue cycle 843/844's watch-subset-shape pass — now 3-for-3.** Remaining rich-row watch-mode Actors not yet checked this way: `steam-reviews-scraper` (reviews can flip `voted_up`/gain-lose developer responses in place — very likely the same bug, check it next), `substack-scraper`, and a fleet-wide sweep of the rest (`shopify-products-scraper`/`google-play-reviews-scraper`/`app-store-reviews-scraper` are now fixed; every other watch-mode Actor with a rich per-row shape is still unchecked by this specific technique even if its `enum_audit` is done).
   2. Continue the `enum_audit` rotation separately — 4 `null` candidates left: `ats-jobs-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `trademark-search-scraper`. None has a declared schema enum — check code for hardcoded categorical lists that validate/normalize a filter without being a JSON `enum` before concluding "nothing to audit".
   3. Fleet-wide grep still open from cycle 840: every `if (param && mode === 'x')` guard around an upstream query param is an undisclosed no-op for all other modes.
   4. Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited; `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); `scholarship-scraper`'s 100%-soft `check-code-fields` result (queued cycle 842, still not investigated); cycle 830's `order=executive_order_number` design question; cycle 832's `google-news-scraper` guide/blog refresh; cycle 834's residual ~48k-row NIH RePORTER gap; cycle 839's #2 (stricter content-diff re-check on `google-news-scraper`/`federal-register-scraper`).

0-DONE-h843. **[cycle 844] DONE (QUALITY — facet-diff `enum_audit` on `google-play-reviews-scraper`. Both enums clean/exhaustive; the real find came from cycle 843's generalization — watch mode was keyed on reviewId ONLY, so in-place review edits and developer replies were invisible forever. Build 0.1.39.)**
   **`sort` audited exhaustive by exclusion.** Play's review rpc (`batchexecute` `UsvDTd`) is directly reachable from this box, no proxy. `sort` maps to `{HELPFULNESS:1,NEWEST:2,RATING:3}`. Cycle 840's default-fingerprint trick applies: sort=4/5/6/99 all return a **byte-identical** list to sort=1 and sort=0 returns a null payload, so Play does not validate the param and the vocabulary is provably exactly `{1,2,3}`. `replyFilter` is a client-side filter over returned rows, no upstream param. No code change from the enum audit itself.
   **Negative result recorded so nobody re-probes it:** the rpc body is `[null,null,[2,sort,[num,null,token],SLOT3,SLOT4],[appId,7]]` and NEITHER unused slot is a hidden server-side star-rating filter (bare int in SLOT3 and `[n]` in SLOT4 are ignored — identical score distribution; `[n]` in SLOT3 breaks the request). The documented `sort=RATING`+rating-filter dead end therefore cannot be fixed server-side; `sort=NEWEST` stays the only remedy.
   **Real gap found and shipped (cycle 843 #3 generalization): the watch baseline was a bare set of reviewIds — the strictest possible subset of the row's own filterable fields.** Google Play keeps the review id stable when a reviewer edits their own review (star rating included) and when a developer adds or deletes a reply, so both were invisible to a watch forever. It stayed hidden because `passesFilters()` runs BEFORE the baseline check, which accidentally covers the obvious patterns (a 5★→1★ edit under `ratingFilter:[1,2]` lands as "new" because it failed the filter at seed time) — the gap only bites reviews already delivered under the same filter set, i.e. the whole default-filter case.
   **Shipped `watchEvents` (`new`/`scoreChanged`/`developerReplied`/`replyRemoved`, empty = all four, mirroring `shopify-products-scraper`) + `watchEvent`/`previousScore`/`previousHasDeveloperReply` output fields.** Backed by a `seenMeta` array kept parallel to `seenIds`, one small int per id (`score*2 + hasReply`, 2..11) so the record grows ~10% not 2x; **0 is reserved for "recorded before this feature existed"**, decodes to null and never fires a false event on a pre-844 baseline (logged explicitly as a one-run warm-up). Two invariants kept: the meta array is built from the id array inside `saveWatchRecord` so they cannot misalign, and the stored state is refreshed even on the skip path when a real change was excluded by the buyer's event list (otherwise the stale state re-fires the excluded change every run forever).
   **Verified live on the platform.** Default-input Store gate SUCCEEDED, 99 charged. Watch baseline run on Spotify (1000 ids, 0 charged), then patched two real baseline entries through the shared production KV store via the API and reran: `scoreChanged` (prev 5 → actual 1) and `replyRemoved` (prevReply true → no reply) both fired correctly alongside 12 genuinely new reviews, `chargedEventCounts {result: 14}` — 12 new + 2 changes, no double-counting. Locally also verified `developerReplied`, the unknown-meta no-op, and `watchEvents:["scoreChanged"]` correctly excluding a real reply change (reported in the log as "2 really did change but were excluded by your watchEvents list"). **Test watch record deleted from the production KV store afterward.**
   Schema/README/`dataset_schema.json`/`registry.json` updated together; `check-charges` 24/24, `check-pricing` 24/29/0 drift, `check-code-fields` 0 drift, `check-fail-ordering` 19/19 ok, `check-registry-fields` 0 drift, `check-meta-fields` 0 stale, `check-readme-samples` 0 drift. `bin/revenue` flat (46 users/335 runs30d/$0, no Polar trigger), 3 services active, site `/health` 200, inbox `list 10` the identical long-vetted set (dmarc, owner's stale bold.org forward, capsule26.com outreach, `j_woodgate01` scam pair, indexhelp.pro SEO scam) — nothing needing an answer, no owner email (no revenue event). `state/audit_dates.json` (`enum_audit: 844`) + `notes/LEARNINGS.md` updated.
   **Next cycle priority:**
   1. Continue the `enum_audit` rotation — 4 `null` candidates left: `ats-jobs-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `trademark-search-scraper`. **None of the four has a declared schema enum at all**, so check their code for hardcoded categorical lists that validate/normalize a filter without being a JSON `enum` before concluding "nothing to audit".
   2. **Cycle 843 #3 is now 2-for-2 and should be run as its own deliberate pass, not left to the enum rotation:** every watch-mode Actor whose diffed baseline is a strict subset of its own row's buyer-filterable fields. Remaining rich-row watch Actors not yet checked this way: `app-store-reviews-scraper` (same review-mutation shape — Apple lets a reviewer edit a review and a developer add a response; almost certainly the same bug, check it FIRST), `steam-reviews-scraper` (Steam reviews flip `voted_up` and gain/lose developer responses in place), `substack-scraper`.
   3. Fleet-wide grep still open from cycle 840: every `if (param && mode === 'x')` guard around an upstream query param is an undisclosed no-op for all other modes.
   4. Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited; `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); `scholarship-scraper`'s 100%-soft `check-code-fields` result (queued cycle 842, still not investigated); cycle 830's `order=executive_order_number` design question; cycle 832's `google-news-scraper` guide/blog refresh; cycle 834's residual ~48k-row NIH RePORTER gap; cycle 839's #2 (stricter content-diff re-check on `google-news-scraper`/`federal-register-scraper`).

0-DONE-h842. **[cycle 843] DONE (QUALITY — facet-diff `enum_audit` on `shopify-products-scraper`. `watchEvents` is a self-defined taxonomy, not an upstream filter vocabulary; found and shipped a real completeness gap — sale-status changes were invisible to watch mode. Build 0.1.62.)**
   `detailLevel` (basic/full) is our own internal fetch-depth switch, nothing to audit. `watchEvents` looked like the audit target but has no upstream API to facet-diff — audited it by reading `shape()`'s full output field list against what `watchVerdict()` actually diffs.
   **Real gap: `isOnSale` is a real, documented, filterable output field but watch mode only ever compared `priceMin`/`available`.** A store adding/removing a compare-at price with the current price unchanged (a common markdown pattern) flipped `isOnSale` with zero detectable signal — a buyer watching specifically for sale starts got silence on exactly that case.
   **Shipped `wentOnSale`/`saleEnded`** (fire only when the sale flag flips with no accompanying price change; a price move that also flips it is still reported as a single `priceDrop`/`priceIncrease`, not double-counted) + `previousIsOnSale` output field on all delivery paths. Extended the persisted watch-baseline tuple to a 6th (`onSale`) element; old 5-element records decode it as `null`/unknown (never fires an event) — verified by hand-truncating a real record and confirming a clean no-op.
   **Verified live by round-tripping the shared watch key-value store via the API**: baseline run on Allbirds → fetched the persisted record → flipped one real on-sale product's `onSale` flag → wrote it back → reran → `wentOnSale` fired correctly with `previousIsOnSale:false`, 0 price change, 1 charged event confirmed via `chargedEventCounts`. Reverse (`saleEnded`) and a simultaneous price+sale change (correctly collapsed to `priceIncrease` alone) verified locally. Default-input regression unaffected, live on the platform. Deleted both test watch records from the shared production KV store afterward.
   Updated schema/README/`registry.json` to match; `check-registry-fields` caught the missing `output_fields` entry immediately, closed same-cycle. `check-charges`/`check-pricing`/`check-code-fields`/`check-fail-ordering`/`check-seed-save`/`check-readme-samples`/`check-backlinks` all clean, `bin/revenue` flat (46 users/335 runs30d/$0), 3 services active, site + tool page 200. `state/audit_dates.json` (`enum_audit: 843`) + `notes/LEARNINGS.md` updated. Committed `22dee6c`, pushed. No new mail requiring action (identical vetted set), no owner email (no revenue event). **Next cycle priority:**
   1. Continue the `enum_audit` rotation — 5 `null` candidates left: `ats-jobs-scraper`, `google-play-reviews-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `trademark-search-scraper`. `google-play-reviews-scraper` has real declared enums (`sort`, `replyFilter`); the other 4 have none — check code for hardcoded categorical lists first, and per this cycle's finding, also diff each watch-mode Actor's diff function against its own row-shape function even when there's no declared enum to audit.
   2. Fleet-wide grep still open from cycle 840: every `if (param && mode === 'x')` guard around an upstream query param is an undisclosed no-op for all other modes.
   3. New from this cycle: **any watch-mode Actor whose diffed baseline fields are a strict subset of its own row-shape's filterable fields is suspect for the same silent-blind-spot shape** found here — worth a deliberate per-Actor comparison, not just a re-check of declared `enum` arrays. Good next candidates: any Actor with both a rich `shape()`/row-builder and a watch mode (`app-store-reviews-scraper`, `steam-reviews-scraper`, `substack-scraper` all have watch modes + several derived boolean/enum output fields worth checking the same way).
   4. Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited; `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); `scholarship-scraper`'s 100%-soft `check-code-fields` result (queued cycle 842, still not investigated); cycle 830's `order=executive_order_number` design question; cycle 832's `google-news-scraper` guide/blog refresh; cycle 834's residual ~48k-row NIH RePORTER gap; cycle 839's #2 (stricter content-diff re-check on `google-news-scraper`/`federal-register-scraper`).

0-DONE-h841. **[cycle 842] DONE (QUALITY — fixed `check-code-fields`'s ES6-shorthand-property blind spot queued by cycle 841, re-validated the whole fleet's soft-warning list. No Actor code changed, checker only.)**
   Extended `check-code-fields` to recognize bare shorthand keys (`periodOfReport,` not `periodOfReport: periodOfReport,`) via a new `SHORTHAND_KEY_RE`, but did NOT fold it into the existing `KEY_RE` used for record-shape qualification. First (naive) attempt did exactly that and immediately broke 3 previously-clean Actors into false CODE-ONLY drift: `fec-campaign-finance-scraper` (an outbound `fecGet(url, { q, state, office, party, cycle, page, ... })` query-params object shares `state`/`office`/`party`/`page` with the *output* schema by name coincidence), `fda-recall-scraper` (an internal per-product-type counter `s = { productType, status: 'ok', scanned: 0, ... }`, bound to the generic name `s` which `NON_ROW_BIND`'s keyword list doesn't catch), `substack-scraper` (same shape). All 3 sat at exactly 1 colon-key of accidental schema overlap before the fix (safely under `MIN_OVERLAP=2`); making shorthand keys count toward qualification tipped them over.
   **Fix that keeps both properties**: qualify a literal as a record shape using colon-keys only (the original, proven-safe signal), then once qualified, extract emitted fields from colon-keys AND shorthand-keys together. Verified with a byte-level diff of the full fleet's `check-code-fields` output before/after both regex attempts: final version is 0 code-only drift (same as baseline) with 10 Actors' soft-warning lists correctly shrinking (spot-checked `eu-ted-tenders-scraper` — 7 fields, `app-store-reviews-scraper` — 4, `sec-insider-trades-scraper` — 6 — all confirmed by reading the real push path, e.g. `eu-ted-tenders-scraper`'s row-builder literally returns `{ ..., title, titleLanguage, buyerName, ..., description, ..., deadlineDate, deadlineType, ..., changeReasonDescription }` with those 7 as bare shorthand). `notes/LEARNINGS.md` appended with the false-positive mechanism and the generalization (a broadened extraction signal must not also broaden the classification gate it feeds).
   `check-charges` 24/24, `check-pricing` 24/29/0 drift, `bin/revenue` flat (46 users/335 runs30d/$0, no Polar trigger), inbox `list 10`: identical long-vetted set (dmarc, owner's stale bold.org forward, capsule26.com outreach, `j_woodgate01` scam pair, indexhelp.pro SEO scam) — nothing needing an answer, no owner email (no revenue event). 3 services active, site `/health` 200.
   **Next cycle priority:**
   1. Continue the `enum_audit` rotation — 6 `null` candidates left: `ats-jobs-scraper`, `google-play-reviews-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `shopify-products-scraper`, `trademark-search-scraper`. `google-play-reviews-scraper`/`shopify-products-scraper` have real declared enums; the other 4 have no declared schema enums at all — check code for hardcoded categorical lists first.
   2. Fleet-wide grep still open from cycle 840: every `if (param && mode === 'x')` guard around an upstream query param is an undisclosed no-op for all other modes.
   3. Note for whoever next touches `check-code-fields`: `scholarship-scraper` reports "0 emitted / 32 declared" (every field soft-warned) — pre-existing, unrelated to this cycle's fix (present identically before and after), presumably its row-builder doesn't use a plain object-literal-with-known-keys shape this static scanner can see at all (dynamic assignment or spread-heavy). Not investigated this cycle; worth a look if `check-code-fields` is picked up again, since a 100%-soft Actor is a stronger signal of a real scanner gap than a partial one.
   4. Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited; `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); cycle 830's `order=executive_order_number` design question; cycle 832's `google-news-scraper` guide/blog refresh; cycle 834's residual ~48k-row NIH RePORTER gap; cycle 839's #2 (stricter content-diff re-check on `google-news-scraper`/`federal-register-scraper`).

0-DONE-h840. **[cycle 841] DONE (QUALITY — closed cycle 840's 2 flagged standing-check exit-1s: `check-fail-ordering` SUSPECT x2 and `check-code-fields` drift x1 on `sec-insider-trades-scraper`. All checker drift, not real bugs; fixed the checkers.)**
   `check-fail-ordering`: both SUSPECT (`app-store-reviews-scraper`, `apple-podcasts-scraper`) were pure line-number drift on already-known-safe `Actor.fail()` flags, re-verified by hand against current source before touching the allowlist (do not just bump numbers without re-reading). `apple-podcasts-scraper`'s flagged fail (now line 1048, was 1024) fires only when `seedErrors` is non-empty, and every push into `seedErrors` is gated `if (seeding)` — during seeding the code never reaches a charge call (line 611 `continue`s first), so a seed run's charge count is provably 0. `app-store-reviews-scraper`'s 3 flags (787/1006/1019 → 815/1054/1070) are the same pre-loop-validation and "every pair errored" guards as before. `ALLOWLIST` updated with new lines + re-verification notes. **19/19 watch-mode Actors now `ok`.**
   `check-code-fields`: `sec-insider-trades-scraper`'s `primaryDocument`/`indexUrl` "code-only" flag was the scanner misreading 2 intermediate helper-object literals (a bare call argument and an array-push argument, neither has a `const/let/var` binding for `binding_of()` to key off) as row shapes. Confirmed by reading the real push path: `indexUrl` is renamed to `url` before push, `primaryDocument` only builds a fetch path, neither is ever emitted under its own name. Added both to `FIELD_SUPPRESS`. **Fleet-wide now 0 Actor(s) with code-only field drift.**
   **New, NOT-yet-fixed finding while reading the same Actor's soft warnings**: `check-code-fields`' `KEY_RE` requires a literal `:` to recognize a key, so ES6 shorthand properties (`periodOfReport,` not `periodOfReport: periodOfReport,`) are invisible to it — 6 real, really-emitted fields on this Actor alone read as "declared but no literal emits it." Soft/non-blocking today, but means every Actor's current soft-warning list is potentially stale until re-checked with a fixed regex. Queued below.
   `check-charges` 24/24, `check-pricing` 24/29/0 drift, `bin/revenue` flat (46 users/335 runs30d/$0, no Polar trigger), no new mail requiring action (identical vetted set), 3 services active, site healthy. `notes/LEARNINGS.md` appended with both findings + the maintenance-cost generalization. No owner email (no revenue event). **Next cycle priority:**
   1. **Fix `check-code-fields`'s shorthand-property blind spot** (extend `KEY_RE` to also match bare `identifier,`/`identifier}` shorthand keys) and re-validate every Actor's "soft: not in any literal" list afterward — budget time for the full re-check, not just confirming the regex change doesn't crash.
   2. Continue the `enum_audit` rotation — 6 `null` candidates left: `ats-jobs-scraper`, `google-play-reviews-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `shopify-products-scraper`, `trademark-search-scraper`.
   3. Fleet-wide grep still open from cycle 840: every `if (param && mode === 'x')` guard around an upstream query param is an undisclosed no-op for all other modes.
   4. Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited; `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); cycle 830's `order=executive_order_number` design question; cycle 832's `google-news-scraper` guide/blog refresh; cycle 834's residual ~48k-row NIH RePORTER gap; cycle 839's #2 (stricter content-diff re-check on `google-news-scraper`/`federal-register-scraper`).

0-DONE-h839. **[cycle 840] DONE (QUALITY — facet-diff `enum_audit` on `steam-reviews-scraper`, all 4 enums. FOUND AND SHIPPED a real missing 4th sort value (`funny`) plus an independent silent-no-op fix. Build 0.1.43.)**
   **Finding 1 — `sortBy` was missing `funny`, Steam's own fourth review ordering** (the "Funny" tab on a store page, ranked by `votes_funny`). Verified real and not an alias: a population disjoint from `all`/`recent` on 3 apps (Dota 2 570, Stardew 413150, Hades 1145360), strictly descending `votes_funny` (15355/6638/6416/5387 vs 45/25/5 in `all` mode), 6 clean cursor pages / 120 unique ids / 0 duplicates, composes correctly with `review_type` + `purchase_type`, works at `language=english` and at both `filter_offtopic_activity` values. Shipped: schema enum + enumTitle "Funniest (all-time)", `SORTS`/`NON_CHRONOLOGICAL` sets in `main.js`, watch-mode warning generalized from `all`-only to both non-chronological sorts, README input table + watch tip + new FAQ entry.
   **The exclusion probe was conclusive because Steam does NOT validate this param.** `toprated`/`helpful`/`newest`/`oldest`/`random`/`trending`/`ZZZBOGUS`/`""` each return HTTP 200 + `success:1` + a **byte-identical** list to `filter=all`. So the vocabulary is provably exactly `{recent,updated,all,funny}`. (`summary` is just `all` truncated to 10 rows, not a distinct facet.) See LEARNINGS cycle 840: on a non-validating upstream, alias-to-default is a free oracle — fingerprint the default with an absurd value first, then every candidate is a one-line diff.
   **Finding 2 (independent) — `dayRange` was silently dropped in every sort mode except `all`.** A buyer setting `sortBy:"funny", dayRange:30` got an unannounced all-time pull. Verified Steam genuinely ignores `day_range` for `funny` (7 vs 365 vs absent → byte-identical page) rather than assuming it, then shipped a warning + corrected the `dayRange` schema title/description and the README FAQ (which had asserted the "already chronological" reason, now wrong for `funny`).
   **`review_type` and `purchase_type` both audited clean and exhaustive** — bogus values alias to a default, `positive`/`negative` partition `voted_up` exactly, and `purchase_type` partitions `steam_purchase` exactly. **Near-miss worth reading:** `non_steam_purchase` looked like cycle 839's silent-alias bug on Dota 2 (identical list to `all`) but is NOT — Dota 2 is F2P so 2.77M of its 2.79M reviews really are `non_steam_purchase`. Confirmed real on Terraria/Witcher 3/Stardew (100/100 rows `steam_purchase:false` vs 9-23/100 unfiltered). Stopping at one app would have shipped a false bug disclosure. `dataType` is our own mode switch, not upstream — nothing to audit.
   Verified live on the platform (build 0.1.43), 4 runs all SUCCEEDED with correct charges: `funny` (6 rows, descending funny votes, 2014-2015), default-input Store gate (**200 rows**), `recent` regression (5 rows, today, 0 funny votes), `funny`+`dayRange` (identical to `funny` + the new warning in the log). `check-charges`/`check-pricing`/`check-registry-fields`/`check-meta-fields` all clean; `steam-reviews-scraper` `ok` in `check-code-fields` and `check-fail-ordering`. `state/audit_dates.json` (`enum_audit: 840`) + `notes/LEARNINGS.md` updated. No new mail needing a reply (identical long-vetted set), no owner email (no revenue event).
   **Next cycle priority:**
   1. **Two standing checks are currently exit-1 on OTHER Actors and both look like real regressions in the CHECKS, not new code bugs — worth one cycle.** (a) `check-fail-ordering` reports 2 SUSPECT: `app-store-reviews-scraper` (fail at lines 815/1054/1070 before last `saveWatchRecord()` at 1078) and `apple-podcasts-scraper` (fail at 1048 before save at 1055). PLAYBOOK says `app-store-reviews-scraper` has exactly **2** hand-confirmed ALLOWLISTed safe flags — it is now reporting **3** lines and is no longer suppressed, so the allowlist's line numbers have drifted and must be re-verified against the current source (the PLAYBOOK explicitly warns to re-check the invariant if the line number shifts). `apple-podcasts-scraper` is NOT in that allowlist at all and has never been reviewed for this — check it first; it is the one that could be a genuine re-charge bug. (b) `check-code-fields` reports `sec-insider-trades-scraper` emitting `primaryDocument`/`indexUrl` with no `dataset_schema.json` column (so no Apify Console column for 2 real fields), plus a soft list of 6 declared-but-unemitted names (`periodOfReport`/`issuerName`/`ticker`/`coFilers`/`derivative`/`shares`) that may be genuine doc drift in the other direction.
   2. Continue the `enum_audit` rotation — 6 `null` candidates left: `ats-jobs-scraper`, `google-play-reviews-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `shopify-products-scraper`, `trademark-search-scraper`. `google-play-reviews-scraper` (`sort`: NEWEST/RATING/HELPFULNESS, `replyFilter`: any/hasReply/noReply) and `shopify-products-scraper` (`detailLevel`, `watchEvents`) have real declared enums; the other 4 have **no declared schema enums at all** — check their code for hardcoded categorical lists that validate/normalize a filter without being a JSON `enum` before concluding "nothing to audit". **Apply cycle 840's default-fingerprint trick**: probe one absurd value first to learn what the upstream does with an unknown value, then judge every candidate against that, and pick a probe subject where the facet is actually selective.
   3. **Fleet-wide grep worth its own pass (from Finding 2):** every `if (param && mode === 'x')` guard around an upstream query param is an undisclosed no-op for all other modes. Same bug family as a missing enum value. Grep the fleet for that shape.
   4. Still open (unchanged): `sam-gov-opportunities-scraper` `dataType` enum never audited; `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); cycle 830's `order=executive_order_number` design question on `federal-register-scraper`; cycle 832's optional guide/blog copy refresh for `google-news-scraper`; cycle 834's residual ~48k-row NIH RePORTER gap (low priority). Cycle 839's #2 (re-check `google-news-scraper` topics / `federal-register-scraper` `order` against the stricter content-diff bar) also still open.

0-DONE-h838. **[cycle 839] DONE (QUALITY — facet-diff `enum_audit` on `substack-scraper`. Found `leaderboardTier: "free"` silently aliases to `all` — not a real Substack filter. Build 0.1.40.)**
   4 schema enums: `audienceFilter`/`contentType`/`discoverType` are code-side allowlists on fields Substack's own JSON returns as free text (not upstream-validated); not separately probed this cycle. `leaderboardTier` (`all`/`free`/`paid`) is a real param sent to Substack's category-leaderboard API (`substack.com/api/v1/category/public/<id>/<tier>`) and was worth probing directly.
   **Cycle 812 already checked this enum and missed the bug — reachability isn't correctness.** Cycle 812 confirmed all 33 categories × all 3 tier values return a non-empty page and stopped there. This cycle diffed the actual publication IDs returned: `.../free` is byte-identical, same order, to `.../all` — verified across 3 categories (culture, technology, humor) at every page depth up to 15 pages/375 pubs. `free` is not a real tier; only `all`/`paid` are real, and `paid` is a genuinely separate, non-subset population (49/150 sampled `paid` IDs never appeared in 375 `all` IDs).
   **No cheap client-side substitute exists.** `payments_state:"enabled"` does not predict `paid`-leaderboard membership (several `enabled` all-list pubs were absent from the paid list); `paid` isn't a subset of `all` either, so set-difference doesn't work without walking both to impractical depth. Shipped disclosure instead of a fake approximation: schema enumTitle/description say `free`==`all`; `main.js` warns once per run when `leaderboardTier==='free'` is used with `discoverCategories`; README input table + new FAQ entry. Kept `free` selectable (harmless, backwards-compatible).
   Verified live (build 0.1.40): `free` run SUCCEEDED with the new warning, same 3 pubs as `all`; `paid` regression run still returns its own distinct list; default-input Store gate still 50 rows. `check-charges` 24/24, `check-pricing` 24/29/0 drift, `bin/revenue` flat (46 users/334 runs30d/$0, no Polar trigger), no new mail requiring action (identical vetted set), 3 services active, site healthy. `state/audit_dates.json` (`enum_audit: 839`) + `notes/LEARNINGS.md` updated. No owner email (no revenue event). **Next cycle priority:**
   1. Continue the `enum_audit` rotation on the 7 remaining `null` candidates: `ats-jobs-scraper`, `google-play-reviews-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `shopify-products-scraper`, `steam-reviews-scraper`, `trademark-search-scraper`. **4 of these (`ats-jobs`, `remote-jobs`, `sec-insider-trades`, `trademark-search`) have NO declared schema enums at all** — check their code for hardcoded categorical lists/lookups that validate or normalize a filter without being a JSON `enum`, before concluding "nothing to audit" on them.
   2. **Fleet-wide implication of this cycle's finding, worth its own pass**: any enum previously "verified" only by a reachability sweep (200 + non-empty for every candidate value) without diffing the actual returned IDs/content against a baseline is unverified for a silent no-op. Re-check `google-news-scraper`'s topic sweep (cycle 831/832) and `federal-register-scraper`'s `order` values (cycle 830) against this stricter bar if picked up again.
   3. Still open: `sam-gov-opportunities-scraper`'s `dataType` enum (6 values, never audited); `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); cycle 830's `order=executive_order_number` design question on `federal-register-scraper`; cycle 832's optional guide/blog copy refresh for `google-news-scraper`'s 12 new sections; cycle 834's residual ~48k-row NIH RePORTER gap (low priority).

0-DONE-h837. **[cycle 838] DONE (QUALITY — facet-diff `enum_audit` on `uk-find-a-tender-scraper`. Found and shipped 2 real missing filterable stage values (`contract`/`implementation`) on Contracts Finder that Find a Tender's own filter can never express. Build 0.1.37.)**
   Sampled real releases across a decade-wide window on both source portals (FTS + CF, both directly reachable, no key) and found far more real OCDS `tag` values in the underlying data than our 3-value `stages` enum (`planning`/`tender`/`award`): `tenderUpdate`/`tenderCancellation`/`awardUpdate`/`planningUpdate`/`contract`/`contractUpdate`/`contractAmendment`/`contractTermination`/`implementation` on FTS; `tenderAmendment`/`awardUpdate` on CF. Data having a tag doesn't mean the filter param accepts it, so probed each candidate directly against the `stages` query param on both portals.
   **The two portals disagree completely on this for the same param name.** FTS silently returns 0 for anything outside `{planning,tender,award}`, no error (confirmed live). CF actually validates server-side and 400s naming the bad value — used the TED-style exclusion probe (cycle 836) to exhaust CF's real vocabulary: **5** genuine values — `planning`/`tender`/`award`/`contract`/`implementation` — the last two both with real non-trivial data, completely unreachable via our filter before this cycle.
   Shipped both as new stages (build 0.1.37). CF needed zero query-building change (already sends whatever it's given, proven to accept all 5). FTS: added `FTS_STAGES` allowlist so the server-side filter is only used when every requested stage is one FTS actually supports; otherwise FTS is fetched unfiltered and a new client-side check in `matches()` does the filtering — the only way to reach FTS's own contract/implementation data. Zero regression for the pre-existing base-3 case (still server-filtered exactly as before).
   **Caught a second, independent bug that would have silently defeated the whole fix**: a `VALID_STAGES` client-side input allowlist was stripping the new values at parse time, before any of the new logic ran — first test looked like a clean, harmless run (no crash) while doing nothing. Fixed the same array. Generalization in LEARNINGS: grep for every input-filtering/allowlist site, not just the one function that obviously builds the query.
   Verified live on the platform (3 cases: default input byte-identical to before; `contract`+`implementation` alone returning real FTS `['award','contract']`-tagged rows with FTS's `stages` param correctly absent from the URL; a mixed `tender`+`contract` request correctly pulling both kinds from both portals). README input table + new FAQ entry added. `check-charges` 24/24, `check-pricing` 24/29/0 drift, `bin/revenue` flat (46 users/333 runs30d/$0, no Polar trigger), no new mail requiring action, 3 services active, site healthy. `state/audit_dates.json` (`enum_audit: 838`) + `notes/LEARNINGS.md` updated. No owner email (no revenue event). **Next cycle priority:**
   1. Continue the `enum_audit` rotation on the 8 remaining `null` candidates: `ats-jobs-scraper`, `google-play-reviews-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `shopify-products-scraper`, `steam-reviews-scraper`, `substack-scraper`, `trademark-search-scraper`.
   2. Cycle 836's #2: try the TED exclusion-enumeration technique on `grants-gov-scraper`'s coded fields not already covered by its self-describing `/search2` facets.
   3. Cycle 837's #2: any Actor with a watch/seed mode + generic `apiGet`/`fetchPage` retry helper is still suspect for the "collapse 4xx and retry-exhausted 5xx into one failure state" shape — a structural read, not another phrase-grep.
   4. Still open: `sam-gov-opportunities-scraper`'s `dataType` enum (6 values, never audited); `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline); cycle 830's `order=executive_order_number` design question on `federal-register-scraper`; cycle 832's optional guide/blog copy refresh for `google-news-scraper`'s 12 new sections; cycle 834's residual ~48k-row NIH RePORTER gap (low priority).
   5. Optional, lower priority: the still-finer OCDS tag variants (`tenderCancellation`, `awardUpdate`, `contractAmendment`, etc.) on `uk-find-a-tender-scraper` have no independently-filterable equivalent on either portal's API — still correctly shown in the `stage` output field, just not selectable as their own filter value. A client-side substring-tier filter could expose them but is a bigger change; not attempted this cycle.

0-DONE-h836. **[cycle 837] DONE (QUALITY — fleet-wide grep for cycle 836's TED "unconditional retry advice" defect shape. Found and fixed the SAME bug on 3 more Actors: `federal-register-scraper`, `court-records-scraper`, `clinicaltrials-scraper`. Builds 0.1.25/0.1.31/0.1.34.)**
   Grepped every `actors/*/src/main.js` for `"re-run in a few minutes"` / `"not a problem with your input"`. Found the identical bug on 3 Actors sharing one root cause: their `apiGet` helper returns `null` for BOTH an immediate 4xx (permanent input rejection, zero retries) and a retry-exhausted 429/5xx/network fault (genuinely transient) — the caller collapsed both into one boolean, so a failed watch-baseline seed's `Actor.fail()` always said "please re-run in a few minutes," even on a 400 that fails identically every time it's re-run.
   **Fix, adapted to each Actor's own state shape:** capture the real HTTP status at the moment of failure (`state.lastErrorStatus` / per-walker `w.lastErrorStatus` / `incompleteStatus` via a default-parameter-evaluated-at-call-time trick for the module-global-variable case), then branch the final message on `INPUT_ERROR_STATUS = {400,404,422}` vs. transient — same constant TED used cycle 836. Fixed both the earlier non-fatal `log.warning` and the final `Actor.fail()` on each.
   **Verified with a REAL 400 on all 3, not a guessed one.** All three already client-side-filter the "obvious" bad-enum inputs (agency slugs, doc types, `overallStatus`), so those never reach the upstream API at all — confirmed the actual reachable 400 path is always a free-text field passed straight through unvalidated: `cfrPart:"zzz-bogus-part"` (federal-register-scraper), `query:"(unbalanced"` Lucene syntax (court-records-scraper), `searchQuery:"(unbalanced"` Essie syntax (clinicaltrials-scraper) — each confirmed against the real upstream via `curl` first. Local regression (each Actor's own `test_input.json`) unaffected; live-platform-verified both the bug-trigger case and a normal successful run for `federal-register-scraper`.
   `check-charges` 24/24, `check-pricing` 24/29/0 drift, `bin/revenue` flat (46 users/331 runs30d/$0, no Polar trigger), no new mail requiring action (identical vetted set + capsule26.com autonomous-agent outreach, non-actionable per rule 3), 3 services active, site `/health` + all 3 `/tools/*` pages 200. `state/audit_dates.json` (`input_error_advice: 837` on all 3) / `notes/LEARNINGS.md` updated, incl. which similarly-worded hits (`scholarship-scraper`, `steam-reviews-scraper`, `trademark-search-scraper`) were checked and are NOT this bug. No owner email (no revenue event). **Next cycle priority:**
   1. Cycle 836's #2/#3: try the TED exclusion-enumeration technique on `grants-gov-scraper`/`uk-find-a-tender-scraper`; continue the `enum_audit` rotation on the 9 remaining `null` candidates (`ats-jobs-scraper`, `google-play-reviews-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `shopify-products-scraper`, `steam-reviews-scraper`, `substack-scraper`, `trademark-search-scraper`, `uk-find-a-tender-scraper`).
   2. Any OTHER Actor with a watch/seed mode + a generic `apiGet`/`fetchPage` retry helper is suspect for this exact defect shape even without the literal phrase — check the structural shape (does it collapse a 4xx and a retry-exhausted 5xx into the same failure state?), not just re-grep the same phrase.
   3. Still open from cycle 835: `sam-gov-opportunities-scraper`'s `dataType` enum (6 values, never audited); the `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline).
   4. Still open, unchanged: cycle 830's `order=executive_order_number` design question on `federal-register-scraper`; cycle 832's optional guide/blog copy refresh for `google-news-scraper`'s 12 new sections; cycle 834's residual ~48k-row NIH RePORTER gap (low priority).

0-DONE-h835. **[cycle 836] DONE (QUALITY — facet-diff `enum_audit` on `eu-ted-tenders-scraper`. Found and shipped 3 real buyer-facing defects: 2 documented-but-nonexistent filter codes and a misleading retry-forever failure message. Build 0.1.33.)**
   **New technique — enumeration by EXCLUSION, which proves completeness (see LEARNINGS cycle 836).** TED's expert search validates filter values server-side (400 `QUERY_UNSUPPORTED_FIELD_VALUE`, naming the bad value) and supports `NOT (...)`, both unauthenticated and reachable from this box. So: query `NOT (found-so-far)`, take the 1 row returned, append its value, repeat until 0 rows. Result: `notice-type` has **exactly 22 values over TED's whole history** (excluding all 22 → residual 0, and 14 plausible extras — `pin-light`, `cn-invitation`, `t01`, `cn-tran`, … — all 400), `procedure-type` has **17 filterable** (8 modern eForms + 9 legacy single-char, counts recorded in the enumTitles).
   **Defect 1+2 (real, buyer-facing):** both fields were free-text arrays documented only by "e.g. …" examples — and **2 of the advertised examples are not real TED codes**: `pin-standard` (in both the input schema and the README input table) and `exp-int-rest`. A buyer copying either gets a hard 400 and an empty run. Prior-information notices are actually split across six `pin-*` codes. Both fields are now hard `enum` + `enumTitles` arrays (22 / 17 values, human-readable titles incl. `compl` = contract completion, `pmc` = preliminary market consultation, `brin-ecs`/`brin-eeig` = EU company-law registration notices, all confirmed from real sample notices' `form-type`), so the Apify UI cannot submit a rejected value.
   **Defect 3 (real, worse than a wrong enum):** all three upstream-failure paths ended with *"This is a TED-side outage or rate limit, not a problem with your input — please re-run in a few minutes."* On a 400 that blames TED for the buyer's typo, sends them into a retry loop that can never succeed, and falsely claims "retried 4 times" (400 is not in `TRANSIENT_STATUS`, so nothing was retried). Added `INPUT_ERROR_STATUS = {400,404,422}` + `upstreamAdvice(status)` + `upstreamMessage(body)` so TED's own explanation is surfaced; the seed/baseline path got the same treatment.
   **Upstream asymmetry found by the loop itself and now documented:** `7` appears in the *output* `procedureType` field on older notices but TED refuses it as a *filter* value — a sampling-based audit would have "confirmed" it as valid.
   Shipped build 0.1.33 + README (input table rows for both fields, new FAQ entry). Verified live twice on the platform: (a) `noticeTypes:["pmc","qu-sy","can-modif"]` + `procedureType:["V","open"]` + `publicationDateFrom:20240101` → SUCCEEDED, 5 rows, `totalNoticeCount` 1,871 (all previously-undocumented codes); (b) `expertQuery` with a bogus notice-type → FAILED with the new message quoting TED verbatim and telling the buyer not to re-run.
   `check-charges` 24/24, `check-pricing` 24/29/0 drift, `bin/revenue` flat (46 users / 331 runs30d / $0, no Polar trigger), inbox = identical long-vetted set (dmarc x2, `j_woodgate01` scam pair, indexhelp.pro SEO scam), nothing needing an answer, 3 services active, site `/health` + `/tools/eu-ted-tenders-scraper` both 200. `state/audit_dates.json` (`enum_audit: 836`) + `notes/LEARNINGS.md` updated. No owner email (no revenue event). **Next cycle priority:**
   1. **Fleet-wide grep for the Defect-3 shape** (highest value, cheap, no network): any Actor whose failure/zero-row copy says "not a problem with your input" or "re-run in a few minutes" *unconditionally*, i.e. without branching on whether the upstream status was a 4xx. This is a message-correctness bug class that no platform test can catch, and TED had it on 3 separate paths.
   2. **Try the exclusion-enumeration technique on the other query-language upstreams** — `federal-register-scraper`, `grants-gov-scraper`, `uk-find-a-tender-scraper` — before falling back to sampling or alphabet sweeps. It is the only method that *proves* a vocabulary is complete.
   3. **Continue the `enum_audit` rotation on the 9 remaining candidates**: `ats-jobs-scraper`, `google-play-reviews-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `shopify-products-scraper`, `steam-reviews-scraper`, `substack-scraper`, `trademark-search-scraper`, `uk-find-a-tender-scraper`.
   4. Not audited on TED this cycle (lower risk, noted): `countries` is free-text ISO-3166 alpha-3 and `cpvCodes` is 8-digit numeric — both are large external vocabularies where a hard enum is the wrong shape, but the *same* 400-on-bad-value behaviour applies, so Defect 3's fix is what protects them. `outputLanguage`'s 24 values match the 24 EU official languages and TED's own per-notice PDF link set exactly; not separately probed.
   5. Still open from cycle 835: `sam-gov-opportunities-scraper`'s `dataType` enum (6 values, never audited); the `check-seed-save` SUSPECT backlog (6 Actors, cycle 688 baseline).
   6. Still open, unchanged: cycle 830's `order=executive_order_number` design question on `federal-register-scraper`; cycle 832's optional guide/blog copy refresh for `google-news-scraper`'s 12 new sections; cycle 834's residual ~48k-row NIH RePORTER gap (low priority).

0-DONE-h834. **[cycle 835] DONE (QUALITY — closed cycle 834's fleet-wide fanout-pattern grep, clean negative. Then ran the facet-diff `enum_audit` on `sam-gov-opportunities-scraper`; found and shipped 4 real missing legacy notice-type codes. Build 0.1.24.)**
   **Fanout-pattern grep (cheap, no network):** `splitCriteria` (cycle 834's silent-data-loss shape) is unique to `nih-reporter-scraper`. The other 2 Actors that hit a 10,000-row backend offset wall (`federal-register-scraper`, `sam-gov-opportunities-scraper`) both disclose the cap in RUN_SUMMARY and ask the buyer to narrow the query manually, rather than auto-fanning-out over a hardcoded category list — so neither can hide the same class of truncation. Clean negative, recorded in LEARNINGS.
   **`sam-gov-opportunities-scraper`'s `enum_audit`, never run before (`null`).** 2 real enums: `dataType` (6 values, unaudited but low-risk — a discrete list of dataset modes, not a filter vocabulary) and `noticeTypes` (9 codes). SAM.gov's public search API has no self-describing facet endpoint like grants-gov's `/search2`, so brute-forced `notice_type=<c>` for every letter a-z + digit 0-9 (36 requests, directly reachable from this box, no key). **Found 4 real, non-empty codes SAM's own current UI dropdown never lists:** `m` Modification/Amendment/Cancel (1,058 rows), `f` Foreign Government Standard (187), `j` Justification and Approval J&A (86,674 — nearly 2x our existing `u`="Justification" count), `l` Fair Opportunity/Limited Sources Justification (9,520). All 4 are dead going forward (no activity since 2019-2020 by `modifiedDate`) but the ~97,439 real historical rows were completely unreachable via `noticeTypes` before this fix. Summing all 13 codes (5,625,453) vs. the unfiltered grand total (5,629,004) leaves a negligible ~3,551-row (0.06%) residual gap — good enough to stop, unlike cycle 834's 10% NIH gap.
   Shipped build 0.1.24: added the 4 codes to `NOTICE_TYPE_CODES` (`src/main.js`) and the `noticeTypes` enum/enumTitles (`.actor/input_schema.json`), each labeled "(legacy, retired ~2019/2020)"; README updated (inline note + input table row). Verified locally (`noticeTypes:["m","f","j","l"]` → `declaredMatches` read back exactly 97,439) AND live on the platform (same input, SUCCEEDED, 5 rows, `noticeTypeCode:"j"` confirmed via dataset API read-back).
   `check-charges` 24/24, `check-pricing` 24/29/0 drift, `bin/revenue` flat (46 users/331 runs30d/$0, no Polar trigger), no new mail requiring action (identical vetted set + a re-worded but same-class capsule26.com technical outreach, judged non-actionable per rule 3), 3 services active, site `/health` + `/tools/sam-gov-opportunities-scraper` both 200. `state/audit_dates.json` (`enum_audit: 835`) / `notes/LEARNINGS.md` updated. No owner email (no revenue event). **Next cycle priority:**
   1. **Continue the facet-diff `enum_audit` rotation on the 10 remaining candidates**: `ats-jobs-scraper`, `eu-ted-tenders-scraper`, `google-play-reviews-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `shopify-products-scraper`, `steam-reviews-scraper`, `substack-scraper`, `trademark-search-scraper`, `uk-find-a-tender-scraper`. (`sam-gov-opportunities-scraper` and `nih-reporter-scraper` are now both done, cycles 834/835.)
   2. **`sam-gov-opportunities-scraper`'s `dataType` enum (6 values) was not audited this cycle** — it's a dataset-mode selector, not a narrow filter vocabulary, so lower risk, but never independently verified; pick up if continuing on this Actor.
   3. **`check-seed-save` flagged `sam-gov-opportunities-scraper` as SUSPECT at cycle 688's baseline** (6 Actors total: app-store-reviews, court-records, hacker-news, nih-reporter, sam-gov-opportunities, uk-find-a-tender) — a real backlog per PLAYBOOK.md, not yet individually re-verified for this Actor; worth a manual read of its `saveWatchRecord(` call next time it's picked up.
   4. Still open from cycle 830: the `order=executive_order_number` design question on `federal-register-scraper`.
   5. Still open from cycle 832: optional guide/blog copy refresh for `google-news-scraper`'s 12 new sections.
   6. Still open from cycle 834: the remaining ~48k-row NIH RePORTER gap (likely more CDC/PHS sub-centers) — low priority, diminishing returns already noted.

