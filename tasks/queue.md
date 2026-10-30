- [ ] **TOP PRIORITY for the next BUILD slot (promoted from SECOND, c2453's finding) --
      `us-federal-awards-scraper` has an unclamped `Actor.fail()` at `src/main.js:1275` echoing an
      unbounded `watchLabel`. Full details carried below (search "found + measured c2453" item) --
      not re-copied here, just promoted to TOP now that the apple-podcasts item above it is DONE.**

- [x] **DONE cycle 2454 (BUILD slot, `2454%3==0`) -- fixed the TOP PRIORITY item: `apple-podcasts-scraper`
      silently ignoring `chartCount`/`useRssForFullArchive` out of scope, build 0.1.108 (package
      0.1.29 -> 0.1.31).** Added a `chartsOnlyIgnored` array (same idiom as `reviewOnlyIgnored`/
      `episodeOnlyIgnored`, c2219) gated on the c2204 default-trap-safe comparison
      (`input.chartCount !== undefined && Number(input.chartCount) !== 50 && dataType !== 'charts'`)
      and a direct `useRssForFullArchive === true && dataType !== 'episodes'` check (no default
      trap needed — schema default is `false`). **Verified the one thing c2452 flagged as unknown
      rather than assuming it:** grepped every call site of `scrapeEpisodes(` — exactly one,
      line 1318, reached only from the `else` branch of the `dataType` if/else-if chain that starts
      with `if (dataType === 'charts')`, so it is NEVER reachable when `dataType === 'charts'`
      (including `chartType: 'episodes'`, which enriches rows via `getShowEpisodeBundle()` instead
      and never calls `scrapeEpisodes()`). So the correct gate is `dataType !== 'episodes'` exactly,
      not `episodeFiltersApply` (which deliberately also covers charts+episodes for the *filter*
      fields, a different question).
      **Found and fixed a second, related bug while verifying on the platform, not from reading the
      diff:** the pre-existing chartCount cap-clamp warning (~line 144, "exceeds Apple's cap...
      fetching N") fired unconditionally regardless of `dataType`, so a non-charts run with an
      explicit `chartCount` above 100 got BOTH the clamp warning and the new ignored-scope warning
      back to back, contradicting each other in the log ("fetching 100" right next to "ignored,
      nothing was filtered"). Gated it on `dataType === 'charts'` too. Build 0.1.107 had only the
      first fix; 0.1.108 has both (second platform verification round below is on 0.1.108).
      **Verified at every level:** `node --check` clean; `./bin/check-mode-scope-warning
      apple-podcasts-scraper` 0 flags (was 2); 4 local runs — (a) `dataType:"reviews"` +
      `chartCount:200` + `useRssForFullArchive:true` fires both new warnings and NOT the clamp
      warning; (b) `dataType:"charts"`, chartCount omitted (defaults to 50) fires NEITHER warning
      (the c2204 regression test); (c) `dataType:"episodes"`, all defaults, fires neither; (d)
      `dataType:"charts"` + `chartType:"episodes"` + `useRssForFullArchive:true` fires the
      useRssForFullArchive warning (confirming it's genuinely dead there) and completes normally,
      5/5 rows pushed, no crash. **Then 2 real platform runs on build 0.1.108**, both SUCCEEDED:
      the forced-scope reviews run (`BqdKu6OWpuU3HQrdR`) logged both new warnings live and NOT the
      clamp warning, `chargedEventCounts {result:0}`; a clean default episodes run
      (`D6owxqSZtXzMknukh`) logged zero scope warnings, `chargedEventCounts {result:0}` (both $0
      because this Actor's free-per-run tier covers the 1-2 rows requested, not a billing lag,
      confirmed by reading the code). `check-charges` 25/0/0, `check-registry-fields` 0 drift (no
      output fields touched — this is a warning-only fix). Added 1 README FAQ entry explaining both
      scope restrictions in plain language, confirmed it's part of the pushed build. Services/site
      reconfirmed healthy after the push (`fetchsmith-web`/`fetchsmith-mail`/`caddy` active, `/` and
      `/tools/apple-podcasts-scraper` both 200). ~$0.01 spent (2 builds + 4 platform runs). 0 new
      Actors today.
      This closes the c2452 TOP PRIORITY item end-to-end and also closes c2452's "one thing the fix
      cycle must verify first" instruction (whether `scrapeEpisodes()` is reachable in the
      charts+episodes path — it is not, confirmed by grep + a live run).

- [ ] *(kept for reference only -- SECOND priority item, now promoted to TOP above; full detail
      retained here since the promoted entry doesn't repeat it)* **found + measured c2453, read-only QUALITY/GROWTH cycle --
      `us-federal-awards-scraper` has an unclamped `Actor.fail()` at `src/main.js:1275` echoing an
      unbounded `watchLabel`, the same bug class the 8-Actor sweep (c2437-c2446) and the 4-Actor
      watch-lock-contention fix (c2450/c2451) already closed elsewhere -- but this Actor was in
      NEITHER of those and has no `clampStatusMessage`/`echoCap` helper anywhere in the file (only
      one `Actor.fail(` call total, confirmed by grep).** Fires in the `seedFailure` branch, 2
      wordings depending on `timeBudgetExceeded`:
      `Seed walk for watch label "${watchLabel}" ran out of run-timeout budget and stopped early;
      baseline was not saved. Raise the run timeout or narrow the filters so the whole seed fits in
      one run.` (base 180 chars at `watchLabel:''`) or the API-failure variant (163 chars at
      `watchLabel:''`, "Re-run this exact seed (same label and filters) to try again."). Confirmed
      via `.actor/input_schema.json` that `watchLabel` is a plain `textfield` with **no
      `maxLength`**. **Measured exactly:** the message crosses 500 chars at a ~320-340 char label
      (timeout wording hits 500 at label len 320; API wording at ~337). Message order is
      `"...watch label \"${watchLabel}\"... baseline was not saved. <remediation sentence>"` --
      the billing-relevant "baseline was not saved" clause comes right after the label splice and
      stays intact through label length 400 in testing, but the trailing REMEDIATION sentence
      ("Raise the run timeout..." / "Re-run this exact seed...") is what gets silently dropped,
      measured to disappear once the label exceeds ~370-400 chars (580/563-char naive concat at
      label=400, remediation gone, cut at exactly 500). So the billing disclosure itself is safe at
      every label length tested, but a
      buyer with a long/automated `watchLabel` loses the actionable "what do I do now" sentence --
      same shape of harm as the already-fixed watch-lock-contention sites, lower severity than the
      sweep's worst cases (which dropped the disclosure itself).
      **Suggested fix:** port the fleet's `clampStatusMessage(msg, suffix='')` + `echoCap(s, max=60)`
      helpers (none exist in this file yet -- add them right after `const input`, this file's
      `Actor.fail()` fires late at line 1275 so TDZ is less of a risk than usual, but follow the
      established placement convention anyway) with base = the upstream-detail clause
      (`"Seed walk for watch label \"${echoCap(watchLabel)}\" ran out of ..."`, `watchLabel`
      `echoCap`'d to 60 since it's in the base alongside unbounded-length risk) and suffix = the
      remediation sentence ("Raise the run timeout..." / "Re-run this exact seed...").
      **Verify bar, same as every sweep Actor:** unit test reconstructing both worst cases (a
      300-400+ char label on both the timeout and API-failure wordings) proving OLD drops the
      remediation and NEW keeps it whole; a local run forcing the real branch (temporarily break
      the USAspending API endpoint or set an artificially tiny run-timeout budget -- check which is
      easier to force for real, reverting immediately after); `apify push --force -w 600` + 1
      platform run reading `statusMessage` back live; `check-charges` + `check-registry-fields`.
      **No code changed this cycle** -- this was a read-only QUALITY/GROWTH pass (c2453), consistent
      with c2437/c2450/c2452's discipline of not fitting a full fix-and-verify cycle into a
      discovery pass. This finding CLOSES the c2451 LOW-priority carried item ("~17 Actors' worth of
      other `Actor.fail()` call sites ... never individually measured") -- every other site in that
      generalized grep was checked this cycle and is either already `clampStatusMessage`-protected
      (apple-podcasts/app-store-reviews/grants-gov/hacker-news/nih-reporter/sam-gov/uk-find-a-tender,
      all pre-existing fixes) or inherently safe: fixed enum/field-name text, validated numbers, or
      a generic `` `Run failed: ${err.message}` `` catch-all with NOTHING after the interpolation to
      protect (Apify's 500-char cut just truncates the error detail itself, dropping no disclosure
      or remediation) -- confirmed this reasoning by reading every catch-all site's surrounding code
      (ats-jobs/fec-campaign-finance/remote-jobs/scholarship/sec-insider-trades/trademark-search/
      website-screenshot x3/steam-reviews). The ~17-Actor item is therefore CLOSED, net of this one
      new finding.

- [ ] **TOP PRIORITY for the next BUILD slot (found + measured c2452) -- `apple-podcasts-scraper`
      silently ignores `chartCount` and `useRssForFullArchive` out of scope. Real, live, buyer-
      visible instance of the exact c2219/c989 bug class, on the SAME Actor c2219 already fixed
      eight sibling fields on.** Found by the tightened `check-mode-scope-warning` shipped this
      cycle (see the DONE entry above) -- it is the first time that tripwire has flagged anything
      the fleet did not already know about, and both flags survived manual confirmation:
      **(1) `chartCount`** (schema: "Charts only: how many chart entries to fetch...") is read only
      at `src/main.js:68` (`chartCountRequested`) -> `:143` (`chartCount`) -> `:1149/:1150` (the two
      chart URL builders). In any `dataType` other than `charts` it is dead. The ONLY warning that
      names it (`:145`) is the cap-clamp warning, which fires solely when the value exceeds
      Apple's 100/200 ceiling and says nothing about mode. There is no `chartsOnlyIgnored` array in
      the file at all -- c2219 built `reviewOnlyIgnored` (`:189`) and `episodeOnlyIgnored` (`:205`)
      and a charts-only equivalent was simply never written.
      **BEWARE THE c2204 DEFAULT TRAP HERE -- `chartCount` carries `default: 50` in the schema**
      (verified by reading `.actor/input_schema.json` directly this cycle), so Apify materializes
      50 into `input` on every run that never mentions the field, and a bare truthiness/
      `!== undefined` test would warn on EVERY non-charts run -- which is the trap that already
      bit `sort` (c2204) and `maxPodcastsPerPublisher` on this same Actor. Use the established
      compare-against-the-default shape, i.e. `input.chartCount !== undefined &&
      Number(input.chartCount) !== 50 && dataType !== 'charts'`, exactly like `:221`.
      **(2) `useRssForFullArchive`** (schema: "Episodes only: fetch each show's own RSS feed...")
      is read only at `:155` (`rssFullArchive`), `:156` (the `perPodcastEpisodes` cap), `:318` (the
      RUN_SUMMARY echo) and `:948` -- and `:948` is inside `async function scrapeEpisodes(id)`.
      Four warnings quote the field name (`:926`, `:936`, `:1360`, `:1400`) but every one of them
      is unrelated advice ("turn it ON to reach further back", or the `explicitFilter` interaction)
      -- none fires because the field was ignored. `default: false`, so unlike `chartCount` a plain
      `input.useRssForFullArchive === true` test is already non-default-safe.
      **ONE THING THE FIX CYCLE MUST VERIFY FIRST, do not assume it:** the right gate is probably
      `dataType !== 'episodes'`, but `episodeFiltersApply` (`:188`) deliberately also covers
      `dataType === 'charts' && chartType === 'episodes'`, and it is NOT established that
      `scrapeEpisodes()` is reachable in that charts-episodes path. **Grep the call sites of
      `scrapeEpisodes(` and gate on what the code actually does**, then word the warning to match
      (if it IS reachable there, reuse `episodeOnlyIgnored`/`episodeFiltersApply` rather than
      writing a third array).
      **Suggested implementation:** add a `chartsOnlyIgnored` array in the `:189`-`:216` idiom for
      (1) and fold (2) into whichever existing array its real gate matches -- both warnings must
      contain an IGNORE_WORD the tightened checker recognises (`ignored` / `only applies` /
      `nothing was filtered out`, same wording as the siblings) or the check will stay red.
      **Verify bar, unchanged from the sweep:** `node --check`; local runs forcing BOTH new
      branches (e.g. `dataType: 'reviews'` + `chartCount: 200` + `useRssForFullArchive: true`
      -> both warnings; and a clean `dataType: 'charts'` run + a clean default-everything run
      -> NEITHER warning, which is the c2204 regression test and the one most likely to fail);
      then `./bin/check-mode-scope-warning apple-podcasts-scraper` must print **0 flags**; then
      `apify push --force -w 600` + 1 real platform run reading `statusMessage`/log back live;
      then `check-charges` + `check-registry-fields`. Also fold in the README copy BEFORE the push
      (c2288/c2436 ordering lesson) -- and note `apple-podcasts-scraper` is one of the two Actors
      in the open c2436 item, so that item does NOT batch into this push (that one is
      `fda-recall-scraper` + `grants-gov-scraper`).

- [x] **DONE cycle 2452 (BUILD slot, `2452%3==1`) -- ran the DUE `git-maintain` and then closed the
      c2424 MEDIUM item by tightening `bin/check-mode-scope-warning`, which immediately found 2
      real live defects (now the TOP PRIORITY item above).** `git-maintain`: tripped on loose size
      (84 MiB >= the 64 MiB threshold, 2067 loose objects), repacked single-threaded at nice 19 --
      loose 2067 -> 0, pack 103 -> 112 MiB, `.git` now 115M, all 3 services active afterwards.
      Recorded via `bin/checks-due --ran git-maintain`, next due cycle 2500. It was the ONLY due
      fleet check; `audit-due --all` showed none due (soonest `google-play-reviews-scraper` in 4c).
      **Then did c2424's option (a)** -- require the field name to appear in a warning whose text
      also carries an ignore-word, instead of ANY warning -- **and followed c2424's own instruction
      to measure the new flag set on the whole fleet BEFORE changing the tool.** Baseline: 25
      Actors, 44 mode-scoped fields, 0 flags. First cut of (a) (ignore-synonyms only): 5 flags
      across 3 Actors -- small enough to read, so the "tripwire nobody reads" risk c2424 worried
      about did not materialise. 3 of those 5 were then confirmed FALSE POSITIVES by reading the
      code, and each one taught the fix: `google-news-scraper`'s `publishedAfter`/`publishedBefore`
      DO have a real disclosure warning (`:147`-`:148`) that says "nothing is filtered out" /
      "comes back unfiltered" and never says "ignored" -> the ignore-word vocabulary has to be the
      fleet's own, not a guessed synonym list; `fec-campaign-finance-scraper`'s `committeeId` has a
      real one too (`:112` `Ignoring committeeId "${committeeIdInput}"`) but names the field in
      PROSE ONLY -- the quoted span is the value and the interpolated identifier is
      `committeeIdInput`, so neither `QUOTED` nor `INTERP_IDENT` ever sees `committeeId`, and
      baseline was green on it only via a wholly unrelated network-error warning at `:624`
      (`candidate name lookup failed for committee ${committeeId}`) -- i.e. green for exactly the
      wrong reason, which is the c2424 defect stated precisely.
      **Shipped fix = two composed changes, neither safe alone:** an `IGNORE_WORD` gate on each
      `.warning(` call (text + enclosing `for` header), plus bare-identifier matching allowed ONLY
      inside a call the gate accepted. The docstring's standing warning against bare-word matching
      (400+ reachable names per Actor, both historical bugs silenced) was measured on UNGATED
      calls; gated, apple-podcasts' reachable set went 34 -> 94 names, nowhere near the blowup, and
      both false-positive classes cleared.
      **Re-measured against BOTH historical bugs under real fault-injection before shipping, not
      from the diff** (reconstructed pre-fix sources in /tmp by deleting the actual fix blocks out
      of the live files, then ran both tools over the same pair via `--main`/`--schema`): c989
      (`fec`, 7 fields stripped out of the warning table + the 4 standalone amount/date warnings)
      -> **14 flags, byte-identical to the old tool**; c2219 (`apple-podcasts`, the whole
      `reviewOnlyIgnored`/`episodeOnlyIgnored` block deleted) -> **10 flags vs the old tool's 6**.
      The tightened tool is therefore strictly more powerful, and the gap is itself a finding: the
      old tool misses `minReleaseDate`/`maxReleaseDate` even in the c2219 PRE-FIX state, so 2 of
      the 8 fields of the very bug it was written for were never actually covered by it.
      **Fleet after shipping: 2 flags, both on `apple-podcasts-scraper`** (`chartCount`,
      `useRssForFullArchive`), both manually confirmed real and both queued with exact line numbers
      + the c2204 default trap flagged. **No Actor code was changed and no build was spent** -- the
      sweep's bar (local runs forcing both branches, the clean-run c2204 regression test, platform
      run, check-charges) does not fit what was left of the budget, same discipline as c2437/c2450.
      Preflight: inbox 10, same pattern as every recent cycle (2 long-resolved owner threads
      `dc593cfb`/`2b237f1b`, 3x DMARC, 2x TinyGate, 2x Actor-rental + 1 IP-lease spam), 0 new
      actionable mail. `bin/revenue` unchanged ($0, 25 public Actors, 49 users, 775 runs30d).
      `bin/traffic`: still 1 verified out_click total, 0 API calls -- the Polar buyer-intent gate
      (>100/day to /pricing or /tools) is nowhere near met, so no owner email. Services all active,
      `/` 200. ~$0 spent (no builds, no platform runs). 0 new Actors today.
      **Also fixed a stale queue entry:** the c2408/c2410/c2413/c2422 partial-bad-seed sweep item
      still read "Still untested: court-records-scraper" even though c2426 closed that Actor and
      declared the sweep fleet-wide CLOSED -- marked done rather than left to mislead a future
      cycle into re-running it.

- [x] **DONE cycle 2451 (BUILD slot, `2451%3==0`) -- fixed all 5 fix-sites in the 2 new
      `Actor.fail()` clamp shapes c2450 found (sites A+B), closing that queue item.** Ported the
      fleet's `clampStatusMessage(msg, suffix='')` + `echoCap(s, max=60)` reservation pattern into
      4 Actors that had neither helper yet (none of the 4 were touched by the original c2437-c2446
      sweep, so both consts were added fresh, placed right after `const input` in each file --
      `apple-podcasts-scraper`, `google-play-reviews-scraper`, `shopify-products-scraper`,
      `trademark-search-scraper`). **Site A** (watch-lock-contention, `acquireWatchLock`): all 4
      Actors, base = `Watch label "${echoCap(label)}" is already being processed by another run
      (started ..., run ...).`, suffix = the "Running the same watch label concurrently ...
      self-expires after 120 minutes)." sentence (exact wording per Actor preserved --
      "episodes"/"reviews"/"new/changed products"/"marks"). **Site B** (`apple-podcasts-scraper`
      seed-failure only, the worst measured case): base = `Baseline run for watch label
      "${echoCap(watchLabel)}" could not read N source(s) from Apple: ${echoCap(seedErrors.join(',
      '), 300)}.`, suffix = "The baseline was NOT saved ... re-run it on the same watch label to
      seed again." (full original wording kept in the suffix, now guaranteed to survive).
      **Verified live, not from the diff, for every one of the 5 fix-sites:** `node --check`
      clean on all 4 files; an isolated string-level unit test against both measured worst cases
      (5 long feed-URLs + 40-char label for site B: 484/500 chars, ends with the re-run advice; a
      300-char label for site A: 473/500 chars, ends with "self-expires after 120 minutes)."); then
      REAL fault injection against the actual shipped code for all 4 Actors' site A (seeded a fake
      `__lock` KV entry at the exact key the Actor itself computes -- discovered by running once
      un-seeded and reading the real key back out of the log, since 3 of the 4 Actors' fingerprint
      functions are nontrivial -- then reran with a 300-char `watchLabel`; all 4 produced the
      expected clamped message, byte-for-byte matching the code, all <=500 chars, full disclosure
      intact) and apple-podcasts' site B (5 unreachable long feed URLs as `podcasts`, local run,
      `Actor.fail()` fired at exactly 394 chars with the "baseline was NOT saved ... re-run" clause
      whole). **Then shipped and platform-verified**: `apify push --force -w 600` on all 4
      (apple-podcasts 0.1.106, google-play-reviews 0.1.97, shopify-products 0.1.107,
      trademark-search 0.1.86), 4/4 builds SUCCEEDED. 1 real platform run per Actor on its own
      `test_input.json` confirmed no regression (all 4 SUCCEEDED, rows pushed as expected) and 1
      platform run on apple-podcasts forcing site B for real (an unresolvable feed URL) FAILED
      with `statusMessage` read back live, matching the local run exactly (394 chars, disclosure
      intact, $0 charged). Site A was not forced on the platform itself (would need two genuinely
      concurrent runs racing on the platform, not just a seeded KV value) -- the 4x local
      fault-injection against the real shipped code already exercises the identical code path the
      platform would run, so this was judged sufficient given the cycle's time budget; flagged
      here rather than silently skipped. `check-charges` 25/0/0, `check-registry-fields` 0 drift
      (no output fields touched). Services/site reconfirmed healthy (all 3 active, `/` 200).
      ~$0.02 spent (4 builds + 5 platform runs), 0 new Actors today (pace rule untouched).
      **Follow-up still open, LOW priority, carried from c2450 verbatim (not re-verified this
      cycle):** `grep -rn 'Actor\.fail(' */src/main.js | grep -v 'watch baseline could not be
      completed'` still lists ~17 Actors' worth of OTHER call sites beyond the two shapes just
      closed, most reading as bounded on a skim (short static pre-charge guards, generic `Run
      failed: ${err.message}` catch-alls) but never individually measured -- treat as unverified,
      not cleared, if picked up in a future QUALITY/GROWTH cycle's read-only pass.

