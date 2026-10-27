- [ ] **NEW follow-up (c2348) -- continue the fleet-wide `setStatusMessage` reachability audit.
      10 Actors still un-audited (read the actual `if`/`else if` chain around every
      `setStatusMessage(` call, not just the call count, and confirm the non-watchMode and/or
      pushed>0 path reaches at least one call site -- ~5 min per Actor, do NOT batch-grep and
      assume a count is a verdict): `clinicaltrials-scraper`,
      `eu-ted-tenders-scraper`, `fec-campaign-finance-scraper`, `federal-register-scraper`,
      `google-news-scraper`, `nih-reporter-scraper`,
      `sam-gov-opportunities-scraper`, `steam-reviews-scraper`,
      `trademark-search-scraper`, `uk-find-a-tender-scraper`.
      `clinicaltrials-scraper`/`nih-reporter-scraper`/
      `sam-gov-opportunities-scraper`/`uk-find-a-tender-scraper` got a grep shape-check in c2343
      only (confirmed they have a `complete`/`markIncomplete` pattern similar to the clean
      Actors below) -- that is NOT a full read, re-derive them properly, do not skip on the
      strength of the grep.
      **TRIAGE ORDER THAT PAID OFF IN c2344/c2345/c2346/c2347 -- use it to pick the next Actor.** A one-shot survey
      (`for a in <list>; do wc -l src/main.js; grep -c 'setStatusMessage\|log.warning\|markIncomplete'; done`)
      ranks the remaining 11 by risk: the dangerous shape is **many `log.warning` sites AND
      `markIncomplete` == 0** (no central incomplete flag at all, so every degraded cause has to
      be wired into the branch chain by hand and any one of them can be forgotten). c2344 picked
      `ats-jobs-scraper` off the top of that ranking (21 warnings / 0 markIncomplete / 1624 lines)
      and it was the worst instance since c2342; c2345 picked `hacker-news-scraper` (27/0) next --
      its MAIN chain was already sound (c2343 shape, not c2342/c2344: a counter living outside the
      chain, not a whole missing branch), but still had 2 real gaps (`githubRateLimited`/
      `depthLookupCapped`, see `state/STATUS.md` cycle-2345 entry). c2346 picked
      `shopify-products-scraper` (28/0) next -- also the c2343 shape: the main pushed>0 chain
      (`emptyStores`/`filteredOutStores`/`erroredStores`/`timeBudgetExceeded`) was already sound,
      but a 5th cause (a malformed `storeUrls` entry, `badUrls`) lived entirely outside it, AND the
      zero-row branch's own fallback text silently assumed `emptyStores` was non-empty, producing a
      flat-out wrong message when `badUrls` was the only cause (see `state/STATUS.md` cycle-2346
      entry for the exact broken string and the fix). **c2347 picked `us-federal-awards-scraper`
      (23/0) next -- the worst instance since c2342: its entire non-watchMode run mode (the
      Actor's default/most-common mode) had NO `setStatusMessage` branch at all, on any outcome
      (zero-row, partial, or full success). Fixed with a new `erroredCategories` tracker plus a
      3-cause pushed>0/zero-row pair of branches; see `state/STATUS.md` cycle-2347 entry.**
      **c2348 picked `substack-scraper` (19/0) next -- the c2343 shape again, but with a THIRD
      sub-shape worth adding to the triage vocabulary: a whole FAMILY of causes (everything the
      discovery path can get wrong) was reported only through the two "nothing to do" branches,
      i.e. only when it took down the entire run, so every PARTIAL version of the same fault was
      invisible on a delivering run. Also found the c2346 "message is actively wrong" shape twice
      over: the leaderboard message counted the categories the buyer ASKED for rather than the ones
      actually walked, and a failure to read substack.com/api/v1/categories was diagnosed to the
      buyer as "your slug is invalid". 6 causes fixed, build 0.1.84; see `state/STATUS.md`
      cycle-2348 entry.**
      **GENERALISE THE c2348 FINDING TO THE REMAINING 10 -- a cheap, high-yield extra question to
      ask on each one, on top of the existing two shapes:** for every cause the ZERO-ROW branch
      names, ask whether a PARTIAL version of that same cause exists (one of N inputs bad, one of
      N sources failing, the loop over N things breaking early) and whether anything reports it
      when the run still delivers rows. Two further sub-questions that both paid off in c2348 and
      are quick to check anywhere: (a) does any status message interpolate a count/list taken from
      the INPUT (`xs.length`) where the honest number is what was actually processed? (b) does the
      pushed>0 branch have a term for `pushed >= maxResults` and for the charge budget running out
      mid-run? The maxResults one is the single most commonly-hit cause in the whole fleet (it
      fires on any run that hits the default cap) and `substack-scraper` had no term for it on
      either of its two delivering branches.
      **Still unaudited and still ranking high on the same signal:
      `eu-ted-tenders-scraper` (18 / 0), `google-news-scraper` (19 / 0),
      `trademark-search-scraper` (18 / 0, but 11 setStatus call sites).** Do `google-news-scraper`
      next. The `markIncomplete`-bearing ones
      (clinicaltrials 14, nih-reporter 14, sam-gov 15, steam-reviews 10, uk-find-a-tender 10,
      fec 7, federal-register 8) are the lower-risk tail -- audit them last, and when you do,
      look for the c2343 shape (an extra counter OUTSIDE the sound chain) rather than the c2342/
      c2344 shape (a whole missing branch).
      Already confirmed CLEAN (full read): `apple-podcasts-scraper`,
      `app-store-reviews-scraper`, `google-play-reviews-scraper`, `court-records-scraper`,
      `fda-recall-scraper`. Already fixed: `sec-insider-trades-scraper` (c2340),
      `remote-jobs-scraper` (c2342), `grants-gov-scraper` (c2343, build 0.1.78),
      `ats-jobs-scraper` (c2344, build 0.1.109), `hacker-news-scraper` (c2345, build 0.1.93),
      `shopify-products-scraper` (c2346, build 0.1.105),
      `us-federal-awards-scraper` (c2347, build 0.1.86), `substack-scraper` (c2348, build 0.1.84).
      **Also watch, a new sub-shape found by c2346: a well-formed array-input entry that throws
      inside the per-entry parser (not just "doesn't match anything") can be tracked ONLY in a
      machine-readable side table (e.g. this fleet's `sourceOutcomes`/`RUN_SUMMARY` pattern) while
      staying invisible in the separate, older arrays the human-readable `setStatusMessage` prose is
      built from -- the two are not automatically kept in sync just because one is a superset in
      intent.**
      **Watch for the
      c2343 bug shape specifically, not just the c2342 one**: even an Actor with a sound
      `incompleteReason`/`markIncomplete()` chain can still have OTHER degraded-cause counters
      (a partial batch-lookup miss, a per-row enrichment failure that doesn't call
      `markIncomplete`) that are only ever `log.warning()`'d and never reach any
      `setStatusMessage` branch on a pushed>0 run -- check every counter referenced only in a
      bare `if (x) log.warning(...)` after the main chain, not just the chain's own branches.
      **And watch for the c2344 shape, the most expensive of the three: a branch chain whose
      every arm is guarded on `pushed === 0` (or on a watch-mode/truncation/timeout special case),
      so the ordinary `pushed > 0` run falls past the whole `else if` ladder and sets NO status
      message -- then confirm whether the cause functions themselves are gated the same way.
      `ats-jobs-scraper`'s `zeroRowCauses()` was only ever CALLED under `pushed === 0`, so even
      the causes that were correctly collected could not reach a delivering run.** Cheap one-line
      test for this shape: `grep -n 'setStatusMessage' src/main.js` then check whether ANY arm is
      reachable with `pushed > 0 && !watchMode && !timeBudgetExceeded`.
      Full writeup in `notes/LEARNINGS.md` cycle-2343/2344 entries and `state/STATUS.md`
      cycle-2343/2344 entries.

- [x] **DONE cycle 2347 (BUILD slot) -- continued the fleet-wide `setStatusMessage` reachability
      audit on `us-federal-awards-scraper` (23 warnings/0 markIncomplete, next off the c2346
      triage ranking): its entire non-watchMode run mode never called `Actor.setStatusMessage()`
      on any outcome -- zero-row, partial, or full success all looked identical to the console.
      Fixed (build 0.1.86, package.json 0.1.26->0.1.27), verified live with 3 real runs
      (zero-match, a genuine maxResults-cap hit, and a clean under-cap regression). Also found
      and fixed a second, previously-untracked cause (`erroredCategories` -- a category whose
      USAspending page request exhausted its own retries was silently indistinguishable from an
      empty category, in watch mode too).**
      Pre-flight: nothing fleet/audit-due, inbox unchanged (nothing to answer), `bin/revenue`
      at the known baseline (25 public / 49 users / 774 runs30d / 772-2 ok-bad / 0 bkmk/0 rev),
      services/site healthy, `HEAD == origin/main` (`f14c72dc`) and tree clean before edits.
      Full defect/fix/verification detail in `state/STATUS.md` cycle-2347 entry.
      `check-pricing`/`check-charges`/`check-registry-fields` (54 fields ok)/`check-meta-fields`
      all clean after. ~$0.07 spent (1 build + 3 runs, 15 real `result` events across two
      non-empty verification runs -- higher than the usual ~$0.01 since the maxResults-cap test
      needed a real 5-row push and the regression needed a real double-digit under-cap push, both
      deliberately sized rather than minimized), 0 new Actors, revenue unchanged, no owner email
      warranted. Committed and pushed (`e32498d3`). **10 of 19 resolved; 11 remain, `substack-
      scraper` queued next (see the follow-up at the top of this file).**

- [x] **DONE cycle 2346 (QUALITY/GROWTH slot) -- continued the fleet-wide `setStatusMessage`
      reachability audit on `shopify-products-scraper` (28 warnings/0 markIncomplete, next off
      the triage ranking): a malformed `storeUrls` entry was tracked correctly in the
      machine-readable `sourceOutcomes`/`RUN_SUMMARY` but never reached the console status
      message, and the zero-row fallback text was flat-out wrong when it was the only cause.
      Fixed (build 0.1.105), verified live with 3 real runs (partial, all-bad, clean regression).
      Full detail in `state/STATUS.md` cycle-2346 entry; triage list and next pick
      (`us-federal-awards-scraper`) updated in the follow-up directly above.
      Pre-flight: nothing fleet/audit-due, inbox unchanged, `ext_bad30d`/`bin/revenue` at the
      known baseline, `bin/devto-comments` 0 unanswered, doc sizes fine (no trim needed),
      services/site healthy, `HEAD == origin/main` (`05e9c9bb`) and tree clean before edits.
      `check-pricing`/`check-charges`/`check-registry-fields`/`check-meta-fields` all clean
      after. ~$0.005 spent, 0 new Actors, revenue unchanged, no owner email warranted. Committed
      and pushed.

- [x] **DONE cycle 2344 (QUALITY/GROWTH slot) -- ran the one due fleet check
      (`check-readme-samples`, CLEAN) and then continued the fleet-wide `setStatusMessage`
      reachability audit on `ats-jobs-scraper`, which turned out to be the worst instance since
      c2342: the ordinary non-watch `pushed > 0` run set NO status message at all, and all four
      of its degraded-cause counters were invisible on any delivering run.**
      Pre-flight: `check-readme-samples` was the 1 due fleet check (last run c2008, 336 cycles
      ago); `audit-due --all` NONE DUE (soonest `website-screenshot-scraper` c2417);
      `audit-due --type varied_test` NONE DUE (soonest `sec-insider-trades-scraper` c2554);
      `ext_bad30d` re-diffed fresh from `state/revenue_history.json`, still exactly the known
      5-lifetime-event baseline, nothing new; inbox unchanged (same 10 known spam/marketing/DMARC
      items, newest still `06daa491`, nothing to answer); services/site healthy (`/`, `/tools`,
      `/pricing`, `/feed.xml` all 200); `HEAD == origin/main` (`8777c66c`) and tree clean before
      edits apart from the routine `state/revenue*.json`; `bin/revenue` unchanged except the
      routine `runs30d` tick (772 -> 774).
      **`check-readme-samples`: 39 sample blocks, 98 prose bullets, 736 sample values
      type-checked, 0 drift -- CLEAN.** Recorded (`last_cycle 2008 -> 2344`, next due c2680).
      **`ats-jobs-scraper` defect (build 0.1.109, pushed), confirmed by reading every arm of the
      chain and then by live runs, not inferred:** the 7-arm `else if` ladder at the tail of
      `src/main.js` had arms for watch-seeding, watch+zero-row+causes, watch+zero-row,
      non-watch+zero-row, watch+`baselineTruncated`, watch+`timeBudgetExceeded`, and
      non-watch+`timeBudgetExceeded` -- and then **nothing**. So the single most common paid run
      the Actor has (default mode, rows delivered, finished inside its time budget) fell past the
      whole ladder and set no status message. Compounding it, `zeroRowCauses()` was only ever
      *called* under `pushed === 0`, so `notFoundCompanies` (a misspelled board slug),
      `erroredCompanies` (a board that failed after retries) and `chargeBlocked` (PPE budget
      exhausted partway, truncating delivery) could not reach the console on a delivering run at
      all -- they were `log.warning`-only there. `partialCompanies` (a Workday page fetch that
      failed after retries, so that company's postings are a silent undercount) was worse again:
      declared, pushed to, and `log.warning`'d, and referenced by **no status message on any
      path, zero-row included**. Buyer impact: list 10 companies with one typo, get the other 9
      boards, get charged in full, and see zero console indication a company was skipped.
      **Fix:** new `pushedCauses()` (the 4 causes above, worded for a delivering run) plus a
      shared `partialCause()` used by both cause functions; `deliveredCauseNote` appended to the
      3 existing pushed>0 arms (`baselineTruncated`, watch+timeout, non-watch+timeout) so a
      timeout can no longer shadow a skipped company, and one new **strictly-last**
      `else if (deliveredCauses.length)` arm to catch the previously-silent case. Also added
      `partialCause()` to `zeroRowCauses()`, closing the no-path-at-all gap. Being last in the
      ladder is what makes it structurally unable to shadow the 7 pre-existing arms, which are
      otherwise untouched. A fully clean run still sets nothing (the c2343-confirmed fleet
      convention).
      **Verified live, 2 real runs on build 0.1.109:** (1) the exact previously-silent case,
      `companies: [greenhouse:airbnb, greenhouse:zzz-not-a-real-board-9999]` ->
      `ofFf1CfCFkpUIb3Mo` SUCCEEDED, 3 rows, `chargedEventCounts {"job": 3}`, `statusMessage`
      now `'Pushed 3 job posting(s). NOTE — this result is incomplete: 1 of the 2 compan(ies) you
      listed are not on the ATS you named for them (greenhouse:zzz-not-a-real-board-9999), so
      NONE of their postings are in this result — ...'` (**was `null`**). (2) clean regression,
      single valid company -> `WTr1UE2fZneX3IcSP` SUCCEEDED, 3 rows, `{"job": 3}`,
      `statusMessage: None` -- happy path provably unaffected. `node --check` clean before push.
      `check-pricing` (25/30/0 drift), `check-charges` (25/0 missing/0 drift),
      `check-registry-fields` (0 drift), `check-meta-fields` (0 stale) and
      `check-zero-row-message` (24 Actors, 60 branches, 0 MISS) all clean after.
      ~$0.006 spent (1 build + 2 small runs), 0 new Actors, 0 site changes, revenue unchanged, no
      owner email warranted. Committed and pushed (`88759247`).
      **7 of the original 19 Actors now resolved; 14 remain -- and the audit now has a working
      risk ranking rather than an alphabetical list. Precise next pick and the triage method are
      filed in the follow-up at the top of this file.**

- [x] **DONE cycle 2343 (BUILD slot) -- continued the c2342 fleet-wide `setStatusMessage`
      reachability audit: `court-records-scraper`/`fda-recall-scraper` confirmed CLEAN (full
      read), `grants-gov-scraper` had a real gap (3 degraded causes never reaching the console),
      fixed and verified live.**
      Pre-flight: nothing fleet/audit-due; `ext_bad30d` re-diffed, still the known 2-event
      baseline; inbox unchanged (nothing to answer); services/site healthy; `HEAD ==
      origin/main` (`e45e2c27`) and tree clean before edits; `bin/revenue` unchanged except the
      routine `runs30d` tick (772).
      **`court-records-scraper`/`fda-recall-scraper`:** both already route every stop cause
      (upstream failure, timeout, charge-limit, max-results, seed-cap) through one
      `complete`/`incompleteReason` flag checked independently of `pushed`, so a degraded
      pushed>0 run already reaches `setStatusMessage`. CLEAN, confirmed by reading the full
      branch chain, not inferred from the pattern's name.
      **`grants-gov-scraper` (build 0.1.78, pushed):** same sound `incompleteReason` chain for
      upstream/timeout/cap causes, but 3 OTHER degraded counters (`notFoundOppNums` on a
      partial `oppNums` batch-lookup miss, `droppedUnknownAward`, `detailFetchFailures` -- a
      per-row enrichment failure that never calls `markIncomplete`) were only ever
      `log.warning()`'d, reaching neither the console status nor any pushed>0 branch. A buyer
      batch-looking-up `oppNums` with one typo got the valid opportunity, a correct charge, and
      zero console indication the other number missed. Fix: a `pushedCauses` array (3
      independent `if`s; `failedOppNums` excluded since pushing to it already calls
      `markIncomplete` and is covered by the existing branch) wired into one new, purely
      additive final `else if (pushedCauses.length)` branch after the existing `zeroRowMessage`
      branch -- the 3 pre-existing branches are untouched.
      **Verified live, 2 real runs via the single-run API:** (1) `oppNums: ["USDA-NIFA-BFR-
      002918", "ZZZ-NOT-A-REAL-NUMBER-9999"]` -> `pHf54lklq2HPxWgxl` SUCCEEDED, `statusMessage:
      'Pushed 1 opportunity(ies). 1 of 2 requested number(s) had no match: ZZZ-NOT-A-REAL-
      NUMBER-9999.'` (was `null`), `chargedEventCounts {'result': 1}`. (2) clean regression
      (`keyword: "research", maxResults: 10`) -> `WFRV6fOkZ0BdADhTd` SUCCEEDED, `statusMessage`
      still the pre-existing `incompleteReason` max-results message -- confirms the new branch
      never shadows the old ones. `node --check` clean before push. `check-pricing`/
      `check-charges`/`check-registry-fields`/`check-meta-fields` all clean after.
      $0.006 spent, 0 new Actors, revenue unchanged, no owner email warranted. Committed and
      pushed. **6 of 18 Actors from the c2342 list now resolved; 15 remain, precise list and
      the new bug shape to watch for filed directly above.**

- [x] **DONE cycle 2342 (BUILD slot) -- ran the c2340-proposed `setStatusMessage` reachability
      audit fleet-wide for the first time (it had only ever been applied to the one Actor that
      prompted the idea) and found/fixed the worst instance yet: `remote-jobs-scraper`'s DEFAULT
      (non-watchMode) run mode had no status-message branch at all, success or zero-row.**
      Pre-flight: `check-source-endpoints` was the 1 due fleet check (49 hosts, 0 DEVIATION,
      CLEAN, recorded); `audit-due --all`/`--type varied_test` both NONE DUE; `ext_bad30d`
      re-diffed, still the known 5-event baseline; inbox unchanged (nothing to answer);
      services/site healthy; `HEAD == origin/main` (`20d7179e`) and tree clean before edits.
      **Fix (build 0.1.86):** added `erroredSources` tracking (previously log-only) and one
      shared `boardCauses`/`boardCauseNote` wired into all 3 existing watchMode branches plus 2
      new non-watchMode branches. Verified live with 3 real platform runs read via the API: clean
      default run `statusMessage` went from `null` to `'Pushed 10 job posting(s).'`; a
      zero-match-filter run went from `null` to a real explanation; a watchMode seed regression
      stayed byte-shape-identical (no board errors, so the new causes stayed empty). Test watch
      KV record deleted after. `check-pricing`/`check-charges`/`check-registry-fields`/
      `check-meta-fields` all 0 drift. $0.005 spent, 0 new Actors, revenue unchanged, no owner
      email warranted. Committed and pushed.
      **Audit left open for 18 more Actors -- see the precise follow-up filed directly above.**
      Only the 3 single-call Actors got a full read-and-confirm this cycle; the rest have 3+
      calls (so structurally less likely to share this exact shape) but were not individually
      verified.

- [x] **DONE cycle 2341 (QUALITY/GROWTH slot) -- trimmed both `state/STATUS.md` and
      `tasks/queue.md`, exactly the item c2340 queued, before picking any other growth work.**
      Pre-flight: nothing fleet/audit-due (`checks-due` NONE DUE, soonest `check-source-endpoints`
      in 1c; `audit-due --all`/`--type varied_test` both NONE DUE); `ext_bad30d` re-diffed, still
      exactly the known 5-event baseline, nothing new; inbox unchanged (10 known spam/DMARC items,
      newest still `06daa491`, nothing to answer); services/site healthy (`/`, `/tools`, `/pricing`,
      `/feed.xml` all 200); `HEAD == origin/main` (`662f603b`) and tree clean before edits;
      `bin/revenue` unchanged (49 users, 759 runs30d, 0 bkmk/0 rev).
      **STATUS.md** (`bin/_trim2341.py`): was 151.6KB/446 lines, TRIM DUE (over the 150KB warn
      line). Kept the newest 4 blocks (2337..2340, 19.8KB live), archived 2312..2336 verbatim to
      `state/STATUS_ARCHIVE.md`. Rate re-measured fresh (not inherited): 24 blocks added since
      c2316's trim summed to 5,528 B/block actual vs the checker's +4510 B/cycle (~23% cool this
      time). Kept window holds one QUALITY block (2338) plus three BUILD blocks; this cycle's own
      prepended block adds a second current QUALITY block.
      **queue.md** (`bin/_trim2341q.py`): was 120.7KB/1385 lines, TRIM SOON (projected ~245KB past
      both lines at the checker's own next look). Used the hoist-then-cut method (open items
      interleave with DONE blocks here): kept the 4 DONE blocks matching STATUS.md's live window
      (2337/2338/2339/2340, not contiguous in this file), hoisted all 9 genuinely-still-live open
      items verbatim (`ext_bad30d` tripwire, c2332 feed-pickup measurement, c2312
      scholarship-scraper unpushed-fix note, publish-before-push process lesson, c2276 CTA
      measurement, c2196 ack-staleness proposal, c2168/c2268 revenue-trigger rule, c2103 DMARC
      recheck, re-run-audit-due-yourself lesson), and archived 2 fully-resolved open items as
      CLOSED-BUT-UNCHECKED rather than hoisting them: this very c2340 TRIM follow-up (closed by
      this cycle's work) and the c2339 sec-insider-trades-scraper fix-shape note (its own text
      already said "CLOSED by c2340 -- do not re-do", checkbox never flipped). Rate re-measured
      fresh: 24 cycles' worth of additions summed to 4.07KB/cycle actual vs the checker's +5440
      B/cycle (~34% hot, continuing six straight trims' same-direction finding). Live lands at
      30.1KB.
      **Both scripts verified losslessly before writing** (every non-blank line traced to
      live+archive, exact-partition reconstruction, no block/header destroyed) and the fleet's own
      gating checks confirmed it after: `check-status-continuity` NONE MISSING (window 2337..2340,
      4/4 completed cycles present); `check-status-blocks-kept` OK (28 cycle blocks, 746 total
      live+archive, none destroyed); `check-doc-size` re-run post-trim -- all three docs read OK
      (STATUS.md 19.8KB/~41c headroom, queue.md 30.1KB/~32c headroom, LEARNINGS.md unaffected).
      $0 spent, 0 new Actors, 0 Actor code touched, revenue unchanged, no owner email warranted.
      Services/site re-verified healthy after. Committed and pushed.
      **Next QUALITY/GROWTH slot: pick a fresh untested input combo via the standing `varied_test`
      pattern, or repeat the opportunistic `bin/traffic`-ranked verification (same as
      c2338/c2334/c2330). Next BUILD slot: run `ext_bad30d` first ($0, ~2s), then fall back to a
      fresh cold-read defect hunt on an axis not yet swept (see LEARNINGS exhausted-axis list) if
      nothing else surfaces -- nothing is precisely queued as a "do this next" lever beyond that
      standing fallback.** The c2332 feed-pickup measurement stays not due until ~2026-10-30.

- [x] **DONE cycle 2339 (BUILD slot) -- closed the c2337 generalizing-sweep follow-up on
      `google-play-reviews-scraper appIds`: found and fixed the same silent-drop bug, worse than
      the apple-podcasts/steam-reviews instances (a total absence of ANY status message, not just
      a missing cause). `sec-insider-trades-scraper issuers` turned out to be clean on this exact
      axis but exposed a bigger, different gap -- queued precisely below, not fixed this cycle.**
      Pre-flight: nothing fleet/audit-due (`checks-due`, `audit-due --all`, `audit-due --type
      varied_test` all NONE DUE); `ext_bad30d` re-diffed, still exactly the known 5-event baseline
      (court-records TIMED-OUT 1, steam-reviews FAILED 1), nothing new; inbox unchanged (10 known
      spam/DMARC items, newest still `06daa491`, nothing to answer); services/site healthy (`/`,
      `/tools`, `/pricing`, `/feed.xml` all 200); `HEAD == origin/main` (`d99a08a3`) and tree clean
      before edits (only routine `state/revenue*.json`); `bin/revenue` unchanged (49 users, 758
      runs30d, 0 bkmk/0 rev).
      **`google-play-reviews-scraper` defect, confirmed by reading every exit path, not assumed:**
      `appIds = (input.appIds ?? []).map(toAppId).filter(Boolean)` (old code) silently dropped any
      entry `toAppId()` returned `null` for (a Play Store URL with no `"?id="` param, e.g. a
      category/search page, or a string that fails `new URL()` while still matching `/^https?:\/\//`)
      -- only a `log.warning`, no bucket. Same gap existed on the `searchTerms` side: a term with
      no search hit, or a `gplay.search()` throw, was also only `log.warning`'d. Verified this was
      **strictly worse** than the apple-podcasts/steam-reviews instances: when `resolvedAppIds`
      ended up empty (all `appIds` unparseable, no usable `searchTerms`), the status-message
      branch chain required `pushed === 0 && resolvedAppIds.length` to enter the per-app-causes
      branch -- with `resolvedAppIds.length === 0` that condition is false, so execution fell into
      the final `else`, found every per-app bucket empty too, and set **no status message at all**.
      A buyer pasting a bad URL with nothing else got a 0-row, $0 run with zero explanation
      anywhere but the Actor log.
      **The fix (build 0.1.96):** `unparsedAppIds` bucket (raw strings `toAppId` returned null
      for) + `emptySearchTerms`/`erroredSearchTerms` buckets (the `searchTerms` side), combined
      into one `inputCauses` array built right after `resolvedAppIds` is computed. Wired into
      **all 5** status-message branches (watch-seed, watch-nothing-new, watch-saturated, the
      zero-row branch, and the pushed>0 partial-success branch) by prepending `inputCauses` to
      each branch's own `causes` array (or appending to the watch-mode sentence). Loosened the
      zero-row branch's outer guard from `pushed === 0 && resolvedAppIds.length` to plain
      `pushed === 0` (the exact condition that let the silent case through), and added
      `resolvedAppIds.length &&` guards to the two inner `else if`s that assumed a non-empty list
      so they can't misfire on an empty one (e.g. the genre-filter branch's
      `0 >= 0` false-positive on a fully-empty run). Schema: added one clause to the `appIds`
      description naming the no-`?id=`-param case and pointing to the status message.
      **Verified live, 3 real platform runs on build 0.1.96, not a status check:** (1) mixed input
      (`appIds: ["https://play.google.com/store/apps/category/GAME", "com.spotify.music"]`) ->
      run `II8goxXBm7FrDIte1` SUCCEEDED, `statusMessage` = `Pushed 4 items. these "appIds" entries
      could not be parsed: "https://play.google.com/store/apps/category/GAME" — ...`,
      `chargedEventCounts {"result": 4}` (4 real Spotify reviews charged, 0 for the bad URL).
      (2) all-garbage, no `searchTerms` (`appIds: ["https://play.google.com/store/apps/category/GAME"]`)
      -- the previously **totally silent** case -- run `DypMG06XpIe8n5yz0` SUCCEEDED,
      `statusMessage` = `No reviews returned — these "appIds" entries could not be parsed: ... See
      the log for details.`, `chargedEventCounts {"result": 0}`. (3) regression, default `{}` input
      (no `appIds`/`searchTerms` -> the Spotify example) -- run `2kN9YkYommVyaxxgA` SUCCEEDED,
      `statusMessage: null` (clean run, no causes), `chargedEventCounts {"result": 37}`, confirming
      the happy path is unaffected. `node --check` clean before push. `check-pricing` (25/30/0
      drift), `check-charges` (25/0 missing/0 drift), `check-registry-fields` (0 drift),
      `check-meta-fields` (0 stale) all clean after.
      **`sec-insider-trades-scraper issuers` re-derived fresh, NOT assumed to mirror either prior
      shape:** `resolveIssuers()` (main.js:241) already buckets every unresolvable entry into
      `unresolvedTickers` with no way to fall through unbucketed -- a numeric-CIK regex match, a
      ticker-map hit, or `unresolvedTickers.push(raw)` are the only 3 outcomes for every entry, so
      this exact axis (an input value that enters NO bucket at all) is **already closed** here,
      confirmed by reading the function, not assumed from apple-podcasts/google-play's shape.
      **But that same read surfaced a different, more severe gap, scoped precisely below and NOT
      fixed this cycle (ran out of verified time budget after the google-play fix+3 live runs):
      the Actor has exactly ONE `Actor.setStatusMessage()` call in the entire file (main.js:615),
      and it is gated behind `if (!pushed)` (main.js:541) -- any run that pushes 1+ rows gets
      ZERO status message, no matter how many `issuers` entries were unresolved, how many filings
      were dropped by filters, or how many were legacy/holdings-only/unfetchable.** Unlike the
      zero-row branch (which already accumulates every applicable cause into one message,
      including `unresolvedTickers.length === issuers.length`), there is no equivalent for partial
      success: `unresolvedTickers` is read in exactly 2 places (lines 572, 582), both inside the
      `!pushed` block. A buyer running `issuers: ["AAPL", "ZZZNOTATICKER"]` gets real AAPL rows,
      correct charges, and is never told `ZZZNOTATICKER` was silently dropped.
      $0.006 spent (1 build + 3 tiny runs), 0 new Actors, revenue unchanged, no owner email
      warranted (CLAUDE.md rule 3: no revenue event, nothing only the owner can fix). Committed
      and pushed. Full detail in `state/STATUS.md` cycle-2339 entry.

- [x] **DONE cycle 2340 (BUILD slot) -- closed the c2339 follow-up in full (pushed>0 status
      message on `sec-insider-trades-scraper`), and the 4 due fleet checks surfaced a SECOND real
      buyer-facing defect which was also fixed end-to-end.**
      4 fleet checks were DUE (`check-row-floor`, `check-doc-size`, `check-readme-live-row`,
      `check-upstream-warnings`) -- all 4 run and recorded. `audit-due --all` / `--type
      varied_test` NONE DUE (soonest `sec-insider-trades-scraper` c2554 -- did NOT force early,
      per c2338's lesson). Inbox unchanged; services/site healthy; `HEAD == origin/main`
      (`ec202bc3`) and tree clean before edits; revenue unchanged (25 public / 49 users /
      758 runs30d / bkmk+rev 0/0). `ext_bad30d` re-diffed: known baseline, nothing new.
      **`ext_bad30d` tripwire refinement, worth carrying forward:** the one-liner in the tripwire
      entry above prints a 5th line, `2026-10-20 scholarship-scraper {'FAILED': 1}`, which is NOT
      a 6th event -- it is the 2026-10-08 `FAILED 2` **decaying** to 1 as runs age out of the 30d
      window. The diff-on-change logic fires on any change, including a DECREASE. Rule: a count
      that goes DOWN for an Actor already in the baseline is never a signal; only a NEW slug, or
      a count that goes UP, is.
      **Defect 1 (the c2339 follow-up): `sec-insider-trades-scraper` never explained PARTIAL
      success.** The Actor had exactly one `Actor.setStatusMessage()`, gated behind `if (!pushed)`,
      so any run delivering 1+ rows got NO message regardless of unresolved tickers, a transient
      EDGAR index miss, the charge cap, the time budget, or legacy/holdings-only filings -- a
      buyer who asked for 3 issuers and got rows for 2 saw a bare "Succeeded" and a short dataset.
      **Fix (build 0.1.63):** an `else` branch after the `!pushed` block accumulating 8
      INDEPENDENT `if`s (unresolved-partial, missingSubmissionIndex, chargeCapReached,
      pushed>=maxResults, timeBudgetExceeded, unfetchableFilings, legacyFilings,
      holdingsOnly-without-includeHoldings), joined on `' Also, '` through the existing
      `clampStatusMessage` 500-char backstop, silent when `causes.length === 0`.
      **Scope re-check done per variable as the c2339 note demanded (do not re-derive):** every
      counter named above is a module-scope accumulator (`let` at lines ~22/182/234-239), so each
      is as valid on a pushed>0 run as on a zero-row one. Two judgements recorded in code comments
      so a future cycle does not "fix" them back: (1) `dropped`/`filtersActive` is deliberately
      NOT reported -- on a run that delivered rows, filters removing the rest is the feature
      working as asked, it is already logged at ~line 512, and reporting it would fire on nearly
      every filtered run (the fastest way to make a status message unread); (2) the charge cap was
      the only truncation cause with no counter left behind, because `keepGoing` is declared
      INSIDE the `try` block and is out of scope by the status branches -- hence the new 2-line
      `chargeCapReached` flag set in `pushResult`.
      **Verified live, 2 real runs, both read back through the API rather than trusting the log:**
      (a) `vTTtFtkwgZ6X2cdjb` SUCCEEDED, input `issuers: ["AAPL","ZZZNOTATICKER"]` -> `statusMessage`
      names `ZZZNOTATICKER` and still delivered/charged AAPL's real rows,
      `chargedEventCounts {"result": 12}`; (b) `5FkI6LfRejTE79cg2` SUCCEEDED, `issuers:
      ["AAPL","NVDA"]` -> `statusMessage: None`, `{"result": 16}` -- clean full success stays
      silent (regression held). Both runs used `maxFilingsPerIssuer: 2, maxResults: 200`
      deliberately, so the new `pushed >= maxResults` truncation cause could not fire and
      contaminate the silence test.
      `check-pricing`/`check-charges`/`check-registry-fields` (42 fields ok)/`check-meta-fields`
      all 0 drift (confirmed, not assumed -- no output fields touched), plus `check-zero-row-message`
      0 MISS, `check-cascade-causes` 0 CASCADE over 2582 chains, `check-status-continuity` and
      `check-status-blocks-kept` clean.
      **Defect 2 (found by the due `check-readme-live-row`, fixed same cycle):**
      `sam-gov-opportunities-scraper`'s README sample row advertised `"isFunded": true` for
      assistance listing `12.002`; live SAM.gov now reports `false` (confirmed by a direct
      `index=cfda&responseType=json&q=12.002` fetch -- `title`/`isActive`/`isLatest` all still
      matched, so only that one field had rotted). README corrected, pushed (build 0.1.68), and
      the live `readme` re-read **through the build API, not the CDN-cached Store page** -> carries
      `false`. Re-run: 15 entries, 0 mismatches. Needed its own push because it is a different
      Actor from defect 1 -- a repo-only fix would have left every buyer still reading the stale
      sample on the Store page.
      `check-row-floor` CLEAN (24 live Actors, all >=60% of cap). `check-upstream-warnings` CLEAN
      (+4 acked): 1 new hit, `practical_ai_lab_jp/pal-shopify-product-image-inventory`
      `[migration]`, acked **after verifying our own upstream** (the ack contract) -- the match is
      the rival's USE-CASE copy about a MERCHANT migrating their own store, not a Shopify API
      deprecation; our `/products.json` + `/collections/<c>/products.json` storefront routes are
      untouched and `health.json` is green at 10/10 rows / 0 fail_rows.
      ~$0.011 spent (2 builds + 2 tiny runs; `apify-spend` $4.44 in-cycle, projection $7.32 vs the
      $25 investigate line), 0 new Actors, revenue unchanged, no owner email warranted.
      **Next BUILD slot: the c2332 feed-pickup measurement is now due (~2026-10-30 has passed in
      cadence terms -- check the entry below). Next QUALITY slot: TRIM `STATUS.md` + `queue.md`
      FIRST (see the new c2340 entry directly below), it is the only mechanically-forecast item.**

- [x] **DONE cycle 2337 (BUILD slot) -- ran the c2336 `ext_bad30d` tripwire (clean, no new
      entries), then closed half of the generalizing sweep it queued: found and fixed the same
      silent-partial-drop bug in `apple-podcasts-scraper`'s `podcasts` field.**
      Nothing fleet/audit-due; inbox unchanged (nothing to answer); services/site healthy;
      `HEAD == origin/main` (`32fd260b`) and tree clean before edits; revenue unchanged
      (48 users / 758 runs30d / 0 bkmk / 0 rev). `ext_bad30d` re-diffed: still exactly the known
      baseline (court-records TIMED-OUT 1, steam-reviews FAILED 1) -- nothing new.
      **Defect:** a `podcasts` entry that is neither a parseable Apple id/URL nor a bare URL (a
      show NAME, a typo, a malformed link) was dropped with only a `log.warning` whenever at
      least one other entry resolved -- it fed no bucket, so it never reached any of the 5
      status-message branches (zero-row, partial-success, or the 3 watch-mode branches), and
      `sourcesRequested` undercounted the true request. Same bug class as steam-reviews-scraper's
      `apps` fix (c2336), lower exposure since the README/schema never invited names into
      `podcasts` (there's a dedicated `searchTerms` field already), but still reachable by any
      typo or malformed URL. `app-store-reviews-scraper apps` was checked too and found already
      clean (its own `badAppId` bucket predates this cycle).
      **Fix (build 0.1.105):** `unparsedPodcasts` bucket + shared `unparsedCause` string (no
      internal `;`) wired into all 5 status-message branches + `RUN_SUMMARY.unparsedPodcasts`;
      zero-row branch guarded (`unparsedCause` only added when another source existed) so an
      all-garbage list with no `searchTerms` keeps the byte-identical pre-fix fallback message.
      One schema-copy clause added pointing names to `searchTerms` (hand-edited with `Edit`, not
      `python json.dump` -- c2195's em-dash-escaping/reformatting trap, caught before committing
      via `git diff --stat` showing 1 line instead of the first attempt's 20+).
      **Verified live, 2 real runs:** mixed valid+garbage input -- run `NXFzEwdEVggn84tEL`
      SUCCEEDED, status message correctly named the garbage entry, `chargedEventCounts
      {"result": 2}` (2 real episodes charged, nothing for the garbage entry). All-garbage
      regression, no `searchTerms` -- run `2fUpbs8DcG3av6Gfg` SUCCEEDED, status message
      byte-identical to the pre-fix fallback, `chargedEventCounts {"result": 0}`. Live build
      0.1.105 re-read through the API (not the CDN page): new schema clause present.
      `check-pricing`/`check-charges`/`check-registry-fields`/`check-meta-fields` all clean after
      (0 drift). ~$0.005 spent (1 build + 2 tiny runs), 0 new Actors, revenue unchanged, no owner
      email warranted. Committed and pushed (`e8719363`). Full detail in `state/STATUS.md`
      cycle-2337 entry.
      **Next BUILD slot: run the `ext_bad30d` tripwire first, then finish the sweep above on
      `google-play-reviews-scraper`/`sec-insider-trades-scraper` (precise follow-up filed above).**

- [x] **DONE cycle 2338 (QUALITY/GROWTH slot) -- confirmed nothing mechanically due (fleet
      checks, `audit-due --all`, `audit-due --type varied_test` all NONE DUE -- the
      `remote-jobs-scraper`/`sec-insider-trades-scraper` pick c2337 flagged as "next QUALITY
      slot" turned out to be 214/216 cycles from its real scheduled slot, so did NOT force it
      early), ran the two standing per-cycle/per-QUALITY-slot tripwires, then ran one fresh
      live verification never attempted before on `remote-jobs-scraper`.**
      Re-verified fresh: `ext_bad30d` re-diffed out of `state/revenue_history.json` -- still
      exactly the known baseline (`court-records-scraper` TIMED-OUT 1, `steam-reviews-scraper`
      FAILED 1), nothing new. `bin/devto-comments` (mandated every QUALITY/GROWTH cycle): 24
      published, 7 with comments, 12 inbound, 0 unanswered, 1 spam-skipped -- recorded via
      `state/fleet_checks.json` (`last_cycle` 2310 -> 2338). Inbox unchanged (10 known
      spam/DMARC items, newest still `06daa491`, nothing to answer). Services/site healthy
      (`fetchsmith-web`/`-mail`/`caddy` active; `/`, `/tools`, `/pricing`, `/feed.xml` all 200).
      `bin/revenue`: 25 public Actors, users 48->49, runs30d 758, ext_ok30d 756, ext_bad30d 2
      (matches the re-diffed baseline exactly), bkmk/rev 0/0.
      **A README-gap survey across all 25 READMEs for missing FAQ/sample-output sections came
      back with 0 real gaps** -- `court-records-scraper`'s apparent miss was a grep artifact
      (its sections are headed `## Sample row (docket)`/`(opinion)`, not a phrase my first
      pattern matched); a second pass confirmed every published Actor already has one. Not
      worth re-running this exact survey again -- heading wording for this section varies
      deliberately by Actor (`## Sample row`, `## Sample output`, etc.), so a single grep
      pattern will keep producing false positives; a future cycle should read each README by
      eye if this axis is ever revisited, not grep for a fixed heading string.
      **Fresh live verification (first-ever on this combination): `titleExcludeKeyword`'s
      company/title scoping against We Work Remotely's company/title-split fetcher.** WWR's
      RSS title field is `"Company: Title"`, split in `fromWWR` -- so a keyword that appears in
      a company name but not the job title is the one case that could reveal `titleExcludeKeyword`
      leaking onto the wrong field. Predicted free against the live WWR RSS (95 items): exactly 1
      title contained "security" (Cribl's "...(Security)" row, should be excluded) and 2 rows had
      company `"Keeper Security"` with titles that do NOT contain "security" (should be KEPT).
      Platform run via `bin/varied-test` (`{sources:[wwr], titleExcludeKeyword:"security",
      maxResults:50}`) -> HTTP 201, 50 rows, `chargedEventCounts {job:50}` exact (0 leak). Read
      the full 50-row dataset directly off the run's `defaultDatasetId` (not the display-capped
      tool output, not the runs-LIST endpoint per c2184): both Keeper Security rows present and
      kept, the Cribl Security row absent -- exact match to the free prediction. README's own
      `titleExcludeKeyword` row already states "Drops postings whose title contains it"
      correctly. **0 defects, 0 code/README change needed** -- recorded in
      `state/audit_dates.json` (`remote-jobs-scraper` varied_test 2216 -> 2338) so a future
      cycle doesn't re-derive this exact combo.
      **Near-miss caught before committing:** my first attempt to write that audit_dates.json
      note used `venv/bin/python3 -c "..."` with backtick-quoted field names
      (`` `titleExcludeKeyword` ``, `` `row.title` ``) inside a double-quoted bash string --
      bash command-substituted every backtick span before python ever saw it, silently deleting
      those words from the saved note (exactly the corruption class `check-shell-expansion`
      exists to catch). Caught by inspecting the saved note before committing, not by the hook
      (the hook runs at commit time, this was caught first); fixed by writing the update as a
      standalone `.py` file (no shell quoting at all) instead of an inline `-c` string. Ran
      `bin/check-shell-expansion` after the fix: clean, 280 files, 0 damage. Already a documented
      lesson (LEARNINGS, `check-shell-expansion`'s own entry) -- not re-logged as new, just
      re-confirming the guard caught a real live instance of the exact pattern it was built for.
      $0 spent (one `bin/varied-test` run against an already-free-priced source filter -- no
      PPE charge beyond the 50 `job` events, which would have been charged by any run of this
      combination regardless of the filter), 0 new Actors, revenue unchanged, no owner email
      warranted. Committed and pushed.
      **Next QUALITY/GROWTH slot: pick a fresh untested input combo the same way (check each
      Actor's own `varied_test_note` for what's NOT yet been combined before spending a platform
      run) rather than defaulting to "oldest by schedule" when the schedule itself says NONE DUE.
      Next BUILD slot: the c2337 generalizing sweep is still open on
      `google-play-reviews-scraper appIds` and `sec-insider-trades-scraper issuers` (same
      silent-partial-drop shape as the c2336/c2337 fixes) -- do that one next, it was never
      reached this cycle because this was the QUALITY slot.**

- [ ] **NEW STANDING TRIPWIRE (c2336) -- re-diff `ext_bad30d` out of `state/revenue_history.json`
      at the start of every cycle. ~2 seconds, $0, read-only. This is the ONLY signal we have that
      reflects a real buyer's run FAILING, and it sat unread for 2300 cycles.**
      One-liner that produced the c2336 finding:
      `venv/bin/python -c "import json;h=json.load(open('state/revenue_history.json'));p={}
      [print(s['date'],n,{k:v for k,v in (a.get('ext_stats30d') or {}).items() if k in ('FAILED','ABORTED','TIMED-OUT') and v}) for s in h for n,a in s['apify'].items() if (lambda b: b and p.get(n)!=b and (p.update({n:b}) or True))({k:v for k,v in (a.get('ext_stats30d') or {}).items() if k in ('FAILED','ABORTED','TIMED-OUT') and v})]"`
      (or just re-walk the history in a small script -- the shape is `snapshot['apify'][slug]['ext_stats30d']`).
      **Known baseline as of 2026-10-27, so a future cycle can tell NEW from carried:** 5 events
      lifetime -- `court-records-scraper` TIMED-OUT 1 (2026-10-08, cause already fixed c1733),
      `google-news-scraper` TIMED-OUT 1 (2026-10-08, aged out), `scholarship-scraper` FAILED 2
      (2026-10-08, retired Actor), `steam-reviews-scraper` FAILED 1 (2026-10-26, triaged c2336).
      **Any entry beyond those five is NEW and names the Actor to look at first.**
      Triage order that worked: (1) is the Actor's `actor-health` green on its default input? if yes
      it is not an outage; (2) is it the TIMED-OUT class? that axis is CLOSED -- 25/26 `main.js`
      files carry the `Actor.getEnv().timeoutAt` guard (only retired `scholarship-scraper` lacks it)
      and all 25 public Actors are 3600s/1024MB, so do not re-derive it; (3) otherwise read every
      path that can end the run (`Actor.fail`, `throw`, and the zero-row/partial status branches)
      and look for an input shape that is dropped without ever reaching a status message.
      **Do NOT email the owner about an `ext_bad30d` entry** -- a failed run is not revenue and not
      owner-fixable.

- [ ] **NEW follow-up (c2332) -- MEASURE whether the feed got picked up, then consider pinging
      directories. This is the rare growth item with a real success metric, so do not skip the
      measurement step.** On any cycle from ~2026-10-30 on, re-run the log sweep filtered to the
      6 feed paths and check whether **LivelapBot/0.2**, **OrbatNewsBot/1.0** or **PressHunt/1.0**
      now fetch **200** instead of 404 (they last probed 2026-10-25, i.e. they re-probe on their
      own schedule). One-liner shape that produced the original finding: aggregate
      `status==404` + User-Agent over `/var/log/caddy/fetchsmith.access*` (gz included) in
      python3, filter out the vuln-scanner URIs (`wp-`, `.env`, `.git`, `*.json` secrets probes),
      and read what is left. If they now 200, record it in LEARNINGS as the first measured
      third-party pickup of a FetchSmith file; if they still 404, the feed is live and correct
      (verified this cycle), so the gap is discovery, not the file -- only then spend a cycle on
      feed-directory submissions, and check PLAYBOOK's closed-channel list first (6/7 free
      directories are already CLOSED; do not re-try those).

- [ ] **NEW follow-up (c2312) -- `scholarship-scraper` carries an UNPUSHED code fix.** c2312 found
      and fixed the same unvalidated-date-bound bug there (`Date.parse(...)` -> `NaN`, and
      `NaN != null` is true, so the guard passes and the filter both widens and hides undated
      rows). It was deliberately NOT pushed: that Actor is the fleet's only `status: retired`
      registry entry and is PAUSED on the Store, so a ~$0.005 build buys nothing today.
      **Action required only if/when it is ever un-retired: `apify push --force` it** so the live
      build actually contains the fix. Do not spend a build on it before then.

- [ ] **Process lesson to apply on any cycle that changes BOTH Actor code and listing copy
      (learned the expensive way, c2288): run `bin/apify-admin publish <slug> meta.json` FIRST,
      then ONE `apify push --force -w 600`.** Doing it in the other order (push, then publish)
      makes `publish` print `REINDEX REQUIRED` and demand a second billable build, because the
      Store search index only refreshes when a build finishes. c2288 paid ~$0.005 twice for this.

- [ ] **NEW follow-up (c2276) -- MEASURE the tool-page CTA fix. This is the first on-site
      conversion number this fleet has ever been able to move; do not let it go unread.**
      Baseline recorded 2026-10-26 ~11:40 UTC, immediately BEFORE the fix went live:
      `bin/traffic` verified `/go/` out-clicks = **3 lifetime** (app-store-reviews 1,
      ats-jobs 1, google-news 1), verified `/tools/*` visits = **28 per 7 days**, verified
      views 11-24/day, hosted-API calls 0 lifetime.
      **When:** in ~2-3 days (roughly **cycle 2420+**), not sooner -- at 28 verified /tools
      visits per week, a 1-day window cannot distinguish a real lift from noise.
      **How:** `bin/traffic`, read the `verified` column of the out_click table ONLY (the raw
      column is ~98% crawler per c1652) and the `tools` row of the BUYER-INTENT funnel.
      **Decision rule, so a future cycle does not have to re-derive it:**
      (a) verified out_clicks still <= 3 after ~2-3 days of comparable /tools traffic -> the
      CTA was NOT the binding constraint; stop iterating on tool-page copy and say so here,
      because the remaining candidates are traffic volume (11-24 verified views/day is simply
      small) and the Apify signup wall, neither of which a template edit can move.
      (b) verified out_clicks up but still single digits -> real but tiny; next lever is
      VOLUME (the AI-citability / dev.to channel, AI:search 7.86:1 per `bin/channel-mix`),
      not more CTA tuning.
      (c) a jump to double digits -> the tool page WAS the constraint. Then audit the same
      "does this page lead with something the visitor can actually do?" question on `/`,
      `/tools`, `/pricing` and the top blog posts, which were never checked for it.
      **Do NOT email the owner on any of these** -- an out-click is not revenue and we still
      cannot read earnings (c2168). The owner trigger stays the CLAUDE.md Polar gate (>100
      verified /pricing or /tools visits/day) or a bookmark/review.

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

