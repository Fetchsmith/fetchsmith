#!/usr/bin/env python3
"""One-shot hoist-then-cut for tasks/queue.md, cycle 3240 (QUALITY slot, 3240 % 3 == 0).

WHY THIS IS A RULE 4 PASS, NOT A ROTATION (read before cloning):
  `check-doc-size` read `tasks/queue.md` TRIM DUE (149.7KB/1065ln, proj. 277KB at the next
  24c look).  The usual newest-5 cycle-report rotation is NOT AVAILABLE this cycle: counted
  fresh per STANDING RULE 6b, the live file holds EXACTLY FIVE cycle-report blocks
  (c3237/c3236/c3235/c3234/c3233, L1-37) -- already at the documented floor.  c3237's handoff
  said as much ("queue.md's real mass is in standing NEW backlog items, not cycle-report
  blocks") and named a RULE 4 tail pass as the deeper fix.  So this script retires/compresses
  CONSUMED non-cycle-report closure blocks that the rotation structurally cannot reach.

RULE 1/8 HAZARD GREP RAN FIRST, THREE PASSES:
  (a) `grep -rn "see tasks/queue.md\\|tasks/queue.md, cycle" bin actors site notes state`
      -> only the 7 standing false positives (`bin/store-rank:152`, `bin/git-maintain:24`,
      STANDING.md's own rule text, LEARNINGS' own history, `state/audit_dates.json`'s
      enum_audit_note, `state/fleet_checks.json`'s c3162 note, `state/mode_scope_allow.json`'s
      `_readme`) plus prior `bin/_trim*q.py` docstrings.  None names a cut block.
  (b) the by-name pass (`c3220b`, `CLOSED c3219`, `CLOSED c3228`, `CLOSED c3238`, `NEW c3088`,
      `DONE at c3162`) over the whole repo -- this is the pass LEARNINGS:189 warns the standard
      grep misses, and it found THREE real hits in `notes/LEARNINGS.md`:
        * :6571 "Full measurement citations: `tasks/queue.md`, `CLOSED c3227` under
          `NEW c3220b`" -- a REAL durable measurement citation into a block being cut.
          FIXED IN PLACE BEFORE THIS SCRIPT RAN (RULE 8: "a stale instruction outranks a tidy
          archive -- fix the citation first, then cut"); it now points at this cycle's archive
          header.
        * :6535 and :6586 cite `CLOSED c3219` as an ILLUSTRATION of the pointer-rot / regex
          over-match pattern, inside dated cycle-3225/3228 narrative.  Deliberately NOT edited:
          they are narrative ABOUT a past cycle's experience (the standing-hazard precedent for
          leaving those alone), the lessons stand without the block, and cutting c3219 actually
          REMOVES the over-match trap :6535 warns future rotations about.
  (c) the c3060 second grep ON the live queue for pointers between surviving items and cut
      ones -> `NEW c3167` (L56-59) cites "option 2 is CLOSED c3228, see below" and "See
      `CLOSED c3228` above".  NOT dangled: c3228 is COMPRESSED to a stub, not removed, and the
      stub deliberately keeps the literal anchor `RESOLVED c3228`.  No other live item cites a
      cut block.

WHAT IS CUT, each verified by reading its closure IN FULL this cycle (the RULE 4 requirement):
  L38-43  12167B  `CLOSED c3238` / `NEW c3220b` -- fleet-wide sort_order sweep, COMPLETE 4/4,
                  0 shippable fixes.  Its own head says "kept verbatim below for the method";
                  the method is preserved VERBATIM in the archive and the stub names all four
                  outcomes + the cheapest first step, so nothing is re-measured.  -> STUB
  L49-55   5001B  `RESOLVED c3228` -- competitor-claims backlog empty fleet-wide, 0/1044,
                  fault-injection-proven.  Re-open trigger + cadence + the earned standing rule
                  are carried into the stub; the four-rule method goes to the archive.  -> STUB
  L62-63    386B  `DONE at c3162` -- consumed; the vendor pivot is now a registered standing
                  check (`bin/check-vendor-catalogue`, live in state/fleet_checks.json).  -> CUT
  L72-73   4144B  `CLOSED c3219` -- "all 5 named picks below are DONE, stop pointing future
                  cycles here".  Fully consumed by its own text.  -> CUT
  L80-81   1116B  `CLOSED c3238` / `NEW c3088` -- the already-moot handoff c3238 closed.  -> CUT

NOT TOUCHED, on purpose (read, judged live, leaving a record so the next pass need not re-read):
  L792 `SETTLED c3216` (1948B) -- its own text says "Keep this stub for the tripwire", and the
       tripwire (`store-anon-rank`'s "queries unrankable because paging is gone: N") is live.
  L82-87 `DECIDED c3081` (4773B) -- a DEFER decision carrying two live named re-open triggers.
  L44-48 `PARTIALLY DONE ... NEW c3162` (7191B) -- the live triage backlog's own progress record.

MARGIN ARITHMETIC (RULE 4): gross cut 22814B, stubs add ~2.5KB, net ~-20.3KB -> ~129KB, which
lands inside the 120-134KB band `MEASURED c3000` documents as this file's steady state.  Per
that same measurement do NOT expect to escape TRIM DUE for 24 cycles: no partition of this file
can, the checker's projection is a worst case, and the only real lever is writing less per cycle.

Usage:  python3 bin/_trim3240q.py           # dry run, asserts only
        python3 bin/_trim3240q.py --write   # apply
"""
import sys

