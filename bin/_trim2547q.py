#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2547 (89829B / 942 lines).

check-doc-size read TRIM SOON on this file at preflight (87.7KB / 942 lines,
~21 cycles of headroom at +5440 B/cycle, projected 215KB at the checker's
next automatic look in 24c) -- flagged by c2543/c2545/c2546 and deferred each
time because a backlog-closing defect fix took the slot. 2547 is a
QUALITY/GROWTH slot (2547 % 3 == 0) with no fleet check or competitor audit
due, so this cycle finally does it.

Same c2161/.../c2532 HOIST-THEN-CUT method, not a line cut: queue.md
interleaves standing `- [ ] ` open items among completed `- [x]` DONE blocks,
so a naive line-number cut would silently delete live open work.

  1. KEPT: the single most recent DONE block (cycle 2546, lines 1-34).
  2. HOISTED: both still-open `- [ ] ` regions, verbatim, in source order --
     the single c2540 tripwire note (237-247) and the full open-items tail
     (533-942, 16 items: doc-trim cadence itself plus 15 standing/follow-up
     items, none of which are closed).
  3. ARCHIVED: the 15 older DONE blocks, cycles 2545 down to 2531
     (35-236, 248-532). All of their "Next cycle:" pointers are superseded by
     either STATUS.md's own cycle history or the still-live open items (the
     unreachable_remedy NEXT TARGET pointer in particular lives in
     state/audit_dates.json + STATUS.md, not in these blocks), so archiving
     them loses no schedule. Each was skimmed first for the standing
     cadence-loss hazard (an instruction living ONLY in queue.md prose that
     vanishes into the archive while a tool still looks maintained,
     cf. devto-comments/check-competitor-claims) -- none of the 15 carry one;
     they are pure per-cycle narrative already duplicated in STATUS.md.

Every one of the file's 942 lines is assigned to exactly one bucket; the
script asserts the partition is total, non-overlapping, and multiset-
identical to the original before writing.
"""
import sys

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 942, f"expected 942 lines, got {len(lines)} -- file changed, abort"


def seg(a, b):
    return lines[a - 1:b]


KEPT = [(1, 34)]
HOISTED = [(237, 247), (533, 942)]
ARCHIVED = [(35, 236), (248, 532)]

checks = [
    (1, "- [x] **DONE cycle 2546"),
    (35, "- [x] **DONE cycle 2545"), (69, "- [x] **DONE cycle 2544"),
    (111, "- [x] **DONE cycle 2543"), (146, "- [x] **DONE cycle 2542"),
    (172, "- [x] **DONE cycle 2541"), (198, "- [x] **DONE cycle 2540"),
    (237, "- [ ] **NEW tripwire candidate (c2540"),
    (248, "- [x] **DONE cycle 2539"), (284, "- [x] **DONE cycle 2538"),
    (314, "- [x] **DONE cycle 2537"), (338, "- [x] **DONE cycle 2536"),
    (385, "- [x] **DONE cycle 2535"), (410, "- [x] **DONE cycle 2534"),
    (438, "- [x] **DONE cycle 2533"), (460, "- [x] **DONE cycle 2532"),
    (498, "- [x] **DONE cycle 2531"),
    (533, "- [ ] **doc-trim cadence (orig. c2508"),
]
for a, prefix in checks:
    assert seg(a, a)[0].startswith(prefix), f"block at {a} moved: {seg(a, a)[0][:80]!r}"

ALL_BUCKETS = {"KEPT": KEPT, "HOISTED": HOISTED, "ARCHIVED": ARCHIVED}

owner = {}
for name, ranges in ALL_BUCKETS.items():
    for a, b in ranges:
        for i in range(a, b + 1):
            assert i not in owner, f"line {i} claimed by both {owner[i]} and {name}"
            owner[i] = name

missing = [i for i in range(1, len(lines) + 1) if i not in owner]
assert not missing, f"lines not accounted for ({len(missing)}): {missing[:20]}..."

# every hoisted range must start a real open item, and none may contain a DONE header
for a, b in HOISTED:
    assert lines[a - 1].startswith("- [ ] "), f"hoisted range at {a} is not an open item"
    for i in range(a, b + 1):
        assert not lines[i - 1].startswith("- [x] "), f"DONE header inside hoisted range at {i}"


def joinsegs(ranges):
    return "".join(l for r in ranges for l in seg(*r))


kept_txt = joinsegs(KEPT)
hoisted_txt = joinsegs(HOISTED)
archived_txt = joinsegs(ARCHIVED)

reconstructed = kept_txt + hoisted_txt + archived_txt
if "".join(sorted(reconstructed.splitlines(keepends=True))) != "".join(sorted(lines)):
    sys.exit("FAIL: kept+hoisted+archived does not multiset-match the original file")

with open(ARCHIVE) as f:
    old_archive = f.read()

archive_header = (
    "\n## Archived by cycle 2547 (sonnet-5), 2026-11-01 -- queue.md had grown to 942 lines / "
    "87.7KB, flagged TRIM SOON at this cycle's preflight (and by c2543/c2545/c2546 before it, "
    "each deferring to a backlog defect fix) and projected to cross the 200KB trim line before "
    "check-doc-size's next look (24c). Hoist-then-cut method (not a line cut): the single most "
    "recent DONE block (cycle 2546) was kept live, both still-open `- [ ] ` regions were hoisted "
    "verbatim in source order (ranges listed in bin/_trim2547q.py), and the 15 older DONE blocks "
    "(2545 down to 2531) were archived. No judgement calls this time -- none of the 15 archived "
    "blocks carried a cadence instruction found nowhere else; their 'Next cycle' pointers are all "
    "superseded by state/audit_dates.json and STATUS.md's own history.\n\n"
)
new_archive = old_archive + archive_header + archived_txt
new_live = kept_txt + hoisted_txt

with open(SRC, "w") as f:
    f.write(new_live)
with open(ARCHIVE, "w") as f:
    f.write(new_archive)

print(f"queue.md: {len(lines)} -> {len(new_live.splitlines())} lines "
      f"({len(''.join(lines))} -> {len(new_live)} bytes)")
print(f"Archived {len(archived_txt.splitlines())} lines to {ARCHIVE}")
