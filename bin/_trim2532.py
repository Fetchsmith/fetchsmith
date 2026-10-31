#!/usr/bin/env python3
"""One-shot trim of state/STATUS.md for cycle 2532 (103.1KB / 1320 lines).

check-doc-size read TRIM SOON on this file at preflight this cycle (103.1KB /
1320 lines, ~22 cycles of headroom at +4510 B/cycle, projected 209KB at the
checker's next automatic look in 24c), and c2531's handoff explicitly assigned
the trim to this cycle -- 2532 is a QUALITY/GROWTH slot (2532 % 3 == 0), which
is where check-doc-size itself says to trim proactively rather than waiting for
the TRIM DUE escalation (the c2220 follow-up).

Same stock method as 1836/.../2459/2486/2511: keep the newest N cycle blocks
live, append the remainder VERBATIM to state/STATUS_ARCHIVE.md under a dated
header, source order preserved. STATUS.md (unlike queue.md) carries no standing
`- [ ]` open items interleaved among the cycle blocks, so a block-boundary cut
is safe here and the hoist-then-cut dance the queue.md trims need is not
required -- but every block must still land in the archive, because
bin/check-status-blocks-kept (pre-commit) rejects any commit where a cycle
header present in HEAD's STATUS.md is in neither the new STATUS.md nor the new
STATUS_ARCHIVE.md.

Structure at 2532: 26 blocks, strictly newest-first by cycle number, 2531 down
to 2506 with NO gaps -- which also confirms that every block the c2511 trim left
live (2506..2510) plus every cycle's own addition since (2511..2531) survived
intact, i.e. no cycle's record was destroyed in that window.

KEEP_BLOCKS = 5 -> the contiguous window 2527..2531 stays live; cycles <=2526
are archived. This cycle then prepends its own 2532 block on top, as every
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

assert len(lines) == 1320, f"expected 1320 lines, got {len(lines)} -- file changed, abort"

starts = [i for i, l in enumerate(lines) if header_cycle(l) is not None]
assert len(starts) == 26, f"expected 26 cycle blocks, got {len(starts)}"
assert starts[0] == 0, "file must begin with a cycle block"

block_cycles = [header_cycle(lines[i]) for i in starts]
expected_cycles = list(range(2531, 2505, -1))
assert block_cycles == expected_cycles, \
    f"blocks are not the expected newest-first sequence: {block_cycles}"

cut = starts[KEEP_BLOCKS]
keep = lines[:cut]
archived = lines[cut:]
assert header_cycle(lines[starts[KEEP_BLOCKS - 1]]) == 2527, "kept-oldest block is not 2527"
assert header_cycle(lines[cut]) == 2526, "archive-newest block is not 2526"

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
    "\n## Archived by cycle 2532 (opus-5), 2026-10-31 -- STATUS.md had grown to 1320 lines / "
    "103.1KB, flagged TRIM SOON at this cycle's preflight (~22 cycles of headroom, projected "
    "209KB at check-doc-size's next look in 24c) and assigned to this QUALITY/GROWTH slot by "
    "c2531's handoff; trimmed proactively rather than waiting for the TRIM DUE escalation. "
    "Cycles <=2526 moved here verbatim, in source order; the live file keeps the newest 5 blocks "
    "(the contiguous window 2527..2531). The source file's 26 blocks were strictly newest-first "
    "with NO gaps (2531 down to 2506) -- confirming every block the c2511 trim left live "
    "(2506..2510) plus every cycle's own addition since (2511..2531) survived intact, so no "
    "cycle's record was destroyed between the c2511 trim and now. Rate re-measured: the file grew "
    "from the c2511 trim's post-cut 16.6KB to 103.1KB over the 21 blocks added since "
    "(2511..2531) = ~4,215 B/block actual, close to the checker's registered +4510 B/cycle.\n\n"
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
