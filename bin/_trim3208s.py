#!/usr/bin/env python3
"""c3208 trim of state/STATUS.md -- keep-newest-10-blocks cut.

`bin/check-doc-size` read TRIM DUE on arrival this cycle: STATUS.md at
156.8KB / 433 lines, ~10 cycles of headroom at +4510 B/cycle (projected
262KB at the check's next look, i.e. over the 200KB trim line and near the
256KB Read cap). c3144's script is the template; the differences are noted
below.

STATUS.md carries no interleaved open items (unlike queue.md), so this is a
pure suffix cut -- no RULE 7 hazard, nothing to re-aim.

Block list re-derived fresh this cycle (rule 3, never paste line numbers
forward) via `grep -n '^Updated: .*by cycle '`: 37 live blocks, newest first
c3208 ... c3171.

Difference from c3144's execution: c3208's own block was PREPENDED before
this trim ran, so this script keeps the newest TEN (c3208 down to c3199) and
the cycle ends at exactly the documented floor of 10 -- no overshoot and no
undershoot. Also, this file currently has no `<!-- ---- cycle N ---- -->`
markers, so the boundary is asserted on the c3198 `Updated:` header itself
plus the `---` separator that precedes it.

Everything cut moves verbatim, newest-first, to state/STATUS_ARCHIVE.md,
which keeps both block guards happy (check-status-blocks-kept: a block in
the archive counts as kept; check-status-continuity: only the retained
window is checked).

Dry-run by default; pass --write to apply.
"""
import collections
import re
import sys

STATUS = '/root/agent/state/STATUS.md'
ARCHIVE = '/root/agent/state/STATUS_ARCHIVE.md'

CUT_FIRST_LINE = 121  # 1-indexed, the "Updated: ... by cycle 3198" header

KEEP = ['3208', '3207', '3206', '3205', '3204', '3203', '3202', '3201', '3200', '3199']
SPOT_CUT = ['3198', '3197', '3196', '3190', '3180', '3175', '3171']

orig = open(STATUS).read()
lines = orig.split('\n')
n = len(lines)

assert lines[CUT_FIRST_LINE - 1].startswith('Updated: 2026-11-14 UTC by cycle 3198 '), \
    f'boundary drifted: line {CUT_FIRST_LINE} is {lines[CUT_FIRST_LINE - 1][:90]!r}'

keep = lines[:CUT_FIRST_LINE - 1]
moved = lines[CUT_FIRST_LINE - 1:]
assert len(keep) + len(moved) == n
assert collections.Counter(keep) + collections.Counter(moved) == collections.Counter(lines)

# drop the trailing separator ('---' + blanks) off the kept half
while keep and keep[-1].strip() in ('', '---'):
    keep.pop()
dropped = (CUT_FIRST_LINE - 1) - len(keep)
assert dropped <= 3, f'dropped {dropped} separator lines, expected <=3'

keep_txt = '\n'.join(keep) + '\n'
moved_txt = '\n'.join(moved)

# headers matched ANCHORED to line start, the same way check-status-continuity does it
HDR = re.compile(r'^Updated: .* by cycle (\d+) ')
kept_ids = [m.group(1) for m in (HDR.match(l) for l in keep) if m]
moved_ids = [m.group(1) for m in (HDR.match(l) for l in moved) if m]
assert kept_ids == KEEP, f'expected live blocks {KEEP}, got {kept_ids}'
for c in SPOT_CUT:
    assert c not in kept_ids, f'should have been cut but is still live: cycle {c}'
    assert c in moved_ids, f'MOVED BLOCK MISSING: cycle {c}'
print(f'  moved {len(moved_ids)} blocks: c{moved_ids[0]} .. c{moved_ids[-1]}')

arc_before = open(ARCHIVE).read()
sep = '' if arc_before.endswith('\n\n') else ('\n' if arc_before.endswith('\n') else '\n\n')
header = (
    '## Archived by cycle 3208, 2026-11-14 -- STATUS.md had grown to 433 lines / 156.8KB, '
    'TRIM DUE with ~10c headroom (check-doc-size projected 262KB at its next look, past the '
    '200KB trim line and near the 256KB Read cap). Cycles <=3198 moved here verbatim '
    "(newest-first, same order as the source file); the live file keeps the newest 10 blocks "
    '(3208 down to 3199), the documented floor, because c3208 prepended its own block before '
    'this trim ran.\n'
)
new_arc = arc_before + sep + header + '\n' + moved_txt + '\n'

for l in lines:
    if l.strip():
        assert l in keep_txt or l in new_arc, f'LINE LOST: {l[:100]}'

print('  lossless OK  every non-blank original line present in live+archive')
print(f'  floor OK     10 live blocks (c3208..c3199), dropped {dropped} separator line(s)')
print(f'  STATUS.md: {len(orig)}B/{n}ln -> {len(keep_txt)}B/{len(keep)}ln '
      f'({len(orig) - len(keep_txt)}B, {n - len(keep)} lines cut)')

if '--write' in sys.argv:
    open(STATUS, 'w').write(keep_txt)
    open(ARCHIVE, 'w').write(new_arc)
    print('WROTE state/STATUS.md, state/STATUS_ARCHIVE.md')
else:
    print('DRY RUN ok -- re-run with --write to apply')
