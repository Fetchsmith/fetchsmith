#!/root/agent/venv/bin/python
"""Cycle 3822 state/STATUS.md trim -- QUALITY slot (3822 % 3 == 0).
check-doc-size reads it TRIM DUE at 206.3KB/534 lines, ~-1 cycle of headroom
(proj. 312KB at next look). Method (notes/STANDING.md doc-trim cadence,
cycle 1836/1799 lineage): keep the newest 10 cycle blocks live, append the
remainder VERBATIM to state/STATUS_ARCHIVE.md under a dated header,
newest-first (unchanged order). Simpler than the queue.md lever (plain
historical log, no live cross-references/open items to strand).

Boundary: block 10 (c3812) ends at the '---' separator on line 119; block
11 (c3811) starts at line 121. Keep lines 1-119 (10 blocks + trailing
separator), archive lines 121-534 (blocks 11.. to the end) verbatim.
"""
from collections import Counter

STATUS = "/root/agent/state/STATUS.md"
ARCHIVE = "/root/agent/state/STATUS_ARCHIVE.md"

orig = open(STATUS).read()
lines = orig.split("\n")
assert len(lines) == 535, f"unexpected line count {len(lines)} -- re-derive boundary"
assert lines[118] == "---" and lines[119] == "" and lines[120].startswith("PRIOR: Updated: 2026-11-27 UTC by cycle 3811")

kept = lines[:119]          # lines 1-119 inclusive (index 0-118)
archived = lines[120:]      # lines 121-535 (index 120..)

new_live = "\n".join(kept) + "\n"
archived_text = "\n".join(archived)
if archived_text and not archived_text.endswith("\n"):
    archived_text += "\n"

header = (
    "\n## Archived by cycle 3822 (doc-size TRIM DUE rotation -- plain keep-newest-10\n"
    "## lineage, cycle 1836/1799 method. Blocks c3811 down through the file's oldest\n"
    "## retained block, moved verbatim, newest-first order unchanged. 0 open\n"
    "## cross-references into this span found live elsewhere -- STATUS.md is a\n"
    "## historical log, not a task list, so unlike queue.md there is nothing to\n"
    "## strand.)\n\n"
)

def nb(s):
    return [l for l in s.split("\n") if l.strip()]

assert Counter(nb(new_live)) + Counter(nb(archived_text)) == Counter(nb(orig)), \
    "LOSSLESS CHECK FAILED -- nothing written"

old_archive = open(ARCHIVE).read()
new_archive = old_archive.rstrip("\n") + "\n" + header + archived_text

open(STATUS, "w").write(new_live)
open(ARCHIVE, "w").write(new_archive)

print("STATUS.md:", len(orig), "->", len(new_live), "bytes")
print("archive appended:", len(new_archive) - len(old_archive), "bytes")
