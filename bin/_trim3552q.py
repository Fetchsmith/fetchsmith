#!/usr/bin/env python3
"""Cycle 3552 tasks/queue.md trim.  Clone of bin/_trim3549q.py, with the
c3492 corrections applied (build every output as a STRING, assert, write LAST;
compare exempted lines by VALUE, never with `is` -- in fact this script needs
NO exemptions at all, because every rewritten line's original text is moved
verbatim into either the archive or PLAYBOOK.md, so the plain lossless check
covers them).

Cuts, in the order the PLAYBOOK method ranks them (census FIRST, then the
rotation, then genuinely-superseded/method content):

  A. ROTATION (rule-6b report-block floor = 5, re-derived fresh this cycle:
     8 report-shaped CLOSED blocks live -> archive the oldest 3, keep 5 so
     c3552's own block makes 6).  Blocks: CLOSED c3546, c3545, c3544.
  B. FOLD-IN REGISTER: the `remote-jobs-scraper -- ALL TEN FOLDED IN at cycle
     3471` entry is RETIRED by its own text ("nothing left owed here") and the
     rotation is not due again until ~c3807 -- genuinely superseded content,
     the one lever notes/STANDING.md:277 still endorses.  Full line to the
     archive verbatim; one-line pointer stays live.
  C. Vendor-catalogue tracker, `Per-batch results` line (4,833B, the line that
     has regrown after 7 prior compressions): its RULE RATIONALE sentences are
     METHOD, so they go to notes/PLAYBOOK.md beside the 7 ruling buckets that
     c3360 relocated out of this very block.  The FINDS INDEX, COVERAGE range
     and the TWO LIVE OBLIGATIONS stay live -- they are the record, not method.
  D. Same tracker, `Method is fixed:` paragraph (980B) -> PLAYBOOK, same
     c3360 precedent, one-line pointer stays live.
  E. Collapse the stray doubled `---` separator after the FOLD-IN REGISTER.

NOT DONE, deliberately: relocating `NEW STANDING TRIPWIRE (c2336)` (3.7KB,
the 4th-largest block) was planned and then DROPPED by hazard-grep pass (a),
which found notes/STANDING.md:11 ruling that c3020 and c2336 "were
deliberately NOT moved and must stay live in `queue.md` permanently" because
both are every-cycle preflight checks, not read-on-demand reference.  Exactly
the c3492 "grep for the method inside the block before cutting it" lesson.
"""
import re, subprocess, sys

QUEUE = 'tasks/queue.md'
ARCH = 'tasks/queue_archive.md'
PLAY = 'notes/PLAYBOOK.md'

orig = open(QUEUE).read()
L = orig.split('\n')


def head_span(pat):
    """(start, end) of the block whose head matches pat; end is exclusive."""
    idx = [i for i, l in enumerate(L) if re.match(pat, l)]
    assert len(idx) == 1, (pat, idx)
    i = idx[0]
    j = i + 1
    while j < len(L) and not re.match(r'^- \[[ x]\] \*\*', L[j]):
        j += 1
    return i, j


# ---- boundary asserts: exact head text, so a drifted line fails loudly ----
s46, e46 = head_span(r'^- \[x\] \*\*CLOSED c3546 -- QUALITY slot')
s45, e45 = head_span(r'^- \[x\] \*\*CLOSED c3545 -- BUILD slot')
s44, e44 = head_span(r'^- \[x\] \*\*CLOSED c3544 -- BUILD slot')
assert s46 < s45 < s44, (s46, s45, s44)
assert e46 == s45 and e45 == s44, 'rotation span is not contiguous'
ROT_A, ROT_B = s46, e44          # one contiguous span, newest-first in-file

# re-derive the report-block count FRESH (never forwarded)
reports = [l for l in L if re.match(r'^- \[x\] \*\*CLOSED c35\d\d -- (BUILD|QUALITY|GROWTH) slot', l)]
assert len(reports) == 8, 'expected 8 live report blocks, found %d' % len(reports)

