#!/usr/bin/env python3
"""One-shot trim of state/STATUS.md for cycle 2781 (118.5KB / 1624 lines, TRIM SOON).

check-doc-size read TRIM SOON this cycle (118.5KB/1624 lines, ~19 cycles of headroom at
+4510 B/cycle, projected 224KB at next automatic look in 24c). 2781 is the designated
QUALITY slot (2781 % 3 == 0) that c2780 named for this exact cut.

Same stock method as 2574/2703s/2733s/2757s: keep the newest N cycle blocks live, append
the remainder VERBATIM to state/STATUS_ARCHIVE.md under a dated header, source order
preserved. No open items are interleaved here (that's queue.md's problem), so a
block-boundary cut is safe, but every block must still land in the archive --
bin/check-status-blocks-kept (pre-commit) rejects any commit where a cycle header present
in HEAD's STATUS.md is in neither the new STATUS.md nor the new STATUS_ARCHIVE.md.

Structure at 2781: 29 blocks, strictly newest-first, 2780 down to 2752, no gaps.

Hazard grep (rule 1) run first over the archive-bound range (lines 358-1624): six hits,
all references to rules already homed elsewhere, not new standing rules -- no rescue
needed. In particular the c2760 "standby Actor does NOT pick up a new build on push"
discovery (line ~1129) explicitly states "In LEARNINGS.md" and is confirmed present there
(LEARNINGS.md:6845, "Cycle 2760"); the c2751 prepend-block rule reference was already
rescued at the 2757s trim.

KEEP_BLOCKS = 5 -> the contiguous window 2776..2780 stays live; cycles <=2775 are archived.
This cycle then prepends its own 2781 block on top, as every post-trim cycle does.
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

assert len(lines) == 1624, f"expected 1624 lines, got {len(lines)} -- file changed, abort"

starts = [i for i, l in enumerate(lines) if header_cycle(l) is not None]
assert len(starts) == 29, f"expected 29 cycle blocks, got {len(starts)}"
assert starts[0] == 0, "file must begin with a cycle block"

block_cycles = [header_cycle(lines[i]) for i in starts]
expected_cycles = list(range(2780, 2751, -1))
assert block_cycles == expected_cycles, \
    f"blocks are not the expected newest-first sequence: {block_cycles}"

cut = starts[KEEP_BLOCKS]
keep = lines[:cut]
archived = lines[cut:]

keep_txt = "".join(keep)

with open(ARCHIVE) as f:
    old_archive = f.read()

addition = (
    f"\n## Archived at cycle 2781 (STATUS.md trim, `bin/_trim2781s.py`) -- "
    f"cycles 2752-2775\n\n" + "".join(archived)
)
new_archive = old_archive + addition

for ln in archived:
    if ln.strip() and ln not in addition:
        sys.exit(f"FAIL: archived line missing from addition: {ln[:90]!r}")

if "".join(keep) + "".join(archived) != "".join(lines):
    sys.exit("FAIL: kept + archived does not reconstruct the original file")

if not (len(keep_txt) < len(''.join(lines))):
    sys.exit("FAIL: new STATUS.md is not strictly smaller")
if not (len(new_archive) > len(old_archive)):
    sys.exit("FAIL: archive did not grow")

with open(SRC, "w") as f:
    f.write(keep_txt)
with open(ARCHIVE, "w") as f:
    f.write(new_archive)

print(f"STATUS.md: {len(lines)} -> {len(keep_txt.splitlines())} lines "
      f"({len(''.join(lines))} -> {len(keep_txt)} bytes)")
print(f"Archived {len(archived)} lines to {ARCHIVE}")
