#!/usr/bin/env python3
"""c2940 QUALITY-slot trim of state/STATUS.md (flagged TRIM SOON by check-doc-size this
cycle: 135.6KB/471 lines, ~15 cycles of headroom at +4510 B/cycle, projected 241KB at
the checker's next look 24c out -- so the next run reads TRIM DUE no matter what).
Pure line cut, same method as bin/_trim2922s.py / _trim2904s.py: STATUS.md carries no
interleaved open `- [ ]` items, so no hoisting or rewrite is needed.

Ranges re-derived fresh this cycle (doc-trim rule 3, never paste forward): 28
`Updated: ... by cycle N` blocks live, c2939 (line 1) down through c2912 (line 450).
Headers are in strict descending cycle order in this file today (verified by assert
below, not assumed -- rule-3's sibling hazard). Keep-newest-10 (bin/check-doc-size
rule) -> keep c2939..c2930 (lines 1-166, i.e. through the `---` + blank separator that
precedes c2929's header, matching _trim2922s.py's boundary convention), archive
c2929..c2912 (18 blocks, lines 167-471) verbatim to STATUS_ARCHIVE.md.

Rule-1 hazard grep runs FIRST over the archive-bound range, pattern
`standing|cadence|always |never |do not |must |\\brule\\b` (case-insensitive). Every
hit is printed for reading before the write happens.

Partition asserted total, non-overlapping, multiset-identical to the original (pure
cut, no rewrites -- identity must hold exactly).
"""
import os
import re
import sys

SRC = "/root/agent/state/STATUS.md"
ARCHIVE = "/root/agent/state/STATUS_ARCHIVE.md"
BACKUP = "/tmp/c2940_status.bak"
NLINES = 471
BOUNDARY = 167  # first archived line = the `Updated: ... by cycle 2929` block header

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

assert lines[BOUNDARY - 1].startswith("Updated: 2026-11-09 UTC by cycle 2929"), \
    f"archive boundary is not the c2929 block header: {lines[BOUNDARY - 1]!r}"
assert lines[BOUNDARY - 2].strip() == "", "line before the boundary should be blank"
assert lines[BOUNDARY - 3].strip() == "---", "expected the `---` separator above that blank"

HEADER_RE = re.compile(r"^Updated:.*?by cycle (\d+)")


def block_cycles(ls):
    return [int(m.group(1)) for m in (HEADER_RE.match(l) for l in ls) if m]


all_cycles = block_cycles(lines)
kept_cycles = block_cycles(kept_lines)
arch_cycles = block_cycles(archived_lines)
assert len(all_cycles) == 28, f"expected 28 blocks live, got {len(all_cycles)}"
assert len(kept_cycles) == 10, f"expected 10 kept blocks, got {len(kept_cycles)}: {kept_cycles}"
assert kept_cycles == sorted(all_cycles, reverse=True)[:10], \
    f"kept blocks are not the 10 newest: {kept_cycles}"
assert sorted(kept_cycles + arch_cycles) == sorted(all_cycles), "a block header went missing"

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
    "## Archived by cycle 2940\n\n"
    "Cut via bin/_trim2940s.py (QUALITY slot, 2940 %% 3 == 0). Covers cycle blocks c2929 "
    "down through c2912 -- state/STATUS.md lines %d-%d before this cut, which read TRIM "
    "SOON at 135.6KB/471 lines with a 241KB projection at check-doc-size's next look "
    "(24c). Keep-newest-10 left c2939 through c2930 live. Pure cut, no rewrites; rule-1 "
    "hazard grep hits were all read before writing (see the script output recorded in "
    "state/STATUS.md's c2940 block).\n\n"
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
