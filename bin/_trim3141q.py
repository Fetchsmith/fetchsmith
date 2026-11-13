#!/usr/bin/env python3
"""One-shot queue.md trim for cycle 3141 (QUALITY slot, 3141 % 3 == 0).

Archives the 6 oldest live 'CLOSED c3' blocks -- c3133, c3132, c3130, c3131,
c3129, c3128 -- restoring the newest-5 floor (11 live blocks counted fresh via
`grep -c '^- \\[ \\] \\*\\*CLOSED c3'`, down to 5: c3140, c3139, c3136,
c3137/c3138, c3134/c3135).

One contiguous range (lines 48-81, 1-indexed inclusive, incl. trailing blank)
holds all 6 CLOSED blocks PLUS three interleaved non-CLOSED items that only
make sense next to the CLOSED blocks they reference -- DONE c3132 ("see
CLOSED c3132 below"), DONE c3133 ("see CLOSED c3133 below" implicitly via its
own evidence paragraph), and CORRECTION c3132 ("to CLOSED c3131's root
cause") -- moving them separately would leave dangling "below"/"to" pointers
in the archive-vs-live split. Hazard grep (RULE 1/8) over bin/actors/site/
notes/state found zero live file-path pointers into any of these 9 headers
outside queue.md itself and each block's own narrative mentions inside
state/STATUS.md's per-cycle blocks (self-contained history in a separate
document, same false-positive class as every prior trim).

Self-verifying per bin/_trim3132q.py: refuses to write unless (a) the range
starts at the expected CLOSED c3133 header and ends on a blank line, (b) the
exact header sequence inside the range matches what RULE 7 expects (9 heads,
none stray), (c) every non-blank original line is still findable in
live+archive afterwards (lossless), and (d) the live file ends up with
exactly 5 'CLOSED c3' blocks.

Dry-run by default; pass --write to apply.
"""
import re
import sys

QUEUE = '/root/agent/tasks/queue.md'
ARCHIVE = '/root/agent/tasks/queue_archive.md'

START, END = 48, 81  # 1-indexed, inclusive

EXPECT_HEAD = '- [ ] **CLOSED c3133 -- Regular/GROWTH slot'
EXPECT_HEADERS = [
    '- [ ] **CLOSED c3133',
    '- [ ] **CLOSED c3132',
    '- [ ] **CLOSED c3130',
    '- [x] **DONE c3132',
    '- [x] **DONE c3133',
    '- [ ] **CORRECTION c3132',
    '- [ ] **CLOSED c3131',
    '- [ ] **CLOSED c3129',
    '- [ ] **CLOSED c3128',
]
WANT_REMAINING = ['c3140', 'c3139', 'c3136', 'c3137/c3138', 'c3134/c3135']

HEADER = (
    '## Archived by cycle 3141 trim (QUALITY slot; 11 live CLOSED blocks counted fresh, '
    "double the floor of 5 -- c3132's own rotation left 5, then c3133/c3134-c3135/c3136/"
    "c3137-c3138/c3139/c3140 each prepended one against zero outbound in between) -- "
    '`CLOSED c3133`, `CLOSED c3132`, `CLOSED c3130`, `DONE c3132`, `DONE c3133`, '
    '`CORRECTION c3132`, `CLOSED c3131`, `CLOSED c3129` and `CLOSED c3128` archived '
    'verbatim as one contiguous range (the three non-CLOSED items only make sense beside '
    'the CLOSED blocks they point at). Newest-first below, same order as the source file.\n'
)


def block_heads(lines):
    return [ln for ln in lines if ln.startswith('- [ ] **') or ln.startswith('- [x] **')]


def main() -> int:
    write = '--write' in sys.argv
    orig = open(QUEUE, encoding='utf-8').read().split('\n')

    cut = orig[START - 1:END]
    kept = orig[:START - 1] + orig[END:]

    if not cut[0].startswith(EXPECT_HEAD):
        print(f'ABORT: line {START} is not the expected c3133 header:\n  {cut[0][:120]!r}')
        return 1
    if cut[-1].strip() != '':
        print(f'ABORT: line {END} is not blank (would glue two items together):\n  {cut[-1][:120]!r}')
        return 1

    heads = block_heads(cut)
    got_prefixes = []
    for h in heads:
        m = re.match(r'(- \[.\] \*\*(?:CLOSED|DONE|CORRECTION) c3\d+)', h)
        got_prefixes.append(m.group(1) if m else h[:40])
    if got_prefixes != EXPECT_HEADERS:
        print('ABORT: header sequence mismatch.')
        print(f'  got:  {got_prefixes}')
        print(f'  want: {EXPECT_HEADERS}')
        return 1

    remaining = [ln for ln in kept if ln.startswith('- [ ] **CLOSED c3')]
    rem_ids = [re.search(r'CLOSED (c3[\d/c]*)', h).group(1) for h in remaining]
    if len(remaining) != 5:
        print(f'ABORT: live file would hold {len(remaining)} CLOSED blocks ({rem_ids}), want exactly 5')
        return 1
    if rem_ids != WANT_REMAINING:
        print(f'ABORT: remaining ids {rem_ids} != expected {WANT_REMAINING}')
        return 1

    new_queue = '\n'.join(kept)
    old_archive = open(ARCHIVE, encoding='utf-8').read()
    new_archive = HEADER + '\n' + '\n'.join(cut).rstrip('\n') + '\n\n\n' + old_archive

    live_set = set(kept)
    arch_lines = set(new_archive.split('\n'))
    missing = [ln for ln in orig if ln.strip() and ln not in live_set and ln not in arch_lines]
    if missing:
        print(f'ABORT: {len(missing)} line(s) would be LOST, e.g.:\n  {missing[0][:160]!r}')
        return 1

    print(f'range lines {START}-{END}: {len(cut)} lines, headers {got_prefixes}')
    print(f'queue.md  {len(orig)} -> {len(kept)} lines, '
          f'{len(os_bytes(orig))} -> {len(os_bytes(kept))} bytes')
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
