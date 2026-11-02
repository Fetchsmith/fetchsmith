#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2628 (91.9KB / 988 lines, TRIM SOON).

check-doc-size read TRIM SOON on this file at this cycle's preflight
(91.9KB/988 lines, ~20 cycles of headroom at +5440 B/cycle, proj. 219KB at
the checker's next automatic look) and asked for a proactive trim in a
QUALITY slot (c2220 follow-up). Cycle 2628 is a QUALITY/GROWTH slot
(2628 % 3 == 0), so this is that trim. Same cycle also trims STATUS.md
(bin/_trim2628.py).

Same hoist-then-cut method as 2588/2604/2605/2619: open `- [ ]` items are
interleaved among `- [x]` DONE blocks, so a single line-range cut would
delete live work. Parse every top-level `- [ ]`/`- [x]` block, keep every
OPEN block plus only the single highest-numbered DONE block (for its "next
cycle" pointer), and archive the rest, in original order, under a dated
header in tasks/queue_archive.md.

Structure at 2628: 32 top-level blocks = 10 DONE (2618-2627) + 22 open.
Newest DONE is 2627 at line 0. Run BEFORE this cycle's own block is added.
"""
import re
import sys

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

TOP_RE = re.compile(r"^- \[([ x])\]")
CYCLE_RE = re.compile(r"cycle (\d+)")

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 988, f"expected 988 lines, got {len(lines)} -- file changed, abort"

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
assert len(done_blocks) == 10, f"expected 10 DONE blocks, got {len(done_blocks)}"
open_blocks = [b for b in blocks if not b["done"]]
assert len(open_blocks) == 22, f"expected 22 open blocks, got {len(open_blocks)}"

newest_done = max(done_blocks, key=lambda b: b["cycle"])
assert newest_done["cycle"] == 2627, f"expected newest DONE block to be 2627, got {newest_done['cycle']}"
assert newest_done["s"] == 0

keep_blocks = [b for b in blocks if not b["done"] or b is newest_done]
archive_blocks = [b for b in blocks if b["done"] and b is not newest_done]
assert len(archive_blocks) == 9
assert len(keep_blocks) == 23  # 22 open + 1 kept DONE

# Partition must be total, non-overlapping, and order-preserving.
assert len(keep_blocks) + len(archive_blocks) == len(blocks)

reorder_check = sorted(blocks, key=lambda b: b["s"])
reassembled = []
for b in reorder_check:
    reassembled.extend(lines[b["s"]:b["e"]])
if "".join(reassembled) != "".join(lines):
    sys.exit("FAIL: block partition does not reconstruct the original file")

keep_lines = []
for b in sorted(keep_blocks, key=lambda b: b["s"]):
    keep_lines.extend(lines[b["s"]:b["e"]])

archive_lines = []
for b in sorted(archive_blocks, key=lambda b: b["s"]):
    archive_lines.extend(lines[b["s"]:b["e"]])

open_hashes_before = [l for b in blocks if not b["done"] for l in lines[b["s"]:b["e"]]]
open_hashes_after = [l for b in keep_blocks if not b["done"] for l in lines[b["s"]:b["e"]]]
if open_hashes_before != open_hashes_after:
    sys.exit("FAIL: open items changed across the cut")

keep_txt = "".join(keep_lines)

with open(ARCHIVE) as f:
    old_archive = f.read()

archived_cycles = sorted({b["cycle"] for b in archive_blocks}, reverse=True)
addition = (
    f"\n## Archived at cycle 2628 (queue.md trim, `bin/_trim2628q.py`) -- "
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
