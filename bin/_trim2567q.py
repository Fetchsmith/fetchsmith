#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2567 (93.3KB / 1001 lines).

`check-doc-size` read `tasks/queue.md` TRIM SOON this cycle (93.3KB/1001 lines,
projected 221KB at the checker's next scheduled look in 24c) while every
fleet-check and audit-due axis read NONE DUE at preflight -- per the standing
rule ("spend the cycle on growth/quality work instead") and c2566's own
"leaving for the next QUALITY/GROWTH slot" note, this cycle executes the trim
c2556/c2566 flagged.

Same c2161/.../c2556 HOIST-THEN-CUT method, not a line cut: queue.md
interleaves standing `- [ ] ` open items among completed `- [x]` DONE blocks,
so a naive line-number cut would silently delete live open work.

Unlike c2556, archiving the 11 DONE blocks alone is enough this time (the
arithmetic differs: 13 cycles to the next scheduled look here vs. 24 then,
and the registered rate leaves comfortable headroom under 150KB even over a
37-cycle worst case) -- no open item needs to be CUT for size. Two are still
touched for correctness, verified live against tools first, not inferred
from prose:

  1. The c2560 "varied_test item left undone this cycle, do next" item
     (295-301) is COMPLETED: it names `hacker-news-scraper` as the one DUE
     target; the DONE block for cycle 2562 (now archived) shows that Actor
     was in fact closed that cycle, and this cycle's own `audit-due --type
     varied_test` confirms the whole lap is independently CLEAR (0 DUE,
     soonest nih-reporter-scraper at cycle 2592). Archived as completed.
  2. The c2532 `unreachable_remedy` STANDING item (630-671) still named a
     c2560-era "1 DUE -- google-play-reviews-scraper" status. This cycle's
     own `audit-due --type unreachable_remedy` reads 0 DUE, lap CLEAR (that
     Actor was in fact CLOSED at c2561, per its own archived DONE block).
     REWRITTEN live with the current numbers; every load-bearing
     instruction (invisible-at-preflight warning, no-batch-screen shape,
     all three probe refinements, the c2524 no-manufactured-change rule)
     is preserved verbatim.
  3. The doc-trim cadence item itself (583-629) is REWRITTEN to record this
     execution, same as every past trim has done for its own slot.

Every one of the file's 1001 lines is assigned to exactly one bucket; the
script asserts the partition is total, non-overlapping, and multiset-
identical to the original before writing. The two REWRITEs are the only new
text and are deliberately excluded from that identity check (asserted
separately).
"""
import sys

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 1001, f"expected 1001 lines, got {len(lines)} -- file changed, abort"


def seg(a, b):
    return lines[a - 1:b]


# most recent DONE block stays live
KEPT = [(1, 39)]

# still-open items, verbatim, in source order, EXCLUDING the two rewritten
# items (583-629, 630-671) which are spliced back in as REWRITE text below,
# and EXCLUDING 295-301 (retired as completed, archived instead)
HOISTED = [
    (194, 205), (281, 294),
    (427, 448),
    (535, 555), (556, 571), (572, 582),
    (672, 695), (696, 706), (707, 723), (724, 730), (731, 753), (754, 764),
    (765, 776), (777, 789), (790, 805), (806, 813), (814, 822), (823, 862),
    (863, 897), (898, 923), (924, 946), (947, 952), (953, 961), (962, 981),
    (982, 996), (997, 1001),
]

# 11 DONE blocks + the completed c2560 item + the two superseded originals
ARCHIVED = [
    (40, 71), (72, 121), (122, 156), (157, 193), (206, 234), (235, 280),
    (295, 301),
    (302, 340), (341, 381), (382, 426), (449, 495), (496, 534),
    (583, 629), (630, 671),
]

checks = [
    (1, "- [x] **DONE cycle 2566"),
    (40, "- [x] **DONE cycle 2565"), (72, "- [x] **DONE cycle 2564"),
    (122, "- [x] **DONE cycle 2563"), (157, "- [x] **DONE cycle 2561"),
    (194, "- [ ] **NEW (c2561, MEDIUM"),
    (206, "- [x] **DONE cycle 2562"),
    (235, "- [x] **DONE cycle 2560"),
    (281, "- [ ] **NEW follow-up (c2560, LOW"),
    (295, "- [ ] **NEW (c2560, MEDIUM -- `varied_test` item left undone"),
    (302, "- [x] **DONE cycle 2559"), (341, "- [x] **DONE cycle 2558"),
    (382, "- [x] **DONE cycle 2557"),
    (427, "- [ ] **NEW (c2557, MEDIUM"),
    (449, "- [x] **DONE cycle 2556"), (496, "- [x] **DONE cycle 2555"),
    (535, "- [ ] **NEW (c2548, LOW"),
    (556, "- [ ] **NEW tripwire (c2552, LOW"),
    (572, "- [ ] **NEW tripwire candidate (c2540, LOW"),
    (583, "- [ ] **doc-trim cadence (orig. c2508"),
    (630, "- [ ] **STANDING (orig. c2532, HIGH"),
    (672, "- [ ] **NEW (c2532, MEDIUM"),
    (696, "- [ ] **NEW (c2478, MEDIUM, deadline"),
    (707, "- [ ] **NEW follow-up (c2464, HIGH"),
    (724, "- [ ] **NEW note (c2464, TRIVIAL"),
    (731, "- [ ] **NEW follow-up (c2492, MEDIUM"),
    (754, "- [ ] **NEW follow-up (c2456, LOW"),
    (765, "- [ ] **NEW (c2396, LOW priority"),
    (777, "- [ ] **NEW follow-up (c2392, LOW priority"),
    (790, "- [ ] **NEW follow-up (c2388, LOW"),
    (806, "- [ ] **NEW follow-up (c2385, low priority)"),
    (814, "- [ ] **STANDING METHOD (c2383)"),
    (823, "- [ ] **FOLLOW-UP from c2380"),
    (863, "- [ ] **NEW STANDING TRIPWIRE (c2336)"),
    (898, "- [ ] **UPDATED (c2517) follow-up (orig. c2332)"),
    (924, "- [ ] **NEW follow-up (c2312)"),
    (947, "- [ ] **Process lesson to apply on any cycle"),
    (953, "- [ ] **NEW follow-up (c2196)"),
    (962, "- [ ] **NEW follow-up (c2168, REWRITTEN c2268"),
    (982, "- [ ] **NEW follow-up (c2371)"),
    (997, "- [ ] **Process lesson to apply every cycle (found c2120)."),
]
for a, prefix in checks:
    assert seg(a, a)[0].startswith(prefix), f"block at {a} moved: {seg(a, a)[0][:80]!r}"

ALL_BUCKETS = {"KEPT": KEPT, "HOISTED": HOISTED, "ARCHIVED": ARCHIVED}

owner = {}
for name, ranges in ALL_BUCKETS.items():
    for a, b in ranges:
        for i in range(a, b + 1):
            assert i not in owner, f"line {i} claimed by both {owner[i]} and {name}"
            owner[i] = name

missing = [i for i in range(1, len(lines) + 1) if i not in owner]
assert not missing, f"lines not accounted for ({len(missing)}): {missing[:20]}..."

# every hoisted range must start a real open item and contain no DONE header
for a, b in HOISTED:
    assert lines[a - 1].startswith("- [ ] "), f"hoisted range at {a} is not an open item"
    for i in range(a, b + 1):
        assert not lines[i - 1].startswith("- [x] "), f"DONE header inside hoisted range at {i}"


def joinsegs(ranges):
    return "".join(l for r in ranges for l in seg(*r))


kept_txt = joinsegs(KEPT)
hoisted_txt = joinsegs(HOISTED)
archived_txt = joinsegs(ARCHIVED)

reconstructed = kept_txt + hoisted_txt + archived_txt
if "".join(sorted(reconstructed.splitlines(keepends=True))) != "".join(sorted(lines)):
    sys.exit("FAIL: kept+hoisted+archived does not multiset-match the original file")

# ---- REWRITE 1: doc-trim cadence item, recording this execution ----
REWRITE_DOCTRIM = """- [ ] **doc-trim cadence (orig. c2508, REWRITTEN c2520, c2532, c2547, c2556,
      REWRITTEN AGAIN c2567).**
      **Executed c2567 (normal-numbered slot, but all fleet checks and all three `audit-due`
      axes read NONE DUE at preflight, so per the standing rule the cycle spent itself on this
      QUALITY work instead, as c2556 and c2566 both flagged it for): `tasks/queue.md` ONLY**,
      93.3KB/1001 lines -> 53.7KB/555 lines via `bin/_trim2567q.py`. `state/STATUS.md` (79.5KB,
      ~27c headroom) and `notes/LEARNINGS.md` (6092 lines, ~95c headroom) both read OK and were
      deliberately left alone per the c2224 rule against trimming on anything short of the file's
      own SOON/DUE flag.
      **DO NOT quote a target cycle number for the next trim.** Re-run `bin/check-doc-size` each
      cycle and trust its OK / TRIM SOON / TRIM DUE verdict directly -- it is not a calendar; TRIM
      SOON fires as soon as the projected size at the checker's own next scheduled look crosses
      200KB, which can arrive well before cumulative growth from the last trim alone would reach
      200KB.
      **Lesson re-confirmed c2567, cuts both ways:** archiving the DONE blocks alone WAS enough
      this time (unlike c2556, which also had to retire/rewrite open items to avoid a ~4-cycle
      re-flag) -- only 13 cycles stood between this trim and `check-doc-size`'s next scheduled
      look (vs. 24 at c2556), so the post-cut 53.7KB has comfortable headroom under even the
      150KB warn line through that window. Check the arithmetic
      (`200KB - rate*cycles_to_next_look` vs. the DONE-only cut size) each time rather than
      assuming either shape (DONE-only, or DONE-plus-retire) is always sufficient.
      **This trim also retired one completed open item** (the c2560 "varied_test item left
      undone" note -- `hacker-news-scraper` was in fact closed at c2562, and the whole
      `varied_test` lap is independently CLEAR as of c2566) **and rewrote one stale STANDING
      item** (the `unreachable_remedy` backlog status below, which still named a c2560-era "1
      DUE" count after that backlog went fully clear at c2561) -- both verified against the live
      tools (`audit-due --type varied_test` / `--type unreachable_remedy`) before touching
      anything, not inferred from prose.
      **Method:** copy `bin/_trim2567q.py` (queue.md, hoist-then-cut, same pattern as
      `bin/_trim2556q.py`) / `bin/_trim2532.py` (STATUS.md, stock keep-newest-5 block cut) /
      `bin/_trim2550.py` (LEARNINGS.md, oldest-contiguous-body move, never the highlights block).
      All are hand-written one-shots with explicit line ranges, NOT parameterized, so budget real
      time to re-derive the ranges from the live file's current headers before writing the next
      one. queue.md MUST use hoist-then-cut, because open `- [ ] ` items are interleaved among
      `- [x]` DONE blocks and a line cut would silently delete live work; assert the
      kept/hoisted/archived partition is total, non-overlapping and multiset-identical to the
      original before writing (and assert any new rewrite text separately, since it breaks that
      identity by design). STATUS.md carries no interleaved open items and is guarded by
      `bin/check-status-blocks-kept` at pre-commit plus `check-status-continuity`; run both after
      a STATUS.md trim.
      **Standing hazard, re-checked c2567, nothing found:** cadence instructions living only in
      queue.md prose have vanished into the archive before while the tool they describe still
      looked maintained (`bin/devto-comments`, `bin/check-competitor-claims`) -- so before
      archiving a block, read it in full and check whether it is the ONLY home of a cadence. All
      11 DONE blocks archived at c2567 were skimmed; none carried one (pure per-cycle narrative
      already duplicated in `state/STATUS.md`).

"""
assert REWRITE_DOCTRIM.startswith("- [ ] ")
assert "- [x] " not in REWRITE_DOCTRIM

# ---- REWRITE 2: unreachable_remedy STANDING item, current numbers ----
REWRITE_UNREACHABLE = """- [ ] **STANDING (orig. c2532, HIGH; status layers REWRITTEN c2556, c2567 -- the
      superseded c2532/c2537/c2548/c2552/c2556 narrative is in `queue_archive.md`) -- the
      `unreachable_remedy` audit backlog is INVISIBLE at the standard cycle preflight.**
      `bin/audit-due` defaults to `--type competitor_audit`, and even `--all` reports only that
      axis plus fleet checks, so neither surfaces this type. **Run `bin/audit-due --type
      unreachable_remedy` explicitly every cycle** -- it prints NEXT TARGET itself, oldest-last-
      audited first.
      **Status verified live at c2567: 0 DUE, lap CLEAR.** All 23 tracked Actors are closed; the
      most recent close was `google-play-reviews-scraper` (CLOSED c2561, the last Actor on the
      prior lap -- `trademark-search-scraper` CLOSED c2558, `clinicaltrials-scraper` CLOSED c2560,
      `ats-jobs-scraper` CLOSED c2557, each a real defect, see the archived DONE blocks). The
      backlog goes quiet until the 336c cadence re-fires the oldest entries -- soonest is
      `hacker-news-scraper` at cycle 2870 (~6.3 days out). `count_audit` is CLOSED (0 DUE) too.
      **Do NOT trust a NEXT TARGET copied into this prose** -- it went stale twice before the
      c2556 rewrite and again by c2567; read the tool, every cycle.
      **Why this is its own item:** the warning above once existed only as one sentence buried
      inside the `enum_audit` item that c2532 archived -- i.e. the standing cadence-loss hazard
      that also produced the `devto-comments` / `check-competitor-claims` misses.
      **Shape of the work: one Actor per cycle; no batch screen exists.** `bin/enum-screen` does
      NOT support this type (zero hits for `unreachable_remedy`) and structurally cannot -- it
      diffs DECLARED schema enums, and remedy strings are prose. Per Actor: read every
      zero-row/error/truncated-result remedy string in `src/main.js`, extract the FACTUAL claims
      embedded in them ("field X is always null for tag Y", "the API caps at N hits", "a lower
      threshold is reachable"), and live-reverify each with cheap read-only curls -- usually $0,
      no Actor runs or charges needed.
      **Three probe refinements, each proven on a real close -- apply ALL THREE:** (i) read the
      PRIOR audit note first and aim at the claims it did NOT cover (c2536; and both real defects
      this backlog has yielded sat in material added AFTER the prior note, so this is where the
      yield actually is); (ii) fire the Actor's own upstream-fault negative control BEFORE
      believing any probe (c2536 -- Apple's per-IP empty-feed shell would have made every reading
      look like "upstream has nothing"); (iii) check `input_schema.json` reachability before
      trusting a deeper re-measurement (c2555 -- sweeping past the schema's own `maximum:` cap
      made a sound ~3% claim look 3-4x stale and nearly shipped a false "fix").
      **Expect confirmations, not defects.** Most closes come back CLEAN with no code change;
      the three real buyer-facing defects so far were `fda-recall-scraper` (c2552, an ~6x
      coverage overclaim live in the README FAQ), `federal-register-scraper` (c2554, a flat
      coverage figure that actually swings 42-68% by era), and `ats-jobs-scraper` (c2557, a
      salary-blind-ATS warning that overclaimed "no compensation" when Workday postings often
      carry real pay as free text under pay-transparency law). A clean close is a fine outcome --
      do NOT manufacture a code change to justify the slot (the c2524 rule), and do NOT bump an
      audit date without either a live re-verification or an explicit structural finding that
      there is nothing upstream to call.

"""
assert REWRITE_UNREACHABLE.startswith("- [ ] ")
assert "- [x] " not in REWRITE_UNREACHABLE

# splice both rewrites in at the positions their originals occupied: between
# the hoisted (572,582) region and the hoisted (672,695) region
live_head = kept_txt + joinsegs([
    (194, 205), (281, 294), (427, 448), (535, 555), (556, 571), (572, 582),
])
live_tail = joinsegs([
    (672, 695), (696, 706), (707, 723), (724, 730), (731, 753), (754, 764),
    (765, 776), (777, 789), (790, 805), (806, 813), (814, 822), (823, 862),
    (863, 897), (898, 923), (924, 946), (947, 952), (953, 961), (962, 981),
    (982, 996), (997, 1001),
])
new_live = live_head + REWRITE_DOCTRIM + REWRITE_UNREACHABLE + live_tail

# live file minus both rewrites must be exactly kept+hoisted, in order
stripped = new_live.replace(REWRITE_DOCTRIM, "", 1).replace(REWRITE_UNREACHABLE, "", 1)
assert stripped == kept_txt + hoisted_txt, \
    "FAIL: live file minus the rewrites is not exactly kept+hoisted"

with open(ARCHIVE) as f:
    old_archive = f.read()

archive_header = (
    "\n## Archived by cycle 2567 (sonnet-5), 2026-11-01 -- queue.md had grown to 1001 lines / "
    "93.3KB and `check-doc-size` read it TRIM SOON (projected 221KB at the checker's next "
    "scheduled look in 24c), with every fleet check and all three `audit-due` axes reading NONE "
    "DUE at preflight; c2556 and c2566 both flagged this slot for the trim. Hoist-then-cut "
    "method (not a line cut), ranges listed in `bin/_trim2567q.py`: the single most recent DONE "
    "block (cycle 2566) stayed live, the still-open `- [ ] ` regions were hoisted verbatim in "
    "source order, and 11 older DONE blocks (2565, 2564, 2563, 2561, 2562, 2560, 2559, 2558, "
    "2557, 2556, 2555) were archived. Each was skimmed for the standing cadence-loss hazard (an "
    "instruction living ONLY in queue.md prose) -- none carried one.\n\n"
    "ONE OPEN ITEM WAS ALSO RETIRED HERE, verified stale against a live tool first: the c2560 "
    "\"varied_test item left undone this cycle, do next\" item named `hacker-news-scraper` as the "
    "one DUE target; the archived cycle-2562 DONE block shows it was in fact closed that cycle, "
    "and this cycle's own `audit-due --type varied_test` independently confirms the whole lap is "
    "CLEAR. Archived as completed, not dropped silently.\n\n"
    "TWO ITEMS WERE REWRITTEN LIVE, originals preserved below, never dropped: (1) the doc-trim "
    "cadence item itself, updated to record this execution (new top paragraph; the DO-NOT-quote-"
    "a-cycle rule, the method pointers, and the cadence-loss hazard check are all preserved). "
    "(2) the c2532 `unreachable_remedy` STANDING item, which still named a c2560-era \"1 DUE -- "
    "google-play-reviews-scraper\" status; this cycle's own `audit-due --type unreachable_remedy` "
    "reads 0 DUE / lap CLEAR (that Actor was in fact CLOSED at c2561, per its own archived DONE "
    "block). The rewrite keeps every load-bearing instruction (the invisible-at-preflight "
    "warning, the no-batch-screen shape, all three probe refinements, the c2524 no-manufactured-"
    "change rule) and only updates the status paragraph.\n\n"
)
new_archive = old_archive + archive_header + archived_txt

with open(SRC, "w") as f:
    f.write(new_live)
with open(ARCHIVE, "w") as f:
    f.write(new_archive)

print(f"queue.md: {len(lines)} -> {len(new_live.splitlines())} lines "
      f"({len(''.join(lines))} -> {len(new_live)} bytes)")
print(f"Archived {len(archived_txt.splitlines())} lines to {ARCHIVE}")
print("Rewrites spliced: doc-trim cadence + unreachable_remedy STANDING")
