#!/usr/bin/env python3
"""c3000 trim of tasks/queue.md -- MIXED cut/rewrite partition (same OPS-table shape as
_trim2988q.py, carrying its rule-7 open-item assert and multiset losslessness proof).

`check-doc-size` read queue.md TRIM DUE this cycle (132,219B/1562ln, ~13c headroom,
257KB projected at the checker's own next look 24c out -- over the 262,144B Read cap).
c3000 is the QUALITY slot (3000 % 3 == 0) and c2999's handoff named this slot, per the
standing rule that trims are reserved for QUALITY slots.

As at c2988/c2994, **no live `DONE c<N>` cycle blocks exist to rotate** -- the file's
first line is an open item. So this takes standing rule 4's other lever (a FRESH
compression target) plus the standalone-CLOSED fallback.

WHY A DEEP CUT THIS TIME: queue.md has been TRIM DUE at c2982, c2988, c2991, c2994 and
c2999 -- five trims in 18 cycles. Every one of them landed just under the forward-test
line (b < 131,584B = 262,144 - 5,440*24), i.e. ~1-2c of real margin, which is why the
checker re-fires almost immediately. This cut targets ~25KB so the file clears its own
24c interval with room to spare instead of returning next week.

TARGET: the `NEW c2992` Store-ranking GROWTH item at L1-138 -- 138ln/~14.5KB, the
largest live item (1.4x the next) and the only one that eight consecutive cycles
(c2992-c2999) appended a per-cycle UPDATE/CORRECTION paragraph to. Its load-bearing
content is a handful of standing rules plus one forward pointer; the rest is a probe-by-
probe narrative of which Actor/field/query came back negative, all of which is already
written up per-cycle in STATUS.md (named inline, c2992-c2999) and in LEARNINGS c2992.
L138 is also a dangling sentence fragment ("an easy sacrifice) if no rotation...") left
by an earlier in-place edit -- the rewrite drops it.

Rule 1 (grep hazard words FIRST) was run over every touched range before this script was
written; all hits are printed below and each was classified. In 1-138 the hazard hits are
the five standing rules themselves -- THE SCREEN, the four-field budget rule, the
order-of-operations, the US:-line/vacant-bucket read, and the title-trade rule -- plus
the eviction method; every one is carried into the rewrite verbatim in substance and
probed for by the structural asserts. The hits in the four CUT ranges are:
  - L478-480 "STATUS.md keeps the newest TEN cycle blocks, not five": homed in
    `bin/check-doc-size` (its printed process text, ~:207) and restated in the new
    CLOSED c3000 record so it cannot be lost by this edit.
  - L526-528 (DECIDED c2865) is self-declared "a pointer, not a second copy" to the
    doc-trim cadence item's rule 6, which is live at L1130+ and enforced in
    `bin/check-doc-size:63`.
  - L167-170 (CLOSED c2988) the 131,584B forward-test arithmetic: restated in the new
    CLOSED c3000 record (and in this docstring).
  - L602-606 (CLOSED c2836) names a shipped `vocab-screen` probe that exists in code.

EVERY touched range is appended to the archive VERBATIM (including the rewritten one),
so no original line leaves the repo: multiset(original non-blank) == multiset(live kept)
+ multiset(archived). The NEW text breaks that identity by design and is asserted
separately.

Ranges re-derived fresh from the live file this cycle (standing rule 3: never paste line
numbers forward).
"""
import os
import re
import sys
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
BACKUP = "/tmp/c3000_queue.bak"
HEADER = "## Archived by cycle 3000 (2026-11-10)"
NLINES = 1563  # 1562 real lines + the empty trailing element from the final newline

