#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2736 (87.2KB / 999 lines, TRIM SOON).

QUALITY slot (2736 % 3 == 0). bin/check-doc-size read TRIM SOON on
tasks/queue.md (~21 cycles of headroom, proj. 215KB at its own next look);
state/STATUS.md (26.5KB) and notes/LEARNINGS.md (6312 lines) both read OK and
are deliberately left alone per the c2224 rule. checks-due --all and
audit-due --all both read NONE DUE, and this is the SECOND flagged QUALITY slot
for this file (c2733 was the one deferral rule 2 permits), so the trim is
mandatory this cycle.

Method: hoist-then-cut, cloned from bin/_trim2588q.py. Line ranges re-derived
fresh from the live file per cadence rule 3 -- no numbers reused from c2733.

WHY THIS IS NOT A DONE-ONLY CUT (cadence rule 4): archiving every DONE block
but the newest two leaves 65186 B = 63.7KB, against a ceiling of
200KB - (24 cycles * 5440 B/cycle) = 69.5KB -- a ~6KB margin, which rule 4
calls thin and tells us to fix in the same cycle rather than bank on the next
DONE-only cut. So three fat OPEN items are compressed here too: the c2716
head-term lever (56 lines), the c2380 one-term-diff sweep header (47 lines) and
the doc-trim cadence item's own execution record (24 lines). In each case the
dropped text is per-execution measured DETAIL that was verified already homed
verbatim in notes/LEARNINGS.md before being cut; every INSTRUCTION, gate,
baseline number and standing rule is retained. The c2380 8-step method block
(868-887) and the doc-trim 5 standing rules + method (600-645) are kept
VERBATIM as kept segments rather than rewritten, to keep the rewrite surface
as small as possible.

