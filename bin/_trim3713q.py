#!/root/agent/venv/bin/python
"""Cycle 3713: prepend CLOSED c3713 block, then floor-3 rotation (archive CLOSED c3710).
Clone of _trim3712q.py. Builds new text in memory, asserts lossless multiset, writes after."""
import re

NEW_BLOCK = """- [x] **CLOSED c3713 -- BUILD slot (3713 % 3 == 2). `NEW c3162` vendor-catalogue triage, owners `sleek_waveform` + `snow_leo_data` completed. 4 rows ruled, 0 disclosures owed, 0 price drift.** Preflight: `git status --porcelain` clean (after `bin/revenue` state refresh only); `inbox-triage new` NONE UNTRIAGED (86 msgs, re-confirmed the Apify-token-rotation and buyer-signal owner threads are old resolved history); `bin/revenue` 27 Actors/54 users/1676 runs30d/0 bookmarks/0 reviews/$0 booked -- no buyer signal, no owner email owed, Polar stays deferred; all 3 services active and `/`, `/pricing`, `/tools` all 200 before and after.
  - **Pointer CAUGHT STALE before it cost a skipped owner, exactly the hazard the mandatory pointer-verify step exists for.** c3712's handoff named `snow_leo_data (index 195 of 247)` as next, but a fresh `>=3x` owner enumeration this cycle found **321** owners (not 247 -- the cohort grows as new disclosures push more owners past `MIN_NAMED`), with `snow_leo_data` now at index 261. Printing indices 257-263 fresh showed `skootle` (259, the actual last-done) immediately followed by **`sleek_waveform` at 260 -- an owner never swept**, then `snow_leo_data` at 261. Swept both rather than trusting the forwarded label.
  - **`sleek_waveform` -- 10 live listings, 0 flagged / 3 already-disclosed / 7 off-niche, 0 disclosures owed.** All 7 off-niche titles manually read (threads/YouTube-trends/contractor-leads/B2B-leads/SaaS-competitor-intel/Zillow/LLM-markdown) -- none matches any of our 27 niches, correctly off-niche, no near-misses. 3 already-disclosed rows re-verified live with 0 price drift: `substack-creator-scraper` (substack-scraper README:217, flat $0.002/post, matches), `federal-contract-scraper-usaspendinggov` (us-federal-awards-scraper README:225, flat $0.001+$0.00005 start, matches), `universal-shopify-scraper` (shopify-products-scraper README:128, $0.0005/product+$0.00005 start, matches).
  - **One sub-material residue on `substack-creator-scraper`, filed not pushed (same materiality bar as c3712's `silentflow` +1-user residue): live has a $0.00005 Actor-start fee the README's parity sentence never mentions, and live user count is 25 against the README's stated 24 (+1).** Both are the SAFE direction (omitting their start fee means the true picture is that they are strictly dearer than us even on Free, not merely tied -- understates our own advantage, same class as `NEW c3632`/`c3640`/`c3652`). Fold into the next edit of that `substack-scraper/README.md:217` paragraph rather than spending a push on it alone; filed as `NEW c3713`.
  - **`snow_leo_data` -- 49 live listings, 4 flagged / 4 already-disclosed / 41 off-niche, plus 3 manual near-misses, 0 disclosures owed.** All 4 sweep flags ruled bucket-3 (dearer at every tier): `ats-jobs-scraper` (4u, FREE $0.0028/GOLD $0.00091 vs our FREE $0.001/GOLD $0.0007, plus a $0.00005 start fee we don't charge), `google-play-scraper` (2u, flat $0.0003 vs our flat $0.0001, 3x dearer), `the-muse-jobs-scraper` (2u, FREE $0.0022/GOLD $0.00121 vs our FREE $0.0015/GOLD $0.001, plus start fee), `google-news-scraper` (1u, FREE $0.0029/GOLD $0.0016 vs our FREE $0.002/GOLD $0.001).
  - **3 manual near-misses, all bucket-1 scope exclusion on standing precedent, vocabulary filter correctly missed all three (title-list rule again earns its keep):** `linkedin-jobs-scraper` (6u) -- LinkedIn is explicitly not one of `remote-jobs-scraper`'s seven boards, same ruling already applied to `silentflow`/`k1ra`/`blueskyscraper`'s LinkedIn listings on that README (line 215/239); `seek-scraper` (6u, SEEK+JobStreet Malaysia/Singapore+JobsDB Hong Kong) -- single-region job boards outside our seven, same class as the already-named Pracuj.pl/NoFluffJobs/WTTJ single-country exclusions; `sec-edgar-scraper` (2u, "EDGAR Full Text Search, XBRL, 10-K, 8-K") -- `sec-insider-trades-scraper/README.md:16` already excludes plain filing-index EDGAR Actors by name ("Most EDGAR Actors hand you an index of 10-K/10-Q/8-K...") as a different shape from our parsed Form-4 transactions, same ruling c3712 gave `silentflow/sec-edgar-filings`. `jobs-ch-scraper` (1u, Swiss) and `instahyre-scraper` (1u, India-only) are the same single-country class, below the naming threshold, not individually argued. `linkedin-profile-scraper` (6u) and `website-contact-scraper`/`sanctions-screening-api` correctly off-niche -- no profile-finder or sanctions-screening niche in this fleet.
  - **4 already-disclosed rows re-verified live with 0 price drift:** `shopify-inventory-scraper` (shopify-products-scraper README:156, tiered $0.0012->$0.00084+start, matches), `government-tenders-scraper` (eu-ted-tenders README:190 + sam-gov README:285, $0.0016-$0.0029, matches), `app-store-scraper` (app-store-reviews README:261, flat $0.0003 post-forecast, matches), `product-recalls-scraper` (fda-recall-scraper README:275, flat $0.00075, matches).
  - Artifacts: `state/audit_data/c3713_sleek_waveform_prices.json`, `c3713_snow_leo_data_prices.json`. Script `bin/_rec3713.py` kept on disk (argv-driven clone of `_rec3712.py`, no changes needed).
  - Also ran the floor-3 `tasks/queue.md` rotation (`bin/_trim3713q.py`, clone of `_trim3712q.py`): archived oldest live block `CLOSED c3710` to `tasks/queue_archive.md`, lossless multiset-verified in memory before the write and again after.
  - Spend: $0 (Store/API reads only -- no builds, no Actor runs, no push). $0 Claude subscription used for customer-facing inference (rule 2). 0 new Actors today (2026-11-25, cap 6). Total budget untouched. No blockers. **Next BUILD: `NEW c3162` at OWNER `soilair` (idx 262, re-derive fresh -- do not trust this label, re-print the array), OR `NEW c3680`, OR `NEW c3691b`. Next QUALITY/rotation: `FOLD-IN REGISTER` or `NEW c3372` relocation, or `NEW c3708` (MCP link-equity floor), or `NEW c3713`'s substack-creator-scraper residue, or the one-off/experimental axes `audit-due --all` lists. Both `state/STATUS.md` (~192KB) and `tasks/queue.md` remain TRIM DUE on the 24-cycle projection -- flag for the next QUALITY slot.**

---

"""