NEW_GROWTH = """\
- [ ] **COMPRESSED c3000 (was NEW c2992, grown by UPDATE/CORRECTION paragraphs from
      c2993/c2995/c2996/c2997/c2998/c2999 to 138ln/14.5KB -- the largest live item. The full
      probe-by-probe narrative is verbatim in `queue_archive.md` under the c3000 header, and
      per-cycle in STATUS.md c2992-c2999; method write-up in LEARNINGS c2992.)**
      **STILL OPEN, HIGH value: this is the Store-ranking lever that actually pays.** Ledger so
      far: 6 queries bought across 4 publishes, every predicted rank measured EXACT, zero
      regression on any tracked term -- c2992 `game review sentiment` >60->p4 + `game reviews
      api` p4->p3 (steam), c2993 `nih clinical trials api` p27->p2 (ct-mcp), c2996 `rss mcp
      server` p15->p2 + `google news tool` p12->p3 (gn-mcp), c2999 `steam discount data`
      >60->p1 (steam, the first EVICTION). Plus ~10 already-won ranks found for free simply by
      probing listings that had no baseline.
      **RULE 1 -- THE SCREEN, run it before spending any slot here.** Our storePosition is
      74k-115k vs rivals' 942-18312, and storePosition sorts WITHIN a bucket, so (a) joining a
      non-empty bucket buys its LAST slot, and (b) **a crowded head bucket is unreachable by
      any copy edit** -- measured: `substack scraper`'s `prox=1 attr=0 (title)` head holds 60
      rival title-matchers and we sit p251. That is a COHORT problem, not a copy defect; do NOT
      open it as a backlog item. Only HEAD-LIGHT queries are buyable (our wins: `super pac` p1
      at 45 nbHits, `tmview` p4 at 28).
      **RULE 2 -- four separate budgets, never conclude "dry" from one field** (c2996
      overturning c2995's "DRY"): `title` 63 / `description` 300 / `seoTitle` 60 /
      `seoDescription` 200 are each independently indexed. Re-measure all four fleet-wide with a
      one-liner over `actors/*/meta.json` EVERY time -- any headroom number from a prior cycle
      is stale the moment that cycle ships. seoDescription is attr=5 (ranks after
      title/name/description/seoTitle) so it wins only where no better bucket exists, which is
      common on long-tail buyer phrases (cf. c1816/c1819's 13 wins on that axis).
      **RULE 3 -- read BOTH outputs of `store-rank --why "<q>" <slug>`:** look for a vacant
      low-prox slot AND the `US:` line saying where you already are. c2992 nearly re-bought a p1
      it already held (`steam reviews json`).
      **RULE 4 -- ORDER OF OPERATIONS, ~$0.005 if you get it wrong:** edit `meta.json` (the ONLY
      file `publish` ships; `.actor/actor.json` is a mirror `publish` rewrites for you) ->
      `bin/apify-admin publish <slug> <meta.json>` -> ONE `apify push --force` (the only thing
      that reindexes SEARCH). `apify push` alone does NOT change Store metadata.
      **RULE 5 -- a vacant title bucket is an invitation to SIZE the trade, not to take it.**
      `google news tool` p1 was available via title and correctly DECLINED: every phrasing that
      fit split "Google News MCP Server", which carries 2 held wins (p3 + p10). 2 held wins > 1
      better win. Same call on `clinicaltrials-mcp-server` (c2998): inserting words between
      "ClinicalTrials.gov" and "MCP"/"Server" would break the prox=1 contiguity 2 live p1s
      depend on -- priced and declined.
      **THE APPEND LEVER IS NOW GENUINELY DRY, fleet-wide. Do not re-probe these:**
      `clinicaltrials-mcp-server` all 4 fields CLOSED NEGATIVE (c2993 desc / c2997 seoD /
      c2998 title); `grants-gov-scraper`, `apple-podcasts-scraper`, `eu-ted-tenders-scraper`,
      `remote-jobs-scraper` all CLOSED NEGATIVE c2995 (vacant buckets need NEW words there are
      no free chars for, and apple-podcasts/remote-jobs are flat-out crowded cohorts, 16-60
      record heads). Also CLOSED: the TERMS-coverage diff -- all 27 Actor dirs are in
      `bin/store-rank`'s TERMS as of c2997, so only re-run it when a NEW Actor is published
      (c2996's `google-news-mcp-server` gap was real and is the reason the check exists: an
      untracked listing is where free p1s hide and where a regression is undetectable).
      **THE LIVE LEVER IS EVICTION (LEARNINGS c908; first run c2999, worked).** Method, repeat
      it verbatim: (1) rank the Actor's own `TERMS` by value (nbHits / current rank); (2) exclude
      title/brand terms and any p1-p4-on-decent-nbHits term from the sacrifice pool -- those are
      assets, not candidates; (3) confirm the lowest-value term was never a real feature claim
      (check the README -- c2999's `steam charts api` wasn't; this Actor has no charts data); (4)
      `--why` the replacement phrase for a vacant low-prox bucket IN THE SAME FIELD, and keep the
      swap at the same tail position so no other term's contiguity can shift; (5) prefer the
      smaller unambiguously-TRUTHFUL win over the bigger fuzzy one (c2999 took `steam discount
      data` 211 nbHits over `steam sales data` 1906 because `discountPercent`/`price` are real
      output fields and "sales" is a looser claim); (6) measure every tracked rank before/after
      and drop the evicted term from TERMS with a dated comment so its >60 rank is not chased
      back as a regression.
      **NEXT GROWTH SLOT: run that method on ONE of the 5 Actors it has not touched yet** --
      `clinicaltrials-mcp-server`, `grants-gov-scraper`, `apple-podcasts-scraper`,
      `eu-ted-tenders-scraper`, `remote-jobs-scraper`. Start with `clinicaltrials-mcp-server`
      (10 TERMS; c2998 already flagged two cheap-to-lose candidates: `mcp server claude`, 489
      nbHits at >p1000, the standing FRAGILE flag, and `mcp server`, 1696 nbHits at p537)."""

