#!/usr/bin/env python3
"""QUALITY-slot trim of notes/LEARNINGS.md, cycle 3603.
Moves the OLDEST contiguous chronological body block (cycles 2864-3002,
lines 2122-3919 inclusive, 1-indexed) to the end of notes/LEARNINGS_ARCHIVE.md,
cutting DEEP (per c1976/c3388 precedent) so the file clears its own 24-cycle
check-doc-size interval with real margin, not just the warn line.
"""
import sys

LIVE = "notes/LEARNINGS.md"
ARCHIVE = "notes/LEARNINGS_ARCHIVE.md"

with open(LIVE, encoding="utf-8") as f:
    orig_text = f.read()
lines = orig_text.splitlines(keepends=True)

# 1-indexed boundaries, verified by hand above.
CUT_START = 2122  # "## c2864 ..."
CUT_END = 3919    # last line before "## c3013 ..." (line 3920)

assert lines[CUT_START - 1].startswith("## c2864"), lines[CUT_START - 1]
assert lines[CUT_END].startswith("## c3013"), lines[CUT_END]

highlights = lines[: CUT_START - 1]
archive_block = lines[CUT_START - 1 : CUT_END]
remaining_body = lines[CUT_END:]

assert archive_block[0].startswith("## c2864")

new_live_lines = highlights + remaining_body
new_live_text = "".join(new_live_lines)

header = (
    "## Archived by cycle 3603 (oldest contiguous body block, cycles 2864-3002)\n\n"
)
archive_addition = header + "".join(archive_block)

# Lossless check by VALUE with multiplicity: every non-blank line removed from
# the live file must reappear somewhere (archive addition), and every
# non-blank line that was in the original file must still be findable in
# new_live_text + archive_addition, with the same multiset of non-blank lines.
def nb(text):
    from collections import Counter

    return Counter(l for l in text.splitlines() if l.strip() != "")

orig_count = nb(orig_text)
new_count = nb(new_live_text) + nb(archive_addition)
new_count[header.strip()] -= 1  # the one intentionally-added header line
assert orig_count == new_count, "LOSSY TRIM: multiset mismatch"

with open(ARCHIVE, "a", encoding="utf-8") as f:
    f.write(archive_addition)

with open(LIVE, "w", encoding="utf-8") as f:
    f.write(new_live_text)

print(f"OK: archived {len(archive_block)} lines (cycles 2864-3002) to {ARCHIVE}")
print(f"new live line count: {len(new_live_lines)}")
