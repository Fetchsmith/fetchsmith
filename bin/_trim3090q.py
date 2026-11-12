#!/usr/bin/env python3
"""Cycle 3090: move 6 of the 8 NEW STANDING RULE/NOTE/WATCH items from tasks/queue.md
to notes/STANDING.md, per NEW c3084's split plan (PROGRESS c3087 next slice).
Self-verifying: dry-run diff against /tmp copies before writing either real file.
c3020 (preflight step) and c2336 (ext_bad30d tripwire) are deliberately EXCLUDED --
both are every-cycle preflight checks (confirmed still being followed each cycle),
not read-on-demand reference material, so they stay live in queue.md.
"""
import re

QUEUE = "/root/agent/tasks/queue.md"
STANDING = "/root/agent/notes/STANDING.md"

with open(QUEUE) as f:
    queue_text = f.read()
with open(STANDING) as f:
    standing_text = f.read()

lines = queue_text.split("\n")
starts = [i for i, l in enumerate(lines) if re.match(r"^- \[[ x]\] ", l)]
starts_set = set(starts)

# (start_line_1indexed, cycle_label) for the 6 items to move, in file order
MOVE_LABELS = ["c2952", "c2904", "c2812", "c2792", "c2688", "c2664"]

def item_span(start0):
    """0-indexed start line -> (start0, end0_exclusive) up to next top-level bullet or EOF."""
    idx = starts.index(start0)
    end0 = starts[idx + 1] if idx + 1 < len(starts) else len(lines)
    return start0, end0

moved_spans = []
for i in starts:
    text = lines[i]
    if "NEW STANDING" not in text:
        continue
    m = re.search(r"c(\d{4})", text)
    label = "c" + m.group(1) if m else None
    if label in MOVE_LABELS:
        moved_spans.append((item_span(i), label))

assert len(moved_spans) == 6, f"expected 6 matches, got {len(moved_spans)}: {moved_spans}"
found_labels = [lbl for (_, lbl) in moved_spans]
assert found_labels == MOVE_LABELS, f"order/labels mismatch: {found_labels}"

# Extract moved blocks (verbatim, including trailing blank line separators consistent with file style)
moved_blocks = []
for (s0, e0), label in moved_spans:
    block_lines = lines[s0:e0]
    # strip trailing blank lines from the block itself; we'll add separators uniformly
    while block_lines and block_lines[-1] == "":
        block_lines.pop()
    moved_blocks.append("\n".join(block_lines))

# Build new queue.md: remove moved spans (highest index first to keep indices valid)
new_lines = lines[:]
for (s0, e0), label in sorted(moved_spans, key=lambda x: -x[0][0]):
    del new_lines[s0:e0]

new_queue_text = "\n".join(new_lines)
# collapse any resulting 3+ blank lines down to 2 (one blank line separator), cosmetic only
new_queue_text = re.sub(r"\n{3,}", "\n\n", new_queue_text)

# Append to STANDING.md
append_text = "\n\n" + "\n\n".join(moved_blocks) + "\n"
new_standing_text = standing_text.rstrip("\n") + append_text

# --- Losslessness check: every non-blank line of the original queue.md must be
# findable somewhere in (new_queue_text + new_standing_text), and nothing new invented ---
def nonblank_lines(s):
    return [l for l in s.split("\n") if l.strip() != ""]

orig_nb = nonblank_lines(queue_text)
union_nb = nonblank_lines(new_queue_text) + nonblank_lines(new_standing_text) + nonblank_lines(standing_text)
# standing_text already counted once in new_standing_text, so only count it once: recompute properly
union_nb = nonblank_lines(new_queue_text) + nonblank_lines(new_standing_text)

from collections import Counter
orig_count = Counter(orig_nb)
# union should contain orig queue lines (now split between queue+standing) PLUS the original standing lines
pre_standing_nb = nonblank_lines(standing_text)
expected = Counter(orig_nb) + Counter(pre_standing_nb)
actual = Counter(union_nb)
missing = expected - actual
extra = actual - expected
assert not missing, f"LOSSY: {len(missing)} line(s) missing, e.g. {list(missing.items())[:3]}"
assert not extra, f"INVENTED: {len(extra)} line(s) extra, e.g. {list(extra.items())[:3]}"

# --- Structural asserts ---
# no moved label should still appear as a top-level "- [ ] **NEW STANDING" bullet in queue.md
for label in MOVE_LABELS:
    assert not re.search(r"- \[ \] \*\*NEW STANDING[^\n]*" + label, new_queue_text), label
# c3020 and c2336 must still be live in queue.md
assert "NEW STANDING PREFLIGHT STEP (c3020" in new_queue_text
assert "NEW STANDING TRIPWIRE (c2336" in new_queue_text
# all 6 moved labels must now be live in STANDING.md
for label in MOVE_LABELS:
    assert label in new_standing_text, label

print("All asserts passed.")
print(f"queue.md: {len(queue_text)} -> {len(new_queue_text)} bytes")
print(f"STANDING.md: {len(standing_text)} -> {len(new_standing_text)} bytes")

with open(QUEUE, "w") as f:
    f.write(new_queue_text)
with open(STANDING, "w") as f:
    f.write(new_standing_text)
print("Written.")
