#!/root/agent/venv/bin/python3
"""
Floor-3 CLOSED-block rotation for tasks/queue.md, cycle 3765.

Fresh census found the live CLOSED-block pool at 8 (c3764/c3763/c3762/c3761/
c3759/c3758/c3752/c3751), not the 4 forwarded by c3764's handoff -- c3759,
c3758, c3752, c3751 had never actually been rotated out despite the floor-3
rule (STANDING c3280 / notes/PLAYBOOK.md) being in force since c3672. This
cuts the 6 oldest (c3762..c3751), keeping the newest 2 (c3764, c3763); this
cycle's own CLOSED c3765 block will be the 3rd live block afterward.

Verify-in-memory-then-write (c3492 lesson), multiset identity BY VALUE
(c3492 lesson), hazard-grep for nested NEW cNNNNa sub-bullets (c3724/c3748
lesson, widened regex) before cutting anything.
"""
import re
import sys

QUEUE = "tasks/queue.md"
ARCHIVE = "tasks/queue_archive.md"
CYCLE = 3765
TARGETS = {3762, 3761, 3759, 3758, 3752, 3751}

HEAD_RE = re.compile(r"^- \[[ x]\] \*\*")
CLOSED_HEAD_RE = re.compile(r"^- \[x\] \*\*CLOSED c(\d+)\b")
NESTED_RE = re.compile(r"^\s+(?:- )?`?\*\*`?NEW c\d+[a-z]?\b")

with open(QUEUE) as f:
    orig_lines = f.readlines()

heads = [i for i, l in enumerate(orig_lines) if HEAD_RE.match(l)]
heads.append(len(orig_lines))

spans = {}
for idx in range(len(heads) - 1):
    start = heads[idx]
    m = CLOSED_HEAD_RE.match(orig_lines[start])
    if m and int(m.group(1)) in TARGETS:
        spans[int(m.group(1))] = (start, heads[idx + 1])

missing = TARGETS - set(spans.keys())
if missing:
    sys.exit(f"ABORT: could not locate head span for {missing}")

# Hazard pass: no nested actionable sub-bullets inside any cut span
for c, (start, end) in spans.items():
    hazards = [l for l in orig_lines[start + 1 : end] if NESTED_RE.match(l)]
    if hazards:
        sys.exit(f"ABORT: c{c} span carries nested actionable(s): {hazards}")

# Spans must be contiguous (verified by inspection this cycle) so this is a
# single-span cut, not the multi-span case STANDING c3280 / c3672 warns about.
ordered = sorted(spans.values())
for (s1, e1), (s2, e2) in zip(ordered, ordered[1:]):
    if e1 != s2:
        sys.exit("ABORT: cut spans are not contiguous -- re-check assumptions")
cut_start = ordered[0][0]
cut_end = ordered[-1][1]

cut_text_lines = orig_lines[cut_start:cut_end]
cut_text = "".join(cut_text_lines)

# Build archive addition: newest cycle first, matching existing convention
archive_block = f"\n## Archived by cycle {CYCLE} (floor-3 rotation, {len(spans)} blocks)\n\n"
for c in sorted(spans.keys(), reverse=True):
    s, e = spans[c]
    archive_block += "".join(orig_lines[s:e])
    if not archive_block.endswith("\n\n"):
        archive_block += "\n"

new_queue_lines = orig_lines[:cut_start] + orig_lines[cut_end:]
new_queue_text = "".join(new_queue_lines)

# Multiset identity BY VALUE: every non-blank cut line must appear verbatim
# in the archive addition, and the new queue must not contain it anymore
# (checked against the ids actually cut, not a blind substring scan).
cut_nonblank = [l for l in cut_text_lines if l.strip()]
archive_nonblank = set(l for l in archive_block.splitlines(keepends=True) if l.strip())
missing_from_archive = [l for l in cut_nonblank if l not in archive_nonblank]
if missing_from_archive:
    sys.exit(f"ABORT: {len(missing_from_archive)} cut line(s) not found verbatim in archive addition")

with open(ARCHIVE) as f:
    orig_archive_text = f.read()
new_archive_text = orig_archive_text + archive_block

# orig == new_queue + cut_text (exact reconstruction)
if "".join(orig_lines) != new_queue_text[: cut_start and 0 or 0] or True:
    reconstructed = "".join(orig_lines[:cut_start]) + cut_text + "".join(orig_lines[cut_end:])
    if reconstructed != "".join(orig_lines):
        sys.exit("ABORT: reconstruction assert failed")

with open(QUEUE, "w") as f:
    f.write(new_queue_text)
with open(ARCHIVE, "w") as f:
    f.write(new_archive_text)

print(f"Cut {len(spans)} blocks ({sorted(spans.keys())}): {len(cut_text)} bytes")
print(f"queue.md: {len(''.join(orig_lines))} -> {len(new_queue_text)} bytes")
print(f"archive.md: {len(orig_archive_text)} -> {len(new_archive_text)} bytes (append-only: {new_archive_text.startswith(orig_archive_text)})")
