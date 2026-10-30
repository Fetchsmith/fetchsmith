#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2486 (112.2KB / 1247 lines).

Same trigger as this cycle's STATUS.md trim (bin/_trim2486.py): check-doc-size
flagged TRIM SOON on both files at c2483/c2484/c2485 without yet escalating to
DUE, and the c2485 handoff asked this QUALITY/GROWTH slot to trim proactively.
Uses the c2161/.../c2459 HOIST-THEN-CUT method, not a line cut: queue.md
interleaves standing `- [ ]` open items among completed `- [x]` cycle blocks,
so a naive line-number cut would silently delete live open work.

  1. KEPT: the single most recent DONE block (cycle 2485, lines 1-28).
  2. HOISTED: every genuinely-still-open `- [ ]` item, verbatim, in source
     order (23 ranges) -- the c2478 Apify /v2/store deadline item, the c2484
     README-lead-claim generalisation, the c2464 HIGH scalar-vs-rung port
     note, the c2464 TRIVIAL build-endpoint note, the standing
     `competitor_audit` backlog pointer (UPDATED, MEDIUM), the c2475/c2472
     LOW audit-note-scan items, the c2456/c2436/c2396/c2392/c2388/c2385 LOW
     gated follow-ups, the c2383 standing method note, the c2380 ACTIVE
     growing-niches rotation, the c2336 standing tripwire, c2332, the c2312
     UNPUSHED-code-fix item, the two standing process lessons, c2196,
     c2168/c2268, and c2371 DMARC.
  3. DROPPED: the c2483 doc-trim follow-up (lines 549-558) that asked for
     exactly this trim -- not carried forward, since this cycle's own new
     DONE block (prepended after this script runs) records it closed.
  4. CLOSED_UNCHECKED (archived, not hoisted, same treatment as prior trims):
     the c2467-superseded STALE item (956-981) and the c2396 CLOSED
     groupBy-aggregates note (994-1007), both of which say in their own text
     not to act on them again.
  5. ARCHIVED: every other DONE cycle block, verbatim, in original order.

