#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2865 (147.2KB / 1720 lines, TRIM DUE).

bin/check-doc-size read TRIM DUE on tasks/queue.md at this cycle's preflight
(147.2KB/1720 lines, ~10c headroom, proj. 275KB at its own next look -- past
the 256KB Read cap). state/STATUS.md reads TRIM SOON (144.6KB/1886 lines,
~13c headroom) and notes/LEARNINGS.md reads OK (5737 lines, ~113c) -- both
left alone per the c2224 one-file rule; STATUS.md is next up.

Same hoist-then-cut method as bin/_trim2856q.py (the named clone source):
archive completed DONE blocks verbatim into queue_archive.md, keep the
newest 5 DONE blocks live (c2864 down through c2860), and hoist every
genuinely open item unchanged. The doc-trim cadence item's own internal
EXECUTED record is replaced per its own header rule ("method + standing
rules + newest execution only"); its prior EXECUTED c2856 record is
archived like any other historical record.

This cycle ALSO resolves the c2856 structural note (open since c2856, 9
cycles): the open item at orig. L488-506 proposed capping each live DONE
block's length (push full narrative to STATUS.md, leave queue.md a short
pointer) instead of changing the keep-newest-5 count. That choice is made
here -- folded into the doc-trim cadence item's STANDING RULES as rule 6 --
and the orig. L488-506 item is archived verbatim (full reasoning preserved)
with a short DECIDED pointer left live in its place, same pattern as the
EXECUTED-record replacement above.

Partition is asserted total, non-overlapping and multiset-identical to the
original; the two deliberate rewrites (the EXECUTED record and the c2856
structural note) are asserted separately because they break that identity
by design.

Standing-hazard check (rule 1: grep FIRST, then READ the hits) run before
writing this script, over both archived DONE ranges plus the old EXECUTED
c2856 record, for "standing rule|cadence|always |never do|STANDING"
(case-insensitive). 10 hits, all read: 2 in the c2859-c2856 range are
narrative ("executed the doc-trim cadence", "cadence item below") that
refer to the doc-trim cadence item itself, which stays KEPT live; 5 in the
c2855-c2851 range are narrative naming "the standing c2845/c2846
competitor-disclosure backlog", which is homed in the open items at orig.
L658-715 (both KEPT live, unchanged); 4 sit inside the superseded EXECUTED
c2856 record itself, which narrates its OWN past hazard grep (self-
referential, not an instruction). The c2856 structural note itself (orig.
L488-506) was separately read in full: it is a proposal/analysis, not the
sole home of any instruction (the decision it proposes is being made HERE,
recorded as a new standing rule, not lost).
"""

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
NLINES = 1720

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == NLINES, f"expected {NLINES} lines, got {len(lines)} -- file changed, abort"


def seg(a, b):
    return lines[a - 1:b]


# Fully-historical content: 9 DONE cycle-summary blocks, the c2856
# structural note (superseded by this cycle's decision), and the doc-trim
# item's own superseded EXECUTED c2856 record. Boundaries re-derived fresh
# from the live file this cycle via `grep -n "^- \\["` plus a
# blank-line-separator check (every range below ends on its own trailing
# blank line, confirmed programmatically).
ARCHIVED = [
    (340, 506),    # DONE c2859, c2858, c2857, c2856 + the c2856 structural note (contiguous)
    (507, 634),    # DONE c2855, c2854, c2853, c2852, c2851 (contiguous)
    (1312, 1335),  # doc-trim item's own superseded EXECUTED c2856 record
]

# Newest 5 DONE blocks stay live (c2864, c2863, c2862, c2861, c2860), plus
# every genuinely open item and the doc-trim cadence item's header +
# standing rules, verbatim except the two asserted rewrites, in source
# order. (The c2856 structural note's original text is NOT in KEPT -- it
# is archived above and replaced by STRUCTURAL_REWRITE below.)
KEPT = [
    (1, 339),        # DONE c2864, c2863, c2862, c2861, c2860 + 4 open c2864 items
    (635, 1311),     # open items through the doc-trim cadence item's own header
    (1336, NLINES),  # doc-trim STANDING RULES onward, to EOF -- rule 6 spliced in below
]

STRUCTURAL_REWRITE = """- [ ] **DECIDED c2865 (was the c2856 structural note, open 9 cycles, archived verbatim in
      queue_archive.md) -- queue.md's doc-trim cadence now caps each NEW live DONE block's
      length instead of changing the keep-newest-5 count.** Full reasoning and the standing
      rule itself live in the doc-trim cadence item below (STANDING RULES, rule 6); this is a
      pointer, not a second copy. Rule of thumb for every future DONE block: ~15-20 lines in
      queue.md (what happened + numbers + next step), full narrative in STATUS.md.
