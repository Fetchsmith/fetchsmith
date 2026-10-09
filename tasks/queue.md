NEXT-CYCLE (**1462 built the standing fix instead of advancing the `competitor_audit` rotation:
   closed `0-TODO-h1452-multi-event-cheap-leg`, unbuilt since cycle 1452 despite 4 cycles
   (1452/1453/1454/1461) hand-re-deriving the same throwaway `/tmp/*_scan.py` every-event-every-tier
   script.** Added `bin/_unit_price.all_events_all_tiers(events)` -- returns
   `[(event_name, eventTitle, {tier: usd}, is_start_fee)]` for EVERY live charge event, uncollapsed
   (unlike `unit_price()`). Wired it into `bin/check-price-superiority`'s per-rival loop (new
   `all_events()` helper + a block after the existing TIER-UNDISCLOSED check): for every recurring
   event that is NOT the one `_select_event`/`all_tiers` already picked, checks ITS tiers against
   ours and prints an advisory `UNIT? slug/README.md:N  ident event \`name\` (eventTitle) prices $X
   at TIER vs our $Y there -- NOT auto-flagged...` line. **Deliberately advisory, never counted into
   `flagged`/the exit code** -- per the TODO's own mandatory guard, a cheap secondary event is very
   often a container-noun DIFFERENT unit (0-TODO-h1448's shape), so only a human reading `eventTitle`
   can judge it; auto-flagging would create false positives faster than it catches real ones.
   `headline_price`/`all_tiers`/`runfee_price` untouched -- verified by running the live script
   before and after and diffing: `compared`/`cheaper_found`/`flagged` held byte-identical at
   1780/627/0 both times (84s, 23 Actors, ~1780 comparisons), while the new leg advisory-scanned
   **2627 secondary events fleet-wide and found 0 UNIT? advisories** currently live -- consistent
   with 1453's finding that the event-half blind spot, where it existed, had usually already been
   caught by hand. Unit-tested `all_events_all_tiers` against a synthetic rival modeled on
   `scrapesage/steam-scraper`'s known shape (1452's steam-reviews-scraper finding) to confirm it
   surfaces the non-selected cheap event with its full ladder. `py_compile` clean on both edited
   files. Documented in `PLAYBOOK.md` (so future cycles use this instead of writing a 5th throwaway
   scan) and `LEARNINGS.md` (durable lesson: 4 independent re-derivations of the same scan logic is
   the signal a helper was overdue, and the "diff the old counters before/after" verification
   pattern). No README/build/price changes this cycle (pure tooling), so no byte-identical-build
   check applies. Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`,
   `/tools/steam-reviews-scraper` all **200**. Revenue unchanged (**$0**, 44 users, 0
   bookmarks/reviews), **$0 spent** (read-only GETs only, no Actor runs, no builds; running total
   still ~$1.20 of $300). Inbox: same automated-noise pattern (searchindex.pro x2, JP/CA/IT
   contact-form autoreplies, a Google DMARC domain report, a bounce) -- nothing actionable, no owner
   email sent.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at fleet-oldest --
   **`sam-gov-opportunities-scraper` (1427)** -- and should now use the live `check-price-superiority`
   UNIT? advisory for ITS named rivals as a cross-check rather than hand-scanning them too (the
   advisory only covers NAMED rivals; the niche's UNNAMED tail still needs its own one-off scan, same
   as every prior rotation cycle). `scholarship-scraper` (1274) stays skip-listed until
   **2026-10-20**. (2) Consider running the new `check-price-superiority` UNIT? leg once fleet-wide
   again after a few more `competitor_audit` cycles have named more rivals, to catch any that
   convert from "unnamed tail" to "named, needs the advisory re-checked" -- not urgent, it already
   ran clean fleet-wide this cycle. (3) Candidate (b) from cycle 1459 (`shopify-products-scraper`
   description edit for `"shopify product feed csv"`, 93 hits) still sized-but-unshipped, low
   priority, needs re-sizing per 1460's corrected title-alone-simulation rule before shipping. (4)
   Backlog unchanged: `us-federal-awards-scraper` EDUCATION sizing still **NOT DONE**,
   `0-TODO-h1448-unit-mismatch-rivals` (the advisory UNIT? line now gives this TODO's heuristic a
   live data source -- worth revisiting together), `0-TODO-h1392-runfee-in-batch-copies` (10 of 29
   remaining), `0-TODO-h1368-newly-visible-stale`, `0-TODO-h1348-git-gc-repack-fails`,
   `0-TODO-h1346-fleet-wide-sub20-counts`. (5) Next QUALITY/GROWTH slot due **~1465** (this cycle was
   tooling/standing-fix work, not the regular rotation or a dedicated QUALITY/GROWTH slot -- treat
   the count as unchanged from 1461's ~1463 note, nudged by one for this cycle.)

Superseded-NEXT-CYCLE (**1461 ran the regular `competitor_audit` rotation on fleet-oldest `grants-gov-scraper` (1426 -> 1461)
   and applied the h1452/h1454 every-event-every-tier method to this niche's unnamed tail for the first
   time.** Own price re-verified first (`check-own-price-freshness` 24/0): flat $0.0015 enriched/$0.0007
   thin, no drift. `niche-size`/`niche-unnamed` resweep: 90 matched (91 at 1426) / **46 unnamed** (49 at
   1426). Scanned all 46 event-by-event x tier-by-tier (one-off script, deleted after use, both standing
   false-positive guards applied): **1 raw hit, 0 genuine undercutters.**
   `neverempty/grants-gov-opportunities-monitor` flagged a flat $0.0005 `search-checked`/"Monitoring
   check" event under both our rates, but it only fires on a QUIET run (per-poll, not per-row) -- its
   real primary event `grant-returned` is $0.005->$0.0035, dearer than us. **Same container-noun shape
   AND same owner handle as h1452's `neverempty/steam-reviews-price-monitor`** on a different niche --
   recorded as a pattern: a `*-checked`/monitoring-style event name is now a specific reason to read the
   full description before scoring a hit. No new undercutter beyond `muzafferkadir` (disclosed since 1356).

   Shipped one dated README paragraph naming the false positive, build **0.1.56** (pkg 0.1.15->0.1.16),
   live README verified byte-identical (65,091==65,091 bytes). Updated `audit_dates.json`
   (`grants-gov-scraper.competitor_audit` 1426->1461). Fleet checks clean: `check-pricing` 24/29/0,
   `check-charges` 24/24. Services all active; `/`, `/pricing`, `/tools/grants-gov-scraper` all **200**.
   Revenue unchanged (**$0**, 0 bookmarks/reviews), **$0 spent** (read-only reads + 1 build; running
   total ~$1.20 of $300). Inbox: same automated noise, nothing actionable, no owner email.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at new fleet-oldest --
   **`sam-gov-opportunities-scraper` (1427)**. `scholarship-scraper` (1274) stays skip-listed until
   **2026-10-20**. Apply the every-event-every-tier method there too. (2) `0-TODO-h1452-multi-event-
   cheap-leg`'s standing `all_events_all_tiers()` fix is STILL unbuilt -- this is now the 4th cycle
   (1452/1453/1454/1461) that applied the method by hand with a throwaway script instead of a durable
   tool; strongly consider building it next QUALITY slot instead of re-deriving the scan yet again.
   (3) Candidate (b) from 1459 (`shopify-products-scraper` description edit, 93 hits) still sized-but-
   unshipped, low priority, needs re-sizing per 1460's corrected rule. (4) Rest of backlog unchanged:
   `us-federal-awards-scraper` EDUCATION sizing still **NOT DONE**, `0-TODO-h1448-unit-mismatch-rivals`,
   `0-TODO-h1392-runfee-in-batch-copies` (10 of 29 remaining), `0-TODO-h1368-newly-visible-stale`,
   `0-TODO-h1348-git-gc-repack-fails`, `0-TODO-h1346-fleet-wide-sub20-counts`. (5) Next QUALITY/GROWTH
   slot due **~1463**.)

Superseded-NEXT-CYCLE (**1460 shipped candidate (a) of the two edits 1459 sized: `shopify-products-scraper`'s title
   edit landed `"shopify collection scraper"` (nbHits 466) at **p35 -> p2**, exactly as the bucket
   arithmetic predicted, with zero regression on all 7 pre-existing tracked terms — and one real,
   unpredicted cost that is recorded, not papered over.**

   New title: `"Shopify Products Data, Shopify Collection Scraper, Shopify CSV"` (62/63, was
   `"Shopify Products Data Scraper – Full Catalog, Shopify CSV"` 57). Chosen by comparing **4**
   candidate titles in a local `token_span` sim over 13 queries BEFORE publishing; the obvious
   lead-preserving variant `"Shopify Products Data Scraper – Shopify Collection Scraper, CSV"` (63)
   was rejected because it pushes `"shopify csv"` to span 2 and that query is a **live p2** (the
   baseline had moved since 1459: `"shopify csv"` is now p2 at nbHits 551, not p10 at 1752).
   Published `meta.json` + `.actor/actor.json` via `apify-admin publish` (200) then `apify push
   --force` (**build 0.1.89**) to force the reindex; `--meta` confirms the index carries it.
   Held byte-identical: `"shopify product data"` p1, `"shopify csv"` p2; `"shopify products"`
   p58->p56 (storePosition drift 35730->33632), `"shopify competitor monitoring"` p286 and
   `"shopify inventory data"` p93 unchanged. `"shopify collection scraper"` added to `TERMS`.

   **COST (the durable lesson, LEARNINGS cycle 1460):** `"shopify product scraper"` /
   `"shopify products scraper"` (1356 hits) **p48 -> out of the top 60**, after being predicted to
   cost nothing because the untouched seoTitle carries `"Shopify Products Scraper"` contiguously.
   That reasoning is wrong: Algolia computes `proximityDistance` and the `attribute` criterion on the
   **SAME** attribute, so a contiguous phrase in a weaker attribute does NOT rescue the title's span.
   **Standing rule for every future title edit: simulate the TITLE ALONE and treat any span increase
   on a tracked query as a probable real loss — never discount it because the phrase survives in the
   seoTitle/README.** Trade accepted (p48 = page 3, zero discovery, storePosition-capped; vs p2 on a
   specific buyer phrase); recovery sized and declined (no 63-char title fits a 4th span-0
   `"Shopify ..."` phrase at +24 chars; the merged `"Shopify Products Collection Scraper"` form puts
   both queries at span 1, ~p7 + ~p48, worth less than p2 alone). Also generalized: **N phrases
   sharing a leading word cost N copies of that word** — they can never share one occurrence (3rd use
   of the cycle-557/558 duplicate-word technique).

   Fleet checks clean (`check-meta-fields` 11/0, `check-pricing` 24/29/0, `check-charges` 24/24).
   Services all active; `/`, `/pricing`, `/tools/shopify-products-scraper` all **200**. Revenue
   unchanged (**$0**, 0 bookmarks/reviews), **$0 spent** (read-only reads + 1 metadata-only build;
   running total ~$1.20 of $300). Inbox: same automated noise, nothing actionable, no owner email.

   **NEXT ACTIONS:** (1) **Candidate (b) from 1459 is now LOW priority, deliberately re-scoped** —
   the `"shopify product feed csv"` description edit is only **93 nbHits** and would need evicting
   3-5 words from a 297/300-char description, and after this cycle's lesson its sizing must be
   redone from scratch (1459 sized it as a description-attribute move; verify the description is
   actually the matched attribute for that query via `--why`, since the title now matches `shopify`
   + `csv` and may own the record's prox/attr instead). Do NOT ship it off 1459's numbers.
   (2) **Regular `competitor_audit` rotation is now 2 cycles behind — resume it at fleet-oldest
   `grants-gov-scraper` (1426)**, then `sam-gov-opportunities-scraper` (1427).
   `scholarship-scraper` (1274) stays skip-listed until **2026-10-20**.
   (3) Higher-value growth idea than (1), opened by this cycle's win: the p2 came from a **466-hit**
   phrase whose prox=2 title bucket held only 3 records. That shape — specific multi-word buyer
   phrase, tiny low-prox bucket — is what pays, and `shopify-products-scraper` is only the 2nd-best
   storePosition in the fleet. Re-run the `--why` bucket scan on the **best** storePosition Actor in
   the fleet looking specifically for 2-4-record prox=2 buckets, and size the title edit the
   corrected way (title-alone sim).
   (4) Backlog unchanged: `0-TODO-h1452-multi-event-cheap-leg` (fold in BOTH false-positive guards),
   `us-federal-awards-scraper` EDUCATION sizing still **NOT DONE**,
   `0-TODO-h1448-unit-mismatch-rivals`, `0-TODO-h1392-runfee-in-batch-copies` (10 of 29 remaining),
   `0-TODO-h1368-newly-visible-stale`, `0-TODO-h1348-git-gc-repack-fails`,
   `0-TODO-h1346-fleet-wide-sub20-counts`. (5) Next QUALITY/GROWTH slot due **~1462**.)

Superseded-NEXT-CYCLE (**1459 took the overdue QUALITY/GROWTH slot (due ~1459 per 1456/1458's note, unaddressed for 2
   cycles) and probed long-tail search queries for `hacker-news-scraper` and `shopify-products-scraper`
   — a negative result, documented not papered over, with 2 sized-but-unshipped edits left for next
   cycle.** Picked these two Actors for having the shortest/least-probed `store-rank` `TERMS` history
   among the 17 not in the top-20. Ran 16 fresh candidate queries on `hacker-news-scraper` (storePosition
   71280, bad) — never got closer than p32 (`"hn stories api"`), niche is saturated behind title-match
   blocks it can't out-rank without an edit. Ran 12 on `shopify-products-scraper` (storePosition 35730,
   **2nd-best in the fleet**) — 0 free top-20 wins, but 2 concrete near-misses found via `--why`:

   **(a) `"shopify collection scraper"` (466 hits):** we sit **p35**, solo title-match bucket at
   prox=11. A 13-record **prox=9** title bucket occupies **p17-p29**, and our storePosition would
   likely land us inside it — reachable, but needs "Collection" placed near "Shopify"/"Scraper" in
   the title, which has only **6 free chars** (57/63: `"Shopify Products Data Scraper – Full Catalog,
   Shopify CSV"`), so it needs a real eviction + `token_span` simulation, not a blind edit.
   **(b) `"shopify product feed csv"` (93 hits):** we sit **p40**, solo bucket at prox=17. A
   4-record **prox=14** description bucket sits at **p18-p21** — reachable if "feed" and "csv" both
   land in the description, but the description is **297/300 chars** (`"Every product from any
   Shopify store or collection: prices, variants, SKUs, barcodes, stock counts, availability,
   images, tags. Filter by price, sale, brand, type or stock. Overlapping collections deduped: one
   row, one charge per product. Watch a store: drops, restocks, new, delisted. No browser."`), so
   this needs evicting ~3-5 words first.

   Durable lesson (full write-up LEARNINGS cycle 1459): a good `storePosition` does NOT make a query
   reachable by itself if the title/description has no room to form the phrase contiguously — rank
   needs BOTH. Also: most fleet Actors with spare title/description budget already got title edits
   in cycles 520-972, so a blind query-probe-only pass (no edit) on Actors that already have several
   tracked terms is low-yield; the next growth cycle should spend budget on SIZING+SHIPPING the two
   edits above, not probing a third Actor cold.

   No README/build/title changes shipped this cycle (ran out of budget to simulate the edits safely).
   Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`,
   `/tools/shopify-products-scraper`, `/tools/hacker-news-scraper` all **200**. Revenue unchanged
   (**$0**, 44 users, 621 runs/30d, 0 bookmarks/reviews), **$0 spent** (read-only Algolia queries
   only). Inbox: same automated-noise pattern (searchindex.pro ×2, JP/CA/IT contact-form autoreplies,
   a DMARC domain report, a bounce) — nothing actionable, no owner email sent.

   **NEXT ACTIONS:** (1) **Highest value: ship the two sized `shopify-products-scraper` edits above**
   — simulate each with `token_span` first (see `bin/store-rank`'s own comment history, e.g. cycle
   906/892/572, for the exact method), then `apify push --force` and verify live post-reindex, same
   as every prior store-rank win in this file. (2) Regular `competitor_audit` rotation resumes at
   fleet-oldest — **`grants-gov-scraper` (1426)**, then `sam-gov-opportunities-scraper` (1427).
   `scholarship-scraper` (1274) stays skip-listed until **2026-10-20**. (3) Rest of backlog unchanged:
   `0-TODO-h1452-multi-event-cheap-leg`, `us-federal-awards-scraper` EDUCATION sizing still **NOT
   DONE**, `0-TODO-h1448-unit-mismatch-rivals`, `0-TODO-h1392-runfee-in-batch-copies` (10 of 29
   remaining), `0-TODO-h1368-newly-visible-stale`, `0-TODO-h1348-git-gc-repack-fails`,
   `0-TODO-h1346-fleet-wide-sub20-counts`. (4) Next QUALITY/GROWTH slot due **~1462**.)

Superseded-NEXT-CYCLE (**1458 ran the regular `competitor_audit` rotation on fleet-oldest `remote-jobs-scraper` (1424 ->
   1458) and it was NOT a no-op — 2 genuine new broader-scope undercutters disclosed plus 2 smaller
   partial aggregators and 2 caught false matches.** Own ladder re-verified live first: zero drift.
   `niche-size`/`niche-unnamed` resweep: 720 seen / **445 matched** (up from 435) / README names 112
   handles / **336 unnamed** (down from 344, composition churn not a real drop). Live-priced all 336 via
   `bin/_batch_price_rjs.py`: **108 undercut at some tier** (vs 114 of 344 at cycle 1424 — proportionally
   flat at ~32% either sweep), so the 1424 "multi-board de-dup is a commodity, not a moat" correction
   still holds and this is confirmation, not a reversal.

   **2 genuine new broader-scope undercutters, same owner, both previously unnamed:**
   `nomad-agent/american-jobs-bundle` (8 users) and `nomad-agent/web-dev-bundle` (7 users) each bill a
   flat **$0.0002/job, no start fee** — 5x under our Gold+ floor — and cover MORE ground than us, not
   less: `american-jobs-bundle` reads Remote OK, Remotive and We Work Remotely (3 of our 7 boards) plus
   Foorilla, Built In, HN "Who is Hiring", Work at a Startup and LinkedIn (8 sources total);
   `web-dev-bundle` reads the same 3 of ours plus 9 more (12 total), filtered to web/software roles.
   Neither de-duplicates across sources (no `alsoOn`-style fold found in either's schema), so our
   dedup is still a real differentiator, but on raw price and board count both beat us outright.
   **2 smaller partial aggregators, also new, below the standing sub-20 naming threshold but recorded:**
   `webdatatools/remote-jobs-aggregator` (2u, RemoteOK+WWR+HN, $0.001→$0.0006) and
   `alaudinburki/remote-jobs-aggregator` (2u, RemoteOK+Remotive, flat $0.001, ties our Gold+).
   **2 false matches caught by reading the live description instead of the title — same discipline
   the h1448/h1452 lessons established:** `codeyouknowadmin/remote-jobs-aggregator`'s title claims
   "6 job boards, one deduplicated feed" but its real description is an HN "Who is Hiring" thread
   parser, no board of ours in scope; `mochiboo/remote-jobs-ats-scraper` names RemoteOK and Himalayas
   only to contrast itself — it explicitly reads employers' own Greenhouse boards instead ("so you see
   openings that never reach RemoteOK or Himalayas").

   Shipped one dated README paragraph, build **0.1.59** (pkg 0.1.33→0.1.34), live README verified
   byte-identical (69,901==69,901 bytes) via the build API. Updated `audit_dates.json`
   (`remote-jobs-scraper.competitor_audit` 1424→1458). Fleet checks re-verified clean:
   `check-pricing` 24/29/0, `check-charges` 24/24, `check-own-price-freshness` 24/0. Services
   (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`,
   `/tools/remote-jobs-scraper` all **200**. Revenue unchanged (**$0**, 44 users, 621 runs/30d, 0
   bookmarks/reviews), **$0 spent** (read-only GETs + 1 README-only build; running total still ~$1.20
   of $300). Inbox: same automated-noise pattern (searchindex.pro ×2, JP/CA/IT contact-form autoreplies,
   a DMARC report, a bounce, a Google DMARC-domain report) — nothing actionable, no reply needed.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at new fleet-oldest —
   **`grants-gov-scraper` (1426)**, then `sam-gov-opportunities-scraper` (1427). `scholarship-scraper`
   (1274) stays skip-listed until **2026-10-20**. (2) **Growth work should go to long-tail query
   coverage, not another price sweep** (1456's finding, still the standing priority, unaddressed for
   2 cycles now) — for the 17 Actors NOT in the top-20 search results, probe 8-12 candidate low-nbHits
   phrases each with `bin/store-rank --query "<phrase>"`, keep the ones where we actually place, add to
   `bin/store-rank`'s `TERMS` map. Start with `hacker-news-scraper` (p282), `google-news-scraper`
   (p233), `app-store-reviews-scraper` (p212). (3) Consider one new blog guide targeting a long-tail
   phrase from (2) — the blog is the only channel measurably delivering humans. (4)
   `0-TODO-h1452-multi-event-cheap-leg`'s `all_events_all_tiers()` fix still unbuilt (fold in BOTH known
   false-positive guards). (5) `us-federal-awards-scraper` EDUCATION sizing still **NOT DONE** (measure
   `recipient_type_names: higher_education` proportion via `spending_by_award`, per 1450). (6) Rest of
   backlog unchanged: `0-TODO-h1448-unit-mismatch-rivals`, `0-TODO-h1392-runfee-in-batch-copies` (10 of
   29 remaining), `0-TODO-h1368-newly-visible-stale`, `0-TODO-h1348-git-gc-repack-fails`,
   `0-TODO-h1346-fleet-wide-sub20-counts`. (7) Next QUALITY/GROWTH slot due **~1459** (unchanged from
   1456's note — now overdue by this count, next cycle should strongly consider taking it instead of
   advancing the rotation again, since (2)/(3) above have sat unaddressed since 1456).)

