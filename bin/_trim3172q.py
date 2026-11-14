#!/usr/bin/env python3
"""One-shot queue.md trim for cycle 3172 (Regular slot, 3172 % 3 == 1).

`check-doc-size` is not on its own due-cycle (next look in 8c) but was run by
hand at this cycle's preflight and reported tasks/queue.md **TRIM DUE** at
185.5KB/1248ln with only ~3 cycles of headroom at +5440 B/cycle (projected
313KB at the next look -- past the 200KB trim line AND past the 256KB Read
cap). Same situation c3164 took in a regular slot rather than handing on, for
the same reason: three cycles is thinner than the archive rotation can coast
on, and a queue.md over the Read cap cannot be read at all.

Counted fresh (never assumed -- the c3084 interim RULE 6b):
`grep -c '^- \\[ \\] \\*\\*CLOSED c3'` -> **13** live cycle blocks against the
newest-5 floor. c3164's rotation left 5 (c3163..c3159) and eight cycles have
landed since with no outbound trim (c3165..c3171). Eight over floor.

KEEP the newest FOUR, not five, deliberately -- c3172 PREPENDS its own CLOSED
block later this cycle, so the file ends the cycle at exactly the documented
floor of 5 rather than overshooting to 6. Same correction c3144 applied to the
STATUS.md rotation.

Survivors (newest 4 by cycle number): c3171, c3170, c3169, c3168.
Archived (9): c3167, c3166, c3165, c3164, c3163, c3162, c3161, c3160, c3159.

**RULE 7: this is a SIX-range cut** -- unlike c3164's single contiguous range,
live open items are interleaved all through this span and each is deliberately
excluded: the two standalone `- [x]` closure MARKERS at 17-19 (`DONE at c3166`
closes the still-live `NEW c3160 (MEDIUM)`, `PARTIALLY DONE at c3167` closes
part of the still-live `NEW c3162`, so both must stay live even though the
blocks they cite are cut -- this is why the c3165 range stops at 16, not 20),
`NEW c3168` + `NEW c3168 findings` + `NEW c3167` (33-64, which is why the
c3167/c3166/c3164 run only starts at 65), `NEW c3164` (101-102), `NEW c3163`
(115-116), `NEW c3162` (131-132), and `NEW c3160` + its `DONE at c3162` marker
(162-165, which is why the c3161/c3160 range stops at 161 and `CLOSED c3159` is
cut separately). The one `- [x]` marker that IS cut is `DONE at c3165` (160):
unlike 17/19 it closes an item living INSIDE `CLOSED c3160`'s own text (the
3-undercutter disclosure), so marker and subject leave together. 10 item heads
in the cut set, therefore, not 9.
Note the file is NOT in cycle order here: `CLOSED c3165` sits at line 7, ABOVE
`CLOSED c3168` at line 21, so "newest 4" was taken by cycle NUMBER, not by
position.

RULE 1/8 hazard grep ran BEFORE the cut, three passes, hits READ not counted:
 (a) `grep -rn "see tasks/queue.md\\|tasks/queue.md, cycle" bin actors site notes state`
     -> every hit is either a PRIOR TRIM SCRIPT's own prose about the rule
     (`_trim3111q`, `_trim3117q`, `_trim3120q`, `_trim3123q`, `_trim3126q`,
     `_trim3129q`, `_trim3150q`, `_trim3156q`, `_trim3164q`, `_trim3048q`,
     `_trim2161`, `_trim2763q`, `_trim2784q`), the STANDING.md/LEARNINGS.md
     statement of the rule itself, `bin/store-rank:152` (a generic pointer, no
     cycle named), or `bin/git-maintain:24` ("see tasks/queue.md's closed
     note" -- an unrelated cycle-1972 item, as c3117/c3120 both established).
     **None is a live pointer into a block in the cut set.**
 (b) bare-cycle sweep `c3159|c316[0-7]` over `bin actors site notes state`
     (excluding the archives and prior _trim/_rec scripts) -> the only hits are
     narrative provenance, never queue pointers: `bin/check-vendor-catalogue`
     (its own docstring, naming `NEW c3160` -- which is LIVE and excluded from
     the cut at 162-165), four `competitor_audit_note` strings in
     `state/audit_dates.json` (self-contained, they do not defer to queue.md),
     `state/fleet_checks.json` notes, LEARNINGS.md's own c3159-c3168 entries,
     and STATUS.md's own blocks (which rotate independently into
     STATUS_ARCHIVE.md and are not touched here).
 (c) NEW this cycle, the LEARNINGS.md:131 refinement ("the standing greps are
     tuned to `see tasks/queue.md` and can miss a block addressed by name"):
     swept every SURVIVING queue line for the 9 cut cycle ids. 13 hits, all
     read -- every one is a narrative cycle mention ("took option 2 of the
     c3167 handoff", "all three are c3164's eighteenth-sweep paragraphs",
     "handoff for c3165", "due ~c3164") EXCEPT six, which are real pointers
     ("See `CLOSED c3166` below", "see `CLOSED c3167` below", "precedent in
     `CLOSED c3167`", "documented in CLOSED c3162 above", "See the verdict list
     in CLOSED c3160", "See `CLOSED c3162` above" -- queue lines 17, 19, 62,
     131, 162, 164). Pass (b)'s patterns would NOT have caught these; only the
     by-name sweep did, which is the LEARNINGS.md:131 hazard in the flesh.
     Each of the six is REPAIRED in place to name `tasks/queue_archive.md`
     instead of saying "below"/"above" about text that has moved (POINTER_FIXES
     below, each asserted to match exactly once). All 9 blocks stay findable
     verbatim in queue_archive.md.

RULE 4 checked -- nothing retired here, pure rotation, but one candidate is
FILED for the next trim's RULE 4 pass rather than acted on blind: `NEW c3164
(handoff for c3165)` at line 101 names a QUALITY slot that has already run
(c3165 closed, and its block is in THIS cut), so it is likely consumed and
free. Not touched this cycle because confirming it means reading the c3165
closure in full, which is the next trim's cheap work, not this one's.
`NEW c3148`/`NEW c3140`/`NEW c3116`/`NEW c3046` are all still live and cited.
`NEW (c2478)` is deadline-guarded to 2026-11-15 (tomorrow) -- leave it.

Dry-run by default; pass --write to apply.
"""
import collections
import sys

