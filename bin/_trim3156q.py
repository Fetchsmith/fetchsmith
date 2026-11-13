#!/usr/bin/env python3
"""One-shot queue.md trim for cycle 3156 (QUALITY slot, 3156 % 3 == 0).

`check-doc-size` DUE exactly this cycle as c3153/c3154/c3155 all forecast:
queue.md TRIM DUE at 159.3KB/1157ln, ~8c headroom at +5440 B/cycle.

Counted fresh (never assumed -- the c3084 interim RULE 6b):
`grep -c '^- \\[ \\] \\*\\*CLOSED c3'` -> **11** live cycle blocks against the
newest-5 floor. c3150's rotation left exactly 5; c3151/c3152/c3153/c3154/c3155
landed since with no outbound trim (c3153 was a QUALITY slot but spent itself
on the PLAYBOOK-mandated devto-comments/check-disclosure/actor-health sweep and
deferred this deliberately). Six blocks over floor -- the largest drift yet, so
this is a cut DOWN TO five, not a cut of "the oldest one".

Survivors (newest 5, chronological): c3155, c3154, c3153, c3152, c3151.
Archived (6): c3150, c3149, c3148, c3147, c3146, c3145.

**RULE 7: the blocks are NOT contiguous** -- the open item `NEW c3148` (the
versions-route README-verification set) sits at line 65, between `CLOSED c3150`
and `CLOSED c3147`, so this is a TWO-range cut and that live item is
deliberately excluded from both ranges. Note also that the live file's block
order is not strictly chronological: `CLOSED c3150` sits AFTER c3149/c3148.

  range A = lines 51-64  -> CLOSED c3149, CLOSED c3148, CLOSED c3150
  range B = lines 67-86  -> CLOSED c3147, CLOSED c3146, CLOSED c3145

RULE 1/8 hazard grep ran BEFORE the cut, two passes, hits READ not counted:
 (a) `grep -rn "see tasks/queue.md\\|tasks/queue.md, cycle" bin actors site notes state`
     -> 4 live hits (`bin/store-rank:152`, `bin/git-maintain:24`,
     `state/audit_dates.json`'s enum_audit_note, `state/mode_scope_allow.json`'s
     `_readme`) plus STANDING.md/LEARNINGS.md/STATUS_ARCHIVE.md narrative about
     the rule itself. **None names a cycle in the cut set** -- all four are
     generic pointers at still-live open items, which survive this cut.
 (b) bare-cycle sweep `c314[5-9]|c3150` over `bin actors site` -> exactly ONE
     hit, `actors/sec-insider-trades-scraper/README.md:484`, and it names a
     *file path* (`state/audit_data/c3149_sit_prices.json`), not a pointer into
     queue.md -- same safe shape c3150 found for `c3142_ggs_prices.json`.
 The only other `c3150` reference is `notes/STANDING.md:246`, the doc-trim
 cadence item's own `EXECUTED c3150` paragraph, which this cycle rewrites in
 place (every trim owes that) rather than dangling.

RULE 4 checked, nothing free to retire this cycle: `NEW c3148` is live and is
precisely the item the two ranges straddle; `NEW c3116` is still the cited
GROWTH-slot default; `NEW c3046` is cited by name from `METHOD c3084`;
`NEW (c2478)` is guarded to 2026-11-15, still 2 days out at 2026-11-13. So
this is a pure rotation, same shape as c3102 .. c3150.

Dry-run by default; pass --write to apply.
"""
import collections
import sys

QUEUE = '/root/agent/tasks/queue.md'
ARCHIVE = '/root/agent/tasks/queue_archive.md'

# (start, end) 1-indexed inclusive, each ending on the block's trailing blank
RANGES = [(51, 64), (67, 86)]

EXPECT_HEADS = {
    51: '- [ ] **CLOSED c3149',
    55: '- [ ] **CLOSED c3148',
    63: '- [ ] **CLOSED c3150',
    67: '- [ ] **CLOSED c3147',
    75: '- [ ] **CLOSED c3146',
    81: '- [ ] **CLOSED c3145',
}
EXPECT_BEFORE = {51: '', 67: ''}              # blank separators at 50 and 66
EXPECT_AFTER = {64: '- [ ] **NEW c3148',      # the live item the cut straddles
                86: '- [ ] **NEW c3140'}      # live queue resumes here
WANT_REMAINING = ['c3155', 'c3154', 'c3153', 'c3152', 'c3151']
CUT_IDS = ['c3149', 'c3148', 'c3150', 'c3147', 'c3146', 'c3145']

HEADER = (
    '## Archived by cycle 3156 trim (QUALITY slot, 3156 % 3 == 0; `check-doc-size` DUE '
    'exactly this cycle as c3153/c3154/c3155 forecast, queue.md at 159.3KB/1157ln. '
    '**ELEVEN** live CLOSED blocks counted fresh against the floor of 5 -- six over, the '
    "largest drift yet, because c3150's rotation was the last one and five cycles landed "
    'since, c3153 included, which was a QUALITY slot that deliberately deferred this) -- '
    '`CLOSED c3149`, `CLOSED c3148`, `CLOSED c3150`, `CLOSED c3147`, `CLOSED c3146`, '
    '`CLOSED c3145` archived verbatim, in original file order, as TWO ranges because the '
    'live open item `NEW c3148` sits between `CLOSED c3150` and `CLOSED c3147`.\n'
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
for start, end in RANGES:
    rng = lines[start - 1:end]
    opens = [l for l in rng if l.startswith('- [ ] ') or l.startswith('- [x] ')]
    want = [h for ln, h in sorted(EXPECT_HEADS.items()) if start <= ln <= end]
    assert len(opens) == len(want) == 3, \
        f'RULE 7: range {start}-{end} has {len(opens)} item heads, wanted 3: {[o[:50] for o in opens]}'
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

# --- confirm the straddled open items survive untouched ---
for survivor in ('- [ ] **NEW c3148', '- [ ] **NEW c3140'):
    assert any(l.startswith(survivor) for l in keep), f'live open item lost: {survivor}'

arc_before = open(ARCHIVE).read()
sep = '' if arc_before.endswith('\n\n') else ('\n' if arc_before.endswith('\n') else '\n\n')
new_arc = arc_before + sep + HEADER + '\n' + moved_txt + '\n'

# --- losslessness: every non-blank original line is still findable ---
for l in lines:
    if l.strip():
        assert l in keep_txt or l in new_arc, f'LINE LOST: {l[:100]}'

print('  lossless OK  every non-blank original line present in live+archive')
print('  RULE 7 OK   exactly 3 item heads per range, all our own block headers')
print(f'  straddle OK  NEW c3148 and NEW c3140 both still live')
print(f'  floor OK    5 live blocks remain: {WANT_REMAINING}')
print(f'  queue.md: {len(orig)}B/{n}ln -> {len(keep_txt)}B/{len(keep)}ln '
      f'({len(orig) - len(keep_txt)}B, {n - len(keep)} lines cut)')

if '--write' in sys.argv:
    open(QUEUE, 'w').write(keep_txt)
    open(ARCHIVE, 'w').write(new_arc)
    print('WROTE tasks/queue.md, tasks/queue_archive.md')
else:
    print('DRY RUN ok -- re-run with --write to apply')
