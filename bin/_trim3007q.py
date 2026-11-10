#!/usr/bin/env python3
"""c3007 trim of tasks/queue.md -- CUT-ONLY (no rewrite needed), self-triggered.

This cycle's own STATUS/queue writes (the CLOSED c3007 record plus the standing
GROWTH-pointer update) pushed queue.md from ~130.0KB to 133,093B, over the forward-test
cap `b < 131,584B` (= 262,144 - 5,440*24). Per the c3004 precedent, a cycle whose OWN
writes trigger TRIM DUE clears it in the same cycle regardless of Regular/Quality slot
labeling (c3004 was also a Regular slot, 3004 % 3 == 1, and did exactly this).

The lever: the newest-5 DONE-block floor (`bin/check-doc-size`, c2224/c1836 rule). With
this cycle's CLOSED c3007 added, the live file now carries SIX cycle-closure records
before any non-closure item: c3007(L1), c3006(L3), c3005(L5), c3004(L7), c3003(L11),
c3000(L144) -- the 6th, `CLOSED c3000`, is past the floor and eligible to archive.

Two facts inside `CLOSED c3000` are load-bearing and must survive the cut -- verified by
grep BEFORE writing this script, both already duplicated verbatim elsewhere in the live
file, so archiving loses no live-doc fact:
  - the forward-test formula `b < 131,584B`: restated in `CLOSED c3004` (L7).
  - "queue.md's DONE-block floor is the newest-5 convention": restated in `CLOSED c3004`
    (L7, "newest-5 DONE-block floor") and in the doc-trim cadence item (~L1037,
    "a newest-5 ... floor").

Second cut: `COMPRESSED c2988` (L164-206), self-declared "BACKLOG FULLY CLOSED c2976 --
zero work left" with its 3 standing lessons already explicitly homed in LEARNINGS.md by
the item's own citations -- verified live before cutting:
  (a) "DISAGREE is presumed-phantom-until-disproven" -> LEARNINGS.md:7044 (Cycle 2964).
  (b) the claim-count-diff rule -> LEARNINGS.md:7157 (Cycle c2976 entry).
  (c) the UNDATED-flag-three-shapes rule -> cited inline as "LEARNINGS c2960, ~line 7034"
      (item's own text, not re-verified byte-for-byte here since it is a direct citation,
      not a claim of duplication).
This item carries no open work (explicitly "do NOT re-open it or re-grind its file list"),
so it is a pure archive-for-space move, same shape as c3004's c2896/c2950 rotation.

Both cuts are archived VERBATIM into queue_archive.md. No rewrite, no new text -- the
multiset-losslessness check is therefore just "every original non-blank line in the two
cut ranges is findable in the archive," simpler than the c3000/c3004 MIXED scripts.
"""
import os
import sys
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
BACKUP = "/tmp/c3007_queue.bak"
HEADER = "## Archived by cycle 3007 (2026-11-10)"
NLINES = 1458  # wc -l + 1 for the trailing split element

# (start, end, label) -- 1-indexed inclusive, all archived verbatim, cut-only
OPS = [
    (144, 163, "CLOSED c3000 (queue.md trim record, past the newest-5 DONE-block floor)"),
    (164, 206, "COMPRESSED c2988 (backlog self-declared FULLY CLOSED c2976, 0 open work)"),
]

orig = open(QUEUE).read()
lines = orig.split("\n")
n = len(lines)
assert n == NLINES, f"expected {NLINES} lines, got {n} -- file changed, abort"

# --- boundary asserts, re-derived fresh ---
checks = [
    (144, "CLOSED c3000"), (163, "Full detail in STATUS.md c3000"),
    (164, "COMPRESSED c2988"), (206, "LEARNINGS c2960, ~line 7034"),
    (207, "NEW STANDING NOTE (c2952"),
]
for ln, frag in checks:
    assert frag in lines[ln - 1], f"L{ln} does not mention {frag!r}: {lines[ln-1][:90]!r}"

taken = {}
for a, b, label in OPS:
    assert lines[a - 1].startswith("- ["), f"L{a} is not an item head: {lines[a-1][:60]!r}"
    for i in range(a, b + 1):
        assert i not in taken, f"overlap at L{i}: {label} vs {taken[i]}"
        taken[i] = label

# the open items immediately adjacent must survive untouched
for ln in [143, 142, 207, 208]:
    assert ln not in taken, f"L{ln} must not be touched"

# the two load-bearing facts must already be duplicated live, BEFORE we cut their only
# other home -- re-verify fresh, not from the docstring's earlier grep
assert "b < 131,584B" in lines[6], "forward-test formula not duplicated at L7 (CLOSED c3004)"
assert "newest-5 DONE-block floor" in lines[6], "DONE-block-floor fact not duplicated at L7"

# --- build archive (verbatim) and new live file ---
chunks = []
for a, b, label in OPS:
    m = f"<!-- c3007: CUT {label}, queue.md lines {a}-{b} -->"
    chunks.append(m)
    chunks.extend(lines[a - 1:b])
    chunks.append("")
archive_text = "\n".join([HEADER, ""] + chunks)

out = [l for i, l in enumerate(lines, 1) if i not in taken]
new_live = "\n".join(out)

# --- losslessness: every cut line is verbatim in the archive ---
def nb(text):
    return Counter(l for l in text.split("\n") if l.strip())

cut_counter = Counter()
for a, b, _ in OPS:
    cut_counter.update(l for l in lines[a - 1:b] if l.strip())
archived_counter = nb(archive_text)
missing = cut_counter - archived_counter
assert not missing, f"LINES LOST: {list(missing)[:5]}"
# and nothing outside the cut ranges changed
assert nb(new_live) + cut_counter == nb(orig), "live+cut no longer reconstructs original"
print("lossless check: OK (every cut line verbatim in archive; live+cut == original)")

# --- structural asserts ---
new_lines = new_live.split("\n")
for gone in ["- [x] **CLOSED c3000", "- [ ] **COMPRESSED c2988"]:
    assert not any(l.startswith(gone) for l in new_lines), f"{gone!r} still live"
for probe in ["- [ ] **CLOSED c3007", "- [ ] **CLOSED c3006", "- [ ] **CLOSED c3005",
              "- [ ] **CLOSED c3004", "- [ ] **CLOSED c3003",
              "- [ ] **NEW STANDING NOTE (c2952"]:
    assert sum(l.startswith(probe) for l in new_lines) == 1, f"do-not-touch probe lost/duped: {probe!r}"
print("structural asserts: OK (2 cut, newest-5 closures and neighbours intact)")

b = len(new_live)
proj = b + 5440 * 24
print(f"forward test: b={b}B, projected at next look = {proj}B "
      f"({'PASS' if proj < 262144 else 'FAIL'}, cap 262144), "
      f"headroom {(262144 - b) / 5440:.1f} cycles")

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
