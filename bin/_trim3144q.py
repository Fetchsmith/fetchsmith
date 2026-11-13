#!/usr/bin/env python3
"""One-shot queue.md trim for cycle 3144 (QUALITY slot, 3144 % 3 == 0).

Counted fresh (never assumed -- the c3084 interim rule):
`grep -c '^- \\[ \\] \\*\\*CLOSED c3'` -> 6 live cycle blocks against the
newest-5 floor (c3142/c3143, c3140, c3139, c3136, c3137/c3138, c3134/c3135).
c3141's rotation left exactly 5; c3142/c3143 merged into one block and c3140
was already there, so this is only ONE block of drift, not the six c3141 found.
Pure rotation: archive the single oldest block, `CLOSED c3134/c3135`.

Range is lines 57-61 (1-indexed inclusive, incl. the trailing blank): the
`CLOSED c3134/c3135` header plus its three continuation paragraphs. RULE 7
is satisfied the strict way here -- the range holds EXACTLY ONE `- [ ] ` line
(its own header), asserted below, so no open item can be hiding inside it.

RULE 1/8 hazard grep ran BEFORE the cut: `c3134|c3135|CLOSED c313[45]` over
bin/ actors/ site/ notes/ state/ (excluding trim scripts). Every hit is a
self-contained narrative mention in a separate document -- state/STATUS.md's
own per-cycle blocks, the audit/fleet-check note strings in
state/audit_dates.json and state/fleet_checks.json, and the EXECUTED c3141
record in notes/STANDING.md (which lists `c3134-c3135` as a block the PRIOR
trim left live -- a historical record of that trim's result, not a pointer).
No live file-path pointer into queue.md dangles. Inside queue.md itself the
only other mentions are prose cross-references in the c3136/c3137-c3138
blocks ("same routine noise as c3135", "the c3134/c3135 two-cycle shape"),
which read fine against the archive and are unchanged by the move.

RULE 4 checked, nothing free to retire this cycle either: `NEW c3116` is
still the cited GROWTH-default history (recorded EXHAUSTED c3130),
`NEW c3046` is cited by name from `METHOD c3084`, and `NEW (c2478)` is
guarded to 2026-11-15 (2 days out) -- so this is a pure rotation, same as
c3102/c3106/.../c3132/c3141.

Dry-run by default; pass --write to apply.
"""
import collections
import sys

QUEUE = '/root/agent/tasks/queue.md'
ARCHIVE = '/root/agent/tasks/queue_archive.md'

START, END = 57, 61  # 1-indexed, inclusive

EXPECT_HEAD = '- [ ] **CLOSED c3134/c3135 -- Regular/GROWTH slot'
EXPECT_BEFORE = ''                       # line 56 is the blank separator
EXPECT_AFTER = '- [ ] **NEW c3116'       # line 62 resumes the live queue
WANT_REMAINING = ['c3142/c3143', 'c3140', 'c3139', 'c3136', 'c3137/c3138']

HEADER = (
    '## Archived by cycle 3144 trim (QUALITY slot, 3144 % 3 == 0; 6 live CLOSED blocks '
    'counted fresh against the floor of 5 -- one cycle of ordinary one-in drift since '
    "c3141's six-block rotation) -- `CLOSED c3134/c3135` archived verbatim.\n"
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

# --- RULE 7: exactly one `- [ ] ` line in the range, and it is our own header ---
opens = [l for l in cut if l.startswith('- [ ] ') or l.startswith('- [x] ')]
assert len(opens) == 1, f'RULE 7: expected 1 item head in range, found {len(opens)}: {[o[:60] for o in opens]}'
assert opens[0].startswith(EXPECT_HEAD)

keep = lines[:START - 1] + lines[END:]
assert collections.Counter(keep) + collections.Counter(cut) == collections.Counter(lines)

keep_txt = '\n'.join(keep)
moved_txt = '\n'.join(l for l in cut if l.strip())

# --- floor assert: exactly the 5 newest blocks survive ---
live = [l for l in keep if l.startswith('- [ ] **CLOSED c3') or l.startswith('- [ ] **PROGRESS c3')]
assert len(live) == 5, f'expected 5 live blocks after the cut, got {len(live)}'
for c in WANT_REMAINING:
    assert any(f'CLOSED {c}' in l or f'PROGRESS {c}' in l for l in live), f'SURVIVOR LOST: {c}'
assert 'CLOSED c3134/c3135' not in keep_txt, 'cut block is still live'

arc_before = open(ARCHIVE).read()
sep = '' if arc_before.endswith('\n\n') else ('\n' if arc_before.endswith('\n') else '\n\n')
new_arc = arc_before + sep + HEADER + '\n' + moved_txt + '\n'

# --- losslessness: every non-blank original line is still findable ---
for l in lines:
    if l.strip():
        assert l in keep_txt or l in new_arc, f'LINE LOST: {l[:100]}'

print('  lossless OK  every non-blank original line present in live+archive')
print(f'  RULE 7 OK   exactly 1 item head in the cut range')
print(f'  floor OK    5 live blocks remain: {WANT_REMAINING}')
print(f'  queue.md: {len(orig)}B/{n}ln -> {len(keep_txt)}B/{len(keep)}ln '
      f'({len(orig) - len(keep_txt)}B, {n - len(keep)} lines cut)')

if '--write' in sys.argv:
    open(QUEUE, 'w').write(keep_txt)
    open(ARCHIVE, 'w').write(new_arc)
    print('WROTE tasks/queue.md, tasks/queue_archive.md')
else:
    print('DRY RUN ok -- re-run with --write to apply')
