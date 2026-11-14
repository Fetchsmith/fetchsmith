#!/root/agent/venv/bin/python
"""One-shot lossless trim for cycle 3204 (QUALITY slot, 3204 % 3 == 0).

`check-doc-size` reported ONLY tasks/queue.md TRIM DUE (162.0KB / 1168 lines,
~7 cycles of headroom, proj. 290KB at the next 24c look -- past both the 200KB
trim line and the 256KB Read cap). STATUS.md reads TRIM SOON (131.4KB, ~16
cycles) and is deliberately NOT touched: it is not due, and `check-doc-size`
names only queue.md.

This is the RULE 4 retirement pass `NEW c3188` has been asking for since c3188
and which c3202/c3203 both deferred -- NOT another bare CLOSED-block rotation.
The rotation lever is exhausted: the file already sits at the documented floor
of 5 live cycle blocks, and c3202's 6-block rotation only bought ~7 cycles.
So the mass cut here is consumed CLOSED/SHIPPED/RETIRED/COMPRESSED records
interleaved among the live tail -- material the block rotation structurally
cannot reach, because it is not a cycle block.

Ten cut ranges (file order) + one in-place pointer repair:
  R1  49-58   CLOSED c3198 -- the ordinary RULE 6b rotation half: 5 live blocks
              today (c3202..c3198), cut to 4 so cycle 3204's own block lands the
              file at exactly the floor of 5.
  R2  59-60   NEW c3188 (consumed -- this cycle IS its RULE 4 pass). NOTE: the
              first draft of this script used 59-62 and the per-range RULE 7
              assert caught it -- the LIVE `NEW c3200` (build bin/enum-canary)
              starts at L61, and the multiset check passed anyway because that
              live item would merely have been MOVED to the archive. Exactly
              the c2948 near-miss class. Re-derive, never widen a range to the
              next head.
  R3  112-112 NEW c3103 (closed record: "check-competitor-claims is now 0
              undated/stale fleet-wide"; superseded by the live `NEW c3168
              (handoff, updated c3189)` which tracks that backlog's CURRENT
              state, 1 STALE + 1 UNDATED)
  R4  113-113 NEW c3100 (consumed: both findings "are now fixed in the pushed
              READMEs"; its one durable lesson -- re-fetch the OTHER live
              figures in a sentence whose count you are fixing -- is homed in
              notes/LEARNINGS.md:5729, verified before cutting)
  R5  122-130 CLOSED c3105 -- the whole `NEW c3084` queue/STANDING split record
              incl. its PROGRESS c3087/c3090/c3105 paragraphs. Its own text:
              "split is now fully executed across all 3 slices -- do not
              re-open it". 7.5KB, the largest consumed record in the file.
  R6  131-132 RESOLVED same-cycle c3070 (transient read glitch, no action)
  R7  137-138 SHIPPED c3053 ("do NOT re-build or re-measure this") incl. the
              struck-through superseded `NEW c3052` spec it closes
  R8  141-142 RETIRED c3024 ("this is a closed record, not a tracker. Do not
              re-open it.")
  R9  147-148 COMPRESSED c3009 (GROWTH slot CLOSED NEGATIVE; its "NEXT GROWTH
              SLOT" pointer is superseded by `NEW c3116`/`NEW c3046`)
  R10 149-150 COMPRESSED c3007 (RULE 6 anchor-map, both CLOSED NEGATIVE)
  REWRITE 133 repairs the one real dangling pointer the RULE 1/8 hazard grep
              found: `NEW c3046` cites "(see `SHIPPED c3053` below)", and that
              block is cut in R7. Re-aimed at the archive. Applied AFTER the
              multiset check so the edit is deliberate, not silent.

DELIBERATELY NOT CUT, so a future trim does not re-litigate them:
  * `COMPRESSED c3008` (L143, 2.2KB) -- it is the direct context for the LIVE
    `NEW note (c3008)` open follow-up immediately below it (L145). Archiving the
    parent while keeping the child is the one thing RULE 8 warns about.
  * `DECIDED c3081` (L116, 4.8KB) -- a DEFER with two named live re-open
    triggers (buyer signal on trademark-search-scraper; sustained zero-row
    watchLabel runs). It is COMPRESSIBLE, not retirable: next trim should keep
    a ~600B live stub (decision + the two triggers + archive pointer) and move
    the 4 reasons / suggested shape verbatim. Worth ~4.2KB.
  * `COMPRESSED c3000` (L151, 9.0KB, the largest live item) -- STILL OPEN HIGH
    value, carries RULES 1-5 of the Store-ranking lever that actually pays.
    Per c2934's standing finding, cutting it trades real operational content
    for bytes. The structural option (move to notes/STANDING.md, as c3084's
    split did) needs its own hazard-grep pass and a full QUALITY slot.
  * `NEW (c2478)` (L845, 4.5KB) -- its 2026-11-15 deadline is TOMORROW; the
    first cycle on/after that date settles it outright. Largest free item left.

Dry-run by default; pass --write to apply. The keep/moved partition is asserted
total, non-overlapping and multiset-identical to the original before anything is
written.
"""
import sys, os

