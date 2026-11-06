- [x] **DONE c2818 (Regular slot, 2818 % 3 == 1) -- `federal-register-scraper`'s 9th
      `competitor_audit` (2481 -> 2818, 337c gap), one of 2 real backlog items `audit-due --all`
      found fleet-wide (the other, `sam-gov-opportunities-scraper`, left for the next Regular
      slot).** Preflight: `checks-due --all` NONE DUE (soonest `check-row-floor` c2820),
      `inbox-triage new` NONE UNTRIAGED of 74, `bin/revenue` $0 booked / 27 Actors / 50 users /
      804 runs30d, services + all 4 pages 200. **Fixed `bin/_batch_price_fedreg.py`'s c2796
      argv-default trap (hardcoded `/tmp` paths, no override, no `persist_sweep`) -- replaced by
      `bin/_batch_price_fedreg2.py` on the `_batch_price_apc2.py` pattern (6th pricer in 8 audits
      with both defects).** Fresh niche-size/niche-unnamed: niche grew **165 -> 180** matched
      (2543 -> 3121 seen), **121** unnamed (**110** NONE + 11 OWNER, up from 108/96+12). All 110
      NONE handles live-priced, **110==110** cross-check against `niche-unnamed`'s own count, 0
      unresolvable; all 11 OWNER handles also re-priced live under their own handles per the
      c2475 lesson -- 0 in scope and cheaper (`malonestar`'s 4 EPA/FWS screeners and
      `nexgenwatch`'s 2 MCP servers are single-vertical US-regulatory tools, not Federal Register
      products; `jungle_synthesizer/bravsearch-brak-de-lawyer-register-scraper` is a German
      lawyer registry). Own price re-verified live first: unchanged, flat $0.0008/result, no
      start fee. **3 new disclosures:** `datalantern/federal-register-search` (2u, flat
      $0.0005/record + $0.00005 start -- cheaper than us at every volume, FederalRegister.gov
      metadata search only), `insight.solutions/federal-register-api` (2u, tiered
      $0.0004->$0.00024 + $0.001 start -- every tier below our floor past ~2-3 rows, same
      no-API-key scope as us incl. Public Inspection), `pandadad0214/federal-register-monitor`
      (2u, tiered $0.001->$0.0007 + $0.00005 start -- dearer Free/Bronze, ties Silver, cheaper
      Gold+, same partial-undercutter shape as `scrapesage`/`hipersoft`/`conserving_celerytop`/
      `tidyharvest` already named above it). `resourceful_playbook/au-legislation-search` (2u,
      AMBIGUOUS unit_price -- 2 recurring events, no primary flag) ruled out on **scope**, not
      price: Australian federal legislation, not the US Federal Register -- the ambiguity never
      needed resolving. **PRICING DECISION: HOLD $0.0008** -- all 3 new undercutters sit at 2
      users, far under the 20-user re-price threshold, and the niche already discloses cheaper/
      free rivals from earlier passes. Shipped README-only build (package 0.1.18 -> 0.1.19, 2
      builds -- the first push's new paragraph tripped `check-competitor-claims`'s UNDATED check
      since "re-verified live first" has no ISO date within 40 chars of "verified"; fixed to
      "re-verified 2026-11-06" and re-pushed, build 0.1.68); live README verified byte-identical
      (50,209 bytes both sides) via `versions/0.1 sourceFiles`. Guards after: `check-price-
      superiority` 2632 named-rival prices / 993 cheaper / 0 undisclosed anywhere; `check-charges`
      27/0/0; `check-registry-fields` 0 drift; `check-own-price-prose` 27/0; `check-competitor-
      claims --only` 0 stale / 0 undated on this file. Rotation recorded in `state/
      audit_dates.json` (persisted sweep at `state/audit_data/c2818_fedreg_prices.json`),
      `audit-due --type competitor_audit` now shows only `sam-gov-opportunities-scraper` DUE.
      Spend ~$0.01 this cycle (2 builds, ~130 read-only API fetches, no platform runs). No owner
      email warranted ($0 booked, nothing only they can fix).

- [x] **DONE c2817 (QUALITY slot, 2817 % 3 == 0) -- trimmed `notes/LEARNINGS.md` (TRIM DUE,
      7613 -> 5237 lines), not `state/STATUS.md` as c2816 had claimed.** Preflight:
      `checks-due --all` NONE DUE, `audit-due --all` 1 real item (`federal-register-scraper`
      `competitor_audit`, left for the next Regular slot per standing precedent), `inbox-triage
      new` NONE UNTRIAGED of 74 (re-read the two owner threads visible in raw `inbox list` --
      CourtListener token, Apify Store Nov-15 notice -- both already resolved in prior cycles).
      `bin/revenue` $0 booked / 27 Actors / 50 users / 801 runs30d, services + all 4 pages 200.
      **Re-ran `check-doc-size` fresh instead of trusting c2816's note, and the note was wrong:**
      `state/STATUS.md` read **OK** (57.8KB, already trimmed at c2808, 9 cycles before c2816
      wrote "still TRIM SOON"), while `notes/LEARNINGS.md` was the one at **TRIM DUE** (7613/8000
      lines, projected 8093 past the checker's own next look). Per the doc-trim cadence item's
      standing rule, DUE outranks SOON. Full details of the trim (method, hazard grep, exact
      line ranges, verification) are in the `doc-trim cadence` item's `EXECUTED c2817` record
      below; this entry is the top-of-queue pointer. Also updated that item's execution record
      in place (superseded `EXECUTED c2808`/`DONE c2811`/`c2813 flag` text archived verbatim to
      `queue_archive.md` under a c2817 header, per the item's own "newest execution only" rule).
      No code changed, no build pushed. `tasks/queue.md` itself is still TRIM SOON (105.0KB) --
      candidate DONE blocks for the next QUALITY slot's cut are named in the doc-trim item.

- [x] **DONE c2816 (Regular slot, 2816 % 3 == 2) -- `apple-podcasts-scraper`'s `competitor_audit`
      (2480 -> 2816, 336c gap), the only real backlog item `audit-due --all` found fleet-wide across
      all 16 types. Preflight: `checks-due --all` NONE DUE (soonest `check-row-floor` c2820),
      `inbox-triage new` NONE UNTRIAGED of 74, `bin/revenue` $0 booked / 27 Actors / 50 users / 801
      runs30d, services + all 4 pages 200. Spend $7.3724/$85, ~$0.01 this cycle (1 build + ~100
      read-only fetches, no platform runs). No owner email (no revenue event, nothing only they can fix).**
      **FIRST MOVE per the c2812 note, and it paid again:** `bin/_batch_price_apc.py` (c1339) carried
      the c2796 trap in its WORST form -- both input and output paths hardcoded with **no argv at
      all**, and c2480's 18-handle input file was still on disk (630 B, Oct 30), so a bare re-run
      would have re-priced a 336-cycle-old cohort behind a normal banner. No `persist_sweep` either.
      Replaced by **`bin/_batch_price_apc2.py`** on the `_batch_price_fda2.py` pattern (both paths
      required args -- bare run exits 1, verified; prints its cohort size for the mandatory
      `niche-unnamed` cross-check; re-reads our own live price first; persists to
      `state/audit_data/`). **Base rate for "pricer carries both defects" is now 5-for-6 audits.**
      Own price re-verified live FIRST: flat $0.001/`result`, no start fee, no rungs, unchanged since
      2026-09-10. niche-size **1102 seen / 192 matched** (up from 1011/166); niche-unnamed **31
      unnamed of 192** (26 NONE, 5 OWNER incl. our self-listing); all 30 non-self handles live-priced,
      **30==30** cross-check, 0 unresolvable, 1 AMBIGUOUS hand-read. **c2812 sign check: matched +26
      and cohort +12 move the SAME way, no screen decay** (and this niche has had no user-count cut
      since c2121 anyway). **13 new disclosures shipped:** 2 every-tier undercutters
      (`thequietstack/apple-podcasts-reviews-charts` 2u -- cheaper at every tier on BOTH row events,
      review $0.0003->$0.00021 and podcast $0.0005->$0.00035, and the closest whole-product match
      we have seen in this niche; `lepone31/apple-podcasts-intelligence` 2u, `pricingInfos` null and
      no scheduled future price = genuinely $0), 1 Bronze-up crossover (`martin10291`), 4 split-event
      partials (`agentsgearbox` cheaper at every tier on episodes AND reviews while dearer at every
      tier on podcast rows; `fabrikit`, `rsiddiq95`, `tacps126`), 2 exact ties ruled NOT undercutters
      (both add a $0.00005 start fee we do not), 4 in-scope dearer. Remaining 17 are the niche's two
      standing exclusions (11 transcription, 6 lead-gen), every one dearer on any unit.
      **The methodological finding: the cross-sweep diff said ZERO of c2480's 18 handles survive --
      a 100% turnover reading -- and it is entirely our own disclosure, not churn.** `grep` showed
      all 18 are now NAMED in our README, which is precisely the `niche-unnamed` exclusion rule, so
      the "gone" set was manufactured by our own last audit. Re-fetched c2480's 5 disclosed
      undercutters anyway (c2796 rule 3): **5/5 live, public, non-deprecated, byte-identical prices
      336 cycles later** -- fleet running total now **55 of 57 re-fetches have falsified a churn
      reading**. Shipped build 0.1.118 (package 0.1.37->38), live README verified byte-identical via
      `versions/sourceFiles` (71,917 B, md5 `5e9e1e8a...`). Guards after: fleet
      `check-price-superiority` 2627 named-rival prices / 991 cheaper / **0 undisclosed anywhere**
      incl. all 13 new ones; `check-competitor-claims --only` 72 claims / 0 stale / 0 unresolvable +
      14 paragraphs / 0 undated; `check-own-price-freshness` 27/0; `check-own-price-prose` 27/0.
      HOLD $0.001/result -- every undercutter sits at 1-2 users.

- [ ] **NEW follow-up (c2816, MEDIUM -- a real SILENT fleet-wide gap in our own guards, found by
      hand; do NOT bolt it on under time pressure, it needs a before/after baseline diff).**
      **A rival named in a README with a published PRICE but NO user count is never
      liveness-checked by anything we own.** `check-competitor-claims` only resolves handles that
      carry an `Nu`/`N users` claim (that is what its `claimed`/`live_users` loop iterates), and
      `check-price-superiority` *explicitly defers to it* for dead handles -- `bin/check-price-superiority:407`
      is literally `continue  # gone from Store -- check-competitor-claims already flags this`,
      which is FALSE for any count-less mention. So such a listing can 404 and we keep publishing
      its price forever. **Confirmed live, twice, in one file this cycle:** both
      `wearefluent/podcast-transcripts` and `wearefluent/podcast-episodes-scraper` are 404 while
      `apple-podcasts-scraper`'s README published their prices, and `check-competitor-claims --only`
      read **0 stale / 0 unresolvable** on that file both before and after. Found only because this
      audit hand-probed all 10 named rivals. **Cheapest fix: `check-price-superiority` already
      fetches every named rival, so have it print a `GONE <file>:<line> <handle>` line (and count
      it) instead of silently `continue`-ing** -- no new network at all. Scope it as advisory-only
      first and diff `compared`/`cheaper`/`flagged` against the 2627/991/0 baseline recorded above
      before trusting the run. Likely several more cases fleet-wide: 122 other README files have
      never had a count-less named rival checked for liveness.

- [ ] **NEW note (c2816, TRIVIAL -- cleanup, delete-not-patch).** `bin/_batch_price_apc.py` (c1339)
      is now orphaned by `_batch_price_apc2.py` -- nothing calls it and it is one of the stalest
      copies in the `_batch_price_*` family (no argv, no `persist_sweep`, no `_unit_price`). Same
      shape as the orphaned `_batch_price_ggs.py` c2806 flagged. **Do not patch either; delete them
      when a cycle next touches this family**, and when you do, re-check `bin/_unit_price_selftest.py`
      first -- it replays saved `/tmp/*_prices.json` cohorts and may name a script by path.

- [ ] **NEW watch (c2816, LOW -- re-read at the next `apple-podcasts-scraper` audit, due ~c3152;
      no action today).** `thequietstack/apple-podcasts-reviews-charts` (2u) is the **first rival in
      this niche that undercuts us at every tier on every row event while selling our exact feature
      shape** (reviews + charts + search). Every previous every-tier undercutter here was a
      single-unit episode/show specialist, which is why the standing answer has been HOLD. The
      c2816 hold still stands on traction (2 users, and the niche's heads -- `ryanclinton` 217u,
      `automation-lab` 124u, `sourabhbgp` 77u -- do not compete on price), **but the hold's reasoning
      is now "no traction", not "no comparable product".** If this listing clears the 1-2-user floor
      by the next audit, that is the first genuine price pressure this niche has produced; price the
      decision then against the full cohort, not against this one listing (the c2692
      `grants-gov-scraper` rule).

- [ ] **NEW note (c2816, TRIVIAL -- saves the next audit a wrong conclusion about a checker).**
      `check-competitor-claims` carries `USER_TOLERANCE = 0.10`, so a count claim inside 10% of live
      is deliberately NOT stale. This cycle's live re-reads (`ryanclinton` 207->217, `sourabhbgp`
      71->77, `tidydata/audio-video-transcription` 20->22) are all inside that band, so its
      `0 stale` was **correct, not a blind spot** -- do not file it as one. Separately: those counts
      were NOT blind-swapped into c2480's dated paragraph, whose conclusion is "did not move"
      (the c2804 falsified-not-stale shape); the fresh numbers and the refined conclusion went in
      the new c2816 block instead.

- [x] **DONE c2813 (Regular slot, 2813 % 3 == 2) -- `sec-insider-trades-scraper`'s 8th
      `competitor_audit` (2476 -> 2813, 337c gap), the only real backlog item `audit-due --all`
      found. Preflight: `checks-due --all` NONE DUE, `inbox-triage new` NONE UNTRIAGED of 74,
      `bin/revenue` $0 booked / 27 Actors / 50 users / 801 runs30d, services + all 4 pages 200.**
      **Checked the c2812 standing rule (compare matched-listings delta vs screened-cohort delta
      before trusting a cut) and it was MOOT here, not a new finding:** this niche has run a
      full-cohort rule (price every unnamed listing regardless of user count) since cycle 1336,
      never a `>=3u` cut, so the windowing blind spot c2812 found on `fda-recall-scraper` was
      never structurally possible on this Actor. niche-size 725 seen / 175 matched (up from
      640/160). niche-unnamed 89 unnamed (86 NONE + 3 OWNER, one being our own listing on title
      overlap). Own price re-verified live first: flat $0.0018/result, unchanged since cycle 810.
      **Fixed `bin/_batch_price_sit.py`'s c2796 argv-default trap (hardcoded `/tmp` paths, no
      override) and missing `persist_sweep` call -- the FOURTH pricer in five audits with both
      defects (ggs c2806, ted c2810, fda c2812, sit c2813), now a 4-for-4 base rate.** Live-priced
      all 86 NONE handles (86==86 cross-check): **79 dearer at every tier, 6 cheaper at every
      tier/headline, 1 genuinely free** (`pintostudio/sec-filings-api`, `pricingInfos` null, no
      scheduled future price) -- all 7 at 2 users. **6 new unit-matched undercutters disclosed**:
      `automation_craft/sec-form-4-insider-trading-scraper` (tiered $0.0004->$0.00038, 78-79%
      cheaper, deepest yet in this niche), `plotpointtech/sec-edgar-filings-insider-trades`
      (tiered $0.0005->$0.00031, 72-83% cheaper -- same owner already flagged as a persistent
      every-rung undercutter on `hacker-news-scraper` c2804), `pushbuild/sec-insider-trades`
      (flat $0.0008, 56% cheaper), `yakeddgraph/sec-edgar-filings-scraper` (flat $0.001, 44%
      cheaper), `mossgreen_zed/sec-insider-trading-form4` (flat $0.0015, 17% cheaper),
      `h1018y/anvil-sec-edgar-all` (tiered $0.0017->$0.00119, 6-34% cheaper). 2 OWNER-bucket
      candidates re-verified live under their own handles and ruled out dearer:
      `automatic/sec-insider-trades` ($0.002/row+$0.005 start) and
      `gochujang/insider-trading-monitor` ($0.01/filing-processed+$0.005 start).
      **PRICING DECISION: HOLD $0.0018** -- all 6 new undercutters sit at 2 users, far under the
      20-user re-price threshold, and the niche already discloses cheaper/free rivals from
      earlier sweeps, so a cut would not make us cheapest either. **Also closed this Actor's 3
      claims in the c2809 guarded-stale-claims backlog as a side effect of the same live-read**
      (`constant_quadruped` 101->117u/17->19 new-in-30d, `constructive_calm` 66->75u, `v0iddo`
      1->2u -- no superlative depended on the swapped numbers). Build 0.1.73 pushed (package
      0.1.26->0.1.27), live README verified byte-identical (75,833 bytes both sides). Guards:
      `check-price-superiority` 2590 named rivals / 982 cheaper / 0 undisclosed anywhere;
      `check-competitor-claims --only` 0 stale on this file. Rotation recorded in
      `state/audit_dates.json`, `audit-due --all` now reads NONE DUE fleet-wide (soonest
      `apple-podcasts-scraper` in 3c). Spend $7.2927/$85, ~$0.008 this cycle (1 build, ~95
      read-only API calls, no platform runs).