- [x] **DONE cycle 2450 (QUALITY/GROWTH slot, `2450%3==2`) -- ran the DUE `check-links` fleet
      check (CLEAN) and did the read-only `Actor.fail()` generalized-grep pass c2426 had queued for
      over 20 cycles, finding the real new bug class detailed in the TOP PRIORITY item above.**
      `check-links`: 152 pages crawled, 152 unique link targets, 152 unique assets, 29 intentional
      redirects resolved (26 outbound `/go/`, 3 internal `/checkout/`), 0 broken -- recorded via
      `bin/checks-due --ran check-links`, next due cycle 2786. No other fleet check was due this
      cycle (`checks-due --all` showed only this one DUE); `audit-due --all` showed none due either
      (soonest `google-play-reviews-scraper` in 6c). Preflight: inbox 10 checked, same pattern as
      every recent cycle (2 long-resolved owner threads, 3x DMARC, 2x TinyGate pitch, 2x
      Actor-rental + 1 IP-lease spam, 1 new rental reply thread `a661a19a` -- read, it is the same
      unsolicited rental-offer spam thread as `04dda4a1`, not a real buyer, no action) -- 0 new
      actionable mail, no owner email warranted. `bin/revenue` not re-checked this cycle (unchanged
      the last 6+ cycles running; the mail/revenue preflight budget went to the grep pass instead).
      Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active, `/` 200 (both
      re-confirmed directly, on top of the check-links crawl already exercising every page). 0 new
      Actors created today, 0 code changed (deliberately
      read-only, same discipline as c2437) -- the fix is queued above with exact file/line numbers
      and measured worst cases so the next BUILD slot spends its budget on diffs, not rediscovery.

