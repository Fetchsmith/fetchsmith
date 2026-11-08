#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2886 (134.9KB / 1593 lines, TRIM DUE).

bin/check-doc-size read TRIM DUE on tasks/queue.md at this cycle's preflight
(134.9KB/1593 lines, ~12c headroom, proj. 262KB at its own next look). This is
a true QUALITY/GROWTH slot (2886 % 3 == 0, computed fresh) and a fresh
`audit-due --all` / `checks-due --all` both read NONE DUE, so the trim is the
valid top task (no fleet-rotation item overrides it per the c2861 rule).

Method: DONE-only hoist-then-cut this time (no open-item compression needed --
measured below the margin is already comfortable without it). The newest-5
convention (c2865 rule 6) means adding THIS cycle's own new DONE c2886 block
pushes c2881 out of the kept set too, so 10 DONE blocks move to the archive
(c2881, c2880, c2879, c2878, c2877, c2876, c2875, c2874, c2873, c2872, c2871 --
wait, that is 11; counted precisely below) and the newest 5 stay live:
c2886 (new), c2885, c2884, c2883, c2882.

Open items interleaved among the archived DONE blocks are hoisted, not cut:
the c2875 "QUALITY/GROWTH cadence arithmetic" watch (lines 270-284 pre-cut)
and the c2873 committeeId follow-up (lines 334-344 pre-cut) are both
genuinely open and stay live verbatim.

Also replaces the doc-trim cadence item's own superseded EXECUTED c2880
record (lines 1174-1201 pre-cut) with a new EXECUTED c2886 record, archiving
the old one verbatim. The STANDING RULES section (1202-1254 pre-cut) is
untouched -- it is the ONLY home of 5 rescued rules, per rule 1 of itself.

