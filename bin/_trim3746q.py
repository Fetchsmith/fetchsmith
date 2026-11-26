#!/root/agent/venv/bin/python
"""Cycle 3746 tasks/queue.md floor-3 rotation, in ONE in-memory build + verify + write.
Clone of _trim3745q.py BY NAME (the GUARDED multi-block-span template).

4 live top-level `CLOSED cNNNN` rotation-pool blocks exist (c3746/c3745/c3744/c3743) after
this cycle's own block was added; floor is 3 (keep newest 2 existing plus this cycle's own,
per `STANDING c3280`). Correct cut is therefore the oldest ONE: c3743.
(`CLOSED c3544` is a separate one-off closure, not part of this rotation pool, and is left alone.)
"""
import re
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

orig = open(QUEUE).read()

START = "- [x] **CLOSED c3743 -- BUILD slot"
start = orig.index(START)
m = re.compile(r"^- \[[ x]\] \*\*", re.M).search(orig, start + len(START))
end = m.start()
span = orig[start:end]

assert span.startswith(START)
assert span.count("- [x] **CLOSED c") == 1, "span shape unexpected -- wrong block count"
assert "CLOSED c3746" not in span and "CLOSED c3745" not in span and "CLOSED c3744" not in span, \
    "floor-3 would be breached"
# GUARD 1 (c3672): never swallow a top-level OPEN item.
assert not re.search(r"^- \[ \] \*\*", span, re.M), "CUT SPAN CONTAINS AN OPEN ITEM -- refusing"
# GUARD 2 (c3724): never strand an actionable nested `NEW cNNNNa` follow-up.
stranded = re.findall(r"^\s+- \*\*NEW c\d+[a-z]?\b", span, re.M)
assert not stranded, f"CUT SPAN STRANDS ACTIONABLE NESTED ITEM(S) {stranded} -- promote first"

new_queue = orig[:start] + orig[end:]
new_queue = re.sub(r"\n{3,}", "\n\n", new_queue)

archive_text = (
    "\n## Archived by cycle 3746 (CLOSED c3743, floor-3 rotation)\n\n"
    + span.rstrip("\n")
    + "\n"
)

def nb(s):
    return [l for l in s.split("\n") if l.strip()]

expect = Counter(nb(orig)) - Counter(nb(span))
assert Counter(nb(new_queue)) == expect, "LOSSLESS CHECK FAILED"
assert "CLOSED c3743" in archive_text

open(QUEUE, "w").write(new_queue)
open(ARCHIVE, "a").write(archive_text)
print(f"OK. queue.md {len(orig)} -> {len(new_queue)} bytes (-{len(orig)-len(new_queue)})")
print(f"   rotation span {len(span)}B")
