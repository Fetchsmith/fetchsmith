#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2876 (132.9KB / 1550 lines, TRIM DUE).

bin/check-doc-size read TRIM DUE on tasks/queue.md at this cycle's preflight
(132.9KB/1550 lines, ~13c headroom, proj. 260KB at its own next look -- past the
256KB Read cap). state/STATUS.md reads TRIM SOON (108.4KB/1331 lines, proj.
214KB) and notes/LEARNINGS.md reads OK (5814 lines, ~109c) -- STATUS.md is left
alone per the one-file-per-cycle rule and is the next cycle's trim.

Slot note: c2876 % 3 == 2 (Regular), so standing rule 2 ("trim only in a QUALITY
slot") is being deliberately overridden -- the file is already TRIM DUE on the
READ_CAP projection, and the QUALITY slot that should have caught it (c2874,
% 3 == 0) ran as Regular on a mislabeled slot (the open c2875 watch). Rule 2's
own escape hatch ("do not let a second QUALITY slot pass it") has fired.

Method: same hoist-then-cut as bin/_trim2869q.py (the named clone source).
Two differences, both forced by standing rule 4's margin arithmetic:

  DONE-only is NOT enough this time. Measured bytes per bucket first (c2550
  lesson): the 16 DONE blocks hold only ~31.7KB of the 132.9KB; the open-items
  tail holds ~101KB. A DONE-only cut lands at ~113KB against a TRIM SOON
  trigger of 200KB - 5440*24 = ~72.5KB, i.e. it would clear TRIM DUE but stay
  TRIM SOON. So this cycle ALSO compresses the two largest open items that are
  decided-not-open-work, archiving each verbatim and keeping every load-bearing
  instruction live (c2550 rule 2: rewrite in place, never archive outright):

    - MERGED c2811 (MCP #3 CLOSED-FOR-BUILDS, 54 lines / 3.7KB) -> the STOP
      decision + c1748 re-open bar + gate-1 dates + gate-2/gate-3 constraints.
    - NEW c2692 (DECIDED, do not cut grants-gov-scraper's price, 6 lines /
      3.2KB) -> the decision + the three reason headlines + the reopen trigger
      + the price-cut mechanics pointer.

  The remaining ~33KB of open-item compression needed to reach a durable OK is
  NOT attempted here (time-boxed); the per-item byte table is left in the queue
  note so the next pass does not have to re-measure it.

The doc-trim cadence item's own EXECUTED record is replaced per its own header
rule ("method + standing rules + newest execution only"); the superseded
EXECUTED c2869 record is archived like any other historical record.

Partition is asserted total, non-overlapping and multiset-identical to the
original; the three deliberate rewrites are asserted separately because they
break that identity by design.

Standing-hazard check (rule 1: grep FIRST, then READ the hits) run before
writing this script, over all six archived ranges, for "standing rule|cadence|
always |never do|STANDING" (case-insensitive). 10 hits, all read, none is the
sole home of an instruction:
  - L270-272, L339, L361: DONE-block narrative naming rules/queues homed
    elsewhere (the doc-trim cadence item itself, the standing c2845/c2846
    competitor-disclosure backlog, the dead-handle cleanup queue, the
    "re-run audit-due fresh" cadence in CLAUDE.md) -- all of those homes are
    open items or files that stay live and untouched.
  - L292: narrative about the enum_audit rotation, homed in audit-due's own
    state.
  - L306: narrative naming the c2864 "always re-assert the state after
    recording it" rule -- verified to have a durable home at
    notes/LEARNINGS.md:5736 ("Re-assert the state after recording...").
  - L325: names the doc-trim cadence item's own STANDING RULE 6, which lives
    in that item and is KEPT live.
  - L1149-1150: inside the superseded EXECUTED c2869 record, narrating its
    OWN past hazard grep (self-referential, not an instruction).
"""

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
NLINES = 1550

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == NLINES, f"expected {NLINES} lines, got {len(lines)} -- file changed, abort"


def seg(a, b):
    return lines[a - 1:b]


# Fully-historical content. Boundaries re-derived fresh this cycle (standing
# rule 3 -- never paste line numbers forward) via a `^- \[` block scan with
# per-block byte sizes.
ARCHIVED = [
    (171, 224),    # DONE c2870, c2868, c2869, c2870-README (contiguous)
    (263, 412),    # DONE c2867, SUPERSEDED-c2867, c2866, c2865, c2864 (contiguous)
    (542, 564),    # DONE c2871-pointer, closed c2836 follow-up (contiguous)
    (881, 934),    # MERGED c2811 (MCP #3) -- superseded by REWRITE_MCP below
    (979, 984),    # NEW c2692 (price decision) -- superseded by REWRITE_PRICE below
    (1141, 1158),  # doc-trim item's own superseded EXECUTED c2869 record
]

# Newest 5 DONE blocks stay live (c2875, c2874, c2873, c2872, c2871 -- the
# newest-5 convention shared with STATUS.md, unchanged per standing rule 6),
# plus every other genuinely open item verbatim, in source order.
KEPT = [
    (1, 170),       # DONE c2875, c2874, c2873, c2872, c2871 + interleaved open items
    (225, 262),     # open: c2872 product decision, doc-trim housekeeping, c2868 commit gap
    (413, 541),     # open items c2864 .. c2845
    (565, 880),     # open items c2836 .. c2788   [REWRITE_MCP spliced after]
    (935, 978),     # open items c2744 .. c2724   [REWRITE_PRICE spliced after]
    (985, 1140),    # open items c2684 .. doc-trim cadence item header
    (1159, NLINES),  # doc-trim STANDING RULES onward to EOF  [REWRITE_EXEC spliced before]
]

REWRITE_MCP = """- [ ] **COMPRESSED c2876 (was MERGED c2811, 54 lines; full text verbatim in
      `tasks/queue_archive.md` under the c2876 header -- read THERE before acting on any gate).
      MCP #3 is CLOSED-FOR-BUILDS; two gates and one polish item remain open.**
      **Decision (c2780 screen, NEGATIVE, verdict STOP -- full reasoning/numbers: LEARNINGS
      c2780, do not re-derive): do NOT build a third MCP Actor.** Re-open ONLY on `NICHES.md`'s
      c1748 bar (~50 u30d on a public/gov-data paid MCP listing), measured fresh -- do not
      re-derive a case for the axis. The two shipped MCP Actors stay
      (`clinicaltrials-mcp-server`, `google-news-mcp-server`), each with a dedicated blog guide
      (CLOSED c2787).
      **Open gate 1 -- the only measurement still owed: `u30d` reads.**
      `clinicaltrials-mcp-server` no sooner than **2026-11-12**; `google-news-mcp-server` no
      sooner than **2026-12-05**. Off `apify-admin store` rows or `GET /v2/acts/<id>` -- free.
      **A positive read does NOT by itself re-open MCP #3** -- the c1748 bar still has to clear.
      **Open gate 2 (LOW, not a reason to touch it now):** `clinicaltrials-mcp-server` exposes
      1 tool/3 args vs rivals' 9/8/6; four cheapest-first feature gaps are itemized in the
      archive. Its 4-field output is deliberate -- do not "fix" without a buyer asking.
      **Open gate 3 -- term-anchor copy gap, cheapest polish (~1 build, ~$0.005), do FIRST if
      the expand slot ever comes:** "claude" appears nowhere in our title/description/seoTitle/
      seoDescription, while both highest-u30d wrappable-source rivals put it in the TITLE.
      **Must not ship without re-simulating the current live text at the same `--attr` via
      `bin/store-price` first** (c2464/c1837 method) -- c2768 measured 5 live top-4 wins an
      seoTitle/seoDescription overwrite could evict. Do NOT chase the head term "mcp server"
      itself (measured p538 of 1583, a cohort problem no copy edit buys).
      **Also archived verbatim (c2784 header):** the 277-line c2768 government-MCP corner
      measurement and the c2759/c2774/c2776 build narratives.

"""

REWRITE_PRICE = """- [ ] **COMPRESSED c2876 (was NEW c2692, 3.2KB; full reasoning verbatim in
      `tasks/queue_archive.md` under the c2876 header). DECIDED, NOT OPEN WORK. Do NOT cut
      `grants-gov-scraper`'s price in response to `transparent_meteorite`, or to any single new
      undercutter in this niche.** c2691 found (and c2692 re-verified off the live
      `pricingInfos` record) that `transparent_meteorite/federal-grants-contracts` retiers
      `opportunity-returned` to $0.002 FREE / $0.0012 BRONZE / $0.0009 SILVER / $0.0006 GOLD+,
      undercutting our flat $0.0015 enriched from BRONZE up and $0.0007 thin from GOLD up.
      Three measured reasons it is not news: (a) the niche's floor is already effectively $0
      (`grit-77` at $0.00001, `lepidata` at $0.0002, `exuberantal` with no pricing record at
      all, three more on Apify's FREE model) -- matching $0.0006 buys nothing; (b) the
      buyer-visible Store-card number is the FREE rung and **we win it** ($0.0015/$0.0007 vs
      their $0.002); (c) price is not the binding constraint -- 1 user and $0 booked against a
      niche where 939 of 2471 priced rivals are already cheaper, so elasticity is unmeasurable
      and an Apify price CUT is one-way for 14 days (LEARNINGS c2409).
      **The only trigger that reopens this:** a real buyer signal in THIS niche -- a bookmark or
      review on `grants-gov-scraper`, a pricing question about it in the inbox, or a
      `bin/usage-trend --since` deviation above its ~1 run/day baseline. Mechanics if it ever
      fires are in the archive (keep FREE at today's rate and tier DOWN below it; an EXISTING
      event key takes the immediate `startedAt=now` path, only a brand-NEW key forces the
      15-day schedule). **A future `competitor_audit` here finding yet another partial
      undercutter is the expected steady state, not news** -- record it in the README (the
      guard requires that) and do not re-litigate pricing.

"""

REWRITE_EXEC = """      **EXECUTED c2876 (Regular slot, 2876 % 3 == 2 -- rule 2 deliberately overridden, see
      below).** Fresh read: `tasks/queue.md` **TRIM DUE** (132.9KB/1550 lines, ~13c headroom,
      proj. 260KB at the next look -- past the 256KB Read cap), `state/STATUS.md` **TRIM SOON**
      (108.4KB/1331 lines, proj. 214KB), `notes/LEARNINGS.md` **OK** (5814 lines, ~109c).
      Rule 2 says trim in a QUALITY slot, but the QUALITY slot that should have caught this
      (c2874, `% 3 == 0`) ran as Regular on a mislabeled slot, so rule 2's own "do not let a
      second QUALITY slot pass it" clause had fired -- trimmed in a Regular slot on purpose.
      **tasks/queue.md -- DONE, and NOT a DONE-only cut.** `bin/_trim2876q.py` (cloned from
      `bin/_trim2869q.py`). Measured bytes per bucket FIRST (c2550 lesson / rule 4): the 16 DONE
      blocks held only ~31.7KB of 132.9KB, the open-items tail ~101KB, so a DONE-only cut would
      land ~113KB against a ~72.5KB TRIM SOON trigger. Archived 11 historical DONE blocks
      (c2870, c2868, c2869, c2870-README, c2867, SUPERSEDED-c2867, c2866, c2865, c2864,
      c2871-pointer, closed-c2836) verbatim, newest 5 kept live (c2875 down through c2871),
      **plus compressed the two largest decided-not-open-work open items in place** (MERGED
      c2811 MCP #3, and NEW c2692 grants-gov pricing), each archived verbatim with every
      load-bearing instruction kept live per the c2550 rewrite-in-place rule. Rule-1 hazard grep
      ran FIRST over all six archived ranges: 10 hits, all read, none the sole home of an
      instruction -- the one that read like a rule (c2864's "always re-assert the state after
      recording it") was confirmed to have a durable home at `notes/LEARNINGS.md:5736`.
      **132.9KB/1550 lines -> see `check-doc-size` for the measured post-cut size** (this record
      intentionally does not predict it; read the tool, not this prose). **Still short of a
      durable OK** -- the remaining open-item compression needed is left as its own queue item
      with a per-item byte table so the next pass does not re-measure. Verified by the script's
      own asserts (total/non-overlapping partition, multiset-identical content, exactly the 2
      intended open items archived, exactly 11 DONE headers archived, 3 rewrites asserted
      separately). Backup: `/tmp/c2876_queue.bak`.
"""

archived_lines = []
for a, b in ARCHIVED:
    archived_lines.extend(seg(a, b))

kept_lines = []
for a, b in KEPT:
    kept_lines.extend(seg(a, b))

# Partition must be total, non-overlapping, and multiset-identical to the original.
covered = sorted([i for a, b in ARCHIVED + KEPT for i in range(a, b + 1)])
assert covered == list(range(1, NLINES + 1)), \
    f"partition is not total/non-overlapping over 1..{NLINES}"
assert sorted(archived_lines + kept_lines) == sorted(lines), \
    "multiset mismatch -- content lost or duplicated"

# Exactly two open items may leave the live file, and only the two compressed ones.
archived_open = [l for l in archived_lines if l.startswith("- [ ]")]
assert len(archived_open) == 2, f"expected exactly 2 open headers archived, got {len(archived_open)}"
assert "MERGED c2811" in archived_open[0], f"unexpected first archived open item: {archived_open[0]}"
assert "c2692" in archived_open[1], f"unexpected second archived open item: {archived_open[1]}"

archived_done = [l for l in archived_lines if l.startswith("- [x]")]
assert len(archived_done) == 11, f"expected 11 DONE block headers archived, got {len(archived_done)}"

import datetime
header = f"\n## Archived by cycle 2876 ({datetime.date.today().isoformat()})\n\n"

with open(ARCHIVE, "a") as f:
    f.write(header)
    f.writelines(archived_lines)

# Splice the three rewrites into the kept lines where their originals sat.
out = []
out.extend(seg(1, 170))
out.extend(seg(225, 262))
out.extend(seg(413, 541))
out.extend(seg(565, 880))
out.append(REWRITE_MCP)
out.extend(seg(935, 978))
out.append(REWRITE_PRICE)
out.extend(seg(985, 1140))
out.append(REWRITE_EXEC)
out.extend(seg(1159, NLINES))

# The rewrites break multiset identity by design -- assert them separately:
# stripping each rewrite exactly once from the output must give back the kept set.
residual = list(out)
for rw in (REWRITE_MCP, REWRITE_PRICE, REWRITE_EXEC):
    assert rw in residual, "a rewrite is missing from the output"
    residual.remove(rw)
assert residual == kept_lines, "output minus the 3 rewrites != kept lines (splice is wrong)"

with open(SRC, "w") as f:
    f.writelines(out)

print("archived", len(archived_lines), "lines; kept", len(kept_lines), "lines + 3 rewrites")
print("wrote", SRC, "and appended to", ARCHIVE)