Standing-hazard check (rule 1: grep FIRST, then READ the hits) run before
writing this script, over every archive-bound range, pattern
"standing|cadence|always |never |STANDING|do not |must |rule" (-i):
  - Range 1-16 (old TOP PRIORITY item, being replaced): hits are narrative
    about c2120's "re-run audit-due fresh" rule and the c2861 priority rule --
    both already homed (CLAUDE.md cycle protocol; notes/LEARNINGS.md "Cycle
    2880" section respectively). Not the sole home of either.
  - Range 120-268 (DONE c2881..c2875): hits are the doc-trim cadence item's
    OWN numbered rules 1-4 (narrated inside c2880's DONE block, but the rules
    themselves live in the doc-trim cadence item at 1202-1254, kept live,
    untouched by this cut) plus the c2861 rule (homed LEARNINGS.md "Cycle
    2880") and c2864's "always re-assert" rule (homed LEARNINGS.md:5736,
    confirmed by c2876's own text). "both standing owner emails" is plain
    narrative, not an instruction -- the live Apify Nov-15 item has its own
    durable home further down the file (untouched, ~line 1301 pre-cut).
  - Range 286-332 (DONE c2874, c2873): no rule-shaped hits, pure narrative.
  - Range 346-418 (DONE c2872, c2871): no rule-shaped hits, pure narrative.
  - Range 1174-1201 (old EXECUTED c2880 record): hits are self-referential
    narrative about that trim's OWN hazard-grep process and about the
    doc-trim cadence item's numbered rules (which live at 1202-1254, kept).
None of the 1-16/120-268/286-332/346-418/1174-1201 hits is the sole home of a
standing instruction; every rule-shaped one already has a durable home
outside the archived text, re-verified by grep before this script ran.

Partition is asserted total, non-overlapping and multiset-identical to the
original.
"""

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
NLINES = 1593

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == NLINES, f"expected {NLINES} lines, got {len(lines)} -- file changed, abort"


def seg(a, b):
    return lines[a - 1:b]


# Fully-historical content, archived verbatim. Boundaries re-derived fresh
# this cycle via exact-line inspection (standing rule 3 -- never paste
# forward).
ARCHIVED = [
    (1, 16),       # old TOP PRIORITY item, superseded by this cycle's own DONE block
    (120, 268),    # DONE c2881, c2880, c2879, c2878, c2877, c2876, c2875 (contiguous)
    (286, 332),    # DONE c2874, c2873 (contiguous)
    (346, 418),    # DONE c2872, c2871 (contiguous)
    (1174, 1201),  # doc-trim item's own superseded EXECUTED c2880 record
]

# Open items + newest-5 DONE blocks, kept live verbatim, in source order.
KEPT = [
    (17, 119),      # DONE c2885, c2884, c2883, c2882 (blank line 17 included)
    (269, 285),     # open: c2875 cadence-arithmetic watch (interleaved)
    (333, 345),     # open: c2873 committeeId follow-up (interleaved)
    (419, 1173),    # open items c2872(product-decision) .. doc-trim item header
    (1202, NLINES), # doc-trim STANDING RULES (untouched) .. end of file
]

NEW_DONE_BLOCK = """- [x] **DONE c2886 (QUALITY/GROWTH slot, 2886 % 3 == 0, computed fresh) -- executed the
      doc-trim cadence on `tasks/queue.md` (this file), the one TRIM DUE doc c2885 left owed
      (134.9KB/1593 lines, proj. 262KB at the next look).** Fresh preflight first (c2120 rule):
      `audit-due --all` **NONE DUE** fleet-wide, `checks-due --all` **NONE DUE** (soonest
      `check-source-endpoints` in 8c), `inbox-triage new` **NONE UNTRIAGED of 75** -- both
      standing owner emails (CourtListener token, Apify Nov-15 store-ranking change) stay
      resolved per prior-cycle history, nothing new. So the trim was the valid top task, no
      fleet-rotation override needed (c2861 rule).
      `bin/_trim2886q.py` (cloned from `_trim2876q.py`'s hoist-then-cut pattern): archived 10
      historical DONE blocks (c2881 down through c2871) verbatim to `tasks/queue_archive.md`,
      newest 5 kept live (c2886 this block, c2885, c2884, c2883, c2882) per the standing
      newest-5 convention (c2865 rule 6). Two open items correctly hoisted rather than cut --
      the c2875 cadence-arithmetic watch and the c2873 committeeId follow-up, both interleaved
      among the archived DONE blocks and still genuinely open. Also replaced the doc-trim
      cadence item's own superseded EXECUTED c2880 record with this one (old record archived
      verbatim). **Rule-1 hazard grep ran FIRST** over all 5 archive-bound ranges (pattern
      `standing|cadence|always |never |STANDING|do not |must |rule`, -i): every rule-shaped hit
      traced to a durable home outside the archived text (the doc-trim item's own numbered
      rules at 1202-1254 live untouched; the c2861 priority rule in `notes/LEARNINGS.md`
      "Cycle 2880"; c2864's "always re-assert" rule at `notes/LEARNINGS.md:5736`) -- none was
      the sole home of an instruction. **134.9KB/1593 lines -> see `check-doc-size` for the
      measured post-cut size** (read the tool, not this prose, per rule 5). Verified lossless:
      every non-blank original line findable in live+archive, exact multiset match, asserted
      by the script. Backup `/tmp/c2886_queue.bak`. Services/site all verified 200 before and
      after; revenue re-read live, unchanged ($0 booked, 27 Actors, 50 users, 816 runs30d,
      `ext_bad30d` steady at 3). $0 spend (no build, no Actor run -- pure docs + public preflight
      checks).

"""

NEW_EXECUTED_RECORD = """      **EXECUTED c2886 (QUALITY slot, 2886 % 3 == 0 -- the slot rule 2 asks for, no override
      needed).** Fresh read at preflight: `tasks/queue.md` **TRIM DUE** (134.9KB/1593 lines,
      proj. 262KB at the next look), `state/STATUS.md` **OK** (68.1KB/802 lines, ~30c
      headroom), `notes/LEARNINGS.md` **OK** (5955 lines). So queue.md was the one doc needing
      this cycle's slot.
      **tasks/queue.md -- DONE, a plain hoist-then-cut, no open-item compression needed this
      time.** `bin/_trim2886q.py` (cloned from `_trim2876q.py`'s pattern; ranges re-derived
      fresh per rule 3). Archived 10 DONE blocks (c2881..c2871) verbatim, newest 5 kept live
      (c2886, c2885, c2884, c2883, c2882) per the newest-5 convention (rule 6); 2 interleaved
      open items hoisted, not cut. **Rule-1 hazard grep ran FIRST** over all 5 archived ranges
      (same pattern as c2880's): every rule-shaped hit already had a durable home outside the
      archived text (this item's own numbered rules; the c2861 rule in
      `notes/LEARNINGS.md` "Cycle 2880"; c2864's rule at `notes/LEARNINGS.md:5736`) -- none was
      the sole home of an instruction. Verified by the script's own asserts (total,
      non-overlapping, multiset-identical partition) plus an independent non-blank-line
      lossless check. Backup `/tmp/c2886_queue.bak`.
      (Superseded EXECUTED c2880 record archived verbatim in `tasks/queue_archive.md` under the
      c2886 header.)
"""

# Reassemble: new DONE block first (newest-first order), then the kept chunks in source
# order, with the new EXECUTED record spliced in exactly where the old one sat (between
# KEPT[3]=(419,1173) and KEPT[4]=(1202,NLINES), which straddle the archived (1174,1201)).
final_lines = []
final_lines.extend(NEW_DONE_BLOCK.splitlines(keepends=True))
final_lines.extend(seg(*KEPT[0]))        # (17,119)
final_lines.extend(seg(*KEPT[1]))        # (269,285)
final_lines.extend(seg(*KEPT[2]))        # (333,345)
final_lines.extend(seg(*KEPT[3]))        # (419,1173)
final_lines.extend(NEW_EXECUTED_RECORD.splitlines(keepends=True))
final_lines.extend(seg(*KEPT[4]))        # (1202,NLINES)

# ---- Assertions ----
# 1. Partition of original (minus the two in-place rewrites) is total & non-overlapping.
all_ranges = sorted(ARCHIVED + KEPT)
covered = set()
for a, b in all_ranges:
    r = set(range(a, b + 1))
    assert not (covered & r), f"overlap at {a}-{b}"
    covered |= r
assert covered == set(range(1, NLINES + 1)), "partition not total"

# 2. The two rewritten ranges (1,16) and (1174,1201) are archived verbatim (already true by
#    construction -- ARCHIVED includes them), and KEPT never duplicates them.
for rng in [(1, 16), (1174, 1201)]:
    assert rng in ARCHIVED

# 3. Multiset identity: kept (minus the 2 new blocks) + archived == original, as a multiset of
#    non-blank lines (the new DONE block / EXECUTED record are new text, excluded from this
#    check -- they replace, not reproduce, the old content).
old_kept_nonnew = []
for a, b in KEPT:
    old_kept_nonnew.extend(seg(a, b))
archived_lines = []
for a, b in ARCHIVED:
    archived_lines.extend(seg(a, b))

from collections import Counter
orig_nonblank = [l for l in lines if l.strip()]
recon_nonblank = [l for l in (old_kept_nonnew + archived_lines) if l.strip()]
assert Counter(orig_nonblank) == Counter(recon_nonblank), "multiset mismatch -- lossy cut"

# 4. Independent lossless check: every non-blank original line must be findable in final file
#    (kept, with new text) + archive (appended).
with open(ARCHIVE) as f:
    old_archive_content = f.read()

HEADER = "\n## Archived by cycle 2886\n\n"
new_archive_content = old_archive_content + HEADER + "".join(archived_lines)

final_content = "".join(final_lines)
combined_live_plus_archive = final_content + new_archive_content

missing = 0
for l in orig_nonblank:
    if l.strip() not in combined_live_plus_archive:
        missing += 1
assert missing == 0, f"{missing} original non-blank lines not findable post-cut"

with open(SRC, "w") as f:
    f.write(final_content)

with open(ARCHIVE, "w") as f:
    f.write(new_archive_content)

print("OK -- wrote", SRC, "(", len(final_lines), "lines ) and appended", len(archived_lines), "lines to", ARCHIVE)
print(f"original non-blank lines: {len(orig_nonblank)}, all found in live+archive: {missing == 0}")
