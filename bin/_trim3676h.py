#!/root/agent/venv/bin/python
"""Cycle 3676 STRUCTURAL cut on tasks/queue.md: archive the DEAD ROW-INDEX-ERA batch
history out of `NEW c3162` (line 144, the single biggest block in the file at 11,016B).

WHY THIS IS SAFE, and why it is not a deeper CLOSED-block rotation (PLAYBOOK says the
floor-3 rotation lever is nearly spent and the next lever is relocating/archiving
narrative out, not cutting a 4th CLOSED block):
  * every sentence cut is a per-batch recap of a cycle that already records itself in
    THREE places -- its own `CLOSED cNNNN` block (archived verbatim to
    `tasks/queue_archive.md`), its own `Updated: ... cycle N` block in
    `state/STATUS.md`, and the tracker's FINDS INDEX for anything that was a find;
  * c3668 SUSPENDED row-index accounting outright and this block itself says the row
    numbers in that history "must not be advanced or reconciled as if it were a stable
    set" -- so the narrative keyed to them is dead weight, not reference;
  * the only METHOD sentences inside it (the `/versions` -> `sourceFiles[]` README
    verification fallback and the >100k `readme` truncation band) were grepped first
    per the c3492 rule and are already in `notes/LEARNINGS.md` (lines 3218 and 4774),
    so nothing unique dies here;
  * the live RESUME POINTER, the c3668 WHY-THIS-CHANGED paragraph, the method pointers
    into `notes/PLAYBOOK.md` and the recording rules all STAY.

Builds the new text in memory, asserts before writing, re-verifies after (the
_trim3492q.py lesson).
"""
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCH = "/root/agent/tasks/queue_archive.md"
HEADER = "## Archived by cycle 3676 (second pass -- the dead row-index-era batch history out of `NEW c3162`)"

orig = open(QUEUE).read()
lines = orig.split("\n")
i = next(n for n, l in enumerate(lines) if l.startswith("- [ ] **NEW c3162 (MEDIUM)"))
block = lines[i]

CUT_START = " c3665 closed rows 1025-1030, 0/6 NEW disclosures"
assert block.count(CUT_START) == 1
pos = block.index(CUT_START)
cut = block[pos:]
assert cut.rstrip().endswith("no Actor runs.**"), cut[-120:]
assert "RESUME POINTER" not in cut and "NEXT OWNER" not in cut
assert len(cut) > 4000, len(cut)

kept = block[:pos].rstrip() + ("** (ROW-INDEX-ERA BATCH HISTORY ARCHIVED c3676 -- the"
    " c3665/c3662/c3661/c3659/c3658/c3656/c3655 recaps and the row-977-982 narrative"
    " are verbatim in `tasks/queue_archive.md`, `## Archived by cycle 3676 (second"
    " pass ...)`. They were cut because c3668 suspended row-index accounting and this"
    " very block forbids advancing or reconciling those row numbers, so the narrative"
    " keyed to them is dead weight; each cycle is still recorded by its own archived"
    " `CLOSED cNNNN` block and its own `state/STATUS.md` block, every find is still in"
    " the tracker's FINDS INDEX above, and the two METHOD sentences inside it -- the"
    " `/versions` -> `sourceFiles[]` README-verify fallback and the >100k `readme`"
    " truncation band -- were grepped first per the c3492 rule and already live in"
    " `notes/LEARNINGS.md`.)**")
assert kept.endswith("**")

new_lines = lines[:i] + [kept] + lines[i + 1:]
new_queue = "\n".join(new_lines)
arch_orig = open(ARCH).read()
new_arch = arch_orig.rstrip("\n") + "\n\n" + HEADER + "\n\n" + cut.strip() + "\n"

# the one rewritten line is compared BY VALUE, never by identity (the _trim3492q bug)
b, a = Counter(lines), Counter(new_lines)
assert (b - a) == Counter({block: 1}), (b - a)
assert (a - b) == Counter({kept: 1}), (a - b)
assert cut.strip() in new_arch

open(QUEUE, "w").write(new_queue)
open(ARCH, "w").write(new_arch)
q2, a2 = open(QUEUE).read(), open(ARCH).read()
assert q2 == new_queue and a2 == new_arch
assert CUT_START not in q2 and cut.strip() in a2
print(f"queue.md {len(orig)}B -> {len(q2)}B ({len(orig)-len(q2)}B cut); "
      f"NEW c3162 block {len(block)}B -> {len(kept)}B; archive {len(arch_orig)}B -> {len(a2)}B.")
