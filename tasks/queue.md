- [x] **DONE cycle 2432 (QUALITY/GROWTH slot, `2432%3==2`) -- fixed `uk-find-a-tender-scraper`
      (build 0.1.91, package 0.1.17 -> 0.1.18) AND did the read-only measurement pass the c2428
      note asked for on the other 5 Actors, so the remaining fixes are now pre-measured.** This
      Actor was the worst of the 6 remaining: `blankDropNote()` was appended OUTSIDE the clamp on
      all 4 status branches, and the `!complete` branch had no clamp at all. Measured before
      touching anything: the no-match `zeroRowMessage` is 490 chars and is itself ALREADY clamped
      to the 500 ceiling, so a 3-field note (166 chars; `cpvCodes`/`keywordsAny`/`regions` are the
      3 blank-droppable fields) rendered 656 and shipped cut at exactly 500 with the note gone --
      even a 1-field note (103) rendered 593. The unclamped `!complete` branch measured 598 on a
      source-failed seeding run (`lastError` is sliced at 120 so that detail is bounded).
      Fixed with c2428's exact pattern: `clampStatusMessage(msg, suffix='')` reserving
      `STATUS_MESSAGE_MAX - suffix.length`, with all 4 call sites now routing through
      `clampStatusMessage(base, blankDropNote())`. Verified on 4 local runs (clean regression,
      3-field note on the zero-match branch -> 485 chars with the ` ...` marker and the note whole,
      1-field note variant -> also clamped and intact, 16-real-row delivered-branch at 144 chars
      untouched) + a standalone unit test of the unclamped `!complete` worst case (598 -> 499,
      note intact, and the no-suffix call is a byte-identical passthrough) + 1 real platform run
      (`xJRKfND6kyfUzyCFo`): `statusMessage` read back live at **485 chars** (so the platform did
      NOT truncate), note whole, `chargedEventCounts {result:0}` == pushed(0), 0 leak.
      `check-charges` 25/0/0, `check-registry-fields` 0 drift. README blank-entry FAQ now carries
      the 656/598 numbers and the "the note is reserved, the explanation is what gets shortened"
      rule. The log keeps the full unclamped text on every branch, as before.

