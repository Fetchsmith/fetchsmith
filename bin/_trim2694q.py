#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2694 (81.1KB/783 lines, TRIM SOON).

check-doc-size read TRIM SOON on this file at preflight (81.1KB/783 lines,
~22 cycles of headroom at +5440 B/cycle, proj. 209KB at the checker's next
look -- past the 200KB trim line). Cycle 2694 is a QUALITY/GROWTH slot
(2694 % 3 == 0, exact), the slot the checker itself asks for (doc-trim
cadence rule 2), and c2693's STATUS.md note explicitly flagged this cycle
to take it proactively.

Standing-hazard grep run FIRST (cadence rule 1), over all 215 archive-bound
lines (the 9 DONE blocks that are not the newest, c2692 down to c2684):
grep for "standing rule|rule N|only here|do not archive|no other home"
found 5 hits, all inside the c2685 DONE block -- every one is a CITATION of
the doc-trim cadence item's own rules (e.g. "Hazard grep run FIRST (cadence
rule 1)"), not a unique home for a rule. The rules themselves live in the
still-open doc-trim-cadence item (STANDING RULES section, kept below).
CLEAN, nothing rehomed.

Margin arithmetic (cadence rule 4): 9 DONE blocks (215 lines, ~14.9KB by
byte share) archived, leaving 30 open blocks + 1 kept DONE block (c2693)
live.

Same hoist-then-cut method as 2588/.../2676/2685: keep every OPEN block
plus only the single newest-by-cycle-number DONE block (for its "next
cycle" pointer), archive the rest in original document order under a
dated header in queue_archive.md.

Structure re-derived fresh at 2694 (cadence rule 3, never pasted forward):
40 top-level blocks = 10 DONE + 30 open. The newest DONE block (2693) is
the first block in the file. Run BEFORE this cycle's own block is added.
"""
import re
import sys

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

TOP_RE = re.compile(r"^- \[([ x])\]")
CYCLE_RE = re.compile(r"cycle (\d+)|c(\d{4})")

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 783, f"expected 783 lines, got {len(lines)} -- file changed, abort"

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
assert len(done_blocks) == 10, f"expected 10 DONE blocks, got {len(done_blocks)}"
assert -1 not in (b["cycle"] for b in done_blocks), "a DONE block's cycle number could not be parsed"
open_blocks = [b for b in blocks if not b["done"]]
assert len(open_blocks) == 30, f"expected 30 open blocks, got {len(open_blocks)}"

newest_done = max(done_blocks, key=lambda b: b["cycle"])
assert newest_done["cycle"] == 2693, f"expected newest DONE block to be 2693, got {newest_done['cycle']}"

keep_blocks = [b for b in blocks if not b["done"] or b is newest_done]
archive_blocks = [b for b in blocks if b["done"] and b is not newest_done]
assert len(archive_blocks) == 9
assert len(keep_blocks) == 31  # 30 open + 1 kept DONE
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
    "\n## Archived at cycle 2694 (queue.md trim, `bin/_trim2694q.py`) -- "
    "9 DONE blocks, document order preserved\n\n" + "".join(archive_lines)
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
