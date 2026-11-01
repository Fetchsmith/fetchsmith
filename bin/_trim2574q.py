#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2574 (73.6KB / 785 lines, TRIM SOON).

checks-due --all and all three audit-due axes read NONE DUE at preflight;
this is a QUALITY/GROWTH slot (2574 % 3 == 0), so per the standing doc-trim
cadence item (c2508/.../c2567) this cycle executes the trim proactively
rather than waiting for TRIM DUE.

Same hoist-then-cut method as bin/_trim2567q.py: archive completed DONE
blocks (and one now-fully-redundant SUPERSEDED notice) verbatim into
queue_archive.md, keep the most recent cycle's DONE block (2573) live since
it still carries the current "next cycle" pointer, and hoist every genuinely
open item unchanged. Partition is asserted total, non-overlapping, and
multiset-identical to the original before writing.
"""
import sys

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 785, f"expected 785 lines, got {len(lines)} -- file changed, abort"


def seg(a, b):
    return lines[a - 1:b]


# Older, now-fully-historical DONE cycle-summary blocks (2572, 2568-summary,
# 2567, 2566, 2569, 2570, 2571, 2568-followup) plus the SUPERSEDED notice
# that is now fully redundant with the 2573 DONE block's own text.
ARCHIVED = [
    (1, 248),      # DONE 2572 / 2568 / 2567 / 2566 / 2569 / 2570 / 2571 / 2568-followup + trailing blank
    (313, 317),    # SUPERSEDED notice + trailing blanks
]

# Most recent cycle's DONE block stays live (still carries the current
# "next cycle" pointer), plus every genuinely open item, verbatim, in
# source order.
KEPT = [
    (249, 312),    # c2560 open follow-up + DONE cycle 2573 block + blank
    (318, 785),    # every open item from c2548 onward through EOF
]

archived_lines = []
for a, b in ARCHIVED:
    archived_lines.extend(seg(a, b))

kept_lines = []
for a, b in KEPT:
    kept_lines.extend(seg(a, b))

# Partition must be total, non-overlapping, and multiset-identical to the original.
covered = sorted([i for a, b in ARCHIVED + KEPT for i in range(a, b + 1)])
expected = list(range(1, 786))
assert covered == expected, "partition is not total/non-overlapping over 1..785"
assert sorted(archived_lines + kept_lines) == sorted(lines), "multiset mismatch -- content lost or duplicated"

HEADER = (
    "\n## Archived at cycle 2574 (queue.md trim, `bin/_trim2574q.py`)\n\n"
    "Older completed DONE blocks (cycles 2572, 2568-summary, 2567, 2566, 2569,\n"
    "2570, 2571, 2568-followup) plus the fully-redundant SUPERSEDED notice for\n"
    "the Workday salary item (superseded by the 2573 DONE block, kept live in\n"
    "queue.md). Verbatim, no content changed.\n\n"
)

with open(ARCHIVE, "a") as f:
    f.write(HEADER)
    f.writelines(archived_lines)

with open(SRC, "w") as f:
    f.writelines(kept_lines)

print(f"archived {len(archived_lines)} lines, kept {len(kept_lines)} lines "
      f"(was {len(lines)})")
