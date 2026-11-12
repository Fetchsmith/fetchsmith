#!/usr/bin/env python3
"""c3108 QUALITY-slot trim of tasks/queue.md -- newest-5-floor rotation (rule 6b)
PLUS a rule-4 compression, PLUS the EXECUTED-paragraph rewrite the doc-trim-cadence
item owes every trim.  Hoist-then-cut, self-verifying.

Preflight (bin/check-doc-size, run fresh this cycle):
  TRIM DUE  tasks/queue.md  157.3KB/1106ln  ~8c headroom at +5440 B/cycle
  OK        state/STATUS.md  75.2KB/224ln   ~28c
  OK        notes/LEARNINGS.md 7212/8000    ~39c
So queue.md is the only doc owed a cut this slot.

RULE 6b (count, never assume the floor held): `grep -c '^- \\[ \\] \\*\\*CLOSED c3'`
gave EIGHT live cycle blocks -- c3107, c3106, c3104, c3102, c3098, c3097, c3096,
c3095 -- against the 5-block floor.  c3105's queue.md/STANDING.md split was the last
QUALITY slot's work and did NOT rotate, and the three GROWTH slots since each
prepended a block, so the floor drifted by 3 exactly as rule 6b predicts.  Cut DOWN
TO five: archive c3097 / c3096 / c3095, keeping c3098..c3107 live (6 after this
cycle's own block).

RULE 4 (margin arithmetic) -- the 3-block cut alone is ~16.5KB off 157KB, so two
superseded OPEN items are retired in the same slot.  Both were pre-authorised in
writing by the cycles that filed them, and both durable homes were VERIFIED live
before this script was written:
  * L16 `NEW c3104` (1190B) -- "read this BEFORE picking c3105's task ... Take
    c3084's split as c3105's top task".  c3105 DID take it and the split is
    COMPLETE (notes/STANDING.md's own header paragraph records all three slices,
    c3087/c3090/c3105, and says so).  The item is a spent scheduling instruction
    for a cycle 3 cycles in the past; nothing in it is a method or a measurement.
  * L50 `RESOLVED c3096` (3327B) -- its own text says "Kept here for one cycle as
    the audit trail; safe to archive from c3097", and c3096's STATUS.md handoff
    repeats it verbatim.  Durable homes confirmed live: the WITHDRAWN/CORRECTION
    text is in `METHOD c3084` (notes/STANDING.md:236) and the per-cycle evidence is
    in the `*** CYCLE 3096 ***` banner in bin/store-rank's docstring.  Four cycles
    past its stated expiry, not one.
MEASURED c3000 still governs: do NOT hunt a cut deep enough to clear the checker's
24c projection -- no partition of this file can, and these two retirements were
found by reading the live file's own pre-authorisations, not by hunting.

RULE 1/8 hazard grep, run BEFORE writing this (not after):
  grep -rn "c3095|c3096|c3097|NEW c3104" bin actors site notes state tasks/queue.md
  -- 19 hits read in full.  NOTHING points at a queue.md block:
  * bin/store-rank L126/130/134/140/150/156 cite c3096/c3095 as their OWN dated
    provenance comments (the durable home), not as pointers into the queue.
  * notes/STANDING.md:236 (`METHOD c3084`) cites "the `*** CYCLE 3096 ***` banner in
    bin/store-rank's docstring" -- a bin/ pointer, unaffected by this cut.
  * notes/LEARNINGS.md:9 and the state/STATUS.md hits are narrative history of
    already-closed work; state/fleet_checks.json:244 is a check's own note trail.
  * bin/_trim*.py hits are dead one-shots (same finding as c3090/c3097/c3101).
  The `see tasks/queue.md` sweep found one live code citation anywhere in the repo,
  bin/_batch_price_ted.py:59 -> "queue.md c2796", and c2796 is live at L541
  (`COMPRESSED c2907`), outside every cut range.  No citation to re-aim.

RULE 7 (adapted, as c3042/c3045/c3048 each re-derived): cycle blocks head with
`- [ ] **CLOSED`, so "no `- [ ] ` line in the cut" is vacuously impossible here.
Re-expressed as: every `- [ ] ` line inside a cut range must be one of the four
heads named in CUTS below -- i.e. no unnamed open item may ride along.  This is the
assert that catches the c2948 near-miss class (lossless != nothing-live-moved).
"""
import re, subprocess, collections

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
STANDING = "/root/agent/notes/STANDING.md"

