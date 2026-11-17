#!/usr/bin/env python3
"""One-shot rotation for tasks/queue.md, cycle 3332 (regular slot, 3332 % 3 == 2).

Preflight fully clean on arrival (tree clean, c3331's `f4fd6b1a` in `git log`;
`checks-due --all` NONE DUE; `audit-due --all` FLEET ROTATIONS NONE DUE;
`inbox-triage new` NONE UNTRIAGED, 82 msgs; `bin/revenue` unchanged -- $0 /
27 Actors / 54 users / 1558 runs30d / no buyer signal).  `check-doc-size` run on
arrival: **tasks/queue.md TRIM DUE at 195.3KB/1062ln with ~1 cycle of headroom**
-- below `STANDING c3280`'s own ~3-cycle trigger and inside the c3331-c3334
window that item names, so this trim is ON schedule, not a reaction to the
banner.  `state/STATUS.md` is also TRIM DUE on the banner but at ~5 cycles of
headroom, i.e. still above the trigger -- deliberately NOT trimmed this cycle
(`STANDING c3296` owns its cadence; expect it to cross at ~c3334-c3336).

Method follows STANDING c3280 in the order that pays:

 (1) PER-BLOCK CENSUS FIRST, re-derived fresh (101 blocks).  Largest live blocks:
     the `PARTIALLY DONE` vendor-catalogue tracker (8,532B/10ln -- exactly the
     regrowth c3324 predicted, "~1.5KB per triage batch, re-compress roughly
     every 5 batches", and 6 batches have landed since c3320), `STANDING c3280`
     itself (8,230B, the trim rule), `COMPRESSED c2994` (6,207B/74ln),
     `PARTIALLY DONE at c3250` (5,227B, the live Rippling plan -- keep),
     `NEW c3162` (4,846B).

 (2) REPORT BLOCKS re-derived FRESH, never forwarded.  13 live per-cycle report
     blocks: c3330(L1), c3328(L5), c3327(L7), c3329(L13), c3326(L21), c3325(L27),
     c3324(L29), c3323(L31-36), c3322(L37-42), c3321(L43-50), c3320(L55-56),
     c3319(L59-60), c3311(L63-64).  Kept the newest 5 -- c3330, c3329, c3328,
     c3327, c3326 -- which this cycle's own prepended block makes 6; archived the
     8 oldest (~30.9KB, the bulk of this trim).  The live `NEW c3321`(L51),
     `NEW c3319`(L57) and `NEW c3311`(L61) items interleaved between them are
     KEPT -- all three are still-open fold-in notes for `remote-jobs-scraper` /
     `ats-jobs-scraper`.  `NEW c3220b SWEEP CLOSED`, `RESOLVED c3228`,
     `SETTLED c3216`, `CLOSED c3276`-style standing closures are not per-cycle
     reports and are excluded from that count by hand, as every prior trim has.

 (3) THE SECOND CUT IS THE PREDICTED ONE.  `NEW c3162`'s tail (1,449 -> end of
     L104, 3,396B) had regrown into two FULL batch paragraphs for c3330 and
     c3331, which is the exact thing the tracker's own RULE forbids ("append AT
     MOST ONE LINE per future batch").  Both are archived verbatim and replaced
     by a pointer; their one-line forms (plus the c3327 and c3332 batches, which
     were never added) go into the tracker's `Per-batch results, one line each`
     line (L91) where the rule says they belong.

 (4) 3-pass hazard grep, pass (c) included -- see the archive header for results.

 (5) Multiset identity asserted here AND re-verified against the written files
     afterwards.

Usage:  python3 bin/_trim3332q.py           # dry run, asserts only
        python3 bin/_trim3332q.py --write   # apply
"""
import sys

QUEUE = 'tasks/queue.md'
ARCHIVE = 'tasks/queue_archive.md'
CYCLE = 3332

# 1-indexed inclusive cut ranges (block + trailing blank/separator), newest-first
# order of the blocks they contain: c3325, c3324, c3323, c3322, c3321, c3320,
# c3319, c3311.
CUTS = [(27, 28), (29, 30), (31, 36), (37, 42), (43, 50),
        (55, 56), (59, 60), (63, 64)]

C3162_LINE = 104          # NEW c3162 (the triage item)
TRACKER_HEAD = 85         # PARTIALLY DONE -- N of 1,485 rows triaged
TRACKER_SCORE = 87        # Running score line
TRACKER_BATCH = 91        # Per-batch results, one line each
C3280_LINE = 75           # STANDING c3280 (the trim rule itself)

