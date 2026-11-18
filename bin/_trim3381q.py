#!/usr/bin/env python3
"""One-shot rotation for tasks/queue.md, cycle 3381 (QUALITY/GROWTH slot, 3381 % 3 == 0).

check-doc-size on arrival: tasks/queue.md TRIM DUE at 188.1KB/1033ln, ~2
cycles of headroom -- inside STANDING c3280's ~3-cycle trigger band.

Fresh per-block census (grep every `- [ ]`/`- [x] **` head) found 7 live
per-cycle "slot" report blocks (CLOSED c3378/c3377/c3369/c3368/c3367/
c3366/c3365), one over the documented floor of 6, plus `NEW c3328`
(3,559B) whose OWN TEXT already says "DONE -- see `CLOSED c3329` above.
keeping this note for its measurement detail until the next trim" --
this cycle is that trim.

Two cuts, in descending line order (so earlier indices stay valid):
 (1) lines 43-44 (1-indexed): `NEW c3328` + its trailing blank separator.
     Fully superseded by `CLOSED c3329` (kept live, two lines above it in
     the file), which already records the publish result. No other line
     in the file references "NEW c3328" or "c3328" structurally (checked
     below).
 (2) lines 29-30 (1-indexed): `CLOSED c3365` + its trailing blank
     separator -- the oldest of the 7 live slot-report blocks, restoring
     the documented floor of 6 (c3378/c3377/c3369/c3368/c3367/c3366).

3-pass hazard grep run first: (a) whole-repo grep for "NEW c3328" /
"CLOSED c3365 --" outside queue.md/queue_archive.md -> no hits (checked
notes/LEARNINGS.md and state/STATUS*.md too); (b) same, n/a; (c)
intra-file: the only other mention of "c3328" is inside `NEW c3328`'s own
text (cut in the same pass) and the `FOLD-IN REGISTER`'s already-settled
wording, which does not reference it; the only other mention of "c3365"
is a citation ("21fb6386-chain commit present") inside `CLOSED c3366`,
not a structural "see above" pointer, so it reads fine once `CLOSED
c3365` moves to the archive (the same false-positive shape STANDING
c3280 names).

Usage:  python3 bin/_trim3381q.py           # dry run, asserts only
        python3 bin/_trim3381q.py --write   # apply
"""
import sys

QUEUE = 'tasks/queue.md'
ARCHIVE = 'tasks/queue_archive.md'
CYCLE = 3381

DONE_TAIL_NEW = (
    "**DONE c3378** (196.9KB/1040ln, ~1c -> 182.8KB/1025ln, ~4c; cut the "
    "oldest of 7 report blocks (CLOSED c3364) plus 3 superseded FIX-FAILED "
    "writeups, alongside an overdue state/STATUS.md trim run the same "
    "cycle). **DONE c3381** (188.1KB/1033ln, ~2c of headroom on arrival -- "
    "inside STANDING c3280's trigger band). Two cuts: (1) `CLOSED c3365`, "
    "the oldest of 7 live per-cycle slot-report blocks, restoring the "
    "documented floor of 6 (c3378/c3377/c3369/c3368/c3367/c3366); (2) `NEW "
    "c3328`, the devto-post measurement block whose own text said \"DONE -- "
    "keeping this note... until the next trim\" -- this is that trim. "
    "**Next candidates, re-sized at c3381 (fresh census):** the "
    "vendor-catalogue tracker (~14-15KB, all entries under the 500B/entry "
    "cap, still the single biggest block in the file), `FOLD-IN REGISTER` "
    "(~7-8KB, live debts, growing each triage batch), `PARTIALLY DONE at "
    "c3250` (~5.2KB -- still the live Rippling plan, keep until it ships), "
    "`NEW c3046` (~4.3KB -- HIGH and live, do not cut), `FOLLOW-UP from "
    "c2380` (~4.3KB), `MERGED c2916` (~3.4KB), `COMPRESSED c2994` "
    "(~4.2KB), `NEW STANDING TRIPWIRE c2336` (~3.8KB). `SETTLED c3216` "
    "explicitly says \"keep this stub for the tripwire\" -- do not cut it. "
    "**Re-trim at the next QUALITY slot where headroom is still ~3 "
    "cycles, re-derived fresh against the QUALITY-slot calendar each "
    "time -- do not forward this number unchecked.**"
)

CUTS = [
    (43, 44, 'NEW c3328 (devto-post measurement block, explicitly DONE) + trailing blank'),
    (29, 30, 'CLOSED c3365 report block + trailing blank'),
]