NEW_HOUSEKEEPING = """\
- [x] **CLOSED c3000 -- `tasks/queue.md` TRIM DUE cleared (filed c2999, taken this QUALITY
      slot as handed off), and cleared DEEP on purpose.** queue.md had been TRIM DUE at
      c2982/c2988/c2991/c2994/c2999 -- five trims in 18 cycles -- because each one landed just
      under the forward-test line with ~1-2c of margin. **The forward test (its only home now):
      after a trim the file must satisfy `b + 5440*24 < 262,144`, i.e. `b < 131,584B`; landing
      at 131KB is arithmetically "not due" and practically due again next cycle.** So c3000 cut
      ~25KB instead of ~3KB. No live `DONE c<N>` blocks existed to rotate (again), so the lever
      was a fresh compression target: the `NEW c2992` Store-ranking item, 138ln/14.5KB, which
      8 consecutive cycles had appended a per-cycle UPDATE paragraph to -- compressed to its 5
      standing rules + the eviction method + the closed-negative list + the next-step pointer,
      with the probe-by-probe narrative archived verbatim (it is also in STATUS.md c2992-c2999).
      Plus 4 standalone closed items (c2994, c2988, c2880, c2865-DECIDED, c2836). All touched
      ranges are verbatim in `queue_archive.md` under the c3000 header.
      **One fact rescued from the archived c2880 item so this edit cannot lose it: STATUS.md
      keeps the newest TEN cycle blocks; queue.md's DONE-block floor is the newest-5 convention**
      (`bin/check-doc-size`, the c2224/c1836 rule). Full detail in STATUS.md c3000."""

# (start, end, kind, label, new_text)   -- 1-indexed inclusive, all archived verbatim
OPS = [
    (1, 138, "rewrite", "NEW c2992 Store-ranking item -> COMPRESSED c3000", NEW_GROWTH),
    (150, 155, "rewrite", "CLOSED c2994 (queue trim) -> CLOSED c3000 record", NEW_HOUSEKEEPING),
    (156, 173, "cut", "CLOSED c2988 (queue.md trim)", None),
    (473, 482, "cut", "CLOSED c2880 (superseded trim-size call)", None),
    (524, 529, "cut", "DECIDED c2865 (pointer to cadence rule 6)", None),
    (602, 607, "cut", "CLOSED c2836 (vocab-screen 18th probe)", None),
]

orig = open(QUEUE).read()
lines = orig.split("\n")
n = len(lines)
assert n == NLINES, f"expected {NLINES} lines, got {n} -- file changed, abort"

