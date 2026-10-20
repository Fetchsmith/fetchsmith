#!/usr/bin/env python3
"""One-shot, lossless STATUS.md -> STATUS_ARCHIVE.md trim for cycle 2004.

`bin/check-doc-size` was DUE this cycle and reported state/STATUS.md **TRIM DUE**
at 163.4KB / 2159 lines: ~8 cycles of headroom at +4510 B/cycle, projected 269KB
at its own next look (24c out, cycle ~2028) -- past both the 200KB trim line and
the 256KB Read-tool cap, with no check scheduled in between. queue.md (111.2KB)
and notes/LEARNINGS.md (6270 lines) both rated OK, so they are left untouched.

Keeps the newest 10 cycle blocks (2003 down to 1994); the cycle-1993 block and
everything older (down to 1968) is moved verbatim to the archive.

Archive placement: **PREPENDED** at the top under a `PRIOR (cycles ...)` header,
matching the most recent STATUS trim (cycle 1983, whose chunk is currently the
archive's first line) rather than the older append-to-end shape of _trim1958.py.
Reason: newest-archived-first at the top is what a reader paging the 7MB archive
wants to hit first. Pre-existing archive bytes are asserted byte-identical and
present as a contiguous suffix afterwards.
"""
import sys

LIVE = "/root/agent/state/STATUS.md"
ARCH = "/root/agent/state/STATUS_ARCHIVE.md"
FIRST_MOVE = 611          # 1-indexed: the "Updated: ... cycle 1993 ..." line
OLDEST_MOVED = 1968
NEWEST_MOVED = 1993
LABEL = "STATUS.md"

HEADER = (
    "PRIOR (cycles {oldest}-{newest}, archived by cycle 2004): {label} was {lines} "
    "lines / {kb}KB and `bin/check-doc-size` -- DUE this cycle -- rated it TRIM DUE "
    "(projected 269KB at its own next look, 24c out, i.e. past both the 200KB trim "
    "line and the 256KB Read cap). Cycles <={newest} moved here verbatim; the live "
    "file keeps the newest 10 cycle blocks (2003 down to 1994). Newest-first below, "
    "same order as the source file.\n"
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
for c in range(1994, 2004):
    if f"cycle {c} " not in keep_txt_probe:
        problems.append(f"cycle {c} block missing from kept half")
if f"cycle {NEWEST_MOVED} (sonnet-5)" in keep_txt_probe:
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
