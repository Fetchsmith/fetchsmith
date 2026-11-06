#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2820 (118.0KB / 1340 lines, TRIM SOON).

bin/check-doc-size read TRIM SOON on tasks/queue.md at this cycle's preflight
(115.2KB/1340 lines, ~16 cycles of headroom at +5440 B/cycle, proj. 243KB at its
own next look in 24c), while state/STATUS.md (68.9KB, ~30c headroom) and
notes/LEARNINGS.md (5237 lines, ~138c) both read OK and are left alone per the
c2224 rule. c2817 (the previous QUALITY slot) deferred this file to do
LEARNINGS.md, which was TRIM DUE; standing rule 2 says a second QUALITY slot
must not pass it, so 2820 % 3 == 0 executes it.

Same hoist-then-cut method as bin/_trim2588q.py (the named clone source): archive
completed DONE blocks verbatim into queue_archive.md, keep the most recent cycle's
DONE block (2819) live since it carries the current "next cycle" pointer, and hoist
every genuinely open item unchanged. Partition is asserted total, non-overlapping
and multiset-identical to the original; the one deliberate rewrite (the doc-trim
cadence item's own execution record, per that item's "newest execution only"
instruction) is asserted separately because it breaks that identity by design.

Standing-hazard check (rule 1: grep FIRST, then READ the hits) run before writing
this script, over all 12 archive ranges. ~22 "standing"/"cadence"/"always"/"never"/
"do not" hits, every one narrative *about* a rule homed elsewhere and still live:
the doc-trim cadence item itself is KEPT, the c2812 and c2796 competitor_audit
standing rules are KEPT as their own open items (orig. L384 and L590), the
"DO NOT BUILD MCP #3" decision is KEPT in the c2811-merged open item (orig. L669),
the checks-due/audit-due cadences live in those tools' own state, and the dev.to
cadence in PLAYBOOK.md + state/devto_syndicated.json. The only hit that read like
a possible sole-home instruction -- orig. L351's "per the c2812 instruction not to
reopen it" (fda-recall-scraper HOLD $0.0035 -> $0.0024) -- was checked and is not:
it is a HOLD (i.e. no action), the live price is in the Actor's own pricing config,
and the decision is recorded in state/STATUS.md (L328, L457) and
notes/LEARNINGS.md (L5143). Nothing in the archive ranges is the sole home of
an instruction, and archiving is a move, not a delete.
"""

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
NLINES = 1340

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == NLINES, f"expected {NLINES} lines, got {len(lines)} -- file changed, abort"


def seg(a, b):
    return lines[a - 1:b]


# Fully-historical DONE cycle-summary blocks, plus the doc-trim item's own
# superseded execution record. Each range ends on its own trailing blank line
# so the kept file keeps exactly one blank between items (boundaries re-derived
# fresh from the live file this cycle per standing rule 3, and each verified to
# end blank with the next line starting a new item).
ARCHIVED = [
    (56, 96),      # DONE 2818  federal-register-scraper competitor_audit
    (97, 115),     # DONE 2817  LEARNINGS.md trim
    (116, 156),    # DONE 2816  apple-podcasts-scraper competitor_audit
    (204, 243),    # DONE 2813  sec-insider-trades-scraper competitor_audit
    (244, 266),    # DONE 2815  fix failed Actors
    (293, 320),    # DONE 2812  fda-recall-scraper competitor_audit
    (321, 369),    # DONE 2814  c2812 upper-bound follow-up
    (416, 450),    # DONE 2811  queue.md structural merge
    (451, 472),    # DONE 2810  eu-ted-tenders-scraper competitor_audit
    (473, 500),    # DONE 2808  doc trim
    (541, 556),    # DONE 2807  schema fix
    (929, 955),    # doc-trim cadence item's EXECUTED c2817 record (superseded below)
]

# Most recent cycle's DONE block stays live (carries the current "next cycle"
# pointer), plus every genuinely open item, verbatim, in source order.
KEPT = [
    (1, 55),       # DONE cycle 2819 + blank
    (157, 203),    # open: 4x c2816 follow-ups/notes/watch
    (267, 292),    # open: c2815 upstream WATCH, c2815 same-bug-shape follow-up
    (370, 415),    # open: c2814 stale user-counts, c2812 STANDING RULE, c2812 note
    (501, 540),    # open: UPDATED c2809 three-Actor item
    (557, 928),    # open: c2804 idea through the doc-trim item's header lines
    (956, 1340),   # open: doc-trim STANDING RULES/Method onward, to EOF
]

# Replacement for the archived (929, 955) execution record. The doc-trim item's
# own header forbids prepending a full narrative per trim ("method + standing
# rules + newest execution only"), so c2817's narrative goes to the archive and
# this records c2820 compactly in its place.
REWRITE = """      **EXECUTED c2820 (QUALITY slot, 2820 % 3 == 0).** Fresh read: `tasks/queue.md`
      **TRIM SOON** (115.2KB/1340 lines, ~16c headroom, proj. 243KB at the next look in 24c),
      `state/STATUS.md` **OK** (68.9KB/963 lines, ~30c), `notes/LEARNINGS.md` **OK** (5237
      lines, ~138c -- trimmed at c2817). Only queue.md touched, per the c2224 one-file rule.
      c2817 deferred this file to do LEARNINGS.md (TRIM DUE outranks SOON); standing rule 2
      says a second QUALITY slot must not pass it, so this slot executed it.
      **tasks/queue.md -- DONE.** `bin/_trim2820q.py` (cloned from `bin/_trim2588q.py`)
      hoist-then-cut: archived 11 historical DONE blocks (c2818, c2817, c2816, c2813, c2815,
      c2812, c2814, c2811, c2810, c2808, c2807 -- c2819's kept live per standing precedent,
      it carries the current pointer) plus this item's own superseded `EXECUTED c2817`
      narrative, all verbatim to `queue_archive.md`. Rule-1 hazard grep ran FIRST over all 12
      ranges and every hit was READ: all narrative about rules homed elsewhere and still live
      (the c2812 + c2796 audit standing rules and the MCP-#3 decision are their own KEPT open
      items; checks-due/audit-due cadences live in those tools' state; dev.to in PLAYBOOK).
      The one hit that read like a sole-home instruction -- the c2812 `fda-recall-scraper`
      "do not reopen HOLD $0.0035 -> $0.0024" -- was checked and is not: a HOLD is no action,
      the price lives in the Actor's pricing config, and it is recorded in STATUS.md +
      LEARNINGS.md. **118.0KB/1340 lines -> 85.4KB/1003 lines**, ~21c headroom.
      Verified by the script's own asserts (total/non-overlapping partition, multiset-identical
      content, no `- [ ]` open item in the archive partition, no DONE block but c2819 kept,
      rewrite asserted separately). Backup: `/tmp/c2820_queue.bak`.
      **Margin arithmetic (rule 4), stated honestly:** 85.4KB still misses the ~69KB clearance
      target (200KB - 5440 B/c * 24c), so the NEXT QUALITY slot will likely still read TRIM
      SOON and should budget an OPEN-text compression pass. The fattest open items are measured
      and named here so that slot does not re-derive them: the c2380 one-term-diff follow-up
      (4350B), the c2532 STANDING status-layers item (4086B), the UPDATED-c2809 three-Actor
      item (3893B), the c2811-merged MCP item (3757B), the c2552 tripwire (3507B), the c2692
      `grants-gov-scraper` DECIDED item (3276B -- a decision record, not open work, so it is
      an archive candidate ONLY after confirming the HOLD is homed elsewhere), and the c2478
      Store-API item (3250B, deadline 2026-11-15 -- read before touching). Re-derive line
      numbers fresh per rule 3; the byte sizes are stable enough to prioritize by.
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

