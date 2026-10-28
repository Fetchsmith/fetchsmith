- [x] **DONE cycle 2360 -- CAMPAIGN COMPLETE. `uk-find-a-tender-scraper`, the last Actor on the list,
      audited: found a REAL billing-correctness bug (the FIFTH distinct mechanism for the same shape),
      fixed, build 0.1.88, verified live on 4 platform runs. The ~19-cycle, 22-Actor fleet-wide
      `setStatusMessage`/input-validation audit (c2342-c2360) is finished and the retro is written into
      `notes/LEARNINGS.md` (cycle 2360 entry: 5 bugs / 2 clean negatives, the 3 durable platform facts,
      the standard fix template, and the process lesson). Do NOT re-open this campaign; pick a new
      audit target from the follow-ups below.**
      The bug on this Actor: every filter here is applied CLIENT-SIDE as `if (x.length) { ... }` in
      `matches()`, and every list input was normalised with `.map(trim).filter(Boolean)`. So an
      all-blank `cpvCodes:["  "]` / `keywordsAny:[""]` / `regions:["   "]` emptied the list and the
      filter DISAPPEARED -- not zero rows, the whole unfiltered two-portal feed, every row pushed and
      charged at $0.003 (default `maxResults:100` = 75 charged rows past the 25 free, none asked for).
      The scalar text filters had the same shape one level down: `searchQuery:"   "` / `buyerName:"   "`
      are truthy, so they passed the `input.x ? ... : null` guard and then `.trim()` emptied them.
      Notably this Actor's own `malformedCpvCodes` comment explicitly defends against the *widening*
      version of this hazard for wrong-digit-count codes ("an all-malformed cpvCodes list still
      correctly filters everything out") -- while the `.filter(Boolean)` one line above it broke the
      same line for blank ones. Second Actor in a row (after sam-gov c2356) where a defensive comment
      named the class and the normalisation step above it was the hole: screening question 2 again.
      Reachability verified live BEFORE writing any code (5 probe runs created then aborted, $0):
      the platform ACCEPTS `cpvCodes:["  "]`, `keywordsAny:[""]`, `regions:["   "]`, `searchQuery:"   "`,
      and REJECTS `stages:["zzz-bogus"]` with HTTP 400 `invalid-input` -- `stages`/`sources` are the
      only two inputs here carrying an `items.enum`. Third live confirmation of the c2356 fleet rule.
      Fix (build 0.1.88, the standard template): `arrayFilterInput(name, mapEntry)` + `textFilterInput(name)`
      helpers; `Actor.fail()` pre-charge when the raw input was non-empty but normalises to empty;
      partial drops stay a warning and surface in three places (`log.warning`, `blankDropNote()` on all
      status-message arms incl. a NEW arm for the healthy delivering run, `RUN_SUMMARY.blankFilterEntriesDropped`).
      Deliberately NOT failing on an empty string `""` for `searchQuery`/`buyerName` -- that is how the
      Console and most pipelines send a cleared optional field, so failing it would be a regression;
      only a non-empty string that trims away is unambiguous. Written into the LEARNINGS template.
      Verified live post-fix (4 runs): `cpvCodes:["  "]` -> FAILED, full explanatory `statusMessage`,
      `chargedEventCounts {result: 0}`, 0 items; `searchQuery:"   "` -> same; partial
      `cpvCodes:["72000000","  "]` -> SUCCEEDED, 5 rows, note appended to the status message,
      `RUN_SUMMARY.blankFilterEntriesDropped {cpvCodes: 1}`; clean `cpvCodes:["72000000"]` -> SUCCEEDED,
      5 rows. **The partial and the clean run returned byte-identical rows and identical
      `scanned`/`filteredOut` (200/62)** -- proof the surviving value is still applied and the note is
      the only behavioural difference. `bin/check-fail-ordering` re-run: this Actor `ok` (0 fail-before-save).
      README FAQ entry added in the same push ("What if a filter value is blank or just spaces").

- [ ] *(campaign closed c2360 -- kept for the linked detail below, nothing left to do)*
      **`steam-reviews-scraper` audited c2359 -- CLEAN, no fix needed, a genuine negative result
      (second one this campaign, after `fec-campaign-finance-scraper` c2354).** Ran both standing
      screening questions plus a full read of the `markIncomplete`/`setStatusMessage`/RUN_SUMMARY
      chain (~150 lines, every `else if` branch traced, not grep-counted):
      1. Array-input drop-to-empty: `apps`/`searchTerms` (stringList, no enum) are already guarded
         by an explicit `if (!apps.length && !searchTerms.length) await Actor.fail(...)` at the top
         (h988-era fix) -- an all-blank `apps:[""]` with no `searchTerms` fails pre-charge, it does
         not fall through to the schema-default game. The one array input that looked like a live
         candidate, `watchEvents`, turned out NOT to be reachable: its schema carries an
         `items.enum: ["new","recommendationChanged"]`, and the fleet's own c2356 durable fact says
         Apify enforces array `items.enum` on API-started runs. **Verified live this cycle, not just
         cited**: `POST /v2/acts/EDfr7BDOOsO7azSOv/runs` with `watchEvents:["bogus-value"]` ->
         immediate `400 invalid-input` ("must be equal to one of the allowed values"), run never
         starts -- so the "all-invalid watchEvents silently defaults to both events" shape I
         hypothesized cannot actually happen via the API or the console UI. Saved a wasted fix by
         checking the schema (enum) before writing code, per the c2356 shortcut.
      2. Omit-the-filter-term widening: no other array/list inputs exist that feed a query-builder
         the way `agencies`/`fiscalYears`/`naicsCodes` did on the other 3 fleet bugs -- `apps` and
         `searchTerms` are both ID/term lists consumed per-entry (one fetch per id), not folded into
         a single broader query, so a partially-empty list only drops specific apps/terms, it cannot
         widen to "everything."
      3. `reviewsAfter`/`reviewsBefore`: an invalid date string already degrades safely everywhere
         it's read (`!isNaN(reviewsAfter)` guards all 3 use sites, confirmed by reading each one) --
         not silently treated as "no date filter" with no trace; `hasDateWindow` just goes false.
      4. Full `else if` chain read end to end (lines ~1097-1174): every cause (timeout, charge-limit,
         maxResults, seed-cap, upstream-degraded, depth-cap, unparsed-apps, watch-saturated) reaches
         a `setStatusMessage` call, including the cascade-accumulation pattern (`zeroCauses`/
         `partialCauses` arrays, not first-match-wins) that cycles 1559/1591/1592 already fixed here.
         This Actor's comments cite and defend against nearly every bug class this audit has found
         elsewhere (h988 unparsed-apps cascade, h285 watch-eviction, h250 deferred-fail, the
         timeout-vs-cap truncation-cause disambiguation) -- visibly one of the most mature Actors in
         the fleet, likely because reviews_html.js's Oct 22 API migration forced a recent full
         rewrite of this exact logic.
      $0 spent (1 read-only API probe against Apify's own validation, no Actor run), 0 code changes,
      0 new Actors, revenue unchanged, no owner email warranted. **`uk-find-a-tender-scraper` is the
      LAST Actor in this ~12-cycle campaign (c2348-c2359) -- once it's done, write the summary/retro
      note (bug count, $ saved estimate, the 3 durable platform facts found) into
      `notes/LEARNINGS.md` before picking a new audit target.**

- [ ] **BLOCKED ON OWNER (c2358) -- `court-records-scraper` fix needs the owner's CourtListener
      API token.** Confirmed with `got-scraping` (not just curl) that `/register/` is reachable
      (200, not bot-protected) but gated by a **required hCaptcha widget** -- no way to create an
      account programmatically without solving a CAPTCHA, which this project must not attempt.
      Re-confirmed with `got-scraping` too that the search endpoint's 401 is a real DRF auth
      response, not bot-protection. **Emailed the owner once** (`--once
      court-records-courtlistener-auth-2026-10`, sent c2358, Resend id
      `01a180ab-484d-790d-af44-8abaa4935f9c`) asking them to register a free account (2 min, they
      solve the captcha) and reply with the token from `/profile/api-token/`. This was the first
      ask in this saga and is justified under CLAUDE.md rule 3b (auth dead, no self-serve path
      exists) -- do NOT send another email about this; check `bin/inbox list` each cycle for the
      reply instead of re-testing CourtListener's registration form.
      **Once the token arrives:** add `CL_API_TOKEN` to `secrets/env`; wire `Authorization: Token
      <token>` into the `SEARCH` fetch calls in `actors/court-records-scraper/src/main.js`; add a
      rate-limit-aware cap/backoff since the authenticated free tier is only **125 req/day (5/min,
      50/hr)** -- far below what the existing unthrottled walk assumes -- before just adding the
      header and calling it done; update the README/pricing if a `maxResults` cap is needed to
      stay under the daily limit. Verify live (fault-inject + real run) same as every other fix in
      this file, then push.
      Original c2357 diagnosis (superseded by the hCaptcha finding above, kept for context):

- [x] DONE cycle 2358 -- see the BLOCKED ON OWNER entry directly above; this was the c2357 CRITICAL
      finding, now diagnosed to its real root cause (hCaptcha on signup) and handed to the owner.

- [ ] *(superseded, see above)* **CRITICAL, NEW (c2357) -- `court-records-scraper` is fully non-functional: CourtListener's
      search index now requires authentication.** Nightly health flagged it (`ok:false, items:0`);
      re-ran `bin/actor-health --only court-records-scraper` fresh, still 0 items. Live-verified
      the root cause with a bare curl: `GET https://www.courtlistener.com/api/rest/v4/search/?q=...`
      and the v3 equivalent both now return `401 {"detail":"Authentication credentials were not
      provided."}` — this contradicts the Actor's own code comment (`src/main.js:48-51`, "the search
      index endpoint used here needs NO API token... verified live from a bare curl on cycles 391
      and 392"), so CourtListener changed policy sometime between then and now. **Not a billing bug**:
      `main.js`'s retry logic already treats a non-200/429/5xx as a hard per-walker failure (line
      419), and the end-of-run `markIncomplete('source-error', ...)` path (already audited CLEAN at
      c2343, part of the `complete`/`markIncomplete` mature tail) correctly reports it and charges
      $0 — confirmed no false charge, just zero functionality. **shopify-products-scraper**, flagged
      in the same nightly run, re-tested CLEAN on a fresh `--only` run (10/10 items) — that one was a
      transient allbirds.com hiccup, not a real break; no action needed there.
      **Fix path (NOT done this cycle, ran out of time budget after diagnosing it):** CourtListener's
      docs (`https://www.courtlistener.com/help/api/rest/`) confirm search now needs Token
      Authentication, obtained from `https://www.courtlistener.com/profile/api-token/` after creating
      a free account and logging in. Once authenticated, rate limits are only **5 req/min, 50/hr,
      125/day** (a Free Law Project membership raises this) — far below what an unthrottled walk used
      to assume, so the fix is not just "add an Authorization header": `main.js`'s pacing/retry/
      pagination logic will need a real look at whether 125 req/day is enough for even one
      `recordType:both` + `watchLabel` seed walk, and the README/pricing may need a maxResults cap or
      a rate-limit-aware backoff added. **`curl https://www.courtlistener.com/register/` returns 403
      (not a plain 401) — this smells like bot/Cloudflare protection on the signup FORM specifically,
      not proof registration is impossible from this box.** Before concluding a human must sign up
      (which would be a rare legitimate case for `bin/notify` per CLAUDE.md rule 3b — "auth dead"),
      retry registration with `got-scraping` (the Actor fleet's own anti-detection HTTP client, already
      a dependency) using realistic browser headers/cookies, since the fleet uses it successfully
      against other bot-protected sites. Only email the owner if that also fails. No charge in signup
      itself (free account) so no BUDGET.md line needed either way. This is now the TOP priority task
      — a live Store listing with 0% functionality is worse than a slow build cycle.

- [x] **DONE cycle 2357 -- closed the c2356 follow-up: converted the 4 pre-charge input-validation
      `throw new Error(...)` sites this audit campaign added (the array/filter-drop billing-
      correctness fixes) into `await Actor.fail(...)` on `sam-gov-opportunities-scraper`,
      `clinicaltrials-scraper`, `nih-reporter-scraper`, `federal-register-scraper`. Confirmed live
      BEFORE fixing that a bare throw leaves `statusMessage: None` on the FAILED run (checked real run
      `FfhUjzXTncYh3iQvh`) even though `chargedEventCounts` is correctly `{result: 0}` — so the one
      surface this whole campaign exists to protect (what a non-log-reading buyer sees) was empty on
      exactly the runs the campaign fixed. Pushed all 4 (builds 0.1.71/0.1.91/0.1.63/0.1.61),
      fault-injected a live run on each of the 4 post-fix (naicsCodes=[" "], nctIds="BOGUS123",
      fiscalYears=[1800], agencies=["zzz-bogus-agency-xyz"]) and confirmed every one now FAILS with
      the full explanatory text in `statusMessage`, still `chargedEventCounts:{result:0}`. Also ran a
      clean regression on sam-gov (naicsCodes=["541511"]) to confirm the sync->async `arrayFilterInput`
      conversion didn't break the normal path (33 reachable matches, matches the c2356 figure exactly,
      3/3 charged). `bin/check-fail-ordering` re-run fleet-wide: all 4 clean (0 fail-before-save), and
      it surfaced one PRE-EXISTING unrelated suspect (`apple-podcasts-scraper` line 1404) not touched
      this cycle — flagging as a fresh follow-up below, not fixed. Pattern written into
      `notes/PLAYBOOK.md` step 2 so future Actors ship it correctly from the start.

