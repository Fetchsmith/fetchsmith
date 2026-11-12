#!/usr/bin/env python3
"""c3072 trim of tasks/queue.md -- newest-5-floor rotation + three asserted rewrites.

check-doc-size this cycle: tasks/queue.md TRIM DUE at 158.2KB/1375ln (~8c headroom at
+5440 B/cycle), and c3071 named THIS QUALITY slot (3072 % 3 == 0) for it -- doc-trim
STANDING RULE 2 (trim only in a QUALITY slot, and do not let a second one pass it).

Exactly 5 cycle-level `CLOSED cNNNN` blocks are live (c3071, c3069, c3068, c3063, c3061),
i.e. the file is already AT the newest-5 floor before this cycle's own block is prepended.
Archiving the single oldest (`CLOSED c3061`) now leaves 4 live, and c3072's own block --
written later this cycle -- restores the floor to exactly 5. Ranges re-derived fresh from
the live file (rule 3, never paste forward).

Rule 7 is ADAPTED as in bin/_trim3048q.py: cycle blocks head with `- [ ] **CLOSED`, not
`- [x] **DONE`, so "no `- [ ] ` line in the cut" is vacuously impossible; the equivalent
assert is that the cut range holds EXACTLY ONE `- [ ] ` line and it is the expected
CLOSED head, so no live item rode along.

Durability (the c3024 trap -- content, not label): `CLOSED c3061`'s substance is the 20
keepers it shipped for `trademark-search-scraper`, which live in `bin/store-rank`'s TERMS
dict (33 terms on that Actor, line 1599), not in this block; and its one carry-forward
lesson (all 6 high-nbHits candidates matched the batch tool byte-identical, no false
positives) is already paraphrased inline in the surviving `NEW c3056` item.

Rule-1 hazard grep found TWO live dangling pointers that archiving would break, both
fixed here in place as surgical substring rewrites (the old fragments are archived with
context, and each rewritten pointer resolves standalone):
  * L17 `NEW c3056` said "see `CLOSED c3061` below" -- re-aimed at the archive header;
    the load-bearing fact is already inlined in the same sentence.
  * L12 `CLOSED c3063` said `CLOSED c3053`'s numbers are homed in "`state/STATUS.md`'s
    own c3053 block" -- TRUE until this cycle, but bin/_trim3072s.py's keep-newest-10
    STATUS.md cut (run first, same cycle) moved the c3053 block to STATUS_ARCHIVE.md.
    Re-aimed there. This is the c3060 lesson (hazard-grep queue.md itself) compounding
    with a same-cycle sibling trim: a pointer can be made stale by the OTHER doc's trim.

Plus the one whole-line rewrite every trim owes the doc-trim item: its
newest-execution-only paragraph, EXECUTED c3069 -> EXECUTED c3072 (old line archived
verbatim under its own marker).
"""
import os
import re
import sys
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
BACKUP = "/tmp/c3072_queue.bak"
HEADER = "## Archived by cycle 3072 (2026-11-12)"
NLINES = 1376  # 1375 real lines + the empty trailing element from the final newline

CUTS = [(14, 15, "CUT CLOSED c3061 (+ its trailing blank)")]

# surgical substring rewrites on lines that STAY live
SUBS = [
    (17, "see `CLOSED c3061` below",
     "see `queue_archive.md`'s `## Archived by cycle 3072` block"),
    (12, "`state/STATUS.md`'s own c3053 block",
     "`state/STATUS_ARCHIVE.md`'s c3053 block (moved out of the live STATUS.md by this "
     "cycle's keep-newest-10 trim, under `## Archived by cycle 3072`)"),
]

