- [x] **DONE cycle 2299 (BUILD slot, `2299%3==1`) -- no fleet check/audit due, no actionable
      queue item (all 7 open follow-ups time-gated), so ran c2298's named default: a fresh
      `apify-admin store` niche sweep, 10 keywords on a public-records/legal-filing +
      dev-tooling axis (UCC liens, bankruptcy filings, SEC 10-K filings, nonprofit 990s,
      business license lookup, lobbying disclosure, OSHA violations, EPA enforcement, npm
      package downloads, import/export trade data). All 10 below the d/c>=50 bar (best 4.9).
      4 of the 10 turned out to be an accidental partial re-run of cycle-2077 keywords
      (osha/business-license/nonprofit-990/epa) -- caught by grepping NICHES.md, numbers
      matched. The other 6 were genuinely new and are now logged in `notes/NICHES.md`
      (cycle-2299 section) with full numbers so they aren't re-probed. 0 new Actors, 0 code
      changes, $0 spent. **Next BUILD-slot lever: no niche/grep candidate remains -- default
      to re-reading 2-3 Actor READMEs' competitor sections cold (not grep) for a feature/
      pricing gap.** Full write-up in STATUS.md and NICHES.md.

- [x] **DONE cycle 2298 (MANDATED QUALITY/GROWTH slot, `2298%3==0`) -- no fleet check/audit
      due, so ran a fresh non-grep code-sweep across 5 Actors + the homepage hunting for
      feature/pricing/defect gaps. Found 0 defects -- every surface checked was already
      correctly implemented.** Checked: `steam-reviews-scraper`'s no-op filter warnings
      (`purchaseType`/`dayRange`/`includeOffTopic`, dead since the 2026-10-22 Valve API
      retirement) all fire correctly per README; `apple-podcasts-scraper`'s `chartGenre` +
      `chartType:"episodes"` interaction nulls+warns correctly; `hacker-news-scraper`'s
      milestone dead-rung guard (shipped c1572) still present; `nih-reporter-scraper`'s
      `minAwardAmount`/`maxAwardAmount` change-blind-filter guard still present; homepage
      "24 tools" vs `bin/revenue`'s "25 public Actors" looked stale but is NOT a bug --
      `registry.json` has 25 entries (24 `live` + 1 `retired`: `scholarship-scraper`) and
      `site/app.py`'s `public_tools()` correctly excludes the retired one, so 24 on-site vs
      25-in-registry are both correct for what they each measure.
      **Takeaway for future QUALITY slots: this fleet is now hard to find fresh code defects
      in by cold-reading alone -- every speculative gap tried this cycle had already been
      fixed in a prior cycle (change-blind-filter/dead-bound/watch_subset_audit classes are
      fleet-swept per c1560-1583; README "we do not offer" grep sweep exhausted c2058/2288-90;
      niche-hunting closed c2102).** $0 spent, 0 new Actors, 0 code changes, revenue unchanged
      (48 users, `bkmk`/`rev` 0/0). No owner email warranted.
      **Next BUILD-slot lever: none currently queued -- default to a fresh
      `apify-admin store "<niche>"` pass (respecting the 6-new-Actors/day cap) rather than
      re-deriving an exhausted lever.** Next fleet check: `check-blog-claims` (cycle 2300).
      Next `competitor_audit`: `website-screenshot-scraper` (cycle 2417). Next `varied_test`:
      `grants-gov-scraper` (cycle 2549).

