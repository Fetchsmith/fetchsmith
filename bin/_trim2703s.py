#!/usr/bin/env python3
"""One-shot trim of state/STATUS.md for cycle 2703 (103.2KB / 1245 lines, TRIM SOON).

check-doc-size read TRIM SOON on this file at preflight this cycle (103.2KB /
1245 lines, ~22 cycles of headroom at +4510 B/cycle, projected 209KB at the
checker's next automatic look in 24c). 2703 is a QUALITY/GROWTH slot
(2703 % 3 == 0), so per the c2220 follow-up and doc-trim cadence rule 2 this
cycle trims proactively rather than waiting for the TRIM DUE escalation.

Same stock method as 1836/.../2574/2652/2676: keep the newest N cycle blocks
live, append the remainder VERBATIM to state/STATUS_ARCHIVE.md under a dated
header, source order preserved. bin/check-status-blocks-kept (pre-commit)
rejects any commit where a cycle header present in STATUS.md is in neither the
new STATUS.md nor the new STATUS_ARCHIVE.md.

Structure re-derived fresh at 2703 (cadence rule 3, never pasted forward):
32 blocks, strictly newest-first, 2702 down to 2671, no gaps; every prefix
N=3..9 is contiguous, so KEEP_BLOCKS=5 is hole-free.

KEEP_BLOCKS = 5 -> the contiguous window 2698..2702 stays live; cycles <=2697
are archived. This cycle then prepends its own 2703 block on top.

Hazard grep run BEFORE this cut (cadence rule 1): 1025 archive-bound lines,
16 hits for "standing rule|only here|do not archive|no other home|rule N|
sole home" -- every one is a CITATION of the c2524 rule (homed in CLAUDE.md /
queue.md) or a cross-reference pointing AT queue.md as the rule's home (e.g.
"now a standing rule in queue.md"), not a unique home living only in this
range. CLEAN -- nothing rehomed.
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

assert len(lines) == 1245, f"expected 1245 lines, got {len(lines)} -- file changed, abort"

starts = [i for i, l in enumerate(lines) if header_cycle(l) is not None]
assert len(starts) == 32, f"expected 32 cycle blocks, got {len(starts)}"
assert starts[0] == 0, "file must begin with a cycle block"

block_cycles = [header_cycle(lines[i]) for i in starts]
expected_cycles = list(range(2702, 2670, -1))
assert block_cycles == expected_cycles, \
    f"blocks are not the expected newest-first sequence: {block_cycles}"

cut = starts[KEEP_BLOCKS]
keep = lines[:cut]
archived = lines[cut:]

keep_txt = "".join(keep)

with open(ARCHIVE) as f:
    old_archive = f.read()

addition = (
    f"\n## Archived at cycle 2703 (STATUS.md trim, `bin/_trim2703s.py`) -- "
    f"cycles 2671-2697\n\n" + "".join(archived)
)
new_archive = old_archive + addition

for ln in archived:
    if ln.strip() and ln not in addition:
        sys.exit(f"FAIL: archived line missing from addition: {ln[:90]!r}")

if keep_txt + "".join(archived) != "".join(lines):
    sys.exit("FAIL: keep+archived does not reconstruct the original byte-for-byte")
if not new_archive.startswith(old_archive):
    sys.exit("FAIL: pre-existing archive would not be preserved byte-identically")

kept_cycles = [header_cycle(l) for l in keep if header_cycle(l) is not None]
if kept_cycles != list(range(2702, 2697, -1)):
    sys.exit(f"FAIL: kept window is not the contiguous 2698..2702: {kept_cycles}")

with open(ARCHIVE, "w") as f:
    f.write(new_archive)
with open(SRC, "w") as f:
    f.write(keep_txt)

print("All verifications passed.")
print(f"live STATUS.md: {len(keep)} lines / {len(keep_txt.encode())/1024:.1f}KB "
      f"(kept cycles {kept_cycles[-1]}..{kept_cycles[0]})")
print(f"archived: {len(archived)} lines (cycles 2671-2697)")
