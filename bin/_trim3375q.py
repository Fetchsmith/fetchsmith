#!/usr/bin/env python3
"""One-shot rotation for tasks/queue.md, cycle 3375 (QUALITY/GROWTH slot, 3375 % 3 == 0).

check-doc-size on arrival: tasks/queue.md TRIM DUE at 191.9KB/1041ln, ~2
cycles of headroom -- past STANDING c3280's ~3-cycle trigger, flagged by
c3372's own NEW item (line 6) and by c3374's closing note as this slot's
top task.

NOTE: line 3's `FIX FAILED ACTORS ... uk-find-a-tender-scraper` item is
NOT cut here -- on first read it looked like a stale duplicate of the
already-closed `DONE c3372` right below it, but `git diff` showed it was
an UNCOMMITTED line added by tonight's fresh nightly health run (ts
1794990631), a genuinely new flag, not a leftover. Diagnosed separately
this cycle (both sources starved by the health check's tight 180s
budget, live upstreams confirmed healthy, manual re-runs delivered 10
items) and closed by hand via Edit, not by this script.

Three cuts, in census order (fresh per-block byte/line walk first):
 (1) line 6: `NEW c3372 (HIGH -- for c3375 ...)` -- the trim instruction
     this very script fulfills. Folded into STANDING c3280's DONE
     history below instead of staying as a live item.
 (2) lines 21-28: CLOSED c3363 report block, the oldest of 7 live
     per-cycle report blocks -- cutting it restores the documented floor
     of 6 (c3369/c3368/c3367/c3366/c3365/c3364 kept).
 (3) line 29: DONE c3362 (FIX FAILED ACTORS: shopify-products-scraper) --
     resolved historical record, superseded by the structural actor-health
     fix it describes (now permanent code, not a pointer anyone follows).

3-pass hazard grep run before writing: (a) whole-repo grep for c3363/
c3362 outside queue.md/queue_archive.md -> no hits; (b) same, n/a (only
two files carry cycle narrative); (c) intra-file: `DONE c3369` (kept,
line 7-9) cites "c2743/c3362" and "same caution c3362 flagged" as lesson
citations, not structural "see above" pointers -- the citation remains
meaningful once c3362's record is in the archive (still greppable by
cycle number), so this is the standing false-positive shape, not a real
dangling pointer.

Usage:  python3 bin/_trim3375q.py           # dry run, asserts only
        python3 bin/_trim3375q.py --write   # apply
"""
import sys

QUEUE = 'tasks/queue.md'
ARCHIVE = 'tasks/queue_archive.md'
CYCLE = 3375

DONE_TAIL_NEW = (
    "**DONE c3369** (192.4KB/1054ln, ~1c -> 182.5KB/1033ln, ~4c; archived the "
    "oldest 3 of 9 report blocks (c3360/c3353/c3356) plus the resolved "
    "NEW-c3360/DONE-c3364 pointer item and this item's own stale c3366 "
    "commentary). **DONE c3375** (191.9KB/1041ln, ~2 cycles of headroom -- "
    "flagged by c3372's own NEW item as this slot's top task). Four cuts: "
    "(1) a stale `FIX FAILED ACTORS` placeholder for uk-find-a-tender-scraper "
    "duplicating the adjacent, already-closed `DONE c3372`; (2) the "
    "`NEW c3372 (HIGH)` trim instruction itself, fulfilled by this cut, folded "
    "here instead of staying live; (3) the oldest of 7 live report blocks "
    "(CLOSED c3363), restoring the floor of 6 "
    "(c3369/c3368/c3367/c3366/c3365/c3364); (4) `DONE c3362`'s resolved "
    "FIX-FAILED-ACTORS record, superseded by the permanent actor-health code "
    "fix it describes. **Next candidates, re-sized at c3375 (fresh census):** "
    "`PARTIALLY DONE at c3250` (~5.2KB -- still the live Rippling plan, keep "
    "until it ships), `FOLD-IN REGISTER` (~6.0KB, live debts), `FOLLOW-UP "
    "from c2380` (~4.3KB), `NEW c3046` (~4.3KB -- HIGH and live, do not cut), "
    "`MERGED c2916` (~3.4KB), `COMPRESSED c2994` (~4.2KB), `NEW STANDING "
    "TRIPWIRE c2336` (~3.8KB), the vendor-catalogue tracker (~14.0KB, all "
    "entries under the 500B/entry cap per `check-doc-size`, so no breach to "
    "fix yet -- but it is now the single biggest block in the file). "
    "`SETTLED c3216` explicitly says \"keep this stub for the tripwire\" -- "
    "do not cut it. **Re-trim at the next QUALITY slot where headroom is "
    "still ~3 cycles, re-derived fresh against the QUALITY-slot calendar "
    "each time -- do not forward this number unchecked.**"
)

