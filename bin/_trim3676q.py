#!/root/agent/venv/bin/python
"""Cycle 3676 floor-3 CLOSED-block rotation on tasks/queue.md.

Keeps the newest 2 CLOSED blocks (c3675, c3674) plus this cycle's own (prepended
separately by the cycle), archiving `CLOSED c3673` verbatim to tasks/queue_archive.md
under a `## Archived by cycle 3676` header. Floor is 3, per the c3672 cadence change
in notes/PLAYBOOK.md.

Method per PLAYBOOK: build both new texts in MEMORY, assert multiset identity of lines
BEFORE any write (the _trim3492q.py lesson), then write, then re-verify from disk.
"""
QUEUE = "/root/agent/tasks/queue.md"
ARCH = "/root/agent/tasks/queue_archive.md"
HEADER = "## Archived by cycle 3676"

orig = open(QUEUE).read()
lines = orig.split("\n")

# locate the CLOSED c3673 block: its head line through the blank line before the next head
start = next(i for i, l in enumerate(lines) if l.startswith("- [x] **CLOSED c3673 --"))
end = start + 1
while end < len(lines) and not lines[end].startswith("- [ ] **") and not lines[end].startswith("- [x] **"):
    end += 1
# `end` is the next block head; the line before it is the separating blank
assert lines[end - 1].strip() == "", repr(lines[end - 1])
cut = lines[start:end - 1]            # block body only, no separating blank
assert cut[0].startswith("- [x] **CLOSED c3673 --")
assert len(cut) == 6, len(cut)

new_lines = lines[:start] + lines[end - 1:]
new_queue = "\n".join(new_lines)

arch_orig = open(ARCH).read()
new_arch = arch_orig.rstrip("\n") + "\n\n" + HEADER + "\n\n" + "\n".join(cut) + "\n"

# losslessness: every original queue line is either still in the queue or in the archive
from collections import Counter
q_before, q_after = Counter(lines), Counter(new_lines)
a_before, a_after = Counter(arch_orig.split("\n")), Counter(new_arch.split("\n"))
moved = q_before - q_after
assert moved == Counter(cut), (moved, cut)
gained = a_after - a_before
assert gained == Counter(cut) + Counter({HEADER: 1}) + Counter({"": gained.get("", 0)}), gained
for l in cut:
    assert l in new_arch, l[:80]

open(QUEUE, "w").write(new_queue)
open(ARCH, "w").write(new_arch)

# independent post-write re-verify against the pre-image
q2, a2 = open(QUEUE).read(), open(ARCH).read()
assert q2 == new_queue and a2 == new_arch
for l in cut:
    assert l not in q2.split("\n"), l[:80]
    assert l in a2.split("\n"), l[:80]
print(f"queue.md {len(orig)}B -> {len(q2)}B ({len(lines)} -> {len(q2.split(chr(10)))} lines); "
      f"archive {len(arch_orig)}B -> {len(a2)}B; moved {len(cut)} line(s) of CLOSED c3673, lossless.")