- [x] **DONE cycle 2449 (normal slot, `2449%3==1`) -- published the follow-up for the shipped
      `diffRegions` feature on both surfaces.** Found the c2448 note's framing was slightly off on
      inspection: the site post never actually had a "Reader note" section (that pattern is dev.to
      -only, added via `PUT /api/articles` since dev.to has no comment-reply endpoint; the site
      mirrors reader-driven content as a normal `## Update, <date>:` section instead, same as the
      existing 2026-10-28 interior-sweep update already in that file). So the two edits were: (a)
      dev.to article 4933369 -- replaced the `## Reader note: @sid_mishra asked for a changed-region
      count...` section (which said the feature was NOT implemented) with `## Update (2026-10-30):
      shipped what @sid_mishra asked for...`, fetched via `GET` (with a `User-Agent` header --
      bare `urllib` gets a silent 403 from dev.to's edge WAF, `curl` is fine without one) and PUT
      back whole (200, body 7749 -> 8232 chars, confirmed live by re-fetching and checking the old
      "NOT implemented" text is gone); (b) added a matching `## Update, 2026-10-30: region counts
      shipped` section to `site/content/blog/visual-diff-threshold-cliff-not-curve.md`, same numbers.
      Both use the two measured results from STATUS.md cycle 2448: the equal-pixel-count demo
      (240x160 contiguous block vs 38,400 isolated pixels, both exactly `diffPixels: 38400` /
      `diffPercent: 4.0`, but `diffRegions` 1 vs 0 and `diffSpecks` 0 vs 38,400) and the real
      platform row `kFg6A0Blp01gjYpAD` (HN vs example.com at `diffThreshold: 0.1`: 6.3515%,
      `diffRegions: 3248`, largest 38,432 px, 643 specks) plus the plain caveat that two unrelated
      pages give thousands of regions since every text line is its own blob, so the field is for
      same-page-over-time checks, not cross-page comparison.
      Verified: `bin/check-blog-claims` (5+17+3+8 claims checked, 0 stale) and `bin/check-disclosure`
      (88 site posts + 25 dev.to articles, 0 missing) both clean after the edit; `/` and
      `/blog/visual-diff-threshold-cliff-not-curve` both 200, page HTML confirmed rendering both the
      new heading and the `diffRegions: 3248` figure. No push needed (content-only, no code change)
      -- committed the one changed file (`site/content/blog/...md`) directly.
      This closes the `diffRegions` feature end-to-end (code shipped c2448, now documented
      everywhere it was promised). No new Actor, no code change, 0 new Actors created today.

- [x] **DONE cycle 2448 (BUILD slot, `2448%3==0`) -- shipped the `diffRegions` feature on
      `website-screenshot-scraper`, closing c2447's candidate.** Builds 0.1.36 (code + schemas)
      and 0.1.37 (README + restored dataset_schema). Four new compare-mode output fields:
      `diffRegions` (4-connected blobs of changed pixels at/above a floor), `diffRegionsLargestPixels`,
      `diffSpecks` (sub-floor blobs ignored) and `diffRegionMinPixels` (echo of the floor used), plus
      a new `diffRegionMinPixels` input (default 4, clamped 1-10000).
      Implemented exactly as c2447 sketched: iterative stack-based flood fill (never recursive) over
      the diff mask pixelmatch ALREADY writes, so there is no second comparison pass. Decoding the
      mask is exact rather than heuristic -- with `includeAA: true` pixelmatch's AA branch is
      unreachable, so counted diffs are drawn in `diffColor` and matching pixels go through
      `drawGrayPixel` (r===g===b), making "not grayscale" an exact test. **That assumption is
      asserted at runtime, not trusted:** if the derived changed-pixel count ever disagrees with
      pixelmatch's own `diffPixels`, the Actor logs a warning and reports all four fields as `null`
      rather than a wrong number (`diffPixels`/`diffPercent` unaffected). Nulls, never 0, whenever
      the count can't be produced -- so "no regions" and "not measured" stay distinct. 40 MP cap
      with its own warning path.
      **BENCHMARKED ON THIS BOX BEFORE SHIPPING, as c2447 required** (1 vCPU / 2 GB): 1920x1080
      all-changed 222 ms / +11 MB; 1920x1080 checkerboard (~1M single-px blobs, the pathological
      component count) 34 ms; 1920x10000 all-changed 930 ms with a 38 MB peak stack. Marking pixels
      seen on PUSH (not pop) bounds each pixel to one stack entry, and the stack grows on demand
      instead of preallocating 4 bytes/pixel. No pathological case found.
      Verified: 5 hand-checked correctness cases (incl. 4-connectivity on a corner-touching
      diagonal); 15 real-pixelmatch configurations sweeping `diffThreshold` 0/0.02/0.05/0.1/0.3/1
      and the floor 1/2/10/500/10000, invariant `derived === diffPixels` held in ALL of them, plus
      an identical-image control; real platform run `kFg6A0Blp01gjYpAD` on 0.1.36 (HN vs
      example.com -> 6.3515%, `diffRegions: 3248`, largest 38,432 px, 643 specks; example.com vs
      itself -> exact zeros on every field) with `chargedEventCounts {result:2}` == 2 rows pushed
      and NO invariant/skip warning in the live log; default-input gate run `Rw3RS8eyCGdesaJRC`
      SUCCEEDED with a non-empty dataset. `check-charges` 25/0/0, `check-registry-fields` 27
      fields / 0 drift, `/` and `/tools/website-screenshot-scraper` both 200 with all four new
      fields rendering. ~$0.01 spent (2 builds), 0 new Actors today.
      **Trap hit and written up: `bin/gen-output-schema` DESTROYED this Actor's hand-maintained
      `dataset_schema.json`** (27 fields + `overview`/`compare` views -> 9 fields + 1 view) because
      it infers from a stale local screenshot-only dataset that never exercised compare mode.
      Restored via `git checkout` and re-applied by script. PLAYBOOK step 4b now carries a
      do-not-run gate, and LEARNINGS cycle 2448 has the general rule.
      Test persisted as `actors/website-screenshot-scraper/test_diff_regions.mjs` (added to
      `.actorignore` so it never ships in a build); it extracts `countDiffRegions` from
      `src/main.js` by text rather than copying it, so it cannot drift from the shipped function.
      **Remaining: the content follow-up (dev.to + site post still say "not implemented") -- see
      the open item above it.**

- [x] **DONE cycle 2446 (normal slot, `2446%3==1`) -- fixed `uk-find-a-tender-scraper`, item (8/8,
      the LAST item) of the `Actor.fail()` clamp-reservation sweep, build 0.1.92 (package 0.1.18 ->
      0.1.19). THE SWEEP IS NOW FULLY CLOSED.** Grepped fresh -- found exactly 3 `Actor.fail()`
      sites. (1) all-blank-array-value guard: echoes only `raw.length`/fixed field name, bounded,
      no change. (2) whitespace-only scalar-text guard (`searchQuery`/`buyerName`/`dateFrom`/
      `dateTo`, no schema `maxLength`): echoed the raw value verbatim, unbounded -- fixed with
      `echoCap(raw, 80)` inline. (3) watch-seed-failure site: bounded `seedFailure` + unbounded
      `watchLabel` (no `maxLength`) -- fixed with the fleet's `clampStatusMessage(msg, suffix='')`
      reservation, `watchLabel` `echoCap`'d to 60 chars in the suffix. Added both helpers (file had
      neither), declared right after `const input` since site (2) fires before any later `const`
      would exist (same TDZ trap every prior sweep Actor hit).
      Verified: unit test on both worst cases (2000-char whitespace echo on site 2; 1000-char label
      + 110-char upstream detail on site 3) -- OLD naive cut provably dropped the re-run advice on
      site 3, NEW code keeps both whole (374/469 chars); clean local regression vs the live FTS/
      Contracts Finder APIs (15 real rows); local runs forcing both unbounded sites for real
      (300-char whitespace searchQuery -> exit 1 at 374 chars; a temporarily-redirected `fts.api`
      host, nonexistent domain, reverted immediately, diff byte-identical, `node --check` clean ->
      genuine `ENOTFOUND` through the real retry loop, `Actor.fail()` fired at 389 chars, advice
      intact); 2 real platform runs on build 0.1.92 -- `crdYVMdyUt81u183L` (forced site-2) FAILED
      with `statusMessage` read back live at 374 chars matching the local run exactly,
      `chargedEventCounts {result:0}`; `FlH7jqKVQ03BYn7aT` (normal `test_input.json`) SUCCEEDED, 15
      rows pushed, `chargedEventCounts {result:0}` confirmed correct by reading the code (first 25
      rows/run are free, not a billing lag). `check-charges` 25/0/0, `check-registry-fields` 0
      drift. README FAQ entry added, confirmed live in the build payload. ~$0.01 spent, 0 new
      Actors today.
      **SWEEP CLOSED, 8/8 Actors fixed across c2437-c2446.** Full writeup in `state/STATUS.md`
      cycle 2446. **Next cycle: return to normal BUILD/QUALITY rotation (new Actor, or a
      competitor-gap audit) -- do not hunt for more sweep items.** Two small LOW-priority
      follow-ups remain open from earlier in the sweep, not urgent: (a) `court-records-scraper`'s 3
      pre-existing `setStatusMessage` sites (main.js ~1303-1329) never had their own clamp pass
      (c2438); (b) a read-only pass to check for an unclamped `Actor.fail()` outside the original
      10-Actor shared-string grep, under different wording (c2426, never acted on).

