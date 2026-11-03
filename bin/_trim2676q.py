#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2676 (90.3KB/974 lines, TRIM SOON).

check-doc-size read TRIM SOON on this file at preflight (90.3KB/974 lines,
~21 cycles of headroom at +5440 B/cycle, proj. 218KB at the checker's next
look). Cycle 2676 is a QUALITY/GROWTH slot (2676 % 3 == 0) -- the slot the
checker itself asks for, per doc-trim cadence rule 2.

Standing-hazard grep run FIRST (before this script), over all 426
archive-bound lines (the 16 DONE blocks that are not the newest): ZERO strong
hits. Consistent with c2652's rule that a grep over closed DONE blocks is
almost always clean because a DONE block records work already homed
elsewhere; nothing here touches an OPEN item's prose. CLEAN.

Margin arithmetic (cadence rule 4): 426 of 974 lines leave ~548 live (~52KB),
projecting ~182KB against the 200KB line at the next look -- ~18KB of margin,
above the ~15KB threshold, so a DONE-only cut is sufficient this cycle and no
OPEN-item compression is needed (unlike c2652).

Same hoist-then-cut method as 2588/.../2643/2652: keep every OPEN block plus
only the single newest-by-cycle-number DONE block (for its "next cycle"
pointer), archive the rest in original document order under a dated header in
queue_archive.md.

Structure re-derived fresh at 2676 (cadence rule 3, never pasted forward):
43 top-level blocks = 17 DONE + 26 open. The newest DONE block (2675) IS the
first block in the file this time, but the partition is still derived purely
from the parsed block list rather than relying on that. Run BEFORE this
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

assert len(lines) == 974, f"expected 974 lines, got {len(lines)} -- file changed, abort"

starts = [i for i, l in enumerate(lines) if TOP_RE.match(l)]
assert starts[0] == 0, "file must begin with a top-level item"
ends = starts[1:] + [len(lines)]

blocks = []
for s, e in zip(starts, ends):
    is_done = TOP_RE.match(lines[s]).group(1) == "x"
    cyc = None
    if is_done:
        m = CYCLE_RE.search("".join(lines[s:min(s + 3, e)]))
        cyc = int(m.group(1) or m.group(2)) if m else -1
    blocks.append({"s": s, "e": e, "done": is_done, "cycle": cyc})

done_blocks = [b for b in blocks if b["done"]]
assert len(done_blocks) == 17, f"expected 17 DONE blocks, got {len(done_blocks)}"
assert -1 not in (b["cycle"] for b in done_blocks), "a DONE block's cycle number could not be parsed"
open_blocks = [b for b in blocks if not b["done"]]
assert len(open_blocks) == 26, f"expected 26 open blocks, got {len(open_blocks)}"

newest_done = max(done_blocks, key=lambda b: b["cycle"])
assert newest_done["cycle"] == 2675, f"expected newest DONE block to be 2675, got {newest_done['cycle']}"

keep_blocks = [b for b in blocks if not b["done"] or b is newest_done]
archive_blocks = [b for b in blocks if b["done"] and b is not newest_done]
assert len(archive_blocks) == 16
assert len(keep_blocks) == 27  # 26 open + 1 kept DONE
assert len(keep_blocks) + len(archive_blocks) == len(blocks)

reassembled = []
for b in sorted(blocks, key=lambda b: b["s"]):
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
    m = TOP_RE.match(l)
    if m and m.group(1) == " ":
        sys.exit(f"FAIL: an OPEN item landed in the archive set: {l[:90]!r}")

keep_txt = "".join(keep_lines)

with open(ARCHIVE) as f:
    old_archive = f.read()

addition = (
    "\n## Archived at cycle 2676 (queue.md trim, `bin/_trim2676q.py`) -- "
    "16 DONE blocks, document order preserved\n\n" + "".join(archive_lines)
)
new_archive = old_archive + addition

for ln in archive_lines:
    if ln.strip() and ln not in addition:
        sys.exit(f"FAIL: archived line missing from addition: {ln[:90]!r}")
if not new_archive.startswith(old_archive):
    sys.exit("FAIL: pre-existing archive would not be preserved byte-identically")

with open(ARCHIVE, "w") as f:
    f.write(new_archive)
with open(SRC, "w") as f:
    f.write(keep_txt)

print("All verifications passed.")
print(f"live queue.md: {len(keep_lines)} lines / {len(keep_txt.encode())/1024:.1f}KB "
      f"({len(open_blocks)} open + 1 DONE kept)")
print(f"archived: {len(archive_lines)} lines, {len(archive_blocks)} DONE blocks")