with open("tasks/queue.md") as f:
    orig = f.read()

OLD_BLOCK_HEADER = "- [x] **CLOSED c3710 -- BUILD slot"
start = orig.index(OLD_BLOCK_HEADER)
end = orig.index("\n---\n", start) + len("\n---\n")
old_block = orig[start:end]
assert old_block.startswith(OLD_BLOCK_HEADER)

archive_text = "\n## Archived by cycle 3713 (CLOSED c3710, floor-3 rotation)\n\n" + old_block.rstrip("\n") + "\n"

new_queue = orig[:start] + orig[end:]
new_queue = NEW_BLOCK + new_queue

def nb(s):
    return [l for l in s.split("\n") if l.strip()]

orig_lines = nb(orig)
new_lines = nb(new_queue)
archived_lines = nb(old_block)
new_block_lines = nb(NEW_BLOCK)

# orig = (new_queue minus new_block_lines) plus archived_lines, as multisets
from collections import Counter
remainder = Counter(new_lines) - Counter(new_block_lines)
check = Counter(remainder) + Counter(archived_lines)
assert check == Counter(orig_lines), "LOSSLESS CHECK FAILED"

with open("tasks/queue.md", "w") as f:
    f.write(new_queue)

with open("tasks/queue_archive.md", "a") as f:
    f.write(archive_text)

print("OK. queue.md", len(orig), "->", len(new_queue), "bytes")
