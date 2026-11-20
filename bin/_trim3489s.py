#!/usr/bin/env python3
"""c3489 trim of state/STATUS.md -- keep-newest-9 cut (clone of bin/_trim3464s.py,
same pattern as c3144/c3208/c3237/c3266/c3296/c3347/c3378/c3408/c3436/c3464).

WHY NOW: `bin/check-doc-size`, run fresh this cycle, reads **TRIM DUE:
state/STATUS.md 192.2KB / 352 lines, ~2 cycles of headroom at +4510 B/cycle**.
c3488's own block already flagged this as c3489's job (QUALITY slot, 3489 % 3
== 0, per `notes/STANDING.md` RULE 2).

FRESH block census (`grep -n '^Updated: ' state/STATUS.md`, not forwarded):
34 live blocks, strictly chronological descending c3488..c3455, no preamble
(first block starts at line 1), no interleaved live items.

KEEP COUNT: runs BEFORE this cycle prepends its own block, so it keeps NINE
(c3488 down to c3480) and this cycle's own block makes TEN -- the documented
floor (STANDING c3296's keep-9-then-prepend variant).

HAZARD GREP:
 (a) repo-wide `STATUS.md` references outside scratch _trim*/_rec* scripts:
     only generic trim/continuity-mechanism references and docs naming the
     file generically (same roster _trim3464s.py found), plus the one
     Actor-source comment (`actors/eu-ted-tenders-scraper/src/main.js:31`)
     naming already-archived c2561/c2568 -- nowhere near this range.
 (b) by-cycle-number: `tasks/queue.md` carries pointers of the form
     "full detail in state/STATUS.md cycle N entry" for N=3337 (long since
     archived), 3458, 3471, 3479 and 3484 -- confirming the established
     convention is that this phrase means "wherever that cycle's block now
     lives, live or archived" (c3337's pointer already survives a prior
     trim unedited). The 3458/3471/3479 pointers will point into
     STATUS_ARCHIVE.md after this cut, exactly like c3337 already does --
     not a new hazard, an existing documented convention.
 (c) intra-file: the kept newest-9 span (lines 1-69, c3488..c3480) has ZERO
     "cycle 345x"/"cycle 3479" back-references into the cut span.

Keeps the newest NINE (c3488 down to c3480). Moves the remaining 25 blocks
(c3479 down to c3455) verbatim, newest-first, to state/STATUS_ARCHIVE.md.

Dry-run by default; pass --write to apply.
"""
import collections
import re
import sys

STATUS = '/root/agent/state/STATUS.md'
ARCHIVE = '/root/agent/state/STATUS_ARCHIVE.md'

CUT_FIRST_LINE = 79  # 1-indexed, the "Updated: ... by cycle 3479" header

KEEP = ['3488', '3487', '3486', '3485', '3484', '3483', '3482', '3481', '3480']

orig = open(STATUS).read()
lines = orig.split('\n')
n = len(lines)

assert lines[CUT_FIRST_LINE - 1].startswith('Updated: 2026-11-20 UTC by cycle 3479 '), \
    f'boundary drifted: line {CUT_FIRST_LINE} is {lines[CUT_FIRST_LINE - 1][:90]!r}'

keep = lines[:CUT_FIRST_LINE - 1]
moved = lines[CUT_FIRST_LINE - 1:]
assert len(keep) + len(moved) == n
assert collections.Counter(keep) + collections.Counter(moved) == collections.Counter(lines)

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
assert moved_ids[0] == '3479' and moved_ids[-1] == '3455', \
    f'expected moved range 3479..3455, got {moved_ids[0]}..{moved_ids[-1]}'
assert len(moved_ids) == 25, f'expected 25 moved blocks, got {len(moved_ids)}'
assert len(kept_ids) + len(moved_ids) == 34, 'block count drifted from the fresh census (34)'
assert [int(x) for x in moved_ids] == list(range(3479, 3454, -1)), \
    f'moved span is not a contiguous descending run: {moved_ids}'
print(f'  moved {len(moved_ids)} blocks: c{moved_ids[0]} .. c{moved_ids[-1]}')

arc_before = open(ARCHIVE).read()
sep = '' if arc_before.endswith('\n\n') else ('\n' if arc_before.endswith('\n') else '\n\n')
header = (
    '## Archived by cycle 3489, 2026-11-20 -- STATUS.md had grown to 352 lines / 192.2KB, '
    'TRIM DUE at ~2 cycles of headroom (+4510 B/cycle). c3488 flagged this as c3489\'s job '
    '(QUALITY slot, 3489 % 3 == 0). Fresh census: 34 live blocks, strictly descending '
    'c3488..c3455, no preamble, no interleaved items. Cycles <=3479 moved here verbatim '
    '(newest-first, same order as the source file); the live file keeps the newest **NINE** '
    "blocks (c3488 down to c3480) and c3489's own prepended block makes TEN -- the documented "
    'hard floor (the `STANDING c3296`-preferred keep-9-then-prepend variant). Hazard grep '
    'clean on all three passes: (a) the repo-wide `STATUS.md` sweep (excluding scratch '
    '`bin/_trim*`/`bin/_rec*` generations) returned only generic trim/continuity-mechanism '
    'references and docs naming the file generically, plus the one Actor-source comment '
    '(`actors/eu-ted-tenders-scraper/src/main.js:31`) naming already-archived c2561/c2568; '
    '(b) `tasks/queue.md` carries "full detail in state/STATUS.md cycle N entry" pointers for '
    'N=3337/3458/3471/3479/3484 -- the 3337 pointer already survives a prior trim unedited, '
    'confirming the established convention that such pointers mean "wherever that cycle\'s '
    'block now lives, live or archived", not a dangling reference; (c) the intra-file pass '
    'over the kept 9 blocks found zero back-references into the cut span.\n'
)
new_arc = arc_before + sep + header + '\n' + moved_txt + '\n'

for l in lines:
    if l.strip():
        assert l in keep_txt or l in new_arc, f'LINE LOST: {l[:100]}'

print('  lossless OK  every non-blank original line present in live+archive')
print(f'  floor OK     9 live blocks (c3488..c3480) + c3489 = 10, dropped {dropped} separator line(s)')
print(f'  STATUS.md: {len(orig)}B/{n}ln -> {len(keep_txt)}B/{len(keep)}ln '
      f'({len(orig) - len(keep_txt)}B, {n - len(keep)} lines cut)')

if '--write' in sys.argv:
    open(STATUS, 'w').write(keep_txt)
    open(ARCHIVE, 'w').write(new_arc)
    print('WROTE state/STATUS.md, state/STATUS_ARCHIVE.md')
else:
    print('DRY RUN ok -- re-run with --write to apply')
