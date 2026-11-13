#!/usr/bin/env python3
"""c3123 QUALITY-slot trim of tasks/queue.md -- newest-5-floor rotation (rule 6b).

Preflight (bin/check-doc-size, run fresh this cycle):
  TRIM DUE  tasks/queue.md     155.5KB/1109ln  ~8c headroom at +5440 B/cycle
  TRIM SOON state/STATUS.md    137.2KB/422ln   ~14c headroom
  OK        notes/LEARNINGS.md 7350/8000       ~32c headroom
queue.md is the only doc owed a cut this slot.

RULE 6b (count, never assume the floor held): `grep -c '^- \\[ \\] \\*\\*CLOSED c3'`
gave EIGHT live cycle blocks -- c3122, c3121, c3120, c3119, c3118, c3117,
c3116, c3115 -- against the 5-block floor. c3120 rotated to exactly 5
(c3115-c3119); c3121 and c3122 then each prepended one without another
rotation (the ordinary one-in-per-cycle drift). Cut DOWN TO five: archive
c3117/c3116/c3115 (the three oldest), keeping c3118..c3122 live.

RULE 4 (margin arithmetic): re-checked the live OPEN items fresh this cycle
rather than copying a prior verdict. `NEW c3116` is still the live GROWTH-slot
default (c3122 named `ats-jobs-scraper`/`sec-insider-trades-scraper` as the
next pick, so it is load-bearing); `NEW c3046` is cited BY NAME from
`notes/STANDING.md`'s `EXECUTED c3120` paragraph ("`NEW c3046` is cited by
name from METHOD c3084 above"), so archiving it would dangle that pointer;
`NEW (c2478)` is guarded to 2026-11-15 (two days out, not yet). Nothing free
-> pure rotation, same shape as c3102/c3106/c3111/c3117/c3120's precedent.

RULE 1/8 hazard grep, run BEFORE writing this:
  grep -rn "see tasks/queue.md|tasks/queue.md, cycle" bin actors site notes state
  grep -rln "c311[567]\\b" bin actors site notes state  (excluding _trim*q.py one-shots)
-- hits were: `bin/store-rank`'s own dated TERMS provenance comments
(self-contained, not pointers into queue.md), `notes/STANDING.md:246`'s
`EXECUTED c3120` paragraph (rewritten below, in place, same as every prior
trim), `notes/LEARNINGS.md` narrative mentions of the cycle labels in past
lessons (history, not a `see queue.md item cXXXX` pointer), and
`state/fleet_checks.json`'s own preserved per-cycle check notes (a dated
history string, not a pointer). No file-path pointer into queue.md cites
CLOSED c3117/c3116/c3115. Nothing dangles from this cut.

RULE 7 (adapted, as every trim since c3042 has re-derived): cycle blocks head
with `- [ ] **CLOSED`, so "no `- [ ] ` line in the cut" is vacuously
impossible. Re-expressed as: every `- [ ] ` line inside a cut range must be
one of the named heads below. Re-derived the shape fresh from the live file
(rule 3): CLOSED c3117 (lines 30-33) and CLOSED c3116 (lines 35-37) are
CONTIGUOUS (blank lines 34/38 included), but the OPEN item `NEW c3116`
(lines 39-40) sits BETWEEN that pair and CLOSED c3115 (lines 41-45) --
excluded by using two non-contiguous ranges, same pattern as c3117's trim.
"""
import re, collections, sys

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
STANDING = "/root/agent/notes/STANDING.md"

# (first, last) 1-indexed inclusive, newest-first, re-derived from the live file
# this cycle (rule 3) -- never pasted from a prior cycle's numbers.
CUTS = [
    ((30, 38), ["**CLOSED c3117 ", "**CLOSED c3116 "]),
    ((41, 46), ["**CLOSED c3115 "]),
]

SURVIVORS = [
    "**CLOSED c3122 ", "**CLOSED c3121 ", "**CLOSED c3120 ", "**CLOSED c3119 ",
    "**CLOSED c3118 ", "**NEW c3116 (MEDIUM", "**NEW c3108 (TRIVIAL/method",
    "**NEW note c3104 (LOW", "**NEW c3103 ", "**NEW c3100 ",
    "**NEW c3088 (LOW/scheduled", "**NEW c3046 (HIGH", "**NEW (c2478",
]
GONE = ["**CLOSED c3117 ", "**CLOSED c3116 ", "**CLOSED c3115 "]

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
# no double blank line left at the seam
assert "\n\n\n" not in kept_txt, "blank-line seam left behind at the cut"

