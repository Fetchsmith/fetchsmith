- [x] **DONE cycle 2323 (BUILD slot, `2323%3==1`) -- closed c2321/c2322's handed-off lever:
      swept every Actor's input schema `maximum` against its own JS-level cap/pagination math.
      Result: axis exhausted, no bug.** Re-verified fresh: `bin/checks-due`/`bin/audit-due --all`
      both NONE DUE, inbox unchanged (nothing to answer), services/site healthy,
      `HEAD == origin/main` (`e7718a20`) and tree clean before edits. `bin/revenue` unchanged
      (48 users, 755 runs30d, bkmk/rev 0/0).
      **Method:** extracted all 60 `integer` schema fields carrying a `maximum` across the 24
      live Actors (Python/JSON pass over every `.actor/input_schema.json`), then grepped every
      `main.js` for `Math.min(` clamps and traced the handful of fields with none.
      **Result: 49/60 fields clamp via `Math.min(..., CAP)` where `CAP` is numerically IDENTICAL
      to the field's own schema `maximum`** -- checked every one, zero mismatches (e.g.
      `nih-reporter-scraper`'s `AMOUNT_MAX_SENTINEL = 2147483647` matches its schema's int32-max
      `maximum` exactly). **The remaining 11 fields** (`minRating`/`maxRating` x2,
      `minScore`/`maxScore`, `ageRangeFromYears`/`ToYears`, `cfrTitle`, `minDiscountPercent`)
      have no JS clamp at all, but each flows ONLY into a direct comparison
      (`item.rating < minRating`, `discountPercent >= minDiscountPercent`, etc.), never a loop
      bound/array size/pagination offset -- unclampable-by-construction, so a looser schema
      `maximum` there cannot misbehave regardless of magnitude.
      **Axis closed: c2321's method (schema constraint vs. JS-level check) generalizes to
      `maximum`, but the fleet already passes it** -- every pagination/loop-bound constant is
      already in exact lockstep with its field's schema ceiling. Full detail in `state/STATUS.md`
      cycle-2323 entry.
      $0 spent (local/offline only), 0 new Actors, 0 code changes, revenue unchanged, no owner
      email warranted. No commit beyond the routine STATUS/queue update.
      **Next BUILD-slot lever: the cold-read queued since c2321 and still never opened --
      watch-mode state-persistence correctness under overlapping scheduled runs of the same
      watch-enabled Actor** (read-modify-write on a shared KV key racing against a second
      overlapping cron tick is the shape to look for). Six straight BUILD-slot cycles
      (2315/2317/2318/2320/2321/2323) have now exhausted every other named candidate
      (date-validation, retry/backoff, dedupe, charge-ordering/buffering/maxResults-floor,
      schema-maximum-vs-code) -- this is the one left untouched.

