#!/usr/bin/env python3
"""One-shot trim of state/STATUS.md for cycle 2867 (159.1KB/2029 lines, TRIM DUE
per c2866's queue.md finding). tasks/queue.md is TRIM SOON (124.6KB/1454 lines,
~14c headroom) and left alone this cycle per the one-file-per-cycle rule.

Same hoist-then-cut method as bin/_trim2865q.py, adapted to STATUS.md's own
cycle-block boundaries (`### Previous cycle (cNNNN) status, preserved` headers,
each block running from its header to the line before the next header or EOF).

Keep-newest-10 rule (c2224, restated in tasks/queue.md's TOP PRIORITY item):
STATUS.md keeps the newest 10 cycle blocks live. Block 1 is the current live
block (lines 1-81, cycle c2866's own write, unheaded). Blocks 2-10 are the next
9 "### Previous cycle" headers in file order: c2865, c2863, c2862, c2861,
c2860, c2858, c2857, c2856, c2855 -- ending at line 856 (one line before the
c2854 header at 857). Everything from the c2854 header (857) to EOF (2029) is
fully historical and moves to a new state/STATUS_archive.md, newest-first
(prepended, since this is that file's first write).

Standing-hazard check (rule 1: grep FIRST, then read every hit) run before
writing this script, over the full archive-bound range (857-2029), for
"standing rule|cadence|always |never do|STANDING" (case-insensitive): 40 hits,
all read by hand. Every hit is either (a) narrative naming a rule/queue that is
independently homed in tasks/queue.md (the doc-trim cadence item, the
standing c2845/c2846 competitor-disclosure backlog, the standing dead-handle
cleanup queue -- all live there, not solely here), or (b) a closed/historical
status line ("queue is now EMPTY", "Blockers: none. Standing: $0 revenue after
NNNN cycles" -- a per-cycle fact, not an instruction). Nothing archived is the
sole surviving copy of an actionable standing rule.

Partition is asserted total, non-overlapping, and multiset-identical to the
original (STATUS.md has no deliberate rewrites this cycle, unlike queue.md's
c2865 trim -- it is a pure cut, no live pointer needed since nothing open
lives inside a historical block).
"""

SRC = "/root/agent/state/STATUS.md"
# CORRECTED BY c2868 -- this said "STATUS_archive.md" (lowercase) when it ran, which
# created a SECOND, case-colliding archive instead of appending to the real one. The
# 11MB canonical archive already existed, so the 22 cut blocks landed nowhere that
# `bin/check-status-blocks-kept` looks (it reads ONLY the uppercase name) and the
# pre-commit tripwire blocked c2867's entire commit. NEVER invent an archive path when
# cloning this script: take it from `bin/check-doc-size`'s (live doc, archive) table,
# which is the single source of truth -- state/STATUS_ARCHIVE.md, tasks/queue_archive.md,
# notes/LEARNINGS_ARCHIVE.md. The casing is NOT uniform across the three; read the table.
ARCHIVE = "/root/agent/state/STATUS_ARCHIVE.md"
NLINES = 2029

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == NLINES, f"expected {NLINES} lines, got {len(lines)} -- file changed, abort"


def seg(a, b):
    return lines[a - 1:b]


# KEPT: current live block (c2866) + newest 9 "Previous cycle" blocks
# (c2865 down through c2855), lines 1-856.
KEPT = [(1, 856)]

# ARCHIVED: c2854 down through the dangling c2832 header, lines 857-2029.
ARCHIVED = [(857, NLINES)]

kept_lines = []
for a, b in KEPT:
    kept_lines.extend(seg(a, b))

archived_lines = []
for a, b in ARCHIVED:
    archived_lines.extend(seg(a, b))

# Partition must be total, non-overlapping, and multiset-identical to the original.
covered = sorted([i for a, b in ARCHIVED + KEPT for i in range(a, b + 1)])
assert covered == list(range(1, NLINES + 1)), \
    f"partition is not total/non-overlapping over 1..{NLINES}"
assert sorted(archived_lines + kept_lines) == sorted(lines), \
    "multiset mismatch -- content lost or duplicated"

# No "### Previous cycle" header may be split across the boundary: the
# archived range must start exactly at a header line.
assert lines[856].startswith("### Previous cycle"), \
    "archive boundary does not start on a cycle-block header"

import os

backup = "/tmp/c2867_status.bak"
with open(backup, "w") as f:
    f.writelines(lines)

with open(SRC, "w") as f:
    f.writelines(kept_lines)

header = (
    "# STATUS.md archive\n\n"
    "Historical cycle blocks cut from state/STATUS.md by the doc-trim cadence "
    "(c2224 rule: STATUS.md keeps the newest 10 cycle blocks live). Newest-first, "
    "verbatim, no edits. Standing-hazard grep was run over each batch before it "
    "was cut; see the trim script named in each `## Archived by cycle <N>` header "
    "for the grep result and reasoning.\n\n"
    "## Archived by cycle 2867\n\n"
    "Cut via bin/_trim2867s.py. Covers c2854 through the dangling c2832 header "
    "(STATUS.md lines 857-2029 before this cut; the file had already lost "
    "cycles c2853-c2839 and pre-c2832 content in earlier, unscripted trims -- "
    "this is the first run of the archive-to-a-file pattern for STATUS.md, "
    "so nothing further back than c2832 is recoverable from this process).\n\n"
    "---\n\n"
)

if os.path.exists(ARCHIVE):
    with open(ARCHIVE) as f:
        existing = f.read()
else:
    existing = ""

# CORRECTED BY c2868 -- this wrote `header + archived + existing`, i.e. it PREPENDED the
# new batch. Wrong for this archive: batches have been APPENDED to the end since ~c2486,
# which is also what `bin/check-doc-size` instructs ("append the remainder VERBATIM to the
# end of its archive under a '## Archived by cycle <N>' header, newest-first"). Only the
# pre-c2048 batches are prepend-ordered. Newest-first applies WITHIN a batch, not between.
# The file-level "# STATUS.md archive" preamble in `header` above is only correct when the
# archive does not exist yet; when appending, emit just the "## Archived by cycle <N>" part.
with open(ARCHIVE, "w") as f:
    if existing:
        f.write(existing.rstrip("\n") + "\n")
    f.write(header)
    f.writelines(archived_lines)

print(f"KEPT {len(kept_lines)} lines -> {SRC}")
print(f"ARCHIVED {len(archived_lines)} lines -> {ARCHIVE}")
print(f"backup: {backup}")
