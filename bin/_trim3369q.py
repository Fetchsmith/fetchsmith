#!/usr/bin/env python3
"""One-shot rotation for tasks/queue.md, cycle 3369 (QUALITY/GROWTH slot, 3369 % 3 == 0).

check-doc-size on arrival: tasks/queue.md TRIM DUE at 192.4KB/1054ln, ~1
cycle of headroom -- past STANDING c3280's ~3-cycle trigger (c3368 flagged
this twice: "c3369 is a QUALITY slot and queue.md is at ~2c headroom, that
trim is the top task"). notes/LEARNINGS.md also reads TRIM DUE but with
~24 real cycles of headroom; left untouched this cycle (time budget),
per c3364's note it needs a DEEP cut when eventually taken, not a token
one. state/STATUS.md reads TRIM DUE too (154.4KB, ~10c) -- not urgent.

Three cuts, in census order:
 (1) report blocks: 9 live per-cycle reports found (c3368,c3367,c3366,
     c3365,c3364,c3363,c3360,c3356,c3353). Floor is 6 (c3348/c3353/c3360/
     c3366 precedent). Archive the oldest 3: c3360 (L19), c3353 (L34),
     c3356 (L36-50), keeping the newest 6 (c3368/c3367/c3366/c3365/c3364/
     c3363).
 (2) the resolved `~~NEW c3360~~ DONE c3364` pointer item (L32) -- its own
     text says "kept one cycle as a pointer, delete at the next trim";
     this is that trim, 4 cycles late (c3366 did not take it). Archived,
     not kept again.
 (3) STANDING c3280 itself, the single biggest block in the file (6737B)
     -- its own text keeps flagging that it regrows every trim ("the rule
     includes itself"). Its DONE c3366 paragraph (1602B) carries a stale
     next-candidates list and a re-derived-window instruction already
     executed by this very cut. Replaced with a short DONE c3366 one-liner
     (matching the c3296..c3360 style) plus a fresh DONE c3369 paragraph
     and a re-derived next-candidates list.

3-pass hazard grep run before writing: (a) whole-repo by-name sweep for
c3360/c3353/c3356 outside queue.md/STATUS* -> only the standing false
positive shape (dead trim-script docstrings describing their own cuts,
e.g. bin/_trim3360q.py, bin/_trim3366q.py); (b) hits in state/STATUS.md
and state/STATUS_ARCHIVE.md only, each keeps its own self-contained
record; (c) intra-file: the only "above" reference near a cut block is
CLOSED c3356's own internal "full numbers in NEW c3356 above" -- NEW
c3356 (L54) is a DIFFERENT, still-live item, not part of this cut, so no
dangling pointer.

Usage:  python3 bin/_trim3369q.py           # dry run, asserts only
        python3 bin/_trim3369q.py --write   # apply
"""
import sys

QUEUE = 'tasks/queue.md'
ARCHIVE = 'tasks/queue_archive.md'
CYCLE = 3369

DONE_TAIL_NEW = (
    "**DONE c3366** (187.9KB/1050ln, ~2c -> 178.4KB/1045ln, ~4c; archived the oldest 3 "
    "of 9 report blocks (c3352/c3351/c3350) plus this item's own stale c3360 "
    "commentary). **DONE c3369** (192.4KB/1054ln, ~1 cycle of headroom -- past the "
    "~3-cycle trigger; flagged twice by c3368/c3367 as this slot's top task). Three "
    "cuts: (1) the oldest 3 of 9 live report blocks (c3360/c3353/c3356, archived "
    "verbatim), kept the newest 6 (c3368/c3367/c3366/c3365/c3364/c3363); (2) the "
    "resolved NEW-c3360/DONE-c3364 pointer item, whose own text called for "
    "deletion at the next trim -- this is that trim, 4 cycles late; (3) this item's own "
    "stale c3366 next-candidates list and re-derived-window instruction, already "
    "executed by this cut, replaced with a fresh one. **Next candidates, re-sized at "
    "c3369 (fresh census):** `PARTIALLY DONE at c3250` (~5.2KB -- still the live "
    "Rippling plan, keep until it ships), `FOLD-IN REGISTER` (~5.0KB, live debts), "
    "`FOLLOW-UP from c2380` (~4.3KB), `NEW c3046` (~4.3KB -- HIGH and live, do not "
    "cut), `MERGED c2916` (~4.3KB), `COMPRESSED c2994` (~4.2KB), `SETTLED c3216` "
    "(~4.2KB), `NEW STANDING TRIPWIRE c2336` (~3.8KB), the vendor-catalogue tracker's "
    "`Per-batch results` line (~8.8KB but `check-doc-size` already reads all 43 "
    "entries under the 500B/entry cap, so no breach to fix yet). **Re-trim at the next "
    "QUALITY slot where headroom is still ~3 cycles, re-derived fresh against the "
    "QUALITY-slot calendar each time -- do not forward this number unchecked.**"
)