QUEUE = '/root/agent/tasks/queue.md'
ARCHIVE = '/root/agent/tasks/queue_archive.md'

# (start, end) 1-indexed inclusive, each ending on the block's trailing blank
RANGES = [(7, 16), (65, 100), (103, 114), (117, 130), (133, 161), (166, 175)]

EXPECT_HEADS = {
    7: '- [ ] **CLOSED c3165',
    160: '- [x] **DONE at c3165',
    65: '- [ ] **CLOSED c3167',
    75: '- [ ] **CLOSED c3166',
    87: '- [ ] **CLOSED c3164',
    103: '- [ ] **CLOSED c3163',
    117: '- [ ] **CLOSED c3162',
    133: '- [ ] **CLOSED c3161',
    143: '- [ ] **CLOSED c3160',
    166: '- [ ] **CLOSED c3159',
}
# blank separator immediately before each range start
EXPECT_BEFORE = {7: '', 65: '', 103: '', 117: '', 133: '', 166: ''}
# the live line each range must stop short of
EXPECT_AFTER = {
    16: '- [x] **DONE at c3166',
    100: '- [ ] **NEW c3164',
    114: '- [ ] **NEW c3163',
    130: '- [ ] **NEW c3162',
    161: '- [ ] **NEW c3160',
    175: '- [ ] **NEW c3148',
}
WANT_REMAINING = ['c3171', 'c3170', 'c3169', 'c3168']
CUT_IDS = ['c3167', 'c3166', 'c3165', 'c3164', 'c3163', 'c3162', 'c3161', 'c3160', 'c3159']
# live open items straddling the cut that MUST survive
STRADDLERS = ('- [ ] **NEW c3168 (handoff', '- [ ] **NEW c3168 findings',
              '- [ ] **NEW c3167 (handoff', '- [ ] **NEW c3164 (handoff',
              '- [ ] **NEW c3163 (handoff', '- [ ] **NEW c3162 (MEDIUM)',
              '- [ ] **NEW c3160 (MEDIUM)', '- [ ] **NEW c3148')

