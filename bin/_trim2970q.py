#!/usr/bin/env python3
"""c2970 proactive trim of tasks/queue.md -- a PURE CUT, no rewrites.

check-doc-size read queue.md as TRIM DUE this cycle (131.8KB/1595ln, ~13c
headroom, 259KB projected at the checker's own next look 24c out). 2970 is the
QUALITY slot (2970 = 3*990 exactly), and c2969's handoff flagged this trim as
this slot's job, per the standing precedent that trims are QUALITY-slot work.

8 cycle-level DONE blocks were live, in INSERTION order (not chronological):
c2968(70) c2969(90) c2967(136) c2966(150) c2965(162) c2964(180) c2963(204)
c2962(215). Keeping the newest 5 BY CYCLE NUMBER (c2969/c2968/c2967/c2966/
c2965) and archiving the oldest 3 (c2964/c2963/c2962), matching STATUS.md's
convention and the doc-trim item's newest-5 floor for queue.md.

The archive-bound set is NON-CONTIGUOUS this time: a standalone one-off item,
"- [x] CLOSED c2969: FIX FAILED ACTORS ..." (lines 200-203), sits wedged
between the c2964 and c2963 cycle blocks. That item is NOT one of the 8
cycle-level DONE blocks (it has its own different heading shape, "CLOSED
c2969:", not "DONE c29XX (...slot...)"), was closed only this same cycle
(c2969), and is left live untouched -- same "dodge the interleaved item"
shape as c2964's own trim script hit with its NEW STANDING NOTE.

Ranges re-derived fresh from the live file this cycle (doc-trim rule 3, never
paste forward). The archive-bound range is hazard-grepped FIRST (rule 1) with
every hit printed. No rewrites, so multiset identity is asserted over the
whole file.
"""
import os
import re
import sys
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
BACKUP = "/tmp/c2970_queue.bak"
HEADER = "## Archived by cycle 2970 (2026-11-09)"
NLINES = 1596  # 1595 real lines + the empty trailing element from the final newline

CUTS = [
    (180, 199, "CUT DONE c2964"),
    (204, 214, "CUT DONE c2963"),
    (215, 228, "CUT DONE c2962"),
]

orig = open(QUEUE).read()
lines = orig.split("\n")
n = len(lines)
assert n == NLINES, f"expected {NLINES} lines, got {n} -- file changed, abort"

for ln, frag in [(70, "c2968"), (90, "c2969"), (136, "c2967"), (150, "c2966"),
                 (162, "c2965"), (180, "c2964"), (200, "CLOSED c2969"),
                 (204, "c2963"), (215, "c2962"), (229, "NEW STANDING NOTE")]:
    assert frag in lines[ln - 1], f"L{ln} does not mention {frag}: {lines[ln-1][:80]!r}"
for ln in (199, 228):
    assert lines[ln - 1].strip() == "", f"L{ln} should be blank: {lines[ln-1][:80]!r}"
# the wedged standalone item must stay live, untouched by any cut
for ln in range(200, 204):
    assert not any(ln in range(a, b + 1) for a, b, _ in CUTS), f"L{ln} (wedged item) must not be cut"

taken = {}
for a, b, label in CUTS:
    assert lines[a - 1].startswith("- [x] **DONE"), \
        f"L{a} is not a DONE head: {lines[a-1][:60]!r}"
    for i in range(a, b + 1):
        assert i not in taken, f"overlap at L{i}: {label} vs {taken[i]}"
        taken[i] = label
        assert not lines[i - 1].startswith("- [ ] "), \
            f"L{i} is an OPEN item inside {label} -- refusing to archive live work: {lines[i-1][:70]!r}"

hazard = re.compile(r"standing|cadence|always |never |do not |must |\brule\b", re.I)
chunks, total_hits = [], 0
for a, b, label in CUTS:
    hits = [(i, lines[i - 1]) for i in range(a, b + 1) if hazard.search(lines[i - 1])]
    total_hits += len(hits)
    print(f"rule-1 hazard grep -- {label} ({a}-{b}): {len(hits)} hit(s)")
    for i, l in hits:
        print(f"  L{i}: {l.strip()[:150]}")
    chunks.append(f"<!-- c2970: {label}, queue.md lines {a}-{b} -->")
    chunks.extend(lines[a - 1:b])
    chunks.append("")
print(f"total hazard hits: {total_hits}")

markers = [c for c in chunks if c.startswith("<!-- c2970: ")]
archive_text = "\n".join([HEADER, ""] + chunks)
new_live = "\n".join([l for i, l in enumerate(lines, 1) if i not in taken])


def nb(text):
    return Counter(l for l in text.split("\n") if l.strip())


got = nb(new_live) + nb(archive_text) - nb(HEADER) - nb("\n".join(markers))
missing, extra = nb(orig) - got, got - nb(orig)
assert not missing, f"LINES LOST: {list(missing)[:5]}"
assert not extra, f"UNEXPLAINED LINES: {list(extra)[:5]}"
print("lossless check: OK (pure cut, multiset identity over live+archive)")

new_lines = new_live.split("\n")
heads = [l for l in new_lines if l.startswith("- [x] **DONE c29")]
assert len(heads) == 5, f"expected 5 cycle-level DONE blocks live, got {len(heads)}"
for frag in ["c2969", "c2968", "c2967", "c2966", "c2965"]:
    assert any(frag in h for h in heads), f"{frag} DONE block went missing"
for frag in ["c2964", "c2963", "c2962"]:
    assert not any(frag in h for h in heads), f"{frag} DONE block should have been archived"
for probe in ["CLOSED c2969: FIX FAILED ACTORS",
              "NEW STANDING NOTE (c2952, HIGH value",
              "NEW c2953 backlog (REWRITTEN c2958"]:
    assert sum(probe in l for l in new_lines) == 1, f"do-not-archive probe lost/duped: {probe!r}"
print("structural asserts: OK (5 DONE blocks live, wedged item + backlog header + standing note intact)")

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
