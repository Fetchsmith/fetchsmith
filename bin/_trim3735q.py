#!/root/agent/venv/bin/python
"""Cycle 3735 QUALITY-slot tasks/queue.md floor-3 rotation, in ONE in-memory build + verify + write.
Clone of _trim3724q.py BY NAME (the GUARDED template -- never clone the most-recently-written
_trimNNNNq.py by recency alone; _trim3730q.py regressed the exact c3724 span bug and sat as the
newest file on disk for two cycles before c3732 caught it).

check-doc-size this cycle: tasks/queue.md 193.1KB / ~1 cycle of headroom -- TRIM DUE and urgent
(the decision rule is headroom < ~3 cycles, not the DUE banner itself, but 1 cycle is past that).

5 live top-level `CLOSED cNNNN` blocks exist (c3734/c3733/c3732/c3731/c3730) + this cycle's own
block = 6; floor is 3 (keep newest 2 existing + this cycle's own). Archive the oldest THREE:
c3732, c3731, c3730. They are contiguous top-level heads (c3732 -> c3731 -> c3730, each separated
only by a `---` divider, no OPEN item in between), so the cut is one span.
"""
import re
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

orig = open(QUEUE).read()

START = "- [x] **CLOSED c3732 -- QUALITY/GROWTH slot"
start = orig.index(START)
SECOND = "- [x] **CLOSED c3731 -- BUILD slot"
second = orig.index(SECOND, start)
THIRD = "- [x] **CLOSED c3730 -- BUILD slot"
third = orig.index(THIRD, second)
# END AT THE NEXT TOP-LEVEL ITEM HEAD, NEVER AT THE NEXT "---" (the c3724 lesson) -- the
# CLOSED blocks are not a contiguous prefix of the file, so a `---`-terminated span can
# over- or under-capture depending on what divider convention the surrounding text used.
m = re.compile(r"^- \[[ x]\] \*\*", re.M).search(orig, third + len(THIRD))
end = m.start()
span = orig[start:end]

assert span.startswith(START)
assert "CLOSED c3731" in span and "CLOSED c3730" in span, "expected all 3 blocks in the contiguous span"
assert span.count("- [x] **CLOSED c") == 3, "span shape unexpected -- wrong block count"
assert "CLOSED c3734" not in span and "CLOSED c3733" not in span, "floor-3 would be breached"
# GUARD 1 (c3672): never swallow a top-level OPEN item.
assert not re.search(r"^- \[ \] \*\*", span, re.M), "CUT SPAN CONTAINS AN OPEN ITEM -- refusing"
# GUARD 2 (c3724): never strand an actionable nested `NEW cNNNNa` follow-up.
stranded = re.findall(r"^\s+- \*\*NEW c\d+[a-z]?\b", span, re.M)
assert not stranded, f"CUT SPAN STRANDS ACTIONABLE NESTED ITEM(S) {stranded} -- promote first"

new_queue = orig[:start] + orig[end:]
new_queue = re.sub(r"\n{3,}", "\n\n", new_queue)

archive_text = (
    "\n## Archived by cycle 3735 (CLOSED c3732 + CLOSED c3731 + CLOSED c3730, floor-3 rotation)\n\n"
    + span.rstrip("\n")
    + "\n"
)

def nb(s):
    return [l for l in s.split("\n") if l.strip()]

expect = Counter(nb(orig)) - Counter(nb(span))
assert Counter(nb(new_queue)) == expect, "LOSSLESS CHECK FAILED"
assert "CLOSED c3732" in archive_text and "CLOSED c3731" in archive_text and "CLOSED c3730" in archive_text

open(QUEUE, "w").write(new_queue)
open(ARCHIVE, "a").write(archive_text)
print(f"OK. queue.md {len(orig)} -> {len(new_queue)} bytes (-{len(orig)-len(new_queue)})")
print(f"   rotation span {len(span)}B")
