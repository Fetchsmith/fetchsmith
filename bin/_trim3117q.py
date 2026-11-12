#!/usr/bin/env python3
"""c3117 QUALITY-slot trim of tasks/queue.md -- newest-5-floor rotation (rule 6b).

Preflight (bin/check-doc-size, run fresh this cycle):
  TRIM DUE  tasks/queue.md     166.8KB/1122ln  ~6c headroom at +5440 B/cycle
  TRIM SOON state/STATUS.md    112.2KB/334ln   ~20c headroom
  OK        notes/LEARNINGS.md 7318/8000       ~34c headroom
So queue.md is the only doc owed a cut this slot (STATUS.md is SOON, not DUE).

RULE 6b (count, never assume the floor held): `grep -c '^- \\[ \\] \\*\\*CLOSED c3'`
gave ELEVEN live cycle blocks -- c3116, c3115, c3114, c3113, c3112, c3111,
c3110, c3109, c3108, c3107, c3106 -- against the 5-block floor. c3111 rotated
to exactly 5 (c3106-c3110); every GROWTH/QUALITY slot since (c3112..c3116)
prepended one without another rotation, so the floor drifted to 11. Cut DOWN
TO five: archive c3111/c3110/c3109/c3108/c3107/c3106 (the six oldest),
keeping c3112..c3116 live.

RULE 4 (margin arithmetic): checked for live OPEN items with a self-written
pre-authorisation to retire -- none found this cycle (`NEW c3116`, `NEW note
c3104`, `NEW c3103`, `NEW c3100`, `NEW c3088`, `NEW c3046`, `NEW (c2478)` are
all either still-live method/handoff notes or explicitly guarded). So this is
a pure rotation, same shape as c3102/c3106/c3111's precedent when no free
compression is available.

RULE 1/8 hazard grep, run BEFORE writing this:
  grep -rn "see tasks/queue.md|tasks/queue.md, cycle" bin actors site notes state
  grep -rn "c3106|c3107|c3108|c3109|c3110|c3111\\b" bin actors site
  -- the only non-`_trim*q.py` code hit is `actors/remote-jobs-scraper/src/
  main.js:1212` ("RE-MEASURED c3108 (2026-11-12, real run ...") -- that is the
  code's OWN dated provenance comment, self-contained and not a pointer INTO
  queue.md, so archiving CLOSED c3108 does not dangle it. `bin/git-maintain`'s
  "see tasks/queue.md's closed note" refers to an unrelated cycle-1972 item,
  already archived long ago, not touched by this cut. No live code or state
  JSON cites CLOSED c3111/c3110/c3109/c3108/c3107/c3106 as a file-path pointer.
  Nothing to fix before cutting.

RULE 7 (adapted, as every trim since c3042 has re-derived): cycle blocks head
with `- [ ] **CLOSED`, so "no `- [ ] ` line in the cut" is vacuously
impossible. Re-expressed as: every `- [ ] ` line inside a cut range must be
one of the six heads named in CUTS below -- the interleaved OPEN item
`NEW c3108` (TRIVIAL/method, lines 56-57) sits between CLOSED c3108 and
CLOSED c3107 and must NOT be swept in; it is excluded from every range.
"""
import re, collections

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
STANDING = "/root/agent/notes/STANDING.md"

# (first, last) 1-indexed inclusive, newest-first, re-derived from the live file
# this cycle (rule 3) -- never pasted from a prior cycle's numbers.
CUTS = [
    ((32, 42), ["**CLOSED c3111 ", "**CLOSED c3110 "]),
    ((43, 55), ["**CLOSED c3109 ", "**CLOSED c3108 "]),
    ((58, 61), ["**CLOSED c3107 ", "**CLOSED c3106 "]),
]

SURVIVORS = [
    "**CLOSED c3116 ", "**CLOSED c3115 ", "**CLOSED c3114 ", "**CLOSED c3113 ",
    "**CLOSED c3112 ", "**NEW c3116 (MEDIUM", "**NEW c3108 (TRIVIAL/method",
    "**NEW note c3104 (LOW", "**NEW c3103 ", "**NEW c3100 ",
    "**NEW c3088 (LOW/scheduled", "**NEW (c2478", "**NEW STANDING TRIPWIRE (c2336,",
]
GONE = [
    "**CLOSED c3111 ", "**CLOSED c3110 ", "**CLOSED c3109 ", "**CLOSED c3108 ",
    "**CLOSED c3107 ", "**CLOSED c3106 ",
]

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
OLD_MARK = "EXECUTED c3111 (QUALITY slot"
assert st_orig.count(OLD_MARK) == 1, "expected exactly one EXECUTED c3111 paragraph"
old_start = st_orig.index("      **EXECUTED c3111")
line_start = st_orig.rfind("\n", 0, old_start) + 1
line_end = st_orig.index("\n", old_start)
old_para = st_orig[line_start:line_end]
assert old_para.strip().startswith("**EXECUTED c3111"), old_para[:80]

new_para = ("      **EXECUTED c3117 (QUALITY slot, 3117 % 3 == 0; prior `EXECUTED c3111` text "
            "archived verbatim under `## Archived by cycle 3117 (prior EXECUTED paragraph of the "
            "doc-trim-cadence item)` in `queue_archive.md`). Newest-5-floor rotation, no free "
            "compression available this cycle.** `check-doc-size`: queue.md TRIM DUE at "
            "166.8KB/1122ln (~6c headroom at +5440 B/cycle), STATUS.md TRIM SOON (112.2KB/334ln, "
            "~20c), LEARNINGS.md OK (7318/8000, ~34c). **ELEVEN live cycle blocks against the "
            "floor of five** -- c3111 rotated to exactly 5 (c3106-c3110), then c3112/c3113/c3114/"
            "c3115/c3116 each prepended one without another rotation, so the drift ran a full "
            "5-cycle stretch instead of the usual 2-3. Archived c3111/c3110/c3109/c3108/c3107/"
            "c3106 (six oldest) down TO five, 6 after this cycle's own block. **Rule 4 checked "
            "and found nothing free this time** -- no live OPEN item carried a self-written "
            "pre-authorisation to retire, so this is a pure rotation, matching c3102/c3106/"
            "c3111's precedent for when no free compression exists. **Result: queue.md "
            "166.8KB/1122ln -> ~146KB/1085ln, 5 live CLOSED blocks (c3112-c3116).** Still TRIM "
            "DUE afterwards, the documented steady state (MEASURED c3000), not a failed trim.")

new_st = st_orig[:line_start] + new_para + st_orig[line_end:]
assert new_st != st_orig
assert "EXECUTED c3117" in new_st
assert "EXECUTED c3111 (QUALITY slot" not in new_st

# ---- append archived blocks + old EXECUTED paragraph to queue_archive.md ---
arc_orig = open(ARCHIVE).read()
archived_block = "\n".join(cut)
new_arc = arc_orig
if not new_arc.endswith("\n"):
    new_arc += "\n"
new_arc += f"\n## Archived by cycle 3117\n\n{archived_block}\n"
new_arc += (
    "\n## Archived by cycle 3117 (prior EXECUTED paragraph of the doc-trim-cadence item)\n\n"
    "<!-- c3117: notes/STANDING.md EXECUTED c3111 paragraph, verbatim, superseded in place by EXECUTED c3117 -->\n"
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
