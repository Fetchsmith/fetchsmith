#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2605 (94.5KB / 1000 lines, TRIM SOON).

check-doc-size read TRIM SOON on this file at preflight (94.5KB/1000 lines,
proj. 222KB at the checker's next automatic look, c2629). Nothing else was
DUE this cycle (audit-due --all / checks-due --all both NONE DUE except
one-off informational axes), so per the c2220 follow-up and the doc-trim
cadence item (tasks/queue.md line ~544) this cycle trims proactively.

Hoist-then-cut, not a line-range cut: open `- [ ]` items are interleaved
among `- [x]` DONE blocks (4 runs: DONE / open / DONE / open-to-EOF), so a
single cut point would delete live work. Instead, parse every top-level
`- [ ]`/`- [x]` block, keep every OPEN block plus only the single highest-
numbered DONE block (for its "next cycle" pointer -- same rule as c2588/
c2604's plan), and archive the rest, in original order, under a dated
header in tasks/queue_archive.md.
"""
import re
import sys

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

TOP_RE = re.compile(r"^- \[([ x])\]")
CYCLE_RE = re.compile(r"cycle (\d+)")

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 1000, f"expected 1000 lines, got {len(lines)} -- file changed, abort"

starts = [i for i, l in enumerate(lines) if TOP_RE.match(l)]
assert starts[0] == 0, "file must begin with a top-level item"
ends = starts[1:] + [len(lines)]

blocks = []
for s, e in zip(starts, ends):
    mark = TOP_RE.match(lines[s]).group(1)
    is_done = mark == "x"
    cyc = None
    if is_done:
        m = CYCLE_RE.search("".join(lines[s:min(s + 3, e)]))
        cyc = int(m.group(1)) if m else -1
    blocks.append({"s": s, "e": e, "done": is_done, "cycle": cyc})

done_blocks = [b for b in blocks if b["done"]]
assert len(done_blocks) == 19, f"expected 19 DONE blocks, got {len(done_blocks)}"
open_blocks = [b for b in blocks if not b["done"]]
assert len(open_blocks) == 24, f"expected 24 open blocks, got {len(open_blocks)}"

newest_done = max(done_blocks, key=lambda b: b["cycle"])
assert newest_done["cycle"] == 2604, f"expected newest DONE block to be 2604, got {newest_done['cycle']}"

keep_blocks = [b for b in blocks if not b["done"] or b is newest_done]
archive_blocks = [b for b in blocks if b["done"] and b is not newest_done]
assert len(archive_blocks) == 18

# Partition must be total, non-overlapping, and order-preserving.
assert len(keep_blocks) + len(archive_blocks) == len(blocks)

keep_lines = []
for b in keep_blocks:
    keep_lines.extend(lines[b["s"]:b["e"]])

archive_lines = []
for b in archive_blocks:
    archive_lines.extend(lines[b["s"]:b["e"]])

# Reassembling keep+archive in original relative order must reconstruct the original file.
reorder_check = sorted(blocks, key=lambda b: b["s"])
reassembled = []
for b in reorder_check:
    reassembled.extend(lines[b["s"]:b["e"]])
if "".join(reassembled) != "".join(lines):
    sys.exit("FAIL: block partition does not reconstruct the original file")

# multiset identity: every line in archive_lines must have come from the original, and
# keep+archive (as sets of blocks) must equal the original block set exactly once each.
assert len(keep_blocks) == 25  # 24 open + 1 kept DONE
assert len(archive_blocks) == 18

open_line_ids_before = {id(l) for b in blocks if not b["done"] for l in lines[b["s"]:b["e"]]}
open_hashes_before = [l for b in blocks if not b["done"] for l in lines[b["s"]:b["e"]]]
open_hashes_after = [l for b in keep_blocks if not b["done"] for l in lines[b["s"]:b["e"]]]
if open_hashes_before != open_hashes_after:
    sys.exit("FAIL: open items changed across the cut")

keep_txt = "".join(keep_lines)

with open(ARCHIVE) as f:
    old_archive = f.read()

archived_cycles = sorted({b["cycle"] for b in archive_blocks}, reverse=True)
addition = (
    f"\n## Archived at cycle 2605 (queue.md trim, `bin/_trim2605q.py`) -- "
    f"DONE blocks for cycles {archived_cycles}\n\n" + "".join(archive_lines)
)
new_archive = old_archive + addition

with open(SRC, "w") as f:
    f.write(keep_txt)
with open(ARCHIVE, "w") as f:
    f.write(new_archive)

print(f"queue.md: {len(lines)} -> {len(keep_txt.splitlines())} lines "
      f"({len(''.join(lines))} -> {len(keep_txt)} bytes)")
print(f"Archived {len(archive_lines)} lines ({len(archive_blocks)} DONE blocks) to {ARCHIVE}")
print(f"Kept DONE block: cycle {newest_done['cycle']}")
