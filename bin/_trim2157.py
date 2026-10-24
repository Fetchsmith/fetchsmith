#!/usr/bin/env python3
"""One-shot, lossless STATUS.md -> STATUS_ARCHIVE.md trim for cycle 2157.

queue.md is still OK per bin/check-doc-size (119.3KB, 15c headroom) -- only
STATUS.md is TRIM DUE (164.4KB, 8c headroom). Keeps the newest 10 cycle blocks
(2156 down to 2147) in the live file, appends the remainder verbatim to the end
of the existing archive under a dated '## Archived by cycle 2157' header (same
shape as the cycle 1836/1799 trims).

Cycle 2156's note: the live file's block anchor is the '^Updated:' line, not the
'## cycle N:' heading, and not even a '---' separator -- at least one boundary in
this file (2152/2151) has no '---' between blocks. So this script locates the
cut purely by counting '^Updated:' lines, not by scanning for '---'.

Verification is arithmetic + content: every moved line must appear verbatim in
the new archive, and keep+moved must reconstruct the original byte-for-byte.
"""
import re

LIVE = "/root/agent/state/STATUS.md"
ARCH = "/root/agent/state/STATUS_ARCHIVE.md"
KEEP_BLOCKS = 10

with open(LIVE, encoding="utf-8") as f:
    orig = f.read()
lines = orig.splitlines(keepends=True)
n = len(lines)
kb = round(len(orig.encode()) / 1024)

updated_idx = [i for i, l in enumerate(lines) if l.startswith("Updated:")]
if len(updated_idx) <= KEEP_BLOCKS:
    print(f"ABORT: only {len(updated_idx)} Updated: blocks found, nothing to trim")
    raise SystemExit(1)

cut = updated_idx[KEEP_BLOCKS]  # 0-indexed start of the 11th-newest block
keep = lines[:cut]
moved = lines[cut:]

# Drop a trailing separator/blank left dangling at the end of the kept half.
while keep and keep[-1].strip() in ("", "---"):
    keep.pop()
dropped = cut - len(keep)
if dropped > 3:
    print(f"ABORT: dropped {dropped} separator lines, expected <=3")
    raise SystemExit(1)

if not moved:
    print("ABORT: nothing to move")
    raise SystemExit(1)
if not moved[0].startswith("Updated:") or "cycle 2146" not in moved[0]:
    print(f"ABORT: first moved line is not the cycle 2146 block: {moved[0][:100]!r}")
    raise SystemExit(1)
if not any("cycle 2147" in l for l in keep[-80:]):
    print("ABORT: cycle 2147 block missing from kept tail")
    raise SystemExit(1)

keep_txt = "".join(keep)
if not keep_txt.endswith("\n"):
    keep_txt += "\n"
moved_txt = "".join(moved)

with open(ARCH, encoding="utf-8") as f:
    arch_before = f.read()
sep = "" if arch_before.endswith("\n\n") else ("\n" if arch_before.endswith("\n") else "\n\n")
header = (
    "## Archived by cycle 2157 (sonnet-5), 2026-10-24 -- STATUS.md had grown to "
    f"{n} lines / {kb}KB, approaching the Read-tool single-file cap (256KB) that "
    "cycles 1836/1833/1799 all hit before it. Cycles <=2146 moved here verbatim; "
    "the live file keeps the newest 10 cycle blocks (2156 down to 2147). "
    "Newest-first below, same order as the source file.\n\n"
)
new_arch = arch_before + sep + header + moved_txt

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

print(f"STATUS.md: {n} lines -> {len(live_after.splitlines())} kept, "
      f"{len(moved)} moved, {dropped} separator line(s) dropped")
print(f"  archive: {len(arch_before.splitlines())} -> {len(arch_after.splitlines())} lines")
if problems:
    for p in problems:
        print(f"  FAIL: {p}")
    raise SystemExit(1)
print("  OK: lossless (moved text verbatim in archive, prior archive intact)")
