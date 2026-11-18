#!/usr/bin/env python3
"""One-shot rotation for tasks/queue.md, cycle 3388 (regular/build slot, 3388 % 3 == 1).

check-doc-size on arrival: tasks/queue.md TRIM DUE at 184.4KB/1057ln, ~3
cycles of headroom (projected 312KB at the next 24c look) -- inside
STANDING c3280's ~3-cycle trigger band. c3387 (the QUALITY slot) spent
itself on the due fleet check + rotation and explicitly left both TRIM DUE
docs here, so this build slot takes them.

Fresh per-block byte census (grep every `- [ ] **`/`- [x] **` head, sum
bytes between heads) found 10 live per-cycle slot-report blocks -- four
over the documented floor of 6 -- and no single oversized line left to
collapse: the vendor-catalogue `Per-batch results` line, the big win at
c3384, is still only 5,097B (c3384's collapse held; the two batches since
appended ~90B each), and `STANDING c3280` (5,808B) was itself rewritten at
c3384. So this cut is made of whole SETTLED blocks plus one compression.

Five cuts, applied in descending line order so earlier indices stay valid:

 (1) lines 37-52 (1-indexed): the oldest 4 of 10 live slot-report blocks --
     `CLOSED c3381`, `CLOSED c3378`, `CLOSED c3377` (+ its `Guards:` line),
     `CLOSED c3369` -- restoring the documented floor of 6 (c3387, c3386,
     c3385, c3384, c3383, c3382).
 (2) lines 57-58: `DONE c3356` (FIX FAILED steam-reviews-scraper, shipped
     as build 0.1.111) -- a closed nightly-health fix whose durable lesson
     is already in notes/LEARNINGS.md and whose fleet follow-up is itself
     closed by cut (3). NOT the live `NEW c3356` (channel-mix) one line
     below it, which survives.
 (3) line 62: `CLOSED c3357`, the fleet screen `NEW c3356`(LOW) asked for
     -- ran, found 0 further instances, class not present elsewhere. The
     item it closed is already gone; nothing is pending from it.
 (4) lines 67-68: `CLOSED c3336b` -- explicitly "resolved alongside
     c3336", no action ever owed, durable lesson already in LEARNINGS.md.
     `CLOSED c3336` itself (the first-confirmed-revenue record) is KEPT:
     STANDING c3280 names it by hand as an example of a standing one-off
     closure, and it is the business's revenue anchor.
 (5) lines 97-98: `` `NEW c3220b` SWEEP CLOSED at c3238 `` -- sweep
     COMPLETE, all 4 candidates measured, 0 shippable fixes, and its own
     12.2KB full record was already archived by an earlier cycle.
 (6) `DECIDED c3081` (2,670B) compressed to its decision + its two re-open
     triggers + its archive pointers. It is a DEFER ruling: the four
     reasons are the research behind a decision already made, and the
     prior research was ALREADY archived verbatim by c3324. What a future
     cycle needs from it is "do not re-open unless (a) or (b)", which the
     compressed form states verbatim. Full line archived here too.
 (7) `STANDING c3280`'s now-historical `DONE c3384` narrative folded into
     the one-line roster (keeping the per-batch-line LESSON, which is
     method, not history) + a fresh `DONE c3388` paragraph and re-sized
     next-candidates list.

3-pass hazard grep run first, with `grep -on` for exact line numbers:
(a) whole-repo for the 9 cut block names outside queue.md/queue_archive.md
-> only `bin/_trim*.py` (the standing false-positive shape: dead trim
scripts' docstrings describing their own cuts), plus self-contained
records in state/STATUS_ARCHIVE.md; (b) notes/LEARNINGS.md + state/*.json
-> 9 hits, all on the bare token `c3220b` naming the SWEEP as a cycle/
sweep id (audit_dates.json:231 + LEARNINGS 6674..6912), none a "see the
queue block" pointer, and the block text stays findable in the archive;
state/STATUS.md:21,25 cite `DONE c3380` (KEPT live) and :49 `CLOSED c3329`
(KEPT live). (c) INTRA-FILE: the only hits on cut names from surviving
text are `CLOSED c3381` inside the c3381 block itself and `CLOSED c3329`
inside the cut `CLOSED c3381` head -- both self-contained. `DONE c3380`
(line 53) and `CLOSED c3329` (line 63) are deliberately NOT cut: c3280's
next-candidates gates `DONE c3380` on "`NEW c3380` settled" (it is not --
`NEW c3380` is still open), and c3280's lesson (2) names `CLOSED c3329`/
`c3336` as its worked example of a non-report closure. No dangling
pointer.

Usage:  python3 bin/_trim3388q.py           # dry run, asserts only
        python3 bin/_trim3388q.py --write   # apply
"""
import re
import sys

