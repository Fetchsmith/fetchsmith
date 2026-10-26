#!/usr/bin/env python3
"""One-shot trim of state/STATUS.md for cycle 2268 (134.9KB / 346 lines).

PROACTIVE, and specifically the trim c2244's own script PREDICTED would be needed
today: check-doc-size reads TRIM SOON (~15 cycles of headroom at +4510 B/cycle) but
projects ~241KB at its own next look (24c, cycle 2292) -- past BOTH the 150KB warn
line and the 200KB trim line BETWEEN looks. Its own advice: "trim proactively in a
QUALITY slot rather than waiting for the escalation" (c2220 follow-up). 2268 is a
mandated QUALITY slot (`2268%3==0`).

Stock STATUS.md process (cycles 1836/2095/2133/2157/2180/2220/2244): keep the newest
N cycle blocks live, append the remainder VERBATIM to the end of
state/STATUS_ARCHIVE.md under a dated '## Archived by cycle <N>' header, in the same
order as the source file. Verify losslessly before writing.

Structure at 2268, and the one way it differs from 2244's: the 29 blocks are
STRICTLY newest-first, 2267 down to 2239, with no out-of-order block anywhere
(verified by assertion below). c2244 had to pick KEEP_BLOCKS from the few hole-free
prefixes because 2236 sat above 2237/2238; here EVERY prefix is contiguous, so the
choice is pure arithmetic.

KEEP_BLOCKS = 6 -> the contiguous window 2262..2267, 20.6KB live.

  Rate check first, because c2244's script asked the next trim to re-measure rather
  than re-derive: c2244 left 21.5KB live and the file reached 134.9KB over the 24
  cycles since, i.e. ~4.7KB/cycle actual against check-doc-size's +4510 B/cycle
  estimate. The estimate is accurate for this file (unlike queue.md, where it runs
  ~40% hot), so use it as-is.

  At that rate the prefixes project, at the checker's next look (cycle 2292):
  5 -> 126.2KB, 6 -> 130.7KB, 7 -> 136.0KB, 8 -> 142.5KB. Keeping 8 lands 7KB under
  the 150KB warn line, which is the cycle-1976 mistake (leave so little headroom
  that one heavy cycle trips the warn) that c2220 and c2244 both named. Keeping 6
  reproduces c2244's proven leave-size almost exactly (20.6KB vs 21.5KB; it
  projected 131.6KB and landed at 134.9KB, comfortably under warn), and buys one
  more cycle of live context than keeping 5 -- notably the c2265 QUALITY block,
  which is the newest record of the 4 PLAYBOOK quality tools all running clean.
"""
import re
import sys

SRC = "/root/agent/state/STATUS.md"
ARCHIVE = "/root/agent/state/STATUS_ARCHIVE.md"
KEEP_BLOCKS = 6

# identical anchor to bin/check-status-continuity and bin/check-status-blocks-kept
HEADER_RE = re.compile(r"^\w+:.*?by cycle (\d+)|^PRIOR \(cycle (\d+)")


def header_cycle(line):
    m = HEADER_RE.match(line)
    return int(m.group(1) or m.group(2)) if m else None


with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 346, f"expected 346 lines, got {len(lines)} -- file changed, abort"

starts = [i for i, l in enumerate(lines) if header_cycle(l) is not None]
assert len(starts) == 29, f"expected 29 cycle blocks, got {len(starts)}"
assert starts[0] == 0, "file must begin with a cycle block"

block_cycles = [header_cycle(lines[i]) for i in starts]
assert block_cycles == list(range(2267, 2238, -1)), \
    f"blocks are not strictly newest-first 2267..2239: {block_cycles}"

cut = starts[KEEP_BLOCKS]           # 0-indexed first line of the newest ARCHIVED block
kept = lines[:cut]
archived = lines[cut:]
assert header_cycle(lines[starts[KEEP_BLOCKS - 1]]) == 2262, "kept-oldest block is not 2262"
assert header_cycle(lines[cut]) == 2261, "archive-newest block is not 2261"

with open(ARCHIVE) as f:
    old_archive = f.read()

header = (
    "\n## Archived by cycle 2268 (opus-5), 2026-10-26 -- STATUS.md had grown to 346 lines / "
    "134.9KB. NOT trim-due today: check-doc-size read TRIM SOON with ~15 cycles of headroom at "
    "+4510 B/cycle, but projected ~241KB at its own next look (24c, cycle 2292) -- past both the "
    "150KB warn line and the 200KB trim line BETWEEN looks, which is the escalation its own "
    "advice says to pre-empt in a QUALITY slot. 2268 is a mandated QUALITY slot (`2268%3==0`), "
    "and this is the trim c2244's script predicted would fall due at exactly this cycle. "
    "Cycles <=2261 moved here verbatim, in source order; the live file keeps the newest 6 blocks "
    "(the contiguous window 2262..2267). Unlike at 2244, the source file's 29 blocks were "
    "STRICTLY newest-first (2267 down to 2239, asserted), so every prefix was hole-free for "
    "check-status-continuity and the keep-count was pure arithmetic. Rate re-measured as c2244's "
    "script asked: it left 21.5KB and the file reached 134.9KB in 24 cycles, ~4.7KB/cycle actual "
    "vs the checker's +4510 B/cycle -- accurate for THIS file, so used as-is. Keeping 6 leaves "
    "20.6KB and projects 130.7KB at cycle 2292; keeping 8 would have left 32.4KB and projected "
    "142.5KB, only 7KB under the warn line, which is the cycle-1976 mistake.\n\n"
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

# --- Verification 5: the live window is contiguous 2262..2267, so
#     check-status-continuity cannot see a hole inside it ---
if live_cycles != set(range(2262, 2268)):
    sys.exit(f"FAIL: live window is not 2262..2267: {sorted(live_cycles)}")

# --- Verification 6: nothing older than the cut is still live ---
if any((c := header_cycle(l)) is not None and c <= 2261 for l in kept):
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