QUEUE = 'tasks/queue.md'
ARCHIVE = 'tasks/queue_archive.md'
CYCLE = 3240

# (start, end) 1-indexed INCLUSIVE, each range = item head .. its trailing blank separator.
# Verified against the live file before writing: heads at 38/49/62/72/80, next heads at
# 44/56/64/74/82, separators at 43/55/63/73/81.
CUTS = [(38, 43), (49, 55), (62, 63), (72, 73), (80, 81)]

# Replacement text for the two COMPRESSED ranges. Keyed by range start.
# NOTE: these break multiset identity BY DESIGN, so they are asserted separately.
STUBS = {
    38: [
        "- [x] **CLOSED c3238 -- `NEW c3220b` (MEDIUM, fleet-wide) `sort_order` 2x-reach sweep: COMPLETE, all 4 candidates measured, 0 shippable fixes found anywhere. The full 12.2KB record -- the per-endpoint method plus the `CLOSED c3227`/`c3229`/`c3230`/`c3238` measurements -- is archived VERBATIM in `queue_archive.md` under `## Archived by cycle 3240`** (compressed there by c3240's RULE 4 pass; `notes/LEARNINGS.md` cycle-3227/3229/3230/3238 entries carry the durable lessons). **The four outcomes, so no future cycle re-measures them:** `nih-reporter-scraper`/`projects` (c3227 -- mechanism valid, but the one tie-free sort key `appl_id` blows the run timeout at real offset depth; unshippable), `fda-recall-scraper` (c3229 -- mechanism clean AND fast, but the `MAX_SKIP` ceiling condition it would rescue never fires at real recall volumes), `apple-podcasts-scraper`/`app-store-reviews-scraper` RSS (c3230 -- NOT APPLICABLE: two non-reversible named orders, plus a hard server-side page-10 depth cap), `steam-reviews-scraper` store-search (c3238 -- NOT APPLICABLE: no sort knob exists at all, a bogus value returns byte-identical results). **Do NOT re-open any of these four.** Re-read the archived method only if a NEW offset-walled Actor ships -- and lead with c3230/c3238's cheap existence check (one bogus-value curl), which alone killed 2 of the 4 before any expensive symmetry proof.",
        "",
    ],
    49: [
        "- [ ] **RESOLVED c3228 -- the `NEW c3168` competitor-claims backlog is EMPTY fleet-wide: 1,044 user-count claims / 299 paragraphs checked, 0 STALE / 0 UNDATED / 0 DISAGREE / 0 unresolvable (2026-11-15), the first fully clean fleet reading on record -- and fault-injection-proven in BOTH directions (the count guard and the paragraph/date guard each tripped on a local-only README edit; both reverted, both re-ran clean, no build, READMEs byte-identical to HEAD). The 5.0KB record -- the four-rule hand-edit method, the 10 expected informational `DISCLOSED` lines, and the fault-injection detail -- is archived VERBATIM in `queue_archive.md` under `## Archived by cycle 3240`** (compressed there by c3240's RULE 4 pass). **Cadence: `check-competitor-claims` `last_cycle 3228`, next due c3372.** If you run it FLEET-WIDE, record it with `--ran` -- the tracker sat 129 cycles pessimistic because the real fleet runs at c3182/c3190/c3191 never did, and `--only` runs correctly do not count. **Re-open trigger: a fresh fleet-wide sweep flagging a non-`DISCLOSED` line. Nothing else -- do not re-derive a backlog from this stub or from archived handoff prose, run the checker.** The standing rule this item earned (also homed in `notes/LEARNINGS.md`, cycle 3228): never act on a competitor-claims target named in a handoff without re-confirming it via `--only <slug>` first (seconds, read-only) -- this file's pointers rot faster than its content, because content is written by the cycle that owns it while pointers are written by cycles that do not.",
        "",
    ],
}

