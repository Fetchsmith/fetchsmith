#!/root/agent/venv/bin/python
"""Cycle 3751: tasks/queue.md floor-3 rotation.

Live CLOSED rotation-pool blocks before this cycle's own block was added: 3
(`c3749`/`c3748`/`c3747`; `CLOSED c3544` is a separate one-off, not pool).
This cycle's own block pushes the pool to 4, floor is 3 (newest 2 + this
cycle's own), so the correct cut is the oldest ONE, `CLOSED c3747`.
Hand-checked `CLOSED c3747`'s span for nested `NEW cNNNNa` sub-bullets
(dashed, dash-less and backticked forms, the c3748 regex): zero found, only
harmless cross-reference mentions inside prose -- no promotion step needed.

Cloned from `bin/_trim3749q.py` BY NAME, per the standing doc-trim convention.
"""
import re

Q = "/root/agent/tasks/queue.md"
A = "/root/agent/tasks/queue_archive.md"

with open(Q) as f:
    lines = f.readlines()

start = sep = None
for i, l in enumerate(lines):
    if l.startswith("- [x] **CLOSED c3747"):
        start = i
    elif start is not None and sep is None and lines[i].strip() == "---":
        sep = i
        break
assert start is not None and sep is not None, "block boundaries not found"
block = lines[start:sep]  # includes trailing blank line before '---'
removed_span = lines[start:sep + 1]  # include the '---' line itself for removal

cut_text = "".join(block)
multiset_before = sorted(l for l in block if l.strip())

with open(A, "a") as f:
    f.write("\n## Archived by cycle 3751 (CLOSED c3747, floor-3 rotation; no nested\n")
    f.write("## actionable items found in the span, so nothing needed promotion)\n\n")
    f.write(cut_text)
    f.write("\n---\n")

new_lines = lines[:start] + lines[sep + 1:]
with open(Q, "w") as f:
    f.writelines(new_lines)

# lossless re-verify
with open(Q) as f:
    after = f.readlines()
with open(A) as f:
    arch_after = f.readlines()

multiset_after_q_missing = [l for l in multiset_before if l not in after]
multiset_after_a_present = [l for l in multiset_before if l in arch_after]
print("lines in cut block:", len(block))
print("non-blank lines in cut block:", len(multiset_before))
print("still-present-in-queue (should be 0 ideally, some generic lines may legitimately repeat):",
      len(multiset_before) - len(multiset_after_q_missing))
print("found verbatim in archive:", len(multiset_after_a_present), "/", len(multiset_before))
assert len(multiset_after_a_present) == len(multiset_before), "LOSS DETECTED: not all lines found in archive"
print("OK -- lossless")