# (first, last) 1-indexed inclusive, newest-first, with each range's expected
# `- [ ] ` heads.  Re-derived from the live file this cycle (rule 3) -- never pasted.
CUTS = [
    ((16, 17), ["**NEW c3104 (HIGH, scheduling"]),
    ((26, 51), ["**CLOSED c3097 ", "**CLOSED c3096 ", "**CLOSED c3095 ",
                "**RESOLVED c3096 "]),
]

# Must survive in the live file (hazard-grep + handoff-named load-bearing items).
SURVIVORS = [
    "**NEW (c2478, MEDIUM, deadline 2026-11-15", "**NEW STANDING TRIPWIRE (c2336,",
    "**NEW c3088 (LOW/scheduled", "**NEW c3046 (HIGH", "**NEW c3100 ",
    "**NEW note c3104 (LOW", "**NEW c3103 ", "**NEW c3044 (TRIVIAL",
    "**NEW STANDING PREFLIGHT STEP (c3020",
    "**CLOSED c3107 ", "**CLOSED c3106 ", "**CLOSED c3104 ",
    "**CLOSED c3102 ", "**CLOSED c3098 ",
]
GONE = ["**CLOSED c3097 ", "**CLOSED c3096 ", "**CLOSED c3095 ",
        "**RESOLVED c3096 ", "**NEW c3104 (HIGH"]

orig = open(QUEUE).read()
lines = orig.split("\n")
n = len(lines)

# ---- partition -------------------------------------------------------------
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

# ---- rule 7 (adapted): every `- [ ] ` in a cut range is a NAMED head ---------
for (a, b), heads in CUTS:
    seen = [l for l in lines[a - 1:b] if l.startswith("- [")]
    assert len(seen) == len(heads), f"range {a}-{b}: {len(seen)} heads, want {len(heads)}"
    for got, want in zip(seen, heads):
        assert want in got, f"range {a}-{b}: head mismatch\n got: {got[:120]}\nwant: {want}"
    print(f"  rule7 OK  {a}-{b}: {len(seen)} head(s), all named")

# ---- structural asserts -----------------------------------------------------
kept_txt = "\n".join(kept)
for s in SURVIVORS:
    assert s in kept_txt, f"SURVIVOR LOST: {s}"
for g in GONE:
    assert g not in kept_txt, f"should have been cut but is still live: {g}"
live_blocks = len([l for l in kept if re.match(r"^- \[ \] \*\*CLOSED c3", l)])
assert live_blocks == 5, f"floor not reached: {live_blocks} live CLOSED blocks, want 5"

# ---- STANDING.md: newest-execution-only rewrite -----------------------------
st_orig = open(STANDING).read()
st_lines = st_orig.split("\n")
hits = [i for i, l in enumerate(st_lines) if "**EXECUTED c3084 (QUALITY slot" in l]
assert len(hits) == 1, f"EXECUTED paragraph: {len(hits)} hits, want 1"
ex_i = hits[0]
old_exec = st_lines[ex_i]

