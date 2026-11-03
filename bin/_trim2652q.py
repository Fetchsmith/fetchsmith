#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2652 (95.4KB/1039 lines, TRIM SOON).

check-doc-size read TRIM SOON on BOTH live docs at this cycle's preflight
(queue.md 95.4KB/1039 lines, ~20 cycles of headroom at +5440 B/cycle, proj.
223KB at the checker's next look). Cycle 2652 is a QUALITY/GROWTH slot
(2652 % 3 == 0) -- the slot the checker itself asks for, and the one c2650
named as the natural trim point.

Standing-hazard grep run FIRST (before this script), over all 354
archive-bound lines (the 10 DONE blocks that are not the newest). 10 keyword
hits, all narrative inside the closed items themselves. The one that reads
like a real standing instruction -- "read each one's call sites ... before
converting -- do not batch-convert from the grep count alone" -- is a
caution for the (now CLOSED, c2650) Actor.fail() campaign, and its live
equivalent for the still-OPEN AbortSignal/timeout campaign is stated
verbatim in that live open queue item ("read before patching, they may
already be covered (do not assume from the grep count)"). The rest
(feed-syndication "do not re-litigate" -> LEARNINGS.md:7058-7066; "6/7 free
directories closed" -> PLAYBOOK.md:231; /blog/null footnote) are c2643's own
records of already-verified rehoming. CLEAN -- nothing needed rehoming.

Same hoist-then-cut method as 2588/2604/2605/2619/2628/2634/2643: keep every
OPEN block plus only the single newest-by-cycle-number DONE block (for its
"next cycle" pointer), archive the rest in original document order under a
dated header in queue_archive.md.

Structure at 2652: 35 top-level blocks = 11 DONE (2647, 2648, 2649, 2650,
2648, 2645, 2651, 2646, 2644, 2643, 2642 in document order) + 24 open. Unlike
every prior trim, the newest DONE block (2651) is NOT the first block in the
file -- it sits at line 218, with older DONE blocks above it -- so the
`newest_done is first block` assert from _trim2643q.py is deliberately
dropped and the partition is derived purely from the parsed block list. Run
BEFORE this cycle's own block is added.
"""
import re
import sys

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

TOP_RE = re.compile(r"^- \[([ x])\]")
CYCLE_RE = re.compile(r"cycle (\d+)|c(\d{4})")

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 1039, f"expected 1039 lines, got {len(lines)} -- file changed, abort"

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
assert len(open_blocks) == 24, f"expected 24 open blocks, got {len(open_blocks)}"

newest_done = max(done_blocks, key=lambda b: b["cycle"])
assert newest_done["cycle"] == 2651, f"expected newest DONE block to be 2651, got {newest_done['cycle']}"
assert newest_done["s"] == 217, f"expected the 2651 DONE block at 0-based line 217, got {newest_done['s']}"

keep_blocks = [b for b in blocks if not b["done"] or b is newest_done]
archive_blocks = [b for b in blocks if b["done"] and b is not newest_done]
assert len(archive_blocks) == 10
assert len(keep_blocks) == 25  # 24 open + 1 kept DONE

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

if len(keep_lines) + len(archive_lines) != len(lines):
    sys.exit("FAIL: keep + archive line counts do not sum to the original")

open_lines_before = [l for b in blocks if not b["done"] for l in lines[b["s"]:b["e"]]]
open_lines_after = [l for b in keep_blocks if not b["done"] for l in lines[b["s"]:b["e"]]]
if open_lines_before != open_lines_after:
    sys.exit("FAIL: open items changed across the cut")

for l in archive_lines:
    if TOP_RE.match(l) and TOP_RE.match(l).group(1) == " ":
        sys.exit(f"FAIL: an OPEN item landed in the archive set: {l[:90]!r}")

keep_txt = "".join(keep_lines)

with open(ARCHIVE) as f:
    old_archive = f.read()

archived_cycles = sorted({b["cycle"] for b in archive_blocks}, reverse=True)
addition = (
    f"\n## Archived at cycle 2652 (queue.md trim, `bin/_trim2652q.py`) -- "
    f"DONE blocks for cycles {archived_cycles} (non-contiguous: the newest DONE "
    f"block, c2651, sat BELOW several older ones and is kept live)\n\n"
    + "".join(archive_lines)
)
new_archive = old_archive + addition

with open(SRC, "w") as f:
    f.write(keep_txt)
with open(ARCHIVE, "w") as f:
    f.write(new_archive)

print(f"kept {len(keep_lines)} lines, archived {len(archive_lines)} lines, cycles {archived_cycles}")