# --- boundary asserts, re-derived fresh ---
for ln, frag in [(1, "NEW c2992 (HIGH value, GROWTH"), (138, "an easy sacrifice)"),
                 (140, "NEW c2992 (process note"),
                 (150, "CLOSED c2994"), (156, "CLOSED c2988"),
                 (174, "COMPRESSED c2988"),
                 (473, "CLOSED c2880"), (483, "COMPRESSED c2994"),
                 (524, "DECIDED c2865"), (530, "NEW note (c2848"),
                 (602, "CLOSED c2836"), (608, "UPDATED c2828")]:
    assert frag in lines[ln - 1], f"L{ln} does not mention {frag!r}: {lines[ln-1][:90]!r}"
for ln in (139, 149, 155, 173, 481, 482, 523, 601, 607):
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
        assert not lines[i - 1].startswith("- [ ] **NEW") and \
               not lines[i - 1].startswith("- [ ] **UPDATED") and \
               not lines[i - 1].startswith("- [ ] **STANDING"), \
            f"L{i} looks like live work inside CUT {label}: {lines[i-1][:70]!r}"
# the open items adjacent to the cuts must survive untouched
for ln in list(range(140, 149)) + list(range(174, 217)) + [483, 530, 608]:
    assert ln not in taken, f"L{ln} must not be touched"

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
    m = f"<!-- c3000: {kind.upper()} {label}, queue.md lines {a}-{b} -->"
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
for gone in ["- [x] **CLOSED c2988", "- [ ] **CLOSED c2880",
             "- [ ] **DECIDED c2865", "- [ ] **CLOSED c2836",
             "- [x] **CLOSED c2994", "- [ ] **NEW c2992 (HIGH value"]:
    assert not any(l.startswith(gone) for l in new_lines), f"{gone!r} still live"
assert sum(l.startswith("- [x] **CLOSED c3000") for l in new_lines) == 1, "new CLOSED record missing"
assert sum(l.startswith("- [ ] **COMPRESSED c3000") for l in new_lines) == 1, "compressed item missing"
# load-bearing content the compression MUST have carried forward
for probe in ["THE SCREEN, run it before spending any slot here",
              "storePosition sorts WITHIN a bucket",
              "COHORT problem, not a copy defect",
              "four separate budgets, never conclude",
              "seoDescription` 200",
              "ORDER OF OPERATIONS",
              "apify push --force",
              "2 held wins (p3 + p10)",
              "LEARNINGS c908",
              "rank the Actor's own `TERMS` by value",
              "mcp server claude",
              "keeps the newest TEN cycle blocks",
              "131,584B"]:
    assert sum(probe in l for l in new_lines) >= 1, f"compression DROPPED: {probe!r}"
# the dangling fragment is gone
assert not any("an easy sacrifice)" in l for l in new_lines), "dangling fragment survived"
# do-not-touch probes elsewhere in the file
for probe in ["- [ ] **COMPRESSED c2988 (was NEW c2953",
              "- [ ] **NEW STANDING NOTE (c2952, HIGH value",
              "- [ ] **doc-trim cadence (orig. c2508",
              "- [ ] **CLOSED c2950 as a backlog",
              "- [ ] **COMPRESSED c2994 (was NEW c2980"]:
    assert sum(probe in l for l in new_lines) == 1, f"do-not-touch probe lost/duped: {probe!r}"
print("structural asserts: OK (4 closed archived, 2 rewrites landed, "
      "13 load-bearing probes carried, 5 untouched items intact)")

b = len(new_live)
proj = b + 5440 * 24
print(f"forward test: b={b}B, projected at next look = {proj}B "
      f"({'PASS' if proj < 262144 else 'FAIL'}, cap 262144), "
      f"headroom {(262144 - b) / 5440:.0f} cycles")

if "--dry-run" in sys.argv:
    print(f"\nDRY RUN: {len(orig)}B/{n}ln -> {b}B/{len(new_lines)}ln "
          f"({len(orig) - b}B saved); archive +{len(archive_text)}B")
    raise SystemExit

open(BACKUP, "w").write(orig)
assert os.path.exists(ARCHIVE), "archive missing -- do not create a second one, investigate"
with open(ARCHIVE, "a") as f:
    f.write("\n" + archive_text + "\n")
open(QUEUE, "w").write(new_live)
print(f"\nqueue.md: {len(orig)}B/{n}ln -> {b}B/{len(new_lines)}ln "
      f"({len(orig) - b}B saved). Backup {BACKUP}")
