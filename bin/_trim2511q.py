#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2511 (85.7KB / 932 lines).

Same trigger as this cycle's STATUS.md trim (bin/_trim2511.py): check-doc-size
flagged TRIM SOON on both files this cycle, projected to cross TRIM DUE
before the checker's next look (24c), and c2510's handoff asked this
QUALITY/GROWTH slot (2511%3==0) to trim proactively. Uses the
c2161/.../c2486 HOIST-THEN-CUT method, not a line cut: queue.md interleaves
standing `- [ ] ` open items among completed `- [x]` cycle blocks, so a naive
line-number cut would silently delete live open work.

  1. KEPT: the single most recent DONE block (cycle 2510, lines 1-17) --
     the file is NOT strictly newest-first throughout (items get edited to
     DONE in place rather than moved to the top), so "most recent" is by
     cycle number, not position; 2510 happens to already sit at the top.
  2. HOISTED: every genuinely-still-open `- [ ]` item, verbatim, in source
     order (23 ranges) -- the c2508 doc-trim follow-up (closed by this
     cycle's own new entry, but not dropped since THIS script runs before
     that entry is written), the c2504 set-example-input note, the
     enum_audit backlog pointer, the c2478 Apify /v2/store deadline item,
     the c2464 HIGH scalar-vs-rung port note + TRIVIAL build-endpoint note,
     the c2492 MEDIUM clean_streak vocabulary item, the c2456/c2436/c2396/
     c2392/c2388/c2385 LOW gated follow-ups, the c2383 standing method note,
     the c2380 ACTIVE growing-niches rotation, the c2336 standing tripwire,
     c2332, the c2312 UNPUSHED-code-fix item, the process lesson on
     code+copy pushes, c2196, c2168/c2268, c2371 DMARC, and the c2120
     standing process lesson.
  3. ARCHIVED: every other DONE/CLOSED/WON'T-FIX block, verbatim, in
     original order -- none of them is the only home of a cadence
     instruction (checked by reading all of them: every interval/cadence
     they reference is already tracked in state/fleet_checks.json or
     state/audit_dates.json, or -- for the two c2492 WON'T-FIX decisions --
     already duplicated as a comment in bin/audit-due itself).

Every one of the file's 932 lines is assigned to exactly one bucket; the
script asserts this partition is total and exhaustive before writing.
"""
import sys

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 932, f"expected 932 lines, got {len(lines)} -- file changed, abort"


def seg(a, b):
    return lines[a - 1:b]


KEPT = [(1, 17)]
HOISTED = [(115, 128), (129, 137), (194, 243), (528, 538), (567, 583),
           (584, 590), (641, 663), (686, 696), (697, 707), (708, 719),
           (720, 732), (733, 748), (749, 756), (757, 765), (766, 805),
           (806, 840), (841, 854), (855, 877), (878, 883), (884, 892),
           (893, 912), (913, 927), (928, 932)]
ARCHIVED = [(18, 42), (43, 70), (71, 91), (92, 114), (138, 160), (161, 181),
            (182, 193), (244, 278), (279, 305), (306, 325), (326, 347),
            (348, 370), (371, 388), (389, 409), (410, 429), (430, 454),
            (455, 474), (475, 499), (500, 527), (539, 566), (591, 609),
            (610, 623), (624, 640), (664, 685)]

checks = [
    (1, "- [x] **DONE cycle 2510"), (115, "- [ ] **NEW follow-up (c2508, MEDIUM"),
    (129, "- [ ] **NEW follow-up (c2504, LOW"), (194, "- [ ] **`enum_audit` backlog"),
    (528, "- [ ] **NEW (c2478, MEDIUM, deadline 2026-11-15"),
    (567, "- [ ] **NEW follow-up (c2464, HIGH"), (584, "- [ ] **NEW note (c2464, TRIVIAL"),
    (641, "- [ ] **NEW follow-up (c2492, MEDIUM"), (686, "- [ ] **NEW follow-up (c2456, LOW"),
    (697, "- [ ] **NEW follow-up (c2436, LOW"), (708, "- [ ] **NEW (c2396, LOW priority"),
    (720, "- [ ] **NEW follow-up (c2392, LOW priority"), (733, "- [ ] **NEW follow-up (c2388, LOW"),
    (749, "- [ ] **NEW follow-up (c2385, low priority"), (757, "- [ ] **STANDING METHOD (c2383)"),
    (766, "- [ ] **FOLLOW-UP from c2380"), (806, "- [ ] **NEW STANDING TRIPWIRE (c2336)"),
    (841, "- [ ] **NEW follow-up (c2332)"), (855, "- [ ] **NEW follow-up (c2312)"),
    (878, "- [ ] **Process lesson to apply on any cycle that changes BOTH"),
    (884, "- [ ] **NEW follow-up (c2196)"), (893, "- [ ] **NEW follow-up (c2168, REWRITTEN c2268"),
    (913, "- [ ] **NEW follow-up (c2371)"), (928, "- [ ] **Process lesson to apply every cycle (found c2120)"),
    (18, "- [x] **DONE cycle 2504"), (43, "- [x] **DONE cycle 2506 (fix) + cycle 2507"),
    (71, "- [x] **DONE cycle 2508"), (92, "- [x] **DONE cycle 2509"),
    (138, "- [x] **DONE cycle 2503"), (161, "- [x] **DONE cycle 2502"),
    (182, "- [x] **DONE cycle 2501"), (244, "- [x] **DONE cycle 2500"),
    (279, "- [x] **DONE cycle 2499"), (306, "- [x] **DONE cycle 2498"),
    (326, "- [x] **DONE cycle 2497"), (348, "- [x] **DONE cycle 2496"),
    (371, "- [x] **DONE cycle 2495"), (389, "- [x] **DONE cycle 2494"),
    (410, "- [x] **DONE cycle 2493"), (430, "- [x] **DONE cycle 2488"),
    (455, "- [x] **DONE cycle 2487"), (475, "- [x] **DONE cycle 2486"),
    (500, "- [x] **DONE cycle 2485"), (539, "- [x] **CLOSED (c2490"),
    (591, "- [x] **CLOSED (c2491"), (610, "- [x] **DONE/CLOSED (c2492"),
    (624, "- [x] **WON'T FIX / CLOSED (c2492"), (664, "- [x] **CLOSED as WON'T FIX (c2492"),
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
    "\n## Archived by cycle 2511 (sonnet-5), 2026-10-31 -- queue.md had grown to 932 lines / "
    "85.7KB, flagged TRIM SOON this cycle and projected to cross TRIM DUE before check-doc-size's "
    "next look (24c); trimmed proactively per the c2510 handoff. Hoist-then-cut method (not a "
    "line cut): every genuinely-open `- [ ] ` item was hoisted to the live file verbatim in "
    "source order (23 ranges, listed in bin/_trim2511q.py), the single most recent DONE block "
    "(cycle 2510) was kept live, and every other DONE/CLOSED/WON'T-FIX block was archived -- none "
    "of them is the only home of a cadence instruction (checked each one: all referenced "
    "intervals live in state/fleet_checks.json or state/audit_dates.json, and the two c2492 "
    "WON'T-FIX decisions are also recorded as a comment in bin/audit-due itself).\n\n"
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
