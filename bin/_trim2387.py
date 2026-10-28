#!/usr/bin/env python3
"""One-shot trim of state/STATUS.md for cycle 2387 (121.2KB / 299 lines).

check-doc-size read TRIM SOON this cycle (~18c headroom today at the
registered +4510 B/cycle, but projecting ~227KB at its own next look, 24c --
past both the 150KB warn and 200KB trim lines between looks). This is the
proactive QUALITY-slot trim it asked for (2387%3==2), same stock method as
1836/2095/2133/2157/2180/2220/2244/2268/2292/2316/2341/2366: keep the newest
N cycle blocks live, append the remainder VERBATIM to state/STATUS_ARCHIVE.md
under a dated header, source order preserved.

Structure at 2387: 27 blocks, strictly newest-first, 2386 down to 2360, no
gaps (2360..2386 is exactly 27 consecutive cycle numbers).

KEEP_BLOCKS = 5 -> the contiguous window 2382..2386, 27.0KB live.

  Rate re-measured fresh: the file held 23,934 bytes right after c2366's
  trim (6 blocks, 2360..2365 live then; see bin/_trim2366.py) and has grown
  to 124,155 bytes over the 21 blocks added since (2366..2386), i.e.
  (124155-23934)/21 = 4,772 B/block actual, close to the checker's own
  +4510 B/cycle. Keeping 5 (2382..2386) leaves 27,670 bytes live; at the
  checker's own +4510 B/cycle that projects to 27,670 + 4510*24 = 135.9KB
  at the next look (24c) -- comfortably under the 150KB warn line. Keeping
  6 would leave 31,182 bytes live and still be safe, but these 5 most-recent
  blocks run noticeably longer than 2366's kept window, so 5 buys the same
  safety margin with one fewer long block carried forward.
"""
import re
import sys

SRC = "/root/agent/state/STATUS.md"
ARCHIVE = "/root/agent/state/STATUS_ARCHIVE.md"
KEEP_BLOCKS = 5

HEADER_RE = re.compile(r"^\w+:.*?by cycle (\d+)|^PRIOR \(cycle (\d+)")


def header_cycle(line):
    m = HEADER_RE.match(line)
    return int(m.group(1) or m.group(2)) if m else None


with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 299, f"expected 299 lines, got {len(lines)} -- file changed, abort"

starts = [i for i, l in enumerate(lines) if header_cycle(l) is not None]
assert len(starts) == 27, f"expected 27 cycle blocks, got {len(starts)}"
assert starts[0] == 0, "file must begin with a cycle block"

block_cycles = [header_cycle(lines[i]) for i in starts]
expected_cycles = list(range(2386, 2359, -1))
assert block_cycles == expected_cycles, \
    f"blocks are not strictly newest-first 2386..2360: {block_cycles}"

cut = starts[KEEP_BLOCKS]
kept = lines[:cut]
archived = lines[cut:]
assert header_cycle(lines[starts[KEEP_BLOCKS - 1]]) == 2382, "kept-oldest block is not 2382"
assert header_cycle(lines[cut]) == 2381, "archive-newest block is not 2381"

with open(ARCHIVE) as f:
    old_archive = f.read()

header = (
    "\n## Archived by cycle 2387 (sonnet-5), 2026-10-28 -- STATUS.md had grown to 299 lines / "
    "121.2KB, projected past the 150KB warn line before check-doc-size's next scheduled look "
    "(24c). check-doc-size itself recommended trimming proactively in a QUALITY slot rather than "
    "waiting for the escalation; 2387%3==2 is that slot. Cycles <=2381 moved here verbatim, in "
    "source order; the live file keeps the newest 5 blocks (the contiguous window 2382..2386). "
    "The source file's 27 blocks were strictly newest-first (2386 down to 2360, no gaps), so "
    "every prefix was hole-free for check-status-continuity. Rate re-measured: the file grew "
    "from 23,934 bytes (right after c2366's trim) to 124,155 bytes over the 21 blocks added "
    "since (2366..2386) = 4,772 B/block actual vs the checker's +4510 B/cycle (close to "
    "registered rate). Keeping 5 leaves 27.0KB live and projects ~135.9KB at the next look (24c) "
    "at the checker's own rate -- comfortably under the 150KB warn line.\n\n"
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

if live_cycles != {2382, 2383, 2384, 2385, 2386}:
    sys.exit(f"FAIL: live window is not 2382..2386: {sorted(live_cycles)}")

if any((c := header_cycle(l)) is not None and c <= 2381 for l in kept):
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
