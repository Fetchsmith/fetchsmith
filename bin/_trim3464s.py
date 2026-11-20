#!/usr/bin/env python3
"""c3464 trim of state/STATUS.md -- keep-newest-9 cut (clone of bin/_trim3436s.py,
same pattern as c3144/c3208/c3237/c3266/c3296/c3347/c3378/c3408/c3436).

WHY NOW: `bin/check-doc-size`, run fresh this cycle (NOT forwarded from c3463's
claimed 189.1KB), reads **TRIM DUE: state/STATUS.md 194.6KB / 376 lines, ~1 cycle
of headroom at +4510 B/cycle (proj. 300KB at the next 24c look)**. The raw file is
**199,293 B -- 707 B under the 200KB trim line**, i.e. the next cycle's prepended
block alone would cross it, and projection runs past the 256KB Read cap. This is
the most urgent this file has ever read: c3436 cut at ~3c and c3408 at ~4c, both
with more slack than this. `STANDING c3296`'s decision rule (re-trim below ~3c of
headroom, not when the banner says DUE) is satisfied with room to spare, and
c3463's own block already named this the FIRST PRIORITY handoff for c3464.
tasks/queue.md is also TRIM DUE but at 176.3KB / ~4 cycles of headroom -- the
lesser gap, left alone per the c2224 one-file-per-cycle rule and flagged for a
later cycle in c3464's own STATUS.md block.

KEEP COUNT: this script runs BEFORE c3464 prepends its own block, so it keeps
NINE (c3463 down to c3455) and c3464's own block makes TEN -- the documented
floor, and the variant `STANDING c3296` explicitly prefers (c3144's reasoning)
over c3208/c3237/c3266/c3436's keep-10-then-prepend-to-11, which wastes a block
of headroom. 10 live blocks is a HARD FLOOR: this is the deepest legal cut, so
expect a fresh TRIM SOON/WARN banner one check-interval from now and do NOT read
it as a failed trim.

FRESH block census (`grep -n '^Updated: ' state/STATUS.md`, not forwarded from any
prior cycle): **37 live blocks, strictly chronological descending c3463..c3427**,
no preamble (the first block starts at line 1), no interleaved live items. Single
contiguous-suffix cut, not a multi-range gather.

HAZARD GREP, all three passes (rule: never skip pass (c)):
 (a) live-files `STATUS.md` sweep across bin/actors/site/notes/state/tasks/,
     excluding the scratch `bin/_trim*`/`bin/_rec*` generations that only describe
     past cuts: only generic infra references that describe the trim/continuity
     MECHANISM (bin/check-doc-size, bin/check-status-blocks-kept,
     bin/check-status-continuity, bin/check-git-push, bin/git-maintain,
     bin/store-rank, bin/store-visibility, bin/traffic, bin/apify-spend,
     bin/widened-candidates, bin/_audit_note_scan.py, bin/check-shell-expansion)
     plus docs/ledgers naming the file generically (notes/PLAYBOOK.md,
     notes/STANDING.md, notes/NICHES.md, notes/LEARNINGS.md, state/BUDGET.md,
     state/fleet_checks.json, state/audit_dates.json, state/inbox_triage.json,
     state/autocommit.log, tasks/queue.md). One Actor-source hit,
     `actors/eu-ted-tenders-scraper/src/main.js:31` ("see their STATUS.md notes"),
     names c2561/c2568 -- long since in STATUS_ARCHIVE.md and nowhere near this
     cut range. No pointer into the span being cut.
 (b) by-cycle-number pass -- every live line naming both "STATUS" and a cycle in
     the cut range c3427..c3454: **6 lines, all self-contained.** Three are
     state/fleet_checks.json ledger notes (c3446/c3444/c3435 entries) which carry
     their own cycle numbers and findings inline rather than referring out to a
     STATUS.md block; two are state/autocommit.log rows (c3446/c3454) that merely
     list the file paths touched by a commit; the one live tasks/queue.md hit
     (`:59`, the vendor-catalogue per-batch tracker) points at
     `tasks/queue_archive.md`'s `## Archived by cycle 3444` header, **not** at
     STATUS.md. This cut creates NO new dangling pointer.
 (c) intra-file pass -- kept lines 1-103 (the newest 9 blocks) matching any of
     `STATUS.md` / `full detail` / `full narrative` / `see cycle` / `cycle N block`
     AND a cut-range cycle number: **exactly 0 hits**. Nothing in the kept half
     points into the cut span at all.

Keeps the newest NINE (c3463 down to c3455). Moves the remaining 28 blocks
(c3454 down to c3427) verbatim, newest-first, to state/STATUS_ARCHIVE.md.

Dry-run by default; pass --write to apply.
"""
import collections
import re
import sys

STATUS = '/root/agent/state/STATUS.md'
ARCHIVE = '/root/agent/state/STATUS_ARCHIVE.md'