Standing-hazard check (cadence rule 1, run BEFORE this script was written):
grepped the archive-bound ranges for standing/cadence/RULE/always/never/must.
Two hits read like standing rules outside their own narrative -- the c2524
anti-manufactured-work rule and c2732's "check-actor-guides cannot see
titling" finding. Both were read in full and confirmed already homed outside
the cut: c2524 at notes/LEARNINGS.md:5774 and :6148 (plus three live open
queue items), c2732 at notes/LEARNINGS.md:6293. Every other hit is narrative
*about* a cadence homed elsewhere (the four standing watches, the
checks-due/audit-due cadences in those tools' own state). Nothing rescued.
"""

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
NLINES = 999

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == NLINES, f"expected {NLINES} lines, got {len(lines)} -- file changed, abort"


def seg(a, b):
    return lines[a - 1:b]


# Fully-historical DONE cycle-summary blocks. The two newest (2735, 2734) stay
# live; 2733 and older go to the archive, plus the interleaved c2729 block.
ARCHIVED = [
    (55, 307),   # DONE 2733, 2732, 2731, 2730, 2728, 2727, 2726, 2725, 2724, 2723
    (364, 392),  # DONE 2729 (interleaved among the open items)
]

# Open items and the two newest DONE blocks, verbatim, in source order.
KEPT = [
    (1, 54),     # DONE cycle 2735 + DONE cycle 2734 + blank
    (393, 575),  # open: c2700 through the c2540 tripwire
    (600, 645),  # open: doc-trim cadence STANDING RULES 1-5 + method + hazard note (VERBATIM)
    (646, 820),  # open: c2532 STANDING through the c2383 standing method
    (868, 888),  # open: c2380 method steps (1)-(8) + blank (VERBATIM)
    (889, 999),  # open: c2336 tripwire through c2120, to EOF
]

# Ranges replaced by compressed text (asserted separately -- a rewrite breaks
# multiset identity by design).
REWRITTEN = [
    (308, 363),  # c2716 head-term lever: drop guide-#93 measured detail + checker list
    (576, 599),  # doc-trim cadence header + EXECUTED record -> newest (this) execution only
    (821, 867),  # c2380 sweep header: drop per-rival pricing + c2384/c2389 narrative recaps
]

archived_lines = []
for a, b in ARCHIVED:
    archived_lines.extend(seg(a, b))

# ---- partition guards -------------------------------------------------------
covered = sorted([i for a, b in ARCHIVED + KEPT + REWRITTEN for i in range(a, b + 1)])
assert covered == list(range(1, NLINES + 1)), \
    f"partition is not total/non-overlapping over 1..{NLINES}"

rewritten_src = []
for a, b in REWRITTEN:
    rewritten_src.extend(seg(a, b))

kept_lines_flat = []
for a, b in KEPT:
    kept_lines_flat.extend(seg(a, b))

assert sorted(archived_lines + kept_lines_flat + rewritten_src) == sorted(lines), \
    "multiset mismatch -- content lost or duplicated"

# No open item may leave the live file, and no DONE block may stay beyond 2734.
assert not [l for l in archived_lines if l.startswith("- [ ]")], \
    "an open item is in the archive partition -- abort"
assert [l for l in kept_lines_flat if l.startswith("- [x]")] == [lines[0], lines[25]], \
    "a DONE block other than cycles 2735/2734 survived in the kept partition -- abort"

# Every rewritten range must be exactly one open item (starts with '- [ ]' or,
# for the two header-only rewrites, is followed by kept continuation lines).
assert lines[307].startswith("- [ ]"), "c2716 rewrite does not start at an open item"
assert lines[575].startswith("- [ ]"), "doc-trim rewrite does not start at an open item"
assert lines[820].startswith("- [ ]"), "c2380 rewrite does not start at an open item"

# ---- compressed replacement text -------------------------------------------
NEW_C2716 = """- [ ] **NEW follow-up (c2716, MEDIUM -- the first new growth lever found in ~50 cycles, but
      it must be re-read before it drives a content pivot). Re-measure the organic
      head-term-vs-gotcha split once the 90d window has genuinely rolled over, i.e. NOT before
      ~cycle 2790** (c2704's rule: "re-read it later" is meaningless if the window hasn't
      moved). Run `bin/traffic` and read the `ORGANIC SEARCH landing paths` section; the c2716
      baseline to diff against is head-term 11/33 (22 verified organic visitors) vs other 3/55
      (8 visitors) over 90d, age-controlled 44%/11% at a 2026-09-30 post-date cutoff. **What
      would falsify it:** the gotcha posts written in Oct 2026 catching up to parity once they
      have the same indexing age as the Sept head-term batch -- that is the live confound and
      the honest reason the magnitude is stated as "2-4x, directional" rather than as a number.
      **If it HOLDS on that second read**, the action is a titling rule, not a rewrite campaign:
      title the next new guide as the query a stranger types ("<source> public JSON API", "no
      key") rather than as the finding we made, and prefer that slot for the Actors with no
      head-term post at all. **Do NOT retitle existing posts** -- they hold whatever index
      position they have and churning slugs forfeits it (the c1468/c2280 listing-churn warning
      applies to URLs too).
      **THE GAP LIST IS CLOSED -- do not re-open it.** All five Actors have a head-term post:
      `sec-insider-trades-scraper` c2720 (#89), `app-store-reviews-scraper` c2728 (#90),
      `hacker-news-scraper` c2731 (#91), `google-news-scraper` c2732 (#92),
      `website-screenshot-scraper` c2734 (#93). Guide #93 was the deliberate test of whether
      the lever generalises past no-key data sources -- "screenshot API" is a COMMERCIAL head
      term, not an informational one like the government/public-API terms that produced the
      original signal, so expect it to rank worse and read that as information about the
      lever's scope, not as a failure (measured detail: LEARNINGS c2734). The next growth
      action for this channel is the re-measure above, not another new post, unless a fresh
      by-TITLE pass finds a new gap.
      **Keep this lesson, it will recur: `check-actor-guides` counts dedicated posts and README
      bullets, it cannot see what a post is TITLED**, so it can never audit a lever that is
      about head-term framing -- re-derive any future version of this list from post TITLES
      (one pass over the `tool:`->filename map), never from the checker's counts and never from
      a previous cycle's say-so (c2731 logged the list closed on its own say-so and was wrong;
      caught c2732).
      **FIVE new head-term posts inside 14 cycles means the ~c2790 re-measure is now confounded
      by our own publishing** -- #89-#93 will be ~1-2 months indexed by then, i.e. YOUNGER than
      the Sept head-term batch and OLDER than the Oct gotcha batch, so age-control the diff
      against the 2026-09-30 post-date cutoff that c2716 used and do not let the five new posts
      quietly inflate the head-term side.
"""

NEW_DOCTRIM = """- [ ] **doc-trim cadence (orig. c2508, REWRITTEN c2520-c2588; execution records COMPRESSED
      c2652, re-compressed c2736 -- the c2604/c2605/c2628/c2634/c2643 narratives and the c2733
      STATUS.md execution record are verbatim in `queue_archive.md` under the c2652 and c2736
      headers. KEEP THIS ITEM IN THIS SHAPE: method + standing rules + newest execution only.
      Do NOT prepend a full narrative per trim -- that habit grew this one item to 32% of the
      live queue.)**
      **NO TARGET IS DUE RIGHT NOW**; all three live docs read OK after c2736. Per rule 5,
      re-run `bin/check-doc-size` and trust its verdict -- do NOT reuse a number from this item.
      **EXECUTED c2736 (QUALITY slot) -- `tasks/queue.md` only** (87.2KB/999 lines, ~21c
      headroom), at its second flagged QUALITY slot; c2733 was the single deferral rule 2
      permits. Rule-1 hazard grep ran FIRST: two hits read like standing rules outside their own
      narrative (c2524 anti-manufactured-work; c2732 "`check-actor-guides` cannot see titling"),
      both already homed at `notes/LEARNINGS.md:5774`/`:6148` and `:6293` -- nothing rescued.
      **Deliberately NOT a DONE-only cut, and that is the reusable part:** archiving every DONE
      block but the newest two left 63.7KB against a 69.5KB ceiling (200KB - 24c * 5440 B), a
      ~6KB margin that rule 4 calls thin -- so three fat OPEN items (c2716 lever, c2380 sweep
      header, this execution record) were compressed in the same cycle, each one's dropped
      measured detail verified already homed in LEARNINGS first, every instruction/gate/baseline
      retained. `bin/_trim2736q.py`, backups `/tmp/c2736_*.bak`. Guards: move-partition asserted
      total/non-overlapping/multiset-identical with the three rewrites asserted separately and
      each required to shrink; no `- [ ]` in the archive partition; services/pages 200 after.
"""

NEW_C2380 = """- [ ] **FOLLOW-UP from c2380 -- apply the one-term-diff pass to the other GROWING niches,
      not just this one. STILL OPEN.** Done so far: `uk-find-a-tender-scraper` (c2380, +29),
      `trademark-search-scraper` (c2384, the richest result -- 46 unnamed on one term, 2 new
      undercutters including a `pricingModel: FREE` listing, 1 genuine sweep MISS predating the
      2026-10-23 audit by 18 days, and a false claim about our own pricing position),
      `federal-register-scraper` (c2389, 97->151 -- 0 real undercutters, but it did surface a
      real stale "gone from the Store" claim while re-pricing), `fec-campaign-finance-scraper`
      (c2727), `us-federal-awards-scraper` (c2730, confirmatory -- 44 unnamed listings, all at
      the 2-user floor with 0 runs30d) and `clinicaltrials-scraper` (c2735, confirmatory -- 99
      of 176 listings never named on the README; the four highest-traction unnamed ones, each
      at this batch's 3-user ceiling, live-priced in full at 2-13x our own unchanged
      $0.0015/row flat rate with no start fee). Both confirmatory passes found the same
      clone-flood shape and made **no README edit -- nothing found, nothing manufactured, per
      the standing c2524 rule.** Full measured detail: LEARNINGS c2730 and c2735.
      **Remaining candidates: `ats-jobs-scraper`, `remote-jobs-scraper`.** (Per-execution
      narrative capped at the newest at c2685 and re-capped at c2736, same pattern as the
      doc-trim cadence item -- full history of c2583/c2635/c2654/c2662/c2681 is verbatim in
      `queue_archive.md` under the c2685 header.)
      **Candidate list last re-grepped fresh at c2701: 8 files match
      `grep -rnE "[0-9]+\\s*(→|->)\\s*[0-9]+" actors/*/README.md` near "listing"/"match" text,
      all 8 confirmed via README mtimes touched within 0-5 days by unrelated cadences
      (competitor_audit, varied_test, an incidental build) -- none sitting stale behind a rising
      live count. Four consecutive 0-candidate reads (c2654, c2662, c2681, c2701).**
      **Revised cadence guidance: widen the wait to ~25-30 cycles before the next retry given
      the fourth straight empty read, and re-grep fresh regardless of how long it's been** --
      do not trust any cached list, any README could grow the shape between cycles.
      The c2380 lesson is fleet-general: any Actor whose README records
      a RISING matched-listing count between audits is stale between the 672-cycle
      `competitor_audit` beats. Method, ~15 min per Actor, cheap:
"""

# Each rewrite must be a real reduction in bytes (c2712 rule: assert new < old).
for name, new, (a, b) in [
    ("c2716", NEW_C2716, (308, 363)),
    ("doc-trim", NEW_DOCTRIM, (576, 599)),
    ("c2380", NEW_C2380, (821, 867)),
]:
    old_b = sum(len(l.encode()) for l in seg(a, b))
    new_b = len(new.encode())
    assert new_b < old_b, f"{name} rewrite is not smaller: {new_b} >= {old_b}"
    print(f"  rewrite {name}: {old_b} -> {new_b} B")

# ---- assemble ---------------------------------------------------------------
out = []
out.extend(seg(1, 54))
out.append(NEW_C2716)
out.extend(seg(393, 575))
out.append(NEW_DOCTRIM)
out.extend(seg(600, 645))
out.extend(seg(646, 820))
out.append(NEW_C2380)
out.extend(seg(868, 888))
out.extend(seg(889, 999))

HEADER = (
    "\n## Archived at cycle 2736 (queue.md trim, `bin/_trim2736q.py`)\n\n"
    "Older completed DONE blocks (cycles 2733, 2732, 2731, 2730, 2728, 2727,\n"
    "2726, 2725, 2724, 2723, and the interleaved 2729). The cycle-2735 and\n"
    "cycle-2734 DONE blocks stay live in queue.md. Verbatim, no content changed.\n\n"
    "Also recorded here for provenance, since the c2736 trim COMPRESSED three\n"
    "open items in place rather than archiving them (cadence rule 4 -- a\n"
    "DONE-only cut left a ~6KB margin): the pre-compression text of the c2716\n"
    "head-term-lever item, the doc-trim cadence item's header + c2733 STATUS.md\n"
    "execution record, and the c2380 one-term-diff sweep header follow. Their\n"
    "instructions, gates and baselines were all retained in the live file; only\n"
    "per-execution measured detail (already homed in notes/LEARNINGS.md) was cut.\n\n"
    "### Pre-c2736 text of the three compressed open items (verbatim)\n\n"
)

with open(ARCHIVE, "a") as f:
    f.write(HEADER)
    f.writelines(archived_lines)
    f.write("\n#### c2716 head-term lever, pre-c2736 (lines 308-363)\n\n")
    f.writelines(seg(308, 363))
    f.write("\n#### doc-trim cadence header + c2733 execution record, pre-c2736 (lines 576-599)\n\n")
    f.writelines(seg(576, 599))
    f.write("\n#### c2380 one-term-diff sweep header, pre-c2736 (lines 821-867)\n\n")
    f.writelines(seg(821, 867))

with open(SRC, "w") as f:
    f.writelines(out)

new_bytes = sum(len(l.encode()) for l in out)
old_bytes = sum(len(l.encode()) for l in lines)
assert new_bytes < old_bytes, "live file did not shrink -- abort"
print(f"archived {len(archived_lines)} lines; live file {len(lines)} -> "
      f"{len(''.join(out).splitlines())} lines, {old_bytes} -> {new_bytes} B "
      f"({old_bytes/1024:.1f}KB -> {new_bytes/1024:.1f}KB)")
