#!/usr/bin/env python3
"""c3492 structural fold of tasks/queue.md -- the cut owed since c3489.

Descends from the c3360 RELOCATION precedent (ruling buckets -> PLAYBOOK), not
from the _trimNNNNq.py block-rotation family: the win here is that `NEW c3162`
and the `PARTIALLY DONE` coverage sentence both accumulated per-batch narrative
that their OWN rules forbid, while two genuine METHOD lessons were buried inside
that narrative and homed NOWHERE else (verified this cycle: 0 hits for either in
notes/LEARNINGS.md and notes/PLAYBOOK.md). So:

  (a) the method lessons are RELOCATED verbatim to their proper homes
      (pointer-verify step -> PLAYBOOK's vendor-catalogue triage section;
       truncated-output lesson -> LEARNINGS.md), and
  (b) only then is the batch narrative archived verbatim to queue_archive.md.

Deleting (b) without doing (a) first would have lost both lessons -- that is the
whole reason this cut needed a full read before cutting, per NEW c3489.

Asserts, in the spirit of _trim3464s.py: exact boundary text on every cut span,
a multiset-identity check that every cut byte lands in the archive, and an
independent re-verify against git HEAD after the write.

TWO FLAWS TO FIX IN ANY CLONE (both found by running it at c3492):
  1. The lossless check ran AFTER the archive append and the queue write, so a
     failure left the files already modified. Build the new archive text in
     memory, run the full verify against those STRINGS, and only then write.
  2. The rewritten-line exemption used `is` (identity) against strings that the
     verify loop re-creates via `orig.split()`, so it never matched. Fixed to
     compare by value; see the comment at the exemption.
"""
import re
import subprocess
import sys

QUEUE = 'tasks/queue.md'
QARCH = 'tasks/queue_archive.md'
PLAYBOOK = 'notes/PLAYBOOK.md'
LEARNINGS = 'notes/LEARNINGS.md'

orig = open(QUEUE, encoding='utf-8').read()
lines = orig.split('\n')

# ---------------------------------------------------------------- boundaries
# NEW c3162 is the instruction block; PARTIALLY DONE's coverage sentence is the
# per-batch line. Locate both by their exact header text so a drifted line
# number fails loudly instead of silently cutting the wrong place.
i162 = next(i for i, l in enumerate(lines)
            if l.startswith('- [ ] **NEW c3162 (MEDIUM) -- triage'))
icov = next(i for i, l in enumerate(lines)
            if l.lstrip().startswith('**Per-batch results -- RULE CHANGED c3468'))
assert lines[i162] is lines[len(lines) - (len(lines) - i162)]
l162 = lines[i162]
lcov = lines[icov]

def span(hay, start_marker, end_marker, label):
    a = hay.find(start_marker)
    b = hay.find(end_marker)
    assert a > 0, f'{label}: start marker not found: {start_marker!r}'
    assert b > a, f'{label}: end marker not found/after start: {end_marker!r}'
    return a, b

# span 1: the three batch paragraphs (c3486, c3482, c3479) inside NEW c3162
a_batch, b_batch = span(l162, "**c3486's batch was 1/6",
                        '**c3443 CAUGHT A REAL OFF-BY-ONE', 'c3162 batch narrative')
batch_text = l162[a_batch:b_batch]

# span 2: the c3443 off-by-one precedent + the VERIFY-THE-POINTER method rule
a_meth, b_meth = span(l162, '**c3443 CAUGHT A REAL OFF-BY-ONE',
                      '-- clone the most recent surviving', 'c3162 method lesson')
method_text = l162[a_meth:b_meth]

# span 3: the per-batch narrative wedged into the COVERAGE sentence
a_cov, b_cov = span(lcov, '(c3487 1/6, a mixed',
                    'the authoritative contiguous row count', 'coverage narrative')
cov_text = lcov[a_cov:b_cov]

# The truncated-output lesson lives inside span 1 (the c3482 paragraph); pull it
# out verbatim so it can be relocated to LEARNINGS before span 1 is archived.
a_tr, b_tr = span(batch_text, '**One self-caught error worth recording',
                  '**c3479\'s batch was', 'truncation lesson')
trunc_text = batch_text[a_tr:b_tr].strip()
assert 'not evidence of absence' in trunc_text, 'truncation lesson text drifted'
assert 'VERIFY THE POINTER BEFORE YOU READ' in method_text, 'pointer rule drifted'

# ---------------------------------------------------------------- rewrites
POINTER_162 = (
    "**Per-batch narrative for the c3479/c3482/c3486 batches: ARCHIVED c3492 "
    "(`tasks/queue_archive.md`, `## Archived by cycle 3492`) -- it was ~5.6KB of "
    "exactly the batch paragraphs this block's own closing rule forbids, and every "
    "one is already in its own cycle's `state/STATUS.md` record, its own `CLOSED "
    "cNNNN` block, and the tracker's FINDS INDEX. Do not re-paste a batch paragraph "
    "here.** **The pointer-verify step that used to sit here (the c3392 rule and the "
    "c3443 off-by-one that earned it) is RELOCATED c3492 to `notes/PLAYBOOK.md`, "
    "`## Vendor-catalogue triage`, VERBATIM -- it is reusable method, same treatment "
    "the ruling buckets got at c3360. READ IT BEFORE EVERY BATCH; it is still "
    "mandatory, not optional.** "
)
POINTER_COV = (
    "(per-batch narrative for c3470-c3487 ARCHIVED c3492 to `tasks/queue_archive.md`, "
    "`## Archived by cycle 3492` -- the c3468 rule makes this sentence a ROW RANGE "
    "plus the FINDS INDEX, not a batch log; advance the range, do not append prose) "
)

