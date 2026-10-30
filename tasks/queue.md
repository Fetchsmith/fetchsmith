- [x] **DONE cycle 2485 (normal slot, `2485%3==1`) -- ran the backlog's NEXT TARGET,
      `court-records-scraper`'s `competitor_audit` (last 2141, 343c gap). NOT CLEAN: 2 genuine
      new in-scope undercutters + 4 jurisdiction-excluded undercutters.** Git-log hidden-resweep
      check first (c2477 rule): only commits since 2141 are disclosure-only/feature work (billing
      clamp, unknown-court-id disclosure, mode-scope warning, closing 3 `check-competitor-claims`
      flags), none a full-cohort resweep -- gap genuinely real. Own price re-read live: flat
      $0.002/result, single primary `result` event, `eventTieredPricingUsd` absent, no start fee
      -- c2464 scalar-vs-rung bug does not apply, `bin/_batch_price_crs.py`'s flat `OURS` already
      matches. `niche-size` 160 matched (up from 156), 6,817 seen. `niche-unnamed` 67 unnamed (8
      NONE, 59 OWNER incl. self), all 66 non-self handles live-priced, 0 unresolvable. 2 in-scope
      undercutters: `rbbscrap/fast-courtlistener-docket-scraper` ($0 FREE model, federal PACER
      dockets only, narrower than our dockets+opinions scope), `parseforge/
      courtlistener-civil-cases-scraper` (dearer Free/Bronze/Silver, crosses under on
      Platinum/Diamond, civil-dockets-only). 4 out-of-scope-but-cheaper on jurisdiction:
      `orange_briefcase_hrj/austria-case-law-search` + `.../german-case-law-search` (new vendor,
      Austria+Germany, every tier), `jungle_synthesizer/canlii-canadian-case-law-scraper` (Canada,
      Silver up), `steadfetch/cendoj-jurisprudence-monitor` (5th Spanish CENDOJ rival, every
      tier). 4 more NONE handles dearer/different-product (`nabeelbaghoor`, `groundplanes`,
      `enterprising_hamster` [Poland, new country, dearer], `tudorlane/adverse-media-watch` [KYC
      screening, not court records]). Remaining 57 of 66 dearer, already covered by an owner
      named above. Shipped README-only build 0.1.74 (package 0.1.24 -> 0.1.25); live README
      byte-identical (71,440 bytes). Guards clean: `check-price-superiority` 2454/933/0
      undisclosed (up from 2444/929), `check-charges` 25/0/0, `check-registry-fields` 0 drift,
      `check-own-price-prose` 0 flags. Recorded in `audit_dates.json` (2141 -> 2485). Backlog now
      **3 DUE**, next target `clinicaltrials-scraper` (last 2144, 341c gap). No new mail, no
      revenue change, no owner email (CLAUDE.md rule 3). ~$0.005 spent (one build), 0 new Actors
      today. Full detail in `state/STATUS.md` cycle 2485.

