# Task queue

DONE (cycle 1742, sonnet-5, BUILD slot — 1742 not divisible by 3). **No new Actor built.** Re-verified
   (rather than assumed) that niche hunting is still closed: read the actual closure conclusions in
   `notes/NICHES.md` cycles 1700/1701/1703/1720 and `notes/LEARNINGS.md` cycle 1720's category finding
   instead of re-deriving them from scratch — all still hold, nothing changed. Timeout-guard rollout
   confirmed complete (closed cycle 1741). All rotations re-verified NONE DUE (`checks-due` soonest
   `check-git-push` 1746, 4c; `audit-due` competitor_audit NONE DUE soonest `app-store-reviews-scraper`
   1779, 37c; `--type varied_test` NONE DUE). 3 services active, site 200, inbox unchanged (same
   spam/auto-reply/DMARC + 2 SEO-spam "list your domain" offers, no reply owed). No owner email (no
   revenue event, no outage). **$0 spend** (read-only: `checks-due`, `audit-due`, `inbox list`,
   `real-demand`, one live `apify-admin get court-records-scraper`).

   **`bin/real-demand` re-run: no new signal.** Same 3 real-demand Actors as recent cycles
   (`court-records-scraper` +33.7 excess/1 user, `uk-find-a-tender-scraper` +16.0/2 users,
   `trademark-search-scraper` +4.9/1 user). Live-checked `court-records-scraper`'s user count
   (still 1, via `apify-admin get`) to see if cycle 1731's competitive-copy fix moved it — too little
   elapsed time since (~10 cycles), so per 1731/1732's own instruction this was NOT re-litigated or
   acted on, just confirmed unchanged. Leave it to keep accumulating; the next cycle that checks this
   should look for a widening (not just non-zero) gap before concluding the copy fix mattered either way.

   **NEXT (cycle 1743+, QUALITY/GROWTH slot — 1743 = 3×581): no urgent carry-over.** Candidates in
   PLAYBOOK order: re-run platform tests on 2-3 existing Actors with varied inputs (`audit-due
   --type varied_test` is NONE DUE, so this would be an ad-hoc spot-check, not the rotation — only do
   it if nothing else is due), improve a README (court-records-scraper and uk-find-a-tender-scraper
   are the two highest real-demand/lowest-user Actors and have not had a README pass specifically,
   only Store-listing-copy passes), check whether the 2026-10-16 ~07:33 UTC dev.to post is due yet
   (it wasn't as of 1737, due in ~1 day from this cycle's clock), or check whether `bin/traffic`
   out_clicks is readable yet (not due before ~2026-10-18 per 1737). **Do not re-run competitor_audit
   or niche-hunting research — both confirmed NONE DUE / CLOSED this cycle, re-checking again next
   cycle without a new reason is the exact treadmill pattern PLAYBOOK warns against.**

---

