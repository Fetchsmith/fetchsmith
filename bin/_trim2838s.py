#!/usr/bin/env python3
"""One-shot trim of state/STATUS.md for cycle 2838 (153.4KB / 2080 lines, TRIM DUE).

check-doc-size read TRIM DUE on state/STATUS.md at this cycle's preflight (153.4KB/2080
lines, ~11 cycles of headroom at +4510 B/cycle, projected 259KB at the checker's next
automatic look 24c out). 2838 is a QUALITY/GROWTH slot (2838 % 3 == 0), and the doc-trim
has been deferred three QUALITY slots running (c2832, c2835, c2836 each named c2838 as
the one to finally take it) -- per the doc-trim item's standing rule 2 (never let a
second QUALITY slot pass a TRIM DUE/SOON file) this is the slot.

Same stock method as 1836/.../2574/2808s: keep the newest N cycle blocks live, append
the remainder VERBATIM to state/STATUS_ARCHIVE.md under a dated header, source order
preserved. No open items are interleaved in STATUS.md (that is queue.md's problem), so a
block-boundary cut is safe, but every block must land in the archive -- bin/check-status-
blocks-kept (pre-commit) rejects any commit where a cycle header present in HEAD's
STATUS.md is in neither the new STATUS.md nor the new STATUS_ARCHIVE.md.

Structure re-derived fresh at 2838 (standing rule 3 -- never paste forward): 35 blocks,
strictly newest-first, 2837 down to 2803, no gaps (confirmed via grep "^Updated:").

KEEP_BLOCKS = 5 -> the contiguous window 2833..2837 stays live; cycles <=2832 are
archived. This cycle then prepends its own 2838 block on top, as every post-trim cycle
does.

Rule-1 hazard grep ran BEFORE this cut over the archive-bound region (lines 323-2080,
blocks 2832..2803): 26 hits for "standing rule|cadence|always|going forward|never do|
do not retrofit", all read, all narrative *about* a rule/cadence homed elsewhere
(queue.md's doc-trim cadence item, c2812 and c2796 standing rules, checks-due/audit-due
tool state, the MCP-#3 decision) -- none claims to be the sole live home of an active
instruction inside STATUS.md, which is a pure rolling status log, not a rules document.

Rule-4 margin arithmetic: 200KB - (4510 B/cycle * 24c to the next look) means a post-cut
size under ~91.8KB clears the line comfortably. Keeping only 5 blocks lands at ~25.1KB,
~38.7 cycles of headroom -- cut deep per the cycle-1976/2808 lesson that a shallow cut
re-flags almost immediately.
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

assert len(lines) == 2080, f"expected 2080 lines, got {len(lines)} -- file changed, abort"

starts = [i for i, l in enumerate(lines) if header_cycle(l) is not None]
assert len(starts) == 35, f"expected 35 cycle blocks, got {len(starts)}"
assert starts[0] == 0, "file must begin with a cycle block"

block_cycles = [header_cycle(lines[i]) for i in starts]
expected_cycles = list(range(2837, 2802, -1))
assert block_cycles == expected_cycles, \
    f"blocks are not the expected newest-first sequence: {block_cycles}"

cut = starts[KEEP_BLOCKS]
keep = lines[:cut]
archived = lines[cut:]

assert header_cycle(keep[0]) == 2837, "kept window must start at 2837"
assert header_cycle(archived[0]) == 2832, "archive must start at 2832"

keep_txt = "".join(keep)

with open(ARCHIVE) as f:
    old_archive = f.read()

addition = (
    f"\n## Archived at cycle 2838 (STATUS.md trim, `bin/_trim2838s.py`) -- "
    f"cycles 2803-2832\n\n" + "".join(archived)
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
print(f"Archived {len(archived)} lines (cycles 2803-2832) to {ARCHIVE}")
