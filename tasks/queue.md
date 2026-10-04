NEXT-CYCLE (1222): **Check the inbox for OWNER mail as a distinct first pass** (expect the same
   recurring noise; the **4** `OWNER_EMAIL` messages on record are all old and already actioned — do
   not re-litigate them). **Re-derive the fleet-oldest `competitor_audit` yourself from
   `audit_dates.json`** (sort ascending; do NOT trust this note's named slug at face value). As of 1221
   the order is `apple-podcasts-scraper` (1198), `fda-recall-scraper` (1199), `steam-reviews-scraper`
   (1200), `hacker-news-scraper` (1201).

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

   **DONE at 1221 (fleet-oldest `competitor_audit` on `google-play-reviews-scraper`, 1196 -> 1221).**
   250 niche matches, 218 unnamed. Live-priced the top of that tail (everything with >=4 users, plus
   the review-scoped >=3-user listings — 28 total). **One genuine new undercutter:**
   `dami_studio/google-play-reviews-scraper` — only 4 total users / 0 in last 30d (invisible to any
   users-based cut), but 97 successful runs in the last 30 days and modified 2026-10-03, i.e. real and
   active despite the low user count. Scope matches ours exactly; charges a flat $0.001 Actor-start fee
   plus a review rate tiered $0.00009 FREE down to $0.000087 DIAMOND — undercuts us above ~100
   reviews/run. Disclosed inline next to the existing `fetchcraftlabs` crossover paragraph. Build
   **0.1.56** (package.json 0.1.11) verified live via the build's own `readme` field. All 3 standing
   checks clean post-edit: 564/0 stale + 108/0 undated, **666/178/0** undisclosed, 23/0 narrow.

   **NOT YET DONE on `google-play-reviews-scraper` — leave for a future light re-check, not urgent:**
   ~12 unnamed matches sitting at exactly 3 users were not individually priced this cycle (long tail,
   same treatment as the README's existing "5-users-or-fewer not priced one by one" disclosure
   sentence). Also `shahidirfan/Google-Play-Store-Scraper` (2u, capital-S "Scraper" — a *different*
   listing from the already-named `shahidirfan/Google-Play-Store-Reviews-Scraper`) carries no
   pricing record at all (likely an unpublished/draft Actor) — re-check if it ever gets a price.

   **FOLLOW-UP still open (noted at 1220, nobody has picked it up yet):** fold the full-list diff
   permanently into `bin/niche-size` itself (e.g. a `--unnamed` flag) so `bin/niche-unnamed` stops
   needing to exec `niche-size` as a separate module — low priority, `niche-unnamed` already works.

   **STANDING LESSON (unchanged) — never edit `audit_dates.json` (or any file with `$price` /
   `` `owner/slug` `` text) via `python3 -c "..."` inside a double-quoted bash string**; backticks and
   `$`-prefixed prices get shell-interpolated before Python sees them. Write the edit to a `.py` file
   with the Write tool and run `python3 /tmp/thatfile.py` instead. **Set `indent=2`** when rewriting
   `audit_dates.json` — any other indent reformats the whole file; check `git diff --stat` shows a
   small diff, not hundreds of lines.

   **STANDING — file sizes.** At 1221: `STATUS.md` **140K** (nearing the ~150K trim threshold —
   check `du -h state/STATUS.md tasks/queue.md` next cycle and archive the older tail to
   `state/STATUS_ARCHIVE.md` if it has crossed 150K), `queue.md` reset to ~3K this cycle (dropped the
   dead `SUPERSEDED-BY-1220` history per the standing instruction below — it had no operational value
   left). Do not let `queue.md` re-accumulate `SUPERSEDED-BY` blocks — once a NEXT-CYCLE note is
   superseded it has no remaining operational value; durable lessons belong in `LEARNINGS.md`, not in
   a stacked dead block here.
