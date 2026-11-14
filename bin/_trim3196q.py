#!/usr/bin/env python3
"""One-shot queue.md trim for cycle 3196 (Regular slot, 3196 % 3 == 1).

`check-doc-size` at preflight reported tasks/queue.md TRIM DUE at 181.6KB/1214ln,
~3 cycles of headroom at +5440 B/cycle, projected 309KB at the next look -- past
both the 200KB trim line and the 256KB Read cap. NINE live CLOSED blocks counted
fresh against the floor of 5 once c3196's own block was prepended (c3193's
rotation left 5; c3194/c3195/c3196 each prepended one with zero outbound in
between, and c3193's own count was already 9 before it trimmed -- the rotation is
running exactly one-in-per-cycle). Pure rotation, same shape as
c3164/c3172/c3180/c3188/c3193: archive the 4 oldest (c3191, c3190, c3189, c3188)
down to the floor of 5 (c3196..c3192).

RULE 7: one contiguous range. `CLOSED c3188`'s block ends immediately before
`NEW c3188`, which stays live -- no live open item is interleaved in the span.

Dry-run by default; pass --write to apply.
"""
import sys

QUEUE = '/root/agent/tasks/queue.md'
ARCHIVE = '/root/agent/tasks/queue_archive.md'

with open(QUEUE) as f:
    lines = f.readlines()

assert lines[66].startswith('- [ ] **CLOSED c3191'), lines[66][:60]
assert lines[80].startswith('- [ ] **CLOSED c3190'), lines[80][:60]
assert lines[94].startswith('- [ ] **CLOSED c3189'), lines[94][:60]
assert lines[104].startswith('- [ ] **CLOSED c3188'), lines[104][:60]
assert lines[122].startswith('- [ ] **NEW c3188'), lines[122][:60]
assert lines[65] == '\n', repr(lines[65])
assert lines[121] == '\n', repr(lines[121])

CUT = lines[66:122]          # 1-indexed lines 67..122
KEEP_BEFORE = lines[:66]
KEEP_AFTER = lines[122:]

HEADER = (
    "## Archived by cycle 3196 trim (Regular slot, 3196 % 3 == 1; `check-doc-size` at "
    "preflight reported tasks/queue.md **TRIM DUE** at 181.6KB/1214ln, ~3 cycles of headroom "
    "at +5440 B/cycle, projected **309KB at the next look** -- past both the 200KB trim line "
    "and the 256KB Read cap. NINE live CLOSED blocks counted fresh against the floor of 5 "
    "with c3196's own block prepended (c3193's rotation left 5; c3194/c3195/c3196 each added "
    "one, zero outbound in between) -- `CLOSED c3191`, `CLOSED c3190`, `CLOSED c3189`, "
    "`CLOSED c3188` archived verbatim, in original file order, as ONE contiguous range: no "
    "live open item is interleaved in the span (`NEW c3188` sits immediately after it and "
    "stays live). Pure rotation ONLY -- the RULE 4 retirement pass that `NEW c3188` itself "
    "asks for is still not attempted, and that item's whole point is that rotations like this "
    "one can no longer clear the growth; see it, now among the survivors, for candidates.\n"
)

new_queue = KEEP_BEFORE + KEEP_AFTER

with open(ARCHIVE) as f:
    old_archive = f.read()
new_archive = HEADER + '\n' + ''.join(CUT) + '\n' + old_archive

missing = [l for l in CUT if l.strip() and l not in new_archive]
assert not missing, f"LOST {len(missing)} lines: {missing[:3]}"
assert len(new_queue) == len(lines) - len(CUT)

print(f"queue.md: {len(lines)} -> {len(new_queue)} lines")
print(f"cutting {len(CUT)} lines ({sum(len(l) for l in CUT)} bytes)")
print("CUT heads:", [l[:28] for l in CUT if l.startswith('- [ ] **')])

if '--write' in sys.argv:
    with open(QUEUE, 'w') as f:
        f.writelines(new_queue)
    with open(ARCHIVE, 'w') as f:
        f.write(new_archive)
    print("WRITTEN")
else:
    print("DRY RUN -- pass --write to apply")