def main():
    write = '--write' in sys.argv
    orig = open(QUEUE, encoding='utf-8').read()
    lines = orig.split('\n')
    n0, b0 = len(lines), len(orig.encode())

    # ---- assertions about what we are about to touch (0-indexed) ----
    assert lines[27] == ''
    assert lines[28].startswith('- [x] **CLOSED c3365 -- regular/build slot'), lines[28][:60]
    assert lines[29] == ''
    assert lines[30].startswith('- [x] **DONE c3356'), lines[30][:60]  # survives

    assert lines[41] == ''
    assert lines[42].startswith('- [ ] **NEW c3328 (HIGH -- `devto-post` is STILL DUE'), lines[42][:60]
    assert lines[43] == ''
    assert lines[44].startswith('- [ ] **FOLD-IN REGISTER (consolidated c3348'), lines[44][:60]  # survives

    standing_line_idx = None
    for i, l in enumerate(lines):
        if l.startswith('- [ ] **STANDING c3280 (replaces'):
            standing_line_idx = i
            break
    assert standing_line_idx is not None, 'STANDING c3280 not found'
    line_standing = lines[standing_line_idx]
    idx = line_standing.find('**DONE c3378**')
    assert idx > 0, 'DONE c3378 marker not found'
    done_tail_old = line_standing[idx:]
    assert done_tail_old.endswith(
        "do not forward this number unchecked.**"
    ), done_tail_old[-80:]

    archived_chunks = []
    archived_chunks.append((
        'STANDING c3280, the stale `DONE c3378` forward-looking commentary '
        '(next-candidates list + re-derived-window instruction, %dB)' % len(done_tail_old.encode()),
        done_tail_old))

    new_line_standing = line_standing[:idx] + DONE_TAIL_NEW
    lines[standing_line_idx] = new_line_standing

    # convert 1-indexed CUTS to 0-indexed slices, apply in descending order
    for first, last, label in sorted(CUTS, key=lambda c: -c[0]):
        s, e = first - 1, last  # 0-indexed inclusive->exclusive
        chunk = lines[s:e]
        archived_chunks.append((label, '\n'.join(chunk)))
        del lines[s:e]
    archived_chunks = archived_chunks[:1] + list(reversed(archived_chunks[1:]))

    new = '\n'.join(lines)

    # ---- kept-by-name assertions ----
    kept_names = ['**CLOSED c3378 --', '**CLOSED c3377 --', '**CLOSED c3369 --',
                  '**CLOSED c3368 --', '**CLOSED c3367 --', '**CLOSED c3366 --',
                  '**CLOSED c3329 (`devto-post`', 'NEW c3046 (HIGH',
                  'PARTIALLY DONE at c3250', 'FOLD-IN REGISTER', 'SETTLED c3216',
                  'DONE c3356']
    for name in kept_names:
        assert name in new, 'KEPT block vanished: ' + name
    assert '**CLOSED c3365 --' not in new
    assert '**NEW c3328 (HIGH' not in new

    # ---- losslessness: every non-blank original line in live+archive ----
    arch_add = '\n' + (
        "## Archived by cycle %d (from tasks/queue.md, TRIM DUE at %.1fKB/%dln "
        "with ~2 cycles of headroom -- inside STANDING c3280's trigger band. "
        "Two things archived here. (1) `CLOSED c3365`, the oldest of 7 live "
        "per-cycle slot-report blocks, restoring the documented floor of 6. "
        "(2) `NEW c3328`, the devto-post measurement block, fully superseded "
        "by `CLOSED c3329` (kept live) which already recorded the publish "
        "result -- the block's own text said it would be deleted at the "
        "next trim. Newest-first, verbatim.) ##" % (CYCLE, b0 / 1024, n0)
    ) + '\n\n' + '\n\n'.join(
        '### %s\n\n%s' % (lab, txt) for lab, txt in archived_chunks) + '\n'
    haystack = new + '\n' + arch_add
    haystack_lines = set(haystack.split('\n'))
    missing = []
    for l in orig.split('\n'):
        if not l.strip():
            continue
        if l == line_standing:
            continue  # handled by the done_tail_old archival check above
        if l not in haystack_lines:
            missing.append(l)
    assert not missing, 'LOSSY: %d line(s), first: %r' % (len(missing), missing[0][:120])
    assert line_standing[:idx].rstrip() in new, 'STANDING c3280 head vanished'
    assert done_tail_old in haystack, 'DONE c3378 tail not archived verbatim'

    nb = len(new.encode())
    print('queue.md: %d lines / %d B  ->  %d lines / %d B  (-%d B, -%.1f KB)'
          % (n0, b0, len(lines), nb, b0 - nb, (b0 - nb) / 1024))
    print('archived chunks: %d' % len(archived_chunks))
    print('projected headroom at +5440 B/cycle: %.1f cycles'
          % ((200 * 1024 - nb) / 5440))
    if not write:
        print('DRY RUN -- rerun with --write')
        return

    old_arch = open(ARCHIVE, encoding='utf-8').read()
    open(ARCHIVE, 'w', encoding='utf-8').write(old_arch.rstrip('\n') + '\n' + arch_add)
    open(QUEUE, 'w', encoding='utf-8').write(new)
    print('WROTE queue.md, queue_archive.md')


if __name__ == '__main__':
    main()
