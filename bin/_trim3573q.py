#!/usr/bin/env python3
"""tasks/queue.md rotation trim, cycle 3573 (QUALITY slot).

Fresh per-block census off ^- \\[x\\] \\*\\*CLOSED c3\\d\\d\\d -- (BUILD|QUALITY|GROWTH) slot:
8 live report-shaped blocks, in file order: c3572, c3571, c3570, c3568, c3569,
c3567, c3566, c3565. Top-5-by-file-position = {c3572,c3571,c3570,c3568,c3569}
= cycles {3572,3571,3570,3568,3569}, which is exactly the 5 HIGHEST cycle
numbers -- position==chronology holds again this time (verified explicitly,
per the c3570 lesson, not assumed). So "oldest 3 by file position" ==
"lowest 3 cycle numbers" == c3567, c3566, c3565, one contiguous span at
lines 34-42 (inclusive), each CLOSED block immediately followed by its own
"Next (...)" sub-bullet and a trailing blank separator.

Boundary: cut lines 34..42 inclusive (0-indexed slice [33:42]) -- swallow
the span's own TRAILING blank (line 42, c3565's separator before `NEW
c3548`) so only the blank ABOVE the cut (line 33, c3567's leading
separator, itself c3569's trailing blank) survives before `NEW c3548`.
Same boundary rule c3567/c3570 used.
"""
import sys
from collections import Counter

SRC = "tasks/queue.md"
ARCHIVE = "tasks/queue_archive.md"
CYCLE = 3573

with open(SRC) as f:
    orig_lines = f.readlines()

# --- boundary asserts: fail loudly if the file has drifted from what was read ---
assert orig_lines[33].startswith("- [x] **CLOSED c3567"), orig_lines[33][:80]
assert orig_lines[36].startswith("- [x] **CLOSED c3566"), orig_lines[36][:80]
assert orig_lines[39].startswith("- [x] **CLOSED c3565"), orig_lines[39][:80]
assert orig_lines[41] == "\n", repr(orig_lines[41])
assert orig_lines[42].startswith("- [ ] **NEW c3548"), orig_lines[42][:80]
assert orig_lines[32] == "\n", repr(orig_lines[32])
assert orig_lines[31].strip().startswith("- [ ] **NEW c3568(c)"), orig_lines[31][:80]

CUT_START = 33  # 0-indexed: line 34 (c3567 header)
CUT_END = 42    # 0-indexed exclusive: up to but not including line 43 (NEW c3548)

cut_span = orig_lines[CUT_START:CUT_END]
assert cut_span[0].startswith("- [x] **CLOSED c3567")
assert cut_span[-1] == "\n"
assert cut_span[-2].strip().startswith("- **Next (BUILD slot)")  # c3565's trailing sub-bullet

new_live = orig_lines[:CUT_START] + orig_lines[CUT_END:]

archive_header = (
    "## Archived by cycle 3573 (from tasks/queue.md: the 3 oldest cycle-report "
    "blocks under the STANDING RULE 6b newest-5 floor -- c3567, c3566, c3565, "
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
    print("--- line at CUT_START in new live file (should be NEW c3548) ---")
    print(new_live[CUT_START][:120])
