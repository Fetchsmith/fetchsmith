#!/usr/bin/env python3
"""QUALITY-slot rotation of tasks/queue.md, cycle 3603.
RULE 6b floor: keep the newest 5 contiguous `CLOSED cNNNN` report blocks,
archive the rest verbatim to tasks/queue_archive.md. Fresh census found 8
live blocks (c3602..c3595); floor-5 makes the oldest 3 (c3597, c3596, c3595,
lines 31-43 inclusive, which ends with the `---` that followed c3595)
rotatable. After the cut, c3598's own trailing `---` (line 29) becomes the
seam directly before the `NEW c3598 -- CLOSED at c3602` pointer line.
"""
from collections import Counter

LIVE = "tasks/queue.md"
ARCHIVE = "tasks/queue_archive.md"

with open(LIVE, encoding="utf-8") as f:
    orig_text = f.read()
lines = orig_text.splitlines(keepends=True)

CUT_START = 31  # "- [x] **CLOSED c3597 ..."
CUT_END = 43    # "---" that followed c3595's block

assert lines[CUT_START - 1].startswith("- [x] **CLOSED c3597")
assert lines[CUT_END - 1].strip() == "---"
assert lines[CUT_END].strip() == ""  # blank line 44, kept
assert lines[CUT_END + 1].startswith("- [x] **NEW c3598")

before = lines[: CUT_START - 1]
archive_block = lines[CUT_START - 1 : CUT_END]
after = lines[CUT_END:]

new_live_lines = before + after
new_live_text = "".join(new_live_lines)

header = "## Archived by cycle 3603\n\n"
archive_addition = header + "".join(archive_block)


def nb(text):
    return Counter(l for l in text.splitlines() if l.strip() != "")


orig_count = nb(orig_text)
new_count = nb(new_live_text) + nb(archive_addition)
new_count[header.strip()] -= 1  # the one intentionally-added header line
assert orig_count == new_count, "LOSSY TRIM: multiset mismatch"

with open(ARCHIVE, "a", encoding="utf-8") as f:
    f.write(archive_addition)

with open(LIVE, "w", encoding="utf-8") as f:
    f.write(new_live_text)

print(f"OK: archived {len(archive_block)} lines (c3597, c3596, c3595) to {ARCHIVE}")
print(f"new live line count: {len(new_live_lines)}")
