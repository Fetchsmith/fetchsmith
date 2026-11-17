#!/usr/bin/env python3
"""c3347 trim of state/STATUS.md -- keep-newest-9-blocks cut (clone of
bin/_trim3296s.py, same pattern as c3144/c3208/c3237/c3266/c3296).

`bin/check-doc-size` read TRIM DUE on arrival: STATUS.md at 254.2KB/592 lines,
~-12 cycles of headroom (badly past the ~3-cycle trigger every prior trim used,
and past both the 200KB trim line and the 256KB Read cap). This is the single
biggest offender this cycle (queue.md is also TRIM DUE but at only ~-1 cycle of
headroom, the lesser gap) so it is the main task.

Fresh block census (`grep -n '^Updated:' state/STATUS.md`): 60 live blocks,
strictly chronological descending c3346..c3287, no preamble, no interleaved
live items -- same shape as every prior STATUS.md trim (c3296, c3266, ...).
Single contiguous-suffix cut, not a multi-range gather.

Hazard grep (rule: never skip): a `STATUS.md` sweep across bin/actors/site/
notes/state/tasks turned up only generic infra references (bin/check-doc-size,
bin/check-status-continuity, bin/_recover2136.py, bin/store-rank comments) that
describe the mechanism, not a pointer into a specific cut cycle; a second pass
for any live-file line naming both "STATUS" and a cycle number in the cut
range (c3287-3337) found only notes/LEARNINGS.md's own narrative account of
the c3296 trim (self-referential, describing that past trim, not a pointer
INTO the content being cut now) and tasks/queue.md's own `CLOSED cNNNN`
report headers (self-referential to queue.md, not STATUS.md). No "See
STATUS.md cycle N for detail" dangling pointer found anywhere live.

Keeps the newest NINE (c3346 down to c3338) so that cycle 3347's own block,
prepended after this script runs, lands the live file at exactly 10 -- the
documented floor. Moves the remaining 51 blocks (c3337 down to c3287)
verbatim, newest-first, to state/STATUS_ARCHIVE.md.

Dry-run by default; pass --write to apply.
"""
import collections
import re
import sys

STATUS = '/root/agent/state/STATUS.md'
ARCHIVE = '/root/agent/state/STATUS_ARCHIVE.md'

CUT_FIRST_LINE = 99  # 1-indexed, the "Updated: ... by cycle 3337" header

KEEP = ['3346', '3345', '3344', '3343', '3342', '3341', '3340', '3339', '3338']

orig = open(STATUS).read()
lines = orig.split('\n')
n = len(lines)

assert lines[CUT_FIRST_LINE - 1].startswith('Updated: 2026-11-17 UTC by cycle 3337 '), \
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
assert moved_ids[0] == '3337' and moved_ids[-1] == '3287', \
    f'expected moved range 3337..3287, got {moved_ids[0]}..{moved_ids[-1]}'
assert len(moved_ids) == 51, f'expected 51 moved blocks, got {len(moved_ids)}'
assert len(kept_ids) + len(moved_ids) == 60, 'block count drifted from the fresh census (60)'
print(f'  moved {len(moved_ids)} blocks: c{moved_ids[0]} .. c{moved_ids[-1]}')

arc_before = open(ARCHIVE).read()
sep = '' if arc_before.endswith('\n\n') else ('\n' if arc_before.endswith('\n') else '\n\n')
header = (
    '## Archived by cycle 3347, 2026-11-17 -- STATUS.md had grown to 592 lines / 254.2KB, '
    'TRIM DUE with ~-12 cycles of headroom (badly past the ~3-cycle trigger every prior '
    'trim used, and past both the 200KB trim line and the 256KB Read cap); this was the '
    'bigger of the two TRIM DUE files this cycle (queue.md was only ~-1 cycle) so it was '
    'taken as the main task. Cycles <=3337 moved here verbatim (newest-first, same order '
    'as the source file); the live file keeps the newest NINE blocks (3346 down to 3338) '
    'so that c3347\'s own block lands it at exactly 10, the documented floor. Hazard grep '
    'clean: the live-files-only `STATUS.md` sweep returned only generic infra references '
    '(check-doc-size, check-status-continuity, _recover2136.py) describing the trim '
    'mechanism itself, and a by-cycle-number pass for the c3287-c3337 range found only '
    'self-referential narrative in notes/LEARNINGS.md (describing the PAST c3296 trim) '
    'and tasks/queue.md\'s own CLOSED headers -- no dangling "see STATUS.md cycle N" '
    'pointer anywhere live.\n'
)
new_arc = arc_before + sep + header + '\n' + moved_txt + '\n'

for l in lines:
    if l.strip():
        assert l in keep_txt or l in new_arc, f'LINE LOST: {l[:100]}'

print('  lossless OK  every non-blank original line present in live+archive')
print(f'  floor OK     9 live blocks (c3346..c3338) + c3347 = 10, dropped {dropped} separator line(s)')
print(f'  STATUS.md: {len(orig)}B/{n}ln -> {len(keep_txt)}B/{len(keep)}ln '
      f'({len(orig) - len(keep_txt)}B, {n - len(keep)} lines cut)')

if '--write' in sys.argv:
    open(STATUS, 'w').write(keep_txt)
    open(ARCHIVE, 'w').write(new_arc)
    print('WROTE state/STATUS.md, state/STATUS_ARCHIVE.md')
else:
    print('DRY RUN ok -- re-run with --write to apply')
