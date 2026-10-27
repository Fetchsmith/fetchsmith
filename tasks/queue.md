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

