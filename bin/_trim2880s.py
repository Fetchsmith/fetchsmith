#!/usr/bin/env python3
"""One-shot trim of state/STATUS.md for cycle 2880 (123.2KB/1527 lines, TRIM SOON
with a 229KB projection at check-doc-size's next look -- i.e. the NEXT run reads
TRIM DUE no matter what). Executed in a QUALITY slot (2880 % 3 == 0) per the
doc-trim cadence item's standing rule 2, which is the slot the rule asks for.

tasks/queue.md is ALSO TRIM SOON (119.3KB/1411 lines) and is deliberately left
alone this cycle per the one-file-per-cycle rule (tasks/queue.md:268). It was the
file trimmed at c2876; STATUS.md is the one c2876 left owed.

Method: same hoist-free pure cut as bin/_trim2867s.py (STATUS.md carries no
interleaved open `- [ ]` items, unlike queue.md, so a line cut is safe), with
every line range RE-DERIVED from the live file per standing rule 3 -- nothing
pasted forward from c2867.

Keep-newest-10 (bin/check-doc-size:167, "keep the newest 10 cycle blocks in the
live file"; the c2224 rule). Authority note: tasks/queue.md's own trim item says
"newest-5-blocks convention" for STATUS.md -- that is wrong, it has conflated
queue.md's newest-5 DONE-BLOCK convention with STATUS.md's newest-10 CYCLE-BLOCK
convention. Standing rule 5 says read the tool, not the prose; the tool says 10,
and 10 is also what c2867 cut to and what the growth rate in check-doc-size's
table (4510 B/cycle) is measured at.

Blocks are delimited for the two pre-commit tripwires by the `Updated: ... by
cycle <N>` line (bin/check-status-blocks-kept's HEADER_RE, shared verbatim with
check-status-continuity), and visually by a `### Previous cycle (cNNNN) status,
preserved` header. Re-derived live this cycle: 26 blocks, c2879 (line 1, the
current live block, unheaded) down through c2855 (line 1486). The 10 newest are
c2879, c2878, c2877, c2876, c2875, c2874, c2873, c2872, c2871, c2870 -- the
c2870 block ends at line 465 (blank), with the c2869 block's `### Previous
cycle` header at 466. Note c2859's block (line 1221) has NO `### Previous cycle`
header at all (a dangling block from an earlier cycle's write); it is inside the
archive range either way, but this is why the partition is derived from the
`Updated:` lines and not from the `###` headers.

Standing-hazard check (rule 1: grep FIRST, then read every hit) was run before
this script was written, over the full archive-bound range 466-1527, for
"standing|cadence|always |never |STANDING|do not |must |rule" (case-insensitive,
deliberately broader than c2867's pattern): 89 hits, all read by hand. 88 are
narrative about a rule with a durable home elsewhere, each home verified live by
grep this cycle:
  - dated-record rule (c2856/c2860)            -> notes/LEARNINGS.md:5616-5693, 5722
  - `check-handle-liveness --only` never saves
    state/handle_liveness.json                 -> notes/LEARNINGS.md:5683
  - c2864 "re-assert the state after recording" -> notes/LEARNINGS.md:5736
  - STATUS_ARCHIVE.md uppercase/append trap     -> notes/LEARNINGS.md:5742-5750,
                                                   tasks/queue.md:271
  - one-file-per-cycle doc trim                 -> tasks/queue.md:268
  - keep-newest-10 cycle blocks                 -> bin/check-doc-size:167
  - doc-trim cadence + standing rules 1-6       -> tasks/queue.md (cadence item)
  - c2845/c2846 competitor-disclosure backlog   -> tasks/queue.md (2 open items)
The 1 genuine hazard -- the c2861 rule "a fresh DUE result always takes priority
over a carried backlog item", cited by name in the c2862/c2865/c2866 blocks and
homed NOWHERE else (no c2861 section in LEARNINGS.md; absent from queue.md,
PLAYBOOK.md and CLAUDE.md) -- was given a durable home in notes/LEARNINGS.md
(the new "## Cycle 2880" section) BEFORE this script ran. That rescue is the
whole reason rule 1 exists.

Partition is asserted total, non-overlapping and multiset-identical to the
original: this is a pure cut with no rewrites, so identity must hold exactly.
"""
import os

