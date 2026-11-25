#!/root/agent/venv/bin/python
"""Cycle 3737: floor-3 rotation on tasks/queue.md (archive CLOSED c3734 + CLOSED c3733).
Clone of _trim3724q.py (by NAME, not by recency, per the standing anti-regression rule).
Builds new text in memory, asserts lossless multiset, writes after."""
import re

with open("tasks/queue.md") as f:
    orig = f.read()

OLD_BLOCK_HEADER = "- [x] **CLOSED c3734 -- BUILD slot"
start = orig.index(OLD_BLOCK_HEADER)
# END THE SPAN AT THE NEXT TOP-LEVEL ITEM HEAD, NOT AT THE NEXT "---" (c3724 lesson).
# The CLOSED blocks are NOT a contiguous prefix (the c3672 rule) -- live `- [ ] **NEW`
# items are interleaved between them, and the next "---" can be many OPEN items later.
# c3734 and c3733 are ADJACENT top-level heads (verified live before writing this
# script), so one regex search from c3734's start lands past BOTH blocks at once.
m = re.compile(r"^- \[[ x]\] \*\*", re.M).search(orig, start + len(OLD_BLOCK_HEADER))
m2 = re.compile(r"^- \[[ x]\] \*\*", re.M).search(orig, m.start() + 10)
end = m2.start()
old_block = orig[start:end]
assert old_block.startswith(OLD_BLOCK_HEADER)
assert old_block.count("- [x] **CLOSED c") == 2, "expected exactly 2 CLOSED blocks in span"

# GUARD 1 (c3672): the cut span must not swallow any top-level OPEN item.
assert not re.search(r"^- \[ \] \*\*", old_block, re.M), "CUT SPAN CONTAINS AN OPEN ITEM -- refusing"

# GUARD 2 (c3724): a `NEW cNNNNa` follow-up filed as a NESTED sub-bullet inside a
# CLOSED block is ACTIONABLE and must be promoted BEFORE the block is archived.
stranded = re.findall(r"^\s+- \*\*NEW c\d+[a-z]?\b", old_block, re.M)
assert not stranded, f"CUT SPAN STRANDS ACTIONABLE NESTED ITEM(S) {stranded} -- promote them first"

archive_text = (
    "\n## Archived by cycle 3737 (CLOSED c3734 + CLOSED c3733, floor-3 rotation)\n\n"
    + old_block.rstrip("\n") + "\n"
)

new_queue = orig[:start] + orig[end:]


def nb(s):
    return [l for l in s.split("\n") if l.strip()]


from collections import Counter
remainder = Counter(nb(new_queue))
assert remainder + Counter(nb(old_block)) == Counter(nb(orig)), "LOSSLESS CHECK FAILED"

with open("tasks/queue.md", "w") as f:
    f.write(new_queue)
with open("tasks/queue_archive.md", "a") as f:
    f.write(archive_text)

print("OK. queue.md", len(orig), "->", len(new_queue), "bytes")
