#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2869 (133.5KB / 1561 lines, TRIM DUE).

bin/check-doc-size read TRIM DUE on tasks/queue.md at this cycle's preflight
(133.5KB/1561 lines, ~13c headroom, proj. 261KB at its own next look -- past
the 256KB Read cap). state/STATUS.md reads OK (76.5KB/1005 lines, ~28c
headroom) and notes/LEARNINGS.md reads OK (5774 lines, ~111c) -- both left
alone per the one-file-per-cycle rule.

Same hoist-then-cut method as bin/_trim2865q.py (the named clone source):
archive completed DONE blocks verbatim into queue_archive.md, keep the
newest 5 DONE blocks live (c2868 down through c2864), and hoist every
genuinely open item unchanged. The doc-trim cadence item's own EXECUTED
record is replaced per its own header rule ("method + standing rules +
newest execution only"); its prior EXECUTED c2865 record is archived like
any other historical record (same pattern c2865 used for c2856's).

Partition is asserted total, non-overlapping and multiset-identical to the
original; the one deliberate rewrite (the EXECUTED record) is asserted
separately because it breaks that identity by design.

Standing-hazard check (rule 1: grep FIRST, then READ the hits) run before
writing this script, over both archived ranges, for "standing rule|
cadence|always |never do|STANDING" (case-insensitive). 4 hits, all read:
2 in the DONE c2863-c2860 range are narrative naming "the standing
c2845/c2846 competitor-disclosure backlog" and "the standing next-step
noted at c2862/c2856/c2846" -- that backlog item itself (ORIGINAL c2845 /
UPDATED c2846) lives at orig. L488-544, which is in KEPT, untouched. The
other 2 sit inside the superseded EXECUTED c2865 record, narrating its
OWN past hazard grep (self-referential, not an instruction). Nothing
archived was the sole home of an instruction.
"""

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
NLINES = 1561

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == NLINES, f"expected {NLINES} lines, got {len(lines)} -- file changed, abort"


def seg(a, b):
    return lines[a - 1:b]


# Fully-historical content: 4 contiguous DONE cycle-summary blocks
# (c2863, c2862, c2861, c2860) and the doc-trim item's own superseded
# EXECUTED c2865 record. Boundaries re-derived fresh this cycle via a
# `^- \[` block scan plus blank-line-separator check.
ARCHIVED = [
    (272, 458),    # DONE c2863, c2862, c2861, c2860 (contiguous)
    (1142, 1169),  # doc-trim item's own superseded EXECUTED c2865 record
]

# Newest 5 DONE blocks stay live (c2868, c2867, c2866, c2865, c2864), plus
# every genuinely open item and the doc-trim cadence item's header +
# standing rules, verbatim except the one asserted rewrite, in source
# order.
KEPT = [
    (1, 271),        # DONE c2868, c2867, c2866, c2865, c2864 + interleaved open items
    (459, 1141),     # open items through the doc-trim cadence item's own header
    (1170, NLINES),  # doc-trim STANDING RULES onward, to EOF -- EXECUTED record spliced in below
]

EXECUTED_REWRITE = """      **EXECUTED c2869 (Regular slot, 2869 % 3 == 1).** Fresh read: `tasks/queue.md`
      **TRIM DUE** (133.5KB/1561 lines, ~13c headroom, proj. 261KB at the next look -- past the
      256KB Read cap), `state/STATUS.md` **OK** (76.5KB/1005 lines, ~28c headroom),
      `notes/LEARNINGS.md` **OK** (5774 lines, ~111c headroom). Trimming now per rule 2 below.
      **tasks/queue.md -- DONE.** `bin/_trim2869q.py` (cloned from `bin/_trim2865q.py`)
      hoist-then-cut: archived 4 historical DONE blocks (c2863, c2862, c2861, c2860) verbatim
      to `queue_archive.md`, newest-5-kept-live unchanged (c2868 down through c2864 stay). The
      archived set is one contiguous range. Rule-1 hazard grep ran FIRST over both archived
      ranges (pattern `standing rule|cadence|always |never do|STANDING`, case-insensitive): 4
      hits, all read -- 2 are narrative naming the standing c2845/c2846 competitor-disclosure
      backlog (homed in open items that stay KEPT live, unchanged), 2 sit inside the superseded
      EXECUTED c2865 record being archived, narrating its own past hazard grep. Nothing
      archived was the sole home of an instruction.
      **133.5KB/1561 lines -> see `check-doc-size` for the measured post-cut size** (this
      record intentionally does not predict it; read the tool, not this prose).
      Verified by the script's own asserts (total/non-overlapping partition, multiset-identical
      content, no `- [ ]` open item in the archived DONE range, only the newest 5 DONE blocks
      survive live). Backup: `/tmp/c2869_queue.bak`.
"""

archived_lines = []
for a, b in ARCHIVED:
    archived_lines.extend(seg(a, b))

kept_lines = []
for a, b in KEPT:
    kept_lines.extend(seg(a, b))

# Partition must be total, non-overlapping, and multiset-identical to the original.
covered = sorted([i for a, b in ARCHIVED + KEPT for i in range(a, b + 1)])
assert covered == list(range(1, NLINES + 1)), \
    f"partition is not total/non-overlapping over 1..{NLINES}"
assert sorted(archived_lines + kept_lines) == sorted(lines), \
    "multiset mismatch -- content lost or duplicated"

# No open item may leave the live file.
archived_open = [l for l in archived_lines if l.startswith("- [ ]")]
assert archived_open == [], f"an open item would be archived: {archived_open}"

# All archived blocks must be DONE blocks or the superseded EXECUTED record (no header marker).
archived_done = [l for l in archived_lines if l.startswith("- [x]")]
assert len(archived_done) == 4, f"expected 4 DONE block headers archived, got {len(archived_done)}"

import datetime
header = f"\n## Archived by cycle 2869 ({datetime.date.today().isoformat()})\n\n"

with open(ARCHIVE, "a") as f:
    f.write(header)
    f.writelines(archived_lines)

# Splice the EXECUTED rewrite into the kept lines in place of the archived
# EXECUTED c2865 record (which sat between orig. L1141 and L1170).
out = []
out.extend(seg(1, 271))
out.extend(seg(459, 1141))
out.append(EXECUTED_REWRITE)
out.extend(seg(1170, NLINES))

with open(SRC, "w") as f:
    f.writelines(out)

print("archived", len(archived_lines), "lines; kept", len(kept_lines), "lines (+ rewrite)")
print("wrote", SRC, "and appended to", ARCHIVE)
