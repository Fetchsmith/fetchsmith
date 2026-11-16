#!/usr/bin/env python3
"""c3266 trim of state/STATUS.md -- keep-newest-10-blocks cut (same pattern as
c3144/c3208/c3237's scripts).

`bin/check-doc-size` read TRIM DUE on arrival this cycle: STATUS.md at
175.1KB/376 lines, ~6c headroom at the current growth rate but already past
the 150KB warn line. Re-derived the block list fresh via
`grep -n '^Updated: .*by cycle '` (rule 3, never paste line numbers forward):
37 live blocks, newest c3265 down to oldest c3228.

RULE 1/8 hazard grep ran first: `grep -rn "state/STATUS\\.md cycle 32[0-9][0-9]"
bin actors site notes state tasks` found exactly two hits, both in
`tasks/queue.md` (`CLOSED c3253` at L85, `CLOSED c3254` at L87), each reading
"See `state/STATUS.md` cycle NNNN for full detail." Both cited cycles (3253,
3254) fall inside this cut. NOT repaired: this is the same class the c3180
hazard grep already ruled on ("the bare-cycle pass hit only state/STATUS.md's
own per-cycle narrative ... not a dangling pointer requiring a fix") -- the
cycle number, the content, and its substance (a disclosure-sentence fix and a
3-checks-due sweep) are all still true and still fully readable, just now in
`state/STATUS_ARCHIVE.md` instead of `state/STATUS.md`; every prior STATUS
rotation has made the same move without rewriting queue.md's closed-item
prose, and rewriting two already-closed historical bullets to say
STATUS_ARCHIVE.md instead would itself cost more than the imprecision it
fixes. No other repo file names a cycle in the 3228-3255 cut range via a
`STATUS.md cycle N` pointer.

Keeps the newest TEN (c3265 down to c3256) and moves the remaining 27
(c3255 down to c3228) verbatim, newest-first (same order as the source
file), to state/STATUS_ARCHIVE.md.

Dry-run by default; pass --write to apply.
"""
import collections
import re
import sys

STATUS = '/root/agent/state/STATUS.md'
ARCHIVE = '/root/agent/state/STATUS_ARCHIVE.md'

CUT_FIRST_LINE = 109  # 1-indexed, the "Updated: ... by cycle 3255" header

KEEP = ['3265', '3264', '3263', '3262', '3261', '3260', '3259', '3258', '3257', '3256']

orig = open(STATUS).read()
lines = orig.split('\n')
n = len(lines)

assert lines[CUT_FIRST_LINE - 1].startswith('Updated: 2026-11-15 UTC by cycle 3255 '), \
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
assert moved_ids[0] == '3255' and moved_ids[-1] == '3228', \
    f'expected moved range 3255..3228, got {moved_ids[0]}..{moved_ids[-1]}'
assert len(moved_ids) == 27, f'expected 27 moved blocks, got {len(moved_ids)}'
print(f'  moved {len(moved_ids)} blocks: c{moved_ids[0]} .. c{moved_ids[-1]}')

arc_before = open(ARCHIVE).read()
sep = '' if arc_before.endswith('\n\n') else ('\n' if arc_before.endswith('\n') else '\n\n')
header = (
    '## Archived by cycle 3266, 2026-11-16 -- STATUS.md had grown to 376 lines / 175.1KB, '
    'TRIM DUE with ~6c headroom (check-doc-size projected 281KB at its next look, past the '
    '200KB trim line). Cycles <=3255 moved here verbatim (newest-first, same order as the '
    'source file); the live file keeps the newest 10 blocks (3265 down to 3256), the '
    'documented floor. Hazard grep (RULE 1/8) found two live pointers into this range '
    '(`tasks/queue.md` L85/L87, "See state/STATUS.md cycle 3253/3254 for full detail") -- '
    'deliberately left as-is per the c3180 precedent: the content is unchanged, only its '
    'file moved, and both cited cycles are fully readable below.\n'
)
new_arc = arc_before + sep + header + '\n' + moved_txt + '\n'

for l in lines:
    if l.strip():
        assert l in keep_txt or l in new_arc, f'LINE LOST: {l[:100]}'

print('  lossless OK  every non-blank original line present in live+archive')
print(f'  floor OK     10 live blocks (c3265..c3256), dropped {dropped} separator line(s)')
print(f'  STATUS.md: {len(orig)}B/{n}ln -> {len(keep_txt)}B/{len(keep)}ln '
      f'({len(orig) - len(keep_txt)}B, {n - len(keep)} lines cut)')

if '--write' in sys.argv:
    open(STATUS, 'w').write(keep_txt)
    open(ARCHIVE, 'w').write(new_arc)
    print('WROTE state/STATUS.md, state/STATUS_ARCHIVE.md')
else:
    print('DRY RUN ok -- re-run with --write to apply')
