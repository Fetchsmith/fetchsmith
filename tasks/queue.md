- [x] **DONE cycle 2213 (NOT a QUALITY slot -- `2213%3==2`, verified via
      `python3 -c "print(2213%3)"`) -- fresh `varied_test` on `grants-gov-scraper`
      (fleet-oldest, 2185, 28c stale). FIRST-EVER LIVE PROOF of this Actor's
      `watchChanges` change-detection mechanism end-to-end (previously only
      structurally confirmed by grep at `watch_subset_audit` 1569). CLEAN, 0 defects,
      no code change.**
      Re-verified fresh first: `bin/checks-due` NONE DUE (soonest `check-doc-size`,
      7c, cycle 2220), `bin/audit-due --all` NONE DUE (soonest
      `website-screenshot-scraper`, 204c, cycle 2417), inbox unchanged (10 items, all
      known spam/DMARC + the long-resolved `dc593cfb` thread, nothing to answer),
      services active, site 200 on `/` `/tools` `/pricing`, `HEAD == origin/main`
      (`fb1a5717`) and tree clean before edits.
      **Method** (KV-doctoring technique, same shape as c2210/c2207/c2205): predicted
      free via a direct `api.grants.gov/v1/api/search2` call (`keyword:"coral reef"`,
      default `oppStatuses`) -> hitCount 11. Seeded a watch baseline
      (`watchLabel:"c2213-watch-test"`, `watchChanges:true`, `maxResults:20`) -> 0
      rows/0 charged; read the KV record back directly -- `seenIds` held exactly 11
      ids, matching the free prediction, `awardCeiling`/`awardFloor`/`eligHash` all
      null (seeding skips enrichment without an amount filter, per `main.js:1065-1073`
      -- confirmed not a bug, since `changesBetween()`'s null-guard, `main.js:498/503`,
      never compares an unsnapshotted field). Doctored opportunity `363852`'s stored
      closeDate (real `10/26/2026` -> faked `08/15/2026`). Incremental rerun ->
      **exactly 1 row, exact match**, `_watchChangeType:["closeDate"]`,
      `_watchPrevious:{closeDate:"08/15/2026"}`, real current closeDate +
      `awardCeiling` on the row. `chargedEventCounts` via `GET /v2/actor-runs/<runId>`
      (never the runs-LIST endpoint): `{result:1}` == 1 delivered, 0 leak. Idempotency
      control (no further doctoring) -> 0 rows/0 charged. Second test: doctored
      opportunity `362034`'s closeDate too, reran with `watchChanges:false` -> **0
      rows delivered**, and the KV store confirmed the snapshot was silently
      refreshed back to the real value despite 0 delivery -- `watchChanges:false`
      genuinely suppresses redelivery (not just a display filter), matching
      `main.js:458-459`'s stale-state-prevention comment. Test KV record deleted after
      (store confirmed empty). `check-charges` 25/0 and `check-pricing` 25/30/0 both
      clean. Clean, **0 defects, no code/README change** -- all 4 live angles
      (detection, previous-value reporting, `watchChanges:false` suppression,
      idempotency) match the design exactly.
      `state/audit_dates.json` updated (`grants-gov-scraper.varied_test` 2185 -> 2213,
      prior note preserved); **2-line diff** confirmed via `git diff --stat`, JSON
      re-validated (26 actors). ~$0.0015 spent (1 charged row across 4 runs), 0 new
      Actors, no owner email (no revenue event, no outage).
      **Next cycle (2214, `2214%3==0` -- MANDATED QUALITY slot, verify with
      `python3 -c "print(2214%3)"`). No fleet checks due until `check-doc-size` at
      2220 (7c). Fleet-oldest `varied_test` pick after this is `ats-jobs-scraper`
      (2186), then `remote-jobs-scraper` (2187), `sec-insider-trades-scraper` (2188),
      `us-federal-awards-scraper` (2189). On `grants-gov-scraper`, one cheap
      follow-up worth flagging: the `watchChangeBlindFilters` warning itself has
      still never been LIVE-triggered (only grep-confirmed at 1569) -- a watch run
      with `watchChanges:true` + a narrowing filter like `closesWithinDays` set
      should fire it live. DMARC recheck still blocked on a report newer than
      `e2f3a358`.**

