#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2907 (124.6KB / 1498 lines, TRIM SOON).

bin/check-doc-size read TRIM SOON at this cycle's fresh preflight (124.6KB/1498
lines, ~14c headroom, proj. 252KB at its own next look -- past the 200KB trim
line and close to the 256KB Read cap). `audit-due --all` and `checks-due --all`
both read NONE DUE (fleet rotations/checks), so per the doc-trim cadence item's
own standing rule 2 ("trim proactively in a QUALITY slot"), this QUALITY/GROWTH
slot (2907 % 3 == 0) takes the trim rather than waiting for the escalation.

Method: hoist-then-cut (DONE blocks + open-item compression), same pattern as
bin/_trim2892q.py / bin/_trim2876q.py (named clones). Two things cut this time:

  1. DONE blocks: 6 live (one over the newest-5 floor, c2865 convention).
     Archive the single oldest by cycle number (c2901, 34 lines/3063B) --
     NOTE the file does not list DONE blocks in strict cycle-number order
     (c2905 sits before c2901), so "oldest" was derived by cycle number, not
     position.

  2. Two open items compressed in place (c2550 method: archive verbatim,
     rewrite in place keeping every load-bearing instruction), chosen as the
     two cheapest-to-verify of the six c2880-measured candidates within a
     25-minute budget:
       - STANDING RULE c2796 (28 lines/2403B) -> kept the NEVER rule + its
         three numbered parts live; archived the steam-niche narrative
         example (fully historical, not needed to apply the rule).
       - STANDING c2532 (46 lines/4086B) -> kept the live method (shape of
         work, three probe refinements, expectations) that
         `audit-due --type unreachable_remedy` sends a future cycle back to;
         archived the stale c2567-era status snapshot and the "why this is
         its own item" history (both purely historical, and the status
         snapshot is actively misleading today -- superseded by whatever
         `audit-due --all` reads fresh).
     NOT touched this cycle (left for the next pass, per the doc-trim item's
     own "remaining candidates" convention): `c2380` one-term-diff (4.35KB),
     `ORIGINAL c2845` (2.8KB), `UPDATED c2846` (2.4KB), `c2464` follow-up
     (2.3KB) -- all are live, actively-tracked backlog with per-item state
     (handle lists, "next Actor" pointers) that needs careful fidelity
     checking, not a quick narrative trim; `c2478` stays DO NOT TOUCH before
     2026-11-15 (live deadline).

  3. The doc-trim cadence item's own EXECUTED sub-block (its standing rule:
     "method + standing rules + newest execution only, do NOT prepend a full
     narrative per trim") replaced: EXECUTED c2892 archived verbatim,
     EXECUTED c2907 written in its place.

