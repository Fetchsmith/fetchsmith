#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2841 (131.5KB / 1542 lines, TRIM DUE).

bin/check-doc-size read TRIM DUE on tasks/queue.md at this cycle's preflight
(131.5KB/1542 lines, ~13 cycles of headroom, proj. 259KB at its own next
look in 24c). state/STATUS.md reads OK (37.5KB, ~37c headroom) and
notes/LEARNINGS.md reads OK (5468 lines, ~127c) -- both left alone per the
c2224 one-file rule. c2841 is a QUALITY slot (2841 % 3 == 0) and was named
explicitly by c2838/c2839/c2840 as the cycle that must not defer this a 4th
time (standing rule 2).

Same hoist-then-cut method as bin/_trim2829q.py (the named clone source):
archive completed DONE blocks verbatim into queue_archive.md, keep the
newest 5 DONE blocks live (matching state/STATUS.md's own keep-newest-5
convention), and hoist every genuinely open item unchanged. The doc-trim
cadence item's own internal EXECUTED record is replaced per its own header
rule ("method + standing rules + newest execution only" -- do not prepend a
full narrative per trim); its prior EXECUTED c2838 record is archived like
any other historical record.

Partition is asserted total, non-overlapping and multiset-identical to the
original; the one deliberate rewrite is asserted separately because it
breaks that identity by design.

Standing-hazard check (rule 1: grep FIRST, then READ the hits) run before
writing this script, over all 9 archive ranges for
"standing rule|cadence|always |never do|STANDING" (case-insensitive). 3
hits, all read: a reference to STATUS.md's own c2829 entry, and two
self-references inside the doc-trim cadence item's own text (which stays
KEPT, not archived) describing its own hazard-grep count and its own
instruction to c2841. Nothing in the archived ranges is the sole home of
an instruction.
"""

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
NLINES = 1542

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == NLINES, f"expected {NLINES} lines, got {len(lines)} -- file changed, abort"


def seg(a, b):
    return lines[a - 1:b]


# Fully-historical DONE cycle-summary blocks (older than the newest 5 kept
# live), plus the doc-trim cadence item's own superseded EXECUTED c2838
# record. Boundaries re-derived fresh from the live file this cycle via
# `grep -n "^- \\["` plus a blank-line-separator check (every range below
# ends on its own trailing blank line, confirmed programmatically).
ARCHIVED = [
    (231, 266),   # DONE 2835  trademark-search-scraper enum_audit
    (267, 311),   # DONE 2834  court-records-scraper hCaptcha/token wiring
    (312, 348),   # DONE 2833  court-records-scraper 8 GONE-line fixes
    (349, 390),   # DONE 2832  de-noised c2831 GONE report
    (391, 402),   # DONE 2829  queue.md trim (this item's own prior execution)
    (403, 461),   # DONE 2828  google-news-scraper 337c-overdue item
    (462, 507),   # DONE 2830  no_pricing_record fix
    (541, 622),   # DONE 2831  c2816 GONE fix
    (1135, 1157),  # doc-trim item's own superseded EXECUTED c2838 record
]

# Newest 5 DONE blocks stay live (2840-2836), plus every genuinely open
# item, verbatim, in source order.
KEPT = [
    (1, 230),      # DONE 2840, 2839, 2838, 2837, 2836 + c2836's 3 open follow-ups
    (508, 540),    # open: UPDATED c2828 + c2824 follow-up
    (623, 1134),   # open items 623-1128 + doc-trim item's own header (1129-1134)
    (1158, NLINES),  # doc-trim STANDING RULES onward, to EOF
]

REWRITE = """      **EXECUTED c2841 (QUALITY slot, 2841 % 3 == 0).** Fresh read: `tasks/queue.md`
      **TRIM DUE** (131.5KB/1542 lines, ~13c headroom, proj. 259KB at the next look in 24c),
      `state/STATUS.md` **OK** (37.5KB/489 lines, ~37c headroom), `notes/LEARNINGS.md` **OK**
      (5468 lines, ~127c). TRIM DUE outranks OK, so queue.md is the one touched this cycle --
      the 4th-deferral deadline c2838/c2839/c2840 each flagged for this slot.
      **tasks/queue.md -- DONE.** `bin/_trim2841q.py` (cloned from `bin/_trim2829q.py`)
      hoist-then-cut: archived 8 historical DONE blocks (c2835, c2834, c2833, c2832, c2829,
      c2828, c2830, c2831) plus this item's own superseded EXECUTED c2838 record, all verbatim
      to `queue_archive.md`, newest-5-kept-live matching STATUS.md's own convention (c2840
      down through c2836 stay). Rule-1 hazard grep ran FIRST over all 9 ranges (pattern
      `standing rule|cadence|always |never do|STANDING`, case-insensitive): 3 hits, all read --
      one is STATUS.md's own c2829 entry, two are the doc-trim item's self-references (which
      stays KEPT). Nothing archived was the sole home of an instruction.
      **131.5KB/1542 lines -> see `check-doc-size` for the measured post-cut size** (this record
      intentionally does not predict it; read the tool, not this prose).
      Verified by the script's own asserts (total/non-overlapping partition, multiset-identical
      content, no `- [ ]` open item in the archive partition, only the newest 5 DONE blocks
      survive live, rewrite asserted separately). Backup: `/tmp/c2841_queue.bak`.
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

