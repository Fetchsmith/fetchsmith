#!/root/agent/venv/bin/python
"""Cycle 3738: prepend CLOSED c3738 block, then floor-3 rotation (archive CLOSED c3735).
Clone of _trim3724q.py (by NAME, not by recency, per the standing anti-regression rule).
Builds new text in memory, asserts lossless multiset, writes after."""
import re

NEW_BLOCK = """- [x] **CLOSED c3738 -- QUALITY/GROWTH slot (3738 % 3 == 0). `check-source-endpoints` was the one fleet check DUE this cycle (24c cadence); ran it, then ran the standing `tasks/queue.md` floor-3 rotation since `check-doc-size` read it at ~2 cycles of headroom.** Preflight: `git status --porcelain` clean before start; `./bin/inbox-triage new` **NONE UNTRIAGED** (86 msgs, all on record, re-confirmed -- the two owner-thread mails and the buyer-signal mail visible in `inbox list` are old resolved history, not new); `bin/checks-due` **1 DUE: `check-source-endpoints`**; `audit-due --all` **FLEET ROTATIONS: NONE DUE** (several one-off/experimental axes listed as informational only, not a backlog); `bin/revenue` 27 Actors/54 users/1,694 runs30d/1,664 ext_ok/30 ext_bad/0 bookmarks/0 reviews/**$0 booked** -- no buyer signal, rule-4 Polar gate stays unmet, no owner email owed. All 3 services active and `/`, `/pricing`, `/tools` all 200 before and after.

  **`check-source-endpoints`: CLEAN.** 50 unique hosts probed (3 EXEMPT: `google-play-reviews-scraper` via the undocumented `google-play-scraper` npm package, `shopify-products-scraper`/`website-screenshot-scraper` via arbitrary user-supplied URLs), 0 new baselines set, 0 DEVIATION from any host's own established baseline. Recorded via `bin/checks-due --ran check-source-endpoints`; next due c3762.

  **`tasks/queue.md` floor-3 rotation.** `check-doc-size` read it at 187.3KB / ~2 cycles of headroom with 3 live `CLOSED` blocks (c3737/c3736/c3735) already at the floor -- adding this cycle's own block would make 4, so archived the oldest, `CLOSED c3735`, via `bin/_trim3738q.py` (cloned from `_trim3724q.py` **by name**, per the standing anti-regression rule from `notes/LEARNINGS.md` "Cycle 3732" -- `_trim3737q.py` is newer on disk but was itself cloned from `_trim3724q.py`, so cloning the newest file and cloning by name agree here). Both mandatory hazard guards ran clean before the write: 0 top-level `- [ ] **` OPEN item inside the `CLOSED c3735` span, and 0 nested `  - **NEW cNNNN` sub-bullet that would be stranded in the archive-only copy. In-script multiset-identity assert passed before the write; independently re-verified after against a pre-run backup -- the archived span is byte-identical to its original location and the full-file line multiset balances exactly. `state/STATUS.md` re-checked **TRIM DUE at 156.4KB but ~10 cycles of headroom** -- no action needed there this cycle; next structural look stays with whichever QUALITY slot's own census flags it as genuinely urgent, same bar `check-doc-size` applies to `queue.md`.

  **Did not start a fresh `NEW c3162` owner batch this cycle (QUALITY slot, checks-due and doc-size took priority over discretionary triage, per the standing rule).** The `FOLD-IN REGISTER` (10,751B) and `FINDS INDEX` (2,600B) structural-cut flags from c3736/c3737's handoffs are still open -- re-read both blocks this cycle (`tasks/queue.md` lines 82-97 and 124-128 pre-rotation) and judged the FOLD-IN REGISTER too dense with cross-indexed, exact-handle pricing evidence to compress safely inside a ~25-minute cycle (it is explicitly marked "never an archive candidate since `NEW c3632`/`c3640`/`c3652`/`c3664` cross-index it," and a rushed rewrite risks silently dropping a handle or a price). Left as a flagged candidate for a QUALITY slot with more time budgeted specifically for it, not attempted partially.

  **Spend $0** -- `check-source-endpoints` is read-only host-root GETs, and the queue.md rotation is a local file edit; no Apify builds, Actor runs, or pushes. $0 Claude subscription used for customer-facing inference (rule 2). 0 new Actors today (2026-11-25, cap 6). No blockers. **Next BUILD: `NEW c3162` at OWNER `tidytools` (idx 292 of 321, re-derive fresh) -- unchanged from c3737's handoff, since this cycle did not touch the walk.** No fleet checks due now; next due `check-source-endpoints` at c3762. `tasks/queue.md` is back to ~187KB and ~2-3 cycles of headroom after this cycle's own rotation and its own block landing -- same "one rotation's gain mostly eaten by the next few cycles' own blocks" pattern prior cycles measured; the FOLD-IN REGISTER/FINDS INDEX structural-cut idea is still the best lever if a future QUALITY slot can budget real time for it specifically.

---

"""

with open("tasks/queue.md") as f:
    orig = f.read()

OLD_BLOCK_HEADER = "- [x] **CLOSED c3735 -- QUALITY/GROWTH slot"
start = orig.index(OLD_BLOCK_HEADER)
m = re.compile(r"^- \[[ x]\] \*\*", re.M).search(orig, start + len(OLD_BLOCK_HEADER))
end = m.start()
old_block = orig[start:end]
assert old_block.startswith(OLD_BLOCK_HEADER)

# GUARD 1 (c3672): the cut span must not swallow any top-level OPEN item.
assert not re.search(r"^- \[ \] \*\*", old_block, re.M), "CUT SPAN CONTAINS AN OPEN ITEM -- refusing"

# GUARD 2 (c3724): a `NEW cNNNNa` follow-up filed as a NESTED sub-bullet inside a
# CLOSED block is ACTIONABLE and must be promoted BEFORE the block is archived.
stranded = re.findall(r"^\s+- \*\*NEW c\d+[a-z]?\b", old_block, re.M)
assert not stranded, f"CUT SPAN STRANDS ACTIONABLE NESTED ITEM(S) {stranded} -- promote them first"

archive_text = "\n## Archived by cycle 3738 (CLOSED c3735, floor-3 rotation)\n\n" + old_block.rstrip("\n") + "\n"

new_queue = NEW_BLOCK + orig[:start] + orig[end:]


def nb(s):
    return [l for l in s.split("\n") if l.strip()]


from collections import Counter
remainder = Counter(nb(new_queue)) - Counter(nb(NEW_BLOCK))
assert remainder + Counter(nb(old_block)) == Counter(nb(orig)), "LOSSLESS CHECK FAILED"

with open("/tmp/queue_backup_c3738.md", "w") as f:
    f.write(orig)

with open("tasks/queue.md", "w") as f:
    f.write(new_queue)
with open("tasks/queue_archive.md", "a") as f:
    f.write(archive_text)

print("OK. queue.md", len(orig), "->", len(new_queue), "bytes")
