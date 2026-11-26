#!/root/agent/venv/bin/python
"""Cycle 3774 tasks/queue.md floor-3 rotation, in ONE in-memory build + verify + write.
Clone of _trim3748q.py BY NAME (the GUARDED multi-block-span template, index-keyed not
id-keyed, per notes/PLAYBOOK.md's explicit directive).

CUT COUNT RE-DERIVED FRESH (the c3773 handoff said "4 live CLOSED report blocks vs floor
3" -- that was already stale by the time this cycle ran: a fresh grep found the real pool
is FIVE report blocks (c3773/c3772/c3771/c3770/c3769), not four. Floor is 3 = keep newest
2 existing (c3773/c3772) plus this cycle's own block, so the correct cut is the oldest
THREE: c3771, c3770, c3769.
(c3764/c3768/c3544/c3760 are one-off ITEM closures, not in this rotation pool, per the
c3745/c3748 rule, and are left alone. `NEW c3728 -- SHIPPED c3729` is also a one-off
closure, immediately AFTER c3769's block in the file -- the span boundary below stops
right before it, confirmed by direct inspection before this script was written.)

GUARD 2 (widened c3748 regex): 0 nested `**NEW cNNNN` actionables found in the 3-block
span by direct inspection before this script was written, so no promotion step is
needed this cycle -- unlike c3748's own run.
"""
import re
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

orig = open(QUEUE).read()
TOP = re.compile(r"^- \[[ x]\] \*\*", re.M)
NESTED = re.compile(r"^\s+(?:- )?\*\*`?NEW c(\d+[a-z]?)`?\b", re.M)

# ---- derive the cut span: c3771 start -> boundary right before NEW c3728 -----
START = "- [x] **CLOSED c3771 -- QUALITY slot"
MID = "- [x] **CLOSED c3769 -- BUILD slot (3769 % 3 == 1)"
start = orig.index(START)
mid = orig.index(MID)
m = TOP.search(orig, mid + len(MID))
end = m.start()
span = orig[start:end]

assert span.startswith(START)
assert mid > start, "c3769 must follow c3771 for a single contiguous span"
assert span.count("- [x] **CLOSED c") == 3, "span shape unexpected -- wrong block count"
assert "CLOSED c3773" not in span and "CLOSED c3772" not in span, "floor-3 would be breached"
assert orig[end:end+40].startswith("- [x] **NEW c3728 -- SHIPPED c3729"), \
    "boundary drifted -- re-locate before cutting"
# one-off closures must never be swallowed by this span as a DEFINITION head
# (mentions of them in prose, e.g. this block's own grep narrative, are fine --
# the c3747 mention-vs-definition distinction).
for oneoff in ("3764", "3768", "3544", "3760"):
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
    "\n## Archived by cycle 3774 (CLOSED c3771 + CLOSED c3770 + CLOSED c3769,\n"
    "## floor-3 rotation; 0 nested actionables found, nothing to promote)\n\n"
    + span.rstrip("\n")
    + "\n"
)

def nb(s):
    return [l for l in s.split("\n") if l.strip()]

# nb(cut) + nb(span) == nb(orig)  (span removed whole, nothing added or lost).
# Compared BY VALUE, not `is` (the c3492 lesson).
assert Counter(nb(cut)) + Counter(nb(span)) == Counter(nb(orig)), "LOSSLESS CHECK FAILED"
assert span.rstrip("\n") in archive_text
assert "CLOSED c3771" in archive_text and "CLOSED c3770" in archive_text and "CLOSED c3769" in archive_text

open(QUEUE, "w").write(cut)
open(ARCHIVE, "a").write(archive_text)
print(f"OK. queue.md {len(orig)} -> {len(cut)} bytes (-{len(orig)-len(cut)})")
print(f"   rotation span {len(span)}B over 3 blocks; promoted 0 nested item(s)")
