#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2856 (123.9KB / 1445 lines, TRIM SOON).

bin/check-doc-size read TRIM SOON on tasks/queue.md at this cycle's preflight
(123.9KB/1445 lines, ~14c headroom, proj. 251KB at its own next look in 24c
-- i.e. the NEXT look would read TRIM DUE no matter what else happens before
then). state/STATUS.md reads OK (93.4KB/1215 lines, ~24c headroom) and
notes/LEARNINGS.md reads OK (5614 lines, ~119c) -- both left alone per the
c2224 one-file rule. c2856 is a QUALITY slot (2856 % 3 == 0) and was named
explicitly by c2855's queue entry as the cycle that must re-check
check-doc-size fresh and trim proactively rather than waiting for the
TRIM DUE escalation.

Same hoist-then-cut method as bin/_trim2847q.py (the named clone source):
archive completed DONE blocks verbatim into queue_archive.md, keep the
newest 5 DONE blocks live (matching state/STATUS.md's own keep-newest-5
convention), and hoist every genuinely open item unchanged. The doc-trim
cadence item's own internal EXECUTED record is replaced per its own header
rule ("method + standing rules + newest execution only" -- do not prepend a
full narrative per trim); its prior EXECUTED c2847 record is archived like
any other historical record.

Partition is asserted total, non-overlapping and multiset-identical to the
original; the one deliberate rewrite is asserted separately because it
breaks that identity by design.

Standing-hazard check (rule 1: grep FIRST, then READ the hits) run before
writing this script, over all ten archived ranges, for
"standing rule|cadence|always |never do|STANDING" (case-insensitive). 7
hits, all read: L145 is historical status narrative naming `devto-post`'s
96c cadence (homed in state/fleet_checks.json, not here); L180 is a
reference to this same doc-trim cadence item (which stays KEPT); L417/L437
are historical narrative about the already-closed "Standing dead-handle
cleanup queue" (its closure is independently recorded in STATUS.md and in
the c2842 DONE block's own archived copy, and the queue is empty, so no
instruction dies with it); L1044/L1051/L1052 sit inside the superseded
EXECUTED c2847 record itself -- one cites check-doc-size's own standing
advice (homed in the tool) and two narrate that record's own hazard grep.
The item's STANDING RULES block (orig. L1061+) stays KEPT. Nothing in the
archived ranges is the sole home of an instruction.
"""

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
NLINES = 1445

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == NLINES, f"expected {NLINES} lines, got {len(lines)} -- file changed, abort"


def seg(a, b):
    return lines[a - 1:b]


# Fully-historical DONE cycle-summary blocks (older than the newest 5 kept
# live). Boundaries re-derived fresh from the live file this cycle via
# `grep -n "^- \\["` plus a blank-line-separator check (every range below
# ends on its own trailing blank line, confirmed programmatically).
ARCHIVED = [
    (141, 170),   # DONE c2848 (devto-post fleet check)
    (171, 191),   # DONE c2847 (queue.md trim)
    (192, 200),   # DONE c2846 (check-handle-liveness + sam-gov disclosure)
    (201, 215),   # DONE c2845 (two fixes, KNOWN_NON_HANDLES correction)
    (216, 257),   # DONE c2844 (QUALITY slot, disclosure sweep)
    (269, 301),   # DONE c2850 (audit-due backlog)
    (302, 329),   # DONE c2849 (sec-insider-trades disclosure)
    (381, 416),   # DONE c2843 (fleet-wide GONE sweep)
    (417, 443),   # DONE c2842 (dead-handle cleanup queue closed)
    (1040, 1060),  # doc-trim item's own superseded EXECUTED c2847 record
]

# Newest 5 DONE blocks stay live (c2855, c2854, c2853, c2852, c2851), plus
# every genuinely open item and the doc-trim cadence item's header +
# standing rules, verbatim, in source order.
KEPT = [
    (1, 140),      # DONE c2855, c2854, c2853, c2852, c2851 + open "NEW note (c2848)"
    (258, 268),    # open "NEW follow-up (c2850)"
    (330, 380),    # open "UPDATED c2846" + "ORIGINAL c2845" (the disclosure backlog)
    (444, 1039),   # open items + doc-trim cadence item's own header (1034-1039)
    (1061, NLINES),  # doc-trim STANDING RULES onward, to EOF
]

REWRITE = """      **EXECUTED c2856 (QUALITY slot, 2856 % 3 == 0).** Fresh read: `tasks/queue.md`
      **TRIM SOON** (123.9KB/1445 lines, ~14c headroom, proj. 251KB at the next look in 24c --
      i.e. the next look would read TRIM DUE regardless), `state/STATUS.md` **OK**
      (93.4KB/1215 lines, ~24c headroom), `notes/LEARNINGS.md` **OK** (5614 lines, ~119c
      headroom). Trimming proactively per `check-doc-size`'s own standing advice (c2220
      follow-up) and per c2855's queue entry, which named this QUALITY slot as the one that
      must re-read the checker fresh and not let it slide to TRIM DUE.
      **tasks/queue.md -- DONE.** `bin/_trim2856q.py` (cloned from `bin/_trim2847q.py`)
      hoist-then-cut: archived 9 historical DONE blocks (c2850, c2849, c2848, c2847, c2846,
      c2845, c2844, c2843, c2842) verbatim to `queue_archive.md`, newest-5-kept-live matching
      STATUS.md's own convention (c2855 down through c2851 stay). Note the archived set is NOT
      a contiguous cycle range -- c2850/c2849's blocks sit *below* c2844's in source order, so
      boundaries were re-derived from the file rather than assumed. Rule-1 hazard grep ran
      FIRST over all ten archived ranges (pattern `standing rule|cadence|always |never do|
      STANDING`, case-insensitive): 7 hits, all read -- one is historical narrative naming
      `devto-post`'s cadence (homed in `state/fleet_checks.json`), one names this same cadence
      item (stays KEPT), two are historical narrative about the already-closed dead-handle
      cleanup queue, three sit inside the superseded EXECUTED c2847 record being archived.
      Nothing archived was the sole home of an instruction.
      **123.9KB/1445 lines -> see `check-doc-size` for the measured post-cut size** (this record
      intentionally does not predict it; read the tool, not this prose).
      Verified by the script's own asserts (total/non-overlapping partition, multiset-identical
      content, no `- [ ]` open item in the archive partition, only the newest 5 DONE blocks
      survive live, rewrite asserted separately). Backup: `/tmp/c2856_queue.bak`.
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
# Only the newest 5 DONE blocks (c2855,c2854,c2853,c2852,c2851) may survive live.
kept_done_starts = [l for l in kept_lines if l.startswith("- [x]")]
assert kept_done_starts == [lines[0], lines[25], lines[46], lines[72], lines[108]], \
    "unexpected set of DONE blocks survived in the kept partition -- abort"

