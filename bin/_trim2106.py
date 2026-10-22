#!/usr/bin/env python3
"""One-shot, lossless notes/LEARNINGS.md -> LEARNINGS_ARCHIVE.md trim for cycle 2106.

`bin/check-doc-size` rated notes/LEARNINGS.md WARN this cycle: 7759 lines (max 8000),
projected 8239 at its own next scheduled look (24c out) -- i.e. it will breach the
8000-line rule before anything is scheduled to look again (the script's own
projection logic flags this as WARN rather than TRIM DUE for LINE_DOCS, trusting a
QUALITY cycle to act on the warning rather than waiting for a hard breach). c2105
queued this exact check for the next QUALITY/GROWTH slot (c2106).

Moves the oldest contiguous chronological block (cycles 1672-2056, everything before
the "## Cycle 2060" header) to the end of the archive, same convention as the
cycle 1976 trim (APPENDED BY CYCLE marker, moved verbatim, newest-first highlights
block at the top of the live file left untouched). Cuts deep (to ~1234 live lines)
for ~300+ cycles of headroom at the registered 20 lines/cycle rate, matching 1976's
stated intent ("not just barely under the line").

Verification: every non-blank line of the original file must be found in
live+archive afterwards, the moved text must land verbatim in the archive, and the
pre-existing archive content must survive byte-for-byte as a prefix.
"""
import sys

LIVE = "/root/agent/notes/LEARNINGS.md"
ARCH = "/root/agent/notes/LEARNINGS_ARCHIVE.md"
FIRST_MOVE = 541   # 1-indexed: start of "## Cycle 1672" header
FIRST_KEEP = 7066  # 1-indexed: start of "## Cycle 2060" header
OLDEST_MOVED = 1672
NEWEST_MOVED = 2056  # last entry before the 2060 block (cycle 2056)
LABEL = "notes/LEARNINGS.md"

MARKER = (
    "# APPENDED BY CYCLE 2106 (2026-10-22) — cycles {oldest}-{newest}, moved verbatim "
    "from notes/LEARNINGS.md (live file was {lines} lines, WARN at the 8000-line trim "
    "rule and projected to breach it before the next scheduled check 24c out; trimmed "
    "to {kept} live lines for deep headroom, same convention as the cycle 1976 trim).\n"
)

with open(LIVE, encoding="utf-8") as f:
    orig = f.read()
lines = orig.splitlines(keepends=True)
n = len(lines)

head_idx = FIRST_MOVE - 1   # 0-indexed start of moved block
keep_idx = FIRST_KEEP - 1   # 0-indexed start of second kept half

head = lines[:head_idx]        # header + highlights block, untouched
moved = lines[head_idx:keep_idx]
tail = lines[keep_idx:]        # newest chronological entries, untouched

problems = []
if f"## Cycle {OLDEST_MOVED}" not in "".join(moved[:3]):
    problems.append(f"first moved line is not the {OLDEST_MOVED} block")
if f"## Cycle {NEWEST_MOVED}" not in "".join(moved):
    problems.append(f"last expected moved block (cycle {NEWEST_MOVED}) not found in moved half")
if "## Cycle 2060" not in "".join(tail[:3]):
    problems.append("kept tail does not start with the cycle 2060 block")
if not moved:
    problems.append("nothing to move")
if problems:
    for p in problems:
        print(f"ABORT {LABEL}: {p}")
    sys.exit(1)

head_txt = "".join(head)
moved_txt = "".join(moved)
tail_txt = "".join(tail)
if not tail_txt.endswith("\n"):
    tail_txt += "\n"
keep_txt = head_txt + tail_txt

with open(ARCH, encoding="utf-8") as f:
    arch_before = f.read()

sep = "" if arch_before.endswith("\n\n") else ("\n" if arch_before.endswith("\n") else "\n\n")
marker = MARKER.format(oldest=OLDEST_MOVED, newest=NEWEST_MOVED, lines=n,
                        kept=len(keep_txt.splitlines()))
new_arch = arch_before + sep + marker + "\n" + moved_txt

with open(ARCH, "w", encoding="utf-8") as f:
    f.write(new_arch)
with open(LIVE, "w", encoding="utf-8") as f:
    f.write(keep_txt)

with open(ARCH, encoding="utf-8") as f:
    arch_after = f.read()
with open(LIVE, encoding="utf-8") as f:
    live_after = f.read()

if not arch_after.startswith(arch_before):
    problems.append("pre-existing archive content is not an intact prefix")
if moved_txt not in arch_after:
    problems.append("moved text NOT found verbatim in archive")
if live_after != keep_txt:
    problems.append("live file does not match computed keep text")
both = live_after + "\n" + arch_after
lost = [l for l in lines if l.strip() and l not in both]
if lost:
    problems.append(f"{len(lost)} original non-blank lines missing from live+archive")

print(f"{LABEL}: {n} lines -> {len(live_after.splitlines())} kept "
      f"({round(len(live_after.encode())/1024, 1)}KB), {len(moved)} moved "
      f"(cycles {OLDEST_MOVED}-{NEWEST_MOVED})")
print(f"  archive: {len(arch_before.splitlines())} -> {len(arch_after.splitlines())} lines "
      f"(appended at end)")
if problems:
    for p in problems:
        print(f"  FAIL: {p}")
    sys.exit(1)
print("  OK: lossless (moved text verbatim in archive, prior archive intact as a "
      "byte-exact prefix, every original non-blank line still present)")