- [x] **DONE c2815 (Regular slot, 2815 % 3 == 1) -- FIX FAILED ACTORS (nightly health
      2026-11-06): `uk-find-a-tender-scraper`. It was NOT a flaky blip -- a real starvation
      bug in our own code.** Preflight: `checks-due --all` NONE DUE, `audit-due --all` NONE
      DUE fleet-wide (16 types), `inbox-triage new` NONE UNTRIAGED of 74, `bin/revenue` $0 /
      27 Actors / 50 users / 801 runs30d. The run's `RUN_SUMMARY` said BOTH sources failed
      `run-timeout budget exceeded` at **0 pages each** -- suspicious, since a dead portal
      reports its own HTTP code, not the clock. Upstream probes per the c2679 rule: **Find a
      Tender 500 after 52.9s, Contracts Finder 200 in 0.62s with real data** -- half the
      product healthy, run still delivered 0 rows. **Mechanism:** the run budget is SHARED,
      `fetchPage` retries a sick source 4x at a 45s request timeout, so FTS burned all 135s
      usable (180s `timeoutSecs` - 45s margin; run ended 167.3s) and CF was never asked a
      single request. **Fix, build 0.1.100 (pkg 0.1.22->0.1.23):** `SIBLING_RESERVE_MS=30_000`
      + `fetchBudgetMs()` + `setSiblingReserve()` -- hold back a reserve for each sibling with
      `pages === 0`, capped at half the remaining budget, applied in `fetchPage`'s loop guard
      and both retry sleeps. Slice stops set a per-source `sliceExceeded` (NOT the global
      `timeBudgetExceeded`, which drives the run-wide summary) with a new honest
      `incompleteReason: "source-time-share"` arm and a `RUN_SUMMARY.sources[].sliceExceeded`
      field. **Verified 3 ways:** happy path live (FTS 5 / CF 5, round-robin intact); the
      starvation condition FORCED via a throwaway `src/_tmp_starve_test.js` with FTS pointed
      at `10.255.255.1` and a real `ACTOR_TIMEOUT_AT` (c2569 trick) -- **CF delivered 10 rows
      where the shipped code delivered 0**, test copy deleted; and `actor-health --only` on
      the platform post-build (`ok: True, items: 10, fail_rows: 0`).

- [ ] **NEW WATCH (c2815, LOW -- upstream, NOT our bug, do not open a task on it).** Find a
      Tender (`www.find-tender.service.gov.uk/api/1.0/ocdsReleasePackages`) is
      **intermittently** degraded, not down: a `?limit=5` probe returned **HTTP 500 after
      52.9s** while the Actor's own real query (`limit=100&updatedFrom=...&stages=tender`)
      answered in under a second on the very next attempt, twice. The c2815 starvation fix
      means an FTS slow spell now costs only FTS's rows, not the whole run, so this is
      survivable and needs no action. **Only escalate if `uk-find-a-tender-scraper` shows
      `sliceExceeded: true` on `fts` across several consecutive nightly runs** -- that would
      mean FTS is persistently (not intermittently) too slow to page inside a 180s run, and
      the answer then is a README note telling buyers to raise the run timeout or use
      `sources:["fts"]` alone, NOT another code change. Check with the RUN_SUMMARY field, not
      by re-probing by hand.

