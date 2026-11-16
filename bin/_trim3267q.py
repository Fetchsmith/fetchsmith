#!/usr/bin/env python3
"""One-shot rotation for tasks/queue.md, cycle 3267 (QUALITY slot, 3267 % 3 == 0).

`check-doc-size` read `tasks/queue.md` TRIM DUE on arrival (226.7KB/1170ln,
negative headroom) -- flagged and deferred by c3264/c3265/c3266. c3266's own
STATUS.md trim already took care of that file; this is the queue.md half
c3266 left as `NEW c3266`.

Re-derived the live cycle-report-block count fresh per STANDING RULE 6b
(never trust a forwarded number): `grep -c '^- \\[ \\] \\*\\*CLOSED c3\\|^- \\[x\\]
\\*\\*CLOSED c3'` reads 19 -- matches c3266's own bare-grep count, so that
number is confirmed, not stale. The documented floor from the c3240 precedent
is 5, so the lever IS a rotation, but the 19 blocks are NOT a simple
chronological prefix the way STATUS.md's `Updated: ... by cycle N` blocks
are -- they are interleaved with standing NEW/RESOLVED/PARTIALLY-DONE items
(e.g. `CLOSED c3264` sits BELOW `NEW c3266`, `CLOSED c3248` sits far below
`CLOSED c3234`). A single keep-newest-N cut across the whole 19 is therefore
not mechanically safe in one pass without re-deriving each boundary by hand.

This cycle does the SAFE SUBSET: one genuinely contiguous run of six
back-to-back cycle-report blocks (c3249, c3240, c3237, c3236, c3235, c3234 --
oldest six of the nineteen by cycle number) that sit as an unbroken span,
L91-136, immediately followed by a non-report item (`NEW c3220b` SWEEP
CLOSED, L137) -- plus one more isolated report block, `CLOSED c3248`
(L158-166), also bounded cleanly by non-report items on both sides. Cutting
these 7 brings the count 19 -> 12, still comfortably above the floor of 5,
and is the largest range provably safe within this cycle's time budget.
The remaining 12 (including the still-interleaved `CLOSED c3264` at L73 and
the newest block at L1) are deliberately left for the next QUALITY slot --
see the `NEW c3267` handoff this cycle adds to the live file.

RULE 1/8 HAZARD GREP RAN FIRST, THREE PASSES (full detail in STATUS.md
cycle 3267):
  (a) `grep -rn "see tasks/queue.md\\|tasks/queue.md, cycle" bin actors site
      notes state` (excluding bin/_trim*.py's own historical docstrings) ->
      only the long-standing false positives (`bin/store-rank:152`,
      `bin/git-maintain:24`, STANDING.md/LEARNINGS.md's own rule text and
      history, `state/fleet_checks.json`/`state/mode_scope_allow.json`'s
      handoff notes) -- none names a block in this cut.
  (b) by-name grep for `c3249`, `c3240`, `c3237`, `c3236`, `c3235`, `c3234`,
      `c3248` across `bin actors site notes state` -> every hit is either
      (i) that cycle's OWN entry in STATUS.md/STATUS_ARCHIVE.md/LEARNINGS.md
      (narrative ABOUT the cycle, not a pointer INTO this file, same class
      the c3180/c3266 precedent already rules on), or (ii) a code comment
      (`actors/ats-jobs-scraper/src/main.js:1163`, "see the `Remote (...)`/
      `Hybrid (...)` open gap c3248 flagged") that cites c3248 as PROVENANCE
      for a convention the code already implements inline two lines below --
      not an instruction to go read the queue block, and the gap itself is
      not open (the function strips it). Left as-is per the same precedent.
  (c) the live-queue self-grep for `CLOSED c3249`/`c3240`/`c3237`/`c3236`/
      `c3235`/`c3234`/`c3248` as literal phrases, outside the cut ranges ->
      one hit, L141 `**CLOSED c3248 (rows 59-64, ...)`, which is a DIFFERENT
      entity: a sub-bullet inside the still-live `PARTIALLY DONE at c3167...`
      item (L139-152) recording that cycle 3248 ALSO ran a vendor-catalogue
      triage round that cycle, unrelated to the Rippling `NEW c3248` build
      item being cut here -- same cycle number, two unrelated pieces of work,
      and the triage sub-bullet's content lives entirely in the kept block.
      No dangling pointer.

Usage:  python3 bin/_trim3267q.py           # dry run, asserts only
        python3 bin/_trim3267q.py --write   # apply
"""
import collections
import sys

