#!/usr/bin/env python3
"""One-shot trim of state/STATUS.md for cycle 2244 (134.3KB / 232 lines).

PROACTIVE, as check-doc-size itself asks for: the check reports TRIM SOON, not TRIM
DUE -- headroom is positive today (~15 cycles at +4510 B/cycle) but the file is
projected at ~240KB by the check's own next look (24c, cycle 2268), i.e. past BOTH
the 150KB warn line and the 200KB trim line BETWEEN looks. Its own advice: "trim
proactively in a QUALITY slot rather than waiting for the escalation". 2244 is a
mandated QUALITY slot (2244%3==0).

Stock STATUS.md process (cycles 1836/2095/2133/2157/2180/2220): keep the newest N
cycle blocks live, append the remainder VERBATIM to the end of
state/STATUS_ARCHIVE.md under a dated '## Archived by cycle <N>' header, in the same
order as the source file. Verify losslessly before writing.

Structure of the file as it stands at 2244 (the mirror image of 2220's): lines 1-196
are the 16 multi-line blocks 2243..2228 left by c2220's trim plus the cycles since;
lines 197-232 are the 16 dense one-or-two-line blocks 2227..2212 that were the top
region at 2220. Cutting by block header in the multi-line region sends the dense tail
to the archive with it, which is what we want -- every dense-tail cycle (2227..2212)
is strictly older than the cut, so no cycle loses its only record.

KEEP_BLOCKS = 5, not the stock 8-10, for two reasons:

  1. Contiguity. The live window must have no holes or bin/check-status-continuity
     reads one as a destroyed block. The file's blocks are NOT strictly newest-first
     (2236 sits above 2237 and 2238, exactly as c2242/c2243 recorded), so only some
     prefixes are hole-free: 5 -> {2239..2243} and 8 -> {2236..2243} are; 6 and 7
     are not (6 adds 2236 while 2237/2238 are still below the cut).
  2. Arithmetic, which is what rules out 8. At +4510 B/cycle over check-doc-size's
     own 24-cycle interval, keeping 8 leaves 36.7KB and -- once this cycle prepends
     its own ~4.5KB block -- projects 146.8KB at cycle 2268, i.e. ON the 150KB warn
     line. That is the cycle-1976 mistake c2220's script named and then came within
     3KB of repeating (it projected 143KB and landed at 134.3KB). Keeping 5 leaves
     21.5KB and projects 131.6KB, which has real room for a heavy cycle.
"""
import re
import sys

SRC = "/root/agent/state/STATUS.md"
ARCHIVE = "/root/agent/state/STATUS_ARCHIVE.md"
KEEP_BLOCKS = 5

# identical anchor to bin/check-status-continuity and bin/check-status-blocks-kept
HEADER_RE = re.compile(r"^\w+:.*?by cycle (\d+)|^PRIOR \(cycle (\d+)")


def header_cycle(line):
    m = HEADER_RE.match(line)
    return int(m.group(1) or m.group(2)) if m else None


with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 232, f"expected 232 lines, got {len(lines)} -- file changed, abort"

# Block starts, 0-indexed, in the multi-line top region only (the dense tail below is
# archived wholesale with the older multi-line blocks).
starts = [i for i, l in enumerate(lines[:196]) if header_cycle(l) is not None]
assert len(starts) == 16, f"expected 16 multi-line cycle blocks, got {len(starts)}"
assert starts[0] == 0, "file must begin with a cycle block"
assert header_cycle(lines[0]) == 2243, "newest block is not cycle 2243"

cut = starts[KEEP_BLOCKS]           # 0-indexed first line of the newest ARCHIVED block
kept = lines[:cut]
archived = lines[cut:]
assert header_cycle(lines[starts[KEEP_BLOCKS - 1]]) == 2239, "kept-oldest block is not 2239"
assert header_cycle(lines[cut]) == 2236, "archive-newest block is not 2236"
assert header_cycle(lines[196]) == 2227, "dense tail does not start at 2227 where expected"

with open(ARCHIVE) as f:
    old_archive = f.read()

header = (
    "\n## Archived by cycle 2244 (opus-5), 2026-10-25 -- STATUS.md had grown to 232 lines / "
    "134.3KB. NOT trim-due today: check-doc-size read TRIM SOON with ~15 cycles of headroom at "
    "+4510 B/cycle, but projected ~240KB at its own next look (24c, cycle 2268) -- past both the "
    "150KB warn line and the 200KB trim line BETWEEN looks, which is the escalation its own "
    "advice says to pre-empt in a QUALITY slot. 2244 is a mandated QUALITY slot. Cycles <=2236 "
    "moved here verbatim, in source order; the live file keeps the newest 5 blocks (the "
    "contiguous set 2239..2243). This addition ALSO carries the 16 DENSE one-or-two-line blocks "
    "(2227 down to 2212) that c2220's trim left at the bottom of the live file -- all of them "
    "are strictly older than the cut, so no cycle lost its only record here. Only 5 blocks kept, "
    "not c2220's 8: the file's blocks are not strictly newest-first (2236 sits above 2237/2238), "
    "so only the 5- and 8-prefixes are hole-free for check-status-continuity, and keeping 8 "
    "leaves 36.7KB which projects 146.8KB at cycle 2268 -- ON the warn line, the cycle-1976 "
    "mistake. Keeping 5 leaves 21.5KB and projects 131.6KB.\n\n"
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

# --- Verification 5: the live window is contiguous 2239..2243, so
#     check-status-continuity cannot see a hole inside it ---
if live_cycles != set(range(2239, 2244)):
    sys.exit(f"FAIL: live window is not 2239..2243: {sorted(live_cycles)}")

# --- Verification 6: the dense tail really left the live file ---
if any(header_cycle(l) is not None and header_cycle(l) <= 2227 for l in kept):
    sys.exit("FAIL: a dense tail block is still live")
if sum(1 for l in archived if header_cycle(l) is not None and header_cycle(l) <= 2227) != 16:
    sys.exit("FAIL: expected all 16 dense tail blocks in the archive addition")

print("All 6 verifications passed. Writing files.")
with open(SRC, "w") as f:
    f.write(live_text)
with open(ARCHIVE, "w") as f:
    f.write(new_archive)
print(f"live STATUS.md:   {len(kept)} lines / {len(live_text.encode())} bytes "
      f"({len(live_text.encode())/1024:.1f}KB)")
print(f"archive addition: {len(archived)} lines")
print(f"live cycles kept: {sorted(live_cycles, reverse=True)}")
