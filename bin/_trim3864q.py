#!/usr/bin/env python3
"""cycle 3864 -- NEW c3824a batch (open-item COMPRESSION, not a report-block rotation).

Rotation cannot shrink tasks/queue.md any further on merit: check-doc-size reads
floor 218.8KB across 112 live OPEN items, so only closing/merging/compressing OPEN
items lowers the floor. This is the c3824a lever, run as a batch of 2 per that
item's "never all at once" instruction.

Targets, re-derived fresh this cycle (never forwarded):
  STANDING c3280  4,241B / 5 lines  (queue.md:154)
  NEW c3372       7,639B / 2 lines  (queue.md:126)

Both are COMPRESS-to-pointer (move (ii) in NEW c3824a), the pattern already applied
to c2994/c2876/c2907/c3046/c3589: full live text appended VERBATIM to
tasks/queue_archive.md under '## Archived by cycle 3864', live copy replaced by a
pointer that keeps every ACTIONABLE residue.

Safety work done before writing this script (PLAYBOOK '## Doc-size trim cadence for
tasks/queue.md', the c3492 relocate-method-first lesson):
  * c3280's METHOD is already verbatim in notes/PLAYBOOK.md, '## Doc-size trim
    cadence for tasks/queue.md' (RELOCATED c3498), and its THREE durable lessons are
    already verbatim in notes/LEARNINGS.md, '## Cycle 3768 -- rotation on
    tasks/queue.md has reached equilibrium ...' (lessons 1/2/3). The live block is a
    THIRD copy. Verified by grep this cycle, not assumed.
  * c3372's METHOD is already verbatim in notes/PLAYBOOK.md, '## Competitor-claim
    refresh method (`NEW c3372` batches)' (RELOCATED c3636), and the
    never-truncate-a-checker-run rule in '## Checker output hygiene' (c3627).
  * notes/STANDING.md carries NO must-stay-live ruling on either id (it rules only
    c3020 and c2336 permanent; _trim3540q.py REJECTED adds c2994/c3046).
  * Hazard grep: both ids keep a LIVE top-level copy (the pointer), so every
    intra-file cross-reference (8 x c3280, 12 x c3372) and every external hit
    (historical _trim*q.py docstrings) stays valid.

Verify-in-MEMORY-then-write, per the _trim3492q.py bug (1) lesson.
"""
import re
import sys

QUEUE = 'tasks/queue.md'
ARCHIVE = 'tasks/queue_archive.md'
CYCLE = 3864

C3280_PTR = (
    "- [ ] **STANDING c3280 -- `tasks/queue.md` doc-size trim cadence: POINTER ONLY "
    "(COMPRESSED c3864; the full prior 4,241B block is verbatim in `tasks/queue_archive.md` "
    "under `## Archived by cycle 3864`). Nothing was lost -- every sentence of it already "
    "existed in two other places, which is why it was compressible.** **METHOD:** "
    "`notes/PLAYBOOK.md`, `## Doc-size trim cadence for tasks/queue.md` (RELOCATED c3498) -- "
    "the decision rule, the per-block census, the 3-pass hazard grep, the c3724/c3748 "
    "nested-follow-up guards, the c3672 floor-3 ruling and the DONE history. **THE THREE "
    "DURABLE LESSONS:** `notes/LEARNINGS.md`, `## Cycle 3768 -- rotation on `tasks/queue.md` "
    "has reached equilibrium ...` -- (1) a forwarded block count fails in BOTH directions and "
    "so does a bare grep: grep the heads THEN classify each one report-block vs one-off "
    "(c3765 under-counted by 4, c3767 over-counted by 3); (2) one-off closures REUSE "
    "report-block cycle ids, so a dict keyed by cycle id silently drops a span -- clone "
    "`bin/_trim3748q.py` BY NAME, never the newest `_trim*q.py` on disk; (3) rotation is now "
    "MAINTENANCE, not a trim -- a floor-3 cut buys roughly what one QUALITY cycle writes back. "
    "**Read both before any trim. Do not re-derive the arithmetic, and do not trust any byte "
    "or block number quoted in a handoff -- re-measure.** The `CLOSED cNNNN` report-block floor "
    "on this file is **3** (c3672 ruling; cannot be cut again). Since c3824 the real lever is "
    "`NEW c3824a` (OPEN-item reduction), not rotation. `COMPRESSED c2994` is still flagged "
    "possibly-immovable (`notes/STANDING.md`, `_trim3540q.py` REJECTED list) -- read both "
    "before attempting it."
)

