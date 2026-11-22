#!/usr/bin/env python3
"""Cycle 3567 tasks/queue.md trim.  QUALITY slot, top-handed-off task
(check-doc-size: 187.2KB/976ln, ~2c headroom -- TRIM DUE, handed off by c3566).

Single lever this cycle: ROTATION only (rule-6b report-block floor = 5).
Fresh census: 8 live report-shaped CLOSED blocks, file order c3566,
c3565, c3564, c3563, c3562, c3561, c3560, c3559.  Archive the oldest 3
in file order (c3561, c3560, c3559), keep the newest 5 (c3566..c3562),
landing at the floor once this cycle's own block is added (makes 6).

Cut is ONE contiguous span: c3561's own block line through the blank
line that follows c3559's block (inclusive) -- these three blocks are
NOT separated by '---' lines in this file region, just a blank line
each.  The separating blank KEPT live is c3562's OWN trailing blank
(the one right after its sub-bullet, already present before the cut
starts), not c3559's -- cutting c3559's trailing blank too, rather than
leaving it adjacent to c3562's, is what keeps the retained c3562 block
separated from the first open item ('NEW c3548') by exactly one blank
instead of two.
"""
import re, subprocess, sys

QUEUE = 'tasks/queue.md'
ARCH = 'tasks/queue_archive.md'

orig = open(QUEUE).read()
L = orig.split('\n')

# ---- boundary asserts: exact head text, so a drifted line fails loudly ----
i_3562 = next(i for i, l in enumerate(L) if l.startswith("- [x] **CLOSED c3562 -- BUILD slot"))
i_3561 = next(i for i, l in enumerate(L) if l.startswith("- [x] **CLOSED c3561 -- QUALITY slot"))
i_3560 = next(i for i, l in enumerate(L) if l.startswith("- [x] **CLOSED c3560 -- BUILD slot"))
i_3559 = next(i for i, l in enumerate(L) if l.startswith("- [x] **CLOSED c3559 -- BUILD slot"))
i_new3548 = next(i for i, l in enumerate(L) if l.startswith("- [ ] **NEW c3548 (MEDIUM"))

assert i_3562 < i_3561 < i_3560 < i_3559 < i_new3548, (i_3562, i_3561, i_3560, i_3559, i_new3548)

# c3562's block is content + 1 sub-bullet, then a blank, then c3561's block.
assert L[i_3562 + 1].startswith('  - '), 'c3562 sub-bullet missing'
assert L[i_3562 + 2] == '', 'c3562 block shape drifted (expected blank at +2)'
assert i_3561 == i_3562 + 3, 'c3561 does not start right after c3562 block'
# c3561's block is content + 1 sub-bullet, then blank, then c3560.
assert L[i_3561 + 1].startswith('  - '), 'c3561 sub-bullet missing'
assert L[i_3561 + 2] == '', 'c3561 block shape drifted (expected blank at +2)'
assert i_3560 == i_3561 + 3, 'c3560 does not start right after c3561 block'
# c3560's block is a single line, then blank, then c3559.
assert L[i_3560 + 1] == '', 'c3560 block shape drifted (expected blank at +1, single-line block)'
assert i_3559 == i_3560 + 2, 'c3559 does not start right after c3560 block'
# c3559's block is a single line, then blank, then the open item.
assert L[i_3559 + 1] == '', 'c3559 block shape drifted (expected blank at +1, single-line block)'
assert i_new3548 == i_3559 + 2, 'open item does not start right after c3559 block'

CUT_A = i_3561                # c3561's own block line (first line cut)
CUT_B = i_new3548             # exclusive end: cut through c3559's trailing blank too,
                               # so only c3562's OWN trailing blank (already before CUT_A) survives

# re-derive the report-block count FRESH (never forwarded)
reports = [l for l in L if re.match(r'^- \[x\] \*\*CLOSED c3\d\d\d -- (BUILD|QUALITY|GROWTH) slot', l)]
assert len(reports) == 8, 'expected 8 live report blocks, found %d' % len(reports)

