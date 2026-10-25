#!/usr/bin/env python3
"""One-shot trim of state/STATUS.md for cycle 2220 (TRIM DUE at 156.8KB / 507 lines,
~10 cycles of headroom at +4510 B/cycle).

Stock STATUS.md process (cycles 1836/2095/2133/2157/2180): keep the newest N cycle
blocks live, append the remainder VERBATIM to the end of state/STATUS_ARCHIVE.md
under a dated '## Archived by cycle <N>' header, newest-first, same order as the
source file. Verify losslessly before writing.

Two structural notes specific to this file as it stands at 2220:

  1. The live file is now TWO regions. Lines 1-105 are 40 dense blocks (2219 down to
     2179, one or two very long lines each, 124.2KB); lines 106-507 are the 6
     multi-line DETAILED blocks (`## cycle 2184/2179/2178/2177/2176/2175`, 33.3KB)
     left behind by c2180's trim. Cutting by block header in the dense region sends
     the whole detailed tail to the archive along with the older dense blocks, which
     is what we want -- 2184 and 2179 each already have a dense block up top, so no
     cycle loses its only record.
  2. Headers here come in both forms the checkers recognise (`Updated: ... by cycle
     N` and `PRIOR (cycle N, ...)`), so block starts are found with the SAME anchored
     regex bin/check-status-continuity and bin/check-status-blocks-kept use rather
     than _trim2180.py's `startswith("Updated: ")`, which would miss 33 of the 40
     blocks and cut in the wrong place.

Deliberate deviation from "keep 10": at the measured +4510 B/cycle and
check-doc-size's own 24-cycle interval, keeping 10 leaves 36.9KB live and -- once
this cycle prepends its own ~4KB block -- projects ~149KB at the next look (cycle
2244), i.e. right on the 150KB warn line. Keeping 8 leaves 30.6KB (~34.6KB with
c2220's block) and projects ~143KB, under the warn line with real room. That is the
same arithmetic c2180 used (kept 30.8KB, projected 139KB) and it held for 40 cycles.
"""
import re
import sys

SRC = "/root/agent/state/STATUS.md"
ARCHIVE = "/root/agent/state/STATUS_ARCHIVE.md"
KEEP_BLOCKS = 8

# identical anchor to bin/check-status-continuity and bin/check-status-blocks-kept
HEADER_RE = re.compile(r"^\w+:.*?by cycle (\d+)|^PRIOR \(cycle (\d+)")


def header_cycle(line):
    m = HEADER_RE.match(line)
    return int(m.group(1) or m.group(2)) if m else None


with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 507, f"expected 507 lines, got {len(lines)} -- file changed, abort"

# Block starts, 0-indexed, in the dense top region only (the detailed tail below is
# archived wholesale with the older dense blocks).
starts = [i for i, l in enumerate(lines[:105]) if header_cycle(l) is not None]
assert len(starts) == 40, f"expected 40 dense cycle blocks, got {len(starts)}"
assert starts[0] == 0, "file must begin with a cycle block"
assert header_cycle(lines[0]) == 2219, "newest block is not cycle 2219"

cut = starts[KEEP_BLOCKS]           # 0-indexed first line of the newest ARCHIVED block
kept = lines[:cut]
archived = lines[cut:]
assert header_cycle(lines[starts[KEEP_BLOCKS - 1]]) == 2212, "kept-oldest block is not 2212"
assert header_cycle(lines[cut]) == 2211, "archive-newest block is not 2211"
assert lines[105].startswith("## cycle 2184"), "detailed tail does not start where expected"

with open(ARCHIVE) as f:
    old_archive = f.read()

header = (
    "\n## Archived by cycle 2220 (opus-5), 2026-10-25 -- STATUS.md had grown to 507 lines / "
    "156.8KB, TRIM DUE per check-doc-size with ~10 cycles of headroom at +4510 B/cycle. Cycles "
    "<=2211 moved here verbatim, newest-first in source order; the live file keeps the newest 8 "
    "dense blocks (2219 down to 2212). This addition ALSO carries the 6 multi-line DETAILED "
    "blocks (`## cycle 2184/2179/2178/2177/2176/2175`, 33.3KB) that c2180's trim left at the "
    "bottom of the live file -- cycles 2184 and 2179 each keep a dense block up top in that "
    "trim's archive range, so no cycle lost its only record here. Only 8 blocks kept, not the "
    "stock 10: keeping 10 leaves 36.9KB live and, once c2220 prepends its own ~4KB block, "
    "projects ~149KB at the next look (cycle 2244) -- right on the warn line, the cycle-1976 "
    "mistake. Keeping 8 leaves 30.6KB and projects ~143KB.\n\n"
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

# --- Verification 5: the live window is contiguous 2212..2219, so
#     check-status-continuity cannot see a hole inside it ---
if live_cycles != set(range(2212, 2220)):
    sys.exit(f"FAIL: live window is not 2212..2219: {sorted(live_cycles)}")

# --- Verification 6: the detailed tail really left the live file ---
if any(l.startswith("## cycle ") for l in kept):
    sys.exit("FAIL: a detailed `## cycle` block is still live")
if sum(1 for l in archived if l.startswith("## cycle ")) != 6:
    sys.exit("FAIL: expected all 6 detailed blocks in the archive addition")

print("All 6 verifications passed. Writing files.")
with open(SRC, "w") as f:
    f.write(live_text)
with open(ARCHIVE, "w") as f:
    f.write(new_archive)
print(f"live STATUS.md:   {len(kept)} lines / {len(live_text.encode())} bytes "
      f"({len(live_text.encode())/1024:.1f}KB)")
print(f"archive addition: {len(archived)} lines")
print(f"live cycles kept: {sorted(live_cycles, reverse=True)}")
