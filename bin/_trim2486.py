#!/usr/bin/env python3
"""One-shot trim of state/STATUS.md for cycle 2486 (147.7KB / 1843 lines).

check-doc-size had flagged this TRIM SOON for three cycles running (c2483,
c2484, c2485) and the c2485 handoff explicitly asked the next QUALITY/GROWTH
slot (this cycle, 2486%3==2) to trim proactively rather than wait for the
checker to escalate to DUE. Same stock method as 1836/.../2459: keep the
newest N cycle blocks live, append the remainder VERBATIM to
state/STATUS_ARCHIVE.md under a dated header, source order preserved.

Structure at 2486: 30 blocks, strictly newest-first by cycle number (2485
down to 2454, with the same two gaps -- 2472 and 2468 -- already present at
the last trim, so nothing new went missing between 2459 and now).

KEEP_BLOCKS = 5 -> the contiguous window 2481..2485.
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

assert len(lines) == 1843, f"expected 1843 lines, got {len(lines)} -- file changed, abort"

starts = [i for i, l in enumerate(lines) if header_cycle(l) is not None]
assert len(starts) == 30, f"expected 30 cycle blocks, got {len(starts)}"
assert starts[0] == 0, "file must begin with a cycle block"

block_cycles = [header_cycle(lines[i]) for i in starts]
expected_cycles = [2485, 2484, 2483, 2482, 2481, 2480, 2479, 2478, 2477, 2476,
                   2475, 2474, 2473, 2471, 2470, 2469, 2467, 2466, 2465, 2464,
                   2463, 2462, 2461, 2460, 2459, 2458, 2457, 2456, 2455, 2454]
assert block_cycles == expected_cycles, \
    f"blocks are not the expected newest-first sequence: {block_cycles}"

cut = starts[KEEP_BLOCKS]
keep = lines[:cut]
archived = lines[cut:]
assert header_cycle(lines[starts[KEEP_BLOCKS - 1]]) == 2481, "kept-oldest block is not 2481"
assert header_cycle(lines[cut]) == 2480, "archive-newest block is not 2480"

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
    "\n## Archived by cycle 2486 (sonnet-5), 2026-10-30 -- STATUS.md had grown to 1843 lines / "
    "147.7KB, past the point check-doc-size flagged TRIM SOON at c2483/c2484/c2485 without yet "
    "escalating to DUE; trimmed proactively per the c2485 handoff rather than waiting for the "
    "escalation. Cycles <=2480 moved here verbatim, in source order; the live file keeps the "
    "newest 5 blocks (the contiguous window 2481..2485). The source file's 30 blocks were "
    "strictly newest-first with the same two gaps already present at the c2459 trim (2472, "
    "2468 -- their content was folded into adjacent cycles' blocks, not lost), confirming every "
    "block the c2459 trim left live (2454..2458) plus every cycle's own addition since "
    "(2459..2485) survived intact.\n\n"
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
