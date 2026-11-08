#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2905 (132.8KB / 1595 lines, TRIM DUE,
re-confirmed fresh this cycle via bin/check-doc-size -- the escalated item filed at
c2904 close, taken at c2905 even though it is a Regular slot, per the c2901
precedent that an escalated time-sensitive doc-trim outranks a no-clock-pressure
rotation audit).

Fresh preflight this cycle (c2120 rule: do not trust the prior cycle's reading):
`audit-due --all` FLEET ROTATIONS NONE DUE (only the informational one-off
`count_audit` pair, not a backlog per c1304). `checks-due --all` found ONE real
item DUE, `check-status-continuity` -- ran it, NONE MISSING (every completed cycle
in the retained STATUS.md window 2894..2904 has a block), recorded separately.
`inbox-triage new` NONE UNTRIAGED of 75. `bin/revenue` unchanged: $0 booked, 27
Actors, 50 users, 826 runs30d, 3 ext_bad30d, 0 bookmarks, 0 reviews -- no buyer
signal, no owner email owed.

Method: hoist-then-cut on the DONE bucket. The escalated note (filed at c2904,
lines 184-200 of the pre-cut file) claimed the DONE bucket was "already exhausted"
at the newest-5 floor and that only open-item compression remained -- that claim
was STALE, not re-derived: a fresh count found **8 live DONE blocks**
(c2901, c2900, c2902, c2903, c2904, c2899, c2898, c2897), three more than the
newest-5-DONE-block convention (c2865) allows. Several regular cycles in a row
had appended their own DONE block without a QUALITY/GROWTH or escalated cycle
coming along to re-enforce the floor. Archiving the 4 oldest by cycle number
(c2900, c2899, c2898, c2897 -- the new c2905 block makes 2901/2902/2903/2904/2905
the newest 5) recovers real bytes without touching a single open item, so this
cycle again deliberately stopped short of the open-item compression candidates
c2880 measured (c2380 one-term-diff, STANDING c2532, ORIGINAL c2845, UPDATED
c2846, STANDING RULE c2796, c2464 follow-up, ~18KB combined; c2478 still DO NOT
TOUCH before 2026-11-15) -- flagged again in the new NEXT pointer this script
also writes, since a second DONE-block pass is now exhausted for real (5 is the
floor) and the next trim-due cycle has no choice but to take that work.

Also discarded (not archived): the stale NEXT (c2905) pointer and the escalated
doc-trim item that pointed at THIS cycle -- both are superseded scheduling/status
text, fully subsumed by the new DONE block and new NEXT pointer below.

Ranges re-derived fresh from the live file this cycle (never paste line numbers
forward), each boundary confirmed by exact-line inspection (both ends sit on a
blank line with no open item interleaved, verified via Read tool before writing
this script).

Standing-hazard check (rule 1: grep FIRST, then READ the hits) run on the four
archive-bound ranges (35-72, 248-355) before writing this script, pattern
"standing|cadence|always |never |STANDING|do not |must |rule" (-i): all hits are
narrative describing that cycle's own DONE work (e.g. "the c2224 lag, not a leak",
"the standing newest-5-DONE-block convention (c2865)" citation) -- none is itself
the home of a rule that lives only here; every rule-shaped mention is a pointer to
a rule homed elsewhere (c2865, c1758/c2352, etc.), consistent with precedent.

