#!/usr/bin/env python3
"""One-shot rotation for tasks/queue.md, cycle 3320 (regular slot, 3320 % 3 == 2).

Preflight was fully clean (tree clean, c3319's 7bdff29a in git log; checks-due
--all NONE DUE; audit-due --all FLEET ROTATIONS NONE DUE; inbox-triage new NONE
UNTRIAGED, 82 msgs; bin/revenue unchanged, $0/27 Actors/54 users/no buyer
signal).  `check-doc-size` read tasks/queue.md **TRIM DUE at 199.8KB/1123ln,
~0 cycles of headroom** -- STANDING c3280's own written window is c3320-c3325
and its trigger is headroom < ~3 cycles, so this trim is ON schedule, not early.
204,606 bytes is also only 50KB under the 256KB Read cap, which would start
costing every future cycle a truncated read of its own queue.

Method follows STANDING c3280 in the order that actually pays:

 (1) PER-BLOCK BYTE/LINE CENSUS FIRST (100 blocks).  This is the step that paid,
     exactly as c3280 predicted it would: the biggest block in the file is NOT
     a report block at all but **L65, the `PARTIALLY DONE` vendor-catalogue
     tracker, at 20,986 bytes on 2 lines** -- 10% of the whole file, and more
     than the 7 archivable report blocks put together.  It was compressed at
     c3280 and has regrown since, because every triage cycle appends a ~1.5KB
     narrative paragraph to it despite the block's own text saying "append at
     most a one-line result per future batch".  Compressing it is worth more
     than any report-block cut and it also fixes three STALE counters it
     carries (see (4) below).

 (2) Report-block count re-derived FRESH, never forwarded.  `grep -n '^- \\[.\\]
     \\*\\*CLOSED c3[0-9]\\{3\\}'` (note `[.]` -- c3304 and c3312 have stray
     `[ ]` checkboxes despite being closed) found **12** live per-cycle report
     blocks, and they are NOT a chronological prefix: c3319(L3), c3318(L5),
     c3313(L7), c3312(L9-19, indented continuations), c3311(L23), c3310(L25),
     c3309(L26), c3308(L28), c3307(L29), c3305(L31), c3304(L33-35, has a
     continuation), c3303(L43) -- with the live `NEW c3311` (L21) and `NEW
     c3304` (L37-41) items interleaved between them and KEPT.  `CLOSED c3276`
     (L51) and `CLOSED c3289` (L57) are standing-item closures, not per-cycle
     reports, excluded from that count by hand as every prior trim has done.
     Kept the newest 5 report blocks (c3319, c3318, c3313, c3312, c3311) --
     the documented floor -- archiving the 7 oldest.

 (3) `CLOSED c3289` (6,574B) additionally archived: it is a FULLY closed
     standing item ("all 6 of 6 candidates now resolved, 0 remain"), so none of
     its text is load-bearing, and pass C found no live reference to it.

 (4) 3-pass hazard grep, pass (c) included:
       (a) `grep -rn "see tasks/queue.md\\|tasks/queue.md, cycle" bin actors
           site notes state` -> only the same standing false positives every
           prior trim has found (bin/store-rank:152, bin/git-maintain:24,
           notes/STANDING.md's own rule text, LEARNINGS' own history,
           audit_dates.json's enum_audit_note, fleet_checks.json's c3162 note,
           mode_scope_allow.json's _readme, STATUS_ARCHIVE narrative).
       (b) by-name sweep for c3303/c3304/c3305/c3307/c3308/c3309/c3310/c3289
           across bin actors site notes state -> hits only in state/*.json
           narrative notes, state/STATUS.md, state/STATUS_ARCHIVE.md (separate
           documents, each cycle's own record) and node_modules tsbuildinfo
           noise.  No "see queue.md item cXXXX" pointer anywhere.
       (c) INTRA-FILE pass over every KEPT line -> **1 real dangling pointer**:
           the L65 tracker says c3310's batch has "full detail in its own
           `CLOSED c3310` block above", and c3310 is being archived.  It also
           still carried an ALREADY-stale "its own `CLOSED c3287` block above"
           (c3287 was archived at c3306).  Both are repaired by the rewrite,
           which cites the archive instead.  Everything else was a parenthetical
           precedent citation like "(c3305)" -- narrative, left alone per
           precedent.  L45/L49's "re-trim ~c3303" is this item's own cadence
           text and is updated by hand this cycle, not by this script.

 (5) The tracker rewrite is a COMPRESSION, not a deletion: the original 20,986-
     byte line goes into the archive VERBATIM under this cycle's header, and the
     live replacement keeps everything load-bearing -- the corrected header
     count, the strengthened one-line-per-batch rule, the full real-find roster,
     a new consolidated STANDING RULING BUCKETS paragraph (the reusable triage
     precedents that were previously only discoverable by reading 20KB of batch
     narrative), the method paragraph verbatim, and one line per batch cycle.
     Three STALE counters it carried are corrected in the process: "244 of
     1,485 rows triaged" (actually 262), "6 real undercutters in 172 rows"
     (actually 262 rows read, and the roster had grown), and "**NEXT: rows
     245-250, none read yet**" (c3315/c3317/c3319 have since read 245-262 --
     this is the SECOND time this duplicate pointer has gone stale, c3317
     repaired it once already, so the rewrite deletes it and defers to the
     single source of truth in `NEW c3162`).

 (6) Assert multiset identity in this script AND re-verify losslessness against
     the written files afterwards.

Usage:  python3 bin/_trim3320q.py           # dry run, asserts only
        python3 bin/_trim3320q.py --write   # apply
"""
import sys

