#!/usr/bin/env python3
"""One-shot queue.md trim for cycle 3193 (Regular slot, 3193 % 3 == 1).

`check-doc-size` at preflight reported tasks/queue.md TRIM DUE at 186.6KB/1234ln,
~3 cycles of headroom at +5440 B/cycle, projected 314KB at the next look -- past
both the 200KB trim line and the 256KB Read cap. 9 live CLOSED blocks counted
fresh against the floor of 5 (c3188's rotation left 5 at c3188; c3189-c3192 each
prepended one with zero outbound in between). Pure rotation, same shape as
c3164/c3172/c3180/c3188: archive the 4 oldest (c3187, c3186, c3185, c3184) down
to the floor of 5 (c3192..c3188).

RULE 7: one contiguous range. c3184's block ends immediately before `NEW c3188`
(no live open item interleaved in the span).

Dry-run by default; pass --write to apply.
"""
import sys

QUEUE = '/root/agent/tasks/queue.md'
ARCHIVE = '/root/agent/tasks/queue_archive.md'

with open(QUEUE) as f:
    lines = f.readlines()

assert lines[74].startswith('- [ ] **CLOSED c3187'), lines[74]
assert lines[88].startswith('- [ ] **CLOSED c3186'), lines[88]
assert lines[98].startswith('- [ ] **CLOSED c3185'), lines[98]
assert lines[112].startswith('- [ ] **CLOSED c3184'), lines[112]
assert lines[126].startswith('- [ ] **NEW c3188'), lines[126]
assert lines[125] == '\n', repr(lines[125])
assert lines[73] == '\n', repr(lines[73])

CUT = lines[74:126]   # lines 75..126 1-indexed
KEEP_BEFORE = lines[:74]
KEEP_AFTER = lines[126:]

HEADER = (
    "## Archived by cycle 3193 trim (Regular slot, 3193 % 3 == 1; `check-doc-size` at "
    "preflight reported tasks/queue.md **TRIM DUE** at 186.6KB/1234ln with only ~3 cycles "
    "of headroom at +5440 B/cycle, projected **314KB at the next look** -- past both the "
    "200KB trim line and the 256KB Read cap. NINE live CLOSED blocks counted fresh against "
    "the floor of 5 (c3188's rotation left 5; c3189-c3192 each prepended one, zero outbound "
    "in between) -- `CLOSED c3187`, `CLOSED c3186`, `CLOSED c3185`, `CLOSED c3184` archived "
    "verbatim, in original file order, as ONE contiguous range: no live open item is "
    "interleaved in the span (`NEW c3188` sits immediately after it and stays live). This is "
    "a pure rotation only -- the RULE 4 retirement pass `NEW c3188` itself asked for is still "
    "not attempted; see that item, now renumbered among the survivors, for candidates.\n"
)

new_queue = KEEP_BEFORE + KEEP_AFTER

with open(ARCHIVE) as f:
    old_archive = f.read()
new_archive = HEADER + '\n' + ''.join(CUT) + '\n' + old_archive

# losslessness: every non-blank line of CUT must appear verbatim in new_archive
missing = [l for l in CUT if l.strip() and l not in new_archive]
assert not missing, f"LOST {len(missing)} lines: {missing[:3]}"

# the queue file must only have lost exactly the CUT lines
assert len(new_queue) == len(lines) - len(CUT)
assert new_queue == KEEP_BEFORE + KEEP_AFTER

print(f"queue.md: {len(lines)} -> {len(new_queue)} lines")
print(f"cutting {len(CUT)} lines ({sum(len(l) for l in CUT)} bytes)")

if '--write' in sys.argv:
    with open(QUEUE, 'w') as f:
        f.writelines(new_queue)
    with open(ARCHIVE, 'w') as f:
        f.write(new_archive)
    print("WRITTEN")
else:
    print("DRY RUN -- pass --write to apply")