I_FOLDIN = next(i for i, l in enumerate(L) if 'ALL TEN FOLDED IN at cycle 3471' in l)
I_BATCH = next(i for i, l in enumerate(L) if l.startswith('  **Per-batch results -- RULE CHANGED c3468'))
I_METH = next(i for i, l in enumerate(L) if l.startswith('  Method is fixed: clone the most recent'))
# E: the doubled separator sits between the FOLD-IN REGISTER and NEW c3408
I_SEP = next(i for i in range(I_FOLDIN, I_FOLDIN + 20)
             if L[i] == '---' and L[i + 1] == '' and L[i + 2] == '---')

ORIG_FOLDIN, ORIG_BATCH, ORIG_METH = L[I_FOLDIN], L[I_BATCH], L[I_METH]

# ---------------- replacement live lines (compressed / pointers) ----------------
NEW_FOLDIN = (
    "  **`remote-jobs-scraper` -- RETIRED at c3471, nothing owed** (all 10 register items "
    "re-priced live with 0 drift and folded into one consolidated README paragraph, build "
    "0.1.110, byte-identical verified; next rotation ~c3807). COMPRESSED c3552: the 10 handles "
    "and the full closure narrative are verbatim in `tasks/queue_archive.md`, "
    "`## Archived by cycle 3552`, and in `state/STATUS.md`'s cycle 3471 entry / "
    "`audit_dates.json`'s `remote-jobs-scraper.competitor_audit_note`."
)

