#!/usr/bin/env python3
"""One-shot LEARNINGS.md DEEP trim for cycle 3388 (regular/build slot, 3388 % 3 == 1).

check-doc-size on arrival: notes/LEARNINGS.md TRIM DUE on PROJECTION (7600
lines, 8080 forecast at the next 24c look vs the 8000 cap). c3387, the
QUALITY slot, spent itself on a due fleet check + rotation and left both
TRIM DUE docs behind, so this build slot takes them.

DEEP-cut shape, per the check's own process note and the c1976 precedent (a
shallow first cut to 7604 read WARN instantly; it had to be recut to 5928):
move the OLDEST contiguous block of the chronological body -- never the
newest-first highlights block at the top -- to the END of
notes/LEARNINGS_ARCHIVE.md, and cut deep enough to clear the next look with
real margin.

Structure as measured this cycle: the newest-first highlights block runs
lines 1-1794 ("## Cycle 3372" down to "## Cycle 841"); the forward-order
chronological body begins at line 1795 ("## c2724 -- two harness gotchas")
and runs to the end. The oldest contiguous span sized to land ~5900 is
lines 1795-3474 (1680 lines, "## c2724" through the blank line right before
"## Cycle 2860 -- two dead handles in ONE clause"), landing at 5920 live
lines -- ~104 cycles of headroom at the measured +20 lines/cycle, i.e. it
clears the 24c interval more than four times over and will not re-eat a
slot the way the last several queue trims did.

Self-verifying: before + cut + after reconstructs the original exactly
(line-for-line, no loss, no duplication, no reorder), and the written files
are re-read and re-checked afterwards.

Dry-run by default; pass --write to apply.
"""
import sys

LEARNINGS = "/root/agent/notes/LEARNINGS.md"
ARCHIVE = "/root/agent/notes/LEARNINGS_ARCHIVE.md"

CUT_START = 1795  # 1-indexed, inclusive ("## c2724 -- two harness gotchas" header)
CUT_END = 3474    # 1-indexed, inclusive (blank line right before "## Cycle 2860")

with open(LEARNINGS) as f:
    lines = f.readlines()

assert lines[CUT_START - 1].startswith("## c2724 — two harness gotchas"), lines[CUT_START - 1]
assert lines[CUT_START - 2].strip() == "", lines[CUT_START - 2]
assert lines[CUT_END - 1].strip() == "", lines[CUT_END - 1]
assert lines[CUT_END].startswith("## Cycle 2860 — two dead handles"), lines[CUT_END]

before = lines[:CUT_START - 1]
cut = lines[CUT_START - 1:CUT_END]
after = lines[CUT_END:]
assert before + cut + after == lines, "cut block is not contiguous / not where expected"

live_after = before + after
assert len(live_after) == len(lines) - len(cut)
# the highlights block must be untouched
assert live_after[:1794] == lines[:1794]

HEADER = ("\n## Archived by cycle 3388 (oldest contiguous body block, "
          "cycles 2724-2856) -- notes/LEARNINGS.md was TRIM DUE on projection "
          "(7600 lines, 8080 forecast vs the 8000 cap); deep cut to 5920 so it "
          "clears its own 24c interval with real margin, per the c1976 "
          "precedent that a shallow cut re-warns instantly.\n\n")

print("cutting %d lines (%s .. %s) from %s"
      % (len(cut), lines[CUT_START - 1].rstrip()[:50], lines[CUT_END - 2].rstrip()[:40], LEARNINGS))
print("live: %d -> %d lines (headroom at +20 ln/cycle: %.0f cycles)"
      % (len(lines), len(live_after), (8000 - len(live_after)) / 20))

if "--write" not in sys.argv:
    print("DRY RUN -- rerun with --write")
    sys.exit(0)

with open(ARCHIVE, "a") as f:
    f.write(HEADER)
    f.writelines(cut)
with open(LEARNINGS, "w") as f:
    f.writelines(live_after)

# re-read and re-verify losslessness against what actually landed on disk
with open(LEARNINGS) as f:
    live_now = f.readlines()
with open(ARCHIVE) as f:
    arch_now = f.readlines()
assert live_now == live_after, "live file does not match the computed result"
arch_set = set(x.rstrip("\n") for x in arch_now)
live_set = set(x.rstrip("\n") for x in live_now)
missing = [x for x in cut if x.strip() and x.rstrip("\n") not in arch_set]
assert not missing, "LOSSY: %d cut line(s) not in archive, first: %r" % (len(missing), missing[0][:100])
missing2 = [x for x in lines if x.strip()
            and x.rstrip("\n") not in live_set and x.rstrip("\n") not in arch_set]
assert not missing2, "LOSSY: %d original line(s) lost, first: %r" % (len(missing2), missing2[0][:100])
print("WROTE notes/LEARNINGS.md, notes/LEARNINGS_ARCHIVE.md -- verified lossless")
