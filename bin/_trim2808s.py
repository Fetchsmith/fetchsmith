#!/usr/bin/env python3
"""One-shot trim of state/STATUS.md for cycle 2808 (107.5KB / 1671 lines, TRIM SOON).

check-doc-size read TRIM SOON on BOTH live docs at this cycle's preflight
(STATUS.md 107.5KB/1671 lines, ~21 cycles of headroom at +4510 B/cycle,
projected 213KB at the checker's next automatic look in 24c). 2808 is a
QUALITY/GROWTH slot (2808 % 3 == 0) and c2807 named this slot for the trim:
c2805 trimmed queue.md but explicitly left STATUS.md untouched as out of scope
for one slot, and c2807's preflight deferred it again. Per the doc-trim item's
standing rule 2 (do not let a second QUALITY slot pass) this is the slot.

Same stock method as 1836/.../2532/2574: keep the newest N cycle blocks live,
append the remainder VERBATIM to state/STATUS_ARCHIVE.md under a dated header,
source order preserved. No open items are interleaved here (that is queue.md's
problem), so a block-boundary cut is safe, but every block must still land in
the archive -- bin/check-status-blocks-kept (pre-commit) rejects any commit
where a cycle header present in HEAD's STATUS.md is in neither the new
STATUS.md nor the new STATUS_ARCHIVE.md.

Structure re-derived fresh at 2808 (standing rule 3 -- never paste forward):
32 blocks, strictly newest-first, 2807 down to 2776, no gaps.

KEEP_BLOCKS = 5 -> the contiguous window 2803..2807 stays live; cycles <=2802
are archived. This cycle then prepends its own 2808 block on top, as every
post-trim cycle does.

Rule-1 hazard grep ran BEFORE this cut over the archive-bound region (blocks
2802..2776) for standing-rule/cadence phrasing: 12 hits, all narrative *about*
a cadence homed elsewhere. The three that read most like instructions were
read in full -- the c2796 argv-default find ("standing rule now at the top of
`queue.md`, write-up in `LEARNINGS.md` c2796"), the c2792 unit_price trap
("recorded as a standing rule in `queue.md`"), and the c2380 per-niche
re-sweep cadence ("the c2380 follow-up's own instruction") -- and each names
its real home explicitly. Nothing unique to STATUS.md is lost.

Rule-4 margin arithmetic: post-cut 17.7KB + (4510 B/cycle * 24c to the next
look) = ~126KB, i.e. ~74KB clear of the 200KB trim line. A block-boundary cut
alone is sufficient for this file; no OPEN-text compression needed here.
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

assert len(lines) == 1671, f"expected 1671 lines, got {len(lines)} -- file changed, abort"

starts = [i for i, l in enumerate(lines) if header_cycle(l) is not None]
assert len(starts) == 32, f"expected 32 cycle blocks, got {len(starts)}"
assert starts[0] == 0, "file must begin with a cycle block"

block_cycles = [header_cycle(lines[i]) for i in starts]
expected_cycles = list(range(2807, 2775, -1))
assert block_cycles == expected_cycles, \
    f"blocks are not the expected newest-first sequence: {block_cycles}"

cut = starts[KEEP_BLOCKS]
keep = lines[:cut]
archived = lines[cut:]

assert header_cycle(keep[0]) == 2807, "kept window must start at 2807"
assert header_cycle(archived[0]) == 2802, "archive must start at 2802"

keep_txt = "".join(keep)

with open(ARCHIVE) as f:
    old_archive = f.read()

addition = (
    f"\n## Archived at cycle 2808 (STATUS.md trim, `bin/_trim2808s.py`) -- "
    f"cycles 2776-2802\n\n" + "".join(archived)
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
print(f"Archived {len(archived)} lines (cycles 2776-2802) to {ARCHIVE}")