Every one of the file's 1247 lines is assigned to exactly one bucket; the
script asserts this partition is total and exhaustive before writing.
"""
import sys

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 1247, f"expected 1247 lines, got {len(lines)} -- file changed, abort"


def seg(a, b):
    return lines[a - 1:b]


KEPT = [(1, 28)]
HOISTED = [(29, 34), (35, 51), (340, 356), (392, 398), (534, 548), (591, 601),
           (602, 614), (709, 719), (843, 853), (982, 993), (1008, 1020),
           (1021, 1036), (1037, 1044), (1045, 1053), (1054, 1093),
           (1121, 1155), (1156, 1169), (1170, 1192), (1193, 1198),
           (1199, 1207), (1208, 1227), (1228, 1242), (1243, 1247)]
DROPPED = [(549, 558)]
CLOSED_UNCHECKED = [(956, 981), (994, 1007)]
ARCHIVED_DONE = [(52, 90), (91, 121), (122, 142), (143, 178), (179, 194),
                 (195, 226), (227, 260), (261, 292), (293, 310), (311, 339),
                 (357, 391), (399, 425), (426, 450), (451, 483), (484, 498),
                 (499, 515), (516, 533), (559, 590), (615, 640), (641, 646),
                 (647, 672), (673, 708), (720, 726), (727, 773), (774, 816),
                 (817, 842), (854, 899), (900, 913), (914, 955), (1094, 1116),
                 (1117, 1120)]

checks = [
    (1, "- [x] **DONE cycle 2485"), (29, "- [ ] **NEW (c2478, MEDIUM, deadline 2026-11-15"),
    (35, "- [ ] **NEW (c2484, LOW-MEDIUM, cheap)"), (340, "- [ ] **NEW follow-up (c2464, HIGH"),
    (392, "- [ ] **NEW note (c2464, TRIVIAL"), (534, "- [ ] **UPDATED follow-up (MEDIUM"),
    (549, "- [ ] **NEW follow-up (c2483, LOW-MEDIUM"), (591, "- [ ] **NEW follow-up (c2475, LOW"),
    (602, "- [ ] **NEW follow-up (c2472, LOW"), (709, "- [ ] **NEW follow-up (c2456, LOW, gated"),
    (843, "- [ ] **NEW follow-up (c2436, LOW"), (956, "- [ ] **STALE, superseded by the c2467 entry"),
    (982, "- [ ] **NEW (c2396, LOW priority"), (994, "- [ ] **CLOSED by c2396"),
    (1008, "- [ ] **NEW follow-up (c2392, LOW priority"), (1021, "- [ ] **NEW follow-up (c2388, LOW"),
    (1037, "- [ ] **NEW follow-up (c2385, low priority"), (1045, "- [ ] **STANDING METHOD (c2383)"),
    (1054, "- [ ] **FOLLOW-UP from c2380"), (1121, "- [ ] **NEW STANDING TRIPWIRE (c2336)"),
    (1156, "- [ ] **NEW follow-up (c2332)"), (1170, "- [ ] **NEW follow-up (c2312)"),
    (1193, "- [ ] **Process lesson to apply on any cycle that changes BOTH"),
    (1199, "- [ ] **NEW follow-up (c2196)"), (1208, "- [ ] **NEW follow-up (c2168, REWRITTEN c2268"),
    (1228, "- [ ] **NEW follow-up (c2371)"), (1243, "- [ ] **Process lesson to apply every cycle (found c2120)"),
    (52, "- [x] **DONE cycle 2484"), (91, "- [x] **DONE cycle 2482"), (122, "- [x] **DONE cycle 2481"),
    (143, "- [x] **DONE cycle 2480"), (179, "- [x] **DONE cycle 2479"), (195, "- [x] **DONE cycle 2477"),
    (227, "- [x] **DONE cycle 2476"), (261, "- [x] **DONE cycle 2470"), (293, "- [x] **DONE cycle 2469"),
    (311, "- [x] **DONE cycle 2464"), (357, "- [x] **DONE cycle 2466"), (399, "- [x] **DONE cycle 2461"),
    (426, "- [x] **DONE cycle 2460"), (451, "- [x] **DONE cycle 2472"), (484, "- [x] **DONE cycle 2473"),
    (499, "- [x] **DONE cycle 2474"), (516, "- [x] **DONE cycle 2475"), (559, "- [x] **DONE cycle 2483"),
    (615, "- [x] **DONE cycle 2459"), (641, "- [x] **DONE cycle 2457"), (647, "- [x] **DONE cycle 2457"),
    (673, "- [x] **DONE cycle 2456"), (720, "- [x] **DONE cycle 2457"), (727, "- [x] **DONE cycle 2455"),
    (774, "- [x] **DONE cycle 2454"), (817, "- [x] **DONE cycle 2458"), (854, "- [x] **DONE cycle 2462"),
    (900, "- [x] **DONE cycle 2463"), (914, "- [x] **DONE cycle 2467"), (1094, "- [x] **DONE cycle 2465"),
    (1117, "- [x] **RAN cycle 2471"),
]
for a, prefix in checks:
    assert seg(a, a)[0].startswith(prefix), f"block at {a} moved: {seg(a, a)[0][:80]!r}"

ALL_BUCKETS = {"KEPT": KEPT, "HOISTED": HOISTED, "DROPPED": DROPPED,
               "CLOSED_UNCHECKED": CLOSED_UNCHECKED, "ARCHIVED_DONE": ARCHIVED_DONE}

owner = {}
for name, ranges in ALL_BUCKETS.items():
    for a, b in ranges:
        for i in range(a, b + 1):
            assert i not in owner, f"line {i} claimed by both {owner[i]} and {name}"
            owner[i] = name

missing = [i for i in range(1, len(lines) + 1) if i not in owner]
assert not missing, f"lines not accounted for ({len(missing)}): {missing[:20]}..."

def joinsegs(ranges):
    return "".join(l for r in ranges for l in seg(*r))


kept_txt = joinsegs(KEPT)
hoisted_txt = joinsegs(HOISTED)
dropped_txt = joinsegs(DROPPED)
closed_txt = joinsegs(CLOSED_UNCHECKED)
archived_done_txt = joinsegs(ARCHIVED_DONE)
archived_txt = closed_txt + archived_done_txt

reconstructed = kept_txt + hoisted_txt + dropped_txt + archived_txt
if "".join(sorted(reconstructed.splitlines(keepends=True))) != "".join(sorted(lines)):
    sys.exit("FAIL: kept+hoisted+dropped+archived does not multiset-match the original file")

with open(ARCHIVE) as f:
    old_archive = f.read()

archive_header = (
    "\n## Archived by cycle 2486 (sonnet-5), 2026-10-30 -- queue.md had grown to 1247 lines / "
    "112.2KB, past the point check-doc-size flagged TRIM SOON at c2483/c2484/c2485 without yet "
    "escalating to DUE; trimmed proactively per the c2485 handoff. Hoist-then-cut method (not a "
    "line cut): every genuinely-open `- [ ] ` item was hoisted to the live file verbatim in "
    "source order (23 ranges, listed in bin/_trim2486q.py), the single most recent DONE block "
    "(cycle 2485) was kept live, and two items that explicitly mark themselves STALE/CLOSED in "
    "their own text were archived rather than hoisted (the c2483 trim follow-up this cycle "
    "itself closes was dropped, not archived, since it would be pure noise once closed).\n\n"
)
new_archive = old_archive + archive_header + archived_txt
new_live = kept_txt + hoisted_txt

with open(SRC, "w") as f:
    f.write(new_live)
with open(ARCHIVE, "w") as f:
    f.write(new_archive)

print(f"queue.md: {len(lines)} -> {len(new_live.splitlines())} lines "
      f"({len(''.join(lines))} -> {len(new_live)} bytes)")
print(f"Archived {len(archived_txt.splitlines())} lines to {ARCHIVE}")
print(f"Dropped (superseded by this cycle's own new entry): {len(dropped_txt.splitlines())} lines")
