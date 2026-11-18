#!/usr/bin/env python3
"""One-shot rotation for tasks/queue.md, cycle 3366 (QUALITY/GROWTH slot, 3366 % 3 == 0).

check-doc-size on arrival: tasks/queue.md TRIM DUE at 187.9KB/1050ln, ~2
cycles of headroom -- past STANDING c3280's ~3-cycle trigger (the predicted
c3363 window went to check-claim-coverage/check-stale-forecast instead, a
fleet check outranking the trim per the standing rule). notes/LEARNINGS.md
also reads TRIM DUE but with ~24 cycles of real headroom before hitting its
8000-line cap; left untouched this cycle per time budget, flagged for the
next QUALITY slot.

Two cuts, in census order:
 (1) report blocks: 9 live per-cycle reports found (c3365,c3364,c3363,c3360,
     c3356,c3353,c3352,c3351,c3350). Floor is 6 (established c3348/c3353/
     c3360 precedent). Archive the oldest 3: c3352 (L50), c3351 (L52),
     c3350 (L54), each a single physical line + its trailing blank line.
 (2) STANDING c3280 itself, the single biggest block in the file (8225B) --
     flagged by its own text as "growing again, the rule includes itself".
     Its DONE c3360 paragraph (3331B) carries stale forward-looking
     commentary (a lesson already absorbed into this item's own decision
     rule, a content summary duplicated in state/STATUS.md and the c3360
     archive header, a next-candidates list now stale, and a "re-trim at
     c3363" instruction already executed/superseded). Replaced with a
     short DONE c3360 one-liner (matching the c3296..c3332 style) plus a
     fresh DONE c3366 paragraph recording this cut and a re-derived
     next-candidates list.

3-pass hazard grep run before writing: (a) whole-repo by-name sweep for
c3352/c3351/c3350 outside queue.md/STATUS* -> only the standing false
positive shape (dead trim-script docstrings describing their own cuts);
(b) hits in state/STATUS.md and state/STATUS_ARCHIVE.md only, each keeps
its own record; (c) intra-file: no live "see CLOSED cNNNN above" pointer
to any of the three archived blocks.

Usage:  python3 bin/_trim3366q.py           # dry run, asserts only
        python3 bin/_trim3366q.py --write   # apply
"""
import sys

QUEUE = 'tasks/queue.md'
ARCHIVE = 'tasks/queue_archive.md'
CYCLE = 3366

DONE_TAIL_NEW = (
    "**DONE c3360** (181.4KB/1050ln, ~3c -> 165.2KB/1025ln, ~7c; -16.6KB in 3 cuts, "
    "verified lossless across THREE files; full lesson/next-candidates/structural-note "
    "text archived verbatim, `tasks/queue_archive.md`, `## Archived by cycle 3366`). "
    "**DONE c3366** (187.9KB/1050ln, ~2 cycles of headroom -- the predicted c3363 window "
    "went to `check-claim-coverage`/`check-stale-forecast` instead per the "
    "fleet-check-outranks-trim rule, so this slipped to c3366, 3 cycles past the original "
    "c3363 target but inside this item's own 'treat a passed window as overdue "
    "immediately' rule, not yet at the -2c c3348 saw; landing size and headroom recorded "
    "in `state/STATUS.md` c3366). Two cuts: (1) the oldest 3 of 9 live report blocks "
    "(c3352/c3351/c3350, archived verbatim), kept the newest 6 "
    "(c3365/c3364/c3363/c3360/c3356/c3353); (2) this item's own stale c3360 "
    "forward-looking commentary (lesson, content summary, next-candidates list, "
    "structural note, the now-executed 're-trim at c3363' instruction) -- all of it "
    "either superseded by this cut or already true a second time, archived verbatim "
    "rather than carried forward again. **Next candidates, re-sized at c3366 (fresh "
    "census):** `PARTIALLY DONE at c3250` (~5.2KB -- still the live Rippling plan, keep "
    "until it ships), `FOLD-IN REGISTER` (~4.9KB, live debts), `FOLLOW-UP from c2380` "
    "(~4.3KB), `NEW c3046` (~4.3KB -- HIGH and live, do not cut), `MERGED c2916` "
    "(~4.3KB), `COMPRESSED c2994` (~4.2KB), `SETTLED c3216` (~4.2KB), `NEW STANDING "
    "TRIPWIRE c2336` (~3.8KB), the vendor-catalogue tracker's `Per-batch results` line "
    "(~8.2KB but `check-doc-size` already reads all 41 entries under the 500B/entry "
    "cap, so no breach to fix yet). **Re-trim at the next QUALITY slot where headroom "
    "is still ~3 cycles, re-derived fresh against the QUALITY-slot calendar each time -- "
    "do not forward this number unchecked.**"
)