ARCHIVE_HEADER = (
    "## Archived by cycle 3369 (from tasks/queue.md, TRIM DUE at 192.4KB/1054ln with "
    "**~1 cycle of headroom** -- past `STANDING c3280`'s ~3-cycle trigger, flagged "
    "twice by c3367/c3368. Three things archived here. (1) The oldest 3 of 9 live "
    "per-cycle report blocks -- c3360, c3353, c3356 -- keeping the newest 6 (c3368, "
    "c3367, c3366, c3365, c3364, c3363), the documented floor. (2) The resolved "
    "NEW-c3360/DONE-c3364 pointer item -- its own text said 'delete at the next "
    "trim'; this is that trim. (3) `STANDING c3280`'s own stale `DONE c3366` "
    "forward-looking commentary (next-candidates list and re-derived-window "
    "instruction, both already executed/superseded). Replaced with a short "
    "one-liner plus a fresh `DONE c3369` paragraph. Newest-first, verbatim.) ##"
)

CUTS = [
    (36, 51, 'CLOSED c3356 report block (incl. trailing blank line)'),
    (34, 35, 'CLOSED c3353 report block'),
    (32, 33, 'resolved ~~NEW c3360~~ DONE c3364 pointer item'),
    (19, 20, 'CLOSED c3360 report block'),
]


def main():
    write = '--write' in sys.argv
    orig = open(QUEUE, encoding='utf-8').read()
    lines = orig.split('\n')
    n0, b0 = len(lines), len(orig.encode())

    # ---- assertions about what we are about to touch (1-indexed in comments) ----
    assert lines[18].startswith('- [x] **CLOSED c3360 --'), lines[18][:60]
    assert lines[19] == ''
    assert lines[31].startswith('- [ ] **~~NEW c3360~~ DONE c3364'), lines[31][:60]
    assert lines[32] == ''
    assert lines[33].startswith('- [x] **CLOSED c3353 --'), lines[33][:60]
    assert lines[34] == ''
    assert lines[35].startswith('- [x] **CLOSED c3356 --'), lines[35][:60]
    assert lines[50] == ''
    assert lines[51].startswith('- [x] **DONE c3356'), lines[51][:60]  # survives, kept

    line86 = lines[85]
    assert line86.startswith('- [ ] **STANDING c3280 ('), line86[:60]
    idx = line86.find('**DONE c3366**')
    assert idx > 0, 'DONE c3366 marker not found'
    done_tail_old = line86[idx:]
    assert done_tail_old.endswith(
        "do not forward this number unchecked.**"
    ), done_tail_old[-80:]

    archived_chunks = []
    archived_chunks.append((
        'STANDING c3280, the stale `DONE c3366` forward-looking commentary '
        '(next-candidates list + re-derived-window instruction, %dB)' % len(done_tail_old.encode()),
        done_tail_old))

    new_line86 = line86[:idx] + DONE_TAIL_NEW
    lines[85] = new_line86

    for first, last, label in CUTS:
        chunk = lines[first - 1:last]
        archived_chunks.append((label, '\n'.join(chunk)))
        del lines[first - 1:last]

    new = '\n'.join(lines)

    # ---- kept-by-name assertions ----
    kept_names = ['**CLOSED c3357 ', '**CLOSED c3329 (', '**CLOSED c3336 ',
                  '**DONE c3356', '**DONE c3362', 'NEW c3356 (MEDIUM',
                  '**CLOSED c3363 --', '**CLOSED c3364 --', '**CLOSED c3365 --',
                  '**CLOSED c3366 --', '**CLOSED c3367 --', '**CLOSED c3368 --',
                  'NEW c3046 (HIGH', 'PARTIALLY DONE at c3250', 'FOLD-IN REGISTER']
    for name in kept_names:
        assert name in new, 'KEPT block vanished: ' + name
    assert '**CLOSED c3360 --' not in new
    assert '**CLOSED c3353 --' not in new
    assert '**CLOSED c3356 --' not in new
    assert '~~NEW c3360~~' not in new

    # ---- losslessness: every non-blank original line in live+archive ----
    arch_add = '\n' + ARCHIVE_HEADER + '\n\n' + '\n\n'.join(
        '### %s\n\n%s' % (lab, txt) for lab, txt in archived_chunks) + '\n'
    haystack = new + '\n' + arch_add
    missing = []
    for l in orig.split('\n'):
        if not l.strip():
            continue
        if l == line86:
            continue  # handled by the done_tail_old archival check above
        if l not in haystack.split('\n'):
            missing.append(l)
    assert not missing, 'LOSSY: %d line(s), first: %r' % (len(missing), missing[0][:120])
    assert line86[:idx].rstrip() in new, 'STANDING c3280 head vanished'
    assert done_tail_old in haystack, 'DONE c3366 tail not archived verbatim'

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
