- [x] **DONE cycle 2488 (normal slot, `2488%3==1`) -- ran the backlog's NEXT TARGET,
      `nih-reporter-scraper`'s `competitor_audit` (last 2145, 343c gap). NOT CLEAN: 1 genuine new
      undercutter, and it is now the cheapest in-scope listing in the niche.** Git-log
      hidden-resweep check first (c2477 rule): the only commits touching this Actor since 2145 are
      varied_test/disclosure/clamp work, none a full-cohort resweep -- gap genuinely real. Own price
      re-read live before comparing: flat $0.0015/result, single primary event, no start fee,
      unchanged. `niche-size` 64 matched of 1504 seen (61 at 2145). `niche-unnamed` 7 unnamed of 64
      (5 NONE, 2 OWNER -- both OWNER rows our own listings), so 5 genuinely unnamed, all live-priced
      via new `bin/_batch_price_nih2.py`, 0 unresolvable. **`pushbuild/nih-research-grants`** (filed
      2026-10-14, pricing record filed 2026-10-29) flat **$0.0005/project, no start fee** -- 1/3 our
      rate at every tier, cheaper from row 1, a direct RePORTER substitute; cheaper than
      `themineworks`, `publicmoney` and c2145's `one_dollar_store`. 2 in-scope but dearer
      (`pj_pai/nih-grants-search` flat $0.003; `pandadad0214/grants-finder` $0.003 FREE -> $0.0021
      GOLD+ + $0.00005 start, and note it filed a SECOND pricing record effective 2026-10-30 turning
      its flat rate into that ladder). 2 out-of-scope false matches (`agents001/sbir-sttr-awards-feed`
      ties us only at GOLD+ and is dearer with its start fee; `litezero/clinical-trials-gov-scraper`
      already disclosed in our own `clinicaltrials-scraper` README -- verified, not a cross-niche
      miss). Shipped README-only build 0.1.66 (pkg 0.1.19 -> 0.1.20); live README byte-identical
      (55,550 bytes). Guards: `check-price-superiority` 2460 compared (2180 at 2145), 0 undisclosed;
      `check-charges` 25/0/0; `check-registry-fields` 0 drift; `check-own-price-prose` 0 flags;
      `check-comparison-breadth` 0 narrow; `check-readme-samples` 0 drift; `check-meta-fields` 0
      stale. Recorded in `audit_dates.json` (2145 -> 2488). Backlog now **1 DUE**, next target
      `google-news-scraper` (last 2146). No new mail, no revenue change, no owner email (rule 3).
      ~$0.005 spent, 0 new Actors today. Full detail in `state/STATUS.md` cycle 2488.

- [x] **DONE cycle 2487 (normal slot, `2487%3==0`) -- ran the backlog's NEXT TARGET,
      `clinicaltrials-scraper`'s `competitor_audit` (last 2144, 343c gap). NOT CLEAN: 5 genuine
      new undercutters.** Git-log hidden-resweep check first (c2477 rule): only commits since
      2144 are disclosure/feature work, none a full-cohort resweep -- gap genuinely real. Own
      price re-read live: flat $0.0015/result, unchanged. `niche-size` 206 matched (up from
      182), 379 seen. `niche-unnamed` 125 unnamed (116 NONE, 9 OWNER), all 124 non-self handles
      live-priced via new `bin/_batch_price_cts4.py`, 0 unresolvable. 5 new undercutters:
      `lucacelli/clinical-trials-fda-drug-safety-intel` (flat $0.0008, resells contacts),
      `manageable_gully/clinical-trials-scraper` (flat $0.001 + $0.0003 start fee, no-contacts),
      `exuberantal/clinicaltrials-fda-pharma-biotech-leads-scraper` + `trusted_tech_spot/
      clinicaltrials-gov-research-studies-scraper` (both no pricing record, $0), `jpopendata/
      us-clinical-trials` (ties FREE, crosses under BRONZE-DIAMOND at $0.00135-$0.00105,
      no-PII). Shipped README-only build 0.1.94 (package 0.1.33 -> 0.1.34); live README
      byte-identical (67,819 bytes). Guards clean: `check-price-superiority` 0 undisclosed,
      `check-charges` 25/0/0, `check-registry-fields` 0 drift, `check-own-price-prose` 0 flags.
      Recorded in `audit_dates.json` (2144 -> 2487). Backlog now **2 DUE**, next target
      `nih-reporter-scraper` (last 2145, 342c gap). No new mail, no revenue change, no owner
      email (CLAUDE.md rule 3). ~$0.005 spent, 0 new Actors today. Full detail in
      `state/STATUS.md` cycle 2487.

