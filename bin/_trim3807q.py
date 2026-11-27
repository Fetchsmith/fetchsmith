#!/root/agent/venv/bin/python
r"""Cycle 3807 tasks/queue.md floor-3 rotation -- QUALITY slot (3807 % 3 == 0),
check-doc-size DUE (last ran c3783, 24c gap) and reading TRIM DUE at 198.9KB/
~0c headroom. Clone of _trim3804q.py BY NAME (the live descendant of the
mandated _trim3748q.py lineage), re-verified before cloning that it carries
the c3748 widened GUARD-2 regex.

CENSUS RE-DERIVED FRESH (not inherited): a per-block byte census of all 120
top-level heads in the live file found only THREE report-shaped `CLOSED
cNNNN -- ... slot` blocks, newest-to-oldest: c3804, c3803, c3802. (c3805 and
c3806 did NOT create their own top-level report blocks -- both recorded their
work inline in the standing `NEW c3372` item instead, per that item's own
convention, so there is nothing of theirs to rotate.) Floor 3 (STANDING
c3280 / c3672 cadence) = keep newest 2 (c3804, c3803) + this cycle's own
block, so the cut is the single c3802 block. This yields less headroom than
a typical 5-8 block cut (c3804 harvested 8 blocks down to this same floor),
confirming the STANDING c3280 "equilibrium" note: the report-block lever is
nearly exhausted again already. The next QUALITY slot's census should look
at the big standing NEW items (c3162 13.2KB, FOLD-IN REGISTER 8.9KB -- but
note c3795a already ruled FOLD-IN REGISTER and COMPRESSED c2994 NOT
relocatable, live data registers) per PLAYBOOK's "ask whether the biggest
block is even a task" lesson, not just report blocks again.

HAZARD GREP (3-pass, run before this script was written):
(a)/(b) whole-repo grep for `c3802\b` outside queue.md/queue_archive.md
    found only: bin/_trim3804q.py (self-contained docstring citing c3802 as
    history, needs no queue.md narrative to resolve) and state/STATUS.md
    (two self-contained per-cycle entries citing c3802 as history/context,
    same pattern). Nothing to relocate.
(c) intra-file: no `NEW cNNNNa`-shaped nested sub-bullet exists inside the
    c3802 block (checked by direct read: all indented lines are plain
    narrative, no `- **NEW c...` nested bullet). GUARD 2 below re-asserts
    this by script so a drifted boundary cannot cut a different block
    cosmetically.
Live "git log ... names c3802" / "ctriolab/ats-jobs-feed ... c3802" mentions
in the kept c3803/c3804 blocks are backward narrative references to a cycle
number in passing, not "see CLOSED c3802 above" pointers -- NEW c3492's
standing ruling already covers this shape (resolves in queue_archive.md).
"""
import re
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

orig = open(QUEUE).read()
NESTED = re.compile(r"^\s+(?:- )?\*\*`?NEW c(\d+[a-z]?)`?\b", re.M)
RESOLVED_NEARBY = re.compile(r"`?NEW c\d+[a-z]?`?\s*(?:--\s*)?(CLOSED|SHIPPED|RESOLVED)\b")

SPAN_START = "- [x] **CLOSED c3802 -- BUILD slot (3802 % 3 == 1)"
SPAN_NEXT = "- [x] **CLOSED c3792 -- the overdue `tasks/queue.md` trim this item flagged HIGH"

start = orig.index(SPAN_START)
end = orig.index(SPAN_NEXT)
span = orig[start:end]

# --- boundary asserts: a drifted line must fail loudly, never cut the wrong place ---
assert orig.count(SPAN_START) == 1 and orig.count(SPAN_NEXT) == 1
assert start < end
assert span.count("\n- [x] **CLOSED c") + 1 == 1, \
    f"span block count unexpected: {span.count(chr(10) + '- [x] **CLOSED c') + 1}"
assert "CLOSED c3804" not in span and "CLOSED c3803" not in span
# c3748 lesson: anchor to a top-level HEAD, never bare narrative text.
assert not re.search(r"^- \[[ x]\] \*\*CLOSED c3792 --", span, re.M)

# --- GUARD 1: span holds no open item ---
assert not re.search(r"^- \[ \] \*\*", span, re.M), "SPAN CONTAINS AN OPEN ITEM -- refusing"

# --- GUARD 2 (c3724/c3748): promote nested actionables, never strand -------------
nested = [l for l in span.split("\n") if NESTED.match(l)]
live = [l for l in nested if not RESOLVED_NEARBY.search(l)]
found = sorted(NESTED.match(l).group(1) for l in live)
assert found == [], f"unexpected nested set {found} -- promotion needed"

# --- build the new live file in MEMORY (verify, THEN write) ----------------------
new_text = orig[:start] + orig[end:]

archive_text = (
    "\n## Archived by cycle 3807 (floor-3 report-block rotation, single-block span --\n"
    "## the report-block lever was already nearly exhausted by c3804's deep cut; only\n"
    "## ONE block, CLOSED c3802, was above the keep-newest-2 floor this time. 0 nested\n"
    "## actionables found, nothing to promote. Live \"c3802\" mentions elsewhere in the\n"
    "## file are backward narrative references, not dependent pointers -- NEW c3492's\n"
    "## standing ruling covers this shape.)\n\n"
    + span.rstrip("\n") + "\n"
)

def nb(s):
    return [l for l in s.split("\n") if l.strip()]

# nb(new) + nb(removed) == nb(orig)  (compare BY VALUE)
removed = Counter(nb(span))
assert Counter(nb(new_text)) + removed == Counter(nb(orig)), \
    "LOSSLESS CHECK FAILED -- nothing written"
assert span.rstrip("\n") in archive_text
assert "c3802" in archive_text
# the kept blocks must still head the live file (anchor to actual top-level HEADS,
# not bare substrings -- c3804's own narrative mentions "the `CLOSED c3792` line
# right above it said so" in passing, which is not the real c3792 head)
def head_idx(cyc):
    m = re.search(rf"^- \[[ x]\] \*\*CLOSED c{cyc}\b", new_text, re.M)
    assert m, f"no top-level head found for c{cyc}"
    return m.start()
assert head_idx("3804") < head_idx("3803") < head_idx("3792")

with open(ARCHIVE, "a") as fh:
    fh.write(archive_text)
with open(QUEUE, "w") as fh:
    fh.write(new_text)

print(f"queue.md {len(orig):,}B -> {len(new_text):,}B  ({len(new_text) - len(orig):+,}B)")
print(f"lines {orig.count(chr(10)):,} -> {new_text.count(chr(10)):,}")
print(f"archived {len(archive_text):,}B under '## Archived by cycle 3807'")
