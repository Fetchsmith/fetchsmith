#!/usr/bin/env python3
"""One-shot trim of state/STATUS.md for cycle 2574 (116.9KB / 1427 lines, TRIM SOON).

check-doc-size read TRIM SOON on this file at preflight this cycle (116.9KB /
1427 lines, ~19 cycles of headroom at +4510 B/cycle, projected 223KB at the
checker's next automatic look in 24c). 2574 is a QUALITY/GROWTH slot
(2574 % 3 == 0) and all checks-due/audit-due axes read NONE DUE, so per the
c2220 follow-up this cycle trims proactively rather than waiting for TRIM DUE.

Same stock method as 1836/.../2511/2532: keep the newest N cycle blocks live,
append the remainder VERBATIM to state/STATUS_ARCHIVE.md under a dated header,
source order preserved. No open items are interleaved here (that is queue.md's
problem), so a block-boundary cut is safe, but every block must still land in
the archive -- bin/check-status-blocks-kept (pre-commit) rejects any commit
where a cycle header present in HEAD's STATUS.md is in neither the new
STATUS.md nor the new STATUS_ARCHIVE.md.

Structure at 2574: 26 blocks, strictly newest-first, 2573 down to 2548, no gaps.

KEEP_BLOCKS = 5 -> the contiguous window 2569..2573 stays live; cycles <=2568
are archived. This cycle then prepends its own 2574 block on top, as every
post-trim cycle does.
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

assert len(lines) == 1427, f"expected 1427 lines, got {len(lines)} -- file changed, abort"

starts = [i for i, l in enumerate(lines) if header_cycle(l) is not None]
assert len(starts) == 26, f"expected 26 cycle blocks, got {len(starts)}"
assert starts[0] == 0, "file must begin with a cycle block"

block_cycles = [header_cycle(lines[i]) for i in starts]
expected_cycles = list(range(2573, 2547, -1))
assert block_cycles == expected_cycles, \
    f"blocks are not the expected newest-first sequence: {block_cycles}"

cut = starts[KEEP_BLOCKS]
keep = lines[:cut]
archived = lines[cut:]

keep_txt = "".join(keep)

with open(ARCHIVE) as f:
    old_archive = f.read()

addition = (
    f"\n## Archived at cycle 2574 (STATUS.md trim, `bin/_trim2574.py`) -- "
    f"cycles 2548-2568\n\n" + "".join(archived)
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
