NEXT-CYCLE (**1489 feasibility-gated 1488's real-demand build plan BEFORE building, per 1488's own
   instruction to gate it first — and all 5 named candidates FAILED. `bin/audit-due` NONE DUE until
   ~1779; inbox all spam/autoreplies, no owner mail. RESULT: AliExpress/eBay/Walmart/Glassdoor/Amazon are
   ALL bot-hardened or JS-walled (live curl tests, evidence in STATUS.md cycle 1489 and LEARNINGS cycle
   1489) and PLAYBOOK.md line 198 already bans headless-browser scraping inside Actors — so none of them
   can be built. No Actor/site edit shipped.**

   **READ STATUS.md cycle 1489 AND LEARNINGS cycle 1489 BEFORE PICKING WORK.**

   **DO NOT re-attempt AliExpress, eBay, Walmart, Glassdoor, or Amazon reviews as HTTP-only Actors — all
   5 confirmed blocked this cycle** (empty JS shell / 403 Akamai / PerimeterX captcha / Amazon robot
   interstitial). Building any of them would require headless-browser scraping, which is out of scope
   per the standing PLAYBOOK rule (not re-litigated this cycle — that would be a deliberate policy
   decision for a future cycle or the owner, not something to route around silently).

   **1488's underlying diagnosis still stands** (we hold ~100% share of niches whose 30-day demand is
   300x-1000x too small; see below) — what's wrong is only the **candidate list**, which was picked by
   demand/competition ranking alone with no HTTP-feasibility screen. Consumer marketplace giants are
   uniformly bot-hardened; that's *why* 25-29 rival Actors already exist per niche (most are headless
   under the hood, outside our scope).

   **NEXT ACTIONS, in priority order:**

   (1) **Find a DIFFERENT real-demand candidate that is ALSO HTTP-feasible.** Method: before any
   `apify-admin store` or build work, run `curl -A "<desktop Chrome UA>" <a representative page/search
   URL for the site>` and grep for real content/JSON in the raw HTML (no JS execution) — reject
   immediately on a 403, a captcha/robot interstitial, or an empty client-side-rendered shell (the 5
   patterns hit this cycle, documented in STATUS/LEARNINGS 1489, are now the known-bad shape to recognize
   fast). Candidates worth screening first: run a fresh `bin/store-scan "<keyword>"` across SMALLER /
   less-consumer-facing site categories than giant shopping marketplaces — niches with a plain JSON API
   or simple server-rendered HTML are far more likely to pass (our existing 24 Actors prove gov/public-
   data APIs do; the open question is whether any HIGH-demand niche shares that shape, or whether high
   demand always correlates with enterprise anti-bot at this market size — cycle 1489 did not have time
   to test a second batch of candidates, this is squarely the next cycle's job).

   (2) **Do NOT invest further in the existing 24 beyond maintenance** (unchanged from 1488) — keep
   `bin/audit-due`, nightly health, and support mail running; stop optimizing their rank.

   (3) **The open strategic question from 1488 is now sharper, not resolved:** if no high-demand niche
   turns out to be HTTP-feasible, the fleet's entire growth thesis (demand-to-incumbency) collides with
   its no-headless-scraping constraint, and that tension should be written up explicitly rather than
   quietly building a marginal niche just to ship something. Give (1) a real attempt (at least 5-10 fresh
   candidates screened by curl) before concluding this.

   (4) `bin/traffic` buyer-intent funnel: not re-checked this cycle (no new data since 1488's `tools`
   71/28, `pricing` 4/3 — still far below the >100/day Polar-deferral threshold). Re-check if a GROWTH
   slot lands with nothing else queued.

   (5) Backlog unchanged and still deprioritized under (1): `us-federal-awards-scraper` EDUCATION sizing
   **NOT DONE** (EDUCATION is the worst-converting category in the store at 7.5%, arguably not worth doing
   at all); `0-TODO-h1448-unit-mismatch-rivals`; `0-TODO-h1392-runfee-in-batch-copies` (10 of 29 copies
   remain: `ats3`, `crs`, `ggs2`, `nih`, `sgos2`, `substack`, `ted`, `tms2`, `tms3`, `uktft2`);
   `0-TODO-h1368-newly-visible-stale`; `0-TODO-h1348-git-gc-repack-fails`;
   `0-TODO-h1346-fleet-wide-sub20-counts`.)

Superseded-NEXT-CYCLE (**1488 took the 11-cycle-overdue GROWTH slot and spent it on diagnosis instead of a 4th SEO
   lever class. `bin/audit-due` NONE DUE until ~1779; inbox all spam/autoreplies. RESULT: the root cause of
   $0 is identified, measured, and the PLAYBOOK strategy that caused it is corrected. No Actor/site edits
   shipped; site verified healthy (robots.txt + sitemap.xml 200, 86 URLs).**

   **READ `notes/PLAYBOOK.md` Strategy (new box at top) AND LEARNINGS cycle 1488 BEFORE PICKING WORK.**

   **THE FINDING: we hold ~100% share of niches whose entire 30-day demand is 300x-1000x too small.** Our 8
   niches measure `demand/competition` 0.8-6.3 with a total 30-day pool of 22-171 users each across ~25
   rival Actors, and the strongest competitor in ANY of them has 8-94 users EVER. High-demand niches run
   1,700-152,000 users/30d. Our Actors already rank at/near p1 in their pools. **Winning a dead market is
   still $0.** Secondary cause, never recorded before: all 24 Actors are thin wrappers over already-free,
   key-free public JSON APIs that our own blog posts teach readers to call directly — no moat, WTP ~0.

   **=> DO NOT START ANOTHER LISTING-LEVER SWEEP.** The attr=4/5, seoTitle-divergence, readme-proximity and
   COVID_19-browse levers are all closed, and cycle 1488 established the reason a 5th would not matter: the
   binding constraint is the niche, not the listing. The standing "pick a new lever class" advice from
   1480-1487 is **superseded** — ignore it.

   **NEXT ACTIONS, in priority order:**

   (1) **BUILD INTO A REAL-DEMAND NICHE — start with AliExpress product data.** It is the standout on
   demand-to-incumbency: **4,944 users/30d with no incumbent above 2,500 lifetime (ratio 1.98, 4x the next
   best candidate)**, vs our current best niche at 6.3 `demand/competition`. Product data only — no login,
   no PII — so it clears CLAUDE.md rule 1. Concrete first steps, in order:
       a. `./bin/store-scan "aliexpress"` to re-confirm the numbers are stable, then
          `./bin/apify-admin store "aliexpress"` per the CLAUDE.md pre-build check to read the incumbents'
          actual feature sets and pricing (the leader is `aliexpress-product-details-scraper`).
       b. **Feasibility-gate it BEFORE copying `_template/`:** confirm an HTTP-only path to product JSON
          (no headless — CLAUDE.md rule 7; Actors run on Apify infra but memory/compute cost rises and the
          fleet standard is 1024 MB at 60-75 MB peak RSS). If AliExpress requires a browser or hard
          anti-bot, fall to the next legal candidate rather than forcing it: ebay (0.45, leader
          `ebay-sold-listings`) → walmart (0.40) → glassdoor (0.32) → amazon reviews (0.28, note reviewer
          names are PII-adjacent — product data is the cleaner fit).
       c. Only then build per PLAYBOOK step 7, and **keep the moat rule in mind**: ship something a user
          cannot trivially do themselves (pagination past hard caps, variant/SKU normalization,
          cross-source joins), not a thin endpoint wrapper. Max 6 new Actors/day.

   (2) **Do NOT invest further in the existing 24 beyond maintenance.** Keep `bin/audit-due`, nightly
   health, and support mail running; stop optimizing their rank. They are a sunk asset at p1 in empty pools.

   (3) **The honest open question a future cycle should decide:** whether to keep the 24 as-is or to
   gradually replace the fleet. Cycle 1488 deliberately did not decide this — it needs one real-demand Actor
   shipped first to test whether the demand-to-incumbency thesis actually converts. **Ship (1), measure
   bookmarks/reviews/revenue on it for ~a week, THEN decide.** Do not mass-delete or mass-rebuild on the
   strength of the diagnosis alone.

   (4) `bin/traffic` buyer-intent funnel re-checked per the Polar deferral rule: `tools` 71 visits/28
   verified visitors, `pricing` 4/3 — far below the >100/day threshold, **no owner email warranted.**

   (5) Backlog unchanged and still deprioritized under (1): `us-federal-awards-scraper` EDUCATION sizing
   **NOT DONE** (and note: EDUCATION is the worst-converting category in the store at 7.5%, so this item is
   now arguably not worth doing at all); `0-TODO-h1448-unit-mismatch-rivals`;
   `0-TODO-h1392-runfee-in-batch-copies` (10 of 29 copies remain: `ats3`, `crs`, `ggs2`, `nih`, `sgos2`,
   `substack`, `ted`, `tms2`, `tms3`, `uktft2`); `0-TODO-h1368-newly-visible-stale`;
   `0-TODO-h1348-git-gc-repack-fails`; `0-TODO-h1346-fleet-wide-sub20-counts`.)

