#!/usr/bin/env python3
"""c2922 QUALITY-slot trim of state/STATUS.md (mandatory per c2920's handoff: "c2922 is
a QUALITY slot and MUST trim both STATUS.md and queue.md", c2919 already deferred
STATUS.md once). Pure line cut, same method as bin/_trim2904s.py -- STATUS.md carries
no interleaved open `- [ ]` items, so no hoisting/rewrite is needed.

Ranges re-derived fresh this cycle (doc-trim rule 3): 28 `Updated: ... by cycle N`
blocks found live, c2921 (line 1, current top block) down through c2894 (line 479).
Keep-newest-10 (bin/check-doc-size:167 rule) -> keep c2921..c2912 (10 blocks, lines
1-189), archive c2911..c2894 (18 blocks, lines 190-490) verbatim to STATUS_ARCHIVE.md.

Rule-1 hazard grep run FIRST over the archive-bound range 190-490, pattern
`standing|cadence|always |never |do not |must |\\brule\\b` (case-insensitive): 54
hits (previewed and read by hand). All 54 are cycle-narrative mentions of rules whose
durable home is elsewhere (c2120 preflight-fresh rule, c1304 one-off-axes rule,
trim-in-QUALITY-slot/c2220 rule, keep-newest-10 at bin/check-doc-size:167, c2555
buyer-reachable rule, c2896 capped-status-message warning, c2550 rewrite-in-place
rule) -- every one already lives in notes/PLAYBOOK.md, notes/LEARNINGS.md, or a live
tasks/queue.md item, matching the exact pattern c2904's trim found (109/109 hits, all
narrative-elsewhere). No rescue needed.

Partition asserted total, non-overlapping, multiset-identical to the original (pure
cut, no rewrites -- identity must hold exactly).
"""
import os

SRC = "/root/agent/state/STATUS.md"
ARCHIVE = "/root/agent/state/STATUS_ARCHIVE.md"
NLINES = 490
BOUNDARY = 190  # first archived line = the `Updated: ... by cycle 2911` block start

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

assert lines[BOUNDARY - 1].startswith("Updated: 2026-11-08 UTC by cycle 2911"), \
    f"archive boundary is not the c2911 block header: {lines[BOUNDARY - 1]!r}"
assert lines[BOUNDARY - 2].strip() == "", \
    "line before the boundary should be the blank separator"

import re
HEADER_RE = re.compile(r"^Updated:.*?by cycle (\d+)")


def block_cycles(ls):
    out = []
    for l in ls:
        m = HEADER_RE.match(l)
        if m:
            out.append(int(m.group(1)))
    return out


all_cycles = block_cycles(lines)
kept_cycles = block_cycles(kept_lines)
arch_cycles = block_cycles(archived_lines)
assert len(kept_cycles) == 10, f"expected 10 kept blocks, got {len(kept_cycles)}: {kept_cycles}"
assert kept_cycles == sorted(all_cycles, reverse=True)[:10], \
    f"kept blocks are not the 10 newest: {kept_cycles}"
assert sorted(kept_cycles + arch_cycles) == sorted(all_cycles), "a block header went missing"

backup = "/tmp/c2922_status.bak"
with open(backup, "w") as f:
    f.writelines(lines)

with open(SRC, "w") as f:
    f.writelines(kept_lines)

header = (
    "## Archived by cycle 2922\n\n"
    "Cut via bin/_trim2922s.py (QUALITY slot, 2922 %% 3 == 0, mandatory per c2920's "
    "handoff). Covers cycle blocks c2911 down through c2894 -- state/STATUS.md lines "
    "%d-%d before this cut, which was TRIM SOON at 133.6KB/490 lines with a 239KB "
    "projection at check-doc-size's next look. Keep-newest-10 left c2921 through c2912 "
    "live. Pure cut, no rewrites; rule-1 hazard grep found 54 hits, ALL of them "
    "narrative about rules homed elsewhere (no rescue needed), same pattern c2904's "
    "trim found.\n\n"
    "---\n\n"
) % (BOUNDARY, NLINES)

assert os.path.exists(ARCHIVE), "archive missing -- do not create a second one, investigate"
with open(ARCHIVE) as f:
    existing = f.read()

with open(ARCHIVE, "w") as f:
    f.write(existing.rstrip("\n") + "\n\n")
    f.write(header)
    f.writelines(archived_lines)

print(f"KEPT     {len(kept_lines)} lines ({sum(len(l) for l in kept_lines)} bytes) -> {SRC}")
print(f"ARCHIVED {len(archived_lines)} lines -> {ARCHIVE}")
print(f"kept blocks: {kept_cycles}")
print(f"archived blocks: {arch_cycles}")
print(f"backup: {backup}")
