#!/root/agent/venv/bin/python
"""Cycle 3768 tasks/queue.md floor-3 rotation, in ONE in-memory build + verify + write.
Clone of _trim3748q.py BY NAME, per notes/PLAYBOOK.md's explicit "CLONE `bin/_trim3748q.py`
BY NAME, NOT the newest `_trim*q.py` on disk" directive (the GUARDED template with the
WIDENED Guard-2 regex + promotion step; _trim3765q.py is newer but single-span-only and
keys spans by cycle id in a dict, which COLLIDES here -- see next paragraph).

POOL RE-DERIVED FRESH BY GREP (never from the forwarded number). c3767's handoff said
"8 live CLOSED blocks vs floor 3". A fresh grep of `^- \\[x\\] \\*\\*CLOSED c(\\d+)` finds 8 heads,
but THREE of them are one-off ITEM closures, not cycle report blocks, and are therefore NOT
in the rotation pool (the c3745/c3748 `CLOSED c3544` distinction):
    L24 `CLOSED c3764 (was NEW c3760 ...)`   <- note: SAME cycle id as the real c3764 report
    L48 `CLOSED c3544 (DONE c3720 ...)`         block, so any id-keyed dict silently drops one
    L78 `CLOSED c3760 (was NEW c3458 ...)`
Live rotation pool is therefore FIVE report blocks: c3767/c3766/c3765/c3764/c3763.
Floor is 3 = keep the newest 2 (c3767, c3766) plus this cycle's own block, so the correct
cut is the oldest THREE: c3765, c3764, c3763 -- one contiguous span, verified by head census.
"""
import re
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

orig = open(QUEUE).read()
TOP = re.compile(r"^- \[[ x]\] \*\*", re.M)
# WIDENED GUARD 2 (c3748): dashed OR dash-less, backtick optional.
NESTED = re.compile(r"^\s+(?:- )?\*\*`?NEW c(\d+[a-z]?)`?\b", re.M)

# ---- derive the cut span: c3765 start -> end of c3763 -------------------------
START = "- [x] **CLOSED c3765 -- QUALITY slot"
MID1 = "- [x] **CLOSED c3764 -- BUILD slot"
MID2 = "- [x] **CLOSED c3763 -- BUILD slot"
start = orig.index(START)
mid1 = orig.index(MID1)
mid2 = orig.index(MID2)
m = TOP.search(orig, mid2 + len(MID2))
end = m.start()
span = orig[start:end]

assert span.startswith(START)
assert start < mid1 < mid2, "blocks must be in c3765 -> c3764 -> c3763 order for one span"
assert span.count("- [x] **CLOSED c") == 3, "span shape unexpected -- wrong block count"
assert "CLOSED c3767" not in span and "CLOSED c3766" not in span, "floor-3 would be breached"
# The three one-off ITEM closures must keep their own top-level DEFINITION heads live.
# Mention vs definition, the c3747 distinction (c3765's block MENTIONS c3764 by number).
for oneoff in (r"^- \[x\] \*\*CLOSED c3544\b", r"^- \[x\] \*\*CLOSED c3764 \(was",
               r"^- \[x\] \*\*CLOSED c3760 \(was"):
    assert not re.search(oneoff, span, re.M), f"one-off closure DEFINITION in span: {oneoff}"
# GUARD 1 (c3672): never swallow a top-level OPEN item.
assert not re.search(r"^- \[ \] \*\*", span, re.M), "CUT SPAN CONTAINS AN OPEN ITEM -- refusing"

# ---- GUARD 2 (c3724, widened c3748): promote nested actionables, never strand -
nested_lines = [l for l in span.split("\n") if NESTED.match(l)]
found = sorted(NESTED.match(l).group(1) for l in nested_lines)
assert found == [], f"unexpected nested actionable(s) {found} -- promote them, re-read the span"
promoted = []  # nothing to promote this cycle; kept so the lossless assert below is identical

# ---- build the new live file in MEMORY (c3492 lesson: verify, THEN write) -----
new_queue = orig[:start] + orig[end:]
new_queue = re.sub(r"\n{3,}", "\n\n", new_queue)

archive_text = (
    "\n## Archived by cycle 3768 (CLOSED c3765 + CLOSED c3764 + CLOSED c3763, floor-3\n"
    "## rotation; pool was 5 report blocks, keeping c3767/c3766 + cycle 3768's own block.\n"
    "## Guard-2 hazard grep found 0 nested actionables in the span, so nothing was promoted.)\n\n"
    + span.rstrip("\n")
    + "\n"
)


def nb(s):
    return [l for l in s.split("\n") if l.strip()]


# nb(new) + nb(span) == nb(orig) + promoted   (span preserved verbatim in archive;
# promoted lines, if any, are the only ADDED content).  Compared BY VALUE (c3492).
assert Counter(nb(new_queue)) + Counter(nb(span)) == Counter(nb(orig)) + Counter(promoted), \
    "LOSSLESS CHECK FAILED"
assert span.rstrip("\n") in archive_text
for cid in ("c3765", "c3764", "c3763"):
    assert f"CLOSED {cid}" in archive_text
# and the kept file must no longer carry any of the three as a top-level head
for cid in ("3765", "3763"):
    assert not re.search(r"^- \[x\] \*\*CLOSED c" + cid + r"\b", new_queue, re.M), cid
assert not re.search(r"^- \[x\] \*\*CLOSED c3764 -- BUILD", new_queue, re.M)
assert re.search(r"^- \[x\] \*\*CLOSED c3764 \(was", new_queue, re.M), \
    "the c3764 one-off ITEM closure must still be live"

open(QUEUE, "w").write(new_queue)
open(ARCHIVE, "a").write(archive_text)
print(f"OK. queue.md {len(orig)} -> {len(new_queue)} bytes (-{len(orig)-len(new_queue)})")
print(f"   rotation span {len(span)}B over 3 blocks; promoted {len(promoted)} nested item(s)")