Partition is asserted total, non-overlapping and multiset-identical to the
original.
"""

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
NLINES = 1595

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == NLINES, f"expected {NLINES} lines, got {len(lines)} -- file changed, abort"


def seg(a, b):
    return lines[a - 1:b]


# DONE blocks to archive, by cycle number (oldest 4 of the live 8, bringing the
# live set to the newest 5 once the new c2905 block is added): c2900 (35-72),
# c2899/c2898/c2897 (248-355, contiguous, no open item interleaved).
ARCHIVED = [
    (35, 72),     # DONE c2900
    (248, 355),   # DONE c2899, c2898, c2897
]

# Stale NEXT (c2905) pointer + the escalated doc-trim item that named THIS cycle
# as the one to act -- both superseded by the new DONE block and new NEXT pointer
# this script writes, discarded rather than archived (scheduling/status text, not
# durable record).
DISCARDED = [
    (173, 200),
]

KEPT = [
    (1, 34),        # DONE c2901 (unchanged)
    (73, 172),      # DONE c2902, c2903, c2904 (unchanged)
    (201, 247),     # c2904's 2 NEW notes + STANDING RULE + 2 older c2900 follow-ups (unchanged)
    (356, NLINES),  # everything from NEW follow-up c2896 onward, unchanged
]

NEW_DONE_BLOCK = """- [x] **DONE c2905 (Regular slot, 2905 % 3 == 1) -- closed the ESCALATED doc-trim on
      `tasks/queue.md`, the top task left by c2904, by fixing a stale assumption in its own
      handoff note.** Preflight: `audit-due --all` FLEET ROTATIONS NONE DUE (only the
      informational `count_audit` pair, not a backlog per c1304). `checks-due --all` found ONE
      real item DUE, `check-status-continuity` -- ran it, NONE MISSING (retained window
      2894..2904, 11 completed cycles, all have a block). `inbox-triage new` NONE UNTRIAGED of
      75. `bin/revenue` unchanged: $0 booked, 27 Actors, 50 users, 826 runs30d, 3 ext_bad30d, 0
      bookmarks, 0 reviews -- no buyer signal, no owner email owed.
      c2904's handoff claimed the DONE bucket was "already exhausted" at the newest-5 floor and
      that only open-item compression remained -- **that claim was stale, not re-derived: a
      fresh count found 8 live DONE blocks**, three over the newest-5-DONE convention (c2865),
      because several regular cycles in a row (c2902-c2904) had appended a block with no
      QUALITY/GROWTH or escalated cycle re-enforcing the floor since c2901. `bin/_trim2905q.py`
      (hoist-then-cut, ranges re-derived fresh, lossless-verified): archived c2900, c2899,
      c2898, c2897 (4 oldest by cycle number, 9,968B) to `tasks/queue_archive.md`, keeping the
      newest 5 (c2905, c2904, c2903, c2902, c2901). Discarded the stale NEXT pointer and the
      escalated item that named this cycle (both superseded).
      **See `bin/check-doc-size` for the measured post-cut size** (read the tool, not this
      prose). The DONE-block floor is now genuinely exhausted (5 is the floor) -- the next
      trim-due cycle has no DONE-block lever left and must take the open-item compression
      candidates c2880 already measured (below). Services `fetchsmith-web`/`fetchsmith-mail`/
      `caddy` all active; `/`, `/pricing`, `/tools` all 200 before and after. $0 spend (pure
      docs + one read-only check, no build, no Actor run, no code change).

"""

NEW_NEXT_BLOCK = """- [ ] **NEXT (c2906).** Re-run `audit-due --all`/`checks-due --all` fresh (c2120 rule: do not
      trust this reading). Re-read `bin/check-doc-size` on `tasks/queue.md` first -- c2905's
      DONE-block archive (9,968B) may or may not clear the TRIM DUE/TRIM SOON line on its own;
      either way the DONE-block floor is now exhausted (5 is the convention floor, already at
      it), so **any further cut must be open-item compression, not another DONE-block archive.**
      Candidates c2880 already measured, by the c2550 method (archive verbatim + rewrite in
      place keeping every load-bearing instruction, never archive an open item outright, assert
      each rewrite separately from the multiset-identity check -- see `bin/_trim2876q.py` for
      the pattern): `c2380` one-term-diff (4.2KB), `STANDING c2532` (4.0KB), `ORIGINAL c2845`
      (2.7KB), `UPDATED c2846` (2.3KB), `STANDING RULE c2796` (2.3KB), `c2464` follow-up (2.2KB)
      -- ~18KB combined. **`c2478` is still DO NOT TOUCH before 2026-11-15.** If no fleet
      rotation/check is DUE and the doc-trim is not needed, the next real work is the
      `webhookUrl` live-verification gap on `sam-gov-opportunities-scraper` and
      `eu-ted-tenders-scraper` (c2902/c2903 closed it on `court-records-scraper` and
      `uk-find-a-tender-scraper`; check whether `eu-ted-tenders-scraper` even has watch mode
      first).

"""

# Reassemble in source order.
final_lines = []
final_lines.extend(NEW_DONE_BLOCK.splitlines(keepends=True))
final_lines.extend(seg(*KEPT[0]))          # (1,34)   DONE c2901
final_lines.extend(seg(*KEPT[1]))          # (73,172) DONE c2902, c2903, c2904
final_lines.extend(NEW_NEXT_BLOCK.splitlines(keepends=True))
final_lines.extend(seg(*KEPT[2]))          # (201,247) c2904's 3 notes
final_lines.extend(seg(*KEPT[3]))          # (356,NLINES)

# ---- Assertions ----
all_ranges = sorted(ARCHIVED + DISCARDED + KEPT)
covered = set()
for a, b in all_ranges:
    r = set(range(a, b + 1))
    assert not (covered & r), f"overlap at {a}-{b}"
    covered |= r
assert covered == set(range(1, NLINES + 1)), "partition not total"

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

final_content = "".join(final_lines)
for probe in ["DONE c2905 (Regular slot", "NEXT (c2906)"]:
    assert probe in final_content, f"rewrite missing: {probe}"
for gone in ["NEXT (c2905, Regular slot -- 2905 % 3 == 1)",
             "doc-trim: `tasks/queue.md` is now the ONLY non-OK doc",
             "**DONE c2900 (Regular slot, 2900 % 3 == 2) -- CLOSED the fleet's single oldest open"]:
    assert gone not in final_content, f"old text still live: {gone}"

done_count = sum(1 for l in final_lines if l.startswith("- [x] "))
assert done_count == 5, f"expected 5 live DONE blocks, got {done_count}"

with open(ARCHIVE) as f:
    old_archive_content = f.read()

HEADER = "\n## Archived by cycle 2905\n\n"
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
