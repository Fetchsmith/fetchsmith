#!/usr/bin/env python3
"""One-shot trim of state/STATUS.md for cycle 2341 (151.6KB / 446 lines).

PROACTIVE, same escalation path c2316 named: check-doc-size reads TRIM DUE today
(over the 150KB warn line, ~11 cycles of headroom to the 200KB trim line at
+4510 B/cycle) and projects ~257KB at its own next look (24c) -- past the Read
cap. 2341 is the mandated QUALITY/GROWTH slot (3rd cycle since c2338's last
QUALITY slot: 2339/2340 BUILD, 2341 QUALITY), and c2340's own queue.md note named
this trim as the first thing the next QUALITY slot should do.

Stock STATUS.md process (cycles 1836/2095/2133/2157/2180/2220/2244/2268/2292/2316):
keep the newest N cycle blocks live, append the remainder VERBATIM to the end of
state/STATUS_ARCHIVE.md under a dated '## Archived by cycle <N>' header, in the
same order as the source file. Verify losslessly before writing.

Structure at 2341: 28 blocks, STRICTLY newest-first, 2340 down to 2312 (2335
never ran, so it is simply absent -- not a hole, the header sequence just skips
it, as recorded at c2336/c2337's STATUS blocks). No out-of-order block.

KEEP_BLOCKS = 4 -> the contiguous window 2337..2340, 19.8KB live.

  RATE re-measured fresh per-block (not re-derived from the checker), summing
  all 24 blocks added since c2316's trim (2316..2340, excluding the never-run
  2335): 132,681 bytes / 24 blocks = 5,528 B/block actual, against
  check-doc-size's +4510 B/cycle -- the checker runs ~23% COOL on this file this
  time (c2316 measured 11% cool the cycle before; the gap has widened, so this
  trim uses the freshly measured rate, not either the checker's or c2316's).

  Keeping 4 (2337..2340) sums to 20,325 bytes = 19.8KB. At the measured
  5,528 B/block, 24 more cycles projects to 20,325 + 5528*24 = 153,006 bytes =
  149.4KB -- just under the 150KB warn line, so check-doc-size should read OK
  (not even WARN) at its next look, with real margin against the 1976-style thin
  guard band. Keeping 5 would add 2336's 6,376 B, landing at 26.7KB live and
  ~159.3KB projected -- already past the warn line at next look, so 4 is the
  right cut, matching c2316's own keep-count exactly.

  NOTE on what the kept window holds, recorded deliberately per c2316's own
  precedent: 2337..2340 contains exactly ONE QUALITY/GROWTH block (2338; 2337,
  2339, 2340 are BUILD-slot blocks). This cycle (2341) is itself a QUALITY slot
  and prepends its own block immediately after this script runs, so the live
  file ends the cycle holding TWO current QUALITY blocks, not zero -- stronger
  than the bare minimum c2316 flagged as acceptable-only-because.
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

assert len(lines) == 446, f"expected 446 lines, got {len(lines)} -- file changed, abort"

starts = [i for i, l in enumerate(lines) if header_cycle(l) is not None]
assert len(starts) == 28, f"expected 28 cycle blocks, got {len(starts)}"
assert starts[0] == 0, "file must begin with a cycle block"

block_cycles = [header_cycle(lines[i]) for i in starts]
expected_cycles = [c for c in range(2340, 2311, -1) if c != 2335]
assert block_cycles == expected_cycles, \
    f"blocks are not strictly newest-first 2340..2312 (skip 2335): {block_cycles}"

cut = starts[KEEP_BLOCKS]           # 0-indexed first line of the newest ARCHIVED block
kept = lines[:cut]
archived = lines[cut:]
assert header_cycle(lines[starts[KEEP_BLOCKS - 1]]) == 2337, "kept-oldest block is not 2337"
assert header_cycle(lines[cut]) == 2336, "archive-newest block is not 2336"

with open(ARCHIVE) as f:
    old_archive = f.read()

header = (
    "\n## Archived by cycle 2341 (sonnet-5), 2026-10-27 -- STATUS.md had grown to 446 lines / "
    "151.6KB, past the 150KB warn line (check-doc-size read TRIM DUE). Cycles <=2336 moved here "
    "verbatim, in source order; the live file keeps the newest 4 blocks (the contiguous window "
    "2337..2340). 2341 is a mandated QUALITY/GROWTH slot (3rd cycle since c2338's last QUALITY "
    "slot: 2339/2340 were BUILD), and this is exactly the trim c2340's queue.md note asked the "
    "next QUALITY slot to do first. The source file's 28 blocks were STRICTLY newest-first (2340 "
    "down to 2312, with 2335 simply absent since that cycle never ran -- not a hole), so every "
    "prefix was hole-free for check-status-continuity and the keep-count was pure arithmetic. "
    "RATE re-measured fresh per-block rather than inherited: the 24 blocks added since c2316's "
    "trim (2316..2340, excluding 2335) sum to 132,681 bytes = 5,528 B/block actual, against the "
    "checker's +4510 B/cycle -- ~23% COOL on this file this time (c2316 measured 11% cool the "
    "cycle before, so the gap has widened and the freshly measured rate is used here, not either "
    "prior figure). Keeping 4 leaves 19.8KB and projects ~149.4KB at the next look (24c), just "
    "under the 150KB warn line with real margin; keeping 5 would add 2336's 6,376 B and already "
    "project past the warn line at next look, so 4 matches c2316's own keep-count exactly. The "
    "kept window 2337..2340 holds one QUALITY block (2338) plus three BUILD blocks, and cycle "
    "2341 itself prepends a second current QUALITY block right after this trim runs.\n\n"
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

# --- Verification 5: the live window is contiguous 2337..2340 ---
if live_cycles != {2337, 2338, 2339, 2340}:
    sys.exit(f"FAIL: live window is not 2337..2340: {sorted(live_cycles)}")

# --- Verification 6: nothing older than the cut is still live ---
if any((c := header_cycle(l)) is not None and c <= 2336 for l in kept):
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
