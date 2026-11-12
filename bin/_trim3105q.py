#!/usr/bin/env python3
"""Cycle 3105: move the 2 pieces NEW c3084's split plan left for last --
`METHOD c3084` (the RULE 6b SEO method/lessons record, L62) and the
`doc-trim cadence` item (L747-878, header+method+STANDING RULES 1-8) -- from
tasks/queue.md to notes/STANDING.md. c3090 already moved the other 6
NEW STANDING items and deliberately left these two for a dedicated pass
("more cross-references, deserve their own hazard-grep"). Hazard grep this
cycle (grep -rn over bin actors site notes state, excluding dead
bin/_trimNNNNq.py one-shots) found no live "see queue.md item cXXXX"
pointer that would go stale -- every hit (bin/store-rank, notes/LEARNINGS.md,
state/STATUS.md, state/STATUS_ARCHIVE.md, state/fleet_checks.json) is a
narrative mention of the c3084 LABEL, which is unchanged by the move, not a
file-path pointer. Self-verifying: lossless multiset diff before writing.
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

def item_span(start0):
    idx = starts.index(start0)
    end0 = starts[idx + 1] if idx + 1 < len(starts) else len(lines)
    return start0, end0

# Locate the two items by their known 1-indexed start lines (verified by hand
# this cycle: L62 "METHOD c3084", L747 "doc-trim cadence"), but don't trust
# the line numbers blindly -- confirm the text at each before cutting.
method_start0 = 61
assert lines[method_start0].startswith("- [ ] **METHOD c3084"), lines[method_start0][:60]
method_span = item_span(method_start0)

doctrim_start0 = 746
assert lines[doctrim_start0].startswith("- [ ] **doc-trim cadence"), lines[doctrim_start0][:60]
doctrim_span = item_span(doctrim_start0)

spans = [method_span, doctrim_span]

# No overlap, correctly ordered
assert spans[0][1] <= spans[1][0], spans

# RULE 7 (c2948 near-miss): assert each span contains EXACTLY ONE top-level
# "- [ ] " line -- its own head -- so no other open/closed item is nested
# inside and would be silently swept up.
for (s0, e0) in spans:
    heads = [i for i in starts if s0 <= i < e0]
    assert heads == [s0], f"span {(s0, e0)} contains unexpected head(s): {heads}"

moved_blocks = []
for (s0, e0) in spans:
    block_lines = lines[s0:e0]
    while block_lines and block_lines[-1] == "":
        block_lines.pop()
    moved_blocks.append("\n".join(block_lines))

new_lines = lines[:]
for (s0, e0) in sorted(spans, key=lambda x: -x[0]):
    del new_lines[s0:e0]

new_queue_text = "\n".join(new_lines)
new_queue_text = re.sub(r"\n{3,}", "\n\n", new_queue_text)

MIGRATION_NOTE = (
    "- [ ] **NEW note (c3105, TRIVIAL -- a pointer, not a task).** The RULE 6b "
    "SEO method (`METHOD c3084`) and the `doc-trim cadence` item's method + "
    "STANDING RULES 1-8 (grep-first, QUALITY-slot-only, re-derive partitions "
    "fresh, margin arithmetic, DONE-block rules, the c3048 whole-repo-citation "
    "hazard grep) moved to `notes/STANDING.md` this cycle (`NEW c3084`'s split, "
    "final slice after c3087/c3090's first two). **Read `notes/STANDING.md` "
    "before: (a) any `tasks/queue.md` trim, (b) any RULE 6b SEO sweep.** Both "
    "are now read-on-demand, not every-cycle, by design -- that is the point "
    "of the split.\n"
)

new_queue_text = new_queue_text.rstrip("\n") + "\n\n" + MIGRATION_NOTE

append_text = "\n\n" + "\n\n".join(moved_blocks) + "\n"
new_standing_text = standing_text.rstrip("\n") + append_text

HEADER_OLD = (
    'read every cycle" rule does not apply to them. Still not moved: the\n'
    "`METHOD c3084` record and the `STANDING RULES` section inside the\n"
    "doc-trim-cadence item in `queue.md` (left for a future QUALITY slot)."
)
HEADER_NEW = (
    'read every cycle" rule does not apply to them. Cycle 3105 moved the final\n'
    "slice: the `METHOD c3084` record and the full `doc-trim cadence` item\n"
    "(method + STANDING RULES 1-8), hazard-grepped first (see\n"
    "`bin/_trim3105q.py`'s docstring) -- no live file-path pointer to either was\n"
    "found outside queue.md itself, only narrative mentions of the c3084 label,\n"
    "which is unchanged by the move. `NEW c3084`'s split is now COMPLETE."
)
assert HEADER_OLD in new_standing_text, "expected header sentence not found verbatim"
new_standing_text = new_standing_text.replace(HEADER_OLD, HEADER_NEW)

def nonblank_lines(s):
    return [l for l in s.split("\n") if l.strip() != ""]

from collections import Counter

orig_queue_nb = nonblank_lines(queue_text)
orig_standing_nb = nonblank_lines(standing_text)

expected = Counter(orig_queue_nb) + Counter(orig_standing_nb)
# account for the added migration note and the header rewrite: remove old header
# lines from "expected" and add new ones, add migration note lines
expected = expected - Counter(nonblank_lines(HEADER_OLD)) + Counter(nonblank_lines(HEADER_NEW))
expected = expected + Counter(nonblank_lines(MIGRATION_NOTE))

actual = Counter(nonblank_lines(new_queue_text)) + Counter(nonblank_lines(new_standing_text))

missing = expected - actual
extra = actual - expected
assert not missing, f"LOSSY: {len(missing)} line(s) missing, e.g. {list(missing.items())[:5]}"
assert not extra, f"INVENTED: {len(extra)} line(s) extra, e.g. {list(extra.items())[:5]}"

# Structural asserts
assert "- [ ] **METHOD c3084" not in new_queue_text
assert "- [ ] **doc-trim cadence" not in new_queue_text
assert "METHOD c3084" in new_standing_text
assert "doc-trim cadence" in new_standing_text
assert "STANDING RULE 8" in new_standing_text
assert "NEW (c2478)" in new_queue_text, "guarded 2026-11-15 deadline item must survive untouched"
assert "NEW STANDING TRIPWIRE (c2336" in new_queue_text, "live triage tripwire must survive untouched"
assert "NEW c3084 (HIGH" in new_queue_text, "the task item itself (to be rewritten EXECUTED by hand) must survive"

print("All asserts passed.")
print(f"queue.md: {len(queue_text)} -> {len(new_queue_text)} bytes")
print(f"STANDING.md: {len(standing_text)} -> {len(new_standing_text)} bytes")

with open(QUEUE, "w") as f:
    f.write(new_queue_text)
with open(STANDING, "w") as f:
    f.write(new_standing_text)
print("Written.")