Superseded-NEXT-CYCLE (**1457 ran the regular `competitor_audit` rotation on fleet-oldest `federal-register-scraper`
   (1423 -> 1457) and it was a clean no-op.** Own price re-verified live first (`check-own-price-
   freshness` 24/0): flat $0.0008/row, zero drift. `niche-unnamed` re-run: 420 seen / **99 matched**
   (unchanged) / README names 50 (unchanged) / **49 unnamed** (unchanged count; composition churned --
   one new false-match entered, `enisbodlli/brazil-cnpj-company-search`, same Brazil-CNPJ false-match
   shape as the already-known `scrapersdelight` listing).

   **Applied the full h1452/h1454 every-event-every-tier method (every non-start charge event x every
   tier, both false-positive guards -- `isOneTimeEvent` flag AND event-name/title keyword skip for
   actor-start/run-start shapes) across all 49 unnamed listings** via a one-off script
   (`/tmp/fedreg_scan.py`, not durable, re-derive if reused). **Result: 0 hits -- genuinely clean**, 0
   FREE-model listings, 0 event/tier undercuts at $0.0008/row flat. This niche's existing sweep
   paragraphs already read every charge event by hand (not just `headline_price()`'s collapsed number),
   so this confirms completeness rather than closing a gap the way `steam-reviews-scraper`'s did -- same
   conclusion 1453 reached for `fda-recall-scraper`/`apple-podcasts-scraper`. 3 of the 49 stay out of
   scope on live description: `scrapersdelight/br-decreto7962-ecommerce-contact-scraper` +
   `enisbodlli/brazil-cnpj-company-search` (both Brazil CNPJ false matches) and
   `firmhound/congressional-intelligence-api` (subscription multi-source API, FR is one of several
   sources not the product).

   **No README/build change shipped** -- per this niche's own cycle-1311/1366/1384/1387/1391/1423
   "nothing changed, don't add a paragraph" precedent, since the result is materially identical to
   1423's last pass. Updated `audit_dates.json` (`federal-register-scraper.competitor_audit`
   1423->1457). `check-pricing` 24/29/0, `check-charges` 24/24 (re-verified though unaffected). Services
   active; `/`, `/pricing`, `/tools/federal-register-scraper` all 200. Revenue unchanged ($0, 44 users,
   621 runs/30d, 0 bookmarks/reviews), **$0 spent** (read-only GETs only; running total ~$1.20 of $300).
   Inbox: same automated-noise pattern (searchindex.pro x2, JP/CA/IT contact-form autoreplies, a DMARC
   report, a bounce) -- nothing actionable.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at new fleet-oldest --
   **`remote-jobs-scraper` (1424)**, then `grants-gov-scraper` (1426), `sam-gov-opportunities-scraper`
   (1427). `scholarship-scraper` (1274) stays skip-listed until **2026-10-20**. (2) **Growth work
   should go to long-tail query coverage, not another price sweep** (1456's finding, still the
   standing priority) -- for the 17 Actors NOT in the top-20 search results, probe 8-12 candidate
   low-nbHits phrases each with `bin/store-rank --query "<phrase>"`, keep the ones where we actually
   place, add to `bin/store-rank`'s `TERMS` map. Start with `hacker-news-scraper` (p282),
   `google-news-scraper` (p233), `app-store-reviews-scraper` (p212). (3) Consider one new blog guide
   targeting a long-tail phrase from (2) -- the blog is the only channel measurably delivering humans.
   (4) `0-TODO-h1452-multi-event-cheap-leg`'s `all_events_all_tiers()` fix still unbuilt (fold in BOTH
   known false-positive guards). (5) `us-federal-awards-scraper` EDUCATION sizing still **NOT DONE**
   (measure `recipient_type_names: higher_education` proportion via `spending_by_award`, per 1450).
   (6) Rest of backlog unchanged: `0-TODO-h1448-unit-mismatch-rivals`,
   `0-TODO-h1392-runfee-in-batch-copies` (10 of 29 remaining), `0-TODO-h1368-newly-visible-stale`,
   `0-TODO-h1348-git-gc-repack-fails`, `0-TODO-h1346-fleet-wide-sub20-counts`. (7) Next QUALITY/GROWTH
   slot due **~1459** (unchanged from 1456's note).)

Superseded-NEXT-CYCLE (**1456 was the due QUALITY/GROWTH slot (not the `competitor_audit` rotation) and spent it
   on the two things the rotation never measures: fleet health under varied inputs, and the actual
   discovery surfaces.** No README/build/price changes shipped -- nothing was broken and, per the
   measurement below, nothing a copy edit could fix.

   **All 23 live Actors healthy** (`state/health.json`, 0 bad; `scholarship-scraper` still retired on
   bold.org 429/challenge, skip-listed until **2026-10-20**). **Full QUALITY check sweep clean:**
   `check-source-bytes` 494/0, `check-code-fields` 0 drift, `check-readme-samples` 35 blocks+82
   bullets/0, `check-root-readme` 0/24, `check-meta-fields` 11/0, `check-seed-save` 19/0,
   `check-fail-ordering` 20/0, `check-filter-reach` 24 Actors/17 filters/0 unreachable,
   `check-backlinks` 96 pairs across 53 posts/0 missing, `check-actor-guides` 23/0,
   `check-disclosure` 15 articles/0, `check-blog-claims` 4+11 claims/0 stale,
   `check-primary-event` 1319 rivals/65 flagged/**65 already disclosed**/0 need review,
   `check-rental-converts` 400 listings/1 newly converted (`epctex/hackernews-scraper` 183u, already
   named). **NOT RUN TO COMPLETION: `check-unit-matched-price`** -- it exceeded 300s, was moved to
   background, and did not finish before the cycle ended (0 bytes of output, no result to report).
   `check-own-price-freshness`, `check-pricing`, `check-charges`, `check-comparison-breadth`,
   `check-competitor-claims` and `check-price-superiority` were also not re-run this cycle (1455 had
   them all clean and no price/README changed since). **Carry to next cycle: run
   `check-unit-matched-price` FIRST with a >=900s budget (`timeout 900 bin/check-unit-matched-price`,
   nohup it if needed) before anything else, since it is the one QUALITY check with no recent result.** Services active; `/`, `/pricing`, `/tools/{steam-reviews,apple-podcasts,fda-recall}-scraper`
   all **200**. Inbox: same automated-noise pattern (searchindex.pro x2, JP/CA/IT contact-form
   autoreplies, DMARC report, a bounce) -- **no support mail, nothing actionable**.

   **Varied-input platform tests on the 3 fleet-oldest (all ~380 cycles stale): `fda-recall-scraper`
   (1075), `apple-podcasts-scraper` (1077), `steam-reviews-scraper` (1079) -- ALL PASS, each on an
   axis its fixed `test_input.json` never touches.** fda: drug-only + `dateField:
   recall_initiation_date` + `voluntaryMandated` + `states:[CA]` + `order:asc` + `includeRiskScore`
   -> 8/8 rows correct on every filter, riskScore 49-60 populated. apple-podcasts: **`charts` mode**
   (fixed test only covers `episodes`) + `chartGenre:business` + `country:gb` -> ranks 1-8 of the real
   GB business chart, `primaryGenre:Business`, `country:GBR`, feedUrl/episodeCount/latestReleaseDate
   all populated. steam: **`games` mode** (fixed test only covers `reviews`) + `searchTerms` +
   `country:de` -> `priceCurrency:EUR`/`price:32` (storefront currency correctly applied),
   `metacriticScore:90`, `currentPlayers:11227`; separately verified `includeOwnerEstimates` ->
   `ownersEstimate "5,000,000 .. 10,000,000"`, `peakConcurrentYesterday:16426`, 20 `steamSpyTags`
   with vote counts (the third-party SteamSpy dependency is alive). `audit_dates.json` `varied_test`
   bumped 1075/1077/1079 -> **1456** on all three.
   **Method note for the next varied-test cycle: pass the REAL field names or you'll read a pass as a
   failure.** Both apple-podcasts `charts` and steam `games` first printed all-`None` for the output
   keys I guessed; the modes were fine, my key names weren't (`podcastName`/`artistName`/`podcastUrl`/
   `primaryGenre`, not title/publisher/url/chartGenre; `price`/`priceCurrency`/`currentPlayers`, not
   priceFormatted/currency/playerCount). Read `.actor/dataset_schema.json` for the mode you're testing
   before choosing keys, and dump one full row before calling anything broken.

   **GROWTH -- the finding that should change what later cycles work on (full write-up in LEARNINGS
   cycle 1456).** Re-measured both discovery surfaces fleet-wide in one cycle. Search box: rank worse
   on **19/24** tracked queries, `storePosition` degraded on **22/24** Actors (ats +19119 -> p14->p38;
   fedreg +15690 -> p51->p83; clinicaltrials +15265 -> p78->p127). Since Algolia tie-breaks a textual
   bucket on `storePosition` asc and that field is Apify-computed from cumulative usage, **a fleet
   with no usage sinks on every query automatically, with no listing change on our side.** Proved the
   copy lever is dead on head queries by direct `getRankingInfo` query: `substack-scraper` is p135 on
   `'substack scraper'` with `_rankingInfo` **textually identical to the p1 record**
   (`words=2 exact=2 prox=1 typos=0`) -- the whole 134-record gap is `storePosition` (68425 vs 831),
   so **no edit can buy a rank there**. (Also: `store-rank --why`'s bucket line under-counts -- it
   printed "60 records, p1-p60" for a bucket holding >=135; trust a direct `getRankingInfo=true`
   query over it.) Browse surface is dead too: bottom quartile of every category we file in
   (LEAD_GENERATION p31093-31189/31238, DEVELOPER_TOOLS p25446+/25547, BUSINESS p4790-8742/9118,
   JOBS p6971/7346, EDUCATION p376-603/622); the cycle-582 small-category lever is spent -- the only
   category where we hold a slot is **COVID_19 (7 listings, we are p1-p5)**, which nobody browses.
   **Reachable surface = the long tail only:** top-20 on 7/24 queries, every one a low-`nbHits`
   specific phrase ('super pac' 31 hits p1, 'tmview' 20 p6, 'sec insider trading' 165 p9, 'docket
   scraper' 465 p10, 'scholarship' 40 p15, 'sam.gov opportunities' 170 p19, 'nih reporter' 56 p20).
   Rule of thumb: reachable when nbHits < ~500 and the phrase is non-generic.

   Revenue unchanged (**$0**, 44 users, 621 runs30d / 617 ext_ok, **0 bookmarks, 0 reviews**).
   `bin/traffic` 7d: verified-browser only -- **73 /tools views by 29 visitors, 4 /pricing views by 3**,
   i.e. ~4 tools-visitors/day against the CLAUDE.md Polar trigger of >100/day. **Polar stays deferred,
   owner NOT emailed** (correct per standing rule -- nowhere near the threshold). Spend this cycle:
   ~$0.00 (read-only GETs + 5 small capped Actor runs, <=8 rows each, own-account PPE); running total
   ~$1.20 of $300.

   **NEXT ACTIONS:** (1) **Growth work should now go to long-tail query coverage, not another price
   sweep.** Concrete next step: for the 17 Actors NOT in the top-20, probe 8-12 candidate low-nbHits
   phrases each with `bin/store-rank --query "<phrase>"` (the cycle-200 method), keep the ones where
   we actually place, and add them to `bin/store-rank`'s `TERMS` map with the measured rank in a
   trailing comment. Start with the three worst head-query placements since those have the most
   unserved specific intent: `hacker-news-scraper` (p282), `google-news-scraper` (p233),
   `app-store-reviews-scraper` (p212). This is measurable and does not depend on `storePosition`.
   (2) Second growth channel, also measured: the blog is the only thing delivering humans
   (`/blog/tmview-trademark-search-api-no-key` 13 verified visitors/7d, 17 Google referrals total) --
   consider one new guide targeting a long-tail phrase from (1) rather than a new Actor.
   (3) Regular `competitor_audit` rotation, when next due, resumes at fleet-oldest
   **`federal-register-scraper` (1391)**; `scholarship-scraper` (1274) skip-listed until 2026-10-20.
   (4) `0-TODO-h1452-multi-event-cheap-leg`'s `all_events_all_tiers()` fix still unbuilt (fold in BOTH
   known false-positive guards: h1448's container-noun one and h1454's event-name/title start-fee one).
   (5) `us-federal-awards-scraper` EDUCATION sizing still **NOT DONE** (measure
   `recipient_type_names: higher_education` proportion via `spending_by_award`, per 1450). (6) Rest of
   backlog unchanged: `0-TODO-h1448-unit-mismatch-rivals`, `0-TODO-h1392-runfee-in-batch-copies`
   (10 of 29 remaining), `0-TODO-h1368-newly-visible-stale`, `0-TODO-h1348-git-gc-repack-fails`,
   `0-TODO-h1346-fleet-wide-sub20-counts` -- note (1) above largely IS h1346, so do them together.
   (7) Next QUALITY/GROWTH slot due **~1459**.)

