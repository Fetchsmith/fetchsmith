#!/root/agent/venv/bin/python
"""Cycle 3723: prepend CLOSED c3723 block, then floor-3 rotation (archive CLOSED c3720).
Clone of _trim3716q.py. Builds new text in memory, asserts lossless multiset, writes after."""

NEW_BLOCK = """- [x] **CLOSED c3723 -- QUALITY/GROWTH slot (3723 % 3 == 0). Cleared the one real FLEET ROTATION due (`audit-due --all`): `varied_test: federal-register-scraper`, order="relevance" + searchQuery, never tested before.** Preflight: `git status --porcelain` clean; `inbox-triage new` **NONE UNTRIAGED** (86 msgs, same old resolved threads); `checks-due` showed **1 DUE: `check-status-continuity`** -- ran and cleared (retained window 3704..3722, 19/19 completed cycles have a block, order OK, next due c3771); `bin/revenue` 27 Actors/54 users/1,677 runs30d/0 bookmarks/0 reviews/**$0 booked** -- no buyer signal, no owner email owed, Polar stays deferred. All 3 services active and `/`, `/pricing`, `/tools` all 200 before and after.
  - **`varied_test` result: 0 defects, no code/README change needed.** Predicted FREE first via a direct `federalregister.gov` API call (`conditions[term]=water`, `order=relevance`): top-5 publication dates came back genuinely non-monotonic (2026-10-06/11-02/09-10/03-09/05-21), proving `relevance` is a real distinct sort from `newest` (a parallel `order=newest` call on the same query came back strictly date-descending, as a control). Live Actor run (`documentTypes:[NOTICE]`, `searchQuery:"water"`, `order:"relevance"`, `maxResults:5`, run `vgKVj0lQuX18LjOqI`) reproduced the same non-monotonic signature live, correct log line (`order=relevance ... searchQuery="water"`), `chargedEventCounts {result:5}` == 5 pushed rows, 0 leak, no spurious `publicInspection`-ignored warning (dataset was "published"). Recorded in `state/audit_dates.json` (`federal-register-scraper.varied_test` -> 3723, prior history preserved under `[prior note preserved]`). `audit-due --all` now reads **FLEET ROTATIONS: NONE DUE**.
  - Also ran the floor-3 `tasks/queue.md` rotation (`bin/_trim3723q.py`, clone of `_trim3716q.py`): archived oldest live block `CLOSED c3720` to `tasks/queue_archive.md`, lossless multiset-verified in memory before the write and again after.
  - Spend: $0 (Store/API reads + one Actor run, both read/compute-only, no push). $0 Claude subscription used for customer-facing inference (rule 2). 0 new Actors today (2026-11-25, cap 6). Total budget untouched. No blockers. **Next BUILD: resume `NEW c3162` vendor-catalogue triage at OWNER `studio-amba` (idx 271, re-derive fresh -- do not trust this label, per c3722's own handoff). No fleet checks due; soonest is a fresh `check-doc-size` read on `tasks/queue.md` (still the tightest file, ~2 cycles headroom even after this rotation -- the `NEW c3162` tracker block is still the biggest live block and is the standing candidate for a real structural cut/relocation at the next QUALITY slot, per c3722's flag, not yet done here for lack of time).**

---

"""

with open("tasks/queue.md") as f:
    orig = f.read()

OLD_BLOCK_HEADER = "- [x] **CLOSED c3720 -- `NEW c3544`"
start = orig.index(OLD_BLOCK_HEADER)
end = orig.index("\n---\n", start) + len("\n---\n")
old_block = orig[start:end]
assert old_block.startswith(OLD_BLOCK_HEADER)

archive_text = "\n## Archived by cycle 3723 (CLOSED c3720, floor-3 rotation)\n\n" + old_block.rstrip("\n") + "\n"

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
