#!/usr/bin/env python3
"""One-shot rotation for tasks/queue.md, cycle 3360 (QUALITY/GROWTH slot, 3360 % 3 == 0).

Preflight fully clean on arrival (tree clean, c3359's `7330d7e3` in `git log`;
`audit-due --all` FLEET ROTATIONS NONE DUE; `inbox-triage new` NONE UNTRIAGED,
83 msgs; full-fleet `actor-health` 24/24 ok; `usage-trend --since 2026-11-09`
both watched Actors still plateaued -- `trademark-search-scraper` 759 runs30d/
7 users, `eu-ted-tenders-scraper` 103/1, so no owner email owed).
`checks-due --all` had 1 DUE, `check-disclosure` -- run first and clean
(95 site blog posts + 35 dev.to articles, 0 missing disclosures), recorded.

`check-doc-size` on arrival: **tasks/queue.md TRIM DUE at 181.4KB/1050ln with
~3 cycles of headroom** -- exactly `STANDING c3280`'s ~3-cycle trigger.  The
timing is the whole reason this runs now rather than later: doc trims are a
QUALITY-slot-only job (STANDING RULES in notes/PLAYBOOK.md), and the next
QUALITY slot is c3363, by which point the file projects to ~197KB / ~0 cycles
of headroom.  c3353 landed this file at 170.9KB 6 cycles ago; growth measured
+5.44KB/cycle since, which matches the recorded rate.  STATUS.md is TRIM SOON
but has ~21 cycles of headroom -- deliberately NOT touched this cycle.

Method follows STANDING c3280 in the order that pays:

 (1) PER-BLOCK CENSUS FIRST, re-derived fresh (98 blocks, 185,674B of 185,771B).
     Largest live blocks: the `PARTIALLY DONE` vendor-catalogue tracker
     (**19,741B/10ln** -- regrown past its 18,649B at c3353, so the biggest
     block in the file for the 4th consecutive trim), `CLOSED c3356` (6,445B,
     a kept report block), `COMPRESSED c2994` (6,207B/74ln, the candidate
     c3280's own next-candidates list has named since c3348), `STANDING c3280`
     itself (5,563B), `PARTIALLY DONE at c3250` (5,227B, the live Rippling
     plan -- KEEP until it ships), `FOLD-IN REGISTER` (4,854B, live debts).

 (2) REPORT BLOCKS re-derived FRESH, never forwarded.  **7** live per-cycle
     report blocks: c3353(L1), c3356(L3), c3352(L25), c3351(L27), c3350(L29),
     c3349(L31), c3348(L33).  `DONE c3356` (L19, the nightly-health fix),
     `CLOSED c3357` (L24), `CLOSED c3329` (L35) and `CLOSED c3336` (L37) are
     one-off/standing closures, NOT per-cycle reports -- KEPT, asserted by
     name below.  Kept the newest 5 (c3356, c3353, c3352, c3351, c3350), which
     this cycle's own prepended block makes 6, the documented floor.  Archived
     the 2 oldest (c3349, c3348; 6,329B).  A report-block cut alone is only
     3.4% of the file now -- the c3348 structural note holds, so the bulk of
     this trim is inside live blocks, not at the top.

 (3) THE PREDICTED ONE, a 4th time: the vendor-catalogue tracker, 19,741B.
     Three separate cuts, each archived verbatim:
     (a) its `Per-batch results, one line each` line (10,314B) carried **four
         entries written as full paragraphs again** -- c3354 (1,362B), c3355
         (1,215B), c3358 (898B), c3359 (1,054B), 4,529B between them, against
         an established one-liner style of ~200-350B.  The identical regrowth
         shape c3348 and c3353 each fixed on a different set of batches: this
         is now 3-for-3, so the rule is being broken by every triage cycle
         that follows a trim, not occasionally.  Rewritten as one line each.
     (b) its `STANDING RULING BUCKETS` line (4,493B) is **not a task at all**
         -- it is the reusable 7-bucket precedent set every future triage
         batch reads before writing a ruling, i.e. method.  RELOCATED verbatim
         to `notes/PLAYBOOK.md` (the c3324 move, which did the same for 9KB of
         Store-search-ranking method), leaving a one-line live pointer.
     (c) its `Running score` line (2,501B) was 2.5KB of narrative explaining
         that both of its own counters are untrustworthy -- which the live
         `NEW c3348` item below it already states as the open task.  Cut to
         one line that keeps both numbers, both dates and the pointer.

 (4) `COMPRESSED c2994` (6,207B): the +7 CLOSED c3316 batch (L315-L350,
     4 per-Actor adjudications + its method note, 3,631B) is closed narrative.
     Archived verbatim; the live block keeps the running total (79/137), the
     c2990 standing method correction, BOTH open flags (google-play 5,
     grants-gov 11), the next-candidates list, the tooling note, and the two
     transferable findings from the c3316 batch (verify an absence claim LIVE,
     and the README-link-list matcher false-positive class).

 (5) 3-pass hazard grep, pass (c) included, run BEFORE writing anything.
     (a) whole-repo by-name sweep for c3348/c3349 outside queue.md/STATUS* ->
         only the standing false positive (the dead `bin/_trim3348q.py`
         docstring, which describes its own cut).  (b) hits in `state/STATUS.md`
         (18) and `state/STATUS_ARCHIVE.md` (1) only -- each keeps its own
         record, no "see queue.md item cXXXX" pointer.  (c) INTRA-FILE over
         every kept line: **no dangling pointer owed by this cut** -- the only
         live citations of c3348 are self-contained narrative ("consolidated
         c3348", "RE-COMPRESSED c3348", "c3348 found this while compressing"),
         and `grep 'c3348 above\\|c3349 above'` is empty.  The one live
         "see `CLOSED c3328`" pointer was already repaired by c3348 to name
         the archive header and is untouched here.

 (6) Multiset identity asserted here AND re-verified against the written files
     afterwards, across live + queue_archive.md + notes/PLAYBOOK.md (the
     relocation target, so the loss-check has to span three files this time).

Usage:  python3 bin/_trim3360q.py           # dry run, asserts only
        python3 bin/_trim3360q.py --write   # apply
"""
import sys

