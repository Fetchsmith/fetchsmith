#!/usr/bin/env python3
"""c3296 trim of state/STATUS.md -- keep-newest-10-blocks cut (clone of
bin/_trim3266s.py, same pattern as c3144/c3208/c3237/c3266).

`bin/check-doc-size` read TRIM DUE on arrival: STATUS.md at 190.9KB/447 lines,
**~2 cycles of headroom** at +4510 B/cycle (projected 297KB at its next look,
past both the 200KB trim line and the 256KB Read cap). This was the top queued
backlog item, escalated by c3294 and re-flagged by c3295 (which trimmed
queue.md instead and explicitly handed STATUS.md to this cycle).

Block census re-derived FRESH (rule 3, never paste line numbers forward) via
`grep -n '^Updated:' state/STATUS.md` plus a per-block byte/line count (rule 1):
**40 live blocks, strictly chronological descending, c3295 down to c3256, no
preamble and no interleaved live items** -- unlike tasks/queue.md, where c3295
found 22 report blocks scattered through the file rather than in a prefix. So
the cut here is a single contiguous suffix, not a multi-range gather.

3-PASS HAZARD GREP, all clean, run BEFORE this script was written:
 (a) generic `STATUS.md cycle`/`see state/STATUS` sweep over bin actors site
     notes state tasks -- every hit names a cycle in the 1400-2800 range or
     lives in an already-archived file (queue_archive.md, LEARNINGS_ARCHIVE.md)
     or in the dead `_trim*.py` docstrings. Nothing in the 3256-3286 cut range.
 (b) tightened pointer sweep restricted to LIVE files only (bin actors site
     notes/LEARNINGS.md notes/PLAYBOOK.md notes/NICHES.md state/*.json
     tasks/queue.md) for `STATUS.md ... (cycle|c)32[56-86]` within a 60-char
     window: **zero hits.** A wider pass for any line in a live file naming
     both "STATUS" and a cut-range cycle returned only queue.md's own
     `CLOSED cNNNN` report headers (self-referential, not pointers into
     STATUS.md) and `bin/_trim3266s.py`'s docstring.
 (c) intra-file pass over EVERY kept line (1..102, blocks c3295..c3287) -- the
     pass c3280 warned never to skip. 14 hits, all narrative mentions
     ("the c3280 trim", "c3272 was a genuinely open question", vendor rulings
     c3278/c3279/c3281/c3282, "c3286's commit verified present in git log").
     **No "See state/STATUS.md cycle N for full detail" dangling pointer.**
     Same ruling as c3180/c3266: the cycle number and its content stay true and
     fully readable, only the file holding them moves.

Keeps the newest NINE (c3295 down to c3287) so that **cycle 3296's own block,
prepended after this script runs, lands the live file at exactly 10** -- the
documented floor, and c3144's explicit reasoning. Moves the remaining 31
blocks (c3286 down to c3256) verbatim, newest-first (same order as the source
file), to state/STATUS_ARCHIVE.md.

DEPTH NOTE (the c1976 lesson, honoured as far as the floor allows): keeping 9 +
this cycle's own block leaves ~50KB live, which at +4510 B/cycle projects to
~158KB at check-doc-size's next 24-cycle look -- past the 150KB WARN line but
far short of the 200KB TRIM line (~9 cycles of real headroom then). Cutting
deeper is NOT available: 10 live blocks is a hard floor, so this is the deepest
legal cut. Expect `TRIM SOON` (not `TRIM DUE`) at the next look and do not
treat it as a failed trim.

Dry-run by default; pass --write to apply.
"""
import collections
import re
import sys

STATUS = '/root/agent/state/STATUS.md'
ARCHIVE = '/root/agent/state/STATUS_ARCHIVE.md'

CUT_FIRST_LINE = 103  # 1-indexed, the "Updated: ... by cycle 3286" header

KEEP = ['3295', '3294', '3293', '3292', '3291', '3290', '3289', '3288', '3287']

orig = open(STATUS).read()
lines = orig.split('\n')
n = len(lines)

assert lines[CUT_FIRST_LINE - 1].startswith('Updated: 2026-11-16 UTC by cycle 3286 '), \
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
assert moved_ids[0] == '3286' and moved_ids[-1] == '3256', \
    f'expected moved range 3286..3256, got {moved_ids[0]}..{moved_ids[-1]}'
assert len(moved_ids) == 31, f'expected 31 moved blocks, got {len(moved_ids)}'
assert len(kept_ids) + len(moved_ids) == 40, 'block count drifted from the fresh census (40)'
print(f'  moved {len(moved_ids)} blocks: c{moved_ids[0]} .. c{moved_ids[-1]}')

arc_before = open(ARCHIVE).read()
sep = '' if arc_before.endswith('\n\n') else ('\n' if arc_before.endswith('\n') else '\n\n')
header = (
    '## Archived by cycle 3296, 2026-11-16 -- STATUS.md had grown to 447 lines / 190.9KB, '
    'TRIM DUE with only ~2 cycles of headroom (check-doc-size projected 297KB at its next '
    'look, past both the 200KB trim line and the 256KB Read cap); this was the top queued '
    'backlog item, escalated by c3294 and handed to this cycle by c3295. Cycles <=3286 '
    'moved here verbatim (newest-first, same order as the source file); the live file keeps '
    'the newest NINE blocks (3295 down to 3287) so that c3296\'s own block lands it at '
    'exactly 10, the documented floor (c3144\'s reasoning). 3-pass hazard grep clean: the '
    'live-files-only pointer sweep for `STATUS.md ... c3256-c3286` returned ZERO hits, and '
    'the intra-file pass over all 102 kept lines found only 14 narrative mentions (the '
    'c3280 trim, the c3272 field-drift lead, vendor rulings c3278/c3279/c3281/c3282, '
    '"c3286\'s commit verified present") -- no dangling "See STATUS.md cycle N" pointer, '
    'same ruling as c3180/c3266. DEPTH: 10 live blocks is a hard floor, so this is the '
    'deepest legal cut; ~50KB live post-prepend projects to ~158KB at the next 24c look, '
    'i.e. expect TRIM SOON (not TRIM DUE) and do not read it as a failed trim.\n'
)
new_arc = arc_before + sep + header + '\n' + moved_txt + '\n'

for l in lines:
    if l.strip():
        assert l in keep_txt or l in new_arc, f'LINE LOST: {l[:100]}'

print('  lossless OK  every non-blank original line present in live+archive')
print(f'  floor OK     9 live blocks (c3295..c3287) + c3296 = 10, dropped {dropped} separator line(s)')
print(f'  STATUS.md: {len(orig)}B/{n}ln -> {len(keep_txt)}B/{len(keep)}ln '
      f'({len(orig) - len(keep_txt)}B, {n - len(keep)} lines cut)')

if '--write' in sys.argv:
    open(STATUS, 'w').write(keep_txt)
    open(ARCHIVE, 'w').write(new_arc)
    print('WROTE state/STATUS.md, state/STATUS_ARCHIVE.md')
else:
    print('DRY RUN ok -- re-run with --write to apply')
