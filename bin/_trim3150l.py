#!/usr/bin/env python3
"""One-shot LEARNINGS.md trim for cycle 3150 (QUALITY slot, 3150 % 3 == 0).

check-doc-size showed notes/LEARNINGS.md TRIM DUE on PROJECTION (7538 lines,
8018 forecast at the next 24c look vs the 8000 cap) -- the DEEP-cut shape,
not the minimal-clear shape: move the OLDEST contiguous block of the
chronological body (never the newest-first highlights block at the top) to
the end of LEARNINGS_ARCHIVE.md, cut deep enough to clear the next look with
real margin (c1976 precedent: a shallow first cut to 7604 read WARN
instantly; recut to 5928). Target here is ~5900 lines.

The highlights block (newest-first, "## Cycle 3144" down to "## Cycle 841")
runs lines 1-1584; the chronological body (forward order) begins at line
1585 ("## Cycle 2588") and runs to the end. The oldest contiguous span of
that body sized to hit the ~5900 target is lines 1585-3243 (1659 lines,
"## Cycle 2588" through the blank line right before "## c2724 -- two harness
gotchas that each manufacture a false reading"), landing at 5879 live lines.

Self-verifying: cut + before + after reconstructs the original exactly
(line-for-line, no loss, no duplication, no reorder).

Dry-run by default; pass --write to apply.
"""
import sys

LEARNINGS = "/root/agent/notes/LEARNINGS.md"
ARCHIVE = "/root/agent/notes/LEARNINGS_ARCHIVE.md"

with open(LEARNINGS) as f:
    lines = f.readlines()

CUT_START = 1585  # 1-indexed, inclusive ("## Cycle 2588" header)
CUT_END = 3243    # 1-indexed, inclusive (blank line right before "## c2724 -- two harness gotchas")

assert lines[CUT_START - 1].startswith("## Cycle 2588"), lines[CUT_START - 1]
assert lines[CUT_START - 2].strip() == "", lines[CUT_START - 2]
assert lines[CUT_END - 1].strip() == "", lines[CUT_END - 1]
assert lines[CUT_END].startswith("## c2724 — two harness gotchas"), lines[CUT_END]

before = lines[:CUT_START - 1]
cut = lines[CUT_START - 1:CUT_END]
after = lines[CUT_END:]

assert before + cut + after == lines, "cut block is not contiguous / not where expected"

live_after = before + after

header = "\n## Archived by cycle 3150 (oldest contiguous body block, cycles 2588-2724)\n\n"

print(f"cutting {len(cut)} lines (cycles 2588-2724) from {LEARNINGS}")
print(f"live: {len(lines)} -> {len(live_after)} lines")

if "--write" in sys.argv:
    with open(ARCHIVE, "a") as f:
        f.write(header)
        f.writelines(cut)
    with open(LEARNINGS, "w") as f:
        f.writelines(live_after)
    print("WROTE notes/LEARNINGS.md, notes/LEARNINGS_ARCHIVE.md")
else:
    print("DRY RUN ok -- re-run with --write to apply")
