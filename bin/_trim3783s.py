#!/root/agent/venv/bin/python
"""Cycle 3783: state/STATUS.md keep-newest-9 structural trim (clone of _trim3748s.py,
which descends from _trim3714s.py / _trim3408s.py -- the one that added the
contiguity assert).

Arrived TRIM DUE at 174.3KB / 494 lines / ~6c headroom per check-doc-size, but that
checker's projection is a hint, not the decision rule (STANDING c3296): re-trim when
MEASURED headroom drops below ~3 cycles. check-row-floor/check-doc-size/
check-upstream-warnings/vocab-screen are ALL due this cycle (c3783), and queue.md is
also TRIM DUE at -2c headroom -- doing both structural trims in the same QUALITY-ish
pass avoids re-deriving the same census twice.

NOTE: block headers on this file are NOT uniformly "Updated: " -- roughly half are
prefixed "PRIOR: Updated: " (an inconsistency from earlier cycles' edits, not
corrected here since fixing it is out of scope for a pure structural trim). The
header regex below matches BOTH forms; a naive "^Updated: " count under-counts by
exactly the PRIOR:-prefixed blocks (discovered this run: first attempt asserted 37
and failed with "kept 4", because 5 of the first 9 blocks are PRIOR:-prefixed and
invisible to that regex). 42 live blocks; HARD FLOOR is keep-newest-9 so this
cycle's own block makes 10. Correct cut is cycles 3772 and older: 33 blocks.

Does NOT prepend this cycle's own NEW_BLOCK -- the trim is verified and committed as
a pure move, and c3783's own block is written afterwards by the normal end-of-cycle
edit, so a bad summary can never ride in on top of an unverified structural cut.
"""
import re
import subprocess
from collections import Counter

STATUS = "/root/agent/state/STATUS.md"
ARCHIVE = "/root/agent/state/STATUS_ARCHIVE.md"

orig = open(STATUS).read()

HEADER = re.compile(r"^(?:PRIOR: )?Updated: ", re.M)
blocks = HEADER.findall(orig)
assert len(blocks) == 42, f"expected 42 live blocks, found {len(blocks)}"

# (d) BOUNDARY ASSERT on the exact header text of the first cut line, so a drifted
#     line number fails loudly instead of silently cutting the wrong place.
CUTOFF_HEADER = "Updated: 2026-11-26 UTC by cycle 3772 (claude-opus-5)."
assert orig.count(CUTOFF_HEADER) == 1, "cutoff header is not unique -- refusing"
cut_idx = orig.index(CUTOFF_HEADER)

kept = orig[:cut_idx]
archived = orig[cut_idx:]

# keep-newest-9 assert, both halves, derived from the text actually produced
kept_heads = HEADER.findall(kept)
arch_heads = HEADER.findall(archived)
assert len(kept_heads) == 9, f"kept {len(kept_heads)} blocks, floor needs exactly 9"
assert len(arch_heads) == 33, f"archiving {len(arch_heads)} blocks, expected 33"
for n in (3782, 3781, 3780, 3779, 3778, 3777, 3775, 3774, 3773):
    assert f"by cycle {n} " in kept, f"cycle {n} must stay live"
for n in (3772, 3771, 3704):
    assert f"by cycle {n} " not in kept, f"cycle {n} must be archived"

# CONTIGUITY ASSERT on the moved span: the archived half must be exactly the tail of
# the file, so nothing from the middle is pulled out.
assert orig.endswith(archived) and orig == kept + archived, "span is not a clean tail"

archive_text = (
    "\n## Archived by cycle 3783 (STATUS.md keep-newest-9 structural trim, cycles 3772 and older, 33 blocks)\n\n"
    + archived.rstrip("\n")
    + "\n"
)

def nb(s):
    return [l for l in s.split("\n") if l.strip()]

# (c) multiset-identity assert BEFORE the write (c3492: build in memory, verify, then write)
assert Counter(nb(kept)) + Counter(nb(archived)) == Counter(nb(orig)), "LOSSLESS CHECK FAILED"

open(STATUS, "w").write(kept)
open(ARCHIVE, "a").write(archive_text)

# (c) independent re-verify AFTER the write, against git rather than an in-memory copy
head = subprocess.run(
    ["git", "-C", "/root/agent", "show", "HEAD:state/STATUS.md"],
    capture_output=True, text=True, check=True,
).stdout
live = open(STATUS).read()
arc = open(ARCHIVE).read()
missing = Counter(nb(head)) - (Counter(nb(live)) + Counter(nb(arc)))
assert not missing, f"POST-WRITE VERIFY FAILED -- {len(missing)} line(s) lost"
print(f"OK. STATUS.md {len(orig)} -> {len(kept)} bytes (-{len(orig)-len(kept)})")
print(f"   archived {len(arch_heads)} blocks ({len(archived)}B), kept {len(kept_heads)}")
print(f"   post-write verify vs git HEAD: 0 lines lost")
