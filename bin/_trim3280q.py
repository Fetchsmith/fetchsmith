#!/usr/bin/env python3
"""One-shot DEEP rotation for tasks/queue.md, cycle 3280 (regular slot, 3280 % 3 == 1).

`check-doc-size` read `tasks/queue.md` **TRIM DUE at 195.5KB/1090ln with ~1
cycle of headroom** on arrival (+5440 B/cycle, projected 323KB at its own
next look -- past both the 200KB trim line and the 256KB Read cap). The
trim has now been deferred by c3276/c3277/c3278/c3279 in favour of real
backlog work; this cycle's preflight was FULLY CLEAN (`checks-due --all`
NONE DUE, soonest `check-dead-endpoint-docs` c3283; `audit-due --all`
FLEET ROTATIONS NONE DUE; `inbox-triage new` NONE UNTRIAGED, 82 msgs;
`bin/revenue` unchanged, $0 booked / 27 Actors / 54 users / no buyer
signal), so there is no rotation to lose by taking it.

WHY THIS CUT IS DEEPER THAN c3274's. c3274 archived 8 report blocks
(217.9 -> 177.4KB) and `check-doc-size` still read TRIM DUE 4 cycles
later, because it projects 24 cycles ahead and the file appends ~2.4KB of
CLOSED cycle-report per cycle (~58KB per check interval). A cut that
frees less than that is arithmetically guaranteed to read DUE again
immediately. This cut frees ~57KB to land near ~140KB, i.e. at the
file's actual steady state for a 24-cycle interval, rather than shaving
the top.

Block inventory re-derived FRESH this cycle (never trust a forwarded
number -- RULE 6b): a per-block byte/line census over every `- [ ] **` /
`- [x] **` head found **17 genuine "cycle N did X" report blocks**, and
confirmed again that they are NOT a chronological prefix (live standing
`NEW c3268`/`NEW c3269`/`NEW c3272` items are interleaved between them).
The census also found the single largest object in the file: the
`NEW c3162` vendor-catalogue triage log at lines 68-81, **33.1KB / 16.5%
of the whole file**, of which line 68 is the live index and lines 69-80
are twelve per-cycle detail paragraphs (c3253, c3248, c3247, c3246,
c3244, c3245, c3243, c3242, c3241, c3239, c3217, c3218) whose content is
already duplicated in each cycle's `state/STATUS.md` record. That log had
never been rotated; archiving it is worth more than any report block.

FIVE cut ranges, each boundary verified by direct read, not assumed:
  (17, 18) -- CLOSED c3272 (the live `NEW c3272` at 19-20 stays).
  (21, 22) -- CLOSED c3269 (the live `NEW c3269` at 23-24 stays).
  (25, 28) -- CLOSED c3268 + CLOSED c3270, contiguous (the three live
              `NEW c3268` items at 29-34 stay).
  (35, 65) -- CORRECTED AND CLOSED c3265; the c3266/c3267 doc-trim
              handoff block (40-49, now superseded -- this cycle writes a
              fresh one); CLOSED c3252, c3253, c3254, c3255 (the
              contiguous run c3274 and c3279 both named as next).
  (68, 80) -- the vendor-catalogue triage log: the stale index line 68
              (it still said "next 6 at c3269 ... rows 119-124", three
              cycles out of date -- c3277/c3278/c3279 did rows 119-136)
              plus its 12 detail paragraphs. Archived VERBATIM and
              replaced in place by INDEX_REPLACEMENT below, which carries
              the live state only.

Live CLOSED report blocks after the cut: 7 (c3279, c3278, c3277, c3276,
c3275, c3274, c3273) -- still above the documented floor of 5.

HAZARD GREP RAN FIRST, three passes:
  (a) `grep -rn "see tasks/queue.md\\|tasks/queue.md, cycle" bin actors
      site notes state` -> only the two long-standing false positives
      (`bin/store-rank:152`, `bin/git-maintain:24`, both pre-existing and
      about unrelated cycles) plus dead `bin/_trimNNNNq.py` docstrings
      and archive narrative. Same conclusion as every prior trim.
  (b) by-name sweep for c3272/c3269/c3268/c3270/c3265/c3266/c3267/
      c3252/c3253/c3254/c3255 across `bin actors site` -> every hit is
      inside a dead one-shot `_trimNNNNq.py`/`_triageNNNN.py` docstring
      (historical narrative ABOUT that cycle, never a live pointer INTO
      this file), plus `node_modules/axios/CHANGELOG.md` matching "c3270"
      as a commit-hash substring. No live cross-reference.
  (c) INTRA-FILE pass (the one c3240 says actually pays): scanned every
      KEPT line for a reference into a cut range. Exactly 3 hits, all
      handled, none left dangling:
        L5  (CLOSED c3274 report) -- "`CLOSED c3252/c3253/c3254/c3255`
            named as the next contiguous run to archive". Historical
            statement inside a dated report block; this cycle satisfies
            it. Left verbatim (rewriting a closed report's own text would
            be a worse defect than a satisfied pointer).
        L13 (live `NEW c3276`) -- same clause, but LIVE, so its doc-size
            sentence is updated by hand after this script runs.
        L68 -- "see `CLOSED c3269` above"; L68 is itself cut and replaced.

Usage:  python3 bin/_trim3280q.py           # dry run, asserts only
        python3 bin/_trim3280q.py --write   # apply
"""
import sys