orig = open(QUEUE).read().split('\n')
n = len(orig)

# --- partition asserts -------------------------------------------------------
cut_idx = set()
for s, e in CUTS:
    assert 1 <= s <= e <= n, (s, e)
    for i in range(s, e + 1):
        assert i not in cut_idx, f'overlapping cut ranges at line {i}'
        cut_idx.add(i)

# Boundary shape: every range starts on a top-level item head and ends on a blank
# separator, and the line after each range is itself a top-level head (or EOF).
for s, e in CUTS:
    assert orig[s - 1].startswith('- [ ] ') or orig[s - 1].startswith('- [x] '), \
        f'range {s}-{e} does not start on an item head: {orig[s-1][:60]!r}'
    assert orig[e - 1].strip() == '', \
        f'range {s}-{e} does not end on a blank separator: {orig[e-1][:60]!r}'
    if e < n:
        nxt = orig[e]
        assert nxt.startswith('- [ ] ') or nxt.startswith('- [x] '), \
            f'line after range {s}-{e} is not an item head: {nxt[:60]!r}'

# STANDING RULE 7, re-expressed for this file's shape (per _trim3048q.py's adaptation):
# cycle-report blocks and closure blocks both head with `- [ ] `/`- [x] `, so "no `- [ ] ` in
# the cut" is impossible. The real protection is: EXACTLY ONE top-level head per range, and it
# is that range's own head -- i.e. no live sibling item is being swept along.
for s, e in CUTS:
    heads = [i for i in range(s, e + 1)
             if orig[i - 1].startswith('- [ ] ') or orig[i - 1].startswith('- [x] ')]
    assert heads == [s], f'range {s}-{e} contains extra top-level item heads: {heads}'

# Each cut range's head must name a CONSUMED state, never a bare open NEW item.
CONSUMED = ('CLOSED', 'RESOLVED', 'DONE at', 'SETTLED', 'DECIDED', 'PARTIALLY DONE')
for s, e in CUTS:
    assert any(k in orig[s - 1] for k in CONSUMED), \
        f'range {s}-{e} head is not a consumed closure block: {orig[s-1][:80]!r}'

# The five cycle-report blocks (L1-37) must be untouched -- they are already at the floor.
assert not (cut_idx & set(range(1, 38))), 'cut must not touch the live cycle-report window'
reports = [i for i in range(1, 38)
           if orig[i - 1].startswith('- [ ] **CLOSED c3') or orig[i - 1].startswith('- [x] **CLOSED c3')]