QUEUE = 'tasks/queue.md'
ARCHIVE = 'tasks/queue_archive.md'
PLAYBOOK = 'notes/PLAYBOOK.md'
CYCLE = 3360

# ---------------------------------------------------------------- replacements
# 1-indexed inclusive ranges, applied highest-first so indices stay valid.

PERBATCH_NEW = (
    "  **Per-batch results, one line each (full narrative in each cycle's own "
    "`state/STATUS.md` record and `CLOSED cNNNN` block; the pre-c3320 verbatim "
    "paragraphs are in `tasks/queue_archive.md`, `## Archived by cycle 3320`, "
    "the c3335-c3343 ones under `## Archived by cycle 3348`, and the "
    "c3354/c3355/c3358/c3359 ones under `## Archived by cycle 3360`).** "
)

# the four over-long entries, verbatim prefixes -> their one-line forms
ONELINERS = {
    'c3354': (
        "c3354 rows 383-388: 0/6, 4 vendors (3 bucket 2 -- a Brazil "
        "company-registry mistagged into the `federal-register-scraper` niche, "
        "a BuiltWith-style tech-stack/lead-gen tool, a per-company "
        "hiring-signal watch; 1 bucket 1 remote-jobs at 4 of our 7 boards; "
        "1 flat-$0.0002 HN that ties our FREE tier and is dearer at every paid "
        "rung; 1 dearer sec-insider-trades). **Exact-handle grep has returned "
        "0 hits fleet-wide for every handle in every batch since c3297 -- the "
        "catalogue is genuinely all-new handles, so that step is cheap "
        "confirmation, not a filter.** "
    ),
    'c3355': (
        "c3355 rows 389-394: 0/6, 4 vendors (2 MCP-shaped bucket 2 -- an "
        "openFDA multi-dataset wrapper, a SAM.gov entity-registry lookup; "
        "1 bucket 2 FAERS already excluded by name; 1 dearer-10x HN; 1 bucket "
        "1 ats-jobs at 9 of our 12 platforms and dearer anyway; 1 GENUINE "
        "every-tier google-news undercut at only 2 users, under the 20-user "
        "re-price threshold `google-news-scraper/README.md` already "
        "documents). "
    ),
    'c3358': (
        "c3358 rows 395-400: 0/6, 2 vendors (2 dearer -- google-news $0.0038 "
        "vs our $0.002, podcast-directory $0.0015 vs our $0.001; 2 bucket 1 "
        "single-ATS and dearer; 1 bucket 2 UN-Comtrade mistagged into the "
        "`nih-reporter-scraper` niche; 1 GENUINE every-tier Substack undercut "
        "already covered by `substack-scraper/README.md`'s existing generic "
        "disclosure that dozens of 1-2-user entrants undercut at that band). "
    ),
    'c3359': (
        "c3359 rows 401-406: **1/6** (`aurenic/shopify-scraper`, flat "
        "$0.0008/product undercutting `shopify-products-scraper`'s "
        "$0.001->$0.00085 ladder at EVERY tier incl. Gold+, disclosed "
        "same-cycle, build 0.1.126, byte-identical live verify); other 5 were "
        "2 bucket 1 (Lever-only; 4 of our 12 ATS platforms), 2 bucket 2 "
        "category mismatches (Regulations.gov dockets vs federalregister.gov "
        "documents; Beehiiv vs Substack), 1 dearer-at-every-tier "
        "federal-register (flat $0.0013 vs our $0.0008)."
    ),
}

