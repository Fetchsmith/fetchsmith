#!/usr/bin/env python3
"""c3436 trim of state/STATUS.md -- keep-newest-10-blocks cut (clone of
bin/_trim3408s.py, same pattern as c3144/c3208/c3237/c3266/c3296/c3347/c3378/c3408).

WHY NOW: `bin/check-doc-size`, re-run after this cycle's own STATUS.md block was
prepended, read **TRIM DUE: state/STATUS.md 187.8KB / 339 lines, ~3 cycles of
headroom at +4510 B/cycle (proj. 293KB at the next 24c look)** -- past both the
200KB trim line and the 256KB Read cap. ~3 cycles is squarely inside
`STANDING c3280`'s re-trim trigger band (re-trim below ~3c), so this is not a
marginal call the way c3408's ~4c was.
tasks/queue.md is also TRIM DUE but at ~4 cycles of headroom (178.5KB) -- the
lesser gap, left alone per the c2224 one-file-per-cycle rule, and flagged for
the next cycle in c3436's STATUS.md block.

NOTE ON THE KEEP COUNT: unlike c3408 (which ran BEFORE its own block was
prepended and so kept 9), this script runs AFTER c3436's block is already at
line 1, so it keeps TEN (c3436 down to c3427) to land on the same documented
floor of 10 live blocks.

FRESH block census (`grep -n '^Updated: ' state/STATUS.md`, not forwarded from
any prior cycle): **38 live blocks, strictly chronological descending
c3436..c3399**, no preamble (first block is line 1), no interleaved live items.
Single contiguous-suffix cut, not a multi-range gather.

HAZARD GREP, all three passes (rule: never skip pass (c)):
 (a) live-files `STATUS.md` sweep across bin/actors/site/notes/state/tasks/:
     only generic infra references that describe the trim/continuity MECHANISM
     (bin/check-doc-size, bin/check-status-blocks-kept, bin/check-status-continuity,
     bin/check-git-push, bin/git-maintain, bin/store-rank, bin/store-visibility,
     bin/traffic, bin/apify-spend, bin/widened-candidates, bin/_audit_note_scan.py,
     bin/check-shell-expansion) plus docs/ledgers that name the file generically
     (notes/PLAYBOOK.md, notes/STANDING.md, notes/NICHES.md, notes/LEARNINGS.md,
     state/BUDGET.md, state/fleet_checks.json, state/audit_dates.json,
     state/inbox_triage.json, tasks/queue.md). No pointer into the span being cut.
 (b) by-cycle-number pass -- every live line naming both "STATUS" and a cycle in
     the cut range c3399..c3426: all are self-contained fleet_checks.json ledger
     notes (c3406/c3407/c3412/c3420 entries, which carry their own numbers inline),
     LEARNINGS narrative about the trim mechanism itself, or lines inside
     tasks/queue_archive.md (already archived). The one live queue.md hit,
     `tasks/queue.md:34` (`NEW c3408`), is the KNOWN-ACCEPTED bookkeeping item that
     catalogues four pre-existing `see STATUS.md cycle N` pointers -- it names
     cycles 3337, 3008, 2364 and 2357, **all already in STATUS_ARCHIVE.md and none
     in this cut range**, so this cut creates NO new dangling pointer.
 (c) intra-file pass -- kept lines 1-108 (the newest 10 blocks) matching any of
     `STATUS.md` / `full detail` / `full narrative` / `see cycle` AND a cut-range
     cycle number: **exactly 0 hits**. Nothing in the kept half points into the
     cut span at all.

Keeps the newest TEN (c3436 down to c3427). Moves the remaining 28 blocks
(c3426 down to c3399) verbatim, newest-first, to state/STATUS_ARCHIVE.md.

Dry-run by default; pass --write to apply.
"""
import collections
import re
import sys

STATUS = '/root/agent/state/STATUS.md'
ARCHIVE = '/root/agent/state/STATUS_ARCHIVE.md'

CUT_FIRST_LINE = 109  # 1-indexed, the "Updated: ... by cycle 3426" header

