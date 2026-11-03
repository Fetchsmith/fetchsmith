#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2643 (80.1KB/867 lines, TRIM SOON).

check-doc-size read TRIM SOON at this cycle's preflight (projected 208KB at
its next look, same as predicted at c2641/c2642). Cycle 2643 is a
QUALITY/GROWTH slot (2643 % 3 == 0) -- c2641/c2642 both correctly deferred
this trim to here per the checker's own guidance.

Standing-hazard grep run FIRST (before this script), on every line that
sits inside a block to be archived (10 DONE blocks: the 8 contiguous
`DONE cycle N` blocks 2641..2633, plus two older `DONE/CLOSED c2636` blocks
that sit interleaved further down among the open items -- NOT a contiguous
range this time, unlike prior trims). 6 keyword hits, all narrative cautions
inside the closed items themselves:
  - the feed-syndication "do not re-litigate" / "two prior readings wrong"
    language -- durable rule already has a live home at
    notes/LEARNINGS.md:7058-7066 ("Business bottom line, so no future cycle
    re-opens it: the feed works and is syndicated...").
  - "do NOT spend a cycle on feed-directory submissions" -- the underlying
    fact (6/7 free directories closed) already lives at notes/PLAYBOOK.md:231.
  - "do not re-investigate /blog/null 404s in old archived logs" -- a closed-
    bug footnote with no separate live home, but low-risk to archive as-is:
    the full block text (and this caution) survives verbatim in
    queue_archive.md, and the worst case if a future cycle misses it is
    re-discovering the same already-fixed 27 historical 404s.
All CLEAN -- nothing needed rehoming beyond what already has one.

Same hoist-then-cut method as prior trims (2588/2604/2605/2619/2628/2634),
generalized because this cycle's DONE blocks are NOT all contiguous: keep
every OPEN block plus only the single newest-by-cycle-number DONE block (for
its "next cycle" pointer), archive the rest in original document order under
a dated header in queue_archive.md.

Structure at 2643: 32 top-level blocks = 11 DONE (2642,2641,2640,2639,2638,
2637,2635,2634,2633,2636,2636) + 21 open. Newest DONE by cycle number is 2642
at line 0 (also the first block in the file). Run BEFORE this cycle's own
block is added.
"""
import re
import sys

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

TOP_RE = re.compile(r"^- \[([ x])\]")
CYCLE_RE = re.compile(r"cycle (\d+)|c(\d{4})")

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 867, f"expected 867 lines, got {len(lines)} -- file changed, abort"

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
        if m:
            cyc = int(m.group(1) or m.group(2))
        else:
            cyc = -1
    blocks.append({"s": s, "e": e, "done": is_done, "cycle": cyc})

done_blocks = [b for b in blocks if b["done"]]
assert len(done_blocks) == 11, f"expected 11 DONE blocks, got {len(done_blocks)}"
assert -1 not in (b["cycle"] for b in done_blocks), "a DONE block's cycle number could not be parsed"
open_blocks = [b for b in blocks if not b["done"]]
assert len(open_blocks) == 21, f"expected 21 open blocks, got {len(open_blocks)}"

newest_done = max(done_blocks, key=lambda b: b["cycle"])
assert newest_done["cycle"] == 2642, f"expected newest DONE block to be 2642, got {newest_done['cycle']}"
assert newest_done["s"] == 0

keep_blocks = [b for b in blocks if not b["done"] or b is newest_done]
archive_blocks = [b for b in blocks if b["done"] and b is not newest_done]
assert len(archive_blocks) == 10
assert len(keep_blocks) == 22  # 21 open + 1 kept DONE

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

open_lines_before = [l for b in blocks if not b["done"] for l in lines[b["s"]:b["e"]]]
open_lines_after = [l for b in keep_blocks if not b["done"] for l in lines[b["s"]:b["e"]]]
if open_lines_before != open_lines_after:
    sys.exit("FAIL: open items changed across the cut")

keep_txt = "".join(keep_lines)

with open(ARCHIVE) as f:
    old_archive = f.read()

archived_cycles = sorted({b["cycle"] for b in archive_blocks}, reverse=True)
addition = (
    f"\n## Archived at cycle 2643 (queue.md trim, `bin/_trim2643q.py`) -- "
    f"DONE blocks for cycles {archived_cycles} (non-contiguous: includes two "
    f"older DONE/CLOSED c2636 blocks that sat interleaved among open items)\n\n"
    + "".join(archive_lines)
)
new_archive = old_archive + addition

with open(SRC, "w") as f:
    f.write(keep_txt)
with open(ARCHIVE, "w") as f:
    f.write(new_archive)

print(f"kept {len(keep_lines)} lines, archived {len(archive_lines)} lines, cycles {archived_cycles}")
