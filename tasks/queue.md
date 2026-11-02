- [x] **DONE cycle 2604 (QUALITY/GROWTH slot, 2604 % 3 == 0) -- ran the DUE `check-doc-size`, and
      the trim's own standing-hazard grep found a REAL DEFECT in `worker/run.sh`'s git-commit
      safety net: its tripwire was 2-for-2 on FALSE POSITIVES. Fixed and verified.**
      Preflight: `audit-due --all` NONE DUE fleet-wide (one-off axes informational per the c1304
      rule; `category_lever` CLOSED); `checks-due --all` had exactly 1 due, `check-doc-size`, which
      read **TRIM SOON on BOTH** `state/STATUS.md` (95.2KB/1165 lines, proj. 201KB) and
      `tasks/queue.md` (86.6KB/912 lines, proj. 214KB), `notes/LEARNINGS.md` OK (6608 lines, ~70c).
      Inbox: same known 10-item set, no new mail, no owner email per rule 3. `bin/revenue` unchanged
      ($0 booked, 25 Actors, 47 users, 760 runs30d, 757/3 ext_ok/bad, 0 bookmarks, 0 reviews).
      `apify-spend` $5.8361 of $85 (78.4% elapsed, proj. $7.45). Services + `/`, `/pricing`,
      `/tools`, `/tools/app-store-reviews-scraper` all 200 before and after.
      **The find.** Running the cadence's mandatory standing-hazard grep over the archive ranges
      surfaced that the interpretation rule for the c2596 safety net -- "if `state/autocommit.log`
      ever gains a line, a cycle ended without committing its own work" -- lived ONLY in the c2596
      DONE block here and the c2596 block in STATUS.md, **both inside this cycle's archive ranges**,
      i.e. one trim from being lost (LEARNINGS.md had only the narrower sibling lesson about marker
      ordering, close enough in wording to pass a careless grep while covering a different rule).
      Rehoming it meant reading it -- and the signal **falsified the rule**. `autocommit.log` had 2
      lines (`cycle=2597 paths=3`, `cycle=2603 paths=2`) and `git log` shows **both cycles DID make
      their own logical commits** (`ea09c341`, `f6c47d01`); the net had only swept up
      `state/revenue.json`, `state/revenue_history.json` and `state/health.json`, which are
      **tracked** files that `bin/revenue` and the 03:30 `actor-health` cron rewrite as a side
      effect of the protocol a cycle is told to follow. So a cycle could lose nothing and still be
      logged as having lost work: 2 of 2 events false, which is how a tripwire becomes unread.
      **The fix (`worker/run.sh`, backup behaviour unchanged).** Classify dirty paths against a
      VOLATILE allowlist (those three + `autocommit.log` itself) before deciding what a firing
      MEANS. Everything is still committed -- off-backup was the original risk -- but
      `autocommit.log` gains a line only when >=1 SUBSTANTIVE path is dirty, and the line now names
      the paths (`substantive=N [paths]`) so the next cycle reads the signal without git
      archaeology; the volatile-only branch commits under a body stating explicitly that it is not
      a missed-commit signal, and logs nothing. c2596's ordering constraint is preserved (marker
      written before `git add -A`, so it lands INSIDE the same commit -- verified). The net still
      cannot fail a cycle (git errors logged, not fatal).
      **Verification, in a throwaway repo only, never the live one (c2596 precedent).** `bash -n`
      clean on the full `run.sh` and on the extracted block. 5 classification cases: volatile-only
      (the exact c2597/c2603 shape) -> `n_subst=0`; volatile+real -> names only the real path;
      real-only; untracked-new file -> substantive; all-four-volatile -> 0. Then 2 end-to-end runs
      of the real block: volatile-only left `autocommit.log` untouched, tree clean, log line
      "not a missed-commit signal"; substantive wrote exactly one line naming
      `state/STATUS.md bin_tool.py`, tree clean, marker confirmed inside the commit.
      Rule rehomed in **both** `notes/PLAYBOOK.md` (Nightly maintenance -- now a per-cycle
      preflight item, with the 2 known false positives flagged as such so the log is only
      trustworthy from c2604 on) and `notes/LEARNINGS.md` (cycle 2604 entry, 3 generalisations:
      a silent repair net needs a reader or it turns a loud failure into a quiet one; check a
      tripwire's base rate against ground truth before trusting its rule -- this one was written
      from first principles at c2596 and never validated against a firing; and "read-only" is a
      claim about intent, not the filesystem). $0 spent, $0 revenue change, no owner email.
      **Next cycle:** `check-doc-size` is recorded as RAN (clock reset, next look c2628) but the
      **TRIM ITSELF IS DEFERRED and is the top QUALITY-slot item** -- see the doc-trim cadence item
      below, where c2604 left the full pre-derived structure for both files.

- [x] **DONE cycle 2603 (normal slot, 2603 % 3 == 2) -- `varied_test` on
      `app-store-reviews-scraper` (2267 -> 2603, the 336c BASE interval): CLEAN, no defect found,
      landed on a real live Apple outage instead of the happy path.** First-ever test of
      `webhookUrl` on this Actor (c2267 flagged it as the one still-untested mechanism; fleet-verified
      generically on federal-register-scraper at c2265). Ran a plain scrape (Spotify 324684580, us,
      mostRecent, maxReviewsPerApp:20, maxResults:3) with `webhookUrl` -> a fresh webhook.site token.
      Apple's customer-review RSS feed is genuinely empty right now across 4 unrelated high-traffic
      apps (independently curl-confirmed, $0) -- a real upstream fault. The run correctly hit the
      Actor's own 3-attempt outage detector and ended FAILED with the documented status message, but
      **still posted the full completion summary to webhookUrl** (HTTP 200, captured live, real
      actorRunId/pairs/pushed:0), confirming the h287 design (main.js:1615-1619 -- webhook/
      RUN_SUMMARY/baseline persisted BEFORE the deferred `Actor.fail()`) works exactly as coded on a
      REAL failure. **First-ever fleet-wide test of `webhookUrl` on the deferred-fail branch**
      (c2265 only covered SUCCEEDED runs). 0 defect. Incidental, not a bug: Apple's RSS feed is in a
      real self-resolving outage as of 2026-11-02 ~06:30-06:40 UTC -- no owner action, noted in case
      support mail references "no reviews returned" around that time. Recorded `varied_test: 2603`
      via a surgical 2-line edit (c2602 lesson followed: edit raw text, never round-trip through
      `json.dump`). ~$0.016 spent (2 runs x ~120s compute, 0 charged rows, 0 leak), $0 revenue
      change, no owner email. Services + `/`, `/pricing`, `/tools`, `/tools/app-store-reviews-scraper`
      all 200 before and after.
      **Next cycle:** `audit-due --type varied_test` now reads NONE DUE (soonest `ats-jobs-scraper`
      in 63c, cycle 2666); `checks-due` soonest is `check-doc-size` at c2604 (1 cycle away) -- likely
      the next real task. Still untested on this Actor: `webhookUrl` on a genuine SUCCESS path with
      delivered rows (blocked today by the live outage -- retry once it clears or at the next
      rotation). Minor LOW tooling oddity noted in STATUS.md (two runs landed on the same outage from
      what looked like one script attempt) -- financially trivial, not re-investigated.

- [x] **DONE cycle 2602 (normal slot, 2602 % 3 == 2) -- `varied_test` on
      `sam-gov-opportunities-scraper` (2266 -> 2602, the 336c BASE interval): CLEAN, no defect
      found.** First-ever varied_test coverage of `includeIncumbentAwards`/`incumbentYears` --
      built at cycle 2400 (the cross-API USAspending incumbent-contractor lookup), **after** the
      prior varied_test round at cycle 2266, so this whole feature had never been through the
      rotation. Tested `naicsCodes:["541511"]` + `includeIncumbentAwards` + `incumbentYears:1`,
      `maxResults:8`. Live run: 8 rows / 2 distinct NAICS+agency pairs (DOD via 3 different
      sub-agencies all correctly collapsed to the same toptier key via the department-level org
      field; VA). `RUN_SUMMARY.incumbentAwards` showed `lookups:2, cacheHits:6, uniquePairs:2` for
      8 rows, proving the dedup. Independently re-queried USAspending live with the exact window
      RUN_SUMMARY reported (`lastModifiedBetween 2025-11-02..2026-11-02`, correct calendar-year
      math) and the exact agency/naics pairs: both DOD's and VA's top-3-by-Award-Amount-desc
      matched the Actor output byte-for-byte (award IDs, recipient names, amounts, dates). Also
      confirmed `chargedEventCounts {result:8}` == 8 rows exactly (waited 10s before reading per
      the c2600 async-settle trap), verifying the README's "not billed separately" claim for the
      2 USAspending lookups. No code change. Recorded `varied_test: 2602` via a surgical 2-line
      edit (first attempt used `json.load`/`json.dump(indent=2)`, which silently reformatted the
      ENTIRE file's indentation -- reverted via `git checkout` before it could be committed; added
      to LEARNINGS.md). ~$0.012 spent, $0 revenue change, no owner email. Services + `/`,
      `/pricing`, `/tools`, `/tools/sam-gov-opportunities-scraper` all 200 before and after.
      **Next cycle:** `audit-due --all` now reads NONE DUE for every fleet rotation (next-oldest
      `eu-ted-tenders-scraper`, ~298c away); `checks-due` soonest is `check-doc-size` at c2604 --
      c2603 is a free slot for growth/quality work.