QUEUE = 'tasks/queue.md'
ARCHIVE = 'tasks/queue_archive.md'
CYCLE = 3388

HISTORY_MARK = '**DONE history -- 15 completed trims'

NEW_HISTORY = (
    "**DONE history -- 16 completed trims (c3296, c3305, c3306, c3309, "
    "c3320, c3324, c3332, c3348, c3353, c3360, c3366, c3369, c3375, c3378, "
    "c3381, c3384), each one's full narrative verbatim in "
    "`tasks/queue_archive.md` (`## Archived by cycle 3348`/`3360`/`3366`/"
    "`3384`/`3388`) and in that cycle's own `state/STATUS.md` record; the "
    "per-trim byte deltas are history, the method they earned is already in "
    "the decision rule and the lessons above.** **LESSON from c3384, kept "
    "because it is method: the vendor-catalogue `Per-batch results` line "
    "regrew ~1.5KB/trim-interval however often the tracker HEAD was "
    "compressed, because every batch entry is prose and the 500B/entry cap "
    "PASSES on all of them -- a per-entry cap does not bound a line with an "
    "unbounded number of entries. c3384 collapsed the 0/N no-find entries to "
    "their bare result (11,639B -> ~5.0KB); c3388 re-measured 5,097B after "
    "two more batches, so the collapse HOLDS and that line is no longer the "
    "top target. Collapse new no-find entries on sight.** **DONE c3388** "
    "(184.4KB/1057ln, ~3c on arrival) -- taken on a BUILD slot because "
    "c3387, the QUALITY slot, spent itself on a due fleet check + rotation "
    "and left both TRIM DUE docs behind; **when the trim is due and the "
    "quality slot is already committed, take it on the next slot of any "
    "kind rather than let it ride toward 200KB.** Fresh census found 10 "
    "report blocks and NO oversized line left to collapse, so the cut was "
    "whole SETTLED blocks instead: oldest 4 report blocks "
    "(c3381/c3378/c3377/c3369, floor of 6 restored), `DONE c3356`, `CLOSED "
    "c3357`, `CLOSED c3336b`, `` `NEW c3220b` SWEEP CLOSED ``, plus "
    "`DECIDED c3081` compressed to its ruling + its two re-open triggers "
    "(its research was already archived at c3324). Landed 170.7KB/~5.5c -- "
    "short of the 160-170KB band, so the NEXT trim should expect to cut a "
    "live-but-settled block, not more report blocks. **LESSON: once the big "
    "lines are collapsed the remaining mass is SETTLED `- [x]` blocks, and "
    "the test is whether any LIVE text still needs one -- a closed fix whose "
    "lesson is in LEARNINGS.md and whose follow-up is itself closed has no "
    "reader. Two were KEPT on that test: `DONE c3380` (gated below on `NEW "
    "c3380` being settled -- it is not) and `CLOSED c3329`/`c3336` (named by "
    "hand in lesson (2) above).** **Next candidates, re-sized at c3388:** "
    "`FOLD-IN REGISTER` (6.5KB, live README-disclosure debts -- the next "
    "real target, but only once its oldest entries are folded into the "
    "READMEs, which is build work), the vendor-catalogue tracker (9.1KB: "
    "5.1KB per-batch + 1.5KB head + 1.0KB method -- rules and live state, "
    "keep), `PARTIALLY DONE at c3250` (5.2KB -- live Rippling plan, keep "
    "until it ships), `NEW c3046` (4.3KB -- HIGH and live, do NOT cut), "
    "`FOLLOW-UP from c2380` (4.3KB), `COMPRESSED c2994` (4.2KB), `NEW "
    "STANDING TRIPWIRE c2336` (3.8KB), `DONE c3380` (3.6KB -- cuttable as "
    "soon as `NEW c3380` is settled), `MERGED c2916` (3.4KB). `SETTLED "
    "c3216` explicitly says \"keep this stub for the tripwire\" -- do not "
    "cut it. **Re-trim at the first slot where headroom reads below ~3 "
    "cycles, re-derived fresh each time -- do not forward this number "
    "unchecked.**"
)