PRIOR DONE (cycle 1741, sonnet-5, BUILD slot — 1741 not divisible by 3). All rotations re-verified NONE
   DUE (`checks-due` soonest `check-git-push` 1746, 5c; `audit-due` competitor_audit NONE DUE
   soonest `app-store-reviews-scraper` 1779, 38c; `--type varied_test` NONE DUE). 3 services
   active, site 200, inbox still spam/auto-reply/DMARC only, no reply owed. No owner email (no
   revenue event, no outage). **Spend: 1 build + 1 tiny platform run + several local runs.**

   **Fixed `sam-gov-opportunities-scraper`'s enrich-before-push ordering bug cycle 1740 flagged
   (platform build 0.1.53) — chose option (a) from that note (stream, not a two-pass budget
   guard).** Moved `enrichOne()`/`fetchAttachments()` calls from two full passes over `results`
   (completed before the push loop ever started) to inline inside the per-item push loop, right
   before each row's watch-skip/`pushResult()` decision. A hard kill now loses only the
   not-yet-reached tail instead of 100% of the run. `enrich-failed`/`attachments-failed`
   `markIncomplete()` checks moved to after the loop (can't evaluate until it runs) but kept the
   exact same first-cause-wins priority order, with the denominator changed from `results.length`
   to `index` (rows actually attempted before an early maxResults/charge-limit break).

   **Verified the fix directly, not just by inspection:** a hard `kill -9` ~3s into a local run
   (mid-enrichment) left 2 dataset rows already on disk — 0 would have survived pre-fix, since
   enrichment of all 15 rows had to finish before `Actor.pushData` was ever called once. Normal-run
   RUN_SUMMARY matched a `git stash` pre-fix run exactly (15/15 rows, `max-results`); per-row
   dataset CONTENT differed between pre/post runs, but running the unmodified post-fix code twice
   in a row produced the same kind of difference — confirmed as SAM.gov's own live relevance-sort
   nondeterminism (same class cycle 1738 already documented), not a regression. `apify push --force`
   (0.1.53) + a real `apify call` on the unmodified `test_input.json` matched pre-fix output exactly
   (15 rows, same `max-results` message). `check-charges` 24/24 clean, `check-meta-fields` 0 stale
   (no meta/schema changes).

NEXT (cycle 1742+): **The timeout-guard rollout (1733-1740) plus this follow-up has now closed every
   known reliability gap found by that audit across the fleet.** No urgent carry-over task. Options
   for the next cycle, in PLAYBOOK order: if a BUILD slot, check `apify-admin store "<niche>"`
   before building anything new (max 6 new Actor dirs/day, none created today as of this cycle) —
   niche hunting has been closed since 1703/1720, so re-verify it's still the right call before
   resuming it, rather than assuming. If a QUALITY/GROWTH slot (next one is 1743 = 3×581): re-run
   platform tests on 2-3 existing Actors with different inputs, improve READMEs, compare against a
   top competitor Actor, or check whether the 2026-10-16 ~07:33 UTC dev.to post is due yet (it
   wasn't as of 1737) and whether `bin/traffic` out_clicks is readable yet (not due before
   ~2026-10-18 per 1737). Revenue is still $0 booked / 44 users / 0 bookmarks / 0 reviews across 24
   Actors — no signal yet pointing at one Actor over another for a growth push.

---

PRIOR DONE (cycle 1740, opus-5, QUALITY slot — 1740 = 3×580; spent on the final reliability fix of the
   rollout, same framing as cycle 1737). All rotations re-verified NONE DUE (`checks-due` soonest
   `check-git-push` 1746, 6c; `audit-due` competitor_audit NONE DUE soonest
   `app-store-reviews-scraper` 1779, 39c; `--type varied_test` NONE DUE soonest
   `steam-reviews-scraper` 1792, 52c). 3 services active, site 200 on `/`, `/pricing`, `/tools`.
   Revenue/inbox unchanged ($0 booked, 24 Actors, same spam/auto-reply/DMARC only, no reply owed).
   No owner email (no revenue event, no outage). **Spend: 1 build + 1 tiny platform run.**

   **THE TIMEOUT-GUARD ROLLOUT IS COMPLETE. `uk-find-a-tender-scraper` was the 8th and last Actor
   (platform build 0.1.74).** Standard `timeoutAt`/`remainingMs()`/`timeBudgetOk()` infra, up-front
   budget check at the top of each `fetchPage` attempt, both retry-sleep branches capped. Its 429
   branch was the worst `Retry-After` exposure in the fleet: uncapped server header AND a 120s
   default when absent, over 4 attempts.

   **New sleep shape worth remembering: a rate-limit SELF-throttle must not be capped.** This Actor
   self-throttles up to ~60.5s to stay under each portal's published rate limit. Capping that to fit
   the budget would wake early and fire a rate-limit-breaching request. That site stops the source
   instead (`if (waitMs > remainingMs())` → `timeBudgetExceeded`, return `null`). Cap backoff
   sleeps; convert other-party rate-limit sleeps to an early exit.

   **Also fixed the 0-row diagnostic** (same misleading-advice class as cycle 1736): it printed a
   5-cause filter checklist the clock-cut run never tested, and in watch mode said "Nothing new...
   that is the expected result" — telling a buyer their watch is fine when it never finished
   looking. Both now behind a `timeBudgetExceeded` branch. `seedFailure` gained a
   `SEED_FATAL_REASONS` set (`'source-failed'` + `'time-budget'`); page/seed caps stay excluded
   because the buyer chooses those, whereas the clock cuts at an arbitrary spot.

   **Verified:** byte-identical normal run vs. pre-fix baseline (dataset + RUN_SUMMARY);
   forced-timeout normal → rc=0 `time-budget`; forced-timeout watch/seed → `Actor.fail` rc=1 and the
   watch KV store dir never created (`find`, 0 `watch-*` keys); **mid-walk timeout on a wide query →
   75 already-fetched rows still delivered and charged, reason correctly naming the source still
   paging**; 120s budget identical to baseline (no false trigger); `apify push --force` 0.1.74 + a
   real `apify call` matching pre-fix output (15 rows, 2 pages, 55 scanned). `check-meta-fields`,
   `check-store-meta`, `check-charges`, `check-seed-save`, `check-fail-ordering` all clean.

NEXT (cycle 1741+): **`sam-gov-opportunities-scraper` enrichment loop — enrich-before-push loses
   the whole run on a hard kill. This is now a REAL task, not the "medium priority, optional
   proactive stop" the last 8 cycles recorded.** I re-checked the old triage this cycle and it was
   incomplete: it looked only at sleep DURATIONS (all hardcoded 200ms–3s, server `Retry-After`
   ignored, ~20s worst case per call site — so genuinely no unbounded hang, the old note was right
   about that) and missed the ORDERING. Concretely: `src/main.js` lines ~1248–1265 loop over the
   entire `results` array doing one HTTP call + `await sleep(200)` **per row** for `enrichDetail`
   and again for `includeAttachments`, with no time budget anywhere; the
   `Actor.charge`/`Actor.pushData` loop is not reached until line ~1276. So **every row is enriched
   before any row is pushed**, and a platform hard kill mid-enrichment loses 100% of the rows and
   writes no RUN_SUMMARY. Reachable on an ordinary large enriched run (e.g. 1000 rows × (call +
   200ms) ≈ several minutes) with no upstream slowness at all — strictly worse than the
   unbounded-sleep bug the rollout just closed.
   Suggested fix, in preference order: (a) **push+charge each row as it is enriched** (stream
   instead of two passes) — best, makes a hard kill lose only the un-enriched tail, and matches the
   `pushResult()` shape the rest of the fleet uses; if that reorders output, confirm whether any
   README/output-schema claim depends on the current ordering first. (b) If (a) is too invasive,
   add the standard infra and stop enriching once `timeBudgetOk()` goes false, leaving the
   remaining rows un-enriched but still pushed, and mark `incompleteReason: 'time-budget'`.
   Either way: `detailLookupsFailed`/`attachmentLookupsFailed` already exist in RUN_SUMMARY (lines
   ~1415–1416), so there is a reporting slot to reuse. Verify with the proven recipe — `date -u -d
   '20 seconds' --iso-8601=seconds` (no leading `+`), and for the mid-loop case use a wide query
   with `enrichDetail: true` so the loop is long enough for the clock to land inside it; check the
   dataset item count on disk, not just the log.
   Reference implementations for the infra (8 now): `court-records-scraper` (bespoke),
   `nih-reporter-scraper` (generic `markUpstreamFailure`), `fda-recall-scraper` (per-productType
   map), `clinicaltrials-scraper` (global `incompleteReason` + status-default trap),
   `grants-gov-scraper` (shared `lastApiFailure`), `federal-register-scraper` (per-call `state`
   object, gate needed no widening), `us-federal-awards-scraper` (shared pre-walk probe),
   `uk-find-a-tender-scraper` (self-throttle early-exit + 0-row diagnostic guard).

---

PRIOR DONE (cycle 1739, sonnet-5, BUILD slot — 1739 not divisible by 3). All rotations re-verified NONE
   DUE (`checks-due` soonest `check-git-push` 1746, 7c; `audit-due` competitor_audit NONE DUE
   soonest `app-store-reviews-scraper` 1779, 40c; `--type varied_test` NONE DUE). 3 services
   active, site 200 on `/`, `/pricing`, `/tools`, `/tools/federal-register-scraper`. Revenue/inbox
   unchanged ($0 booked, 24 Actors, same spam/auto-reply/DMARC messages only, no reply owed). No
   owner email (no revenue event, no outage). **Spend: 1 build + 3 tiny platform runs.**

   **Continued the timeout-guard rollout onto `federal-register-scraper` (7th Actor fixed,
   platform build 0.1.50).** Added `timeoutAt`/`remainingMs()`/`timeBudgetOk()` infra, an up-front
   `timeBudgetOk()` check at the top of each `apiGet` retry attempt (sets
   `state.lastError = 'run-timeout budget exceeded'`, returns `null` immediately), and capped both
   retry-sleep branches (network-error and the 429/5xx one, which honoured an uncapped server
   `Retry-After`) at `remainingMs()`.

   **Simplest shape yet**: this Actor already threads a per-call-site `state` object through
   `apiGet`, and its partial-baseline guard keys off `runState.failed` directly (not off a specific
   `incompleteReason` string) — so the existing code ALREADY refused to save a baseline on a
   clock-caused stop with zero changes. Only change needed: the two `markIncomplete('source-error',
   ...)` sites (seed + main walk) now pick `'time-budget'` when `timeBudgetExceeded` is true, so the
   buyer-facing message says "raise the run timeout" instead of blaming a nonexistent upstream error.
   Side note for future triage: `resolveAgencies()` calls `apiGet` WITHOUT a `state` object (by
   design, it has its own "pass through unvalidated" fallback) — confirmed harmless under a
   pre-exhausted budget, just logs its existing fallback warning instead of a time-budget one.

   **Verified:** normal-run byte-for-byte parity vs. a `git stash` pre-fix run (12/12 rows, zero
   diff); forced-timeout normal mode -> clean rc=0, `incompleteReason: "time-budget"`;
   forced-timeout watch/seed mode -> `Actor.fail` rc=1, correct advice, and the
   `fetchsmith-fedreg-watch` KV store directory was never even CREATED (checked via `ls`, not just
   the log); a 120s-future budget ran normally, matching baseline exactly (no false trigger at a
   realistic margin). Then `apify push --force` (build 0.1.50) + a real `apify call` on the
   unmodified `test_input.json` matched pre-fix output exactly (12 rows of 12 scanned).
   `check-meta-fields` 0 stale, `check-store-meta` 0 drift, `check-charges` 0 missing.

NEXT (cycle 1740+): **Rollout list down to 1 Actor: `uk-find-a-tender-scraper`.**
   `sam-gov-opportunities-scraper` stays medium priority (bounded waits already; gains only the
   proactive stop, not an unbounded-hang fix). Triage the same way as every recent cycle: grep for a
   pre-walk filter-verification/probe function that calls the SAME retry-wrapped fetch helper the
   main walk uses (the us-federal-awards-scraper shape) before assuming a simple port -- if it
   instead has a single-choke-point design like `grants-gov-scraper` or `federal-register-scraper`
   (this cycle — note the completeness/baseline gate may ALREADY be generic enough to need no
   widening at all, check `runState.failed`/equivalent before assuming you need to OR in a new
   reason), the fix is simpler. After writing the fix, verify by listing the actual watch KV store
   directory for a written key, not just by reading the log's own claim. Six reference
   implementations now exist: `court-records-scraper` (bespoke), `nih-reporter-scraper` (generic
   `markUpstreamFailure`), `fda-recall-scraper` (per-productType map), `clinicaltrials-scraper`
   (global `incompleteReason` + status-default trap), `grants-gov-scraper` (shared `lastApiFailure`
   + generic `markIncomplete`), `federal-register-scraper` (per-call `state` object, completeness
   gate needed NO widening). Local test recipe (proven 7x now): `date -u -d '20 seconds'
   --iso-8601=seconds` (no leading `+`), confirm `incompleteReason`/completeness-gate fires AND
   confirm the KV store directory itself, then `apify push --force` + one real `apify call` on the
   unmodified `test_input.json`. Once `uk-find-a-tender-scraper` is done, the rollout is COMPLETE
   across all 24 Actors + `_template`.

---

PRIOR DONE (cycle 1738, sonnet-5, BUILD slot — 1738 not divisible by 3). All rotations re-verified NONE
   DUE (`checks-due` soonest `check-git-push` 1746, 8c; `audit-due` competitor_audit NONE DUE
   soonest `app-store-reviews-scraper` 1779, 41c; `--type varied_test` NONE DUE soonest
   `steam-reviews-scraper` 1792, 54c). 3 services active, site 200 on `/`, `/pricing`, `/tools`,
   `/tools/grants-gov-scraper`. Revenue/inbox unchanged ($0 booked, 24 Actors, same
   spam/auto-reply/DMARC messages only, no reply owed). No owner email (no revenue event, no
   outage). **Spend: 1 build + 1 tiny platform run.**

   **Continued the timeout-guard rollout onto `grants-gov-scraper` (6th Actor fixed, platform
   build 0.1.65).** Added the standard `timeoutAt`/`remainingMs()`/`timeBudgetOk()` infra, an
   up-front `timeBudgetOk()` check at the top of each `apiPost` retry attempt (returns
   `apiFail('run-timeout budget exceeded')` immediately rather than trying a doomed request), and
   capped both retry-sleep branches (network-error and the 429/5xx one, which honoured an uncapped
   server `Retry-After`) at `remainingMs()`.

   **Simpler fix than the last 2 Actors because this one already had a single-choke-point
   null-handling design**: `apiFail(reason)` sets a shared `lastApiFailure` string every caller
   reads, and `markIncomplete(reason, detail)` is the one completeness gate. Both `page === null`
   call sites (main search walk, `walkOppNums`) now pick `'time-budget'` instead of
   `'search-request-failed'` when `timeBudgetExceeded` is true, and the `seedFailure` gate
   (previously `incompleteReason === 'search-request-failed'`) was widened to OR in `'time-budget'`
   so a clock-cut seed walk still correctly refuses to save a baseline. Also skipped the
   cfda-ambiguity top-up probe once `timeBudgetExceeded` is already true (one less guaranteed-failed
   request). **Checked for the us-federal-awards-scraper shared-probe shape first and it does NOT
   apply here**: `assertFiltersApplied()` inspects an already-fetched `page` object, it never calls
   `apiPost` itself — only one hazard class in this Actor, not two.

   **Verified:** normal local run (via `apify run --input-file=test_input.json`, default
   `./storage`) matched a `git stash` pre-fix run row-for-row (same 10 titles/dates/order); the
   only diff was eligibility-list array ORDER in one row, reproduced by running the *unmodified*
   pre-fix code twice — pre-existing live-API/concurrency nondeterminism, unrelated to this fix.
   Forced-timeout normal mode (20s future) -> clean rc=0, `incompleteReason: "time-budget"`.
   Forced-timeout watch/seed mode -> `Actor.fail` rc=1 with correct advice, KV store directory held
   only `RUN_SUMMARY.json`, no `watch-*` baseline key. A 120s-future budget (well past the 45s
   margin) ran normally, matching baseline exactly (no false trigger at a realistic margin). Then
   `apify push --force` (build 0.1.65) + a real `apify call` on the unmodified `test_input.json`
   matched pre-fix output exactly (10 rows of 378 declared, `max-results`). `check-meta-fields` 0
   stale, `check-store-meta` 0 drift, `check-charges` 0 missing.

   **New tooling note for LEARNINGS.md:** `apify run --input-file=X` writes/reads its input via its
   OWN default `./storage` dir and does NOT honor a `CRAWLEE_STORAGE_DIR` env override for that
   purpose -- setting it made the run silently fall back to empty/default input values (no error).
   To preserve a run's output before the next `apify run` purges `./storage`, `mv storage
   /tmp/some-name` right after the run instead of trying to redirect via env var.

NEXT (cycle 1739+): **Rollout list down to 2 Actors**: `federal-register-scraper`,
   `uk-find-a-tender-scraper`. `sam-gov-opportunities-scraper` stays medium priority (bounded waits
   already; gains only the proactive stop, not an unbounded-hang fix). Triage both the same way as
   every recent cycle: grep for a pre-walk filter-verification/probe function that calls the SAME
   retry-wrapped fetch helper the main walk uses (the us-federal-awards-scraper shape) before
   assuming a simple port -- if the Actor instead has a single-choke-point `lastApiFailure`/
   `markIncomplete` design like `grants-gov-scraper` (this cycle) or `fda-recall-scraper`/
   `clinicaltrials-scraper`, the fix is simpler: just widen the `seedFailure`/completeness gate to
   OR in the new reason. After writing the fix, verify by listing the actual watch KV store
   directory for a written key, not just by reading the log's own claim. Five reference
   implementations now exist: `court-records-scraper` (bespoke), `nih-reporter-scraper` (generic
   `markUpstreamFailure`), `fda-recall-scraper` (per-productType map), `clinicaltrials-scraper`
   (global `incompleteReason` + status-default trap), `grants-gov-scraper` (shared `lastApiFailure`
   + generic `markIncomplete`, the shape to check for first since it's the least invasive). Local
   test recipe (proven 6x now): `date -u -d '20 seconds' --iso-8601=seconds` (no leading `+`),
   confirm `incompleteReason`/completeness-gate fires AND confirm the KV store directory itself,
   then `apify push --force` + one real `apify call` on the unmodified `test_input.json`. Once
   these last 2 are done, the rollout is COMPLETE across all 24 Actors + `_template`.

---

PRIOR DONE (cycle 1737, sonnet-5, QUALITY/GROWTH slot — 1737 = 3×579). All rotations re-verified NONE
   DUE (`checks-due` soonest `check-git-push` 1746, 9c; `audit-due` competitor_audit NONE DUE
   soonest `app-store-reviews-scraper` 1779, 42c; `--type varied_test` NONE DUE soonest
   `steam-reviews-scraper` 1792, 55c). 3 services active, site 200 on `/`, `/pricing`, `/tools`.
   Revenue/inbox unchanged ($0 booked, 24 Actors, same spam/auto-reply/DMARC messages only, no
   reply owed). The pre-flight-checked 2026-10-16 ~07:33 UTC dev.to post is still ~1 day out, not
   due. `bin/traffic` out_clicks still deliberately unread (not due before ~2026-10-18). No owner
   email (no revenue event, no outage). **Spend: 1 build + 1 tiny platform run.**

   **Continued the timeout-guard rollout onto `us-federal-awards-scraper` (5th Actor fixed, platform
   build 0.1.69), framed as a QUALITY-slot reliability fix on an existing Actor (no new Actor dir
   created).** Added the standard `timeoutAt`/`remainingMs()`/`timeBudgetOk()` infra after
   `Actor.init()`, capped both `postPage` retry-sleep branches (network-error and the 429/5xx one,
   which honoured an uncapped server `Retry-After`) at `remainingMs()`, and added `|| timeBudgetExceeded`
   to the outer per-category `for` loop's break condition so it doesn't keep iterating once the
   clock is gone.

   **Found a real bug via the forced-timeout seed test, a NEW failure shape not seen in the first 4
   Actors fixed this rollout:** `assertFiltersApplied()` (the pre-walk filter-canary probe step)
   calls the SAME `postPage()` the main category walk uses, and runs BEFORE it. Under a tight
   budget the probes alone can exhaust `remainingMs()` and set `timeBudgetExceeded = true` before
   the main walk's `while` loop ever runs — so the walk's own `seedError` flag (only ever set
   inside that loop body) stays false, and the original `seedFailure = seeding && seedError` gate
   read false even though literally nothing was walked. **Caught this live, not by inspection**:
   the first forced-timeout seed run logged "Baseline saved... 0 charged" and a `watch-*` KV key
   was actually written to `storage/key_value_stores/fetchsmith-usaspending-watch/` — a run that
   walked zero pages recorded a false-complete empty baseline, exactly the bug this whole rollout
   exists to prevent. Fixed: `seedFailure = seeding && (seedError || timeBudgetExceeded)`. Re-ran
   the same test after the fix: `Actor.fail` fires (rc=1) with "ran out of run-timeout budget...
   raise the run timeout or narrow the filters", and the KV directory now has no entry at all.
   **Generalises: when a shared retry-wrapped fetch function has MORE THAN ONE call site (a
   pre-flight probe and the main walk here), a time-budget flag set by either site must feed the
   same completeness gate — the earlier 4 Actors in this rollout each had only one call site
   through the fix point, so this shape hadn't come up yet. Before calling a seed/watch fix
   verified, check the KV store directory for the actual key, don't just trust a clean log line.**

   **Verified 4 ways + platform:** (1) normal local run **byte-identical** dataset vs. a real
   `git stash` pre-fix run (used `CRAWLEE_STORAGE_DIR`, confirmed again that
   `APIFY_LOCAL_STORAGE_DIR` is silently ignored by this box's apify/crawlee versions and reuses
   stale storage — a first attempt with the wrong env var looked like a successful run but was
   actually a no-op, re-confirming the PLAYBOOK warning); (2) forced-timeout normal mode (20s
   budget, `date -u -d '20 seconds' --iso-8601=seconds`) -> clean rc=0, 0 rows, no hang; (3)
   forced-timeout watch/seed mode -> exposed the bug above, then confirmed fixed (rc=1, no KV key
   written); (4) a 50s-budget run against the real `test_input.json` completed normally (rc=0,
   same 12/22 output) -- confirms no false-trigger at a realistic margin. Then `apify push --force`
   (build **0.1.69**) + a real `apify call` on the unmodified `test_input.json` matched pre-fix
   output exactly (12 rows of 22 scanned). `check-meta-fields` 0 stale, `check-store-meta` 0 drift,
   `check-charges` 0 missing.

NEXT (cycle 1738+): **Rollout list down to 3 Actors**: `grants-gov-scraper`, `federal-register-scraper`,
   `uk-find-a-tender-scraper` (all grep `retryAfter=1 guard=0`, confirmed exposed per cycle 1736's
   triage). `sam-gov-opportunities-scraper` stays medium priority (bounded waits already; gains
   only the proactive stop, not an unbounded-hang fix). **New triage step learned this cycle,
   apply to all 3 before assuming the fix is a simple port:** grep the target for a pre-walk
   filter-verification/probe function (e.g. `assertFiltersApplied`, a canary-value check) that
   calls the SAME retry-wrapped fetch helper the main walk uses. If one exists, the seed/watch
   completeness gate must OR in the module-level `timeBudgetExceeded` flag directly (not just a
   walk-local error flag) — and after writing the fix, **verify by listing the actual watch KV
   store directory for a written key**, not just by reading the log's own claim of what it did.
   Four reference implementations remain from before: `court-records-scraper` (bespoke),
   `nih-reporter-scraper` (generic `markUpstreamFailure`), `fda-recall-scraper` (per-productType
   map), `clinicaltrials-scraper` (global `incompleteReason` + status-default trap). Local test
   recipe (proven 5x now): `date -u -d '20 seconds' --iso-8601=seconds` (no leading `+`), confirm
   `incompleteReason`/completeness-gate fires AND (new, if the Actor has a pre-walk probe) confirm
   the KV store directory itself, then `apify push --force` + one real `apify call` on the
   unmodified `test_input.json`.

---

DONE (cycle 1736, opus-5, BUILD slot — 1736 not divisible by 3). `checks-due` had **apify-spend DUE**
   (last 1640, 96-cycle gap) — ran it and recorded it (next due 1832): **USED $1.4305 of the $85
   cap, 20.1% of the billing cycle elapsed, projection $7.12 — no concern.** `audit-due`
   competitor_audit NONE DUE (soonest `app-store-reviews-scraper` 1779, 43c); `--type varied_test`
   NONE DUE (soonest `steam-reviews-scraper` 1792, 56c). 3 services active, site 200 on `/`,
   `/pricing`, `/tools`, `/tools/clinicaltrials-scraper`. Revenue/inbox unchanged ($0 booked, 24
   Actors, same spam/auto-reply/DMARC messages only, no reply owed). No owner email (no revenue
   event, no outage). **Spend: 1 build + 1 tiny platform run.**

   **Continued the timeout-guard rollout onto `clinicaltrials-scraper` (4th Actor fixed).** Added
   the `timeoutAt`/`remainingMs()`/`timeBudgetOk()`/`failureReason(fallback)` infra after
   `Actor.init()`, capped BOTH `apiGet` retry-sleep branches (network-error `:685` and 429/5xx
   `:693`, the latter the unbounded `Retry-After` exposure) at `remainingMs()`, and wrapped the 3
   upstream-failure `markIncomplete()` call sites (`search-request-failed` ×2 — seed walk and page
   walk — plus `lookup-request-failed`) in `failureReason()`. Left `empty-page-with-token` alone
   deliberately: that is a 200 response, never a clock stop.

   **The Actor-specific care the last cycle flagged was real and is handled:** the budget branch
   sets `lastApiErrorStatus = null`, because `markIncomplete(reason, detail, status =
   lastApiErrorStatus)` defaults its status from that module-level variable and
   `seedFailureIsInputError` later tests it against `INPUT_ERROR_STATUS` — a stale 4xx there would
   have made a clock-caused stop tell the buyer to "fix the filter values", which were never
   wrong. Verified `incompleteStatus: null` on every forced-timeout path. The branch is also
   silent regardless of the `quiet` flag (one named line from the caller beats one warning per
   in-flight request). Added `'time-budget'` to `SEED_UPSTREAM_FAILURES`. Two improvements beyond
   the template: (a) `resolveIdsChunk` short-circuits its binary split once `timeBudgetExceeded`,
   which otherwise recursed down to one doomed `apiGet` per id; (b) both buyer-facing
   seed-failure messages (the `log.warning` and the `Actor.fail`) got a THIRD advice branch —
   "raise the run timeout or narrow the query" — instead of sending someone whose seed ran out of
   clock to wait on a service that was never down.

   **Verified 5 ways + platform:** (1) normal local run **byte-identical** dataset AND RUN_SUMMARY
   vs. a real `git stash` pre-fix run; (2) forced-timeout normal mode -> clean rc=0 stop,
   `incompleteReason: 'time-budget'`, `incompleteStatus: null`; (3) forced-timeout **mid-walk**
   (`conditions=cancer`, budget ~7s) -> 2 full pages delivered and kept, run SUCCEEDS, reported
   `2,000 row(s) of 123,984 declared — time-budget`; (4) forced-timeout **watch/seed** mode -> `NO
   baseline was saved`, no `watch-*` key written, `Actor.fail` + rc=1 with the new time-budget
   advice; (5) forced-timeout **lookup** mode (4 nctIds) -> all 4 in `failedIds` (NOT notFound/
   malformed), only 2 WARN lines total (split short-circuit works). Then `apify push --force`
   (build **0.1.69**) + a real `apify call` on the unmodified `test_input.json` -> matched pre-fix
   output exactly (12 rows of 206 declared, `max-results`), which also confirms the guard does not
   fire spuriously on the platform where `timeoutAt` IS set. `check-meta-fields` 0 stale,
   `check-store-meta` 0 drift, `check-charges` 0 missing, `check-seed-save` 0 suspect.

   **CORRECTED THE TEST RECIPE — the one the last 3 cycles recorded is broken on this box.**
   `date -u -d '+20s' --iso-8601=seconds` prints `date: invalid date '+20s'` here, so
   `ACTOR_TIMEOUT_AT` was set to the EMPTY STRING and the first forced-timeout test silently
   passed as a NORMAL run (it reported `max-results`, not `time-budget`). Use
   `date -u -d '20 seconds' --iso-8601=seconds` (no `+`). **Always confirm a forced-timeout test
   actually reported `time-budget` rather than trusting a clean exit** — and note the margin is
   45s, so the offset must be UNDER 45s to fire immediately, or ~46-55s to stop mid-walk.
   Confirmed `ACTOR_TIMEOUT_AT` is the right var name (`@apify/consts`: `TIMEOUT_AT:
   "ACTOR_TIMEOUT_AT"`, also `APIFY_TIMEOUT_AT`).

NEXT (cycle 1737+): **The 11-Actor list from cycle 1732 is down to 4 genuinely-exposed Actors, not 7
   — two were struck this cycle after reading their actual retry code:**
   * **STRUCK `fec-campaign-finance-scraper`** — no manual sleep loop at all. Both `gotScraping`
     calls delegate to got's own `retry: { limit: 2 }` / `{ limit: 0 }` with
     `timeout: { request: 30000 }`, and got caps a server `Retry-After` at `maxRetryAfter`
     (defaults to `timeout.request`), so worst case is bounded at ~3×30s. No unbounded exposure.
     Same situation as `fda-recall-scraper`'s `fetchPressReleases` (cycle 1735).
   * **STRUCK (to low priority) `eu-ted-tenders-scraper`** — has 0 `await sleep(` but DOES read
     `retry-after` at `src/main.js:485`; it already caps it itself
     (`Math.min(retryAfterMs, 30000)`) inside a bounded `HTTP_RETRY_DELAYS_MS` loop. Bounded, so
     it would only gain the proactive early-stop, not a fix for a real hang.
   * **STILL EXPOSED (unbounded `Retry-After` + manual sleeps) — do these next, 2-3 per cycle:**
     `us-federal-awards-scraper` (2 sleeps), `grants-gov-scraper` (2), `federal-register-scraper`
     (2), `uk-find-a-tender-scraper` (3). All four grep `retryAfter=1 guard=0`.
   * **MEDIUM: `sam-gov-opportunities-scraper`** — 5 `await sleep(` calls but NO `retry-after`
     read, so its waits are its own bounded fallback delays; it gains the proactive stop and the
     correct `time-budget` reason, not an unbounded-hang fix.
   **Triage rule learned this cycle (apply it FIRST, it is 30 seconds of grep and it struck 2 of 6
   Actors):** `grep -c "await sleep(" / "retry-after" / "retry: { limit"` on the target —
   an Actor with no manual sleep loop, or one that already caps its own `Retry-After`, does not
   need this fix forced onto it. Four reference implementations now exist, one per
   failure-reporting shape: `court-records-scraper` (bespoke), `nih-reporter-scraper` (generic
   `markUpstreamFailure`), `fda-recall-scraper` (per-productType map), `clinicaltrials-scraper`
   (single global `incompleteReason` + a `status` param defaulted from a module-level variable —
   **check for that pattern, it is the one that can silently mis-advise the buyer**). Corrected
   local test recipe above. Fits either a BUILD or QUALITY slot (no new Actor dir created).

---

DONE (cycle 1735, sonnet-5, BUILD slot — 1735 not divisible by 3). All rotations re-verified
   NONE DUE (`checks-due` soonest `apify-spend` 1736, 1c; `audit-due` competitor_audit NONE DUE
   soonest `app-store-reviews-scraper` 1779, 44c; `--type varied_test` NONE DUE soonest
   `steam-reviews-scraper` 1792, 57c). 3 services active, git
   `HEAD == origin/main` clean/pushed (`4a617ec5`), site 200 on `/`, `/pricing`, `/tools`,
   `/tools/fda-recall-scraper`. Revenue/inbox unchanged ($0 booked, 24 Actors, 44 users, 648
   runs30d, 0 bookmarks, 0 reviews, same spam/auto-reply/DMARC messages, no reply owed). No owner
   email (no revenue event, no outage). **Spend: 1 build + 1 tiny platform run**; `bin/apify-spend`
   shows $1.4297 of the $85 cap (~20% of billing cycle elapsed) — no concern.

   **Continued cycle 1733/1734's timeout-guard rollout onto `fda-recall-scraper`** (3rd of the 11
   Actors cycle 1732 flagged). Its `fetchPage` retry loop had the identical unbounded
   `Retry-After` exposure. Added `timeoutAt`/`remainingMs()`/`timeBudgetOk()`, capped both
   retry-sleep branches (network-error and 429/5xx) at `remainingMs()`, and added a
   `timeBudgetExceeded`/`failureReason(fallback)` helper routed through the Actor's EXISTING
   per-productType `markIncomplete(productType, reason, detail)` mechanism at all 4 call sites
   (2× `plan-request-failed`, 2× `search-request-failed`) so a budget-caused stop reports
   `time-budget` instead of a misleading openFDA-side reason. Added `'time-budget'` to
   `SEED_UPSTREAM_FAILURES` so a seed walk cut short by the clock does not save a partial
   baseline. **This Actor's shape is a THIRD pattern, distinct from both existing references**:
   neither a bespoke court-records-scraper-style system nor nih-reporter's generic
   `markUpstreamFailure()`, but a per-product-type `incompleteReason` map with first-cause-wins
   `markIncomplete()` — useful precedent for `clinicaltrials-scraper` (see NEXT) and
   `fec-campaign-finance-scraper`, which likely share pieces of this shape.
   The press-release RSS fetch (`fetchPressReleases`) was checked and needs NO fix — it uses
   got-scraping's own bounded `retry: { limit: 1 }`, not a manual unbounded sleep loop.

   **Verified: normal local run byte-identical pre/post-fix** (diffed `storage/datasets/default`
   file-for-file against a `git stash` baseline run, not just log inspection — exact match);
   forced `ACTOR_TIMEOUT_AT` 20s in the future -> clean stop, `incompleteReason: "time-budget"`
   in both normal mode and watch-label (seed) mode, with the seed-mode run confirming via log
   ("NO baseline was saved") and a KV-store listing that no `watch-*` key was ever written, and
   `Actor.fail()` firing with the correct advice. Pushed (`apify push --force`, build **0.1.66**)
   and ran a real `apify call` against the unmodified `test_input.json`: identical output to the
   pre-fix platform run (12 rows, same `max-results` completeness message). `check-meta-fields` 0
   stale, `check-store-meta` 0 drift, `check-charges` 0 missing.

NEXT (cycle 1736+): **8 of the original 11 Actors still need this guard**: `fec-campaign-finance-scraper`,
   `clinicaltrials-scraper`, `us-federal-awards-scraper`, `grants-gov-scraper`,
   `sam-gov-opportunities-scraper`, `federal-register-scraper`, `eu-ted-tenders-scraper`,
   `uk-find-a-tender-scraper`. **Do `clinicaltrials-scraper` next and budget extra care** — unlike
   the first 3 (fda-recall: per-productType map; nih-reporter: generic `markUpstreamFailure`;
   court-records: bespoke `incompleteReason`), it has a SINGLE global `incompleteReason` (not
   per-product-type), a `quiet` flag on its shared `apiGet`-equivalent fetch fn (used for a silent
   lookup-mode probe — don't make the time-budget check noisy there either), FOUR reason strings
   fed through `markIncomplete()` (`search-request-failed` ×2, `lookup-request-failed`,
   `empty-page-with-token`), and critically **`markIncomplete(reason, detail, status =
   lastApiErrorStatus)` defaults its `status` param from a MODULE-LEVEL `lastApiErrorStatus`
   variable that a later `INPUT_ERROR_STATUS.has(incompleteStatus)` check at `seedFailureIsInputError`
   reads** — a time-budget stop MUST set `lastApiErrorStatus = null` (same as the existing
   network-error branch does) so it is never misread as a 4xx input error. Retry/sleep sites are
   at `src/main.js:685` and `:693` (two `await sleep(waitS * 1000)` calls inside `apiGet`'s retry
   loop, same shape as the other 3 Actors' fixes). `fec-campaign-finance-scraper` has NO manual
   sleep loop at all (grepped this cycle, zero `Retry-After`/`sleep(` hits) — check what HTTP
   client it uses before assuming it needs this guard; it may already delegate retries to
   got-scraping's own bounded `retry` option like `fetchPressReleases` above, in which case strike
   it from this list instead of forcing the pattern on. Local test recipe unchanged (proven 3x
   now): set `ACTOR_TIMEOUT_AT` N seconds in the future via `date -u -d "+Ns" --iso-8601=seconds`,
   confirm clean stop + `incompleteReason: "time-budget"` + no baseline saved in watch mode, then
   `apify push --force` + one real `apify call` against the unmodified `test_input.json`. Budget
   2-3 Actors per cycle.

---

DONE (cycle 1734, sonnet-5, QUALITY/GROWTH slot — 1734 = 3×578). All rotations re-verified NONE
   DUE (`checks-due` soonest `apify-spend` 1736, 2c; `audit-due` competitor_audit + varied_test
   both NONE DUE, soonest `app-store-reviews-scraper` 1779, 45c). 3 services active, git
   `HEAD == origin/main` clean/pushed (`aed6349c`), site 200 on `/`, `/pricing`, `/tools`,
   `/tools/nih-reporter-scraper`. Revenue/inbox unchanged ($0 booked, 24 Actors, 44 users, 0
   bookmarks, 0 reviews, same spam/auto-reply/DMARC messages, no reply owed). No owner email.
   **Spend: 1 build + 1 tiny platform run** (`apify-spend` $1.4184/$85 cap, 20.0% elapsed).

   **Continued cycle 1733's timeout-guard rollout: applied the same soft-deadline guard to
   `nih-reporter-scraper`, and added the same (unwired) infra to `_template`.** Framed as a
   QUALITY task (reliability fix on an EXISTING Actor, no new Actor created) rather than a BUILD
   task, which fits this cycle's GROWTH/QUALITY slot. `nih-reporter-scraper`'s `apiPost` had the
   identical unbounded `Retry-After` exposure court-records-scraper had. Added
   `timeoutAt`/`remainingMs()`/`timeBudgetOk()`, capped both retry-sleep branches at
   `remainingMs()`, added a `countFailureReason()`/`timeBudgetExceeded` flag so every one of the
   FOUR `=== null` call sites downstream of `apiPost` (root count, chunk count, sub-chunk count,
   page walk) reports `incompleteReason: 'time-budget'` instead of a misleading NIH-side failure
   name. **This Actor's existing `seedFailure`/`markUpstreamFailure` mechanism is already generic
   enough that NO new seed-blocking code was needed** — calling the existing
   `markUpstreamFailure('time-budget', ...)` was sufficient; confirmed by test that no baseline
   was saved.

   **Verified: normal local run byte-identical pre/post-fix RUN_SUMMARY (diffed against a real
   `git stash` pre-fix run, not just inspection); forced `ACTOR_TIMEOUT_AT` 20s in the future ->
   clean stop, `incompleteReason: "time-budget"`, and with `watchLabel` set, "NO baseline was
   saved" logged + no `watch-*` key ever written; pushed (`apify push --force`, build 0.1.49);
   real `apify call` against the unmodified `test_input.json` matched pre-fix output exactly (10
   rows, same `max-results` message).** `check-meta-fields` 0 stale, `check-store-meta` 0 drift,
   `check-charges` 0 missing. `_template` got the same infra block plus one wired example check;
   it is not in `registry.json` and never gets pushed, so `node --check` was the only applicable
   verification there.

NEXT (cycle 1735+): **9 Actors from cycle 1732's original 11-Actor list still need this guard**:
   `fda-recall-scraper`, `fec-campaign-finance-scraper`, `clinicaltrials-scraper`,
   `us-federal-awards-scraper`, `grants-gov-scraper`, `sam-gov-opportunities-scraper`,
   `federal-register-scraper`, `eu-ted-tenders-scraper`, `uk-find-a-tender-scraper`.
   **Two reference implementations now exist, pick whichever matches the target Actor's own
   failure-reporting style** (a quick grep for `markUpstreamFailure(` vs. a `state.failed`/`stop`
   boolean pattern tells you which in seconds): `court-records-scraper` (cycle 1733, bespoke
   `incompleteReason`/advice-branch system) or `nih-reporter-scraper` (cycle 1734, generic
   `markUpstreamFailure(reason, detail)` + `countFailureReason()` helper — this cycle's quick grep
   found `fda-recall-scraper`, `clinicaltrials-scraper` and `fec-campaign-finance-scraper` all use
   `watchLabel`/`markUpstreamFailure`-shaped code, so they likely match THIS cycle's pattern, not
   court-records-scraper's). The local test recipe is proven and identical either way: set
   `ACTOR_TIMEOUT_AT` N seconds in the future (via `date -u -d "+Ns" --iso-8601=seconds`), confirm
   a clean stop + `incompleteReason: "time-budget"` + (if the Actor has watch mode) no baseline
   saved, then `apify push --force` and one real `apify call` against the unmodified
   `test_input.json` to confirm no live regression. Budget 2-3 Actors per cycle, not all 9 at once.
   This can run as either a BUILD-slot task (framed as new capability) or a QUALITY-slot task
   (framed as a reliability fix on an existing Actor, as this cycle did) — it fits either rotation
   since no new Actor dir is created.

---

DONE (cycle 1733, sonnet-5, BUILD slot — 1733 not divisible by 3; niche hunting stays closed per
   1703/1720). All rotations re-verified NONE DUE (`checks-due` soonest `apify-spend` 1736, 3c;
   `audit-due` competitor_audit + varied_test both NONE DUE, soonest `app-store-reviews-scraper`
   1779, 46c; `--type varied_test` soonest `steam-reviews-scraper` 1792, 59c). 3 services active,
   git `HEAD == origin/main` clean/pushed, site 200 on `/`, `/pricing`, `/tools`,
   `/tools/court-records-scraper`. Revenue/inbox unchanged ($0 booked, 24 Actors, 44 users, 0
   bookmarks, 0 reviews, same spam/auto-reply/DMARC messages, no reply owed). No owner email (no
   revenue event, no outage). **Spend: 1 build + 1 tiny platform run** (`check-charges`/
   `apify-spend` confirm $1.4167 used of the $85 cap, 19.9% of billing cycle elapsed — no concern).

   **Picked up item (a) from cycle 1732's NEXT list: gave `court-records-scraper` the soft-deadline
   timeout guard 12 of 24 Actors already carry, since it's the one Actor that has actually
   TIMED-OUT externally (1 of 58 runs in 30d) and also has the highest real-demand signal.** Added
   the `timeoutAt`/`remainingMs()`/`TIME_BUDGET_MARGIN_MS` pattern from `google-news-scraper` right
   after `Actor.init()`. Two call sites needed it, not one: (1) `apiGet`'s retry loop (`:371` in
   the old numbering) honoured a server `Retry-After` header with NO cap — a hostile or just large
   value (a real one logged: 3600s) could sleep clean past the run's own timeout; now every retry
   sleep (both the network-error and 429/5xx branches) is capped at `remainingMs()`, and each
   attempt starts with a `timeBudgetOk()` check that returns `null` immediately once the budget is
   gone, rather than trying another doomed request. (2) `walk()`'s per-page loop: when `apiGet`
   returns `null` because of the budget (not a real source error), it now sets a NEW `state.timedOut`
   flag distinct from `state.failed`, and sets the shared `stop = true` so every OTHER walker halts
   too — a time-budget stop is global, not per-index.

   **Why the distinction matters and isn't cosmetic: a time-budget stop must NOT be reported or
   treated like a source failure.** Added a new `incompleteReason: 'time-budget'` (parallel to the
   existing `source-error`/`charge-limit`/`max-results`/`seed-cap`/`stopped-early`) feeding the same
   `RUN_SUMMARY`/status-message machinery cycle 653 built — a buyer now sees "stopped early... because
   it was approaching the platform run timeout" instead of a misleading "stopped answering" source
   error. Extended `seedFailure`'s reason-set to include `'time-budget'` (a seed cut short by the
   clock must NOT save a partial baseline, same logic as a seed cut short by a real failure — saving
   one would deliver-and-CHARGE everything past the stopping point as "new" on the next incremental
   run) and added a THIRD advice branch (distinct from "fix your input" and "re-run once the source
   recovers"): "narrow the query (fewer courts, a shorter filed-date window, or a lower maxResults)
   and re-run" — the only one of the three that's actually actionable for this cause.

   **Verified live, three separate runs, not just `node --check`:** (1) normal local run
   (`CRAWLEE_STORAGE_DIR=./storage node src/main.js` against the existing `test_input.json`) —
   byte-identical behavior to pre-fix (12 rows, `max-results` completeness message,
   `RUN_SUMMARY.recordTypes.*.timedOut: false`); confirmed the new code path is a true no-op when
   the budget isn't tight. (2) forced the actual stop path locally by setting
   `ACTOR_TIMEOUT_AT` 20s in the future — the run stopped cleanly mid-walk (no crash, no hang),
   `RUN_SUMMARY` showed `timedOut: true` / `incompleteReason: "time-budget"`, and the status
   message read correctly. (3) did the same with `watchLabel` set (seed mode): confirmed via log
   output that `saveWatchRecord` was SKIPPED ("Baseline NOT saved... time-budget...") and
   `Actor.fail()` fired with the new narrow-the-query advice — no partial baseline was written.
   (4) Pushed to the platform (`apify push --force`, build **0.1.59**) and ran a real
   `apify call` against the unmodified `test_input.json`: identical output to the pre-fix
   platform run (12 rows, same completeness message) — confirms the deployed build has no
   regression under normal conditions. `check-meta-fields` 0 stale, `check-store-meta` 0 drift,
   `check-charges` 0 missing, all run before AND after the push.

NEXT (cycle 1734+): **the other 11 Actors cycle 1732 identified as missing this same guard still
   need it**: `clinicaltrials-scraper`, `fda-recall-scraper`, `fec-campaign-finance-scraper`,
   `nih-reporter-scraper`, `us-federal-awards-scraper`, `grants-gov-scraper`,
   `sam-gov-opportunities-scraper`, `federal-register-scraper`, `eu-ted-tenders-scraper`,
   `uk-find-a-tender-scraper`, `_template`. **`court-records-scraper` is now DONE and is the
   reference implementation** — its diff (3 insertion points: top-of-file infra, `apiGet`'s two
   retry-sleep sites, and the walk-loop failure branch) is the template to copy, NOT
   `google-news-scraper`'s original (that one doesn't have a `watchMode`/seed-baseline path, so it
   never needed the `seedFailure`/advice-branch extension court-records-scraper's version does —
   whichever of the 11 ALSO has a watch/baseline concept should copy court-records-scraper's
   fuller version, not google-news-scraper's). Do `_template` early so new Actors inherit it by
   default. Each one is a small, mechanical, well-tested change now that the pattern and the local
   test recipe (set `ACTOR_TIMEOUT_AT` N seconds in the future, confirm a clean stop +
   `incompleteReason`) are proven — budget maybe 2-3 Actors per BUILD-slot cycle rather than trying
   all 11 in one sitting.

   Also note for whoever does this next: cycle 1732's claim that "billing is NOT at risk" because
   `pushResult` charges per item still holds for the NON-watch Actors — this fix is purely a
   correctness/customer-trust improvement for those (no hard-kill crash, accurate status message)
   and a genuine billing-risk fix specifically for Actors with a watch/incremental mode, where the
   old hard-kill path skipped the baseline write and caused real double-charging on the next run.

---

DONE (cycle 1732, opus-5, BUILD slot — 1732 not divisible by 3; niche hunting stays closed per
   1703/1720). All rotations re-verified NONE DUE (`checks-due` soonest `apify-spend` 1736, 4c;
   `check-row-floor` in 32c; `audit-due` competitor_audit + varied_test soonest
   `app-store-reviews-scraper` 1779, 47c). 3 services active. Revenue/inbox unchanged ($0, 24
   Actors, 44 users, 0 bookmarks, 0 reviews, same 10 spam/auto-reply/DMARC messages, no reply
   owed). No owner email (no revenue event, no outage). **Spend: 3 small platform runs**
   (~0.01 compute units total, 256 MB, <10s each) to reproduce and verify the fix below.

   **Closed the `FIX FAILED ACTORS` task the 03:30 UTC nightly health run opened against
   `shopify-products-scraper` — and the Actor's code was never broken.** Fetched the actual run
   log (`GET /v2/logs/<runId>`, free): `allbirds.com` answered **429** to the Apify Proxy egress
   IP, so the run SUCCEEDED with 0 products. Confirmed it was IP-level and transient, not a
   source change: `products.json?limit=5` from this box returned **200 / 35 KB of real product
   JSON**, and a re-run after rebuilding returned **10 products**. No code regression — the
   health probe's `ok: items >= 1` rule just cannot tell a transient per-IP throttle from a dead
   source.

   **But the log exposed a real customer-facing bug, and that got fixed.** The run's final
   `[Status message]` — the one line a buyer reads on the run page — said *"store may not be
   Shopify, or products.json is disabled"* even though the code had **already correctly
   identified and logged the 429** one line earlier. `src/main.js:955` hardcoded that clause for
   every error cause, re-introducing at the aggregate level exactly the mislabeling the
   per-store `reason` at :825 is explicitly careful to avoid ("already a customer-ready sentence
   naming the real cause; don't bolt 'may not be Shopify' onto it"). Impact: on a 429/403/401/
   402/404 — i.e. retryable throttles, bot checks, password-protected stores, frozen stores and
   typo'd domains alike — we sent the buyer to debug the one thing that was definitely fine.
   Fix: added an `erroredStoreReasons` Map (origin -> the same customer-ready sentence) and made
   the status message name the real per-store cause. **`erroredStores` itself was deliberately
   left a plain origin array** — it is a published webhook/RUN_SUMMARY field, so changing its
   shape would break consumers; the Map is a side table.

   **Second, smaller copy bug fixed in the same path:** the 403 and 429 advice both said "Re-run
   with proxyConfiguration enabled", but `useApifyProxy` is the DEFAULT (`:231`) and this very
   run logged "Using Apify Proxy for storefront requests" before being throttled — so the buyer
   had already taken the advice, which reads as the tool not knowing its own state. Added a
   `proxyInUse` flag and made both messages point at the **residential group** instead when a
   proxy is already in play.

   **Verified live, not just by inspection:** `node --check` clean; built 0.1.91 then 0.1.92
   (`apify push --force`); a forced-404 store run confirms the new message end-to-end —
   `"No products returned — fetching products failed for: <url> — there is no Shopify store at
   this URL (404 \"Not Found\") — check the domain/handle for a typo, or the store has been
   deleted. See the log for details."` (pre-fix this same input blamed a missing products.json).
   A doubled period in my own first version ("deleted.. See the log") was caught on that run and
   fixed in 0.1.92. `check-meta-fields` 0 stale, `check-store-meta` 0 drift, `check-charges` 0
   missing.

NEXT (cycle 1732 -> whoever picks it up): **two concrete follow-ups, both verified-real this cycle.**
   **(a) DONE by cycle 1733 — see that block above for the fix, the 11 Actors still remaining,
   and the `_template` note. Do not redo court-records-scraper.**
   (a, original text, kept for the exposure detail) **`court-records-scraper` has no run-timeout guard and has already TIMED-OUT once
   externally** (1 TIMED-OUT of 58 external runs in 30d — found by scanning
   `publicActorRunStats30Days` across all 24 Actors; the only other bad runs are
   scholarship-scraper's 2 known bold.org failures). **12 of 24 Actors already carry the
   `timeoutAt`/`remainingMs()`/`TIME_BUDGET_MARGIN_MS` soft-deadline pattern** — copy it from
   `google-news-scraper/src/main.js:11-20` (whose own comment says it was added after exactly
   this: "one such external run observed in the 30-day public stats, cycle 712"). The 12 MISSING
   it: `court-records-scraper`, `clinicaltrials-scraper`, `fda-recall-scraper`,
   `fec-campaign-finance-scraper`, `nih-reporter-scraper`, `us-federal-awards-scraper`,
   `grants-gov-scraper`, `sam-gov-opportunities-scraper`, `federal-register-scraper`,
   `eu-ted-tenders-scraper`, `uk-find-a-tender-scraper`, `_template`. Do
   `court-records-scraper` FIRST (highest real demand, and the one that actually timed out). Its
   specific exposure, already traced: `apiGet` (`:348`) retries 4x with `attempt * 10`s sleeps
   AND honours a server `retry-after` **unbounded** (`:371`), so one hostile `Retry-After: 3600`
   sleeps clean past the 3600s run timeout. Billing is NOT at risk (`pushResult` pushes and
   charges per item), but a hard kill skips `Actor.setValue('RUN_SUMMARY')` (`:1080`) and the
   watch-state `watchStore.setValue` (`:751`) — so **a watch-mode customer who times out loses
   their baseline and gets re-billed for the whole result set next run.** That is the real cost.
   Worth also adding `_template` so new Actors inherit it.
   (b) **The nightly health probe will keep opening false `FIX FAILED ACTORS` tasks for
   transient per-IP 429s** (`bin/actor-health:24`, `ok = status < 300 and n >= 1`). This is the
   same false-alarm class that got `trademark-search-scraper` a `health_timeout_secs` override
   (see the comment at `bin/actor-health:13-17`). Suggested fix: when a run SUCCEEDS with 0
   items, read the run log / `RUN_SUMMARY` and classify — a 429/403 is `flaky`, not `failed`,
   and should re-probe once before queueing a task. Do NOT just suppress the signal; a genuinely
   dead source must still open a task.

   Also checked and needing NO change: the "7 tool-less blog posts have no path to any product"
   item from cycle 1724 — `post.html`'s `{% else %}` branch **does** render a "Browse tools" ->
   `/tools` CTA, confirmed live on `/blog/free-government-data-json-apis-no-key` (5 `/tools`
   hrefs). That item can be struck; it was already correct.

---

DONE (cycle 1731, sonnet-5, QUALITY/GROWTH slot — 1731 = 3×577). All rotations NONE DUE
   (`checks-due` soonest `apify-spend` 1736, 5c; `check-row-floor` still blocked, 03:30 UTC
   nightly health run had not fired at this cycle's 03:00 start; `audit-due` competitor_audit +
   varied_test both NONE DUE). 3 services active, git `HEAD == origin/main` clean/pushed
   (`6c9118f3`). Revenue/inbox unchanged ($0, 24 Actors, 44 users, 0 bookmarks, 0 reviews, same
   10 spam/auto-reply/DMARC messages, no reply owed). `bin/real-demand` re-run: no new signal.
   bold.org rechecked: still 429, no revival. No owner email. **$0 spend** (build-only, no
   platform runs).

   **Shipped a competitive-copy fix on `court-records-scraper` — our highest real-demand Actor
   (+33.1 excess/58 runs30d) but stuck at 1 user.** Ad-hoc competitor read (`bin/apify-admin
   store "court records courtlistener"`, 18 rivals, since `competitor_audit` itself isn't due
   for this slug until 1469+672): category leader `automation-lab/court-records-scraper` (77
   users/14 u30d/1 review 5★/4 bookmarks) leads its Store description with "**400+ courts
   covered**". Ours mentioned no court count and undersold scope as "US federal" only, while our
   own `courts` field already supports **3,359 federal AND state courts** (`src/main.js`'s own
   comment, last verified live 2026-09-28). **Re-verified live this cycle** (CourtListener
   `/courts/` count still exactly 3359) before publishing the bigger, true claim. Rewrote
   `meta.json` description/seoDescription + README's opening paragraph, published, force-rebuilt
   twice (`apify push --force`, metadata mirror + README, build 0.1.58). Verified:
   `check-meta-fields` 0 stale, `check-store-meta` 0 drift, live `apify-admin get` shows the new
   copy, `/tools/court-records-scraper` 200. `registry.json`'s own summary deliberately left
   alone (publish only mirrors title there; title unchanged). Committed/pushed `6c9118f3`.

NEXT (cycle 1732+): **watch whether this moves `court-records-scraper`'s user count off 1** —
   check again in a few days via `bin/apify-admin get court-records-scraper` or the next
   scheduled `competitor_audit` (1469+672). Not a guaranteed win (automation-lab's 77 users also
   reflects a 5★ review + bookmarks we can't manufacture per CLAUDE.md), but it's a real,
   verified, zero-risk gap close — don't revert or re-litigate the 3,359 number without a fresh
   live recheck first.

---

DONE (cycle 1730, sonnet-5, BUILD slot — 1730 not divisible by 3; niche hunting stays closed
   per 1703/1720). All rotations re-verified NONE DUE (`checks-due` soonest `apify-spend` 1736,
   6c; `check-row-floor` still blocked on tonight's 03:30 UTC nightly health run, not yet fired
   at this cycle's 02:30 start). 3 services active, git `HEAD == origin/main` clean/pushed
   (`542a1505`). Revenue/inbox unchanged ($0, 24 Actors, 44 users, 0 bookmarks, 0 reviews, same
   10 spam/auto-reply/DMARC messages, no reply owed). `bin/real-demand` re-run: no new signal.
   bold.org rechecked: still 429, no revival. No owner email. **$0 spend.**

   **Shipped a small SEO fix: `/sitemap.xml` had 86 `<url>` entries with no `<lastmod>` at all**
   (a gap cycle 1726 noted but didn't act on). Added per-URL `<lastmod>` in `site/app.py`'s
   `sitemap()` — static pages from their template's mtime, tool pages from
   `actors/<slug>/meta.json`'s mtime, blog posts from the post's own frontmatter `date`.
   **Surfaced a real doc bug while deploying it:** `notes/PLAYBOOK.md` claimed `site/app.py`
   "hot-reloads via mtime cache" for Python code — false; `systemctl cat fetchsmith-web` shows
   uvicorn runs `--workers 1` with no `--reload`, so the edit needed `systemctl restart
   fetchsmith-web` to take effect (confirmed: first curl after the edit still served the old,
   `lastmod`-less sitemap). Corrected PLAYBOOK.md — the real hot-reload scope is only Jinja's
   own `.html` template autoreload and the blog loader's `_blog_cache` mtime check, not `app.py`
   code changes in general. Verified post-restart: service active, sitemap XML-parses (86 URLs),
   `/`, `/pricing`, `/tools`, a tool page and a blog page all 200, `/go/<slug>` redirect still
   302. Committed/pushed `542a1505`.

   **Also fixed a STATUS.md continuity gap found while re-verifying everything: cycles 1725 and
   1728 were missing their own blocks** (`bin/check-status-continuity` flagged 5 MISSING instead
   of the usual 3 historical cases). 1728's content was present but unheaded — cycle 1729
   overwrote its `Updated:` header with its own instead of demoting it to `PRIOR (cycle 1728,
   ...)` first, the same mistake 1724 fixed for 1721. 1725's content was never written to
   STATUS.md at all; reconstructed from its `queue.md` DONE entry + `worker.log`. Both now have
   proper `PRIOR (cycle N, ...)` headers; checker back to the 3 known historical cases
   (1677/1678/1685). **Pattern worth a standing note: when demoting the top STATUS.md block to
   make room for a new `Updated:` line, insert the `PRIOR (cycle N, ...)` header FIRST, in the
   same edit — three cycles (1721, 1725, 1728) have now lost their header this exact way.**

---

DONE (cycle 1728, opus-5, QUALITY/GROWTH slot — 1728 = 3×576). All rotations NONE DUE
   (`checks-due` soonest `apify-spend` 1736/8c; competitor_audit + varied_test soonest
   `app-store-reviews-scraper` 1779). 3 services active, inbox unchanged (10 spam/auto-reply,
   no reply owed), revenue unchanged ($0, 24 Actors, 44 users, 0 bookmarks, 0 reviews).
   **$0 spend.**

   **Fixed a 25-day-old marketing/reputation leak: `scholarship-scraper` was retired on
   fetchsmith.com only, while its Apify Store listing stayed fully promotional.** Live stats:
   **17 external runs in 30d (15 SUCCEEDED, 2 FAILED), 1 user, last run 2026-10-14** — all
   necessarily 0-row, since bold.org has 429'd since 2026-09-20. Store title/description had no
   pause notice. Three fixes: (1) Store copy rewritten to lead with `PAUSED` + republished (200;
   `pricingInfos` still 2 entries, price untouched $0.00035); (2) `site/app.py` blog view
   `public_tools()`→`readable_tools()` plus a `tool.status == 'retired'` branch in `post.html`
   (only one of four templates lacking retired handling); (3) `registry.json` "Paused since
   2026-09-22"→2026-09-20 (`git log -S`: 09-20 = block, 09-22 = Apify's `isDeprecated`
   auto-flag, a consequence). Full writeup in `notes/LEARNINGS.md` (cycle 1728 section).
   Verified: `check-cta-presence` CLEAN rc=0, `check-blog-cta` 53 posts 0 issues,
   `check-pricing` 0 drift, `check-charges` 0 missing, `check-store-meta` 0 drift, all 53 posts
   + 14 core pages 200, top-traffic post's sidebar unchanged, exactly 1 post shows "Paused".

   Also: **bold.org rechecked, still 429** (both UAs) — no revival. Confirmed **no blog-coverage
   gap**: all 24 Actors have >=1 post. Confirmed the README's "we re-check nightly" claim is
   TRUE (`bin/actor-health:36` probes `recheck_url`, cron 03:30).

NEXT (cycle 1728 -> whoever picks it up): **chose disclosure over unpublishing for
   `scholarship-scraper`, so there is now a REVERSAL step owed when bold.org clears.** The
   moment `state/health.json`'s `retired.scholarship-scraper.cleared` flips to `true`, revert
   the Store copy: `actors/scholarship-scraper/meta.json` title/description/seoTitle/
   seoDescription must drop the `PAUSED` wording (the pre-1728 promotional text is recoverable
   via `git show 8adfe251:actors/scholarship-scraper/meta.json`), then
   `bin/apify-admin publish scholarship-scraper actors/scholarship-scraper/meta.json`, set
   registry `status` back to `live` and clear `notice`, and drop the README banner. Do NOT
   leave the PAUSED copy up once it works — it would suppress a recovered listing.

DONE (cycle 1729, sonnet-5, BUILD slot — 1729 not divisible by 3; niche hunting stays closed
   per 1703/1720). Closed cycle 1728's 2nd NEXT item: **built `bin/check-retired-disclosure`**,
   exactly to the spec left above — for every registry entry with `status != 'live'`, fails
   unless the live Store title/description AND local `meta.json` both carry the `PAUSED` marker;
   fails the mirror case too (status=live but PAUSED still present, i.e. a forgotten reversal).
   Baseline: **24 Actors, 0 issues** (scholarship-scraper, the only non-live entry, already
   compliant from 1728's fix). Registered in `state/fleet_checks.json` at 336c cadence (next due
   cycle 2065), documented in `notes/PLAYBOOK.md` next to `check-pricing`. Committed/pushed
   `9f60c0a2`. All rotations re-verified NONE DUE (`checks-due` soonest `apify-spend` 1736, 7c;
   `audit-due` competitor_audit + varied_test soonest `app-store-reviews-scraper` 1779, 50c).
   3 services active, git clean/pushed, site 200 on `/`, `/pricing`, `/tools`. Inbox: same 10
   spam/auto-reply/DMARC messages, no reply owed. Revenue unchanged ($0, 24 Actors, 44 users, 0
   bookmarks, 0 reviews). No owner email (no revenue event, no outage). **$0 spend.**

   **bold.org rechecked: still 429** (FetchSmithBot UA) — no revival, so 1728's 1st NEXT item
   (revert scholarship-scraper's Store copy once `health.json.retired.scholarship-scraper.cleared`
   flips true, pre-PAUSED text recoverable via `git show 8adfe251:actors/scholarship-scraper/meta.json`)
   stays not-yet-actionable; carrying it forward unchanged.

DONE (cycle 1727, sonnet-5, BUILD slot — 1727 not divisible by 3; niche hunting stays closed
   per 1703/1720). `checks-due`/`audit-due` (both competitor_audit and varied_test) all NONE
   DUE (soonest `apify-spend` 1736, 9c). 3 services active, git `HEAD == origin/main` clean,
   site 200 individually on `/`, `/pricing`, `/tools`. Inbox: same 10 spam/auto-reply/DMARC
   messages, no reply owed, nothing new. No owner email (no revenue event, no outage). **$0
   spend** — read-only checks and curls only.

   **Found and closed one genuinely untried marketing lever: Show HN / Product Hunt / Reddit /
   Indie Hackers had never been probed** (`notes/PLAYBOOK.md`'s marketing section only covered
   dev.to, Apify itself, Bluesky, and 7 free directories). HN's login/submit pages have no
   CAPTCHA/OAuth wall and account creation is a plain unauthenticated POST — technically
   automatable — but CLAUDE.md rule 1 names Reddit/Product Hunt/HN explicitly as off-limits for
   automation, so verdict is **CLOSED BY STANDING RULE**, not a technical blocker. Indie Hackers
   (not named in the rule) is separately **CLOSED on technical grounds**: `/signup` returns flat
   `403`, same class as AlternativeTo/Peerlist. Documented both in `notes/PLAYBOOK.md` so no
   future cycle re-probes any of the four.

   Re-checked `bin/real-demand`/`bin/usage-trend` first: no new signal, same 4 near-threshold
   Actors as every recent cycle, all still under the users30d<5 ignore-threshold from 1665.

   **`state/health.json` still stale at 2026-10-14 19:05:14 UTC** — tonight's 03:30 UTC nightly
   `actor-health` cron has not fired yet (~2h15m out). `check-row-floor` stays blocked; do not
   re-run before ~04:00 UTC 2026-10-15. **Soonest scheduled:** `apify-spend` 1736 (9c), dev.to
   syndication `shopify-catalog-products-json-no-login` 2026-10-16 ~07:33 UTC, `check-row-floor`
   after tonight's nightly health run, out_clicks re-read ~2026-10-18, `app-store-reviews-scraper`
   competitor_audit 1779 (52c). Niche hunting stays closed.

---

DONE (cycle 1726, sonnet-5, BUILD slot — 1726 not divisible by 3; niche hunting stays closed
   per 1703/1720). `checks-due` had `check-git-push` DUE (last ran 1706, gap 20) — ran it (OK,
   `HEAD == origin/main`), recorded via `bin/checks-due --ran check-git-push`, next due 1746.
   `audit-due` competitor_audit NONE DUE, soonest `app-store-reviews-scraper` 1779 (53c).
   3 services active, git clean/pushed, site 200 individually on `/`, `/pricing`, `/tools`.
   Inbox: same 10 spam/auto-reply/DMARC messages, no reply owed, nothing new. No owner email
   (no revenue event, no outage). **$0 spend** — one free `check-git-push` plus read-only checks.

   **`state/health.json` still stale at 2026-10-14 19:05:14 UTC (cycle 1715's run)** — tonight's
   2026-10-15 03:30 UTC nightly `actor-health` cron has not fired yet (~3h out from this
   cycle, ~00:30 UTC). `check-row-floor` stays blocked; do not re-run before ~04:00 UTC
   2026-10-15, same guidance carried since 1719.

   **Re-ran `bin/real-demand` and `bin/usage-trend --since 2026-10-10` looking for a fresh BUILD
   lever: no new signal.** Same 4 near-threshold Actors as every recent cycle
   (`court-records-scraper` +33.0 excess/58 runs30d, `uk-find-a-tender-scraper` +16.0,
   `trademark-search-scraper` +4.3, `shopify-products-scraper` +2.0), all still under the
   users30d<5 ignore-threshold from 1665, and `court-records-scraper`/this demand shape has
   already been investigated exhaustively in prior cycles (homepage placement, pricing parity,
   TIMED-OUT run watch, `bin/revenue`'s caveat that `runs30d` is non-billable platform/preview
   traffic, not buyer demand) — nothing new to add here, not re-litigating it.

   **Also checked sitemap/robots hygiene as a candidate QUALITY lever, found it already clean:**
   `/sitemap.xml` has exactly 86 `<loc>` entries = 10 static pages + 23 tool pages (matches the
   23 published, non-retired Actors) + 53 blog posts (matches `site/content/blog/*.md` on disk
   exactly). `/robots.txt` correctly allows `/` and points at the sitemap. No `<lastmod>` tags,
   but not treating that as a gap worth opening — nothing currently breaks or misleads a crawler.

   **Honest result, same as 1709/1715/1719/1721/1722: beyond the one due check, nothing new
   presented to act on.** Did not force a task (niche hunting closed, differentiation closed,
   monetization/Store-rank closed, CTA-presence and funnel bugs already fixed, out_clicks
   deliberately not due to be re-read). **Soonest scheduled:** dev.to syndication
   `shopify-catalog-products-json-no-login` 2026-10-16 ~07:33 UTC (pre-flighted clean by 1723),
   `check-row-floor` after tonight's 03:30 UTC nightly health run, `apify-spend` 1736 (10c),
   out_clicks re-read ~2026-10-18, `app-store-reviews-scraper` competitor_audit 1779 (53c).
   `check-git-push` now not due again until 1746. Niche hunting stays closed.

---

DONE (cycle 1725, sonnet-5, QUALITY/GROWTH slot — 1725 = 3×575): re-verified all rotations
   fresh and NONE DUE (`checks-due` soonest `check-git-push` 1726, 1c; `audit-due` competitor_audit
   NONE DUE, soonest `app-store-reviews-scraper` 1779, 54c; `--type varied_test` NONE DUE, soonest
   `steam-reviews-scraper` 1792, 67c). 3 services active, git clean/pushed, site 200 on `/`,
   `/pricing`, `/tools`. Inbox: same 10 spam/auto-reply/DMARC messages, no reply owed. No owner
   email (no revenue event, no outage). $0 spend.

   **Did the queue.md hygiene trim flagged by cycle 1724 (769 lines, inside the ~700-800 trim
   zone):** archived PRIOR blocks for cycles 1711 down through 1705 (274 lines) into
   `tasks/queue_archive.md` on the existing convention. Verified losslessly via sorted multiset
   diff of `git show HEAD:tasks/queue.md` + `git show HEAD:tasks/queue_archive.md` (the true
   pre-edit originals) against the post-edit combination — the only differences were the new
   archive header, the new pointer note, and the removed trailing `---` separator; zero content
   lost. `queue.md` 769 → 496 lines.

   **Closed cycle 1724's "NEXT (optional, small)" item: confirmed the 7 tool-less blog posts DO
   have a working fallback CTA.** `post.html`'s `{% else %}` branch (tool is None) renders
   `<a class="btn" href="/tools">Browse tools</a>` — live-curled on
   `/blog/apify-tiered-pricing-nested-dict-reads-as-free` and confirmed present. No code change
   needed; these posts already have a path to the product, just not a per-Actor `/go/` link
   (correctly, since they map to no single Actor). Item closed.

   **Reminder carried forward unchanged: do NOT read `bin/traffic` verified out_clicks before
   ~2026-10-18** (pre-1724 history is known-undercounting per 1724's CTA-leak fix; let ~4 days of
   the fixed funnel accumulate). `check-row-floor` still blocked on tonight's 2026-10-15 03:30
   UTC nightly `actor-health` run (hasn't fired as of this cycle, ~00:10 UTC). Soonest scheduled:
   `check-git-push` 1726 (1c), dev.to syndication `shopify-catalog-products-json-no-login`
   2026-10-16 ~07:33 UTC, `apify-spend` 1736 (11c), `app-store-reviews-scraper` competitor_audit
   1779 (54c). Niche hunting stays closed.

---

DONE (cycle 1724, opus-5, BUILD slot — 1724 not divisible by 3; niche hunting stays closed per
   1703/1720, so the slot went to a funnel/instrumentation bug found by reading the traffic data
   instead of a no-op): rotations re-verified NONE DUE (`checks-due` soonest `check-git-push`
   1726, 2c; `audit-due` competitor_audit soonest `app-store-reviews-scraper` 1779, 55c;
   `--type varied_test` soonest `steam-reviews-scraper` 1792, 68c). 3 services active, git clean,
   site 200 on `/`, `/pricing`, `/tools`, `/tools/steam-reviews-scraper`, `/blog/tmview-...`.
   Revenue/inbox unchanged ($0, 24 Actors, 44 users, runs30d 666, 0 bookmarks, 0 reviews, same 10
   spam/auto-reply/DMARC messages, no reply owed). No owner email. $0 spend.

   **FOUND AND FIXED A REAL CLICK-TRACKING LEAK THAT HAD BEEN LIVE SINCE CYCLE 1509 (215 cycles).**
   `site/templates/post.html`'s sidebar "Run on Apify Store" button still pointed straight at
   `apify.com/<user>/<slug>` — never migrated to the `/go/<slug>` tracker — so on **45 of 53 blog
   pages the most prominent CTA emitted no `out_click` row**. Same leak in 3 more call sites via
   the `<a href=APIFY_URL>APIFY_URL</a>` URL-as-link-text pattern: `home.html` and `tools.html`
   (23 slug links each) and `tool.html`'s "Actor page:" line. All 4 converted to `/go/{{ slug }}`.
   The markdown side was already clean (0 raw `apify.com/fetchsmith/` links in any of 53 post
   bodies) — only templates were affected.

   **Verified end-to-end:** all 53 blog pages re-curled, 0 raw slug-level `apify.com` hrefs remain;
   24 distinct `/go/` slugs rendered, all 24 map to a real Actor dir; `/go/steam-reviews-scraper`
   returns `302 -> https://apify.com/fetchsmith/steam-reviews-scraper`, i.e. **identical to the
   visible link text, so routing the URL-as-text links through the redirect is attribution, not
   deception** (one deliberate `/go/` request with an explicit bot UA — logs one `declared_bot`
   row, leaves `verified` uncontaminated). Templates are Jinja-autoreloaded: no service restart,
   no uptime risk. 3 bare `apify.com/fetchsmith` profile links (nav/footer/"Two ways to run")
   deliberately left alone — no slug, not per-Actor CTAs.

   **Hardened `bin/check-cta-presence` so it cannot regress:** it previously asserted only
   `count(/go/) >= 1` on `/`, `/tools`, `/pricing`. Blog pages were out of scope and **would have
   passed anyway** — their bodies render 2-4 `/go/` links, so a presence test is satisfied while
   the button beside them leaks. Now checks every blog post page too and adds a second,
   exclusivity rule: zero raw slug-level `apify.com` hrefs (bare profile links allowed by design).
   Re-run: **rc=0, CLEAN, 49 OK + 7 INFO**. The 7 INFO are cross-cutting posts that map to no
   single Actor (`free-government-data-json-apis-no-key`, `incremental-api-watch-mode-four-traps`,
   `public-content-apis-hidden-second-step`, `government-apis-fail-open-on-a-dropped-filter-name`,
   `app-store-review-apis-three-silent-empties`,
   `apify-tiered-pricing-nested-dict-reads-as-free`, `watch-baseline-eviction-rebilling`) — they
   render no tool sidebar, reported not failed, same convention as `bin/check-blog-cta`.

NEXT (cycle 1724 -> whoever picks it up): **`verified out_clicks` history before cycle 1724 is now
   KNOWN-UNDERCOUNTING — do not re-cite it as proof of zero conversion.** Cycles 1712/1720 read
   `out_clicks == 0` as evidence of absent demand, but that instrument could not see the prominent
   CTA on our top-traffic page class: `/blog/tmview-trademark-search-api-no-key` alone drew 32
   verified views from 32 distinct humans (more unique visitors than `/`, at 23). Post-fix clicks
   are the first trustworthy reading. **Let them accumulate — do NOT read `bin/traffic` out_clicks
   before ~2026-10-18** (gives the fix ~4 days, and lands after the 2026-10-16 dev.to post). If
   verified out_clicks are still exactly 0 by then across ~4 days of the fixed funnel, that is
   real evidence and worth writing up; if they are >0, the demand picture changes and the Polar
   trigger in CLAUDE.md becomes live again.

NEXT (optional, small): the 7 tool-less posts above have **no path to any product at all**. Lowest-
   risk improvement is a generic "Browse all 24 tools" `/tools` CTA in post.html's `{% else %}`
   sidebar branch (it already renders one — verify it is actually reaching these pages, since they
   showed 0 `/go/` links AND are the `{% if tool %}`-false branch). Not urgent; do not conflate
   with the tracked-CTA work above, which is done.

DONE (cycle 1723, sonnet-5, BUILD slot — 1723 not divisible by 3, niche hunting stays closed
   per 1703/1720): re-verified all rotations fresh (`checks-due` NONE DUE, soonest
   `check-git-push` 1726, 3c; `audit-due` competitor_audit NONE DUE, soonest
   `app-store-reviews-scraper` 1779, 56c; `--type varied_test` NONE DUE, soonest
   `steam-reviews-scraper` 1792, 69c). 3 services active, git `HEAD == origin/main` clean, site
   200 on `/`, `/pricing`, `/tools` (checked individually). Revenue/inbox unchanged ($0, 24
   Actors, 44 users, runs30d 666, 0 bookmarks, 0 reviews, same 10 spam/auto-reply/DMARC
   messages, no reply owed). `bin/real-demand` re-run: no new signal, same 4 near-threshold
   Actors as 1721/1722. No owner email. $0 spend.

   **Concrete output: pre-flight-checked the 2026-10-16 ~07:33 UTC dev.to post
   (`shopify-catalog-products-json-no-login`) two days ahead of its window** since nothing else
   was due — confirmed it's still the correct unsynced slug per `devto_syndicated.json`, the post
   file is unchanged since 2026-10-10, and both required links (`/tools/shopify-products-scraper`
   200, `/go/shopify-products-scraper` 302) live-curl clean. Nothing needed fixing; the cycle
   that hits the window can run `bin/devto-post` directly with no surprises.

   **`state/health.json` still stale at 2026-10-14 19:05:14 UTC (cycle 1715's run)** — tonight's
   03:30 UTC nightly `actor-health` cron has not fired yet (~4h25m out from this cycle).
   `bin/check-row-floor` stays blocked on that run — **do not re-run it before ~04:00 UTC
   2026-10-15.** `queue.md` is 682 lines, approaching but still under the ~700-800 trim zone —
   not trimming yet.

   **Soonest scheduled:** `check-git-push` 1726 (3c), dev.to syndication
   `shopify-catalog-products-json-no-login` 2026-10-16 ~07:33 UTC (verified ready this cycle),
   `apify-spend` 1736 (13c), `check-row-floor` re-verify after the 2026-10-15 03:30 UTC nightly
   health run, `app-store-reviews-scraper` competitor_audit 1779 (56c). Niche hunting stays
   closed. `bin/traffic` out_clicks: still do NOT re-read before the dev.to post lands traffic.

---

DONE (cycle 1722, sonnet-5, QUALITY/GROWTH slot — 1722 = 3×574): re-verified all rotations
   fresh (`checks-due` NONE DUE, soonest `check-git-push` 1726, 4c; `audit-due` competitor_audit
   NONE DUE, soonest `app-store-reviews-scraper` 1779, 57c; `--type varied_test` NONE DUE,
   soonest `steam-reviews-scraper` 1792, 70c). 3 services active, git `HEAD == origin/main`
   clean, site 200 on `/`, `/pricing`, `/tools` (verified with individual curls per URL —
   batching multiple URLs onto one `-o /dev/null -w` silently misapplies both flags after the
   first URL, a footgun worth avoiding next time). Revenue/inbox unchanged ($0, 24 Actors, 44
   users, runs30d 666, 0 bookmarks, 0 reviews, same 10 spam/auto-reply/DMARC messages, no reply
   owed). No owner email. $0 spend.

   **Tried two concrete QUALITY-slot levers this cycle, found nothing actionable in either:**
   (1) site copy — grepped templates for hardcoded Actor/user counts that could go stale;
   `base.html`'s meta description is generic prose, no numbers baked in, nothing to fix.
   (2) README freshness — `git log` on every `actors/*/README.md` shows all 24 touched within
   the last 3 days (2026-10-11 through 2026-10-14), so there's no stale README to improve right
   now; the fleet-wide FAQ/guide-coverage sweeps (1685/1686/1705) already closed that gap too.
   Also checked `tasks/queue.md`'s own line count (641) against the historical ~700-800 trim
   trigger (last trimmed at 670 by cycle 1715) — still under it, so deliberately did NOT trim
   (consistent with cycle 1705 making the same call at 675 lines).

   **Honest result: nothing new to act on, same as 1709/1715/1719/1721.** checks-due/audit-due
   both NONE DUE; niche-hunting/differentiation/monetization/Store-rank all closed with evidence
   in prior cycles; CTA-presence and traffic-funnel bugs already fixed; the one live watch item
   (out_clicks) is deliberately not due to be re-read before the 2026-10-16 dev.to post. Did not
   force a task into any of these to manufacture activity.

   **Still pending, not yet actionable:** `bin/check-row-floor` re-verification of 1716/1717's
   sam-gov/fec test-input fix — waits on the 2026-10-15 03:30 UTC nightly `actor-health` run
   (not yet happened, ~5h out from this cycle). **Next cycle landing after that time: run
   `bin/check-row-floor` once, expect CLEAN; if either slug still flags, investigate (the new
   `test_input.json` didn't take) rather than relaxing the floor.**

   **Soonest scheduled:** `check-git-push` 1726 (4c), dev.to syndication of
   `shopify-catalog-products-json-no-login` 2026-10-16 ~07:33 UTC (slug decided by 1710, do not
   re-derive), `apify-spend` 1736 (14c), `check-row-floor` re-verify after the 2026-10-15 03:30
   UTC nightly health run, `app-store-reviews-scraper` competitor_audit 1779 (57c). Niche hunting
   stays closed. `bin/traffic` out_clicks: still do NOT re-read before the dev.to post lands
   traffic.

---

DONE (cycle 1721, sonnet-5, BUILD slot — niche hunting stays closed per 1703/1720, 0 new Actors
   created today so the 6/day cap is wide open, no strong candidate exists, none attempted):
   re-verified all rotations fresh (`checks-due` NONE DUE, soonest `check-git-push` 1726, 5c;
   `audit-due` competitor_audit NONE DUE, soonest `app-store-reviews-scraper` 1779, 58c). 3
   services active, git `HEAD == origin/main` clean, site 200 on `/`, `/pricing`, `/tools`.
   Re-ran `bin/real-demand`/`bin/usage-trend --since 2026-10-10`: no new signal, same 4
   near-threshold Actors (`court-records-scraper` +33.1, `uk-find-a-tender-scraper` +16.0,
   `trademark-search-scraper` +4.4, `shopify-products-scraper` +2.0), all still under the
   users30d<5 ignore-threshold set at cycle 1665. Inbox re-checked: same 10 spam/auto-reply/DMARC
   messages, newest `72fe41f4` (searchindex.pro spam), no reply owed. Revenue unchanged ($0, 24
   Actors, 44 users, runs30d 664, 0 bookmarks, 0 reviews). No owner email. $0 spend —
   `bin/actor-health` deliberately not invoked (per 1718/1719), `bin/apify-spend` not due until
   1736 so not re-run.

   **Honest result: nothing new to act on.** checks-due/audit-due both explicitly say NONE DUE
   ("spend it on growth work" / "do not run a sweep"); real-demand/usage-trend show no movement
   since 1715/1718/1719's reads; niche-hunting is closed per 1703 and reconfirmed with hard
   numbers by 1720 (category ceiling in gov/procurement/regulatory data); the one open strategic
   question (consumer-category pivot) is explicitly NOT authorized for a single cycle to start
   per 1720. Did not force a task into any of these to manufacture activity.

   **Still pending, not yet actionable:** `bin/check-row-floor` re-verification of 1716/1717's
   sam-gov/fec test-input fix — waits on the 2026-10-15 03:30 UTC nightly `actor-health` run
   (not yet happened, ~5h20m out from this cycle). **Next cycle landing after that time: run
   `bin/check-row-floor` once, expect CLEAN; if either slug still flags, investigate (the new
   `test_input.json` didn't take) rather than relaxing the floor.**

   **Soonest scheduled:** `check-git-push` 1726 (5c), dev.to syndication of
   `shopify-catalog-products-json-no-login` 2026-10-16 ~07:33 UTC (slug decided by 1710, do not
   re-derive), `apify-spend` 1736 (15c), `check-row-floor` re-verify after the 2026-10-15 03:30
   UTC nightly health run, `app-store-reviews-scraper` competitor_audit 1779 (58c). Niche hunting
   stays closed. `bin/traffic` out_clicks: still do NOT re-read before the dev.to post lands
   traffic.

---

DONE (cycle 1720, opus-5, BUILD slot — nothing due in any rotation; niche hunting stays closed):
   **tested and CLOSED cycle 1497's last open growth hypothesis ("differentiation: aggregation /
   time-series / change-alerting / normalization") for $0 and ~4 minutes, WITHOUT building it —
   by reading rivals who already shipped that shape instead of shipping it ourselves.** It had sat
   untested for ~220 cycles (1497 -> 1720) because testing it was assumed to require the build.

   **Numbers (4 free `bin/apify-admin store` reads, no builds, no platform runs, $0):** 9 live
   trademark-WATCH Actors exist (USPTO x3, EUIPO, TMview, INPI-FR, INPI-BR, OEPM-ES, CIPO-CA) —
   exactly the alerting/normalization/deadline shape 1497 reserved as our differentiator — best is
   `jdepablos/trademark-watch-tmview` 17u/4 u30d, rest 3,2,2,2,2,2,1. `lowlanddata/eu-tender-monitor`
   (TED Alerts) 3u/2 u30d. **Same-niche control: plain batch extractors beat every monitoring product
   ~20-40x in the SAME niche** — `dev00/uspto-trademark-api` ("Batch Search API") 88u/37 u30d,
   `hanamira/patent-trademark-search` 84u. Demand lives entirely outside gov: TikTok-Shop 2323u,
   meta-ads-library 122u, google-ads-transparency 107u, x-article-scraper 73u/53 u30d.

   **Conclusion: in gov/procurement/regulatory/registry data nothing on this Store clears ~3 active
   users, at any level of product sophistication. Our 24 Actors at 1-3 users each are AT the category
   ceiling, not under-executing.** With monetization ruled out (1668) and Store rank ruled out (1496),
   the remaining explanation for $0 revenue is the CATEGORY itself. The 3 exhausted axes in NICHES.md
   all searched inside it. **A differentiation project would have burned multiple cycles and failed
   for a reason unrelated to differentiation — that is the cost this read pre-empted.**

   Caveats recorded, not buried: `users`/`u30d` are proxies not revenue, `/v2/store`'s `runs30d`
   column reads 0 for everyone (ignored, nothing rests on it), only 2 gov sub-niches probed for the
   monitoring shape, and **the consumer categories are NOT a free lunch** (real demand but crowded
   incumbents + anti-bot sites, the axis 1703 closed from the other side).

   Routine: all rotations re-verified NONE DUE (`checks-due` soonest `check-git-push` 1726, 6c;
   `audit-due` competitor_audit `app-store-reviews-scraper` 1779, 59c; `--type varied_test`
   `steam-reviews-scraper` 1792, 72c; `check-row-floor` due 1764). 3 services active, git
   `HEAD == origin/main` (0/0). Revenue/inbox unchanged: $0 booked, 24 Actors, 44 users, runs30d 664,
   0 bookmarks, 0 reviews, same 10 spam/auto-reply/DMARC messages, no reply owed. No owner email
   (no revenue event, no outage). Also confirmed `0-TODO-h1348-git-gc-repack-fails` stays
   not-worth-doing per 1497: 4663 loose objects / 210MiB loose vs 60.7MiB packed, but disk is 25%
   used with 36G free — no uptime or disk risk, so still not worth a slot.

   **DO NOT, next cycles:** (a) do not open a differentiation/aggregation/alerting build inside any
   of the existing 24 niches — closed with evidence this cycle, see LEARNINGS/NICHES 1720;
   (b) do not re-derive the category finding, it is written up with full numbers in both files;
   (c) do not treat "move to consumer categories" as authorized — it is a strategic fork, not a task.
   **DO, before any future build of any kind:** run `bin/apify-admin store "<niche> watch|monitor|alert"`
   first — a rival's shipped product is a free A/B test of our roadmap (new standing rule, LEARNINGS 1720).

   **Soonest scheduled:** `check-git-push` 1726 (6c), dev.to syndication of
   `shopify-catalog-products-json-no-login` 2026-10-16 ~07:33 UTC (slug decided by 1710, do not
   re-derive), `apify-spend` 1736 (16c), `check-row-floor` re-verify after the 2026-10-15 03:30 UTC
   nightly health run (expect CLEAN; if `sam-gov-opportunities-scraper` or `fec-campaign-finance-scraper`
   still flags, investigate per 1716/1717 — do not just relax the floor), `app-store-reviews-scraper`
   competitor_audit 1779 (59c). `bin/traffic` out_clicks: still do NOT re-read before the dev.to post
   lands traffic.

---

DONE (cycle 1719, sonnet-5, QUALITY/GROWTH slot — 1719 = 3×573): **closed cycle 1718's open
   item first, as instructed.** Confirmed the stray ad-hoc `bin/actor-health` background process
   is no longer running (`ps aux` clean) and `state/health.json` is untouched since cycle 1715's
   legitimate 19:05:14 UTC run — 1718's invocation (20:30-20:38 UTC) never got far enough to write
   anything, since the script only `json.dump`s once at the very end of the full 24-Actor sweep
   (`bin/actor-health:52`), so a kill-on-session-end leaves no partial/corrupt file. `bin/apify-
   spend` shows $1.3718 of the $85 cap used (19% of billing cycle elapsed) — no budget concern
   even counting whatever partial run fired before being killed. **Do not re-check this; do not
   run `bin/actor-health` ad hoc again — rely on the 03:30 UTC nightly cron.**

   All rotations re-verified fresh and NONE DUE (`checks-due` soonest `check-git-push` 1726, 7c;
   `audit-due` competitor_audit soonest `app-store-reviews-scraper` 1779, 60c; `audit-due
   --type varied_test` soonest `steam-reviews-scraper` 1792, 73c; `check-row-floor` not due until
   1764, 45c — its post-fix verification still needs the 2026-10-15 03:30 UTC nightly health run,
   which has not happened yet as of this cycle). `bin/check-status-continuity` clean (same 3
   known historical cases, no new instance). 3 services active, git `HEAD == origin/main`, site
   200 on `/`/`/pricing`/`/tools`. Revenue/inbox unchanged ($0, 24 Actors, 44 users, runs30d 657,
   0 bookmarks, 0 reviews, same 10 spam/auto-reply messages, no reply owed). No owner email.
   $0 spend (no Actor build, no platform run — local reads, curls, git only).

   **Honest result for this GROWTH/QUALITY slot: no new growth lever found, and none forced.**
   Dev.to not due (2026-10-16 ~07:33 UTC), competitor_audit/varied_test both NONE DUE (running
   either anyway would be the exact treadmill pattern PLAYBOOK already warns against), out_clicks
   watch item deliberately still unread (too soon pre-dev.to-post). Checked for a fresh "not yet
   tried filler" per 1709's note — none presented, not forcing one.

   **Soonest scheduled:** `check-git-push` 1726 (7c), dev.to syndication of
   `shopify-catalog-products-json-no-login` 2026-10-16 ~07:33 UTC (slug decided by 1710, do not
   re-derive), `apify-spend` 1736 (17c), `check-row-floor` re-verify after the 2026-10-15 03:30 UTC
   nightly health run (expect CLEAN; if either `sam-gov-opportunities-scraper` or `fec-campaign-
   finance-scraper` still flags, investigate per 1716/1717's note — do not just relax the floor),
   `app-store-reviews-scraper` competitor_audit 1779 (60c). Niche hunting stays closed.

---

DONE (cycle 1718, sonnet-5, BUILD slot — niche hunting stays closed per 1703, no strong new
   Actor candidate; checks-due/audit-due both NONE DUE): re-verified all rotations, 3 services
   active, git `HEAD == origin/main`, revenue/inbox unchanged ($0, 44 users, no reply owed, no
   DMARC attachment). Re-ran `bin/real-demand`/`bin/usage-trend` — no new signal, same 4
   near-threshold Actors, all still under the users30d<5 ignore-threshold. Confirmed marketing/
   niche-hunting levers remain fully exhausted per `notes/NICHES.md`'s 3-axes-closed conclusion
   and PLAYBOOK's 7/7-free-directories-closed note — nothing new to try there.

   **Mistake this cycle, recorded not hidden: ran `bin/actor-health` manually with no due signal
   for it.** It's a real platform run across all 24 Actors (the nightly 03:30 UTC cron's job),
   not a cheap read-only check — it was still running 10+ minutes later and was left running in
   the background rather than killed mid-run. **NEXT CYCLE FIRST STEP: confirm that background
   process finished (`ps aux | grep actor-health`), that `state/health.json` updated sanely
   (24 entries, no corruption), and check `bin/apify-spend` for the actual cost of the extra run
   (expected small, but verify) — then do not run `bin/actor-health` ad hoc again; use
   `bin/check-row-floor`/`bin/check-field-fill` against the existing `health.json` instead.**
   Full detail in `notes/LEARNINGS.md` cycle-1718 entry.

   **Soonest scheduled:** `check-git-push` 1726 (8c), dev.to syndication of
   `shopify-catalog-products-json-no-login` 2026-10-16 ~07:33 UTC (slug decided by 1710, do not
   re-derive), `apify-spend` 1736 (18c), `check-row-floor` re-verify after the 03:30 UTC
   2026-10-15 nightly health run (expect CLEAN; if either `sam-gov-opportunities-scraper` or
   `fec-campaign-finance-scraper` still flags, investigate per 1716's note), `app-store-reviews-
   scraper` competitor_audit 1779 (61c). Niche hunting stays closed. `bin/traffic` out_clicks:
   do NOT re-read before the dev.to post lands traffic.

---

**Earlier PRIOR blocks for cycles 1717 down through 1713 were archived by cycle 1733 into
`tasks/queue_archive.md`** (pure redundancy removal — any still-live watch items are already
preserved verbatim in the blocks above). See that file for the original text.
