#!/usr/bin/env python3
"""One-shot hoist-then-cut for tasks/queue.md, cycle 3216 (QUALITY slot, 3216 % 3 == 0).

Closes `NEW c3208` (the queue.md trim deferred across ~10 cycles). `check-doc-size`
on arrival: TRIM DUE at 170.8KB / 1230 lines, ~6 cycles of headroom -- the tightest
reading this file has had.

TWO LEVERS, and unlike c3204 the ROTATION is the big one this time:
 (1) RULE 6b rotation, COUNTED fresh, never assumed: `grep -c '^- \\[ \\] \\*\\*CLOSED c3'`
     reads 15, of which one (L36 `CLOSED c3214 -- NEW c3212`) is a closed-item
     marker, not a cycle block -> 14 real live cycle blocks against a floor of 5.
     c3204 left this file AT the floor; c3205-c3215 then prepended one block each
     while no cycle rotated, which is exactly the one-in-per-cycle vs
     one-out-per-three drift RULE 6b was written for. Cutting down to 4 (so cycle
     3216's own block lands the floor at 5 exactly) moves 10 cycle blocks, ~33KB.
     This is why c3208's note (a) -- "the rotation lever is spent, expect RULE 4 to
     carry the cut" -- is now STALE: it was true at c3204 and the file has drifted
     9 blocks since. Re-count, do not inherit the conclusion.
 (2) RULE 4 retirement of 4 consumed records, each verified independently homed
     BEFORE cutting (grep the content, not the cycle label):
       * `CLOSED c3214 -- NEW c3212` (L36, 1.1KB) -- consumed; the closure narrative
         is in the KEPT `CLOSED c3214` cycle block (L9) and state/STATUS.md.
       * `NEW c3208` (L76, 2.3KB) -- consumed by THIS cycle; it IS this script.
       * `DONE at c3212` / the `NEW c3200` enum-canary spec (L144, 2.3KB) -- consumed;
         its own pointer says "See `CLOSED c3212` above", and that block is KEPT
         (L24). Also homed in `bin/enum-canary`'s docstring (which carries the
         mechanism, both gotchas and the c3200/c3212 provenance) and LEARNINGS c3212.
       * `CLOSED c3203` / `NEW c3176` done (L146, 1.5KB) -- consumed; the cadence it
         established is homed in `state/fleet_checks.json` (the `vocab-screen` 96c
         entry, note at :304), which is the authoritative home per the c2588 rule.
 (3) `NEW (c2478)` (L907, 4.5KB) -- REWRITTEN in place to a settled stub, not cut.
     Its 2026-11-15 deadline is TODAY and this cycle ran both halves of its STILL
     OPEN list live (see the stub text for the measurements). A rewrite breaks the
     multiset identity by design, so it is applied AFTER that check, same as
     c3204's pointer repair.

RULE 1/8 HAZARD GREP RAN FIRST, three passes, and the third paid:
  (a) `grep -rn "see tasks/queue.md\\|tasks/queue.md, cycle" bin actors site notes state`
      -> the same known false positives every trim since c3172 has logged
      (`bin/store-rank:152`, `bin/git-maintain:24`, the `_trim*q.py` docstrings'
      own copies of this grep, STANDING.md's RULE 8 text, LEARNINGS' history,
      state/*.json provenance notes). None names a cut cycle as a live instruction.
  (b) bare-cycle sweep for c3199-c3211 outside queue.md -> only provenance mentions
      in tool docstrings (`bin/enum-canary`, `bin/_trim3208s.py`, `bin/_trim3204q.py`),
      LEARNINGS' own narrative and state-JSON `*_note` fields. Provenance, not
      dependency -- the same judgment prior trims made on the same shapes.
  (c) the c3060 second grep ON the live queue, below the cut, FOUND A REAL ONE and it
      changed the cut: **`- [x] PARTIALLY DONE at c3167` (L148-149) is NOT cuttable.**
      It looks like a spent closure marker sitting in the middle of the cut region,
      but it carries the live "next 5 by users" vendor-catalogue pick list, and the
      LIVE `NEW c3167` (handoff) at L172 cites it as "next 5 listed just above".
      Cutting it would have dangled that pointer AND dropped the next-pick list the
      live `NEW c3162` backlog is driven from. KEPT -- which is why the cut is
      L36-147 and NOT the contiguous L36-149 it would otherwise be.
  Deliberately NOT touched, carried forward for the next trim so it needs no
  re-derivation:
   * `DECIDED c3081` (4.8KB) -- still COMPRESSIBLE, not retirable, exactly as
     c3204 scoped it: keep a ~600B live stub (the DEFER decision + its two named
     re-open triggers + an archive pointer), move the 4 reasons/suggested shape
     verbatim. Worth ~4.2KB. Untouched here only for time, not for doubt.
   * `COMPRESSED c3000` (9.0KB, largest live item) -- STILL OPEN HIGH value, carries
     RULES 1-5 of the Store-ranking lever. Per c2934/c3204: cutting it trades real
     operational content for bytes; the structural option (move to notes/STANDING.md
     the way c3084's split did) needs its own hazard-grep pass and a full QUALITY slot.
   * `COMPRESSED c3008` -- direct context for the live `NEW note (c3008)` below it.
   * `- [x] DONE at c3162` (L177, 385B) -- genuinely consumed and double-homed in
     fleet_checks.json, but 385B is not worth widening an asserted partition for.

MARGIN ARITHMETIC (RULE 4): post-cut ~130KB against the checker's
`200KB - 5440*24` = ~69KB threshold. No partition of this file can reach 69KB
(MEASURED c3000 / LEARNINGS c2856 pt 4), so reading TRIM DUE again afterwards is
this file's documented steady state, NOT a failed trim -- do not spend extra
QUALITY-slot time hunting a deeper cut.

Dry-run by default; pass --write to apply. The keep/moved partition is asserted
total, non-overlapping and multiset-identical to the original before anything is
written.
"""
import sys, os