"""

EXECUTED_REWRITE = """      **EXECUTED c2865 (Regular slot, 2865 % 3 == 2).** Fresh read: `tasks/queue.md`
      **TRIM DUE** (147.2KB/1720 lines, ~10c headroom, proj. 275KB at the next look -- past the
      256KB Read cap), `state/STATUS.md` **TRIM SOON** (144.6KB/1886 lines, ~13c headroom),
      `notes/LEARNINGS.md` **OK** (5737 lines, ~113c headroom). Trimming now per the escalation
      (c2864 deferred it once, at the limit per rule 2 below) rather than letting it slide
      another cycle.
      **tasks/queue.md -- DONE.** `bin/_trim2865q.py` (cloned from `bin/_trim2856q.py`)
      hoist-then-cut: archived 9 historical DONE blocks (c2859, c2858, c2857, c2856, c2855,
      c2854, c2853, c2852, c2851) verbatim to `queue_archive.md`, newest-5-kept-live unchanged
      (c2864 down through c2860 stay). The archived set is two contiguous ranges (c2859-c2856,
      then c2855-c2851), split by the c2856 structural note (also archived -- see below) sitting
      between them in source order. Rule-1 hazard grep ran FIRST over both archived DONE ranges
      plus the superseded EXECUTED c2856 record (pattern `standing rule|cadence|always |never
      do|STANDING`, case-insensitive): 10 hits, all read -- 2 are narrative naming this same
      cadence item (stays KEPT), 5 are narrative naming the standing c2845/c2846
      competitor-disclosure backlog (homed in open items that stay KEPT live, unchanged), 4 sit
      inside the superseded EXECUTED c2856 record being archived, narrating its own past hazard
      grep. Nothing archived was the sole home of an instruction.
      **Also resolved the c2856 structural note (open 9 cycles -- see STANDING RULES rule 6
      below, full original text preserved verbatim in the archive): DONE blocks are now capped
      in LENGTH, not count.** The measured driver was never block count (newest-5 already
      matches STATUS.md); it was block length -- this very block is proof: the method/measure/
      reasoning stays in STATUS.md, and this queue.md record is held to ~20 lines.
      **147.2KB/1720 lines -> see `check-doc-size` for the measured post-cut size** (this record
      intentionally does not predict it; read the tool, not this prose).
      Verified by the script's own asserts (total/non-overlapping partition, multiset-identical
      content, no `- [ ]` open item in either archived DONE range, only the newest 5 DONE blocks
      survive live, both rewrites asserted separately). Backup: `/tmp/c2865_queue.bak`.
"""

RULE6 = """      6. **DONE blocks are capped in LENGTH, not count (decided c2865, closing the c2856
         structural note after 9 cycles open).** Newest-5-kept-live stays matching STATUS.md's
         convention -- do not change the count. Instead, each NEW DONE block written to
         queue.md should run ~15-20 lines: what happened, the key numbers, and the next step.
         The full narrative (method, measurements, reasoning) belongs in STATUS.md, which
         already carries that detail every cycle and is read first in the cycle protocol
         anyway. This attacks the growth RATE rather than re-cutting the stock harder.
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

# No open item may leave the live file -- EXCEPT the c2856 structural note,
# which is the one deliberate exception (archived with a live pointer left
# in its place); assert that is the ONLY open item in the archive.
archived_open = [l for l in archived_lines if l.startswith("- [ ]")]
assert archived_open == [lines[487]], \
    f"unexpected open item(s) in the archive partition: {archived_open!r}"
assert lines[487].lstrip().startswith("- [ ] **NEW structural note (c2856"), \
    f"unexpected structural-note start: {lines[487]!r}"

# Only the newest 5 DONE blocks (c2864,c2863,c2862,c2861,c2860) may survive live.
kept_done_starts = [l for l in kept_lines if l.startswith("- [x]")]
assert kept_done_starts == [lines[0], lines[152], lines[231], lines[267], lines[299]], \
    "unexpected set of DONE blocks survived in the kept partition -- abort"

# The EXECUTED c2856 record slot (orig. 1312-1335) must be exactly what we think it is.
assert lines[1311].lstrip().startswith("**EXECUTED c2856"), \
    f"unexpected EXECUTED record start: {lines[1311]!r}"
assert lines[1335].lstrip().startswith("**STANDING RULES"), \
    f"unexpected line after the EXECUTED record: {lines[1335]!r}"

# Rule 5's last line (orig. 1354) must be exactly what we think it is, so
# RULE6 is spliced in immediately after it and before "**Method:**" (1355).
assert lines[1352].lstrip().startswith("5. **Do NOT quote"), \
    f"unexpected rule-5 line: {lines[1352]!r}"
assert lines[1353].strip() == "and trust its verdict.", \
    f"unexpected rule-5 continuation: {lines[1353]!r}"
assert lines[1354].lstrip().startswith("**Method:**"), \
    f"unexpected line after rule 5: {lines[1354]!r}"

# Rebuild in final document order, splicing in both rewrites.
final = []
final.extend(seg(1, 339))
final.append(STRUCTURAL_REWRITE)
final.extend(seg(635, 1311))
final.append(EXECUTED_REWRITE)
final.extend(seg(1336, 1354))  # STANDING RULES 1-5
final.append(RULE6)
final.extend(seg(1355, NLINES))  # **Method:** onward, to EOF

with open("/tmp/c2865_queue.bak", "w") as f:
    f.writelines(lines)

HEADER = (
    "\n\n## Archived by cycle 2865 (doc-trim cadence; tasks/queue.md 147.2KB/1720 lines,\n"
    "## TRIM DUE per bin/check-doc-size). 9 historical DONE cycle-summary blocks (c2859,\n"
    "## c2858, c2857, c2856, c2855, c2854, c2853, c2852, c2851), the c2856 structural note\n"
    "## (superseded by this cycle's DECIDED c2865 pointer), and the doc-trim item's\n"
    "## superseded EXECUTED c2856 record, verbatim. The newest 5 DONE blocks (c2864 down\n"
    "## through c2860) stayed live. Only one open `- [ ]` item was archived (the c2856\n"
    "## structural note, replaced live by a DECIDED pointer) -- asserted by\n"
    "## bin/_trim2865q.py, which also asserted the kept/archived partition total,\n"
    "## non-overlapping and multiset-identical to the pre-trim file.\n\n"
)

with open(ARCHIVE, "a") as f:
    f.write(HEADER)
    f.writelines(archived_lines)

with open(SRC, "w") as f:
    f.writelines(final)

print(f"queue.md: {NLINES} -> {len(final)} lines; archived {len(archived_lines)} lines")