CUT_TEXT = '\n'.join(L[CUT_A:CUT_B])
for must in ('CLOSED c3561 -- QUALITY slot', 'CLOSED c3560 -- BUILD slot', 'CLOSED c3559 -- BUILD slot'):
    assert must in CUT_TEXT, 'missing %s from cut span' % must

# ---------------- archive addition (verbatim) ----------------
arch = open(ARCH).read()
ARCH_NEW = (
    arch.rstrip('\n') + '\n\n'
    + '## Archived by cycle 3567 (from tasks/queue.md: the 3 oldest cycle-report blocks under '
      'the STANDING RULE 6b newest-5 floor -- c3561, c3560, c3559, in original file order; '
      'rotation-only lever, QUALITY slot, one contiguous span.)\n\n'
    + CUT_TEXT.strip('\n') + '\n'
)

# ---------------- new queue text ----------------
new_L = L[:CUT_A] + L[CUT_B:]
new_queue = '\n'.join(new_L)

# ---------------- asserts, all BEFORE any write ----------------
pool = set(x.strip() for x in (new_queue.split('\n') + ARCH_NEW.split('\n')) if x.strip())
missing = [x for x in L if x.strip() and x.strip() not in pool]
assert not missing, 'LOSSLESS FAIL, %d line(s): %r' % (len(missing), missing[:3])

live_reports = [l for l in new_queue.split('\n')
                if re.match(r'^- \[x\] \*\*CLOSED c3\d\d\d -- (BUILD|QUALITY|GROWTH) slot', l)]
assert len(live_reports) == 5, 'floor broken: %d live report blocks' % len(live_reports)
for pat in ('CLOSED c3561 -- QUALITY slot', 'CLOSED c3560 -- BUILD slot', 'CLOSED c3559 -- BUILD slot'):
    assert pat not in new_queue, 'rotated block still live: %s' % pat
    assert pat in ARCH_NEW, 'rotated block not archived: %s' % pat

# the kept c3562 line must end up separated from the open item by exactly one blank
j = new_L.index([l for l in new_L if l.startswith("- [x] **CLOSED c3562 -- BUILD slot")][0])
assert new_L[j + 1].startswith('  - '), 'lost c3562 sub-bullet'
assert new_L[j + 2] == '', 'lost the blank after c3562 sub-bullet'
assert new_L[j + 3].startswith('- [ ] **NEW c3548 (MEDIUM'), 'open item not adjacent after the cut'

# live items that merely share a cycle number, or sit right after the cut, must survive
for must in ('NEW c3548 (MEDIUM', 'NEW c3544 (LOW)', 'CLOSED c3566 -- BUILD slot',
             'CLOSED c3562 -- BUILD slot', 'NEW c3536', 'CLOSED c3518/c3520/c3529'):
    assert must in new_queue, 'lost a live line: %s' % must

print('asserts OK  queue %.1fKB -> %.1fKB (%d -> %d lines)  archive +%.1fKB'
      % (len(orig) / 1024, len(new_queue) / 1024,
         len(L), len(new_L), (len(ARCH_NEW) - len(arch)) / 1024))

if '--write' not in sys.argv:
    print('dry run; pass --write'); sys.exit(0)

open(ARCH, 'w').write(ARCH_NEW)
open(QUEUE, 'w').write(new_queue)
print('written')

# ---------------- independent re-verify against git HEAD ----------------
head = subprocess.run(['git', 'show', 'HEAD:tasks/queue.md'],
                      capture_output=True, text=True, check=True).stdout
pool2 = set()
for p in (QUEUE, ARCH):
    pool2.update(x.strip() for x in open(p).read().split('\n') if x.strip())
miss2 = [x for x in head.split('\n') if x.strip() and x.strip() not in pool2]
assert not miss2, 'POST-WRITE LOSSLESS FAIL: %r' % miss2[:3]
print('post-write re-verify vs git HEAD: lossless, %d non-blank lines all accounted for'
      % len([x for x in head.split('\n') if x.strip()]))