NEW_BATCH = (
    "  **Per-batch results -- RULES (c3468 no-find batches are not recorded individually; "
    "c3516 a find gets its HANDLE and at most a short parenthetical, never a price/tier/shape "
    "narrative). RELOCATED c3552 to `notes/PLAYBOOK.md`, `## Vendor-catalogue triage -- why this "
    "line keeps regrowing (the c3468/c3516 recording rules)`: the full rationale for why those "
    "two rules exist and must not be reverted, verbatim.** Prior generations of this line are in "
    "`tasks/queue_archive.md` under `## Archived by cycle 3320`/`3348`/`3360`/`3396`/`3444`/"
    "`3468`/`3492`/`3516`/`3552`. **COVERAGE: rows 161-838 triaged across 111 batches, "
    "c3287-c3515 inclusive** -- advance this ROW RANGE, do not append prose. The authoritative "
    "contiguous row count is in the `PARTIALLY DONE` head above, not here, and the only "
    "resumption authority is the RESUME POINTER in `NEW c3162` below; trust prose for nothing "
    "but the last-done INDEX (c3443). **FINDS INDEX -- the count `NEW c3348` asks for, rows "
    "161-772 ONLY, derived at c3468 off the full pre-compression line (its pre-c3287 batches are "
    "in the archive, so c3348 is advanced, not closed): 24 bolded N/6 price finds + 10 "
    "non-price/scope-excluded/awareness-only finds.** Handles are kept because the live "
    "`FOLD-IN REGISTER` above cross-indexes them; **what is actually OWED lives THERE and in the "
    "READMEs, never here.** PRICE FINDS: c3297 `goat255`; c3313 `factpipe`; c3314 `gazidev`; "
    "c3326 `ninhothedev/shopify-store-scraper`; c3327 `nomad-agent/dynamitejobs-scraper`; c3335 "
    "`accountable_eel/himalayas-jobs-lookup`; c3338 `actor-forge/career-page-jobs`; c3359 "
    "`aurenic/shopify-scraper`; c3367 `bepolabs/podcast-episodes` + `bepolabs/sam-gov` (2/6); "
    "c3368 `bepolabs/website-screenshot`; c3398 `datahamster/screenshot-url`; c3400 "
    "`datamule/ashby-jobs-scraper` + `datamule/lever-jobs-scraper` + "
    "`datalayer/shopify-brand-intelligence` (3/6); c3409 `dennydevelops/shopify-store-tracker`; "
    "c3430 `forgedata/workday-jobs`; c3437 `gmpsignal/eu-ted-tenders-scraper`; c3439 "
    "`grit-77/usaspending-awards`; c3440 `grit-77/itunes-podcasts`; c3448 "
    "`informed_almandine_vzb/shopify-store-products-scraper` (FREE-rung-only -- see the "
    "INVERTED-LADDER note in LEARNINGS c3448); c3454 `jpopendata/remoteok-jobs`; c3467 "
    "`locaihost/sec-edgar`; c3473 `mambalabs/substack-scraper`; c3478 "
    "`maydit/trade-policy-rule-monitor` + `maydit/google-news-brand-monitor` + "
    "`maydit/remote-jobs-employer-direct` (3/6); c3479 `maydit/workable-jobs-scraper` + "
    "`maydit/workday-jobs-scraper` + `maydit/greenhouse-jobs-scraper` + "
    "`maydit/lever-jobs-scraper` (4/6, same vendor/ladder as the c3478 find); c3486 "
    "`mina_safwat/substack-scraper`; c3487 `myagizm/google-news-scraper`. NON-PRICE / "
    "SCOPE-EXCLUDED / AWARENESS-ONLY: c3304 (2 non-price, `NEW c3304`); c3311 (`NEW c3311`); "
    "c3319 (`NEW c3319`); c3321 (`NEW c3321`, `kadi_bence/remote-jobs-scraper`); c3340 "
    "(`actor-forge/remote-jobs`, every-tier undercut but bucket 7, `NEW c3340`); c3395 "
    "(`datadesk-io/eu-ted-tenders-scraper`); c3436 (`glasswing/jobs-search-api`, the only scope "
    "superset in a 6-handle fleet-shadow vendor -> FOLD-IN REGISTER, not an edit); c3446 "
    "(`hridayrungta/career-site-jobs-scraper`, `NEW c3446`); c3452 (`NEW c3452`); c3460 (`NEW "
    "c3460`); c3514 (`nefes-tools/eu-company-jobs`, `NEW c3514`). **TWO LIVE OBLIGATIONS are the "
    "only open work this line carries -- everything else above is disclosed and closed: (1) "
    "c3327 `nomad-agent/dynamitejobs-scraper` is STILL PENDING FOLD-IN (`NEW c3327`), the one "
    "price find in this index with open work; (2) c3395 `datadesk-io/eu-ted-tenders-scraper`, "
    "the first GENUINE same-source TED-native rival in the catalogue (dearer than us at every "
    "tier), must be NAMED at `eu-ted-tenders-scraper`'s next scheduled `competitor_audit`.** "
    "Every other find was disclosed same-cycle unless a `NEW cNNNN` is named beside it."
)

NEW_METH = (
    "  Method is fixed -- RELOCATED c3552 to `notes/PLAYBOOK.md`, `## Vendor-catalogue triage -- "
    "the fixed per-batch method`, VERBATIM (clone `_triageNNNN.py`; price via "
    "`check-price-superiority.effective(...)`, not `pricingInfos[-1]`; expand every charge event "
    "and tier rung; read each live README past the title; exact-grep our own READMEs for the "
    "slug; disclose a real undercutter SAME-CYCLE). Same c3360 lever that moved the 7 ruling "
    "buckets out of this block. **At 6 rows/cycle the 647-row tail is ~108 cycles; it is a "
    "FALLBACK for cycles with no real backlog, never a reason to skip one.**"
)

# ---------------- PLAYBOOK additions (relocated METHOD, verbatim) ----------------
play = open(PLAY).read()
play_lines = play.split('\n')
i_anchor = next(i for i, l in enumerate(play_lines)
                if l.startswith('## Doc-size trim cadence for tasks/queue.md'))

