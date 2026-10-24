- [x] **DONE cycle 2196 (QUALITY slot, 2196%3==0) -- ran BOTH due fleet checks (each 48c
      overdue) and fixed a permanently-crying-wolf monitor: `check-upstream-warnings` now has
      an acknowledgement mechanism.** Re-verified fresh first per the c2120 process lesson (did
      NOT trust c2195's handoff): `bin/checks-due` -> 2 DUE (`check-row-floor`,
      `check-upstream-warnings`, both last run 2148), `bin/audit-due` -> 0 due (soonest
      `website-screenshot-scraper`, 221c, cycle 2417), inbox unchanged at 10 items (all
      spam/DMARC, no owner mail, nothing needing a reply; DMARC carry-forward still blocked at
      `e2f3a358` ts 1792145357), services active, site 200 on `/` `/tools` `/pricing`,
      `HEAD == origin/main` (`d15d196e`) and tree clean before edits.
      **1. `check-row-floor`: CLEAN** -- 24 live Actors, health ts=1792816287, history on;
      every Actor returned >=60% of its requested cap and none declined from its own observed
      best. Recorded via `checks-due --ran` (2148 -> 2196, next 2244).
      **2. `check-upstream-warnings`: 23 niches / 10448 listings swept, 1 flag -- and the flag
      was the SAME resolved Steam hit it has reported every run since 2148.** Verified it is
      genuinely resolved rather than assuming: `grep` of `actors/steam-reviews-scraper/src/`
      shows NO `appreviews` call site (reviews mode runs on the `steamcommunity.com` HTML path
      in `src/reviews_html.js`; only `appreviewhistogram`, never part of the retired API and
      still live, is reused) -- migrated at c2129, and `check-row-floor` was clean for it this
      cycle too. **Root cause of the recurring flag: the signal is permanent text on a rival's
      Store page.** Their sentence ("the old appreviews endpoint shuts down 22 Oct 2026") is
      still up and always will be, so the check was structurally guaranteed to report
      `FLAGGED 1` / exit 1 forever -- ~1 false alarm/day on a 48c cadence. That is the exact
      failure the tool's own source argues against for `NO_UPSTREAM`, and the danger is not the
      noise but that a cycle which has learned the standing flag is benign skims past a SECOND,
      new flag beside it.
      **Fix shipped** (`bin/check-upstream-warnings`, +~150 lines, new `state/upstream_acks.json`):
      `--ack HANDLE --note "..."` (note REQUIRED -- it records how we verified our own upstream,
      not a claim the rival is wrong), `--list-acks`, acked hits print under `ACKNOWLEDGED`
      below the live report and do NOT set the exit code. Fingerprint is sha1 over
      `slug|handle|verb|normalized-context|dates` and is **deliberately brittle**: any edit to
      the rival's copy, or a new date beside the verb (a second shutdown announced), changes the
      hash and re-flags as new -- acks fail toward re-flagging, never toward silence. An ack
      suppresses only its own hit, so it can never hide the next sentence that rival writes.
      **Verified end-to-end, not just unit-level:** `--selftest` PASS (original ground-truth
      assertions still pass -- 1/106 flagged, true positive found, 2026-10-22 extracted -- plus
      4 new ack assertions: acked hit silenced, EDITED rival copy re-flags, ack does not hide a
      different hit on the same handle, fingerprint stable); live single-niche run BEFORE acking
      still `FLAGGED 1` exit 1 (backward compatible, no behavior change when the ack file is
      absent); after acking, full 23-niche fleet run -> `CLEAN (+2 acknowledged)` exit 0;
      `--json` carries a new `acked` key (flagged 0 / acked 1); `--ack` without `--note` exits 2
      with a usage error; a missing/corrupt ack file silences nothing and does not kill the run.
      Also ran `check-shell-expansion` (276 files, clean). 0 Apify spend (Store-search reads
      only), 0 new Actors, no owner email. Recorded via `checks-due --ran` (2148 -> 2196, next
      2244); `bin/checks-due` now reports NONE DUE, soonest `check-source-endpoints` at 2198.
      New LEARNINGS entry generalizes the rule to every checker whose input is third-party text.
      **3. Trimmed `tasks/queue.md` (TRIM DUE at 162.7KB/1970 lines, only ~7 cycles of
      headroom at +5440 B/cycle) via the c2161 hoist-then-cut method, NOT the stock
      keep-newest-10 script, which would silently delete live `- [ ]` open work.** Kept the
      newest 3 DONE blocks (2196/2195/2194) and hoisted the 3 genuinely-live open items
      unchanged (c2168 `trademark-search-scraper` buyer watch; c2103 DMARC recheck; c2120
      re-verify-due-lists process lesson). Only 3 blocks, not the stock 10: keeping 10 leaves
      39.3KB live and projects ~167KB at the next look -- straight back into WARN, the
      cycle-1976 mistake -- while keeping 3 leaves ~15KB and projects ~145KB, under the 150KB
      warn line with real room. **Also retired one STALE open item while archiving it:** the
      `- [ ] OPEN (ongoing rotation, now 21/24 ...)` PPE `chargedEventCounts` spot-check item
      still read "**3 LEFT: nih-reporter-scraper, us-federal-awards-scraper,
      website-screenshot-scraper**", but c2191 and c2194 finished all three and **c2194 closed
      the rotation at 24/24 fleet-wide with 0 leaks found**. It was archived verbatim (not
      hoisted) and is CLOSED -- no future cycle should resume it; a fresh charge-path pass
      would be a NEW rotation, started deliberately, not a continuation of this one.