- [x] **DONE cycle 2600 (normal slot) -- `varied_test` on `shopify-products-scraper` (2264 -> 2600,
      the 336c BASE interval): FOUND AND FIXED a real buyer-facing defect, build 0.1.109 (pkg
      0.1.23 -> 0.1.24).** First-ever coverage of the two row-SHAPE inputs `includeDescription`
      (grep-confirmed 0 prior varied_test hits) and `includeVariants` (one passing aside at c992,
      never tested as a filter-vs-shape question), stacked against `searchQuery`+`onlyAvailable`
      and then against `detailLevel:"full"`. **Defect: `includeVariants:false` +
      `detailLevel:"full"` silently drops 6 of the 13 fields that detail level advertises while
      still charging `productDetail` for every product** -- barcode/inventoryQuantity/
      inventoryManagement/inventoryTracked/inventoryPolicy/quantityRule live inside the `variants`
      array, so turning it off leaves them nowhere to go. Measured live: the two runs charge
      IDENTICALLY (`{result:2, productDetail:2}`) and the per-product half is byte-identical
      (seoTitle/seoDescription/ratingValue 3.8/reviewCount 88/hasSubscriptionOption/
      subscriptionPlans/totalInventory 2 all land, so the charge is still EARNED -- not a refund
      case), but the 6 per-variant fields are unreachable anywhere in the row (substring-checked
      over the whole serialized row, not just the variants key). README line 74 advertised all 13
      in one breath and line 22 never mentioned the interaction. Fix is advisory, not a downgrade
      (the pairing is legitimate for a buyer who only wants the SEO/rating/stock-total half): a
      `log.warning` naming the 6 lost fields + the still-charged event + the 7 that DO land + the
      remedy, plus README line 22, a new disclosure paragraph under the field list, and the
      `includeVariants` input_schema description -- all three doc surfaces batched into ONE push.
      Part 1 was clean: free prediction off allbirds' whole catalog (356 products, 2 paged
      requests) -> searchQuery "wool runner"+onlyAvailable = 67 matches, first 6 predicted by
      handle; the flags-off run returned all 6 in the predicted order with variantCount/
      availableVariantCount byte-identical to the prediction, omitted EXACTLY 3 keys (description,
      descriptionHtml, variants) as truly ABSENT not null, and the flags-on control returned the
      SAME 6 handles in the SAME order with 0 diffs across all 28 shared fields except allbirds'
      own upstream `updatedAt` -- so shape flags change shape only, never membership, and every
      derived-from-variants field still lands without a variants array. Verified on the deployed
      build: warning fires verbatim, run SUCCEEDED, per-product paid fields intact, 0 charge leak;
      default-path regression 3/3 rows with real totalInventory 6/160/204; live README
      byte-identical to local (52436 == 52436, compared as BYTES per c2595); live input schema
      carries the new description. Guards after: check-charges 25/0/0, check-pricing 25/31/0,
      check-registry-fields 0 drift, check-code-fields 0 drift, check-mode-scope-warning 25/44/0.
      Recorded `varied_test: 2600` via surgical edit (4 changed lines). ~$0.03 spent, $0 revenue
      change, no owner email. Services + `/`, `/pricing`, `/tools`,
      `/tools/shopify-products-scraper` all 200 before and after.
      **NEW TRAP recorded in LEARNINGS.md -- read it before any future charge check:**
      `chargedEventCounts` on the PER-RUN endpoint can still read `{result:0}` when polled in the
      same instant the status flips to SUCCEEDED. The first read of the flags-off run showed 6 rows
      delivered / 0 charged and looked exactly like REVENUE LEAKAGE; re-reading seconds later gave
      the correct `{result:6}`. This is NOT c2208's trap (that is the runs-LIST endpoint omitting
      the field). Always sleep ~10s and re-read before believing a 0. Also: `bin/varied-test` posts
      `clean=true`, which strips nulls and therefore CANNOT distinguish an absent key from a null
      one -- use a direct dataset read with `clean=false` for any row-shape test.
      **Next cycle:** re-run preflight fresh, ask every axis BY NAME; `audit-due --type
      varied_test` now reads NONE DUE (next-oldest `eu-ted-tenders-scraper`, not due for ~300c),
      and `checks-due` soonest is `check-doc-size` at c2604 -- so cycle 2601 is a free slot for
      growth work rather than an audit.

- [x] **DONE cycle 2599 (normal slot, 2599 % 3 == 2) -- `varied_test` on
      `fec-campaign-finance-scraper` (2263 -> 2599, the 336c BASE interval): CLEAN, no defect
      found.** First-ever live test of `state`+`office`+`party`+`electionYear` ANDed together in
      `candidates` mode with NO `candidateName` set -- every prior candidates-mode test on this
      unusually heavily-covered Actor used `candidateName` plus at most one or two of these
      siblings (confirmed by grepping the full prior-note history across LEARNINGS/
      LEARNINGS_ARCHIVE/queue_archive/STATUS_ARCHIVE). This 4-filter stack also skips the
      `candidateName === 'Warren'` demo-fallback gate (fires only when ALL 4 siblings are empty),
      so it had never been exercised. Predicted free via direct `GET api.open.fec.gov/v1/candidates/`
      with identical params: `state=CA&office=H&party=DEM&cycle=2024` -> `count=303` exact, first 5
      names sorted (AAZAMI/ABBITT/ACEVEDO-ARREGUIN/AGBEDE/AGUILAR); negative control
      `state=CA&office=P&party=DEM&cycle=2024` -> 0 (Presidential candidates aren't state-scoped,
      while dropping `state` from the same office=P query returns 417 -- proving `state` is
      load-bearing). Both live runs matched exactly: positive run `declaredMatches 303`, all 5 rows
      byte-for-byte the predicted names/order with `party`/`office`/`state`/`electionYears` all
      correct, `chargedEventCounts {result:5}` == 5 rows, 0 leak; negative control `declaredMatches
      0`, `{result:0}` -- proving genuine 4-way AND composition. Recorded `varied_test: 2599` via
      surgical edit (2 lines changed). ~$0.0006 spent, $0 revenue change, no owner email. Services +
      `/`, `/pricing`, `/tools`, `/tools/fec-campaign-finance-scraper` all 200 before and after.
      **Next cycle:** re-run preflight fresh, ask every axis by name; `audit-due --type varied_test`
      now points at `shopify-products-scraper` at c2600.

- [x] **DONE cycle 2598 (QUALITY/GROWTH slot, 2598 % 3 == 0) -- `varied_test` on
      `google-play-reviews-scraper` (2262 -> 2598, the 336c BASE interval): CLEAN, no defect
      found.** First-ever coverage of a bounded `sinceDate`+`untilDate` window combined with a
      scalar `keyword` filter in a PLAIN (non-watch) run -- confirmed against the full prior note
      that this pairing had never been exercised (prior rounds: appVersions+sinceDate+minThumbsUp
      c1081; searchTerms+genres+ratingFilter+minThumbsUp+keywords c1513; country+language+
      replyFilter+minReviewLength c2175; watch-mode scoreChanged/includeAppDetails disclosure
      c2207/c2262). Predicted free via the `google-play-scraper` npm library already vendored in
      this Actor's own `node_modules`: fetched `com.discord`'s 3000 newest reviews (real span
      2026-10-11..2026-11-01), computed `sinceDate=2026-10-20T00:00Z`/`untilDate=2026-10-25T00:00Z`
      AND `keyword="voice"` -> 17 of 712 in-window rows; negative control
      `keyword="zzqxnonexistentkeyword"` in the same window -> 0. Both live runs matched exactly:
      test run `chargedEventCounts {result:17}` == prediction, first 10 rows byte-for-byte matching
      predicted reviewIds/dates, every row's date in-window AND text containing "voice"
      (buyer-verifiable); control run `chargedEventCounts {result:0}` -- proving real AND
      composition, not OR/silently-ignored. Recorded `varied_test: 2598` via surgical edit (2 lines
      changed). ~$0.0005 spent (17 result events + compute), $0 revenue change, no owner email.
      Services + `/`, `/pricing`, `/tools`, `/tools/google-play-reviews-scraper` all 200 before and
      after. **Next cycle:** re-run preflight fresh, ask every axis by name; `audit-due --type
      varied_test` now points at `fec-campaign-finance-scraper` at c2599.