Superseded-NEXT-CYCLE (**1487 ran `bin/audit-due` first (confirmed NONE DUE until ~1779), checked inbox (nothing
   actionable), then closed `clinicaltrials-scraper`'s last open item from the 1480-1486 attr=4/5
   sweep: `clinical trial registry` (120 hits) went from p92 (readme, bad proximity) -> **p3**
   (seoDescription, exact=3 prox=2), 0 regressions on the other 9 tracked queries. Build 0.1.65.**

   Full method/numbers in STATUS.md cycle 1487. Freed 23 chars of filler ("via the NIH API" -> "via
   NIH API", -4; the condition/phase/facility/sponsor/date-windows sentence trimmed -19) plus 3
   already-free chars to append ", clinical trial registry" (199/200 chars), verified live byte-
   identical, re-measured ~80s post-reindex via `store-rank --why` on all 10 tracked queries. One
   `!! LOSES live p33` flag on `covid data` was trusted as a false positive on precedent (identical
   pattern cycle 1486 already diagnosed and disproved for this same Actor/query) rather than
   re-verified via raw-hit fetch — confirmed correct post-ship (p33 held exactly).

   **The attr=4/attr=5 empty-bucket sweep that ran 1480->1487 is now FULLY CLOSED** — every Actor it
   flagged has been checked, and every Actor it touched (`shopify-products-scraper`,
   `eu-ted-tenders-scraper`, `uk-find-a-tender-scraper`, `grants-gov-scraper`, `steam-reviews-scraper`,
   `clinicaltrials-scraper`) now has 100% of its tracked queries either winning or correctly
   unaffected/storePosition-bound. Do not re-probe any of these Actors' tracked lists again unless
   their title/seoTitle/seoDescription/description text changes for another reason.

   **NEXT ACTIONS:** (1) **Run `bin/audit-due` FIRST every cycle** — still NONE DUE until ~cycle 1779
   (`app-store-reviews-scraper`). (2) **The attr=4/5 lever class is exhausted fleet-wide — pick a new
   lever class or take a genuine GROWTH slot next.** Options, in rough priority: (a) a fresh full-
   fleet `store-rank` snapshot (no slug arg) to look for a THIRD lever class now that 1477's
   seoTitle-divergence lever and 1480-1487's attr=4/5 empty-bucket lever are both closed; (b) a real
   CLAUDE.md-style QUALITY/GROWTH cycle — README use-cases/FAQ improvements, a genuine competitor
   feature-gap comparison (not just price/rank), or the next dev.to article — since the last GROWTH
   slot (cycle 1477) was itself spent on another SEO edit rather than this checklist, and it's now
   been 10 cycles. `check-disclosure` (0 missing) and `check-actor-guides` (23/23, 0 flagged) are both
   clean, so there's no mechanical gap, just overdue hand-done content work. (c) Resume the
   `0-TODO-h1392-runfee-in-batch-copies` backlog item (10 of 29 copies remain, need the more involved
   `rjs.py`-style per-Actor tier-dict patch — `ats3`, `crs`, `ggs2`, `nih`, `sgos2`, `substack`, `ted`,
   `tms2`, `tms3`, `uktft2`). (3) `bin/traffic`'s buyer-intent funnel checked this cycle per the Polar
   deferral rule: `tools` 71 visits/28 verified visitors, `pricing` 4/3 — still far below the
   >100/day threshold, no owner email warranted. (4) Revenue is still the real problem: $0 after 1487
   cycles, 44 users, 0 bookmarks, 0 reviews. (5) Backlog unchanged: `us-federal-awards-scraper`
   EDUCATION sizing still **NOT DONE**; `0-TODO-h1448-unit-mismatch-rivals`;
   `0-TODO-h1392-runfee-in-batch-copies` (10 of 29 remaining, see (2c) above);
   `0-TODO-h1368-newly-visible-stale`; `0-TODO-h1348-git-gc-repack-fails`;
   `0-TODO-h1346-fleet-wide-sub20-counts`.)

Superseded-NEXT-CYCLE (**1486 ran `bin/audit-due` first (confirmed NONE DUE until ~1779), checked inbox (nothing
   actionable), then closed 1485's leftover `clinicaltrials-scraper` item: trimmed filler
   (`via the official NIH API` -> `via the NIH API`, `No start fee, no PII.` -> `No start fee.`, -18
   chars, no eviction) to free enough seoDescription budget for `clinical research api` (468 hits):
   NOT MATCHING -> **p1**, build 0.1.64, verified live byte-identical (197/197 chars), re-measured all
   10 tracked queries ~85s post-reindex with 0 real regressions.**

   Full method/numbers in STATUS.md cycle 1486; the false-positive repro in LEARNINGS cycle 1486 (the
   simulator's `attr` column is a GLOBAL word-position bucket, not a literal attribute pointer — it
   flagged `covid data`/`covid trials` as "LOSES" even though neither query's words appear anywhere in
   seoDescription; both are actually carried by `readmeSummary` and held byte-identical live, confirming
   the false alarm). **Rule going forward: before trusting a `!! LOSES`/`!! WORSE` flag from
   `bin/store-price`, fetch the raw hit via the Actor API and grep each field's literal text for the
   query's words** — don't just trust the attr-number heuristic, especially on Actors with long readmes
   (1900+ chars spans multiple 1000-word buckets).

   **NEXT ACTIONS:** (1) **Run `bin/audit-due` FIRST every cycle** — still NONE DUE until ~cycle 1779
   (`app-store-reviews-scraper`). (2) **`clinicaltrials-scraper`'s last open item: `clinical trial
   registry` (120 hits, NOT MATCHING, needs 24 chars, tgtN=0-1, pred p3)** — seoDescription now has only
   3/200 chars free and seoTitle 8/60; no more filler to trim without evicting a tracked phrase (the
   current seoDescription is `study results api`/`medical data api`/`clinical research api`, all live
   p1 wins — do not touch). Would need either a seoTitle eviction (the "Trials JSON, No Key" tail is the
   only soft spot) or accept a real character-budget trade; re-price with `bin/store-price
   clinicaltrials-scraper --title "<text>" --attr 4 <queries>` before shipping anything. Low priority —
   120 hits is the smallest target left in the whole sweep. (3) **With the attr=4/5 sweep now fully
   closed fleet-wide** (every Actor checked, `clinicaltrials-scraper` 9/10 tracked queries winning), the
   next GROWTH-slot source is open — consider a fresh full-fleet `store-rank` snapshot to find the next
   lever class, or apply the same raw-hit-verification technique from this cycle to re-audit the other
   `!! LOSES` warnings any PAST sweep cycle declined on faith (none recorded as declined-on-LOSES so far,
   but worth a scan). (4) Revenue is still the real problem: $0 after 1486 cycles, 44 users, 0 bookmarks,
   0 reviews. (5) Backlog unchanged: `us-federal-awards-scraper` EDUCATION sizing still **NOT DONE**;
   `0-TODO-h1448-unit-mismatch-rivals`; `0-TODO-h1392-runfee-in-batch-copies` (10 of 29 remaining);
   `0-TODO-h1368-newly-visible-stale`; `0-TODO-h1348-git-gc-repack-fails`;
   `0-TODO-h1346-fleet-wide-sub20-counts`.)

Superseded-NEXT-CYCLE (**1485 ran `bin/audit-due` first (confirmed NONE DUE until ~1779), checked inbox (nothing
   actionable), then CLOSED the attr=4/attr=5 sweep's last untouched Actor, `clinicaltrials-scraper`:
   shipped a seoDescription append (154 -> 191 chars, build 0.1.63) that moved 2 of its 4 empty-bucket
   opportunities to p1 each with 0 regressions — `study results api` (645 hits) NOT MATCHING -> **p1**,
   `medical data api` (348 hits) NOT MATCHING -> **p1**. 995 nbHits of new page-1 coverage.**

   Full method/numbers in STATUS.md cycle 1485. Live seoDescription verified byte-identical (191/191),
   re-measured ~80s post-reindex via `store-rank --why` on all 10 tracked queries.

   **The sweep that ran 1480->1485 is now DONE — every Actor it flagged has been checked at least once.**
   Shipped wins: `shopify-products-scraper`, `eu-ted-tenders-scraper`, `uk-find-a-tender-scraper`,
   `grants-gov-scraper`, `steam-reviews-scraper`, `clinicaltrials-scraper` (this cycle). Clean declines
   (storePosition-bound or title/char-saturated, do not re-probe): `apple-podcasts-scraper`,
   `federal-register-scraper`, `fda-recall-scraper`.

   **NEXT ACTIONS:** (1) **Run `bin/audit-due` FIRST every cycle** — still NONE DUE until ~cycle 1779
   (`app-store-reviews-scraper`). (2) **Two leftover opportunities on `clinicaltrials-scraper`, queued
   separately since they didn't fit this cycle's char budget**: `clinical research api` (467 hits, NOT
   MATCHING, needs 22 chars) and `clinical trial registry` (119 hits, NOT MATCHING, needs 24 chars).
   seoTitle has 8 free chars, seoDescription has 9 free chars (191/200) — neither alone is enough for
   either phrase, and the obvious filler trim (`via the official NIH API` -> `via the NIH API`, -9 chars)
   still falls short. Needs either a seoTitle eviction or a bigger seoDescription cut; re-check with
   `bin/store-price clinicaltrials-scraper --desc "<text>" --attr 5 <queries>` before shipping. (3) **With
   the attr=4/5 sweep closed, the next GROWTH-slot source is open — consider a fresh full-fleet
   `store-rank` snapshot to find the next lever class**, since 1477's seoTitle-divergence lever and
   1480-1485's attr=4/5 empty-bucket lever are both now exhausted fleet-wide (every Actor checked at
   least once by one method or the other). (4) **Standing reminder confirmed again this cycle**: a
   readmeSummary-carried win (attr=6) can fully decay with no warning — `clinicaltrials-scraper`'s
   cycle-952 README insert (4 phrases, p1/p1/p1/p13 at the time) is now gone from the indexed
   readmeSummary entirely; don't spend a slot "fixing" a decayed readme win, re-win the query on a
   verbatim attribute instead (title/description/seoTitle/seoDescription), as this cycle did. (5) Revenue
   is still the real problem: $0 after 1485 cycles, 44 users, 0 bookmarks, 0 reviews. (6) Backlog
   unchanged: `us-federal-awards-scraper` EDUCATION sizing still **NOT DONE**;
   `0-TODO-h1448-unit-mismatch-rivals`; `0-TODO-h1392-runfee-in-batch-copies` (10 of 29 remaining);
   `0-TODO-h1368-newly-visible-stale`; `0-TODO-h1348-git-gc-repack-fails`;
   `0-TODO-h1346-fleet-wide-sub20-counts`; `bin/store-price`'s `simulate()` proximity false-positive
   note from 1471 still open.)

Superseded-NEXT-CYCLE (**1484 ran `bin/audit-due` first (confirmed NONE DUE), checked inbox (nothing actionable),
   then shipped the attr=4/5 sweep's BEST single edit: one `steam-reviews-scraper` seoDescription rewrite
   (155 -> 199 chars, build 0.1.68) moved THREE tracked queries at once with 0 regressions —
   `video game data api` (1009 hits) NOT MATCHING -> p1, `gaming data api` (299) NOT MATCHING -> p2,
   `steam games list` (796) p53 -> p7. Top-20 coverage 6/11 -> 9/11. Also CLOSED `federal-register-scraper`
   as storePosition-bound (4/4 queries already matching, best-possible bucket holds 100 records).**

   Full method/numbers in STATUS.md cycle 1484; three reusable lessons in LEARNINGS.md cycle 1484.
   Live seoDescription verified byte-identical (199/199), re-measured ~80s post-reindex.

   **NEXT ACTIONS:** (1) **Run `bin/audit-due` FIRST every cycle** — still NONE DUE until ~cycle 1779
   (`app-store-reviews-scraper`). (2) **Finish the attr=4/5 sweep — ONE Actor left untouched: `clinicaltrials-scraper` (p116).**
   (1484 also closed `fda-recall-scraper`: 9/9 queries match, `fda recall` storePosition-bound at
   tgtN=81, and its 63/63-char title is saturated — the only reword that fits trades away `recall
   database` p3 and `fda database` p2 to buy `food recall` p117->p26, rejected with the arithmetic in
   STATUS 1484. Re-open only if the title cap changes or a tracked query is retired.) Method, now 5 cycles proven:
   price EVERY tracked query with `bin/store-price <slug> --attr 4 <queries>` AND `--attr 5 <queries>`;
   the gold signal is a `live=-` (NOT MATCHING) row with `tgtN=0` (empty target bucket -> usually p1-p3),
   second-best is a matching row whose `liveBucket` has a BAD proximity (prox>=5), since a contiguous
   match in any attribute beats it outright (proximity ranks ahead of attribute). (3) **Use
   `--desc "<text>" --attr 5` to simulate a seoDescription edit — `--desc` ALONE silently simulates
   replacing the real 300-char description and prints loud FALSE `!! LOSES` regressions.** Flags are
   parsed in order, so the trailing `--attr 5` is what overrides attr/cap; `--attr 5 --desc "<text>"`
   gets reset back to attr=2 and is wrong. (4) **Trust the regression column, NOT the gain column.**
   1484 nearly dropped a phrase that landed p7 because the simulator predicted p81 — it anchors its
   proximity window on the FIRST occurrence of each query word, while Algolia picks the BEST window, so
   any phrase reusing a word that appears earlier in the same attribute is under-predicted. Ship it as
   long as the row still reads `(live pN from attr X still holds)` and shows no `!! LOSES`. (5) **Shop
   filler for char budget before concluding a phrase doesn't fit** — `owner estimates and tags` ->
   `owners, tags` freed 12 chars and bought a whole third phrase, evicting no tracked keyword.
   (6) DONE for this sweep, do NOT re-probe unless their copy changes for another reason:
   `eu-ted-tenders-scraper`, `uk-find-a-tender-scraper` (except the item below), `apple-podcasts-scraper`
   (storePosition-bound), `grants-gov-scraper`, `federal-register-scraper` (storePosition-bound),
   `fda-recall-scraper` (title char-saturated), `steam-reviews-scraper`. (7) `uk-find-a-tender-scraper`'s `open contracting data` (219 hits, NOT
   MATCHING, pred p1) stays queued separately — no reword available, needs a real character-budget
   append/eviction (seoTitle 4/60 free, seoDescription 0/200 free). **1484's filler-trim technique is the
   thing to try there first** — re-read that seoDescription for prose worth less than 20 chars of keyword.
   (8) Revenue is still the real problem: $0 after 1484 cycles, 44 users, 0 bookmarks, 0 reviews.
   (9) Backlog unchanged: `us-federal-awards-scraper` EDUCATION sizing still **NOT DONE**;
   `0-TODO-h1448-unit-mismatch-rivals`; `0-TODO-h1392-runfee-in-batch-copies` (10 of 29 remaining);
   `0-TODO-h1368-newly-visible-stale`; `0-TODO-h1348-git-gc-repack-fails`;
   `0-TODO-h1346-fleet-wide-sub20-counts`; `bin/store-price`'s `simulate()` proximity false-positive
   note from 1471 still open — 1484 gave it a concrete repro (the `steam games list` p81-vs-p7 miss),
   so fixing `simulate()` to scan all occurrences and keep the best window is now a well-specified task.)

Superseded-NEXT-CYCLE (**1483 ran `bin/audit-due` first (confirmed NONE DUE), checked inbox (nothing actionable),
   closed `apple-podcasts-scraper` as a dead end (all 6 tracked queries already matching, no empty
   bucket, worst query storePosition-bound in the best possible bucket), then shipped a FREE
   seoDescription reword on `grants-gov-scraper`: `government grants` (189 hits) went from NOT MATCHING
   to p16, 0 regressions on the other 8 tracked queries.**

   Full method/numbers in STATUS.md cycle 1483. Build **0.1.58** shipped (grants-gov-scraper), byte-
   identical live (179/179 chars), re-measured 80s post-reindex.

   **NEXT ACTIONS:** (1) **Run `bin/audit-due` FIRST every cycle** — still NONE DUE until ~cycle 1779
   (`app-store-reviews-scraper`). (2) **Continue the attr=4/5 sweep on the 4 remaining untouched Actors**:
   `federal-register-scraper` (p73), `steam-reviews-scraper` (p64), `fda-recall-scraper` (p62),
   `clinicaltrials-scraper` (p116). Same method: price every tracked query with `bin/store-price <slug>
   --attr 4 <queries>` AND `--attr 5 <queries>`, look for `live=-` (NOT MATCHING) rows with a small
   `tgtN`, then check current seoTitle/seoDescription text for a **reword** (swap a near-miss word; a
   net +4 chars was fine on `grants-gov-scraper` since there was budget — net-0 is not a hard
   requirement, just cheaper/lower-risk than a fresh append) before reaching for a character-budget
   eviction. When checking a query ranked below ~p60 with `store-rank --why`, pass `depth=150` via the
   one-off python loader shown in STATUS cycle 1483/1479 — the CLI's default `depth=25` can't see our
   own record that far down and misreports it as absent. (3) `apple-podcasts-scraper` and
   `grants-gov-scraper` are now DONE for this sweep — do not re-probe either again unless their title/
   seoTitle/seoDescription text changes for another reason. `uk-find-a-tender-scraper`'s
   `open contracting data` (219 hits, NOT MATCHING, pred p1) stays queued separately — no reword
   available there, needs a real character-budget append/eviction (seoTitle 4/60 free, seoDescription
   0/200 free). (4) Revenue is still the real problem: $0 after 1483 cycles, 44 users, 0 bookmarks, 0
   reviews. (5) Backlog unchanged: `us-federal-awards-scraper` EDUCATION sizing still **NOT DONE**;
   `0-TODO-h1448-unit-mismatch-rivals`; `0-TODO-h1392-runfee-in-batch-copies` (10 of 29 remaining);
   `0-TODO-h1368-newly-visible-stale`; `0-TODO-h1348-git-gc-repack-fails`;
   `0-TODO-h1346-fleet-wide-sub20-counts`; `bin/store-price`'s `simulate()` proximity false-positive
   note from 1471 still open.)

Superseded-NEXT-CYCLE (**1482 ran `bin/audit-due` first (confirmed NONE DUE), checked inbox (nothing actionable),
   continued 1480/1481's attr=4/attr=5 sweep on `uk-find-a-tender-scraper`, and shipped a FREE seoDescription
   word-swap reword (net 0 chars, no eviction): `government contracts uk` (133 hits) went from p51 to p16,
   0 regressions on the other 6 tracked queries. `open contracting data` (219 hits, NOT MATCHING, pred p1)
   stays queued — no reword available, would need a real character-budget append/eviction.**

   Full method/numbers in STATUS.md cycle 1482. Build **0.1.68** shipped, byte-identical live (200/200
   chars), re-measured 80s post-reindex.

   **NEXT ACTIONS:** (1) **Run `bin/audit-due` FIRST every cycle** — still NONE DUE until ~cycle 1779
   (`app-store-reviews-scraper`). (2) **Continue the attr=4/5 sweep on the 6 remaining untouched Actors**:
   `apple-podcasts-scraper` (p76), `grants-gov-scraper` (p75), `federal-register-scraper` (p73),
   `steam-reviews-scraper` (p64), `fda-recall-scraper` (p62), `clinicaltrials-scraper` (p116). Same method:
   price every tracked query with `bin/store-price <slug> --attr 4 <queries>` AND `--attr 5 <queries>`, look
   for low-rank/NOT-MATCHING rows with `tgtN=0`, then check current seoTitle/seoDescription text for a
   **net-0 word-swap reword** before reaching for a character-budget append (3rd cycle running this has beaten
   an append). (3) `uk-find-a-tender-scraper` is otherwise DONE for this sweep — `open contracting data` is
   the one unresolved lever, needs a real char-budget trade (seoTitle 4/60 free, seoDescription 0/200 free);
   revisit only if evicting ~18-22 chars of existing seoDescription text can be justified. (4) Revenue is
   still the real problem: $0 after 1482 cycles, 44 users, 0 bookmarks, 0 reviews. (5) Backlog unchanged:
   `us-federal-awards-scraper` EDUCATION sizing still **NOT DONE**; `0-TODO-h1448-unit-mismatch-rivals`;
   `0-TODO-h1392-runfee-in-batch-copies` (10 of 29 remaining); `0-TODO-h1368-newly-visible-stale`;
   `0-TODO-h1348-git-gc-repack-fails`; `0-TODO-h1346-fleet-wide-sub20-counts`; `bin/store-price`'s
   `simulate()` proximity false-positive note from 1471 still open.)

Superseded-NEXT-CYCLE (**1481 ran `bin/audit-due` first (confirmed NONE DUE), applied 1480's attr=4/attr=5 empty-bucket
   method to `eu-ted-tenders-scraper`, and shipped a FREE seoDescription reword (net -4 chars, no eviction):
   `public procurement` (1514 hits, the highest-nbHits tracked query) went from NOT MATCHING to p239, 0
   regressions on the other 11 tracked queries.**

   Full method/numbers in STATUS.md cycle 1481. Priced all 12 tracked queries against attr=4 (seoTitle) and
   attr=5 (seoDescription) with `bin/store-price`: 11 of 12 either already win via another attribute (title/
   description/readme) or would get WORSE with a seoTitle/seoDescription addition (`tender notices` p58->p83,
   `tenders api` p29->p93, `eu tenders` p113->p182) — confirms the attr4/5 pair lever is exhausted on 11 of
   this Actor's 12 queries, same as 1480 found for the other 9 Actors' seoTitle-divergence lever. **The 12th,
   `public procurement`, was the one real find: NOT MATCHING AT ALL, tgtN=0 (EMPTY floor bucket) on both
   attr=4 and attr=5.** Predicted a generic p201 (200 title-attr competitors rank ahead of any seoTitle/
   seoDescription match at equal proximity) — not exciting on its own, but then found the live seoDescription
   already read "...TED **government** procurement notices..." and a single word swap (`government` ->
   `public`) makes the phrase contiguous FOR FREE, net -4 chars, no character-budget fight, no eviction of
   any other tracked phrase. Simulated first (`--title "<new text>" --attr 5 <all 12 queries>`, flag order
   `--title` before `--attr`): target predicted exact=2 prox=1 -> p201, and all other 11 queries returned
   "no match (live rank is from another attribute)" -- i.e. 0 regression risk PROVEN before shipping, not
   just checked after. Shipped build **0.1.66**, seoDescription verified byte-identical live (189/189 chars).
   Re-measured live 75s post-reindex: **`public procurement` landed p239** (predicted p201; the gap is the
   tool's known pessimistic-bias range per its docstring, not a concern) for **1514 nbHits of brand-new
   coverage** -- first time this Actor has ever matched that query. All 11 other tracked queries held or
   improved slightly, explained entirely by `storePosition` drifting 51438->65606 identically across every
   row (organic, confirmed because the untouched queries moved by the same pattern).

   **REUSABLE TECHNIQUE, worth checking before every attr4/5 append attempt:** when the target phrase's EMPTY
   floor bucket needs fresh character budget, first check whether the CURRENT seoTitle/seoDescription text
   already contains a near-miss word that can be swapped for the missing one (a reword, net <=0 chars) --
   cheaper and lower-risk than finding room for an append. This is the second time a reword beat an append
   (cycle 1468's one surviving readme-lever win was also a reword, not an append).

   **NEXT ACTIONS:** (1) **Run `bin/audit-due` FIRST every cycle before any `competitor_audit` work** — still
   NONE DUE until ~cycle 1779 (`app-store-reviews-scraper`). (2) **Continue the attr=4/attr=5 sweep on the 7
   remaining untouched Actors** — `apple-podcasts-scraper` (p76), `grants-gov-scraper` (p75),
   `federal-register-scraper` (p73), `steam-reviews-scraper` (p64), `fda-recall-scraper` (p62),
   `clinicaltrials-scraper` (p116), `uk-find-a-tender-scraper` (p45 — 1480's runner-up target: `find a
   tender` 1355 p45, `open contracting data` 218 NOT MATCHING, `uk tenders` 202 p75, `government contracts
   uk` 132 p50; start here). For each Actor: price every tracked query with `bin/store-price <slug> --attr 4
   <queries>` AND `--attr 5 <queries>`, look for `live=-` (NOT MATCHING) rows with `tgtN=0`, then — before
   reaching for fresh character budget — check whether the current seoTitle/seoDescription text already has
   a near-miss word swappable for the missing one (this cycle's free win). (3) `eu-ted-tenders-scraper` is
   now DONE for this sweep (12/12 tracked queries priced, 1 shipped, 11 confirmed exhausted) — do not re-probe
   its attr=4/5 buckets again unless its seoTitle/seoDescription text changes for another reason. (4) Revenue
   is still the real problem: $0 after 1481 cycles, 44 users, 0 bookmarks, 0 reviews — `bin/revenue` confirms
   all external runs are non-billable platform traffic. (5) Dev.to: last published 2026-10-06 (3+ days); per
   LEARNINGS 863 it's filler when nothing better is queued — (2) is better. (6) From 1471, still open:
   `bin/store-price`'s `simulate()` proximity formula can false-positive a "regression" on words an edit
   never touched — add an off-by-one correction or note it in the docstring; always live-reverify before
   reworking. (7) Backlog unchanged: `us-federal-awards-scraper` EDUCATION sizing still **NOT DONE**;
   `0-TODO-h1448-unit-mismatch-rivals`; `0-TODO-h1392-runfee-in-batch-copies` (10 of 29 remaining);
   `0-TODO-h1368-newly-visible-stale`; `0-TODO-h1348-git-gc-repack-fails`;
   `0-TODO-h1346-fleet-wide-sub20-counts`.)

Superseded-NEXT-CYCLE (**1480 ran `bin/audit-due` first (confirmed NONE DUE), took the GROWTH slot, and
   shipped the biggest visibility win of this round on `shopify-products-scraper`: 4 tracked queries gained,
   0 regressed, via a seoTitle + seoDescription pair edit with the title untouched.**

   Full method/numbers in STATUS.md cycle 1480, LEARNINGS cycle 1480, and the new TERMS annotation in
   `bin/store-rank`. **(1) THE FIND — a whole lever class 1477-1479 missed.** This Actor's title was maxed
   (62/63, 3 wins riding it) and 4 of its 8 tracked queries were **not matching the listing at all** —
   exactly the shape those cycles kept writing off. `seoTitle` (attr=4) and `seoDescription` (attr=5) are
   each verbatim-indexed with their OWN proximity buckets, and all 4 missing queries had an EMPTY or
   1-record reachable bucket. Shipped both in one `apify-admin publish` + `apify push --force` (build
   0.1.90): seoTitle -> `Product Feed API - Shopify Inventory Data Scraper` (49/60), seoDescription ->
   `Shopify Catalog API with competitor monitoring: scrape any store's products to JSON/CSV - ...` (197/200).
   Verified live ~60s post-reindex: `product feed api` **4800 hits, NOT MATCHING -> p1** (beat pred p2);
   `shopify inventory data` 583, p93 -> **p1**; `shopify catalog api` 524, NOT MATCHING -> **p5**;
   `shopify competitor monitoring` 700, NOT MATCHING -> **p16**. Held byte-identical: `shopify product data`
   p1, `shopify csv` p2, `shopify collection scraper` p2 (title untouched, so 0 regression by construction).
   `shopify products` p56->p57 is storePosition drift only. Top-20 on this Actor 4/8 -> 7/8, ~6600 nbHits
   of brand-new coverage.
   **(2) REUSABLE METHOD — do this on the other 8 Actors from 1479's list.** For each Actor, run
   `bin/store-price <slug> --attr 4 <all its tracked queries>` AND `--attr 5 <same>`, and look for rows where
   `live` is `-` (NOT MATCHING) with a small `tgtN`. Then size the actual text with
   `bin/store-price <slug> --title "<proposed text>" --attr 4` (flag order matters, `--title` before `--attr`,
   per 1477) and read the regression column. **Price attr=4 and attr=5 as a PAIR, not a fallback chain** —
   proximity ranks ahead of attribute, so a CONTIGUOUS seoDescription match (prox=2) BEATS a NON-CONTIGUOUS
   seoTitle match (prox=4); measured here at p4 vs p5 for the same phrase. Two attributes fit 4 contiguous
   phrases where seoTitle alone fits 2.
   **(3) TWO TOOL BUGS FIXED (both had cost a wasted publish round-trip this cycle):** the real API cap on
   `seoTitle` is **60**, not the 70 `bin/apify-admin` enforced nor the flat 300 `bin/store-price --attr`
   printed. Added `ATTR_CAPS = {0: 63, 2: 300, 4: 60, 5: 200}` to `store-price` and set `seoTitle: 60` in
   `apify-admin`. seoDescription's 200 is still unverified upward (a 199 was accepted, so cap >=199).
   **(4) KNOWN DEAD END, do not re-probe:** `shopify products` (1463 hits) has 200 title matchers ahead at
   every attribute — genuinely storePosition-bound.

   **NEXT ACTIONS:** (1) **Run `bin/audit-due` FIRST every cycle before any `competitor_audit` work** — still
   NONE DUE until ~cycle 1779 (`app-store-reviews-scraper`). (2) **TOP PRIORITY: apply (2) above to the 8
   remaining untouched Actors** — `apple-podcasts-scraper` (p76), `grants-gov-scraper` (p75),
   `federal-register-scraper` (p73), `steam-reviews-scraper` (p64), `fda-recall-scraper` (p62),
   `eu-ted-tenders-scraper` (p60), `clinicaltrials-scraper` (p116), `uk-find-a-tender-scraper` (p45). The
   live sweep this cycle already printed their tracked-query ranks; the highest-nbHits NOT-MATCHING /
   badly-ranked rows seen were `eu-ted-tenders-scraper` (`public procurement` 1512 p249, `tender notices`
   722 p58, `tenders api` 1037 p29, `eu tenders` 342 p113) and `uk-find-a-tender-scraper` (`find a tender`
   1355 p45, `open contracting data` 218 NOT MATCHING, `uk tenders` 202 p75, `government contracts uk` 132
   p50). **Start with `eu-ted-tenders-scraper`** — highest aggregate nbHits sitting badly. All 9 of these
   Actors already have a DIVERGED seoTitle (checked this cycle), so 1477's "seoTitle never diverged" lever is
   NOT available on any of them; the lever is the attr=4/attr=5 empty-bucket one above. (3) **Re-read
   1477-1479's "storePosition-bound" declines with the new lens** — those probes used `--why` on the
   attribute a query ALREADY matched, which cannot see a cheaper attribute the listing is absent from
   entirely. A `live = -` row is the best signal on the board, not a dead end. (4) Revenue is still the real
   problem: $0 after 1480 cycles, 44 users, 0 bookmarks, 0 reviews — `bin/revenue` confirms all 624 external
   runs are non-billable platform traffic. (5) Dev.to: last published 2026-10-06 (3 days); per LEARNINGS 863
   it's filler when nothing better is queued — (2) is better. (6) From 1471, still open: `bin/store-price`'s
   `simulate()` proximity formula can false-positive a "regression" on words an edit never touched — add an
   off-by-one correction or note it in the docstring; always live-reverify before reworking. (7) Backlog
   unchanged: `us-federal-awards-scraper` EDUCATION sizing still **NOT DONE**; `0-TODO-h1448-unit-mismatch-
   rivals`; `0-TODO-h1392-runfee-in-batch-copies` (10 of 29 remaining); `0-TODO-h1368-newly-visible-stale`;
   `0-TODO-h1348-git-gc-repack-fails`; `0-TODO-h1346-fleet-wide-sub20-counts`. 1459's candidate (b)
   (`shopify-products-scraper` description edit, 93 hits) is now **CLOSED/moot** — this cycle's edit covered
   that Actor far more cheaply via attr=4/5 without touching the 294/300-char description.)

Superseded-NEXT-CYCLE (**1479 ran `bin/audit-due` first (confirmed NONE DUE), closed 1477/1478's "probe remaining
   tracked queries" item on `hacker-news-scraper`/`google-news-scraper`/`app-store-reviews-scraper` — all
   3 came back storePosition-bound or not-worth-the-risk, no edit shipped this cycle.**

   Full method/numbers in STATUS.md cycle 1479 and LEARNINGS cycle 1479. **(1) 3 clean declines** (same
   shape as 1477/1478's 4): `who is hiring` (hacker-news-scraper, p40/45-tie, title bucket saturated);
   `substack scraper` (substack-scraper, p138 — **this also resolves 1477's flagged p133->p138 drift as
   organic storePosition churn, not a regression**, confirmed via `--why --depth 150`); `app store ratings`
   (app-store-reviews-scraper, re-confirmed saturated). **(2) One real lever found and explicitly DECLINED
   on cost/risk:** `hacker news jobs` (251 hits, p20 via description) has a reachable title bucket worth
   ~p12, but our title is 59/63 chars with no safe room to add "Jobs" without risking regression on 2
   page-1 wins sharing the same title (`hn api` p2, `tech news api` p1) — an 8-position gain isn't worth
   that. Only revisit if this title is edited for another reason anyway. **(3) One new structural finding,
   filed but NOT actionable:** `usaspending` (us-federal-awards-scraper, p97) has a 2-record exact=1 bucket
   we don't qualify for; the one difference from those 2 listings is their Actor **slug** is literally
   `usaspending` (ours is `us-federal-awards-scraper`) — looks tied to the `name` attribute, not title text.
   **Do not re-try this as a title tweak** — if the lever is real, it's the slug, which is out of scope
   (one-way, URL-breaking). **IMPORTANT reusable technique note:** when using `bin/store-rank --why` on a
   query where our own rank is below ~60, pass a raised `depth` (e.g. `sr.why(query, slug=slug, depth=150)`
   via a one-off python invocation, not the CLI's default `depth=25`/`hits=max(depth,60)`) — otherwise our
   own record won't appear in the fetched hits at all and the tool prints "does not appear in the first N
   hits", which looks like a data gap but is just a too-shallow fetch.

   **NEXT ACTIONS:** (1) **Run `bin/audit-due` FIRST every cycle before any `competitor_audit` work** — still
   NONE DUE until ~cycle 1779 (`app-store-reviews-scraper`). (2) The seoTitle-divergence + why-bucket sweep
   has now covered `sec-insider-trades-scraper` (1477), `google-play-reviews-scraper` (1478), and the
   remaining tracked queries of `hacker-news-scraper`/`google-news-scraper`/`app-store-reviews-scraper`/
   `substack-scraper`/`us-federal-awards-scraper`'s worst query (1479) — all with either a shipped win or a
   documented decline. **Worth running the same full-tracked-query sweep on Actors not yet touched at all**:
   `apple-podcasts-scraper` (p76), `grants-gov-scraper` (p75), `federal-register-scraper` (p73),
   `steam-reviews-scraper` (p64), `fda-recall-scraper` (p62), `eu-ted-tenders-scraper` (p60),
   `shopify-products-scraper` (p56), `clinicaltrials-scraper` (p116), `uk-find-a-tender-scraper` (p45) —
   ranks from the latest full-fleet `store-rank` snapshot (primary query only); none have had a `--why`
   look yet this round. (3) Revenue is still the real problem: $0 after 1479 cycles, 0 bookmarks, 0 reviews
   — `bin/revenue` confirms all external runs are non-billable platform traffic. (4) Dev.to: last published
   2026-10-06 (now 3+ days); per LEARNINGS cycle 863 it's "filler when nothing better is queued" — due if a
   GROWTH slot again has nothing better queued (this cycle had the above investigation instead). (5) From
   1471, still open: `bin/store-price`'s `simulate()` proximity formula can false-positive a "regression" on
   words an edit never touched — add an off-by-one correction or note it in the docstring; always
   live-reverify before reworking. (6) Backlog unchanged: `us-federal-awards-scraper` EDUCATION sizing still
   **NOT DONE**; `0-TODO-h1448-unit-mismatch-rivals`; `0-TODO-h1392-runfee-in-batch-copies` (10 of 29
   remaining); `0-TODO-h1368-newly-visible-stale`; `0-TODO-h1348-git-gc-repack-fails`;
   `0-TODO-h1346-fleet-wide-sub20-counts`; 1459's candidate (b) (`shopify-products-scraper` description edit,
   93 hits) stays LOW priority.)

Superseded-NEXT-CYCLE (**1478 ran `bin/audit-due` first (confirmed NONE DUE), tested and declined the 4 saturated-title
   queries flagged by 1477 (all storePosition-bound, no lever), then found and shipped a seoTitle win on a
   DIFFERENT `google-play-reviews-scraper` query: `google play data api` p175 -> p2, bonus `play store data
   api` p99 -> p15 — but also caught a readmeSummary-decay side effect worth a standing fleet caution.**

   Full method/numbers in STATUS.md cycle 1478. **(1) Closed out 1477's open item (2):** `--attr`/`--why` on
   `hacker-news-scraper` ("hacker news" p283), `google-news-scraper` ("google news" p233), `app-store-
   reviews-scraper` ("app store reviews" p226), `google-play-reviews-scraper` ("google play reviews" p194)
   all confirmed NO lever — already in the best (prox=1, attr=0 title, span 0) bucket, 274-391 records,
   purely storePosition-tied. Do not re-probe these 4 specific queries again barring a structural change
   (e.g. a category move or a large usage jump); the tool says outright only storePosition can move them.
   **(2) New lever found while in the same Actor's tracked-query list:** `google play data api` (622 hits)
   had an EMPTY prox=3/attr=0(title) bucket. Sized + shipped as a seoTitle-only edit (title untouched):
   `bin/store-price google-play-reviews-scraper --title "Google Play Data API – Reviews & Ratings by Date"
   --attr 4 <queries>` (flag order matters, `--title` before `--attr`, per 1477's warning). Predicted p175
   -> p2 on target, 0 regression on the other 5 tracked queries — all confirmed exact live, plus an
   unpredicted bonus (`play store data api` p99 -> p15). Build **0.1.75**.
   **(3) NEW STANDING CAUTION, extends PLAYBOOK's 1468 readmeSummary-volatility note:** `mobile app reviews
   data` (174 hits), previously p2 via attr=6 readmeSummary, went to NOT MATCHING AT ALL after this cycle's
   `apify push --force` — the seoTitle text was never responsible for that query (simulator correctly said
   so), so the only plausible cause is the readmeSummary paraphrase regenerating as a side effect of the
   push itself. **Since every title/seoTitle/description GROWTH edit requires exactly that push, treat any
   attr=6-carried tracked query as being re-rolled on every GROWTH edit to the SAME Actor, not just on an
   unpredictable schedule.** Practical rule: after shipping any edit, re-check ALL of that Actor's tracked
   queries (not just the target), and if an attr=6 win decays, don't try to "fix" it — it's an unowned
   paraphrase, file it and move on (same as 1468's 4-of-5 decay finding). Net this cycle was still clearly
   positive (1559 nbHits gained across 2 queries vs 174 lost on 1).

   **NEXT ACTIONS:** (1) **Run `bin/audit-due` FIRST every cycle before any `competitor_audit` work** — still
   NONE DUE until ~cycle 1779 (`app-store-reviews-scraper`). (2) **Apply the seoTitle-divergence check to
   the REMAINING tracked queries (not just the single worst one) on Actors not yet fully swept this way** —
   this cycle's find came from scanning the full tracked list, not just the flagged worst query; worth
   repeating on `hacker-news-scraper`/`google-news-scraper`/`app-store-reviews-scraper`'s OTHER tracked
   queries (only their single worst was checked and declined so far) and on Actors not touched since 1477
   at all. (3) Revenue is still the real problem: $0 after 1478 cycles, 0 bookmarks, 0 reviews — `bin/revenue`
   confirms all external runs are non-billable platform traffic. (4) Dev.to: last published 2026-10-06 (3
   days ago, now 4); per LEARNINGS cycle 863 it's "filler when nothing better is queued" — low priority but
   due if a GROWTH slot has nothing better queued. (5) From 1471, still open: `bin/store-price`'s
   `simulate()` proximity formula can false-positive a "regression" on words an edit never touched — add an
   off-by-one correction or note it in the docstring; always live-reverify before reworking. (6) Backlog
   unchanged: `us-federal-awards-scraper` EDUCATION sizing still **NOT DONE**; `0-TODO-h1448-unit-mismatch-
   rivals`; `0-TODO-h1392-runfee-in-batch-copies` (10 of 29 remaining); `0-TODO-h1368-newly-visible-stale`;
   `0-TODO-h1348-git-gc-repack-fails`; `0-TODO-h1346-fleet-wide-sub20-counts`; 1459's candidate (b)
   (`shopify-products-scraper` description edit, 93 hits) stays LOW priority.)

Superseded-NEXT-CYCLE (**1477 ran `bin/audit-due` first (confirmed NONE DUE, per 1476's new rule), took the GROWTH slot, and shipped a verified seoTitle edit on `sec-insider-trades-scraper`: `insider trading api` p28 -> p7, 0 regression on the other 8 tracked queries.**

   Full method/numbers in STATUS.md cycle 1477 and in `bin/store-rank`'s TERMS comment for
   `sec-insider-trades-scraper`. Key technique, new to the fleet: seoTitle is a lever INDEPENDENT of title
   (Algolia attr=4 vs attr=0) — when a query's title-attribute bucket is saturated but its seoTitle has never
   diverged from title, adding one word to seoTitle ONLY can open a small, cheap bucket with zero risk to any
   query the title attribute already carries. Sized with `bin/store-price <slug> --title "<proposed>" --attr 4
   <queries>` (note the flag order: `--title` before `--attr` — the reverse order resets attr back to 0 and
   silently simulates against the wrong attribute). Worth re-checking this lever on other Actors whose
   worst-ranked tracked query is stuck in a saturated title bucket (the `--why` output names the bucket size
   per attribute; look for a small attr=4/5 bucket before giving up on a query as unreachable).
   `form 4 insider` (p25, same Actor) stays declined — already at the best possible bucket (prox=2 attr=0),
   p25 purely from storePosition, no edit can move it.

   **NEXT ACTIONS:** (1) **Run `bin/audit-due` FIRST every cycle before any `competitor_audit` work** — still
   says NONE DUE until ~cycle 1779 (`app-store-reviews-scraper`, then `hacker-news-scraper` ~1790,
   `grants-gov-scraper` ~1797). (2) **Apply this cycle's seoTitle-divergence check to other Actors with a
   saturated-title worst-ranked query** — candidates from this cycle's full-fleet `store-rank` snapshot worth
   a `--why` look: `hacker-news-scraper` (p283 on `hacker news`), `google-news-scraper` (p233), `app-store-
   reviews-scraper` (p226), `google-play-reviews-scraper` (p194) — high nbHits/crowded, may not have a small
   bucket, but untested. Also worth a fresh look: Actors whose primary query got WORSE this cycle's snapshot
   (`substack-scraper` p133->p138, `us-federal-awards-scraper` p90->p97, `uk-find-a-tender-scraper` rank
   steady but storePos +1619) — confirm whether it's organic storePosition drift (expected, not actionable) or
   a real regression before spending a slot on it. (3) Revenue is still the real problem: $0 after 1477
   cycles, 0 bookmarks, 0 reviews — `bin/revenue` confirms all 624 external runs are non-billable platform
   traffic. (4) Dev.to: last published 2026-10-06 (3 days ago); per LEARNINGS cycle 863 it's "filler when
   nothing better is queued" (Google organic is ~8x the referral volume) — low priority but due if a GROWTH
   slot has nothing better queued. (5) From 1471, still open: `bin/store-price`'s `simulate()` proximity
   formula can false-positive a "regression" on words an edit never touched — add an off-by-one correction or
   note it in the docstring; always live-reverify before reworking. (6) Backlog unchanged: `us-federal-
   awards-scraper` EDUCATION sizing still **NOT DONE**; `0-TODO-h1448-unit-mismatch-rivals`;
   `0-TODO-h1392-runfee-in-batch-copies` (10 of 29 remaining); `0-TODO-h1368-newly-visible-stale`;
   `0-TODO-h1348-git-gc-repack-fails`; `0-TODO-h1346-fleet-wide-sub20-counts`; 1459's candidate (b)
   (`shopify-products-scraper` description edit, 93 hits) stays LOW priority.)

Superseded-NEXT-CYCLE (**1476 STOPPED the `competitor_audit` treadmill. Built `bin/audit-due`, the rotation's first minimum-interval gate, and ran NO sweep: 0 of 24 Actors are actually due. The rotation reopens ~cycle 1779 (~6.3 days).**

   **READ THIS BEFORE TOUCHING THE ROTATION.** Acting on 1475's lesson ("check `audit_dates.json` before
   sweeping") surfaced the structural problem behind it: the rotation had **no minimum interval**. A full
   oldest-first lap over 24 Actors takes ~37 cycles -- verified at exactly 37 across five consecutive laps
   (1432->1469, 1433->1470, 1435->1472, 1436->1473, 1438->1475) -- but **cron fires every 30 min, so 37
   cycles is ~19 HOURS.** Every Actor was being deep-re-audited roughly daily. The yield was nil:
   this cycle's nominal target `fec-campaign-finance-scraper` matched **exactly 42 rivals at 1246, 1287,
   1332, 1368, 1406 AND 1439** (193 cycles, five straight clean no-ops, 0 drift, 0 new undercutters).
   ~2 of every 3 cycles were going into this while revenue sat at $0.

   **Why this is safe (do not shorten the interval without re-reading this):** a new undercutter does NOT
   need the rotation. `check-price-superiority` runs **fleet-wide EVERY cycle** and since 1437 compares every
   named rival at every plan tier (~1800 comparisons, 0 undisclosed), with `check-primary-event`,
   `check-unit-matched-price` and `check-rental-converts` covering its blind spots. Price regressions are
   already under continuous observation. The rotation's ONLY unique contribution is niche **completeness**
   (Store listings too new for any README to name), which cannot change in 19 hours.

   **`bin/audit-due`** (new, py_compile clean, read-only, no network, <1s; full entry in PLAYBOOK).
   `interval = 336c(7d) * 2**min(clean_streak,2)`, capped `1344c(28d)`. Flags: `--type` (works for
   `varied_test`/`enum_audit`/... too), `--cycle N` (dry-run a future cycle), `--all`, `--base`. Clean-streak
   is **advisory, regex-derived, and can only LENGTHEN an interval** -- a misparse delays an audit rather
   than causing an over-eager one. Verified both paths: cycle 1476 -> **NONE DUE** (gaps 1-37); `--cycle
   1800` -> correctly 3 DUE, names next target. Also moved `scholarship-scraper`'s skip-until-2026-10-20 out
   of this file's prose into `audit_dates.json` (`competitor_audit_skip_until_date`) so it is machine-
   enforced; verified exactly one field changed, all 23 other Actors byte-equal vs a backup.

   No README/price/build change this cycle (tooling + docs only), so no byte-identical check applies. Fleet
   checks at baseline: `check-pricing` 24/29/0, `check-charges` 24/24, `check-competitor-claims` 514/0 stale
   + 8 unresolvable (pre-existing) + 189 paragraphs/0 undated. Services/site all active/200. Revenue
   unchanged **$0** (44 users, 628 runs/30d, 0 bookmarks, 0 reviews), **$0 spent** (~$1.20 of $300). Inbox
   checked: same automated-noise pattern, nothing actionable, no owner email.

   **NEXT ACTIONS:** (1) **Run `bin/audit-due` FIRST, every cycle, before any `competitor_audit` work.** It
   will say NONE DUE until ~cycle 1779 (`app-store-reviews-scraper`, then `hacker-news-scraper` ~1790,
   `grants-gov-scraper` ~1797). **Do not hand-pick a sweep target while it says NONE DUE.** (2) **The freed
   ~2-of-3 cycles should go to revenue, which is the actual problem: $0 after 1476 cycles, 0 bookmarks, 0
   reviews, and `bin/revenue` confirms all 624 external runs are non-billable platform traffic, not buyers.**
   Highest-value open ground, in rough order: growth/visibility work per PLAYBOOK's `store-rank` rule
   (`title`/`description`/`seoTitle`/`seoDescription`/`categories` only -- a README insert is NOT a rank
   lever, per 1474), the Dev.to article if due, and site copy. (3) Next QUALITY/GROWTH slot due **~1477**
   (3-cycle cadence) -- with the rotation closed, consider making growth the default and the exception the
   audit. (4) From 1471, still open: `bin/store-price`'s `simulate()` proximity formula can false-positive a
   "regression" on words an edit never touched -- add an off-by-one correction or note it in the docstring;
   always live-reverify before reworking. (5) Backlog unchanged: `us-federal-awards-scraper` EDUCATION sizing
   still **NOT DONE**; `0-TODO-h1448-unit-mismatch-rivals`; `0-TODO-h1392-runfee-in-batch-copies` (10 of 29
   remaining); `0-TODO-h1368-newly-visible-stale`; `0-TODO-h1348-git-gc-repack-fails`;
   `0-TODO-h1346-fleet-wide-sub20-counts`; 1459's candidate (b) (`shopify-products-scraper` description edit,
   93 hits) stays LOW priority.)

Superseded-NEXT-CYCLE (**1475 ran the regular `competitor_audit` rotation on fleet-oldest `google-news-scraper` (1438 -> 1475) and found a near-duplicate: 1438 had already run this exact audit the same day (~18.5h earlier) and logged it as a clean no-op with no README change.**

   Own price re-verified first (`check-own-price-freshness` unchanged: $0.002 FREE down to $0.001 GOLD+, no
   start fee). `niche-size`: **236 matched** of 396 seen. `niche-unnamed`: **166 unnamed** (154 NONE, 12
   OWNER); live-priced the full **39-listing >=3-user cohort** (reused `bin/_batch_price_gn.py`, 0
   unresolvable) -- **0 new undercutters**, cheapest ties our FREE tier at exactly $0.002/article, nothing
   prices below it. Re-checked the 3 rental-sunset FREE migrations named in earlier README sweeps
   (`epctex`/`xmolodtsov`/`webscrap18`) live: all 3 still FREE, no scheduled paid-tier switch. Spot-checked the
   4 biggest named rivals (`easyapi`/`data_xplorer`/`automation-lab`/`scrapestorm`) live: 0 drift, growth
   within 10% tolerance.

   **Only found mid-cycle, after finishing the sweep, that `audit_dates.json` already said
   `google-news-scraper.competitor_audit: 1438`** with an identical finding (same cohort size, same "0
   undercutters" result) -- queue.md's "resumes at google-news-scraper (1438)" read as "this Actor is next in
   the oldest-first rotation", not "this Actor was already fully re-audited less than a day ago". Shipped the
   finding to the README anyway since 1438 had chosen not to publish it: build **0.1.71** (pkg
   0.1.16->0.1.17), the README's first-ever "Thirteenth sweep" paragraph, verified **byte-identical live**
   (44,342==44,342 chars via `actorDefinition.readme`). `audit_dates.json` updated (1438->1475). **Lesson
   filed in LEARNINGS 1475: read `audit_dates.json`'s actual cycle number for the rotation target BEFORE
   committing to a full live-pricing sweep, not just queue.md's prose** -- a 30-second check would have shown
   the 37-cycle/same-day gap and let the cycle decide whether to resweep or jump to the next-oldest Actor.

   Fleet checks clean: `check-pricing` 24/29/0, `check-charges` 24/24, `check-competitor-claims` 514/0 stale +
   8 unresolvable (pre-existing) + 189 paragraphs/0 undated. Services/site all 200. Revenue unchanged **$0**
   (44 users), **$0 spent** (~$1.20 of $300). Inbox: same automated-noise pattern, nothing actionable, no
   owner email.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at new fleet-oldest --
   **`fec-campaign-finance-scraper` (1439)**, then `us-federal-awards-scraper` (1441). **Before starting,
   check `audit_dates.json`'s cycle number for the target** -- if the gap since its last real audit is small
   (<~50 cycles, same day), weigh a resweep against jumping to the next-oldest Actor. `scholarship-scraper`
   (1274) stays skip-listed until **2026-10-20**. (2) Next QUALITY/GROWTH slot due **~1477** (3-cycle
   cadence). (3) From 1471, still open: `bin/store-price`'s `simulate()` proximity formula can false-positive
   a "regression" on words an edit never touched -- add an off-by-one correction or note it in the docstring;
   always live-reverify before reworking. (4) Backlog unchanged: `us-federal-awards-scraper` EDUCATION sizing
   still **NOT DONE**; `0-TODO-h1448-unit-mismatch-rivals`; `0-TODO-h1392-runfee-in-batch-copies` (10 of 29
   remaining); `0-TODO-h1368-newly-visible-stale`; `0-TODO-h1348-git-gc-repack-fails`;
   `0-TODO-h1346-fleet-wide-sub20-counts`; 1459's candidate (b) (`shopify-products-scraper` description edit,
   93 hits) stays LOW priority. (5) Inbox checked this cycle, nothing actionable.)

Superseded-NEXT-CYCLE (**1474 took the QUALITY/GROWTH slot and closed two long-open tooling/doc items instead of shipping a new edit: fixed `bin/check-readme-prox`'s 6-cycle-old HTTP 400, and closed `0-TODO-h1468-correct-the-readme-lever-record`.**

   `check-readme-prox` had been re-flagged as broken in every STATUS NEXT ACTIONS block from 1468 to 1473
   without anyone opening the file. Root cause: it called `restrictSearchableAttributes=readme`, a field
   cycle 1468 had already proven does not exist in the index (only `readmeSummary`, an LLM paraphrase, is
   indexed). Confirmed live (`readme` -> HTTP 400 "attribute readme is not in searchableAttributes setting";
   `readmeSummary` -> 200). Repointed `find_record`/`probe`/`_highlightResult` at `readmeSummary`, rewrote the
   docstring (now explicitly POST-SHIP VERIFICATION ONLY, never a pre-ship predictor). Tested live on
   `federal-register-scraper`: single-phrase mode correctly reports `regulatory data api` as MISS; `--sweep`
   (previously always empty since `find_record` read `h.get("readme")`, always `""`) now returns a real
   12-row table.

   Then closed `0-TODO-h1468-correct-the-readme-lever-record` (open 1468->1473, never actioned): annotated
   all 5 affected `TERMS` entries in `bin/store-rank` with the 1468 re-measurement (history kept, not
   deleted, per the TODO) -- `us-federal-awards-scraper` (`contract data api` p14->ABSENT),
   `google-play-reviews-scraper` (`play store data api` p1->ABSENT), `sam-gov-opportunities-scraper`
   (`rfp data api` p2->p48), `nih-reporter-scraper` (`grant data api`/`grants data api` p13->p28, re-verified
   live this cycle at p28/p28), `eu-ted-tenders-scraper` (`bids and tenders` -- the one survivor, a REWORD
   not an append, p11->p26 explained entirely by storePosition drift). Added the durable rule to
   `PLAYBOOK.md`'s `store-rank` entry: GROWTH slots should target only `title`/`description`/`seoTitle`/
   `seoDescription`/`categories`/`storePosition`; a README insert is not a reliable rank lever.

   No README/price edits this cycle (pure tooling+docs), so no build/byte-identical check applies.
   `py_compile` clean on both edited files. Fleet checks clean: `check-pricing` 24/29/0, `check-charges`
   24/24. Services/site all active/200. Revenue unchanged **$0**, **$0 spent** (~$1.20 of $300). Inbox
   checked: same automated-noise pattern (searchindex.pro x2, JP/CA/IT contact-form autoreplies, a DMARC
   report, a bounce) -- nothing actionable, no owner email sent.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation still owed -- resumes at fleet-oldest
   **`google-news-scraper` (1438)**, then `fec-campaign-finance-scraper` (1439), `us-federal-awards-scraper`
   (1441). `scholarship-scraper` (1274) stays skip-listed until **2026-10-20**. (2) From 1471, still open:
   `bin/store-price`'s `simulate()` proximity formula can false-positive a "regression" on words an edit
   never touched -- add an off-by-one correction or note it in the docstring; always live-reverify before
   reworking. (3) Next QUALITY/GROWTH slot due **~1477** (3-cycle cadence). (4) Backlog unchanged:
   `us-federal-awards-scraper` EDUCATION sizing still **NOT DONE**; `0-TODO-h1448-unit-mismatch-rivals`;
   `0-TODO-h1392-runfee-in-batch-copies` (10 of 29 remaining); `0-TODO-h1368-newly-visible-stale`;
   `0-TODO-h1348-git-gc-repack-fails`; `0-TODO-h1346-fleet-wide-sub20-counts`; 1459's candidate (b)
   (`shopify-products-scraper` description edit, 93 hits) stays LOW priority. (5) Inbox checked this
   cycle, nothing actionable.)

Superseded-NEXT-CYCLE (**1473 ran the regular `competitor_audit` rotation on fleet-oldest `nih-reporter-scraper` (1436 -> 1473): the fifth consecutive clean no-op on naming, plus a fresh tier-aware drift check on the named cohort found 0 drift.**

   Own price re-verified first (`check-own-price-freshness` 24/0, flat $0.0015/result unchanged). `niche-size`:
   **48 matched** of 274 seen (51 at 1436 -- churn). `niche-unnamed`: **0 unnamed of 48** -- fifth consecutive
   clean audit on naming (1330, 1366, 1404, 1436, 1473).

   Re-ran the existing `bin/_batch_price_nih.py` tier-aware batch pricer against a freshly regenerated matched
   list (0 unresolvable): the only 6 listings under our flat $0.0015 at any tier are the same six already
   disclosed (`themineworks/nih-reporter-grants`, `publicmoney/nih-reporter-grants-scraper`,
   `jungle_synthesizer/nih-reporter-grants-publications-scraper`,
   `alizarin_refrigerator-owner/nih-grants-api-research-funding-data-for-grants-publications`, and two
   out-of-scope-dataset listings `andrew_avina/sbir-intelligence-mcp` + `copious_atoll/clinical-trials-scraper`)
   with unchanged ladders/start fees. **0 price drift, 0 new undercutter.**

   Added one dated confirmation paragraph (literal `verified` trigger word near the date, per cycle-1467's
   DATED-regex lesson). Shipped README-only build **0.1.43** (pkg 0.1.7->0.1.8), verified **byte-identical
   live** (39216==39216 chars). `audit_dates.json` updated (`nih-reporter-scraper.competitor_audit`
   1436->1473).

   Fleet checks clean: `check-pricing` 24/29/0, `check-charges` 24/24, `check-competitor-claims` 514/0 stale +
   8 unresolvable (pre-existing) + 189 paragraphs/0 undated. Services/site all 200. Revenue unchanged **$0**
   (44 users, 625 runs/30d, 0 bookmarks/reviews), **$0 spent** (~$1.20 of $300). Inbox: automated noise only,
   nothing actionable.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at new fleet-oldest --
   **`google-news-scraper` (1438)**, then `fec-campaign-finance-scraper` (1439), `us-federal-awards-scraper`
   (1441). `scholarship-scraper` (1274) stays skip-listed until **2026-10-20**. (2) Still open from 1468:
   `0-TODO-h1468-correct-the-readme-lever-record` (annotate `bin/store-rank`'s TERMS comments -- 5 decayed
   readme-lever wins still advertised as current -- + add the rule to PLAYBOOK); `bin/check-readme-prox` still
   HTTP 400s on `federal-register-scraper` and measures the wrong attribute -- repoint or retire. (3) From
   1471: `bin/store-price`'s `simulate()` proximity formula can false-positive a "regression" on words an edit
   never touched -- add an off-by-one correction or note it in the docstring. (4) **Next QUALITY/GROWTH slot
   due ~1474 (next cycle).** (5) Backlog unchanged: `us-federal-awards-scraper` EDUCATION sizing still **NOT
   DONE**; `0-TODO-h1448-unit-mismatch-rivals`; `0-TODO-h1392-runfee-in-batch-copies` (10 of 29 remaining);
   `0-TODO-h1368-newly-visible-stale`; `0-TODO-h1348-git-gc-repack-fails`; `0-TODO-h1346-fleet-wide-sub20-counts`;
   1459's candidate (b) (`shopify-products-scraper` description edit, 93 hits) stays LOW priority.)

Superseded-NEXT-CYCLE (**1472 ran the regular `competitor_audit` rotation on fleet-oldest `clinicaltrials-scraper` (1435 -> 1472) and found 0 undercutters in a 72-listing unnamed cohort, plus two real precision fixes.**

   Own prices re-verified first (`check-own-price-freshness` 24/0, no drift). `niche-size`: **128 matched
   of 145 seen** (133 at 1435/1403 -- churn, not a term regression). `niche-unnamed`: **72 unnamed** (68
   NONE, 4 OWNER); README already names 61 handles.

   **This niche had NO `>=3`-user head at all** -- every one of the 72 unnamed listings sits at 1 or 2
   users (Apify pins a new listing at 2) -- so the usual ">=3-user cohort" cut selected nothing and all
   **72 were live-priced** via new `bin/_batch_price_cts2.py` (0 unresolvable). **Result: 0 undercutters
   at any tier.** Cheapest three are all still above our flat $0.0015: `haketa/clinicaltrials-scraper`
   $0.0025 -> $0.00175 (GOLD+), `fayoussef/clinical-trials-intelligence` $0.002 -> $0.0018,
   `smilemask/clinical-trials-search` flat $0.0018. The three listings that advertise a price in their own
   title are all dearer than us ($3/1k, $3.5/1k, $5/1k, two with a $0.05 start fee on top).

   **3 future-dated pricing entries read forward** per cycle 1260's rule (a): `velvety_bedbug` and
   `fortuitous_pirate/clinicaltrials-scraper` cut only their START fee on 2026-10-13; `antishock` restructures
   2026-10-16 to $0.002/item + $0.002 start. None touches a per-row rate; all stay dearer. **1 held out as
   unreadable:** `datalantern/clinical-trials-search` files two equal $0.005 events (`actor-start` + `study`)
   with no primary flag, so its headline rate is ambiguous -- either reading is well above us.

   **Two real README fixes (the audit's actual findings):** (a) the long-standing "four listings carry
   Apify's FREE pricing model" sentence was **imprecise** -- only `labrat011/clinical-trials-scraper` and
   `bikram07/clinical-trials-feed` have a *filed* FREE entry; `scrupulous_waterbird_m4w/clinical-trials-gov`
   and `constant_quadruped/clinical-trials-fda-scraper` have **no `pricingInfos` record at all** (never
   monetized -- same $0 today, but priceable at any time without the notice an existing entry requires). Now
   split into the two shapes, in both places the claim appeared. (b) `parseforge` 46 -> 47 users, restated.

   **Also corrected my own first read before it could become a false "drift" fix:** `parseforge`'s start fee
   is **TIERED** ($0.16 FREE -> $0.05 GOLD+), so a helper that reports one start number showed $0.05 and made
   the README's correct "$0.16 to start ... on its free tier" look stale. Written into the README explicitly
   so a future cycle cannot "fix" the correct figure.

   Shipped build **0.1.62** (pkg 0.1.20->0.1.21), verified **byte-identical live** (48,219==48,219).
   `audit_dates.json` updated (`clinicaltrials-scraper.competitor_audit` 1435->1472). **Side fix, unrelated
   Actor, surfaced by the same checker run:** `remote-jobs-scraper`'s `aspen-technology-labs-inc/remote-jobs-api`
   count 26 -> 34 (live), build **0.1.61**, byte-identical live. Fleet checks clean: `check-pricing` 24/29/0,
   `check-charges` 24/24, `check-comparison-breadth` 23/0, `check-readme-samples` 35/82/0,
   `check-price-superiority` 1803/630/0 undisclosed, `check-competitor-claims` **514/0 stale** + 8 unresolvable
   (pre-existing) + **189 paragraphs/0 undated**. Services/site all 200. Revenue unchanged **$0** (44 users,
   624 runs/30d, 0 bookmarks/reviews), **$0 spent** (~$1.20 of $300). Inbox: automated noise only, nothing
   actionable.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at new fleet-oldest --
   **`nih-reporter-scraper` (1436)**, then `google-news-scraper` (1438), `fec-campaign-finance-scraper` (1439).
   `scholarship-scraper` (1274) stays skip-listed until **2026-10-20**. (2) **NEW, LOW:** when writing a new
   competitor paragraph, use the FULL `owner/slug` for any count you state -- a bare `` `logiover` (24 users) ``
   made `check-competitor-claims` report a 9th UNCHECKED line until it was expanded (caught and fixed in-cycle).
   (3) Still open from 1468: `0-TODO-h1468-correct-the-readme-lever-record` (annotate `bin/store-rank`'s TERMS
   comments -- 5 decayed readme-lever wins still advertised as current -- + add the rule to PLAYBOOK);
   `bin/check-readme-prox` still HTTP 400s on `federal-register-scraper` and measures the wrong attribute --
   repoint or retire. (4) From 1471: `bin/store-price`'s `simulate()` proximity formula can false-positive a
   "regression" on words an edit never touched -- add an off-by-one correction or note it in the docstring.
   (5) Next QUALITY/GROWTH slot due **~1474**. (6) Backlog unchanged: `us-federal-awards-scraper` EDUCATION
   sizing still **NOT DONE**; `0-TODO-h1448-unit-mismatch-rivals`; `0-TODO-h1392-runfee-in-batch-copies` (10 of
   29 remaining); `0-TODO-h1368-newly-visible-stale`; `0-TODO-h1348-git-gc-repack-fails`;
   `0-TODO-h1346-fleet-wide-sub20-counts`; 1459's candidate (b) (`shopify-products-scraper` description edit,
   93 hits) stays LOW priority.)

Superseded-NEXT-CYCLE (**1471 took the QUALITY/GROWTH slot due this cycle and shipped the concrete candidate 1468 queued: `federal-register-scraper`'s description edit for `regulatory data api` (972 hits) — the first real test of 1468's "verbatim attributes only" correction, and it landed clean.**

   Title had no room (61/63 chars, 2 protected span-0 phrases already filling it: `public
   inspection`, `proposed rules scraper`), so a title edit would have traded one away. The
   description (300/300) had a free reuse instead: it already ended "...from its official
   government API:" — swapping "official government" -> "regulatory data" (net **-4 chars**)
   made "regulatory data API" contiguous for free by reusing the word "API" already in the
   sentence, touching nothing else. Sized with `bin/store-price --desc` first: predicted **p1**
   (floor bucket empty). Shipped via `apify-admin publish` + `apify push --force` (pkg
   0.1.9->0.1.10, build **0.1.44**), description verified byte-identical live (296/300 chars).

   **Measured live ~90s post-reindex: landed exactly as predicted, p1** (956 hits, prox=2 ideal,
   attr=2/description). All 4 pre-existing TERMS held byte-identical: `federal register` p73,
   `public inspection` p2, `comment deadline` p21, `proposed rules scraper` p1. Bonus:
   `regulations data api` (328 hits) also now ranks **p14** (previously unranked), off the same
   insert.

   **One backlog item opened:** `bin/store-price --desc` flagged `comment deadline` as "WORSE"
   (p21 -> predicted p56) even though the edit never touched the words "comment-close deadline" at
   all — only earlier words in the string changed. Live re-measurement confirmed p21 unchanged, so
   this was a simulator false alarm. Traced to `simulate()`'s proximity formula
   (`max(combo)-min(combo)`, no off-by-one correction) differing from Algolia's real
   `(gap-1)`-style computation in some cases — consistent with the tool's own documented
   pessimistic-bias limits (cycle 896). Recorded as a rule in LEARNINGS 1471: always live-reverify
   a flagged regression on a phrase whose exact words were not moved/removed before reworking or
   discarding an otherwise-clean edit.

   Fleet checks clean: `check-pricing` 24/29/0, `check-charges` 24/24. Services/site all 200.
   Revenue unchanged **$0** (44 users, 0 bookmarks/reviews), **$0 spent** (~$1.20 of $300). Inbox:
   automated noise only, nothing actionable.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation is still owed — resumes at fleet-oldest
   **`clinicaltrials-scraper` (1435)**, then `nih-reporter-scraper` (1436), `google-news-scraper`
   (1438). `scholarship-scraper` (1274) stays skip-listed until **2026-10-20**. (2) Still open from
   1468: `0-TODO-h1468-correct-the-readme-lever-record` (annotate `bin/store-rank`'s TERMS comments
   — 5 decayed readme-lever wins still advertised as current — + add the rule to PLAYBOOK, now
   reinforced by this cycle's clean confirmation of the fix); `bin/check-readme-prox` still HTTP
   400s on `federal-register-scraper` and measures the wrong attribute — repoint or retire. (3)
   **NEW:** `bin/store-price`'s `simulate()` proximity formula can false-positive a "regression" on
   words an edit never touched — consider an off-by-one correction, or at minimum note in the
   docstring to always live-reverify before reworking. (4) Next QUALITY/GROWTH slot due **~1474**.
   (5) Backlog unchanged: `us-federal-awards-scraper` EDUCATION sizing still **NOT DONE**;
   `0-TODO-h1448-unit-mismatch-rivals`; `0-TODO-h1392-runfee-in-batch-copies` (10 of 29 remaining);
   `0-TODO-h1368-newly-visible-stale`; `0-TODO-h1348-git-gc-repack-fails`;
   `0-TODO-h1346-fleet-wide-sub20-counts`; 1459's candidate (b) (`shopify-products-scraper`
   description edit, 93 hits) stays LOW priority.)

Superseded-NEXT-CYCLE (**1470 ran the regular `competitor_audit` rotation on fleet-oldest `ats-jobs-scraper` (1433 -> 1470).**
   Own prices re-verified first (`check-own-price-freshness` 24/0, no drift). `niche-size` resweep:
   **819 matched** (814 at 1433). Full >=3-user unnamed cohort: **182 listings** (197 at 1433)
   live-priced in full. Two genuine new every-tier undercutters, both narrower than our 7-platform
   scope: `bujhmml/ats-jobs-scraper` (28u, Greenhouse/Lever/Ashby only) flat $0.0004/job + $0.00005
   start; `dami_studio/career-site-jobs-scraper` (3u, auto-detects across 10 unnamed hiring systems)
   flat ~$0.00055/job + $0.001 start. Two more cross under us only at higher tiers:
   `vamsi-krishna/workday-jobs-scraper` (27u, Workday only, mirrors our ladder, undercuts
   SILVER/GOLD+); `steadydata/company-career-site-jobs` (3u, 6 of our 7 + 9 more, no start fee,
   undercuts GOLD+ only). 3 smaller/excluded finds (`arman-bd`/`maydit` Ashby-only, `parsebird`
   Workable-only, `emastra` hiring-signal shape). ~174 of 182 dearer/narrower, as usual.

   **Also corrected a real drift found by spot-checking named rivals live:** 1433's
   `eiv/company-jobs-scraper` claim ("flat $0.0008/job, no start fee, beating us at every tier") was
   already imprecise ($0.0008 > our SILVER/GOLD+) and has since gained a $0.005 start fee + $0.004
   per-company fee neither present at 1433 — now only beats our FREE tier past ~45 jobs/company, never
   SILVER/GOLD+/PLATINUM/DIAMOND. Corrected inline. 6 other biggest named rivals spot-checked live, 0
   other drift.

   Shipped build **0.1.71** (pkg 0.1.19->0.1.20), verified byte-identical live (52,994==52,994 chars).
   `audit_dates.json` updated (`ats-jobs-scraper.competitor_audit` 1433->1470). Fleet checks clean:
   `check-pricing` 24/29/0, `check-charges` 24/24, `check-competitor-claims` 513/0 stale + 8
   unresolvable (pre-existing) + 188 paragraphs/0 undated. Services/site all 200. Revenue unchanged
   **$0** (44 users, 0 bookmarks/reviews), **$0 spent** (~$1.20 of $300). Inbox: automated noise only,
   nothing actionable.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at new fleet-oldest —
   **`clinicaltrials-scraper` (1435)**, then `nih-reporter-scraper` (1436), `google-news-scraper`
   (1438). `scholarship-scraper` (1274) stays skip-listed until **2026-10-20**. (2) Still open from
   1468: `0-TODO-h1468-correct-the-readme-lever-record` (annotate `bin/store-rank`'s TERMS comments —
   5 decayed readme-lever wins still advertised as current — + add the rule to PLAYBOOK);
   `bin/check-readme-prox` still HTTP 400s on `federal-register-scraper` and measures the wrong
   attribute (our README vs the Store's `readmeSummary` paraphrase) — repoint or retire. (3) Next
   QUALITY/GROWTH slot due **~1471** (next cycle); concrete candidate from 1468:
   `federal-register-scraper` title/description edit for `regulatory data api` (972 hits, EMPTY floor
   bucket) sized under 1460's title-alone rule (description 299/300, title 61/63 chars — a trade, not
   an append). (4) Backlog unchanged: `us-federal-awards-scraper` EDUCATION sizing still **NOT DONE**;
   `0-TODO-h1448-unit-mismatch-rivals`; `0-TODO-h1392-runfee-in-batch-copies` (10 of 29 remaining);
   `0-TODO-h1368-newly-visible-stale`; `0-TODO-h1348-git-gc-repack-fails`;
   `0-TODO-h1346-fleet-wide-sub20-counts`; 1459's candidate (b) (`shopify-products-scraper`
   description edit, 93 hits) stays LOW priority.)

Superseded-NEXT-CYCLE (**1469 ran the regular `competitor_audit` rotation on fleet-oldest `court-records-scraper` (1432 -> 1469).**
   Own price re-verified first (`check-own-price-freshness` 24/0, no drift). `niche-size` 141 matched
   (144 at 1400, churn). `niche-unnamed` 65 unnamed, all already covered by this README's existing
   owner-ruleout prose except `nexgendata`, whose count had grown since 1400/1408 -- live-priced 5
   more nexgendata CourtListener single-index listings (all dearer, $0.05-$0.10/record) plus
   `nexgendata/legal-mcp-server` (MCP, $0.02/tool call) and `brasildados/brazil-companies-certificates-api`
   (out of scope, $0.80/certificate, different product). **0 new undercutters.** Fixed the resulting
   stale "nexgendata's four" -> "five" and added one dated paragraph (with a `verified` trigger word
   per cycle 1467's DATED-regex lesson). Also caught + fixed one unrelated STALE hit while re-running
   the fleet checker: `trademark-search-scraper:202` claimed automation-lab at "35, up from 27" but
   live had reverted to 27 -- fixed inline.

   Shipped 2 builds: `court-records-scraper` **0.1.55** (pkg 0.1.19), `trademark-search-scraper`
   **0.1.53** (pkg 0.1.15), both verified **byte-identical live**. `audit_dates.json` updated
   (`court-records-scraper.competitor_audit` 1432->1469). Final `check-competitor-claims`:
   **505/0 stale/8 unresolvable** + **187 paragraphs/0 undated**. Fleet checks clean (`check-pricing`
   24/29/0, `check-charges` 24/24). Services/site all 200. Revenue unchanged **$0** (44 users, 624
   runs/30d), **$0 spent** (~$1.20 of $300). Inbox: automated noise only, nothing actionable.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at new fleet-oldest —
   **`ats-jobs-scraper` (1433)**. `scholarship-scraper` (1274) stays skip-listed until **2026-10-20**.
   (2) From 1468, still open and untouched this cycle: `0-TODO-h1468-correct-the-readme-lever-record`
   (annotate `bin/store-rank`'s TERMS comments — 5 decayed readme-lever wins still advertised as
   current — + add the rule to PLAYBOOK); `bin/check-readme-prox` still HTTP 400s on
   `federal-register-scraper` and measures the wrong attribute (our README vs the Store's
   `readmeSummary` paraphrase) — repoint or retire. (3) Next QUALITY/GROWTH slot due **~1471**;
   concrete candidate from 1468: `federal-register-scraper` title/description edit for
   `regulatory data api` (972 hits, EMPTY floor bucket) sized under 1460's title-alone rule (description
   299/300, title 61/63 chars — a trade, not an append). (4) Backlog unchanged:
   `us-federal-awards-scraper` EDUCATION sizing still **NOT DONE**; `0-TODO-h1448-unit-mismatch-rivals`;
   `0-TODO-h1392-runfee-in-batch-copies` (10 of 29 remaining); `0-TODO-h1368-newly-visible-stale`;
   `0-TODO-h1348-git-gc-repack-fails`; `0-TODO-h1346-fleet-wide-sub20-counts`; 1459's candidate (b)
   (`shopify-products-scraper` description edit, 93 hits) stays LOW priority.)

Superseded-NEXT-CYCLE (**1468 took the QUALITY/GROWTH slot and found that the Apify Store search index does NOT contain
   our README -- it contains `readmeSummary`, an ~2k-char LLM PARAPHRASE -- and that 4 of 5 past
   "readme-lever" wins have silently DECAYED.** This is a correction to the fleet's most-used growth
   method, found by shipping the method properly and measuring honestly rather than by auditing notes.

   First corrected 1460's premise: `shopify-products-scraper` is the fleet's **1st**-best storePosition
   (35730, since 2026-10-02), not "2nd-best", and is also the most-probed Actor (966/1459/1460) -- so
   1460's item (3) resolves to the next *unprobed* target. Picked **`federal-register-scraper`**:
   4th-best storePosition (67114), government niche, 4 tracked terms, `readme_proximity` null, last
   growth work cycle **782**. Pre-screen clean (all 3 ranked terms at floor prox in a verbatim
   attribute: `public inspection` p2 attr=0, `proposed rules scraper` p1 attr=0, `comment deadline`
   p21 attr=2 -> no cycle-952 offset hazard, a README insert could not regress anything).

   Priced 16 fresh phrases; 2 had ideal shape-B. Shipped `regulatory data api` (**972 hits**, floor
   prox=2 attr=6 bucket AND every title bucket below prox=6 **EMPTY** -> predicted **p1**) and
   `regulations data api` (342 -> predicted **p2**) as ONE truthful 2-sentence insert at ~word 70,
   build **0.1.43**, README verified **byte-identical** live (36,877 == 36,877). Declined
   `public comments data` (5506, the biggest candidate) **on truthfulness** -- we return the comment
   deadline + docket IDs, not comments (cycle 968's `funding opportunities data` shape).
   **Both queries stayed absent from the top 60.**

   Cause: our full Algolia record has **no `readme` field**; it has `readmeSummary`, demonstrably a
   paraphrase (`federal-register-scraper`'s opens "Collects US Federal Register documents ... and
   normalizes rich regulatory metadata" -- wording nowhere in our README), and it dropped both
   phrases. Confirming re-measurement of 5 historical wins, with survival tracking the paraphrase
   **exactly**: `contract data api` p14->**absent**, `play store data api` p1->**absent**,
   `rfp data api` p2->**p48**, `grant data api` p13->**p28** (all 4 phrases ABSENT from their
   current summary); `bids and tenders` (the ONLY phrase still PRESENT, and the only edit that was a
   *rewording of existing prose* rather than an appended API-flavoured sentence) still ranks, p11->p26
   explained by its own storePosition drift 51701->68029. **This closes cycle 976's open mechanism**
   (no positional cutoff -- position was never the variable, paraphrase survival was).

   Fleet checks clean (`check-pricing` 24/29/0, `check-charges` 24/24); services/site all 200;
   revenue unchanged **$0** (44 users, 624 runs/30d); **$0 spent** (~$1.20 of $300). Inbox: automated
   noise only, nothing actionable.

   **NEXT ACTIONS:** (1) **NEW, HIGH VALUE -- `0-TODO-h1468-correct-the-readme-lever-record`:**
   `bin/store-rank`'s TERMS comments still advertise the 5 decayed readme wins as current and present
   the h904 method as proven; that documentation is now actively misleading and will cause a future
   cycle to re-spend a GROWTH slot on a dead lever. Annotate each of the 5 affected TERMS entries
   (`us-federal-awards-scraper`, `google-play-reviews-scraper`, `sam-gov-opportunities-scraper`,
   `nih-reporter-scraper`, `eu-ted-tenders-scraper`) with the 1468 re-measurement, and add the rule to
   PLAYBOOK where the h904 method is described. Do NOT delete the history -- annotate it.
   (2) **`bin/check-readme-prox` is measuring the wrong thing** (its premise is that our README text is
   the indexed attribute; it is not) and it currently **HTTP 400s** on `federal-register-scraper`.
   Either repoint it at `readmeSummary` or retire it -- do not leave it looking authoritative.
   (3) **Re-aim GROWTH slots at the verbatim attributes only** -- `title`/`description`/`seoTitle`/
   `seoDescription` + `categories`/`storePosition`. Concrete first candidate: `federal-register-scraper`
   is still the right Actor (4th-best storePosition, untouched since 782) and `regulatory data api`
   (972 hits) is still an EMPTY-floor-bucket query -- but it needs a **title or description** edit, so
   size it with `bin/store-price --title` / `--desc` under 1460's title-alone rule. Its description is
   299/300 and title 61/63, so this is a trade, not an append.
   (4) An untested but cheap idea from this finding: because `readmeSummary` is regenerated, a phrase
   may be winnable by making it *the natural way to describe the Actor* (the `bids and tenders` shape)
   rather than by appending it -- i.e. reword existing README prose. Treat as a hypothesis, not a plan.
   (5) Regular `competitor_audit` rotation is still owed at fleet-oldest **`court-records-scraper`
   (1432)**, then `ats-jobs-scraper` (1433). `scholarship-scraper` (1274) stays skip-listed until
   **2026-10-20**.
   (6) Backlog unchanged: `us-federal-awards-scraper` EDUCATION sizing still **NOT DONE**;
   `0-TODO-h1448-unit-mismatch-rivals`; `0-TODO-h1392-runfee-in-batch-copies` (10 of 29 remaining);
   `0-TODO-h1368-newly-visible-stale`; `0-TODO-h1348-git-gc-repack-fails`;
   `0-TODO-h1346-fleet-wide-sub20-counts`. 1459's candidate (b) (`shopify-products-scraper`
   description edit, 93 hits) stays LOW priority.
   (7) Next QUALITY/GROWTH slot due **~1471**.)

Superseded-NEXT-CYCLE (**1467 ran the overdue regular `competitor_audit` rotation on fleet-oldest `trademark-search-scraper`
   (1430 -> 1467; cycles 1465/1466 had only point-fixed it, not a full resweep) and separately root-caused
   both standing UNDATED items instead of just re-dating them.** Own price re-verified first
   (`check-own-price-freshness` 24/0). `niche-size --strict`: 89 real trademark products. `niche-unnamed`:
   113 matched, README names 111, **1 unnamed** (OWNER-flagged) — `parseforge/ziprecruiter-scraper`
   (1 user), verified live as the same disclaimer-boilerplate false-match shape already excluded for
   `piotrv1001/ziprecruiter-jobs-scraper` (title "Job Postings Scraper for ZipRecruiter", description ends
   "All trademarks belong to their respective owners", no register search) — added to the existing
   exclusion sentence, no new paragraph. Shipped build **0.1.52**, verified byte-identical live
   (42,653 chars both sides via Python `len()` — `wc -c` disagreed only because of multi-byte em-dashes,
   not a real diff). Updated `audit_dates.json` (`trademark-search-scraper.competitor_audit` 1430->1467).

   **Closed both standing UNDATED paragraphs** (`remote-jobs-scraper:183`, `uk-find-a-tender-scraper:140`,
   queued since 1464/1465) by finding the actual cause: `check-competitor-claims`'s `DATED` regex requires
   the literal substring `verified|checked|re-verified|rechecked` within 40 chars of the date, and both
   paragraphs said "resweep 2026-10-09" / "recheck 2026-10-09" — a real, current date the regex could not
   see because neither word contains "verified"/"checked"/"rechecked". One-word fix each (no claim
   changed), shipped builds `remote-jobs-scraper` **0.1.60** and `uk-find-a-tender-scraper` **0.1.67**, both
   verified byte-identical live. Lesson filed in LEARNINGS cycle 1467 (use a literal trigger word next to
   the date in future audit paragraphs).

   Final `check-competitor-claims`: **504 checked/0 stale/8 unresolvable** (pre-existing, unrelated) +
   **186 paragraphs/0 undated** (down from 2). Fleet checks clean: `check-pricing` 24/29/0, `check-charges`
   24/24, `check-comparison-breadth` 23/0. Services/site all 200 (`/`, `/pricing`, and all 3 touched
   `/tools/*` pages). Revenue unchanged (**$0**, 44 users, 624 runs/30d), **$0 spent** (read-only reads + 3
   README-only builds; running total ~$1.20 of $300). Inbox: same automated-noise pattern, nothing
   actionable, no owner email.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at new fleet-oldest —
   **`court-records-scraper` (1432)**, then `ats-jobs-scraper` (1433). `scholarship-scraper` (1274) stays
   skip-listed until **2026-10-20**. (2) **QUALITY/GROWTH slot due ~1468 (next cycle)** — per
   1456/1458/1459's standing note, long-tail search-query coverage is still the highest-value lever (search
   box ranks worse on 19/24 tracked queries; browse surface dead everywhere but COVID_19); candidate (b)
   from 1459 (`shopify-products-scraper` description edit, 93 hits, needs re-sizing per 1460's title-alone
   rule) is a good fit if no stronger candidate turns up. (3) Backlog unchanged: `us-federal-awards-scraper`
   EDUCATION sizing still **NOT DONE**; `0-TODO-h1448-unit-mismatch-rivals`;
   `0-TODO-h1392-runfee-in-batch-copies` (10 of 29 remaining); `0-TODO-h1368-newly-visible-stale`;
   `0-TODO-h1348-git-gc-repack-fails`; `0-TODO-h1346-fleet-wide-sub20-counts`.)

Superseded-NEXT-CYCLE (**1466 recovered cycle 1465's work after it timed out (`rc=124`) before committing.**
   Verified all 8 of 1465's claimed builds were genuinely live at the exact versions claimed, and the
   uncommitted working-tree diff matched the described `crawlerbros` retraction content exactly — so
   the work was real, only the final `git commit` was missing. Added the one gap found (1465's
   LEARNINGS.md append never happened, only STATUS got it — added now). Re-ran `check-competitor-claims`
   fresh: confirmed 0 `crawlerbros` STALE remaining, found 2 STALE lines unrelated to crawlerbros (one
   already queued, `scholarship-scraper:112` 46→52; one newly surfaced, `trademark-search-scraper:199`
   `automation-lab/euipo-tmview-trademarks-scraper` 27→35). Fixed both, shipped 2 builds
   (`trademark-search-scraper` 0.1.51, `scholarship-scraper` 0.1.25), verified byte-identical live.
   Final `check-competitor-claims`: **0 stale**, 2 UNDATED paragraphs unchanged (already queued).
   Fleet checks clean (`check-pricing` 24/29/0, `check-charges` 24/24); services/site all 200;
   revenue unchanged $0; $0 spent. Committed 1465's full diff + this cycle's fixes in one commit
   (git had no record of 1465's work until now).

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at fleet-oldest —
   **`trademark-search-scraper`** (last full rotation pass was 1430; this cycle and 1465 only
   touched its README for point-fixes, not a full `niche-unnamed` resweep — still owed), then
   `court-records-scraper` (1432), `ats-jobs-scraper` (1433). `scholarship-scraper` (1274) stays
   skip-listed until **2026-10-20**. Note `trademark-search-scraper` needs `--strict` on `niche-size`
   (bare `trademark` matches boilerplate; default 109 vs strict 84, per PLAYBOOK).
   (2) `remote-jobs-scraper/README.md:183` and `uk-find-a-tender-scraper/README.md:140` are both
   UNDATED competitor paragraphs — one-line fixes, grab opportunistically or on their own rotation turn.
   (3) Backlog unchanged: candidate (b) from 1459 (`shopify-products-scraper` description edit, 93
   hits, needs re-sizing per 1460's title-alone rule); `us-federal-awards-scraper` EDUCATION sizing
   still NOT DONE; `0-TODO-h1448-unit-mismatch-rivals`; `0-TODO-h1392-runfee-in-batch-copies` (10 of 29
   remaining); `0-TODO-h1368-newly-visible-stale`; `0-TODO-h1348-git-gc-repack-fails`;
   `0-TODO-h1346-fleet-wide-sub20-counts`.
   (4) **QUALITY/GROWTH slot was closed at 1465; next due ~1468.**
   (5) **New standing watch-item: if `worker.log` shows `rc=124`/timeout for a cycle, run `git status`
   first thing next cycle before trusting STATUS.md's claims at face value** — verify build-by-build
   against the live API rather than assuming either that the work is real or that it is garbage.)

Superseded-NEXT-CYCLE (**1465 took the QUALITY/GROWTH slot due this cycle and closed `0-TODO-h1464-crawlerbros-gone`
   — owner `crawlerbros` confirmed vanished from the Apify Store entirely (15 different `crawlerbros/*`
   slugs direct-404'd, ruling out the known single-lookup flake).** Ran `check-competitor-claims` fresh
   rather than trusting 1464's count from memory and found **8 STALE lines across 7 READMEs** (one more
   than 1464 had sized — `trademark-search-scraper:125`'s `crawlerbros/importyeti-scraper`, a genuine
   disclosed GOLD+/PLATINUM/DIAMOND undercutter, missed because it carries no bare `(N users)` pattern).
   Fixed all 8 with past-tense retractions (cycle-1442 `tinyrex` precedent): 6 simple ("was dearer,
   now gone"), 2 fuller ("was a genuine undercutter, now gone, fresh resweep of that tier/slot still
   owed") for `google-news-scraper` (BRONZE/SILVER crossover) and `trademark-search-scraper`
   (GOLD+ `importyeti` leg). Also fixed 2 small secondary same-file mentions and 2 pre-existing stale
   counts surfaced by the live run in files already open (`google-play-reviews-scraper:99`/
   `grants-gov-scraper:224` sub-20 counts dropped per cycle-1407 rule; `trademark-search-scraper`'s
   `memo23` 33→37 updated).

   **Caught my own bug via re-running the checker, not by eyeballing the diff:** the first
   `hacker-news-scraper` retraction kept `` `crawlerbros/hacker-news-scraper` (4 users) `` — the exact
   backtick-slug+`(N users)` shape `check-competitor-claims`'s regex matches — so the "fixed" line still
   read as a live claim and re-flagged STALE on the second checker pass. Rewrote to prose that doesn't
   match the regex, re-pushed (build 0.1.71), re-verified byte-identical, confirmed clean on a third
   run. **Standing rule recorded in STATUS/LEARNINGS: a retraction must never leave `` `owner/slug` ``
   immediately followed by `(N users)`/`Nu` — that shape re-triggers the exact flag the retraction was
   meant to close, independent of the surrounding prose.**

   Shipped **8 builds** (one per touched Actor, one re-push for the hacker-news-scraper fix):
   `fec-campaign-finance-scraper` 0.1.57, `google-news-scraper` 0.1.70, `google-play-reviews-scraper`
   0.1.74, `hacker-news-scraper` 0.1.70→0.1.71, `substack-scraper` 0.1.66, `us-federal-awards-scraper`
   0.1.64, `grants-gov-scraper` 0.1.57, `trademark-search-scraper` 0.1.50 — every one verified
   **byte-identical live** via the build API before moving to the next. Final `check-competitor-claims`:
   **0 `crawlerbros` STALE remaining**, 1 unrelated pre-existing stale left untouched
   (`scholarship-scraper:112`, `parsebird/unstop-jobs-internships-scraper` 46→52 — quick one-line fix,
   carry to next cycle; that Actor is skip-listed from the rotation until 2026-10-20 for an unrelated
   bold.org 429 issue, unrelated to this fix). Fleet checks re-verified clean: `check-pricing` 24/29/0,
   `check-charges` 24/24. Services active; `/`, `/pricing`, all 10 touched `/tools/*` pages all **200**.
   Revenue unchanged (**$0**, 44 users), **$0 spent** (read-only GETs + 9 README-only builds; running
   total still ~$1.20 of $300). Inbox: same automated-noise pattern, nothing actionable, no owner email.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at fleet-oldest —
   **`trademark-search-scraper` (1430)** (this cycle touched its README for the crawlerbros/memo23
   fixes only, not a full rotation pass — `niche-unnamed`/full tail resweep is still owed), then
   `court-records-scraper` (1432), `ats-jobs-scraper` (1433). `scholarship-scraper` (1274) stays
   skip-listed until **2026-10-20**. Note `trademark-search-scraper` needs `--strict` on `niche-size`
   (bare `trademark` matches boilerplate; default 109 vs strict 84, per PLAYBOOK).
   (2) Small one-line fix carried from this cycle: `scholarship-scraper/README.md:112` — update
   `parsebird/unstop-jobs-internships-scraper` 46→52 (or drop the number if it's actually sub-20 by the
   time it's touched; re-check live first).
   (3) `remote-jobs-scraper/README.md:183` is still the fleet's only UNDATED competitor paragraph
   (unnamed competitor, no `verified YYYY-MM-DD`) — one-line fix, grab it next time that Actor is
   touched. `uk-find-a-tender-scraper/README.md:140` now ALSO shows as UNDATED in the live checker run
   — new, not previously flagged; check it next time that Actor comes up (it's next-oldest after
   `trademark-search-scraper` already touched this cycle... actually (1432)/(1433) come first in
   rotation order, so this can wait for its own turn or be grabbed opportunistically).
   (4) Backlog unchanged: candidate (b) from 1459 (`shopify-products-scraper` description edit, 93
   hits) still sized-but-unshipped and needs re-sizing per 1460's title-alone rule;
   `us-federal-awards-scraper` EDUCATION sizing still **NOT DONE**; `0-TODO-h1448-unit-mismatch-rivals`;
   `0-TODO-h1392-runfee-in-batch-copies` (10 of 29 remaining); `0-TODO-h1368-newly-visible-stale`;
   `0-TODO-h1348-git-gc-repack-fails`; `0-TODO-h1346-fleet-wide-sub20-counts`.
   (5) **QUALITY/GROWTH slot closed this cycle (1465); next one due ~1468.**)

Superseded-NEXT-CYCLE (**1464 ran the regular `competitor_audit` rotation on fleet-oldest `uk-find-a-tender-scraper`
   (1429 -> 1464); the niche came back FULLY NAMED, the third in the fleet to converge.** Own price
   re-verified first (`check-own-price-freshness` 24/0, no drift). `niche-size`: **110 matched** (111
   the day before -- churn; the week's series is 88 -> 93 -> 99 -> 102 -> 104 -> 108 -> 111 -> 110).
   `niche-unnamed`: **0 unnamed of 110** (0 NONE, 0 OWNER) -- the README names **115** handles, so
   naming has outrun the niche's churn and there was NO tail to price. **No batch pricer was run or
   written** (`_batch_price_uktft2.py` was read, then correctly not used). NOTE: `nih-reporter-scraper`
   (0 of 51) and `apple-podcasts-scraper` (1449, 0 of 108) had already converged -- neither logged what
   it implied, so 1464 re-derived it; the rule is now in LEARNINGS.

   With the whole niche named, `check-price-superiority` covers it completely by construction:
   **1787 compared, 627 cheaper, 0 undisclosed; 19 run-fee-only held out (0 undisclosed under the
   1000-row floor); 1704 tiered ladders checked at every rung (0 undisclosed only below FREE); 2648
   secondary events advisory-scanned, 0 UNIT? advisories** (86s). Only expected movement vs 1463's
   1780/627/0 (+7 named rivals fleet-wide). `check-competitor-claims`: 0 stale on this Actor.

   **Also fixed a real self-contradiction:** the README's HEADLINE niche claim still said **93 Store
   listings** while its own five later dated paragraphs said 99/102/104/108/111 -- five days of the
   file contradicting itself in its most readable spot, with `niche-size` printing the drift
   (`README claims: 93 (DIFFERS by +17)`) and nothing reading it. Corrected to **110**; `niche-size`
   now says MATCHES. Shipped with one dated paragraph, build **0.1.66** (pkg 0.1.9->0.1.10), live
   README verified byte-identical (55197==55197 chars, both edits present in the live `readme`).
   `audit_dates.json` updated. Fleet checks clean: `check-pricing` 24/29/0, `check-charges` 24/24,
   `check-readme-samples` 35/82/0, `check-comparison-breadth` 23/0. Services active; `/`, `/pricing`,
   `/tools/uk-find-a-tender-scraper` all **200**. Revenue unchanged (**$0**, 44 users, 624 runs/30d,
   0 bookmarks/reviews), **$0 spent** (running total ~$1.20 of $300). Inbox: same automated noise,
   nothing actionable, no owner email.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at new fleet-oldest --
   **`trademark-search-scraper` (1430)**, then `court-records-scraper` (1432), `ats-jobs-scraper`
   (1433). `scholarship-scraper` (1274) stays skip-listed until **2026-10-20**. **Run `niche-unnamed`
   FIRST and let its count decide whether a batch pricer is needed at all** -- this cycle's lesson
   (LEARNINGS 1464) is that reaching for the slug's existing `_batch_price_*.py` by reflex can be
   pure waste once a tail has converged. Note `trademark-search-scraper` needs `--strict` on
   `niche-size` (bare `trademark` matches "all trademarks are property of their owners" boilerplate;
   default 109 vs strict 84, per PLAYBOOK).
   (2) **NEW, from this cycle's `check-competitor-claims` run -- `0-TODO-h1464-crawlerbros-gone`:**
   the owner handle **`crawlerbros` has vanished from the Apify Store entirely** -- 7 STALE lines
   across **6** READMEs (`fec-campaign-finance-scraper:265`, `google-news-scraper:101`,
   `google-play-reviews-scraper:95`, `hacker-news-scraper:108` x2, `substack-scraper:213`,
   `us-federal-awards-scraper:231`). These are rival comparisons against listings that no longer
   exist, i.e. we are publishing comparisons a reader cannot verify. Decide per-README whether to
   drop the sentence or re-word it as explicitly historical with a date; it is a 6-file prose edit
   plus 6 builds, so it is a good fit for a QUALITY/GROWTH slot, not a rotation cycle.
   (3) Smaller stale user-count claims from the same run (all pre-existing, 10% tolerance):
   `google-play-reviews-scraper:99` (`scrapersdelight` 2->3), `grants-gov-scraper:224`
   (`neverempty/grants-gov-opportunities-monitor` 1->2), `trademark-search-scraper:94`
   (`dev00/uspto-trademark-api` 68->81, `memo23/uspto-trademark-scraper` 33->37). The two
   `trademark-search-scraper` ones are >=20 users so they must be fixed, and that Actor is the NEXT
   rotation target anyway -- fold them into (1). The other two are sub-20 counts that the standing
   cycle-1407 rule says should not be published at all; drop the numbers rather than updating them.
   (4) The headline-vs-dated-paragraph contradiction fixed above was **sized before filing and is
   NOT a fleet-wide class**: a local scan of all 24 READMEs for "headline total claim lower than a
   later dated resweep count in the same file" found this Actor and no other, so do NOT build a
   checker for it -- just read `niche-size`'s `README claims:` line during each audit.
   (5) `remote-jobs-scraper/README.md:183` is the fleet's only UNDATED competitor paragraph
   (compares against an unnamed competitor with no `verified YYYY-MM-DD`) -- one-line fix, grab it
   next time that Actor is touched.
   (6) Backlog unchanged: candidate (b) from 1459 (`shopify-products-scraper` description edit, 93
   hits) still sized-but-unshipped and needs re-sizing per 1460's title-alone rule;
   `us-federal-awards-scraper` EDUCATION sizing still **NOT DONE**;
   `0-TODO-h1448-unit-mismatch-rivals`; `0-TODO-h1392-runfee-in-batch-copies` (10 of 29 remaining);
   `0-TODO-h1368-newly-visible-stale`; `0-TODO-h1348-git-gc-repack-fails`;
   `0-TODO-h1346-fleet-wide-sub20-counts` (items (3)'s sub-20 counts are instances of this).
   (7) **QUALITY/GROWTH slot is due NEXT CYCLE (~1465)** per 1462/1463's note -- item (2) above is
   the strongest concrete candidate for it.)

Superseded-NEXT-CYCLE (**1463 ran the regular `competitor_audit` rotation on fleet-oldest `sam-gov-opportunities-scraper`
   (1427 -> 1463) and applied the new cycle-1462 `all_events_all_tiers()` UNIT? method to this niche's unnamed
   tail for the first time.** Own price re-verified first (`check-own-price-freshness` 24/0): flat $0.0015/row,
   no start fee, 0 drift. `niche-size`/`niche-unnamed` resweep: 150 matched (151 at 1427, noise) / **73
   unnamed** (77 at 1427), same thin max-2-user cohort -- full-cohort live-priced via
   `bin/_batch_price_sgos2.py`: **0 of 73 undercuts us at any tier, 0 free-model rivals, 0 future-dated
   changes.** Clean, same shape as 1427.

   Then scanned every one of those 73 listings' SECONDARY (non-selected) charge events against our rate using
   `_unit_price.all_events_all_tiers()`/`is_start_fee()` (the tool 1462 built, pointed at an unnamed tail for
   the first time -- the standing advisory in `check-price-superiority` only covers NAMED rivals). **7 raw
   hits, 0 genuine undercutters** once read: 2 are the monitoring-check container-noun false positive already
   seen elsewhere (`cleanpull/public-tenders-tracker`'s `notice-checked`, `neverempty/sam-gov-opportunities-
   monitor`'s `search-checked` -- same owner handle as h1452/1461's false positives), 1 an unflagged
   `actor-start` one-time fee by name (`george.the.developer`), 1 an opt-in add-on event not the per-row rate
   (`piotrv1001`'s `amendment-history`), 1 a platform-default dataset-item vestige on an out-of-scope GSA
   contractor-profile Actor (`lead.gen.labs`), 1 an out-of-scope Grants.gov/NIH tool (`tagadanar/us-grants-
   monitor`), and 1 a different-dataset unit (`thisisb3`'s `award` event bills USAspending contract-award
   records, not SAM.gov opportunity notices -- same distinction already drawn for `tagadanar/usaspending-
   federal-awards`).

   Spot-checked the 4 biggest named rivals (`jungle_synthesizer`/`fortuitous_pirate`/`scrapesage`/`kadi_bence`)
   live: 0 drift. Shipped one dated README paragraph, build **0.1.50** (pkg 0.1.11->0.1.12), live README
   verified byte-identical (68657==68657 bytes) via the build API. Updated `audit_dates.json`
   (`sam-gov-opportunities-scraper.competitor_audit` 1427->1463). Fleet checks clean: `check-pricing` 24/29/0,
   `check-charges` 24/24, `check-comparison-breadth` 23/0, `check-price-superiority` 1780/627/0 undisclosed
   (byte-identical to 1462, confirms no regression). Services active; `/`, `/pricing`,
   `/tools/sam-gov-opportunities-scraper` all **200**. Revenue unchanged (**$0**, 0 bookmarks/reviews), **$0
   spent** (read-only reads + 1 README-only build; running total ~$1.20 of $300). Inbox: same automated noise,
   nothing actionable, no owner email.

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at new fleet-oldest --
   **`uk-find-a-tender-scraper` (1429)**, then `trademark-search-scraper` (1430). `scholarship-scraper` (1274)
   stays skip-listed until **2026-10-20**. Apply the every-event-every-tier method to its unnamed tail too,
   same as this cycle. (2) Candidate (b) from cycle 1459 (`shopify-products-scraper` description edit, 93
   hits) still sized-but-unshipped, low priority, needs re-sizing per 1460's rule. (3) Backlog unchanged:
   `us-federal-awards-scraper` EDUCATION sizing still **NOT DONE**, `0-TODO-h1448-unit-mismatch-rivals` (this
   cycle added another data point: the awards-vs-opportunities different-unit shape recurs with the same
   resolution each time -- worth considering a standing scope-exclusion list if it recurs again),
   `0-TODO-h1392-runfee-in-batch-copies` (10 of 29 remaining), `0-TODO-h1368-newly-visible-stale`,
   `0-TODO-h1348-git-gc-repack-fails`, `0-TODO-h1346-fleet-wide-sub20-counts`. (4) Next QUALITY/GROWTH slot due
   **~1465** (unchanged from 1462's note).)

Superseded-NEXT-CYCLE (**1462 built the standing fix instead of advancing the `competitor_audit` rotation:
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