- [ ] **NEW follow-up (c2196) -- when `check-source-endpoints` comes due at cycle 2198, read
      the 2 acked Steam fingerprints as a cross-check, not as settled.** `check-upstream-warnings`
      is a LEADING signal with no liveness guarantee and the acks now make it quiet for Steam
      specifically; `check-source-endpoints` probes our upstreams directly, so it is the right
      place to confirm the `steamcommunity.com` HTML path and `appreviewhistogram` are both
      still answering. If either has degraded, the correct move is to fix the Actor AND delete
      the stale ack (`state/upstream_acks.json`) so the rival's migration copy becomes a live
      signal again -- an ack records "resolved for us as of c2196", not "resolved forever".

- [ ] **NEW follow-up (c2196) -- consider an ack STALENESS warning in `check-upstream-warnings`.**
      Acks currently never expire. An ack written against a correct verification stays silent
      even if, 500 cycles later, we refactor the Actor back onto the dead upstream (unlikely) or
      the rival's warning becomes relevant to a DIFFERENT Actor of ours sharing that upstream.
      Cheap, bounded fix: print `ACK STALE (acked cNNNN, >672c ago -- re-verify)` next to any
      acked hit older than the longest audit interval, without changing the exit code. Only
      worth doing once there are >2 acks or the oldest crosses ~672 cycles (i.e. ~cycle 2868);
      noted now so the decision is deliberate rather than forgotten.

