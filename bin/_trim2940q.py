#!/usr/bin/env python3
"""c2940 QUALITY-slot trim of tasks/queue.md (flagged TRIM SOON by check-doc-size this
cycle: 123.0KB/1485 lines, ~14c headroom at +5440 B/cycle, 251KB projected at the
checker's next look; plus an explicit rule-6 flag -- the newest DONE block is 23 lines
against the ~20-line cap).

Three operations, all ranges re-derived fresh from the live file this cycle (doc-trim
rule 3, never paste forward). Every archive-bound range is hazard-grepped FIRST
(rule 1) and every hit printed for reading before anything is written.

A. REWRITE lines 1-22 -- the newest DONE block (c2939), 23 lines incl. its trailing
   blank, which `bin/check-doc-size` flags as OVER rule 6's ~20-line cap. Rule 6's own
   remedy is "put the full narrative in STATUS.md and keep this file's copy to the
   cap"; the full c2939 narrative is already in state/STATUS.md's c2939 block (kept
   live by this cycle's keep-newest-10 STATUS trim), so the queue copy is compressed to
   14 lines. Original archived verbatim.

B. CUT lines 135-236 -- the 6 cycle-level DONE blocks over the newest-5-kept-live floor
   (c2934, c2933, c2932, c2931, c2930, c2929, in that source order), contiguous, plus
   the trailing blank separator at 236. Leaves c2939/c2938/c2937/c2936/c2935 live,
   matching STATUS.md's convention. 11 cycle-level DONE blocks were live; `CLOSED
   c2927` (line 415) is a closed ITEM, not a cycle block, and is deliberately untouched.

C. REWRITE lines 1051-1101 -- the header plus the TWO stacked execution records inside
   the still-open `doc-trim cadence` item (`EXECUTED c2916`, its re-measured candidate
   list, `RE-MEASURED c2934`, and the superseded-c2907 pointer). At 8880B/104 lines
   that item is the largest open item in the file by 2x, and it is in violation of its
   OWN header rule ("KEEP THIS ITEM IN THIS SHAPE: method + standing rules + newest
   execution only. Do NOT prepend a full narrative per trim"). This is precisely the
   "scan for genuinely superseded/duplicate content fresh" lever c2934 said to use
   instead of re-reading its candidate list. Replaced by one compressed `EXECUTED
   c2940` record that PRESERVES c2934's standing verdict (the only home of it) and the
   live 2026-11-15 guard on the c2478 item. Lines 1102-1153 -- the six STANDING RULES,
   the Method block and the standing hazard note, marked "they are now ONLY here, so do
   not archive this section" -- are NOT touched by any range here.

The kept/archived partition is asserted total and non-overlapping over 1..N. Multiset
identity is asserted for the pure CUT only; the two rewrites break identity by design,
so their replacement text is asserted separately (rule: assert any new rewrite text
separately -- the Method block's own instruction).
"""
import os
import re
import sys
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
BACKUP = "/tmp/c2940_queue.bak"
HEADER = "## Archived by cycle 2940 (2026-11-09)"

NLINES = 1486  # 1485 real lines + the empty trailing element from the final newline

# (start, end, label, replacement_lines_or_None)  -- None means a pure cut
A_NEW = """\
- [x] **DONE c2939 (regular slot) -- took the DUE `varied_test: app-store-reviews-scraper`
      rotation and closed the gap c2603 left open: webhookUrl had never been tested on a
      genuine SUCCESS path with delivered rows (c2603's only attempt hit a live Apple-feed
      outage and FAILED).** Feed healthy again (verified live first). 2 cheap real runs vs
      Spotify, each with `webhookUrl` -> a fresh webhook.site token: maxResults 5 charged
      `{result:0}` (inside the Actor's `FREE_REVIEWS_PER_RUN=10` free tier -- read
      `chargeAndPush()` before calling that a leak, it isn't); maxResults 15 charged
      `{result:5}` (15-10). Both webhook payloads matched the real run's
      `actorRunId`/`defaultDatasetId` and were byte-identical to its `RUN_SUMMARY`.
      **0 defects**, no code change; the mechanism (main.js:1635-1673) is now verified on
      this Actor across every reachable outcome. `check-charges` 1/0/0, `check-pricing`
      27/33/0. ~$0.002. Recorded in `audit_dates.json` (`varied_test` -> 2939).
      Full narrative in `state/STATUS.md`'s c2939 block (rule 6).
      **NEXT: no fleet rotation DUE after this reset (soonest `check-source-endpoints` c2942).**"""

