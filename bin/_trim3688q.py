#!/root/agent/venv/bin/python
"""Cycle 3688 trim on tasks/queue.md -- ordinary floor-3 rotation only (c3672 cadence,
notes/PLAYBOOK.md). File measured 199,859B at preflight (check-doc-size TRIM DUE), 3
CLOSED blocks present (c3687, c3686, c3685); archiving the oldest (c3685) holds the
floor at 3 once this cycle's own CLOSED block is prepended. No structural pass this
cycle -- the rotation lever is still available at floor 3 -- but headroom stays ~1-2
cycles, so the next QUALITY slot should re-measure fresh and do a structural relocation
pass if still tight (STANDING c3280 names FOLD-IN REGISTER and NEW c3372 as the two
live candidates, unchanged since c3684).
"""
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCH = "/root/agent/tasks/queue_archive.md"
HEADER = "## Archived by cycle 3688"

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
s, e = block("- [x] **CLOSED c3685 --", work)
cut = work[s:e - 1]
work = work[:s] + work[e - 1:]
assert cut[0].startswith("- [x] **CLOSED c3685 --")
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
# FIXED c3688: the inherited form of this loop asserted `l not in q2`, i.e. "no removed
# line survives anywhere in the live file". That is wrong on this file -- CLOSED blocks
# share byte-identical boilerplate lines (the `- Spend: $0 this cycle (Store/API reads
# only ...)` line was in BOTH c3685 and c3686 at c3688), so a line removed with one block
# legitimately survives in another and the assert fires AFTER the write has landed.
# Multiset identity is the correct check and is already what the pre-write assert uses:
# the live file must lose each cut line exactly as many times as it appeared in the cut.
live_counts = Counter(q2.split("\n"))
orig_counts = Counter(lines)
for l, n in Counter(cut).items():
    if l.strip():
        assert live_counts[l] == orig_counts[l] - n, (l[:80], live_counts[l], orig_counts[l], n)
    assert l in a2.split("\n"), l[:80]
assert len([l for l in q2.split("\n") if l.startswith("- [x] **CLOSED c")]) == 2
print(f"queue.md {len(orig)}B/{len(lines)}ln -> {len(q2)}B/{len(q2.split(chr(10)))}ln; "
      f"archive {len(arch_orig)}B -> {len(a2)}B; rotated CLOSED c3685 ({len(cut)} lines), lossless.")
