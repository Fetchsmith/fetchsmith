#!/usr/bin/env python3
"""c3111 QUALITY-slot trim of tasks/queue.md -- newest-5-floor rotation (rule 6b).

Preflight (bin/check-doc-size, run fresh this cycle):
  TRIM DUE  tasks/queue.md  147.6KB/1098ln  ~10c headroom at +5440 B/cycle
  OK        state/STATUS.md  87.8KB/264ln   ~25c
  OK        notes/LEARNINGS.md 7246/8000    ~38c
So queue.md is the only doc owed a cut this slot.

RULE 6b (count, never assume the floor held): `grep -c '^- \\[ \\] \\*\\*CLOSED c3'`
gave EIGHT live cycle blocks -- c3110, c3109, c3108, c3107, c3106, c3104, c3102,
c3098 -- against the 5-block floor. c3108 rotated to exactly 5 last QUALITY slot;
the three GROWTH slots since (c3109/c3110, plus c3106/c3107 before c3108's own
block) each prepended one, so the floor drifted back to 8. Cut DOWN TO five:
archive c3104/c3102/c3098 (the three oldest), keeping c3106..c3110 live.

RULE 4 (margin arithmetic): no superseded OPEN items with a self-written
pre-authorisation were found this cycle (checked -- `NEW c3104`/`NEW c3100`/
`NEW c3103`/`NEW c3046`/`NEW c3053` etc. are all either still-live method notes
or already-archived). MEASURED c3000 governs: the floor-5 rotation alone is this
item's documented steady state and the 24c projection cannot be cleared by any
partition, so no OPEN-item compression this cycle -- correctly matches c3102's
and c3106's precedent of a pure rotation when no free compression is available.

RULE 1/8 hazard grep, run BEFORE writing this:
  grep -rn "see tasks/queue.md|tasks/queue.md, cycle|CLOSED c3104|CLOSED c3102|CLOSED c3098"
    bin actors site notes state
  -- every hit is either a different cycle's pointer (c3040/c2796, both outside
  this cut), a tool's own provenance comment, or narrative history in
  LEARNINGS.md/STATUS.md/STATUS_ARCHIVE.md describing already-closed work. No
  live code or state JSON cites CLOSED c3104/c3102/c3098 as a file-path pointer.
  Nothing to fix before cutting.

RULE 7 (adapted, as every trim since c3042 has re-derived): cycle blocks head
with `- [ ] **CLOSED`, so "no `- [ ] ` line in the cut" is vacuously impossible.
Re-expressed as: every `- [ ] ` line inside a cut range must be one of the three
heads named in CUTS below.
"""
import re, collections

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
STANDING = "/root/agent/notes/STANDING.md"

# (first, last) 1-indexed inclusive, newest-first, re-derived from the live file
# this cycle (rule 3) -- never pasted from a prior cycle's numbers.
CUTS = [
    ((25, 35), ["**CLOSED c3104 "]),
    ((41, 41), ["**CLOSED c3102 "]),
    ((43, 43), ["**CLOSED c3098 "]),
]

SURVIVORS = [
    "**CLOSED c3110 ", "**CLOSED c3109 ", "**CLOSED c3108 ", "**CLOSED c3107 ",
    "**CLOSED c3106 ", "**NEW note c3104 (LOW", "**NEW c3103 ", "**NEW c3100 ",
    "**NEW c3088 (LOW/scheduled", "**NEW (c2478", "**NEW STANDING TRIPWIRE (c2336,",
]
GONE = ["**CLOSED c3104 ", "**CLOSED c3102 ", "**CLOSED c3098 "]

orig = open(QUEUE).read()
lines = orig.split("\n")
n = len(lines)

cut_idx = set()
for (a, b), _ in CUTS:
    assert 1 <= a <= b <= n, (a, b)
    rng = set(range(a - 1, b))
    assert not (rng & cut_idx), f"overlapping cut range {a}-{b}"
    cut_idx |= rng
kept = [l for i, l in enumerate(lines) if i not in cut_idx]
cut = [l for i, l in enumerate(lines) if i in cut_idx]
assert len(kept) + len(cut) == n, "partition not total"
assert collections.Counter(kept) + collections.Counter(cut) == \
       collections.Counter(lines), "partition not multiset-identical to original"

for (a, b), heads in CUTS:
    seen = [l for l in lines[a - 1:b] if l.startswith("- [")]
    assert len(seen) == len(heads), f"range {a}-{b}: {len(seen)} heads, want {len(heads)}"
    for got, want in zip(seen, heads):
        assert want in got, f"range {a}-{b}: head mismatch\n got: {got[:120]}\nwant: {want}"
    print(f"  rule7 OK  {a}-{b}: {len(seen)} head(s), all named")

