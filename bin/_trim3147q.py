#!/usr/bin/env python3
"""One-shot queue.md trim for cycle 3147 (QUALITY slot, 3147 % 3 == 0).

Counted fresh (never assumed -- the c3084 interim rule):
`grep -c '^- \\[ \\] \\*\\*CLOSED c3'` -> 8 live cycle blocks against the
newest-5 floor (c3146, c3145, c3144, c3142/c3143, c3140, c3139, c3136,
c3137/c3138). c3144's rotation left exactly 5; three cycles (c3145, c3146,
plus the c3142/c3143 merge already counted) landed since without an
outbound trim -- ordinary one-in-per-cycle drift, 3 blocks over floor.

Range is lines 53-76 (1-indexed inclusive, incl. the trailing blank): the
three oldest blocks -- `CLOSED c3139`, `CLOSED c3136`, `CLOSED c3137/c3138`
-- back to back. Two OPEN items sit adjacent and must stay live: `NEW c3140`
immediately BEFORE the range (lines 51-52) and `NEW c3136` immediately
AFTER it (lines 77-78) -- neither is included in the cut.

RULE 1/8 hazard grep ran BEFORE the cut: `c3139|c3136|CLOSED c313[6-9]|
c3137|c3138` over bin/ actors/ site/ notes/ state/ (excluding trim scripts
and queue_archive.md). Every hit is a self-contained narrative mention in a
separate document -- state/STATUS.md's own per-cycle blocks, and
state/audit_dates.json's own competitor_audit_note strings (which embed
"cycle 3138 (... prep done c3137 ...)" and an unrelated c2796-era note that
happens to contain the substring "queue.md/LEARNINGS c2796", itself a
historical cross-reference to a different cycle, not a pointer into the
range being cut here). No live file-path pointer into queue.md dangles.

RULE 4 checked, nothing free to retire this cycle: `NEW c3116` is still the
cited GROWTH-default history (recorded EXHAUSTED c3130), `NEW c3046` is
cited by name from `METHOD c3084`, `NEW (c2478)` is guarded to 2026-11-15
(2 days out) -- so this is a pure rotation, same shape as c3102 .. c3144.

Dry-run by default; pass --write to apply.
"""
import collections
import sys

QUEUE = '/root/agent/tasks/queue.md'
ARCHIVE = '/root/agent/tasks/queue_archive.md'

START, END = 53, 76  # 1-indexed, inclusive

EXPECT_HEAD = '- [ ] **CLOSED c3139 -- Regular/GROWTH slot'
EXPECT_BEFORE = ''                       # line 52 is the blank after NEW c3140
EXPECT_AFTER = '- [ ] **NEW c3136'       # line 77 resumes the live queue
WANT_REMAINING = ['c3146', 'c3145', 'c3144', 'c3142/c3143', 'c3140']

HEADER = (
    '## Archived by cycle 3147 trim (QUALITY slot, 3147 % 3 == 0; 8 live CLOSED blocks '
    'counted fresh against the floor of 5 -- three cycles of ordinary one-in drift since '
    "c3144's rotation) -- `CLOSED c3139`, `CLOSED c3136`, `CLOSED c3137/c3138` archived "
    'verbatim, in original order.\n'
)

orig = open(QUEUE).read()
lines = orig.split('\n')
n = len(lines)

# --- boundary asserts (rule 3: re-derive, never paste line numbers forward) ---
assert lines[START - 1].startswith(EXPECT_HEAD), \
    f'head drifted: line {START} is {lines[START - 1][:90]!r}'
assert lines[START - 2].strip() == EXPECT_BEFORE, \
    f'line {START - 1} should be the blank separator, is {lines[START - 2][:90]!r}'
assert lines[END - 1].strip() == '', \
    f'line {END} should be the trailing blank, is {lines[END - 1][:90]!r}'
assert lines[END].startswith(EXPECT_AFTER), \
    f'tail drifted: line {END + 1} is {lines[END][:90]!r}'

cut = lines[START - 1:END]

# --- RULE 7: exactly the 3 item heads we intend, and nothing else foreign ---
opens = [l for l in cut if l.startswith('- [ ] ') or l.startswith('- [x] ')]
assert len(opens) == 3, f'RULE 7: expected 3 item heads in range, found {len(opens)}: {[o[:60] for o in opens]}'
assert opens[0].startswith('- [ ] **CLOSED c3139')
assert opens[1].startswith('- [ ] **CLOSED c3136')
assert opens[2].startswith('- [ ] **CLOSED c3137/c3138')

keep = lines[:START - 1] + lines[END:]
assert collections.Counter(keep) + collections.Counter(cut) == collections.Counter(lines)

keep_txt = '\n'.join(keep)
moved_txt = '\n'.join(l for l in cut if l.strip())

# --- floor assert: exactly the 5 newest blocks survive ---
live = [l for l in keep if l.startswith('- [ ] **CLOSED c3') or l.startswith('- [ ] **PROGRESS c3')]
assert len(live) == 5, f'expected 5 live blocks after the cut, got {len(live)}'
for c in WANT_REMAINING:
    assert any(f'CLOSED {c}' in l or f'PROGRESS {c}' in l for l in live), f'SURVIVOR LOST: {c}'
for cut_id in ('c3139', 'c3136', 'c3137/c3138'):
    assert f'CLOSED {cut_id}' not in keep_txt, f'cut block {cut_id} is still live'

# --- confirm the two adjacent open items survive untouched ---
assert any(l.startswith('- [ ] **NEW c3140') for l in keep), 'NEW c3140 lost'
assert any(l.startswith('- [ ] **NEW c3136') for l in keep), 'NEW c3136 lost'

arc_before = open(ARCHIVE).read()
sep = '' if arc_before.endswith('\n\n') else ('\n' if arc_before.endswith('\n') else '\n\n')
new_arc = arc_before + sep + HEADER + '\n' + moved_txt + '\n'

# --- losslessness: every non-blank original line is still findable ---
for l in lines:
    if l.strip():
        assert l in keep_txt or l in new_arc, f'LINE LOST: {l[:100]}'

print('  lossless OK  every non-blank original line present in live+archive')
print('  RULE 7 OK   exactly 3 item heads in the cut range, all our own headers')
print(f'  floor OK    5 live blocks remain: {WANT_REMAINING}')
print(f'  queue.md: {len(orig)}B/{n}ln -> {len(keep_txt)}B/{len(keep)}ln '
      f'({len(orig) - len(keep_txt)}B, {n - len(keep)} lines cut)')

if '--write' in sys.argv:
    open(QUEUE, 'w').write(keep_txt)
    open(ARCHIVE, 'w').write(new_arc)
    print('WROTE tasks/queue.md, tasks/queue_archive.md')
else:
    print('DRY RUN ok -- re-run with --write to apply')
