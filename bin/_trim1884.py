#!/usr/bin/env python3
"""One-shot, lossless queue.md -> queue_archive.md trim for cycle 1884.

`bin/check-doc-size` (24c clock, due this cycle) reported tasks/queue.md at
145.9KB / 1874 lines with only ~10 cycles of headroom before the 256KB Read-tool
cap. STATUS.md was OK (138.4KB, ~14 cycles) and is deliberately NOT touched here.

Keeps the newest contiguous run of cycle blocks (1872..1883 + the NEXT 1884
block, 12 DONE blocks >= the "newest 10" floor in the documented process) in the
live file; everything from the cycle-1872 block's predecessor onward is appended
verbatim to the end of the archive under a dated header, same shape as the
cycle 1836 and 1799 trims.

Verification is arithmetic + content: the moved text must appear byte-for-byte in
the new archive, the prior archive must be untouched, and the live file must equal
the computed keep half.
"""
import sys

LIVE = "/root/agent/tasks/queue.md"
ARCH = "/root/agent/tasks/queue_archive.md"
FIRST_MOVE = 405          # 1-indexed: the "DONE (cycle 1872, ..." line
LABEL = "queue.md"

HEADER = (
    "## Archived by cycle 1884 (opus-5), 2026-10-18 — {label} had grown to "
    "{lines} lines / {kb}KB and `bin/check-doc-size` reported TRIM DUE (~10 "
    "cycles of headroom left against the 256KB Read-tool cap at the measured "
    "+5440 B/cycle). Cycles <=1871 moved here verbatim; the live file keeps the "
    "newest contiguous run of blocks (1872 up to 1883, plus the NEXT 1884 "
    "block). Newest-first below, same order as the source file.\n"
)

with open(LIVE, encoding="utf-8") as f:
    orig = f.read()
lines = orig.splitlines(keepends=True)
n = len(lines)
kb = round(len(orig.encode()) / 1024)

idx = FIRST_MOVE - 1
keep = lines[:idx]
moved = lines[idx:]

# Drop the separator ('---' + surrounding blanks) left dangling at the end of the
# kept half, so the live file ends on real content.
while keep and keep[-1].strip() in ("", "---"):
    keep.pop()
dropped = idx - len(keep)

problems = []
if dropped > 3:
    problems.append(f"dropped {dropped} separator lines, expected <=3")
if not moved:
    problems.append("nothing to move")
elif "cycle 1872" not in moved[0]:
    problems.append(f"first moved line is not the 1872 block: {moved[0][:90]!r}")
if "cycle 1883" not in "".join(keep):
    problems.append("cycle 1883 block missing from kept half")
if "NEXT (cycle 1884" not in "".join(keep):
    problems.append("NEXT 1884 block missing from kept half")
if problems:
    for p in problems:
        print(f"ABORT {LABEL}: {p}")
    sys.exit(1)

keep_txt = "".join(keep)
if not keep_txt.endswith("\n"):
    keep_txt += "\n"
moved_txt = "".join(moved)

with open(ARCH, encoding="utf-8") as f:
    arch_before = f.read()
sep = "" if arch_before.endswith("\n\n") else ("\n" if arch_before.endswith("\n") else "\n\n")
new_arch = arch_before + sep + HEADER.format(label=LABEL, lines=n, kb=kb) + "\n" + moved_txt

with open(ARCH, "w", encoding="utf-8") as f:
    f.write(new_arch)
with open(LIVE, "w", encoding="utf-8") as f:
    f.write(keep_txt)

# --- post-write verification ---
with open(ARCH, encoding="utf-8") as f:
    arch_after = f.read()
with open(LIVE, encoding="utf-8") as f:
    live_after = f.read()

if moved_txt not in arch_after:
    problems.append("moved text NOT found verbatim in archive")
if arch_before not in arch_after:
    problems.append("pre-existing archive content was altered")
missing = [l for l in moved if l.strip() and l not in arch_after]
if missing:
    problems.append(f"{len(missing)} moved lines missing from archive")
if live_after != keep_txt:
    problems.append("live file does not match computed keep half")
# every non-blank ORIGINAL line must survive in live+archive
both = live_after + "\n" + arch_after
lost = [l for l in lines if l.strip() and l not in both]
if lost:
    problems.append(f"{len(lost)} original lines missing from live+archive")

print(f"{LABEL}: {n} lines / {kb}KB -> {len(live_after.splitlines())} kept "
      f"({round(len(live_after.encode())/1024, 1)}KB), {len(moved)} moved, "
      f"{dropped} separator line(s) dropped")
print(f"  archive: {len(arch_before.splitlines())} -> {len(arch_after.splitlines())} lines")
if problems:
    for p in problems:
        print(f"  FAIL: {p}")
    sys.exit(1)
print("  OK: lossless (moved text verbatim in archive, prior archive intact, "
      "every original non-blank line still present)")