Rule-1 hazard grep (grep FIRST, then read every hit) ran before writing this
script, over all four archive-bound ranges, for "standing rule|cadence|always
|never do|STANDING" (case-insensitive):
  - DONE c2901 (lines 25-58): "cadence"/"standing" hits are the block
    narrating ITS OWN execution of the doc-trim cadence and the newest-5-DONE
    convention -- both homed at c2865 and in the doc-trim item itself (kept
    live elsewhere in this file), not solely here.
  - STANDING RULE c2796 (764-791): "STANDING RULE" is the item naming itself
    (its content survives via the rewrite below); "always" at line 778 is
    inside numbered part (1) of the rule, kept live verbatim in the rewrite.
  - EXECUTED c2892 sub-block (1070-1098): "STANDING RULES" at line 1086
    explicitly reads "this item's own STANDING RULES, kept live" -- confirms
    that section (lines ~1100-1125, outside this archived range) is the real
    home and stays untouched; the other two hits just name STANDING c2532 /
    STANDING RULE c2796 in a stale byte table, both superseded by this same
    cycle's rewrites.
  - STANDING c2532 (1153-1198): "STANDING" (self-naming, survives via
    rewrite); "cadence" x2 are narrative about the rotation's own 336c cadence
    (re-derivable from audit-due's interval data, not a sole home) and the
    "why this is its own item" history (being archived, pure history); "always"
    is inside an example quote ("field X is always null for tag Y"), not an
    instruction, and is kept live in the rewrite's method section anyway.

Partition is asserted total, non-overlapping and multiset-identical to the
original; the four rewrites are asserted separately because they break that
identity by design.
"""

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
NLINES = 1498

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == NLINES, f"expected {NLINES} lines, got {len(lines)} -- file changed, abort"


def seg(a, b):
    return lines[a - 1:b]


# Fully-historical / superseded content, boundaries re-derived fresh this
# cycle via a `^- \[` block scan with per-block byte sizes (standing rule 3).
ARCHIVED = [
    (25, 58),      # DONE c2901 (oldest live DONE block by cycle number)
    (764, 791),    # STANDING RULE c2796 -- superseded by REWRITE_C2796
    (1070, 1098),  # doc-trim item's own superseded EXECUTED c2892 record
    (1153, 1198),  # STANDING c2532 -- superseded by REWRITE_C2532
]

KEPT = [
    (1, 24),       # DONE c2905 + anything before line 25
    (59, 763),     # open items + DONE c2902/c2903/c2904/c2906 etc.
    (792, 1069),   # open items between c2796 and the doc-trim item's header
    (1099, 1152),  # doc-trim item's STANDING RULES + method + hazard note
    (1199, NLINES),  # c2478 Nov-15 item onward to EOF
]

REWRITE_C2796 = """- [ ] **COMPRESSED c2907 (was STANDING RULE c2796, 28 lines; full narrative
      verbatim in `tasks/queue_archive.md` under the c2907 header). STANDING RULE,
      HIGH for every FUTURE `competitor_audit`.** **NEVER run a
      `bin/_batch_price_*.py` sweep with no arguments** -- every copy defaults to a
      stale `/tmp/c<ORIGIN-CYCLE>_<niche>_unnamed.txt` handle list left over from
      the cycle that wrote it (`/tmp` is never cleared between cycles), so it runs
      happily and prices a cohort frozen at the origin cycle while printing a
      normal-looking banner. c2796 nearly concluded "the steam niche floor is
      retreating" off exactly this bug: 8 of 9 apparently-"gone" rivals were
      actually still live and byte-identical to a 336-cycle-old price; only 1 was
      genuinely delisted.
      **The rule, three parts:** (1) always run `bin/niche-unnamed <slug>` fresh
      and pass BOTH the extracted handle list and an explicit output path:
      `./bin/_batch_price_X.py /tmp/c<THIS>_X_unnamed.txt /tmp/c<THIS>_X_prices.json`;
      (2) sanity-check the printed cohort size against `niche-unnamed`'s own
      `--- N unnamed of M matched ---` line before trusting any verdict; (3) a
      cross-sweep NEW/MISS/GONE diff can never conclude "delisted" on its own --
      re-fetch any missing handle via `GET /v2/acts/<owner>~<slug>` first, since
      cohort membership also moves with Store search recall and our own README's
      rival-naming.
      **Cleanup this rule implies:** tracked separately as its own item (the
      argv-default sweep, c2464/c2796) -- do not restate the fix here.

"""

REWRITE_C2532 = """- [ ] **STANDING (orig. c2532, status layers REWRITTEN c2556/c2567, COMPRESSED
      c2907 -- stale status snapshots and the "why this is its own item" history
      verbatim in `queue_archive.md` under the c2907 header). `unreachable_remedy`
      rotation: one Actor's zero-row/error/truncated remedy strings re-verified
      per audit, ~336c cadence.** Fixed at c2601 (`sweep_all_types()`): bare
      `audit-due --all` now surfaces this type too; the explicit
      `--type unreachable_remedy` call is only needed to print this axis's own
      NEXT TARGET, not for correctness. **Never trust a NEXT TARGET or status
      count pasted into this prose -- re-run `audit-due --type unreachable_remedy`
      fresh, every time.**
      **Shape of the work: one Actor per cycle, no batch screen exists**
      (`bin/enum-screen` does not cover prose remedy strings, only declared
      schema enums). Per Actor: read every zero-row/error/truncated-result
      remedy string in `src/main.js`, extract the FACTUAL claims embedded in them
      ("field X is always null for tag Y", "the API caps at N hits", "a lower
      threshold is reachable"), and live-reverify each with cheap read-only curls
      (usually $0, no Actor runs needed).
      **Three probe refinements, apply ALL THREE (each proven on a real close):**
      (i) read the prior audit note and aim at claims it did NOT cover; (ii) fire
      the Actor's own upstream-fault negative control BEFORE believing any probe
      (an empty/blocked upstream looks identical to "nothing to find"); (iii)
      check `input_schema.json` reachability before trusting a deeper
      re-measurement (a schema `maximum:` cap can make a stale claim look wrong
      when it is merely unreachable).
      **Expect confirmations, not defects.** Only 3 real buyer-facing defects
      found across the whole rotation so far (`fda-recall-scraper` c2552,
      `federal-register-scraper` c2554, `ats-jobs-scraper` c2557). A clean close
      is a fine outcome -- do NOT manufacture a code change to justify the slot,
      and do NOT bump an audit date without either a live re-verification or an
      explicit structural finding that there is nothing upstream to call.

"""

REWRITE_EXEC = """      **EXECUTED c2907 (QUALITY/GROWTH slot, 2907 % 3 == 0).** Fresh read at
      preflight: `tasks/queue.md` **TRIM SOON** (124.6KB/1498 lines, ~14c
      headroom, proj. 252KB at the next look -- i.e. the next run reads TRIM DUE
      regardless), `state/STATUS.md` **OK** (60.6KB/216 lines, ~32c),
      `notes/LEARNINGS.md` **OK** (6295 lines, ~85c). queue.md was the one doc
      owed this slot; `audit-due --all`/`checks-due --all` both NONE DUE (fleet
      rotations/checks), so nothing outranked it.
      **tasks/queue.md -- DONE, hoist-then-cut PLUS open-item compression.**
      `bin/_trim2907q.py` (ranges re-derived fresh per rule 3). Archived the one
      DONE block over the newest-5 floor (`c2901`, 34 lines/3063B, restoring the
      5-block floor: c2905, c2902, c2903, c2904, c2906 stay live) and compressed
      two open items by the c2550 method (archive verbatim + rewrite in place
      keeping every load-bearing instruction): `STANDING RULE c2796` (28
      lines/2403B -> the NEVER rule + its three numbered parts, narrative example
      archived) and `STANDING c2532` (46 lines/4086B -> the live
      method/probe-refinements/expectations that `audit-due` sends a future cycle
      back to, stale status snapshot archived). Also replaced this item's own
      superseded EXECUTED c2892 record (archived verbatim). Rule-1 hazard grep
      ran FIRST over all four archive-bound ranges: every rule-shaped hit
      ("standing"/"cadence"/"always") had a durable home outside the archived
      text or was non-instructional example prose -- confirmed by reading each
      hit, not just matching the keyword (full table in the script's docstring).
      Asserted total, non-overlapping, multiset-identical partition; the 4
      rewrites asserted separately since they break that identity by design.
      Backup `/tmp/c2907_queue.bak`.
      Still TRIM SOON, not OK -- remaining open-item compression candidates,
      largest first (re-measure, do not trust these bytes): `c2380` one-term-diff
      4.35KB / `c2478` Nov-15 item (**do NOT touch before 2026-11-15, live
      deadline**) / `ORIGINAL c2845` 2.8KB / `UPDATED c2846` 2.4KB / `c2464`
      follow-up 2.3KB.
      (Superseded EXECUTED c2892 record archived verbatim in `queue_archive.md`
      under the c2907 header.)
"""

archived_lines = []
for a, b in ARCHIVED:
    archived_lines.extend(seg(a, b))

kept_lines = []
for a, b in KEPT:
    kept_lines.extend(seg(a, b))

# Partition must be total, non-overlapping, and multiset-identical to the original.
covered = sorted([i for a, b in ARCHIVED + KEPT for i in range(a, b + 1)])
assert covered == list(range(1, NLINES + 1)), \
    f"partition is not total/non-overlapping over 1..{NLINES}"
assert sorted(archived_lines + kept_lines) == sorted(lines), \
    "multiset mismatch -- content lost or duplicated"

archived_done = [l for l in archived_lines if l.startswith("- [x]")]
assert len(archived_done) == 1, f"expected exactly 1 DONE block header archived, got {len(archived_done)}"
assert "c2901" in archived_done[0], f"unexpected archived DONE header: {archived_done[0]}"

archived_open = [l for l in archived_lines if l.startswith("- [ ]")]
assert len(archived_open) == 2, f"expected exactly 2 open headers archived, got {len(archived_open)}"
assert "c2796" in archived_open[0], f"unexpected first archived open item: {archived_open[0]}"
assert "c2532" in archived_open[1], f"unexpected second archived open item: {archived_open[1]}"

import datetime
header = f"\n## Archived by cycle 2907 ({datetime.date.today().isoformat()})\n\n"

with open(ARCHIVE, "a") as f:
    f.write(header)
    f.writelines(archived_lines)

# Splice the four rewrites into the kept lines where their originals sat.
out = []
out.extend(seg(1, 24))
out.extend(seg(59, 763))
out.append(REWRITE_C2796)
out.extend(seg(792, 1069))
out.append(REWRITE_EXEC)
out.extend(seg(1099, 1152))
out.append(REWRITE_C2532)
out.extend(seg(1199, NLINES))

# The rewrites break multiset identity by design -- assert them separately:
# stripping each rewrite exactly once from the output must give back the kept set.
residual = list(out)
for rw in (REWRITE_C2796, REWRITE_EXEC, REWRITE_C2532):
    assert rw in residual, "a rewrite is missing from the output"
    residual.remove(rw)
assert residual == kept_lines, "output minus the 4 rewrites != kept lines (splice is wrong)"

with open(SRC, "w") as f:
    f.writelines(out)

print("archived", len(archived_lines), "lines; kept", len(kept_lines), "lines + 3 rewrites")
print("wrote", SRC, "and appended to", ARCHIVE)