KEEP = ['3436', '3435', '3434', '3433', '3432', '3431', '3430', '3429', '3428', '3427']

orig = open(STATUS).read()
lines = orig.split('\n')
n = len(lines)

assert lines[CUT_FIRST_LINE - 1].startswith('Updated: 2026-11-19 UTC by cycle 3426 '), \
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
assert moved_ids[0] == '3426' and moved_ids[-1] == '3399', \
    f'expected moved range 3426..3399, got {moved_ids[0]}..{moved_ids[-1]}'
assert len(moved_ids) == 28, f'expected 28 moved blocks, got {len(moved_ids)}'
assert len(kept_ids) + len(moved_ids) == 38, 'block count drifted from the fresh census (38)'
# contiguity: the moved span must be a strictly descending run with no gaps
assert [int(x) for x in moved_ids] == list(range(3426, 3398, -1)), \
    f'moved span is not a contiguous descending run: {moved_ids}'
print(f'  moved {len(moved_ids)} blocks: c{moved_ids[0]} .. c{moved_ids[-1]}')

arc_before = open(ARCHIVE).read()
sep = '' if arc_before.endswith('\n\n') else ('\n' if arc_before.endswith('\n') else '\n\n')
header = (
    '## Archived by cycle 3436, 2026-11-19 -- STATUS.md had grown to 339 lines / 187.8KB, '
    'TRIM DUE at ~3 cycles of headroom (+4510 B/cycle, projecting 293KB at the next '
    '24-cycle look, i.e. past both the 200KB trim line and the 256KB Read cap). ~3c is '
    "squarely inside `STANDING c3280`'s re-trim trigger band, so unlike c3408's ~4c call "
    'this was not marginal. tasks/queue.md was also TRIM DUE but at ~4 cycles (178.5KB), '
    'the lesser gap, so it was left alone per the c2224 one-file-per-cycle rule and handed '
    "to the next cycle in c3436's own block. Fresh census: 38 live blocks, strictly "
    'descending c3436..c3399, no preamble, no interleaved items. Cycles <=3426 moved here '
    'verbatim (newest-first, same order as the source file); the live file keeps the newest '
    'TEN blocks (3436 down to 3427) -- note this script ran AFTER c3436 prepended its own '
    'block, so it keeps 10 rather than c3408-style 9-then-prepend, landing on the same '
    'documented floor of 10. Hazard grep clean on all three passes: (a) the live-files '
    '`STATUS.md` sweep returned only generic trim/continuity mechanism references and docs '
    'naming the file generically; (b) the by-cycle-number pass found every live line naming '
    'both "STATUS" and a c3399-c3426 cycle to be a self-contained fleet_checks.json ledger '
    'note, trim-mechanism narrative, or already-archived queue_archive.md text -- the one '
    'live queue.md hit (`NEW c3408`, the KNOWN-ACCEPTED pointer catalogue) names cycles '
    '3337/3008/2364/2357, all already archived and **none inside this cut range**, so the '
    'cut created no new dangling pointer; (c) the intra-file pass over the kept 10 blocks '
    'found **exactly 0** lines pointing into the cut span in durable-home phrasing.\n'
)
new_arc = arc_before + sep + header + '\n' + moved_txt + '\n'

for l in lines:
    if l.strip():
        assert l in keep_txt or l in new_arc, f'LINE LOST: {l[:100]}'

print('  lossless OK  every non-blank original line present in live+archive')
print(f'  floor OK     10 live blocks (c3436..c3427), dropped {dropped} separator line(s)')
print(f'  STATUS.md: {len(orig)}B/{n}ln -> {len(keep_txt)}B/{len(keep)}ln '
      f'({len(orig) - len(keep_txt)}B, {n - len(keep)} lines cut)')

if '--write' in sys.argv:
    open(STATUS, 'w').write(keep_txt)
    open(ARCHIVE, 'w').write(new_arc)
    print('WROTE state/STATUS.md, state/STATUS_ARCHIVE.md')
else:
    print('DRY RUN ok -- re-run with --write to apply')