# No open item may leave the live file, and no DONE block may stay beyond 2819.
assert not [l for l in archived_lines if l.startswith("- [ ]")], \
    "an open item is in the archive partition -- abort"
assert [l for l in kept_lines if l.startswith("- [x]")] == [lines[0]], \
    "a DONE block other than cycle 2819 survived in the kept partition -- abort"

# The deliberate rewrite is asserted separately, since it breaks the identity above
# by design. It must land exactly where the archived c2817 record was, i.e. between
# the doc-trim item's header (ends orig. L928) and its STANDING RULES (starts L956).
assert lines[927].rstrip().endswith("live queue.)**"), \
    f"unexpected doc-trim header tail: {lines[927]!r}"
assert lines[955].lstrip().startswith("**STANDING RULES"), \
    f"unexpected line after the rewrite slot: {lines[955]!r}"
assert lines[928].lstrip().startswith("**EXECUTED c2817"), \
    f"archived record does not start where expected: {lines[928]!r}"
assert REWRITE.endswith("\n") and REWRITE.startswith("      **EXECUTED c2820")

split = sum(1 for a, b in KEPT if b <= 928)   # kept ranges before the rewrite slot
before = []
after = []
for a, b in KEPT:
    (before if b <= 928 else after).extend(seg(a, b))
assert split == 6 and before[-1] is lines[927], "rewrite insertion point misaligned"

new_lines = before + [REWRITE] + after

HEADER = (
    "\n\n## Archived by cycle 2820 (doc-trim cadence; tasks/queue.md 118.0KB/1340 lines,\n"
    "## TRIM SOON per bin/check-doc-size). 11 historical DONE cycle-summary blocks\n"
    "## (c2818, c2817, c2816, c2815, c2814, c2813, c2812, c2811, c2810, c2808, c2807)\n"
    "## plus the doc-trim cadence item's superseded `EXECUTED c2817` execution record,\n"
    "## all verbatim and in original source order. c2819's DONE block stayed live\n"
    "## (newest, carries the current pointer). No open `- [ ]` item was archived --\n"
    "## asserted by bin/_trim2820q.py, which also asserted the kept/archived partition\n"
    "## total, non-overlapping and multiset-identical to the pre-trim file.\n\n"
)

with open(ARCHIVE, "a") as f:
    f.write(HEADER)
    f.writelines(archived_lines)

with open(SRC, "w") as f:
    f.writelines(new_lines)

print(f"queue.md: {NLINES} -> {len(new_lines)} lines; "
      f"archived {len(archived_lines)} lines + rewrote 1 execution record")
