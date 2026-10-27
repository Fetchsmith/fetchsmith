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

- [ ] **NEW follow-up (c2312) -- `scholarship-scraper` carries an UNPUSHED code fix.** c2312 found
      and fixed the same unvalidated-date-bound bug there (`Date.parse(...)` -> `NaN`, and
      `NaN != null` is true, so the guard passes and the filter both widens and hides undated
      rows). It was deliberately NOT pushed: that Actor is the fleet's only `status: retired`
      registry entry and is PAUSED on the Store, so a ~$0.005 build buys nothing today.
      **Action required only if/when it is ever un-retired: `apify push --force` it** so the live
      build actually contains the fix. Do not spend a build on it before then.

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

- [x] **DONE cycle 2308 (BUILD slot, `2308%3==1`) -- ran the due `git-maintain` fleet check
      (TRIPPED: first live trip of the c2164 size gauge, `.git` 170 -> 106 MiB) and shipped a
      real `ats-jobs-scraper` fix found by cold-read defect hunt (silent salary-filter zero-rows
      on the 5 salary-blind ATSes).**
      `git-maintain`: loose 1651 obj / 74 MiB -- SIZE threshold (64) fired, COUNT (4000) at only
      41% would have no-op'd a 5th straight time. Repacked loose 1651 -> 0, pack 96 -> 103 MiB.
      Growth model re-derived and CORRECTED (the 74 MiB spans 144c since the last real repack at
      c2164, not 48c): ~550 obj / 24.7 MiB per 48c day, mildly accelerating. c2212's forecast was
      right on both cycles. Next due c2356; forecast no-trip at c2356/c2404, **TRIPS at c2452**.
      `ats-jobs-scraper`: `workable`/`teamtailor`/`personio`/`smartrecruiters`/`workday` hard-code
      `salaryMin`/`salaryMax` to null (no upstream compensation field), so `hasSalary`/`minSalary`/
      `maxSalary` silently drops those whole boards. The Actor already warns per-board for the
      identical `employmentTypeKeyword` case; `zeroRowCauses()` does NOT cover it because that only
      fires when the run matched nothing at all -- on a mixed list the blind boards contribute 0
      invisibly. Added `SALARY_BLIND_ATS` + run-derived `salaryFilterNames` + a per-board
      `log.warning`. Build **0.1.108** pushed; verified on a live run (workday + `minSalary:50000`
      -> the warning fires naming only `minSalary`, with `20 postings, 0 kept`). First run was
      inconclusive (hit `maxResults` on the greenhouse board before reaching workday) so it was
      re-run rather than claimed. Full details in `state/STATUS.md` cycle-2308 entry.
      ~$0.005 spent (1 build + 2 small runs), 0 new Actors, revenue unchanged (48 users, 0/0),
      no owner email warranted.

