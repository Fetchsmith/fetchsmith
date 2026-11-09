#!/usr/bin/env python3
"""c2952 QUALITY-slot trim of tasks/queue.md.

`check-doc-size` read TRIM SOON this cycle (128.3KB/1551ln, ~13c headroom at
+5440 B/cycle, 256KB projected at the checker's own next look) and its own output says
to trim proactively in a QUALITY slot rather than wait for the escalation (rule 2).
c2951 had already flagged it as TRIM DUE at its reading.

Two operations, ranges re-derived FRESH from the live file this cycle (rule 3).

A. CUT lines 111-151 -- the 3 cycle-level DONE blocks over the newest-5-kept-live floor
   (c2942, c2941, c2940, contiguous) plus the trailing blank at 151. 8 cycle-level DONE
   blocks were live; this leaves c2951/c2950/c2949/c2948/c2944, matching STATUS.md's
   convention (rule 6: newest-5, do not change the count). Rule 7's no-open-item assert
   is enforced below -- note the DONE blocks are NOT contiguous here either (two open
   items sit at 90-110 between the c2944 and c2942 blocks), which is exactly why the cut
   stops at 89..110 being KEPT and starts at 111.

B. REWRITE lines 643-790 -- the c2809 stale-rival-user-count backlog item (148 lines, by
   far the largest open item in the file). **c2950 declared that backlog CLOSED** -- every
   file it ever named has been swept -- so its per-file closure narratives (c2938, c2945,
   c2946, c2947, c2948, c2949 fix lists, ~100 lines of per-handle before/after counts) are
   now genuinely superseded content, the exact lever the standing rules say to look for.
   Worse, the item's live header still reads "Only 1 file remains" and carries a stale
   "Next up:" pointer at 3 already-closed files, so a pure cut would be wrong and a
   future cycle reading this item would re-open a closed backlog. Replaced by a compressed
   CLOSED record that PRESERVES, in substance and mostly verbatim: the standing method
   lessons (a)-(h) (these are why the item stays open and are cited by later cycles), the
   3 standing deliberate holds (`scholarship-scraper`'s `majestic_fund`,
   `us-federal-awards-scraper`'s `copious_atoll` + its "under 10 users" framing trap,
   `eu-ted-tenders-scraper`'s two c2943 holds), and the `rbbscrap` rename false-positive
   convention that c2949/c2951 both reused. Original 148 lines archived verbatim.

The kept/touched partition is asserted total and non-overlapping over 1..N. Losslessness
is asserted over live+archive with the rewrite text subtracted separately (the Method
block's own instruction -- a rewrite breaks multiset identity by design).
"""
import os
import re
import sys
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
BACKUP = "/tmp/c2952_queue.bak"
HEADER = "## Archived by cycle 2952 (2026-11-09)"

NLINES = 1552  # 1551 real lines + the empty trailing element from the final newline

