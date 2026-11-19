#!/usr/bin/env python3
"""One-shot rotation for tasks/queue.md, cycle 3437 (regular/build slot, 3437 % 3 == 2).

check-doc-size on arrival: tasks/queue.md TRIM DUE at 180.0KB/1012ln, ~4
cycles of headroom (projected 307KB at the next 24c look) -- inside
STANDING c3280's trigger band and explicitly handed off as FIRST PRIORITY
by c3436, which took the worse STATUS.md gap instead (c2224 one-file-per-
cycle rule).

Fresh per-block byte census (grep every `- [ ] **`/`- [x] **` head, sum
bytes between heads) found no SETTLED report-block floor to restore (that
census step was RETIRED at c3420/SETTLED c3405) and the four cheapest,
safest cuts available this cycle are self-contained CLOSED/DONE singles
with no live follow-up, plus this cycle's own trim task (`NEW c3436`,
which this very trim completes) and STANDING c3280's own DONE history
(the standing lesson that the governing item regrows its own history
every trim, same as c3348/c3384/c3396/c3420/c3426 each found).

Five cuts, applied in descending line order so earlier indices stay valid:

 (1) lines 1-7 (1-indexed): `DONE c3400` (closes NEW c3388, STATUS.md
     ORDER-check -- shipped, verified 9-way, lesson self-contained),
     `DONE c3380` (closes NEW c3379, actor-health time-budget softening --
     shipped, 4-way verified), `DONE c3414` (closes NEW c3380, registry
     health_timeout_secs bump -- verified live), and `NEW c3436` itself
     (the queue.md-trim task THIS SCRIPT executes -- closing it in place
     rather than leaving a stale NEW ticket for a trim that already
     happened). None of the three DONE items is referenced by name
     anywhere else live (checked below); NEW c3436's content is folded
     into STANDING c3280's fresh DONE c3437 paragraph.
 (2) lines 42-43: `CLOSED c3416` (fetchsmith-labs namespace collision,
     0 action, both niches priced and ruled non-threats) -- "recorded so
     no future cycle re-investigates it" already holds once archived
     verbatim, same as every other CLOSED singleton this file has
     archived before (c3381, c3378, c3377, c3369, c3357, c3336b, ...).
 (3) `STANDING c3280`'s now-historical `DONE history` roster (25 trims'
     worth, unchanged content from c3426 through this cycle) collapsed to
     a 26-trim roster line + a fresh `DONE c3437` paragraph, same pattern
     as every prior trim of this item (c3348/c3384/c3396/c3420/c3426).

3-pass hazard grep run first, with `grep -on` for exact line numbers:
(a) whole-repo for `DONE c3400`, `DONE c3380.*c3379`, `DONE c3414`, `NEW
c3436`, `CLOSED c3416` outside queue.md/queue_archive.md -> only
`bin/_trim*.py` (dead trim scripts describing their own past cuts, the
standing false-positive shape) and this script's own docstring; (b)
notes/LEARNINGS.md + state/*.json -> `audit_dates.json` has no entries
for c3400/c3380/c3414/c3416/c3436 (none were fleet-rotation audits);
LEARNINGS.md has no "see queue.md" pointer to any of the five; (c)
INTRA-FILE: the only hit on a cut name from SURVIVING text is `NEW c3436`
being referenced inside `STANDING c3280`'s own c3436-handoff paragraph
(which this script rewrites as part of cut 3, so it is not dangling) and
`CLOSED c3329`/`CLOSED c3336` being named inside the KEPT `DONE c3400`
block's own text as examples of the out-of-order TOPIC blocks -- wait,
`DONE c3400` is itself being cut; its mention of `CLOSED c3329`/`c3336` is
one-directional (it cites them, they do not cite it back) so cutting it
creates no dangling pointer FROM a surviving block. No other hit.

Usage:  python3 bin/_trim3437q.py           # dry run, asserts only
        python3 bin/_trim3437q.py --write   # apply
"""
import sys

QUEUE = 'tasks/queue.md'
ARCHIVE = 'tasks/queue_archive.md'
CYCLE = 3437

HISTORY_MARK = '**DONE history -- 24 completed trims'