QUEUE = 'tasks/queue.md'
ARCHIVE = 'tasks/queue_archive.md'
CYCLE = 3280

CUTS = [(17, 18), (21, 22), (25, 28), (35, 65), (68, 80)]

# Replaces the cut triage-log index line (old L68) in place. Live state only;
# the 12 per-cycle detail paragraphs it used to carry are in the archive.
INDEX_REPLACEMENT = (
    "- [x] **PARTIALLY DONE -- 136 of `NEW c3162`'s 1,485 vendor-catalogue rows triaged "
    "(c3167, c3217, c3218, c3239, c3241-c3244, c3246-c3248, c3253, c3255-c3261, c3269, "
    "c3277, c3278, c3279); 1,349 remain. COMPRESSED c3280: the 12 per-cycle detail "
    "paragraphs this item used to carry (c3217, c3218, c3239, c3241, c3242, c3243, c3244, "
    "c3245, c3246, c3247, c3248, c3253 -- 31.3KB) are archived VERBATIM in "
    "`tasks/queue_archive.md` under `## Archived by cycle 3280`; each cycle's full narrative "
    "also lives in its own `state/STATUS.md` record. Do NOT re-expand them here -- append at "
    "most a one-line result per future batch.** **Running score: 4 real undercutters found in "
    "136 rows (~3%)** -- `code-node-tools/website-screenshot-api` (c3261), "
    "`johnvc/greenhouse-job-board-api` cheap-leg index rows (c3244), "
    "`freshactors/smartrecruiters-jobs-scraper` (c3277, partial/breakeven), "
    "`locaihost/screenshot` (c3278) -- plus 2 non-price finds (the c3243 "
    "`nexgendata/shopify-store-analyzer` pivot, the c3269 `ats-jobs-scraper` stale listing) "
    "and one product gap (Rippling, c3248). Everything else was a false positive on niche "
    "vocabulary, a different product shape, or dearer than us at every tier. "
    "**NEXT: rows 137-142, none read yet** -- `datagleaner/google-play-scraper` 6u "
    "(google-play-reviews-scraper), `foxlabs/ukraine-prozorro-tenders` 6u "
    "(eu-ted-tenders-scraper), `hipersoft/onlinejobs-scraper` 6u (remote-jobs-scraper), "
    "`inexhaustible_glass/job-scraper` 6u (ats-jobs-scraper), "
    "`jungle_synthesizer/curia-eu-court-of-justice-judgment-scraper` 6u "
    "(court-records-scraper), `nabeelbaghoor/mobile-app-intelligence-api` 6u "
    "(google-play-reviews-scraper). Method is fixed: clone `bin/_triage3279.py`, price via "
    "`check-price-superiority.effective(pricingInfos, now)` (NOT `pricingInfos[-1]`, the "
    "c3244 future-dated rule), expand EVERY charge event and tier rung (the c3244 cheap-leg "
    "rule), read each live README past the title for scope exclusions, and exact-string-grep "
    "our own READMEs for the slug before calling anything new. At 6 rows/cycle the tail is "
    "~225 cycles; it is a FALLBACK for cycles with no real backlog, never a reason to skip "
    "one.**"
)

orig = open(QUEUE).read().split('\n')
n = len(orig)

cut_idx = set()
for s, e in CUTS:
    assert 1 <= s <= e <= n, (s, e)
    for i in range(s, e + 1):
        assert i not in cut_idx, f'overlapping cut ranges at line {i}'
        cut_idx.add(i)

