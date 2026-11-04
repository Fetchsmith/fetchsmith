#!/usr/bin/env python3
"""One-shot trim of state/STATUS.md for cycle 2733 (108.9KB / 1552 lines, TRIM SOON).

check-doc-size read TRIM SOON on this file this cycle (108.9KB/1552 lines, ~21
cycles of headroom at +4510 B/cycle, projected 215KB at the checker's next
automatic look in 24c). This is the designated QUALITY slot (2733 % 3 == 0)
that queue.md's doc-trim cadence item names as the hard deadline (a third
deferral past 2730/2733 was ruled unacceptable in that item).

Same stock method as 1836/.../2574/2703s: keep the newest N cycle blocks
live, append the remainder VERBATIM to state/STATUS_ARCHIVE.md under a dated
header, source order preserved. No open items are interleaved here (that is
queue.md's problem), so a block-boundary cut is safe, but every block must
still land in the archive -- bin/check-status-blocks-kept (pre-commit)
rejects any commit where a cycle header present in HEAD's STATUS.md is in
neither the new STATUS.md nor the new STATUS_ARCHIVE.md.

Structure at 2733: 35 blocks, strictly newest-first, 2732 down to 2698, no gaps.

Hazard grep (rule 1) run first over the archive-bound range (lines 221-1552):
only one line read like a standing rule outside this narrative ("any
'replace in place / keep newest only' rule needs a mechanical new < old
assert in bytes" -- cycle 2712's block). Verified it is already homed
verbatim at notes/LEARNINGS.md:6014 before cutting, so no rescue needed.

KEEP_BLOCKS = 5 -> the contiguous window 2728..2732 stays live; cycles <=2727
are archived. This cycle then prepends its own 2733 block on top, as every
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

assert len(lines) == 1552, f"expected 1552 lines, got {len(lines)} -- file changed, abort"

starts = [i for i, l in enumerate(lines) if header_cycle(l) is not None]
assert len(starts) == 35, f"expected 35 cycle blocks, got {len(starts)}"
assert starts[0] == 0, "file must begin with a cycle block"

block_cycles = [header_cycle(lines[i]) for i in starts]
expected_cycles = list(range(2732, 2697, -1))
assert block_cycles == expected_cycles, \
    f"blocks are not the expected newest-first sequence: {block_cycles}"

cut = starts[KEEP_BLOCKS]
keep = lines[:cut]
archived = lines[cut:]

keep_txt = "".join(keep)

with open(ARCHIVE) as f:
    old_archive = f.read()

addition = (
    f"\n## Archived at cycle 2733 (STATUS.md trim, `bin/_trim2733s.py`) -- "
    f"cycles 2698-2727\n\n" + "".join(archived)
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
