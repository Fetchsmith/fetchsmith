#!/usr/bin/env python3
"""One-shot hoist-then-cut for tasks/queue.md, cycle 3225 (QUALITY slot, 3225 % 3 == 0).

Closes `NEW c3224` (the queue.md trim it filed for itself: 153.1KB/1113ln ~9c
headroom on arrival at c3224, now 158.1KB/1121ln ~8c headroom per `check-doc-size`
this cycle). Both `checks-due --all` and `audit-due --all` read NONE DUE this
cycle, so this HIGH-priority housekeeping item is the pick.

REAL FINDING BEFORE CUTTING, not just a rotation: RULE 6b's own counting command
(`grep -c '^- \\[ \\] \\*\\*CLOSED c3' tasks/queue.md`) read **5** on arrival, which
looks like "already at floor, nothing to rotate" -- but that count is WRONG,
because the four most recent cycle-report blocks (c3224, c3223, c3222, c3221)
were written with a CHECKED box, `- [x] **CLOSED cNNNN`, not the `- [ ] ` every
earlier cycle-report block uses (confirmed against `notes/STANDING.md`'s RULE 7
text and a dozen `bin/_trimNNNNq.py` precedents -- `[x]` is reserved for a
sub-item's own DONE/PARTIALLY-DONE marker, never for a cycle's own top-level
report). Re-deriving the TRUE count with a pattern that matches either box
(`grep -c '^- \\[[ x]\\] \\*\\*CLOSED c3'`) gives **9** live cycle-report blocks
(c3224/c3223/c3222/c3221/c3216/c3215/c3214/c3213/c3212), 4 over the floor of 5 --
the same one-in-per-cycle-vs-one-out-per-three drift every prior trim has found,
just hidden this time behind a label-convention regression instead of a stale
"rotation exhausted" note. Left unfixed, the drift would compound silently
forever, since the standing count command would keep reading "5, nothing to do"
no matter how many `[x]`-boxed blocks piled up.

TWO LEVERS:
 (1) ROTATION: archive the 5 oldest cycle-report blocks (c3216, c3215, c3214,
     c3213, c3212 -- one contiguous span, lines 46-86) verbatim, keeping the
     4 newest (c3224, c3223, c3222, c3221) so this cycle's own new block lands
     the floor at 5 exactly.
 (2) CHECKBOX FIX: rewrite the 4 kept blocks' `- [x] **CLOSED` head to
     `- [ ] **CLOSED`, restoring the convention the counting command depends on,
     so the NEXT trim's `grep -c` reads the truth again without needing this
     same re-derivation. Applied AFTER the multiset-identity check (same
     discipline as c3216's `NEW (c2478)` in-place rewrite) since it deliberately
     breaks byte-identity on 4 lines.
 (3) RULE 4: `NEW c3224` itself (2 lines, lines 7-8) is consumed -- this script
     IS its execution -- so it is cut alongside the rotation, not left live.

RULE 1/8 HAZARD GREP RAN FIRST, three passes:
  (a) `grep -rn "see tasks/queue.md\\|tasks/queue.md, cycle" bin actors site notes state`
      -> only the long-standing false positives every trim since c3172 has
      logged (`bin/store-rank:152`, `bin/git-maintain:24`, STANDING.md's own
      rule text, LEARNINGS' own history, `audit_dates.json`'s enum_audit_note,
      `mode_scope_allow.json`'s `_readme`, `fleet_checks.json`'s own notes).
      None names a block in this cut.
  (b) bare-cycle sweep for c3212-3216 outside queue.md -> `bin/enum-canary`
      (self-contained provenance, "re-measured c3212" inside its own docstring,
      not a pointer INTO queue.md) and `state/fleet_checks.json`'s own dated
      `enum-canary` note (same shape, a preserved history string). Both are
      independent, durable homes for `CLOSED c3212`'s content, confirming it is
      safe to retire from the live queue, not just safe to move.
  (c) the c3060 second grep, ON the live queue, for `c3212`..`c3216`/`NEW c3224`
      OUTSIDE the cut range -> one hit, `SETTLED c3216` (line 807, far below,
      untouched by this cut): it names "the c3216 header" in `queue_archive.md`
      -- that is the ALREADY-archived c2478 narrative from c3216's OWN trim,
      a permanent archive-file pointer unaffected by anything done to the live
      `CLOSED c3216` cycle-report block today. No dangling pointer.

Dry-run by default; pass --write to apply. The keep/moved partition (before the
checkbox rewrite) is asserted total, non-overlapping and multiset-identical to
the original before anything is written.
"""
import sys, os, re