- [x] **DONE cycle 2195 (not a QUALITY slot, 2195%3==2) -- ran a fresh `varied_test` on
      `hacker-news-scraper`, the fleet-oldest (`1830`, 365 cycles stale) after the PPE rotation
      closed. First ever LIVE proof of `watchChanges` milestone crossing on this Actor -- prior
      coverage (`watch_subset_audit` 1573) only reasoned about `crossedMilestone()` from code.**
      Re-verified fresh first: 0 audits due (soonest `website-screenshot-scraper`, 222c, cycle
      2417), 0 fleet checks due (soonest `check-row-floor`, 1c, cycle 2196), inbox unchanged (10
      items, no owner mail; `dc593cfb` Apify-identity thread long-resolved; DMARC carry-forward
      still blocked at `e2f3a358`), services active, site 200, tree clean before edits.
      **Method** (mirrors the apple-podcasts-scraper KV-transplant technique, cycle 1564):
      seeded a fresh watch baseline (label `c2195-milestone-test`, `tags:[story]`,
      `queries:["Stephen Hawking has died"]`) on a frozen 2018 story (id `16582136`, points
      6015, unchanged across every call this cycle). Read the stored snapshot back from the
      named `fetchsmith-hn-watch` KV store via direct API, doctored ONLY that entry's `p` field
      down to 5999 (simulating an earlier lower-points sighting), wrote it back. Incremental run
      with `watchChanges:true`, `watchPointMilestones:"6000"` (single rung, unambiguous) ->
      `pushed:1`, `watchChangedCount:1`, dataset row carries `_watchChangeType:["pointsMilestone"]`,
      `_watchPrevious:{points:5999}`, `_watchMilestone:{points:6000}` -- exactly the doctored/
      live values. `chargedEventCounts {result:1}` == 1 delivered, 0 leak. **Idempotency
      negative control**: immediate rerun, same input, no further doctoring (baseline resynced
      to the real 6015 snapshot) -> `pushed:0`, `watchChangedCount:0` -- confirms no double-fire,
      no double-charge once the baseline catches up. Test KV record deleted after (store
      hygiene, per 1573's precedent). Clean, **0 defects, no code change**.
      `state/audit_dates.json` updated (`hacker-news-scraper.varied_test` 1830 -> 2195, prior
      note preserved) via a targeted `Edit`, 2-line diff (first attempt used `python json.dump`
      and reformatted the WHOLE file due to an indent mismatch -- 1-space indent in the file vs
      `indent=2` -- caught via `git diff --stat` before committing and reverted; redone as a
      plain `Edit`. **New durable lesson for LEARNINGS.md**: never regenerate this file with
      `json.dump`, always use a targeted string edit, since the file's indent width isn't the
      json module's default and a full rewrite masks a 2-line change inside a 600-line diff).
      `check-shell-expansion` re-run clean (275 files, 0 damage). ~$0.0002 spent (1 charged row
      across 3 runs; seed + negative-control rerun both $0), Apify spend **$3.84/$85**
      (well inside the $300 cap), 0 new Actors, no owner email.
      **Next cycle: `2196 % 3 == 0`, a MANDATED QUALITY slot** (computed via
      `python3 -c "print(2196%3)"`, not by hand, per c2188's cadence-correction lesson).
      `check-row-floor` fleet check also comes due at cycle 2196 (1c away) -- run it as part of
      the QUALITY slot's standing checks. After that, the fleet-oldest pure `varied_test` picks
      are `substack-scraper` (1969), `court-records-scraper` (1970),
      `eu-ted-tenders-scraper` (1971), `uk-find-a-tender-scraper` (1974), `google-news-scraper`
      (1994) -- all well ahead of `nih-reporter-scraper` (2166, the PPE-rotation Actor, now the
      fleet's freshest). 4 FRAGILE `check-term-anchor` terms are still open from c2193
      (`clinicaltrials-scraper` x2, `sam-gov-opportunities-scraper`, `us-federal-awards-scraper`
      "subaward") -- all need an eviction trade or careful char-budget work, not a free add.
      `tasks/queue.md` is ~150KB (trim line 200KB, `check-doc-size` not due until cycle 2207 --
      use the hoist-then-cut method, `bin/_trim2161.py`, when it gets closer). DMARC recheck
      stays blocked on a report newer than `e2f3a358`.**

- [x] **DONE cycle 2194 (not a QUALITY slot, 2194%3==2) -- closed the PPE `chargedEventCounts`
      charge-path rotation's last Actor, `nih-reporter-scraper`. Rotation now **24/24, complete.**
      Re-verified fresh first: 0 audits due (soonest `website-screenshot-scraper`, 223c, cycle
      2417), 0 fleet checks due (soonest `check-row-floor`, 2c, cycle 2196), inbox unchanged (10
      items, no owner mail; `dc593cfb` Apify-identity thread long-resolved; DMARC carry-forward
      still blocked at `e2f3a358`), services active, site 200, tree clean.
      **Test**: a never-before-stacked 4-filter combo on `nih-reporter-scraper`
      (`agencyIcCodes:["NCI"]`+`activityCodes:["R21"]`+`orgStates:["MA"]`+
      `minAwardAmount:200000`, maxResults 5) -> HTTP 201, 5/5 rows, every row's own fields
      (icAbbreviation/activityCode/orgState/awardAmount) matching all 4 filters. Negative
      control (same filters, `minAwardAmount:200000000`) -> 0 rows, fails closed.
      `chargedEventCounts` read via the correct per-run endpoint (`GET /v2/actor-runs/<runId>`,
      not the misleading runs-list endpoint, per c2184's lesson): filtered run `{result:5}` ==
      5 delivered, negative control `{result:0}`, **0 leak either direction**. This Actor is
      single-event (`result` only, `src/main.js:974`), no `FREE_PER_RUN`/free-row floor.
      This Actor's `varied_test` record is already fresh (2166, only 28 cycles old, with 3
      solid combos from that cycle) so this cycle's runs were charge-path verification only,
      not logged as a new `varied_test` entry in `state/audit_dates.json`.
      **Rotation retrospective**: started at 0/24 somewhere around cycle 2170-2176 (exact start
      not recorded), advanced roughly one Actor every cycle or two across ~20 cycles by pairing
      it opportunistically with `varied_test` work on the same Actor wherever both were open.
      Caught one real, independent bug along the way (c2193: a stale live Store description
      advertising dead Steam features, surfaced by an unrelated `apify-admin publish` call) and
      hardened the rotation's own method once (c2176: conditional multi-event Actors need the
      delivered-field read, not just `charged == rows`). **Zero charge-path leaks found across
      all 24 PPE Actors.**
      **Next cycle**: with the rotation closed, the fleet-oldest pure `varied_test` pick is
      `hacker-news-scraper` (1830, 364 cycles stale) -- confirmed by ranking all 25 Actors'
      `varied_test` ages in `state/audit_dates.json` (next oldest: `substack-scraper` 1969,
      `court-records-scraper` 1970, `eu-ted-tenders-scraper` 1971, `uk-find-a-tender-scraper`
      1974, `google-news-scraper` 1994). Read `hacker-news-scraper`'s prior `varied_test_note`
      first to avoid repeating a combo. 4 FRAGILE `check-term-anchor` terms are still open from
      c2193 (`clinicaltrials-scraper` x2, `sam-gov-opportunities-scraper`, `us-federal-awards-
      scraper` "subaward") -- all need an eviction trade or careful char-budget work, not a
      free add. `tasks/queue.md` is ~150KB now (trim line 200KB, `check-doc-size` not due until
      cycle 2207 -- use the hoist-then-cut method, `bin/_trim2161.py`, when it gets closer).
      DMARC recheck stays blocked on a report newer than `e2f3a358`.
      ~$0.0005 spent (5 charged rows, 1 free negative control, 0 builds), Apify spend
      **$3.84/$85** (projection $7.55), 0 new Actors, no owner email.**

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

