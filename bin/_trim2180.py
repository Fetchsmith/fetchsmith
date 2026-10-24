#!/usr/bin/env python3
"""One-shot trim of state/STATUS.md for cycle 2180 (TRIM DUE at 151.2KB).

Stock STATUS.md process (cycles 1836/2095/2133/2157): keep the newest N cycle
blocks live, append the remainder VERBATIM to the end of state/STATUS_ARCHIVE.md
under a dated '## Archived by cycle <N>' header, newest-first, same order as the
source file. Verify losslessly before writing.

Deliberate deviation from "keep 10": at this file's measured growth (+4510 B/cycle)
and check-doc-size's own 24-cycle interval, keeping 10 blocks leaves 50.9KB live and
projects 159KB at the next look -- i.e. it would land back in WARN immediately, the
exact mistake cycle 1976 made and documented. Keeping 6 leaves 30.8KB live and
projects 139KB, under the 150KB warn line with real room to spare.
"""
import sys

SRC = "/root/agent/state/STATUS.md"
ARCHIVE = "/root/agent/state/STATUS_ARCHIVE.md"
KEEP_BLOCKS = 6

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 1773, f"expected 1773 lines, got {len(lines)} -- file changed, abort"

starts = [i for i, l in enumerate(lines) if l.startswith("Updated: ")]
assert len(starts) == 34, f"expected 34 cycle blocks, got {len(starts)}"
assert starts[0] == 0, "file must begin with a cycle block"
assert "cycle 2180" in lines[0], "newest block is not cycle 2180"

cut = starts[KEEP_BLOCKS]          # 0-indexed first line of the oldest KEPT-OUT block
kept = lines[:cut]
archived = lines[cut:]
assert "cycle 2175" in lines[starts[KEEP_BLOCKS - 1]], "kept-oldest block is not cycle 2175"
assert "cycle 2174" in lines[cut], "archive-newest block is not cycle 2174"

with open(ARCHIVE) as f:
    old_archive = f.read()

header = (
    "\n## Archived by cycle 2180 (opus-5), 2026-10-24 -- STATUS.md had grown to 1773 lines / "
    "151.2KB, TRIM DUE per check-doc-size. Cycles <=2174 moved here verbatim; the live file keeps "
    "the newest 6 cycle blocks (2180 down to 2175). Only 6, not the stock 10: at the measured "
    "+4510 B/cycle growth and this check's own 24-cycle interval, keeping 10 would have left "
    "50.9KB live and projected 159KB at the next look -- straight back into WARN (the cycle-1976 "
    "mistake). Keeping 6 leaves 30.8KB and projects 139KB. Newest-first below, same order as the "
    "source file.\n\n"
)
addition = header + "".join(archived)

# --- Verification 1: every non-blank archived line is present verbatim in the addition ---
for ln in archived:
    if ln.strip() and ln not in addition:
        sys.exit(f"FAIL: archived line missing from addition: {ln!r}")

# --- Verification 2: exact full-file reconstruction (no line lost/duplicated/reordered) ---
if "".join(kept + archived) != "".join(lines):
    sys.exit("FAIL: kept + archived does not reconstruct the original file")

# --- Verification 3: prior archive content is untouched, addition only appends ---
new_archive = old_archive + addition
if not new_archive.startswith(old_archive):
    sys.exit("FAIL: prior archive content would not be preserved byte-identically")

# --- Verification 4: every cycle header in the original still exists in live+archive ---
orig_headers = [l for l in lines if l.startswith("Updated: ")]
live_text, arch_text = "".join(kept), new_archive
for h in orig_headers:
    if h not in live_text and h not in arch_text:
        sys.exit(f"FAIL: cycle header would be destroyed: {h[:80]!r}")

print("All checks passed. Writing files.")
with open(SRC, "w") as f:
    f.write("".join(kept))
with open(ARCHIVE, "w") as f:
    f.write(new_archive)
print(f"live STATUS.md: {len(kept)} lines / {len(live_text.encode())} bytes")
print(f"archive addition: {len(archived)} lines")
