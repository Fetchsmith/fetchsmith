#!/usr/bin/env python3
"""One-shot queue.md trim for cycle 3188 (Regular slot, 3188 % 3 == 2).

`check-doc-size` was run by hand after this cycle's STATUS/queue writes (it is
not on its own due-cycle) and reported tasks/queue.md **TRIM DUE** at
182.4KB/1251ln -- before c3188's own block -- with only ~3 cycles of headroom
at +5440 B/cycle and a projected **310KB at the next look**, past both the
200KB trim line and the 256KB Read cap. Same call c3164 and c3172 made in a
regular slot: three cycles is thinner than the rotation can coast on, and a
queue.md over the Read cap cannot be read at all.

Counted fresh (never assumed -- the c3084 interim RULE 6b):
`grep -c '^- \\[ \\] \\*\\*CLOSED c3'` -> **13** live cycle blocks against the
floor of 5. c3172's rotation left 5 (c3171..c3168) and sixteen cycles have
landed since with only that one outbound trim.

KEEP the newest FIVE (c3188, c3187, c3186, c3185, c3184) -- exactly the floor,
not four: unlike c3172/c3144 this script runs AFTER c3188 has already prepended
its own block, so there is nothing still to land this cycle.

Survivors: c3188, c3187, c3186, c3185, c3184.
Archived (7): c3182, c3181, c3180, c3179, c3178, c3177, c3176.
(`CLOSED c3183` is not in the live file at all -- it never had a CLOSED block
here, only a STATUS.md block, so it is not part of this cut. Noted because
line 169 cites it in the same provenance list as blocks that ARE being cut.)

**RULE 7: this is a ONE-range cut.** Unlike c3172's six ranges, no live open
item is interleaved anywhere in the span: lines 69..144 are seven consecutive
CLOSED blocks and the first live open item, `NEW c3176`, sits at line 145
immediately after. Verified by listing every `- [ ]`/`- [x]` head in the range
(must be exactly the 7 CLOSED heads, nothing foreign).

RULE 1/8 hazard grep ran BEFORE the cut, all three passes, hits READ not
counted:
 (a) `grep -rn "see tasks/queue.md\\|tasks/queue.md, cycle" bin actors site
     notes state` -> every hit is a PRIOR TRIM SCRIPT's own prose about the
     rule, the STANDING.md/LEARNINGS.md statement of the rule itself,
     `bin/store-rank:152` (generic, no cycle named), or `bin/git-maintain:24`
     (the unrelated cycle-1972 item c3117/c3120/c3172 all re-cleared). None is
     a live pointer into a block in the cut set.
 (b) bare-cycle sweep `c3176|c3177|c3178|c3179|c318[0-2]` over
     `bin actors site notes state` (excluding archives and prior _trim/_rec
     scripts) -> narrative provenance only: `state/audit_dates.json` audit
     notes (self-contained, they never defer to queue.md), `state/
     fleet_checks.json` notes, LEARNINGS.md's own entries for those cycles, and
     STATUS.md's own blocks (which rotate independently into STATUS_ARCHIVE.md
     and are untouched here).
 (c) the LEARNINGS.md:131 refinement (the standing greps are tuned to `see
     tasks/queue.md` and can miss a block addressed BY NAME): swept every
     SURVIVING queue line for the 7 cut cycle ids. 12 hits, all read, and
     **none is a directional pointer** -- no "see ... below"/"above" anywhere in
     the set, which is what c3172 had to repair six of. Four are references to
     the LIVE open item `NEW c3176` (line 145, excluded from the cut, so those
     stay correct); the rest are narrative precedent mentions ("per c3182/
     c3174", "the c3167/c3182 precedent", "due ~c3181", "c3181 already had to
     correct c3180") or parenthetical provenance labels in `NEW c3168
     findings`'s already-closed list at line 169 ("(CLOSED c3182)",
     "(CLOSED c3178)", "(CLOSED c3179)", "(CLOSED c3177)"). That list already
     cites `CLOSED c3183`, whose block has never been live in this file, so the
     label convention is independent of whether the block is live -- no repair
     needed, and POINTER_FIXES is therefore empty rather than omitted.

RULE 4 checked -- pure rotation, nothing retired here. `NEW c3176` (the
`vocab-screen` cadence registration) is still open and is deliberately kept
live. `NEW (c2478)` is deadline-guarded to 2026-11-15, which is TOMORROW
relative to this cycle -- leave it; the first cycle dated 2026-11-15+ takes it.

Dry-run by default; pass --write to apply.
"""
import collections
import sys

QUEUE = '/root/agent/tasks/queue.md'
ARCHIVE = '/root/agent/tasks/queue_archive.md'

