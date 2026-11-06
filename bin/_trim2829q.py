#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2829 (129.8KB / 1506 lines, TRIM DUE).

bin/check-doc-size read TRIM DUE on tasks/queue.md at this cycle's preflight
(129.8KB/1506 lines, ~13 cycles of headroom at +5440 B/cycle, proj. 257KB at
its own next look in 24c). state/STATUS.md reads TRIM SOON (113.3KB, ~20c
headroom) and notes/LEARNINGS.md reads OK (5352 lines, ~132c) -- both left
alone per the c2224 one-file rule; TRIM DUE outranks SOON, and the standing
doc-trim rule 2 says a QUALITY slot must not pass a TRIM DUE file, so 2829
(2829 % 3 == 0) executes it.

Same hoist-then-cut method as bin/_trim2820q.py (the named clone source):
archive completed DONE blocks verbatim into queue_archive.md, keep the most
recent cycle's DONE block (2828) live since it carries the current "next
cycle" pointer, and hoist every genuinely open item unchanged. Partition is
asserted total, non-overlapping and multiset-identical to the original; the
one deliberate rewrite (the doc-trim cadence item's own execution record, per
that item's "newest execution only" instruction) is asserted separately
because it breaks that identity by design.

Standing-hazard check (rule 1: grep FIRST, then READ the hits) run before
writing this script, over all 11 archive ranges. Hits were: owner-email rule
("nothing only they can fix" -- CLAUDE.md rule 3, not sole-homed here),
"standing rule" references to c2812/c2796 (both their own KEPT open items,
orig. L646/L751), a cadence reference to the doc-trim item itself (which
stays KEPT, not archived), and one slot-process lesson (orig. L345, "check
the slot-type arithmetic FIRST") -- every cycle's STATUS.md header since has
in fact led with the slot-type arithmetic, so the lesson has already
propagated into practice and is not the sole record of it (CLAUDE.md's cycle
protocol is the standing instruction; this was one cycle's reminder-to-self).
Nothing in the archive ranges is the sole home of an instruction, and
archiving is a move, not a delete.
"""

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
NLINES = 1506

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == NLINES, f"expected {NLINES} lines, got {len(lines)} -- file changed, abort"


def seg(a, b):
    return lines[a - 1:b]


# Fully-historical DONE cycle-summary blocks, each range ends on its own
# trailing blank line so the kept file keeps exactly one blank between items
# (boundaries re-derived fresh from the live file this cycle per standing
# rule 3, via `grep -n "^- \\["`).
ARCHIVED = [
    (97, 143),     # DONE 2827  failed-Actor triage + check-dead-endpoint-docs + nih-reporter-scraper audit
    (144, 191),    # DONE 2826  devto-comments/check-disclosure QUALITY slot
    (192, 227),    # DONE 2825  clinicaltrials-scraper competitor_audit
    (228, 247),    # DONE 2827  trademark-search-scraper transient-failure triage (2nd 2827 block)
    (248, 299),    # DONE 2824  check-primary-event fleet check
    (300, 353),    # DONE 2823  court-records-scraper competitor_audit
    (371, 385),    # SUPERSEDED 2828  johnvc/GoogleNewsAPI arithmetic (superseded by the live UPDATED c2828 watch)
    (391, 427),    # DONE 2822  trademark-search-scraper competitor_audit
    (428, 468),    # DONE 2821  uk-find-a-tender-scraper competitor_audit
    (469, 503),    # DONE 2820  2 DUE checks + queue.md trim
    (504, 558),    # DONE 2819  sam-gov-opportunities-scraper competitor_audit
    (1090, 1121),  # doc-trim item's own superseded EXECUTED c2820 record (replaced by REWRITE below)
]

# Most recent cycle's DONE block stays live (carries the current "next cycle"
# pointer), plus every genuinely open item, verbatim, in source order.
KEPT = [
    (1, 96),       # DONE cycle 2828 + its 2 open follow-ups (precision-defect note, johnvc UPDATED watch)
    (354, 370),    # open: c2824 check-primary-event ack-mechanism follow-up
    (386, 390),    # open: c2823 doc-hygiene follow-up (left for a small follow-up edit after this trim)
    (559, 1089),   # open: c2816 through doc-trim item's own header lines
    (1122, NLINES),  # open: doc-trim STANDING RULES onward, to EOF
]

# Replacement for the archived (1090, 1121) execution record. The doc-trim
# item's own header forbids prepending a full narrative per trim ("method +
# standing rules + newest execution only"), so c2820's narrative goes to the
# archive and this records c2829 compactly in its place.
REWRITE = """      **EXECUTED c2829 (QUALITY slot, 2829 % 3 == 0).** Fresh read: `tasks/queue.md`
      **TRIM DUE** (129.8KB/1506 lines, ~13c headroom, proj. 257KB at the next look in 24c),
      `state/STATUS.md` **TRIM SOON** (113.3KB/1548 lines, ~20c headroom -- left alone, one file
      per cycle per the c2224 rule), `notes/LEARNINGS.md` **OK** (5352 lines, ~132c). TRIM DUE
      outranks SOON, so queue.md is the one touched this cycle.
      **tasks/queue.md -- DONE.** `bin/_trim2829q.py` (cloned from `bin/_trim2820q.py`)
      hoist-then-cut: archived 10 historical DONE blocks (c2827 x2, c2826, c2825, c2824, c2823,
      c2822, c2821, c2820, c2819 -- c2828's kept live per standing precedent, it carries the
      current pointer) plus the superseded c2828 `johnvc/GoogleNewsAPI` arithmetic record
      (the live UPDATED c2828 watch item already carries the pointer forward), all verbatim to
      `queue_archive.md`. Rule-1 hazard grep ran FIRST over all 11 ranges and every hit was READ:
      the owner-email rule is CLAUDE.md's, not sole-homed here; the c2812/c2796 standing-rule
      references point to their own KEPT open items; one slot-process lesson (orig. L345, "check
      the slot-type arithmetic FIRST") has visibly propagated into practice in every subsequent
      cycle's own STATUS.md header, so archiving it loses no live instruction.
      **129.8KB/1506 lines -> {NEW_KB:.1f}KB/{NEW_LINES} lines**, ~{HEADROOM}c headroom (measured
      by `check-doc-size` after the write, not predicted).
      Verified by the script's own asserts (total/non-overlapping partition, multiset-identical
      content, no `- [ ]` open item in the archive partition, no DONE block but c2828 kept,
      rewrite asserted separately). Backup: `/tmp/c2829_queue.bak`.
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

# No open item may leave the live file, and no DONE block may stay beyond 2828.
assert not [l for l in archived_lines if l.startswith("- [ ]")], \
    "an open item is in the archive partition -- abort"
assert [l for l in kept_lines if l.startswith("- [x]")] == [lines[0]], \
    "a DONE block other than cycle 2828 survived in the kept partition -- abort"

# The deliberate rewrite is asserted separately, since it breaks the identity
# above by design. It must land exactly where the archived c2820 execution
# record was, i.e. between the doc-trim item's header (ends orig. L1089) and
# its STANDING RULES (starts L1122).
assert lines[1088].rstrip().endswith("live queue.)**"), \
    f"unexpected doc-trim header tail: {lines[1088]!r}"
assert lines[1121].lstrip().startswith("**STANDING RULES"), \
    f"unexpected line after the rewrite slot: {lines[1121]!r}"
assert lines[1089].lstrip().startswith("**EXECUTED c2820"), \
    f"archived record does not start where expected: {lines[1089]!r}"

split = sum(1 for a, b in KEPT if b <= 1089)   # kept ranges before the rewrite slot
before = []
after = []
for a, b in KEPT:
    (before if b <= 1089 else after).extend(seg(a, b))
assert split == 4 and before[-1] is lines[1088], "rewrite insertion point misaligned"

new_lines_preview = before + [REWRITE] + after

HEADER = (
    "\n\n## Archived by cycle 2829 (doc-trim cadence; tasks/queue.md 129.8KB/1506 lines,\n"
    "## TRIM DUE per bin/check-doc-size). 10 historical DONE cycle-summary blocks\n"
    "## (c2827 x2, c2826, c2825, c2824, c2823, c2822, c2821, c2820, c2819) plus the\n"
    "## superseded c2828 johnvc/GoogleNewsAPI arithmetic record, all verbatim and in\n"
    "## original source order. c2828's DONE block stayed live (newest, carries the\n"
    "## current pointer). No open `- [ ]` item was archived -- asserted by\n"
    "## bin/_trim2829q.py, which also asserted the kept/archived partition total,\n"
    "## non-overlapping and multiset-identical to the pre-trim file.\n\n"
)

with open("/tmp/c2829_queue.bak", "w") as f:
    f.writelines(lines)

with open(ARCHIVE, "a") as f:
    f.write(HEADER)
    f.writelines(archived_lines)

# Write a placeholder first so check-doc-size can measure the real post-cut size,
# then patch the REWRITE text's {NEW_KB}/{NEW_LINES}/{HEADROOM} placeholders in a
# second pass (the record is informational prose, not load-bearing data).
with open(SRC, "w") as f:
    f.writelines(before + [REWRITE] + after)

print(f"queue.md: {NLINES} -> {len(before) + REWRITE.count(chr(10)) + len(after)} lines (approx); "
      f"archived {len(archived_lines)} lines")
