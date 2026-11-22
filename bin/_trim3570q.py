#!/usr/bin/env python3
"""tasks/queue.md rotation trim, cycle 3570 (QUALITY slot).

Fresh per-block census off ^- \\[x\\] \\*\\*CLOSED c3\\d\\d\\d -- (BUILD|QUALITY|GROWTH) slot:
8 live report-shaped blocks, in file order: c3568, c3569, c3567, c3566, c3565,
c3564, c3563, c3562. The top-5-by-position set {c3568,c3569,c3567,c3566,c3565}
is exactly the 5 HIGHEST cycle numbers (3565-3569) -- the c3568/c3569 ordering
swap at the very top is a quirk of how c3569 inserted its closure block right
below c3568's (it was closing out the finding c3568 made), not a break in the
overall newest-at-top / oldest-at-bottom convention. So "oldest 3 in file
order" == "lowest 3 cycle numbers" == c3564, c3563, c3562, at lines 21-29,
one contiguous span (blanks at line 24, 27 are internal separators between
those 3 blocks, kept verbatim in the archived span).

Boundary: cut lines 21..30 inclusive -- i.e. swallow the span's own TRAILING
blank (line 30, c3562's separator before `NEW c3548`) so only the blank
ABOVE the cut (line 20, c3565's trailing blank) survives as the single
separator before `NEW c3548`. This is the same boundary fix c3567 recorded
(its "two consecutive blanks" bug) applied proactively.
"""
import sys

SRC = "tasks/queue.md"
ARCHIVE = "tasks/queue_archive.md"
CYCLE = 3570

with open(SRC) as f:
    orig_lines = f.readlines()

# --- boundary asserts: fail loudly if the file has drifted from what was read ---
assert orig_lines[20].startswith("- [x] **CLOSED c3564"), orig_lines[20][:80]
assert orig_lines[24].startswith("- [x] **CLOSED c3563"), orig_lines[24][:80]
assert orig_lines[27].startswith("- [x] **CLOSED c3562"), orig_lines[27][:80]
assert orig_lines[29] == "\n", repr(orig_lines[29])
assert orig_lines[30].startswith("- [ ] **NEW c3548"), orig_lines[30][:80]
assert orig_lines[19] == "\n", repr(orig_lines[19])
assert orig_lines[18].strip().startswith("- **Next (BUILD slot)"), orig_lines[18][:80]

CUT_START = 20  # 0-indexed: line 21 (c3564 header)
CUT_END = 30    # 0-indexed exclusive: up to and including line 30 (blank), i.e. python slice [20:30]

cut_span = orig_lines[CUT_START:CUT_END]
assert cut_span[0].startswith("- [x] **CLOSED c3564")
assert cut_span[-1] == "\n"
assert cut_span[-2].strip().startswith("- **NEXT (any slot)")  # c3562's trailing sub-bullet

new_live = orig_lines[:CUT_START] + orig_lines[CUT_END:]

archive_header = (
    "## Archived by cycle 3570 (from tasks/queue.md: the 3 oldest cycle-report "
    "blocks under the STANDING RULE 6b newest-5 floor -- c3564, c3563, c3562, "
    "in original file order; rotation-only lever, QUALITY slot, one contiguous span.)\n"
)

with open(ARCHIVE) as f:
    archive_orig = f.read()

new_archive_tail = archive_header + "".join(cut_span)

# --- lossless check (in memory, before any write) ---
orig_nonblank = [l for l in orig_lines if l.strip()]
new_live_nonblank = [l for l in new_live if l.strip()]
cut_nonblank = [l for l in cut_span if l.strip()]
combined = new_live_nonblank + cut_nonblank
# every original non-blank line must appear (by value) in the combined set,
# with matching multiplicity
from collections import Counter
orig_c = Counter(orig_nonblank)
combined_c = Counter(combined)
missing = orig_c - combined_c
extra = combined_c - orig_c
assert not missing, f"MISSING lines: {list(missing.items())[:3]}"
assert not extra, f"EXTRA lines: {list(extra.items())[:3]}"
print(f"Lossless check OK: {len(orig_nonblank)} non-blank original lines all accounted for.")

if "--write" in sys.argv:
    with open(SRC, "w") as f:
        f.writelines(new_live)
    with open(ARCHIVE, "a") as f:
        f.write(new_archive_tail)
    print("WROTE.")
else:
    print("DRY RUN ONLY. Pass --write to commit.")
    print(f"queue.md: {len(orig_lines)} -> {len(new_live)} lines")
    print("--- first 3 lines of new live file ---")
    print("".join(new_live[:3]))
    print("--- last 5 lines of cut span (going to archive) ---")
    print("".join(cut_span[-5:]))
    print("--- line after cut in new live file (should be NEW c3548) ---")
    print(new_live[CUT_START][:120])
