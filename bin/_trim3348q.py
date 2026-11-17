#!/usr/bin/env python3
"""One-shot rotation for tasks/queue.md, cycle 3348 (QUALITY/GROWTH slot, 3348 % 3 == 0).

Preflight fully clean on arrival (tree clean, c3347's `54fbbfe7` in `git log`;
`audit-due --all` FLEET ROTATIONS NONE DUE; `inbox-triage new` NONE UNTRIAGED,
83 msgs; `usage-trend --since 2026-11-09` both watched Actors still plateaued --
`trademark-search-scraper` 759 runs30d/7 users, `eu-ted-tenders-scraper` 103/1).
`checks-due --all` had 2 DUE: `check-doc-size` and `check-readme-live-row`.
`check-doc-size` on arrival: **tasks/queue.md TRIM DUE at 211.5KB/1085ln with
~-2 cycles of headroom** -- past `STANDING c3280`'s own ~3-cycle trigger, and
that item's predicted re-trim window was **c3337-c3340**, so this trim is
**8-11 cycles LATE**: the same staleness failure c3347 hit on `STANDING c3296`'s
STATUS.md window.  STATUS.md itself is OK (49.2KB, ~34c) after c3347's trim.

Method follows STANDING c3280 in the order that pays:

 (1) PER-BLOCK CENSUS FIRST, re-derived fresh.  Head (L1-190) is 139.0KB of the
     216.6KB file; the ~886-line tail (L192-1086) is ~75KB of small live notes.
     Largest live blocks: the `PARTIALLY DONE` vendor-catalogue tracker
     (**16,041B/10ln** -- doubled from 8,532B at c3332, exactly the ~1.5KB/batch
     regrowth c3324 predicted), `STANDING c3280` itself (**9,117B**, now pure
     DONE-history narrative), `COMPRESSED c2994` (6,208B/74ln), `PARTIALLY DONE
     at c3250` (5,228B, the live Rippling plan -- keep), `NEW c3046` (4,271B,
     HIGH and live).

 (2) REPORT BLOCKS re-derived FRESH, never forwarded.  **13** live per-cycle
     report blocks: c3347(L1), c3346(L7), c3345(L13), c3344(L19), c3342(L25),
     c3339(L31), c3334(L33), c3333(L39), c3332(L43), c3330(L45), c3328(L49),
     c3327(L51), c3326(L74).  Kept the newest 5 -- c3347, c3346, c3345, c3344,
     c3342 -- which this cycle's own prepended block makes 6 (the documented
     floor).  Archived the 8 oldest (30.7KB).  L31-L56 happens to be contiguous
     so it is cut as one range; L74-79 is the second.  `CLOSED c3329`,
     `CLOSED c3336`, `CLOSED c3336b` are standing one-off closures, NOT
     per-cycle reports -- excluded from the count by hand and KEPT, as every
     prior trim has done.

 (3) THE PREDICTED ONE: the vendor-catalogue tracker, compressed at c3280 and
     AGAIN at c3320, had regrown to 16.0KB -- and this time in BOTH places:
     ~3.0KB of batch narrative in its HEAD line (L108) and two full batch
     paragraphs (c3340, c3341, ~3.6KB) inside the very `Per-batch results, one
     line each` line (L114) whose entire purpose is to prevent that.  Both
     archived verbatim and replaced by one-liners.  The reusable precedent those
     paragraphs established ("dominated by an already-disclosed cheaper-or-equal
     rival") is promoted into the STANDING RULING BUCKETS line as bucket (7),
     which is the c3320 pattern.

 (4) THE SECOND PREDICTED ONE, new this cycle: `STANDING c3280` itself is
     9,117B of DONE narrative for 7 past trims.  Its own lesson -- "a block that
     was compressed before is a PRIME census candidate" -- applies to itself.
     Rewritten to keep the decision rule, the 4-step method, the 3 transferable
     lessons and a one-line-per-trim history; the full narrative is archived.

 (5) CORRECTNESS, not just bytes (the c3320 rule): the tracker carries TWO
     running-score counters that disagree -- its head line says "17 real
     undercutters in 340 rows (~5.0%)" (last updated c3340) while its score line
     says "12 ... in 316 rows (~3.8%)" (last updated c3332).  This cycle does NOT
     re-derive the true count (a research task, not a trim); both numbers are
     labelled UNRELIABLE in place and the reconciliation is filed as `NEW c3348`.

 (6) 3-pass hazard grep, pass (c) included.  (a) only the standing false
     positives (dead `_trimNNNNq.py` docstrings).  (b) hits only in
     `state/STATUS.md` / `state/STATUS_ARCHIVE.md` narrative, each of which keeps
     its own record -- no "see queue.md item cXXXX" pointer.  (c) found **1 real
     dangling pointer owed by this cut**: `NEW c3328` (L63, live, HIGH) cites
     "(see `CLOSED c3328`)", which this trim archives -- repaired in place to
     name the archive header.  Its other citation, "see `CLOSED c3329` above",
     is safe (c3329 is a standing closure and is KEPT).

 (7) Multiset identity asserted here AND re-verified against the written files.

Usage:  python3 bin/_trim3348q.py           # dry run, asserts only
        python3 bin/_trim3348q.py --write   # apply
"""
import sys

QUEUE = 'tasks/queue.md'
ARCHIVE = 'tasks/queue_archive.md'
CYCLE = 3348

# 1-indexed inclusive cut ranges (blocks + trailing blank/separator lines).
# (31,56) holds c3339, c3334, c3333, c3332, c3330, c3328, c3327 (contiguous);
# (74,79) holds c3326.
CUTS = [(31, 56), (74, 79)]

C3280_LINE = 98            # STANDING c3280 (the trim rule itself)
TRACKER_HEAD = 108         # PARTIALLY DONE -- N of 1,485 rows triaged
TRACKER_SCORE = 110        # Running score line
TRACKER_BUCKETS = 112      # STANDING RULING BUCKETS
TRACKER_BATCH = 114        # Per-batch results, one line each
C3328_LINE = 63            # NEW c3328 (live, HIGH) -- pass-C pointer repair
INSERT_AFTER = 117         # blank line closing the tracker block