- [x] **DONE cycle 2309 (BUILD slot, `2309%3==2`) -- continued c2308's bug-class hunt on the 3
      named candidates. `court-records-scraper`/`eu-ted-tenders-scraper` ruled out (single
      upstream each, no cross-source subset possible); `remote-jobs-scraper` (7 boards) had the
      exact gap and got the same fix ats-jobs-scraper got at c2308.**
      Mapped via `grep ": null"` per fetcher: `jobTypeKeyword` blind on `remoteok`/`workingnomads`
      (2/7), `seniorityKeyword` blind on `remotive`/`remoteok`/`arbeitnow`/`workingnomads`/`wwr`
      (5/7), `salaryOnly`/`minSalaryAnnual` blind on `arbeitnow`/`workingnomads`/`wwr` (3/7,
      Remotive keeps `salaryText` so it's NOT blind on this axis). README already disclosed all
      three precisely -- the gap was purely a missing RUNTIME warning, same shape c2308 closed.
      Shipped `JOBTYPE_BLIND`/`SENIORITY_BLIND`/`SALARY_BLIND` + run-derived `salaryFilterNames`
      + `warnIfBlindFilter(src)` in `src/main.js`, called once per source next to the existing
      "N match the filters" log line. Build **0.1.85** pushed; verified live
      (`sources:["remoteok","jobicy"], jobTypeKeyword:"contract"` -> `WARN remoteok: ... drops
      every posting ...` fired exactly once, no false-fire on the unset seniority/salary filters,
      jobicy's 2 real contract rows came through correctly). `check-registry-fields`/
      `check-code-fields`/`check-meta-fields`/`check-pricing` all re-run clean (no field/pricing
      change, so this was a no-op sanity check). ~$0.005 spent, 0 new Actors, revenue unchanged
      (48 users, 0/0), no owner email warranted. Full details in STATUS.md cycle-2309 entry.

- [x] **DONE cycle 2310 (MANDATED QUALITY/GROWTH slot, `2310%3==0`) -- ran the two standing
      PLAYBOOK QUALITY-cycle tools (`check-disclosure`, `devto-comments`), both clean, and caught
      a real process drift: neither had actually run in the last 5 QUALITY slots (since c2295).**
      Nothing fleet-wide due (checks/audits/varied_test all NONE DUE), inbox unchanged, no
      actionable queue follow-up, services/site healthy throughout. `check-disclosure`: 88 site
      posts + 24 dev.to articles, 0 missing AI-authorship disclosure. `devto-comments`: 24
      published articles, 7 with comments, 12 inbound, 0 unanswered, 1 spam-skipped. Both tools
      are supposed to run "every QUALITY/GROWTH cycle" per `PLAYBOOK.md:153,155`, but c2298/2301/
      2304/2307 (all QUALITY slots) ran ad-hoc work instead -- only the 48c/144c backstop clocks
      in `fleet_checks.json` were tracking it, with 33c/129c of margin left. Recorded via
      `bin/checks-due --ran check-disclosure/devto-comments` (next due c2358/c2454). $0 spent,
      0 new Actors, 0 code changes, revenue unchanged (48 users, 0/0), no owner email warranted.
      Committed and pushed (`8710782e`). Full details in `state/STATUS.md` cycle-2310 entry.
      **Next QUALITY-slot default: both standing tools now current -- pick a fresh README-
      competitor or cold-read pass instead of re-running these before c2358/c2454.**

- [x] **DONE cycle 2311 (BUILD slot, `2311%3==1`) -- closed the "hard-coded-null-subset" bug
      class fleet-wide by checking the 3 remaining unverified candidates; 0 defects, 0 code
      changes.** `google-news-scraper`: single upstream (Google News RSS, 3 URL shapes for
      query/topic/topic-hash, all the same feed) -- not a multi-source aggregator, no
      cross-source subset possible. `sam-gov-opportunities-scraper`: single upstream (sam.gov),
      3 different endpoints (search/detail/attachments) of the SAME API, not independent
      sources -- same verdict. `uk-find-a-tender-scraper` IS a genuine 2-source aggregator
      (Find a Tender + Contracts Finder, both OCDS) -- but its one asymmetric filter (`stages`:
      FTS's API only recognizes 3 of 5 OCDS stage values) already has a `CF_BLIND_STAGES`
      runtime warning (`src/main.js:39-50`) plus a dated README section disclosing it --
      i.e. this Actor already got the exact fix this bug class calls for, years before this
      hunt started. Grepped for any OTHER `source.key`-conditional branch in the file (rate
      limits, URL building, pagination, error messages) -- none affects field population or
      filter correctness, only operational behavior identical in effect across both portals.
      **Verdict: the bug class is fully exhausted fleet-wide** -- `ats-jobs-scraper` (c2308),
      `remote-jobs-scraper` (c2309) got fixes; `court-records-scraper`/`eu-ted-tenders-scraper`
      (single-upstream, c2309) and now `google-news-scraper`/`sam-gov-opportunities-scraper`
      (single-upstream) /`uk-find-a-tender-scraper` (already guarded) are all ruled out. Do not
      re-run this hunt without a new multi-source Actor entering the fleet.
      Checked `bin/checks-due`/`audit-due --all`/`--type varied_test --all` first: all NONE DUE.
      Inbox re-read in full (10 items, unchanged) -- the one owner reply (`dc593cfb`,
      2026-10-19, "Done" re: Apify identity verification) is already resolved:
      `website-screenshot-scraper` has lived in `registry.json` with a real `apify_actor_id`
      since before c2310 counted 25 public Actors. Nothing to answer, no new signal.
      $0 spent, 0 new Actors, 0 code changes, revenue unchanged (48 users, `bkmk`/`rev` 0/0),
      no owner email warranted. Services/site re-verified healthy (systemd active x3, `/` and
      `/tools` both 200), git clean before and after (nothing to commit from this cycle's
      investigation besides this STATUS.md/queue.md update).
      **Next BUILD-slot lever: none queued for the null-subset class (closed) -- default to a
      cold-read defect hunt on the next-oldest-touched Actor tier (c2307's method, last used
      successfully at c2308/c2309). Check `apify-admin store` output isn't needed; just pick
      2-3 Actors not cold-read recently and look for a different defect shape (not
      filter-blindness -- that axis is now exhausted) -- e.g. pagination edge cases, date-window
      math, or a dedupe gap.**

- [x] **DONE cycle 2307 (MANDATED QUALITY/GROWTH slot, `2307%3==0`) -- interim re-check of
      c2272's `/llms-full.txt` follow-up (still not due, window tightened to ~cycle 2320-2368)
      plus a cold-read defect hunt on `grants-gov-scraper` (oldest-touched Actor fleet-wide,
      0 defects -- already correctly guarded on the change-blind-filter bug class).**
      Nothing due (`checks-due`/`audit-due --all`/`--type varied_test --all` all NONE DUE),
      inbox unchanged, git clean and synced before edits, 0 Actors created today. Full details
      in `state/STATUS.md` cycle-2307 entry. $0 spent, 0 code changes, revenue unchanged (48
      users, `bkmk`/`rev` 0/0), no owner email warranted. **Next BUILD-slot lever: still none
      queued (niche-hunting + README-competitor exhausted c2302-2306) -- default to a cold-read
      defect hunt on the next tier of Actors (all last-touched 2026-10-25, listed in STATUS.md).**

- [x] **DONE cycle 2306 (BUILD slot, `2306%3==2`) -- repeated the `WebSearch`-for-new/
      deprecated-sources niche-hunting method (c1699/c1700), the one lever not re-run in
      600+ cycles; null result, lever downgraded to a calendar cadence.**
      Nothing due (`checks-due`/`audit-due --all`/`--type varied_test --all` all NONE
      DUE), inbox unchanged (same 10 known spam/DMARC/resolved items), git clean and
      synced before edits. Niche-hunting (10 keyword-category axes) and the
      README-competitor-section lever were both already declared exhausted fleet-wide
      by c2302-2305, and c1647 explicitly warns against hand-guessing another keyword
      axis from memory -- so this cycle picked up the one niche-hunting method not
      re-tried since c1700-1701 instead: `WebSearch` for newly-launched or
      newly-deprecated public APIs.
      2 searches ("new free public government API launched October 2026",
      "government API deprecated sunset 2026") returned **zero new candidates** -- the
      first converged on the exact same sources c1699/c1700 already found and closed
      (USAspending, FiscalData, Federal Register, openFDA, CDC, GBIF, USGS, World Bank,
      Census -- all already one of our 24 Actors or already scanned+closed in
      `NICHES.md`); the second surfaced only consumer-tech API sunsets (Google Fit,
      OpenAI, Meta, Microsoft SOAP) irrelevant to a scraping Actor, plus one NCBI
      sub-endpoint deprecation too narrow to be a buyer-facing gap.
      **Downgraded the lever's cadence from cycle-count to calendar-time**: c1699's
      "every ~50-100 cycles" assumed a much lower cycles/day rate than today's 48/day
      (`bin/checks-due`) -- 606 cycles is only ~13 calendar days, too short for
      genuinely new gov APIs to appear AND go unindexed by the same listicles already
      swept. **Do not re-run this specific WebSearch lever before ~2026-12-26** (~60
      real days out), and only then if no sharper signal (inbox request, `bin/traffic`
      spike, an organic find) has already surfaced something better. Full write-up in
      `notes/NICHES.md` cycle-2306 section.
      **Net: every niche-hunting axis this fleet has is now fully exhausted** (dataset-
      name guessing, WebSearch-for-sources, EU legal-mandate structural lever, paid/B2B
      anti-bot, CATEGORY-level, 10 keyword-category sweeps) with nothing left to try
      this cycle count. $0 spent (2 free WebSearch calls), 0 new Actors, 0 code changes,
      revenue unchanged (48 users, `bkmk`/`rev` 0/0, $0 booked), no owner email
      warranted. **Next BUILD-slot lever: none queued -- default to a cold read of 2-3
      Actors' README/source the fleet hasn't touched recently for a small honest defect
      or feature gap (c2296/c2297's shape), rather than re-deriving an exhausted lever.**

- [x] **DONE cycle 2304 (MANDATED QUALITY/GROWTH slot, `2304%3==0`) -- built the fleet
      declared-vs-exercised CHARGE-EVENT matrix and closed 2 of the 3 never-verified
      billing surfaces on `substack-scraper`, the fleet's biggest one. Both correct; 0
      defects, 0 code changes.**
      Nothing due (`checks-due`/`audit-due --all`/`--type varied_test --all` all NONE DUE;
      soonest `git-maintain` 2308, `competitor_audit` 2417, `varied_test` 2549), inbox
      unchanged (same 10 known spam/DMARC/resolved items, newest still `c2fa5a9c`),
      all 7 open follow-ups re-confirmed still correctly time-gated -- so I picked up
      c2264's open test-coverage thread instead of re-litigating them.
      **The sweep (free, local, authoritative):** declared events come from each Actor's
      `meta.json` `events` (the set `check-pricing` confirms against the platform), NOT
      from grepping `src/` -- a source grep misses Actors whose event name is a variable
      and reported 2 Actors as having 0 events. Result: **30 charge events over 24 public
      Actors, and only 3 Actors carry more than one** -- `grants-gov-scraper`
      (`result`/`opportunity-thin`, both verified live c2213 incl. a cross-contamination
      check), `shopify-products-scraper` (`result`/`productDetail`, verified c2264), and
      `substack-scraper` (**4 events** = 13% of all fleet billing surface) which had
      **zero live `chargedEventCounts` readings in its entire history** -- its
      `varied_test_note` mentions charging exactly once, and only as the fleet-wide
      STATIC `check-charges` pass. (c2264 estimated "~5 Actors carry a second event"; the
      real number is 3, and 2 were already closed, which is why this narrowed to one
      target.) **This corrects c2264's estimate -- do not go looking for the other 2.**
      **Why this one was the worst case, worse than c2264's shopify find:**
      `src/main.js:84` is `POST_EVENT = includeBodyText || includeBodyHtml ? 'result' :
      'post-metadata'`, and `bin/check-charges`' own docstring (line 31) says PASS 2
      "cannot see through the variable" on substack specifically. So the static check
      admitted it could not cover this branch and no live test ever did either -- the
      exact "a disclaimer is a queued bug report" shape from c2112, but on a *billing*
      branch. Compounding it: `includeBodyText` **defaults true**, so every past
      `varied_test` billed the premium `result` event and `post-metadata` could only ever
      fire on an explicit opt-out that nothing ever sent.
      **Both reads taken from `GET /v2/actor-runs/<runId>`** (never the runs-LIST
      endpoint, the c2184/c2208 trap) **and re-read 30s later** to rule out the c2224
      eventual-consistency lag -- byte-identical on both reads in both runs.
      (1) `post-metadata`: `includeBodyText:false`+`includeBodyHtml:false`,
      `maxPostsPerPublication:3`, `maxResults:3` -> 3 rows, `bodyText` correctly ABSENT
      from all 3 (opt-out honored; `varied-test` flagged it as NOT A FIELD rather than a
      null, which is the right reading), `chargedEventCounts {result:0, post-metadata:3,
      leaderboard-row:0, comment:0}`. **Branch is the right way round** -- the $0.00112
      event fires, the $0.002 one does not, so a customer who opts out of body text is
      not overbilled. 0 cross-contamination.
      (2) `leaderboard-row` (`src/main.js:708`, a separate code path):
      `leaderboardOnly:true` alone returned **0 rows** -- and that is NOT a defect, the
      run log names the exact fix ("leaderboardOnly requires discoverCategories --
      publicationUrls/postUrls are not used in this mode"), i.e. a clean
      `unreachable_remedy` pass found incidentally. Re-ran with
      `discoverCategories:["technology"]`, `maxPublicationsPerCategory:3`,
      `maxResults:3` -> 3 rows, rank 1/2/3, `chargedEventCounts {result:0,
      post-metadata:0, leaderboard-row:3, comment:0}`. Exact, 0 contamination.
      Recorded under a NEW `charge_event_verified` key in `state/audit_dates.json`
      (cycle 2304) **deliberately WITHOUT bumping `varied_test` (still 2225)** -- I ran
      charge verification, not a filter-combo rotation, and bumping it would have silently
      skipped a genuine audit. `check-charges` (25/0/0) and `check-pricing` (25 Actors /
      30 events / 0 drift) both clean after.
      3 runs, **$0.0004 total compute**, 0 builds, 0 new Actors, 0 code changes (nothing
      was broken), revenue unchanged (48 users, `runs30d` 762, `bkmk`/`rev` 0/0), no owner
      email warranted.

- [x] **DONE cycle 2305 (BUILD slot, `2305%3==1`) -- closed c2304's substack-scraper
      charge-matrix follow-up: the last 2 of its 4 charge events (`comment`, `result`)
      now have live `chargedEventCounts` readings, so all 30 fleet-wide charge events
      across 24 public Actors have been live-verified at least once.**
      Nothing due (`checks-due`/`audit-due --all`/`--type varied_test --all` all NONE
      DUE; soonest `git-maintain` 2308, `competitor_audit` 2417, `varied_test` 2549),
      inbox unchanged (same 10 known spam/DMARC/resolved items), git clean and synced
      before edits -- so picked up this well-specified top-of-queue item rather than
      re-attempting an 11th niche axis (10 already exhausted with 0 candidates each).
      Found a real Open Thread post live and free first (no spend): substack's own
      `/api/v1/archive` (astralcodexten.substack.com 301-redirects to
      www.astralcodexten.com -- noted for the next cycle that hits this Actor, the
      redirect is harmless since `parseTarget()` builds its own API URLs off `u.origin`)
      listed `open-thread-457` at `comment_count:104`; confirmed its post-detail API
      resolves (id 222234438) before spending anything.
      Used `bin/run-charged` (the c2226 settle-poll helper, not a one-shot read) on
      `{"postUrls":["https://www.astralcodexten.com/p/open-thread-457"],
      "includeComments":true,"maxCommentsPerPost":2,"maxPostsPerPublication":1,
      "maxResults":5}` -> SUCCEEDED, 3 rows (1 post + 2 comments, cap honored),
      `chargedEventCounts` SETTLED `{result:1, post-metadata:0, leaderboard-row:0,
      comment:2}` -- sum(charged)==rows==3, 0 cross-contamination with the other 2
      events c2304 verified. Read the 3 dataset rows directly, not just the count: a
      real post titled "Open Thread 457" + 2 distinct real comment bodies, not
      placeholders. This closes both the never-exercised `comment` event and the
      never-actually-READ default `result` path in one run.
      Recorded under `charge_event_verified` (now 2305) in `state/audit_dates.json`,
      prior c2304 note preserved under `charge_event_verified_note_c2304` -- edited via
      a targeted `json.load`/key-update/`json.dump` with `git diff --stat` checked
      immediately after to confirm no whole-file reformat (the c2291 lesson: a
      load+dump of a differently-indented file rewrites every line). `check-charges`
      25/0/0 and `check-pricing` 25/30/0 both clean after.
      ~$0.003 spent (1 capped run), 0 builds, 0 new Actors, 0 code changes (nothing was
      broken), revenue unchanged (48 users, `bkmk`/`rev` 0/0), no owner email warranted.
      **Next BUILD-slot lever: still an 11th niche axis** (c2303/c2304's handoff,
      README-competitor lever exhausted fleet-wide) -- this cycle's item was a genuine
      higher-priority finish-the-thread task, not a new lever, so the niche-axis default
      still stands for the next BUILD slot that has nothing else queued.

- [x] **DONE cycle 2303 (BUILD slot, `2303%3==2`) -- closed the README-competitor-section
      lever fleet-wide: checked c2302's 3 named candidates plus the 4 oldest
      `competitor_audit` Actors (7 total), found 6 already exhaustively current, and
      shipped a fresh sweep + 3 new disclosed rivals on the 7th, the genuine outlier.**
      `federal-register-scraper`/`nih-reporter-scraper`/`sec-insider-trades-scraper`
      (c2302's "oldest-verified" list) and `fec-campaign-finance-scraper`/
      `remote-jobs-scraper`/`eu-ted-tenders-scraper`/`ats-jobs-scraper` (oldest
      `competitor_audit` `last` cycles) all turned out already resweeped within the last
      ~4-18 days -- 0 new gaps on any of the 6.
      `us-federal-awards-scraper` was the real outlier: last competitor update cycle 1441
      (2026-10-09), 862 cycles/18 days, the longest gap fleet-wide. Full sweep
      (`niche-unnamed` + the Actor's own `_batch_price_ufaw.py`): niche grew 133->218
      matched listings, all 127 unnamed ones live-priced. **2 genuine new undercutters
      that beat even the page's previously-cheapest rival:** `lepidata/usaspending` (flat
      $0.0002/award, no start fee, contract/IDV/grant/loan scope) and
      `j0401/usaspending-awards` (tiered $0.00005->$0.00003, cheaper still but
      contracts-only). Plus `leadforge-data/federal-contract-leads` (free, no pricing
      record yet, 3 days old). Own price re-verified first, unchanged ($0.004/$0.0025).
      Added a dated README paragraph naming all three with scope caveats.
      Pushed build `0.1.83` (README-only, no publish-ordering trap), verified live via
      the build's own `readme` field (`GET /v2/actor-builds/<id>` through
      `taggedBuilds.latest.buildId`) -- all 3 new handles present. `check-registry-fields`/
      `check-code-fields`/`check-meta-fields`/`check-pricing`/`check-readme-samples` all
      clean after (0 drift). ~$0.005 spent, 0 new Actors, revenue unchanged (48 users,
      `bkmk`/`rev` 0/0), no owner email warranted.
      **Next BUILD-slot lever: README-competitor-section re-read is now exhausted
      fleet-wide** (nothing older than ~18 days remains, and that one is now closed).
      Default to an 11th niche axis next, since niche-hunting and this lever are both now
      exhausted on every angle tried so far.

- [x] **DONE cycle 2302 (BUILD slot, `2302%3==1`) -- cold README competitor re-read on 2
      Actors (0 gaps, already exhaustively swept) + a fresh 6-keyword niche sweep on a
      consumer-safety/legal-data axis (all below the ≥50 bar, 0 new candidates).**
      No fleet check/audit due. Tried c2301's named default first: cold-read
      `grants-gov-scraper` and `steam-reviews-scraper` (oldest README-modification dates,
      2026-10-23) for an unclosed feature/pricing gap -- both already carry exhaustive
      multi-pass competitor sweeps through cycle 2131-2134 (same date), every undercutter
      and gap already disclosed and priced live. 0 new gaps on these two specifically.
      Fell back to `bin/store-scan` on 6 never-tried keywords (CFPB consumer complaints,
      CPSC product recalls, NHTSA vehicle recalls, FDA drug shortages, state legislature
      bill tracking, patent litigation/court dockets): all 6 scored demand/competition
      0.7-1.0, all 6 showing the same clone-flood pattern (17-28 near-identical listings,
      mostly 2-3 users, `runs30d=0` fleet-wide on every listing in all 6 niches -- zero
      real demand anywhere). Full numbers in `notes/NICHES.md` cycle-2302 section so these
      6 phrases aren't re-probed. Niche-hunting now exhausted on 10 category axes.
      Also ran `bin/actor-health` as a fleet sanity check (not strictly due): all 24 live
      Actors `ok:true`, `fail_rows:0`.
      **Next BUILD-slot lever: pick a *different* 2-3 Actors' README competitor sections**
      (candidates by oldest competitor-verification mention, approximate --
      `federal-register-scraper`, `nih-reporter-scraper`, `scholarship-scraper`,
      `sec-insider-trades-scraper`, `us-federal-awards-scraper` -- see STATUS.md cycle-2302
      note on why this list is approximate) **or try an 11th niche axis** -- 10 are now
      exhausted (8 category axes + business-entity 9/9 + US-gov-open-data + intl registries
      + axis-5 + marketplaces/real-estate/legal/weather/academic + public-records/
      dev-tooling + consumer-safety/legal-data this cycle).
      $0 spent, 0 new Actors, 0 code changes, revenue unchanged (48 users, `bkmk`/`rev`
      0/0, $0 booked), no owner email warranted.

- [x] **DONE cycle 2301 (QUALITY/GROWTH slot, `2301%3==0`) -- closed c2300's README
      follow-up: fixed both stale self-claims and added the 5th `check-blog-claims` check.**
      `us-federal-awards-scraper/README.md` lines 221/223 "37 typed fields" -> **52**
      (confirmed not a defensible subset -- prime-only is 39, not 37 -- so pure staleness).
      `clinicaltrials-scraper/README.md` lines 7/157 "37 flat fields" -> **38**: resolved the
      membership question the item raised by reading the table in context -- it's introduced
      as "including the ones most ClinicalTrials.gov Actors skip," a deliberately curated
      subset (also missing `nctId`/`startDate`/etc, not just the 6 named fields), never meant
      to enumerate all 38 -- so the fix is the total plus rewording line 157's "what the field
      table above lists" (implied the table = the count) to "what this page documents."
      Added the 5th check to `bin/check-blog-claims` (README self-claims, reusing `reg`/`COUNT`,
      no `links_on()` needed since a README is already scoped to one slug): 8 claims checked,
      0 stale. Negative-tested per PLAYBOOK line 23 (reintroduced 37, confirmed STALE + rc=1,
      reverted, reconfirmed clean) and recorded via `checks-due --ran` (next due 2637).
      Pushed both Actors (builds 0.1.82/0.1.87) since the Store page server-renders the README;
      verified live via the latest build's own `readme` field over the API (not the CDN-cached
      page, not the Store index, which dropped `readme` per check-store-index's cycle-1408
      note) -- both show the corrected numbers. `check-registry-fields`/`check-code-fields`/
      `check-meta-fields`/`check-pricing`/`check-readme-samples` all clean after. ~$0.01 spent
      (2 builds), 0 new Actors, revenue unchanged (48 users, `bkmk`/`rev` 0/0), no owner email.
      **Next BUILD-slot lever: none currently queued** -- default to a fresh `apify-admin store`
      niche sweep (last run cycle 2299) or a cold README-competitor-section re-read (c2298's
      method).

- [x] **DONE cycle 2300 (BUILD slot, `2300%3==2`) -- ran the one due fleet check,
      `check-blog-claims`, and the interesting result was not its verdict but its own
      counter: it passed green while reporting "0 Actor field-count claim(s) checked".
      The check had been structurally blind for ~790 cycles. Fixed the blindness, then
      fixed the 3 real stale numbers it immediately exposed.**
      **Root cause (vocabulary drift, not a parser bug):** `links_on()` recognised only
      `/tools/<slug>` and `apify.com/fetchsmith/<slug>`, but blog product CTAs moved behind
      `/go/<slug>` in **cycle 1509** so out_clicks could be logged. Measured fleet-wide:
      **169+ `/go/` links vs 0 `apify.com/fetchsmith/`** -- that second form is now dead
      everywhere. Every field-count sentence in the blog happened to use `/go/`, so check 1
      matched nothing and still exited 0.
      **Shipped in `bin/check-blog-claims`:** taught `links_on()` the `/go/<slug>` form and
      de-duplicated check 1's inline copy of the same logic onto it (claims checked went
      **0 -> 5** for check 1 and **7 -> 17** for checks 2-3, which share the helper); switched
      the field-count truth from `len(output_fields)` to the **sellable (non-`_`) count**; and
      added a **4th check** covering `registry.json` summary field counts (3 claims checked).
      Docstring records both causes so the next reader sees why it was green.
      **3 stale customer-facing numbers found and fixed:** blog `fda-openfda-recall-json-api`
      "39 flat fields" -> **40**; blog `usaspending-federal-awards-json-api` "54 flat fields"
      -> **52**; and `registry.json`'s `us-federal-awards-scraper` summary "54 typed output
      fields" -> **52** -- that last one **self-healed the live tool page and `/llms-full.txt`
      with no restart**, since the app reads registry.json per request (verified by curl).
      **Convention settled (it was genuinely undecided):** only 3 registry summaries carry a
      field count and the two that discriminate **disagreed 1-1** (fda said 40 = non-underscore,
      us-federal-awards said 54 = raw total). Resolved to **exclude `_`-prefixed columns** on
      the READMEs' own evidence -- both document `_watchChangeType`/`_watchPrevious` as
      appearing *only on a `watchChanges` re-delivery*, off by default, so counting them
      overstates a default run. Not a majority vote: with 3 data points there was none.
      **Verified, per PLAYBOOK line 23:** negative-tested the new registry guard by
      reintroducing 54 (it printed STALE and exited non-zero), then reverted and re-confirmed
      green; the link fix proved itself by biting on 2 real blog lines. Site re-checked after
      edits: `/`, `/tools`, `/pricing`, both edited blog posts, the tool page, `/llms.txt` and
      `/llms-full.txt` all **200**, with 40/52 rendering live. Check recorded via
      `checks-due --ran` (next due 2636). 0 new Actors, $0 spent, revenue unchanged
      (48 users, `bkmk`/`rev` 0/0). No owner email warranted.
      **Next BUILD-slot lever: the README follow-up at the top of this file** -- READMEs are
      the one surface this bug class is still unguarded on, and 2 stale self-claims are already
      measured and waiting (incl. us-federal-awards understating itself by 15 fields in its own
      competitor comparison). Next fleet check: `git-maintain` (cycle 2308).
      Next `competitor_audit`: `website-screenshot-scraper` (cycle 2417).

- [x] **DONE cycle 2299 (BUILD slot, `2299%3==1`) -- no fleet check/audit due, no actionable
      queue item (all 7 open follow-ups time-gated), so ran c2298's named default: a fresh
      `apify-admin store` niche sweep, 10 keywords on a public-records/legal-filing +
      dev-tooling axis (UCC liens, bankruptcy filings, SEC 10-K filings, nonprofit 990s,
      business license lookup, lobbying disclosure, OSHA violations, EPA enforcement, npm
      package downloads, import/export trade data). All 10 below the d/c>=50 bar (best 4.9).
      4 of the 10 turned out to be an accidental partial re-run of cycle-2077 keywords
      (osha/business-license/nonprofit-990/epa) -- caught by grepping NICHES.md, numbers
      matched. The other 6 were genuinely new and are now logged in `notes/NICHES.md`
      (cycle-2299 section) with full numbers so they aren't re-probed. 0 new Actors, 0 code
      changes, $0 spent. **Next BUILD-slot lever: no niche/grep candidate remains -- default
      to re-reading 2-3 Actor READMEs' competitor sections cold (not grep) for a feature/
      pricing gap.** Full write-up in STATUS.md and NICHES.md.

- [x] **DONE cycle 2298 (MANDATED QUALITY/GROWTH slot, `2298%3==0`) -- no fleet check/audit
      due, so ran a fresh non-grep code-sweep across 5 Actors + the homepage hunting for
      feature/pricing/defect gaps. Found 0 defects -- every surface checked was already
      correctly implemented.** Checked: `steam-reviews-scraper`'s no-op filter warnings
      (`purchaseType`/`dayRange`/`includeOffTopic`, dead since the 2026-10-22 Valve API
      retirement) all fire correctly per README; `apple-podcasts-scraper`'s `chartGenre` +
      `chartType:"episodes"` interaction nulls+warns correctly; `hacker-news-scraper`'s
      milestone dead-rung guard (shipped c1572) still present; `nih-reporter-scraper`'s
      `minAwardAmount`/`maxAwardAmount` change-blind-filter guard still present; homepage
      "24 tools" vs `bin/revenue`'s "25 public Actors" looked stale but is NOT a bug --
      `registry.json` has 25 entries (24 `live` + 1 `retired`: `scholarship-scraper`) and
      `site/app.py`'s `public_tools()` correctly excludes the retired one, so 24 on-site vs
      25-in-registry are both correct for what they each measure.
      **Takeaway for future QUALITY slots: this fleet is now hard to find fresh code defects
      in by cold-reading alone -- every speculative gap tried this cycle had already been
      fixed in a prior cycle (change-blind-filter/dead-bound/watch_subset_audit classes are
      fleet-swept per c1560-1583; README "we do not offer" grep sweep exhausted c2058/2288-90;
      niche-hunting closed c2102).** $0 spent, 0 new Actors, 0 code changes, revenue unchanged
      (48 users, `bkmk`/`rev` 0/0). No owner email warranted.
      **Next BUILD-slot lever: none currently queued -- default to a fresh
      `apify-admin store "<niche>"` pass (respecting the 6-new-Actors/day cap) rather than
      re-deriving an exhausted lever.** Next fleet check: `check-blog-claims` (cycle 2300).
      Next `competitor_audit`: `website-screenshot-scraper` (cycle 2417). Next `varied_test`:
      `grants-gov-scraper` (cycle 2549).

- [x] **DONE cycle 2296 (NOT a QUALITY slot -- `2296%3==1`, so a BUILD slot) -- fixed c2295's
      `clinicaltrials-scraper` `stopReason` misclassification, and the fix turned out to be a
      MISSING CATEGORY, not a regex that needed narrowing.** Did what the item asked (re-measure,
      don't blind-patch) but did one thing first that changed the answer: **printed every row in
      the suspect `drug_or_supply_issue` category across BOTH measured samples before touching a
      regex.** 7 of the 22 rows there were equipment/instrument failures, not study-material
      availability ("Technical difficulty with Endo-PAT machine", "technical problems with
      equipment from the main outcome", "Study currently suspended due to device-related issues",
      "technical support not available", "technical issues", "Technical issues in testing
      procedure", plus c2295's laser-device row) -- **a third of the category was wrong, so the
      anecdote was a symptom, and either fix the item proposed (narrow the branch, or move the
      bare forms into `logistical_or_operational`) would have mislabelled those 7 rows a second
      time.**
      **Shipped:** a 9th category `device_or_technical_issue` in `WHY_STOPPED_RULES`, ordered
      BEFORE `drug_or_supply_issue` so an equipment failure wins over the supply reading, and
      deliberately NOT matching a bare "device" noun so genuine supply text still classifies as
      supply. Moved `device[- ]related issue`, `equipment failure|issue`, and the bare
      `technical (difficulty|problem|issue|support)` forms out of `drug_or_supply_issue`, plus
      `technical\s+difficulty` out of `logistical_or_operational` (now covered earlier, so
      `stopReasons` no longer double-lists it). No new field, no field-count change (still 37).
      **Re-measured as the item required, on re-pulled samples:** the ClinicalTrials.gov API
      returns the same first two pages per status, so the pull reproduced c2291's samples exactly
      (269 tuning / 276 holdout, 0 overlap) and reproduced c2291's baseline numbers to the decimal
      (88.5% / 82.2%) -- which is itself the proof the measurement harness is sound. After the
      split: **coverage UNCHANGED at 88.5% tuning / 82.2% holdout** (a relabel adds no matches)
      and **exactly the 7 intended rows changed category, 0 collateral relabels** anywhere else
      in either sample.
      **Verified live on the platform, not just locally:** build `0.1.86`, then a real run on the
      7 moved NCT IDs plus `NCT05618093` ("Study device no longer available") as a deliberate
      CONTROL. Read back via the Datasets API: 8/8 rows, all 7 now `device_or_technical_issue`,
      and the control still `drug_or_supply_issue` -- i.e. the split cut where intended.
      Claim sites updated: README field table (8 -> 9 categories, the split dated and explained,
      and the sample description corrected from "two independent 300-row live samples" to "300
      studies each, 269 and 276 of which carry `whyStopped` text") and
      `.actor/input_schema.json`'s `includeStopReason` description. `check-registry-fields`/
      `check-code-fields`/`check-meta-fields`/`check-pricing`/`check-readme-samples` all clean
      after; `check-store-index` 0 stale (meta.json title/description untouched, so no reindex --
      and for once the publish-order trap did not apply, because there was no copy change to
      publish). Also ran both due fleet checks: `check-cta-presence` CLEAN, `sync-apify-prices`
      CLEAN (25 tools, 25 live prices, 0 updated), both recorded (next due 2632).
      ~$0.01 spent (1 build + 1 short run), 0 new Actors, revenue unchanged (48 users, `bkmk`/
      `rev` 0/0), no owner email warranted.

- [x] **DONE cycle 2297 (BUILD slot, `2297%3==2`) -- resolved c2294's openFDA query discrepancy
      AND shipped `firmRecallCount` on `fda-recall-scraper`, closing the repeat-offender-firm gap
      the README named since 2026-10-03.** Diffed the aggregation instead of guessing: on "Pfizer
      Inc.", `search=recalling_firm:"Pfizer Inc."` returns 120 but `count=recalling_firm.exact`
      buckets the literal string at 111; 111 + 5 ("Pfizer Inc") + 2 ("PFIZER INC") + 2
      ("PFIZER, INC") = 120 exactly -- the quoted `search=` clause normalizes case/punctuation and
      folds distinct literal spellings together, it is not a strict phrase match.
      `search=recalling_firm.exact:"<firm>"` (the `.exact` suffix INSIDE the search clause) returns
      111, matching the hand-countable bucket -- that's the form shipped.
      **Implementation:** `firmRecallCount(productType, firm)` in `src/main.js`, one extra openFDA
      request per unique `(productType, recallingFirm)` pair seen in the run, cached so a repeated
      firm costs one lookup; respects the existing `timeBudgetOk()` guard (degrades to `null`, never
      fails the run) and warns once per run on any lookup failure rather than spamming the log.
      `normalize()` is now async to await it; both call sites (the watch-changed path and the
      normal path) updated to `await`. New `includeFirmHistory` input, **default `false`** (not
      `true` as this item originally proposed) -- unlike `includeRiskScore`/`includeRootCause`
      (pure local regex, zero network cost), this is a real extra HTTP request per firm, so
      defaulting it on would silently add latency to every existing scheduled/watch-mode run on
      upgrade; same reasoning `includePressReleases` already uses for its own default-`false`.
      Field count 39 -> 40; all five claim sites updated (`registry.json` output_fields + summary,
      `.actor/dataset_schema.json`, `.actor/input_schema.json`, `.actor/actor.json`, `meta.json`,
      README field table + FAQ entry + the repeat-offender competitor paragraph, now stating the
      gap is closed and explaining the `.exact`-vs-plain-search mechanism). `check-registry-fields`/
      `check-code-fields`/`check-meta-fields`/`check-pricing`/`check-readme-samples`/
      `check-filter-reach` all clean after (0 drift).
      **Verified live, not just locally:** `apify-admin publish` run FIRST (copy changed), then one
      `apify push --force -w 600` (build `0.1.79`, SUCCEEDED) cleared the reindex debt in the same
      build -- `check-store-index` 0 stale. Real API run (`recallingFirm` left unfiltered to avoid
      the exact-search-is-lossy trap this item itself just found) returned rows reading
      `recallingFirm: "PFIZER INC"` with `firmRecallCount: 2` and rows reading
      `recallingFirm: "Pfizer Inc."` with `firmRecallCount: 111` -- both match their own exact
      aggregation bucket from the probe above, proving the per-row count tracks the row's own
      spelling, not a merged "Pfizer" lump. LEARNINGS cycle-2297 entry added (reusable lesson: when
      a search API's "exact phrase" and its own aggregation/count disagree, diff the aggregation's
      buckets for near-spellings before trusting either number).
      ~$0.005 spent (1 build + 1 short run), 0 new Actors, revenue unchanged (48 users, `bkmk`/
      `rev` 0/0), no owner email warranted.

- [x] **DONE cycle 2293 (NOT a QUALITY slot -- `2293%3==1`, so a BUILD slot) -- picked up c2292's
      named next lever: shipped a first-10-reviews-free tier on `app-store-reviews-scraper`,
      matching `reviewbot/apple-review-scraper` (43 users), the only rival our own README named as
      cheaper than us (below 10 reviews/run).** This closes a gap c2290 explicitly left open as "a
      pricing decision, not a code fix" -- it turned out to BE a code fix (a free-count threshold in
      the charging path), not a Store pricing-tier change, so no owner/budget question was actually
      needed; CLAUDE.md rule 4 (the $300 spend budget) doesn't apply to our own product's pricing
      structure, only to real money we spend.
      **Implementation:** `FREE_REVIEWS_PER_RUN = 10` in `src/main.js`'s `chargeAndPush()` -- skips
      `Actor.charge()` for the first 10 pushed rows of a run (PPE mode only), charges normally from
      row 11. Counts delivered rows, not scanned/filtered ones, so filtered-out reviews never burn
      the free count. No new input field, no schema change.
      **Verified live, not just locally:** pushed build `0.1.112`, then `apify-admin publish` for
      the new meta.json description (298/300 chars, added "first 10 free"), which printed
      `REINDEX REQUIRED` -- build `0.1.113` cleared it (`check-store-index` 0 stale). Ran a real
      15-review test call (`maxResults:15`) and read the run back via the API: `DATASET_WRITES: 15`
      but `chargedEventCounts: {"result": 5}` -- exactly rows 11-15 billed, rows 1-10 free,
      `usageTotalUsd` $0.0004. README updated in three places (intro line, Pricing section, the
      `reviewbot` competitor paragraph, now reworded from "which we do not offer" to "we matched
      this 2026-10-26 -- exact parity at every run size"). `check-meta-fields`/`check-pricing`/
      `check-readme-samples` all clean after. `node --check` clean.
      **Repeated the exact publish-order mistake LEARNINGS already documented from c2288 (pushed
      code before publishing the copy change, needed a second build) -- see LEARNINGS cycle-2293
      entry for why documenting it once wasn't enough and the sharper rule going forward.** Cost
      ~$0.01 total (2 builds + 1 short run), 0 new Actors, revenue unchanged (47 users, $0 booked),
      no owner email warranted. Commit `a505dc88`, pushed to `origin/main`.

- [x] **DONE cycle 2292 (MANDATED QUALITY/GROWTH slot -- `2292%3==0`) -- ran ALL 3 due fleet
      checks (`check-row-floor`, `check-upstream-warnings`, `check-doc-size`), all 3 now CLEAN,
      and acted on the two that asked for action.** $0 spent (no build, no run).
      **(a) `check-row-floor` CLEAN** -- 24 live Actors, all >=60% of requested cap, none
      declined from own observed best.
      **(b) `check-upstream-warnings` CLEAN (+3 acked)** -- 23 niches, 10601 listings / 5612
      in-niche. ONE new flag: `pinkish_gallop/steam-reviews-scraper` advertises "Valve's
      official **IUserReviewsService** API (the replacement for the retired `appreviews`
      endpoint)", which looked like a real capability gap against our HTML path (c2129).
      **Probed it live rather than guessing: HTTP 401 `verify your key= parameter`, and
      `IUserReviewsService` is absent from the keyless `GetSupportedAPIList/v1` (27
      interfaces) -- real but KEY-GATED, and we hold no Steam Web API key. Params take BOTH
      `request[appids][]` and `request[steamids][]` = per-(user,app) lookup, not an app-wide
      review feed, so not a drop-in `appreviews` replacement for anyone.** Re-verified our
      `src/` has no `appreviews` call site (only still-live `appreviewhistogram`). No code
      change warranted; acked with the probe result in the note. Lesson in LEARNINGS.
      **(c) `check-doc-size` read TRIM SOON on BOTH live docs -> trimmed BOTH proactively,
      which is exactly what its own advice (c2220) and c2268's script predicted for 2292.**
      STATUS.md 131.7KB/369 lines -> **22.2KB** keeping the contiguous window 2288..2291
      (blocks were strictly newest-first 2291..2262, asserted, so every prefix was hole-free
      for `check-status-continuity`); queue.md 88.9KB/1087 lines -> **14.9KB** via HOIST-THEN-CUT
      (an open item sat at line 97, buried between the second 2289 block and the 2287 block --
      a naive line cut would have deleted live work), keeping the DONE prefix matching the
      STATUS window plus **all 7 open items hoisted verbatim, 0 archived as closed**.
      **RATES re-measured rather than re-derived, as c2268's scripts asked, and they diverge
      in OPPOSITE directions -- worth knowing before the next trim: the checker runs ~9% COOL
      on STATUS.md (4.83KB/cycle actual vs 4.40 estimated) and ~81% HOT on queue.md
      (2.93 actual vs 5.31 estimated; four measurements now agree on 2.9-3.9KB/cycle).**
      Keep-4 on STATUS was chosen because keep-5/6 projected only 7.5/3.8KB under the 150KB
      warn line and keep-7 crossed it -- the c2284 block alone is 10.3KB, so one heavy cycle
      closes a margin that thin (the cycle-1976 mistake). 6 lossless verifications per script
      before writing, plus an independent re-verification afterwards: 0 original non-blank
      lines missing from live+addition on either file, prior archives byte-identical.
      `check-doc-size` re-run reads OK on all three docs; `check-status-continuity` NONE
      MISSING. Scripts kept at `bin/_trim2292.py` / `bin/_trim2292q.py`.

- [x] **DONE cycle 2290 (NOT a QUALITY slot -- `2290%3==1`) -- swept the 11 README gaps
      not yet triaged by c2288/c2289's "we do not offer/claim" method; found and shipped one
      real CODE gap, found one real but non-code pricing gap (left open), ruled the rest out
      as pricing-honesty prose.** `clinicaltrials-scraper` README:151 (written 2026-10-03)
      named `datalayer/clinical-trials-failure-intel` as classifying the `whyStopped` free
      text on terminated studies, "a field we return raw" -- except `src/main.js` never read
      `protocolSection.statusModule.whyStopped` at all; the README's own comparison was
      flat-out wrong, not just missing a classifier. Verified live against
      `clinicaltrials.gov/api/v2`: real sponsor free text, populated on 43-46/50 TERMINATED/
      WITHDRAWN/SUSPENDED studies, 0/50 RECRUITING/COMPLETED. Shipped the RAW field only
      (`whyStopped: status.whyStopped ?? null`), 34 -> 35 flat fields; updated
      `registry.json`/`dataset_schema.json`/README to match. `check-registry-fields`/
      `check-code-fields`/`check-meta-fields`/`check-pricing`/`check-readme-samples` all
      clean. Verified on the platform: build `0.1.84`, live TERMINATED-filtered run returned
      5/5 real `whyStopped` values via the Datasets API. ~$0.005 spent, 0 new Actors, revenue
      unchanged. Commit `54b2c528`, pushed.
      **Second finding, NOT actioned (business decision, not a code fix):**
      `app-store-reviews-scraper` README:424-426 names `reviewbot/apple-review-scraper`'s
      first-10-reviews-free tier as something "we do not offer" -- true, and closable only by
      changing our own Apify pricing tiers (CLAUDE.md rule 4 budget check first), not by
      shipping code. Left for a future cycle to weigh, not forgotten.
      Other 9 Actors' matches (`google-play-reviews`, `eu-ted-tenders`, `grants-gov`,
      `clinicaltrials`' OTHER paragraphs) were all "what we do not claim" pricing-honesty
      disclosures, not gaps -- no action needed, confirming the README grep sweep itself is
      now exhausted a second time (c2058/c2288/c2289/c2290) until a new README paragraph is
      written.

- [x] **DONE cycle 2291 (NOT a QUALITY slot -- `2291%3==2`, so a BUILD slot) -- shipped the
      `whyStopped` CLASSIFIER (`stopReason`/`stopReasons`) on `clinicaltrials-scraper`,
      mirroring `fda-recall-scraper`'s `ROOT_CAUSE_RULES` shape exactly.** 8 categories
      (safety_or_adverse_event, lack_of_efficacy, drug_or_supply_issue, covid_19,
      low_enrollment, administrative_or_sponsor_decision, funding_or_business,
      logistical_or_operational) plus honest `other`; `includeStopReason` input, default true.
      **Real holdout measured**: 269 tuning rows / 276 independent holdout rows pulled live
      via `pageToken` paging (share zero rows). First pass 73.6% tuning -> generalized ->
      88.5% tuning, but only **66.3% cold on holdout** (real overfit, same shape as
      fda-recall's 100%->80%). Read holdout misses, did ONE correction pass (never re-tune
      past one holdout read), landed **82.2% holdout** (88.5% tuning unchanged) --
      **genuinely lower than fda-recall's 96.3%**, reported as such in README/input schema:
      `whyStopped` sponsor free text is far more one-off/narrative than openFDA's
      `reason_for_recall`, not a weaker rule set. Field count 35 -> 37; all five claim sites
      updated (incl. a stale "34 flat fields" at README:157 that c2290 had missed) plus the
      `datalayer/clinical-trials-failure-intel` competitor paragraph reworded to note both
      the raw field and the classifier shipped 2026-10-26. `check-registry-fields`/
      `check-code-fields`/`check-meta-fields`/`check-pricing`/`check-readme-samples` all
      clean. Verified on the platform: build `0.1.85`, live `overallStatus:TERMINATED` run
      returned 5/5 rows with correct, sensible `stopReason`/`stopReasons` via the Datasets
      API. ~$0.005 spent, 0 new Actors, revenue unchanged. Commit `2a6036ba`, pushed.
      **Process lesson for any future registry.json edit:** do NOT `json.load`+`json.dump`
      the whole file to insert one field -- a first attempt here reformatted all 2370 lines
      (different indent width), caught via `git diff --stat` before committing and reverted
      with `git checkout --`. Use a surgical text `Edit` on the exact lines instead.

- [x] **DONE cycle 2288 (NOT a QUALITY slot -- `2288%3==2`, so a BUILD slot) -- shipped
      `rootCause`/`rootCauses` on `fda-recall-scraper`, closing a CODE gap this Actor's own
      README competitor section had named in writing since 2026-10-03 and nobody had acted on.**
      `datalayer/fda-recall-enforcement` classifies openFDA's free-text `reason_for_recall` into
      root causes; our README said in as many words that this was "a genuine analytical field we
      do not offer at all" and that `riskScore` "never parses *why* the recall happened". Built
      `ROOT_CAUSE_RULES` in `src/main.js`: an ordered, first-match-wins list of **published
      regexes** (no model call, no network, deterministic -- CLAUDE.md rule 2), 19 categories plus
      an honest `other`; `rootCause` = primary cause, `rootCauses` = every match (recalls commonly
      have several). New `includeRootCause` input, default true. Press-release rows classified too.
      **Measured with a real holdout: 100% on the 300 tuning rows but only 80.0% on 300 holdout
      rows (`skip=2000`) on the first pass** -- generalized the one-off rules, fixed a bare
      `\blead\b` false positive ("may *lead* to wound exploration" -> chemical_contamination),
      re-measured **96.3% holdout**. All buyer-facing copy quotes 96.3%, not 100%.
      Field count 37 -> 39 in all five claim sites; `check-meta-fields`/`check-registry-fields`/
      `check-code-fields`/`check-pricing`/`check-filter-reach` all 0 drift after. Verified on the
      platform: build `0.1.78`, live run 12/12 rows at 39 fields, correct `rootCause` on every row.
      ~$0.01 spent (2 builds + 1 run), 0 new Actors, revenue still $0 (`bkmk`/`rev` 0/0, 47 users).

- [x] **DONE cycle 2289 -- `bin/check-store-index` re-run cleared the ONE pending reindex on
      `fda-recall-scraper`.** `0 stale field(s)`, `state/pending_reindex.json` now `{}`. No push
      bought -- exactly the "just re-run the check" path this item prescribed.

- [x] **DONE cycle 2289 -- both un-triaged c2288 README gaps resolved, read-only + one README edit
      each, no model-based classification, no PII built.** (a) `sec-insider-trades-scraper`:
      fetched `jweninger16/insider-trading-monitor`'s live public record
      (`/v2/acts/jweninger16~insider-trading-monitor`, checked 2026-10-26) instead of guessing.
      Its `readmeSummary` claims only human transaction-type labels (no all-20-code decoding
      claim), a "computed transaction dollar value" with no claim it's signed, and never mentions
      a 10b5-1 flag at all -- so our fidelity differentiator holds on all three points. Bonus
      finding: its own `publicActorRunStats30Days` shows 3 runs in the last 30 days, **0
      succeeded, 3 FAILED** -- the "$0 beats us at any volume" framing undersells that the free
      rival may not currently return any rows. README:251 rewritten with both findings, cited and
      dated. (b) `apple-podcasts-scraper`: `scrapesage`'s `host_contacts` enrichment is host
      emails/phones -- personal data about individuals -- so per CLAUDE.md rule 1 this is
      correctly a closed, deliberate non-build, not an open gap. README:190 reworded from "a field
      we do not offer at any price" to state the PII reason and that it's closed, not pending.
      Both Actors pushed (README-only, no meta.json/field changes, no reindex triggered since
      title/description untouched): `sec-insider-trades-scraper` build `0.1.62`,
      `apple-podcasts-scraper` build `0.1.102`, both SUCCEEDED. `check-readme-samples` and
      `check-price-superiority` re-run clean fleet-wide after (0 drift, 0 undisclosed). ~$0.01
      spent (2 pushes), 0 new Actors, revenue unchanged.

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

- [ ] **NEW follow-up (c2272, RE-CHECKED interim at c2307 -- still NOT due, window tightened)
      -- check whether anything actually FETCHED `/llms-full.txt`, and only then expand it
      further.** This is the honest test of the c2272 change and it is cheap (no network,
      read-only). Run: `python3 - <<'EOF'` over `/var/log/caddy/fetchsmith.access*` (gzip +
      plain, `json.loads` each line, filter `'llms-full' in line`, print ts/status/User-Agent);
      **ignore `curl/8.5.0` rows, those are our own probes.**
      **c2307 interim result: 12 lifetime requests, only 1 non-curl (`agentcensus-crawler/1.0`,
      ts 1792882360 = 2026-10-24 22:52, BEFORE the file shipped -- same hit c2272 already
      counted, NOT a new one). 0 new external hits, 0 real 200s from anything but our own
      probes, 17.6h after shipment (c2272 commit 2026-10-26 09:36 UTC).** That is short of the
      "~1-2 days" window c2272 specified (~cycle 2320-2368 at 48 cycles/day) -- do NOT close
      this item before cycle ~2320, even though the signal so far is consistent with "nothing
      fetched it."
      **If real non-curl agents are fetching it 200 by then:** the next expansion is guide
      BODIES (the 88 posts, 860KB of markdown) -- `_parse_post` currently keeps only rendered
      `html`, so that needs the raw `body` retained in the cache (~860KB more RSS, acceptable
      on 2GB but measure `systemctl status fetchsmith-web` RSS before/after).
      **If still nothing by cycle ~2320+:** do NOT expand it further and do not keep
      re-checking -- record that result and treat the llms.txt family as done at this size,
      since the cost of a bigger file is real and the measured benefit would be zero.

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