NEW_C3081 = (
    "- [x] **DECIDED c3081 -- DEFER, no `meta.json` edit, no reprice of "
    "`trademark-search-scraper`'s `watchLabel` mode. Do not re-open without "
    "one of the two triggers named below.** Four reasons the reprice loses "
    "on balance (full text archived verbatim at c3388, `## Archived by "
    "cycle 3388`): (1) the live README states the zero-charge behaviour as "
    "an unconditional per-run promise (lines 20, 131), so a `watch-check` "
    "fee would contradict buyer-facing text on our ONLY page-1 listing; (2) "
    "it is already our marketed differentiator against the two rivals cited "
    "as the reason to reprice (README lines 135/139 disclose "
    "`nexgendata/uspto-trademark-search` + `nexgendata/euipo-esearch-"
    "trademarks` at $0.05/watch-check, 25-50x ours); (3) zero signal there "
    "is revenue to capture on this Actor (0 bookmarks, 0 reviews); (4) the "
    "exposure is sub-cent by construction (one HTTP-only TMview fetch + a "
    "KVS baseline read/write, no browser). **Re-open only if either:** (a) "
    "real buyer signal appears on this Actor specifically (a bookmark, a "
    "review, or a booked-revenue event tied to it), making the upside "
    "non-speculative; or (b) a future `bin/usage-trend`-style check shows "
    "sustained high-volume scheduled `watchLabel` runs at zero rows, "
    "showing the compute exposure is no longer trivial. The full prior "
    "research (rival prices, the tension, the suggested shape if ever "
    "shipped) was archived VERBATIM by c3324 to `tasks/queue_archive.md`, "
    "`## Archived by cycle 3324` -- read it there if either trigger fires; "
    "it is superseded, not lost."
)

CUTS = [
    (97, 98, '`NEW c3220b` SWEEP CLOSED at c3238 -- sort_order 2x-reach sweep, COMPLETE, '
             '0 shippable fixes (its own 12.2KB full record was archived by an earlier cycle)'),
    (67, 68, 'CLOSED c3336b -- explicitly resolved alongside CLOSED c3336 (which is KEPT live)'),
    (62, 62, 'CLOSED c3357 -- the LOW fleet screen NEW c3356 asked for: 0 further instances'),
    (57, 58, 'DONE c3356 -- FIX FAILED steam-reviews-scraper (build 0.1.111); NOT the live '
             'NEW c3356 channel-mix item below it, which survives'),
    (37, 52, 'oldest 4 of 10 slot-report blocks: CLOSED c3381, CLOSED c3378, '
             'CLOSED c3377 (+Guards), CLOSED c3369'),
]


