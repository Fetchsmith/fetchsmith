#!/root/agent/venv/bin/python
"""Cycle 3745 tasks/queue.md floor-3 rotation, in ONE in-memory build + verify + write.
Clone of _trim3743q.py BY NAME (the GUARDED multi-block-span template).

4 live top-level `CLOSED cNNNN` rotation-pool blocks exist (c3744/c3743/c3742/c3741) before
this cycle's own block is added; floor is 3 (keep newest 2 existing + this cycle's own, per
`STANDING c3280`). Correct cut is therefore the oldest TWO: c3742, c3741.
(`CLOSED c3544` is a separate one-off closure, not part of this rotation pool, and is left alone.)
"""
import re
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

orig = open(QUEUE).read()

START = "- [x] **CLOSED c3742 -- BUILD slot"
start = orig.index(START)
SECOND = "- [x] **CLOSED c3741 -- QUALITY"
second = orig.index(SECOND, start)
m = re.compile(r"^- \[[ x]\] \*\*", re.M).search(orig, second + len(SECOND))
end = m.start()
span = orig[start:end]

assert span.startswith(START)
assert "CLOSED c3741" in span, "expected both blocks in the contiguous span"
assert span.count("- [x] **CLOSED c") == 2, "span shape unexpected -- wrong block count"
assert "CLOSED c3744" not in span and "CLOSED c3743" not in span, "floor-3 would be breached"
# GUARD 1 (c3672): never swallow a top-level OPEN item.
assert not re.search(r"^- \[ \] \*\*", span, re.M), "CUT SPAN CONTAINS AN OPEN ITEM -- refusing"
# GUARD 2 (c3724): never strand an actionable nested `NEW cNNNNa` follow-up.
stranded = re.findall(r"^\s+- \*\*NEW c\d+[a-z]?\b", span, re.M)
assert not stranded, f"CUT SPAN STRANDS ACTIONABLE NESTED ITEM(S) {stranded} -- promote first"

new_queue = orig[:start] + orig[end:]
new_queue = re.sub(r"\n{3,}", "\n\n", new_queue)

archive_text = (
    "\n## Archived by cycle 3745 (CLOSED c3742 + CLOSED c3741, floor-3 rotation)\n\n"
    + span.rstrip("\n")
    + "\n"
)

def nb(s):
    return [l for l in s.split("\n") if l.strip()]

expect = Counter(nb(orig)) - Counter(nb(span))
assert Counter(nb(new_queue)) == expect, "LOSSLESS CHECK FAILED"
assert "CLOSED c3742" in archive_text and "CLOSED c3741" in archive_text

open(QUEUE, "w").write(new_queue)
open(ARCHIVE, "a").write(archive_text)
print(f"OK. queue.md {len(orig)} -> {len(new_queue)} bytes (-{len(orig)-len(new_queue)})")
print(f"   rotation span {len(span)}B")
