#!/usr/bin/env python3
"""One-shot rotation for state/STATUS.md, cycle 3378 (QUALITY/GROWTH slot, 3378 % 3 == 0).

check-doc-size on arrival: state/STATUS.md TRIM DUE at 196.0KB/407ln, ~1
cycle of headroom -- past STANDING c3280's ~3-cycle trigger (c3280 covers
queue.md by name but the same ~3-cycle rule is applied to STATUS.md per
the c3144/c3296/c3347 precedent trims). Last STATUS.md trim was c3347,
which archived cycles <=3337 and kept the newest 10 blocks (3346..3338
plus its own). Since then 40 blocks have accumulated (3377 down to
3338) with NO trim -- restore the documented floor of 10 (newest:
3377..3368), archive the oldest 30 (3367..3338) verbatim.

Usage:  python3 bin/_trim3378_status.py           # dry run, asserts only
        python3 bin/_trim3378_status.py --write    # apply
"""
import re
import sys

STATUS = 'state/STATUS.md'
ARCHIVE = 'state/STATUS_ARCHIVE.md'
CYCLE = 3378
KEEP_BLOCKS = 10


def main():
    write = '--write' in sys.argv
    orig = open(STATUS, encoding='utf-8').read()
    lines = orig.split('\n')
    n0, b0 = len(lines), len(orig.encode())

    starts = [i for i, l in enumerate(lines) if l.startswith('Updated: ')]
    cycles = []
    for i in starts:
        m = re.search(r'cycle (\d+)', lines[i])
        assert m, lines[i][:80]
        cycles.append(int(m.group(1)))
    assert len(starts) == 40, 'expected 40 live blocks, found %d' % len(starts)
    assert cycles == list(range(3377, 3337, -1)), cycles[:5]

    cut_from = starts[KEEP_BLOCKS]  # first line of the 11th-newest block (3367)
    kept_head = lines[:cut_from]
    archived_tail_lines = lines[cut_from:]
    # drop one trailing blank line to avoid a doubled separator at the join
    while archived_tail_lines and archived_tail_lines[-1] == '':
        archived_tail_lines.pop()

    archived_text = '\n'.join(archived_tail_lines)
    assert archived_text.startswith('Updated: 2026-11-18 UTC by cycle 3367'), archived_text[:60]

    header = (
        "## Archived by cycle %d, 2026-11-18 -- state/STATUS.md had grown to "
        "%d lines / %.1fKB with NO trim since cycle 3347 (40 live blocks, "
        "3377 down to 3338), TRIM DUE with only ~1 cycle of headroom. Cycles "
        "3367 down to 3338 (30 blocks) moved here verbatim (newest-first, "
        "same order as the source file); the live file keeps the newest 10 "
        "blocks (3377 down to 3368), the documented floor."
        % (CYCLE, n0, b0 / 1024)
    )

    new_live = '\n'.join(kept_head).rstrip('\n') + '\n'
    nb = len(new_live.encode())

    # ---- assertions ----
    assert new_live.count('Updated: ') == KEEP_BLOCKS
    assert 'cycle 3368' in new_live and 'cycle 3367' not in new_live
    assert 'cycle 3338' not in new_live

    haystack_lines = set(new_live.split('\n')) | set(archived_text.split('\n'))
    missing = []
    for l in orig.split('\n'):
        if not l.strip():
            continue
        if l not in haystack_lines:
            missing.append(l)
    assert not missing, 'LOSSY: %d line(s), first: %r' % (len(missing), missing[0][:120])

    print('STATUS.md: %d lines / %d B  ->  %d lines / %d B  (-%d B, -%.1f KB)'
          % (n0, b0, new_live.count(chr(10)) + 1, nb, b0 - nb, (b0 - nb) / 1024))
    print('projected headroom at +4510 B/cycle: %.1f cycles' % ((200 * 1024 - nb) / 4510))
    if not write:
        print('DRY RUN -- rerun with --write')
        return

    old_arch = open(ARCHIVE, encoding='utf-8').read()
    open(ARCHIVE, 'w', encoding='utf-8').write(
        old_arch.rstrip('\n') + '\n\n' + header + '\n\n' + archived_text + '\n')
    open(STATUS, 'w', encoding='utf-8').write(new_live)
    print('WROTE state/STATUS.md, state/STATUS_ARCHIVE.md')


if __name__ == '__main__':
    main()
