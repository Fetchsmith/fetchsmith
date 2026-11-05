#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2757 (87.0KB / 982 lines, TRIM SOON).

check-doc-size read TRIM SOON this cycle (87.0KB/982 lines, ~21 cycles of headroom at
+5440 B/cycle, projected 215KB at next automatic look in 24c). c2756 explicitly named 2757
as the next QUALITY slot and the designated place to trim both STATUS.md and queue.md.

Hoist-then-cut (the standing method, same shape as c2745's trim): a contiguous run of 6
DONE blocks (c2752/c2753/c2754/c2755/old-closed-c2752-narrative/c2746) sits at lines
54-160, sandwiched between the live c2756 HIGH item (lines 1-53) and the resumption of
open items at line 161 (c2744 LOW note). A naive "keep first N lines" cut would either
destroy the live c2756 item (if N<54) or keep stale DONE blocks (if N>160) -- so this cuts
exactly the DONE range and leaves everything else untouched, regardless of position.

Hazard grep (rule 1) run first over the archive-bound range (lines 54-159): one hit
("house style" at former line 79, inside the OLD/closed c2752 narrative) -- read in context,
it is a reference to an already-established convention (dated correction banners on blog
posts), not a new standing rule, so no rescue needed.

Structure at 2757: line 1 = open item start; lines 54-159 = 6 contiguous DONE blocks (`- [x]`),
line 160 blank; line 161 = next open item start. Archive lines 54-159 verbatim; keep 1-53
and 160-end.
"""
import sys

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
ARCHIVE_START = 54   # 1-indexed, inclusive
ARCHIVE_END = 159     # 1-indexed, inclusive

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 982, f"expected 982 lines, got {len(lines)} -- file changed, abort"

# Sanity-check the exact boundary this script assumes.
assert lines[ARCHIVE_START - 1].startswith("- [x] **DONE c2752"), \
    f"line {ARCHIVE_START} is not the expected DONE block start: {lines[ARCHIVE_START-1]!r}"
assert lines[ARCHIVE_END - 1].strip().endswith("for this slug."), \
    f"line {ARCHIVE_END} is not the expected DONE block end: {lines[ARCHIVE_END-1]!r}"
assert lines[ARCHIVE_END].strip() == "", "expected a blank separator line after the DONE range"
assert lines[ARCHIVE_END + 1].startswith("- [ ] **NEW note (c2744, LOW"), \
    f"line {ARCHIVE_END+2} is not the expected next open item: {lines[ARCHIVE_END+1]!r}"

before = lines[:ARCHIVE_START - 1]
archived = lines[ARCHIVE_START - 1:ARCHIVE_END]
after = lines[ARCHIVE_END:]

keep = before + after
keep_txt = "".join(keep)
archived_txt = "".join(archived)

if "".join(before) + archived_txt + "".join(after) != "".join(lines):
    sys.exit("FAIL: before + archived + after does not reconstruct the original file")

with open(ARCHIVE) as f:
    old_archive = f.read()

addition = (
    f"\n## Archived at cycle 2757 (queue.md trim, `bin/_trim2757q.py`) -- "
    f"6 DONE blocks (c2752/c2753/c2754/c2755/old-closed/c2746)\n\n" + archived_txt
)
new_archive = old_archive + addition

for ln in archived:
    if ln.strip() and ln not in addition:
        sys.exit(f"FAIL: archived line missing from addition: {ln[:90]!r}")

if not (len(keep_txt) < len("".join(lines))):
    sys.exit("FAIL: new queue.md is not strictly smaller")
if not (len(new_archive) > len(old_archive)):
    sys.exit("FAIL: archive did not grow")

open_before = sum(1 for l in lines if l.startswith("- [ ]"))
open_after = sum(1 for l in keep if l.startswith("- [ ]"))
if open_before != open_after:
    sys.exit(f"FAIL: open item count changed {open_before} -> {open_after}")

with open(SRC, "w") as f:
    f.write(keep_txt)
with open(ARCHIVE, "w") as f:
    f.write(new_archive)

print(f"queue.md: {len(lines)} -> {len(keep_txt.splitlines())} lines "
      f"({len(''.join(lines))} -> {len(keep_txt)} bytes)")
print(f"Archived {len(archived)} lines to {ARCHIVE}")
print(f"Open items before/after: {open_before}/{open_after}")
