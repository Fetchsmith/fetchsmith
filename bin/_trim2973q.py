#!/usr/bin/env python3
"""c2973 proactive trim of tasks/queue.md -- a PURE CUT, no rewrites.

check-doc-size read queue.md as TRIM DUE this cycle (134.7KB/1628ln, ~12c
headroom, 262KB projected at the checker's own next look 24c out). 2973 is
the QUALITY slot (2973 = 3*991 exactly), and c2972's handoff flagged this
trim as this slot's job, per the standing precedent that trims are
QUALITY-slot work.

9 cycle-level DONE blocks are live, in INSERTION order (not chronological):
c2972(102) c2971(118) c2970(129) c2968(148) c2969(168) c2967(214) c2966(228)
c2965(240). Two shallower cuts were tried and rejected before this one:
keeping the newest 5 (archiving only c2967/c2966/c2965, 214-257) landed at
131.1KB, and keeping the newest 4 (also archiving c2968, 148-167) landed
at 132360B/~129.3KB -- BOTH still read TRIM DUE afterward, because
`check-doc-size`'s FORWARD-LOOKING test (`projected = b + rate*gap >=
READ_CAP`, cycle 1860/2220's lesson) needs b < 131584B (READ_CAP 262144 -
rate 5440 * gap 24), and 132360 missed that line by 776B. c2970's own trim
landed at 128.3KB and cleared it, but that was this doc's size at the time,
not a fixed "5 blocks is enough" rule -- the real target is the byte line,
not a block count. So this version keeps the newest 3 BY CYCLE NUMBER
(c2972/c2971/c2970) and archives the oldest 5 (c2969/c2968/c2967/c2966/
c2965), landing at ~125KB, comfortably under 128.5KB with margin for this
cycle's own remaining edits.

The archive-bound set is contiguous: c2968 (148-167) through c2965
(240-257) sit back-to-back as one 148-257 run. The nearby "CLOSED c2969:
FIX FAILED ACTORS" one-off starts at :258, immediately after the cut, and
is left live untouched.

Ranges re-derived fresh from the live file this cycle (doc-trim rule 3,
never paste forward). The archive-bound range is hazard-grepped FIRST
(rule 1) with every hit printed. No rewrites, so multiset identity is
asserted over the whole file.
"""
import os
import re
import sys
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
BACKUP = "/tmp/c2973_queue.bak"
HEADER = "## Archived by cycle 2973 (2026-11-09)"
NLINES = 1639  # 1638 real lines + the empty trailing element from the final newline
# (shifted +10 from the original 1629 by this cycle's own inserted carry-forward
# item -- the eu-ted-tenders-scraper round-loop follow-up, preserved as a live
# open task before the c2969 DONE block that originated it gets archived below)

CUTS = [
    (158, 267, "CUT DONE c2968+c2969+c2967+c2966+c2965"),
]

orig = open(QUEUE).read()
lines = orig.split("\n")
n = len(lines)
assert n == NLINES, f"expected {NLINES} lines, got {n} -- file changed, abort"

for ln, frag in [(112, "c2972"), (128, "c2971"), (139, "c2970"), (158, "c2968"),
                 (178, "c2969"), (224, "c2967"), (238, "c2966"), (250, "c2965"),
                 (268, "CLOSED c2969"), (272, "NEW STANDING NOTE")]:
    assert frag in lines[ln - 1], f"L{ln} does not mention {frag}: {lines[ln-1][:80]!r}"

taken = {}
for a, b, label in CUTS:
    assert lines[a - 1].startswith("- [x] **DONE"), \
        f"L{a} is not a DONE head: {lines[a-1][:60]!r}"
    for i in range(a, b + 1):
        assert i not in taken, f"overlap at L{i}: {label} vs {taken[i]}"
        taken[i] = label
        assert not lines[i - 1].startswith("- [ ] "), \
            f"L{i} is an OPEN item inside {label} -- refusing to archive live work: {lines[i-1][:70]!r}"
# the wedged standalone item right after the cut must stay live, untouched
for ln in range(268, 272):
    assert not any(ln in range(a, b + 1) for a, b, _ in CUTS), f"L{ln} (wedged item) must not be cut"

hazard = re.compile(r"standing|cadence|always |never |do not |must |\brule\b", re.I)
chunks, total_hits = [], 0
for a, b, label in CUTS:
    hits = [(i, lines[i - 1]) for i in range(a, b + 1) if hazard.search(lines[i - 1])]
    total_hits += len(hits)
    print(f"rule-1 hazard grep -- {label} ({a}-{b}): {len(hits)} hit(s)")
    for i, l in hits:
        print(f"  L{i}: {l.strip()[:150]}")
    chunks.append(f"<!-- c2973: {label}, queue.md lines {a}-{b} -->")
    chunks.extend(lines[a - 1:b])
    chunks.append("")
print(f"total hazard hits: {total_hits}")

markers = [c for c in chunks if c.startswith("<!-- c2973: ")]
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
assert len(heads) == 3, f"expected 3 cycle-level DONE blocks live, got {len(heads)}"
for frag in ["c2972", "c2971", "c2970"]:
    assert any(h.startswith(f"- [x] **DONE {frag} ") for h in heads), f"{frag} DONE block went missing"
for frag in ["c2969", "c2968", "c2967", "c2966", "c2965"]:
    assert not any(h.startswith(f"- [x] **DONE {frag} ") for h in heads), f"{frag} DONE block should have been archived"
for probe in ["- [x] CLOSED c2969: FIX FAILED ACTORS",
              "NEW STANDING NOTE (c2952, HIGH value",
              "NEW c2953 backlog (REWRITTEN c2958"]:
    assert sum(probe in l for l in new_lines) == 1, f"do-not-archive probe lost/duped: {probe!r}"
print("structural asserts: OK (3 DONE blocks live, wedged item + backlog header + standing note intact)")

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
