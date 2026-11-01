#!/usr/bin/env python3
"""One-shot trim of state/STATUS.md for cycle 2553 (110.5KB / 1329 lines).

check-doc-size read TRIM SOON on this file at preflight this cycle (107.9KB /
1329 lines, ~21 cycles of headroom at +4510 B/cycle, projected 214KB at the
checker's next automatic look in 24c), and c2550/c2552's handoffs both
explicitly assigned the trim to this QUALITY/GROWTH slot (2553 % 3 == 0) --
the designated proactive-trim point (c2220 follow-up), rather than waiting
for the TRIM DUE escalation.

Same stock method as 1836/.../2511/2532: keep the newest N cycle blocks live,
append the remainder VERBATIM to state/STATUS_ARCHIVE.md under a dated header,
source order preserved. STATUS.md carries no standing `- [ ]` open items
interleaved among the cycle blocks, so a block-boundary cut is safe here (no
hoist-then-cut needed, unlike queue.md).

Structure at 2553: 26 blocks, strictly newest-first by cycle number, 2552 down
to 2527, NO gaps -- confirming every block the c2532 trim left live
(2527..2531) plus every cycle's own addition since (2532..2552) survived
intact.

KEEP_BLOCKS = 5 -> the contiguous window 2548..2552 stays live; cycles <=2547
are archived.
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

assert len(lines) == 1329, f"expected 1329 lines, got {len(lines)} -- file changed, abort"

starts = [i for i, l in enumerate(lines) if header_cycle(l) is not None]
assert len(starts) == 26, f"expected 26 cycle blocks, got {len(starts)}"
assert starts[0] == 0, "file must begin with a cycle block"

block_cycles = [header_cycle(lines[i]) for i in starts]
expected_cycles = list(range(2552, 2526, -1))
assert block_cycles == expected_cycles, \
    f"blocks are not the expected newest-first sequence: {block_cycles}"

cut = starts[KEEP_BLOCKS]
keep = lines[:cut]
archived = lines[cut:]
assert header_cycle(lines[starts[KEEP_BLOCKS - 1]]) == 2548, "kept-oldest block is not 2548"
assert header_cycle(lines[cut]) == 2547, "archive-newest block is not 2547"

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
    "\n## Archived by cycle 2553 (sonnet-5), 2026-11-01 -- STATUS.md had grown to 1329 lines / "
    "107.9KB, flagged TRIM SOON at this cycle's preflight (~21 cycles of headroom, projected "
    "214KB at check-doc-size's next look in 24c) and assigned to this QUALITY/GROWTH slot by "
    "c2550/c2552's handoffs; trimmed proactively rather than waiting for the TRIM DUE "
    "escalation. Cycles <=2547 moved here verbatim, in source order; the live file keeps the "
    "newest 5 blocks (the contiguous window 2548..2552). The source file's 26 blocks were "
    "strictly newest-first with NO gaps (2552 down to 2527) -- confirming every block the "
    "c2532 trim left live (2527..2531) plus every cycle's own addition since (2532..2552) "
    "survived intact, so no cycle's record was destroyed between the c2532 trim and now.\n\n"
)
addition = header + archived_txt
new_archive = old_archive + addition

for ln in archived:
    if ln.strip() and ln not in addition:
        sys.exit(f"FAIL: archived line missing from addition: {ln[:90]!r}")

dropped_lines = lines[len(keep):cut]
if any(l.strip() not in ("", "---") for l in dropped_lines):
    sys.exit(f"FAIL: a dropped separator line has real content: {dropped_lines!r}")
if "".join(keep) + "".join(dropped_lines) + "".join(archived) != "".join(lines):
    sys.exit("FAIL: kept + dropped + archived does not reconstruct the original file")

with open(SRC, "w") as f:
    f.write(keep_txt)
with open(ARCHIVE, "w") as f:
    f.write(new_archive)

print(f"STATUS.md: {len(lines)} -> {len(keep_txt.splitlines())} lines "
      f"({len(''.join(lines))} -> {len(keep_txt)} bytes)")
print(f"Archived {len(archived)} lines to {ARCHIVE}")
