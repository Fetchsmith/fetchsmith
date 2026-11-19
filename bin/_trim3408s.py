#!/usr/bin/env python3
"""c3408 trim of state/STATUS.md -- keep-newest-9-blocks cut (clone of
bin/_trim3347s.py, same pattern as c3144/c3208/c3237/c3266/c3296/c3347/c3378).

WHY NOW: `bin/check-doc-size` on arrival read **TRIM DUE: state/STATUS.md
183.8KB / 382 lines, ~4 cycles of headroom at +4510 B/cycle (proj. 290KB at
the next 24c look)**. `STANDING c3296` in tasks/queue.md predicted the re-trim
window as **c3382-c3392 -- that window has PASSED unacted-on**, and that item's
own capitalised lesson (earned the hard way at c3347, and again at c3348 on
queue.md) is: IF THE PREDICTED WINDOW PASSES WITHOUT A TRIM, TREAT IT AS
OVERDUE IMMEDIATELY. So this is taken as the QUALITY-slot main task (3408 % 3
== 0) even though 4c is marginally above the ~3-cycle trigger band.
queue.md is also TRIM DUE but at ~5 cycles of headroom (c3405 trimmed it to
174.6KB only 3 cycles ago) -- the lesser gap, left alone per the c2224
one-file-per-cycle rule.

FRESH block census (`grep -n '^Updated:' state/STATUS.md`, not forwarded from
any prior cycle): **40 live blocks, strictly chronological descending
c3407..c3368**, no preamble (first block is line 1), no interleaved live items.
Single contiguous-suffix cut, not a multi-range gather.

HAZARD GREP, all three passes (rule: never skip pass (c)):
 (a) live-files `STATUS.md` sweep across bin/actors/site/notes/state/tasks/
     worker: only generic infra references that describe the trim/continuity
     MECHANISM (bin/check-doc-size, bin/check-status-blocks-kept,
     bin/check-status-continuity, bin/store-rank, bin/traffic, bin/apify-spend)
     plus ~30 historical one-shot `_trim*.py`/`_rec*.py` scripts that narrate
     their OWN past trims. No pointer into the span being cut.
 (b) by-cycle-number pass -- every live line naming both "STATUS" and a cycle
     in the cut range c3368..c3398 (39 lines): all either self-referential
     narrative (notes/LEARNINGS.md:20 describes the PAST c3387 ordering
     incident), check-ledger notes self-contained in state/fleet_checks.json,
     one-shot scripts, or lines inside STATUS.md itself (pass (c) below).
     The durable-home-phrased pointers that exist live name c3404 (KEPT),
     c3337, c3008, c2364, c2357 -- **none in the cut range**, so this cut
     creates NO new dangling pointer. (The c3337/c3008/c2364/c2357 ones are
     already-stale PRE-EXISTING pointers into STATUS_ARCHIVE.md, filed as a
     finding by c3408 rather than silently rewritten here.)
 (c) intra-file pass -- kept lines 1-70 referencing a cut-range cycle in
     durable-home phrasing: exactly 2 (L7, L9), both self-contained. L7 is
     c3405's own note that "STATUS.md already carries each archived cycle's
     own full narrative, so references ... are self-contained, not dangling
     pointers"; L9 is c3405's ruling that queue.md's `CLOSED cNNNN` report
     blocks retire BECAUSE STATUS.md keeps the full narrative "under its own
     trim cadence" -- which is exactly this cut, moving it verbatim to the
     archive. Neither breaks.

Keeps the newest NINE (c3407 down to c3399) so that cycle 3408's own block,
prepended after this script runs, lands the live file at exactly 10 -- the
documented floor (c3144's reasoning; keeping 10 and ending at 11 also works
but wastes a block of headroom). Moves the remaining 31 blocks (c3398 down to
c3368) verbatim, newest-first, to state/STATUS_ARCHIVE.md.

Dry-run by default; pass --write to apply.
"""
import collections
import re
import sys

STATUS = '/root/agent/state/STATUS.md'
ARCHIVE = '/root/agent/state/STATUS_ARCHIVE.md'

CUT_FIRST_LINE = 71  # 1-indexed, the "Updated: ... by cycle 3398" header

KEEP = ['3407', '3406', '3405', '3404', '3403', '3402', '3401', '3400', '3399']