PLAY_NEW = [
    "## Vendor-catalogue triage -- why the per-batch line keeps regrowing (the c3468/c3516 recording rules) (RELOCATED here by cycle 3552 from the `PARTIALLY DONE` vendor-catalogue tracker in `tasks/queue.md`)",
    "",
    "RELOCATED because it is the reusable RATIONALE for two recording rules, not a task -- the same c3360 lever that moved the 7 standing ruling buckets out of this very block, and the only lever `notes/STANDING.md` still endorses for this file. The live line keeps the rules in brief plus the FINDS INDEX, the COVERAGE row range and the TWO LIVE OBLIGATIONS. Text below is verbatim as it stood at c3552; the full pre-compression generations of the line are in `tasks/queue_archive.md` under the c3320/c3348/c3360/c3396/c3444/c3468/c3492/c3516/c3552 headers.",
    "",
    "**RULE CHANGED c3468: no-find batches are NOT recorded individually any more.** A 0/6 batch is recorded ONLY by the coverage sentence plus its own cycle's `state/STATUS.md` record; only FINDS get a clause. **RULE TIGHTENED c3516: a find gets its HANDLE and at most a short parenthetical -- NOT a vendor-by-vendor price/tier/shape narrative.** That narrative is what regrew the line to 6,235B in the 48 cycles after c3468 had just cut it from 18,582B, and it is already in each find-cycle's own `state/STATUS.md` record and in the target Actor's dated README paragraph -- the README is the authoritative disclosure, the live line is only an index.",
    "",
    "**WHY the c3468 rule exists, do not revert it:** the line was compressed at c3320, c3348, c3384, c3396, c3420 and c3444 and regrew every single time, because each compression bounded the ENTRY and left the ENTRY COUNT growing one per triage cycle -- exactly the `notes/LEARNINGS.md` c3384 lesson (**a per-entry cap cannot bound a line with an unbounded number of entries**). Recording finds only bounds the COUNT by the ~5% hit rate; c3516 bounds the ENTRY too, because ~5% of the 647 rows still to triage is ~30 more finds.",
    "",
    "## Vendor-catalogue triage -- the fixed per-batch method (RELOCATED here by cycle 3552 from the `PARTIALLY DONE` vendor-catalogue tracker in `tasks/queue.md`, where it had lived since c3162)",
    "",
    "RELOCATED because it is reusable per-batch METHOD, not a task (c3360 precedent, as above). Verbatim as it stood at c3552:",
    "",
    ORIG_METH.strip(),
    "",
]

new_play = '\n'.join(play_lines[:i_anchor] + PLAY_NEW + play_lines[i_anchor:])

# ---------------- archive addition (verbatim) ----------------
arch = open(ARCH).read()
ARCH_NEW = (
    arch.rstrip('\n') + '\n\n'
    + '## Archived by cycle 3552 (rule-6b report-block rotation: oldest 3 of 8, floor 5; '
      'plus the retired `remote-jobs-scraper` FOLD-IN REGISTER entry and the pre-compression '
      '`Per-batch results` line, both verbatim)\n\n'
    + '\n'.join(L[ROT_A:ROT_B]).rstrip('\n') + '\n\n'
    + '### FOLD-IN REGISTER entry, retired at c3471, compressed to a pointer at c3552 (verbatim)\n\n'
    + ORIG_FOLDIN + '\n\n'
    + '### Vendor-catalogue tracker `Per-batch results` line as it stood before the c3552 '
      'rationale relocation (verbatim; the rationale itself is now in '
      '`notes/PLAYBOOK.md`)\n\n'
    + ORIG_BATCH + '\n\n'
    + '### Vendor-catalogue tracker `Method is fixed:` paragraph, relocated to '
      '`notes/PLAYBOOK.md` at c3552 (verbatim)\n\n'
    + ORIG_METH + '\n'
)

# ---------------- new queue text ----------------
out = []
for i, l in enumerate(L):
    if ROT_A <= i < ROT_B:
        continue
    if i in (I_SEP, I_SEP + 1):      # drop one of the doubled '---' and its blank
        continue
    if i == I_FOLDIN:
        out.append(NEW_FOLDIN)
    elif i == I_BATCH:
        out.append(NEW_BATCH)
    elif i == I_METH:
        out.append(NEW_METH)
    else:
        out.append(l)