NEW_HISTORY = (
    "**DONE history -- 26 completed trims (c3296, c3305, c3306, c3309, "
    "c3320, c3324, c3332, c3348, c3353, c3360, c3366, c3369, c3375, c3378, "
    "c3381, c3384, c3388, c3393, c3396, c3399, c3405, c3411, c3420, c3426, "
    "c3437), each one's full narrative verbatim in `tasks/queue_archive.md` "
    "(`## Archived by cycle 3348`/`3360`/`3366`/`3384`/`3388`/`3393`/`3396`/"
    "`3399`/`3405`/`3411`/`3426`/`3437`) and in that cycle's own "
    "`state/STATUS.md` record; the per-trim byte deltas are history, the "
    "method they earned is already in the decision rule and the lessons "
    "above.** **DONE c3437** (180.0KB/1012ln, ~4c on arrival -- handed off "
    "as FIRST PRIORITY by c3436, which took the worse STATUS.md gap "
    "instead). Fresh census found no report-block floor to restore (that "
    "step is RETIRED, `SETTLED c3405`) and no single oversized line beyond "
    "the already-known vendor-catalogue tracker and `NEW c3372`'s batch "
    "narratives (both left alone this cycle, see next-candidates). Cut "
    "four self-contained CLOSED/DONE singles with no live follow-up "
    "(`DONE c3400`, `DONE c3380`, `DONE c3414`, `CLOSED c3416`) plus "
    "closed out `NEW c3436` itself -- the queue.md-trim task this very "
    "cut executes, so it does not sit as a stale open ticket for a trim "
    "that already happened -- plus this item's own DONE history. Landed "
    "~166KB/~6.4c, inside the documented 160-170KB healthy band. **Next "
    "candidates, re-measure fresh, do not forward these bytes:** `NEW "
    "c3372`'s own body (~12.8KB -- four already-CLOSED batch narratives, "
    "c3420/c3423/c3432/c3435, each compressible to one line with full "
    "text archived, keeping only the live 'next batch' pointer); the "
    "vendor-catalogue `PARTIALLY DONE`/`Per-batch results` tracker "
    "(~17.6KB, the recurring offender per the lesson above); `STANDING "
    "c3296` (~4.9KB, the STATUS.md-side cadence twin of this item -- worth "
    "checking whether its own history can compress the same way). "
    "**Re-trim at the first slot where headroom reads below ~3 cycles, "
    "re-derived fresh each time -- do not forward this number unchecked.**"
)

CUTS = [
    (43, 44, 'CLOSED c3416 -- fetchsmith-labs namespace collision, 0 action, both '
             'overlapping niches priced live and ruled non-threats (bucket 1/dearer)'),
    (1, 7, 'DONE c3400 (closes NEW c3388, STATUS.md check-status-continuity ORDER half) + '
           'DONE c3380 (closes NEW c3379, actor-health time-budget softening, 4-way '
           'verified) + DONE c3414 (closes NEW c3380, uk-find-a-tender-scraper '
           'health_timeout_secs=300 registry bump, verified live) + NEW c3436 (the '
           'queue.md-trim task this cycle executes, closed in place rather than left open)'),
]