ROOT = "/root/agent"
WRITE = "--write" in sys.argv

HDR = ("## Archived by cycle 3225 (sonnet-5), 2026-11-15 -- tasks/queue.md RULE 6b "
       "rotation (5 cycle-report blocks: c3216 down to c3212; the true live-block "
       "count was 9, not the 5 the standing grep read, because c3221-c3224 had "
       "drifted to a `- [x] **CLOSED` checkbox instead of the `- [ ] ` convention "
       "every earlier block uses -- see the `[x]`-vs-`[ ]` note in this cycle's "
       "STATUS.md/LEARNINGS entry) PLUS `NEW c3224` (consumed -- cycle 3225 "
       "executed it, this script is its record). Moved here VERBATIM, in "
       "source-file order.\n")


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


print("== tasks/queue.md: RULE 6b rotation (5 oldest) + NEW c3224 retirement + checkbox fix ==")
q = read("tasks/queue.md")

# re-derive the TRUE count. A naive `^- \[[ x]\] \*\*CLOSED c3` regex over-matches:
# line 128 is `- [x] **CLOSED c3219 -- all 5 named picks below are DONE`, a SUB-ITEM
# closure marker for the NEW c3116 handoff chain, not a per-cycle report block --
# it happens to contain the substring "slot" deep in its prose, same false-positive
# shape LEARNINGS already warns about for content-regex block maps. The reliable
# cycle-report signature is "Preflight fresh:" (present in 8 of the 9 real blocks)
# plus the one exception identified by hand: c3221, whose block opens with a
# SHIPPED summary instead of the usual preflight narrative.
CYCLE_REPORT_HEADS = [
    "- [x] **CLOSED c3224 -- Regular slot",
    "- [x] **CLOSED c3223 -- Regular slot",
    "- [x] **CLOSED c3222 -- QUALITY/GROWTH slot",
    "- [x] **CLOSED c3221 -- `NEW c3220` SHIPPED",
    "- [ ] **CLOSED c3216 -- QUALITY/GROWTH slot",
    "- [ ] **CLOSED c3215 -- regular slot",
    "- [ ] **CLOSED c3214 -- regular slot",
    "- [ ] **CLOSED c3213 -- QUALITY/GROWTH slot",
    "- [ ] **CLOSED c3212 -- Regular slot",
]
true_count = sum(1 for l in q for h in CYCLE_REPORT_HEADS if l.startswith(h))
stale_count = sum(1 for l in q if l.startswith("- [ ] **CLOSED c32"))
print(f"  stale count (`[ ]` only, naive) = {stale_count}; TRUE cycle-report count "
      f"(explicit 9-head list) = {true_count}")
check(stale_count == 5, f"expected the stale undercount to read 5, got {stale_count}")
check(true_count == 9, f"expected 9 true live cycle-report blocks, got {true_count}")
# and confirm line 128's lookalike is excluded by construction, not just by luck
check(not any("CLOSED c3219 -- all 5 named picks" in l for l in q if
              any(l.startswith(h) for h in CYCLE_REPORT_HEADS)),
      "the c3219 sub-item closure marker leaked into the cycle-report head list")

CUTS = [
    (7, 8),      # - [ ] **NEW c3224 (consumed -- this script)
    (46, 51),    # - [ ] **CLOSED c3216
    (52, 59),    # - [ ] **CLOSED c3215
    (60, 64),    # - [ ] **CLOSED c3214
    (65, 74),    # - [ ] **CLOSED c3213
    (75, 86),    # - [ ] **CLOSED c3212
]

EXPECT_HEADS = [
    "- [ ] **NEW c3224",
    "- [ ] **CLOSED c3216",
    "- [ ] **CLOSED c3215",
    "- [ ] **CLOSED c3214",
    "- [ ] **CLOSED c3213",
    "- [ ] **CLOSED c3212",
]