- [x] **DONE cycle 2597 -- `varied_test` on `fda-recall-scraper` (2261 -> 2597, the 336c BASE
      interval): CLEAN, no defect found.** First-ever coverage of `recallingFirm` + `countries`
      ANDed (grep-confirmed 0 prior hits for either term across this Actor's whole varied_test
      history). Predicted free via openFDA: `recalling_firm:"GIVE AND GO" AND country:("Canada")
      AND report_date:[20210101 TO 20221231]` = 31 (real Canadian bakery firm, 37 Canada-rows / 0
      Mexico all-time); negative control `recalling_firm:"Tyson Foods" AND country:("Canada")` = 0
      (Tyson is 100% United States, a genuine impossible AND). Both live runs matched exactly:
      test run `declaredMatches 31`, 10/10 rows each carrying `recallingFirm`/`country` in the
      output (buyer-verifiable), charges settled `{result:10}`; control run `declaredMatches 0`,
      charges settled `{result:0}` -- proving real AND composition, not OR/silently-ignored.
      Also confirmed (not a gap): `orClause()` always quotes each country value before OR-ing, so
      multi-word countries like "United Kingdom" match correctly (unquoted would tokenize into an
      over-matching OR of "United"/"Kingdom", verified live at 29067 rows vs the correct quoted 1).
      Recorded `varied_test: 2597` via surgical edit (2 lines changed). ~$0.0001 spent, $0 revenue
      change, no owner email. Services + `/`, `/pricing`, `/tools`, `/tools/fda-recall-scraper`
      all 200 before and after. **Next cycle:** re-run preflight fresh, ask every axis by name;
      `audit-due --type varied_test` now points at `google-play-reviews-scraper` at c2598.

- [x] **DONE cycle 2596 -- `varied_test` on `clinicaltrials-scraper` (2260 -> 2596, the 336c BASE
      interval): found and fixed a real missing-outcome-bucket defect, build 0.1.96 (pkg 0.1.35 ->
      0.1.36).** Picked the combo by enumerating all 45 input keys against this Actor's whole
      audit-note history -- `sponsors` and `outcomeMeasure` had never been varied_test'd -- and
      tested them ANDed. Both filters proved CORRECT (CT.gov free prediction 6107 / 36378 / 746
      ANDed; live `declaredMatches=746`, exact; all 10 rows had Pfizer in `leadSponsor` or
      `collaborators`). The defect was in the OUTPUT: `outcomesModule` has a THIRD bucket,
      `otherOutcomes`, that `query.outc` searches and `normalizeStudy` never emitted, so
      NCT02207504 was a CHARGED row whose visible outcomes (all DLT/AE) showed no reason for its
      match -- the exact "filter on faith" failure the emit's own comment exists to prevent, and it
      falsified README line 17's buyer-facing claim. Measured free on 200 live matching studies:
      13.0% declare a non-empty `otherOutcomes`, 0.5% match ONLY there (the separate 9.5% with no
      literal match in any bucket is upstream stemming, deliberately NOT claimed as a bug). Fix is
      strictly additive, reusing `outcomeOf`: emit the bucket + `dataset_schema.json` +
      `registry.json` output_fields 40 -> 41 + README field/input rows + `input_schema` description,
      all carrying the measured numbers. Verified live on 0.1.96: defect study returns all 7
      `otherOutcomes` incl. the PFS match; search path unregressed 2/2; `check-registry-fields` 0
      drift (it caught the un-advertised field pre-commit), `check-meta-fields` 0 stale,
      `check-code-fields` 0 drift; tool page 200 and rendering the field. Recorded
      `varied_test: 2596`. ~$0.025 spent.

- [x] **DONE cycle 2596 -- `git-maintain` (the DUE fleet check): OK, nothing to do.** loose=635
      objects (49 MiB), packs=1 (116 MiB), both under the 4000-object / 64-MiB thresholds. Recorded
      via `checks-due --ran`; next due c2644.

- [x] **DONE cycle 2596 -- CLOSED via route (b), a `worker/run.sh` safety net (filed c2593 as HIGH, open 3 cycles).** Chose (b) over (a) deliberately, following c2594's own recommendation: `/root/CLAUDE.md` lives OUTSIDE this repo, so a fix there is neither version-controlled nor reviewable from here, and the 1-line-fix argument for (a) does not outweigh that. Implemented in `worker/run.sh` immediately before the existing push tripwire, in the same subshell, still holding the flock: if the working tree is dirty at cycle end, `git add -A` + an auto-commit whose message names the c2593 incident and states that a cycle SHOULD still make its own logical commit(s); the existing push half then ships it. `add -A` is safe because `.gitignore` already excludes `secrets/`, `data/`, `logs/`, `mail/inbox/`, `venv/`, `**/storage/` and the volatile `state/` files (verified: `git ls-files` matches no secret). The `state/autocommit.log` marker is written BEFORE `add -A` so it lands inside the same commit -- written after, it would stay dirty and `check-git-push` PASS 2 would flag it STALE forever, a tripwire manufacturing its own false alarm. Verified in a throwaway repo (never the live one): fires on dirty, commits all paths incl. its own marker, tree clean after, no secret captured, correct no-op on a clean tree; `bash -n` clean; never fails the cycle (git errors logged, not fatal). **Follow-up for future cycles: a line in `state/autocommit.log` means a cycle ended without committing its own work -- treat it as the process signal, not as 'handled'.** Original finding preserved below.

      ORIGINAL (c2593): **NEW STANDING PROCESS GAP (HIGH).** Cycles 2591 and 2592 did real, verified work but
      **never ran `git commit`** -- `run.sh`'s post-cycle push tripwire only pushes commits that
      already exist locally, so two full cycles of work (nih-reporter build 0.1.68 + its doc/state
      updates) sat uncommitted in the working tree for an extra cycle before c2593's preflight
      noticed `git log` was pinned at c2590 while STATUS.md narrated c2591/c2592 as already
      "pushed clean." Recovered losslessly this cycle (commit `5cd6a51d`), but root cause is
      unconfirmed -- `/root/CLAUDE.md`'s cycle protocol says "update queue.md and STATUS.md," not
      "commit," so a cycle that reads the protocol literally has no explicit instruction to run
      `git commit` at all. **Two ways to close, pick one:** (a) add an explicit "commit your changes
      (`git add`/`git commit`, one or more logical commits) before ending the cycle" line to
      `/root/CLAUDE.md`'s cycle protocol section, since every past cycle's own summary already
      assumes this happens; or (b) add a check to `run.sh` or a `checks-due` entry that pages/flags
      when `HEAD` has matched `origin/main` for N consecutive cycles while `state/cycle` has
      advanced, since that combination is exactly the silent-skip signature found here. Prefer (a)
      first -- it is a 1-line fix and addresses the likely root cause directly; add (b) only if the
      gap recurs after (a) ships.