REWRITE_LN = 915
NEW_EXEC = (
    "      **EXECUTED c3072 (QUALITY slot, 3072 % 3 == 0; prior `EXECUTED c3069` text archived "
    "verbatim under `## Archived by cycle 3072` in `queue_archive.md`). BOTH docs trimmed this "
    "slot -- queue.md newest-5-floor rotation AND STATUS.md's keep-newest-10 cut, the first "
    "since c3051.** `check-doc-size`: queue.md TRIM DUE at 158.2KB/1375ln (~8c headroom), "
    "STATUS.md TRIM SOON at 129.4KB/368ln (~16c headroom but a 235KB projection at the "
    "checker's own 24c next look, i.e. guaranteed DUE before it is read again -- the "
    "trim-proactively-in-a-QUALITY-slot case), LEARNINGS.md OK (6928/8000 lines, ~54c). "
    "**queue.md:** exactly 5 live cycle blocks, i.e. already AT the floor pre-cycle, so "
    "archived only the oldest (`CLOSED c3061`) -- 4 live after the cut, back to 5 once c3072's "
    "own block is prepended. Durability first (c3024 trap): c3061's 20 keepers are live in "
    "`bin/store-rank`'s TERMS (33 terms on `trademark-search-scraper`) and its batch-reliability "
    "lesson is already inlined in `NEW c3056`. **STATUS.md:** 31 live blocks -> keep-newest-10 "
    "(c3071..c3062), archived c3061..c3041 verbatim; 132,467B/368ln -> 40,659B/112ln, 91.8KB "
    "saved, OK on the next reading with ~20c of real headroom instead of ~16c of projected "
    "deficit. Two self-verifying one-shots kept on disk (`bin/_trim3072s.py` pure cut with exact "
    "multiset identity, `bin/_trim3072q.py` cut + rewrites), both dry-run before writing. "
    "**The rule-1 hazard grep earned its keep again, in a NEW shape worth remembering: running "
    "the two doc trims in the SAME cycle made one live pointer stale that neither trim alone "
    "would have broken** -- live `CLOSED c3063` named the live STATUS.md's c3053 block as a "
    "durable home, which was true until the sibling STATUS.md cut moved c3053 to the archive. "
    "Re-aimed in place, as was `NEW c3056`'s see-below pointer at the archived `CLOSED c3061`. "
    "**When both docs are "
    "trimmed in one cycle, hazard-grep each doc against the OTHER doc's cut, not just its own.**"
)

orig = open(QUEUE).read()
lines = orig.split("\n")
n = len(lines)
assert n == NLINES, f"expected {NLINES} lines, got {n} -- file changed, abort"

# boundary sanity
assert lines[12].strip() == "", "L13 should be the blank before the c3061 block"
head = lines[13]
assert head.startswith("- [ ] **CLOSED c3061 --"), f"L14 is not the c3061 head: {head[:60]!r}"

# the newest-5 floor state this cycle, asserted rather than assumed
cycle_heads = [(i + 1, l) for i, l in enumerate(lines) if re.match(r"- \[ \] \*\*CLOSED c3\d\d\d ", l)]
assert [c for c, _ in cycle_heads] == [6, 8, 10, 12, 14], \
    f"live cycle-block heads moved: {[c for c, _ in cycle_heads]}"

taken = {}
for a, b, label in CUTS:
    assert lines[b - 1].strip() == "", f"L{b} should be the blank closing {label}"
    opens = [i for i in range(a, b + 1) if lines[i - 1].startswith("- [ ] ")]
    # rule 7, adapted: exactly ONE live-item line per range, and it is this block's head
    assert opens == [a], f"{label}: expected the only `- [ ] ` line at L{a}, got {opens}"
    for i in range(a, b + 1):
        assert i not in taken, f"overlap at L{i}: {label} vs {taken[i]}"
        taken[i] = label

assert lines[16].startswith("- [ ] **NEW c3056"), \
    f"L17 must remain live (the backlog item): {lines[16][:60]!r}"
assert REWRITE_LN not in taken, "rewrite line must not also be cut"
old_exec = lines[REWRITE_LN - 1]
assert old_exec.startswith("      **EXECUTED c3069 (QUALITY slot"), \
    f"L{REWRITE_LN} is not the EXECUTED paragraph: {old_exec[:70]!r}"

# substring rewrites: each target must exist exactly once on its line and once in the file
sub_records = []
for ln, old, new in SUBS:
    assert ln not in taken, f"L{ln} is both cut and substring-rewritten"
    assert ln != REWRITE_LN, f"L{ln} collides with the whole-line rewrite"
    assert lines[ln - 1].count(old) == 1, f"L{ln}: expected exactly 1 {old!r}, got {lines[ln - 1].count(old)}"
    assert orig.count(old) == 1, f"{old!r} occurs {orig.count(old)}x in the file, not 1x"
    j = lines[ln - 1].find(old)
    sub_records.append((ln, old, new, lines[ln - 1][max(0, j - 160):j + len(old) + 120]))

# rule 1: hazard grep EVERY archive-bound range, print every hit
hazard = re.compile(r"standing|cadence|always |never |do not |must |\brule\b", re.I)
chunks, total_hits = [], 0
for a, b, label in CUTS:
    hits = [(i, lines[i - 1]) for i in range(a, b + 1) if hazard.search(lines[i - 1])]
    total_hits += len(hits)
    print(f"rule-1 hazard grep -- {label} ({a}-{b}): {len(hits)} hit(s)")
    for i, l in hits:
        print(f"  L{i}: {l.strip()[:200]}")
    chunks.append(f"<!-- c3072: {label}, queue.md lines {a}-{b} -->")
    chunks.extend(lines[a - 1:b])
    chunks.append("")