BUCKETS_NEW = (
    "  **STANDING RULING BUCKETS -- RELOCATED c3360 to `notes/PLAYBOOK.md`, "
    "`## Vendor-catalogue triage -- the 7 standing ruling buckets`, VERBATIM "
    "with every cited precedent handle.** They are reusable method, not a "
    "task: 7 buckets (1 scope exclusion, 2 category/niche mismatch, 3 thin or "
    "tier-crossing price ties, 4 unmonetized/FREE, 5 near-miss, 6 start-fee "
    "shape, 7 dominated by an already-disclosed cheaper-or-equal rival), "
    "consolidated at c3320 from ~20KB of archived batch narrative, bucket 7 "
    "promoted at c3348.  **Reach for one of these before writing a new "
    "ruling.** "
)

SCORE_NEW = (
    "  **Running score -- BOTH COUNTERS ARE UNRELIABLE, do not quote either "
    "as fact; the open reconciliation is `NEW c3348` below, and the NAMED "
    "FINDS in the per-batch line are the reliable record.** The tracker head "
    "read *17 real undercutters in 340 rows (~5.0%)* (last touched c3340) and "
    "this line read *12 in 316 rows (~3.8%)* (last touched c3332), against "
    "**406 rows triaged as of c3359**; neither has ever been re-derived, and "
    "c3348 deliberately labelled both in place rather than guessing (that is "
    "research, not a trim).  Full c3348 narrative: `tasks/queue_archive.md`, "
    "`## Archived by cycle 3348`; this line's own 2.5KB predecessor is under "
    "`## Archived by cycle 3360`. "
)

C2994_NEW = [
    "      **+7 CLOSED c3316, all TRUE / 0 edits -- total now 79/137.** Ran on the back of",
    "      the due `check-absence-claims` fleet rotation (c2992's rule satisfied), taking the",
    "      4 never-adjudicated Actors with the fewest claims: `app-store-reviews-scraper` 2/2,",
    "      `apple-podcasts-scraper` 2/2, `clinicaltrials-mcp-server` 2/2, `scholarship-scraper`",
    "      1/1 (fleet re-measures at **137 self-scoped, up from 128 at c2980**; per-Actor counts",
    "      in STATUS.md c3316, full per-claim adjudication verbatim in `queue_archive.md`,",
    "      `## Archived by cycle 3360`). **Two transferable findings kept live:** (1) a claim in",
    "      the founding incident's family (a wrongly-asserted MISSING field) must be verified",
    "      LIVE against the endpoint, not from memory -- `app-store-reviews-scraper:45`'s",
    "      \"no developer-reply field\" was confirmed by one 39,496 B call to the only review",
    "      feed `main.js` reads, 0 occurrences of `reply`/`response`/`respond`; (2) a",
    "      **README-link-list false positive** is a recurring matcher class -- a hyperlinked",
    "      BLOG-POST TITLE that happens to be an absence claim about the UPSTREAM API",
    "      (`clinicaltrials-mcp-server:138`) is not our claim; no edit. The `--only <slug>` loop",
    "      over all 28 dirs (~3 min) is what made those 4 visible as a closeable batch.",
]

# ------------------------------------------------------------------- cut ranges
# (first_line, last_line, label)  1-indexed inclusive, including trailing blank
CUTS = [
    (315, 350, 'COMPRESSED c2994 -- the +7 CLOSED c3316 per-Actor adjudication batch'),
    (33, 34, 'CLOSED c3348 report block'),
    (31, 32, 'CLOSED c3349 report block'),
]