# --- this cycle's own report block, prepended ------------------------------
REPORT = (
    "- [x] **CLOSED c3332 -- regular slot (3332 % 3 == 2, verified with `echo "
    "$((3332 % 3))`). Preflight fully clean on arrival** (tree clean, c3331's "
    "`f4fd6b1a` present in `git log`; `checks-due --all` **NONE DUE** (soonest "
    "`check-status-continuity` in 7c, c3339); `audit-due --all` **FLEET "
    "ROTATIONS NONE DUE** (only the informational one-off/experimental axes -- "
    "`count_audit`, `feature_diff_audit`, `input_error_advice`, "
    "`watch_subset_audit`, `within_field_and_audit`, c1304 rule, not a "
    "backlog); `inbox-triage new` **NONE UNTRIAGED** (82 msgs, zero new mail); "
    "`bin/revenue` unchanged -- **$0 booked, 27 Actors, 54 users, 1558 runs30d, "
    "31 ext_bad30d, 0 bookmarks/reviews, polar {}, no buyer signal**). **Two "
    "tasks, in priority order.** (1) **Continued the standing `NEW c3162` "
    "vendor-catalogue triage at rows 311-316 (indices 310-315)** -- live Apify "
    "GET per handle via a `bin/_triage3332.py` clone (deleted after use), "
    "`cps.effective(pricingInfos, now)` for the tier actually in force, every "
    "charge event and tier rung read, each rival's live description/README read "
    "for scope, exact-handle grep across `actors/*/README.md`/`site/`/`notes/` "
    "confirming all 6 genuinely new (**0 hits**). **0 of 6 real.** The one that "
    "needed real work was `publicmoney/awards-ticker-mini` (3u, flagged under "
    "`us-federal-awards-scraper`): it reads the SAME upstream (USAspending) and "
    "its tiered **$0.002 (Free) -> $0.0007 (Diamond)** + $0.00005 start fee is "
    "cheaper than our $0.004 -> $0.0025 at every tier -- but **our README "
    "already discloses that exact ladder, under that exact owner**: `README.md:"
    "225` names `publicmoney/usaspending-awards-scraper` at "
    "`$0.002 (Free) -> $0.0007 (Diamond)` (and `datamule/"
    "usaspending-gov-awards-scraper` cheaper still at $0.0005 -> $0.00025), so "
    "no buyer-facing price claim on that page is falsified and there is nothing "
    "to correct. Its live README/input schema also make it a **10-field "
    "ticker-attribution product** (`status`, `tickerSymbol`, `listedName`, "
    "`matchBasis`, `matchConfidence`, `recipientName`, `value`, "
    "`awardingAgency`, `startDate`, `url`, plus a `rollup` mode totalling by "
    "ticker) with **keyword-only filtering and ONE award type per run** "
    "(`mode`/`awardTypes`/`keyword`/`awardsToRead`/`matchedOnly`/`maxItems`) -- "
    "against our 52 typed fields, 6 award categories, sub-awards joined to "
    "prime, watch mode and opportunity score, it is a derived finance product, "
    "not a substitute. The other 5: `publicmoney/mendoza-compras-scraper` "
    "(Mendoza **province**, Argentina) and `publicmoney/monaqasat-qatar-scraper` "
    "(Qatar) are the standing single-portal scope exclusion against "
    "`eu-ted-tenders-scraper` and are not even EU, starker than the usual "
    "`publicmoney/*` ruling; `redfoxxie/apple-app-store-review-alert-monitor` "
    "and `redfoxxie/google-play-review-change-monitor-alerts` charge a flat "
    "**$0.005/alert** against our $0.0001 -> $0.00007 and flat $0.0001 -- **50x "
    "and 71x dearer** -- and their advertised features are all already ours "
    "(checked field by field against the live input schemas: rating filters "
    "`minRating`/`maxRating` and `minScore`/`maxScore`/`ratingFilter`, "
    "countries, `appVersions`, developer replies via `replyFilter`, helpful "
    "votes via `minVoteSum`/`minVoteCount`/`minThumbsUp`, and dedup via "
    "`watchLabel`/`watchEvents`), so no feature gap to close either; "
    "`rowfeed/shopify-store-list` is a BuiltWith-alternative technology-lookup "
    "list billed **$0.005/domain + a $0.02 start fee**, already covered "
    "generically by `shopify-products-scraper/README.md:119`'s "
    "lead/email-finder scope exclusion. **316/1,485 rows triaged (running "
    "score: 12 real undercutters in 316 rows, ~3.8%); next 6 (rows 317-322) "
    "named in `NEW c3162`.** (2) **Ran the queue.md trim `STANDING c3280` was "
    "due** (`check-doc-size`: 195.3KB/1062ln, **~1 cycle of headroom**, below "
    "the item's own ~3-cycle trigger and inside the c3331-c3334 window it "
    "named) -- `bin/_trim3332q.py`, archiving the 8 oldest of 13 live report "
    "blocks plus the two over-long batch paragraphs `NEW c3162` had regrown in "
    "breach of its own one-line rule. Guards: `check-charges`/"
    "`check-registry-fields` not re-run (no code/output-field/pricing change "
    "this cycle). All 3 services active; `/`, `/tools`, `/pricing` all **200**. "
    "**Spend: $0** (read-only own-token Apify metadata GETs only). **Blockers: "
    "none. Owner email: none owed.** **Pace: 0 new Actors built today "
    "(2026-11-17).**\n"
)