ROOT = "/root/agent"
WRITE = "--write" in sys.argv

HDR = ("## Archived by cycle 3204 (opus-5), 2026-11-14 -- tasks/queue.md RULE 4 "
       "retirement pass (the pass `NEW c3188` asked for; the CLOSED-block rotation "
       "was exhausted at the floor of 5). Retired: CLOSED c3198 (rotation), NEW c3188 "
       "(consumed), NEW c3103, NEW c3100, CLOSED c3105 (+PROGRESS c3087/c3090/c3105), "
       "RESOLVED c3070, SHIPPED c3053 (+the struck-through NEW c3052 spec), RETIRED "
       "c3024, COMPRESSED c3009, COMPRESSED c3007. Moved here VERBATIM, in source-file "
       "order.\n")


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


print("== tasks/queue.md: RULE 6b rotation to 4 + RULE 4 retirement pass ==")
q = read("tasks/queue.md")

CUTS = [(49, 58), (59, 60), (112, 112), (113, 113), (122, 130),
        (131, 132), (137, 138), (141, 142), (147, 148), (149, 150)]

# RULE 7 (c3048 adaptation): EXACTLY ONE item head per range, and it is that
# range's own head -- expressed as the ordered list of heads expected in the cut.
EXPECT_HEADS = [
    "- [ ] **CLOSED c3198",
    "- [ ] **NEW c3188",
    "- [ ] **NEW c3103",
    "- [ ] **NEW c3100",
    "- [x] **CLOSED c3105",
    "- [x] **RESOLVED same-cycle c3070",
    "- [x] **SHIPPED c3053",
    "- [ ] **RETIRED c3024",
    "- [ ] **COMPRESSED c3009",
    "- [ ] **COMPRESSED c3007",
]

# heads that MUST survive (RULE 7/8: no live work may ride along)
MUST_SURVIVE = [
    "- [ ] **CLOSED c3202", "- [ ] **CLOSED c3201", "- [ ] **CLOSED c3200",
    "- [ ] **CLOSED c3199", "- [x] **CLOSED c3203",
    "- [ ] **NEW c3200", "- [ ] **NEW c3168 (handoff",
    "- [ ] **NEW c3168 findings", "- [ ] **NEW c3167 (handoff",
    "- [ ] **NEW c3162 (MEDIUM)", "- [ ] **NEW c3148", "- [ ] **NEW c3116",
    "- [ ] **NEW c3046", "- [x] **DECIDED c3081",
    "- [ ] **COMPRESSED c3008", "- [ ] **NEW note (c3008",
    "- [ ] **COMPRESSED c3000", "- [ ] **NEW (c2478",
    "- [ ] **NEW STANDING TRIPWIRE (c2336",
    "- [ ] **NEW STANDING PREFLIGHT STEP (c3020",
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

# in-place pointer repair (breaks the identity by design -> applied AFTER the check)
OLD_P = "(see `SHIPPED c3053` below)"
NEW_P = ("(see `CLOSED c3053` / `SHIPPED c3053` in `tasks/queue_archive.md`, "
         "archived by cycle 3204)")
hits = [k for k, l in enumerate(q_keep) if OLD_P in l]
check(len(hits) == 1, f"pointer repair matched {len(hits)} lines, expected 1")
if len(hits) == 1:
    q_keep[hits[0]] = q_keep[hits[0]].replace(OLD_P, NEW_P)

q_keep_txt = "".join(q_keep)
q_moved_txt = "".join(q_moved)
print(f"  {len(q)} lines / {kb(''.join(q)):.1f}KB -> {len(q_keep)} kept / "
      f"{kb(q_keep_txt):.1f}KB, {len(q_moved)} moved ({kb(q_moved_txt):.1f}KB), "
      f"1 pointer repaired")

live_blocks = sum(1 for l in q_keep if l.startswith("- [ ] **CLOSED c3"))
print(f"  live cycle blocks after cut: {live_blocks} (floor 5; cycle 3204's own "
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
    f.write("\n" + HDR + "\n" + q_moved_txt)
with open(os.path.join(ROOT, "tasks/queue.md"), "w", encoding="utf-8") as f:
    f.write(q_keep_txt)

# post-write losslessness: prior archive byte-intact, every moved line present
qa_after = "".join(read("tasks/queue_archive.md"))
assert qa_after.startswith(qa_before), "prior queue_archive.md content was altered"
assert q_moved_txt in qa_after, "moved text is not verbatim in the archive"
live_after = "".join(read("tasks/queue.md"))
assert live_after == q_keep_txt, "live file does not match the computed keep half"
print(f"\nWROTE. queue.md {kb(''.join(q)):.1f}KB -> {kb(live_after):.1f}KB; "
      f"archive {kb(qa_before):.1f}KB -> {kb(qa_after):.1f}KB. Lossless asserts green.")
