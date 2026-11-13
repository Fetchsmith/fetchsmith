#!/usr/bin/env python3
"""c3126 QUALITY-slot trim of tasks/queue.md -- newest-5-floor rotation (rule 6b).

Preflight (bin/check-doc-size, run fresh this cycle):
  TRIM DUE  tasks/queue.md     155.3KB/1110ln  ~8c headroom at +5440 B/cycle
  TRIM DUE  state/STATUS.md    152.0KB/468ln   ~11c headroom
  OK        notes/LEARNINGS.md 7350/8000       ~32c headroom
Both queue.md and STATUS.md are owed a cut this slot; this script is queue.md's
(see bin/_trim3126s.py for STATUS.md).

RULE 6b (count, never assume the floor held): `grep -c '^- \\[ \\] \\*\\*CLOSED c3'`
gave EIGHT live cycle blocks -- c3125, c3124, c3123, c3122, c3121, c3120,
c3119, c3118 -- against the 5-block floor. c3123 rotated to exactly 5
(c3118-c3122); c3124 and c3125 then each prepended one without another
rotation (the ordinary one-in-per-cycle drift). Cut DOWN TO five: archive
c3120/c3119/c3118 (the three oldest), keeping c3125..c3121 live.

RULE 1/8 hazard grep, run BEFORE writing this:
  grep -rn "see tasks/queue.md|tasks/queue.md, cycle" bin actors site notes state
  grep -rln "c312[0]\\b|c3119\\b|c3118\\b" bin actors site notes state (excluding _trim*q.py)
-- hits were: `bin/store-rank`'s own dated TERMS provenance comments (self-
contained, cite the cycle LABEL as history, not a pointer into queue.md),
`notes/STANDING.md:246`'s `EXECUTED c3123` paragraph (rewritten below, in
place, same as every prior trim), `notes/LEARNINGS.md` narrative mentions of
past lessons, and `state/fleet_checks.json`'s own preserved per-cycle check
note (a dated history string). No file-path pointer into queue.md cites
CLOSED c3120/c3119/c3118. Nothing dangles from this cut.

RULE 4 (margin arithmetic): re-checked the live OPEN items fresh. `NEW c3116`
is still the live GROWTH-slot default (c3125 named `us-federal-awards-scraper`
or `shopify-products-scraper` as the next pick, load-bearing); `NEW c3046` is
cited by name from `notes/STANDING.md`'s `METHOD c3084` paragraph (archiving
it would dangle that pointer); `NEW (c2478)` is guarded to 2026-11-15 (two
days out, not yet). Nothing free -> pure rotation, same shape as
c3102/c3106/c3111/c3117/c3120/c3123's precedent.

RULE 7 (adapted): cycle blocks head with `- [ ] **CLOSED`, so "no `- [ ] `
line in the cut" is vacuously impossible; re-expressed as "EXACTLY ONE
`- [ ] ` line per range, and it is that block's own head." Re-derived fresh
from the live file (rule 3): the three target blocks are CONTIGUOUS (lines
28-44 plus the blank separator at 45) -- the interleaved OPEN item
`NEW c3116` starts at line 46, immediately after the span, and is excluded.
One range suffices (a property of today's file, not a rule change); the
per-range head assert still runs.
"""
import re, collections, sys

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
STANDING = "/root/agent/notes/STANDING.md"

CUTS = [
    ((28, 45), ["**CLOSED c3120 ", "**CLOSED c3119 ", "**CLOSED c3118 "]),
]

SURVIVORS = [
    "**CLOSED c3125 ", "**CLOSED c3124 ", "**CLOSED c3123 ", "**CLOSED c3122 ",
    "**CLOSED c3121 ", "**NEW c3116 ", "**NEW c3108 ", "**NEW note c3104 ",
    "**NEW c3103 ", "**NEW c3100 ", "**NEW c3088 ", "**NEW c3046 ",
    "**NEW (c2478",
]
GONE = ["**CLOSED c3120 ", "**CLOSED c3119 ", "**CLOSED c3118 "]

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
assert "\n\n\n" not in kept_txt, "blank-line seam left behind at the cut"

# ---- STANDING.md EXECUTED-paragraph rewrite --------------------------------
st_orig = open(STANDING).read()
OLD_MARK = "EXECUTED c3123 (QUALITY slot"
assert st_orig.count(OLD_MARK) == 1, "expected exactly one EXECUTED c3123 paragraph"
old_start = st_orig.index("      **EXECUTED c3123")
line_start = st_orig.rfind("\n", 0, old_start) + 1
line_end = st_orig.index("\n", old_start)
old_para = st_orig[line_start:line_end]
assert old_para.strip().startswith("**EXECUTED c3123"), old_para[:80]

new_para = ("      **EXECUTED c3126 (QUALITY slot, 3126 % 3 == 0, recomputed by hand; prior "
            "`EXECUTED c3123` text archived verbatim under `## Archived by cycle 3126 (prior "
            "EXECUTED paragraph of the doc-trim-cadence item)` in `queue_archive.md`). "
            "`check-doc-size` run fresh: queue.md TRIM DUE at 155.3KB/1110ln (~8c headroom at "
            "+5440 B/cycle), STATUS.md ALSO TRIM DUE (152.0KB/468ln, ~11c headroom), "
            "LEARNINGS.md OK (7350/8000, ~32c) -- both live docs cut this slot, see "
            "`bin/_trim3126s.py` for STATUS.md's. **EIGHT live cycle blocks against the floor "
            "of five** (counted, not assumed): c3123 rotated to exactly 5, then c3124 and c3125 "
            "each prepended one, i.e. the ordinary one-in-per-cycle drift. Archived "
            "c3120/c3119/c3118 (the three oldest) down TO five. One contiguous range sufficed "
            "(lines 28-45, the interleaved `NEW c3116` starts immediately after) -- a property "
            "of today's file, not a rule change; the per-range head assert still ran. **Rule 4 "
            "checked, nothing free again** -- `NEW c3116` is the live GROWTH default (c3125 "
            "named `us-federal-awards-scraper`/`shopify-products-scraper` as the next pick), "
            "`NEW c3046` is cited by name from METHOD c3084 above, `NEW (c2478)` is guarded to "
            "2026-11-15, the rest are durable method records -- so pure rotation, as at "
            "c3102/c3106/c3111/c3117/c3120/c3123. **Result: queue.md 155.3KB/1110ln -> "
            "~142KB/~1091ln, 5 live CLOSED blocks (c3121-c3125).** Still TRIM DUE/SOON "
            "afterwards is the documented steady state (MEASURED c3000), not a failed trim.")

new_st = st_orig[:line_start] + new_para + st_orig[line_end:]
assert new_st != st_orig
assert "EXECUTED c3126" in new_st
assert "EXECUTED c3123 (QUALITY slot" not in new_st

# ---- append archived blocks + old EXECUTED paragraph to queue_archive.md ---
arc_orig = open(ARCHIVE).read()
archived_block = "\n".join(cut)
new_arc = arc_orig
if not new_arc.endswith("\n"):
    new_arc += "\n"
new_arc += f"\n## Archived by cycle 3126\n\n{archived_block}\n"
new_arc += (
    "\n## Archived by cycle 3126 (prior EXECUTED paragraph of the doc-trim-cadence item)\n\n"
    "<!-- c3126: notes/STANDING.md EXECUTED c3123 paragraph, verbatim, superseded in place by EXECUTED c3126 -->\n"
    f"{old_para.strip()}\n"
)

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