# (5) the 8 pending competitor-audit fold-in items, consolidated into ONE
# register.  Text lines only -- the blanks between them are left to the
# blank-collapse pass so no `---` separator is disturbed.
FOLD_LINES = {65: 'NEW c3340', 66: 'NEW c3335', 68: 'NEW c3334',
              70: 'NEW c3327', 80: 'NEW c3321', 84: 'NEW c3319',
              86: 'NEW c3311', 88: 'NEW c3304',
              90: '`tidytools/ats-career-site-jobs`',
              92: '`wulfcare/app-store-reviews-scraper`'}
FOLD_INSERT_AFTER = 64     # blank line before the first of them

# --- this cycle's own report block, prepended ------------------------------
REPORT = (
    "- [x] **CLOSED c3348 -- QUALITY/GROWTH slot (3348 % 3 == 0, verified with "
    "`echo $((3348 % 3))`). Preflight fully clean on arrival** (tree clean, "
    "c3347's `54fbbfe7` present in `git log`; `audit-due --all` **FLEET "
    "ROTATIONS NONE DUE** (only the informational one-off/experimental axes, "
    "c1304 rule); `inbox-triage new` **NONE UNTRIAGED** (83 msgs, 0 new); "
    "`bin/usage-trend --since 2026-11-09` both watched Actors still "
    "**plateaued** -- `trademark-search-scraper` 759 runs30d/7 users, "
    "`eu-ted-tenders-scraper` 103 runs30d/1 user, both unchanged since "
    "c3337/c3340 -- no owner email owed). `checks-due --all` had **2 DUE: "
    "`check-doc-size` and `check-readme-live-row`.** **MAIN TASK: the "
    "`tasks/queue.md` trim c3347 handed over, which `check-doc-size` read at "
    "211.5KB/1085ln with ~-2 cycles of headroom.** The census found the trim "
    "was **8-11 cycles LATE** -- `STANDING c3280`'s own predicted window was "
    "**c3337-c3340** and it passed unnoticed, the identical staleness failure "
    "c3347 had just hit on `STANDING c3296`'s STATUS.md window, so this is now "
    "a pattern and not a one-off. `bin/_trim3348q.py` (clone of "
    "`_trim3332q.py`) made **four** cuts, in census order. (1) The 8 oldest of "
    "**13** live report blocks (c3339/c3334/c3333/c3332/c3330/c3328/c3327/"
    "c3326, 30.7KB), keeping the newest 5 at the documented floor with this "
    "block making 6; `CLOSED c3329`/`c3336`/`c3336b` are standing one-off "
    "closures, not per-cycle reports, and were kept. (2) **The predicted one: "
    "the vendor-catalogue tracker, 16,041B -- doubled from 8,532B at c3332, "
    "exactly the ~1.5KB/batch rate c3324 forecast** -- and it had regrown in "
    "BOTH places this time, ~3.0KB of batch narrative in its head line AND two "
    "full batch paragraphs (c3340, c3341) inside the very `Per-batch results, "
    "one line each` line whose purpose is to prevent that. Both archived "
    "verbatim, replaced by one-liners for all 5 unlogged batches "
    "(c3335/c3338/c3340/c3341/c3343), and the reusable precedent they "
    "established was promoted into `STANDING RULING BUCKETS` as **bucket (7), "
    "'dominated by an already-disclosed cheaper-or-equal rival'** (the c3320 "
    "pattern). (3) **A second predicted one, new this cycle: `STANDING c3280` "
    "itself at 9,117B** -- its own lesson, *a block that was compressed before "
    "is a PRIME census candidate*, finally applied to itself; rewritten to the "
    "decision rule + 4-step method + 3 transferable lessons + a one-line-per-"
    "trim history, with the full DONE narrative archived. (4) **Correctness, "
    "not just bytes (the c3320 rule): the tracker carries TWO running-score "
    "counters that disagree** -- head line '17 real undercutters in 340 rows "
    "(~5.0%)' (last updated c3340) vs score line '12 in 316 rows (~3.8%)' "
    "(last updated c3332). This cycle deliberately did NOT re-derive the true "
    "count (that is research, not a trim); both are labelled UNRELIABLE in "
    "place and the reconciliation is filed as `NEW c3348`. (5) **The 8 pending "
    "competitor-audit fold-in items** (`NEW c3304`/`c3311`/`c3319`/`c3321`/"
    "`c3327`/`c3334`/`c3335`/`c3340`, **16.0KB**) consolidated into a single "
    "**`FOLD-IN REGISTER`** grouped by target Actor -- all 12 handles, price "
    "ladders and undercut magnitudes stay live and greppable, the full items "
    "are archived. They were repeating the same preamble, the same 'do not "
    "publish off-cycle' ruling and the same baseline ladder 8 times over, and "
    "grouping by Actor makes the `accountable_eel` one-Actor-per-board clone "
    "strategy visible at a glance. 3-pass hazard grep "
    "run first; **pass (c) earned its keep again** -- `NEW c3328` (live, HIGH) "
    "cited '(see `CLOSED c3328`)', a block this trim archives, repaired in "
    "place to name the archive header. Losslessness asserted in the script and "
    "re-verified against the written files. Guards: `check-registry-fields`/"
    "`check-charges`/`sync-apify-prices` not re-run (pure doc maintenance, "
    "nothing shipped to the fleet). All 3 services active; `/`, `/tools`, "
    "`/pricing` all **200**. **Spend: $0.** **Blockers: none. Owner email: "
    "none owed.** **Pace: 0 new Actors built today (2026-11-17).**\n"
)

# --- (6c) pointer repair in the live `NEW c3328` --------------------------
C3328_OLD = "(see `CLOSED c3328`)"
C3328_NEW = ("(see `CLOSED c3328`, archived by c3348 -- `tasks/queue_archive.md`, "
             "`## Archived by cycle 3348`)")

# --- tracker head: drop the regrown batch narrative -----------------------
HEAD_NARR_START = "c3340 (rows 341-346) and c3341 (rows 347-352):"
HEAD_NARR_END = "**RULE, tightened at c3320"
HEAD_NARR_REPL = (
    "**Those batches' results live as ONE LINE EACH in the `Per-batch results` "
    "line below -- c3348 had to archive ~3.0KB of batch narrative out of THIS "
    "head line (c3335, c3338, c3340, c3341, c3343) to restore that, verbatim in "
    "`tasks/queue_archive.md`, `## Archived by cycle 3348`.** "
)

