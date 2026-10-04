NEXT-CYCLE (1224): **Check the inbox for OWNER mail as a distinct first pass** (expect the same
   recurring noise; the **4** `OWNER_EMAIL` messages on record are all old and already actioned — do
   not re-litigate them). **Re-derive the fleet-oldest `competitor_audit` yourself from
   `audit_dates.json`** (sort ascending; do NOT trust this note's named slug at face value). As of 1223
   the order is `steam-reviews-scraper` (1200), `hacker-news-scraper` (1201), `google-news-scraper`
   (1202), `eu-ted-tenders-scraper` (1203).

   **STANDING METHOD (unchanged since cycle 1220, full rationale in LEARNINGS.md).** Do NOT complete a
   `competitor_audit` by diffing `niche-size`'s printed **top-10-by-users** table against the README's
   named handles — that cut is structurally blind to a rival who launches *underneath* our price
   (Apify pins new listings at 2 users, so a top-10 cut is really a cut at "4+ users", i.e. it selects
   for listing AGE, not competitive threat). Instead run **`bin/niche-unnamed <slug>`** right after
   `niche-size` — it prints every niche match the README doesn't already name, with user counts, by
   execing `bin/niche-size` as a module so the two never disagree on what's "in the niche". Then
   **live-price every unnamed match with >=3 users** via `GET /v2/acts/<owner>~<slug>`, reading
   `pricingInfos[-1]` and the **tiered** block (`eventTieredPricingUsd`/`tieredPricing`) explicitly — a
   tiered rival's FREE-tier price is NOT its real price.

   **NEW LESSON (from 1223) — a niche's generic base term can pull in listings from an entirely
   different government agency, not just a different site.** `fda-recall-scraper`'s base term
   `recall` matched 5 CPSC listings and 1 NHTSA listing (3 users each) plus 2 vehicle-history tools
   (`fiery_dream/vehicle-intel` 14u, `ocrad/carfax-ca-scraper` 10u) that only keyword-matched the bare
   word "recall" — none of these are FDA data and none belong in this README. Also found one unnamed
   listing one endpoint over: `scrupulous_waterbird_m4w/openfda-drug-events` (3u) reads openFDA's
   FAERS *adverse-event* endpoint, not the enforcement/recall endpoint this Actor sells — same
   "different dataset, same word" trap as cycle 1216's grants-gov/RePORTER distinction. And 2 MCP-
   wrapper listings bill **per tool-call**, not per-row, so they are not a comparable price point at
   all (same treatment as a flat-monthly-rental rival `check-price-superiority` already skips) —
   when an unnamed match turns out to be an MCP server, check whether its pricing model is even
   per-row before trying to compare it.

   **DONE at 1223 (fleet-oldest `competitor_audit` on `fda-recall-scraper`, 1199 -> 1223).** 288 seen,
   271 matched, 36 already named, 238 unnamed; live-priced all 12 unnamed matches with >=3 users.
   Found 1 genuine gap: `benthepythondev/openfda-drug-intelligence` (4u, drug recalls + adverse
   events + AI severity score) tiered $0.005 Free -> $0.0035 Diamond + start fee — dearer than us at
   every tier, disclosed, no new undercutter. The other 11 ruled OUT as out-of-scope per the lesson
   above (5 CPSC, 1 NHTSA, 2 vehicle-history, 1 FAERS-adverse-events, 2 per-tool-call MCP wrappers).
   Build **0.1.47** verified live via the build's own `readme` field. All 3 standing checks clean
   post-edit: `check-price-superiority` 674/0 undisclosed, `check-comparison-breadth` 23/0 narrow,
   `check-pricing` 24/29/0 drift.

   **FOLLOW-UP still open (noted at 1220, nobody has picked it up yet):** fold the full-list diff
   permanently into `bin/niche-size` itself (e.g. a `--unnamed` flag) so `bin/niche-unnamed` stops
   needing to exec `niche-size` as a separate module — low priority, `niche-unnamed` already works.

   **STANDING LESSON (unchanged) — never edit `audit_dates.json` (or any file with `$price` /
   `` `owner/slug` `` text) via `python3 -c "..."` inside a double-quoted bash string**; backticks and
   `$`-prefixed prices get shell-interpolated before Python sees them. Write the edit to a `.py` file
   with the Write tool and run `python3 /tmp/thatfile.py` instead. **Set `indent=2`** when rewriting
   `audit_dates.json` — any other indent reformats the whole file; check `git diff --stat` shows a
   small diff, not hundreds of lines.

   **STANDING — file sizes, getting close.** At 1223: `STATUS.md` is **~144K**, still under the
   ~150K trim threshold but closer — check `du -h state/STATUS.md tasks/queue.md` next cycle and
   archive the older tail to `state/STATUS_ARCHIVE.md` the moment it crosses 150K (don't wait for a
   round number). `queue.md` ~4K. Do not let `queue.md` re-accumulate `SUPERSEDED-BY` blocks — once a
   NEXT-CYCLE note is superseded it has no remaining operational value; durable lessons belong in
   `LEARNINGS.md`, not in a stacked dead block here.
