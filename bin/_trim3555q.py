#!/usr/bin/env python3
"""Cycle 3555 tasks/queue.md trim.  QUALITY slot, top-handed-off task
(check-doc-size: 197.1KB/989ln, ~1c headroom).

Single lever this cycle: ROTATION only (rule-6b report-block floor = 5).
Fresh census: 8 live report-shaped CLOSED blocks (c3554, c3553, c3552,
c3551, c3550, c3549, c3547, c3548, in file order -- c3547/c3548 are kept
adjacent because they are the same bundled two-part FEC guard-relaxation
task, not a reordering bug).  Archive the oldest 3 in file order (c3549,
c3547, c3548), keep the newest 5 (c3554..c3550), landing at the floor.

Cut is ONE contiguous span: the '---' separator right after c3550's block
through the blank line right before the first open ('NEW') item -- i.e.
exactly the c3549 block, its surrounding '---', and the c3547+c3548
bundle.  No RELOCATION/COMPRESSION lever attempted this cycle (time
budget); the per-SPAN candidates named in c3552's handoff were not
re-read.
"""
import re, subprocess, sys

QUEUE = 'tasks/queue.md'
ARCH = 'tasks/queue_archive.md'

orig = open(QUEUE).read()
L = orig.split('\n')

# ---- boundary asserts: exact head text, so a drifted line fails loudly ----
i_3550 = next(i for i, l in enumerate(L) if l.startswith("- [x] **CLOSED c3550 -- BUILD slot"))
i_3549 = next(i for i, l in enumerate(L) if l.startswith("- [x] **CLOSED c3549 -- QUALITY slot"))
i_3547 = next(i for i, l in enumerate(L) if l.startswith("- [x] **CLOSED c3547 -- BUILD slot"))
i_3548 = next(i for i, l in enumerate(L) if l.startswith("- [x] **CLOSED c3548 -- BUILD slot"))
i_new3548 = next(i for i, l in enumerate(L) if l.startswith("- [ ] **NEW c3548 (MEDIUM"))

assert i_3550 < i_3549 < i_3547 < i_3548 < i_new3548, (i_3550, i_3549, i_3547, i_3548, i_new3548)

# the '---' + blank right after c3550's own two-line block
assert L[i_3550 + 2] == '' and L[i_3550 + 3] == '---' and L[i_3550 + 4] == ''
CUT_A = i_3550 + 3          # the '---' line
CUT_B = i_new3548            # exclusive end: first line of the open item, kept live
assert L[CUT_B - 1] == '', 'expected a blank line right before the open item'

# re-derive the report-block count FRESH (never forwarded)
reports = [l for l in L if re.match(r'^- \[x\] \*\*CLOSED c3\d\d\d -- (BUILD|QUALITY|GROWTH) slot', l)]
assert len(reports) == 8, 'expected 8 live report blocks, found %d' % len(reports)

CUT_TEXT = '\n'.join(L[CUT_A:CUT_B])
for must in ('CLOSED c3549 -- QUALITY slot', 'CLOSED c3547 -- BUILD slot', 'CLOSED c3548 -- BUILD slot'):
    assert must in CUT_TEXT, 'missing %s from cut span' % must

# ---------------- archive addition (verbatim) ----------------
arch = open(ARCH).read()
ARCH_NEW = (
    arch.rstrip('\n') + '\n\n'
    + '## Archived by cycle 3555 (from tasks/queue.md: the 3 oldest cycle-report blocks under '
      'the STANDING RULE 6b newest-5 floor -- c3549, c3547, c3548, in original file order '
      '(c3547/c3548 kept adjacent, same bundled two-part FEC guard-relaxation task); '
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
for pat in ('CLOSED c3549 -- QUALITY slot', 'CLOSED c3547 -- BUILD slot', 'CLOSED c3548 -- BUILD slot'):
    assert pat not in new_queue, 'rotated block still live: %s' % pat
    assert pat in ARCH_NEW, 'rotated block not archived: %s' % pat

# live items that merely share a cycle number, or sit right after the cut, must survive
for must in ('NEW c3548 (MEDIUM', 'NEW c3544 (LOW)', 'CLOSED c3550 -- BUILD slot',
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
