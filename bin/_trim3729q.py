#!/usr/bin/env python3
"""Floor-3 CLOSED-block rotation on tasks/queue.md, cycle 3729.
Clone of _trim3726q.py. Archives CLOSED c3724 (the oldest of the three live
CLOSED blocks before this cycle's own block lands), bringing the floor back
to 3 (c3729 own + c3726 + c3725) per the c3672 cadence change (floor is 3,
not 5). c3544 is a standalone cross-reference stub, not part of this
rotation's target set, and is left untouched.

Guards per notes/PLAYBOOK.md c3724 lesson:
(1) cut span ends at the next top-level `- [ ] **` / `- [x] **` head via
    regex, NEVER at the next `---` (CLOSED blocks are not a contiguous
    prefix).
(2) refuse if the span contains any nested `  - **NEW cNNNN` sub-bullet
    (would strand an actionable item in the archive).
(3) verify multiset identity in memory before writing either file.
"""
import re
import sys

Q = "tasks/queue.md"
A = "tasks/queue_archive.md"

with open(Q) as f:
    text = f.read()

HEAD_RE = re.compile(r"^- \[[ x]\] \*\*", re.M)
heads = [m.start() for m in HEAD_RE.finditer(text)]

TARGETS = ["CLOSED c3724"]


def span_for(label, text, heads):
    idx = text.find(f"- [x] **{label}")
    if idx == -1:
        sys.exit(f"FATAL: head for {label} not found")
    if idx not in heads:
        sys.exit(f"FATAL: {label} match is not at a head boundary")
    pos = heads.index(idx)
    end = heads[pos + 1] if pos + 1 < len(heads) else len(text)
    return idx, end


spans = []
for label in TARGETS:
    start, end = span_for(label, text, heads)
    chunk = text[start:end]
    # Guard (2): refuse if a nested NEW cNNNN sub-bullet lives in this span.
    if re.search(r"^\s+- \*\*NEW c\d+", chunk, re.M):
        sys.exit(f"FATAL: {label} span contains a nested NEW cNNNN sub-bullet -- promote it first")
    spans.append((start, end, chunk))

spans.sort(key=lambda s: s[0])
new_queue_parts = []
cursor = 0
archived_chunks = []
for start, end, chunk in spans:
    new_queue_parts.append(text[cursor:start])
    archived_chunks.append(chunk)
    cursor = end
new_queue_parts.append(text[cursor:])
new_queue_text = "".join(new_queue_parts)

archive_header = "## Archived by cycle 3729 (CLOSED c3724, floor-3 rotation)\n\n"
archive_addition = archive_header + "\n".join(archived_chunks) + "\n\n"

removed_lines = []
for _, _, chunk in spans:
    removed_lines.extend([l for l in chunk.split("\n") if l.strip()])
archive_lines = [l for l in archive_addition.split("\n") if l.strip() and not l.startswith("## Archived by cycle")]
assert sorted(removed_lines) == sorted(archive_lines), "LOSSLESS CHECK FAILED -- aborting, no files touched"

with open(A, "a") as f:
    f.write(archive_addition)

with open(Q, "w") as f:
    f.write(new_queue_text)

print(f"OK: archived {len(spans)} block(s), queue.md {len(text)}B -> {len(new_queue_text)}B, archive +{len(archive_addition)}B")