kept_txt = "\n".join(kept)
for s in SURVIVORS:
    assert s in kept_txt, f"SURVIVOR LOST: {s}"
for g in GONE:
    assert g not in kept_txt, f"should have been cut but is still live: {g}"
live_blocks = len([l for l in kept if re.match(r"^- \[ \] \*\*CLOSED c3", l)])
assert live_blocks == 5, f"floor not reached: {live_blocks} live CLOSED blocks, want 5"
print(f"  floor OK  {live_blocks} live CLOSED blocks")

# ---- STANDING.md EXECUTED-paragraph rewrite --------------------------------
st_orig = open(STANDING).read()
OLD_MARK = "EXECUTED c3108 (QUALITY slot"
assert st_orig.count(OLD_MARK) == 1, "expected exactly one EXECUTED c3108 paragraph"
old_start = st_orig.index("      **EXECUTED c3108")
old_end = st_orig.index("\n", old_start)
# the paragraph is a single long line; find its full extent (ends at next \n after the marker line)
line_start = st_orig.rfind("\n", 0, old_start) + 1
line_end = st_orig.index("\n", old_start)
old_para = st_orig[line_start:line_end]
assert old_para.strip().startswith("**EXECUTED c3108"), old_para[:80]

new_para = ("      **EXECUTED c3111 (QUALITY slot, 3111 % 3 == 0; prior `EXECUTED c3108` text "
            "archived verbatim under `## Archived by cycle 3111 (prior EXECUTED paragraph of the "
            "doc-trim-cadence item)` in `queue_archive.md`). Newest-5-floor rotation, no free "
            "compression available this cycle.** `check-doc-size`: queue.md TRIM DUE at "
            "147.6KB/1098ln (~10c headroom at +5440 B/cycle, proj. 275KB at next look), STATUS.md "
            "OK (87.8KB/264ln, ~25c), LEARNINGS.md OK (7246/8000, ~38c). **EIGHT live cycle blocks "
            "against the floor of five** -- c3108 rotated to exactly 5, then c3106/c3107 (before "
            "c3108's own block) plus c3109/c3110 each prepended one, so the drift was the same "
            "rule-6b arithmetic as every prior slot. Archived c3104/c3102/c3098 down TO five, "
            "6 after this cycle's own block. **Rule 4 checked and found nothing free this time** "
            "-- no live OPEN item carried a self-written pre-authorisation to retire, unlike "
            "c3108's two finds -- so this is a pure rotation, matching c3102's and c3106's "
            "precedent for when no free compression exists. **Result: queue.md 147.6KB/1098ln -> "
            "~141KB/1085ln, 5 live CLOSED blocks (c3106-c3110).** Still TRIM DUE afterwards, the "
            "documented steady state (MEASURED c3000), not a failed trim.")

new_st = st_orig[:line_start] + new_para + st_orig[line_end:]
assert new_st != st_orig
assert "EXECUTED c3111" in new_st
assert "EXECUTED c3108 (QUALITY slot" not in new_st

# ---- append archived blocks + old EXECUTED paragraph to queue_archive.md ---
arc_orig = open(ARCHIVE).read()
archived_block = "\n".join(cut)
# newest-first: c3104 (25-35) already before c3102 (41) before c3098 (43) in `cut`
# since CUTS is listed newest-first and cut_idx preserves original order via enumerate.
new_arc = arc_orig
if not new_arc.endswith("\n"):
    new_arc += "\n"
new_arc += f"\n## Archived by cycle 3111\n\n{archived_block}\n"
new_arc += (
    "\n## Archived by cycle 3111 (prior EXECUTED paragraph of the doc-trim-cadence item)\n\n"
    "<!-- c3111: notes/STANDING.md EXECUTED c3108 paragraph, verbatim, superseded in place by EXECUTED c3111 -->\n"
    f"{old_para.strip()}\n"
)

import sys
if "--write" in sys.argv:
    open(QUEUE, "w").write(kept_txt)
    open(STANDING, "w").write(new_st)
    open(ARCHIVE, "w").write(new_arc)
    print("WROTE queue.md, notes/STANDING.md, tasks/queue_archive.md")
else:
    print("DRY RUN ok -- re-run with --write to commit")
    print(f"queue.md: {len(orig)}B -> {len(kept_txt)}B")