QUEUE = 'tasks/queue.md'
ARCHIVE = 'tasks/queue_archive.md'
CYCLE = 3267

# (start, end) 1-indexed INCLUSIVE, each range = item head .. its trailing blank separator.
CUTS = [(91, 136), (158, 166)]

orig = open(QUEUE).read().split('\n')
n = len(orig)

# --- partition asserts -------------------------------------------------------
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

# Exactly one top-level head per range, EXCEPT the deliberately multi-block
# first range (91-136), which is checked separately below against the exact
# expected 6-cycle sequence.
for s, e in CUTS:
    if s == 91:
        continue
    heads = [i for i in range(s, e + 1)
             if orig[i - 1].startswith('- [ ] ') or orig[i - 1].startswith('- [x] ')]
    assert heads == [s], f'range {s}-{e} contains extra top-level item heads: {heads}'

# Each cut range's head must literally be a CLOSED cNNNN report block.
EXPECT_HEAD = {91: 'CLOSED c3249', 158: 'CLOSED c3248'}
for s, e in CUTS:
    assert EXPECT_HEAD[s] in orig[s - 1], \
        f'range {s}-{e} head does not match expected {EXPECT_HEAD[s]!r}: {orig[s-1][:80]!r}'

# The six-block contiguous span inside the first range: c3249/c3240/c3237/c3236/c3235/c3234.
inner_heads = [i for i in range(91, 137)
               if orig[i - 1].startswith('- [ ] ') or orig[i - 1].startswith('- [x] ')]
assert len(inner_heads) == 6, f'expected 6 report blocks in L91-136, found {len(inner_heads)}'
for i, cyc in zip(inner_heads, ['c3249', 'c3240', 'c3237', 'c3236', 'c3235', 'c3234']):
    assert f'CLOSED {cyc}' in orig[i - 1], f'line {i} does not head {cyc}: {orig[i-1][:60]!r}'

# --- build the two halves ----------------------------------------------------
kept, archived = [], []
for i, line in enumerate(orig, start=1):
    (archived if i in cut_idx else kept).append(line)

# Lossless: every original non-blank line present exactly once across kept+archived.
c_orig = collections.Counter(l for l in orig if l.strip())
c_new = collections.Counter(l for l in kept + archived if l.strip())
assert c_new == c_orig, 'LOSSLESS CHECK FAILED: kept+archived != original'

gross = sum(len(orig[i - 1]) + 1 for i in sorted(cut_idx))
before = sum(len(l) + 1 for l in orig)
after = sum(len(l) + 1 for l in kept)

print(f'{QUEUE}: {before/1024:.1f}KB/{len(orig)}ln -> {after/1024:.1f}KB/{len(kept)}ln')
print(f'  ranges cut : {CUTS}  (7 report blocks: c3249/c3240/c3237/c3236/c3235/c3234/c3248)')
print(f'  gross cut  : {gross}B ({len(cut_idx)} lines)')
print(f'  archive    : +{sum(len(l)+1 for l in archived)}B under "## Archived by cycle {CYCLE}"')
print('  ALL ASSERTS PASSED')

if '--write' not in sys.argv:
    print('\ndry run -- pass --write to apply')
    sys.exit(0)

prior_archive = open(ARCHIVE).read()
header = (f'\n\n## Archived by cycle {CYCLE} (from tasks/queue.md -- newest-5-floor-style '
          f'rotation of the one contiguous span available: 7 of the 19 live CLOSED-cNNNN '
          f'report blocks, cycles c3249/c3240/c3237/c3236/c3235/c3234 (one unbroken L91-136 '
          f'span) plus the isolated c3248 block (L158-166). The remaining 12 report blocks '
          f'are interleaved with live standing items and were deliberately left for the next '
          f'QUALITY slot -- see `NEW c3267` in tasks/queue.md. Verbatim, in original order.)\n\n')
with open(ARCHIVE, 'w') as f:
    f.write(prior_archive + header + '\n'.join(archived) + '\n')
with open(QUEUE, 'w') as f:
    f.write('\n'.join(kept))

live = open(QUEUE).read()
arch = open(ARCHIVE).read()
assert arch.startswith(prior_archive), 'prior archive content was modified'
for s, e in CUTS:
    assert orig[s - 1] not in live, f'cut head still live: {orig[s-1][:60]!r}'
    assert orig[s - 1] in arch, f'cut head missing from archive: {orig[s-1][:60]!r}'
print('\nWROTE both files; post-write verification passed.')