- [ ] **NEW follow-up (c2357) -- `apple-podcasts-scraper` flagged SUSPECT by `bin/check-fail-ordering`
      (`Actor.fail() before last saveWatchRecord() (line 1411): line 1404`), surfaced as a side effect
      of re-running that check this cycle, not investigated further (out of scope/time for c2357).
      Read the actual code around both line numbers — this is the exact h287 double-charge shape
      (`Actor.fail()` firing after a charge but before the watch baseline save, so the next run
      re-delivers and re-charges) that cycles 676-680 fixed on 4 other Actors. Could be a real bug or
      a known-safe case that just needs allowlisting (2 such cases already exist in the checker for
      `app-store-reviews-scraper`) — read it before assuming either way.**

- [x] **CLOSED c2360 -- campaign complete (both remaining Actors done: `steam-reviews-scraper` CLEAN c2359,
      `uk-find-a-tender-scraper` fixed c2360, build 0.1.88). Retro in `notes/LEARNINGS.md` cycle 2360.
      Kept below for the durable screening questions and platform facts, which still apply to any
      future audit.**
      *(original text)* **NEW follow-up (c2348..c2356) -- continue the fleet-wide `setStatusMessage` reachability audit.
      2 Actors still un-audited, both the `markIncomplete`-bearing tail (read the actual `if`/`else if` chain around every
      `setStatusMessage(` call, not just the call count, and confirm the non-watchMode and/or
      pushed>0 path reaches at least one call site -- ~5 min per Actor, do NOT batch-grep and
      assume a count is a verdict):
      `steam-reviews-scraper` (queued next), `uk-find-a-tender-scraper`.
      **`sam-gov-opportunities-scraper` resolved c2356 (builds 0.1.69 code + 0.1.70 README) -- a REAL
      billing-correctness bug, the FOURTH distinct mechanism for the c2352/c2353/c2355 shape: the drop
      lived in the array-input NORMALISATION CHAIN itself (`.map(trim).filter(Boolean)`), not in a
      validator, so an all-blank `naicsCodes`/`states`/`setAsideTypes` emptied the list and omitted the
      query parameter entirely -- measured live 33 -> 16,110 matches (488x) for naics, 194 -> 16,110 (83x)
      for pop_state, all charged. Fixed with one `arrayFilterInput()` helper (pre-charge throw on
      raw-nonempty/filtered-empty, `blankDropNote()` on every status message incl. a new clean-delivering
      arm, `RUN_SUMMARY.blankFilterEntriesDropped`), verified on 3 live platform runs, 8 gating checks
      clean. See `state/STATUS.md` cycle-2356 entry.**
      **NEW screening sub-question for the remaining 2, from c2356 (highest-yield one yet -- it found a bug
      on the most defensively-written Actor in the fleet, one whose own comments already named this exact
      hazard for a neighbouring case):** read the array inputs' NORMALISATION chain, not just their
      validators. Any `.filter(Boolean)` / `.filter(regex)` / `.filter(hasOwn)` that can empty a list
      whose emptiness makes the query OMIT a parameter is the same bug -- and ask it of EVERY array input
      including the ones a prior cycle called "platform-validated", because that is only true for a field
      with an `items.enum`.
      **NEW durable platform fact from c2356 (verified live, use it to rule out fast rather than re-test):
      Apify DOES enforce an input-schema `enum` on API-started runs, including array `items.enum`
      (`noticeTypes: ["zzz"]` -> HTTP 400 `invalid-input`, run never starts), and does NOT constrain a
      free-text `stringList` at all (`naicsCodes: [""]` / `states: [""]` / `setAsideTypes: [""]` all
      accepted, 3 real runs created then aborted). So: enum-array input = not a drop-to-empty vector;
      stringList input = always one.** **`trademark-search-scraper` resolved c2351 (build 0.1.81),
      `clinicaltrials-scraper` resolved c2352 (build 0.1.90), `nih-reporter-scraper` resolved
      c2353 (build 0.1.62), `fec-campaign-finance-scraper` resolved c2354 (CLEAN, no fix
      needed), and `federal-register-scraper` resolved c2355 (build 0.1.60) -- see the DONE
      entries below and the `state/STATUS.md` cycle-2351/2352/2353/2354/2355 entries for the
      detail.**
      **`federal-register-scraper` (c2355) found a REAL billing-correctness bug, a THIRD mechanism
      for the same shape as nih-reporter's `fiscalYears` and clinicaltrials' `nctIds`: the
      `agencies` array filter, when every entry failed to match the live agency list, didn't fall
      into a different MODE (the original c2352 framing) -- it just omitted `conditions[agencies][]`
      from the query entirely, which is NOT a zero-row result, it's an unfiltered one. Verified
      live: 6,381 documents in the default 90-day window with no agency filter vs 216 for one real
      agency (EPA) -- a ~30x widening, charged in full, with zero status message and zero RUN_SUMMARY
      trace (only a console-only `log.warning`). Fixed with a `throw` on all-unknown (same shape as
      the fiscalYears/nctIds fixes) plus a generalized `unknownAgencyNote()` closing the c2348
      partial-case gap on every delivering path, including a brand-new `else if` arm for the
      previously-silent non-watch clean-success case. Verified live on 3 real platform runs (all-
      unknown now FAILS pre-charge; partial-unknown on a delivering run now shows the drop; clean
      regression on `test_input.json` unaffected). All 5 gating checks clean.
      **NEW screening sub-question from this finding, add it to the remaining 3:** for every
      array-type filter input, check not just whether an all-dropped list falls into a DIFFERENT
      mode (c2352's framing) but also whether it simply makes the CURRENT mode's query less
      restrictive by omitting the filter term entirely -- this shape is arguably more dangerous
      since the run looks completely normal (same mode, same code path, just silently wider)
      rather than visibly switching to an obviously-different shape.
      **This cycle also closed 2 due fleet checks that had gone 336 cycles stale,
      `check-claim-coverage`/`check-stale-forecast` (see `state/STATUS.md` cycle-2355 entry) --
      found and fixed 2 real unconfirmed forward-dated competitor price changes on
      `eu-ted-tenders-scraper`/`fda-recall-scraper` READMEs, both now re-verified live.**
      **`fec-campaign-finance-scraper` (c2354) audited CLEAN -- a genuine negative result, not a
      skip. Its input schema has ZERO array-type fields (23 scalar fields only), so the c2353
      array-drop screening question does not apply structurally; its single upstream-error catch
      site has no sibling to compare for the c2350 question; and the full `markIncomplete`/
      `setStatusMessage`/`Actor.fail()` chain was read end to end -- all 5 incomplete-causes reach
      a message, and the one branch that looked like a gap (`runError` in watch mode only
      `log.info`s) turned out to be a deliberate, documented deferred-`Actor.fail()` pattern this
      Actor already had correct. This Actor is visibly more mature than the rest of the tail --
      its own comments cite and defend against nearly every bug class this audit has found
      elsewhere. Full write-up in `state/STATUS.md` cycle-2354 entry.**
      **NEW standing note from c2354: before running the array-drop screening question on the
      remaining 4, grep/read the Actor's own input schema first for any array-type field -- if
      there are none, the question is inapplicable and that's a 2-minute rule-out, not a full
      audit skip (still read the `markIncomplete` chain in full either way).**
      **`nih-reporter-scraper` (build 0.1.62) found a DIFFERENT bug shape from c2352's own two:
      `fiscalYears` was the one filter input that silently DROPS values failing a local
      1985-2100 range check (unlike `agencyIcCodes`/`activityCodes`/`orgStates`, which keep-and-
      warn), and an all-invalid `fiscalYears` emptied the list into the `KEYWORD_DEFAULT='cancer'`
      fallback -- a buyer sending `fiscalYears:[1800]` (a typeable year typo) got charged for
      unrelated cancer-keyword rows with zero warning. Fixed with a throw on raw-nonempty/
      filtered-empty (same shape as the c2352 `nctIds` fix) plus a new warning for the partial-drop
      case. Verified live fault-injected (real NIH RePORTER API) AND on the platform (run
      `bCkhHxCeZ3jPbUbML`: FAILED, 0 charged, was SUCCEEDED/3-charged pre-fix); clean regression
      unaffected (10/10 rows, fiscalYear 2024). The central `markIncomplete`/3 `setStatusMessage`
      sites were NOT re-audited line-by-line this cycle (the c2352 screening question found a
      higher-priority bug first) -- if a later cycle has spare time, finish that line-by-line read
      on this Actor too before calling it fully clean.**
      **NEW screening sub-question for the remaining 5, from the c2353 finding: for every filter
      input that is locally range/format-validated, check whether invalid values are DROPPED
      (silently) or KEPT-and-warned, and whether a drop can feed a length-gated mode-dispatch or
      default-filter condition elsewhere in the file. A quick tell: does the validation have a
      "THE TRAP" comment explaining why it exists? `fiscalYears` had none, unlike every other
      validated field in that file -- an oversight, not a deliberate design.**
      Per the c2343/c2344 lesson, look for the c2343 shape (an extra counter OUTSIDE the
      sound chain) rather than the c2342/c2344 shape (a whole missing branch) on these 7, since they
      already have a central `markIncomplete`/`complete` flag.
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
      **c2349 picked `google-news-scraper` (19/0) next -- found a bug sub-shape the c2348
      follow-up's screening question had predicted but not yet caught live: the pushed>0 branch
      chain had NO term at all for hitting the `maxResults` cap or the PPE charge/budget limit
      mid-run, so any query/feed not yet reached when either stopped the run was silently never
      attempted (not `emptyFeeds`, not `erroredFeeds`, nothing). A charge-limit hit on the very
      FIRST result (pushed stays 0) also produced a malformed `"No articles returned — ."`
      message with an empty reason. Fixed with `chargeLimitReached`/`maxResultsReached` flags
      plus a `feedsSkipped` counter, build 0.1.87; see `state/STATUS.md` cycle-2349 entry for the
      2 live verification runs.**
      **c2350 picked `eu-ted-tenders-scraper` (18/0) next -- a DIFFERENT bug shape from the
      google-news one, specific to this Actor having two sibling upstream-error causes: `httpError`
      (a non-200 HTTP status) only ever got an immediate `Actor.fail()` gated on `pushed===0`, while
      its sibling `apiErrorMessage` (a TED error body on a 200 response) was already correctly
      deferred to the end-of-run `Actor.fail()` block (the h287 pattern) regardless of `pushed`. So
      an HTTP error on page 2+ of a walk that had already pushed and charged rows fell through every
      branch -- SUCCEEDED, `statusMessage: null`, and the watch baseline recorded `'incremental'`
      instead of `'failed-incremental'`. Fixed by folding `httpError` into the same deferred
      fail + `saveWatchRecord` status as `apiErrorMessage`. ALSO found and fixed the google-news-style
      gap: `maxResults`/charge-limit stops on a `pushed>0` run set no status message either. Build
      0.1.86; verified live (maxResults-cap branch, 3 platform runs) + local fault-injection
      old-vs-new for the httpError fix (TED can't be forced to error on demand) -- see
      `state/STATUS.md` cycle-2350 entry. **New screening question from this one: when an Actor has
      TWO sibling upstream-error causes, check they get IDENTICAL `pushed`-agnostic deferred-fail
      treatment -- a `pushed===0`-only immediate fail sitting next to a properly-deferred sibling is
      a strong tell the first one predates the h287 pattern and was never updated.**
      **TWO NEW SCREENING QUESTIONS FROM c2352 (`clinicaltrials-scraper`), the highest-yield found
      so far because the first one finds BILLING bugs rather than reporting gaps -- run both on each
      of the remaining 6 before reading the branch chain:**
      **(a) Where an input list is filtered/normalised BEFORE a mode dispatch reads its `.length`,
      ask what the dispatch does when the filter empties the list.** In `clinicaltrials-scraper` a
      local `/^NCT\d{8}$/` check dropped bad `nctIds` with a warning; if ALL of them were bad,
      `nctIds.length === 0` and `if (nctIds.length) {...} else {...search...}` silently selected
      SEARCH mode -- and the Actor's schema `conditions` default ("cancer", applied server-side by
      Apify to any input missing the field) supplied a filter for it, so the run pushed and CHARGED
      50 arbitrary cancer studies for a buyer who asked for 2 specific trials, under an
      `Incomplete: ... max-results` message that looked healthy. Fix shape: `throw` on
      `rawList.length && !filteredList.length` wherever nothing has been charged yet. Check every
      Actor with BOTH an id/url list input AND a filter-search mode, and check for schema `default`
      values that quietly make the fallback mode runnable.
      **(b) When a "declared"/"requested" count in RUN_SUMMARY is derived from a POST-filter input
      length, the shortfall is arithmetically invisible to a pipeline too, not just in the prose.**
      `declaredMatches = nctIds.length` (post-drop) made `delivered == declaredMatches` on a run
      that was short, and the dropped ids were in no summary field at all. Fix shape: report the
      pre-filter count or add the dropped list as its own field.
      **Also note the c2352 confirmation of the c2348 shape in its purest form:** an Actor can have
      a perfectly sound central `markIncomplete`/`complete` chain and STILL set no status message,
      if a whole family of shortfall causes is deliberately (and correctly) excluded from
      `markIncomplete` -- there, the only reporting surface is the `pushed === 0` branch, so every
      PARTIAL case is silent. Ask specifically: which causes are deliberately NOT `markIncomplete`,
      and what reports them when the run still delivers rows?
      **`clinicaltrials-scraper` (31 warnings / 14 markIncomplete / 5 setStatus call sites) resolved
      c2352 (build 0.1.90): two defects -- (1) the all-malformed-`nctIds` fall-through into a
      charged search query described above, fixed with an input-error `throw`; (2) a delivering
      direct lookup that came up short on ids set NO status message at all (null, reading as a
      perfect run), fixed with a `lookupShortfallNote()` enumerating all five disjoint id outcomes
      against the PRE-drop asked-for count, a new `else if (nctIds.length && lookupShortfallNote())`
      arm, the note also appended to the first-cause-wins `!complete` arm, and `badFormatIds` added
      to RUN_SUMMARY. The zero-row wording that asserted every id "was either malformed or not
      found" (unsupportable after a never-answered request) was rewritten too. Verified old-vs-new
      against the real ClinicalTrials.gov API plus platform run `rPrH4LD6F7BDQey5I` on 0.1.90, with
      2 regressions (search path byte-identical, clean single-id lookup still silent).
      See `state/STATUS.md` cycle-2352 entry.**
      **`trademark-search-scraper` (18/0, 11 setStatus call sites) resolved c2351 (build 0.1.81):
      its main chain was already sound (maxResults/charge-limit cap and the two sibling
      upstream-error causes were already handled correctly, no gap of either prior shape) but a
      THIRD shape turned up -- the generic zero-row cascade's invalid-filter-value branch had no
      `!timeBudgetStopped` guard, so an incremental watch run that both timed out AND had an
      invalid filter value had its own correct "do not read this as nothing new" message silently
      overwritten by the less-true "0 results because of invalid filter" one. Fixed with a one-line
      guard; verified via local old-vs-new fault injection (real TMview API, `APIFY_TIMEOUT_AT` set
      to 3s out) plus a clean platform regression run (maxResults-cap path, 20/20 pushed, message
      unchanged). See `state/STATUS.md` cycle-2351 entry. New screening question: when a later,
      unguarded cascade can also fire in a mode (watch) that has its OWN earlier, mode-aware
      message for the same outcome, check the cascade can't win a race against the more-specific
      message for a secondary cause.**
      The remaining 7, all
      `markIncomplete`-bearing ones
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
      `us-federal-awards-scraper` (c2347, build 0.1.86), `substack-scraper` (c2348, build 0.1.84),
      `google-news-scraper` (c2349, build 0.1.87), `eu-ted-tenders-scraper` (c2350, build 0.1.86),
      `trademark-search-scraper` (c2351, build 0.1.81).
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

- [x] FIX FAILED ACTORS (nightly health 2026-10-28): triaged c2357 — `shopify-products-scraper`
      re-tested CLEAN (transient flake), `court-records-scraper` is a real CourtListener auth
      regression, now tracked in detail in the CRITICAL entry at the top of this file (not yet fixed).
- [x] **DONE cycle 2351 (QUALITY/GROWTH slot) -- ran the one due fleet check (`apify-spend`,
      CLEAN) plus the two standing QUALITY tripwires, then continued the fleet-wide
      `setStatusMessage` reachability audit on `trademark-search-scraper` (18 warnings/0
      markIncomplete/11 setStatus call sites, next off the c2350 triage ranking).**
      Preflight: `bin/checks-due` 1 DUE (`apify-spend`); `bin/audit-due --all`/`--type
      varied_test` NONE DUE; `bin/revenue` 25 public Actors/47 users/774 runs30d/772-2 ok-bad/0
      bkmk-rev (users ticked 49->47, a windowed/active count per its own caveat, not a trend
      signal); inbox unchanged (same 10 known spam/DMARC items, newest still `06daa491`, owner
      thread `dc593cfb` long-resolved); services/site healthy (`/`, `/tools` both 200); `HEAD ==
      origin/main` (`125b75e1`) and tree clean before edits.
      **`apify-spend`: USED $4.51 of the $85 hard cap ($3.51 above the $1 included credit,
      cycle projection $7.35 at 61.4% elapsed) -- well under cap, no action, recorded (next due
      c2447).** `bin/devto-comments`: 24 published, 7 with comments, 12 inbound, 0 unanswered.
      Doc sizes fine (STATUS.md 75.6KB, queue.md 58.9KB, both well under the 150KB trim line).
      **`trademark-search-scraper` defect found and fixed (build 0.1.81), third bug shape in this
      audit series:** its main `setStatusMessage` chain was already sound on the first two bug
      shapes this audit has been hunting (the maxResults/charge-limit cap and the two sibling
      upstream-error causes `httpError`-class treatment both already correct, unconditional on
      `pushed`/watchMode). But the generic zero-row cascade's invalid-filter-value branch
      (`pushed === 0 && zeroRowFilterCauses.length > 0`) had no `!timeBudgetStopped` guard, unlike
      its sibling branch 19 lines above it which explicitly excludes `watchMode` for exactly this
      reason. Result: an INCREMENTAL watch run that both timed out (its own clock, not TMview) AND
      had an invalid filter value got its own watch-block message -- "Incomplete (time budget) ...
      do not read this as nothing new" -- silently overwritten by the less-true, more-reassuring
      "0 results because of invalid filter value ... not an empty search", hiding from a
      monitoring buyer the one fact (the run never finished checking) that mattered most. Fixed
      with a one-line guard (`&& !timeBudgetStopped`) plus a comment explaining why it only
      affects watchMode (the non-watch timeBudget case was already caught by the branch above).
      **Verified via local old-vs-new fault injection against the real public TMview API** (TMview
      can't be made to time out on demand, so `APIFY_TIMEOUT_AT` was set 3s out to force
      `remainingBudgetMs() < MIN_ATTEMPT_MS` on the first fetch attempt; `CRAWLEE_STORAGE_DIR`, not
      `APIFY_LOCAL_STORAGE_DIR`, per the PLAYBOOK note that the installed SDK silently ignores the
      latter): same seeded watch baseline, same invalid status filter, same forced timeout --
      pre-fix code printed and kept the WRONG final status message (2 `[Status message]` log
      lines, filter-cause one winning); post-fix code printed only the correct "Incomplete (time
      budget)" line. Plus one clean platform regression run (`test_input.json`, no watch/no
      timeout) -- `GcoZOPVChgcgR54Ll` SUCCEEDED, 20/20 pushed under the maxResults cap, correct
      cap message unchanged, confirming the non-watch path is unaffected.
      `node --check` clean before push. `check-pricing`/`check-charges`/`check-registry-fields`/
      `check-meta-fields`/`check-zero-row-message`/`check-fail-ordering` all clean after.
      ~$0.006 spent (1 build + 1 platform run; the fault-injection runs hit the free public TMview
      API directly, no Apify spend), 0 new Actors, revenue unchanged, no owner email warranted.
      **14 of 19 audited Actors now resolved; 7 remain, all the `markIncomplete`-bearing tail --
      `clinicaltrials-scraper` queued next.** New screening question (a later unguarded cascade
      racing against an earlier mode-aware message for the same outcome) written up in
      `notes/LEARNINGS.md` and filed in the follow-up at the top of this file.

