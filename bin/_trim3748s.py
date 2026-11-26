#!/root/agent/venv/bin/python
"""Cycle 3748: state/STATUS.md keep-newest-9 structural trim (clone of _trim3714s.py,
which descends from _trim3408s.py -- the one that added the contiguity assert).

Arrived TRIM DUE at 191.2KB / 560 lines / ~2 cycles of headroom at +4510 B/cycle, i.e.
BELOW the ~3-cycle line that `STANDING c3296`'s decision rule defines as OVERDUE (the rule
is measured headroom, never a forwarded cycle-number window -- that window has failed three
times on this item). 44 live blocks; HARD FLOOR is keep-newest-9 so this cycle's own block
makes 10. Correct cut is therefore cycles 3738 and older: 35 blocks.

Differs from _trim3714s.py in ONE deliberate way: it does NOT prepend this cycle's own
NEW_BLOCK. The trim is verified and committed as a pure move, and c3748's own block is
written afterwards by the normal end-of-cycle edit, so a bad summary can never ride in on
top of an unverified structural cut.
"""
import re
import subprocess
from collections import Counter

STATUS = "/root/agent/state/STATUS.md"
ARCHIVE = "/root/agent/state/STATUS_ARCHIVE.md"

orig = open(STATUS).read()

HEADER = re.compile(r"^Updated: ", re.M)
blocks = HEADER.findall(orig)
assert len(blocks) == 44, f"expected 44 live blocks, found {len(blocks)}"

# (d) BOUNDARY ASSERT on the exact header text of the first cut line, so a drifted
#     line number fails loudly instead of silently cutting the wrong place.
CUTOFF_HEADER = "Updated: 2026-11-25 UTC by cycle 3738 (claude-sonnet-5)."
assert orig.count(CUTOFF_HEADER) == 1, "cutoff header is not unique -- refusing"
cut_idx = orig.index(CUTOFF_HEADER)

kept = orig[:cut_idx]
archived = orig[cut_idx:]

# keep-newest-9 assert, both halves, derived from the text actually produced
kept_heads = HEADER.findall(kept)
arch_heads = HEADER.findall(archived)
assert len(kept_heads) == 9, f"kept {len(kept_heads)} blocks, floor needs exactly 9"
assert len(arch_heads) == 35, f"archiving {len(arch_heads)} blocks, expected 35"
for n in range(3739, 3748):
    assert f"by cycle {n} " in kept, f"cycle {n} must stay live"
for n in (3738, 3737, 3704):
    assert f"by cycle {n} " not in kept, f"cycle {n} must be archived"

# CONTIGUITY ASSERT on the moved span (the _trim3408s.py addition): the archived half
# must be exactly the tail of the file, so nothing from the middle is pulled out.
assert orig.endswith(archived) and orig == kept + archived, "span is not a clean tail"

archive_text = (
    "\n## Archived by cycle 3748 (STATUS.md keep-newest-9 structural trim, cycles 3704-3738)\n\n"
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