C_NEW = """\
- [ ] **doc-trim cadence (orig. c2508, REWRITTEN c2520-c2588; execution records COMPRESSED
      c2652, re-compressed c2736, re-compressed c2940 -- the c2604/c2605/c2628/c2634/c2643
      narratives and the c2733 STATUS.md record are verbatim in `queue_archive.md` under the
      c2652/c2736 headers, and the `EXECUTED c2916` + `RE-MEASURED c2934` records under the
      c2940 header. KEEP THIS ITEM IN THIS SHAPE: method + standing rules + newest execution
      only. Do NOT prepend a full narrative per trim -- that habit grew this one item to 32%
      of the live queue once, and by c2940 it had regrown to 8.9KB/104ln (largest open item,
      2x the next) purely by stacking a second execution record on top of the first.)**
      **EXECUTED c2940 (QUALITY/GROWTH slot).** Fresh preflight read: `STATUS.md` TRIM SOON
      (135.6KB/471ln, ~15c), `queue.md` TRIM SOON (123.0KB/1485ln, ~14c) + a rule-6 flag on
      the newest DONE block (23ln vs the ~20 cap), `LEARNINGS.md` OK (6756ln, ~62c). Nothing
      rotation/check/inbox due, so nothing outranked the trim.
      **STATUS.md** (`bin/_trim2940s.py`, pure cut, keep-newest-10): 135.6KB/471ln ->
      50.1KB/166ln; archived c2929-c2912 (18 blocks). 57 hazard hits, all read, all narrative
      about rules homed elsewhere (LEARNINGS c2926/c2929, the c2120 preflight rule, rule 3/6
      which live in `bin/check-doc-size` and this item) -- no rescue needed.
      **queue.md** (`bin/_trim2940q.py`, hoist-then-cut + 2 rewrites): DONE-block floor
      (archived c2934-c2929, kept c2939-c2935) + rule-6 compression of the c2939 block
      (23ln -> 14ln, full narrative already in STATUS.md) + this item's two stacked execution
      records. **Margin arithmetic (rule 4), stated honestly: the result still reads TRIM
      SOON, and that is the file's steady state, not a failed trim** -- the checker projects
      +130KB over its own 24c look interval, so any post-trim size above ~70KB reads TRIM
      SOON and a newest-5 floor cannot reach 70KB (LEARNINGS c2856 pt 4).
      **STANDING -- carried forward from c2934's re-measurement, this is its only home:
      the c2916 candidate list (c2380 / c2478 / c2880 / c2336 / c2895 / c2464 / c2532 /
      c2809) is a DEAD END; stop re-reading it each QUALITY slot.** c2934 read the top
      three live: all are dense, already-once-compressed STANDING METHOD documentation a
      future audit executes, not stale narrative -- cutting them trades real operational
      content for a few hundred bytes. c2880/c2809 are already at their floor.
      `c2478` stays guarded (**live 2026-11-15 deadline, do NOT touch before then**) and
      `c2336` is a live triage tripwire. The only levers that have actually worked are the
      DONE-block-floor rotation and finding a NEW compression target by scanning for
      genuinely superseded/duplicate content fresh -- which is how c2940 found THIS item."""

OPS = [
    (1, 22, "REWRITE c2939 DONE block (rule 6: 23ln -> 14ln)", A_NEW.split("\n")),
    (135, 236, "CUT DONE c2934+c2933+c2932+c2931+c2930+c2929 (newest-5 floor)", None),
    (1051, 1101, "REWRITE doc-trim cadence item header + 2 stacked execution records", C_NEW.split("\n")),
]


