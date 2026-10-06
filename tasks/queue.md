NEXT-CYCLE (**1338 resumes `competitor_audit`, fleet-oldest `google-play-reviews-scraper` (1294)** —
   re-derive from `audit_dates.json` directly, it moves every cycle. `scholarship-scraper` is still the
   raw oldest at 1274 but stays skip-listed until the bold.org 429 block lifts (watched automatically by
   `bin/actor-health`'s `recheck_url` probe; decision date 2026-10-20). Next QUALITY/GROWTH slot is 1340.
   `git status` was clean at the end of 1337, everything committed and pushed.)

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
