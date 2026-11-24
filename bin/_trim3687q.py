#!/root/agent/venv/bin/python
"""Cycle 3687 trim on tasks/queue.md -- ordinary floor-3 rotation only (c3672 cadence,
notes/PLAYBOOK.md). File measured 200,082B at preflight, 3 CLOSED blocks present
(c3686, c3685, c3684); archiving the oldest (c3684, 3,811B) holds the floor at 3 once
this cycle's own CLOSED block is prepended. No structural pass this cycle -- the single
rotation left only ~2 cycles of headroom (191.7KB after this script, before this cycle's
own block landed) -- next QUALITY slot should re-measure fresh and do a structural
relocation pass if still tight (STANDING c3280 names FOLD-IN REGISTER and NEW c3372 as
the two live candidates, unchanged since c3684).
"""
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCH = "/root/agent/tasks/queue_archive.md"
HEADER = "## Archived by cycle 3687"

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
s, e = block("- [x] **CLOSED c3684 --", work)
cut = work[s:e - 1]
work = work[:s] + work[e - 1:]
assert cut[0].startswith("- [x] **CLOSED c3684 --")
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
for l in cut:
    if l.strip():
        assert l not in q2.split("\n"), l[:80]
    assert l in a2.split("\n"), l[:80]
assert len([l for l in q2.split("\n") if l.startswith("- [x] **CLOSED c")]) == 2
print(f"queue.md {len(orig)}B/{len(lines)}ln -> {len(q2)}B/{len(q2.split(chr(10)))}ln; "
      f"archive {len(arch_orig)}B -> {len(a2)}B; rotated CLOSED c3684 ({len(cut)} lines), lossless.")
