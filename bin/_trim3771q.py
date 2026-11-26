#!/root/agent/venv/bin/python
"""Cycle 3771 tasks/queue.md floor-3 rotation, in ONE in-memory build + verify + write.
Clone of _trim3768q.py BY NAME, per notes/PLAYBOOK.md's explicit "CLONE `bin/_trim3748q.py`
BY NAME" lineage (3768q is itself that clone with the widened Guard-2 regex + promotion step).

POOL RE-DERIVED FRESH BY GREP AND CLASSIFICATION (never from a forwarded number). A fresh
grep of `^- \\[x\\] \\*\\*CLOSED c(\\d+)` finds heads at both report blocks AND one-off ITEM
closures (`CLOSED c3764 (was NEW c3760 ...)`, `CLOSED c3544 (DONE c3720 ...)`,
`CLOSED c3760 (was NEW c3458 ...)`) -- the latter are NOT in the rotation pool (c3745/c3748
rule: only cycle report blocks rotate). Live rotation pool is FIVE report blocks:
c3770/c3769/c3768/c3767/c3766. Floor is 3 = keep the newest 2 (c3770, c3769) plus this
cycle's own block, so the correct cut is the oldest THREE: c3768, c3767, c3766 -- one
contiguous span (verified by head census: ends exactly at `NEW c3728 -- SHIPPED`, the next
top-level head after c3766's block).
"""
import re
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

orig = open(QUEUE).read()
TOP = re.compile(r"^- \[[ x]\] \*\*", re.M)
# WIDENED GUARD 2 (c3748): dashed OR dash-less, backtick optional.
NESTED = re.compile(r"^\s+(?:- )?\*\*`?NEW c(\d+[a-z]?)`?\b", re.M)

# ---- derive the cut span: c3768 start -> end of c3766 -------------------------
START = "- [x] **CLOSED c3768 -- QUALITY slot"
MID1 = "- [x] **CLOSED c3767 -- BUILD slot"
MID2 = "- [x] **CLOSED c3766 -- BUILD slot"
start = orig.index(START)
mid1 = orig.index(MID1)
mid2 = orig.index(MID2)
m = TOP.search(orig, mid2 + len(MID2))
end = m.start()
span = orig[start:end]

assert span.startswith(START)
assert start < mid1 < mid2, "blocks must be in c3768 -> c3767 -> c3766 order for one span"
assert span.count("- [x] **CLOSED c") == 3, "span shape unexpected -- wrong block count"
assert "CLOSED c3770" not in span and "CLOSED c3769" not in span, "floor-3 would be breached"
# The one-off ITEM closures must keep their own top-level DEFINITION heads live --
# none of them are in this span at all, but assert it anyway (c3747 mention-vs-definition).
for oneoff in (r"^- \[x\] \*\*CLOSED c3544\b", r"^- \[x\] \*\*CLOSED c3764 \(was",
               r"^- \[x\] \*\*CLOSED c3760 \(was"):
    assert not re.search(oneoff, span, re.M), f"one-off closure DEFINITION in span: {oneoff}"
# GUARD 1 (c3672): never swallow a top-level OPEN item.
assert not re.search(r"^- \[ \] \*\*", span, re.M), "CUT SPAN CONTAINS AN OPEN ITEM -- refusing"
# the still-open NEW c3768 lever (one-off-closure byte lever) must sit AFTER this span,
# i.e. this rotation must not touch or strand it.
assert "NEW c3768 (MEDIUM" not in span, "NEW c3768 lever item must not be in the cut span"

# ---- GUARD 2 (c3724, widened c3748): promote nested actionables, never strand -
nested_lines = [l for l in span.split("\n") if NESTED.match(l)]
found = sorted(NESTED.match(l).group(1) for l in nested_lines)
assert found == [], f"unexpected nested actionable(s) {found} -- promote them, re-read the span"
promoted = []  # nothing to promote this cycle; kept so the lossless assert below is identical

# ---- build the new live file in MEMORY (c3492 lesson: verify, THEN write) -----
new_queue = orig[:start] + orig[end:]
new_queue = re.sub(r"\n{3,}", "\n\n", new_queue)

archive_text = (
    "\n## Archived by cycle 3771 (CLOSED c3768 + CLOSED c3767 + CLOSED c3766, floor-3\n"
    "## rotation; pool was 5 report blocks, keeping c3770/c3769 + cycle 3771's own block.\n"
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
for cid in ("c3768", "c3767", "c3766"):
    assert f"CLOSED {cid}" in archive_text
# and the kept file must no longer carry any of the three as a top-level report-block head
for cid in ("3767", "3766"):
    assert not re.search(r"^- \[x\] \*\*CLOSED c" + cid + r" --", new_queue, re.M), cid
assert not re.search(r"^- \[x\] \*\*CLOSED c3768 -- QUALITY", new_queue, re.M)
# the unrelated c3768-cycle one-off ITEM closure (different block, same cycle id) must survive
assert re.search(r"^- \[x\] \*\*CLOSED c3768 \(was", new_queue, re.M), \
    "the c3768 one-off ITEM closure (was NEW c3764) must still be live"
# the still-open NEW c3768 lever item must survive untouched
assert "NEW c3768 (MEDIUM" in new_queue

open(QUEUE, "w").write(new_queue)
open(ARCHIVE, "a").write(archive_text)
print(f"OK. queue.md {len(orig)} -> {len(new_queue)} bytes (-{len(orig)-len(new_queue)})")
print(f"   rotation span {len(span)}B over 3 blocks; promoted {len(promoted)} nested item(s)")