# --- L104 `NEW c3162`: resume pointer + the regrown tail -------------------
C3162_POINTER_OLD = (
    "**RESUME POINTER (updated c3331): rows 1-310 (indices 0-309) are DONE; "
    "next cycle starts at rows 311-316 (indices 310-315)**"
)
C3162_POINTER_NEW = (
    "**RESUME POINTER (updated c3332): rows 1-316 (indices 0-315) are DONE; "
    "next cycle starts at rows 317-322 (indices 316-321)**"
)
C3162_TAIL_START = "**c3330 batch (rows 299-304): 0 of 6 real, all non-issues.**"
C3162_TAIL_NEW = (
    "**Per-batch results live as ONE LINE EACH in the `PARTIALLY DONE` tracker "
    "above -- that is this item's own rule, and c3332 had to re-archive two full "
    "paragraphs (the c3330 and c3331 batches, 3.4KB) to restore it; they are "
    "verbatim in `tasks/queue_archive.md`, `## Archived by cycle 3332`, and each "
    "batch's full narrative is also in its own cycle's `state/STATUS.md` record "
    "and `CLOSED cNNNN` block. Do not paste a batch paragraph here again.** "
    "The three standing rulings these batches kept re-using are already "
    "consolidated in the tracker's `STANDING RULING BUCKETS` line -- reach for "
    "one of those before writing a new ruling."
)

# --- the tracker's own three summary lines --------------------------------
HEAD_OLD = ("**PARTIALLY DONE -- 298 of `NEW c3162`'s 1,485 vendor-catalogue rows "
            "triaged (c3167, c3217, c3218, c3239, c3241-c3244, c3246-c3248, c3253, "
            "c3255-c3261, c3269, c3277-c3290, c3297-c3327); 1,187 remain.**")
HEAD_NEW = ("**PARTIALLY DONE -- 316 of `NEW c3162`'s 1,485 vendor-catalogue rows "
            "triaged (c3167, c3217, c3218, c3239, c3241-c3244, c3246-c3248, c3253, "
            "c3255-c3261, c3269, c3277-c3290, c3297-c3332); 1,169 remain.**")

SCORE_OLD = ("**Running score: 292 rows read, 11 real price undercutters disclosed "
             "or filed (~3.8%), plus 3 non-price finds and 1 product gap.**")
SCORE_NEW = ("**Running score: 316 rows read, 12 real price undercutters disclosed "
             "or filed (~3.8%), plus 3 non-price finds and 1 product gap.** The "
             "12th is `nomad-agent/dynamitejobs-scraper` (c3327, filed in "
             "`NEW c3327` for `remote-jobs-scraper`'s next `competitor_audit`).")