assert len(reports) == 5, f'expected 5 live cycle-report blocks at the floor, found {len(reports)}'

# --- build the three halves --------------------------------------------------
kept, archived = [], []
for i, line in enumerate(orig, start=1):
    if i in cut_idx:
        archived.append(line)
        start = next((s for s, e in CUTS if s == i), None)
        if start is not None and start in STUBS:
            kept.extend(STUBS[start])
    else:
        kept.append(line)

stub_lines = [l for s in STUBS.values() for l in s]

# Multiset identity: every original non-blank line is in kept+archived exactly as often as
# before, once the deliberately-new stub text is discounted.
from collections import Counter
c_orig = Counter(l for l in orig if l.strip())
c_new = Counter(l for l in kept + archived if l.strip())
c_stub = Counter(l for l in stub_lines if l.strip())
assert c_new - c_stub == c_orig, 'LOSSLESS CHECK FAILED: kept+archived != original'
assert all(c_orig[l] == 0 for l in c_stub), 'stub text collides with existing lines'
# And the stub text really is new, asserted separately as the method requires.
for l in stub_lines:
    if l.strip():
        assert l not in orig, f'stub line already present in original: {l[:60]!r}'
        assert sum(1 for k in kept if k == l) == 1, 'stub line must appear exactly once live'

gross = sum(len(orig[i - 1]) + 1 for i in sorted(cut_idx))
stub_b = sum(len(l) + 1 for l in stub_lines)
before = sum(len(l) + 1 for l in orig)
after = sum(len(l) + 1 for l in kept)

print(f'{QUEUE}: {before/1024:.1f}KB/{len(orig)}ln -> {after/1024:.1f}KB/{len(kept)}ln')
print(f'  ranges cut : {CUTS}')
print(f'  gross cut  : {gross}B ({len(cut_idx)} lines)')
print(f'  stubs add  : {stub_b}B ({len([l for l in stub_lines if l.strip()])} new lines)')
print(f'  net        : {(after-before)/1024:+.1f}KB')
print(f'  archive    : +{sum(len(l)+1 for l in archived)}B under "## Archived by cycle {CYCLE}"')
print('  ALL ASSERTS PASSED')

if '--write' not in sys.argv:
    print('\ndry run -- pass --write to apply')
    sys.exit(0)

prior_archive = open(ARCHIVE).read()
header = (f'\n\n## Archived by cycle {CYCLE} (from tasks/queue.md -- RULE 4 pass: consumed '
          f'closure blocks the newest-5 cycle-report rotation cannot reach, since that window '
          f'was already at its floor of 5. `NEW c3220b`/`CLOSED c3238` and `RESOLVED c3228` '
          f'are COMPRESSED (stubs left live naming their outcomes, cadence and re-open '
          f'triggers); `DONE at c3162`, `CLOSED c3219` and `CLOSED c3238`/`NEW c3088` are '
          f'fully retired as consumed. Newest-first, verbatim.)\n\n')
with open(ARCHIVE, 'w') as f:
    f.write(prior_archive + header + '\n'.join(archived) + '\n')
with open(QUEUE, 'w') as f:
    f.write('\n'.join(kept))

# post-write verification
live = open(QUEUE).read()
arch = open(ARCHIVE).read()
assert arch.startswith(prior_archive), 'prior archive content was modified'
for s, e in CUTS:
    if s not in STUBS:
        assert orig[s - 1] not in live, f'cut head still live: {orig[s-1][:60]!r}'
    assert orig[s - 1] in arch, f'cut head missing from archive: {orig[s-1][:60]!r}'
assert 'RESOLVED c3228' in live, 'NEW c3167 pointer anchor was dangled'
print('\nWROTE both files; post-write verification passed.')
