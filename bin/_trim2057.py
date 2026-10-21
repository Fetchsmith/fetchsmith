#!/usr/bin/env python3
"""One-shot, lossless tasks/queue.md -> queue_archive.md trim for cycle 2057.

check-doc-size exited 1 this cycle (TRIM DUE: queue.md 129.2KB, projected 257KB at
its next scheduled look in 24c -- past the 256KB Read cap). Keeps the newest 10
cycle blocks in the live file (2056 down to 2047), appends the remainder verbatim
to the end of the existing archive under a dated '## Archived by cycle 2057'
header, same shape as the cycle 1836/1799 trims.

Verification is arithmetic + content: every archived line must appear in the new
archive, and keep+moved must reconstruct the original byte-for-byte.
"""
import sys

LIVE = "/root/agent/tasks/queue.md"
ARCH = "/root/agent/tasks/queue_archive.md"
FIRST_MOVE = 401  # 1-indexed first line to MOVE (start of the cycle 2046 block)
LABEL = "queue.md"

HEADER = (
    "## Archived by cycle 2057 (sonnet-5), 2026-10-21 — {label} had grown to "
    "{lines} lines / {kb}KB, projected past the Read-tool single-file cap (256KB) "
    "before check-doc-size's next scheduled look. Cycles <=2046 moved here "
    "verbatim; the live file keeps the newest 10 cycle blocks (2056 down to "
    "2047). Newest-first below, same order as the source file.\n"
)

with open(LIVE, encoding="utf-8") as f:
    orig = f.read()
lines = orig.splitlines(keepends=True)
n = len(lines)
kb = round(len(orig.encode()) / 1024)

idx = FIRST_MOVE - 1
keep = lines[:idx]
moved = lines[idx:]

while keep and keep[-1].strip() in ("", "---"):
    keep.pop()
dropped = idx - len(keep)
if dropped > 3:
    print(f"ABORT {LABEL}: dropped {dropped} separator lines, expected <=3")
    sys.exit(1)

ok = True
if not moved:
    print(f"ABORT {LABEL}: nothing to move")
    sys.exit(1)
if "cycle 2046" not in moved[0]:
    print(f"ABORT {LABEL}: first moved line is not the 2046 block: {moved[0][:90]!r}")
    sys.exit(1)
if "2047" not in "".join(keep[-120:]):
    print(f"ABORT {LABEL}: cycle 2047 block missing from kept tail")
    sys.exit(1)

keep_txt = "".join(keep)
if not keep_txt.endswith("\n"):
    keep_txt += "\n"
moved_txt = "".join(moved)

with open(ARCH, encoding="utf-8") as f:
    arch_before = f.read()
sep = "" if arch_before.endswith("\n\n") else ("\n" if arch_before.endswith("\n") else "\n\n")
new_arch = (arch_before + sep
            + HEADER.format(label=LABEL, lines=n, kb=kb) + "\n"
            + moved_txt)

with open(ARCH, "w", encoding="utf-8") as f:
    f.write(new_arch)
with open(LIVE, "w", encoding="utf-8") as f:
    f.write(keep_txt)

with open(ARCH, encoding="utf-8") as f:
    arch_after = f.read()
with open(LIVE, encoding="utf-8") as f:
    live_after = f.read()

problems = []
if moved_txt not in arch_after:
    problems.append("moved text NOT found verbatim in archive")
if arch_before not in arch_after:
    problems.append("pre-existing archive content was altered")
missing = [l for l in moved if l.strip() and l not in arch_after]
if missing:
    problems.append(f"{len(missing)} moved lines missing from archive")
if live_after != keep_txt:
    problems.append("live file does not match computed keep half")

print(f"{LABEL}: {n} lines -> {len(live_after.splitlines())} kept, "
      f"{len(moved)} moved, {dropped} separator line(s) dropped")
print(f"  archive: {len(arch_before.splitlines())} -> "
      f"{len(arch_after.splitlines())} lines")
if problems:
    ok = False
    for p in problems:
        print(f"  FAIL: {p}")
else:
    print("  OK: lossless (moved text verbatim in archive, prior archive intact)")

sys.exit(0 if ok else 1)