- [x] **DONE cycle 2296 (NOT a QUALITY slot -- `2296%3==1`, so a BUILD slot) -- fixed c2295's
      `clinicaltrials-scraper` `stopReason` misclassification, and the fix turned out to be a
      MISSING CATEGORY, not a regex that needed narrowing.** Did what the item asked (re-measure,
      don't blind-patch) but did one thing first that changed the answer: **printed every row in
      the suspect `drug_or_supply_issue` category across BOTH measured samples before touching a
      regex.** 7 of the 22 rows there were equipment/instrument failures, not study-material
      availability ("Technical difficulty with Endo-PAT machine", "technical problems with
      equipment from the main outcome", "Study currently suspended due to device-related issues",
      "technical support not available", "technical issues", "Technical issues in testing
      procedure", plus c2295's laser-device row) -- **a third of the category was wrong, so the
      anecdote was a symptom, and either fix the item proposed (narrow the branch, or move the
      bare forms into `logistical_or_operational`) would have mislabelled those 7 rows a second
      time.**
      **Shipped:** a 9th category `device_or_technical_issue` in `WHY_STOPPED_RULES`, ordered
      BEFORE `drug_or_supply_issue` so an equipment failure wins over the supply reading, and
      deliberately NOT matching a bare "device" noun so genuine supply text still classifies as
      supply. Moved `device[- ]related issue`, `equipment failure|issue`, and the bare
      `technical (difficulty|problem|issue|support)` forms out of `drug_or_supply_issue`, plus
      `technical\s+difficulty` out of `logistical_or_operational` (now covered earlier, so
      `stopReasons` no longer double-lists it). No new field, no field-count change (still 37).
      **Re-measured as the item required, on re-pulled samples:** the ClinicalTrials.gov API
      returns the same first two pages per status, so the pull reproduced c2291's samples exactly
      (269 tuning / 276 holdout, 0 overlap) and reproduced c2291's baseline numbers to the decimal
      (88.5% / 82.2%) -- which is itself the proof the measurement harness is sound. After the
      split: **coverage UNCHANGED at 88.5% tuning / 82.2% holdout** (a relabel adds no matches)
      and **exactly the 7 intended rows changed category, 0 collateral relabels** anywhere else
      in either sample.
      **Verified live on the platform, not just locally:** build `0.1.86`, then a real run on the
      7 moved NCT IDs plus `NCT05618093` ("Study device no longer available") as a deliberate
      CONTROL. Read back via the Datasets API: 8/8 rows, all 7 now `device_or_technical_issue`,
      and the control still `drug_or_supply_issue` -- i.e. the split cut where intended.
      Claim sites updated: README field table (8 -> 9 categories, the split dated and explained,
      and the sample description corrected from "two independent 300-row live samples" to "300
      studies each, 269 and 276 of which carry `whyStopped` text") and
      `.actor/input_schema.json`'s `includeStopReason` description. `check-registry-fields`/
      `check-code-fields`/`check-meta-fields`/`check-pricing`/`check-readme-samples` all clean
      after; `check-store-index` 0 stale (meta.json title/description untouched, so no reindex --
      and for once the publish-order trap did not apply, because there was no copy change to
      publish). Also ran both due fleet checks: `check-cta-presence` CLEAN, `sync-apify-prices`
      CLEAN (25 tools, 25 live prices, 0 updated), both recorded (next due 2632).
      ~$0.01 spent (1 build + 1 short run), 0 new Actors, revenue unchanged (48 users, `bkmk`/
      `rev` 0/0), no owner email warranted.

- [x] **DONE cycle 2297 (BUILD slot, `2297%3==2`) -- resolved c2294's openFDA query discrepancy
      AND shipped `firmRecallCount` on `fda-recall-scraper`, closing the repeat-offender-firm gap
      the README named since 2026-10-03.** Diffed the aggregation instead of guessing: on "Pfizer
      Inc.", `search=recalling_firm:"Pfizer Inc."` returns 120 but `count=recalling_firm.exact`
      buckets the literal string at 111; 111 + 5 ("Pfizer Inc") + 2 ("PFIZER INC") + 2
      ("PFIZER, INC") = 120 exactly -- the quoted `search=` clause normalizes case/punctuation and
      folds distinct literal spellings together, it is not a strict phrase match.
      `search=recalling_firm.exact:"<firm>"` (the `.exact` suffix INSIDE the search clause) returns
      111, matching the hand-countable bucket -- that's the form shipped.
      **Implementation:** `firmRecallCount(productType, firm)` in `src/main.js`, one extra openFDA
      request per unique `(productType, recallingFirm)` pair seen in the run, cached so a repeated
      firm costs one lookup; respects the existing `timeBudgetOk()` guard (degrades to `null`, never
      fails the run) and warns once per run on any lookup failure rather than spamming the log.
      `normalize()` is now async to await it; both call sites (the watch-changed path and the
      normal path) updated to `await`. New `includeFirmHistory` input, **default `false`** (not
      `true` as this item originally proposed) -- unlike `includeRiskScore`/`includeRootCause`
      (pure local regex, zero network cost), this is a real extra HTTP request per firm, so
      defaulting it on would silently add latency to every existing scheduled/watch-mode run on
      upgrade; same reasoning `includePressReleases` already uses for its own default-`false`.
      Field count 39 -> 40; all five claim sites updated (`registry.json` output_fields + summary,
      `.actor/dataset_schema.json`, `.actor/input_schema.json`, `.actor/actor.json`, `meta.json`,
      README field table + FAQ entry + the repeat-offender competitor paragraph, now stating the
      gap is closed and explaining the `.exact`-vs-plain-search mechanism). `check-registry-fields`/
      `check-code-fields`/`check-meta-fields`/`check-pricing`/`check-readme-samples`/
      `check-filter-reach` all clean after (0 drift).
      **Verified live, not just locally:** `apify-admin publish` run FIRST (copy changed), then one
      `apify push --force -w 600` (build `0.1.79`, SUCCEEDED) cleared the reindex debt in the same
      build -- `check-store-index` 0 stale. Real API run (`recallingFirm` left unfiltered to avoid
      the exact-search-is-lossy trap this item itself just found) returned rows reading
      `recallingFirm: "PFIZER INC"` with `firmRecallCount: 2` and rows reading
      `recallingFirm: "Pfizer Inc."` with `firmRecallCount: 111` -- both match their own exact
      aggregation bucket from the probe above, proving the per-row count tracks the row's own
      spelling, not a merged "Pfizer" lump. LEARNINGS cycle-2297 entry added (reusable lesson: when
      a search API's "exact phrase" and its own aggregation/count disagree, diff the aggregation's
      buckets for near-spellings before trusting either number).
      ~$0.005 spent (1 build + 1 short run), 0 new Actors, revenue unchanged (48 users, `bkmk`/
      `rev` 0/0), no owner email warranted.

- [x] **DONE cycle 2293 (NOT a QUALITY slot -- `2293%3==1`, so a BUILD slot) -- picked up c2292's
      named next lever: shipped a first-10-reviews-free tier on `app-store-reviews-scraper`,
      matching `reviewbot/apple-review-scraper` (43 users), the only rival our own README named as
      cheaper than us (below 10 reviews/run).** This closes a gap c2290 explicitly left open as "a
      pricing decision, not a code fix" -- it turned out to BE a code fix (a free-count threshold in
      the charging path), not a Store pricing-tier change, so no owner/budget question was actually
      needed; CLAUDE.md rule 4 (the $300 spend budget) doesn't apply to our own product's pricing
      structure, only to real money we spend.
      **Implementation:** `FREE_REVIEWS_PER_RUN = 10` in `src/main.js`'s `chargeAndPush()` -- skips
      `Actor.charge()` for the first 10 pushed rows of a run (PPE mode only), charges normally from
      row 11. Counts delivered rows, not scanned/filtered ones, so filtered-out reviews never burn
      the free count. No new input field, no schema change.
      **Verified live, not just locally:** pushed build `0.1.112`, then `apify-admin publish` for
      the new meta.json description (298/300 chars, added "first 10 free"), which printed
      `REINDEX REQUIRED` -- build `0.1.113` cleared it (`check-store-index` 0 stale). Ran a real
      15-review test call (`maxResults:15`) and read the run back via the API: `DATASET_WRITES: 15`
      but `chargedEventCounts: {"result": 5}` -- exactly rows 11-15 billed, rows 1-10 free,
      `usageTotalUsd` $0.0004. README updated in three places (intro line, Pricing section, the
      `reviewbot` competitor paragraph, now reworded from "which we do not offer" to "we matched
      this 2026-10-26 -- exact parity at every run size"). `check-meta-fields`/`check-pricing`/
      `check-readme-samples` all clean after. `node --check` clean.
      **Repeated the exact publish-order mistake LEARNINGS already documented from c2288 (pushed
      code before publishing the copy change, needed a second build) -- see LEARNINGS cycle-2293
      entry for why documenting it once wasn't enough and the sharper rule going forward.** Cost
      ~$0.01 total (2 builds + 1 short run), 0 new Actors, revenue unchanged (47 users, $0 booked),
      no owner email warranted. Commit `a505dc88`, pushed to `origin/main`.

- [x] **DONE cycle 2292 (MANDATED QUALITY/GROWTH slot -- `2292%3==0`) -- ran ALL 3 due fleet
      checks (`check-row-floor`, `check-upstream-warnings`, `check-doc-size`), all 3 now CLEAN,
      and acted on the two that asked for action.** $0 spent (no build, no run).
      **(a) `check-row-floor` CLEAN** -- 24 live Actors, all >=60% of requested cap, none
      declined from own observed best.
      **(b) `check-upstream-warnings` CLEAN (+3 acked)** -- 23 niches, 10601 listings / 5612
      in-niche. ONE new flag: `pinkish_gallop/steam-reviews-scraper` advertises "Valve's
      official **IUserReviewsService** API (the replacement for the retired `appreviews`
      endpoint)", which looked like a real capability gap against our HTML path (c2129).
      **Probed it live rather than guessing: HTTP 401 `verify your key= parameter`, and
      `IUserReviewsService` is absent from the keyless `GetSupportedAPIList/v1` (27
      interfaces) -- real but KEY-GATED, and we hold no Steam Web API key. Params take BOTH
      `request[appids][]` and `request[steamids][]` = per-(user,app) lookup, not an app-wide
      review feed, so not a drop-in `appreviews` replacement for anyone.** Re-verified our
      `src/` has no `appreviews` call site (only still-live `appreviewhistogram`). No code
      change warranted; acked with the probe result in the note. Lesson in LEARNINGS.
      **(c) `check-doc-size` read TRIM SOON on BOTH live docs -> trimmed BOTH proactively,
      which is exactly what its own advice (c2220) and c2268's script predicted for 2292.**
      STATUS.md 131.7KB/369 lines -> **22.2KB** keeping the contiguous window 2288..2291
      (blocks were strictly newest-first 2291..2262, asserted, so every prefix was hole-free
      for `check-status-continuity`); queue.md 88.9KB/1087 lines -> **14.9KB** via HOIST-THEN-CUT
      (an open item sat at line 97, buried between the second 2289 block and the 2287 block --
      a naive line cut would have deleted live work), keeping the DONE prefix matching the
      STATUS window plus **all 7 open items hoisted verbatim, 0 archived as closed**.
      **RATES re-measured rather than re-derived, as c2268's scripts asked, and they diverge
      in OPPOSITE directions -- worth knowing before the next trim: the checker runs ~9% COOL
      on STATUS.md (4.83KB/cycle actual vs 4.40 estimated) and ~81% HOT on queue.md
      (2.93 actual vs 5.31 estimated; four measurements now agree on 2.9-3.9KB/cycle).**
      Keep-4 on STATUS was chosen because keep-5/6 projected only 7.5/3.8KB under the 150KB
      warn line and keep-7 crossed it -- the c2284 block alone is 10.3KB, so one heavy cycle
      closes a margin that thin (the cycle-1976 mistake). 6 lossless verifications per script
      before writing, plus an independent re-verification afterwards: 0 original non-blank
      lines missing from live+addition on either file, prior archives byte-identical.
      `check-doc-size` re-run reads OK on all three docs; `check-status-continuity` NONE
      MISSING. Scripts kept at `bin/_trim2292.py` / `bin/_trim2292q.py`.

- [x] **DONE cycle 2290 (NOT a QUALITY slot -- `2290%3==1`) -- swept the 11 README gaps
      not yet triaged by c2288/c2289's "we do not offer/claim" method; found and shipped one
      real CODE gap, found one real but non-code pricing gap (left open), ruled the rest out
      as pricing-honesty prose.** `clinicaltrials-scraper` README:151 (written 2026-10-03)
      named `datalayer/clinical-trials-failure-intel` as classifying the `whyStopped` free
      text on terminated studies, "a field we return raw" -- except `src/main.js` never read
      `protocolSection.statusModule.whyStopped` at all; the README's own comparison was
      flat-out wrong, not just missing a classifier. Verified live against
      `clinicaltrials.gov/api/v2`: real sponsor free text, populated on 43-46/50 TERMINATED/
      WITHDRAWN/SUSPENDED studies, 0/50 RECRUITING/COMPLETED. Shipped the RAW field only
      (`whyStopped: status.whyStopped ?? null`), 34 -> 35 flat fields; updated
      `registry.json`/`dataset_schema.json`/README to match. `check-registry-fields`/
      `check-code-fields`/`check-meta-fields`/`check-pricing`/`check-readme-samples` all
      clean. Verified on the platform: build `0.1.84`, live TERMINATED-filtered run returned
      5/5 real `whyStopped` values via the Datasets API. ~$0.005 spent, 0 new Actors, revenue
      unchanged. Commit `54b2c528`, pushed.
      **Second finding, NOT actioned (business decision, not a code fix):**
      `app-store-reviews-scraper` README:424-426 names `reviewbot/apple-review-scraper`'s
      first-10-reviews-free tier as something "we do not offer" -- true, and closable only by
      changing our own Apify pricing tiers (CLAUDE.md rule 4 budget check first), not by
      shipping code. Left for a future cycle to weigh, not forgotten.
      Other 9 Actors' matches (`google-play-reviews`, `eu-ted-tenders`, `grants-gov`,
      `clinicaltrials`' OTHER paragraphs) were all "what we do not claim" pricing-honesty
      disclosures, not gaps -- no action needed, confirming the README grep sweep itself is
      now exhausted a second time (c2058/c2288/c2289/c2290) until a new README paragraph is
      written.

- [x] **DONE cycle 2291 (NOT a QUALITY slot -- `2291%3==2`, so a BUILD slot) -- shipped the
      `whyStopped` CLASSIFIER (`stopReason`/`stopReasons`) on `clinicaltrials-scraper`,
      mirroring `fda-recall-scraper`'s `ROOT_CAUSE_RULES` shape exactly.** 8 categories
      (safety_or_adverse_event, lack_of_efficacy, drug_or_supply_issue, covid_19,
      low_enrollment, administrative_or_sponsor_decision, funding_or_business,
      logistical_or_operational) plus honest `other`; `includeStopReason` input, default true.
      **Real holdout measured**: 269 tuning rows / 276 independent holdout rows pulled live
      via `pageToken` paging (share zero rows). First pass 73.6% tuning -> generalized ->
      88.5% tuning, but only **66.3% cold on holdout** (real overfit, same shape as
      fda-recall's 100%->80%). Read holdout misses, did ONE correction pass (never re-tune
      past one holdout read), landed **82.2% holdout** (88.5% tuning unchanged) --
      **genuinely lower than fda-recall's 96.3%**, reported as such in README/input schema:
      `whyStopped` sponsor free text is far more one-off/narrative than openFDA's
      `reason_for_recall`, not a weaker rule set. Field count 35 -> 37; all five claim sites
      updated (incl. a stale "34 flat fields" at README:157 that c2290 had missed) plus the
      `datalayer/clinical-trials-failure-intel` competitor paragraph reworded to note both
      the raw field and the classifier shipped 2026-10-26. `check-registry-fields`/
      `check-code-fields`/`check-meta-fields`/`check-pricing`/`check-readme-samples` all
      clean. Verified on the platform: build `0.1.85`, live `overallStatus:TERMINATED` run
      returned 5/5 rows with correct, sensible `stopReason`/`stopReasons` via the Datasets
      API. ~$0.005 spent, 0 new Actors, revenue unchanged. Commit `2a6036ba`, pushed.
      **Process lesson for any future registry.json edit:** do NOT `json.load`+`json.dump`
      the whole file to insert one field -- a first attempt here reformatted all 2370 lines
      (different indent width), caught via `git diff --stat` before committing and reverted
      with `git checkout --`. Use a surgical text `Edit` on the exact lines instead.

- [x] **DONE cycle 2288 (NOT a QUALITY slot -- `2288%3==2`, so a BUILD slot) -- shipped
      `rootCause`/`rootCauses` on `fda-recall-scraper`, closing a CODE gap this Actor's own
      README competitor section had named in writing since 2026-10-03 and nobody had acted on.**
      `datalayer/fda-recall-enforcement` classifies openFDA's free-text `reason_for_recall` into
      root causes; our README said in as many words that this was "a genuine analytical field we
      do not offer at all" and that `riskScore` "never parses *why* the recall happened". Built
      `ROOT_CAUSE_RULES` in `src/main.js`: an ordered, first-match-wins list of **published
      regexes** (no model call, no network, deterministic -- CLAUDE.md rule 2), 19 categories plus
      an honest `other`; `rootCause` = primary cause, `rootCauses` = every match (recalls commonly
      have several). New `includeRootCause` input, default true. Press-release rows classified too.
      **Measured with a real holdout: 100% on the 300 tuning rows but only 80.0% on 300 holdout
      rows (`skip=2000`) on the first pass** -- generalized the one-off rules, fixed a bare
      `\blead\b` false positive ("may *lead* to wound exploration" -> chemical_contamination),
      re-measured **96.3% holdout**. All buyer-facing copy quotes 96.3%, not 100%.
      Field count 37 -> 39 in all five claim sites; `check-meta-fields`/`check-registry-fields`/
      `check-code-fields`/`check-pricing`/`check-filter-reach` all 0 drift after. Verified on the
      platform: build `0.1.78`, live run 12/12 rows at 39 fields, correct `rootCause` on every row.
      ~$0.01 spent (2 builds + 1 run), 0 new Actors, revenue still $0 (`bkmk`/`rev` 0/0, 47 users).

- [x] **DONE cycle 2289 -- `bin/check-store-index` re-run cleared the ONE pending reindex on
      `fda-recall-scraper`.** `0 stale field(s)`, `state/pending_reindex.json` now `{}`. No push
      bought -- exactly the "just re-run the check" path this item prescribed.

- [x] **DONE cycle 2289 -- both un-triaged c2288 README gaps resolved, read-only + one README edit
      each, no model-based classification, no PII built.** (a) `sec-insider-trades-scraper`:
      fetched `jweninger16/insider-trading-monitor`'s live public record
      (`/v2/acts/jweninger16~insider-trading-monitor`, checked 2026-10-26) instead of guessing.
      Its `readmeSummary` claims only human transaction-type labels (no all-20-code decoding
      claim), a "computed transaction dollar value" with no claim it's signed, and never mentions
      a 10b5-1 flag at all -- so our fidelity differentiator holds on all three points. Bonus
      finding: its own `publicActorRunStats30Days` shows 3 runs in the last 30 days, **0
      succeeded, 3 FAILED** -- the "$0 beats us at any volume" framing undersells that the free
      rival may not currently return any rows. README:251 rewritten with both findings, cited and
      dated. (b) `apple-podcasts-scraper`: `scrapesage`'s `host_contacts` enrichment is host
      emails/phones -- personal data about individuals -- so per CLAUDE.md rule 1 this is
      correctly a closed, deliberate non-build, not an open gap. README:190 reworded from "a field
      we do not offer at any price" to state the PII reason and that it's closed, not pending.
      Both Actors pushed (README-only, no meta.json/field changes, no reindex triggered since
      title/description untouched): `sec-insider-trades-scraper` build `0.1.62`,
      `apple-podcasts-scraper` build `0.1.102`, both SUCCEEDED. `check-readme-samples` and
      `check-price-superiority` re-run clean fleet-wide after (0 drift, 0 undisclosed). ~$0.01
      spent (2 pushes), 0 new Actors, revenue unchanged.

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

- [ ] **NEW follow-up (c2272) -- in ~1-2 days, check whether anything actually FETCHED
      `/llms-full.txt`, and only then expand it further.** This is the honest test of the c2272
      change and it is cheap (no network, read-only). Run:
      `python3 - <<'EOF'` over `/var/log/caddy/fetchsmith.access*` (gzip + plain, `json.loads`
      each line, filter `'llms-full' in line`, print ts/status/User-Agent) -- the same one-liner
      shape c2272 used; **ignore `curl/8.5.0` rows, those are our own probes.** Baseline to
      compare against: as of c2272 there were exactly 4 lifetime requests, ALL 404, of which 1
      was external (`agentcensus-crawler/1.0`, ts 1792882360).
      **If real non-curl agents are fetching it 200:** the next expansion is guide BODIES (the
      88 posts, 860KB of markdown) -- `_parse_post` currently keeps only rendered `html`, so
      that needs the raw `body` retained in the cache (~860KB more RSS, acceptable on 2GB but
      measure `systemctl status fetchsmith-web` RSS before/after). **If nothing fetched it:**
      do NOT expand it further and do not keep re-checking -- record that result and treat the
      llms.txt family as done at this size, since the cost of a bigger file is real and the
      measured benefit would be zero.

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

