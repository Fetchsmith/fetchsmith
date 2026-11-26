#!/root/agent/venv/bin/python
"""Cycle 3743 tasks/queue.md floor-3 rotation, in ONE in-memory build + verify + write.
Clone of _trim3741q.py BY NAME (the GUARDED multi-block-span template, itself cloned from
_trim3735q.py) -- c3742's handoff flagged this rotation as owed but undercounted the cut
(said "oldest ONE, CLOSED c3739"), the same undercount shape c3741 caught on c3740's handoff.

4 live top-level `CLOSED cNNNN` rotation-pool blocks exist (c3742/c3741/c3740/c3739) before
this cycle's own block is added; floor is 3 (keep newest 2 existing + this cycle's own, per
`STANDING c3280`). Correct cut is therefore the oldest TWO: c3740, c3739 -- not just c3739.
(`CLOSED c3544` is a separate one-off closure, not part of this rotation pool, and is left alone.)
"""
import re
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

orig = open(QUEUE).read()

START = "- [x] **CLOSED c3740 -- BUILD slot"
start = orig.index(START)
SECOND = "- [x] **CLOSED c3739 -- BUILD slot"
second = orig.index(SECOND, start)
# END AT THE NEXT TOP-LEVEL ITEM HEAD, NEVER AT THE NEXT "---" (the c3724 lesson) -- the
# CLOSED blocks are not a contiguous prefix of the file, so a `---`-terminated span can
# over- or under-capture depending on what divider convention the surrounding text used.
m = re.compile(r"^- \[[ x]\] \*\*", re.M).search(orig, second + len(SECOND))
end = m.start()
span = orig[start:end]

assert span.startswith(START)
assert "CLOSED c3739" in span, "expected both blocks in the contiguous span"
assert span.count("- [x] **CLOSED c") == 2, "span shape unexpected -- wrong block count"
assert "CLOSED c3742" not in span and "CLOSED c3741" not in span, "floor-3 would be breached"
# GUARD 1 (c3672): never swallow a top-level OPEN item.
assert not re.search(r"^- \[ \] \*\*", span, re.M), "CUT SPAN CONTAINS AN OPEN ITEM -- refusing"
# GUARD 2 (c3724): never strand an actionable nested `NEW cNNNNa` follow-up.
stranded = re.findall(r"^\s+- \*\*NEW c\d+[a-z]?\b", span, re.M)
assert not stranded, f"CUT SPAN STRANDS ACTIONABLE NESTED ITEM(S) {stranded} -- promote first"

new_queue = orig[:start] + orig[end:]
new_queue = re.sub(r"\n{3,}", "\n\n", new_queue)

archive_text = (
    "\n## Archived by cycle 3743 (CLOSED c3740 + CLOSED c3739, floor-3 rotation)\n\n"
    + span.rstrip("\n")
    + "\n"
)

def nb(s):
    return [l for l in s.split("\n") if l.strip()]

expect = Counter(nb(orig)) - Counter(nb(span))
assert Counter(nb(new_queue)) == expect, "LOSSLESS CHECK FAILED"
assert "CLOSED c3740" in archive_text and "CLOSED c3739" in archive_text

open(QUEUE, "w").write(new_queue)
open(ARCHIVE, "a").write(archive_text)
print(f"OK. queue.md {len(orig)} -> {len(new_queue)} bytes (-{len(orig)-len(new_queue)})")
print(f"   rotation span {len(span)}B")