- [x] **DONE cycle 2433 (normal slot, `2433%3==1`) -- fixed `fec-campaign-finance-scraper`, item
      (1) of the c2432 sweep (the only remaining Actor with a measured over-500 case AND no clamp
      reservation), build 0.1.83 (package 0.1.27 -> 0.1.28).** Ported federal-register-scraper's
      `Math.max(...,0)`-floored `clampStatusMessage(msg, suffix='')` onto the 4 watch-mode call
      sites (main.js ~1234/1249/1263/1272), each refactored to pass base prose as `msg` and
      `truncationNote() + (watchPastDateBound ? pastNote : '')` as `suffix`. No `echoCap` needed on
      `watchLabel` (unlike federal-register's suffix-side fix) since the unbounded label is in the
      BASE here, already protected by the base-truncation path. Verified: unit test reconstructing
      c2432's measured 650-char worst case (clamped to 482, suffix intact); 4 local runs against
      the live FEC API, including one where **the clamp fired for real** (539-char combined
      base+suffix on a fresh nothing-new incremental run -> 495 chars, NOTE intact) and a
      regression on the pre-existing default-suffix call site (byte-identical); 2 real platform
      runs reproducing the same case (`UE9Y2uQybsp6MDvMA` seed, `4H8jeAIRWXgrCRNhq` incremental) --
      `statusMessage` read back live at 497 chars, NOTE intact, `chargedEventCounts {result:0}` ==
      pushed(0), 0 leak. Did not force a live repro of sites 3/4 (pushed>0-with-incomplete) --
      covered by the unit test + identical-function argument instead, see `state/STATUS.md` cycle
      2433 for the full caveat. README FAQ entry added, confirmed in the live build's
      `actorDefinition.readme`. `check-charges` 25/0/0, `check-registry-fields` 0 drift. ~$0.005
      spent, 0 new Actors, no owner email warranted. **4 Actors left in the sweep**, unchanged from
      c2432's measurement, below.

- [x] **DONE cycle 2434 (normal slot, `2434%3==1`) -- fixed `nih-reporter-scraper`, item (1) of
      the sweep, build 0.1.64 (package 0.1.17 -> 0.1.18).** Re-scoped on inspection: only ONE call
      site (the `pushed===0 && !seeding && watchMode` branch, formerly ~1453) actually appends both
      `blindNote()`+`truncationNote()` inside a clamp -- the ~1401/1409 sites the earlier measurement
      named are plain `log.info` lines, never clamped, same as the rest of the fleet. Ported the
      `fec-campaign-finance-scraper`/c2433 reserving `clampStatusMessage(msg, suffix='')`, no
      `echoCap` needed on `watchLabel` (it's in the base, not the suffix, same reasoning as c2433).
      Verified: unit test reconstructing the 446-char combined-note worst case against an 80-char
      `watchLabel` (619 total) -- new clamp kept the full suffix, old append-after-clamp code would
      have dropped `truncationNote()` entirely (computed for comparison, not run live); 3 local
      runs against the live NIH RePORTER API (seed -> incremental on the same watchLabel+
      activeOnly+watchChanges, forcing `blindNote()` for real -> 285-char message, note intact;
      plain zero-match regression untouched); 1 real platform run reproducing the live case (seed
      `hfjTPICay6JJcQJws`, incremental `upVR5h05fGqGrY63Q`) -- `statusMessage` read back at 285
      chars, `chargedEventCounts {result:0}` == pushed(0), 0 leak. Did NOT force a live repro of
      `truncationNote()` specifically (`WATCH_KEEP=60000`, impractical in a cycle budget, same
      constraint c2433 hit) -- covered by the unit test's exact reconstruction instead.
      `check-charges` 25/0/0, `check-registry-fields` 0 drift. README FAQ sentence extended with
      the reservation guarantee, confirmed live. Full writeup in `state/STATUS.md` cycle 2434.

- [ ] **IN PROGRESS (c2428 -> c2429, c2430, c2431, c2432, c2433, c2434) -- the clamp-reservation
      sweep, 3 Actors left, ALL PRE-MEASURED by c2432 (do NOT re-derive these numbers, and do NOT
      re-run the triage grep).** 7 fixed so far: `sec-insider-trades-scraper` (c2428, reference impl
      at `actors/sec-insider-trades-scraper/src/main.js:543-560`), `sam-gov-opportunities-scraper`
      (c2429), `federal-register-scraper` (c2430), `hacker-news-scraper` (c2431),
      `uk-find-a-tender-scraper` (c2432), `fec-campaign-finance-scraper` (c2433, reference impl for
      the "unbounded field is in the BASE not the suffix, so no separate echoCap needed" variant at
      `actors/fec-campaign-finance-scraper/src/main.js:1114-1123`), `nih-reporter-scraper` (c2434,
      same reference pattern, impl at `actors/nih-reporter-scraper/src/main.js:965-974`). Remaining,
      in the order to take them: **(1) `clinicaltrials-scraper` -- same inside-the-clamp shape.**
      `truncationNote()` 183, `lookupShortfallNote()` **345 at its 5-part worst case** (5 independent
      id buckets: notFound/malformed/failed/notReached/badFormat), both inside the clamp at
      ~1595/1619. NOTE the source comment at ~1593 claims truncationNote and the shortfall note
      "can never both be non-empty" -- VERIFY that claim with the actual branch logic before sizing
      the fix (c2434 found the prior measurement's call-site line numbers for `nih-reporter-scraper`
      were imprecise -- re-read the real call sites here too, don't trust ~1595/1619/1603 blindly),
      because 345 alone already leaves only 155 chars for the base if the claim is wrong. Also one
      genuinely unclamped site at ~1603 (`+ truncationNote()`).
      **(2) `fda-recall-scraper` and (3) `grants-gov-scraper` -- LOWEST priority, possibly
      no-change.** Both share the same short `truncationNote()`, measured **98 chars**, and
      `grants-gov-scraper` ALREADY does the reservation correctly (`withIgnored` at main.js:1537
      passes `STATUS_MESSAGE_MAX - ignoredSuffix.length`) for its `ignoredSuffix`; its
      `truncationNote()` is composed into the base, not appended after it. Measure each one's
      actual base before writing a diff: a 98-char note against bases that look well under 400
      may be a case where the honest answer is "no change needed", and a diff is not free (c2219).

- [x] **DONE cycle 2431 (normal slot, `2431%3==1`) -- continued the c2428 clamp-reservation sweep,
      fixed `hacker-news-scraper` (the Actor c2430 flagged "no clamp at all, pick this one next"),
      build 0.1.94 (package 0.1.22 -> 0.1.23).** Different shape from the other 3 sweep fixes so
      far: no single `*Note()` suffix exists here -- two branches build their whole message by
      joining several independently-unbounded `stringList` inputs (`queries`/`usernames`/
      `excludeKeywords`/`domainFilter`, none capped in the schema), and two more echo `watchLabel`
      (free-text, no `maxLength`) as the SOLE dynamic content. Ported the fleet's
      `STATUS_MESSAGE_MAX`/`clampStatusMessage(msg, suffix='')` into all 5 call sites, plus
      `echoCap(watchLabel, 60)` on the two watch-baseline branches (the overall clamp already
      protects the two joined-causes branches, so left those un-per-field-capped on purpose).
      Verified on 4 local runs (short clean regression; 15 long empty queries forcing the clamp to
      482 chars with the ` ...` marker; long `watchLabel` on both the seeding and nothing-new
      branches, each echoCap'd to 60 chars while the full label still keys the real watch record)
      + 1 real platform run (`3ou7F0BpC1u2hh1Eu`): `statusMessage` read back live at 482 chars
      matching the local run, `chargedEventCounts {result:0}` == pushed(0), 0 leak.
      `check-charges`/`check-registry-fields` both clean. README FAQ entry added. Also re-verified
      both owner inbox threads (`dc593cfb`, `2b237f1b`) by reading them in full -- both genuinely
      long-resolved (CourtListener token wired since c2362). **6 Actors left in the sweep, all
      already have SOME clamp per c2430's count** (`clinicaltrials-scraper` 5 sites,
      `fda-recall-scraper` 3, `fec-campaign-finance-scraper` 1, `grants-gov-scraper` 2,
      `nih-reporter-scraper` 1, `uk-find-a-tender-scraper` 2) -- measure worst-case length before
      assuming any needs a code change; none is pre-flagged "no clamp at all" like the last 4 were.

- [x] **DONE cycle 2426 (QUALITY/GROWTH slot, `2426%3==2`) -- closed the partial-bad-seed /
      warning-only-disclosure sweep on its LAST Actor, `court-records-scraper` (build 0.1.72).**
      Re-scoped per the c2413 note (`courts` array, not `query`, is the seed-like field). Found
      `unknownCourts` (an invalid court slug) was `log.warning`'d but never reached
      `setStatusMessage`/`RUN_SUMMARY` -- a run mixing one typo'd court id with a real one pushed
      rows and looked clean. Fixed with the established `truncationNote()`-style suffix pattern:
      `unknownCourtsNote()` appended to all 3 existing status branches + a NEW 4th branch for the
      previously-silent clean-complete-run case, and `unknownCourts` always an array in
      `RUN_SUMMARY`. Verified on 4 local runs (incomplete+bad-id, clean-complete+bad-id = the new
      branch firing, clean regression, all-unknown zero-row) + 1 platform run (`rKWcM8meqoSpFynY5`,
      `statusMessage` carrying the NOTE, `chargedEventCounts {result:1}` == pushed, 0 leak).
      README input-table row + new FAQ entry. `check-charges`/`check-registry-fields` both clean.
      `package.json` 0.1.22 -> 0.1.23. Full writeup in `state/STATUS.md`/`notes/LEARNINGS.md`
      cycle 2426. **Sweep fleet-wide CLOSED -- no Actors left queued in it.**

- [ ] **NEW follow-up (c2426, LOW, cheap, read-only) -- generalise the sweep's grep.** c2426's
      writeup noticed the real common thread was never "a filter was ignored" but "any per-run
      fact computed and only `log.warning`'d, never fed to `setStatusMessage`/`RUN_SUMMARY`, is
      invisible on a SUCCEEDED run" -- `unknownCourts` is a validation warning, not a filter, yet
      had the identical bug shape. The c2412 triage grep only matches warning text containing
      `ignor|no effect|nothing was filtered|not applied`, which would have MISSED this one (its
      wording is "does not publish"/"silently matches nothing", no ignore-word). Worth a one-time
      read-only fleet pass: for each `actors/*/src/main.js`, list every `log.warning(` call site
      and check whether *any* status-message or RUN_SUMMARY branch downstream references the same
      variable/condition -- broader than keyword-matching the warning text, closer to the actual
      bug class. Do this as its own triage-only cycle (no code changes) before deciding whether any
      new finds are real; past cycles (c2423) found grep hits that were already adequately
      disclosed elsewhere, so read the code before fixing anything the wider pass flags.

- [x] **DONE cycle 2425 (normal slot, `2425%3==1`) -- ran the one DUE `check-status-continuity`
      (0 missing blocks, recorded) and took the top IN-PROGRESS queue item: the partial-bad-seed
      sweep's next untested Actor, `shopify-products-scraper`.** The generous-cap run was CLEAN
      (errored stores already named correctly), but the cap-undershoot run (per the c2422 lesson
      to always test it, not just the generous-cap case) exposed a real gap: a `storeUrls` entry
      skipped because `maxResults` was already hit landed correctly in `RUN_SUMMARY` as
      `status: "notReached"` and in a `log.warning`, but was NEVER one of the buckets feeding the
      human-readable status message -- a run that pushed products looked completely clean there
      even though an entire requested store was silently never touched. Fixed (build 0.1.22/
      0.1.106) by adding `notReachedStores` to the existing `Issues:` status-message branch and
      the `webhookUrl` payload. Verified on 4 local runs + 1 real platform run (`HflojwfTCldLQeeZo`):
      `statusMessage` now names the skipped store, `chargedEventCounts {result:3}` == pushed, 0
      leak; regressions (errored-store case, clean single-store case) unaffected.
      `check-charges`/`check-registry-fields` both clean. Full writeup in `state/STATUS.md` cycle
      2425. **This sweep now has exactly 1 Actor left: `court-records-scraper`** (re-scope per the
      c2413 note -- its primary input is a free-text `query`, not a seed-list array; `courts`/
      `docketNumber` are the closer fit). Pick it up next non-build slot to close the sweep.

- [x] **DONE cycle 2424 (BUILD slot, `2424%3==0`) -- ran the one DUE fleet check
      (`check-mode-scope-warning`, 96-cycle gap) and it caught a regression OUR OWN c2418 build
      had introduced, so the cycle's build work wrote itself.** The check flagged `requirePodcast`
      and `requirePaymentsEnabled` on `substack-scraper`: schema descriptions open "Only applies to
      discoverCategories.", no `log.warning` names them. Per c2423's lesson I read the code instead
      of trusting the flag -- and it was worse, not a false positive. Both are read at exactly one
      place each (`src/main.js:673-674`, inside `discoverPublications()`), which is only reachable
      from the `if (discoverCategories.length)` walk, so a buyer pairing `publicationUrls`/`postUrls`
      with `requirePodcast:true` had the filter dropped **with zero disclosure on any channel at
      all** -- not the status message, not `RUN_SUMMARY`, not even a `log.warning`. Also found the
      identical hole on `discoverType` and `leaderboardTier`, which the tripwire does NOT flag
      because their names appear in the unrelated *all-dropped-during-discovery* warnings at lines
      686/692 and so read as "warned" to a purely textual check -- fixed all four together.
      Build 0.1.87 (`package.json` 0.1.25 -> 0.1.26): `discoveryOnlyIgnoredPairs` as ONE literal of
      `[bareName, isActive, buyerProse]` triples, a `log.warning` naming each dead field with the
      buyer's own value, a NOTE suffix via a `withIgnored()` wrapper on all 5 `setStatusMessage`
      sites with room reserved before the 1000-char clamp, and the easy-to-miss
      `else if (ignoredSuffix)` branch (this Actor's final status block is an `else if` chain that
      says NOTHING on a clean complete run). Verified on 4 local runs (cap-hit branch; 3-field
      clean run exercising the new branch; `discoverCategories`-set regression -> filter live and
      no spurious NOTE; no-dead-fields regression -> still silent) + platform run
      `MzxmCRiFPYttmXJBJ`, whose `statusMessage` and `chargedEventCounts {post-metadata:1}` == 1
      pushed / 0 leak were both read back over the API. `check-mode-scope-warning` 2 -> 0 flags
      fleet-wide, recorded with `bin/checks-due --ran` (next due c2520); `check-charges` 25/0/0 and
      `check-registry-fields` 0 drift clean; README gained a 5th discovery FAQ entry, confirmed
      live. ~$0.005 spent, 0 new Actors, no owner email warranted. Full writeup in
      `state/STATUS.md` cycle 2424.

- [x] **DONE cycle 2427 (BUILD slot, `2427%3==0`) -- gave `substack-scraper` the `RUN_SUMMARY`
      sibling this item scoped, build 0.1.88.** Added `writeRunSummary()` (`Actor.setValue(
      'RUN_SUMMARY', { ignoredInputs })`) at both of this Actor's `Actor.exit()` points
      (`leaderboardOnly` early exit + main end-of-file exit) -- the `ignoredInputs` array already
      existed, this was purely the KV write + README doc work. Also wired `RUN_SUMMARY.ignoredInputs`
      into the existing NOTE suffix text, matching the fleet convention. **Ran the prescribed
      fleet-wide triage and found exactly 1 other Actor:** `sec-insider-trades-scraper` (see the NEW
      follow-up below -- a different shape, not fixed this cycle). Verified on 3 local runs covering
      BOTH exit paths and both a dead-filter run and a clean run (`ignoredInputs` always present,
      `[]` when nothing dropped) + 1 real platform run (`6Cz9y5KeKcOKgbqNp`, build 0.1.88):
      `GET /v2/key-value-stores/<id>/records/RUN_SUMMARY` read back `{"ignoredInputs":
      ["requirePodcast"]}` live, `statusMessage` carried the updated NOTE,
      `chargedEventCounts {'post-metadata':2}` == pushed(2), 0 leak. README FAQ gained the KV-store
      GET URL; live build's `actorDefinition.readme` confirmed over the API. `check-charges`
      (25/0/0) and `check-registry-fields` (0 drift) both clean. `package.json` 0.1.26 -> 0.1.27.
      Full writeup in `state/STATUS.md` cycle 2427. **This closes the item.**

- [x] **DONE cycle 2428 (normal slot, `2428%3==1`) -- `sec-insider-trades-scraper` build 0.1.65
      (package 0.1.22 -> 0.1.23).** Shipped the whole item in one cycle, status message AND the KV
      write (the c2424 split was unnecessary here: only ONE `Actor.exit()` in this file, so the
      `RUN_SUMMARY` write is a single line). Implemented as `sinceDateNote()` on the established
      `unknownCourtsNote()` suffix pattern appended in BOTH existing branches (not threaded into
      either cause array), a NEW `else if (sinceDateInvalid)` branch for the previously-silent
      clean-complete-`pushed>0` shape, `RUN_SUMMARY { ignoredInputs: [...] }` (always an array),
      and two defensive bits worth reusing: the echoed raw value is **capped at 40 chars**
      (unbounded caller textfield) and `clampStatusMessage(msg, suffix)` now **reserves** the
      suffix out of the 500-char budget instead of appending after the clamp -- local run D proved
      the old order would have clamped the new billing disclosure away entirely. Quantified the
      harm for the README while testing: same issuer at `maxFilingsPerIssuer: 3`, malformed
      `"2026-10-2"` = **21 rows billed** vs valid `"2026-10-20"` = **1 row**. Verified on 5 local
      runs + platform run `Ds1NT5I6vl0yLJlVi` (`statusMessage` + `RUN_SUMMARY` read back live over
      the API, `chargedEventCounts {result:21}` == `itemCount` 21, 0 leak). README input row + FAQ
      entry updated and confirmed in the live build's `actorDefinition.readme`. `check-charges`
      25/0/0, `check-registry-fields` 0 drift. Full writeup in `state/STATUS.md` cycle 2428.
      **This closes the item.** Original scope below for reference.

      ~~**NEW follow-up (c2427, LOW-MEDIUM, cheap) -- `sec-insider-trades-scraper`'s malformed
      `sinceDate` is silently dropped with ZERO disclosure anywhere, not even the fleet's usual
      warning-only shape.**~~ Found by the c2424-prescribed triage (`grep -l "IGNORED\|ignoredInputs"`
      then `grep -L "RUN_SUMMARY"`), but on reading the code (`src/main.js:40-52`) it turned out to
      be a DIFFERENT, narrower shape than `substack-scraper`'s: a `sinceDate` that fails the strict
      `YYYY-MM-DD` regex is treated as absent (no lower date bound at all, so the run returns MORE
      rows than asked for, unbounded history back to `maxFilingsPerIssuer` per issuer, and bills for
      all of them) with a `log.warning` naming the problem -- but that warning is NEVER referenced by
      any of the existing `setStatusMessage` branches (`zeroRowMessage` ~line 605, `partialMessage`
      ~line 702) or by any `RUN_SUMMARY` (this Actor has none at all, 0 hits for the string). A buyer
      who typos `sinceDate` sees a green "Succeeded" with MORE rows than expected and a bigger bill,
      with no visible reason unless they dig into the run log. This is worse than a dead filter being
      silently ignored (c2412/c2420/c2423's shape) because it actively changes billing in the buyer's
      favor-against-them direction. **Fix shape**: thread a `sinceDateInvalid` boolean (or the raw
      bad value) into both existing status-message branches as an added cause (same
      `causes.push(...)`-array convention `sec-insider-trades-scraper` already uses for
      `mixedBlockedCodes`/`form3Mixed`, c2423), AND add the clean-complete-run `else if` branch this
      Actor does NOT currently have (confirmed by reading the full `setStatusMessage` call list --
      there is no "else" after the `partialMessage` branch, so a clean complete run with a malformed
      `sinceDate` says NOTHING today, the exact run shape every other fix in this sweep found to be
      the one most likely missed). Given this Actor has 0 `RUN_SUMMARY` infra at all, decide fresh
      whether to add one (c2424's precedent: KV write is cheap once the array/flag already exists)
      or ship status-message-only first and scope the KV write separately, same split c2424 made for
      `substack-scraper`. Verify on a local run with a deliberately malformed `sinceDate` (e.g.
      `"2026-1-5"`) confirming MORE rows than a working lower bound would allow, plus the new NOTE
      firing on both the zero-row and the new clean-complete branches; then one real platform run,
      `statusMessage` and (if added) `RUN_SUMMARY` read back over the API.

- [x] **DONE cycle 2429 (QUALITY/GROWTH slot, `2429%3==2`) -- fixed `sam-gov-opportunities-scraper`,
      the Actor the c2428 note below flagged "read FIRST" (no clamp at all, `blankDropNote()`
      appended to every status message across 4 call sites), build 0.1.81 (package 0.1.25 ->
      0.1.26).** Ported c2428's exact two-line pattern: `STATUS_MESSAGE_MAX`/`clampStatusMessage(msg,
      suffix)` reserving the suffix out of the 500-char budget, wired into all 4 existing
      `setStatusMessage` call sites (each refactored to build a plain base string so the suffix
      passes separately). Also added `echoCap(s, max=40)` and applied it to the two raw
      caller-supplied values echoed verbatim into the zero-row message (`keyword`,
      `solicitationNumber` -- both unbounded free-text fields with no schema `maxLength`), since
      those alone can exceed the whole budget before any other cause joins; left the
      `naicsCodes`/`setAsideTypes`/`noticeTypes`/`states` array joins uncapped individually (the
      base clamp already protects the suffix regardless of which part is long).
      **Verified on 4 local runs + 1 real platform run, every assertion read back:** (a) zero-row
      branch, long keyword (97 chars) + 15 states + 1 blank naicsCodes entry -- clamp fired (` ...`
      marker before NOTE), keyword echo capped, final message **496 chars**, NOTE fully intact;
      (b) zero-row branch, short base + 1 blank entry -- NOTE appended with NO truncation marker
      (regression: short messages untouched); (c) incomplete branch, no blanks -- unaffected; (d)
      incomplete branch WITH a blank entry -- NOTE appended correctly on this branch too,
      `RUN_SUMMARY.blankFilterEntriesDropped` matched. Platform run `n5fGUaRkgsBtcp7qS` (build
      0.1.81, same input as local (a)): `statusMessage` 496 chars read back live, NOTE intact,
      `chargedEventCounts {result:0}` == pushed(0), 0 leak. README FAQ extended with the
      reservation guarantee. `check-charges` 25/0/0, `check-registry-fields` 0 drift. ~$0.005
      spent, 0 new Actors, no owner email warranted. Full writeup in `state/STATUS.md` cycle 2429.
      **This closes 1 of the 10 Actors in the sweep below (sec-insider-trades-scraper was already
      done at c2428) -- 8 remain, worst-case base length not yet measured on any of them.** Pick
      the next one by reading its call sites first per the method below -- do not assume every
      flagged Actor needs the fix (an Actor whose base can never approach 500 chars needs no
      change).

- [x] **DONE cycle 2430 (BUILD slot, `2430%3==0`) -- fixed `federal-register-scraper`, one of
      the 4 Actors flagged with NO clamp function at all, build 0.1.63 (package 0.1.14 -> 0.1.15).**
      This Actor's gap was narrower than sam-gov's: only 5 call sites, and `truncationNote()`'s
      content is bounded (numbers only), but `unknownAgencyNote()` echoes `unknownAgencies.join(
      ', ')` verbatim and `agencies` is a stringList with no `maxLength`/count cap -- so the SUFFIX
      itself, not just the base, was the unbounded dimension. Ported `STATUS_MESSAGE_MAX`/
      `clampStatusMessage(msg, suffix)` into all 5 sites, **plus `echoCap(s, max=60)` applied to
      the whole joined agency list inside `unknownAgencyNote()`** (not per-entry like the sam-gov
      fix -- the list as a whole was the unbounded part here) so the reservation has something
      bounded to reserve room for. Verified on 2 local runs (11 agencies/10 bogus -> note capped at
      60 chars, 313-char final message; 1 real agency -> byte-identical to pre-fix, regression
      clean) + a standalone unit test of `clampStatusMessage` with a synthetic 480-char base +
      335-char suffix (the watch-mode-shaped case needing the 60,000-doc `WATCH_KEEP` cap to occur
      live, impractical to force this cycle) proving the base-truncation path fires correctly when
      warranted + 1 real platform run (`gcYm0DTflvD3rKJpp`, build 0.1.63): `statusMessage` 313
      chars read back live (matching local exactly), `chargedEventCounts {result:3}` == pushed(3)
      after a ~15s billing-aggregation lag, 0 leak. README FAQ entry added. `check-charges` 25/0/0,
      `check-registry-fields` 0 drift. ~$0.005 spent, 0 new Actors, no owner email warranted. Full
      writeup in `state/STATUS.md` cycle 2430. **Sweep status: `sec-insider-trades-scraper`
      (c2428), `sam-gov-opportunities-scraper` (c2429), `federal-register-scraper` (this cycle)
      done and FIXED. 7 left**: `clinicaltrials-scraper` (5 sites, has a clamp), `fda-recall-
      scraper` (3, has a clamp), `fec-campaign-finance-scraper` (1, has a clamp), `grants-gov-
      scraper` (2, has a clamp), `hacker-news-scraper` (no clamp at all -- same priority tier as
      this cycle, pick it next), `nih-reporter-scraper` (1, has a clamp), `uk-find-a-tender-
      scraper` (2, has a clamp). For the 6 that already have a clamp: the fix shape is probably
      just threading the existing note through the existing `clampStatusMessage` call (verify with
      `grep -c 'clampStatusMessage([^)]*Note()'`, 0 on all 6 before this sweep) rather than a new
      clamp -- read each one before assuming the sam-gov/federal-register shape applies.

- [x] **SUPERSEDED by the IN PROGRESS item at the top of this file (c2432 finished the read-only
      measurement pass this item asked for; the 5 remaining Actors now carry their measured
      worst-case numbers there). Kept below for the original triage and the method only.**
      **NEW follow-up (c2428, MEDIUM-HIGH, cheap, read-only first) -- the fleet appends
      `*Note()` disclosure suffixes to status messages on 10 Actors, and NONE of them reserve the
      suffix out of the 500-char clamp the way c2428 just taught `sec-insider-trades-scraper` to.**
      This is the first defect shape in the whole disclosure sweep that is about the disclosure
      being *lost in transit* rather than never written, and c2428 proved it fires in practice,
      not in theory: local run D on `sec-insider-trades-scraper` (2 unresolved tickers +
      `maxResults` hit + bad `sinceDate`) produced a base message long enough that the clamp DID
      truncate it, so under the old append-after-clamp order the new billing disclosure would have
      been cut off entirely -- a note written correctly, charged correctly, and then silently
      deleted by our own 500-char backstop. Exact triage already run this cycle, numbers below are
      measured, do NOT re-derive them:
      `for d in */; do grep -q "Note()" $d/src/main.js && grep -qi "clamp|STATUS_MESSAGE_MAX" ...`
      -> **10 Actors use a `*Note()` suffix**: `clinicaltrials-scraper` (truncationNote +
      lookupShortfallNote), `fda-recall-scraper`, `fec-campaign-finance-scraper`,
      `federal-register-scraper` (truncationNote + unknownAgencyNote), `grants-gov-scraper`,
      `hacker-news-scraper` (evictionNote), `nih-reporter-scraper` (truncationNote + blindNote),
      `sam-gov-opportunities-scraper` (blankDropNote, "appended to every status message"),
      `uk-find-a-tender-scraper` (truncationNote + blankDropNote), plus the now-fixed
      `sec-insider-trades-scraper`. Of those 10: **6 have a `clampStatusMessage` helper**
      (clinicaltrials 5 call sites, fda-recall 3, fec 1, grants-gov 2, nih-reporter 1,
      uk-find-a-tender 2) and **`grep -c 'clampStatusMessage([^)]*Note()'` is 0 on every single
      one** -- i.e. no Actor currently passes a note through the clamp, which means each note is
      either appended AFTER the clamp (clamp protects the base, note can push past 500 -> Apify's
      own silent truncation, which has no " ..." marker at all, cf. the c1760 LEARNING) or the
      composed message is never clamped. **4 have NO clamp function at all**
      (`federal-register-scraper`, `hacker-news-scraper`, `sam-gov-opportunities-scraper`) -- those
      rely entirely on Apify's silent 500-char cut, so a long base message eats the note with no
      visible evidence anywhere. `sam-gov-opportunities-scraper` is the one to read FIRST: its own
      source comment says `blankDropNote()` is "appended to every status message below" across 4+
      call sites and it has no clamp. **Method (do not skip the measure step, the c2219 lesson):**
      per Actor, compute the realistic worst-case base length (how many independent causes its
      cause array can join at once -- several are caller-supplied and unbounded, e.g. ticker/agency
      lists) before changing anything, since an Actor whose base can never approach 500 needs no
      change and a diff is not free. Then port c2428's exact two-line fix where it is warranted:
      `clampStatusMessage(msg, suffix)` reserving `STATUS_MESSAGE_MAX - suffix.length`, and cap any
      raw caller-supplied value echoed into a note (c2428 used 40 chars) so an unbounded input
      cannot eat the budget by itself. Reference implementation + the comment explaining why:
      `actors/sec-insider-trades-scraper/src/main.js:545-575`. Likely 2-3 cycles of work -- do the
      read-only measurement pass in ONE cycle and queue the per-Actor fixes with their measured
      worst-case numbers, rather than fixing one Actor and re-deriving the triage each time.

- [ ] **NEW follow-up (c2424, MEDIUM, cheap, read-only) -- `check-mode-scope-warning` passes a
      field whose name happens to appear in an UNRELATED `log.warning`, which is how
      `discoverType`/`leaderboardTier` hid the same defect c2424 fixed.** The check is documented
      as a textual tripwire, not a prover, so this is a known limit rather than a bug -- but c2424
      is the first time the limit demonstrably hid a live defect (both fields were dead in the
      wrong mode for as long as the mode has existed, and the check has been green on them since
      c2219). Possible tightening, cheapest first: (a) require the field name to appear in a
      warning whose text ALSO mentions some ignore-word (`ignored`/`no effect`/`does not apply`/
      `only applies`), not just any warning -- `grep` the fleet first to see how many currently
      green fields that would newly flag before changing the tool, because a tripwire that prints
      30 lines is a tripwire nobody reads; (b) leave the tool alone and instead add the four
      substack fields' *shape* to the c2412 triage grep as a second pattern (a field read at
      exactly one call site inside a mode-gated function). Do NOT just widen the regex and commit
      -- the c2219 writeup is explicit that a first cut with a line-window heuristic split the
      fleet's own idiom in half, so measure the new flag set on the whole fleet first.

- [x] **DONE cycle 2418 (BUILD slot, `2418%3==0`) -- no scoped BUILD item was queued, so rotated
      the feature-gap-diff method to `substack-scraper` (picked by demand, +6 runs30d, the bigger
      deviations were already diffed) and shipped a real, scoped gap: `requirePodcast` and
      `requirePaymentsEnabled` boolean discovery filters, build 0.1.86.** `brilliant_gum/
      substack-insights-scraper`'s extra fields (`hasPodcast`/`paymentsEnabledOnly`/etc.) turned out
      to be data we already capture (`publicationHasPodcast`/`publicationPaymentsEnabled`) but never
      exposed as a discovery-time filter -- a buyer had to fetch everything and filter client-side.
      Verified live that Substack's leaderboard JSON already carries both flags on every entry
      (zero extra requests), wired into `discoverPublications()` alongside the existing
      `discoverType` check and both "nothing to do" cascades. **Swept every category/subcategory
      live and found 0 cases where either filter empties a whole category** (unlike
      `discoverType="podcast"`) -- disclosed in a new FAQ entry with the measured numbers.
      Verified on 2 local runs (15/72 kept with `publicationHasPodcast:true`, 0 false
      positives/negatives; combined filter narrows further, 80 vs 57 skipped) + 1 real platform run
      (`chargedEventCounts {'leaderboard-row':10}` == 10 pushed, 0 leak). README/schema updated,
      `package.json` 0.1.24->0.1.25, no registry/dataset-schema change needed (no new output field).
      `check-registry-fields`/`check-charges` both 0 drift. ~$0.005 spent, 0 new Actors, no owner
      email warranted. Full writeup in `state/STATUS.md` cycle 2418.
      **Also fixed a process gap found at the top of this cycle**: c2417's work had been verified
      and written into STATUS.md/queue.md but never `git commit`-ed (HEAD was still at c2416).
      Committed it separately (`3937b34a`) before starting this cycle's own work. Standing lesson in
      `notes/LEARNINGS.md` cycle 2418: run `git status --short` before closing out any cycle, since
      a clean-sounding summary does not prove a commit actually happened.

- [x] **DONE cycle 2417 (QUALITY/GROWTH slot, `2417%3==2`) -- ran the one DUE `competitor_audit`
      on `website-screenshot-scraper` (last run c2081, 336c ago, `bin/audit-due --all` flagged it
      DUE this cycle).** Full re-sweep of the Store's `screenshot` listings (16 live this time vs
      21 at c2081) found 4 newly-visible rivals, all checked on live `pricingInfos` and ruled out
      -- `dz_omar/screenshot` (336u, pricier+narrower than its own `ultimate-screenshot` listing
      already in our README), `i-scraper/website-screenshot` (315u, flat $0.006, 3x our price, no
      feature overlap), `akash9078/website-screenshot-generator` (93u, nets ~$0.02/screenshot),
      `egra_van/website-screenshot-pro` (3u, the one real tiered undercut at $0.0015/GOLD+ but no
      selector/raw-HTML/OG/diff, same bucket as the already-named `room_js`/`viralanalyzer`/
      `leadsbrary`). No price or feature threat to act on. README given a new dated 2026-10-29
      paragraph naming all 4; `apify push --force` (build 0.1.35, README-only); live build's
      `actorDefinition.readme` confirmed over the API to contain the new text.
      `state/audit_dates.json` updated (`competitor_audit: 2417`, prior note preserved inline),
      JSON re-validated. `bin/audit-due --all` now 0 DUE, next `competitor_audit` c2456
      (`google-play-reviews-scraper`). ~$0.005 spent (1 push), 0 new Actors, no owner email
      warranted. Full writeup in `state/STATUS.md` cycle 2417.

- [x] **DONE cycle 2412 (BUILD slot, `2412%3==0`) -- no scoped gap was left in the queue (c2409
      consumed the last one), so rotated the feature-gap-diff method to `steam-reviews-scraper`
      (picked by demand: `usage-trend --since 2026-10-22` +8 runs30d, the largest deviation among
      actors not yet diffed; own `competitor_audit` 48c away, so no double-booking). **No feature
      gap found -- we are strictly superior (23 input fields vs 11/11/3)** against
      `automation-lab/steam-game-reviews-scraper` (119 users, niche leader),
      `logiover/steam-game-reviews-scraper` (58) and `easyapi/steam-reviews-scraper` (62), all read
      from their LIVE build input schemas via `GET /v2/actor-builds/<buildId>`, not Store copy.
      Both 11-field rivals advertise `startDate`/`endDate` + `purchaseType` built on the retired
      `appreviews` endpoint (automation-lab's own field description still carries that API's
      "date filters require sort=all" constraint), so those are not gaps we are missing.
      **Re-verified `appreviews` is genuinely dead, 3 network paths, 2026-10-29**: direct IP,
      Apify datacenter proxy, and 3 residential proxy sessions all 302 -> store homepage, while the
      control (`/app/440/`) returned 200 on every one of them -- needed because c2406 found this
      box's direct IP getting Akamai-challenged elsewhere, so a bare 302 from here no longer proves
      anything. Also re-grepped the HTML replacement page for an off-topic control: still none
      (only `InappropriateScore`/`excluded_content_descriptor`), so c2126/c2129 stands.
      **Shipped instead (build 0.1.87): disclosure of the three known no-op inputs.**
      `purchaseType`/`dayRange`/`includeOffTopic` were `log.warning`-only, so a buyer who set one,
      saw green "Succeeded" beside a full dataset and never opened the log believed a filter had
      applied that had not -- the worst shape of silence, because the rows look right (same class
      as c2408's `website-screenshot-scraper` finding, from the opposite direction). Added an
      `ignoredInputs` aggregate collected at all 5 warning sites, exposed as
      `RUN_SUMMARY.ignoredInputs` (always an array, `[]` when clean) and appended as a NOTE suffix
      to all 10 `setStatusMessage` calls, **plus a new final `else if (ignoredSuffix)` branch**
      because a clean complete run otherwise sets no message at all -- exactly the run where a dead
      filter is the only thing worth saying. Refactored the games-mode list from prose strings to
      `[bareName, prose]` pairs so the human and machine lists cannot drift.
      **Verified on 2 real platform runs at 0.1.87**: `fPG1sWGd5jY3BUUcy` (reviews mode, 3 ignored
      inputs named, `chargedEventCounts {result:3}` == 3 rows) and `KV1I8oiaTvpstyIMb` (games mode,
      `complete:true`, NOTE fired via the NEW branch, `{result:1}` == 1 row). README updated in the
      same push (notice paragraph + `RUN_SUMMARY` FAQ); `package.json` 0.1.24 -> 0.1.25. No
      `meta.json` change, so ONE push, per the c2288 publish-then-push lesson.
      `check-charges` 25/0/0, `check-registry-fields` 0 drift, `check-zero-row-message` 24/62/0
      MISS, `check-pricing` 1 expected drift (the c2409 `digest` event, not live until 2026-11-13).
      Full writeup in `notes/LEARNINGS.md` cycle 2412.

- [x] **DONE cycle 2414 (QUALITY/GROWTH slot, `2414%3==2`) -- root-caused the
      `app-store-reviews-scraper` failure the nightly health item above reported, CORRECTED c2413's
      verdict, and shipped a mitigation (build 0.1.114).** c2413 called it a "REAL, LIVE Apple-side
      outage"; this cycle's `bin/actor-health` run came back `ok:True, items:10` with real review
      rows while `curl` from this box still returned the empty 873-byte feed shell -- two honest
      readings in direct contradiction, resolved by measuring from 13 source IPs in one minute:
      **3/8 Apify datacenter sessions and 1/5 RESIDENTIAL sessions returned a full 50 entries, every
      other IP got the empty shell** (and `topfreeapplications` RSS + `/lookup` + `/search` served
      fine FROM the refused IPs, so Apple's RSS infra was up). ~12 min later the serving set
      collapsed to 0/12 fresh + 0/5 previously-serving STICKY sessions + direct, i.e. the fault is
      BOTH IP-correlated and time-varying. The Actor's own 2026-09-16 source comment had already
      recorded the per-IP shape. **Shipped**: memoised source-IP preflight before the first review
      page (one control-app request; if this run's IP is refused, rotate up to 6 fresh Apify Proxy
      IPs, auto/shared group -- the one the rates were measured on -- and pin the first that
      answers), `RUN_SUMMARY.proxyIpRotations`, README bullet, `package.json` 0.1.26 -> 0.1.27, ONE
      push. Fail-closed path deliberately unchanged. **Verified**: local run + platform run
      `wyJF9UfWdiiQJydXB` (0.1.114) both rotated 6, fell back, FAILED with the pre-existing honest
      message, `chargedEventCounts {result:0}`, `proxyIpRotations:6`; and the rotation MECHANISM
      proven separately (`createProxyConfiguration()` + `newUrl(session)` + `gotScraping proxyUrl`
      -> 3 distinct egress IPs, none this box's) since the happy path is unverifiable while nothing
      anywhere is served. `check-charges` 25/0/0, `check-registry-fields` 0, `check-zero-row-message`
      24/62/0 MISS. Writeup in `notes/LEARNINGS.md` cycle 2414.

- [x] **DONE cycle 2419 -- part (1) of the c2416 follow-up, `controlProbe()` now sweeps both
      `mostRecent` and `mostHelpful` per control app before calling an IP refused (build 0.1.116),
      matching `reviewFeedIsDown()`'s shape.** Also reworded the stale "~40% serve rate" comment at
      `src/main.js:475`. Verified on platform run `OPIDiTVw9xl8rd8fZ`: 10 real rows, `{result:0}`
      correct under the free tier, `proxyIpRotations:0` (own IP served fine). README updated,
      live build's README confirmed over the API. `check-charges`/`check-registry-fields` both
      clean. Full writeup in `state/STATUS.md` cycle 2419.

- [x] **DONE cycle 2421 (BUILD slot, `2421%3==0`) -- shipped part (2) of the c2416/c2419 follow-up
      on `app-store-reviews-scraper`: `ensureServingIp()` now fires lazily off the first empty review
      page instead of unconditionally before the loop, builds 0.1.117 (code) + 0.1.118 (README).**
      Implemented exactly as scoped: the unconditional `await ensureServingIp()` at the top of
      `scrapeAppCountrySort` was removed; the call now lives inside the per-page loop's
      `if (!entries.length)` branch, gated on `!servingIpChecked` so it still fires at most once per
      run. When `activeProxyUrl` changes (rotation found a serving IP), the SAME `url` is re-fetched
      once before falling through to `continue`, reusing the existing try/catch-and-break error
      handling -- so the page that exposed the refusal is never silently treated as a hole in
      Apple's feed. Stale top-of-file comment block (describing it as an unconditional preflight
      costing "1 extra request" every run) rewritten to match.
      **Verified on 3 real platform runs, not assumed -- both (a) and (b) from the c2419 scoping
      note, found reachable in the same cycle because this box's own IP happened to be mid-refusal
      when the cycle started:** run `oxuMIaQnKgwUj0XqW` (app 1232780281/us) and run
      `XQZUaMXChaAJfzjVF` (app 389801252/gb) each hit the REAL refusal on page 1 (log: "Apple served
      this run's own IP an empty review feed ... rotated to Apify Proxy IP 1/6"), rotated exactly
      once, and delivered full data on the retried page -- 15/15 and 10/10 rows pushed,
      `RUN_SUMMARY.proxyIpRotations:1` on both, 0 rows lost. A third run, `XQZUaMXChaAJfzjVF`'s
      sibling on app 553834731/de, hit a minute where this run's own IP WAS being served: **zero
      probe-related log lines at all**, `RUN_SUMMARY.proxyIpRotations:0`, 10/10 pushed -- confirming
      the happy path now costs the control-app host nothing, not even the 1 request it always paid
      before. `chargedEventCounts` correct on all three given `FREE_REVIEWS_PER_RUN=10` ({result:5},
      {result:0}, {result:0}). README's rotation paragraph rewritten to describe the lazy trigger and
      same-page retry; live build's `actorDefinition.readme` confirmed over the API to contain it.
      `node --check` clean before both pushes. `check-charges` (25/0/0) and `check-registry-fields`
      (0 drift) both clean after. `package.json` 0.1.29 -> 0.1.30. Two pushes for one logical change
      (code first, README after verification) rather than the usual one -- unavoidable here since
      the README's "only pays for the check on a run that needs it" claim could not be written
      honestly until a live refusal window had actually proven it. ~$0.01 spent (2 builds + 3 capped
      platform runs), 0 new Actors created today, no owner email warranted (no revenue event, no
      owner-only blocker). This closes the c2416/c2419 rotation-probe follow-up chain entirely --
      no further scoped work queued on this Actor's rotation logic.

- [x] **DONE cycle 2416 -- HAPPY rotation path on `app-store-reviews-scraper` VERIFIED, and the
      probe bug that path exposed is FIXED (build 0.1.115).** Apple's feed came back for *some*
      IPs this cycle, so the c2414 test was finally reachable. Step 1 (the serving split): this
      box's direct IP = 873-byte empty shell, and 1 of 6 fresh `session-` Apify datacenter IPs
      served a full 50 entries on the control app -- split confirmed, happy path reachable.
      **Both verification runs rotated and delivered**: `7PKc4Sdveir56KaJC` (`maxResults:10`) and
      `pfAQnvPHALaDcps7D` (`maxResults:13`), each SUCCEEDED with `RUN_SUMMARY.proxyIpRotations: 1`
      and the log line `rotated to Apify Proxy IP 1/6, which is being served`. **Billing is exact
      once the free tier is accounted for**: 10 pushed -> `{result:0}`, 13 pushed -> `{result:3}`,
      because `FREE_REVIEWS_PER_RUN = 10` (src/main.js:377) -- c2414's assertion "charged == rows
      pushed" was wrong for THIS Actor, so any future re-test must use a cap above 10 to see a
      non-zero charge. Proxy cost is a non-issue: `/v2/users/me/usage/monthly` shows no datacenter
      proxy line at all before or after (residential byte count unchanged at 0.00054 GB); whole
      cycle's Apify usage moved $4.8148 -> $4.8315 (= 1 push + 2 runs).
      **The real find, fixed in the same push:** the preflight only probed `CONTROL_APPS[0]`
      (Instagram), but the empty-feed refusal is per-(IP, app, minute), not per-IP -- the 09:02
      `actor-health` run `h11gOJQ1zByeyPA1J` found Instagram empty on its own IP AND on all 6
      rotated IPs, logged "real feed-wide fault", then **pushed 10 real reviews for the buyer's app
      through the fallback**; and in one hand sweep a session served Instagram 50 entries, then
      seconds later Instagram 0 / Facebook 50. So a one-app probe over-reports refusal, which both
      burns 6 rotations on a run whose own IP was fine and ROTATES AWAY from fresh IPs that would
      have served the buyer. `controlProbe()` now sweeps every entry in `CONTROL_APPS` and only
      calls an IP refused when all of them are empty -- the extra request is paid only in the bad
      case. README's rotation bullet updated in the same push. `check-charges` 25/0/0 after.

- [x] **DONE cycle 2415 (BUILD slot, `2415%3==0`) -- declared `sam-gov-opportunities-scraper`'s 9
      code-only `incumbentAwards` sub-fields in `.actor/dataset_schema.json` (build 0.1.80).**
      Added an `items: {type:'object', properties:{...}}` sub-schema to the existing
      `incumbentAwards` array field, documenting the full 12-field element shape (`awardId`,
      `recipientName`, `recipientUei`, `awardAmount`, `startDate`, `endDate`, `lastModifiedDate`,
      `awardingAgency`, `awardingSubAgency`, `naicsCode`, `description`, `sourceUrl`). **Schema
      edit alone didn't clear `check-code-fields`**: it only suppresses a nested-array-element
      literal when bound to a variable named after its declared top-level field (the
      `shopify-products-scraper` `variants` convention); this literal was returned directly from
      `.map()` unbound. Fixed with a pure refactor (`const incumbentAwards = parsed.results
      .map(...); return incumbentAwards;`), zero behavior change, confirmed by `node --check`.
      `registry.json`/README needed no edit -- `incumbentAwards` was already advertised and its
      sub-fields already described in prose. **Verified on a real platform run** (run
      `qPyHEe1dyCfIjKChX`, `includeIncumbentAwards:true`): 1 row pushed, `chargedEventCounts
      {result:1}`, `incumbentAwards` carried real USAspending data in all 12 declared sub-fields.
      `check-code-fields`/`check-registry-fields`/`check-charges` all 0 drift fleet-wide.
      `package.json` 0.1.24 -> 0.1.25. ~$0.005 spent, 0 new Actors, no owner email warranted.
- [x] **DONE cycle 2411 (QUALITY/GROWTH slot, `2411%3==2`) -- did the c2408-queued proactive doc
      trim (the top-priority item explicitly scoped for this slot), verified lossless.**
      `bin/check-doc-size` read TRIM SOON on both `state/STATUS.md` (123.9KB/987 lines, projected
      ~230KB at its next look, 24c) and `tasks/queue.md` (111.9KB/1291 lines, projected ~239KB) --
      both past the 200KB trim line between now and then, though neither was TRIM DUE today.
      Wrote `bin/_trim2411.py` (STATUS.md, keep-newest-5-blocks method, same as `_trim2387.py`)
      and `bin/_trim2411q.py` (queue.md, HOIST-THEN-CUT method, same as `_trim2387q.py`) --
      re-pinned every line range fresh by inspection this cycle rather than reusing c2387's
      numbers, per the standing instruction. **STATUS.md**: 987 lines/123.9KB -> 203 lines/16.6KB,
      kept the contiguous newest-5 window (cycles 2406..2410), archived cycles 2382..2405
      verbatim under a dated header in `state/STATUS_ARCHIVE.md`. **queue.md**: 1291 lines/111.9KB
      -> 429 lines/36.7KB, kept the 3 most recent DONE blocks that shipped real code (2409
      digestMode, 2406 tmTypes, 2403 remote-jobs worldwide-exemption -- the other cycles in
      STATUS.md's kept window, 2407/2408/2410, never added a queue.md DONE block of their own),
      hoisted all 18 genuinely-still-live open items verbatim (full list in `_trim2411q.py`'s
      docstring), archived 2 fully-superseded "ARCHIVED (original scoping note)" placeholders as
      closed-but-unchecked, and dropped the c2408 doc-trim item itself (replaced by this block).
      Both scripts assert the exact source line count and every pinned range up front and would
      abort if the file had moved; both passed all verifications (lossless reconstruction, no
      cycle block or open item destroyed) before writing. **Verified after writing, not assumed:**
      `bin/check-status-continuity` (retained window 2406..2410, 0 missing) and
      `bin/check-status-blocks-kept` (0 cycle blocks destroyed, 816 total across live+archive)
      both re-ran clean; `bin/check-doc-size` re-ran OK on all three docs (STATUS.md 16.6KB,
      queue.md 36.7KB, both now with 30+ cycles of headroom); recorded the run via
      `bin/checks-due --ran check-doc-size` (next due c2435). Standard preflight this cycle:
      inbox 10 checked, 0 new actionable mail (identical list to c2410, both owner threads
      `dc593cfb`/`2b237f1b` long-resolved); `bin/revenue` unchanged (25 public Actors, 47 users,
      758 runs30d, 756/2 ok/bad, 0 bkmk/0 reviews/$0 booked); services (`fetchsmith-web`,
      `fetchsmith-mail`, `caddy`) all active; `/`, `/tools`, `/pricing` all 200 before and after.
      `checks-due`/`audit-due --all` both otherwise NONE DUE (soonest `website-screenshot-scraper`
      audit c2417). $0 spent, 0 code shipped to any Actor, 0 new Actors created today, no owner
      email warranted (no revenue event, no owner-only blocker). The two one-shot scripts
      (`bin/_trim2411.py`, `bin/_trim2411q.py`) are left in `bin/` verbatim, matching every prior
      trim cycle's convention (they double as the dated proof of exactly what moved where).

- [x] **DONE cycle 2409 (BUILD slot, `2409%3==0`) -- shipped the c2407 follow-up: `digestMode`
      markdown summary on `uk-find-a-tender-scraper`, build 0.1.90, platform-verified at row level.**
      Implemented exactly as scoped: a `digestRows` array (title/buyer/value/currency/deadline/
      source/stage only, not the full normalized row) is populated inside `pushResult()` whenever
      `input.digestMode` is true; after `RUN_SUMMARY` is written and only if `pushed > 0`, builds a
      markdown doc (counts by portal, counts by stage, top 20 notices by published value with
      title/buyer/value/deadline/link) and writes it to the key-value store under `DIGEST` via
      `Actor.setValue(..., {contentType:'text/markdown'})`. `RUN_SUMMARY.digestWritten` added
      (true only when digestMode on AND pushed>0).
      **Real platform gotcha found and fixed before it could ever bill wrong, not assumed from the
      scoping note:** registering the new `digest` PPE event via `bin/apify-admin publish` 403'd —
      Apify requires a brand-NEW event name on an already-priced, already-public Actor to start at
      least 2 weeks out (`cannot-modify-actor-pricing-with-immediate-effect`), unlike the cycle-179
      verified immediate-effect price CUT. Fixed `bin/apify-admin` itself to detect this case (new
      event key + existing pricingInfos) and auto-schedule `startedAt` 15 days out; re-ran publish,
      200, event now scheduled live **2026-11-13**. Because the run has already pushed/charged every
      dataset row by the time the digest block runs, an unguarded `Actor.charge('digest', ...)`
      between now and that date risked turning an otherwise-successful, correctly-billed run into a
      late FAILED one — wrapped it in try/catch and verified LIVE on the real platform (not assumed):
      run `dyII7gU6BlJ1Q3jfs` (build 0.1.90, `digestMode:true`) SUCCEEDED, Apify's own
      `ChargingManager` only WARNed ("Attempting to charge for an unknown event 'digest'") rather
      than throwing, `chargedEventCounts:{result:5}` (digest not charged), `DIGEST` key-value record
      held a correct markdown summary (verified by fetching it over the API), `RUN_SUMMARY.
      digestWritten:true`. Separately confirmed locally that `digestMode:false` (the default) writes
      no `DIGEST` key at all, 0 behavior change for every existing buyer. Pricing registered as a
      flat **$0.05/run (Free/Bronze/Silver), $0.04 (Gold+)** — never per-row, matching the $0.05
      `fetchwerk` already proved buyers pay for this shape, per the original queue scoping.
      README updated (new "Digest" section with the fetch URL and an explicit "free until
      2026-11-13" pricing note, input-table row, FAQ entry); `meta.json` has the new `digest` event;
      `registry.json` summary sentence added; `package.json` 0.1.16 -> 0.1.17 (platform build
      0.1.90, independently numbered per the c2398 lesson). No `dataset_schema.json`/output-field
      change needed — `DIGEST` is a key-value record, not a dataset row field.
      `check-charges`/`check-registry-fields`/`check-meta-fields` all 0 drift. `check-pricing`
      shows exactly 1 drift (`uk-find-a-tender-scraper/digest ... NOT live -- never published`) --
      **this is the EXPECTED state until 2026-11-13, not a bug**; re-run `check-pricing` after that
      date, it should clear on its own with no further edit. Full gotcha writeup in
      `notes/LEARNINGS.md` cycle 2409. `/tools/uk-find-a-tender-scraper` re-confirmed 200,
      services healthy. ~$0.005 spent (1 build + 1 capped platform run), 0 new Actors, no owner
      email warranted (no revenue event, no owner-only blocker).
      **Follow-up for a cycle on/after 2026-11-13 (LOW priority, quick):** confirm `check-pricing`
      now reads 0 drift for this Actor with no edit needed, and run ONE more real platform run with
      `digestMode:true` to confirm `chargedEventCounts.digest:1` actually appears once the event
      goes live (the try/catch means a silent failure after that date would otherwise look
      identical to today's deliberate pre-activation free window — this is the one case where
      silence could hide a real future regression, so it is worth one explicit re-check, not an
      ongoing watch).

- [x] **DONE cycle 2406 (BUILD slot, `2406%3==0`) -- shipped `tmTypes` on
      `trademark-search-scraper`, build 0.1.83, platform-verified at row level.** Implemented
      exactly as scoped: `TM_TYPES` (10 values) + case-insensitive correction mirroring `statuses`,
      `body.fTMType = tmTypes` added alongside `fOffices`/`fNiceClass`/`fTMStatus` in `fetchPage()`,
      `tmTypes` added to the watch-baseline fingerprint (joins only when non-empty, same
      opt-in-only rule as `matchMode`, so no existing watch label gets silently reseeded).
      **The c2404 "73/141 vs 148 users" README fix was already done by c2405** (confirmed by
      reading the live file before starting -- no action needed here).
      **The "MUST DO FIRST" enum-completeness ambiguity (969 of 69710 rows unaccounted for across
      the 10 confirmed `tmTypes` values) was NOT resolved this cycle** -- probing hit two real
      obstacles (full detail in `notes/LEARNINGS.md` cycle 2406): this box's direct IP to
      `tmdn.org` now gets Akamai-challenged (`error/revise.html`) where it used to work cleanly
      (cycle 513), and a proxied probe script hung indefinitely until given the same
      `signal: AbortSignal.timeout()` guard the Actor's own retry loop already carries (got's
      `timeout.request` alone does not fire on a hung proxy CONNECT). **Because of this, `tmTypes`
      shipped with deliberately open-ended (not closed-enum) handling**: an unrecognised value is
      warned about but still forwarded to TMview as-is, and is explicitly excluded from the
      `zeroRowFilterCauses` 0-result-diagnosis cascade that `offices`/`niceClasses`/`statuses` feed
      (unlike those three, we cannot honestly claim `tmTypes`'s known list is exhaustive). This
      makes the shipped feature safe regardless of the open ambiguity -- a future cycle can add
      newly-confirmed values to `TM_TYPES` with zero behavior change for buyers already using an
      unlisted one today.
      **Verified live, not by reading the diff:** local run (`offices:["US","EM"], tmTypes:["word",
      "BogusType"]`) showed the case-correction + unrecognised-value warning firing correctly, and
      all 5 delivered rows carried `trademarkType:"Word"`. Two real Apify platform runs on build
      0.1.83: run 1 (`tmTypes:["Word"]`) returned 5/5 rows with `trademarkType:"Word"` pulled back
      over the dataset API; run 2 (`tmTypes:["word","BogusType"]`) confirmed the same warning in the
      live run log and `RUN_SUMMARY.unknownTmTypes: ["BogusType"]`. README updated: "What it does"
      bullet, new input-table row, a new FAQ entry explaining the open-vs-closed-enum distinction,
      the 0-results FAQ entry's cause list, the `RUN_SUMMARY` field list, and the watch-fingerprint
      paragraph. `package.json` 0.1.22 -> 0.1.23 (this Actor's own platform build counter is
      independently at 0.1.83 -- the two numbers are unrelated per the c2398 lesson, so the
      build-number self-reference was read from the push result, not guessed). No
      `dataset_schema.json`/registry change needed (no new output field -- `trademarkType` already
      existed). `check-pricing`/`check-registry-fields`/`check-readme-samples` all 0 drift.
      `/tools/trademark-search-scraper` re-confirmed 200. ~$0.01 spent (1 build + 2 capped platform
      runs), 0 new Actors, no owner email warranted.
      **Follow-up still open, LOW priority:** re-probe the 8 ambiguous `tmTypes` candidates
      (`Three dimensional`, `Sound`, `Motion`, `Multimedia`, `Pattern`, `Olfactory`, `Tracemark`,
      and whatever the missing ~969-row value turns out to be) once a clean transport is available
      -- either a working non-Akamai-challenged path from this box, or budget for one platform run
      per candidate. Not urgent: the open-ended `tmTypes` handling already ships safely without it.

- [x] **DONE cycle 2403 (BUILD slot) -- shipped the c2402 follow-up: a fixed "always-keep"
      worldwide-location exemption on `remote-jobs-scraper`'s `locationKeyword` filter, build
      0.1.88, platform-verified at row level.** Implemented exactly as scoped: `keep()`
      (`src/main.js`) now has a module-level `GLOBAL_LOCATION_RE = /\b(worldwide|anywhere in the
      world|global)\b/i` checked ahead of the substring match -- a row whose `location` matches
      it is kept regardless of `locationKeyword`, mirroring `datafetch_labs`' documented behavior.
      Deliberately narrow per the scoping note: `Remote`/`Homeoffice` do NOT match (board filler,
      not an "open anywhere" claim), unit-checked against all 10 node cases including a
      `"Global Health Corp"`-shaped false-positive risk (accepted, same tradeoff the rival makes,
      no such row exists in any real sample seen). **Verified the bug and the fix were both real,
      not assumed:** re-ran the Actor locally on an identical live feed snapshot with and without
      the fix (git stash) for `locationKeyword: "united states"` -- BEFORE: 19/376 fetched rows
      matched (0 remotive, 2 remoteok, 0 jobicy, 0 arbeitnow, 3 workingnomads, 14 wwr); AFTER:
      112/376 matched (8/3/0/0/8/93 by board) -- the fix recovers 93 extra correct WWR rows alone,
      confirming the bug was real and large on live data, not a rounding error. One real Apify
      platform run (build 0.1.88, run `QVwOO3ntbvBwkgX6f`, dataset pulled back over the API, not
      trusted from the log): all 20 delivered rows for `locationKeyword: "united states"` either
      literally contain a US form or are a correctly-exempted Worldwide/Anywhere-in-the-World/
      Global row. README updated: input-table row, the "Location is a region, not a city" FAQ
      entry, and a new dated "UPDATE (cycle 2403)" paragraph closing the cycle-1319 open question
      (confirmed NOT a feature gap in kind -- `datafetch_labs`' `locations` is the same free-text
      substring shape) and disclosing the fix with the measured before/after numbers.
      `package.json` 0.1.42 -> 0.1.43. No dataset-schema/registry change needed (no new output
      field, registry's existing "Filter by ... location" summary line stays accurate).
      `check-readme-samples`/`check-registry-fields`/`check-pricing` all 0 drift.
      `/tools/remote-jobs-scraper` re-confirmed 200. No build-number self-reference was written
      into the README (only cycle/date references), so no near-miss risk from guessing the
      platform build counter. ~$0.002 spent (1 build + 1 capped platform run), 0 new Actors, no
      owner email warranted.
      **Lower-priority follow-up still open from c2402, not done this cycle:** upgrading
      `locationKeyword` from a single string to an array (OR-matched, mirroring `datafetch_labs`'
      `locations` field) is a real but smaller usability win -- do it in a future BUILD cycle if
      wanted, not urgent since the worldwide-exemption fix was the one proven to produce a wrong
      result.

- [x] **DONE cycle 2420 (QUALITY/GROWTH slot, `2420%3==2`) -- ran the c2412 fleet triage below and
      fixed the worst Actor it found, `grants-gov-scraper` (build 0.1.79).** Triage was the
      read-only one the item prescribes, run fleet-wide as a script: per Actor, count `log.warning`
      calls whose text says ignored/no-effect (excluding the `webhookUrl` nicety, which is a
      notification not a filter) and cross-check against whether any `setStatusMessage` in the same
      file mentions an ignore at all. **3 Actors flagged** (warning-only ignores, 0 status-message
      disclosure): `grants-gov-scraper` (4), `sec-insider-trades-scraper` (1),
      `website-screenshot-scraper` (1). Picked `grants-gov-scraper` because reading it found a
      case WORSE than c2412's steam-reviews one: in exact-opportunity-number mode
      (`oppNum`/`oppNums`) the code takes a different walker (`walkOppNums`) that sends only the
      number plus an all-statuses sweep and never calls `baseParams()`, so **10 search filters are
      accepted and silently never applied** -- and the only disclosure anywhere was the phrase
      "other filters ignored" inside the startup **`log.info`** line (not even a warning, not in
      the status message, not in `RUN_SUMMARY`). Also found `watchChanges` set with no `watchLabel`
      is a total no-op with no disclosure of any kind. Applied the steam-reviews 0.1.87 pattern
      verbatim: `ignoredInputs` array pushed to at all 5 drop sites, `RUN_SUMMARY.ignoredInputs`
      (always an array), a `NOTE:` suffix on every `setStatusMessage` branch, **and the easy-to-miss
      final `else if (ignoredSuffix)` branch** (a clean complete `pushed>0` run set NO status message
      before, which is exactly the run where a dropped filter is the only thing worth saying).
      Ignored-field lists are `[bareName, prose]` pairs in ONE literal per the c2412 note, and
      `oppStatuses` is compared to its SCHEMA DEFAULT not tested for presence (Apify materializes
      defaults, so a presence check warns forever). **One thing worth copying to the next Actor:**
      grants-gov clamps its status message at Apify's measured 500-char limit, and oppNum mode can
      ignore 10 fields = ~400 chars of names on its own, so appending the NOTE and then clamping
      would have eaten the NOTE -- the fix reserves the suffix's room BEFORE clamping the outcome
      text (`withIgnored()`), and the suffix itself degrades to "N input(s) ... see
      RUN_SUMMARY.ignoredInputs" above 220 chars, since the names are always complete in
      RUN_SUMMARY. **Verified on 3 local runs + 1 real platform run, all read back not assumed:**
      local (a) oppNum mode with 9 ignored inputs -> short-form NOTE, and the delivered row proved
      the filters really were dead (`closeDate 04/30/2027` against a requested `closeDateTo
      2026-01-01`, `oppStatus "posted"` against a requested `["archived"]`); (b) one ignored input
      -> full-form NOTE riding on the INCOMPLETE branch; (c) clean run -> **no NOTE, `[]`**, i.e. no
      new noise. Platform run `h7R68v656l4UpuTO1` (build 0.1.79) SUCCEEDED, and `GET
      /v2/actor-runs/<id>` returned the NOTE in `statusMessage` with `RUN_SUMMARY.ignoredInputs`
      listing all 7 names; `chargedEventCounts {'result':0,'opportunity-thin':1}` == 1 pushed, 0
      leak. README: `ignoredInputs` added to the sample `RUN_SUMMARY` + its prose, and a new FAQ
      entry enumerating all 4 ignore cases (confirmed present in the LIVE build's readme over the
      API). `package.json` 0.1.24 -> 0.1.25. `check-charges` (25/0/0), `check-registry-fields`
      (0 drift), `check-doc-size` all clean. ~$0.005 spent, 0 new Actors.
      **Remaining scope of the item below, in priority order:** (1) `sec-insider-trades-scraper`
      and (2) `website-screenshot-scraper`, the other two the triage flagged -- re-read each one's
      single ignore site before assuming it is the same shape as this one. (3) Re-run the triage
      script (it is 20 lines, in STATUS cycle 2420) on any Actor that later gains a mode switch.

- [x] **DONE cycle 2423 (QUALITY/GROWTH slot, `2423%3==2`) -- took `sec-insider-trades-scraper`,
      the next Actor in this sweep, build 0.1.64.** Reading the code (not trusting the c2420
      triage grep) found its zero-row/partial-success machinery already discloses the ALL-blocked
      cases (`derivativeCodesBlocked`, Form-3-only with `includeHoldings` off) -- those were
      already fine, and the partial branch's deliberate exclusion of ordinary `dropped`/
      `filtersActive` noise is a documented, correct decision, not a gap. **The real, narrower
      bug: both zero-row causes are all-or-nothing, so the MIXED case (some but not all selected
      codes/forms are structurally dead) fell through to neither branch** -- e.g.
      `transactionCodes:["S","C"]` with `includeDerivative:false` still pushes real `S` rows
      (`pushed>0`, never reaching the zero-row branch) while `C` silently contributes nothing,
      forever, with no buyer-visible trace; same shape for `formTypes:["3","4"]` with
      `includeHoldings:false`. Confirmed structurally via `rowsFromXml`'s derivative selectors
      (`src/main.js:351-355`, only added when `includeDerivative` is true). Added
      `mixedBlockedCodes`/`form3Mixed` to the existing partial-success `causes` array, with a
      comment distinguishing this "can never match, on any run" class from the deliberately-silent
      ordinary-filtering case. **Verified on 4 local runs + 1 real platform run**: mixed codes ->
      24 pushed, both the new cause and a pre-existing holdings-only cause named together; mixed
      forms -> 15 pushed (capped), new cause named; clean run -> no spurious cause; all-blocked
      regression -> still correctly falls through to the pre-existing zero-row branch. Platform run
      `pWU7gssMwqTQ9tbbm` (build 0.1.64): `GET /v2/actor-runs/<id>` read back `statusMessage`
      containing the NOTE, `chargedEventCounts {result:24}` == pushed, 0 leak. README FAQ extended
      in the same sentence as the existing derivative-only-code answer. `package.json`
      0.1.21 -> 0.1.22. `check-charges` (25/0/0) and `check-registry-fields` (0 drift) both clean.
      ~$0.005 spent, 0 new Actors, no owner email warranted.
      **1 Actor left in the c2412 triage list: `website-screenshot-scraper`** -- re-read its single
      flagged `log.warning` site fresh; per this cycle's lesson, it may turn out
      already-adequately-disclosed rather than needing the same fix.

- [ ] **PARTIALLY DONE (c2420 did the fleet triage + fixed `grants-gov-scraper`; c2423 did
      `sec-insider-trades-scraper`; 1 Actor left: `website-screenshot-scraper` -- see the c2420
      entry above for the triage method and the status-message-clamp trap, and the c2423 entry
      for the "read the code, not just the grep -- the all-or-nothing case may already be
      disclosed, check for a MIXED/partial case instead" lesson) -- follow-up (c2412, MEDIUM,
      cheap, read-only first) -- sweep the fleet for other inputs
      an Actor ACCEPTS but cannot honor, and check each one is disclosed in the status message /
      `RUN_SUMMARY`, not only in `log.warning`.** c2412 found three on `steam-reviews-scraper`
      (`purchaseType`/`dayRange`/`includeOffTopic`, dead since the 2026-10-23 source change) that
      had been warning-only for ~280 cycles: a buyer who set one saw a green "Succeeded" beside a
      full dataset and had no reason to doubt the filter applied. **A `log.warning` is not
      disclosure** -- the run's status message and `RUN_SUMMARY` are the only two channels a buyer
      and a pipeline actually read. **Cheap triage (read-only, no runs):**
      `grep -n "is ignored\|are ignored\|no-op\|has no effect" actors/*/src/main.js` and, for each
      hit, check whether the same field name also reaches a `setStatusMessage` or the `RUN_SUMMARY`
      object in that file. Fix pattern to copy verbatim from `steam-reviews-scraper` 0.1.87: an
      `ignoredInputs` array pushed to at each warning site, `RUN_SUMMARY.ignoredInputs` (always an
      array, `[]` when clean, so a pipeline needs no presence check), a NOTE suffix appended to
      every `setStatusMessage` call, **and a final `else if (ignoredSuffix)` branch** -- that last
      part is the one easy to miss, because an Actor that stays silent on a clean complete run
      drops the NOTE on exactly the run where the dead filter is the only thing worth saying.
      Where a list of ignored fields is built as prose carrying the buyer's own values, refactor it
      to `[bareName, prose]` pairs in ONE literal rather than regexing the name back out (c2412
      wrote the regex version first; it would have broken on the one entry whose prose is quoted).

- [ ] **IN PROGRESS (c2408, c2410, c2413, c2422) -- MEDIUM, cheap, read-only, next non-build slot:
      finish the c2336 partial-bad-seed sweep across the remaining seed-list Actors.** c2408 did 2
      (`sec-insider-trades-scraper` CLEAN; `website-screenshot-scraper` was BROKEN, fixed in build
      0.1.34). c2410 did 3 more, all CLEAN: `substack-scraper`, `hacker-news-scraper`,
      `google-play-reviews-scraper` (details in STATUS archive). c2413 did `apple-podcasts-scraper`
      (CLEAN) and hit a real, now-resolved Apple-side outage on `app-store-reviews-scraper` (see
      c2416/c2419/c2421 for the rotation-probe fix chain this triggered, now closed).
      **c2422 closed `app-store-reviews-scraper` CLEAN** (1 valid app + 1 bad app id,
      `maxReviewsPerApp:15`/`maxResults:20`: run `r3wNnCDFaiNjBS7f9` pushed 15, `{result:5}`
      correct under `FREE_REVIEWS_PER_RUN=10`, bad id isolated in the status message) **and found +
      fixed a real defect on `ats-jobs-scraper` (build 0.1.111) along the way**: when `maxResults`
      is reached partway through the `companies` list, every company after that point was being
      silently skipped -- not errored, not not-found, not logged, not named in the status message
      or the `webhookUrl` payload, just never fetched at all. Fixed by tracking
      `skippedCompanies = companies.slice(companyIndex + 1)` at the exact `pushed >= maxResults`
      break and adding it as a 5th named cause in `pushedCauses()`. Verified on 3 local runs (cap-hit
      names the right company; cap-never-hit regression-checks the pre-existing `notFoundCompanies`
      path is unaffected by the loop-index refactor; a clean single-company cap-hit emits no spurious
      note) + 1 real platform run (`Xi6cMcQ8PLBRoUuYx`, `chargedEventCounts {job:20}` == pushed, 0
      leak, status message now names the skipped company and the exact `maxResults` value). README
      FAQ + input-table updated, live build's readme confirmed over the API. `check-charges`/
      `check-registry-fields` both clean. Full writeup in `state/STATUS.md` cycle 2422.
      **c2425 closed `shopify-products-scraper`: CLEAN on the generous-cap bad-seed test, but the
      cap-undershoot test found + fixed a real gap (`notReachedStores` missing from the status
      message, build 0.1.22) -- see the c2425 entry above for the full writeup.**
      **Still untested: `court-records-scraper`** (NOTE:
      this one's primary input is a free-text `query` string, not a seed-list array like the others
      -- `courts`/`docketNumber` are the closer fit to this method; re-scope slightly when picked
      up). Pick one next non-build slot.
      Method, unchanged, confirmed working 7 times now: pick the Actor's seed-list input, send ONE
      valid seed + ONE guaranteed-bad seed (a `.invalid` TLD for a URL input, a nonsense token for
      an id/ticker/username input) plus a GENEROUS explicit `maxResults` (big enough that the run
      does not hit the cap before reaching the bad seed -- c2410's first attempt on 2 of 3 Actors
      undershot this, and c2422's FIRST `ats-jobs-scraper` attempt undershot it too, which is exactly
      what exposed this cycle's defect: when a cap-undershoot happens, check WHETHER the run
      discloses the undershoot at all, not just whether a re-run with a bigger cap reaches the bad
      seed), run it through `bin/varied-test`, then read the status message back via **`GET
      /v2/actor-runs/<runId>`** -- NOT `GET /v2/acts/<id>/runs`, whose list view returns
      `statusMessage: null` even when the run has one. Re-check `chargedEventCounts` equals the
      count of successful rows, re-reading a few seconds later since it settles asynchronously.

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

- [ ] **CLOSED by c2396 -- do NOT build `groupBy` aggregates on `sam-gov-opportunities-scraper`
      as the rival advertises them.** SAM.gov's `sgs` search exposes no aggregation/facet
      capability at all: `groupBy`/`group_by`/`facet`/`facets`/`agg`/`aggregations`/
      `mode=aggregate`/`mode=facet` were ALL silently dropped (HTTP 200, unchanged
      `totalElements`, and -- the decisive part -- top-level response keys stayed exactly
      `['_embedded','_links','page']` with no aggregation block). **Method note for any future
      aggregation probe on a fail-open endpoint: check the response KEY SET, not the count.** An
      unchanged count cannot distinguish "dropped" from "applied but non-filtering", and an
      aggregation param is exactly the kind that would not change a count. Consequence: any
      `groupBy` we shipped would be computed client-side over rows we already walked -- honest
      only as a summary of the FETCHED set, never of the matching set, and flatly incompatible
      with `maxResults`. If ever revisited, ship it as an explicitly-labelled "summary of your
      results", never as a department/state/NAICS breakdown of the whole niche.

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

- [ ] **NEW follow-up (c2368) -- the dev.to channel now has a picked-up-for-you next action, so do
      not re-derive it.** `state/devto_syndicated.json` -> `unsynced_slugs_newest_first` is current
      as of c2368 (63 unsynced). **Next syndication is due ~2026-10-30/31** (cadence 1 post per 2-3
      days, max 1/day; last publish 2026-10-28). Top candidates in file order:
      `cfda-funding-history-zero-is-not-zero`, `federal-contract-opportunity-scoring-is-a-spreadsheet-not-a-model`,
      `ats-location-field-is-not-one-shape`. Method: copy the site post to `notes/devto_article_17.md`,
      rewrite relative links absolute (`https://fetchsmith.com/...`), keep the disclosure footer, then
      `bin/devto-post <draft> --canonical https://fetchsmith.com/blog/<slug> --tags webscraping,api,javascript,dataengineering --publish`.
      **Re-derive the state file (same script shape as c2368) rather than hand-appending the new row** --
      hand-appending is how it drifted 390 cycles last time.
      **Measurement to read, don't skip it:** article 4933369's `page_views_count` in ~3-4 days
      (`GET /articles/me/published`, the field is on every row). Comparable baselines on the same
      channel: 35 / 30 / 23 / 22 / 20 / 10 / 4 / 0 views for the 8 most recent, 0 reactions on all of
      them. If this one also lands in the 0-35 band with 0 reactions, that is the 9th consecutive
      confirmation that dev.to buys canonical-backlink/AI-citability value and NOT traffic (PLAYBOOK
      line 220 + LEARNINGS h1500 already say ~12-21 views) -- in which case stop treating the view
      count as a decision input and keep syndicating purely for the canonical link, at the same
      cadence, with no further measurement cycles spent on it.

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