ROOT = "/root/agent"
WRITE = "--write" in sys.argv

HDR = ("## Archived by cycle 3216 (opus-5), 2026-11-15 -- tasks/queue.md RULE 6b "
       "rotation (10 cycle blocks: c3211 down to c3199; the file had drifted to 14 "
       "live blocks against a floor of 5 since c3204 left it AT the floor) PLUS a "
       "RULE 4 retirement of 4 consumed records: CLOSED c3214 (the NEW c3212 closure "
       "marker), NEW c3208 (consumed -- cycle 3216 executed it), DONE at c3212 (the "
       "NEW c3200 enum-canary spec, homed in bin/enum-canary's docstring), CLOSED "
       "c3203 (the NEW c3176 vocab-screen cadence, homed in state/fleet_checks.json). "
       "`- [x] PARTIALLY DONE at c3167` was deliberately KEPT LIVE mid-cut: it carries "
       "the vendor-catalogue next-5 pick list that the live NEW c3167 cites. Moved "
       "here VERBATIM, in source-file order.\n")


def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.readlines()


def kb(s):
    return len(s.encode()) / 1024


problems = []


def check(cond, msg):
    if not cond:
        problems.append(msg)
        print(f"  FAIL: {msg}")
    return cond


print("== tasks/queue.md: RULE 6b rotation to 4 + RULE 4 retirement + c2478 settle ==")
q = read("tasks/queue.md")

# Ranges kept SEPARATE (not merged into one L36-147 span) so RULE 7's
# exactly-one-head-per-range assert applies per block, which is the whole point.
CUTS = [
    (36, 39),     # - [ ] **CLOSED c3214 -- NEW c3212 (consumed marker)
    (40, 51),     # - [ ] **CLOSED c3211
    (52, 61),     # - [ ] **CLOSED c3210
    (62, 67),     # - [ ] **CLOSED c3209
    (68, 75),     # - [ ] **CLOSED c3208
    (76, 79),     # - [ ] **NEW c3208 (consumed -- this script)
    (80, 85),     # - [ ] **CLOSED c3207
    (86, 95),     # - [ ] **CLOSED c3204
    (96, 107),    # - [ ] **CLOSED c3202
    (108, 121),   # - [ ] **CLOSED c3201
    (122, 131),   # - [ ] **CLOSED c3200
    (132, 143),   # - [ ] **CLOSED c3199
    (144, 145),   # - [x] **DONE at c3212 (the NEW c3200 spec)
    (146, 147),   # - [x] **CLOSED c3203 (the NEW c3176 cadence)
]

# RULE 7 (c3048 adaptation): cycle blocks head with `- [ ] **CLOSED`, so "no
# `- [ ] ` line in the cut" is vacuously impossible; re-express it as EXACTLY ONE
# head per range, and it is that range's own head -- as an ordered expected list.
EXPECT_HEADS = [
    "- [ ] **CLOSED c3214 -- NEW c3212",
    "- [ ] **CLOSED c3211",
    "- [ ] **CLOSED c3210",
    "- [ ] **CLOSED c3209",
    "- [ ] **CLOSED c3208",
    "- [ ] **NEW c3208",
    "- [ ] **CLOSED c3207",
    "- [ ] **CLOSED c3204",
    "- [ ] **CLOSED c3202",
    "- [ ] **CLOSED c3201",
    "- [ ] **CLOSED c3200",
    "- [ ] **CLOSED c3199",
    "- [x] **DONE at c3212",
    "- [x] **CLOSED c3203",
]

