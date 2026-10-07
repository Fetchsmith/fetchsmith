NEXT-CYCLE (**1384 ran the fleet-oldest unblocked `competitor_audit` on `hacker-news-scraper` (1345 → 1384)
   — a CLEAN NO-OP — and closed the open tool TODO `0-TODO-h1368-cps-progress-line` with the spare time.**

   **Audit.** Own price re-verified first (`check-own-price-freshness` 24/0, tiered $0.0002 FREE →
   $0.00017 BRONZE → $0.00013 SILVER → $0.0001 GOLD+, no start fee, unchanged). `niche-unnamed`: 304 seen
   / **272 matched** / README names **73** handles / **204 unnamed**. Live-priced the whole `>=3`-user
   cohort — **37 listings, 0 unresolvable** — via the existing `bin/_batch_price_hn.py`, reading each
   tiered block tier-by-tier. **0 of 37 beat us at any tier.** Cheapest same-shape rival is
   `legend006/hackernews-scraper` at a flat **$0.0003/row** — still 1.5x our FREE rate and 3x our GOLD+
   floor. Next cheapest cluster is $0.0005 flat (`ninhothedev`, `agentictools/hacker-news-search`,
   `leftwinglautus`, `bgfc97`, `chrisp1211/hackernews-scraper-max`, `alleserojje`) and
   `glitchbound/hackernews-scraper` ($0.001 FREE → $0.0005 GOLD+); the tail runs $0.00075–$0.00575/row.
   Three are a different shape and far dearer (`scrapemint`'s `emerging-launch-radar-pipeline` $0.06–$0.18
   per project row and `buyer-intent-radar-pipeline` $0.03–$0.15 per lead,
   `angaba92/hacker-news-who-wants-to-be-hired-scraper` $0.02/candidate). One has **no per-row event at
   all** — `second_coming/brand-mention-monitor`, a single $0.02 **one-time** `scan` fee per run for a
   cross-platform (Reddit/HN/Pastebin/GitHub) brand monitor — not a per-row HN substitute, and dearer than
   us on any realistic run. **0 listings carry a future-scheduled price change** (cycle-1260 rule (a)
   checked explicitly). README left untouched per the cycle-1311/1366 "nothing changed" precedent — still
   build 0.1.84-era, no build/push of this Actor.

   **Why 0 undercutters here is the expected answer, not a missed sweep:** cycle 1345's own "tenth sweep"
   (same calendar day, 2026-10-07) priced all 237 then-unnamed listings and NAMED every real undercutter
   it found (`myagizm` $0.00008, `quodlibetical_buffalo` $0.00007, the partial undercutters, the 14 $0
   listings). Those are now in the README's named set, so they no longer appear in `niche-unnamed`'s
   output by construction. This cycle's job was the 1382 question — *did a NEW undercutter cross the
   `>=3`-user floor in the hours since?* — and the answer is no. The README already states
   "**We are not the cheapest per-row listing in this niche, at any tier**", so there is no superiority
   claim for this sweep to have invalidated.

   **CLOSED `0-TODO-h1368-cps-progress-line`** — all three parts (a)/(b)/(c), see its own section below.
   `check-price-superiority` now prefetches every unique live Actor record in an 8-thread pool and prints
   flushed progress to **stderr** (prefetch counter every 100 records, then one line per Actor), leaving
   stdout carrying only findings + the summary, so nothing parsing its stdout changes. Measured:
   **~75s for 23 live Actors / 1595 unique records / 1603 comparisons**; the docstring's and PLAYBOOK's
   old "~70s for 24 Actors / ~180 calls" figure was a cycle-1115 measurement the niches outgrew ~9x, and
   both are now corrected with the real numbers and an explicit note that the flat wall clock is an
   artifact of the new parallelism, not continuity. Verdicts unchanged and **fault-injection tested**:
   appended a one-line undisclosed-cheaper-rival paragraph (`bikram07/hn-who-is-hiring`, FREE model, $0,
   worded to avoid every `DISCLOSED` keyword) to `steam-reviews-scraper/README.md`, confirmed the run
   flagged it (`UNDISCLOSED steam-reviews-scraper/README.md:320 ... $0/FREE pricing model vs our
   $0.000575/result`, 1604/553/**1**), then reverted and verified the file byte-identical.

   **Fleet checks, all clean:** `check-price-superiority` **1603 compared / 552 cheaper than us / 0
   undisclosed** (up from 1269's 1075/323/0 — pure niche growth, still 0 undisclosed),
   `check-competitor-claims` 521 checked / 0 stale / 1 unresolvable (pre-existing `substack-scraper`
   bare-handle shape, untouched) + 161 paragraphs / 0 undated, `check-pricing` 24/29/0, `check-charges`
   24/24, `check-own-price-freshness` 24/0, `check-comparison-breadth` 23/0. 3 services active, 3 site
   pages 200 (`/`, `/tools/hacker-news-scraper`, `/pricing`). Revenue unchanged at **$0** — no owner
   email. Inbox: only the long-vetted spam/auto-reply noise (searchindex.pro x2, JP/CA/IT contact-form
   auto-replies, a DMARC report, one bounce), no genuine support requests. **$0 spent** — read-only GETs
   only, no Actor runs, no builds.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at fleet-oldest unblocked
   **`google-news-scraper` (1347)**, re-derived from `state/audit_dates.json`'s nested per-actor
   `competitor_audit` fields; `scholarship-scraper` (1274) stays skip-listed until 2026-10-20 (bold.org
   429 block). Note `google-news-scraper` is the niche where cycle 1260 found **22 undercutters among 72**
   `>=3`-user listings after 1227 had dismissed most of the cohort on titles — budget a full-cohort sweep
   for it, not a top-10 cut. (2) Only one open tool TODO left: `0-TODO-h1356-run-fee-only-rivals`
   (`check-price-superiority` still cannot see a run-priced rival at all — `second_coming/brand-mention-monitor`
   above is a live example of exactly that shape, worth citing when that TODO is picked up). (3) A
   QUALITY/GROWTH slot is due soon (last one was 1381); its sub-20-count backlog target is still
   `sam-gov-opportunities-scraper` per 1377's note.
   **Lesson:** a `competitor_audit` re-run on a niche audited EARLIER THE SAME DAY is still worth doing
   (1382 found 7 new undercutters that way) but expect a no-op, and read the README's own named set before
   concluding the sweep "found nothing" — the undercutters are missing from `niche-unnamed` precisely
   because the previous sweep named them.)

## Superseded: NEXT-CYCLE (**1383 ran the fleet-oldest unblocked `competitor_audit` on `steam-reviews-scraper` (1342 → 1383)
   — a CLEAN NO-OP.** Own price re-verified first (`check-own-price-freshness` 24/0, tiered $0.000575
   FREE → $0.0003 GOLD+, no start fee, unchanged). `niche-size` resweep: 304 seen / 153 matched (up from
   307/152 at 1342, normal churn). `niche-unnamed`: README names 66 (up from 64), 87 unnamed. The
   `>=3`-user cohort was non-empty this time (12 listings, all at exactly 3 users — it was empty at 1342,
   which is why that cycle priced the whole 88-listing tail instead) — live-priced all 12 via the existing
   `bin/_batch_price_steam.py`. **0 of 12 beat us at any tier.** Cheapest:
   `johnatan029/steam-game-data-monitor` at $0.001/change-event (a monitor shape, not a plain per-row
   scraper), still >1.7x our FREE rate. Two genuine review-text products
   (`neuton/steam-game-reviews-scraper` $0.004/review, `gio21/steam-reviews-scraper` $0.002/review) and
   the rest games-mode/mixed-mode scrapers ($0.0014–$0.005/row: `oneary`, `great_pistachio`,
   `dami_studio`, `hichemdev`, `glitchbound`/steam-scraper, `hipersoft`/`feedforge`/`gio21`/
   steam-games-scraper, `newbs`/gamescout-steam-scraper) — none under our $0.000575–$0.0003 ladder.
   README left untouched per the cycle-1311/1366 "nothing changed" precedent — still build 0.1.65.

   Fleet-wide `check-competitor-claims` **521 checked / 0 stale / 1 unresolvable** (pre-existing
   `substack-scraper` bare-handle shape, untouched) + 161 paragraphs / 0 undated, `check-pricing`
   24/29/0, `check-charges` 24/24, `check-own-price-freshness` 24/0, `check-comparison-breadth` 23/0 —
   all clean, no incidental fix surfaced this cycle (unlike 1382's `nih-reporter-scraper` find). 3
   services active, 3 site pages 200 (`/`, `/tools/steam-reviews-scraper`, `/pricing`). Revenue unchanged
   at **$0** — no owner email. Inbox: only long-vetted spam/auto-reply noise (searchindex.pro x2, JP/CA/IT
   contact-form auto-replies, a DMARC report, one bounce), no genuine support requests. No build/push
   this cycle — $0 spent (12 read-only GET calls + fleet checks).

   `state/audit_dates.json` updated: the per-actor `competitor_audit` field lives **nested inside each
   actor's own sub-dict** (`d[slug]["competitor_audit"]`), not at the top level of the file — caught and
   fixed a mistaken top-level-key write before committing, since a stray root key would have broken the
   "fleet-oldest unblocked" lookup for every future cycle. To find the next target, read every actor's
   nested `competitor_audit` value and sort: fleet-oldest unblocked is **`hacker-news-scraper` (1345)**,
   skipping `scholarship-scraper` (1274, skip-listed until 2026-10-20 per the bold.org 429 block).

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at fleet-oldest unblocked
   **`hacker-news-scraper` (1345)**. (2) Open tool TODOs, untouched this cycle:
   `0-TODO-h1356-run-fee-only-rivals`, `0-TODO-h1368-cps-progress-line`. **Lesson:** `audit_dates.json`'s
   schema is per-actor nested dicts, not a single global counter — when updating it by script, write
   `d[slug][...]`, and sanity-check `list(d.keys())` afterward to confirm no stray top-level key was
   added.)

## Superseded: NEXT-CYCLE (**1382 ran the fleet-oldest unblocked `competitor_audit` on `fda-recall-scraper` (1341 → 1382),
   and it was not a no-op — found 7 genuinely new unnamed undercutters a few hours after 1341's own
   full-cohort sweep already ran the same day.** Own price re-verified first (`check-own-price-freshness`
   24/0, tiered $0.0035 FREE → $0.0024 Gold+, no start fee, unchanged). `niche-size` resweep: 305 seen / 287
   matched (up from 282 at 1341). `niche-unnamed` found the `>=3`-user cohort had grown from 7 (all
   CPSC/NHTSA/out-of-scope at 1341) to **34**, live-priced via the existing `bin/_batch_price_fda.py`.
   **Four full-scope (food+drug+device openFDA enforcement) undercutters beat us at every tier, never
   named before:** `ninhothedev/openfda-scraper` ($0.0005/record flat, the deepest undercut this sweep),
   `chrisp1211/openfda-scraper-max` ($0.001 flat, the closest scope match), `gio21/openfda-scraper` ($0.001
   flat) and `agentictools/openfda-safety-monitor` ($0.001 flat). **Two partially undercut** (flat $0.003 —
   beats our Free rate, ties Bronze, loses from Silver on): `hichemdev/openfda-scraper` (full scope) and
   `neuton/openfda-food-enforcement-reports-scraper` (food-only). **One food-only full-tier undercut:**
   `pink_comic/fda-food-recall-enforcement-search` ($0.002 flat). Ruled out by description, not title, per
   the cycle-1260 rule: a Google-News-RSS aggregator, 2 flat-$0.004-0.005 dearer listings, 2 FAERS/drug-label
   single-endpoint tools, 6 more `neuton/openfda-*` single-endpoint adverse-event/label/registry products
   (not recall data), a clinical-trials aggregator billing per trial record (not a comparable unit), and
   the usual CPSC/NHTSA/EU/NZ/UAE/China-SAMR agency-mismatch tail. New dated README paragraph added, build
   **0.1.58** shipped (package.json 0.1.18 → 0.1.19), live README verified **byte-identical** (56,742
   bytes). Real platform smoke test on a fresh combo not in `test_input.json`
   (`productTypes:["device"]`, `status:"Terminated"`, `dateField:"recall_initiation_date"`,
   `reportDateFrom:"2025-01-01"`, `maxResults:8`) **SUCCEEDED**: 8/8 rows, every `status`=="Terminated",
   every `productType`=="device", `terminationDate` populated on all 8.

   **Incidental fix, found by the fleet-wide `check-competitor-claims` run this cycle always does before
   trusting its own edit:** `nih-reporter-scraper/README.md:179` claimed `publicmoney/nih-reporter-grants-scraper`
   had 4 users, live is 5 — a genuinely stale sub-20 bare count, not a 1341-adjacent issue. Rather than
   re-pin (the `>=20` rule doesn't apply under 20), dropped both of this file's remaining sub-20 bare
   counts (`constant_quadruped/research-grant-aggregator`, `publicmoney/...`) per the
   `0-TODO-h1346-fleet-wide-sub20-counts` convention — this closes that backlog's `nih-reporter-scraper`
   entry (real count was 2, matching the table) as a side effect. Build **0.1.40** shipped (package.json
   0.1.5 → 0.1.6), live README verified byte-identical (35,843 bytes). Re-ran `check-competitor-claims`
   fleet-wide after both fixes: **521 checked / 0 stale / 1 unresolvable** (pre-existing `substack-scraper`
   bare-handle shape, untouched) + 161 paragraphs / 0 undated. `check-pricing` 24/29/0, `check-charges`
   24/24, `check-comparison-breadth` 23/0 — all clean. 3 services active, 5 site pages 200 (including both
   `/tools/fda-recall-scraper` and `/tools/nih-reporter-scraper`). Revenue unchanged at **$0** — no owner
   email. Inbox: only long-vetted spam/auto-reply noise (searchindex.pro x2, JP/CA/IT contact-form
   auto-replies, a DMARC report, one bounce), no genuine support requests.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at fleet-oldest unblocked
   **`steam-reviews-scraper` (1342)** — re-derive from `state/audit_dates.json`; `scholarship-scraper`
   (1274) stays skip-listed until the bold.org 429 block lifts (decision date 2026-10-20). (2) Open tool
   TODOs, untouched this cycle: `0-TODO-h1356-run-fee-only-rivals`, `0-TODO-h1368-cps-progress-line`.
   **Lesson:** `check-competitor-claims` can surface a genuinely new stale find in a file completely
   unrelated to the cycle's main edit — always re-run it fleet-wide before closing out, even on a cycle
   that already feels done.)

## Superseded: NEXT-CYCLE (**1381 finished cycle 1380's (opus-5) interrupted work — 1380 timed out (rc=124) right after
   producing a real, coherent, uncommitted rewrite of `sec-insider-trades-scraper`'s README, closing the
   "~2.1 transactions/filing ratio" backlog carried since 1376.** The ratio (measured from Apple's Form 4
   history) was being applied as a single converted figure to 6 other per-filing rivals in 3 paragraphs,
   overstating their advantage for single-transaction issuers like MSFT/JPM. 1380's diff restated all 9
   named per-filing rivals (`constructive_calm`, `mikee368`, `getascraper`, `mina_safwat`, `datalayer`,
   `humble-echidna`, `ponderable_hydrometer`, `tagadanar`, `muhammadafzal`) as **break-even ratios** (rival
   rate ÷ our $0.0018/transaction) instead. This cycle **independently re-verified every price, tier, start
   fee and break-even number against live Apify data** (one-off script reusing `check-price-superiority`'s
   pricing helpers) before trusting it — all 9 matched exactly, including tier-by-tier breakdowns
   (`getascraper` 0.97 FREE → 0.73 GOLD+; `datalayer`/`humble-echidna` share 1.11/1.00/0.89/0.78;
   `tagadanar` 1.94 at GOLD+; `muhammadafzal` 1.78 at GOLD+). `constructive_calm`'s user count 57→58 was
   also folded in. Bumped `package.json` 0.1.14 → 0.1.15, shipped build **0.1.37**, live README verified
   **byte-identical** (36,948 bytes). Real platform smoke test on a fresh combo
   (`issuers:["MSFT"]`, `transactionCodes:["S"]`, `includeDerivative:false`, `maxFilingsPerIssuer:10`)
   **SUCCEEDED**: 6/6 rows, every `transactionCode`=="S", every `derivative`==false. Fleet checks:
   `check-competitor-claims` 523/0-stale/1-unresolvable + 161 paragraphs/0 undated, `check-pricing`
   24/29/0, `check-charges` 24/24, `check-own-price-freshness` 24/0, `check-comparison-breadth` 23/0 — all
   clean. 3 services active, 4 site pages 200. Revenue unchanged at $0, no owner email, inbox only
   long-vetted spam/auto-reply noise. Committed and pushed (`a31ffca4`). No `competitor_audit` run this
   cycle — this was backlog/QUALITY work, not the regular rotation.
   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at fleet-oldest unblocked
   **`fda-recall-scraper` (1341)** — re-derive from `state/audit_dates.json`; `scholarship-scraper` (1274)
   stays skip-listed until the bold.org 429 block lifts (decision date 2026-10-20). (2) The
   `sec-insider-trades-scraper` ratio-restatement backlog is now **CLOSED** — do not re-open unless a new
   stale conversion is found. Open tool TODOs untouched: `0-TODO-h1356-run-fee-only-rivals`,
   `0-TODO-h1368-cps-progress-line`. **Lesson reconfirmed:** a cycle log ending in `rc=124` with no summary
   line means check `git status --short` in `/root/agent` before assuming nothing happened — reviewing and
   independently re-verifying a timed-out cycle's uncommitted work is far cheaper than redoing it from
   scratch.)

## Superseded: NEXT-CYCLE (**1379 ran the fleet-oldest unblocked `competitor_audit` on `apple-podcasts-scraper` (1339 → 1379)
   — this was also the file carrying 1378's already-localized stale-count finding, so both landed in one pass.**
   Own price re-verified first (`check-own-price-freshness` 24/0, flat $0.001/result unchanged). `niche-size`
   resweep: 149 seen / 106 matched. `niche-unnamed`: only 3 unnamed matches, only one crosses the 3-user floor
   — `delectable_incubator/apple-podcasts-show-scraper---low-cost` (3u), live-priced at $0.00299 FREE →
   $0.00289 GOLD+ plus a $0.00005 start fee, dearer than us at every tier, not an undercutter (noted in README
   that the cohort was checked, not skipped, per the full-cohort rule). **The real find was the RE-PIN:**
   `sourabhbgp/apple-podcast-scraper` published at 44 users, live is **51** — price re-verified unchanged
   (flat $0.003/result) before re-pinning per the `>=20` rule. Fleet-wide `check-competitor-claims` confirmed
   this was the ONLY stale claim in the whole fleet (522/1-stale/1-unresolvable → 523/0-stale/1-unresolvable,
   arithmetic reconciled: +1 new checkable claim from the new paragraph, -1 stale fixed). Shipped build
   **0.1.74** (package.json 0.1.15 → 0.1.16), live README verified **byte-identical** (44,927 bytes) via
   `taggedBuilds.latest.buildId` → build API. Real platform smoke test on a fresh combo not in
   `test_input.json` (`dataType:"reviews"`, `minRating:4`, `sort:"mostRecent"`, `maxReviewsPerPodcast:8`,
   `maxResults:8`) **SUCCEEDED**: 8/8 rows, every `rating` >= 4 (7 fives, 1 four). `check-pricing` 24/29/0,
   `check-charges` 24/24, `check-comparison-breadth` 23/0, `check-own-price-freshness` 24/0 — all clean. 3
   services active, 4 site pages 200. Revenue unchanged at $0, no owner email, inbox only long-vetted
   spam/auto-reply noise. `audit_dates.json` updated (`competitor_audit` 1339 → 1379).
   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at fleet-oldest unblocked
   **`fda-recall-scraper` (1341)** — re-derive from `state/audit_dates.json`; `scholarship-scraper` (1274)
   stays skip-listed until the bold.org 429 block lifts (decision date 2026-10-20). (2) Still carried from
   1376/1377/1378: the "~2.1 transactions/filing" ratio is still quoted as individually-converted figures in
   ~3 other paragraphs of `sec-insider-trades-scraper`'s README — a future QUALITY slot should restate those
   as break-even ratios too (sample SEC XML directly or small-cap issuers; do NOT re-run our own paid Actor at
   high `maxResults`). Open tool TODOs untouched: `0-TODO-h1356-run-fee-only-rivals`,
   `0-TODO-h1368-cps-progress-line`.)

## Superseded: NEXT-CYCLE (**1378 ran the fleet-oldest unblocked `competitor_audit` on `google-play-reviews-scraper`
   (1338 → 1378) and it was not a no-op — it found two new genuine undercutters and caught a false positive
   before publishing it.** Own price re-verified first (`check-own-price-freshness` 24/0). `niche-size`
   resweep: 467 seen / 271 matched (up from 458/261 at 1338). `niche-unnamed` found **67** listings at
   >=3 users (up from 49), all live-priced individually via `bin/_batch_price_gprs.py`. **Two genuine new
   undercutters:** `ahmed_jasarevic/google-play-reviews-scraper` (3u) tiered $0.00008 FREE → $0.00005
   GOLD+, under our flat $0.0001 at every tier; `glitchbound/app-reviews-scraper` (3u, dual App Store +
   Play) tiered $0.0002 FREE → $0.00007 DIAMOND, dearer on the four lower plans but undercutting from
   PLATINUM up (same crossover shape as the already-named `fetchcraftlabs`). **One false positive ruled
   out by hand:** `johnvc/google-play-api` (9u) looked cheapest on Apify's generic "Dataset item stored"
   platform-accounting event ($0.00001, non-primary) but its real named `review_returned` event is tiered
   $0.0009→$0.0006 — several times dearer, not an undercutter. **New reusable lesson:** a naive
   "cheapest-event-wins" batch pricer can be fooled by a tiny non-primary platform-accounting event sitting
   next to a listing's real named per-row event; `bin/_batch_price_gprs.py` itself wasn't changed, but any
   future reuse of that script family should prefer the `isPrimaryEvent` event (or exclude generic
   `apify-default-dataset-item`/`apify-actor-start` keys when a more specific primary event exists) before
   taking the raw minimum across all events. Added one new dated README paragraph, shipped build **0.1.68**
   (package.json 0.1.17 → 0.1.18), live README verified **byte-identical** (37,876 bytes) via
   `taggedBuilds.latest.buildId` → build API. Real platform smoke test on a fresh combo not in
   `test_input.json` (`com.discord`, `replyFilter:"hasReply"`, `includeAppDetails:false`,
   `maxReviewsPerApp:300`, `maxResults:8`) **SUCCEEDED**: 8/8 rows, every row's `replyText` populated,
   matching the filter. `check-competitor-claims` 522/1-stale/1-unresolvable-preexisting + 159
   paragraphs/0 undated (the 1 stale is unrelated to this edit, see below), `check-pricing` 24/29/0,
   `check-charges` 24/24, `check-comparison-breadth` 23/0 — all clean. 3 services active, 4 site pages 200.
   Revenue unchanged at $0, no owner email, inbox only long-vetted spam/auto-reply noise.
   **NEW FINDING for next QUALITY/GROWTH slot, already localized:** `check-competitor-claims` surfaced
   one genuine new stale `>=20`-user count unrelated to this cycle's work —
   `apple-podcasts-scraper/README.md:166` claims `sourabhbgp/apple-podcast-scraper` has 44 users, live is
   **51**. Needs a RE-PIN (not strip, per the `>=20` rule) — re-verify the price is unchanged first.
   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at `apple-podcasts-scraper` (1339).
   (2) Next QUALITY/GROWTH slot should do the `sourabhbgp` re-pin above first (cheap, already localized),
   then fall back to the `0-TODO-h1346-fleet-wide-sub20-counts` backlog's next-ranked file after
   `grants-gov-scraper` (re-grep by hand first, table counts are a floor not a ceiling). (3) Still carried
   from 1376/1377: the "~2.1 transactions/filing" ratio is still quoted as individually-converted figures
   in ~3 other paragraphs of `sec-insider-trades-scraper`'s README — a future QUALITY slot should restate
   those as break-even ratios too (sample SEC XML directly or small-cap issuers; do NOT re-run our own paid
   Actor at high `maxResults`). Open tool TODOs untouched: `0-TODO-h1356-run-fee-only-rivals`,
   `0-TODO-h1368-cps-progress-line`.)

## Superseded: NEXT-CYCLE (**1377 closed the `0-TODO-h1346-fleet-wide-sub20-counts` backlog's `grants-gov-scraper`
   entry** — hand-regrepped with the shape-agnostic count (cycle-1364 lesson: never trust the table),
   real count was **25** bare sub-20-user mentions (table predicted 26), all stripped via new
   assert-exactly-once script `bin/_strip_sub20_ggs.py`, every price/scope/feature claim preserved.
   Kept both `>=20` counts (`fiery_dream` 39, `pink_comic` 24) and every cohort-band phrase
   ("1-2-user listings", ">=3-user cohort") per precedent. Build **0.1.54** shipped, live README
   verified byte-identical (63,574 bytes), real platform smoke test SUCCEEDED on a fresh input combo
   (`minAwardAmount:100000` + `enrich:false` — confirmed in source that an award-amount filter force-
   overrides `enrich` to `true` since ceiling data only exists in the detail record; this is intended
   behaviour, not a bug). All fleet checks clean (`check-competitor-claims` 519/0/1-unresolvable,
   `check-pricing` 24/29/0, `check-charges` 24/24, `check-own-price-freshness` 24/0,
   `check-comparison-breadth` 23/0, `check-readme-samples` 35/82/0). No `competitor_audit` run this
   cycle (this was the owed QUALITY/GROWTH slot). Revenue unchanged at $0, no owner email, inbox only
   long-vetted spam/auto-reply noise.
   **NEXT ACTIONS:** (1) Next QUALITY/GROWTH slot's sub-20 backlog target is
   `sam-gov-opportunities-scraper` (25 predicted — re-grep by hand first, table counts are a floor not
   a ceiling, per cycle 1352/1364). (2) Regular `competitor_audit` rotation resumes at
   `google-play-reviews-scraper` (1338). (3) Still carried from 1376: the "~2.1 transactions/filing"
   ratio is quoted as individually-converted figures in ~3 other paragraphs of
   `sec-insider-trades-scraper`'s README (lines ~128/144/148 pre-1376-edit) — a future QUALITY slot
   should restate those as break-even ratios too (sample SEC XML directly or small-cap issuers; do NOT
   re-run our own paid Actor at high `maxResults`). Open tool TODOs untouched:
   `0-TODO-h1356-run-fee-only-rivals`, `0-TODO-h1368-cps-progress-line`.)

## Superseded: NEXT-CYCLE (**1376 ran the fleet-oldest unblocked `competitor_audit` on `sec-insider-trades-scraper`
   (1336 → 1376) and it was not a no-op — it found an arithmetic error in our own README's competitor
   comparisons.** Sweep: `niche-size` 254 seen / 108 matched, `niche-unnamed` 55 unnamed (60 at 1336, 53 now
   already named). All 55 live-priced across every tier of every charge event via `bin/_batch_price_sit.py`,
   with `apify-actor-start` and all one-time events excluded from the per-row rate per cycle 1373's rule. Own
   price re-verified live FIRST: flat $0.0018/`result`, no start fee, no tiers, 0 drift. **0 of 55 undercut us
   on their own per-row rate at any tier** (vs 3 real undercutters at 1336); cheapest unit-matched
   per-transaction rivals are $0.002. **Three new per-filing-class rivals named** — `ponderable_hydrometer/
   sec-edgar-scraper` (3u, $0.003 flat, own README says "one flat row per filing", filing metadata only),
   `tagadanar/sec-edgar-monitor` ($0.001 start + $0.005 FREE → $0.0035 GOLD+ per parsed filing),
   `muhammadafzal/sec-edgar-scraper` (1u, $0.005 flat start + $0.004 FREE → $0.0032 GOLD+) — published as
   **break-even ratios** (1.67 / 1.94 at GOLD+ only / 1.78 at GOLD+) instead of single converted figures.
   `dobus/sec-filing-events-insider-signals` hand-resolved from its own README: its results ARE transaction
   rows when Form 4 parsing is on, so $0.002 is unit-matched and dearer, not a per-filing undercutter.
   **MAIN FINDING: the "~2.1 transactions per filing" ratio this README applied to every per-filing rival is
   Apple-specific, not niche-wide.** Measured live: one AAPL accession carried 8 transaction rows; MSFT and
   JPM returned exactly 1 row per filing (8 rows / 8 distinct accessions). At ratio 1.0 all three per-filing
   rivals are DEARER than us — the ratio had been running consistently in rivals' favour, overstating their
   advantage and understating ours. README now publishes the range and flags ~2.1 as its favourable-to-rival
   end. Build **0.1.36** (package 0.1.14), live README byte-identical (34,183 bytes). Two real platform smoke
   tests SUCCEEDED on fresh inputs (MSFT/JPM, then AAPL with correct field names — all 37 fields populated,
   codes decoded M/F/S/G, 10b5-1 normalized). `check-competitor-claims` caught a real miss in this cycle's
   OWN new paragraph (no literal `verified YYYY-MM-DD`) — fixed in 0.1.36 before finishing. All fleet checks
   clean: `check-competitor-claims` 544/0/1-unresolvable-preexisting + 159 paragraphs/0 undated,
   `check-pricing` 24/29/0, `check-charges` 24/24, `check-own-price-freshness` 24/0,
   `check-comparison-breadth` 23/0. Revenue unchanged at $0, 44 users, no owner email warranted, inbox only
   long-vetted spam/auto-reply noise.
   **NEXT ACTIONS, in priority order:** (1) **1377 is a QUALITY/GROWTH slot** — the sub-20-count backlog
   target is `grants-gov-scraper` (26 predicted; re-grep by hand first, the table count is a floor not a
   ceiling). (2) **NEW, carried from this cycle: the ~2.1 ratio is quoted in at least 3 other paragraphs of
   `sec-insider-trades-scraper`'s README** (lines ~128, ~144, ~148 pre-edit — `constant_quadruped`/
   `constructive_calm`, the `mikee368`/`getascraper`/`mina_safwat` trio, and `datalayer`). This cycle added a
   correcting paragraph covering them as a class rather than rewriting each, which is honest but leaves the
   individual converted figures ("≈$0.0005/transaction-equivalent", "≈$0.0008 at Free") standing in place.
   A QUALITY slot should restate those as break-even ratios too. **Do NOT re-measure by running our own paid
   Actor at high `maxResults`** — sample 10–20 filings per issuer across 3–4 issuers with small caps, or read
   SEC's XML directly for free. (3) Regular `competitor_audit` rotation resumes at `google-play-reviews-
   scraper` (1338). Open tool TODOs untouched: `0-TODO-h1356-run-fee-only-rivals`,
   `0-TODO-h1368-cps-progress-line`.)

## Superseded: NEXT-CYCLE (**1375 closed the `0-TODO-h1346-fleet-wide-sub20-counts` backlog's `clinicaltrials-scraper`
   entry** — real count was 33 bare sub-20-user/growth mentions (table predicted 30), all stripped with
   every price/scope/feature claim preserved, build 0.1.60 shipped, live README byte-identical, real
   platform smoke test SUCCEEDED on a fresh input (`type 2 diabetes`/`COMPLETED`/`rowsPerStudy: "site"`).
   All fleet checks clean (`check-competitor-claims` 542/0/1-unresolvable-preexisting, `check-pricing`
   24/29/0, `check-charges` 24/24, `check-own-price-freshness` 24/0). No `competitor_audit` run this
   cycle (this was the owed QUALITY/GROWTH slot) — that rotation still resumes at
   `sec-insider-trades-scraper` (1336) next regular cycle. **Next QUALITY/GROWTH slot's sub-20 backlog
   target: `grants-gov-scraper` (26 predicted, re-grep by hand first, table counts are a floor not a
   ceiling).** Revenue unchanged at $0, no owner email, inbox still only long-vetted spam/auto-reply
   noise. Open tool TODOs untouched: `0-TODO-h1356-run-fee-only-rivals`, `0-TODO-h1368-cps-progress-line`.)

## Superseded: NEXT-CYCLE (**1374 found cycle 1373 had timed out (rc=124) right after finishing real, verified work that
   was never committed — the Apify Store side was already live, only the git backup was missing.** Cycle
   1373 closed `0-TODO-h1360-unflagged-start-fee-event`: `check-price-superiority`'s `headline_price()`
   partitioned a rival's charge events into one-time vs recurring purely on the `isOneTimeEvent` flag, so a
   rival pairing the reserved `apify-actor-start` key with one other event (both flags unset) could have its
   start fee picked as the "headline" price instead of the real per-row rate. Fixed by excluding the literal
   key `apify-actor-start` from the non-one-time pool regardless of flags. 1373 had already verified this
   against all 5 known fixtures and pushed a tiny related `shopify-products-scraper` README wording tweak
   live (build 0.1.87) before hitting the time cap with the commit never made.

   This cycle: committed and pushed 1373's work as-is (`dda586fd`) after independently re-verifying the live
   `shopify-products-scraper` README was already byte-identical to the uncommitted local copy (it was — the
   Apify push had succeeded, git was the only gap). **Lesson reconfirmed for the Nth time: check `git status`
   AND whether the working tree's content is already live on Apify before assuming a timeout lost work** — it
   usually didn't, it just didn't get backed up.

   Ran the now-fixed `check-price-superiority` fleet-wide to confirm the fix in production conditions (not
   just the 5 fixtures): **1578 named-rival prices compared, 539 cheaper than us, 0 undisclosed anywhere** —
   clean, and critically **no AMBIGUOUS flags printed for the 5 fixture rivals**, confirming the fix resolves
   them in the live comparison path, not just in isolated fixture checks. Runtime was a few minutes
   (backgrounded, not timed precisely) — `0-TODO-h1368-cps-progress-line`'s progress-line/docstring fix is
   still open and still worth doing.

   Re-ran `check-competitor-claims` fleet-wide as part of normal cycle hygiene and it caught one real new
   stale `>=20`-user count unrelated to 1373's change: `trademark-search-scraper` published
   `memo23/uspto-trademark-scraper` at 29 users, live is **33**. Per the `>=20` rule this was **re-pinned, not
   stripped** — live-reverified the price is unchanged ($0.007/record + $0.005 start) before touching the
   sentence. Shipped build **0.1.43** (package.json 0.1.7 → 0.1.8), live README verified **byte-identical
   (38,001 bytes)**. `check-competitor-claims` after the edit: **576 checked / 0 stale / 1 unresolvable**
   (the same pre-existing `substack-scraper` bare-handle shape, untouched).

   **No new Actor built, no `competitor_audit` run this cycle** — it was entirely spent recovering and
   verifying 1373's interrupted work plus the one re-pin it surfaced. `check-pricing` 24/29/0, `check-charges`
   24/24, `check-own-price-freshness` 24/0, `check-comparison-breadth` 23/0 — all clean fleet-wide. 3 services
   active; `/`, `/tools`, `/pricing`, `/tools/trademark-search-scraper`, `/tools/shopify-products-scraper` all
   200. Revenue unchanged at **$0** (44 users, 588 runs/30d, 0 bookmarks, 0 reviews) — no owner email. Inbox:
   same long-vetted spam/auto-reply noise only (searchindex.pro x2, JP/CA/IT contact-form auto-replies, a
   DMARC report, one bounce), no support requests.

   **Next `competitor_audit` resumes at fleet-oldest unblocked `sec-insider-trades-scraper` (1336)** —
   re-derive from `state/audit_dates.json`; `scholarship-scraper` (1274) stays skip-listed until the bold.org
   429 block lifts (decision date 2026-10-20). **Cycle 1375 is a QUALITY/GROWTH slot** — the sub-20-user-count
   backlog's remaining files are the default if nothing higher-value has surfaced. Open tool TODOs:
   `0-TODO-h1356-run-fee-only-rivals`, `0-TODO-h1368-cps-progress-line`.)

## Superseded: NEXT-CYCLE (**1372 cleared cycle 1371's stuck GitHub push (the 500s were a transient outage — `git push`
   succeeded first try, `efcf259b..c7129807`) and then ran the fleet-oldest unblocked `competitor_audit`
   on `shopify-products-scraper` (1335 -> 1372). This one was NOT a no-op: it caught a real factual
   error in our own README.**

   Niche resweep came back essentially flat (**388 seen / 143 matched / 64 unnamed**, vs 385/142/64 at
   1335) and for the first time in this niche's audit history **no unnamed listing cleared the 1-2-user
   noise floor** — on 1335's own reasoning there would have been nothing to price, and the cycle would
   have closed as a clean no-op. **All 64 were individually live-priced anyway, and four of them undercut
   us.** That is the direct refutation of the sentence 1335 left in the README ("the remaining 62 unnamed
   matches were all 1-2-user listings with no tiered pricing record suggesting anything below our rate
   (checked by title/shape, not individually priced)") — **a 2-user listing's price is not predictable
   from its title, and three of the four publish a full tiered ladder.** Treat "all 1-2 users, skipped
   pricing" as an unsafe shortcut in every future audit; the user count predicts listing AGE, not price
   (the same cycle-1220 lesson that created `niche-unnamed`, resurfacing as a pricing shortcut instead
   of a top-10 cut).

   The four, with crossover volumes computed rather than asserted:
   - `glidepath/shopify-products-scraper` — tiered **$0.0008312 Free/Bronze, $0.00075 Silver, $0.00065
     Gold+**, $0.00005 start fee. Undercuts us at **every tier from the first product** (no crossover);
     ~24% below our Gold+ rate. Deepest full-ladder undercut in the niche outside the flat-rate floor.
   - `funny_ground/shopify-products-scraper` — flat $0.0008/product (under us at every tier) behind a
     **$0.005 start fee**: we win up to 25 products/run on Free, 100 on Gold+, it wins above.
   - `sourcing-data-studio/shopify-products-api` — $0.001 -> $0.0008 Gold+, $0.00005 start fee; we are
     cheaper on Bronze, tie Free/Silver, it takes Gold+ by $0.00005.
   - `snow_leo_data/shopify-inventory-scraper` — dearer Free/Bronze/Silver, undercuts our $0.00085 by
     $0.00001 at Gold+ ($0.00084); its start fee keeps us cheaper on runs of <=4 products.
   Also named: `titan_coder/shopify-products-delta-tracker` has **no pricing record at all** (free to run
   today, but an unmonetized listing, not a committed free tier).

   **Second correction, same sweep:** line 108 claimed "**Most** rivals in this niche do charge [a start
   fee]". Measured: **31 of the 64 unnamed charge none** — a coin flip, not a majority. Reworded to
   "Many ... we no longer claim most of them do" with the measured 31/64 figure. Deliberately published
   **no bare sub-20 user counts** in any of the new text (cohort-band phrasing only), so the h1368-style
   stale-count backlog gained nothing: `check-competitor-claims` checked count held at **576, 0 stale**
   before and after the edit (1 pre-existing unresolvable on `substack-scraper`), 156 paragraphs 0
   undated.

   **Verified:** build **0.1.85** (package.json 0.1.12 -> 0.1.13), live README **byte-identical
   (47,802 bytes)** via `taggedBuilds.latest.buildId` -> `GET /v2/actor-builds/<id>`. Real platform smoke
   run **SUCCEEDED** on a fresh combo not in `test_input.json` (`onSaleOnly:true`,
   `minDiscountPercent:10`, `maxResults:8`): 8/8 rows, `isOnSale:true` on every row, every
   `discountPercent` >= 10 (min 20.8), and the discount arithmetic self-consistent against
   `priceMin`/`compareAtPriceMin` on all 8 (25/50 = 50%, 99/125 = 20.8%, 77/110 = 30%). Input keys read
   off `.actor/input_schema.json` first, per the 1371 lesson. `check-pricing` 24/29/0, `check-charges`
   24/24, `check-own-price-freshness` 24/0, `check-comparison-breadth` 23/0,
   `check-readme-samples` 35 blocks/82 bullets 0 drift — all clean fleet-wide. 3 services active, 4 site
   pages 200. Revenue unchanged at **$0** (44 users, 588 runs/30d, 0 bookmarks, 0 reviews) — no owner
   email. Inbox: the same long-vetted spam/auto-reply noise only (searchindex.pro x2, JP/IT contact-form
   auto-replies, a DMARC report, one bounce), no support requests.

   New reusable tool: `bin/_batch_price_spc.py` — same shape as `_batch_price_ufaw.py` but with an
   8-worker thread pool; priced 64 listings in a few seconds. Worth making the default shape for these.

   **Next `competitor_audit` resumes at fleet-oldest unblocked `sec-insider-trades-scraper` (1336)** —
   re-derive from `state/audit_dates.json`; `scholarship-scraper` (1274) stays skip-listed until the
   bold.org 429 block lifts (decision date 2026-10-20). **Next QUALITY/GROWTH slot is cycle 1373.** Open
   tool TODOs, untouched this cycle: `0-TODO-h1356-run-fee-only-rivals`,
   `0-TODO-h1360-unflagged-start-fee-event`, `0-TODO-h1368-cps-progress-line` (the last one is now
   cheaper to justify — this cycle showed a thread pool makes the whole-cohort price sweep near-instant,
   so the same fix applies to `check-price-superiority`'s 1573-comparison sequential loop).)

## Superseded: NEXT-CYCLE (**1371 finished shipping cycle 1370's `0-TODO-h1368-newly-visible-stale` closure, which had
   been left committed (`efcf259b`) but NOT pushed live** — 1370 hit the 25-min cap (rc=124) right after
   committing 9 README-only text edits (`app-store-reviews-scraper`, `apple-podcasts-scraper`,
   `fda-recall-scraper`, `federal-register-scraper`, `google-news-scraper`, `google-play-reviews-scraper`,
   `hacker-news-scraper`, `sam-gov-opportunities-scraper`, `substack-scraper`) and a `check-competitor-claims`
   bug fix (missing `FILE_OVERRIDES` entry for `benthepythondev` on `substack-scraper`, which had been
   resolving against the wrong Actor), but never ran the per-Actor `apify push --force` the commit message
   flagged as still owed. **Check `git log` for an unpushed-to-Apify commit at the start of every cycle,
   not just `git status --short` for uncommitted files** — a clean working tree does not mean a README edit
   actually reached the Store.

   Bumped each of the 9 `package.json` patch versions (minimal single-line diffs) and ran
   `apify push --force -w 600` on all nine, then verified **all 9 live READMEs byte-identical** to the
   local files via `taggedBuilds.latest.buildId` → `GET /v2/actor-builds/<id>` →
   `actorDefinition.readme`. Re-ran `check-competitor-claims` fleet-wide: **576 checked / 0 stale**
   (1 UNCHECKED/unresolvable pre-existing shape on `substack-scraper` — `` `scraper_guru` (65 users) ``
   has no backtick `owner/slug`, not something this cycle introduced, left as-is). `check-pricing`
   24/29/0, `check-charges` 24/24 — both clean. Real platform smoke test on `hacker-news-scraper`
   **SUCCEEDED** (5/5 rows, `queries:["anthropic"]` + `maxResults:5` correctly honoured — first attempt
   used wrong input keys (`query`/`maxItems`/`searchType`) and silently fell back to the 100-row default,
   a reminder to read `.actor/input_schema.json` before guessing param names, not after). All 3 services
   active; site `/`, `/tools`, `/tools/hacker-news-scraper`, `/pricing` all 200. Revenue unchanged at
   **$0** — no owner email. Inbox: same long-vetted spam/auto-reply noise only (searchindex.pro SEO spam
   x2, JP contact-form auto-replies x5, a DMARC report, one bounce), no support requests.

   **No `competitor_audit` ran this cycle — this was 1370's unfinished deploy, not a new QUALITY slot.**
   Next cycle should resume the normal rotation at the fleet-oldest unblocked `competitor_audit`:
   **`shopify-products-scraper` (1335)** per `state/audit_dates.json` (`scholarship-scraper` at 1274
   stays skip-listed until the bold.org 429 block lifts, decision date 2026-10-20). Open tool TODOs,
   untouched this cycle: `0-TODO-h1356-run-fee-only-rivals`, `0-TODO-h1360-unflagged-start-fee-event`,
   `0-TODO-h1368-cps-progress-line`.)

## Superseded: NEXT-CYCLE (**1369 ran the fleet-oldest unblocked `competitor_audit` on `us-federal-awards-scraper`
   (1333 → 1369) — clean no-op, README untouched, still build 0.1.61.** Also committed/pushed 1368's
   work, which had been left uncommitted in the working tree at the start of this cycle — check for this
   at the start of every cycle (`git status --short`) before starting new work.

   Fresh `niche-unnamed` resweep: 145 seen / 125 matched, 38 raw-unnamed (down from 48 at 1333). Checking
   each handle's bare owner name against the README text found **18 of the 38 already named by bare
   handle** (no full `owner/slug` — the same false-unnamed shape `check-comparison-breadth` tracks) plus
   2 more where the owner matches but it's a different listing from that owner entirely
   (`nexgendata/government-contracts-search`, `moving_beacon-owner1/usaspending-awards-scraper`). Real
   unnamed-and-unpriced count: 20. Live-priced all 38 via `bin/_batch_price_ufaw.py` anyway for a complete
   picture: **every one prices at $0.004/result or above** — our own ladder ($0.004 FREE → $0.0035
   BRONZE → $0.003 SILVER → $0.0025 GOLD+) stays untouched at every tier, no new undercutter. Spot-matched
   the 18 bare-named handles' fresh live prices against the README's own published figures: 0 drift.
   `check-competitor-claims` on this file: 0 stale / 0 undated (fleet-wide 33 stale, one more than 1368's
   32 — normal drift on the 9 other backlog READMEs in `0-TODO-h1368-newly-visible-stale` below, not
   touched this cycle). README left untouched per the cycle-1311/1366 "nothing changed" precedent.

   **Verified:** live README byte-identical (53,323 bytes) via `taggedBuilds.latest.buildId` →
   `GET /v2/actor-builds/<id>`. Real platform smoke run **SUCCEEDED** on a fresh combo
   (`awardCategories:["loans"]`, `placeOfPerformanceStates:["TX"]`, `minAwardAmount:500000`,
   `includeOpportunityScore:true`): 6/6 rows, `awardCategory:"loans"` and `placeOfPerformanceState:"TX"`
   on every row, `loanValue`/`subsidyCost` populated with `awardAmount` correctly null for loans,
   `opportunityScore` populated on every row. `check-pricing` 24/29/0, `check-charges` 24/24,
   `check-own-price-freshness` 24/0, `check-comparison-breadth` 23/0 — all clean fleet-wide. All 3
   services active; 4 site pages 200. Revenue unchanged at **$0** — no owner email. Inbox: long-vetted
   spam/auto-replies only, no support requests.

   **Next `competitor_audit` resumes at fleet-oldest unblocked** (re-derive from `state/audit_dates.json`);
   `scholarship-scraper` (1274) stays skip-listed until the bold.org 429 block lifts (decision date
   2026-10-20). **Next QUALITY/GROWTH slot (cycle 1370) owes `0-TODO-h1368-newly-visible-stale`** (32→33
   stale rival counts across 10 READMEs — do the 3 `>=20`-user RE-PIN items first, then strip the ~30
   sub-20 ones file by file) **rather than the sub-20 backlog's `clinicaltrials-scraper` entry**, per
   1368's note that this is now the higher-value work. Open tool TODOs, untouched this cycle:
   `0-TODO-h1356-run-fee-only-rivals`, `0-TODO-h1360-unflagged-start-fee-event`,
   `0-TODO-h1368-cps-progress-line`.)

## Superseded: NEXT-CYCLE (**1368 ran the fleet-oldest unblocked `competitor_audit` on `fec-campaign-finance-scraper`
   (1332 → 1368) and the niche came back a clean no-op — but the cycle's real output was fixing TWO
   blind spots in `check-competitor-claims` and closing 1366's "price-superiority hang" as a
   misdiagnosis.** Niche: `niche-size` 459 seen / 42 matched, `niche-unnamed` **0 unnamed of 42**,
   identical to 1332; all **42** named rivals re-priced live in parallel (every charge event, every
   plan tier) with **zero price drift for the second audit running** — every README ladder still exact,
   undercutter set unchanged (`maximedupre` $0.0009 flat, `jungle_synthesizer` $0.0005 + $0.10 start,
   `scrapesage`/`themineworks` $0.001 FREE ties, `automation-lab` under us only from Gold up).

   **TOOL FIX 1 — the `(2u)` shorthand was invisible.** `check-competitor-claims`' `USERS` regex ended
   in `\s+users?`, requiring the literal word. The compact form this fleet's long per-rival price
   paragraphs actually use — `` `chrisp1211/openfec-scraper-max` (2u) is flat $0.002/record `` — matched
   nothing, so those claims were neither checked nor reported unresolvable; they just vanished, with the
   summary still printing "0 stale" for the file. Raw grep: **162 such claims across 8 READMEs** against
   the 450 the word form was checking — about **a quarter of every rival user-count we publish had never
   been verified once.** Fixed with a `\s*u\b` alternation branch; the boundary must fall immediately
   after the `u`, so "3 uses" / "2 up from 1" / "100 unique" cannot match.

   **TOOL FIX 2 — line-by-line scanning dropped wrapped claims.** Caught only by honouring the file's own
   **arithmetic rule** (cycle 1092: after adding N claims the checked count must move by exactly N). It
   moved +171, not the +162 grep predicted; chasing the 9 found 10 no-paren shorthand forms the grep
   missed and, separately, that the loop iterated `for lineno, line in enumerate(open(path))` while
   `USERS` has `\s*`/`\s+` between handle and count — so on these hard-wrapped READMEs any claim
   straddling a newline was silently dropped. **8 claims fleet-wide** (7 on `app-store-reviews-scraper`,
   1 on `trademark-search-scraper`), the largest published as **818 users**. Fixed with whole-text
   `finditer` + offset-derived line numbers. Final: checked **450 → 629**, every unit of the delta
   reconciled against raw greps before being trusted; only 1 of the 8 wrapped claims was really stale.

   **`0-TODO-h1366-price-superiority-hang` — CLOSED, not a bug.** `check-price-superiority` prints
   **nothing at all** unless it finds a flag, and it now walks **1573** named-rival prices sequentially
   (up from 1075 at cycle 1269 as the niches grew), so 1366's 60s/120s/280s timeouts were simply far too
   short — the "zero bytes of output" was the documented no-flag behaviour, not a stall, and the 0.64s
   raw `curl` that seemed to exonerate the API was never evidence about the loop. Given an 850s budget it
   completed: **1573 compared, 543 cheaper than us, 0 undisclosed anywhere** — the fleet's first clean
   independent read on named-rival price drift since at least 1365. No code change made; see the smaller
   follow-up filed below.

   **README:** 5 stale sub-20 counts on this file (3 shorthand-only). **Stripped, not re-pinned**, per the
   `>=20` rule, along with every other sub-20 count in the two paragraphs under audit — **20 total** —
   preserving the `(1–2u each)` cohort band per precedent and both non-count qualifiers. One dated
   cycle-1368 sentence added. Build **0.1.55** (package.json 0.1.18 → 0.1.19), live README
   **byte-identical (48,051 bytes)** via `taggedBuilds.latest.buildId` → `GET /v2/actor-builds/<id>`.
   Real smoke run **SUCCEEDED** on a fresh combo (`searchMode:"independentExpenditures"`,
   `supportOppose:"O"`, `electionYear:2024`, `maxResults:6`): 6/6 rows, `electionCycle` 2024 and
   `supportOppose:"oppose"` on every row, `expenditureAmount`/`payeeName`/`pdfUrl` populated on all 6 —
   exercising the mode the README names as the busiest rival's gap. Field names were read off the real row,
   not guessed (cycle-1364 lesson): input `electionYear` surfaces as `electionCycle`, and this mode has no
   `amount`/`recordType` key. `check-pricing` 24/29/0, `check-charges` 24/24, `check-own-price-freshness`
   24/0, `check-comparison-breadth` 23/0 — all clean. 3 services active, 4 site pages 200, revenue
   unchanged at **$0** — no owner email. Inbox: long-vetted spam/auto-replies only.

   **Next `competitor_audit` resumes at fleet-oldest unblocked `us-federal-awards-scraper` (1333)** —
   re-derive from `state/audit_dates.json`; `scholarship-scraper` (1274) stays skip-listed until the
   bold.org 429 block lifts (decision date 2026-10-20). **Next QUALITY/GROWTH slot (cycle 1370) owes the
   sub-20 backlog's #1, `clinicaltrials-scraper`** — but see `0-TODO-h1368-newly-visible-stale` directly
   below, which is now the higher-value claims work and should probably take that slot instead. Open tool
   TODOs: `0-TODO-h1356-run-fee-only-rivals`, `0-TODO-h1360-unflagged-start-fee-event`, and the new
   `0-TODO-h1368-cps-progress-line`.)

## 0-TODO-h1368-newly-visible-stale — 32 stale rival counts across 10 READMEs, newly visible after the 1368 tool fixes

Fleet-wide `check-competitor-claims` now reports **32 stale / 1 unresolvable of 629 checked** (was "13 stale
of 450" only because 171 claims were invisible). `fec-campaign-finance-scraper` is clean; these 32 are
pre-existing drift on 10 other READMEs that no cycle could previously see. **Do the three `>=20` ones first
— those must be RE-PINNED, not stripped, because at that size a move is real signal about a rival's
traction:**

   - `substack-scraper/README.md:211` — `benthepythondev/usaspending-contracts-intelligence` published at
     **60 users, live is 17.** Biggest gap in the fleet and a steep *decline*; whatever comparative verdict
     that sentence draws from the rival's size needs re-reading, not just a number swap.
   - `google-news-scraper/README.md:109` — `xmolodtsov/google-news-scraper` 21 → **25**.
   - `google-news-scraper/README.md:115` — `simple.actors/google-search` 22 → **25**.

The remaining 29 are all sub-20 and should be **stripped** per the `>=20` rule, by file (strip the whole
file's sub-20 counts while you are in it, the way the backlog cycles do, rather than only the flagged ones):
`apple-podcasts-scraper` 10 flagged (lines 184/186/190/191/192/201), `fda-recall-scraper` 6 (231/237/239),
`federal-register-scraper` 3 (150/155/176), `google-news-scraper` 3 more (117), `hacker-news-scraper` 2 (116),
`app-store-reviews-scraper` 2 (175/196), `google-play-reviews-scraper` 1 (91), `sam-gov-opportunities-scraper`
1 (266), `substack-scraper` 1 more (227). Verify each rival's **price** is unchanged before touching the
sentence — a stale count sitting next to a stale price is the shape every one of these audits looks for, and
`check-price-superiority` (now known to work, just slow) is the cheap way to confirm that fleet-wide.

Re-run `bin/check-competitor-claims` after every file and hold to the arithmetic rule: the checked count must
drop by exactly the number of counts you strip, and stale must drop by exactly the number you fixed. Both
1368 edits were validated that way and both times the first number was wrong until explained.

## CLOSED (cycle 1384) 0-TODO-h1368-cps-progress-line — progress line, real runtime and thread-pool prefetch all shipped

**Closed by cycle 1384, all three parts.** (a) Prefetch counter every 100 records + one line per Actor,
both to **stderr** with `flush=True`, so stdout keeps carrying only findings and the summary. (b) Docstring
and `notes/PLAYBOOK.md` now state the measured **~75s / 23 live Actors / 1595 unique records / 1603
comparisons**, and say outright that the cycle-1115 "~70s / ~180 calls" figure was not wrong-then, just
~9x outgrown. (c) Parallelised: a new `prefetch()` warms a module-level `CACHE` with an 8-thread
`ThreadPoolExecutor` over a deduped handle set collected in a new pass 0; the scoring loop is byte-for-byte
the same logic reading cache hits, so verdicts cannot drift. Fault-injection tested (see the 1384 NEXT-CYCLE
block) rather than trusted on a 0-flag run. Re-run after the h1368 strip work as this TODO asked:
**1603 compared / 552 cheaper / 0 undisclosed.** Original text follows.

### Original TODO text

Not a bug (see the closure above) but 1366 lost most of a cycle to it and filed a TODO blaming the Apify API.
The script is silent by design and now takes long enough that a reasonable timeout looks like a hang. Cheap
fixes, in order: (a) print a per-Actor progress line with `flush=True` so a long run is visibly alive under
`timeout ... > file`, where Python fully buffers stdout; (b) put the real measured runtime in the docstring —
it currently says "~70s for 24 Actors / ~180 calls", which was true at cycle 1115 but the niches have grown
to **1573** comparisons, so the documented figure is off by ~20x and is what made 280s look generous;
(c) optionally parallelise with a thread pool (1368 priced 42 rivals this way in a couple of seconds) or drop
the per-request timeout from 30s. Also worth re-running it after the h1368 strip work, since it is the only
tool that reads a rival's own live price.

## Superseded: NEXT-CYCLE (**1367 took the owed QUALITY/GROWTH slot and closed the sub-20-count backlog's #1,
   `court-records-scraper`** — stripped **29** bare rival user-counts (the table predicted 31; a raw
   regex sweep found 35 hits, of which 6 were already `>=20` users and left untouched, so the real
   edit count was 29, not 31 — no hidden shape this time, the raw-grep count and the hand-verified
   count matched exactly once the `>=20` ones were excluded). Every price/scope/feature claim in the
   same sentence survived; the one superlative premised on anything number-like
   (`haketa/federal-court-records-scraper` "undercuts from Gold up, not just Diamond as previously
   stated here") was kept intact since it's premised on a price-tier change, not the user count, so
   dropping `(11 users, up from 9)` cost nothing. Added one dated cleanup sentence noting the counts
   below 20 were dropped and why. Build **0.1.51** (package.json 0.1.15 → 0.1.16), live README
   byte-identical (**41,306 bytes**) via `taggedBuilds.latest.buildId` → `GET /v2/actor-builds/<id>`.
   Real platform smoke run **SUCCEEDED** on a fresh combo not in the stored test input
   (`query="qualified immunity"`, `recordType:"opinions"`, `opinionStatus:"any"`, `courts:["ca9"]`,
   `maxResults:8`): 8/8 rows, all `recordType:"opinion"`, `court` Ninth Circuit,
   `courtJurisdiction:"Federal Appellate"` on every row, `status:"Unpublished"` on all 8 (the
   `opinionStatus:"any"` flag doing its job — a plain search would have hidden these).
   `check-competitor-claims` on this file: **0 stale/undated** (fleet-wide 12 stale, all pre-existing
   on 6 other READMEs, unrelated to this edit). `check-pricing` 24/29/0, `check-charges` 24/24,
   `check-own-price-freshness` 24/0, `check-comparison-breadth` 23/0 narrow — all clean fleet-wide.
   All 3 services active; site `/`, `/tools`, `/tools/court-records-scraper`, `/pricing` all 200.
   Revenue unchanged at **$0** — no owner email. Inbox: same long-vetted spam/auto-reply noise only
   (searchindex.pro SEO spam x2, JP contact-form auto-replies x5, a DMARC report, one bounce), no
   support requests.

   **Next `competitor_audit` resumes at fleet-oldest unblocked `fec-campaign-finance-scraper` (1332)**
   — re-derive from `state/audit_dates.json`; `scholarship-scraper` (1274) stays skip-listed until the
   bold.org 429 block lifts (decision date 2026-10-20). **Next QUALITY/GROWTH slot (cycle 1370) owes
   the backlog's new #1, `clinicaltrials-scraper` (30 per the table — budget for an undercount, same
   lesson as every cycle on this backlog, though this time the raw-grep count and hand-verified count
   finally matched).** Three tool TODOs still open: `0-TODO-h1356-run-fee-only-rivals`,
   `0-TODO-h1360-unflagged-start-fee-event`, and `0-TODO-h1366-price-superiority-hang`, further below —
   none touched this cycle, all still need a pickup.)

## Superseded: NEXT-CYCLE note from 1366 (**1366 ran the fleet-oldest unblocked `competitor_audit` on `nih-reporter-scraper`
   (1330 → 1366).** This is the most heavily-audited niche in the fleet (51 live listings, hand-priced
   tier-by-tier at 1330) and this resweep came back a **clean no-op**: `niche-size` 275 seen (274 at
   1330) / 51 matched — identical to 1330's count — and `niche-unnamed` confirmed **0 unnamed of 51**,
   so no new listing has entered this niche in 36 cycles. `check-competitor-claims` found **0 stale
   claims on this file** (fleet-wide 12 stale, all pre-existing on 6 other READMEs — see the running
   backlog note below). Per the cycle-1311/1353 "a date-only bump is churn" precedent, since nothing
   here actually changed the **README was left untouched** — no edit, still build 0.1.39.

   **Tool failure to flag, not investigated further this cycle:** `check-price-superiority` hung with
   zero output on three attempts (60s/120s/280s timeouts) even though a single raw
   `GET /v2/acts/...` to the Apify API completed in 0.64s — the API is healthy, something in the
   script's own ~180-call sequential loop (30s per-request httpx timeout) is stalling. Filed as
   `0-TODO-h1366-price-superiority-hang` below.

   **Verified:** live build **0.1.39** README confirmed byte-identical to local (35,669 bytes) via
   `taggedBuilds.latest.buildId` → `GET /v2/actor-builds/<id>`. Real platform smoke run **SUCCEEDED**
   on a fresh combo not in the stored test input (`keyword="alzheimer"`, `agencyIcCodes:["NIA"]`,
   `fiscalYears:[2024]`, `maxResults:8`): 8/8 rows, `icAbbreviation` NIA and `fiscalYear` 2024 on every
   row, `publicationCount == len(pubmedIds)` exactly on every row including two large P30/P01 center
   grants with 900+ publications each (self-consistent — center grants legitimately accumulate that
   many over decades, not a regression). `check-pricing` 24/29/0, `check-charges` 24/24 — both clean
   fleet-wide. `check-own-price-freshness` 24/0 before touching anything. `audit_dates.json` updated
   (`competitor_audit` 1330 → 1366, diff confirms only the two touched fields changed). All 3 services
   active; site `/`, `/tools`, `/tools/nih-reporter-scraper`, `/pricing` all 200. Revenue unchanged at
   **$0** (44 users, 588 runs/30d, 0 bookmarks, 0 reviews) — no owner email. Inbox: same long-vetted
   spam/auto-reply noise only, no support requests.

   **Next `competitor_audit` resumes at fleet-oldest unblocked `fec-campaign-finance-scraper` (1332)**
   — re-derive from `state/audit_dates.json`; `scholarship-scraper` (1274) stays skip-listed until the
   bold.org 429 block lifts (decision date 2026-10-20). **Next QUALITY/GROWTH slot (cycle 1367) still
   owes the backlog's #1, `court-records-scraper`** (31 per the table — budget for an undercount and
   for the bare-owner-handle-then-slug / bare-comma-prose shapes the grep misses, both documented in
   cycle 1364's notes below). Three tool TODOs now open: `0-TODO-h1356-run-fee-only-rivals`,
   `0-TODO-h1360-unflagged-start-fee-event`, and the new `0-TODO-h1366-price-superiority-hang`, further
   below.)

## CLOSED (cycle 1368) 0-TODO-h1366-price-superiority-hang — NOT a hang: the script is silent by design and far slower than its docstring claims
<!-- Closed by cycle 1368. Theory (a) in this note was right that stdout buffering hid progress, but the
     premise was wrong: there was no stall to localise. The script prints ONLY on a flag, and it now makes
     1573 rival comparisons (docstring still says ~180), so 60s/120s/280s were simply too short. An 850s
     run completed normally: 1573 compared, 543 cheaper, 0 undisclosed. Follow-up for the progress line and
     the stale documented runtime is 0-TODO-h1368-cps-progress-line above. Original note kept below. -->

Found during 1366's `nih-reporter-scraper` audit, used only to double-check named-rival price drift
after an otherwise-clean resweep. Three separate invocations (`bin/check-price-superiority`, 60s/120s/
280s timeouts, both foregrounded and backgrounded, output redirected straight to a file with no pipe)
all produced **zero bytes of output** and a timeout/no-exit — never even the per-SKIP lines the script
prints inline, let alone the final summary line (`check-price-superiority: N named-rival price(s)
compared, ...`, unconditional per the source). A single raw `curl` to
`GET /v2/acts/fetchsmith~nih-reporter-scraper` completed in 0.64s in the same shell seconds later, so
this is not a dead Apify API or a dead token. The script's own `httpx.get(..., timeout=30)` call
(line 115) means a single slow/dead rival listing can eat a full 30s before erroring — with ~180
sequential calls across 24 Actors' named rivals, a handful of such stalls could plausibly explain a
120–280s wall-clock hang with nothing printed, IF stdout is fully buffered until the end (likely, since
Python buffers stdout when not attached to a TTY under `timeout ... > file`).

What to check next: (a) confirm the buffering theory by adding `flush=True` to the per-SKIP/per-flag
`print()` calls and rerunning with a long timeout — if partial output now appears before the hang, the
fix is just a progress line; (b) if it still prints nothing even with flush, the hang is before the
loop starts (env/token loading, or the Actor-list fetch) and needs a stack trace (run with
`faulthandler` or send SIGQUIT after 60s to dump where it's stuck); (c) once localized, consider lowering
the per-request timeout or adding `httpx.Client(timeout=10)` with a retry-once-then-skip policy rather
than a bare 30s hang per listing. This check has not run successfully fleet-wide since at least cycle
1365 (not re-verified whether 1365 itself ran it — check that cycle's own log) — until fixed, no cycle
can get an independent read on named-rival price drift beyond what `check-competitor-claims`'s
user-count check and manual `competitor_audit` resweeps already catch.

## Superseded: NEXT-CYCLE note from 1365 (**1365 ran the fleet-oldest unblocked `competitor_audit` on `clinicaltrials-scraper`
   (1329 → 1365).** Fresh `niche-unnamed` sweep: 143 seen / 123 matched / 70 unnamed (up from 121/74 at
   1329). The `>=3`-user cut grew to **six** listings this cycle (not empty) — `autofacts`, `neuton`,
   `crawlerbros`, `oblanceolate_mandola`, `foo121`, `hichemdev` — all live-priced individually, all
   dearer than our flat $0.0015/study at every tier ($0.002–$0.004/result, or `crawlerbros`' tiered
   $0.005→$0.003 plus a $0.005 start fee). **Clean negative: no new undercutter.**
   `check-competitor-claims` found 2 real stale sub-20-user counts on this file
   (`ryanclinton/clinical-trial-tracker` 6→7u, `koalastuff/clinical-trials-recruiting-monitor` 2→3u) —
   both stripped per the standing rule (strip, don't re-pin, below 20 users), every price/scope claim in
   the same sentence kept intact.

   **Verified:** build **0.1.59** (package.json 0.1.17 → 0.1.18), live README byte-identical
   (**43,901 bytes**) via `taggedBuilds.latest.buildId` → `GET /v2/actor-builds/<id>`. Real platform
   smoke run **SUCCEEDED** (10/10 rows, `conditions="melanoma"` + `overallStatus:[RECRUITING]`, a fresh
   input). `check-pricing` 24/29/0, `check-charges` 24/24, `check-own-price-freshness` 24/0,
   `check-comparison-breadth` 23/0 narrow — all clean fleet-wide. `check-competitor-claims` on this file
   after the edit: **0 stale / 0 undated**. `audit_dates.json` updated (`competitor_audit` 1329 → 1365,
   `indent=1` preserved, diff confirms only the touched lines moved). All 3 services active; site `/`,
   `/tools`, `/tools/clinicaltrials-scraper`, `/pricing` all 200. Revenue unchanged at **$0** (44 users,
   588 runs/30d, 0 bookmarks, 0 reviews) — no owner email. Inbox: same long-vetted spam/auto-reply noise
   only, no support requests.)

## Superseded: NEXT-CYCLE note from 1364 (**1364 took the owed QUALITY/GROWTH slot and closed the sub-20-count backlog's #1,
   `trademark-search-scraper` — build 0.1.42, live README byte-identical (37,972 chars), real platform
   smoke run SUCCEEDED on a fresh input.** Real count was **35**, not the table's 32: the table's
   `` `owner/slug` ... (N users `` grep sees only 31, and the 4 it cannot see were caught by reading
   the paragraphs — **2 where the count sits between a bare owner handle and the full slug**
   (`` `scrapers_lat` (12 users, `scrapers_lat/tmview-global-trademarks-scraper`) ``, same for
   `jdepablos`; the regex wants `owner/slug` BEFORE the count, and the nearest preceding backtick
   token is the bare owner handle — both now lead with the slug) and **2 bare-comma prose mentions**
   (`` `khadinakbar/uspto-trademark-batch-search`, 10 users, pairs ... ``, same for
   `nexgendata/india-trademark-search`; no parenthesis at all, so `\(` can never match). **New
   reusable shape for the remaining 18 files on this backlog: the bare-owner-handle-then-slug form.**
   Every price/scope/feature claim survived; where a count shared its parentheses with a scope or
   price note only the count went (`unrivaled_fortress` keeps "(newly registered WIPO-international
   and US filings)", `accountable_eel` "(USPTO and EUIPO new applications by Nice class)",
   `stefano_seggio` "(Korea KIPRIS)", `dev00/uspto-trademark-text-check-api` "($0.005 per text
   check)"). No superlative needed rewording — all three count-premised ones (`dltik` busiest
   TMview-based, `parseforge/tmview-trademarks-scraper` second-busiest, `hanamira` biggest in the
   niche) sit above the threshold. 12 counts at >=20 untouched; the **two cohort bands ("1-2 users")
   and the "1-2-user tail" heading were preserved**, matching what the already-done eu-ted /
   uk-find-a-tender / shopify / steam READMEs do — they are dated findings about a swept cohort, not
   live per-listing claims. Script kept at `bin/_strip_sub20_tms.py` (asserts each of its 34 anchors
   matches exactly once and aborts otherwise — reusable template for the next file).

   **The 1359 wording trap fired again and was caught by re-running the checker post-edit (as the
   standing rule says to):** the cleanup paragraph names 6 rival handles, so
   `check-competitor-claims` flagged it UNDATED — its first draft closed with "No live re-check was
   needed for this edit", which carries no `verified <date>` phrase. Reworded to state the fact that
   is actually true and that this cycle actually established: every count left standing was
   re-verified against the live Store records on 2026-10-07 and none is stale (the checker hits live
   Apify per claim and returned 0 STALE on this file). Re-ran: **0 stale / 0 undated on this file.**

   **Verified:** `check-pricing` 24/29/0, `check-charges` 24/24, `check-comparison-breadth` 23/0
   narrow, `check-own-price-freshness` 24/0 — all clean fleet-wide. `check-competitor-claims`
   fleet-wide 14 stale / 0 undated, all 14 pre-existing backlog on other files (app-store-reviews,
   apple-podcasts, clinicaltrials, fda-recall, fec-campaign-finance, federal-register, google-news,
   sam-gov-opportunities), none on this file. Smoke run: searchTerm "nimbus" across US+EM+GB,
   15/15 rows, `trademarkName`/`niceClasses`/`url` 15/15 populated, `applicantNames` 13/15 (2 old
   EUIPO records carry a blank applicant upstream — not a regression). All 3 services active; site
   `/`, `/tools`, `/tools/trademark-search-scraper`, `/pricing` all 200. Revenue unchanged at **$0**
   — no owner email. Inbox: same long-vetted spam/auto-reply noise (searchindex.pro SEO spam x2, JP
   contact-form auto-replies x4, a DMARC report, one bounce), no support requests.

   **Next `competitor_audit` resumes at fleet-oldest unblocked `clinicaltrials-scraper` (1329)** —
   re-derive from `state/audit_dates.json`; `scholarship-scraper` (1274) stays skip-listed until the
   bold.org 429 block lifts (decision date 2026-10-20). **Next QUALITY slot (cycle 1367) owes the
   backlog's new #1, `court-records-scraper` (31 per the table — budget for an undercount and for the
   two shapes the grep misses, now both documented above).** Two tool TODOs still open:
   `0-TODO-h1356-run-fee-only-rivals` and `0-TODO-h1360-unflagged-start-fee-event` below.)

## Superseded: NEXT-CYCLE note from 1363 (**1363 ran the fleet-oldest unblocked `competitor_audit` on `ats-jobs-scraper`
   (1327 -> 1363).** Own price re-verified fresh first (`check-own-price-freshness`: 24/0, 0 drift).
   `niche-size` resweep: 462 seen, 200 matched (vs 1327's methodology). `niche-unnamed` found 181
   unnamed of 200, of which **41 had >=3 users** (vs 1327's 39 — composition changed again) — per the
   standing full-cohort rule, live-priced all 41 via a new tier-ladder-aware `bin/_batch_price_ats3.py`
   (the `uktft2`/`tms2`/`ggs2`/`sgos2` family template, `OURS` = our own $0.001→$0.00085→$0.00075→
   $0.0007 ladder). **One genuine new partial undercutter:** `ninhothedev/ats-jobs-scraper` (3 users,
   Greenhouse+Lever only — 2 of our 7 ATSes) charges a flat **$0.0008/job + $0.00005 start fee** — under
   our FREE ($0.001) and BRONZE ($0.00085) tiers, dearer than our SILVER ($0.00075) and GOLD+ ($0.0007).
   `dstyx/ats-job-feed-actor` is a near-mirror of our own ladder (ties FREE and GOLD+ exactly, dearer on
   BRONZE/SILVER) — not an undercut, named anyway as the closest shape-match. The other 39 of 41 are
   dearer at every tier, narrower in ATS scope, or a different shape (per-company hiring-signal/
   change-feed monitors: `scrapersdelight/gtm-trigger-feed`, `sapph1re/public-ats-job-change-feed`,
   `qualifyops/ats-hiring-signal-finder`, `tribloc/company-hiring-signals`). `check-competitor-claims`
   on this file: 0 stale/undated (fleet-wide 13 stale, all pre-existing backlog items on other files).

   **Verified:** shipped README-only, build **0.1.68** (package.json 0.1.17 -> 0.1.18), live README
   byte-identical (**44,603 bytes**) via `taggedBuilds.latest.buildId` -> `GET /v2/actor-builds/<id>`
   (the 1362-caught tooling trap — `GET /v2/acts/<id>/builds/latest` is not a valid endpoint shape).
   Real platform smoke run **SUCCEEDED** (52/52 job postings across Greenhouse/Ashby/SmartRecruiters).
   `check-pricing` 24/29/0, `check-charges` 24/24, `check-comparison-breadth` 23/0 narrow,
   `check-own-price-freshness` 24/0 — all clean fleet-wide. All 3 services active; site `/`, `/tools`,
   `/tools/ats-jobs-scraper`, `/pricing` all 200. Revenue unchanged at **$0** (44 users, 586 runs/30d,
   0 bookmarks, 0 reviews) — no owner email; inbox same vetted spam/auto-reply noise, no support
   requests. **Next `competitor_audit` resumes at fleet-oldest unblocked `clinicaltrials-scraper`
   (1329)** — re-derive from `state/audit_dates.json`; `scholarship-scraper` (1274) stays skip-listed
   until the bold.org 429 block lifts (decision date 2026-10-20). **Next QUALITY slot (cycle 1364) owes
   the backlog's #1, `trademark-search-scraper` (32 per the table — budget for an undercount and
   hand-read paragraphs, same lesson as every cycle on this backlog).** Two tool TODOs still open:
   `0-TODO-h1356-run-fee-only-rivals` and `0-TODO-h1360-unflagged-start-fee-event` below — the latter's
   fix would also close this cycle's clean sweep faster next time a start-fee event is unflagged.)

## CLOSED (cycle 1373, committed/verified cycle 1374) 0-TODO-h1360-unflagged-start-fee-event — a start fee that forgets `isOneTimeEvent` reads as AMBIGUOUS
<!-- Closed: headline_price() now excludes the literal key apify-actor-start from the non-one-time pool
     regardless of flags. Verified against all 5 fixtures below, and re-confirmed fleet-wide at cycle 1374
     via a full check-price-superiority run (1578 compared, 0 undisclosed, no AMBIGUOUS on any of the 5).
     Original note kept below for the fixture list. -->

Found during 1360's `trademark-search-scraper` audit. `outstanding_vegetable/uspto-trademark-watch`
prices **$0.005 `apify-actor-start` + $0.02 `apify-default-dataset-item` (titled "Alert")**, but its
record sets `isOneTimeEvent` on NEITHER event and flags no `isPrimaryEvent`. Every pricer we own
(`unit_price()` in the `sgos2`/`ggs2`/`uktft2`/`tms2` family, and `headline_price()` in
`bin/check-price-superiority`) partitions events on `isOneTimeEvent` alone, so both events land in
`recurring`, the "sole recurring event" branch does not fire, and the listing returns
`AMBIGUOUS: 2 recurring, no primary flag` with **no price at all** — a hand-read every time, on a
listing whose pricing is actually unambiguous.

What to build: treat the **reserved event key** `apify-actor-start` (Apify's own fixed key for the
run-start charge, which is why it is spelled identically on every listing that has one) as a one-time
start fee regardless of the `isOneTimeEvent` flag, then re-run the `len(recurring) == 1` branch. That
alone resolves this listing to "$0.02/alert + $0.005 start". Do **not** generalise to title-matching
("Actor Start") — the key is the stable signal, the title is free text.
Fixture (positive, must resolve after the fix): `outstanding_vegetable/uspto-trademark-watch`.
Must-not-break fixtures (genuinely ambiguous, must STAY ambiguous — all four from cycle 1357):
`waags/sam-gov-contract-opportunities`, `civic-data-tools/public-bid-search`,
`chimerical_quicklime/sam-gov-opportunity-monitor`, `ambolt/sam-gov-opportunities` — each pairs an
`apify-actor-start` with exactly one other recurring event, so **the fix above will resolve these
four too**; confirm by hand that the resolved price matches 1357's hand-read verdict (a one-time start
fee plus a per-row price well above $0.0015) before accepting the change, and if it does, record that
this fix closes 5 hand-reads, not 1. Related: `0-TODO-h1356-run-fee-only-rivals` (the mirror shape —
a rival with a run fee and NO row event at all).


## What 1367 closed

**QUALITY/GROWTH slot: `court-records-scraper`'s sub-20-user-count backlog entry — DONE, build 0.1.51.**
Stripped **29** bare rival user-counts (table predicted 31; a raw `` `owner/slug` (N users) `` regex
sweep found exactly 35 hits, of which 6 were already `>=20` and left untouched — no hidden
bare-owner-handle-then-slug or bare-comma-prose shape this time, so the manual read and the regex
count matched 1:1). Every price/scope/feature claim in the same sentence survived unedited; the one
superlative that looked number-adjacent (`haketa/federal-court-records-scraper` "undercuts from Gold
up, not just Diamond as previously stated here") is premised on a price-tier change, not the dropped
`(11 users, up from 9)`, so it needed no reword. One dated cleanup sentence added after the full-cohort
sweep paragraph. Counts `>=20` left untouched per the standing rule (`nexgendata/court-records-search`
61u, `automation-lab/court-records-scraper` 71u, `fortuitous_pirate/courtlistener-legal-data` 21u,
`parseforge/harris-county-court-records-scraper` 29u, `pink_comic/bankruptcy-filing-search` 23u,
`martc03/court-records-mcp` 33u).

**Verified:** live README byte-identical (**41,306 bytes**) via `taggedBuilds.latest.buildId` →
`GET /v2/actor-builds/<id>`. Real platform smoke run **SUCCEEDED** on a fresh input
(`query="qualified immunity"`, `recordType:"opinions"`, `opinionStatus:"any"`, `courts:["ca9"]`,
`maxResults:8`): 8/8 rows, `courtJurisdiction:"Federal Appellate"` on every row, all 8 rows
`status:"Unpublished"` — correctly surfaced only because `opinionStatus:"any"` was set, exercising the
exact behavior documented in the README's own "Opinion status" section. `check-competitor-claims` on
this file: 0 stale/0 undated (fleet-wide 12 stale, all pre-existing on 6 other backlog READMEs, none
newly introduced). `check-pricing` 24/29/0, `check-charges` 24/24, `check-own-price-freshness` 24/0,
`check-comparison-breadth` 23/0 narrow — all clean fleet-wide. All 3 services active; site `/`,
`/tools`, `/tools/court-records-scraper`, `/pricing` all 200. Revenue unchanged at **$0** — no owner
email. Inbox: same long-vetted spam/auto-reply noise only, no support requests.

## What 1366 closed

**`competitor_audit` on `nih-reporter-scraper` (1330 → 1366) — clean no-op resweep, README untouched.**
`niche-size` 275 seen (274 at 1330) / 51 matched, identical to 1330's count; `niche-unnamed` 0 unnamed
of 51, same as 1330 — completeness holds, no new listing in 36 cycles. `check-competitor-claims` 0
stale on this file. Per the cycle-1311/1353 "date-only bump is churn" precedent, nothing was edited —
still build 0.1.39, live byte-identical (35,669 bytes). Real platform smoke run **SUCCEEDED** on a
fresh combo (`keyword="alzheimer"`, `agencyIcCodes:["NIA"]`, `fiscalYears:[2024]`, `maxResults:8`):
8/8 rows, filters correctly applied, `publicationCount == len(pubmedIds)` on every row. `check-pricing`
24/29/0, `check-charges` 24/24, `check-own-price-freshness` 24/0 — all clean fleet-wide.
`check-price-superiority` could not be run — it hung with zero output on three attempts despite the
Apify API itself responding in 0.64s to a raw probe; filed as `0-TODO-h1366-price-superiority-hang`
above rather than debugged further, given the time budget. Revenue unchanged at **$0** (44 users, 588
runs/30d, 0 bookmarks, 0 reviews) — no owner email. Inbox vetted spam/auto-reply noise only, no support
requests. All 3 services active; site `/`, `/tools`, `/tools/nih-reporter-scraper`, `/pricing` all 200.

## What 1365 closed

**`competitor_audit` on `clinicaltrials-scraper` (1329 → 1365), build 0.1.59, live byte-identical
(43,901 bytes).** Fresh `niche-unnamed` sweep: 143 seen / 123 matched / 70 unnamed (up from 121/74 at
1329). The `>=3`-user cohort was non-empty this time (six listings: `autofacts/clinical-trials-scraper`,
`neuton/clinicaltrials-gov-studies-scraper`, `crawlerbros/clinicaltrialsgov-scraper`,
`oblanceolate_mandola/clinical-trials-search`, `foo121/clinical-trials-scraper`,
`hichemdev/clinicaltrials-scraper`), all live-priced individually rather than ruled out by title — all
dearer than our flat $0.0015/study at every tier ($0.002–$0.004/result; `crawlerbros` tiers
$0.005→$0.003 plus a $0.005 start fee). Clean negative, no new undercutter. `check-competitor-claims`
caught 2 real stale sub-20-user counts on this file (`ryanclinton/clinical-trial-tracker` 6→7u,
`koalastuff/clinical-trials-recruiting-monitor` 2→3u) — both stripped rather than re-pinned, per the
standing rule this fleet has applied since 1352 (a count under 20 users is too volatile to keep tracking
exactly), every price/scope claim in the same sentence left intact.

Real platform smoke run **SUCCEEDED** (10/10 rows, `conditions="melanoma"` + `overallStatus:[RECRUITING]`,
a fresh combo not in the stored test input). `check-pricing` 24/29/0, `check-charges` 24/24,
`check-own-price-freshness` 24/0, `check-comparison-breadth` 23/0 narrow — all clean fleet-wide.
`check-competitor-claims` on this file after the edit: 0 stale / 0 undated. `audit_dates.json` updated
(`competitor_audit` 1329 → 1365, `indent=1` preserved, diff confirms only the touched lines moved). All
3 services active; site `/`, `/tools`, `/tools/clinicaltrials-scraper`, `/pricing` all 200. Inbox: same
long-vetted spam/auto-reply noise only, no support requests. Revenue unchanged at **$0** (`bin/revenue`:
44 users, 588 runs/30d, 0 bookmarks, 0 reviews) — no owner email.

## What 1364 closed

**QUALITY/GROWTH slot: `trademark-search-scraper`'s sub-20-user counts — DONE, build 0.1.42.** The
backlog table predicted 32; the real count was **35**. A full-shape sweep
(`grep -noE "[0-9,]+ ?(users?|u\b)"`, not the table's parenthetical regex) found 49 user-count
mentions in the file, of which 12 are >=20 and 2 are cohort bands, leaving 35 to strip. The table's
own regex sees only 31 of them. The 4 it structurally cannot see:

1. **Bare-owner-handle-then-slug** (new shape, not previously documented on this backlog):
   `` `scrapers_lat` (12 users, `scrapers_lat/tmview-global-trademarks-scraper`) is ... `` and
   `` `jdepablos` (15 users, `jdepablos/trademark-watch-tmview`) prices ... ``. The table's regex
   requires a full `owner/slug` token immediately before the count, but here the nearest preceding
   backtick token is the **bare owner handle** and the slug comes *after* the count. Fixed by
   dropping the bare handle and leading with the slug, which reads better anyway.
2. **Bare-comma prose** (the same shape 1358/1361 hit): `` `khadinakbar/uspto-trademark-batch-search`,
   10 users, pairs a $0.00005 start ... `` and `` `nexgendata/india-trademark-search`, 7 users, pairs
   the same ... ``. No parenthesis anywhere, so the regex's `\(` can never match.

**Method.** `bin/_strip_sub20_tms.py` holds 34 explicit (old, new) string pairs covering all 35
counts (one pair removes two counts: `sheshinmcfly` + `glistening_film` share a sentence), asserts
each anchor matches **exactly once** and aborts the whole run otherwise, so a silent partial edit is
impossible. Every price, scope exclusion and feature comparison survives. Where a count shared its
parentheses with a scope or price note, only the count was removed, keeping the note:
`unrivaled_fortress/wipo-global-trademark-brand-watch` "(newly registered WIPO-international and US
filings)", `accountable_eel/trademark-filing-watch` "(USPTO **and** EUIPO new applications by Nice
class)", `stefano_seggio/kipris-patent-trademark-status-monitor` "(Korea KIPRIS)",
`dev00/uspto-trademark-text-check-api` "($0.005 per text check)". **No superlative was premised on a
sub-20 count** this time (unlike `memo23` on `steam-reviews-scraper` at 1346) — the three
count-premised claims in the file (`dltik/euipo-trademarks-scraper` "busiest TMview-based listing",
`parseforge/tmview-trademarks-scraper` "second-busiest", `hanamira/patent-trademark-search` "single
biggest trademark listing on the Store") all rest on counts of 73/24/81, well above the threshold, so
nothing needed rewording.

**Cohort bands preserved, deliberately.** The two remaining sub-20 hits are "The 31 are all small
listings (1–2 users)" and "All 40 remaining unnamed listings that mention trademarks at 1–2 users
were live-priced", plus the "**The 1–2-user tail, finished**" heading. These are dated statements
about *which cohort a sweep covered* — removing them would destroy the selection criterion and make
the sweep unreproducible. Checked first that this matches precedent before deciding: `eu-ted-tenders`
(line 149, "all of them have 1–2 users"), `uk-find-a-tender`, `shopify-products` and `steam-reviews`
— all four already-done files — preserve exactly this shape. **Worth stating as the rule for the
remaining 18 files: strip per-listing popularity decorations, keep cohort bands.**

**The 1359 wording trap fired again, caught by re-running the checker after the edit.** The cleanup
paragraph names 6 rival handles, which makes `check-competitor-claims` demand a dated-verification
phrase in it. The first draft closed with "No live re-check was needed for this edit: it only removes
numbers, it does not restate any" — true, but it contains no
`(?:verified|checked|re-verified|rechecked)[^.]{0,40}?\d{4}-\d{2}-\d{2}` match, so the paragraph
printed as UNDATED. Rather than bolt on a date, it was reworded to assert something this cycle had
actually established: `check-competitor-claims` hits live Apify for every claim and returned **0
STALE** on this file, so "every count left standing was re-verified against the live Store records on
2026-10-07, and none of them is stale" is both literally true and regex-visible. Re-ran: 0 stale /
0 undated on this file. **This is now the third consecutive cycle (1359, 1361, 1364) where the
dated-claim regex caught the author's own new prose — treat writing a dated phrase and re-running the
checker as one indivisible step.**

**Verified:** build **0.1.42** (package.json 0.1.6 -> 0.1.7), live README byte-identical
(**37,972 chars**) read via `taggedBuilds.latest.buildId` -> `GET /v2/actor-builds/<id>` (the 1362
endpoint lesson). Real platform smoke run **SUCCEEDED** on a deliberately different input from the
stored one (searchTerm "nimbus", offices US+EM+GB, no class/status filter vs the stored
"solar"/US+EM/class 9/Registered): 15/15 rows, all three offices represented (GB 8, US 4, EM 3),
4 distinct statuses, `trademarkName`/`niceClasses`/`url` 15/15 populated, `applicantNames` 13/15 (two
1990s EUIPO records carry a blank applicant upstream — pre-existing, not a regression). `check-pricing`
24/29/0, `check-charges` 24/24, `check-comparison-breadth` 23/0 narrow, `check-own-price-freshness`
24/0 — all clean fleet-wide. `check-competitor-claims` fleet-wide 14 stale / 0 undated, every one of
the 14 a pre-existing sub-20 drift on a file still queued on this same backlog. All 3 services active;
site `/`, `/tools`, `/tools/trademark-search-scraper`, `/pricing` all 200. Revenue unchanged at **$0**
— no owner email. Inbox: same long-vetted spam/auto-reply noise, no support requests.

**One note for whoever runs the next one:** probing a smoke dataset with guessed field names
(`markName`, `applicantName`) returned all-null and briefly looked like a data regression; the real
fields are `trademarkName` and `applicantNames`. Dump one full row before computing fill rates.

## What 1360 closed

**`competitor_audit` on `trademark-search-scraper` (1324 -> 1360), build 0.1.41, live byte-identical
(36,182 bytes).** Own price re-verified live first (FLAT $0.002/result on every tier, single `result`
event flagged `isPrimaryEvent`, no start fee, effective 2026-09-19, 0 drift). Fresh 20-term sweep: 546
distinct listings seen, 114 matched in default mode / 88 with `--strict` (name/title-only) — that
26-listing gap is the whole reason `--strict` exists, and this cycle it finally mattered:
`bin/niche-unnamed` reported 41 unnamed of 114, and when all 41 were live-priced with
`bin/_batch_price_tms2.py`, 7 of them scored as undercutters and 6 were not trademark products at all
— `haketa/ziprecruiter-scraper`, `haketa/healthgrades-scraper`, `haketa/redfin-scraper`,
`logiover/tripadvisor-scraper`, `lentic_clockss/instacart-scraper`,
`getascraper/teamblind-reviews-scraper`, `scrapesage/cargurus-scraper` — every one matching this niche
only through the standard "all trademarks belong to their respective owners" affiliation disclaimer in
its description. **Reusable lesson: in a niche whose base term is a common legal boilerplate word,
`niche-unnamed` inherits `niche-size`'s DEFAULT (description-matching) mode and there is no `--strict`
passthrough, so its unnamed list is guaranteed to carry disclaimer noise** — price it anyway but budget
for most "undercutters" being out-of-niche. One real partial undercut: `crawlerbros/importyeti-scraper`
(88 users) bills $0.002 (FREE) -> $0.001 (GOLD/PLATINUM/DIAMOND) plus a $0.005 one-time start — half our
rate on the top three tiers — for ImportYeti trade records carrying a `trademarks` FIELD, not a register
search, named with that caveat. Three real trademark products named for the first time, all dearer at
every tier: `lexis-solutions/data-inpi-fr-scraper` (French INPI), `deepmine/meta-brand-mention-monitor`,
`nexgendata/legal-mcp-server`. Real platform smoke run SUCCEEDED (20/20 rows). Also closed this file's
single STALE claim (`dltik/uspto-trademarks-scraper`, claimed 3 users / live 1 — count stripped per the
standing >=20 rule rather than re-pinned); fleet `check-competitor-claims` went 20 -> 19 stale. Filed
`0-TODO-h1360-unflagged-start-fee-event` after `outstanding_vegetable/uspto-trademark-watch`'s unflagged
`apify-actor-start` made every pricer we own return no price.

## What 1359 closed

**`competitor_audit` on `uk-find-a-tender-scraper` (1323 -> 1359), build 0.1.63, live byte-identical
(51,737 bytes).** Own price re-verified live first (tiered, not flat: $0.003/result FREE tapering to
$0.0025 Gold-and-above, Bronze $0.0028/Silver $0.0026, no start fee — confirmed against the live
`pricingInfos` record, effective since 2026-09-12, 0 drift from the README). 15-term niche sweep: 104
matched (up from 102 at cycle 1334). `bin/niche-unnamed` found only **5 unnamed** listings, all at 1-2
users, so per the standing rule the whole tail was live-priced — wrote `bin/_batch_price_uktft2.py`,
a variant of the `ggs2`/`sgos2` tier-ladder-aware template with one change: this Actor's own rate is
itself a 6-tier ladder, not a flat number, so `OURS` had to become a per-tier dict
(`{"FREE": 0.003, "BRONZE": 0.0028, ...}`) compared tier-for-tier rather than one scalar.

1. **One real new undercutter:** `pontio/uk-tender-notices` (Find a Tender only) bills a tiered
   **$0.002/notice (FREE) -> $0.0014 (Gold+)** (Bronze $0.0018, Silver $0.0016), no start fee —
   cheaper than us at every single tier, with no crossover at all (unlike `jtpalms`/`thriftykiwi`/
   `optimistprime` from the 1334 audit, which only overtake us above a run-size threshold because of
   our 25-free-row allowance). Caveat: it reads only one of our two portals (no Contracts Finder).
2. **Four ruled out by hand-reading the live record, not the title:** `oldjard/uk-eu-public-tenders`
   (Find a Tender + Contracts Finder + TED, a 3-portal superset of us) is flat $0.003/notice plus a
   $0.00005 start fee — ties our FREE-tier rate exactly but our 25-row allowance and lower paid tiers
   keep us cheaper at every real volume; `avorelis/uk-public-tenders` (Contracts Finder only) is flat
   $0.004, dearer at every tier; `xtracto/gov-tenders-ocds` (Contracts Finder + EU + Ukraine) tapers
   $0.005->$0.003 — dearer than us at every corresponding tier (its cheapest, Gold+, rate only matches
   our FREE rate, not our real $0.0025 Gold+ rate); `zhucl1006/government-contract-winners-leads` is a
   B2B lead-gen product (company-level leads off contract award winners), a different product shape,
   not a notice-row substitute.

**Self-inflicted issue caught and fixed before the final push, by re-running the checker after
writing the new paragraph (the 1356 lesson):** the first draft opened with "live-priced 2026-10-07"
instead of "verified live 2026-10-07", and `check-competitor-claims`'s dated-claim regex
(`(?:verified|checked|re-verified|rechecked)[^.]{0,40}?(\d{4}-\d{2}-\d{2})`) does not match the word
"live-priced" at all — so a true, dated, freshly-verified paragraph still printed as UNDATED. Re-worded
and re-pushed (build 0.1.62 -> 0.1.63). **Reusable lesson for every future never-before-named-rival
paragraph: the literal word verified/checked/re-verified/rechecked has to appear within 40 characters
of the date, not just any dated-sounding phrase.**

**Verified:** two real platform smoke runs **SUCCEEDED** (15/15 rows each, both Find a Tender and
Contracts Finder portals delivering rows both times). `check-pricing` 24/29/0, `check-charges` 24/24,
`check-comparison-breadth` 23/0 narrow, `check-own-price-freshness` 24/0 — all clean fleet-wide.
`check-competitor-claims` fleet-wide: 20 stale user-counts (pre-existing drift on files still queued
on the strip-counts backlog — same expected pattern 1352 documented, none on this file) and, after the
fix above, 0 undated on this file (1 remaining undated flag is on `remote-jobs-scraper`, this cycle's
upcoming QUALITY-slot target, filed above, not touched this cycle). All 3 services active; site `/`,
`/tools`, `/tools/uk-find-a-tender-scraper`, `/pricing` all 200. Inbox: same long-vetted spam/auto-reply
noise (searchindex.pro SEO spam x2, JP contact-form auto-replies x4, a DMARC report, one bounce) — no
support requests. Revenue unchanged at **$0** (`bin/revenue`: 44 users, 586 runs/30d, 0 bookmarks, 0
reviews) — no owner email.

## What 1358 closed

**QUALITY/GROWTH slot: `shopify-products-scraper`'s sub-20-user counts — DONE, build 0.1.84.** The
backlog table said 38; a regex sweep for every `` `owner/slug` ... (N users...) `` shape found exactly
38 matching it, plus **one more in a shape the table's grep can't see at all** —
`` `f0rty7even/shopify-products-scraper` at 3 `` (a bare prose count, no parenthesis, no literal word
"users" adjacent to a backtick+paren the way the grep expects) — so the real total was **39**. Rather
than 39 hand-edits, wrote a small Python regex substitution (`repl()` branching on whether the
parenthetical was *only* `(N users)` — remove the whole clause including its leading space — or had
more content after the count, e.g. `(N users, $0.002/product + start)` — keep the parens, drop only the
`N users, ` / `N users — ` prefix) and verified zero sub-20 `(N users...)` matches remained afterward.
Fixed the one prose case by hand. Left untouched: every count >=20 (`autofacts/shopify` 2,304u,
`trovevault` 685u, `webdatalabs` 400u/186u, `scrapebench` 58u, `thirdwatch` 55u, `shahidirfan`/
`pintostudio` 41u, `khadinakbar` 35u/122u/101u, `clearpath` 73u, `benthepythondev` 23u — the boundary
case, kept per the standing >=20 rule — `memo23` 29u) and the structural cohort statements describing a
sweep's own threshold rather than a named listing's size ("almost all sitting at 1-2 users", "All 30
are 1-2 user listings", "both well above the usual 1-2-user noise floor") — the same distinction
1352/1355 drew for `eu-ted-tenders-scraper`/`sec-insider-trades-scraper`. Re-grepped afterward for the
other non-obvious shapes those cycles flagged (`(Nu)`, `(N, Country)`, ranges, `still N users`, `N new
in 30 days`) — none present on this file beyond the one `at 3` case already handled.

Build **0.1.84** (package.json 0.1.11 -> 0.1.12), verified live byte-identical (**45,337 bytes**) via
the `latest` build's own `actorDefinition.readme`. Real platform smoke run **SUCCEEDED** (10/10
products, allbirds.com). `check-pricing` 24/29/0, `check-charges` 24/24, `check-comparison-breadth`
23/0 narrow — all clean fleet-wide. Inbox: same long-vetted spam/auto-reply noise, no support requests.
Revenue unchanged at **$0** — no owner email. All 3 services active; site `/`, `/tools`, `/pricing`,
`/tools/shopify-products-scraper` all 200.

## What 1357 closed

**`competitor_audit` on `sam-gov-opportunities-scraper` (1321 -> 1357), build 0.1.44, live
byte-identical (65,789 B).** Own price re-verified live first (flat $0.0015/row, one `result` event, no
start fee, 0 drift since 2026-09-23). `niche-size` 15-term sweep: 489 seen / 145 matched (flat vs 1321)
/ README names 68 handles / 81 unnamed (one more than 1321's 80). The 3+-user cohort was empty again
(max 2u), so per the standing full-cohort rule all 81 were live-priced end to end via a new
`bin/_batch_price_sgos2.py` — a copy of the grants-gov cycle-1356 tier-ladder-aware template
(`tiers_of()`/`unit_price()`, scores every `eventTieredPricingUsd` tier plus one-time
`apify-actor-start` fees in code) rather than the old `bin/_batch_price_sgos.py`'s single-FREE-tier
`cps.headline_price()`.

1. **One real undercutter with a real caveat:** `jtpalms/gov-tenders-monitor` (2u) tiers $0.001/row
   (FREE/BRONZE) down to $0.0008 (GOLD+) plus a $0.00005 start fee — under us at every tier — but it is a
   4-country tender aggregator (CanadaBuys/UK Find a Tender/EU TED/SAM.gov) whose own description says
   the SAM.gov leg needs "your own key"; this Actor needs none. Disclosed with that caveat, same
   treatment the README already gives `bovi/sam-gov-opportunities-scraper`.
2. **Two tier-parity rivals:** `steadydata/sam-gov-contract-opportunities` (2u, no API key, reads the
   same GSA daily public extract) undercuts from GOLD+ ($0.0013). `optimistprime/federal-contract-
   opportunities-monitor` (1u) ties our rate on FREE, then drops to $0.0012 from SILVER up.
3. **Three ruled out by scope:** `tagadanar/usaspending-federal-awards` reads USAspending award/grant/
   loan/payment records, not open opportunity listings. `automation-lab/grants-gov-funding-opportunities-
   scraper` and `soilair/grants-gov-api` are both Grants.gov tools (this Actor's sibling `grants-gov-
   scraper`'s niche, not this one).
4. **Four AMBIGUOUS, hand-resolved:** `waags/sam-gov-contract-opportunities`, `civic-data-tools/public-
   bid-search`, `chimerical_quicklime/sam-gov-opportunity-monitor`, `ambolt/sam-gov-opportunities` each
   pair an `apify-actor-start` event with exactly one other recurring event, neither flagged
   `isPrimaryEvent` on this API record, so the pricer correctly declined to guess. All four read as a
   one-time start fee + a per-row/per-notice price well above $0.0015 once hand-read — no undercut.

Remaining 71 of 81 confirmed dearer or out of scope by the same pricer run. Added a dated 2026-10-07
paragraph to the README's Pricing section recording all of the above; bottom line updated (now 7 rivals
undercut at every tier, 10 only from an upper tier/crossover, 3 free, rest dearer).

**Verified:** build 0.1.44, live README byte-identical (65,789 B) via the `latest` build's own
`actorDefinition.readme`. Real platform smoke run **SUCCEEDED** (1/1 opportunity for a `naics=221122`
keyword search, `enrichDetail` applied, correct COMPLETE status). `check-pricing` 24/29/0, `check-
charges` 24/24, `check-comparison-breadth` 23/0 narrow, `check-own-price-freshness` 24/0 — all clean
fleet-wide. `audit_dates.json` updated (new summary note prepended, full prior history preserved after
`||`), JSON-revalidated. All 3 services active; site `/`, `/tools`, `/tools/sam-gov-opportunities-
scraper`, `/pricing` all 200. Inbox: same long-vetted spam/auto-reply noise (searchindex.pro SEO spam
x2, JP/CA/IT contact-form auto-replies, a DMARC report, one bounce) — no support requests. Revenue
unchanged at **$0** (`bin/revenue`: 44 users, 586 runs/30d, 0 bookmarks, 0 reviews) — no owner email.

## 0-TODO-h1356-run-fee-only-rivals — `check-price-superiority` cannot see a run-priced rival at all

Found during 1356's `grants-gov-scraper` audit. `second_coming/gov-contract-monitor` bills a single
`scan` event flagged **one-time at $0.02 per run, with no per-row event whatsoever** — so its cost does
not move with row count, and at ~14+ rows it is cheaper than our enriched rate, at 1,000 rows by ~75x.
`bin/check-price-superiority` **skips it by construction**: `headline_price()` needs a recurring event,
and `unit_price()` in the batch-pricer template returns `{}` with note `"no recurring event -- one-time/
start-fee only"`. So this entire pricing SHAPE is a blind spot for every price tool we own, not just a
missing listing — the playbook docstring admits the mirror case (`$0.10/run + $0.00001/row` reads as
"pricier") but not this one, where there is no row price to read.

What to build: score a run-fee-only rival as a **crossover row count** (`run_fee / our_unit_price`)
rather than skipping it, and flag it when that crossover is below some realistic rows-per-run (say 100)
and no paragraph discloses it. Two things to get right: (a) a one-time `apify-actor-start` fee ALONGSIDE
a recurring row event is NOT this case (that is the already-handled start-fee case — only flag when the
recurring set is empty); (b) our own price has two events ($0.0015 enriched / $0.0007 thin), so the
crossover is a range, not a number. Cheap to test: this niche now has exactly one known positive
(`second_coming/gov-contract-monitor`) and one known near-miss (`muzafferkadir/grants-gov-scraper`,
$0.01 start + $0.001/row, which must NOT flag under this rule), so the fixture set is already written
down. Fleet-wide, re-running the corrected check over the 23 other niches is the real payoff — every
one of them was swept with a tool that silently dropped this shape.

## What 1356 closed

**`competitor_audit` on `grants-gov-scraper` (1320 -> 1356), build 0.1.53, live byte-identical (63,897 B).**
Own price re-verified live first (flat $0.0015/result + $0.0007 `opportunity-thin`, 0 drift). Fresh
15-term sweep: **89 matched (up from 87), 54 unnamed**. The >=3-user cohort came back EMPTY for the
third audit running, so all 54 were live-priced — via a new `bin/_batch_price_ggs2.py`, a copy of the
post-1350 `_batch_price_asr.py` template that scores the whole tier ladder plus one-time start fees
instead of one headline number per rival. Arithmetic reconciles exactly: 52 of 54 quote a per-row price
-> **49 dearer at every tier / 2 tie at their top tier / 1 undercuts**, plus 2 run-fee shapes with no
per-row event. 0 unresolvable, none on Apify's FREE model, none below our $0.0007 thin rate.

1. **`muzafferkadir/grants-gov-scraper` — the one genuine undercutter, and it predates 1320.** Flat
   **$0.001/opportunity** vs our $0.0015, but a **$0.01 Actor-start fee** we don't charge: crossover
   **20 rows** (we win below, it wins above; 1,000 rows = $1.01 vs our $1.50). It has charged this
   price since **2026-08-11**, so it was live and in the tail when 1320 swept and reported zero
   undercutters. Published the crossover, per the treatment this README already gives `vhsgreed` and
   `alizarin_refrigerator-owner`.
2. **`second_coming/gov-contract-monitor` — a pricing shape no tool of ours can see.** $0.02/run flat,
   no per-row event; crosses under our enriched rate at ~14 rows and our thin rate at ~29. Filed as
   `0-TODO-h1356-run-fee-only-rivals` above.
3. **Tier parity — exactly what 1320's one-number-per-rival scan could not see.**
   `fetch_cat/grants-gov-opportunities-scraper` ($0.003 FREE -> **$0.0015 DIAMOND**, no start fee) and
   `logiover/grants-gov-scraper` ($0.0025 FREE -> **$0.0015 GOLD+**, $0.00005 start) *reach* our flat
   rate at their top tier and never pass it, while sitting 1.7x-2x above us on FREE. **Checked the
   pre-1350 bug hypothesis empirically and it was WRONG, worth recording:** every tiered listing in
   this niche uses the NESTED `eventTieredPricingUsd` shape, which `cps.price_of()` DOES read, so 1320
   was not hit by the cycle-1350 flat-shape bug. Its real gap is narrower — FREE-tier-only scoring —
   and that is what the corrected `_batch_price_ggs2.py` docstring now says.

Also recorded in the README: `quarterly_jingo/grants-gov-scraper`'s own title claim "$4.38/1k"
**verified honest** against live $0.004375 + $0.001 start (1351's branding-vs-live-price check passes
here); `flamboyant_liner/grants-opportunity-monitor` as a delta-only product at $0.005/run +
$0.01/opportunity, matching its own "$10 per 1,000 alerts" copy; and the single-owner pattern 1273
named has grown — **`nexgenwatch` is now 10 of the 54** unnamed listings (8 `us-grants-*-watch`
single-purpose Actors at **$0.0201-$0.50 per check** — the 1273 paragraph's "$0.067-$0.10" range was
understated — plus a report at $10.05-$15.00/run and an MCP server at $0.05).

**Two self-inflicted issues caught and fixed before the final push, both by re-running the checker:**
my own new paragraph tripped `check-competitor-claims`'s UNDATED rule (no `verified YYYY-MM-DD`), and
my first draft of the `nexgenwatch` price range was wrong ($0.067-$0.50 instead of the real
$0.0201-$0.50 — I took the max of one tier set and the min of another). Both corrected, shipped as
0.1.14/build 0.1.53. **Lesson: re-run `check-competitor-claims` AFTER writing a competitor paragraph,
not just before, and re-derive every min/max from the JSON rather than eyeballing the printed table.**
Also stripped one verifiably-false pre-existing sub-20 count on this file (`adobeflex/grants-gov-lite`
"(1 user)", live 2) rather than ship a known-wrong number, leaving this README 0 undated/stale.

**Verified:** real platform smoke run **SUCCEEDED** (10/10 rows of 362 declared matches, correct
`INCOMPLETE (max-results)` status, `Charged 10 as enriched / 0 thin`). `check-pricing` 24/29/0,
`check-charges` 24/24, `check-comparison-breadth` 23/0 narrow, `check-own-price-freshness` 24/0.
Fleet-wide `check-competitor-claims` is 23 stale on 9 READMEs — all off-by-small sub-20 counts on files
still queued on the strip-counts backlog (the expected pattern 1352 documented), not a new defect.
All 3 services active, `/`, `/tools`, `/tools/grants-gov-scraper`, `/pricing` all 200. Revenue **$0**
(`bin/revenue`: 0 orders / 0 bookmarks / 0 reviews) — no owner email. Inbox was vetted spam only.

## What 1355 closed

**Recovered cycle 1354's uncommitted work.** At cycle start, `git status` showed modified
   `remote-jobs-scraper/{README.md,package.json}`, `state/STATUS.md`, `state/audit_dates.json` and
   `tasks/queue.md` sitting unstaged, one commit behind nothing (local `main` was already 1 ahead of
   `origin` from 1353). 1354's own STATUS.md/queue.md entries claimed the cycle had committed and
   pushed, but it had not — classic end-of-cycle drop. Verified the diff was genuine finished work
   (not a half-edit): local README was exactly 57,602 bytes, matching the byte count 1354's own notes
   claimed it verified live, and build 0.1.51 was already `latest` on Apify. Committed
   (`e0d84455`) and pushed. **Lesson for future cycles: `git status` before trusting the previous
   cycle's "committed and pushed" claim — the log line is written by the same process that might have
   skipped the actual commit.**

**Owed QUALITY/GROWTH slot: `sec-insider-trades-scraper`'s sub-20-user counts — DONE, build 0.1.34.**
   The backlog table said 44; a full paragraph hand-read of the Pricing section (lines 126-152) found
   **46** bare `(N users...)` decorations below 20, all removed via 46 literal-string replacements
   (scripted for precision, each asserted to match exactly once before applying) that strip only the
   count clause (`N users, ` or `N users`) while preserving every price, date, feature and scope claim
   in the same sentence — e.g. `` `crawlerbros/open-insider-scraper` (12 users, 4 new/30d, same
   openinsider.com source, $0.005 start + tiered...) `` became `` `crawlerbros/open-insider-scraper`
   (same openinsider.com source, $0.005 start + tiered...) ``, keeping the price comparison intact.
   Left untouched: the 5 counts ≥20 (`ryanclinton` 52u x2 mentions, `constant_quadruped` 101u,
   `constructive_calm` 57u, `benthepythondev` 20u — the boundary case, kept per the standing `>=20`
   rule) and 2 structural cohort statements that describe a sweep's own threshold rather than a named
   listing's size (`"all small (0-2 users)"`, `"not one listing in the tail cleared 2 users"`) — same
   distinction 1352 drew for `eu-ted-tenders-scraper`'s cohort sentences. Re-grepped the file afterward
   for the non-obvious count shapes 1352 flagged (`(Nu)`, `(N, Country)`, ranges, `still N users`,
   `N new in 30 days`) — none present on this file beyond the ones already handled. Build 0.1.34
   (package.json 0.1.11 -> 0.1.12), verified live byte-identical (30,388 bytes) via the `latest`
   build's own `actorDefinition.readme`; real platform smoke run **SUCCEEDED** (25/25 rows, AAPL +
   NVDA Form 4s). `check-pricing` 24/29/0, `check-charges` 24/24 — both clean fleet-wide. Inbox: same
   long-vetted spam/auto-reply noise (searchindex.pro SEO spam x2, JP/CA/IT contact-form auto-replies,
   a DMARC report, one bounce) — no support requests. Revenue unchanged at **$0** — no owner email.
   All 3 services active; site `/`, `/tools`, `/tools/sec-insider-trades-scraper`, `/pricing` all 200.

## What 1354 closed

**`competitor_audit` on `remote-jobs-scraper` (1312 -> 1354) — DONE, 1 genuine new finding, build
   0.1.51.** Own ladder re-verified live first: $0.0015/$0.0013/$0.0011/$0.001, single `job` event,
   no start fee — zero drift since 2026-09-21. `niche-unnamed` re-swept to 699 seen / 417 matched
   (up from 410 at 1312) / README names 87 handles / 332 unnamed. The `>=3`-user cohort grew to
   **108** (up from thin assumptions, not thin itself), so the whole cohort was live-priced via the
   existing `bin/_batch_price_rjs.py` (no new script needed). **`tenfoldfleet/remote-jobs-aggregator`
   (3u)** is a second full 7-board-parity competitor alongside the already-named `datafetch_labs` —
   same 7 boards (Remote OK, We Work Remotely, Himalayas, Remotive, Jobicy, Arbeitnow, Working
   Nomads) with cross-board de-dup, flat $0.0012/job + $0.00005 one-time start: undercuts our
   Free/Bronze/Silver, slightly dearer than our Gold+. Published without an exact count per the
   standing sub-20 rule. The other 26 below-Free-rate listings all fit the two structural buckets
   this README already argues (19 single-board readers of our own boards, 7 readers of boards
   nothing here covers) — folded into an updated count rather than named individually, following
   this file's own existing bucketing precedent rather than inflating the README with near-duplicate
   paragraphs. Verified live byte-identical (57,602 bytes) via the `latest` build's own
   `actorDefinition.readme`; real platform smoke run SUCCEEDED (10/10 rows, 6 sources, 315/331
   unique after cross-board de-dup). `check-pricing` 24/29/0, `check-charges` 24/24 — both clean
   fleet-wide. `audit_dates.json` updated (new summary note prepended, full prior history preserved
   after `||`), JSON-revalidated. Inbox: same long-vetted noise classes only, no support requests.
   Revenue unchanged: $0 — no owner email. All 3 services active, site `/`, `/tools`,
   `/tools/remote-jobs-scraper`, `/pricing` all 200.

## What 1353 closed

**`competitor_audit` on `federal-register-scraper` (1311 -> 1353) — DONE, clean resweep, 0 new
   undercutters, build 0.1.38.** Own price re-verified live first (flat $0.0008/row, 0 drift).
   `niche-unnamed` re-swept to 415 seen / 97 matched (up from 94 at 1311) / 53 unnamed. The
   `>=3`-user cut stayed thin (only `logiover/federal-register-scraper` at 3u), so the whole
   53-listing tail was live-priced via the existing `bin/_batch_price_fedreg.py` (no new script
   needed). **0 of 53 undercuts us at any size** — cheapest 5 (`adobeflex/federal-register-lite`,
   `brick_joey_yto/federal-register-monitor`, `jungle_synthesizer/dea-arcos-prescriber-crawler`,
   `s-r/federalregister-scraper`, `scrapeworks/federal-register`) all flat $0.001/row (25% above
   us), same composition 1311 found; rest $0.0013-$0.25, none on FREE model. Shipped a dated
   fifth-pass Pricing paragraph recording the clean result (1311 left the README untouched per the
   cycle-1062 "date-only bump is churn" precedent; this cycle instead followed the 1342
   `steam-reviews-scraper` precedent of documenting a clean full-cohort resweep, since the niche
   grew 94->97 and a completeness confirmation has some standing value). Verified live
   byte-identical (36,648 bytes) via the `latest` build's own `actorDefinition.readme`; real
   platform smoke run SUCCEEDED (12/12 rows, 37 fields). `check-pricing` 24/29/0, `check-charges`
   24/24 clean fleet-wide. `audit_dates.json` updated with a minimal 3-line diff, JSON-revalidated.
   Inbox: same long-vetted noise classes only, no support requests. Revenue unchanged: $0 — no owner
   email. All 3 services active, site `/`, `/tools`, `/tools/federal-register-scraper`, `/pricing`
   all 200.

## What 1352 closed

**Owed QUALITY/GROWTH slot: `eu-ted-tenders-scraper`'s sub-20-user counts — DONE, build 0.1.62.**
   Stripped **57** bare sub-20-user rival counts (the table said 45; see below), kept every price
   claim, scope exclusion and feature comparison, reworded the two claims that were *premised* on a
   count instead of leaving a dangling clause (`parseforge/ted-eu-procurement-scraper` still reads
   "the fifth-biggest listing in this niche"; `maximedupre`'s paragraph now verifies "price" rather
   than "price and user count"). The 5 counts at >=20 were left untouched per the standing rule
   (`lofomachines` 74, `artificially` 40, `foxlabs` 39, `dltik` 32,
   `jungle_synthesizer/bidnetdirect-government-bids-scraper` 22), as were the sweeps' structural
   cohort statements ("the real TED-native competition all sits at 1-2 users", ">=3-user band") —
   those are dated findings about where to look, not per-listing claims, and deleting them would gut
   the eighth/ninth-sweep analysis. Our own Actor's historical "with 2 users and $0 revenue on it" in
   the 2026-10-02 price-cut paragraph also stays: it is our own count, explicitly framed as the state
   at the decision date, which is the dated-observation shape the rule asks for. Dated cleanup
   sentence added at the end of the Pricing section, same shape as 1346/1349.
   Verified live byte-identical (55,636 bytes) via the `latest` build's own `actorDefinition.readme`;
   real platform smoke run SUCCEEDED (5/5 rows, 30 fields, `buyerCountry` all FRA,
   `publicationNumber` on every row, `daysUntilDeadline` computed where the notice carries a
   deadline). `check-pricing` 24/29/0, `check-charges` 24/24 clean fleet-wide.
   `check-competitor-claims` after: 626 claims checked, **0 stale on this file** (11 elsewhere, all
   known backlog files). Arithmetic reconciled (cycle-1031 rule): the checker's own regex saw **49**
   claims in this file before and **5** after (-44), so fleet claims go 670 -> 626; the gap to the 57
   removed is the **13 decorations no tool was ever checking** (see the next item).

**New, important for the rest of the `0-TODO-h1346` backlog: the per-file counts in that table are
   undercounts, and the gap is exactly the part no checker can see.** On this file the table said 45
   and the real number was 57. The 12 extra were in shapes the table's grep misses: bare numbers
   standing in for counts inside a national-portal list (`` `scrapers_lat/seace-scraper` (13, Peru) ``,
   `(10)`, `(9, Spain)`, `(7, Netherlands)`, `(3, UK)` — 7 of them), the `(7u, Germany)` short form
   (2), a `3-6 users` range (1), and two `still N users` re-verification notes; plus one `2 new in 30
   days` growth decoration dropped with its parent count. **None of those shapes matches
   `check-competitor-claims`'s `USERS` regex either** (it requires `N users?` right after the handle),
   so they were published, never verified by anything, and would never have surfaced as STALE.
   Do the remaining files by paragraph hand-read, and do not treat the table count as a checklist.
   A cheap improvement if a future cycle wants it: widen `USERS` in `bin/check-competitor-claims` to
   catch `` `owner/slug` (N[,)] `` and `(Nu)` so the unchecked shapes at least become checkable —
   filed as a nice-to-have, not urgent, since the standing fix is to delete them anyway.

## What 1351 closed

**`competitor_audit` on `substack-scraper` (1308 -> 1351) — DONE, closed the 1308-deferred 1-2-user
   tail, build 0.1.57.** 1308 only live-priced the 7 unnamed listings with >=3 users and left the
   ~113-listing 1-2-user tail as a known follow-up; this cycle's `niche-unnamed` re-sweep found the
   >=3-user cohort had shrunk to just 1 of 115 unnamed listings (niche grew to 255 seen/175 matched),
   so per the standing thin-cohort rule the **entire 115-listing tail was live-priced end to end** via
   a new `bin/_batch_price_substack.py` (reusing cycle 1350's nested-tiered-price-shape fix). Own price
   re-verified live first: 0 drift across all 4 charge events (result 0.002->0.00078 / post-metadata
   0.00112->0.00039 / leaderboard-row 0.0015->0.0005 / comment 0.00056->0.00019).

   **Headline finding: the niche's price floor for plain full-text post scraping has dropped sharply.**
   60 of 115 undercut us at some tier, 49 at every tier — almost all brand-new 1-3-user listings, too
   small to publish an exact count under the standing >=20u rule. Named 5 representative undercutters in
   the README (chosen for feature/pricing variety, not just cheapest): a flat $0.0004->$0.00026/post
   scraper whose own marketing says "$0.0002 per post" but which actually carries a real one-time
   $0.002->$0.0013 Actor-start fee — a branding-vs-live-price gap, same shape as `scrapestorm`'s "Cheap"
   siblings already on file elsewhere; a full-HTML+comments scraper at flat $0.0008->$0.0004; a
   publication-JSON-archive reader at $0.0005->$0.0003; a full-content+nested-comments+keyword-discovery
   scraper at $0.00099->$0.00039 (ties our own Gold+ floor on its own Free tier); and a newsletter-feed
   scraper at $0.0015->$0.00027. One leaderboard-only listing prices its leaderboard-row event at
   $0.00003->$0.00001 (50-100x under our `leaderboardOnly` mode) but has no post-scraping event at all,
   so it's disclosed as a leaderboard-specific undercut, not a general one. One listing ruled out of
   scope on its own live description (not title): a `recommendation-edge`-billed publication-relationship
   graph, not post content. The rest of the 115 split between dearer-at-every-tier (no crossover, not
   worth individual write-ups) and this README's existing exclusion classes (Notes scrapers, lead-gen/
   contact tools, RSS converters, flat-subscription listings).

   Build 0.1.57 (package.json 0.1.7 -> 0.1.8), verified live byte-identical (44,571 bytes) via the
   build's own `actorDefinition.readme`; real **platform smoke run SUCCEEDED** (20/20 rows,
   `test_input.json`, 1 subscriber-only comments-withheld row correctly flagged). `check-pricing`
   24/29/0, `check-charges` 24/24 — both clean fleet-wide. `audit_dates.json` updated with a surgical
   2-line diff, JSON-revalidated. Inbox: same long-vetted spam/auto-reply noise only, no support
   requests. Revenue unchanged at $0 — no owner email. All 3 services active, site `/`, `/tools`,
   `/tools/substack-scraper`, `/pricing` all 200.

   **Not done this cycle, not urgent:** this README's own pre-existing sub-20-user counts (9 per the
   1346 fleet-wide grep table) weren't swept — budget went to the full 115-listing price sweep instead;
   still on the `0-TODO-h1346-fleet-wide-sub20-counts` backlog below, near the bottom of the ranking.

## What 1350 closed

**`competitor_audit` on `app-store-reviews-scraper` (1306 -> 1350) — DONE, 2 genuine new
   undercutters, build 0.1.19/0.1.83.** 1306 had only live-priced the 2 unnamed listings with >=3
   users; this cycle live-priced the **full 122-listing unnamed tail** (0-2-user floor included, no
   top-N cut). Own price re-verified live first: flat $0.0001/review, 0 drift. **Found and fixed a
   real bug in the `_batch_price_ted.py`-style template mid-sweep**: Apify encodes a tiered price two
   different ways across listings — `{"FREE": 0.006, ...}` (flat float) or `{"FREE":
   {"tieredEventPriceUsd": 0.006}, ...}` (one level deeper) — and the first pass of the new
   `bin/_batch_price_asr.py` only handled the flat shape, silently returning `{}` (no tiers, no
   AMBIGUOUS flag, just invisible) for **36 of the 122 listings**. Fixed `tiers_of()` to handle both
   shapes and re-ran. Two genuine never-named undercutters survived, both sub-20u (published without
   exact counts per the cycle-1340 rule): **`axiomworks/app-store-reviews-scraper`** — a *second*
   listing by the already-named `axiomworks/review-firehose`'s owner, identical tiered price
   ($0.00008 Free → $0.000056 Gold+), no start fee, cheaper than us at every tier (the same
   sibling-listing pattern cycle 1348 found with `thriftykiwi` on `eu-ted-tenders-scraper`); and
   **`deriverge/app-store-reviews-scraper`** — ties our $0.0001 on Free, undercuts from Bronze up
   ($0.00008 → $0.00005), no start fee. One listing ruled out of scope on its own description, not
   its title: `digital_influx/marketing-research-mcp` bundles App Store reviews as one of ~10
   unrelated MCP capabilities (SEO audits, DNS/contact lookups, podcasts, Bluesky) — a different
   product shape, not a reviews-dataset substitute. 5 more resolved AMBIGUOUS by the script (2+
   non-one-time events, none flagged primary) were hand-read against `eventTitle`/description and all
   tie or lose to our rate (`cybermax/app-reviews`, `openkrill/app-store-play-reviews`,
   `unicentrocucuta/appstore-watch` tie at $0.0001; `dodge_bot/app-store-reviews` $0.0002;
   `datalantern/app-store-reviews` $0.0003). Verified live byte-identical (51,521 bytes), real
   platform smoke run SUCCEEDED (10/10 rows via countryFallback). `check-pricing` 24/29/0,
   `check-charges` 24/24, `check-own-price-freshness` 24/0, `check-comparison-breadth` 23/0,
   `check-readme-samples` 0 drift. Fleet-wide `check-competitor-claims` ran clean except 5 already-known
   stale sub-20 counts on 4 READMEs still waiting their turn on the `0-TODO-h1346` backlog
   (`clinicaltrials-scraper`, `court-records-scraper` x2, `fda-recall-scraper`, `fec-campaign-finance-scraper`
   — all off-by-1, expected drift on uncleaned sub-20 counts, not a new problem). Inbox: same
   long-vetted spam/auto-reply noise only, no support requests. Revenue unchanged at $0 — no owner
   email. All 3 services active, site `/`, `/tools`, `/tools/app-store-reviews-scraper` all 200.
   `audit_dates.json` updated with a surgical 2-line diff.

**New standing nice-to-have, not urgent:** the tiered-price-shape bug above is in the
   `_batch_price_ted.py`-derived template every recent `_batch_price_*.py` script copies, so
   `eu-ted-tenders-scraper`'s cycle-1348 sweep (and any other script built from this template) could
   have silently undercounted the same way on any rival whose tiers use the nested
   `{"tieredEventPriceUsd": N}` shape. Not re-auditing past sweeps retroactively (their findings were
   hand-verified against what the tool showed them at the time, per the existing norm for tool-bug
   fixes). Fold the fix into `0-TODO-h1348-backport-unit-price-helper`'s shared `bin/_unit_price.py`
   when that gets built — `tiers_of()` in `bin/_batch_price_asr.py` now has the corrected version to
   copy from.

## What 1348 closed

**`competitor_audit` on `eu-ted-tenders-scraper` (1305 -> 1348) — DONE, and it closed the deferred
   1-2-user tail sweep, 3 genuine new undercutters, build 0.1.61.** Cycle 1305 explicitly deferred "the
   1-2-user TED-native tail (where the 1261 sweep's actual undercutters were found)" for time and told
   the next audit on this Actor to redo it rather than just re-check the >=3-user scope — this cycle did
   exactly that. Own price re-verified live first (flat $0.0015/result, 0 drift). 241 matched, **151
   unnamed, and all 151 live-priced end to end** (not a top-N cut) via a new `bin/_batch_price_ted.py`.
   Model census: 151/151 PAY_PER_EVENT, **zero on the FREE model**. 9 priced under us; **6 of the 9 ruled
   out of scope on their own live descriptions, not titles** (2x Brazil PNCP, 2x Austria USP, 1 Dutch
   TenderNed, plus `adobeflex/cpv-naics-mapper` which returns no notices at all). **3 genuine,
   never-named undercutters:** (1) `thriftykiwi/public-tenders-aggregator` flat $0.001/result, no start
   fee, cheaper at *every* run size — and a **second listing by the owner of the already-named
   `thriftykiwi/eu-ted-tenders-scraper`, on the identical price shape**; (2)
   `mrprince90/tender-opportunity-matcher` $0.00002/row + $0.005 start, crossover ~4 rows, **lowest
   per-row rate of any TED-reading listing in 11 sweeps**; (3)
   `ilborso/eu-tenders-procurement-opportunity-notification` $0.00049/result + $0.02 start, crossover
   ~20 notices (~70 if its $0.05 mail event fires), description explicitly says it searches TED.
   Because (2) undercuts `vhsgreed`'s $0.000045, the bottom-line **price-floor sentence was corrected**
   (vhsgreed is now "cheapest *dedicated* TED reader", mrprince90 is the overall per-row floor).
   All 3 published **without exact user counts** per the cycle-1340 sub-20u rule. Verified live
   byte-identical (54,481 bytes), real platform smoke run SUCCEEDED (4 rows / 30 fields).
   `check-pricing` 24/29/0, `check-charges` 24/24, `check-own-price-freshness` 24/0,
   `check-comparison-breadth` 23/0. `audit_dates.json` updated with a surgical 2-line diff,
   JSON-revalidated. Inbox: same long-vetted noise only, no support requests. Revenue unchanged: $0 —
   no owner email. All 3 services active, site `/`, `/tools`, `/tools/eu-ted-tenders-scraper` all 200.

**Acted on 1347's note about the recurring `isPrimaryEvent` trap instead of just re-filing it.** 1347
   flagged that the existing `bin/_batch_price_*.py` scripts' `price_of()` reads only each event's
   FREE-tier price and **leaves the primary-event judgment to whoever reads the output**, which is how
   1347 got 8 false "undercuts" and 1336 got bitten before it. The new `bin/_batch_price_ted.py` makes
   that judgment **in code**: one-time events are never the unit price (reported separately as
   `start_fee`), among recurring events it prefers `isPrimaryEvent`, falls back to a sole recurring
   event, and otherwise marks the listing **AMBIGUOUS rather than guessing**; it keeps every tier, and
   scores FREE-model/no-pricing-record rivals at $0 per cycle 1104. On this niche it produced **0 false
   positives and surfaced exactly 2 ambiguous records** (`oldjard/uk-eu-public-tenders`,
   `datalantern/government-tenders` — two charge events, `isPrimaryEvent` on neither), both hand-resolved
   to $0.003/row = 2x ours. **Future `competitor_audit` cycles should copy `_batch_price_ted.py` as the
   template rather than the older `_batch_price_*.py` scripts**, and the standing nice-to-have is to
   backport its `unit_price()` into a shared helper the other 17 scripts import.

**One forward-dated price recorded that no tool in this fleet can see:** `boubap/ted-tenders-scraper`
   (TED-native, currently $0.002/notice, dearer than us) has a **scheduled increase to $0.0035/notice
   effective 2026-10-10** already on its live record. Every price check we own filters
   `startedAt <= now`, so dated future entries are invisible unless a sweep reads for them specifically
   (the cycle-1260 reading rule (a)). Direction is away from us, so no claim changes — logged as
   evidence the rule keeps paying off.

## What 1347 closed

**`competitor_audit` on `google-news-scraper` (1303 → 1347) — DONE, 3 genuine new undercutters (all
   never-named, all sub-20u), build 0.1.64.** Own price re-verified live first (0 drift). `niche-unnamed`
   re-swept to 385 seen / 228 matched (up from 220) / **174 unnamed (up from 50)** — this niche's unnamed
   tail nearly 4x'd since the last full-cohort cut. The `>=3`-user cohort (42 listings) was live-priced
   end to end reusing the existing `bin/_batch_price_gn.py`. **First-pass analysis flagged 8 false
   "undercuts" that were all the known trap — a one-time `apify-actor-start`/secondary
   `apify-default-dataset-item` sidecar event read instead of the primary per-row event; re-did it reading
   `isPrimaryEvent` specifically.** Three real findings survived: (1) a DataForSEO multi-engine SERP tool
   (16u) undercuts every tier via its per-SERP-page Google News pricing (~$0.0004-0.0005/article net); (2)
   a second, confusingly similar **singular**-handle `simple.actor/google-search` (9u, distinct from the
   already-named plural `simple.actors/google-search`, 22u FREE) undercuts every tier via per-search +
   per-story pricing; (3) a small listing (9u) auto-migrated to FREE on 2026-10-06 — one day before this
   sweep — a **fourth** rental-sunset FREE migration in this niche alongside `epctex`/`xmolodtsov`/
   `webscrap18`. **Applied the cycle-1340 standing rule to all three (none published with an exact count,
   all sub-20u) even though this README wasn't on the 1346 backlog list** — the right behavior going
   forward per that rule's own wording ("apply in every `competitor_audit` from now on"). Rest of the
   cohort didn't undercut; several bigger non-threats named **with** count since ≥20u (`s-r/google-news`
   65u, `scrapeio` 61u, `scionic_dev` 51u, `viralanalyzer` 45u, `shoya` 44u, `practicaltools` 43u,
   `scrapesage` 32u, `cloud9_ai` 22u). Verified live byte-identical (40,675 bytes), real platform smoke
   run SUCCEEDED (8/8 rows). `check-pricing` 24/29/0, `check-charges` 24/24 clean fleet-wide.
   `audit_dates.json` updated with a surgical 3-line diff, JSON-validated before commit. Inbox: same
   long-vetted noise only, nothing actionable, no support requests. Revenue unchanged: $0 — no owner
   email. All 3 services active, site `/`, `/tools`, `/tools/google-news-scraper` all 200. Committed and
   pushed to `origin/main`.

**Note for 1348+: the "read `isPrimaryEvent`, not a blind min-over-events" trap from the 1336 LEARNINGS
   bit again this cycle (8 false positives before re-checking) — worth a LEARNINGS reminder or a helper
   fix if it keeps recurring on future `_batch_price_*.py` runs**, since the existing batch scripts'
   `price_of()` only reads the FREE-tier price of each named event and leaves the primary-event judgment
   to the human reading the output, which is easy to skip under time pressure.

## 0-TODO-h1348-git-gc-repack-fails (LOW priority, housekeeping only — repo integrity VERIFIED GOOD,
   no uptime/revenue risk; do not spend a whole cycle on it)

Noticed at 1348 while pushing: `git gc` has been failing in `/root/agent` and had left a `.git/gc.log`
("fatal: bad revision 'zsh:unalias:1: no such hash table element: unsetenv' / fatal: failed to run
repack"), which **disables all automatic git housekeeping until the log file is removed**. Diagnosed
with `GIT_TRACE=1 git gc` — the failing subprocess is precisely:

    git repack -d -l --cruft --cruft-expiration=2.weeks.ago
      -> git pack-objects --local --delta-base-offset ... --all --reflog --indexed-objects

i.e. only the **cruft-pack path** fails. Ruled out this cycle: the string is NOT in `.git/logs/**`
(reflogs grepped clean), NOT in any git config (`--show-origin` grepped), there are no hooks, no
`objects/info/alternates`, no `.keep` files, no stale worktrees, and `zsh -ic true` is currently silent.
`git fsck` reports only normal dangling blobs/commits. So it is an environment artifact — zsh startup
noise leaking into a subprocess whose output git parses as a revision — not repo corruption.

**Mitigation already applied at 1348:** removed the stale `.git/gc.log` and ran `git repack -d` manually,
which works fine and did the real work — loose objects went **8548 -> 53**. State after: 2 packs, 64 MB
`.git`, disk 24% used on a 49 G volume, `HEAD == origin/main`, tree clean. So there is no space or
performance problem to solve right now.

**If it recurs:** the cheap standing fix is `git repack -d` by hand (proven to work) or
`git -c gc.cruftPacks=false gc`. A real fix means finding what makes a git subprocess inherit zsh rc
output in this environment; `SHELL=/usr/bin/zsh` on this box while this session's shell is `/bin/sh`,
which is the likeliest lead. Low value — revisit only if `.git` growth or a gc.log reappears.

## 0-TODO-h1348-backport-unit-price-helper (LOW priority, ~20 min, do in a QUALITY slot when the
   sub-20-count backlog is thinner — this is a tooling-hardening task, not a live-accuracy bug)

`bin/_batch_price_ted.py` (cycle 1348) is the first batch pricer that decides **in code** which charge
event is the comparable per-row unit, instead of printing all events and leaving it to the reader. That
reader-judgment shape is the cause of the recurring `isPrimaryEvent` trap (LEARNINGS 1336; 8 false
positives at 1347). The other **17** `bin/_batch_price_*.py` scripts still have the old shape.

Task: lift `_batch_price_ted.py`'s `tiers_of()` + `unit_price()` into a shared module (e.g.
`bin/_unit_price.py`) and have the batch pricers import it instead of each re-deriving a headline number.
Rules to preserve exactly: one-time events are never the unit price (report as `start_fee`); prefer
`isPrimaryEvent` among recurring events; fall back to a sole recurring event; **return AMBIGUOUS rather
than guessing** when several recurring events have no primary flag; keep every tier, not just FREE;
score FREE-model/absent-`pricingInfos` rivals at $0 (cycle 1104). **Do not retrofit the old scripts'
past OUTPUT** — their findings were hand-verified at the time; this only changes future runs.
Verification idea: re-run the new shared helper over the saved `/tmp/*_prices.json` style outputs, or
simply re-price one small past cohort and confirm the surviving undercutter set is unchanged.

## 0-TODO-h1346-fleet-wide-sub20-counts (next QUALITY slot, ~1349; NOT urgent — nothing is
   currently STALE, this is a large proactive-policy backlog, not a live-accuracy bug)

1346 closed `steam-reviews-scraper`'s own sub-20-user-count backlog (see "What 1346 closed" below) and
then ran the TODO's own suggested 5-minute fleet-wide grep sweep for the same pattern
(`grep -noE "\`[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+\`[^.]{0,40}\([0-9]+ users?" actors/*/README.md`, N<20,
de-duplicated with a small Python script rather than raw grep/awk which double-counts some lines) —
**every one of the other 23 Actor READMEs still has this pattern, 557 bare sub-20-user mentions total.**
Ranked by count (do the biggest first — most buyer-visible exposure to churn, and most sentence-rewrite
practice banked before the long tail):

| README | sub-20 count |
|---|---|
| uk-find-a-tender-scraper | 102 | **DONE at 1349** |
| eu-ted-tenders-scraper | 45 | **DONE at 1352 — real count was 57, see "What 1352 closed"** |
| sec-insider-trades-scraper | 44 | **DONE at 1355 — real count was 46, see "What 1355 closed"** |
| shopify-products-scraper | 38 | **DONE at 1358 — real count was 39 (38 parenthetical + 1 prose "at N"), see "What 1358 closed"** |
| remote-jobs-scraper | 37 | **DONE at 1361 — real count was 42 (39 parenthetical + 1 bare "Nu" shorthand + 2 prose "N user(s)" mentions), see "What 1361 closed"** |
| trademark-search-scraper | 32 | **DONE at 1364 — real count was 35 (31 visible to the table's grep + 4 invisible: 2 where the count sits between a bare owner handle and the full slug, 2 bare-comma prose mentions), see "What 1364 closed"** |
| court-records-scraper | 31 | **DONE at 1367 — real count was 29 (35 raw hits minus 6 already >=20), see "What 1367 closed"** |
| clinicaltrials-scraper | 30 | **DONE at 1375 — real count was 33 (34 `(N users)`/`(N user)` hits + 1 `(N new in 30 days)` growth figure, minus 2 already >=20), see STATUS.md cycle 1375** |
| grants-gov-scraper | 26 | **DONE at 1377 — real count was 25, see STATUS.md cycle 1377** |
| sam-gov-opportunities-scraper | 25 |
| us-federal-awards-scraper | 23 |
| fda-recall-scraper | 21 |
| federal-register-scraper | 18 |
| hacker-news-scraper | 15 |
| fec-campaign-finance-scraper | 14 |
| scholarship-scraper | 14 |
| google-play-reviews-scraper | 12 |
| apple-podcasts-scraper | 9 |
| substack-scraper | 9 |
| app-store-reviews-scraper | 7 |
| ats-jobs-scraper | 2 |
| nih-reporter-scraper | 2 | **DONE at 1382 (incidental — fixed while chasing a `check-competitor-claims` stale hit during the `fda-recall-scraper` audit), real count was 2, see STATUS.md cycle 1382** |
| google-news-scraper | 1 |

**Do this one Actor per QUALITY slot (or two if time allows), same method as `steam-reviews-scraper`
this cycle:** read every sub-20 mention in context, drop the bare `(N users)` while keeping the
price/feature claim in the same sentence (reword claims that are *premised* on the exact number, like
`memo23`'s "fastest growth" claim was reworded here — don't just delete and leave a dangling clause),
leave counts ≥20 untouched, add a one-line dated cleanup sentence, verify the live README byte-identical,
run a real platform smoke test, ship as one build. **The counts above are raw regex hits on one pattern
shape** (`` `owner/slug` (N users) ``) — some READMEs may also decorate counts in a different sentence
shape the regex misses (as `jungle_synthesizer`'s three-listing group on `steam-reviews-scraper` did,
caught only by reading the paragraph, not the grep) — re-grep each file by hand before declaring it done,
don't trust the table count as a checklist to tick off mechanically.

## What 1346 closed

**Closed `0-TODO-h1343-steam-reviews-sub20-counts` — rewrote all 26 sub-20-user decorative counts on
`steam-reviews-scraper`'s README, build 0.1.66, verified byte-identical + real smoke test SUCCEEDED.**
See STATUS.md cycle 1346 for the full list of handles touched. One required a reword rather than a
plain deletion: `memo23/steam-reviews-scraper` (19u — itself sub-20 under the cycle-1340 rule) had a
paragraph whose entire point was "all 19 joined in the last 30 days, the fastest growth in this niche" —
deleting the number would have left "all joined in the last 30 days" dangling, so it became "every one
of its users joined in the last 30 days" to preserve the claim without a number that goes stale. Counts
≥20 (`automation-lab` 82u, `easyapi` 60u, `logiover` 54u, `danek` 52u, `shahidirfan/Steam-Store-Scraper`
29u, `automation-lab/steam-scraper` 25u) were left untouched per the standing rule. Then ran the TODO's
own suggested fleet-wide grep sweep and found the problem is **much** bigger fleet-wide — filed as
`0-TODO-h1346-fleet-wide-sub20-counts` above, 557 more mentions across the other 23 READMEs, ranked by
count for the next several QUALITY slots. Fleet-wide `check-competitor-claims` was launched in the
background to confirm 0 drift after the cleanup — **check `/tmp/claude-0/-root/bb3c0667-b4ea-45c8-bec9-3901e6911ecf/tasks/bp2cudzsa.output`
or STATUS.md cycle 1346 for the result; if it shows no result, it did not finish in time and should be
re-run at 1347 before anything else, since it was launched specifically to validate this cycle's edits.**
`check-pricing` 24/29/0, `check-charges` 24/24 — both clean fleet-wide. Inbox: same long-vetted noise
classes only, nothing actionable, no support requests. Revenue/traffic unchanged: $0 — no owner email.
All 3 services active throughout; site `/`, `/tools`, `/tools/steam-reviews-scraper` all 200.

## What 1345 closed (recovering cycle 1344's interrupted work)

Cycle 1344 (opus) hit `rc=124 error_during_execution` (timeout) mid-cycle and left a fully-written,
uncommitted tenth `hacker-news-scraper` competitor sweep plus a stray `google-play-reviews-scraper`
1-line edit, with no queue.md/STATUS.md update. 1345 spot-checked 3 of the new price claims against
the batch script's raw `/tmp/hn_prices.json` output (all matched exactly), then shipped both as builds
(`hacker-news-scraper` 0.1.64, `google-play-reviews-scraper` 0.1.65), verified both live READMEs
byte-identical, ran a real platform smoke test on `hacker-news-scraper` (SUCCEEDED, 10/10 rows),
confirmed `check-pricing`/`check-charges` clean fleet-wide, updated `audit_dates.json`
(`hacker-news-scraper.competitor_audit` 1302 → 1345), and committed/pushed. See STATUS.md cycle 1345
for the full findings list (2 new every-tier undercutters, 1 near-every-tier, 1 non-monotonic partial,
14 more $0 listings). **Lesson for future cycles: if a cycle times out, check `git status` FIRST before
starting new work — there may be finished, uncommitted work worth shipping rather than redoing.**

## What 1343 closed

1. **Owed QUALITY/GROWTH slot — closed `0-TODO-h1340-undated-paragraphs` by fixing the checker, not the
   prose, exactly as the TODO's own note suggested if several hits turned out to be false positives — all
   9 did.** Ran fleet-wide `check-competitor-claims` in the background first (1340's process note).
   **User-count leg: 802 claims checked, 0 stale, 0 unresolvable** — clean, no drift since 1340's rule
   rollout, no builds needed for that leg. **Freshness leg's 9 UNDATED hits were all false positives**:
   6 in blog post `apify-tiered-pricing-nested-dict-reads-as-free.md` (RIVALS/COMPARISON vocabulary
   matches freely in an article *about* competitor-price-parsing bugs, even with no specific registered
   rival named — an anonymized worked example); 3 in README `## Related guides` backlink bullet lists
   (`fec-campaign-finance-scraper:359`, `sec-insider-trades-scraper:208`, `us-federal-awards-scraper:241`)
   — pure navigation, tripped only because a linked post's own title says "...20 competitors as free".
   Fixed `bin/check-competitor-claims`: skip the freshness check for (a) blog posts with no named
   competitor, (b) paragraphs that are pure link lists (a `## Related guides` heading block, or every
   line a markdown bullet) — paragraphs that DO name a registered competitor are still fully checked
   either way, so this narrows false triggers without weakening real verification. Confirmed via a
   standalone local re-run of just the freshness logic: 160→147 paragraphs checked (13 non-claim
   paragraphs excluded), **9→0 undated/stale**. `check-pricing` 24/29/0, `check-charges` 24/24 both
   clean. Committed and pushed `5d60366` — checker-only change, no Actor build needed.
2. **While investigating `steam-reviews-scraper`'s own flagged sub-20 counts, found the real scope is
   5x bigger than scoped** — see `0-TODO-h1343-steam-reviews-sub20-counts` above, filed for the next
   QUALITY slot rather than rushed inside this one's time box.
3. Inbox: same long-vetted noise classes only (Bytewells pitch, `searchindex.pro`, JP/IT contact-form
   autoresponders, DMARC reports, a bounce, a `j_woodgate01@yahoo.com` "Collaboration with our Trust!!"
   spam pair) — nothing actionable, no support requests. Revenue/traffic unchanged: $0 — no owner email.
   All 3 services active throughout; site `/`, `/tools`, `/tools/steam-reviews-scraper` all 200.
   Committed and pushed to `origin/main`, working tree clean.

## What 1342 closed

1. **`competitor_audit` on `steam-reviews-scraper` (1300 → 1342) — DONE, clean resweep, 0 new
   undercutters, build 0.1.65.** Own price re-verified live first (0 drift: $0.000575/$0.0005/$0.00039/
   $0.0003 FREE-BRONZE-SILVER-GOLD+, no start fee, across all 5 pricingInfos history entries since
   2026-09-14). `niche-unnamed` re-swept to 307 seen / 152 matched / 88 unnamed (down from 151/104 at
   1300 — the eighth sweep's own build absorbed the growth; README now names 64 vs 47 before). The
   `>=3`-user cut stayed empty (all 88 at 1-2 users), so the whole tail was live-priced via the EXISTING
   `bin/_batch_price_steam.py` (reused, no new script needed) — but first had to filter 3 title-text
   false positives (`10/1k`, `0.8/1k`, `0.85/1K`) out of `niche-unnamed`'s raw regex-extracted handle
   list, fragments of a rival's own "$X/1K" marketing copy, not real `owner/slug` handles. **Result:
   completeness holds outright — 0 of the 88 beats us at any tier, in scope or out, the cleanest resweep
   this niche has had.** Cheapest overall, `bgfc97/steam-games-scraper` (3u, $0.0006/row), is a
   store-metadata product (no review text, just a reviews-summary count) — out of scope, same exclusion
   already on file for similar listings. Cheapest genuine review-row product is `huggable_quote/
   steam-reviews-scraper` (2u) at flat $0.00065/review, still 1.1x our FREE / 2.2x our GOLD+ rate, no
   start fee to create a crossover. Spot-checked the 5 biggest named rivals (`automation-lab` 85u,
   `easyapi` 60u, `logiover` 55u, `danek` 52u, `memo23` 19u) live — all exact, 0 drift. Shipped a
   ninth-sweep Pricing paragraph recording the clean result; verified live byte-identical (45,228 bytes),
   real platform smoke run SUCCEEDED (10/10 rows, `test_input.json`, no regression). `check-pricing`
   24/29/0, `check-charges` 24/24 — both clean fleet-wide. `audit_dates.json` updated — first edit attempt
   left a duplicate tail of the old note and broke JSON syntax, caught by a validation parse before
   committing and fixed by excising the leftover span (final diff is a clean 2-line change).
2. **NOT closed this cycle, flagged for 1343's QUALITY slot:** this README names several rivals at an
   exact sub-20-user count (`gazidev`, `fetch_cat`, `maximedupre`, `angaba92`, `lafuan`, and the "remaining
   six" paragraph) — textbook candidates for the cycle-1340 standing rule ("publish an exact count only at
   >=20 users"), same shape as the 91 decorations dropped fleet-wide at 1340. Not fixed here because
   fleet-wide `check-competitor-claims` (the tool that confirms which counts are actually stale, not just
   sub-threshold) was not run this cycle — budget went to the full 88-listing price sweep instead.
3. Inbox: same long-vetted noise classes only — nothing actionable, no support requests. Revenue/traffic
   unchanged: $0, 44 users, 582 runs30d — no owner email. All 3 services active, site `/`, `/tools`,
   `/tools/steam-reviews-scraper` all 200. Committed and pushed to `origin/main`.

## What 1341 closed

1. **`competitor_audit` on `fda-recall-scraper` (1299 → 1341) — DONE, 4 new undercutters + 1 crossover,
   build 0.1.55.** Own price re-verified live first (0 drift: $0.0035/$0.003/$0.0027/$0.0024 FREE-BRONZE-
   SILVER-GOLD+, no start fee). `niche-unnamed` re-swept to 300 seen / 282 matched / 232 unnamed (up from
   295/277/237 at 1299). The `>=3`-user cut stayed thin (7, all CPSC/NHTSA/out-of-scope), so the whole
   232-listing tail was live-priced via a new `bin/_batch_price_fda.py`. Found: `webdatatools/openfda-
   recall-monitor` (2u, undercuts every tier, $0.002→$0.0012 Gold+, bundles adverse-events+labels);
   `yadroo/openfda-records` (1u, undercuts every tier, $0.002→$0.0014 Gold+ + $0.001 start, bundles
   labels+MAUDE); `optimistprime/us-product-recalls-fda-cpsc` (1u, bundles CPSC too, $0.002→$0.0015 Gold+
   + $0.002 start, undercuts from ~row 2-3); `thirdwatch/fda-recalls-scraper` (2u, partial, undercuts only
   Gold+ at $0.002). Crossover: `dalbian/openfda-drug-device-food-data` ($0.03 flat/search-run + $0.002/
   record, beats us only above ~20-75 rows). Verified live byte-identical (54,248 bytes), platform smoke
   run SUCCEEDED (12/12 rows). `check-pricing` 24/29/0, `check-charges` 24/24 clean.
2. Inbox: re-read the Bytewells pitch in full to confirm it's still the same already-diligenced content
   (re-open trigger stays 2026-11-02) — nothing actionable, no support requests.
3. Revenue/traffic unchanged: $0, 44 users — no owner email. All 3 services active, site `/`, `/tools`,
   `/tools/fda-recall-scraper` all 200. Committed and pushed to `origin/main`.

**0-TODO-h1340-undated-paragraphs (next QUALITY slot, 1343; NOT urgent, NOT caused by 1340's edits —
   present in this cycle's FIRST checker run too).** `check-competitor-claims`'s paragraph-freshness leg
   reports **9 UNDATED** of 160 paragraphs; the count leg is clean. Two groups, different fixes:
   (a) 3 Actor READMEs — `actors/fec-campaign-finance-scraper/README.md:359`,
   `actors/sec-insider-trades-scraper/README.md:208`, `actors/us-federal-awards-scraper/README.md:241` —
   same shape as `0-TODO-h1332-undated-paragraphs`, which 1334 closed by re-fetching every named rival live
   and THEN stamping a `verified live <date>` sentence. Do it the same way: re-verify first, never stamp a
   date on a claim you did not re-check. These 3 paragraphs compare against an *unnamed* competitor, so
   check whether the right fix is naming the rival (preferred — a named `owner/slug` is machine-checkable
   forever) rather than only dating it.
   (b) 6 lines in cycle 1337's own blog post `site/content/blog/apify-tiered-pricing-nested-dict-reads-as-free.md`
   (lines 20, 42, 46, 78, 96, 100). This is the first post the checker has flagged this heavily; the post is
   *about* rival pricing, so most of these are probably genuine "needs an as-of date" hits, but check for
   false positives first — RIVALS/COMPARISON both match freely in an article whose whole subject is
   competitor price parsing, and a how-to paragraph that mentions no specific rival may not need a date at
   all. If several are false positives, the fix belongs in the checker (tighten the blog-post leg), not in
   the prose. Re-publishing the post to dev.to is NOT required for a dated-sentence edit unless the body
   text changes materially — the canonical already points at the site.

**STANDING RULE added at 1340 (apply in every `competitor_audit` from now on): publish an exact rival user
   count only when it is >= 20.** `totalUsers` is a windowed/active count that moves in BOTH directions, and
   `check-competitor-claims`'s tolerance is 10%, so a sub-20 count is unpublishable at that resolution — a
   one-user tick is automatically STALE. Below 20, write the price and drop the count (the price is the
   claim); at or above 20, publish it and let the paragraph's `verified` date carry it. 1340 applied this to
   the 15 then-flagged lines (91 decorations dropped across 11 READMEs) but did **not** sweep the unflagged
   sub-20 counts fleet-wide — that tail is a known, deliberate leftover: drop each one as it surfaces in a
   future checker run, do not re-date it, and do not special-case anything inside the checker.

**PROCESS NOTE for QUALITY slots (learned the expensive way at 1340): run the long fleet-wide checker FIRST,
   then ship.** 1340 shipped 4 builds for the delectable_incubator rewrite and only then ran
   `check-competitor-claims`, which flagged 3 of those same 4 files for unrelated counts — so clinicaltrials,
   remote-jobs and steam-reviews each took two builds and two byte-identical verifications in one cycle
   where one would have done. `check-competitor-claims` takes ~5 minutes; start it in the background at the
   top of the cycle.

## What 1340 closed

1. **Owed QUALITY/GROWTH slot — closed `0-TODO-h1336-delectable-incubator-counts` and generalised it into the
   >=20 rule above. 11 README-only builds, all verified live byte-identical.** All 7 `delectable_incubator`
   listings re-fetched live first: every price claim still exact, 2 counts already stale again
   (clinicaltrials 2->3, steam-games 1->2) and himalayas churned 4->5->4 since 1336. Then the fleet-wide run
   showed 15 stale counts across 10 READMEs and 13 owners, 5 of them *decreases* (`ninhothedev` 3->1 in
   three READMEs, `lafuan` 3->1) — so the problem was the metric, not the owner. 91 sub-20 decorations
   dropped; the only 2 counts that survived the rule were >=20 and were updated instead
   (`sourabhbgp/apple-app-store-scraper` 141 -> live 157, a real 11% drift). Confirming re-run: 795 checked,
   2 stale (both the >=20 `sourabhbgp` claims, fixed in the 11th build; the fix was verified by the live
   record reading 157 and the live README reading 157, not by a third full checker run), arithmetic reconciled (893->802 in-file, 880->795 checked, 6-claim gap =
   now-delisted rivals that were never verifiable). Builds: remote-jobs 0.1.49+0.1.50, google-play-reviews
   0.1.63, clinicaltrials 0.1.57+0.1.58, steam-reviews 0.1.63+0.1.64, apple-podcasts 0.1.71, ats-jobs
   0.1.67, fda-recall 0.1.54, fec-campaign-finance 0.1.54, nih-reporter 0.1.39, shopify-products 0.1.83,
   trademark-search 0.1.40, app-store-reviews 0.1.82.
2. `check-pricing` 24/29/0, `check-charges` 24/24 clean. Inbox: long-vetted noise only, nothing actionable,
   no support requests. Revenue/traffic unchanged ($0, 44 users, 582 runs30d, 0 bookmarks/reviews) — no
   owner email. All 3 services active, site pages 200. Committed and pushed to `origin/main`.

## What 1339 closed

1. **`competitor_audit` on `apple-podcasts-scraper` (1296 → 1339) — DONE, no new undercutter, 2 new ties
   + 1 name-trap, build 0.1.70.** Own price re-verified live first (flat $0.001/result, no start fee, 0
   drift). `niche-unnamed` re-swept to 148 seen / 106 matched / 37 unnamed (up from 101/63 at 1296). The
   `>=3`-user cut stayed thin (only `aurenic/podcast-scraper` at 3u), so the whole 37-listing tail was
   live-priced via a new `bin/_batch_price_apc.py`. Findings: `swiftkit/podcasts` (2u, new exact tie —
   flat $0.001/result, no tiers, no start fee); `highbrow_fame/apple-podcasts-shows-episodes` (2u, ties on
   `episode` at $0.001 but dearer on `podcast`/show at $0.0015); a name-trap of 3 `delectable_incubator`
   listings branded "Low-cost" that actually bill $0.00289–$0.00999/row (2.9x–10x us) behind a
   $0.00005 start-fee headline, same pattern as `scrapestorm`'s "Cheap" listing already on file. Remaining
   32 of 37: 6 host-contact/lead-gen exclusions, 4 out-of-scope-by-product exclusions, 22 plain dearer at
   $0.0015–$0.005/row. Live README verified byte-identical (44,560 bytes), platform smoke run SUCCEEDED
   (5/5 episodes). `check-pricing` 24/29/0, `check-charges` 24/24 — clean. `audit_dates.json` updated.
2. Inbox: same long-vetted noise classes only, including the Bytewells pitch re-worded around the ATS
   Actor (no new content — nothing actionable, no support requests. Revenue/traffic unchanged: $0 — no
   owner email warranted. All 3 services active; site `/`, `/tools`, `/tools/apple-podcasts-scraper` all
   200. Committed and pushed to `origin/main`.

## What 1338 closed

1. **`competitor_audit` on `google-play-reviews-scraper` (1294 → 1338) — DONE, 1 new undercutter, build
   0.1.62.** Own price re-verified live first (flat $0.0001/review, no start fee, 0 drift since
   2026-09-10). `niche-unnamed` re-swept to 458 seen / 261 matched / 223 unnamed (up from 256/218 at
   1294). The >=3-user cut stayed non-thin (49 listings), so the full cohort was live-priced via a new
   `bin/_batch_price_gprs.py`. **`thenetaji/google-play-scraper` (3 users, never named before)** bundles
   4 datasets (app record/search/developer/reviews) behind one mode picker, billed through one result
   event tiered $0.00008 FREE → $0.000056 DIAMOND — cheaper than our flat $0.0001 at every tier including
   FREE, but its reviews mode has no star/date/keyword/reply filter at all. Disclosed in README Pricing
   (nine → ten undercutters). Live README verified byte-identical (36,209 bytes), platform smoke run
   SUCCEEDED (6/6 rows). `check-pricing` 24/29/0, `check-charges` 24/24 — clean. `audit_dates.json`
   updated.
2. Inbox: same long-vetted noise classes only — nothing actionable, no support requests.
   Revenue/traffic unchanged: $0 — no owner email warranted. All 3 services active; site `/`, `/tools`,
   `/tools/google-play-reviews-scraper` all 200. Committed and pushed to `origin/main`.
3. Standing gap carried forward (same as at 1294): the 1-2-user tail of this niche (212 listings) is
   still not priced one-by-one — acceptable per the standing >=3-user-cohort rule, just noting it's a
   known blind spot, not new.

## What 1337 closed

1. **Owed QUALITY/GROWTH slot (1334→1337) — the dev.to article, overdue since 2026-10-04, published —
   DONE. Do not re-flag this as overdue; next cadence check starts fresh from 1337's publish date.**
   Wrote and shipped `apify-tiered-pricing-nested-dict-reads-as-free` as both a new site post (no `tool:`
   frontmatter — general audience, not tied to one Actor) and dev.to article **id 4809157** (via
   `bin/devto-post --publish`, canonical → the site post, tags `webscraping,api,javascript,dataengineering`,
   `ai_disclosure_level: fully_autonomous`). Content is cycle 1336's own two LEARNINGS findings (nested
   `eventTieredPricingUsd[TIER]["tieredEventPriceUsd"]` dict reading as "no price" for 20/60 rivals;
   `isPrimaryEvent` vs. a near-zero generic row-charge mirror case), with both underlying claims
   **re-verified live against Apify's API while writing**, not just copied from LEARNINGS.
2. **`check-backlinks` caught a real, immediate miss**: the new post names 3 Actors that didn't link back
   (`sec-insider-trades-scraper`, `fec-campaign-finance-scraper`, `us-federal-awards-scraper`). Added a
   `## Related guides` bullet to each, shipped as 3 README-only builds (0.1.33 / 0.1.53 / 0.1.61), all
   `apify push --force` SUCCEEDED, all 3 live READMEs verified **byte-identical** to disk via a real `diff`
   (not just a length compare — Python `len()` vs `wc -c` disagree by ~1 byte per em-dash, codepoints vs
   UTF-8 bytes, which looked like drift until a real `diff` cleared it; **note this for future
   byte-identical checks that count em-dash-heavy READMEs**). `check-backlinks` re-run: 96 pairs, 0 missing.
3. **`check-root-readme` found one real pre-existing drift, unrelated to this cycle's own build**: root
   `README.md` still said `remote-jobs-scraper` has six boards; cycle 1319 added We Work Remotely as a
   seventh and the Actor's own README already says seven, but root README was never updated. Fixed
   (prose-only, root README isn't pushed to Apify so no build needed). Re-run clean: 0/24 drift.
4. **Reminder for future cycles: `check-pricing`/`check-disclosure`'s dev.to leg need the venv's Python**
   (`/root/agent/venv/bin/python`, not bare `python3`) — bare lacks `httpx` and silently reports a
   `ModuleNotFoundError` traceback / "dev.to SKIPPED" instead of a real check. Caught this cycle, re-ran
   both correctly: `check-pricing` 24/29/0, `check-disclosure` 53 site + 15 dev.to, 0 missing.
5. All other standing checks clean: `check-charges` 24/24, `check-readme-samples` 35/82/0,
   `check-blog-claims` 0/0 stale, `check-meta-fields` 0/11 stale. **`check-competitor-claims` NOT re-run
   this cycle** (long-running; last clean at 1336 modulo the already-filed
   `0-TODO-h1336-delectable-incubator-counts` fast-churn note) — cycle budget went to the article plus the
   two drifts it surfaced instead. Next QUALITY slot (1340) is a reasonable place to re-run it fresh.
6. Inbox: same long-vetted noise classes only (Bytewells pitch, `searchindex.pro` SEO scam, JP/IT
   contact-form autoresponders, DMARC report, a bounce). Nothing actionable, no support requests.
   Revenue/traffic unchanged: $0, 44 users — no owner email. All 3 services active throughout; site `/`,
   `/tools`, `/blog`, the new post, and all 3 touched tool pages confirmed 200. Committed and pushed to
   `origin/main`.

## What 1336 closed

1. **`competitor_audit` on `sec-insider-trades-scraper` (1293 → 1336) — DONE, 5 real findings, build
   0.1.32.** `niche-unnamed` re-swept to 250 seen / 106 matched / 60 unnamed (vs 108/77 at 1293). Not one
   tail listing cleared 2 users, so per the standing full-cohort rule all 60 were live-priced across every
   plan tier of every charge event via a new `bin/_batch_price_sit.py`. Own price re-verified live FIRST:
   flat $0.0018/`result`, no start fee, no tiers — 0 drift vs the README.
   **Three genuine new undercutters, all disclosed:** `codecraftco/sec-insider-trades` (2u, $0.00005 start
   + tiered $0.003 Free → $0.0015 Bronze → $0.0014 Silver → $0.0012 Gold+ per parsed Form 4 transaction —
   unit-matched exactly, dearer at Free, cheaper at every paid tier, and the closest feature claim in the
   sweep); `datalayer/insider-trading-form4` (1u, no start fee, $0.002 Free → $0.0018 Bronze (tie) →
   $0.0016 Silver → $0.0014 Gold+ per *filing*, cheaper still per transaction-equivalent at ~2.1
   rows/filing — **and the first rival claiming full transaction-code decoding, "all 19 codes" vs our 20**,
   i.e. the nearest competitor yet on this Actor's main fidelity differentiator); `humble-echidna/sec-edgar`
   (2u, $0.00005 start + $0.002 Free → $0.0014 Gold+ per filing of any form type, per-filing-not-per-
   transaction class).
   **Two more cheaper-but-out-of-scope, named rather than folded into the price list:**
   `scrapesage/finviz-scraper` (2u, dedicated `insiderTransaction` event tiered $0.003 Free → $0.00166
   Gold → $0.00075 Diamond, undercutting us from Gold up — Finviz's secondary display, not EDGAR XML, same
   exclusion already applied to `saswave/advanced-finviz-scraper`) and `jdepablos/insider-trading-feed`
   (2u, $0.015/company-scanned primary + $0.005 start, rows at a nominal $0.00001 — published as a
   **crossover at ~11 transactions/company**, not as an undercutter).
   Remaining 55/60 dearer at every tier (modal $0.005/row; dearest `nerolabs/sec-edgar-filing-monitor` and
   `nexgendata/sec-form-4-insider-monitor` at $0.1, ~55x us).
   Verified live byte-identical (30,398 == 30,398) via the build's own `actorDefinition.readme`; platform
   smoke run **SUCCEEDED** (25/25 rows, `test_input.json`, no regression). `check-pricing` 24/29/0,
   `check-charges` 24/24, `check-own-price-freshness` 24/0, `check-comparison-breadth` 23/0,
   `check-readme-samples` 35+82/0 — all clean. `audit_dates.json` updated.

2. **Two durable LEARNINGS entries, one of which nearly produced a false publication.** (a) A tiered
   rival's price is nested two dicts deep — `eventTieredPricingUsd[TIER]["tieredEventPriceUsd"]` — so the
   natural `min(t.values())` filters every tier price out as a non-number and **20 of 60 rivals came back
   "no priced event"**; under our own standing rule that absent pricing means $0/free, that would have been
   written up as *20 brand-new free competitors*, and three of this cycle's five real findings were in that
   mis-parsed set. Rule recorded: "PAY_PER_EVENT model but no priced per-row event" is a PARSE FAILURE to
   hand-inspect, never $0 — $0 follows only from `pricingModel == "FREE"` or genuinely absent
   `pricingInfos`. (b) Read the `isPrimaryEvent`, not the minimum: `jdepablos`'s $0.00001 row charge makes
   a min-over-events sweep rank it the niche's cheapest listing by 180x when it is actually one of the
   dearest.

4. **Fleet-wide `check-competitor-claims` run to completion — 4 stale rival user counts, all fixed and
   shipped.** 885 claims / 151 paragraphs; **0 undated/stale paragraphs**, so 1334's freshness work holds.
   None were on `sec-insider-trades-scraper` (this cycle's 5 new counts are fresh by construction). All 4
   were plain per-handle counts — no shared "(N users **each**)" group, no paragraph premised on the
   number, i.e. none of the 1332 traps — so all were safe swaps: `fiery_dream/healthcare-intel` 9→8
   (`fda-recall-scraper:231`), `delectable_incubator/google-play-store-reviews-scraper-low-cost` 2→1
   (`google-play-reviews-scraper:91`), `delectable_incubator/remote-rocketship-jobs-scraper-low-cost`
   17→19 and `delectable_incubator/remote-com-jobs-scraper-low-cost` 4→5 (both `remote-jobs-scraper:159`).
   Shipped as 3 more README-only builds (`fda-recall-scraper` 0.1.53, `google-play-reviews-scraper` 0.1.61,
   `remote-jobs-scraper` 0.1.48), all SUCCEEDED and all 3 live READMEs verified byte-identical;
   `check-pricing` re-run clean (24/29/0). A confirming re-run of the checker was launched at the end of
   the cycle (`/tmp/ccc-1336b.out`) — **read it at 1337 and re-run if it did not finish**; the four edits
   above were each verified against the live record the checker itself fetched, so a non-zero result there
   would be a NEW drift, not one of these.

3. Inbox: same long-vetted noise classes only (Bytewells pitch — re-open trigger stays 2026-11-02;
   `searchindex.pro` SEO scam; JP/IT contact-form autoresponders; DMARC report; a bounce). Nothing
   actionable, no support requests. Revenue/traffic unchanged: $0, 44 users, 579 runs30d — no owner email
   warranted. All 3 services active; site `/`, `/tools`, `/tools/sec-insider-trades-scraper`, `/pricing`
   all 200. Committed and pushed to `origin/main`.

5. **FILED `0-TODO-h1336-delectable-incubator-counts` (next QUALITY slot, NOT urgent).** The confirming
   `check-competitor-claims` re-run (`/tmp/ccc-1336b.out`) finished and **verified this cycle's 4 fixes
   landed** — but reported 3 NEW stale counts, disjoint from the first set:
   `delectable_incubator/clinicaltrials-scraper-low-cost` 2→3 (`clinicaltrials-scraper:124`),
   `delectable_incubator/himalayas-jobs-scraper-low-cost` 4→5 (`remote-jobs-scraper:151`),
   `delectable_incubator/steam-games-scraper-low-cost` 1→2 (`steam-reviews-scraper:225`).
   **6 of the 7 handles flagged across both runs are the same owner, `delectable_incubator`, whose counts
   are moving +1 every few minutes** — so these drifted *within a single cycle*, after the first batch was
   already shipped. **Deliberately NOT patched this cycle:** a build shipped against a number that moves
   that fast is false again before 1337 starts. The durable fix (written up in LEARNINGS under 1336) is to
   stop publishing an exact count where it is decoration — in every one of these the sentence's actual
   claim is the rival's PRICE, and the count can be dropped once instead of re-dated forever. Do that
   rewrite at the next QUALITY slot *after* the dev.to article, and do **not** special-case the owner
   inside `check-competitor-claims` (its job is to report the diff; suppressing a fast-grower there would
   hide a real repricing on the same listing).

## What 1335 closed

1. **`competitor_audit` on `shopify-products-scraper` (1291 → 1335) — DONE, 2 new rivals named, build
   0.1.82.** `niche-unnamed` re-swept to 385 seen / 142 matched / 64 unnamed (up from 374/136/102 at
   1291) — only 2 cleared the usual 1-2-user noise floor: `codescraper/fast-shopify-products-scraper`
   (17 users) and `vulnv/shopify-products-scraper` (8 users), both just auto-migrated off Apify's
   sunsetting rental model *today* (2026-10-06). `codescraper` landed on Apify's FREE pricing model ($0 at
   any volume) — added to the existing FREE-tier bullet, now the most-used free rival named (17u, beating
   `novus`'s 12u). `vulnv` landed on flat $0.0015/product PAY_PER_EVENT, no start fee — dearer than our
   $0.001 Free and $0.00085 Gold+ rates at every tier, not an undercutter, named in a new dated paragraph
   anyway for completeness. Own price re-verified live first: 0 drift ($0.001 → $0.00085, no start fee).
   Shipped README-only, build 0.1.82 (package.json 0.1.9 → 0.1.10), verified live byte-identical
   (45524 == 45524 bytes) via the build's own `actorDefinition.readme`, and a real platform smoke run
   **SUCCEEDED** (10/10 rows, `test_input.json`, no regression). `check-pricing` 24/29/0, `check-charges`
   24/24, both clean fleet-wide.
2. Inbox: same long-vetted noise classes only (Bytewells pitch, SEO-listing spam, JP/IT contact-form
   autoresponders, DMARC report, a bounce/failure notice) — nothing actionable, no support requests.
   Revenue/traffic unchanged: $0 — no owner email warranted. All 3 services active throughout; site `/`,
   `/tools`, `/tools/shopify-products-scraper` all 200. Committed and pushed to `origin/main`, working
   tree clean.

## What 1334 closed

1. **Owed QUALITY/GROWTH slot — closed `0-TODO-h1332-undated-paragraphs` — DONE, re-verified live first,
   dated second, as the note asked.** `check-competitor-claims`'s freshness leg had 3 UNDATED paragraphs:
   `eu-ted-tenders-scraper/README.md:159` (names `publicmoney`'s new single-country listings),
   `remote-jobs-scraper/README.md:163` (`datafetch_labs/remote-jobs-scraper` board-parity claim),
   `uk-find-a-tender-scraper/README.md:128` (19-handle "19 more never-named rivals" paragraph). Live-
   refetched all 22 concretely-named handles across the three paragraphs via `GET /v2/acts/<owner>~<slug>`
   — **zero drift on any of them** (user counts and headline prices all matched published claims exactly,
   incl. `alpinedata/german-public-tenders` 7u still Germany-only, `wafspaul/kenya-government-tenders` 6u
   still Kenya-only, `datafetch_labs/remote-jobs-scraper` 1u still 7-board at $0.001+$0.00005 start, and
   all 19 UK-FTS handles). Stamped all three with a dated `verified live 2026-10-06` sentence.
2. **Caught and fixed 3 more incidental stale user counts while the checker was open:**
   `kmltmr00/universal-remote-job-scraper` 4→2 users (`remote-jobs-scraper:143`), `martc03/
   nih-clinical-trials` 2→3 users (`clinicaltrials-scraper:126`), `martc03/fda-recalls` 2→3 users
   (`fda-recall-scraper:231`). **`check-competitor-claims` is now fully clean fleet-wide: 877 user-count
   claims / 0 stale, 150 paragraphs / 0 undated/stale.**
3. Shipped as 5 README-only builds: `remote-jobs-scraper` 0.1.47, `eu-ted-tenders-scraper` 0.1.60,
   `uk-find-a-tender-scraper` 0.1.60, `clinicaltrials-scraper` 0.1.52, `fda-recall-scraper` 0.1.56 — all 5
   `apify push --force` SUCCEEDED, all 5 live READMEs verified byte-identical to disk. `check-pricing`
   24/29/0, `check-charges` 24/24. All 3 services active, site `/`/`/tools` both 200.
4. Inbox: same long-vetted noise classes only, nothing actionable, no support requests. Revenue/traffic
   unchanged: $0 — no owner email. Committed and pushed to `origin/main`.

## What 1333 closed

1. **`competitor_audit` on `us-federal-awards-scraper` (1289 → 1333) — DONE, 2 genuine new undercutters
   disclosed, build 0.1.60.** `niche-unnamed`: 144 seen / 124 matched / 48 unnamed (down from 77 at 1289,
   normal churn). `>=3`-user cut empty (max 2u), so the whole 48-listing tail was live-priced via a new
   reusable `bin/_batch_price_ufaw.py`. Found: `northpine-studio/usaspending-awards` (2u, flat
   $0.002/result) and `nightwave-owner/usaspending-federal-contracts` (2u, flat $0.002/contract) — both
   cheaper than our $0.0025 Gold+ rate at every tier, neither has a start fee. Spot-checked
   previously-named handles (`dataio`, `open-data-tools`, `straightforward_hydra`, `invaluable_rondeau`,
   `zinin`) — 0 drift. Verified live byte-identical (52703==52703 bytes); platform smoke run SUCCEEDED
   (12/12 rows). `check-pricing` 24/29/0, `check-charges` 24/24, `check-comparison-breadth` 23/0,
   `check-own-price-freshness` 24/0, all clean.
2. Inbox: same long-vetted noise classes only. Nothing actionable, no support requests.
3. Revenue/traffic unchanged: $0 — no owner email. All 3 services active, site `/`, `/tools`,
   `/tools/us-federal-awards-scraper` all 200. Committed and pushed to `origin/main`.

## What 1332 closed

1. **`competitor_audit` on `fec-campaign-finance-scraper` (1287 → 1332) — DONE, niche clean, two stale
   freshness dates fixed, build 0.1.52.** `niche-unnamed`: 459 seen, 42 matched, all 42 already named,
   **0 unnamed** (42 stable across 1246/1287/1332). Went past 1287's resweep-only pass and **live-priced
   all 42 named rivals end-to-end** (new `bin/_batch_price_fec.py`, same shape as `_batch_price_cts.py`) —
   headline event *and* every plan tier of every charge event, not just the FREE tier
   `check-price-superiority` reads — then machine-diffed every `$` figure the README prints inside each
   rival's own sentence against that rival's live price set: **0 real price drift across 42 rivals** (6
   regex hits, all window-bleed into the next bullet, hand-checked). All five disclosed undercutters still
   accurate (`maximedupre` $0.0009 flat; `jungle_synthesizer` $0.0005 + $0.10 start; `scrapesage` $0.001
   FREE → $0.00025 Diamond; `themineworks` $0.001 → $0.0006 Gold+ + $0.005 start; `automation-lab`
   $0.00184 → $0.000448, under us only from Gold). **The one real defect was the dates** — the README
   claimed "re-verified live … on 2026-10-03" / "re-verified 2026-10-04"; both are now genuinely true as
   of 2026-10-06 and were updated, plus a dated 1332 sentence recording 459/42/0-unnamed and the
   zero-drift full-tier re-price. Verified live byte-identical (46,895 == 46,895) + platform smoke run
   SUCCEEDED 5/5.

2. **Cycle 1330's unfinished fleet-wide `check-competitor-claims` — run to completion, 16 real findings,
   all fixed and shipped.** 873 user-count claims / 150 paragraphs checked: **16 stale rival user counts
   across 10 Actors**, none on `fec-campaign-finance-scraper`. Biggest: `hirebase/remote-jobs` 142→165
   (+16%, the remote-jobs niche's #2 listing by users) and `brilliant_gum/substack-insights-scraper`
   128→144 (30-day figure 29→39 too). Also `x.com/google-playstore-review-scraper` 17→20,
   `parseforge/google-play-store-scraper` 18→16, `logiover/fda-data-scraper` 8→9,
   `parseforge/ip-australia-trademarks-scraper` 3→4, `kmltmr00/universal-remote-job-scraper` 3→4,
   `glidepath/remote-jobs-scraper` 3→4, `malonestar/clinical-trials-meta-search` 2→3,
   `getascraper/eu-ted-tender-monitor` 2→3, `koalastuff/eu-ted-tender-monitor` 2→3,
   `koalastuff/fda-enforcement-report-finder` 2→3, `getascraper/sec-form4-insider-monitor` 2→3, and three
   that FELL: `usta/remote-jobs-feeds` 3→1, `martc03/regulatory-monitor-mcp` 2→1,
   `riadh_chebbi/apple-app-store-reviews-scraper` 3→1. **Two could not be a blind number swap** (see
   LEARNINGS): `riadh_chebbi` lives in a paragraph premised on "every unnamed listing with 3+ users", so
   it became "(1 user today, 3 when that sweep ran)"; `eu-ted-tenders-scraper` grouped three handles under
   one shared "(2 users **each**…)" and only two of the three moved, so the shared count was split into
   three explicit per-handle counts. Shipped as 10 README-only builds, **all 11 builds (incl. FEC)
   SUCCEEDED with all 11 live READMEs byte-identical to disk**; checker re-run after: **875 claims, 0
   stale.**

3. Standing checks clean: `check-pricing` 24/29/0, `check-charges` 24/24, `check-readme-samples` 35+82/0,
   `check-comparison-breadth` 23/0, `check-own-price-freshness` 24/0. All 3 services active; site `/`,
   `/tools`, `/tools/fec-campaign-finance-scraper`, `/pricing` all 200. Inbox: long-vetted noise only.
   Revenue/traffic unchanged ($0, 44 users, 579 runs30d) — no owner email.

## What 1331 closed

1. **QUALITY/GROWTH slot — `enum_audit` on `apple-podcasts-scraper` (797 → 1331) — DONE, 91 missing
   `chartGenre` subgenre values found and shipped, build 0.1.69.** Re-derived fleet-oldest directly
   from `audit_dates.json`: `enum_audit` at 797 (never done on this Actor since launch) was by far the
   oldest entry across both real axes (`varied_test` fleet-oldest was 1075). Pulled Apple's own genre
   tree live (`ws/genres?id=26`) and found `chartGenre`'s whitelist had only the 19 TOP-LEVEL categories
   — Apple's tree has **91 more real leaf subgenres** underneath them (Christianity/Islam/Judaism under
   Religion & Spirituality; Soccer/Football/Basketball under Sports; Business News/Tech News/Politics
   under News; etc.), each with its own per-genre chart feed on the exact same endpoint our code already
   calls. **Verified live these are genuinely distinct charts, not a filtered view of the parent**:
   Judaism/Islam top-10s share zero titles with each other or the overall Religion & Spirituality chart;
   Soccer's top-10 shares zero titles with the overall Sports chart.
2. **Shipped all 91 as new `CHART_GENRE_IDS` map entries + matching `input_schema.json` enum/enumTitles**
   (111 values total incl. the existing `""` overall-chart option) — camelCase keys generated
   programmatically from Apple's subgenre names, checked for zero collisions against the existing 19 keys
   and each other before writing. Cross-verified main.js's key SET and the schema's key SET are exactly
   identical (not just same length) before shipping. README input table + FAQ updated to say 110 values
   (19 + 91), not the stale "19 genres" line.
3. **No other enum field on this Actor needed changes — recorded so it isn't re-derived:** `chartType`
   (shows/episodes) is Apple's only 2 chart types; `explicitFilter`/`sort` are this product's own filter
   vocabulary, not an Apple-API enum, so there's no external vocabulary to diff them against.
4. Verified live byte-identical (README 41,023==41,023 bytes; `chartGenre` enum/enumTitles both match disk
   exactly) via the build's own `actorDefinition`. **Platform-verified end-to-end**: default regression
   SUCCEEDED 5/5 unaffected; two NEW subgenre values (`christianity`, `soccer`) run live through the Actor
   matched the direct Apple API exactly; an unrecognized `chartGenre` still falls back cleanly with a
   warning (no crash). `check-pricing` 24/29/0, `check-charges` 24/24. `audit_dates.json` updated with
   `indent=1` (surgical 2-line diff — first `package.json` bump attempt via `json.dumps` reformatted the
   whole file, reverted before committing, same recurring trap as cycles 1327/1328).
5. Inbox checked: same long-vetted noise classes only, plus two more JP/IT-style contact-form
   autoresponders (`co-sol.ca`, `adkm.it`) — same noise class, not new. Nothing actionable, no support
   requests. Dev.to: last published 2026-10-04T19:02Z, 2 days out, right at the cadence edge, not clearly
   due — no article written this cycle (time-boxed).
6. Revenue/traffic unchanged: $0, no owner email warranted. All 3 services active, site `/`, `/tools`,
   `/tools/apple-podcasts-scraper` all 200.

## What 1330 closed

1. **`competitor_audit` on `nih-reporter-scraper` (1284 → 1330) — DONE, clean resweep + 1 user-count
   drift fixed, build 0.1.38.** `niche-unnamed` re-swept clean: 274 seen, 51 matched, README names all
   51 — 0 unnamed, no new listing since 1284. Live-priced all 51 named handles end to end (headline
   price + FULL `eventTieredPricingUsd` map per tiered listing, not just the FREE tier that
   `check-price-superiority`'s `price_of()` reads) via a one-off script reusing that script's helpers.
   Every cited price matched exactly, including both already-published full per-tier breakdowns
   (`themineworks/nih-reporter-grants` $0.001→$0.0006, `publicmoney/nih-reporter-grants-scraper`
   $0.002→$0.0007) and the `tagadanar/us-grants-monitor` citation (its `award-record` event, $0.003
   Free + $0.001 start, is correctly the one cited for NIH data even though Apify's Store
   `isPrimaryEvent` flag points at a DIFFERENT event on the same Actor, `opportunity-found`, which
   prices its separate Grants.gov-opportunities product — `isPrimaryEvent` is a Store-display choice,
   not a per-dataset truth, when one Actor sells two things). One real drift found:
   `mambalabs/public-award-monitor`'s user count moved 2 → 3 (+50%, past the 10% tolerance) — fixed;
   its tiered price map itself is unchanged. Shipped README-only, verified live byte-identical
   (35645==35645 bytes) via the build's own `actorDefinition.readme`; real platform smoke run
   SUCCEEDED (10/10 rows). `check-pricing` 24/29/0, `check-charges` 24/24. Fleet-wide
   `check-price-superiority` separately confirms 0 undisclosed cheaper rivals anywhere (1391 compared).
   `audit_dates.json` updated.
2. Inbox checked: same long-vetted noise classes only. Nothing actionable, no support requests.
3. Revenue/traffic unchanged: $0, no owner email warranted. All 3 services active, site `/`, `/tools`,
   `/tools/nih-reporter-scraper` all 200.

## What 1329 closed

1. **`competitor_audit` on `clinicaltrials-scraper` (1283 → 1329) — DONE, clean resweep + 2 new exact ties
   and 2 traps correctly handled, build 0.1.54.** Re-derived fleet-oldest from `audit_dates.json` directly
   (`scholarship-scraper` still correctly skip-listed until 2026-10-20). Fresh full-cohort sweep: 153 seen,
   121 matched, 74 unnamed (up from 152/120/85 at 2026-10-05) — **completeness holds, no real new
   undercutter.** The `>=3`-user cut cleared only `funnyvalentine69/fda-drug-pipeline-intelligence` (3u,
   $0.005/row) and `red.cars/drug-intelligence-mcp` (3u, $0.03/call) — both AI-synthesis/MCP multi-source
   products out of scope by shape and dearer anyway. Live-priced the full 74-listing unnamed tail via a new
   reusable `bin/_batch_price_cts.py`: two previously-unnamed exact ties at our $0.0015/study rate —
   `aurenic/clinicaltrials-scraper` (2u, ties the rate but also bills a $0.00005 start fee we don't charge,
   so dearer overall) and `realai_pl/recruiting-clinical-trials` (2u, no start fee but scoped to
   `overallStatus: RECRUITING` only, not a full substitute) — plus two sub-$0.002-headline traps correctly
   excluded (`malekh/clinical-trial-protocol-amendments` and `red.cars/clinical-trials-mcp`, both advertise
   a $0.00001 dataset-item event but their real charges are $0.05-$0.75 per non-row event). Spot-checked all
   previously-named headline rivals live (`parseforge`, `logiover`, `bovi`, `ryanclinton`, `pink_comic`,
   `devilscrapes`, `scrapepilot`, `alizarin_refrigerator-owner`, `quotient_variablebarrier`, both `labrat011`
   listings, `webdata_labs`) — all matched published figures exactly except `parseforge` ticking 46→47 users
   (inside the 10% tolerance, not restated). Shipped README-only, build 0.1.54 (package.json 0.1.14→0.1.15),
   verified live byte-identical (43,074==43,074 bytes) via the build's own `actorDefinition.readme`; real
   platform smoke run SUCCEEDED (12/12 rows, no regression). `check-pricing` 24/29/0, `check-charges` 24/24.
   `audit_dates.json` updated with `indent=1` preserved (diff checked — only the touched lines moved).
2. Inbox checked: same long-vetted noise classes only (Bytewells pitch, `searchindex.pro` SEO scam, JP/IT
   contact-form autoresponders, DMARC report, a bounce). Nothing actionable, no support requests.
3. Revenue/traffic unchanged: $0, no owner email warranted. All 3 services active, site `/`, `/tools`,
   `/tools/clinicaltrials-scraper` all 200. Committed (`29ef602`) and pushed to `origin/main`.

## What 1328 closed

1. **QUALITY/GROWTH slot — `enum_audit` on `fda-recall-scraper` (797 → 1328) — DONE, 3 MISSING enum values
   + 1 silent-row-loss disclosure found and shipped, build 0.1.50.** Re-derived the stalest axis fleet-wide
   from `audit_dates.json`: `enum_audit` (797, tied `apple-podcasts-scraper`/`fda-recall-scraper`) — picked
   the FDA one because openFDA's `count=<field>.exact` makes cycle 828's **bidirectional** facet-diff possible
   (the 797 pass predated that method and could only ever find *dead* values, never missing ones). 9 requests
   gave the complete live vocabulary for all 3 enum fields × 3 endpoints. Findings:
   - **`classifications` was missing a real 4th value `Not Yet Classified`** (food 2 / drug 2 / device 1):
     selecting Class I+II+III was **not** equivalent to leaving the filter empty, and those rows were
     unreachable through the filter entirely.
   - **`voluntaryMandated` was missing `N/A`** (6 / 23 / 8 = 37 rows), FDA's own value for an uncaptured
     initiating party. A further 23 rows (1/12/10) carry an **empty** value — documented as only reachable
     with the filter off, since our `''` option means "no filter".
   - **`dateField` was missing `center_classification_date`** — a real range-queryable *and* sortable date
     field on all 3 endpoints at ~99.99% coverage, i.e. **better covered than the `termination_date` we
     already shipped.**
   - **Disclosure gap (the highest-value find for buyers): `dateField=termination_date` silently shrinks the
     CORPUS, not just the window.** `_exists_` counts: food 27,958/29,471 (~5% lost), drug 14,810/18,002
     (~18%), device **25,491/40,113 (~36%)**. A row with no value in the chosen date field can never be
     returned however wide the window, so `termination_date` is the wrong field for any "how many recalls"
     total. Now a README FAQ table + input-table note + schema warning.
2. **Both new enum values needed the schema AND the client-side allowlist in `main.js` patched**
   (`CLASSIFICATIONS`, `VOLUNTARY_MANDATED`, `DATE_FIELDS`) — cycle 838's lesson, live again: the allowlist
   silently coerces an unrecognised value away, so a schema-only fix would have shipped a dead dropdown
   option. `riskScore` already scored an unknown classification with a neutral severity component (no change).
   Also fixed the now-misleading `order` enumTitles ("Newest **report date** first" → "Newest first (by the
   date field above)") since there are 4 date fields now.
3. **CLEAN/CLOSED on this Actor — do not re-derive:** `status` facets to exactly Ongoing/Completed/Terminated
   on all 3 endpoints, so `Pending` remains real-vocabulary-but-zero-data (existing warning is correct);
   every facet set reconciles **exactly** to the endpoint grand totals (29,471 / 18,002 / 40,113), proving
   there are no blank `status` or `classification` rows; `productTypes` is complete — openFDA's own
   `/download.json` manifest lists `enforcement` under food, drug and device **only**
   (tobacco/animalandveterinary/other all 404), so there is no 4th endpoint to add.
4. Verified live: 3 local runs proved each new value returns exactly the facet-predicted rows (5 for
   `Not Yet Classified`, the `N/A` rows in correct `center_classification_date` sort order); one apparent
   zero-row result was checked against the API directly and was a **genuine** zero (newest `N/A` drug row is
   2023-11-16, so a 2025 window correctly returns nothing) rather than a bug. Live README byte-identical
   (51,230 bytes) via the build's own `readme` field; **platform smoke run SUCCEEDED** (2/2/1 = 5 rows).
   `check-pricing` 24/29/0, `check-charges` 24/24. `audit_dates.json` updated with `indent=1` (this file's
   real indent). The `input_schema.json` edit was done with surgical `Edit` calls, not `json.dumps` — the
   first attempt reformatted the whole file (424 lines) because it hand-formats short arrays inline; caught
   and reverted before committing, same trap as cycle 1327.
5. Inbox: same long-vetted noise classes only (bytewells pitch, `searchindex.pro` SEO scam, JP/IT
   contact-form autoresponders, DMARC report, one bounce). Nothing actionable, no support requests.
   Revenue/traffic unchanged: $0, 44 users, 577 runs30d, 0 bookmarks/reviews — no owner email. All 3 services
   active, site `/`, `/tools`, `/tools/fda-recall-scraper` all 200.

## What 1327 closed

1. **`competitor_audit` on `ats-jobs-scraper` (1281 → 1327) — DONE, clean resweep + 1 stale user count
   fixed, build 0.1.66.** The >=3-user unnamed cohort (39 listings this time, composition changed from
   44) was fully live-priced via a new reusable `bin/_batch_price_ats.py` — **zero new undercutters**,
   every one dearer than our GOLD+ rate at every tier; `vnx0/lever-ats-job-scraper` and
   `chilly_damask/company-careers-job-scraper` (both 8u, flat $0.001/job) only tie our FREE tier, same
   shape as the already-named `wickfeed` tie.
2. **Resolved (as far as possible) the `illehius/ats-jobs-scraper` ambiguity flagged since 1281:**
   attempted a real test run to see which of its two charge events actually fires — got `403
   public-actor-disabled`, confirming **our Apify plan cannot run ANY public Actor at all**. This is
   permanent, not a "recheck when it grows users" item — documented so no future cycle retries it.
   User count updated 1→4 in the note regardless.
3. Spot-checked all 20 previously-named headline rivals' full tiered price maps live — all unchanged
   except `openclawai/career-site-ats-jobs-scraper`'s user count (19→22, +16%, past tolerance), fixed.
   Own price re-verified first, zero drift.
4. Verified live byte-identical via the build's own `readme` field (43,036 bytes); post-push smoke run
   SUCCEEDED (50/50 rows, no regression — this Actor's `companies` input is `{ats,slug}` objects, not
   `"provider:slug"` strings, learned the hard way on the first smoke-test attempt). `check-pricing`
   24/29/0, `check-charges` 24/24. `audit_dates.json` updated with `indent=1` (this file's real indent
   — caught an accidental `indent=2` whole-file reformat before committing, see LEARNINGS.md).
5. Inbox: same long-vetted noise classes only, nothing actionable. Revenue/traffic unchanged: $0, no
   owner email. All 3 services active, site `/`, `/tools`, `/tools/ats-jobs-scraper` all 200.

## What 1326 closed

1. **`competitor_audit` on `court-records-scraper` (1280 → 1326) — DONE, completeness holds, one real
   drift fixed, build 0.1.49.** `niche-unnamed` re-swept clean: 434 seen/30 matched, README names all
   40 handles, **0 unnamed** — no new rivals since 1280's full-cohort sweep. Live-reread `pricingInfos`
   for the 7 closest-named rivals rather than trusting the 1280 prose: 6/7 exact, but
   `haketa/federal-court-records-scraper` drifted on both counts it's named for — users 9→11 (+22%,
   past the 10% tolerance) and the tier claim was wrong. README said it undercuts us only on Diamond
   ($0.0018); the full `eventTieredPricingUsd` map shows GOLD and PLATINUM are also flat $0.0018 (below
   our $0.002 flat), so it undercuts from **GOLD up**, three tiers not one. Fixed both, dated
   2026-10-06. `pink_comic` ticked 15→16 users but stayed inside tolerance — left alone. Verified live
   byte-identical via the build's own `actorDefinition.readme` (41,042==41,042 bytes); real platform
   smoke run SUCCEEDED (12/12 rows, one transient upstream CourtListener timeout+retry, no regression).
   `audit_dates.json` updated — new fleet-oldest is `ats-jobs-scraper` (1281).
2. **Found and fixed a 2-cycle git commit backlog.** Cycles 1324 (`trademark-search-scraper`) and 1325
   (`clinicaltrials-scraper`) both shipped real Apify builds and updated state files, but neither
   cycle's working tree was ever committed — last commit on `main` was `ad2c727` (cycle 1323). Committed
   each backlogged fix separately (`29cb2b6` for 1324, `f9b0116` for 1325) plus this cycle's own fix
   (`163b25e`), then pushed all three to `origin/main`. **Lesson for future cycles: verify `git status`
   is clean (or commit your own diff) before ending every cycle — the STATUS.md/queue.md write-up alone
   does not guarantee the code change was committed.**
3. Inbox checked: same long-vetted noise classes only (Bytewells pitch — re-open trigger stays
   2026-11-02 — plus the usual SEO scam / JP/IT autoresponders / DMARC / bounce). No support requests.
4. Revenue/traffic unchanged: $0, no owner email. All 3 services active, site `/`, `/tools`,
   `/tools/court-records-scraper` all 200.

## What 1325 closed

1. **Owed QUALITY/GROWTH slot — `varied_test` on `clinicaltrials-scraper` (1073 → 1325) — DONE, real
   bug found and fixed, build 0.1.53.** The file's own precedence comment claimed "a typed input for
   the same key overwrites" a `startUrl`'s `aggFilters` code, but that was only coded for 3 of the 10
   UI sidebar codes (`docs`/`results`/`violation`, which share one Map with their typed equivalents).
   The other 7 (`status`/`phase`/`studyType`/`sex`/`healthy`/`ages`/`funderType`) route through a
   separate mechanism (`filter.overallStatus` / `AREA[...]filter.advanced`) that never touched the
   `startUrl`'s code — so a pasted URL's `aggFilters=status:rec` plus a typed
   `overallStatus:["COMPLETED"]` silently ANDed into a contradiction instead of the typed value
   winning. **Verified 3 ways live:** direct CT.gov API (rec alone=18,747, COMPLETED alone=53,394,
   both=**0**); reproduced through the Actor pre-fix (`declaredMatches:0`, generic "No studies
   matched" advice, no mention of the real cause — same undisclosed-contradiction shape as cycle
   1028's `resultsAvailability`+`resultsFirstPostedDate` fix); post-fix the same combo returns 5/5
   genuinely-`COMPLETED` rows. Two regressions confirmed clean: non-conflicting `startUrl`
   (`status:rec,phase:3`, no typed override) still 5/5 `RECRUITING`+`PHASE3`; plain no-`startUrl`
   search still filters correctly. Fix: delete the `startUrl`'s aggFilter-code entry for any of the 7
   keys whose matching typed input is set, before the `aggFilters`/`AREA[...]` params are built.
   Shipped README (new FAQ entry + input-table note) + source, build 0.1.53 (source
   0.1.13→0.1.14), verified live byte-identical via the build's own `actorDefinition.readme`
   (40,810==40,810 bytes) + 3 phrase probes. `check-pricing` 24/29/0, `check-charges` 24/24.
   `audit_dates.json` updated — this Actor's `varied_test` note now documents the fix.
2. Inbox checked: `peter@bytewells.com` "monthly rentals for ats jobs scraper" looked new but is the
   same already-diligenced-and-declined Bytewells pitch, just worded around a different Actor —
   re-open trigger stays **2026-11-02**, not before. Everything else is the long-vetted noise classes.
   No support requests.
3. Dev.to cadence checked **by hitting the API directly**: last published 2026-10-04T19:02Z, cadence
   1/2-3 days, not clearly due — no article written this cycle (time-boxed; the bug fix above was the
   higher-value use of the cycle).
4. Revenue/traffic unchanged: $0, no owner email. All 3 services active, site `/`, `/tools`,
   `/tools/clinicaltrials-scraper` all 200. $0 spent beyond the one build + a handful of small
   self-charged verification runs.

## What 1324 closed

1. **`competitor_audit` on `trademark-search-scraper` (1278 → 1324) — DONE, three stale whole-niche
   aggregates + one stale user count fixed, build 0.1.38.** Niche grew on BOTH counts: `niche-size`
   default 108 → **114** mentions, `--strict` 84 → **89** real trademark products (543 distinct seen).
   The README still published `108/84` AND the cycle-1212 bookkeeping *"names 37 of the niche's 84 …
   priced all 47 that it does not"* — re-derived mechanically (strict matched set minus full-handle
   substring match) that is **89 matched / 58 named / 31 unnamed**, i.e. three numbers wrong at once.
   All 31 live-priced end to end via a new reusable `bin/_batch_price_tmss.py` (55 default-mode unnamed
   priced; the 31 strict ones are the real niche). **COMPLETENESS HOLDS** — zero undercutters, the
   7-undercutter set is still the full set. Closest unnamed is
   `unrivaled_fortress/wipo-global-trademark-brand-watch` at $0.0026/row GOLD+ (1.3x ours, a new-filings
   feed not a register search), then `axiomworks` at $0.002975 GOLD+. **13 listings named for the first
   time** (10 never priced before + `friendlyapi`/`automation_studio`/`stefano_seggio`, which 1278 priced
   but never named by handle), incl. `devilscrapes/uspto-trademark-scraper` ($0.005/result + a **$0.20
   actor-start**, dearest start fee in the niche) and `neverempty/uspto-trademark-search-monitor` (closest
   in SHAPE — a real USPTO text/owner/class search + monitoring, $0.008→$0.005/row). Sub-$0.002 trap
   re-checked: 7 of the 31 advertise a sub-$0.002 event and **not one is a row price** (6 actor-start
   fees + `neverempty`'s $0.0005 monitoring check). Also fixed `dev00/uspto-trademark-api` 59 → **68**
   users (+15%, now past `check-competitor-claims`' 10% tolerance; was 62/within-tolerance at 1212) —
   that check now reports 14 stale fleet-wide, none on this Actor. Verified live byte-identical via the
   build's own `actorDefinition.readme` (32662 == 32662 bytes) + 5 phrase probes; post-push smoke run SUCCEEDED
   (solar/US+EM/class 9/Registered → 20 rows of 1,436 declared). `check-pricing` 24/29/0,
   `check-charges` 24/24, `check-own-price-freshness` 0 flags. `audit_dates.json` updated. Full write-up
   in STATUS.md cycle 1324.
2. **WATCH ITEM re-verified live and STILL PENDING, do not re-derive it:** both `dev00` listings' filed
   change is still `startedAt 2026-10-14T16:43:52.372Z` and still **FREE-plan-only**
   (`uspto-trademark-api` trademark-verify flat $0.003 → FREE $0.10 / BRONZE+ $0.003;
   `uspto-trademark-text-check-api` $0.005 → FREE $0.10 / BRONZE+ $0.005). The README already states this
   with exact numbers — a cycle on/after **2026-10-14** need only flip the tense. Do **not** read it as a
   general price rise.
3. Inbox checked: same long-vetted noise classes only (bytewells pitch, `searchindex.pro` SEO scam,
   Japanese/Italian contact-form autoresponders, DMARC report, one bounce). Nothing actionable, no
   support requests.
4. Revenue/traffic unchanged: $0, 44 users, 564 runs30d, 0 bookmarks/reviews — no owner email. All 3
   services active, site `/`, `/tools`, `/tools/trademark-search-scraper` all 200.

**New standing note for this Actor (3-for-3 failure mode):** the stale-whole-niche-aggregate defect has
now hit `trademark-search-scraper` at 1212, 1278 and 1324. Its niche grows every ~45 cycles, and no
standing check we own catches a count sentence. **Always re-run `niche-size --strict` AND re-derive the
named/unnamed split mechanically before trusting any count in this README.**

## What 1323 closed

1. **`competitor_audit` on `uk-find-a-tender-scraper` (1277 → 1323) — DONE, 3 real undercutters found and
   disclosed, build 0.1.59.** Niche re-swept to 102 matched (up from 99); the `>=3`-user cut came back
   empty again (19 unnamed, all 1-2u), so the whole tail was live-priced via a new reusable
   `bin/_batch_price_uktft.py`. New finds: `jtpalms/gov-tenders-monitor` and
   `thriftykiwi/public-tenders-aggregator` (single-portal, cross over ~38-42 rows),
   `optimistprime/uk-eu-public-tenders` (genuine FTS+CF+TED 3-source substitute, crosses over ~129 rows
   on Gold+), plus `compass_lab/uk-tenders-scraper` (dual-portal, dearer). Two listings
   (`mikee368/eu-tender-monitor`, `dobus/eu-uk-public-tender-intelligence-api`) matched the sweep's search
   terms but read **no UK portal at all** on inspection of their own description — a title-only read would
   have miscounted both. Verified live via the build's own `readme` field; post-push smoke run SUCCEEDED
   (15/15 rows, no regression). `check-pricing`/`check-charges`/`check-own-price-freshness` all clean.
   `audit_dates.json` updated. Full write-up in STATUS.md cycle 1323.
2. Inbox checked: same long-vetted noise classes, nothing actionable, no new support requests.
3. Revenue/traffic unchanged: $0, 44 users, 564 runs30d — no owner email.

## What 1322 closed

1. **QUALITY/GROWTH slot — `varied_test` on `google-news-scraper` (1071 → 1322), DONE, real finding
   fixed.** Tested the never-before-tried combo `decodeUrls:false` + `fetchArticleBody:true`. Found
   `main.js` silently forces `decodeUrls` back on whenever `fetchArticleBody` is on (needs the real URL
   to fetch the body) — only logged as a run-log warning, never disclosed in README/schema. Proven live
   on a real `"Tesla"` query: `url` still came back fully resolved (`teslarati.com`, `futurism.com`)
   despite `decodeUrls:false`. Not a code bug (the override itself is correct and necessary) — fixed
   the disclosure: new FAQ entry + input-table/schema notes, pointing to `googleNewsUrl` as the escape
   hatch for the raw link. Shipped README/schema-only, build 0.1.63, verified live via the build's own
   `readme` field; post-push smoke run clean, no regression. `check-pricing`/`check-charges` both
   clean. Full write-up in STATUS.md cycle 1322 and `audit_dates.json`'s `varied_test_note`.
2. Checked dev.to cadence **by hitting the API directly**, not a copy-forwarded note (cycle-997
   lesson) — last published 2026-10-04T19:02Z, cadence is 1/2-3 days, genuinely not due. No article
   written this cycle.
3. Inbox checked: nothing actionable, same long-vetted noise (DMARC report, `searchindex.pro` SEO
   scam, Japanese/Italian contact-form autoresponders, a bounce). No new pitches, no support requests.
4. Revenue/traffic unchanged: $0, 44 users, 564 runs30d — no owner email.

## What 1321 closed

1. **`competitor_audit` on `sam-gov-opportunities-scraper` — DONE, clean (build 0.1.43).** Rotation
   moved 1275 → 1321. Niche grew 140 → 145 matched; the `>=3`-user cohort was empty again (max 2u), so
   per the standing full-cohort rule all 80 unnamed listings were live-priced via a new reusable
   `bin/_batch_price_sgos.py`. **Zero new findings** — no free rivals, no undercutters anywhere in the
   80. Also spot-checked the 6 headline undercutters already named in the README (`jungle_synthesizer`,
   `scrapesage`, `yourwingman`, `acid-base`, `bridged`, `gochujang`) live — zero drift on any of them.
   Shipped README-only, verified via the build's own `readme` field; post-push smoke run SUCCEEDED (1/1
   row, 1 charge, no regression). Full write-up in STATUS.md cycle 1321 and `audit_dates.json`'s
   `competitor_audit_note`.
2. Inbox checked: all noise classes already catalogued, plus one new one worth recording — a
   cold-outreach email from `capsule26.com` (self-described autonomous AI agent business) asking a
   genuine technical question about our watch-mode-rebilling postmortem. Not a support request, not
   revenue, no reply needed/sent. Another `bytewells.com` pitch also arrived (same pitch as before,
   still correctly declined per the 1316 diligence — re-open trigger not before 2026-11-02).
3. Revenue/traffic unchanged: $0, 44 users, 564 runs30d, 0 bookmarks/reviews — no owner email.

## What 1320 closed

**`competitor_audit` on `grants-gov-scraper` — DONE, two real README corrections shipped (build
   0.1.51).** Rotation moved 1273 → 1320. Priced the whole niche live, both halves: all **53 unnamed**
   listings AND all **34 already-named** rivals, every event and every tier (87 live GETs). Niche is now
   **87 matched** (was 85). Full write-up in STATUS.md cycle 1320 and `audit_dates.json`'s
   `competitor_audit_note`.
   - **Unnamed tail is CLEAN** — zero undercutters, zero FREE-model listings. **Do not re-flag
     `tagadanar/us-grants-monitor`**: its `$0.001` is an `actor-start` RUN FEE, not a row price; its real
     row event is `$0.004 → $0.0028` (GOLD+), 1.9–2.7x ours. Named in the README so it stays closed.
   - **Two named rivals were TIERED where we had published FLAT**, both fixed:
     `vhsgreed/us-federal-contracts` (`record` $0.00125/$0.00115/$0.00105/$0.00095 — our published "~8
     rows" break-even was its FREE tier only; really ~8/~5.7/~4.4/~3.6, so paid-plan buyers cross over
     twice as early as we said) and `upward_enterprises/grants-gov-opportunity-finder` (detail
     $0.003→$0.0024, summary $0.001→$0.0008; "dearer at both tiers" conclusion survives at every plan).
   - **Recurring failure mode worth remembering, not re-discovering:** this is the *second* time this
     Actor's README published a FREE-tier price as if it were flat (cycle 1233 self-corrected
     `shahidirfan`/`chorelet` the same way). When auditing ANY niche, read the full
     `eventTieredPricingUsd` map — `bin/check-price-superiority`'s `price_of()` returns the **FREE tier
     only**, which is exactly how both of these got published wrong.

## Open for 1324 (next BUILD/AUDIT cycle)

1. **`competitor_audit` fleet-oldest: `trademark-search-scraper` (1278)** < `court-records-scraper` (1280)
   < `ats-jobs-scraper` (1281) < `clinicaltrials-scraper` (1283) < `nih-reporter-scraper` (1284).
   **Re-derive from `audit_dates.json` directly rather than trusting this cached list** — it moves every
   time any Actor is audited.
2. **Other axes, fleet-oldest (for reference — `competitor_audit` is the live rotation):**
   `varied_test` → `google-news-scraper` (1071); `enum_audit` → `apple-podcasts-scraper` / `fda-recall-scraper`
   (both 797); `unreachable_remedy` → has **no never-done candidates left** (closed fleet-wide at 1318);
   re-ranking fleet-oldest among its 24 done entries is the only way to revisit it, and no re-sweep is
   due — **don't pick it as a top task.**
3. **Loose thread, not urgent, for a future `remote-jobs-scraper` `competitor_audit`** (carried from
   1319): verify live whether `datafetch_labs/remote-jobs-scraper` has a genuinely structured
   "region-style" location filter that our `locationKeyword` substring match does not match. Flagged
   honestly in that README as unverified rather than conceded. **The board-count gap itself is CLOSED
   (WWR added as a 7th board at 1319) — do not re-add WWR or re-litigate it.**

**Standing constraints, unchanged:**
- **SKIP `scholarship-scraper` entirely** (it is fleet-oldest on every axis and will keep surfacing):
  bold.org has 429'd it since 2026-09-20, decision point **2026-10-20** (cycle 1292). That date has NOT
  passed as of 2026-10-06 — check it before touching this Actor at all.
- **Axis-ranking rule, settled, stop re-litigating:** only `varied_test`, `enum_audit`,
  `unreachable_remedy`, `competitor_audit` are real fleet-wide rotations (24 entries each).
  `count_audit`, `input_error_advice`, `description_mine`, `watch_subset_audit`, `search_scope_audit`
  are one-off experiments (cycle-1304 LEARNINGS entry) — never rank them against the 4 real axes.
- **`competitor_audit` method:** run `bin/niche-unnamed` first; if the >=3-user cut is thin or empty,
  live-price the WHOLE unnamed tail, and if it is large, live-price the whole >=3-user cut anyway
  (reuse the `_batch_price_*.py` `SourceFileLoader` pattern with `raw_events` + `startedAt` so finalist
  tiers need no second round of calls); **never rule a listing out of scope on TITLE ALONE** — read the
  live Store description, and for anything that looks like a real substitute read its latest build's
  `actorDefinition.readme` + input schema too; verify full `pricingInfos` event maps by CURRENT
  `startedAt` across MULTIPLE tiers before naming anyone. A low price in a listing's TITLE is
  marketing, not a price. **Also distinguish a per-ROW event from an `actor-start` RUN FEE before
  calling anything an undercutter** (cycle 1320's `tagadanar` false positive — `isOneTimeEvent` is
  `false` on some start fees, so that flag alone will not save you). Diff published prose against live
  prices in BOTH directions, not just "did anyone undercut us" (cycle 1288).
- **Bytewells — DILIGENCED AND DECLINED at 1316. Stop re-flagging it.** Payout geography is
  dispositive (EU/EEA/UK only; owner is in Egypt), PPE unsupported at launch, and their API-key import
  wants full Apify account access. **RE-OPEN TRIGGER — not before 2026-11-02** (their stated public
  launch), and only if Egypt appears in the payout-country answer at
  `https://bytewells.com/developer-waitlist`. Their pitch mail keeps arriving; it is noise now.
- **Inbox:** nothing actionable as of 1320. All remaining mail is the long-vetted noise classes (DMARC
  reports, `searchindex.pro` SEO scam, Japanese/Italian contact-form autoresponders, the `j_woodgate01`
  advance-fee pitch, the `bytewells.com` pitch, the owner's stale scholarship-scraper forward, one
  bounce). No support requests outstanding.
- **Polar checkout stays deferred** by owner decision — do NOT ask for it unless `bin/traffic` shows
  >100 visits/day to `/pricing` or `/tools`, or a real purchase request lands in the inbox.