ARCHIVE_HEADER = (
    "## Archived by cycle 3360 (from tasks/queue.md, TRIM DUE at 181.4KB/1050ln "
    "with **~3 cycles of headroom** -- exactly `STANDING c3280`'s ~3-cycle "
    "trigger, and timed by the rule that doc trims are QUALITY-slot-only: the "
    "next QUALITY slot is c3363, by which point this file projects to ~197KB / "
    "~0 cycles of headroom. Five things archived here, in the order a FRESH "
    "per-block census ranked them. (1) THE PREDICTED ONE, a FOURTH consecutive "
    "trim: the `PARTIALLY DONE` vendor-catalogue tracker at **19,741B**, past "
    "its own 18,649B at c3353, cut three ways -- (a) **four `Per-batch results` "
    "entries written as full paragraphs again** (c3354 1,362B, c3355 1,215B, "
    "c3358 898B, c3359 1,054B; 4,529B against an established one-liner style of "
    "~200-350B), the identical regrowth c3348 and c3353 each fixed on a "
    "different set of batches, so **every triage cycle that follows a trim "
    "breaks the block's own one-line rule -- 3 for 3**; (b) its 4,493B "
    "`STANDING RULING BUCKETS` line, which **is not a task at all** but the "
    "reusable 7-bucket precedent set, RELOCATED VERBATIM to `notes/PLAYBOOK.md` "
    "under `## Vendor-catalogue triage -- the 7 standing ruling buckets` (the "
    "c3324 move, which did the same for 9KB of Store-search-ranking method) "
    "with a one-line live pointer left behind -- so this cut's losslessness "
    "check spans THREE files; (c) its 2,501B `Running score` line, 2.5KB of "
    "narrative explaining that both of its own counters are untrustworthy, "
    "which the live `NEW c3348` item directly below it already carries as the "
    "open task -- cut to one line keeping both numbers, both dates and the "
    "pointer. (2) `COMPRESSED c2994`'s **+7 CLOSED c3316 batch** (3,631B, 4 "
    "per-Actor absence-claim adjudications + its method note), the candidate "
    "`STANDING c3280`'s own next-candidates list has named since c3348: closed "
    "narrative, archived verbatim, with the running total, BOTH open flags "
    "(google-play 5, grants-gov 11), the c2990 method correction, the "
    "next-candidates list, the tooling note and TWO transferable findings "
    "(verify a missing-field claim LIVE; the README-link-list matcher "
    "false-positive class) kept live. (3) The **2 oldest of 7** live per-cycle "
    "report blocks -- c3349, c3348, 6,329B -- keeping the newest 5 (c3356, "
    "c3353, c3352, c3351, c3350), which c3360's own prepended block makes 6, "
    "the documented floor. `DONE c3356`, `CLOSED c3357`, `CLOSED c3329` and "
    "`CLOSED c3336` are one-off/standing closures, NOT per-cycle reports, and "
    "were KEPT; the script asserts that by name. **A report-block cut is now "
    "only 3.4% of this file**, so the c3348 structural note holds: the bulk of "
    "every future trim is inside live blocks, not at the top. Hazard-grepped "
    "first, 3 passes: (a) whole-repo by-name sweep for c3348/c3349 outside "
    "queue.md/STATUS* -> only the standing false positive, the dead "
    "`bin/_trim3348q.py` docstring describing its own cut; (b) hits in "
    "`state/STATUS.md` (18) and `state/STATUS_ARCHIVE.md` (1) only, each of "
    "which keeps its own record -- no \"see queue.md item cXXXX\" pointer; "
    "(c) INTRA-FILE over every kept line -> **no dangling pointer owed by this "
    "cut**: every live citation of c3348 is self-contained narrative "
    "(\"consolidated c3348\", \"RE-COMPRESSED c3348\", \"c3348 found this while "
    "compressing both\"), `grep 'c3348 above\\|c3349 above'` is empty, and the "
    "one live \"see `CLOSED c3328`\" pointer was already repaired by c3348 to "
    "name its archive header. Newest-first, verbatim.) ##"
)

PLAYBOOK_SECTION_HEAD = (
    "## Vendor-catalogue triage -- the 7 standing ruling buckets\n\n"
    "RELOCATED here by cycle 3360 from the `PARTIALLY DONE` vendor-catalogue "
    "tracker in `tasks/queue.md` (where it had lived as a 4,493B line since "
    "c3320), because it is reusable METHOD, not a task: every `NEW c3162` "
    "triage batch reads it before writing a ruling, and it is the consolidated "
    "form of ~20KB of archived per-batch narrative. Bucket 7 was promoted into "
    "it at c3348. The live tracker now carries a one-line pointer here. Text "
    "below is verbatim as it stood at c3360.\n"
)