- [x] **DONE cycle 2445 (BUILD slot, `2445%3==0`) -- fixed `sam-gov-opportunities-scraper`, item (7)
      of the `Actor.fail()` clamp-reservation sweep, build 0.1.82 (package 0.1.26 -> 0.1.27).**
      Re-measured from a fresh grep per c2444's note -- found **11** `Actor.fail()` sites, the most
      of any sweep Actor. 8 bounded (enum/fixed field names, already-validated dates, numbers), no
      change needed. **3 genuinely unbounded, unclamped:** (1) `dateWindowInput`'s bad-date guard
      (~480) echoes `postedFrom`/`postedTo`/`deadlineFrom`/`deadlineTo` verbatim -- confirmed via
      the live schema these have no `maxLength`; (2) the all-punctuation `solicitationNumber` guard
      (~605) echoes it verbatim, same schema gap; (3) the watch-seed-failure site (~2517) had **no
      `clampStatusMessage` call at all**, concatenating `seedFailure` (can carry an unbounded
      upstream `err.message`) + free-text `watchLabel` (no schema `maxLength`) straight into
      `Actor.fail()`. Fixed (1)/(2) with the file's own pre-existing `echoCap()` helper (already
      used elsewhere in this file, just never wired into these 2 sites); fixed (3) by porting the
      fleet's `clampStatusMessage(msg, suffix='')` reservation + `echoCap`'d `watchLabel`. Also
      capped `err.message` in the retry loop (~303) at 120 chars via `echoCap`, closing the one
      unbounded upstream string feeding into (3) via `lastApiError` -> `incompleteDetail` ->
      `seedFailure`. No TDZ issue -- the helpers (~423-444) are declared before any of these 3
      sites actually execute.
      Verified: unit test on the watch-seed worst case (648-char naive concat -- OLD dropped the
      ENTIRE "no baseline was saved" sentence, NEW keeps it whole at 411 chars) and on sites
      (1)/(2) with a 2000-char adversarial echo (438/294 chars with `echoCap`); clean local
      regression vs the live SAM.gov API (`CRAWLEE_STORAGE_DIR`, not `APIFY_LOCAL_STORAGE_DIR` --
      PLAYBOOK note confirmed correct -- 15 real rows); local runs forcing all 3 sites for real,
      including a temporarily-redirected `SEARCH_API` (nonexistent host, reverted, diff
      byte-identical, `node --check` clean) that produced a genuine `ENOTFOUND` through the real
      retry loop; 2 real platform runs on 0.1.82 -- `meXVdwRKY45cBv6hc` FAILED with `statusMessage`
      read back live at 438 chars fully intact, `chargedEventCounts {result:0}`, and
      `JRiEgqduBn3yATY9P` SUCCEEDED with `{result:15}` == 15 rows pushed, 0 leak. `check-charges`
      25/0/0, `check-registry-fields` 0 drift (sam-gov's pre-existing note is explicitly marked
      "ok" by the check, unrelated). README FAQ added, confirmed in the push. ~$0.01 spent, 0 new
      Actors today.
      **1 Actor remains in the sweep: `uk-find-a-tender-scraper`** (measured <500 under an
      illustrative `watchLabel` by c2437 -- treat as a floor per every sweep Actor since
      `clinicaltrials-scraper`/c2440: grep it fresh for ALL `Actor.fail(` sites, read each one in
      full, and check every echoed free-text input against the live `.actor/input_schema.json` for
      a missing `maxLength` before ruling a site safe. This is the LAST item in the sweep -- once
      fixed, the clamp-reservation sweep across the fleet is complete; the next cycle after that
      should go back to normal BUILD/QUALITY rotation (new Actor or competitor-gap audit) rather
      than hunting for more sweep items.**

- [x] **DONE cycle 2444 (QUALITY/GROWTH slot, `2444%3==2`) -- fixed `nih-reporter-scraper`, item (6)
      of the `Actor.fail()` clamp-reservation sweep, build 0.1.65 (package 0.1.18 -> 0.1.19).**
      Grepped for ALL `Actor.fail(` sites first -- found **TWO**, not the one c2437 measured: (1) the
      all-invalid-`fiscalYears` input guard (~line 286, pre-charge) and (2) the watch-seed-failure
      site (~line 1569). Third sweep Actor in a row with an extra site the c2437 grep missed.
      Site (1) was the severe one and this queue had `nih-reporter-scraper` ranked as low-risk
      ("<500 under an illustrative watchLabel"): it echoes `JSON.stringify(input.fiscalYears)` and
      `fiscalYears` has **no schema `maxItems`** -- a 30-value worst case measured **627 chars**, and
      Apify's silent cut took BOTH the "different, unrelated, CHARGED query" warning and the
      "Nothing was charged" disclosure off the end. Site (2) measured 602 chars with a 229-char
      programmatic `watchLabel`. Fixed both with `clampStatusMessage(msg, suffix='')` + `echoCap`;
      had to MOVE the helpers from ~line 965 to just above `const input` (site (1) fires at ~286 --
      TDZ `ReferenceError` otherwise, same trap as c2440/c2442), and add `echoCap` (file had none).
      Verified: unit test on both worst cases (OLD provably dropped the disclosure at both, NEW
      keeps it whole at 269/467); clean local regression vs the live NIH API (3 real rows); local
      runs forcing BOTH sites for real (site 2 via a temporarily-nonexistent API path -> genuine
      HTTP 400 `InvalidApiVersion` from the live upstream, reverted, `diff` byte-identical,
      `node --check` clean); 2 real platform runs on 0.1.65 -- `IKBr3C9rL8Si4Zx1J` FAILED with
      `statusMessage` read back live at 479 chars fully intact + `chargedEventCounts {result:0}`,
      and `he6nMW97ZOUHNyBNU` SUCCEEDED with `{result:3}` == 3 rows pushed, 0 leak. Confirmed by
      reading the code that a seeding run never calls `pushResults`, so site (2)'s "nothing was
      charged" is accurate. `check-charges` 25/0/0, `check-registry-fields` 0 drift, `/` and
      `/tools/nih-reporter-scraper` 200. README FAQ added, confirmed live in the build payload.
      ~$0.01 spent, 0 new Actors today.
      **NEW METHOD CAVEAT for the rest of the sweep (full writeup in LEARNINGS, found by RUNNING
      the fix, not reading it):** the fleet's "caller text in the BASE needs no `echoCap`, the base
      truncates first" convention (established c2433, repeated c2434/c2435) **is wrong when the
      base text contains no spaces.** First version of site (1) followed it exactly and a real run
      printed `fiscalYears was given ...` -- naming NONE of the rejected values, because a JSON
      array has no spaces so `cut.lastIndexOf(' ')` fell back to the lone space in "was given" and
      binned the whole echo. Billing disclosure survived, diagnostic value did not. **So: `echoCap`
      any space-free caller echo (JSON arrays, ids, URLs, hashes) even in the base.** Check the two
      remaining Actors for this shape, and do not just trust the convention as written.
      **2 Actors remain in the sweep:** `sam-gov-opportunities-scraper` and
      `uk-find-a-tender-scraper` (each measured <500 under an illustrative `watchLabel` but
      genuinely unbounded, no schema `maxLength`) -- but note c2444 found the *illustrative-label*
      measurement understated the real risk on this Actor by missing a whole second site, so
      re-measure both from a fresh grep rather than trusting the c2437 numbers. Same verify bar.

- [x] **DONE cycle 2443 (normal slot, `2443%3==1`) -- fixed `hacker-news-scraper`, item (5) of
      the `Actor.fail()` sweep, build 0.1.95 (package 0.1.23 -> 0.1.24).** Grepped for ALL
      `Actor.fail(` sites first per c2442's reminder -- only one here (main.js:1317), so no
      second site this time. The `clampStatusMessage`/`echoCap` helpers already existed at the
      top of the file (added c2431) but were never wired into this call site, which concatenated
      an unbounded `seedFailure` (joined failed-query list) and a free-text `watchLabel` straight
      into `Actor.fail()` with no reservation. Ported the reservation: base = upstream failure
      detail, suffix = "no baseline was saved / nothing was charged" + re-run advice, `watchLabel`
      `echoCap`'d to 60 chars in the suffix.
      Verified: unit test reconstructing the worst case (3 long failed queries + 88-char
      watchLabel, 502-char naive concat) -- OLD code would have dropped the re-run advice; a local
      run forcing the real branch by temporarily pointing the Algolia URL at a nonexistent host
      (reverted immediately, diff confirmed clean) got a genuine `ENOTFOUND` through the retry
      loop and the clamp fired for real at 499 chars, suffix intact; a clean local regression
      against the live Algolia API (3 real rows); 1 real platform run (`JpHtYCY6oh7EKMktD`, build
      0.1.95) -- SUCCEEDED, `statusMessage` read back live, `chargedEventCounts {result:2}` ==
      pushed(2), 0 leak. `check-charges` 25/0/0, `check-registry-fields` 0 drift. README FAQ entry
      added in the same push, confirmed live. ~$0.005 spent, 0 new Actors today.
      **3 Actors remain in the sweep:** `nih-reporter-scraper`/`sam-gov-opportunities-scraper`/
      `uk-find-a-tender-scraper` (each <500 under an illustrative `watchLabel` but genuinely
      unbounded, no schema `maxLength`). Same pattern, same verify bar -- grep each for ALL
      `Actor.fail(` sites first (this cycle found only 1, unlike c2440/c2442's extra-site finds).

- [x] **DONE cycle 2435 (QUALITY/GROWTH slot, `2435%3==2`) -- fixed `clinicaltrials-scraper`,
      item (1) of the sweep, build 0.1.92 (package 0.1.31 -> 0.1.32).** Verified the source
      comment's claim at ~1593 that `truncationNote()` and `lookupShortfallNote()` "can never both
      be non-empty" -- TRUE: `truncationNote()` requires `baselineTruncated>0`, which only happens
      in a watch-seeding run, which requires `watchMode`, which requires `nctIds.length===0`
      (main.js:391); `lookupShortfallNote()` returns `''` whenever `nctIds.length===0`
      (main.js:1479). So the two never combine -- but `lookupShortfallNote()` ALONE (5-part worst
      case, 345 chars measured by c2432) plus a long `incompleteDetail` (`lastApiError`, up to
      ~210 chars on an HTTP-error detail) in the `!complete` branch's base can still exceed 500 on
      their own, and that branch's `clampStatusMessage(msg)` had no suffix-reservation capability
      at all (single-argument function). Also found a SECOND, genuinely unclamped site at the
      `baselineTruncated>0` branch (~1610, re-read fresh rather than trusting the ~1603 the prior
      measurement named) -- no `clampStatusMessage` call whatsoever, relying entirely on Apify's
      silent 500-char cut to protect `truncationNote()` against an unbounded `watchLabel`.
      Fixed both: ported the fleet's `clampStatusMessage(msg, suffix='')` reservation (reference
      impl `fec-campaign-finance-scraper/src/main.js:1114-1123`) and wired it into both sites, each
      passing its note(s) as the suffix. No `echoCap` needed on `watchLabel` -- it's in the base at
      both sites, not the suffix, so the base-truncates-first order already protects it (same
      reasoning as fec-campaign-finance-scraper/c2433 and nih-reporter-scraper/c2434).
      Verified: unit test reconstructing a worst case (298-char base with a long `incompleteDetail`
      + 344-char 5-part `lookupShortfallNote()`, 642 naive concat) -- NEW clamp kept the full
      suffix at 419 chars total; OLD append-after-clamp code (computed for comparison, not run
      live) would have produced 498 chars with the suffix entirely gone, confirming the bug was
      real. 2 local runs against the live ClinicalTrials.gov API: (a) clean regression (short
      search, no notes) byte-identical to pre-fix; (b) a mixed direct lookup (1 valid + 1
      not-found + 1 bad-format id, `maxResults:1`) -- the real `!complete` branch fired with
      `lookupShortfallNote()` intact, 270 chars total. Did not force a live repro of the
      `baselineTruncated>0` branch (`WATCH_KEEP=60000`, impractical in a cycle budget, same
      constraint c2433/c2434 hit) -- covered by the unit test's exact reservation-math
      reconstruction instead. **Plus 1 real platform run** (`47Xh0gMXHkcjhCe1W`, build 0.1.92,
      same input as local case (b)): `GET /v2/actor-runs/<id>` read back `statusMessage` at **270
      chars** live, note whole, `chargedEventCounts {result:1}` == pushed(1), 0 leak.
      `node --check` clean before the push. README FAQ extended with the reservation guarantee,
      confirmed present in the live build's `actorDefinition.readme` over the API. `check-charges`
      25/0/0, `check-registry-fields` 0 drift (pre-existing sam-gov note unrelated). Also recorded
      `check-doc-size` as run this cycle (it was DUE on the schedule, not failing): STATUS.md
      128.6KB/1580 lines and queue.md 97.9KB/1121 lines both read TRIM SOON (~16-19c headroom,
      projected past the trim line before the next scheduled look) -- deferred the proactive trim
      to a future QUALITY slot given this cycle's time budget; next check-doc-size due c2459.

- [x] **DONE cycle 2441 (QUALITY/GROWTH slot, `2441%3==2`) -- diagnosed and fixed the
      `trademark-search-scraper` live blocker, build 0.1.85 (package 0.1.23 -> 0.1.24).** The
      candidate fix this item itself suggested first (switch to residential proxy) was DISPROVEN
      by testing, not assumed to work: a standalone probe sending the Actor's exact request shape
      got HTTP 200 (not a transport error) with an F5/TSPD bot-detection JS challenge page
      instead of JSON on EVERY path tried -- direct, 2 Apify datacenter sessions, AND residential.
      Real fix: TMview's search API now requires a WAF session cookie that only a plain GET to
      the search page sets first (no JS executed -- not a headless-browser workaround). Added a
      shared `tough-cookie` jar, primed with one GET before the first POST and re-primed on every
      proxy rotation / direct fallback (cookies are tied to the exit IP). Also removed the error
      message's now-disproven "set proxyConfiguration to a residential group" advice, which was
      additionally inactionable -- this Actor's `input_schema.json` has no `proxyConfiguration`
      field a Console buyer could set. Verified: a real local run of the Actor's own code against
      the live API (hit the pre-existing flaky-exit-node timeout, rotated, then the fix fired and
      returned 23,252 declared matches / 3 rows pushed); a clean zero-match regression unaffected;
      2 real platform runs on build 0.1.85, both SUCCEEDED, `statusMessage` + `chargedEventCounts`
      read back live matching rows pushed (0 leak once the documented ~15s billing-aggregation lag
      is accounted for). `bin/actor-health --only trademark-search-scraper` now healthy;
      `check-charges` 25/0/0, `check-registry-fields` 0 drift. README FAQ entry added, confirmed
      live in the build payload. Full writeup in `state/STATUS.md` cycle 2441. **This Actor needs
      no further action unless the nightly probe flags it again** -- if it does, the pre-existing
      flaky-exit-node transport issue (unrelated to this fix) is the remaining known cause.

- [x] **DONE cycle 2442 (BUILD slot, `2442%3==0`) -- fixed `federal-register-scraper`, item (4) of
      the `Actor.fail()` sweep, build 0.1.64 (package 0.1.15 -> 0.1.16).** This Actor had TWO
      `Actor.fail()` sites, not the one the c2437 grep measured (same blind-spot class c2440 found
      on `clinicaltrials-scraper`): (1) the all-agencies-unmatched input guard (~line 312, fires
      BEFORE any API call or charge) echoes the unmatched list from a `stringList` with no
      schema `maxLength`, unbounded; (2) the watch-seed-failure site (~line 1101, the one c2437
      measured at 511 chars). Neither had any `clampStatusMessage` call. Fixed both: ported the
      fleet's `clampStatusMessage(msg, suffix='')` reservation, `echoCap()`'d the unmatched-agency
      list to 60 chars in the base of site (1) (remediation advice reserved as the suffix), and
      reserved the "no baseline was saved / nothing was charged" disclosure + re-run advice as the
      suffix on site (2) (upstream detail as the base). **Had to move
      `STATUS_MESSAGE_MAX`/`clampStatusMessage`/`echoCap` from their old location (~line 833, after
      the 5 `setStatusMessage` sites) to just under `Actor.init()`**, since site (1) fires at
      line ~312, long before the old declaration -- same TDZ concern c2440 hit on
      `clinicaltrials-scraper`. Also capped the one remaining unbounded upstream interpolation,
      `request failed: ${err.message}` (network-error retry path), at 120 chars to match every
      other upstream-body interpolation already in this file.
      Verified: unit test reconstructing both worst cases (30 long bogus agency names on site 1;
      a 120-char capped `lastError` with `isInputError` true on site 2) -- old naive
      `(base+suffix).slice(0,500)` provably drops the remediation clause at exactly 500 chars on
      site 2, new reservation keeps both intact (420/393 chars); a clean local regression against
      the live Federal Register API (12 real rows, unaffected `setStatusMessage` branch); a local
      run forcing site (1) for real (2 bogus agency values, message intact, well under budget); a
      local run forcing site (2) for real by temporarily pointing `API` at a broken path to force
      an HTTP 404 from the live upstream (reverted immediately after, `node --check` clean) --
      message read back at 477 chars with the raw HTML error body truncated mid-base (the
      `" ..."` marker) and the full billing disclosure + remediation intact at the end; 1 real
      platform run (`vPcqYjduLuCNPpyKx`, build 0.1.64, same bogus-agency input as the local site-1
      test) -- FAILED as expected, `statusMessage` read back live at 414 chars, full message
      intact, `chargedEventCounts {result:0}`, 0 leak. `check-charges` 25/0/0,
      `check-registry-fields` 0 drift, `/` and `/tools/federal-register-scraper` both 200. README
      FAQ extended with 2 new entries (the all-unmatched hard-fail case, the watch-baseline-failure
      case) in the same push.
      **4 Actors remain in the sweep, severity order unchanged:** `hacker-news-scraper` (504+),
      `nih-reporter-scraper`/`sam-gov-opportunities-scraper`/`uk-find-a-tender-scraper` (measured
      <500 under an illustrative label but genuinely unbounded, no schema `maxLength` on
      `watchLabel`). Same pattern, same verify bar. **Keep grepping each Actor for ALL
      `Actor.fail(` sites, not just the shared seed-failure string** -- this is now the second
      sweep Actor (after `clinicaltrials-scraper`) with an extra site the original c2437 grep
      missed, so treat the per-Actor counts from c2437 as a floor, not a total, on the remaining 4
      too.

- [ ] *(superseded by the DONE entry above -- kept for the diagnosis detail only)*
      ~~TOP PRIORITY c2441 -- `trademark-search-scraper` is FAILING on the platform, REPRODUCED
      twice (nightly health + a c2440 re-probe ~5 min later).~~ Runs `H3faDD0y7eQPT4JyZ`
      (21:05:48Z, nightly) and `4jGPrApTlc9GJY8oz` (21:10:39Z, c2440's re-probe), both build
      0.1.83, both `exitCode 1`, both with the SAME statusMessage: *"Could not reach TMview
      (tmdn.org) through any network path this run: 3 Apify Proxy session(s) and a direct
      connection all failed transport-level -- last error: The operation was aborted due to
      timeout."* So this is NOT the one-off transient that wording was written for -- two
      independent runs 5 minutes apart exhausted all 4 routes (3 proxy sessions + direct).
      **Good news, and the reason this is not an emergency: the Actor fails SAFELY.** Both runs
      charged `{result: 0}` -- a buyer gets a FAILED run with an accurate, actionable message and
      no bill, not silent garbage. The 500-char clamp work this sweep has been doing is exactly
      what keeps that message intact. Nothing to refund, nothing misleading live.
      **Diagnosis to do FIRST next cycle (do not start by editing code):** (a) probe `tmdn.org`
      from this box directly AND through each Apify Proxy group to find out which routes are
      actually dead now -- but note c2406's finding that this box's own direct IP is
      Akamai-challenged (`tmdn.org/error/revise.html`), so a direct-from-box failure proves
      nothing about the proxy path; (b) check whether TMview changed its edge (Akamai Bot Manager
      now rejecting datacenter ranges wholesale would make the current DATACENTER-group default
      permanently dead, not transient); (c) `bin/usage-trend --since` on this Actor to see when
      the failures began -- if they are days old, the "re-run in a few minutes" advice in the
      status message is now WRONG and misleading a buyer, which makes the copy a bug of its own.
      **Candidate fixes in order of cost:** switch the default `proxyConfiguration` to RESIDENTIAL
      for this Actor (the status message already tells buyers to do this by hand, which is an
      admission the default is wrong -- but check the residential price delta against the PPE
      price first, it may not be affordable at our per-result price); raise the proxy session
      count / retry budget; or, if TMview's edge is now categorically closed to Apify ranges,
      treat it as the same structural wall as zillow/etsy (c2107) and consider retiring or
      re-scoping the Actor rather than shipping a product that cannot run. **This outranks the
      remaining clamp sweep** -- a 25-Actor fleet with one Actor that cannot complete a run is a
      bigger revenue/reputation problem than a status message that might get cut.
      NOTE on method (c2440): `bin/actor-health` takes ONLY `--only <slug>`; it IGNORES positional
      args, so `bin/actor-health check-charges` silently re-runs the FULL billable fleet probe
      instead of the named check (that is what happened this cycle, ~25 real platform runs of
      spend for nothing). The real checks are standalone: `bin/check-charges`,
      `bin/check-registry-fields`. Use `bin/actor-health --only trademark-search-scraper` to
      re-probe just this one.

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

- [x] **DONE cycle 2436 (normal slot, `2436%3==0`) -- the c2428 clamp-reservation sweep is
      CLOSED, 10/10 Actors.** Took both remaining items in one cycle; the queue's guess that they
      might be "no change needed" was WRONG for both, and for a reason the whole sweep had been
      blind to (see the new follow-up below).
      **(1) `fda-recall-scraper`, build 0.1.82 (package 0.1.30 -> 0.1.31).** The premise inherited
      from c2432 -- "98-char `truncationNote()`" -- was itself wrong: re-reading the file fresh
      (per c2434/c2435's warning) showed `truncationNote()` at main.js:260 is interpolated ONLY
      into two `log.info` calls (1322, 1328) and never reaches a status message at all, so there
      was no note to reserve. The real gaps were elsewhere: (a) the `firstIncomplete` branch had
      NO clamp, measured **903 chars** worst case (4-cause `short` 125 + an `incompleteDetail` of
      642, the seed-walk-failed wording with `lastApiFailure` carrying up to 310 chars of upstream
      HTTP body) -- Apify's cut deleted both the "re-run the seed before relying on it" remediation
      AND the RUN_SUMMARY pointer; (b) the zero-row watch branch WAS clamped, but the change-blind
      NOTE was concatenated into the base, so a 200-char `watchLabel` (no schema `maxLength`)
      rendered **568 -> 493 with the NOTE gone** -- a monitor that can never report a change
      reading byte-identical to a healthy quiet run, which is the exact defect the Actor's own
      `watchChangeBlindFilters` code was written to prevent. Fixed by porting the reserving
      `clampStatusMessage(msg, suffix='')`, making the RUN_SUMMARY pointer and the change-blind
      NOTE reserved suffixes, adding `echoCap()` on `watchLabel`(60)/`recallNumber`(40)/
      `eventId`(40) in the message only (logs and the watch record keep full values), and capping
      `lastApiFailure` at 120 chars so upstream noise cannot displace the Actor's own billing prose
      after it (the full body stays in the `log.warning` immediately above). **Deliberately left
      ONE site unclamped and said so: the `baselineTruncated` branch measures a 223-char max bound
      (static + numeric only, no user strings), so a diff there would be cost without benefit
      (c2219).**
      **(2) `grants-gov-scraper`, build 0.1.80 (package 0.1.25 -> 0.1.26).** Confirmed the queue's
      read that `withIgnored` (main.js:1536) already reserves `ignoredSuffix` correctly, so all 5
      `setStatusMessage` sites needed NO change -- but its `Actor.fail()` did (below). Used this
      file's own `clampStatusMessage(msg, max)` reservation idiom rather than importing the
      fleet's second-argument-is-a-suffix variant, to keep one convention per file.
      Verified: 22-assertion unit test on `fda-recall-scraper` reconstructing every measured worst
      case -- including an assertion that the OLD single-argument form really did drop the NOTE,
      and a no-suffix byte-identical passthrough check -- plus 7 assertions on `grants-gov-scraper`
      (incl. the modest case being byte-identical to the old output); local runs forcing each
      branch for real (a patched-endpoint copy returning a non-JSON 200 to reach the seed-failure
      path, a 200-char `watchLabel` to make the clamp fire, clean 6-row and 5-row regressions with
      40- and full-field rows); platform runs `UNqntv7K49EmAOgfW` (seed, silent by design) and
      `nLkJ3rtcc4mrcYTY1` -- `statusMessage` read back live at 400 chars with the NOTE intact and
      the label capped at 60+`...`, `chargedEventCounts {result:0}` == pushed(0) -- and
      `PnbO97KBFRz5shAKD` (224 chars, charged 5 == 5 rows, 0 leak). `check-charges` 25/0/0,
      `check-registry-fields` 0 drift, `/tools/fda-recall-scraper` + `/tools/grants-gov-scraper`
      both 200. Full writeup in `state/STATUS.md` cycle 2436.

- [x] **DONE cycle 2437 (normal slot, `2437%3==1`) -- the read-only `Actor.fail()` measurement
      pass c2436 asked for. Read-only this cycle on purpose (per c2436's own instruction) --
      found the bug class is BIGGER than the 2 Actors already fixed, across every Actor sharing
      the `"The watch baseline could not be completed: ..."` seed-failure message
      (`grep -ln 'watch baseline could not be completed' */src/main.js` -> 10 Actors; 2
      already fixed this sweep leave 8 unmeasured).** All 8 share something WORSE than
      `fda-recall-scraper`/`grants-gov-scraper` had before c2436's fix: zero `clampStatusMessage`
      call of ANY kind at the `Actor.fail()` site -- a bare template literal straight into
      `Actor.fail()`, relying entirely on Apify's silent 500-char cut. Measured each (worst
      case, read code only, no runs):
      - **`court-records-scraper` (main.js:1378) -- 805 chars**, the worst in the fleet. Two
        walkers (docket + opinion) can both fail in the same run, and the message joins BOTH
        walkers' `lastError` (each up to ~130 chars of upstream HTTP detail) plus a 100+-char
        explanatory clause -- the cut lands well before the "nothing was charged" / re-run advice.
      - **`eu-ted-tenders-scraper` (main.js:902) -- 594+ chars** on a 300-char `body.message`,
        and that interpolation (main.js:625, `TED returned an API error on baseline page N:
        ${body.message}`) has NO `.slice()` at all, unlike every other upstream-body
        interpolation in this fleet -- genuinely unbounded, not just "large."
      - **`clinicaltrials-scraper` (main.js:1682) -- 580 chars.** A THIRD site on an Actor
        already touched twice this sweep (c2435 fixed 2 `setStatusMessage` sites) -- this
        `Actor.fail()` call was never in scope because the c2435 triage also grepped
        `setStatusMessage` only, same blind spot c2436 found on fda-recall/grants-gov.
      - **`federal-register-scraper` (main.js:1091) -- 511 chars**, `lastError` capped at 120
        (one of the few actually-bounded interpolations) but still over the ceiling with the
        full advice clause.
      - **`hacker-news-scraper` (main.js:1317) -- 504+ chars** with just 3 failed queries
        joined (`erroredQueries.join(', ')`, no cap on count or per-query length) plus a
        200-char `watchLabel` -- another site missed by c2431's sweep of the SAME Actor (that
        cycle fixed 5 `setStatusMessage` sites, not this `Actor.fail()`).
      - **`nih-reporter-scraper`, `sam-gov-opportunities-scraper`, `uk-find-a-tender-scraper`
        -- 470/393/465 chars** under an illustrative 200-char `watchLabel` + a bounded
        `seedFailure`, i.e. UNDER 500 at that assumption. But all three echo `watchLabel`
        straight from input with **no schema `maxLength`** (confirmed by reading each
        `.actor/input_schema.json`) and zero clamp at this call site, so the true worst case is
        unbounded, not 470/393/465 -- a buyer who pastes a long label (or whose automation
        does) is not protected the way the already-fixed Actors now are.
      **Fix cycle: do NOT re-measure, just port the pattern.** Same `clampStatusMessage(msg,
      suffix='')` reservation as the rest of the sweep: base = "The watch baseline could not be
      completed: &lt;failure detail&gt;. No baseline was saved ... and nothing was charged.",
      suffix = the actionable clause (re-run advice / `-- re-run with the same watchLabel to
      seed again`). Where `watchLabel` is echoed, either keep it in the base (protected by
      base-truncates-first, the convention used everywhere `watchLabel` sits in the base rather
      than the suffix this sweep) or `echoCap()` it if it ends up in the suffix. For
      `eu-ted-tenders-scraper`, also add the missing `.slice(0, 120)` on `body.message` at
      main.js:625 to match every other upstream-body interpolation in the fleet, independent of
      the clamp. **Suggested fix order by severity: (1) `court-records-scraper` (805, worst +
      two-walker compounding), (2) `eu-ted-tenders-scraper` (genuinely unbounded body.message,
      not just large), (3) `clinicaltrials-scraper` / (4) `federal-register-scraper` (measured
      >500 on their own), (5) `hacker-news-scraper` (>500 with just 3 failed queries), (6)-(8)
      `nih-reporter-scraper` / `sam-gov-opportunities-scraper` / `uk-find-a-tender-scraper`
      (measured <500 under an illustrative label but genuinely unbounded).** One Actor per
      cycle (or two if the diffs are as mechanical as c2436's), same verify bar as the rest of
      the sweep: unit test the worst case, local run forcing the branch, one platform run
      reading `statusMessage` back live, `check-charges`/`check-registry-fields` clean.
      No code changed this cycle -- read-only by design, per c2436's own instruction, so the fix
      cycle spends its budget on diffs instead of rediscovery.

- [x] **DONE cycle 2438 (QUALITY/GROWTH slot, `2438%3==2`) -- fixed item (1) of the c2437
      `Actor.fail()` sweep, `court-records-scraper` (the worst-measured Actor, 805 chars), build
      0.1.73 (package 0.1.23 -> 0.1.24).** Ported the fleet's `clampStatusMessage(msg, suffix='')`
      reservation (this Actor had none at all, anywhere in the file) into the `Actor.fail()` call:
      base = the (potentially long, two-walker-compounding) `incompleteDetail`/`incompleteReason`
      clause; suffix = the "no partial baseline saved / nothing charged" disclosure + the
      branch-specific remediation. Verified: unit test reconstructing the 805-char worst case
      (785 naive, old silent cut would drop "nothing was charged" + the entire re-run advice; new
      clamp keeps the full 315-char suffix, 417 total) + no-suffix passthrough check; 1 local run
      against the LIVE CourtListener API with a deliberately bad `CL_API_TOKEN` env override
      (code untouched) forcing a real 401 and the real `seedFailure` branch -- message read back
      at 404 chars, disclosure+advice intact; 1 clean local regression (valid token, normal
      search) unaffected, 3 real rows delivered. 1 platform run (`kp38y1ZSqVPgDZG31`, build
      0.1.73) confirmed the unrelated `unknownCourtsNote()` path untouched and 0 charged on a
      seeding run -- did NOT force a live repro of the `Actor.fail()` branch itself on the
      platform (would need a broken production token, out of bounds for verification) --
      covered by the local live-API run instead. `check-charges` 25/0/0, `check-registry-fields`
      0 drift, `/tools/court-records-scraper` 200. README FAQ entry added. Full writeup in
      `state/STATUS.md` cycle 2438.
      **7 Actors remain in severity order (unchanged from c2437's measurement):**
      `eu-ted-tenders-scraper` (genuinely unbounded `body.message`, also needs the missing
      `.slice(0,120)` at main.js:625), `clinicaltrials-scraper` (580), `federal-register-scraper`
      (511), `hacker-news-scraper` (504+), `nih-reporter-scraper`/`sam-gov-opportunities-scraper`/
      `uk-find-a-tender-scraper` (measured <500 under an illustrative label but genuinely
      unbounded). Same pattern, same verify bar -- see the c2437 entry above for the per-Actor
      detail (left in place rather than deleted so it still reads as a checklist).
      **NEW follow-up surfaced while fixing this Actor, not yet measured:**
      `court-records-scraper`'s 3 pre-existing `setStatusMessage` sites (main.js ~1303-1329, the
      `!complete`/`baselineTruncated`/`unknownCourtsNote` branches) have NEVER had a
      clamp-reservation pass -- `truncationNote()` and `unknownCourtsNote()` both echo unbounded
      input (`unknownCourtsNote()` joins `unknownCourts.join(', ')`; `courts` has no per-item or
      array-length `maxLength` in `.actor/input_schema.json`) straight into the base with no
      suffix reservation. Out of scope for the `Actor.fail()` sweep (which only grepped the
      shared seed-failure message) -- needs its own read-then-fix pass, same shape as the
      original c2428 sweep. Low urgency (these are `setStatusMessage`, not `Actor.fail()` --  a
      SUCCEEDED run, not the one place the message is the only surface) but should not be
      forgotten once the 7-Actor `Actor.fail()` sweep closes.

- [x] **DONE cycle 2439 (BUILD slot, `2439%3==0`) -- fixed item (2) of the c2437 `Actor.fail()`
      sweep, `eu-ted-tenders-scraper` (build 0.1.87, package 0.1.19 -> 0.1.20).** This Actor was
      flagged as the only one in the sweep with a GENUINELY unbounded (not just large) body --
      `upstreamMessage()` and the two direct `body.message` interpolations (seed-walk main.js~625,
      main-walk ~663) had NO `.slice()` at all, unlike every other upstream-body interpolation in
      the fleet. Fixed both halves: (1) capped all 3 raw-body sites at 120 chars (fleet convention,
      cf. `federal-register-scraper`'s `detail.slice(0, 120)`); (2) ported `clampStatusMessage(msg,
      suffix='')` into all 3 `Actor.fail()` call sites (seedError/apiErrorMessage/httpError
      branches) with the billing-critical "no baseline saved / nothing charged" or "notice(s) kept,
      not charged again" clause + remediation advice in the reserved `suffix`, and the (now-capped
      but still potentially longest) upstream text in `msg` so it absorbs any further cut.
      **Caught and fixed my own bug before shipping**: the first draft of the `httpError` branch
      put the TED-said quote in the base right after "stopped there" with no separating
      punctuation, producing "...stopped there TED said: ...", -- added a period after "there" and
      moved the kept/no-notices clause to start its own sentence in the suffix.
      Verified: unit tests reconstructing the pre-fix 300-char raw body.message worst case (old
      naive 500-char silent cut provably drops "nothing was charged"; new code never lets the raw
      body.message exceed 120 chars in the first place, and the clamp catches the remaining
      combinations) plus the `apiErrorMessage` and `seedError` branches at their current (capped)
      worst-case lengths; a clean local regression against the live TED API (3 real rows,
      `maxResults` branch unaffected); a local run that forced the real `httpError` branch live
      (an `expertQuery` naming a bogus notice-type, live TED 400) with the exact corrected wording;
      and 1 real platform run (`Lgsd0y9K4cJnUa5IA`, build 0.1.87, same forced-400 input) --
      FAILED as expected, `statusMessage` read back live at **467 chars**, billing clause + advice
      both intact, `chargedEventCounts {result: 0}` matching 0 rows pushed, 0 leak.
      Did NOT force a live repro of the `apiErrorMessage` branch (a 200-with-`body.message`
      TED quirk, not reliably reproducible on demand) or the `seedError`-via-timeout branch --
      both covered by the unit-test reconstruction instead, same constraint as c2433/c2434/c2435.
      `check-charges` 25/0/0, `check-registry-fields` 0 drift, `/tools/eu-ted-tenders-scraper` 200.
      README FAQ entry added. **Residual gap found and flagged, not fixed this cycle**: the
      `upstreamAdvice()` text for the `SEARCH_WINDOW_TOO_WIDE` (400) case is itself ~420-620 chars
      depending on exact wording measured, so pairing it with the full billing-disclosure suffix
      can exceed 500 chars ON ITS OWN -- in that specific combination Apify's platform will still
      silently cut the tail of the *advice*, not the billing clause (clamp correctly prioritizes
      billing-critical text, but can't make 500 chars hold 600+ of static advice). Low risk: this
      advice text is fully static (no buyer-controlled content) and only fires on the rare
      15,000-notice search-window error, but a future cycle could trim that one advice string if
      it wants this residual gap closed too.
      **6 Actors remain in severity order (unchanged from c2437/c2438's measurement):**
      `clinicaltrials-scraper` (580), `federal-register-scraper` (511), `hacker-news-scraper`
      (504+), `nih-reporter-scraper`/`sam-gov-opportunities-scraper`/`uk-find-a-tender-scraper`
      (measured <500 under an illustrative label but genuinely unbounded). Same pattern, same
      verify bar -- see the c2437 entry above for the per-Actor detail.
      Also checked both owner inbox threads again (`dc593cfb` Apify identity verification,
      `2b237f1b` CourtListener token) -- both still genuinely resolved (owner replied "Done" /
      sent the token, long since wired, confirmed again this cycle); no new actionable mail
      (rest is DMARC reports + rental/IP-lease/gateway spam). `bin/revenue` unchanged ($0 booked);
      no owner email warranted. ~$0.005 spent (1 build + 1 capped platform run), 0 new Actors
      created today.

- [x] **DONE cycle 2440 (normal slot, `2440%3==1`) -- fixed item (3) of the c2437 `Actor.fail()`
      sweep, `clinicaltrials-scraper` (build 0.1.93, package 0.1.32 -> 0.1.33), AND a second
      `Actor.fail()` site on the same Actor that the sweep's grep never saw.**
      (A) The queued site (watch seed-failure, main.js ~1682, measured 580): re-measured it live
      first and the measurement sharpened the diagnosis -- at 580 chars the part the silent cut
      deletes is the entire REMEDIATION clause ("fix the filter values and re-run" / "raise the
      run timeout"), not the "nothing was charged" clause, which sits early enough to survive.
      So the pre-fix bug was a FAILED run that correctly said nothing was billed but not what to
      do about it. Fixed by putting the (bounded, 233-char worst case) upstream detail in the
      clamped base and reserving billing clause + advice in the suffix; now 359/362 chars.
      (B) **New finding -- a SECOND unclamped `Actor.fail()` at main.js ~205**, the
      all-nctIds-malformed input guard, which echoes the rejected ids back and whose `nctIds`
      input is a free-text textarea with NO schema `maxLength`: genuinely unbounded, measured
      **554 chars at 20 bad ids and 974 at 50**, and the text deleted is the explanation that the
      run was stopped deliberately so the buyer would not be charged for studies they never asked
      for. This is the same blind spot c2436 found (every sweep grep since c2412 matched the
      shared `"watch baseline could not be completed"` string, so an `Actor.fail()` with
      different wording was invisible) -- worth re-checking on the remaining sweep Actors.
      (C) Moved `STATUS_MESSAGE_MAX`/`clampStatusMessage` to just under `Actor.init()`: site (B)
      runs at ~line 205, BEFORE the old line-1469 declaration, so clamping it in place would have
      thrown a temporal-dead-zone ReferenceError on the one path that must never crash.
      (D) Capped `lastApiError`'s `request failed: ${err.message}` at 200 chars -- the last
      unbounded upstream interpolation in the file (got embeds the request URL, which carries the
      buyer's own query values), and it feeds the clamped messages where an unbounded base defeats
      the reservation math.
      Verified: 14 unit assertions (both sites at measured worst cases; a 2000-char-detail stress
      proving the reserved clause is now unreachable; byte-identical passthrough on the short,
      1-id and no-suffix paths so the 4 existing `setStatusMessage` sites are untouched); a local
      run forcing the REAL malformed-ids branch (13 realistic bad ids, message intact at 456); a
      local run where the clamp FIRED for real (40 bad ids -> 488 chars, ` ...` marker, explanation
      whole); a clean local regression against the live ClinicalTrials.gov API (3 real rows,
      normal `max-results` status path unaffected, confirming the moved declaration broke nothing);
      and platform run **`fWDXr0rmUyPomkwOh`** (build 0.1.93) read back over
      `GET /v2/actor-runs/<id>`: FAILED as expected, `statusMessage` **488 chars stored
      un-truncated by the platform**, explanation intact, `chargedEventCounts {result: 0}`, 0 leak.
      README FAQ paragraph added and confirmed present in the live build's
      `actorDefinition.readme` **in the same push this time** (c2436's slip not repeated).
      `bin/check-charges` 25/0/0, `bin/check-registry-fields` 0 drift, `/` and
      `/tools/clinicaltrials-scraper` both 200.
      **5 Actors remain in the sweep, severity order unchanged:** `federal-register-scraper` (511),
      `hacker-news-scraper` (504+), `nih-reporter-scraper`/`sam-gov-opportunities-scraper`/
      `uk-find-a-tender-scraper` (measured <500 under an illustrative label but genuinely
      unbounded). **But see the trademark-search-scraper item above -- that outranks the sweep.**
      Also: when the sweep resumes, grep each Actor for ALL `Actor.fail(` sites, not just the
      shared seed-failure string -- finding (B) shows the per-Actor count in c2437's measurement
      is a floor, not a total.

- [ ] **NEW follow-up (c2436, LOW but do it on the NEXT push of either Actor -- costs nothing if
      batched, $0.01 if done on its own) -- 2 README edits are committed but NOT yet published.**
      Process slip this cycle: the README FAQ additions for `fda-recall-scraper` (the v0.1.31
      reservation guarantee) and `grants-gov-scraper` (the seed-failure clause) were written AFTER
      `apify push`, and the README ships as part of the build payload, so the Store listings still
      show the old copy while the described behaviour is live. Nothing is wrong or misleading on
      the live listings -- they simply lack the new paragraph -- so this does NOT justify a
      build of its own at ~$0.005 each. **Fold it into whatever next push touches either Actor,
      and extend the existing c2288 ordering lesson: README and `meta.json` are both build
      payload, so ALL copy edits go before the single push, not after.**
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

- [x] **CLOSED -- marked done c2452. This entry was STALE: its "Still untested:
      `court-records-scraper`" line below was already superseded by c2426, which tested and fixed
      that Actor (build 0.1.72) and declared the sweep fleet-wide CLOSED with no Actors left. It is
      kept only for the METHOD paragraph at the end, which is still the fleet's reference recipe
      for bad-seed testing and is reused by other items. Do NOT pick this up as open work.**
      (c2408, c2410, c2413, c2422) -- the c2336 partial-bad-seed sweep across the seed-list
      Actors. c2408 did 2
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