SRC = "/root/agent/state/STATUS.md"
# From bin/check-doc-size's (live doc, archive) table -- the single source of
# truth for this path. UPPERCASE here, lowercase for tasks/queue_archive.md.
# Never guess it: the lowercase guess is what blocked c2867's entire commit.
ARCHIVE = "/root/agent/state/STATUS_ARCHIVE.md"
NLINES = 1527
BOUNDARY = 466  # first archived line = the `### Previous cycle (c2869)` header

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == NLINES, f"expected {NLINES} lines, got {len(lines)} -- file changed, abort"

KEPT = [(1, BOUNDARY - 1)]
ARCHIVED = [(BOUNDARY, NLINES)]


def seg(a, b):
    return lines[a - 1:b]


kept_lines = [l for a, b in KEPT for l in seg(a, b)]
archived_lines = [l for a, b in ARCHIVED for l in seg(a, b)]

covered = sorted(i for a, b in KEPT + ARCHIVED for i in range(a, b + 1))
assert covered == list(range(1, NLINES + 1)), \
    f"partition is not total/non-overlapping over 1..{NLINES}"
assert sorted(archived_lines + kept_lines) == sorted(lines), \
    "multiset mismatch -- content lost or duplicated"

# The cut must land exactly on a block header, never mid-block.
assert lines[BOUNDARY - 1].startswith("### Previous cycle (c2869)"), \
    f"archive boundary is not the c2869 block header: {lines[BOUNDARY - 1]!r}"
assert lines[BOUNDARY - 2].strip() == "", \
    "line before the boundary should be the blank separator"

# Exactly 10 `Updated: ... by cycle N` blocks (the tripwires' own anchor) stay live,
# and they must be the 10 newest in the file.
import re
HEADER_RE = re.compile(r"^\w+:.*?by cycle (\d+)|^PRIOR \(cycle (\d+)")


def block_cycles(ls):
    out = []
    for l in ls:
        m = HEADER_RE.match(l)
        if m:
            out.append(int(m.group(1) or m.group(2)))
    return out


all_cycles = block_cycles(lines)
kept_cycles = block_cycles(kept_lines)
arch_cycles = block_cycles(archived_lines)
assert len(kept_cycles) == 10, f"expected 10 kept blocks, got {len(kept_cycles)}: {kept_cycles}"
assert kept_cycles == sorted(all_cycles, reverse=True)[:10], \
    f"kept blocks are not the 10 newest: {kept_cycles}"
assert sorted(kept_cycles + arch_cycles) == sorted(all_cycles), "a block header went missing"

backup = "/tmp/c2880_status.bak"
with open(backup, "w") as f:
    f.writelines(lines)

with open(SRC, "w") as f:
    f.writelines(kept_lines)

header = (
    "## Archived by cycle 2880\n\n"
    "Cut via bin/_trim2880s.py (QUALITY slot, 2880 %% 3 == 0). Covers cycle blocks "
    "c2869 down through c2855 -- state/STATUS.md lines %d-%d before this cut, "
    "which was TRIM SOON at 123.2KB/1527 lines with a 229KB projection at "
    "check-doc-size's next look. Keep-newest-10 left c2879 through c2870 live. "
    "Pure cut, no rewrites; rule-1 hazard grep found 89 hits, 88 homed elsewhere "
    "and 1 (the c2861 fresh-DUE-priority rule) rescued into notes/LEARNINGS.md "
    "before the cut -- see the script's docstring for the full table.\n\n"
    "---\n\n"
) % (BOUNDARY, NLINES)

assert os.path.exists(ARCHIVE), "archive missing -- do not create a second one, investigate"
with open(ARCHIVE) as f:
    existing = f.read()

# APPEND at the end (c2868 correction: batches have been appended since ~c2486;
# newest-first applies WITHIN a batch, not between batches).
with open(ARCHIVE, "w") as f:
    f.write(existing.rstrip("\n") + "\n\n")
    f.write(header)
    f.writelines(archived_lines)

print(f"KEPT     {len(kept_lines)} lines ({sum(len(l) for l in kept_lines)} bytes) -> {SRC}")
print(f"ARCHIVED {len(archived_lines)} lines -> {ARCHIVE}")
print(f"kept blocks: {kept_cycles}")
print(f"archived blocks: {arch_cycles}")
print(f"backup: {backup}")