# --- tracker score line ---------------------------------------------------
SCORE_OLD = (
    "**Running score: 316 rows read, 12 real price undercutters disclosed or "
    "filed (~3.8%), plus 3 non-price finds and 1 product gap.** The 12th is "
    "`nomad-agent/dynamitejobs-scraper` (c3327, filed in `NEW c3327` for "
    "`remote-jobs-scraper`'s next `competitor_audit`)."
)
SCORE_NEW = (
    "**Running score -- BOTH COUNTERS ARE UNRELIABLE, do not quote either as "
    "fact (c3348).** This line and the tracker head above were maintained "
    "independently and disagree: the head read **17 real undercutters in 340 "
    "rows (~5.0%)** (last updated c3340), this line read **12 in 316 rows "
    "(~3.8%)** (last updated c3332), and **358 rows are triaged as of c3343**. "
    "c3348 compressed both blocks but deliberately did NOT re-derive the true "
    "count -- that is research, not a trim -- so it is filed as `NEW c3348` "
    "below. **The named finds are the reliable record; the totals are not.** "
    "Filed since this line was last updated: `NEW c3327` "
    "(`nomad-agent/dynamitejobs-scraper`), `NEW c3334` (three "
    "`accountable_eel/*` per-board clones), `NEW c3335` "
    "(`accountable_eel/himalayas-jobs-lookup`), `NEW c3340` "
    "(`actor-forge/remote-jobs`, awareness-only under bucket 7), plus c3338's "
    "same-cycle disclosure of `actor-forge/career-page-jobs` in "
    "`ats-jobs-scraper/README.md`."
)

# --- ruling buckets: promote the precedent the archived paragraphs earned --
BUCKETS_TAIL = ("(`intelscrape/we-work-remotely-jobs-scraper` c3319).")
BUCKETS_ADD = (
    " (7) **Dominated by an already-disclosed cheaper-or-equal rival** "
    "(established across c3338/c3340/c3343, promoted here by c3348) -- a "
    "genuine every-tier undercut is still NOT disclosure-worthy when a rival "
    "that is cheaper-or-equal on the same scope is ALREADY named in the same "
    "README: it falsifies no claim we make and adds nothing a buyer can act "
    "on. File it awareness-only, do not disclose off-cycle. "
    "(`actor-forge/website-screenshot` vs `code-node-tools` c3338; "
    "`actor-forge/remote-jobs` $0.0008/job vs the still-live "
    "`nivlekk/remote-jobs-aggregator` $0.0005 and `silicatelabs/JobsFlow` "
    "$0.00001, both re-verified live at c3340; "
    "`adaptive_labs/app-reviews-play-appstore` FREE vs the already-disclosed "
    "FREE `magicfingers/appstore-scraper` c3343.) **Check bucket 7 BEFORE "
    "writing a disclosure paragraph -- it is the one that most often turns a "
    "'real find' into a non-event.**"
)

# --- per-batch line: archive the two full paragraphs, add 5 one-liners ----
BATCH_P1_START = "c3340 rows 341-346: **0/6**"
BATCH_GREP_SENT = "**Exact-handle grep has returned 0 hits fleet-wide"
BATCH_P2_START = "c3341 rows 347-352: **0/6, but a method correction"
BATCH_ONELINERS = (
    "c3335 rows 329-334: **1/6** (`accountable_eel/himalayas-jobs-lookup`, "
    "Himalayas-only undercut, filed as `NEW c3335`); other 5 were 1 near-miss "
    "(cheaper only at Gold+), 1 dearer Substack publication-stats event, 1 "
    "SEEK-Australia general board (bucket 1), 1 HN parser 10-20x dearer, 1 "
    "typosquat/DNS monitor (bucket 2). **c3338 rows 335-340: 1/6** "
    "(`actor-forge/career-page-jobs`, flat $0.015/company vs `ats-jobs-scraper`'s "
    "per-job ladder, disclosed same-cycle -- crosses under us only past ~15-21 "
    "jobs/company); other 5 were 2 dearer-or-tied-with-fewer-features vs "
    "already-disclosed rivals (bucket 7), 1 dearer Substack leaderboard, 2 "
    "category mismatches. c3340 rows 341-346: 0/6 (all six `actor-forge/*`; "
    "`actor-forge/remote-jobs` IS an every-tier undercut but bucket 7 applies -- "
    "dominated by two still-live already-disclosed cheaper rivals -- so it was "
    "filed awareness-only in `NEW c3340`; 4 single-platform-and-dearer, 1 "
    "textbook bucket 3 EU-tenders tie-plus-start-fee). c3341 rows 347-352: 0/6 "
    "(1 dearer Steam game-data, 2 single-platform-and-dearer, 1 brand-mentions "
    "category mismatch, 2 unmonetized/already-named `adaptive_labs/*`) -- "
    "**the real finding was a method correction, now in `notes/LEARNINGS.md` "
    "cycle 3341: grep the FULL `owner/slug`, never the basename, which threw 3 "
    "false 'already disclosed' positives here.** c3343 rows 353-358: 0/6 (1 "
    "FREE dual-store listing dominated under bucket 7, 1 Reed-UK-only bucket 1, "
    "4 dearer-at-every-tier incl. one in-scope Steam games/player-count "
    "listing). **Full narrative for c3335/c3338/c3340/c3341/c3343 is verbatim "
    "in `tasks/queue_archive.md`, `## Archived by cycle 3348`.** "
)

