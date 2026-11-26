#!/root/agent/venv/bin/python
"""Cycle 3747 QUALITY-slot tasks/queue.md work, in ONE in-memory build + verify + write.

c3746's handoff flagged that the floor-3 CLOSED-block rotation lever is exhausted (only
~1 cycle of headroom gained because the cut block was small) and said the next lever is
a per-block byte census of the NON-CLOSED content, not another rotation. Census found the
`NEW c3162` RESUME POINTER line (tasks/queue.md line 142) at 7,318B on one line -- the
single biggest non-CLOSED line in the file -- and it is carrying TWO fully superseded
pointer generations (the `thoob`-era c3736 completion, and the `tubetext`-era c3742
completion) that the live c3746 pointer has already superseded. This is exactly the
regrowth pattern PLAYBOOK's "why the per-batch line keeps regrowing" section and the
c3732 FINDS INDEX compression both describe: history that is no longer load-bearing
sitting in the live file instead of the archive.

Lossy BY DESIGN (same as c3732): the stale span is archived VERBATIM, not deleted.
"""
import re
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

orig = open(QUEUE).read()
lines = orig.split("\n")

idx = [i for i, l in enumerate(lines) if l.lstrip().startswith("- **RESUME POINTER is an OWNER NAME")]
assert len(idx) == 1, f"expected exactly 1 RESUME POINTER line, got {len(idx)}"
i = idx[0]
old_line = lines[i]
assert len(old_line) > 7000, f"RESUME POINTER line unexpectedly short ({len(old_line)}B) -- re-read before cutting"

A = "**Completed through `thoob`"
B = "**POINTER SUPERSEDED (c3746)"
a = old_line.index(A)
b = old_line.index(B)
assert a < b, "marker order unexpected"
stale = old_line[a:b]
assert "POINTER SUPERSEDED -- READ THIS CLAUSE, NOT THE ONE ABOVE (c3742)" in stale
assert "NEXT OWNER: `thriftykiwi`" in stale
assert "NEXT OWNER: `unfenced-group`" in stale
# the only `NEW cNNNN` token in the stale span is a cross-reference, not a sub-bullet
# definition living only here -- confirm that shape before archiving.
refs = re.findall(r"NEW c\d+[a-z]?", stale)
assert refs == ["NEW c3632"], f"unexpected NEW c-refs in stale span: {refs}"

NOTE = (
    "**COMPRESSED c3747 -- two fully superseded pointer generations (the `thoob`-era "
    "c3736 completion and the `tubetext`-era c3742 completion, both already superseded "
    "by the live c3746 pointer below) archived verbatim in `tasks/queue_archive.md`, "
    "`## Archived by cycle 3747`. Full pre-compression line is there too, in case any "
    "nuance was lost.** "
)

new_line = old_line[:a] + NOTE + old_line[b:]
assert len(new_line) < len(old_line)

new_lines = list(lines)
new_lines[i] = new_line
new_queue = "\n".join(new_lines)

archive_text = (
    "\n## Archived by cycle 3747 (NEW c3162 RESUME POINTER -- 2 superseded pointer generations, pre-compression line verbatim)\n\n"
    "### Pre-compression `NEW c3162` RESUME POINTER line (7,318B, replaced in place by cycle 3747)\n\n"
    + old_line.strip()
    + "\n"
)

# ------------------------------------------------------- lossless verify, THEN write
def nb(s):
    return [l for l in s.split("\n") if l.strip()]

expect = Counter(nb(orig)) - Counter([old_line]) + Counter([new_line])
assert Counter(nb(new_queue)) == expect, "LOSSLESS CHECK FAILED"
assert old_line.strip() in archive_text, "old RESUME POINTER line not preserved in archive"
assert new_line in new_queue and old_line not in new_queue
assert "NEXT OWNER: `unrivaled_fortress`" in new_queue, "current live pointer lost -- abort"

open(QUEUE, "w").write(new_queue)
open(ARCHIVE, "a").write(archive_text)
print(f"OK. queue.md {len(orig)} -> {len(new_queue)} bytes (-{len(orig)-len(new_queue)})")
print(f"   RESUME POINTER line {len(old_line)} -> {len(new_line)}B")