CUT_FIRST_LINE = 104  # 1-indexed, the "Updated: ... by cycle 3454" header

KEEP = ['3463', '3462', '3461', '3460', '3459', '3458', '3457', '3456', '3455']

orig = open(STATUS).read()
lines = orig.split('\n')
n = len(lines)

assert lines[CUT_FIRST_LINE - 1].startswith('Updated: 2026-11-20 UTC by cycle 3454 '), \
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
assert moved_ids[0] == '3454' and moved_ids[-1] == '3427', \
    f'expected moved range 3454..3427, got {moved_ids[0]}..{moved_ids[-1]}'
assert len(moved_ids) == 28, f'expected 28 moved blocks, got {len(moved_ids)}'
assert len(kept_ids) + len(moved_ids) == 37, 'block count drifted from the fresh census (37)'
# contiguity: the moved span must be a strictly descending run with no gaps
assert [int(x) for x in moved_ids] == list(range(3454, 3426, -1)), \
    f'moved span is not a contiguous descending run: {moved_ids}'
print(f'  moved {len(moved_ids)} blocks: c{moved_ids[0]} .. c{moved_ids[-1]}')

arc_before = open(ARCHIVE).read()
sep = '' if arc_before.endswith('\n\n') else ('\n' if arc_before.endswith('\n') else '\n\n')
header = (
    '## Archived by cycle 3464, 2026-11-20 -- STATUS.md had grown to 376 lines / 194.6KB '
    '(199,293 B raw, just **707 B under the 200KB trim line**), TRIM DUE at ~1 cycle of '
    'headroom (+4510 B/cycle, projecting 300KB at the next 24-cycle look, past both the '
    '200KB trim line and the 256KB Read cap). That is the tightest this file has ever been '
    "cut at -- c3436 ran at ~3c and c3408 at ~4c -- so `STANDING c3296`'s re-trim-below-~3c "
    "rule was satisfied with room to spare, and c3463's block had already named this c3464's "
    'FIRST PRIORITY handoff. tasks/queue.md was also TRIM DUE but at 176.3KB / ~4 cycles, '
    'the lesser gap, so it was left alone per the c2224 one-file-per-cycle rule and flagged '
    "in c3464's own block. Fresh census: 37 live blocks, strictly descending c3463..c3427, "
    'no preamble, no interleaved items. Cycles <=3454 moved here verbatim (newest-first, '
    'same order as the source file); the live file keeps the newest **NINE** blocks '
    "(c3463 down to c3455) and c3464's own prepended block makes TEN -- the documented hard "
    'floor, taking the `STANDING c3296`-preferred keep-9-then-prepend variant (c3144) rather '
    "than c3436's keep-10-then-end-at-11, which wastes a block of headroom. Hazard grep clean "
    'on all three passes: (a) the live-files `STATUS.md` sweep (excluding the scratch '
    '`bin/_trim*`/`bin/_rec*` generations) returned only generic trim/continuity mechanism '
    'references and docs naming the file generically, plus one Actor-source comment '
    '(`actors/eu-ted-tenders-scraper/src/main.js:31`) naming c2561/c2568, long archived and '
    'nowhere near this range; (b) the by-cycle-number pass found **6** live lines naming both '
    '"STATUS" and a c3427-c3454 cycle, every one self-contained -- three fleet_checks.json '
    'ledger notes (c3446/c3444/c3435) that carry their numbers and findings inline, two '
    'autocommit.log rows (c3446/c3454) listing only commit paths, and one tasks/queue.md line '
    '(`:59`) whose pointer targets `tasks/queue_archive.md`\'s `## Archived by cycle 3444` '
    'header rather than STATUS.md -- so the cut created no new dangling pointer; (c) the '
    'intra-file pass over the kept 9 blocks found **exactly 0** lines pointing into the cut '
    'span in durable-home phrasing.\n'
)
new_arc = arc_before + sep + header + '\n' + moved_txt + '\n'

for l in lines:
    if l.strip():
        assert l in keep_txt or l in new_arc, f'LINE LOST: {l[:100]}'

print('  lossless OK  every non-blank original line present in live+archive')
print(f'  floor OK     9 live blocks (c3463..c3455) + c3464 = 10, dropped {dropped} separator line(s)')
print(f'  STATUS.md: {len(orig)}B/{n}ln -> {len(keep_txt)}B/{len(keep)}ln '
      f'({len(orig) - len(keep_txt)}B, {n - len(keep)} lines cut)')

if '--write' in sys.argv:
    open(STATUS, 'w').write(keep_txt)
    open(ARCHIVE, 'w').write(new_arc)
    print('WROTE state/STATUS.md, state/STATUS_ARCHIVE.md')
else:
    print('DRY RUN ok -- re-run with --write to apply')
