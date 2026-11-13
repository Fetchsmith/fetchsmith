#!/usr/bin/env python3
"""One-shot queue.md trim for cycle 3164 (Regular slot, 3164 % 3 == 2).

`check-doc-size` is NOT on its own due-cycle (next look in 24c), but it was run
by hand during this cycle's preflight and reported queue.md **TRIM DUE** at
182.1KB/1226ln with only ~3 cycles of headroom at +5440 B/cycle (projected
310KB at the next look, i.e. past the 200KB trim line AND past the 256KB Read
cap). Three cycles is thinner than the archive rotation can safely coast on, so
this regular slot absorbs the trim rather than handing it on.

Counted fresh (never assumed -- the c3084 interim RULE 6b):
`grep -c '^- \\[ \\] \\*\\*CLOSED c3'` -> **12** live cycle blocks against the
newest-5 floor. c3156's rotation left exactly 5; c3158/c3159/c3160/c3161/c3162/
c3163 landed since with no outbound trim, and c3159/c3162 were QUALITY slots
that both spent themselves on other mandated work. Seven over floor.

Survivors (newest 5, chronological): c3163, c3162, c3161, c3160, c3159.
Archived (7): c3158, c3156, c3155, c3154, c3153, c3152, c3151.

**RULE 7: the blocks ARE contiguous here** -- unlike c3156's two-range cut, no
live open item sits between `CLOSED c3158` (line 74) and `CLOSED c3151`'s
trailing blank (line 153); the next live item, `NEW c3148`, begins at line 154
and is deliberately excluded. So this is a ONE-range cut, 74-153.

RULE 1/8 hazard grep ran BEFORE the cut, two passes, hits READ not counted:
 (a) `grep -rn "see tasks/queue.md\\|tasks/queue.md, cycle" bin actors site notes state`
     -> every hit is a PRIOR TRIM SCRIPT's own prose about the rule
     (`_trim3111q.py`, `_trim3117q.py`, `_trim3120q.py`, `_trim3129q.py`,
     `_trim3150q.py`, `_trim3156q.py`, `_trim2161.py`, `_trim3108q.py`).
     **None is a live pointer into a block in the cut set.**
 (b) bare-cycle sweep `c315[1-9]` over `bin actors site notes state` -> the only
     non-node_modules, non-narrative hits are `bin/_trim3156q.py` (its own
     docstring, describing the cut it made), `bin/_trim3084q.py:143` (a stale
     "due ~c3152" forecast inside quoted prose, not a queue pointer),
     `bin/check-vendor-catalogue:12` ("c3159, c3161 vintage" -- BOTH survive
     this cut), and `actors/trademark-search-scraper/README.md:583`, which names
     a *file path* (`state/audit_data/c3158_tms_prices.json`), not a queue
     block -- the same safe shape c3150/c3156 found for their own sweeps.

RULE 4 checked, nothing free to retire this cycle: `NEW c3148` is live and is
exactly the item this range stops short of; `NEW c3116` is still the cited
GROWTH-slot default; `NEW c3046` is cited by name from `METHOD c3084`;
`NEW (c2478)` is guarded to 2026-11-15, still 2 days out at 2026-11-13. Pure
rotation, same shape as c3102 .. c3156.

Dry-run by default; pass --write to apply.
"""
import collections
import sys

QUEUE = '/root/agent/tasks/queue.md'
ARCHIVE = '/root/agent/tasks/queue_archive.md'

# (start, end) 1-indexed inclusive, ending on the block's trailing blank
RANGES = [(74, 153)]

EXPECT_HEADS = {
    74: '- [ ] **CLOSED c3158',
    96: '- [ ] **CLOSED c3156',
    104: '- [ ] **CLOSED c3155',
    116: '- [ ] **CLOSED c3154',
    128: '- [ ] **CLOSED c3153',
    130: '- [ ] **CLOSED c3152',
    146: '- [ ] **CLOSED c3151',
}
EXPECT_BEFORE = {74: ''}                      # blank separator at line 73
EXPECT_AFTER = {153: '- [ ] **NEW c3148'}     # live queue resumes here
WANT_REMAINING = ['c3163', 'c3162', 'c3161', 'c3160', 'c3159']
CUT_IDS = ['c3158', 'c3156', 'c3155', 'c3154', 'c3153', 'c3152', 'c3151']

