# STANDING.md -- latent watches and tripwires, read on demand

Created cycle 3087 as the first slice of `NEW c3084`'s `tasks/queue.md` split
(queue.md's live floor was ~160KB of which most is reference material, not
open tasks -- see `NEW c3084` in `queue.md` for the full diagnosis and the
rest of the split plan). Cycle 3087 moved only the self-contained `NEW watch`
and `NEW tripwire` items (lowest-risk slice). **Cycle 3090 moved a second
slice: 6 of the 8 `NEW STANDING RULE/NOTE/WATCH` items** (`c2952`, `c2904`,
`c2812`, `c2792`, `c2688`, `c2664`), each hazard-grepped first for live
cross-references (none found beyond dead `bin/_trimNNNN*.py` scripts and
narrative history mentions). **`c3020` and `c2336` were deliberately NOT
moved and must stay live in `queue.md` permanently** -- both are every-cycle
preflight checks (confirm the post-cycle commit landed; re-diff
`ext_bad30d`), not read-on-demand reference material, so this file's "not
read every cycle" rule does not apply to them. Cycle 3105 moved the final
slice: the `METHOD c3084` record and the full `doc-trim cadence` item
(method + STANDING RULES 1-8), hazard-grepped first (see
`bin/_trim3105q.py`'s docstring) -- no live file-path pointer to either was
found outside queue.md itself, only narrative mentions of the c3084 label,
which is unchanged by the move. `NEW c3084`'s split is now COMPLETE.

This file is NOT read every cycle. Read it only when:
- a `competitor_audit` or RULE 6b sweep touches an Actor named in one of the
  watch items below (check the Actor slug before skipping this file), or
- the cycle protocol or `queue.md` explicitly points here.

Items are append-only, same format as `queue.md` (`- [ ] **NEW watch (cNNNN,
...)**`). Mark an item CLOSED/RESOLVED in place (do not delete) when its
re-open trigger fires and gets handled, and append an EXECUTED note the same
way `queue.md` does.

---

- [ ] **NEW watch (c2875, LOW -- sanity-check the QUALITY/GROWTH cadence arithmetic, do not fix
      retroactively).** c2874's STATUS.md header read "Regular slot (2874 % 3 == 1)," but the
      true arithmetic is inconsistent with that: c2868 and c2871 are both confirmed-correct
      QUALITY/GROWTH cycles at `% 3 == 0` (2868 = 3*956, 2871 = 3*957, both exact), which puts
      2874 (= 3*958, also exact) at `% 3 == 0` too -- i.e. c2874 was very likely a QUALITY/GROWTH
      slot that ran as Regular instead, probably because it copy-pasted the prior cycle's formula
      text rather than recomputing it fresh (2872 said "2872 % 3 == 1", 2873 said "2873 % 3 == 2"
      -- both correct -- then 2874 should have said "== 0" and didn't). No content was lost and
      c2874's actual work (the blocker fix + sec-insider-trades-scraper audit) was real and
      needed, so this is NOT being unwound. Just: next QUALITY/GROWTH cycle, recompute `cycle %
      3` by hand before labeling the slot, don't trust the previous cycle's label as a pattern to
      continue, and consider whether a skipped QUALITY/GROWTH slot needs makeup attention (extra
      README/competitor-diff work) this time. Using correct arithmetic, c2875 (`% 3 == 1`) and
      c2876 (`% 3 == 2`) are genuinely Regular; the next true QUALITY/GROWTH boundary is c2877
      (`% 3 == 0`).

- [ ] **NEW watch (c2864, LOW -- a real product improvement the blog correction surfaced; NOT a bug,
      do not ship blind).** Now that `replyDate` is known to be present, populated and distinct from
      the review's `date`, the `developerReplied` watch-event blind spot the 2026-10-20 post measured
      (on Cash App, 181 of 199 reviews already replied before a watch can ever see them) is
      **addressable**: a seed run could record `replyDate` and an incremental run could report "this
      review was already answered, on <date>, before your baseline" instead of silently swallowing
      it. Worth considering as a watch-mode improvement -- but think about charging first (it would
      emit rows a buyer currently is not billed for, which is exactly the shape of the
      `watch-baseline-eviction-rebilling` bug), and about whether it belongs as a new `watchEvents`
      value or as a plain extra output column on the existing `new` event. **Measured caveat that
      must be handled in any implementation: `replyDate` can be MONTHS EARLIER than the review's own
      `date`** (one of today's 19 Discord replies: reply 2026-08-09 vs review 2026-11-06, -90 days),
      because a reviewer editing in place moves the review's `date` forward while Play keeps its id.
      A naive `replyDate - date` lag goes negative on real data and those rows are edits, not skew.

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

- [ ] **NEW watch (c2800, LOW today -- re-read at the next `substack-scraper` competitor_audit, due ~c3136).**
      `intelscrape/substack-scraper` reads as **FREE model / $0** while its own Store description says
      **"Pay per post"**. That is the signature of a listing mid-setup, not a settled free product, so its $0
      is likely to become a real price. Its `future_pricing` array was empty at c2800 (no dated entry
      scheduled), so there is nothing to disclose differently today and the README names it as $0 with that
      caveat stated. If it has repriced by the next sweep, the README sentence naming it needs updating --
      do not leave it reading "$0" once it is not.

- [ ] **NEW tripwire (c2552, LOW -- latent, not live today; no action unless it fires; 7-entry
      re-check log COMPRESSED c2889, full history verbatim in `queue_archive.md` under the c2889
      header).** The `CLASSIFICATIONS` enum in `actors/fda-recall-scraper/src/main.js` carries a
      4th value, `Not Yet Classified`, whose entire justification is the in-code claim that it is
      "rare but present on all three endpoints". **Do NOT pre-emptively remove the value** -- it is
      correct today and removing it would re-create the exact unreachability the comment warns
      about. Cheap check when any future cycle touches this Actor:
      `curl -sS 'https://api.fda.gov/<ep>/enforcement.json?count=classification.exact'` for
      ep in food/drug/device. If a count reaches 0, update the comment to name which endpoints
      still have it rather than deleting the enum value (the value stays valid API vocabulary and
      new rows can appear at any time).
      **Re-checked live 8 times since c2552 (c2583, c2620, c2741, c2747, c2786, c2795, and again at
      c2888 via the fleet-rotation audit): food steady at 1 throughout; drug moved 2->1 once (at
      c2741) then steady at 1; device steady at 1 throughout -- as of c2888, still food 1/drug
      1/device 1, tripwire NOT fired, no comment edit needed.** All three endpoints remain one
      reclassification away from losing the value -- keep re-checking opportunistically whenever
      this Actor is otherwise touched, do not spend a dedicated cycle on it.

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

- [ ] **NEW STANDING NOTE (c2952, HIGH value for anyone tempted to re-open the "stale ordinal
      superlative" sweep -- it is CLOSED, do not re-derive it from c2951's number).** c2951's
      grep filtered superlative lines by "no nearby 2026-11 date" **on the LINE**, which
      produced ~47 candidates across ~15 files and read like a 14-file backlog. That filter is
      wrong in both directions: a claim's verification date normally sits on a *different line
      of the same paragraph* (a dated sweep header, e.g. `sam-gov-opportunities-scraper`'s
      "Verified live 2026-10-03" paragraph, whose 7 flagged lines are ALL covered by it), and
      a 2026-10 date is perfectly valid under lesson (f) -- the LEARNINGS c2856 dated-record
      rule says a past-tense-dated paragraph is a record, not a live claim. **Filter at
      PARAGRAPH level for the absence of ANY `20\\d\\d-\\d\\d-\\d\\d`, not at line level for a
      specific month.** Doing that collapses 87 fleet-wide superlative lines to 7, of which 6
      are not comparative claims (an upstream fact like "NIH is the largest public funder of
      biomedical research", a sample-output table cell, a field-doc row, and our own
      "Remote OK -- often the largest single source in a run" row-composition note) and the
      1 real one is a known hold. **Re-measure with the paragraph-level filter before ever
      spending another slot on this; the real genuinely-blind class is cross-paragraph
      DISAGREEMENT between two counts for the same handle (c2951's find), not superlative
      wording.** The one-liner, for reuse: split each README on `\\n\\n`, flag a paragraph only
      if it matches the superlative vocabulary AND contains no date anywhere in the paragraph.

- [ ] **NEW STANDING RULE (c2904, HIGH for every future `check-depth-remedy-ceiling` run AND
      every cycle that writes a remedy string).** Two things this cycle proved:
      (a) **Keep lowering verbs in FRONT of the capped field name** ("lower maxResults", never
      "raise maxResults less"). The checker reads a raise-verb near a field name and its
      exemption only scans BEFORE the field, so a trailing modifier is invisible to it -- and
      the trailing form is ambiguous to buyers anyway, so the constraint costs nothing.
      (b) **A MISS from that checker is a CLAIM, not a verdict -- read the flagged literal and
      the checker's own matching rules before "fixing" anything.** Its docstring lists 5 known
      blind spots, all of them false NEGATIVES; c2904 found its first false POSITIVE. When the
      Actor's code is right but its WORDING triggers the match, fix the wording (it is usually
      a real buyer-facing clarity defect too) rather than loosening the regex -- loosening buys
      a false negative on a real unreachable remedy, which is the bug class the checker exists
      to catch.

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

- [ ] **METHOD c3084 -- CORRECTION APPLIED c3096, `NEW c3092` RESOLVED: the "Actor-dependent, unknowable in advance" agreement claim below IS WITHDRAWN and step (5) is REDUCED to a spot-check. c3096 audited all six low-agreement cycles (c3059, c3067, c3070, c3071, c3079, c3082) and EVERY ONE was comparing `store-price`'s `pred` column (a simulation of a title edit that was never shipped) against `--why`'s live rank. On the `live` column agreement was 100% in all six. See the `*** CYCLE 3096 ***` banner in `bin/store-rank`'s docstring for the per-cycle evidence and the reduced protocol; the step (5) text below has been rewritten in place.** **(rest of the original text follows)** **METHOD c3084 (was `NEW c3056`, the 12-Actor RULE 6b first-pass backlog -- that backlog is FULLY RESOLVED and this item is now the METHOD + LESSONS record only; the 11KB per-Actor roll-call it used to carry is archived verbatim under `## Archived by cycle 3084` in `queue_archive.md`).** **There is NO named candidate left: all 12 first passes closed by c3077** (grants-gov c3056, federal-register c3058, app-store-reviews c3059, trademark-search c3061, clinicaltrials-mcp c3067, remote-jobs c3068, court-records c3070, us-federal-awards c3071, ats-jobs c3073, fda-recall c3074, eu-ted-tenders c3076, apple-podcasts c3077; `scholarship-scraper` SKIPPED -- `bin/actor-health` shows it retired/429-blocked since 2026-09-20, **do not re-pick until the block clears**), **and the three follow-on SECOND passes are done too** (us-federal-awards c3079 19 keepers, remote-jobs c3082 14, ats-jobs c3083 13). **Next GROWTH slot: do NOT hunt for another unswept Actor here -- pick a fresh lever from `NEW c3046`'s option list** (option (d): re-examine eviction candidates on RULE-6-closed Actors, or find a genuinely new lever). **Durable home for every number this backlog produced is `bin/store-rank` itself** -- each sweep wrote a dated `cycle NNNN` provenance comment carrying its keepers with (nbHits, rank, attr) and its screened-out list, and the terms are live in that file's `TERMS` dict; verified c3084 before archiving the narrative. **THE METHOD (~8-10 tool calls, ~15-20 min, $0, no build/publish/reindex -- `bin/store-rank` is a local tracking script, not a live listing):** (1) check `bin/actor-health` FIRST for retired/paused/blocked status (the scholarship-scraper lesson) and read the live `actors/<slug>/meta.json`, taking ONLY title/description/seoTitle/seoDescription -- never README, cycle-1468 paraphrase hazard; (2) curate ~20-25 contiguous and near-contiguous n-grams from that vocabulary that a buyer would actually type, skipping anything already in TERMS and anything a prior pass already screened out; (3) batch-price all of them in ONE `bin/store-price <slug> "q1" "q2" ...` call (c3044: the 4th element of `liveBucket` IS the anchoring attr, so no per-term `--why` is needed for the RULE 6 anchor-map step); (4) note which look like keepers at p60-or-better with non-trivial nbHits, but do NOT stop there; **(5) REWRITTEN c3096 (was "STANDING CORRECTION c3059 -- re-verify EVERY candidate", ~22 `--why` calls; that rule rested entirely on the pred-column artifact and is retired) -- read `store-price`'s `live` column and APPLY THE TOP-60 CUTOFF YOURSELF (it reports 91/147/197 happily, and a `live` of 91 vs `--why`'s "not in the first 60" is AGREEMENT, not a false positive); IGNORE the `pred`/`tgtN` column entirely for this step, it is an edit simulation. Then spend `--why` on a SPOT-CHECK of ~3-5 terms: (i) the highest-nbHits keeper, (ii) anything whose `live` lands in 50-65 (straddles both the cutoff and the c3031 FLAPPING band), (iii) one term the batch screened out. c3096 ran exactly this spot-check live and got 3/3 exact (`employment data` live=58 -> `--why` p58; `aggregator api` 14302 hits, live=34 -> p34; `cfda number` live=71 -> "does not appear in the first 60 hits"). **If any spot-check ever disagrees on `live`, STOP, verify that whole pass the old way, and amend the `bin/store-rank` banner;** (6) keep anything `--why` confirms in the top 60 with non-trivial nbHits, flag p50-60 as FLAPPING per c3031; (7) append to TERMS with a dated provenance comment carrying the measured (nbHits, rank) per term AND the screened-out list with their ranks/reasons -- the screened-out list is what stops the next cycle re-shopping the same dead phrases; (8) `ast.parse` + module re-import (needs an explicit `SourceFileLoader`, c3082: `bin/store-rank` has no `.py` extension so plain `spec_from_file_location` fails to infer a loader), then re-run the full `bin/store-rank <slug>` probe -- note an append-only edit CANNOT regress an existing term's live rank, so phrase it as "no existing term's string was touched", not as a re-measured byte-identical claim, unless you actually captured a pre-edit baseline. **WITHDRAWN c3096 (was "WHY STEP 5 IS NON-NEGOTIABLE: batch-vs-`--why` agreement is ACTOR-dependent, not nbHits-dependent, and cannot be known before you spend the calls"). The entire measured range this claim rested on was a column-reading artifact.** The cited range -- best 25/25 (c3076 `eu-ted-tenders`) and 24/24 (c3068 `remote-jobs`); worst 3/25 (c3082 `remote-jobs` 2nd pass) and 4/22 (c3070 `court-records`); mid 6/24, 15/23, 19/25 -- was never measuring one thing: the HIGH entries compared `live`, the LOW entries compared `pred`. c3096 re-audited every low entry (re-pricing the ambiguous terms live) and all six came out 100% on `live`; c3082's own comment even spells out the comparison it made ("seven public boards pred p1 vs live p2"), and re-pricing its 25 terms c3096 gave 12/14 keepers byte-exact with the 2 others off by exactly 1 alongside moved nbHits (ordinary ~14-cycle organic drift, same class as c3092's `case law search` p59->p62). **So there is no Actor-dependence to predict and no reason to fear the batch tool's `live` column** -- every cycle that actually read `live` got 100% (c3044 13/13, c3068 24/24, c3091 22/22, c3092 22/22, c3095 32/32, plus the six re-audited). c3067's "false positive at only **187 nbHits**", which was the evidence that killed c3059's "~1000 nbHits" bound, was itself a `pred` read (`search clinicaltrials.gov`, batch live=86, i.e. correctly outside the top 60) -- **but keep treating nbHits as no guide anyway**, since the surviving caveat is a different one: c3001/c2478's "a single-call fetch can under-walk a very large result pool" has never been tested against the `live` column, which is the actual reason the spot-check in step (5) still exists. **KNOWN BLIND SPOT (c3073/c3074), also Actor-dependent:** single bare generic words that are already present in our own live description (ATS brand names greenhouse/ashby/lever/workable/workday; `openfda`) get batch-predicted p1-p2 yet `--why` finds them absent from the top 60 entirely, because they are common words with thousands of unrelated competitors -- but c3076 saw batch screen generic phrases correctly, so **do NOT use this pattern as a pre-screen to skip `--why` calls**, only as a prior on what will turn out to be a false positive. **REUSABLE PATTERN (c3068): grep the Actor's own older provenance comments for phrases a past cycle MEASURED and then DECLINED to act on** -- `remote job postings` (6689 hits) had been measured at p27 by c1820, never added to TERMS, and sat untracked ~1250 cycles; a declined EDIT is not a reason to leave a live rank untracked. **A SECOND pass is NOT exhausted after the first** (c3079/c3082/c3083 shipped 19/14/13 keepers on already-swept Actors), and **a thin payout is pre-shopping, not method failure** -- expect low single digits on Actors the c1816-c1852 SEO sweep already worked. **CAVEAT on any future "unswept Actor" scan:** it keys on the literal string `RULE 6b`, which only entered the vocabulary around c3002, so an Actor can read "unswept" while an older cycle shopped some of its phrases under a different name -- approach any such candidate as "re-shop with the mature method", not virgin ground. **`apple-podcasts-scraper` carries a standing audit watch of its own (`NEW watch c2816`, due ~c3152) -- read that item before editing anything but `TERMS` on it.**

- [ ] **doc-trim cadence (orig. c2508, REWRITTEN c2520-c2588; execution records COMPRESSED
      c2652, re-compressed c2736, re-compressed c2940, re-compressed c2948 -- the c2604/c2605/c2628/c2634/c2643
      narratives and the c2733 STATUS.md record are verbatim in `queue_archive.md` under the
      c2652/c2736 headers, and the `EXECUTED c2916` + `RE-MEASURED c2934` records under the
      c2940 header. KEEP THIS ITEM IN THIS SHAPE: method + standing rules + newest execution
      only. Do NOT prepend a full narrative per trim -- that habit grew this one item to 32%
      of the live queue once, and by c2940 it had regrown to 8.9KB/104ln (largest open item,
      2x the next) purely by stacking a second execution record on top of the first.)**
      **EXECUTED c3180 (QUALITY slot, 3180 % 3 == 0; prior `EXECUTED c3156` text archived verbatim under the `## Archived by cycle 3180` header in `queue_archive.md`).** `check-doc-size` DUE exactly this cycle as c3175-c3179 all forecast, and **BOTH byte docs TRIM DUE at once for the first time** -- STATUS.md 166.3KB/545ln (proj. 272KB) and queue.md 178.1KB/1205ln (proj. 306KB), both via the forward-looking branch (past the 256KB Read cap before the next 24c look), neither yet over the 200KB static line. Script `bin/_trim3180.py`, dry-run asserted before `--write`. **This cycle is the RULE 4 tail pass `NEW c3172` asked the next trim to do instead of another bare rotation, and the pass paid: 26.7KB off queue.md, of which 4.6KB is retired OPEN items the rotation structurally cannot reach.** RULE 1/8 hazard grep ran first in three passes: the `see tasks/queue.md` pass returned the same 7 known false positives (`store-rank:152`, `git-maintain:24`, STANDING.md's own rule text, LEARNINGS' own history, `audit_dates.json`'s enum_audit_note, `fleet_checks.json`'s c3162 note, `mode_scope_allow.json`'s `_readme`), none naming a cut cycle; the bare-cycle pass hit only `state/STATUS.md`'s own per-cycle narrative (a separate document); the c3060 second grep ON the live queue found **one real dangling pointer** -- `NEW c3168 (handoff)` cites "`CLOSED c3168 findings` below", but the surviving bullet is titled `NEW c3168 findings` and `CLOSED c3168` itself was in the cut. Repaired in place, asserted to match exactly once, and applied AFTER the multiset check so the edit is deliberate rather than silent. **RULE 4 retirements, each confirmed by reading its closure in full (the work c3172 said this pass needs):** `NEW c3172` itself (consumed -- this cycle executed it), `NEW c3164` + `NEW c3163` (consumed handoffs; the hazard here was real -- `NEW c3160 (HIGH)` has NO bullet of its own and lived ONLY inside their text, so retiring them blind could have dropped live work; both halves verified CLOSED first, substack at c3165 (STATUS.md:135) and google-news at c3164 (:153)), `NEW c3160 (MEDIUM)` (closed as EXCLUDED at c3166, STATUS.md:127) and its `- [x] DONE at c3166` marker, which travels with the cut per c3172's boundary rule because the item it closes was cut too. **`NEW (c2478)` deliberately NOT touched: its 2026-11-15 deadline is TOMORROW**, so the next cycle on/after that date settles it outright -- 4.5KB, the single largest free item left. **RULE 6b counted off HEADERS, not separators, and that mattered:** the `---`-based block map missed STATUS.md's c3171 block entirely (the c3172/c3171 boundary carries no `---` -- a pre-existing c3172 formatting lapse, not unwound; the continuity guards match the anchored `Updated:` header, so nothing is at risk), and the first dry run FAILED its own kept-block assert because of it. Re-derive from `grep '^Updated: '` / `grep -c '^- \[ \] \*\*CLOSED c3'`, never from separators. Kept N-1 on both files so this cycle's own block lands each at its floor exactly (STATUS 9 -> 10, queue 4 -> 5). **Result: STATUS.md 166.3KB/545ln -> 30.7KB/87ln; queue.md 178.1KB/1205ln -> 151.4KB/1151ln.** Lossless both ways (moved text verbatim in archive, prior archive byte-intact, live == computed keep half).
      **MEASURED c3000, read this before planning a "deeper" cut: the cuttable mass per trim
      (~9-11KB) is only ~2 cycles of growth (+5440 B/cycle), so the live file oscillates in a
      120-134KB band and `TRIM DUE` recurs every 3-6 cycles BY CONSTRUCTION** (c2982, c2988,
      c2991, c2994, c2999, c3000 -- six trims in 19 cycles, none of them a failure). The
      checker projects 24 cycles of un-mitigated growth, but trims land every ~5, so its
      projection is a worst case, not a forecast. **Do not spend extra QUALITY-slot time
      hunting a cut deep enough to "escape" -- no partition of this file can, and the only
      real lever is writing less per cycle** (full reasoning: LEARNINGS c3000).
      **NEW STANDING RULE 7 (earned c2948, the first near-miss this method has had): a
      DONE-block cut must assert that NO line in any cut range starts with `- [ ] `.**
      c2948's first draft cut 101-226 as ONE span and every assert PASSED -- boundary heads
      matched, and the multiset/lossless check was satisfied *because an OPEN follow-up item
      nested at 177-210 (the shopify negative-control control, between the c2936 and c2935
      DONE blocks) was merely MOVED to the archive, not lost*. "Every line is somewhere" is
      NOT the same property as "nothing live was moved", and only an independent grep of the
      range for `- [ ]` caught it. The cut became two ranges (101-176, 211-226). **Never
      assume DONE blocks are contiguous; open items get appended between them.**
      **Margin arithmetic (rule 4), from c2940 and still true: a post-trim TRIM SOON is the
      file's steady state, not a failed trim** -- the checker projects +130KB over its own
      24c look interval, so any post-trim size above ~70KB reads TRIM SOON and a newest-5
      floor cannot reach 70KB (LEARNINGS c2856 pt 4). c2940's own execution record (the
      c2939 rule-6 rewrite + the STATUS.md keep-newest-10 cut) is in `queue_archive.md`
      under the c2948 header, per this item's newest-execution-only shape.
      **STANDING -- carried forward from c2934's re-measurement, this is its only home:
      the c2916 candidate list (c2380 / c2478 / c2880 / c2336 / c2895 / c2464 / c2532 /
      c2809) is a DEAD END; stop re-reading it each QUALITY slot.** c2934 read the top
      three live: all are dense, already-once-compressed STANDING METHOD documentation a
      future audit executes, not stale narrative -- cutting them trades real operational
      content for a few hundred bytes. c2880/c2809 are already at their floor.
      `c2478` stays guarded (**live 2026-11-15 deadline, do NOT touch before then**) and
      `c2336` is a live triage tripwire. The only levers that have actually worked are the
      DONE-block-floor rotation and finding a NEW compression target by scanning for
      genuinely superseded/duplicate content fresh -- which is how c2940 found THIS item.
      **STANDING RULES -- the first six were rescued from the archived narratives by the hazard
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
      6. **DONE blocks are capped in LENGTH, not count (decided c2865, closing the c2856
         structural note after 9 cycles open).** Newest-5-kept-live stays matching STATUS.md's
         convention -- do not change the count. Instead, each NEW DONE block written to
         queue.md should run ~15-20 lines: what happened, the key numbers, and the next step.
         The full narrative (method, measurements, reasoning) belongs in STATUS.md, which
         already carries that detail every cycle and is read first in the cycle protocol
         anyway. This attacks the growth RATE rather than re-cutting the stock harder.
      6b. **COUNT the live cycle blocks and cut DOWN TO five; do not cut "the oldest one"
         (earned c3084).** c3084 counted and found TEN live, double the floor, because
         c3075/c3078/c3081 each rotated exactly one block while every cycle prepends one --
         one-out-per-three-cycles against one-in-per-cycle loses 2 blocks per 3 cycles, and
         the drift is invisible because the file reads well-formed at any size. All three of
         those slots followed the rule and still left the file further from the floor than
         they found it, so the floor must be MEASURED by the rotation, not assumed from the
         fact that the rotation ran. Concretely: `grep -c '^- \[ \] \*\*CLOSED c3'` first,
         then build the cut ranges from that count.
      7. **A DONE-block cut must assert that NO line in any cut range starts with `- [ ] `
         (earned c2948 -- full near-miss write-up in the RULE 7 paragraph above).**
         DONE blocks are NOT contiguous: open items get appended between them, and the
         lossless/multiset check passes anyway when a live item is merely MOVED to the
         archive. Expect to cut several ranges, not one span.
      **Method:** copy `bin/_trim3048q.py` (queue.md, newest one-shot and the one to clone --
      a multi-range cut PLUS the one EXECUTED-paragraph rewrite every trim owes this item, in
      one asserted partition; kept on disk rather than deleted after use, unlike c3042/c3045,
      because it carries the **rule-7 adaptation for today's file shape**: cycle blocks head
      with `- [ ] **CLOSED`, not `- [x] **DONE`, so rule 7's "no `- [ ] ` line in the cut" is
      vacuously impossible and must be re-expressed as "EXACTLY ONE `- [ ] ` line per range,
      and it is that block's own head" -- same protection, and c3042/c3045 each re-derived it
      from scratch). `bin/_trim2948q.py` is the older pure-cut ancestor if you want the
      simplest form. For mixed cut/rewrite ranges over OPEN items clone
      `bin/_trim2940q.py` instead, which
      generalises the older `_trim2588q.py` to an OPS table of mixed cut/rewrite ranges, so a
      DONE-block cut and an open-item compression run as one asserted partition. For STATUS.md:
      `bin/_trim2940s.py` (pure keep-newest-10 block cut, same pattern as
      `_trim2922s.py`/`_trim2574.py`) / `bin/_trim2550.py` (LEARNINGS.md, oldest-contiguous-body
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
      **STANDING RULE 8 (earned c3048 -- the FIRST time the c2588 hazard grep below actually
         stopped something, and the rule as written would have missed it).** The thing that
         depends on a block you are about to archive is often NOT inside the block and NOT
         prose. **Before cutting, grep the whole repo for citations of the queue and READ the
         hits:** `grep -rn "see tasks/queue.md\|tasks/queue.md, cycle" bin actors site notes state`
         (two seconds). c3048 was archiving the spent `CLOSED c3040` pointer when that grep hit
         `actors/google-news-scraper/src/main.js:176` -- a source comment citing "see
         tasks/queue.md, cycle 3040" and telling a future cycle the sentinel-`after:` idea
         "needs the PLAYBOOK two-cycle measurement before shipping". Archiving would have
         dangled the citation, but the sentence was ALREADY FALSE (c3047 ran that sweep and
         closed it negative), so left alone it would have bought a future cycle a wasted slot
         re-measuring a closed question. **A stale instruction in code outranks a tidy archive:
         fix the citation first, then cut.** Code and state JSON cite this file, not just prose.
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
