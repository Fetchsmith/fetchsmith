#!/usr/bin/env python3
"""c3237 trim of state/STATUS.md -- keep-newest-10-blocks cut (same pattern as
c3144/c3208's scripts).

`bin/check-doc-size` read TRIM DUE on arrival this cycle: STATUS.md at
165.5KB/425 lines before this cycle's own block was prepended. Re-derived
the block list fresh via `grep -n '^Updated: .*by cycle '` (rule 3, never
paste line numbers forward): 39 live blocks after c3237's own block was
prepended, newest c3237 down to oldest c3199.

Keeps the newest TEN (c3237 down to c3228) and moves the remaining 29
(c3227 down to c3199) verbatim, newest-first (same order as the source
file), to state/STATUS_ARCHIVE.md.

Dry-run by default; pass --write to apply.
"""
import collections
import re
import sys

STATUS = '/root/agent/state/STATUS.md'
ARCHIVE = '/root/agent/state/STATUS_ARCHIVE.md'

CUT_FIRST_LINE = 102  # 1-indexed, the "Updated: ... by cycle 3227" header

KEEP = ['3237', '3236', '3235', '3234', '3233', '3232', '3231', '3230', '3229', '3228']

orig = open(STATUS).read()
lines = orig.split('\n')
n = len(lines)

assert lines[CUT_FIRST_LINE - 1].startswith('Updated: 2026-11-15 UTC by cycle 3227 '), \
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

HDR = re.compile(r'^Updated: .* by cycle (\d+) ')
kept_ids = [m.group(1) for m in (HDR.match(l) for l in keep) if m]
moved_ids = [m.group(1) for m in (HDR.match(l) for l in moved) if m]
assert kept_ids == KEEP, f'expected live blocks {KEEP}, got {kept_ids}'
assert moved_ids[0] == '3227' and moved_ids[-1] == '3199', \
    f'expected moved range 3227..3199, got {moved_ids[0]}..{moved_ids[-1]}'
assert len(moved_ids) == 29, f'expected 29 moved blocks, got {len(moved_ids)}'
print(f'  moved {len(moved_ids)} blocks: c{moved_ids[0]} .. c{moved_ids[-1]}')

arc_before = open(ARCHIVE).read()
sep = '' if arc_before.endswith('\n\n') else ('\n' if arc_before.endswith('\n') else '\n\n')
header = (
    '## Archived by cycle 3237, 2026-11-15 -- STATUS.md had grown to 432 lines (after this '
    'cycle prepended its own block) / 165.5KB pre-prepend, TRIM DUE with ~8c headroom '
    '(check-doc-size projected 271KB at its next look, past the 200KB trim line). Cycles '
    '<=3227 moved here verbatim (newest-first, same order as the source file); the live file '
    'keeps the newest 10 blocks (3237 down to 3228), the documented floor.\n'
)
new_arc = arc_before + sep + header + '\n' + moved_txt + '\n'

for l in lines:
    if l.strip():
        assert l in keep_txt or l in new_arc, f'LINE LOST: {l[:100]}'

print('  lossless OK  every non-blank original line present in live+archive')
print(f'  floor OK     10 live blocks (c3237..c3228), dropped {dropped} separator line(s)')
print(f'  STATUS.md: {len(orig)}B/{n}ln -> {len(keep_txt)}B/{len(keep)}ln '
      f'({len(orig) - len(keep_txt)}B, {n - len(keep)} lines cut)')

if '--write' in sys.argv:
    open(STATUS, 'w').write(keep_txt)
    open(ARCHIVE, 'w').write(new_arc)
    print('WROTE state/STATUS.md, state/STATUS_ARCHIVE.md')
else:
    print('DRY RUN ok -- re-run with --write to apply')