C3372_PTR = (
    "- [ ] **NEW c3372 (MEDIUM -- competitor-claim refresh, no hard deadline. Do it off-cadence, "
    "in QUALITY slots, a batch at a time. RE-COMPRESSED c3516; RE-CENSUSED c3636; NARRATIVE "
    "COMPRESSED c3759; NARRATIVE RE-COMPRESSED c3864 -- batches 13/14/15's per-batch findings are "
    "now verbatim in `tasks/queue_archive.md` under `## Archived by cycle 3864`, batch 12 under "
    "`## Archived by cycle 3759`, batches 1-11 under `## Archived by cycle 3516`, the 11.5KB "
    "batches-1-10 body under `## Archived by cycle 3461`, the c3444-era compression under "
    "`## Archived by cycle 3444`.)** **METHOD -- read it before running a batch, do not re-derive "
    "it and do not re-cut it:** `notes/PLAYBOOK.md`, `## Competitor-claim refresh method "
    "(`NEW c3372` batches)` carries the CLASS 1 / DATED-regex false-positive rule, the four "
    "cross-batch lessons, the live-ladder re-stamp rule and the date-staggering rule verbatim; "
    "the never-truncate-a-checker-run rule is in `## Checker output hygiene`. **CLASS 2 is the "
    "live work, and the tally in this item is NOT the backlog -- the live "
    "`bin/check-competitor-claims` output is.** **LAST FLEET MEASUREMENT, c3804: 354 paragraphs "
    "checked, 107 flagged, ALL class-2 FRESHNESS** (checks 1 and 3 clean fleet-wide; dates "
    "clustered 2026-10-03..10-09, i.e. one aged cohort, not new drift). The trend this item "
    "predicted holds -- 46/309 at c3372 -> 107/354 at c3804: paragraphs age past the 45d "
    "`MAX_AGE_DAYS` faster than batches close them, so never treat a flag count as a fixed list. "
    "**Next fleet run due c3948. The fleet run takes >5 min -- REDIRECT IT "
    "(`bin/check-competitor-claims > /tmp/ccc.txt 2>&1`); c3804 ran it on plain stdout, the "
    "harness backgrounded it at 300s and the first ~28 lines were lost. A truncated run must not "
    "be used to pick batch targets.** **15 BATCHES DONE, one Actor/cluster at a time, every one "
    "landing `0 stale, 0 undated` with `check-price-superiority` re-run fleet-wide at `0 "
    "undisclosed`:** 1 c3420 `sam-gov-opportunities`; 2 c3423 `trademark-search`; 3 c3432 "
    "`google-news`; 4 c3435 `hacker-news`; 5 c3438 `scholarship`+`shopify-products`; 6 c3441 "
    "`sec-insider-trades`; 7 c3447 `steam-reviews`; 8 c3453 `substack`; 9 c3456 "
    "`federal-register`; 10 c3459 `grants-gov`; 11 c3462 `google-play-reviews`; 12 c3666 "
    "`uk-find-a-tender`; 13 c3805 `sec-insider-trades` (3 REAL price drifts + 1 material "
    "break-even reclassification, not just staleness); 14 c3806 `remote-jobs` (19 user-count "
    "claims); 15 c3861 `remote-jobs` (2 user-count drifts, one of which the checker never "
    "flagged). **THE LESSON THOSE THREE EARNED, and the reason a batch is not a re-date pass: "
    "re-fetch every named handle's live `pricingInfos`/`stats.totalUsers` -- c3805, c3806 and "
    "c3861 EACH found real drift (tier changes, start-fee changes, a rival moving from "
    "high-density-only to beats-us-at-any-density), and c3861's second drift was invisible to "
    "the checker.** **NEXT:** `trademark-search-scraper` or `sam-gov-opportunities-scraper` -- "
    "re-confirm counts fresh with `--only` FIRST (they will have shifted since c3804, and c3861 "
    "showed a `COMPETITORS.md` relocation can shrink a backlog silently by moving paragraphs out "
    "of the checker's glob, see `NEW c3812a`). **ALSO STILL OPEN, from c3475's `substack-scraper` "
    "competitor_audit rotation (a side effect, not this item's own sweep):** "
    "`substack-scraper/README.md:215` flagged STALE (compares against `benthepythondev`, last "
    "verified 2026-10-04) -- BATCH 8 (c3453) already closed this Actor once, so this is FRESH "
    "drift, not a leftover; re-verify live and re-date, same method as every other batch."
)


def top_level_items(lines):
    """Yield (start_idx, end_idx_exclusive, head_line) for every top-level checklist item."""
    heads = [i for i, l in enumerate(lines)
             if l.startswith('- [ ] ') or l.startswith('- [x] ')]
    out = []
    for n, i in enumerate(heads):
        end = heads[n + 1] if n + 1 < len(heads) else len(lines)
        out.append((i, end, lines[i]))
    return out


def find_one(items, pattern):
    hits = [it for it in items if re.match(pattern, it[2])]
    if len(hits) != 1:
        sys.exit('FATAL: pattern %r matched %d items, expected exactly 1' % (pattern, len(hits)))
    return hits[0]


orig = open(QUEUE).read()
lines = orig.split('\n')
items = top_level_items(lines)

t3280 = find_one(items, r'- \[ \] \*\*STANDING c3280 ')
t3372 = find_one(items, r'- \[ \] \*\*NEW c3372 ')

