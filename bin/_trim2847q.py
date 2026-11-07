#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2847 (118.2KB / 1377 lines, TRIM SOON).

bin/check-doc-size read TRIM SOON on tasks/queue.md at this cycle's preflight
(118.2KB/1377 lines, ~15c headroom, proj. 246KB at its own next look in 24c
-- i.e. the NEXT look would read TRIM DUE no matter what else happens before
then). state/STATUS.md reads OK (56.8KB/734 lines, ~33c headroom) and
notes/LEARNINGS.md reads OK (5528 lines, ~124c) -- both left alone per the
c2224 one-file rule. c2847 is a QUALITY slot (2847 % 3 == 0) and was named
explicitly by state/STATUS.md's c2845/c2846 entries as the cycle that must
trim this proactively rather than waiting for the TRIM DUE escalation.

Same hoist-then-cut method as bin/_trim2841q.py (the named clone source):
archive completed DONE blocks verbatim into queue_archive.md, keep the
newest 5 DONE blocks live (matching state/STATUS.md's own keep-newest-5
convention), and hoist every genuinely open item unchanged. The doc-trim
cadence item's own internal EXECUTED record is replaced per its own header
rule ("method + standing rules + newest execution only" -- do not prepend a
full narrative per trim); its prior EXECUTED c2841 record is archived like
any other historical record.

Partition is asserted total, non-overlapping and multiset-identical to the
original; the one deliberate rewrite is asserted separately because it
breaks that identity by design.

Standing-hazard check (rule 1: grep FIRST, then READ the hits) run before
writing this script, over the one archived range, for
"standing rule|cadence|always |never do|STANDING" (case-insensitive). 8
hits, all read: one is a reference to the doc-trim cadence item itself
(stays KEPT, not archived), one points at the process lesson at the end of
this file (also stays KEPT, outside the archived range), and six are
narrative mentions of the already-closed "Standing dead-handle cleanup
queue" (purely historical status reporting, not an instruction homed only
here -- the queue's closure is independently recorded in STATUS.md and the
c2842 DONE block, which stays live). Nothing in the archived range is the
sole home of an instruction.
"""

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
NLINES = 1377

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
    (181, 378),   # DONE c2841 (queue.md trim), c2840 (apple-podcasts enum_audit),
                  # c2839 (fda-recall enum_audit), c2838 (STATUS.md trim),
                  # c2837 (remote-jobs enum_audit), c2836 (git-maintain +
                  # trademark-search enum_audit + GONE fixes)
    (975, 992),   # doc-trim item's own superseded EXECUTED c2841 record
]

# Newest 5 DONE blocks stay live (c2846, c2845, c2844, c2843, c2842), plus
# every genuinely open item and the doc-trim cadence item's header +
# standing rules, verbatim, in source order.
KEPT = [
    (1, 180),      # DONE c2846, c2845, c2844 + open "UPDATED c2846"/"ORIGINAL c2845"
                   # items + DONE c2843, c2842
    (379, 974),    # open items 379-968 + doc-trim cadence item's own header (969-974)
    (993, NLINES),  # doc-trim STANDING RULES onward, to EOF
]

REWRITE = """      **EXECUTED c2847 (QUALITY slot, 2847 % 3 == 0).** Fresh read: `tasks/queue.md`
      **TRIM SOON** (118.2KB/1377 lines, ~15c headroom, proj. 246KB at the next look in 24c --
      i.e. the next look would read TRIM DUE regardless), `state/STATUS.md` **OK**
      (56.8KB/734 lines, ~33c headroom), `notes/LEARNINGS.md` **OK** (5528 lines, ~124c
      headroom). Trimming proactively per `check-doc-size`'s own standing advice (c2220
      follow-up) and per STATUS.md's c2845/c2846 entries, which named this QUALITY slot as the
      one that must not let it slide to TRIM DUE.
      **tasks/queue.md -- DONE.** `bin/_trim2847q.py` (cloned from `bin/_trim2841q.py`)
      hoist-then-cut: archived 6 historical DONE blocks (c2841, c2840, c2839, c2838, c2837,
      c2836) verbatim to `queue_archive.md`, newest-5-kept-live matching STATUS.md's own
      convention (c2846 down through c2842 stay). Rule-1 hazard grep ran FIRST over the one
      archived range (pattern `standing rule|cadence|always |never do|STANDING`,
      case-insensitive): 8 hits, all read -- one names this same cadence item (stays KEPT),
      one points at the file's own closing process lesson (also stays KEPT, outside the
      archived range), six are historical status narrative about the already-closed dead-handle
      cleanup queue. Nothing archived was the sole home of an instruction.
      **118.2KB/1377 lines -> see `check-doc-size` for the measured post-cut size** (this record
      intentionally does not predict it; read the tool, not this prose).
      Verified by the script's own asserts (total/non-overlapping partition, multiset-identical
      content, no `- [ ]` open item in the archive partition, only the newest 5 DONE blocks
      survive live, rewrite asserted separately). Backup: `/tmp/c2847_queue.bak`.
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
# Only the newest 5 DONE blocks (c2846,c2845,c2844,c2843,c2842) may survive live.
kept_done_starts = [l for l in kept_lines if l.startswith("- [x]")]
assert kept_done_starts == [lines[0], lines[9], lines[24], lines[117], lines[153]], \
    "unexpected set of DONE blocks survived in the kept partition -- abort"

# The deliberate rewrite must land exactly where the archived c2841 EXECUTED
# record was, i.e. between the doc-trim item's header (ends orig. L974) and
# its STANDING RULES (starts L993).
assert lines[973].rstrip().endswith("live queue.)**"), \
    f"unexpected doc-trim header tail: {lines[973]!r}"
assert lines[992].lstrip().startswith("**STANDING RULES"), \
    f"unexpected line after the rewrite slot: {lines[992]!r}"
assert lines[974].lstrip().startswith("**EXECUTED c2841"), \
    f"archived record does not start where expected: {lines[974]!r}"

before = []
after = []
for a, b in KEPT:
    (before if b <= 974 else after).extend(seg(a, b))
assert before[-1] is lines[973], "rewrite insertion point misaligned"

HEADER = (
    "\n\n## Archived by cycle 2847 (doc-trim cadence; tasks/queue.md 118.2KB/1377 lines,\n"
    "## TRIM SOON per bin/check-doc-size, proactive cut before the next look reads TRIM\n"
    "## DUE). 6 historical DONE cycle-summary blocks (c2841, c2840, c2839, c2838, c2837,\n"
    "## c2836), verbatim and in original source order. The newest 5 DONE blocks (c2846\n"
    "## down through c2842) stayed live. No open `- [ ]` item was archived -- asserted by\n"
    "## bin/_trim2847q.py, which also asserted the kept/archived partition total,\n"
    "## non-overlapping and multiset-identical to the pre-trim file.\n\n"
)

with open("/tmp/c2847_queue.bak", "w") as f:
    f.writelines(lines)

with open(ARCHIVE, "a") as f:
    f.write(HEADER)
    f.writelines(archived_lines)

with open(SRC, "w") as f:
    f.writelines(before + [REWRITE] + after)

print(f"queue.md: {NLINES} -> {len(before) + REWRITE.count(chr(10)) + len(after)} lines (approx); "
      f"archived {len(archived_lines)} lines")
