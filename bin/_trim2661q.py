#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2661 (83.7KB/917 lines, TRIM SOON).

check-doc-size read TRIM SOON on tasks/queue.md this cycle's preflight
(83.7KB/917 lines, ~22 cycles of headroom at +5440 B/cycle, projected 211KB
at the checker's next scheduled look -- past the 200KB trim line). STATUS.md
is OK (58.2KB, ~32 cycles of headroom) so only queue.md needs cutting.
2661 % 3 == 0 -- a true QUALITY/GROWTH slot, the kind c2660 named as the
natural trim point.

Standing-hazard grep run FIRST (before this script), over all candidate
archive-bound lines (the 10 DONE blocks that are not the newest, c2660).
Hits were narrative inside the closed items themselves (already-resolved
Grants.gov API behavior, URL-encoding allowlist notes, a one-off
"nih-reporter-quebec" naming rule already homed in LEARNINGS.md) or
cross-references to STANDING RULES sections that already live in an OPEN
item by design (the doc-trim cadence item itself carries METHOD + STANDING
RULES + newest execution only, unaffected by this cut since it is OPEN).
The c2646 AbortSignal/timeout-budget campaign and the c2357 bare-throw/
Actor.fail() campaign are BOTH independently confirmed CLOSED with no open
follow-up item anywhere in the live file (grepped for both campaign names
and for the 3 Actors a stale STATUS.md passage once named as "remaining" --
zero hits outside already-archived DONE narrative). CLEAN -- nothing needed
rehoming.

Same hoist-then-cut method as 2588/2604/2605/2619/2628/2634/2643/2652: keep
every OPEN block plus only the single newest-by-cycle-number DONE block (for
its "next cycle" pointer), archive the rest in original document order under
a dated header in queue_archive.md.

Structure at 2661: 34 top-level blocks = 11 DONE (2660, 2659, 2658, 2657,
2656, 2655, 2654, 2653, 2652, 2651, 2646 in document order) + 23 open. The
newest DONE block (2660) IS the first block in the file. Run BEFORE this
cycle's own block is added.
"""
import re
import sys

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

TOP_RE = re.compile(r"^- \[([ x])\]")
CYCLE_RE = re.compile(r"cycle (\d+)|c(\d{4})")

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 917, f"expected 917 lines, got {len(lines)} -- file changed, abort"

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
assert len(open_blocks) == 23, f"expected 23 open blocks, got {len(open_blocks)}"

newest_done = max(done_blocks, key=lambda b: b["cycle"])
assert newest_done["cycle"] == 2660, f"expected newest DONE block to be 2660, got {newest_done['cycle']}"
assert newest_done["s"] == 0, f"expected the 2660 DONE block to be the first block, got start {newest_done['s']}"

keep_blocks = [b for b in blocks if not b["done"] or b is newest_done]
archive_blocks = [b for b in blocks if b["done"] and b is not newest_done]
assert len(archive_blocks) == 10
assert len(keep_blocks) == 24  # 23 open + 1 kept DONE

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
    f"\n## Archived at cycle 2661 (queue.md trim, `bin/_trim2661q.py`) -- "
    f"DONE blocks for cycles {archived_cycles}\n\n"
    + "".join(archive_lines)
)
new_archive = old_archive + addition

with open(SRC, "w") as f:
    f.write(keep_txt)
with open(ARCHIVE, "w") as f:
    f.write(new_archive)

print(f"kept {len(keep_lines)} lines, archived {len(archive_lines)} lines, cycles {archived_cycles}")
