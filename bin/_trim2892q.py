#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2892 (125.6KB / 1462 lines, TRIM SOON).

QUALITY/GROWTH slot (2892 % 3 == 0, computed fresh). Fresh preflight read
`audit-due --all` FLEET ROTATIONS NONE DUE and `checks-due --all` NONE DUE, so
the doc-trim cadence item is the valid top task (standing rule 2's slot).
`check-doc-size` reads tasks/queue.md **TRIM SOON** (122.7KB at preflight,
~15c headroom, proj. 250KB at its own next look) -- the only non-OK doc.

Method: hoist-then-cut on the DONE bucket PLUS two open-item compressions
(rule 4's margin arithmetic: the DONE bucket alone is ~11.4KB against a
TRIM-SOON trigger of 200KB - 5440*24 = ~72.5KB, so a DONE-only cut cannot
reach a durable OK and rule 4 says compress open items in the same cycle).
The two compressed items are exactly the ones c2880's measured per-item byte
table named as cheapest-fat-per-risk and that no later cycle has taken:
`UPDATED c2809` (3.8KB) and the `c2336` ext_bad30d tripwire (2.7KB).

Ranges re-derived fresh from the live file this cycle (standing rule 3 --
never paste line numbers forward), each boundary confirmed by exact-line
inspection.

Standing-hazard check (rule 1: grep FIRST, then READ the hits) run before
writing this script over every archive-bound range, pattern
"standing|cadence|always |never |STANDING|do not |must |rule" (-i):
  - Range 159-290 (DONE c2886..c2882): every rule-shaped hit is narrative
    about prior trims/audits and points at a rule homed elsewhere -- the
    doc-trim item's own STANDING RULES (live, untouched, further down this
    file), the c2861 priority rule (notes/LEARNINGS.md "Cycle 2880"), and
    c2864's "always re-assert" rule (notes/LEARNINGS.md:5736). None is a
    sole home.
  - Ranges 674-712 and 1360-1387 are NOT archived-only: they are archived
    verbatim AND rewritten in place, with every load-bearing instruction
    carried into the rewrite (c2550 method). Checked instruction-by-
    instruction below.
  - Range 1053-1070 (doc-trim item's own superseded EXECUTED c2886 record):
    self-referential narrative about that trim's hazard-grep process; the
    numbered rules it refers to live at 1071+ and are untouched.

Correctness note folded into the c2336 rewrite (a real defect found while
re-running that tripwire's own instruction this cycle): its "current
confirmed state" line was stale in two directions. Re-diffed
state/revenue_history.json live -- the file is a rolling **400-snapshot
window that now only reaches back to 2026-10-31**, so the word "lifetime" is
no longer derivable from it at all; and the actual in-window set today is
steam-reviews-scraper FAILED 1 / remote-jobs-scraper TIMED-OUT 1 /
nih-reporter-scraper FAILED 1 (== ext_bad30d 3, stable since 2026-11-05 when
court-records-scraper's TIMED-OUT aged out). The old text omitted
steam-reviews entirely and claimed remote-jobs had aged out -- i.e. it would
have made a future cycle flag a 7-week-known entry as NEW and miss a real
new one. Corrected in place.

Partition is asserted total, non-overlapping and multiset-identical to the
original.
"""

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
NLINES = 1462

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == NLINES, f"expected {NLINES} lines, got {len(lines)} -- file changed, abort"


def seg(a, b):
    return lines[a - 1:b]


# Fully-historical content (159-290, 1053-1070) + the two open items that are
# archived verbatim and rewritten in place (674-712, 1360-1387).
ARCHIVED = [
    (159, 290),    # DONE c2886, c2885, c2884, c2883, c2882 (contiguous, no open items interleaved)
    (674, 712),    # UPDATED c2809 stale-claim item, rewritten in place below
    (1053, 1070),  # doc-trim item's own superseded EXECUTED c2886 record
    (1360, 1387),  # c2336 ext_bad30d tripwire, rewritten (and corrected) in place below
]

KEPT = [
    (1, 158),       # DONE c2891, c2890, c2888, c2887 (newest 4; c2892 is prepended)
    (291, 673),     # open items c2875 watch .. blank before c2809 item
    (713, 1052),    # open items after c2809 .. doc-trim item header + KEEP-THIS-SHAPE note
    (1071, 1359),   # doc-trim STANDING RULES + method .. blank before the c2336 tripwire
    (1388, NLINES), # blank + open items from c2312 follow-up .. end of file
]

NEW_DONE_BLOCK = """- [x] **DONE c2892 (QUALITY/GROWTH slot, 2892 % 3 == 0, computed fresh) -- executed the
      doc-trim cadence on `tasks/queue.md`, the only non-OK doc, and corrected a real stale
      claim inside the item being compressed.** Fresh preflight: `audit-due --all` FLEET
      ROTATIONS **NONE DUE** (only the informational one-off `count_audit` axes), `checks-due
      --all` **NONE DUE** (soonest `check-source-endpoints` in 2c, c2894), `inbox-triage new`
      **NONE UNTRIAGED of 75**, `bin/revenue` $0 booked / 27 Actors / 50 users / **818** runs30d
      (816 -> 818) / 3 ext_bad30d -- no buyer signal, no owner email owed.
      `bin/_trim2892q.py` (hoist-then-cut + rule-4 open-item compression, ranges re-derived
      fresh): archived DONE c2886..c2882 verbatim (newest 5 live: c2892, c2891, c2890, c2888,
      c2887, per rule 6), replaced the doc-trim item's superseded EXECUTED c2886 record, and
      compressed the two items c2880's byte table named cheapest-fat-per-risk -- `UPDATED
      c2809` and the `c2336` ext_bad30d tripwire -- archive-verbatim-then-rewrite (c2550
      method), every load-bearing instruction carried over. Rule-1 hazard grep ran FIRST on
      every archive-bound range; no sole-home rule archived.
      **Real defect found and fixed while re-running the c2336 tripwire's own instruction:**
      its "current confirmed state" line omitted `steam-reviews-scraper` FAILED (known since
      2026-10-26) and claimed `remote-jobs-scraper` had aged out when it has not -- so the
      tripwire would have flagged a long-known entry as NEW and missed a real one. Also
      `state/revenue_history.json` is a rolling 400-snapshot window now starting 2026-10-31,
      so "lifetime events" is no longer derivable from it; both corrected in place.
      **125.6KB/1462 lines -> see `bin/check-doc-size` for the measured post-cut size** (read
      the tool, not this prose, per rule 5). Lossless-verified by the script (total,
      non-overlapping, multiset-identical partition + every non-blank original line findable in
      live+archive). Backup `/tmp/c2892_queue.bak`. $0 spend (docs + read-only local/public
      checks only; no build, no Actor run).

"""

C2809_REWRITE = """- [ ] **UPDATED c2809 (COMPRESSED c2892 -- full c2809 narrative verbatim in `queue_archive.md`
      under the c2892 header) -- stale named-rival user-counts in Actor READMEs. 90 remain, all
      carrying a guard, across 11 files.** By file: `remote-jobs-scraper` 22, `substack-scraper`
      16, `google-play-reviews-scraper` 16, `us-federal-awards-scraper` 8, `google-news-scraper`
      7, `scholarship-scraper` 6, `eu-ted-tenders-scraper` 5, `trademark-search-scraper` 4,
      `fda-recall-scraper` 4, `website-screenshot-scraper` 1, `hacker-news-scraper` 1.
      Fully clean: `court-records`, `ats-jobs`, `app-store-reviews`, `apple-podcasts`,
      `shopify-products`, `sam-gov-opportunities`, `fec-campaign-finance`, `sec-insider-trades`.
      **Next up, smallest first:** `website-screenshot-scraper` and `hacker-news-scraper` (1
      claim each -- fastest clean win for a QUALITY/idle slot).
      **Standing method/lessons (these are why this item stays open):**
      (a) **Always re-run the sweep fresh** -- counts drift UP as named rivals gain users, so
      never trust a prior cycle's snapshot; `hacker-news-scraper` re-dirtied itself after c2804
      closed it.
      (b) **Live-verify every number against the Apify API** (`GET /v2/acts/<owner>~<slug>`),
      not the checker's own snapshot. Decreases are real, not typos.
      (c) **Read the whole surrounding paragraph before swapping** -- a superlative or trend
      sentence can rest on a different figure (c2809: `scrapesage`'s "busiest by recent
      activity" rests on its 24-runs-in-30-days, not the user total). Do not blind-swap; same
      failure mode `check-price-superiority`'s docstring warns about.
      (d) Per-Actor script, exact-text PAIRS, verify unique match before writing, re-verify with
      `--only <slug>` after -- follow `bin/_refresh_claims_gn.py` / `_refresh_claims_sub.py`.
      (e) **A file clears for FREE when its own `competitor_audit` rotation reaches it** (that
      re-fetches the whole niche live anyway) -- don't duplicate that work standalone when a
      rotation is close. Pure prose-freshness, no price action implied.
"""

C2336_REWRITE = """- [ ] **NEW STANDING TRIPWIRE (c2336, COMPRESSED c2775, RE-COMPRESSED + CORRECTED c2892 --
      earlier narratives verbatim in `queue_archive.md` under the c2775 and c2892 headers) --
      re-diff `ext_bad30d` out of `state/revenue_history.json` at the start of every cycle.
      ~2 seconds, $0, read-only. This is the ONLY signal we have that reflects a real buyer's
      run FAILING.**
      Shape: `snapshot['apify'][<slug>]['ext_stats30d']`; count the `FAILED` / `ABORTED` /
      `TIMED-OUT` keys with a non-zero value and print each per-Actor transition. A 6-line
      script, no one-liner needed (the original is in the archive).
      **CORRECTION c2892 -- `revenue_history.json` is a ROLLING 400-snapshot window** (~8 days
      at 2 cycles/hour; it began at 2026-10-31 as of this cycle), so **"lifetime events" is no
      longer derivable from this file** -- older events survive only in
      `state/STATUS_ARCHIVE.md` / `queue_archive.md`.
      **Current confirmed state (re-diffed live c2892, 2026-11-08; matches `ext_bad30d` 3):
      3 entries in-window, all long-known and resolved -- `steam-reviews-scraper` FAILED 1
      (2026-10-26, upstream `appreviews` degenerate empty body), `remote-jobs-scraper`
      TIMED-OUT 1 (the c2646 `got`-retry class, fixed fleet-wide), `nih-reporter-scraper`
      FAILED 1 (2026-11-03, guard rejecting NIH's own "FY2024" convention -- fixed, LEARNINGS
      Cycle 2647). Set has been STABLE since 2026-11-05, when `court-records-scraper`'s
      TIMED-OUT (2026-10-08) aged out. Also aged out and resolved: `google-news-scraper`
      TIMED-OUT, `scholarship-scraper` FAILED 2 (Actor retired).**
      **Any Actor name beyond those six is NEW and is the one to look at first.** (c2892 found
      the prior version of this line wrong in both directions -- it omitted steam-reviews and
      wrongly retired remote-jobs -- so re-derive the set, never trust this prose alone.)
      Triage order that worked: (1) is the Actor's `actor-health` green on its default input? if
      yes it is not an outage; (2) is it the TIMED-OUT class? **do not assume that axis is
      closed just because a `timeoutAt`/budget guard exists** -- c2471 called exactly such a
      guard a one-off and the failure recurred; the real defect (c2646) is that
      `timeout:{request:ms}` bounds one HTTP attempt, not one call, so `got`'s internal retries
      multiply it ~4x. Fixed with `AbortSignal.timeout()` clamped to `remainingMs()` (~19
      Actors + `_template`, commit `0a7e7800`); LEARNINGS Cycle 2646 has the full method if it
      resurfaces; (3) otherwise read every path that can end a run (`Actor.fail`, `throw`, the
      zero-row/partial status branches) for an input shape dropped without reaching a status
      message.
      **Do NOT email the owner about an `ext_bad30d` entry** -- a failed run is not revenue and
      not owner-fixable.
"""

NEW_EXECUTED_RECORD = """      **EXECUTED c2892 (QUALITY slot, 2892 % 3 == 0 -- the slot rule 2 asks for, no override
      needed; `audit-due --all` and `checks-due --all` both NONE DUE, so nothing outranked it).**
      Fresh read at preflight: `tasks/queue.md` **TRIM SOON** (122.7KB/1462 lines, ~15c
      headroom, proj. 250KB at the next look -- i.e. the next run reads TRIM DUE regardless),
      `state/STATUS.md` **OK** (91.0KB/1042 lines, ~25c), `notes/LEARNINGS.md` **OK** (5996
      lines, ~100c). queue.md was the one doc owed this slot.
      **tasks/queue.md -- DONE, hoist-then-cut PLUS rule-4 open-item compression.**
      `bin/_trim2892q.py` (ranges re-derived fresh per rule 3). Archived DONE c2886..c2882
      verbatim (newest 5 live per rule 6: c2892, c2891, c2890, c2888, c2887 -- no open items
      were interleaved in that range this time, so nothing needed hoisting); replaced this
      item's own superseded EXECUTED c2886 record; and compressed the two open items c2880's
      byte table named cheapest-fat-per-risk, `UPDATED c2809` (3.8KB) and the `c2336`
      ext_bad30d tripwire (2.7KB), by the c2550 method (archive verbatim + rewrite in place
      keeping every load-bearing instruction) -- a DONE-only cut was ~11.4KB against a
      ~72.5KB trigger, so rule 4 required this. **Rule-1 hazard grep ran FIRST** over every
      archive-bound range; every rule-shaped hit had a durable home outside the archived text
      (this item's own STANDING RULES, kept live; the c2861 rule in `notes/LEARNINGS.md`
      "Cycle 2880"; c2864's rule at `notes/LEARNINGS.md:5736`). Asserted total,
      non-overlapping, multiset-identical partition + an independent non-blank-line lossless
      check. Backup `/tmp/c2892_queue.bak`.
      Still TRIM SOON, not OK -- remaining candidates, largest first (re-measure, do not trust
      these bytes): c2380 one-term-diff 4.2KB / STANDING c2532 4.0KB / c2478 Nov-15 item 3.2KB
      (**do NOT touch before 2026-11-15, live deadline**) / ORIGINAL c2845 2.7KB / UPDATED
      c2846 2.3KB / STANDING RULE c2796 2.3KB / c2464 follow-up 2.2KB.
      (Superseded EXECUTED c2886 record archived verbatim in `queue_archive.md` under the c2892
      header.)
"""

# Reassemble in source order, splicing each rewrite exactly where its original sat.
final_lines = []
final_lines.extend(NEW_DONE_BLOCK.splitlines(keepends=True))
final_lines.extend(seg(*KEPT[0]))        # (1,158)
final_lines.extend(seg(*KEPT[1]))        # (291,673)
final_lines.extend(C2809_REWRITE.splitlines(keepends=True))
final_lines.extend(seg(*KEPT[2]))        # (713,1052)
final_lines.extend(NEW_EXECUTED_RECORD.splitlines(keepends=True))
final_lines.extend(seg(*KEPT[3]))        # (1071,1359)
final_lines.extend(C2336_REWRITE.splitlines(keepends=True))
final_lines.extend(seg(*KEPT[4]))        # (1388,NLINES)

# ---- Assertions ----
# 1. Partition of the original is total & non-overlapping.
all_ranges = sorted(ARCHIVED + KEPT)
covered = set()
for a, b in all_ranges:
    r = set(range(a, b + 1))
    assert not (covered & r), f"overlap at {a}-{b}"
    covered |= r
assert covered == set(range(1, NLINES + 1)), "partition not total"

# 2. The three in-place-rewritten ranges are archived verbatim.
for rng in [(674, 712), (1053, 1070), (1360, 1387)]:
    assert rng in ARCHIVED, f"{rng} rewritten but not archived"

# 3. Multiset identity on non-blank lines: kept + archived == original.
from collections import Counter

old_kept = []
for a, b in KEPT:
    old_kept.extend(seg(a, b))
archived_lines = []
for a, b in ARCHIVED:
    archived_lines.extend(seg(a, b))

orig_nonblank = [l for l in lines if l.strip()]
recon_nonblank = [l for l in (old_kept + archived_lines) if l.strip()]
assert Counter(orig_nonblank) == Counter(recon_nonblank), "multiset mismatch -- lossy cut"

# 4. Each rewrite asserted separately: the new text must actually be present, and the old
#    item's opening line must NOT be (it moved to the archive).
final_content = "".join(final_lines)
for probe in ["UPDATED c2809 (COMPRESSED c2892", "RE-COMPRESSED + CORRECTED c2892",
              "EXECUTED c2892 (QUALITY slot", "DONE c2892 (QUALITY/GROWTH slot"]:
    assert probe in final_content, f"rewrite missing: {probe}"
for gone in ["(the 3 files c2804 named next-up) now fully clean; 93 guarded claims",
             "**EXECUTED c2886 (QUALITY slot",
             "**Current confirmed state (re-diffed c2662, 2026-11-03)"]:
    assert gone not in final_content, f"old text still live: {gone}"

# 5. Newest-5 DONE convention (rule 6) holds exactly.
done_count = sum(1 for l in final_lines if l.startswith("- [x] "))
assert done_count == 5, f"expected 5 live DONE blocks, got {done_count}"

# 6. Independent lossless check: every non-blank original line findable in live+archive.
with open(ARCHIVE) as f:
    old_archive_content = f.read()

HEADER = "\n## Archived by cycle 2892\n\n"
new_archive_content = old_archive_content + HEADER + "".join(archived_lines)
combined = final_content + new_archive_content

missing = [l for l in orig_nonblank if l.strip() not in combined]
assert not missing, f"{len(missing)} original non-blank lines not findable post-cut"

with open(SRC, "w") as f:
    f.write(final_content)
with open(ARCHIVE, "w") as f:
    f.write(new_archive_content)

print("OK -- wrote", SRC, f"({len(final_lines)} lines), appended {len(archived_lines)} lines to", ARCHIVE)
print(f"original non-blank lines: {len(orig_nonblank)}, all found in live+archive: True")