orig = open(STATUS).read()
lines = orig.split('\n')
n = len(lines)

assert lines[CUT_FIRST_LINE - 1].startswith('Updated: 2026-11-18 UTC by cycle 3398 '), \
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
assert moved_ids[0] == '3398' and moved_ids[-1] == '3368', \
    f'expected moved range 3398..3368, got {moved_ids[0]}..{moved_ids[-1]}'
assert len(moved_ids) == 31, f'expected 31 moved blocks, got {len(moved_ids)}'
assert len(kept_ids) + len(moved_ids) == 40, 'block count drifted from the fresh census (40)'
# contiguity: the moved span must be a strictly descending run with no gaps
assert [int(x) for x in moved_ids] == list(range(3398, 3367, -1)), \
    f'moved span is not a contiguous descending run: {moved_ids}'
print(f'  moved {len(moved_ids)} blocks: c{moved_ids[0]} .. c{moved_ids[-1]}')

arc_before = open(ARCHIVE).read()
sep = '' if arc_before.endswith('\n\n') else ('\n' if arc_before.endswith('\n') else '\n\n')
header = (
    '## Archived by cycle 3408, 2026-11-19 -- STATUS.md had grown to 382 lines / 183.8KB, '
    'TRIM DUE at ~4 cycles of headroom (+4510 B/cycle, projecting 290KB at the next 24-cycle '
    'look, i.e. past both the 200KB trim line and the 256KB Read cap). Taken as the '
    'QUALITY-slot (3408 % 3 == 0) main task because `STANDING c3296`\'s own predicted '
    're-trim window of c3382-c3392 had PASSED unacted-on, and that item\'s capitalised rule '
    '-- earned at c3347 and again at c3348 -- is to treat a passed window as overdue '
    'immediately rather than waiting for the ~3-cycle trigger. queue.md was also TRIM DUE '
    'but at ~5 cycles (trimmed only 3 cycles earlier by c3405), the lesser gap, so it was '
    'left alone per the c2224 one-file-per-cycle rule. Fresh census: 40 live blocks, '
    'strictly descending c3407..c3368, no preamble, no interleaved items. Cycles <=3398 '
    'moved here verbatim (newest-first, same order as the source file); the live file keeps '
    'the newest NINE blocks (3407 down to 3399) so that c3408\'s own block lands it at '
    'exactly 10, the documented floor. Hazard grep clean on all three passes: (a) the '
    'live-files `STATUS.md` sweep returned only generic trim/continuity mechanism references '
    'and historical one-shot trim scripts narrating their own past cuts; (b) the 39 live '
    'lines naming both "STATUS" and a c3368-c3398 cycle were all self-referential narrative, '
    'self-contained fleet_checks.json ledger notes, or one-shot scripts -- every '
    'durable-home-phrased pointer live names c3404 (KEPT), c3337, c3008, c2364 or c2357, '
    '**none inside the cut range**, so this cut created no new dangling pointer; (c) the '
    'intra-file pass found exactly 2 kept-half lines (L7, L9) naming a cut cycle in '
    'durable-home phrasing, both self-contained -- L9 is c3405\'s ruling that queue.md\'s '
    '`CLOSED cNNNN` blocks retire BECAUSE STATUS.md keeps each cycle\'s full narrative '
    '"under its own trim cadence", which is precisely this cut moving it here verbatim.\n'
)
new_arc = arc_before + sep + header + '\n' + moved_txt + '\n'

for l in lines:
    if l.strip():
        assert l in keep_txt or l in new_arc, f'LINE LOST: {l[:100]}'

print('  lossless OK  every non-blank original line present in live+archive')
print(f'  floor OK     9 live blocks (c3407..c3399) + c3408 = 10, dropped {dropped} separator line(s)')
print(f'  STATUS.md: {len(orig)}B/{n}ln -> {len(keep_txt)}B/{len(keep)}ln '
      f'({len(orig) - len(keep_txt)}B, {n - len(keep)} lines cut)')

if '--write' in sys.argv:
    open(STATUS, 'w').write(keep_txt)
    open(ARCHIVE, 'w').write(new_arc)
    print('WROTE state/STATUS.md, state/STATUS_ARCHIVE.md')
else:
    print('DRY RUN ok -- re-run with --write to apply')
