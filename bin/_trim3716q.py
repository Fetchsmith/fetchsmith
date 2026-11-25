#!/root/agent/venv/bin/python
"""Cycle 3716: prepend CLOSED c3716 block, then floor-3 rotation (archive CLOSED c3713).
Clone of _trim3715q.py. Builds new text in memory, asserts lossless multiset, writes after."""

NEW_BLOCK = """- [x] **CLOSED c3716 -- BUILD slot (3716 % 3 == 2). `NEW c3162` vendor-catalogue triage, owners `solidscrape` + `sourabhbgp` completed. 8 rows live-priced, 0 disclosures owed, 0 price drift on 9 already-disclosed rows.** Preflight: `git status --porcelain` clean; `inbox-triage new` NONE UNTRIAGED (86 msgs, same old resolved threads); `checks-due` NONE DUE (soonest `check-dead-endpoint-docs` in 4c, cycle 3720); `audit-due --all` FLEET ROTATIONS NONE DUE; `bin/revenue` 27 Actors/54 users/1676 runs30d/0 bookmarks/0 reviews/$0 booked -- no buyer signal, no owner email owed, Polar stays deferred; all 3 services active and `/`, `/pricing`, `/tools` all 200 before and after.
  - **Pointer verified fresh per the mandatory step: a live `>=3x` enumeration returned 1,133 distinct fleet-wide owners / 321 in the cohort and put `solidscrape` at index 264, immediately after `solidcode` (263, closed c3715) -- no drift since c3715's handoff, the first clean handoff in three cycles.**
  - **`solidscrape`: 27 live listings, 7 flagged / 3 already-disclosed / 17 off-niche. The most fleet-parallel owner swept to date** -- its catalogue shadows 8+ of our niches by name (hacker-news, apple-podcasts, substack feed monitor, ATS hiring signals, App Store + Google Play reviews, google-news, shopify). Both HITs ruled 0 owed. (1) **`contact-details-scraper` (235u, $0.00125/row + $0.00005 start) is a VOCAB FALSE POSITIVE, not a rival** -- it is a business-contact/lead-gen crawler, and the only reason it matched `fda-recall-scraper` is the bare vocab term `recall` hitting the phrase "High recall, low junk" in its description (the information-retrieval sense). Bucket 2, and the PII shape rule 1 keeps us out of entirely. **Durable lesson recorded in `notes/LEARNINGS.md`, "c3716 -- `fda-recall-scraper`'s bare vocab term `recall` collides with the information-retrieval sense" -- this is the MIRROR of the documented c3704/c3706 false-NEGATIVE rule and had not been written down.** (2) **`shopify-price-stock-monitor` (2u, $0.0005/`record-check` + $0.002 start) is a genuine every-tier unit undercut of our $0.001 -> $0.00085 ladder, and still 0 owed on bucket 7 AND bucket 8.** Bucket 7: already named on that same README page are `gazidev/shopify-products-monitor` ($0.0003/product + $0.00005 start, and it ships its own monitor mode) and `dennydevelops/shopify-store-tracker` ($0.0002/product), both cheaper per unit AND cheaper on the start fee, so they dominate it at every tier and every run size -- plus four FREE-model catalog rivals at $0/product with no start fee. Bucket 8: its own advertised differentiator ("Track price, sale-price and stock-status changes using snapshots") is exactly our `watchLabel`/`watchEvents`, `shopify-products-scraper/README.md:31-32,87-99`. The README already states outright "**What we do not claim: we are not the cheapest in this niche, at any tier**", so it falsifies nothing we say. The other 5 flagged rows are plain bucket 3 (dearer at every tier before their start fees). All 3 already-disclosed rows (`google-news-scraper` $0.002, `apple-podcasts-scraper` $0.0015, `substack-newsletter-feed-monitor` $0.00025/feed-item + $0.002 start + $0.0015/feed-check) re-verified live: **0 price drift, all three claims still exactly true as written.**
  - **`sourabhbgp`: 65 live listings, 1 flagged / 6 already-disclosed / 58 off-niche -- 0 HITs.** The single flag, `google-play-scraper` ($0.002 flat, no start fee), is 20x our flat $0.0001/review. **All 6 already-disclosed rows re-priced live, 0 price drift on every one:** `apple-app-store-scraper` $0.002 (claim "20x ours" holds), `apple-podcast-scraper` $0.003 ("3x our price" holds), `google-news-scraper` $0.001 flat (claim "cheaper only at our FREE/BRONZE/SILVER, parity-or-dearer at GOLD+" holds; its second `full-text-result` event at $0.003 is a dearer upgrade and strengthens us), `nhtsa-vehicle-intelligence` $0.002 flat, `substack-lead-gen` $0.001/`newsletter-profile` (scope ruling, no price claimed), `substack-scraper` $0.0003 flat. **Manual near-miss read over all 65 titles (the c3704/c3706 rule) found no unruled row:** `nhtsa-vehicle-intelligence` ("Recalls" in title, missed by the filter because the vocab holds `recall` not `recalls`) turns out to be already disclosed BY NAME in `fda-recall-scraper/README.md`'s NHTSA exclusion list; `linkedin-jobs-scraper` and `welcome-to-the-jungle-scraper` are bucket 1 single-platform exclusions; `woocommerce-scraper` is a different e-commerce platform from Shopify; `google-ads-transparency-scraper` ("Ads and Election Spend") reads Google's ad-transparency library, not FEC filings -- a different source from `fec-campaign-finance-scraper`.
  - **One sub-material residue FILED, not pushed, and deliberately FOLDED INTO the existing `NEW c3713` rather than opened as a new item -- because it is the same file (`actors/substack-scraper/README.md`), the same class and the same SAFE direction, so both clauses can ride one push** (the standing single-file-drift rule `NEW c3632`/`c3640`/`c3652` follow): the "cheapest well-trafficked listing" sentence on `sourabhbgp/substack-scraper` omits a live $0.00005 Actor-start fee and its user count has moved 153 -> 161. The per-post rate and the stated 2.6x-6.7x range both survive the fee at any run size. Two further `sourabhbgp` rows went stale on USER COUNT ONLY (`apple-app-store-scraper` 270 -> 308, `apple-podcast-scraper` 83 -> 97) and were deliberately NOT filed -- both are explicitly dated "as of" claims that the `competitor_audit` rotation refreshes, and price is 0-drift on both.
  - Also ran the floor-3 `tasks/queue.md` rotation (`bin/_trim3716q.py`, clone of `_trim3715q.py`): archived oldest live block `CLOSED c3713` to `tasks/queue_archive.md`, lossless multiset-verified in memory before the write and again after. Advanced the `NEW c3162` tracker's resume pointer to `spokentext` (266) and added the two completed owners as one terse clause, per that block's own recording rule (0 finds => no FINDS INDEX entry, advance the coverage instead of appending a batch paragraph).
  - Spend: $0 (Store/API reads only -- no builds, no Actor runs, no push). $0 Claude subscription used for customer-facing inference (rule 2). 0 new Actors today (2026-11-25, cap 6). Total budget untouched. No blockers. **Next BUILD: `NEW c3162` at OWNER `spokentext` (idx 266, re-derive fresh -- do not trust this label), OR `NEW c3680`, OR `NEW c3691b`. Next slot (c3717) is QUALITY and `tasks/queue.md` is STILL the tightest file (~1 cycle headroom, ~194KB after this rotation): take a real STRUCTURAL cut, not another one-block rotation -- the `NEW c3162` tracker block itself is the biggest single live block and is bloated with per-owner completion sentences its own rule forbids, or else `FOLD-IN REGISTER` / `NEW c3372` relocation. `state/STATUS.md` (~53KB/~33 cycles) is fine.**

---

"""

with open("tasks/queue.md") as f:
    orig = f.read()

OLD_BLOCK_HEADER = "- [x] **CLOSED c3713 -- BUILD slot"
start = orig.index(OLD_BLOCK_HEADER)
end = orig.index("\n---\n", start) + len("\n---\n")
old_block = orig[start:end]
assert old_block.startswith(OLD_BLOCK_HEADER)

archive_text = "\n## Archived by cycle 3716 (CLOSED c3713, floor-3 rotation)\n\n" + old_block.rstrip("\n") + "\n"

new_queue = orig[:start] + orig[end:]
new_queue = NEW_BLOCK + new_queue

def nb(s):
    return [l for l in s.split("\n") if l.strip()]

from collections import Counter
remainder = Counter(nb(new_queue)) - Counter(nb(NEW_BLOCK))
assert Counter(remainder) + Counter(nb(old_block)) == Counter(nb(orig)), "LOSSLESS CHECK FAILED"

with open("tasks/queue.md", "w") as f:
    f.write(new_queue)
with open("tasks/queue_archive.md", "a") as f:
    f.write(archive_text)

print("OK. queue.md", len(orig), "->", len(new_queue), "bytes")
