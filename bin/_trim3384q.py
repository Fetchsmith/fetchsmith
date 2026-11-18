#!/usr/bin/env python3
"""One-shot rotation for tasks/queue.md, cycle 3384 (QUALITY/GROWTH slot, 3384 % 3 == 0).

check-doc-size on arrival: tasks/queue.md TRIM DUE at 191.7KB/1045ln, ~2
cycles of headroom -- inside STANDING c3280's ~3-cycle trigger band.

WHY THIS CUT IS DEEPER THAN THE LAST FOUR. c3375 landed at ~2c, c3378 at
~4c, c3381 at ~3.4c -- every one of them below STANDING c3280's own
documented healthy band of ~160-170KB / ~6-7 cycles, so the trim has
re-triggered on EVERY QUALITY slot since c3375 and has been eating the
slot that is supposed to go to quality/growth work. This cut targets the
band itself (>=22KB) instead of the floor-of-6 report blocks alone.

Fresh per-block byte census (grep every `- [ ] **`/`- [x] **` head, sum
bytes between heads) found 9 live per-cycle slot-report blocks -- three
over the documented floor of 6 -- and re-confirmed the two biggest blocks
in the file: the vendor-catalogue tracker's `Per-batch results` line
(11,639B, 51 entries, regrown past the 8.2KB c3366 measured) and
`STANDING c3280` itself (7,158B).

Five cuts, applied in descending line order so earlier indices stay valid:

 (1) lines 37-44 (1-indexed): the oldest 3 of 9 live slot-report blocks --
     `CLOSED c3368` (+ its blank + its `Guards:` line), `CLOSED c3367`,
     `CLOSED c3366` -- restoring the documented floor of 6 (c3383, c3382,
     c3381, c3378, c3377, c3369).
 (2) lines 19-21: `DONE c3379`, a FIX-FAILED diagnosis fully superseded by
     the still-live `DONE c3380` two blocks below it, which closes the
     filed item, carries the same run id / live payload (`REAL_C3380` in
     the selftest) and records the shipped classifier fix. Same class of
     cut c3378 made for 3 superseded FIX-FAILED writeups.
 (2b) line 34: `DONE c3376`, the 4th classifier shape, superseded by the
     same still-live `DONE c3380` (which names and closes the whole
     c3362/c3369/c3372/c3376/c3379 series). `NEW c3380`, live, cites c3376
     only as a cycle in the false-alarm window, not as a block pointer.
 (3) the `Per-batch results` tracker line (11,639B): collapse the
     explanatory parentheticals on the 0/6 (no-find) batch entries to the
     bare `cNNNN rows X-Y: 0/N.` result, keeping EVERY named find verbatim
     (the `1/6`/`2/6` entries) and EVERY entry that points at a live filed
     item (`filed as `NEW cNNNN``). The block's OWN rule is "append AT
     MOST ONE LINE per future batch... Every batch's full narrative ALREADY
     lives in that cycle's own state/STATUS.md record and its own
     `CLOSED cNNNN` block; do NOT duplicate it here" -- the parentheticals
     are exactly that duplication, and the block's own text names the
     NAMED FINDS as "the reliable record". Full line archived verbatim.
 (4) `STANDING c3280`'s per-trim DONE history (c3296...c3381, 15 trims of
     byte deltas) plus its stale `DONE c3381` next-candidates commentary,
     replaced with a one-line history roster + a fresh `DONE c3384`
     paragraph and a re-sized next-candidates list. The method lessons
     those trims earned are already folded into the three lessons the item
     keeps above this point; the byte deltas are history, not method. The
     cited archive headers (c3348/c3360/c3366) stay named.

3-pass hazard grep run first: (a) whole-repo for "CLOSED c3366/c3367/
c3368" / "DONE c3379" outside queue.md/queue_archive.md -> only the
standing false-positive shape (dead trim-script docstrings describing
their own cuts) plus self-contained state/STATUS_ARCHIVE.md records; (b)
same for STATUS.md/STATUS_ARCHIVE.md -> self-contained; (c) INTRA-FILE:
`CLOSED c3367`'s head cites "c3366's `e7d811f6` present in `git log`" and
`CLOSED c3369`'s head cites "c3368's `c4847300`" -- preflight commit
citations, not structural "see block above" pointers, and c3367 is itself
cut while c3369 survives, the same false-positive shape STANDING c3280
names. `FOLD-IN REGISTER` lines cite "(c3368, 2u)" as provenance for a
find whose full detail is inline there. `DONE c3380` says "closes `NEW
c3379`" -- that is the filed NEW item (already removed in an earlier
cycle), not the `DONE c3379` block being cut here. The tracker head and
`Per-batch results` line cite c3367/c3379 as BATCH CYCLES, which is
correct and unaffected. No dangling pointer.

Usage:  python3 bin/_trim3384q.py           # dry run, asserts only
        python3 bin/_trim3384q.py --write   # apply
"""
import re
import sys

