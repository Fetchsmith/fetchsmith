#!/root/agent/venv/bin/python
"""Cycle 3783 tasks/queue.md floor-3 rotation, in ONE in-memory build + verify + write.
Clone of _trim3774q.py BY NAME, which is itself a clone of _trim3748q.py (the GUARDED
multi-block-span template, index-keyed not id-keyed, per notes/PLAYBOOK.md's explicit
directive).

CUT COUNT RE-DERIVED FRESH (c3782's forwarded number was never trusted): a fresh grep of
`^- \\[x\\] \\*\\*CLOSED c(\\d+)` found 11 heads. Classifying each by shape (report block --
"-- BUILD slot"/"-- QUALITY slot" immediately after the cycle number -- vs one-off ITEM
closure): 7 are report blocks (c3782/c3779/c3778/c3777/c3774/c3773/c3772) and 4 are one-off
ITEM closures (`CLOSED c3764 (was NEW c3760)`, `CLOSED c3768 (was NEW c3764)`,
`CLOSED c3778 (was NEW c3620)` -- a DUPLICATE cycle-id with the c3778 report block, same
known collision class as c3764/c3768's prior duplicate, `CLOSED c3544 (DONE c3720)`,
`CLOSED c3760 (was NEW c3458)`, `CLOSED c3780 (was NEW c3523)`, `CLOSED c3781 (was NEW
follow-up c2873)` -- the last two have no separate "-- BUILD/QUALITY slot" report block
anywhere in the file; their cycles' queue.md record IS the one-off closure).

Floor 3 = keep newest 2 report blocks (c3782, c3779) + this cycle's own block, so the
correct cut is the oldest 5 report blocks: c3778, c3777, c3774, c3773, c3772, one
contiguous span. (All 4 one-off closures sit AFTER this span in the file, past the
`NEW c3728 -- SHIPPED c3729` one-off block that the span boundary stops before, so none
of them are at risk of being swallowed.)

GUARD 2 (widened c3748 regex): 0 nested `**NEW cNNNN` actionables found in the 5-block
span by direct inspection before this script was written (every indented continuation
line starts with a narrative bold lead-in -- "Tried", "Pivoted", "A fresh grep",
"Pointer re-verified", "Batch", "Bucket-7", etc. -- never `NEW c<digits>`), so no
promotion step is needed this cycle.
"""
import re
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

orig = open(QUEUE).read()
TOP = re.compile(r"^- \[[ x]\] \*\*", re.M)
NESTED = re.compile(r"^\s+(?:- )?\*\*`?NEW c(\d+[a-z]?)`?\b", re.M)

# ---- derive the cut span: c3778 report start -> boundary right before NEW c3728 ----
START = "- [x] **CLOSED c3778 -- BUILD slot (3778 % 3 == 1)"
MID = "- [x] **CLOSED c3772 -- BUILD slot (3772 % 3 == 1)"
start = orig.index(START)
mid = orig.index(MID)
m = TOP.search(orig, mid + len(MID))
end = m.start()
span = orig[start:end]

assert span.startswith(START)
assert mid > start, "c3772 must follow c3778 for a single contiguous span"
assert span.count("- [x] **CLOSED c") == 5, "span shape unexpected -- wrong block count"
assert "CLOSED c3782" not in span and "CLOSED c3779" not in span, "floor-3 would be breached"
assert orig[end:end+40].startswith("- [x] **NEW c3728 -- SHIPPED c3729"), \
    "boundary drifted -- re-locate before cutting"
# one-off closures must never be swallowed by this span as a DEFINITION head
# (mentions of them in prose, e.g. this block's own grep narrative, are fine --
# the c3747 mention-vs-definition distinction).
for oneoff in ("3764", "3768", "3544", "3760", "3780", "3781"):
    assert not re.search(r"^- \[[ x]\] \*\*CLOSED c" + oneoff + r"\b", span, re.M), \
        f"CLOSED c{oneoff} DEFINITION must not be rotated"
# GUARD 1 (c3672): never swallow a top-level OPEN item.
assert not re.search(r"^- \[ \] \*\*", span, re.M), "CUT SPAN CONTAINS AN OPEN ITEM -- refusing"

# ---- GUARD 2 (c3724, widened c3748): promote nested actionables, never strand -
nested_lines = [l for l in span.split("\n") if NESTED.match(l)]
found = sorted(NESTED.match(l).group(1) for l in nested_lines)
assert found == [], f"unexpected nested set {found} -- re-read the span, promotion needed"

# ---- build the new live file in MEMORY (c3492 lesson: verify, THEN write) -----
cut = orig[:start] + orig[end:]

archive_text = (
    "\n## Archived by cycle 3783 (CLOSED c3778 + CLOSED c3777 + CLOSED c3774 +\n"
    "## CLOSED c3773 + CLOSED c3772, floor-3 rotation; 0 nested actionables found,\n"
    "## nothing to promote)\n\n"
    + span.rstrip("\n")
    + "\n"
)

def nb(s):
    return [l for l in s.split("\n") if l.strip()]

# nb(cut) + nb(span) == nb(orig)  (span removed whole, nothing added or lost).
# Compared BY VALUE, not `is` (the c3492 lesson).
assert Counter(nb(cut)) + Counter(nb(span)) == Counter(nb(orig)), "LOSSLESS CHECK FAILED"
assert span.rstrip("\n") in archive_text
for cyc in ("3778", "3777", "3774", "3773", "3772"):
    assert f"CLOSED c{cyc}" in archive_text

open(QUEUE, "w").write(cut)
open(ARCHIVE, "a").write(archive_text)
print(f"OK. queue.md {len(orig)} -> {len(cut)} bytes (-{len(orig)-len(cut)})")
print(f"   rotation span {len(span)}B over 5 blocks; promoted 0 nested item(s)")