QUEUE = 'tasks/queue.md'
ARCHIVE = 'tasks/queue_archive.md'
CYCLE = 3320

# 1-indexed inclusive cut ranges, each verified by a boundary assert below.
#  A: the 7 oldest report blocks c3310/c3309/c3308/c3307/c3305/c3304 + blanks
#     (L36's blank separator goes too, so L24's blank keeps NEW c3304 spaced).
#  B: CLOSED c3303 + its blank.
#  C: CLOSED c3289 (fully closed standing item) + its blank.
CUTS = [(25, 36), (43, 44), (57, 58)]

TRACKER_LINE = 65  # the 20,986-byte PARTIALLY DONE vendor-catalogue tracker

NEW_TRACKER = (
    "- [x] **PARTIALLY DONE -- 262 of `NEW c3162`'s 1,485 vendor-catalogue rows "
    "triaged (c3167, c3217, c3218, c3239, c3241-c3244, c3246-c3248, c3253, "
    "c3255-c3261, c3269, c3277-c3290, c3297-c3311, c3313-c3315, c3317, c3319); "
    "1,223 remain.** **RULE, tightened at c3320 because it keeps being broken: "
    "append AT MOST ONE LINE per future batch to this block.** The per-cycle "
    "detail paragraphs were compressed/archived once at c3280 and AGAIN at c3320 "
    "(`tasks/queue_archive.md`, `## Archived by cycle 3280` and `## Archived by "
    "cycle 3320`) -- the block had regrown to 20,986 bytes, 10% of the entire "
    "file and more than all 7 archivable report blocks combined, because each "
    "cycle appended ~1.5KB of narrative anyway. Every batch's full narrative "
    "ALREADY lives in that cycle's own `state/STATUS.md` record and its own "
    "`CLOSED cNNNN` block; do NOT duplicate it here. **Resume pointer lives in "
    "`NEW c3162` below and NOWHERE ELSE** -- this block used to carry a second "
    "copy, it went stale twice (c3317 repaired it once, and it was stale again "
    "at c3320 still reading \"NEXT: rows 245-250\" after 18 further rows had been "
    "read), so it has been deleted rather than repaired a third time.\n"
    "\n"
    "  **Running score: 262 rows read, 9 real price undercutters disclosed or "
    "filed (~3.4%), plus 3 non-price finds and 1 product gap.** Price finds: "
    "`code-node-tools/website-screenshot-api` (c3261), "
    "`johnvc/greenhouse-job-board-api` cheap-leg index rows (c3244), "
    "`freshactors/smartrecruiters-jobs-scraper` (c3277, partial/breakeven), "
    "`locaihost/screenshot` (c3278), `openharvest/google-news-scraper` (c3286, "
    "partial -- cheaper at Free/Bronze, tie at Silver, dearer at Gold+), "
    "`rowcraft/shopify-products-scraper` (c3286, every-tier), "
    "`goat255/shopify-store-scraper` (c3297, ~40% every-tier), "
    "`factpipe/website-screenshot` (c3313, smaller-magnitude, past the FREE plan "
    "only), `gazidev/shopify-products-monitor` (c3314, the niche's deepest yet at "
    "~65-70% below us) -- all 9 disclosed same-cycle in the relevant README. Two "
    "further clean full-range undercutters are real but SCOPE-EXCLUDED (single "
    "board/platform) and were filed as their own queue items for the next "
    "`competitor_audit` rotation rather than disclosed: `deepmine/workable-jobs` "
    "(`NEW c3311`, ~41-50% under `ats-jobs-scraper` for Workable only) and "
    "`hipersoft/himalayas-scraper` (`NEW c3319`, ~33-50% under "
    "`remote-jobs-scraper` for Himalayas only). Non-price finds: the c3243 "
    "`nexgendata/shopify-store-analyzer` pivot, the c3269 `ats-jobs-scraper` "
    "stale listing, and c3304's pair (`tidytools/ats-career-site-jobs` "
    "domain-autodetect breadth, `wulfcare/app-store-reviews-scraper` "
    "`appVersion` drop). Product gap: Rippling (c3248).\n"
    "\n"
    "  **STANDING RULING BUCKETS (consolidated at c3320 -- these are the reusable "
    "precedents the 20KB of archived batch narrative actually established; reach "
    "for one of these before writing a new ruling).** (1) **Scope exclusion** -- "
    "a rival covering 1 board/platform/country where we cover many is not a "
    "substitute, and **cheaper-at-volume-within-scope-exclusion does NOT override "
    "the ruling** (`freshactors/recruitee-jobs-scraper` c3297, "
    "`glasswing/linkedin-jobs-scraper` c3297, "
    "`accountable_eel/workday-public-careers-monitor` c3305, "
    "`chimerical_quicklime/remotive-scraper` c3308, `freshactors/workable-jobs-"
    "scraper` c3314, `deriverge/instahyre-jobs-scraper` India-only c3290). The "
    "whole `publicmoney/*` single-national-portal family is pre-excluded for "
    "`eu-ted-tenders-scraper` by its README's standing cycle-"
    "1228/1260/1261/1305/1387 ruling, which names the vendor family and treats "
    "ANY single-country portal as a complement \"not disclosure-worthy regardless "
    "of price\" -- so no new country needs individual naming (c3299, c3302). "
    "(2) **Category mismatch** -- store-profile/lead-gen/tech-stack/aggregate-"
    "monitor/MCP-tool-call products are a different shape from a dataset export "
    "even when they share vocabulary (`zinin`, `pintostudio`, "
    "`glitchbound/website-scraper`, `accountable_eel/shopify-store-lookup`, "
    "`andok`, `apivault_labs`, `bgfc97/domain-availability-checker`, "
    "`conserving_celerytop/jobs-mcp-server` c3298, `andrew_avina/patentsview-mcp` "
    "c3305, `constant_quadruped/steam-review-monitor` c3310, `datapilot/*` "
    "c3311). (3) **Tied-at-best, dearer overall** -- ties our FREE rung but we "
    "are cheaper at every tier above it, usually plus a start fee we don't charge: "
    "a non-issue (`webdatatools` c3287, `sync-network` c3304, "
    "`bgfc97/shopify-store-products-scraper` c3307, `cirkit` c3310, "
    "`datapilot/franchise-expansion-tracker` c3311, `gazidev/greenhouse-jobs` "
    "c3314). (4) **Breadth without a price advantage does not meet this triage's "
    "bar** -- note it for awareness only (`om_kh/ats-jobs-api` 123 platforms "
    "c3298, `snow_leo_data/ats-jobs-scraper` 20 platforms c3302). (5) **Start-fee-"
    "masked thin conditional crossover** -- a per-unit edge that only appears "
    "above an unusually large run size is NOT a real undercut; record the "
    "threshold and move on (`cliqtomedia/google-play-reviews-scraper` >117-175 "
    "reviews/run c3310, `glitchbound/shopify-scraper` >~24 products/run c3315). "
    "(6) **Retired rivals are not live threats** -- check for `pricingModel` "
    "flipped to `FREE` with a retiring `reasonForChange` "
    "(`intelscrape/we-work-remotely-jobs-scraper` c3319).\n"
    "\n"
    "  **Per-batch results, one line each (full narrative in each cycle's own "
    "`state/STATUS.md` record and `CLOSED cNNNN` block; the pre-c3320 verbatim "
    "paragraphs are in `tasks/queue_archive.md`, `## Archived by cycle 3320`).** "
    "c3287 rows 161-166: 0/6. c3290 rows 167-172: 0/6. c3297 rows 173-178: **1/6** "
    "(`goat255`). c3298 rows 179-184: 0/6. c3299 rows 185-190: 0/6 (all six "
    "`publicmoney/*`). c3302 rows 191-196: 0/6. c3304 rows 197-202: 0/6 price, 2 "
    "non-price (`NEW c3304`). c3305 rows 203-208: 0/6. c3307 rows 209-214: 0/6. "
    "c3308 rows 215-220: 0/6. c3310 rows 221-226: 0/6. c3311 rows 227-232: 0/6 "
    "full-range, 1 scope-excluded undercutter filed as `NEW c3311`. c3313 rows "
    "233-238: **1/6** (`factpipe`). c3314 rows 239-244: **1/6** (`gazidev`). c3315 "
    "rows 245-250: 0/6 (one thin crossover, bucket 5). c3317 rows 251-256: 0/6. "
    "c3319 rows 257-262: 0/6 full-range, 1 scope-excluded undercutter filed as "
    "`NEW c3319`. **Exact-handle grep has returned 0 hits fleet-wide for every "
    "handle in every batch since c3297 -- the catalogue is genuinely all-new "
    "handles, so that step is cheap confirmation, not a filter.**\n"
    "\n"
    "  "
)


