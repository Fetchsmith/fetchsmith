#!/usr/bin/env python3
"""Cycle 3561 tasks/queue.md trim.  QUALITY slot, top-handed-off task
(check-doc-size: 192.0KB/993ln, ~2c headroom).

Single lever this cycle: ROTATION only (rule-6b report-block floor = 5).
Fresh census: 8 live report-shaped CLOSED blocks, file order c3560,
c3559, c3558, c3557, c3556, c3555, c3554, c3553.  Archive the oldest 3
in file order (c3555, c3554, c3553), keep the newest 5 (c3560..c3556),
landing at the floor once this cycle's own block is added (makes 6).

Cut is ONE contiguous span: the '---' separator right after c3556's
block through the blank line right before the first open item
('NEW c3548') -- leaves exactly one blank line between the kept c3556
block and the kept c3548 open item, matching the original no-dashes
style at the end of the closed-blocks section.
"""
import re, subprocess, sys

QUEUE = 'tasks/queue.md'
ARCH = 'tasks/queue_archive.md'

orig = open(QUEUE).read()
L = orig.split('\n')

# ---- boundary asserts: exact head text, so a drifted line fails loudly ----
i_3556 = next(i for i, l in enumerate(L) if l.startswith("- [x] **CLOSED c3556 -- BUILD slot"))
i_3555 = next(i for i, l in enumerate(L) if l.startswith("- [x] **CLOSED c3555 -- QUALITY slot"))
i_3554 = next(i for i, l in enumerate(L) if l.startswith("- [x] **CLOSED c3554 -- BUILD slot"))
i_3553 = next(i for i, l in enumerate(L) if l.startswith("- [x] **CLOSED c3553 -- BUILD slot"))
i_new3548 = next(i for i, l in enumerate(L) if l.startswith("- [ ] **NEW c3548 (MEDIUM"))

assert i_3556 < i_3555 < i_3554 < i_3553 < i_new3548, (i_3556, i_3555, i_3554, i_3553, i_new3548)

# c3556's own block is 3 lines here (content + 2 sub-bullets); the blank
# right after it, then '---', then a blank, then c3555's block starts.
assert L[i_3556 + 3] == '', 'c3556 block shape drifted (expected blank at +3)'
assert L[i_3556 + 4] == '---', 'expected --- separator after c3556 block'
assert L[i_3556 + 5] == '', 'expected blank after the --- separator'
assert i_3555 == i_3556 + 6, 'c3555 does not start right after the separator'

CUT_A = i_3556 + 4            # the '---' line right after c3556's block (first line cut)
CUT_B = i_new3548             # exclusive end: first line of the open item, kept live
assert L[CUT_B - 1] == '', 'expected a blank line right before the open item'

# re-derive the report-block count FRESH (never forwarded)
reports = [l for l in L if re.match(r'^- \[x\] \*\*CLOSED c3\d\d\d -- (BUILD|QUALITY|GROWTH) slot', l)]
assert len(reports) == 8, 'expected 8 live report blocks, found %d' % len(reports)

CUT_TEXT = '\n'.join(L[CUT_A:CUT_B])
for must in ('CLOSED c3555 -- QUALITY slot', 'CLOSED c3554 -- BUILD slot', 'CLOSED c3553 -- BUILD slot'):
    assert must in CUT_TEXT, 'missing %s from cut span' % must

# ---------------- archive addition (verbatim) ----------------
arch = open(ARCH).read()
ARCH_NEW = (
    arch.rstrip('\n') + '\n\n'
    + '## Archived by cycle 3561 (from tasks/queue.md: the 3 oldest cycle-report blocks under '
      'the STANDING RULE 6b newest-5 floor -- c3555, c3554, c3553, in original file order; '
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
for pat in ('CLOSED c3555 -- QUALITY slot', 'CLOSED c3554 -- BUILD slot', 'CLOSED c3553 -- BUILD slot'):
    assert pat not in new_queue, 'rotated block still live: %s' % pat
    assert pat in ARCH_NEW, 'rotated block not archived: %s' % pat

# live items that merely share a cycle number, or sit right after the cut, must survive
for must in ('NEW c3548 (MEDIUM', 'NEW c3544 (LOW)', 'CLOSED c3556 -- BUILD slot',
             'NEW STANDING TRIPWIRE (c2336,', '(c3020,'):
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
