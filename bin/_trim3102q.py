#!/usr/bin/env python3
"""Cycle 3102: routine newest-5-floor rotation of tasks/queue.md's CLOSED cycle
blocks. 7 were live (c3098..c3092), above the 5-block floor established by
c3087/c3097. Moves the 2 OLDEST (c3093, c3092) verbatim to tasks/queue_archive.md,
keeping c3094-c3098 live. Self-verifying: dry-run multiset diff before writing
either file, modeled on bin/_trim3097q.py.
"""
import re
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
MOVE_LABELS = ["c3093", "c3092"]  # newest-first, matches file order

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

spans = []
for i in starts:
    m = re.match(r"^- \[ \] \*\*CLOSED (c30\d\d) ", lines[i])
    if m and m.group(1) in MOVE_LABELS:
        spans.append((item_span(i), m.group(1)))

assert len(spans) == 2, f"expected 2 CLOSED blocks, found {len(spans)}: {spans}"
found_labels = [lbl for (_, lbl) in spans]
assert found_labels == MOVE_LABELS, f"order/labels mismatch: {found_labels}"

moved_blocks = []
for (s0, e0), label in spans:
    block_lines = lines[s0:e0]
    while block_lines and block_lines[-1] == "":
        block_lines.pop()
    moved_blocks.append("\n".join(block_lines))

new_lines = lines[:]
for (s0, e0), label in sorted(spans, key=lambda x: -x[0][0]):
    del new_lines[s0:e0]

new_queue_text = "\n".join(new_lines)
new_queue_text = re.sub(r"\n{3,}", "\n\n", new_queue_text)

HEADER = ("\n## Archived by cycle 3102 (sonnet-5), 2026-11-12 -- routine "
          "newest-5-floor rotation of tasks/queue.md's CLOSED cycle blocks "
          "(7 live -> 5). Moved verbatim, newest-first: CLOSED c3093, c3092. "
          "c3094-c3098 remain live in queue.md.\n\n")
append_text = HEADER + "\n\n".join(moved_blocks) + "\n"
new_archive_text = archive_text.rstrip("\n") + "\n" + append_text

# --- Losslessness check ---
def nonblank(s):
    return [l for l in s.split("\n") if l.strip() != ""]

orig_nb = nonblank(queue_text)
new_queue_nb = nonblank(new_queue_text)
pre_archive_nb = nonblank(archive_text)
new_archive_nb = nonblank(new_archive_text)

HEADER_LINE = HEADER.strip()
expected = Counter(orig_nb) + Counter(pre_archive_nb) + Counter([HEADER_LINE])
actual = Counter(new_queue_nb) + Counter(new_archive_nb)
missing = expected - actual
extra = actual - expected
assert not missing, f"LOSSY: {len(missing)} line(s) missing, e.g. {list(missing.items())[:3]}"
assert not extra, f"INVENTED: {len(extra)} line(s) extra, e.g. {list(extra.items())[:3]}"

# --- Structural asserts ---
for label in MOVE_LABELS:
    assert not re.search(r"- \[ \] \*\*CLOSED " + label, new_queue_text), label
    assert label in new_archive_text, label
for keep_label in ["c3098", "c3097", "c3096", "c3095", "c3094"]:
    assert re.search(r"- \[ \] \*\*CLOSED " + keep_label + r" ", new_queue_text), keep_label
# critical standing items must still be present, untouched
assert "NEW (c2478, MEDIUM, deadline 2026-11-15" in new_queue_text
assert "NEW STANDING TRIPWIRE (c2336" in new_queue_text
assert "METHOD c3084" in new_queue_text
assert "NEW c3101" in new_queue_text
assert "NEW c3100" in new_queue_text

print("All asserts passed.")
print(f"queue.md: {len(queue_text)} -> {len(new_queue_text)} bytes "
      f"({len(queue_text)/1024:.1f}KB -> {len(new_queue_text)/1024:.1f}KB)")
print(f"queue_archive.md: {len(archive_text)} -> {len(new_archive_text)} bytes")

with open(QUEUE, "w", encoding="utf-8") as f:
    f.write(new_queue_text)
with open(ARCHIVE, "w", encoding="utf-8") as f:
    f.write(new_archive_text)
print("Written.")
