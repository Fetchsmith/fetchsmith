#!/usr/bin/env python3
"""One-shot trim of state/STATUS.md for cycle 2605 (101.8KB / 1248 lines, TRIM SOON).

check-doc-size read TRIM SOON (101.8KB/1248 lines, proj. 207KB at the
checker's next automatic look, c2629). Nothing else was DUE this cycle, so
per the c2220 follow-up and the doc-trim cadence item this cycle trims
proactively rather than waiting for TRIM DUE.

Same stock method as 1836/.../2532/2574: keep the newest N cycle blocks
live, append the remainder VERBATIM to state/STATUS_ARCHIVE.md under a
dated header, source order preserved. No open items are interleaved here,
so a block-boundary cut is safe; every block must still land in the
archive -- bin/check-status-blocks-kept (pre-commit) checks this.

Structure at 2605: 21 blocks, strictly newest-first, 2604 down to 2584, no
gaps (one PRIOR-cycle-2588 header handled by the same regex).

KEEP_BLOCKS = 5 -> the contiguous window 2600..2604 stays live; cycles
<=2599 are archived.
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

assert len(lines) == 1248, f"expected 1248 lines, got {len(lines)} -- file changed, abort"

starts = [i for i, l in enumerate(lines) if header_cycle(l) is not None]
assert len(starts) == 21, f"expected 21 cycle blocks, got {len(starts)}"
assert starts[0] == 0, "file must begin with a cycle block"

block_cycles = [header_cycle(lines[i]) for i in starts]
expected_cycles = list(range(2604, 2583, -1))
assert block_cycles == expected_cycles, \
    f"blocks are not the expected newest-first sequence: {block_cycles}"

cut = starts[KEEP_BLOCKS]
keep = lines[:cut]
archived = lines[cut:]

keep_txt = "".join(keep)

with open(ARCHIVE) as f:
    old_archive = f.read()

addition = (
    f"\n## Archived at cycle 2605 (STATUS.md trim, `bin/_trim2605.py`) -- "
    f"cycles 2584-2599\n\n" + "".join(archived)
)
new_archive = old_archive + addition

for ln in archived:
    if ln.strip() and ln not in addition:
        sys.exit(f"FAIL: archived line missing from addition: {ln[:90]!r}")

if "".join(keep) + "".join(archived) != "".join(lines):
    sys.exit("FAIL: kept + archived does not reconstruct the original file")

with open(SRC, "w") as f:
    f.write(keep_txt)
with open(ARCHIVE, "w") as f:
    f.write(new_archive)

print(f"STATUS.md: {len(lines)} -> {len(keep_txt.splitlines())} lines "
      f"({len(''.join(lines))} -> {len(keep_txt)} bytes)")
print(f"Archived {len(archived)} lines to {ARCHIVE}")
