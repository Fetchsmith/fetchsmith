#!/usr/bin/env python3
"""c2964 proactive trim of state/STATUS.md (flagged TRIM SOON by check-doc-size this
cycle: 132.1KB/399 lines, ~15 cycles of headroom at +4510 B/cycle, projected 238KB at the
checker's next look 24c out -- so the next run reads TRIM DUE no matter what, and the
checker's own advice is to trim proactively in a QUALITY slot). 2964 is the QUALITY slot
(2964 = 3*988 exactly). Pure line cut, same method as bin/_trim2952s.py /
bin/_trim2940s.py: STATUS.md carries no interleaved open `- [ ]` items (asserted below),
so no hoisting or rewrite is needed, and multiset identity must hold exactly.

Ranges re-derived fresh this cycle (doc-trim rule 3, never paste forward): 22
`Updated: ... by cycle N` blocks live, c2963 (line 1) down through c2942 (line 390).
Headers are asserted to be in strict descending cycle order rather than assumed (rule-3's
sibling hazard). Keep-newest-10 (bin/check-doc-size's rule) -> keep c2963..c2954
(lines 1-175, i.e. through the `---` + blank separator that precedes c2953's header,
matching _trim2952s.py's boundary convention), archive c2953..c2942 (12 blocks, lines
176-399) verbatim to STATUS_ARCHIVE.md.

Rule-1 hazard grep runs FIRST over the archive-bound range and every hit is printed for
reading before the write happens. bin/check-status-blocks-kept (pre-commit) independently
verifies that no block present in HEAD vanished from live+archive.
"""
import os
import re
import sys

SRC = "/root/agent/state/STATUS.md"
ARCHIVE = "/root/agent/state/STATUS_ARCHIVE.md"
BACKUP = "/tmp/c2964_status.bak"
NLINES = 399
BOUNDARY = 176  # first archived line = the `Updated: ... by cycle 2953` block header

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

assert lines[BOUNDARY - 1].startswith("Updated: 2026-11-09 UTC by cycle 2953"), \
    f"archive boundary is not the c2953 block header: {lines[BOUNDARY - 1]!r}"
assert lines[BOUNDARY - 2].strip() == "", "line before the boundary should be blank"
assert lines[BOUNDARY - 3].strip() == "---", "expected the `---` separator above that blank"
assert lines[0].startswith("Updated: 2026-11-09 UTC by cycle 2963"), \
    f"L1 is not the c2963 block header: {lines[0][:60]!r}"

HEADER_RE = re.compile(r"^Updated:.*?by cycle (\d+)")


def block_cycles(ls):
    return [int(m.group(1)) for m in (HEADER_RE.match(l) for l in ls) if m]


all_cycles = block_cycles(lines)
kept_cycles = block_cycles(kept_lines)
arch_cycles = block_cycles(archived_lines)
assert len(all_cycles) == 22, f"expected 22 blocks live, got {len(all_cycles)}"
assert all_cycles == sorted(all_cycles, reverse=True), \
    f"blocks are NOT in descending cycle order -- re-derive the boundary: {all_cycles}"
assert len(kept_cycles) == 10, f"expected 10 kept blocks, got {len(kept_cycles)}: {kept_cycles}"
assert kept_cycles == sorted(all_cycles, reverse=True)[:10], \
    f"kept blocks are not the 10 newest: {kept_cycles}"
assert kept_cycles[0] == 2963 and kept_cycles[-1] == 2954, f"kept span wrong: {kept_cycles}"
assert sorted(kept_cycles + arch_cycles) == sorted(all_cycles), "a block header went missing"
# no open task items should exist in this file at all (they live in queue.md)
assert not any(l.startswith("- [ ] ") for l in lines), \
    "STATUS.md unexpectedly contains open `- [ ]` items -- use the hoist-then-cut method"

hazard = re.compile(r"standing|cadence|always |never |do not |must |\brule\b", re.I)
hits = [(BOUNDARY + i, l) for i, l in enumerate(archived_lines) if hazard.search(l)]
print(f"rule-1 hazard grep over {BOUNDARY}-{NLINES}: {len(hits)} hit(s)")
for i, l in hits:
    print(f"  L{i}: {l.rstrip()[:160]}")

if "--dry-run" in sys.argv:
    kb = sum(len(l) for l in kept_lines)
    print(f"\nDRY RUN: {sum(len(l) for l in lines)}B/{NLINES}ln -> {kb}B/{len(kept_lines)}ln "
          f"({sum(len(l) for l in lines) - kb}B saved)")
    print(f"kept blocks: {kept_cycles}")
    print(f"archived blocks: {arch_cycles}")
    sys.exit(0)

with open(BACKUP, "w") as f:
    f.writelines(lines)

with open(SRC, "w") as f:
    f.writelines(kept_lines)

header = (
    "## Archived by cycle 2964\n\n"
    "Cut via bin/_trim2964s.py (QUALITY slot, 2964 %% 3 == 0, 2964 = 3*988 exactly). Covers "
    "cycle blocks c2953 down through c2942 -- state/STATUS.md lines %d-%d before this cut, "
    "which read TRIM SOON at 132.1KB/399 lines with a 238KB projection at check-doc-size's "
    "next look (24c), i.e. guaranteed TRIM DUE next reading. Keep-newest-10 left c2963 "
    "through c2954 live. Pure cut, no rewrites; rule-1 hazard grep hits were all read "
    "before writing (see the script output recorded in state/STATUS.md's c2964 block).\n\n"
    "---\n\n"
) % (BOUNDARY, NLINES)

assert os.path.exists(ARCHIVE), "archive missing -- do not create a second one, investigate"
with open(ARCHIVE) as f:
    existing = f.read()
with open(ARCHIVE, "w") as f:
    f.write(existing.rstrip("\n") + "\n\n")
    f.write(header)
    f.writelines(archived_lines)

print(f"\nKEPT     {len(kept_lines)} lines ({sum(len(l) for l in kept_lines)} bytes) -> {SRC}")
print(f"ARCHIVED {len(archived_lines)} lines -> {ARCHIVE}")
print(f"kept blocks: {kept_cycles}")
print(f"archived blocks: {arch_cycles}")
print(f"backup: {BACKUP}")
