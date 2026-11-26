#!/root/agent/venv/bin/python
"""Cycle 3748 tasks/queue.md floor-3 rotation, in ONE in-memory build + verify + write.
Clone of _trim3746q.py BY NAME (the GUARDED multi-block-span template), with GUARD 2 WIDENED.

CUT COUNT RE-DERIVED FRESH (the c3747 handoff said "cut CLOSED c3744" -- an UNDERCOUNT, the
same pattern logged against the c3741/c3742 handoffs). Live top-level rotation-pool blocks are
FOUR: c3747/c3746/c3745/c3744. Floor is 3 = keep newest 2 existing (c3747/c3746) plus this
cycle's own block, so the correct cut is the oldest TWO: c3745 AND c3744.
(`CLOSED c3544` is a separate one-off closure, not in this rotation pool, and is left alone.)

GUARD 2 BLIND SPOT FOUND AND FIXED THIS CYCLE -- a REAL near-loss, the c3724 shape again.
`CLOSED c3744` carries two actionable follow-ups, `NEW c3744a` (a measured trademark-search
filter gap) and `NEW c3744b` (the www.tmdn.org unreachability method note), written as
dash-less BACKTICKED bold paragraphs:

      **`NEW c3744a` (LOW-MEDIUM -- ...

The c3724 guard regex `^\\s+- \\*\\*NEW c\\d+` misses that form on TWO counts: there is no
leading `- ` dash, and a backtick sits between `**` and `NEW`. So the rotation would have
passed its own guard and stranded both in the archive -- exactly the c3724 loss. Widened
regex below matches the dashed, dash-less and backticked forms alike, and the script now
REQUIRES a promoted top-level copy in the live file for every nested item it finds.
"""
import re
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

orig = open(QUEUE).read()
TOP = re.compile(r"^- \[[ x]\] \*\*", re.M)
# WIDENED GUARD 2 (c3748): dashed OR dash-less, backtick optional.
NESTED = re.compile(r"^\s+(?:- )?\*\*`?NEW c(\d+[a-z]?)`?\b", re.M)

# ---- derive the cut span: c3745 start -> end of c3744 -------------------------
START = "- [x] **CLOSED c3745 -- BUILD slot"
MID = "- [x] **CLOSED c3744 -- QUALITY/GROWTH slot"
start = orig.index(START)
mid = orig.index(MID)
m = TOP.search(orig, mid + len(MID))
end = m.start()
span = orig[start:end]

assert span.startswith(START)
assert mid > start, "c3744 must follow c3745 for a single contiguous span"
assert span.count("- [x] **CLOSED c") == 2, "span shape unexpected -- wrong block count"
assert "CLOSED c3747" not in span and "CLOSED c3746" not in span, "floor-3 would be breached"
# c3544 is MENTIONED inside c3745's narrative ("`c3544` is not pool"); what must not be
# rotated is its own top-level DEFINITION head.  Mention vs definition, the c3747 distinction.
assert not re.search(r"^- \[[ x]\] \*\*CLOSED c3544\b", span, re.M), \
    "one-off closure DEFINITION must not be rotated"
# GUARD 1 (c3672): never swallow a top-level OPEN item.
assert not re.search(r"^- \[ \] \*\*", span, re.M), "CUT SPAN CONTAINS AN OPEN ITEM -- refusing"

# ---- GUARD 2 (c3724, widened c3748): promote nested actionables, never strand -
nested_lines = [l for l in span.split("\n") if NESTED.match(l)]
found = sorted(NESTED.match(l).group(1) for l in nested_lines)
assert found == ["3744a", "3744b"], f"unexpected nested set {found} -- re-read the span"

promoted = []
for line in nested_lines:
    body = line.strip()
    new_line = "- [ ] " + body
    # content must be byte-identical apart from the added top-level prefix
    assert new_line.endswith(body) and new_line[:6] == "- [ ] "
    promoted.append(new_line)

# ---- build the new live file in MEMORY (c3492 lesson: verify, THEN write) -----
cut = orig[:start] + orig[end:]
first_open = re.search(r"^- \[ \] \*\*", cut, re.M)
assert first_open, "no open-item region found to promote into"
ins = first_open.start()
new_queue = cut[:ins] + "\n".join(promoted) + "\n" + cut[ins:]
new_queue = re.sub(r"\n{3,}", "\n\n", new_queue)

# every nested item the span carried must now exist as a live top-level item
for key in found:
    assert re.search(r"^- \[ \] \*\*`?NEW c" + key + r"`?\b", new_queue, re.M), \
        f"NEW c{key} NOT promoted -- refusing to strand it"

archive_text = (
    "\n## Archived by cycle 3748 (CLOSED c3745 + CLOSED c3744, floor-3 rotation;\n"
    "## `NEW c3744a` and `NEW c3744b` were PROMOTED to top-level open items in\n"
    "## tasks/queue.md first -- they are kept here verbatim only as part of the record)\n\n"
    + span.rstrip("\n")
    + "\n"
)

def nb(s):
    return [l for l in s.split("\n") if l.strip()]

# nb(new) + nb(span) == nb(orig) + promoted   (span preserved verbatim in archive;
# the 2 promoted lines are the only ADDED content).  Compared BY VALUE, not `is`
# (the c3492 lesson).
assert Counter(nb(new_queue)) + Counter(nb(span)) == Counter(nb(orig)) + Counter(promoted), \
    "LOSSLESS CHECK FAILED"
assert span.rstrip("\n") in archive_text
assert "CLOSED c3745" in archive_text and "CLOSED c3744" in archive_text

open(QUEUE, "w").write(new_queue)
open(ARCHIVE, "a").write(archive_text)
print(f"OK. queue.md {len(orig)} -> {len(new_queue)} bytes (-{len(orig)-len(new_queue)})")
print(f"   rotation span {len(span)}B over 2 blocks; promoted {len(promoted)} nested item(s)")
