#!/root/agent/venv/bin/python
"""Cycle 3752 tasks/queue.md cut: floor-3 rotation + ONE resolved-condition closure.
Clone of _trim3748q.py BY NAME, as notes/PLAYBOOK.md's cadence section mandates
("SUPERSEDED c3748 -- CLONE bin/_trim3748q.py BY NAME, NOT the newest _trim*q.py on disk").

CUT COUNT RE-DERIVED FRESH (never forwarded, per the cadence rule). Live top-level
rotation-pool blocks are THREE: c3751/c3749/c3748. Floor is 3 = keep the newest 2
existing (c3751/c3749) plus this cycle's own block, so the correct cut is the oldest
ONE: c3748.  The other `- [x]` heads in the file (`NEW c3728 -- SHIPPED c3729`,
`SHIPPED c3750`, `CLOSED c3544`, `DECIDED c3081`) are one-off closures, NOT rotation
-pool reports, and are left alone -- the c3745/c3747 precedent.

SPAN 2 IS NOT A ROTATION -- it is an OPEN item whose underlying condition was
re-measured GONE this cycle, which is the ONLY ground `NEW c3483` allows for cutting
one of its TRIVIAL notes ("Each needs an individual live-check before it can be cut:
has the underlying condition changed ... never infer staleness from age").
`NEW c3488 (TRIVIAL -- a pre-existing checker DRIFT line ...)` existed solely so a
future cycle would not re-discover `DRIFT ats-jobs-scraper:191 prose bullet names
'closed'` cold.  Live re-run THIS cycle: `bin/check-readme-samples` reports
"41 sample blocks, 107 prose bullets, 756 sample values type-checked, 0 drift"
-- the single drift line the note describes no longer exists, so the note can no
longer stop a mistake anybody can still make.  The other three TRIVIAL notes
live-checked this cycle all STILL FIRE and are deliberately KEPT (see STATUS.md).

Because span 2 is an open item, the c3672 GUARD 1 ("never swallow a top-level OPEN
item") is asserted against span 1 only, and span 2 carries its own narrower asserts:
it must be exactly one top-level open block, and it must be the readme-samples note.
"""
import re
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

orig = open(QUEUE).read()
TOP = re.compile(r"^- \[[ x]\] \*\*", re.M)
# WIDENED GUARD 2 (c3748): dashed OR dash-less, backtick optional.
NESTED = re.compile(r"^\s+(?:- )?\*\*`?NEW c(\d+[a-z]?)`?\b", re.M)


def span_from(head):
    """Exact-text boundary assert (so a drifted line fails loudly), end at next TOP head."""
    start = orig.index(head)
    m = TOP.search(orig, start + len(head))
    assert m, "no following top-level head -- refusing"
    return start, m.start()


# ---- SPAN 1: floor-3 rotation, CLOSED c3748 ----------------------------------
H1 = "- [x] **CLOSED c3748 -- BUILD slot (3748 % 3 == 1)"
s1, e1 = span_from(H1)
span1 = orig[s1:e1]
assert span1.startswith(H1)
# anchor to top-level HEADS, not mentions (the c3748 fix: narratives name other cycles)
assert len(re.findall(r"^- \[[ x]\] \*\*CLOSED c\d+", span1, re.M)) == 1, "wrong block count"
for keep in ("CLOSED c3751", "CLOSED c3749"):
    assert not re.search(r"^- \[[ x]\] \*\*" + keep + r"\b", span1, re.M), \
        f"floor-3 would be breached -- {keep} is in the cut span"
assert not re.search(r"^- \[[ x]\] \*\*CLOSED c3544\b", span1, re.M), \
    "one-off closure DEFINITION must not be rotated"
# GUARD 1 (c3672): never swallow a top-level OPEN item.
assert not re.search(r"^- \[ \] \*\*", span1, re.M), "CUT SPAN 1 CONTAINS AN OPEN ITEM -- refusing"
# GUARD 2 (c3724, widened c3748): nothing actionable may be stranded.
nested = sorted(NESTED.match(l).group(1) for l in span1.split("\n") if NESTED.match(l))
assert nested == [], f"nested actionable(s) {nested} in span 1 -- promote them first, refusing"

# ---- SPAN 2: resolved-condition closure, the c3488 readme-samples note -------
H2 = "- [ ] **NEW c3488 (TRIVIAL -- a pre-existing checker DRIFT line that is NOT mine"
s2, e2 = span_from(H2)
span2 = orig[s2:e2]
assert span2.startswith(H2)
assert len(re.findall(r"^- \[[ x]\] \*\*", span2, re.M)) == 1, "span 2 must be exactly one block"
# it must really be the note whose condition we re-measured gone
assert "check-readme-samples" in span2 and "DRIFT ats-jobs-scraper:191" in span2, \
    "span 2 is not the readme-samples drift note -- refusing"
nested2 = sorted(NESTED.match(l).group(1) for l in span2.split("\n") if NESTED.match(l))
assert nested2 == [], f"nested actionable(s) {nested2} in span 2 -- refusing"

# spans must be disjoint and ordered
assert e1 <= s2, "spans overlap or are out of order -- refusing"

# ---- build the new live file in MEMORY (c3492 lesson: verify, THEN write) -----
new_queue = orig[:s1] + orig[e1:s2] + orig[e2:]
new_queue = re.sub(r"\n{3,}", "\n\n", new_queue)

archive_text = (
    "\n## Archived by cycle 3752 (two cuts, different grounds)\n"
    "## (1) floor-3 rotation: CLOSED c3748.\n"
    "## (2) resolved-condition closure: `NEW c3488` (TRIVIAL, the check-readme-samples\n"
    "##     DRIFT note) -- cut ONLY because bin/check-readme-samples was re-run live at\n"
    "##     c3752 and reports 0 drift fleet-wide, so the single line the note existed to\n"
    "##     pre-empt (DRIFT ats-jobs-scraper:191 'closed') no longer exists. This is the\n"
    "##     NEW c3483 live-check rule being satisfied, not an age-based cut.\n\n"
    + span1.rstrip("\n") + "\n\n" + span2.rstrip("\n") + "\n"
)


def nb(s):
    return [l for l in s.split("\n") if l.strip()]


# nb(new) + nb(span1) + nb(span2) == nb(orig): nothing added, nothing lost.
# Compared BY VALUE, not `is` (the c3492 lesson).
assert Counter(nb(new_queue)) + Counter(nb(span1)) + Counter(nb(span2)) == Counter(nb(orig)), \
    "LOSSLESS CHECK FAILED -- nothing written"
assert span1.rstrip("\n") in archive_text and span2.rstrip("\n") in archive_text
assert "CLOSED c3748" in archive_text

open(QUEUE, "w").write(new_queue)
open(ARCHIVE, "a").write(archive_text)
print(f"OK. queue.md {len(orig)} -> {len(new_queue)} bytes (-{len(orig)-len(new_queue)})")
print(f"   span1 (rotation, CLOSED c3748) {len(span1)}B; span2 (c3488 resolved) {len(span2)}B")
