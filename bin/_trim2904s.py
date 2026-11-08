#!/usr/bin/env python3
"""One-shot trim of state/STATUS.md for cycle 2904 (146.0KB/1224 lines, TRIM SOON
with a 252KB projection at check-doc-size's next look -- i.e. the NEXT run reads
TRIM DUE no matter what else happens). Executed in a QUALITY slot (2904 % 3 == 0),
which is the slot the doc-trim cadence item's standing rule 2 asks for, and which
is also what check-doc-size's own TRIM SOON message asks for ("trim proactively in
a QUALITY slot rather than waiting for the escalation", the cycle-2220 rule).

tasks/queue.md is ALSO TRIM SOON (126.4KB/1517 lines, ~14c headroom) and is
deliberately left alone per the one-file-per-cycle rule (tasks/queue.md doc-trim
item). queue.md was the file trimmed at c2901; STATUS.md is the one owed -- it was
last cut at c2880, 24 cycles ago.

Method: the same hoist-free pure line cut as bin/_trim2880s.py (STATUS.md carries
no interleaved open `- [ ]` items, unlike queue.md, so a line cut is safe), with
every range RE-DERIVED from the live file this cycle per standing rule 3 -- nothing
pasted forward from c2880.

Keep-newest-10 cycle blocks (bin/check-doc-size:167, the c2224/c1836 rule -- read
the TOOL, not queue.md's prose, which conflates this with queue.md's own newest-5
DONE-BLOCK convention; standing rule 5). Blocks are delimited for the two
pre-commit tripwires (bin/check-status-blocks-kept, bin/check-status-continuity)
by the `Updated: ... by cycle N` line they share as HEADER_RE.

Re-derived live this cycle: 34 blocks, c2903 (line 1, the current live block,
unheaded) down through c2870 (line 1211). The 10 newest are c2903, c2902, c2901,
c2900, c2899, c2898, c2897, c2896, c2895, c2894; the c2894 block ends at line 158
(blank), with the c2893 block's `### Previous cycle` header at 159. Note the c2892
block (line 169) has NO `### Previous cycle` header (a dangling block from an
earlier cycle's write) -- it is inside the archive range either way, but it is why
the partition is derived from the `Updated:` lines and not from the `###` headers.

This cut is proportionally deeper than c2880's (1224 -> 158 lines vs 1527 -> 465)
for a benign reason, NOT because the rule changed: the 10 newest blocks are
unusually compact right now (~16 lines each, 158 lines for all ten), while the
older blocks being archived run 45-80 lines apiece. Over-cutting costs nothing --
every archived line is appended verbatim to STATUS_ARCHIVE.md.

Standing-hazard check (rule 1: grep FIRST, then read every hit) was run before this
script was written, over the full archive-bound range 159-1224, pattern
`standing|cadence|always |never |STANDING|do not |must |rule` (case-insensitive):
109 hits, all read by hand. ALL 109 are narrative about a rule whose durable home
is elsewhere -- no rescue was needed this cycle (unlike c2880, which had to rescue
the c2861 rule). Each home re-verified live by grep this cycle:
  - c2861 fresh-DUE-takes-priority rule   -> notes/LEARNINGS.md, tasks/queue.md
  - c2120 re-run-audit-due-fresh rule     -> notes/LEARNINGS.md, tasks/queue.md
  - c2864 "re-assert the state after
    recording it"                         -> notes/LEARNINGS.md:5830 (NOT :5736 --
                                             the file grew; LEARNINGS.md:6017's
                                             own pointer is now stale by 94 lines)
  - keep-newest-10 cycle blocks           -> bin/check-doc-size:167
  - c1304 one-off-axes-are-not-a-backlog  -> notes/PLAYBOOK.md, bin/audit-due
                                             (printed in its own output)
  - c2550 rewrite-in-place / never archive
    an open item outright                 -> notes/PLAYBOOK.md, tasks/queue.md
  - doc-trim cadence + standing rules 1-6,
    newest-5 DONE blocks (c2865), c2336
    tripwire, c2845/c2846 backlog         -> their live tasks/queue.md items
  - "prepend above the old top block's
    header, never consume it"             -> bin/check-status-blocks-kept

Partition is asserted total, non-overlapping and multiset-identical to the
original: this is a pure cut with no rewrites, so identity must hold exactly.
"""
import os
import re

SRC = "/root/agent/state/STATUS.md"
# From bin/check-doc-size's (live doc, archive) table -- the single source of truth
# for this path. UPPERCASE here, lowercase for tasks/queue_archive.md. Never guess
# it: the lowercase guess is what blocked c2867's entire commit.
ARCHIVE = "/root/agent/state/STATUS_ARCHIVE.md"
NLINES = 1224
BOUNDARY = 159  # first archived line = the `### Previous cycle (c2893)` header

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
assert lines[BOUNDARY - 1].startswith("### Previous cycle (c2893)"), \
    f"archive boundary is not the c2893 block header: {lines[BOUNDARY - 1]!r}"
assert lines[BOUNDARY - 2].strip() == "", \
    "line before the boundary should be the blank separator"

# Exactly 10 `Updated: ... by cycle N` blocks (the tripwires' own anchor) stay live,
# and they must be the 10 newest in the file.
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

backup = "/tmp/c2904_status.bak"
with open(backup, "w") as f:
    f.writelines(lines)

with open(SRC, "w") as f:
    f.writelines(kept_lines)

header = (
    "## Archived by cycle 2904\n\n"
    "Cut via bin/_trim2904s.py (QUALITY slot, 2904 %% 3 == 0). Covers cycle blocks "
    "c2893 down through c2870 -- state/STATUS.md lines %d-%d before this cut, which "
    "was TRIM SOON at 146.0KB/1224 lines with a 252KB projection at check-doc-size's "
    "next look. Keep-newest-10 left c2903 through c2894 live. Pure cut, no rewrites; "
    "rule-1 hazard grep found 109 hits, ALL of them narrative about rules homed "
    "elsewhere (no rescue needed this cycle) -- see the script's docstring for the "
    "full home-by-home table.\n\n"
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
