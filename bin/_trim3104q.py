#!/usr/bin/env python3
"""Cycle 3104: routine newest-5-floor rotation of tasks/queue.md's CLOSED cycle
blocks. 6 were live (c3102, c3098..c3094) -- counted, not assumed, per the c3084
interim rule -- against the 5-block floor established by c3087/c3097. Moves the
single OLDEST (c3094) verbatim to tasks/queue_archive.md, keeping c3095-c3102 live.

This rotation is NOT a fix for the standing `TRIM DUE` on queue.md and is not
presented as one: at 170.8KB the file is ~100KB above what check-doc-size wants,
and a 1-block rotation recovers single-digit KB. See `NEW c3084` -- the structural
split is the only lever that closes it, and c3105 (% 3 == 0) is a QUALITY slot.

Self-verifying: dry-run multiset diff before writing either file, modeled on
bin/_trim3102q.py.
"""
import re
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
MOVE_LABELS = ["c3094"]

with open(QUEUE, encoding="utf-8") as f:
    queue_text = f.read()
with open(ARCHIVE, encoding="utf-8") as f:
    archive_text = f.read()

lines = queue_text.split("\n")
starts = [i for i, l in enumerate(lines) if re.match(r"^- \[[ x]\] ", l)]

def item_span(start0):
    idx = starts.index(start0)
    end0 = starts[idx + 1] if idx + 1 < len(starts) else len(lines)
    return start0, end0

# Guard: the floor only means something if the live count is what we think it is.
live_closed = [m.group(1) for l in lines
               for m in [re.match(r"^- \[ \] \*\*CLOSED (c3\d\d\d) ", l)] if m]
assert len(live_closed) == 6, f"expected 6 live CLOSED blocks, found {len(live_closed)}: {live_closed}"
assert live_closed[-1] == "c3094", f"oldest live block is {live_closed[-1]}, not c3094"

spans = []
for i in starts:
    m = re.match(r"^- \[ \] \*\*CLOSED (c3\d\d\d) ", lines[i])
    if m and m.group(1) in MOVE_LABELS:
        spans.append((item_span(i), m.group(1)))

assert len(spans) == 1, f"expected 1 CLOSED block, found {len(spans)}: {spans}"
assert [lbl for (_, lbl) in spans] == MOVE_LABELS

moved_blocks = []
for (s0, e0), label in spans:
    block_lines = lines[s0:e0]
    while block_lines and block_lines[-1] == "":
        block_lines.pop()
    moved_blocks.append("\n".join(block_lines))

new_lines = lines[:]
for (s0, e0), label in sorted(spans, key=lambda x: -x[0][0]):
    del new_lines[s0:e0]

new_queue_text = re.sub(r"\n{3,}", "\n\n", "\n".join(new_lines))

HEADER = ("\n## Archived by cycle 3104 (opus-5), 2026-11-12 -- routine "
          "newest-5-floor rotation of tasks/queue.md's CLOSED cycle blocks "
          "(6 live -> 5, counted per the c3084 interim rule). Moved verbatim: "
          "CLOSED c3094. c3095-c3102 remain live in queue.md. This does NOT "
          "clear the standing TRIM DUE -- see NEW c3084.\n\n")
append_text = HEADER + "\n\n".join(moved_blocks) + "\n"
new_archive_text = archive_text.rstrip("\n") + "\n" + append_text

# --- Losslessness check: every non-blank line of the old queue must survive,
# --- either still in the queue or appended to the archive.
def nonblank(s):
    return Counter(l for l in s.split("\n") if l.strip())

before = nonblank(queue_text)
# The archive HEADER is the one line this move legitimately introduces; everything
# else must be a line that already existed in queue.md.
after = nonblank(new_queue_text) + nonblank(append_text) - nonblank(HEADER)
missing = before - after
extra = after - before
assert not missing, f"LOSSY -- {sum(missing.values())} line(s) dropped: {list(missing)[:3]}"
assert not extra, f"ADDED unexpected line(s): {list(extra)[:3]}"

arch_before = nonblank(archive_text)
assert nonblank(new_archive_text) - (arch_before + nonblank(append_text)) == Counter()

with open(QUEUE, "w", encoding="utf-8") as f:
    f.write(new_queue_text)
with open(ARCHIVE, "w", encoding="utf-8") as f:
    f.write(new_archive_text)

print(f"queue.md {len(queue_text)} -> {len(new_queue_text)} bytes "
      f"({len(queue_text) - len(new_queue_text)} moved)")
print(f"archive  {len(archive_text)} -> {len(new_archive_text)} bytes")
print("lossless: verified (non-blank line multiset preserved)")