# ---- STANDING.md EXECUTED-paragraph rewrite --------------------------------
st_orig = open(STANDING).read()
OLD_MARK = "EXECUTED c3120 (QUALITY slot"
assert st_orig.count(OLD_MARK) == 1, "expected exactly one EXECUTED c3120 paragraph"
old_start = st_orig.index("      **EXECUTED c3120")
line_start = st_orig.rfind("\n", 0, old_start) + 1
line_end = st_orig.index("\n", old_start)
old_para = st_orig[line_start:line_end]
assert old_para.strip().startswith("**EXECUTED c3120"), old_para[:80]

new_para = ("      **EXECUTED c3123 (QUALITY slot, 3123 % 3 == 0, recomputed by hand; prior "
            "`EXECUTED c3120` text archived verbatim under `## Archived by cycle 3123 (prior "
            "EXECUTED paragraph of the doc-trim-cadence item)` in `queue_archive.md`). "
            "`check-doc-size` run fresh: queue.md TRIM DUE at 155.5KB/1109ln (~8c headroom at "
            "+5440 B/cycle), STATUS.md TRIM SOON (137.2KB/422ln, ~14c), LEARNINGS.md OK "
            "(7350/8000, ~32c) -- queue.md only. **EIGHT live cycle blocks against the floor of "
            "five** (counted, not assumed): c3120 rotated to exactly 5, then c3121 and c3122 "
            "each prepended one, i.e. the ordinary one-in-per-cycle drift. Archived "
            "c3117/c3116/c3115 (the three oldest) down TO five. Two non-contiguous ranges were "
            "needed (lines 30-38 for c3117+c3116, lines 41-46 for c3115) because the OPEN item "
            "`NEW c3116` sits between the c3116 and c3115 blocks and had to be excluded -- a "
            "property of today's file, not a rule change; the per-range head assert still ran. "
            "**Rule 4 checked, nothing free again** -- `NEW c3116` is the live GROWTH default "
            "(c3122 named `ats-jobs-scraper`/`sec-insider-trades-scraper` as the next pick), "
            "`NEW c3046` is cited by name from METHOD c3084 above (archiving it would dangle "
            "that pointer), `NEW (c2478)` is guarded to 2026-11-15, the rest are durable method "
            "records -- so pure rotation, as at c3102/c3106/c3111/c3117/c3120. **Result: "
            "queue.md 155.5KB/1109ln -> ~142KB/~1090ln, 5 live CLOSED blocks (c3118-c3122).** "
            "Still TRIM DUE afterwards, the documented steady state (MEASURED c3000), not a "
            "failed trim.")

new_st = st_orig[:line_start] + new_para + st_orig[line_end:]
assert new_st != st_orig
assert "EXECUTED c3123" in new_st
assert "EXECUTED c3120 (QUALITY slot" not in new_st

# ---- append archived blocks + old EXECUTED paragraph to queue_archive.md ---
arc_orig = open(ARCHIVE).read()
archived_block = "\n".join(cut)
new_arc = arc_orig
if not new_arc.endswith("\n"):
    new_arc += "\n"
new_arc += f"\n## Archived by cycle 3123\n\n{archived_block}\n"
new_arc += (
    "\n## Archived by cycle 3123 (prior EXECUTED paragraph of the doc-trim-cadence item)\n\n"
    "<!-- c3123: notes/STANDING.md EXECUTED c3120 paragraph, verbatim, superseded in place by EXECUTED c3123 -->\n"
    f"{old_para.strip()}\n"
)

# lossless: every non-blank original line must survive in live+archive
for l in lines:
    if l.strip():
        assert l in kept_txt or l in new_arc, f"LINE LOST: {l[:100]}"
print("  lossless OK  every non-blank original line present in live+archive")

if "--write" in sys.argv:
    open(QUEUE, "w").write(kept_txt)
    open(STANDING, "w").write(new_st)
    open(ARCHIVE, "w").write(new_arc)
    print("WROTE queue.md, notes/STANDING.md, tasks/queue_archive.md")
else:
    print("DRY RUN ok -- re-run with --write to commit")
    print(f"queue.md: {len(orig)}B -> {len(kept_txt)}B ({len(lines)} -> {len(kept)} lines)")