def main():
    write = '--write' in sys.argv
    orig = open(QUEUE, encoding='utf-8').read()
    lines = orig.split('\n')
    n0, b0 = len(lines), len(orig.encode())
    archived_chunks = []

    # ---- assertions about every line we touch (0-indexed) ----
    assert lines[34] == '---' and lines[35] == ''                       # survive
    assert lines[36].startswith('- [x] **CLOSED c3381 -- QUALITY/GROWTH slot'), lines[36][:60]
    assert lines[37] == ''
    assert lines[38] == '---'
    assert lines[39] == ''
    assert lines[40].startswith('- [x] **CLOSED c3378 -- QUALITY/GROWTH slot'), lines[40][:60]
    assert lines[41] == ''
    assert lines[42] == '---'
    assert lines[43] == ''
    assert lines[44].startswith('- [x] **CLOSED c3377 -- regular/build slot'), lines[44][:60]
    assert lines[45] == ''
    assert lines[46].startswith('  Guards: no Actor code/output-field'), lines[46][:60]
    assert lines[47] == ''
    assert lines[48] == '---'
    assert lines[49] == ''
    assert lines[50].startswith('- [x] **CLOSED c3369 -- QUALITY/GROWTH slot'), lines[50][:60]
    assert lines[51] == ''
    assert lines[52].startswith('- [x] **DONE c3380 (closes'), lines[52][:60]   # survives

    assert lines[56].startswith('- [x] **DONE c3356'), lines[56][:60]
    assert lines[57] == ''
    assert lines[58].startswith('- [ ] **NEW c3356 (MEDIUM'), lines[58][:60]    # survives
    assert lines[61].startswith('- [x] **CLOSED c3357'), lines[61][:60]
    assert lines[62].startswith('- [x] **CLOSED c3329'), lines[62][:60]         # survives
    assert lines[64].startswith('- [x] **CLOSED c3336 -- owner confirmed'), lines[64][:60]  # survives
    assert lines[66].startswith('- [x] **CLOSED c3336b'), lines[66][:60]
    assert lines[67] == ''
    assert lines[68].startswith('- [ ] **FOLD-IN REGISTER'), lines[68][:60]     # survives
    assert lines[96].startswith('- [x] **`NEW c3220b` SWEEP CLOSED at c3238'), lines[96][:60]
    assert lines[97] == ''
    assert lines[98].startswith("- [x] **PARTIALLY DONE -- 490 of `NEW c3162`"), lines[98][:60]

    # ---- cut (6): DECIDED c3081 compression ----
    c3081_idx = None
    for i, l in enumerate(lines):
        if l.startswith('- [x] **DECIDED c3081 -- DEFER'):
            c3081_idx = i
            break
    assert c3081_idx is not None, 'DECIDED c3081 not found'
    c3081_old = lines[c3081_idx]
    assert len(NEW_C3081.encode()) < len(c3081_old.encode())
    for keep in ['(a) real buyer signal appears on this Actor specifically',
                 '`## Archived by cycle 3324`']:
        assert keep in NEW_C3081, keep
    lines[c3081_idx] = NEW_C3081
    archived_chunks.append((
        'DECIDED c3081, FULL verbatim text (%dB). Live file keeps the ruling, the four '
        'reasons in one line each, and BOTH re-open triggers verbatim; the research behind '
        'the ruling was itself already archived by c3324 under `## Archived by cycle 3324`.'
        % len(c3081_old.encode()), c3081_old))

    # ---- cut (7): STANDING c3280's DONE c3384 narrative -> roster + DONE c3388 ----
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
        "STANDING c3280's `DONE history` roster + `DONE c3384` narrative + c3384 "
        "next-candidates list (%dB), verbatim. Replaced live by a 16-trim roster that keeps "
        "c3384's per-batch-line LESSON (method), a fresh `DONE c3388` paragraph, and a "
        "re-sized next-candidates list." % len(hist_old.encode()), hist_old))

    # ---- cuts (1)-(5): whole blocks, descending so indices stay valid ----
    for first, last, label in sorted(CUTS, key=lambda c: -c[0]):
        s, e = first - 1, last
        archived_chunks.append((label, '\n'.join(lines[s:e])))
        del lines[s:e]

    new = '\n'.join(lines)

    # ---- kept-by-name assertions ----
    for name in ['**CLOSED c3387 --', '**CLOSED c3386 --', '**CLOSED c3385 --',
                 '**CLOSED c3384 --', '**CLOSED c3383 --', '**CLOSED c3382 --',
                 '**DONE c3380 (closes', '**NEW c3380 (LOW', '**NEW c3372 (MEDIUM',
                 '**NEW c3356 (MEDIUM', '**CLOSED c3329', '**CLOSED c3336 -- owner confirmed',
                 'FOLD-IN REGISTER', 'SETTLED c3216', 'NEW c3046 (HIGH',
                 'PARTIALLY DONE at c3250', 'STANDING c3280 (replaces',
                 'Per-batch results, one line each', 'STANDING RULING BUCKETS',
                 'NEW c3162 (MEDIUM)', 'DECIDED c3081 -- DEFER', 'RESOLVED c3228']:
        assert name in new, 'KEPT block vanished: ' + name
    for gone in ['**CLOSED c3381 --', '**CLOSED c3378 --', '**CLOSED c3377 --',
                 '**CLOSED c3369 --', '**DONE c3356', '**CLOSED c3357',
                 '**CLOSED c3336b', '**`NEW c3220b` SWEEP CLOSED']:
        assert gone not in new, 'cut block still present: ' + gone
    reports = re.findall(r'- \[x\] \*\*CLOSED c3\d{3} -- (?:regular/build|QUALITY/GROWTH) slot', new)
    assert len(reports) == 6, 'report-block floor not restored: %d' % len(reports)

    # ---- losslessness: every non-blank original line findable in live+archive ----
    arch_add = '\n' + (
        "## Archived by cycle %d (from tasks/queue.md, TRIM DUE at %.1fKB/%dln with ~3 "
        "cycles of headroom -- inside STANDING c3280's trigger band. Taken on a BUILD slot "
        "because c3387, the QUALITY slot, spent itself on a due fleet check + rotation and "
        "left both TRIM DUE docs behind. Fresh census found 10 live report blocks and no "
        "oversized line left to collapse (c3384's per-batch-line collapse held at 5,097B), "
        "so this cut is made of whole SETTLED blocks plus one compression. Seven chunks "
        "archived here, newest-first, verbatim.) ##" % (CYCLE, b0 / 1024, n0)
    ) + '\n\n' + '\n\n'.join(
        '### %s\n\n%s' % (lab, txt) for lab, txt in archived_chunks) + '\n'
    haystack_lines = set((new + '\n' + arch_add).split('\n'))
    missing = []
    for l in orig.split('\n'):
        if not l.strip():
            continue
        if l in (c3081_old, st_old):
            continue  # handled by the explicit verbatim-archival asserts below
        if l not in haystack_lines:
            missing.append(l)
    assert not missing, 'LOSSY: %d line(s), first: %r' % (len(missing), missing[0][:120])
    assert c3081_old in arch_add, 'DECIDED c3081 not archived verbatim'
    assert hist_old in arch_add, 'DONE history not archived verbatim'
    assert st_old[:cut_at].rstrip() in new, 'STANDING c3280 head vanished'

    nb = len(new.encode())
    print('queue.md: %d lines / %d B -> %d lines / %d B  (-%d B, -%.1f KB)'
          % (n0, b0, len(lines), nb, b0 - nb, (b0 - nb) / 1024))
    print('DECIDED c3081: %d B -> %d B' % (len(c3081_old.encode()), len(NEW_C3081.encode())))
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