- [ ] **NEW follow-up (c2815, MEDIUM -- same bug shape, other Actors, bias is "runs return
      fewer rows than they should", never overbilling).** The starvation bug is NOT
      specific to this Actor: it exists in any fleet Actor that walks **multiple upstream
      sources against one shared run-timeout budget** with per-request timeouts large enough
      that one sick source can spend the lot. `uk-find-a-tender-scraper` is now fixed; the
      obvious candidates to read next are `ats-jobs-scraper` (7 boards -- LEARNINGS c2569
      already records it genuinely running out of budget after 2 of 7 sources, which is the
      SAME shape and was then treated as correct behaviour) and `remote-jobs-scraper`.
      **Method that worked, reuse it:** grep the Actor for its source/cursor loop, check
      whether the time-budget guard is global or per-source, then force the condition with a
      throwaway copy of `src/main.js` pointing ONE source at `10.255.255.1` and a real
      `ACTOR_TIMEOUT_AT` -- do not reason about it statically, and delete the copy after.
      Do NOT batch-fix: one Actor per cycle, each with its own forced-starvation test.
- [x] **DONE c2812 (Regular slot, 2812 % 3 == 1) -- `fda-recall-scraper`'s 6th
      `competitor_audit` (2475 -> 2812, 337c gap), the backlog item c2811 deferred to this
      slot. Preflight: `checks-due --all` NONE DUE (soonest `check-row-floor` c2820),
      `audit-due --all` 2 real items (`fda-recall-scraper`, `sec-insider-trades-scraper`),
      `inbox-triage new` NONE UNTRIAGED of 74, `bin/revenue` $0 booked / 27 Actors / 50
      users / 801 runs30d, services + `/`,`/pricing`,`/tools`,`/blog` all 200.**
      **THE FINDING -- the `>=3-user` floor every prior sweep on this Actor used had gone
      blind, and the narrow cut would have published a false all-clear.** Niche GREW 556 ->
      607 matched (936 seen, 502 unnamed) while the never-named `>=3u` cohort FELL 14 -> 2,
      both out of scope. Widened to all **328** `>=2u` never-named listings, live-priced
      every one: **143 below our $0.0024 floor, 42 after the agency/country/endpoint title
      screen, 39 undercutting at every tier**, modal flat $0.001-$0.002/record. 5
      re-verified individually (public / not deprecated / no future repricing /
      `all_events_all_tiers` per c2792): `cliqtomedia/fda-recalls-enforcement-monitor`
      ($0.0001 -> $0.00007 + $0.002 start -- deepest in-scope undercut on file here, near
      filter parity), `tali-works/openfda-recall-monitor` ($0.0005 + $0.00005),
      `br_data_hub/fda-recalls-monitor` ($0.001 -> $0.0007 + $0.00005, closest shape match
      to our ladder), `apex-nexus/fda-recall-delta-monitor` (Apify FREE $0/row, delta-only
      scope), `rbbscrap/fast-openfda-scraper` ($0.0013 -> $0.0009, drug-only + FAERS).
      **DECISION: HOLD $0.0035 -> $0.0024** -- all 42 carry 2 users, far under the 20-user
      re-price threshold, and free / $0.00001-row rivals are already named on the page.
      Fixed `bin/_batch_price_fda2.py` (c2796 argv-default trap + missing `persist_sweep`).
      Build 0.1.89 SUCCEEDED (pkg 0.1.34 -> 0.1.35, README-only), live README verified
      byte-identical via the build API (86,431 both sides). Guards: `check-price-superiority`
      2581 named / 975 cheaper / **0 undisclosed anywhere**, `check-charges` 27/0/0,
      `check-registry-fields` 0 drift. Sweep kept at
      `state/audit_data/c2812_fda_prices.json`. One dated README paragraph added.

- [x] **DONE c2814 (QUALITY slot, 2814 % 3 == 0) -- closed the c2812 upper-bound follow-up:
      `fda-recall-scraper`'s "39 every-tier undercutters among 42 screened listings" was a
      published upper bound (only 5 of 42 individually scope-verified); now fully resolved.**
      Preflight: `checks-due --all` NONE DUE, `audit-due --all` NONE DUE (0 real backlog
      items fleet-wide), `inbox-triage new` NONE UNTRIAGED of 74, `bin/revenue` $0 booked /
      27 Actors / 50 users / 801 runs30d, services + all 4 pages 200, spend $7.32/$85 (cycle
      projection $7.92). With nothing due, used the QUALITY slot on this backlog item per the
      `notes/PLAYBOOK.md` cadence.
      **Used the existing `state/audit_data/c2812_fda_prices.json` cohort (328 listings) --
      no re-sweep, no new API calls for the pricing data.** Individually scope-checked all
      143 below-floor listings by title + description against the page's own scope test (US
      openFDA enforcement data -- food/drug/device recall records; not adverse events/FAERS,
      labels, UDI, NDC, Drugs@FDA/approvals, drug shortages, 510(k), clinical trials, another
      agency (CPSC/NHTSA/FSIS/CFPB), another country). **Verified count: 30 in-scope (not
      42), 27 every-tier undercutters (not 39).** The known partials from the c2812 note
      (`rbbscrap`, `apex-nexus/fda-recall-delta-monitor`, `smilemask/fda-medical-device-
      recalls`, `soilair/openfda-device-enforcement-status-watch-api`, `flamelit_arowana`)
      stayed in with their caveats unchanged; `thescrapelab` and `thriftykiwi/nz-food-
      recalls-scraper` stayed out (foreign-only, as already documented). **12 dropped from
      the original 42 title-screen pass**, found on full description review: 9 are
      multi-dataset openFDA wrappers where recalls is one of several equal-billed datasets
      rather than the product's focus (`pushbuild/openfda`, `bepolabs/openfda`,
      `j0401/openfda-compliance`, `grit-77/openfda`, `deanko/openfda-scraper`,
      `conserving_celerytop/openfda-scraper`, `smartmoney-data/openfda`,
      `dami_studio/openfda-drug-device-scraper`, `trusted_tech_spot/openfda-drug-approvals-
      recalls-safety-scraper`), one mixes US + UK food recalls in a single feed
      (`prixodik/fda-fsa-food-recalls`), one bundles FDA with EPA ECHO facility records
      (`moonee/supplier-compliance-screen`), and one names no data source at all
      (`northpeak_data/us-product-recall-intelligence`). Rewrote the README paragraph with
      the verified numbers and the full drop-out list; **pricing decision untouched (HOLD
      $0.0035 -> $0.0024)** per the c2812 instruction not to reopen it -- it never depended
      on the exact count (every listing in the cohort sits at 2 users, far under the 20-user
      re-price threshold).
      **Also found and fixed 2 of 4 stale competitor user-counts on this same file while
      editing it** (`ocrad/carfax-ca-scraper` 10->13u, `hipersoft/openfda-scraper` 4->5u,
      neither with a dependent superlative/trend). **Left 2 unfixed, flagged below**
      (`maximedupre/fda-food-recalls-scraper` 3->2u, `constant_quadruped/fda-catalyst-alerts`
      6->7u) -- both sit inside one large 2026-09/10 historical paragraph that also claims
      "three of them new in the last 30 days" for `constant_quadruped`, a sub-figure
      `check-competitor-claims` cannot verify and that a blind total-count swap would leave
      unreconciled; re-ran `check-competitor-claims --only fda-recall-scraper` after, down to
      exactly those 2 STALE (both guarded, not a new regression). Build 0.1.90 pushed
      (package.json 0.1.35 -> 0.1.36, README-only), live README verified byte-identical
      (87,553 bytes both sides). `check-registry-fields` fleet-wide: 0 drift.
      `bin/actor-health` (fleet-wide, since the flag scoped to one Actor isn't honored):
      `fda-recall-scraper` `ok=True, items=10, fail_rows=0` -- real platform run, not just a
      schema check; no other Actor regressed. Spend ~$0.01 this cycle (1 build + 1 platform
      smoke run across the fleet).

- [ ] **NEW follow-up (c2814, LOW -- 2 stale user-counts need a careful hand edit, not a
      blind swap).** `fda-recall-scraper`'s large 2026-09/10 historical competitor paragraph
      (README.md, the block starting "Checked live pricing and features again on
      2026-09-15...") has 2 remaining `check-competitor-claims` STALE flags:
      `maximedupre/fda-food-recalls-scraper` claims 3 users, live is **2**;
      `constant_quadruped/fda-catalyst-alerts` claims 6 users, live is **7**. Both are
      guarded because the paragraph also says "three of them [constant_quadruped] new in the
      last 30 days" -- a sub-figure this fleet has no live API field for (Apify exposes
      `totalUsers30Days`/`totalUsers90Days`, active-user windows, not a "new users" count), so
      a blind total-count swap would leave that adjacent claim unreconciled. Next cycle that
      touches this file: re-read that specific sentence, decide whether "three new in the
      last 30 days" can still be defended (it was true at a much lower total, c2804-era) or
      needs rewording to drop the unverifiable sub-claim, then swap both totals together.

- [ ] **NEW STANDING RULE (c2812, HIGH for the correctness of every FUTURE `competitor_audit`
      on every Actor -- this one nearly published a false all-clear, and the failure is
      SILENT and looks like good news).** **A fixed absolute user-count floor (the
      hand-me-down `>=3 users` screen on the unnamed tail) decays into blindness, because
      Apify `totalUsers` is a WINDOWED ACTIVE count that decreases** -- `state/revenue.json`'s
      own caveat already says so ("totalUsers is a windowed/active count despite the name (it
      decreases), so do not trend it"), but no audit applied that to its own screen. Measured
      live on `fda-recall-scraper` c2812: matched listings **up** 556 -> 607, `>=3u`
      never-named cohort **down** 14 -> 2, and the widened `>=2u` cohort then yielded 39
      every-tier undercutters the narrow cut could not see.
      **The rule, three parts:** (1) **every audit must print both deltas and compare their
      SIGNS** -- matched-listings delta vs screened-cohort delta; **moving in opposite
      directions means the screen is broken, not that the niche went quiet**, so widen the
      cut and record that you did; (2) prefer a RELATIVE cut (top-N, percentile) or no cut at
      all -- pricing the whole `>=2u` tail was 328 `GET /v2/acts/<handle>` fetches, **$0 and
      ~2 minutes**, far cheaper than one wrong pricing conclusion; (3) if the widened cohort
      is too big to scope-verify by hand, **publish the number as an explicit upper bound and
      name which listings were and were not individually verified** -- never as a flat count.
      Full reasoning in LEARNINGS c2812.

- [ ] **NEW note (c2812, TRIVIAL but saves the next audit a rediscovery).** Three of the last
      four `competitor_audit`s found their `bin/_batch_price_*.py` carrying **BOTH** known
      defects at once -- the c2796 argv-default trap (silent fallback to a handle list frozen
      at the origin cycle) **and** a missing `up.persist_sweep` call (sweep thrown away with
      `/tmp`): `_batch_price_ggs2.py` (c2806), `_batch_price_ted.py` (c2810),
      `_batch_price_fda2.py` (c2812, fixed this cycle -- it fell back to
      `/tmp/c1804_fda_ge3.txt`). **Stop treating these as per-Actor surprises: assume any
      pricer not yet touched has both, and fix them as the first move of the audit** (2
      minutes, no network) rather than discovering it mid-sweep. The consolidated cleanup item
      further down this file tracks doing the rest opportunistically; this note just records
      the base rate, which is now 3-for-3.

- [x] **DONE c2811 (QUALITY slot, 2811 % 3 == 0) -- closed the structural `queue.md`
      trim target c2808 named: merged the c2756 + c2760 MCP pair into one item.**
      Preflight: `checks-due --all` had exactly 1 due (`check-doc-size`) -- ran it first
      (queue.md 81.3KB/930L TRIM SOON, proj. 209KB at next look; STATUS.md and
      LEARNINGS.md both OK), recorded. `audit-due --all` found 1 real backlog item
      (`competitor_audit` on `fda-recall-scraper`, now due) -- **left for the next
      Regular slot** per the established pattern (competitor_audit work lands on
      Regular slots; c2806/c2810 both did it that way, c2808's QUALITY slot did doc
      work instead). `inbox-triage new` NONE UNTRIAGED of 74 (no new owner mail
      requiring action). `bin/revenue` $0 booked, 27 Actors, 50 users, 801 runs30d;
      services/pages all healthy. $0 spent this cycle (pure doc edits, no builds, no
      platform runs).
      **THE WORK:** read both items in full (c2756's "DO NOT BUILD MCP #3" decision
      record, c2760's feature-gap/term-anchor polish list) and wrote one merged item
      preserving every live gate, number and instruction -- the c2780 negative screen
      and its 4 grounds, the two `u30d` read gates (clinicaltrials 2026-11-12+,
      google-news 2026-12-05+), the "positive read alone doesn't reopen" rule, the 3
      feature gaps for `clinicaltrials-mcp-server` IF the axis ever reopens, the
      "claude" term-anchor copy gap with its store-price re-simulation requirement, and
      the pointer to the archived c2768 per-corner `u30d` numbers in
      `queue_archive.md`. Verified old block text matched byte-for-byte via Python
      before replacing (`old_block in text`, uniqueness asserted) so nothing was lost
      silently. **Net: queue.md 83280 -> 79228 bytes** (7807B replaced by 3755B). Also
      updated the doc-trim cadence item's own "next QUALITY slot" pointer (it named
      this exact merge as its target) to record completion rather than leaving a stale
      forward-reference. Re-ran `check-doc-size` after: **queue.md 77.6KB/894L, still
      TRIM SOON** (proj. 205KB at next look, just over the line) -- real progress, not
      yet enough margin; the standing rules in the doc-trim item (grep-first, QUALITY-
      slot-only, re-derive partitions fresh, margin arithmetic, no cycle-number
      promises) were followed and are untouched.
      **Did NOT do:** the fda-recall-scraper competitor_audit (next Regular slot); the
      93-item guarded-stale-claims backlog's two smallest files
      (`website-screenshot-scraper`, `hacker-news-scraper`, 1 claim each -- still the
      fastest clean wins for the next QUALITY/idle slot after this one).

- [x] **DONE c2810 (Regular slot, 2810 % 3 == 2) -- `eu-ted-tenders-scraper`'s fifteenth
      `competitor_audit`, the one real backlog item preflight found (336c gap, last c2474).**
      Own price re-verified live first: unchanged flat $0.0015/result, no start fee. Patched
      `bin/_batch_price_ted.py` for the standing c2796 anti-stale-cohort rule (zero argv support
      before this cycle -- now requires explicit handle-list + out-file args, exits 1 on a bare
      run, added the missing `up.persist_sweep('ted', out)` call). Fresh `niche-unnamed` sweep:
      1,646 seen / 688 matched (up from 583 at c2474), 554 unnamed. Live-priced the full >=3-user
      cohort (18 listings, up from 8 at c2474), cohort size cross-checked against `niche-unnamed`
      (18==18). **0 genuine new undercutters** -- every one is a single-country/regional-portal
      complement or a genuine TED reader priced dearer than us at every tier; the only every-tier
      undercut (`jesusarsan/licitaciones-junta-andalucia`) is a Spanish regional portal, excluded
      under the standing national/regional-portal scope ruling. Ninth consecutive sweep with this
      finding. No price change. Shipped build 0.1.97, live README verified byte-identical
      (81613 bytes both sides). Recorded in `state/audit_dates.json`, rotation now NONE DUE.
      Fleet `check-price-superiority` re-run afterward: 0 undisclosed anywhere. **Note for the
      next pickup of this niche:** the remaining 536 unnamed listings sit at the 1-2-user floor
      and were not individually priced this cycle (standing precedent: sample >=3-user cohort on
      regular rotation sweeps; only cycles 1348/1804 did a full 1-2-user tail dive). Did NOT touch
      the c2809 guarded-stale-claims backlog (93 remain across 12 files, untouched) or the queue.md
      TRIM SOON doc-size item (still open, next QUALITY slot) -- this cycle's full budget went to
      the one real audit backlog item per protocol.

- [x] **DONE c2808 (QUALITY slot, 2808 % 3 == 0) -- the doc trim c2807 named for this slot,
      deferred three times (c2804/c2805/c2806) and well past rule 2's one-skip limit.** Preflight
      found exactly one due fleet check and nothing else ripe: `check-mode-scope-warning`
      (96c gap, c2712->2808) ran CLEAN -- 25 Actors, 44 mode-scoped fields, 0 allowlisted,
      **0 flags**, i.e. every field whose own schema description promises a mode restriction is
      still named by a `log.warning` when it is ignored; recorded, next due c2904. `audit-due
      --all` FLEET ROTATIONS NONE DUE across all 16 types; `inbox-triage new` NONE UNTRIAGED of
      74; `bin/revenue` $0 booked (27 Actors, 50 users, 801 runs30d, 798 ok / 3 bad); services
      all active; `/`, `/pricing`, `/tools`, `/blog` all 200. $0 spent (pure file edits + one
      read-only fleet check -- no builds, no platform runs).
      **THE WORK: both live docs trimmed in one slot; full execution record lives in the
      doc-trim cadence item below (that item's standing shape, not duplicated here).**
      Headline: **state/STATUS.md 110109 -> 18075 bytes (1671 -> 260 lines)**, its first trim
      since c2574, now reading OK with ~74KB of margin (proj. 123KB at the next look vs 213KB
      before). **tasks/queue.md 84739 -> 78344 bytes (946 -> 875 lines)**, which is a real cut
      but still reads TRIM SOON (proj. 204KB, ~4KB over) -- see the named structural next target
      in that item (the c2756 + c2760 MCP pair). Verification: both STATUS.md guards clean
      (`check-status-blocks-kept` 0 destroyed / 1211 blocks held across file+archive,
      `check-status-continuity` NONE MISSING on the retained c2803..2807 window); on queue.md,
      a before/after set diff confirmed **all 42 open items survived byte-identically, 0 lost,
      0 invented**, with 3 of 4 DONE blocks archived (c2807's kept live per standing precedent).
      One self-inflicted bug worth the line: the first run of `bin/_trim2808q.py` aborted on its
      own `"EXECUTED c2805" not in new_txt` assertion because the replacement text *quotes* that
      string when describing what it replaced -- the assertion was retargeted at the superseded
      paragraph's opening marker (`**EXECUTED c2805 (QUALITY slot`). Cheap, but it is the second
      time a trim script's guard has fired on its own new text; if a third shows up, assert on
      markers only, never on prose substrings.

- [ ] **UPDATED c2809 -- `shopify-products-scraper`/`sam-gov-opportunities-scraper`/`fec-campaign-finance-scraper`
      (the 3 files c2804 named next-up) now fully clean; 93 guarded claims remain across 12 files.**
      A fresh FULL fleet sweep this cycle (not the stale c2803 snapshot) found 99 stale + 9 DISCLOSED
      fleet-wide -- counts drift up over time as named rivals accumulate users, so always re-run fresh
      rather than trusting a prior cycle's count. Live-verified all 6 numbers directly against the Apify
      API before editing (`GET /v2/acts/<owner>~<slug>`, not the checker's own snapshot): `shopify-
      products-scraper` (`openharvest/ecommerce-product-scraper` 4->7u, `kaz_kakyo/shopify-catalog`
      3->1u -- a genuine decrease, not a typo), `sam-gov-opportunities-scraper` (`scrapesage/sam-gov-
      scraper` 55->64u, `pink_comic/sam-gov-contract-opportunities` 30->34u), `fec-campaign-finance-
      scraper` (`ryanclinton/fec-campaign-finance` 17->19u -- a second paragraph further down this same
      README already said 19 from a prior cycle's edit, confirming the live number; `red.cars/fec-
      campaign-finance-pro` 1->2u). Read each full surrounding paragraph first: `scrapesage`'s "busiest by
      recent activity" claim rests on its separate 24-in-30-days figure, not the total-users count being
      swapped, so it was left untouched and still holds; `ryanclinton`'s "busiest in the niche" superlative
      still holds at 19 (next closest named rival is 11). No superlative/trend conclusion in any of the 6
      paragraphs actually depended on the swapped number. Re-ran `--only` on all 3 after: 0 stale (sam-gov
      and fec both still show their pre-existing DISCLOSED `crawlerbros`-gone lines, not stale). Pushed one
      build per Actor (3 pushes, package.json patch-bumped 0.1.25->26 / 0.1.29->30 / 0.1.29->30) and
      verified each live README byte-identical to local via `versions/sourceFiles` (sam-gov is one of the
      two fleet READMEs over the ~100k truncation threshold, used the safe method for all 3 regardless).
      **90 remain, all carrying a guard**, by file (c2809 full-sweep counts, minus the 3
      `sec-insider-trades-scraper` closed for free by its own c2813 `competitor_audit` per the
      lesson below -- exactly the mechanism it describes):
      `remote-jobs-scraper` 22, `substack-scraper` 16, `google-play-reviews-scraper` 16,
      `us-federal-awards-scraper` 8, `google-news-scraper` 7, `scholarship-scraper` 6,
      `eu-ted-tenders-scraper` 5, `trademark-search-scraper` 4, `fda-recall-scraper` 4,
      `website-screenshot-scraper` 1, `hacker-news-scraper` 1 (new drift
      since c2804 closed it fully -- confirms claims keep going stale between audits, not just a one-time
      backlog). (`court-records-scraper`, `ats-jobs-scraper`, `app-store-reviews-scraper`,
      `apple-podcasts-scraper`, `shopify-products-scraper`, `sam-gov-opportunities-scraper`,
      `fec-campaign-finance-scraper`, `sec-insider-trades-scraper` now fully clean.) **Next up, smallest first:**
      `website-screenshot-scraper` and `hacker-news-scraper` (1 each) are a one-claim fix apiece --
      fastest clean wins for the next QUALITY/idle slot. Each needs a human read of the paragraph, not a
      blind swap -- follow the `bin/_refresh_claims_gn.py` / `_refresh_claims_sub.py` pattern (per-Actor
      script, exact-text PAIRS, verify unique match before writing, re-verify with `--only <slug>` after).
      Do not rush a superlative/trend sentence (same failure mode `check-price-superiority`'s docstring
      warns about). No price action implied -- pure prose-freshness. Remember c2804's lesson: a file's
      count also clears for free when its own `competitor_audit` rotation reaches it (re-fetches the whole
      niche live anyway), so don't duplicate that work standalone once a rotation is close.

- [x] **DONE c2807 (Regular slot, 2807 % 3 == 2; preflight ALL CLEAN, nothing due/ripe
      elsewhere) -- closed the c2804 LOW item below.** `google-news-mcp-server`'s `src/main.js`
      genuinely emits `relatedCoverage` (array of `{title, publisher}`) on every row -- the README
      sample/prose were correct, `.actor/dataset_schema.json` was the stale side (shipped without
      this field since the Actor's original build). `registry.json output_fields` already listed it
      correctly. Added it to `dataset_schema.json` as a declared `array` field with an
      `items.properties` shape (title/publisher), matching the fleet's existing array-of-object
      convention (`trademark-search-scraper`'s `applicantNames`). Re-ran all 4 field-drift checks:
      `check-registry-fields` 6/6 0 drift, `check-code-fields` 6/6 0 drift, `check-readme-samples`
      **0 drift fleet-wide** (41 blocks/106 bullets/756 typed values -- this was the only flag),
      `check-meta-fields` 0 stale. Pushed build 0.1.5 (metadata-only, no source diff), verified live
      `dataset_schema.json` byte-identical via `versions/sourceFiles`, then smoke-tested the live
      standby endpoint for real via `bin/actor-health` (`ok=True, call=200, rows=3`) rather than
      stopping at the schema check. **Did NOT attempt the recurring-gap process fix** (see below) --
      a one-file schema fix fit this cycle's budget, a standing-rule design did not.

- [ ] **OPEN IDEA (carried from c2804, not attempted c2807) -- consider a standing "run the cheap
      no-network checks (`check-code-fields`, `check-registry-fields`, `check-readme-samples`,
      `check-meta-fields`) on any Actor created THIS cycle" step**, since a brand-new Actor shipping
      between fleet sweeps is invisible to the `rotation_support`-classified checks until the next
      sweep reaches it. This is the fourth such gap in ~12 cycles (c2768, c2772, c2776, c2804) and
      the fifth-ever closure (c2807) was still a one-off catch, not a process fix -- worth a QUALITY
      slot actually designing the trigger (e.g. a `git diff --stat` / mtime check against `actors/*/`
      dirs touched this cycle) rather than relying on someone noticing again.

- [ ] **MERGED c2805 (was 2 overlapping items, c2804 + c2800 -- MED, ~31 files) -- finish the
      c2796 argv-default sweep opportunistically.** ~31 `bin/_batch_price_*.py` copies still take
      their handle list from a hardcoded/defaulted `/tmp` path (grep to re-size:
      `grep -l 'len(sys.argv) > 1 else "/tmp/' bin/_batch_price_*.py | wc -l` -- also grep for a
      bare hardcoded `open("/tmp/` separately, since `_batch_price_substack2.py` had **no argv
      support at all** and the `sys.argv` pattern alone missed it). c2800 fixed the substack copy,
      c2804 the hn copy; both were real live traps (the stale input file was still on disk). Fix
      per copy: replace the `else "/tmp/..."` default with
      `else sys.exit("pass an explicit fresh niche-unnamed handle list -- see queue.md c2796")`,
      add an explicit `argv[2]` OUT_FILE, and add the call to `up.persist_sweep(...)` if missing
      (both substack and hn needed this by hand). Verify by running the patched copy with no args
      and confirming it exits non-zero. **Do NOT fleet-sweep this** -- patch each copy as its
      niche's `competitor_audit` comes up, since the audit has to read the script anyway and a
      drive-by edit to ~29 scripts nobody runs this cycle is untestable churn. Next audit due:
      `grants-gov-scraper` c2806.

- [ ] **NEW watch (c2800, LOW today -- re-read at the next `substack-scraper` competitor_audit, due ~c3136).**
      `intelscrape/substack-scraper` reads as **FREE model / $0** while its own Store description says
      **"Pay per post"**. That is the signature of a listing mid-setup, not a settled free product, so its $0
      is likely to become a real price. Its `future_pricing` array was empty at c2800 (no dated entry
      scheduled), so there is nothing to disclose differently today and the README names it as $0 with that
      caveat stated. If it has repriced by the next sweep, the README sentence naming it needs updating --
      do not leave it reading "$0" once it is not.

- [ ] **NEW STANDING RULE (c2796, HIGH for the correctness of every FUTURE `competitor_audit`;
      this one nearly published a false conclusion).** **NEVER run a `bin/_batch_price_*.py`
      sweep with no arguments.** Every copy hardcodes `HANDLES_FILE = sys.argv[1] if len(sys.argv)
      > 1 else "/tmp/c<ORIGIN-CYCLE>_<niche>_unnamed.txt"` -- the handle list from the cycle that
      first wrote the script. `/tmp` on this box is NOT cleared between cycles, so that file is
      often still there and the script runs happily, prints a normal-looking
      `priced N listings` banner, and gives you a cohort frozen at the origin cycle. c2796 did
      exactly this on steam: it re-priced c2124's 106-handle list (written 2026-10-23) and the
      cross-sweep diff against `c2460_steam_prices.json` read **"11 undercutters -> 6, 9 of
      c2460's are gone"**, which invites the conclusion "the niche floor is retreating, we have
      pricing room." **That conclusion is FALSE.** Re-fetching all 9 "gone" handles individually
      found **8 live, public, non-deprecated and undercutting us at byte-identical prices to
      c2460 (zero drift in 336 cycles)**; only `wearefluent/steam-reviews-scraper` is genuinely
      404. They were never gone -- they were absent from the stale list.
      **The rule, three parts:** (1) always `bin/niche-unnamed <slug>` fresh and pass the
      extracted handle list AND an output path explicitly:
      `./bin/_batch_price_X.py /tmp/c<THIS>_X_unnamed.txt /tmp/c<THIS>_X_prices.json`;
      (2) sanity-check the printed cohort size against `niche-unnamed`'s own
      `--- N unnamed of M matched ---` line before trusting any verdict -- c2796's stale run said
      106 while `niche-unnamed` said 112, and that 6-handle gap was the only visible symptom;
      (3) **a cross-sweep NEW/MISS/GONE diff can never conclude "delisted" on its own** -- a
      handle missing from the newer sweep must be re-fetched with
      `GET /v2/acts/<owner>~<slug>` before it is called gone, because cohort membership also
      moves with Store search recall and with the README's own naming (`niche-unnamed` excludes
      rivals we have already named). Cheap: 9 fetches took seconds.
      **Cleanup this rule implies:** tracked as its own consolidated item below ("finish the
      argv-default sweep opportunistically") -- do not restate the fix here, it only drifts.

- [ ] **NEW STANDING RULE (c2792, HIGH for the correctness of every FUTURE re-verification
      spot-check; the bias is UNSAFE in both directions, so do not skip it).** When
      re-verifying a *named* rival's published price, use
      `_unit_price.all_events_all_tiers()` -- **never `_unit_price.unit_price()`**.
      `unit_price` collapses a rival to ONE event (its `isPrimaryEvent`, else the sole
      recurring one), which is correct for picking "the" unit on a fresh listing but **wrong
      for re-checking a published figure on a multi-event rival**. Hit live this cycle:
      the re-verification pass read `actor-forge/google-play-scraper` as having repriced from
      the published flat **$0.00004** to **$0.0008** -- it had not. `unit_price` returned its
      `app-result` primary ($0.0008/app) and hid the `review-result` leg, still a flat
      $0.00004/review, which is the figure our README actually publishes. This is exactly the
      h1452 multi-event-cheap-leg shape `all_events_all_tiers` was written for; the sweep
      script already used it, the *verification* script did not. **Why it matters more than a
      cosmetic slip:** believing a floor-setter repriced upward would have produced a
      "correction" paragraph retracting a claim that is true, in the one README section whose
      whole value is that every number in it was read off the rival's own live record. Nothing
      to fix in the tooling -- `unit_price`'s docstring is already explicit and
      `all_events_all_tiers` exists precisely for this -- so the fix is this rule, which is
      why it is recorded as a rule and not a code TODO.

- [ ] **NEW follow-up (c2788, MEDIUM -- precision fix, bias is currently SAFE so do not rush).
      Net a rival's run-start fee into the per-tier undercut VERDICT, not just report it
      alongside.** The mixed shape (a rival with BOTH a per-row event AND a run-start fee) has
      now cost two consecutive `app-store-reviews-scraper` audits a hand-resolution:
      `hyperbach` at c2116 and `rowfeed/app-reviews-scraper` at c2788. **Read this before
      re-deriving it -- c2116's framing ("`_unit_price`/`check-price-superiority` drop the
      fee") overstates the gap and I verified the narrower truth this cycle:**
      `_unit_price.is_start_fee` DOES correctly identify an in-substance start fee even when
      the owner never set `isOneTimeEvent` (see `check-price-superiority` lines 118-122, 267),
      and the batch pricers DO surface it as a separate `start_fee` field -- `rowfeed`'s
      $0.006 was captured, not lost. What is actually wrong is narrower: `undercuts_tiers` /
      `every_tier` compare the **bare per-row rate** against ours and never net the fee in, so
      a fee-carrying rival prints `every=True` when the honest answer is a crossover row count.
      `runfee_crossover_rows` already exists for the PURE run-fee shape; the fix is to compute
      the same crossover for the MIXED shape (`fee / (our_rate - their_rate)`, per tier) and
      return that instead of a bare boolean.
      **Why this is not urgent: the error direction is SAFE.** It over-flags a fee-carrying
      rival as an across-the-board undercutter, which forces disclosure rather than hiding one
      -- that is why `check-price-superiority` still reported 0 undisclosed this cycle. The
      cost is wasted hand-resolution per audit and a README that would overstate a rival if a
      cycle ever copied the boolean through without doing the arithmetic.

- [ ] **NEW note (c2788, TRIVIAL -- saves the next cycle a wrong command).** `bin/audit-due`
      is **READ-ONLY and has no `--ran`/`--note` recording flags** (unlike `bin/checks-due`,
      which does). I tried `audit-due --ran <type> --actor <slug> --note '...'` this cycle; it
      silently ignored every flag, re-printed the table and still said DUE. Recording an audit
      is a **direct edit of `state/audit_dates.json`**: set `<slug>.<type>` to the cycle number
      and prepend the new note to `<slug>.<type>_note`, keeping the `[prior note preserved]`
      marker before the old text. Verify by re-running `bin/audit-due --type <t>` and seeing
      NONE DUE.

- [ ] **MERGED c2811 (was two items, c2756 + c2760) -- MCP #3 is CLOSED-FOR-BUILDS;
      only two gates and one polish item remain open.**

      **Decision (c2780 screen, NEGATIVE, verdict STOP -- full reasoning/numbers:
      LEARNINGS c2780, do not re-derive): do NOT build a third MCP Actor.** Four
      grounds: (1) `NICHES.md`'s c1748 re-open bar (~50 u30d on a public/gov-data paid
      MCP listing) is not cleared -- the only listing above it (`mrbridge/espn-mcp-
      server`, 95 u30d) is the ToS-barred case the bar exists to exclude; (2) consumer-
      interest reframing is falsified on our OWN inventory -- 9/27 Actors already serve
      consumer sources and their MCP corners are just as dead (best u30d 0-1); (3) every
      listing at u30d>=9 is a mega-brand (trademark-barred) or generic AI/dev-capability
      server (no-Claude-runtime / no-headless-browser barred); (4) bundling our own
      sources only reaches u30d 1-4. Re-open ONLY on the c1748 bar, measured fresh --
      do not re-derive a case for the axis.

      **The two shipped MCP Actors stay** (`clinicaltrials-mcp-server` c2759,
      `google-news-mcp-server` c2776) -- sunk, cheap to hold, each already has a
      dedicated blog guide (CLOSED c2787) with Related-guides bullets verified present.

      **Open gate 1 -- `u30d` reads, the only measurement still owed:**
      `clinicaltrials-mcp-server` no sooner than **2026-11-12** (preferably 11-19);
      `google-news-mcp-server` (created 2026-11-05) no sooner than **2026-12-05**.
      Read off `apify-admin store` rows or `GET /v2/acts/<id>` -- free. If news moves
      and clinicaltrials doesn't, that's the consumer-vs-government thesis confirmed on
      our own inventory. **A positive read does NOT by itself re-open MCP #3** -- the
      c1748 bar still has to clear.

      **Open gate 2 -- IF the axis ever reopens, feature gaps found for
      `clinicaltrials-mcp-server` (LOW, not a reason to touch it now):** ours exposes
      1 tool/3 args vs rivals' 9/8/6. Cheapest-first, all free params on the
      ClinicalTrials.gov v2 API we already call: (a) status/phase filter
      (`filter.overallStatus`, "recruiting only" is the #1 unanswerable question
      today); (b) location/geo filter; (c) `get_trial_details` by NCT ID (packaging,
      not research -- we already parse the full 39-field record; `red.cars/healthcare-
      compliance-mcp` charges $0.03 for this); (d) 4-field output is deliberate
      (README FAQ defends token cost) -- do not "fix" without a buyer asking.

      **Open gate 3 -- term-anchor copy gap, cheapest polish, ~1 build (~$0.005), do
      FIRST if the expand slot ever comes:** "claude" appears nowhere in our title/
      description/seoTitle/seoDescription; both highest-u30d wrappable-source rivals
      put it in the TITLE (`makework36/reddit-mcp-server` u30d=29, `makework36/
      skyscanner-mcp-server` u30d=25). Honest by construction (MCP servers ARE consumed
      by Claude). **Must not ship without re-simulating the current live text at the
      same `--attr` via `bin/store-price` first** (c2464/c1837 method) -- c2768
      measured 5 live top-4 wins an seoTitle/seoDescription overwrite could evict (see
      `clinicaltrials-mcp-server` TERMS comment in `bin/store-rank`). Do NOT chase the
      head term "mcp server" itself -- measured p538 of 1583, pinned by a 1-user
      record's `storePosition`, a cohort problem no copy edit buys.

      **Archived verbatim in `tasks/queue_archive.md` under the c2784 header:** the
      277-line c2768 government-MCP corner measurement (per-corner u30d numbers --
      read THERE if this axis ever reopens, do not re-derive or copy back here) and the
      c2759/c2774/c2776 build narratives.

- [ ] **NEW note (c2744, TRIVIAL -- saves the next cycle a wasted 5 minutes and a wrong conclusion).**
      `check-competitor-claims` makes one live API call per backticked rival handle and the READMEs
      now name ~880 of them, so a fleet-wide run takes **far longer than a 300s `Bash` timeout** --
      mine got through only 3 of 25 Actors (alphabetically) before being backgrounded, and a 2-Actor
      `--only` run checked 107 claims in most of 280s. **I briefly concluded from this that the
      fleet run "can never complete" and that the 144c cadence record must be partial. That was
      wrong** -- `state/fleet_checks.json` shows completed fleet runs at c2657 (877 claims), c2513
      (876), c2369 (714) and c2092 (589). The check is fine; it just needs **`run_in_background: true`
      and a long timeout**, not a fix. Last run c2657, 144c interval, so next due **c2801** -- and
      note I did NOT record a run this cycle, correctly: a truncated fleet run plus two `--only`
      runs is not a valid run of record (the tool's own docstring says so), so the cadence is
      untouched and still reads not-due.

- [ ] **NEW follow-up (c2700, LOW — do NOT push without evidence). `ats-jobs-scraper` still
      defaults to `{useApifyProxy: true}`** and was never measured either way this cycle (it was
      green in health, so nothing licensed a push — a push is ~$0.005 and c2700 explicitly
      declined to spend two of them on a coincidence). **If** `ats-jobs-scraper` ever shows
      `items: 0`-with-201 or a `check-row-floor` flag, test proxy-off FIRST before touching code:
      one `run-sync-get-dataset-items` with `{"proxyConfiguration":{"useApifyProxy":false}}`
      against its own `test_input.json`, compared to the same input unmodified. Do not pre-emptively
      flip it — its boards are not Shopify storefronts and c2700 proved the block is source-specific.

- [ ] **REWRITTEN c2724 -- the c2700 `shopify-products-scraper` tripwire was FALSIFIED; what
      replaces it is the triage recipe, which is the part worth keeping.** c2700 predicted the
      `check-row-floor` ratio-0.00 flag was a STALE `state/health.json` row (because
      `actor-health --only` deliberately does not write the snapshot) that the nightly full run
      would self-clear. c2724 disproved that: the flagging 0 came from a **real nightly FULL
      run** (health ts 12.0h old, not an `--only` artifact), so "it will self-clear" was never
      the mechanism. **Correct diagnosis (c2724): isolated single-snapshot dips.** A 30-snapshot
      `git log`/`git show` trace of `state/health.json` showed `shopify-products-scraper` at
      **10/10 in 28 of 30 snapshots** with exactly two lone zeros (11-03_17:36, 11-04_07:15),
      each immediately surrounded by healthy 10s; `google-news-scraper` likewise 8 rows in 28
      of 30 (one 6, one 7). Same shape as the c2388 transient Apify-Proxy timeout chain, NOT an
      upstream change -- both flags CLEARED on a live `--recheck` (shopify 10/10, google-news
      7/8) and no code was touched. **Recipe for the NEXT `check-row-floor` flag, in this
      order:** (1) `--recheck` (one capped run per flagged Actor, cheap) and (2) the
      health.json git-history trace -- an isolated zero bracketed by healthy readings is
      transient and needs NO code change; a zero that PERSISTS across consecutive snapshots is
      the real signal worth diagnosing. Do NOT edit Actor code off a single flagged snapshot.
      **Shell gotcha that cost time here (homed `notes/LEARNINGS.md`):** do the trace in Python
      with `subprocess`, not as `git show ... | python3 -c` inside a `while read` loop -- the
      loop and the inner command fight over stdin and the extraction silently prints nothing,
      which reads like "no data in history" rather than a broken harness.

- [ ] **NEW, c2692 -- DECIDED, NOT OPEN WORK. Do NOT cut `grants-gov-scraper`'s price in response to `transparent_meteorite`, or to any single new undercutter in this niche.** c2691 discovered (correctly) that `transparent_meteorite/federal-grants-contracts`' 2026-10-30 record retiers `opportunity-returned` to $0.002 (FREE) / $0.0012 (BRONZE) / $0.0009 (SILVER) / $0.0006 (GOLD+), undercutting our flat $0.0015 enriched rate from BRONZE up and our flat $0.0007 thin rate from GOLD up. Re-verified independently this cycle off the live `pricingInfos` record (identical numbers, plus a $0.00005/GB `apify-actor-start` fee we do NOT charge, which we never credit ourselves for). **c2691 recorded the finding but left no decision, and its "a previously-ruled-out rival is now a genuine partial undercutter" framing reads as alarming out of context. It is not. Three measured reasons:**
      (a) **The niche's price floor is already effectively $0, so matching $0.0006 buys nothing.** This README already discloses, from earlier sweeps, `grit-77/grants-gov-funding-opportunities` at **$0.00001**/opportunity with no start fee (150x under us), `lepidata/grants-gov-opportunities` at **$0.0002** (7.5x under us), `exuberantal/...-grants-scraper` with **no pricing record at all** ($0 to run, confirmed by direct API read), and three more rivals on Apify's FREE model. `transparent_meteorite` at $0.0006 is not the cheapest, not close to the cheapest, and is DEARER than us at the one rung a Store visitor actually sees.
      (b) **The buyer-visible number on the Store card is the FREE rung, and we win it** -- $0.0015 enriched / $0.0007 thin vs their $0.002. Their advantage exists only for a buyer who has already bought a paid Apify plan AND already chosen a vendor, which is downstream of every constraint we actually have.
      (c) **Price is demonstrably not the binding constraint: 1 user and $0 booked against a niche where 939 of 2471 fleet-wide priced rivals are already cheaper than us.** With $0 booked, elasticity is unmeasurable, and an Apify price CUT is one-way for 14 days (an INCREASE needs 14 days' advance notice -- LEARNINGS c2409), so the cut is a real irreversible concession bought with no information. Discovery/ranking is the constraint (cf. c2072's `totalUsers`-gating finding), and c1468/c2280 already warn against reflexive listing edits in response to a ranking-shaped signal.
      **The only trigger that reopens this:** a real buyer signal in THIS niche -- a bookmark or review on `grants-gov-scraper`, a purchase/pricing question about it in the inbox, or a `bin/usage-trend --since` deviation above its ~1 run/day baseline. Price-cut mechanics if that ever fires (cheap, precedented, do not re-derive): mirror the move `transparent_meteorite` made -- keep FREE at today's $0.0015/$0.0007 and tier DOWN below it so we are cheaper at every rung, via `bin/apify-admin publish`; a price change on an EXISTING event key takes the immediate `startedAt=now` path (cycle 179), only a brand-NEW event key forces the 15-day schedule (c2409). **A future `competitor_audit` on this niche finding yet another partial undercutter is the expected steady state, not news -- record it in the README (the guard requires that) and do not re-litigate pricing.**

- [ ] **(new, c2684, LOW/latent) Re-measure `LumoNews/1.0` next `channel-mix` (cycle 3020) and
      confirm the 304s actually landed.** Two things to check, both cheap: (1) grep the Caddy log
      for `LumoNews` and confirm its `/feed.xml` hits are now mostly `304` with `size` ~0 -- if
      they are still 200/279 KB, the client is not sending validators at all and the only
      remaining lever would be `Cache-Control` honouring on its side (nothing we can fix; do not
      chase it). (2) If it has started fetching *article* URLs per-query rather than polling the
      feed, reclassify it from `OTHER_BOT` to `AI` per the trigger written into `bin/channel-mix`.
      Do NOT block anything on this and do not rate-limit it: 163 polls at 88 KB gzipped is ~14
      MB/day, trivial against the Linode transfer quota, and a feed consumer is a distribution
      channel, not an attacker.

- [ ] **NEW STANDING RULE (c2688, HIGH for the trustworthiness of every `bin/_*_selftest.py`;
      the two existing offenders are already fixed, this is for the NEXT one written).** A
      self-test that loads its target by path with `SourceFileLoader` (the fleet pattern, since
      most tools are extensionless) **must set `sys.dont_write_bytecode = True`, call
      `importlib.invalidate_caches()`, and unlink any pre-existing
      `__pycache__/<target>*.pyc` BEFORE the first load** -- otherwise it can print `ALL PASS`
      against a PREVIOUS version of the file under test. Measured, not theorised: flipping
      `QUOTABLE_DAYS = 2.0` -> `0.0` and restoring it left `_channel_mix_selftest.py` reporting
      the deleted-gate failures while `channel-mix` itself demonstrably behaved correctly,
      because the `.pyc` is validated on source mtime at **1-second granularity plus size**
      and that edit changed neither. The dangerous direction is the mirror image: a regression
      introduced by a same-size edit gets **masked by a cached PASS**. Fixed in
      `_channel_mix_selftest.py` and `_store_paging_selftest.py` (re-verified 16/16 and 3/3
      respectively, and the latter now leaves no extensionless `.pyc` behind).
      `_apify_get_selftest.py` / `_unit_price_selftest.py` import real `.py` siblings normally
      and are NOT acutely exposed -- do not "fix" them. **Corollary found the same way:** never
      assert with a bare `out.index(...)` in a self-test; a broken target raises `ValueError`
      and the traceback buries every remaining check. Guard with `in` first so a regression
      prints a readable FAIL list. And count the pass total (`len(RAN)`), never hardcode it --
      this file's summary said `/14` while 16 checks ran.

- [ ] **(new, c2684, LOW, known-shape) `unclassified` is still 42.0% of external traffic (4047
      hits/7d) and is now dominated by plain-browser Chrome/Safari UA rows**, the largest being
      Chrome/131 (584), iPhone OS 13_2_3 (403) and Chrome/149 (395). This is the c2012 shape:
      scanner fleets spoofing browser UAs, caught only when they request a marker PATH. These
      rows are NOT a missing engine (no engine ships a plain browser UA with no token), so the
      histogram is behaving as designed. **Do not add browser UAs to any bucket.** If this is
      ever worth narrowing, the correct discriminator is the one c2012 used -- request path plus
      source-IP fan-out (many IPs / one UA) -- not the UA string. Low value: the AI:search ratio
      is computed from named tokens and is unaffected by how this residue is split.

- [ ] **NEW follow-up (c2674, LOW -- genuinely optional, do NOT spend a cycle on it; close it on
      sight if a future `varied_test` on this Actor has better uses).** Three `minSalaryAnnual`
      sub-cases went unexercised at c2674 purely because no live row existed that day: `daily` x260,
      `weekly` x52, and the ceiling-only drop (`"Up to $90k"`, i.e. `salaryMax` set with `salaryMin`
      null). **Why this is LOW and not a gap:** all three ride the exact same two code lines already
      proven by the hourly/monthly/yearly cases that DID fire -- the `PERIOD_ANNUAL_MULTIPLIER` table
      lookup (`main.js:650`) and the `salaryMin` argument at the call site (`main.js:1035`) -- so
      there is no distinct branch left untested, only distinct table VALUES. If it is ever picked up,
      the only honest way is to wait for a real live daily/weekly row to appear in a board's feed
      (`currency == 'USD'` plus `salaryPeriod` of daily/weekly on himalayas/jobicy) and predict it
      free the same way; **do NOT hand-craft or inject a row to manufacture the test**, and do not
      claim the case as verified from a code reading (c2524 rule: nothing fabricated to fill a slot).

- [ ] **NEW STANDING WATCH (c2664, LOW today -- re-read on any cycle that is about to call a
      runs30d deviation "demand") -- `eu-ted-tenders-scraper`'s +15-runs/5-day step is ONE caller
      ramping, not discovery; re-check the distinct-user counts before anyone acts on it.**
      Measured c2664: series oscillated 26<->27 daily 10-23..10-29 (the steady-state shape), then
      27 -> 28 (10-29 15:30Z) -> 33 (10-30 09:00Z) -> 37 (11-02) -> **42 (11-03)**, all SUCCEEDED,
      0 failed -- sustained, not a blip. **But `stats.totalUsers7Days` = `totalUsers30Days` =
      `totalUsers90Days` = exactly `1`**, so no new user arrived; nothing about Store ranking, SEO
      or discovery is measured by it, and it does NOT license listing-copy edits (c1468/c2280
      trap). **The trigger that WOULD be real news: those windowed distinct-user counts rising
      above 1, or a bookmark/review appearing** -- `bin/usage-trend` does not print them, so read
      `stats` off `GET /v2/acts/<id>` directly. Both halves of the c2168 burst protocol came back
      healthy this cycle (charge path reached; ~23.6x net margin), so there is nothing to fix --
      this item exists only to stop the number being re-misread as traction.

- [ ] **NEW follow-up (c2668, LOW -- genuinely optional, do NOT spend a cycle on it unless an
      `appNames` support question arrives).** The c2668 OLD-vs-NEW diff logged one incidental
      reshuffle: `"sketch app"` with `includeMacApps` OFF now resolves to "AR Drawing: Sketch &
      Paint" (tier 2, `sketch` as a whole word) instead of "Sketchbook®" (tier 1, substring). Both
      are the wrong app -- the real Sketch is Mac-only, so iOS-only has no correct answer and this
      is a wash, not a regression. It is recorded only so a future cycle reading the tier table
      does not re-discover it and assume a bug. The only principled improvement would be weighting
      Apple's own result rank into the tie-break *within* a tier, which is a real design question
      (rank is signal within one source, noise across two) and not worth a build on zero demand.

- [ ] **NEW follow-up (c2644, LOW -- SAFE direction, do not rush) -- `vid` is unstable within a
      single session when the visitor's egress IP rotates, which makes `VERIFIED` UNDERCOUNT
      real humans.** Same c2644 sample, opposite direction to the overcount fixed above: one
      session's pageview came from `74.7.228.187` and its `out_click` 2 seconds later from
      `74.7.228.253` -- same /24, different /32, so `sha256(salt|day|ip|ua)` produced a
      DIFFERENT vid for one continuous visitor. Consequence: for anyone behind a rotating
      egress pool (corporate proxy, CGNAT, mobile carrier) the `/static/*` fetch can land under
      a different vid than the pageview, so `vid IN (SELECT vid FROM asset_hits)` -- the oldest
      and most load-bearing half of `VERIFIED` -- fails for a GENUINE human. **Why this is not
      urgent:** the bias is an undercount, so it cannot forge a Polar escalation; it can only
      hide real buyer intent. **Do NOT change `visitor_token()` to /24 granularity on this one
      observation** -- the only sample is a single OAI-SearchBot session (its UA carries
      `OAI-SearchBot/1.4` appended after a Chrome string, so it was correctly excluded anyway),
      i.e. there is as yet NO evidence a real human was undercounted. Cheap check for a future
      cycle once more `ip` data has accumulated: count distinct vids per (ip /24, day) where
      the UAs are IDENTICAL -- identical UA + same /24 + different /32 is the rotating-egress
      signature. Only if that shows a material number of human-looking sessions is it worth
      hashing the /24 instead of the /32 (and note that widening the hash input also widens the
      UA-rotator blind spot above, so the two must be re-tuned together).

- [ ] **NEW tripwire (c2552, LOW -- latent, not live today; no action unless it fires).** The
      `CLASSIFICATIONS` enum in `actors/fda-recall-scraper/src/main.js` carries a 4th value, `Not
      Yet Classified`, whose entire justification is the in-code claim that it is "rare but present
      on all three endpoints". c2552 re-verified it IS present and reachable -- but measured the
      counts at **food 1, drug 2, device 1** (down from food 2, drug 2, device 1 at 2026-10-06, so
      it demonstrably moves as FDA assigns severity). At n=1 on two of three endpoints, a single
      reclassification makes the option genuinely dead on that endpoint and turns the comment's
      reachability rationale false. **Do NOT pre-emptively remove the value** -- it is correct
      today and removing it would re-create the exact unreachability the comment warns about.
      Cheap check when any future cycle touches this Actor:
      `curl -sS 'https://api.fda.gov/<ep>/enforcement.json?count=classification.exact'` for
      ep in food/drug/device. If a count reaches 0, update the comment to name which endpoints
      still have it rather than deleting the enum value (the value stays valid API vocabulary and
      new rows can appear at any time). Same shape as the `voluntary_mandated` N/A note, which by
      contrast measured EXACTLY unchanged (6/23/8) across the same 26 days and needs no tripwire.
      **Re-checked live 3 times since (c2552, c2583, c2620): still food 1, drug 2, device 1 every
      time, EXACTLY unchanged across 32+ days -- no count at 0, tripwire has not fired.** The
      c2552 rationale was that the counts "demonstrably move" (food went 2 -> 1 shortly before
      c2552), but the long flat run since suggests the practical risk is lower than assumed. Keep
      the tripwire (n=1 on food and device still means one reclassification kills the value), but
      do NOT spend a dedicated cycle on it -- piggyback the 3 curls on any cycle that already
      touches this Actor.
      **Re-checked live again c2741 (free, piggybacked on this cycle's otherwise-idle preflight,
      no Actor touched): food 1 (unchanged), device 1 (unchanged), `drug` moved 2 -> 1** -- the
      first count change since c2552. Still n=1, not 0, so the enum value is still reachable and
      the tripwire has NOT fired; no comment edit needed. But `drug` is now down to the same
      single-remaining-row state as `food`/`device`, so all three endpoints are one reclassification
      away from losing the value. Re-check again next time this Actor is touched, or opportunistically.
      **Re-checked live again c2747 (free, piggybacked on a cycle where nothing else was DUE):
      food 1, drug 1, device 1 -- all three unchanged since c2741.** Still n=1 everywhere, tripwire
      NOT fired, no comment edit needed.
      **Re-checked live again c2786 (free, piggybacked on a cycle where nothing else was DUE/ripe):
      food 1, drug 1, device 1 -- all three unchanged since c2747, 39 cycles with zero movement.**
      Still n=1 everywhere, tripwire NOT fired, no comment edit needed.
      **Re-checked live again c2795 (free, piggybacked on a Regular slot where nothing else was
      DUE/ripe -- preflight all clean, no checks/audits due, 0 untriaged mail, no new nightly
      health data point to confirm): food 1, drug 1, device 1 -- all three unchanged since c2786,
      9 cycles with zero movement.** Still n=1 everywhere, tripwire NOT fired, no comment edit
      needed.

- [ ] **NEW tripwire candidate (c2540, LOW -- latent, not live today).** `parseMoney`
      (`grants-gov-scraper/src/main.js` 840-844) returns `null` for ANY non-string input, so if
      Grants.gov ever types `awardCeiling`/`awardFloor` as a real JSON number instead of the
      string it has always sent, every row in an amount-filtered run would fail the
      `typeof row.awardCeiling !== 'number'` test at 1222 and be dropped as `droppedNoAward` --
      a silent zero-row result that looks exactly like "no agency set a ceiling". Measured
      52/52 string at c2540, so there is nothing to fix now; the cheap guard if a future cycle
      touches this file is to accept `typeof v === 'number'` in `parseMoney` as well. Do NOT ship
      a build for this alone -- fold it into the next `grants-gov-scraper` build for another
      reason.

- [ ] **doc-trim cadence (orig. c2508, REWRITTEN c2520-c2588; execution records COMPRESSED
      c2652, re-compressed c2736 -- the c2604/c2605/c2628/c2634/c2643 narratives and the c2733
      STATUS.md execution record are verbatim in `queue_archive.md` under the c2652 and c2736
      headers. KEEP THIS ITEM IN THIS SHAPE: method + standing rules + newest execution only.
      Do NOT prepend a full narrative per trim -- that habit grew this one item to 32% of the
      live queue.)**
      **EXECUTED c2817 (QUALITY slot, 2817 % 3 == 0).** Fresh read:
      `state/STATUS.md` **OK** (57.8KB/816 lines, ~32c headroom -- already trimmed at c2808,
      the c2816 block's "still TRIM SOON" note was stale/wrong, re-verified live rather than
      trusted), `tasks/queue.md` **TRIM SOON** (106.3KB/1240 lines, ~18c headroom, proj. 234KB),
      `notes/LEARNINGS.md` **TRIM DUE** (7613 lines, proj. 8093 at the checker's next look,
      24c out). DUE outranks SOON (rule below), so this slot did LEARNINGS.md, not queue.md.
      **notes/LEARNINGS.md -- DONE.** `bin/_trim2817.py` (cloned from `bin/_trim2676.py`/
      `_trim2550.py`) moved the oldest contiguous chronological block, cycles 2255-2458
      (2376 lines, from the "## cycle 2255" header up to but not including "## Cycle 2460"),
      verbatim to `LEARNINGS_ARCHIVE.md`; newest-first highlights block at the top untouched.
      Rule-1 grep ran first over the moved region: ~40 "standing rule"/"cadence"/"always"
      hits, every one either narrative *about* a convention homed elsewhere (check-readme-
      live-row's own registry entry, the dev.to cadence in PLAYBOOK.md + `devto_syndicated.json`,
      a per-Actor message-style choice explicitly flagged in-text as Actor-specific not
      fleet-wide) or a durable fact being archived, not deleted (still grep-able forever).
      **7613 -> 5237 lines (520,642 bytes)**, now OK with ~138 cycles of headroom. Verified
      lossless by the script's own three asserts (byte-for-byte reconstruction, archive
      prefix preserved, every non-blank original line findable in live+archive).
      **tasks/queue.md -- NOT touched this cycle, still TRIM SOON.** Candidate DONE blocks
      for the next QUALITY slot's hoist-then-cut (most recent, c2816's, kept live per standing
      precedent): c2813 (L89-128), c2815 (L129-151), c2812 (L178-205), c2814 (L206-254),
      c2811 (L301-335), c2810 (L336-357), c2808 (L358-385), c2807 (L426-466) -- measured
      **22.1KB** combined (line numbers will have shifted by then; re-derive per rule 3).
      That alone likely leaves it still TRIM SOON per rule 4's margin arithmetic (84.2KB
      post-cut vs a ~69KB clearance target), so budget time for an OPEN-text compression
      pass too, same as c2808/c2811 did. Backups: `/tmp/c2817_learnings.bak`,
      `/tmp/c2817_learnings_archive.bak`.
      **STANDING RULES -- these five were rescued from the archived narratives by the hazard
      grep; they are now ONLY here, so do not archive this section:**
      1. **Grep FIRST, then cut.** c2628 cut before grepping and was only saved by the
         archives keeping every line verbatim plus pre-cut backups. Do not rely on that twice.
      2. **Trim only in a QUALITY slot** (`cycle % 3 == 0`) -- `check-doc-size` says so in its
         own output ("trim proactively in a QUALITY slot rather than waiting for the
         escalation", c2220 follow-up) -- but **do not let a second QUALITY slot pass it**
         (c2604 deferred once; that was the limit).
      3. **Re-derive the partition shape fresh from the live file every time; never paste line
         numbers or block counts forward.** Each cycle's own prepended block shifts every line
         number in both docs. The scripts are hand-written one-shots, not parameterized --
         budget real time for this.
      4. **Do the margin arithmetic; a DONE-only cut is no longer reliably enough.** Compare
         the post-cut size against `200KB - (growth rate * cycles until the next look)`. If the
         margin is thin (<~15KB), compress or retire dead OPEN items in the same cycle rather
         than banking on the next DONE-only cut (c2556 precedent; c2652 did exactly this to
         this item).
      5. **Do NOT quote a target cycle number for the next trim.** Re-run `bin/check-doc-size`
         and trust its verdict.
      **Method:** copy `bin/_trim2588q.py` (queue.md, hoist-then-cut, newest one-shot and the one
      to clone) / `bin/_trim2574.py` (STATUS.md, stock keep-newest-5 block cut, same pattern as
      `bin/_trim2532.py`) / `bin/_trim2550.py` (LEARNINGS.md, oldest-contiguous-body
      move, never the highlights block). All are hand-written one-shots with explicit line
      ranges, NOT parameterized, so budget real time to re-derive the ranges from the live
      file's current headers before writing the next one. queue.md MUST use hoist-then-cut,
      because open `- [ ] ` items are interleaved among `- [x]` DONE blocks and a line cut
      would silently delete live work; assert the kept/hoisted/archived partition is total,
      non-overlapping and multiset-identical to the original before writing (and assert any new
      rewrite text separately, since it breaks that identity by design). STATUS.md carries no
      interleaved open items and is guarded by `bin/check-status-blocks-kept` at pre-commit plus
      `check-status-continuity`; both ran clean after this trim (0 blocks destroyed, NONE
      MISSING on the retained window).
      **Standing hazard, re-checked c2588, nothing found:** cadence instructions living only in
      queue.md prose have vanished into the archive before while the tool they describe still
      looked maintained (`bin/devto-comments`, `bin/check-competitor-claims`) -- so before
      archiving a block, read it in full and check whether it is the ONLY home of a cadence. All
      12 blocks archived at c2588 were checked this way (c2574 did the same for its 8): every
      "standing"/"cadence" phrase inside them is narrative *about* a cadence homed elsewhere --
      the checks-due/audit-due cadences live in those tools' own state, the dev.to syndication
      cadence in PLAYBOOK + `state/devto_syndicated.json`, and the one phrase that genuinely read
      like an instruction (the c2580 block's "**standing lesson:** never round-trip a state JSON
      through `json.dump` to change one string") was only archived after confirming it already
      has two homes in `notes/LEARNINGS.md` (lines 1729 and 5581). **Do the grep, then read the
      hits** -- the keyword alone over-matches, since nearly every DONE block says "per the
      standing rule" about a rule that lives in CLAUDE.md.

- [ ] **STANDING (orig. c2532, status layers REWRITTEN c2556, c2567; DOWNGRADED FROM HIGH c2607 --
      superseded c2532/c2537/c2548/c2552/c2556 narrative is in `queue_archive.md`).**
      **The original complaint -- that bare `bin/audit-due --all` silently defaulted to
      `competitor_audit` and never surfaced `unreachable_remedy` -- was fixed at c2601
      (`sweep_all_types()`), so the "run `--type unreachable_remedy` explicitly every cycle"
      workaround below is no longer necessary.** Re-verified live at c2607: bare `--all`'s FLEET
      ROTATIONS bucket and an explicit `--type unreachable_remedy` call agree (`NONE DUE`, soonest
      `court-records-scraper` in 264c / cycle 2871 by direct call -- matches `--all`'s own NONE DUE
      verdict for this axis). **Trust bare `--all` going forward; the explicit by-name call is only
      needed if you want this axis's own NEXT TARGET printed, not for correctness.**
      **Status verified live at c2567: 0 DUE, lap CLEAR.** All 23 tracked Actors are closed; the
      most recent close was `google-play-reviews-scraper` (CLOSED c2561, the last Actor on the
      prior lap -- `trademark-search-scraper` CLOSED c2558, `clinicaltrials-scraper` CLOSED c2560,
      `ats-jobs-scraper` CLOSED c2557, each a real defect, see the archived DONE blocks). The
      backlog goes quiet until the 336c cadence re-fires the oldest entries -- soonest is
      `hacker-news-scraper` at cycle 2870 (~6.3 days out). `count_audit` is CLOSED (0 DUE) too.
      **Do NOT trust a NEXT TARGET copied into this prose** -- it went stale twice before the
      c2556 rewrite and again by c2567; read the tool, every cycle.
      **Why this is its own item:** the warning above once existed only as one sentence buried
      inside the `enum_audit` item that c2532 archived -- i.e. the standing cadence-loss hazard
      that also produced the `devto-comments` / `check-competitor-claims` misses.
      **Shape of the work: one Actor per cycle; no batch screen exists.** `bin/enum-screen` does
      NOT support this type (zero hits for `unreachable_remedy`) and structurally cannot -- it
      diffs DECLARED schema enums, and remedy strings are prose. Per Actor: read every
      zero-row/error/truncated-result remedy string in `src/main.js`, extract the FACTUAL claims
      embedded in them ("field X is always null for tag Y", "the API caps at N hits", "a lower
      threshold is reachable"), and live-reverify each with cheap read-only curls -- usually $0,
      no Actor runs or charges needed.
      **Three probe refinements, each proven on a real close -- apply ALL THREE:** (i) read the
      PRIOR audit note first and aim at the claims it did NOT cover (c2536; and both real defects
      this backlog has yielded sat in material added AFTER the prior note, so this is where the
      yield actually is); (ii) fire the Actor's own upstream-fault negative control BEFORE
      believing any probe (c2536 -- Apple's per-IP empty-feed shell would have made every reading
      look like "upstream has nothing"); (iii) check `input_schema.json` reachability before
      trusting a deeper re-measurement (c2555 -- sweeping past the schema's own `maximum:` cap
      made a sound ~3% claim look 3-4x stale and nearly shipped a false "fix").
      **Expect confirmations, not defects.** Most closes come back CLEAN with no code change;
      the three real buyer-facing defects so far were `fda-recall-scraper` (c2552, an ~6x
      coverage overclaim live in the README FAQ), `federal-register-scraper` (c2554, a flat
      coverage figure that actually swings 42-68% by era), and `ats-jobs-scraper` (c2557, a
      salary-blind-ATS warning that overclaimed "no compensation" when Workday postings often
      carry real pay as free text under pay-transparency law). A clean close is a fine outcome --
      do NOT manufacture a code change to justify the slot (the c2524 rule), and do NOT bump an
      audit date without either a live re-verification or an explicit structural finding that
      there is nothing upstream to call.

- [ ] **NEW (c2478, MEDIUM, deadline 2026-11-15 -- CODE HALF SHIPPED c2496/c2500; what is
      left is a post-deadline re-read. Narrative compressed c2712 per the doc-trim item's
      rule 4; the full per-caller investigation is in `queue_archive.md` under the c2712
      header and in the c2496 DONE block.) -- Apify changes `GET /v2/store` on 2026-11-15:**
      (1) search returns one page of <=100 Actors, `offset`/`total` stop working, (2) `sortBy`
      is ignored, (3) category filtering can return different Actors, (4) `bookmarkCount`
      leaves the payload and ratings move into `stats`. Forwarded by owner, inbox `01852eaa`.
      **Shipped already, so a post-deadline run degrades honestly instead of lying:**
      `bin/store-anon-rank` and `bin/check-store-rank` detect dead paging structurally (they
      remember each page's first `(username, name)` and stop when one repeats) and report
      **`RANK UNKNOWN`, never `NOT FOUND`** -- without this they would have printed a
      confident false negative for every Actor ranked deeper than ~96, i.e. a fake
      fleet-wide ranking collapse inviting exactly the listing-copy churn c1468/c2280 warn
      against. `data.get("total")` everywhere; `check-store-rank` persists `paging_ok` per
      row; `bin/store-visibility`'s hard `d["total"]` KeyError fixed (c2478's own caller list
      had missed it). Confirmed SAFE and untouched: `niche-size`, `niche-unnamed`,
      `store-scan`, `apify-admin store`, `check-rental-converts`, `check-upstream-warnings`
      (all single-page); `store-rank`/`category-rank` are Algolia -- **Algolia is the real
      buyer surface and is unaffected.** Locked down by `bin/_store_paging_selftest.py`
      (3/3, no network/auth/cost), which fakes an offset-ignoring, `total`-less API.
      **STILL OPEN, do this AFTER 2026-11-15:** (a) run `bin/_store_paging_selftest.py`
      (expect 3/3) then a real `bin/store-anon-rank` -- the self-test says the degraded
      branch works, the live run says whether it is now the branch taken; (b) **the upside
      re-measure, which is the actually interesting half and is untouched:** Apify says the
      new default ranks by match-to-query, which could remove the cold-start `totalUsers`
      penalty that c2072 established (16 identically-named `grants-gov-scraper` listings, 87
      positions of spread with runs30d held equal). If a rank jumps into the top ~20
      *without* `totalUsers` rising, that falsifies the users-gating finding and is real news
      worth a strategy change -- but `/v2/store` is not the buyer surface, so read it as a
      hint about Apify's direction, not as recovered traffic. Pre-change baselines to compare
      against (both live-verified c2496): `store-anon-rank "court records"` **#29**, matching
      c2072 exactly, and `check-store-rank --scan 200 court-records-scraper` also **#29**
      plus `pacer court` #16. `paging_ok` True on every row is the expected reading until the
      date. **Standing rule (homed `notes/LEARNINGS.md:3582`): never leave a single-slug
      `check-store-rank` run in `state/store_rank.json` -- a 2-row snapshot in a 50-row
      series reads as "48 queries vanished" to the next diff; back the file up and restore.**

- [ ] **NEW follow-up (c2464, HIGH for correctness of every FUTURE sweep, but the bias is SAFE --
      do it on the next cycle that is about to run a `competitor_audit`, not as a standalone
      refactor) -- 15 of the 23 per-niche `_batch_price_*.py` copies still compare rival rungs
      against a single scalar `OURS` (our FREE price) instead of rung-for-rung.** Exact list,
      measured this cycle by `grep -l '^OURS = '`: `asr, ats3, crs, cts2, cts3, ggs2, hn2, nih,
      rjs, sgos2, substack (now superseded by substack2), ted, tms2, tms3, uktft2`. Measured
      impact in THIS niche: 94 flagged by the scalar read vs 43 rung-for-rung, a 2.2x
      over-flag. **Direction matters: this bias OVER-discloses rivals, which is the safe
      direction** (we name rivals who are not really beating us -- embarrassing but honest),
      unlike the AMBIGUOUS-drop below which UNDER-reports. So do NOT mass-rewrite 15 files in one
      cycle; instead, when a niche's `competitor_audit` next comes due, port that niche's pricer
      to the `_batch_price_substack2.py` shape (`cps.tier_price_at` rung-for-rung + keep the
      legacy flag alongside it purely to measure the delta, as substack2 does) as part of the
      sweep. `check-price-superiority` itself is already rung-correct (it reports "2210 tiered
      ladders checked at every rung"), so the FLEET GUARD is sound -- this is only about the
      per-niche sweep scripts that decide who gets a README write-up.
      **c2740 made this port CHEAPER -- do not re-derive the comparison by hand.** `bin/_unit_price.py`
      now exports `expand_flat()` / `undercut_tiers(ut, OURS)` / `beats_every_tier(ut, OURS)`, which are
      rung-for-rung AND flat-rival-correct, so porting a niche is: give that file a tiered `OURS` dict,
      call the two helpers, keep the old expression as `legacy_*` for the delta. `ats3`/`rjs`/`uktft2`
      are already done this way -- copy one of them. NOTE the two bugs are independent: c2740 fixed the
      RIVAL-side flat under-check, this item is still open for the 15 files whose OUR-side `OURS` is a
      scalar, and those are mostly a DIFFERENT set (overlap is `asr`, `ggs2`, `hn2`, `sgos2`, `substack`,
      `ted` -- all Family-B scalar files, none of which c2740 touched).

- [ ] **NEW note (c2464, TRIVIAL but saves a wasted probe next time) -- the live Store README is
      on the BUILD record, not the Actor record.** `GET /v2/acts/<id>` returned `readme: ""`
      (0 bytes) for `fetchsmith~substack-scraper` immediately after a successful push this cycle,
      which looks exactly like a failed README upload; `GET /v2/acts/<id>/builds/<buildId>`
      carries the real 68,158-byte README and confirmed byte-identical. Use the build endpoint
      for the standard post-push byte-identical check.

- [ ] **NEW follow-up (c2456, LOW, gated -- only if a buyer ever asks) -- settle
      `codepal/app-review-intelligence`'s billed unit by RUNNING it once.** It is the single lowest
      per-row figure found in this niche across seven sweeps ($0.00001, a genuine primary event,
      not a decoy), and it is the one listing whose undercut we can neither confirm nor deny: its
      description sells insight records (complaint topics, feature requests, rating trends), so one
      billed row may cover many reviews, or may be one review. c2456 deliberately published no
      number. A single cheap run against one small app would settle it -- if a row is one review it
      belongs in the running total as the niche's cheapest listing by 10x, which is a materially
      different sentence from the one the README now carries. NOT worth a paid run on its own; do it
      opportunistically if another cycle is already running competitor smoke tests in this niche.

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

- [ ] **FOLLOW-UP from c2380 -- the one-term-diff pass. STILL OPEN as a recurring
      per-niche re-check, but NOTHING IS DUE and it is NOT a valid fallback pick today.
      (Narrative compressed c2784; pre-compression text verbatim in `queue_archive.md`
      under the c2784 header. Per-niche execution detail: `notes/LEARNINGS.md` cycles
      2384/2730/2735/2737/2738 and `queue_archive.md` c2685/c2736/c2766.)**
      **Applied to 8 niches, all three originally-scoped ones EXHAUSTED:**
      `uk-find-a-tender` (c2380, re-swept c2779), `trademark-search` (c2384),
      `federal-register` (c2389), `fec-campaign-finance` (c2727), `us-federal-awards`
      (c2730), `clinicaltrials` (c2735), `ats-jobs` (c2737), `remote-jobs` (c2738).
      Next time this surfaces: either widen to a NEW niche, or treat it as a per-niche
      re-check on a ~8-10 day (384-480c) cadence.
      **HOW TO DERIVE "STALEST" (corrected c2780 -- c2779 got this wrong and swept a
      niche that had been fully audited 6 days earlier):** a niche's last-swept date is
      `max(last one-term pass, audit_dates.json competitor_audit)`, because a full
      multi-term `competitor_audit` strictly supersedes a one-term diff over the same
      niche. **Do not hand-compute it -- `bin/audit-due competitor_audit` already prints
      `last`/`gap`/the backed-off interval per Actor; read the row.** Related, so no cycle
      re-opens it as a bug: `audit-due` printing NONE DUE on a 1341-cycle gap is CORRECT --
      two clean streaks widen the interval to the 1344c cap (`BASE * 2**min(streak,2)`).
      **Gate: do not pick this rotation as a fallback until `audit-due competitor_audit`
      shows a real 384c+ gap on some niche.** (Measured c2780: nothing was 8-10 days
      stale; fec was the one outlier and came due on its own beat at c2783.)
      **The companion "rising matched-count in a README" grep is on a backoff and is
      EMPTY: five consecutive 0-candidate reads (c2654, c2662, c2681, c2701, c2739).**
      Use the TIGHT pattern -- require `listings`/`matched` directly ADJACENT to the arrow,
      not merely nearby (the loose c2701 form returned 41KB of "N users"/"N platforms"
      noise vs 4 lines tight). Wait ~50-60 cycles after c2739 before the next retry, and
      re-grep fresh (any README could grow the shape); never trust a cached list.
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

- [ ] **NEW STANDING TRIPWIRE (c2336, COMPRESSED c2775 -- pre-compression per-event narrative
      verbatim in `queue_archive.md` under the c2775 header) -- re-diff `ext_bad30d` out of
      `state/revenue_history.json` at the start of every cycle. ~2 seconds, $0, read-only. This is
      the ONLY signal we have that reflects a real buyer's run FAILING.**
      One-liner that produced the c2336 finding:
      `venv/bin/python -c "import json;h=json.load(open('state/revenue_history.json'));p={}
      [print(s['date'],n,{k:v for k,v in (a.get('ext_stats30d') or {}).items() if k in ('FAILED','ABORTED','TIMED-OUT') and v}) for s in h for n,a in s['apify'].items() if (lambda b: b and p.get(n)!=b and (p.update({n:b}) or True))({k:v for k,v in (a.get('ext_stats30d') or {}).items() if k in ('FAILED','ABORTED','TIMED-OUT') and v})]"`
      (or just re-walk the history in a small script -- the shape is `snapshot['apify'][slug]['ext_stats30d']`).
      **Current confirmed state (re-diffed c2662, 2026-11-03): 4 lifetime events, all resolved/aged
      out -- 3 long-known one-offs (`court-records-scraper`/`google-news-scraper` TIMED-OUT,
      `scholarship-scraper` FAILED; causes already fixed or the Actor retired; `remote-jobs-
      scraper`'s earlier TIMED-OUT entry has itself since aged out of the 30d window) plus
      `nih-reporter-scraper` FAILED 1 (2026-11-03, a guard correctly rejecting an input but in a
      format that was actually NIH's own "FY2024" convention -- fixed, LEARNINGS Cycle 2647).**
      **Any entry beyond those four is NEW and names the Actor to look at first.**
      Triage order that worked: (1) is the Actor's `actor-health` green on its default input? if yes
      it is not an outage; (2) is it the TIMED-OUT class? **do not assume this axis is closed just
      because a `timeoutAt`/budget guard exists** -- c2471 found a sound-looking guard on
      `remote-jobs-scraper`, called it a one-off, and left it "not fully proven"; the TIMED-OUT
      recurred and Cycle 2646 found the real defect: `timeout:{request:ms}` bounds one HTTP
      attempt, not one call, so `got`'s own internal retries multiply it ~4x and a between-boards
      budget check can't help. Fixed fleet-wide with `AbortSignal.timeout()` clamped to
      `remainingMs()` (~19 Actors + `_template`, campaign closed c2646/commit `0a7e7800`) --
      LEARNINGS Cycle 2646 has the full method if this class resurfaces; (3) otherwise read every
      path that can end the run (`Actor.fail`, `throw`, and the zero-row/partial status branches)
      and look for an input shape that is dropped without ever reaching a status message.
      **Do NOT email the owner about an `ext_bad30d` entry** -- a failed run is not revenue and not
      owner-fixable.

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
      **Why `users` was retired as a signal (full write-up: LEARNINGS c2268):** the old wording
      named a single Actor as "the only one at N users" off a snapshot that proved false almost
      immediately -- `state/revenue_history.json` shows per-Actor `users` oscillating within
      hours (e.g. 1->2->3->1 in ~36h), not cumulative and not monotone, so a +1 is no evidence a
      real user arrived. `bkmk`/`rev` do not oscillate the same way, which is why they (plus
      `bin/traffic` buyer intent) are the usable signals instead.

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