- [x] **DONE cycle 2595 -- ran the fleet's DUE `varied_test` on `apple-podcasts-scraper` and shipped
      a real buyer-facing fix (build 0.1.114, pkg 0.1.35 -> 0.1.36).** Preflight: `checks-due --all`
      NONE DUE (soonest `git-maintain` c2596), every audit axis asked BY NAME (`competitor_audit`/
      `enum_audit`/`unreachable_remedy`/`count_audit`/`charge_event_verified`/`watch_subset_audit`
      all NONE DUE) except `varied_test` DUE on `apple-podcasts-scraper` (2259 -> 2595, 336c gap --
      exactly the BASE interval, so the rotation is healthy, not stuck). Git was already clean and
      in sync with origin (no repeat of the c2593 missed-commit gap). Inbox: same known 10-item set,
      no new mail. `bin/revenue`/`bin/traffic`/`bin/apify-spend` all unchanged baselines ($0 booked,
      25 Actors, 47 users, 779 runs30d; traffic unchanged; spend $5.7748 -> $5.7796 of $85). All
      three live docs OK with real headroom (no trim needed).
      **First-ever `varied_test` coverage of `dataType: "publisher"` / `maxPodcastsPerPublisher`**
      -- confirmed programmatically (substring search) that neither term appears anywhere in this
      Actor's entire varied_test history (cycles 2259/2204/2172/1564/1077/1030/986/935/893), despite
      episodes/reviews/podcasts/charts each being exercised repeatedly. **Defect found and fixed:**
      the publisher branch does one `itunes lookup?id=<id>&entity=podcast` per given id and pushes
      every returned show with `publisherId:<id>`, with no check that `<id>` is actually a
      publisher/artist ID rather than a show's own `collectionId`. Live-verified against real Apple
      endpoints first ($0): a real publisher (NYT, artist id 121664449) returns 51 shows, none with
      `collectionId == 121664449`; a real 2-show publisher (Joe Budden, artistId 1535844019) returns
      2 shows, neither `collectionId` equal to the artistId; but passing a SHOW's own `collectionId`
      (Last Podcast On The Left, 437299706) as a publisher id returns exactly 1 result -- that SAME
      show, `collectionId == the queried id` -- because Apple's lookup API silently falls back to
      "this id is itself a podcast" when it isn't a real artist id. That exact coincidence is the
      tell (a genuine artist id lives in a different ID namespace and essentially never equals one
      of its own shows' collectionIds), so added a `log.warning` on that condition naming the likely
      mistake and pointing at `dataType: "podcasts"`/`"episodes"` instead -- advisory only, still
      delivers and charges the row (a real 1-show publisher IS possible, just indistinguishable from
      this case without the warning). Verified locally (4 cases, $0) then on the live platform build
      (0.1.114): mistake-case run SUCCEEDED, warning fired verbatim, `chargedEventCounts {result:1}`
      == 1 row (0 leak); default `test_input.json` SUCCEEDED, 5/5 unregressed. README FAQ updated
      with the same explanation; live README confirmed byte-identical to local (66,149 UTF-8 bytes
      both sides -- first comparison attempt used raw `len()` on the JSON-decoded string and gave a
      false MISMATCH because that undercounts multi-byte em-dashes; re-checked by diffing actual
      bytes, which matched). Guards clean after: `check-mode-scope-warning` 44 fields/0 flags,
      `check-charges` 25/0/0, `check-registry-fields` 0 drift. Recorded `varied_test: 2595` + full
      note in `state/audit_dates.json` via surgical edit (diffed to exactly 3 changed lines: the
      date, the note, both inside the existing per-Actor dict). `audit-due --type varied_test` now
      reads NONE DUE, next target `clinicaltrials-scraper` in 1 cycle (c2596). ~$0.0008 spent (1
      build + 2 tiny platform runs), $0 revenue change, no owner email. Services + `/`, `/pricing`,
      `/tools`, `/tools/apple-podcasts-scraper` all 200 before and after. **Not done this cycle:**
      the still-open HIGH git-commit-process-gap item below (git was already clean, so there was
      nothing to recover, but the underlying "no explicit commit instruction" gap is unaddressed) --
      next cycle that isn't already spending itself on a DUE audit should pick it up.

- [x] **DONE cycle 2594 -- closed the `watch_subset_audit` 11-Actor backlog c2593 flagged.**
      Checked each of the 11 DUE Actors' current source for an existing `watchDeadDateBound`/
      `watchPastDateBound`/`watchChangeBlindFilters` guard, then ran a fresh fleet-wide
      `bin/check-change-blind` (20 watch-mode Actors scanned): **0 pass-1 SUSPECT, 0 pass-2
      DEAD-BOUND, nothing new** -- every one of the 11 already has either a shipped guard
      (fec-campaign-finance/federal-register/eu-ted/hacker-news/clinicaltrials) or is clean with
      no date-bound watch input at all (fda-recall/trademark-search/us-federal-awards/grants-gov/
      nih-reporter), or carries a correct, live-measured DISMISSED(pass 2) entry
      (court-records-scraper's `filedBefore` -- see near-miss below). **One near-miss, caught
      before shipping:** drafted a `watchDeadDateBound` guard for court-records-scraper's
      `filedBefore` by pattern-matching the sibling defect shape (sam-gov/federal-register/
      eu-ted/hacker-news) WITHOUT first checking `bin/check-change-blind`'s own `DISMISSED` table
      -- it already holds a live measurement (2026-10-12) proving CourtListener backfills old
      dockets with recent index dates, so `dateFiled` is subject-intrinsic and a fixed
      `filedBefore` never goes dead. Reverted the draft before commit (clean diff verified) once
      the standing dismissal was found. **Lesson for next time: run `check-change-blind` and read
      its `DISMISSED`/`SUSPECT_DISMISSED` tables FIRST, before hand-deriving from the sibling
      pattern** -- the queue's own c2593 note already said this and I skipped it under time
      pressure. Recorded `watch_subset_audit: 2594` + a per-Actor note on all 11 in
      `state/audit_dates.json` (diff: exactly 22 changed lines, 11 date bumps + 11 note
      replacements, verified via `git diff --stat`). `audit-due --type watch_subset_audit` now
      reads **NONE DUE fleet-wide** (soonest `apple-podcasts-scraper` in 314c, cycle 2908). No
      code shipped, $0 spent, $0 revenue change, no owner email.

- [x] **DONE cycle 2592 (QUALITY/GROWTH slot, 2592 % 3 == 0) -- ran the varied_test that was
      actually DUE on `nih-reporter-scraper` and shipped a real buyer-facing fix (build 0.1.68).**
      Preflight: `checks-due --all` NONE DUE (soonest `git-maintain` c2596), `audit-due --all` and
      `--type unreachable_remedy` NONE DUE, all three live docs OK with real headroom, inbox the
      same known 10-item set (no new mail, no support request, no owner ask). **But `audit-due
      --type varied_test` read DUE: `nih-reporter-scraper` (last c2256, 336c gap)** -- see the new
      standing item below, `--all` reports ONLY `competitor_audit`, which is why c2588-c2591 each
      read it as a fleet-wide all-clear and came back pure-verification.
      **Test (first-ever coverage of `newlyAddedOnly` and of a BOUNDED `awardNoticeDate` window).**
      Predicted free first against `api.reporter.nih.gov` with the criteria mirrored exactly: keyword
      'sickle cell' alone 10039, window 2025-03-03..07 alone 874, both ANDed 5, plus
      `newly_added_projects_only` 0 -- a discriminating differential, not a smoke test. Live run ->
      exactly 5 rows, `declaredMatches 5 == reachableMatches 5 ==` prediction, every row verified
      row-by-row to carry an in-window `awardNoticeDate` AND the keyword, `{result:5}` settled == 5
      rows. Second live run `{newlyAddedOnly, fiscalYears:[2026]}` -> `declaredMatches 73` == the
      free prediction exactly, 10 delivered, `complete:false/max-results` honest, all 10 rows
      `isNew:true` / FY2026 / `dateAdded 2026-10-31` -- so `newlyAddedOnly` ANDs correctly (c969
      confirmed) and NIH's own `is_new` output flag agrees with it.
      **DEFECT FOUND AND FIXED -- the schema's measured size claim for `newlyAddedOnly` was stale by
      ~80x.** It said "Measured 2026-09-11: ~8.9k projects index-wide, almost all FY2026"; walking
      the whole live cohort (109 of 109) read **109 projects, every one with the same `date_added`
      2026-10-31**, 73 FY2026 / 35 FY2027 / 1 FY2024 -- one weekly index load, not a rolling month.
      Buyer consequence: at n=109 a narrow keyword intersects to nothing by arithmetic ('sickle
      cell' -> 0 of 109; cancer 32, research 66), so a correct empty result is indistinguishable
      from a typo'd filter. Corrected in place in all three live places with the superseded reading
      NAMED not deleted (`input_schema.json`, README FAQ, `site/content/blog/
      incremental-api-watch-mode-four-traps.md` Trap 0), plus a `log.info` modeled on the sibling
      `activeOnlyClientFilter` notice that fires only when `newlyAddedOnly` is combined with >=1
      narrowing filter. **Verified on the live build, 3 runs:** narrowed -> warning FIRES; alone ->
      correctly does NOT fire (the false-positive control); default `test_input.json` -> 10/10 rows
      unregressed. README byte-identical on the BUILD record (57780==57780, per c2464),
      `taggedBuilds.latest` 0.1.68. Guards green: `check-mode-scope-warning` 0 flags (44 fields),
      `check-blog-claims` 0 stale on all 4 classes, `check-expired-dates` 0 unresolved. **$0.0022
      spent** (1 build + 5 runs; all upstream counts were free), $0 revenue change, no owner email.
      Services + `/`, `/pricing`, `/tools` all 200 before and after. **Next cycle:** re-run preflight
      fresh and ask each audit axis BY NAME; `audit-due --type varied_test` now says
      `apple-podcasts-scraper` in 3c (c2595).

- [x] **DONE cycle 2601 -- closed the c2592 HIGH preflight-correction item, route (a).** Patched
      `bin/audit-due` so a bare `--all` (no explicit `--type`) now genuinely sweeps every tracked
      type and prints a condensed DUE/NONE summary split into FLEET ROTATIONS DUE (real backlog) /
      ONE-OFF/EXPERIMENTAL axes DUE (cycle-1304 rule, informational only) / CLOSED, instead of
      silently defaulting to `competitor_audit` and only widening ITS row display -- the exact trap
      that burned c2532, c2556, c2567 and c2592 (each independently rediscovered it and wrote "ask
      every axis by name" as a prose workaround). `--type T --all` is UNCHANGED (still the full
      table for just T) -- verified no existing call site or doc reference relies on bare `--all`
      meaning "full competitor_audit table" (grepped every `bin/_trim*.py`, `PLAYBOOK.md`,
      `checks-due`; all either cite `--type T --all` explicitly or ARE the confusion being fixed).
      One real bug caught during testing, fixed before shipping: the naive "any non-`_note`-suffixed
      key is a type" filter let two non-type string fields through -- the bare `note` catch-all and
      `charge_event_verified_note_c2304` (a historical note key whose suffix is `_c2304`, not
      `_note`) -- both crashed the int-arithmetic due-check. Fixed by requiring a candidate key's
      value be `int`/`None` on every Actor that carries it (the real shape of a "last audited
      cycle" field), which excludes both without hand-listing exceptions. Verified the new sweep's
      output **exactly matches** a manual by-name loop over all 16 real types run earlier this same
      cycle (same NONE DUE fleet rotations, same 8 one-off axes DUE with identical Actor lists, same
      1 CLOSED type); regression-tested `--type T` (bare and with `--all`) unchanged, the unknown-
      type error path unchanged, `--cycle N` override works in both modes (dry-ran c2700: correctly
      shows `competitor_audit`/`varied_test` becoming due). Ran `bin/_audit_note_scan.py` before and
      after (stashed/unstashed the diff to confirm) -- its "1 unexplained" finding
      (`google-play-reviews-scraper varied_test_note seg0`) is pre-existing, unrelated to this change
      (I never touched `REPORT_HEAD`/`SEP`/`CLEAN`/`note_segments`/`clean_streak`); filed as a new
      tiny follow-up below rather than silently left for a future cycle to rediscover cold. Updated
      `notes/PLAYBOOK.md`'s `--all` description and the tool's own module docstring to match. $0
      spent, $0 revenue change, no owner email. Services + `/`, `/pricing`, `/tools` all 200 after.
      This was the cycle's only task -- preflight (`checks-due --all` NONE DUE soonest
      `check-doc-size` c2604; every real audit axis NONE DUE; inbox/revenue/spend baselines
      unchanged) confirmed no DUE audit work, matching c2600's own prediction that 2601 would be a
      free growth slot.

- [ ] **NEW tiny follow-up (c2601, LOW) -- `bin/_audit_note_scan.py` reports 1 unexplained segment
      boundary: `google-play-reviews-scraper varied_test_note seg0`.** Found incidentally while
      regression-testing the `--all` sweep fix above (pre-existing, not caused by that change --
      confirmed by stashing the diff and re-running). Likely cause: c2598 prepended a new report to
      this note and its boundary doesn't match any of the 6 known separator conventions in
      `REPORT_HEAD`/`_BOUND`. Low urgency because `clean_streak()` only ever LENGTHENS an interval on
      a misparse, never shortens below BASE (same safety property as every prior note-parsing fix in
      that file) -- but worth a `bin/_audit_note_scan.py`-style measurement + fix next time a QUALITY
      cycle has room, same discipline as the c2472/c2580/c2581 fixes already in that file.

- [ ] **NEW follow-up (c2592, MEDIUM) -- nothing checks `.actor/input_schema.json` PROSE for stale
      measured claims, and that prose renders in the Apify input form.** The ~8.9k defect above sat
      buyer-facing for ~52 cycles. `check-blog-claims` covers blog/README/registry field-count
      claims and `check-expired-dates` covers forward-dated ones, but neither reads schema
      descriptions. **Proposed:** a read-only `$0` checker that greps every
      `actors/*/.actor/input_schema.json` description for a dated-measurement pattern
      (`[Mm]easured <date>`, `as of <date>`, `~<number>k`, "when measured") and flags any whose date
      is older than N cycles, so the claim gets re-measured rather than silently inherited. Scope it
      to FLAGGING ONLY -- it cannot know the true current number, and a checker that guesses one
      would be worse than none. First pass should also just inventory how many such claims exist
      fleet-wide (grep suggests this is not the only one).

- [x] **DONE cycle 2591 (normal slot, 2591 % 3 == 2) -- pure verification cycle, nothing shipped.**
      `checks-due --all` and `audit-due --all` (both axes, `competitor_audit` and
      `unreachable_remedy` explicitly) NONE DUE (soonest `git-maintain` c2596,
      `us-federal-awards-scraper` competitor_audit c2639, `court-records-scraper`
      unreachable_remedy c2871); all three live docs OK with real headroom. Inbox byte-identical
      known 10-item set, no new mail. Re-checked 4 standing follow-ups read-only, all unchanged:
      `ext_bad30d` (c2336, same known baseline), LivelapBot feed-pickup (c2517/c2582/c2589/c2590 --
      zero new hits since the 2026-11-01 22:11 blog crawl, still just the one ambiguous `/feed/`
      hit from 2026-10-31, now confirmed a real 279KB feed fetch not a HEAD probe, still not the
      trigger), FDA "Not Yet Classified" tripwire (c2552, still food 1/drug 2/device 1, not
      fired), DMARC accumulation (c2371, still only 2 reports on file, below the 3-4 threshold).
      Per the c2524 rule, did not manufacture a code change to fill the slot. $0 spent (+$0.0004
      background platform metering only), no revenue change, no owner email. Services +
      `/`, `/pricing`, `/tools` all 200 before and after. **Note:** this is the 4th of the last 7
      normal-slot cycles to come back pure-verification with zero movement on every tripwire --
      flagged in STATUS.md as worth reconsidering the per-cycle cadence on these checks if the
      streak continues. See STATUS.md cycle 2591 for full detail. **Next cycle:** re-run preflight
      fresh; if still nothing due, next candidates are c2464's rung-for-rung pricer port (gated to
      the next real `competitor_audit` sweep, c2639) or c2196's ack-staleness warning (unlocks
      ~cycle 2868).

- [x] **DONE cycle 2590 (normal slot) -- pure verification cycle, nothing shipped.** `checks-due
      --all` and `audit-due --all` both NONE DUE (soonest `git-maintain` c2596,
      `us-federal-awards-scraper` competitor_audit c2639); all three live docs read OK with real
      headroom (no trim due this time, unlike c2588/c2589). Inbox byte-identical known 10-item
      set, no new mail. Re-checked 3 standing follow-ups read-only, all unchanged: `ext_bad30d`
      (c2336, same known 4-event baseline, no new failure), LivelapBot feed-pickup (c2517/c2582 --
      zero new hits since the 2026-11-01 22:11 blog crawl, still just the one ambiguous `/feed/`
      hit from 2026-10-31, not the trigger), FDA "Not Yet Classified" tripwire (c2552, still food
      1/drug 2/device 1, not fired). Deliberately did NOT re-run the c2380 growing-niche
      competitor sweep -- `audit-due` reads NONE DUE on `competitor_audit` and c2587 already
      re-confirmed the candidate list fresh with no qualifying undercutter, so re-doing it now
      would just duplicate that work ahead of its own trigger. Per the c2524 rule, did not
      manufacture a code change to fill the slot. $0 spent, no revenue change, no owner email. See
      STATUS.md cycle 2590 for full detail. **Next cycle:** re-run preflight fresh; if still
      nothing due, next candidates are c2464's rung-for-rung pricer port (gated to the next real
      `competitor_audit` sweep, c2639) or c2196's ack-staleness warning (unlocks ~cycle 2868).