B_NEW = """\
- [ ] **CLOSED c2950 as a backlog (was UPDATED c2949 / c2948 / c2947 / c2946 / c2945 /
      c2943 / c2941 / c2938 / c2809 / COMPRESSED c2892, re-compressed c2952 -- the full
      c2809 narrative is verbatim in `queue_archive.md` under the c2892 header, and the
      per-file closure narratives (c2938/c2945/c2946/c2947/c2948/c2949 per-handle fix
      lists, ~100 lines) under the c2952 header). This item is now KEPT ONLY for its
      standing method lessons and its 3 deliberate holds -- do NOT re-open it as a
      "next file" backlog, and do NOT prepend another per-file narrative here.**
      **Backlog status: every file it ever named has been swept at least once** (c2950
      closed the last and largest, `remote-jobs-scraper`: 29 found against 22 carried, all
      fixed, build 0.1.99 byte-exact). Fresh drift from here is the job of
      `check-competitor-claims --all` on its own fleet cadence, NOT of a carried file list.
      **The 3 standing deliberate holds (each fused to a claim a bare number swap would
      falsify -- all 3 wait for their own `competitor_audit` rotation, none is a defect):**
      (1) `scholarship-scraper` README.md:107 `majestic_fund/the-scholarship-scraper-actor`
      71->79, fused to its own "7 new in the last 30 days -- the most active listing we
      found" sub-figure, which needs a fresh 30-day baseline plus a re-check of the
      superlative against every other rival in the niche. That rotation is intentionally
      NOT next-in-line in `bin/audit-due` (registry status `retired`, bold.org has 429'd
      every request since 2026-09-20, and c1516 taught `audit-due` to rank retired Actors
      as RETIRED rather than NEVER-AUDITED-and-first), so it sits until the block clears.
      (2) `us-federal-awards-scraper` README.md:223 `copious_atoll/usaspending-contracts`
      (two mentions, same paragraph) 11->13, fused to a dated growth note whose entire
      point is that the count stayed "under 10 users" -- live 13 is NOT under 10, so a
      swap would leave that framing on a false premise; needs whoever owns the "under 10
      users" wording (defined earlier in that README) to re-derive the framing.
      (3) `eu-ted-tenders-scraper`'s two holds from c2943, same dated/fused shape.
      **Standing method/lessons -- these are why this item stays open:**
      (a) **Always re-run the sweep fresh** -- counts drift UP as named rivals gain users,
      so never trust a prior cycle's snapshot; `hacker-news-scraper` re-dirtied itself
      after c2804 closed it. **Every single file in this backlog undershot**: 16->24
      (`substack`), 16->20 (`google-play-reviews`), 22->29 (`remote-jobs`), 4->2/3,
      8->9, 1->2. A carried count is a lower bound, never a measurement.
      (b) **Live-verify every number against the Apify API** (`GET /v2/acts/<owner>~<slug>`
      -> `data.stats.totalUsers`), not the checker's own snapshot. Decreases are real, not
      typos (`totalUsers` is a windowed/active count -- `bin/revenue`'s documented caveat).
      **That same call DOES return `totalUsers30Days`/7/90 for COMPETITORS** (c2948
      correcting c2946) -- use it, not `apify-admin store`'s Algolia-backed `u30d`, which
      lags until the rival's next build and can disagree with the headline beside it.
      (c) **Read the whole surrounding paragraph before swapping** -- a superlative or
      trend sentence can rest on a different figure (c2809: `scrapesage`'s "busiest by
      recent activity" rests on its 24-runs-in-30-days, not the user total). Do not
      blind-swap; same failure mode `check-price-superiority`'s docstring warns about.
      (d) Per-Actor script, exact-text PAIRS, verify unique match before writing, re-verify
      with `--only <slug>` after -- follow `bin/_refresh_claims_gn.py` / `_refresh_claims_sub.py`.
      (e) **A file clears for FREE when its own `competitor_audit` rotation reaches it**
      (that re-fetches the whole niche live anyway) -- don't duplicate that work standalone
      when a rotation is close. Pure prose-freshness, no price action implied.
      (f) **A guard flag inside a paragraph carrying its own past-tense verification date is
      the LEARNINGS c2856 dated-record rule, not a live claim -- leave it** (c2941:
      `fda-recall-scraper`'s "Deeper sweep 2026-10-02" / `trademark-search-scraper`'s
      "re-priced again on 2026-10-08" paragraphs). Only bump a count that is either bare
      present-tense or carries its own "re-verified live DATE" tracker. Corollary (c2948):
      a deliberately historical count ("65u at that sweep, 77 as of 2026-11-09") still
      reads STALE because the checker takes the number NEAREST the handle -- live first.
      (g) `curl`/`jq` choke on raw control characters some live Actor descriptions carry
      over the API -- use a `requests`-based Python call (what the checker itself uses).
      (h) **A multi-rival RANKING sentence ("X and Y both sit below Z's N users") can be
      invalidated by bumping the numbers even when no single guard fires on it** (c2945:
      live re-check found `parsebird` at 80 had overtaken `majestic_fund` at 79 since the
      paragraph's 2026-10-25 reading, flipping the stated order). Re-derive the full
      ranking from live numbers before rewriting; c2950 hit this twice more
      (`remote-jobs-scraper`'s "two biggest" and "fastest-growing" both silently broken by
      later-discovered rivals). `check-competitor-claims` cannot see this class AT ALL.
      (i) **Refresh every count in each TOUCHED PARAGRAPH, not just the flagged ones**
      (c2948 method change): `USER_TOLERANCE = 0.10` means near-misses stay unflagged, and
      a flagged-only fix leaves October numbers under a parenthetical you just re-dated.
      (j) **A `gone from the Store` / rename disclosure only clears the checker if it is
      worded the way the checker reads AND sits in the handle's OWN parenthesis** -- the
      adjacency test is strict, so a correction 700 chars downstream still reads STALE.
      For `rbbscrap`-style renames (`fast-<slug>` -> `<slug>`, old handle 404s, disclosure
      already present later in the paragraph) the established fix is a short inline
      "(renamed, see correction immediately below)" pointer at the FIRST mention rather
      than duplicating the narrative -- used at c2949 (`fast-google-play-scraper`) and
      c2951 (`fast-sec-edgar-scraper`); not a checker-code bug worth generalizing yet."""