# --- (5) the consolidated fold-in register --------------------------------
FOLD_REGISTER = (
    "- [ ] **FOLD-IN REGISTER (consolidated c3348 from 8 separate items -- "
    "`NEW c3304`, `NEW c3311`, `NEW c3319`, `NEW c3321`, `NEW c3327`, "
    "`NEW c3334`, `NEW c3335`, `NEW c3340`, 16.0KB combined; each one's FULL "
    "text is verbatim in `tasks/queue_archive.md`, `## Archived by cycle "
    "3348`, and every handle below is exact so a grep still finds it). "
    "Vendor-catalogue findings waiting on an Actor's NEXT `competitor_audit` "
    "rotation. None is published as an off-cycle README edit -- that is the "
    "standing ruling for scope-excluded and bucket-7 finds.**\n"
    "\n"
    "  **`remote-jobs-scraper` -- SEVEN pending** (our baseline: a flat-across-"
    "7-boards `job` event, **$0.0015 FREE -> $0.0013 BRONZE -> $0.0011 SILVER "
    "-> $0.001 GOLD+**; rotation lands ~c3471). (1) **`nomad-agent/"
    "dynamitejobs-scraper`** (c3327, 3u) -- **~90-95% under us at every tier** "
    "($0.0001 FREE/BRONZE -> $0.00005 GOLD+) **and a genuine COVERAGE GAP**: "
    "Dynamite Jobs is not one of our 7 de-duplicated boards. The steepest of "
    "the seven and the only one that is also a product gap. (2) "
    "**`hipersoft/himalayas-scraper`** (c3319, 3u) -- Himalayas only, $0.001 "
    "-> $0.0005, **~33-50% under, no crossover**. (3) **`kadi_bence/"
    "remote-jobs-scraper`** (c3321, 4u) -- 5 of our 7 boards, $0.0009 -> "
    "$0.00072, **~28-40% under, no crossover**. (4) **`accountable_eel/"
    "himalayas-jobs-lookup`** (c3335, 1u) -- Himalayas only, $0.001 -> "
    "$0.0005, **~33-50% under**; beats the already-disclosed `vital_tuxedo/"
    "remote-jobs-feed` (which only TIES our Gold+) outright; its $0.003 start "
    "fee amortizes away. (5) **`unfenced-group/remoteok-scraper`** (c3334, 3u) "
    "-- Remote OK only, $0.00099 -> $0.00059, **~19-41% under**, negligible "
    "start fee. (6) **`accountable_eel/workingnomads-jobs-lookup`** and (7) "
    "**`accountable_eel/remoteok-jobs-lookup`** (c3334, 2u each) -- one board "
    "each, $0.001 -> $0.0005 per-unit (~33-50% under) **but a $0.0015 start "
    "fee means they only cross below us past ~3-4 jobs/run**, the same shape "
    "already documented for `automation-lab/omni-jobs-board-scraper`. "
    "**Handle these as ONE per-board pricing pass, not seven lines:** (2), "
    "(4), (6) and (7) are the same `accountable_eel`-style one-Actor-per-board "
    "clone strategy (full-range undercut plus a start fee), so the rotation's "
    "real question is whether we can match any single-board price without "
    "discounting the other 6 boards. **Awareness-only (bucket 7), do NOT name "
    "unless the README's undercutter list is being refreshed anyway:** "
    "`actor-forge/remote-jobs` (c3340, 2u, flat $0.0008/job, 4 of our 7 "
    "boards) is a real every-tier undercut but is dominated by two still-live "
    "already-named rivals (`nivlekk/remote-jobs-aggregator` $0.0005, "
    "`silicatelabs/JobsFlow` $0.00001) and our README already states outright "
    "that we are not the cheapest listing in this niche.\n"
    "\n"
    "  **`ats-jobs-scraper` -- TWO pending** (baseline: flat `job` **$0.001 "
    "FREE -> $0.00085 BRONZE -> $0.00075 SILVER -> $0.0007 GOLD+**). (1) "
    "**`deepmine/workable-jobs`** (c3311, 1u) -- Workable only (1 of our 12 "
    "platforms), $0.00059 -> $0.00035, **~41-50% under at every tier, no start "
    "fee, no crossover**. (2) **`tidytools/ats-career-site-jobs`** (c3304, 7u, "
    "140 runs30d) -- **NOT a price undercut** (ties our FREE, dearer at every "
    "tier below it), and that is exactly why it matters: **the gap is the "
    "INPUT SHAPE, not the price.** It auto-detects the ATS from a bare company "
    "domain (`stripe.com` works as input) across 21 claimed platforms, while "
    "ours needs the company SLUG (`README.md:50`) -- the first rival to "
    "combine domain-level auto-detect AND 20+ platforms AND a price that ties "
    "ours. `check-price-superiority` will never surface it.\n"
    "\n"
    "  **`app-store-reviews-scraper` -- ONE pending.** "
    "**`wulfcare/app-store-reviews-scraper`** (c3304, 4u) is the **third** "
    "listing to claim no-500-cap depth, after the still-live `sourabhbgp` "
    "(already disclosed honestly at `README.md:617`) and the delisted "
    "`gh0st1k` (`README.md:482`) -- **the claim SHAPE is already generically "
    "disclosed, so no urgent edit is owed.** Worth a rotation paragraph for "
    "one reason: its own README admits `appVersion` is present \"for the "
    "newest 500\" only, i.e. **its deep path returns a REDUCED field set**. If "
    "that holds, the honest comparison is \"they go deeper with fewer fields\" "
    "rather than \"they go deeper and we do not\" -- materially better for us "
    "and **cheap to check** (one run of theirs, or just read their schema). "
    "Not a price undercut either: flat $0.0001/review ties our FREE and is "
    "dearer than our $0.00009/$0.00008/$0.00007.\n"
    "\n"
    "  **`eu-ted-tenders-scraper` -- nothing owed.** `actor-forge/eu-tenders` "
    "(c3340) is the tightest scope match found against it so far (TED notices "
    "+ awards + CPV/country/value filters + a monitoring mode) but **ties our "
    "flat $0.0015 at every tier and adds a $0.00005 start fee we do not "
    "charge** -- textbook bucket 3, recorded here only so the next triage does "
    "not re-derive it.\n"
)

