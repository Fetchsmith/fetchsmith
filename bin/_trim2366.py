#!/usr/bin/env python3
"""One-shot trim of state/STATUS.md for cycle 2366 (144.2KB / 343 lines).

check-doc-size read TRIM SOON this cycle (~13c headroom at the registered
+4510 B/cycle, but projecting ~250KB at its own next look, 24c -- past the
trim line between looks). c2364 explicitly queued this trim for the c2366
QUALITY slot (2366%3==2), and this is that trim.

Same stock method as 1836/2095/2133/2157/2180/2220/2244/2268/2292/2316/2341:
keep the newest N cycle blocks live, append the remainder VERBATIM to
state/STATUS_ARCHIVE.md under a dated header, source order preserved.

Structure at 2366: 29 blocks, strictly newest-first, 2365 down to 2337, no
gaps (2337..2365 is exactly 29 consecutive cycle numbers).

KEEP_BLOCKS = 6 -> the contiguous window 2360..2365, 23.9KB live.

  Rate re-measured fresh: the file held ~24.4KB right after c2341's trim
  (2337..2341 live then; see bin/_trim2341.py) and has grown to 147,614
  bytes over the 24 blocks added since (2342..2365), i.e. (147614-24372)/24
  = 5,135 B/block actual, vs the checker's +4510 B/cycle (~14% hot).
  Keeping 6 (2360..2365) leaves 23,934 bytes live; at the checker's own
  +4510 B/cycle that projects to 23,934 + 4510*24 = 131.2KB at the next
  look (24c) -- comfortably under the 150KB warn line. Keeping 5 would
  drop to 18.9KB but only buys ~5KB of extra headroom for one fewer block
  of context; 6 keeps slightly more recent history live for roughly the
  same safety margin.
"""
import re
import sys

SRC = "/root/agent/state/STATUS.md"
ARCHIVE = "/root/agent/state/STATUS_ARCHIVE.md"
KEEP_BLOCKS = 6

HEADER_RE = re.compile(r"^\w+:.*?by cycle (\d+)|^PRIOR \(cycle (\d+)")


def header_cycle(line):
    m = HEADER_RE.match(line)
    return int(m.group(1) or m.group(2)) if m else None


with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 343, f"expected 343 lines, got {len(lines)} -- file changed, abort"

starts = [i for i, l in enumerate(lines) if header_cycle(l) is not None]
assert len(starts) == 29, f"expected 29 cycle blocks, got {len(starts)}"
assert starts[0] == 0, "file must begin with a cycle block"

block_cycles = [header_cycle(lines[i]) for i in starts]
expected_cycles = list(range(2365, 2336, -1))
assert block_cycles == expected_cycles, \
    f"blocks are not strictly newest-first 2365..2337: {block_cycles}"

cut = starts[KEEP_BLOCKS]
kept = lines[:cut]
archived = lines[cut:]
assert header_cycle(lines[starts[KEEP_BLOCKS - 1]]) == 2360, "kept-oldest block is not 2360"
assert header_cycle(lines[cut]) == 2359, "archive-newest block is not 2359"

with open(ARCHIVE) as f:
    old_archive = f.read()

header = (
    "\n## Archived by cycle 2366 (sonnet-5), 2026-10-28 -- STATUS.md had grown to 343 lines / "
    "144.2KB, projected past the 150KB warn line before check-doc-size's next scheduled look "
    "(24c). c2364 queued this trim for the c2366 QUALITY slot. Cycles <=2359 moved here "
    "verbatim, in source order; the live file keeps the newest 6 blocks (the contiguous window "
    "2360..2365). The source file's 29 blocks were strictly newest-first (2365 down to 2337, no "
    "gaps), so every prefix was hole-free for check-status-continuity. Rate re-measured: the file "
    "grew from ~24.4KB (right after c2341's trim) to 147,614 bytes over the 24 blocks added "
    "since (2342..2365) = 5,135 B/block actual vs the checker's +4510 B/cycle (~14% hot). Keeping "
    "6 leaves 23.9KB live and projects ~131.2KB at the next look (24c) at the checker's own rate "
    "-- comfortably under the 150KB warn line.\n\n"
)
addition = header + "".join(archived)
new_archive = old_archive + addition

for ln in archived:
    if ln.strip() and ln not in addition:
        sys.exit(f"FAIL: archived line missing from addition: {ln[:90]!r}")

if "".join(kept + archived) != "".join(lines):
    sys.exit("FAIL: kept + archived does not reconstruct the original file")

if not new_archive.startswith(old_archive):
    sys.exit("FAIL: prior archive content would not be preserved byte-identically")

live_text = "".join(kept)

orig_cycles = {c for l in lines if (c := header_cycle(l)) is not None}
live_cycles = {c for l in kept if (c := header_cycle(l)) is not None}
arch_cycles = {int(m.group(1) or m.group(2))
               for m in re.finditer(HEADER_RE.pattern, new_archive, re.MULTILINE)}
lost = sorted(orig_cycles - (live_cycles | arch_cycles))
if lost:
    sys.exit(f"FAIL: cycle block(s) would be destroyed: {lost}")

if live_cycles != {2360, 2361, 2362, 2363, 2364, 2365}:
    sys.exit(f"FAIL: live window is not 2360..2365: {sorted(live_cycles)}")

if any((c := header_cycle(l)) is not None and c <= 2359 for l in kept):
    sys.exit("FAIL: a block older than the cut is still live")

print("All 6 verifications passed. Writing files.")
with open(SRC, "w") as f:
    f.write(live_text)
with open(ARCHIVE, "w") as f:
    f.write(new_archive)
print(f"live STATUS.md:   {len(kept)} lines / {len(live_text.encode())} bytes "
      f"({len(live_text.encode())/1024:.1f}KB)")
print(f"archive addition: {len(archived)} lines")
print(f"live cycles kept: {sorted(live_cycles, reverse=True)}")
