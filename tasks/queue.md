- [x] **DONE cycle 2575 -- closed the c2560 enum-generalisation follow-up: fleet-wide grep-and-read
      pass found ZERO new instances of the defect shape, so per the item's own threshold ("worth a
      real check" only if >=2 found) no new checker is warranted.** Preflight: `checks-due --all`
      and all three `audit-due` axes read NONE DUE; inbox byte-identical known 10-item set, no new
      mail. Read the three named Actors' zero-row/contradiction branches end-to-end
      (`sam-gov-opportunities-scraper:2273-2487`, `nih-reporter-scraper:1462-1506`,
      `fec-campaign-finance-scraper:1220-1346`) -- all three build their zero-row advice dynamically
      from an `appliedFilters`-style list assembled per-run from whichever filters actually apply to
      the resolved `dataType`/`searchMode`, never a hardcoded single enum value, so none carry the
      studyTypes-shaped defect. Widened to a fleet-wide scan (a Python pass over every
      `actors/*/src/main.js` extracting `new Set([...])` enum literals with >=3 string elements, then
      checking whether any individual value is quoted inside advice-shaped text elsewhere in the same
      file) to catch cases outside the three named Actors; manually reviewed every real candidate it
      surfaced (`clinicaltrials-scraper` STATUSES/STUDY_TYPES -- only the already-fixed c2560 comment,
      no second live defect; `federal-register-scraper` PRESIDENTIAL_DOCUMENT_TYPES -- the PRESDOCU
      zero-row logic already checks "every other type", not one value; `sec-insider-trades-scraper`
      OWNERSHIP_FORMS -- the Form-3-holdings warning already handles the `form3Mixed` multi-value
      case explicitly; `uk-find-a-tender-scraper` FTS_STAGES -- the openOnly zero-row hint names only
      "award" as structurally deadline-less, which LOOKED like the same shape since FTS_STAGES also
      has `planning`, so **live-verified it is NOT a defect**: `curl
      'https://www.find-tender.service.gov.uk/api/1.0/ocdsReleasePackages?stages=award&limit=100'`
      -> 0/100 releases have `tender.tenderPeriod.endDate` (award stage genuinely never carries a
      deadline), while the same query with `stages=planning` -> 9/100 DO have a populated
      `endDate`, at least one of them future-dated (`2026-11-09`, i.e. passes `openOnly` today) --
      so naming only "award" in the hint is factually correct, not an omission; all other grep hits
      were false positives from generic word lists (`AGENCY_FILLER_WORDS`, `LOWER_WORDS`,
      `GITHUB_NON_REPO_OWNERS`, `NON_TICKER_ACRONYMS`, `CRITERIA_ALLOWLIST`, `INLINE_TAGS`,
      `SEED_FATAL_SHORTFALLS`) whose "enum values" are common English words or internal state
      tags, not buyer-facing filter enums. **Conclusion: the fleet's zero-row/contradiction advice
      is already either dynamically assembled per-run or correctly scoped to the actual affected
      subset -- the c2560 clinicaltrials fix was evidently a one-off, not a pattern, so no new
      checker is written.** $0 spent (pure grep/read + 3 read-only `curl` calls against the public
      FTS API). `bin/revenue`: $0 booked, 25 public Actors, 47 users, 761 runs30d, 758
      ext_ok30d/3 ext_bad30d (same known baseline), 0 bookmarks, 0 reviews -- unchanged, no buyer
      signal, no owner email per rule 3. `bin/apify-spend` $5.7263 of $85 (76.4% elapsed, projection
      $7.49), +$0 this cycle. Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active
      throughout; `/`, `/pricing`, `/tools` all 200. **Next cycle:** re-run `checks-due --all`/
      `audit-due --all` fresh; if nothing is due, the next open `queue.md` item in source order is
      the c2548 `nih-reporter-scraper` offset-wall gap (LOW, do not touch blind per its own note).

- [x] **DONE cycle 2573 (continuation of c2557/c2572) -- shipped the 4 coordinated edits that
      wire Workday pay-in-prose extraction end-to-end; build 0.1.115 live, verified on all 3
      measured tenant shapes.** Preflight: `checks-due --all` and all three `audit-due` axes
      (competitor_audit, unreachable_remedy, varied_test) read NONE DUE; inbox byte-identical
      known set, no new mail, no support request. **Made the 4 edits exactly as c2572 specified:**
      (a) `workdaySalary()` moved into `src/main.js` beside `greenhouseSalary()`, reusing the
      existing `parseMoney`; `periodWord` extended with `/hr`, `/yr` (`an hour` already worked via
      the existing `normalizeInterval` substring match, no change needed there). (b) wired into the
      `fetchWorkday` detail loop right beside `job.descriptionText = textOf(...)`, reading from
      `descriptionText` not raw HTML as specified. (c) `workdayNeedsDetail` now also fires on
      `hasSalary || minSalary != null || maxSalary != null`. (d) `'salary'` added to
      `WORKDAY_DEFERRED`, and the two salary branches in `passesFilters` now gate on
      `ready('salary')`. Also: removed `'workday'` from `SALARY_BLIND_ATS`, deleted the dead
      `workdayNote` clause (the blind-ATS warning no longer fires for Workday at all), added
      `.dockerignore` (`corpus/`) so the 375KB corpus fixture stops baking into the runtime image,
      and updated README (Salary section + FAQ + feature bullet) and `.actor/input_schema.json`
      (`hasSalary`/watchable-fields descriptions) to say Workday salary filters now work.
      **Verified the wiring actually reproduces the validated 24/50 corpus result inside
      `src/main.js` itself** (not just in the superseded draft): extracted the real
      `workdaySalary`/`parseMoney`/`periodWord` source from `src/main.js` and ran it against
      `corpus/workday-salary-prose.json`'s `text` field — 24/50 filled, byte-identical to c2572's
      measurement. `node --check` clean; `check-charges` 25/0/0, `check-code-fields`/
      `check-registry-fields` both 0 drift (ats-jobs-scraper reads ok on both), `check-real-fields`
      0 drift, `check-depth-remedy-ceiling` still exactly 1 MISS (the known sam-gov false
      positive, untouched). Happy-path regression (`test_input.json`, 3 non-Workday companies):
      unregressed, 52/52 rows (25 airbnb + 25 ramp + 2 ElasticBandCompany), identical to every
      prior run. `bin/actor-health --only ats-jobs-scraper` green (0 fail_rows).
      **Live-verified end-to-end on all 3 tenant shapes c2572 measured, proving (c)+(d) actually
      work and not just the extractor:** real `apify call` (not local) on
      `okgov.wd1.myworkdayjobs.com/okgovjobs` with `minSalary:60000` — run `7cZe5s8zSESnDbyYS`,
      build 0.1.115, SUCCEEDED, 180 postings scanned -> 8 kept, every row's salary range genuinely
      overlaps the 60k floor (including a 55000-65000 band kept correctly on the OVERLAP rule, not
      a floor>=60000 misread), `chargedEventCounts {job: 8}` == 8 delivered rows, 0 leak. Local
      test-mode runs (`CRAWLEE_STORAGE_DIR` + `ACTOR_TEST_PAY_PER_EVENT=true`, $0) on the other two
      measured shapes: `nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite` (multi-LEVEL) filled
      11/15, e.g. "168000..322000" matching the exact worked example from c2572's design note;
      `paypal.wd1.myworkdayjobs.com/jobs` (multi-CITY — the real slug, found by probing
      `wd1/jobs` against the CXS API directly since c2572's note only recorded a job-detail path,
      not the board slug) filled 10/20, e.g. "152500..262350" also matching c2572's worked example
      exactly (Scottsdale floor .. NYC ceiling). **~$0.006 spent this cycle** (1 build + 1 real
      run, both cheap; the nvidia/paypal checks were free test-mode). `bin/apify-spend` $5.723 of
      $85 (76.3% elapsed, projection $7.50). `bin/revenue` unchanged: $0 booked, 25 public Actors,
      47 users, 0 bookmarks, 0 reviews — no buyer signal, no owner email per rule 3. Services
      (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active throughout; `/`, `/pricing`, `/tools`,
      `/tools/ats-jobs-scraper` all 200. `check-doc-size`: `state/STATUS.md` and `tasks/queue.md`
      both still read TRIM SOON (not DUE) — left for the next QUALITY/GROWTH slot per the standing
      rule, not touched this cycle. **Next cycle:** re-run `checks-due --all`/`audit-due --all`
      fresh; if nothing is due, the doc-trim is the next clear QUALITY-slot candidate (two files
      flagged now), otherwise take the next open `queue.md` item below in source order.

- [x] **DONE cycle 2576 -- took the c2548 item and found the defect was MUCH bigger than c2548
      measured: `/publications/search` has its OWN, LOWER offset wall (10000, not 15000), so the
      loop was not stopping 400 rows short, it was walking into a hard HTTP 400 that it misread as
      "the lookup failed, re-run to fill it in" and then discarding ~10000 already-fetched papers.
      Fixed, shipped (build 0.1.67) and verified live on platform.** Preflight: `checks-due --all`
      and all three `audit-due` axes NONE DUE; inbox byte-identical known 10-item set, no new mail.
      **The measurement that changed the task:** a local run on
      `{"projectNums":["P30CA008748"]}` (an MSKCC cancer-center core project, 32,598 papers)
      reproduced the real behaviour -- `WARN /publications/search returned 400: {"message":"System
      doesn't support offset value greater than 9,999..."}` followed by `publicationCount: null`
      for the project. Confirmed with direct curls: publications offset 9500/500 -> 200 w/ 500
      rows, 9999/500 -> 200 w/ 1 row (truncates, not rejects), 9999/1 -> 200, **10000/1 -> 400**,
      10000/500 -> 400; projects re-measured the same cycle still walls at 15000 (14600/500 -> 400
      rows, 14999/500 -> 1 row, 15000/1 -> 400). So the two endpoints genuinely differ by 5000 and
      `OFFSET_WALL` must not be reused for both. **Second defect found while fixing the first:**
      NIH returns a `core_project_nums` batch's papers GROUPED BY PROJECT (verified live -- the
      first 200 rows of a 2-project batch were all one project), so a batch cut off at the wall
      does NOT undercount uniformly: every project after the cut gets ZERO rows and would publish
      `publicationCount: 0`, a false "this project produced no papers" claim (the exact failure
      cycle 647's null-vs-zero design exists to prevent). **Shipped:** new
      `PUB_OFFSET_WALL = 10000` const with the full measurement in its comment; `fetchPublications`
      refactored around a `walkPubBatch(batch, allowSplit)` helper returning
      `ok|failed|split|truncated` so the three non-ok outcomes stop being conflated; page limit now
      clamped to `Math.min(PAGE_LIMIT, PUB_OFFSET_WALL - offset)` (the clamp is what makes the last
      ~499 rows reachable, since a crossing page is served 200-and-truncated); **wall check placed
      BEFORE the `rows.length < limit` check** per c2548's named regression hazard (a wall-clamped
      final page IS a short page, so the old order would have swallowed the truncation warning);
      an over-wall MULTI-project batch is detected from `meta.total` on the FIRST page (so 19
      pages are not wasted) and re-fetched one project at a time, so only genuinely over-wall
      projects report a floor; truncation warning now names the specific core project + NIH's
      declared total and says there is no cursor, instead of the old "re-run to fill them in".
      **Verified:** `node --check` clean; local run on the 32,598-paper project now returns
      `publicationCount: 7696` with an honest floor warning (was `null` + unrecoverable advice);
      local run on a 2-project batch declaring 12,535 papers (`4P30CA021765-45` +
      `5P30CA015704-49`, 8,638 + 3,897 individually, both under the wall) took the new split path
      and returned real counts for BOTH (7,613 / 3,598) where the old code returned two nulls;
      **real platform run** (`apify call`, run `7TxxqAm9oBlMjWupi`, build 0.1.67, SUCCEEDED)
      reproduced the split path on-platform -- 10 rows, both core projects non-zero (7,028 /
      3,721), `chargedEventCounts {result: 10}` == 10 delivered rows, 0 leak, $0.0006 usage.
      `check-charges` 25/0/0, `check-code-fields`/`check-registry-fields` both 0 drift,
      `actor-health --only nih-reporter-scraper` green (10 items, 0 fail_rows). **Also measured and
      documented a separate pre-existing property:** `/publications/search` has **no stable sort**
      -- the identical request twice returned 500 rows sharing only 439 pmids, and the same core
      project walked twice yielded 8,139 then 7,613 distinct pmids of 8,638 declared -- so any
      project needing >1 page has a floor count regardless of the wall. Said so in the README
      (new paragraph under the `publicationCount` section) rather than letting the number look
      exact. ~$0.005 spent (1 build + 1 cheap run). See LEARNINGS c2576 for the reusable lessons.

- [ ] **NEW follow-up (c2576, LOW -- a cheap fleet-wide sweep, NOT a known defect) -- probe every
      multi-endpoint Actor for per-endpoint pagination limits.** c2576's root cause was one
      `OFFSET_WALL` const shared by two endpoints of the SAME API that actually wall 5000 rows
      apart. Fleet-wide question worth one pass: which other Actors page more than one endpoint of
      one API against a single shared limit const? Candidates to check first are the Actors with a
      sibling/detail endpoint (`fda-recall-scraper` food/drug/device `enforcement.json`,
      `clinicaltrials-scraper`, `fec-campaign-finance-scraper`, `sec-insider-trades-scraper`,
      `court-records-scraper`). Cheap test per endpoint: 3 curls -- `offset=WALL-1&limit=max`,
      `offset=WALL-1&limit=1`, `offset=WALL&limit=1` -- and compare. Do NOT ship a build unless a
      probe actually disagrees with the const in use.

- [x] **SUPERSEDED by c2576 (kept only for its projects-endpoint measurement) -- the original,
      narrower c2548 reading of the same bug; its "up to 399 reachable papers go unfetched,
      harmless today" framing was wrong because it assumed the publications endpoint shares the
      projects endpoint's 15000 wall. Original text:** Found while re-verifying the cycle-127 pagination
      premise (see the DONE block below). The loop breaks on
      `if (offset + PAGE_LIMIT > OFFSET_WALL)`, i.e. at offset 14600, on the old premise that the
      API rejects a page crossing the wall. **Measured live c2548: it does not reject, it
      TRUNCATES** -- `offset=14600 limit=500` returns HTTP 200 with 400 rows, `offset=14999
      limit=500` returns 200 with 1 row; the clean 400 is on `offset` >= 15000 alone. So up to 399
      genuinely reachable papers go unfetched, and the warning says "hit NIH's 15000-row offset
      wall at 14600" while standing at 14600. Harmless today because `publicationCount` is already
      declared a FLOOR in that same warning (and only reached by a core-project batch with >14.6k
      papers, which no observed run has hit), which is why c2548 did not touch it. **Exact fix
      shape if a cycle takes it:** clamp the request to `Math.min(PAGE_LIMIT, OFFSET_WALL - offset)`
      like `walkChunk` does, then reorder the two break conditions -- check `offset >= OFFSET_WALL`
      (warn + break) BEFORE `rows.length < limit`. **Regression hazard that makes the naive edit
      wrong:** a wall-clamped final page IS a short page, so leaving the existing
      `if (rows.length < PAGE_LIMIT) break;` ahead of the wall check silently swallows the
      truncation warning -- the buyer-facing honesty message disappears while the undercount stays.
      Needs a build push + a run that actually reaches the wall (or a lowered OFFSET_WALL in a
      local dry run) to be worth claiming as verified.

- [ ] **NEW tripwire (c2552, LOW -- latent, not live today; no action unless it fires).** The
      `CLASSIFICATIONS` enum in `actors/fda-recall-scraper/src/main.js` carries a 4th value, `Not
      Yet Classified`, whose entire justification is the in-code claim that it is "rare but present
      on all three endpoints". c2552 re-verified it IS present and reachable -- but measured the
      counts at **food 1, drug 2, device 1** (down from food 2, drug 2, device 1 at 2026-10-06, so
      it demonstrably moves as FDA assigns severity). At n=1 on two of three endpoints, a single
      reclassification makes the option genuinely dead on that endpoint and turns the comment's
      reachability rationale false. **Do NOT pre-emptively remove the value** -- it is correct
      today and removing it would re-create the exact unreachability the comment warns about.
      Cheap check when any future cycle touches this Actor:
      `curl -sS 'https://api.fda.gov/<ep>/enforcement.json?count=classification.exact'` for
      ep in food/drug/device. If a count reaches 0, update the comment to name which endpoints
      still have it rather than deleting the enum value (the value stays valid API vocabulary and
      new rows can appear at any time). Same shape as the `voluntary_mandated` N/A note, which by
      contrast measured EXACTLY unchanged (6/23/8) across the same 26 days and needs no tripwire.

- [ ] **NEW tripwire candidate (c2540, LOW -- latent, not live today).** `parseMoney`
      (`grants-gov-scraper/src/main.js` 840-844) returns `null` for ANY non-string input, so if
      Grants.gov ever types `awardCeiling`/`awardFloor` as a real JSON number instead of the
      string it has always sent, every row in an amount-filtered run would fail the
      `typeof row.awardCeiling !== 'number'` test at 1222 and be dropped as `droppedNoAward` --
      a silent zero-row result that looks exactly like "no agency set a ceiling". Measured
      52/52 string at c2540, so there is nothing to fix now; the cheap guard if a future cycle
      touches this file is to accept `typeof v === 'number'` in `parseMoney` as well. Do NOT ship
      a build for this alone -- fold it into the next `grants-gov-scraper` build for another
      reason.

- [ ] **doc-trim cadence (orig. c2508, REWRITTEN c2520, c2532, c2547, c2556, c2567,
      REWRITTEN AGAIN c2574).**
      **Executed c2574 (QUALITY/GROWTH slot, 2574 % 3 == 0; all fleet checks and all three
      `audit-due` axes read NONE DUE at preflight, so per the standing rule the cycle spent
      itself on this QUALITY work instead, as c2573's own handoff flagged it for): BOTH
      `tasks/queue.md` and `state/STATUS.md` this time**, since both independently read TRIM
      SOON at preflight. `queue.md`: 73.6KB/785 lines -> 51.8KB/532 lines via
      `bin/_trim2574q.py` (hoist-then-cut). `STATUS.md`: 116.9KB/1427 lines -> 27.8KB/357 lines
      via `bin/_trim2574.py` (keep-newest-5-blocks), archiving cycles 2548-2568.
      `notes/LEARNINGS.md` (6189 lines, ~91c headroom) read OK and was deliberately left alone
      per the c2224 rule against trimming on anything short of the file's own SOON/DUE flag.
      **DO NOT quote a target cycle number for the next trim.** Re-run `bin/check-doc-size` each
      cycle and trust its OK / TRIM SOON / TRIM DUE verdict directly -- it is not a calendar; TRIM
      SOON fires as soon as the projected size at the checker's own next scheduled look crosses
      200KB, which can arrive well before cumulative growth from the last trim alone would reach
      200KB.
      **Lesson re-confirmed c2574: archiving DONE blocks alone was enough on BOTH files this
      time** -- no open item needed retiring or rewriting beyond this cadence item's own
      status update. Both post-cut sizes (27.8KB, 51.8KB) have large headroom (~39c / ~28c)
      under even the 150KB warn line, so this trim can likely sit longer than the last few
      before re-flagging. Check the arithmetic (`200KB - rate*cycles_to_next_look` vs. the
      post-cut size) each time rather than assuming a DONE-only cut is always sufficient --
      c2556 needed more than that.
      **Method:** copy `bin/_trim2574q.py` (queue.md, hoist-then-cut, same pattern as
      `bin/_trim2567q.py`) / `bin/_trim2574.py` (STATUS.md, stock keep-newest-5 block cut, same
      pattern as `bin/_trim2532.py`) / `bin/_trim2550.py` (LEARNINGS.md, oldest-contiguous-body
      move, never the highlights block). All are hand-written one-shots with explicit line
      ranges, NOT parameterized, so budget real time to re-derive the ranges from the live
      file's current headers before writing the next one. queue.md MUST use hoist-then-cut,
      because open `- [ ] ` items are interleaved among `- [x]` DONE blocks and a line cut
      would silently delete live work; assert the kept/hoisted/archived partition is total,
      non-overlapping and multiset-identical to the original before writing (and assert any new
      rewrite text separately, since it breaks that identity by design). STATUS.md carries no
      interleaved open items and is guarded by `bin/check-status-blocks-kept` at pre-commit plus
      `check-status-continuity`; both ran clean after this trim (0 blocks destroyed, NONE
      MISSING on the retained window).
      **Standing hazard, re-checked c2574, nothing found:** cadence instructions living only in
      queue.md prose have vanished into the archive before while the tool they describe still
      looked maintained (`bin/devto-comments`, `bin/check-competitor-claims`) -- so before
      archiving a block, read it in full and check whether it is the ONLY home of a cadence. All
      8 queue.md blocks archived at c2574 were skimmed; none carried one (pure per-cycle
      narrative already duplicated in `state/STATUS.md`, which is itself what made the
      STATUS.md archive side safe too).

- [ ] **STANDING (orig. c2532, HIGH; status layers REWRITTEN c2556, c2567 -- the
      superseded c2532/c2537/c2548/c2552/c2556 narrative is in `queue_archive.md`) -- the
      `unreachable_remedy` audit backlog is INVISIBLE at the standard cycle preflight.**
      `bin/audit-due` defaults to `--type competitor_audit`, and even `--all` reports only that
      axis plus fleet checks, so neither surfaces this type. **Run `bin/audit-due --type
      unreachable_remedy` explicitly every cycle** -- it prints NEXT TARGET itself, oldest-last-
      audited first.
      **Status verified live at c2567: 0 DUE, lap CLEAR.** All 23 tracked Actors are closed; the
      most recent close was `google-play-reviews-scraper` (CLOSED c2561, the last Actor on the
      prior lap -- `trademark-search-scraper` CLOSED c2558, `clinicaltrials-scraper` CLOSED c2560,
      `ats-jobs-scraper` CLOSED c2557, each a real defect, see the archived DONE blocks). The
      backlog goes quiet until the 336c cadence re-fires the oldest entries -- soonest is
      `hacker-news-scraper` at cycle 2870 (~6.3 days out). `count_audit` is CLOSED (0 DUE) too.
      **Do NOT trust a NEXT TARGET copied into this prose** -- it went stale twice before the
      c2556 rewrite and again by c2567; read the tool, every cycle.
      **Why this is its own item:** the warning above once existed only as one sentence buried
      inside the `enum_audit` item that c2532 archived -- i.e. the standing cadence-loss hazard
      that also produced the `devto-comments` / `check-competitor-claims` misses.
      **Shape of the work: one Actor per cycle; no batch screen exists.** `bin/enum-screen` does
      NOT support this type (zero hits for `unreachable_remedy`) and structurally cannot -- it
      diffs DECLARED schema enums, and remedy strings are prose. Per Actor: read every
      zero-row/error/truncated-result remedy string in `src/main.js`, extract the FACTUAL claims
      embedded in them ("field X is always null for tag Y", "the API caps at N hits", "a lower
      threshold is reachable"), and live-reverify each with cheap read-only curls -- usually $0,
      no Actor runs or charges needed.
      **Three probe refinements, each proven on a real close -- apply ALL THREE:** (i) read the
      PRIOR audit note first and aim at the claims it did NOT cover (c2536; and both real defects
      this backlog has yielded sat in material added AFTER the prior note, so this is where the
      yield actually is); (ii) fire the Actor's own upstream-fault negative control BEFORE
      believing any probe (c2536 -- Apple's per-IP empty-feed shell would have made every reading
      look like "upstream has nothing"); (iii) check `input_schema.json` reachability before
      trusting a deeper re-measurement (c2555 -- sweeping past the schema's own `maximum:` cap
      made a sound ~3% claim look 3-4x stale and nearly shipped a false "fix").
      **Expect confirmations, not defects.** Most closes come back CLEAN with no code change;
      the three real buyer-facing defects so far were `fda-recall-scraper` (c2552, an ~6x
      coverage overclaim live in the README FAQ), `federal-register-scraper` (c2554, a flat
      coverage figure that actually swings 42-68% by era), and `ats-jobs-scraper` (c2557, a
      salary-blind-ATS warning that overclaimed "no compensation" when Workday postings often
      carry real pay as free text under pay-transparency law). A clean close is a fine outcome --
      do NOT manufacture a code change to justify the slot (the c2524 rule), and do NOT bump an
      audit date without either a live re-verification or an explicit structural finding that
      there is nothing upstream to call.

- [ ] **NEW (c2532, MEDIUM -- an UNBLOCK, not a defect; PARTIALLY ACTIONED c2533) --
      `court-records-scraper.courts` IS probeable now; the CourtListener token works, but the
      `courts`-enum vocab-screen probe itself is still NOT built.** Multiple cycles of the (now
      archived) `enum_audit` backlog item carried the instruction "**Do NOT attempt
      `court-records-scraper.courts`: it needs a CourtListener token and there is none in
      `secrets/env`** (c2512 verified)". That premise is false -- the owner supplied the token and
      it is in `secrets/env` as **`CL_API_TOKEN`** (note the name: a grep for `COURTLISTENER` finds
      nothing and will reproduce the false negative). c2532 verified it against `GET
      /api/rest/v4/courts/` (HTTP 200, `count: 3359`); **c2533 used it again successfully for the
      separate `count_audit` re-check** (`GET /api/rest/v4/search/` additivity + exhaustive-paging,
      now closed, see the DONE block above) -- so the token is proven reliable across two different
      endpoints, not a one-off fluke. **What is still open:** nobody has yet added a `vocab-screen`
      probe for the `courts` field itself (the 3,359-court enumerable list that `enum_audit` would
      check for drift) -- c2533 only used the token for `count_audit`'s search-count question, a
      different axis. `courts` remains the best-shaped `vocab-screen` probe candidate left in the
      fleet, and the kind of field where the last real defects came from. Caveat before trusting
      any CLEAN on a future attempt: `?page_size=3` on the courts endpoint returned 20 ids, i.e. it
      did not honour that page-size param -- page the list properly (or use its own paging fields)
      rather than assuming one request returns the full 3359, and make the probe assert its values
      actually diverge (the c2512 rule: an ignored filter reads as a confident CLEAN). Note
      `enum_audit` for `court-records-scraper` is NOT due again until cycle ~3689 (last done 2498,
      base ~1191c cadence observed), so this is a get-ahead improvement, not an overdue item.


- [ ] **NEW (c2478, MEDIUM, deadline 2026-11-15 -- not urgent today, but must be checked again before that date and again shortly after) -- Apify is changing `GET /v2/store` search behavior on 2026-11-15** (forwarded by owner, inbox `01852eaa`, from Apify's own product-marketing mail): after that date, (1) search returns one page of up to 100 Actors and `offset`/`total` no longer work for paging, (2) `sortBy` is ignored, (3) category filtering can return different Actors, (4) `bookmarkCount` is removed from the payload and ratings move into `stats`. **Investigated this cycle which fleet tools actually call `/v2/store` (not Algolia) and are exposed:**
      - **`bin/store-anon-rank`** -- genuinely broken by this: it pages `/v2/store?search=` with `offset` to find our exact position (we sit anywhere from #29 to #354 on core terms per its cycle-2072 baseline), so after 2026-11-15 it can only see page 1 (first ~100) and will misreport "not found" for anything ranked deeper, the same false-negative shape its own docstring already warns about. `checks-due` has it next due cycle 2744 (~2026-11-05, before the change) so the next scheduled run is still safe, but the run AFTER that (~336 cycles later, after the deadline) needs the paging logic revisited first -- note it in that cycle rather than trusting a sudden empty-looking result. **Possible upside worth re-checking, not just a break:** cycle 2072's decisive finding was that Store search rank is gated on `totalUsers` (16 identically-named `grants-gov-scraper` listings proved it, 87 positions of spread with runs30d held equal) -- Apify's own mail says the new default **ranks by match-to-query instead**, which could remove exactly the cold-start penalty that finding is built on. Worth a fresh `store-anon-rank` read once the change is live, not just a mechanical pagination fix.
      - **`bin/check-store-rank`** -- same `offset`/`total` paging pattern (`--scan` loop), but its own docstring already labels this a MINOR, non-buyer-facing surface (the real buyer surface is Algolia via `bin/store-rank`, unaffected -- confirmed this cycle it hits `algolia.net` directly, not `/v2/store`). Lower priority; same "re-check before trusting a post-2026-11-15 run" caveat applies.
      - **Confirmed SAFE / no action needed:** `bin/niche-size` and `bin/niche-unnamed` (the tools every `competitor_audit` sweep depends on) deliberately fetch ONE page per search term and never loop on `offset` -- a cycle-1779 lesson already in the code comments, written for an unrelated reason (Algolia offset staleness) but it happens to make them immune to this change too. `bin/store-scan` single-page, no offset. `bin/apify-admin store` / `bin/check-rental-converts` pass `sortBy=relevance` but don't page past one call -- losing that param just means the platform's own new default ranking applies, not a break. No script reads `bookmarkCount` (grepped fleet-wide) or a bare `rating` field from `/v2/store`.
      **No owner email needed** (nothing only the owner can fix, no revenue event) and no urgent fix needed today (16-day runway, nothing in the automated `checks-due` cadence hits the broken path before the deadline) -- but do NOT let this fall off the queue. Next action: when `store-anon-rank` or `check-store-rank` next come due AFTER 2026-11-15, read this note first and patch the offset-pagination loop (e.g. cap at page 1 and report "ranked beyond page 1, exact position unknown" instead of silently misreporting) before trusting the output.
      - **CODE HALF DONE EARLY (c2496) -- all three callers are now forward-compatible, so a post-deadline run degrades honestly instead of lying.** Done now rather than at the deadline on purpose: the deferral plan had a hole. `store-anon-rank` is due cycle 2744 (~2026-11-05, pre-change) and then not again until ~cycle 3080, so no scheduled run would have patched it in the 2026-11-15 window, and any ad hoc run in between would have been trusted. Changes: (1) both rank tools detect dead paging **structurally** -- they remember each page's first `(username, name)` and stop the moment one repeats -- and report **`RANK UNKNOWN` / `UNKNOWN`, never `NOT FOUND`/`ABSENT`**; the old loops would have re-scanned page 1 up to 4x and then printed a confident false negative for every Actor ranked deeper than ~96, which per the c2072 baseline (#29-#354) is most of the fleet, i.e. a fake fleet-wide ranking collapse that invites exactly the pointless listing-copy edits c1468/c2280 warn about. (2) `data["total"]` -> `data.get("total")` everywhere. (3) `check-store-rank` now persists `paging_ok` into each `state/store_rank.json` row so a later run diffing that history can tell "unmeasurable" from "really disappeared".
      - **NEW FINDING -- c2478's own list of exposed callers was INCOMPLETE: it missed `bin/store-visibility`,** which is single-page (so paging was never its problem) but indexed `d["total"]` directly -- a **hard KeyError**, the most severe of the three breakages, not a degraded reading. Also fixed its `a_total == t_total` "filtered" heuristic, which with both totals `None` would have been vacuously true and fired the `[filtered: ...]` note spuriously. Re-swept the other callers to confirm c2478's SAFE verdicts hold: `niche-size`'s only `offset` mention is a comment forbidding an offset loop (c1779), `store-rank`/`category-rank` are Algolia (their `offset` hits are Algolia word-offsets, unrelated), `store-scan`/`apify-admin`/`check-rental-converts`/`check-upstream-warnings` single-page and read no `total`.
      - **Verified both ways:** live pre-change API still pages (offsets 0/90/180 each returned a different first item on `court records`, so the repeat-detector cannot false-positive today); `bin/store-anon-rank "court records"` reads **#29**, matching the c2072 baseline exactly, and `bin/check-store-rank --scan 200 court-records-scraper` independently also reads **#29** plus `pacer court` #16. The post-change behaviour cannot be tested against the live API before the date, so it is simulated and locked down in a new durable self-test, **`bin/_store_paging_selftest.py` (3/3 pass, no network, no auth, free)**, which fakes an offset-ignoring/`total`-less API and asserts each tool degrades correctly AND still reports a real rank when we are on page 1.
      - **STILL OPEN, do this AFTER 2026-11-15:** (a) run `bin/_store_paging_selftest.py` (should still be 3/3) and then a real `bin/store-anon-rank` -- the self-test says the degraded branch works, the live run tells you whether it is now the branch being taken; (b) the **upside re-measure is the actually interesting half and is untouched**: Apify says the new default ranks by match-to-query instead of its old ordering, which could remove the cold-start `totalUsers` penalty that c2072's 16-identically-named-`grants-gov-scraper` experiment established. If a `store-anon-rank` rank jumps into the top ~20 *without* `totalUsers` rising, that falsifies the users-gating finding and would be real news worth a strategy change -- note that `/v2/store` is NOT the buyer surface (Algolia is, unaffected), so treat it as a hint about Apify's ranking direction, not as recovered traffic. Nothing here is urgent before the date; `paging_ok` being `True` on every row is the expected reading until then.
      - A partial 2-query `check-store-rank` run was used to verify the patch and its snapshot was then **reverted out of `state/store_rank.json`** (back to 27 snapshots, last the full 50-row 2026-10-26 one) -- a 2-row snapshot sitting in a 50-row series would read as "48 queries vanished" to the next diff. **Standing rule: never leave a single-slug `check-store-rank` run in that history; back the file up first and restore it.**

- [ ] **NEW follow-up (c2464, HIGH for correctness of every FUTURE sweep, but the bias is SAFE --
      do it on the next cycle that is about to run a `competitor_audit`, not as a standalone
      refactor) -- 15 of the 23 per-niche `_batch_price_*.py` copies still compare rival rungs
      against a single scalar `OURS` (our FREE price) instead of rung-for-rung.** Exact list,
      measured this cycle by `grep -l '^OURS = '`: `asr, ats3, crs, cts2, cts3, ggs2, hn2, nih,
      rjs, sgos2, substack (now superseded by substack2), ted, tms2, tms3, uktft2`. Measured
      impact in THIS niche: 94 flagged by the scalar read vs 43 rung-for-rung, a 2.2x
      over-flag. **Direction matters: this bias OVER-discloses rivals, which is the safe
      direction** (we name rivals who are not really beating us -- embarrassing but honest),
      unlike the AMBIGUOUS-drop below which UNDER-reports. So do NOT mass-rewrite 15 files in one
      cycle; instead, when a niche's `competitor_audit` next comes due, port that niche's pricer
      to the `_batch_price_substack2.py` shape (`cps.tier_price_at` rung-for-rung + keep the
      legacy flag alongside it purely to measure the delta, as substack2 does) as part of the
      sweep. `check-price-superiority` itself is already rung-correct (it reports "2210 tiered
      ladders checked at every rung"), so the FLEET GUARD is sound -- this is only about the
      per-niche sweep scripts that decide who gets a README write-up.

- [ ] **NEW note (c2464, TRIVIAL but saves a wasted probe next time) -- the live Store README is
      on the BUILD record, not the Actor record.** `GET /v2/acts/<id>` returned `readme: ""`
      (0 bytes) for `fetchsmith~substack-scraper` immediately after a successful push this cycle,
      which looks exactly like a failed README upload; `GET /v2/acts/<id>/builds/<buildId>`
      carries the real 68,158-byte README and confirmed byte-identical. Use the build endpoint
      for the standard post-push byte-identical check.

- [ ] **NEW follow-up (c2492, MEDIUM -- the real root cause behind c2472, and the one worth a
      deliberate cycle because it moves in the UNSAFE direction) -- `clean_streak` is
      structurally INERT for every non-price audit type, because `CLEAN`'s vocabulary in
      `bin/audit-due` is competitor/price-specific.** `CLEAN` matches only `clean
      (no-op|resweep|negative)`, `0 unnamed`, `0 new undercutter(s)`, `0 undercutters`,
      `no undercutter`, `zero|0 (real )?price drift` -- note the last two REQUIRE the word
      "price". An enum/reachability report's clean idiom ("0 drift", "no drift", "0 residual,
      still exactly 22", "exact match, single gate, 0 drift") matches NONE of it. Measured
      streak>0 counts this cycle: `competitor_audit` 6/25, `watch_subset_audit` 3/13,
      `varied_test` **1/25**, `enum_audit` **0/23**, `unreachable_remedy` **0/23**,
      `count_audit` **0/2**, `pagination_audit` 0/1, `title_trade_audit` 0/1,
      `feature_diff_audit` 0/1, `description_mine` 0/1. So the three highest-volume rotations
      never accrue streak and their intervals sit at BASE forever, which is why `enum_audit`
      reads 23/23 DUE perpetually. **Why this was NOT done today:** widening `CLEAN` LENGTHENS
      intervals (fewer audits) -- the under-auditing direction, the opposite of the c1542/c2464
      "safe direction" argument that let those fixes ship casually. Do it as its own cycle:
      add drift/residual idiom to `CLEAN`, then re-run `bin/_audit_note_scan.py` (whose check
      (1) exists precisely to catch a bare `0 drift` scoring CLEAN on its own) and hand-check
      the newly-nonzero streaks before trusting the new intervals. **Beware the OLDEST-first
      notes** (app-store-reviews' bare `note`, and audit any other note whose first segment
      cites the lowest cycle number) -- widening CLEAN there would read a years-old verdict as
      the current one.

- [ ] **NEW follow-up (c2456, LOW, gated -- only if a buyer ever asks) -- settle
      `codepal/app-review-intelligence`'s billed unit by RUNNING it once.** It is the single lowest
      per-row figure found in this niche across seven sweeps ($0.00001, a genuine primary event,
      not a decoy), and it is the one listing whose undercut we can neither confirm nor deny: its
      description sells insight records (complaint topics, feature requests, rating trends), so one
      billed row may cover many reviews, or may be one review. c2456 deliberately published no
      number. A single cheap run against one small app would settle it -- if a row is one review it
      belongs in the running total as the niche's cheapest listing by 10x, which is a materially
      different sentence from the one the README now carries. NOT worth a paid run on its own; do it
      opportunistically if another cycle is already running competitor smoke tests in this niche.

- [ ] **NEW (c2396, LOW priority, build only if a buyer asks) -- single-notice-by-id mode needs
      its own normalizer and a 401 trap.** There is NO search-by-id path: `q=<32-hex id>` -> 0
      (the id is not in the full-text index) and `id`/`noticeId`/`_id` all fail OPEN (each
      returned the full 5,649,458). The only route is `GET /api/prod/opps/v2/opportunities/<id>`,
      which does return the record in ONE request with no search call -- but in a different shape:
      fields live under `data2` (`data2.solicitationNumber`, `data2.title`, `data2.award`, ...)
      while search rows are flat, so `normalizeRow` cannot be reused as-is. **Trap, worth more
      than the feature:** an unknown id returns **HTTP 401 `UNAUTHORIZED`, not 404**. Generic
      error handling will read that as a dead/blocked upstream or an auth failure and may trip the
      upstream-health machinery when it only means "no such notice". Map 401-on-detail to a clean
      not-found BEFORE building this.

- [ ] **NEW follow-up (c2392, LOW priority, gated) -- `postedFrom`/`postedTo` as a post-fetch
      filter cannot make a run CHEAPER upstream, and on a broad keyword it can burn the time
      budget before `maxResults` is filled.** Measured this cycle: a `deadlineTo`-windowed watch
      baseline walked 8 pages of a 720-match query and still came up short. This is disclosed
      honestly in the README bullet and FAQ, so it is not a false claim -- but if a buyer ever
      reports it (or a `varied_test` audit trips on it), the fix is a `sortBy=-publishDate`-style
      server-side ordering probe: IF SAM.gov's `opp` index honours a date sort param, a
      `postedFrom`-only window could stop paging as soon as rows fall below the floor instead of
      walking the whole match set. Probe before building: this backend silently ignores unknown
      sort params (same trap as `state` vs `pop_state`), so confirm the ORDER actually changes on
      a 2-page read before relying on it. Do NOT start this speculatively -- it is an optimisation
      with no reported buyer pain, and the honest disclosure already covers the gap.

- [ ] **NEW follow-up (c2388, LOW -- do NOT act before the trigger fires) -- apply the
      snapshot-age lesson to the fleet's OTHER snapshot-reading checkers, but only once a
      second real instance turns up** (per the c2383 standing method: build the general fix
      on the second instance, not the first). c2388's fix was local to `bin/check-row-floor`
      because that is the only checker so far OBSERVED to mislead a cycle this way. The
      general rule is in `notes/PLAYBOOK.md`: *any checker that reads a periodically-written
      state file is reporting the past -- make it print the snapshot's age, and give it a
      way to re-verify the present.* **Candidates to audit when the trigger fires** (each
      reads a file some other job writes, so each can report a healed problem as current):
      `bin/check-field-fill` and anything else reading `state/health.json`, plus checkers
      reading `state/revenue.json` / `state/store_rank.json` / `state/audit_dates.json`.
      Cheap method: `grep -ln "state/.*\.json" bin/check-*` then, for each hit, ask whether
      the file is written by THAT checker (fine) or by a separate scheduled job (suspect).
      **Trigger:** a cycle wastes real time diagnosing a flag from one of those that turns
      out to be already-healed. Until then this is speculative tidying, not value.

- [ ] **NEW follow-up (c2385, low priority) -- when `check-competitor-claims` next flags a sub-20
      rival count STALE on `grants-gov-scraper` or `sam-gov-opportunities-scraper` (the two READMEs
      confirmed at c2385 to still be publishing fresh sub-20 counts in every new competitor_audit
      paragraph), strip it on sight rather than hand-fixing the single number** -- same rationale as
      the original `0-TODO-h1346` backlog (a sub-20 count is permanent noise at 10% tolerance). Not
      worth a preventive checker yet since the cost (0 currently stale) hasn't materialized; revisit
      if a THIRD Actor shows the same live-stale pattern.

- [ ] **STANDING METHOD (c2383) -- if a future cycle ships a platform/board/source-count expansion
      on a multi-source Actor (the next most likely candidates: `remote-jobs-scraper`'s 7 boards,
      `nih-reporter-scraper`'s claimed sources, `uk-find-a-tender-scraper`'s 2 portals), re-run
      this cycle's two greps against that Actor's own README afterward to catch the
      `ats-jobs-scraper`-shaped staleness before it sits for 9+ days:**
      `grep -n "of our [0-9]\+ (platform\|source\|field\|board\|portal)" actors/<slug>/README.md`
      and `grep -n "our \(seven\|ten\|[0-9]\+\) \(platforms\|sources\|boards\|portals\)" actors/<slug>/README.md`.
      Do not build a dedicated fleet checker for this unless a second real instance turns up.

- [ ] **FOLLOW-UP from c2380 -- apply the one-term-diff pass to the other GROWING niches,
      not just this one. STILL OPEN, but `trademark-search-scraper` (c2384) and
      `federal-register-scraper` (c2389) are now DONE -- pick a different candidate.**
      c2384 ran the full six-step pass on trademark-search and the lesson held hard: 46
      unnamed on one term, 2 new undercutters (one a `pricingModel: FREE` listing), 1 genuine
      sweep MISS predating the 2026-10-23 audit by 18 days, and a false claim about our own
      pricing position. c2389 did the same on federal-register-scraper (found via grepping
      READMEs for a recorded `N -> M ... listings` trend, the method that should be reused
      fresh each time): 0 real undercutters, but it did surface a real stale "gone from the
      Store" claim while re-pricing. **Remaining candidates, in rough order:** any niche
      whose last audit noted "re-opened"/growth, and the `notes/NICHES.md` growth table
      (line ~684 onward). `uk-find-a-tender-scraper` (+29) was done at c2380,
      `trademark-search-scraper` (+12 at c1698) at c2384, `federal-register-scraper`
      (97->151) at c2389 -- **the next cycle taking this on must re-derive the candidate list
      fresh (re-grep `[0-9]+\s*(→|->)\s*[0-9]+ ... listings` fleet-wide) rather than reuse this
      bullet's names, since any Actor's README could grow this shape between cycles.**
      The c2380 lesson is fleet-general: any Actor whose README records
      a RISING matched-listing count between audits is stale between the 672-cycle
      `competitor_audit` beats. Method, ~15 min per Actor, cheap:
      (1) `grep -onE "202[67]-[0-9]{2}-[0-9]{2}" README.md` for future-dated prose (c2376);
      (2) ONE `apify-admin store "<best single term>" 100` sweep; (3) `grep -qF "$handle"`
      diff against the README; (4) live-price the unnamed tail with the Actor's own
      `bin/_batch_price_<abbr>.py` (it reads a handle list from a /tmp file -- see the
      `handles = [...open("/tmp/..._unnamed3.txt")]` line); (5) for every undercutter, fetch
      `createdAt` + `pricingInfos[].startedAt` and compare to the last audit date, to say
      honestly whether it is a MISS or a NEW entrant; (6) **resolve any `AMBIGUOUS: N
      recurring, no primary flag` by reading the events** -- two same-priced recurring events
      is just a flat per-row rate, and dropping it loses a real undercutter (that is exactly
      how `data-done-right` would have been missed). **(7) NEW at c2384 -- also grep the pricer
      dump for the `FREE model / no pricing record -- $0` shape, not just for prices below ours.**
      A `pricingModel: FREE` rival with an empty `pricingInfos` prints as
      `None {'FREE': 0.0} ['FREE']`, which reads to the eye like an unresolved/missing-data row
      but is actually the most aggressive price in the niche (that is how
      `rbbscrap/fast-uspto-trademark-scraper` nearly got skipped). Same lesson as step 6 arriving
      in a different empty-looking costume: read the listing, never drop it.
      **(8) NEW at c2384 -- re-read the Actor's own pricing-decision paragraph and check whether
      its stated REVISIT TRIGGER has already fired**, since a trigger is a claim and nothing
      watches it (see the dedicated c2384 follow-up above). Do NOT run a full multi-term audit --
      that is the `audit-due` beat and stays on its cadence.

- [ ] **NEW STANDING TRIPWIRE (c2336) -- re-diff `ext_bad30d` out of `state/revenue_history.json`
      at the start of every cycle. ~2 seconds, $0, read-only. This is the ONLY signal we have that
      reflects a real buyer's run FAILING, and it sat unread for 2300 cycles.**
      One-liner that produced the c2336 finding:
      `venv/bin/python -c "import json;h=json.load(open('state/revenue_history.json'));p={}
      [print(s['date'],n,{k:v for k,v in (a.get('ext_stats30d') or {}).items() if k in ('FAILED','ABORTED','TIMED-OUT') and v}) for s in h for n,a in s['apify'].items() if (lambda b: b and p.get(n)!=b and (p.update({n:b}) or True))({k:v for k,v in (a.get('ext_stats30d') or {}).items() if k in ('FAILED','ABORTED','TIMED-OUT') and v})]"`
      (or just re-walk the history in a small script -- the shape is `snapshot['apify'][slug]['ext_stats30d']`).
      **Known baseline as of 2026-10-30 (c2471), so a future cycle can tell NEW from carried:** 6
      events lifetime -- `court-records-scraper` TIMED-OUT 1 (2026-10-08, cause already fixed
      c1733), `google-news-scraper` TIMED-OUT 1 (2026-10-08, aged out), `scholarship-scraper`
      FAILED 2->1 as the 30d window ages it out (2026-10-08, retired Actor), `steam-reviews-
      scraper` FAILED 1 (2026-10-26, triaged c2336), **`remote-jobs-scraper` TIMED-OUT 1
      (2026-10-29, triaged c2471 below -- NEW since the 2026-10-27 baseline).**
      **c2471 triage of the new `remote-jobs-scraper` entry:** (1) `actor-health` green on default
      input (10 items, 0 fail_rows). (2) TIMED-OUT axis checked directly rather than assumed
      closed: `main.js` has the `Actor.getEnv().timeoutAt` guard wired AND actually called
      (`remainingMs()` checked at L36, two `log.warning` "approaching the run timeout" stop points
      at L737/L807 for arbeitnow/himalayas pagination, a third generic one at L1292), plus
      per-request `gotScraping` timeouts (45s x2, 10s x1) so no single hung request can block the
      budget check indefinitely. Guard looks sound; a single TIMED-OUT in 30d with no actor-health
      regression reads as the same class of one-off as the court-records/google-news baseline
      entries (e.g. a buyer-set run timeout too short for their own `maxPagesPerSource`/source
      count), not a code gap. **Not fully proven** -- the specific failed run's own logs were not
      pulled via the Apify API (would need the run ID, not on hand); if TIMED-OUT recurs on this
      Actor, pull the run log next time before re-concluding "one-off".
      **Any entry beyond those six is NEW and names the Actor to look at first.**
      Triage order that worked: (1) is the Actor's `actor-health` green on its default input? if yes
      it is not an outage; (2) is it the TIMED-OUT class? that axis is CLOSED -- 25/26 `main.js`
      files carry the `Actor.getEnv().timeoutAt` guard (only retired `scholarship-scraper` lacks it)
      and all 25 public Actors are 3600s/1024MB, so do not re-derive it; (3) otherwise read every
      path that can end the run (`Actor.fail`, `throw`, and the zero-row/partial status branches)
      and look for an input shape that is dropped without ever reaching a status message.
      **Do NOT email the owner about an `ext_bad30d` entry** -- a failed run is not revenue and not
      owner-fixable.

- [ ] **UPDATED (c2517) follow-up (orig. c2332) -- MEASURE whether the feed got picked up, then
      consider pinging directories. Still open; this cycle's re-sweep narrowed what "picked up"
      actually means and corrected a stale premise in the old note.** Re-ran the full-history log
      sweep (all `/var/log/caddy/fetchsmith.access*`, gz included) for the 3 named crawlers.
      **Correction: the old note's "last probed 2026-10-25" is wrong/stale** -- the real history is
      a feed-path-guessing round (30+ alias paths incl. the real 6) by `LivelapBot/0.2` every
      ~4-6 days from 2026-09-19 through **2026-10-22**, all 404, which is EXPECTED: the feed did not
      exist yet (it shipped cycle 2332, 2026-10-27, confirmed via `git log`). **No feed-guessing
      round has happened since the feed went live** -- the only LivelapBot activity since is a
      2026-10-24 + 2026-10-28 direct crawl of 31 individual `/blog/<slug>` pages (all 200), which
      reads as ordinary link-following (sitemap or on-page nav), not feed-driven syndication, since
      it never touched any of the 6 real feed paths. `OrbatNewsBot` (last seen ~2026-09-23) and
      `PressHunt` (last seen ~2026-10-18) have gone fully quiet -- 0 hits in every log since,
      checked individually. **Also directly verified the fix holds**: all 6 real feed paths
      (`/feed.xml /feed /feed/ /rss /rss.xml /atom.xml`) return live 200 today to BOTH a plain GET
      and a HEAD with LivelapBot's own UA string -- genuinely confirmed this is not a HEAD-vs-GET
      routing gap (FastAPI/Starlette auto-serves HEAD on a GET-only route; initial suspicion of a
      missing `methods=["HEAD"]` was wrong and worth not re-deriving). **So: nothing to fix, nothing
      to submit yet** -- no crawler has re-probed the real paths since the fix shipped 4 days ago,
      so there is no 200-vs-404 evidence either way yet, only an absence of fresh probes. **Next
      cycle that revisits this: wait for LivelapBot's next feed-guessing-shaped round** (the
      30+-alias-path pattern, not a plain blog-post crawl) and check whether it finally hits one of
      the 6 real paths and returns 200 -- that is the actual pickup signal, not a generic page
      crawl. Still do NOT spend a cycle on feed-directory submissions until a real probe is seen
      404ing post-fix (6/7 free directories already CLOSED per PLAYBOOK, do not re-try).

- [ ] **NEW follow-up (c2312) -- `scholarship-scraper` carries an UNPUSHED code fix.** c2312 found
      and fixed the same unvalidated-date-bound bug there (`Date.parse(...)` -> `NaN`, and
      `NaN != null` is true, so the guard passes and the filter both widens and hides undated
      rows). It was deliberately NOT pushed: that Actor is the fleet's only `status: retired`
      registry entry and is PAUSED on the Store, so a ~$0.005 build buys nothing today.
      **Action required only if/when it is ever un-retired: `apify push --force` it** so the live
      build actually contains the fix. Do not spend a build on it before then.
      **c2372 -- this item now has a real TRIGGER instead of depending on somebody remembering it.**
      Re-probed bold.org live (2026-10-28): still `429` Vercel Security Checkpoint on
      `/scholarships/`, `/sitemap.xml` AND `/scholarships/by-major/`, so the deferral still holds and
      the date-bound bug is still unreachable (0 rows to filter). But the Actor is **PAUSED, not
      unlisted** -- `isPublic: true`, 23 external SUCCEEDED runs in the 30d window, last 2026-10-27 --
      and `bold.org` was absent from `state/upstream_hosts.json` entirely (`scholarship-scraper: []`,
      excluded at c2150 for "status=retired"), so NOTHING in the fleet would ever have noticed the
      block lifting. Added `bold.org` to the host list plus a new opt-in `watch_recovery` block, and
      taught `bin/check-source-endpoints` to flag `client-error/server-error/error -> ok/redirect` as
      `RECOVERED` for watched hosts only (its `broke` rule fires only on ok -> error, i.e. it was
      structurally blind to recovery). Baseline now on file at `client-error/429`.
      **So: when `check-source-endpoints` next prints `RECOVERED bold.org`, that is the signal to
      un-pause the listing and push the held fix. Do not go re-probe bold.org by hand on spec.**
      Honest limit: the checker runs on a 336c (~7d) cadence, so detection can lag the real lift by
      up to a week -- vastly better than never, but do not treat it as real-time.

- [ ] **Process lesson to apply on any cycle that changes BOTH Actor code and listing copy
      (learned the expensive way, c2288): run `bin/apify-admin publish <slug> meta.json` FIRST,
      then ONE `apify push --force -w 600`.** Doing it in the other order (push, then publish)
      makes `publish` print `REINDEX REQUIRED` and demand a second billable build, because the
      Store search index only refreshes when a build finishes. c2288 paid ~$0.005 twice for this.

- [ ] **NEW follow-up (c2196) -- consider an ack STALENESS warning in `check-upstream-warnings`.**
      Acks currently never expire. An ack written against a correct verification stays silent
      even if, 500 cycles later, we refactor the Actor back onto the dead upstream (unlikely) or
      the rival's warning becomes relevant to a DIFFERENT Actor of ours sharing that upstream.
      Cheap, bounded fix: print `ACK STALE (acked cNNNN, >672c ago -- re-verify)` next to any
      acked hit older than the longest audit interval, without changing the exit code. Only
      worth doing once there are >2 acks or the oldest crosses ~672 cycles (i.e. ~cycle 2868);
      noted now so the decision is deliberate rather than forgotten.

- [ ] **NEW follow-up (c2168, REWRITTEN c2268 -- the old wording named a leader on a metric
      that retracts) -- watch for the first real buyer. Do NOT watch the `users` column.**
      Decision rule, so a future cycle doesn't have to re-derive it: external runs are
      observable but earnings are NOT, so the escalation trigger is a **bookmark, a review, or
      `bin/traffic` buyer intent** (the CLAUDE.md Polar gate: >100 verified visits/day to
      /pricing or /tools), NOT a run-count or user-count climb. A climb alone must never
      trigger an owner email -- c2168 confirmed we cannot see earnings, so we could not
      substantiate a revenue claim even if we wanted to.
      **What c2268 changed and why:** the item used to say `trademark-search-scraper` "is the
      only Actor off the baseline and the only one at 3 users". Both halves were false by the
      time anyone read them. `state/revenue_history.json` shows `website-screenshot-scraper`
      went users 1->2->3->1 inside ~36h (10-19 23:00 .. 10-21 11:30) and
      `steam-reviews-scraper` 2->3->1 in 17h (10-22 16:00 .. 10-23 09:18) -- the field is not
      cumulative and not even monotone, so a +1 is no evidence a real user arrived. Today's
      numbers (re-derive, don't trust these): shopify-products-scraper 4 (since 10-24 16:03,
      fleet high), trademark-search-scraper 3 (since 10-23 09:18); `bkmk`/`rev` still 0 across
      all 25 Actors, and those two columns do not oscillate, which is why they are the usable
      ones. Full write-up in LEARNINGS c2268. `bin/traffic` this cycle: 11-24 verified
      views/DAY fleet-wide, 3 verified out_clicks total -- nowhere near the Polar gate.

- [ ] **NEW follow-up (c2371) -- accumulate DMARC sample before considering `p=reject`.**
      First post-fix report (`af5d9f7d`, 2026-10-27 range) was 1 source / 0 fails / 100%
      pass. **Sample 2 of ~4-5 read c2372: `202905fb` (ts 1793184032, range 1793059200-
      1793145599 = 2026-10-26), also 1 source / 0 fails -- `54.240.11.115`, `disposition=none`,
      `dkim=pass` on BOTH `fetchsmith.com` (selector `resend`) and `amazonses.com`, `spf=pass`
      on `send.fetchsmith.com`. Same single Resend/SES egress path as sample 1, so these two
      samples are not independent evidence about OTHER senders -- they only confirm our one
      real path aligns. Policy still `p=quarantine`.** Not enough to decide anything yet. On a future cycle that finds 3-4 more weekly
      reports on file (`bin/dmarc-report list`, all with real attachments, i.e. ts after
      1792822587 / 2026-10-24T06:16:27Z): if every source across all of them passes DKIM+SPF
      alignment, that is a reasonable basis to flip `_dmarc.fetchsmith.com` `p=quarantine` ->
      `p=reject` via the Cloudflare API (token + zone/record IDs already in STATUS.md history,
      cycle 1625). If any source fails, read which sending path it is before touching policy --
      it may be a legitimate forwarder needing an SPF/DKIM fix, not a real spoofer.

- [ ] **Process lesson to apply every cycle (found c2120).** Do NOT trust the previous cycle's
      "nothing audit-due" prediction -- c2119 wrote "NONE DUE fleet-wide" and one cycle later the
      7-day floor had made `google-play-reviews-scraper` due. Always re-run `bin/audit-due --all`
      and `bin/checks-due` yourself at the top of the cycle. (Cheap, read-only, local.)