# Every range must start on an item head, sit after a blank line, and be
# followed by an item head (the (68,80) range ends on a detail line whose
# own trailing blank, L81, is deliberately kept as the separator).
ENDS_ON_BLANK = {(17, 18): True, (21, 22): True, (25, 28): True,
                 (35, 65): True, (68, 80): False}
for s, e in CUTS:
    assert orig[s - 1].startswith(('- [ ] ', '- [x] ')), \
        f'range {s}-{e} does not start on an item head: {orig[s-1][:60]!r}'
    assert orig[s - 2].strip() == '', \
        f'line before range {s}-{e} is not blank: {orig[s-2][:60]!r}'
    if ENDS_ON_BLANK[(s, e)]:
        assert orig[e - 1].strip() == '', \
            f'range {s}-{e} does not end on a blank separator: {orig[e-1][:60]!r}'
        assert orig[e].startswith(('- [ ] ', '- [x] ')), \
            f'line after range {s}-{e} is not an item head: {orig[e][:60]!r}'
    else:
        assert orig[e].strip() == '', \
            f'line after range {s}-{e} is not the kept blank: {orig[e][:60]!r}'

EXPECTED_HEADS = {(17, 18): 1, (21, 22): 1, (25, 28): 2, (35, 65): 6, (68, 80): 1}
for s, e in CUTS:
    heads = [i for i in range(s, e + 1) if orig[i - 1].startswith(('- [ ] ', '- [x] '))]
    assert len(heads) == EXPECTED_HEADS[(s, e)], (s, e, len(heads), heads)

cut_lines = []
for s, e in CUTS:
    cut_lines.extend(orig[s - 1:e])

kept = []
for i, ln in enumerate(orig, start=1):
    if i == 68:
        kept.append(INDEX_REPLACEMENT)   # replaces the cut index line in place
    elif i in cut_idx:
        continue
    else:
        kept.append(ln)

# Losslessness: strip the one deliberate insertion, then every original line
# must appear exactly once across kept+cut (no loss, no duplication).
kept_wo_ins = [ln for ln in kept if ln is not INDEX_REPLACEMENT]
assert len(kept_wo_ins) + len(cut_lines) == n, (len(kept_wo_ins), len(cut_lines), n)
assert sorted(orig) == sorted(kept_wo_ins + cut_lines), 'multiset identity failed'

header = (
    f"## Archived by cycle {CYCLE} DEEP trim (regular slot, {CYCLE} % 3 == 1; "
    f"`check-doc-size` TRIM DUE at 195.5KB/1090ln with ~1 cycle of headroom, deferred by "
    f"c3276-c3279, preflight otherwise fully clean). Two kinds of content, both verbatim, "
    f"in original file order. (1) **10 CLOSED cycle-report blocks**: c3272, c3269, c3268, "
    f"c3270, c3265, the c3266/c3267 doc-trim handoff block (superseded -- c3280 writes a "
    f"fresh one), c3252, c3253, c3254, c3255 -- restoring queue.md's live CLOSED count from "
    f"17 to 7, still above the floor of 5. (2) **the `NEW c3162` vendor-catalogue triage "
    f"log's stale index line plus its 12 per-cycle detail paragraphs** (c3253, c3248, c3247, "
    f"c3246, c3244, c3245, c3243, c3242, c3241, c3239, c3217, c3218 -- 33.1KB, the single "
    f"largest object in the file and never previously rotated); the live item stays in "
    f"queue.md with a compressed index pointing here."
)

print(f"orig lines: {n}  ({sum(len(l)+1 for l in orig)} B)")
print(f"cut lines: {len(cut_lines)}  ({sum(len(l)+1 for l in cut_lines)} B)")
print(f"kept lines: {len(kept)}  ({sum(len(l)+1 for l in kept)} B)")
print("losslessness: OK")

if '--write' in sys.argv:
    with open(QUEUE, 'w') as f:
        f.write('\n'.join(kept))
    old_archive = open(ARCHIVE).read()
    new_block = header + '\n\n' + '\n'.join(cut_lines) + '\n\n'
    with open(ARCHIVE, 'w') as f:
        f.write('\n' + new_block + old_archive.lstrip('\n'))
    print("WROTE.")
else:
    print("DRY RUN ONLY -- pass --write to apply.")