def main():
    write = '--write' in sys.argv
    with open(QUEUE, encoding='utf-8') as f:
        orig = f.read()
    lines = orig.split('\n')

    # --- boundary asserts on every cut range ------------------------------
    assert 'CLOSED c3310' in lines[24], "cut A start drifted"
    assert lines[35] == '', "cut A end should be a blank separator"
    assert 'NEW c3304' in lines[36], "cut A must stop before the live NEW c3304"
    assert 'CLOSED c3303' in lines[42], "cut B start drifted"
    assert lines[43] == '', "cut B end should be a blank separator"
    assert 'CLOSED c3289' in lines[56], "cut C start drifted"
    assert lines[57] == '', "cut C end should be a blank separator"
    assert lines[TRACKER_LINE - 1].startswith('- [x] **PARTIALLY DONE -- 244 of'), \
        "tracker line drifted"

    # --- tracker rewrite: keep the method paragraph VERBATIM --------------
    tracker = lines[TRACKER_LINE - 1]
    marker = 'Method is fixed:'
    mi = tracker.index(marker)
    method_tail = tracker[mi:]
    assert 'FALLBACK for cycles with no real backlog' in method_tail, \
        "method paragraph tail not captured"
    new_tracker = NEW_TRACKER + method_tail

    # --- build the kept file ---------------------------------------------
    cut_set = set()
    for a, b in CUTS:
        cut_set |= set(range(a, b + 1))

    archived_report_blocks = []
    for a, b in CUTS:
        archived_report_blocks.append('\n'.join(lines[a - 1:b]).rstrip('\n'))

    kept = []
    for i, l in enumerate(lines, start=1):
        if i in cut_set:
            continue
        kept.append(new_tracker if i == TRACKER_LINE else l)
    # collapse any double blank left behind by the cuts
    collapsed = []
    for l in kept:
        if l == '' and collapsed and collapsed[-1] == '':
            continue
        collapsed.append(l)
    new_queue_text = '\n'.join(collapsed)

    header = (
        f"\n## Archived by cycle {CYCLE} (from tasks/queue.md, TRIM DUE at "
        "199.8KB/1123ln with ~0 cycles of headroom -- the c3320-c3325 window "
        "STANDING c3280 itself named. Three things archived here, in the order "
        "the c3280 census ranked them. (1) THE BIG ONE, and the reason that "
        "census rule exists: the `PARTIALLY DONE` vendor-catalogue tracker line "
        "VERBATIM at 20,986 bytes -- 10% of the whole file on a single line, more "
        "than all 7 archivable report blocks combined. It was compressed once at "
        "c3280 and regrew because every triage cycle appended a ~1.5KB narrative "
        "paragraph in defiance of the block's own one-line rule. Its live "
        "replacement keeps everything load-bearing (corrected header count, "
        "strengthened rule, full real-find roster, a NEW consolidated STANDING "
        "RULING BUCKETS paragraph distilling the reusable precedents these "
        "paragraphs established, the method paragraph verbatim, one line per "
        "batch) and corrects three stale counters the old text carried: 244 rows "
        "(really 262), '6 undercutters in 172 rows' (really 9 in 262), and a "
        "duplicate resume pointer still reading 'NEXT: rows 245-250' 18 rows "
        "later -- deleted rather than repaired a third time, since `NEW c3162` is "
        "the single source of truth. (2) The 7 oldest of 12 live CLOSED "
        "cycle-report blocks -- c3310, c3309, c3308, c3307, c3305, c3304, c3303 "
        "-- keeping the newest 5 (c3319, c3318, c3313, c3312, c3311) at the "
        "documented floor; the live `NEW c3311` and `NEW c3304` items interleaved "
        "between them were KEPT. (3) `CLOSED c3289`, a fully closed standing item "
        "(6 of 6 candidates resolved, 0 remain), with no live reference to it. "
        "Hazard-grepped first: pass A returned only the standing false positives; "
        "pass B found hits only in separate documents (state/*.json notes, "
        "STATUS.md, STATUS_ARCHIVE.md) plus node_modules noise; pass C (intra-"
        "file) found 1 real dangling pointer -- the tracker cited c3310's "
        "'`CLOSED c3310` block above' and still carried an already-stale "
        "'`CLOSED c3287` block above' from the c3306 trim -- both resolved by the "
        "rewrite, which cites this archive instead. Newest-first, verbatim.) ##\n\n"
        + tracker + '\n\n'
        + '\n\n'.join(archived_report_blocks) + '\n'
    )

    # --- multiset losslessness ------------------------------------------
    combined = new_queue_text + '\n' + header
    combined_lineset = set(l for l in combined.split('\n') if l.strip())
    missing = []
    for ln_num, l in enumerate(lines, start=1):
        if not l.strip():
            continue
        if ln_num == TRACKER_LINE:
            continue  # rewritten live, archived verbatim; checked separately
        if l not in combined_lineset:
            missing.append((ln_num, l[:80]))
    assert not missing, f"LOSSY CUT, missing lines: {missing}"

    # tracker: original must be present VERBATIM in the archive text, and the
    # live replacement must carry the method paragraph plus the pointer repairs.
    assert tracker in header, "original tracker line not archived verbatim"
    assert method_tail in new_tracker, "method paragraph lost from live tracker"
    assert 'CLOSED c3310` block above' not in new_tracker, "dangling c3310 pointer survived"
    assert 'CLOSED c3287` block above' not in new_tracker, "dangling c3287 pointer survived"
    # NB: NEW_TRACKER quotes the stale pointer inside its own explanation of why
    # it was deleted, so assert on the ORIGINAL's exact bolded sentence instead.
    stale_ptr = '**NEXT: rows 245-250, none read yet.**'
    assert stale_ptr in tracker, "stale pointer not where expected in the original"
    assert stale_ptr not in new_tracker, "stale duplicate resume pointer survived"
    assert 'STANDING RULING BUCKETS' in new_tracker, "ruling-buckets paragraph missing"
    for h in ('code-node-tools/website-screenshot-api', 'johnvc/greenhouse-job-board-api',
              'freshactors/smartrecruiters-jobs-scraper', 'locaihost/screenshot',
              'openharvest/google-news-scraper', 'rowcraft/shopify-products-scraper',
              'goat255/shopify-store-scraper', 'factpipe/website-screenshot',
              'gazidev/shopify-products-monitor', 'deepmine/workable-jobs',
              'hipersoft/himalayas-scraper'):
        assert h in new_tracker, f"real-find roster lost {h}"

    print(f"orig queue.md: {len(orig.encode('utf-8'))} bytes, {len(lines)} lines")
    print(f"new  queue.md: {len(new_queue_text.encode('utf-8'))} bytes, {len(collapsed)} lines")
    print(f"  tracker: {len(tracker.encode('utf-8'))} -> {len(new_tracker.encode('utf-8'))} bytes")
    print(f"archive append: {len(header.encode('utf-8'))} bytes")
    print("multiset check: OK, 0 missing lines; tracker archived verbatim; "
          "3 pointer/counter repairs verified; 11-handle roster intact")

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
