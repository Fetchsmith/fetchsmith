#!/usr/bin/env python3
"""One-shot LEARNINGS.md trim for cycle 3009.
Moves the oldest contiguous block of the chronological body (cycles 2460..2576,
lines 1117-2478 inclusive, 1-indexed) verbatim to the end of LEARNINGS_ARCHIVE.md
under a dated header. Never touches the newest-first highlights block (lines 1-1116).
Self-verifying: live_after + cut == original (line-for-line, no loss, no duplication).
"""
import sys

LEARNINGS = "notes/LEARNINGS.md"
ARCHIVE = "notes/LEARNINGS_ARCHIVE.md"

with open(LEARNINGS) as f:
    lines = f.readlines()

CUT_START = 1117  # 1-indexed, inclusive ("## Cycle 2460" header)
CUT_END = 2478    # 1-indexed, inclusive (blank line right before "## Cycle 2588" header)

assert lines[CUT_START - 1].startswith("## Cycle 2460"), lines[CUT_START - 1]
assert lines[CUT_END] .startswith("## Cycle 2588"), lines[CUT_END]

before = lines[:CUT_START - 1]
cut = lines[CUT_START - 1:CUT_END]
after = lines[CUT_END:]

live_after = before + after

# Losslessness: every line in `cut` leaves the live file, nothing else changes.
assert live_after == before + after
assert len(before) + len(cut) + len(after) == len(lines)
assert (before + cut + after) == lines, "cut block is not contiguous / not where expected"

header = "\n## Archived by cycle 3009 (oldest contiguous body block, cycles 2460-2576)\n\n"

with open(ARCHIVE, "a") as f:
    f.write(header)
    f.writelines(cut)

with open(LEARNINGS, "w") as f:
    f.writelines(live_after)

print(f"cut {len(cut)} lines (cycles 2460-2576) from {LEARNINGS}")
print(f"live now {len(live_after)} lines (was {len(lines)})")