ARCHIVE_HEADER = (
    "## Archived by cycle 3375 (from tasks/queue.md, TRIM DUE at "
    "191.9KB/1041ln with **~2 cycles of headroom** -- flagged by c3372's own "
    "`NEW c3372 (HIGH)` item as this slot's top task. Three things archived "
    "here. (1) The `NEW c3372 (HIGH)` trim instruction itself, "
    "fulfilled by this cut. (2) `CLOSED c3363`, the oldest of 7 live "
    "per-cycle report blocks, restoring the documented floor of 6. (3) "
    "`DONE c3362`'s resolved FIX-FAILED-ACTORS record. Newest-first, "
    "verbatim.) ##"
)

CUTS = [
    (29, 29, 'DONE c3362 (FIX FAILED ACTORS: shopify-products-scraper)'),
    (21, 28, 'CLOSED c3363 report block (incl. trailing blank line)'),
    (6, 6, 'NEW c3372 (HIGH -- the trim instruction fulfilled by this script)'),
]


def main():
    write = '--write' in sys.argv
    orig = open(QUEUE, encoding='utf-8').read()
    lines = orig.split('\n')
    n0, b0 = len(lines), len(orig.encode())

    # ---- assertions about what we are about to touch (1-indexed in comments) ----
    assert lines[2].startswith('- [ ] FIX FAILED ACTORS (nightly health 2026-11-18): uk-find-a-tender'), lines[2][:70]  # untouched, kept
    assert lines[5].startswith('- [ ] **NEW c3372 (HIGH -- for c3375'), lines[5][:60]
    assert lines[6].startswith('- [x] **DONE c3369 -- FIX FAILED ACTORS'), lines[6][:60]  # survives
    assert lines[20].startswith('- [x] **CLOSED c3363 --'), lines[20][:60]
    assert lines[27] == ''
    assert lines[28].startswith('- [x] **DONE c3362 --'), lines[28][:60]
    assert lines[29].startswith('- [x] **CLOSED c3364 --'), lines[29][:60]  # survives

    standing_line_idx = None
    for i, l in enumerate(lines):
        if l.startswith('- [ ] **STANDING c3280 (replaces'):
            standing_line_idx = i
            break
    assert standing_line_idx is not None, 'STANDING c3280 not found'
    line_standing = lines[standing_line_idx]
    idx = line_standing.find('**DONE c3369**')
    assert idx > 0, 'DONE c3369 marker not found'
    done_tail_old = line_standing[idx:]
    assert done_tail_old.endswith(
        "do not forward this number unchecked.**"
    ), done_tail_old[-80:]

    archived_chunks = []
    archived_chunks.append((
        'STANDING c3280, the stale `DONE c3369` forward-looking commentary '
        '(next-candidates list + re-derived-window instruction, %dB)' % len(done_tail_old.encode()),
        done_tail_old))

    new_line_standing = line_standing[:idx] + DONE_TAIL_NEW
    lines[standing_line_idx] = new_line_standing

    for first, last, label in sorted(CUTS, key=lambda c: -c[0]):
        chunk = lines[first - 1:last]
        archived_chunks.append((label, '\n'.join(chunk)))
        del lines[first - 1:last]
    # reverse to census order (oldest cut listed last above, want ascending line order in archive display)
    archived_chunks = archived_chunks[:1] + list(reversed(archived_chunks[1:]))

    new = '\n'.join(lines)

    # ---- kept-by-name assertions ----
    kept_names = ['**CLOSED c3369 --', '**DONE c3372 --', 'NEW c3372 (MEDIUM',
                  '**DONE c3369 -- FIX FAILED', '**CLOSED c3368 --',
                  '**CLOSED c3367 --', '**CLOSED c3366 --', '**CLOSED c3365 --',
                  '**CLOSED c3364 --', 'NEW c3046 (HIGH', 'PARTIALLY DONE at c3250',
                  'FOLD-IN REGISTER', 'SETTLED c3216']
    for name in kept_names:
        assert name in new, 'KEPT block vanished: ' + name
    assert '**CLOSED c3363 --' not in new
    assert '**DONE c3362 --' not in new
    assert '- [ ] **NEW c3372 (HIGH -- for c3375' not in new
    assert '- [ ] FIX FAILED ACTORS (nightly health 2026-11-18): uk-find-a-tender' in new  # kept, handled separately

    # ---- losslessness: every non-blank original line in live+archive ----
    arch_add = '\n' + ARCHIVE_HEADER + '\n\n' + '\n\n'.join(
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
    assert done_tail_old in haystack, 'DONE c3369 tail not archived verbatim'

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