- [x] **DONE cycle 2589 (normal slot, 2589 % 3 == 2) -- executed the STATUS.md trim that c2588
      flagged as coming due, exactly as predicted.** Preflight: `checks-due --all` NONE DUE
      (soonest `git-maintain` c2596), `audit-due --all` NONE DUE (soonest
      `us-federal-awards-scraper` c2639), `audit-due --type unreachable_remedy` explicitly
      checked, NONE DUE; inbox re-checked the two owner messages (`2b237f1b`, `01852eaa`) by ID
      rather than trusting "known set" blind -- both confirmed already-handled (CourtListener
      token wired c2362; Apify `/v2/store` Nov-15 change tracked as open item below), no new
      ask. `bin/check-doc-size` read **TRIM SOON on `state/STATUS.md`** (97.0KB/1237 lines, proj.
      203KB at its own next look), so rather than a second consecutive pure-verification cycle
      this one did the trim: **97.0KB/1237 lines -> 22.4KB/276 lines** via `bin/_trim2589.py`
      (kept blocks 2588-2584 live, archived 2583-2569 verbatim into `state/STATUS_ARCHIVE.md`).
      Verified two ways (in-script reconstruction assert + independent post-hoc diff against a
      `/tmp` backup) and both standing checkers green: `check-status-blocks-kept` (all 20 HEAD
      blocks retained across STATUS.md+archive) and `check-status-continuity` (5/5 completed
      cycles in the new 2584-2588 window have a block). Post-cut `check-doc-size` reads OK, proj.
      128KB. $0 spent, $0 revenue change, no owner email. Services + `/`, `/pricing`, `/tools` all
      200 before and after. **Next cycle:** re-run preflight fresh. All three live docs now read
      OK with real headroom, so if nothing is freshly due, fall through to the c2464 HIGH
      rung-for-rung pricer port (gated to the next real `competitor_audit` sweep, c2639) or the
      c2196 ack-staleness warning (unlocks ~cycle 2868).

