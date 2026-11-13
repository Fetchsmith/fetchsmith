#!/usr/bin/env python3
"""c3126 QUALITY-slot trim of state/STATUS.md -- keep-newest-10-blocks cut.

STATUS.md carries no interleaved open items (unlike queue.md), so this is a
pure prefix cut: keep the newest 10 `Updated: ... by cycle N` blocks live,
move everything older verbatim to state/STATUS_ARCHIVE.md.

Preflight: TRIM DUE at 152.0KB/468ln (~11c headroom). `grep -n '^Updated:'`
re-derived fresh (rule 3, never paste line numbers forward) gives 34 live
blocks, newest first: c3125, c3124, c3123, c3122, c3121, c3120, c3119, c3118,
c3117, c3116, c3115, ... c3090. The 10th-newest is c3116 (Updated: line 135),
the 11th is c3115 (marker line 145). Keep lines 1-143 (through the end of the
c3116 block, dropping the trailing blank as the usual separator); archive
lines 145-468 (c3115 down through c3090) verbatim.
"""
import collections, sys

STATUS = "/root/agent/state/STATUS.md"
ARCHIVE = "/root/agent/state/STATUS_ARCHIVE.md"

CUT_FIRST_LINE = 145  # 1-indexed, first line of the "cycle 3115" marker block

orig = open(STATUS).read()
lines = orig.split("\n")
n = len(lines)
assert lines[CUT_FIRST_LINE - 1].strip() == "<!-- ---- cycle 3115 ---- -->", \
    f"boundary drifted: line {CUT_FIRST_LINE} is {lines[CUT_FIRST_LINE - 1]!r}"

keep = lines[:CUT_FIRST_LINE - 1]
moved = lines[CUT_FIRST_LINE - 1:]
assert len(keep) + len(moved) == n
assert collections.Counter(keep) + collections.Counter(moved) == collections.Counter(lines)

# drop trailing blank separator lines off the kept half
while keep and keep[-1].strip() == "":
    keep.pop()
dropped = (CUT_FIRST_LINE - 1) - len(keep)
assert dropped <= 3, f"dropped {dropped} separator lines, expected <=3"

keep_txt = "\n".join(keep) + "\n"
moved_txt = "\n".join(moved)

assert keep_txt.count("Updated: ") == 10, f"expected 10 live blocks, got {keep_txt.count('Updated: ')}"
for c in ("3125", "3124", "3123", "3122", "3121", "3120", "3119", "3118", "3117", "3116"):
    assert f"by cycle {c} " in keep_txt, f"SURVIVOR LOST: cycle {c}"
for c in ("3115", "3114", "3113", "3090"):
    assert f"by cycle {c} " not in keep_txt, f"should have been cut but is still live: cycle {c}"
    assert f"by cycle {c} " in moved_txt, f"MOVED BLOCK MISSING: cycle {c}"

arc_before = open(ARCHIVE).read()
sep = "" if arc_before.endswith("\n\n") else ("\n" if arc_before.endswith("\n") else "\n\n")
header = (
    "## Archived by cycle 3126, 2026-11-13 -- STATUS.md had grown to 468 lines / 152.0KB, "
    "TRIM DUE. Cycles <=3115 moved here verbatim (newest-first, same order as the source "
    "file); the live file keeps the newest 10 blocks (3125 down to 3116).\n"
)
new_arc = arc_before + sep + header + "\n" + moved_txt + "\n"

for l in lines:
    if l.strip():
        assert l in keep_txt or l in new_arc, f"LINE LOST: {l[:100]}"
print("  lossless OK  every non-blank original line present in live+archive")
print(f"  floor OK  10 live blocks (c3125..c3116), dropped {dropped} separator line(s)")

if "--write" in sys.argv:
    open(STATUS, "w").write(keep_txt)
    open(ARCHIVE, "w").write(new_arc)
    print("WROTE state/STATUS.md, state/STATUS_ARCHIVE.md")
else:
    print("DRY RUN ok -- re-run with --write to commit")
    print(f"STATUS.md: {len(orig)}B -> {len(keep_txt)}B ({n} -> {len(keep)} lines)")