BATCH_APPEND = (
    " **c3327 rows 293-298: 1/6** (`nomad-agent/dynamitejobs-scraper`, a new "
    "remote board at a lower rate -- filed in `NEW c3327`, not yet folded in); "
    "other 5 were 1 breadth-without-price DACH multi-ATS, 2 single-fixed-target "
    "boards (Ashby HQ's own listings; Stripe+Figma only -- no company field in "
    "either input schema), 2 dearer review scrapers. c3330 rows 299-304: 0/6 "
    "(1 BOAMP national-portal exclusion, 1 dearer HN, 1 single-ATS tie-then-"
    "undercut, 1 different-upstream regulations.gov, 2 category mismatches). "
    "c3331 rows 305-310: 0/6 (the whole batch was the `publicmoney/*` "
    "single-country-portal family -- Belgium, Slovenia, Scotland, Canada, "
    "Ukraine, Czechia). c3332 rows 311-316: 0/6 (2 more single-portal "
    "exclusions -- Mendoza province Argentina, Qatar -- 2 redfoxxie review "
    "monitors at a flat $0.005/alert, 50-71x dearer with no feature we lack, "
    "1 BuiltWith-style store list already covered generically, and "
    "`publicmoney/awards-ticker-mini`, whose cheaper $0.002->$0.0007 ladder is "
    "ALREADY disclosed on `us-federal-awards-scraper/README.md:225` under that "
    "same owner's other listing, so nothing was falsified)."
)

# --- STANDING c3280: record this trim and re-aim the next one -------------
C3280_OLD = (
    "`MERGED c2916` (3.4KB) -- `DECIDED c3081` is OFF this list, trimmed 4.8KB "
    "-> 2.6KB at c3324. Re-trim around **c3331-c3334** (headroom < ~3 cycles), "
    "not sooner."
)
C3280_NEW = (
    "`MERGED c2916` (3.4KB) -- `DECIDED c3081` is OFF this list, trimmed 4.8KB "
    "-> 2.6KB at c3324. **DONE c3332** (195.3KB/1062ln, **~1 cycle of "
    "headroom** on arrival -- the trigger fired inside the c3331-c3334 window "
    "this item predicted, which is the cadence working rather than a surprise): "
    "archived the 8 oldest of **13** live report blocks (c3325/c3324/c3323/"
    "c3322/c3321/c3320/c3319/c3311, ~30.9KB), keeping the newest 5 at the "
    "documented floor with this cycle's own block making 6, and separately "
    "re-compressed `NEW c3162`'s tail (3.4KB of two full batch paragraphs it "
    "had regrown in breach of its own one-line rule) back into the tracker's "
    "one-line-per-batch line. **The vendor-catalogue tracker remains the "
    "largest live block and the predicted next candidate** -- c3324 called its "
    "regrowth rate at ~1.5KB/batch and that held exactly, so budget a "
    "re-compression of it roughly every 5 batches regardless of what the "
    "banner says. `bin/_trim3332q.py` is the template to clone next. Re-trim "
    "around **c3337-c3340** (headroom < ~3 cycles), not sooner."
)