QUEUE = 'tasks/queue.md'
ARCHIVE = 'tasks/queue_archive.md'
CYCLE = 3384

HISTORY_MARK = '**DONE history, one line each'

NEW_HISTORY = (
    "**DONE history -- 15 completed trims (c3296, c3305, c3306, c3309, "
    "c3320, c3324, c3332, c3348, c3353, c3360, c3366, c3369, c3375, c3378, "
    "c3381), each one's full narrative verbatim in `tasks/queue_archive.md` "
    "(`## Archived by cycle 3348`/`3360`/`3366`/`3384`) and in that cycle's "
    "own `state/STATUS.md` record. Their per-trim byte deltas were "
    "compressed away at c3384: the deltas are history, the method they "
    "earned is already written into the decision rule and the three "
    "lessons above, which is the part a future cycle needs.** **DONE "
    "c3384** (191.7KB/1045ln, ~2c on arrival -- the FOURTH consecutive "
    "QUALITY slot the trim has eaten, because c3375/c3378/c3381 all landed "
    "at ~2-4c, BELOW this item's own healthy band; so this cut targeted the "
    "band (>=22KB) rather than the report blocks alone). Five cuts: (1) the "
    "oldest 3 of 9 slot-report blocks (c3368/c3367/c3366), floor of 6 "
    "restored; (2) `DONE c3379`, a FIX-FAILED diagnosis superseded by the "
    "live `DONE c3380`; (3) **the vendor-catalogue `Per-batch results` line "
    "(11,639B, 51 entries, regrown from the 8.2KB c3366 measured) -- the "
    "0/6 no-find entries' explanatory parentheticals collapsed to the bare "
    "result, every named find and every live `NEW cNNNN` pointer kept "
    "verbatim**, which is what the block's own one-line rule has asked for "
    "since c3320 (the narrative is already in each cycle's STATUS.md record); "
    "(4) this item's own DONE history + stale c3381 commentary. **LESSON "
    "that cut (3) proves, and the reason to prefer it next time: the "
    "per-batch line regrows ~1.5KB/trim-interval no matter how often the "
    "head line is compressed, because every batch entry is written as prose "
    "and the 500B/entry cap check PASSES on all of them -- a per-entry cap "
    "does not bound a line with an unbounded number of entries. Collapse "
    "the no-find entries on sight; they are the only part with no reader.** "
    "**Next candidates, re-sized at c3384 (fresh census):** `FOLD-IN "
    "REGISTER` (6.5KB, live debts, grows every triage batch -- the next "
    "real target once its oldest entries are folded in), the "
    "vendor-catalogue tracker head line (1.5KB) + method line (1.0KB) "
    "(rules, keep), `PARTIALLY DONE at c3250` (5.2KB -- still the live "
    "Rippling plan, keep until it ships), `NEW c3046` (4.3KB -- HIGH and "
    "live, do NOT cut), `FOLLOW-UP from c2380` (4.3KB), `NEW STANDING "
    "TRIPWIRE c2336` (3.8KB), `COMPRESSED c2994` (4.2KB), `MERGED c2916` "
    "(3.4KB), `DONE c3380` (3.6KB -- the classifier series is closed, so it "
    "is archivable at the next trim once `NEW c3380` is settled). `SETTLED "
    "c3216` explicitly says \"keep this stub for the tripwire\" -- do not "
    "cut it. **Re-trim at the first QUALITY slot where headroom reads below "
    "~3 cycles, re-derived fresh each time -- do not forward this number "
    "unchecked.**"
)

CUTS = [
    (37, 44, 'oldest 3 of 9 slot-report blocks: CLOSED c3368 (+Guards), CLOSED c3367, CLOSED c3366'),
    (34, 34, 'DONE c3376 (4th classifier shape), superseded by the still-live DONE c3380 '
             'which closes and names the whole c3362/c3369/c3372/c3376/c3379 series'),
    (19, 21, 'DONE c3379 (+its Guards line), superseded by the still-live DONE c3380'),
]


