#!/usr/bin/env python3
"""One-shot rotation for tasks/queue.md, cycle 3378 (QUALITY/GROWTH slot, 3378 % 3 == 0).

check-doc-size on arrival: tasks/queue.md TRIM DUE at 196.9KB/1040ln, ~1
cycle of headroom -- past STANDING c3280's ~3-cycle trigger, flagged by
c3376/c3377's closing notes as this slot's top task (shared with the
state/STATUS.md trim done alongside this one).

Fresh per-block census (bin/-style grep over every `- [ ]`/`- [x]` head)
found 7 live "per-cycle report" blocks (3377/3369/3368/3367/3366/3365/
3364), one over the documented floor of 6, plus three now-superseded
`FIX FAILED ACTORS` incident records for the uk-find-a-tender-scraper /
grants-gov-scraper nightly-health saga that c3376's `DONE c3376` already
closed out (closes `NEW c3375`, "the fourth and LAST open shape in the
c3362/c3369/c3372 classifier series") -- the underlying code fix is now
permanent and self-documenting in `bin/actor-health`, so the three older
blow-by-blow incident writeups are redundant with that one consolidated
closure line, which is kept.

Four cuts, in descending line order (so earlier indices stay valid):
 (1) lines 27-36 (1-indexed): `CLOSED c3364` report block, the oldest of
     7 live report blocks -- restores the floor of 6 (c3377/c3369/c3368/
     c3367/c3366/c3365).
 (2) lines 13-15 (1-indexed): `DONE c3369 -- FIX FAILED ACTORS:
     grants-gov-scraper` + its trailing `Guards:` line, superseded by
     c3376's consolidated closure. Keeps the blank separator (line 15)
     before `CLOSED c3368`.
 (3) line 11 (1-indexed): `DONE c3372 -- FIX FAILED ACTORS:
     uk-find-a-tender-scraper`, same reasoning.
 (4) line 9 (1-indexed): `DONE c3375 -- FIX FAILED ACTORS:
     uk-find-a-tender-scraper`, same reasoning (and the one whose own
     text cross-references `DONE c3372`, which is cut alongside it, so
     no dangling intra-reference survives).

`DONE c3376` itself (closes `NEW c3375`) is KEPT -- it is the single
consolidated record of the whole saga's root cause and fix.

3-pass hazard grep run first: (a) whole-repo grep for "DONE c3372"/
"DONE c3369 -- FIX FAILED"/"DONE c3375 -- FIX FAILED"/"CLOSED c3364"
outside queue.md/queue_archive.md -> no hits (checked notes/LEARNINGS.md
and state/STATUS*.md too); (b) same, n/a; (c) intra-file: the only
in-file mention of "DONE c3372" is inside `DONE c3375`'s own text,
cut in the same pass, and `DONE c3376`'s text names the classifier
series by cycle number ("c3362/c3369/c3372") as a citation, not a
structural "see above" pointer, so it reads fine once those blocks
move to the archive (same false-positive shape STANDING c3280 names).

Usage:  python3 bin/_trim3378q.py           # dry run, asserts only
        python3 bin/_trim3378q.py --write   # apply
"""
import sys

QUEUE = 'tasks/queue.md'
ARCHIVE = 'tasks/queue_archive.md'
CYCLE = 3378

DONE_TAIL_NEW = (
    "**DONE c3375** (191.9KB/1041ln, ~2c -> 187.6KB/1033ln, ~2c; 3 cuts: a "
    "stale FIX-FAILED placeholder, the fulfilled NEW-c3372 trim instruction, "
    "the oldest of 7 report blocks (CLOSED c3363, floor restored to 6), and "
    "DONE c3362's resolved FIX-FAILED record). **DONE c3378** (196.9KB/1040ln, "
    "~1 cycle of headroom -- flagged by c3376/c3377 as this slot's top task, "
    "run alongside an overdue state/STATUS.md trim, 40 live blocks with no "
    "trim since c3347, cut to the floor of 10). Four cuts here: (1) the "
    "oldest of 7 live report blocks (CLOSED c3364), restoring the floor of "
    "6 (c3377/c3369/c3368/c3367/c3366/c3365); (2)-(4) three now-superseded "
    "`FIX FAILED ACTORS` incident writeups for the uk-find-a-tender-scraper/"
    "grants-gov-scraper nightly-health saga (DONE c3375, DONE c3372, DONE "
    "c3369-grants-gov) -- the permanent code fix is self-documenting in "
    "`bin/actor-health` and c3376's own `DONE c3376` is the one consolidated "
    "closure record, kept live. **Next candidates, re-sized at c3378 (fresh "
    "census):** `PARTIALLY DONE at c3250` (~5.2KB -- still the live Rippling "
    "plan, keep until it ships), `FOLD-IN REGISTER` (~6.0KB, live debts), "
    "`FOLLOW-UP from c2380` (~4.3KB), `NEW c3046` (~4.3KB -- HIGH and live, "
    "do not cut), `MERGED c2916` (~3.4KB), `COMPRESSED c2994` (~4.2KB), `NEW "
    "STANDING TRIPWIRE c2336` (~3.8KB), the vendor-catalogue tracker (~14.4KB, "
    "all entries under the 500B/entry cap per `check-doc-size`, still the "
    "single biggest block in the file). `SETTLED c3216` explicitly says "
    "\"keep this stub for the tripwire\" -- do not cut it. **Re-trim at the "
    "next QUALITY slot where headroom is still ~3 cycles, re-derived fresh "
    "against the QUALITY-slot calendar each time -- do not forward this "
    "number unchecked.**"
)