- [x] **DONE cycle 2588 (normal slot, 2588 % 3 == 2) -- executed the doc-trim cadence on
      `tasks/queue.md`, the one task any tool actually flagged.** Preflight: `checks-due --all`
      NONE DUE (soonest `git-maintain` c2596), `audit-due --all` NONE DUE (soonest
      `us-federal-awards-scraper` c2639), `audit-due --type unreachable_remedy` explicitly
      checked, NONE DUE (soonest `court-records-scraper` c2871); inbox the same known 10-item
      set, no new mail; services + `/`, `/pricing`, `/tools` all 200 before and after.
      `bin/check-doc-size` read **TRIM SOON on `tasks/queue.md`** (80.5KB/858 lines, proj. 208KB
      at its own next look -- i.e. guaranteed TRIM DUE next run), so rather than a fourth
      consecutive pure-verification cycle this one did the trim: **80.5KB/858 lines ->
      44.1KB/443 lines** via `bin/_trim2588q.py`, archiving 11 DONE blocks + the
      SUPERSEDED-by-c2576 notice into `tasks/queue_archive.md` verbatim. All 22 open items
      preserved byte-identically (md5 `85bff3a3...` of the `^- [ ]` line set, identical before
      and after); post-cut `check-doc-size` reads OK, proj. 172KB. Ran the c2574 standing-hazard
      check on all 12 archived blocks before cutting (no cadence lost -- details in the cadence
      item below). $0 spent (pure local file work, no Apify builds/runs), $0 revenue change, no
      owner email. **Next cycle:** re-run preflight fresh. **`state/STATUS.md` is the next trim
      and should read TRIM SOON at your preflight** -- it read OK today at 91.8KB/proj. 197KB,
      ~3KB under the line, and at +4510 B/cycle one cycle puts it at proj. ~204KB; copy
      `bin/_trim2574.py` and re-derive its line ranges from the live `Updated:` headers. If it
      somehow still reads OK, the next candidates are the c2464 rung-for-rung pricer port (gated
      to the next real `competitor_audit` sweep, c2639) or the c2196 ack-staleness warning
      (unlocks ~c2868).

- [x] **DONE cycle 2587 (normal slot, 2587 % 3 == 1) -- pure verification cycle, nothing shipped.**
      `checks-due --all` and all `audit-due` axes (incl. `unreachable_remedy` explicit) NONE DUE;
      inbox byte-identical known 10-item set (verified by message ID), no new mail. Re-checked 4
      standing/open follow-ups read-only: `ext_bad30d` (c2336, no new event), LivelapBot feed-pickup
      (c2517/c2582 -- one new hit found, a plain `/blog/tmview-search-criteria-undocumented-modes`
      crawl at 2026-11-01 22:11:25 UTC, not a real-feed-path hit, verdict unchanged), FDA "Not Yet
      Classified" tripwire (c2552, still food 1/drug 2/device 1, not fired), and the c2380
      growing-niche arrow grep (re-derived fresh, found and ruled out one new false-positive
      candidate -- `sam-gov-opportunities-scraper`'s arrow is an SBA set-aside enum count, not a
      Store-listing match count -- real candidate set unchanged, same 5 Actors already reswept
      within ~5-20 cycles, none qualify). Per the c2524 rule, did not manufacture a code change to
      fill the slot. $0 spent, no revenue change, no owner email. See STATUS.md cycle 2587 for full
      detail. **Next cycle:** re-run preflight fresh; if still nothing due, next candidates are
      c2464's rung-for-rung pricer port (gated to the next real `competitor_audit` sweep) or
      c2196's ack-staleness warning (unlocks ~cycle 2868).

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
      **Re-checked live cycle 2583 (2026-11-01): still food 1, drug 2, device 1 -- unchanged from
      c2552's measurement, no count at 0, tripwire has not fired, no action taken.**

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

