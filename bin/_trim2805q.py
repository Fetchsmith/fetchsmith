#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2805 (86.9KB/997 lines, TRIM SOON).

check-doc-size read TRIM SOON on both tasks/queue.md and state/STATUS.md at
preflight; c2804 explicitly named this QUALITY slot (2805 % 3 == 0) as the
one to trim queue.md in, and the doc-trim cadence item's rule 2 says do not
let a second QUALITY slot pass it (c2802 was the first skip since c2799).

Same hoist-then-cut method as bin/_trim2588q.py / bin/_trim2799*.py: archive
completed DONE blocks verbatim into queue_archive.md, keep the most recent
cycle's DONE block (c2804) live since it still carries live pointers (sweep
data file paths, "next audit due" note), and hoist every genuinely open item
unchanged. Partition asserted total, non-overlapping, multiset-identical to
the original before writing.

Standing-hazard check (cadence living ONLY in an archived block) done before
writing this script: c2803's block (dead-endpoint-docs, next due c2827) --
that due date lives in state/fleet_checks.json, not only here. c2802's block
(readme-truncation gotcha) -- the real fix is already in PLAYBOOK.md rule 9
per that cycle's own text, so nothing is lost. c2800's block (substack audit,
argv-trap rule, forgedata record) -- the argv-trap STANDING RULE itself lives
in the c2796 item (kept, not touched by this script); the substack price
numbers live in state/audit_data/c2800_substack_prices.json per that block's
own text. c2799's block (queue-trim execution record) -- superseded by this
very trim; the STANDING RULES it carries live in the doc-trim cadence item
(kept, lines 589-658 pre-cut) which this script does not touch.
"""

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
NLINES = 997

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == NLINES, f"expected {NLINES} lines, got {len(lines)} -- file changed, abort"


def seg(a, b):
    return lines[a - 1:b]


# Fully-historical DONE cycle-summary blocks, each ending on its own trailing
# blank line. The c2804 DONE block (34-46) stays live -- most recent, carries
# current pointers -- per the standing precedent.
ARCHIVED = [
    (64, 67),    # DONE c2803 (check-dead-endpoint-docs)
    (68, 83),    # DONE c2802 (readme-truncation gotcha, now in PLAYBOOK.md)
    (84, 143),   # DONE c2800 (substack competitor_audit)
    (163, 207),  # DONE c2799 (queue.md trim execution, superseded by this trim)
]

KEPT = [
    (1, 63),     # open c2804 items + live c2804 DONE block
    (144, 162),  # open c2800 follow-up + watch items
    (208, 997),  # everything else, open items through EOF
]

archived_lines = []
for a, b in ARCHIVED:
    archived_lines.extend(seg(a, b))

kept_lines = []
for a, b in KEPT:
    kept_lines.extend(seg(a, b))

covered = sorted([i for a, b in ARCHIVED + KEPT for i in range(a, b + 1)])
assert covered == list(range(1, NLINES + 1)), \
    f"partition is not total/non-overlapping over 1..{NLINES}"
assert sorted(archived_lines + kept_lines) == sorted(lines), \
    "multiset mismatch -- content lost or duplicated"

assert not [l for l in archived_lines if l.startswith("- [ ]")], \
    "an open item is in the archive partition -- abort"
archived_done_starts = [l for l in archived_lines if l.startswith("- [x]")]
assert len(archived_done_starts) == 4, \
    f"expected exactly 4 archived DONE blocks, got {len(archived_done_starts)}"
kept_done_starts = [l for l in kept_lines if l.startswith("- [x]")]
assert kept_done_starts == [lines[33]], \
    "a DONE block other than c2804 survived in the kept partition, or c2804 is missing"

HEADER = (
    "\n## Archived at cycle 2805 (queue.md trim, `bin/_trim2805q.py`)\n\n"
    "Older completed DONE blocks (cycles 2803, 2802, 2800, 2799). The cycle-2804\n"
    "DONE block stays live in queue.md (it carries live pointers: sweep data file\n"
    "paths, next-audit-due note). Verbatim, no content changed.\n\n"
)

with open(ARCHIVE, "a") as f:
    f.write(HEADER)
    f.writelines(archived_lines)

with open(SRC, "w") as f:
    f.writelines(kept_lines)

print(f"archived {len(archived_lines)} lines, kept {len(kept_lines)} lines "
      f"(was {len(lines)})")
