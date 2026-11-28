#!/root/agent/venv/bin/python
"""Cycle 3852 state/STATUS.md trim -- QUALITY slot (3852 % 3 == 0).
check-doc-size reads it TRIM DUE at 200.6KB/434 lines, ~-0 cycles of headroom
(proj. 306KB at next look, +4510 B/cycle). Method (notes/STANDING.md doc-trim
cadence, cycle 1836/1799 lineage, same shape as bin/_trim3822s.py): keep the
newest 10 cycle blocks live, append the remainder VERBATIM to
state/STATUS_ARCHIVE.md under a dated header, newest-first (order unchanged).
Simpler than the queue.md lever -- STATUS.md is a plain historical log with no
live open items or cross-references to strand.

Boundary re-derived fresh this cycle (NOT inherited from c3822). The 10 newest
blocks are c3851, 3850, 3849, 3847, 3845, 3844, 3841, 3840, 3839, 3838 -- note
3841/3840/3839 use the `## Previous cycle (N)` + `Updated: ... by cycle N`
two-line header form, not the `PRIOR: Updated:` form, so a grep for
`^PRIOR: Updated:` alone undercounts blocks and would cut 3 blocks too deep.
Block 10 (c3838) ends at the '---' separator on line 148; block 11 (c3837)
starts at line 150. Keep lines 1-148 (10 blocks + trailing separator), archive
lines 150..end verbatim.
"""
from collections import Counter

STATUS = "/root/agent/state/STATUS.md"
ARCHIVE = "/root/agent/state/STATUS_ARCHIVE.md"

orig = open(STATUS).read()
lines = orig.split("\n")
assert len(lines) == 435, f"unexpected line count {len(lines)} -- re-derive boundary"
assert lines[147] == "---" and lines[148] == "", f"line 148/149 not the separator: {lines[147]!r}"
assert lines[149].startswith("PRIOR: Updated: 2026-11-27 UTC by cycle 3837"), \
    f"line 150 is not block 11's header: {lines[149][:80]!r}"

kept = lines[:148]          # lines 1-148 inclusive (index 0-147)
archived = lines[149:]      # lines 150..end (index 149..)

new_live = "\n".join(kept) + "\n"
archived_text = "\n".join(archived)
if archived_text and not archived_text.endswith("\n"):
    archived_text += "\n"

header = (
    "\n## Archived by cycle 3852 (doc-size TRIM DUE rotation -- plain keep-newest-10\n"
    "## lineage, cycle 1836/1799 method. Blocks c3837 down through the file's oldest\n"
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