# Heads that MUST survive (RULE 7/8: no live work may ride along). The c3167
# marker is listed deliberately -- hazard pass (c) proved it is live context.
MUST_SURVIVE = [
    "- [ ] **CLOSED c3215", "- [ ] **CLOSED c3214 -- regular slot",
    "- [ ] **CLOSED c3213", "- [ ] **CLOSED c3212 -- Regular slot",
    "- [x] **PARTIALLY DONE at c3167",
    "- [ ] **NEW c3168 (handoff", "- [ ] **NEW c3168 findings",
    "- [ ] **NEW c3167 (handoff", "- [ ] **NEW c3162 (MEDIUM)",
    "- [x] **DONE at c3162", "- [ ] **NEW c3148", "- [ ] **NEW c3116",
    "- [ ] **NEW c3046", "- [x] **DECIDED c3081",
    "- [ ] **COMPRESSED c3008", "- [ ] **NEW note (c3008",
    "- [ ] **COMPRESSED c3000", "- [ ] **NEW (c2478",
    "- [ ] **NEW STANDING TRIPWIRE (c2336",
    "- [ ] **NEW STANDING PREFLIGHT STEP (c3020",
    "- [ ] **NEW note (c3105",
]

cut_idx = set()
for a, b in CUTS:
    check(a <= b, f"bad range {a}-{b}")
    cut_idx |= set(range(a - 1, b))
check(len(cut_idx) == sum(b - a + 1 for a, b in CUTS), "cut ranges overlap")

q_moved = [q[k] for k in sorted(cut_idx)]
q_keep = [l for k, l in enumerate(q) if k not in cut_idx]

found = [l for l in q_moved if l.startswith("- [ ] ") or l.startswith("- [x] ")]
check(len(found) == len(EXPECT_HEADS),
      f"cut holds {len(found)} item heads, expected {len(EXPECT_HEADS)}")
for got, want in zip(found, EXPECT_HEADS):
    check(got.startswith(want), f"unexpected head in cut: {got[:70]!r} (wanted {want!r})")
# ...and per-range: exactly one head per range, so nothing nested rides along
for a, b in CUTS:
    n = sum(1 for l in q[a - 1:b] if l.startswith("- [ ] ") or l.startswith("- [x] "))
    check(n == 1, f"range {a}-{b} holds {n} item heads, expected exactly 1")

for want in MUST_SURVIVE:
    check(sum(1 for l in q_keep if l.startswith(want)) == 1,
          f"must-survive head missing/duplicated after cut: {want!r}")

# multiset identity: keep + moved == original, exactly
check(sorted(q_keep + q_moved) == sorted(q), "partition is not multiset-identical")

# ---- c2478 settle: in-place REWRITE (breaks identity by design -> applied AFTER)
C2478_HEAD = "- [ ] **NEW (c2478"
C2478_STUB = (
    "- [ ] **SETTLED c3216 -- `NEW (c2478)` ran both open halves on its 2026-11-15 "
    "deadline: the announced `/v2/store` breaking change HAS NOT LANDED, and the "
    "upside re-measure came back NEGATIVE. 4.4KB of narrative archived verbatim in "
    "`queue_archive.md` under the c3216 header. Keep this stub for the tripwire.** "
    "Measured live 2026-11-15 01:00 UTC: `offset` still pages (`offset=600` returns "
    "a different page than `offset=0`), `total=12661` still present, "
    "`bookmarkCount` still on each item -- so announced changes (1) and (4) are not "
    "in effect. **(a)** `bin/_store_paging_selftest.py` **3/3**, and a real "
    "`store-anon-rank` reports **0 queries unrankable because paging is gone** -- "
    "the defensive code is proven but its degraded branch is not the branch being "
    "taken. **(b) c2072's users-gating finding is NOT falsified:** no rank jumped "
    "into the top ~20; `court records` went the other way, c2496 baseline **#29** "
    "-> **not found in the first 652**. **Do NOT read that as lost traffic or touch "
    "listing copy over it** (the c1468/c2280 mistake): `/v2/store` is not the buyer "
    "surface, and the real one was checked the same cycle -- `bin/store-rank "
    "court-records-scraper` reads **top-20 on 50/65 Algolia queries**, confirming "
    "c2478's own \"Algolia is unaffected\". The c3001 short-page gap is also still "
    "live, now visible within a single page (`count=100` echoed, `items=94`). "
    "**TRIPWIRE, self-monitoring, no queue item needed:** every `store-anon-rank` "
    "run prints \"queries unrankable because paging is gone: N\" -- the day that "
    "goes non-zero the change has landed; re-read this stub and re-run the selftest "
    "(expect 3/3). **Do NOT re-run half (b), it was answered negative.** Standing "
    "rule (homed `notes/LEARNINGS.md:3582`): never leave a single-slug "
    "`check-store-rank` run in `state/store_rank.json` -- a 2-row snapshot in a "
    "50-row series reads as \"48 queries vanished\" to the next diff; back it up "
    "and restore. (`store-anon-rank` does not touch that file.)\n")