def main():
    write = '--write' in sys.argv
    with open(QUEUE, encoding='utf-8') as f:
        orig = f.read()
    lines = orig.split('\n')

    # --- boundary asserts on every cut range ------------------------------
    expect = {27: 'CLOSED c3325', 29: 'CLOSED c3324', 31: 'CLOSED c3323',
              37: 'CLOSED c3322', 43: 'CLOSED c3321', 55: 'CLOSED c3320',
              59: 'CLOSED c3319', 63: 'CLOSED c3311'}
    for ln, tag in expect.items():
        assert tag in lines[ln - 1], f"cut start drifted at L{ln} ({tag})"
    for a, b in CUTS:
        assert lines[b - 1] == '' or lines[b - 1] == '---', \
            f"cut ({a},{b}) must end on a blank/separator, got {lines[b - 1][:40]!r}"
    # the three live items interleaved between the cuts must survive
    for ln, tag in ((51, 'NEW c3321'), (57, 'NEW c3319'), (61, 'NEW c3311')):
        assert tag in lines[ln - 1], f"live item {tag} moved off L{ln}"
        assert not any(a <= ln <= b for a, b in CUTS), f"{tag} is inside a cut"
    # the 5 report blocks that must stay
    for ln, tag in ((1, 'CLOSED c3330'), (5, 'CLOSED c3328'), (7, 'CLOSED c3327'),
                    (13, 'CLOSED c3329'), (21, 'CLOSED c3326')):
        assert tag in lines[ln - 1], f"kept report {tag} moved off L{ln}"
    assert lines[C3162_LINE - 1].startswith('- [ ] **NEW c3162'), "NEW c3162 drifted"
    assert lines[TRACKER_HEAD - 1].startswith('- [x] **PARTIALLY DONE -- 298'), \
        "tracker head drifted"
    assert 'Running score:' in lines[TRACKER_SCORE - 1], "score line drifted"
    assert 'Per-batch results, one line each' in lines[TRACKER_BATCH - 1], \
        "per-batch line drifted"
    assert 'STANDING c3280' in lines[C3280_LINE - 1], "STANDING c3280 drifted"

    # --- in-place edits ---------------------------------------------------
    c3162 = lines[C3162_LINE - 1]
    assert C3162_POINTER_OLD in c3162, "c3162 resume pointer drifted"
    idx = c3162.find(C3162_TAIL_START)
    assert idx > 0, "c3162 batch-paragraph tail not found"
    c3162_tail = c3162[idx:]
    c3162 = c3162[:idx].replace(C3162_POINTER_OLD, C3162_POINTER_NEW, 1) + C3162_TAIL_NEW

    head = lines[TRACKER_HEAD - 1]
    assert HEAD_OLD in head, "tracker head text drifted"
    head = head.replace(HEAD_OLD, HEAD_NEW, 1)

    score = lines[TRACKER_SCORE - 1]
    assert SCORE_OLD in score, "score text drifted"
    score = score.replace(SCORE_OLD, SCORE_NEW, 1)

    batch = lines[TRACKER_BATCH - 1]
    marker = ("**Exact-handle grep has returned 0 hits fleet-wide for every handle "
              "in every batch since c3297")
    assert marker in batch, "per-batch closing sentence drifted"
    batch = batch.replace(marker, BATCH_APPEND.strip() + " " + marker, 1)

    c3280 = lines[C3280_LINE - 1]
    assert C3280_OLD in c3280, "c3280 next-trim sentence drifted"
    c3280 = c3280.replace(C3280_OLD, C3280_NEW, 1)

    # --- build the kept file ----------------------------------------------
    cut_set = set()
    for a, b in CUTS:
        cut_set |= set(range(a, b + 1))
    rewritten = {C3162_LINE, TRACKER_HEAD, TRACKER_SCORE, TRACKER_BATCH, C3280_LINE}
    repl = {C3162_LINE: c3162, TRACKER_HEAD: head, TRACKER_SCORE: score,
            TRACKER_BATCH: batch, C3280_LINE: c3280}

    kept = [REPORT.rstrip('\n'), '']
    for i, l in enumerate(lines, start=1):
        if i in cut_set:
            continue
        kept.append(repl.get(i, l))
    collapsed = []
    for l in kept:
        if l == '' and collapsed and collapsed[-1] == '':
            continue
        collapsed.append(l)
    new_queue_text = '\n'.join(collapsed)

    archived_blocks = ['\n'.join(lines[a - 1:b]).rstrip('\n').rstrip('-').rstrip()
                       for a, b in CUTS]
    # keep the separators verbatim instead of stripping them: rebuild raw
    archived_blocks = ['\n'.join(lines[a - 1:b]).rstrip('\n') for a, b in CUTS]

    header = (
        f"\n## Archived by cycle {CYCLE} (from tasks/queue.md, TRIM DUE at "
        "195.3KB/1062ln with **~1 cycle of headroom** -- below `STANDING "
        "c3280`'s own ~3-cycle trigger and inside the **c3331-c3334** window "
        "that item predicted, so this trim is on cadence rather than a reaction "
        "to the banner. Two things archived here, in the order the fresh "
        "per-block census ranked them. (1) THE BULK: the **8 oldest of 13** "
        "live per-cycle report blocks -- c3325, c3324, c3323, c3322, c3321, "
        "c3320, c3319, c3311, ~30.9KB -- keeping the newest 5 (c3330, c3329, "
        "c3328, c3327, c3326) at the documented floor, which c3332's own "
        "prepended block makes 6. The three live fold-in notes interleaved "
        "between them (`NEW c3321`, `NEW c3319`, `NEW c3311`, all still-open "
        "competitor-audit debts against `remote-jobs-scraper` / "
        "`ats-jobs-scraper`) were KEPT, and the script asserts that by name. "
        "(2) THE PREDICTED ONE: `NEW c3162`'s tail had regrown into two FULL "
        "batch paragraphs (c3330 rows 299-304 and c3331 rows 305-310, 3,396B) "
        "-- which is precisely what that tracker's own RULE forbids (\"append "
        "AT MOST ONE LINE per future batch\", tightened at c3320 'because it "
        "keeps being broken'). Archived verbatim below; the live item now "
        "carries a pointer, and the one-line forms of the c3327, c3330, c3331 "
        "and c3332 batches were written into the tracker's `Per-batch results, "
        "one line each` line where the rule says they belong. c3324 predicted "
        "this regrowth at ~1.5KB/batch and the measurement held exactly, so the "
        "re-compression budget of ~every 5 batches is now evidence-backed "
        "twice. Hazard-grepped first, 3 passes: (a) `grep -rn \"see "
        "tasks/queue.md\\|tasks/queue.md, cycle\" bin actors site notes state` "
        "-> only the standing false positives every prior trim has found "
        "(bin/store-rank, bin/git-maintain, dead `_trimNNNNq.py` docstrings, "
        "notes/STANDING.md's own rule text, LEARNINGS/STATUS narrative, "
        "state/*.json notes); (b) by-name sweep for c3311/c3319/c3320/c3321/"
        "c3322/c3323/c3324/c3325 across bin actors site notes state -> hits "
        "only in separate documents that each keep their own record "
        "(notes/LEARNINGS.md, state/STATUS.md, state/STATUS_ARCHIVE.md, "
        "state/*.json narrative) -- no \"see queue.md item cXXXX\" pointer "
        "anywhere; (c) INTRA-FILE over every KEPT line -> the only live "
        "citations of a cut cycle number are parenthetical precedent references "
        "like \"(c3320)\"/\"consolidated at c3320\", which are narrative and "
        "stay, plus `STANDING c3280`'s own next-candidate list, which this "
        "cycle re-sized in place. No dangling \"above\"/\"below\"/\"at the top "
        "of this file\" pointer was created or found. Newest-first, verbatim.) "
        "##\n\n"
        + '\n\n'.join(archived_blocks) + '\n\n'
        + "### `NEW c3162` batch-paragraph tail, cut from L104 by cycle 3332 "
          "(verbatim; replaced in the live item by a pointer, and by one-line "
          "entries in the tracker's per-batch line)\n\n"
        + c3162_tail + '\n'
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

    # every cut block must be present verbatim in the archive
    for a, b in CUTS:
        assert '\n'.join(lines[a - 1:b]).rstrip('\n') in header, \
            f"cut ({a},{b}) not archived verbatim"
    assert c3162_tail in header, "c3162 tail not archived verbatim"

    # the 5 rewritten lines: assert each edit stuck and nothing was lost
    assert C3162_POINTER_NEW in new_queue_text, "resume pointer not updated"
    # NB: the bare phrase "rows 311-316 (indices 310-315)" legitimately recurs in
    # this cycle's own report block, so assert on the POINTER text, not the rows.
    assert C3162_POINTER_OLD not in new_queue_text, "stale resume pointer survived"
    assert C3162_TAIL_START not in new_queue_text, "c3162 batch paragraphs survived"
    assert HEAD_NEW in new_queue_text and HEAD_OLD not in new_queue_text, \
        "tracker head not updated"
    assert SCORE_NEW in new_queue_text and SCORE_OLD not in new_queue_text, \
        "score line not updated"
    assert 'c3332 rows 311-316: 0/6' in new_queue_text, "batch one-liner missing"
    assert C3280_NEW in new_queue_text, "c3280 trim record missing"
    assert 'Re-trim around **c3331-c3334**' not in new_queue_text, \
        "stale c3280 window survived"
    # the kept report blocks and live interleaved items
    for tag in ('CLOSED c3332', 'CLOSED c3330', 'CLOSED c3329', 'CLOSED c3328',
                'CLOSED c3327', 'CLOSED c3326', 'NEW c3321', 'NEW c3319',
                'NEW c3311'):
        assert tag in new_queue_text, f"lost {tag} from the live file"
    for tag in ('CLOSED c3325', 'CLOSED c3324', 'CLOSED c3323', 'CLOSED c3322',
                'CLOSED c3321', 'CLOSED c3320', 'CLOSED c3319', 'CLOSED c3311'):
        assert tag in header, f"{tag} not in the archive header"

    print(f"orig queue.md: {len(orig.encode('utf-8'))} bytes, {len(lines)} lines")
    print(f"new  queue.md: {len(new_queue_text.encode('utf-8'))} bytes, "
          f"{len(collapsed)} lines")
    print(f"  report blocks archived: 8 of 13 "
          f"({sum(len(b.encode('utf-8')) for b in archived_blocks)} bytes)")
    print(f"  c3162 tail archived: {len(c3162_tail.encode('utf-8'))} bytes")
    print(f"  this cycle's own report block added: {len(REPORT.encode('utf-8'))} bytes")
    print(f"archive append: {len(header.encode('utf-8'))} bytes")
    print("multiset check: OK, 0 missing lines; 8 blocks + 1 tail archived "
          "verbatim; 5 in-place edits verified")

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
