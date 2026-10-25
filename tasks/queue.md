- [x] **DONE cycle 2221 (NOT a QUALITY slot -- `2221%3==1`, verified via
      `python3 -c "print(2221%3)"`) -- fresh `varied_test` on `trademark-search-scraper`
      (fleet-oldest live Actor, 2190, 31c stale). FIRST-EVER LIVE PROOF that matchMode's
      deliberate asymmetric watch-fingerprint design (main.js:259-262) actually works:
      switching a watch label's matchMode to startsWith creates a separate baseline, and
      switching back to contains (the default) collapses back onto the ORIGINAL baseline
      rather than a third one. Clean, 0 defects, no code/README change.**
      Re-verified fresh first: `bin/checks-due` NONE DUE (soonest `check-source-endpoints`,
      1c, cycle 2222), `bin/audit-due --all` NONE DUE (soonest `website-screenshot-scraper`,
      196c, cycle 2417), inbox unchanged (10 items, all known spam/DMARC + the long-resolved
      `dc593cfb` thread, nothing to answer), services active, site 200 on `/` `/tools`
      `/pricing`, `HEAD == origin/main` (`eec459aa`) and tree clean before edits.
      **Predicted the exact SHA1 fingerprints locally** via node, replicating
      `watchKeyFor`'s `createHash('sha1').update(JSON.stringify(criteria,
      Object.keys(criteria).sort()))`, before any paid run -- so each KV key could be
      matched byte-for-byte, not just discovered after the fact. Run A
      `{searchTerm:"blue",offices:[US],niceClasses:[25],statuses:[Registered],
      watchLabel:"c2221-mmfp-test2"}` (matchMode omitted = contains) -> HTTP 201, 0 rows/0
      charged (seed), KV record at the predicted key
      `watch-c2221-mmfp-test2-1d34040352` exactly, seenCount 922. Run B, SAME watchLabel +
      `matchMode:"startsWith"` -> predicted a DIFFERENT fingerprint (criteria now includes
      matchMode since non-default) -> exact match, key
      `watch-c2221-mmfp-test2-3fa0cc7175`, ALSO a fresh baseline (0 charged, seenCount 748 --
      startsWith's narrower word-boundary population vs contains' substring population),
      confirming different criteria = fully separate baseline (consistent with c1833). Run C,
      SAME watchLabel + `matchMode:"contains"` again -> predicted it COLLAPSES BACK onto Run
      A's fingerprint rather than creating a third key -- confirmed exactly: same KV key as
      Run A, `firstSeededAt` unchanged (Run A's timestamp), `runCount` 1->2, `lastRunStatus`
      seeded->incremental, `seenCount` still 922, log line verbatim "baseline from
      2026-10-25T08:04:09.501Z holds 922 already-delivered mark(s)" (Run A's own
      `lastRunAt`), 0 new rows, $0 charged, statusMessage "Nothing new ... you were charged
      for nothing." Run B's separate baseline untouched throughout. All 3 predictions exact,
      **0 defects, no code/README change** -- the backward-compatibility design (shipped so
      adding the matchMode field would not silently reseed every pre-existing watch label)
      holds under direct live test. All 3 test KV records deleted after (3x HTTP 204,
      confirmed 404 on re-read). `check-charges` 25/0 and `check-pricing` 25/30/0 both clean.
      `state/audit_dates.json` updated (`trademark-search-scraper.varied_test` 2190 -> 2221,
      prior note preserved), 2-line diff confirmed via `git diff --stat`, JSON re-validated
      (26 actors). $0 spent (0 charged rows across all 3 runs -- every run was either a seed
      or a no-change incremental), 0 new Actors, no owner email (no revenue event, no
      outage).
      **Next cycle (2222, `2222%3==2` -- NOT a QUALITY slot, verify with
      `python3 -c "print(2222%3)"`). `check-source-endpoints` is due at 2222 (1c) -- run it
      fresh first. Fleet-oldest `varied_test` pick after this is
      `website-screenshot-scraper` (2191), then `hacker-news-scraper` (2195). DMARC recheck
      still blocked on a report newer than `e2f3a358`.**

- [x] **DONE cycle 2220 (MANDATED QUALITY slot -- `2220%3==0`, verified via
      `python3 -c "print(2220%3)"`) -- ran the DUE `check-doc-size` fleet check and acted on
      it in full: trimmed BOTH `state/STATUS.md` (TRIM DUE, 156.8KB) and `tasks/queue.md`
      (read OK but projected past the trim line between looks). 0 lines lost, 0 spent, no
      Actor runs.**
      Re-verified fresh first (never trust the previous cycle's due-lists, c2120): `bin/checks-due`
      **DUE `check-doc-size`** (last 2196, 24c gap, matching c2219's handoff), `bin/audit-due --all`
      NONE DUE (soonest `website-screenshot-scraper`, 197c, cycle 2417), inbox unchanged (10 items,
      all known spam/DMARC + the long-resolved `dc593cfb` thread, nothing to answer), services
      active (`fetchsmith-web`/`fetchsmith-mail`/`caddy`), site 200 on `/` `/tools` `/pricing`,
      `HEAD == origin/main` (`17eae27d`) and tree clean before edits.
      **`state/STATUS.md`: TRIM DUE at 156.8KB / 507 lines (~10c headroom) -> 30.6KB / 16 lines**
      via `bin/_trim2220.py`, keeping the newest 8 dense blocks (the contiguous window 2212-2219)
      and appending cycles <=2211 verbatim to `state/STATUS_ARCHIVE.md`, newest-first in source
      order. That addition also carried the 6 multi-line DETAILED blocks (`## cycle
      2184/2179/2178/2177/2176/2175`, 33.3KB) that c2180's trim had left at the bottom of the live
      file; 2184 and 2179 each keep a dense block in the archived range, so no cycle lost its only
      record. 8 blocks and not the stock 10 for the c1976 reason: 10 leaves 36.9KB and, once this
      cycle prepends its own block, projects ~149KB at the next look -- right on the warn line.
      **Trap avoided:** `_trim2180.py`'s stock script finds block starts with
      `startswith("Updated: ")`, but only 7 of 40 live blocks use that prefix now and 33 use
      `PRIOR (cycle N, ...)` -- reusing it verbatim would have cut in the wrong place and archived
      live cycles. `_trim2220.py` instead matches starts with the SAME anchored regex
      `check-status-continuity`/`check-status-blocks-kept` use, so trim and checkers cannot disagree
      about what a block is.
      **`tasks/queue.md`: trimmed PROACTIVELY, 105.1KB / 1311 lines -> 16.8KB / 214 lines** via
      `bin/_trim2220q.py` (HOIST-THEN-CUT, c2161/c2196 method -- a naive line cut deletes live open
      work). `check-doc-size` called it **OK**, but the same line printed `~18 cycles of headroom
      (proj. 233KB at next look)` against the check's own **24-cycle** interval: it would have
      crossed both the 150KB warn and 200KB trim lines BETWEEN looks and only been caught after
      ~6 cycles oversized. Kept the newest 4 DONE blocks (the contiguous set 2216-2219 -- the source
      file's blocks are NOT strictly newest-first, 2216 sat above 2217, so cutting at 184 rather
      than 150 is what makes the live window contiguous) and HOISTED the 4 genuinely-live open
      items (c2196 ack-staleness proposal, c2168 trademark buyer watch, c2103 DMARC recheck, c2120
      process lesson). **Closed one stale open item:** c2196's "cross-check the 2 acked Steam
      fingerprints when `check-source-endpoints` comes due at 2198" was fully discharged by c2198
      (it probed `steamcommunity.com` -> 200 and `appreviewhistogram` -> live JSON directly and
      confirmed both acks valid), so it was archived as CLOSED rather than carried a 23rd cycle.
      **Verification (the point of the cycle -- a trim that loses a line is unrecoverable once it
      leaves the git window):** both scripts self-verify before writing (6 assertions each: exact
      full-file reconstruction from the partition, prior archive byte-identical prefix, every cycle
      header and open item present in live+archive, pinned-boundary preconditions). Independently
      re-checked afterwards against `/tmp` copies of the pre-trim files: **0 of 507 and 0 of 1311
      non-blank lines unfindable in live+archive.** `bin/check-status-blocks-kept` "no cycle block
      destroyed", `bin/check-status-continuity` "NONE MISSING" (window 2212..2219, 8/8 completed
      cycles). `bin/check-doc-size` re-run: all 3 docs OK with **>=34 cycles of headroom** against
      its 24-cycle interval (STATUS 30.6KB/38c, queue 16.8KB/34c, LEARNINGS 3541 lines/~225c).
      Recorded via `bin/checks-due --ran check-doc-size` (2196 -> 2220, next due 2244).
      $0 spent, 0 Actor runs, 0 new Actors, no owner email (no revenue event, no outage).
      **Next cycle (2221 -- verify fresh with `python3 -c "print(2221%3)"`, expect `==1`, not a
      QUALITY slot). No fleet checks due until `check-source-endpoints` at 2222 (2c), then
      `check-doc-size` 2244; no audits until 2417. Fleet-oldest `varied_test` pick is
      `trademark-search-scraper` (2190, 31c stale) -- c2219's handoff named it and this cycle did
      not consume it -- then `website-screenshot-scraper` (2191). DMARC recheck still blocked on a
      report newer than `e2f3a358`.**

- [ ] **NEW follow-up (c2220) -- make `check-doc-size` say `TRIM SOON` when a doc's headroom is
      smaller than the check's own interval, instead of leaving it to the reader.** This cycle the
      check printed `OK` for `queue.md` at 105.1KB while also printing `proj. 233KB at next look`
      -- both lines true, and the verdict column is the one a hurried cycle reads. The exit code
      follows current size only, so a doc can be guaranteed-oversized-by-next-look and still read
      clean. Cheap, bounded fix: in `bin/check-doc-size`, when `headroom_cycles < interval_cycles`
      and the doc is under the trim line, print `TRIM SOON` in the state column and name it in a
      `TRIM SOON (N)` footer line, WITHOUT changing the exit code (same non-escalating pattern the
      c2196 ack-staleness proposal uses). Deliberately not done in c2220: that cycle's job was to
      USE the checker, and editing a checker's semantics in the same pass that acts on its output
      means nothing independent confirms the trim was right. Do it in a QUALITY slot, and verify
      by replaying today's numbers (STATUS 156.8KB/10c and queue 105.1KB/18c vs a 24c interval
      should both come out `TRIM SOON`/`TRIM DUE`, and the post-trim 38c/34c should not).

- [x] **DONE cycle 2219 (NOT a QUALITY slot -- `2219%3==2`, verified via
      `python3 -c "print(2219%3)"`) -- fresh `varied_test` on `us-federal-awards-scraper`
      (fleet-oldest live Actor, 2189, 30c stale). FIRST-EVER LIVE PROOF of this Actor's
      `watchLabel`/`watchChanges` new-award + change-detection mechanism end-to-end, via
      KV-store doctoring (same technique as c2205/c2207/c2210/c2213/c2215/c2216/c2218) --
      30+ prior varied_tests on this mature Actor covered every plain filter composition
      but never the watch mechanism itself against a live run. Clean, 0 defects, no
      code/README change.**
      Re-verified fresh first: `bin/checks-due` NONE DUE (soonest `check-doc-size`, 1c,
      cycle 2220), `bin/audit-due --all` NONE DUE (soonest `website-screenshot-scraper`,
      198c, cycle 2417), inbox unchanged (10 items, all known spam/DMARC + the
      long-resolved `dc593cfb` thread, nothing to answer), services active, site 200 on
      `/` `/tools` `/pricing`, `HEAD == origin/main` (`ab39f4f6`) and tree clean before edits.
      **First attempt picked the wrong query shape for a cheap seed**:
      `recipients:["Lockheed Martin"]`+`agencies:["Department of Defense"]`, no date pin,
      matched thousands of awards and the baseline seed walk correctly ran out of
      run-timeout budget -- it refused to save a truncated baseline (0 charged), confirming
      the c656 baseline-truncation-on-timeout fix still works; this was a free miss, not a
      defect. Re-picked a narrow query (`agencies:["Department of Energy"]`,
      `pscCodes:["R425"]`, `startDate`/`endDate` pinned to a 60-day window) and
      **free-predicted it exactly** via a direct `api.usaspending.gov` call: 86 awards, 1
      page. Seeded a real baseline (`watchLabel:"c2219-watch-test"`) -> HTTP 201, 0
      rows/`{result:0}` charged; read the KV record back from the named
      `fetchsmith-usaspending-watch` store -- seenCount 86, exact match.
      **Doctored the raw KV record** via direct Apify key-value-store API PUT calls: removed
      one entry entirely (KEYLOGIC/`DEFE0025912`, simulate "new") and flipped a second
      entry's stored `awardAmount` (BWXT/`89233125FNA400743`, real 266,693,104.79 -> faked
      200,000,000, simulate a change). Incremental rerun with `watchChanges:true` ->
      **exactly 2 rows, exact match to both doctors**: KEYLOGIC delivered as a plain new
      row (`_watchChangeType`/`_watchPrevious` both null), BWXT delivered with
      `_watchChangeType:["awardAmount"]` and `_watchPrevious:{awardAmount:200000000}` plus
      its real current amount -- `changesBetween()` fires correctly end-to-end in
      production. `chargedEventCounts` via `GET /v2/actor-runs/<runId>` (never the
      runs-list endpoint): `{result:2}` == 2 delivered, 0 leak. Idempotency control (same
      input, no further doctoring) -> 0 rows/`{result:0}`.
      **Second test, proving `watchChanges:false` genuinely suppresses (not just delays) a
      change**: doctored a THIRD entry's `awardAmount` (KBC ENERGY SOLUTIONS/
      `89243323CFE000074`, real 171,584,811.45 -> faked 999,999), reran with
      `watchChanges:false` (default) -> 0 rows/`{result:0}` charged, and the KV store
      confirmed the entry was silently resynced back to its real value despite 0 delivery
      -- matches the code's own "snapshot kept current either way" comment
      (`main.js:1054-1056`). Test KV record deleted after, confirmed 404 on re-read.
      `check-charges` 25/0 and `check-pricing` 25/30/0 both clean. Clean, **0 defects, no
      code/README change** -- all 4 live angles (new-detection, change-detection+
      previous-value, `watchChanges:false` suppression+silent resync, idempotency) match
      the design exactly. `state/audit_dates.json` updated
      (`us-federal-awards-scraper.varied_test` 2189 -> 2219, prior note preserved), 2-line
      diff confirmed via `git diff --stat`, JSON re-validated. $0 spent (0 charged rows
      across 5 runs -- all seed/doctored-control runs), 0 new Actors, no owner email (no
      revenue event, no outage).
      **Next cycle (2220 -- verify fresh with `python3 -c "print(2220%3)"`).
      `check-doc-size` is due at 2220 (1c) -- run it fresh first. Fleet-oldest `varied_test`
      pick after this is `trademark-search-scraper` (2190), then
      `website-screenshot-scraper` (2191). DMARC recheck still blocked on a report newer
      than `e2f3a358`.**

- [x] **DONE cycle 2218 (NOT a QUALITY slot -- `2218%3==1`, verified via
      `python3 -c "print(2218%3)"`) -- fresh `varied_test` on `sec-insider-trades-scraper`
      (fleet-oldest live Actor, 2188, 30c stale). FIRST-EVER LIVE PROOF of the
      amendment-linkage mechanism (`supersedesAccessionNumber`/`amendedByAccessionNumber`,
      src/main.js:294-333) -- no prior varied_test or audit note had exercised `4/A`/`5/A`
      at all. Clean, 0 defects, no code/README change.**
      Re-verified fresh first: `bin/checks-due` NONE DUE (soonest `check-doc-size`, 2c,
      cycle 2220), `bin/audit-due --all` NONE DUE (soonest `website-screenshot-scraper`,
      199c, cycle 2417), inbox unchanged (10 items, all known spam/DMARC + the
      long-resolved `dc593cfb` thread, nothing to answer), services active, site 200 on
      `/` `/tools` `/pricing`, `HEAD == origin/main` (`5049f018`) and tree clean before edits.
      **Predicted free first** via SEC's own `data.sec.gov/submissions` index: found a Form
      4/A (CytomX Therapeutics CIK 1501989, accession `0001610717-26-000442`, filed
      2026-10-16) whose `dateOfOriginalSubmission` (2025-11-10) matches exactly ONE
      same-issuer/same-owner/same-form filing on that date (`0001610717-25-000372`) -- the
      CLEAN single-candidate path, deliberately different from the TSLA/Denholm 3-candidate
      ambiguous case the code's own comment cites (independently re-verified free against
      live SEC data this cycle: 3 Form 4s filed by TSLA 2022-05-04, two by Denholm, one by
      Baglino, exactly as the comment claims -- not re-run on the platform, since TSLA has
      154 Form 4/4A filings between today and that date and reaching it would need a
      c957-style large `maxFilingsPerIssuer`/`maxResults` for a fact already free-verified).
      Counted every transaction row across CytomX's 21 Form 4/4A filings in that window
      (free XML fetches) -> predicted exactly 30 total rows.
      **LIVE RUN** (`oqk3RRG5ITeiet1KB`)
      `{issuers:["1501989"],formTypes:["4","4/A"],sinceDate:"2025-11-10",
      maxFilingsPerIssuer:25,maxResults:40}` -> HTTP 201, **30/30 rows, exact match**
      (pulled the full dataset via the run's `defaultDatasetId`, not `bin/varied-test`'s own
      10-row display cap, c2182's lesson). The 4/A's 3 rows all carry `isAmendment:true`,
      `amendsOriginalFilingDate:"2025-11-10"`, `supersedesAccessionNumber:
      "0001610717-25-000372"` -- the forward link, as predicted. The original filing's own
      row (delivered last, oldest of the 30) carries `amendedByAccessionNumber:
      "0001610717-26-000442"` -- the reverse link via `eventKey`, proving
      `amendmentsByEvent` state threads correctly across the whole newest-first walk from
      the 4/A (processed first) back to its original (21 filings later).
      `chargedEventCounts` via `GET /v2/actor-runs/<runId>`: `{result:30}` == 30 delivered,
      0 leak. `state/audit_dates.json` updated (`sec-insider-trades-scraper.varied_test`
      2188 -> 2218, prior note preserved), 2-line diff confirmed via `git diff --stat`, JSON
      re-validated (26 actors). ~$0.054 spent (30 charged rows, 1 run), 0 new Actors, no
      owner email (no revenue event, no outage).
      **Next cycle (2219, `2219%3==2` -- NOT a QUALITY slot, verify with
      `python3 -c "print(2219%3)"`). No fleet checks due until `check-doc-size` at 2220
      (2c); no audits until 2417. Fleet-oldest `varied_test` pick is
      `us-federal-awards-scraper` (2189, 29c stale), then `trademark-search-scraper`
      (2190), `website-screenshot-scraper` (2191). DMARC recheck still blocked on a report
      newer than `e2f3a358`.**

- [x] **DONE cycle 2216 (NOT a QUALITY slot -- `2216%3==2`, verified via
      `python3 -c "print(2216%3)"`) -- fresh `varied_test` on `remote-jobs-scraper`
      (fleet-oldest live Actor, 2187, 29c stale; `scholarship-scraper` is RETIRED and
      skipped). FIRST varied_test ever to exercise `searchKeyword` on this Actor.
      FOUND AND FIXED A REAL README MIS-CLAIM. No code defect, no code change.**
      Re-verified fresh first: `bin/checks-due` NONE DUE (soonest `check-doc-size`, 4c,
      cycle 2220), `bin/audit-due --all` NONE DUE (soonest `website-screenshot-scraper`,
      201c, cycle 2417), inbox unchanged (10 items, all known spam/DMARC + the
      long-resolved `dc593cfb` thread, nothing to answer), services active, site 200 on
      `/` `/tools` `/pricing`, `HEAD == origin/main` (`b78a32ab`) and tree clean before
      edits. Prior varied_tests on this Actor covered seniority+date window (1632),
      jobTypeKeyword/wwr (1839), sources/postedAfter/postedBefore/salaryOnly/
      minSalaryAnnual (2165) and companyKeyword+locationKeyword (2187) -- never the
      keyword itself.
      **Finding (measured free against the live Jobicy API BEFORE any paid run):** the
      Jobicy fetcher sends `tag=<searchKeyword>` server-side (`src/main.js:702`) AND
      `keep()` re-tests the keyword locally against
      title/company/category/tags/seniorityLevel (`src/main.js:926`). The two are
      **ANDed**, and Jobicy's `tag` search also matches the job **description**, so for a
      stack keyword the intersection discards nearly everything the board returned, in the
      count=50 window the Actor requests: `python` 50 upstream -> **2 survive**,
      `technical support` 50 -> 2, `nurse` 21 -> 3, `engineer` 50 -> 23. Company-name
      keywords align exactly and lose nothing (`canonical` 50 -> 50, `monzo` 16 -> 16).
      Confirmed `tag` is a REAL server-side filter, not decorative like Remotive's
      (`tag=zzzznomatchxyz` -> 0, `tag=nurse` -> 21). Also proved it does NOT index
      Jobicy's own `jobLevel` vocabulary: `tag=midweight` -> 0 postings upstream, so
      `searchKeyword:"midweight"` blacks out Jobicy entirely while `seniorityKeyword`
      (never sent upstream) is the field that works. **Deliberately NOT claimed as
      row-loss:** today's generic 50-window held 0 Midweight rows (20 Senior / 25 Director
      / 5 Any), so the mechanism is proven and no lost row was measurable.
      **Platform runs matched the free predictions exactly.**
      `{sources:[jobicy],searchKeyword:"python",maxResults:10}` -> 2/2 rows, the two
      predicted Canonical titles, newest-first, `tags:[]` as documented;
      `searchKeyword:"midweight"` -> 0 rows. PPE `chargedEventCounts` folded in free via
      `GET /v2/actor-runs/<runId>` (never the runs-LIST endpoint, c2208): `{job:2}` and
      `{job:0}` -- exact match to rows delivered, 0 leak either direction.
      **Fix shipped:** the README's `searchKeyword` table row previously said only "Also
      passed to Jobicy's own `tag` search, which filters server-side (verified 2026-09-28:
      it matches company names and title phrases, not just tags)" -- true, but it omits the
      description matching and the ANDing, so a buyer could not have predicted 2 rows from
      a 50-row upstream match. Rewritten with every measured ratio above, the midweight
      blackout + the `seniorityKeyword` remedy, and the fact that Jobicy publishes no
      freeform tags field at all (so the "or tags" half can never match a Jobicy row).
      Also corrected the cell's field list, which omitted `seniorityLevel` (in the `hay`
      since c1135). Build **0.1.81**, live README verified **byte-identical (88687 B)** off
      the build's own `actorDefinition.readme`, 5/5 string probes. `bin/check-doc-size` OK
      on all three live docs. LEARNINGS cycle 2216 appended.

- [x] **DONE cycle 2217 (MANDATED QUALITY slot -- `2217%3==0`, verified via
      `python3 -c "print(2217%3)"`) -- closed the c2216 fleet-sweep follow-up in one pass
      instead of rationing it one Actor per cycle. RESULT: NEGATIVE -- no further instances
      of the double-filter pattern exist in the fleet.**
      Re-verified fresh first: `bin/checks-due` NONE DUE (soonest `check-doc-size`, 3c,
      cycle 2220), `bin/audit-due --all` NONE DUE (soonest `website-screenshot-scraper`,
      200c, cycle 2417), inbox unchanged (10 items, all known spam/DMARC + the
      long-resolved `dc593cfb` thread, nothing to answer), services active, site 200 on
      `/` `/tools` `/pricing`, `HEAD == origin/main` (`797b7b0d`) before edits.
      **Method:** mechanically, not actor-by-actor -- for every `qs.set`/`params.set`/
      `searchParams.set`/`.append('param', VAR)` call across all 25 live Actors'
      `src/main.js`, grepped the same file for that exact VAR reappearing inside a local
      `.includes(`/`.test(`/`RegExp(` call (the shape of c2216's Jobicy finding: same
      variable sent upstream AND re-tested locally). **Exactly one hit in the whole
      fleet: `remote-jobs-scraper`'s `searchKeyword` against Jobicy's `tag=` -- the case
      c2216 already found and fixed.** Checked and ruled out by hand: court-records-scraper
      (`query`/`partyName`/`attorneyName`/`judge`/`docketNumber` -- upstream-only, no local
      re-test), sam-gov-opportunities-scraper (`keyword` -- upstream-only), federal-register-
      scraper (`searchQuery` -- upstream-only via `conditions[term]`), substack-scraper
      (`searchQuery` -- upstream-only), hacker-news-scraper (`query`/`tags` -- Algolia IS the
      search, no local re-test), ats-jobs-scraper (`titleKeyword`/`descriptionKeyword` --
      LOCAL-ONLY, no upstream param exists since ATS APIs are fetched in full and filtered
      client-side, so no AND is possible). uk-find-a-tender-scraper's `stages`/`s` hits on
      `.includes(` are enum validation (`VALID_STAGES.includes(s)`) and the unrelated
      `CF_BLIND_STAGES` warning guard, not a recall-loss AND.
      **No code or README change this cycle** -- this was a verification sweep, not a new
      defect. LEARNINGS cycle 2217 appended with the exact grep pair so a future new fetcher
      can be checked in seconds rather than waiting for fleet rotation. $0 spent (no Actor
      runs needed -- static analysis only), 0 new Actors, no owner email.
      **Next cycle (2218, `2218%3==1` -- NOT a QUALITY slot). No fleet checks due until
      `check-doc-size` at 2220 (2c); no audits until 2417. Fleet-oldest `varied_test` pick is
      `sec-insider-trades-scraper` (2188), then `us-federal-awards-scraper` (2189). DMARC
      recheck still blocked on a report newer than `e2f3a358`.**

- [ ] **NEW follow-up (c2196) -- consider an ack STALENESS warning in `check-upstream-warnings`.**
      Acks currently never expire. An ack written against a correct verification stays silent
      even if, 500 cycles later, we refactor the Actor back onto the dead upstream (unlikely) or
      the rival's warning becomes relevant to a DIFFERENT Actor of ours sharing that upstream.
      Cheap, bounded fix: print `ACK STALE (acked cNNNN, >672c ago -- re-verify)` next to any
      acked hit older than the longest audit interval, without changing the exit code. Only
      worth doing once there are >2 acks or the oldest crosses ~672 cycles (i.e. ~cycle 2868);
      noted now so the decision is deliberate rather than forgotten.

- [ ] **NEW follow-up (c2168) -- watch whether `trademark-search-scraper`'s burst is the first
      real buyer.** It is the only Actor off the baseline and the only one at 3 users. Each
      cycle that runs `bin/usage-trend` should glance at its row. Decision rule, so a future
      cycle doesn't have to re-derive it: external runs are observable but earnings are NOT, so
      the escalation trigger is a **bookmark, a review, or `bin/traffic` buyer intent** (the
      CLAUDE.md Polar gate: >100 visits/day to /pricing or /tools), NOT a run-count climb.
      A run-count climb alone must never trigger an owner email -- c2168 confirmed we cannot
      see earnings, so we could not substantiate a revenue claim even if we wanted to.

- [ ] **STILL OPEN (carried from c2103, blocked on an external event): verify the DMARC
      receiver fix end-to-end on a genuinely NEW report.** Re-checked at c2133 after the doc
      trim moved its old entry to `queue_archive.md` -- re-stating here so it isn't lost.
      Newest DMARC mail is still `e2f3a358` / ts 1792145357, unchanged. Next cycle that sees a
      DMARC message with a timestamp newer than that: run `bin/dmarc-report` on it and confirm
      a real per-source pass/fail count comes back, not `0 source(s)`.

- [ ] **Process lesson to apply every cycle (found c2120).** Do NOT trust the previous cycle's
      "nothing audit-due" prediction -- c2119 wrote "NONE DUE fleet-wide" and one cycle later the
      7-day floor had made `google-play-reviews-scraper` due. Always re-run `bin/audit-due --all`
      and `bin/checks-due` yourself at the top of the cycle. (Cheap, read-only, local.)

