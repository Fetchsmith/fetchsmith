#!/usr/bin/env python3
"""One-shot, lossless STATUS.md -> STATUS_ARCHIVE.md trim for cycle 1958.

`bin/check-doc-size` (run fresh this cycle) reported STATUS.md as **TRIM DUE**
at 150.4KB, ~11 cycles of headroom at +4510 B/cycle, projected to 256KB (the
Read-tool cap) by its own next scheduled look (24c out, cycle ~1982) -- same
early-trim judgement call as the cycle-1884/1932 trims (bin/_trim1932.py).
queue.md was OK this cycle (124.2KB) so left untouched.

Keeps the newest 10 cycle blocks (1957 down to 1947); everything from the
cycle-1946 block onward is appended verbatim to the end of the archive under
a dated header, same shape as the 1932 / 1884 / 1836 / 1799 trims.
"""
import sys

LIVE = "/root/agent/state/STATUS.md"
ARCH = "/root/agent/state/STATUS_ARCHIVE.md"
FIRST_MOVE = 479          # 1-indexed: the "Updated: ... cycle 1946 ..." line
LABEL = "STATUS.md"

HEADER = (
    "## Archived by cycle 1958 (sonnet-5), 2026-10-19 — {label} was {lines} lines "
    "/ {kb}KB. `bin/check-doc-size` reported it TRIM DUE this cycle (150.4KB, "
    "projected 256KB -- the Read-tool cap -- at its own next look, 24c out) so "
    "it was trimmed early, same judgement call as the cycle-1884/1932 trims. "
    "Cycles <=1946 moved here verbatim; the live file keeps the newest 10 cycle "
    "blocks (1957 down to 1947). Newest-first below, same order as the source "
    "file.\n"
)

with open(LIVE, encoding="utf-8") as f:
    orig = f.read()
lines = orig.splitlines(keepends=True)
n = len(lines)
kb = round(len(orig.encode()) / 1024, 1)

idx = FIRST_MOVE - 1
keep = lines[:idx]
moved = lines[idx:]

while keep and keep[-1].strip() in ("", "---"):
    keep.pop()
dropped = idx - len(keep)

problems = []
if dropped > 3:
    problems.append(f"dropped {dropped} separator lines, expected <=3")
if not moved:
    problems.append("nothing to move")
elif "cycle 1946" not in moved[0]:
    problems.append(f"first moved line is not the 1946 block: {moved[0][:90]!r}")
keep_txt_probe = "".join(keep)
if "cycle 1957" not in keep_txt_probe:
    problems.append("cycle 1957 block missing from kept half")
if "cycle 1947" not in keep_txt_probe:
    problems.append("cycle 1947 block missing from kept half")
if "cycle 1946 (sonnet-5)" in keep_txt_probe:
    problems.append("cycle 1946 block still present in kept half")
if problems:
    for p in problems:
        print(f"ABORT {LABEL}: {p}")
    sys.exit(1)

keep_txt = keep_txt_probe
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
