#!/root/agent/venv/bin/python
"""Cycle 3872 state/STATUS.md trim.

WHY NOW: `bin/check-doc-size` read it TRIM DUE at 170.6KB/390 lines (~7 cycles
of headroom, proj. 276KB at the next look) BEFORE this cycle prepended its own
8.7KB block. Method = the cycle 1836/1799 lineage, same shape as
`bin/_trim3852s.py`: keep the newest 10 cycle blocks live, append the remainder
VERBATIM to `state/STATUS_ARCHIVE.md` under a dated header, newest-first order
unchanged. STATUS.md is a plain historical log -- no live open items and no
cross-references to strand, unlike tasks/queue.md.

BOUNDARY RE-DERIVED FRESH (and heeding _trim3852s.py's own warning that a grep
for one header form undercounts): this file mixes THREE block-header forms --
bare `Updated: ...`, `PRIOR: Updated: ...`, and a `## Previous cycle (N)` line
followed by `Updated: ...`. Counting all three, 34 blocks are live, newest
first: 3872, 3871, 3870, 3869, 3868, 3867, 3866, 3865, 3864, 3863 | 3862, 3861,
3860, 3859, 3858, 3857, 3856, 3855, 3854, 3853, 3852, 3851, 3850, 3849, 3848,
3847, 3845, 3844, 3843, 3842, 3841, 3840, 3839, 3838. A grep for `^Updated: `
alone would have found only 17 and cut far too deep.

So block 10 is c3863; it ends at the `---` separator on line 137, and block 11
(c3862) starts on line 139. Keep lines 1-137 (10 blocks + the trailing
separator), archive lines 139..end verbatim.
"""
from collections import Counter

STATUS = "/root/agent/state/STATUS.md"
ARCHIVE = "/root/agent/state/STATUS_ARCHIVE.md"

orig = open(STATUS).read()
lines = orig.split("\n")
assert len(lines) == 413, f"unexpected line count {len(lines)} -- re-derive boundary"
assert lines[136] == "---" and lines[137] == "", \
    f"line 137/138 not the separator: {lines[136]!r} {lines[137]!r}"
assert lines[138].startswith("PRIOR: Updated: 2026-11-28 UTC by cycle 3862"), \
    f"line 139 is not block 11's header: {lines[138][:80]!r}"
assert lines[0].startswith("Updated: 2026-11-28 UTC by cycle 3872"), "block 1 is not c3872"

kept = lines[:137]        # lines 1-137 inclusive (index 0-136)
archived = lines[138:]    # lines 139..end (index 138..)

new_live = "\n".join(kept) + "\n"
archived_text = "\n".join(archived)
if archived_text and not archived_text.endswith("\n"):
    archived_text += "\n"

# the 10 blocks that must survive live, and the newest archived one
for cyc in (3872, 3871, 3870, 3869, 3868, 3867, 3866, 3865, 3864, 3863):
    assert f"by cycle {cyc} " in new_live, f"c{cyc} block lost from live file"
for cyc in (3862, 3838):
    assert f"by cycle {cyc} " in archived_text, f"c{cyc} block missing from archive text"
    assert f"by cycle {cyc} " not in new_live, f"c{cyc} block still live -- cut did not land"

header = (
    "\n## Archived by cycle 3872 (doc-size TRIM DUE rotation -- plain keep-newest-10\n"
    "## lineage, cycle 1836/1799 method, same shape as bin/_trim3852s.py. Blocks c3862\n"
    "## down through c3838, moved verbatim, newest-first order unchanged. Boundary was\n"
    "## re-derived by counting ALL THREE block-header forms in this file (bare\n"
    "## `Updated:`, `PRIOR: Updated:`, and `## Previous cycle (N)` + `Updated:`): 34\n"
    "## blocks were live, so 24 rotate. A grep for `^Updated: ` alone finds only 17 and\n"
    "## would have cut far too deep -- the exact trap _trim3852s.py warned about. 0 open\n"
    "## cross-references into this span: STATUS.md is a historical log, not a task list.)\n\n"
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
