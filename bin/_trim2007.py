#!/usr/bin/env python3
"""One-shot, lossless tasks/queue.md -> tasks/queue_archive.md trim for cycle 2007.

Scoped by cycle 2004's note (queue.md top item at the time): `check-doc-size`
rated queue.md OK at 2004 (111.2KB/1330 lines) but projected 239KB at its own
next look (cycle 2028), crossing the 200KB trim line around cycle ~2021 --
unseen by the check. By cycle 2007 it had grown to 119,997 bytes / 1400 lines.

Unlike a STATUS.md trim (newest-N-cycle-blocks by line count), queue.md's live
half MUST keep every open `[ ]` item regardless of age, so the cut is on
closed-block boundaries, not a single line number. Cycle 2007 found the 5 open
items (lines 18, 69, 346, 364, 374) are NOT all below one cutoff -- a single
large closed block ("CLOSED cycle 2004 -- history of the check-readme-live-row
extension backlog", the v1-v15 per-version detail, lines 82-345) sits BETWEEN
open item 69 and open item 346. So there are two moved segments:
  B: lines 82-345  (the v1-v15 closed history block)
  D: lines 390-EOF (everything from "CLOSED by cycle 1988" onward -- all closed)
and two kept segments:
  A: lines 1-81    (DONE cycle 2006, open item 18, DONE cycle 2004 x2, open 69)
  C: lines 346-389 (open items 346/364/374 and their content)
A ends on a blank line (81) and C starts directly on an open item (346), so
A+C concatenates cleanly with no stray separator to add or drop.

Archive placement: PREPENDED at the top under a `PRIOR (...)` header, matching
cycle 2004's STATUS.md convention. Archive file is the real one on disk,
`tasks/queue_archive.md` (lowercase -- the cycle 2004 note said
`queue_ARCHIVE.md`, a typo; no such file exists, confirmed by `ls`). Moved
segments are archived in their original order (B before D), newest-first,
matching the source file.
"""
import sys

LIVE = "/root/agent/tasks/queue.md"
ARCH = "/root/agent/tasks/queue_archive.md"
LABEL = "queue.md"

# 1-indexed, inclusive line ranges
A = (1, 81)
B = (82, 345)
C = (346, 389)
D = (390, None)  # None = to EOF

HEADER = (
    "PRIOR (closed/DONE queue items, archived by cycle 2007): {label} was {lines} "
    "lines / {kb}KB and `bin/check-doc-size` had projected it would cross the 200KB "
    "trim line around cycle ~2021 unseen (last rated OK at cycle 2004, 111.2KB). "
    "Moved here: the v1-v15 `check-readme-live-row` extension-backlog history block "
    "(closed cycle 2004) and every closed/DONE block from cycle 1988 backward. The 5 "
    "still-open `[ ]` items at trim time (queue.md trim itself, the README/"
    "dataset_schema check candidate, the Bytewells re-evaluation, the CFDA "
    "obligation-field feature, the next blog-post candidate) all stayed in the live "
    "file. Newest-first below, same order as the source file.\n"
)

with open(LIVE, encoding="utf-8") as f:
    orig = f.read()
lines = orig.splitlines(keepends=True)
n = len(lines)
kb = round(len(orig.encode()) / 1024, 1)


def seg(rng):
    start, end = rng
    end = n if end is None else end
    return lines[start - 1:end]


seg_a, seg_b, seg_c, seg_d = seg(A), seg(B), seg(C), seg(D)

problems = []
if len(seg_a) + len(seg_b) + len(seg_c) + len(seg_d) != n:
    problems.append("segments do not cover the whole file exactly once")
if not seg_a[-1].strip() == "":
    problems.append("segment A does not end on a blank line")
if "CLOSED cycle 2004" not in seg_b[0]:
    problems.append(f"segment B does not start with the cycle-2004 history block: {seg_b[0][:90]!r}")
if "Re-evaluate the \"Bytewells" not in seg_c[0]:
    problems.append(f"segment C does not start with the Bytewells open item: {seg_c[0][:90]!r}")
if "CLOSED by cycle 1988" not in seg_d[0]:
    problems.append(f"segment D does not start with the cycle-1988 block: {seg_d[0][:90]!r}")

keep_lines = seg_a + seg_c
moved_lines = seg_b + seg_d
keep_txt = "".join(keep_lines)
for marker in (
    "THIS file) is the next trim",
    "New check candidate, scoped by cycle 2004's finding",
    "Bytewells by ThoughtPivot",
    "Possible feature, only with the caller-choice design",
    "Next blog-post candidate (re-scoped by cycle 1988",
):
    if marker not in keep_txt:
        problems.append(f"open item marker missing from kept half: {marker!r}")
moved_txt_probe = "".join(moved_lines)
if "CLOSED cycle 2004" not in moved_txt_probe or "CLOSED by cycle 1988" not in moved_txt_probe:
    problems.append("expected closed blocks missing from moved half")
if problems:
    for p in problems:
        print(f"ABORT {LABEL}: {p}")
    sys.exit(1)

if not keep_txt.endswith("\n"):
    keep_txt += "\n"
moved_txt = "".join(moved_lines)
if not moved_txt.endswith("\n"):
    moved_txt += "\n"

with open(ARCH, encoding="utf-8") as f:
    arch_before = f.read()

chunk = HEADER.format(label=LABEL, lines=n, kb=kb) + "\n" + moved_txt + "\n"
new_arch = chunk + arch_before

with open(ARCH, "w", encoding="utf-8") as f:
    f.write(new_arch)
with open(LIVE, "w", encoding="utf-8") as f:
    f.write(keep_txt)

with open(ARCH, encoding="utf-8") as f:
    arch_after = f.read()
with open(LIVE, encoding="utf-8") as f:
    live_after = f.read()

if moved_txt not in arch_after:
    problems.append("moved text NOT found verbatim in archive")
if not arch_after.endswith(arch_before):
    problems.append("pre-existing archive content is not an intact suffix")
if live_after != keep_txt:
    problems.append("live file does not match intended kept text")

if problems:
    for p in problems:
        print(f"POST-WRITE PROBLEM {LABEL}: {p}")
    sys.exit(1)

print(f"{LABEL}: {n} lines / {kb}KB -> live {len(keep_lines)} lines / "
      f"{round(len(keep_txt.encode())/1024,1)}KB, archive +{len(moved_lines)} lines "
      f"(prepended, archive now {round(len(arch_after.encode())/1024/1024,2)}MB)")
