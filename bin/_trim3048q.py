#!/usr/bin/env python3
"""c3048 trim of tasks/queue.md -- newest-5-floor rotation + ONE in-place rewrite.

check-doc-size left queue.md TRIM DUE at c3046 (143.6KB then, 149.6KB now) and named THIS
QUALITY slot as the owed handoff (doc-trim STANDING RULE 2: trim only in a QUALITY slot,
and do not let a second one pass it).

7 cycle-level `CLOSED cNNNN` blocks were live; this keeps the newest 5 (c3046, c3045,
c3044, c3043, c3042) and archives c3041 + c3040 verbatim, matching STATUS.md's convention.
Also archives the `CLOSED c3040 (sentinel sub-question)` pointer item, which c3047 already
marked superseded by the live `NEW c3047` item directly below it -- same precedent as
c3045 archiving the spent `RESOLVED c3037` pointer.

Ranges re-derived fresh from the live file this cycle (rule 3, never paste forward).
Rule 7 is ADAPTED, not dropped: these cycle blocks head with `- [ ] **CLOSED`, not
`- [x] **DONE`, so "no `- [ ] ` line in the cut" would be vacuously impossible. The
equivalent assert here is that each cut range contains EXACTLY ONE `- [ ] ` line and it
is the expected CLOSED head -- i.e. no extra live item rode along in the range.

One rewrite (L911): the doc-trim item's newest-execution-only paragraph, EXECUTED c3045
-> EXECUTED c3048. Old text archived verbatim under its own header, per that item's
"method + standing rules + newest execution only" shape.
"""
import os
import re
import sys
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
BACKUP = "/tmp/c3048_queue.bak"
HEADER = "## Archived by cycle 3048 (2026-11-11)"
NLINES = 1352  # 1351 real lines + the empty trailing element from the final newline

# THREE ranges, not one span: each block is a single long line followed by a blank, and
# the live `NEW c3047` item sits immediately after the third range at L21 -- it must stay.
CUTS = [(15, 16, "CUT CLOSED c3041"),
        (17, 18, "CUT CLOSED c3040"),
        (19, 20, "CUT CLOSED c3040 sentinel-sub-question pointer (superseded by NEW c3047)")]

REWRITE_LN = 911
NEW_EXEC = (
    "      **EXECUTED c3048 (QUALITY slot; owed since c3046's due `check-doc-size` left queue.md "
    "TRIM DUE at 143.6KB and named this slot). Standard newest-5-floor rotation on queue.md only** "
    "-- archived `CLOSED c3041` + `CLOSED c3040` and the spent `CLOSED c3040 (sentinel sub-question)` "
    "pointer item verbatim to `queue_archive.md` under `## Archived by cycle 3048` (floor restored to "
    "5: c3046/c3045/c3044/c3043/c3042); pre-edit 153,232B/1352ln. Durability check before archiving "
    "(the c3024 trap -- content, not label): `grep -c 3041 bin/store-rank` == 1, so c3041's 11 TERMS "
    "wins are durably homed; c3040's three shipped fixes re-verified still present in "
    "`actors/google-news-scraper/src/main.js`, `site/content/blog/google-news-rss-public-feeds-no-key.md` "
    "and `state/devto_syndicated.json`. **The c2588 only-home hazard grep earned its keep for the first "
    "time in six trims:** the pointer item was the referent of a LIVE SOURCE COMMENT -- "
    "`main.js:176` read \"NOT DONE, deliberately (see tasks/queue.md, cycle 3040) ... needs the PLAYBOOK "
    "two-cycle measurement before shipping\", which archiving would have left dangling AND which was "
    "ALREADY FALSE (c3047 ran that sweep and closed it negative). Rewrote that comment in place first "
    "-- it now carries c3047's negative result, an explicit do-not-re-open, and a pointer to the live "
    "`NEW c3047` item ($0, no build, `node --check` clean). **Lesson for the next trim: the hazard grep "
    "must cover CODE that cites the queue, not just prose inside the block being cut.**"
)

orig = open(QUEUE).read()
lines = orig.split("\n")
n = len(lines)
assert n == NLINES, f"expected {NLINES} lines, got {n} -- file changed, abort"

# boundary sanity
assert lines[13].strip() == "", "L14 should be the blank before the c3041 block"
for ln, frag in [(15, "CLOSED c3041"), (17, "CLOSED c3040 --"), (19, "CLOSED c3040 (the")]:
    head = lines[ln - 1]
    assert head.startswith("- [ ] **CLOSED c"), f"L{ln} is not a CLOSED head: {head[:60]!r}"
    assert frag in head, f"L{ln} does not mention {frag!r}: {head[:90]!r}"