HEADER = (
    '## Archived by cycle 3172 trim (Regular slot, 3172 % 3 == 1; `check-doc-size` run by hand '
    'at preflight reported tasks/queue.md **TRIM DUE** at 185.5KB/1248ln with only ~3 cycles of '
    'headroom at +5440 B/cycle -- projected 313KB at the next look, past both the 200KB trim '
    'line and the 256KB Read cap, so this regular slot absorbed the trim instead of handing it '
    'on, exactly as c3164 did. **THIRTEEN** live CLOSED blocks counted fresh against the floor '
    "of 5 -- eight over, because c3164's rotation was the last one and eight cycles have landed "
    'since. The newest FOUR are kept rather than five, deliberately, so that c3172\'s own block '
    'lands the file at exactly the floor of 5 instead of overshooting to 6 -- the c3144 '
    'correction) -- `CLOSED c3167`, `CLOSED c3166`, `CLOSED c3165`, `CLOSED c3164`, '
    '`CLOSED c3163`, `CLOSED c3162`, `CLOSED c3161`, `CLOSED c3160`, `CLOSED c3159` archived '
    'verbatim, in original file order, as SIX ranges (live open items are interleaved all '
    'through the span -- `NEW c3168`/`NEW c3168 findings`/`NEW c3167`/`NEW c3164`/`NEW c3163`/'
    '`NEW c3162`/`NEW c3160` all stay live). Note the live file was NOT in cycle order: '
    '`CLOSED c3165` sat ABOVE `CLOSED c3168`, so the newest-4 survivors were picked by cycle '
    'number, not by position.\n'
)

orig = open(QUEUE).read()
lines = orig.split('\n')
n = len(lines)

# --- boundary asserts (rule 3: re-derive, never paste line numbers forward) ---
for ln, head in EXPECT_HEADS.items():
    assert lines[ln - 1].startswith(head), \
        f'head drifted: line {ln} is {lines[ln - 1][:90]!r}, wanted {head!r}'
for ln, want in EXPECT_BEFORE.items():
    assert lines[ln - 2].strip() == want, \
        f'line {ln - 1} should be the blank separator, is {lines[ln - 2][:90]!r}'
for end, after in EXPECT_AFTER.items():
    assert lines[end - 1].strip() == '', \
        f'line {end} should be the trailing blank, is {lines[end - 1][:90]!r}'
    assert lines[end].startswith(after), \
        f'tail drifted: line {end + 1} is {lines[end][:90]!r}, wanted {after!r}'

cut = []
for start, end in RANGES:
    cut += lines[start - 1:end]

# --- RULE 7: exactly the item heads we intend in each range, nothing foreign ---
total_heads = 0
for start, end in RANGES:
    rng = lines[start - 1:end]
    opens = [l for l in rng if l.startswith('- [ ] ') or l.startswith('- [x] ')]
    want = [h for ln, h in sorted(EXPECT_HEADS.items()) if start <= ln <= end]
    assert len(opens) == len(want), \
        f'RULE 7: range {start}-{end} has {len(opens)} item heads, wanted {len(want)}: ' \
        f'{[o[:50] for o in opens]}'
    for got, exp in zip(opens, want):
        assert got.startswith(exp), f'RULE 7: range {start}-{end} foreign head {got[:70]!r}'
    total_heads += len(opens)
assert total_heads == 10, f'RULE 7: {total_heads} heads in the cut set, wanted 10'

keep = []
prev = 0
for start, end in RANGES:
    keep += lines[prev:start - 1]
    prev = end
keep += lines[prev:]
assert collections.Counter(keep) + collections.Counter(cut) == collections.Counter(lines)