ARCHIVE_HEADER = (
    "## Archived by cycle 3366 (from tasks/queue.md, TRIM DUE at 187.9KB/1050ln with "
    "**~2 cycles of headroom** -- past `STANDING c3280`'s ~3-cycle trigger because the "
    "predicted c3363 window went to two due fleet checks instead. Two things archived "
    "here. (1) The oldest 3 of 9 live per-cycle report blocks -- c3352, c3351, c3350 -- "
    "keeping the newest 6 (c3365, c3364, c3363, c3360, c3356, c3353), the documented "
    "floor. (2) `STANDING c3280`'s own stale `DONE c3360` forward-looking commentary: "
    "its lesson (the QUALITY-slot-calendar off-by-one, now folded into the item's "
    "standing decision rule rather than repeated in the history line), its c3360 "
    "content summary (duplicated in `state/STATUS.md` c3360 and this file's own "
    "`## Archived by cycle 3360` header), its now-stale next-candidates list, its "
    "structural note on report-block share, and its 're-trim at the QUALITY slot "
    "c3363' instruction -- which this very cut executes, 3 cycles late. Replaced with "
    "a short one-liner plus a fresh `DONE c3366` paragraph. Newest-first, verbatim.) ##"
)

CUTS = [
    (54, 55, 'CLOSED c3350 report block'),
    (52, 53, 'CLOSED c3351 report block'),
    (50, 51, 'CLOSED c3352 report block'),
]


def main():
    write = '--write' in sys.argv
    orig = open(QUEUE, encoding='utf-8').read()
    lines = orig.split('\n')
    n0, b0 = len(lines), len(orig.encode())

    # ---- assertions about what we are about to touch ----
    assert lines[49].startswith('- [x] **CLOSED c3352 --'), lines[49][:60]
    assert lines[51].startswith('- [x] **CLOSED c3351 --'), lines[51][:60]
    assert lines[53].startswith('- [x] **CLOSED c3350 --'), lines[53][:60]
    assert lines[48].startswith('- [x] **CLOSED c3357'), lines[48][:60]
    assert lines[55].startswith("- [x] **CLOSED c3329"), lines[55][:60]
    assert lines[50] == '' and lines[52] == '' and lines[54] == ''

    line82 = lines[81]
    assert line82.startswith('- [ ] **STANDING c3280 ('), line82[:60]
    idx = line82.find('**DONE c3360**')
    assert idx > 0, 'DONE c3360 marker not found'
    done_tail_old = line82[idx:]
    assert done_tail_old.endswith(
        "spend it on the staged tail pass named above rather than another small report-block cut."
    ), done_tail_old[-80:]

    archived_chunks = []

    archived_chunks.append((
        'STANDING c3280, the stale `DONE c3360` forward-looking commentary '
        '(lesson/content-summary/next-candidates/structural-note/re-trim-instruction, '
        '%dB)' % len(done_tail_old.encode()),
        done_tail_old))

    new_line82 = line82[:idx] + DONE_TAIL_NEW
    lines[81] = new_line82

    for first, last, label in CUTS:
        chunk = lines[first - 1:last]
        archived_chunks.append((label, '\n'.join(chunk)))
        del lines[first - 1:last]

    new = '\n'.join(lines)

    # ---- kept-by-name assertions ----
    kept_names = ['**CLOSED c3357 ', '**CLOSED c3329 (', '**CLOSED c3336 ',
                  '**CLOSED c3356 --', '**CLOSED c3353 --', '**CLOSED c3360 --',
                  '**CLOSED c3363 --', '**CLOSED c3364 --', '**CLOSED c3365 --',
                  'NEW c3046 (HIGH', 'PARTIALLY DONE at c3250', 'FOLD-IN REGISTER']
    for name in kept_names:
        assert name in new, 'KEPT block vanished: ' + name
    assert '**CLOSED c3352 --' not in new
    assert '**CLOSED c3351 --' not in new
    assert '**CLOSED c3350 --' not in new

    # ---- losslessness: every non-blank original line in live+archive ----
    arch_add = '\n' + ARCHIVE_HEADER + '\n\n' + '\n\n'.join(
        '### %s\n\n%s' % (lab, txt) for lab, txt in archived_chunks) + '\n'
    haystack = new + '\n' + arch_add
    # the STANDING c3280 line is rewritten (not removed wholesale), so check it
    # separately: the old line's content must be reconstructible from new+archive.
    missing = []
    for l in orig.split('\n'):
        if not l.strip():
            continue
        if l == line82:
            continue  # handled by the done_tail_old archival check above
        if l not in haystack.split('\n'):
            missing.append(l)
    assert not missing, 'LOSSY: %d line(s), first: %r' % (len(missing), missing[0][:120])
    # explicit check for the rewritten line: both halves must survive somewhere
    assert line82[:idx].rstrip() in new, 'STANDING c3280 head vanished'
    assert done_tail_old in haystack, 'DONE c3360 tail not archived verbatim'

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
