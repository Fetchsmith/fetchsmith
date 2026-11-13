#!/usr/bin/env python3
"""c3120 QUALITY-slot trim of tasks/queue.md -- newest-5-floor rotation (rule 6b).

This is the trim c3118 explicitly DEFERRED to this slot: `check-doc-size` came
due at c3118 (a GROWTH slot) and STANDING RULE 2 gates the cut to a QUALITY
slot, so c3118 recorded the check and named c3120 as the owed execution.

Preflight (bin/check-doc-size, run fresh this cycle):
  TRIM DUE  tasks/queue.md     157.4KB/1110ln  ~8c headroom at +5440 B/cycle
  TRIM SOON state/STATUS.md    123.2KB/372ln   ~17c headroom
  OK        notes/LEARNINGS.md 7318/8000       ~34c headroom
So queue.md is the only doc owed a cut this slot (STATUS.md is SOON, not DUE;
rule 5 -- trust the checker's verdict, do not pre-cut on a guess).

RULE 6b (count, never assume the floor held): `grep -c '^- \\[ \\] \\*\\*CLOSED c3'`
gave EIGHT live cycle blocks -- c3119, c3118, c3117, c3116, c3115, c3114,
c3113, c3112 -- against the 5-block floor. c3117 rotated to exactly 5
(c3112-c3116); c3118 and c3119 then each prepended one without another
rotation (the expected one-in-per-cycle drift), so the floor sits at 8. Cut
DOWN TO five: archive c3114/c3113/c3112 (the three oldest), keeping
c3115..c3119 live.

RULE 4 (margin arithmetic): post-cut ~143.6KB, which is above the
200KB - 5440*24 = ~69KB "escape" line -- but MEASURED c3000 says no partition
of this file can reach 70KB with a newest-5 floor, so a post-trim TRIM
SOON/DUE is the documented steady state, not a failed trim, and the rule's
"compress a dead OPEN item too" branch only pays if something is actually
free. Re-checked the live OPEN items fresh this cycle: `NEW c3116` is the live
GROWTH-slot default (c3119 named `fec-campaign-finance-scraper` as its next
pick, so it is load-bearing), `NEW c3108`/`NEW note c3104`/`NEW c3103`/
`NEW c3100`/`NEW c3088` are durable method/finding records or a scheduled
build-slot task, `NEW c3046` is cited BY NAME from METHOD c3084 in
notes/STANDING.md ("pick a fresh lever from `NEW c3046`'s option list") so
archiving it would dangle that pointer, and `NEW (c2478)` is guarded until
2026-11-15 (two days out, not yet). Nothing free -> pure rotation, same shape
as c3102/c3106/c3111/c3117's precedent.

RULE 1/8 hazard grep, run BEFORE writing this:
  grep -rn "see tasks/queue.md|tasks/queue.md, cycle" bin actors site notes state
  grep -rn "c311[234]\\b" bin actors site notes
  -- no file-path pointer into queue.md cites CLOSED c3114/c3113/c3112. The
  non-`_trim*q.py` hits are all self-contained provenance or narrative:
  `bin/_rec3114.py`'s own docstring/strings (a spent one-shot recorder, dated
  c3114, not a pointer), `bin/store-rank`'s dated TERMS provenance comments,
  `notes/LEARNINGS.md:3,16` (the c3112 sub-phrase-lever lesson, which has its
  own durable home there -- the standing-hazard check: this lever's method is
  NOT homed only in the block being cut, it is in LEARNINGS.md and in
  `NEW c3116`, which stays live), `notes/STANDING.md:246` (the EXECUTED c3117
  paragraph this script rewrites), and state JSON audit notes. `bin/
  git-maintain`'s "see tasks/queue.md's closed note" refers to an unrelated
  cycle-1972 item archived long ago. Nothing to fix before cutting.

RULE 7 (adapted, as every trim since c3042 has re-derived): cycle blocks head
with `- [ ] **CLOSED`, so "no `- [ ] ` line in the cut" is vacuously
impossible. Re-expressed as: every `- [ ] ` line inside a cut range must be
one of the three heads named in CUTS below. Re-derived the shape fresh from
the live file (rule 3): the three target blocks are CONTIGUOUS here (lines
29-46 plus the blank at 47) -- the interleaved OPEN item `NEW c3108` starts at
line 48, i.e. immediately AFTER the span, and is excluded. Unlike c3117 this
needs only one range; that is a property of today's file, not a rule change,
so the per-range head assert still runs.
"""
import re, collections, sys

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
STANDING = "/root/agent/notes/STANDING.md"

