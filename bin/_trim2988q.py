#!/usr/bin/env python3
"""c2988 trim of tasks/queue.md -- a MIXED cut/rewrite partition (clone of _trim2940q.py's
OPS-table shape, carrying _trim2948q.py's rule-7 open-item assert).

`check-doc-size` read queue.md TRIM DUE this cycle (133,493B/1583ln, ~13c headroom,
258KB projected at the checker's own next look 24c out). 2988 is the QUALITY slot
(2988 % 3 == 0) and c2987's handoff named this slot for the trim, per standing rule 2.

The usual lever is unavailable: **no live `DONE c<N>` cycle blocks exist to rotate**
(c2982/c2986 already archived them all). Only 3 standalone `- [x]` CLOSED items are
live, worth ~2.4KB -- not enough, since the forward-looking test (`projected = b +
rate*gap >= READ_CAP`, cycle 1860/2220) needs b < 131,584B (262,144 - 5,440*24) and a
2.4KB cut lands at ~131.1KB, i.e. instantly TRIM DUE again. So this trim also takes
standing rule 4's other documented lever -- "finding a NEW compression target by
scanning for genuinely superseded/duplicate content fresh".

That target is the `NEW c2953 backlog` item at L30-182: the largest live item
(12,583B/153ln, 1.4x the next), which **self-declares "FULLY CLOSED c2976 -- no work
left in this item. It stays live ONLY for the standing lessons and standing holds at
the bottom"** while still carrying ~120 lines of superseded per-file closure narrative
(c2954-c2977 build numbers and byte counts). Compressed to its load-bearing content.

Rule 1 (grep FIRST) was run on every touched range before this script was written.
17 hazard hits in 30-182, all classified and all retained in the rewrite:
  - the 2 surviving DELIBERATE STANDING HOLDS (apple-podcasts-scraper:222) -- kept
  - the `majestic_fund` 71v79 hold being DEAD (c2976 retired it) -- kept as an
    explicit "do not re-apply" guard, since 6 of the 17 hits reference that hold
  - the 3 standing lessons (c2952 DISAGREE-phantom, c2976 claim-count denominator,
    c2960 UNDATED-three-shapes) -- kept, each verified to ALSO have a full write-up
    in notes/LEARNINGS.md (lines ~7044, ~7157, ~7034 respectively) before compressing
  - `USER_TOLERANCE = 0.10` -- also homed in the `CLOSED c2950` item's lesson (i)
1 hazard hit in 12-22 (c2986's "standing cycle-1836 process ... newest 10 cycle
blocks"): narrative ABOUT a cadence homed in `bin/check-doc-size:167` and in the
doc-trim cadence item's rule 6. 0 hits in 23-29 and 217-224.

EVERY touched range is appended to the archive VERBATIM (including the two rewritten
ones), so no original line leaves the repo and losslessness is exact: multiset of
original non-blank lines == multiset(live kept) + multiset(archived). The two blocks of
NEW text break that identity by design and are asserted separately.

Ranges re-derived fresh from the live file this cycle (standing rule 3, never paste
line numbers forward).
"""
import os
import re
import sys
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
BACKUP = "/tmp/c2988_queue.bak"
HEADER = "## Archived by cycle 2988 (2026-11-10)"
NLINES = 1584  # 1583 real lines + the empty trailing element from the final newline

NEW_HOUSEKEEPING = """\
- [x] **CLOSED c2988 -- `tasks/queue.md` TRIM DUE cleared (filed c2987, taken this QUALITY
      slot as handed off).** No live `DONE c<N>` cycle blocks existed to rotate, and the
      c2982 standalone-CLOSED fallback was only worth ~2.4KB on its own (which lands at
      ~131.1KB, still TRIM DUE), so this trim also took standing rule 4's other lever: a
      FRESH compression target. The `NEW c2953 backlog` item -- largest live item,
      12.6KB/153ln, self-declared "FULLY CLOSED c2976 -- no work left" -- was carrying
      ~120 lines of superseded per-file closure narrative; compressed to its 2 standing
      holds + 3 standing lessons (each verified to have a full LEARNINGS home first).
      Plus the 3 standalone `- [x]` items (c2986/c2982/c2983). All 5 touched ranges are
      verbatim in `queue_archive.md` under the c2988 header, so nothing left the repo.
      130.4KB/1583ln -> SIZE_PLACEHOLDER. Full detail in STATUS.md."""