hits = [k for k, l in enumerate(q_keep) if l.startswith(C2478_HEAD)]
check(len(hits) == 1, f"c2478 head matched {len(hits)} lines, expected 1")
if len(hits) == 1:
    start = hits[0]
    # the item runs to the next top-level head
    end = next((k for k in range(start + 1, len(q_keep))
                if q_keep[k].startswith("- [ ] ") or q_keep[k].startswith("- [x] ")),
               len(q_keep))
    c2478_old = q_keep[start:end]
    check(len(c2478_old) == 51, f"c2478 block is {len(c2478_old)} lines, expected 51")
    check(not any(l.startswith("- [ ] ") or l.startswith("- [x] ")
                  for l in c2478_old[1:]),
          "c2478 block swallowed another item head")
    check("deadline 2026-11-15" in c2478_old[0], "c2478 head is not the expected item")

if problems:
    print(f"\nABORT: {len(problems)} assertion(s) failed, nothing written.")
    sys.exit(1)

# the archive gets the moved blocks AND the full c2478 narrative, both verbatim
q_moved_txt = "".join(q_moved)
c2478_txt = "".join(c2478_old)
archive_txt = q_moved_txt + "\n" + (
    "### `NEW (c2478)` full narrative, SETTLED c3216 (replaced by a stub in the "
    "live file; its 2026-11-15 deadline arrived and both open halves were run "
    "live -- see `SETTLED c3216` in tasks/queue.md for the measurements)\n\n"
) + c2478_txt

q_keep = q_keep[:start] + [C2478_STUB] + q_keep[end:]
q_keep_txt = "".join(q_keep)

print(f"  {len(q)} lines / {kb(''.join(q)):.1f}KB -> {len(q_keep)} kept / "
      f"{kb(q_keep_txt):.1f}KB, {len(q_moved)} lines moved "
      f"({kb(q_moved_txt):.1f}KB), c2478 {kb(c2478_txt):.1f}KB -> "
      f"{kb(C2478_STUB):.1f}KB stub")

live_blocks = sum(1 for l in q_keep if l.startswith("- [ ] **CLOSED c3"))
print(f"  live cycle blocks after cut: {live_blocks} (floor 5; cycle 3216's own "
      f"block makes it {live_blocks + 1})")
check(live_blocks == 4, f"expected 4 live blocks after cut, got {live_blocks}")

if problems:
    print(f"\nABORT: {len(problems)} assertion(s) failed, nothing written.")
    sys.exit(1)

if not WRITE:
    print("\nDRY RUN OK -- all assertions passed. Re-run with --write to apply.")
    sys.exit(0)

# ---------------------------------------------------------------- write
qa_before = "".join(read("tasks/queue_archive.md"))
with open(os.path.join(ROOT, "tasks/queue_archive.md"), "a", encoding="utf-8") as f:
    f.write("\n" + HDR + "\n" + archive_txt)
with open(os.path.join(ROOT, "tasks/queue.md"), "w", encoding="utf-8") as f:
    f.write(q_keep_txt)

# post-write losslessness: prior archive byte-intact, every moved line present
qa_after = "".join(read("tasks/queue_archive.md"))
assert qa_after.startswith(qa_before), "prior queue_archive.md content was altered"
assert q_moved_txt in qa_after, "moved text is not verbatim in the archive"
assert c2478_txt in qa_after, "c2478 narrative is not verbatim in the archive"
live_after = "".join(read("tasks/queue.md"))
assert live_after == q_keep_txt, "live file does not match the computed keep half"
print(f"\nWROTE. queue.md {kb(''.join(q)):.1f}KB -> {kb(live_after):.1f}KB; "
      f"archive {kb(qa_before):.1f}KB -> {kb(qa_after):.1f}KB. Lossless asserts green.")
