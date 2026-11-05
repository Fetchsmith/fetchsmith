#!/usr/bin/env python3
"""One-shot trim of state/STATUS.md for cycle 2757 (107.0KB / 1384 lines, TRIM SOON).

check-doc-size read TRIM SOON this cycle (107.0KB/1384 lines, ~21 cycles of headroom at
+4510 B/cycle, projected 213KB at next automatic look in 24c). c2756 explicitly named 2757
as the next QUALITY slot and the designated place to trim both STATUS.md and queue.md.

Same stock method as 2574/2703s/2733s: keep the newest N cycle blocks live, append the
remainder VERBATIM to state/STATUS_ARCHIVE.md under a dated header, source order preserved.
No open items are interleaved here (that's queue.md's problem), so a block-boundary cut is
safe, but every block must still land in the archive -- bin/check-status-blocks-kept
(pre-commit) rejects any commit where a cycle header present in HEAD's STATUS.md is in
neither the new STATUS.md nor the new STATUS_ARCHIVE.md.

Structure at 2757: 29 blocks, strictly newest-first, 2756 down to 2728, no gaps.

Hazard grep (rule 1) run first over the archive-bound range (lines 293-1384): one line read
like a standing rule outside this narrative (c2751's "every future STATUS.md edit: prepend
a new block, never replace the top one's header in place"). NOT previously homed in
LEARNINGS.md (checked, 0 hits) -- rescued verbatim into notes/LEARNINGS.md under a new
"c2751" header before running this cut. The other three grep hits (store_rank.json backup
rule, LEARNINGS.md:6014 reference, the c2733 trim's own prior hazard-grep note) are all
references to rules already homed elsewhere, not new rules -- no further rescue needed.

KEEP_BLOCKS = 5 -> the contiguous window 2752..2756 stays live; cycles <=2751 are archived.
This cycle then prepends its own 2757 block on top, as every post-trim cycle does.
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

assert len(lines) == 1384, f"expected 1384 lines, got {len(lines)} -- file changed, abort"

starts = [i for i, l in enumerate(lines) if header_cycle(l) is not None]
assert len(starts) == 29, f"expected 29 cycle blocks, got {len(starts)}"
assert starts[0] == 0, "file must begin with a cycle block"

block_cycles = [header_cycle(lines[i]) for i in starts]
expected_cycles = list(range(2756, 2727, -1))
assert block_cycles == expected_cycles, \
    f"blocks are not the expected newest-first sequence: {block_cycles}"

cut = starts[KEEP_BLOCKS]
keep = lines[:cut]
archived = lines[cut:]

keep_txt = "".join(keep)

with open(ARCHIVE) as f:
    old_archive = f.read()

addition = (
    f"\n## Archived at cycle 2757 (STATUS.md trim, `bin/_trim2757s.py`) -- "
    f"cycles 2728-2751\n\n" + "".join(archived)
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