NEW_C2953 = """\
- [ ] **COMPRESSED c2988 (was NEW c2953, REWRITTEN c2958 / re-REWRITTEN c2964 -- 153ln/12.6KB,
      the largest live item and self-declared FULLY CLOSED at c2976. The whole per-file
      closure narrative, c2954-c2977, is verbatim in `queue_archive.md` under the c2988
      header; earlier per-handle history is under the c2958/c2964 headers.)**
      **BACKLOG FULLY CLOSED c2976 -- zero work left. Do NOT re-open it or re-grind its
      file list:** the fleet cross-paragraph-disagreement sweep (orig. 22 stale / 12
      disagree / 16 undated) ended at 4 stale / 10 disagree / 0 undated, and every
      remaining flag is either a standing hold or a confirmed phantom (both below).
      Fresh drift found after c2976 is filed as its own item, never back into this one.
      **The 2 surviving DELIBERATE STANDING HOLDS (not work; they will be re-flagged by
      every future sweep -- do not "fix" them):** `apple-podcasts-scraper`:222's
      `tidydata/audio-video-transcription` 20v27 and `sourabhbgp` 71v83. Both sit inside
      dated past-tense sweep records, so LEARNINGS c2856 lesson 1 applies -- a count in a
      dated measurement is not a claim about today, and editing it falsifies the record.
      **`scholarship-scraper`'s `majestic_fund` 71v79 hold is DEAD -- do not re-apply it.**
      c2976 RETIRED it rather than holding it, rewriting :107 into the c2971 "N as of
      DATE, was M at the <sweep> sweep" convention, which closed the STALE *and* a
      3-cycle-old :107-vs-:115 DISAGREE in one edit without falsifying the record.
      **All 10 remaining DISAGREE are known phantoms:** apple-podcasts(3) + google-play(7).
      **3 standing lessons survive this backlog. Each has its full write-up in LEARNINGS,
      so this is the short form:**
      (a) **DISAGREE is presumed-phantom-until-disproven** (c2952, re-confirmed c2957 and
      c2964 -- 3-for-3 across every cluster this backlog investigated). Before fixing one,
      check whether each paragraph carries its OWN date and the values are in date order;
      if so it is a correct growth record, not a bug. Budget it as a read, not a fix.
      (LEARNINGS c2964, ~line 7044.)
      (b) **After ANY competitor-count edit, diff the checker's "N claim(s) checked" total
      against the pre-edit run, not just its stale count -- a DROP means you deleted a
      claim from coverage, not that you fixed it.** `check-competitor-claims:287`'s `USERS`
      regex only matches a count reached from the backticked handle via `at|with|has|still`,
      a bare `(`, or an `N -> M` arrow chain, so a reworded "had only" silently drops the
      claim and reports a clean 0 stale that is really a blind spot. Use c2967's arrow
      shape. (LEARNINGS c2976, ~line 7157.)
      (c) **An UNDATED flag has THREE shapes and only one is real work:** (i) genuinely
      unverified -- go verify; (ii) the WORDING GAP -- a real in-window date the regex
      cannot see because the preceding word is "audit"/"sweep" rather than
      `verified|checked|re-verified|rechecked`, so reword in place; (iii) the CONTINUATION
      PARAGRAPH -- a long sweep section states its date in its opening block and the
      flagged block is a later part of that same section, so restate the section's date
      inside the continuation block. ALWAYS read the enclosing section before calling
      anything unverified, and do NOT merge the paragraphs or loosen the regex (an
      any-nearby-date rule would read every paragraph quoting a rival's filing date as
      verified). (LEARNINGS c2960, ~line 7034.)"""

# (start, end, kind, label, new_text)   -- 1-indexed inclusive, all archived verbatim
OPS = [
    (1, 10, "rewrite", "c2987 housekeeping item -> CLOSED c2988 record", NEW_HOUSEKEEPING),
    (12, 22, "cut", "CLOSED c2986 (STATUS.md trim)", None),
    (23, 29, "cut", "CLOSED c2982 (queue.md trim)", None),
    (30, 182, "rewrite", "NEW c2953 backlog -> COMPRESSED c2988", NEW_C2953),
    (217, 224, "cut", "CLOSED c2983 (devto-comments fix)", None),
]

orig = open(QUEUE).read()
lines = orig.split("\n")
n = len(lines)
assert n == NLINES, f"expected {NLINES} lines, got {n} -- file changed, abort"

# --- boundary asserts, re-derived fresh ---
for ln, frag in [(1, "NEW HOUSEKEEPING (c2987)"), (10, "per standing convention"),
                 (12, "CLOSED c2986"), (23, "CLOSED c2982"),
                 (30, "NEW c2953 backlog"), (182, "budget it as a read, not a fix"),
                 (183, "NEW STANDING NOTE (c2952"), (217, "CLOSED c2983"),
                 (225, "UPDATED c2937")]:
    assert frag in lines[ln - 1], f"L{ln} does not mention {frag!r}: {lines[ln-1][:90]!r}"
for ln in (11, 22, 29, 216, 224):
    assert lines[ln - 1].strip() == "", f"L{ln} expected blank, got {lines[ln-1][:60]!r}"

taken = {}
for a, b, kind, label, _new in OPS:
    assert lines[a - 1].startswith("- ["), f"L{a} is not an item head: {lines[a-1][:60]!r}"
    for i in range(a, b + 1):
        assert i not in taken, f"overlap at L{i}: {label} vs {taken[i]}"
        taken[i] = label
# rule 7: no OPEN item may be swallowed by a CUT range (rewrites replace their own head)
for a, b, kind, label, _new in OPS:
    if kind != "cut":
        continue
    for i in range(a, b + 1):
        assert not lines[i - 1].startswith("- [ ] "), \
            f"L{i} is an OPEN item inside CUT {label} -- refusing to archive live work: {lines[i-1][:70]!r}"