# (start, end) 1-indexed inclusive, ending on the block's trailing blank
RANGES = [(69, 144)]

EXPECT_HEADS = {
    69: '- [ ] **CLOSED c3182',
    81: '- [ ] **CLOSED c3181',
    93: '- [ ] **CLOSED c3180',
    107: '- [ ] **CLOSED c3179',
    117: '- [ ] **CLOSED c3178',
    129: '- [ ] **CLOSED c3177',
    139: '- [ ] **CLOSED c3176',
}
EXPECT_BEFORE = {69: ''}                       # blank separator before the range
EXPECT_AFTER = {144: '- [ ] **NEW c3176'}      # the live line the range stops short of
WANT_REMAINING = ['c3188', 'c3187', 'c3186', 'c3185', 'c3184']
CUT_IDS = ['c3182', 'c3181', 'c3180', 'c3179', 'c3178', 'c3177', 'c3176']
# live open items that must survive untouched (sampled across the whole file)
STRADDLERS = ('- [ ] **NEW c3176', '- [ ] **NEW c3168 (handoff',
              '- [ ] **NEW c3168 findings', '- [ ] **NEW c3167 (handoff',
              '- [ ] **NEW c3162 (MEDIUM)', '- [ ] **NEW c3148',
              '- [ ] **NEW c3046')

HEADER = (
    '## Archived by cycle 3188 trim (Regular slot, 3188 % 3 == 2; `check-doc-size` run by hand '
    'after this cycle\'s writes reported tasks/queue.md **TRIM DUE** at 182.4KB/1251ln with only '
    '~3 cycles of headroom at +5440 B/cycle -- projected 310KB at the next look, past both the '
    '200KB trim line and the 256KB Read cap -- so this regular slot absorbed the trim instead of '
    'handing it on, exactly as c3164 and c3172 did. **THIRTEEN** live CLOSED blocks counted fresh '
    'against the floor of 5: c3172 was the last rotation and sixteen cycles have landed since. '
    'The newest FIVE are kept -- exactly the floor, not four, because unlike c3172/c3144 this '
    'script runs AFTER c3188 prepended its own block, so nothing is still to land this cycle) -- '
    '`CLOSED c3182`, `CLOSED c3181`, `CLOSED c3180`, `CLOSED c3179`, `CLOSED c3178`, '
    '`CLOSED c3177`, `CLOSED c3176` archived verbatim, in original file order, as ONE contiguous '
    'range: no live open item is interleaved in the span (the first one, `NEW c3176`, sits '
    'immediately after it and stays live). `CLOSED c3183` is absent from this cut because it was '
    'never live in this file -- it only ever had a STATUS.md block, though line 169\'s provenance '
    'list cites it alongside blocks that ARE cut, which is why that list needed no repair.\n'
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
assert total_heads == 7, f'RULE 7: {total_heads} heads in the cut set, wanted 7'

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

# --- confirm every live open item sampled survives untouched ---
for survivor in STRADDLERS:
    assert any(l.startswith(survivor) for l in keep), f'live open item lost: {survivor}'

arc_before = open(ARCHIVE).read()
sep = '' if arc_before.endswith('\n\n') else ('\n' if arc_before.endswith('\n') else '\n\n')
new_arc = arc_before + sep + HEADER + '\n' + moved_txt + '\n'

# --- losslessness: every non-blank original line is still findable ---
for l in lines:
    if l.strip():
        assert l in keep_txt or l in new_arc, f'LINE LOST: {l[:100]}'

# RULE 1/8: no POINTER_FIXES this cycle -- pass (c) of the hazard grep found no
# directional pointer ("see ... above/below") into any cut block, only narrative
# mentions and parenthetical provenance labels. Kept explicit rather than omitted
# so the next trim can see the pass ran and came back empty.
POINTER_FIXES = []
print(f'  pointers OK  {len(POINTER_FIXES)} repairs needed (no directional ref into a cut block)')
print('  lossless OK  every non-blank original line present in live+archive')
print(f'  RULE 7 OK   exactly 7 item heads across {len(RANGES)} range, all our own blocks')
print(f'  straddle OK  all {len(STRADDLERS)} sampled live open items still live')
print(f'  floor OK    5 live blocks remain: {WANT_REMAINING} (exactly the floor)')
print(f'  queue.md: {len(orig)}B/{n}ln -> {len(keep_txt)}B/{len(keep)}ln '
      f'({len(orig) - len(keep_txt)}B, {n - len(keep)} lines cut)')

if '--write' in sys.argv:
    open(QUEUE, 'w').write(keep_txt)
    open(ARCHIVE, 'w').write(new_arc)
    print('WROTE tasks/queue.md, tasks/queue_archive.md')
else:
    print('DRY RUN ok -- re-run with --write to apply')
