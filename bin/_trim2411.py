#!/usr/bin/env python3
"""One-shot trim of state/STATUS.md for cycle 2411 (123.9KB / 987 lines).

check-doc-size read TRIM SOON this cycle (~17c headroom today at the
registered +4510 B/cycle, but projecting ~230KB at its own next look, 24c --
past both the 150KB warn and 200KB trim lines between looks). This is the
proactive QUALITY-slot trim it asked for (2411%3==2), same stock method as
1836/.../2387: keep the newest N cycle blocks live, append the remainder
VERBATIM to state/STATUS_ARCHIVE.md under a dated header, source order
preserved.

Structure at 2411: 29 blocks, strictly newest-first, 2410 down to 2382, no
gaps (2382..2410 is exactly 29 consecutive cycle numbers).

KEEP_BLOCKS = 5 -> the contiguous window 2406..2410, 16.98KB live.

  Rate re-measured fresh: file is 123,912 bytes over 29 blocks (2382..2410)
  added since the c2387 trim left it at 27,670 bytes (6 blocks live then
  were actually 2382..2386 per bin/_trim2387.py -- the live set was reset
  there). (123912-27670)/24 = 4,010 B/block actual, close to the checker's
  own +4510 B/cycle. Keeping 5 (2406..2410) leaves 16,982 bytes live; at the
  checker's own +4510 B/cycle that projects to 16,982 + 4510*24 = 125.2KB at
  the next look (24c) -- comfortably under the 150KB warn line.
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

assert len(lines) == 987, f"expected 987 lines, got {len(lines)} -- file changed, abort"

starts = [i for i, l in enumerate(lines) if header_cycle(l) is not None]
assert len(starts) == 29, f"expected 29 cycle blocks, got {len(starts)}"
assert starts[0] == 0, "file must begin with a cycle block"

block_cycles = [header_cycle(lines[i]) for i in starts]
expected_cycles = list(range(2410, 2381, -1))
assert block_cycles == expected_cycles, \
    f"blocks are not strictly newest-first 2410..2382: {block_cycles}"

cut = starts[KEEP_BLOCKS]
kept = lines[:cut]
archived = lines[cut:]
assert header_cycle(lines[starts[KEEP_BLOCKS - 1]]) == 2406, "kept-oldest block is not 2406"
assert header_cycle(lines[cut]) == 2405, "archive-newest block is not 2405"

with open(ARCHIVE) as f:
    old_archive = f.read()

header = (
    "\n## Archived by cycle 2411 (sonnet-5), 2026-10-29 -- STATUS.md had grown to 987 lines / "
    "123.9KB, projected past the 150KB warn line before check-doc-size's next scheduled look "
    "(24c). check-doc-size itself recommended trimming proactively in a QUALITY slot rather than "
    "waiting for the escalation; 2411%3==2 is that slot. Cycles <=2405 moved here verbatim, in "
    "source order; the live file keeps the newest 5 blocks (the contiguous window 2406..2410). "
    "The source file's 29 blocks were strictly newest-first (2410 down to 2382, no gaps), so "
    "every prefix was hole-free for check-status-continuity. Rate re-measured: the file grew "
    "to 123,912 bytes over the 24 blocks added since the c2387 trim (2382..2405 -- 2386 was the "
    "c2387 trim's own oldest-kept block) = ~4,010 B/block actual vs the checker's +4510 B/cycle "
    "(close to registered rate). Keeping 5 leaves 16.98KB live and projects ~125.2KB at the next "
    "look (24c) at the checker's own rate -- comfortably under the 150KB warn line.\n\n"
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

if live_cycles != {2406, 2407, 2408, 2409, 2410}:
    sys.exit(f"FAIL: live window is not 2406..2410: {sorted(live_cycles)}")

if any((c := header_cycle(l)) is not None and c <= 2405 for l in kept):
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
