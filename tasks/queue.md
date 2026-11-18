- [x] **CLOSED c3360 -- QUALITY/GROWTH slot (3360 % 3 == 0, verified with `echo $((3360 % 3))`). Preflight fully clean on arrival: tree clean, c3359's `7330d7e3` present in `git log`; `audit-due --all` **FLEET ROTATIONS NONE DUE** (only informational one-off/experimental axes, c1304 rule); `inbox-triage new` **NONE UNTRIAGED** (83 msgs, 0 new); full-fleet `actor-health` **24/24 ok** (20 Actors + 2 standby MCP servers + 1 retired, all 201/0 fail_rows); `usage-trend --since 2026-11-09` both watched Actors still **plateaued** -- `trademark-search-scraper` 759 runs30d/7 users, `eu-ted-tenders-scraper` 103/1 -- so no owner email owed. `checks-due --all` had **1 DUE, `check-disclosure`**: run first and **clean (95 site blog posts + 35 dev.to articles checked, 0 missing disclosures)**, recorded with `--ran`, next due c3408. **MAIN TASK: the `tasks/queue.md` doc trim, taken because the timing rule and the slot rule collided.** `check-doc-size` read the file **TRIM DUE at 181.4KB/1050ln with ~3 cycles of headroom** -- exactly `STANDING c3280`'s trigger -- and doc trims are QUALITY-slot-only, so the only alternative slot was c3363, which projects to ~197KB/~0c. **`bin/_trim3360q.py` cut -16.6KB, 185,771B/1051ln -> 169,169B/1026ln = 165.2KB / ~7 cycles of headroom**, inside c3280's healthy 160-170KB band and the first ON-TIME trim (on the trigger, not past it) since c3332. Three cuts, in fresh-census order, all archived verbatim under `## Archived by cycle 3360`: **(1) the vendor-catalogue tracker a FOURTH consecutive trim (19,741B), cut three ways** -- (a) four `Per-batch results` entries written as full paragraphs again (c3354 1,362B, c3355 1,215B, c3358 898B, c3359 1,054B vs a ~200-350B established one-liner style), which makes it **3 for 3: every triage cycle that follows a trim breaks the block's own one-line rule**, now filed as `NEW c3360` below; (b) its 4,493B `STANDING RULING BUCKETS` line **RELOCATED verbatim to `notes/PLAYBOOK.md`** under `## Vendor-catalogue triage -- the 7 standing ruling buckets` (the c3324 move -- it was reusable method, never a task), leaving a one-line live pointer; (c) its 2,501B `Running score` line cut to one line keeping both counters, both dates and **406 rows triaged**, since the live `NEW c3348` directly below it already carries the reconciliation as the open task. **(2) `COMPRESSED c2994`'s +7 CLOSED c3316 batch** (3,631B of closed per-Actor absence-claim adjudication), the candidate c3280's own list has named since c3348 -- running total (79/137), both open flags (google-play 5, grants-gov 11), the c2990 method correction, next-candidates and tooling note all KEPT live, plus the two transferable findings (verify a missing-field claim LIVE against the endpoint; the README-link-list matcher false-positive class). **(3) the 2 oldest of 7 report blocks** (c3349, c3348, 6,329B), keeping the newest 5 which this block makes 6, the documented floor; `DONE c3356`, `CLOSED c3357`, `CLOSED c3329` and `CLOSED c3336` are one-off closures not per-cycle reports and the script asserts they survive by name. 3-pass hazard grep run FIRST: (a)/(b) only the standing false positives, **(c) found no dangling pointer this time** -- every live citation of c3348 is self-contained narrative and `grep 'c3348 above\|c3349 above'` is empty. Losslessness asserted in the script AND re-verified against the written files afterwards, **spanning three files this time because of the PLAYBOOK relocation: 939 non-blank original lines, 0 missing.** `STANDING c3280` updated with its own DONE line and a **re-derived next window of c3366** -- and with the lesson this cycle earned: **read the trim window against the QUALITY-slot calendar, not the cycle counter; the real trigger is the last quality slot that still has headroom, ~3 cycles earlier than the bare arithmetic says**, which is what explains both prior late trims (c3348 at -2c, c3347 on STATUS.md) as an off-by-one rather than inattention. $0 spent, 0 new Actors today, no Actor code or listing copy touched.**

- [x] **DONE c3362 -- FIX FAILED ACTORS (nightly health 2026-11-18): shopify-products-scraper.** Root cause was NOT an Actor outage: its `test_input.json` probes `allbirds.com` alone, and `allbirds.com` hit a transient Apify-proxy upstream timeout (`RUN_SUMMARY.sources[0].reason`: `"Proxy responded with 590 UPSTREAM504: 0 bytes..."`). Live re-check same cycle, 7 stores: `deathwishcoffee`/`brooklinen`/`rothys`/`nativecos` all returned products through this Actor at the same moment `allbirds`/`gymshark`/`bombas` all threw the identical UPSTREAM504 message -- store-specific, not code-wide, and literally the same three stores (plus deathwishcoffee) the c2742/c2743 reputation-block measurement named, just observed as a proxy timeout instead of an explicit 403/429. **Fixed the structural gap, not just this instance:** `bin/actor-health`'s `inconclusive_blocked()` only recognized parenthesized storefront codes `(403)`/`(429)` (c2743), so this proxy-level shape fell through to FAILED. Added `PROXY_UPSTREAM_CODE` matching `UPSTREAM(\d{3})`, gated to `{502, 504}` only (the two codes actually measured live: 502 at c992/trademark-search-scraper's h913/h825/h826, 504 here) -- deliberately NOT 503, since that would just be the storefront's own excluded 503 relayed through the proxy wrapper. Verified the new logic against 4 cases (the real captured UPSTREAM504 reason -> True; a genuine unrelated error string -> False; the old 403 case -> still True; a storefront 503 -> still False, confirming the exclusion held), then re-ran full-fleet `actor-health --all`: **24/24 ok**, `shopify-products-scraper` itself back to `ok: True` (allbirds cleared within the hour, consistent with "time-varying"). No Actor code changed, no README edit owed (no customer-facing defect, unlike the c3356 steam-reviews precedent this resembles in shape).
- [ ] **NEW c3360 (LOW-MEDIUM, cheap mechanization of a rule that is now broken 3 times out of 3 -- do NOT let it block a triage batch).** The vendor-catalogue tracker's `Per-batch results, one line each` line has been re-paragraphed by the triage cycles following EVERY one of the last three trims: c3348 fixed c3340/c3341, c3353 fixed c3349-c3352, c3360 fixed c3354/c3355/c3358/c3359 (4,529B of the 10,314B line). The rule is stated twice inside the block itself and tightened once (c3320) and that has not worked, so the next attempt should be a checker, not stronger prose. **Cheapest version: extend `bin/check-doc-size` with one extra warning -- split `tasks/queue.md`'s `Per-batch results` line on the `/\bc3\d{3} rows /` boundary (the exact regex `bin/_trim3360q.py` already uses) and warn when any entry exceeds ~500B, naming the offending cycles.** That is ~15 lines, runs in the existing 24-cycle `check-doc-size` cadence that already reads this file, needs no new state and no network, and it would have caught all three breaches in the cycle that caused them instead of 5-6 cycles later at ~1.5KB/batch. **Generalize only if it is free:** the same entry-size warning applied to any `one line each`-labelled line would cover future trackers built on this pattern. Do NOT instead try to stop triage cycles writing full narrative -- that narrative is correct and belongs in `state/STATUS.md`; the defect is purely that it also gets pasted into the compressed line.

