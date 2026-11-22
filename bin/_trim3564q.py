#!/usr/bin/env python3
"""Cycle 3564 tasks/queue.md trim.  QUALITY slot, top-handed-off task
(check-doc-size: 187.0KB/980ln, ~2c headroom -- the urgent one; STATUS.md
is also TRIM DUE but at ~5c).

Single lever this cycle: ROTATION only (rule-6b report-block floor = 5).
Fresh census: 8 live report-shaped CLOSED blocks, file order c3563,
c3562, c3561, c3560, c3559, c3558, c3557, c3556.  Archive the oldest 3
in file order (c3558, c3557, c3556), keep the newest 5 (c3563..c3559),
landing at the floor once this cycle's own block is added (makes 6).

Cut is ONE contiguous span: c3558's own block line through the LAST
sub-bullet of c3556's block, including the two '---' separators that sit
between them.  The blank line that followed c3556's block is KEPT, so the
retained c3559 line is still separated from the first open item
('NEW c3548') by exactly one blank -- matching the original no-dashes
style at the end of the closed-blocks section.
"""
import re, subprocess, sys

QUEUE = 'tasks/queue.md'
ARCH = 'tasks/queue_archive.md'

orig = open(QUEUE).read()
L = orig.split('\n')

# ---- boundary asserts: exact head text, so a drifted line fails loudly ----
i_3559 = next(i for i, l in enumerate(L) if l.startswith("- [x] **CLOSED c3559 -- BUILD slot"))
i_3558 = next(i for i, l in enumerate(L) if l.startswith("- [x] **CLOSED c3558 -- QUALITY slot"))
i_3557 = next(i for i, l in enumerate(L) if l.startswith("- [x] **CLOSED c3557 -- BUILD slot"))
i_3556 = next(i for i, l in enumerate(L) if l.startswith("- [x] **CLOSED c3556 -- BUILD slot"))
i_new3548 = next(i for i, l in enumerate(L) if l.startswith("- [ ] **NEW c3548 (MEDIUM"))

assert i_3559 < i_3558 < i_3557 < i_3556 < i_new3548, (i_3559, i_3558, i_3557, i_3556, i_new3548)

# c3559's block is a single line, with c3558's block starting immediately after.
assert i_3558 == i_3559 + 1, 'c3559/c3558 adjacency drifted'
# c3556's block is content + 2 sub-bullets, then a blank, then the open item.
assert L[i_3556 + 1].startswith('  - '), 'c3556 sub-bullet 1 missing'
assert L[i_3556 + 2].startswith('  - '), 'c3556 sub-bullet 2 missing'
assert L[i_3556 + 3] == '', 'c3556 block shape drifted (expected blank at +3)'
assert i_new3548 == i_3556 + 4, 'open item does not start right after c3556 block'

CUT_A = i_3558                # c3558's own block line (first line cut)
CUT_B = i_3556 + 3            # exclusive end: the blank after c3556, KEPT live

# the two separators between the three rotated blocks must be inside the span
assert L[CUT_A:CUT_B].count('---') == 2, 'expected exactly 2 --- separators in the cut span'

# re-derive the report-block count FRESH (never forwarded)
reports = [l for l in L if re.match(r'^- \[x\] \*\*CLOSED c3\d\d\d -- (BUILD|QUALITY|GROWTH) slot', l)]
assert len(reports) == 8, 'expected 8 live report blocks, found %d' % len(reports)

CUT_TEXT = '\n'.join(L[CUT_A:CUT_B])
for must in ('CLOSED c3558 -- QUALITY slot', 'CLOSED c3557 -- BUILD slot', 'CLOSED c3556 -- BUILD slot'):
    assert must in CUT_TEXT, 'missing %s from cut span' % must

# ---------------- archive addition (verbatim) ----------------
arch = open(ARCH).read()
ARCH_NEW = (
    arch.rstrip('\n') + '\n\n'
    + '## Archived by cycle 3564 (from tasks/queue.md: the 3 oldest cycle-report blocks under '
      'the STANDING RULE 6b newest-5 floor -- c3558, c3557, c3556, in original file order; '
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
for pat in ('CLOSED c3558 -- QUALITY slot', 'CLOSED c3557 -- BUILD slot', 'CLOSED c3556 -- BUILD slot'):
    assert pat not in new_queue, 'rotated block still live: %s' % pat
    assert pat in ARCH_NEW, 'rotated block not archived: %s' % pat

# the kept c3559 line must end up separated from the open item by exactly one blank
j = new_L.index([l for l in new_L if l.startswith("- [x] **CLOSED c3559 -- BUILD slot")][0])
assert new_L[j + 1] == '', 'lost the blank after c3559'
assert new_L[j + 2].startswith('- [ ] **NEW c3548 (MEDIUM'), 'open item not adjacent after the cut'

# live items that merely share a cycle number, or sit right after the cut, must survive
for must in ('NEW c3548 (MEDIUM', 'NEW c3544 (LOW)', 'CLOSED c3563 -- BUILD slot',
             'CLOSED c3559 -- BUILD slot', 'NEW c3536', 'CLOSED c3518/c3520/c3529'):
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