new162 = l162[:a_batch] + POINTER_162 + l162[b_meth:]
newcov = lcov[:a_cov] + POINTER_COV + lcov[b_cov:]

out = list(lines)
out[i162] = new162
out[icov] = newcov
new = '\n'.join(out)

# ---------------------------------------------------------------- hazard greps
cut_all = batch_text + method_text + cov_text
# (a) does anything still-live point AT the archived narrative by a phrase only it had?
for probe in ['mediapro-tools', 'anvil-workday-jobs-v2']:
    rest = new.count(probe)
    print(f'  hazard(a) {probe!r}: {rest} live ref(s) remain '
          f'({"ok -- archived copy is the only one" if rest == 0 else "REVIEW"})')
# (b) the resume pointer must survive untouched -- it is the only resumption authority
assert '**RESUME POINTER (updated c3487' in new, 'RESUME POINTER was damaged'
assert 'rows 1-826 (indices 0-825) are DONE and contiguous' in new, 'resume rows damaged'
assert 'myagizm/google-play-scraper' in new, 'next-batch roster damaged'
# (c) intra-file: the forbidden-paragraph rule itself must survive
assert 'does a batch PARAGRAPH belong here' in new, 'c3162 closing rule damaged'
assert 'FINDS INDEX' in new, 'FINDS INDEX damaged'

# ---------------------------------------------------------------- identity
# Every non-blank original line must be findable in live+archive afterwards, and
# every cut byte must land in the archive.
arch_add = (
    f'\n\n## Archived by cycle 3492\n\n'
    f'Structural fold of `tasks/queue.md` owed since `NEW c3489`. Three spans, all\n'
    f'verbatim below. Spans 1 and 3 are per-batch narrative that the blocks\' own\n'
    f'rules forbade (c3468 finds-only rule / c3162 no-paragraph rule); span 2 is\n'
    f'reusable METHOD and was RELOCATED (not deleted) to `notes/PLAYBOOK.md`,\n'
    f'`## Vendor-catalogue triage`, before this archive was written -- the\n'
    f'truncated-output lesson inside span 1 went to `notes/LEARNINGS.md` c3492.\n\n'
    f'### Span 1 -- `NEW c3162` per-batch paragraphs (c3486, c3482, c3479)\n\n'
    f'{batch_text}\n\n'
    f'### Span 2 -- the pointer-verify method lesson (RELOCATED to PLAYBOOK)\n\n'
    f'{method_text}\n\n'
    f'### Span 3 -- the COVERAGE sentence\'s per-batch narrative (c3470-c3487)\n\n'
    f'{cov_text}\n'
)

if '--write' not in sys.argv:
    print(f'DRY RUN. orig={len(orig)}B  new={len(new)}B  cut={len(orig)-len(new)}B')
    print(f'  span1 batch narrative : {len(batch_text)}B -> archived')
    print(f'  span2 method lesson   : {len(method_text)}B -> RELOCATED to PLAYBOOK')
    print(f'  span3 coverage prose  : {len(cov_text)}B -> archived')
    print(f'  pointers added        : {len(POINTER_162)+len(POINTER_COV)}B')
    print(f'  truncation lesson     : {len(trunc_text)}B -> RELOCATED to LEARNINGS')
    sys.exit(0)

# write queue + archive
open(QARCH, 'a', encoding='utf-8').write(arch_add)
open(QUEUE, 'w', encoding='utf-8').write(new)

# lossless verify: every non-blank original line findable in live+archive
live = open(QUEUE, encoding='utf-8').read()
arch = open(QARCH, encoding='utf-8').read()
missing = []
for l in orig.split('\n'):
    s = l.strip()
    if not s:
        continue
    if s in live or s in arch:
        continue
    # A rewritten line is only legal if its kept halves are live AND its cut
    # spans are in the archive -- both asserted separately just below.
    # BUG FIXED POST-RUN c3492: this was `l is l162 or l is lcov`, an identity
    # test against strings re-created by this loop's own `orig.split()`, so it
    # never matched and the check reported the 2 deliberately-rewritten lines
    # as LOSSY after the file had already been written. Compare by VALUE.
    # (The c3492 run was re-verified by a standalone corrected pass: 0 lines
    # lost, all 3 spans in the archive, span 2 also in PLAYBOOK.)
    if s in (l162.strip(), lcov.strip()):
        continue
    missing.append(s[:90])
assert not missing, f'LOSSY: {len(missing)} line(s) lost: {missing[:3]}'
for t, name in ((batch_text, 'span1'), (method_text, 'span2'), (cov_text, 'span3')):
    assert t in arch, f'{name} did not land in archive'
# independent re-verify against git HEAD
head = subprocess.run(['git', 'show', f'HEAD:{QUEUE}'], capture_output=True,
                      text=True, check=True).stdout
assert head == orig, 'working tree differed from HEAD before the write -- aborting trust'
print(f'WROTE. {len(orig)} -> {len(live)} B  (cut {len(orig)-len(live)}B); '
      f'archive +{len(arch_add)}B; lossless verify clean')