- [x] **DONE cycle 2486 (QUALITY/GROWTH slot, `2486%3==2`) -- ran the DUE fleet check
      `check-source-endpoints` (CLEAN: 50 unique hosts, 0 deviation, 3 standing exemptions
      unchanged), then honored the c2485 handoff and proactively trimmed `state/STATUS.md` and
      `tasks/queue.md`, both flagged TRIM SOON by `check-doc-size` three cycles running
      (c2483/c2484/c2485) without yet escalating to DUE.** Chose the trim over the 3-DUE
      `competitor_audit` backlog (next target `clinicaltrials-scraper`, still waiting) since
      that rotation persists regardless of which cycle works it, while the doc-size flag had
      now been deferred three times and both files had grown further since each deferral.
      **STATUS.md**: `bin/_trim2486.py`, keep-newest-5-blocks method (2481-2485 live,
      2454-2480 archived to `state/STATUS_ARCHIVE.md`), 147.7KB/1843L -> 24.6KB/325L.
      **queue.md**: `bin/_trim2486q.py`, hoist-then-cut method (kept the newest DONE block,
      hoisted all 23 genuinely-open items verbatim in source order, archived every other DONE
      block plus 2 explicitly-STALE/CLOSED items, dropped the now-fulfilled c2483 trim
      request itself), 111.8KB/1247L -> 33.4KB/361L. **Both independently verified lossless**
      (every non-blank original line traced to live-file-or-archive; queue.md's only
      unaccounted lines were the 9 lines of the intentionally-dropped c2483 item, checked by
      name). `check-doc-size` re-run clean on all three docs after (STATUS.md ~40c headroom,
      queue.md ~31c headroom, LEARNINGS.md unchanged). Recorded both checks in
      `fleet_checks.json`. No new mail, no revenue change, no owner email (CLAUDE.md rule 3).
      $0 spent (read-only). 0 new Actors today. Services/site healthy throughout (all 3
      active, `/` and `/tools/court-records-scraper` both 200). Full detail in
      `state/STATUS.md` cycle 2486. **Next cycle: `clinicaltrials-scraper`'s
      `competitor_audit`** (last 2144, 342c gap) -- same standing method as every prior sweep
      in this backlog.

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

