#!/root/agent/venv/bin/python
"""Cycle 3692 trim on tasks/queue.md -- ordinary floor-3 rotation only (c3672 cadence,
notes/PLAYBOOK.md). check-doc-size read TRIM DUE at 195.1KB /
~1 cycle of headroom at preflight, 3 CLOSED blocks present (c3691, c3690, c3689);
archiving the oldest (c3689) holds the floor at 3 once this cycle's own CLOSED block is
prepended. No structural pass this cycle (narrow BUILD slot) -- STANDING c3280's
relocation pass is still the owed lever, still named for the next QUALITY slot.

c3692 FIXED A BUG INHERITED FROM _trim3687q.py, which every future clone would have hit:
the post-write verification looped `assert l not in q2` over each cut line, which is
FALSE for boilerplate a CLOSED block shares with its siblings -- it fired here on the
bare `---` horizontal rule, AFTER the write had already landed. c3688 hit the identical
false alarm and fixed it in its own copy; cloning 3687 instead silently reintroduced it.
Replaced with the multiset form (the pre-write `moved == Counter(cut)` assert is the real
losslessness proof anyway): every ORIGINAL line must still be findable in live+archive.
"""
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCH = "/root/agent/tasks/queue_archive.md"
HEADER = "## Archived by cycle 3692"

orig = open(QUEUE).read()
lines = orig.split("\n")


def block(head_prefix, src):
    start = next(i for i, l in enumerate(src) if l.startswith(head_prefix))
    end = start + 1
    while end < len(src) and not src[end].startswith(("- [ ] **", "- [x] **")):
        end += 1
    assert src[end - 1].strip() == "", repr(src[end - 1])
    return start, end


closed_now = [l for l in lines if l.startswith("- [x] **CLOSED c")]
assert len(closed_now) == 3, [l[:30] for l in closed_now]

work = list(lines)
s, e = block("- [x] **CLOSED c3689 --", work)
cut = work[s:e - 1]
work = work[:s] + work[e - 1:]
assert cut[0].startswith("- [x] **CLOSED c3689 --")
moved = Counter(lines) - Counter(work)
assert moved == Counter(cut), moved

new_queue = "\n".join(work)

arch_orig = open(ARCH).read()
new_arch = (arch_orig.rstrip("\n") + "\n\n" + HEADER + "\n\n" + "\n".join(cut) + "\n")

for l in cut:
    assert l in new_arch, l[:80]

open(QUEUE, "w").write(new_queue)
open(ARCH, "w").write(new_arch)

q2, a2 = open(QUEUE).read(), open(ARCH).read()
assert q2 == new_queue and a2 == new_arch
# Multiset, not per-line membership: see the docstring. Every original line must survive
# somewhere in live+archive, and the cut block's own lines must all be in the archive.
assert not (Counter(lines) - Counter(q2.split("\n")) - Counter(a2.split("\n"))), "lossy"
for l in cut:
    assert l in a2.split("\n"), l[:80]
assert len([l for l in q2.split("\n") if l.startswith("- [x] **CLOSED c")]) == 2
print(f"queue.md {len(orig)}B/{len(lines)}ln -> {len(q2)}B/{len(q2.split(chr(10)))}ln; "
      f"archive {len(arch_orig)}B -> {len(a2)}B; rotated CLOSED c3689 ({len(cut)} lines), lossless.")