# --- the new reconciliation item ------------------------------------------
NEW_C3348 = (
    "- [ ] **NEW c3348 (LOW-MEDIUM, correctness of a counter nobody acts on -- "
    "do NOT let it block a triage batch).** The vendor-catalogue tracker above "
    "carried **two independently-maintained running-score counters that "
    "disagree**: its head line said *17 real undercutters in 340 rows (~5.0%)* "
    "(last touched c3340) and its score line said *12 in 316 rows (~3.8%)* "
    "(last touched c3332), while 358 rows are triaged as of c3343. c3348 found "
    "this while compressing both and labelled them UNRELIABLE in place rather "
    "than guessing. **The fix is a re-derivation, not an edit:** walk the "
    "`Per-batch results, one line each` line end to end (it is now complete "
    "through c3343 and is the only per-batch record in the live file), count "
    "the bolded N/6 hits, and separately count the fold-in items still pending "
    "(`NEW c3304`/`c3311`/`c3319`/`c3321`/`c3327`/`c3334`/`c3335`/`c3340`) -- "
    "the two were almost certainly conflated, since 'disclosed same-cycle' and "
    "'filed for the next rotation' finds were being added to different "
    "counters. Then write ONE counter and delete the other. **Cheap (one pass "
    "over one line, no API calls) and it makes the ~5% hit rate quotable "
    "again, which is the only number that justifies continuing a 1,127-row "
    "tail at 6 rows/cycle.**\n"
)

# --- STANDING c3280, rewritten --------------------------------------------
C3280_NEW_TMPL = (
    "- [ ] **STANDING c3280 (replaces the archived c3266/c3267 doc-trim "
    "handoff; updated c3295, RE-COMPRESSED c3348 -- the full DONE narrative for "
    "c3296/c3305/c3306/c3309/c3320/c3324/c3332 is verbatim in "
    "`tasks/queue_archive.md`, `## Archived by cycle 3348`) -- `tasks/queue.md` "
    "doc-size cadence, with the arithmetic written down so no future cycle "
    "re-derives it.** **THE DECISION RULE: re-trim when headroom drops below "
    "~3 cycles, NOT when the banner says DUE.** `check-doc-size` projects **24 "
    "cycles ahead**, so it prints `TRIM DUE` on this file at any size above "
    "roughly 70KB -- that is not a failed trim and is not a reason to re-trim. "
    "A healthy post-trim landing is **~160-170KB / ~6-7 cycles of headroom**; "
    "growth runs ~5.4KB/cycle. **AND IF THE PREDICTED WINDOW PASSES WITHOUT A "
    "TRIM, TREAT IT AS OVERDUE IMMEDIATELY** -- c3348 arrived 8-11 cycles past "
    "the c3337-c3340 window this item named, at ~-2 cycles of headroom, the "
    "identical staleness failure c3347 hit on `STANDING c3296`'s STATUS.md "
    "window one cycle earlier. Two for two: the window is a trigger, not a "
    "hint. **Method, in the order that actually pays** (`bin/_trim3348q.py` is "
    "the template to clone): (1) run a **per-block byte/line census** FIRST "
    "(`grep` every `- [ ] **`/`- [x] **` head, sum bytes between heads) -- "
    "c3280 found a 33.1KB non-report block that 4 prior cycles of "
    "report-block-only thinking had never looked at, worth more than all 10 "
    "report blocks combined; (2) re-derive the report-block count **FRESH**, "
    "never from a forwarded number, and remember they are **not** a "
    "chronological prefix (live `NEW cNNNN` items are interleaved between them, "
    "and standing one-off closures like `CLOSED c3329`/`c3336` are not reports "
    "at all); (3) **3-pass hazard grep, and do not skip pass (c), the "
    "intra-file one** -- passes (a)/(b) have returned nothing but the same "
    "known false positives for ~25 trims, while (c) has found a real dangling "
    "pointer on c3306, c3309, c3320, c3324 and c3348; (4) assert multiset "
    "identity in the script AND re-verify losslessness against the written "
    "files afterwards. **Three lessons the DONE history earned, kept here "
    "because they are method, not history:** (a) **a block that was compressed "
    "before is a PRIME census candidate, not a solved problem** -- c3320 found "
    "the vendor-catalogue tracker at 21KB on ONE line, more than all 7 "
    "archivable report blocks combined, because every triage cycle appends "
    "~1.5KB in defiance of the block's own one-line rule; c3348 found it back "
    "at 16KB and found THIS item at 9.1KB, so the rule now includes itself; "
    "(b) **the biggest block may not be a task at all** -- ask of every big "
    "block whether it is method/reference that belongs in `notes/PLAYBOOK.md` "
    "or `notes/LEARNINGS.md` (c3324 RELOCATED `COMPRESSED c3000`, 9KB of "
    "Store-search-ranking playbook content that had lived in the task queue for "
    "324 cycles); (c) **compressing a stale tracker fixes correctness, not just "
    "bytes** -- c3320 found 3 stale counters and a duplicate resume pointer; "
    "c3348 found the tracker's two running-score counters disagreeing (17-in-340 "
    "vs 12-in-316) and filed `NEW c3348`. **DONE history, one line each (full "
    "narrative in the archive headers named above):** c3296 (the STATUS.md "
    "half, 195.4KB -> 44.8KB); c3305 (re-measure only, 188.7KB/~2c); c3306 "
    "(-> 168.8KB/~6c, 6 of 14 report blocks); c3309 (-> 164.5KB/~7c, 4 of 9, "
    "kept count dropped to the floor of 5); c3320 (199.8KB/**~0c** -> "
    "162.9KB/~7c, the tracker cut, 21KB -> 7.3KB plus the `STANDING RULING "
    "BUCKETS` consolidation); c3324 (184.6KB/~3c -> 161.7KB/~7c, the PLAYBOOK "
    "relocation); c3332 (195.3KB/~1c -> ~165KB, 8 of 13 report blocks + the "
    "`NEW c3162` tail). **DONE c3348** (216.6KB/1086ln, **~-2 cycles of "
    "headroom**, 8-11 cycles late -> **__NEW_SIZE__**; 8 of 13 report blocks "
    "(30.7KB), the tracker a third time (16.0KB, regrown in BOTH its head line "
    "and its per-batch line), and this item itself (9.1KB of narrative -> the "
    "one-line history above); bucket (7) promoted into the tracker's ruling "
    "buckets; `NEW c3348` filed for the counter reconciliation; and **the 8 "
    "pending competitor-audit fold-in items** (`NEW c3304`/`c3311`/`c3319`/"
    "`c3321`/`c3327`/`c3334`/`c3335`/`c3340`, **16.0KB**) consolidated into "
    "the single `FOLD-IN REGISTER` above, with all 12 handles, their price "
    "ladders and their magnitudes kept live and greppable and the full items "
    "archived. **That cut was worth more than its bytes: 8 items were "
    "repeating the same preamble, the same 'do not publish off-cycle' ruling "
    "and the same baseline price ladder, and grouping them by TARGET ACTOR "
    "made the `accountable_eel` one-Actor-per-board clone strategy visible at "
    "a glance in a way 8 scattered items never did.**) **Next "
    "candidates, sized at c3348:** `COMPRESSED "
    "c2994` (6.2KB/74ln), `PARTIALLY DONE at c3250` (5.2KB -- still the live "
    "Rippling implementation plan, **keep until it ships**), `FOLLOW-UP from "
    "c2380` (4.4KB), `NEW c3046` (4.3KB -- HIGH and live, do not cut), `NEW "
    "STANDING TRIPWIRE c2336` (3.8KB), `MERGED c2916` (3.4KB). **Structural "
    "note (c3348): the head of the file (L1-190) is 139KB of the 216KB; the "
    "~886-line tail is ~75KB of small live LOW/TRIVIAL notes that no single "
    "trim can touch.** With the fold-in register landed, the next real lever is "
    "a staged tail pass (~10 notes/cycle into one-line index entries + verbatim "
    "archive), not another report-block cut. **The vendor-catalogue tracker "
    "will regrow at ~1.5KB/batch -- budget a re-compression roughly every 5 "
    "batches regardless of what the banner says.** Re-trim around "
    "**c3353-c3356** (headroom < ~3 cycles), not sooner."
)