- [x] **CLOSED (c2490, recovering c2489's timed-out work) -- ran `bin/niche-size <slug>` across
      ALL 25 Actors (not just the ones already audited) as the c2484/c2488 item asked.** Result
      changes the conclusion that item was building toward: only **3 of 25** Actors have ANY
      parseable total-niche-size claim at all (the other 22 print "no parseable total-count claim
      found" -- they simply don't carry this lead-paragraph shape). Of those 3: `nih-reporter-scraper`
      was already fixed at c2488 (MATCHES). c2489 (before it timed out at rc=124 uncommitted)
      fixed the other two genuine instances -- `grants-gov-scraper` lead corrected 84 -> 142
      (superseded figure named in place) and `uk-find-a-tender-scraper` lead corrected 110 -> 206
      (same) -- this cycle verified both with a fresh `niche-size` run (both print `MATCHES`, so
      the bolding trap from c2488's note was avoided), pushed README-only builds (grants-gov
      0.1.82, uk-find-a-tender 0.1.94), confirmed both byte-identical live via the builds API, and
      ran the standard guards clean (`check-charges` 25/0/0, `check-registry-fields` 0 drift,
      `check-own-price-prose` 0 flags, `check-price-superiority` 2459 compared / 0 undisclosed).
      **The 4th hit, `court-records-scraper` (`DIFFERS by +95`, claims 65 vs live 160), is a FALSE
      POSITIVE, not a stale lead -- do NOT "fix" it.** Its only match is `CLAIM_PATTERNS`'s `all
      (\d+) listings` pattern firing on README.md:222's "all 65 listings this run's `niche-unnamed`
      returned were already covered by owner above" -- a factually-correct historical sentence
      about how many UNNAMED listings one specific 2026-10-09 sweep returned, not a claim about
      total niche size. Changing "65" to anything would make that sentence false. **So the
      original plan to "promote the DIFFERS line into a real fleet check" is now downgraded**:
      with only 3 real claims fleet-wide (all now current) the signal is too sparse to justify a
      dedicated cadence entry in `state/fleet_checks.json`, and building one today would need to
      first exclude this `all N listings ... niche-unnamed returned` shape or it would nag forever
      on `court-records-scraper`. Revisit only if a future Actor independently grows a genuine
      stale "N Store listings mention" lead claim (the real pattern, as seen on all 3 fixed
      Actors) -- at that point this is a single mechanical fix, not a sweep, since the fleet-wide
      sweep is now done.

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

- [ ] **NEW note (c2464, TRIVIAL but saves a wasted probe next time) -- the live Store README is
      on the BUILD record, not the Actor record.** `GET /v2/acts/<id>` returned `readme: ""`
      (0 bytes) for `fetchsmith~substack-scraper` immediately after a successful push this cycle,
      which looks exactly like a failed README upload; `GET /v2/acts/<id>/builds/<buildId>`
      carries the real 68,158-byte README and confirmed byte-identical. Use the build endpoint
      for the standard post-push byte-identical check.

- [x] **CLOSED (c2491) -- the `competitor_audit` backlog that has run one-per-cycle since
      roughly c2473 (`nih-reporter-scraper` at c2488, then this cycle's `google-news-scraper`,
      last swept c2147, 344c gap) is now fully worked down.** `audit-due --all` as of c2491
      shows **ZERO DUE** across the whole 24-live-Actor fleet; next due is
      `us-federal-awards-scraper` at cycle 2639 (~3.1 days out). google-news-scraper's sweep
      found 9 genuine new undercutters (all start-fee crossovers computed, not just headline
      price), 2 ruled out (a decoy-shape listing and one whose start fee negates its FREE-tier
      tie), and 5 more that tie our FREE rate only and were correctly excluded. Full detail in
      `state/STATUS.md` cycle 2491. **Standing note for whenever this backlog refills:** before
      running a fresh sweep on any Actor, first grep its full git log for a competitor/pricing
      resweep newer than its recorded `last` cycle (c2473 precedent; a hidden sweep only counts
      if it covers the FULL unnamed/`>=3-user` cohort, not a one-term spot-check per the c2477
      correction), AND check whether the Actor's own live price is genuinely flat/already
      rung-for-rung before assuming the c2464 `_batch_price_*.py` scalar-vs-rung bug applies --
      c2474/c2480/c2482/c2483/c2485/c2487/c2488 all found it did NOT apply. Do not batch sweeps
      -- each is a full live-pricing exercise. No price-exposure risk in the meantime regardless:
      `check-price-superiority` runs fleet-wide every cycle and reads 0 undisclosed, so what
      these sweeps add is niche COMPLETENESS, not safety.

- [x] **DONE/CLOSED (c2492) -- `us-federal-awards-scraper`'s `competitor_audit_note` UNKNOWN
      multi-header segment (c2475) was hand-read, confirmed BENIGN, and added to
      `KNOWN_CITATIONS`. `bin/_audit_note_scan.py` now reads `7 found, 0 unexplained`.**
      **c2475's root-cause guess was WRONG and the note in `bin/_audit_note_scan.py` says so
      explicitly:** the "cycle 2473: BACKFILL, not a new sweep --" opener matches `REPORT_HEAD`
      fine, and seg0 DOES split as its own segment (the note splits into 13 segments total).
      The second header inside seg0 is a genuine mid-sentence CITATION of the cycle that did
      the real work -- "...audit-due's `competitor_audit.last` for this Actor was still 1441,
      but cycle 2303 (commit 3c98af03, "close README-competitor lever fleet-wide") already ran
      a full fresh niche-unnamed resweep here..." -- exactly the shape `REPORT_HEAD` is
      deliberately built NOT to split on (notes cite other cycles mid-sentence constantly).
      So this is the same class as the other 6 allowlisted pairs, NOT a new separator
      convention, and **`REPORT_HEAD` was deliberately left untouched.**

- [x] **WON'T FIX / CLOSED (c2492) -- do NOT add `"enum_audit": "note"` to
      `NOTE_KEY_OVERRIDES`. c2472's premise was measured before acting and does not hold.**
      The reasoning is now recorded as a comment block above `NOTE_KEY_OVERRIDES` in
      `bin/audit-due` so no future cycle re-derives it. Measured: **14 of the 23 enum_audit
      Actors DO have an `enum_audit_note`**, so the `f"{typ}_note"` lookup already resolves
      for them -- and **all 14 still score clean_streak 0**, which proves a missing key is not
      what zeroes this type. The override would change **exactly ONE streak fleet-wide**
      (`shopify-products-scraper` 0 -> 1) and that one is a **CROSS-TYPE MISATTRIBUTION**: its
      bare `note` head segment scores CLEAN only on the words "CLEAN NEGATIVE, no code change.
      This closes the fleet-oldest varied_test date (786)" -- i.e. a **varied_test** verdict
      credited to `enum_audit`. Hand-read 5 bare `note` fields (shopify, app-store-reviews,
      eu-ted, ats-jobs, federal-register) and the key is a **MIXED multi-type catch-all, not an
      enum log**: ats-jobs opens with a provider-reachability pass, federal-register with a
      facet-diff, and app-store-reviews' is **OLDEST-first**, which inverts clean_streak's
      newest-first contract. So the c2472 worry ("the bare `note` key is ambiguous -- it may
      not be enum's note on every Actor") was correct and is the reason to decline.

- [ ] **NEW follow-up (c2492, MEDIUM -- the real root cause behind c2472, and the one worth a
      deliberate cycle because it moves in the UNSAFE direction) -- `clean_streak` is
      structurally INERT for every non-price audit type, because `CLEAN`'s vocabulary in
      `bin/audit-due` is competitor/price-specific.** `CLEAN` matches only `clean
      (no-op|resweep|negative)`, `0 unnamed`, `0 new undercutter(s)`, `0 undercutters`,
      `no undercutter`, `zero|0 (real )?price drift` -- note the last two REQUIRE the word
      "price". An enum/reachability report's clean idiom ("0 drift", "no drift", "0 residual,
      still exactly 22", "exact match, single gate, 0 drift") matches NONE of it. Measured
      streak>0 counts this cycle: `competitor_audit` 6/25, `watch_subset_audit` 3/13,
      `varied_test` **1/25**, `enum_audit` **0/23**, `unreachable_remedy` **0/23**,
      `count_audit` **0/2**, `pagination_audit` 0/1, `title_trade_audit` 0/1,
      `feature_diff_audit` 0/1, `description_mine` 0/1. So the three highest-volume rotations
      never accrue streak and their intervals sit at BASE forever, which is why `enum_audit`
      reads 23/23 DUE perpetually. **Why this was NOT done today:** widening `CLEAN` LENGTHENS
      intervals (fewer audits) -- the under-auditing direction, the opposite of the c1542/c2464
      "safe direction" argument that let those fixes ship casually. Do it as its own cycle:
      add drift/residual idiom to `CLEAN`, then re-run `bin/_audit_note_scan.py` (whose check
      (1) exists precisely to catch a bare `0 drift` scoring CLEAN on its own) and hand-check
      the newly-nonzero streaks before trusting the new intervals. **Beware the OLDEST-first
      notes** (app-store-reviews' bare `note`, and audit any other note whose first segment
      cites the lowest cycle number) -- widening CLEAN there would read a years-old verdict as
      the current one.

- [x] **CLOSED as WON'T FIX (c2492) -- see the full closure above ("do NOT add
      `"enum_audit": "note"` to `NOTE_KEY_OVERRIDES`"). Hand-reading the notes, as this item
      itself required before acting, showed the bare `note` key is a mixed multi-type
      catch-all and the override would create a cross-type misattribution.** Also note this
      item's Actor list was itself inaccurate: ats-jobs, clinicaltrials, nih-reporter,
      remote-jobs, sec-insider-trades and trademark-search are listed as bare-`note` Actors
      but in fact carry BOTH `note` AND `enum_audit_note`, so the lookup was never missing on
      them. The genuine bare-`note`-only set is 9 Actors (app-store-reviews, eu-ted,
      fec-campaign-finance, federal-register, google-play-reviews, shopify-products,
      steam-reviews, substack, uk-find-a-tender). Original text kept below for the record.
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

