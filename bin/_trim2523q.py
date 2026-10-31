#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2523 (89.0KB / 947 lines).

Scheduled by c2520 (this is the next QUALITY/GROWTH slot, 2523%3==0) after
check-doc-size read TRIM SOON on queue.md this cycle (89.0KB/947 lines,
projected to cross the 200KB trim line before the checker's next automatic
look in 24c). Same c2161/.../c2511 HOIST-THEN-CUT method, not a line cut:
queue.md interleaves standing `- [ ] ` open items among completed `- [x]`
cycle blocks, so a naive line-number cut would silently delete live open
work.

  1. KEPT: the single most recent DONE block (cycle 2522, lines 1-46) --
     the file is NOT strictly newest-first throughout (items get edited to
     DONE in place rather than moved to the top), so "most recent" is by
     cycle number, not position; 2522 happens to already sit at the top.
  2. HOISTED: every genuinely-still-open `- [ ]` item, verbatim, in source
     order (22 ranges) -- the doc-trim cadence note (this script's own
     trigger, rewritten c2520), the enum_audit backlog pointer + its
     superseded-method predecessor (kept for context, still literally
     marked open), the c2478 Apify /v2/store 2026-11-15 deadline item, the
     c2464 HIGH rung-pricer note + TRIVIAL build-endpoint note, the c2492
     MEDIUM clean_streak item, the c2456/c2396/c2392/c2388/c2385 LOW gated
     follow-ups, the c2383 standing method note, the c2380 growing-niches
     rotation, the c2336 standing tripwire, c2332 feed-pickup, c2312
     scholarship-scraper unpushed fix, the process lesson on code+copy
     pushes, c2196, c2168/c2268, c2371 DMARC, and the c2120 standing
     process lesson.
  3. ARCHIVED: every other DONE/CLOSED block, verbatim, in original order
     -- none of them is the only home of a cadence instruction (checked by
     reading all of them: every interval/next-due reference they carry is
     already tracked in state/fleet_checks.json's own per-check notes).

Every one of the file's 947 lines is assigned to exactly one bucket; the
script asserts this partition is total and exhaustive before writing.
"""
import sys

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 947, f"expected 947 lines, got {len(lines)} -- file changed, abort"


def seg(a, b):
    return lines[a - 1:b]


KEPT = [(1, 46)]
HOISTED = [(481, 506), (532, 584), (585, 634), (635, 645), (646, 662),
           (663, 669), (670, 692), (693, 703), (711, 722), (723, 735),
           (736, 751), (752, 759), (760, 768), (769, 808), (809, 843),
           (844, 869), (870, 892), (893, 898), (899, 907), (908, 927),
           (928, 942), (943, 947)]
ARCHIVED = [(47, 120), (121, 159), (160, 209), (210, 256), (257, 298),
            (299, 340), (341, 367), (368, 392), (393, 413), (414, 444),
            (445, 463), (464, 480), (507, 531), (704, 710)]

checks = [
    (1, "- [x] **DONE cycle 2522"), (481, "- [ ] **doc-trim cadence (orig. c2508"),
    (532, "- [ ] **`enum_audit` backlog -- now has a REAL tool"),
    (585, "- [ ] **(superseded screening method, kept for context)"),
    (635, "- [ ] **NEW (c2478, MEDIUM, deadline 2026-11-15"),
    (646, "- [ ] **NEW follow-up (c2464, HIGH"), (663, "- [ ] **NEW note (c2464, TRIVIAL"),
    (670, "- [ ] **NEW follow-up (c2492, MEDIUM"), (693, "- [ ] **NEW follow-up (c2456, LOW"),
    (711, "- [ ] **NEW (c2396, LOW priority"), (723, "- [ ] **NEW follow-up (c2392, LOW priority"),
    (736, "- [ ] **NEW follow-up (c2388, LOW"), (752, "- [ ] **NEW follow-up (c2385, low priority"),
    (760, "- [ ] **STANDING METHOD (c2383)"), (769, "- [ ] **FOLLOW-UP from c2380"),
    (809, "- [ ] **NEW STANDING TRIPWIRE (c2336)"), (844, "- [ ] **UPDATED (c2517) follow-up (orig. c2332)"),
    (870, "- [ ] **NEW follow-up (c2312)"), (893, "- [ ] **Process lesson to apply on any cycle that changes BOTH"),
    (899, "- [ ] **NEW follow-up (c2196)"), (908, "- [ ] **NEW follow-up (c2168, REWRITTEN c2268"),
    (928, "- [ ] **NEW follow-up (c2371)"), (943, "- [ ] **Process lesson to apply every cycle (found c2120)"),
    (47, "- [x] **DONE cycle 2521"), (121, "- [x] **DONE cycle 2520 (QUALITY/GROWTH slot"),
    (160, "- [x] **DONE cycle 2519"), (210, "- [x] **DONE cycle 2518"),
    (257, "- [x] **DONE cycle 2517"), (299, "- [x] **DONE cycle 2516"),
    (341, "- [x] **DONE cycle 2515"), (368, "- [x] **DONE cycle 2514"),
    (393, "- [x] **DONE cycle 2513"), (414, "- [x] **DONE cycle 2512"),
    (445, "- [x] **DONE cycle 2511"), (464, "- [x] **DONE cycle 2510"),
    (507, "- [x] **DONE cycle 2520 (orig. c2504"), (704, "- [x] **CLOSED (verified cycle 2517)"),
]
for a, prefix in checks:
    assert seg(a, a)[0].startswith(prefix), f"block at {a} moved: {seg(a, a)[0][:80]!r}"

ALL_BUCKETS = {"KEPT": KEPT, "HOISTED": HOISTED, "ARCHIVED": ARCHIVED}

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
archived_txt = joinsegs(ARCHIVED)

reconstructed = kept_txt + hoisted_txt + archived_txt
if "".join(sorted(reconstructed.splitlines(keepends=True))) != "".join(sorted(lines)):
    sys.exit("FAIL: kept+hoisted+archived does not multiset-match the original file")

with open(ARCHIVE) as f:
    old_archive = f.read()

archive_header = (
    "\n## Archived by cycle 2523 (sonnet-5), 2026-10-31 -- queue.md had grown to 947 lines / "
    "89.0KB, flagged TRIM SOON this cycle and projected to cross TRIM DUE (216KB) before "
    "check-doc-size's next look (24c); trimmed proactively per the c2520 schedule. "
    "Hoist-then-cut method (not a line cut): every genuinely-open `- [ ] ` item was hoisted to "
    "the live file verbatim in source order (22 ranges, listed in bin/_trim2523q.py), the "
    "single most recent DONE block (cycle 2522) was kept live, and every other DONE/CLOSED "
    "block was archived -- none of them is the only home of a cadence instruction (checked each "
    "one: every next-due/interval reference they carry is already tracked in "
    "state/fleet_checks.json's per-check notes).\n\n"
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