# Cut spans must not overlap, and must be processed high-index-first so earlier
# replacements do not shift later indices.
targets = sorted([(t3280, C3280_PTR, 'STANDING c3280'),
                  (t3372, C3372_PTR, 'NEW c3372')],
                 key=lambda t: t[0][0], reverse=True)
spans = [t[0] for t in targets]
for a, b in zip(spans, spans[1:]):
    if b[1] > a[0]:
        sys.exit('FATAL: target spans overlap')

# GUARD (c3724/c3748): refuse if a cut span carries a nested actionable follow-up
# that would only exist inside the text being moved to the archive. Widened regex
# per _trim3748q.py (dash optional, backticks optional).
NESTED = re.compile(r'^\s+(?:- )?\*\*`?NEW c(\d+[a-z]?)`?\b')
new_lines = list(lines)
archive_chunks = []
for (start, end, head), ptr, label in targets:
    body = lines[start:end]
    # Trailing blank lines belong to the file's layout, not the item -- keep them live.
    while body and body[-1].strip() == '':
        body = body[:-1]
        end -= 1
    for bl in body[1:]:
        m = NESTED.match(bl)
        if m:
            sys.exit('FATAL: nested actionable NEW c%s inside %s -- promote it first' % (m.group(1), label))
    if len(ptr.split('\n')) != 1:
        sys.exit('FATAL: pointer for %s must be exactly one line' % label)
    archive_chunks.append((label, start + 1, len(body), '\n'.join(body)))
    new_lines[start:end] = [ptr]

new_queue = '\n'.join(new_lines)

hdr = ['', '## Archived by cycle %d' % CYCLE, '',
       '`NEW c3824a` OPEN-item COMPRESSION batch (not a `CLOSED` report-block rotation).',
       'Each block below was replaced in `tasks/queue.md` by a one-line pointer that names',
       'this header plus the `notes/PLAYBOOK.md` / `notes/LEARNINGS.md` sections holding its',
       'method and lessons. Text is verbatim as it stood at cycle %d.' % CYCLE, '']
for label, lineno, nl, chunk in archive_chunks:
    hdr += ['### %s (was `tasks/queue.md`:%d, %d line(s), %d bytes)' % (label, lineno, nl, len(chunk) + 1),
            '', chunk, '']
addition = '\n'.join(hdr)

old_archive = open(ARCHIVE).read()
new_archive = old_archive + ('' if old_archive.endswith('\n') else '\n') + addition
if not new_archive.startswith(old_archive):
    sys.exit('FATAL: archive write would not be append-only')

# ---- verify in memory, before any write -------------------------------------
# 1. losslessness: every non-blank original queue line must still be findable in
#    the new queue OR in the new archive.
live_set = set(new_queue.split('\n'))
arch_set = set(new_archive.split('\n'))
missing = [l for l in lines if l.strip() and l not in live_set and l not in arch_set]
if missing:
    sys.exit('FATAL: %d original line(s) would be lost, first: %r' % (len(missing), missing[0][:120]))

# 2. each moved block must be present verbatim as a contiguous substring of the
#    archive, and absent from the live file.
for label, lineno, nl, chunk in archive_chunks:
    if chunk not in new_archive:
        sys.exit('FATAL: %s not verbatim in archive' % label)
    if chunk in new_queue:
        sys.exit('FATAL: %s still present verbatim in live queue' % label)

# 3. both ids must keep a LIVE top-level OPEN copy (the pointer) -- this is what
#    makes every intra-file cross-reference to them still resolve.
new_items = top_level_items(new_queue.split('\n'))
for pat, label in [(r'- \[ \] \*\*STANDING c3280 ', 'STANDING c3280'),
                   (r'- \[ \] \*\*NEW c3372 ', 'NEW c3372')]:
    if len([it for it in new_items if re.match(pat, it[2])]) != 1:
        sys.exit('FATAL: %s lost its live top-level copy' % label)

# 4. item-count invariant: compression must not change how many items exist.
if len(new_items) != len(items):
    sys.exit('FATAL: item count changed %d -> %d' % (len(items), len(new_items)))

# 5. the pointers must carry the archive header so the full text is findable.
for ptr in (C3280_PTR, C3372_PTR):
    if 'Archived by cycle 3864' not in ptr:
        sys.exit('FATAL: a pointer does not name the archive header')

open(QUEUE, 'w').write(new_queue)
open(ARCHIVE, 'w').write(new_archive)

print('queue.md  %d -> %d bytes (%+d), %d -> %d lines'
      % (len(orig), len(new_queue), len(new_queue) - len(orig),
         len(lines), len(new_queue.split('\n'))))
print('archive   %d -> %d bytes (+%d, append-only)'
      % (len(old_archive), len(new_archive), len(new_archive) - len(old_archive)))
for label, lineno, nl, chunk in archive_chunks:
    print('  archived %-16s %5d bytes / %d line(s)' % (label, len(chunk) + 1, nl))
print('all 5 in-memory verifications passed before writing')