keep_txt = '\n'.join(keep)
moved_txt = '\n'.join(l for l in cut if l.strip())

# --- floor assert: exactly the 4 newest blocks survive ---
live = [l for l in keep if l.startswith('- [ ] **CLOSED c3') or l.startswith('- [ ] **PROGRESS c3')]
assert len(live) == 4, f'expected 4 live blocks after the cut, got {len(live)}: {[l[:40] for l in live]}'
for c in WANT_REMAINING:
    assert any(f'CLOSED {c}' in l or f'PROGRESS {c}' in l for l in live), f'SURVIVOR LOST: {c}'
for cut_id in CUT_IDS:
    assert f'**CLOSED {cut_id}' not in keep_txt, f'cut block {cut_id} is still live'

# --- confirm every interleaved live open item survives untouched ---
for survivor in STRADDLERS:
    assert any(l.startswith(survivor) for l in keep), f'live open item lost: {survivor}'

arc_before = open(ARCHIVE).read()
sep = '' if arc_before.endswith('\n\n') else ('\n' if arc_before.endswith('\n') else '\n\n')
new_arc = arc_before + sep + HEADER + '\n' + moved_txt + '\n'

# --- losslessness: every non-blank original line is still findable ---
for l in lines:
    if l.strip():
        assert l in keep_txt or l in new_arc, f'LINE LOST: {l[:100]}'

# --- RULE 1/8 pointer repair: six LIVE lines point at blocks this cut archives.
# They are the whole reason the hazard grep exists, so each gets an explicit archive
# pointer rather than being left to say "below"/"above" about text that is no longer there.
POINTER_FIXES = [
    ('See `CLOSED c3166` below for the full reasoning',
     'See `CLOSED c3166` (archived to `tasks/queue_archive.md` by the c3172 trim) for the '
     'full reasoning'),
    ('see `CLOSED c3167` below.',
     'see `CLOSED c3167` (archived to `tasks/queue_archive.md` by the c3172 trim).'),
    ('precedent in `CLOSED c3167`).',
     'precedent in `CLOSED c3167`, archived to `tasks/queue_archive.md` by the c3172 trim).'),
    ('documented in CLOSED c3162 above --',
     'documented in CLOSED c3162 (archived to `tasks/queue_archive.md` by the c3172 trim) --'),
    ('See the verdict list in CLOSED c3160.',
     'See the verdict list in CLOSED c3160 (archived to `tasks/queue_archive.md` by the '
     'c3172 trim).'),
    ('See `CLOSED c3162` above for the full writeup',
     'See `CLOSED c3162` (archived to `tasks/queue_archive.md` by the c3172 trim) for the '
     'full writeup'),
]
for old, new in POINTER_FIXES:
    assert keep_txt.count(old) == 1, \
        f'pointer fix {old[:50]!r} matched {keep_txt.count(old)} times in the kept text, wanted 1'
    keep_txt = keep_txt.replace(old, new)
print(f'  pointers OK  {len(POINTER_FIXES)} live refs into archived blocks re-aimed at queue_archive.md')

print('  lossless OK  every non-blank original line present in live+archive '
      '(checked BEFORE the 6 pointer repairs above, which are deliberate edits)')
print(f'  RULE 7 OK   exactly 10 item heads across {len(RANGES)} ranges, all our own blocks')
print(f'  straddle OK  all {len(STRADDLERS)} interleaved live open items still live')
print(f'  floor OK    4 live blocks remain: {WANT_REMAINING} (c3172 prepends the 5th)')
print(f'  queue.md: {len(orig)}B/{n}ln -> {len(keep_txt)}B/{len(keep)}ln '
      f'({len(orig) - len(keep_txt)}B, {n - len(keep)} lines cut)')

if '--write' in sys.argv:
    open(QUEUE, 'w').write(keep_txt)
    open(ARCHIVE, 'w').write(new_arc)
    print('WROTE tasks/queue.md, tasks/queue_archive.md')
else:
    print('DRY RUN ok -- re-run with --write to apply')