def main():
    write = '--write' in sys.argv
    with open(QUEUE, encoding='utf-8') as f:
        orig = f.read()
    lines = orig.split('\n')

    # --- boundary asserts -------------------------------------------------
    assert 'CLOSED c3339' in lines[30], "cut start drifted at L31"
    assert lines[55] == '', "cut (31,56) must end on a blank line"
    assert 'CLOSED c3326' in lines[73], "cut start drifted at L74"
    assert lines[78] == '', "cut (74,79) must end on a blank line"
    for tag, ln in (('CLOSED c3334', 33), ('CLOSED c3333', 39),
                    ('CLOSED c3332', 43), ('CLOSED c3330', 45),
                    ('CLOSED c3328', 49), ('CLOSED c3327', 51)):
        assert tag in lines[ln - 1], f"{tag} moved off L{ln}"
    # the 5 report blocks that must stay, and the 3 standing closures
    for ln, tag in ((1, 'CLOSED c3347'), (7, 'CLOSED c3346'), (13, 'CLOSED c3345'),
                    (19, 'CLOSED c3344'), (25, 'CLOSED c3342'),
                    (57, 'CLOSED c3329'), (59, 'CLOSED c3336'),
                    (61, 'CLOSED c3336b')):
        assert tag in lines[ln - 1], f"kept block {tag} moved off L{ln}"
    assert lines[C3328_LINE - 1].startswith('- [ ] **NEW c3328'), "NEW c3328 drifted"
    assert lines[C3280_LINE - 1].startswith('- [ ] **STANDING c3280'), "c3280 drifted"
    assert lines[TRACKER_HEAD - 1].startswith('- [x] **PARTIALLY DONE -- 358'), \
        "tracker head drifted"
    assert 'Running score:' in lines[TRACKER_SCORE - 1], "score line drifted"
    assert 'STANDING RULING BUCKETS' in lines[TRACKER_BUCKETS - 1], "buckets drifted"
    assert 'Per-batch results, one line each' in lines[TRACKER_BATCH - 1], \
        "per-batch line drifted"
    assert lines[INSERT_AFTER - 1] == '', "insert point is not a blank line"
    assert lines[FOLD_INSERT_AFTER - 1] == '', "fold insert point is not blank"
    for ln, tag in FOLD_LINES.items():
        assert tag in lines[ln - 1], f"fold-in item {tag} moved off L{ln}"
        assert not any(a_ <= ln <= b_ for a_, b_ in CUTS), \
            f"fold-in item {tag} is inside a report-block cut"

    # --- in-place edits ---------------------------------------------------
    # (6c) pointer repair
    c3328 = lines[C3328_LINE - 1]
    assert C3328_OLD in c3328, "the CLOSED c3328 citation drifted"
    c3328 = c3328.replace(C3328_OLD, C3328_NEW, 1)

    # tracker head: cut the batch narrative
    head = lines[TRACKER_HEAD - 1]
    a = head.find(HEAD_NARR_START)
    b = head.find(HEAD_NARR_END)
    assert 0 < a < b, "tracker head narrative bounds not found"
    head_narr = head[a:b]
    head = head[:a] + HEAD_NARR_REPL + head[b:]

    # score line
    score = lines[TRACKER_SCORE - 1]
    assert SCORE_OLD in score, "score text drifted"
    score = score.replace(SCORE_OLD, SCORE_NEW, 1)

    # ruling buckets: promote bucket (7)
    buckets = lines[TRACKER_BUCKETS - 1]
    assert buckets.rstrip().endswith(BUCKETS_TAIL), "buckets line does not end as expected"
    buckets = buckets.rstrip() + BUCKETS_ADD

    # per-batch line: archive 2 paragraphs, insert 5 one-liners
    batch = lines[TRACKER_BATCH - 1]
    p1 = batch.find(BATCH_P1_START)
    g = batch.find(BATCH_GREP_SENT)
    p2 = batch.find(BATCH_P2_START)
    assert 0 < p1 < g < p2, "per-batch paragraph bounds not found"
    batch_p1 = batch[p1:g]
    batch_p2 = batch[p2:]
    batch = batch[:p1] + BATCH_ONELINERS + batch[g:p2].rstrip() + ' '
    batch = batch.rstrip()

    # STANDING c3280
    c3280_old_full = lines[C3280_LINE - 1]

    # --- build the kept file ----------------------------------------------
    cut_set = set()
    for a_, b_ in CUTS:
        cut_set |= set(range(a_, b_ + 1))
    repl = {C3328_LINE: c3328, TRACKER_HEAD: head, TRACKER_SCORE: score,
            TRACKER_BUCKETS: buckets, TRACKER_BATCH: batch,
            C3280_LINE: '__C3280__'}
    rewritten = set(repl)

    kept = [REPORT.rstrip('\n'), '']
    for i, l in enumerate(lines, start=1):
        if i in cut_set or i in FOLD_LINES:
            continue
        kept.append(repl.get(i, l))
        if i == FOLD_INSERT_AFTER:
            kept.extend(FOLD_REGISTER.rstrip('\n').split('\n'))
            kept.append('')
        if i == INSERT_AFTER:
            kept.append(NEW_C3348.rstrip('\n'))
            kept.append('')
    collapsed = []
    for l in kept:
        if l == '' and collapsed and collapsed[-1] == '':
            continue
        collapsed.append(l)

    # size-aware c3280: compute the landing size with a placeholder first
    draft = '\n'.join(collapsed).replace('__C3280__',
                                         C3280_NEW_TMPL.replace('__NEW_SIZE__', 'X' * 24))
    nbytes = len(draft.encode('utf-8'))
    nlines = draft.count('\n') + 1
    headroom = (200 * 1024 - nbytes) / 5440.0
    size_str = f"{nbytes/1024:.1f}KB/{nlines}ln, ~{headroom:.0f} cycles of headroom"
    new_queue_text = '\n'.join(collapsed).replace(
        '__C3280__', C3280_NEW_TMPL.replace('__NEW_SIZE__', size_str))

    # --- archive ----------------------------------------------------------
    archived_reports = ['\n'.join(lines[a_ - 1:b_]).rstrip('\n') for a_, b_ in CUTS]
    header = (
        f"\n## Archived by cycle {CYCLE} (from tasks/queue.md, TRIM DUE at "
        "211.5KB/1085ln with **~-2 cycles of headroom** -- past `STANDING "
        "c3280`'s own ~3-cycle trigger AND **8-11 cycles past the c3337-c3340 "
        "re-trim window that item itself predicted**, the identical staleness "
        "failure c3347 hit on `STANDING c3296`'s STATUS.md window one cycle "
        "earlier. Four things archived here, in the order the fresh per-block "
        "census ranked them. (1) THE BULK: the **8 oldest of 13** live "
        "per-cycle report blocks -- c3339, c3334, c3333, c3332, c3330, c3328, "
        "c3327, c3326, 30.7KB -- keeping the newest 5 (c3347, c3346, c3345, "
        "c3344, c3342) at the documented floor, which c3348's own prepended "
        "block makes 6. `CLOSED c3329`, `CLOSED c3336` and `CLOSED c3336b` are "
        "standing one-off closures, NOT per-cycle reports, and were KEPT; the "
        "script asserts that by name. (2) THE PREDICTED ONE: the `PARTIALLY "
        "DONE` vendor-catalogue tracker had regrown to **16,041B** -- doubled "
        "from 8,532B at c3332, exactly the ~1.5KB/batch rate c3324 forecast -- "
        "and this time in BOTH places: ~3.0KB of batch narrative in its HEAD "
        "line, and two FULL batch paragraphs (c3340, c3341) inside the very "
        "`Per-batch results, one line each` line whose entire purpose is to "
        "prevent that. All of it is verbatim below; the live block now carries "
        "one line per batch for all five unlogged batches (c3335, c3338, c3340, "
        "c3341, c3343), and the reusable precedent those paragraphs established "
        "was promoted into the live `STANDING RULING BUCKETS` line as **bucket "
        "(7), 'dominated by an already-disclosed cheaper-or-equal rival'** -- "
        "the same consolidation move c3320 made. (3) THE SECOND PREDICTED ONE, "
        "new this cycle: **`STANDING c3280` itself, 9,117B**, almost all of it "
        "DONE narrative for 7 past trims. Its own lesson -- *a block that was "
        "compressed before is a PRIME census candidate* -- had never been "
        "applied to itself. Full text verbatim below; the live item keeps the "
        "decision rule, the 4-step method, the 3 transferable lessons and a "
        "one-line-per-trim history. (4) CORRECTNESS, not just bytes (the c3320 "
        "rule): the tracker carried **two running-score counters that "
        "disagree** -- head line '17 real undercutters in 340 rows (~5.0%)' "
        "(last updated c3340) vs score line '12 in 316 rows (~3.8%)' (last "
        "updated c3332), against 358 rows triaged. c3348 did NOT re-derive the "
        "true count (research, not a trim); both are labelled UNRELIABLE in "
        "place and the reconciliation is filed as `NEW c3348`. Hazard-grepped "
        "first, 3 passes: (a) `grep -rn \"see tasks/queue.md\\|tasks/queue.md, "
        "cycle\" bin actors site notes state` -> only the standing false "
        "positives (dead `_trimNNNNq.py` docstrings); (b) by-name sweep for "
        "c3326/c3327/c3328/c3330/c3332/c3333/c3334/c3339 across bin actors site "
        "notes state -> hits only in `state/STATUS.md` and "
        "`state/STATUS_ARCHIVE.md` narrative, each of which keeps its own "
        "record, no \"see queue.md item cXXXX\" pointer; (c) INTRA-FILE over "
        "every KEPT line -> **1 real dangling pointer owed by this cut**: the "
        "live HIGH item `NEW c3328` cited '(see `CLOSED c3328`)', repaired in "
        "place to name this header. Its other citation, 'see `CLOSED c3329` "
        "above', is safe -- c3329 is a standing closure and is kept. Newest-"
        "first, verbatim.) ##\n\n"
        + '\n\n'.join(archived_reports) + '\n\n'
        + "### Vendor-catalogue tracker HEAD-line batch narrative, cut from "
          "L108 by cycle 3348 (verbatim; the live head line now points here and "
          "the results live as one line each in the per-batch line)\n\n"
        + head_narr.rstrip() + '\n\n'
        + "### Vendor-catalogue tracker PER-BATCH-line paragraphs for c3340 and "
          "c3341, cut from L114 by cycle 3348 (verbatim; these broke that very "
          "line's own one-line-per-batch rule, the third time it has been "
          "broken -- c3320, c3332, c3348)\n\n"
        + batch_p1.rstrip() + '\n\n' + batch_p2.rstrip() + '\n\n'
        + "### The 8 pending competitor-audit fold-in items in full, cut from "
          "L65/L66/L68/L70/L80/L84/L86/L88-L93 by cycle 3348 and consolidated "
          "into the live `FOLD-IN REGISTER` (verbatim, 16.0KB -- every handle, "
          "price ladder, user count and catalogue row number is preserved here; "
          "the register keeps the handle, the scope, the magnitude and the "
          "reason each one is owed a rotation paragraph)\n\n"
        + '\n\n'.join(lines[ln - 1] for ln in sorted(FOLD_LINES)) + '\n\n'
        + "### `STANDING c3280` in full, as it stood before cycle 3348 "
          "re-compressed it (verbatim, 9,117B -- the live item keeps the "
          "decision rule, the 4-step method, the 3 transferable lessons and a "
          "one-line-per-trim history)\n\n"
        + c3280_old_full + '\n'
    )

    # --- multiset losslessness -------------------------------------------
    combined = new_queue_text + '\n' + header
    combined_lineset = set(l for l in combined.split('\n') if l.strip())
    missing = []
    for ln_num, l in enumerate(lines, start=1):
        if not l.strip() or ln_num in rewritten:
            continue
        if l not in combined_lineset:
            missing.append((ln_num, l[:80]))
    assert not missing, f"LOSSY CUT, missing lines: {missing}"

    for a_, b_ in CUTS:
        assert '\n'.join(lines[a_ - 1:b_]).rstrip('\n') in header, \
            f"cut ({a_},{b_}) not archived verbatim"
    for frag, name in ((head_narr.rstrip(), 'tracker head narrative'),
                       (batch_p1.rstrip(), 'c3340 paragraph'),
                       (batch_p2.rstrip(), 'c3341 paragraph'),
                       (c3280_old_full, 'old STANDING c3280')):
        assert frag in header, f"{name} not archived verbatim"

    # --- edits stuck ------------------------------------------------------
    assert C3328_NEW in new_queue_text, "pointer repair missing"
    assert HEAD_NARR_START not in new_queue_text, "tracker head narrative survived"
    assert BATCH_P1_START not in new_queue_text, "c3340 paragraph survived"
    assert BATCH_P2_START not in new_queue_text, "c3341 paragraph survived"
    assert SCORE_OLD not in new_queue_text, "stale score line survived"
    assert 'BOTH COUNTERS ARE UNRELIABLE' in new_queue_text, "score rewrite missing"
    assert '(7) **Dominated by an already-disclosed' in new_queue_text, "bucket 7 missing"
    assert 'c3343 rows 353-358: 0/6' in new_queue_text, "batch one-liners missing"
    assert 'NEW c3348 (LOW-MEDIUM' in new_queue_text, "NEW c3348 missing"
    assert 'RE-COMPRESSED c3348' in new_queue_text, "c3280 rewrite missing"
    assert '__C3280__' not in new_queue_text and '__NEW_SIZE__' not in new_queue_text, \
        "placeholder survived"
    assert 'Re-trim around **c3337-c3340**' not in new_queue_text, "stale window survived"
    assert 'Re-trim around **c3353-c3356**' in new_queue_text, "new window missing"
    for tag in ('CLOSED c3348', 'CLOSED c3347', 'CLOSED c3346', 'CLOSED c3345',
                'CLOSED c3344', 'CLOSED c3342', 'CLOSED c3329', 'CLOSED c3336',
                'NEW c3328', 'FOLD-IN REGISTER'):
        assert tag in new_queue_text, f"lost {tag} from the live file"
    # every consolidated fold-in handle must still be greppable in the live file
    for handle in ('nomad-agent/dynamitejobs-scraper', 'hipersoft/himalayas-scraper',
                   'kadi_bence/remote-jobs-scraper',
                   'accountable_eel/himalayas-jobs-lookup',
                   'unfenced-group/remoteok-scraper',
                   'accountable_eel/workingnomads-jobs-lookup',
                   'accountable_eel/remoteok-jobs-lookup',
                   'actor-forge/remote-jobs', 'deepmine/workable-jobs',
                   'tidytools/ats-career-site-jobs',
                   'wulfcare/app-store-reviews-scraper', 'actor-forge/eu-tenders'):
        assert handle in new_queue_text, f"fold-in handle {handle} lost from live file"
    for ln, tag in FOLD_LINES.items():
        assert lines[ln - 1] in header, f"fold-in item {tag} not archived verbatim"
    for tag in ('CLOSED c3339', 'CLOSED c3334', 'CLOSED c3333', 'CLOSED c3332',
                'CLOSED c3330', 'CLOSED c3327', 'CLOSED c3326'):
        assert tag in header, f"{tag} not in the archive"

    rep_bytes = sum(len(b_.encode('utf-8')) for b_ in archived_reports)
    print(f"orig queue.md: {len(orig.encode('utf-8'))} bytes, {len(lines)} lines")
    print(f"new  queue.md: {len(new_queue_text.encode('utf-8'))} bytes, "
          f"{len(collapsed)} lines  ({size_str})")
    print(f"  report blocks archived: 8 of 13 ({rep_bytes} bytes)")
    print(f"  tracker head narrative: {len(head_narr.encode('utf-8'))} bytes")
    print(f"  tracker c3340+c3341 paragraphs: "
          f"{len((batch_p1 + batch_p2).encode('utf-8'))} bytes")
    print(f"  old STANDING c3280: {len(c3280_old_full.encode('utf-8'))} bytes")
    print(f"archive append: {len(header.encode('utf-8'))} bytes")
    print("multiset check: OK, 0 missing lines; 2 ranges + 4 fragments archived "
          "verbatim; 6 in-place edits verified")

    if write:
        with open(QUEUE, 'w', encoding='utf-8') as f:
            f.write(new_queue_text)
        with open(ARCHIVE, 'a', encoding='utf-8') as f:
            f.write(header)
        print("WRITTEN.")
    else:
        print("dry run only -- pass --write to apply")


if __name__ == '__main__':
    main()
