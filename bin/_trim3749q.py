#!/root/agent/venv/bin/python
"""Cycle 3749 tasks/queue.md floor-3 rotation, in ONE in-memory build + verify + write.
Clone of _trim3748q.py BY NAME (the GUARDED multi-block-span template).

CUT COUNT RE-DERIVED FRESH. Live top-level rotation-pool blocks before this cycle's own
block is added are THREE: c3748/c3747/c3746 -- already at the floor. Adding this cycle's
own CLOSED c3749 block (appended separately, at the top, before running this script) makes
the pool FOUR: c3749/c3748/c3747/c3746. Floor is 3 = keep newest 2 existing (c3748/c3747)
plus this cycle's own block (c3749), so the correct cut is the oldest ONE: c3746.

GUARD 2 checked by hand before writing this script: the c3746 span contains zero nested
`NEW cNNNNa` sub-bullets (dashed, dash-less or backticked forms all checked), so no
promotion step is needed this cycle -- this is a plain single-block cut.
"""
import re
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

orig = open(QUEUE).read()
TOP = re.compile(r"^- \[[ x]\] \*\*", re.M)
NESTED = re.compile(r"^\s+(?:- )?\*\*`?NEW c(\d+[a-z]?)`?\b", re.M)

# ---- derive the cut span: CLOSED c3746 only ----------------------------------
START = "- [x] **CLOSED c3746 -- BUILD slot"
start = orig.index(START)
m = TOP.search(orig, start + len(START))
end = m.start()
span = orig[start:end]

assert span.startswith(START)
assert span.count("- [x] **CLOSED c") == 1, "span shape unexpected -- wrong block count"
assert "CLOSED c3749" not in span and "CLOSED c3748" not in span and "CLOSED c3747" not in span, \
    "floor-3 would be breached"
assert not re.search(r"^- \[[ x]\] \*\*CLOSED c3544\b", span, re.M), \
    "one-off closure DEFINITION must not be rotated"
# GUARD 1 (c3672): never swallow a top-level OPEN item.
assert not re.search(r"^- \[ \] \*\*", span, re.M), "CUT SPAN CONTAINS AN OPEN ITEM -- refusing"

# ---- GUARD 2 (c3724/c3748): nested actionables must be promoted, never stranded -
nested_lines = [l for l in span.split("\n") if NESTED.match(l)]
found = sorted(NESTED.match(l).group(1) for l in nested_lines)
assert found == [], f"unexpected nested set {found} -- re-read the span, promotion step needed"

# ---- build the new live file in MEMORY (c3492 lesson: verify, THEN write) -----
new_queue = orig[:start] + orig[end:]
new_queue = re.sub(r"\n{3,}", "\n\n", new_queue)

archive_text = (
    "\n## Archived by cycle 3749 (CLOSED c3746, floor-3 rotation; no nested\n"
    "## actionable items found in the span, so nothing needed promotion)\n\n"
    + span.rstrip("\n")
    + "\n"
)

def nb(s):
    return [l for l in s.split("\n") if l.strip()]

assert Counter(nb(new_queue)) + Counter(nb(span)) == Counter(nb(orig)), \
    "LOSSLESS CHECK FAILED"
assert span.rstrip("\n") in archive_text
assert "CLOSED c3746" in archive_text

open(QUEUE, "w").write(new_queue)
open(ARCHIVE, "a").write(archive_text)
print(f"OK. queue.md {len(orig)} -> {len(new_queue)} bytes (-{len(orig)-len(new_queue)})")
print(f"   rotation span {len(span)}B over 1 block; 0 nested items promoted")
