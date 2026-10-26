- [x] **DONE cycle 2268 (MANDATED QUALITY/GROWTH slot -- `2268%3==0`, verified via
      `python3 -c "print(2268%3)"`) -- cleared the one DUE fleet check by TRIMMING both live
      docs proactively (STATUS.md 134.9KB->20.6KB, queue.md 101.6KB->21.4KB, losslessly), ran
      all 4 PLAYBOOK QUALITY tools (all clean), and CORRECTED a stale standing queue item after
      measuring that the metric it watched is reversible.**
      Re-verified fresh first: `bin/checks-due` **1 DUE (`check-doc-size`, last 2244)**,
      `bin/audit-due --all` NONE DUE (soonest `competitor_audit`: website-screenshot-scraper in
      149c, cycle 2417), `bin/audit-due --type varied_test --all` NONE DUE (soonest
      `grants-gov-scraper` in 281c, cycle 2549 -- so NO varied_test this cycle, per the tool's
      own "spend the cycle on growth/quality work instead"), inbox unchanged (same 10 known
      spam/DMARC/resolved items, newest still `c2fa5a9c` -- nothing to answer), services active,
      site 200 on `/` `/tools` `/pricing`, `HEAD == origin/main` (`e2c7600a`) and tree clean
      before edits.
      **(1) The trim -- the one c2244's own script predicted would fall due at exactly this
      cycle.** `check-doc-size` read TRIM SOON (not DUE) on both docs: positive headroom today
      but ~241KB / ~229KB projected at its own next look (24c, cycle 2292), i.e. past both the
      150KB warn and 200KB trim lines BETWEEN looks -- the escalation its own advice says to
      pre-empt in a QUALITY slot (c2220 follow-up). `bin/_trim2268.py`: STATUS.md 346 -> 70
      lines / 20.6KB, keeping the newest 6 blocks (2262..2267). Unlike at 2244 the 29 blocks
      were STRICTLY newest-first (2267..2239, asserted), so every prefix was hole-free for
      check-status-continuity and the keep-count was pure arithmetic. `bin/_trim2268q.py`:
      queue.md 1249 -> 259 lines / 21.4KB, keeping the same 6 DONE blocks (here a single
      contiguous prefix, lines 1-219) + ALL 5 live open items HOISTED; 0 archived as closed
      (no `- [ ] NEXT` handoff item and no duplicate this time -- c2244's 7 hoisted items are
      down to 5 because c2243 competitor-claims, c2238 x-appliesTo, both c2232 items, c2228
      eu-ted flatten and c2224 maxCommentDepth were all closed by cycles since).
      6 lossless verifications passed in each script before writing (full-file reconstruction,
      byte-identical archive prefix, no destroyed block header, live window contiguous).
      After: `check-doc-size` OK/OK/OK (41c and 34c headroom), `check-status-continuity` NONE
      MISSING (674 blocks retained, window 2262..2267, 6 rc=0 cycles all present),
      `check-status-blocks-kept` OK (HEAD's 29 blocks all still present across live+archive).
      Recorded via `bin/checks-due --ran check-doc-size` -> next due 2292.
      **Rates re-measured, as c2244's script explicitly asked the next trim to do rather than
      re-derive:** STATUS.md ~4.7KB/cycle actual (c2244 left 21.5KB; file hit 134.9KB in 24c) --
      the checker's +4510 B/c is accurate for this file, used as-is. queue.md ~3.3KB/cycle
      actual (c2244 left 24.0KB; file hit 101.6KB in 24c) vs the checker's +5440 B/c, i.e. it
      runs ~60% hot here -- third consecutive measurement agreeing on 3.3-3.9KB/c (c2220 ~3.75,
      c2244 ~3.9, c2268 ~3.3). Projections at cycle 2292: STATUS.md 126KB, queue.md ~104KB at
      the measured rate (149KB at the checker's pessimistic one). Kept 6 blocks not 8 in
      STATUS.md because 8 would have left 32.4KB projecting 142.5KB -- only 7KB under the warn
      line, the cycle-1976 mistake c2220 and c2244 both named.
      **(2) All 4 PLAYBOOK QUALITY tools, all clean:** `check-disclosure` 87 site posts + 23
      dev.to articles / 0 missing; `devto-comments` 23 published / 7 with comments / 12 inbound
      / 0 unanswered / 1 spam-skipped; `check-backlinks` 131 post-Actor pairs across 87 posts /
      0 missing / 0 unresolved; `check-actor-guides` 24 live Actors / 0 flagged. No support mail
      to answer.
      **(3) The real finding -- the `users` column is reversible, so the c2168 standing item was
      watching a metric that retracts.** Glanced at `bin/usage-trend` per that item and noticed
      its premise ("trademark-search-scraper is the only Actor off the baseline and the only one
      at 3 users") no longer held: shopify-products-scraper is at 4. Dug the transitions out of
      `state/revenue_history.json` (400 snapshots, ~every 30 min, printing only the snapshots
      where the tuple CHANGES -- collapses 400 records to 7 lines) and found the field is **not
      cumulative and not monotone**: `website-screenshot-scraper` went 1->2->3->1 inside ~36h
      (10-19 23:00 -> 10-21 11:30) and `steam-reviews-scraper` 2->3->1 in 17h (10-22 16:00 ->
      10-23 09:18), i.e. a -2 step. So shopify's 3->4 (10-24 16:03) and trademark's 2->3 (10-23
      09:18) are equally likely to evaporate and neither is evidence of a buyer. Rewrote the
      c2168 open item: it now carries the DECISION RULE only (escalate on a bookmark, a review,
      or `bin/traffic` buyer intent -- never on a run/user climb) plus today's numbers explicitly
      marked re-derive-don't-trust, instead of a named-leader claim with a ~1-day shelf life.
      Wrote the method + the three consequences up in LEARNINGS c2268.
      `bin/traffic` checked in the same pass: 11-24 VERIFIED views/day fleet-wide (raw
      207-440/day is crawler-inflated), 3 verified out_clicks total, top verified paths are blog
      posts and `/tools/<slug>` pages at 5-7 views each -- nowhere near the CLAUDE.md Polar gate
      (>100 verified visits/day to /pricing or /tools), so no owner email, correctly.
      $0 spent (no Actor runs, no builds -- all local/read-only work), 0 new Actors, revenue
      still $0 booked, `bkmk`/`rev` 0 across all 25 Actors, no owner email warranted.
      **Next `varied_test` target when one next comes due: `grants-gov-scraper` (last 2213) --
      but note NOTHING is strictly due until cycle 2549, so the next two cycles should pick up
      queue work rather than force a rotation.**

- [x] **DONE cycle 2267 (NOT a QUALITY slot -- `2267%3==2`, verified via
      `python3 -c "print(2267%3)"`) -- ran the fleet-oldest `varied_test`
      (`app-store-reviews-scraper`, 2212, 55c stale): FIRST-EVER live test of watch-mode
      `scoreChanged` detection on this Actor. 0 defects, clean confirmation, no code change.**
      Re-verified fresh first: `bin/checks-due`/`bin/audit-due --all`/`bin/audit-due --type
      varied_test --all` all NONE DUE, inbox unchanged (same 10 known spam/DMARC/resolved
      items, newest still `c2fa5a9c` -- nothing to answer; also re-checked the old owner
      "Done" identity-verification thread (`dc593cfb`) via `apify-admin list` and confirmed
      `website-screenshot-scraper` is public, fleet at 25 live Actors -- stays resolved),
      services active, site 200 on `/` `/tools` `/pricing`, `HEAD == origin/main` (`43d7b246`)
      and tree clean before edits.
      Grepped all 6 prior `varied_test` notes on this Actor (833/1089/1517/1827/2182/2212) for
      `watchLabel`/`webhookUrl`/"watch mode" -- all scored 0 (c2228 method), so the entire
      watch mechanism (shipped alongside the Actor, never exercised live) was the gap.
      (1) Seed run `{apps:["324684580"], countries:["us"], sort:"mostRecent",
      maxReviewsPerApp:50, maxResults:5, watchLabel:"ast-watch-test1"}` (Spotify) -> HTTP 201,
      `pushed:0`, baseline of 50 reviews recorded in KV store `fetchsmith-app-store-reviews-watch`.
      (2) Reimplemented `watchKeyFor()` in python (sha1 of `JSON.stringify(criteria,
      sortedKeys)`, compact separators) to compute the exact KV key -- matched the live key
      first try (`watch-ast-watch-test1-d31527f929`). Doctored one real review's stored
      `seenMeta` (id `324684580:us:6052627987`, live rating 5) from 5 down to 1 via the
      key-value-store API, simulating a stale baseline predating a rating change. (3) Re-ran
      the identical input -> exactly 1 row: `reviewId:6052627987`, `rating:5` (today's live
      value), `watchEvent:"scoreChanged"`, `previousScore:1` (the doctored value) -- precisely
      correct. Run log status message matched `main.js:1344` verbatim. `chargedEventCounts`
      settled to `{result:1}` == 1 delivered row (polled 6x/60s), 0 leak. Test KV record
      deleted after (204, confirmed 404 on re-GET).
      `check-charges` 25/0, `check-pricing` 25/30/0 both clean (no build, no code touched).
      `audit_dates.json` recorded at 2267 with full note.
      ~$0.0005 spent (1 free seed run, 1 charged test result), 0 new Actors, revenue still $0
      booked, no owner email warranted. **Next `varied_test` target: `grants-gov-scraper`
      (2213, now fleet-oldest by `last`).** Still untested on `app-store-reviews-scraper`
      itself: `webhookUrl` (generic mechanism fleet-verified on `federal-register-scraper` at
      c2265, never on this Actor specifically).

- [x] **DONE cycle 2266 (NOT a QUALITY slot -- `2266%3==1`, verified via
      `python3 -c "print(2266%3)"`) -- ran the fleet-oldest `varied_test`
      (`sam-gov-opportunities-scraper`, 2211, 55c stale): closed TWO gaps at once --
      first-ever test of `wage-determinations-cba` (last of the 3 wd siblings, per c2211's
      own note) AND first-ever test of `watchLabel`/`watchChanges` on this Actor at ANY
      dataType. 0 defects, clean confirmation, no code change.**
      Re-verified fresh first: `bin/checks-due`/`bin/audit-due --all`/`bin/audit-due --type
      varied_test --all` all NONE DUE, inbox unchanged (same 10 known spam/DMARC/resolved
      items, newest still `c2fa5a9c` -- nothing to answer), services active, site 200 on `/`
      `/tools` `/pricing`, `HEAD == origin/main` (`c144868c`) and tree clean before edits.
      Predicted free first via 3 direct `sam.gov/api/prod/sgs/v1/search/?index=wd` calls:
      scanned 200 live CBA rows and found `revisionNumber` can be nonzero even when
      `isActive:true` (`_id` 56262, `cbaNumber` CBA-2013-6079, `revisionNumber` 1) --
      confirming a CBA revision updates the SAME `_id` in place, so `watchChanges`'
      `revisionNumber` detection is genuinely live-exercisable. `keyword:"CBA-2013-6079"`
      isolates exactly that 1 record live.
      (1) Seed run (watchLabel + watchChanges:true) -> `watchSeeding:true`, `baselineSize:1`,
      `pushed:0`, `watchChangeBlindFilters:["isActive"]` (correct, documented default-on
      `activeOnly` blind spot). (2) Reimplemented `watchKeyFor()` in node to compute the exact
      KV key, doctored the live named record (`fetchsmith-samgov-watch`) via the
      key-value-store API -- set the stored revisionNumber from the real 1 down to 0.
      (3) Re-ran identical input -> `watch-incremental`, `pushed:1`, `changedRedelivered:1`,
      `chargedEventCounts` settled `{result:1}`, 1:1 no leak. Dataset row confirmed:
      `revisionNumber:1` (today's live value), `_watchChangeType:["revisionNumber"]`,
      `_watchPrevious:{revisionNumber:0}` -- exactly correct. Test KV record deleted after
      (204, confirmed 404 on re-GET).
      `check-charges` 25/0, `check-pricing` 25/30/0 both clean (no build, no code touched).
      `audit_dates.json` recorded at 2266 with full note.
      ~$0.0003 spent (2 tiny capped live runs, 1 charged result), 0 new Actors, revenue still
      $0 booked, no owner email warranted. **Next `varied_test` target:
      `app-store-reviews-scraper` (2212, now fleet-oldest by `last`).** Still untested on this
      Actor specifically: `webhookUrl` (generic mechanism fleet-verified on
      `federal-register-scraper` at c2265, never on `sam-gov-opportunities-scraper` itself),
      and `organizationId` combined with `assistance-listings`/`exclusions`.

- [x] **DONE cycle 2265 (MANDATED QUALITY/GROWTH slot -- `2265%3==0`, verified via
      `python3 -c "print(2265%3)"`) -- ran both PLAYBOOK QUALITY tools (check-disclosure,
      devto-comments, check-backlinks, check-actor-guides -- all clean, recorded), then the
      fleet-oldest `varied_test` (`federal-register-scraper`, last=2210, 55c stale): FIRST-EVER
      live test of `webhookUrl` across the ENTIRE FLEET (0-count per c2228's LEARNINGS method),
      also the first test combining it with `watchLabel`. 0 defects -- clean confirmation, not a
      bug cycle.**
      Re-verified fresh first: `bin/checks-due`/`bin/audit-due --all`/`bin/audit-due --type
      varied_test --all` all NONE DUE, inbox unchanged (same 10 known spam/DMARC/resolved items,
      newest still `c2fa5a9c` -- nothing to answer), services active, site 200 on `/` `/tools`
      `/pricing`, `HEAD == origin/main` (`f54f0cbd`) and tree clean before edits (aside from the
      routine daily `state/revenue.json`/`revenue_history.json` snapshot).
      **Quality tools:** `check-disclosure` 87 posts + 23 dev.to articles / 0 missing;
      `devto-comments` 23 articles / 12 inbound / 0 unanswered; `check-backlinks` 131 pairs / 0
      missing; `check-actor-guides` 24 live Actors / 0 flagged. No support mail.
      **The varied_test:** created a real public capture endpoint (webhook.site, no account
      needed) and pointed 3 live platform runs at it as `webhookUrl`. (1) Plain search
      (documentTypes:[NOTICE], agencies:[nuclear-regulatory-commission], maxResults:3) -- webhook
      received one POST, 200, payload matched the run exactly (`pushed:3`, `scanned:3`,
      `summary.complete:false`, `incompleteReason:'max-results'`, correct). (2) Watch SEED (same
      filters, `watchLabel`) -- payload `watchSeeding:true`, `watchNewCount:null`,
      `baselineSize:102`, `pushed:0`, correct. (3) Watch INCREMENTAL after doctoring one id
      (`2026-21781`) out of the live KV baseline via the API (c2210's technique) -- payload
      `watchSeeding:false`, `watchNewCount:1`, `skippedSeen:101`, and the delivered dataset row's
      `documentNumber` matched the doctored-out id exactly. All 3 confirmed independently via the
      run log's own `Posted completion summary to webhookUrl (200)` line. **0 defects** -- the
      mechanism works exactly as coded on both plain search and watch seed/incremental. Test KV
      record deleted after (204, confirmed 404 on re-GET). No code/README change (nothing to fix).
      `check-charges` 25/0, `check-pricing` 25/30/0 drift, both clean.
      **Side-finding, not a bug:** `chargedEventCounts` via `GET /v2/actor-runs/<id>` lagged the
      real charge by far longer than previously seen -- still `{result:0}` ~47s after `SUCCEEDED`
      on the 1-row incremental run, well past c2210's ~15s. Verified the charge had actually
      happened via the run log instead (`pushResult()` only calls `Actor.pushData` after
      `Actor.charge(...).chargedCount > 0`, so a logged "Pushed N documents" **is** proof of
      charge) -- recorded as a LEARNINGS method note so a future cycle doesn't misread a slow
      summary field as a leak.
      `audit_dates.json` recorded (`federal-register-scraper.varied_test` -> 2265, full note).
      ~$0.001 spent (3 small live runs), 0 new Actors, revenue still $0 booked, no owner email
      warranted. **Next `varied_test` target: `sam-gov-opportunities-scraper` (2211, now
      fleet-oldest by `last`).**

- [x] **DONE cycle 2264 (NOT a QUALITY slot -- `2264%3==2`, verified via
      `python3 -c "print(2264%3)"`) -- ran the fleet-oldest `varied_test` (`shopify-products-scraper`,
      2209, 55c stale): FIRST-EVER live test of `detailLevel:"full"` and of the `productDetail`
      charge event, and it found and fixed a real ordering defect. Build 0.1.102 live and
      byte-verified.**
      Re-verified fresh first: `bin/checks-due`/`bin/audit-due --all` both NONE DUE, inbox unchanged
      (same 10 known spam/DMARC/resolved items, newest `c2fa5a9c` -- nothing to answer), services
      active, site 200 everywhere, `HEAD == origin/main` (`40947236`) and tree clean before edits.
      **The live test:** every prior `varied_test` here ran basic detail (c2209/c2180/c2162 all
      recorded `productDetail:0`), so the second charge event had never run on the platform.
      Predicted free first (c1514 technique) from `allbirds.com/products.json?limit=5` + each
      handle's `.js` route -> tracked-variant roll-up 8/169/210/160/61. Live run
      (`detailLevel:full`, `maxProductsPerStore:5`, `maxResults:5`) -> 5/5 rows, `totalInventory`
      matched all five predictions exactly, every variant carried barcode/inventoryQuantity/
      inventoryManagement/inventoryTracked/inventoryPolicy, `quantityRule` correctly `null` on
      Shopify's universal default (README claim verified live for the first time), and
      `chargedEventCounts` (via `GET /v2/actor-runs/<runId>`, not the runs-LIST endpoint) was
      `{result:5, productDetail:5}` -- one detail charge per enriched product, 0 leak.
      **The bug:** `enrichWithDetail`'s `available`-resolution block (fills a null `available`/
      `availableVariantCount`/per-variant `available` from the `.js` route's own flags) sat AFTER
      the `nothing found, nothing charged` early return, so the case the README FAQ promises it for
      skipped it: a store publishing no stock data at all (verified free on brooklinen.com -- its
      `.js` route returns inventory_management/policy/quantity ALL null, so `hasInventoryData` is
      false for every variant) whose product page also yielded nothing (bot-blocked -> no `<title>`,
      no meta description, no rating) shipped `available: null` while the `.js` response in hand had
      the answer. Not a charge bug either direction -- a data gap against a stated promise.
      Proved $0 with a pure extraction of the function tail (`/tmp/prove_avail_order.js`): pre-fix
      `charged=0 available=null`, post-fix `charged=0 available=true availableVariantCount=1`;
      both other paths (seo-found, base-route-already-shipped-available) identical pre/post.
      **Fix:** hoisted the fill above both gates (it is a BASE field and costs no request of its
      own), charge rule untouched. Live post-fix regression on the deployed build: 2/2 rows, detail
      fields intact, `{result:2, productDetail:2}`. Build 0.1.102 (package 0.1.17 -> 0.1.18), live
      source byte-identical (76801==76801, sha `257dd1b8`). README needed no change (the FAQ claim
      is now unconditionally true). `check-charges` 25/0, `check-pricing` 25/30/0, `node --check`
      clean. `audit_dates.json` recorded at 2264 with full note.
      ~$0.006 spent (1 push + 3 small live runs), 0 new Actors, revenue still $0 booked, no owner
      email warranted. **Next `varied_test` target: `federal-register-scraper` (2210, now
      fleet-oldest by `last`).**

- [x] **DONE cycle 2263 (NOT a QUALITY slot -- `2263%3==1`, verified via
      `python3 -c "print(2263%3)"`) -- ran the fleet-oldest `varied_test` (`fec-campaign-finance-scraper`,
      2208, 55c stale) and it found and fixed a real disclosure bug. Build 0.1.79 live and byte-verified.**
      Re-verified fresh first: `bin/checks-due`/`bin/audit-due --all` both NONE DUE, inbox unchanged
      (10 known spam/DMARC/resolved items, incl. the old owner "Done" verification thread -- already
      acted on, nothing to answer), services active, site 200 everywhere, `HEAD == origin/main`
      (`f59aedff`) and tree clean before edits.
      **The bug:** the incremental watch-mode status message's `pushed === 0` branch fired
      unconditionally, so a run that stopped early (`chargeLimitReached`/`timeBudgetHit`/
      `watchPageCapHit`) before delivering anything told the buyer "every matching contribution had
      already been delivered ... that is the expected result most of the time" -- false confidence
      when the scan genuinely hadn't finished and a real new row could exist past the stopping point.
      Proved via an extracted branch-selection snippet (pure control-flow, $0, no network needed):
      pre-fix code picks the misleading message for `{pushed:0, complete:false,
      incompleteReason:"charge-limit"}`. **Fix:** split on `complete` -- `pushed===0 && complete`
      keeps the old message; `pushed===0` alone (incomplete) gets a new one naming
      incompleteReason/incompleteDetail and stating "this is NOT a confirmed 'nothing new'". Re-ran
      the extraction post-fix on all 3 cases (charge-limit-incomplete, genuine-quiet,
      normal-delivery) -- correct, no regression.
      **Live check:** seeded a real 3-row watch baseline (contributions, donorEmployer=GOOGLE,
      state=AK, electionYear=2026), doctored one id out of the named KV record via the API, reran
      with a tiny `maxTotalChargeUsd` -- confirmed the general chargeLimitReached -> "Scan
      INCOMPLETE" path fires correctly. Could NOT isolate the exact `pushed===0` edge live:
      `maxTotalChargeUsd` on the runs API (query param and JSON body, both tried) was silently
      ignored (`isMaxTotalChargeUsdSetByUser` stayed `false`), so the existing row got charged
      before a limit could block it. Logged in LEARNINGS -- do not re-try the same two shapes; check
      whether an Actor Task or the Console UI's limit field is needed instead, if a future cycle
      wants to force `chargedCount:0` on the very first charge of a run. Test KV record deleted
      after. Build 0.1.79 (package 0.1.24 -> 0.1.25), live source byte-identical. README needed no
      change. `check-charges` 25/0, `check-pricing` 25/30/0, `node --check` clean. `audit_dates.json`
      recorded at 2263 with full note.
      ~$0.0015 spent (one build + two tiny live runs, 1 charged test result), 0 new Actors, revenue
      still $0 booked, no owner email warranted. One commit (`8b4f19e9`) pushed to `origin/main`.
      **Next `varied_test` target: `shopify-products-scraper` (2209, now fleet-oldest).**

- [x] **DONE cycle 2262 (MANDATED QUALITY/GROWTH slot -- `2262%3==0`, verified via
      `python3 -c "print(2262%3)"`) -- ran both PLAYBOOK QUALITY tools (both clean, recorded),
      then the fleet-oldest `varied_test` (`google-play-reviews-scraper`, 55c stale), which
      FOUND AND FIXED a real disclosure bug. Build 0.1.91 live and byte-verified.**
      Re-verified fresh first: `bin/checks-due`/`bin/audit-due --all` both NONE DUE, inbox
      unchanged (10 known spam/DMARC/resolved items), services active, site 200 everywhere,
      `HEAD == origin/main` (`52500008`) and tree clean before edits.
      `check-disclosure` 87 posts + 23 dev.to articles / 0 missing (recorded, next due 2310);
      `devto-comments` 23 articles / 12 inbound / 0 unanswered (recorded, next due 2406). No
      support mail. dev.to cadence checked live: most recent post 2.2 days old, within cadence.
      **The bug:** in watch mode, the per-app app-details snapshot is pushed and counted in
      `pushed` like a review row, but the status message and `webhookUrl` payload both derived
      "new reviews" as `pushed - watchChanged` -- silently counting that app-detail row as a
      phantom "new review" whenever `includeAppDetails` (default **true**) was combined with
      `watchLabel` and any app had a delivery. First-ever test of this exact combination.
      Reproduced for $0 locally (real Spotify reviews via `CRAWLEE_STORAGE_DIR`): doctored the
      stored watch record (remove-a-reviewId for a "new" case, edit-a-score for a "changed"
      case, same KV method as c2207) to deterministically prove pre-fix overcounts: 2 reported
      as "new" when only 1 (or 0) really were. **Fix:** added `watchNewDelivered`, incremented
      only when a genuinely new review row is pushed (never for the app record or a changed
      row), and swapped both reporting paths to read it directly. Proved 3 paths for $0: new+
      app-record (now correct), changed+app-record (now correct), no-app-record (unaffected,
      regression-safe). README needed no change (names the field, makes no formula claim).
      Build 0.1.91 (0.1.28 -> 0.1.29), live source byte-identical (51493==51493). **Then
      reproduced the exact scenario on the REAL PLATFORM**, not just locally: seeded a live
      watch baseline, doctored the live named KV record via the API, reran -- log correctly
      said "1 new review(s)" for `pushed=2`, `chargedEventCounts {result:2}` matched exactly
      (checked twice, no charge leak -- disclosure bug only). Test KV record deleted after.
      `check-charges` 25/0, `check-pricing` 25/30/0, `node --check` clean. `audit_dates.json`
      recorded at 2262 with full note.
      ~$0.0004 spent (one build + two tiny capped live runs), 0 new Actors, revenue still $0
      booked, no owner email warranted. One commit (`8166d520`) pushed to `origin/main`.
      **Next `varied_test` target: `fec-campaign-finance-scraper` (2208, now fleet-oldest).**

- [ ] **NEW follow-up (c2260) -- consider a checker for the same number stated twice with two
      different values.** Concretely: parse numeric claims out of each Actor's
      `.actor/input_schema.json` descriptions and its `README.md` and flag any claim that
      appears in both with disagreeing values. Motivating incident is in the c2260 entry above:
      c822 live-corrected "max seen: 110 sites" to 1,089 in the schema and left 110 in the
      README for ~1,438 cycles. `bin/check-meta-fields` is the nearest existing tool but only
      covers "N fields" counts. Scope it narrowly first (same unit word within N tokens, e.g.
      "sites", "fields", "studies") and measure the false-positive rate on the fleet BEFORE
      registering it in `state/fleet_checks.json` -- a noisy checker is worse than none.

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