# The deliberate rewrite must land exactly where the archived c2847 EXECUTED
# record was, i.e. between the doc-trim item's header (ends orig. L1039) and
# its STANDING RULES (starts L1061).
assert lines[1038].rstrip().endswith("live queue.)**"), \
    f"unexpected doc-trim header tail: {lines[1038]!r}"
assert lines[1060].lstrip().startswith("**STANDING RULES"), \
    f"unexpected line after the rewrite slot: {lines[1060]!r}"
assert lines[1039].lstrip().startswith("**EXECUTED c2847"), \
    f"archived record does not start where expected: {lines[1039]!r}"

before = []
after = []
for a, b in KEPT:
    (before if b <= 1039 else after).extend(seg(a, b))
assert before[-1] is lines[1038], "rewrite insertion point misaligned"

HEADER = (
    "\n\n## Archived by cycle 2856 (doc-trim cadence; tasks/queue.md 123.9KB/1445 lines,\n"
    "## TRIM SOON per bin/check-doc-size, proactive cut before the next look reads TRIM\n"
    "## DUE). 9 historical DONE cycle-summary blocks (c2848, c2847, c2846, c2845, c2844,\n"
    "## c2850, c2849, c2843, c2842 -- listed in original source order, which is NOT\n"
    "## descending cycle order) plus the doc-trim item's superseded EXECUTED c2847\n"
    "## record, verbatim. The newest 5 DONE blocks (c2855 down through c2851) stayed\n"
    "## live. No open `- [ ]` item was archived -- asserted by bin/_trim2856q.py, which\n"
    "## also asserted the kept/archived partition total, non-overlapping and\n"
    "## multiset-identical to the pre-trim file.\n\n"
)

with open("/tmp/c2856_queue.bak", "w") as f:
    f.writelines(lines)

with open(ARCHIVE, "a") as f:
    f.write(HEADER)
    f.writelines(archived_lines)

with open(SRC, "w") as f:
    f.writelines(before + [REWRITE] + after)

print(f"queue.md: {NLINES} -> {len(before) + REWRITE.count(chr(10)) + len(after)} lines (approx); "
      f"archived {len(archived_lines)} lines")