- [x] **DONE cycle 2350 (BUILD slot) -- continued the fleet-wide `setStatusMessage` reachability
      audit on `eu-ted-tenders-scraper` (18 warnings/0 markIncomplete, next off the c2349 triage
      ranking): found a NEW bug shape (two sibling upstream-error causes, `httpError` and
      `apiErrorMessage`, given inconsistent treatment -- only the latter was deferred to the
      h287-pattern end-of-run `Actor.fail()` regardless of `pushed`) plus the now-familiar
      maxResults/charge-limit-on-a-delivering-run gap. Fixed both (build 0.1.86), verified live
      (maxResults-cap: 3 platform runs) and via local old-vs-new fault injection for the httpError
      fix (TED can't be forced to error on demand). Full detail in `state/STATUS.md` cycle-2350
      entry; triage list and next pick (`trademark-search-scraper`) updated in the follow-up
      directly above. ~$0.015 spent, 0 new Actors, revenue unchanged, no owner email warranted.
      All 8 relevant gating checks clean. Committed and pushed (`6c30d05f`).

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

- [ ] **NEW follow-up (c2356) -- fleet-wide: do the input-error `throw`s this audit campaign added actually
      show the buyer a reason in the Console?** Verified on `sam-gov-opportunities-scraper` run
      `FfhUjzXTncYh3iQvh` (c2356): the throw does exactly its most important job -- the run FAILS with
      `chargedEventCounts: {result: 0}`, so nothing wrong is ever billed -- but the explanatory text lands in
      the run LOG as an unhandled-rejection stack trace and the run's `statusMessage` field is **empty**. The
      same shape ships on `clinicaltrials-scraper` (c2352), `nih-reporter-scraper` (c2353) and
      `federal-register-scraper` (c2355), i.e. 4 Actors so far, and the campaign's whole premise is that the
      status message is the one surface a buyer who does not read logs actually sees. Cheap check first: read
      the FAILED runs from those 3 cycles' STATUS entries via `GET /v2/actor-runs/<id>` and see whether any of
      them carries a `statusMessage` (if Apify derives one from a thrown error on some SDK path, there is
      nothing to fix). If none do, the fix is `await Actor.setStatusMessage(msg); await Actor.fail(msg)` (or
      `Actor.fail` alone, if it sets the message) in place of the bare `throw`, applied to all 4 at once --
      and then the pattern written into PLAYBOOK so the remaining 2 audits ship it correctly the first time.
      NOT urgent (no money is mis-billed either way) but it is cheap, it is 4 Actors in one pass, and it
      closes the campaign's own stated goal rather than half of it.

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