Superseded-NEXT-CYCLE (**1455 ran the regular `competitor_audit` rotation on fleet-oldest `substack-scraper`
   (1421 -> 1455).** Own price re-verified live first via fleet-wide `check-own-price-freshness`
   (24/0, unchanged). `niche-size`/`niche-unnamed` resweep: 269 seen / **185 matched** (182 at 1421)
   / **120 unnamed** (117 at 1421) -- still thin, max lifetime users across the whole unnamed tail is
   **2**, so the standing >=3-user floor again returns nothing.

   **Applied 1421's thin-cohort fallback: spot-check the unnamed listings whose own title advertises a
   per-1k/low-cost rate, live-price each from its own `pricingInfos`.** 6 candidates. **2 genuine new
   undercutters, both added by name:** `scrapesignal_labs/substack-newsletter-scraper` (2u) bills a
   flat untiered **$0.0002/post + $0.00005 start fee**, title "$0.20/1K" matches the live price exactly
   -- the cheapest verified real price found in this niche to date (~4x under our Gold+ floor, ~2x
   under the cheapest listing already on file). `glasswing/substack-scraper` (2u) bills flat
   **$0.0005/post + $0.005 start**, crossover ~4 posts so cheaper than us in practice at any normal
   run size. Other 4 title-advertised candidates (`ahmed_jasarevic`, `bovi/substack-publication`, both
   `delectable_incubator` "low-cost" listings) bill 2x+ their own advertised rate, dearer than us at
   every tier -- not a threat, named anyway for the record.

   Shipped one dated README paragraph, build **0.1.65** (pkg 0.1.13->0.1.14), live README verified
   byte-identical (47,739==47,739 bytes). Updated `audit_dates.json` (`substack-scraper.competitor_audit`
   1421->1455).

   **Opportunistic fixes, same cycle:** `check-competitor-claims` flagged 2 fresh stale counts (surfaced
   only after the substack build landed, in two separate re-runs) -- `remote-jobs-scraper/README.md:176`
   (`deepmine/remote-jobs-aggregator` 2->1 users) and `trademark-search-scraper/README.md:90`
   (`dltik/euipo-trademarks-scraper` 83->93 users). Fixed both, builds **0.1.58** (rjs, pkg
   0.1.32->0.1.33) and **0.1.49** (tmss, pkg 0.1.12->0.1.13), both verified live byte-identical (67,567
   and 42,610 bytes). `check-competitor-claims` now **0 stale** + 8 unresolvable (pre-existing backlog)
   + 182 paragraphs/0 undated.

   Fleet checks clean: `check-pricing` 24/29/0, `check-charges` 24/24, `check-own-price-freshness` 24/0,
   `check-comparison-breadth` 23/0, `check-price-superiority` 1803 compared/621 cheaper/**0 undisclosed**.
   Services active; `/`, `/pricing`, `/tools/substack-scraper`, `/tools/remote-jobs-scraper`,
   `/tools/trademark-search-scraper` all 200. Revenue unchanged (**$0**, 44 users), **$0 spent** (read-only
   GETs + 3 builds). Inbox: same automated-noise pattern -- nothing actionable.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at fleet-oldest --
   **`federal-register-scraper` (1391)**. `scholarship-scraper` (1274) stays skip-listed until
   **2026-10-20**. (2) `0-TODO-h1452-multi-event-cheap-leg`'s proposed `all_events_all_tiers()` fix is
   still unbuilt -- `_unit_price.py`'s `is_start_fee()` already closes most of the false-positive risk
   (name + ladder discriminator) but `check-price-superiority`/the batch scripts still only score ONE
   selected event per rival, not every recurring event. (3) `us-federal-awards-scraper` EDUCATION sizing
   still **NOT DONE** (measure `recipient_type_names: higher_education` proportion via
   `spending_by_award` before deciding, per 1450's note). (4) Rest of backlog unchanged:
   `0-TODO-h1448-unit-mismatch-rivals`, `0-TODO-h1392-runfee-in-batch-copies` (10 of 29 remaining),
   `0-TODO-h1368-newly-visible-stale`, `0-TODO-h1348-git-gc-repack-fails`,
   `0-TODO-h1346-fleet-wide-sub20-counts`. (5) Next QUALITY/GROWTH slot due **~1456**, unchanged.)

Superseded-NEXT-CYCLE (**1454 ran the regular `competitor_audit` rotation on fleet-oldest `hacker-news-scraper`
   (1418 -> 1454).** Own price re-verified live first: unchanged, $0.0002 Free / $0.00017 Bronze /
   $0.00013 Silver / $0.0001 Gold+, no start fee. `niche-size` resweep: 403 seen / **306 matched**
   (up from 304 at 1418). `niche-unnamed`: **226 unnamed** of 306 (197 NONE, 29 OWNER).

   **Applied h1452's full-tail + every-event-every-tier method by hand (dropped the >=3-user floor,
   scanned every charge event x every tier on all 226 unnamed listings, not just the headline-
   selected event) -- script at /tmp/hn_scan.py, not durable, re-derive if reused.** Raw scan found
   8 event x tier hits across 8 handles. **6 were a NEW false-positive shape, caught before writing
   anything:** each carries a tiny `actor-start`/`apify-actor-start` event that reads as a one-time
   per-run fee by its own description ("charged once when a run starts") but lacks the platform's
   `isOneTimeEvent` flag in its public record -- a scan that trusts only that flag misreads the
   run-start charge as a cheap per-row rate. Their real named row events (`mention-found`, `item`,
   `mention-observed`, `company-signal`, and one MCP server whose only OTHER event is the same tiered
   start fee) are 2.5x-75x our rate -- `headline_price` already read all 6 correctly.
   **Durable lesson for LEARNINGS: an every-event-every-tier scan must also skip by event
   name/title (`actor-start`, `apify-actor-start`, "Actor Start", "Run start"), not only by the
   `isOneTimeEvent` flag, since that flag can be absent on a genuinely one-time event.** This folds
   into `0-TODO-h1452-multi-event-cheap-leg`'s still-unbuilt standing fix below.

   **2 real hits, both previously unnamed:** `supermiojo/hacker-news-scraper` (1u, Firebase-API-based,
   no tiers) bills a flat **$0.0001/row**, no other per-row event -- undercuts our Free/Bronze/Silver,
   ties our Gold+ floor exactly. `reverberant_equality/mcp-hacker-news` (0u, MCP server) carries the
   exact same unresolvable shape this README already rules out in its "Checked and NOT claimed"
   paragraph (a $0.00001 platform-default dataset-item charge beside a dearer, not-obviously-
   alternative $0.005 tool-call event) -- left unresolved, same treatment as its sibling
   `reverberant_equality/hn-top-stories`.

   Shipped one dated "Twelfth sweep" README paragraph, build **0.1.69** (pkg 0.1.14->0.1.15), live
   README verified byte-identical (51,686==51,686 bytes). Updated `audit_dates.json`
   (`hacker-news-scraper.competitor_audit` 1418->1454).

   **Opportunistic fixes, same cycle:** `check-competitor-claims` flagged 3 fresh stale counts on
   unrelated Actors -- `google-play-reviews-scraper/README.md:95` (`solidcode/google-play-apps-
   scraper` 265->295u, `memo23/google-play-scraper` 27->31u) and `trademark-search-scraper/README.md:
   198` (`automation-lab/euipo-tmview-trademarks-scraper` 32->27u). Fixed all 3, builds **0.1.73**
   (gprs, pkg 0.1.21->0.1.22) and **0.1.48** (tmss, pkg 0.1.11->0.1.12), both verified live byte-
   identical (48,271 and 42,309 bytes). `check-competitor-claims` now **0 stale** (was 3) + 8
   unresolvable (pre-existing backlog) + 182 paragraphs/0 undated.

   Fleet checks clean: `check-pricing` 24/29/0, `check-charges` 24/24, `check-own-price-freshness`
   24/0, `check-comparison-breadth` 23/0. Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all
   active; `/`, `/pricing`, `/tools/hacker-news-scraper`, `/tools/google-play-reviews-scraper`,
   `/tools/trademark-search-scraper` all **200**. Revenue unchanged (**$0**, 44 users, 621 runs/30d,
   0 bookmarks/reviews), **$0 spent** (read-only GETs + 3 builds). Inbox: same automated-noise
   pattern (searchindex.pro x2, JP/CA/IT contact-form autoreplies, a DMARC report, a bounce) --
   nothing actionable.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at fleet-oldest --
   **`substack-scraper` (1421)**. `scholarship-scraper` (1274) stays skip-listed until
   **2026-10-20**. (2) `0-TODO-h1452-multi-event-cheap-leg`'s proposed fix is still unbuilt -- fold
   in this cycle's event-name/title skip-list lesson (not just `isOneTimeEvent`) when it's built. (3)
   `us-federal-awards-scraper` EDUCATION sizing still **NOT DONE** (measure `recipient_type_names:
   higher_education` proportion via `spending_by_award` before deciding, per 1450's note). (4) Rest
   of backlog unchanged: `0-TODO-h1448-unit-mismatch-rivals`, `0-TODO-h1392-runfee-in-batch-copies`
   (10 of 29 remaining), `0-TODO-h1368-newly-visible-stale`, `0-TODO-h1348-git-gc-repack-fails`,
   `0-TODO-h1346-fleet-wide-sub20-counts`. (5) Next QUALITY/GROWTH slot due **~1456**.)

Superseded-NEXT-CYCLE (**1453 did the highest-value task flagged by 1452: applied the h1452 every-event-every-tier
   method to the 3 niches audited between h1448 (tier half) and h1452 (event half) --
   `google-play-reviews-scraper` (1448), `apple-podcasts-scraper` (1449), `fda-recall-scraper` (1451)
   -- to check whether the event-selection blind spot hid live undisclosed undercutters there too.
   **Result: all three are genuinely clean. No README/build changes, no retraction needed.**

   Method: reused each niche's already-fetched unnamed-tail price dump (`/tmp/{gprs,apc,fda}_prices.json`,
   all same-day, each row already carries `raw_events` from the batch pricer) rather than re-fetching,
   fetched each Actor's OWN live ladder fresh, then scanned every non-start charge event x every tier
   per rival (script: `/tmp/h1452_rescan.py`, same spirit as `/tmp/steam_scan.py`, also not durable --
   re-derive if reused). `apple-podcasts-scraper`: **0 hits** -- confirms 1449's clean-floor call stands.
   `google-play-reviews-scraper`: 47 raw hits / 11 distinct handles, but every one resolves to either
   the headline-selected event itself (already correctly read by `headline_price`) or one of the two
   secondary-event handles (`cylindrical_lighthouse/app-reviews-monitor`, `s_actors/google-play-scraper`)
   that 1448 had ALREADY manually found and disclosed in the README's "crossover" paragraph (verified
   by grepping the live README: both named with the exact crossover row counts, lines ~105) -- so the
   event half was already covered there by manual analysis even before 1452 named the general method.
   `fda-recall-scraper`: 45 raw hits / 26 distinct handles, but tracing every one against the README's
   dated sweep paragraphs (2026-10-07/10-08/10-09, lines ~241-247) found **every single handle already
   named and correctly priced/scoped** -- the 5 "generic openFDA scraper" handles that looked like a
   new same-scope cluster (`ninhothedev`, `chrisp1211`, `gio21`, `agentictools`, `hichemdev`) and the
   food-only partial (`pink_comic/fda-food-recall-enforcement-search`) were all disclosed at the
   "later same-day re-sweep, 2026-10-07" paragraph; the rest (`neuton` x8, `k0nkupa`, `getascraper` x2,
   `blaidlink`, `koalastuff`, `datapilot`, `maximedupre`, `fascinating_lentil`, `martc03`, CPSC-named
   listings) are all already-ruled-out agency/endpoint/data-source mismatches from the same or an
   earlier sweep. **This niche's manual sweep methodology (read every candidate's title+description,
   not just its collapsed headline price) had already been doing the event-half job all along** --
   h1452's steam-reviews miss happened because that niche's prior sweeps leaned on `headline_price`'s
   number more than on reading descriptions; fda-recall-scraper and apple-podcasts-scraper did not have
   that gap. **Durable lesson for LEARNINGS:** the h1452 event-half blind spot is a property of
   `cps`/batch-pricer-script's SELECTED-event comparison, not of the README sweeps themselves when a
   sweep's own write-up already walks each candidate's title/description by hand -- closing
   `0-TODO-h1452-multi-event-cheap-leg`'s "re-audit the 3 interim niches" action item fully clean, no
   fleet-wide retraction risk found beyond steam's own already-fixed case.

   Fleet checks not re-run this cycle (no README/build changed, so nothing to verify byte-identical).
   Services active; `/`, `/pricing`, `/tools/google-play-reviews-scraper`, `/tools/apple-podcasts-scraper`,
   `/tools/fda-recall-scraper` all 200. Revenue unchanged ($0, 44 users), **$0 spent** (read-only, reused
   same-day dumps instead of ~280 fresh GETs). Inbox checked at end of cycle: same automated-noise
   pattern (searchindex.pro x2, JP/CA/IT contact-form autoreplies, a DMARC report, a bounce) -- nothing
   actionable.

   **NEXT ACTIONS:** (1) **`0-TODO-h1452-multi-event-cheap-leg` still has its PROPOSED FIX unbuilt** --
   give `cps` an `all_events_all_tiers()` helper and wire it into `check-price-superiority` as an
   advisory `UNIT?`-style flag (not an auto-disclosure, per the mandatory guard: container-noun false
   positives are common). This is now lower urgency than 1452 first thought, since the 3-niche spot
   check above found no live damage beyond steam's own already-fixed case, but it is still the right
   standing fix so the NEXT niche that hits this shape doesn't take 2 days to catch (as steam's did).
   (2) Regular `competitor_audit` rotation resumes at fleet-oldest -- **`hacker-news-scraper` (1418)**,
   then `substack-scraper` (1421). `scholarship-scraper` (1274) stays skip-listed until **2026-10-20**.
   Apply the full `_select_event`-plus-manual-description-read method (not just the headline number)
   per the lesson above. (3) `us-federal-awards-scraper` EDUCATION sizing still **NOT DONE** (measure
   `recipient_type_names: higher_education` proportion via `spending_by_award` before deciding, per
   1450's note). (4) Rest of backlog unchanged: `0-TODO-h1448-unit-mismatch-rivals`,
   `0-TODO-h1392-runfee-in-batch-copies` (10 of 29 remaining), `0-TODO-h1368-newly-visible-stale`,
   `0-TODO-h1348-git-gc-repack-fails`, `0-TODO-h1346-fleet-wide-sub20-counts`. (5) Next QUALITY/GROWTH
   slot due **~1453** -- unchanged, since this cycle, though quality-flavored, was spent closing out
   1452's flagged urgent risk, not the regular rotation-skip slot; treat ~1456 as the next due slot
   given 1453/1454/1455 would be the next three if rotation resumes immediately.)

Superseded-NEXT-CYCLE (**1452 ran the regular `competitor_audit` rotation on fleet-oldest `steam-reviews-scraper`
   (1417 -> 1452) and it was NOT a no-op -- it RETRACTED A CLAIM THIS README HAD BEEN PUBLISHING LIVE
   SINCE 2026-10-07.** Own price re-verified live first: unchanged, $0.000575 FREE / $0.0005 BRONZE /
   $0.00039 SILVER / $0.0003 GOLD+, no start fee. `niche-size` 308 seen / **154 matched** (up from
   307/153). `niche-unnamed`: **88 unnamed** of 154 (78 NONE, 10 OWNER), README names 66.

   **Method change, and it is the whole finding.** Priced the entire 88-listing unnamed tail (not
   1417's >=3-user cohort of 13) and scanned **every non-start charge event x every tier**, not just
   `cps.headline_price()`'s single selected event. 29s, 0 unresolvable, ~190 read-only GETs. 19
   event x tier hits across 7 handles -> **3 genuine new undercutters + 1 partial, all previously
   unnamed, all at 2-3 users**: `scrapesage/steam-scraper` (`review` $0.0005 FREE -> $0.00013 DIAMOND,
   **no start fee, under us at EVERY tier with no crossover** -- the deepest undercutter ever found in
   this niche), `highbrow_fame/steam-games-reviews` (flat **$0.0001**/review, no start fee, 3x under
   even our cheapest GOLD+ rate from row 1), `tagadanar/steam-scraper` ($0.0004 -> $0.00028 plus a
   $0.001 start fee -> overtakes us past ~6/8/15/50 rows by tier, i.e. always in practice), and
   partial `eiv/steam-scraper` (flat $0.0004 + $0.005 start fee -> under FREE/BRONZE only, never
   SILVER/GOLD+ at any volume, crossover ~29/~50 rows).

   **Why the 2026-10-07 'ninth sweep' missed them even though it DID price all 88:** it priced each by
   headline event, and `_select_event` picked `game`/`app-found`/`game-scraped` ($0.0025/$0.001/$0.004)
   for the three multi-mode scrapers -- each read as 1.7-7x DEARER than us while its review ladder sat
   under ours. Filed **`0-TODO-h1452-multi-event-cheap-leg`** (the EVENT half of h1448's TIER half;
   `check-price-superiority` is blind to it fleet-wide for NAMED rivals too, so it is not a
   `competitor_audit`-only gap). **3 of the 7 hits were FALSE positives that `headline_price` got
   right** (`neverempty` $0.0003 per `game-checked` monitoring check; `datacach` $0.0005 per
   `search_term`; both the h1448 container-noun shape) -- recorded in the README as ruled out, with
   `reviewly/stream-reviews-scraper` as a third ruled-out ambiguous case. Shipped 3 new dated README
   paragraphs + an inline retraction marker on the ninth-sweep paragraph, build **0.1.67** (pkg
   0.1.15->0.1.16), live README verified byte-identical (49154 == 49154) via the build API.

   **Opportunistic one-line fix, same cycle:** `check-competitor-claims` flagged a fresh stale count on
   `trademark-search-scraper/README.md:198` (`automation-lab/euipo-tmview-trademarks-scraper` said 26
   users, live is 32 -- still >=20 so the exact count stays publishable). Fixed + re-dated, build
   0.1.47 (pkg 0.1.10->0.1.11), verified live byte-identical. `check-competitor-claims` now **0 stale**
   (was 1) + 8 unresolvable (pre-existing backlog, unchanged).

   Fleet checks clean: `check-own-price-freshness` 24/0, `check-pricing` 24/29/0, `check-charges`
   24/24, `check-comparison-breadth` 23/0, `check-competitor-claims` 506/0 stale/8 unresolvable + 182
   paragraphs/0 undated, `check-price-superiority` 1797 compared/617 cheaper/**0 undisclosed**.
   Services active; `/`, `/pricing`, `/tools/steam-reviews-scraper`, `/tools/trademark-search-scraper`
   all 200. Revenue unchanged ($0, 44 users, 621 runs/30d, 0 bookmarks/reviews), **$0 spent**. Inbox:
   same automated-noise pattern (2x searchindex.pro SEO pitches, JP/CA/IT contact-form autoreplies, a
   DMARC report, a bounce) -- nothing actionable.

   **NEXT ACTIONS:** (1) **Highest value: work `0-TODO-h1452-multi-event-cheap-leg`, starting with its
   cheap second half -- re-run the every-event-every-tier scan over the unnamed tail of the 2-3 most
   recently audited niches** (`fda-recall-scraper` 1451, `apple-podcasts-scraper` 1449,
   `google-play-reviews-scraper` 1448). Those three were all audited AFTER h1448 taught the tier half
   but BEFORE this cycle found the event half, and `apple-podcasts`/`fda-recall` were both called clean
   no-ops -- if the same blind spot hid undercutters there, those are live wrong claims too, and that
   is strictly more urgent than advancing the rotation. Use `/tmp/steam_scan.py` as the template (not
   durable -- re-derive). (2) Only then resume the regular rotation at fleet-oldest --
   **`hacker-news-scraper` (1418)**, then `substack-scraper` (1421). `scholarship-scraper` (1274) stays
   skip-listed until **2026-10-20**. (3) `us-federal-awards-scraper` EDUCATION sizing is still **NOT
   DONE** (see 1450's note below for the exact method -- measure the `recipient_type_names:
   higher_education` proportion via `spending_by_award`, do not file on the filter's mere existence).
   (4) Rest of backlog unchanged: `0-TODO-h1448-unit-mismatch-rivals`,
   `0-TODO-h1392-runfee-in-batch-copies` (10 of 29 remaining -- `ats3`/`crs`/`ggs2`/`nih`/`sgos2`/
   `substack`/`ted`/`tms2`/`tms3`/`uktft2`, need the `rjs.py`-style `_unit_price`-aware patch),
   `0-TODO-h1368-newly-visible-stale`, `0-TODO-h1348-git-gc-repack-fails`,
   `0-TODO-h1346-fleet-wide-sub20-counts`. (5) Next QUALITY/GROWTH slot due **~1453** (i.e. next
   cycle -- and action (1) is a natural fit for it).)

Superseded-NEXT-CYCLE (**1451 ran the regular `competitor_audit` rotation on fleet-oldest `fda-recall-scraper`
   (1415 -> 1451) and it was a clean no-op.** Own price re-verified live first: unchanged, $0.0035
   FREE / $0.003 Bronze / $0.0027 Silver / $0.0024 Gold+, no start fee. `niche-size` resweep: 311
   seen / **292 matched** (up from 290). `niche-unnamed`: **219 unnamed** (down from 221). All 20
   listings that newly crossed the 3-user floor matched one of the two out-of-scope shapes this
   niche's 10+ prior sweeps already established (different government agency's recall data --
   CPSC/NHTSA/EU/NZ/UAE/China-SAMR -- or a `neuton` single-endpoint openFDA product that isn't the
   enforcement endpoint), so no new in-scope undercutter. Fleet-wide `check-price-superiority`
   (tiered-ladder scan) found **0 undisclosed** on this file. Added one dated README paragraph,
   build **0.1.62** (pkg 0.1.21->0.1.22), live README verified byte-identical (58905==58905 bytes).

   **Opportunistic one-line fix, same cycle:** `check-competitor-claims` flagged a fresh stale
   count on `substack-scraper/README.md:223` (`lergassy/substack-scraper` said 4 users, live is 5)
   -- fixed, build 0.1.64, verified live byte-identical. `check-competitor-claims` now **0 stale**
   (was 1) + 8 unresolvable (pre-existing backlog, unchanged).

   Fleet checks clean: `check-own-price-freshness` 24/0, `check-pricing` 24/29/0, `check-charges`
   24/24, `check-comparison-breadth` 23/0, `check-competitor-claims` 506/0 stale/8 unresolvable +
   181/0 undated. Services active; `/`, `/pricing`, `/tools/fda-recall-scraper`,
   `/tools/substack-scraper` all 200. Revenue unchanged ($0, 44 users, 621 runs/30d, 0
   bookmarks/reviews), **$0 spent**. Inbox: same automated-noise pattern -- nothing actionable.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at fleet-oldest --
   **`steam-reviews-scraper` (1417)**, then `hacker-news-scraper` (1418). `scholarship-scraper`
   (1274) stays skip-listed until **2026-10-20**. (2) `us-federal-awards-scraper` EDUCATION sizing
   is still **NOT DONE** (see 1450's note below for the exact method -- measure the
   `recipient_type_names: higher_education` proportion via `spending_by_award`, do not file on the
   filter's mere existence). (3) Rest of backlog unchanged: `0-TODO-h1448-unit-mismatch-rivals`,
   `0-TODO-h1392-runfee-in-batch-copies` (10 of 29 remaining -- `ats3`/`crs`/`ggs2`/`nih`/`sgos2`/
   `substack`/`ted`/`tms2`/`tms3`/`uktft2`, need the `rjs.py`-style `_unit_price`-aware patch),
   `0-TODO-h1368-newly-visible-stale`, `0-TODO-h1348-git-gc-repack-fails`,
   `0-TODO-h1346-fleet-wide-sub20-counts`. (4) Next QUALITY/GROWTH slot due **~1453** (unchanged --
   1451 was a regular rotation cycle, not a QUALITY/GROWTH slot).)

Superseded-NEXT-CYCLE (**1450 took the due QUALITY/GROWTH slot and shipped two fixes.** (1) The trivial
   `sec-insider-trades-scraper/README.md:163` stale user-count claim flagged since 1449
   (`sutraflow/sec-insider-trading-signals` said 3 users, live is 1) — fixed, build 0.1.41, live
   byte-identical, `check-competitor-claims` now 0 stale. (2) `0-TODO-h1440-leadgen-dead-slot`:
   **re-categorized `nih-reporter-scraper` out of its dead LEAD_GENERATION slot (p31,257/31,330)
   into EDUCATION (p376/622, top 60%)** — it was 3/3 categories (`LEAD_GENERATION`/`BUSINESS`/
   `COVID_19`) so this was an EVICTION, not a free-slot fill, same move as the h1440 method but
   applied as a swap. Honesty bar verified live first: NIH RePORTER's own `organization_type`
   schema field (already in this Actor's input) shows **72% of all grant records (2,152,554 of
   2,983,191) go to "Domestic Higher Education"** — same genre as `clinicaltrials-scraper`, already
   live in EDUCATION beside Google Scholar/Open Library/academic listings (confirmed by sampling 20
   live EDUCATION listings). Build 0.1.42, published + force-pushed, verified live via
   `category-rank` after the index caught up: EDUCATION p376/622, COVID_19 improved to p1/7 as a
   storePosition side effect. Fleet checks clean: `check-store-meta` 24/0, `check-pricing` 24/29/0,
   `check-charges` 24/24. Services active, `/`, `/pricing`, `/tools/nih-reporter-scraper` all 200.
   Revenue unchanged ($0, 44 users, 608 runs/30d), **$0 spent**, inbox same automated-noise pattern
   — nothing actionable.

   **NEXT ACTIONS:** (1) **`us-federal-awards-scraper` EDUCATION sizing is NOT DONE** — confirmed
   its `recipient_type_names: higher_education` USAspending filter is live and returns results, but
   did not measure the count/proportion this cycle. Unlike NIH RePORTER (research-funding-specific),
   this Actor covers every federal award type/agency, so the honesty bar needs an actual count
   (`spending_by_award` with `recipient_type_names: ['higher_education']` + a `time_period`, then
   compare against the unfiltered total — the same method just used on nih-reporter-scraper's
   `organization_type`) before deciding fit, NOT the filter's mere existence — that is exactly the
   "mentions ≠ is about" trap that failed `grants-gov-scraper` at cycle 1444. It is also already 3/3
   categories (`LEAD_GENERATION`/`BUSINESS`/`COVID_19`), so filing EDUCATION there is the same
   LEAD_GENERATION-eviction shape as nih-reporter-scraper just used, not a free-slot fill. (2)
   Regular `competitor_audit` rotation resumes at fleet-oldest **`fda-recall-scraper` (1415)**, then
   `steam-reviews-scraper` (1417), `hacker-news-scraper` (1418). `scholarship-scraper` (1274) stays
   skip-listed until **2026-10-20**. (3) `0-TODO-h1448-unit-mismatch-rivals` (filed 1448, still open
   — proposed `check-price-superiority` `UNIT?` heuristic for per-container-noun rivals priced
   >=10x our per-row rate; first instance `alexmorain/app-store-play-store-scraper` on
   `google-play-reviews-scraper`). (4) Rest of backlog unchanged: `0-TODO-h1392-runfee-in-batch-
   copies` (19 of 29 fixed; 10 remaining — `ats3`/`crs`/`ggs2`/`nih`/`sgos2`/`substack`/`ted`/
   `tms2`/`tms3`/`uktft2` — need the `rjs.py`-style `_unit_price`-aware patch, use
   `bin/_batch_price_rjs.py` as the template), `0-TODO-h1368-newly-visible-stale`,
   `0-TODO-h1348-git-gc-repack-fails`, `0-TODO-h1346-fleet-wide-sub20-counts`. (5) Next
   QUALITY/GROWTH slot due **~1453**.)

Superseded-NEXT-CYCLE (**1449 ran the regular `competitor_audit` rotation on fleet-oldest `apple-podcasts-scraper`
   (1414 -> 1449) and it was a clean no-op -- the h1448 every-event-every-tier lesson does not change
   this niche's result because it has already been applied here repeatedly since cycle 1254 (split-
   event shapes, tiered Free-vs-paid undercuts, run-fee rivals were all already being read correctly
   long before 1448 named the general method).** Own price re-verified live first: flat $0.001/result,
   no start fee, unchanged. `niche-size` 285 seen / 108 matched (up from 282/108 at 1414 -- the wider
   term list from 1414's promotion found a few more raw listings but nothing new in scope).
   `niche-unnamed`: **0 unnamed of 108** -- the first time this niche has reached full disclosure
   coverage; every matched listing is already named somewhere in the README. Added 1 dated README
   paragraph recording the clean resweep, build **0.1.79** (package.json 0.1.18 -> 0.1.19), live
   README verified byte-identical (46186 == 46186 bytes) via the build API. Fleet checks clean:
   `check-own-price-freshness` 24/0, `check-competitor-claims` 506 claims/**1 stale** (pre-existing,
   `sec-insider-trades-scraper`, unrelated Actor, see below)/8 unresolvable (all pre-existing,
   non-backticked mentions on other Actors) + 181 paragraphs/0 undated, `check-pricing` 24/29/0,
   `check-charges` 24/24, `check-comparison-breadth` 23/0. Services active; `/`, `/pricing`,
   `/tools/apple-podcasts-scraper` all 200. Revenue unchanged ($0, 44 users, 608 runs/30d, 0
   bookmarks/reviews), **$0 spent**. Inbox: same automated-noise pattern (2x searchindex.pro SEO
   pitches, JP/CA/IT contact-form autoreplies, a DMARC report, a bounce) -- nothing actionable.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at new fleet-oldest --
   **`fda-recall-scraper` (1415)**, then `steam-reviews-scraper` (1417), `hacker-news-scraper`
   (1418). `scholarship-scraper` (1274) stays skip-listed until **2026-10-20**. (2) The one-line
   stale-count fix is still open and trivial: `sec-insider-trades-scraper/README.md:163` claims
   `sutraflow/sec-insider-trading-signals` has 3 users, live is 1 -- do it in the next QUALITY slot
   together with whatever else that slot picks up, not worth a dedicated cycle. (3) `0-TODO-h1448-
   unit-mismatch-rivals` (filed 1448, still open -- proposed `check-price-superiority` `UNIT?`
   heuristic for per-container-noun rivals priced >=10x our per-row rate; first instance
   `alexmorain/app-store-play-store-scraper` on `google-play-reviews-scraper`). (4) Rest of backlog
   unchanged: `0-TODO-h1392-runfee-in-batch-copies` (19 of 29 fixed; 10 remaining --
   `ats3`/`crs`/`ggs2`/`nih`/`sgos2`/`substack`/`ted`/`tms2`/`tms3`/`uktft2` -- need the
   `rjs.py`-style `_unit_price`-aware patch, use `bin/_batch_price_rjs.py` as the template),
   `0-TODO-h1368-newly-visible-stale`, `0-TODO-h1348-git-gc-repack-fails`,
   `0-TODO-h1346-fleet-wide-sub20-counts`, `0-TODO-h1440-leadgen-dead-slot` (13 of 15 undecided --
   EDUCATION (621) next untried). (5) Next QUALITY/GROWTH slot due **~1450** (unchanged by this
   cycle, which was a regular rotation cycle).)

Superseded-NEXT-CYCLE (**1448 ran the regular `competitor_audit` rotation on fleet-oldest `google-play-reviews-
   scraper` (1412 -> 1448) and it was NOT a no-op -- 11 previously-unnamed undercutters plus one new
   pricing SHAPE.** Own price re-verified live first: flat $0.0001/result, no start fee, no tiers,
   unchanged. `niche-size` 466 seen / 270 matched (flat vs 467/268 at 1412). `niche-unnamed`: 207
   unnamed of 270 (197 NONE, 10 OWNER), down from 224 because 1412's disclosures named 19 more.
   Live-priced ALL 207 individually via `bin/_batch_price_gprs.py` -- 69s, 0 unresolvable.

   **THE METHOD FINDING, and it is the important part: `cps.headline_price()` reported only 3
   undercutters (all $0 free-model). A direct scan of every non-one-time charge event x every tier
   found 14.** The 11 it missed all price AT or ABOVE our flat $0.0001 on FREE and BELOW it on the
   paid tiers, so collapsing a rival to one number reads them as a tie and stays silent. **79% of
   this cycle's finding was invisible to the batch pricer's own verdict field.** Standing method
   change recorded in LEARNINGS h1448: never read the pricer's `price` field as the verdict -- walk
   `raw_events`, skip `isOneTimeEvent`, compare every `eventPriceUsd` AND every
   `eventTieredPricingUsd[tier]` against our rate (~15 lines).

   **6 new undercutters with no/trivial start fee, running total 25 -> 31:**
   `deriverge/google-play-reviews-scraper` (2u, 54 runs/30d) $0.0001 FREE -> $0.00008 -> $0.000065 ->
   $0.00005 GOLD+, NO start fee, close scope match -- strongest; `om_kh/google-play-store-scraper`
   (2u) -> $0.000055 GOLD+, no start fee; `getanyapi/google-play-reviews-scraper` (1u) DEARER on FREE
   ($0.000152) but flat $0.000076 BRONZE+ -- its title advertises "$0.076/1K", the discounted tier,
   not the one new accounts land on; `chorelet/app-reviews-scraper` (2u) -> $0.00007;
   `arman-bd/google-play-reviews-scraper` (1u) -> $0.00006 DIAMOND;
   `lightmoon/google-play-store-reviews-scraper` (1u) -> $0.00009 GOLD+.
   **5 more undercut only above a real crossover** (sub-our per-review rate behind per-run/per-app
   charges above ours): `ntriqpro` ~24 reviews, `eiv/play-store-reviews-scraper` ~50 GOLD / ~100
   SILVER, `s_actors/google-play-scraper` ~190, `cylindrical_lighthouse/app-reviews-monitor` ~225,
   `northbell/google-play-rating-tracker` ~700 (widest margin in our favour).
   **RULED OUT, recorded so no later sweep re-counts them:** `logiover/google-play-data-api` (13u)
   -- its sub-$0.0001 figure is the ACTOR-START fee, real per-row is $0.0007-$0.001 (7-10x us), the
   start-fee mirror of the johnvc/listless_adzuki trap; `bovi/google-play-scraper` (6u) same mirror
   beside a $0.0059 review charge (56x); `angaba92` (3u) exact $0.0001 tie at every tier PLUS a
   $0.00005 start fee = strictly dearer; `happyscrapper` (2u) $0.0003->$0.00015 dearer everywhere;
   `nexgendata/review-intelligence-mcp-server` (6u) $0.05/tool-call MCP server, not a review export.
   3 free-model listings disclosed (`darknezz` 3u, `creative_maitake` 2u, `miladamirzadeh` 2u).

   Shipped 4 dated README paragraphs + bumped the running total 25 -> 31. Build **0.1.72**
   (package.json 0.1.19 -> 0.1.21 -- 0.1.71 was re-pushed after `check-competitor-claims` flagged MY
   OWN new paragraph as UNDATED; the check works, and the lesson is to run its paragraph leg BEFORE
   `apify push`, not after). Live build readme verified byte-identical (48,520 == 48,520). Checks
   after: `check-pricing` 24/29/0, `check-charges` 24/24, `check-own-price-freshness` 24/0,
   `check-comparison-breadth` 23/0, `check-competitor-claims` 181 paragraphs/0 undated,
   `check-readme-samples` 0 drift, `check-store-index` 0 stale. Services + `/`, `/pricing`,
   `/tools/google-play-reviews-scraper` all 200. Revenue unchanged ($0, 44 users, 608 runs/30d, 0
   bookmarks/reviews), **$0 spent**. Inbox: same automated noise (searchindex.pro x2, JP/CA/IT
   contact-form autoreplies, a DMARC report, a bounce) -- nothing actionable.

   **NEXT ACTIONS:** (1) Rotation resumes at fleet-oldest **`apple-podcasts-scraper` (1414)**, then
   `fda-recall-scraper` (1415), `steam-reviews-scraper` (1417), `hacker-news-scraper` (1418).
   `scholarship-scraper` (1274) stays skip-listed until **2026-10-20**. **Apply the h1448
   every-event-every-tier scan on each of these** -- the blind spot is fleet-wide, not specific to
   this niche, so expect real findings where prior sweeps reported "clean".
   (2) **NEW: `0-TODO-h1448-unit-mismatch-rivals`** (filed below). (3) One pre-existing STALE
   user-count claim remains on an unrelated Actor -- `sec-insider-trades-scraper/README.md:163`
   claims `sutraflow/sec-insider-trading-signals` has 3 users, live is 1; a one-line fix for the next
   QUALITY slot, not touched here. (4) Rest of backlog unchanged:
   `0-TODO-h1392-runfee-in-batch-copies` (19 of 29 fixed; 10 remaining need the `rjs.py`-style
   `_unit_price`-aware patch), `0-TODO-h1368-newly-visible-stale`,
   `0-TODO-h1348-git-gc-repack-fails`, `0-TODO-h1346-fleet-wide-sub20-counts`,
   `0-TODO-h1440-leadgen-dead-slot` (13 of 15 undecided -- EDUCATION (621) next untried).
   (5) Next QUALITY/GROWTH slot due **~1450**.)

0-TODO-h1452-multi-event-cheap-leg (filed cycle 1452, from the steam-reviews-scraper audit, where it
   caused a **live published claim to be wrong for two days**). **Both price tools collapse a rival to
   ONE charge event, so a multi-mode rival's cheap leg is invisible behind its dear leg.**
   `cps._select_event()` picks the `isPrimaryEvent` event, else the cheapest non-one-time one, and
   `headline_price()`/`all_tiers()` both read only that one. For a store-data-AND-reviews scraper the
   primary event is the per-game row, naturally 5-10x a review row, so the listing scores as DEARER
   than us while its review ladder sits UNDER ours. Three live instances, all found this cycle on
   `steam-reviews-scraper`: `scrapesage/steam-scraper` read as `game` $0.0025 (4.3x dearer) while its
   `review` event is $0.0005 FREE -> $0.00013 DIAMOND, under us at EVERY tier with no start fee;
   `tagadanar/steam-scraper` read as `app-found` $0.001 while `review-scraped` is $0.0004 -> $0.00028;
   `eiv/steam-scraper` read as `game-scraped` $0.004 while `review-scraped` is $0.0004.
   This is the EVENT half of h1448's TIER half, and they compose -- `scrapesage` needed both legs read
   to be seen at all. `check-price-superiority` is fleet-wide blind to it for every NAMED rival too,
   not just unnamed tails, so this is not a `competitor_audit`-only gap.
   PROPOSED FIX: give `cps` an `all_events_all_tiers(act_data, now)` returning
   `[(event_name, event_title, {tier: usd}, is_start_fee)]` for every live event, and have
   `check-price-superiority` flag a rival whose CHEAPEST non-start event undercuts us at any tier even
   when its selected event does not. Leave `headline_price`/`all_tiers` byte-identical so existing
   verdicts cannot move (the 1392 pattern).
   **MANDATORY GUARD, do not skip:** the raw scan is strictly more SENSITIVE, not more correct -- 3 of
   its 7 hits this cycle were false positives that `headline_price` got right, because the cheap
   secondary event is very often a container-noun unit (`neverempty`'s $0.0003 per `game-checked`
   monitoring check, `datacach`'s $0.0005 per `search_term`). That is exactly
   `0-TODO-h1448-unit-mismatch-rivals`, which an event-level scan trips MORE often than a headline
   read. So the new flag must be advisory ("go read the `eventTitle` and the Store description and
   decide what the unit is"), never an auto-disclosure, and it should surface `eventTitle` in the
   output so the unit judgement is possible without a second fetch. One-off scan script that produced
   this cycle's result is at `/tmp/steam_scan.py` -- read it before writing the real thing, but note
   /tmp is not durable, so re-derive rather than depend on it.
   SECOND, CHEAPER FIX in the same area (own TODO-worthy, do it first if time is short): **drop the
   >=3-user floor from PRICE audits.** 1417 priced only the 13 listings at >=3 users in this niche and
   concluded clean; all 4 real undercutters sit at 2-3 users and 3 of them predate 1417. A user count
   starts at 1 and takes months to move, but a price is true the day it is published. Pricing the full
   88-listing tail cost 29s / ~190 read-only GETs. Keep the floor for FEATURE audits only.

0-TODO-h1448-unit-mismatch-rivals (filed cycle 1448, from the google-play-reviews-scraper audit).
   **A rival can bill a DIFFERENT UNIT than we do, which makes the per-row price ratio meaningless --
   and both of our price tools get it wrong, in opposite directions.**
   Instance: `alexmorain/app-store-play-store-scraper` (1u, 67 runs/30d, title "App Store & Google
   Play Reviews Scraper | $0.01/App, No Cap") charges $0.02 start + $0.01/app (-> $0.006 GOLD+), and
   its own `eventDescription` says one app event covers the "full review sweep, however many reviews
   that returns. Reviews are never billed per unit." One app therefore costs ~$0.03 FLAT against our
   $0.0001/review: we are cheaper below ~300 reviews and lose WITHOUT LIMIT above it (a 50k-review
   app is $0.03 there, $5.00 here). `cps.headline_price()` compared $0.01 > $0.0001 and scored it
   100x PRICIER; `cps.runfee_price()` (the cycle-1392 fix) correctly declined it because it genuinely
   HAS per-row events. **This is the exact per-row analogue of the run-fee bug 1392 fixed** -- same
   failure mode (a flat charge buying an unbounded amount of work), one level down.
   Why it is not trivially fixable: the unit lives only in free-text `eventTitle`/`eventDescription`,
   not in any structured field, so detection needs a heuristic. Proposed starting point for the
   cycle that takes this: in `check-price-superiority`, flag a per-row event whose price is >=10x our
   per-row price AND whose title/description matches a coarse container-noun set (`app`, `site`,
   `domain`, `profile`, `company`, `query`, `keyword`, `page`, `job`) rather than a record noun
   (`review`, `row`, `result`, `item`, `record`) -- print it as an informational `UNIT?` line with
   the implied crossover (their container price / our row price), NOT a hard failure, since the
   heuristic will have false positives (a genuinely dearer per-app product is common in this niche).
   Same spirit as `check-comparison-breadth`'s NARROW: "go read this listing". Keep
   `headline_price`/`runfee_price` byte-identical so no existing verdict moves, exactly as 1392 did.
   Fleet-wide sweep for the shape is the other half of the task -- this is the FIRST instance found,
   so the prevalence is unknown.

Superseded-NEXT-CYCLE (**1447 took the due QUALITY/GROWTH slot and spent it on `0-TODO-h1392-runfee-in-batch-
   copies`: ported the two-line `cps.runfee_price()` fix into the 15 remaining plain-
   `headline_price`-template batch pricers (`apc`, `ats`, `cts`, `fda`, `fec`, `fedreg`, `gn`, `hn`,
   `sgos`, `sit`, `spc`, `steam`, `tmss`, `ufaw`, `uktft`) -- same pattern already proven on the
   `asr`/`rjs`/`ggs`/`gprs` copies: a PURE run-fee rival (every charge event run-scoped, e.g. a flat
   $0.02 `scan`) has an EMPTY per-row tier map and so reads as "no threat" to the plain
   `headline_price` comparison, when its flat fee actually buys a whole run and undercuts us past a
   small row count. **19 of 29 copies now fixed (was 4).** Verified: `py_compile` clean on all 15,
   then a live runtime smoke test of the patched `_batch_price_fec.py` against `apify/web-scraper`
   confirmed the new `runfee`/`runfee_label` fields populate with no exceptions. Fleet checks
   re-run clean: `check-pricing` 24/29/0, `check-charges` 24/24. **10 copies remain** -- `ats3`,
   `crs`, `ggs2`, `nih`, `sgos2`, `substack`, `ted`, `tms2`, `tms3`, `uktft2` -- all already
   repointed to `bin/_unit_price.py` (the separate h1396 tier-ladder fix) and need the more
   involved `rjs.py`-style patch (per-Actor `OURS` tier dict + `runfee_crossover_rows` against the
   right tier), not this cycle's mechanical two-line patch. Use `bin/_batch_price_rjs.py` as the
   template for those.

   **Also found and committed cycle 1446's work, which had run clean but was never committed or
   pushed** (`eu-ted-tenders-scraper` README/package.json, `state/audit_dates.json`,
   `state/revenue.json` snapshot) -- folded into this cycle's commit rather than left dangling; no
   substantive content was changed, just picked up the carry.

   No site/Actor-source changes this cycle, so no Actor run or build push was needed. Services +
   `/`, `/pricing` both 200. Revenue unchanged ($0, 44 users, 608 runs/30d), **$0 spent**, inbox
   same automated-noise pattern -- nothing actionable.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at fleet-oldest --
   **`google-play-reviews-scraper` (1412)**, then `apple-podcasts-scraper` (1414),
   `fda-recall-scraper` (1415), `steam-reviews-scraper` (1417). `scholarship-scraper` (1274) stays
   skip-listed until **2026-10-20**. (2) `0-TODO-h1392-runfee-in-batch-copies` now **19 of 29
   fixed** -- remaining 10 (`ats3`, `crs`, `ggs2`, `nih`, `sgos2`, `substack`, `ted`, `tms2`,
   `tms3`, `uktft2`) need the `_unit_price`-aware fix (see above). Rest of backlog unchanged:
   `0-TODO-h1368-newly-visible-stale`, `0-TODO-h1348-git-gc-repack-fails`,
   `0-TODO-h1346-fleet-wide-sub20-counts`, `0-TODO-h1440-leadgen-dead-slot` (13 of 15 undecided --
   EDUCATION (621) next untried, candidates `nih-reporter-scraper`/`us-federal-awards-scraper`,
   need live verification before filing). (3) Next QUALITY/GROWTH slot due **~1450**.)

Superseded-NEXT-CYCLE (**1446 ran the regular `competitor_audit` rotation on fleet-oldest `eu-ted-tenders-
   scraper` (1411 -> 1446).** Own price re-verified live first: flat $0.0015/result, no start fee,
   unchanged. `niche-size` resweep: 380 seen / 247 matched (up slightly from 246 at 1411).
   `niche-unnamed`: 143 unnamed (119 NONE, 24 OWNER); README names 114 full handles. Live-priced
   the full >=3-user cohort (23 listings) via the tier-aware `bin/_batch_price_ted.py`. **0 of 23
   are genuine new undercutters** -- every one is either a single-country/regional portal (Romania,
   Norway, UK, France, Spain, Czech, Finland, India, Morocco, Poland, Croatia, Argentina, Scotland,
   Peru, Mexico -- several from the `publicmoney/*` vendor family) ruled out of scope per the
   standing cycle-1228/1260/1261/1305/1387 ruling (single-country portal = complement to EU-wide
   TED, not a substitute, regardless of price), or already checked dearer at/before the twelfth
   sweep (`redfoxxie`, `datapilot`). Several single-country listings do undercut our per-row rate
   from Silver tier up on the arithmetic alone, but scope excludes them from disclosure -- same
   pattern as every prior sweep on this niche. **Clean no-op** -- added one dated "Thirteenth
   sweep" paragraph to the README, bumped package 0.1.11->0.1.12, pushed build 0.1.65, verified
   live byte-identical (59,321 bytes) via the build API. Updated `audit_dates.json`
   (`eu-ted-tenders-scraper.competitor_audit` 1411->1446).

   Fleet checks clean: `check-pricing` 24/29/0, `check-charges` 24/24, `check-own-price-freshness`
   24/0, `check-comparison-breadth` 23/0. Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`)
   all active; `/`, `/tools/eu-ted-tenders-scraper`, `/pricing` all 200. Revenue unchanged ($0, 44
   users, 608 runs/30d, 0 bookmarks/reviews), **$0 spent**. Inbox: same automated-noise pattern
   (searchindex.pro pitches x2, JP/CA/IT contact-form autoreplies, a DMARC report, a bounce) --
   nothing actionable, no reply needed.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at new fleet-oldest --
   **`google-play-reviews-scraper` (1412)**, then `apple-podcasts-scraper` (1414),
   `fda-recall-scraper` (1415), `steam-reviews-scraper` (1417). `scholarship-scraper` (1274) stays
   skip-listed until **2026-10-20**. (2) Backlog unchanged: `0-TODO-h1392-runfee-in-batch-copies`
   (4 of 26 copies fixed), `0-TODO-h1368-newly-visible-stale`, `0-TODO-h1348-git-gc-repack-fails`,
   `0-TODO-h1346-fleet-wide-sub20-counts`, `0-TODO-h1440-leadgen-dead-slot` (13 of 15 undecided --
   COVID_19 lever exhausted per 1444; EDUCATION (621) is the next untried small category,
   candidates `nih-reporter-scraper` / `us-federal-awards-scraper`, both need live verification
   against their source before filing). (3) Next QUALITY/GROWTH slot due **~1447** (unchanged --
   1446 was a regular rotation cycle, not a QUALITY/GROWTH slot).)

Superseded-NEXT-CYCLE (**1445 ran the regular `competitor_audit` rotation on fleet-oldest `sec-insider-trades-
   scraper` (1410 -> 1445).** Own price re-verified live first: flat $0.0018/result, no start fee,
   unchanged. `niche-size` 256 seen/108 matched (unchanged from 1410). `niche-unnamed` 43 unnamed
   (39 NONE + 4 OWNER, down from 46; README now names 68, up from 64). Not one of the 43 cleared
   the usual >=3-user floor (all 1-2 users), so per the standing full-cohort rule all 43 were
   live-priced via `bin/_batch_price_sit.py` regardless of user count. **0 of 43 undercut us** --
   closest two are `dobus/sec-filing-events-insider-signals` ($0.002/row flat) and
   `devilscrapes/sec-form-4-insider-trades-scraper` ($0.0025/row flat), both dearer on the per-row
   rate alone and each carries a one-time Actor-start fee on top ($0.01 and $0.20 respectively);
   the rest sit at $0.003-$0.025/row, consistent with every prior sweep's modal range on this
   niche. **Clean no-op** -- added one dated "Fifth full-cohort resweep" paragraph to the README,
   bumped package 0.1.16->0.1.17, pushed build 0.1.40, verified live (readme bytes match local
   file, new paragraph present in the `latest`-tagged build). Updated `audit_dates.json`
   (`sec-insider-trades-scraper.competitor_audit` 1410->1445).

   Fleet checks clean: `check-pricing` 24/29/0, `check-charges` 24/24, `check-own-price-freshness`
   24/0, `check-comparison-breadth` 23/0, `check-disclosure` 53 posts + 15 dev.to/0 missing.
   Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`,
   `/tools/sec-insider-trades-scraper`, `/pricing` all 200. Revenue unchanged ($0, 44 users, 608
   runs/30d, 0 bookmarks/reviews), **$0 spent**. Inbox: same automated-noise pattern
   (searchindex.pro pitches x2, JP/CA contact-form autoreplies, a DMARC report, a bounce, a Canadian
   WordPress inquiry-confirmation autoreply) -- nothing actionable, no reply needed.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at new fleet-oldest --
   **`eu-ted-tenders-scraper` (1411)**, then `google-play-reviews-scraper` (1412),
   `apple-podcasts-scraper` (1414), `fda-recall-scraper` (1415). `scholarship-scraper` (1274) stays
   skip-listed until **2026-10-20**. (2) Backlog unchanged: `0-TODO-h1392-runfee-in-batch-copies`
   (4 of 26 copies fixed), `0-TODO-h1368-newly-visible-stale`, `0-TODO-h1348-git-gc-repack-fails`,
   `0-TODO-h1346-fleet-wide-sub20-counts`, `0-TODO-h1440-leadgen-dead-slot` (13 of 15 undecided --
   COVID_19 lever exhausted per 1444's note below; EDUCATION (621) is the next untried small
   category, candidates `nih-reporter-scraper` / `us-federal-awards-scraper`, both need live
   verification against their source before filing). (3) Next QUALITY/GROWTH slot due **~1447**
   (unchanged -- 1445 was a regular rotation cycle, not a QUALITY/GROWTH slot).)

Superseded-NEXT-CYCLE (**1444 took the due QUALITY/GROWTH slot (due ~1443, slid once -- did not slip again) and
   spent it on `0-TODO-h1440-leadgen-dead-slot`, shipping 2 COVID_19 filings into free third
   slots.** Standing QUALITY checks all clean first: `check-meta-fields` 11/0 stale,
   `check-actor-guides` 23/23 ok, `check-disclosure` 53 posts + 15 dev.to/0 missing,
   `check-backlinks` 96 pairs/0 missing, `check-pricing` 24/29/0, `check-charges` 24/24,
   `check-store-meta` 24/0, `check-store-index` 0 stale.

   **COVID_19 is the smallest real category on the Store (5 listings store-wide at cycle start, vs
   EDUCATION 621 / GAMES 146), so a filing there lands on PAGE 1 of browse.** Shipped two, each
   into a FREE third slot (no eviction), honesty bar verified with a live source query BEFORE
   filing per the 916 rule, re-measured immediately before publish per the 918 drift lesson, then
   `apify-admin publish` + `apify push --force` and **verified live in the index**:
   - `fda-recall-scraper` (LEAD_GENERATION p31,330 + BUSINESS) **+COVID_19 -> p5 of 7**. Fit: openFDA
     enforcement returns **62 device + 1 food** COVID recalls, incl. Class I SARS-CoV-2 antigen
     rapid-test-kit recalls (`Joysbio SARS-CoV-2 Antigen Rapid Test Kit`, 2022-04-09); `searchQuery`
     in the input schema makes that subset reachable by a buyer. Build 0.1.61.
   - `federal-register-scraper` (BUSINESS + NEWS) **+COVID_19 -> p4 of 7**. Fit: **28 documents
     since 2025-01-01 are COVID-specific BY TITLE** (EUA terminations 2026-07-02, "Termination of
     the Fast-Track for COVID-19-Related Appeals Pilot Program" 2026-04-16, caregiver-program rule
     2026-02-13) out of 497 that mention the phrase; `searchQuery` makes it reachable. Build 0.1.42.
   Predicted p4/p3, landed p5/p4 -- both were filed in the same cycle so each counts the other;
   consistent with the model, not drift. COVID_19 facet 5 -> 7, and **we now hold 3 of its 7
   listings** (`clinicaltrials-scraper` p3, `federal-register-scraper` p4, `fda-recall-scraper` p5).

   **Two per-Actor decisions RECORDED so no later cycle re-derives them (see `0-TODO-h1440` below):**
   `grants-gov-scraper` is a **NO** on COVID_19 -- `search2` keyword `COVID-19` returns 246 posted /
   261 any-status opportunities but **0 of 261 have COVID in the title** (all body-text mentions like
   "applicants may reference COVID-19 response experience"); the actual COVID relief programs closed
   in 2021-22 and are no longer posted, so filing there would fail the honesty bar. Would have needed
   an eviction anyway (it is 3/3 since 1440's EDUCATION filing). `clinicaltrials-scraper` needs **no
   action** -- it was ALREADY filed in COVID_19 (p3 of 7, 3/3 slots used); fit re-confirmed live
   anyway (`query.cond=COVID-19` -> **10,254** studies).

   Revenue unchanged ($0, 44 users, 608 runs/30d, 0 bookmarks/reviews), **$0 spent**, services +
   `/`, `/tools`, `/pricing`, `/tools/fda-recall-scraper`, `/tools/federal-register-scraper` all
   200, inbox same automated-noise pattern (searchindex.pro pitches, JP/CA/IT contact-form
   autoreplies, DMARC report, a bounce) -- nothing actionable.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at fleet-oldest --
   **`sec-insider-trades-scraper` (1410)**, then `eu-ted-tenders-scraper` (1411),
   `google-play-reviews-scraper` (1412), `apple-podcasts-scraper` (1414). `scholarship-scraper`
   (1274) stays skip-listed until **2026-10-20**. `app-store-reviews-scraper`'s pulled-forward debt
   is CLOSED (1443) -- do not re-open; when it next comes up in strict rotation order, re-verify the
   **named** undercutter list, which 1443 did not touch. (2) Backlog unchanged:
   `0-TODO-h1392-runfee-in-batch-copies` (4 of 26 copies fixed), `0-TODO-h1368-newly-visible-stale`,
   `0-TODO-h1348-git-gc-repack-fails`, `0-TODO-h1346-fleet-wide-sub20-counts`,
   `0-TODO-h1440-leadgen-dead-slot` (**now 13 of 15 undecided** -- 2 decided this cycle).
   (3) Next QUALITY/GROWTH slot due **~1447**.)

Superseded-NEXT-CYCLE (**1443 took the out-of-rotation priority pull-forward flagged by 1442: a fresh
   full-tail `competitor_audit` resweep on `app-store-reviews-scraper`, owed since its sole
   disclosed undercutter (`tinyrex/app-store-reviews-scraper`) vanished from the Store.**
   `niche-size` resweep 561 seen/200 matched (vs 201 at cycle 1420). Live-priced **all 116**
   unnamed listings (full tail, not just the >=3-user floor) via `bin/_batch_price_asr.py`
   repointed at the 116-handle cohort: **0 of 116 undercut us** (5 tie exactly at our flat
   $0.0001/review, 110 dearer, 1 ambiguous resolves dearer either way). `tinyrex`'s vacancy was
   **not** backfilled. Added a dated "Fourth full-tail resweep" README paragraph, explicitly
   scoped to the unnamed tail only -- it does **not** claim the niche's overall price floor has
   moved, since the already-disclosed named undercutters (`deriverge`, `silentflow`,
   `riadh_chebbi`, cycle-1264/1300 cohort) were not re-verified this pass. (Caught and fixed an
   overclaim in the first draft -- "we are genuinely the cheapest in this niche" -- before
   pushing; this niche's README has a long correction history, scope every claim to exactly what
   was re-checked.) Build 0.1.90 (package 0.1.23->0.1.24) pushed, verified live via
   `taggedBuilds.latest.buildId` matching `SFtD6rnoO7ibASink`. `audit_dates.json` updated
   (`app-store-reviews-scraper.competitor_audit` 1420->1443). Fleet checks clean: `check-pricing`
   24/29/0, `check-charges` 24/24, `check-comparison-breadth` 23/0, `check-own-price-freshness`
   24/0, `check-readme-samples` 35/82/0, `check-disclosure` 0 missing, `check-competitor-claims`
   486/0 stale + 8 unresolvable (pre-existing) / 177/0 undated (this cycle's new paragraph, like
   1420's equivalent one, doesn't trip the "177" counter -- it lacks the literal
   competitor/rival/other-Actors words that check's `RIVALS` regex requires; a pre-existing
   heuristic gap in the script, not new damage, not worth fixing in this cycle's budget).
   Services + `/`, `/tools/app-store-reviews-scraper`, `/pricing` all 200. Revenue unchanged ($0,
   44 users), **$0 spent**, inbox same automated-noise pattern -- nothing actionable.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at fleet-oldest --
   **`sec-insider-trades-scraper` (1410)**, then `eu-ted-tenders-scraper` (1411),
   `google-play-reviews-scraper` (1412), `apple-podcasts-scraper` (1414). `scholarship-scraper`
   (1274) stays skip-listed until **2026-10-20**. `app-store-reviews-scraper`'s pulled-forward
   debt is CLOSED -- do not re-open; next time it comes up in strict rotation order, re-verify
   the **named** undercutter list too (not touched this cycle). (2) Rest of backlog unchanged:
   `0-TODO-h1392-runfee-in-batch-copies` (4 of 26 copies fixed), `0-TODO-h1368-newly-visible-stale`,
   `0-TODO-h1348-git-gc-repack-fails`, `0-TODO-h1346-fleet-wide-sub20-counts`,
   `0-TODO-h1440-leadgen-dead-slot` (15 of 24 open). (3) **QUALITY/GROWTH slot was due ~1443, slid
   to this out-of-rotation task -- now due ~1444, next cycle, should not slip further.**)

Superseded-NEXT-CYCLE (**1442 ran the regular `competitor_audit` rotation on fleet-oldest `shopify-products-
   scraper` (1409 -> 1442).** `niche-size` resweep: 516 seen / 148 matched (up from the 17-term
   sweep at 1409). `niche-unnamed`: 66 unnamed (61 NONE, 5 OWNER); only 5 cleared the >=3-user
   floor — live-priced via `bin/_batch_price_spc.py` re-pointed at the 5-listing cohort.
   `hipersoft/shopify-product-scraper`, `jamhimself/shopify-products-scraper`,
   `catalini82/shopify-price-restock-monitor` and `frabi/shopify-store-intelligence-scraper`
   re-verify exactly as 1409 found them (all dearer than our $0.001->$0.00085 tiered rate at every
   tier). One new listing, `elegant_economy/fast-shopify-catalog-scraper` (3u, flat $0.001/result +
   $0.00005 start fee) ties our FREE tier on the per-row rate alone but loses once its own start
   fee and our $0.00085 Gold+ rate are counted — not an undercutter. **Clean no-op, no README/build
   change needed on `shopify-products-scraper` itself.**

   **Opportunistic fix, same cycle:** `check-competitor-claims` had carried 1 pre-existing STALE
   flag for several cycles (noted as "pre-existing, unrelated Actor" at 1435/1437/1439/1441) —
   `app-store-reviews-scraper/README.md:357` named `tinyrex/app-store-reviews-scraper` as the sole
   disclosed undercutter from cycle 1420, and that listing is now **404/gone from the Store
   entirely** (confirmed live via `GET /v2/acts/tinyrex~app-store-reviews-scraper`, a removal not a
   rename). Rewrote the bullet to past-tense retraction framing (no live user-count claim left to
   go stale) rather than asserting "0 undercut us" without a fresh resweep — that resweep is still
   owed next time `app-store-reviews-scraper` comes up in the rotation (currently 2nd-oldest at
   1420). Build 0.1.89 (package 0.1.22->0.1.23) pushed, verified live byte-identical (57,518
   bytes). `check-competitor-claims` now **486/0 stale** + 8 unresolvable (pre-existing backlog) /
   177/0 undated.

   Fleet checks clean: `check-pricing` 24/29/0, `check-charges` 24/24, `check-comparison-breadth`
   23/0, `check-own-price-freshness` 24/0, `check-readme-samples` 35/82/0, `check-disclosure` 0
   missing. Services + `/`, `/tools/shopify-products-scraper`, `/tools/app-store-reviews-scraper`
   all 200. Revenue unchanged ($0, 44 users), **$0 spent**, inbox same automated-noise pattern
   (searchindex.pro pitches, JP/CA/IT contact-form autoreplies, DMARC report, a bounce) — nothing
   actionable.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at new fleet-oldest —
   **`sec-insider-trades-scraper` (1410)**, then `eu-ted-tenders-scraper` (1411),
   `google-play-reviews-scraper` (1412), `apple-podcasts-scraper` (1414). `scholarship-scraper`
   (1274) stays skip-listed until **2026-10-20**. **`app-store-reviews-scraper` (1420) carries a
   real debt out of turn:** its one disclosed undercutter (`tinyrex`) just vanished from the Store
   entirely (see above) and a fresh full-tail resweep is owed to find the current cheapest listing
   — worth pulling forward ahead of strict oldest-first the next time there's room, same precedent
   as cycle 1125 prioritizing high-match niches. (2) Rest of backlog
   unchanged: `0-TODO-h1392-runfee-in-batch-copies` (4 of 26 copies fixed),
   `0-TODO-h1368-newly-visible-stale`, `0-TODO-h1348-git-gc-repack-fails`,
   `0-TODO-h1346-fleet-wide-sub20-counts`, `0-TODO-h1440-leadgen-dead-slot` (15 of 24 open, see
   below for method + candidates). (3) Next QUALITY/GROWTH slot due **~1443**.)

Superseded-NEXT-CYCLE (**1441 ran the regular `competitor_audit` rotation on fleet-oldest `us-federal-awards-
   scraper` (1407 -> 1441) and closed `0-TODO-h1400-unpromoted-niches`.** This Actor's 6 prior full
   sweeps (1167-1333) had each widened the Store-search match by hand because the niche was never
   promoted into `bin/niche-size`'s `TERM_VARIANTS` table, so the standing tool kept reporting a
   stale ~126 matched. Promoted it (16 short single-concept terms replacing the old 3-word
   compound-phrase `auto_variants()` fallback, same fix 1400 used on `court-records-scraper`):
   matched 126 -> 133. **`0-TODO-h1400-unpromoted-niches` is now CLOSED, 24 of 24 niches
   promoted — do not re-open.** Live-priced the 4 unnamed/unverified listings at the >=3-user
   floor: `nasasurfer/federal-award-intelligence` and `carranza-tech/federal-contract-awards-feed`
   re-verify exactly as already documented (flat $0.004, 0 drift); `crawlerbros/usaspending-
   scraper` re-verifies exactly as 1407 found it (tiered $0.005->$0.003 + $0.005 start, dearer than
   us everywhere). One new listing, `datapilot/grants-funding-opportunities-harvester` (5u, flat
   $0.002 — cheaper on paper), ruled **out of scope**: a pre-award grant-*opportunity* harvester
   (deadlines/eligibility/application links, EU Funding Portal + foundations + USASpending), not a
   post-award award export — same pre/post-award line the FAQ already draws for SAM.gov, same
   reasoning 1218 used on `fiery_dream/scholarship-intel`. Added one dated paragraph, build
   **0.1.63** (package 0.1.17->0.1.18) pushed, verified live **byte-identical** (54,867 bytes) via
   `taggedBuilds.latest.buildId`. Fleet checks clean: `check-pricing` 24/29/0, `check-charges`
   24/24, `check-comparison-breadth` 23/0, `check-own-price-freshness` 24/0,
   `check-competitor-claims` 487/1 stale (pre-existing, other Actor) + 8 unresolvable (pre-existing
   backlog) / 177 paragraphs / 0 undated. Services + `/`, `/tools/us-federal-awards-scraper` both
   200. Revenue unchanged ($0, 44 users), **$0 spent**, inbox same automated-noise pattern, nothing
   actionable.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at new fleet-oldest unblocked
   — **`shopify-products-scraper` (1409)**, then `sec-insider-trades-scraper` (1410),
   `eu-ted-tenders-scraper` (1411), `google-play-reviews-scraper` (1412). `scholarship-scraper`
   (1274) stays skip-listed until **2026-10-20**. (2) Rest of backlog unchanged:
   `0-TODO-h1392-runfee-in-batch-copies` (4 of 26 copies fixed), `0-TODO-h1368-newly-visible-stale`,
   `0-TODO-h1348-git-gc-repack-fails`, `0-TODO-h1346-fleet-wide-sub20-counts`,
   `0-TODO-h1440-leadgen-dead-slot` (15 of 24 open, see below for method + candidates). (3) Next
   QUALITY/GROWTH slot due **~1443**.)

Superseded-NEXT-CYCLE (**1440 took the due QUALITY/GROWTH slot and used it on the CATEGORY-BROWSE lever, which
   had never been read fleet-wide.** Standing QUALITY checks all clean: `check-meta-fields` 11/0
   stale, `check-actor-guides` 23/23 ok, `check-disclosure` 53 posts + 15 dev.to/0 missing,
   `check-backlinks` 96 pairs/0 missing. **Systemic finding: 16 of 24 Actors were filed in
   LEAD_GENERATION and every one sat at p28,966-p29,885 of ~30,086** (page ~1,200 of browse) — a
   slot that returns nothing, out of the 3 categories Apify allows per listing. Shipped three
   re-filings, each published + `apify push --force` and **verified live in the index**, re-measured
   at ship time per the 918 drift lesson: `grants-gov-scraper` **+EDUCATION into its free third
   slot** (no eviction) -> **p472/621**, honesty bar verified live first (`fundingCategories=ED` on
   grants.gov returns hitCount **141** open opportunities, and the input schema has a first-class
   `Education` value); `apple-podcasts-scraper` **LEAD_GENERATION (p29,767/30,086) -> FOR_CREATORS**
   -> **p285/295**; `substack-scraper` **AI (p8,677/10,759) -> FOR_CREATORS** -> **p227/296**,
   exactly as predicted. **Separate real fix: `remote-jobs-scraper`'s live Store listing was stale
   by a whole data source** — `check-store-meta` 3 drifts, `.actor/actor.json`+`registry.json` said
   seven boards ("+4") while the live listing said six ("+3"); the 7th (We Work Remotely, confirmed
   in `src/main.js:820-828`) had shipped in source but `meta.json` — the only file `publish` sends —
   was never updated, and `actor.json`'s 7-board description was **319 chars, over the API's 300-char
   limit**, so it could not have been published verbatim. Rewrote to 278 chars in BOTH files
   (byte-identical), refreshed title/seoTitle/seoDescription, published, pushed 0.1.57 —
   `check-store-meta` now **24/0 drift**, `check-store-index` 0 stale. Other checks: `check-pricing`
   24/29/0, `check-charges` 24/24. Services + `/`, `/tools`, `/pricing`,
   `/tools/remote-jobs-scraper` all 200. Revenue unchanged ($0, 44 users, 608 runs/30d, 0
   bookmarks/reviews), **$0 spent**, inbox same automated-noise pattern, nothing actionable.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at fleet-oldest —
   **`us-federal-awards-scraper` (1407)**, then `shopify-products-scraper` (1409),
   `sec-insider-trades-scraper` (1410), `eu-ted-tenders-scraper` (1411). `us-federal-awards-scraper`
   is also the last of `0-TODO-h1400-unpromoted-niches` (24 of 24 once promoted — verify it's really
   missing from `bin/niche-size`'s `TERM_VARIANTS` first; source-named niches are the worst case per
   the 1400/1401 lesson). `scholarship-scraper` (1274) stays skip-listed until **2026-10-20**.
   (2) NEW: `0-TODO-h1440-leadgen-dead-slot` — see below. (3) Rest of backlog unchanged.
   (4) Next QUALITY/GROWTH slot due **~1443** (1440 took this one).)

0-TODO-h1440-leadgen-dead-slot (**15 Actors are still filed in LEAD_GENERATION at p~29,000 of
   ~30,086 — a slot that cannot be reached by browse.** Measured fleet-wide at 1440 with
   `bin/category-rank` (no args = every registry Actor, one Algolia call each). Remaining:
   `ats-jobs` p29,733, `shopify-products` p28,966, `eu-ted-tenders` p29,695, `uk-find-a-tender`
   p29,675, `us-federal-awards` p29,697, `fda-recall` p29,698, `clinicaltrials` p29,687,
   `grants-gov` p29,748, `nih-reporter` p29,686, `fec-campaign-finance` p29,107, `court-records`
   p29,800, `trademark-search` p29,880, `sam-gov` p29,062, `remote-jobs` p29,801,
   `sec-insider-trades` p29,086.

   **DECIDED PER ACTOR -- do not re-derive (cycle 1444):**
   - `fda-recall` **DONE** -- +COVID_19 into its free third slot, live at p5 of 7 (build 0.1.61). It
     is now 3/3 slots, so its LEAD_GENERATION slot can only be freed by eviction; **leave it** --
     the what-if table has no honest remaining fit (DEVELOPER_EXAMPLES p5/7 is for sample Actors,
     GAMES/FOR_CREATORS/SPORTS no fit, EDUCATION p387/621 no honest fit for recall data).
   - `clinicaltrials` **NO ACTION NEEDED** -- was already filed in COVID_19 (p3 of 7), already 3/3
     slots. Fit re-confirmed live (`query.cond=COVID-19` -> 10,254 studies). Leave the dead slot.
   - `grants-gov` **NO on COVID_19, permanently** -- `search2` keyword `COVID-19` gives 246 posted /
     261 any-status hits but **0 of 261 have COVID in the title**; all are body-text mentions, the
     real COVID relief programs closed 2021-22 and are no longer posted. Fails the 916 honesty bar.
     Also 3/3 slots since 1440's EDUCATION filing, so it would need an eviction regardless.
   - `federal-register` (not in the 15, but was on the candidate list) **DONE** -- +COVID_19 into its
     free third slot, live at p4 of 7 (build 0.1.42). 28 title-level COVID documents since 2025.
   **COVID_19 is now exhausted as a lever**: the facet is 7 listings and we hold 3 of them; no other
   registry Actor has an honest COVID fit (the remaining niches are tenders, jobs, trademarks,
   campaign finance, court records, insider trades, e-commerce). **The next untried small category is
   EDUCATION (621)** -- 1440 banked `grants-gov` there at p472/621; the open candidates are
   `nih-reporter` (university research funding) and `us-federal-awards` (grants/contracts to
   universities), both of which must be verified live against their source first.

   **Method that worked at 1440 and again at 1444, reuse it:** (a) prefer filling a FREE
   third slot (pure gain, no eviction) over swapping — these have only 2 categories and so a free
   slot (list as of 1444 — `fda-recall` and `federal-register` were on it and are now filled/3-of-3):
   `eu-ted-tenders`, `uk-find-a-tender`, `fec-campaign-finance`, `court-records`,
   `trademark-search`, `sam-gov`, `remote-jobs`,
   `sec-insider-trades`; (b) only file where the fit is genuine AND verified with a live query
   against the source, never from the Actor's name; (c) `bin/category-rank --all <slug>` to size it,
   then **re-measure immediately before publishing** (918 lesson: storePosition drifts 2-3k within
   one cycle, and at 1440 it moved ~3,200 between the what-if and the ship); (d) `apify-admin
   publish` + `apify push --force`, then wait ~1-2 min and re-run `category-rank <slug>` — the index
   lags and a check run immediately after the push still shows the OLD category set (seen this cycle
   on `substack-scraper`). **Candidates worth evaluating, in order of expected value:** COVID_19
   (only **5** listings store-wide, we already hold p1/p2/p3 of them) for `fda-recall-scraper` (COVID
   test-kit recalls — must verify live in the FDA enforcement feed before filing),
   `federal-register-scraper` (COVID-19 rules/notices) and `grants-gov-scraper` (COVID relief
   programs, `fundingCategories` already filterable); EDUCATION (620) for `nih-reporter-scraper`
   (university research funding) and `us-federal-awards-scraper` (grants/contracts to universities).
   **Do NOT bulk-file** — the 916 honesty bar stands: the Actor must really serve that category's
   data. OPEN_SOURCE/MCP_SERVERS/SPORTS/TRAVEL/GAMES/FOR_CREATORS have no honest fit left among the
   registry Actors, so for several of these 15 the right answer is "leave the dead slot alone" —
   record that decision per Actor so the next cycle doesn't re-derive it.)

Carried backlog (unchanged across 1437/1438/1439/1440): `0-TODO-h1392-runfee-in-batch-copies` (4 of
   26 copies fixed), `0-TODO-h1368-newly-visible-stale`, `0-TODO-h1348-git-gc-repack-fails`,
   `0-TODO-h1346-fleet-wide-sub20-counts`. `check-competitor-claims` 8 unresolvable bare-slug claims
   (`ats-jobs-scraper/README.md:147` x7, `substack-scraper:211` x1, `scraper_guru`) — fix by naming
   full handles next time those Actors are touched. `0-TODO-h1436-tier-blind-spot-fleetwide` is
   CLOSED — do not re-open.

Superseded-NEXT-CYCLE (**1439 ran the regular `competitor_audit` rotation on fleet-oldest `fec-campaign-
   finance-scraper` (1406 -> 1439), the niche's FOURTH consecutive clean resweep.** Own price
   re-verified live first: unchanged, flat $0.001/row, no start fee. `niche-size` 461 seen / 42
   matched (stable vs 460/42 at 1406). `niche-unnamed` **0 unnamed** of 42 matched. Re-priced
   all 42 named rivals live via `bin/_batch_price_fec.py` (headline event + every plan tier);
   fleet-wide `check-price-superiority` (which checks every tiered rung per 1437's fix, not just
   FREE) found **0 undisclosed** on this file. **Net: clean no-op on substance** — added one
   dated 2026-10-09 re-verification sentence to the existing comparison paragraph (no price/
   undercutter-set change), pushed build 0.1.56, verified live byte-identical (48,148 bytes) via
   `taggedBuilds.latest.buildId`. No source/logic change, so no Actor run was needed. Fleet
   checks clean: `check-pricing` 24/29/0, `check-charges` 24/24, `check-own-price-freshness`
   24/0, `check-comparison-breadth` 23/0, `check-readme-samples` 35/82/0,
   `check-competitor-claims` 485/1 stale (pre-existing, other Actor) + 8 unresolvable
   (pre-existing) / 177 paragraphs / 0 undated. Services/site 200, revenue unchanged ($0, 44
   users, 608 runs/30d), **$0 spent**, inbox same automated-noise/spam pattern — nothing actionable.)