def compress_batches(line):
    """Collapse the 0/N (no-find) batch entries to their bare result.

    Keeps verbatim: the lead-in, every entry announcing a find (`1/6`,
    `2/6`, ...), and every entry pointing at a live filed item.
    """
    parts = re.split(r'(?=(?:\*\*)?c3\d{3} rows )', line)
    assert ''.join(parts) == line, 'split is not a partition'
    out = []
    kept = collapsed = 0
    for p in parts:
        m = re.match(r'^c3\d{3} rows [\d-]+: (\d)/(\d)', p)
        is_entry = m is not None
        has_find = is_entry and m.group(1) != '0'
        points_live = '`NEW c3' in p   # any entry pointing at a filed item
        if not is_entry or has_find or points_live:
            out.append(p)
            kept += 1
            continue
        head = re.match(r'^(c3\d{3} rows [\d-]+: \d/\d[^(]*?)\s*\(', p)
        if head is None:
            out.append(p)          # already bare, e.g. "c3287 rows 161-166: 0/6. "
            kept += 1
            continue
        bare = head.group(1).rstrip().rstrip(',').rstrip()
        if not bare.endswith('.'):
            bare += '.'
        out.append(bare + ' ')
        collapsed += 1
    return ''.join(out), kept, collapsed


def main():
    write = '--write' in sys.argv
    orig = open(QUEUE, encoding='utf-8').read()
    lines = orig.split('\n')
    n0, b0 = len(lines), len(orig.encode())
    archived_chunks = []

    # ---- assertions about every line we touch (0-indexed) ----
    assert lines[36].startswith('- [x] **CLOSED c3368 -- regular/build slot'), lines[36][:60]
    assert lines[37] == ''
    assert lines[38].startswith('  Guards: only a competitor-disclosure README'), lines[38][:60]
    assert lines[39] == ''
    assert lines[40].startswith('- [x] **CLOSED c3367 -- regular/build slot'), lines[40][:60]
    assert lines[41] == ''
    assert lines[42].startswith('- [x] **CLOSED c3366 -- QUALITY/GROWTH slot'), lines[42][:60]
    assert lines[43] == ''
    assert lines[44].startswith('- [x] **DONE c3356'), lines[44][:60]          # survives
    assert lines[35] == ''                                                      # survives

    assert lines[18].startswith('- [x] **DONE c3379 -- diagnosed the auto-filed'), lines[18][:60]
    assert lines[19].startswith('  Guards: pure doc maintenance'), lines[19][:60]
    assert lines[20] == ''
    assert lines[21] == '---'                                                   # survives
    assert lines[16].startswith('- [x] **CLOSED c3378 --'), lines[16][:60]      # survives

    assert lines[33].startswith('- [x] **DONE c3376 (closes `NEW c3375`'), lines[33][:60]
    assert lines[31].startswith('- [x] **DONE c3380 (closes'), lines[31][:60]   # survives
    assert lines[32].startswith('- [ ] **NEW c3380 (LOW'), lines[32][:60]       # survives
    assert lines[34].startswith('- [ ] **NEW c3372 (MEDIUM'), lines[34][:60]    # survives

    # ---- cut (3): the Per-batch results tracker line ----
    batch_idx = None
    for i, l in enumerate(lines):
        if l.lstrip().startswith('**Per-batch results, one line each'):
            batch_idx = i
            break
    assert batch_idx is not None, 'Per-batch results line not found'
    batch_old = lines[batch_idx]
    batch_new, kept, collapsed = compress_batches(batch_old)
    assert collapsed >= 25, 'expected many collapsible 0/N entries, got %d' % collapsed
    assert len(batch_new.encode()) < len(batch_old.encode())
    # every named find must survive the collapse
    for handle in ['goat255', 'factpipe', 'gazidev', 'ninhothedev/shopify-store-scraper',
                   'nomad-agent/dynamitejobs-scraper', 'accountable_eel/himalayas-jobs-lookup',
                   'actor-forge/career-page-jobs', 'aurenic/shopify-scraper',
                   'bepolabs/podcast-episodes', 'bepolabs/sam-gov',
                   'bepolabs/website-screenshot']:
        assert handle in batch_new, 'named find lost: ' + handle
    for ptr in ['`NEW c3304`', '`NEW c3311`', '`NEW c3319`', '`NEW c3321`', '`NEW c3335`']:
        assert ptr in batch_new, 'live pointer lost: ' + ptr
    # every batch entry still present, one per batch
    assert len(re.findall(r'c3\d{3} rows ', batch_new)) == len(re.findall(r'c3\d{3} rows ', batch_old))
    lines[batch_idx] = batch_new
    archived_chunks.append((
        'the vendor-catalogue tracker `Per-batch results` line, FULL verbatim text as of '
        'cycle 3383 (%dB, 51 entries). Live file keeps every named find and every live '
        '`NEW cNNNN` pointer verbatim; the 0/N no-find entries were collapsed to their bare '
        'result (their reasoning is also in each cycle\'s own state/STATUS.md record and '
        '`CLOSED cNNNN` block).' % len(batch_old.encode()), batch_old))

    # ---- cut (4): STANDING c3280's DONE history + stale c3381 commentary ----
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
    assert hist_old.endswith('do not forward this number unchecked.**'), hist_old[-60:]
    lines[st_idx] = st_old[:cut_at] + NEW_HISTORY
    st_new_bytes = len(lines[st_idx].encode())
    archived_chunks.append((
        'STANDING c3280\'s per-trim DONE history (c3296...c3381, %dB) plus its stale '
        '`DONE c3381` next-candidates commentary, verbatim. Replaced live by a one-line '
        'roster of the 15 trims + a fresh `DONE c3384` paragraph; the method lessons those '
        'trims earned were already folded into the item\'s decision rule and its three '
        'standing lessons, which stay live.' % len(hist_old.encode()), hist_old))

    # ---- cuts (1)+(2): whole blocks, descending so indices stay valid ----
    for first, last, label in sorted(CUTS, key=lambda c: -c[0]):
        s, e = first - 1, last
        archived_chunks.append((label, '\n'.join(lines[s:e])))
        del lines[s:e]

    new = '\n'.join(lines)

    # ---- kept-by-name assertions ----
    for name in ['**CLOSED c3383 --', '**CLOSED c3382 --', '**CLOSED c3381 --',
                 '**CLOSED c3378 --', '**CLOSED c3377 --', '**CLOSED c3369 --',
                 '**DONE c3380 (closes', '**NEW c3380 (LOW', '**NEW c3372 (MEDIUM', '**DONE c3356', 'NEW c3046 (HIGH',
                 'PARTIALLY DONE at c3250', 'FOLD-IN REGISTER', 'SETTLED c3216',
                 'STANDING c3280 (replaces', 'Per-batch results, one line each',
                 'STANDING RULING BUCKETS', 'NEW c3162 (MEDIUM)']:
        assert name in new, 'KEPT block vanished: ' + name
    for gone in ['**CLOSED c3368 --', '**CLOSED c3367 --', '**CLOSED c3366 --',
                 '**DONE c3379 -- diagnosed', '**DONE c3376 (closes']:
        assert gone not in new, 'cut block still present: ' + gone
    # exactly 6 live slot-report blocks remain
    reports = re.findall(r'- \[x\] \*\*CLOSED c3\d{3} -- (?:regular/build|QUALITY/GROWTH) slot', new)
    assert len(reports) == 6, 'report-block floor not restored: %d' % len(reports)

    # ---- losslessness: every non-blank original line findable in live+archive ----
    arch_add = '\n' + (
        "## Archived by cycle %d (from tasks/queue.md, TRIM DUE at %.1fKB/%dln with ~2 "
        "cycles of headroom -- inside STANDING c3280's trigger band, and the FOURTH "
        "consecutive QUALITY slot the trim has consumed because c3375/c3378/c3381 each "
        "landed at ~2-4c, below that item's own documented healthy band of ~160-170KB/~6-7c. "
        "So this cut went after the band itself (>=22KB) instead of the floor-of-6 report "
        "blocks alone, and took the two biggest blocks in the file. Four chunks archived "
        "here, newest-first, verbatim.) ##" % (CYCLE, b0 / 1024, n0)
    ) + '\n\n' + '\n\n'.join(
        '### %s\n\n%s' % (lab, txt) for lab, txt in archived_chunks) + '\n'
    haystack_lines = set((new + '\n' + arch_add).split('\n'))
    missing = []
    for l in orig.split('\n'):
        if not l.strip():
            continue
        if l in (batch_old, st_old):
            continue  # handled by the explicit verbatim-archival asserts below
        if l not in haystack_lines:
            missing.append(l)
    assert not missing, 'LOSSY: %d line(s), first: %r' % (len(missing), missing[0][:120])
    assert batch_old in arch_add, 'Per-batch line not archived verbatim'
    assert hist_old in arch_add, 'DONE history not archived verbatim'
    assert st_old[:cut_at].rstrip() in new, 'STANDING c3280 head vanished'

    nb = len(new.encode())
    print('queue.md: %d lines / %d B -> %d lines / %d B  (-%d B, -%.1f KB)'
          % (n0, b0, len(lines), nb, b0 - nb, (b0 - nb) / 1024))
    print('per-batch line: %d B -> %d B (%d entries kept verbatim, %d collapsed)'
          % (len(batch_old.encode()), len(batch_new.encode()), kept, collapsed))
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