taken = {}
for a, b, label in CUTS:
    assert lines[b - 1].strip() == "", f"L{b} should be the blank closing {label}"
    opens = [i for i in range(a, b + 1) if lines[i - 1].startswith("- [ ] ")]
    # rule 7, adapted: exactly ONE live-item line per range, and it is this block's head
    assert opens == [a], f"{label}: expected the only `- [ ] ` line at L{a}, got {opens}"
    for i in range(a, b + 1):
        assert i not in taken, f"overlap at L{i}: {label} vs {taken[i]}"
        taken[i] = label

assert lines[20].startswith("- [ ] **NEW c3047"), \
    f"L21 must remain live (the item the pointer defers to): {lines[20][:60]!r}"
assert REWRITE_LN not in taken, "rewrite line must not also be cut"
old_exec = lines[REWRITE_LN - 1]
assert old_exec.startswith("      **EXECUTED c3045 (QUALITY slot"), \
    f"L{REWRITE_LN} is not the EXECUTED paragraph: {old_exec[:70]!r}"

# rule 1: hazard grep EVERY archive-bound range, print every hit
hazard = re.compile(r"standing|cadence|always |never |do not |must |\brule\b", re.I)
chunks, total_hits = [], 0
for a, b, label in CUTS:
    hits = [(i, lines[i - 1]) for i in range(a, b + 1) if hazard.search(lines[i - 1])]
    total_hits += len(hits)
    print(f"rule-1 hazard grep -- {label} ({a}-{b}): {len(hits)} hit(s)")
    for i, l in hits:
        print(f"  L{i}: {l.strip()[:200]}")
    chunks.append(f"<!-- c3048: {label}, queue.md lines {a}-{b} -->")
    chunks.extend(lines[a - 1:b])
    chunks.append("")
print(f"total hazard hits: {total_hits}")

# the replaced paragraph is archived verbatim too, under its own marker
chunks.append("<!-- c3048: REPLACED doc-trim-cadence execution record (was EXECUTED c3045, "
              f"queue.md line {REWRITE_LN}) -->")
chunks.append(old_exec)
chunks.append("")

markers = [c for c in chunks if c.startswith("<!-- c3048: ")]
archive_text = "\n".join([HEADER, ""] + chunks)

new_lines_list = []
for i, l in enumerate(lines, 1):
    if i in taken:
        continue
    new_lines_list.append(NEW_EXEC if i == REWRITE_LN else l)
new_live = "\n".join(new_lines_list)


def nb(text):
    return Counter(l for l in text.split("\n") if l.strip())


# multiset identity, accounting for the one rewrite (new text added, old text moved to archive)
got = nb(new_live) + nb(archive_text) - nb(HEADER) - nb("\n".join(markers)) - nb(NEW_EXEC)
missing, extra = nb(orig) - got, got - nb(orig)
assert not missing, f"LINES LOST: {[m[:90] for m in list(missing)[:5]]}"
assert not extra, f"UNEXPLAINED LINES: {[e[:90] for e in list(extra)[:5]]}"
print("lossless check: OK (multiset identity over live+archive, modulo the asserted rewrite)")
assert new_live.count(NEW_EXEC) == 1, "new EXECUTED paragraph not placed exactly once"
assert old_exec not in new_live, "old EXECUTED paragraph still live"
assert old_exec in archive_text, "old EXECUTED paragraph not archived"
print("rewrite asserts: OK (old text archived verbatim, new text placed once)")

new_lines = new_live.split("\n")
heads = [l for l in new_lines if l.startswith("- [ ] **CLOSED c30")]
assert len(heads) == 5, f"expected 5 cycle-level CLOSED blocks live, got {len(heads)}"
for frag in ["c3046", "c3045", "c3044", "c3043", "c3042"]:
    assert sum(f"**CLOSED {frag}" in h for h in heads) == 1, f"{frag} CLOSED block went missing"
assert sum(l.startswith("- [ ] **NEW c3047") for l in new_lines) == 1, "NEW c3047 lost"
# item-count delta: 3 items archived, none added by this script
before_items = sum(l.startswith("- [ ] ") or l.startswith("- [x] ") for l in lines)
after_items = sum(l.startswith("- [ ] ") or l.startswith("- [x] ") for l in new_lines)
assert before_items - after_items == 3, f"item delta {before_items - after_items}, expected 3"
for probe in ["**STANDING RULES -- the first six were rescued",
              "1. **Grep FIRST, then cut.**",
              "6. **DONE blocks are capped in LENGTH, not count",
              "stop re-reading it each QUALITY slot"]:
    assert sum(probe in l for l in new_lines) == 1, f"do-not-archive probe lost/duped: {probe!r}"
print(f"structural asserts: OK (5 CLOSED blocks live, items {before_items} -> {after_items}, "
      "do-not-archive section intact)")

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
