#!/usr/bin/env python3
"""One-shot rotation for tasks/queue.md, cycle 3274 (regular slot, 3274 % 3 == 1).

`check-doc-size` read tasks/queue.md TRIM DUE on arrival (217.9KB/1141ln,
NEGATIVE headroom -- projected 345KB at its own next-look interval, past
both the 200KB trim line and the 256KB Read cap). Deferred 7+ times since
c3266 (c3266/3267/3268/3269/3270/3271/3272/3273 all left it open, each
prioritizing a real fleet-rotation backlog item instead) -- but the growth
is compounding and this cycle's own real backlog item (varied_test on
sam-gov-opportunities-scraper) does not depend on queue.md's size, so this
cycle does the trim first (cheap, ~5 min) and still has time left for the
rotation after.

Re-derived the live CLOSED-cycle-report-block set fresh (never trust a
forwarded number): `grep -n "^- \\[.\\] \\*\\*"` over the file, by hand-read
of the first 120 lines. Counted 18 genuine "cycle N did X" report blocks,
well above the documented floor of 5 (c3240 precedent). They are NOT a
clean chronological prefix (interleaved with NEW/PARTIALLY DONE standing
items, confirmed again this cycle at lines 86-98: a `CORRECTED AND CLOSED
c3265` block and the c3266/c3267 doc-trim HANDOFF note itself, which is
left live and updated in place rather than archived since it IS this
task's own in-progress record).

Two provably safe ranges cut this cycle, each bounded by a blank line and
a non-report item on both sides (verified by direct sed -n read, not
assumed):
  (21, 85)  -- 7 contiguous blocks: CLOSED c3263, c3262, c3261, c3260,
              c3259, c3257, c3256. Line 20 blank (end of `NEW c3268`
              TRIVIAL item), line 21 starts `CLOSED c3263`, line 85 blank,
              line 86 starts `CORRECTED AND CLOSED c3265` (kept live).
  (99, 100) -- 1 isolated block: CLOSED c3264. Line 98 blank (end of the
              c3266/c3267 handoff note, kept live), line 99 is the whole
              block, line 100 blank, line 101 starts `CLOSED c3252` (kept
              live).

HAZARD GREP RAN FIRST (same two-pass method as every prior *q trim):
  (a) `grep -rn "see tasks/queue.md\\|tasks/queue.md, cycle" bin actors
      site notes state` -> only the two long-standing false positives
      (`bin/store-rank:152`, `bin/git-maintain:24`), both pre-existing and
      unrelated to any cycle number in this cut (same conclusion every
      prior trim has reached).
  (b) by-name grep for c3263/c3262/c3261/c3260/c3259/c3257/c3256/c3264
      across `bin actors site` -> every hit lives inside a dead
      `bin/_trimNNNNs.py`/`bin/_triageNNNN.py` one-shot script's own
      docstring (`_triage3269.py`, `_triage3261.py`, `_triage3258.py`,
      `_trim3266s.py`, `_trim3267q.py`) -- historical narrative ABOUT that
      cycle's work, never a live pointer INTO this file. Same false-
      positive class the c3108/c3172/c3267 precedents already ruled on.

No live cross-reference into either cut range. Archived VERBATIM, in
original (newest-first) file order, prepended to the top of
tasks/queue_archive.md per the standing format.

Usage:  python3 bin/_trim3274q.py           # dry run, asserts only
        python3 bin/_trim3274q.py --write   # apply
"""
import sys

QUEUE = 'tasks/queue.md'
ARCHIVE = 'tasks/queue_archive.md'
CYCLE = 3274

CUTS = [(21, 85), (99, 100)]

orig = open(QUEUE).read().split('\n')
n = len(orig)

cut_idx = set()
for s, e in CUTS:
    assert 1 <= s <= e <= n, (s, e)
    for i in range(s, e + 1):
        assert i not in cut_idx, f'overlapping cut ranges at line {i}'
        cut_idx.add(i)

for s, e in CUTS:
    assert orig[s - 1].startswith('- [ ] ') or orig[s - 1].startswith('- [x] '), \
        f'range {s}-{e} does not start on an item head: {orig[s-1][:60]!r}'
    assert orig[e - 1].strip() == '', \
        f'range {s}-{e} does not end on a blank separator: {orig[e-1][:60]!r}'
    if e < n:
        nxt = orig[e]
        assert nxt.startswith('- [ ] ') or nxt.startswith('- [x] '), \
            f'line after range {s}-{e} is not an item head: {nxt[:60]!r}'
    prev = orig[s - 2]
    assert prev.strip() == '', f'line before range {s}-{e} is not blank: {prev[:60]!r}'

# Range (21,85) is a deliberate 7-block span; (99,100) is a single block.
EXPECTED_HEAD_COUNT = {(21, 85): 7, (99, 100): 1}
for s, e in CUTS:
    heads = [i for i in range(s, e + 1)
             if orig[i - 1].startswith('- [ ] ') or orig[i - 1].startswith('- [x] ')]
    assert len(heads) == EXPECTED_HEAD_COUNT[(s, e)], (s, e, heads)

cut_lines = []
for s, e in CUTS:
    cut_lines.extend(orig[s - 1:e])

kept = [ln for i, ln in enumerate(orig, start=1) if i not in cut_idx]

# losslessness: every original line is either kept or in cut_lines, no duplication/loss
assert len(kept) + len(cut_lines) == n
multiset_orig = sorted(orig)
multiset_rejoined = sorted(kept + cut_lines)
assert multiset_orig == multiset_rejoined, 'multiset identity failed'

n_blocks = sum(1 for s, e in CUTS for ln in [orig[s - 1]] if True)
header = (
    f"## Archived by cycle {CYCLE} trim (regular slot, {CYCLE} % 3 == 1; "
    f"check-doc-size TRIM DUE at 217.9KB/1141ln, negative headroom, deferred "
    f"7+ times since c3266). 8 CLOSED cycle-report blocks archived verbatim "
    f"in two ranges: CLOSED c3263, c3262, c3261, c3260, c3259, c3257, c3256 "
    f"(one contiguous span) and CLOSED c3264 (isolated). Newest-first below, "
    f"same order as the source file, restoring queue.md's live CLOSED count "
    f"from 18 to 10, still well above the floor of 5."
)

print(f"orig lines: {n}")
print(f"cut lines total: {len(cut_lines)}")
print(f"kept lines: {len(kept)}")
print("header:", header)

if '--write' in sys.argv:
    with open(QUEUE, 'w') as f:
        f.write('\n'.join(kept))

    old_archive = open(ARCHIVE).read()
    new_block = header + '\n\n' + '\n'.join(cut_lines) + '\n\n'
    with open(ARCHIVE, 'w') as f:
        f.write('\n' + new_block + old_archive.lstrip('\n'))
    print("WROTE.")
else:
    print("DRY RUN ONLY -- pass --write to apply.")
