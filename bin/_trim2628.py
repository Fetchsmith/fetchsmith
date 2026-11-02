#!/usr/bin/env python3
"""One-shot trim of state/STATUS.md for cycle 2628 (121.3KB / 1516 lines, TRIM SOON).

check-doc-size read TRIM SOON at this cycle's preflight (121.3KB/1516 lines,
~18 cycles of headroom at +4510 B/cycle, proj. 227KB at the checker's next
automatic look) and said in as many words: "trim proactively in a QUALITY
slot rather than waiting for the escalation (cycle 2220 follow-up)". Cycle
2628 IS a QUALITY/GROWTH slot (2628 % 3 == 0), so this is that trim.

Same stock method as 1836/.../2574/2605: keep the newest N cycle blocks
live, append the remainder VERBATIM to state/STATUS_ARCHIVE.md under a
dated header, source order preserved. No open items are interleaved here,
so a block-boundary cut is safe; every block must still land in the
archive -- bin/check-status-blocks-kept (pre-commit) checks this.

Structure at 2628: 28 blocks, strictly newest-first, 2627 down to 2600, no
gaps (the PRIOR-cycle header form is handled by the same regex).

KEEP_BLOCKS = 5 -> the contiguous window 2623..2627 stays live; cycles
<=2622 are archived. Run BEFORE this cycle's own block is prepended.
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

assert len(lines) == 1516, f"expected 1516 lines, got {len(lines)} -- file changed, abort"

starts = [i for i, l in enumerate(lines) if header_cycle(l) is not None]
assert len(starts) == 28, f"expected 28 cycle blocks, got {len(starts)}"
assert starts[0] == 0, "file must begin with a cycle block"

block_cycles = [header_cycle(lines[i]) for i in starts]
expected_cycles = list(range(2627, 2599, -1))
assert block_cycles == expected_cycles, \
    f"blocks are not the expected newest-first sequence: {block_cycles}"

cut = starts[KEEP_BLOCKS]
keep = lines[:cut]
archived = lines[cut:]

keep_txt = "".join(keep)

with open(ARCHIVE) as f:
    old_archive = f.read()

addition = (
    f"\n## Archived at cycle 2628 (STATUS.md trim, `bin/_trim2628.py`) -- "
    f"cycles 2600-2622\n\n" + "".join(archived)
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