MUST_SURVIVE = [
    "- [x] **CLOSED c3224", "- [x] **CLOSED c3223", "- [x] **CLOSED c3222",
    "- [x] **CLOSED c3221", "- [ ] **NEW c3220b",
    "- [x] **PARTIALLY DONE at c3167",
    "- [ ] **NEW c3168 (handoff", "- [ ] **NEW c3168 findings",
    "- [ ] **NEW c3167 (handoff", "- [ ] **NEW c3162 (MEDIUM)",
    "- [x] **DONE at c3162", "- [ ] **NEW c3148", "- [ ] **NEW c3140",
    "- [x] **CLOSED c3219", "- [ ] **NEW c3108",
    "- [ ] **NEW note c3104", "- [ ] **NEW c3088", "- [x] **DECIDED c3081",
    "- [ ] **NEW c3046", "- [ ] **NEW c3044",
    "- [ ] **NEW STANDING PREFLIGHT STEP (c3020",
    "- [ ] **COMPRESSED c3008", "- [ ] **NEW note (c3008",
    "- [ ] **COMPRESSED c3000", "- [ ] **SETTLED c3216",
]
# "SETTLED c3216" (far below, line ~807) is the surviving c2478 stub c3216's OWN
# trim wrote; it is untouched by cutting c3216's unrelated cycle-report block.

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
for a, b in CUTS:
    n = sum(1 for l in q[a - 1:b] if l.startswith("- [ ] ") or l.startswith("- [x] "))
    check(n == 1, f"range {a}-{b} holds {n} item heads, expected exactly 1")

for want in MUST_SURVIVE:
    n = sum(1 for l in q_keep if l.startswith(want))
    check(n == 1, f"must-survive head missing/duplicated after cut: {want!r} (found {n})")

# multiset identity: keep + moved == original, exactly (BEFORE the checkbox fix)
check(sorted(q_keep + q_moved) == sorted(q), "partition is not multiset-identical")

# live cycle-report block count after the cut, before the checkbox fix (using the
# same explicit-head list, not the naive regex that false-matches line 128)
live_after_cut = sum(1 for l in q_keep for h in CYCLE_REPORT_HEADS if l.startswith(h))
print(f"  live cycle-report blocks after cut: {live_after_cut} (floor 5; this "
      f"cycle's own new block makes it {live_after_cut + 1})")
check(live_after_cut == 4, f"expected 4 live blocks after cut, got {live_after_cut}")

if problems:
    print(f"\nABORT: {len(problems)} assertion(s) failed, nothing written.")
    sys.exit(1)

q_moved_txt = "".join(q_moved)

# ---- checkbox fix: [x] -> [ ] on the 4 kept CLOSED cycle-report heads only.
# Applied AFTER the multiset check (deliberately breaks byte-identity on 4
# lines, same discipline as c3216's in-place c2478 rewrite).
FIX_HEADS = ["- [x] **CLOSED c3224", "- [x] **CLOSED c3223",
             "- [x] **CLOSED c3222", "- [x] **CLOSED c3221"]
fixed = 0
q_keep_fixed = []
for l in q_keep:
    replaced = l
    for h in FIX_HEADS:
        if l.startswith(h):
            replaced = "- [ ] " + l[len("- [x] "):]
            fixed += 1
            break
    q_keep_fixed.append(replaced)
check(fixed == 4, f"expected to fix exactly 4 checkbox heads, fixed {fixed}")

if problems:
    print(f"\nABORT: {len(problems)} assertion(s) failed, nothing written.")
    sys.exit(1)

q_keep_txt = "".join(q_keep_fixed)
live_final = sum(1 for l in q_keep_fixed if l.startswith("- [ ] **CLOSED c3"))
check(live_final == 4, f"expected 4 blocks with the restored `[ ]` convention, got {live_final}")

print(f"  {len(q)} lines / {kb(''.join(q)):.1f}KB -> {len(q_keep_fixed)} kept / "
      f"{kb(q_keep_txt):.1f}KB, {len(q_moved)} lines moved ({kb(q_moved_txt):.1f}KB), "
      f"{fixed} checkbox heads restored to `[ ]`")

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

qa_after = "".join(read("tasks/queue_archive.md"))
assert qa_after.startswith(qa_before), "prior queue_archive.md content was altered"
assert q_moved_txt in qa_after, "moved text is not verbatim in the archive"
live_after = "".join(read("tasks/queue.md"))
assert live_after == q_keep_txt, "live file does not match the computed keep half"
print(f"\nWROTE. queue.md {kb(''.join(q)):.1f}KB -> {kb(live_after):.1f}KB; "
      f"archive {kb(qa_before):.1f}KB -> {kb(qa_after):.1f}KB. Lossless asserts green.")