new_queue = '\n'.join(out)

# ---------------- asserts, all BEFORE any write ----------------
# 1. multiset identity: every original non-blank line lands in queue|archive|playbook
pool = new_queue.split('\n') + ARCH_NEW.split('\n') + new_play.split('\n')
pool_set = set(x.strip() for x in pool if x.strip())
missing = [x for x in L if x.strip() and x.strip() not in pool_set]
assert not missing, 'LOSSLESS FAIL, %d line(s): %r' % (len(missing), missing[:3])

# 2. the three rewritten originals are present verbatim somewhere
for name, s in (('foldin', ORIG_FOLDIN), ('batch', ORIG_BATCH), ('meth', ORIG_METH)):
    assert s in ARCH_NEW, 'original %s not archived verbatim' % name
assert ORIG_METH.strip() in new_play, 'method paragraph not relocated to PLAYBOOK'

# 3. rotation floor held, and the 3 archived heads are gone from live
live_reports = [l for l in new_queue.split('\n')
                if re.match(r'^- \[x\] \*\*CLOSED c35\d\d -- (BUILD|QUALITY|GROWTH) slot', l)]
assert len(live_reports) == 5, 'floor broken: %d live report blocks' % len(live_reports)
for pat in ('**CLOSED c3546 -- QUALITY slot', '**CLOSED c3545 -- BUILD slot',
            '**CLOSED c3544 -- BUILD slot'):
    assert pat not in new_queue, 'rotated block still live: %s' % pat
    assert pat in ARCH_NEW, 'rotated block not archived: %s' % pat

# 4. live items that merely SHARE a cycle number must survive
assert '**NEW c3544 (LOW) -- `ats-jobs-scraper`' in new_queue, 'killed live NEW c3544'
# 5. the forbidden-to-move tripwire is untouched (notes/STANDING.md:11)
assert '**NEW STANDING TRIPWIRE (c2336,' in new_queue, 'c2336 tripwire must stay live'
assert '(c3020,' in new_queue, 'c3020 preflight step must stay live'
# 6. the record half of the batch line survived the compression
for must in ('c3297 `goat255`', 'c3487 `myagizm/google-news-scraper`',
             'TWO LIVE OBLIGATIONS', 'COVERAGE: rows 161-838',
             'c3514 (`nefes-tools/eu-company-jobs`'):
    assert must in new_queue, 'lost from finds index: %s' % must

print('asserts OK  queue %.1fKB -> %.1fKB (%d -> %d lines)  archive +%.1fKB  playbook +%.1fKB'
      % (len(orig) / 1024, len(new_queue) / 1024,
         len(L), len(new_queue.split('\n')),
         (len(ARCH_NEW) - len(arch)) / 1024, (len(new_play) - len(play)) / 1024))

if '--write' not in sys.argv:
    print('dry run; pass --write'); sys.exit(0)

open(ARCH, 'w').write(ARCH_NEW)
open(PLAY, 'w').write(new_play)
open(QUEUE, 'w').write(new_queue)
print('written')

# ---------------- independent re-verify against git HEAD ----------------
head = subprocess.run(['git', 'show', 'HEAD:tasks/queue.md'],
                      capture_output=True, text=True, check=True).stdout
pool2 = set()
for p in (QUEUE, ARCH, PLAY):
    pool2.update(x.strip() for x in open(p).read().split('\n') if x.strip())
miss2 = [x for x in head.split('\n') if x.strip() and x.strip() not in pool2]
assert not miss2, 'POST-WRITE LOSSLESS FAIL: %r' % miss2[:3]
print('post-write re-verify vs git HEAD: lossless, %d non-blank lines all accounted for'
      % len([x for x in head.split('\n') if x.strip()]))