# No open item may leave the live file.
assert not [l for l in archived_lines if l.startswith("- [ ]")], \
    "an open item is in the archive partition -- abort"
# Only the newest 5 DONE blocks (2840,2839,2838,2837,2836) may survive live.
kept_done_starts = [l for l in kept_lines if l.startswith("- [x]")]
assert kept_done_starts == [lines[0], lines[45], lines[68], lines[83], lines[135]], \
    "unexpected set of DONE blocks survived in the kept partition -- abort"

# The deliberate rewrite must land exactly where the archived c2838 EXECUTED
# record was, i.e. between the doc-trim item's header (ends orig. L1134) and
# its STANDING RULES (starts L1158).
assert lines[1133].rstrip().endswith("live queue.)**"), \
    f"unexpected doc-trim header tail: {lines[1133]!r}"
assert lines[1157].lstrip().startswith("**STANDING RULES"), \
    f"unexpected line after the rewrite slot: {lines[1157]!r}"
assert lines[1134].lstrip().startswith("**EXECUTED c2838"), \
    f"archived record does not start where expected: {lines[1134]!r}"

before = []
after = []
for a, b in KEPT:
    (before if b <= 1134 else after).extend(seg(a, b))
assert before[-1] is lines[1133], "rewrite insertion point misaligned"

HEADER = (
    "\n\n## Archived by cycle 2841 (doc-trim cadence; tasks/queue.md 131.5KB/1542 lines,\n"
    "## TRIM DUE per bin/check-doc-size). 8 historical DONE cycle-summary blocks\n"
    "## (c2835, c2834, c2833, c2832, c2829, c2828, c2830, c2831) plus the doc-trim\n"
    "## cadence item's own superseded EXECUTED c2838 record, all verbatim and in\n"
    "## original source order. The newest 5 DONE blocks (c2840 down through c2836)\n"
    "## stayed live. No open `- [ ]` item was archived -- asserted by\n"
    "## bin/_trim2841q.py, which also asserted the kept/archived partition total,\n"
    "## non-overlapping and multiset-identical to the pre-trim file.\n\n"
)

with open("/tmp/c2841_queue.bak", "w") as f:
    f.writelines(lines)

with open(ARCHIVE, "a") as f:
    f.write(HEADER)
    f.writelines(archived_lines)

with open(SRC, "w") as f:
    f.writelines(before + [REWRITE] + after)

print(f"queue.md: {NLINES} -> {len(before) + REWRITE.count(chr(10)) + len(after)} lines (approx); "
      f"archived {len(archived_lines)} lines")
