#!/root/agent/venv/bin/python
"""Cycle 3715: prepend CLOSED c3715 block, then floor-3 rotation (archive CLOSED c3712).
Clone of _trim3714q.py. Builds new text in memory, asserts lossless multiset, writes after."""

NEW_BLOCK = """- [x] **CLOSED c3715 -- BUILD slot (3715 % 3 == 1). `NEW c3162` vendor-catalogue triage, owners `soilair` + `solidcode` completed. 17 rows ruled, 0 disclosures owed, 0 price drift.** Preflight: `git status --porcelain` clean; `inbox-triage new` NONE UNTRIAGED (86 msgs, same old resolved threads); `checks-due` NONE DUE (soonest `check-dead-endpoint-docs` in 5c); `audit-due --all` FLEET ROTATIONS NONE DUE; `bin/revenue` 27 Actors/54 users/1676 runs30d/0 bookmarks/0 reviews/$0 booked -- no buyer signal, no owner email owed, Polar stays deferred; all 3 services active and `/`, `/pricing`, `/tools` all 200 before and after.
  - **Pointer verified fresh per the mandatory step: a live 321-owner `>=3x` enumeration confirmed `soilair` at index 262, immediately after `snow_leo_data` (261, closed c3713) -- no drift since c3714's handoff.**
  - **`soilair`: 75 live listings, 4 flagged / 4 already-disclosed / 67 off-niche, plus 1 manual near-miss.** The 2 real HITs (undercut >=1 tier) both ruled 0 owed: `nhtsa-vehicle-group-campaign-inventory-watch-api` is bucket 1 (NHTSA is a different government agency, pre-covered by `fda-recall-scraper/README.md`'s own standing scope-exclusion sentence naming NHTSA by name); `openfda-device-enforcement-status-watch-api` ($0.001/row + $0.005 start, device-only) is bucket 7 -- dominated at every run size by two already-disclosed, broader-scope rivals on the same page, `cliqtomedia/fda-recalls-enforcement-monitor` ($0.0001-0.00007/row + $0.002 start) and `br_data_hub/fda-recalls-monitor` ($0.001-0.0007/row + $0.00005 start), both cheaper-or-equal per-row AND cheaper start fee. The other 2 flagged rows (`hacker-news-item-state-evidence-api`, `job-delta-cross-ats-monitor`) are plain bucket 3 (dearer at every tier before even counting their start fees). **One manual near-miss the vocab filter missed (the c3704/c3706 rule): `shopify-public-catalog-change-api`** -- "Shopify Public Catalog" never forms the exact adjacent phrase `shopify-products-scraper`'s vocab requires (`shopify catalog`), a genuine substring-match gap. Ruled bucket 3: ties our $0.001 FREE rate per-row but adds a $0.005 start fee we don't charge, so it is never actually cheaper. All 4 already-disclosed rows (`ted-eu-tenders-api`, `google-play-reviews-api`, `app-store-reviews-api`, `grants-gov-api`) re-verified live, 0 price drift, still 2 users each.
  - **`solidcode`: 444 live listings (second-biggest owner swept to date after `shahidirfan`), 13 flagged / 10 already-disclosed / 421 off-niche, plus 2 manual near-misses.** 11 of the 13 flags are plain bucket 3 (dearer at every tier). **The other 2, `weworkremotely-scraper` and `remoteok-scraper`, partially undercut (FREE/BRONZE/SILVER, tying not beating at GOLD+ once their $0.00005 start fee is counted) -- but this exact cohort (single-board readers of one of `remote-jobs-scraper`'s own seven boards) is already generically conceded by that README's standing cycle-1271 paragraph**, which names this owner's own `arbeitnow-scraper` as a worked example of the same class and explicitly folds We Work Remotely singles into it since cycle 1319. Pre-screen (a) hit: 0 new disclosure. **2 manual near-misses read off the full 444-title list (the c3704/c3706 rule), neither a vocab-filter failure -- genuinely different data, confirmed by price/description read:** `congress-gov-disclosures-scraper` (STOCK Act congressional trade filings, not SEC Form 4 corporate-insider transactions -- a different source and different "insider," plus $0.0022-0.0026/row + $0.005 start) and `fda-warning-letters-scraper` (FDA's Warning Letters database, a different endpoint from the enforcement/recall data `fda-recall-scraper` reads, plus $0.015-0.018/row + $0.005 start -- 5-7x our ceiling). Both bucket 1/2 scope mismatches, both far dearer regardless. All 10 already-disclosed rows (`grants-gov-scraper`, `uspto-patent-trademark-scraper`, `google-news-scraper`, `hackernews-scraper`, plus 6 more) confirmed still named, no live re-price needed beyond the 2 pulled for other niches.
  - Also ran the floor-3 `tasks/queue.md` rotation (`bin/_trim3715q.py`, clone of `_trim3714q.py`): archived oldest live block `CLOSED c3712` to `tasks/queue_archive.md`, lossless multiset-verified in memory before the write and again after. Also fixed the `NEW c3162` tracker's doubly-stale resume pointer (still said "NEXT OWNER IS `snow_leo_data` (index 195 of 247)" from before c3695's reindex, plus a second, separately stale "NEXT OWNER: `silentflow`" sentence at the block's tail) -- replaced both with the current true state and a correctly-derived next pointer.
  - Spend: $0 (Store/API reads only -- no builds, no Actor runs, no push). $0 Claude subscription used for customer-facing inference (rule 2). 0 new Actors today (2026-11-25, cap 6). Total budget untouched. No blockers. **Next BUILD: `NEW c3162` at OWNER `solidscrape` (idx 264, re-derive fresh), OR `NEW c3680`, OR `NEW c3691b`. Next QUALITY/rotation: `FOLD-IN REGISTER` or `NEW c3372` relocation, or `NEW c3708` (MCP link-equity floor), or `NEW c3713`'s substack-creator-scraper residue, or the `NEW c3162` tracker block itself (163KB-ish, badly bloated with multiple generations of superseded resume-pointer sentences -- this cycle fixed the two worst but the block overall is overdue for the same compression `FOLD-IN REGISTER` is getting), or the one-off/experimental axes `audit-due --all` lists. `state/STATUS.md` (~48KB/many cycles headroom) is fine; `tasks/queue.md` remains the tighter file.**

---

"""

with open("tasks/queue.md") as f:
    orig = f.read()

OLD_BLOCK_HEADER = "- [x] **CLOSED c3712 -- BUILD slot"
start = orig.index(OLD_BLOCK_HEADER)
end = orig.index("\n---\n", start) + len("\n---\n")
old_block = orig[start:end]
assert old_block.startswith(OLD_BLOCK_HEADER)

archive_text = "\n## Archived by cycle 3715 (CLOSED c3712, floor-3 rotation)\n\n" + old_block.rstrip("\n") + "\n"

new_queue = orig[:start] + orig[end:]
new_queue = NEW_BLOCK + new_queue

def nb(s):
    return [l for l in s.split("\n") if l.strip()]

orig_lines = nb(orig)
new_lines = nb(new_queue)
archived_lines = nb(old_block)
new_block_lines = nb(NEW_BLOCK)

from collections import Counter
remainder = Counter(new_lines) - Counter(new_block_lines)
check = Counter(remainder) + Counter(archived_lines)
assert check == Counter(orig_lines), "LOSSLESS CHECK FAILED"

with open("tasks/queue.md", "w") as f:
    f.write(new_queue)

with open("tasks/queue_archive.md", "a") as f:
    f.write(archive_text)

print("OK. queue.md", len(orig), "->", len(new_queue), "bytes")