CUTS = [
    (27, 36, 'CLOSED c3364 report block (incl. surrounding blank lines)'),
    (13, 15, 'DONE c3369 -- FIX FAILED ACTORS: grants-gov-scraper + Guards line'),
    (11, 11, 'DONE c3372 -- FIX FAILED ACTORS: uk-find-a-tender-scraper'),
    (9, 9, 'DONE c3375 -- FIX FAILED ACTORS: uk-find-a-tender-scraper'),
]


def main():
    write = '--write' in sys.argv
    orig = open(QUEUE, encoding='utf-8').read()
    lines = orig.split('\n')
    n0, b0 = len(lines), len(orig.encode())

    # ---- assertions about what we are about to touch (0-indexed) ----
    assert lines[8].startswith('- [x] **DONE c3375 -- FIX FAILED ACTORS'), lines[8][:60]
    assert lines[9].startswith('- [x] **DONE c3376 (closes'), lines[9][:60]  # survives
    assert lines[10].startswith('- [x] **DONE c3372 -- FIX FAILED ACTORS'), lines[10][:60]
    assert lines[11].startswith('- [ ] **NEW c3372 (MEDIUM'), lines[11][:60]  # survives
    assert lines[12].startswith('- [x] **DONE c3369 -- FIX FAILED ACTORS (nightly health 2026-11-18): g'), lines[12][:70]
    assert lines[13] == ''
    assert lines[14].startswith('  Guards: one shared script'), lines[14][:60]
    assert lines[15] == ''
    assert lines[16].startswith('- [x] **CLOSED c3368 --'), lines[16][:60]  # survives
    assert lines[24].startswith('- [x] **CLOSED c3365 --'), lines[24][:60]  # survives
    assert lines[25] == ''
    assert lines[26].startswith('- [x] **CLOSED c3364 --'), lines[26][:60]
    assert lines[35] == ''
    assert lines[36].startswith('- [x] **DONE c3356'), lines[36][:60]  # survives

    standing_line_idx = None
    for i, l in enumerate(lines):
        if l.startswith('- [ ] **STANDING c3280 (replaces'):
            standing_line_idx = i
            break
    assert standing_line_idx is not None, 'STANDING c3280 not found'
    line_standing = lines[standing_line_idx]
    idx = line_standing.find('**DONE c3375**')
    assert idx > 0, 'DONE c3375 marker not found'
    done_tail_old = line_standing[idx:]
    assert done_tail_old.endswith(
        "do not forward this number unchecked.**"
    ), done_tail_old[-80:]

    archived_chunks = []
    archived_chunks.append((
        'STANDING c3280, the stale `DONE c3375` forward-looking commentary '
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
    kept_names = ['**CLOSED c3377 --', '**DONE c3376 (closes', 'NEW c3372 (MEDIUM',
                  '**CLOSED c3369 --', '**CLOSED c3368 --', '**CLOSED c3367 --',
                  '**CLOSED c3366 --', '**CLOSED c3365 --', 'NEW c3046 (HIGH',
                  'PARTIALLY DONE at c3250', 'FOLD-IN REGISTER', 'SETTLED c3216',
                  'DONE c3356']
    for name in kept_names:
        assert name in new, 'KEPT block vanished: ' + name
    assert '**CLOSED c3364 --' not in new
    assert '**DONE c3375 -- FIX FAILED' not in new
    assert '**DONE c3372 -- FIX FAILED' not in new
    assert '**DONE c3369 -- FIX FAILED ACTORS (nightly health 2026-11-18): g' not in new

    # ---- losslessness: every non-blank original line in live+archive ----
    arch_add = '\n' + (
        "## Archived by cycle %d (from tasks/queue.md, TRIM DUE at %.1fKB/%dln "
        "with ~1 cycle of headroom -- flagged by c3376/c3377's closing notes as "
        "this slot's top task. Four things archived here. (1) `CLOSED c3364`, "
        "the oldest of 7 live per-cycle report blocks, restoring the "
        "documented floor of 6. (2)-(4) three now-superseded `FIX FAILED "
        "ACTORS` incident writeups for the uk-find-a-tender-scraper/"
        "grants-gov-scraper nightly-health saga (DONE c3375, DONE c3372, DONE "
        "c3369-grants-gov) -- the permanent code fix is self-documenting in "
        "`bin/actor-health`, superseding these blow-by-blow records; "
        "`DONE c3376`'s consolidated closure stays live. Newest-first, "
        "verbatim.) ##" % (CYCLE, b0 / 1024, n0)
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
    assert done_tail_old in haystack, 'DONE c3375 tail not archived verbatim'

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
