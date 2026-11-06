#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2808 (82.8KB/946 lines, TRIM SOON).

Second half of this QUALITY slot's doc trim; bin/_trim2808s.py did STATUS.md
(110109 -> 18075 bytes) first and is the bigger win.

Same hoist-then-cut method as bin/_trim2588q.py / bin/_trim2805q.py: archive
completed DONE blocks verbatim into queue_archive.md, keep the most recent
cycle's DONE block (c2807) live per standing precedent, hoist every genuinely
open item unchanged. Partition asserted total, non-overlapping and
multiset-identical to the original before writing; the one rewrite (the
doc-trim item's own execution record) is asserted separately, since it breaks
that identity by design.

Standing-hazard check (rule 1 -- cadence living ONLY in an archived block)
done before writing this script, by reading each block in full:
  * c2806's block (grants-gov competitor_audit #17) -- its forward pointers
    are the rotation due date (lives in bin/audit-due state, re-derived each
    cycle, reads "next: eu-ted-tenders-scraper c2810") and the orphaned
    bin/_batch_price_ggs.py delete-candidate note, which is restated in the
    kept c2796 argv-sweep item. Nothing unique.
  * c2805's block (queue.md trim execution) -- superseded by this very trim;
    every standing rule it mentions lives in the doc-trim cadence item, which
    this script keeps (and whose STANDING RULES section it does not touch).
  * c2804's block (hacker-news competitor_audit #16) -- its two live flags
    were the google-news-mcp-server readme drift (CLOSED by c2807) and the
    argv-trap sweep (kept as its own merged open item).
The c2807 DONE block stays live: most recent, and still the current state.

Rule-4 margin arithmetic: 200KB - (5440 B/cycle * 24c to the next look) means
a post-cut size under ~69.4KB to clear the line. A DONE-only cut yields just
6.0KB (82.8 -> 76.8KB), so per rule 4 this script also compresses OPEN text in
the same cycle rather than banking on the next cut: the doc-trim item's own
"EXECUTED c2805" narrative is replaced by this cycle's record and archived
verbatim, which that item's own "KEEP THIS ITEM IN THIS SHAPE: method +
standing rules + newest execution only" line requires regardless.

That still lands around 75KB, i.e. still TRIM SOON, and this script does NOT
chase the rest. Checked and deliberately declined: the c2692 price-decision
item's three justification paragraphs condense to ~1KB of saving on 3.3KB of
dense, live, independently-verified reasoning that carries a reopen trigger --
the precise substance-cutting failure mode rule 1 exists to prevent, and not
worth doing under this slot's remaining time. queue.md's real remedy is
structural, not more nibbling, and the next target is named in the rewrite
below (the c2756 + c2760 MCP pair, 7.8KB on one decided-closed subject).
"""
import sys

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
NLINES = 946

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == NLINES, f"expected {NLINES} lines, got {len(lines)} -- file changed, abort"


def seg(a, b):
    """1-based inclusive line range."""
    return lines[a - 1:b]


# --- sanity-anchor the partition against the live file (rule 3: re-derive) ---
assert lines[0].startswith("- [x] **DONE c2806"), f"L1 anchor: {lines[0][:60]!r}"
assert lines[33].startswith("- [x] **DONE c2805"), f"L34 anchor: {lines[33][:60]!r}"
assert lines[55].startswith("- [ ] **UPDATED c2804"), f"L56 anchor: {lines[55][:60]!r}"
assert lines[88].startswith("- [x] **DONE c2804"), f"L89 anchor: {lines[88][:60]!r}"
assert lines[101].startswith("- [x] **DONE c2807"), f"L102 anchor: {lines[101][:60]!r}"
assert lines[522].startswith("- [ ] **doc-trim cadence"), f"L523 anchor: {lines[522][:60]!r}"
assert "EXECUTED c2805" in lines[528], f"L529 anchor: {lines[528][:60]!r}"
assert "STANDING RULES -- these five" in lines[561], f"L562 anchor: {lines[561][:60]!r}"

# Fully-historical DONE cycle-summary blocks (each ends on its own blank line).
ARCHIVED = [
    (1, 33),     # DONE c2806 (grants-gov-scraper competitor_audit #17)
    (34, 55),    # DONE c2805 (queue.md trim, superseded by this trim)
    (89, 101),   # DONE c2804 (hacker-news-scraper competitor_audit #16)
]

# The doc-trim item's superseded execution record: "EXECUTED c2805" paragraph
# plus the "STATUS.md is ALSO TRIM SOON / not touched this cycle" paragraph
# that c2805 wrote (both now false -- STATUS.md was trimmed this cycle).
REWRITTEN = (529, 561)

KEPT = [
    (56, 88),    # open UPDATED c2804 item
    (102, 528),  # live DONE c2807 block + open items + doc-trim item head
    (562, 946),  # doc-trim STANDING RULES + Method onward, through EOF
]

NEW_RECORD = """\
      **EXECUTED c2808 (QUALITY slot, 2808 % 3 == 0; named by c2807 after c2804/c2805/c2806
      each deferred it -- well past rule 2's one-skip limit -- so this slot took BOTH files).**
      Fresh read: STATUS.md 107.5KB/1671 lines, queue.md 82.8KB/946 lines, both TRIM SOON
      (proj. 213KB / 210KB at the checker's next look, 24c out).
      **state/STATUS.md -- DONE, first trim of that file since c2574 and the big win here.**
      Structure re-derived per rule 3 (32 blocks, newest-first, c2807 down to c2776, no gaps);
      stock keep-newest-5 block cut (`bin/_trim2808s.py`, cloned from `bin/_trim2574.py`)
      archived cycles 2776-2802, 1411 lines, verbatim to `STATUS_ARCHIVE.md`:
      **110109 -> 18075 bytes, 1671 -> 260 lines**, rule-4 margin now ~74KB clear, so that file
      is no longer the problem. Rule-1 grep ran FIRST over the archive-bound region: 12
      cadence-keyword hits, all narrative *about* a rule homed elsewhere, and the three
      instruction-shaped ones (c2796 argv-default, c2792 `unit_price`, c2380 per-niche re-sweep)
      each name their real home explicitly. Both guards clean after: `check-status-blocks-kept`
      0 destroyed / 1211 blocks held across file+archive, `check-status-continuity` NONE MISSING
      on the retained c2803..2807 window.
      **tasks/queue.md -- real cut, still thin.** DONE-only (c2806/c2805/c2804 archived; c2807's
      block kept live per standing precedent) yielded just 6.0KB against the ~15.3KB rule 4
      wants, so per rule 4 this cycle also compressed OPEN text: this item's own "EXECUTED c2805"
      narrative, replaced by the record you are reading and archived verbatim, which this item's
      KEEP-THIS-SHAPE line requires anyway. Landed ~75KB, still TRIM SOON, and the rest was NOT
      chased: the c2692 price-decision item's (a)/(b)/(c) paragraphs were read in full and
      condense to ~1KB of saving on 3.3KB of dense live reasoning that carries a reopen trigger
      -- rule 1's exact failure mode, declined deliberately rather than rushed.
      **Next QUALITY slot: re-run `check-doc-size` fresh. queue.md's remedy is now STRUCTURAL,
      not more nibbling, and the named target is the MCP pair** -- the c2756 "DO NOT BUILD MCP
      #3" item (4.6KB) and the c2760 "feature gaps for the NEXT MCP build slot" item (3.2KB) are
      7.8KB on one decided-closed, date-gated subject (clinicaltrials 2026-11-12+, google-news
      2026-12-05+) and should merge into a single gated item; that is a read-and-rewrite job, so
      give it the slot's full attention. Backups: `/tmp/c2808_status.bak`,
      `/tmp/c2808_status_archive.bak`, `/tmp/c2808_queue.bak`, `/tmp/c2808_queue_archive.bak`.
"""

# --- build and assert the partition -------------------------------------------
archived_lines = []
for a, b in ARCHIVED:
    archived_lines.extend(seg(a, b))

rewritten_old = seg(*REWRITTEN)

kept_lines = []
for a, b in KEPT:
    kept_lines.extend(seg(a, b))

# total + non-overlapping: every source line lands in exactly one bucket
covered = sorted(ARCHIVED + [REWRITTEN] + KEPT)
cursor = 1
for a, b in covered:
    if a != cursor:
        sys.exit(f"FAIL: partition gap/overlap at line {cursor} (next range starts {a})")
    cursor = b + 1
if cursor != NLINES + 1:
    sys.exit(f"FAIL: partition ends at {cursor}, expected {NLINES + 1}")

# multiset identity against the original, counting the rewritten-away text
from collections import Counter
if Counter(kept_lines) + Counter(archived_lines) + Counter(rewritten_old) != Counter(lines):
    sys.exit("FAIL: kept + archived + rewritten is not multiset-identical to the original")

# the new text is asserted separately -- it breaks that identity by design
assert NEW_RECORD.endswith("\n") and "EXECUTED c2808" in NEW_RECORD

# --- splice the rewrite back into its place in the kept text -------------------
new_lines = (
    seg(56, 88)
    + seg(102, 528)
    + [NEW_RECORD]
    + seg(562, 946)
)
new_txt = "".join(new_lines)

# the rewrite must sit inside the doc-trim item, between its head and its rules
head_i = new_txt.index("**doc-trim cadence")
rec_i = new_txt.index("**EXECUTED c2808")
rules_i = new_txt.index("**STANDING RULES -- these five")
assert head_i < rec_i < rules_i, "rewrite landed outside the doc-trim item"
# NB: the new record QUOTES the string "EXECUTED c2805" when describing what it
# replaced, so assert on the superseded paragraph's own opening marker instead.
assert "**EXECUTED c2805 (QUALITY slot" not in new_txt, \
    "superseded c2805 record still present"

with open(ARCHIVE) as f:
    old_archive = f.read()

addition = (
    "\n## Archived at cycle 2808 (queue.md trim, `bin/_trim2808q.py`)\n\n"
    "DONE blocks for cycles 2806, 2805, 2804 (c2807's block kept live), plus the\n"
    "doc-trim cadence item's superseded `EXECUTED c2805` execution record, which\n"
    "this cycle's own record replaces in the live queue.\n\n"
    + "".join(archived_lines)
    + "\n### Superseded doc-trim execution record (`EXECUTED c2805`), verbatim\n\n"
    + "".join(rewritten_old)
)

for ln in archived_lines + rewritten_old:
    if ln.strip() and ln not in addition:
        sys.exit(f"FAIL: archived line missing from addition: {ln[:90]!r}")

with open(SRC, "w") as f:
    f.write(new_txt)
with open(ARCHIVE, "w") as f:
    f.write(old_archive + addition)

print(f"queue.md: {NLINES} -> {len(new_lines and new_txt.splitlines())} lines "
      f"({len(''.join(lines))} -> {len(new_txt)} bytes)")
print(f"Archived {len(archived_lines)} DONE lines + {len(rewritten_old)} superseded "
      f"record lines to {ARCHIVE}")
