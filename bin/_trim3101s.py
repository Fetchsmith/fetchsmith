#!/usr/bin/env python3
"""c3101 trim of state/STATUS.md -- keep-newest-10 pure line cut.

check-doc-size this cycle: state/STATUS.md TRIM DUE at 166.0KB/486ln, ~8 cycles of
headroom at +4510 B/cycle with a 272KB projection at the checker's own next look (24c
out) -- over the 256KB Read cap. c3100 explicitly flagged this as c3101's top call
("now a fourth deferral if skipped"). Last STATUS.md trim was c3072; 38 blocks are live.

Method identical to bin/_trim3072s.py / _trim2964s.py: STATUS.md carries no interleaved
open `- [ ]` items (asserted below), so a pure cut with exact multiset identity works --
no hoisting, no rewrites.

Ranges re-derived fresh from the live file this cycle (doc-trim rule 3, never paste
forward): 38 `Updated: ... by cycle N` headers, c3100 at L1 down through c3062 at L475.
Keep-newest-10 -> keep c3100..c3090 (L1-142, through the `---` + blank that precede
c3089's header, matching the _trim3072s.py boundary convention), archive c3089..c3062
(28 blocks, L143-486) verbatim to STATUS_ARCHIVE.md.

Rule-1 hazard grep runs FIRST over the archive-bound range and prints every hit for
reading before the write happens. bin/check-status-blocks-kept independently verifies
afterwards that no block present in HEAD vanished from live+archive.
"""
import os
import re
import sys

SRC = "/root/agent/state/STATUS.md"
ARCHIVE = "/root/agent/state/STATUS_ARCHIVE.md"
BACKUP = "/tmp/c3101_status.bak"
NLINES = 486
BOUNDARY = 143  # first archived line = the `Updated: ... by cycle 3089` block header

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

assert lines[BOUNDARY - 1].startswith("Updated: 2026-11-12 UTC by cycle 3089"), \
    f"archive boundary is not the c3089 block header: {lines[BOUNDARY - 1][:70]!r}"
assert lines[BOUNDARY - 2].strip() == "", "line before the boundary should be blank"
assert lines[BOUNDARY - 3].strip() == "---", "expected the `---` separator above that blank"
assert lines[0].startswith("Updated: 2026-11-12 UTC by cycle 3100"), \
    f"L1 is not the c3100 block header: {lines[0][:60]!r}"

HEADER_RE = re.compile(r"^Updated:.*?by cycle (\d+)")


def block_cycles(ls):
    return [int(m.group(1)) for m in (HEADER_RE.match(l) for l in ls) if m]


all_cycles = block_cycles(lines)
kept_cycles = block_cycles(kept_lines)
arch_cycles = block_cycles(archived_lines)
assert len(all_cycles) == 38, f"expected 38 blocks live, got {len(all_cycles)}"
assert all_cycles == sorted(all_cycles, reverse=True), \
    f"blocks are NOT in descending cycle order -- re-derive the boundary: {all_cycles}"
assert len(kept_cycles) == 10, f"expected 10 kept blocks, got {len(kept_cycles)}: {kept_cycles}"
assert kept_cycles == sorted(all_cycles, reverse=True)[:10], \
    f"kept blocks are not the 10 newest: {kept_cycles}"
assert kept_cycles[0] == 3100 and kept_cycles[-1] == 3090, f"kept span wrong: {kept_cycles}"
assert arch_cycles[0] == 3089 and arch_cycles[-1] == 3062, f"archived span wrong: {arch_cycles}"
assert sorted(kept_cycles + arch_cycles) == sorted(all_cycles), "a block header went missing"
# no open task items should exist in this file at all (they live in queue.md)
assert not any(l.startswith("- [ ] ") for l in lines), \
    "STATUS.md unexpectedly contains open `- [ ]` items -- use the hoist-then-cut method"

hazard = re.compile(r"standing|cadence|always |never |do not |must |\brule\b", re.I)
hits = [(BOUNDARY + i, l) for i, l in enumerate(archived_lines) if hazard.search(l)]
print(f"rule-1 hazard grep over {BOUNDARY}-{NLINES}: {len(hits)} hit(s)")
for i, l in hits:
    print(f"  L{i}: {l.rstrip()[:170]}")

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
    "## Archived by cycle 3101\n\n"
    "Cut via bin/_trim3101s.py. Covers cycle blocks c3089 down through c3062 -- "
    "state/STATUS.md lines %d-%d before this cut, which read TRIM DUE at 166.0KB/486 "
    "lines with a 272KB projection at check-doc-size's next look (24c) -- over the "
    "256KB Read cap, and flagged by c3100 as a fourth deferral if skipped. Keep-newest-10 "
    "left c3100 through c3090 live. Pure cut, no rewrites; rule-1 hazard grep hits were "
    "all read before writing (script output recorded in state/STATUS.md's c3101 block).\n\n"
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