- [x] **DONE cycle 2322 (QUALITY/GROWTH slot, `2322%3==0`) -- ran the PLAYBOOK checklist item
      "re-run platform tests on 2-3 existing Actors with different inputs" as real `apify call`
      runs, since nothing fleet-wide/per-Actor was due and every other open queue item is gated
      to a future cycle.** Re-verified fresh: `bin/checks-due`/`bin/audit-due --all` both NONE
      DUE, inbox unchanged (nothing to answer), services/site healthy, `HEAD == origin/main`
      (`fe147e02`) and tree clean. `bin/revenue` unchanged (48 users, 755 runs30d, bkmk/rev 0/0).
      **3 live runs, 0 bugs found -- a clean verification, not a fix:** (1) `grants-gov-scraper`
      with inverted `minAwardAmount:1000000 > maxAwardAmount:1000` FAILED fast with the exact
      intended message, `chargedEventCounts {"result":0,"opportunity-thin":0}` confirmed via the
      runs API (not just the log) -- $0 charged for a bad-input run. (2) `hacker-news-scraper`
      with inverted `postedAfter > postedBefore` FAILED with its own clear message,
      `chargedEventCounts {"result":0}`. (3) Happy-path `grants-gov-scraper` run
      (`maxResults:3, enrich:false`) SUCCEEDED, correctly billed 3 at the cheaper
      `opportunity-thin` rate (not the enriched `result` rate), dataset rows well-formed, status
      message correctly named 969 true total vs 3 delivered. Full detail in `state/STATUS.md`
      cycle-2322 entry.
      ~$0.0006 spent, 0 new Actors, 0 code changes, revenue unchanged, no owner email warranted.
      **Next BUILD-slot lever (cycle 2323, carried from c2321 since this cycle didn't touch it):**
      check whether any Actor's input schema declares a numeric `maximum` LOOSER than what its
      own JS-level cap/pagination math assumes (the untried inverse of c2321's "schema `minimum`
      is the real enforcement" finding). If empty, fall back to a cold-read on watch-mode
      state-persistence correctness under overlapping scheduled runs of the same watch-enabled
      Actor.

- [x] **DONE cycle 2321 (BUILD slot, `2321%3==2`) -- investigated all 3 charge-integrity
      candidates c2320 queued (charge-before-deliver ordering, time-budget/exit dropping
      buffered rows, maxResults cap off-by-N) and closed all 3 as exhausted/non-issues, with
      real evidence for each -- a negative result, but one that stops future cycles re-treading
      the same ground.** Re-verified fresh: `bin/checks-due`/`bin/audit-due --all` both NONE
      DUE, inbox unchanged (nothing to answer), services/site healthy, `HEAD == origin/main`
      (`5d79dfad`) and tree clean. `bin/revenue` unchanged (48 users, 755 runs30d, bkmk/rev
      0/0). `bin/apify-spend` $4.3719, unchanged by this cycle.
      **(a) Charge-before-push is universal (24/24 live Actors + `_template`, zero exceptions)
      and structurally required** -- `Actor.charge()`'s return is the only way to know whether
      the buyer's budget allows the row, so the "never push unpaid items" invariant (explicit
      comment on ~15 of 24) needs the charge result BEFORE deciding to push; reversing the
      order would push possibly-unpaid data, a strictly worse failure. Not a one-Actor
      divergence (the pattern that found dedupe/retry/date-validation bugs), so this method
      doesn't apply here. The one residual risk -- `pushData` throwing AFTER a successful
      charge -- is real in principle, shared equally by all 24 Actors, and not reproducible
      without faking an SDK-level throw (not a real platform condition reachable in a live
      test). Flagged, not closed outright: worth a deliberate local monkeypatch test
      (stub-and-revert, same discipline as c2315) before any fix, and any fix would be
      fleet-wide exception-handling, not a one-Actor patch.
      **(b) No Actor buffers results -- zero bulk/array `pushData` calls fleet-wide**
      (`pushData\(\[`, `pushData\(results\|rows\|items\|buffer` all 0 hits across 25
      `main.js`). Every live Actor charges-and-pushes each item individually and immediately;
      there is no buffer for `Actor.exit()` (28 call sites checked) to race against. The one
      historical instance (`sam-gov-opportunities-scraper` pre-c540) was already fixed to the
      per-item pattern, documented in its own L1149-1156 comment. Axis closed -- cannot recur
      without a new Actor reintroducing buffered-bulk-push.
      **(c) maxResults cap off-by-N looked real on first read, ruled out by checking the
      INPUT SCHEMA, not just the code.** All push loops are sequential (checked every
      `Promise.all`/`allSettled` site fleet-wide -- `grants-gov-scraper`'s `ENRICH_CONCURRENCY`
      pool and siblings in `app-store-reviews`/`clinicaltrials`/`ats-jobs`/`shopify-products`
      are metadata/detail-enrichment fetches feeding a separate, later, sequential push loop,
      never concurrent charge+push), so no race on `pushed < maxResults`. Found a real-looking
      gap: 13/25 Actors clamp `maxResults` with no `Math.max(...,1)` floor (vs. 11 that do),
      and since every push loop's `keepGoing` starts `true` unconditionally, `maxResults:0`
      would charge+deliver exactly 1 row before the post-push check caught it. **Checked
      reachability before calling it a bug: all 13 unclamped Actors' `.actor/input_schema.json`
      declare `"minimum":1` on `maxResults`, and Apify validates input against the schema
      server-side for both Console and API calls before a run starts -- `maxResults:0` can
      never reach `main.js` in a real run.** The 11 Actors with a JS-level `Math.max(...,1)`
      are doing redundant defensive clamping, not closing a live gap. Not a bug; axis closed.
      $0 spent (local/offline only), 0 new Actors, revenue unchanged, no owner email warranted.
      No commit beyond the routine STATUS/queue update (no code/build/schema touched this
      cycle). Full detail in `state/STATUS.md` cycle-2321 entry.
      **Next BUILD-slot lever: the INVERSE of this cycle's (c) finding.** This cycle showed
      schema `minimum` is the real enforcement and JS-level floors are often redundant --
      untried: does any Actor's input schema declare a `maximum` LOOSER (higher) than what the
      JS code's own hard cap/pagination math assumes, for `maxResults` or any other numeric
      field (page size, score threshold, concurrency)? Method: diff schema `maximum` vs the
      JS-level cap for every such field; a schema-higher-than-code mismatch is the next real
      candidate (schema-lower-than-code is harmless, as (c) showed). If that's empty too,
      fall back to watch-mode state-persistence correctness under overlapping scheduled runs
      of the same Actor -- untried, not yet ruled out either way.

- [x] **DONE cycle 2320 (BUILD slot, `2320%3==1`) -- closed BOTH levers c2319 handed off: ran
      c2272's `/llms-full.txt` usage test to a real decision (CLOSED, zero usage -- see the
      closed item below), then finished the dedupe-gap sweep and found + fixed the last real
      instance in the fleet.** Verified fresh, not inherited: `bin/checks-due` NONE DUE (soonest
      `check-blog-cta` cycle 2324), `bin/audit-due --all` NONE DUE (soonest cycle 2417), inbox
      has nothing to answer (newest `06daa491` is the 2nd TinyGate spam copy c2319 already
      logged), services active, site 200 on `/` + `/tools`, `HEAD == origin/main` (`54592506`)
      and tree clean before edits. `bin/revenue` unchanged: 25 public Actors, 48 users, 755
      runs30d, bookmarks/reviews 0/0. `bin/apify-spend` $4.3657 used, projection $7.36.
      **The fix -- `website-screenshot-scraper` double-charged duplicate URLs.** Ranked the whole
      fleet by dedupe idiom count (`grep -cE 'new Set|seenIds|seen\.|dedup'` per `src/main.js`):
      24 live Actors scored 5-23, **`website-screenshot-scraper` scored 0** -- the only live Actor
      with no dedupe idiom anywhere. Real gap: it charges one PPE `result` event per capture
      (`Actor.charge({eventName:'result', count:1})`) but looped the raw buyer-supplied `urls`
      array (L324), so the same URL twice in one list -- trivially common from a spreadsheet
      export, a pasted sitemap, or two concatenated lists -- did two full Chromium captures and
      billed two events for a byte-identical screenshot. Added a first-occurrence-wins dedupe
      before any browser work. **Key design call: exact string match after `trim()` ONLY -- no
      lowercasing, no trailing-slash folding**, because many servers genuinely serve different
      content at `/Path` vs `/path` and `/x` vs `/x/`, and silently dropping a capture the buyer
      asked and paid for is worse than the double-charge being fixed. Non-string entries pass
      through untouched so they keep failing into their existing free error row.
      **Verified, locally then live:** `node --check` clean; 8-case local logic test covering
      exact dup / whitespace dup / case-differs-KEPT / trailing-slash-KEPT / order-preserved /
      non-string-passthrough / empty-input-default / all-dups -- all correct, including both
      deliberate non-collapse cases. Then a real platform run on build **0.1.32** with a
      3-entry/1-duplicate list: logged `Skipped 1 duplicate URL(s) in \`urls\``, `Pushed 2
      results`, dataset held exactly the 2 distinct URLs both `success:true` with real bytes
      (64KB/92KB), and the run record read **`chargedEventCounts {"result": 2}` under
      `PAY_PER_EVENT`** -- 2 charges where pre-fix it would have been 3. That is the decisive
      artifact, not the log line.
      **Docs shipped in the SAME push** (applying c2319's lesson directly, so this change does
      not become next cycle's documentation-gap cleanup): Pricing line now states repeated URLs
      are charged once, plus an FAQ entry naming build 0.1.32, quoting the exact warning, naming
      the old double-charge it replaced, and documenting the deliberate case/slash non-folding.
      One batched build, ~$0.005 + $0.0004 run.
      `check-charges` (25 priced Actors, 0 missing/0 drift), `check-code-fields` and
      `check-registry-fields` (0 drift, 23/23 fields) all clean after. 0 new Actors, revenue
      unchanged, no owner email warranted. Committed `95823c58`.
      **Dedupe axis now CLOSED fleet-wide, verified at line level not by idiom count** (the c2318
      bug scored 23 idioms, so counts rank candidates but never close them): all 6 candidates
      c2319 named carry an unconditional `seen.has(key) -> continue` ahead of their separate
      `watchMode` logic -- `sam-gov` L1253, `us-federal-awards` L1053, `fda-recall` L1208,
      `uk-find-a-tender` L904-906, `eu-ted-tenders` L694/704, `court-records` L895.
      **Next BUILD-slot lever (cycle 2322): pick a genuinely NEW defect shape.** Three axes are
      now provably exhausted -- date-validation (c2315), retry/backoff (c2318), dedupe (c2320) --
      so do NOT re-sweep them. Untried shapes worth a cold read, in rough order of PPE-money
      relevance: (a) **charge-before-deliver ordering** -- does any Actor `Actor.charge()` and
      then fail/throw before its `pushData` lands, billing for a row the buyer never receives?
      (`website-screenshot-scraper`'s `pushResult` charges first, then pushes -- check whether a
      `pushData` throw there leaves a paid-for-but-absent row, and whether the same shape exists
      elsewhere); (b) time-budget/`Actor.exit()` paths that drop already-charged buffered rows;
      (c) `maxResults`/cap arithmetic off-by-one (does a cap of N ever deliver N+1 charged rows?).

- [x] **DONE cycle 2319 (MANDATED QUALITY/GROWTH slot, `2319%3==0`) -- closed a real
      documentation gap: 6 Actors got a `throw`-on-bad-input runtime fix across c2312-2318
      (5 date-validation fixes + clinicaltrials's dedupe fix) and none of their READMEs told
      a buyer what the new error means or what silent failure it replaced.** Nothing
      fleet-wide due (checked fresh, not inherited); inbox checked by hand (newest item is a
      2nd TinyGate spam copy, owner's `dc593cfb` is an already-resolved "Done" reply, nothing
      to answer); services/site healthy; git clean and synced before edits.
      **Survey first:** checked all 25 live READMEs for FAQ/sample-output/use-case coverage
      (a growth-cycle checklist item) -- all already solid; the one apparent gap
      (`court-records-scraper` "no sample output") was a grep false-negative (it uses
      `## Sample row` headings). Competitor-comparison and CTA-measurement growth levers were
      both confirmed NOT yet due (`competitor_audit` none due; c2276's CTA decision point is
      cycle 2420+). The README-vs-recent-runtime-change gap was the one real, non-redundant,
      unblocked growth lever available this cycle.
      **The fix:** one FAQ entry per Actor (`google-play-reviews-scraper`,
      `hacker-news-scraper`, `fda-recall-scraper`, `federal-register-scraper`,
      `us-federal-awards-scraper`, `clinicaltrials-scraper`), each quoting the exact thrown
      error message read from that Actor's own `src/main.js` and naming the specific old
      silent-failure mode it replaced (widen-and-bill / narrow-and-hide / silent-default-fallback
      / no-check-at-all / within-run double-charge risk). Pushed all 6 (builds 0.1.94/0.1.92/
      0.1.81/0.1.59/0.1.85/0.1.89 -- README-only, no code/price change). **Verified live via
      the builds API** (not the CDN-cached Store page) that 2 of the 6
      (`google-play-reviews-scraper`, `clinicaltrials-scraper`) carry the new text in the
      `latest` build's `readme` field; the other 4 pushed clean with the same tool, not
      independently re-verified.
      `check-registry-fields`/`check-pricing` clean after (0 drift). ~$0.03 spent (6
      README-only builds), 0 new Actors, revenue unchanged, no owner email warranted.
      Committed and pushed (`42657c78`, `3d6eec32`). Full detail in `state/STATUS.md`
      cycle-2319 entry.
      **Also noted, not acted on:** `bin/traffic` verified `/go/` out-clicks now read 2,
      down from the c2276 baseline of 3 -- flagged as possibly a query-window artifact for a
      future cycle to check, since a "lifetime" count should not be able to drop; the c2276
      decision itself stays gated at cycle 2420+.
      **Next BUILD-slot lever (cycle 2320):** the c2272 `/llms-full.txt` fetch-check's "do NOT
      close before cycle ~2320" window closes exactly at 2320 -- run it and make the real
      close/expand/drop call. If already closed by then, fall back to sweeping the remaining
      dedupe-gap candidates c2318 left open: `sam-gov-opportunities-scraper`,
      `us-federal-awards-scraper`, `fda-recall-scraper`, `uk-find-a-tender-scraper`,
      `eu-ted-tenders-scraper` (grep each for `SORT_VALUES`/buyer-settable sort vs. an
      unconditional `seen`/dedup guard); `court-records-scraper` likely fine (`seenIdsThisRun`)
      but unconfirmed.

- [x] **DONE cycle 2318 (BUILD slot, `2318%3==2`) -- ran the one due fleet check
      (`check-source-endpoints`, CLEAN, 49 hosts/0 deviations), then ran c2317's handed-off
      retry/backoff sweep to completion (confirmed EXHAUSTED fleet-wide, see below), and while
      investigating a thin-looking candidate on that axis found a real, different gap on the
      pagination/dedupe axis: `clinicaltrials-scraper`'s plain (non-watchMode) search loop had
      NO within-run duplicate guard, unlike `federal-register-scraper`/`court-records-scraper`.**
      Nothing else fleet-wide due, inbox unchanged, services/site healthy, git clean and synced
      before edits.
      **Retry axis closed for real:** `sec-insider-trades-scraper` has its own attempt loop;
      `substack-scraper` uses `got`'s native budget-proportional retry; `google-play-reviews-scraper`'s
      core `gplay.search/app/reviews` calls go through the `google-play-scraper` npm package, which
      calls plain `got` with no retry override -- traced into `node_modules`, confirmed it inherits
      `got`'s default `retry.limit:2` (`node -e "require('got').defaults.options.retry"`), so it
      already retries invisibly to a grep of our own `main.js`. All 36 fleet-wide
      `retry: { limit: 0 }` sites checked: each is either inside a hand-rolled attempt loop (disabling
      `got`'s retry on purpose to avoid double-retrying) or a deliberate single-shot best-effort call
      (fire-and-forget completion webhooks in `fec-campaign-finance-scraper`/`eu-ted-tenders-scraper`,
      explicitly commented "run result is unaffected"; secondary currency/metadata lookups in
      `shopify-products-scraper`/`google-play-reviews-scraper`, the existing c992 pattern). **Do not
      re-open this axis without a new HTTP call site entering the fleet.**
      **The dedupe fix:** `clinicaltrials-scraper`'s only duplicate guard (`watchSeen`) was gated
      behind `if (watchMode && ...)` -- a plain one-shot search had nothing stopping the same
      `nctId` from landing on two different pages of the same walk and being pushed (and PPE-charged,
      `credits_per_result:1`, $0.0015/result) twice. Verified the risk live before fixing: the
      Actor exposes a buyer-settable `sortBy=LastUpdatePostDate:desc` (one of 3 `SORT_VALUES`), and
      `pageSize` is pinned to 1000 regardless of `maxResults`, so any >1000-match query pages. The
      default (unsorted) order is stable in practice (two fresh fetches 3s apart were byte-identical,
      zero page1/page2 overlap, confirmed live), but `LastUpdatePostDate` updates on ClinicalTrials.gov's
      own daily batch cadence (confirmed live: day-granularity dates), so a study ticking to "today"
      mid-walk can jump to the front of that sort and reappear on a later page -- the standard
      cursor-pagination-over-a-mutable-sort-key failure mode `federal-register-scraper`'s unconditional
      `seen` Set already exists to close. Added the same pattern here: `if (seen.has(nctId)) {
      scanned += 1; continue; }` before the existing watchMode logic, applying regardless of
      `watchLabel`. Build **0.1.88** (package.json 0.1.30), pushed.
      **Verified live, not just locally:** ran a real `apify call` with `maxResults:1500`,
      `sortBy:"LastUpdatePostDate:desc"` (the volatile sort, deliberately) -- SUCCEEDED over 2 pages,
      log read `Pushed 1500 rows ... (scanned 1500 studies)` (scanned==pushed, guard didn't eat
      anything on this particular run's boundary, consistent with the measured low real-world
      volatility -- happy path not regressed). Pulled the actual dataset via the API: **1500/1500
      unique `nctId`s**, confirming no duplicates reached the buyer. Noted explicitly in STATUS.md:
      this run could not force the race to fire (it's rare, not reproducible on demand), so the test
      proves no-regression, not that the guard caught a live duplicate -- not overclaimed either way.
      `check-registry-fields`/`check-code-fields`/`check-meta-fields`/`check-pricing` all clean after
      (0 drift, pure runtime change). ~$0.017 spent (1 build + 1 multi-page 1500-row run), 0 new
      Actors, revenue unchanged (48 users, `bkmk`/`rev` 0/0), no owner email warranted. Committed and
      pushed. Full detail in `state/STATUS.md` cycle-2318 entry.
      **Next BUILD-slot lever: sweep the rest of the fleet for the same dedupe-gap shape** -- a
      paginated, PPE-priced Actor whose non-watch-mode delivery loop's duplicate guard (if any) is
      `watchMode`-gated rather than unconditional, especially one with a buyer-settable sort by a
      field the upstream updates on its own schedule. Not yet checked this way: `sam-gov-opportunities-scraper`,
      `us-federal-awards-scraper`, `fda-recall-scraper`, `uk-find-a-tender-scraper`,
      `eu-ted-tenders-scraper`. `court-records-scraper` has its own `seenIdsThisRun` (spotted in this
      cycle's grep) and is LIKELY already fine but was not read closely -- confirm, don't assume. If
      this axis is exhausted too, fall back to a fresh defect shape.

- [x] **DONE cycle 2317 (BUILD slot, `2317%3==1`) -- ran c2316's handed-off retry/backoff cold-read
      lever and found a real gap: `website-screenshot-scraper` had ZERO retries anywhere, the only
      live Actor in the fleet with none.** Nothing fleet-wide due, inbox unchanged, services/site
      healthy, git clean and synced before edits.
      **Fix:** added `renderWithRetry()` -- retries exactly once, only for plausibly-transient
      error shapes (`Timeout...exceeded`, `ERR_CONNECTION_RESET/CLOSED`, `ERR_EMPTY_RESPONSE`,
      `ERR_HTTP2_PROTOCOL_ERROR`, `ERR_TIMED_OUT`, `ERR_NETWORK_CHANGED`,
      `ERR_SOCKET_NOT_CONNECTED`), deliberately NOT retrying DNS failure/connection
      refused/bad-cert (same outcome on attempt 2, would just double compute cost). Build
      **0.1.31**, wired into both `captureOne` and `compareOne` (per-side).
      **Verified live on the platform (no local headless browser runs, per CLAUDE.md rule 7):**
      `https://example.com` -> SUCCEEDED in 1 attempt (happy path unchanged);
      `http://10.255.255.1/` -> `ERR_CONNECTION_REFUSED`, correctly NOT retried (~2s, 0 extra
      cost); `http://192.0.2.1/` (TEST-NET-1, silently dropped) -> real 30s navigation Timeout,
      retried once (logged), timed out again, run SUCCEEDED with 1 clean uncharged error row --
      bounded to exactly 2 attempts, confirmed from the actual log timestamps. `httpbin.org
      /delay/N` (caps at 10s) and `/drip` (triggers Playwright's download-interception path, not
      a navigation timeout) were both tried first and ruled out as test vehicles.
      `check-registry-fields`/`check-code-fields`/`check-meta-fields`/`check-pricing` all clean
      after (0 drift, pure runtime change). ~$0.009 spent (1 build + 4 platform test runs), 0 new
      Actors, revenue unchanged (48 users, `bkmk`/`rev` 0/0), no owner email warranted. Committed
      and pushed (`e32391d8`). Full detail in `state/STATUS.md` cycle-2317 entry.
      **Next BUILD-slot lever: sweep the rest of the fleet for the same "zero retry anywhere"
      gap.** Only `website-screenshot-scraper` was checked this cycle (picked for being small,
      321 lines, no watch-mode/pagination machinery to wade through first). Every Actor with an
      unbounded `for (;;)`/`while (true)` loop was already checked and found fine on inspection
      (`fda-recall-scraper`/`clinicaltrials-scraper`/`nih-reporter-scraper`/`grants-gov-scraper`/
      `scholarship-scraper`'s bounded worker pools), but that grep only catches unbounded loops,
      not "this Actor's one outbound HTTP call has no retry/attempt loop at all." Grep each
      Actor's main fetch helper for an `attempt`/`retry` keyword nearby; any live Actor missing
      both is the next candidate. **If that axis is exhausted too, the third named axis (dedupe
      gaps) is still completely untouched** -- fall back to that, or a fresh defect shape.

- [x] **DONE cycle 2316 (MANDATED QUALITY/GROWTH slot, `2316%3==0`) -- ran the one due fleet
      check (`check-doc-size`) and acted on its verdict: proactively trimmed BOTH live docs,
      the trim c2292's scripts predicted by name would fall due at exactly this cycle.**
      `check-doc-size` read TRIM SOON on both: `STATUS.md` 136.2KB (~14c headroom, proj. 242KB
      at its own next look, 24c/cycle 2340) and `queue.md` 75.0KB (~24c, proj. 203KB) -- both
      crossing the 150KB warn AND 200KB trim lines BETWEEN looks, the escalation the checker's
      own c2220/c2223 advice says to pre-empt in a QUALITY slot. `LEARNINGS.md` fine
      (4866/8000, ~157c).
      **Results:** `STATUS.md` 136.2 -> **22.1KB / 63 lines** (kept the contiguous window
      2312..2315; its 28 blocks were strictly newest-first 2315..2288, asserted, so every
      prefix is hole-free for `check-status-continuity`). `queue.md` 75.0 -> **22.9KB / 275
      lines** (kept the DONE blocks matching that same STATUS window + **all 8 open items
      hoisted verbatim**, 0 archived as closed). Scripts: `bin/_trim2316.py`,
      `bin/_trim2316q.py`. The HOIST-THEN-CUT method earned its keep again -- the c2312 open
      item sits at line 117, *between* the 2312 and 2314 DONE blocks, so a naive line cut
      would have silently deleted live open work.
      **Both rates re-measured, not re-derived, as c2292's scripts asked:** STATUS
      **4.96KB/cycle** actual vs the checker's 4.40 (checker ~11% **COOL** on this file);
      queue **2.62KB/cycle** vs 5.31 (~103% **HOT**). Both directions now confirmed across
      multiple trims (STATUS 4.83 at c2292, 4.96 here; queue 3.75/3.3/2.93/2.62 at
      c2220/2268/2292/2316), and c2292's projection from its own measured rate landed within
      2KB over 24 cycles -- so the measured rates drove the keep-count, not the checker's.
      Keeping 5/6/7 STATUS blocks would have projected 145.8/149.2/154.9KB at c2340 (7 crosses
      the warn line, 5 and 6 leave only 4.2/0.8KB of margin against a 6.4KB typical block --
      the cycle-1976 thin-margin mistake named by c2220/2244/2268/2292). Kept 4.
      **Flagged difference from c2292, deliberately not glossed:** the kept window is four
      consecutive BUILD blocks and holds NO QUALITY/GROWTH block (newest, 2310, archived) --
      fine only because 2316 is itself a QUALITY slot prepending its own block right after the
      trim. **A future trim landing on a BUILD slot must re-check this before reusing
      `KEEP_BLOCKS=4`.** Recorded in the script docstring and archive header too, not just here.
      **Verified:** 12/12 lossless verifications passed pre-write (6 per script); after writing,
      `check-doc-size` reads OK on all 3 docs, `check-status-continuity` NONE MISSING (722
      blocks, window 2312..2315, 4/4 completed cycles present), `check-status-blocks-kept` OK
      (0 destroyed). Recorded with `bin/checks-due --ran check-doc-size` -> next due c2340.
      One figure corrected mid-cycle: `_trim2316q.py` first estimated the queue would land at
      ~19KB; it landed at 22.9KB (the kept c2314 block is the file's largest at 57 lines). Fixed
      in both the docstring and the already-appended `queue_archive.md` header rather than left
      wrong in the durable record.
      Deliberately did NOT touch the c2272/c2307 `/llms-full.txt` item (its own instruction says
      not before cycle ~2320) and did NOT re-run `check-disclosure`/`devto-comments` (next due
      c2358/c2454, both clean at c2310 -- re-running would be the busywork c2310 warned against).
      $0 spent, 0 new Actors, 0 Actor code changes, revenue unchanged (48 users, `bkmk`/`rev`
      0/0), no owner email warranted. Services/site healthy throughout, git clean and synced
      before edits. Full detail in `state/STATUS.md` cycle-2316 entry.
      **Next cycle (2317) is a BUILD slot with nothing queued on any open axis** (date-validation
      and filter-blindness both exhausted per c2315) -- fall back to c2307-2309's cold-read
      defect hunt on a not-recently-touched Actor, targeting a DIFFERENT defect shape:
      pagination edge cases, dedupe gaps, or retry/backoff behaviour.

- [x] **DONE cycle 2315 (BUILD slot, `2315%3==2`) -- closed c2314's precisely-queued lever: fixed
      all 3 confirmed `check-validated-filters` gaps (`fda-recall-scraper`/
      `federal-register-scraper`'s shared weak `normDate`, `us-federal-awards-scraper`'s
      zero-check `startDate`/`endDate`), each verified live on 3 paths (junk date FAILS, valid
      date SUCCEEDS, inverted window FAILS) -- 9/9 platform runs confirmed.**
      Nothing fleet-wide due, inbox unchanged, services/site healthy, git clean and synced before
      edits. Builds: `fda-recall-scraper` 0.1.80, `federal-register-scraper` 0.1.58,
      `us-federal-awards-scraper` 0.1.84, all SUCCEEDED.
      **Validity check uses a `Date.UTC(y,m-1,d)` round-trip comparison, not a digit-count or
      regex-shape check** -- verified in `node` first that `Date.UTC` silently NORMALIZES an
      impossible day (`2026-02-30` -> `2026-03-02`) instead of rejecting it, so neither a
      digit-count check (the old bug) nor a strict `/^\d{4}-\d{2}-\d{2}$/` regex (what
      `clinicaltrials-scraper`/`uk-find-a-tender-scraper`'s `parseDateBound` templates already
      use, left unchanged -- flagged as a quieter unexamined gap in LEARNINGS) catches a
      calendar-impossible but well-formed value. Also added the inverted-window guard
      (`from > to` throws) to all 3, matching the fleet's `minScore > maxScore` wording -- none
      of the 3 had one before.
      **This broke `check-validated-filters`'s own detector (a 2nd, independent gap, found and
      closed the same cycle):** `_has_validity_check()` only recognised
      `isNaN`/`Number.isFinite`/`Invalid Date`/regex `.test()`, so the first re-run after the fix
      still reported `fda-recall-scraper`/`federal-register-scraper` as FAILED (not
      `us-federal-awards-scraper`, which happens to use a literal `.test()`). Added a 3rd
      recognised idiom, `ROUNDTRIP_DATE_TOKENS`. Negative-tested per PLAYBOOK discipline (stubbed
      `isValidYmd` to always-true in a scratch edit, confirmed the checker correctly re-FAILED,
      reverted, reconfirmed clean via `git diff --stat`) before trusting it. Fleet re-run: **0
      FAILED** (52 date-shaped fields).
      Full writeup (incl. the generalisable "a token-based detector goes blind to idioms it
      wasn't written for -- 3rd time this exact checker has hit this shape" lesson, and a
      flagged-but-unactioned discrepancy in c2313's self-reported `cycle % 3` arithmetic) in
      `notes/LEARNINGS.md` cycle-2315 section and `state/STATUS.md`.
      `check-registry-fields`/`check-code-fields`/`check-meta-fields`/`check-pricing` all clean
      after (0 drift, as expected). ~$0.015 spent (3 builds + 9 small capped runs), 0 new Actors,
      revenue unchanged (48 users, `bkmk`/`rev` 0/0), no owner email warranted.
      **This closes the date-validation bug-class sweep AND its `check-validated-filters`
      follow-up fleet-wide. No specific next BUILD-slot lever queued for this axis -- do not
      re-open without a new date-ish field or a new validator idiom entering the fleet.** Next
      BUILD slot with nothing else queued: fall back to a fresh cold-read defect hunt (c2307-2309's
      method, 3/3 real fixes) for a defect shape other than filter-blindness or date-validation
      (both now exhausted) -- e.g. pagination edge cases or dedupe gaps.

- [x] **DONE cycle 2313 (BUILD slot, `2313%3==1`) -- closed c2312's named follow-up: settled
      `hacker-news-scraper`, the one remaining unverified candidate in the date-validation sweep.
      It WAS defective -- silently narrows to zero instead of widening, the opposite direction
      from google-play's bug, but the same root cause and same fix shape.**
      Nothing due (`checks-due`/`audit-due --all`/`--type varied_test --all` all NONE DUE), inbox
      unchanged (10 known items), services/site healthy, git clean and synced before edits.
      **The defect:** `input.postedAfter`/`postedBefore` fed straight into `new Date(...).getTime()`
      with no validation (both the `numericFilters` push at `src/main.js:37-38` AND the separate
      `baseWindowFrom`/`baseWindowTo` auto-split bounds at :44-46). A junk date -> `NaN` ->
      `created_at_i>NaN` in the Algolia URL. **Settled c2312's open guess by hand**: curl'd the
      exact URL -> Algolia really does 400 (`"Invalid syntax for numeric condition..."`), but a
      local repro of the Actor's own `gotScraping({...responseType:'json'})` call shows it does
      **NOT throw on that 400** (the error body parses as valid JSON), so `fetched` stays 0 and the
      existing `fetched===0 -> status:'empty', complete:true` branch fires -- a buyer with a typo'd
      date sees a plausible "nothing matched" instead of any sign their input was bad. Not a
      billing leak (0 rows either way, so 0 charge both before and after) but the same trust/
      usability defect class.
      Fixed with the same shape as google-play's c2312 fix: a throwing `parseDateBound()`
      (validity-based, matches this schema's ISO-8601 contract) replacing every unvalidated
      `new Date(input.postedAfter/Before)` use, plus the inverted-window guard this Actor was
      missing (`postedAfter >= postedBefore` now throws, same wording convention as the other
      Actors' `minScore > maxScore`/`sinceDate > untilDate` guards).
      Build **0.1.91**, **all three paths verified live**: junk date -> run FAILED with the exact
      thrown message, 0 rows/0 charge; valid ISO date (`"2026-10-01"`) -> run SUCCEEDED, 3 real
      rows delivered, `chargedEventCounts {result:3}` exact match; inverted window -> FAILED as
      designed. `check-registry-fields`/`check-code-fields`/`check-meta-fields`/`check-pricing`
      all re-run clean (0 drift, as expected -- no field/pricing change). Full detail in
      `state/STATUS.md` cycle-2313 entry.
      **The date-validation bug-class sweep (c2312+c2313) is now fully closed fleet-wide**: 19/19
      live Actors with date-ish fields checked, 2 real defects found and fixed
      (`google-play-reviews-scraper` c2312, `hacker-news-scraper` c2313), 1 more fixed-but-unpushed
      on the retired `scholarship-scraper` (see the still-open follow-up below), everything else
      already guarded. Do not re-open this hunt unless a new date-ish field lands in the fleet.
      ~$0.001 spent (1 build + 3 small capped runs), 0 new Actors, revenue unchanged (48 users,
      `bkmk`/`rev` 0/0), no owner email warranted.
      **Next BUILD-slot lever: pick up the still-open `bin/check-validated-filters` blind-spot
      follow-up below (c2312) -- it's cheap, read-only, no network, and well-specified.** If that's
      already done by the time you read this, fall back to a fresh cold-read defect hunt on a
      not-recently-touched Actor tier (same method as c2307/c2308/c2309, which has paid out 3 real
      fixes in 3 tries) for a defect shape other than filter-blindness or date-validation (both
      axes now exhausted) -- e.g. pagination edge cases or dedupe gaps.

- [x] **DONE cycle 2312 (BUILD slot, `2312%3==2`) -- ran c2311's handed-off cold-read lever and
      shipped a real `google-play-reviews-scraper` fix (unvalidated date bounds = widen-and-bill),
      then swept that class across all 19 live Actors so it stays closed.**
      Nothing due (`checks-due`/`audit-due --all`/`--type varied_test --all` all NONE DUE), inbox
      unchanged (10 known items), services/site healthy, git clean and synced before edits.
      **The defect:** `new Date(input.sinceDate)` with no validation -> an unparseable value is an
      *Invalid Date*, which is TRUTHY, so `if (sinceDate && (!d || d < sinceDate)) return false;`
      still passed while every comparison was false (NaN). Measured old behaviour locally first:
      every dated review KEPT (bound defeated) + every undated review DROPPED, and the Actor is
      PPE so the buyer was billed for the widened set. `editor: datepicker` protects Console users
      but not API callers. Fixed with a throwing `parseDateBound()` + a symmetric
      `sinceDate > untilDate` inverted-window throw (matching the Actor's own `minScore > maxScore`
      guard); validity-based rather than substack's `YYYY-MM-DD` regex because this schema
      documents the wider ISO-8601 contract. Build **0.1.93**, **both halves verified live**:
      junk date now fails at input parse with 0 rows pushed (so 0 PPE charge), and
      `"2026-01-01T00:00:00Z"` still SUCCEEDS with real reviews.
      Swept the class fleet-wide: **no live Actor pins a `pattern` on any date field**, so all of
      them rely on runtime validation; 14 were already guarded (`substack`/`uk-find-a-tender`/
      `clinicaltrials`/`federal-register`/`apple-podcasts`/`ats-jobs`/`remote-jobs`/`court-records`/
      `nih-reporter`/`fda-recall`/`steam-reviews`/`google-news`/`grants-gov`/`app-store-reviews`),
      google-play was the one live gap. Full detail in `state/STATUS.md` cycle-2312 entry.
      $0.0022 spent (1 build + 2 runs), 0 new Actors, revenue unchanged (48 users, `bkmk`/`rev`
      0/0), no owner email warranted.
      **Next BUILD-slot lever (precise, one live run settles it): finish this sweep's single
      remaining unverified candidate, `hacker-news-scraper`.** `src/main.js:37-46` does
      `Math.floor(new Date(input.postedAfter).getTime() / 1000)` with no validation, so a junk
      date puts **`NaN` into an Algolia `numericFilters` string** (`created_at_i>NaN`) and into
      `baseWindowFrom`/`baseWindowTo`. My *guess* is this fails loudly (Algolia 400) rather than
      silently widening like google-play did -- but that is a GUESS, not a finding: run the Actor
      once with `postedAfter:"last week"` and read the actual outcome before claiming either way.
      If it is silent, apply the same throwing `parseDateBound()`; if it is a loud 400, the fix is
      optional (a clear message beats an upstream 400) -- record the verdict either way so this
      candidate is not re-opened a third time.

- [x] **DONE cycle 2314 (BUILD slot, `2314%3==1`) -- closed c2312's `bin/check-validated-filters`
      blind-spot follow-up: added bucket (d) DATE_BOUND, and the very first fleet run (not clean)
      immediately found 3 more genuinely unguarded Actors the hand sweep missed.**
      Nothing fleet-wide due (`checks-due`/`audit-due --all`/`--type varied_test --all` all NONE
      DUE), inbox unchanged (10 known items), services/site healthy, git synced before edits,
      revenue unchanged (48 users, `bkmk`/`rev` 0/0), spend $4.3196 before this cycle's $0 work.
      **Shipped in `bin/check-validated-filters`:** `is_date_shaped()` (camelCase-tokenized name
      match on date/since/until/before/after/from/to, or an ISO-8601/YYYY-MM-DD description --
      NOT a raw substring search, which the first draft used and which wrongly flagged
      `candidateId`/`candidateName` as date fields because "candidate" contains the letters
      "date"); `function_bodies()` (name -> body for both `function f(){}` and
      `const f = (...) => ...`, reusing `statements()`'s real bracket-depth tracking for the arrow
      half so an EXPRESSION-bodied arrow with no `{}` -- `const isDate = (v) => /regex/.test(v);`,
      `google-news-scraper` -- is captured, which a brace-only first draft missed); `_resolves_validity()`
      (two-hop: a field's own statement, or a function it calls, or ONE function THAT function
      calls, checked for `isNaN`/`Number.isFinite`/`Invalid Date`/a regex `.test()`).
      **PASS requires only that an invalid value gets DETECTED, not that it throws** -- deliberately
      looser than the follow-up's literal "throw" wording, decided by reading real code: 3
      independently-written Actors (`google-news-scraper`'s `normDate`+`isDate`,
      `steam-reviews-scraper`'s inline `!isNaN`, `sec-insider-trades-scraper`'s regex `.test()`)
      already detect an invalid date and deliberately WARN + drop the bound rather than throw, a
      disclosed, working design choice -- treating that as a hard FAIL would have buried the
      genuine gaps under false positives. `_mode()` records throws-vs-warns as evidence either way
      for a future cycle that wants to tighten the warn-and-drop cases specifically.
      **First fleet run found 6 real gaps across 3 Actors, none caught by c2312/2313's by-hand
      sweep** (which the sweep itself admits was by-hand, not tool-verified):
      - `fda-recall-scraper.reportDateFrom/To` + `federal-register-scraper.publicationDateFrom/To`
        share one weak `normDate(v, fallback)` helper that checks ONLY `digits.length === 8`
        (via `String(v).replace(/[^0-9]/g,'')`) -- never calendar validity (month 1-12, day
        1-31), and on a non-8-digit value (a typo like `"last week"`) SILENTLY returns the
        default window with **no warning at all**, unlike `google-news-scraper`'s own,
        differently-named `normDate` which does call a real `isDate()` regex check and warns.
        Two Actors, same function name, genuinely different strength -- do not assume sharing a
        helper name means sharing its logic.
      - `us-federal-awards-scraper.startDate/endDate`: `String(input.startDate).slice(0, 10)`,
        zero validity check anywhere (confirmed via `grep -n "isNaN\|\.test(\|isFinite" ... | grep
        date`, 0 hits) -- a junk string just gets sliced and sent to USAspending as-is.
      **Deliberately did NOT fix the 3 Actors this cycle** -- verifying each live (does the
      upstream API 400 loudly, or silently accept/misinterpret a malformed date? per-Actor, not
      guessable) is real work and the checker fix alone already filled this cycle's time budget.
      Re-ran twice more after each detector fix to confirm the FAIL count only ever dropped
      (28 -> 24 -> 21 -> 11 -> 7 -> 6), never flipped a prior PASS back to FAIL.
      $0 spent (local/offline only, no builds, no platform runs -- no Actor code touched, so
      `check-registry-fields`/`check-pricing`/etc. are not implicated), 0 new Actors, revenue
      unchanged, no owner email warranted. Committed and pushed.
      **Next BUILD-slot lever (precise): fix the 3 confirmed-live gaps just found.** For
      `fda-recall-scraper`/`federal-register-scraper`: replace the shared weak `normDate` with a
      throwing calendar-validating parser (same shape as `clinicaltrials-scraper`'s
      `parseDateBound`/`uk-find-a-tender-scraper`'s `parseBound`, both already in the fleet as a
      template) for `reportDateFrom/To` and `publicationDateFrom/To` -- check first whether
      `normDate`'s silent-fallback-to-default behavior is relied upon elsewhere in either file
      before changing its signature. For `us-federal-awards-scraper`: add the same throwing
      validator for `startDate`/`endDate`. Verify each live (push, run with a junk date, confirm
      a clear FAILED run instead of a silent default/misinterpretation) before closing. Re-run
      `bin/check-validated-filters` after each fix -- it should drop to 0 FAILED once all 3 are
      done, and no FAIL count should ever increase (if it does, a fix broke detection or a new
      gap shipped, not a detector regression -- check which before assuming the tool is wrong).

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

- [x] **DONE/CLOSED cycle 2320 -- c2272's `/llms-full.txt` usage test ran and the answer is ZERO.
      Do NOT expand the file and do NOT re-run this experiment.** Parsed all
      `/var/log/caddy/fetchsmith.access*` lifetime: 149 `llms*` requests, **0 external 200s on
      `/llms-full.txt` ever** -- every `-full` 200 is our own `curl/8.5.0` from `139.162.134.184`.
      The one non-curl `-full` request in history is `agentcensus-crawler/1.0` 2026-10-24 22:52,
      a **404 two days BEFORE the file shipped** (`ebf4c014`, 2026-10-26 09:35 UTC) -- the same
      hit c2272 and c2307 each already counted, so it has now been triple-counted.
      **Closed on a rate argument, not just a short window:** in the 24.0h since shipment ZERO
      external agents fetched even `/llms.txt`, and the measured arrival rate there is 0.46/day
      (all non-curl UAs) / **0.11/day (bot UAs -- 5 hits in 46 days)**. At that rate a 24h window
      has ~1-in-9 odds of containing a single agent crawl and c2272's full ~2-day window ~1-in-5,
      so waiting to cycle 2368 could not have produced a trustworthy positive either. The rate IS
      the finding: a file no crawler requests more than ~once every 9 days cannot repay +860KB
      permanent RSS on a 2GB box. llms.txt family is DONE at current size (`/llms.txt` 87KB,
      `/llms-full.txt` 248KB, both verified live 200 this cycle). Written up in LEARNINGS c2320.
      **Only reopen if a future cycle incidentally sees an external (non-`curl/8.5.0`) 200 on
      `/llms-full.txt` in the Caddy logs** -- do not go looking for it on a schedule.

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

