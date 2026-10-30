#!/usr/bin/env python3
"""One-shot trim of state/STATUS.md for cycle 2459 (242.2KB / 2981 lines).

check-doc-size read TRIM DUE this cycle (~-10c headroom today, projecting
~348KB at its own next look, 24c -- well past both the 150KB warn and 200KB
trim lines). This is the QUALITY-slot (2459%3==2) trim it asked for, same
stock method as 1836/.../2411: keep the newest N cycle blocks live, append
the remainder VERBATIM to state/STATUS_ARCHIVE.md under a dated header,
source order preserved.

Structure at 2459: 53 blocks, strictly newest-first, 2458 down to 2406, no
gaps (2406..2458 is exactly 53 consecutive cycle numbers) -- this is the
live window the c2411 trim left (2406..2410) plus every cycle's own block
added since (2411..2458), confirming no block was lost between trims.

KEEP_BLOCKS = 5 -> the contiguous window 2454..2458.

  Rate re-measured fresh: file is 248,027 bytes over 53 blocks (2406..2458)
  added since the c2411 trim left it with 5 blocks live (2406..2410) at
  16,982 bytes. (248027-16982)/48 = 4,813 B/block actual, close to the
  checker's registered +4510 B/cycle. Keeping 5 (2454..2458) leaves the
  smallest live file that still matches the established precedent size;
  measured below after the cut.
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

assert len(lines) == 2981, f"expected 2981 lines, got {len(lines)} -- file changed, abort"

starts = [i for i, l in enumerate(lines) if header_cycle(l) is not None]
assert len(starts) == 53, f"expected 53 cycle blocks, got {len(starts)}"
assert starts[0] == 0, "file must begin with a cycle block"

block_cycles = [header_cycle(lines[i]) for i in starts]
expected_cycles = list(range(2458, 2405, -1))
assert block_cycles == expected_cycles, \
    f"blocks are not strictly newest-first 2458..2406: {block_cycles}"

cut = starts[KEEP_BLOCKS]
keep = lines[:cut]
archived = lines[cut:]
assert header_cycle(lines[starts[KEEP_BLOCKS - 1]]) == 2454, "kept-oldest block is not 2454"
assert header_cycle(lines[cut]) == 2453, "archive-newest block is not 2453"

# Drop the separator ('---' + surrounding blanks) between the last kept
# block and the first archived block, same as every prior trim.
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
    "\n## Archived by cycle 2459 (sonnet-5), 2026-10-30 -- STATUS.md had grown to 2981 lines / "
    "242.2KB, past both the 150KB warn and 200KB trim lines and check-doc-size read it as TRIM "
    "DUE (not just SOON). Cycles <=2453 moved here verbatim, in source order; the live file keeps "
    "the newest 5 blocks (the contiguous window 2454..2458). The source file's 53 blocks were "
    "strictly newest-first (2458 down to 2406, no gaps) -- confirming every block the c2411 trim "
    "left live (2406..2410) plus every cycle's own addition since (2411..2458) survived intact. "
    "Rate re-measured: the file grew to 248,027 bytes over the 48 blocks added since the c2411 "
    "trim's post-cut 16,982 bytes (2406..2410 live then) = ~4,813 B/block actual, close to the "
    "checker's registered +4510 B/cycle.\n\n"
)
addition = header + archived_txt
new_archive = old_archive + addition

for ln in archived:
    if ln.strip() and ln not in addition:
        sys.exit(f"FAIL: archived line missing from addition: {ln[:90]!r}")

# The only lines NOT present in keep_txt+archived_txt should be the <=3
# dropped separator lines (blank/'---'), already bounded above.
dropped_lines = lines[len(keep):cut]
if any(l.strip() not in ("", "---") for l in dropped_lines):
    sys.exit(f"FAIL: a dropped separator line has real content: {dropped_lines!r}")
if "".join(keep) + "".join(dropped_lines) + "".join(archived) != "".join(lines[:cut]) + "".join(archived):
    sys.exit("FAIL: kept + dropped + archived does not reconstruct the original file")

if not new_archive.startswith(old_archive):
    sys.exit("FAIL: prior archive content would not be preserved byte-identically")

orig_cycles = {c for l in lines if (c := header_cycle(l)) is not None}
live_cycles = {c for l in keep if (c := header_cycle(l)) is not None}
arch_cycles = {int(m.group(1) or m.group(2))
               for m in re.finditer(HEADER_RE.pattern, new_archive, re.MULTILINE)}
lost = sorted(orig_cycles - (live_cycles | arch_cycles))
if lost:
    sys.exit(f"FAIL: cycle block(s) would be destroyed: {lost}")

if live_cycles != {2454, 2455, 2456, 2457, 2458}:
    sys.exit(f"FAIL: live window is not 2454..2458: {sorted(live_cycles)}")

if any((c := header_cycle(l)) is not None and c <= 2453 for l in keep):
    sys.exit("FAIL: a block older than the cut is still live")

print("All 6 verifications passed. Writing files.")
with open(SRC, "w") as f:
    f.write(keep_txt)
with open(ARCHIVE, "w") as f:
    f.write(new_archive)
print(f"live STATUS.md:   {len(keep)} lines / {len(keep_txt.encode())} bytes "
      f"({len(keep_txt.encode())/1024:.1f}KB)")
print(f"archive addition: {len(archived)} lines")
print(f"live cycles kept: {sorted(live_cycles, reverse=True)}")