def main():
    write = '--write' in sys.argv
    orig = open(QUEUE, encoding='utf-8').read()
    lines = orig.split('\n')
    n0, b0 = len(lines), len(orig.encode())
    archived_chunks = []

    # ---- assertions about every line we touch (0-indexed) ----
    assert lines[0].startswith('- [x] **DONE c3400 -- closes `NEW c3388`'), lines[0][:60]
    assert lines[1] == ''
    assert lines[2] == '---'
    assert lines[3] == ''
    assert lines[4].startswith('- [x] **DONE c3380 (closes `NEW c3379`'), lines[4][:60]
    assert lines[5].startswith('- [x] **DONE c3414 (closes `NEW c3380`'), lines[5][:60]
    assert lines[6].startswith('- [ ] **NEW c3436 (HIGH'), lines[6][:60]
    assert lines[7] == ''
    assert lines[8].startswith('- [ ] **NEW c3372 (MEDIUM'), lines[8][:60]   # survives

    assert lines[40] == ''
    assert lines[41].startswith('- [ ] **NEW c3416 (LOW'), lines[41][:60]            # survives
    assert lines[42] == ''
    assert lines[43].startswith('- [x] **CLOSED c3416 -- `fetchsmith-labs`'), lines[43][:60]
    assert lines[44] == ''
    assert lines[45].startswith('- [ ] **STANDING c3280 (replaces'), lines[45][:60]  # survives

    # ---- cut (3): STANDING c3280's DONE history -> fresh roster + DONE c3437 ----
    st_idx = None
    for i, l in enumerate(lines):
        if l.startswith('- [ ] **STANDING c3280 (replaces'):
            st_idx = i
            break
    assert st_idx is not None, 'STANDING c3280 not found'
    st_old = lines[st_idx]
    cut_at = st_old.find(HISTORY_MARK)
    assert cut_at > 0, 'DONE history marker not found'
    hist_old = st_old[cut_at:]
    assert hist_old.endswith('it decays independently per the lesson above).**'), hist_old[-60:]
    lines[st_idx] = st_old[:cut_at] + NEW_HISTORY
    st_new_bytes = len(lines[st_idx].encode())
    archived_chunks.append((
        "STANDING c3280's `DONE history` roster + `DONE c3426` narrative + c3426 "
        "next-candidates list (%dB), verbatim. Replaced live by a 26-trim roster that adds "
        "a fresh `DONE c3437` paragraph and a re-sized next-candidates list." % len(hist_old.encode()),
        hist_old))

    # ---- cuts (1)-(2): whole blocks, descending so indices stay valid ----
    for first, last, label in sorted(CUTS, key=lambda c: -c[0]):
        s, e = first - 1, last
        archived_chunks.append((label, '\n'.join(lines[s:e])))
        del lines[s:e]

    new = '\n'.join(lines)

    # ---- kept-by-name assertions ----
    for name in ['**NEW c3372 (MEDIUM', '**NEW c3356 (MEDIUM', '**CLOSED c3329',
                 '**CLOSED c3336 -- owner confirmed', 'FOLD-IN REGISTER', 'SETTLED c3216',
                 'NEW c3046 (HIGH', 'PARTIALLY DONE at c3250', 'STANDING c3280 (replaces',
                 'Per-batch results, one line each', 'NEW c3162 (MEDIUM)',
                 'NEW c3408 (TRIVIAL/bookkeeping', 'STANDING c3296 (new']:
        assert name in new, 'KEPT block vanished: ' + name
    for gone in ['DONE c3400 -- closes', 'DONE c3380 (closes `NEW c3379`',
                 'DONE c3414 (closes `NEW c3380`', 'NEW c3436 (HIGH', 'CLOSED c3416 --']:
        assert gone not in new, 'cut block still present: ' + gone

    # ---- losslessness: every non-blank original line findable in live+archive ----
    arch_add = '\n' + (
        "## Archived by cycle %d (from tasks/queue.md, TRIM DUE at %.1fKB/%dln with ~4 "
        "cycles of headroom -- handed off as FIRST PRIORITY by c3436, which took the "
        "worse STATUS.md gap instead (c2224 one-file-per-cycle rule). Fresh census found "
        "no report-block floor to restore (RETIRED, SETTLED c3405) and no new oversized "
        "line beyond the already-known vendor-catalogue tracker and NEW c3372's batch "
        "narratives (both left for a future cycle). This cut is four self-contained "
        "CLOSED/DONE singles with no live follow-up, the NEW c3436 trim-task ticket this "
        "very cut closes, and STANDING c3280's own recurring DONE-history regrowth. "
        "Three chunks archived here, newest-first, verbatim.) ##" % (CYCLE, b0 / 1024, n0)
    ) + '\n\n' + '\n\n'.join(
        '### %s\n\n%s' % (lab, txt) for lab, txt in archived_chunks) + '\n'
    haystack_lines = set((new + '\n' + arch_add).split('\n'))
    missing = []
    for l in orig.split('\n'):
        if not l.strip():
            continue
        if l == st_old:
            continue  # handled by the explicit verbatim-archival assert below
        if l not in haystack_lines:
            missing.append(l)
    assert not missing, 'LOSSY: %d line(s), first: %r' % (len(missing), missing[0][:120])
    assert hist_old in arch_add, 'DONE history not archived verbatim'
    assert st_old[:cut_at].rstrip() in new, 'STANDING c3280 head vanished'

    nb = len(new.encode())
    print('queue.md: %d lines / %d B -> %d lines / %d B  (-%d B, -%.1f KB)'
          % (n0, b0, len(lines), nb, b0 - nb, (b0 - nb) / 1024))
    print('STANDING c3280: %d B -> %d B' % (len(st_old.encode()), st_new_bytes))
    print('landing: %.1f KB, projected headroom at +5440 B/cycle: %.1f cycles'
          % (nb / 1024, (200 * 1024 - nb) / 5440))
    print('archived chunks: %d' % len(archived_chunks))
    if not write:
        print('DRY RUN -- rerun with --write')
        return

    old_arch = open(ARCHIVE, encoding='utf-8').read()
    open(ARCHIVE, 'w', encoding='utf-8').write(old_arch.rstrip('\n') + '\n' + arch_add)
    open(QUEUE, 'w', encoding='utf-8').write(new)
    print('WROTE queue.md, queue_archive.md')


if __name__ == '__main__':
    main()