def main():
    write = '--write' in sys.argv
    orig = open(QUEUE, encoding='utf-8').read()
    lines = orig.split('\n')
    n0, b0 = len(lines), len(orig.encode())

    # ---- assertions about what we are about to touch (fail loudly if drifted)
    assert lines[30].startswith('- [x] **CLOSED c3349 --'), lines[30][:60]
    assert lines[32].startswith('- [x] **CLOSED c3348 --'), lines[32][:60]
    assert lines[31] == '' and lines[33] == ''
    assert lines[314].lstrip().startswith('- `app-store-reviews-scraper` 2/2.'), lines[314][:60]
    assert lines[349].lstrip().startswith('each" visible as a closeable 7-claim batch'), lines[349][:60]
    assert lines[309].lstrip().startswith('**+7 CLOSED c3316'), lines[309][:60]
    # kept-by-name assertions (one-off closures must survive)
    kept_names = ['**DONE c3356 ', '**CLOSED c3357 ', '**CLOSED c3329 (',
                  '**CLOSED c3336 ', '**CLOSED c3356 --', '**CLOSED c3353 --',
                  '**CLOSED c3352 --', '**CLOSED c3351 --', '**CLOSED c3350 --']
    score_line, buckets_line, perbatch_line = lines[72], lines[74], lines[76]
    assert score_line.lstrip().startswith('**Running score --')
    assert buckets_line.lstrip().startswith('**STANDING RULING BUCKETS')
    assert perbatch_line.lstrip().startswith('**Per-batch results, one line each')

    archived_chunks = []   # (label, text) newest-first within this header

    # ---- (1a) per-batch line: rebuild with one-liners -----------------------
    import re
    parts = re.split(r'(?=\bc3\d{3} rows )', perbatch_line)
    assert parts[0].lstrip().startswith('**Per-batch results')
    new_parts = [PERBATCH_NEW]
    replaced = []
    for p in parts[1:]:
        key = p[:5]
        if key in ONELINERS:
            replaced.append(key)
            new_parts.append(ONELINERS[key])
        else:
            new_parts.append(p)
    assert sorted(replaced) == ['c3354', 'c3355', 'c3358', 'c3359'], replaced
    new_perbatch = ''.join(new_parts)
    archived_chunks.append((
        'vendor-catalogue tracker, `Per-batch results` line as it stood at '
        'c3359 (10,314B; four entries -- c3354, c3355, c3358, c3359 -- written '
        'as full paragraphs in breach of the block\'s own one-line rule)',
        perbatch_line))

    # ---- (1b) ruling buckets -> PLAYBOOK ------------------------------------
    archived_chunks.append((
        'vendor-catalogue tracker, `STANDING RULING BUCKETS` line (4,493B) -- '
        'RELOCATED verbatim to `notes/PLAYBOOK.md`; kept here too so this '
        'archive alone remains a complete record of the cut',
        buckets_line))

    # ---- (1c) running score --------------------------------------------------
    archived_chunks.append((
        'vendor-catalogue tracker, `Running score` line (2,501B)', score_line))

    lines[76] = new_perbatch
    lines[74] = BUCKETS_NEW
    lines[72] = SCORE_NEW

    # ---- (2)+(3) range cuts, highest-first ----------------------------------
    for first, last, label in CUTS:
        chunk = lines[first - 1:last]
        archived_chunks.append((label, '\n'.join(chunk)))
        if (first, last) == (315, 350):
            lines[first - 1:last] = C2994_NEW
        else:
            del lines[first - 1:last]

    new = '\n'.join(lines)
    for name in kept_names:
        assert name in new, 'KEPT block vanished: ' + name
    assert '**CLOSED c3348 --' not in new and '**CLOSED c3349 --' not in new
    assert 'NEW c3348 (LOW-MEDIUM' in new      # the live reconciliation task
    assert 'PARTIALLY DONE at c3250' in new    # the live Rippling plan

    # ---- losslessness: every non-blank original line in live+archive+playbook
    arch_add = '\n' + ARCHIVE_HEADER + '\n\n' + '\n\n'.join(
        '### %s\n\n%s' % (lab, txt) for lab, txt in archived_chunks) + '\n'
    pb_add = ('\n' + PLAYBOOK_SECTION_HEAD + '\n' + buckets_line.lstrip() + '\n')
    haystack = new + '\n' + arch_add + '\n' + pb_add
    missing = [l for l in orig.split('\n') if l.strip() and l not in haystack.split('\n')]
    # the 3 rewritten tracker lines live in the archive as whole lines; the
    # cut ranges go in as whole lines too -- so nothing should be missing.
    assert not missing, 'LOSSY: %d line(s), first: %r' % (len(missing), missing[0][:120])

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
    old_pb = open(PLAYBOOK, encoding='utf-8').read()
    open(PLAYBOOK, 'w', encoding='utf-8').write(old_pb.rstrip('\n') + '\n' + pb_add)
    open(QUEUE, 'w', encoding='utf-8').write(new)
    print('WROTE queue.md, queue_archive.md, notes/PLAYBOOK.md')


if __name__ == '__main__':
    main()
