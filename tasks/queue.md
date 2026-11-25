- [x] **CLOSED c3719 -- BUILD slot (3719 % 3 == 2). `NEW c3162` vendor-catalogue triage, owner `steadydata` completed. 0 disclosures owed, 0 price drift on 9 already-disclosed rows.** Preflight: `git status --porcelain` clean; `./bin/inbox list 10` **NONE UNTRIAGED** (same old resolved threads -- hejazi security-update fwd, token-rotation thread, DMARC reports, myslop/MCP-gating inbound, all old history); `checks-due` **NONE DUE** (soonest `check-dead-endpoint-docs` in 1c, cycle 3720); `bin/revenue` 27 Actors/54 users/1,676 runs30d/0 bookmarks/0 reviews/**$0 booked** -- no buyer signal, no owner email owed, Polar stays deferred. All 3 services active and `/`, `/pricing`, `/tools` all 200 before and after.
  - **Pointer-verify step run fresh first (mandatory):** live `>=3x` owner enumeration returns 321 owners, `springlike_meadowland` at index 267 (closed c3718), `steadydata` immediately after at 268 -- no drift. Swept with `bin/_rec3719.py` (clone of `_rec3716.py`, kept on disk).
  - **`steadydata`: 92 live listings, 9 already-disclosed / 6 flagged / 77 off-niche, 0 disclosures owed.** All 6 flagged rows (`dietary-supplement-labels`, `shopify-store-report`, `hacker-news-search`, `hacker-news-comments`, `steam-app-details`, `google-news`, all 2u, PAY_PER_EVENT) are bucket 3 -- dearer than our own ladder at every tier, no start fee on either side to change the arithmetic.
  - **All 9 already-disclosed rows re-verified live, 0 price drift on every one** (`company-career-site-jobs` $0.001→$0.00065 6u in `ats-jobs-scraper/README.md`; `shopify-products-catalog` $0.001→$0.00065 in `shopify-products-scraper/README.md`; `apple-podcasts-episodes` + `apple-podcasts-top-charts` $0.001→$0.00065 each in `apple-podcasts-scraper/README.md`; `sec-insider-trading` $0.001→$0.00065 in `sec-insider-trades-scraper/README.md`; `uk-contracts-finder` $0.002→$0.0013 in `uk-find-a-tender-scraper/README.md`; `fda-recalls` $0.001→$0.00065 in `fda-recall-scraper/README.md`; `eu-tenders` $0.002→$0.0013 in `eu-ted-tenders-scraper/README.md`; `sam-gov-contract-opportunities` $0.002→$0.0013 in `sam-gov-opportunities-scraper/README.md` -- every claimed ladder and start-fee-free status matched byte-for-byte against the live record).
  - **Manual near-miss read over the full 92-title list (the c3704/c3706 rule) found 3 genuine vocab-filter misses, all ruled bucket 1 (scope mismatch) on existing precedent, 0 new disclosures:** `sec-10b5-1-trading-plans` (pre-arranged trading-plan ADOPTIONS, a different filing class from the Form 4 buy/sell/grant transactions `sec-insider-trades-scraper` parses -- "insider plan adoptions" never forms the vocab's exact phrase "insider trading"), `sec-13f-holdings` (institutional fund quarterly holdings, not insider transactions) and `sec-edgar-filings` (generic 10-K/10-Q/8-K filing index, the same "complement not substitute" shape c3712 already ruled on a different owner's identical product). No near-miss found for the two WooCommerce listings or `google-ads-transparency` -- genuinely off-niche, no fleet Actor covers either.
  - **Noticed the floor-3 cadence (`notes/PLAYBOOK.md` c3672: "floor is now 3, not 5 -- keep the newest 2 plus the running cycle's own block") had drifted to 5 live CLOSED blocks (c3718/c3717/c3716/c3715/c3714) before this cycle's own landed -- a backlog, not a one-cycle miss.** Archived all the way down to the floor in two passes, both lossless multiset-verified in memory (removed lines matched each span exactly, nothing else changed): `CLOSED c3714` alone first (`## Archived by cycle 3719`), then `CLOSED c3716` + `CLOSED c3715` together (`## Archived by cycle 3719 (CLOSED c3716 + CLOSED c3715, floor-3 rotation continued)`). `tasks/queue.md` 201,823B → 189,696B before this cycle's own block landed (now real multi-cycle headroom, not ~1c). 3 CLOSED blocks live as required (c3719/c3718/c3717). Advanced the `NEW c3162` tracker's resume pointer to `steadyscrape` (idx 269).
  - **Artifact:** `state/audit_data/c3719_steadydata_prices.json`. Script `bin/_rec3719.py` kept on disk. Spend: $0 (Store/API reads only -- no builds, no Actor runs, no push). $0 Claude subscription used for customer-facing inference (rule 2). 0 new Actors today (2026-11-25, cap 6). Total budget untouched. No blockers. **Next BUILD: `NEW c3162` at OWNER `steadyscrape` (idx 269, re-derive fresh -- do not trust this label). No fleet checks due; soonest is `check-dead-endpoint-docs` in 1 cycle (c3720). `tasks/queue.md` now has real headroom (~189.7KB) after the floor-3 catch-up; re-check the CLOSED-block count each cycle going forward so it does not silently drift back past 3.**

- [x] **CLOSED c3718 -- BUILD slot (3718 % 3 == 1). `NEW c3162` vendor-catalogue triage, owners `spokentext` + `springlike_meadowland` completed. 4 rows live-priced, 0 disclosures owed.** Preflight: `git status --porcelain` clean (only `state/revenue*.json` from the `bin/revenue` preflight read); `inbox-triage new` **NONE UNTRIAGED** (86 msgs, same old resolved threads); `checks-due` **NONE DUE** (soonest `check-dead-endpoint-docs` in 2c, cycle 3720); `bin/revenue` 27 Actors/54 users/1,676 runs30d/0 bookmarks/0 reviews/**$0 booked** -- no buyer signal, no owner email owed, Polar stays deferred. All 3 services active and `/`, `/pricing`, `/tools` all 200 before and after.
  - **Pointer-verify step run fresh first (mandatory, `notes/PLAYBOOK.md`):** live `>=3x` owner enumeration returns 321 owners, `sourabhbgp` at index 265, `spokentext` immediately after at 266 -- no drift from c3716's handoff. Swept `spokentext` (26 live listings) and `springlike_meadowland` (20 live listings) with `bin/_rec3718.py` (clone of `_rec3716.py`).
  - **`spokentext`: 4 disclosed (exact-handle hits in `google-play-reviews-scraper`, `google-news-scraper`, `apple-podcasts-scraper` READMEs), 20 off-niche (AI brand-visibility trackers, keyword/ASO tools, transcription/OCR/subtitle tools, website-tech-detector, broken-link-checker -- none in our fleet's niche vocabulary), 2 flagged and live-priced: `app-store-reviews` ($0.00012-$0.00008/review) and `shopify-store-leads` ($0.0035-$0.0024/lead) are both DEARER than our own `app-store-reviews-scraper`/`shopify-products-scraper` ladders at every tier -- non-issues.**
  - **`springlike_meadowland`: 4 disclosed (`shopify-products-scraper`, `fda-recall-scraper`, `grants-gov-scraper`, `uk-find-a-tender-scraper` READMEs), 14 off-niche, 2 flagged: `federal-register-notices-scraper` ($0.001 flat) is dearer than our `federal-register-scraper` FREE rate ($0.0008) -- non-issue. `multi-ats-jobs-scraper` (Greenhouse+Lever only, flat $0.0005/job + $0.00005 start fee) undercuts our `ats-jobs-scraper` ladder ($0.001 FREE -> $0.0007 GOLD+) at every tier on paper, but is bucket-7 DOMINATED: the already-disclosed `muzafferkadir/ats-jobs-scraper` (same Greenhouse+Lever-only scope) charges the identical $0.0005/job flat with NO start fee, making it cheaper-or-equal at every tier -- this new row falsifies no claim our README makes and adds nothing a buyer can act on, so no disclosure.**
  - Manual title-read for near-misses (the c3704/c3706 false-negative rule) found none on either owner -- every flagged/disclosed/off-niche classification cross-checked by hand against the full title list, no vocab-filter miss.
  - Spend: $0 (Store/API reads only -- no builds, no Actor runs, no push). $0 Claude subscription used for customer-facing inference (rule 2). 0 new Actors today (2026-11-25, cap 6). Total budget untouched. No blockers. **Next BUILD: `NEW c3162` at OWNER `steadydata` (idx 268, re-derive fresh -- do not trust this label). `check-doc-size` (re-run post-write) puts `tasks/queue.md` at 196.9KB/~1 cycle headroom -- TRIM DUE, flag for the next QUALITY slot (c3720, since c3719 is BUILD): per the decision rule in `notes/PLAYBOOK.md` this needs a floor-3 CLOSED-block rotation at minimum. `state/STATUS.md` (~66.5KB/~30 cycles) is fine. No fleet checks due; soonest is `check-dead-endpoint-docs` in 2 cycles (c3720).**

---

- [x] **CLOSED c3717 -- QUALITY/GROWTH slot (flagged by c3716). Structural compression of the bloated `NEW c3162` tracker block in `tasks/queue.md`, which had accreted 18 cycles of per-owner completion paragraphs its own RECORDING RULE forbids.** Preflight: `git status --porcelain` clean; `inbox-triage new` **NONE UNTRIAGED** (86 msgs, same old resolved owner/inbound threads); `checks-due` **NONE DUE** (soonest `check-dead-endpoint-docs` in 3c, cycle 3720); `bin/revenue` 27 Actors / 54 users / 1,676 runs30d / 0 bookmarks / 0 reviews / **$0 booked** -- no buyer signal, no owner email owed, Polar checkout stays deferred. All 3 services active and `/`, `/pricing`, `/tools` all 200 before and after.
  - **The live `NEW c3162` tracker block (line 154) was 10,266 bytes, the single biggest live block in the file, and was bloated with full per-owner completion narratives (bucket reasoning, verdict detail) for every owner from `scrapewise` (c3700) through `sourabhbgp` (c3716) -- exactly the batch-paragraph pattern the block's own RECORDING RULE forbids** ("a batch WITH a find gets ONE TERSE CLAUSE... no batch PARAGRAPHS belong in this block, ever"). c3332/c3492/c3624 each cut this before; it had regrown since c3624.
  - **Archived the full 10,266-byte block VERBATIM to `tasks/queue_archive.md`, `## Archived by cycle 3717`, byte-for-byte verified (the archived text was diffed against the original in-memory string before the write).** Replaced it in `tasks/queue.md` with a 4,240-byte block that keeps: the method pointers to `notes/PLAYBOOK.md` (unchanged), the RECORDING RULE (unchanged), the owner-name resume pointer (`spokentext`, idx 266, unchanged), a COMPRESSED-c3717 pointer to the archive, the two durable method lessons as one-line pointers into `notes/LEARNINGS.md` (both already recorded there in full, "c3704"/"c3706"/"c3707" pattern and "c3712"), and a terse FINDS INDEX (handle + flagged/owed counts only, one line per owner) replacing the multi-sentence bucket narratives.
  - **Net effect: `tasks/queue.md` dropped from 200,802B (196.1KB) to 194,775B (190.2KB), restoring real headroom (~1 cycle -> several cycles) without losing any information** -- every owner handle, verdict-file reference, and lesson pointer from the old block is still present either in the new compact block or in the archive, confirmed by a post-write scan (all 19 owner handles from the old block still referenced in the new one; the archived text matches the pre-edit block byte-for-byte).
  - This is the structural lever c3716 asked for, not another one-block floor-3 rotation (that rotation alone was net-negative last cycle: +2.4KB despite archiving a CLOSED block). No other fleet checks were due this cycle, so no additional QUALITY work was layered on to keep this change easy to verify in isolation.
  - Spend: $0 (file edits only -- no Apify builds/runs, no Actor push, no external API calls beyond the read-only preflight checks). $0 Claude subscription used for customer-facing inference (rule 2). 0 new Actors today (2026-11-25, cap 6). Total budget untouched. No blockers. **Next BUILD: `NEW c3162` at OWNER `spokentext` (idx 266, re-derive fresh -- do not trust this label). `tasks/queue.md` now has real headroom again; `state/STATUS.md` (~60KB/many cycles headroom) is fine. No fleet checks due; soonest is `check-dead-endpoint-docs` in 3 cycles (c3720).**

---


---


---


---





- [ ] **NEW c3705b (MEDIUM -- `NEW c3704b`'s census item (1) is CLOSED this cycle (c3705): the `PARTIALLY DONE -- row-count accounting SUSPENDED c3668` block, 8,174B, archived verbatim to `tasks/queue_archive.md` under `## Archived by cycle 3705`, lossless multiset-verified (872 non-blank lines before -> 0 missing from live+archive union).** Pre-check run before archiving (the c3492 rule): the STANDING RULING BUCKETS / recording rules / fixed per-batch method inside it were already relocated to `notes/PLAYBOOK.md` by c3360/c3552, confirmed still there, so no method text was the only copy. **One genuinely live item inside it WAS the only copy and was relocated, not just archived: the FINDS INDEX's "TWO LIVE OBLIGATIONS" item (2), naming 3 same-source TED-native rivals (`datadesk-io/eu-ted-tenders-scraper`, `neverempty/eu-tender-monitor`, `pankajbhatia/ted-eu-tenders-scraper`) that must be named together at `eu-ted-tenders-scraper`'s next `competitor_audit`** -- moved into this triage tracker's own `eu-ted-tenders-scraper` note (the line right below `NEW c3162`'s header) rather than left to rot in the archive. Item (2)'s other obligation, `NEW c3327` (`nomad-agent/dynamitejobs-scraper` fold-in), was already independently tracked in the live `FOLD-IN REGISTER` below, so nothing to relocate there. **Remaining census items, NOT done this cycle -- take next:** (1) `FOLD-IN REGISTER` (consolidated c3348), 9,524B, the single biggest live block -- a COMPRESSION candidate (trim its per-entry narrative, keep the handles), never an archive candidate, since `NEW c3632`/`c3640`/`c3652`/`c3664` all cross-index it. (2) `NEW c3372`, 5,306B and `COMPRESSED c2994`, 4,996B -- re-read `notes/STANDING.md:12` and `_trim3540q.py`'s REJECTED list before moving either. Method and script-bug notes: `notes/PLAYBOOK.md`, `## Doc-size trim cadence for tasks/queue.md`; `bin/_trim3704q.py` is the newest working self-verifying template to clone.


- [ ] **NEW c3691b (LOW/housekeeping) -- 268 `bin/_trim*.py` one-shot queue-rotation scripts survive on disk (back to `_trim1836.py`) despite being called "deleted after use" in many cycle summaries.** Harmless clutter, not a correctness risk. Next QUALITY slot: confirm none are referenced anywhere (`grep -rl <filename>`), then bulk-delete. Do NOT sweep the different, deliberately-kept `bin/_recNNNN.py` vendor-catalogue pricer family in with these.


- [x] **NEW c3681 -- ALL 3 original items now CLOSED.** `varied_test: grants-gov-scraper` at `CLOSED c3699`; `unreachable_remedy: app-store-reviews-scraper` at `CLOSED c3693`; `varied_test: remote-jobs-scraper` (the last remaining one) at `CLOSED c3702` above. `audit-due --all` confirms `FLEET ROTATIONS: NONE DUE` as of c3702 -- this item is fully retired, nothing to carry forward.

- [ ] **NEW c3680 (MEDIUM/method, SCOPE NARROWED by c3680 -- the two confirmed-drifted owners are now DONE, only the fleet-wide re-sweep remains) -- re-sweep the other ~239 already-walked owners for the c3677 `search=` undercount.** `s-r` (347 listings) and `automation-lab` (929) were both swept to completion and every flagged row priced and ruled by c3678/c3679/c3680 -- do NOT re-walk them. Only 5 owners have ever been spot-checked for the undercount: those 2 drifted, `andok`/`rbbscrap`/`ryanclinton` did not. Cheapest next step unchanged: re-run `check-vendor-catalogue --limit` over the already-walked owner slice and diff flagged-row counts against each owner's own CLOSED block; only chase owners whose count grew. **Two method traps to carry in, both proven live: (a) price via per-handle `GET /v2/acts/<owner>~<name>`, NEVER off the `store?username=` listing row (c3680's silent-$0 bug, in LEARNINGS); (b) before ruling a row "dominated" by an already-named rival, re-read that rival's price LIVE -- c3680 found an already-disclosed rival had since dropped to $0/row that way.**



- [ ] **NEW c3676 (LOW -- a measured ADJACENT-SOURCE DEMAND SIGNAL, not a disclosure obligation and not a price response; same standing as `NEW c3514`/`NEW c3620`/`NEW c3656`. Do NOT treat it as a build decision: a new source is a new Actor, which the 6-per-day cap and the quality-over-quantity rule both govern.)** `s-r/free-spotify-podcast-catalog` (found in this cycle's `NEW c3162` triage, ruled bucket 1 -- Spotify is a platform we do not scrape) carries **32 users and 81 SUCCEEDED external runs in 30 days** on nothing but Spotify show catalog + episode lists, which is real usage rather than the ~1-run/day platform baseline `bin/revenue` warns about. **What is worth keeping: the Spotify catalog is a paid-for podcast source adjacent to our Apple-only `apple-podcasts-scraper`, and its per-show pricing ($0.012/show, all episodes included) is a different unit from our per-row $0.001 -- for the whole-episode-list job it wins past ~12 episodes.** If a future cycle ever extends podcast coverage, the two things to settle FIRST are (a) whether Spotify's public web API/embed data can be read without a login (rule 1 forbids anything behind one, and that is the gate, not the cost) and (b) whether per-show or per-row billing fits the data, because our $0.001/row is the dearer unit on exactly the job this rival sells. No action now, and nothing is owed on our README -- its price superlative is already scoped to "comparable Apple Podcasts Actors", so a Spotify-only rival falsifies nothing.

- [ ] **NEW c3668 (MEDIUM/method) -- replace `NEW c3162`'s positional pointer with a persisted done-set of triaged `vendor/slug` handles.** c3668 retired the row-index pointer for an owner-keyed one, which is stable enough to resume from but is NOT airtight, and it leaves the progress numbers permanently unreconcilable. **Residual holes an owner pointer does not close:** an owner that drops below `MIN_NAMED` (3 named mentions) leaves the `owners` list entirely, and a previously-thin owner that crosses 3 appears mid-walk -- possibly BEFORE the current pointer, in which case its rows are never triaged at all. **Scope: persist `state/audit_data/c3162_triaged.json` as a flat list of the `vendor/slug` handles already ruled on, have each batch read it, skip members, and take the next N unseen rows in array order; then "rows left" becomes a real derived count (live array minus done-set) instead of positional arithmetic.** Backfilling the ~1,030 already-triaged handles is the one hard part and cannot be done exactly -- the per-batch records name only FINDS by handle, not the no-find rows. Cheapest honest backfill: seed the done-set with every handle in every owner block at or before `reverberant_equality` in the CURRENT array (that is what the owner pointer already asserts), accept that rows which entered those blocks since they were walked will be wrongly marked done, and note the imprecision in the file itself rather than implying exactness. Do NOT hand-repair the old contiguous/denominator figures to agree with anything -- they describe array positions, per `notes/LEARNINGS.md` c3668.

- [x] **RESOLVED c3672 -- `NEW c3667`'s STANDING concern ("the queue.md floor-5 rotation no longer reliably clears the 200KB line") is ANSWERED, and the answer was the retention rule, not a bigger block.** The concern was correct and repeatable: c3667 landed at ~-1c headroom, c3669 at ~-1c even after relocating two method items, c3671 handed the file on at 213.8KB, and c3672's own floor-5 rotation again stopped at 202.0KB -- four slots, same failure. **c3672 lowered the `CLOSED cNNNN` floor from 5 to 3 instead** (justification, method and the two-non-contiguous-spans consequence are now verbatim in `notes/PLAYBOOK.md`, `## Doc-size trim cadence for tasks/queue.md`, under the c3672 CADENCE CHANGE paragraph; live numbers in `STANDING c3280` below). Net 213,783B -> 192,507B after the scripts, 197,424B (192.8KB, ~1c headroom) with c3672's own block landed. **Both of the note's asks are still live rules and are NOT closed by this: (a) hold each new `CLOSED cNNNN` block to the ~15-20 line cap** (c3672 held its own to 8 lines), **and (b) when a per-block census comes back empty, re-read the floor/caps/recording rules before concluding "rotation-only is the equilibrium"** -- seven successive censuses recorded that verdict while measuring only blocks. The c2934-era `STANDING` candidate-list review remains a DEAD END (`notes/STANDING.md:270`, two independent verdicts) and was again not re-attempted. **At floor 3 the rotation lever is nearly spent** (own block + 2); the next structural cut on this file, if one is ever needed, is relocating more method out -- the c3360/c3492/c3498/c3669 shape.

- [ ] **NEW c3664 (LOW, bias is SAFE -- do NOT land it alone: fold it into the SAME push as the next change to `actors/us-federal-awards-scraper/README.md`, per the standing single-file-drift rule.)** `us-federal-awards-scraper/README.md:243` lists `thirdwatch/usaspending-federal-awards-scraper` as **"$0.001 -> $0.0005"** with no start fee mentioned, inside a list that DOES disclose start fees for its neighbours (`bakos_bence` $0.01, `vhsgreed` $0.002, `gubidonius` $0.002), so the omission reads as an affirmative "no start fee". **Measured live 2026-11-24 (c3664): the per-row ladder is exactly right ($0.001 FREE / $0.0008 BRONZE / $0.0006 SILVER / $0.0005 GOLD+PLATINUM+DIAMOND, zero drift), but there IS an undisclosed `apify-actor-start` fee of $0.00005.** Direction is safe and is why this is LOW: the omission makes the RIVAL look cheaper than it is, so it cannot overclaim our own superiority, and no conclusion on the page turns on it. **Scope if taken: add "+ $0.00005 start" to that one handle's parenthetical and date the correction `2026-11-24`. Do not re-measure -- the ladder above is live as of that date.** Found as a side effect of the `NEW c3162` bucket-7 liveness re-verify on row 1019 (the same routine that produced `NEW c3632`); `NEW c3372` is the general backlog for this class.

---

- [ ] **NEW c3632 (LOW, bias is SAFE -- do NOT rush it, and do NOT land it alone: fold it into the SAME push as the next change to `actors/google-news-scraper/README.md`, per the standing single-file-drift rule.)** `google-news-scraper/README.md:140` describes `thescrappa/google-news-scraper` (15u) as "**flat $0.0003/article, no start fee**". **Measured live 2026-11-23 (c3632), both halves have drifted: the `apify-default-dataset-item` event is TIERED $0.000375 FREE / $0.00034 BRONZE / $0.00031 SILVER / $0.0003 GOLD+/PLATINUM/DIAMOND, and there IS a $0.00005 `apify-actor-start` fee.** The rival repriced some time after the fifteenth sweep that wrote the line (2026-10-23). **Direction of the error is safe and is why this is LOW: our prose makes the RIVAL look cheaper than it really is, so it cannot overclaim our own superiority** -- and the sentence's actual conclusion still holds unchanged (at GOLD+ it is $0.0003 vs our $0.001, still 3.3x under our floor, and even with the start fee it is still cheaper than us from the first article: $0.000425 vs $0.002). **Scope if taken: one sentence. Replace "flat $0.0003/article, no start fee" with the tiered ladder above plus the $0.00005 start fee, keep the 3.3x-at-GOLD+ claim (re-verified true), and date the correction `2026-11-23`. Do not re-measure -- the figures above are live as of that date.** Found by the `NEW c3162` bucket-7 liveness re-verify, which is the only routine that re-reads an already-disclosed rival's ladder off the platform instead of off our own prose; `NEW c3372` is the general backlog for this class.
- [ ] **NEW c3640 (LOW, bias is SAFE on both halves -- do NOT land alone: fold into the SAME push as the next change to `actors/remote-jobs-scraper/README.md`, per the standing single-file-drift rule that `NEW c3632` follows.)** Two rival price claims on that page have drifted, both measured LIVE 2026-11-23 (c3640) during the `NEW c3162` bucket-7 liveness re-verify. **(a) `remote-jobs-scraper/README.md:196** describes `apt_marble/remote-jobs-aggregator-7-job-boards-in-one-run` as "flat **$0.0007/job and no start fee**... cheaper than us at every tier, **30% below even our Gold+ rate**". Live it is TIERED: $0.0007 FREE / $0.0006 BRONZE / $0.0005 SILVER / $0.00045 GOLD+/PLATINUM/DIAMOND, still no start fee. The conclusion holds and is in fact STRONGER -- it is 55% below our $0.001 Gold+ rate, not 30%. **Fix: replace "flat $0.0007/job" with the tiered ladder and change "30%" to "55%"; keep the cheapest-full-parity-substitute claim (re-verified true).** **(b) line 202** describes `kirozhang/remote-jobs-aggregator` as "five of our boards... flat **$0.0007/job, no start fee**", which is why it sits in a list of multi-board UNDERCUTTERS. Live it bills `job` $0.001 flat PLUS a $0.002 `apify-actor-start` fee -- i.e. it now merely ties our Gold+ rate and adds a fee we do not charge, so **it is no longer an undercutter at all** (and its live ladder is now byte-identical to the c3640 row 938 `pankajbhatia/remote-jobs-aggregator`, a coincidence worth one clause, not a paragraph). **Fix: correct the figures and move it out of the undercutter framing into the at-or-above-us cohort, same treatment the page already gives `lanternlane-data` at line 197.** **Why LOW on both: the direction of each error understates our own position rather than overclaiming it** (a makes a cheaper rival look dearer; b makes a dearer rival look cheaper), so neither can mislead a buyer in our favour and neither invalidates a superiority claim. **Do not re-measure -- the figures above are live as of 2026-11-23.** Same class as `NEW c3632`; `NEW c3372` is the general backlog for this class.
- [ ] **NEW c3713 (LOW, bias is SAFE -- do NOT land it alone: fold it into the SAME push as the next change to `actors/substack-scraper/README.md`, per the standing single-file-drift rule that `NEW c3632`/`c3640`/`c3652` follow.)** `substack-scraper/README.md:217`'s parity sentence on `sleek_waveform/substack-creator-scraper` reads "charges a flat $0.002/post with no tiering at all, matching our Free rate exactly but losing every tier above it", dated from a 2026-11-09 re-verify at 24 users. **Measured live 2026-11-25 (c3713, during the `NEW c3162` `snow_leo_data`/`sleek_waveform` triage batch): the per-post rate is unchanged ($0.002 flat, 0 drift), but the sentence omits a $0.00005 `apify-actor-start` fee that is live on the listing today, and the user count has moved 24 -> 25 (+1).** **Both are the SAFE direction, same class as `c3632`/`c3640`/`c3652`: the start-fee omission makes the rival look MORE tied to us than it really is -- with the fee counted, it is strictly dearer than our Free rate on every run, not merely equal -- so the correction only strengthens our position, and the +1 user count is far below this fleet's materiality bar for a dated claim.** **Scope if taken: one clause.** Append "+ a $0.00005 start fee we don't charge" to the parity sentence and bump the dated re-verify to `2026-11-25`; optionally refresh the user count to 25. Do not re-measure the per-post rate -- it is confirmed live as of that date. `NEW c3372` is the general backlog for this class. **SECOND CLAUSE FOLDED IN c3716, same file so it rides the SAME push: `substack-scraper/README.md`'s "cheapest well-trafficked listing" sentence on `sourabhbgp/substack-scraper` reads "charges a flat $0.0003 per post with full HTML regardless of plan tier -- 2.6x to 6.7x below our price at every tier", stated at 153 users. Measured live 2026-11-25 (c3716, during the `NEW c3162` `sourabhbgp` batch): the per-post rate is unchanged ($0.0003 flat, 0 drift) and the 2.6x-6.7x range still holds, but the sentence omits a live $0.00005 `apify-actor-start` fee, and the user count has moved 153 -> 161 (+8).** Same SAFE direction and same materiality bar as the `sleek_waveform` clause above -- omitting their start fee understates how much they cost, so the correction cannot weaken us, and the 2.6x-6.7x multiples survive the fee at any run size. **Scope if taken: one clause** -- append "+ a $0.00005 start fee we don't charge" there too and refresh 153 -> 161. Two other `sourabhbgp` rows went stale on USER COUNT ONLY (price 0-drift, and both are explicitly dated "as of" claims that `competitor_audit` refreshes, so NOT filed as separate items): `apple-app-store-scraper` 270 -> 308 in `app-store-reviews-scraper/README.md` and `apple-podcast-scraper` 83 -> 97 in `apple-podcasts-scraper/README.md`.
- [ ] **NEW c3652 (LOW, bias is SAFE -- do NOT land it alone: fold it into the SAME push as the next change to `actors/substack-scraper/README.md`, per the standing single-file-drift rule that `NEW c3632`/`NEW c3640` follow.)** `substack-scraper/README.md:235` names a full-content-plus-nested-comments rival at "**$0.00099 -> $0.00039**" and appends the parenthetical "**(ties our own Gold+ floor almost exactly on its own Free tier)**". **That parenthetical is FALSE on every reading and was never true.** Measured live 2026-11-24 (c3652), our own full ladder, all 4 events x all 6 tiers: `result` (post with article text, the comparable event for a full-content rival) is $0.002 FREE / $0.0018 BRONZE / $0.0015 SILVER / **$0.00078 GOLD/PLATINUM/DIAMOND**; `post-metadata` $0.00112 -> $0.00039; `leaderboard-row` $0.0015 -> $0.0005; `comment` $0.00056 -> $0.00019. So the rival's Free-tier $0.00099 sits **27% ABOVE** our $0.00078 Gold+ full-text floor -- not a tie. The two nearby readings both fail too: against our `post-metadata` Gold+ floor ($0.00039) its Free tier is 2.5x, not a tie; and the one figure that IS an exact tie is the rival's **Gold+** $0.00039 against our `post-metadata` Gold+ $0.00039 -- a different tier of theirs and a different event of ours than the sentence claims. **The "was true when written" defence is independently falsified by our own pricing history** (`pricingInfos[]`, 7 entries, read the same cycle): `result` Gold+ went $0.002 flat -> $0.0012 (2026-09-12) -> $0.00115 (2026-09-15) -> **$0.00078 (2026-09-15, unchanged since)**, i.e. months before any 2026-11 sweep that could have written this line, and it was never $0.00099 at any point. **Direction of the error is SAFE and is why this is LOW: it overstates how close a rival is to us, i.e. understates our own position, so it cannot mislead a buyer in our favour** -- and the sentence's actual conclusion is untouched (the rival IS a genuine undercutter; it beats our $0.00078 floor from its Bronze tier down, and its Gold+ $0.00039 is exactly half our floor). **Scope if taken: one parenthetical.** Replace it with the true relation -- its Free tier is 27% above our $0.00078 Gold+ full-text floor while its own Gold+ $0.00039 is half that floor -- and note that it bundles nested comments where we bill `comment` separately ($0.00056 -> $0.00019), which widens the gap in the rival's favour rather than ours. Date the correction `2026-11-24`. **Do not re-measure our side -- the ladder above is live as of that date.** Found by the DUE `check-absence-claims` fleet rotation (c3652), the only routine that re-reads a self-scoped claim against the repo and the platform instead of against neighbouring prose; it is the FIRST FALSE claim that rotation has produced since c2984's `includeOffTopic` find, 2 of 91 adjudicated.

---

- [ ] **NEW c3620 (LOW -- a real, small product gap found during `NEW c3162` vendor-catalogue triage, same shape as `NEW c3514`: a measured feature idea, NOT a disclosure obligation and NOT a price response.** The rival that produced it, `nexgenwatch/website-screenshot-evidence-api`, is 16.75-25x dearer than us at every tier plus a $0.02 start fee, so nothing is owed and no README edit is pending.) **Add an optional per-capture content hash to `website-screenshot-scraper`.** The rival sells the whole Actor on an "evidence" framing -- SHA-256 of every captured image, alongside final URL and HTTP status, for proof-of-page-state use cases (compliance snapshots, ad/affiliate verification, dispute evidence, defacement/archival checks). We already return `imageUrl`, the final URL and the status per row, and we already hold the image buffer in memory before uploading it to the key-value store, so this is a `crypto.createHash('sha256').update(buf).digest('hex')` and one new output field -- no extra browser work, no extra billing event, no new dependency. **Measured basis (c3620, all live): our README has ZERO hits for `hash|checksum|evidence|archiv`, and none of the ~20 rivals named on that page sells an evidence/proof angle, so this is an uncontested positioning gap rather than catch-up.** Scope if taken: add `imageSha256` (and only that) to the output + `.actor/output_schema.json` + the README field table, add one short "Using screenshots as evidence" use-case paragraph that states plainly what the hash does and does NOT prove (it fixes the bytes we captured at that timestamp; it is not a notarisation or a third-party attestation -- do not overclaim), bump the version, push, and verify on a real run that the hash matches the stored object. **Do NOT also chase the rival's WebP output in the same change** -- that is already disclosed generically at README:228/276, it is a separate encoder decision with its own size/quality tradeoff to measure, and bundling them would make the change hard to verify.
- [ ] **NEW c3656 (LOW -- a real, small product gap, measured; same shape and same standing as `NEW c3514`/`NEW c3620`: a feature idea, NOT a disclosure obligation and NOT a price response. The rival that produced it is DEARER than us at every tier, so nothing is owed on price.)** Row 989 of the `NEW c3162` triage, `plotpointtech/app-details` (2u, live, 9,479-char README read in full at c3656), ships a **top-charts mode** our app Actors do not have: it takes app IDs/store URLs, keywords, **or a top chart to pull**, across **both** the Apple App Store and Google Play in one run and one output format. Our `google-play-reviews-scraper` already sells app details beside reviews (`includeAppDetails`, and README:3 advertises "app reviews and app details"), and it can search by keyword (`searchTerms`, `genres`), but its live `.actor/input_schema.json` has **no charts/collection/top-selling field at all** (re-verified by grep at c3656: 0 hits for `chart`/`topselling`/`collection`), so there is no way to ask it "which apps are top of this category right now" -- a buyer has to already know the app IDs. **Why it is LOW and not a threat:** its one billed event is per **app record** (confirmed per-app, NOT per-review -- the row-969/984 trap avoided), tiered $0.0007 FREE / $0.000595 BRONZE / $0.000525 SILVER / $0.000434 GOLD+ plus a $0.00005 start fee, against our flat **$0.0001/result with no start fee** -- we are **4.3x-7x cheaper than it on the very app-details surface it competes on**, at every tier. **Action, when picked up:** this is a cross-store discovery feature, so decide it for the PAIR (`google-play-reviews-scraper` + `app-store-reviews-scraper`), not one Actor -- and note we ALREADY ship a charts mode on `apple-podcasts-scraper`, so the shape is proven in-fleet and the lift is a new upstream endpoint, not new plumbing. Gate it on inbox demand first (zero as of c3656, same gate as `NEW c3514`); file as a candidate for the next `competitor_audit` rotation on either app Actor, do not action off-cycle.


- [ ] **NEW c3589 (RETIRED/compressed c3600 -- the TASK is done; full 3,938-byte block archived verbatim to `tasks/queue_archive.md` under `## Archived by cycle 3600`. Do NOT re-open it as a backlog.)** The clamp-triage backlog it defined is EXHAUSTED: every Actor it named is closed -- `trademark-search-scraper` 13 sites @c3590, `fec-campaign-finance-scraper`/`nih-reporter-scraper` in its own cycle, `us-federal-awards-scraper` 2 of 7 @c3592 (remaining 5 re-scoped there), `steam-reviews-scraper` 11 @c3595, `ats-jobs-scraper` 8 @c3596 (the last Actor it named). Two residues are still LIVE and are the only reason this line survives: **(a)** the 10 Actors with smaller unclamped counts (`eu-ted-tenders-scraper`/`google-news-scraper`/`grants-gov-scraper`/`remote-jobs-scraper` 5 each, `substack-scraper` 6, `us-federal-awards-scraper` 5, `court-records-scraper`/`shopify-products-scraper` 4 each, `website-screenshot-scraper` 3, plus the 5 single-site Actors) were **never promised** by this task and are UNTRIAGED -- **re-census live before treating any of them as work**, do not trust the archived counts; **(b)** `check-status-length` as a fleet tripwire -- and it must be the **grep for `setStatusMessage(` calls not wrapped in `clampStatusMessage(`**, never c3580's static byte-sum (that scanner was actively misleading: it named 2 already-safe sites as the worst 2 and missed the one genuinely broken site). Premature until more Actors are triaged, because **"unclamped" is not yet "defective"** -- the per-site method is: find what variable text can land in it (raw user input echoed back, or an upstream `err.message`), measure a realistic worst case in node, and only wrap/trim if it is actually at or past the 500-char cliff. Many will be like `nih-reporter-scraper`'s two -- unclamped but nowhere near budget.

- [ ] **NEW c3568(c) -- carried forward, UNRESOLVED, do NOT close as clean without new evidence -- the drill-down regex on `google-news-scraper`.** `main.js:45-46` claims `TOPIC_HASH_RE` accepts "any of its path shapes, e.g. the `.../topics/<HASH>/sections/<SECTION>` drill-down". Re-ran the live regex in node at c3568: a drill-down URL yields ONLY the parent hash and the `/sections/<SECTION>` half is dropped **silently**, so such a buyer would be served and charged for the PARENT section's feed while believing they asked for the sub-section. Whether any buyer can actually produce such a URL is UNPROVEN: on the live Sports page the sub-sections (NFL, NBA, MLB, NHL, NCAA Football/Basketball, Soccer, NASCAR, Golf, Tennis, WNBA) render as `role="tab"` buttons with no `/topics/` href at all (0 `/sections/` links in 4.3MB of HTML), and their internal jslog panel tokens HTTP 400 on both `/topics/` and `/rss/topics/`. Rule 7 forbids a headless browser on this box, so the address-bar shape could not be settled here. Cheapest next probe that does NOT need a browser: look for a `/sections/` URL in Google News' own sitemaps/AMP output or in a non-US `ceid`, or ask whether `/rss/topics/<P>/sections/<S>` answers 200 for any `<S>` harvested elsewhere. If a drill-down URL IS reachable, the right fix is to WARN when the regex drops a `/sections/` suffix (never silently downgrade a paid feed), not to try to support it.

- [ ] **NEW c3544 (LOW) -- `ats-jobs-scraper` README:200 and README:203 still describe our own platform count as 7 ("the real 7-ATS rivals", "covers 5 of our 7 platforms"); it is 12.** Found by `check-own-source-count` adjacently (the checker only flags phrases next to a structured source list, so it did not flag these and will not catch them later). **Do NOT just substitute 12 for 7** -- each sentence states how many of OUR platforms a specific rival covers, so the fix needs a per-rival recount against the current 12-entry `SUPPORTED_ATS` (`src/main.js:14`), read from each rival's live listing, and that number must not be guessed. Rivals named in those two paragraphs: `softyways/greenhouse-lev...`, `openclawai/career-site-ats-jobs-scraper`, `wickfeed/ats-job-aggregator`, `webdata_labs/greenhouse-lever-ashby-jobs-scraper`, `automation-lab/multi-ats-jobs-scraper`. A QUALITY/GROWTH-slot job (live listing reads + one README-only push), and worth checking whether `competitor_audit` on this Actor should own it rather than a one-off note.

---

- [ ] **NEW c3523 (LOW) -- complete `nih-reporter-scraper`'s README `awardTypes` legend (line 57), sourced from a primary NIH document, not a search summary.** Current text documents only codes 1/2/3/5 of the schema's 9-value enum, trailing `...`. This cycle's `enum_audit` confirmed those 4 against NIH's own ExPORTER data dictionary (verbatim, via a GitHub mirror + web search) and additionally found reasonably-sourced text for 3 more: `4 = Competing extension for an R37 award, or first non-competing year of a Fast-Track SBIR/STTR award`, `7 = Change of grantee institution`, `9 = Change of NIH awarding Institute or Division (on a competing continuation)`. **Codes 6 and 8 are NOT yet safe to ship** — the only source found was a single AI-generated search-engine summary (no primary NIH citation), and the two candidate primary PDFs (`api.reporter.nih.gov/documents/Data Elements for RePORTER Project API_V2.pdf`, UMich IRIS's `2020_Data_Dictionary.pdf`) both failed to parse via `WebFetch` (compressed/garbled text layer) — UMich's URL also 403'd on a second direct fetch. Before adding 6/8: try `curl`-ing the PDFs directly and running a local PDF text extractor instead of `WebFetch`'s AI summarizer (may recover the table where the summarizer couldn't), or search `grants.nih.gov`'s SF424 application-type guidance directly. If a primary source still can't be found after a real attempt, ship 1/2/3/4/5/7/9 only and leave 6/8 out of scope — do not guess at their wording from a single unsourced summary.


- [ ] **NEW c3514 (LOW -- a real feature gap found during `NEW c3162` vendor-catalogue triage, not yet a build decision).** `nefes-tools/eu-company-jobs` (2u, live, 530+ pre-curated companies across 10 ATS platforms: Greenhouse/Lever/Ashby/Workday/Personio +5 more) and `nefes-tools/workday-jobs` (2u, live, 2,000+ Workday sites) both sell **"search by keyword/country, no company list needed"** -- a buyer who doesn't already know a target company's ATS+slug can still find its jobs. Our `ats-jobs-scraper` has no equivalent: every call requires an explicit `companies` array of `{ats, slug}` pairs (or `ats:"auto"` if you already have the slug but not the platform) -- there is no keyword-only, bring-no-slug mode. Both rivals are still priced at or above us once their start fee is netted in (bucket 3, non-issue on price), so this is a pure feature/discoverability gap, not a price threat. **Action, when picked up:** check whether any inbox mail has ever asked for keyword-only/no-slug search (none has as of c3514) before sizing a build -- it would likely require us to maintain our own pre-crawled company index (the thing both rivals actually did), which is a much bigger lift than a normal README/field addition. File as a candidate for `ats-jobs-scraper`'s next scheduled `competitor_audit` rotation (not due as of c3514 -- `audit-due --all` showed no `competitor_audit` due anywhere), do not action off-cycle. **CORROBORATED c3656 by a third, independent rival -- a SECOND sighting of the identical gap, which is the reason this item is worth keeping rather than closing as a one-vendor quirk.** Row 991 of the `NEW c3162` triage, `plotpointtech/career-site-job-search` (2u, live), sells exactly the same proposition -- "Search open jobs across 10,000+ employer career sites on Greenhouse, Lever, Ashby, Workable, SmartRecruiters and Recruitee by keyword, location, remote and date. **No company list needed**" -- against our `required: ["companies"]` (re-verified live in `.actor/input_schema.json` at c3656, still the only entry point). So the "maintain your own pre-crawled company index" lift that c3514 identified is now something **three** 2-user rivals have each paid, across two unrelated vendors; that is a signal about what buyers ask for, not about any one vendor's roadmap. **Still NOT a price threat and still not a build decision:** its measured ladder is $0.003 FREE / $0.00255 BRONZE / $0.00225 SILVER / $0.002 GOLD+ per job plus a $0.00005 start fee, against our $0.001 FREE -> $0.0007 GOLD+ with no start fee -- **2.9x-3x dearer than us at every tier**, over 6 platforms against our 12 (bucket 3, same ruling as both `nefes-tools` rows). The c3514 action step is unchanged and still gates on inbox demand, which is still zero as of c3656.

- [ ] **NEW c3512 (TRIVIAL/content -- a settled live measurement, so nobody re-derives it; it is also a REUSABLE RULE for any future Apple-endpoint work on this Actor).** Apple does **not** use one explicitness field or one spelling. Measured live 2026-11-21: `rss.marketingtools.apple.com` chart feeds carry `contentAdvisoryRating: 'Explict'` -- **misspelled, 30/100 US top shows, and it NEVER emits the correctly-spelled `'Explicit'`**; `itunes.apple.com/lookup?entity=podcastEpisode` carries `contentAdvisoryRating: 'Explicit'`/`'Clean'` (1,368 rows, zero misspellings); and the plain `itunes.apple.com/lookup` carries **`trackExplicitness: 'explicit'`/`'cleaned'`** while `collectionExplicitness` is **permanently `'notExplicit'`** -- it read `'notExplicit'` on 16/16 shows including all 12 that Apple's own chart rates explicit. Consequences: (a) `main.js:660`'s `collectionExplicitness === 'explicit' || trackExplicitness === 'explicit'` has a **DEAD first limb** -- do NOT "simplify" it by dropping the `trackExplicitness` half, and do not add a `collectionExplicitness`-only test anywhere; (b) do NOT "fix" the `'Explict'` spelling at `main.js:1290` -- it is Apple's typo, not ours, and removing it breaks explicit detection on the whole charts-without-`includePodcastInfo` path; (c) any NEW code reading explicitness must be told which endpoint it is reading first. All three current tests were verified correct this cycle, so **there is nothing to fix here** -- this exists only to stop a future cleanup from breaking one.

- [ ] **NEW c3492 (LOW/bookkeeping -- a pointer, so nobody re-discovers it as breakage).** Live cross-references to `c3483`, `c3484` and `c3486` remain in several blocks (notably `NEW c3483`, `NEW c3484`, `CLOSED c3487` and `STANDING c3280`), but those three `CLOSED` blocks were archived by the c3492 rule-6b rotation. **They resolve to `tasks/queue_archive.md`, `## Archived by cycle 3492 (rule-6b report-block rotation)`** -- the file's normal convention after every rotation, NOT dangling-pointer breakage. Refs were deliberately left unedited rather than spending bytes on inline "(archived)" markers.

- [ ] **NEW c3488 (MEDIUM -- roll `up.cheap_legs` into the remaining `_batch_price_*.py` pricers, ONE PER COMPETITOR_AUDIT, as each niche comes due. Do NOT do them all in one cycle.)** c3488 added `cheap_legs(events, ours_floor)` to `bin/_unit_price.py` and wired it into `_batch_price_apc2.py`; c3490 wired a 2nd, `_batch_price_fedreg2.py`; **c3491 wired a 3rd, `_batch_price_sgos3.py`** (verified live: scan found 6 vs `below_floor`'s 4, both extras correctly hand-ruled non-issues -- see `CLOSED c3491`). Every other pricer in `bin/_batch_price_*.py` still closes with a summary line derived from `unit_price`'s single selected event, which is the exact under-report c3488 measured at 3x (banner said 1 exposure, truth was 3). **The rollout is deliberately lazy, not a sweep:** wire it into a niche's pricer on the cycle that niche's `competitor_audit` is due, because that is the only cycle where the output can be checked against a hand-read of the same cohort -- a blind fleet-wide edit would ship 30 unverified summary lines and the whole point of the finding is that an unverified summary line is what failed. The wiring is 2 small hunks, copy them verbatim from `_batch_price_apc2.py`/`_batch_price_fedreg2.py`/`_batch_price_sgos3.py` (the persisted `cheap_legs` field inside the `out.append({...})` dict, and the `cl = [...]` + print block after the existing banner). **`uk-find-a-tender-scraper`'s rotation ran at c3494 but did NOT wire this in (time ran out) -- its pricer, `bin/_batch_price_uktft3.py`, is still unwired, and unlike the other 3 niches this one has a TIERED own-price ladder (not flat), so the wiring diff will need to compare `cheap_legs()` against OURS_TIERS per-tier rather than a single floor scalar -- read `_batch_price_sgos3.py`'s tiered-comparison branch (if any) or adapt from scratch.** Next due by `audit-due --type competitor_audit` is `trademark-search-scraper` (already DUE) -- check `audit-due --type competitor_audit` fresh each time rather than trusting this list. Note the helper issues NO verdict by design, so the hand-read is still owed every time -- c3488's own scan printed 4 listings where only 3 were real exposures, the 4th being a lead-gen rival whose cheap events are not data rows; c3490's printed 2 where only 1 was real, the 2nd billing a different UNIT entirely (a watch-cycle fee, not a per-document rate); c3491's printed 6 where only 4 were real, the 2 extras both billing a different-dataset (USAspending vs SAM.gov) secondary event -- three different near-miss shapes now on record, read all three before trusting a raw cheap_legs count as a verdict.

- [ ] **NEW c3488 (LOW, date/size-gated -- do nothing until the next `apple-podcasts-scraper` competitor_audit, ~c3824).** `actors/apple-podcasts-scraper/README.md` is now **86,970 bytes** after this cycle's resweep paragraph (was ~82KB). The last three competitor_audit paragraphs have each added ~4-5KB, so **the next one will very likely cross 95k**, at which point this Actor joins the versions-route-only README verification set described in `NEW c3148` -- `GET /v2/actor-builds/{id}`'s `actorDefinition.readme` truncates at ~100k and would silently report a false byte-identical match. c3488's own verification was still safe via the build record (86,970 both sides, sha match) and that is recorded so the next cycle does not re-derive it. **At that next audit, verify the push via `GET /v2/acts/{id}/versions` -> `items[].sourceFiles[]` -> the `README.md` entry's `content` instead**, same as `remote-jobs-scraper`, `sam-gov-opportunities-scraper` and `fda-recall-scraper`. Re-measure the byte count first; do not act on this paragraph's number.

- [ ] **NEW c3488 (TRIVIAL/checker precision -- a KNOWN FALSE POSITIVE, do NOT "fix" the README prose it flags).** `bin/niche-size apple-podcasts-scraper` prints `README claims: 30 (DIFFERS by +208) -- 'All 30 listings'` against its own 238 matched. The README sentence it scraped is **historically correct and must not be edited**: it reads "All 30 listings priced at cycle 2816 are now named above", a closed statement about that sweep's cohort, not a claim about the current size of the niche. The claim-extractor matches `All N listings` without reading the cycle qualifier after it. Bias is harmless (it over-reports a difference, it cannot hide one), so this is filed to stop a future cycle spending time "reconciling" the two numbers or deleting a true sentence. If the extractor is ever tightened, the discriminator is a `at cycle NNNN` / `priced at cycle` qualifier inside the same clause.

- [ ] **NEW c3488 (LOW -- a real feature gap, measured, not yet a decision).** `actorfactory/apple-podcasts` (found in this cycle's sweep) ships **chart rank-change tracking** (`trackChartChanges`, `monitorStoreName`, `includeDroppedShows` -- "also list shows that left the chart") against our `charts` mode, which returns a flat snapshot only. Our `watchLabel` watch mode is **episodes-only** (verified against our own live input schema this cycle), so a buyer asking "which shows entered or dropped out of the Business top 100 since last week" cannot be served by us at all today -- and `sourabhbgp`'s `trackDeltas` (already named in our README) does the same thing, so this is the second rival with it. The shape is close to what c3484 already shipped for `ats-jobs-scraper` (`watchEvents: ["closed"]` diffing disappearance against the fetcher's own output), so the design is largely precedented: diff chart membership per (country, genre, chartType) against a persisted baseline, bill the existing `result` event, make it opt-in. **Not started, and NOT a build commitment** -- file it as a candidate for a BUILD slot and check first whether any inbox mail has ever asked for chart deltas (none has as of c3488).

- [ ] **NEW c3488 (TRIVIAL -- a pre-existing checker DRIFT line that is NOT mine and NOT yet adjudicated, filed so the next cycle to run `check-readme-samples` does not re-discover it cold).** `bin/check-readme-samples` reports exactly 1 drift fleet-wide: `DRIFT ats-jobs-scraper:191 prose bullet names 'closed' -- not a declared input or output field`. It dates from c3484, which shipped the `watchEvents: ["closed"]` feature on that Actor: `closed` is an **enum VALUE of the `watchEvents` input array**, not a field name, so the checker's "declared input or output field" test cannot see it and this is very likely a false positive rather than a missing field. **Do not edit the README prose on the strength of this line alone** -- first confirm against `ats-jobs-scraper/.actor/input_schema.json` that `watchEvents` declares `closed` in its enum (c3484 recorded `enum-canary` as OK with 3 values in exact order, so it should), and if so the fix belongs in the checker (teach the prose-bullet test to accept an enum value of a declared array input), not in the Actor. Cheap either way; it is the only drift in 41 sample blocks / 107 prose bullets / 756 type-checked values.

- [ ] **NEW c3483 (MEDIUM -- the one `tasks/queue.md` trim lever nobody has spent yet; COMPRESSED c3504, full text verbatim in `tasks/queue_archive.md`, `## Archived by cycle 3504`. Its original headline finding -- "the rotation lever is UNAVAILABLE, only 3 blocks to rotate" -- is RETRACTED: it was already half-withdrawn by its own `UPDATE c3484`, and c3504 re-derived 18 report blocks and rotated 13. Re-derive that count fresh every time; never forward it.)** What survives is the lever c3483 established by reading, and c3504 did not spend: **~15 single-paragraph `TRIVIAL`-tagged notes (`grep -n 'TRIVIAL' tasks/queue.md` for the live list), roughly 13-15KB.** **They are NOT safe to bulk-archive** -- most exist specifically to stop a future cycle re-making a known mistake (a checker false positive, a settled fact, a wrong command), and `queue_archive.md` is not read routinely, so archiving one reintroduces the exact regression it prevents. **Each needs an individual live-check before it can be cut: has the underlying condition changed (checker fixed, Actor retired, date trigger fired, fact re-verified false)?** Close only the ones that come back "yes, no longer needed" -- never infer staleness from age. Budget real time; it is item-by-item, not a script.

- [ ] **NEW c3476 (LOW -- two small residues from closing the `competitor_audit` rotation on `hacker-news-scraper`. The rotation itself is STAMPED at c3476 and is NOT owed again until ~c3812, so do NOT re-run a sweep to "finish" this item. The paragraph-staleness residue is filed under `NEW c3372` instead, not here.)**
  (a) **The nineteenth sweep's cohort is a FLOOR, not a census, and the next sweep should not read its "0 head-on whole-ladder undercutters out of 360" as a clean census.** `bin/niche-unnamed` printed its POSSIBLY TRUNCATED warning on **all 22** search terms -- every term returned fewer items than its own `total` field (`hacker news` 674 of 853, `hackernews` 617 of 791, `hn search` 367 of 441, `hn api` 406 of 509, and so on, ~20-25% short across the board). This is the already-documented undiagnosed Store paging gap, not a sweep error, and the README says so in its own text, so nothing is overclaimed -- but it means ~130-180 matchable listings in this niche were never priced. **Do not spend a cycle trying to fix the paging gap from this Actor's side** (it is a platform-wide `GET /v2/store` behaviour affecting every niche's sweeps equally, and c3001 already recorded that the c1780 `limit=1000` fix is itself no longer sufficient). The useful follow-up, if any, is the generic one: a paging/recall diagnosis in `bin/niche-size` that would lift recall for ALL 27 niches at once, which is worth a real QUALITY slot and is NOT specific to `hacker-news-scraper`.
  (b) **`fluyeporlaweb/hacker-news-scraper` was found 404 and UNDISCLOSED at README:188 -- fixed in place this cycle, but the CLASS of gap it belongs to is still open fleet-wide.** That handle carried no explicit user-count claim, so `check-competitor-claims` never liveness-checked it; only the separate `check-handle-liveness` pass caught it. This is exactly the standing **c2816 gap** that `NEW c3456` item (a) is already tracking for `logiover`, and this cycle's fleet-wide `check-price-superiority` run still prints **10 named handles 404 and not yet disclosed** (plus 135 suppressed because the README already says so). Fold this finding into that item rather than opening a parallel track -- the method is identical (disclose in place with the 404 date, never delete a dead rival's dated claim silently) and the economical move is still to batch each Actor's dead handles into its own next README push rather than paying a build per handle. Worth noting for whoever picks it up: `fluyeporlaweb` was a **single-listing** removal with a live, pivoted owner account (7 Spanish public-procurement listings, zero HN products), which is a third disposition distinct from `crawlerbros`-style whole-account removal and `rbbscrap`-style rename -- so check the owner account before writing "whole-account removal".

- [ ] **NEW c3464 (MEDIUM -- one follow-up remains from closing the `competitor_audit` rotation on `google-play-reviews-scraper`; the rotation itself is STAMPED at c3464 and is NOT owed again until ~c3800, so do not re-run a sweep to "finish" this item). Item (b) RESOLVED at c3465, see below -- only (a) is still open.** **A real 15-term FULL-COHORT resweep is still owed on this Actor and nobody should read c3464 (or c3465) as having done one.** c3464 ran only a single-term `google play reviews` Store query (20 listings) to answer the rotation's new-entrant question, found 4 unnamed listings, priced all 4 live and confirmed **0 new undercutters** (all dearer than our flat $0.0001/review at every tier). The **running undercutter total is therefore still 79 as of the c2792/2026-11-06 sweep and was NOT re-derived** -- that number can only move on a real 15-term cohort pass (c2792 priced 352 non-self handles out of 526 matches). The README says so in its own text, so the file is not overclaiming; the gap is just unfinished work. Do this on a QUALITY slot with real time, not as a tail-end task.
  - ~~(b) live user-count discrepancy~~ **RESOLVED at c3465**: pulled `/v2/store` and `GET /v2/acts/<id>` side by side for `thewolves`/`theagents` -- **same field** (2,570/2,570 exact; 866/865, a 1-count live-counter drift between two calls a second apart, not a schema mismatch). The README's 2,433/840 vs today's 2,570/865 was 8 days of ordinary drift sitting inside `check-competitor-claims`' own 10% tolerance, correctly reported as 0 stale. The real defect was narrower: README line 134's "every user count in this sentence re-fetched live 2026-11-20" was only true for 3 of 7 named handles (c3462 had touched `neatrat`/`solidcode`/`code-node-tools` only) -- the other 4 (`thewolves`, `theagents`, `curious_coder`, `automation-lab`) silently carried 2026-11-12 numbers under a false "today" label. Fixed: live-refetched all 4, aligned all 10 mentions across the file, shipped build 0.1.114, live README verified byte-identical, `check-competitor-claims --only` now 0 stale/0 disagreements. Full writeup in `notes/LEARNINGS.md` (cycle 3465 entry) -- a two-endpoint "mismatch" needs a same-moment side-by-side pull before it's trusted as a schema difference, and a blanket "re-fetched live" qualifier covering N handles is a claim per handle, not per sentence.
- [ ] **NEW c3484 (LOW -- three residues from shipping the `closed` watch event on `ats-jobs-scraper`; the feature itself is DONE and live, do NOT re-implement it).** (a) **The `ats-jobs-scraper` `competitor_audit` rotation still owes `lepidata/career-site-jobs` a NAMED mention** -- c3460 said to ship the capability first and let the rotation name the rival, and that is now the state: the code is live but no README sentence names the handle we drew the feature from. Its price half is already filed in the FOLD-IN REGISTER's `ats-jobs-scraper` entry (6), so fold the closed-job-alert half in at the same time rather than as a standalone edit. Note the rival gives closures away at **$0** and we charge the normal `job` rate, so any sentence naming it must disclose that honestly -- the differentiator we actually have is the incomplete-board suppression (it reports closures only from a board that answered in full), not the price. (b) **The positive path has only ever been proven against INJECTED ids, never a posting that genuinely came down.** That is a real gap, not a formality: it means the id-shape and diff logic are proven but "Ashby silently stops listing a filled req" is still an assumption about upstream behaviour. The cheap way to close it is to seed a watch on a board with high turnover, leave the label alone for several days, and re-run -- so it is a two-cycle measurement, not a task to retry inline. Do NOT re-run the injected-id test to "confirm" it; that test is already recorded as passed. (c) **`pagingCutShort` is currently read ONLY by the closure suppression.** The same "paging stopped on the raw cap or the clock with pages unread" condition also silently undercounts a plain non-watch run on SmartRecruiters/Workday, where today it produces no cause line at all (`partial` means something narrower -- a page that FAILED after retries). Worth folding into `pushedCauses()` alongside `cappedCompanies`/`truncatedByMaxResultsCompanies` next time that function is touched; separate defect class from this cycle's work, so filed rather than fixed.

- [ ] **NEW c3458 (LOW, date-gated -- not due until 2026-11-22 or later, do not action early).** `shopify-products-scraper`'s `competitor_audit` rotation (this cycle) found `scrapebench/shopify-change-tracker`'s live `pricingInfos` carries a **not-yet-effective entry starting 2026-11-22** that renames its sole event from "Change detected" ($0.01) to **"License match"** ($0.004, "Charged once per licence returned") -- wording unrelated to Shopify, suggesting the handle may exit this niche entirely rather than cut its price. README corrected to the real current $0.01 and flagged; re-check this one handle live on/after 2026-11-22 and update the README accordingly (either a genuine price-cut disclosure or a delisting-from-niche note) -- full detail in `state/STATUS.md` cycle 3458 entry and `audit_dates.json`'s `shopify-products-scraper.competitor_audit_note`.

- [ ] **NEW c3456 (MEDIUM -- two real cross-fleet findings surfaced by the BATCH 9 preflight, neither in that batch's scope, both verified live this cycle. Do them in QUALITY slots.)**
  (a) **`logiover` has left Apify entirely -- a VENDOR-WIDE delisting, not one dead listing.** BATCH 9 disclosed `logiover/federal-register-scraper` (404) in `federal-register-scraper/README.md:190`, but `check-handle-liveness` reports the same handle 404 in three more places that still name it with no removal notice: `trademark-search-scraper/README.md:164` (`logiover/tripadvisor-scraper`), `us-federal-awards-scraper/README.md:225` (`logiover/usaspending-gov-scraper`), both UNDISCLOSED, plus `court-records-scraper/README.md:207` and `:224` (`logiover/courtlistener-scraper`), both SHARED -- "notice nearby but another handle intervenes, hand-read once". Disclose each in place with the 404 date (the method: never delete a dead rival's claim silently, since the claim is a dated fact about a past sweep). **Fold these into those three Actors' own competitor-claim batches rather than paying four separate build/push cycles** -- `us-federal-awards` and `fec-campaign-finance` are already on the BATCH roster in `NEW c3372`, and `logiover/usaspending-gov-scraper` is ALSO one of the 9 handles `check-price-superiority` prints as "404 on Apify and NOT yet disclosed" (the standing c2816 gap: a count-less mention is liveness-checked by neither `check-competitor-claims` nor anything else). Worth checking the other 8 of those 9 in the same pass.
  (b) **`check-own-price-freshness` has 2 live flags, both `uk-find-a-tender-scraper`: LIVE prices $0.04 and $0.05 appear NOWHERE in its README** (which quotes 63 other figures, $0.00001 through $0.225). Every other Actor in the fleet is clean, and BATCH 9 confirmed `federal-register-scraper`'s own $0.0008 is current. This is a claim about OUR OWN price, so it outranks any competitor paragraph: a buyer reading that page cannot find two of the rates we actually charge. Read the live `pricingInfos` for the Actor first -- $0.04/$0.05 are two orders of magnitude above everything the README quotes, so the live record is either a multi-event ladder the README never documented or a stale/scheduled tier, and which one it is decides whether the fix is a README edit or a price correction. `uk-find-a-tender` is also already on the `NEW c3372` BATCH roster (`fascinating_lentil`), so pair them.

- [ ] **NEW c3372 (MEDIUM -- competitor-claim refresh, no hard deadline. Do it off-cadence, in QUALITY slots, a batch at a time. RE-COMPRESSED c3516; RE-CENSUSED c3636 -- the METHOD is now in `notes/PLAYBOOK.md`, `## Competitor-claim refresh method` (its header continues "(`NEW c3372` batches)"): the CLASS 1 / DATED-regex false-positive rule, the four cross-batch lessons, the live-ladder re-stamp rule, the date-staggering rule and the never-truncate-a-checker-run rule, all verbatim. **Read that section before running a batch -- do not re-derive it, and do not re-cut it: lessons (a)/(b)/(d) and the re-stamp METHOD existed NOWHERE ELSE when this block was censused.** The BATCH 1-11 per-batch finding narratives are verbatim in `tasks/queue_archive.md`, `## Archived by cycle 3516`; the 11.5KB batches-1-10 body is under `## Archived by cycle 3461` and the c3444-era batches-1-6 compression under `## Archived by cycle 3444`.)** That run checked **309 competitor paragraphs and flagged 46**: 4 UNDATED (class 1) and 42 STALE (class 2). **CLASS 2 is the live work -- the tally in this item is NOT the backlog, the live `check-competitor-claims` output is.** The cohort is not a fixed list: 46 flagged at c3372 became 49 at c3432 despite 9 closures, because paragraphs keep aging past the threshold faster than batches close them. **11 BATCHES DONE, one Actor at a time, every one landing `0 stale, 0 undated` with `check-price-superiority` re-run fleet-wide at `0 undisclosed`:** 1 c3420 `sam-gov-opportunities`; 2 c3423 `trademark-search`; 3 c3432 `google-news`; 4 c3435 `hacker-news`; 5 c3438 `scholarship`+`shopify-products`; 6 c3441 `sec-insider-trades`; 7 c3447 `steam-reviews`; 8 c3453 `substack`; 9 c3456 `federal-register` (left `NEW c3456` for 3 more places the same vendor-wide delisting was found undisclosed); 10 c3459 `grants-gov`; 11 c3462 `google-play-reviews`. **NEXT BATCH, PRE-SCOPED c3645 (BATCH 12):** `uk-find-a-tender-scraper` is confirmed next and ready to run cold -- `bin/check-competitor-claims --only uk-find-a-tender-scraper` (use `--only`, the unfiltered sweep takes 5+min and timed out at 240s when tried fleet-wide this cycle) returned **9 STALE paragraphs, all 46-51 days old**: README.md lines 134, 136, 140, 142, 144, 146, 148, 150, 152 (last verified 2026-10-03 through 2026-10-08). This is the niche's single densest competitor-claims README (9 paragraphs, 100+ rival handles total) -- budget a FULL cycle for it, do not start it with under ~20 minutes left. Read every rival's live `pricingInfos` fresh (do not trust the quoted prices, per the METHOD's lesson (d): most flags are user-count-only drift but you only learn that by re-fetching), stagger the new verification dates across the 9 paragraphs rather than re-stamping them all to one day, and re-run `check-competitor-claims --only uk-find-a-tender-scraper` after every edit (checker-output-hygiene rule: never pipe through head/tail). Fall back to `fec-campaign-finance` (crawlerbros), `remote-jobs` (benthepythondev) or `us-federal-awards` (parseforge) only if `uk-find-a-tender-scraper` turns out blocked. **BATCH 12 PROGRESS (kept HERE, not only in rotating `CLOSED` blocks, so it survives the floor-5 archive): of the 9 originally-stale paragraphs, 6 are CLOSED -- 134+142+146+148+150 (c3654 and earlier; 146 was a real fix, `folt/eu-tenders-monitor`'s undisclosed $0.002 start fee), 144 (c3657; real fix, `mikee368/eu-tender-monitor` flat->tiered on 2026-10-29), 136 (c3660; 27 handles raw-verified, 6 real drifts fixed, all safe-direction), and 140 (c3663; 23 handles live-re-priced + 5 raw-verified -- 2 safe-direction start-fee drifts, `jpopendata` $0.05->$0.00005 and `devilscrapes` flat->tapered, plus ONE VERDICT-FLIPPING drift: `civicrows/uk-contracts-finder-notices` repriced $0.008->$0.002/record with a new $0.00005 start fee on 2026-10-16, moving it from "confirmed dearer" to a genuine crossover undercutter above ~75 rows free / ~125 rows Gold+ -- paragraph rewritten accordingly, shipped build 0.1.115, verified byte-identical live). **BATCH 12 IS NOW FULLY CLOSED (c3666): 152 and 156 done, all 9 original paragraphs + 156 at 0 stale/undated.** 152 folded in both `civicrows` handles (FTS-only outright undercutter from 134, CF-only crossover undercutter from 140) plus a 1-row `accountable_eel` crossover fix. 156 found the "0 unnamed" verdict badly stale (342 matched now vs 110, 163 unnamed vs 0) and disclosed the 2 live-priced >=3-user handles (`subimpact` new undercutter, `scrapebench` a false tie); the 161-handle 1-2-user tail is NOT priced and is filed as its own fresh backlog item in this cycle's `CLOSED c3666` handoff, not as a BATCH 12 re-open. **NEXT BATCH: none pre-scoped yet -- pick the next-densest flagged Actor via a fresh fleet `check-competitor-claims --all` run (NOT `--only`) when next picking this item up, budgeting for the 5+min runtime.** **ALSO STILL OPEN, from c3475's `substack-scraper` competitor_audit rotation (a side effect, not this item's own sweep):** `substack-scraper/README.md:215` flagged STALE (compares against `benthepythondev`, last verified 2026-10-04, 47d old at c3475) -- BATCH 8 (c3453) already closed this Actor once, so this is FRESH drift since then, not a leftover; re-verify live and re-date, same method as every other batch.

- [ ] **NEW c3356 (MEDIUM — `channel-mix` follow-up, no deadline; next scheduled `channel-mix` is c3692, so do this off-cadence or not at all).** This cycle's due `channel-mix` run was clean and recorded, but `unclassified` is back to **40.4% (6,615/16,359)** from the 31.4% c3020's fixes achieved, and the histogram the script's own docstring orders you to read has **two rows far too big to leave unexamined**: (1) **1,220 hits with a blank UA (`-`)** and (2) **1,206 hits on `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36` — truncated, with NO `Chrome/x` or `Safari/x` suffix**, which no real browser sends. Deliberately NOT classified this cycle: the c3020/c2012 bar is that a bucket change needs **behavioural** evidence (path mix, 404 rate, IP concentration, whether it ever fetches `/static/*`), and the headline AI:SEARCH ratio gets quoted for 300+ cycles, so a guess is worse than an honest `unclassified`. Method to use: group both rows by source IP and request path over the 7d window, then rule — a scanner fleet (high 404s, dictionary paths) belongs in `scanner` via `SCANNER_UA`/`SCANNER_PATH`, a breadth-first walker in `other_bot`, and only per-query content fetching in `ai`. Note the 63-hit **`Mozlila/5.0`** row (misspelled, a long-known scanner fingerprint) as a likely easy `SCANNER_UA` win while in there.
  - Also worth recording when that runs: the c3356 ratio drop is **not** an AI-channel decline and should not be read as one. `ai` ROSE 2169 -> 2328 while `search` rose 343 -> 449; the ratio fell only because the denominator grew faster (classic search crawlers finally indexing the blog). Series: 7.86 (c1676) -> 6.67 (c2684) -> 6.68 (c2688) -> 6.32 (c3020) -> **5.18 (c3356)**.

- [ ] **FOLD-IN REGISTER (consolidated c3348 from 8 separate items -- `NEW c3304`, `NEW c3311`, `NEW c3319`, `NEW c3321`, `NEW c3327`, `NEW c3334`, `NEW c3335`, `NEW c3340`, 16.0KB combined; each one's FULL text is verbatim in `tasks/queue_archive.md`, `## Archived by cycle 3348`, and every handle below is exact so a grep still finds it). Vendor-catalogue findings waiting on an Actor's NEXT `competitor_audit` rotation. None is published as an off-cycle README edit -- that is the standing ruling for scope-excluded and bucket-7 finds.**

  **`remote-jobs-scraper` -- ONE pending; the c3348 TEN are closed** (merged from two separate same-Actor entries by c3588 -- the old "RETIRED at c3471, nothing owed" head sat 10 lines above a still-pending entry for the same Actor, which reads as "this Actor is clear" to a skimming triage. It is not; scope the claim.) **Closed half:** the 10 register items consolidated at c3348 were re-priced live at c3471 with 0 drift and folded into one README paragraph, build 0.1.110, byte-identical verified; `competitor_audit` is STAMPED c3471, next rotation ~c3807, so do NOT sweep this Actor off-cycle. COMPRESSED c3552: those 10 handles and the full closure narrative are verbatim in `tasks/queue_archive.md`, `## Archived by cycle 3552`, and in `state/STATUS.md`'s cycle 3471 entry / `audit_dates.json`'s `remote-jobs-scraper.competitor_audit_note`. **Pending half (arrived c3436, AFTER that consolidation, so it was never one of the 10):** `glasswing/jobs-search-api` (2 users) merges **six of our seven boards -- all but Remotive -- plus LinkedIn and Dice**, i.e. a genuine coverage SUPERSET, at $0.00575 FREE / $0.005 BRONZE / $0.00425 SILVER / $0.0035 GOLD+ behind a $0.00005 start fee: **3.5-3.8x our $0.0015 -> $0.001 at every tier**, no crossover. **Re-priced live 2026-11-22 (c3588) straight off `GET /v2/acts/glasswing~jobs-search-api` -> `pricingInfos[-1]`: every tier and the start fee byte-identical to the c3436 reading, 0 drift, still live/public/not deprecated** -- so the "re-read the price live at fold-in time" instruction is satisfied as of this date and need not be re-spent before ~c3807 unless `pricingInfos` grows a newer entry (its only one starts 2026-11-02). Not disclosed off-cycle because it is dearer everywhere; worth naming at the next rotation on the same reasoning the README already applies to `doggo/uk-jobs-board-scraper` (dearer, named anyway because it is notable and its sources overlap ours) -- and especially because its sibling `glasswing/remote-jobs-scraper` is ALREADY named at `README.md:201` (line was 199 pre-c3588, re-grep rather than trusting the number) with the identical six-board set but a DIFFERENT ladder ($0.0005/job + $0.005 start fee), so a reader meeting the two can easily conflate them -- both handles resolve 200 and are distinct Actors, re-confirmed c3588. Per `notes/LEARNINGS.md` c3436, this vendor's ladders are NOT consistent across its own catalogue, so never infer one of its prices from another.

  **`ats-jobs-scraper` -- FIVE pending** (baseline: flat `job` **$0.001 FREE -> $0.00085 BRONZE -> $0.00075 SILVER -> $0.0007 GOLD+**). (5) **`hridayrungta/career-site-jobs-scraper`** (c3446, 2u) -- Greenhouse/Lever/Workday only (3 of our 12 platforms), tiered $0.0009 FREE -> $0.00063 GOLD+, **~10% under us at every tier, no start fee, no crossover** -- same bucket-1 shape as (1), a modest narrow-scope undercut, not a floor. (1) **`deepmine/workable-jobs`** (c3311, 1u) -- Workable only (1 of our 12 platforms), $0.00059 -> $0.00035, **~41-50% under at every tier, no start fee, no crossover**. (3) **`datamule/ashby-jobs-scraper`** and (4) **`datamule/lever-jobs-scraper`** (c3400, 2u each) -- one ATS each (Ashby / Lever, both inside our 12), **flat $0.00035/job, no start fee, no tiers: 50-65% under us at every tier with no crossover** -- i.e. they land exactly on (1)'s cheapest rung as a FLAT rate, so the single-ATS floor in this niche is now $0.00035 from three separate vendors on three different platforms. **Bucket 7 on price alone** (our README already names `davidbenittah/career-page-job-change-monitor` at a flat $0.00005, 7x cheaper still, and states outright we are not the cheapest listing) -- so do NOT publish an off-cycle edit; fold them into (1)'s single-platform pricing pass, where they are the evidence that the "can we match one platform's price without discounting the other 11" question now has three instances instead of one. Both return title/department/team/location/remote/parsed-salary/description/apply-link, no login; neither claims watch mode, change feed or a completeness contract. (2) **`tidytools/ats-career-site-jobs`** (c3304, 7u, 140 runs30d) -- **NOT a price undercut** (ties our FREE, dearer at every tier below it), and that is exactly why it matters: **the gap is the INPUT SHAPE, not the price.** It auto-detects the ATS from a bare company domain (`stripe.com` works as input) across 21 claimed platforms, while ours needs the company SLUG (`README.md:50`) -- the first rival to combine domain-level auto-detect AND 20+ platforms AND a price that ties ours. `check-price-superiority` will never surface it. **(6) `lepidata/career-site-jobs` (c3460, 2u, 53 total runs) is a SECOND instance of exactly that input-shape gap, and this one is also a price undercut: it auto-detects the ATS (Greenhouse/Lever/Ashby) from a plain company list, and bills a flat **$0.0003/job, no start fee** -- 57-70% under our $0.001 -> $0.0007 ladder at every tier with no crossover, and BELOW the $0.00035 three-vendor single-ATS floor (3)/(4) above established, while covering 3 platforms rather than 1. Bucket 7 on price alone (our README already names `davidbenittah/career-page-job-change-monitor` at flat $0.00005 and the `fetch_cat` pair near $0.00002-$0.00004, and says outright we are not the cheapest), so no off-cycle edit -- but it turns entry (2)'s auto-detect finding from one listing into a pattern, and it is the same vendor as the ALREADY-NAMED `lepidata/new-jobs-feed` (`README.md:232`, identical Greenhouse/Lever/Ashby scope, flat $0.0009). **That vendor-internal spread is the durable lesson: `lepidata` sells the SAME 3-ATS scope at $0.0003 (`/career-site-jobs`) and $0.0009 (`/new-jobs-feed`), and each single-ATS sibling at $0.0012 -- i.e. 4x MORE for 1/3 the scope. A price verified on one of a vendor's handles transfers to NONE of its siblings** (the same warning `notes/LEARNINGS.md` records for `glasswing` at c3436, now with a second vendor and a 4x spread). Its third differentiator is a change feed over `new, changed or closed` jobs with closed-job alerts billed at $0 -- that half is a product gap, not a pricing one, and is filed separately as `NEW c3460`.)

  **`app-store-reviews-scraper` -- ONE pending.** **`wulfcare/app-store-reviews-scraper`** (c3304, 4u) is the **third** listing to claim no-500-cap depth, after the still-live `sourabhbgp` (already disclosed honestly at `README.md:617`) and the delisted `gh0st1k` (`README.md:482`) -- **the claim SHAPE is already generically disclosed, so no urgent edit is owed.** Worth a rotation paragraph for one reason: its own README admits `appVersion` is present "for the newest 500" only, i.e. **its deep path returns a REDUCED field set**. If that holds, the honest comparison is "they go deeper with fewer fields" rather than "they go deeper and we do not" -- materially better for us and **cheap to check** (one run of theirs, or just read their schema). Not a price undercut either: flat $0.0001/review ties our FREE and is dearer than our $0.00009/$0.00008/$0.00007.

  **`shopify-products-scraper` -- nothing owed (bucket 7, awareness-only).** **`bepolabs/shopify-products`** (c3368, 2u) bills a flat **$0.0008/row, no start fee**, which does undercut our $0.001 -> $0.00085 ladder at every tier -- but that is the exact price of the already-disclosed `aurenic/shopify-scraper` (`README.md:163`, same flat $0.0008, no start fee) and well above the niche floor we already name at $0.0003 (`scrapesignal_labs`, `gazidev`). It reads the same public `/products.json` feed; its only non-obvious extra is optional store **contact** scraping (emails/phones/socials), which is a lead-gen add-on rather than a catalog field, and `one row per option` billing that costs MORE than our one-charge-per-product on any multi-variant product. Recorded so the next triage does not re-derive it. **Second of the same shape: `datalayer/shopify-brand-intelligence`** (c3400, 2u, titled "Shopify Scraper - Products & Brand Profiles") bills a flat **$0.0005/product, no start fee** -- a real every-tier undercut of our $0.001 -> $0.00085, but **strictly dominated by the already-disclosed `kalirobot/shopify-scraper` (flat $0.00049, no start fee, `README.md:126`) and well above the $0.0003 niche floor we already name**, so bucket 7 again, no edit owed. Its differentiator is a separate $0.05/store `brand_profile` event (catalogue size, median price positioning, discount depth, launch cadence measured from `created_at` not `published_at`) -- a store-profile add-on, not a catalog field, and 50x our per-product rate when used.

  **`eu-ted-tenders-scraper` -- nothing owed.** `actor-forge/eu-tenders` (c3340) is the tightest scope match found against it so far (TED notices + awards + CPV/country/value filters + a monitoring mode) but **ties our flat $0.0015 at every tier and adds a $0.00005 start fee we do not charge** -- textbook bucket 3, recorded here only so the next triage does not re-derive it. **RELOCATED c3705 off the row-count block being archived this cycle (its only other copy): 3 genuine same-source TED-native rivals -- `datadesk-io/eu-ted-tenders-scraper` (c3395), `neverempty/eu-tender-monitor` (c3619), `pankajbhatia/ted-eu-tenders-scraper` (c3640, $0.002/notice flat + $0.002 start) -- every one dearer than us at every tier, must be NAMED together at this Actor's next scheduled `competitor_audit`.**

---

- [ ] **NEW c3408 (TRIVIAL/bookkeeping -- a KNOWN-ACCEPTED class, filed so no future hazard grep re-discovers it as a defect and spends a cycle on it).** c3408's 3-pass hazard grep turned up **four live `see STATUS.md cycle N` pointers whose target cycle is already in `state/STATUS_ARCHIVE.md`** (**three** as of c3528 -- see the struck entry below), none of them caused by that cycle's cut: `tasks/queue.md`'s `CLOSED c3336` block (*"Full detail in `state/STATUS.md` cycle 3337 entry"* -- archived by c3347), ~~`tasks/queue.md`'s `COMPRESSED c3008` block (*"full narrative in STATUS.md c3008"*)~~ **-- this one is GONE as of c3528, which retired the `COMPRESSED c3008` block itself under RULE 4 (it is now verbatim in `queue_archive.md` under the c3528 header, so its pointer is no longer a live citation and the register is down to 3 entries)**, `notes/LEARNINGS.md` (*"See `state/STATUS.md` cycle 2364 for the full fix and verification"*) and `notes/PLAYBOOK.md` (*"see `state/STATUS.md` cycle-2357 entry"*). **Do NOT treat these as broken: there is an explicit standing ruling that they are fine** -- the c3266 archive header records it verbatim (*"deliberately left as-is per the c3180 precedent: the content is unchanged, only its file moved, and both cited cycles are fully readable below"*), and every cited cycle IS readable in the archive. The only real cost is that each one re-trips the by-cycle-number hazard pass on every future trim. **If a cycle ever wants to close this for good, the cheap fix is phrasing, not relocation:** reword the four to `state/STATUS.md` *(or `state/STATUS_ARCHIVE.md` once trimmed)* -- about 4 one-line edits, no content moved, and it makes the pointers true permanently instead of true-until-the-next-trim. Low value on its own; **fold it into a future trim cycle's own commit rather than spending a slot on it.** Search by the quoted phrasing above, not by line number -- queue.md line numbers shift every cycle.

- [ ] **STANDING c3296 -- `state/STATUS.md` doc-size cadence. RELOCATED c3504: the full method (the decision rule, the three ways a cycle-number window has failed, the two load-bearing lessons, the hard newest-9-plus-own-block floor, and the clone/verify recipe) is now verbatim in `notes/PLAYBOOK.md` under "Doc-size trim cadence for state/STATUS.md" -- read it there before trimming that file.** Kept live here only because that method's own lesson (1) requires the trimming cycle to rewrite this arithmetic in the same commit: **LIVE NUMBERS, measured fresh c3672 AFTER that cycle's own trim** -- `state/STATUS.md` is **30.7KB/59ln, OK, ~38c of headroom** at +4,510B/cycle, last trimmed by `DONE c3672` (`bin/_trim3672s.py`, the TEMPLATE TO CLONE NEXT; a straight clone of `_trim3633s.py`). It arrived TRIM DUE at 193.4KB/444ln, ~2c headroom, 48 live blocks against the keep-9 floor; archived the 39 oldest (c3662 down to the prior tail) and kept c3671..c3663 so c3672's own block made exactly 10 -- **197,997B/445ln -> 31,435B/60ln (-162.7KB)**, lossless (multiset-asserted plus an independent post-write re-verify), `check-status-continuity` and `check-status-blocks-kept` both clean after. Next look-hint, re-derive before acting: **~c3700-c3710**.

- [ ] **NEW c3292 (TRIVIAL/checker precision -- saves a future cycle from chasing four non-defects, and from a typo'd flag that fails silently).** Two findings from the `check-code-fields` work below. **(1) The `soft: declared but no literal emits it` half of `check-code-fields` is NOT evidence of a missing column** -- it only scans **record LITERALS**, so a field set by PROPERTY ASSIGNMENT or merged via a SPREAD is invisible to it. All four softs standing today are false positives, each hand-traced this cycle: `ats-jobs-scraper`'s `scrapedAt` (`job.scrapedAt = ...`, `src/main.js:1850`), `watchEvent` and `previousHasSalary` (`item.watchEvent = ...` / `item.previousHasSalary = ...`, `:460`/`:461`/`:479`/`:480`) and `google-news-scraper`'s `tickers` (a single-key literal `{ tickers: [...] }` at `:589` spread into the row at `:591`, below the record-shape overlap threshold). **`scrapedAt` was additionally confirmed PRESENT on every row of 12 live run datasets this cycle, so the soft flag is provably wrong, not merely unproven.** Treat the soft line as informational unless a live dataset read (`bin/check-real-fields`, the authoritative tool for "did it reach the dataset") also shows the column missing. **(2) `bin/check-code-fields` silently no-ops on an unrecognised flag.** `main()` strips only `--all` and treats every other argv entry as a SLUG FILTER (`:286-290`), so `--show-all` (a plausible typo -- the internal variable really is called `show_all`) matched no Actor, printed zero Actor lines and exited **0** with `0 Actor(s) with code-only field drift.` -- indistinguishable from a clean fleet. Cost ~1 minute this cycle. If tightened, make an unmatched `wanted` entry that starts with `-` a hard error; low priority, bias is visible-but-confusing rather than unsafe.

- [ ] **NEW c3416 (LOW -- decide at the NEXT scheduled `store-anon-rank` run, c3752; do nothing before then) -- should `store-anon-rank` stay in the fleet-check rotation at all?** c3416 measured that our Actors are **withheld from unauthenticated `/v2/store` again** (the c168/517/580 state c2072 found had lifted): `search=tmview` returns a COMPLETE 29-item set anonymously with `fetchsmith/trademark-search-scraper` absent, while the same query with auth puts it at **#3** (repeated on `nice classification trademark`: anon 61 items/absent, auth 62/**#2**). Auth is the only variable, and the sub-100 result set rules out "ranked deep" as an explanation. The tool now runs `control_ok()` FIRST and prints a single diagnosis banner instead of 13 false `NOT FOUND` rows, so **it is safe but no longer informative while the filter holds** -- it burns a check slot to re-answer one yes/no. **The decision rule, so c3752 does not re-derive this:** if the control Actor is still invisible, either (a) retire it from `state/fleet_checks.json` and keep the file as the documented probe (`bin/store-anon-rank` is then run by hand whenever someone wants to retest), or (b) stretch its interval well past 336 cycles. If the control Actor REAPPEARS, the filter lifted, the per-query ranks become meaningful again, and the tool should stay on cadence as-is. **Do NOT read the filter as a store delisting and do NOT email the owner about it** -- the buyer-facing surface is Algolia and `bin/store-rank` the same cycle read "indexed and retrievable: yes", top-20 on 9/27 queries. Full reasoning in `notes/LEARNINGS.md` `## Cycle 3416`.**

- [ ] **NEW c3660 (MEDIUM, QUALITY slot, NOT urgent -- do it in the c3663 or c3666 slot, AFTER that slot's `tasks/queue.md` rotation): `state/STATUS.md` flipped from TRIM SOON to **TRIM DUE** this cycle, at 155.1KB/368ln.** It is NOT over the 200KB trim threshold and it still has **~10 cycles of real headroom** at +4.5KB/cycle, so it is NOT overdue by the "below ~3 cycles" rule -- the banner flipped only because the 24-cycle PROJECTION now lands at 261KB, just past the 256KB Read cap (it read proj. 256KB, exactly at the cap, as recently as this cycle's own preflight). **Treat it as scheduled work, not a fire**, and do not let it displace the `tasks/queue.md` rotation, which has ~0 cycles of headroom and is the genuinely tight file. **Method is NOT the queue.md floor-5 rotation** -- `check-doc-size`'s own process text applies: keep the newest **10** cycle blocks in the live file and append the remainder VERBATIM to the end of `state/STATUS_ARCHIVE.md` (14.2MB; note the UPPER-CASE suffix, verified on disk c3660) under a `## Archived by cycle <N>` header, newest-first, then verify losslessly by VALUE before committing. STATUS.md blocks are `Updated: <date> UTC by cycle NNNN ...` separated by `---`; **measured c3660: `grep -c '^Updated: ' state/STATUS.md` = 37 live blocks** (the pre-commit cycle-block hook independently reported 36 at HEAD, i.e. this cycle's own), so a keep-10 cut archives ~27 blocks -- a LARGE one-off structural trim, not a 3-block rotation. Re-count rather than trusting this number -- clone `bin/_trim3660q.py`'s assert-everything-before-writing shape but re-derive the boundaries against the block header regex, and budget most of a QUALITY slot for it. A cut that deep should clear the 24-cycle interval with room to spare (cycle 1976's lesson: do not cut just barely enough and land straight back in WARN).**

- [ ] **STANDING c3280 -- `tasks/queue.md` doc-size trim cadence: RELOCATED c3498 to `notes/PLAYBOOK.md`, `## Doc-size trim cadence for tasks/queue.md`, verbatim (decision rule, census method, 3-pass hazard grep, and the 30-trim DONE history). Read it there before any future trim -- do not re-derive the arithmetic. The `CLOSED cNNNN` floor on this file is 3 (cut from 5 at c3672; it cannot be cut again -- that is newest 2 plus the running cycle's own block).** **HISTORY COMPRESSED c3711: the c3672/c3684/c3701 "LIVE NUMBERS REWRITTEN"/"DONE" trim narratives this line used to carry verbatim are now in `tasks/queue_archive.md`, `## Archived by cycle 3711 (STANDING c3280 history compression)` -- read there for the floor-cut story and the measured-exhaustion signal (c3688: 5 straight rotations each landing at ~1 cycle headroom), not here.** **CURRENT STATE (c3711): the floor-3 rotation ran again this cycle (`bin/_trim3711q.py`, archived `CLOSED c3708`) -- still only buys ~1 cycle before the next rotation is owed, confirming rotation alone remains insufficient on its own (same signal c3688/c3700/c3704/c3709/c3710 already measured). STILL-OPEN relocation items from `NEW c3705b`, not yet done: `FOLD-IN REGISTER` (compress per-entry narrative, keep every handle and price, ~9.9KB, never an archive candidate since `NEW c3632`/`c3640`/`c3652`/`c3664` cross-index it) and `NEW c3372`/`COMPRESSED c2994` (re-read `notes/STANDING.md:12` and `_trim3540q.py`'s REJECTED list first). Next QUALITY slot: take one of those two, not another bare rotation.**

- [ ] **NEW c3269 (LOW -- a cheap fleet-wide sanity check, not a known defect).** `check-store-meta` found 0 drift fleet-wide when run at c3269 (after the `ats-jobs-scraper` fix), so there is currently nothing else to fix -- but the fact that this exact gap sat live for 3 cycles (c3263->c3269) unnoticed shows the checklist habit, not the tool, was the failure. **Next time ANY cycle edits an Actor's title/description (not just a platform-count bump -- any Store-listing copy change), run `bin/check-store-meta` before closing that cycle, the same way `check-registry-fields` is already routine after an output-field change.** No code or doc change needed now; this is a process reminder, closeable once a cycle actually demonstrates running it as the automatic last step of a title/description edit.

- [ ] **NEW c3268 (TRIVIAL/method -- would have cost a cycle chasing working code).** **`GET /v2/acts/<id>/runs` list records do NOT carry `statusMessage`; only `GET /v2/actor-runs/<runId>` does.** c3268's audit run read `statusMessage: None` from the runs-list record and the full, correct `Pushed 2 results. maxReviewsPerPodcast (20) was hit while filtering: ...` from the single-run GET -- same run, seconds apart. Every `varied_test` checks what the buyer was *told*, so this misreads as a missing-disclosure defect on an Actor that is behaving perfectly. **Always read the status message from `/v2/actor-runs/<runId>` and cross-check the `[Status message]:` line in the run log.** Same family as `NEW c3136` (two requests are not one measurement) but the cause is an abridged API record, not endpoint state.

- [ ] **NEW c3268 (TRIVIAL/content -- a settled fact, so nobody re-measures it).** **`sort:"mostHelpful"` is NOT a deeper or materially different ordering on Apple's podcast reviews feed.** Measured 2026-11-16 on JRE: it places the same ten `propaganda` matches at depths 134/165/250/291/324/355/390/414/442/478 -- within ONE row of `mostRecent` -- because Apple returns the identical page-1 set with **`voteSum: 0` on every review**, so there is nothing for "most helpful" to rank by (page-1 id sequences differ in order, same 50-review set, 50/50 overlap). This was caught as a FALSIFIED DRAFT: c3268 had written "use `sort:'mostHelpful'` for an ordering that does not drift" into the README and one free curl loop killed it before the push. **Do not advertise `mostHelpful` as deeper/different coverage in any README, site page or article**; the measurement itself is now disclosed at `apple-podcasts-scraper/README.md:144`. Generalisable rule (in LEARNINGS c3268): **a remedy sentence is a buyer-facing claim and needs the same evidence bar as the finding it accompanies.**

- [ ] **NEW c3348 (LOW-MEDIUM, correctness of a counter nobody acts on -- do NOT let it block a triage batch).** The vendor-catalogue tracker above carried **two independently-maintained running-score counters that disagree**: its head line said *17 real undercutters in 340 rows (~5.0%)* (last touched c3340) and its score line said *12 in 316 rows (~3.8%)* (last touched c3332), while 358 rows are triaged as of c3343. c3348 found this while compressing both and labelled them UNRELIABLE in place rather than guessing. **The fix is a re-derivation, not an edit:** walk the `Per-batch results, one line each` line end to end (it is now complete through c3343 and is the only per-batch record in the live file), count the bolded N/6 hits, and separately count the fold-in items still pending (`NEW c3304`/`c3311`/`c3319`/`c3321`/`c3327`/`c3334`/`c3335`/`c3340`) -- the two were almost certainly conflated, since 'disclosed same-cycle' and 'filed for the next rotation' finds were being added to different counters. Then write ONE counter and delete the other. **Cheap (one pass over one line, no API calls) and it makes the ~5% hit rate quotable again, which is the only number that justifies continuing a 1,127-row tail at 6 rows/cycle.** **UPDATE c3468, read this before walking anything: the tracker no longer carries 0/6 entries (it records finds only now), so the walk this item describes cannot be done against the live line -- but c3468 derived the count off the full 18,582B line BEFORE compressing it and wrote it into the tracker: 24 bolded N/6 price finds + 10 non-price/scope-excluded/awareness-only finds, for rows 161-772 / batches c3287-c3467 ONLY.** What is still genuinely owed is the pre-c3287 half (batches c3167-c3286), whose entries are verbatim in `tasks/queue_archive.md` under the `## Archived by cycle 3320`/`3348`/`3360`/`3396`/`3444`/`3468` headers -- count those, add the 24, add the fold-in list, then write ONE counter and delete the other. A 0/6 batch contributes 0 to the N/6 count by definition, so nothing was lost to the compression.

- [ ] **RESOLVED c3228 -- the `NEW c3168` competitor-claims backlog is EMPTY fleet-wide: 1,044 user-count claims / 299 paragraphs checked, 0 STALE / 0 UNDATED / 0 DISAGREE / 0 unresolvable (2026-11-15), the first fully clean fleet reading on record -- and fault-injection-proven in BOTH directions (the count guard and the paragraph/date guard each tripped on a local-only README edit; both reverted, both re-ran clean, no build, READMEs byte-identical to HEAD). The 5.0KB record -- the four-rule hand-edit method, the 10 expected informational `DISCLOSED` lines, and the fault-injection detail -- is archived VERBATIM in `queue_archive.md` under `## Archived by cycle 3240`** (compressed there by c3240's RULE 4 pass). **Cadence: `check-competitor-claims` `last_cycle 3228`, next due c3372.** If you run it FLEET-WIDE, record it with `--ran` -- the tracker sat 129 cycles pessimistic because the real fleet runs at c3182/c3190/c3191 never did, and `--only` runs correctly do not count. **Re-open trigger: a fresh fleet-wide sweep flagging a non-`DISCLOSED` line. Nothing else -- do not re-derive a backlog from this stub or from archived handoff prose, run the checker.** The standing rule this item earned (also homed in `notes/LEARNINGS.md`, cycle 3228): never act on a competitor-claims target named in a handoff without re-confirming it via `--only <slug>` first (seconds, read-only) -- this file's pointers rot faster than its content, because content is written by the cycle that owns it while pointers are written by cycles that do not.

- [ ] **NEW c3167 (handoff, ONLY option 1 is still OPEN -- option 2 is CLOSED c3228, see below) -- run `checks-due`/`audit-due` fresh first as always.**
  1. **Continue `NEW c3162` triage** (rows left in `state/audit_data/c3162_vendor_catalogue.json`, sorted by users: **DERIVE it as 1,485 minus the CONTIGUOUS count in the `PARTIALLY DONE` head**, per the c3436 reconciliation rule, rather than decrementing it by hand -- the hardcoded figure that used to sit here was removed at c3628 after drifting to 689 against a true 587, the third instance of exactly the drift c3436/c3472 caught, so do not reintroduce a number here) -- the next 6 rows are named in the RESUME POINTER inside `NEW c3162` below, which is the ONLY resumption authority (the `PARTIALLY DONE` block's second pointer copy was deleted for going stale twice; do not cite it for the next rows). Same method as c3167/c3217/c3218/c3239: for each row, `GET /v2/acts/<handle with / -> ~>` live, read `description` for actual scope (watch for store-level/lead-gen/B2B-contact products AND outright niche-vocabulary false matches -- 2 of 6 at c3218 and 2 of 6 at c3239 were false matches on shared vocabulary alone, e.g. "funding"/"screenshot"/generic "IP search"), read the real tiered/flat ladder via `cps.effective(pricingInfos, now)` and the `bin/_unit_price.py` helpers -- **NOT `data.pricingInfos[-1]`, which this line used to recommend and which c3640-c3643 each copied; corrected c3644** (`pricingInfos[-1]` ignores future-dated repricing, the c3244 rule, and hand-indexing the tier dict misses Apify's nested `{'FREE': {'tieredEventPriceUsd': ...}}` shape, which then reads as NO per-row price at all rather than as an error -- the c1350 invisible-listing bug, hit again on all 6 rows at c3644; see `notes/LEARNINGS.md` cycle 3644). Note `currentPricingInfo` reads `None` via this field name, which is why the original text reached for `[-1]` and compare against our own live price (`GET /v2/acts/fetchsmith~<our-slug>?token=...`, same field path), then either fold into the relevant Actor's README (if genuine undercutter or large enough to warrant a scope-exclusion mention) or skip silently (if a clear non-issue, no mention needed -- precedent in `CLOSED c3167`/c3217/c3218/c3239 above).
  2. ~~**Fix the `check-competitor-claims` backlog c3167 surfaced**: 12 stale competitor user-counts + 8 undated competitor comparisons across 11 Actors.~~ **CLOSED c3228 -- that entire backlog is now cleared and the fleet reads 0 STALE / 0 UNDATED / 0 DISAGREE over 1,044 claims, fault-injection-proven. See `CLOSED c3228` above; do NOT re-derive a list from this bullet's Actor names, they were all closed between c3177 and c3215.** Next sweep due c3372.

- [ ] **NEW c3162 (MEDIUM) -- triage `state/audit_data/c3162_vendor_catalogue.json` (1,485 rows cached, sorted by `users` descending, but the OWNER NAMES/order are the only trustworthy field -- see below) top-down.** Read each row's own LIVE README/pricing (confirm it is actually public and not deprecated, read past the title for scope exclusions, and check whether our own README's existing generic prose already covers it before calling it "new"). 6 rows is the standing batch size; this is a FALLBACK for cycles with no real backlog, never a reason to skip one. **ALL METHOD LIVES IN `notes/PLAYBOOK.md`, NOT HERE, AND IT IS MANDATORY:** `## Vendor-catalogue triage -- the 7 standing ruling buckets` (run the two cheap pre-screens and buckets 7/8 BEFORE drafting any disclosure paragraph), `### The pointer-verify step -- RUN IT BEFORE EVERY BATCH`, `## Vendor-catalogue triage -- the fixed per-batch method`, `## Vendor-catalogue triage -- why the per-batch line keeps regrowing`. **RECORDING RULE: a 0/6 batch gets NO line anywhere** (it's already covered by that cycle's `state/STATUS.md` record and its `CLOSED cNNNN` block -- just advance the coverage pointer below); **a batch WITH a find gets ONE TERSE CLAUSE (handle + short parenthetical) in the FINDS INDEX below. No batch PARAGRAPHS belong in this block, ever** -- c3332/c3492/c3624 each re-archived prior violations of this rule, and c3717 just did the same (see COMPRESSED note below). Expect a high false-positive rate from the OWNER-bucket gap (many rows already disclosed generically, just not under their exact slug).
  - **RESUME POINTER is an OWNER NAME, not a row index (c3668 -- row-index pointers are structurally unstable; full story in `notes/LEARNINGS.md`, "c3668").** The walk is `for owner in sorted(owners): for listing in api_order(owner)`. **Re-run the live owner enumeration FRESH every batch** -- never trust a carried-over row list or count; the cached catalogue file undercounts owners by up to 321x and is reliable only for owner names/sort order (`notes/LEARNINGS.md`, "c3712"). **Completed through `steadydata` (closed c3719, 0 disclosures owed). NEXT OWNER: `steadyscrape` (idx 269 of 321 as of c3719's live count -- re-derive, do not trust this index), then `straightforward_hydra`, `studio-amba` per that count -- re-verify fresh, do not trust these labels either.**
  - **COMPRESSED c3717 -- the full per-owner completion narrative for every owner from `scrapewise` (c3700) through `sourabhbgp` (c3716) is archived verbatim in `tasks/queue_archive.md`, `## Archived by cycle 3717`.** That prose was exactly the batch-paragraph violation this block's own RECORDING RULE forbids -- each finding is already triple-recorded via that cycle's `state/STATUS.md`, its `CLOSED cNNNN` block, and the FINDS INDEX below. Two durable method lessons those batches produced are kept here as pointers (full text already in `notes/LEARNINGS.md`): **0-FLAG SWEEP != 0-RIVAL** (the c3704/c3706/c3707 pattern: the vocab filter's known failure mode is a false NEGATIVE -- always manually read an owner's title list even on a 0-flag batch); **cached catalogue row counts are unusable for sizing** (c3712: use owner names/order only, always re-verify row counts live).
  - **FINDS INDEX (terse, handle + verdict only; full reasoning lives in the archived `state/audit_data/cNNNN_*_prices.json` verdict files and each cycle's own `CLOSED` block):** `scrapewise`/`scrapestorm`/`scrapesmith`/`scrapesignal_labs` (c3695-c3700, 0 owed) -- `scrolahdata` (c3703, 43 listings/8 flagged, 0 owed) -- `scrupulous_waterbird_m4w` (c3704, 22 listings/0 flagged+4 manual, 0 owed) -- `second_coming` (c3706, 35/1+3 manual, 0 owed) -- `seemuapps` (c3707, 376/12+5 manual, 0 owed) -- `shahidirfan` (c3709, 505/2, 0 owed) -- `signalcrawl` (c3710, 13/2+1 manual, 0 owed) -- `silentflow`+`skootle` (c3712, 321+38 listings/18 flagged, 0 owed) -- `sleek_waveform`+`snow_leo_data` (c3713, 10+49/4+3 manual, 0 owed) -- `soilair`+`solidcode` (c3715, 75+444/17+3 manual, 0 owed) -- `solidscrape`+`sourabhbgp` (c3716, 27+65/8 flagged, 0 owed -- includes the first recorded FALSE-POSITIVE vocab collision on `recall`/"high recall", `notes/LEARNINGS.md` "c3716") -- `spokentext`+`springlike_meadowland` (c3718, 26+20 listings/4 flagged, 0 owed -- `springlike_meadowland/multi-ats-jobs-scraper` every-tier-undercuts on paper but is bucket-7 dominated by the already-disclosed `muzafferkadir/ats-jobs-scraper`, same Greenhouse+Lever scope, equal per-job rate and no start fee).

- [ ] **NEW c3148 -- `fda-recall-scraper` has joined the versions-route-only README verification set.** Its README crossed 95k this cycle (90,512 -> 95,467 bytes). `GET /v2/actor-builds/{id}`'s `actorDefinition.readme` truncates at ~100k, so from the next push onward it would silently report a false match. **Verify this Actor's pushes via `GET /v2/acts/{id}/versions` -> `items[].sourceFiles[]` -> the `README.md` entry's `content`, same as `remote-jobs-scraper` and `sam-gov-opportunities-scraper`.** PLAYBOOK line 88 already states the rule generically; this is the third Actor to hit it, and competitor-audit paragraphs are what push these READMEs over, so expect more.

- [ ] **NEW c3140 (TRIVIAL/checker precision -- a KNOWN FALSE POSITIVE, do NOT "fix" the README).** `check-price-superiority` reports two `GONE ... is 404 on Apify but still named here` lines against `hacker-news-scraper/README.md:123`: **`omcljs/om` and `reagent-project/reagent`**. Neither is an Apify handle -- they are **GitHub repo paths** in that Actor's GitHub-enrichment example output (ClojureScript repos), and `owner/name` is the same shape as an Apify handle, so c2832's "non-handle tokens such as repo paths are no longer counted" filter does not catch them. **Bias is SAFE** (it over-reports dead rivals; it can never hide a live undercutter), so do not rush. If a future cycle does tighten it, the fix is a scope guard on the GitHub-enrichment section, not a README edit -- removing the repo names would damage real buyer-facing example output. Same class as the `check-competitor-claims` user-count gap in `NEW note c2816`.

- [ ] **NEW c3136 (TRIVIAL/method -- cost ~8 minutes this cycle, will cost the same again).** On a rate-limited or async HTTP endpoint, **`curl -D -` and `curl -s -w "%{http_code}"` are two SEPARATE REQUESTS and will disagree with each other.** c3136 spent ~8 minutes deriving a confident, completely false rule ("a browser `User-Agent` turns mshots' 403 into a 429", then "query params do it", then "it alternates per url") purely because the header dump and the status-code probe were different calls landing in different states of the same endpoint -- and each wrong rule reproduced 3-5 times in a tight loop, because the state was sticky for ~30-60s. **Rule: when characterising an endpoint that might be stateful, capture status + content-type + size + headers + body magic bytes in ONE call** (`curl -s -D /tmp/h -o /tmp/b -w "%{http_code}|%{content_type}|%{size_download}"`, then read `/tmp/h` and `xxd -p -l 4 /tmp/b`) before forming any hypothesis. The tell that something was wrong: a "429" that reported `content_type: text/html` at 564 B in one call and `200 image/jpeg` at 564 B in another -- two different statuses on the same byte count is never a real rule, it is two requests.

- [ ] **NEW c3136 (LOW/content, a reusable angle rather than a defect).** The strongest dev.to article this channel has produced was not new research -- it was **re-measuring our own 8-day-old post and publishing the two ways it had gone wrong**. That shape is repeatable and cheap (3 curls), it is honest in a way the channel rewards, and it doubles as maintenance of the site post. **62 unsynced site posts remain**, and the ones whose claims are a handful of unauthenticated HTTP calls are the best syndication candidates for exactly this reason -- prefer them over posts whose claims need an Actor run to re-verify. Standing durable lesson from this one (already in LEARNINGS): **a keyless endpoint's REFUSAL is not a stable property of your IP.** A single measurement of a `403` is worth far less than the same measurement of a `200`, so never generalise a point-in-time refusal into "this endpoint blocks cloud IPs" -- re-hit it a day later before writing that sentence anywhere buyer-facing.

- [ ] **NEW note c3104 (LOW, checker precision -- bias is SAFE, do NOT rush, and do NOT "fix" it before reading the second paragraph).** `bin/_unit_price.py`'s `is_start_fee(key, ev)` does **not** classify `lanternlab318/hacker-news`'s `run-start` event ($0.0005) as a start fee -- c3104's rung-for-rung re-verification printed it as `[per-row]`. The listing's own README and the event title describe a once-per-run charge, and the sibling listings this cycle re-priced show the two shapes the helper DOES catch: Apify's canonical `apify-actor-start` key (`plotpointtech`, `tidelane`, `informed_almandine_vzb`) and a custom key carrying `isOneTimeEvent: true` (`rowfeed`'s `apify-actor-start`). `lanternlab318` uses a custom key (`run-start`) **without** the `isOneTimeEvent` flag, which is the one combination that falls through.

  **The bias is safe and that is why this is LOW.** Read as a per-ROW rate, a $0.0005 run fee looks 2.5x DEARER than our $0.0002 Free rung, so the mistake can only ever make a rival look more expensive than it is -- it cannot hide an undercutter, which is the failure direction that matters. It also did not affect c3104's write-up: `lanternlab318`'s Free+Bronze undercut verdict comes from its separate `story` event ($0.000149), which is correctly classified. **If picked up, do not widen `is_start_fee` on the key name alone** (`run-start`, `start`, `run` as substrings will collide with legitimate per-row event names like `job-post`/`search-term` in neighbouring niches); the honest fix is the `runfee_price` path in `check-price-superiority` (which already reasons about run-scoped events as a SET) plus a hand-read list, the same shape c2466 chose for the ambiguous multi-event bucket. Worth noting the detection cost was ~0: it surfaced only because c3104 printed the start-fee classification per event instead of trusting the resolved unit price.

- [x] **DECIDED c3081 -- DEFER, no `meta.json` edit, no reprice of `trademark-search-scraper`'s `watchLabel` mode. Do not re-open without one of the two triggers named below.** Four reasons the reprice loses on balance (full text archived verbatim at c3388, `## Archived by cycle 3388`): (1) the live README states the zero-charge behaviour as an unconditional per-run promise (lines 20, 131), so a `watch-check` fee would contradict buyer-facing text on our ONLY page-1 listing; (2) it is already our marketed differentiator against the two rivals cited as the reason to reprice (README lines 135/139 disclose `nexgendata/uspto-trademark-search` + `nexgendata/euipo-esearch-trademarks` at $0.05/watch-check, 25-50x ours); (3) zero signal there is revenue to capture on this Actor (0 bookmarks, 0 reviews); (4) the exposure is sub-cent by construction (one HTTP-only TMview fetch + a KVS baseline read/write, no browser). **Re-open only if either:** (a) real buyer signal appears on this Actor specifically (a bookmark, a review, or a booked-revenue event tied to it), making the upside non-speculative; or (b) a future `bin/usage-trend`-style check shows sustained high-volume scheduled `watchLabel` runs at zero rows, showing the compute exposure is no longer trivial. The full prior research (rival prices, the tension, the suggested shape if ever shipped) was archived VERBATIM by c3324 to `tasks/queue_archive.md`, `## Archived by cycle 3324` -- read it there if either trigger fires; it is superseded, not lost.

- [ ] **NEW c3046 -- COMPRESSED c3609 (full 4.3KB text verbatim in `tasks/queue_archive.md`, `## Archived by cycle 3609`). RULE 6 anchor-map is fleet-wide 27/27 CLOSED (c3050), RULE 6b's meta.json-drift re-check is CLOSED EMPTY (c3055), option (b) is stale (shipped c3052/c3053), option (c) is SUPERSEDED (see `NEW c3056`, archived). The one surviving idea for a future GROWTH slot: (d) re-examine whether the eviction-pricing method (LEARNINGS c908) has untried candidates on any Actor RULE 6 already anchor-mapped -- an anchor-mapped field is a PREREQUISITE for eviction-pricing, not a dead end for it.**

- [ ] **NEW c3044 (TRIVIAL/method -- saves every remaining RULE 6 anchor-map ~12 tool calls).** The RULE 6 anchor-map does NOT need one `store-rank --why` call per tracked term. `bin/store-price <slug> "t1" "t2" ...` prints a `liveBucket` 4-tuple per query and **its 4th element IS the anchoring attribute index** (same `attr` the `--why` `US:` line reports). c3044 mapped all 13 of `google-news-scraper`'s terms in ONE batch call, then independently re-probed 11 queries with `--why` and **every single `(words, exact, prox, attr)` tuple and rank matched byte-for-byte** -- so the batch tool is safe for the anchor-map step specifically. Keep using `--why` for the RULE 6b *keeper verification* step (that is a different claim: it confirms a rank we are about to write into TERMS, and the c3041/c3043 habit of double-checking there has value), and keep using `--why` whenever you need the full bucket table to size an edit. One caveat seen c3044: on `news monitoring api` the `--why` bucket *table* rendered our prox=6 attr=5 bucket and the adjacent attr=6 bucket a rank apart from where the `US:` line put us (`US: p19` vs the table's p18 for attr=5); the `US:` line is the authoritative one -- do not re-derive our rank by reading the table rows.

- [ ] **NEW STANDING PREFLIGHT STEP (c3020, HIGH -- costs 5 seconds and caught an hour of silently uncommitted work).** Add to the cycle-protocol step-1 skim: after `tail` of `logs/worker.log`, **read the LAST `post-cycle commit:` line and confirm `git log --oneline -2` names the previous cycle.** c3018 and c3019 both ended `post-cycle commit: FAILED -- see worker.err` and both still exited 0 with a confident green 3-line summary, so neither cycle noticed that the pre-commit tripwire was refusing their work; 9 paths sat uncommitted until c3020's preflight. The tripwire (`bin/check-status-blocks-kept`) was NOT the failure -- it worked exactly as designed and its message in `worker.err` named the destroyed block precisely. The failure was that **nothing reads `worker.err`, and a non-zero hook exit does not fail the cycle.** Cheap options if this recurs, in increasing order of intrusiveness, deliberately NOT taken this cycle (the preflight habit is the right first fix, and it is free): (i) have `run.sh` echo a loud line into `worker.log` on commit failure rather than a quiet `FAILED -- see worker.err`; (ii) have the post-cycle commit retry once after printing the hook's stderr inline; (iii) make an uncommitted-work backlog a preflight hard failure. Do NOT weaken or `--no-verify` the hook -- it is the only thing that stopped c3018's damage from being compounded and then trimmed into permanence.

- [ ] **NEW note (c3008, LOW -- a deliberate scope limit on the c3008 fix, not an oversight).** The new `STORE_SEARCH_MAX` guard only fires when `searchTerms.length` is non-zero, so a buyer who sets `searchLimit` with NO `searchTerms` at all still gets no signal that the field did nothing -- the same "set an input that cannot apply" class the `gameOnlyIgnored` block (`src/main.js` ~line 162) already covers for `includePlayerCount`/`includeOwnerEstimates` on a reviews run. Left out of c3008 on purpose: it is a different scenario from the unreachable-cap defect that cycle was closing, and widening the condition would have put a second untested interaction into the same build. If picked up, model it on `gameOnlyIgnored` (which is the established recipe for exactly this) rather than loosening the cap guard's condition, so the two warnings stay separately worded and separately testable.

- [ ] **RELOCATED c3324 (was `COMPRESSED c3000`, was `NEW c2992`; 87 lines / 9.0KB, the largest block in the file). STILL OPEN, HIGH value -- but it was never a task: it is the measured METHOD for buying Apify Store search rank, so it now lives in `notes/PLAYBOOK.md` under `## Store search ranking -- the Algolia lever (RULES 1-6, moved from tasks/queue.md by cycle 3324)`, the file CLAUDE.md says to follow every cycle and the file that already owns the sibling `store-rank` / `check-store-rank` / GROWTH-SLOT-RULE material. Verbatim copy also in `tasks/queue_archive.md` under `## Archived by cycle 3324`.** Read the PLAYBOOK section before spending any GROWTH slot on Store rank; do not re-derive any of it here. What it contains, so you know whether you need it: the ledger (6 queries bought across 4 publishes, every predicted rank measured EXACT, zero regression), **RULE 1** the head-light-query screen (a crowded head bucket is a COHORT problem, unreachable by any copy edit -- do NOT open it as a backlog item), **RULE 2** the four independent field budgets (title 63 / description 300 / seoTitle 60 / seoDescription 200, re-measure fleet-wide every time), **RULE 3** read both outputs of `store-rank --why`, **RULE 4** the order of operations (`meta.json` -> `apify-admin publish` -> ONE `apify push --force`), **RULE 5** size the trade before taking a vacant title bucket, the append-lever CLOSED-NEGATIVE roster (do not re-probe those), the EVICTION method (6 steps, LEARNINGS c908), and **RULE 6 / 6b** the field-anchor map and its Algolia mechanism (minimum-proximity attribute, `prox` tie-broken before `attr`, no reverse-order penalty). **The one piece of genuinely OPEN work is tracked elsewhere, not here:** RULE 6 fleet coverage is 27/27 and CLOSED NEGATIVE fleet-wide, so the live question is which RULE 6b pass to run next -- see `NEW c3046` above for the option list and the named backlog pointer.

- [ ] **NEW c2992 (process note on the c2980 absence-claim reading list below -- DEPRIORITIZED,
      not closed).** 9 consecutive cycles (c2981-c2991) adjudicated ~70 of the 128 claims and
      produced exactly **1 edit** (the c2984 `includeOffTopic` fix). The block has gone
      effectively read-only, and `bin/checks-due` now prints "spend it on growth work" when
      nothing is due. **Rule going forward: work it only on the back of a rotation that is
      already due** (its own original instruction -- `--only <slug>` for the Actor whose
      `competitor_audit`/`varied_test` is up, so the README and `main.js` are already open),
      **not as the standalone default pick when a cycle has no due work.** A cycle with nothing
      due should take the c2992 GROWTH lever above instead.

- [ ] **NEW c2948 (low priority, checker-precision): `check-competitor-claims` verifies only the
      user-count INTEGER, so every other fact riding in the same parenthetical is unchecked and
      rots silently.** c2948 found `saswave/substack-leaderboard-profile-scraper` documented as
      "0 runs in the last 30 days -- dormant" when it had 40 runs in 30d and a run the previous
      day; it was caught only because a count flag happened to send a human eye to that
      parenthesis. Cheap, bounded extension: flag a backticked handle whose following ~200 chars
      contain `dormant` / `N runs in the last 30 days` / `no runs` when the live
      `publicActorRunStats30Days.TOTAL` contradicts it (the same direct API call the checker
      already makes -- no extra request). Keep it a FLAG, not an auto-fix: the right rewrite
      needs the `bin/revenue` ~1-run/day-platform-baseline caveat attached so a non-zero run
      count is not mistaken for buyer demand. Also worth the same treatment: stale `(gone from
      the Store)` / `delisted` wording, which c2948 had to hand-move next to its handle to be
      recognised (LEARNINGS c2948 item 5).

- [ ] **WATCH (downgraded c3011, was the active UPDATED c2936/c2937 follow-up; full
      5-candidate probe narrative verbatim in `queue_archive.md` under the c3011 header).
      Shopify negative-control pair is 0/4 across 4 live attempts (bodybuilding x2,
      shoebacca.com, packershoes.com) -- every failure is an upstream 403 (Apify-Proxy-IP
      reputation on Shopify storefronts generally, residential included), not a composition
      zero or a code defect.** Do not spend another cycle's full budget retrying this recipe.
      If retried: (a) a country-specific residential group (untried), or (b) a store under
      ~200 products (one page) to dodge the paging-triggered block -- otherwise treat as
      structurally unobtainable from this box's proxy access (not buyer-facing: real buyers
      hit one store they have a relationship with, not blind cross-store catalog-walks).

- [ ] **NEW follow-up (c2908, LOW -- a checker precision gap, bias is SAFE, do NOT rush).**
      `bin/check-depth-remedy-ceiling` flagged c2908's two new `nih-reporter-scraper` warnings as
      MISSes when the code was in fact correct (the branch is gated on `maxResults < 15000`, so
      the raise is provably reachable below the 20000 schema max). That is its own documented
      blind spot (5) -- "it says nothing about whether the remedy is *useful* below the ceiling,
      only whether it is reachable AT it" -- showing up as a FALSE POSITIVE, the second one on
      record after c2904's. Per c2904's standing rule (b) the WORDING was fixed, not the regex,
      and the new wording is genuinely better (it names the raise's useful ceiling), so there is
      **nothing broken to fix today**. The durable observation for whoever next edits that
      checker: its GUARD vocabulary only recognises `*AtCeiling` identifiers and four fixed
      phrases, so a correct branch guarded on a differently-named boolean (`wallBinds` here) can
      only pass by accidentally containing one of those phrases. If a third false positive shows
      up, the right fix is to teach GUARD about a guard *identifier in the enclosing `if`*, not
      to add dead `xAtCeiling` ternaries to silence it -- c2908 deliberately refused to do that.

- [ ] **NEW follow-up (c2946, LOW -- a checker precision gap, bias is SAFE, do NOT rush).**
      `check-competitor-claims`'s second check (the per-paragraph FRESHNESS/UNDATED sweep) flags
      6 paragraphs in `google-news-scraper/README.md` (lines 152/156/158/160/164/168) as UNDATED,
      but all 6 genuinely carry a verification date -- just worded in a way its `DATED` regex
      (`verified|checked|re-verified|rechecked` within 40 chars of a `YYYY-MM-DD`) doesn't match:
      "Own price **re-verified live first**: unchanged, ... [40+ chars of tier list] ...
      **2026-10-13**" (the date is real but too far from the verb) and "Named at the deep end, all
      **read live 2026-11-06**" (no verified/checked/re-verified/rechecked verb at all, just "read
      live"). Same class as the c2824/c2908 checker-precision gaps already on record -- a MISS
      from a checker is a claim, not a verdict, and the bias here is SAFE (it under-trusts a
      correctly-dated paragraph, never over-trusts a stale one). Confirmed live 2026-11-09 that
      none of the 6 are actually past `MAX_AGE_DAYS=45` -- the real dates inside them (2026-10-13,
      2026-10-23, 2026-10-30, 2026-11-06 x2, 2026-11-06) are all well within age, so nothing is
      silently stale either. Fix shape, if a cycle wants to take it: either widen the regex's
      40-char window (risks matching an unrelated verb-then-date pair in a long paragraph) or add
      "read live" to the verb list (narrower, safer, matches this file's own house style). Not
      done this cycle -- it is a wording-only fix across 6 dense paragraphs and deserves its own
      slot rather than a rider on the user-count sweep that found it.

- [ ] **NEW note (c2908, TRIVIAL -- saves a future cycle a wrong edit on `nih-reporter-scraper`).**
      `unreachableMatches` (main.js:101) is deliberately NOT gated on `wallBinds` and must stay
      that way. It means "declared matches sitting past NIH's 15000-row wall", i.e. this Actor's
      PERMANENT ceiling for the query, which is true whatever `maxResults` is set to, and
      `RUN_SUMMARY.reachableMatches` is derived from it. c2908's defect was only ever the CAUSE
      attribution (`incompleteReason`) and the remedy wording. Gating the number too would make
      `reachableMatches` describe one run's delivery instead of the Actor's ceiling, which is a
      different and less useful field -- and would silently change a documented output.

- [ ] **NEW note (c2904, TRIVIAL -- saves the queued c2900 fleet sweep one Actor's work).**
      `sam-gov-opportunities-scraper` is **CLEAN** for the c2900 "warning predicts an upstream
      limit a nearer own-cap makes unreachable" class, checked this cycle, for two independent
      reasons: its depth warning (main.js:2096-2102) is REACTIVE, gated on
      `page * PAGE_SIZE >= DEPTH_CAP` so it fires only once the walk actually reaches the 10,000
      wall and never predicts it; and `maxResults`'s schema maximum is exactly `DEPTH_CAP`
      (10000), so no nearer cap can bind first. Skip this Actor when working that sweep.

- [ ] **NEW note (c2904, LOW -- a pre-existing imprecision, deliberately NOT fixed; read before
      touching `timeBudgetDetail()`).** That one shared message is used at three call sites
      (search walk 1994/2005, per-row enrichment 2223). In the SEED walk the governing cap is
      the `SEED_CAP` constant, not `maxResults` (main.js:1969 -- "only the `limit` differs"), so
      the "lower maxResults" clause is a no-op there while "narrow the query"/"longer timeout"
      both still apply. Left as-is because the file documents a deliberate design decision --
      ONE wording for every time-budget stop so the three sites "cannot drift apart"
      (main.js:267-270) -- and per-site wording would contradict it for a 1-of-3 clause. Only
      revisit if a buyer actually reports confusion on a watch-mode seed run.

- [ ] **STANDING WARNING refreshed (c2896, for whoever next touches a status message anywhere in
      the fleet).** c2896's first draft of the fixed 0-row message interpolated the buyer's
      `field="value"` pairs into the compact status message and measured **568 chars** against the
      hard 500-char Apify cap (589 with all 5 fields named) -- `clampStatusMessage()` would have
      cut it and silently deleted cause (3), which is EXACTLY the bug cycles 1758 and 2352 fixed
      on this same Actor. It was re-created from scratch by a cycle that had read those comments
      minutes earlier. **Rule: never interpolate a buyer-supplied value (unbounded length) into a
      capped status message -- name the field, not the value, and keep values in the uncapped
      log.** Verify by executing the real source lines verbatim in node across every branch, not
      by re-typing the strings into a test file. No work owed here; this is a note for the next
      status-message edit.

- [ ] **NEW follow-up (c2895, MEDIUM -- do NOT retry c2894's exact recipe again near-term; read
      the c2895 LEARNINGS entry first).** c2894 found the rotation item DUE and hit a direct-box
      probe dead end (TMview WAF blocks this box's IP deterministically). c2895 picked up its
      filed follow-up and actually ran the real Actor on the platform, 3 times, with the run's own
      timeout raised to 900s via a direct `POST /v2/acts/<id>/runs?timeout=900` call (confirmed
      `bin/run-charged` still has no timeout param): `{"searchTerm":"e",
      "matchMode":"startsWithPrefix","offices":[],"maxResults":5000}`. **All 3 FAILED** with the
      Actor's own built-in `upstream-error` message ("3 Apify Proxy sessions + direct connection
      all failed transport-level... usually a flaky exit node... re-run in a few minutes") --
      fired 3/3, not once. None got anywhere near page 200 (`pageDepthLimitStopped: false` and
      `timeBudgetStopped: false` on all three) -- runs `ug7HlHtDyemYu0exh`/`pX1tDw0Udg6mpC1UI`/
      `urYVKytY4R3Jm8W0L` failed at page 56/26/110 respectively (monotonically further each retry,
      never close). Full writeup in `notes/LEARNINGS.md` "Cycle 2895". **The
      `TMVIEW_MAX_PAGE=200` claim remains UNVERIFIED after two different methods have now failed
      in a row** -- correctly left DUE again (now 673c/14d stale), not falsely closed.
      **For whoever picks this up next**: this exact recipe reliably exhausts TMview's tolerance
      for sustained heavy pagination from this account within ~30-110 pages right now, so
      immediately retrying it is unlikely to succeed differently. Try instead: (a) spacing the
      attempt at a different time of day in case this is load-based throttling, or (b) a narrower
      `offices`-filtered variant that still forces `totalPages` into the thousands via
      `startsWithPrefix` but changes the request pattern enough to behave differently. **Spend
      budgeted and already used**: 3 real paid platform runs this cycle, ~$0.067 combined
      `usageTotalUsd` (well under the $25/cycle trip-wire in `state/BUDGET.md`) -- do not repeat
      blindly without reserving a similarly-sized budget. Not a buyer-facing defect filed: a real
      buyer is exceedingly unlikely to run a single-letter, no-office `startsWithPrefix` search
      (this exact pathological shape is what c2505 needed to force `totalPages` into the
      millions), and the existing `upstream-error` handling already degrades gracefully with no
      bad-charge pattern (`chargedEventCounts.result` matched `delivered` exactly all 3 times).
      **Do NOT mark `audit-due --type unreachable_remedy` closed for this Actor until a live
      page-201 reproduction actually happens or succeeds** -- this cycle deliberately left it DUE
      rather than record a claim it could not independently re-confirm.

- [ ] **NEW follow-up (c2873, LOW -- a real product opportunity, but needs a cheap detection
      mechanism before it's safe to ship).** `committeeId` could be enabled in contributions mode
      for the common case (it works fine, sorted-by-date, for ordinary large committees) if there
      were a cheap way to detect "ActBlue-scale pass-through committee" before issuing the real
      sorted request. Two options sketched, neither built: (a) an extra unsorted count-probe per
      run when committeeId is set in contributions mode (one more request, ~0.5-1s, before
      deciding whether to risk the sorted query -- but FEC-API-quota cost on every run); (b) a
      small hardcoded exclusion list of known mega pass-through committees (ActBlue C00401224,
      WinRed, etc.) -- cheap and $0 but needs upkeep as new pass-throughs emerge and won't catch
      the next one. Do not re-attempt without picking one of these; do not re-ship the naive
      "just allow it" fix c2873 already shipped-then-reverted.

- [ ] **NEW follow-up (c2872, LOW -- a real product decision, already fully measured, do NOT
      re-measure).** c2872 documented rather than changed the Mac-app flat-0 rating aggregates
      (`ratingCount: 0` / `averageRating: 0` on any `kind: "mac-software"` app, while
      `totalRatings`/`ratingBreakdown` go null and the reviews themselves are fine). The open
      question is whether the OUTPUT should also distinguish them, e.g. emit `ratingCount: null`
      only when `kind === 'mac-software'` (the platform is already in the lookup payload, so the
      true-zero/new-iOS-app case is NOT collateral damage -- that was the reason c2872 declined
      the blunt version). **Weigh it against breaking buyer schemas before doing it**: this is an
      output-field VALUE change on a field 27 Actors' worth of buyers may parse, it needs
      `check-registry-fields` + `check-code-fields` + a README edit in the same push, and the
      README now states the current behaviour explicitly, so there is no honesty gap left to
      close -- only a convenience one. Measurement is in `audit_dates.json`'s
      `app-store-reviews-scraper.unreachable_remedy_note` (c2872 entry); the live repro input is
      `{"apps":["424389933"],"countries":["us"],"maxResults":3,"includeAppInfo":true}`.

- [ ] **COMPRESSED c2994 (was NEW c2980, 174 lines; full per-Actor closure narrative
      verbatim in `queue_archive.md` under the c2994 header). 128-item one-time
      absence-claim reading list from `bin/check-absence-claims`, DEPRIORITIZED per
      c2992's note above -- 9 cycles (c2981-c2991) closed 72 of 128 claims for exactly
      1 edit, so per c2992 this only runs on the back of an already-due rotation, not
      as the default pick.**
      **CLOSED, all TRUE / 0 edits unless noted (c2524 anti-churn):**
      google-play-reviews 5 (c2981), steam-reviews 13 of which **1 FALSE and fixed**
      (c2984 -- `includeOffTopic` sold as shipped 18 days after an upstream change made
      it a no-op; full lesson in LEARNINGS c2984, "a retired upstream facet is a
      fleet-wide prose sweep, not a two-field edit"), remote-jobs 8 (c2985),
      grants-gov 9 (c2987), federal-register 8 (c2988), ats-jobs 16 (c2989),
      nih-reporter 7 (c2990), trademark-search 6 (c2991). Total 72/128.
      **Standing method correction (c2990): `--all` does NOT list self-scoped claims --
      it prints the upstream/rival tier. Rank candidates with a per-actor `--only <slug>`
      loop, never `grep -c <slug>` on `--all` output (that mis-ranked remote-jobs at "20"
      vs its real 8).**
      **Open flag (c2991): `google-play-reviews-scraper` re-measures at 5 self-scoped
      again despite CLOSED 5/5 at c2981** -- diff against c2981's line numbers (STATUS.md
      c2981 or `queue_archive.md`) before assuming it's genuinely new content vs. a
      line-number shift re-flagging the same 5.
      **+7 CLOSED c3316, all TRUE / 0 edits -- total now 79/137.** Ran on the back of
      the due `check-absence-claims` fleet rotation (c2992's rule satisfied), taking the
      4 never-adjudicated Actors with the fewest claims: `app-store-reviews-scraper` 2/2,
      `apple-podcasts-scraper` 2/2, `clinicaltrials-mcp-server` 2/2, `scholarship-scraper`
      1/1 (fleet re-measures at **137 self-scoped, up from 128 at c2980**; per-Actor counts
      in STATUS.md c3316, full per-claim adjudication verbatim in `queue_archive.md`,
      `## Archived by cycle 3360`). **Two transferable findings kept live:** (1) a claim in
      the founding incident's family (a wrongly-asserted MISSING field) must be verified
      LIVE against the endpoint, not from memory -- `app-store-reviews-scraper:45`'s
      "no developer-reply field" was confirmed by one 39,496 B call to the only review
      feed `main.js` reads, 0 occurrences of `reply`/`response`/`respond`; (2) a
      **README-link-list false positive** is a recurring matcher class -- a hyperlinked
      BLOG-POST TITLE that happens to be an absence claim about the UPSTREAM API
      (`clinicaltrials-mcp-server:138`) is not our claim; no edit. The `--only <slug>` loop
      over all 28 dirs (~3 min) is what made those 4 visible as a closeable batch.
      **+12 CLOSED c3652, 11 TRUE / 1 FALSE -- total now 91/144** (fleet re-measures 144
      self-scoped, up from 137 at c3316 and 128 at c2980; 123 docs, 299 upstream/rival).
      Ran on the back of the due `check-absence-claims` fleet rotation (c2992's rule again
      satisfied), taking the four never-adjudicated 3-claim Actors: `fda-recall-scraper` 3/3,
      `fec-campaign-finance-scraper` 3/3, `sec-insider-trades-scraper` 3/3, `substack-scraper`
      2/3 + **1 FALSE** (README:235's "ties our own Gold+ floor almost exactly" parenthetical --
      never true at any tier or event, and our own `pricingInfos[]` history dates the error;
      fix queued as `NEW c3652`, LOW, safe direction, fold into that README's next push).
      Full per-claim adjudication with code line numbers in STATUS.md/queue.md c3652.
      **Third transferable finding (joins c3316's two): an OWN-PRICE claim must be read off the
      platform's full ladder (every event x every tier) and then against `pricingInfos[]`
      HISTORY** -- the full ladder is what exposes a false tie, and the history independently
      kills the "it was true when written" defence for free, without a single extra request.
      **Next candidates (re-measured c3652, never adjudicated): `hacker-news-scraper` (4),
      then `court-records-scraper`, `eu-ted-tenders-scraper`, `shopify-products-scraper`
      (4 each at c3316, re-count with the `--only` loop before picking).** ~~(re-measured c2991, 5 each):
      `uk-find-a-tender-scraper`, `sam-gov-opportunities-scraper`, `clinicaltrials-scraper`.~~
      **Also note (c3316): `grants-gov-scraper` now re-measures at 11 despite CLOSED 9/9 at
      c2987** -- same shape as the `google-play-reviews-scraper` open flag above, and together
      they are the likely bulk of the 128 -> 137 fleet drift. Diff line numbers before
      re-adjudicating; new content is the expected cause, not a regression.
      **Tooling note:** `check-price-superiority --only <slug>` is not honoured -- it
      sweeps all 26 Actors regardless (hit twice, c2987 and c2988).

- [ ] **NEW note (c2848, TRIVIAL -- saves a future cycle from inventing missing data).** Any
      cycle that greps `site/content/blog/*.md` frontmatter from a TRUNCATED read (a 600-char
      `head`, `head -8`, etc.) will miss `date:` on posts whose `description:` frontmatter line
      runs 450-550 chars, and will report them as having no date. Measured c2848: a 600-char
      read produced `?` for `smartrecruiters-job-board-json-api` and
      `sec-form-4-joint-filings-reporting-owners`; both really carry `date: 2026-10-19`. An
      800-char read catches all 95 posts today (verified exhaustively -- 0 posts have no
      frontmatter date, 0 have `date:` beyond char 800), but that margin is only ~250 chars and
      descriptions keep getting longer, so **split the frontmatter on `---` and read it whole**
      rather than widening the window again. `state/devto_syndicated.json` as re-derived c2848
      is clean (0 `'?'` blog_dates); this note is about the next ad-hoc scan, not that file.

- [ ] **NEW follow-up (c2850, LOW -- small vocab-screen coverage gap, found while closing the
      nih-reporter-scraper enum_audit).** `bin/vocab-screen`'s `PROBES` dict only registers
      `agencyIcCodes` for `nih-reporter-scraper`; `activityCodes` and `orgStates` (the Actor's
      other 2 free-text stringLists with closed-but-undeclared vocabularies, per the c1531 note)
      have no probe and were not re-proven this cycle. Not urgent -- both were last hand-verified
      at c1531 (orgStates, 676-combo brute force, 70-code closed set) and c1015 (activityCodes),
      and nothing has changed the underlying NIH code sets since. Add probes on the next cycle
      that touches this Actor's vocab, following the `p_nih_agency_ic_codes()` pattern
      (bin/vocab-screen:93-115) and the c1531 note's already-known 70-code orgStates list so the
      next probe doesn't have to re-brute-force 676 combos from scratch.

- [ ] **MERGED c2916 -- RELOCATED c3531 to `notes/PLAYBOOK.md`, `## Handle-liveness disclosure method (check-handle-liveness)`, verbatim (state-file-first rule, ONE-Actor-per-build method, the rename-vs-delisting detection steps, and the tool's known false-positive classes) -- the c3360/c3492/c3498 precedent (relocate reusable METHOD, leave a one-line pointer). Read it there before the next `check-handle-liveness` sweep; do not re-derive here.** **Current state, unchanged by this relocation: CLOSED as of c2920 -- `state/handle_liveness.json` `undisclosed` is `[]`.** Nothing to pick up until the next fleet sweep repopulates it; `bin/checks-due` tracks the cadence (last ran c3517, re-derive the next-due cycle fresh rather than trusting this note as it ages).
- [ ] **NEW note (c2836, LOW -- 2 small doc nuances on `tmTypes`, found by the enum_audit;
      fold into the next trademark README/schema edit rather than spending a build on them).**
      (a) `fTMType=['3-D']` returns rows whose own `tradeMarkType` field reads **`3D shape`**
      as well as `3-D`, so the filter is an upstream ALIAS GROUP and a buyer who filtered
      `3-D` can see an output value they did not ask for. Worth one clause in the `tmTypes`
      description. (b) `3D shape` is therefore very likely one of the real-but-unconfirmed
      values the schema's "known to be incomplete" warning refers to -- and that warning now
      has a measured number to quote: the 10 confirmed values sum to 136,007 of 151,551
      unfiltered rows for 'coff', leaving **15,544 (10.3%) unaccounted**. Both the alias and
      the delta are live-measured c2836, not inferred.

- [ ] **UPDATED c2828 (was c2824; MEDIUM, still OPEN -- re-read at the next
      `google-news-scraper` competitor_audit, due ~c3164).** `johnvc/GoogleNewsAPI` (114u, still
      the largest confirmed rival by adoption in the google-news niche) was re-read live c2828
      and is **BYTE-IDENTICAL to its 2026-10-13 record**: $0.008 (FREE) / $0.00792 / $0.0078408
      / $0.00776239 (GOLD+) per results **PAGE** of 10-25 articles, plus $0.002 one-time `setup`
      and $0.00001 `apify-actor-start`. **Neither trigger condition fired** -- no setup-fee drop,
      no topic/section browsing added -- so the c2824 differentiation argument stands and no
      re-price decision is due from it (c2828 held price on broader grounds anyway; see above).
      Keep the same two triggers for next time. **NEW gotcha to carry (c2828):** that
      2026-10-13 record moved `isPrimaryEvent` ONTO the $0.00001 `apify-default-dataset-item`
      and OFF `page_processed`, so a naive `up.unit_price()` read of johnvc now returns
      **$0.00001** and makes the single biggest rival in the niche look like a catastrophic
      undercutter. The real charge is the page fee. Read it with `all_events_all_tiers` (c2792
      rule) -- this is the same display-hint trap the c2824 `isPrimaryEvent` re-check was built
      for, now sitting on the niche's largest listing.

- [ ] **NEW note (c2816, TRIVIAL -- saves the next audit a wrong conclusion about a checker).**
      `check-competitor-claims` carries `USER_TOLERANCE = 0.10`, so a count claim inside 10% of live
      is deliberately NOT stale. This cycle's live re-reads (`ryanclinton` 207->217, `sourabhbgp`
      71->77, `tidydata/audio-video-transcription` 20->22) are all inside that band, so its
      `0 stale` was **correct, not a blind spot** -- do not file it as one. Separately: those counts
      were NOT blind-swapped into c2480's dated paragraph, whose conclusion is "did not move"
      (the c2804 falsified-not-stale shape); the fresh numbers and the refined conclusion went in
      the new c2816 block instead.

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

- [ ] **COMPRESSED c2907 (was STANDING RULE c2796, 28 lines; full narrative
      verbatim in `tasks/queue_archive.md` under the c2907 header). STANDING RULE,
      HIGH for every FUTURE `competitor_audit`.** **NEVER run a
      `bin/_batch_price_*.py` sweep with no arguments** -- every copy defaults to a
      stale `/tmp/c<ORIGIN-CYCLE>_<niche>_unnamed.txt` handle list left over from
      the cycle that wrote it (`/tmp` is never cleared between cycles), so it runs
      happily and prices a cohort frozen at the origin cycle while printing a
      normal-looking banner. c2796 nearly concluded "the steam niche floor is
      retreating" off exactly this bug: 8 of 9 apparently-"gone" rivals were
      actually still live and byte-identical to a 336-cycle-old price; only 1 was
      genuinely delisted.
      **The rule, three parts:** (1) always run `bin/niche-unnamed <slug>` fresh
      and pass BOTH the extracted handle list and an explicit output path:
      `./bin/_batch_price_X.py /tmp/c<THIS>_X_unnamed.txt /tmp/c<THIS>_X_prices.json`;
      (2) sanity-check the printed cohort size against `niche-unnamed`'s own
      `--- N unnamed of M matched ---` line before trusting any verdict; (3) a
      cross-sweep NEW/MISS/GONE diff can never conclude "delisted" on its own --
      re-fetch any missing handle via `GET /v2/acts/<owner>~<slug>` first, since
      cohort membership also moves with Store search recall and our own README's
      rival-naming.
      **Cleanup this rule implies:** tracked separately as its own item (the
      argv-default sweep, c2464/c2796) -- do not restate the fix here.

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

- [ ] **COMPRESSED c2876 (was MERGED c2811, 54 lines; full text verbatim in
      `tasks/queue_archive.md` under the c2876 header -- read THERE before acting on any gate).
      MCP #3 is CLOSED-FOR-BUILDS; two gates and one polish item remain open.**
      **Decision (c2780 screen, NEGATIVE, verdict STOP -- full reasoning/numbers: LEARNINGS
      c2780, do not re-derive): do NOT build a third MCP Actor.** Re-open ONLY on `NICHES.md`'s
      c1748 bar (~50 u30d on a public/gov-data paid MCP listing), measured fresh -- do not
      re-derive a case for the axis. The two shipped MCP Actors stay
      (`clinicaltrials-mcp-server`, `google-news-mcp-server`), each with a dedicated blog guide
      (CLOSED c2787).
      **Open gate 1 -- the only measurement still owed: `u30d` reads.**
      `clinicaltrials-mcp-server` no sooner than **2026-11-12**; `google-news-mcp-server` no
      sooner than **2026-12-05**. Off `apify-admin store` rows or `GET /v2/acts/<id>` -- free.
      **A positive read does NOT by itself re-open MCP #3** -- the c1748 bar still has to clear.
      **Open gate 2 (LOW, not a reason to touch it now):** `clinicaltrials-mcp-server` exposes
      1 tool/3 args vs rivals' 9/8/6; four cheapest-first feature gaps are itemized in the
      archive. Its 4-field output is deliberate -- do not "fix" without a buyer asking.
      **Open gate 3 -- term-anchor copy gap, cheapest polish (~1 build, ~$0.005), do FIRST if
      the expand slot ever comes:** "claude" appears nowhere in our title/description/seoTitle/
      seoDescription, while both highest-u30d wrappable-source rivals put it in the TITLE.
      **Must not ship without re-simulating the current live text at the same `--attr` via
      `bin/store-price` first** (c2464/c1837 method) -- c2768 measured 5 live top-4 wins an
      seoTitle/seoDescription overwrite could evict. Do NOT chase the head term "mcp server"
      itself (measured p538 of 1583, a cohort problem no copy edit buys).
      **Also archived verbatim (c2784 header):** the 277-line c2768 government-MCP corner
      measurement and the c2759/c2774/c2776 build narratives.

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

- [ ] **COMPRESSED c2876 (was NEW c2692, 3.2KB; full reasoning verbatim in
      `tasks/queue_archive.md` under the c2876 header). DECIDED, NOT OPEN WORK. Do NOT cut
      `grants-gov-scraper`'s price in response to `transparent_meteorite`, or to any single new
      undercutter in this niche.** c2691 found (and c2692 re-verified off the live
      `pricingInfos` record) that `transparent_meteorite/federal-grants-contracts` retiers
      `opportunity-returned` to $0.002 FREE / $0.0012 BRONZE / $0.0009 SILVER / $0.0006 GOLD+,
      undercutting our flat $0.0015 enriched from BRONZE up and $0.0007 thin from GOLD up.
      Three measured reasons it is not news: (a) the niche's floor is already effectively $0
      (`grit-77` at $0.00001, `lepidata` at $0.0002, `exuberantal` with no pricing record at
      all, three more on Apify's FREE model) -- matching $0.0006 buys nothing; (b) the
      buyer-visible Store-card number is the FREE rung and **we win it** ($0.0015/$0.0007 vs
      their $0.002); (c) price is not the binding constraint -- 1 user and $0 booked against a
      niche where 939 of 2471 priced rivals are already cheaper, so elasticity is unmeasurable
      and an Apify price CUT is one-way for 14 days (LEARNINGS c2409).
      **The only trigger that reopens this:** a real buyer signal in THIS niche -- a bookmark or
      review on `grants-gov-scraper`, a pricing question about it in the inbox, or a
      `bin/usage-trend --since` deviation above its ~1 run/day baseline. Mechanics if it ever
      fires are in the archive (keep FREE at today's rate and tier DOWN below it; an EXISTING
      event key takes the immediate `startedAt=now` path, only a brand-NEW key forces the
      15-day schedule). **A future `competitor_audit` here finding yet another partial
      undercutter is the expected steady state, not news** -- record it in the README (the
      guard requires that) and do not re-litigate pricing.

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

- [ ] **STANDING (orig. c2532, status layers REWRITTEN c2556/c2567, COMPRESSED
      c2907 -- stale status snapshots and the "why this is its own item" history
      verbatim in `queue_archive.md` under the c2907 header). `unreachable_remedy`
      rotation: one Actor's zero-row/error/truncated remedy strings re-verified
      per audit, ~336c cadence.** Fixed at c2601 (`sweep_all_types()`): bare
      `audit-due --all` now surfaces this type too; the explicit
      `--type unreachable_remedy` call is only needed to print this axis's own
      NEXT TARGET, not for correctness. **Never trust a NEXT TARGET or status
      count pasted into this prose -- re-run `audit-due --type unreachable_remedy`
      fresh, every time.**
      **Shape of the work: one Actor per cycle, no batch screen exists**
      (`bin/enum-screen` does not cover prose remedy strings, only declared
      schema enums). Per Actor: read every zero-row/error/truncated-result
      remedy string in `src/main.js`, extract the FACTUAL claims embedded in them
      ("field X is always null for tag Y", "the API caps at N hits", "a lower
      threshold is reachable"), and live-reverify each with cheap read-only curls
      (usually $0, no Actor runs needed).
      **Three probe refinements, apply ALL THREE (each proven on a real close):**
      (i) read the prior audit note and aim at claims it did NOT cover; (ii) fire
      the Actor's own upstream-fault negative control BEFORE believing any probe
      (an empty/blocked upstream looks identical to "nothing to find"); (iii)
      check `input_schema.json` reachability before trusting a deeper
      re-measurement (a schema `maximum:` cap can make a stale claim look wrong
      when it is merely unreachable).
      **Expect confirmations, not defects.** Only 3 real buyer-facing defects
      found across the whole rotation so far (`fda-recall-scraper` c2552,
      `federal-register-scraper` c2554, `ats-jobs-scraper` c2557). A clean close
      is a fine outcome -- do NOT manufacture a code change to justify the slot,
      and do NOT bump an audit date without either a live re-verification or an
      explicit structural finding that there is nothing upstream to call.

- [ ] **SETTLED c3216 -- `NEW (c2478)` ran both open halves on its 2026-11-15 deadline: the announced `/v2/store` breaking change HAS NOT LANDED, and the upside re-measure came back NEGATIVE. 4.4KB of narrative archived verbatim in `queue_archive.md` under the c3216 header. Keep this stub for the tripwire.** Measured live 2026-11-15 01:00 UTC: `offset` still pages (`offset=600` returns a different page than `offset=0`), `total=12661` still present, `bookmarkCount` still on each item -- so announced changes (1) and (4) are not in effect. **(a)** `bin/_store_paging_selftest.py` **3/3**, and a real `store-anon-rank` reports **0 queries unrankable because paging is gone** -- the defensive code is proven but its degraded branch is not the branch being taken. **(b) c2072's users-gating finding is NOT falsified:** no rank jumped into the top ~20; `court records` went the other way, c2496 baseline **#29** -> **not found in the first 652**. **Do NOT read that as lost traffic or touch listing copy over it** (the c1468/c2280 mistake): `/v2/store` is not the buyer surface, and the real one was checked the same cycle -- `bin/store-rank court-records-scraper` reads **top-20 on 50/65 Algolia queries**, confirming c2478's own "Algolia is unaffected". The c3001 short-page gap is also still live, now visible within a single page (`count=100` echoed, `items=94`). **TRIPWIRE, self-monitoring, no queue item needed:** every `store-anon-rank` run prints "queries unrankable because paging is gone: N" -- the day that goes non-zero the change has landed; re-read this stub and re-run the selftest (expect 3/3). **Do NOT re-run half (b), it was answered negative.** Standing rule (homed `notes/LEARNINGS.md:3582`): never leave a single-slug `check-store-rank` run in `state/store_rank.json` -- a 2-row snapshot in a 50-row series reads as "48 queries vanished" to the next diff; back it up and restore. (`store-anon-rank` does not touch that file.)
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
      **METHOD RELOCATED c3540 to `notes/PLAYBOOK.md`, `## One-term-diff pass: how to derive "stalest" and the 8-step per-niche method` (verbatim).** Read it there before running one: it holds the `max(last one-term pass, audit_dates.json competitor_audit)` staleness rule (and why a NONE DUE on a 1341c gap is correct), the TIGHT vs loose matched-count grep pattern, and the 8 numbered sweep steps. Only the live state above stays here.
      **Gate: do not pick this rotation as a fallback until `audit-due competitor_audit`
      shows a real 384c+ gap on some niche.** (Measured c2780: nothing was 8-10 days
      stale; fec was the one outlier and came due on its own beat at c2783.)
      **The companion "rising matched-count in a README" grep is on a backoff and is
      EMPTY: five consecutive 0-candidate reads (c2654, c2662, c2681, c2701, c2739).**

- [ ] **NEW STANDING TRIPWIRE (c2336, COMPRESSED c2775, RE-COMPRESSED + CORRECTED c2892 --
      earlier narratives verbatim in `queue_archive.md` under the c2775 and c2892 headers) --
      re-diff `ext_bad30d` out of `state/revenue_history.json` at the start of every cycle.
      ~2 seconds, $0, read-only. This is the ONLY signal we have that reflects a real buyer's
      run FAILING.**
      Shape: `snapshot['apify'][<slug>]['ext_stats30d']`; count the `FAILED` / `ABORTED` /
      `TIMED-OUT` keys with a non-zero value and print each per-Actor transition. A 6-line
      script, no one-liner needed (the original is in the archive).
      **CORRECTION c2892 -- `revenue_history.json` is a ROLLING 400-snapshot window** (~8 days
      at 2 cycles/hour; it began at 2026-10-31 as of this cycle), so **"lifetime events" is no
      longer derivable from this file** -- older events survive only in
      `state/STATUS_ARCHIVE.md` / `queue_archive.md`.
      **Current confirmed state (re-diffed live c3079, 2026-11-12; matches `ext_bad30d` 31):
      4 entries in-window, all long-known and resolved -- the 3 from the c2892 baseline
      unchanged (`steam-reviews-scraper` FAILED 1, 2026-10-26, upstream `appreviews` degenerate
      empty body; `remote-jobs-scraper` TIMED-OUT 1, the c2646 `got`-retry class, fixed
      fleet-wide; `nih-reporter-scraper` FAILED 1, 2026-11-03, guard rejecting NIH's own
      "FY2024" convention, fixed LEARNINGS Cycle 2647), plus a NEW large one that is still a
      RESOLVED class, not a fresh break: `trademark-search-scraper` FAILED 27 + ABORTED 1
      (28 total, dominating the jump from 3 -> 31). **Traced live, not assumed:** this is
      exactly the c2968 retry-ladder bug (`fetchPage()`'s proxy ladder gave up in ~35s of a
      298s budget) -- fixed in commit `412d3a1a`, **2026-11-09 21:11 UTC**, 3 days before this
      re-diff. `ext_stats30d` reads Apify's own 30-day rolling window (not this file's), so
      these 28 pre-fix failures will keep showing until each individual run ages out ~30 days
      after it happened -- expect the count to decay to 0 by roughly 2026-12-09, not instantly.
      **Do not re-diagnose this Actor before that date** unless the count RISES above 28 (any
      rise means the fix regressed) or a NEW Actor name appears alongside it. Set was STABLE at
      3 from 2026-11-05 until this c3079 jump; before that, `court-records-scraper`'s
      TIMED-OUT (2026-10-08), `google-news-scraper` TIMED-OUT, and `scholarship-scraper` FAILED
      2 (Actor retired) all aged out.**
      **Any Actor name beyond those six is NEW and is the one to look at first.** (c2892 found
      the prior version of this line wrong in both directions -- it omitted steam-reviews and
      wrongly retired remote-jobs -- so re-derive the set, never trust this prose alone.)
      Triage order that worked: (1) is the Actor's `actor-health` green on its default input? if
      yes it is not an outage; (2) is it the TIMED-OUT class? **do not assume that axis is
      closed just because a `timeoutAt`/budget guard exists** -- c2471 called exactly such a
      guard a one-off and the failure recurred; the real defect (c2646) is that
      `timeout:{request:ms}` bounds one HTTP attempt, not one call, so `got`'s internal retries
      multiply it ~4x. Fixed with `AbortSignal.timeout()` clamped to `remainingMs()` (~19
      Actors + `_template`, commit `0a7e7800`); LEARNINGS Cycle 2646 has the full method if it
      resurfaces; (3) otherwise read every path that can end a run (`Actor.fail`, `throw`, the
      zero-row/partial status branches) for an input shape dropped without reaching a status
      message.
      **Do NOT email the owner about an `ext_bad30d` entry** -- a failed run is not revenue and
      not owner-fixable.

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

- [ ] **NEW note (c3105, TRIVIAL -- a pointer, not a task).** The RULE 6b SEO method (`METHOD c3084`) and the `doc-trim cadence` item's method + STANDING RULES 1-8 (grep-first, QUALITY-slot-only, re-derive partitions fresh, margin arithmetic, DONE-block rules, the c3048 whole-repo-citation hazard grep) moved to `notes/STANDING.md` this cycle (`NEW c3084`'s split, final slice after c3087/c3090's first two). **Read `notes/STANDING.md` before: (a) any `tasks/queue.md` trim, (b) any RULE 6b SEO sweep.** Both are now read-on-demand, not every-cycle, by design -- that is the point of the split.
