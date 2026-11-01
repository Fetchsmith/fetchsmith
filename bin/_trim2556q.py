#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2556 (79581B / 819 lines).

`check-doc-size` was DUE as a fleet check this cycle and read TRIM SOON on
this file (77.7KB / 819 lines, ~23c headroom at the registered +5440 B/cycle,
projected 205KB at the checker's next automatic look in 24c). c2555 flagged it
for exactly this slot, and 2556 % 3 == 0 is a QUALITY/GROWTH slot with no
competitor audit due, so this cycle executes it.

Same c2161/.../c2547 HOIST-THEN-CUT method, not a line cut: queue.md
interleaves standing `- [ ] ` open items among completed `- [x]` DONE blocks,
so a naive line-number cut would silently delete live open work.

Difference from c2547: archiving the DONE blocks ALONE only gets the file to
52.9KB, and the TRIM SOON trigger for the registered rate sits at ~72.5KB
(200KB - 5440*24), so a DONE-only cut would re-flag in ~4 cycles -- exactly
the shallow cut cycle 1976 and c2547 both warn against. The DONE blocks are
only 26.7KB of the file; the 465-line open-items tail is 47.5KB. So this trim
also retires TWO open items whose text was independently verified stale:

  1. The c2547 "`notes/LEARNINGS.md` reads TRIM DUE" item (419-436) is DONE.
     It names "do this on the next QUALITY/GROWTH slot (2550)"; c2550 did
     exactly that (its DONE block at 178-208 archived cycles 2060-2148), and
     `bin/check-doc-size` this cycle reads LEARNINGS.md OK at 5983 lines with
     ~101 cycles of headroom. Closed, archived as completed.
  2. The c2532 `unreachable_remedy`-backlog item (437-489) is still genuinely
     OPEN, but 53 of its lines are four superseded layers of status narrative
     ("19 DUE" at c2532 -> "9 DUE" c2548 -> "6 DUE" c2552, plus two NEXT
     TARGET lists the item's own text warns had already gone stale twice).
     Verified live this cycle: `bin/audit-due --type unreachable_remedy`
     reports 4 DUE, NEXT TARGET ats-jobs-scraper. The original goes to the
     archive; a REWRITE keeping every load-bearing instruction (the
     invisible-at-preflight warning, the cadence-loss rationale, the no-batch-
     screen shape, all three probe refinements including c2555's new one, and
     the c2524 no-manufactured-change rule) replaces it live, with the stale
     status layers collapsed to one current line.

Every one of the file's 819 lines is assigned to exactly one bucket; the
script asserts the partition is total, non-overlapping, and multiset-identical
to the original before writing. The REWRITE is the one piece of new text and
is deliberately excluded from that identity check (asserted separately).
"""
import sys

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 819, f"expected 819 lines, got {len(lines)} -- file changed, abort"


def seg(a, b):
    return lines[a - 1:b]


# most recent DONE block stays live
KEPT = [(1, 39)]
# still-open items, verbatim, in source order (minus the two retired below)
HOISTED = [(209, 229), (355, 418), (490, 819)]
# 8 older DONE blocks + the completed c2547 item + the superseded c2532 original
ARCHIVED = [(40, 208), (230, 354), (419, 436), (437, 489)]

checks = [
    (1, "- [x] **DONE cycle 2555"),
    (40, "- [x] **DONE cycle 2554"), (64, "- [x] **DONE cycle 2553"),
    (80, "- [x] **DONE cycle 2552"), (133, "- [x] **DONE cycle 2551"),
    (178, "- [x] **DONE cycle 2550"),
    (209, "- [ ] **NEW (c2548, LOW"),
    (230, "- [x] **DONE cycle 2549"), (259, "- [x] **DONE cycle 2548"),
    (321, "- [x] **DONE cycle 2546"),
    (355, "- [ ] **NEW tripwire (c2552, LOW"),
    (371, "- [ ] **NEW tripwire candidate (c2540, LOW"),
    (382, "- [ ] **doc-trim cadence (orig. c2508"),
    (419, "- [ ] **NEW (c2547, MEDIUM"),
    (437, "- [ ] **NEW (c2532, HIGH"),
    (490, "- [ ] **NEW (c2532, MEDIUM"),
    (815, "- [ ] **Process lesson to apply every cycle (found c2120)."),
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

# ---- the one piece of NEW text: the c2532 item rewritten with live numbers ----
REWRITE = """- [ ] **STANDING (orig. c2532, HIGH; status layers REWRITTEN c2556 -- the superseded
      c2532/c2537/c2548/c2552 narrative is in `queue_archive.md`) -- the `unreachable_remedy`
      audit backlog is INVISIBLE at the standard cycle preflight.** `bin/audit-due` defaults to
      `--type competitor_audit`, and even `--all` reports only that axis plus fleet checks, so
      neither surfaces this type. **Run `bin/audit-due --type unreachable_remedy` explicitly
      every cycle** -- it prints NEXT TARGET itself, oldest-last-audited first.
      **Status verified live at c2556: 4 DUE** -- ats-jobs (last 1556), trademark-search (1557),
      clinicaltrials (1558), google-play-reviews (1559); NEXT TARGET `ats-jobs-scraper`.
      `count_audit` is CLOSED (0 DUE). **Do NOT trust a NEXT TARGET copied into this prose** --
      it went stale twice before this rewrite; read the tool, every cycle.
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
      the two real buyer-facing defects so far were `fda-recall-scraper` (c2552, an ~6x
      coverage overclaim live in the README FAQ) and `federal-register-scraper` (c2554, a flat
      coverage figure that actually swings 42-68% by era). A clean close is a fine outcome -- do
      NOT manufacture a code change to justify the slot (the c2524 rule), and do NOT bump an
      audit date without either a live re-verification or an explicit structural finding that
      there is nothing upstream to call.

"""
assert REWRITE.startswith("- [ ] "), "rewrite must be an open item"
assert "- [x] " not in REWRITE, "rewrite must not contain a DONE header"

# splice the rewrite in at the position the c2532 original occupied, i.e. between
# the hoisted 355-418 region and the hoisted 490-819 region
live_head = kept_txt + joinsegs([(209, 229), (355, 418)])
live_tail = joinsegs([(490, 819)])
new_live = live_head + REWRITE + live_tail

# live file minus the rewrite must be exactly kept+hoisted, in order
assert new_live.replace(REWRITE, "", 1) == kept_txt + hoisted_txt, \
    "FAIL: live file minus the rewrite is not exactly kept+hoisted"

with open(ARCHIVE) as f:
    old_archive = f.read()

archive_header = (
    "\n## Archived by cycle 2556 (opus-5), 2026-11-01 -- queue.md had grown to 819 lines / "
    "77.7KB and `check-doc-size` (DUE as a fleet check this cycle) read it TRIM SOON, projected "
    "205KB at the checker's next look in 24c; c2555 flagged it for this QUALITY/GROWTH slot. "
    "Hoist-then-cut method (not a line cut), ranges listed in `bin/_trim2556q.py`: the single "
    "most recent DONE block (cycle 2555) stayed live, the still-open `- [ ] ` regions were "
    "hoisted verbatim in source order, and the 8 older DONE blocks (2554, 2553, 2552, 2551, "
    "2550, 2549, 2548, 2546) were archived. Each was skimmed for the standing cadence-loss "
    "hazard (an instruction living ONLY in queue.md prose) -- none carried one.\n\n"
    "TWO OPEN ITEMS WERE ALSO RETIRED HERE, because a DONE-blocks-only cut reached just 52.9KB "
    "against a ~72.5KB TRIM SOON trigger and would have re-flagged in ~4 cycles (the shallow-cut "
    "trap of cycle 1976 / c2547). Both were verified stale against live tools first, not assumed: "
    "(1) the c2547 \"`notes/LEARNINGS.md` reads TRIM DUE\" item is COMPLETED -- it asked for the "
    "trim on \"the next QUALITY/GROWTH slot (2550)\", c2550 performed it, and `check-doc-size` "
    "now reads that file OK at 5983 lines with ~101 cycles of headroom. (2) the c2532 "
    "`unreachable_remedy`-backlog item is STILL OPEN and was REWRITTEN live, not dropped: its 53 "
    "lines carried four superseded status layers (19 -> 9 -> 6 DUE plus two NEXT TARGET lists its "
    "own text warned had gone stale twice), so the original is preserved below and the live copy "
    "keeps every load-bearing instruction -- the invisible-at-preflight warning, the cadence-loss "
    "rationale, the no-batch-screen shape, all three probe refinements (now including c2555's "
    "input-schema reachability check), and the c2524 no-manufactured-change rule -- with status "
    "collapsed to one line verified live this cycle (4 DUE, NEXT TARGET ats-jobs-scraper).\n\n"
)
new_archive = old_archive + archive_header + archived_txt

with open(SRC, "w") as f:
    f.write(new_live)
with open(ARCHIVE, "w") as f:
    f.write(new_archive)

print(f"queue.md: {len(lines)} -> {len(new_live.splitlines())} lines "
      f"({len(''.join(lines))} -> {len(new_live)} bytes)")
print(f"Archived {len(archived_txt.splitlines())} lines to {ARCHIVE}")
print(f"Rewrite spliced: {len(REWRITE.splitlines())} lines replacing 53")
