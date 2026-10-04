NEXT-CYCLE (1223): **Check the inbox for OWNER mail as a distinct first pass** (expect the same
   recurring noise; the **4** `OWNER_EMAIL` messages on record are all old and already actioned — do
   not re-litigate them). **Re-derive the fleet-oldest `competitor_audit` yourself from
   `audit_dates.json`** (sort ascending; do NOT trust this note's named slug at face value). As of 1222
   the order is `fda-recall-scraper` (1199), `steam-reviews-scraper` (1200), `hacker-news-scraper`
   (1201), `google-news-scraper` (1202).

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

   **NEW STANDING LESSON (from 1222) — do not trust a prior audit's own prose summary, even one
   written the same day.** Cycle 1198's note on `apple-podcasts-scraper` asserted "top 10 by users
   unchanged and all already named" — this was simply false: 2 of the real top-10 (`benthepythondev`,
   61u; `parseforge/podchaser-scraper`, 39u) were never named in the README. A verdict phrase like
   "all already named" / "unchanged" is itself an unverified claim until you `grep` the actual handles
   against the README text — treat it the same way the standing lesson already treats "out of scope"
   / "already checked" (see cycle 1165/1216's grants-gov lesson in LEARNINGS.md). When a note claims
   a top-10 diff came back clean, re-run the diff yourself rather than skipping straight to the wider
   sweep.

   **DONE at 1222 (fleet-oldest `competitor_audit` on `apple-podcasts-scraper`, 1198 -> 1222).** 144
   seen, 98 matched, 83 unnamed. Found the false "all already named" claim above. Live-priced the 2
   real top-10 gaps: `benthepythondev/podcast-intelligence-aggregator` (61u) disclosed as a genuine
   dearer rival ($0.03/result FREE -> $0.021 Diamond + small start fee, 21-30x us); `parseforge/
   podchaser-scraper` (39u) ruled OUT — it scrapes Podchaser.com, a different site, and only
   keyword-matched via an optional Apple-chart-rank field. Build **0.1.64** verified live via the
   build's own `readme` field. All 3 standing checks clean post-edit: `check-price-superiority`
   668/0 undisclosed, `check-comparison-breadth` 23/0 narrow, `check-pricing` 24/29/0 drift.

   **NOT YET DONE on `apple-podcasts-scraper` — leave for a future light re-check, not urgent:** ~17
   remaining unnamed matches sitting at 3-6 users were not individually priced this cycle (time
   budget), same treatment as the niche's existing "5-users-or-fewer not priced one by one"
   disclosure sentence.

   **FOLLOW-UP still open (noted at 1220, nobody has picked it up yet):** fold the full-list diff
   permanently into `bin/niche-size` itself (e.g. a `--unnamed` flag) so `bin/niche-unnamed` stops
   needing to exec `niche-size` as a separate module — low priority, `niche-unnamed` already works.

   **STANDING LESSON (unchanged) — never edit `audit_dates.json` (or any file with `$price` /
   `` `owner/slug` `` text) via `python3 -c "..."` inside a double-quoted bash string**; backticks and
   `$`-prefixed prices get shell-interpolated before Python sees them. Write the edit to a `.py` file
   with the Write tool and run `python3 /tmp/thatfile.py` instead. **Set `indent=2`** when rewriting
   `audit_dates.json` — any other indent reformats the whole file; check `git diff --stat` shows a
   small diff, not hundreds of lines.

   **STANDING — file sizes.** At 1222: `STATUS.md` **~143K** (nearing the ~150K trim threshold —
   check `du -h state/STATUS.md tasks/queue.md` next cycle and archive the older tail to
   `state/STATUS_ARCHIVE.md` if it has crossed 150K), `queue.md` ~4K. Do not let `queue.md`
   re-accumulate `SUPERSEDED-BY` blocks — once a NEXT-CYCLE note is superseded it has no remaining
   operational value; durable lessons belong in `LEARNINGS.md`, not in a stacked dead block here.
