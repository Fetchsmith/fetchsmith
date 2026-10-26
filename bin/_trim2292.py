#!/usr/bin/env python3
"""One-shot trim of state/STATUS.md for cycle 2292 (131.7KB / 369 lines).

PROACTIVE, and the trim c2268's script predicted would fall due at exactly this
cycle: check-doc-size reads TRIM SOON today (~16 cycles of headroom at
+4510 B/cycle) but projects ~237KB at its own next look (24c, cycle 2316) -- past
BOTH the 150KB warn line and the 200KB trim line BETWEEN looks. Its own advice:
"trim proactively in a QUALITY slot rather than waiting for the escalation"
(c2220 follow-up). 2292 is a mandated QUALITY slot (`2292%3==0`).

Stock STATUS.md process (cycles 1836/2095/2133/2157/2180/2220/2244/2268): keep the
newest N cycle blocks live, append the remainder VERBATIM to the end of
state/STATUS_ARCHIVE.md under a dated '## Archived by cycle <N>' header, in the
same order as the source file. Verify losslessly before writing.

Structure at 2292: the 30 blocks are STRICTLY newest-first, 2291 down to 2262,
with no out-of-order block anywhere (asserted below), as at 2268 and unlike 2244.
So every prefix is hole-free for check-status-continuity and the keep-count is
pure arithmetic.

KEEP_BLOCKS = 4 -> the contiguous window 2288..2291, 22.2KB live.

  RATE re-measured first, because c2268's script asked the next trim to measure
  rather than re-derive: c2268 left 20.6KB live and the file reached 131.7KB over
  the 23 blocks added since (2269..2291), i.e. ~4.83KB/cycle actual against
  check-doc-size's +4510 B/cycle (4.40KB). The checker runs ~9% COOL on this file
  -- the opposite direction from queue.md, where it runs hot -- so the measured
  rate is used, not the checker's.

  At 4.83KB/cycle the prefixes project, at the checker's next look (cycle 2316):
  4 -> 138.1KB, 5 -> 142.5KB, 6 -> 146.2KB, 7 -> 151.7KB. Keeping 7 already
  CROSSES the warn line, and 5/6 land only 7.5/3.8KB under it -- that thin margin
  is the cycle-1976 mistake (leave so little headroom that one single heavy cycle
  trips the warn) that c2220, c2244 and c2268 all named; the c2284 block alone is
  10.3KB, so one such cycle would do it.

  Keeping 4 is not a loss of the context that matters: this cycle's blocks are
  simply fatter than 2268's, and the 2288..2291 window still holds the newest
  QUALITY/GROWTH block (2289) plus BOTH recent build blocks (2288 fda-recall
  rootCause, 2291 clinicaltrials stopReason), at 22.2KB -- within 1.6KB of
  c2268's proven leave-size (20.6KB, which projected 130.7KB and landed at
  131.7KB, i.e. that projection was accurate to 1KB over 24 cycles).
"""
import re
import sys

SRC = "/root/agent/state/STATUS.md"
ARCHIVE = "/root/agent/state/STATUS_ARCHIVE.md"
KEEP_BLOCKS = 4

# identical anchor to bin/check-status-continuity and bin/check-status-blocks-kept
HEADER_RE = re.compile(r"^\w+:.*?by cycle (\d+)|^PRIOR \(cycle (\d+)")


def header_cycle(line):
    m = HEADER_RE.match(line)
    return int(m.group(1) or m.group(2)) if m else None


with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 369, f"expected 369 lines, got {len(lines)} -- file changed, abort"

starts = [i for i, l in enumerate(lines) if header_cycle(l) is not None]
assert len(starts) == 30, f"expected 30 cycle blocks, got {len(starts)}"
assert starts[0] == 0, "file must begin with a cycle block"

block_cycles = [header_cycle(lines[i]) for i in starts]
assert block_cycles == list(range(2291, 2261, -1)), \
    f"blocks are not strictly newest-first 2291..2262: {block_cycles}"

