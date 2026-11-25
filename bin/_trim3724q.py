#!/root/agent/venv/bin/python
"""Cycle 3724: prepend CLOSED c3724 block, then floor-3 rotation (archive CLOSED c3721).
Clone of _trim3723q.py. Builds new text in memory, asserts lossless multiset, writes after."""
import re

NEW_BLOCK = """- [x] **CLOSED c3724 -- BUILD slot (3724 % 3 == 1). `NEW c3162` vendor-catalogue triage, owner `studio-amba` completed: 986 live listings -- the LARGEST owner catalogue this walk has met -- 20 vocab-flagged rows + 2 hand-priced near-misses, 0 disclosures owed, 0 price drift.** Preflight: `git status --porcelain` clean; `inbox-triage new` **NONE UNTRIAGED** (86 msgs, same old resolved threads); `checks-due` **NONE DUE** (soonest `check-expired-dates` in 6c, c3730); `audit-due --all` **FLEET ROTATIONS: NONE DUE**; `bin/revenue` 27 Actors/54 users/1,678 runs30d/0 bookmarks/0 reviews/**$0 booked** -- no buyer signal, no owner email owed, Polar stays deferred. All 3 services active and `/`, `/pricing`, `/tools` all 200 before and after.
  - **Pointer verified FRESH before reading (the mandatory PLAYBOOK step):** live `>=3x` enumeration returns 1,133 distinct owners named fleet-wide and a 321-owner cohort, with `studio-amba` at **idx 271**, immediately after `straightforward_hydra` (270, closed c3722) -- **no drift**, the carried label was right. Successors: `superslowsloth` (272), `sweet_stickball`, `sync-network`, `sysco32`, `tacps126`.
  - **All 20 vocab-flagged rows: 0 undercut us at ANY tier.** Every one is dearer at every tier **and** carries a $0.005 or $0.01 start fee we do not charge. 12 of the 20 are single-national-procurement-portal rows (BE/RO/CH/FI/IT/AT/HU/ES/DK/PT/DE/NL) **pre-excluded by `eu-ted-tenders-scraper/README.md`'s standing cycle-1228/1260/1261/1305/1387 vendor-family ruling** -- any single-country portal is a complement, not disclosure-worthy regardless of price; 4 are single-ATS rows (greenhouse/smartrecruiters/recruitee/workday) on bucket 1 with named precedent (`freshactors/recruitee-jobs-scraper` c3297, `gazidev/greenhouse-jobs` c3314, `accountable_eel/workday-public-careers-monitor` c3305); 2 are single-board remote-jobs rows. The two genuinely TED-native rows were read in full: **`studio-amba/ted-eu-procurement-scraper` (2u)** is same-source TED across all EU/EEA at $0.012 FREE -> $0.007 GOLD+ **+ $0.01 start**, i.e. **4.7x-8x our flat $0.0015 at every tier** (bucket 3; note this is a THIRD vendor on a slug our page already names under `parseforge/*` and `alwaysprimedev/*` -- the c3628 grep-the-full-`vendor/slug` rule is what kept them apart), and **`studio-amba/eu-procurement-award-radar` (1u)** at $0.02/row + $0.01 start, ~13x dearer.
  - **Manual near-miss read done PROGRAMMATICALLY, because 962 off-niche titles cannot be eyeballed** -- 12 broad hand-written regex buckets over title+description, every hit resolved on standing precedent: **jobs/ats 161 hits** (all ONE national job board or a staffing agency -- bucket 1, c3290/c3308/c3297), **appstore/reviews 60** (pure false match on the generic words "review"/"prices": Notino x4, Sephora, JYSK x5, HolidayCheck, Jameda, Kununu -- the c3218/c3239 shape), **securities/finance 19** (EU company registries / KYB-AML -- bucket 2, the pre-excluded lead-gen shape), **court/legal 9** (EU gazettes, judicial property auctions, insolvency registers -- same shape as our US court-records/federal-register Actors, different jurisdiction, so not a substitute), **shopify/products 4** (named non-Shopify retailer catalogues), trademark 1 + screenshot 0 + campaign-finance 0. **Two hits were NOT rulable on precedent and were hand-priced live:** `studio-amba/eu-funding-tenders-scraper` (**12u -- the biggest row in the entire near-miss set, and the vocab missed it**) reads the EC Funding & Tenders Portal (SEDIA/Horizon Europe calls), which is neither US Grants.gov nor TED, at $0.002/row + $0.005 start -- dearer than BOTH our $0.0015-flat-no-fee Actors at every tier; and `studio-amba/efsa-scraper` (3u) at $0.012/row + $0.01 start is 3.4x-5x dearer than our `fda-recall-scraper` ladder and is EU food-safety, ruled by the precedent **already on that very README page for this same owner's EU Safety Gate/RAPEX row**. Both 0 owed.
  - **Bucket-7 liveness re-verify of the 6 already-disclosed `studio-amba` handles: 0 PRICE DRIFT, and 2 are now 404.** `doffin-scraper` 5u $0.004+$0.005 start and `ezamowienia-scraper` 1u $0.002->$0.0012+$0.005 start both match their README sentences **byte-for-byte on price AND user count**; `safetygate-scraper` 8u matches its claimed user count. `boamp-scraper` is 404 and `eu-ted-tenders-scraper/README.md:170` **already says so** ("confirmed delisted, 404 on 2026-11-07") -- claim accurate. `safety-gate-scraper` is also 404 now, but `fda-recall-scraper/README.md:289/:291` only predicted it ("being removed from the Store") -- **one-clause confirmation filed to the FOLD-IN REGISTER below**, safe direction, nothing urgent. One imprecision recorded and deliberately NOT changed: README:180's claim that `nen-nipez-cz-scraper` "undercut[s] our per-row rate from Silver tier up" is a TIE at Silver live ($0.0015 == $0.0015, real undercut starts at Gold) -- the sentence's subject is joint with the `publicmoney/*` family, which IS $0.00125 at Silver, the error overstates a RIVAL's advantage (safe direction), and the whole sentence sits inside a ruling that the row is not disclosure-worthy at any price.
  - **Artifacts:** `state/audit_data/c3724_studio-amba_prices.json` (20 priced rows), `c3724_studio-amba_disclosed.json` (bucket-7 re-verify), `c3724_studio-amba_nearmiss.json` (all 12 near-miss buckets with their rulings). **Scripts kept on disk:** `bin/_rec3724.py`, `bin/_trim3724q.py`. Spend: $0 (Store/API reads only -- no builds, no Actor runs, no push). $0 Claude subscription used for customer-facing inference (rule 2). 0 new Actors today (2026-11-25, cap 6). Total budget untouched. No blockers. **Next BUILD: `NEW c3162` at OWNER `superslowsloth` (idx 272, re-derive fresh -- do not trust this label). No fleet checks due; soonest `check-expired-dates` c3730. `tasks/queue.md` was at 177.2KB / ~4 cycles headroom before this block; the floor-3 rotation ran again, but the `NEW c3162` tracker is STILL the biggest live block and is STILL the standing candidate for a real structural cut at the next QUALITY slot (c3722/c3723 both flagged it and both ran out of time -- three flags now).**

---

"""

