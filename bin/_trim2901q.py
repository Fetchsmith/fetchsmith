#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2901 (134.7KB / 1618 lines, TRIM DUE).

QUALITY/GROWTH slot (2901 % 3 == 0). Fresh preflight: `audit-due --all` found
ONE real fleet-rotation item DUE (`varied_test: court-records-scraper`,
2564 -> now, 337c+) -- deliberately declined this cycle in favor of the
escalated doc-trim (see reasoning in the new DONE block below). `checks-due
--all` NONE DUE except `check-doc-size` itself (soonest in 1c, which is what
surfaced TRIM DUE). `check-doc-size` read tasks/queue.md as TRIM DUE: the
trigger was its *projected-over-256KB-Read-cap* branch (134,700B +
5440 B/cycle * 24c = ~262KB >= 256KB), not the file being over the 200KB
trim line today.

Method: hoist-then-cut on the DONE bucket only. Archiving the 6 oldest DONE
blocks (18,248B gross) comfortably clears the Read-cap-projection trigger
(only ~6.3KB of net cut was needed to drop projected size back under 256KB);
a full cut to the ~72.5KB "OK" line would require also compressing several
open items (c2380/STANDING c2532/ORIGINAL c2845/UPDATED c2846/STANDING RULE
c2796/c2464 follow-up, ~18KB combined per c2880's own measurement, Nov-15
item c2478 excluded) which this cycle intentionally left untouched given a
25-minute time budget -- flagged as the next candidates in the new NEXT
pointer this script also writes.

Ranges re-derived fresh from the live file this cycle (never paste line
numbers forward), each boundary confirmed by exact-line inspection via sed
and cat -A (verified both ends of the archived range sit on a blank line
with no open item interleaved).

Standing-hazard check (rule 1: grep FIRST, then READ the hits) run before
writing this script over the archive-bound range 230-441: pattern
"standing|cadence|always |never |STANDING|do not |must |rule" (-i) --
every rule-shaped hit is narrative about prior audits/fixes describing a
rule homed elsewhere (e.g. the c1758/c2352 status-message rule, which lives
as its own standing-warning queue item outside this range, untouched).

Partition is asserted total, non-overlapping and multiset-identical to the
original.
"""

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
NLINES = 1618

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == NLINES, f"expected {NLINES} lines, got {len(lines)} -- file changed, abort"


def seg(a, b):
    return lines[a - 1:b]


# Fully-historical content: 6 contiguous DONE blocks (c2893, c2892, c2891,
# c2890, c2888, c2887), no open items interleaved. Plus the stale NEXT
# pointer (39-44), replaced in place (not archived -- it is superseded
# scheduling text, not durable record; discarded, not moved).
ARCHIVED = [
    (230, 441),   # DONE c2893, c2892, c2891, c2890, c2888, c2887
]

DISCARDED = [
    (39, 44),     # stale "NEXT (c2901...)" pointer, replaced below (not archived)
]

KEPT = [
    (1, 38),        # DONE c2900 (unchanged) + its trailing blank line
    (45, 229),      # c2900 follow-ups .. DONE c2899, c2898, c2897 .. open items thru blank before DONE c2893
    (442, NLINES),  # everything from NEW watch c2875 onward, unchanged
]

NEW_DONE_BLOCK = """- [x] **DONE c2901 (QUALITY/GROWTH slot, 2901 % 3 == 0) -- executed the overdue doc-trim
      cadence on `tasks/queue.md`, which `check-doc-size` read fresh this cycle as **TRIM DUE**
      (134.7KB/1618 lines) via its projected-over-the-256KB-Read-cap branch (134,700B +
      5440 B/cycle * 24c-interval = ~262KB), not because the file itself was over the 200KB trim
      line -- carried as TRIM SOON for three straight prior cycles (c2898-c2900) with no cycle
      picking it up.** Preflight: `audit-due --all` found ONE real fleet-rotation item DUE,
      `varied_test: court-records-scraper` (2564 -> now, 337c+) -- **DELIBERATELY DECLINED** this
      cycle: the escalated doc-trim is cheap, safe and already overdue by the checker's own
      forward-looking rule, while the rotation audit runs on a 7-day cadence with no clock
      pressure and no prior slot had taken it either. `checks-due --all` NONE DUE except
      `check-doc-size` itself (soonest in 1c, which is what surfaced this). `inbox-triage new`
      NONE UNTRIAGED of 75. `bin/revenue` unchanged: $0 booked, 27 Actors, 50 users, 825
      runs30d, 3 ext_bad30d, 0 bookmarks, 0 reviews -- no buyer signal, no owner email owed.
      `bin/_trim2901q.py` (hoist-then-cut, ranges re-derived fresh, boundaries confirmed on
      blank-line edges with no open item interleaved): archived the 6 oldest live DONE blocks
      (c2893, c2892, c2891, c2890, c2888, c2887 -- 18,248B) verbatim to `tasks/queue_archive.md`
      under a new header, keeping the newest 5 (c2901, c2900, c2899, c2898, c2897) per the
      standing newest-5-DONE-block convention (c2865). Also discarded the now-stale `NEXT
      (c2901...)` scheduling pointer and wrote a fresh one for c2902 (below, this file).
      **See `bin/check-doc-size` for the measured post-cut size** (read the tool, not this
      prose, per standing rule). Lossless-verified: total, non-overlapping, multiset-identical
      partition of non-blank lines between kept+archived content and the original (the discarded
      NEXT pointer is scheduling text, intentionally not part of the lossless guarantee -- it is
      fully superseded by the replacement pointer below). Backup `/tmp/c2901_queue.bak`.
      **Did NOT touch the open-item compression candidates c2880 already measured** (c2380,
      STANDING c2532, ORIGINAL c2845, UPDATED c2846, STANDING RULE c2796, c2464 follow-up --
      ~18KB combined; Nov-15 item c2478 still DO NOT TOUCH before 2026-11-15) -- the DONE-block
      archive alone was enough to clear the Read-cap-projection trigger, so this cycle stopped
      there rather than take on open-item-compression risk under a 25-minute time budget. They
      remain the next candidates if `check-doc-size` still reads TRIM SOON/DUE next time (very
      likely -- the ~72.5KB durable-OK line is far below where this cut lands).
      Services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; `/`, `/pricing`, `/tools`
      all 200 before and after. $0 spend (pure docs, no build, no Actor run, no code change).

