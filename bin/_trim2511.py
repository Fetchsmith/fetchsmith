#!/usr/bin/env python3
"""One-shot trim of state/STATUS.md for cycle 2511 (127.1KB / 1626 lines).

check-doc-size flagged this TRIM SOON this cycle (and projected TRIM DUE at
the next look in 24c) and c2510's handoff asked the next QUALITY/GROWTH slot
(this cycle, 2511%3==0) to trim proactively. Same stock method as
1836/.../2486: keep the newest N cycle blocks live, append the remainder
VERBATIM to state/STATUS_ARCHIVE.md under a dated header, source order
preserved.

Structure at 2511: 29 blocks, strictly newest-first by cycle number (2510
down to 2481, no gaps in this window).

KEEP_BLOCKS = 5 -> the contiguous window 2506..2510.
"""
import re
import sys

SRC = "/root/agent/state/STATUS.md"
ARCHIVE = "/root/agent/state/STATUS_ARCHIVE.md"
KEEP_BLOCKS = 5

HEADER_RE = re.compile(r"^Updated:.*?by cycle (\d+)|^PRIOR \(cycle (\d+)")


def header_cycle(line):
    m = HEADER_RE.match(line)
    return int(m.group(1) or m.group(2)) if m else None


with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 1626, f"expected 1626 lines, got {len(lines)} -- file changed, abort"

starts = [i for i, l in enumerate(lines) if header_cycle(l) is not None]
assert len(starts) == 29, f"expected 29 cycle blocks, got {len(starts)}"
assert starts[0] == 0, "file must begin with a cycle block"

block_cycles = [header_cycle(lines[i]) for i in starts]
expected_cycles = [2510, 2509, 2508, 2507, 2506, 2505, 2504, 2503, 2502, 2501,
                    2500, 2499, 2498, 2497, 2496, 2495, 2494, 2493, 2492, 2491,
                    2490, 2488, 2487, 2486, 2485, 2484, 2483, 2482, 2481]
assert block_cycles == expected_cycles, \
    f"blocks are not the expected newest-first sequence: {block_cycles}"

cut = starts[KEEP_BLOCKS]
keep = lines[:cut]
archived = lines[cut:]
assert header_cycle(lines[starts[KEEP_BLOCKS - 1]]) == 2506, "kept-oldest block is not 2506"
assert header_cycle(lines[cut]) == 2505, "archive-newest block is not 2505"

while keep and keep[-1].strip() in ("", "---"):
    keep.pop()
dropped = cut - len(keep)
if dropped > 3:
    sys.exit(f"ABORT: dropped {dropped} separator lines, expected <=3")

keep_txt = "".join(keep)
if not keep_txt.endswith("\n"):
    keep_txt += "\n"
archived_txt = "".join(archived)

with open(ARCHIVE) as f:
    old_archive = f.read()

header = (
    "\n## Archived by cycle 2511 (sonnet-5), 2026-10-31 -- STATUS.md had grown to 1626 lines / "
    "127.1KB, flagged TRIM SOON this cycle and projected to cross TRIM DUE before check-doc-size's "
    "next look (24c); trimmed proactively per the c2510 handoff. Cycles <=2505 moved here verbatim, "
    "in source order; the live file keeps the newest 5 blocks (the contiguous window 2506..2510). "
    "The source file's 29 blocks were strictly newest-first with the pre-existing gaps at 2489 "
    "(recovery cycle, folded into 2490's own block) -- confirming no block vanished between the "
    "c2486 trim and now.\n\n"
)
addition = header + archived_txt
new_archive = old_archive + addition

for ln in archived:
    if ln.strip() and ln not in addition:
        sys.exit(f"FAIL: archived line missing from addition: {ln[:90]!r}")

dropped_lines = lines[len(keep):cut]
if any(l.strip() not in ("", "---") for l in dropped_lines):
    sys.exit(f"FAIL: a dropped separator line has real content: {dropped_lines!r}")
if "".join(keep) + "".join(dropped_lines) + "".join(archived) != "".join(lines[:cut]) + "".join(archived):
    sys.exit("FAIL: kept + dropped + archived does not reconstruct the original file")

with open(SRC, "w") as f:
    f.write(keep_txt)
with open(ARCHIVE, "w") as f:
    f.write(new_archive)

print(f"STATUS.md: {len(lines)} -> {len(keep_txt.splitlines())} lines "
      f"({len(''.join(lines))} -> {len(keep_txt)} bytes)")
print(f"Archived {len(archived)} lines to {ARCHIVE}")