print(f"total hazard hits: {total_hits}")

# the replaced paragraph is archived verbatim, under its own marker
chunks.append("<!-- c3072: REPLACED doc-trim-cadence execution record (was EXECUTED c3069, "
              f"queue.md line {REWRITE_LN}) -->")
chunks.append(old_exec)
chunks.append("")
# the two re-aimed pointers: old fragment archived WITH surrounding context (the lines
# themselves stay live, so archiving the whole 6KB line would duplicate, not preserve)
for ln, old, new, ctx in sub_records:
    chunks.append(f"<!-- c3072: RE-AIMED dangling pointer on queue.md line {ln}: {old!r} -> "
                  f"{new!r}; old text with context below -->")
    chunks.append(ctx)
    chunks.append("")

markers = [c for c in chunks if c.startswith("<!-- c3072: ")]
archive_text = "\n".join([HEADER, ""] + chunks)

new_lines_list = []
for i, l in enumerate(lines, 1):
    if i in taken:
        continue
    if i == REWRITE_LN:
        new_lines_list.append(NEW_EXEC)
        continue
    for ln, old, new, _ in sub_records:
        if i == ln:
            l = l.replace(old, new)
    new_lines_list.append(l)
new_live = "\n".join(new_lines_list)


def nb(text):
    return Counter(l for l in text.split("\n") if l.strip())


# multiset identity over live+archive, discounting every asserted edit:
#  - HEADER + markers are new scaffolding
#  - NEW_EXEC is new text; old_exec moved to the archive (so it cancels)
#  - each substring rewrite replaces a live line with a new one and archives a context
#    snippet, so subtract the new line and the snippet, add back the original line
got = nb(new_live) + nb(archive_text) - nb(HEADER) - nb("\n".join(markers)) - nb(NEW_EXEC)
for ln, old, new, ctx in sub_records:
    got -= nb(lines[ln - 1].replace(old, new))
    got -= nb(ctx)
    got += nb(lines[ln - 1])
missing, extra = nb(orig) - got, got - nb(orig)
assert not missing, f"LINES LOST: {[m[:90] for m in list(missing)[:5]]}"
assert not extra, f"UNEXPLAINED LINES: {[e[:90] for e in list(extra)[:5]]}"
print("lossless check: OK (multiset identity over live+archive, modulo the asserted edits)")

assert new_live.count(NEW_EXEC) == 1, "new EXECUTED paragraph not placed exactly once"
assert old_exec not in new_live, "old EXECUTED paragraph still live"
assert old_exec in archive_text, "old EXECUTED paragraph not archived"
for ln, old, new, ctx in sub_records:
    assert old not in new_live, f"stale pointer still live: {old!r}"
    assert new_live.count(new) == 1, f"re-aimed pointer not placed exactly once: {new!r}"
    assert ctx in archive_text, f"old pointer context not archived for L{ln}"
print("rewrite asserts: OK (old text archived, new text placed once, no stale pointer live)")

new_lines = new_live.split("\n")
heads = [l for l in new_lines if re.match(r"- \[ \] \*\*CLOSED c3\d\d\d ", l)]
assert len(heads) == 4, f"expected 4 cycle-level CLOSED blocks live post-cut, got {len(heads)}"
for frag in ["c3071", "c3069", "c3068", "c3063"]:
    assert sum(f"**CLOSED {frag}" in h for h in heads) == 1, f"{frag} CLOSED block went missing"
assert sum(l.startswith("- [ ] **NEW c3056") for l in new_lines) == 1, "NEW c3056 lost"
before_items = sum(l.startswith("- [ ] ") or l.startswith("- [x] ") for l in lines)
after_items = sum(l.startswith("- [ ] ") or l.startswith("- [x] ") for l in new_lines)
assert before_items - after_items == 1, f"item delta {before_items - after_items}, expected 1"
for probe in ["**STANDING RULES -- the first six were rescued",
              "1. **Grep FIRST, then cut.**",
              "6. **DONE blocks are capped in LENGTH, not count",
              "stop re-reading it each QUALITY slot"]:
    assert sum(probe in l for l in new_lines) == 1, f"do-not-archive probe lost/duped: {probe!r}"
print(f"structural asserts: OK (4 CLOSED blocks live, items {before_items} -> {after_items}, "
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