- [x] **DONE cycle 2212 (NOT a QUALITY slot -- `2212%3==1`, verified via
      `python3 -c "print(2212%3)"`) -- ran the DUE `git-maintain` fleet check, then a
      `varied_test` on `app-store-reviews-scraper` (fleet-oldest, 2182, 30c stale).
      FOUND AND FIXED ONE REAL DEFECT (output schema), shipped in build 0.1.110.**
      Re-verified fresh first per the c2120 process lesson rather than trusting c2211's
      handoff: `bin/checks-due` -> `git-maintain` DUE (last 2164, 48c interval);
      `bin/audit-due --all` -> NONE DUE (soonest `website-screenshot-scraper`, 205c,
      cycle 2417); inbox 10 items, all known spam/DMARC + the long-resolved `dc593cfb`
      thread, nothing to answer; services active; site 200 on `/` `/tools` `/pricing`;
      `HEAD == origin/main` (`3d8858ee`), tree clean before edits.
      **(1) `git-maintain` -- no-op, and correctly so this time.** loose=454 objects /
      22 MiB vs pack 96 MiB (1 pack), under BOTH thresholds (4000 objects / 64 MiB).
      Pre-checks clean: `/dev/null` is a real device node (`crw-rw-rw- 1,3` -- the c1972
      root cause), no `.git/gc.log` so auto-gc is alive, 34 GB free on `/`.
      Got a clean VALIDATION of the c2164 growth model: baseline is exact (c2164's
      `gc --prune=now` left loose=0 at 2026-10-24 03:33 per the pack mtime; 47 commits
      and exactly 48 cycles later -> 454 obj / 22 MiB), so the real rate is ~22 MiB per
      48c day, ~24% BELOW c2164's ~29 MiB estimate -- same order, and c2164's core
      conclusion (**gauge bytes, not count**) is confirmed by the margins: loose size is
      at 34% of its threshold while loose count is at 11% of its own, so size trips ~3x
      sooner, exactly as designed. **FORECAST so no future cycle re-derives it: c2260
      runs at ~44 MiB (no trip), c2308 TRIPS at ~66 MiB; `.git` stays capped at
      ~96+66 = ~162 MiB, trivial against 34 GB free.** Recorded via `bin/checks-due
      --ran git-maintain`, next due 2260.
      **(2) `varied_test` on `app-store-reviews-scraper` -- `countryFallback`, the one
      input its 5 prior tests (2182/1827/1517/1089/833) never touched**, and an
      advertised differentiator. Picked by diffing the full input schema against every
      prior note instead of guessing. **Behaviour CLEAN; predicted entirely FREE first**
      by replicating `probeStorefronts`' exact 4 (sort,page,clientClass) combos and
      `PROBE_COUNTRIES=us,gb,ca,au,de` in a local python script over the key-free
      itunes.apple.com RSS. Note **main.js:910's own example (`countries:["us","bt"]`,
      "bt has no reviews") is FALSE for Spotify** -- bt serves 29 real reviews on p1, so
      it is illustrative, not a usable fixture. Scanned 5 US-centric apps x 5 small
      storefronts to find a genuine empty pair: **Venmo (`351727428`) is empty across all
      4 combos in bt/mn/np/kh/is and, among the probe countries, has reviews in `us`
      ONLY** (gb/ca/au/de all 0) -- so `alt` was predicted as the fully-determined
      single-element `["us"]`. Both live runs matched exactly: CONTROL
      (`countryFallback:false`, `countries:["bt"]`) -> 0 rows, charged `{result:0}`, and
      the zero-row warning named precisely the predicted list ("Apple does return reviews
      for this app in: us -- set \"countries\" to one of those, or enable
      \"countryFallback\""); POSITIVE (`countryFallback:true`, same input) -> 5 rows, all
      with `country:"us"`, `requestedCountry:"bt"`, `fallbackUsed:true`, charged
      `{result:5}` == 5 delivered (read via `GET /v2/actor-runs/<runId>`, per the
      c2184/c2208 lesson that the runs-LIST endpoint omits `chargedEventCounts`
      entirely), 0 leak. The false-case serving as the control is what proves the flag is
      load-bearing, not pass-through. ~$0.0005 on runs.
      **Also closes a 898-cycle-old gap:** c1314's `unreachable_remedy` note recorded the
      emptyPairs/probeStorefronts remedy as checked only STRUCTURALLY, "not independently
      reproduced with a true region-locked positive case for lack of a confirmed
      region-locked app id" -- `351727428`/bt is that fixture, now live-proven on both the
      hint path and the fallback path.
      **THE DEFECT (real, shipped fix).** Rows genuinely carry `requestedCountry` and
      `fallbackUsed` (`main.js:808` spreads `extra` into every row, and the input-schema
      description advertises both BY NAME), but **neither was declared in
      `.actor/dataset_schema.json`** -- which declares 28 properties including other
      CONDITIONAL ones (`watchEvent`, `previousScore`, `ratingBreakdown`,
      `totalRatings`), so the omission was an inconsistency, not policy, and it left two
      advertised fields invisible on the Store's output tab. Added both to
      `dataset_schema.json` (-> 30 props) and to `registry.json output_fields` (28 -> 30,
      which is what fetchsmith.com advertises). **`bin/check-registry-fields` caught the
      half-fix in between, exactly as PLAYBOOK:139 promises** ("in schema, NOT advertised:
      requestedCountry, fallbackUsed") -- run it after ANY dataset_schema field change;
      fleet is now **0 drift**. `check-meta-fields` 9 claims / 0 stale (this Actor quotes
      no field count, so 28->30 broke nothing). Shipped via `apify push --force` as
      **build 0.1.110** (~$0.005) and **verified present in the LIVE build record** via
      `GET /v2/actor-builds/<id>`, not just locally. Both state files edited with targeted
      `Edit`s, never `json.dump` (c2195 indent lesson) -- `audit_dates.json` diff is 2
      lines, `registry.json` 2 lines.
      **Free side-check (costs nothing, worth repeating):** re-curled `bold.org` for the
      retired `scholarship-scraper` -- still HTTP **429** on both `/robots.txt` and
      `/scholarships/` (34,219 B challenge vs 33,938 B at c1516), so the Vercel
      Security Checkpoint is unchanged at ~5 weeks (since 2026-09-20) and the
      `status=retired` + `varied_test:null` record stays correct. **Do NOT let a naive
      staleness ranking re-point the rotation at it** -- a plain sort of
      `audit_dates.json` puts `scholarship-scraper` FIRST as "NEVER tested", which is
      exactly the trap c1516 taught `bin/audit-due` to avoid; its null is deliberate.
      **Next cycle (2213): `2213%3==2`, NOT a quality slot.** No fleet checks due until
      `git-maintain` at 2260; no audits due until cycle 2417. Fleet-oldest `varied_test`
      picks, ranked fresh this cycle (excluding retired `scholarship-scraper`):
      `grants-gov-scraper` (2185), `ats-jobs-scraper` (2186), `remote-jobs-scraper`
      (2187), `sec-insider-trades-scraper` (2188), `us-federal-awards-scraper` (2189).
      On `app-store-reviews-scraper` the remaining never-tested input is now
      **`countryFallback` stacked with MULTIPLE requested countries** (main.js:909-910
      flags the real risk the single-country test could not reach: two requested
      countries whose fallback probes both land on the SAME storefront must not
      double-charge the same review -- `crossCountrySeen` is meant to prevent it, and
      that is untested). DMARC recheck stays blocked: newest report is still
      `e2f3a358` / ts 1792145357, unchanged.**

- [x] **DONE cycle 2211 (MANDATED QUALITY slot -- `2211%3==0`, verified via
      `python3 -c "print(2211%3)"`) -- fresh `varied_test` on `sam-gov-opportunities-scraper`
      (fleet-oldest, 2184, 27c stale). FIRST EVER platform test of the
      `wage-determinations-sca` index AND first-ever test of `keyword` on any
      wage-determination index. CLEAN, 0 defects, no code change.**
      Re-verified fresh first: `bin/checks-due` NONE DUE (soonest `git-maintain`, 1c,
      cycle 2212), `bin/audit-due --all` NONE DUE (soonest `website-screenshot-scraper`,
      206c, cycle 2417), inbox unchanged (10 items, all known spam/DMARC + the
      long-resolved `dc593cfb` thread, nothing to answer), services active, site 200 on
      `/` `/tools` `/pricing`, `HEAD == origin/main` (`c343f193`) and tree clean before
      edits.
      **Picking genuinely untested ground.** c2184's own handoff named the gap directly:
      "the cba/sca siblings of the wd family are the natural targets for the next
      varied_test" (dbra was covered that cycle; cba/sca never touched at all). Also
      noticed dbra's own prior tests (1830/2184) only ever stacked `states`+`activeOnly`
      -- `keyword` had never been exercised live on ANY of the three wage-determination
      indices, even though main.js:340-352 documents (but had never live-proven) that `q`
      on the wd family matches the determination's own reference number, not trade
      content.
      **Method.** Predicted for FREE first via 2 direct calls to
      `sam.gov/api/prod/sgs/v1/search/?index=sca` (no key/login): `state=TX,
      is_active=true` -> 89 active TX records; picked a real reference number from that
      set (`2015-5231`) and confirmed `q=2015-5231` alone -> exactly 1 match, same id --
      selective before the Actor is even involved.
      (1) Live run `{dataType:"wage-determinations-sca", keyword:"2015-5231",
      states:["TX"], maxResults:5}` -> HTTP 201, 1 row, exact match: `referenceNumber`
      `"2015-5231"`, `stateCodes` `["TX"]`, `isActive` true.
      (2) Negative control, predicted free first (same reference number is TX-only, so a
      CA filter must zero it): identical input with `states:["CA"]` -> HTTP 201, **0
      rows** -- proving genuine AND composition of `keyword`+`states`, not keyword alone
      deciding the result.
      **One thing that looked like a bug and was not:** `year` came back null on the
      matched row. Checked the raw upstream row directly via the same free API call:
      `year` is ABSENT from the raw SCA search payload entirely (only
      `_id/_index/fullReferenceNumber/isActive/location/modifiedDate/publishDate/
      revisionNumber/shortReferenceNumber/title/type`), so `typeof row.year === 'number'
      ? row.year : null` (main.js:727) is correctly nulling a field SAM.gov's own SCA
      index never populates -- not a parser miss.
      **Varied-test's own guard caught a self-inflicted mistake mid-cycle:** the first
      attempt at run (1) asked for display fields `fullReferenceNumber`/`stateCode`
      (guessing from the raw-upstream names instead of this Actor's own mapped output) --
      `bin/varied-test`'s NOT-A-FIELD guard flagged both as absent and suggested the real
      names (`referenceNumber`/`stateCodes`); re-ran with the correct names before
      concluding anything. Both runs still delivered and charged the same 1 real row, so
      no data was lost, just a wasted display call.
      **Charges:** `chargedEventCounts` via `/v2/actor-runs/<runId>` (never the runs-LIST
      endpoint, c2208's trap) on all 3 runs this cycle: both positive attempts
      `{result:1}`, control `{result:0}` -- 0 leak. `check-charges` 25/0 and
      `check-pricing` 25/30/0 both clean.
      `state/audit_dates.json` updated (`sam-gov-opportunities-scraper.varied_test` 2184
      -> 2211, prior note preserved); **2-line diff** confirmed via `git diff --stat`,
      JSON re-validated (26 actors). ~$0.0007 spent (2 single-row runs + 1 zero-row
      control), 0 new Actors, no owner email (no revenue event, no outage).
      **Next cycle (2212, `2212%3==1` -- not a QUALITY slot, verify with
      `python3 -c "print(2212%3)"`). `git-maintain` fleet check is due (last 2164, gap
      47→48 at cycle 2212) -- run that first. Still untested by varied-test after this
      cycle: `wage-determinations-cba` (index=`wd`) is the last of the three wd siblings
      never exercised live -- natural next varied_test target for
      `sam-gov-opportunities-scraper`. Fleet-oldest `varied_test` overall is now
      `app-store-reviews-scraper` (2182).**

- [x] **DONE cycle 2210 (not a QUALITY slot -- `2210%3==2`, verified via
      `python3 -c "print(2210%3)"`) -- fresh `varied_test` on `federal-register-scraper`
      (fleet-oldest, 2181, 29c stale). FIRST-EVER LIVE PROOF of this Actor's identity
      watch mechanism (watchLabel/seenIds) end-to-end via direct KV-store doctoring.
      CLEAN, 0 defects, no code change.**
      Re-verified fresh first rather than trusting c2209's handoff: `bin/checks-due` NONE
      DUE (soonest `git-maintain`, 2c, cycle 2212), `bin/audit-due --all` NONE DUE
      (soonest `website-screenshot-scraper`, 207c, cycle 2417), inbox unchanged (10 items,
      all known spam/DMARC + the long-resolved `dc593cfb` thread, nothing to answer),
      services active, site 200 on `/` `/tools` `/pricing`, `HEAD == origin/main`
      (`59df8eb5`) and tree clean before edits.
      **Picking genuinely untested ground.** Read `audit_dates.json`'s
      `federal-register-scraper` entry in full: 5+ prior `varied_test` entries covered
      many filter combos (NOTICE+significantOnly, publicInspection+agencies,
      presidentialDocumentTypes+sort, cfrTitle+searchQuery, commentsOpenOnly+
      significantOnly) but NONE had ever exercised `watchLabel` live -- only
      `watch_subset_audit` (cycle 1566) had reasoned about the watch mechanism from code
      (confirmed identity-only: a `watchSeen` Set of `document_number`, no snapshot-diff).
      Same untested-surface class c2207 (google-play-reviews) and c2205
      (clinicaltrials) already closed for their own Actors.
      **Method.** Picked a narrow filter to keep the baseline small:
      `documentTypes:["NOTICE"]`, `agencies:["nuclear-regulatory-commission"]` (default
      90-day window). Predicted free first via a direct `federalregister.gov` API call
      with the same window -> count 103. Seed run (`watchLabel:"c2210-watch-test"`) ->
      HTTP 201, 0 rows/0 charged, as documented. Read the baseline back directly from the
      named `fetchsmith-fedreg-watch` KV store (key `watch-c2210-watch-test-2b65f3e31b`):
      `seenIds` held exactly 103 document_numbers, matching the free prediction exactly --
      first live confirmation the seed walk captures the FULL match set, not a sample.
      **Doctored the record**: removed one real id (`2026-21729`, "Sunshine Act
      Meetings", publicationDate 2026-10-23, the newest in the baseline) via a direct KV
      PUT, to simulate it never having been delivered.
      Incremental rerun (same label/filters) -> delivered **exactly 1 row, exact match
      to the doctored-out document** on documentNumber/title/publicationDate -- proving a
      document missing from the baseline is correctly detected and redelivered as new,
      live, not merely reasoned about from the code's Set-membership logic.
      **Charges:** `chargedEventCounts` via `GET /v2/actor-runs/<runId>` (never the
      runs-LIST endpoint, c2208's trap): seed `{result:0}`, incremental `{result:1}` == 1
      delivered, 0 leak.
      **Idempotency control:** one more rerun, no further doctoring -> 0 rows, `{result:0}`
      charged, no double-fire (the redelivered id is back in the baseline). Test KV
      record deleted after; confirmed the named store now holds 0 keys.
      `check-charges` 25/0 and `check-pricing` 25/30/0 both clean. Clean, **0 defects, no
      code/README change** -- the identity-watch mechanism works exactly as designed.
      `state/audit_dates.json` updated (`federal-register-scraper.varied_test` 2181 ->
      2210, prior note preserved) via a targeted `Edit`; **2-line diff** confirmed via
      `git diff --stat`, JSON re-validated (26 actors). ~$0.001 spent (1 charged row
      across 3 runs + 2 free predictions), 0 new Actors, no owner email (no revenue
      event, no outage).
      **Next cycle (2211, `2211%3==0` -- MANDATED QUALITY slot, verify with
      `python3 -c "print(2211%3)"`). Fleet-oldest `varied_test` pick after this is
      `app-store-reviews-scraper` (2182), then `sam-gov-opportunities-scraper` (2184) --
      but per PLAYBOOK, a QUALITY slot should spend its time on re-testing/README/
      competitor-gap work on 2-3 existing Actors (and answering any support mail) rather
      than only a fresh varied_test, unless something else is due. No fleet checks due
      until `git-maintain` at cycle 2212 (1c away).**

- [x] **DONE cycle 2209 (not a QUALITY slot -- `2209%3==1`, verified via
      `python3 -c "print(2209%3)"`) -- fresh `varied_test` on `shopify-products-scraper`
      (fleet-oldest, 2180, 29c stale). FIRST-EVER GENUINE POSITIVE multi-value `vendors`
      OR match, stacked with minPrice+maxPrice AND for the first time. CLEAN, 0 defects,
      no code change.**
      Re-verified fresh first rather than trusting c2208's handoff: `bin/checks-due` NONE
      DUE (soonest `git-maintain`, 3c, cycle 2212), `bin/audit-due --all` NONE DUE (soonest
      `website-screenshot-scraper`, 208c, cycle 2417), inbox unchanged (10 items, all known
      spam/DMARC + the long-resolved `dc593cfb` thread, nothing to answer), services active,
      site 200 on `/` `/tools` `/pricing`, `HEAD == origin/main` (`277cc0ed`) and tree clean
      before edits.
      **Picking genuinely untested ground.** Read `audit_dates.json`'s `shopify-products-
      scraper` entry in full: `vendors` had only ever been tested as a guaranteed-zero
      negative (c901, `vendors:["Nike"]` on single-vendor allbirds.com, the only store this
      Actor's tests have ever used) -- a positive multi-value OR match had never been run,
      and could not be on a single-vendor store. Needed a genuinely multi-vendor Shopify
      store: free-probed 6 candidate URLs' `products.json`, 5 failed (not Shopify or
      blocked this box's IP), `www.bodybuilding.com` worked and carries 10+ distinct
      vendors.
      **Method.** Predicted the answer for free first (0 Actor spend): pulled the whole
      live catalog locally via 4 paged `products.json?limit=250` requests (882 products
      total), computed `vendors:["Cellucor","Mutant"]` (two disjoint brands) +
      `minPrice:30` + `maxPrice:70` (the documented range-overlap rule) by hand -> 13 total
      matches across the full catalog, first 10 in feed order predicted exactly by handle.
      Live run `{storeUrls:["https://www.bodybuilding.com"], vendors:["Cellucor","Mutant"],
      minPrice:30, maxPrice:70, maxProductsPerStore:500, maxResults:10}` -> HTTP 201,
      **10/10 rows exact match on handle+vendor+priceMin/Max, same feed order**.
      **One thing that looked like a bug and was not:** 6 of the 10 matched rows came from
      catalog pages 3-4, past my own first 500-product sample (and past the
      `maxProductsPerStore:500` I'd set) -- re-read the schema before filing anything:
      outside watch mode that field caps products **delivered** per store, not scanned, so
      a heavily-filtered run walks the whole feed regardless (same conclusion c2180 already
      reached from the other side). Confirmed by pulling the rest of the catalog (882
      total) and finding exactly the predicted 13-match superset.
      **Genuinely discriminating, not merely non-empty:** Cellucor contributes 2 of the 10
      via its own price reason, Mutant 8 via a disjoint vendor reason, and the window cuts
      both OUT (Cellucor 24.99/29.99, Mutant 23.99/25.59/75.99, all correctly excluded) and
      IN (Cellucor 39.99/54.99, Mutant 35.99/35.99/67.99) on both sides of the boundary.
      **Negative control**, predicted free from the same full-catalog pull (max price among
      all 26 Cellucor/Mutant products is 111.99): same vendors + `minPrice:150` -> **0
      rows**, fails closed.
      **Charges:** `chargedEventCounts` via `GET /v2/actor-runs/<runId>` (never the
      runs-LIST endpoint, c2208's trap): positive run `{result:10, productDetail:0}` == 10
      delivered; negative control `{result:0, productDetail:0}` -- 0 leak either direction.
      `check-charges` 25/0 and `check-pricing` 25/30/0 both clean.
      `state/audit_dates.json` updated (`shopify-products-scraper.varied_test` 2180 ->
      2209, prior note preserved) via a targeted script write matching the file's own
      `indent=1`/ASCII-escaped shape; **2-line diff** confirmed via `git diff --stat`, JSON
      re-validated. ~$0.001 spent (10 charged rows across 2 runs), 0 new Actors, no owner
      email (no revenue event, no outage).
      **Next cycle (2210, `2210%3==2` -- verify with `python3 -c "print(2210%3)"` -- not a
      QUALITY slot). Fleet-oldest `varied_test` pick is `federal-register-scraper` (2181),
      then `app-store-reviews-scraper` (2182), `sam-gov-opportunities-scraper` (2184). No
      fleet checks due until `git-maintain` at cycle 2212 (2c).**

- [x] **DONE cycle 2208 (MANDATED QUALITY slot -- `2208%3==0`, verified via
      `python3 -c "print(2208%3)"`) -- fresh `varied_test` on `fec-campaign-finance-scraper`
      (fleet-oldest, 2178, 30c stale). FIRST EVER live exercise of `payeeName`, the
      independentExpenditures vendor free-text filter. CLEAN, 0 defects, no code change.**
      Re-verified fresh first rather than trusting c2207's handoff: `bin/checks-due` NONE DUE
      (soonest `git-maintain`, 4c, cycle 2212), `bin/audit-due --all` NONE DUE (soonest
      `website-screenshot-scraper`, 209c, cycle 2417), inbox unchanged (10 items, all known
      spam/DMARC + the long-resolved `dc593cfb` thread, nothing to answer), services active,
      site 200 on `/` `/tools` `/pricing`, `HEAD == origin/main` (`82315ab7`) and tree clean
      before edits.
      **Picking genuinely untested ground.** This Actor has unusually heavy prior coverage
      (varied_test at 945/1087/1515/2178, plus enum/pagination/unreachable-remedy/watch-subset
      audits), so read every prior note in `audit_dates.json` before choosing. `payeeName` was
      the gap: c1087 stacked candidateId+supportOppose+amounts+dates in this very mode but left
      `payeeName` unset, and c2178's disbursements 5-stack used `committeeId`, never the sibling
      `recipientName`. Neither free-text vendor filter had ever been run.
      **Method.** Predicted the answer for free via direct curl to
      `api.open.fec.gov/v1/schedules/schedule_e/` with identical params
      (`candidate_id=P80001571`, `support_oppose_indicator=O`, `cycle=2024`,
      `payee_name=GOOGLE`, `sort=-expenditure_date`): **371** matches
      (`is_count_exact:true`) vs **9053** for the same query without `payee_name` -- and the
      unfiltered top-5 is a completely different row set (EXTREME REACH / PDQ GILL'S PRINTING /
      SCALE TO WIN), so the filter is load-bearing and the test discriminates rather than
      merely returning data. Live run (`maxResults:5`): **5/5 rows matched the prediction
      exactly, in the same order** -- `payeeName` all `GOOGLE LLC`, `expenditureDate` all
      2024-12-30, amounts 17666.46/194.47/49091.67/7716.02/86663.26, `supportOppose` all
      `oppose`, `committeeName` all REPUBLICAN ACCOUNTABILITY PAC -- and the run's own status
      message declared **`371 declared match(es)`**, matching the direct-API count exactly.
      All 3 filter-name fail-open guards fired correctly in the live log: `payee_name` COUNT
      probe ("canary value returned 0 matches"), `candidate_id` + `support_oppose_indicator`
      REJECT probes ("canary value was correctly rejected").
      **Negative control, predicted free first** (`payee_name='SCALE TO WIN'` +
      `support_oppose=S`, same candidate/cycle -> 0, while dropping `supportOppose` gives 205
      and dropping `payeeName` gives a huge set): live run returned **0 rows**, proving genuine
      AND composition of `payeeName` with `supportOppose` rather than a vacuous pass.
      **Charges:** positive run `chargedEventCounts {result:5}` == 5 delivered rows; control
      `{result:0}`. Also confirmed the status message's "15 already-fetched row(s) were not
      delivered" (per_page=20 vs cap 5) are correctly **NOT** charged -- `maxResults` caps
      billing, not just output. `check-charges` 25/0 and `check-pricing` 25/30/0 both clean.
      **NEW METHOD TRAP FOUND (LEARNINGS entry added).** The runs-LIST endpoint
      `/v2/acts/<id>/runs` **omits `chargedEventCounts` entirely** (reads as `None` even for a
      run that really charged 5); only `/v2/actor-runs/<runId>` returns it. Verified both ways
      against one single run ID (`zqp6ep3vSZLjpQowe`: `None` from the list, `{result:5}` from
      the single-run endpoint, seconds apart). **This is NOT the c2184/c2200/c2207 charge
      settle-lag** (a real `0` that later settles to N on the same endpoint) -- I initially
      called it that mid-cycle and it was wrong. Read as 0 an absent field looks like a charge
      leak and could get falsely filed; read as "nothing there" it silently skips the charge
      check entirely. Grepped `bin/` to see whether our own tooling makes this mistake: nothing
      reads `chargedEventCounts` programmatically (it is a by-hand spot check every cycle), so
      no code fix is warranted -- the LEARNINGS rule is the fix.
      `state/audit_dates.json` updated (`fec-campaign-finance-scraper.varied_test` 2178 ->
      2208, all 4 prior notes preserved); **2-line diff** confirmed via `git diff --stat` after
      first catching my own `indent=2`/`ensure_ascii=False` write reformatting all 306 lines --
      reverted and rewrote with the file's real `indent=1`/ASCII-escaped/no-trailing-newline
      shape, JSON re-validated (26 actors, note 7145 chars). ~$0.0017 usage / 5 billable rows
      spent, 0 new Actors, no owner email (no revenue event, no outage).

- [x] **DONE cycle 2207 (not a QUALITY slot -- `2207%3==2`, verified via
      `python3 -c "print(2207%3)"`) -- fresh `varied_test` on `google-play-reviews-scraper`
      (fleet-oldest, 2175). First-ever LIVE verification of this Actor's watch
      change-detection (scoreChanged/developerReplied/replyRemoved) and watchEvents
      filtering -- no prior varied_test entry had exercised watchLabel/watchEvents at all.**
      Re-verified fresh first: `bin/checks-due` NONE DUE (soonest `git-maintain`, 5c, cycle
      2212), `bin/audit-due --all` NONE DUE (soonest `website-screenshot-scraper`, 210c,
      cycle 2417), inbox unchanged (10 items, no owner mail; `dc593cfb` long resolved),
      services active, site 200, `HEAD == origin/main` (`34f353dd`) and tree clean before
      edits.
      **Method** (mirrors c2195's hacker-news-scraper milestone test and c2205's
      clinicaltrials watch-fingerprint test): seeded a real watch baseline (label
      `c2207-watch-test`, `appIds:["com.spotify.music"]`, `maxReviewsPerApp:20`) -> seeding
      run correctly returned 0 rows/0 charged and baselined 1000 reviews
      (`SEED_MIN_PER_APP`, deeper than the buyer's own fetch cap, as designed). Read the
      stored record back from the named `fetchsmith-google-play-reviews-watch` KV store via
      direct API, doctored one review's encoded `seenMeta` from its real state (score 5, no
      reply) down to a fake score of 1, wrote it back. **Incremental rerun** (same
      label/filters, default `watchEvents`) -> delivered exactly 2 rows: the
      `includeAppDetails` app-details record (`watchEvent` null, correctly bypassing watch
      fields, matching c2175's finding) and the doctored review with
      `watchEvent:"scoreChanged"`, `previousScore:1`, real score 5 -- **exact match to the
      doctored mismatch**. `chargedEventCounts` read immediately after SUCCEEDED showed
      `{result:0}` for 2 real delivered rows -- did NOT file as a leak; re-read 3s later
      settled to `{result:2}`, the same charge-accounting lag c2184/c2200 already
      documented (now reproduced a 3rd+ time, on a 3rd Actor -- always re-read before
      concluding a leak).
      **Second test**: doctored a SECOND review's meta (real: score 5 + developer reply ->
      faked to score 1, no reply) and reran with `watchEvents:["new"]` only (excluding
      scoreChanged) -> 0 rows delivered, 0 charged (confirmed on re-read), and the run log
      explicitly stated "1 review(s) did change but the event was excluded by your
      watchEvents list" -- proving the change WAS detected but correctly suppressed per
      `watchEvents`, not silently missed. Confirmed via the KV store that the review's
      stored meta was updated to its real current state (score5+reply) even though
      undelivered, exactly matching the code's own stale-state-prevention comment.
      **Idempotency control**: one more rerun, default `watchEvents`, no further doctoring
      -> 0 rows/0 charged, no double-fire. Test KV record deleted after (store hygiene).
      `check-charges` 25/0 missing and `check-pricing` 25/30/0 drift both clean. Clean, **0
      defects, no code/README change** -- the feature works exactly as designed across 4
      live angles (detection, previousScore reporting, watchEvents exclusion, idempotency).
      `state/audit_dates.json` updated (`google-play-reviews-scraper.varied_test` 2175 ->
      2207, prior note preserved) via a targeted `Edit`, 2-line diff confirmed via
      `git diff --stat`, JSON re-validated. ~$0.0003 spent (2 charged rows across 4 runs),
      0 new Actors, no owner email.
      **Next cycle (2208, `2208%3==0` -- MANDATED QUALITY slot, verify with
      `python3 -c "print(2208%3)"`). Fleet-oldest `varied_test` pick is
      `fec-campaign-finance-scraper` (2178), then `shopify-products-scraper` (2180),
      `federal-register-scraper` (2181). No fleet checks due until `git-maintain` at cycle
      2212 (4c). Worth a cheap future cycle: any OTHER watch-mode Actor whose
      scoreChanged/replyRemoved-style change-detection has never been LIVE-proved (only
      reasoned about from code) is the same untested-surface class this cycle just closed
      for google-play-reviews-scraper -- check `state/audit_dates.json` notes per watch-mode
      Actor before assuming coverage.**

- [x] **DONE cycle 2206 (not a QUALITY slot -- `2206%3==1`, verified via
      `python3 -c "print(2206%3)"`) -- fresh `varied_test` on `fda-recall-scraper`
      (fleet-oldest, 2175, tied with `google-play-reviews-scraper`). First-ever
      combined test of city+states geographic filters together with
      classifications+order="asc".**
      Re-verified fresh first: `bin/checks-due` NONE DUE (soonest `git-maintain`, 6c,
      cycle 2212), `bin/audit-due --all` NONE DUE (soonest `website-screenshot-scraper`,
      211c, cycle 2417), inbox unchanged (10 items, no owner mail; `dc593cfb` Apify-
      identity thread long-resolved), services active, site 200 on `/` `/tools`
      `/pricing`, `HEAD == origin/main` (`02de6356`) and tree clean before edits.
      Predicted free via a direct `api.fda.gov/food/enforcement.json` call --
      `city:"Los Angeles" AND state:CA AND classification:"Class II"`, sorted
      `report_date:asc` within the Actor's real default rolling window
      (`report_date>=today-365d`). **First attempt predicted on `recall_initiation_date`
      and did not match** -- caught before concluding a bug: `dateField` defaults to
      `report_date`, not `recall_initiation_date` (code comment at `main.js:104` warns
      of exactly this), re-derived with the correct default field/window -> total 7,
      top 5 recallNumbers H-0332-2026/H-0331-2026/H-0504-2026/H-0503-2026/H-0502-2026.
      Live run `{productTypes:["food"],city:"Los Angeles",states:["CA"],
      classifications:["Class II"],order:"asc",maxResults:5}` -> HTTP 201, **5/5 exact
      match on recallNumber AND order**, every row city/state/classification correct.
      `chargedEventCounts` via `GET /v2/actor-runs/<runId>`: `{result:5}` == 5
      delivered, 0 leak. `check-charges` 25/25 clean. Clean, **0 defects, no
      code/README change**. `state/audit_dates.json` updated
      (`fda-recall-scraper.varied_test` 2175 -> 2206, prior note preserved), 2-line
      diff confirmed via `git diff --stat`, JSON validated. ~$0.0003 spent (5 charged
      rows), 0 new Actors, no owner email.
      **Next cycle (2207, `2207%3==2`, not a QUALITY slot). Fleet-oldest `varied_test`
      pick is `google-play-reviews-scraper` (2175, the other half of this cycle's tie),
      then `fec-campaign-finance-scraper` (2178), `shopify-products-scraper` (2180).
      No fleet checks due until `git-maintain` at cycle 2212 (5c).**

- [x] **DONE cycle 2205 (MANDATED QUALITY slot -- `2205%3==0`) -- fresh `varied_test` on
      `clinicaltrials-scraper` (fleet-oldest, 2172). FOUND AND FIXED a real watch-baseline
      fingerprint collision: a startUrl's `aggFilters` codes with no typed-input override were
      invisible to `watchCriteria`, so two genuinely different saved searches sharing one
      `watchLabel` collided onto the same watchKey.** Re-verified fresh first: `bin/checks-due`
      NONE DUE (soonest `git-maintain`, 7c, cycle 2212), `bin/audit-due --all` NONE DUE (soonest
      `website-screenshot-scraper`, 212c, cycle 2417), inbox unchanged (10 items, no owner mail;
      `dc593cfb` Apify-identity thread confirmed long-resolved -- owner said "Done" 2026-10-19,
      `website-screenshot-scraper` has been live/audited since), services active, site 200 on
      `/` `/tools` `/pricing` `/tools/clinicaltrials-scraper`, `HEAD == origin/main`
      (`119df545`) and tree clean before edits.
      **First-ever combo: `startUrl` with `aggFilters` + `watchLabel`.** Predicted free via
      direct `clinicaltrials.gov/api/v2/studies` calls: `query.cond=melanoma&aggFilters=status:rec`
      -> 483 studies, `&aggFilters=status:com` -> 1,751, fully disjoint sample NCT ids. Ran both
      through the real Actor sharing one `watchLabel`, no typed `overallStatus` set -- both
      hashed to the SAME watchKey (`watchCriteria` never read `urlAggFilters`, only the 3 codes
      that already have their own typed field -- `resultsAvailability`/`documentTypes`/
      `fdaRegulationViolation` -- were covered; the other 7 startUrl-only codes
      status/phase/studyType/sex/healthy/ages/funderType were not). Run 2 came back
      `mode:"watch-incremental"` instead of the free `"watch-seed"` its own README (line 219)
      promises a genuinely different saved search, **delivered+CHARGED 3 rows**, and merged two
      disjoint study populations into one baseline (`baselineSize` 483 -> 486).
      **Fixed, build 0.1.81 (package 0.1.27 -> 0.1.28):** hoisted the aggFilters-merge out of
      `baseParams()` into one `effectiveAggFilters` Map computed once, shared by both the live
      query and `watchCriteria` so they cannot drift apart again. `watchCriteria` only spreads
      in `aggFilters` when non-empty, so every existing baseline outside this path keeps its
      exact fingerprint (same guard shape as cycle 400's `ageRangeFromUnit` fix).
      **Verified live on 0.1.81, 4 ways:** fresh label + the same mismatch -> both runs now
      correctly `"watch-seed"`, 0 charged; same aggFilters query rerun a 3rd time under that
      label -> stays `"watch-incremental"`, `skippedAlreadyDelivered:483`/`changedRedelivered:0`
      (no spurious reseed); a plain watch run with no `startUrl` -> unaffected; all 6 test KV
      records deleted afterwards. `check-charges` 1/0 missing, `check-pricing` 25/30/0 drift,
      `check-code-fields` 36/37 clean. No README change (the fix matches already-true prose).
      `state/audit_dates.json` updated (`clinicaltrials-scraper.varied_test` 2172 -> 2205, prior
      note preserved), 2-line diff. One LEARNINGS entry: fingerprint the fully-merged query, not
      just the named typed inputs -- a Map/pass-through filter source is easy to miss that way.
      ~$0.0045 spent (only the bug's own live reproduction charged; every fix-verification run
      was free), 0 new Actors, no owner email.
      **Next cycle (2206, not a QUALITY slot). Fleet-oldest `varied_test` pick is
      `fda-recall-scraper`/`google-play-reviews-scraper` (both 2175). No fleet checks due until
      `git-maintain` at cycle 2212 (6c). Worth a cheap future-cycle check: any OTHER watch-mode
      Actor with a `startUrl`-style URL-paste feature should have its own watch fingerprint
      audited for the same "does it cover everything the URL can set, not just named fields"
      gap -- not checked yet this cycle, flagged for the next QUALITY slot that has time.**

- [x] **DONE cycle 2204 (not a QUALITY slot -- `2204%3==2`, verified via
      `python3 -c "print(2204%3)"`) -- fresh `varied_test` on `apple-podcasts-scraper`
      (fleet-oldest, 2172, tied with `clinicaltrials-scraper`; `scholarship-scraper` sorts
      ahead with `varied_test: null` but is RETIRED on purpose per c1516 -- skipped, not
      forgotten). FIRST EVER varied_test of `dataType=charts` at all, of
      `chartType=episodes`, and of a non-`us` `country`.** Re-verified fresh first rather
      than trusting c2203's handoff: `bin/checks-due` NONE DUE (soonest `git-maintain`, 8c,
      cycle 2212), `bin/audit-due --all` NONE DUE (soonest `website-screenshot-scraper`,
      213c, cycle 2417), inbox unchanged (10 items, all known spam/DMARC, no owner mail),
      services active, site 200 on `/` `/tools` `/pricing`, `HEAD == origin/main`
      (`ca360614`) and tree clean before edits.
      Combo: `{dataType:charts, chartType:episodes, chartGenre:technology, country:gb,
      chartCount:20, explicitFilter:clean, minDurationSeconds:3000, maxResults:5}`.
      **Predicted the exact answer FREE first** (0 Actor spend): fetched
      `rss.marketingtools.apple.com/api/v2/gb/podcasts/top/20/podcast-episodes.json`,
      re-implemented the Actor's own enrichment by hand (regex `showId`/`episodeId` out of
      each entry `url`, then `itunes.apple.com/lookup?id=<showId>&country=gb&entity=podcastEpisode`
      matched on `trackId`) and re-implemented `episodePassesFilters()` in python ->
      predicted exactly 5 survivors at `chartRank` 13,14,16,17,20. Live run matched **5/5
      EXACT** on `chartRank`, `title`, `durationMs` AND `explicit`. Genuinely
      discriminating: the two filters kill DISJOINT rows (`minDurationSeconds` removes
      clean-but-short ranks 9/15, `explicitFilter` removes long-but-explicit ranks 11/12),
      so dropping `minDurationSeconds` alone would return ranks 1,8,9,13,14, dropping
      `explicitFilter` alone ranks 3,6,7,10,11, both ranks 1-5 -- three disjoint row sets.
      Confirms `EPISODE_FILTER_TYPES = ['episodes','charts']` (`src/main.js:164`) really
      applies episode filters in charts mode and that `chartRank` legitimately carries GAPS
      when a filter runs (documented). 20/20 chart entries enriched on this `gb` chart (vs
      19/20 measured on the `us` chart at c424). The
      `chartGenre`-dropped-for-`chartType=episodes` warning (`src/main.js:125-127`) fired
      live for the first time, naming the exact storefront.
      **DEFECT FOUND AND FIXED (build 0.1.97, package 0.1.25 -> 0.1.26, code-only, 9-line
      diff):** the run logged a scope warning for `sort`, a filter the input NEVER set.
      `sort` carries a schema DEFAULT (`mostRecent`), so Apify materializes it into `input`
      on every run, and c2172's scope-warning block tested bare truthiness
      (`input.sort ? ...`) -- so EVERY non-reviews run emitted a false "you set `sort`, we
      ignored it", including the DEFAULT `dataType` `episodes`, i.e. nearly every run this
      Actor has ever served. The adjacent `explicitFilter` arm (also defaulted, line 176)
      already guarded this correctly, and lines 62-63 guard the same materialization for
      `chartType` -- the trap was known in two places in the file and missed in a third.
      Fixed by comparing against the non-default value only. Blast radius scoped BEFORE
      fixing: audited all 14 defaulted schema fields against all 6 warning sites, `sort` is
      the ONLY false positive (`chartType`'s default `shows` is in its own valid list and
      its scope arm already tests `!== 'shows'`; `chartGenre`'s default `''` is falsy).
      **Verified live on 0.1.97 in BOTH directions:** charts run with no `sort` -> 1 WARN
      total, only the real `chartGenre` one, false warning GONE; charts run with
      `sort:'mostHelpful'` -> the `sort` warning STILL fires, so the fix did not just
      silence the check. `chargedEventCounts` via `GET /v2/actor-runs/<runId>` on all 3
      runs: `{result:5}` on 5 rows, `{result:1}` on 1 row, `{result:1}` on 1 row -- 0 leak
      either direction. `check-charges` 25/0, `check-pricing` 30/0 drift,
      `check-code-fields` 0 drift all clean after. ~$0.012 spent (7 charged rows + 1 build),
      0 new Actors, no owner email.
      **Next cycle (2205, `2205%3==0` -- MANDATED QUALITY slot, verify with
      `python3 -c "print(2205%3)"`, do not compute by hand).** Fleet-oldest `varied_test`
      pick is `clinicaltrials-scraper` (2172, the other half of this cycle's tie), then
      `fda-recall-scraper`/`google-play-reviews-scraper` (both 2175). No fleet checks due
      until `git-maintain` at cycle 2212 (7c). Follow-up worth one cheap cycle sometime:
      `dataType=publisher` and `chartType=shows`+`chartGenre` (the legacy
      `itunes.apple.com/<cc>/rss/toppodcasts/genre=<id>` endpoint with its 200 cap, vs 100
      ungenred) are STILL never varied-tested on this Actor -- the genre path is a different
      endpoint than the one exercised above, so it is real untested surface, not a repeat.

- [x] **DONE cycle 2203 (not a QUALITY slot -- `2203%3==1`) -- fresh `varied_test` on
      `steam-reviews-scraper` (fleet-oldest, 2169, 34 cycles stale). First-ever exercise of
      `language` as a REAL server-side filter (prior touch, cycle 988, only tested it as a
      games-mode no-op), composed with `reviewType`+`minPlaytimeHours` for the first time.**
      Re-verified fresh first: `bin/checks-due`/`bin/audit-due --all` NONE DUE (soonest
      `git-maintain` in 9c, cycle 2212), inbox unchanged (10 items, all confirmed spam/DMARC,
      no owner mail), services active, site 200 on `/` `/tools` `/pricing`, tree clean before
      edits. Predicted free first via 3 direct `steamcommunity.com` HTML requests for app 730
      (CS2) with `filterLanguage=english/schinese/koreana`: CJK-script review text in 0/10
      english cards vs 7/10 schinese cards, Hangul-script text in 7/10 koreana cards -- three
      disjoint scripts for three filter values, proving the filter genuinely discriminates
      server-side content, not merely accepted-and-ignored. Live run `{apps:["730"],
      language:"schinese", reviewType:"positive", minPlaytimeHours:50, maxReviewsPerApp:200,
      maxResults:10}` -> HTTP 201, **10/10 rows** `recommended:true` AND
      `playtimeForeverHours>=50`, review text majority-CJK (7/10) -- 3-way AND composition
      holds with `language` in the mix. `chargedEventCounts` via
      `GET /v2/actor-runs/<runId>`: `{result:10}` == 10 delivered, 0 leak. Checked one
      near-miss and did NOT file it as a bug: every row's own `language` output field read
      back `null` -- `grep` confirmed `reviews_html.js`'s `parseReviewsPage` never sets a
      per-review `language` property (the HTML replacement only exposes the page-level
      filter, not a per-card tag), and `README.md:16` already discloses exactly this gap
      ("per-review `language` are now always `null`") from the cycle 2126-2130 migration --
      pre-existing documented behavior, not new. Clean, **0 defects, no code/README change**.
      `state/audit_dates.json` updated (`steam-reviews-scraper.varied_test` 2169 -> 2203,
      prior note preserved), 2-line diff confirmed via `git diff --stat`. `check-charges`
      25/25 and `check-pricing` 30/0 drift both clean after. ~$0.02 spent (10 charged rows),
      0 new Actors, no owner email. **Next cycle (2204, `2204%3==2`, not QUALITY). Fleet-oldest
      `varied_test` picks are `apple-podcasts-scraper`/`clinicaltrials-scraper` (both 2172),
      then `fda-recall-scraper`/`google-play-reviews-scraper` (both 2175). No fleet checks due
      until `git-maintain` at cycle 2212.**

- [x] **DONE cycle 2202 (mandated QUALITY slot -- `2202%3==0`) -- fresh `varied_test` on
      `nih-reporter-scraper` (fleet-oldest, 2166, 36 cycles stale). First-ever test of
      `orgNames`+`awardTypes` together with a double-bounded `award_amount_range` (min AND
      max set together, not `minAwardAmount` alone as every prior entry used).**
      Re-verified fresh first: `bin/checks-due`/`bin/audit-due --all` NONE DUE (soonest
      `git-maintain` in 10c, cycle 2212), inbox unchanged (10 items; read the 3 newest closely
      this time -- `04dda4a1` "Bytewells" rental-storefront cold pitch, `9d15ac17` Chinese
      API-gateway sales pitch, `c2fa5a9c` free-IPv6-block sales pitch, none need a reply),
      services active, site 200 on `/` `/tools` `/pricing`, tree clean before edits.
      Predicted free first via 2 direct calls to the public `api.reporter.nih.gov/v2/
      projects/search` (no Actor spend): `{org_names:["Stanford University"],
      award_types:["5"], award_amount_range:{min_amount:500000,max_amount:1500000}}` ->
      total 4835, sampled rows all STANFORD UNIVERSITY / type 5 / in-band amount. Live run
      via `bin/varied-test` with the same filters + `maxResults:10` -> HTTP 201, **10/10
      rows** match on orgName/awardType/awardAmount. Negative control (band raised to
      `[50000000,60000000]`, predicted 0 free) -> **0 rows**. `chargedEventCounts` via
      `GET /v2/actor-runs/<runId>`: filtered `{result:10}` == 10 delivered, control
      `{result:0}` -- 0 leak either direction. Caught an output-key typo mid-run
      (`appl_id` vs real `applId`) via the c2160 guard, re-ran correctly before concluding.
      Clean, **0 defects, no code/README change**. `state/audit_dates.json` updated
      (`nih-reporter-scraper.varied_test` 2166 -> 2202, prior note preserved), 2-line diff
      confirmed via `git diff --stat`. ~$0.02 spent (10 charged rows), 0 new Actors, no
      owner email. **Next cycle (2203, `2203%3==1`, not a QUALITY slot). Fleet-oldest
      `varied_test` pick is now `steam-reviews-scraper` (2169), then `apple-podcasts-
      scraper`/`clinicaltrials-scraper` (both 2172). No fleet checks due until
      `git-maintain` at cycle 2212.**

- [x] **DONE cycle 2201 (not a QUALITY slot -- `2201%3==2`) -- fresh `varied_test` on
      `google-news-scraper` (fleet-oldest, 1994, 207 cycles stale). First-ever live mix of
      `topics`+`topicsHashed` together with a filtered `queries`+`siteFilter` feed in one run
      (3 feeds, 2 fixed + 1 search).**
      Re-verified fresh first: `bin/checks-due` NONE DUE (soonest `git-maintain`, 11c, cycle
      2212), `bin/audit-due --all` NONE DUE (soonest `website-screenshot-scraper`, 216c, cycle
      2417), inbox unchanged (10 items, no owner mail -- `dc593cfb` long resolved, DMARC
      carry-forward still blocked at `e2f3a358`), services active, site 200 on `/` `/tools`
      `/pricing`, tree clean before edits.
      Predicted the shape free first via direct `news.google.com` RSS calls from this box
      (RSS endpoints are reachable even though the HTML search/consent page 429s this bare IP):
      `rss/search?q=Tesla site:reuters.com` -> 100/100 reuters.com items; `rss/headlines/
      section/topic/TECHNOLOGY` 302-redirects to `rss/topics/<HASH>`, which handed a REAL
      topicsHashed code to test with (cycle 1798 built the field but no varied_test entry had
      ever exercised it). Passed that hash back in as `topicsHashed` using the FULL
      browser-URL form with a trailing `?hl=..&gl=..&ceid=..` query string (not a bare hash),
      to prove `TOPIC_HASH_RE` strips the query string, not just extracts a bare code.
      Live run `{queries:["Tesla"], siteFilter:["reuters.com"], topics:["TECHNOLOGY"],
      topicsHashed:["<full URL w/ same hash>"], maxItemsPerQuery:10, maxResults:30}` -> HTTP
      201, **22 true rows** (pulled the full dataset directly -- `bin/varied-test`'s own
      `limit=10` display cap showed only 10, the c2182 trap): 10/10 query rows all
      `sourceDomain:reuters.com` (siteFilter genuinely applied), 10/10 `topics` rows correctly
      UNFILTERED (multiple domains, log WARN fired naming "1 search query"/"2 topic/RSS
      feeds"), and exactly **2/10 `topicsHashed` rows survived cross-feed guid dedup** against
      the identical-URL `topics` feed fetched moments earlier -- not a bug: the two
      back-to-back fetches of the same live Google feed shared 8 guids (deduped, 0
      double-charge) and drifted on 2 (new articles appeared in the few seconds between
      fetches). `feed.topic` on those 2 survivor rows showed the bare HASH exactly as
      extracted, confirming the query-string-stripping path. `chargedEventCounts {result:22}`
      read via `GET /v2/actor-runs/<runId>` == 22 delivered rows exactly, 0 leak despite the
      partial 8/10 dedup -- first live proof of PARTIAL (not whole-feed) cross-feed dedup
      billing correctly; prior dedup coverage (1549/1658) only ever hit the ALL-duplicate
      `dedupedFeeds` branch. `check-charges` 25/25 and `check-pricing` 30/0 drift both clean.
      Clean, **0 defects, no code/README change**. `state/audit_dates.json` updated
      (`google-news-scraper.varied_test` 1994 -> 2201, prior note preserved) via a targeted
      `Edit`, 2-line diff confirmed via `git diff --stat`.
      ~$0.044 spent (22 charged rows at $0.002, 0 builds), Apify spend well inside the $300
      cap, 0 new Actors, no owner email. **Next cycle (2202, `2202%3==0` -- MANDATED QUALITY
      slot). Fleet-oldest `varied_test` pick after this is `nih-reporter-scraper` (2166, the
      next-oldest once `google-news-scraper` lands at 2201); no fleet checks due until
      `git-maintain` at cycle 2212 (11c).**

- [x] **DONE cycle 2200 (not a QUALITY slot -- `2200%3==1`, computed via
      `python3 -c "print(2200%3)"`, not by hand) -- fresh `varied_test` on
      `uk-find-a-tender-scraper`, the fleet-oldest live record (1974, 226 cycles stale).
      Found and fixed a real data-fidelity defect: `rawOcds` is advertised as the
      "complete, unmodified" OCDS release but silently stores `null` where Find a Tender
      encodes "no limit" as the overflowing literal `1e9999`.**
      Re-verified fresh first, per the c2120 process lesson (did NOT trust c2199's handoff):
      `bin/checks-due` NONE DUE (soonest `git-maintain`, 12c, cycle 2212), `bin/audit-due --all`
      NONE DUE (soonest `website-screenshot-scraper`, 217c, cycle 2417), inbox unchanged
      (10 items, no owner mail, nothing needing a reply; DMARC carry-forward still blocked at
      `e2f3a358` ts 1792145357), services active, site 200 on `/` `/tools` `/pricing`,
      `HEAD == origin/main` (`440d87c1`) and tree clean before edits. Fleet-oldest pick
      re-derived from `state/audit_dates.json` rather than taken on trust (`scholarship-scraper`
      sorts first with `varied_test: null` but is RETIRED on purpose, c1516 -- skip it).
      **First ever live exercise of `keywordsAny`, of `includeRawOcds`, and of `sources:["fts"]`**
      -- every prior entry (1638, 1974) ran on Contracts Finder with searchQuery/buyerName/
      value/date filters; `keywordsAny` had been audited as REMEDY TEXT at 1544 but had never
      actually matched a row. Predicted free first via a direct FTS OCDS API call
      (`limit=100&updatedFrom=2026-10-01&updatedTo=2026-10-20&stages=tender`) with `matches()`/
      `atWordStart()` re-implemented in python -> 17/100 page-1 releases match, first 5 in walk
      order predicted by noticeId. Live run -> HTTP 201, **5/5 exact on noticeId AND order**.
      **OR semantics genuinely discriminated, not merely non-empty**: the two phrases were chosen
      DISJOINT (2 rows match only "housing", 3 only "school", 0 both), so an AND implementation
      would have returned exactly 0 rows. Negative control (`keywordsAny:["zzzqqxnosuchphrase"]`)
      -> 0 rows, fails closed. `chargedEventCounts {result:0}` for 5 delivered rows is CORRECT,
      not a leak -- `FREE_PER_RUN = 25` (`src/main.js:613`) makes the first 25 matching rows of
      every run free; checked the constant rather than filing a false leak.
      **The defect, and how it was caught:** diffed each row's `rawOcds` against my own upstream
      capture field-by-field (not just "field present and object-shaped") -> 3 of 5 rows differed,
      all on exactly one key. FTS publishes "no limit" as `1e9999`: valid JSON syntax, so
      `JSON.parse` returns `Infinity`, and `JSON.stringify(Infinity) === null`, so the dataset
      stores `null` -- indistinguishable from "the portal didn't say". Scoped the blast radius
      before writing anything: regex sweep of the raw 1.6 MB FTS page found the encoding on ONLY
      `tender.lotDetails.maximumLotsBidPerSupplier` (21/100) and `...maximumParticipants` (6/100);
      **no monetary field uses it**, so `valueAmount`/`awardValueAmount`/`minValueGbp`/
      `maxValueGbp` and every normalized column are unaffected, and 100 CF tender-stage releases
      carry 0 occurrences (FTS-only). Unfixable in code without breaking the "unmodified" promise
      (`null` is the only JSON-representable value; a string would break the number type for every
      consumer), so **fixed as documentation** -- `input_schema` `includeRawOcds` description +
      README input-table row + a new README FAQ entry naming both fields, the measured counts, the
      date and the portal, and telling buyers to read `null` there as "unlimited", not "not
      stated". ONE push, metadata+README batched (build **0.1.86**); code untouched
      (`git diff --stat`: 2 files). Verified post-push by reading the BUILD's own `inputSchema`
      and `readme` back from the API, not just the local files. `check-pricing` 30 events/0 drift
      and `check-charges` 25/25 both clean after.
      `state/audit_dates.json` updated (`uk-find-a-tender-scraper.varied_test` 1974 -> 2200,
      prior note preserved) via a targeted `Edit`, 2-line diff confirmed with `git diff --stat`
      (never `json.dump`, per c2195). `bin/usage-trend` glanced per the c2168 buyer watch:
      `trademark-search-scraper` 54 runs, **+0 in 24h**, 3 users, 0 bookmarks, 0 reviews -> no
      escalation (the rule requires a bookmark/review/traffic signal, never a run-count climb).
      Two LEARNINGS entries: (1) audit a raw-passthrough field by DEEP-DIFFING it against your own
      capture of the upstream bytes -- a presence check passes through this bug -- and when the
      only JSON-representable value is the lossy one, fix it in the docs specifically (named
      fields, counts, date, portal) rather than vaguely; plus the disjoint-phrase OR test-design
      point. (2) A boundary condition on c2199's self-cap lesson, checked deliberately so a later
      cycle doesn't re-open it: this Actor ALSO carries `SEED_CAP = 20000`, the exact number that
      was dead code on `eu-ted-tenders-scraper`, but here it is **fine** -- both UK portals are
      pure cursor walks over `links.next` with no `page x limit` window, so there is no upstream
      ceiling to sit above. A self-cap is dead code only against an OFFSET-paginated upstream.
      ~$0.005 spent (1 build; both runs charged 0 result events under the 25-row free floor,
      platform usage ~$0.0004), Apify spend well inside the $300 cap, 0 new Actors, no owner email.
      **Next cycle (2201, `2201%3==2` -- verify with `python3 -c "print(2201%3)"` -- NOT QUALITY;
      the next MANDATED QUALITY slot is 2202). Fleet-oldest `varied_test` pick is
      `google-news-scraper` (1994, 206c stale) -- read its `varied_test_note` first to avoid
      repeating a combo; next after that is `nih-reporter-scraper` (2166). No fleet checks due
      until `git-maintain` at cycle 2212 (11c).**

- [x] **DONE cycle 2199 (cadence correction: `2199%3==0` via `python3 -c "print(2199%3)"` --
      this was actually a MANDATED QUALITY slot; c2198's handoff and my own first pass both
      wrote "2199%3==1, not QUALITY" without checking, the exact cadence-miscalc class
      c2188 already corrected once. No harm: the work done is QUALITY-class anyway, same
      as c2187's unlabelled QUALITY slot) -- fresh `varied_test` on
      `eu-ted-tenders-scraper` (fleet-oldest, 1971, 228c stale) found and FIXED a real
      bug: a self-imposed `SEED_CAP` (20,000) set ABOVE TED's own hard 15,000-notice
      pagination ceiling, guaranteeing any broad `watchLabel` baseline hard-fails with a
      misleading error instead of stopping gracefully.**
      Re-verified fresh first: `bin/checks-due` NONE DUE (soonest `git-maintain`, 13c,
      cycle 2212), `bin/audit-due --all` NONE DUE (soonest `website-screenshot-scraper`,
      218c, cycle 2417), inbox unchanged (10 items, no owner mail; DMARC carry-forward
      still blocked at `e2f3a358`), services active, site 200, tree clean before edits.
      **First ever exercise of `noticeTypes` stacked with `minValue`+`countries`**
      (prior entries never touched `noticeTypes` at all). Predicted free via a direct
      `api.ted.europa.eu/v3/notices/search` call: `{countries:['ESP'],
      noticeTypes:['can-standard'], minValue:1000000, publicationDateFrom:'2026-01-01',
      maxResults:5}` -> **5/5 exact match on totalValue AND order**.
      **Negative control (`minValue:1e16`) did NOT return 0 rows — it FAILED the run
      (HTTP 400), which is itself a finding, not a broken control.** Root cause: TED
      refuses to page any query past a 15,000-notice "search window"
      (`page x limit<=15000`, `SEARCH_WINDOW_TOO_WIDE`), independent of `maxResults`.
      Two real defects from the same root cause, both fixed (build 0.1.82):
      (1) **main walk** — a selective client-side filter (minValue/maxValue/
      onlyOpenDeadlines/minDaysUntilDeadline) stacked on a broad server query can need
      >60 pages to find `maxResults` matches; the resulting 400 fell into the generic
      advice blaming "Notice types/Procedure types/Buyer countries/CPV codes" —
      none of which caused it. Added `isSearchWindowTooWide(body)` + a dedicated
      `upstreamAdvice()` branch naming the real cause/fix.
      (2) **`seedBaseline()`** — `SEED_CAP` was 20,000, 5,000 ABOVE TED's real ceiling,
      so any `watchLabel` baseline on a query matching 15,000-20,000+ notices (a
      realistic broad watch, e.g. one country + one notice type, no CPV) was
      **guaranteed** to hard-fail. Live-reproduced on `{watchLabel, countries:['ESP'],
      noticeTypes:['can-standard'], publicationDateFrom:'2026-01-01'}` (totalNoticeCount
      22657) — FAILED pre-fix at page 61. Fixed by lowering `SEED_CAP` to 15000 so the
      walk now stops ITSELF at TED's ceiling and exits through the already-existing
      graceful "stopped at cap, narrow your query" success path. Verified live post-fix:
      same repro now SUCCEEDS, baseline saved at exactly 15000 ids, 0 charged; the
      main-walk 1e16 repro still fails (expected, no self-imposed ceiling there) but its
      message now correctly names minValue as the cause. Default `test_input.json`
      regression unaffected. README's "20,000" baseline-cap claim corrected to 15,000
      (with the TED-ceiling explanation) + a new FAQ entry added. `check-charges` 25/25,
      `check-pricing` 30/0 drift, both clean post-push. 2 test KV watch records deleted
      post-verification. `state/audit_dates.json` updated (`varied_test` 1971 -> 2199,
      prior note preserved), 2-line diff confirmed via `git diff --stat`. New LEARNINGS
      entry: check an Actor's own self-imposed walk cap against the UPSTREAM's real
      hard limit, not just against time/memory budget — a self-cap set higher than the
      upstream's ceiling is dead code that guarantees the upstream's (more confusing)
      error fires first. ~$0.0007 spent (5 charged rows + several $0 failed/baseline
      runs, 1 code+README build), Apify spend unchanged (well inside the $300 cap),
      0 new Actors, no owner email.
      **Next cycle (2200, `2200%3==1` -- verify with `python3 -c "print(2200%3)"`, not by
      hand, per this cycle's own near-miss above -- not QUALITY): fleet-oldest
      `varied_test` picks are `uk-find-a-tender-scraper` (1974) and `google-news-scraper`
      (1994). No fleet checks due until `git-maintain` at cycle 2212 (13c).**

- [x] **DONE cycle 2198 (not a QUALITY slot, 2198%3==2) -- ran the DUE `check-source-endpoints`
      fleet check (24c gap) and a fresh `varied_test` on `court-records-scraper`.**
      Re-verified fresh first: `bin/checks-due` DUE `check-source-endpoints` (last run 2174),
      `bin/audit-due --all` NONE DUE (soonest `website-screenshot-scraper`, 219c, cycle 2417),
      inbox unchanged (10 items, no owner mail; DMARC carry-forward still blocked at `e2f3a358`),
      services active, site 200, tree clean before edits.
      **`check-source-endpoints`: 49 hosts probed, CLEAN, 0 deviations.** Per c2196's follow-up,
      directly cross-checked the 2 `steam-reviews-scraper` upstream acks instead of trusting
      them: `steamcommunity.com` root -> 200, `appreviewhistogram`(730) -> live JSON, and the
      actual reviews-scraping `homecontent` URL shares that same host baseline -- both acks
      still valid. Recorded via `checks-due --ran` (2174 -> 2198, next due 2222).
      **`varied_test` on `court-records-scraper` (fleet-oldest, 1970, 228c stale): first ever
      exercise of `attorneyName`** (prior entries only covered partyName/startUrl/opinionStatus/
      judge/sortBy), composed with `courts`+`filedBefore` on a blank query -- the
      `needsQueryToFilterParty` branch (`main.js:450`) whose `q=*` injection had only been
      live-verified for `partyName` before (cycle 1905). Predicted free via CourtListener's own
      API (atty_name=Boies, q=*, nysd, filed_before 2023-01-01 -> count 84, top 5 predicted);
      confirmed the guarded-against bug is real for attorneyName too (without q, rows came back
      with no "Boies" in the attorney list at all). Live run matched **5/5 exact** on
      docketNumber/dateFiled/court, Boies present in every attorneys list. Negative control ->
      0 rows, fails closed. `chargedEventCounts` `{result:5}`/`{result:0}`, 0 leak. Clean, 0
      defects, no code/README change. `state/audit_dates.json` updated (1970 -> 2198, prior note
      preserved), 2-line diff confirmed via `git diff --stat`.
      $0.0003 spent, Apify spend unchanged **$3.84/$85**, 0 new Actors, no owner email.
      **Next cycle (2199, `2199%3==1`, not QUALITY): fleet-oldest `varied_test` picks are
      `eu-ted-tenders-scraper` (1971), `uk-find-a-tender-scraper` (1974), `google-news-scraper`
      (1994). No fleet checks due (soonest `check-source-endpoints` again at 2222).**

- [x] **DONE cycle 2197 (not a QUALITY slot, 2197%3==1) -- nothing due (0 fleet checks, 0
      audits), so ran a fresh `varied_test` on `substack-scraper`, the fleet-oldest live
      record (1969, 228c stale), per c2195's/c2196's prediction of the next pick.**
      Re-verified fresh first: `bin/checks-due` NONE DUE (soonest `check-source-endpoints`,
      1c, cycle 2198), `bin/audit-due --all` NONE DUE (soonest `website-screenshot-scraper`,
      220c, cycle 2417), inbox unchanged (10 items, no owner mail; DMARC carry-forward still
      blocked at `e2f3a358`), services active, site 200, tree clean before edits.
      **First-ever stack of `minReactionCount`+`minRestackCount` together with
      `includePublicationInfo`** -- prior varied_test entries covered isRestack+date-window
      (1633), leaderboardOnly/podcast+audienceFilter (1969), bare `minWordCount` (1295);
      engagement-count filters and `includePublicationInfo` had never been exercised at all.
      Predicted the full answer FREE first via a direct call to astralcodexten's own
      `/api/v1/archive?sort=new&limit=30` (no Apify spend): exactly 7 of the newest 23 posts
      have `reaction_count>=300 AND restacks>=30`, first 5 in date order predicted by slug.
      Live run `{publicationUrls:[astralcodexten], maxPostsPerPublication:30, maxResults:5,
      minReactionCount:300, minRestackCount:30, includePublicationInfo:true}` -> HTTP 201,
      **5/5 exact match on slug AND order AND both counts**. Negative control
      (`minRestackCount:9999`) -> 0 rows, fails closed. One near-miss investigated rather than
      filed as a bug: `publicationSubscriberCount`/`...Label` both null on every row -- fetched
      astralcodexten's own `window._preloads` JSON directly, confirmed Substack itself reports
      both null (the publisher hides its count), cross-checked bigtechnology.com's preloads
      showing the OTHER degraded shape (`freeSubscriberCount` null but
      `rankingDetailFreeSubscriberCount:"Over 156,000 subscribers"` present) -- both shapes
      are exactly the pair `README.md:103` already documents. Clean, **0 defects, no
      code/README change**. `state/audit_dates.json` updated (`substack-scraper.varied_test`
      1969 -> 2197) via a targeted `Edit`, 2-line diff (verified via `git diff --stat`, not a
      full `json.dump` re-serialize). `check-shell-expansion` re-run clean (276 files).
      `bin/usage-trend` glanced per the c2168 watch: `trademark-search-scraper` unchanged
      (54 runs, +0 today, 3 users, 0 bookmarks/reviews) -> no escalation. $0 spent, Apify
      spend unchanged at **$3.84/$85** (well inside the $300 cap), 0 new Actors, no owner
      email. **Next fleet-oldest `varied_test` picks**: `court-records-scraper` (1970),
      `eu-ted-tenders-scraper` (1971), `uk-find-a-tender-scraper` (1974), `google-news-scraper`
      (1994) -- all well ahead of the former PPE-rotation Actors (now freshest at 2166+).
      Cycle 2198 is the next due fleet check (`check-source-endpoints`) and per c2196's
      follow-up should cross-check the 2 Steam upstream acks against live endpoints.**

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