# the one OPEN item nested among the cuts must survive untouched
for ln in range(183, 216):
    assert ln not in taken, f"L{ln} (NEW STANDING NOTE c2952) must not be touched"

# --- rule 1 hazard grep, every hit printed ---
hazard = re.compile(r"standing|cadence|always |never |do not |must |\brule\b", re.I)
total_hits = 0
for a, b, kind, label, _new in OPS:
    hits = [(i, lines[i - 1]) for i in range(a, b + 1) if hazard.search(lines[i - 1])]
    total_hits += len(hits)
    print(f"rule-1 hazard grep -- {label} ({a}-{b}, {kind}): {len(hits)} hit(s)")
    for i, l in hits:
        print(f"  L{i}: {l.strip()[:140]}")
print(f"total hazard hits: {total_hits}\n")

# --- build archive (ALL touched ranges, verbatim) and new live file ---
chunks, markers = [], []
for a, b, kind, label, _new in OPS:
    m = f"<!-- c2988: {kind.upper()} {label}, queue.md lines {a}-{b} -->"
    markers.append(m)
    chunks.append(m)
    chunks.extend(lines[a - 1:b])
    chunks.append("")
archive_text = "\n".join([HEADER, ""] + chunks)

new_by_start = {a: new for a, b, kind, label, new in OPS if kind == "rewrite"}
out = []
for i, l in enumerate(lines, 1):
    if i in new_by_start:
        out.extend(new_by_start[i].split("\n"))
    if i not in taken:
        out.append(l)
new_live = "\n".join(out)

# --- losslessness: pure multiset identity, new text accounted for separately ---
def nb(text):
    return Counter(l for l in text.split("\n") if l.strip())

new_text_lines = nb("\n".join(new_by_start.values()))
got = (nb(new_live) + nb(archive_text)
       - nb(HEADER) - nb("\n".join(markers)) - new_text_lines)
missing, extra = nb(orig) - got, got - nb(orig)
assert not missing, f"LINES LOST: {list(missing)[:5]}"
assert not extra, f"UNEXPLAINED LINES: {list(extra)[:5]}"
print("lossless check: OK (every original non-blank line is in live+archive; "
      "new rewrite text asserted separately)")

# --- structural asserts on the result ---
new_lines = new_live.split("\n")
assert not any(l.startswith("- [x] **CLOSED c2986") for l in new_lines), "c2986 not archived"
assert not any(l.startswith("- [x] **CLOSED c2982") for l in new_lines), "c2982 not archived"
assert not any(l.startswith("- [x] **CLOSED c2983") for l in new_lines), "c2983 not archived"
# head-prefix checks, not substring: the new text legitimately CITES both old headings
assert not any(l.startswith("- [ ] **NEW c2953 backlog") for l in new_lines), "c2953 head still live"
assert not any(l.startswith("- [ ] **NEW HOUSEKEEPING (c2987)") for l in new_lines), "c2987 head still live"
assert sum(l.startswith("- [x] **CLOSED c2988") for l in new_lines) == 1, "new CLOSED record missing"
assert sum(l.startswith("- [ ] **COMPRESSED c2988") for l in new_lines) == 1, "compressed item missing"
# load-bearing content the compression MUST have carried forward
for probe in ["tidydata/audio-video-transcription` 20v27",
              "hold is DEAD -- do not re-apply it",
              'N claim(s) checked" total',
              "presumed-phantom-until-disproven",
              "CONTINUATION",
              "LEARNINGS c2856 lesson 1 applies"]:
    assert sum(probe in l for l in new_lines) >= 1, f"compression DROPPED: {probe!r}"
# do-not-touch probes elsewhere in the file
for probe in ["- [ ] **NEW STANDING NOTE (c2952, HIGH value",
              "- [ ] **doc-trim cadence (orig. c2508",
              "- [ ] **CLOSED c2950 as a backlog",
              "- [ ] **NEW c2980 (MEDIUM"]:
    assert sum(probe in l for l in new_lines) == 1, f"do-not-touch probe lost/duped: {probe!r}"
print("structural asserts: OK (3 CLOSED archived, 2 rewrites landed, "
      "6 load-bearing probes carried, 4 untouched items intact)")

if "--dry-run" in sys.argv:
    print(f"\nDRY RUN: {len(orig)}B/{n}ln -> {len(new_live)}B/{len(new_lines)}ln "
          f"({len(orig) - len(new_live)}B saved); archive +{len(archive_text)}B")
    raise SystemExit

open(BACKUP, "w").write(orig)
assert os.path.exists(ARCHIVE), "archive missing -- do not create a second one, investigate"
with open(ARCHIVE, "a") as f:
    f.write("\n" + archive_text + "\n")
open(QUEUE, "w").write(new_live)
print(f"\nqueue.md: {len(orig)}B/{n}ln -> {len(new_live)}B/{len(new_lines)}ln "
      f"({len(orig) - len(new_live)}B saved). Backup {BACKUP}")
