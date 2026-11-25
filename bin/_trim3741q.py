#!/root/agent/venv/bin/python
"""Cycle 3741 QUALITY-slot tasks/queue.md floor-3 rotation, in ONE in-memory build + verify + write.
Clone of _trim3735q.py BY NAME (the GUARDED template for a multi-block span archive; c3740 flagged
this rotation as overdue but only named one block -- re-derived the real floor-3 math below).

5 live top-level `CLOSED cNNNN` blocks exist (c3740/c3739/c3738/c3737/c3736) before this cycle's
own block is added; floor is 3 (keep newest 2 existing + this cycle's own, per `STANDING c3280`).
Archive the oldest THREE: c3738, c3737, c3736. They are contiguous top-level heads (each separated
only by a `---` divider, no OPEN item in between), so the cut is one span.
"""
import re
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

orig = open(QUEUE).read()

START = "- [x] **CLOSED c3738 -- QUALITY/GROWTH slot"
start = orig.index(START)
SECOND = "- [x] **CLOSED c3737 -- BUILD slot"
second = orig.index(SECOND, start)
THIRD = "- [x] **CLOSED c3736 -- BUILD slot"
third = orig.index(THIRD, second)
# END AT THE NEXT TOP-LEVEL ITEM HEAD, NEVER AT THE NEXT "---" (the c3724 lesson) -- the
# CLOSED blocks are not a contiguous prefix of the file, so a `---`-terminated span can
# over- or under-capture depending on what divider convention the surrounding text used.
m = re.compile(r"^- \[[ x]\] \*\*", re.M).search(orig, third + len(THIRD))
end = m.start()
span = orig[start:end]

assert span.startswith(START)
assert "CLOSED c3737" in span and "CLOSED c3736" in span, "expected all 3 blocks in the contiguous span"
assert span.count("- [x] **CLOSED c") == 3, "span shape unexpected -- wrong block count"
assert "CLOSED c3740" not in span and "CLOSED c3739" not in span, "floor-3 would be breached"
# GUARD 1 (c3672): never swallow a top-level OPEN item.
assert not re.search(r"^- \[ \] \*\*", span, re.M), "CUT SPAN CONTAINS AN OPEN ITEM -- refusing"
# GUARD 2 (c3724): never strand an actionable nested `NEW cNNNNa` follow-up.
stranded = re.findall(r"^\s+- \*\*NEW c\d+[a-z]?\b", span, re.M)
assert not stranded, f"CUT SPAN STRANDS ACTIONABLE NESTED ITEM(S) {stranded} -- promote first"

new_queue = orig[:start] + orig[end:]
new_queue = re.sub(r"\n{3,}", "\n\n", new_queue)

archive_text = (
    "\n## Archived by cycle 3741 (CLOSED c3738 + CLOSED c3737 + CLOSED c3736, floor-3 rotation)\n\n"
    + span.rstrip("\n")
    + "\n"
)

def nb(s):
    return [l for l in s.split("\n") if l.strip()]

expect = Counter(nb(orig)) - Counter(nb(span))
assert Counter(nb(new_queue)) == expect, "LOSSLESS CHECK FAILED"
assert "CLOSED c3738" in archive_text and "CLOSED c3737" in archive_text and "CLOSED c3736" in archive_text

open(QUEUE, "w").write(new_queue)
open(ARCHIVE, "a").write(archive_text)
print(f"OK. queue.md {len(orig)} -> {len(new_queue)} bytes (-{len(orig)-len(new_queue)})")
print(f"   rotation span {len(span)}B")