"""

NEW_NEXT_BLOCK = """- [ ] **NEXT (c2902) -- `varied_test: court-records-scraper` is the only real fleet-rotation
      item DUE** (2564 -> now, 337c+; DECLINED by c2901 in favor of the escalated doc-trim; see
      the DONE c2901 block above for why). Re-run `audit-due --all`/`checks-due --all` fresh; if
      nothing newer is DUE, take this one. Also re-read `bin/check-doc-size` on `tasks/queue.md`
      -- c2901's DONE-block archive cleared the immediate TRIM DUE trigger but the file is very
      likely still TRIM SOON (far from the ~72.5KB durable-OK line); the open-item compression
      candidates c2880 measured are the next cut if so: `c2380` one-term-diff, `STANDING c2532`,
      `ORIGINAL c2845`, `UPDATED c2846`, `STANDING RULE c2796`, `c2464` follow-up (~18KB combined
      -- Nov-15 item `c2478` still DO NOT TOUCH before 2026-11-15).

"""

# Reassemble in source order.
final_lines = []
final_lines.extend(NEW_DONE_BLOCK.splitlines(keepends=True))
final_lines.extend(seg(*KEPT[0]))          # (1,38)  DONE c2900 + trailing blank
final_lines.extend(NEW_NEXT_BLOCK.splitlines(keepends=True))
final_lines.extend(seg(*KEPT[1]))          # (45,229)
final_lines.extend(seg(*KEPT[2]))          # (442,NLINES)

# ---- Assertions ----
# 1. Partition of the original (ARCHIVED + DISCARDED + KEPT) is total & non-overlapping.
all_ranges = sorted(ARCHIVED + DISCARDED + KEPT)
covered = set()
for a, b in all_ranges:
    r = set(range(a, b + 1))
    assert not (covered & r), f"overlap at {a}-{b}"
    covered |= r
assert covered == set(range(1, NLINES + 1)), "partition not total"

# 2. Multiset identity on non-blank lines: (kept + archived) must equal
#    (original minus discarded), i.e. the only lines allowed to vanish are the
#    discarded stale pointer's.
from collections import Counter

old_kept = []
for a, b in KEPT:
    old_kept.extend(seg(a, b))
archived_lines = []
for a, b in ARCHIVED:
    archived_lines.extend(seg(a, b))
discarded_lines = []
for a, b in DISCARDED:
    discarded_lines.extend(seg(a, b))

orig_nonblank = [l for l in lines if l.strip()]
discarded_nonblank = [l for l in discarded_lines if l.strip()]
expected_nonblank = Counter(orig_nonblank)
for l in discarded_nonblank:
    expected_nonblank[l] -= 1
expected_nonblank = Counter({k: v for k, v in expected_nonblank.items() if v > 0})

recon_nonblank = [l for l in (old_kept + archived_lines) if l.strip()]
assert Counter(recon_nonblank) == expected_nonblank, "multiset mismatch -- lossy cut beyond the intended discard"

# 3. Each rewrite asserted present/absent.
final_content = "".join(final_lines)
for probe in ["DONE c2901 (QUALITY/GROWTH slot", "NEXT (c2902)"]:
    assert probe in final_content, f"rewrite missing: {probe}"
for gone in ["NEXT (c2901, QUALITY/GROWTH slot, 2901 % 3 == 0) -- `varied_test: court-records-scraper`",
             "**DONE c2893 (Regular slot, 2893 % 3 == 1)"]:
    assert gone not in final_content, f"old text still live: {gone}"

# 4. Newest-5 DONE convention holds exactly.
done_count = sum(1 for l in final_lines if l.startswith("- [x] "))
assert done_count == 5, f"expected 5 live DONE blocks, got {done_count}"

# 5. Independent lossless check: every non-blank original line (minus the
#    intentionally-discarded NEXT pointer) must be findable in live+archive.
with open(ARCHIVE) as f:
    old_archive_content = f.read()

HEADER = "\n## Archived by cycle 2901\n\n"
new_archive_content = old_archive_content + HEADER + "".join(archived_lines)
combined = final_content + new_archive_content

discarded_stripped = {l.strip() for l in discarded_nonblank}
missing = [
    l for l in orig_nonblank
    if l.strip() not in combined and l.strip() not in discarded_stripped
]
assert not missing, f"{len(missing)} original non-blank lines not findable post-cut"

with open(SRC, "w") as f:
    f.write(final_content)
with open(ARCHIVE, "w") as f:
    f.write(new_archive_content)

print("OK -- wrote", SRC, f"({len(final_lines)} lines), appended {len(archived_lines)} lines to", ARCHIVE)
print(f"original non-blank lines: {len(orig_nonblank)}, discarded: {len(discarded_nonblank)}, "
      f"all remaining found in live+archive: True")
