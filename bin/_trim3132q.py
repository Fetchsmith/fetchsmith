#!/usr/bin/env python3
"""One-shot queue.md trim for cycle 3132 (QUALITY slot).

Archives the 4 oldest live cycle blocks -- CLOSED c3127 / c3126 / c3125 / c3124,
one contiguous range (lines 29-49, 1-indexed inclusive, incl. the trailing blank)
-- to tasks/queue_archive.md under a '## Archived by cycle 3132' header, VERBATIM
and newest-first (same order as the source file), restoring the newest-5 floor
(live blocks left: c3132, c3131, c3130, c3129, c3128).

Self-verifying per bin/_trim1836.py: refuses to write unless (a) the range's
first line is the expected CLOSED c3127 header and its last line is blank,
(b) every non-blank original line is still findable in live+archive afterwards
(lossless), and (c) the live file ends up with exactly 5 'CLOSED c3' blocks.

Dry-run by default; pass --write to apply.
"""
import re
import sys

QUEUE = '/root/agent/tasks/queue.md'
ARCHIVE = '/root/agent/tasks/queue_archive.md'

START, END = 29, 49  # 1-indexed, inclusive
EXPECT_HEAD = '- [ ] **CLOSED c3127 -- Regular/GROWTH slot'
HEADER = (
    '## Archived by cycle 3132 trim (QUALITY slot; restoring the newest-5 floor after this '
    "cycle's own `CLOSED c3132` block took the live count to 9) -- `CLOSED c3127`, `CLOSED c3126`, "
    '`CLOSED c3125` and `CLOSED c3124` archived verbatim. Newest-first below, same order as the '
    'source file.\n'
)


def main() -> int:
    write = '--write' in sys.argv
    orig = open(QUEUE, encoding='utf-8').read().split('\n')

    cut = orig[START - 1:END]          # the block to move
    kept = orig[:START - 1] + orig[END:]

    # (a) range asserts -- never trust the line numbers blind
    if not cut[0].startswith(EXPECT_HEAD):
        print(f'ABORT: line {START} is not the expected c3127 header:\n  {cut[0][:120]!r}')
        return 1
    if cut[-1].strip() != '':
        print(f'ABORT: line {END} is not blank (would glue two items together):\n  {cut[-1][:120]!r}')
        return 1
    heads = [ln for ln in cut if ln.startswith('- [ ] **CLOSED c3')]
    want = ['c3127', 'c3126', 'c3125', 'c3124']
    got = [re.search(r'CLOSED (c3\d+)', h).group(1) for h in heads]
    if got != want:
        print(f'ABORT: range holds {got}, expected {want}')
        return 1

    # (c) live floor
    remaining = [ln for ln in kept if ln.startswith('- [ ] **CLOSED c3')]
    rem_ids = [re.search(r'CLOSED (c3\d+)', h).group(1) for h in remaining]
    if len(remaining) != 5:
        print(f'ABORT: live file would hold {len(remaining)} CLOSED blocks ({rem_ids}), want exactly 5')
        return 1

    new_queue = '\n'.join(kept)
    old_archive = open(ARCHIVE, encoding='utf-8').read()
    new_archive = HEADER + '\n' + '\n'.join(cut).rstrip('\n') + '\n\n\n' + old_archive

    # (b) lossless: every non-blank original line must survive somewhere
    live_set = set(kept)
    arch_lines = set(new_archive.split('\n'))
    missing = [ln for ln in orig if ln.strip() and ln not in live_set and ln not in arch_lines]
    if missing:
        print(f'ABORT: {len(missing)} line(s) would be LOST, e.g.:\n  {missing[0][:160]!r}')
        return 1

    print(f'range lines {START}-{END}: {len(cut)} lines, blocks {got}')
    print(f'queue.md  {len(orig)} -> {len(kept)} lines, {len(os_bytes(orig))} -> {len(os_bytes(kept))} bytes')
    print(f'live CLOSED blocks after: {rem_ids}')
    print('lossless check: PASS (every non-blank original line found in live+archive)')

    if not write:
        print('\nDRY RUN -- pass --write to apply.')
        return 0

    open(QUEUE, 'w', encoding='utf-8').write(new_queue)
    open(ARCHIVE, 'w', encoding='utf-8').write(new_archive)
    print('\nWRITTEN.')
    return 0


def os_bytes(lines):
    return '\n'.join(lines).encode('utf-8')


if __name__ == '__main__':
    sys.exit(main())