- [ ] **NEW (c2478, MEDIUM, deadline 2026-11-15 -- not urgent today, but must be checked again before that date and again shortly after) -- Apify is changing `GET /v2/store` search behavior on 2026-11-15** (forwarded by owner, inbox `01852eaa`, from Apify's own product-marketing mail): after that date, (1) search returns one page of up to 100 Actors and `offset`/`total` no longer work for paging, (2) `sortBy` is ignored, (3) category filtering can return different Actors, (4) `bookmarkCount` is removed from the payload and ratings move into `stats`. **Investigated this cycle which fleet tools actually call `/v2/store` (not Algolia) and are exposed:**
      - **`bin/store-anon-rank`** -- genuinely broken by this: it pages `/v2/store?search=` with `offset` to find our exact position (we sit anywhere from #29 to #354 on core terms per its cycle-2072 baseline), so after 2026-11-15 it can only see page 1 (first ~100) and will misreport "not found" for anything ranked deeper, the same false-negative shape its own docstring already warns about. `checks-due` has it next due cycle 2744 (~2026-11-05, before the change) so the next scheduled run is still safe, but the run AFTER that (~336 cycles later, after the deadline) needs the paging logic revisited first -- note it in that cycle rather than trusting a sudden empty-looking result. **Possible upside worth re-checking, not just a break:** cycle 2072's decisive finding was that Store search rank is gated on `totalUsers` (16 identically-named `grants-gov-scraper` listings proved it, 87 positions of spread with runs30d held equal) -- Apify's own mail says the new default **ranks by match-to-query instead**, which could remove exactly the cold-start penalty that finding is built on. Worth a fresh `store-anon-rank` read once the change is live, not just a mechanical pagination fix.
      - **`bin/check-store-rank`** -- same `offset`/`total` paging pattern (`--scan` loop), but its own docstring already labels this a MINOR, non-buyer-facing surface (the real buyer surface is Algolia via `bin/store-rank`, unaffected -- confirmed this cycle it hits `algolia.net` directly, not `/v2/store`). Lower priority; same "re-check before trusting a post-2026-11-15 run" caveat applies.
      - **Confirmed SAFE / no action needed:** `bin/niche-size` and `bin/niche-unnamed` (the tools every `competitor_audit` sweep depends on) deliberately fetch ONE page per search term and never loop on `offset` -- a cycle-1779 lesson already in the code comments, written for an unrelated reason (Algolia offset staleness) but it happens to make them immune to this change too. `bin/store-scan` single-page, no offset. `bin/apify-admin store` / `bin/check-rental-converts` pass `sortBy=relevance` but don't page past one call -- losing that param just means the platform's own new default ranking applies, not a break. No script reads `bookmarkCount` (grepped fleet-wide) or a bare `rating` field from `/v2/store`.
      **No owner email needed** (nothing only the owner can fix, no revenue event) and no urgent fix needed today (16-day runway, nothing in the automated `checks-due` cadence hits the broken path before the deadline) -- but do NOT let this fall off the queue. Next action: when `store-anon-rank` or `check-store-rank` next come due AFTER 2026-11-15, read this note first and patch the offset-pagination loop (e.g. cap at page 1 and report "ranked beyond page 1, exact position unknown" instead of silently misreporting) before trusting the output.

- [ ] **NEW (c2484, LOW-MEDIUM, cheap) -- a README's LEAD niche-size claim can go stale for weeks
      even while the Actor is being audited, and `bin/niche-size` already prints the evidence.**
      Found during c2484's `trademark-search-scraper` sweep: the Pricing section's lead paragraph
      still said "114 Store listings mention trademarks (543 distinct seen)" from **2026-10-06**,
      i.e. it survived the c2139 sweep (which wrote its new 145-matched figure into a NEW dated
      paragraph lower down instead of correcting the lead) and the c2384 recheck. `niche-size`
      printed `README claims: 114 (DIFFERS by +40)` on every run in between -- the signal was
      there and nobody acted on it, because the append-a-dated-paragraph convention makes it easy
      to add a fresh count without touching the stale one above it. Fixed for this Actor in c2484.
      **Next action (one QUALITY slot, ~15 min, $0, no builds):** run `bin/niche-size <slug>` across
      the fleet, collect every Actor whose `README claims: N (DIFFERS...)` line is non-trivially off,
      and fix the LEAD claim in each (correcting in place with the superseded figure named, per the
      standing "correct rather than quietly re-date" rule). If more than a couple are stale, promote
      the DIFFERS line into a real fleet check in `state/fleet_checks.json` so it has a cadence
      instead of depending on an audit happening to read it -- note that the per-Actor sweep
      rotation is 336c+, so a lead claim can currently rot for ~300 cycles between looks.

- [x] **DONE cycle 2484 (normal slot, `2484%3==0`) -- ran both DUE fleet checks
      (`check-row-floor` CLEAN: 24 live Actors, all >=60% of requested cap, none declined from
      its own observed best; `check-upstream-warnings` CLEAN: 23 niches, 10,917 listings seen /
      5,968 in-niche, 0 new upstream shutdown/deprecation/migration copy, same 7 acknowledged
      hits with unchanged fingerprints), then the backlog's NEXT TARGET,
      `trademark-search-scraper`'s `competitor_audit` (last 2139, 345c gap). NOT CLEAN: 1
      genuine new undercutter.** Git-log hidden-resweep check first: the only commits touching
      this Actor since 2139 are c2384's one-term recheck and c2405's user-count fix, neither a
      full-cohort sweep, so per the c2477 rule the formal gap stood. Own price re-read live
      before comparing: flat $0.002/result on every tier, single primary `result` event,
      `eventTieredPricingUsd` ABSENT, no start fee -- c2464 scalar-vs-rung bug does not apply.
      `niche-size` 2,401 distinct seen / **154 matched** (up from 145); the README lead
      paragraph still claimed 114-of-543 from 2026-10-06 and was corrected in place (see the
      NEW item above, which generalises this). `niche-unnamed` 9 never-named handles (7 NONE, 2
      OWNER), **all 9 live-priced via `_batch_price_tms3.py`, 0 unresolvable, 0 AMBIGUOUS**,
      both OWNER handles re-priced under their own Actor IDs rather than inheriting a sibling's
      verdict. The undercutter: **`alexmorain/inpi-trademark-scraper`**, $0.001 (FREE) /
      $0.00085 (BRONZE) / $0.0007 (SILVER) / $0.0005 (GOLD+) + $0.002 start, crossover ~2 rows
      -- France's INPI register (FR + EU + international marks with French effect), **runs on
      the buyer's own free INPI account** where we are keyless, one office vs our 70+. 5
      in-scope and dearer at every tier (`olliolli/eu-trademark-watch` $0.03+$0.05 start and
      the closest to us by source; `atesen-software/trademark-phrase-risk-check` $0.05/phrase;
      `chaptersoft/trademark-watch` $0.01->$0.008; `maliksaid/uspto-trademark-watch` $0.006;
      `barefoot_grade/uspto-trademarks-scraper` $0.004+$0.005 start). 3 out of scope on their
      own descriptions, only ONE of them even cheaper per unit
      (`ahmed_jasarevic/importyeti-scraper` $0.0012->$0.0011 but customs bill-of-lading
      profiles with "trademarks" as one field, same exclusion as
      `crawlerbros/importyeti-scraper`; `vncntlabs/amazon-book-tshirt-niche-analyzer` $0.15;
      `parseforge/colorado-business-registry-scraper` $0.0045->$0.0024). **PRICE HELD flat
      $0.002** -- the 2026-10-16 revisit trigger did NOT fire (it needs a MULTI-OFFICE
      undercutter, a `foxlabs` cut, or an undercutter crossing 20 users; this one is
      single-register at the 2-user floor with a buyer-credential requirement we lack). Shipped
      README-only build **0.1.87** (package 0.1.24 -> 0.1.25), live README byte-identical
      (79,458 B, md5 match) via the `versions/0.1` `sourceFiles` endpoint per the c2482 gotcha.
      Guards clean: `check-price-superiority` 2,444/929/**0 undisclosed**, `check-charges`
      25/0/0, `check-registry-fields` 0 drift, `check-own-price-freshness` 25/0,
      `check-own-price-prose` 0 flags. Recorded in `audit_dates.json` (2139 -> 2484); backlog
      5 -> **4 DUE**, next target **`court-records-scraper`** (last 2141, 343c gap).

- [x] **DONE cycle 2482 (normal slot, `2482%3==1`) -- ran the DUE fleet check
      `devto-comments` (clean: 26 published, 8 with comments, 14 inbound, 0 unanswered, 1
      spam-skipped), then the backlog's NEXT TARGET, `sam-gov-opportunities-scraper`'s
      `competitor_audit` (last 2135, 347c gap). NOT CLEAN: 9 genuine new undercutters, the
      largest single-sweep haul this niche has had since 2026-10-23.** Git-log hidden-resweep
      check first: all commits since 2135 are feature work (incumbent-award lookup, date-window/
      solicitation-number/status-clamp fixes), gap was real. Own price re-read live: flat
      $0.0015/row, no start fee, `eventTieredPricingUsd` ABSENT -- c2464 bug doesn't apply.
      niche-size 278 matched (up from 229); `niche-unnamed` 184 unnamed (167 NONE/17 OWNER), all
      167 NONE live-priced via `bin/_batch_price_sgos2.py` (0 unresolvable, 3 AMBIGUOUS hand-read,
      all dearer), all 17 OWNER handles re-priced under their own IDs (16/17 dearer, 1 out of
      scope). 9 new undercutters: `tidyflowlabs/samgov-opportunities` (every tier $0.0012->
      $0.0008), `chaptersoft/gov-contract-opportunities` (every tier $0.0005->$0.00035),
      `openwell-data/federal-contract-opportunity-monitor` (FREE, real $0), `loomwise/federal-
      opportunities` ($0.0009+$0.00005 start), `barefoot_grade/sam-gov-opportunities-scraper`
      ($0.001+$0.005 start, crossover ~row 10), `actor-forge/public-tenders` ($0.0012+$0.00005
      start, SAM.gov needs buyer's own key), `jpopendata/us-sam-opportunities` (GOLD+ only),
      `capable_coach/sam-gov-contract-opportunities` (BRONZE+), `clearpath-data/us-federal-
      contract-opportunities` (SILVER+). 1 ruled out by scope (`jpopendata/us-federal-spending`,
      USAspending awards not SAM.gov opportunities). Shipped README-only build 0.1.83 (package
      0.1.27 -> 0.1.28). **New gotcha: the build record's own `readme` field silently truncated
      at 100,566 bytes for this large file -- had to use the `/v2/acts/<id>/versions/0.1`
      `sourceFiles` endpoint instead to get a true byte-identical check (113,094 bytes both
      sides).** Guards clean: `check-price-superiority` 2425/918/0 undisclosed (up from
      2411/911), `check-charges` 25/0/0, `check-registry-fields` 0 drift,
      `check-own-price-freshness` 25/0, `check-own-price-prose` 0 flags. Recorded in
      `audit_dates.json` (2135 -> 2482). Backlog now **5 DUE**, next target
      `uk-find-a-tender-scraper` (last 2137, 345c gap). No new mail, no revenue change, no owner
      email (CLAUDE.md rule 3). ~$0.005 spent (one build), 0 new Actors today. Full detail in
      `state/STATUS.md` cycle 2482.

- [x] **DONE cycle 2481 (normal slot, `2481%3==0`) -- ran the backlog's NEXT TARGET,
      `federal-register-scraper`'s eighth `competitor_audit` pass (last 2131, 349c gap). HOLD
      $0.0008/result, quietest sweep this Actor has had: 0 of 107 live-priced listings
      undercuts us.** Git-log hidden-resweep check first (c2477 rule): only the already-excluded
      c2389 one-term spot-check touched this Actor since 2131, gap was real. Own price re-read
      live: flat $0.0008/result, no start fee, `eventTieredPricingUsd` ABSENT (confirmed
      `bin/_batch_price_fedreg.py` has no hardcoded `OURS` scalar either, so the c2464 bug doesn't
      apply). Fresh niche-size: 165 matched (up from 151). `niche-unnamed`: 108 unnamed (96 NONE,
      12 OWNER), all 107 non-self handles live-priced, 0 unresolvable. Only headline-cheap
      candidate (`tali-works/faa-airworthiness-directive-monitor`, $0.0005/item) ruled out on
      scope -- FAA ADs, not Federal Register documents. All 12 OWNER-section handles re-priced
      live under their own handles per the c2475 lesson; none in scope and cheaper (closest,
      `v0iddo/us-executive-orders-tracker`, is 12.5x dearer). Shipped README-only build (package
      0.1.16 -> 0.1.17, build 0.1.65), live README byte-identical (47,052 bytes). Guards:
      `check-price-superiority` 2411/911/0 undisclosed, `check-charges` 25/0/0,
      `check-registry-fields` 0 drift, `check-own-price-prose` 0 flags. Recorded in
      `audit_dates.json` (2131 -> 2481). Committed `d88a34aa`. Backlog now **6 DUE**, next target
      `sam-gov-opportunities-scraper` (last 2135, 346c gap). No new mail, no revenue change, no
      owner email (CLAUDE.md rule 3). ~$0.005 spent (one build), 0 new Actors today. Full detail
      in `state/STATUS.md` cycle 2481.

- [x] **DONE cycle 2480 (QUALITY/GROWTH slot, `2480%3==2`; ran a sweep because `audit-due`
      showed 7 DUE, per the c2474/c2477 precedent that sweeps count as quality work) -- ran the
      confirmed NEXT TARGET, `apple-podcasts-scraper`'s `competitor_audit` (last 2121, 359c gap).**
      Hidden-resweep check first per the c2477 rule: `a7f825ff` (cycle 2457) postdates `last=2121`
      but is a **one-term recheck**, not a full-cohort resweep, so it does not retire the formal gap
      -- sweep was genuinely due. Own price re-read live FIRST: flat **$0.001/result, no start fee,
      `eventTieredPricingUsd` ABSENT** -> the c2464 scalar-vs-rung pricer bug does not apply here
      (c2474/c2476 precedent), verified not assumed. Niche grew to **1,011 seen / 166 matched** (up
      from 919/135) but the unnamed cohort **SHRANK 34 -> 19** because c2457's one-term recheck had
      already named 17 of them; all **18** non-self handles live-priced via `bin/_batch_price_apc.py`
      (18/18 resolvable). **5 new undercutters, all at the 2-user floor:**
      `deriverge/podcast-episodes-scraper` (episodes-only, $0.0005 -> $0.00025, no start fee,
      **cheaper at EVERY tier, 50-75% under**), `ucchiii/podcast-rss-episodes` (tie at FREE then
      $0.0009 -> $0.0007), `maydit/apple-podcast-discovery-monitor` (tie FREE+BRONZE, undercuts
      $0.0008 SILVER / $0.0006 GOLD+ + $0.00005 start -- plan-tier crossover), plus episode-row-only
      partials `yiafirm/podcast-monitor` ($0.0004/episode) and `deriverge/podcast-charts-scraper`
      ($0.0005 -> $0.00025/episode). **3 in-scope rivals hand-read and ruled NOT undercutters:**
      `barefoot_grade/apple-podcasts-scraper` (closest whole-product match this sweep but $0.0014/row
      = 40% dearer + $0.005 start fee), `h1018y/anvil-podcast-videos` (5.6-7.5x dearer),
      `nabeelbaghoor/podcast-data-api` (Podchaser BYO-key, 5-20x dearer). Remaining 10 are the
      standing transcription-per-audio-minute (7) and guest-booking/email lead-gen (3) exclusions,
      every one dearer on any unit. **All 6 OWNER-section handles re-priced under their own handles
      per the c2475 lesson** -- that is what caught both `deriverge` listings and the
      `tidydata`/`wearefluent` pair as distinct Actor IDs from their already-named siblings (3 of the
      5 undercutters). **HOLD $0.001** (every undercutter at 2u; trafficked listings `ryanclinton`
      207u / `automation-lab` 124u / `sourabhbgp` 71u did not move -- growth still entirely at the
      1-2-user floor). Shipped README-only build **0.1.111** (pkg 0.1.33 -> 0.1.34), live README
      **byte-identical** (65,376 B, md5 `eee5602674d9ae1c635dc43b33cf0720`) via the
      `/v2/acts/<id>/versions/0.1` sourceFiles endpoint. Guards clean: `check-price-superiority`
      2409 compared / 910 cheaper / **0 undisclosed fleet-wide** (up from 2391), `check-charges`
      25/0/0, `check-registry-fields` 0 drift, `check-own-price-prose` 0 flags,
      `check-own-price-freshness` 25/0. Recorded in `audit_dates.json` (2121 -> 2480). Backlog
      **7 -> 6 DUE**, next target `federal-register-scraper` (last 2131, 349c gap). ~$0.005 spent,
      0 new Actors, no new mail, no revenue event, no owner email (CLAUDE.md rule 3). Full detail in
      `state/STATUS.md` cycle 2480.

- [x] **DONE cycle 2479 (normal slot, `2479%3==1`) -- finished the `ats-jobs-scraper`
      `competitor_audit` cycle 2477 left half-done (data gathered, pricing not started).
      Full >=3-user cohort (290 listings, up from 256 at 1805), live-priced via
      `bin/_batch_price_ats3.py`, 0 unresolvable.** 13 genuine new undercutters (all
      single/dual-platform, narrower than our 10-platform scope) + 1 free whole-product
      match (`tomstudio/ats-jobs-scraper`, $0). 10 every-tier undercutters (biggest by users:
      `jobo.world/ashby-jobs-scraper-api` 194u $0.00099 flat), 2 cross-under-everywhere-
      except-FREE (`deriverge` pair, `hipersoft/smartrecruiters-scraper`), 1 FREE listing
      read and ruled out as lead-gen/AI shape (`enosgb/ats-job-intelligence-api`). Build
      0.1.112, live README byte-identical (77,863B). Guards clean: `check-charges` 25/0/0,
      `check-registry-fields` 0 drift, `check-own-price-prose` 0 flags,
      `check-price-superiority` 2391 compared/0 undisclosed fleet-wide. `audit_dates.json`
      recorded (1805 -> 2479). Committed `16657950`. Backlog now **6 DUE**, next target
      `apple-podcasts-scraper` (last 2121, 358c gap). Full detail in `state/STATUS.md`
      cycle 2479.

- [x] **DONE cycle 2477 (data-gathering half; superseded by the full close above) -- started
      `ats-jobs-scraper`'s `competitor_audit` (last 1805, 672c gap), data-gathering half done,
      pricing half not started.** `check-own-price-freshness` 25/0 (no drift). Fresh `niche-size
      ats-jobs-scraper`: **2019 matched** (up from 1,479 at c1805), 3694 seen across 15 queries.
      `niche-unnamed ats-jobs-scraper`: **1926 unnamed of 2019** (1771 NONE, 155 OWNER) -- too
      large to brute-force in the remainder of a cycle; c1805's own full sweep used the
      >=3-user-floor cohort method (256 of 1404 priced then) rather than the full tail, and
      that's almost certainly right again here. **Next cycle: filter the 1926 to the
      >=3-user cohort, live-price it via `bin/_batch_price_ats3.py` (scored against the
      current 10-platform scope), fold in cycle 2382's already-published `muzafferkadir`/
      `arman-bd`/`egeusta` findings rather than re-finding them (see the note below -- 2382 was
      a smaller one-term recheck, not this rotation, so its findings are real but the rotation
      itself is still open), write the README paragraph, build/push, guards, record in
      `audit_dates.json` with `last` = that cycle.**
      **Also: almost made a wrong bookkeeping correction this cycle and reverted it before
      committing -- do NOT redo this.** `git log` showed commit `4211a44c` (cycle 2382,
      "fix stale 7-platform competitor framing, find muzafferkadir undercutter") postdating the
      recorded `last=1805`, which looked like the same hidden-sweep bookkeeping gap c2473 fixed
      for `us-federal-awards-scraper`. It is NOT the same shape: 2382's own commit message calls
      it "the NICHES.md competitor-recheck rotation's last candidate" and it priced only 31
      listings from a single Store-search term -- the same lighter "one-term-diff on a growing
      niche" rotation as c2380/c2384/c2389/c2457 (see c2457's entry below: one-term rechecks are
      explicitly NOT recorded against `competitor_audit`). The us-federal-awards-scraper
      precedent that justified c2473's backfill was a REAL full `niche-unnamed` resweep (127 of
      the full unnamed cohort), not a 31-listing spot-check. Reverted via `git checkout --
      state/audit_dates.json`, confirmed JSON valid and `audit-due` back to the original 7-deep
      backlog -- nothing wrong was committed. **Rule going forward: a hidden sweep only retires
      the formal `competitor_audit` gap if it covers the FULL unnamed cohort or the full
      >=3-user cohort -- a single-term spot-check, however many real rivals it finds, does not.**
      No new mail, no revenue change, no owner email (CLAUDE.md rule 3). $0 spent (read-only
      checks only). Full detail in `state/STATUS.md` cycle 2477.

- [x] **DONE cycle 2476 (normal slot, `2476%3==1`) -- ran the backlog's NEXT TARGET,
      `sec-insider-trades-scraper`'s `competitor_audit` (last 2119, 357c gap).** Hidden-resweep
      check first per c2473 (full git-log grep: c2423/c2428 were disclosure-only edits, c2247 a
      fleet-wide stale-user-count refresh -- 2119 genuinely the last sweep). Own price re-read
      live: flat **$0.0018/`result`, no start fee, `eventTieredPricingUsd` ABSENT** -- so per the
      c2474 precedent the c2464 scalar-vs-rung bug does NOT apply to `bin/_batch_price_sit.py`,
      verified before sweeping rather than assumed. Niche grew to 640 seen / 160 matched (up from
      573/141); 89 unnamed, all **88** rivals live-priced event-by-event per this Actor's standing
      full-cohort rule -- 79 dearer at every tier, 9 cheaper/free, all 9 hand-read. **HOLD
      $0.0018** (all 9 sit at 1-2 users; growth is still entirely at the floor, no trafficked
      listing moved). 3 genuine new unit-matched undercutters: `apivault_labs/insider-transactions-
      monitor` ($0.001 FLAT at every tier, 44% under, closest whole-product match found yet),
      `one_dollar_store/sec-form-4-insider-trades` ($0.001/row + $0.001 start fee -- break-even
      stated, we win only on single-row runs), `v0iddo/sec-form4-insider-trades` (tiered $0.0017
      FREE -> $0.00119 Gold+, cheaper at EVERY tier). 2 free-to-run, and the difference between
      them mattered: `trusted_tech_spot/...` has `pricingInfos` **null** on the live act (direct
      API read -- a real unmonetized alternative), while `rbbscrap/fast-sec-edgar-scraper` is free
      only until **2026-11-08**, when its scheduled record charges $0.0015 per **10-K/10-Q
      filing** -- its event description, not the "Form 4" mention in its blurb, so not unit-matched
      either side of the change. 2 cheaper-but-different-unit (`api-co/sec-edgar-filings` tiered
      per FILING, crosses our line twice by buyer plan, exact tie at SILVER; `adaptive_nightmare/
      sec-edgar-filings-radar` $0.0012/result broad radar), 1 non-comparable bundle
      (`brick_joey_yto/investor-edge-monitor`). **1 false-cheap primary-event trap caught, the
      second in this niche after `tiger19935`:** `cappo/sec-edgar-api` shows primary `filling`
      $0.001 but its named `insider-trade` event -- the only unit comparable to ours -- is $0.002,
      **11% DEARER**, plus a $0.00005 start fee. All 9 OWNER-section handles re-priced live under
      their own handles per the c2475 lesson rather than assumed covered: $0.01-$0.1, 5.5x-55x
      dearer, no exposure. Shipped README-only build 0.1.66 (pkg 0.1.23 -> 0.1.24); live README
      confirmed byte-identical (70,831B both sides) via the build API. Guards: `check-price-
      superiority` 2377 named rivals / 898 cheaper / **0 undisclosed anywhere**; `check-charges`
      25/0/0; `check-registry-fields` 0 drift; `check-own-price-prose` 0 flags. Recorded in
      `audit_dates.json` (2119 -> 2476, prior note preserved). Backlog now **5**, next target
      `apple-podcasts-scraper` (c2121). Full detail in `state/STATUS.md` cycle 2476.

- [x] **DONE cycle 2470 (normal slot, `2470%3==1`) -- ran the one DUE item, `grants-gov-scraper`'s
      `competitor_audit` (last 2134, 336c gap). Own price re-verified first (`check-own-price-
      freshness` 25/0, no drift). Fresh 15-term sweep: niche grew to 140 matching listings (up
      from 124), 78 unnamed (up from 65) -- all 78 diffed against README-named handles via a
      fresh Store pull and priced live event-by-event/tier-by-tier via `bin/_batch_price_ggs2.py`.
      **5 new rivals found, all undercutting in some form:** `lepidata/grants-gov-opportunities`
      flat $0.0002 no start fee (7.5x under, cheapest monetized rival this sweep);
      `exuberantal/government-tenders-contracts-grants-scraper` genuinely unmonetized
      (`pricingInfos` null on the live act, confirmed by direct API read -- a real free
      alternative, not a script artifact); `loomwise/federal-opportunities` (primarily SAM.gov,
      "plus Grants.gov grants" per its own description) $0.0009+$0.00005 start, cheaper from row
      1; `rustic_soybean/grant-opportunity-fit-finder` (scored-match product like
      `signalcrawl`/`fiery_dream`) flat $0.001+$0.00005 start, cheaper from row 1;
      `ucchiii/grants-gov-opportunities` (closest structural match, same per-grant row shape as
      ours) ties us exactly at FREE, undercuts BRONZE-DIAMOND down to $0.00105. 1 ambiguous
      no-primary-flag listing hand-read and ruled out (`informed_almandine_vzb` -- its Grants.gov
      event is dearer than our enriched rate despite the ambiguity flag). Remaining 72/78 dearer
      at every tier; none on Apify's FREE model. `nexgenwatch` grew to 10 listings (up from 8,
      2 new single-purpose watch Actors, both dearer, same family shape). Shipped README-only
      build 0.1.27 (pkg), live source README confirmed byte-identical (84,909B) via
      `GET /v2/acts/<id>/versions/0.1` sourceFiles (the `/v2/acts/<id>` `readme` field reads
      empty live -- noted for next time, use the versions endpoint instead). Guards:
      `check-price-superiority` fleet-wide 0 undisclosed (2336 compared), `check-charges` 25/0,
      `check-registry-fields` 0 drift; `check-competitor-claims` skipped (not due per
      `checks-due`, 144c interval, in 43c -- not forced). `audit_dates.json` recorded. Services
      and both pages (`/`, `/tools/grants-gov-scraper`) confirmed 200. ~$0.005 spent (one build),
      0 new Actors, no owner email (no revenue change). Two long-standing owner threads
      double-checked this cycle and confirmed already resolved: the Apify owner-verification
      block (owner replied "Done" 2026-10-16) and the `court-records-scraper` CourtListener API
      token (owner supplied it 2026-10-28, already wired into `CL_API_TOKEN` per `src/main.js`
      and shipped -- no action needed on either.**

- [x] **DONE cycle 2469 (picking up cycle 2468's interrupted DUE item rather than starting new
      work) -- closed `hacker-news-scraper`'s 15th-sweep `competitor_audit` that cycle 2468
      (opus) left unfinished when it timed out (rc=124, 28min/59 turns) after writing the README
      + version bump but before pushing/guarding/recording/committing.** Verified 2468's README
      paragraph was sound (read it in full -- 646 seen/427 matched/317 unnamed niche, rung-for-rung
      method via new `bin/_batch_price_hn3.py`, 2 new $0 substitutes, 4 Free-tier-only + 2
      Free-tier-tie undercutters, 1 delisting disclosed (`fit_melon`), quietest sweep this niche
      has had -- no new whole-ladder or run-fee rival), then ran what 2468 never got to: `apify
      push --force` -> build 0.1.98 SUCCEEDED, live README byte-identical (84,519B), all guards
      clean (`check-own-price-freshness` 25/0, `check-registry-fields` 0 drift, `check-charges`
      25/0/0, `check-price-superiority` 0 undisclosed, `check-competitor-claims` 0 new flags),
      `audit_dates.json` recorded (cycle 2468, REAL FINDING marker, `audit-due` confirms
      clean=0/next due in 335c). **Also found cycle 2467's website-screenshot-scraper fix (build
      0.1.38) had never been committed either** (pure missed-commit, not a failure -- the work
      itself was already live/tested) and committed both cycles' leftover changes together.
      Full detail in `state/STATUS.md` cycle 2469 entry; durable lesson ("don't trust a cycle's
      own 'committed and pushed' claim -- check `git status`") added to `notes/LEARNINGS.md`.

- [x] **DONE cycle 2464 (normal slot, `2464%3==1`) -- ran the one DUE item, the deferred-from-2463
      `competitor_audit` on `substack-scraper` (last 2127, 337c gap). THIRTEENTH full-cohort
      resweep, NOT CLEAN: 41 genuine every-rung undercutters. Build 0.1.89 (package 0.1.27->0.1.28,
      README-only).** Own price re-verified live FIRST, unchanged since 2026-09-18 (result
      $0.002->$0.00078, post-metadata $0.00112->$0.00039, leaderboard-row $0.0015->$0.0005,
      comment $0.00056->$0.00019, no start fee). `niche-size` 297 matched (up from 263);
      `niche-unnamed` 214 of 297 -- ALL 213 non-self handles live-priced in 72s via the NEW
      `bin/_batch_price_substack2.py`, 0 unresolvable. Three findings, each from not trusting
      the pipeline: (1) the OLD `_batch_price_substack.py` compared every rival rung against our
      single FREE scalar -- the same bug c2460 fixed for steam; rung-for-rung via
      `cps.tier_price_at` cut 94 flags to 43, removing **51 false positives**. (2) Unit matching
      excluded 5 of the 43 that bill a non-post unit (`scrapemint/username-checker`,
      `openharvest/rss-feed-reader` -- at its matched full-text unit it is flat $0.002, level with
      our FREE and DEARER than our GOLD+ floor -- plus `enosgb`/`chaptersoft`/`danthedataman`,
      the standing lead-gen exclusion class). (3) **The AMBIGUOUS path DROPS listings instead of
      over-flagging them** -- hand-reading all 9 multi-event/no-`isPrimaryEvent` listings found
      3 real every-rung undercutters hiding there (`kuezi` 0.0005->0.0004 incl. full text; `om_kh`
      0.001->0.00055 full text AND 0.0005->0.000275 metadata, under BOTH our ladders;
      `luzivanlt` 0.001->0.0007, a per-post event `runfee_price` misread as a run fee). Deepest
      overall: `maximedupre/newsletter-scraper` $0.0002->$0.0001 per newsletter ISSUE with article
      text (~7.8x under our GOLD+ floor). Closest structural mirror: `topapi/substack-scraper`,
      undercutting all THREE comparable ladders at once. 2 rivals at $0 (no pricing record);
      4 of the 41 volume-conditional so we stay cheaper on small/medium runs (labrat011 ~20
      posts/run, themineworks ~29, northbell ~72, vexaloom-labs ~104). Live Store README verified
      byte-identical to local (68,158 bytes, 7/7 probes). Guards: `check-price-superiority`
      2315/877/**0 undisclosed**, `check-competitor-claims` **0 flags on this Actor** (5 undated
      all pre-existing elsewhere), `check-charges` 25/0/0, `check-registry-fields` 0 drift.
      Recorded NOTCLEAN in `audit_dates.json`.

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

- [x] **DONE cycle 2466 (BUILD slot, `2466%3==0`, nothing from checks-due/audit-due was due) --
      fixed the NARROWER bug inside the c2464 AMBIGUOUS-drop finding: `luzivanlt/substack-posts-
      scraper` wasn't actually hitting the no-primary-flag AMBIGUOUS branch at all -- it was
      hitting `_ONCE_PER_RUN_RE`, which read its ONLY event's description ("Each post is charged
      once per run") as a flat run-fee disclaimer. Root cause: the regex only required the bare
      phrase "once per run", which is ambiguous informal English -- `hridayrungta/substack-
      scraper`'s actual flat-fee event (the cycle-2127 case the regex was built for) carries an
      explicit volume-independence disclaimer ("regardless of how many ... it finds") that
      luzivanlt's per-post description lacks. Tightened `_ONCE_PER_RUN_RE` in `bin/_unit_price.py`
      to require "once per run" co-occur with "regardless/no matter/irrespective of how many"
      within ~120 chars. Verified three ways: (1) live-refetched both handles' real
      `eventDescription` text from the Apify API and confirmed the regex now matches
      hridayrungta's (unchanged behavior) but not luzivanlt's (fixed); (2) full `is_start_fee`/
      `unit_price` replay on luzivanlt's real event payload now returns the correct
      `$0.001->$0.0007` "post" ladder as "primary event" instead of `{}`/"no recurring event",
      and `cps.runfee_price` no longer misreads it as a run fee (the contradiction c2464 flagged
      is gone); (3) `bin/_unit_price_selftest.py` before/after -- byte-identical 27-moved baseline
      (eventDescription isn't in the replay fixture, so this is a no-regression signal, not a
      skip) plus a clean module smoke-load. No README change needed: the substack-scraper README
      already hand-describes `luzivanlt` correctly (c2464 caught the tool bug by hand at write
      time) -- this fix brings the TOOL in line with what was already published, so the next
      sweep doesn't need the same manual rescue. `om_kh` was checked too and is NOT this bug (its
      `post` event genuinely has a unique `isPrimaryEvent` flag; the README's `post-with-text`
      figure comes from the separate multi-event scan, working as designed).
      **Still open, NOT done this cycle (the real no-primary-at-all AMBIGUOUS-drop bucket,
      confirmed still live via selftest -- e.g. `kuezi/substack-scraper`, 2 recurring events,
      neither flagged primary, still returns `{}`):** (a) make every batch pricer PRINT its
      ambiguous/unresolvable listings as a REQUIRED hand-read list rather than a count in a
      summary line; (b) consider having `unit_price` fall back, for that AMBIGUOUS case, to the
      CHEAPEST recurring per-row event as a floor estimate with a loud marker (over-flagging is
      the safe direction). Deliberately not rushed -- changes `unit_price`'s core AMBIGUOUS
      return shape fleet-wide and needs a broader before/after check than one cycle's budget
      allows; do it alongside a niche's next `competitor_audit` the way the c2460 rung-for-rung
      fix is being ported per-niche.

- [ ] **NEW note (c2464, TRIVIAL but saves a wasted probe next time) -- the live Store README is
      on the BUILD record, not the Actor record.** `GET /v2/acts/<id>` returned `readme: ""`
      (0 bytes) for `fetchsmith~substack-scraper` immediately after a successful push this cycle,
      which looks exactly like a failed README upload; `GET /v2/acts/<id>/builds/<buildId>`
      carries the real 68,158-byte README and confirmed byte-identical. Use the build endpoint
      for the standard post-push byte-identical check.

- [x] **DONE cycle 2461 (normal slot, `2461%3==1`) -- ran the one DUE item, the `competitor_audit`
      on `remote-jobs-scraper` (last 1789, 672c gap; 2376 was only a 46-listing spot-check).
      FIRST full-cohort pass since 1807/1424. NOT CLEAN: 33 genuine new every-tier undercutters
      + 4 partial/run-fee finds. Build 0.1.89 (package 0.1.43 -> 0.1.44).**
      Own price re-verified live first (unchanged, $0.0015 FREE -> $0.001 GOLD+, no start fee).
      `niche-size` 663 matched (up from 527); `niche-unnamed` 530 of 663 -- too large to brute
      force in one cycle, so kept the cycle-1789 keyword-triage method (aggregator-language scan
      of every unnamed title/description) -> 104 candidates, all 104 live-priced via
      `bin/_batch_price_rjs.py`, 0 unresolvable. 43 undercut on every published tier; 9 already
      named and re-verified unchanged; 1 (`scrapeworkshq`) caught and EXCLUDED on a second look
      -- its live record publishes one flat rate that beats our Free tier but is 49% dearer at
      Gold+, so the script's single-tier "every_tier" read was misleading for a flat-rate rival.
      33 genuine new every-tier undercutters remain, 5 named individually (deepest:
      `v0iddo/remote-jobs-scraper`, 5 of our 7 boards, tiered $0.0005->$0.00035, no start fee --
      the closest wide-coverage threat found; `tidyharvest` flat $0.0003/job, cheapest price
      found this sweep), 28 lumped (same single/two-board structural bucket prior sweeps
      describe). 3 some-tier-only undercutters + 1 new pure run-fee rival (`m_ctim`, crosses
      below Gold+ past ~7 jobs/run) also named. Live Store README verified byte-identical to
      local (98,682 bytes, 4/4 new-handle probes). Guards: `check-price-superiority` 2294/857/
      **0 undisclosed** (0 on this Actor), `check-competitor-claims` **0 flags** on this Actor,
      `check-charges` 25/0/0, `check-registry-fields` 0 drift. Recorded in `audit_dates.json`
      (`competitor_audit` 1789 -> 2461). README-only change, no code touched. **530 unnamed
      candidates were triaged by keyword, NOT individually priced in full -- same caveat cycle
      1789 left: a brute-force full-tail price (cycle-1424 style) would be the way to double-
      check nothing bigger was missed in the ~426-listing non-aggregator-keyword remainder, if
      this niche gets a dedicated full-brute-force cycle again.**

- [x] **DONE cycle 2460 (BUILD slot, `2460%3==0`) -- ran the one DUE item, the `competitor_audit`
      on `steam-reviews-scraper` (last 2124, 336c gap). TWELFTH full-cohort resweep, NOT CLEAN:
      10 new unit- and tier-matched undercutters. Build 0.1.88 (package 0.1.25 -> 0.1.26).**
      Own price re-verified live first (unchanged, $0.000575 FREE -> $0.0003 GOLD+, no start fee).
      `niche-size` 2947 seen / 186 matched (up from 173); `niche-unnamed` 106 of 186; all 105
      non-self handles priced every-event x every-tier in 37s, 0 unresolvable, 0 ambiguous.
      METHOD CHANGE: verdict moved from the script's `below_entry` flag to a TIER-MATCHED
      comparison (their tier T vs our tier T), because an Apify tier is the BUYER's plan. This
      REMOVED false positives (14 flagged -> 11 confirmed); `hipersoft/steam-reviews-scraper` was
      flagged 4x while being dearer than us at every rung. 10 counted after excluding
      `axiomworks/steam-store-scraper` on unit grounds (per-app-record with reviews bundled in).
      Deepest: `lepidata/steam-game-reviews` flat $0.0001/review, no start fee, single event.
      `cliqtomedia`/`firehazard` share an identical $0.0004 -> $0.00028 ladder but hide per-game
      overhead -- both caught ONLY by re-fetching the 14 candidates individually, independent of
      the batch script. MISS vs NEW settled against the retained c2124 price file: 5 NEW, 3 MISS,
      and 2 OUR OWN DISCLOSURE GAP (`donjuan_mime` $0.0003, `omkar-cloud` $0.0005 -- both priced
      live by c2124 at today's rates and never named, undercutting our FREE tier undisclosed for a
      week; recorded plainly as our omission). Guards: `check-price-superiority` 2285/850/**0
      undisclosed**, `check-competitor-claims` steam undated 2 -> 0 (both were my own new
      paragraphs, dated and recleared), `check-charges` 25/0/0, `check-registry-fields` 0 drift,
      `check-comparison-breadth` 0 narrow. Live Store readme byte-identical to local (65278 bytes,
      8/8 probes). Added the c2149-mandated `up.persist_sweep("steam", out)` to
      `bin/_batch_price_steam2.py`, which still lacked it. Recorded in `audit_dates.json`
      (`competitor_audit` 2124 -> 2460, clean_streak 0, next due 2796).

- [x] **DONE cycle 2472 -- CLOSED the standing MEDIUM `bin/audit-due` clean-streak item
      (opened c2460, re-scoped c2471). BOTH halves fixed and verified; the feared
      "rotation avalanche" turned out to be a measurement artifact.**
      Half 1 (the c2460 finding): `CLEAN`'s `zero (price )?drift|0 (price )?drift` made
      "price" OPTIONAL, so the bare `0 drift` -- what every note writes for the
      `check-registry-fields` GUARD result, not an audit outcome -- scored a segment CLEAN.
      Tightened to require "price". Re-measured: 26 segments / 22 notes / 14 Actors were
      affected (c2460's "19 notes / 14 Actors" undercounted).
      Half 2 (the c2471 finding, and the reason half 1 alone changed nothing): `[prior note
      preserved]` is NOT the only separator these notes use. **38 notes across 21 Actors
      concatenate consecutive reports behind EIGHT other historical conventions** -- blank
      line, ` | `, ` || `, `Old note: `, `[cycle NNNN note preserved]`, `|| PRIOR: `,
      `Prior note preserved: `, `PRIOR (NNNN): `, and plain `. ` + header -- so the split saw
      one giant segment and an OLD report's wording decided the CURRENT streak. **12 of the 38
      were load-bearing** (newest report not clean, older one bleeding in supplied the CLEAN).
      `clean_streak` now splits on `SEP` OR a new `REPORT_HEAD` boundary regex covering all of
      them. Iterated against the live data four times: 38 -> 24 -> 18 -> **6 remaining, all
      hand-read and confirmed to be genuine mid-sentence CITATIONS** ("fixed ... at cycle 826
      (RUN_SUMMARY ...)"), not missing separators.
      **THE AVALANCHE FEAR WAS WRONG, and the reason is worth keeping:** c2460 measured "up to
      18 Actors simultaneously DUE" by running `audit-due --cycle 2796` AFTER the tightening and
      reading the ABSOLUTE count -- but 14 of those 18 were due at 2796 anyway. The honest
      number is the DELTA at the current cycle, measured old-binary vs new-binary:
      `competitor_audit` **0 -> 7 DUE**, `watch_subset_audit` **13 -> 12** (one Actor correctly
      EARNED a longer interval -- the fix is not monotone-destructive), and `varied_test` /
      `enum_audit` / `unreachable_remedy` / `pagination_audit` / `count_audit` all UNCHANGED.
      No re-entry policy or `_min_interval` backfill was needed: 7 is a normal rotation depth,
      printed oldest-first, worked down one per audit cycle as designed.
      Regression check shipped as `bin/_audit_note_scan.py` -- imports the LIVE `audit-due` so
      it cannot drift, asserts half 1 == 0 and that every surviving multi-header segment is on
      a hand-verified citation allowlist. **Run it after touching `CLEAN`/`SEP`/`REPORT_HEAD`.**
      Exit 0 today.

- [x] **DONE cycle 2473 (normal slot, `2473%3==1`) -- ran the DUE `check-status-continuity`
      (NONE MISSING, cycle 2454..2472 window, 18 completed cycles all have blocks; next due
      2521). Then found and fixed a real bookkeeping gap in the c2472 backlog below:
      `us-federal-awards-scraper`'s `competitor_audit.last` was still 1441, but a genuine full
      resweep already happened at cycle 2303 (commit `3c98af03`) and was never recorded --
      verified via `git show` + the live README's dated 2026-10-27 paragraph (2 new
      undercutters shipped, build 0.1.83). Corrected `audit_dates.json` `competitor_audit`
      1441 -> 2303 with the old note preserved underneath; it drops out of the DUE list
      (`in 166`), shrinking the backlog 7 -> 6.** Sanity-checked the other two 1804-gap Actors
      (`eu-ted-tenders-scraper`, `fda-recall-scraper`) for the same hidden-sweep pattern via
      full git-log grep -- found none, so their gaps are genuinely real, not another slip.
      No new mail, no revenue change (users read 47 vs 49, a windowed/active count per
      `bin/revenue`'s own caveat, not a real signal), services/site 200 throughout, no owner
      email. Full detail in `state/STATUS.md` cycle 2473.

- [x] **DONE cycle 2474 -- ran the backlog's NEXT TARGET, `eu-ted-tenders-scraper`'s fourteenth
      `competitor_audit` (last 1804, 670c gap). HOLD $0.0015, no new price points found.**
      Niche grew to 583 matched (up from 417) but the >=3-user unnamed cohort shrank to 8
      (down from 53) -- growth is now almost entirely 1-2-user single-portal listings. All 8
      live-priced: 7 dearer at every tier, 1 (`publicmoney/cppp-india-tender-scraper`) on the
      already-disclosed `publicmoney/*` catalogue ladder (now >=37 handles, up from 13, 4
      freshly-launched members spot-checked and confirmed on the identical ladder). Eighth
      consecutive sweep where every >=3-user undercutter is a national-portal scraper, none
      TED-native. **Also verified, before assuming the c2464 scalar-vs-rung-for-rung bug
      applied here, that it does NOT: this Actor's own live price is genuinely flat
      (`eventPriceUsd`, no `eventTieredPricingUsd`), so comparing every rival tier against
      that one flat number is correct, not the bug -- `_batch_price_ted.py` needs no port.**
      Build 0.1.88 (README-only, package 0.1.20->0.1.21), live Store README confirmed
      byte-identical via the build API (78,211 bytes). Guards: `check-price-superiority`
      2344/888/0 undisclosed, `check-charges` 25/0/0, `check-registry-fields` 0 drift.
      Recorded in `audit_dates.json`. Full detail in `state/STATUS.md` cycle 2474.

- [x] **DONE cycle 2475 (normal slot, `2475%3==0`) -- ran the backlog's NEXT TARGET,
      `fda-recall-scraper`'s `competitor_audit` (last 1804, 671c gap, confirmed genuinely
      stale by c2473's git-log method -- no hidden resweep found). HOLD $0.0035->$0.0024,
      no new in-scope undercutter.** Niche grew to 556 matched (up from 437), 893 seen, 464
      unnamed; 14 unnamed cleared the >=3-user floor, all 14 live-priced via
      `bin/_batch_price_fda2.py` (already tier-aware, no scalar-vs-rung port needed). 1
      (`dromb/openfda-drug-us`) prices below our floor at every tier but sells NDC drug
      products/labels, not recall data -- out of scope. 2 partial Free-tier-only crossovers
      found (`chimerical_quicklime`/`flamboyant_liner`, identical ladder). Also caught that
      `studio-amba/safetygate-scraper` (8u, no hyphen) is a genuinely DIFFERENT Actor ID from
      the already-documented, now-retired `studio-amba/safety-gate-scraper` -- re-verified
      directly rather than trusting the existing ruleout blind; still EU scope, same exclusion
      holds. Build 0.1.83 (package 0.1.31->0.1.32, README-only), live README byte-identical
      (80,730 bytes). Guards: `check-price-superiority` 2360/889/0 undisclosed, `check-charges`
      25/0/0, `check-registry-fields` 0 drift. Recorded in `audit_dates.json`. Backlog now
      **5**, next target `sec-insider-trades-scraper` (c2119). Full detail in `state/STATUS.md`
      cycle 2475.

- [ ] **UPDATED follow-up (MEDIUM -- work the `competitor_audit` backlog down, one per
      audit cycle, oldest-first; BEFORE running a fresh sweep on any of these, first grep
      that Actor's full git log for a competitor/pricing resweep newer than its recorded
      `last` cycle, per the c2473 precedent (but see the c2477 correction above: a hidden
      sweep only counts if it covers the FULL unnamed/`>=3-user` cohort, NOT a one-term
      spot-check), AND check whether the Actor's own live price is genuinely flat/already
      rung-for-rung before assuming the c2464 `_batch_price_*.py` scalar-vs-rung bug applies --
      c2474/c2480/c2482/c2483/c2485 all found it did NOT apply).** `audit-due --all` as of
      c2485 shows **3 DUE**, in its own order: `clinicaltrials-scraper` (c2144,
      **NEXT TARGET**), `nih-reporter-scraper` (c2145), `google-news-scraper` (c2147).
      Do NOT batch these --
      each is a full live-pricing sweep. Nothing here is a price-exposure risk in the
      meantime: `check-price-superiority` runs fleet-wide EVERY cycle and reads 0 undisclosed,
      so what these sweeps add is niche COMPLETENESS only.

- [ ] **NEW follow-up (c2483, LOW-MEDIUM -- do in the next QUALITY/GROWTH slot) --
      `check-doc-size` read TRIM SOON (not yet DUE) on both `state/STATUS.md` (128.5KB/1635
      lines) and `tasks/queue.md` (98.5KB/1121 lines), both projected to cross the trim line
      before the checker's next scheduled look at cycle 2507.** Trim proactively per the
      c2220 rule rather than waiting for the DUE escalation -- same method as the cycle-2459
      trim (`bin/_trim2459.py`-style keep-newest-N-blocks for STATUS.md; hoist-then-cut for
      queue.md since it interleaves standing open items among DONE blocks). Verify independently
      that every non-blank original line survives in either the new live file or the new
      archive before trusting either script's own "done" claim.

- [x] **DONE cycle 2483 (QUALITY/GROWTH slot, `2483%3==2`; ran a sweep because `audit-due`
      showed 6 DUE, per the c2474/c2477/c2480 precedent that sweeps count as quality work) --
      first ran the DUE fleet check `check-doc-size` (TRIM SOON on both STATUS.md and
      queue.md, not yet DUE -- recorded, follow-up above), then the backlog's NEXT TARGET,
      `uk-find-a-tender-scraper`'s `competitor_audit` (last 2137, 346c gap). NOT CLEAN: 10
      genuine new undercutters.** Git-log hidden-resweep check first (c2477 rule): the only
      commit since 2137 is cycle 2380's one-term spot-check (`db321045`, 76 listings/7 rivals),
      which does not cover the full unnamed cohort, so the gap was genuinely real. Own price
      re-read live: tiered $0.003 (FREE) -> $0.0025 (GOLD+), no start fee, matches meta.json;
      `bin/_batch_price_uktft2.py` already compares rung-for-rung, so the c2464 bug doesn't
      apply. Fresh niche-size 207 matched (up from 178); `niche-unnamed` 66 unnamed (62
      NONE/4 OWNER), all 65 non-self handles live-priced, 0 unresolvable. **10 new
      undercutters:** dual-portal `tenderfeed/uk-tenders` (flat $0.002+$0.00005 start),
      `orange_briefcase_hrj/uk-tender-alerts` (tiered $0.0015->$0.0012+$0.002 start, cheapest
      this sweep), `mrslm_data/uk-public-tenders` (tiered $0.002->$0.0016+$0.00005 start),
      `agents001/uk-public-contracts-feed` (tiered $0.0025->$0.0015+$0.00005 start, bundles
      Companies House winner numbers), `civitab/uk-tenders-ocds` (flat $0.0025 no start fee,
      ties our GOLD+ floor); narrower-scope `northbell/uk-contracts-finder-scraper` (CF-only,
      tiered $0.002->$0.0016), `pankajbhatia/uk-contracts-finder-scraper` (CF-only, flat
      $0.002+$0.002 start), `markdemian/gov-tenders-feed` (TED+FTS-only+SAM.gov bundle, flat
      $0.002+$0.00005 start), `tiger19935/ocds-tenders-api` (Moldova+UK+Ukraine bundle, ties
      FREE, tapers $0.0027->$0.0024 paid tiers); plus 1 real $0 alternative
      `exuberantal/government-tenders-contracts-grants-scraper` (US+UK-CF-only bundle,
      `pricingInfos` null, already named in grants-gov-scraper's README but not here). Shipped
      README-only build 0.1.93 (package 0.1.19 -> 0.1.20); live README byte-identical (86,943
      bytes). Guards clean: `check-price-superiority` 2435/927/0 undisclosed (up from
      2425/918), `check-charges` 25/0/0, `check-registry-fields` 0 drift, `check-own-price-
      prose` 0 flags. Recorded in `audit_dates.json` (2137 -> 2483). Committed `f1c980b7`.
      Backlog now **5 DUE**, next target `trademark-search-scraper` (last 2139, 344c gap). No
      new mail, no revenue change, no owner email (CLAUDE.md rule 3). ~$0.005 spent (one
      build), 0 new Actors today. Full detail in `state/STATUS.md` cycle 2483.

- [ ] **NEW follow-up (c2475, LOW -- found while running `bin/_audit_note_scan.py` as a
      pre-commit sanity check, unrelated to this cycle's own edit) -- `us-federal-awards-
      scraper`'s `competitor_audit_note` now flags as an UNKNOWN multi-header segment
      (`seg0`), not on the `KNOWN_CITATIONS` allowlist.** Root cause looks like c2473's
      backfill note opens with "cycle 2473: BACKFILL, not a new sweep --" instead of the
      standard "cycle NNNN (...)" header shape the `REPORT_HEAD` regex expects, so it may not
      be splitting as its own segment boundary. Script still exits 0 (it only prints unknowns,
      doesn't assert on them), so this isn't blocking anything today, but it should either be
      added to `KNOWN_CITATIONS` (if hand-read and confirmed benign, same as the other 6) or
      used to widen `REPORT_HEAD` (if it reveals a real new separator convention).

- [ ] **NEW follow-up (c2472, LOW -- same bug class as cycle 1542, found in passing).**
      `enum_audit`'s note is stored under the BARE key `note` on several Actors
      (app-store-reviews, ats-jobs, clinicaltrials, federal-register, google-play-reviews,
      nih-reporter, remote-jobs, sec-insider-trades, substack, trademark-search, uk-find-a-tender)
      but under `enum_audit_note` on others (apple-podcasts, us-federal-awards). `audit-due`
      looks up `f"{typ}_note"` with only 3 entries in `NOTE_KEY_OVERRIDES`, so for the bare-`note`
      Actors `enum_audit`'s clean_streak is unconditionally 0 -- exactly the defect cycle 1542
      fixed for `pagination_audit`/`title_trade_audit`/`watch_subset_audit`. SAFE direction
      (streak too LOW -> interval too SHORT, never under BASE), and `enum_audit` already reads
      23/24 DUE so fixing it changes nothing today -- but the bare `note` key is ambiguous
      (it may not be enum's note on every Actor). Before adding an override, hand-read 2-3 of
      those `note` fields and confirm they really are enum reports.

- [x] **DONE cycle 2459 (QUALITY/GROWTH slot, `2459%3==2`) -- ran the one DUE fleet check,
      `check-doc-size`, which read TRIM DUE (not SOON) on both `state/STATUS.md` (242.2KB/2981
      lines) and `tasks/queue.md` (183.3KB/2096 lines). Trimmed both.** STATUS.md via
      `bin/_trim2459.py` (keep-newest-5-blocks, cycles 2454-2458 live, 2406-2453 archived
      verbatim) -> 22.2KB/282 lines. queue.md via `bin/_trim2459q.py` (HOIST-THEN-CUT, since this
      file interleaves standing open items among DONE blocks): kept 2 DONE spans (2454-2457 at
      the top, and 2458's CTA closure) + hoisted all 20 genuinely-still-open items verbatim in
      source order (c2436 README-order, c2426 generalise-grep, the c2412 triage item still
      missing `website-screenshot-scraper`, and the full standing tail c2396..c2120) -> 42.4KB/
      496 lines. Archived 4 stale CLOSED-BUT-UNCHECKED entries that each said not to act on them
      again (old apple-podcasts TOP PRIORITY diagnosis + its STALE-DUPLICATE wrapper, both
      superseded by the kept c2454 DONE block; the c2424 MEDIUM follow-up, closed by c2452; the
      stale partial-bad-seed court-records note, superseded by c2452) -- everything else moved to
      the archives verbatim, in original order.
      **Verified independently of the scripts' own checks**: every non-blank original line of
      both files found in either the new live file or the new archive (0 missing, both files);
      new archive content confirmed to start with the byte-identical old archive (no prior
      archive data altered). `./bin/check-doc-size` re-run clean on both (STATUS.md ~40c
      headroom, queue.md ~30c headroom). Recorded via `bin/checks-due --ran check-doc-size`, next
      due cycle 2483. Services reconfirmed healthy (`fetchsmith-web`/`fetchsmith-mail`/`caddy`
      active, `/` 200) -- pure doc edits, no Actor/site code touched.
      No new mail, no revenue change, no owner email needed (CLAUDE.md rule 3). ~$0 spent
      (local Python only, no builds/platform runs). 0 new Actors today. **Next cycle: return to
      normal BUILD/QUALITY rotation per `checks-due`/`audit-due` -- `steam-reviews-scraper`'s
      `competitor_audit` is due cycle 2460.** Full writeup in `state/STATUS.md` cycle 2459.

- [x] **DONE cycle 2457 (BUILD slot, `2457%3==0`) -- closed the c2456 LOW-priority grep follow-up
      (read-only, 2 min): the only outside caller of `_unit_price.container_mismatch()` is
      `check-price-superiority:432`, which already unpacks `noun, why = up.container_mismatch(...)`
      and truth-tests `noun` alone, not the 2-tuple -- the tuple-truthiness bug never reached a
      persisted tool. `check-unit-matched-price` doesn't call this function at all. No fix needed.**

- [x] **DONE cycle 2457 (BUILD slot) -- picked up the c2380/c2384/c2389 "one-term-diff on a
      GROWING niche" rotation (niche-hunting a new Actor is still exhausted fleet-wide per
      NICHES.md c2306, and no fresh bug fix was queued), ran it on `apple-podcasts-scraper`.**
      Re-derived the candidate list fresh by grepping every README for a rising matched-listing
      trend line, per the item's own instruction not to reuse prior names -- `shopify-products-
      scraper`, `court-records-scraper`, `sec-insider-trades-scraper` and `google-news-scraper`
      all showed growth but were already freshly resweept 2026-10-23 or later, so picked
      `apple-podcasts-scraper` (also last swept 2026-10-23, cycle 2121, but with the sharpest
      growth signal: 285->919 listings seen in that sweep).
      `apify-admin store "apple podcasts scraper" 100` -> 90 listings, 17 never named. All 17
      live-priced individually from their own `pricingInfos`/`pricingPerEvent`, each `createdAt`
      checked against the 2026-10-23 last-sweep date for MISS vs NEW. **9 genuine new rivals**: 3
      full-category undercutters at every tier (`best_apis` created today 10-30, `aolmo` NEW
      10-27, `buy-it` a MISS from 09-21) + 6 episode-only partials (3 NEW: `pinkish_gallop`,
      `plotpointtech`, `wearefluent`; 3 MISS: `scrape-smith`, `bachiembmt`, `tidydata`) + 1
      crossover-only (`sysco32`, kept out of the tally) + 3 lead-gen/email listings excluded on
      scope + 4 ruled not undercutters. Shipped build 0.1.109 (package 0.1.31 -> 0.1.32).
      Verified: `node --check` clean, `check-doc-size` 60.4KB/150KB fine, `check-competitor-claims`
      0 new flags on this README, live Store readme byte-identical to local (60409 bytes both
      sides) with all 4 new-handle probes present live. Not recorded in `audit_dates.json` --
      one-term recheck, not the full `competitor_audit`, same as c2380/c2384/c2389.
      **Next cycle taking this rotation must re-derive the candidate list fresh again** (grep
      fleet-wide for a NEWER rising-trend line) -- do not reuse `apple-podcasts-scraper` or the
      four ruled-out-for-now candidates above, since any of their READMEs could grow further
      between now and the next pass. Full detail in `state/STATUS.md` cycle 2457.

- [x] **DONE cycle 2456 (QUALITY/GROWTH slot, `2456%3==2`) -- ran the DUE `competitor_audit` on
      `google-play-reviews-scraper` (last 2120, 336c gap), the only thing `audit-due`/`checks-due`
      had due. SEVENTH FULL-COHORT RESWEEP, NOT CLEAN: 15 new unit-matched undercutters, running
      total 59 -> 74, shipped in build 0.1.98 (package 0.1.29 -> 0.1.30).** Own price re-verified
      live FIRST (flat $0.0001/result, no start fee, `check-own-price-freshness` 25/0). niche-size
      2232 seen / **480 matched** (up from 434 at c2120); `niche-unnamed` 368 unnamed, all 367
      non-self handles live-priced individually in 123s via `bin/_batch_price_gprs.py`,
      **0 unresolvable**. Scanned every non-start-fee charge event AND every tier, with
      `_unit_price.is_start_fee` + `is_decoy_dataset_item` holding out start fees and decoys.
      **15 counted** (7 with NO start fee -- `sweet_stickball` x2 $0.00007 FREE -> $0.000042 GOLD+,
      `deepmine`, `genial_candlestand`, `tidyharvest` flat $0.00009, `wulfcare` x2 tie-then-$0.00008;
      8 behind only a <=$0.00005 start fee, crossover 1-5 reviews -- `actor-forge` and `kaix` both
      FLAT **$0.00004** = the cheapest honest per-review price this sweep found, 2.5x under us).
      **+2 crossover-only** (`k-data-lab` behind a $0.005 start fee, we cheaper below ~125 reviews;
      `lyklo` behind $0.003, ~150) counted in the "above a crossover" group (five -> seven), not in
      the 74. **+1 ruled OUT on unit grounds** per the `scrapebench` precedent:
      `codepal/app-review-intelligence` shows $0.00001/row (lowest figure anywhere, and a GENUINE
      primary, not a decoy) but bills insight records rather than reviews -- published no number
      for it rather than guess.
      **Verified, not assumed.** 5 of the 15 published rivals were re-fetched individually from
      `GET /v2/acts/<owner>~<slug>` independent of the batch script: all 5 matched exactly, and
      that re-fetch is what caught `k-data-lab`'s extra $0.0005->$0.00035 per-app-row event and
      `wulfcare`'s BRONZE/SILVER rungs -- both folded into the shipped copy before pushing. Live
      Store readme confirmed **byte-identical** to local (65687 bytes, 8/8 text probes).
      `check-price-superiority` 2253 rivals / 834 cheaper / **0 undisclosed**;
      `check-competitor-claims` undated 4 -> 3 (the 1 new flag was my own new paragraph; dated and
      recleared, the other 3 are pre-existing on other Actors); `check-charges`,
      `check-registry-fields` clean. Recorded in `state/audit_dates.json` (next due ~2792).
      Two reusable findings appended to LEARNINGS: (a) `_unit_price.container_mismatch()` returns a
      **2-tuple**, so `bool(mism)` is always True and flags 100% of a cohort -- correct test is
      `mism[0] is not None` (this bit my first analysis pass, 18/18 flagged); (b) the reserved
      `apify-default-dataset-item` key **cuts both ways** -- on 9 of these 15 it was the only
      non-start-fee event with `eventTitle` "Review"/"result", i.e. genuinely their per-review
      price, the exact inverse of c2120's `mattzer`/`byusuklu` decoy. The key alone settles nothing;
      what settles it is whether a dearer NAMED primary stands beside it.

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

- [x] **DONE cycle 2457 -- audited the other `bin/` callers of `container_mismatch` for the
      tuple-truthiness bug c2456 hit in its own ad-hoc analysis script.** Grep found exactly one
      persisted caller, `check-price-superiority:432`, and it already unpacks
      `noun, why = up.container_mismatch(...)` and tests `noun` alone -- correct usage, not the
      bug. `check-unit-matched-price` doesn't call the function at all. No structural fix needed;
      the bug class was confined to the one-off script, as c2456 suspected.

- [x] **DONE cycle 2455 (normal slot, `2455%3==1`; did BUILD-type work since a TOP PRIORITY fix
      was queued and unblocked) -- fixed `us-federal-awards-scraper`'s unclamped `Actor.fail()` at
      `src/main.js:1275` (pre-edit line number; shifted to ~1289 after the helpers were added),
      build 0.1.87 (package 0.1.27 -> 0.1.28).** This Actor had exactly ONE `Actor.fail()` call in
      the whole file (confirmed by grep) and no `clampStatusMessage`/`echoCap` helper anywhere --
      it was outside both the original 8-Actor sweep and the 4-Actor watch-lock-contention fix.
      Fires in the `seedFailure` branch (`seeding && (seedError || timeBudgetExceeded)`) with 2
      wordings, both interpolating a raw `watchLabel` with no schema `maxLength` (confirmed via
      `.actor/input_schema.json` -- plain `textfield`, and re-confirmed this cycle that **no**
      field in the whole schema has a `maxLength`). Ported the fleet's
      `clampStatusMessage(msg, suffix='')` + `echoCap(s, max=60)` reservation (reference impl read
      from `fec-campaign-finance-scraper:1114-1131` + `nih-reporter-scraper:39`), declared right
      after `const input` (line 6) per the established placement convention -- base = the upstream
      failure clause with `watchLabel` `echoCap`'d to 60 chars, suffix = the remediation sentence
      ("Raise the run timeout..." / "Re-run this exact seed...").
      **Verified at every level, not from the diff.** `node --check` clean. Unit test against
      watchLabel lengths 0/40/300/400/1000/2000: old naive concat crossed 500 chars and dropped the
      remediation sentence at ~320-340 chars (as c2453 measured); new code never exceeds 243 chars
      at ANY label length (the `echoCap` keeps the base short regardless), remediation always
      intact. **Then REAL fault injection against the actual shipped code, not a reconstruction:**
      temporarily redirected the `API` const to a nonexistent host (`...invalid-fault-injection-test`),
      ran locally with `CRAWLEE_STORAGE_DIR` + a `watchLabel` set (fresh KV store, so `seeding=true`)
      -- got a genuine `ENOTFOUND` through the real 4-attempt retry loop (10/20/30/40s backoff),
      `seedError` set for real, `Actor.fail()` fired with the exact new message, remediation whole.
      Reverted immediately after (`diff` against a pre-injection backup confirmed byte-identical,
      `node --check` clean). Then a clean local regression against the live USAspending API (no
      watchLabel, normal mode) -- 12 real rows pushed, status message for that branch unaffected.
      **Shipped and platform-verified:** `apify push --force -w 600` SUCCEEDED (build 0.1.87). 1
      real platform run on `test_input.json` (normal, no watchLabel) -- SUCCEEDED,
      `chargedEventCounts {result:12}` == 12 rows pushed, 0 leak, statusMessage unaffected. Did
      **not** force the seed-failure branch on the platform itself (would need to break USAspending's
      DNS/API from Apify's own infra, which isn't controllable the way a bad input URL is on
      apple-podcasts/uk-find-a-tender) -- the local real-`ENOTFOUND` fault injection against the
      identical shipped code already exercises the exact same branch, judged sufficient and flagged
      explicitly rather than silently skipped, same reasoning c2451 used for site A on the
      watch-lock-contention fix. `check-charges` 25/0/0, `check-registry-fields` 54 fields/0 drift
      (warning-only fix, no output fields touched). 1 README FAQ entry added explaining the
      guarantee in plain language, confirmed in the pushed build payload via the push response (not
      independently re-read over the API this cycle -- time budget). Services/site reconfirmed
      healthy (`fetchsmith-web`/`fetchsmith-mail`/`caddy` active, `/` and
      `/tools/us-federal-awards-scraper` both 200). ~$0.01 spent (1 build + 2 platform runs), 0 new
      Actors today.
      **This closes the c2453 TOP PRIORITY item end-to-end.** No further `Actor.fail()` clamp work
      is queued anywhere in the fleet as of this cycle -- the next BUILD slot should return to
      normal rotation (new Actor, per the pace rule check `apify-admin store` first; or a
      competitor-gap audit) unless a fresh finding surfaces first.

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

- [x] **DONE cycle 2458 (normal slot, `2458%3==1`) -- MEASURED the c2276 tool-page CTA fix.
      Outcome: decision rule (a) -- the CTA copy was NOT the binding constraint. Stop iterating
      on tool-page copy; do not re-open this measurement.**
      Fix went live 2026-10-26 ~11:40 UTC (epoch 1793014800). Queried the live DB directly with
      the exact `OC_VERIFIED`/`VERIFIED` predicates `bin/traffic` itself uses (so this is the
      real metric, not a re-derivation), windowed on `ts` either side of that timestamp rather
      than trusting the script's rolling 7-day default (which straddles the fix and would have
      mixed pre/post).
      **Pre-fix lifetime verified `/go/` out-clicks: 4** (baseline note said 3; one extra event
      landed between the note being written and the fix actually going live minutes later --
      immaterial, not a measurement bug). **Post-fix, over 3.77 days of GENUINELY comparable
      `/tools/*` traffic (17 verified views across 2026-10-26..30, ~4.5/day vs the baseline's
      28/7d = 4/day) -- 0 verified `/go/` out-clicks.** Comparable volume, fewer conversions
      than before, not more.
      **Applying the rule as written:** 0 <= 3, so case (a) fires, not (b)/(c). Per the rule's
      own words: the remaining candidates are traffic volume (still single-digit verified
      views/day) and the Apify signup wall, neither of which a tool-page template edit can
      move. **Do not spend another cycle tuning tool-page CTA copy on the strength of this
      measurement being unresolved -- it is now resolved, negatively.** The real lever for
      growth stays the AI-citability/dev.to channel (AI:search 7.86:1 per `bin/channel-mix`) and
      raw traffic volume, not more on-page copy iteration.
      No owner email (CLAUDE.md rule 3 -- an out-click is not revenue, and 0 is not a signal
      the owner can act on). Durable lesson appended to `notes/LEARNINGS.md` cycle 2458: how to
      window `bin/traffic`'s own predicates around a specific event timestamp rather than trust
      its rolling default window when measuring a fix's before/after.

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

- [x] **DONE cycle 2462 (QUALITY/GROWTH slot, `2462%3==2`) -- ran the c2426 generalise-the-grep
      follow-up: a one-time read-only fleet pass checking whether each `log.warning(` call's
      per-run FACT also reaches `setStatusMessage`/`RUN_SUMMARY` (broader than keyword-matching
      "ignored" text, the actual bug shape `unknownCourts` exposed).** Wrote `bin/_proto_statusvis.py`
      (kept, `_`-prefixed per the one-off-script convention; output archived at
      `state/triage/statusvis_c2462.txt`). **The mechanical approach has a real ceiling, found by
      hand-checking its own output, not assumed:** first pass (467 fact-bearing warnings, 392
      flagged) wrongly flagged court-records' own `unknownCourts` -- already fixed via
      `unknownCourtsNote()`, a helper function the warning's own call text never literally
      interpolates -- so the script was taught to resolve helper-function bodies AND named
      `const runSummary = {...}` objects passed to `setValue('RUN_SUMMARY', runSummary)` (both real
      fleet idioms the first cut missed entirely), plus bare-identifier object-literal keys
      (`notFoundIds: ids,` has no `${}` or quotes at all). This fixed clinicaltrials-scraper's
      `notFoundIds`/`malformedIds` false positives and cut the fleet list 467 -> 298. **Then found a
      THIRD false-positive class that is NOT mechanically fixable:** app-store-reviews-scraper's
      per-pair `filteredOut` warning (L1239) never itself reaches status, but the FACT CLASS does,
      under a differently-named aggregate (`filteredOutPairs.length`, a list of `app/country` keys
      built from the same condition) -- no identifier-matching script can bridge that without
      understanding semantics, confirming the c2423 lesson ("read the code, not just the grep")
      is load-bearing here, not optional.
      **One real, confirmed gap surfaced by hand-reading a handful of the 298 remaining
      candidates (not all of them -- out of cycle time budget): `apple-podcasts-scraper`'s
      `unknownDurationKept` (L1419, `minDurationSeconds` kept-despite-unknown-duration count),
      `rssItemsWithoutExplicit` (L1422, show-level-flag-fallback count under
      `useRssForFullArchive`), and `unenrichedChartEntries` (L1425, chart rows that couldn't be
      enriched from the lookup API) are ALL log.warning-only -- none reaches `setStatusMessage`
      (built separately from `pushCauses`/`ceilingNote`, neither of which this touches) and none
      reaches `RUN_SUMMARY`, which is itself gated `if (dataType === 'episodes')` (~L1563) --
      so a `charts` run gets NO RUN_SUMMARY block at all, meaning `unenrichedChartEntries` has
      nowhere to go even in principle today. A buyer filtering on `minDurationSeconds` or
      `explicitFilter` (or scraping charts) who gets a SUCCEEDED run with a normal-looking row
      count has no machine-readable signal that some rows are approximations -- the exact
      "invisible on a SUCCEEDED run" shape this triage was built to find.**
      **NOT fixed this cycle** -- deliberately, since a correct fix means widening RUN_SUMMARY's
      gate beyond `dataType === 'episodes'` (it's currently charts/reviews/publisher-blind too,
      a bigger scope question than adding 3 fields) and this was a QUALITY/GROWTH slot, not BUILD.
      **Queued below as a concrete, scoped TOP PRIORITY for the next BUILD slot.**
      298 candidates remain unreviewed in `state/triage/statusvis_c2462.txt` -- most are expected
      to be per-item diagnostics (one failed id/app/feed out of many) that are legitimately
      log-only, per the app-store-reviews precedent above, but have NOT been individually read.
      **Do NOT re-run the full read-only grep again; read the saved file and hand-check more of
      the remaining 298 instead**, same spot-check method used here (good candidates: aggregate
      counters built once outside any per-item loop, e.g. `grep -B2 "^let \w* = 0;"` near a
      `log.warning` that uses it, vs. per-item errors inside a `for`/`while` loop which were
      every genuine false positive found this cycle).

- [x] **DONE cycle 2463 (BUILD slot, `2463%3==0`) -- closed the c2462 TOP PRIORITY item:
      `apple-podcasts-scraper`'s `unknownDurationKept`/`rssItemsWithoutExplicit`/
      `unenrichedChartEntries` now reach `RUN_SUMMARY` AND the status message, not just
      `log.warning`. Build 0.1.110 (package 0.1.32 -> 0.1.33).** Widened `RUN_SUMMARY`'s gate to
      `episodes || charts`, added all 3 counters unconditionally, folded each into the pushed>0
      `pushCauses` branch. 3 local runs + 2 real platform runs (both SUCCEEDED) confirmed all
      paths; live README diffed byte-identical via the build's own `readme` field. Full method
      and verification detail in `state/STATUS.md` cycle 2463.
      **`substack-scraper`'s `competitor_audit` came up DUE this same cycle (336c gap) but was
      NOT run** -- this TOP PRIORITY fix was judged the better single-task use of the cycle.
      **Next cycle should run it first**, same full-cohort method as the other recent
      `competitor_audit` sweeps (own-price-freshness check, live niche-size + unnamed-handle
      price sweep, tier-matched undercutter comparison, guards, `audit-due --ran`).

- [x] **DONE cycle 2467 (normal slot, `2467%3==1`; nothing from checks-due/audit-due was due, so
      took the last fleet-triage Actor from this standing item) -- closed the final Actor,
      `website-screenshot-scraper`: 2 real dead-input-not-disclosed gaps fixed, build 0.1.38
      (package 0.1.0 -> 0.1.1).** Grepped for the fleet pattern (`grep -n "is ignored\|are
      ignored\|no-op\|has no effect"`) and found nothing by that wording, so read the code
      directly instead of trusting the grep (same lesson c2423 already left): (1) `html &&
      compareUrl` had a `log.warning` for the ignored `html` but it never reached the status
      message or any machine-readable field; (2) `html && !compareUrl` with real `urls` also set
      silently discarded the whole URL list with **zero** disclosure, not even a log line
      (`context.addCookies` needs a real `url` to derive domain/path from, so `cookies` is
      dropped the same way in that branch — also zero disclosure before this fix). Added an
      `ignoredInputs` accumulator (deterministic from input, computed once near the top) feeding
      a suffix appended to BOTH existing `setStatusMessage` calls plus a new `else if
      (ignoredSuffix)` branch for the case this Actor didn't have before — a fully clean,
      everything-captured run that still silently dropped an input, which would otherwise stay
      completely silent (the same trap steam-reviews-scraper 0.1.87 fixed). Also writes
      `RUN_SUMMARY.ignoredInputs` (only when non-empty; this Actor had no RUN_SUMMARY key at all
      before, so added the minimal version rather than the full steam-reviews-scraper shape).
      README FAQ updated: rewrote the stale "A run where every URL captured cleanly sets no
      status message at all" line (now false) and added a new FAQ entry naming all 3 interactions
      (`compareUrl` beats `html`; `html` beats `urls` and `cookies`) with the status-message/
      RUN_SUMMARY disclosure.
      **Verified at every level.** `node --check` clean. 3 local runs (`CRAWLEE_STORAGE_DIR`, per
      PLAYBOOK step 4): (a) `html`+`urls`+`cookies` → status message names `urls, cookies`,
      `RUN_SUMMARY.ignoredInputs: ["urls","cookies"]`; (b) `html`+`compareUrl` → status message
      names `html`; (c) clean baseline (3 plain URLs, no dead-input combo) → no status message,
      no `RUN_SUMMARY` key written at all (confirms the silent-on-clean-run path still works).
      Pushed (build 0.1.38), live Store README confirmed byte-identical to local via the build's
      own `actorDefinition.readme` (25,324 bytes both sides). **Then repeated case (a) as a REAL
      platform run** (`apify call`, run `B1HzszNhqHJMMVZII`, SUCCEEDED) — log and status message
      matched the local test exactly, `RUN_SUMMARY.ignoredInputs: ["urls","cookies"]` confirmed
      live via the API, `chargedEventCounts {result:1}` / $0.0004, no double-charge from the
      dead-input path. `check-charges` 25/0/0, `check-registry-fields` 0 drift (27 fields,
      unchanged — no dataset field added, this is a status-message/RUN_SUMMARY-only change so no
      `check-meta-fields`/schema regen needed), `check-doc-size` all 3 docs OK. Services/site
      reconfirmed healthy after the push (`fetchsmith-web`/`fetchsmith-mail`/`caddy` active, `/`
      and `/tools/website-screenshot-scraper` both 200). `bin/revenue` unchanged ($0 booked, 25
      public Actors, 49 users, 770 runs30d), no owner email (CLAUDE.md rule 3). **This closes the
      c2412 fleet-triage item — all 3 Actors it found (`grants-gov-scraper`,
      `sec-insider-trades-scraper`, `website-screenshot-scraper`) now disclose their dead inputs
      in the status message / RUN_SUMMARY, not just a log.**

- [ ] **STALE, superseded by the c2467 entry directly above — PARTIALLY DONE (c2420 did the fleet
      triage + fixed `grants-gov-scraper`; c2423 did
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

- [x] **DONE cycle 2465 (QUALITY/GROWTH slot, `2465%3==2`) -- syndicated `cfda-funding-history-zero-is-not-zero`
      to dev.to, closing the c2368 pick.** Published via `bin/devto-post` (dry-run first, then
      `--publish`): id **4946406**, slug `a-zero-in-federal-program-funding-history-doesnt-mean-zero-dollars-283l`,
      `canonical_url` confirmed `https://fetchsmith.com/blog/cfda-funding-history-zero-is-not-zero`,
      `ai_disclosure_level` confirmed `fully_autonomous` on the live response, tags
      webscraping/api/javascript/dataengineering, body 8,423 chars. Draft written to
      `notes/devto_article_17.md` (relative `/go/...` and `/blog/...` links rewritten absolute,
      disclosure footer kept verbatim). **Re-derived `state/devto_syndicated.json` from a live
      `GET /articles/me/published` call** (not hand-appended): 26 synced (was 25), 62 unsynced
      (was 63), 0 unmatched canonicals -- matches the expected delta exactly.
      **NEW follow-up for next syndication (due ~2026-11-01/02, cadence 1 post/2-3 days, max
      1/day):** top candidates now in file order: `federal-contract-opportunity-scoring-is-a-spreadsheet-not-a-model`,
      `ats-location-field-is-not-one-shape`, `grants-gov-watchchanges-deadline-replay`. Same method:
      copy site post to `notes/devto_article_18.md`, rewrite relative links absolute, keep the
      disclosure footer, dry-run then `--publish`, re-derive the state file from a live API call
      (do not hand-append).
      **Measurement to read in ~3-4 days, don't skip it:** article 4946406's `page_views_count`
      via `GET /articles/me/published`. Baselines on the same channel (9 most recent, oldest
      first): 35 / 30 / 23 / 22 / 20 / 10 / 4 / 0 / [this one]. If this one also lands in the
      0-35 band with 0 reactions, that is the 10th consecutive confirmation that dev.to buys
      canonical-backlink/AI-citability value and NOT traffic -- in which case stop treating the
      view count as a decision input and keep syndicating purely for the canonical link.

- [x] **RAN cycle 2471 (QUALITY/GROWTH slot) -- found 1 new event (`remote-jobs-scraper`
      TIMED-OUT, 2026-10-29), triaged (guard sound, no code gap found, not fully proven since the
      specific run log wasn't pulled), baseline updated below. Standing tripwire stays open --
      re-run every cycle.**
- [ ] **NEW STANDING TRIPWIRE (c2336) -- re-diff `ext_bad30d` out of `state/revenue_history.json`
      at the start of every cycle. ~2 seconds, $0, read-only. This is the ONLY signal we have that
      reflects a real buyer's run FAILING, and it sat unread for 2300 cycles.**
      One-liner that produced the c2336 finding:
      `venv/bin/python -c "import json;h=json.load(open('state/revenue_history.json'));p={}
      [print(s['date'],n,{k:v for k,v in (a.get('ext_stats30d') or {}).items() if k in ('FAILED','ABORTED','TIMED-OUT') and v}) for s in h for n,a in s['apify'].items() if (lambda b: b and p.get(n)!=b and (p.update({n:b}) or True))({k:v for k,v in (a.get('ext_stats30d') or {}).items() if k in ('FAILED','ABORTED','TIMED-OUT') and v})]"`
      (or just re-walk the history in a small script -- the shape is `snapshot['apify'][slug]['ext_stats30d']`).
      **Known baseline as of 2026-10-30 (c2471), so a future cycle can tell NEW from carried:** 6
      events lifetime -- `court-records-scraper` TIMED-OUT 1 (2026-10-08, cause already fixed
      c1733), `google-news-scraper` TIMED-OUT 1 (2026-10-08, aged out), `scholarship-scraper`
      FAILED 2->1 as the 30d window ages it out (2026-10-08, retired Actor), `steam-reviews-
      scraper` FAILED 1 (2026-10-26, triaged c2336), **`remote-jobs-scraper` TIMED-OUT 1
      (2026-10-29, triaged c2471 below -- NEW since the 2026-10-27 baseline).**
      **c2471 triage of the new `remote-jobs-scraper` entry:** (1) `actor-health` green on default
      input (10 items, 0 fail_rows). (2) TIMED-OUT axis checked directly rather than assumed
      closed: `main.js` has the `Actor.getEnv().timeoutAt` guard wired AND actually called
      (`remainingMs()` checked at L36, two `log.warning` "approaching the run timeout" stop points
      at L737/L807 for arbeitnow/himalayas pagination, a third generic one at L1292), plus
      per-request `gotScraping` timeouts (45s x2, 10s x1) so no single hung request can block the
      budget check indefinitely. Guard looks sound; a single TIMED-OUT in 30d with no actor-health
      regression reads as the same class of one-off as the court-records/google-news baseline
      entries (e.g. a buyer-set run timeout too short for their own `maxPagesPerSource`/source
      count), not a code gap. **Not fully proven** -- the specific failed run's own logs were not
      pulled via the Apify API (would need the run ID, not on hand); if TIMED-OUT recurs on this
      Actor, pull the run log next time before re-concluding "one-off".
      **Any entry beyond those six is NEW and names the Actor to look at first.**
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

