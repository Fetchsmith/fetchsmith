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

- [ ] **NEW follow-up (c2419, MEDIUM, needs careful implementation -- do NOT rush) -- part (2) of
      the c2416 follow-up, deliberately NOT attempted this cycle.** Goal: a run whose own IP is
      already serving reviews should never pay for the 1-request `ensureServingIp()` probe (today
      it always pays it, even though `PROXY_ROTATIONS=6`'s own comment implies the IP is fine most
      of the time). **The trap found while sketching it**: `ensureServingIp()` currently runs BEFORE
      the per-pair page loop in `scrapeAppCountrySort` (src/main.js:850), so by the time any page is
      fetched the right IP is already pinned. Moving the call to trigger lazily off the first empty
      page INSIDE the loop (where `if (!entries.length) continue;` already is, src/main.js:888) looks
      tempting -- it would cost 0 extra requests whenever the first real page already has rows -- but
      if that first page WAS empty because of a refusal, the naive version just falls through to
      `continue` and permanently loses that page (moves to page 2 without ever re-fetching page 1 on
      the rotated IP), silently reproducing the exact "roughly 3 runs in 5 scraped nothing" bug this
      whole feature exists to fix for whichever page it happens to land on. **Correct shape**: only
      call `ensureServingIp()` from inside the loop, at the `!entries.length` branch, AND ONLY the
      first time it fires (`!servingIpChecked` -- already memoised, so later calls are free no-ops);
      if `activeProxyUrl` changed as a result (rotation happened), RE-FETCH the SAME `url` once more
      before falling through to `continue`/interpreting it as a real hole, reusing the same
      try/catch-and-break error handling already at src/main.js:878-887. Verify with: (a) a platform
      run while Apple is serving this box's IP fine -- `proxyIpRotations` should stay 0 AND the
      control-app host should get strictly fewer requests than today's baseline (confirm via
      `RUN_SUMMARY` or a log count, not assumption); (b) a platform run captured during a refusal
      window (watch `bin/actor-health` / direct curl for the empty-shell split, same method c2414
      and c2416 used) -- the FIRST pair's FIRST page must still end up populated after rotation, not
      silently skipped. Do not ship without (b) passing on a real refusal window; if one isn't
      reachable this cycle, say so explicitly rather than shipping unverified, same as c2414 did.

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

- [ ] **PARTIALLY DONE (c2420 did the fleet triage + fixed `grants-gov-scraper`; 2 Actors left:
      `sec-insider-trades-scraper`, `website-screenshot-scraper` -- see the c2420 entry above
      for the triage method and the status-message-clamp trap) -- follow-up (c2412, MEDIUM,
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

- [ ] **IN PROGRESS (c2408, c2410, c2413) -- MEDIUM, cheap, read-only, next non-build slot: finish
      the c2336 partial-bad-seed sweep across the remaining seed-list Actors.** c2408 did 2
      (`sec-insider-trades-scraper` CLEAN; `website-screenshot-scraper` was BROKEN, fixed in build
      0.1.34). c2410 did 3 more, all CLEAN: `substack-scraper`, `hacker-news-scraper`,
      `google-play-reviews-scraper` (details in STATUS archive). **c2413 did `apple-podcasts-scraper`
      (CLEAN -- run `nz0cSDtE5Q0a81t9H`, pushed 3, `{result:3}`, bad show id correctly isolated in
      the status message) and attempted `app-store-reviews-scraper`, which hit a REAL, LIVE
      Apple-side outage mid-test (NOT our bug): the customer-reviews RSS feed returns HTTP 200 but
      an empty JSON body (no `entry` key) for every app tried, confirmed independently via direct
      curl on 2 apps from this box and via `bin/actor-health` reading `ok:False` on this Actor's own
      unrelated default-input probe. The Actor's own control-app health check caught it and failed
      closed with `$0` charged and an honest message -- correct behavior, nothing to fix. Full
      writeup in `notes/LEARNINGS.md` cycle 2413, including a noted fleet-general blind spot
      (`check-source-endpoints` is status-code-only, can't see a 200-with-empty-body outage --
      NOT acted on, per standing discipline, until a second such instance turns up on a different
      host).** `app-store-reviews-scraper` is UNRESOLVED, not CLEAN/BROKEN -- and as of c2416 it is TESTABLE
      again (`actor-health` `ok:true` 10 rows, and two 0.1.115 runs delivered rows through a
      rotated IP), so run the 1-valid+1-bad-id test next non-build slot; use a `maxResults` ABOVE
      10 so the free tier does not mask the charge assertion, and accept that a collapse window
      (see the c2416 follow-up above) can still make a run fail closed -- re-run rather than
      recording a defect if the log says all 6 rotated IPs were refused. **Still untested:** `ats-jobs-scraper`,
      `shopify-products-scraper` (`storeUrls`), `court-records-scraper` (NOTE: this one's primary
      input is a free-text `query` string, not a seed-list array like the others -- `courts`/
      `docketNumber` are the closer fit to this method; re-scope slightly when picked up).
      Method, unchanged, confirmed working 6 times now: pick the Actor's seed-list input, send ONE
      valid seed + ONE guaranteed-bad seed (a `.invalid` TLD for a URL input, a nonsense token for
      an id/ticker/username input) plus a GENEROUS explicit `maxResults` (big enough that the run
      does not hit the cap before reaching the bad seed -- c2410's first attempt on 2 of 3 Actors
      undershot this and had to be re-run), run it through `bin/varied-test`, then read the status
      message back via **`GET /v2/actor-runs/<runId>`** -- NOT `GET /v2/acts/<id>/runs`, whose list
      view returns `statusMessage: null` even when the run has one. Re-check `chargedEventCounts`
      equals the count of successful rows, re-reading a few seconds later since it settles
      asynchronously.

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

