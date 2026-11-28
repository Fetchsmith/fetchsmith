#!/root/agent/venv/bin/python
"""QUALITY-slot trim of notes/LEARNINGS.md, cycle 3852.
check-doc-size reads it TRIM DUE at 7592/8000 lines with ~20 cycles of headroom
against its own 24-cycle interval -- i.e. it would be WARN again before the next
look. Per the c1976/c3388/c3603 precedent, cut DEEP rather than shaving to the
line: move the OLDEST contiguous chronological body block to the END of
notes/LEARNINGS_ARCHIVE.md, leaving the newest-first highlights block (lines
1-2635) untouched.

Boundary re-derived fresh this cycle: the chronological body starts at line 2636
(`## c3013`). Cut cycles c3013..c3172 -- lines 2636-4660 inclusive (1-indexed),
2025 lines, ending at the last line before `## c3312` on line 4661. Leaves 5567
lines live (2433 lines of headroom at +20 lines/cycle, ~100+ cycles), comparable
to c3603's 5794 and c1976's 5928 recut.
"""
from collections import Counter

LIVE = "/root/agent/notes/LEARNINGS.md"
ARCHIVE = "/root/agent/notes/LEARNINGS_ARCHIVE.md"

with open(LIVE, encoding="utf-8") as f:
    orig_text = f.read()
lines = orig_text.splitlines(keepends=True)

assert len(lines) == 7592, f"unexpected line count {len(lines)} -- re-derive boundary"

CUT_START = 2636  # "## c3013 ..."  (first line of the chronological body)
CUT_END = 4660    # last line before "## c3312 ..." on line 4661

assert lines[CUT_START - 1].startswith("## c3013"), lines[CUT_START - 1][:80]
assert lines[CUT_END].startswith("## c3312"), lines[CUT_END][:80]

highlights = lines[: CUT_START - 1]
archive_block = lines[CUT_START - 1 : CUT_END]
remaining_body = lines[CUT_END:]

new_live_text = "".join(highlights + remaining_body)

header = "## Archived by cycle 3852 (oldest contiguous body block, cycles 3013-3172)\n\n"
archive_addition = header + "".join(archive_block)


def nb(text):
    return Counter(l for l in text.splitlines() if l.strip() != "")


orig_count = nb(orig_text)
new_count = nb(new_live_text) + nb(archive_addition)
new_count[header.strip()] -= 1  # the one intentionally-added header line
assert orig_count == new_count, "LOSSY TRIM: multiset mismatch -- nothing written"

with open(ARCHIVE, "a", encoding="utf-8") as f:
    f.write(archive_addition)

with open(LIVE, "w", encoding="utf-8") as f:
    f.write(new_live_text)

print(f"OK: archived {len(archive_block)} lines (cycles 3013-3172) to {ARCHIVE}")
print(f"new live line count: {len(highlights) + len(remaining_body)}")
