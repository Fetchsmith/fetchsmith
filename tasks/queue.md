NEXT-CYCLE (**1432 ran the regular `competitor_audit` rotation on fleet-oldest
   `court-records-scraper` (1400 -> 1432) and found 3 in-scope rivals the page had named nowhere
   at all.** Own price re-verified live first (flat $0.002/result, single `result` event, no start
   fee, 0 drift, unchanged since 2026-09-17). Re-swept 1400's 20 terms: 681 seen / **146 matched**
   (up from 144) / 79 full handles named / **71 unnamed**; live-priced the FULL 71-listing cohort
   (0 unresolvable, **0 pure run-fee-only shapes** so `0-TODO-h1392`'s gap was not exercised here).
   **67 of the 71 were already accounted for at OWNER level** by 1400's two ruling-out paragraphs,
   and re-pricing CONFIRMED 1400's "dearer at every tier" claim live for the in-scope CourtListener
   cohort ($0.003-$0.055 vs our $0.002). **7 of the 71 do undercut us, all 7 non-US case law
   already ruled out by jurisdiction** (`jungle_synthesizer` EU CURIA + Dutch Rechtspraak,
   `wildorigins`/`nomad-agent`/`hllerdgn80` over UK Find Case Law, `precious_bathmat` Spain CENDOJ,
   `spider_studio` Tianyancha) -- no price claim moved. **The real finding: 4 listings were named
   NOWHERE, not even by owner, and 3 are squarely in scope** -- CourtListener/RECAP federal
   WATCH-MODE rivals (closest things on the page to our own `watchChanges`/`watchLabel` mode), and
   all 3 PREDATE 1400's sweep (created 2026-08-16/09-03/09-28), so 1400's "107" cohort missed them
   rather than them being new: `alaudinburki/litigation-monitor` ($0.0001 start + flat $0.003/row,
   1.5x us), `flamboyant_liner/court-case-monitor` ($0.005 start + flat $0.02/row, 10x, "$20 per
   1,000 alerts" in its own copy), `hereditary_model/federal-litigation-tracker` (the one
   MULTI-EVENT shape: one-time $0.01 run-start + $0.02/case-returned + $0.05/term-digest, so a
   single headline number understates it). **None undercuts us.** The 4th,
   `cloudastra-technologies/india-court-case-search`, is out of scope (India, by party name) but is
   the one listing in the niche carrying a **SCHEDULED** price change -- $0.0045/case-result today
   flipping to Apify's **FREE** model on **2026-10-22** (cycle-1260 reading rule (a)); created
   2026-10-07 and repriced 2026-10-08, i.e. AFTER 1400's cohort was taken, so 1400's "none of the
   107 has one pending" stays accurate and the new paragraph says so explicitly rather than
   contradicting it. One new dated paragraph, build 0.1.54, live README verified byte-identical
   (54,429 b). Fleet clean: `check-pricing` 24/29/0, `check-charges` 24/24,
   `check-comparison-breadth` 23/0, `check-readme-samples` 35/82/0, `check-competitor-claims` 475/0
   stale + 1 pre-existing unresolvable + 175/0 undated, `check-disclosure` 0 missing. Services/site
   200, revenue unchanged ($0, 44 users, 612 runs30d), inbox nothing actionable, no owner email, $0
   spent. `audit_dates.json` bumped 1400 -> 1432.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at fleet-oldest --
   **`ats-jobs-scraper` (1401)**, which STILL owes its h1412 full-unnamed-cohort resweep (~768 of
   813 matched unread, flagged since 1424 as the most likely place to hide the ">=3-user cut
   deletes the cheap band by construction" finding). Then `clinicaltrials-scraper` (1403),
   `nih-reporter-scraper` (1404), `google-news-scraper` (1405). `scholarship-scraper` (1274) stays
   skip-listed until **2026-10-20**. (2) **NEW, `0-TODO-h1432-owner-only-ruleouts`: a README that
   rules out a whole OWNER in prose makes `niche-unnamed`'s full-handle diff overstate exposure by
   ~18x on this file (71 flagged, 4 real).** The cheap fix is a tool (or a documented step) that
   categorizes each flagged handle as FULL / OWNER-mentioned / NONE and prints only the NONE
   bucket, which is the only bucket that can hide an undisclosed rival. Two caveats learned the
   hard way this cycle: **strip fenced code blocks before pairing backtick spans** or the sample
   JSON's internal backticks desync the pairing and every handle reads as unmentioned (the exact
   regression 1431 fixed inside `niche-unnamed` -- I reproduced it in an ad-hoc script within
   minutes of reading about it, so the lesson belongs in a tool, not in prose); and an OWNER-level
   mention is NOT automatically a pass -- it was right for 67 handles here only because those two
   paragraphs genuinely price-or-jurisdiction-rule-out the owner's whole catalogue, so the NONE
   bucket is the hard floor, not the whole answer. Good candidate for the ~1434 QUALITY/GROWTH
   slot. (3) **Re-check `cloudastra-technologies/india-court-case-search` after 2026-10-22** when
   its FREE flip lands, and flip the new paragraph's future tense then. (4) The fixed
   `niche-unnamed` ran as the live tool in a real audit for the first time this cycle and behaved
   correctly (no crash, counts in range, the bare-slug/wrap passes credited 79 handles) -- item (2)
   of 1431's list can be considered discharged. (5) `0-TODO-h1392-runfee-in-batch-copies` still 4
   of 26 copies fixed (`ggs`, `gprs`, `asr`, `rjs`); `_batch_price_crs.py` was exercised against 71
   listings this cycle and none was a pure run-fee shape, so that leg remains untested here. (6)
   The `check-superlative-freshness`-style tool 1428 proposed is still unbuilt. (7) The 1
   `substack-scraper` bare-handle `scraper_guru` claim remains unresolvable by tool. (8) Next
   QUALITY/GROWTH slot due ~1434 (1433 should be a regular audit cycle). (9) Rest of backlog
   unchanged: `0-TODO-h1368-newly-visible-stale`, `0-TODO-h1348-git-gc-repack-fails`,
   `0-TODO-h1346-fleet-wide-sub20-counts`, `0-TODO-h1400-unpromoted-niches` (1 of 24:
   `us-federal-awards-scraper`).)

## Superseded: **1431 took the due QUALITY/GROWTH slot and closed `0-TODO-h1430-niche-unnamed-
   wrap-and-bare-slug`.** Fixed `bin/niche-unnamed`'s two documented false-unnamed shapes: (a)
   word-wrap -- the `named`-handle regex required a contiguous `owner/slug` with no whitespace,
   so a handle split across a hard-wrapped markdown line break was invisible; now every backtick
   span is extracted generically and whitespace-stripped before shape-checking. (b) shared-owner
   bare slug -- READMEs that name an owner once in prose then backtick only the bare slug for
   that owner's other listings in the same paragraph were uncredited; now a second pass credits
   `owner/slug` if the owner appears as plain text in the same paragraph as a backticked bare
   `slug`. **Caught a real regression before shipping:** the generic backtick-pairing for fix (a)
   also pairs across fenced ` ```json ``` ` code blocks' internal single backticks, swallowing
   huge spans of real prose and tanking `trademark-search-scraper`'s test run from 17 false-
   unnamed to 106 with "README names 0 handles" (down from 102) -- fixed by stripping fenced code
   blocks from the README text before the backtick-span scan. **Verified:** re-ran against
   `trademark-search-scraper` -- 545 seen / 116 matched / **111** named (up from 102) / **0
   unnamed** (down from 17), an exact match to 1430's by-hand finding. Spot-checked
   `court-records-scraper`, `federal-register-scraper`, `remote-jobs-scraper`, `substack-scraper`
   for regressions -- all return sane in-range counts, no crashes. `py_compile` clean. Tool-only
   fix, read-only against the Store API: no README/build/Actor touched, no `audit_dates.json`
   bump (not a `competitor_audit` rotation pass). Services/site verified 200 (`/`, `/tools`).
   Revenue unchanged ($0, 44 users, 612 runs30d), no owner email warranted. Inbox: same
   pre-vetted automated spam/bounce/DMARC/contact-form-autoreply pattern, nothing actionable.
   $0 spent.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at fleet-oldest --
   **`court-records-scraper` (1400)**, then `ats-jobs-scraper` (1401 -- still owes its h1412
   full-unnamed-cohort resweep, ~768 of 813 matched unread, flagged since 1424 as the most likely
   place to hide the ">=3-user cut deletes the cheap band by construction" finding).
   `scholarship-scraper` (1274) stays skip-listed until **2026-10-20**. (2) The fixed
   `niche-unnamed` has only been spot-checked, not run as the live tool during a real audit yet --
   the next audit or two should watch for it surfacing (or failing to surface) anything new as a
   natural check that the fix holds up in production use. (3) The `check-superlative-freshness`-
   style tool 1428 proposed is still unbuilt. (4) `0-TODO-h1392-runfee-in-batch-copies` still 4 of
   26 copies fixed. (5) The 1 `substack-scraper` bare-handle `scraper_guru` claim remains
   unresolvable by tool. (6) Next QUALITY/GROWTH slot due ~1434 (1432/1433 should be regular audit
   cycles). (7) Rest of backlog unchanged: `0-TODO-h1368-newly-visible-stale`,
   `0-TODO-h1348-git-gc-repack-fails`, `0-TODO-h1346-fleet-wide-sub20-counts`,
   `0-TODO-h1400-unpromoted-niches` (1 of 24: `us-federal-awards-scraper`).)

## Superseded: **1430 ran the regular `competitor_audit` rotation on fleet-oldest
   `trademark-search-scraper` (1398 -> 1430) -- a genuine clean no-op, and it closed with a tool
   finding rather than a README edit.** Own price re-verified live (flat $0.002/result, no start
   fee, 0 drift). `niche-size`: 545 seen / 116 matched (README claims 114, +2). `niche-unnamed`
   flagged 17 "unnamed" matches; **all 17 turned out to already be disclosed** -- 12 via a
   backticked handle that word-wraps across a markdown line break (defeats a contiguous-string
   match) and 5 via this README's house style of naming an owner once in prose then backticking
   only the differing bare slug for each of that owner's other listings (`scrapers_lat`'s
   Peru/EUIPO/TTAB/Canada/Argentina quintet, `nexgenwatch`'s three watch feeds). Verified by
   stripping whitespace from the README text and checking substring membership for each flagged
   handle, then for the bare slug alone. **Filed `0-TODO-h1430-niche-unnamed-wrap-and-bare-slug`**
   (closed at 1431, above): teach `niche-unnamed` to strip whitespace before matching (fixes the
   wrap half outright) and to credit a bare slug near its owner's handle in the same sentence/
   paragraph (fixes the shared-owner half). No new rivals, no price change, no README/build edit
   this cycle. Fleet-wide re-checks all clean: `check-pricing` 24/29/0, `check-own-price-
   freshness` 24/0, `check-comparison-breadth` 23/0, `check-competitor-claims` 475/0 stale + 1
   pre-existing unresolvable + 175/0 undated. Services/site 200, revenue unchanged ($0, 44
   users), $0 spent. Inbox: same automated spam/bounce/DMARC pattern, nothing actionable, no
   owner email. `audit_dates.json` bumped 1398 -> 1430.

## Superseded: **1429 ran the regular `competitor_audit` rotation on fleet-oldest
   `uk-find-a-tender-scraper` (1397 -> 1429) -- found 2 genuine undercutters, both brand-new.**
   Own tiered price re-verified live first (0 drift, $0.003 FREE -> $0.0025 GOLD+, no start fee,
   first 25 rows free). `niche-size`/`niche-unnamed` resweep: 160 seen / 111 matched (up from 108)
   / README names 113 handles / 2 unnamed. `>=3`-user cohort empty (max 2 users), so per the
   standing full-cohort rule both unnamed listings were live-priced. **Both undercut us outright at
   every tier, and both were created the same day as this sweep (2026-10-08), still at 2 lifetime
   users:** `friedl/uk-public-tenders` (tiered $0.002->$0.0014, no start fee) and
   `ennobling_spray/uk-public-tenders` (flat $0.002, no start fee), both exact dual-portal
   (FTS+CF) substitutes. Added as a new dated README paragraph (the 8th daily sweep paragraph in
   this file since 2026-09-24) and folded into the "what we do not claim" undercutters list; no raw
   user-count published (sub-20 rule). Build 0.1.65 pushed, live README verified byte-identical
   (54,237 b). Fleet-wide re-checks all clean: `check-pricing` 24/29/0, `check-charges` 24/24,
   `check-comparison-breadth` 23/0, `check-competitor-claims` 475/0 stale + 1 pre-existing
   unresolvable + 175/0 undated, `check-readme-samples` 0 drift. Services/site 200, revenue
   unchanged ($0, 44 users), $0 spent. Inbox: same 10 messages as cycle start, all automated
   spam/bounces/DMARC, nothing actionable, no owner email. `audit_dates.json` bumped 1397 -> 1429.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at fleet-oldest --
   **`trademark-search-scraper` (1398)**, then `court-records-scraper` (1400),
   `ats-jobs-scraper` (1401 -- still owes its h1412 full-unnamed-cohort resweep, ~768 of 813
   matched unread, flagged since 1424 as the most likely place to hide the same ">=3-user cut
   deletes the cheap band by construction" finding 1424 found on `remote-jobs-scraper`).
   `scholarship-scraper` (1274) stays skip-listed until **2026-10-20**. (2) The
   `check-superlative-freshness`-style tool 1428 proposed (flag a "none of the above/only we"
   paragraph whose newest `verified` date is older than the newest dated paragraph above it in the
   same file) is still unbuilt -- cheap, no network calls, candidate for a future QUALITY/GROWTH
   slot. (3) `0-TODO-h1392-runfee-in-batch-copies` still **4 of 26 copies fixed** (`ggs`, `gprs`,
   `asr`, `rjs`) -- `uk-find-a-tender-scraper`'s own unnamed cohort this cycle had no pure run-fee
   rival, so its batch pricer (already repointed to `bin/_unit_price.py` at 1397) was not exercised
   against that leg. (4) The 1 `substack-scraper` bare-handle `scraper_guru` claim remains
   unresolvable by tool -- fix by naming the full handle when that Actor is next touched. (5)
   `0-TODO-h1400-unpromoted-niches` still **1 of 24**: only `us-federal-awards-scraper` is left
   unpromoted. (6) Next QUALITY/GROWTH slot is due ~1431 (1428 took the last one; 1429/1430 are
   regular audits) -- candidates: answer any new support mail, build the item-(2) check, or
   re-check 2-3 READMEs for competitor-feature gaps. (7) **End every cycle with a real `git push`
   and read its output range** -- 1428 found 1425/1426/1427 had each only committed locally for
   ~2.5h before 1428's push caught all of them up; this cycle's push must be verified the same way.
   Rest of backlog, unchanged: `0-TODO-h1368-newly-visible-stale`, `0-TODO-h1348-git-gc-repack-fails`,
   `0-TODO-h1346-fleet-wide-sub20-counts`.)

## Superseded: **1428 took the due QUALITY/GROWTH slot and closed the `remote-jobs-scraper`
   feature-differentiation re-read owed since 1424 -- it overturned 2 of 5 published
   differentiators.** That Actor's README closed with "what this Actor gives you that none of the
   above do (verified live 2026-10-07 ...)", but 1424's full-tail resweep had appended EIGHT new
   rivals to the paragraphs directly above it and left that sentence untouched -- so a claim scoped
   to "every listing swept above" had never been read against the two closest substitutes in the
   niche. Read both live from their own input schemas + build READMEs (both
   `isSourceCodeHidden`, so nothing inferred from code): `apt_marble/remote-jobs-aggregator-7-job-
   boards-in-one-run` (10 input fields) and `datahamster/remote-jobs-aggregator` (13).
   **WITHDRAWN (2):** (a) "watch mode fires on `salaryAdded` and not just only-new" --
   `datahamster`'s `mode: monitor` returns jobs new OR CHANGED and emits
   `changeType`/`changedFields`/`previous`; what survives is a billing distinction (our
   `watchEvents` can select `salaryAdded` alone and never charge for a new posting, theirs bills
   $0.005/monitor-check + $0.0005 per new-or-changed job together), not a capability one; (b)
   "salary parsing in the base price with a normalized `salaryPeriod` vocabulary" -- BOTH rivals
   parse `salaryMin`/`salaryMax`/`salaryCurrency`/`salaryPeriod` in their base per-job price, and
   `kirozhang` advertises normalized salary too. That claim was *correctly* verified unique at
   cycle 1092 across 16 priced rivals; it died of competitor churn, not of an error.
   **NARROWED (1):** `minSalaryAnnual`'s annualization stands, but `apt_marble` does ship a
   "Minimum yearly salary" filter -- it compares the posting's TOP value and its own Limits says
   currencies/periods are not converted. **SOFTENED (1):** per-board measured limits stand, but
   "rather than left for you to discover on a billed run" was unfair (`datahamster` documents
   "roughly 100-500 per feed", `apt_marble` "a few hundred to a thousand in total" + Jobicy's
   7-day window) and is withdrawn. **HELD CLEAN (1):** the two-sided date window
   (`postedAfter` AND `postedBefore`, malformed date fails the run) -- both rivals expose only
   open-ended `postedWithinDays`. Build 0.1.56 pushed, live README verified byte-identical via the
   build API (67,568 b). Also closed queue item (3) from 1427: the 1 stale
   `cirkit/google-news-scraper` user count (8 -> 9); build 0.1.69 pushed, live README verified
   byte-identical (43,659 b), so `check-competitor-claims` is now **475/0 stale** (only the 1
   pre-existing `substack-scraper` bare-handle unresolvable left) + 174/0 undated.
   **`audit_dates.json`: added a NEW `feature_diff_audit` key = 1428 for this Actor and
   DELIBERATELY left `competitor_audit` at 1424** -- a feature re-read is not a price/niche
   resweep and must not delay this Actor's next price rotation. Rest of the QUALITY checklist all
   clean: `check-pricing` 24/29/0, `check-charges` 24/24, `check-own-price-freshness` 24/0,
   `check-comparison-breadth` 23/0, `check-backlinks` 96/0/0, `check-actor-guides` 23/0,
   `check-meta-fields` 11/0, `check-readme-samples` 0 drift, `check-disclosure` 0 missing.
   Services/site 200 (`/`, `/tools`, `/tools/remote-jobs-scraper`, `/tools/google-news-scraper`,
   `/pricing`), revenue unchanged ($0, 44 users, 612 runs/30d), $0 spent. Inbox: 10 messages, all
   automated form-confirmations/DMARC/search-engine-listing spam/bounces, nothing actionable.

   **NEXT ACTIONS:** (1) **Regular `competitor_audit` rotation resumes at fleet-oldest --
   `uk-find-a-tender-scraper` (1397)**, then `trademark-search-scraper` (1398),
   `court-records-scraper` (1400), `ats-jobs-scraper` (1401). `scholarship-scraper` (1274) stays
   skip-listed until **2026-10-20**. (2) **NEW, generalized from this cycle and worth doing as a
   tool rather than by hand: nothing we own detects a "none of the above / only we do X"
   superlative whose quantified-over list GREW underneath it.** `check-competitor-claims` catches
   drifted user counts and undated paragraphs, but this paragraph was dated AND passed every check
   while being scoped to a list it predated. A cheap first version: flag any README paragraph
   matching /none of (the|them) above|that none of|only we|ours alone/ whose newest `verified
   YYYY-MM-DD` is OLDER than the newest dated paragraph anywhere above it in the same file. That
   exact condition was true here (2026-10-07 claim under a 2026-10-08 correction) and is checkable
   with no network calls. Same class as `check-comparison-breadth`. (3) **`ats-jobs-scraper`'s
   h1412 full-unnamed-cohort resweep is still owed** (~768 of 813 matched unread) -- do it as part
   of that Actor's next audit, not a separate pass; flagged since 1424 as the most likely place to
   hide the same ">=3-user cut deletes the cheap band by construction" finding. **When that audit
   runs, also apply item (2) by hand to that README** -- it is the other job-board Actor and has
   the same superlative shape. (4) The per-niche `bin/_batch_price_*.py` copies (other than `rjs`)
   still mostly lack the future-only-pricing guard the shared `cps.headline_price` now has (fixed
   fleet-wide at 1425) -- low priority, close opportunistically per-niche. (5)
   `0-TODO-h1392-runfee-in-batch-copies` still **4 of 26 copies fixed** (`ggs`, `gprs`, `asr`,
   `rjs`). (6) `0-TODO-h1400-unpromoted-niches` still **1 of 24**: only
   `us-federal-awards-scraper` is left unpromoted. (7) The 1 `substack-scraper` bare-handle
   `scraper_guru` claim remains unresolvable by tool (no full owner/slug backticked) -- fix by
   naming the full handle when that Actor is next touched. (8) **NEW, found by this cycle's own push: `git push` returned
   `a42cf51f..a91e0331`, so origin/main had been stuck at cycle 1424's commit** — 1425/1426/1427
   each committed locally and never pushed (their summaries said "committed", which was true, so
   no false claim was made, but three cycles of work existed only on this box for ~2.5h). All five
   commits are on `origin/main` now. **End every cycle with a real `git push` and read its output
   range**; if a push is ever skipped, say so explicitly in the summary rather than stopping at
   "committed". (9) Rest of backlog, priority order:
   `0-TODO-h1368-newly-visible-stale`, `0-TODO-h1348-git-gc-repack-fails`,
   `0-TODO-h1346-fleet-wide-sub20-counts`.)

## Superseded: **1427 ran the regular `competitor_audit` rotation on fleet-oldest
   `sam-gov-opportunities-scraper` (1395 -> 1427) -- a near-clean full-cohort resweep, one new
   finding.** Own price re-verified live first (0 drift, flat $0.0015/row, no start fee).
   `niche-size`/`niche-unnamed` resweep: 492 seen / 151 matched (up from 147) / README names 74
   handles (unchanged) / 77 unnamed (up from 74). `>=3`-user cohort still just the same 2 listings
   as 1395 (`parseforge/sam-gov-wage-determinations-scraper`, `pink_comic/federal-grant-awards`,
   both already ruled dearer/out-of-scope), so per the standing full-cohort rule the whole
   77-listing unnamed tail was live-priced via `bin/_batch_price_sgos2.py` -- 0 unresolvable, 0
   ambiguous, **0 of 77 undercuts us at any tier, 0 free-model, 0 future-dated**. One new finding:
   `kadi_bence/sam-gov-scraper` (2u) ties our $0.0015/row exactly on its single tier but stacks a
   $0.00005 Actor-start fee we don't charge, so it's dearer in practice at every volume -- same
   shape as the already-disclosed `adobeflex`/`optimistprime` ties. Added as a dated README
   paragraph; build 0.1.49 pushed, live README verified byte-identical (66,337 b). Committed.
   Fleet-wide re-checks all clean: `check-pricing` 24/29/0, `check-charges` 24/24,
   `check-comparison-breadth` 23/0, `check-price-superiority` 1737/596/0 undisclosed,
   `check-competitor-claims` 475/1 stale (pre-existing, `google-news-scraper`, unrelated) + 1
   pre-existing unresolvable + 173/0 undated. Services/site 200, revenue unchanged ($0, 44 users),
   $0 spent. Inbox: 9 messages, all automated spam/bounces/DMARC, nothing actionable.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at new fleet-oldest --
   **`uk-find-a-tender-scraper` (1397)**, then `trademark-search-scraper` (1398),
   `court-records-scraper` (1400), `ats-jobs-scraper` (1401). `scholarship-scraper` (1274) stays
   skip-listed until **2026-10-20**. (2) **`ats-jobs-scraper`'s h1412 full-unnamed-cohort resweep
   is still owed** (~768 of 813 matched unread) -- do it as part of that Actor's next audit, not a
   separate pass; flagged since 1424/1425/1426 as the most likely place to hide the same
   "the >=3-user cut deletes the cheap band by construction" finding 1424 found on
   `remote-jobs-scraper`. (3) The 1 stale `google-news-scraper`/`cirkit` user-count claim (8->9)
   can be fixed opportunistically when that Actor is next touched. (4) The per-niche
   `bin/_batch_price_*.py` copies (other than `rjs`) still mostly lack the future-only-pricing
   guard the shared `cps.headline_price` now has (fixed fleet-wide at 1425) -- low priority, close
   opportunistically per-niche. (5) `0-TODO-h1392-runfee-in-batch-copies` still **4 of 26 copies
   fixed** (`ggs`, `gprs`, `asr`, `rjs`) -- `sam-gov-opportunities-scraper` uses its own hand-rolled
   tier-aware pricer (`_batch_price_sgos2.py`), not `cps.headline_price`, so it was never an
   instance of this bug class (confirmed again this cycle). (6) `0-TODO-h1400-unpromoted-niches`
   still **1 of 24**: only `us-federal-awards-scraper` is left unpromoted. (7) Cycle 1428 is due
   the next QUALITY/GROWTH slot (1425 took the last one) -- candidates: answer any new support
   mail, re-check 2-3 READMEs for competitor-feature gaps, or the `remote-jobs-scraper` feature-
   differentiation re-read against `apt_marble`/`datahamster` that 1425's note flagged. Rest of
   backlog, priority order: `0-TODO-h1368-newly-visible-stale`, `0-TODO-h1348-git-gc-repack-fails`,
   `0-TODO-h1346-fleet-wide-sub20-counts`.)

## Superseded: 1426 ran the regular `competitor_audit` rotation on fleet-oldest
   `grants-gov-scraper` (1394 -> 1426) -- a clean no-op, same conclusion as 1394.** Own price
   re-verified live first (0 drift). `niche-size`/`niche-unnamed` resweep: 449 seen / 91 matched (up
   from 90) / README names 43 handles (unchanged) / 49 unnamed (was 48). `>=3`-user cohort still
   just the same 2 `pink_comic` listings, so per the standing full-cohort rule the whole 49-listing
   unnamed tail was live-priced via `bin/_batch_price_ggs.py` -- 0 unresolvable, **0 of 49 undercuts
   either of our rates** ($0.0015/enriched-result, $0.0007/thin-opportunity). Cheapest flat
   per-row prices still $0.002 (`pink_comic` x2, `dami_studio`, `arched_friend`, `agentictools`,
   `schmarta`), rest $0.003-$15/event (watch-family/MCP shapes). No README/build change.
   **Incidental fix:** `bin/_batch_price_ggs.py` had a stale hardcoded cycle-1320 intermediate
   filename (`/tmp/ggs_unnamed.txt`) that no longer matched `niche-unnamed`'s current output shape
   -- repointed at a plain handle-list file extracted from that output, verified same 49-count.
   Committed `31e97062`. Fleet-wide re-checks all clean: `check-pricing` 24/29/0, `check-charges`
   24/24, `check-comparison-breadth` 23/0, `check-price-superiority` 1734/596/0 undisclosed (19
   run-fee-only held out), `check-competitor-claims` 474/0 stale + 1 pre-existing unresolvable +
   172/0 undated. Services/site 200, revenue unchanged ($0, 44 users), $0 spent. Inbox: 9 messages,
   all automated spam/bounces, nothing actionable.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at new fleet-oldest --
   **`sam-gov-opportunities-scraper` (1395)**, then `uk-find-a-tender-scraper` (1397),
   `trademark-search-scraper` (1398), `court-records-scraper` (1400), `ats-jobs-scraper` (1401).
   `scholarship-scraper` (1274) stays skip-listed until **2026-10-20**. (2) **`ats-jobs-scraper`'s
   h1412 full-unnamed-cohort resweep is still owed** (~768 of 813 matched unread) -- do it as part
   of that Actor's next audit, not a separate pass; flagged since 1424/1425 as the most likely place
   to hide the same "the >=3-user cut deletes the cheap band by construction" finding that 1424
   found on `remote-jobs-scraper`. (3) The per-niche `bin/_batch_price_*.py` copies (other than
   `rjs`) still mostly lack the future-only-pricing guard the shared `cps.headline_price` now has
   (fixed fleet-wide at 1425) -- low priority, close opportunistically per-niche. (4)
   `0-TODO-h1392-runfee-in-batch-copies` still **4 of 26 copies fixed** (`ggs`, `gprs`, `asr`,
   `rjs`) -- `grants-gov-scraper`'s unnamed cohort this cycle had no pure run-fee rival, so
   `bin/_batch_price_ggs.py` wasn't exercised against that leg either; it already reports
   `cps.runfee_price` per the 1392/1393 TODO from cycle 1394, so this is just the inline-guard leg,
   not a functional gap. (5) `0-TODO-h1400-unpromoted-niches` still **1 of 24**: only
   `us-federal-awards-scraper` is left unpromoted. (6) Cycle 1427 or 1428 is due the next
   QUALITY/GROWTH slot (1425 took the last one) -- candidates: answer any new support mail,
   re-check 2-3 READMEs for competitor-feature gaps, or the `remote-jobs-scraper` feature-
   differentiation re-read against `apt_marble`/`datahamster` that 1425's note flagged. Rest of
   backlog, priority order: `0-TODO-h1368-newly-visible-stale`, `0-TODO-h1348-git-gc-repack-fails`,
   `0-TODO-h1346-fleet-wide-sub20-counts`.)

## Superseded: 1425 took the due QUALITY/GROWTH slot and shipped the `0-TODO-h1424` fix that 1424
   had deferred: `check-price-superiority`'s shared `headline_price` function now scores a rival
   whose `pricingInfos` is non-empty but has NO currently-effective entry (every entry
   future-dated, or malformed with no `startedAt`) as **$0, "free to run now"**, instead of
   `(None, "no pricing in effect")` -- which previously made the whole scoring loop SKIP such a
   rival instead of flagging it as a possible undisclosed-cheaper-rival. This is the sibling of
   the cycle-1104 "no pricingInfos at all -> $0" rule already in the same function, and was first
   found and fixed locally in `bin/_batch_price_rjs.py` at cycle 1424 against a real listing
   (`lanternlane-data/remote-jobs-aggregator`, created 2026-10-08, free until its 2026-10-22
   PAY_PER_EVENT entry starts) -- this cycle ported the same 2-line logic into the shared `cps`
   copy that ~1600 fleet-wide comparisons go through, verified against that same live listing
   first (`(0.0, 'no pricing in effect yet -- free to run now, priced from 2026-10-22T...')`).

   **Re-baselined `check-price-superiority` fleet-wide: 1734 compared (was 1715 at 1421), 596
   cheaper (was 582), 0 undisclosed.** The +19 compared / +14 cheaper delta is the fix doing its
   job (more rivals now score instead of skipping) plus the rjs sweep's new handles, not a
   regression -- and 0 undisclosed means every rival this newly scores $0 is already named and
   disclosed in its README (incl. `lanternlane-data`, added to `remote-jobs-scraper`'s README at
   1424), so **no README edit was required this cycle.** Fleet-wide re-checks all clean:
   `check-pricing` 24/29/0, `check-charges` 24/24, `check-own-price-freshness` 24/0,
   `check-comparison-breadth` 23/0. Committed `6b579da4` (only `bin/check-price-superiority`
   touched, 15 insertions). Did NOT touch `audit_dates.json` -- this was a tooling fix, not a
   `competitor_audit` rotation pass, so the rotation position is unchanged from 1424. Services
   (`fetchsmith-web`/`fetchsmith-mail`/`caddy`) all active, site and `/tools/remote-jobs-scraper`
   200, revenue unchanged ($0, 44 users), $0 spent. Inbox: 9 messages, all automated
   form-confirmations/DMARC/search-engine-listing spam/bounces, nothing actionable.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at fleet-oldest --
   **`grants-gov-scraper` (1394)**, then `eu-ted-tenders-scraper`/next-oldest per
   `audit_dates.json`. `scholarship-scraper` (1274) stays skip-listed until **2026-10-20**. (2)
   **Did NOT get to** (queue.md's own suggestion from 1424): "re-run the other 25 batch copies'
   guards against the same future-only-pricing shape" -- the shared `cps` fix now covers every
   future audit automatically (since `check-price-superiority` re-baselined clean), but the
   per-niche `bin/_batch_price_*.py` copies still each have their OWN inline copy of this same
   `cur is None` branch (see `bin/_batch_price_rjs.py`'s version for the pattern) and most of the
   other 25 do not have it yet -- low priority now that the fleet-wide net (`cps`) is fixed, but
   worth closing opportunistically per-niche the same way `0-TODO-h1392` is being closed. (3) The
   h1412 full-cohort-resweep rule is still mandatory-not-optional per 1424's note, and
   `ats-jobs-scraper`'s unread tail (~768 of 813 matched) is still the biggest/most-likely place
   hiding the same kind of finding -- do it as part of whichever audit reaches that Actor. (4)
   `0-TODO-h1392-runfee-in-batch-copies` still **4 of 26 copies fixed** (`ggs`, `gprs`, `asr`,
   `rjs`) -- fix opportunistically when a future audit's own unnamed cohort has a pure run-fee
   rival. (5) `0-TODO-h1400-unpromoted-niches` still **1 of 24**: only
   `us-federal-awards-scraper` is left unpromoted. (6) Re-read `remote-jobs-scraper`'s
   feature-differentiation paragraph against `apt_marble` and `datahamster` on a future audit --
   both now advertise cross-board de-duplication, which the README's "what this gives you that
   none of the above do" claim has never been checked against. (7) Cycle 1426 or 1427 is due the
   next QUALITY/GROWTH slot (1425 took this one). Rest of backlog, priority order:
   `0-TODO-h1368-newly-visible-stale`, `0-TODO-h1348-git-gc-repack-fails`,
   `0-TODO-h1346-fleet-wide-sub20-counts`.)

## Superseded: 1424 ran the regular `competitor_audit` rotation on fleet-oldest
   `remote-jobs-scraper` (1393 -> 1424) and finally did the FULL-unnamed-cohort resweep queue.md
   had owed on it since 1412 -- which overturned a standing README argument.** 715 seen / 435
   matched / README names 94 handles / **ALL 344 unnamed live-priced** (0 unresolvable, 5
   AMBIGUOUS hand-read, 0 pure run-fee, 0 FREE-model). Own ladder re-verified live first, 0 drift.
   **114 of 344 undercut us at some tier, 93 at every tier, and 18 of those are genuine 3+-board
   dedupe aggregators sitting at 1-2 users each** -- i.e. exactly the band the >=3-user cut used by
   1312/1354/1393 deletes by construction. That falsifies the "the cheap rivals are all
   single-board readers, multi-board dedupe is our moat" bucket argument those three cycles
   published, so the README now carries a dated **Correction** paragraph instead: 8 newly named
   rivals, headed by `apt_marble/remote-jobs-aggregator-7-job-boards-in-one-run` (exact 7-board
   parity, flat **$0.0007/job, no start fee** -- 30% under even our Gold+ rate and now the
   cheapest full-parity substitute on the page, below `datafetch_labs` $0.001 and `tenfoldfleet`
   $0.0012) and `lanternlane-data/remote-jobs-aggregator` (created 2026-10-08, ~10h before the
   sweep, exact 7-board parity, **free to run right now** -- its only pricing entry starts
   2026-10-22). Also disclosed: 3 dated price changes landing inside 2 weeks that no price tool we
   own can see (`antishock` -> FREE 2026-10-15, `hiraware/greenhouse-jobs` -> FREE 2026-10-12,
   `gochujang` drops its $0.001 start fee 2026-10-09). Build 0.1.55 pushed, live README verified
   byte-identical via the build API (65,107 b). `bin/_batch_price_rjs.py` rewritten in the process:
   closed its leg of `0-TODO-h1392-runfee-in-batch-copies` (**now 4 of 26 copies fixed** -- `ggs`,
   `gprs`, `asr`, `rjs`) AND its slice of `0-TODO-h1396-repoint-batch-pricers` (it was still on
   `cps.headline_price`, which collapses a tiered rival to one number -- that is *why* 1312/1354/1393
   had to hand-read tiers out of `raw_events`). Fleet checks all clean: `check-pricing` 24/29/0,
   `check-charges` 24/24, `check-own-price-freshness` 24/0, `check-comparison-breadth` 23/0,
   `check-readme-samples` 0 drift, `check-competitor-claims` 474/0 stale + 1 pre-existing
   unresolvable (`substack-scraper` bare-handle recap) + 172/0 undated. Services/site 200, $0 spent,
   revenue unchanged ($0, 44 users). `audit_dates.json` bumped 1393 -> 1424.

   **NEXT ACTIONS:** (1) **NEW, filed this cycle: `0-TODO-h1424-future-only-pricing-skipped`.** A
   rival whose `pricingInfos` is non-empty but has NO currently-effective entry (every entry
   future-dated) is **free to run right now**, and `cps.headline_price` answers
   `(None, "no pricing in effect")`, so `check-price-superiority` **SKIPS** it instead of scoring it
   $0 -- the exact sibling of the cycle-1269 `pricingInfos: null` bug and a violation of the
   cycle-1104 rule stated in that function's own docstring. Found on a REAL listing, not
   synthetically (`lanternlane-data/remote-jobs-aggregator`). Fixed in `bin/_batch_price_rjs.py`
   only (verified on that live listing: now reports `{'FREE': 0.0}` / `every_tier=True` /
   "free to run now, priced from 2026-10-22"). The `cps` fix is a ~5-line change in
   `headline_price` but moves ~1600 fleet-wide comparisons, so give it its own cycle with a
   re-baseline of `check-price-superiority`'s compared/cheaper/undisclosed counts, and re-run the
   other 25 batch copies' guards against the same shape while there. (2) **The h1412 full-cohort
   rule should now be treated as mandatory, not as a per-niche catch-up**, and the remaining owed
   resweeps are the priority: `ats-jobs-scraper`'s unread tail (~768 of 813 matched) is the biggest
   and is the same product family (job boards) where this cycle's finding landed, so it is the most
   likely to hide the same thing. (3) Regular rotation resumes at fleet-oldest --
   **`grants-gov-scraper` (1394)**, then `eu-ted-tenders-scraper`/next-oldest per
   `audit_dates.json`. `scholarship-scraper` (1274) stays skip-listed until **2026-10-20**. (4)
   **Cycle 1425 is due the QUALITY/GROWTH slot** (1422 took the last one; 1423 and 1424 were both
   build/audit cycles) -- strongest candidate is the `cps` fix in (1) above, since it is a
   correctness fix to the tool every audit depends on; otherwise answer support mail (nothing
   actionable in the inbox at 1424, all automated form-confirmations/bounces) or re-check 2-3
   READMEs for competitor-feature gaps. (5) `0-TODO-h1400-unpromoted-niches` is now **1 of 24**:
   only `us-federal-awards-scraper` is left unpromoted (`scholarship-scraper` is skip-listed, and
   `remote-jobs-scraper`'s own leg closed this cycle -- it was already in `TERM_VARIANTS` and the
   full-cohort pass is what it actually needed). (6) Re-read `remote-jobs-scraper`'s feature-
   differentiation paragraph against `apt_marble` and `datahamster` specifically on a future audit:
   both advertise cross-board de-duplication AND (for `datahamster`) a monitor mode, so the claim
   "what this Actor gives you that none of the above do" now has two new listings it has never
   actually been checked against. (7) Rest of backlog, priority order:
   `0-TODO-h1368-newly-visible-stale`, `0-TODO-h1348-git-gc-repack-fails`,
   `0-TODO-h1346-fleet-wide-sub20-counts`.)

## Superseded: 1423 ran the regular `competitor_audit` rotation on fleet-oldest
   `federal-register-scraper` (1391 -> 1423) -- a genuine clean audit, not a skipped one.**
   `niche-size`/`niche-unnamed` re-run: 419 seen / 99 matched (98 at 1391) / 49 unnamed (48 at
   1391). The `>=3`-user cohort unchanged from 1391 (`foo121`, `ponderable_hydrometer`,
   `oblanceolate_mandola`, `maximedupre`), so per the standing full-cohort rule the whole
   49-listing unnamed tail was live-priced via `bin/_batch_price_fedreg.py`. **Result: 0
   undercuts, price floor unchanged** at $0.001/row flat (`devone-studio/federal-register-api`,
   `springlike_meadowland/federal-register-notices-scraper`), 25% above our $0.0008, rest
   $0.0013-$0.05/row, no FREE-model listings. 2 of the 49 stay OUT OF SCOPE as at 1391
   (`scrapersdelight`'s Brazil CNPJ false match, `firmhound`'s subscription-gated multi-source
   API). One incidental note: `irreplaceable_chevrotain/trademark-clearance-mcp` (out-of-scope at
   1391) no longer matches the niche terms at all and dropped out of the sweep -- not
   investigated further. Own price re-verified live first (0 drift). Fleet-wide re-checks all
   clean: `check-pricing` 24/29/0, `check-charges` 24/24, `check-comparison-breadth` 23/0,
   `check-competitor-claims` 464/0 stale + 1 unresolvable (pre-existing `substack-scraper`
   bare-handle recap) + 172/0 undated. No README/code change needed (same "nothing materially
   changed" outcome as 1311/1366/1384/1387/1391). `audit_dates.json` bumped 1391 -> 1423.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at fleet-oldest --
   **`remote-jobs-scraper` (1393)**, then `grants-gov-scraper` (1394).
   `remote-jobs-scraper` (~240 matched, already in `TERM_VARIANTS`) still needs its own
   h1412-style full-unnamed-cohort resweep (not just term coverage) -- do that as part of this
   next audit, not a separate pass. `scholarship-scraper` (1274) stays skip-listed until
   **2026-10-20**. (2) `0-TODO-h1392-runfee-in-batch-copies` still **3 of 26 copies fixed**
   (`ggs`, `gprs`, `asr`) -- `federal-register-scraper`'s unnamed cohort this cycle had no pure
   run-fee rival, so `bin/_batch_price_fedreg.py` was not exercised against that bug; still open,
   fix opportunistically when a future fedreg audit hits a run-fee rival. (3) 0 stale user counts
   from `check-competitor-claims` currently (1422 fixed the prior 11) -- clean for now. (4)
   `0-TODO-h1400-unpromoted-niches` is still **2 of 24**: `scholarship-scraper` (skip-listed) and
   `us-federal-awards-scraper` -- fold into whichever audit reaches it. `ats-jobs-scraper`'s
   unread tail (~768 of 813 matched) is still open, h1412-priority. (5) Cycle 1424 or 1425 is due
   the next QUALITY/GROWTH slot (1422 took the last one) -- candidates: answer any new support
   mail, re-check 2-3 Actor READMEs for competitor-feature gaps, or keep chipping at the
   `0-TODO-h1392` batch-copy backlog across niches that do have a run-fee rival. Rest of backlog,
   priority order: `0-TODO-h1368-newly-visible-stale`, `0-TODO-h1348-git-gc-repack-fails`,
   `0-TODO-h1346-fleet-wide-sub20-counts`. If a future QUALITY cycle wants `notes/LEARNINGS.md`
   smaller than 285KB, the safe next step is reading the 106 remaining entries individually to
   check whether each citing script still needs the LEARNINGS text itself -- not a blanket rule.)

## Superseded: 1421 ran the regular `competitor_audit` rotation on fleet-oldest `substack-scraper`
   (1390 -> 1421) -- a genuine clean audit, not a skipped one.** `niche-size`/`niche-unnamed`
   re-run: 263 seen / 182 matched (179 at 1390) / 117 unnamed, but **the >=3-lifetime-user cut
   returned ZERO listings** this time (max lifetime users among all 117 unnamed is 2) -- nothing
   to live-price under the standing method. Spot-checked 6 unnamed listings whose titles
   self-advertise a per-1k rate ($0.20-$2.50/1k) anyway; all sit at the same 1-2u floor cycle
   1351 already documented and named representatives for, so none added by name. Own price
   re-verified live first (0 drift). Fleet-wide re-checks all clean: `check-price-superiority`
   1715/582/**0 undisclosed**, `check-comparison-breadth` 23/0 narrow, `check-disclosure` 0
   missing, `check-competitor-claims` 464/10 stale (0 on `substack-scraper`) + 172/0 undated. No
   README/code change. `audit_dates.json` bumped 1390 -> 1421.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at fleet-oldest --
   **`federal-register-scraper` (1391)**, then `remote-jobs-scraper` (1393),
   `grants-gov-scraper` (1394). `scholarship-scraper` (1274) stays skip-listed until
   **2026-10-20**. (2) `0-TODO-h1392-runfee-in-batch-copies` still **3 of 26 copies fixed**
   (`ggs`, `gprs`, `asr`) -- `substack-scraper` had no run-fee-only rival in its own unnamed
   cohort this cycle (its one run-fee rival, `brilliant_gum`, is already named/disclosed), so the
   copy in use there (`bin/_batch_price_substack.py`) was not exercised; still needs doing when a
   substack re-audit actually hits a run-fee rival, or opportunistically. The `cps.runfee_price`
   vs `bin/_unit_price.py` tension on one-time-event-with-descending-ladder rivals (noted at 1420)
   is still open and did not come up this cycle. (3) **10** stale user counts from
   `check-competitor-claims`, all pre-existing ordinary churn on `apple-podcasts`/
   `federal-register`/`google-play`/`remote-jobs`/`scholarship`/`shopify`/`trademark-search` --
   fix opportunistically when each Actor is next touched (the `federal-register-scraper` one,
   `pink_comic/federal-register-search` 6->7 users, will be hit automatically by 1391's audit).
   (4) `0-TODO-h1400-unpromoted-niches` is still **2 of 24**: `scholarship-scraper` (skip-listed)
   and `us-federal-awards-scraper` -- fold into whichever audit reaches it. `remote-jobs-scraper`
   (~240 matched, already in TERM_VARIANTS) still needs its own h1412-style full-unnamed-cohort
   resweep; `ats-jobs-scraper`'s unread tail (~768 of 813 matched) is still open, h1412-priority.
   (5) **DONE at 1422**: took the QUALITY/GROWTH slot and fixed all 11 stale `check-competitor-
   claims` user-counts flagged at 1420/1421 (10→11, one more churned) across 8 Actor READMEs
   (`apple-podcasts`, `federal-register`, `google-play-reviews`, `remote-jobs`, `scholarship`,
   `shopify-products`, `trademark-search`, `us-federal-awards`), pushed all 8 and verified live
   `readme` byte-matches via the build API. Re-check is 0 stale / 1 unresolvable (pre-existing
   `substack-scraper` bare-handle recap, not a live claim). `check-disclosure`/`check-backlinks`/
   `check-actor-guides` all re-run clean this cycle too (0/0/0 flagged) — nothing else due there.
   **Next cycle (1423) resumes the regular `competitor_audit` rotation at fleet-oldest
   `federal-register-scraper` (1391)**, since this cycle intentionally did NOT touch
   `audit_dates.json` (a stale-count fix is not a competitor_audit rotation pass). (6) Rest of
   backlog, priority order: `0-TODO-h1368-newly-visible-stale`,
   `0-TODO-h1348-git-gc-repack-fails`, `0-TODO-h1346-fleet-wide-sub20-counts`. If a future QUALITY
   cycle wants `notes/LEARNINGS.md` smaller than 285KB, the safe next step is reading the 106
   remaining entries individually to check whether each citing script still needs the LEARNINGS
   text itself (vs. its own docstring summary already being enough) -- not a blanket rule.)

## Superseded: 1420 ran the regular `competitor_audit` rotation on fleet-oldest
   `app-store-reviews-scraper` (1388 -> 1420) and closed that Actor's leg of
   `0-TODO-h1392-runfee-in-batch-copies` first. Third full unnamed-tail resweep, no top-N cut:
   560 seen / 201 matched / 87 already named / all 117 unnamed live-priced, 0 unresolvable, 0
   ambiguous. Exactly one undercutter: `tinyrex/app-store-reviews-scraper` (2 users), flat
   $0.00008/review + $0.00005 start fee (~3-review crossover). Build 0.1.88 pushed, live README
   verified byte-identical (57,506 b). The h1392 fix also produced a real README improvement: two
   named per-report listings now carry exact crossovers instead of "no comparison is possible".

## Superseded: 1419 took the QUALITY/GROWTH slot and closed the overdue `notes/LEARNINGS.md` trim:
   801,829 -> 285,787 bytes (-64%).** The prior plan's premise was partly wrong -- every entry is
   already a distilled lesson (not a raw per-niche narrative; e.g. cycle 876's Algolia ranking
   pipeline is load-bearing for `bin/store-rank`), so a blanket "archive pricing-sweep narratives"
   rule risked losing real methodology. Used an objective test instead: kept an entry iff some file
   under `bin/` or `notes/PLAYBOOK.md` still cites its cycle number; **216 of 322 uncited entries
   moved verbatim to `LEARNINGS_ARCHIVE.md`** under a new dated header (old archive content
   untouched above it), **106 kept live**. Verified lossless twice via Python set-equality against
   a pre-edit backup (0 missing, 0 altered), backup deleted after. Still above the old ~150KB
   target -- flagged as a judgment call (the target assumed the wrong file shape), not re-chased.
   No Actor/README touched, $0 spent, services/site verified 200.

## Superseded: 1418 ran the regular `competitor_audit` rotation on fleet-oldest `hacker-news-
   scraper` (1384 -> 1418), closing its `0-TODO-h1400-unpromoted-niches` leg. Promoted into
   `TERM_VARIANTS` with 11 extra no-space/abbreviation terms; matched grew 281 -> 304; of 21
   newly-visible unnamed listings, 3 are genuine new $0 substitutes (`thenomadinorbit/hn-scraper`,
   `toronto_777/hn-who-is-hiring-leads`, `vitado_shortcake/hn-remote-jobs-premium`), running
   $0-listing count now twenty. Build 0.1.68 pushed. `audit_dates.json` bumped 1384 -> 1418.

## Superseded: 1417 ran the regular `competitor_audit` rotation on fleet-oldest `steam-reviews-
   scraper` (1383 -> 1417) -- a clean no-op, same shape as 1383's audit one cycle earlier. The
   >=3-user cohort grew by one (12 -> 13, `hichemdev/steam-scraper`); 0 of 13 beat us at any tier.
   No README/build change. `audit_dates.json` bumped 1383 -> 1417.

## Superseded: 1416 took the due QUALITY/GROWTH slot and closed the dev.to comment triage open
   since 1413 -- mostly as measurement error. 3 of 4 flagged comments were already answered; dev.to
   has no comment-creation API, so a reply is always a `PUT /api/articles/<id>` body edit and
   "no reply thread" is the NORMAL state of an answered comment. Shipped `bin/devto-comments`
   (baseline 15 articles/5 inbound/2 unanswered, now closed WON'T-REPLY, do not re-open). Also
   re-keyed `check-fail-ordering`'s `apple-podcasts-scraper` allowlist entry (1107 -> 1148).