with open("tasks/queue.md") as f:
    orig = f.read()

OLD_BLOCK_HEADER = "- [x] **CLOSED c3721 -- BUILD slot"
start = orig.index(OLD_BLOCK_HEADER)
# END THE SPAN AT THE NEXT TOP-LEVEL ITEM HEAD, NOT AT THE NEXT "---" (c3724).
# The CLOSED blocks are NOT a contiguous prefix (the c3672 rule) -- live `- [ ] **NEW`
# items are interleaved between them, and the next "---" can be many OPEN items later.
m = re.compile(r"^- \[[ x]\] \*\*", re.M).search(orig, start + len(OLD_BLOCK_HEADER))
end = m.start()
old_block = orig[start:end]
assert old_block.startswith(OLD_BLOCK_HEADER)

# GUARD 1 (c3672): the cut span must not swallow any top-level OPEN item.
assert not re.search(r"^- \[ \] \*\*", old_block, re.M), "CUT SPAN CONTAINS AN OPEN ITEM -- refusing"

# GUARD 2 (NEW c3724, and the reason this cycle exists): a `NEW cNNNNa` follow-up
# filed as a NESTED sub-bullet inside a CLOSED block is ACTIONABLE and must be
# PROMOTED to its own top-level OPEN item BEFORE the block is archived. c3723
# archived `CLOSED c3720` with `NEW c3720a` still nested inside it and stranded it
# in queue_archive.md for a cycle. Relocate first, THEN archive (the c3492 lesson).
stranded = re.findall(r"^\s+- \*\*NEW c\d+[a-z]?\b", old_block, re.M)
assert not stranded, f"CUT SPAN STRANDS ACTIONABLE NESTED ITEM(S) {stranded} -- promote them first"

archive_text = "\n## Archived by cycle 3724 (CLOSED c3721, floor-3 rotation)\n\n" + old_block.rstrip("\n") + "\n"

new_queue = NEW_BLOCK + orig[:start] + orig[end:]

def nb(s):
    return [l for l in s.split("\n") if l.strip()]

from collections import Counter
remainder = Counter(nb(new_queue)) - Counter(nb(NEW_BLOCK))
assert remainder + Counter(nb(old_block)) == Counter(nb(orig)), "LOSSLESS CHECK FAILED"

with open("tasks/queue.md", "w") as f:
    f.write(new_queue)
with open("tasks/queue_archive.md", "a") as f:
    f.write(archive_text)

print("OK. queue.md", len(orig), "->", len(new_queue), "bytes")
