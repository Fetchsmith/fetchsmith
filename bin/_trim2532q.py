#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2532 (72.5KB / 763 lines).

check-doc-size read TRIM SOON on this file at preflight (72.5KB / 763 lines,
~24 cycles of headroom at +5440 B/cycle, projected 200KB at the checker's next
automatic look in 24c), and c2531's handoff assigned the trim to this cycle --
2532 is a QUALITY/GROWTH slot (2532 % 3 == 0), where check-doc-size itself says
to trim proactively rather than wait for the TRIM DUE escalation.

Same c2161/.../c2511/c2523 HOIST-THEN-CUT method, not a line cut: queue.md
interleaves standing `- [ ] ` open items among completed `- [x]` cycle blocks,
so a naive line-number cut would silently delete live open work. Structure at
2532 is unusually clean -- 7 DONE blocks (2531, 2530, 2529, 2526, 2524, 2523,
2522) occupy lines 1-254 and all 22 open items are contiguous at 255-763 -- but
the method is kept anyway so the partition is asserted rather than assumed.

  1. KEPT: the single most recent DONE block (cycle 2531, lines 1-35).
  2. HOISTED: 20 of the 22 still-open `- [ ] ` items, verbatim, in source order.
     (This cycle then rewrites the hoisted doc-trim cadence item in place and
     appends two new items -- done with Edit AFTER this script, so that the
     verbatim-partition assertions below stay honest.)
  3. ARCHIVED: the 6 older DONE blocks (36-254) PLUS the two `enum_audit`
     backlog items (281-407 and the superseded-screening-method predecessor it
     kept for context, 408-457). Those two are archived because the backlog
     they track is GENUINELY CLOSED, not merely deferred: c2531 closed the last
     2 Actors and `bin/audit-due --type enum_audit` reads NONE DUE this cycle,
     soonest `sec-insider-trades-scraper` in 301 cycles (cycle 2833). Their
     cadence is tracked in state/audit_dates.json, not in this prose, so
     archiving them loses no schedule.

     Per the standing hazard (cadence instructions that live ONLY in queue.md
     prose have twice vanished into the archive while the tool still looked
     maintained -- bin/devto-comments 43 cycles unrun, check-competitor-claims
     121), both items were READ IN FULL first to find anything they are the only
     home of. Two things were, and both are carried forward as live open items
     this cycle instead of being archived:
       - the "hidden backlog behind audit-due's single-type default" warning,
         which this cycle CONFIRMED is live and real: `--type unreachable_remedy`
         reads 23 DUE and `--type count_audit` 2 DUE, neither surfaced by the
         standard `audit-due --all` preflight.
       - the "Do NOT attempt court-records-scraper.courts, there is no
         CourtListener token" note, whose premise is now FALSE: `CL_API_TOKEN`
         is in secrets/env and was verified live this cycle (HTTP 200, 3359
         courts from /api/rest/v4/courts/).
     Their durable METHOD lessons (targeted audit_dates.json edits over
     json.dump, mirror the key the Actor itself sends, make probes assert their
     values diverge, enum-screen's declared-enums-only and surface-only limits)
     are already in notes/LEARNINGS.md -- grep-confirmed this cycle -- so they
     are not lost either.

Every one of the file's 763 lines is assigned to exactly one bucket; the script
asserts the partition is total, non-overlapping, and multiset-identical to the
original before writing.
"""
import sys

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 763, f"expected 763 lines, got {len(lines)} -- file changed, abort"


def seg(a, b):
    return lines[a - 1:b]


KEPT = [(1, 35)]
HOISTED = [(255, 280), (458, 468), (469, 485), (486, 492), (493, 515),
           (516, 526), (527, 538), (539, 551), (552, 567), (568, 575),
           (576, 584), (585, 624), (625, 659), (660, 685), (686, 708),
           (709, 714), (715, 723), (724, 743), (744, 758), (759, 763)]
ARCHIVED = [(36, 101), (102, 136), (137, 158), (159, 194), (195, 208),
            (209, 254), (281, 407), (408, 457)]

checks = [
    (1, "- [x] **DONE cycle 2531"),
    (36, "- [x] **DONE cycle 2530"), (102, "- [x] **DONE cycle 2529"),
    (137, "- [x] **DONE cycle 2526"), (159, "- [x] **DONE cycle 2524"),
    (195, "- [x] **DONE cycle 2523"), (209, "- [x] **DONE cycle 2522"),
    (255, "- [ ] **doc-trim cadence (orig. c2508"),
    (281, "- [ ] **`enum_audit` backlog -- now has a REAL tool"),
    (408, "- [ ] **(superseded screening method, kept for context)"),
    (458, "- [ ] **NEW (c2478, MEDIUM, deadline 2026-11-15"),
    (469, "- [ ] **NEW follow-up (c2464, HIGH"),
    (486, "- [ ] **NEW note (c2464, TRIVIAL"),
    (493, "- [ ] **NEW follow-up (c2492, MEDIUM"),
    (516, "- [ ] **NEW follow-up (c2456, LOW"),
    (527, "- [ ] **NEW (c2396, LOW priority"),
    (539, "- [ ] **NEW follow-up (c2392, LOW priority"),
    (552, "- [ ] **NEW follow-up (c2388, LOW"),
    (568, "- [ ] **NEW follow-up (c2385, low priority"),
    (576, "- [ ] **STANDING METHOD (c2383)"),
    (585, "- [ ] **FOLLOW-UP from c2380"),
    (625, "- [ ] **NEW STANDING TRIPWIRE (c2336)"),
    (660, "- [ ] **UPDATED (c2517) follow-up (orig. c2332)"),
    (686, "- [ ] **NEW follow-up (c2312)"),
    (709, "- [ ] **Process lesson to apply on any cycle that changes BOTH"),
    (715, "- [ ] **NEW follow-up (c2196)"),
    (724, "- [ ] **NEW follow-up (c2168, REWRITTEN c2268"),
    (744, "- [ ] **NEW follow-up (c2371)"),
    (759, "- [ ] **Process lesson to apply every cycle (found c2120)"),
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

# every hoisted range must start a real open item, and none may contain a DONE header
for a, b in HOISTED:
    assert lines[a - 1].startswith("- [ ] "), f"hoisted range at {a} is not an open item"
    for i in range(a, b + 1):
        assert not lines[i - 1].startswith("- [x] "), f"DONE header inside hoisted range at {i}"


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
    "\n## Archived by cycle 2532 (opus-5), 2026-10-31 -- queue.md had grown to 763 lines / "
    "72.5KB, flagged TRIM SOON at this cycle's preflight and projected to cross the 200KB trim "
    "line before check-doc-size's next look (24c); trimmed proactively per the c2531 handoff in "
    "this QUALITY/GROWTH slot. Hoist-then-cut method (not a line cut): the single most recent "
    "DONE block (cycle 2531) was kept live, 20 still-open `- [ ] ` items were hoisted verbatim in "
    "source order (ranges listed in bin/_trim2532q.py), and the 6 older DONE blocks (2530, 2529, "
    "2526, 2524, 2523, 2522) were archived. ALSO archived, and this is the only judgement call in "
    "the cut: the two `enum_audit` backlog items, because that backlog is genuinely CLOSED rather "
    "than deferred -- c2531 closed the last 2 Actors and `bin/audit-due --type enum_audit` read "
    "NONE DUE this cycle (soonest sec-insider-trades-scraper in 301c, cycle 2833), and its "
    "schedule lives in state/audit_dates.json, not in this prose. Both were read in full first "
    "per the standing cadence-loss hazard; the two things they were the ONLY home of were carried "
    "forward as live open items instead of archived -- (a) the hidden backlog behind audit-due's "
    "single-type default, CONFIRMED live this cycle (`--type unreachable_remedy` 23 DUE, "
    "`--type count_audit` 2 DUE, neither surfaced by `audit-due --all`), and (b) the "
    "court-records-scraper.courts 'no CourtListener token' blocker, whose premise is now FALSE "
    "(CL_API_TOKEN is in secrets/env, verified live this cycle: HTTP 200, 3359 courts). Their "
    "durable method lessons are already in notes/LEARNINGS.md (grep-confirmed).\n\n"
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
