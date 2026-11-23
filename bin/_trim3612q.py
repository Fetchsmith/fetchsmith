#!/usr/bin/env python3
"""QUALITY-slot trim of tasks/queue.md, cycle 3612. Clone of bin/_trim3603q.py,
extended to multi-span (the floor-5 rotation alone was only 12.4KB against a
203.1KB file at ~0 cycles of headroom, so it is paired with a dead-item
retirement exactly as c3611's handoff and the PLAYBOOK cadence call for).

Fresh census (never forwarded): 8 contiguous `CLOSED cNNNN` REPORT blocks live
(c3611..c3604). RULE 6b floor keeps the newest 5 (c3611..c3607); c3606/c3605/
c3604 rotate (lines 31-45, 12,431B).

Paired retirement -- 4 blocks that are CLOSED/DONE and carry no open work:
  46-47  `NEW c3598 -- CLOSED at c3602`      231B  (dead pointer)
  48-49  `CLOSED c3593` depth-cap sweep    3,885B  (method is already in
         notes/LEARNINGS.md:5782-5798, verified before cutting)
  54-55  `CLOSED c3604 (was NEW c3548)`    4,054B  (shipped 0.1.38/build 0.1.97)
  447-457 `CLOSED c3496`                     910B  (ack mechanism shipped)

Hazard grep, all three passes, run before writing:
  (a)/(b) external: only dead `bin/_trimNNNN*.py` scripts plus narrative in
      state/STATUS.md and tasks/queue_archive.md -- the known-false-positive
      class this check has returned for ~25 trims.
  (c) intra-file: c3593 -> self only; c3598 -> line 31 (itself being archived)
      + self; c3496 -> self only; c3548/c3601-pagination -> lines 43/54 (both
      archived) and line 19 (c3608's block, a narrative mention, not a pointer).
Clean.
"""
from collections import Counter

LIVE = "tasks/queue.md"
ARCHIVE = "tasks/queue_archive.md"

with open(LIVE, encoding="utf-8") as f:
    orig_text = f.read()
lines = orig_text.splitlines(keepends=True)

# (start, end) 1-indexed inclusive, plus the head text each span must open with.
SPANS = [
    (31, 49, "- [x] **CLOSED c3606"),   # c3606, c3605, c3604 reports + c3598 + c3593
    (54, 55, "- [x] **CLOSED c3604 (was `NEW c3548`"),
    (447, 457, "- [x] **CLOSED c3496"),
]

for start, end, head in SPANS:
    assert lines[start - 1].startswith(head), f"boundary drift at line {start}"
    assert lines[end - 1].strip() == "", f"span {start}-{end} must end on a blank"
    assert lines[end].startswith("- ["), f"line {end + 1} must be the next item head"

# Seam asserts for the rotation span specifically.
assert lines[28].strip() == "---"        # line 29, c3607's trailing seam, kept
assert lines[29].strip() == ""           # line 30, kept as the separator
assert lines[49].startswith("- [ ] **NEW c3589")   # line 50, first survivor

cut_blocks = []
keep = []
cut_set = set()
for start, end, _ in SPANS:
    cut_set.update(range(start, end + 1))
for n, line in enumerate(lines, 1):
    (cut_blocks if n in cut_set else keep).append(line)

new_live_text = "".join(keep)

header = "## Archived by cycle 3612\n\n"
archive_addition = header + "".join(cut_blocks)


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

before = len(orig_text.encode())
after = len(new_live_text.encode())
print(f"OK: archived {len(cut_blocks)} lines across {len(SPANS)} spans to {ARCHIVE}")
print(f"{before} B / {len(lines)} ln  ->  {after} B / {len(keep)} ln  (-{before - after} B)")