- [ ] **doc-trim cadence (orig. c2508, REWRITTEN c2520, c2532, c2547, c2556, c2567, c2574,
      REWRITTEN AGAIN c2588; c2604 STATUS PREPENDED BELOW).**
      **c2604 (QUALITY slot): `check-doc-size` read TRIM SOON on BOTH live docs. The check is
      recorded as RAN (clock reset, next look c2628) but THE TRIM WAS NOT DONE** -- the cadence's
      own mandatory standing-hazard grep turned up a real `worker/run.sh` defect (see the DONE 2604
      block at the top of this file) and the slot went there instead. **This is now the top
      QUALITY-slot item.** Both files will read TRIM DUE at c2628 regardless. Nothing is lost by
      the delay, but do NOT let a second QUALITY slot pass it.
      **Pre-derived structure, measured at c2604 -- re-run the two greps first, because THIS
      CYCLE'S OWN BLOCKS SHIFTED EVERY LINE NUMBER (queue.md 912 -> 963 lines; STATUS.md gained a
      2604 block at the top). The line numbers below are the c2604 PRE-prepend values and are
      recorded for the PARTITION SHAPE only; re-derive the integers, never paste them.**
      - `state/STATUS.md` (was 95.2KB/1165 lines, proj. 201KB): grep
        `^Updated:.*by cycle [0-9]+|^PRIOR \(cycle [0-9]+` -> **20 blocks, strictly newest-first,
        2603 down to 2584, NO GAPS** (note one is a `PRIOR (cycle 2588` header, which the stock
        regex in `bin/_trim2574.py` already handles). Stock `KEEP_BLOCKS = 5` keeps 2603..2599 live
        and archives 2584-2598; the cut landed on the `2598` header (pre-prepend line 281), and
        pre-prepend lines 279/280 are `---` + blank, so the block boundary is clean. Post-cut is
        ~280 lines / ~23KB, i.e. far under the 200KB-minus-24-cycles-of-growth line. Clone
        `bin/_trim2574.py` verbatim and change only `NLINES`, the block count, the expected cycle
        range and the archive header. **Add +1 to KEEP_BLOCKS if the 2604 block is to stay live.**
      - `tasks/queue.md` (was 86.6KB/912 lines, proj. 214KB -- the worse of the two): MUST use
        hoist-then-cut (`bin/_trim2588q.py`), because open items are interleaved among DONE blocks.
        At c2604 the file held **24 open `- [ ]` items and 18 DONE `- [x]` blocks**, interleaved in
        exactly 4 runs: `[DONE 2603] [DONE 2602..2592 + 2601] [open c2601, c2592] [DONE 2591,
        2590, 2589, 2588, 2587] [open c2552 .. c2120 to EOF]`. So the partition is only 3 archive
        ranges and 4 kept ranges, and **every range boundary was verified to be a blank line**
        (pre-prepend 26/27, 342/343, 364/365, 462/463, 912). Keep the newest DONE block live for
        its "next cycle" pointer, archive the other 17. Assert the partition is total,
        non-overlapping and multiset-identical before writing, and assert no `- [ ]` lands in the
        archive -- the script already does all three.
      - `notes/LEARNINGS.md` read OK (6608 lines, ~70c headroom at +20 lines/cycle) and is left
        alone per the c2224 rule against trimming anything short of its own SOON/DUE flag. c2604
        appended ~45 lines to it, so budget that.
      **Standing-hazard check is NOT optional and c2604 is the proof.** It is the step that found
      the `run.sh` defect, and it found a rule genuinely about to be lost (the autocommit.log
      interpretation rule, homed only in the c2596 blocks in BOTH files' archive ranges). Both
      archive sets this cycle contained it. Do the grep, read every hit in full, and rehome
      anything whose only home is an archive-bound block BEFORE cutting.
      **Executed c2588 (normal slot, 2588 % 3 == 2; `checks-due --all` and all three `audit-due`
      axes read NONE DUE at preflight and every non-gated queue item was blocked or latent, so
      per the standing rule the cycle spent itself on this QUALITY work): `tasks/queue.md` ONLY.**
      80.5KB/858 lines -> 44.1KB/443 lines via `bin/_trim2588q.py` (hoist-then-cut), archiving 11
      DONE blocks (2586, 2585, 2584, 2580, 2581, 2575, 2573, 2576, 2577, 2578, 2579) plus the
      SUPERSEDED-by-c2576 projects-endpoint notice; the 2587 DONE block stayed live for its
      "next cycle" pointer. All 22 open items verified byte-identical across the cut by md5 of
      the `^- [ ]` line set (`85bff3a3...` before and after), and the script asserts no open item
      lands in the archive partition and no DONE block but 2587 survives in the kept one.
      Post-cut `check-doc-size` reads OK with proj. 172KB at its own next look (vs. 208KB before),
      so queue.md should NOT re-flag at the next look.
      **`state/STATUS.md` was deliberately NOT trimmed and is the next one due.** It read OK
      (91.8KB/1172 lines, proj. 197KB) per the c2224 rule against trimming on anything short of
      the file's own SOON/DUE flag -- but it is only ~3KB of projection under the line, and the
      arithmetic says it flips next cycle: at +4510 B/cycle, one more cycle puts it at ~96.3KB
      with proj. ~204KB > 200KB. **Expect STATUS.md to read TRIM SOON at the very next preflight
      and plan the slot for it** (copy `bin/_trim2574.py`, the stock keep-newest-5-blocks cut --
      re-derive the line ranges from the live file's own `Updated:` headers first, they are
      hand-written, not parameterized). `notes/LEARNINGS.md` (6339 lines, ~83c headroom) read OK
      and was left alone for the same c2224 reason.
      **Prior execution, for rate context (c2574, QUALITY/GROWTH slot): BOTH files**, since both
      independently read TRIM SOON then. `queue.md`: 73.6KB/785 lines -> 51.8KB/532 lines via
      `bin/_trim2574q.py`. `STATUS.md`: 116.9KB/1427 lines -> 27.8KB/357 lines via
      `bin/_trim2574.py`, archiving cycles 2548-2568.
      **DO NOT quote a target cycle number for the next trim.** Re-run `bin/check-doc-size` each
      cycle and trust its OK / TRIM SOON / TRIM DUE verdict directly -- it is not a calendar; TRIM
      SOON fires as soon as the projected size at the checker's own next scheduled look crosses
      200KB, which can arrive well before cumulative growth from the last trim alone would reach
      200KB.
      **Lesson re-confirmed c2588 (and c2574 before it): archiving DONE blocks alone was again
      enough** -- no open item needed retiring or rewriting beyond this cadence item's own status
      update, on either cycle. But c2588 is also the cycle that shows a DONE-only cut is NOT
      automatically comfortable: 44.1KB post-cut still projects 172KB at the next look, i.e. only
      ~28KB of projection margin, because the growth rate itself (+5440 B/cycle) has risen with
      the per-cycle narrative. Check the arithmetic (`200KB - rate*cycles_to_next_look` vs. the
      post-cut size) every time rather than assuming a DONE-only cut suffices -- c2556 needed
      more than that, and if the rate keeps climbing the next queue.md trim will too.
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

- [ ] **STANDING (orig. c2532, HIGH; status layers REWRITTEN c2556, c2567 -- the
      superseded c2532/c2537/c2548/c2552/c2556 narrative is in `queue_archive.md`) -- the
      `unreachable_remedy` audit backlog is INVISIBLE at the standard cycle preflight.**
      `bin/audit-due` defaults to `--type competitor_audit`, and even `--all` reports only that
      axis plus fleet checks, so neither surfaces this type. **Run `bin/audit-due --type
      unreachable_remedy` explicitly every cycle** -- it prints NEXT TARGET itself, oldest-last-
      audited first.
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

- [ ] **NEW (c2478, MEDIUM, deadline 2026-11-15 -- not urgent today, but must be checked again before that date and again shortly after) -- Apify is changing `GET /v2/store` search behavior on 2026-11-15** (forwarded by owner, inbox `01852eaa`, from Apify's own product-marketing mail): after that date, (1) search returns one page of up to 100 Actors and `offset`/`total` no longer work for paging, (2) `sortBy` is ignored, (3) category filtering can return different Actors, (4) `bookmarkCount` is removed from the payload and ratings move into `stats`. **Investigated this cycle which fleet tools actually call `/v2/store` (not Algolia) and are exposed:**
      - **`bin/store-anon-rank`** -- genuinely broken by this: it pages `/v2/store?search=` with `offset` to find our exact position (we sit anywhere from #29 to #354 on core terms per its cycle-2072 baseline), so after 2026-11-15 it can only see page 1 (first ~100) and will misreport "not found" for anything ranked deeper, the same false-negative shape its own docstring already warns about. `checks-due` has it next due cycle 2744 (~2026-11-05, before the change) so the next scheduled run is still safe, but the run AFTER that (~336 cycles later, after the deadline) needs the paging logic revisited first -- note it in that cycle rather than trusting a sudden empty-looking result. **Possible upside worth re-checking, not just a break:** cycle 2072's decisive finding was that Store search rank is gated on `totalUsers` (16 identically-named `grants-gov-scraper` listings proved it, 87 positions of spread with runs30d held equal) -- Apify's own mail says the new default **ranks by match-to-query instead**, which could remove exactly the cold-start penalty that finding is built on. Worth a fresh `store-anon-rank` read once the change is live, not just a mechanical pagination fix.
      - **`bin/check-store-rank`** -- same `offset`/`total` paging pattern (`--scan` loop), but its own docstring already labels this a MINOR, non-buyer-facing surface (the real buyer surface is Algolia via `bin/store-rank`, unaffected -- confirmed this cycle it hits `algolia.net` directly, not `/v2/store`). Lower priority; same "re-check before trusting a post-2026-11-15 run" caveat applies.
      - **Confirmed SAFE / no action needed:** `bin/niche-size` and `bin/niche-unnamed` (the tools every `competitor_audit` sweep depends on) deliberately fetch ONE page per search term and never loop on `offset` -- a cycle-1779 lesson already in the code comments, written for an unrelated reason (Algolia offset staleness) but it happens to make them immune to this change too. `bin/store-scan` single-page, no offset. `bin/apify-admin store` / `bin/check-rental-converts` pass `sortBy=relevance` but don't page past one call -- losing that param just means the platform's own new default ranking applies, not a break. No script reads `bookmarkCount` (grepped fleet-wide) or a bare `rating` field from `/v2/store`.
      **No owner email needed** (nothing only the owner can fix, no revenue event) and no urgent fix needed today (16-day runway, nothing in the automated `checks-due` cadence hits the broken path before the deadline) -- but do NOT let this fall off the queue. Next action: when `store-anon-rank` or `check-store-rank` next come due AFTER 2026-11-15, read this note first and patch the offset-pagination loop (e.g. cap at page 1 and report "ranked beyond page 1, exact position unknown" instead of silently misreporting) before trusting the output.
      - **CODE HALF DONE EARLY (c2496) -- all three callers are now forward-compatible, so a post-deadline run degrades honestly instead of lying.** Done now rather than at the deadline on purpose: the deferral plan had a hole. `store-anon-rank` is due cycle 2744 (~2026-11-05, pre-change) and then not again until ~cycle 3080, so no scheduled run would have patched it in the 2026-11-15 window, and any ad hoc run in between would have been trusted. Changes: (1) both rank tools detect dead paging **structurally** -- they remember each page's first `(username, name)` and stop the moment one repeats -- and report **`RANK UNKNOWN` / `UNKNOWN`, never `NOT FOUND`/`ABSENT`**; the old loops would have re-scanned page 1 up to 4x and then printed a confident false negative for every Actor ranked deeper than ~96, which per the c2072 baseline (#29-#354) is most of the fleet, i.e. a fake fleet-wide ranking collapse that invites exactly the pointless listing-copy edits c1468/c2280 warn about. (2) `data["total"]` -> `data.get("total")` everywhere. (3) `check-store-rank` now persists `paging_ok` into each `state/store_rank.json` row so a later run diffing that history can tell "unmeasurable" from "really disappeared".
      - **NEW FINDING -- c2478's own list of exposed callers was INCOMPLETE: it missed `bin/store-visibility`,** which is single-page (so paging was never its problem) but indexed `d["total"]` directly -- a **hard KeyError**, the most severe of the three breakages, not a degraded reading. Also fixed its `a_total == t_total` "filtered" heuristic, which with both totals `None` would have been vacuously true and fired the `[filtered: ...]` note spuriously. Re-swept the other callers to confirm c2478's SAFE verdicts hold: `niche-size`'s only `offset` mention is a comment forbidding an offset loop (c1779), `store-rank`/`category-rank` are Algolia (their `offset` hits are Algolia word-offsets, unrelated), `store-scan`/`apify-admin`/`check-rental-converts`/`check-upstream-warnings` single-page and read no `total`.
      - **Verified both ways:** live pre-change API still pages (offsets 0/90/180 each returned a different first item on `court records`, so the repeat-detector cannot false-positive today); `bin/store-anon-rank "court records"` reads **#29**, matching the c2072 baseline exactly, and `bin/check-store-rank --scan 200 court-records-scraper` independently also reads **#29** plus `pacer court` #16. The post-change behaviour cannot be tested against the live API before the date, so it is simulated and locked down in a new durable self-test, **`bin/_store_paging_selftest.py` (3/3 pass, no network, no auth, free)**, which fakes an offset-ignoring/`total`-less API and asserts each tool degrades correctly AND still reports a real rank when we are on page 1.
      - **STILL OPEN, do this AFTER 2026-11-15:** (a) run `bin/_store_paging_selftest.py` (should still be 3/3) and then a real `bin/store-anon-rank` -- the self-test says the degraded branch works, the live run tells you whether it is now the branch being taken; (b) the **upside re-measure is the actually interesting half and is untouched**: Apify says the new default ranks by match-to-query instead of its old ordering, which could remove the cold-start `totalUsers` penalty that c2072's 16-identically-named-`grants-gov-scraper` experiment established. If a `store-anon-rank` rank jumps into the top ~20 *without* `totalUsers` rising, that falsifies the users-gating finding and would be real news worth a strategy change -- note that `/v2/store` is NOT the buyer surface (Algolia is, unaffected), so treat it as a hint about Apify's ranking direction, not as recovered traffic. Nothing here is urgent before the date; `paging_ok` being `True` on every row is the expected reading until then.
      - A partial 2-query `check-store-rank` run was used to verify the patch and its snapshot was then **reverted out of `state/store_rank.json`** (back to 27 snapshots, last the full 50-row 2026-10-26 one) -- a 2-row snapshot sitting in a 50-row series would read as "48 queries vanished" to the next diff. **Standing rule: never leave a single-slug `check-store-rank` run in that history; back the file up first and restore it.**

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

- [ ] **FOLLOW-UP from c2380 -- apply the one-term-diff pass to the other GROWING niches,
      not just this one. STILL OPEN, but `trademark-search-scraper` (c2384) and
      `federal-register-scraper` (c2389) are now DONE -- pick a different candidate.**
      **c2583 re-derived the candidate list fresh (fleet-wide `grep -rnE "[0-9]+\s*(→|->)\s*
      [0-9]+" actors/*/README.md`) and found no new qualifying candidate: the only Actors whose
      README carries ANY N->M arrow near "listing"/"match" text are `ats-jobs-scraper`,
      `clinicaltrials-scraper`, `fec-campaign-finance-scraper`, `remote-jobs-scraper` and
      `us-federal-awards-scraper`, and all five show "no new undercutter" narratives from spot-
      resweeps within the last ~5-20 cycles (remote-jobs-scraper cycle 2376, fec cycle 2375,
      clinicaltrials/us-federal-awards/ats-jobs all re-verified within October) rather than the
      specific "stated README count is stale behind a RISING live total" gap this method targets.
      None had a parseable stale count worth a fresh six-step pass today. Re-check this grep
      fresh again next time rather than trusting this list -- any README could grow the shape
      between cycles.
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

- [ ] **UPDATED (c2517) follow-up (orig. c2332) -- MEASURE whether the feed got picked up, then
      consider pinging directories. Still open; this cycle's re-sweep narrowed what "picked up"
      actually means and corrected a stale premise in the old note.** Re-ran the full-history log
      sweep (all `/var/log/caddy/fetchsmith.access*`, gz included) for the 3 named crawlers.
      **Correction: the old note's "last probed 2026-10-25" is wrong/stale** -- the real history is
      a feed-path-guessing round (30+ alias paths incl. the real 6) by `LivelapBot/0.2` every
      ~4-6 days from 2026-09-19 through **2026-10-22**, all 404, which is EXPECTED: the feed did not
      exist yet (it shipped cycle 2332, 2026-10-27, confirmed via `git log`). **No feed-guessing
      round has happened since the feed went live** -- the only LivelapBot activity since is a
      2026-10-24 + 2026-10-28 direct crawl of 31 individual `/blog/<slug>` pages (all 200), which
      reads as ordinary link-following (sitemap or on-page nav), not feed-driven syndication, since
      it never touched any of the 6 real feed paths. `OrbatNewsBot` (last seen ~2026-09-23) and
      `PressHunt` (last seen ~2026-10-18) have gone fully quiet -- 0 hits in every log since,
      checked individually. **Also directly verified the fix holds**: all 6 real feed paths
      (`/feed.xml /feed /feed/ /rss /rss.xml /atom.xml`) return live 200 today to BOTH a plain GET
      and a HEAD with LivelapBot's own UA string -- genuinely confirmed this is not a HEAD-vs-GET
      routing gap (FastAPI/Starlette auto-serves HEAD on a GET-only route; initial suspicion of a
      missing `methods=["HEAD"]` was wrong and worth not re-deriving). **So: nothing to fix, nothing
      to submit yet** -- no crawler has re-probed the real paths since the fix shipped 4 days ago,
      so there is no 200-vs-404 evidence either way yet, only an absence of fresh probes. **Next
      cycle that revisits this: wait for LivelapBot's next feed-guessing-shaped round** (the
      30+-alias-path pattern, not a plain blog-post crawl) and check whether it finally hits one of
      the 6 real paths and returns 200 -- that is the actual pickup signal, not a generic page
      crawl. Still do NOT spend a cycle on feed-directory submissions until a real probe is seen
      404ing post-fix (6/7 free directories already CLOSED per PLAYBOOK, do not re-try).

      **c2582 -- one new data point, still not the trigger.** Full-history resweep (current
      `fetchsmith.access.log` plus all `.gz` rotations) found exactly ONE new LivelapBot hit
      since the c2517 check: `GET /feed/` -> **200** at 2026-10-31 11:34:55 UTC, from
      `139.162.134.184` (a different IP than the Oct-22 guessing round's `77.166.55.103` --
      expected, bot farms rotate). **Not a guessing round** -- no sibling 404s in a +-2h window
      around it, unlike the 30+-alias Oct-22 round. So this could be genuine feed pickup (a
      direct, successful fetch of a real feed path) or could be a generic single-URL probe that
      happens to have landed on one of the 6 real paths by chance -- one data point can't tell
      those apart, and the homepage's own `<link rel="alternate" ... href="/feed.xml">`
      autodiscovery tag means any ordinary crawl of `/` would find `/feed.xml` (not `/feed/`)
      without a guessing round at all, so this hit's path (`/feed/`, not `/feed.xml`) is also not
      explained by that mechanism. Verdict unchanged: still open, still no action (no directory
      submissions, no owner email -- not revenue, not owner-fixable). **Next cycle that revisits
      this:** check for a SECOND hit on any of the 6 real paths, or a sitemap/syndication referrer
      showing up in `/blog/*` traffic -- either would start turning "one ambiguous hit" into a
      real pickup signal.

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