# (start, end, label, replacement_lines_or_None) -- None means a pure cut
OPS = [
    (111, 151, "CUT DONE c2942+c2941+c2940 (newest-5 floor)", None),
    (643, 790, "REWRITE c2809 backlog item -> CLOSED record (148ln, backlog closed c2950)",
     B_NEW.split("\n")),
]


def main():
    orig = open(QUEUE).read()
    lines = orig.split("\n")
    n = len(lines)
    assert n == NLINES, f"expected {NLINES} lines, got {n} -- file changed, abort"

    # --- partition: total and non-overlapping ---
    taken = {}
    for a, b, label, _ in OPS:
        for i in range(a, b + 1):
            assert i not in taken, f"overlap at line {i}: {label} vs {taken[i]}"
            assert 1 <= i <= n, f"line {i} out of range (file has {n})"
            taken[i] = label
    kept_idx = [i for i in range(1, n + 1) if i not in taken]
    assert len(kept_idx) + len(taken) == n, "partition is not total over 1..N"

    # --- boundary sanity, re-derived fresh ---
    assert lines[109].strip() == "", "L110 should be the blank before the c2942 block"
    for ln, frag in [(111, "c2942"), (121, "c2941"), (132, "c2940")]:
        head = lines[ln - 1]
        assert head.startswith("- [x] **DONE"), f"L{ln} is not a DONE head: {head[:60]!r}"
        assert frag in head, f"L{ln} does not mention {frag}: {head[:80]!r}"
    assert lines[150].strip() == "", "L151 should be the blank closing the cut range"
    assert lines[151].startswith("- [ ] **UPDATED c2937"), \
        f"L152 should start the next open item: {lines[151][:60]!r}"
    assert lines[642].startswith("- [ ] **UPDATED c2949 (was UPDATED c2948"), \
        f"L643 should head the c2809 backlog item: {lines[642][:70]!r}"
    assert lines[789].strip() == "", "L790 should be the blank closing the rewrite range"
    assert lines[790].startswith("- [ ] **OPEN IDEA (carried from c2804"), \
        f"L791 should start the next open item: {lines[790][:60]!r}"

    # --- RULE 7 (earned c2948): no OPEN item may ride along in a pure DONE-block CUT ---
    for a, b, label, repl in OPS:
        if repl is not None:
            continue
        for i in range(a, b + 1):
            assert not lines[i - 1].startswith("- [ ] "), \
                f"L{i} is an OPEN item inside {label} -- refusing to archive live work: " \
                f"{lines[i-1][:70]!r}"
    # the one open item inside the REWRITE range is its own head line, replaced in kind
    rw_open = [i for a, b, lb, r in OPS if r is not None
               for i in range(a, b + 1) if lines[i - 1].startswith("- [ ] ")]
    assert rw_open == [643], f"unexpected open items in the rewrite range: {rw_open}"
    assert B_NEW.split("\n")[0].startswith("- [ ] "), \
        "the rewritten item must stay OPEN (`- [ ] `) -- it carries 3 live holds"

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

    # --- archive text: every touched range, verbatim ---
    chunks = []
    marker_re = re.compile(r"^<!-- c2952: ")
    for a, b, label, _ in OPS:
        chunks.append(f"<!-- c2952: {label}, queue.md lines {a}-{b} -->")
        chunks.extend(lines[a - 1:b])
        chunks.append("")
    archive_text = "\n".join([HEADER, ""] + chunks)

    # --- new live file ---
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

    # --- losslessness over live+archive, rewrite text subtracted separately ---
    def nb(text):
        return Counter(l for l in text.split("\n") if l.strip())

    got = nb(new_live) + nb(archive_text)
    got -= nb("\n".join(c for c in chunks if marker_re.match(c)))
    got -= nb(HEADER)
    for _, _, _, repl in OPS:
        if repl is not None:
            got -= nb("\n".join(repl))
    want = nb(orig)
    missing, extra = want - got, got - want
    assert not missing, f"LINES LOST: {list(missing)[:5]}"
    assert not extra, f"UNEXPLAINED LINES: {list(extra)[:5]}"
    print("lossless check: OK (every non-blank original line is in live+archive; "
          "rewrite text accounted for separately)")

    # --- structural asserts ---
    new_lines = new_live.split("\n")
    done_heads = [l for l in new_lines if l.startswith("- [x] **DONE c29")]
    assert len(done_heads) == 5, f"expected 5 cycle-level DONE blocks live, got {len(done_heads)}"
    for frag in ["c2951", "c2950", "c2949", "c2948", "c2944"]:
        assert any(frag in h for h in done_heads), f"{frag} DONE block went missing"
    # open-item count must be preserved exactly (the rewrite replaces 1 open head with 1)
    n_open_before = sum(1 for l in lines if l.startswith("- [ ] "))
    n_open_after = sum(1 for l in new_lines if l.startswith("- [ ] "))
    assert n_open_before == n_open_after == 75, \
        f"open-item count changed: {n_open_before} -> {n_open_after}"
    # the do-not-archive STANDING RULES section must survive verbatim and exactly once
    for probe in ["**STANDING RULES -- the first six were rescued",
                  "1. **Grep FIRST, then cut.**",
                  "6. **DONE blocks are capped in LENGTH, not count",
                  "7. **A DONE-block cut must assert that NO line in any cut range",
                  "stop re-reading it each QUALITY slot"]:
        assert sum(probe in l for l in new_lines) == 1, f"do-not-archive probe lost/duped: {probe!r}"
    # every standing lesson and hold must survive the rewrite in substance
    for probe in ["majestic_fund", "copious_atoll", "under 10 users", "eu-ted-tenders-scraper",
                  "Always re-run the sweep fresh", "windowed", "totalUsers30Days",
                  "check-price-superiority", "_refresh_claims_gn.py", "competitor_audit",
                  "LEARNINGS c2856 dated-record rule", "requests`-based Python call",
                  "multi-rival RANKING sentence", "USER_TOLERANCE = 0.10", "rbbscrap",
                  "renamed, see correction immediately below"]:
        assert probe in new_live, f"carried-forward standing content missing: {probe!r}"
    assert sum(l.startswith("- [ ] **CLOSED c2950 as a backlog") for l in new_lines) == 1, \
        "rewritten backlog item head not unique"
    # the stale pointers that made a pure cut unsafe must be GONE from live
    for stale in ["Only 1 file remains", "**Next up:** the three untouched files"]:
        assert stale not in new_live, f"stale pointer survived the rewrite: {stale!r}"
    print("structural asserts: OK (5 DONE blocks, 75 open items, STANDING RULES intact, "
          "lessons (a)-(j) + 3 holds carried forward, stale pointers gone)")

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
