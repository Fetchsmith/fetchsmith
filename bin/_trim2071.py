#!/usr/bin/env python3
"""One-shot, lossless state/STATUS.md -> STATUS_ARCHIVE.md trim for cycle 2071.

check-doc-size exited 1 this cycle (TRIM DUE: STATUS.md 155.9KB/2061 lines,
projected 262KB at its own next scheduled look (24c out) -- past the Read-tool
256KB cap). Keeps the newest 10 cycle blocks in the live file (2070 down to
2061), appends the remainder verbatim to the end of the existing archive under
a dated '## Archived by cycle 2071' header, same shape as the 1884/1932/1958/
1836/1799/2057 trims.

Verification is arithmetic + content: every archived line must appear in the
new archive, and keep+moved must reconstruct the original byte-for-byte.
"""
import sys

LIVE = "/root/agent/state/STATUS.md"
ARCH = "/root/agent/state/STATUS_ARCHIVE.md"
FIRST_MOVE = 701  # 1-indexed first line to MOVE (start of the cycle 2060 block)
LABEL = "STATUS.md"

HEADER = (
    "## Archived by cycle 2071 (sonnet-5), 2026-10-22 — {label} had grown to "
    "{lines} lines / {kb}KB, TRIM DUE per check-doc-size (projected past the "
    "Read-tool single-file cap, 256KB, at its next scheduled look). Cycles "
    "<=2060 moved here verbatim; the live file keeps the newest 10 cycle "
    "blocks (2070 down to 2061). Newest-first below, same order as the "
    "source file.\n"
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

if not moved:
    print(f"ABORT {LABEL}: nothing to move")
    sys.exit(1)
if "cycle 2060" not in moved[0]:
    print(f"ABORT {LABEL}: first moved line is not the 2060 block: {moved[0][:90]!r}")
    sys.exit(1)
if "2061" not in "".join(keep[-120:]):
    print(f"ABORT {LABEL}: cycle 2061 block missing from kept tail")
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
    problems.append("prior archive content NOT preserved")
if live_after != keep_txt:
    problems.append("live file does not match expected keep text")

if problems:
    print("ABORT:", "; ".join(problems))
    sys.exit(1)

print(f"OK: moved {len(moved)} lines ({len(moved_txt.encode())} bytes) from {LABEL}")
print(f"live now {len(keep)} lines / {round(len(keep_txt.encode())/1024,1)}KB")
print(f"archive now {len(arch_after.splitlines())} lines")