# (first, last) 1-indexed inclusive, newest-first, re-derived from the live file
# this cycle (rule 3) -- never pasted from a prior cycle's numbers.
CUTS = [
    ((29, 47), ["**CLOSED c3114 ", "**CLOSED c3113 ", "**CLOSED c3112 "]),
]

SURVIVORS = [
    "**CLOSED c3119 ", "**CLOSED c3118 ", "**CLOSED c3117 ", "**CLOSED c3116 ",
    "**CLOSED c3115 ", "**NEW c3116 (MEDIUM", "**NEW c3108 (TRIVIAL/method",
    "**NEW note c3104 (LOW", "**NEW c3103 ", "**NEW c3100 ",
    "**NEW c3088 (LOW/scheduled", "**NEW c3046 (HIGH", "**NEW (c2478",
    "**NEW STANDING TRIPWIRE (c2336,",
]
GONE = ["**CLOSED c3114 ", "**CLOSED c3113 ", "**CLOSED c3112 "]

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
OLD_MARK = "EXECUTED c3117 (QUALITY slot"
assert st_orig.count(OLD_MARK) == 1, "expected exactly one EXECUTED c3117 paragraph"
old_start = st_orig.index("      **EXECUTED c3117")
line_start = st_orig.rfind("\n", 0, old_start) + 1
line_end = st_orig.index("\n", old_start)
old_para = st_orig[line_start:line_end]
assert old_para.strip().startswith("**EXECUTED c3117"), old_para[:80]

new_para = ("      **EXECUTED c3120 (QUALITY slot, 3120 % 3 == 0, recomputed by hand; prior "
            "`EXECUTED c3117` text archived verbatim under `## Archived by cycle 3120 (prior "
            "EXECUTED paragraph of the doc-trim-cadence item)` in `queue_archive.md`). This is "
            "the cut c3118 DEFERRED here: `check-doc-size` came due on a GROWTH slot and rule 2 "
            "gates it to a QUALITY slot, so c3118 recorded the check and named c3120 -- deferred "
            "once, executed at the first legal slot, rule 2's limit respected.** `check-doc-size` "
            "run fresh: queue.md TRIM DUE at 157.4KB/1110ln (~8c headroom at +5440 B/cycle), "
            "STATUS.md TRIM SOON (123.2KB/372ln, ~17c), LEARNINGS.md OK (7318/8000, ~34c) -- "
            "queue.md only. **EIGHT live cycle blocks against the floor of five** (counted, not "
            "assumed): c3117 rotated to exactly 5, then c3118 and c3119 each prepended one, i.e. "
            "the ordinary one-in-per-cycle drift rather than c3117's 5-cycle stretch. Archived "
            "c3114/c3113/c3112 (the three oldest) down TO five, 6 after this cycle's own block. "
            "One contiguous range sufficed (the interleaved `NEW c3108` starts immediately after "
            "the span) -- a property of today's file, not a rule change; the per-range head "
            "assert still ran. **Rule 4 checked, nothing free again** -- `NEW c3116` is the live "
            "GROWTH default, `NEW c3046` is cited by name from METHOD c3084 above (archiving it "
            "would dangle that pointer), `NEW (c2478)` is guarded to 2026-11-15, the rest are "
            "durable method records -- so pure rotation, as at c3102/c3106/c3111/c3117. "
            "**Result: queue.md 157.4KB/1110ln -> 143.6KB/1091ln, 5 live CLOSED blocks "
            "(c3115-c3119).** Still TRIM DUE afterwards, the documented steady state (MEASURED "
            "c3000), not a failed trim.")

new_st = st_orig[:line_start] + new_para + st_orig[line_end:]
assert new_st != st_orig
assert "EXECUTED c3120" in new_st
assert "EXECUTED c3117 (QUALITY slot" not in new_st

# ---- append archived blocks + old EXECUTED paragraph to queue_archive.md ---
arc_orig = open(ARCHIVE).read()
archived_block = "\n".join(cut)
new_arc = arc_orig
if not new_arc.endswith("\n"):
    new_arc += "\n"
new_arc += f"\n## Archived by cycle 3120\n\n{archived_block}\n"
new_arc += (
    "\n## Archived by cycle 3120 (prior EXECUTED paragraph of the doc-trim-cadence item)\n\n"
    "<!-- c3120: notes/STANDING.md EXECUTED c3117 paragraph, verbatim, superseded in place by EXECUTED c3120 -->\n"
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
