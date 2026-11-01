#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2588 (80.5KB / 858 lines, TRIM SOON).

bin/check-doc-size read TRIM SOON on tasks/queue.md at preflight (proj. 208KB
at its own next look, i.e. the next run reads TRIM DUE no matter what), while
state/STATUS.md (91.8KB, proj. 197KB) and notes/LEARNINGS.md (6339 lines) both
read OK and are deliberately left alone per the c2224 rule. checks-due --all
and all three audit-due axes read NONE DUE, so per the standing doc-trim
cadence item (c2508/.../c2574) this cycle executes the trim proactively.

Same hoist-then-cut method as bin/_trim2574q.py: archive completed DONE blocks
verbatim into queue_archive.md, keep the most recent cycle's DONE block (2587)
live since it still carries the current "next cycle" pointer, and hoist every
genuinely open item unchanged. Partition is asserted total, non-overlapping and
multiset-identical to the original before writing.

Standing-hazard check (cadence living ONLY in an archived block) run before
writing this script: every "standing"/"cadence" phrase inside the three archive
ranges is narrative *about* a cadence homed elsewhere -- the doc-trim cadence
item itself is KEPT (349-464), the checks-due/audit-due cadences live in those
tools' own state, the dev.to syndication cadence lives in PLAYBOOK plus
state/devto_syndicated.json, and the one "standing lesson" in the c2580 block
(never round-trip a state JSON through json.dump) already has two homes in
notes/LEARNINGS.md (lines 1729 and 5581). Nothing in the archive ranges is the
sole home of an instruction.
"""

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
NLINES = 858

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == NLINES, f"expected {NLINES} lines, got {len(lines)} -- file changed, abort"


def seg(a, b):
    return lines[a - 1:b]


# Fully-historical DONE cycle-summary blocks. Each range ends on its own
# trailing blank line so the kept file keeps exactly one blank between items.
ARCHIVED = [
    (17, 348),   # DONE 2586, 2585, 2584, 2580, 2581, 2575, 2573, 2576, 2577 + SUPERSEDED-by-c2576 notice
    (465, 488),  # DONE 2578 (courts vocab-screen probe) + trailing blanks
    (524, 582),  # DONE 2579 (audit-due CLEAN vocabulary)
]

# Most recent cycle's DONE block stays live (carries the current "next cycle"
# pointer), plus every genuinely open item, verbatim, in source order.
KEPT = [
    (1, 16),     # DONE cycle 2587 + blank
    (349, 464),  # open: c2552 tripwire, c2540 tripwire, doc-trim cadence, c2532 STANDING
    (489, 523),  # open: c2478 Store-API deadline, c2464 HIGH pricer port, c2464 TRIVIAL note
    (583, 858),  # open: c2456 through c2120, every remaining item to EOF
]

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

# No open item may leave the live file, and no DONE block may stay beyond 2587.
assert not [l for l in archived_lines if l.startswith("- [ ]")], \
    "an open item is in the archive partition -- abort"
assert [l for l in kept_lines if l.startswith("- [x]")] == [lines[0]], \
    "a DONE block other than cycle 2587 survived in the kept partition -- abort"

HEADER = (
    "\n## Archived at cycle 2588 (queue.md trim, `bin/_trim2588q.py`)\n\n"
    "Older completed DONE blocks (cycles 2586, 2585, 2584, 2580, 2581, 2575,\n"
    "2573, 2576, 2577, 2578, 2579) plus the SUPERSEDED-by-c2576 projects-endpoint\n"
    "notice. The cycle-2587 DONE block stays live in queue.md (it carries the\n"
    "current \"next cycle\" pointer). Verbatim, no content changed.\n\n"
)

with open(ARCHIVE, "a") as f:
    f.write(HEADER)
    f.writelines(archived_lines)

with open(SRC, "w") as f:
    f.writelines(kept_lines)

print(f"archived {len(archived_lines)} lines, kept {len(kept_lines)} lines "
      f"(was {len(lines)})")
