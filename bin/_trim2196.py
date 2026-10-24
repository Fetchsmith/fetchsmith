#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2196 (TRIM DUE at 162.7KB / 1970 lines,
~7 cycles of headroom at +5440 B/cycle).

Uses the c2161 HOIST-THEN-CUT method, not the stock keep-newest-10-blocks script:
queue.md interleaves standing `- [ ]` open items among completed `- [x]` cycle
blocks, so a naive cut by line number silently deletes live open work.

  1. Keep the newest 3 DONE cycle blocks (2196, 2195, 2194 -- lines 1-165). The
     c2196 block already contains this cycle's two new `- [ ]` follow-ups inline
     (lines 62-78), so those stay live for free.
  2. Hoist the 3 genuinely-live open items verbatim after the kept blocks:
       - c2168 trademark-search-scraper buyer watch   (1228-1235)
       - c2103 DMARC recheck, blocked on new mail      (1973-1978)
       - c2120 re-verify due-lists process lesson      (1981-1984)
  3. Archive everything else verbatim to tasks/queue_archive.md, in original order.
     This deliberately INCLUDES the stale `- [ ]` PPE rotation item (1273), which
     still advertises "3 LEFT" even though c2191/c2194 finished all three and c2194
     closed the rotation at 24/24 fleet-wide. It is archived as-is rather than
     rewritten, so the lossless verification below stays a byte-level check; its
     closure is recorded in the live c2196 block instead.

Why 3 blocks and not the stock 10: keeping 10 leaves 39.3KB live, which at the
measured +5440 B/cycle and check-doc-size's own 24-cycle interval projects ~167KB at
the next look -- straight back into WARN, the mistake cycle 1976 made and documented.
Keeping 3 leaves ~15KB and projects ~145KB, under the 150KB warn line with room.

Verifies losslessly before writing anything.
"""
import sys

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 1985, f"expected 1985 lines, got {len(lines)} -- file changed, abort"

# 1-indexed inclusive ranges, pinned by inspection this cycle.
KEEP_END = 165                      # line 166 starts the cycle 2193 block
TRADEMARK = (1228, 1235)
DMARC = (1973, 1978)
LESSON = (1981, 1984)
HOISTED = [TRADEMARK, DMARC, LESSON]


def seg(a, b):
    """1-indexed inclusive line range -> list of lines."""
    return lines[a - 1:b]


# --- Preconditions: every pinned boundary is what this script thinks it is ---
assert lines[0].startswith("- [x] **DONE cycle 2196"), "newest block is not cycle 2196"
assert lines[KEEP_END].startswith("- [x] **DONE cycle 2193"), "cut point is not cycle 2193"
assert seg(*TRADEMARK)[0].startswith("- [ ] **NEW follow-up (c2168)"), "trademark range moved"
assert seg(*DMARC)[0].startswith("- [ ] **STILL OPEN (carried from c2103"), "DMARC range moved"
assert seg(*LESSON)[0].startswith("- [ ] **Process lesson"), "lesson range moved"
for a, b in HOISTED:
    assert a > KEEP_END, "a hoisted range overlaps the kept region"
    assert lines[b].strip() == "", f"range {a}-{b} does not end on a blank line"

kept = seg(1, KEEP_END)
hoisted = []
for a, b in HOISTED:
    hoisted += seg(a, b) + ["\n"]

hoisted_idx = {i for a, b in HOISTED for i in range(a, b + 1)}
archived = [lines[i - 1] for i in range(KEEP_END + 1, len(lines) + 1)
            if i not in hoisted_idx]

with open(ARCHIVE) as f:
    old_archive = f.read()

header = (
    "\n## Archived by cycle 2196 (opus-5), 2026-10-24 -- tasks/queue.md had grown to "
    "1970 lines / 162.7KB, TRIM DUE per check-doc-size with only ~7 cycles of headroom at "
    "+5440 B/cycle. Cycles <=2193 moved here verbatim, in original order; the live file keeps "
    "the newest 3 DONE blocks (2196, 2195, 2194) plus the 3 genuinely-live open items, which "
    "were HOISTED (c2168 trademark-search buyer watch, c2103 DMARC recheck, c2120 "
    "re-verify-due-lists process lesson). Only 3 blocks, not the stock 10: keeping 10 leaves "
    "39.3KB live and projects ~167KB at the next look -- straight back into WARN (the "
    "cycle-1976 mistake) -- while 3 leaves ~15KB and projects ~145KB. NOTE: the `- [ ] OPEN "
    "(ongoing rotation, now 21/24 ...)` PPE chargedEventCounts item below is archived as "
    "CLOSED, not pending: it still reads '3 LEFT' but c2191/c2194 finished all three and c2194 "
    "closed that rotation at 24/24 fleet-wide with 0 leaks. Do not resume it; a fresh "
    "charge-path pass would be a NEW rotation.\n\n"
)
addition = header + "".join(archived)
new_archive = old_archive + addition
new_live = kept + hoisted
while len(new_live) >= 2 and new_live[-1] == "\n" and new_live[-2] == "\n":
    new_live.pop()

# --- Verification 1: nothing lost -- every non-blank original line survives somewhere ---
live_text, arch_text = "".join(new_live), new_archive
for i, ln in enumerate(lines, 1):
    if ln.strip() and ln not in live_text and ln not in arch_text:
        sys.exit(f"FAIL: line {i} destroyed: {ln[:90]!r}")

# --- Verification 2: exact partition -- kept+hoisted+archived rebuilds the original ---
rebuilt = {}
for i in range(1, KEEP_END + 1):
    rebuilt[i] = lines[i - 1]
for a, b in HOISTED:
    for i in range(a, b + 1):
        rebuilt[i] = lines[i - 1]
for n, i in enumerate(i for i in range(KEEP_END + 1, len(lines) + 1)
                      if i not in hoisted_idx):
    rebuilt[i] = archived[n]
if "".join(rebuilt[i] for i in sorted(rebuilt)) != "".join(lines):
    sys.exit("FAIL: kept + hoisted + archived does not reconstruct the original file")
assert len(rebuilt) == len(lines), "partition does not cover every line exactly once"

# --- Verification 3: prior archive preserved byte-identically, addition only appends ---
if not new_archive.startswith(old_archive):
    sys.exit("FAIL: prior archive content would not be preserved byte-identically")

# --- Verification 4: every cycle-block header still exists in live+archive ---
for ln in lines:
    if ln.startswith("- [x] **DONE cycle") or ln.startswith("- [ ] **"):
        if ln not in live_text and ln not in arch_text:
            sys.exit(f"FAIL: block header destroyed: {ln[:90]!r}")

# --- Verification 5: all 3 hoisted items are live, and the stale one is NOT ---
for a, b in HOISTED:
    if lines[a - 1] not in live_text:
        sys.exit(f"FAIL: hoisted item {a} did not land in the live file")
stale = "- [ ] **OPEN (ongoing rotation, now 21/24"
if any(l.startswith(stale) for l in new_live):
    sys.exit("FAIL: the stale PPE rotation item should be archived, not live")
if not any(l.startswith(stale) for l in archived):
    sys.exit("FAIL: the stale PPE rotation item is missing from the archive")

print("All 5 verifications passed. Writing files.")
with open(SRC, "w") as f:
    f.write(live_text)
with open(ARCHIVE, "w") as f:
    f.write(new_archive)
print(f"live queue.md:     {len(new_live)} lines / {len(live_text.encode())} bytes")
print(f"archive addition:  {len(archived)} lines")
print(f"open items live:   {sum(1 for l in new_live if l.startswith('- [ ] '))}")