- [x] **CLOSED c3353 -- regular/build slot (3353 % 3 == 2, verified with `echo $((3353 % 3))`). Preflight fully clean on arrival (tree clean, c3352's `f0f89da2` present in `git log`; `audit-due --all` **FLEET ROTATIONS NONE DUE** (only informational one-off/experimental axes, c1304 rule); `inbox-triage new` **NONE UNTRIAGED** (83 msgs, 0 new); both watched Actors still **plateaued** -- `trademark-search-scraper` 759/7, `eu-ted-tenders-scraper` 103/1 -- no owner email owed. `checks-due --all` **NONE DUE** (soonest `check-dead-endpoint-docs` in 2c).** `check-doc-size` read `tasks/queue.md` **TRIM DUE at 185.6KB/1056ln, ~3 cycles of headroom** -- exactly `STANDING c3280`'s own c3353-c3356 trigger window, so this was a trim cycle by the number as well as the banner. `bin/_trim3353q.py` made two cuts, in census order. (1) The 5 oldest of 10 live report blocks (c3347/c3346/c3345/c3344/c3342, contiguous lines 11-40), keeping the newest 5 (c3352/c3351/c3350/c3349/c3348) which this cycle's own block makes 6 -- the documented floor, same precedent as c3348. (2) **The predicted one: the `PARTIALLY DONE` vendor-catalogue tracker, 18,649B, up from 16,041B at c3348 -- the ~1.5KB/batch regrowth held for 4 more batches.** Its `Per-batch results` line alone was 9,234B because c3349/c3350/c3351/c3352 were each appended as full paragraphs again, in breach of the block's own one-line-per-batch rule -- the identical regrowth shape c3348 fixed last time on a different set of batches. All 4 archived verbatim, replaced with one-liners matching the established style of every older batch on that line. 3-pass hazard grep run first: passes (a)/(b) only the standing false positives; pass (c) found no dangling pointer this time -- every other mention of c3347/c3346/c3345/c3344/c3342 in the file is self-contained ("c3347's `54fbbfe7` present in `git log`" style), not a "see CLOSED cNNNN above" reference, so no repair was owed. Losslessness asserted in the script and re-verified against the written files. Guards: no code/pricing/charge-event change (pure doc maintenance), so `check-registry-fields`/`check-charges`/`sync-apify-prices` not re-run. All 3 services active; `/`, `/tools`, `/pricing` all **200**. **Spend: $0.** **Blockers: none. Owner email: none owed.** **Pace: 0 new Actors built today (2026-11-17). Next cycle: resume `NEW c3162` triage at rows 383-388 if nothing else is due; `NEW c3348`'s counter reconciliation remains a cheap alternative.**

- [x] **CLOSED c3356 -- regular/build slot (3356 % 3 == 2, verified with `echo $((3356 % 3))`). Preflight fully clean on arrival: tree clean, c3355's `f1ca814b` present in `git log`; `audit-due --all` **FLEET ROTATIONS NONE DUE** (only informational one-off/experimental axes, c1304 rule); `inbox-triage new` **NONE UNTRIAGED** (83 msgs, 0 new). `checks-due --all` had **1 DUE: `channel-mix`** -- ran and recorded it (clean, next due c3692, full numbers in `NEW c3356` above and STATUS.md). But the full-fleet `actor-health` sweep came back **19/20 ok and `steam-reviews-scraper` FAILING** (`ok: false, items: 0, status: 201, err: '[]'`), which took the cycle over the standing `NEW c3162` triage fallback -- correctly, because it turned out to be a live customer-facing defect rather than the outage it looked like.**

  **Triage: NOT an Actor outage, and not a flake.** Reproduced on a second sweep (identical 0 items), then read the platform run log: `WARN review page 1 failed for 1145360: steamcommunity.com returned HTTP 503` -- a transient upstream outage, confirmed live with `curl` (steamcommunity.com review pages 503 at 23:10, serving again by 23:17; the 22:02/22:33 sweeps passed and the 23:17 run delivered 10 rows, so the window was ~15 min). The run was marked **SUCCEEDED**.

  **THE REAL FINDING -- the Actor told the buyer a factual lie about Steam's data, and billed it as a success.** After the 503 the log printed: `App 1145360 has no Steam reviews at all yet (that is Steam's data, not a scrape failure).` App 1145360 is **Hades**, with ~200k reviews. Two independent root causes, both reproduced live before touching code:
  1. **`getReviewTotals` manufactured a confident zero from a degraded response.** `src/main.js:633` summed the `appreviewhistogram` buckets and trusted the result. Probed live during the outage: `store.steampowered.com` (a DIFFERENT host, so it stayed up) answered **HTTP 200** with `{"success":1,"results":{"start_date":"1575997560","end_date":"1575997560","weeks":[]}}` -- **no `rollups` key and an empty `weeks`**, which sums to `totalReviews: 0`. The zero-row branch read that explicit 0 and earned the "no reviews at all yet" claim. `getReviewTotals` already returned `null` on a throw, which is why this was never caught: the failure mode is a 200 with an empty body, not an error.
  2. **A page-1 fetch failure was swallowed and never reached the zero-row reporting.** `src/main.js:858`'s `catch` logged a WARN and `break`-ed, so the caller saw only `got === 0`, filed the app under `emptyIds` ("Steam answered, with nothing") and reported an empty SUCCESS. The architecture already had the right mechanism -- `upstreamDegraded` -> `runError` -> `Actor.fail()`, built at h250 precisely so "an upstream fault that produced nothing is a failed run, not an empty one" -- but a hard 5xx on page 1 was the one path that never fed it. The existing `degenerate` check only catches a fetch that SUCCEEDS with 0 cards.

  **Fix shipped, build 0.1.111** (`package.json` 0.1.30 -> 0.1.31; two pushes, the second only to normalise the quoted error string -- see below). (a) An empty histogram is now **unknown (`null`), never a zero** -- an app that genuinely has no reviews is indistinguishable from a degraded response, so the confident claim is only printed when Steam returns a real bucket-backed 0; both callers already handled `null`. **This also fixed a silent data-quality bug in `games` mode**, which was shipping `totalReviews: 0` rows for degraded apps and now correctly nulls the fields with a warning. (b) New `firstPageError` carried out of `scrapeReviews` into a new **`fetchFailed` bucket** (kept separate from `upstreamDegraded` per the file's one-bucket-per-cause convention: "Steam is down" and "Steam answered oddly" are different buyer actions), wired into `runError`, `markIncomplete('fetch-failed')`, `degradedSuffix`, the partial-success `partialCauses` chain (for a multi-app run where other apps DID deliver) and `RUN_SUMMARY.fetchFailed` as `[{id, reason}]`.

  **Verified both branches, not just the happy one.** Healthy path on the **deployed** build 0.1.111: `run-sync` delivered 10 rows, SUCCEEDED, no regression; `actor-health --only steam-reviews-scraper` back to **`ok: true, items: 10, fail_rows: 0`**. Fault path by **injection**, since Steam recovered mid-cycle and the 503 could no longer be reproduced through the real upstream: appended `127.0.0.1 steamcommunity.com` to `/etc/hosts` (backed up first, **restored and `getent`-verified immediately after each of the two runs**) and ran the shipped source locally -- the false "has no reviews at all yet" claim is **gone**, the new WARN names the real cause and explicitly disclaims any statement about review count, the run **FAILS** instead of succeeding, `RUN_SUMMARY.fetchFailed` is populated and `emptyIds` is correctly **empty**. The injected TLS error exposed one cosmetic defect the common 503 case would have hidden -- OpenSSL messages carry embedded newlines, so the status message rendered as `...SSL alert number 80\n)` -- so the reason is now whitespace-normalised and capped at 200 chars (a multi-app outage concatenates one per app into a single-line status message); re-verified clean, which is what the second push bought.

  **README: the FAQ claim this defect falsified is now true again.** `README.md:345` ("My run returned zero reviews for a game I know has thousands") promised that the Actor fails the run on an upstream fault so **"a zero-row *successful* run always means your filters or the game, never a silent Steam outage"** -- which today's run disproved, since the FAQ only ever covered the `success: 1`-but-empty shape, not a hard 5xx. Rewritten to name **both** failure shapes, point at `RUN_SUMMARY.fetchFailed`, and disclose the 0.1.31 change including the wrong-`totalReviews` games-mode bug. Live README verified **byte-identical** (77,316 chars both sides, under the 100k truncation cliff). `check-registry-fields` **0 drift** and `check-charges` **27/0/0** run after the output-field change, per the PLAYBOOK step-7 rule.

  **Spend ~$0.01** (two builds at ~$0.005) + ~6 platform runs + read-only API/checker calls. 0 new Actors today. Not escalated to the owner: no revenue event and nothing only they can fix. Two follow-ups filed above (`channel-mix` unclassified rows; fleet-wide screen for both halves of this defect class). Durable lesson in `notes/LEARNINGS.md` c3356.

- [x] **DONE c3356 — FIX FAILED ACTORS (nightly health 2026-11-17): steam-reviews-scraper.** Root cause was NOT an Actor outage: `steamcommunity.com` was serving HTTP 503 for ~15 min (transient, recovered during the cycle; the 22:02/22:33 sweeps passed, 23:04/23:09 failed, 23:17 delivered again). The real finding is the **customer-facing defect the 503 exposed**, fixed and shipped as build 0.1.111 — see `CLOSED c3356` below.

- [ ] **NEW c3356 (MEDIUM — `channel-mix` follow-up, no deadline; next scheduled `channel-mix` is c3692, so do this off-cadence or not at all).** This cycle's due `channel-mix` run was clean and recorded, but `unclassified` is back to **40.4% (6,615/16,359)** from the 31.4% c3020's fixes achieved, and the histogram the script's own docstring orders you to read has **two rows far too big to leave unexamined**: (1) **1,220 hits with a blank UA (`-`)** and (2) **1,206 hits on `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36` — truncated, with NO `Chrome/x` or `Safari/x` suffix**, which no real browser sends. Deliberately NOT classified this cycle: the c3020/c2012 bar is that a bucket change needs **behavioural** evidence (path mix, 404 rate, IP concentration, whether it ever fetches `/static/*`), and the headline AI:SEARCH ratio gets quoted for 300+ cycles, so a guess is worse than an honest `unclassified`. Method to use: group both rows by source IP and request path over the 7d window, then rule — a scanner fleet (high 404s, dictionary paths) belongs in `scanner` via `SCANNER_UA`/`SCANNER_PATH`, a breadth-first walker in `other_bot`, and only per-query content fetching in `ai`. Note the 63-hit **`Mozlila/5.0`** row (misspelled, a long-known scanner fingerprint) as a likely easy `SCANNER_UA` win while in there.
  - Also worth recording when that runs: the c3356 ratio drop is **not** an AI-channel decline and should not be read as one. `ai` ROSE 2169 -> 2328 while `search` rose 343 -> 449; the ratio fell only because the denominator grew faster (classic search crawlers finally indexing the blog). Series: 7.86 (c1676) -> 6.67 (c2684) -> 6.68 (c2688) -> 6.32 (c3020) -> **5.18 (c3356)**.

- [x] **CLOSED c3357 — `NEW c3356` LOW fleet screen for the steam-reviews two-part defect class, taken on this QUALITY/GROWTH cycle (3357 % 3 == 0) as the item itself asked for. Result: 0 further instances found; class is NOT present elsewhere in the fleet.** **(a) catch-and-break swallowing a fetch error into a bare zero-row report:** grepped every `actors/*/src/main.js` for the exact pre-fix shape (`catch (e) { log.warning(...); break; }` with no reason propagated) — **0 matches fleet-wide**. Manually read every near-miss the broader grep surfaced: `apple-podcasts-scraper:1080` sets `failed = got === 0; pageError = true` before break and gates the `feedCeiling` claim on `!pageError` — already correct, same shape steam now has. `app-store-reviews-scraper:966,991` set `tally.storefrontError = e.message` before break, read by the caller — already correct. `google-news-scraper`'s two break sites are time-budget exits, not fetch failures (no claim-of-emptiness risk). **(b) an empty aggregate summing to a confident zero:** read all 3 named candidates plus everything `grep`-matched on `totalReviews|reduce(|histogram`. `app-store-reviews-scraper:744` already has `if (!total) return null` before trusting the histogram (comment at :775-780 shows this was deliberately hardened against the Mac-App-Store all-zero case). `google-play-reviews-scraper` never computes its own sum — `histogram`/`reviewsCount` pass straight through the `gplay` library's own response, nothing for this Actor to get wrong. `fda-recall-scraper:720-732` already fails the product-type closed (`markIncomplete('plan-request-failed')`, explicit "NOT evidence that no recall matched" comment) when the initial count probe comes back empty rather than reporting 0 scanned. **No code changes needed anywhere — the class was isolated to steam's two call sites, now both fixed in 0.1.111.** Closes the `NEW c3356` LOW item.
- [x] **CLOSED c3352 -- regular/build slot (3352 % 3 == 1, verified with `echo $((3352 % 3))`). Preflight fully clean: tree clean, c3351's `670c0f97` present in `git log`; `audit-due --all` **FLEET ROTATIONS NONE DUE**; `inbox-triage new` **NONE UNTRIAGED** (83 msgs, 0 new); both watched Actors still **plateaued** -- `trademark-search-scraper` 759/7, `eu-ted-tenders-scraper` 103/1 -- no owner email owed. `checks-due --all` had **1 DUE: `check-readme-samples`.**** Ran it: **CLEAN** -- 41 sample blocks, 106 prose bullets, 756 sample values type-checked across all 3 passes, **0 drift**; recorded (3016 -> 3352, next due c3688), `checks-due` now NONE DUE (soonest `check-real-fields` in 57c). **Then resumed `NEW c3162` triage at rows 377-382: 0/6 real undercutters,** all 6 genuinely new handles, all six `alaudinburki` -- the **third consecutive single-vendor batch** (c3350/c3351/c3352), all at 2 users. 3 category mismatches, bucket 2 (`openfda-adverse-events`/FAERS, `openfda-food-events`/CAERS, `drug-shortage-monitor`) -- cheaper than our ladder but a different openFDA endpoint, and **`fda-recall-scraper/README.md:310` already excludes that whole class by name**, so with c3350's drug-labels and c3351's device-events that is 5 rows across 3 cycles priced individually when one grep settles the family. 1 dearer-at-every-tier AND feature-dominated (`federal-register-monitor`, $0.001+$0.0001 start vs our flat $0.0008 no-start-fee, and its only pitch -- "new since your last run" -- is our `watchLabel`, `federal-register-scraper/README.md:61,90-102`). 1 dearer by 50x (`google-play-reviews` $0.005 vs our $0.0001). 1 bucket 3 + bucket 1 (`ats-jobs-multiboard`, 3 of our 12 ATS platforms, flat $0.001 ties only our FREE rung, dearer from Bronze up, plus a start fee). No README edit owed anywhere. **The durable output is a method fix, not the 0/6: added `STANDING RULING BUCKETS` bucket (8) "feature-dominated" plus TWO pre-screens that run before any price lookup** (grep the target README's generic scope-exclusion paragraph for the row's source noun; read the row's `description` for its selling point and grep our README for that feature) -- buckets 1-7 are all price/breadth-shaped, which is exactly why both kept being missed. Full reasoning in `notes/LEARNINGS.md` c3352. Updated the `PARTIALLY DONE` head (376->382, 1,109->1,103 remain), `Per-batch results` (+1 line), buckets line, and the `NEW c3162` resume pointer (-> rows 383-388). **`check-doc-size`: 181.3KB/1054ln/~4c BEFORE this cycle's doc writes, 185.5KB/1056ln/~3c AFTER them -- this cycle's own updates pushed the file ONTO `STANDING c3280`'s ~3c trigger. No re-trim taken here, but c3353 is a TRIM cycle by the NUMBER now, not just by the window.** Guards: no code/pricing/charge-event change (one read-only check + research + docs), so `check-registry-fields`/`check-charges`/`sync-apify-prices` not re-run. All 3 services active; `/`, `/tools`, `/pricing` all **200**. **Spend: $0** (read-only own-token Apify GETs; no runs, no builds). **Blockers: none. Owner email: none owed.** **Pace: 0 new Actors built today (2026-11-17). Next cycle: the `tasks/queue.md` trim is the expected pick (clone `bin/_trim3348q.py`, census first, do not skip hazard pass (c)); otherwise resume `NEW c3162` at rows 383-388 using the new pre-screens.**

- [x] **CLOSED c3351 -- QUALITY/GROWTH slot (3351 % 3 == 0, verified with `echo $((3351 % 3))`). Preflight fully clean: tree clean, c3350's `3037d611` present in `git log`; `checks-due --all` **NONE DUE** (soonest `check-readme-samples` in 1c); `audit-due --all` **FLEET ROTATIONS NONE DUE**; `inbox-triage new` **NONE UNTRIAGED** (83 msgs, 0 new); both watched Actors still **plateaued** -- `trademark-search-scraper` 759/7, `eu-ted-tenders-scraper` 103/1 -- no owner email owed. Nothing fleet-due, so resumed the standing `NEW c3162` triage fallback at rows 371-376.** All six rows from one vendor, `alaudinburki`: **0/6 real undercutters.** Three single-platform bucket-1 scope exclusions (`jobicy-jobs` -- 1 of `remote-jobs-scraper`'s 7 boards; `ashby-jobs-api`/`greenhouse-jobs-api` -- 1 of `ats-jobs-scraper`'s 12 ATS platforms each, both flat $0.0005/job, cheaper than our GOLD+ $0.0007 but scope-excluded regardless of price). Three category mismatches, bucket 1, niche-tagged on vocabulary alone (`openalex-funders` -- a research-funder directory, not NIH grants; `un-comtrade-trade` -- trade statistics; `openfda-device-events` -- MAUDE adverse-event reports, not the enforcement/recall data `fda-recall-scraper` reads, same shape as c3350's `openfda-drug-labels` miss on this same vendor). All 6 handles confirmed genuinely new (0 exact-handle hits). Updated `tasks/queue.md`'s `PARTIALLY DONE` head (370->376, 1,115->1,109 remain), `Per-batch results` tracker (+1 line), `NEW c3162` resume pointer (->rows 377-382). `tasks/queue.md` at 182.3KB -- inside the healthy band, no re-trim owed (next window stays c3353-c3356 per `STANDING c3280`). Guards: no code/pricing/charge-event change (pure research + doc update), so `check-registry-fields`/`check-charges`/`sync-apify-prices` not re-run. All 3 services active; `/`, `/tools`, `/pricing` all **200**. **Spend: $0** (read-only own-token Apify metadata GETs only). **Blockers: none. Owner email: none owed.** **Pace: 0 new Actors built today (2026-11-17). Next cycle: resume `NEW c3162` at rows 377-382 if nothing else is due; `NEW c3348`'s counter reconciliation remains a cheap alternative.**

- [x] **CLOSED c3350 -- regular/build slot (3350 % 3 == 2, verified with `echo $((3350 % 3))`). Preflight: tree clean, c3349's `b77870f6` present in `git log`; `audit-due --all` **FLEET ROTATIONS NONE DUE**; `inbox-triage new` **NONE UNTRIAGED** (83 msgs, 0 new); both watched Actors still **plateaued** -- `trademark-search-scraper` 759/7, `eu-ted-tenders-scraper` 103/1 -- no owner email owed. `checks-due --all` had **3 fleet checks DUE NOW: `check-row-floor`, `check-upstream-warnings`, `check-source-endpoints`.**** Ran all 3. `check-row-floor` flagged `sec-insider-trades-scraper` (8/10 vs its own best, on a 16.5h-old snapshot) -- `--recheck` ran a fresh capped run and **CLEARED it** (8/10 live, weak-test-input not an outage). `check-upstream-warnings`: 23 niches, 12,240 listings, **CLEAN**, 9 standing acks unchanged. `check-source-endpoints`: 50 hosts, **0 deviations**. All 3 recorded via `checks-due --ran`; re-run confirms **NONE DUE** (soonest `check-readme-samples` in 2c). **Then resumed `NEW c3162` triage at rows 365-370: 0/6 real undercutters.** Two `adaptive_nightmare/*` Show HN/Ask HN radar clones dearer at every tier vs `hacker-news-scraper`. `adaptive_nightmare/remoteok-jobs-radar` (RemoteOK only) bucket-1 scope-excluded + only beats our FREE tier. `agentsgearbox/remote-jobs-scraper` (6 boards+HN-hiring, $0.0006 flat) genuinely undercuts our ladder but is bucket-7 dominated by the already-disclosed `datahamster/remote-jobs-aggregator` (cheaper, no start fee, near-identical scope). `agentsgearbox/company-jobs-scraper` (9/12 ATS platforms) bucket-1 scope-excluded + only beats FREE tier. `alaudinburki/openfda-drug-labels` is a category mismatch (drug labels, not recalls) despite the catalogue's niche tag. All 6 handles confirmed genuinely new (0 exact-handle hits). Updated `tasks/queue.md`'s `PARTIALLY DONE` head (364->370, 1,121->1,115 remain), `Per-batch results` tracker (+1 line), `NEW c3162` resume pointer (->rows 371-376), and filed a note on the `cps` module ambiguity (`check-price-superiority` vs `_unit_price.py`) that cost a few minutes this cycle. `check-doc-size`: `tasks/queue.md` 174.3KB/1050ln, ~5c headroom -- inside the healthy band per `STANDING c3280`, no re-trim taken despite the TRIM DUE banner (next window stays c3353-c3356). Guards: no code/pricing/charge-event change (checks + research only), so `check-registry-fields`/`check-charges`/`sync-apify-prices` not re-run. All 3 services active; `/`, `/tools`, `/pricing` all **200**. **Spend: $0** (read-only GETs + 1 capped recheck run). **Blockers: none. Owner email: none owed.** **Pace: 0 new Actors built today (2026-11-17). Next cycle: nothing due until `check-readme-samples` in 2c; if nothing else is due, resume `NEW c3162` at rows 371-376; `NEW c3348`'s counter reconciliation remains a cheap alternative.**

- [x] **CLOSED c3329 (`devto-post`, using this note's own measurements -- closes the item below).** Drafted `notes/devto_article_24.md` per the suggested thesis (apex-404 bug first, then the teaser-field inversion, then the smaller paging/token changes, then what held + the mutable `wordcount`), dry-ran `bin/devto-post`, verified the canonical URL (`/blog/substack-full-text-json-api`) live 200, published: **devto id `5055990`, HTTP 201**, `ai_disclosure_level: fully_autonomous` confirmed, article page verified live 200 post-publish. Recorded `checks-due --ran devto-post` (next due c3425). Re-derived `state/devto_syndicated.json` whole-file from a live `GET /api/articles/me/published`: 95 site posts, 35 synced (was 34), 60 unsynced, 0 unmatched, 0 rows lost, exactly 1 added -- diffed old vs new slug sets to confirm. Also re-read the two newest owner emails about the Apify security-incident token rotation (`9be9604c`/`f11632f7`, 2026-11-11) -- already resolved, since c3326-c3328 made live successful Apify API calls under the replacement token; no action needed.

- [x] **CLOSED c3336 -- owner confirmed money accrued.** Owner replied (`fb22b1b1`, 2026-11-17, triaged `owner`): *"Yes in the insights I can see profit of $36."* This is the **first confirmed real revenue in the business's history.** Re-measured c3337: `trademark-search-scraper` still growing (759 runs30d now, was 731 this morning), competitive position already strong (closest rival `scrapers_lat/tmview-global-trademarks-scraper` 6-7.5x dearer), no site-traffic signal to act on (Polar stays deferred), Actor itself needs no immediate build work (full 81-office coverage, 22 fields, watch mode, exhaustive README already in place). **No further owner email owed** -- they answered the ask; CLAUDE.md's booked-revenue email trigger is about notifying them, not re-confirming what they told us. **Standing instruction for future cycles: check `bin/usage-trend` on `trademark-search-scraper` specifically every cycle (not just the fleet scalar) so the next real signal -- growth, reversal, or a new undercutter -- is caught same-cycle.** Full detail in `state/STATUS.md` cycle 3337 entry. Resume `NEW c3162` triage as the default fallback; it is not superseded, just no longer the only thing worth checking first.

- [x] **CLOSED c3336b -- resolved alongside c3336.** The 27 FAILED runs stayed frozen (not growing) through c3337's re-measurement; still a one-day 2026-11-09 ramp-up artifact, not a live breakage. No action was ever owed; closing with c3336 since both were read from the same per-Actor decomposition. Durable lesson already in LEARNINGS.md: decompose `ext_bad30d` per-Actor, never read the fleet scalar alone.

- [ ] **NEW c3328 (HIGH -- `devto-post` is STILL DUE; the syndication was deliberately deferred, and all its live measurements are recorded here so the next cycle does NOT have to re-probe). DONE -- see `CLOSED c3329` above; keeping this note for its measurement detail until the next trim.** `devto-post` fired at c3328 and the chosen candidate was the unsynced site post `substack-full-text-json-api` (2026-09-11). Per the c2656 standing rule its claims were re-measured live FIRST -- and the first two probes turned up a **live customer-facing bug in `substack-scraper`**, which took the cycle (see `CLOSED c3328`, archived by c3348 -- `tasks/queue_archive.md`, `## Archived by cycle 3348`). The article itself was NOT written or published, so **`checks-due --ran devto-post` was deliberately NOT recorded** and the check stays DUE -- that is intentional, not an oversight. **Everything measured live on 2026-11-17 (two independent publications, `astralcodexten` + `bigtechnology`), ready to write up as-is:** (1) archive endpoint returns `{posts, nextCursor}`, NOT a bare array; `offset=0` -> `400 {"errors":[{"location":"query","param":"offset","value":"0","msg":"Invalid value"}]}`; `nextCursor` base64-decodes to `{"post_date":"2026-10-26T20:16:14.835894Z"}` (keyset paging). (2) `truncated_body_text` is `null` on all 12 `astralcodexten` rows but populated on **20 of 23 `only_paid` rows and 0 of 2 free rows** on `bigtechnology` -- teaser text for posts you CANNOT read, nothing for posts you can; the exact `royce-on-san-francisco` row the post printed is now `audience: everyone` with `truncated_body_text: None`. (3) apex custom domains 404 (`Server: Apache`, 17 bytes) while `www.` serves JSON directly with **no redirect** (`code=200`, empty `redirect_url`) -- on BOTH publications. (4) comments `token=` requirement GONE: omitting it returns `200` with the identical 313,000 bytes; response now also carries `automod_hidden_comments` (empty list on the post sampled). (5) **HELD byte-identical 2 months on:** `body_html` `null` on every archive row, `body_json` `null` too, single-post `/api/v1/posts/<slug>` returns exactly **14,799 chars** for `royce-on-san-francisco`; `sort=search` still `400` (error object now also carries a `value` field); `sort=new&search=AI` still returns the same two titles ("God Help Us, Let's Try To Understand AI Monosemanticity", "Make A Personalized AI Kids' Book"); global `substack.com/api/v1/post/search` still `200` with an empty result set (shape now `{focused,results,resultsWithTrackingParams,more,publications}`); comment `children` tree with no `parentCommentId`. (6) **`wordcount` is MUTABLE on an unchanged post: 3812 -> 2393** while `body_html` stayed byte-identical at 14,799 chars, and 2393 is the accurate one (rough tag-strip counts ~2397) -- so the figure we published in September was wrong when published. **Suggested dev.to thesis** (strongest angle, and it is a correction post like c3136/c3232): *"We documented Substack's public archive API in September. The redirect we told you to follow is now a 404 -- and the teaser field inverted."* Lead with the apex-404 finding because it is the one that silently broke real code (ours). The site post already carries a dated `> Correction, 2026-11-17` blockquote naming all four changes, so the dev.to version should cite and extend it, not repeat it. Draft to `notes/devto_article_24.md`, dry-run `bin/devto-post`, verify the canonical URL 200s BEFORE `--publish`, then re-derive `state/devto_syndicated.json` whole-file and diff for lost rows.

- [ ] **FOLD-IN REGISTER (consolidated c3348 from 8 separate items -- `NEW c3304`, `NEW c3311`, `NEW c3319`, `NEW c3321`, `NEW c3327`, `NEW c3334`, `NEW c3335`, `NEW c3340`, 16.0KB combined; each one's FULL text is verbatim in `tasks/queue_archive.md`, `## Archived by cycle 3348`, and every handle below is exact so a grep still finds it). Vendor-catalogue findings waiting on an Actor's NEXT `competitor_audit` rotation. None is published as an off-cycle README edit -- that is the standing ruling for scope-excluded and bucket-7 finds.**

  **`remote-jobs-scraper` -- SEVEN pending** (our baseline: a flat-across-7-boards `job` event, **$0.0015 FREE -> $0.0013 BRONZE -> $0.0011 SILVER -> $0.001 GOLD+**; rotation lands ~c3471). (1) **`nomad-agent/dynamitejobs-scraper`** (c3327, 3u) -- **~90-95% under us at every tier** ($0.0001 FREE/BRONZE -> $0.00005 GOLD+) **and a genuine COVERAGE GAP**: Dynamite Jobs is not one of our 7 de-duplicated boards. The steepest of the seven and the only one that is also a product gap. (2) **`hipersoft/himalayas-scraper`** (c3319, 3u) -- Himalayas only, $0.001 -> $0.0005, **~33-50% under, no crossover**. (3) **`kadi_bence/remote-jobs-scraper`** (c3321, 4u) -- 5 of our 7 boards, $0.0009 -> $0.00072, **~28-40% under, no crossover**. (4) **`accountable_eel/himalayas-jobs-lookup`** (c3335, 1u) -- Himalayas only, $0.001 -> $0.0005, **~33-50% under**; beats the already-disclosed `vital_tuxedo/remote-jobs-feed` (which only TIES our Gold+) outright; its $0.003 start fee amortizes away. (5) **`unfenced-group/remoteok-scraper`** (c3334, 3u) -- Remote OK only, $0.00099 -> $0.00059, **~19-41% under**, negligible start fee. (6) **`accountable_eel/workingnomads-jobs-lookup`** and (7) **`accountable_eel/remoteok-jobs-lookup`** (c3334, 2u each) -- one board each, $0.001 -> $0.0005 per-unit (~33-50% under) **but a $0.0015 start fee means they only cross below us past ~3-4 jobs/run**, the same shape already documented for `automation-lab/omni-jobs-board-scraper`. **Handle these as ONE per-board pricing pass, not seven lines:** (2), (4), (6) and (7) are the same `accountable_eel`-style one-Actor-per-board clone strategy (full-range undercut plus a start fee), so the rotation's real question is whether we can match any single-board price without discounting the other 6 boards. **Awareness-only (bucket 7), do NOT name unless the README's undercutter list is being refreshed anyway:** `actor-forge/remote-jobs` (c3340, 2u, flat $0.0008/job, 4 of our 7 boards) is a real every-tier undercut but is dominated by two still-live already-named rivals (`nivlekk/remote-jobs-aggregator` $0.0005, `silicatelabs/JobsFlow` $0.00001) and our README already states outright that we are not the cheapest listing in this niche.

  **`ats-jobs-scraper` -- TWO pending** (baseline: flat `job` **$0.001 FREE -> $0.00085 BRONZE -> $0.00075 SILVER -> $0.0007 GOLD+**). (1) **`deepmine/workable-jobs`** (c3311, 1u) -- Workable only (1 of our 12 platforms), $0.00059 -> $0.00035, **~41-50% under at every tier, no start fee, no crossover**. (2) **`tidytools/ats-career-site-jobs`** (c3304, 7u, 140 runs30d) -- **NOT a price undercut** (ties our FREE, dearer at every tier below it), and that is exactly why it matters: **the gap is the INPUT SHAPE, not the price.** It auto-detects the ATS from a bare company domain (`stripe.com` works as input) across 21 claimed platforms, while ours needs the company SLUG (`README.md:50`) -- the first rival to combine domain-level auto-detect AND 20+ platforms AND a price that ties ours. `check-price-superiority` will never surface it.

  **`app-store-reviews-scraper` -- ONE pending.** **`wulfcare/app-store-reviews-scraper`** (c3304, 4u) is the **third** listing to claim no-500-cap depth, after the still-live `sourabhbgp` (already disclosed honestly at `README.md:617`) and the delisted `gh0st1k` (`README.md:482`) -- **the claim SHAPE is already generically disclosed, so no urgent edit is owed.** Worth a rotation paragraph for one reason: its own README admits `appVersion` is present "for the newest 500" only, i.e. **its deep path returns a REDUCED field set**. If that holds, the honest comparison is "they go deeper with fewer fields" rather than "they go deeper and we do not" -- materially better for us and **cheap to check** (one run of theirs, or just read their schema). Not a price undercut either: flat $0.0001/review ties our FREE and is dearer than our $0.00009/$0.00008/$0.00007.

  **`eu-ted-tenders-scraper` -- nothing owed.** `actor-forge/eu-tenders` (c3340) is the tightest scope match found against it so far (TED notices + awards + CPV/country/value filters + a monitoring mode) but **ties our flat $0.0015 at every tier and adds a $0.00005 start fee we do not charge** -- textbook bucket 3, recorded here only so the next triage does not re-derive it.

---

---

- [ ] **STANDING c3296 (new, replaces the `state/STATUS.md` half of the c3294/c3295 DOC-SIZE handoff, which is now CLOSED) -- `state/STATUS.md` doc-size cadence, arithmetic written down so no future cycle re-derives it.** Post-c3296-trim state: **43.8KB / 101 lines / 9 live blocks** (c3295..c3287), which c3296's own prepended block lands at exactly **10 -- the documented floor**. `check-doc-size` projects **150KB at its next 24-cycle look (~35 cycles of headroom)**, i.e. right at the 150KB WARN line and nowhere near the 200KB TRIM line. **Re-trim around c3320-c3330, not sooner.** **Expect `TRIM SOON`/WARN at the next look and do NOT read it as a failed trim** -- 10 live blocks is a HARD FLOOR, so c3296 already took the deepest legal cut; there is no deeper cut available at any future date either, which means this file will always re-warn roughly one check-interval after each trim. The real decision rule, same as queue.md's: **re-trim when headroom drops below ~3 cycles, not when the banner says DUE.** Method: clone `bin/_trim3296s.py` (which is itself a clone of `_trim3266s.py`), keeping (a) the fresh per-block census, (b) all three hazard-grep passes with pass (c) the intra-file one, (c) the multiset-identity assert before the write and an independent re-verify against `git show HEAD:...` after, and (d) a boundary assert on the exact header text of the first cut line so a drifted line number fails loudly instead of silently cutting the wrong place. **Keep the newest 9 blocks and let your own block make 10** (c3144's reasoning); c3208/c3237/c3266 instead kept 10 and ended at 11, which is also fine but wastes a block of headroom. ~~`tasks/queue.md`~~ is tracked separately in `STANDING c3280` below (re-trim ~c3324-c3327 after the c3320 trim; do not read a cadence number out of this item, it goes stale). **LESSON FROM THE GAP, important: nobody actually re-trimmed at the c3320-c3330 window this item named -- the file grew unwatched for ~50 more cycles until `check-doc-size` hit `TRIM DUE` at ~-12 cycles of headroom (254.2KB/592ln) by c3347, far past the ~3-cycle trigger every other trim in this file respects.** `DONE c3347` (`bin/_trim3347s.py`, template to clone next): archived the 51 oldest of 60 live blocks (c3337 down to c3287, 214.1KB) to `state/STATUS_ARCHIVE.md`, keeping the newest 9 (c3346..c3338) so c3347's own prepended block lands at exactly **10 -- the floor**. New state: **45.1KB / 95 lines**, `check-doc-size` projects ~151KB at its next 24c look (~35 cycles of headroom). **Re-trim around c3382-c3392, not sooner -- and this time, actually check it at that window rather than letting the banner sit unread.** Filed the staleness itself as a `notes/LEARNINGS.md` entry (cycle 3347) so future cycles treat a `check-doc-size` banner on this file as a real signal, not routine noise to skip past.

- [ ] **NEW c3292 (TRIVIAL/checker precision -- saves a future cycle from chasing four non-defects, and from a typo'd flag that fails silently).** Two findings from the `check-code-fields` work below. **(1) The `soft: declared but no literal emits it` half of `check-code-fields` is NOT evidence of a missing column** -- it only scans **record LITERALS**, so a field set by PROPERTY ASSIGNMENT or merged via a SPREAD is invisible to it. All four softs standing today are false positives, each hand-traced this cycle: `ats-jobs-scraper`'s `scrapedAt` (`job.scrapedAt = ...`, `src/main.js:1850`), `watchEvent` and `previousHasSalary` (`item.watchEvent = ...` / `item.previousHasSalary = ...`, `:460`/`:461`/`:479`/`:480`) and `google-news-scraper`'s `tickers` (a single-key literal `{ tickers: [...] }` at `:589` spread into the row at `:591`, below the record-shape overlap threshold). **`scrapedAt` was additionally confirmed PRESENT on every row of 12 live run datasets this cycle, so the soft flag is provably wrong, not merely unproven.** Treat the soft line as informational unless a live dataset read (`bin/check-real-fields`, the authoritative tool for "did it reach the dataset") also shows the column missing. **(2) `bin/check-code-fields` silently no-ops on an unrecognised flag.** `main()` strips only `--all` and treats every other argv entry as a SLUG FILTER (`:286-290`), so `--show-all` (a plausible typo -- the internal variable really is called `show_all`) matched no Actor, printed zero Actor lines and exited **0** with `0 Actor(s) with code-only field drift.` -- indistinguishable from a clean fleet. Cost ~1 minute this cycle. If tightened, make an unmatched `wanted` entry that starts with `-` a hard error; low priority, bias is visible-but-confusing rather than unsafe.

- [ ] **STANDING c3280 (replaces the archived c3266/c3267 doc-trim handoff; updated c3295, RE-COMPRESSED c3348 -- the full DONE narrative for c3296/c3305/c3306/c3309/c3320/c3324/c3332 is verbatim in `tasks/queue_archive.md`, `## Archived by cycle 3348`) -- `tasks/queue.md` doc-size cadence, with the arithmetic written down so no future cycle re-derives it.** **THE DECISION RULE: re-trim when headroom drops below ~3 cycles, NOT when the banner says DUE.** `check-doc-size` projects **24 cycles ahead**, so it prints `TRIM DUE` on this file at any size above roughly 70KB -- that is not a failed trim and is not a reason to re-trim. A healthy post-trim landing is **~160-170KB / ~6-7 cycles of headroom**; growth runs ~5.4KB/cycle. **AND IF THE PREDICTED WINDOW PASSES WITHOUT A TRIM, TREAT IT AS OVERDUE IMMEDIATELY** -- c3348 arrived 8-11 cycles past the c3337-c3340 window this item named, at ~-2 cycles of headroom, the identical staleness failure c3347 hit on `STANDING c3296`'s STATUS.md window one cycle earlier. Two for two: the window is a trigger, not a hint. **Method, in the order that actually pays** (`bin/_trim3348q.py` is the template to clone): (1) run a **per-block byte/line census** FIRST (`grep` every `- [ ] **`/`- [x] **` head, sum bytes between heads) -- c3280 found a 33.1KB non-report block that 4 prior cycles of report-block-only thinking had never looked at, worth more than all 10 report blocks combined; (2) re-derive the report-block count **FRESH**, never from a forwarded number, and remember they are **not** a chronological prefix (live `NEW cNNNN` items are interleaved between them, and standing one-off closures like `CLOSED c3329`/`c3336` are not reports at all); (3) **3-pass hazard grep, and do not skip pass (c), the intra-file one** -- passes (a)/(b) have returned nothing but the same known false positives for ~25 trims, while (c) has found a real dangling pointer on c3306, c3309, c3320, c3324 and c3348; (4) assert multiset identity in the script AND re-verify losslessness against the written files afterwards. **Three lessons the DONE history earned, kept here because they are method, not history:** (a) **a block that was compressed before is a PRIME census candidate, not a solved problem** -- c3320 found the vendor-catalogue tracker at 21KB on ONE line, more than all 7 archivable report blocks combined, because every triage cycle appends ~1.5KB in defiance of the block's own one-line rule; c3348 found it back at 16KB and found THIS item at 9.1KB, so the rule now includes itself; (b) **the biggest block may not be a task at all** -- ask of every big block whether it is method/reference that belongs in `notes/PLAYBOOK.md` or `notes/LEARNINGS.md` (c3324 RELOCATED `COMPRESSED c3000`, 9KB of Store-search-ranking playbook content that had lived in the task queue for 324 cycles); (c) **compressing a stale tracker fixes correctness, not just bytes** -- c3320 found 3 stale counters and a duplicate resume pointer; c3348 found the tracker's two running-score counters disagreeing (17-in-340 vs 12-in-316) and filed `NEW c3348`. **DONE history, one line each (full narrative in the archive headers named above):** c3296 (the STATUS.md half, 195.4KB -> 44.8KB); c3305 (re-measure only, 188.7KB/~2c); c3306 (-> 168.8KB/~6c, 6 of 14 report blocks); c3309 (-> 164.5KB/~7c, 4 of 9, kept count dropped to the floor of 5); c3320 (199.8KB/**~0c** -> 162.9KB/~7c, the tracker cut, 21KB -> 7.3KB plus the `STANDING RULING BUCKETS` consolidation); c3324 (184.6KB/~3c -> 161.7KB/~7c, the PLAYBOOK relocation); c3332 (195.3KB/~1c -> ~165KB, 8 of 13 report blocks + the `NEW c3162` tail). **DONE c3348** (216.6KB/1086ln, **~-2 cycles of headroom**, 8-11 cycles late -> **169.6KB/1049ln, ~6 cycles of headroom**; 8 of 13 report blocks (30.7KB), the tracker a third time (16.0KB, regrown in BOTH its head line and its per-batch line), and this item itself (9.1KB of narrative -> the one-line history above); bucket (7) promoted into the tracker's ruling buckets; `NEW c3348` filed for the counter reconciliation; and **the 8 pending competitor-audit fold-in items** (`NEW c3304`/`c3311`/`c3319`/`c3321`/`c3327`/`c3334`/`c3335`/`c3340`, **16.0KB**) consolidated into the single `FOLD-IN REGISTER` above, with all 12 handles, their price ladders and their magnitudes kept live and greppable and the full items archived. **That cut was worth more than its bytes: 8 items were repeating the same preamble, the same 'do not publish off-cycle' ruling and the same baseline price ladder, and grouping them by TARGET ACTOR made the `accountable_eel` one-Actor-per-board clone strategy visible at a glance in a way 8 scattered items never did.**) **DONE c3353** (185.6KB/1056ln, ~3c -> 170.9KB; 5 of 10 report blocks + the tracker a 4th time, 18,649B, its `Per-batch results` line alone 9,234B because c3349-c3352 were each appended as full paragraphs again). **DONE c3360** (181.4KB/1050ln, **~3 cycles of headroom -- on the trigger, not past it, the first on-time trim since c3332** -> **165.2KB/1025ln, ~7 cycles**; -16.6KB in 3 cuts, verified lossless across THREE files). Its lesson: **the trim window must be read against the QUALITY-slot calendar, not the cycle counter.** c3360 was at exactly ~3 cycles of headroom, i.e. 'trim next time' by the letter of the rule -- but the next QUALITY slot was c3363, 3 cycles out, which projects to ~197KB/~0c. **So the real trigger is: trim on the LAST quality slot that still has headroom, which is always ~3 cycles EARLIER than the bare arithmetic says.** Both prior late trims (c3348 at -2c, c3347 on STATUS.md) are explained by this off-by-one, not by inattention. Content: the tracker a FOURTH time (19,741B) cut three ways -- 4 `Per-batch results` entries re-paragraphed (c3354/c3355/c3358/c3359, 4,529B vs a ~200-350B one-liner style, so **3 for 3: every triage cycle that follows a trim breaks the one-line rule**), the 4,493B `STANDING RULING BUCKETS` line RELOCATED verbatim to `notes/PLAYBOOK.md` (the c3324 move -- it was never a task), and the 2,501B `Running score` line cut to one line since `NEW c3348` already carries its open task; plus `COMPRESSED c2994`'s +7 CLOSED c3316 batch (3,631B) and the 2 oldest of 7 report blocks (c3349/c3348, 6,329B). **Next candidates, re-sized at c3360 (census re-run fresh):** `PARTIALLY DONE at c3250` (5.2KB -- still the live Rippling implementation plan, **keep until it ships**), `STANDING c3280` itself (5.6KB and growing again, 2 trims after its own compression -- the rule includes itself), `FOLD-IN REGISTER` (4.9KB, live debts), `FOLLOW-UP from c2380` (4.4KB), `NEW c3046` (4.3KB -- HIGH and live, do not cut), `NEW STANDING TRIPWIRE c2336` (3.8KB), `MERGED c2916` (3.4KB), `COMPRESSED c2994` (2.6KB after c3360). **Structural note, re-measured c3360: a report-block cut is now only 3.4% of this file (6.3KB of 181KB), so the c3348 note is confirmed -- the bulk of every future trim is inside live blocks, not at the top.** The next real lever is still a staged tail pass (~10 of the ~886-line tail's small LOW/TRIVIAL notes per cycle into one-line index entries + verbatim archive). **The vendor-catalogue tracker will regrow at ~1.5KB/batch -- budget a re-compression roughly every 5 batches regardless of what the banner says.** **Re-trim at the QUALITY slot c3363** -- and note HOW that number moved inside c3360 itself, because it is the same off-by-one in miniature: the cut landed at 165.2KB/~7c, but c3360's own report block (4.0KB), its `NEW c3360` item (1.6KB) and this item's own DONE paragraph (1.9KB) then added **7.4KB in one cycle, not the 5.44KB average** -- a trim cycle always writes the longest block in the file -- so the true post-cycle figure is **172.4KB/1030ln, ~5.1 cycles of headroom**, which puts the overrun at ~c3365 and makes c3363 (not c3366) the last quality slot with headroom. **LESSON FOR THE NEXT TRIM: size the cut against the POST-CYCLE total, i.e. subtract ~7-8KB of your own writing before declaring a landing zone -- aiming at 160-170KB post-cut means aiming at ~155-162KB pre-block.** c3363 is 3 cycles out, so if the queue has no cheaper work that slot, spend it on the staged tail pass named above rather than another small report-block cut.

- [ ] **NEW c3269 (LOW -- a cheap fleet-wide sanity check, not a known defect).** `check-store-meta` found 0 drift fleet-wide when run at c3269 (after the `ats-jobs-scraper` fix), so there is currently nothing else to fix -- but the fact that this exact gap sat live for 3 cycles (c3263->c3269) unnoticed shows the checklist habit, not the tool, was the failure. **Next time ANY cycle edits an Actor's title/description (not just a platform-count bump -- any Store-listing copy change), run `bin/check-store-meta` before closing that cycle, the same way `check-registry-fields` is already routine after an output-field change.** No code or doc change needed now; this is a process reminder, closeable once a cycle actually demonstrates running it as the automatic last step of a title/description edit.

- [ ] **NEW c3268 (TRIVIAL/method -- would have cost a cycle chasing working code).** **`GET /v2/acts/<id>/runs` list records do NOT carry `statusMessage`; only `GET /v2/actor-runs/<runId>` does.** c3268's audit run read `statusMessage: None` from the runs-list record and the full, correct `Pushed 2 results. maxReviewsPerPodcast (20) was hit while filtering: ...` from the single-run GET -- same run, seconds apart. Every `varied_test` checks what the buyer was *told*, so this misreads as a missing-disclosure defect on an Actor that is behaving perfectly. **Always read the status message from `/v2/actor-runs/<runId>` and cross-check the `[Status message]:` line in the run log.** Same family as `NEW c3136` (two requests are not one measurement) but the cause is an abridged API record, not endpoint state.

- [ ] **NEW c3268 (TRIVIAL/content -- a settled fact, so nobody re-measures it).** **`sort:"mostHelpful"` is NOT a deeper or materially different ordering on Apple's podcast reviews feed.** Measured 2026-11-16 on JRE: it places the same ten `propaganda` matches at depths 134/165/250/291/324/355/390/414/442/478 -- within ONE row of `mostRecent` -- because Apple returns the identical page-1 set with **`voteSum: 0` on every review**, so there is nothing for "most helpful" to rank by (page-1 id sequences differ in order, same 50-review set, 50/50 overlap). This was caught as a FALSIFIED DRAFT: c3268 had written "use `sort:'mostHelpful'` for an ordering that does not drift" into the README and one free curl loop killed it before the push. **Do not advertise `mostHelpful` as deeper/different coverage in any README, site page or article**; the measurement itself is now disclosed at `apple-podcasts-scraper/README.md:144`. Generalisable rule (in LEARNINGS c3268): **a remedy sentence is a buyer-facing claim and needs the same evidence bar as the finding it accompanies.**

- [x] **`NEW c3220b` SWEEP CLOSED at c3238 (MEDIUM, fleet-wide) -- `sort_order` 2x-reach sweep: COMPLETE, all 4 candidates measured, 0 shippable fixes found anywhere. The full 12.2KB record -- the per-endpoint method plus the `CLOSED c3227`/`c3229`/`c3230`/`c3238` measurements -- is archived VERBATIM in `queue_archive.md` under `## Archived by cycle 3240`** (compressed there by c3240's RULE 4 pass; `notes/LEARNINGS.md` cycle-3227/3229/3230/3238 entries carry the durable lessons). **The four outcomes, so no future cycle re-measures them:** `nih-reporter-scraper`/`projects` (c3227 -- mechanism valid, but the one tie-free sort key `appl_id` blows the run timeout at real offset depth; unshippable), `fda-recall-scraper` (c3229 -- mechanism clean AND fast, but the `MAX_SKIP` ceiling condition it would rescue never fires at real recall volumes), `apple-podcasts-scraper`/`app-store-reviews-scraper` RSS (c3230 -- NOT APPLICABLE: two non-reversible named orders, plus a hard server-side page-10 depth cap), `steam-reviews-scraper` store-search (c3238 -- NOT APPLICABLE: no sort knob exists at all, a bogus value returns byte-identical results). **Do NOT re-open any of these four.** Re-read the archived method only if a NEW offset-walled Actor ships -- and lead with c3230/c3238's cheap existence check (one bogus-value curl), which alone killed 2 of the 4 before any expensive symmetry proof.

- [x] **PARTIALLY DONE -- 412 of `NEW c3162`'s 1,485 vendor-catalogue rows triaged (c3167, c3217, c3218, c3239, c3241-c3244, c3246-c3248, c3253, c3255-c3261, c3269, c3277-c3290, c3297-c3343, c3349-c3355, c3358-c3359, c3361); 1,073 remain.** **Those batches' results live as ONE LINE EACH in the `Per-batch results` line below -- c3348 had to archive ~3.0KB of batch narrative out of THIS head line (c3335, c3338, c3340, c3341, c3343) to restore that, verbatim in `tasks/queue_archive.md`, `## Archived by cycle 3348`.** **RULE, tightened at c3320 because it keeps being broken: append AT MOST ONE LINE per future batch to this block.** The per-cycle detail paragraphs were compressed/archived once at c3280 and AGAIN at c3320 (`tasks/queue_archive.md`, `## Archived by cycle 3280` and `## Archived by cycle 3320`) -- the block had regrown to 20,986 bytes, 10% of the entire file and more than all 7 archivable report blocks combined, because each cycle appended ~1.5KB of narrative anyway. Every batch's full narrative ALREADY lives in that cycle's own `state/STATUS.md` record and its own `CLOSED cNNNN` block; do NOT duplicate it here. **Resume pointer lives in `NEW c3162` below and NOWHERE ELSE** -- this block used to carry a second copy, it went stale twice (c3317 repaired it once, and it was stale again at c3320 still reading "NEXT: rows 245-250" after 18 further rows had been read), so it has been deleted rather than repaired a third time.

  **Running score -- BOTH COUNTERS ARE UNRELIABLE, do not quote either as fact; the open reconciliation is `NEW c3348` below, and the NAMED FINDS in the per-batch line are the reliable record.** The tracker head read *17 real undercutters in 340 rows (~5.0%)* (last touched c3340) and this line read *12 in 316 rows (~3.8%)* (last touched c3332), against **406 rows triaged as of c3359**; neither has ever been re-derived, and c3348 deliberately labelled both in place rather than guessing (that is research, not a trim).  Full c3348 narrative: `tasks/queue_archive.md`, `## Archived by cycle 3348`; this line's own 2.5KB predecessor is under `## Archived by cycle 3360`. 

  **STANDING RULING BUCKETS -- RELOCATED c3360 to `notes/PLAYBOOK.md`, `## Vendor-catalogue triage -- the 7 standing ruling buckets`, VERBATIM with every cited precedent handle.** They are reusable method, not a task: 7 buckets (1 scope exclusion, 2 category/niche mismatch, 3 thin or tier-crossing price ties, 4 unmonetized/FREE, 5 near-miss, 6 start-fee shape, 7 dominated by an already-disclosed cheaper-or-equal rival), consolidated at c3320 from ~20KB of archived batch narrative, bucket 7 promoted at c3348.  **Reach for one of these before writing a new ruling.** 

  **Per-batch results, one line each (full narrative in each cycle's own `state/STATUS.md` record and `CLOSED cNNNN` block; the pre-c3320 verbatim paragraphs are in `tasks/queue_archive.md`, `## Archived by cycle 3320`, the c3335-c3343 ones under `## Archived by cycle 3348`, and the c3354/c3355/c3358/c3359 ones under `## Archived by cycle 3360`).** c3287 rows 161-166: 0/6. c3290 rows 167-172: 0/6. c3297 rows 173-178: **1/6** (`goat255`). c3298 rows 179-184: 0/6. c3299 rows 185-190: 0/6 (all six `publicmoney/*`). c3302 rows 191-196: 0/6. c3304 rows 197-202: 0/6 price, 2 non-price (`NEW c3304`). c3305 rows 203-208: 0/6. c3307 rows 209-214: 0/6. c3308 rows 215-220: 0/6. c3310 rows 221-226: 0/6. c3311 rows 227-232: 0/6 full-range, 1 scope-excluded undercutter filed as `NEW c3311`. c3313 rows 233-238: **1/6** (`factpipe`). c3314 rows 239-244: **1/6** (`gazidev`). c3315 rows 245-250: 0/6 (one thin crossover, bucket 5). c3317 rows 251-256: 0/6. c3319 rows 257-262: 0/6 full-range, 1 scope-excluded undercutter filed as `NEW c3319`. c3321 rows 263-268: 0/6 full-range, 1 scope-excluded undercutter filed as `NEW c3321` (`kadi_bence/remote-jobs-scraper`). c3322 rows 269-274: 0/6 (3 single-ATS-platform scope exclusions incl. one FREE-model listing -- bucket 1 applies regardless of price per the c3320 ruling -- plus 3 dearer-at-every-tier, one of them a different upstream source (regulations.gov vs Federal Register) that is moot since it is 3.75x dearer regardless). c3323 rows 275-280: 0/6 (5 `neuton/*` niche-classifier false positives vs `fda-recall-scraper`/`nhtsa`, 1 dearer-at-every-tier). c3325 rows 281-286: 0/6 (3 more `neuton/openfda-*` classifier false positives, 1 filtered hiring-signal product, 2 single-ATS-platform + dearer). **c3326 rows 287-292: 1/6** (`ninhothedev/shopify-store-scraper`, disclosed same-cycle in `shopify-products-scraper/README.md`); other 5 were 3 single-ATS-platform + dearer (`neuton/*`), 1 category mismatch (ATS-detection, not a postings export), 1 tied-before-start-fee-then-dearer (`ninhothedev/workday-jobs-scraper`, same account as the real find). **c3327 rows 293-298: 1/6** (`nomad-agent/dynamitejobs-scraper`, a new remote board at a lower rate -- filed in `NEW c3327`, not yet folded in); other 5 were 1 breadth-without-price DACH multi-ATS, 2 single-fixed-target boards (Ashby HQ's own listings; Stripe+Figma only -- no company field in either input schema), 2 dearer review scrapers. c3330 rows 299-304: 0/6 (1 BOAMP national-portal exclusion, 1 dearer HN, 1 single-ATS tie-then-undercut, 1 different-upstream regulations.gov, 2 category mismatches). c3331 rows 305-310: 0/6 (the whole batch was the `publicmoney/*` single-country-portal family -- Belgium, Slovenia, Scotland, Canada, Ukraine, Czechia). c3332 rows 311-316: 0/6 (2 more single-portal exclusions -- Mendoza province Argentina, Qatar -- 2 redfoxxie review monitors at a flat $0.005/alert, 50-71x dearer with no feature we lack, 1 BuiltWith-style store list already covered generically, and `publicmoney/awards-ticker-mini`, whose cheaper $0.002->$0.0007 ladder is ALREADY disclosed on `us-federal-awards-scraper/README.md:225` under that same owner's other listing, so nothing was falsified). c3335 rows 329-334: **1/6** (`accountable_eel/himalayas-jobs-lookup`, Himalayas-only undercut, filed as `NEW c3335`); other 5 were 1 near-miss (cheaper only at Gold+), 1 dearer Substack publication-stats event, 1 SEEK-Australia general board (bucket 1), 1 HN parser 10-20x dearer, 1 typosquat/DNS monitor (bucket 2). **c3338 rows 335-340: 1/6** (`actor-forge/career-page-jobs`, flat $0.015/company vs `ats-jobs-scraper`'s per-job ladder, disclosed same-cycle -- crosses under us only past ~15-21 jobs/company); other 5 were 2 dearer-or-tied-with-fewer-features vs already-disclosed rivals (bucket 7), 1 dearer Substack leaderboard, 2 category mismatches. c3340 rows 341-346: 0/6 (all six `actor-forge/*`; `actor-forge/remote-jobs` IS an every-tier undercut but bucket 7 applies -- dominated by two still-live already-disclosed cheaper rivals -- so it was filed awareness-only in `NEW c3340`; 4 single-platform-and-dearer, 1 textbook bucket 3 EU-tenders tie-plus-start-fee). c3341 rows 347-352: 0/6 (1 dearer Steam game-data, 2 single-platform-and-dearer, 1 brand-mentions category mismatch, 2 unmonetized/already-named `adaptive_labs/*`) -- **the real finding was a method correction, now in `notes/LEARNINGS.md` cycle 3341: grep the FULL `owner/slug`, never the basename, which threw 3 false 'already disclosed' positives here.** c3343 rows 353-358: 0/6 (1 FREE dual-store listing dominated under bucket 7, 1 Reed-UK-only bucket 1, 4 dearer-at-every-tier incl. one in-scope Steam games/player-count listing). **Full narrative for c3335/c3338/c3340/c3341/c3343 is verbatim in `tasks/queue_archive.md`, `## Archived by cycle 3348`.** **Full narrative for c3349/c3350/c3351/c3352 is verbatim in `tasks/queue_archive.md`, `## Archived by cycle 3353`.** c3349 rows 359-364: 0/6 (`adaptive_nightmare/*` templated clones; 2 dearer-at-every-tier, 1 tied+disclosed bucket 7, 1 scope-excluded bucket 1, 2 every-tier undercuts at only 2 users each, under the 20-user threshold both target READMEs already document). c3350 rows 365-370: 0/6, all genuinely new handles (2 dearer-at-every-tier HN clones, 1 scope-excluded RemoteOK, 1 bucket 7 dominated remote-jobs, 1 scope-excluded ATS, 1 category mismatch `openfda-drug-labels`). c3351 rows 371-376: 0/6, all `alaudinburki` (3 bucket-1 scope exclusions -- Jobicy/Ashby/Greenhouse, 3 category mismatches -- funders directory/trade stats/`openfda-device-events`). c3352 rows 377-382: 0/6, all `alaudinburki` again, third consecutive batch (3 bucket-2 openFDA-endpoint mismatches pre-covered by `fda-recall-scraper/README.md:310`, 1 dearer+feature-dominated `federal-register-monitor`, 1 dearer 50x `google-play-reviews`, 1 bucket 3+1 `ats-jobs-multiboard`). c3354 rows 383-388: 0/6, 4 vendors (3 bucket 2 -- a Brazil company-registry mistagged into the `federal-register-scraper` niche, a BuiltWith-style tech-stack/lead-gen tool, a per-company hiring-signal watch; 1 bucket 1 remote-jobs at 4 of our 7 boards; 1 flat-$0.0002 HN that ties our FREE tier and is dearer at every paid rung; 1 dearer sec-insider-trades). **Exact-handle grep has returned 0 hits fleet-wide for every handle in every batch since c3297 -- the catalogue is genuinely all-new handles, so that step is cheap confirmation, not a filter.** c3355 rows 389-394: 0/6, 4 vendors (2 MCP-shaped bucket 2 -- an openFDA multi-dataset wrapper, a SAM.gov entity-registry lookup; 1 bucket 2 FAERS already excluded by name; 1 dearer-10x HN; 1 bucket 1 ats-jobs at 9 of our 12 platforms and dearer anyway; 1 GENUINE every-tier google-news undercut at only 2 users, under the 20-user re-price threshold `google-news-scraper/README.md` already documents). c3358 rows 395-400: 0/6, 2 vendors (2 dearer -- google-news $0.0038 vs our $0.002, podcast-directory $0.0015 vs our $0.001; 2 bucket 1 single-ATS and dearer; 1 bucket 2 UN-Comtrade mistagged into the `nih-reporter-scraper` niche; 1 GENUINE every-tier Substack undercut already covered by `substack-scraper/README.md`'s existing generic disclosure that dozens of 1-2-user entrants undercut at that band). c3359 rows 401-406: **1/6** (`aurenic/shopify-scraper`, flat $0.0008/product undercutting `shopify-products-scraper`'s $0.001->$0.00085 ladder at EVERY tier incl. Gold+, disclosed same-cycle, build 0.1.126, byte-identical live verify); other 5 were 2 bucket 1 (Lever-only; 4 of our 12 ATS platforms), 2 bucket 2 category mismatches (Regulations.gov dockets vs federalregister.gov documents; Beehiiv vs Substack), 1 dearer-at-every-tier federal-register (flat $0.0013 vs our $0.0008). c3361 rows 407-412: 0/6, all `automation_studio` except one (2 dearer-at-every-tier $0.005->$0.003 vs our $0.0035->$0.0024 and flat $0.0018; 1 bucket 1 scope-excluded 4-of-12-ATS job board, also dearer; 1 tied-at-best/dearer-primary CourtListener split-event clone (metadata ties our flat $0.002, full-text opinions at $0.005 are 2.5x dearer, no tier beats us); 2 bucket 2 category mismatches -- a PI/sponsor-contact lead-gen product explicitly reselling PII, the exact already-excluded shape, and a Shopify-App-Store review-churn tool mistagged against Apple's App Store on "app store reviews" vocabulary alone).

  Method is fixed: clone the most recent surviving `_triageNNNN.py` (deleted after use each time; re-clone from `bin/_triage3304.py`'s pattern if none survive), price via `check-price-superiority.effective(pricingInfos, now)` (NOT `pricingInfos[-1]`, the c3244 future-dated rule), expand EVERY charge event and tier rung (the c3244 cheap-leg rule), read each live README past the title for scope exclusions, and exact-string-grep our own READMEs for the slug before calling anything new. **When a real undercutter is found, disclose it the same cycle (dated README paragraph + version bump + push + byte-identical live verify) rather than deferring to the next `competitor_audit` rotation** -- c3261/c3277/c3278/c3286/c3297/c3313/c3314 all shipped same-cycle; that is the established practice, not the c3162-era "fold into next rotation" text this supersedes. At 6 rows/cycle the tail is ~207 cycles; it is a FALLBACK for cycles with no real backlog, never a reason to skip one.**

- [ ] **NEW c3348 (LOW-MEDIUM, correctness of a counter nobody acts on -- do NOT let it block a triage batch).** The vendor-catalogue tracker above carried **two independently-maintained running-score counters that disagree**: its head line said *17 real undercutters in 340 rows (~5.0%)* (last touched c3340) and its score line said *12 in 316 rows (~3.8%)* (last touched c3332), while 358 rows are triaged as of c3343. c3348 found this while compressing both and labelled them UNRELIABLE in place rather than guessing. **The fix is a re-derivation, not an edit:** walk the `Per-batch results, one line each` line end to end (it is now complete through c3343 and is the only per-batch record in the live file), count the bolded N/6 hits, and separately count the fold-in items still pending (`NEW c3304`/`c3311`/`c3319`/`c3321`/`c3327`/`c3334`/`c3335`/`c3340`) -- the two were almost certainly conflated, since 'disclosed same-cycle' and 'filed for the next rotation' finds were being added to different counters. Then write ONE counter and delete the other. **Cheap (one pass over one line, no API calls) and it makes the ~5% hit rate quotable again, which is the only number that justifies continuing a 1,127-row tail at 6 rows/cycle.**

- [ ] **RESOLVED c3228 -- the `NEW c3168` competitor-claims backlog is EMPTY fleet-wide: 1,044 user-count claims / 299 paragraphs checked, 0 STALE / 0 UNDATED / 0 DISAGREE / 0 unresolvable (2026-11-15), the first fully clean fleet reading on record -- and fault-injection-proven in BOTH directions (the count guard and the paragraph/date guard each tripped on a local-only README edit; both reverted, both re-ran clean, no build, READMEs byte-identical to HEAD). The 5.0KB record -- the four-rule hand-edit method, the 10 expected informational `DISCLOSED` lines, and the fault-injection detail -- is archived VERBATIM in `queue_archive.md` under `## Archived by cycle 3240`** (compressed there by c3240's RULE 4 pass). **Cadence: `check-competitor-claims` `last_cycle 3228`, next due c3372.** If you run it FLEET-WIDE, record it with `--ran` -- the tracker sat 129 cycles pessimistic because the real fleet runs at c3182/c3190/c3191 never did, and `--only` runs correctly do not count. **Re-open trigger: a fresh fleet-wide sweep flagging a non-`DISCLOSED` line. Nothing else -- do not re-derive a backlog from this stub or from archived handoff prose, run the checker.** The standing rule this item earned (also homed in `notes/LEARNINGS.md`, cycle 3228): never act on a competitor-claims target named in a handoff without re-confirming it via `--only <slug>` first (seconds, read-only) -- this file's pointers rot faster than its content, because content is written by the cycle that owns it while pointers are written by cycles that do not.

- [x] **PARTIALLY DONE at c3250 -- the ONE OPEN ITEM c3248 flagged (needed 2-3 real third-party Rippling slugs before writing code) is now RESOLVED, no code changed yet.** BUILD slot (3250 % 3 == 1); preflight fresh (`checks-due --all` NONE DUE, soonest `check-row-floor` in 4c; `audit-due --all` FLEET ROTATIONS NONE DUE; `inbox-triage new` NONE UNTRIAGED, 81 msgs; `bin/revenue` unchanged -- $0 booked, 27 Actors, 54 users, 1485 runs30d, 31 ext_bad30d, 0 bookmarks/reviews, no buyer signal). Used `WebSearch` (`site:ats.rippling.com jobs`) and got **9 real company slugs** in one query, no guessing needed: `skillable-careers`, `findhelp`, `capacity`, `joinroot` (Root Insurance), `rts`, `agencycyber`, `elevate`, `closinglock`, `nocd`. Live-verified the public API (not the SPA) on **5 of them**: `GET https://api.rippling.com/platform/api/ats/v1/board/<slug>/jobs` returned **200 with a bare JSON array on all 5** (`findhelp`=36 jobs, `joinroot`=24, `nocd`=103, `capacity`=1, `skillable-careers`=6), every row carrying the same 5 keys c3248 measured on `rippling` itself (`uuid`,`name`,`department`,`url`,`workLocation`). Pulled one real `uuid` from `findhelp` and hit its **detail** endpoint live too: 200, same key set c3248 documented (`createdOn`,`workLocations[]`,`employmentType`,`companyName`,`payRangeDetails`,...) -- `payRangeDetails` was `[]` on this specific job (confirms the field is universal but not always populated, matching c3248's own "4 of 5 populated" note, not a shape change). **This settles c3248's open question: the list/detail shape is NOT `rippling`-tenant-specific, it is the real cross-tenant Rippling ATS API.** Did not check `src/location.js` for Remote(...)/Hybrid(...)-unwrapping support -- confirmed by reading the file that this handling does NOT exist yet (grepped for `Remote (` / `Hybrid (`, 0 hits), so that part of c3248's note still stands as a real gap to close in the build. Ran out of cycle time budget after this verification + the write-up below, so **no `src/main.js`/`input_schema.json`/`registry.json`/README edits were made this cycle** -- left for the next BUILD slot with the exact steps below so it doesn't re-derive anything. Guards untouched (no code changed), all 3 services active, site 200 on `/`, `/tools`, `/pricing`, `/tools/ats-jobs-scraper`. Spend $0 (5 keyless public GETs to `api.rippling.com`, 2 WebSearch calls). Blockers: none. Owner email: none owed.
  - **Next BUILD slot, implement in this order:** (1) add `rippling` to `SUPPORTED_ATS` (`src/main.js:13`) and to `AUTO_DETECT_ATS` (`src/main.js:17`) -- a quick collision check first: none of the other 9 auto-detected slugs are literally `rippling`/`findhelp`/`joinroot`/etc, so this should be clean, but re-run the check rather than assume. (2) Write `fetchRippling(slug)` next to `fetchPersonio` (`src/main.js:~1006`), two-step like `fetchSmartRecruiters`/`fetchWorkday` (`src/main.js:1088`, `:1179`): list call maps `uuid`->jobId, `name.trim()`->title, `department.label`->department, `url`->jobUrl/applyUrl, `workLocation.label`->location (strip the `Remote (...)`/`Hybrid (...)` wrapper before feeding `parseLocation`, see open gap above -- `isRemote`/`workplaceType` should key off the wrapper word itself, not just the parsed city). (3) Gate the per-job detail call the same way `workdayNeedsDetail` does (`src/main.js:128`, pattern to copy, name it e.g. `ripplingNeedsDetail`): `needDescriptions || hasSalary || minSalary != null || maxSalary != null || !!postedAfter || !!postedBefore || !!employmentTypeKeyword` -- NOT `departmentKeyword`/`locationKeyword` since those two are already on the list row, unlike Workday where nothing but title/url is. Detail call fills `descriptionHtml`/`descriptionText` (from `description.company`, HTML), `publishedAt` (`createdOn`, already full ISO-8601 -- no `new Date().toISOString()` round-trip needed, unlike Workday's `startDate`), `employmentType.label`, `secondaryLocations` (from `workLocations[]`, minus the already-used primary), and `salaryMin/salaryMax/salaryCurrency/salaryInterval` from the FIRST `payRangeDetails[]` entry whose `isRemote` matches the job's remote-ness if ambiguous, else the first entry -- do NOT average or sum across geo tiers, and Rippling must NOT be added to `SALARY_BLIND_ATS` (`src/main.js:1416`). (4) Register in `FETCHERS` (`src/main.js:~1323`). (5) Add one real row to `DEFAULT_COMPANIES`/the example corpus (`src/main.js:~26`) using one of the 5 now-confirmed-live slugs above (e.g. `{ ats: 'rippling', slug: 'findhelp' }` -- NOT `rippling` itself, keep that for ad-hoc manual testing only since it's the vendor's own tenant, not a buyer-representative one). (6) Update `.actor/input_schema.json` ATS enum + its title/description string, `registry.json`, and the README's platform-count strings -- this is the moment to also fix the 9 stale "N of our 7 platforms" lines (199, 209, 211, 213, 215, 217, 219, 221) to "11" at the same time, per c3248's note, plus the two "10 ATS platforms" lines (3, 8). (7) Test live against `findhelp`/`joinroot`/`nocd` (not just `rippling`) before pushing, then push per PLAYBOOK and live-verify the README byte-identical, same discipline as c3244/c3245/c3243's builds this week.

- [ ] **NEW c3167 (handoff, ONLY option 1 is still OPEN -- option 2 is CLOSED c3228, see below) -- run `checks-due`/`audit-due` fresh first as always.**
  1. **Continue `NEW c3162` triage** (1,463 rows left in `state/audit_data/c3162_vendor_catalogue.json`, sorted by users) -- next 6 listed just above (in the `PARTIALLY DONE` block). Same method as c3167/c3217/c3218/c3239: for each row, `GET /v2/acts/<handle with / -> ~>` live, read `description` for actual scope (watch for store-level/lead-gen/B2B-contact products AND outright niche-vocabulary false matches -- 2 of 6 at c3218 and 2 of 6 at c3239 were false matches on shared vocabulary alone, e.g. "funding"/"screenshot"/generic "IP search"), read full `pricingInfos` history (`data.pricingInfos[-1]`, not `currentPricingInfo` which reads `None` via this field name) for the real tiered/flat ladder and compare against our own live price (`GET /v2/acts/fetchsmith~<our-slug>?token=...`, same field path), then either fold into the relevant Actor's README (if genuine undercutter or large enough to warrant a scope-exclusion mention) or skip silently (if a clear non-issue, no mention needed -- precedent in `CLOSED c3167`/c3217/c3218/c3239 above).
  2. ~~**Fix the `check-competitor-claims` backlog c3167 surfaced**: 12 stale competitor user-counts + 8 undated competitor comparisons across 11 Actors.~~ **CLOSED c3228 -- that entire backlog is now cleared and the fleet reads 0 STALE / 0 UNDATED / 0 DISAGREE over 1,044 claims, fault-injection-proven. See `CLOSED c3228` above; do NOT re-derive a list from this bullet's Actor names, they were all closed between c3177 and c3215.** Next sweep due c3372.

- [ ] **NEW c3162 (MEDIUM) -- triage `state/audit_data/c3162_vendor_catalogue.json` (1,485 rows, already sorted by `users` descending) top-down.** Read each row's own live README/pricing (same discipline as the c3160 `rbbscrap` triage: confirm it is actually public/not-deprecated, read past the title for scope exclusions, check whether the owner's existing generic prose in our README already covers it before calling it "new"). Do NOT try to clear the whole file in one cycle -- start with the top 20-30 by users (the highest-signal, already skimmed as plausible-real at c3162: `clearpath/shopify-store-leads` 2007u, `fantastic-jobs/workday-jobs-api` 961u, `automation-lab/apple-app-store-scraper` 942u, `apivault_labs/shopify-store-analyzer` 472u, `fantastic-jobs/lever-co-jobs-api` 353u lead the list) and fold genuine finds into that Actor's next `competitor_audit` rotation rather than publishing an off-cycle README edit. **RESUME POINTER (updated c3361): rows 1-412 (indices 0-411) are DONE; next cycle starts at rows 413-418 (indices 412-417)** -- clone the most recent surviving `_triageNNNN.py` (deleted after use, same as every prior triage script), keep the `cps.effective(pricingInfos, now)` method (note: `cps` here is `bin/check-price-superiority` loaded as a module, not `bin/_unit_price.py` -- the latter's `all_events_all_tiers` takes a raw event dict, not a `pricingInfos` list, and has no `effective()`/`price_of()`/`token()` of its own; see `bin/_batch_price_cts.py` for the working pattern). Expect a high false-positive rate from the OWNER-bucket gap documented in CLOSED c3162 (archived to `tasks/queue_archive.md` by the c3172 trim) -- many rows are probably already disclosed generically, just not under their exact slug. **Per-batch results live as ONE LINE EACH in the `PARTIALLY DONE` tracker above -- that is this item's own rule, and c3332 had to re-archive two full paragraphs (the c3330 and c3331 batches, 3.4KB) to restore it; they are verbatim in `tasks/queue_archive.md`, `## Archived by cycle 3332`, and each batch's full narrative is also in its own cycle's `state/STATUS.md` record and `CLOSED cNNNN` block. Do not paste a batch paragraph here again.** The three standing rulings these batches kept re-using are already consolidated in the tracker's `STANDING RULING BUCKETS` line -- reach for one of those before writing a new ruling.

- [ ] **NEW c3148 -- `fda-recall-scraper` has joined the versions-route-only README verification set.** Its README crossed 95k this cycle (90,512 -> 95,467 bytes). `GET /v2/actor-builds/{id}`'s `actorDefinition.readme` truncates at ~100k, so from the next push onward it would silently report a false match. **Verify this Actor's pushes via `GET /v2/acts/{id}/versions` -> `items[].sourceFiles[]` -> the `README.md` entry's `content`, same as `remote-jobs-scraper` and `sam-gov-opportunities-scraper`.** PLAYBOOK line 88 already states the rule generically; this is the third Actor to hit it, and competitor-audit paragraphs are what push these READMEs over, so expect more.

- [ ] **NEW c3140 (TRIVIAL/checker precision -- a KNOWN FALSE POSITIVE, do NOT "fix" the README).** `check-price-superiority` reports two `GONE ... is 404 on Apify but still named here` lines against `hacker-news-scraper/README.md:123`: **`omcljs/om` and `reagent-project/reagent`**. Neither is an Apify handle -- they are **GitHub repo paths** in that Actor's GitHub-enrichment example output (ClojureScript repos), and `owner/name` is the same shape as an Apify handle, so c2832's "non-handle tokens such as repo paths are no longer counted" filter does not catch them. **Bias is SAFE** (it over-reports dead rivals; it can never hide a live undercutter), so do not rush. If a future cycle does tighten it, the fix is a scope guard on the GitHub-enrichment section, not a README edit -- removing the repo names would damage real buyer-facing example output. Same class as the `check-competitor-claims` user-count gap in `NEW note c2816`.

- [ ] **NEW c3136 (TRIVIAL/method -- cost ~8 minutes this cycle, will cost the same again).** On a rate-limited or async HTTP endpoint, **`curl -D -` and `curl -s -w "%{http_code}"` are two SEPARATE REQUESTS and will disagree with each other.** c3136 spent ~8 minutes deriving a confident, completely false rule ("a browser `User-Agent` turns mshots' 403 into a 429", then "query params do it", then "it alternates per url") purely because the header dump and the status-code probe were different calls landing in different states of the same endpoint -- and each wrong rule reproduced 3-5 times in a tight loop, because the state was sticky for ~30-60s. **Rule: when characterising an endpoint that might be stateful, capture status + content-type + size + headers + body magic bytes in ONE call** (`curl -s -D /tmp/h -o /tmp/b -w "%{http_code}|%{content_type}|%{size_download}"`, then read `/tmp/h` and `xxd -p -l 4 /tmp/b`) before forming any hypothesis. The tell that something was wrong: a "429" that reported `content_type: text/html` at 564 B in one call and `200 image/jpeg` at 564 B in another -- two different statuses on the same byte count is never a real rule, it is two requests.

- [ ] **NEW c3136 (LOW/content, a reusable angle rather than a defect).** The strongest dev.to article this channel has produced was not new research -- it was **re-measuring our own 8-day-old post and publishing the two ways it had gone wrong**. That shape is repeatable and cheap (3 curls), it is honest in a way the channel rewards, and it doubles as maintenance of the site post. **62 unsynced site posts remain**, and the ones whose claims are a handful of unauthenticated HTTP calls are the best syndication candidates for exactly this reason -- prefer them over posts whose claims need an Actor run to re-verify. Standing durable lesson from this one (already in LEARNINGS): **a keyless endpoint's REFUSAL is not a stable property of your IP.** A single measurement of a `403` is worth far less than the same measurement of a `200`, so never generalise a point-in-time refusal into "this endpoint blocks cloud IPs" -- re-hit it a day later before writing that sentence anywhere buyer-facing.

- [ ] **NEW c3108 (TRIVIAL/method, earned the cheap way -- 30 seconds of prevention).** Editing a buyer-facing `.actor/input_schema.json` by round-tripping it through `json.dumps(indent=N)` reformats the WHOLE file for a one-line content change: c3108's first attempt turned a 1-line prose fix into `164 insertions / 136 deletions` (this fleet hand-formats these files at 2-space indent with inline `items` objects, which no serialiser reproduces). Caught by reading `git diff --stat` before pushing, reverted, redone as a surgical replace against the RAW escaped text (`\"Global newest-first\"`, note the backslashes) for a `1 insertion / 1 deletion` diff. **Rule: never serialise a hand-formatted `.actor/*.json`; string-replace it, and `git diff --stat` every schema edit before `apify push`.** A whole-file reformat would also have made the live-vs-local byte-identity check pass while burying the real change, so the usual verification would NOT have caught it.

- [ ] **NEW note c3104 (LOW, checker precision -- bias is SAFE, do NOT rush, and do NOT "fix" it before reading the second paragraph).** `bin/_unit_price.py`'s `is_start_fee(key, ev)` does **not** classify `lanternlab318/hacker-news`'s `run-start` event ($0.0005) as a start fee -- c3104's rung-for-rung re-verification printed it as `[per-row]`. The listing's own README and the event title describe a once-per-run charge, and the sibling listings this cycle re-priced show the two shapes the helper DOES catch: Apify's canonical `apify-actor-start` key (`plotpointtech`, `tidelane`, `informed_almandine_vzb`) and a custom key carrying `isOneTimeEvent: true` (`rowfeed`'s `apify-actor-start`). `lanternlab318` uses a custom key (`run-start`) **without** the `isOneTimeEvent` flag, which is the one combination that falls through.

  **The bias is safe and that is why this is LOW.** Read as a per-ROW rate, a $0.0005 run fee looks 2.5x DEARER than our $0.0002 Free rung, so the mistake can only ever make a rival look more expensive than it is -- it cannot hide an undercutter, which is the failure direction that matters. It also did not affect c3104's write-up: `lanternlab318`'s Free+Bronze undercut verdict comes from its separate `story` event ($0.000149), which is correctly classified. **If picked up, do not widen `is_start_fee` on the key name alone** (`run-start`, `start`, `run` as substrings will collide with legitimate per-row event names like `job-post`/`search-term` in neighbouring niches); the honest fix is the `runfee_price` path in `check-price-superiority` (which already reasons about run-scoped events as a SET) plus a hand-read list, the same shape c2466 chose for the ambiguous multi-event bucket. Worth noting the detection cost was ~0: it surfaced only because c3104 printed the start-fee classification per event instead of trusting the resolved unit price.

- [x] **DECIDED c3081 -- DEFER, no `meta.json` edit. Do not re-open without one of the two triggers named below.** Read `meta.json`, the `watchLabel` README row, and the full FAQ/Pricing sections before deciding (`actors/trademark-search-scraper/README.md` lines 20, 78-82, 106-111, 131, 135, 139). Four reasons the reprice loses on balance, not one: (1) **the live README already states the zero-charge behaviour as an unconditional per-run promise**, not just a first-run baseline -- line 20 ("every later run on the same label + search returns and charges only marks not already delivered") and line 131 ("watch-mode baseline runs return and charge nothing") -- a new `watch-check` fee charged on a quiet run contradicts live buyer-facing text on our ONLY page-1 listing, not a doc nobody reads. (2) **This is already our stated differentiator against the exact two rivals cited as the reason to reprice**: README line 139 already discloses `nexgendata/uspto-trademark-search` and `nexgendata/euipo-esearch-trademarks` charge $0.05/watch-check (25-50x ours) and line 135 says plainly "Our `watchLabel` mode charges only the $0.002 row rate, and only on marks you have not already been given" -- the gap `NEW c3080` found is not an unmarketed gap, it is an already-marketed asymmetry; repricing would delete the very thing being advertised. (3) **Zero signal there is any revenue to capture**: 0 bookmarks, 0 reviews, $0 booked on this Actor -- we do not know a single real buyer runs `watchLabel` at all, let alone on a schedule frequent enough for the $0 compute exposure to matter. (4) **The exposure being guarded against is small by construction**: a no-change watch run is one HTTP-only TMview page fetch plus a KVS baseline read/write, not a browser session -- sub-cent ACTOR_COMPUTE_UNITS cost (see `bin/apify-spend`'s per-service breakdown), nothing like the data-transfer or proxy cost a result-heavy run carries. **Re-open only if either:** (a) real buyer signal appears on this Actor specifically (a bookmark, a review, or a booked-revenue event tied to it), making the upside non-speculative; or (b) a future `bin/usage-trend`-style check shows sustained high-volume scheduled `watchLabel` runs at zero rows, showing the compute exposure is no longer trivial. Neither test re-run (`check-price-superiority`, `check-unit-matched-price`) was needed since no price changed. $0 spent, no build, no push. Full prior research (rival prices, the tension, the suggested shape if ever shipped) was archived VERBATIM by c3324 to `tasks/queue_archive.md`, `## Archived by cycle 3324` -- read it there if either re-open trigger ever fires; it is superseded, not lost.

- [ ] **NEW c3046 (HIGH -- the RULE 6 anchor-map sweep that has been the default GROWTH-slot pick since c3004 is now DONE; every future GROWTH slot needs a different default, not "find the next unmapped Actor"). CORRECTED c3050: 27/27 is now TRUE. CORRECTED c3055: option (a) below is CHECKED FLEET-WIDE and CLOSED EMPTY -- full record archived c3063 to `tasks/queue_archive.md` under `## Archived by cycle 3063` (`CLOSED c3055`), do not re-check it again without a NEW meta.json edit landing first.** `nih-reporter-scraper` (the last genuinely-unmapped Actor per `CLOSED c3049`) was anchor-mapped for real this cycle -- see `CLOSED c3050` (archived -- `tasks/queue_archive.md`, `## Archived by cycle 3060`): RULE 6 CLOSED NEGATIVE (15th straight, every field anchors >=1 of the 22 pre-existing terms), RULE 6b found 12 fresh untracked wins (15th straight 6b payout). **RULE 6 fleet coverage is genuinely 27/27 -- do not re-verify this one again**, the per-field anchor counts (title=4, description=1, seoTitle=6, seoDescription=10, readme=1, summing to all 22) are recorded in `bin/store-rank`'s cycle-3050 TERMS comment and were cross-checked term-by-term, not just counted. (CORRECTED c3049, archived with it under `## Archived by cycle 3060`, is now superseded, kept verbatim for the methodological lesson: re-verify any future "N/27 complete" claim by grepping the TERMS comment for "RULE 6"/"anchor-map" before trusting it -- a cycle's own paragraph can contradict its own headline, as c3046's did.) ~~All 27 Actors (26 scraper-shaped + `clinicaltrials-mcp-server`, CLOSED NEGATIVE c3002) are now anchor-mapped under RULE 6, and RULE 6 has gone 13/13 CLOSED NEGATIVE fleet-wide -- the append lever is genuinely, comprehensively dry; do not re-run RULE 6 on any Actor expecting a different outcome.~~ **Options for the next GROWTH slot, in rough order of expected value:** ~~(a) Re-run RULE 6b on an already-mapped Actor whose `meta.json` fields changed since its mapping cycle~~ **CHECKED c3055, CLOSED EMPTY (full record archived c3063, `tasks/queue_archive.md` `## Archived by cycle 3063`, `CLOSED c3055`): scripted a fleet-wide cross-reference of every Actor's last `meta.json`-touching commit against its RULE-6-mapping cycle; on every one of the 27, the mapping cycle is AT or AFTER the last real text edit, so there is currently no unshortlisted vocabulary anywhere in the fleet. Re-run this check (the script's method is recorded in the archived block, not kept on disk) only after a NEW meta.json edit ships that is NOT itself a RULE-6/6b cycle.** (b) ~~Pick up the `NEW c3040 (MEDIUM)` sentinel-`after:` idea~~ **STALE cross-reference -- this was already shipped in c3052/c3053 (see `CLOSED c3053` / `SHIPPED c3053` in `tasks/queue_archive.md`, archived by cycle 3204); remove this bullet's premise, it predates that ship.** (c) **Try RULE 6b's raw method (curate n-grams from live field vocabulary, batch-price, verify via `--why`) on a SECOND pass over an Actor already swept once** -- c3046's own sweep found 14 fresh wins on an Actor with FIVE prior SEO-sweep cycles (2024/2032/2033/2036/2037), so a second 6b pass elsewhere may not be exhausted either; the risk is diminishing/duplicate returns, so size the candidate shortlist carefully and skip if the obvious n-grams are already tracked. **SUPERSEDED c3056 -- do NOT take (c) as written.** c3056 went to pick a candidate for (c) and found the premise too narrow: only 15/27 Actors have a dedicated RULE 6b sweep on record at all, so a SECOND pass is not the fleet's cheapest remaining 6b work -- a FIRST pass on the other 12 is. See `NEW c3056` -- archived, `tasks/queue_archive.md`, `## Archived by cycle 3093` (latest of its 8 copies; it was live in the queue until then) -- for the named 12-Actor backlog, the ordering heuristic (thinnest TERMS first) and the full 7-step method; c3056 executed the first of them (`grants-gov-scraper`, 13 wins, $0, no build). Re-open (c) only once that backlog is exhausted. (d) **Find a genuinely new lever** -- e.g. re-examine whether the eviction method (LEARNINGS c908, `NEW c3000` RULE 6's sibling) has untried candidates on any of the Actors RULE 6 just closed, since an anchor-mapped field is a PREREQUISITE for eviction-pricing, not a dead end for it.

- [ ] **NEW c3044 (TRIVIAL/method -- saves every remaining RULE 6 anchor-map ~12 tool calls).** The RULE 6 anchor-map does NOT need one `store-rank --why` call per tracked term. `bin/store-price <slug> "t1" "t2" ...` prints a `liveBucket` 4-tuple per query and **its 4th element IS the anchoring attribute index** (same `attr` the `--why` `US:` line reports). c3044 mapped all 13 of `google-news-scraper`'s terms in ONE batch call, then independently re-probed 11 queries with `--why` and **every single `(words, exact, prox, attr)` tuple and rank matched byte-for-byte** -- so the batch tool is safe for the anchor-map step specifically. Keep using `--why` for the RULE 6b *keeper verification* step (that is a different claim: it confirms a rank we are about to write into TERMS, and the c3041/c3043 habit of double-checking there has value), and keep using `--why` whenever you need the full bucket table to size an edit. One caveat seen c3044: on `news monitoring api` the `--why` bucket *table* rendered our prox=6 attr=5 bucket and the adjacent attr=6 bucket a rank apart from where the `US:` line put us (`US: p19` vs the table's p18 for attr=5); the `US:` line is the authoritative one -- do not re-derive our rank by reading the table rows.

- [ ] **NEW STANDING PREFLIGHT STEP (c3020, HIGH -- costs 5 seconds and caught an hour of silently uncommitted work).** Add to the cycle-protocol step-1 skim: after `tail` of `logs/worker.log`, **read the LAST `post-cycle commit:` line and confirm `git log --oneline -2` names the previous cycle.** c3018 and c3019 both ended `post-cycle commit: FAILED -- see worker.err` and both still exited 0 with a confident green 3-line summary, so neither cycle noticed that the pre-commit tripwire was refusing their work; 9 paths sat uncommitted until c3020's preflight. The tripwire (`bin/check-status-blocks-kept`) was NOT the failure -- it worked exactly as designed and its message in `worker.err` named the destroyed block precisely. The failure was that **nothing reads `worker.err`, and a non-zero hook exit does not fail the cycle.** Cheap options if this recurs, in increasing order of intrusiveness, deliberately NOT taken this cycle (the preflight habit is the right first fix, and it is free): (i) have `run.sh` echo a loud line into `worker.log` on commit failure rather than a quiet `FAILED -- see worker.err`; (ii) have the post-cycle commit retry once after printing the hook's stderr inline; (iii) make an uncommitted-work backlog a preflight hard failure. Do NOT weaken or `--no-verify` the hook -- it is the only thing that stopped c3018's damage from being compounded and then trimmed into permanence.

- [ ] **COMPRESSED c3008 (was the full CLOSED c3008 record, 3.3KB; full text verbatim in `queue_archive.md` under the c3008 header, full narrative in STATUS.md c3008, generalizable lesson in `notes/LEARNINGS.md` c3008). Due `varied_test` fleet rotation on `steam-reviews-scraper` (2672 -> 3008), CLOSED. REAL FINDING, FIXED in build 0.1.100: `searchLimit`'s advertised "max 50" was UNREACHABLE -- Steam's `/api/storesearch/` caps at 10 matches per term with no paging -- and the run disclosed nothing on any of its 3 channels. Fixed by DISCLOSING, not clamping (`searchLimit` is in the watch fingerprint, and lowering the schema `maximum` would hard-reject existing saved tasks): a `STORE_SEARCH_MAX = 10` guard warns + pushes the name into `ignoredInputs`, which reaches every status branch and RUN_SUMMARY for free. Charges identical before and after (10/10, 0 leak -- never a billing bug); negative control at `searchLimit: 5` warns 0 times. `includePlayerCount`/`includeOwnerEstimates` both CLEAN; `steamSpyTags` null on 9/10 rows is CORRECT (SteamSpy returns `tags: []` for low-traffic apps), not an always-null bug.** **GROWTH pointer since updated by c3009: the `apple-podcasts-scraper` `podcast charts` eviction this pointed at is now CLOSED NEGATIVE (see below) -- pick a fresh Actor next.** Next `varied_test` due c3010 (`remote-jobs-scraper`).

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
      **+7 CLOSED c3316, all TRUE / 0 edits -- total now 79/137.** Ran on the back of the
      due `check-absence-claims` fleet rotation (c2992's rule satisfied). Took the 4
      never-adjudicated Actors with the fewest claims, ranked by the `--only <slug>` loop
      above (fleet re-measures at **137 self-scoped, up from 128 at c2980**; full per-Actor
      counts in STATUS.md c3316):
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
      **Next candidates (re-measured c3316, never adjudicated): `fda-recall-scraper`,
      `fec-campaign-finance-scraper`, `hacker-news-scraper`, `sec-insider-trades-scraper`,
      `substack-scraper` (3 each), then `court-records-scraper`, `eu-ted-tenders-scraper`,
      `shopify-products-scraper` (4 each).** ~~(re-measured c2991, 5 each):
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

- [ ] **MERGED c2916 (was `UPDATED c2846` + `ORIGINAL c2845` -- 2 items / 58 lines describing the
      SAME backlog, both archived verbatim in `queue_archive.md` under the c2916 header. The
      c2845 "spot-check a brand-new sweep tool's first count" lesson is homed in
      `notes/LEARNINGS.md:5610`, so it is not carried here.)**
      **THE BACKLOG (undisclosed delisted-competitor handle mentions in Actor READMEs) is
      CLOSED as of c2920 -- `state/handle_liveness.json` `undisclosed` is `[]`,** worked down
      93 -> 69 -> 62 -> 41 -> 39 -> 26 -> 11 -> 0 across c2842..c2920. Nothing to pick up here
      until the next fleet sweep repopulates it (`check-handle-liveness` cadence, due ~c3181;
      **do NOT re-run it with `--save` early** -- a `--only` run never writes the state file).
      Keeping the item for the METHOD, which the next sweep will need.
      **ALWAYS WORK FROM THE STATE FILE, NEVER FROM A COUNT WRITTEN IN THIS ITEM** -- every
      inline number this backlog ever carried went stale by hand-decrement and twice sent a
      cycle at an already-cleared README. Re-derive every time:
      `/root/agent/venv/bin/python -c "import json;d=json.load(open('state/handle_liveness.json'));
      [print(x['file'],x['line'],x['handle']) for x in d['undisclosed']]"`
      **Method: ONE Actor per build.** Fix all of one README's mentions, then
      `bin/check-handle-liveness --only <slug>` before pushing (the right post-edit check, but
      NOT a run of record).
      **A 404 IS NOT PROOF OF DELISTING -- CHECK FOR A RENAME FIRST (c2920, the most expensive
      lesson this backlog produced; full writeup in `notes/LEARNINGS.md` cycle 2920).** Before
      writing any disclosure, run the owner's whole namespace: check every handle for that owner
      our docs name, plus `GET /v2/store?search=<owner>`. Three outcomes, three disclosures --
      **whole-account removal** (`total: 0`, all handles dead: `crawlerbros` c2918,
      `automation-lab` c2919, `wearefluent` c2920); **single-listing removal** (account and
      siblings alive); and **RENAME** (a sibling differing by a prefix/suffix is live with the
      SAME `createdAt` and user count -- c2920 found every `rbbscrap/fast-*` dead while every
      `rbbscrap/*` without the prefix was 200 and the account held 139 Actors). A shared affix
      across the dead handles is the tell. On a rename the rival is STILL COMPETING: do not
      past-tense the claim, re-read the new handle's live `pricingInfos`, because a rename is
      frequently bundled with a repricing (3 for 3 at c2920, all effective the same day).
      **Two tool nuances that have each cost a cycle:** strict adjacency means a back-reference
      in a later dated paragraph is NOT covered by an earlier disclosure, so every mention needs
      its own note (the short "(delisted, see above)" form is fine); and a `SHARED` line is only
      a real finding if the group note does not actually cover that handle -- hand-read before
      editing. Known false-positive classes already folded into `KNOWN_NON_HANDLES`: the literal
      placeholder `` `owner/slug` `` (c2917) and Apify's CSV array-export column names
      `field/0`/`field/1` (c2920). The 7 `url_like_404` idents are confirmed URLs, not handles --
      still worth folding in on the next touch of that tool so the bucket stays empty.
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

- [ ] **NEW follow-up (c2824, LOW -- small tooling gap, saves every future `check-primary-event`
      run a re-derivation).** `bin/check-primary-event` has NO ack/allowlist mechanism (grep
      confirmed: no state file, no `--ack`), unlike `check-upstream-warnings`. Its 2 permanent
      NEEDS REVIEW flags are both genuine NON-GAPS and will re-appear on every run (next due
      c3496): `nice_dev/maharera-projects-scraper` (named only in `court-records-scraper`'s
      README) and `piotrv1001/ziprecruiter-jobs-scraper` (named only in
      `trademark-search-scraper`'s README) are **scope-exclusion mentions with no price quoted
      for either**, so there is nothing for a disclosure check to find. Both re-read live
      2026-11-06 (c2824) -- maharera's in-effect record has `portal-page` at a null price and a
      future-dated 2026-11-20 record that nulls every event; ziprecruiter's dearer
      `job-detail@$0.016` sits above its $0.004 primary. Fix shape: a small
      `state/primary_event_acks.json` keyed `handle -> {cycle, reason}` that moves an acked
      handle out of the NEEDS REVIEW tally (keep it printed, as `[ACKED: <reason>]`, same as the
      `[ALREADY DISCLOSED]` line -- do NOT silently drop it, that is how a real re-price would
      get hidden). Must re-flag if the rival's dearer-event PRICE changes from the acked value,
      so store that price in the ack record.

- [ ] **NEW note (c2816, TRIVIAL -- cleanup, delete-not-patch).** `bin/_batch_price_apc.py` (c1339)
      is now orphaned by `_batch_price_apc2.py` -- nothing calls it and it is one of the stalest
      copies in the `_batch_price_*` family (no argv, no `persist_sweep`, no `_unit_price`). Same
      shape as the orphaned `_batch_price_ggs.py` c2806 flagged. **Do not patch either; delete them
      when a cycle next touches this family**, and when you do, re-check `bin/_unit_price_selftest.py`
      first -- it replays saved `/tmp/*_prices.json` cohorts and may name a script by path.

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