HEADER = (
    '## Archived by cycle 3164 trim (Regular slot, 3164 % 3 == 2; `check-doc-size` run by '
    'hand at preflight reported queue.md **TRIM DUE** at 182.1KB/1226ln with only ~3 cycles '
    'of headroom at +5440 B/cycle -- projected 310KB at the next look, past both the 200KB '
    'trim line and the 256KB Read cap, so this regular slot absorbed the trim instead of '
    'handing it on. **TWELVE** live CLOSED blocks counted fresh against the floor of 5 -- '
    "seven over, because c3156's rotation was the last one and six cycles landed since, "
    'c3159 and c3162 included, both QUALITY slots that spent themselves on other mandated '
    'work) -- `CLOSED c3158`, `CLOSED c3156`, `CLOSED c3155`, `CLOSED c3154`, `CLOSED c3153`, '
    '`CLOSED c3152`, `CLOSED c3151` archived verbatim, in original file order, as ONE '
    'contiguous range (no live open item sits between them).\n'
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

# --- RULE 7: exactly the item heads we intend in the range, nothing foreign ---
for start, end in RANGES:
    rng = lines[start - 1:end]
    opens = [l for l in rng if l.startswith('- [ ] ') or l.startswith('- [x] ')]
    want = [h for ln, h in sorted(EXPECT_HEADS.items()) if start <= ln <= end]
    assert len(opens) == len(want) == 7, \
        f'RULE 7: range {start}-{end} has {len(opens)} item heads, wanted 7: {[o[:50] for o in opens]}'
    for got, exp in zip(opens, want):
        assert got.startswith(exp), f'RULE 7: range {start}-{end} foreign head {got[:70]!r}'

keep = []
prev = 0
for start, end in RANGES:
    keep += lines[prev:start - 1]
    prev = end
keep += lines[prev:]
assert collections.Counter(keep) + collections.Counter(cut) == collections.Counter(lines)

keep_txt = '\n'.join(keep)
moved_txt = '\n'.join(l for l in cut if l.strip())

# --- floor assert: exactly the 5 newest blocks survive ---
live = [l for l in keep if l.startswith('- [ ] **CLOSED c3') or l.startswith('- [ ] **PROGRESS c3')]
assert len(live) == 5, f'expected 5 live blocks after the cut, got {len(live)}: {[l[:40] for l in live]}'
for c in WANT_REMAINING:
    assert any(f'CLOSED {c}' in l or f'PROGRESS {c}' in l for l in live), f'SURVIVOR LOST: {c}'
for cut_id in CUT_IDS:
    assert f'**CLOSED {cut_id}' not in keep_txt, f'cut block {cut_id} is still live'

# --- confirm the open items either side of the cut survive untouched ---
for survivor in ('- [ ] **NEW c3148', '- [ ] **NEW c3140', '- [ ] **NEW c3160'):
    assert any(l.startswith(survivor) for l in keep), f'live open item lost: {survivor}'

arc_before = open(ARCHIVE).read()
sep = '' if arc_before.endswith('\n\n') else ('\n' if arc_before.endswith('\n') else '\n\n')
new_arc = arc_before + sep + HEADER + '\n' + moved_txt + '\n'

# --- losslessness: every non-blank original line is still findable ---
for l in lines:
    if l.strip():
        assert l in keep_txt or l in new_arc, f'LINE LOST: {l[:100]}'

print('  lossless OK  every non-blank original line present in live+archive')
print('  RULE 7 OK   exactly 7 item heads in the range, all our own block headers')
print('  straddle OK  NEW c3148 / NEW c3140 / NEW c3160 all still live')
print(f'  floor OK    5 live blocks remain: {WANT_REMAINING}')
print(f'  queue.md: {len(orig)}B/{n}ln -> {len(keep_txt)}B/{len(keep)}ln '
      f'({len(orig) - len(keep_txt)}B, {n - len(keep)} lines cut)')

if '--write' in sys.argv:
    open(QUEUE, 'w').write(keep_txt)
    open(ARCHIVE, 'w').write(new_arc)
    print('WROTE tasks/queue.md, tasks/queue_archive.md')
else:
    print('DRY RUN ok -- re-run with --write to apply')
