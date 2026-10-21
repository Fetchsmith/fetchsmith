#!/usr/bin/env python3
"""One-shot, lossless STATUS.md -> STATUS_ARCHIVE.md trim for cycle 2027.

`bin/check-doc-size` rated state/STATUS.md **TRIM DUE** this cycle at
158.6KB / 2102 lines (past the 150KB warn line, ~9c headroom at +4510 B/cycle,
projected 264KB at its own next look). queue.md (51.9KB) and LEARNINGS.md
(6726 lines) both rated OK, left untouched.

Keeps the newest 10 cycle blocks (2026 down to 2017); the cycle-2016 block
and everything older (down to 1994) is moved verbatim to the archive.

Archive placement: PREPENDED at the top under a `PRIOR (cycles ...)` header,
matching cycle 2004's convention (newest-archived-first at the top).
Pre-existing archive bytes are asserted byte-identical and present as a
contiguous suffix afterwards.
"""
import sys

LIVE = "/root/agent/state/STATUS.md"
ARCH = "/root/agent/state/STATUS_ARCHIVE.md"
FIRST_MOVE = 736          # 1-indexed: the "Updated: ... cycle 2016 ..." line
OLDEST_MOVED = 1994
NEWEST_MOVED = 2016
LABEL = "STATUS.md"

HEADER = (
    "PRIOR (cycles {oldest}-{newest}, archived by cycle 2027): {label} was {lines} "
    "lines / {kb}KB and `bin/check-doc-size` rated it TRIM DUE (158.6KB, past the "
    "150KB warn line, projected 264KB at its own next look). Cycles <={newest} moved "
    "here verbatim; the live file keeps the newest 10 cycle blocks (2026 down to "
    "2017). Newest-first below, same order as the source file.\n"
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
elif f"cycle {NEWEST_MOVED}" not in moved[0]:
    problems.append(f"first moved line is not the {NEWEST_MOVED} block: {moved[0][:90]!r}")
moved_txt_probe = "".join(moved)
if f"cycle {OLDEST_MOVED}" not in moved_txt_probe:
    problems.append(f"oldest block (cycle {OLDEST_MOVED}) not in the moved half")
keep_txt_probe = "".join(keep)
for c in range(2017, 2027):
    if f"cycle {c} " not in keep_txt_probe:
        problems.append(f"cycle {c} block missing from kept half")
if f"cycle {NEWEST_MOVED} (" in keep_txt_probe:
    problems.append(f"cycle {NEWEST_MOVED} block still present in kept half")
if problems:
    for p in problems:
        print(f"ABORT {LABEL}: {p}")
    sys.exit(1)

keep_txt = keep_txt_probe
if not keep_txt.endswith("\n"):
    keep_txt += "\n"
moved_txt = moved_txt_probe
if not moved_txt.endswith("\n"):
    moved_txt += "\n"

with open(ARCH, encoding="utf-8") as f:
    arch_before = f.read()

chunk = (HEADER.format(label=LABEL, lines=n, kb=kb, oldest=OLDEST_MOVED,
                       newest=NEWEST_MOVED) + "\n" + moved_txt + "\n")
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
if len(arch_after) != len(chunk) + len(arch_before):
    problems.append("archive byte count != chunk + prior archive")
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
print(f"  archive: {len(arch_before.splitlines())} -> {len(arch_after.splitlines())} lines "
      f"(prepended, newest chunk at top)")
if problems:
    for p in problems:
        print(f"  FAIL: {p}")
    sys.exit(1)
print("  OK: lossless (moved text verbatim in archive, prior archive intact as a "
      "byte-exact suffix, every original non-blank line still present)")
