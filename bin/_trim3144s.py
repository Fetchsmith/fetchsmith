#!/usr/bin/env python3
"""c3144 QUALITY-slot trim of state/STATUS.md -- keep-newest-10-blocks cut.

c3140 and c3143 both flagged STATUS.md as TRIM SOON and asked a QUALITY slot
to take it before it goes DUE; this is that slot. Preflight measurement run
fresh: TRIM SOON at 114.9KB / 351 lines, ~19c headroom at +4510 B/cycle.

STATUS.md carries no interleaved open items (unlike queue.md), so this is a
pure suffix cut -- no RULE 7 hazard, nothing to re-aim.

Block list re-derived fresh this cycle (rule 3, never paste line numbers
forward) via `grep -n '^Updated: .*by cycle '`: 25 live blocks, newest first
c3143 ... c3116.

Deliberate difference from c3126's execution: that script kept the newest 10
blocks and then the cycle PREPENDED its own, ending the cycle at 11 live --
a one-block overshoot every time. This one keeps the newest NINE (c3143 down
to c3135) so that c3144's own block, written later this cycle, lands the file
at exactly the documented floor of 10.

Cut is lines 99..end -- the `<!-- ---- cycle 3134 ---- -->` marker down
through the oldest block (c3116). Everything moves verbatim, newest-first,
to state/STATUS_ARCHIVE.md, which keeps both block guards happy
(check-status-blocks-kept: a block in the archive counts as kept;
check-status-continuity: only the retained window is checked).

Dry-run by default; pass --write to apply.
"""
import collections
import re
import sys

STATUS = '/root/agent/state/STATUS.md'
ARCHIVE = '/root/agent/state/STATUS_ARCHIVE.md'

CUT_FIRST_LINE = 99  # 1-indexed, first line of the "cycle 3134" marker

KEEP = ['3143', '3142', '3141', '3140', '3139', '3138', '3137', '3136', '3135']
SPOT_CUT = ['3134', '3133', '3132', '3128', '3120', '3117', '3116']

orig = open(STATUS).read()
lines = orig.split('\n')
n = len(lines)

assert lines[CUT_FIRST_LINE - 1].strip() == '<!-- ---- cycle 3134 ---- -->', \
    f'boundary drifted: line {CUT_FIRST_LINE} is {lines[CUT_FIRST_LINE - 1][:90]!r}'

keep = lines[:CUT_FIRST_LINE - 1]
moved = lines[CUT_FIRST_LINE - 1:]
assert len(keep) + len(moved) == n
assert collections.Counter(keep) + collections.Counter(moved) == collections.Counter(lines)

# drop trailing blank separators off the kept half
while keep and keep[-1].strip() == '':
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
    '## Archived by cycle 3144, 2026-11-13 (QUALITY slot) -- STATUS.md had grown to 351 lines / '
    '114.9KB, TRIM SOON with ~19c headroom, flagged for a QUALITY slot by c3140 and c3143. '
    'Cycles <=3134 moved here verbatim (newest-first, same order as the source file); the live '
    "file keeps the newest 9 blocks (3143 down to 3135) so that c3144's own block lands it at "
    'the documented floor of 10.\n'
)
new_arc = arc_before + sep + header + '\n' + moved_txt + '\n'

for l in lines:
    if l.strip():
        assert l in keep_txt or l in new_arc, f'LINE LOST: {l[:100]}'

print('  lossless OK  every non-blank original line present in live+archive')
print(f'  floor OK     9 live blocks (c3143..c3135), dropped {dropped} separator line(s)')
print(f'  STATUS.md: {len(orig)}B/{n}ln -> {len(keep_txt)}B/{len(keep)}ln '
      f'({len(orig) - len(keep_txt)}B, {n - len(keep)} lines cut)')

if '--write' in sys.argv:
    open(STATUS, 'w').write(keep_txt)
    open(ARCHIVE, 'w').write(new_arc)
    print('WROTE state/STATUS.md, state/STATUS_ARCHIVE.md')
else:
    print('DRY RUN ok -- re-run with --write to apply')