def main():
    orig = open(QUEUE).read()
    lines = orig.split("\n")
    n = len(lines)
    assert n == NLINES, f"expected {NLINES} lines, got {n} -- file changed, abort"

    # --- partition: total and non-overlapping over the touched ranges ---
    taken = {}
    for a, b, label, _ in OPS:
        for i in range(a, b + 1):
            assert i not in taken, f"overlap at line {i}: {label} vs {taken[i]}"
            assert 1 <= i <= n, f"line {i} out of range (file has {n})"
            taken[i] = label
    kept_idx = [i for i in range(1, n + 1) if i not in taken]
    assert len(kept_idx) + len(taken) == n, "partition is not total over 1..N"

    # --- boundary sanity: every range starts and ends where we think it does ---
    assert lines[0].startswith("- [x] **DONE c2939"), f"L1: {lines[0][:60]!r}"
    assert lines[22].strip() == "", "L23 should be the blank after the c2939 block"
    for ln, frag in [(135, "c2934"), (154, "c2933"), (168, "c2932"),
                     (188, "c2931"), (210, "c2930"), (220, "c2929")]:
        head = lines[ln - 1]
        assert head.startswith("- [x] **DONE"), f"L{ln} is not a DONE head: {head[:60]!r}"
        assert frag in head, f"L{ln} does not mention {frag}: {head[:80]!r}"
    assert lines[235].strip() == "", "L236 should be the blank closing the cut range"
    assert lines[236].startswith("- [ ] "), f"L237 should start a new open item: {lines[236][:60]!r}"
    assert lines[1050].startswith("- [ ] **doc-trim cadence"), f"L1051: {lines[1050][:60]!r}"
    assert lines[1100].strip() == "header.)", f"L1101 should end the superseded-c2907 pointer: {lines[1100]!r}"
    assert "STANDING RULES" in lines[1101], \
        f"L1102 must be the start of the do-not-archive STANDING RULES block: {lines[1101][:70]!r}"
    assert lines[1152].rstrip().endswith("lives in CLAUDE.md."), \
        f"L1153 should be the last line of the item: {lines[1152]!r}"

    # --- rule 1: hazard grep EVERY archive-bound range, print every hit ---
    hazard = re.compile(r"standing|cadence|always |never |do not |must |\brule\b", re.I)
    total_hits = 0
    for a, b, label, _ in OPS:
        hits = [(i, lines[i - 1]) for i in range(a, b + 1) if hazard.search(lines[i - 1])]
        total_hits += len(hits)
        print(f"\nrule-1 hazard grep -- {label} ({a}-{b}): {len(hits)} hit(s)")
        for i, l in hits:
            print(f"  L{i}: {l.strip()[:150]}")
    print(f"\ntotal hazard hits across all ranges: {total_hits}")

    # --- build the archive text (every touched range, verbatim) ---
    chunks = []
    marker_re = re.compile(r"^<!-- c2940: ")
    for a, b, label, _ in OPS:
        chunks.append(f"<!-- c2940: {label}, queue.md lines {a}-{b} -->")
        chunks.extend(lines[a - 1:b])
        chunks.append("")
    archive_text = "\n".join([HEADER, ""] + chunks)

    # --- build the new live file ---
    out = []
    i = 1
    while i <= n:
        op = next((o for o in OPS if o[0] == i), None)
        if op:
            a, b, label, repl = op
            if repl is not None:
                out.extend(repl)
            i = b + 1
        else:
            out.append(lines[i - 1])
            i += 1
    new_live = "\n".join(out)

    # --- losslessness: every ORIGINAL non-blank line is in live-or-archive ---
    def nb(text):
        return Counter(l for l in text.split("\n") if l.strip())

    got = nb(new_live) + nb(archive_text)
    got -= nb("\n".join(c for c in chunks if marker_re.match(c)))
    got -= nb(HEADER)
    for _, _, _, repl in OPS:
        if repl is not None:
            got -= nb("\n".join(repl))
    want = nb(orig)
    missing = want - got
    extra = got - want
    assert not missing, f"LINES LOST: {list(missing)[:5]}"
    assert not extra, f"UNEXPLAINED LINES: {list(extra)[:5]}"
    print("lossless check: OK (every non-blank original line is in live+archive; "
          "rewrite text accounted for separately)")

    # --- rewrites asserted separately (they break multiset identity by design) ---
    new_lines = new_live.split("\n")
    done_heads = [l for l in new_lines if l.startswith("- [x] **DONE c29")]
    assert len(done_heads) == 5, f"expected 5 cycle-level DONE blocks live, got {len(done_heads)}"
    for frag in ["c2939", "c2938", "c2937", "c2936", "c2935"]:
        assert any(frag in h for h in done_heads), f"{frag} DONE block went missing"
    assert len(A_NEW.split("\n")) <= 20, "rewritten c2939 block still over rule 6's ~20-line cap"
    # the do-not-archive section must survive verbatim and exactly once
    for probe in ["**STANDING RULES -- these six were rescued",
                  "1. **Grep FIRST, then cut.**",
                  "6. **DONE blocks are capped in LENGTH, not count",
                  "**Standing hazard, re-checked c2588, nothing found:**"]:
        assert sum(probe in l for l in new_lines) == 1, f"do-not-archive probe lost/duped: {probe!r}"
    # c2934's verdict must survive the rewrite in substance
    for probe in ["DEAD END", "2026-11-15", "stop re-reading it each QUALITY slot"]:
        assert probe in new_live, f"carried-forward standing content missing: {probe!r}"
    assert new_lines.count("- [ ] **doc-trim cadence (orig. c2508, REWRITTEN c2520-c2588; "
                           "execution records COMPRESSED") == 1, "cadence item header not unique"
    print("rewrite asserts: OK (5 DONE blocks live, c2939 block within rule 6, "
          "do-not-archive section intact, c2934 verdict carried forward)")

    if "--dry-run" in sys.argv:
        print(f"\nDRY RUN: {len(orig)}B/{n}ln -> {len(new_live)}B/{len(out)}ln "
              f"({len(orig) - len(new_live)}B saved); archive +{len(archive_text)}B")
        return

    open(BACKUP, "w").write(orig)
    assert os.path.exists(ARCHIVE), "archive missing -- do not create a second one, investigate"
    with open(ARCHIVE, "a") as f:
        f.write("\n" + archive_text + "\n")
    open(QUEUE, "w").write(new_live)
    print(f"\nqueue.md: {len(orig)}B/{n}ln -> {len(new_live)}B/{len(out)}ln "
          f"({len(orig) - len(new_live)}B saved). Backup {BACKUP}")


if __name__ == "__main__":
    main()