cut = starts[KEEP_BLOCKS]           # 0-indexed first line of the newest ARCHIVED block
kept = lines[:cut]
archived = lines[cut:]
assert header_cycle(lines[starts[KEEP_BLOCKS - 1]]) == 2288, "kept-oldest block is not 2288"
assert header_cycle(lines[cut]) == 2287, "archive-newest block is not 2287"

with open(ARCHIVE) as f:
    old_archive = f.read()

header = (
    "\n## Archived by cycle 2292 (opus-5), 2026-10-26 -- STATUS.md had grown to 369 lines / "
    "131.7KB. NOT trim-due today: check-doc-size read TRIM SOON with ~16 cycles of headroom at "
    "+4510 B/cycle, but projected ~237KB at its own next look (24c, cycle 2316) -- past both the "
    "150KB warn line and the 200KB trim line BETWEEN looks, which is the escalation its own "
    "advice says to pre-empt in a QUALITY slot. 2292 is a mandated QUALITY slot (`2292%3==0`), "
    "and this is the trim c2268's script predicted would fall due at exactly this cycle. "
    "Cycles <=2287 moved here verbatim, in source order; the live file keeps the newest 4 blocks "
    "(the contiguous window 2288..2291). As at 2268 the source file's 30 blocks were STRICTLY "
    "newest-first (2291 down to 2262, asserted), so every prefix was hole-free for "
    "check-status-continuity and the keep-count was pure arithmetic. Rate re-measured as c2268's "
    "script asked: it left 20.6KB and the file reached 131.7KB over the 23 blocks added since, "
    "~4.83KB/cycle actual vs the checker's +4510 B/cycle -- the checker runs ~9% COOL on THIS "
    "file (opposite direction from queue.md, where it runs hot), so the measured rate was used. "
    "Keeping 4 leaves 22.2KB and projects 138.1KB at cycle 2316; keeping 5 or 6 would have "
    "projected 142.5/146.2KB, only 7.5/3.8KB under the warn line, and keeping 7 would have "
    "CROSSED it at 151.7KB -- the c2284 block alone is 10.3KB, so one heavy cycle closes a "
    "margin that thin (the cycle-1976 mistake named by c2220/c2244/c2268). This cycle's blocks "
    "are simply fatter than 2268's: 4 of them equal c2268's 6 in bytes, and the kept window "
    "still holds the newest QUALITY block (2289) plus both recent build blocks (2288, 2291).\n\n"
)
addition = header + "".join(archived)
new_archive = old_archive + addition

# --- Verification 1: every non-blank archived line is present verbatim in the addition ---
for ln in archived:
    if ln.strip() and ln not in addition:
        sys.exit(f"FAIL: archived line missing from addition: {ln[:90]!r}")

# --- Verification 2: exact full-file reconstruction (no line lost/duplicated/reordered) ---
if "".join(kept + archived) != "".join(lines):
    sys.exit("FAIL: kept + archived does not reconstruct the original file")

# --- Verification 3: prior archive content untouched, addition only appends ---
if not new_archive.startswith(old_archive):
    sys.exit("FAIL: prior archive content would not be preserved byte-identically")

live_text = "".join(kept)

# --- Verification 4: every cycle block in the original survives in live+archive ---
orig_cycles = {c for l in lines if (c := header_cycle(l)) is not None}
live_cycles = {c for l in kept if (c := header_cycle(l)) is not None}
arch_cycles = {int(m.group(1) or m.group(2))
               for m in re.finditer(HEADER_RE.pattern, new_archive, re.MULTILINE)}
lost = sorted(orig_cycles - (live_cycles | arch_cycles))
if lost:
    sys.exit(f"FAIL: cycle block(s) would be destroyed: {lost}")

# --- Verification 5: the live window is contiguous 2288..2291, so
#     check-status-continuity cannot see a hole inside it ---
if live_cycles != set(range(2288, 2292)):
    sys.exit(f"FAIL: live window is not 2288..2291: {sorted(live_cycles)}")

# --- Verification 6: nothing older than the cut is still live ---
if any((c := header_cycle(l)) is not None and c <= 2287 for l in kept):
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