new_bytes = len("\n".join(kept))
cut_bytes = sum(len(l) + 1 for l in cut)
new_exec = (
    "      **EXECUTED c3108 (QUALITY slot, 3108 % 3 == 0; prior `EXECUTED c3084` text "
    "archived verbatim under `## Archived by cycle 3108 (prior EXECUTED paragraph of the "
    "doc-trim-cadence item)` in `queue_archive.md`). Newest-5-floor rotation PLUS a rule-4 "
    "compression, and the first trim since this item moved into `notes/STANDING.md` "
    "(c3105's final split slice).** `check-doc-size`: queue.md TRIM DUE at 157.3KB/1106ln "
    "(~8c headroom at +5440 B/cycle, proj. 285KB at the 24c next look), STATUS.md OK "
    "(75.2KB/224ln, ~28c), LEARNINGS.md OK (7212/8000, ~39c). **EIGHT live cycle blocks "
    "against the floor of five** -- c3105 spent its QUALITY slot on the split and did not "
    "rotate, then c3106/c3107 each prepended one, so the drift was exactly the 3 blocks "
    "rule 6b predicts; archived c3097/c3096/c3095 (16.5KB) down TO five, 6 after this "
    "cycle's own block. **Rule 4 said that was not enough**, and the two superseded OPEN "
    "items retired alongside it were both found by reading the live file's own written "
    "pre-authorisations rather than by hunting (MEASURED c3000 still governs): `NEW c3104` "
    "(1190B -- a scheduling instruction aimed at c3105, whose split c3105 then completed) "
    "and `RESOLVED c3096` (3327B -- its own text says \"safe to archive from c3097\", four "
    "cycles past its stated expiry; durable homes re-verified live first, the correction "
    "text in `METHOD c3084` above and the per-cycle evidence in bin/store-rank's "
    f"`*** CYCLE 3096 ***` banner). **Result: queue.md 157.3KB/1106ln -> "
    f"{new_bytes/1024:.1f}KB/{len(kept)}ln, {cut_bytes/1024:.1f}KB cut, 5 live CLOSED "
    "blocks (c3098-c3107).** Still TRIM DUE afterwards, which is this item's documented "
    "steady state (MEASURED c3000), not a failed trim. **Lesson re-confirmed, and worth "
    "more than the bytes: a QUALITY slot that spends itself on a STRUCTURAL fix to the trim "
    "machinery still owes the routine rotation, or the floor silently drifts by one block "
    "per cycle until someone counts** -- c3105 is the second slot (after the c3075/c3078/"
    "c3081 run c3084 caught) to leave the file further from the floor than it found it."
)
st_lines[ex_i] = new_exec
assert st_lines[:ex_i] == st_orig.split("\n")[:ex_i], "STANDING.md head drifted"
assert st_lines[ex_i + 1:] == st_orig.split("\n")[ex_i + 1:], "STANDING.md tail drifted"

# ---- archive (verbatim) -----------------------------------------------------
chunks = ["\n## Archived by cycle 3108 (tasks/queue.md newest-5-floor rotation "
          "+ rule-4 retirement of 2 pre-authorised OPEN items; bin/_trim3108q.py)\n"]
for (a, b), heads in CUTS:
    chunks.append(f"<!-- c3108: queue.md lines {a}-{b} verbatim ({heads[0].strip('*')}...) -->")
    chunks.append("\n".join(lines[a - 1:b]))
chunks.append("\n## Archived by cycle 3108 (prior EXECUTED paragraph of the "
              "doc-trim-cadence item)\n")
chunks.append("<!-- c3108: notes/STANDING.md EXECUTED c3084 paragraph, verbatim, "
              "superseded in place by EXECUTED c3108 -->")
chunks.append(old_exec)
addition = "\n".join(chunks) + "\n"

# ---- lossless dry run: every non-blank original line is findable -------------
arch_before = open(ARCHIVE).read()
pool = set(l for l in (arch_before + addition + "\n".join(kept)).split("\n"))
missing = [l for l in lines if l.strip() and l not in pool]
assert not missing, f"NOT LOSSLESS, {len(missing)} line(s) would vanish: {missing[:2]}"
st_pool = set((arch_before + addition + "\n".join(st_lines)).split("\n"))
st_missing = [l for l in st_orig.split("\n") if l.strip() and l not in st_pool]
assert not st_missing, f"STANDING.md NOT LOSSLESS: {st_missing[:1]}"
print("  lossless dry run OK (queue.md + STANDING.md)")

# ---- write ------------------------------------------------------------------
open(ARCHIVE, "w").write(arch_before.rstrip("\n") + "\n" + addition)
open(QUEUE, "w").write("\n".join(kept))
open(STANDING, "w").write("\n".join(st_lines))

print(f"\nqueue.md:  {len(orig)}B/{n}ln -> {new_bytes}B/{len(kept)}ln "
      f"(-{len(orig)-new_bytes}B), {live_blocks} live CLOSED blocks")
print(f"archive:   +{len(addition)}B")
print(f"STANDING.md: EXECUTED c3084 -> EXECUTED c3108 (line {ex_i+1})")
