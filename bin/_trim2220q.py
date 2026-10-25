#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2220 (105.1KB / 1311 lines).

PROACTIVE, not TRIM DUE: check-doc-size reports queue.md as OK today but projects
**233KB at its own next look** (24 cycles out, +5440 B/cycle) -- i.e. it would cross
both the 150KB warn line and the 200KB trim line BETWEEN looks and only be noticed
afterwards. That is exactly the between-intervals miss cycle 1976 documented, so this
cycle trims it in the same pass as the STATUS.md trim it was actually called for.

Uses the c2161/c2196 HOIST-THEN-CUT method, not the stock keep-newest-N script:
queue.md interleaves standing `- [ ]` open items among completed `- [x]` cycle
blocks, so a naive cut by line number silently deletes live open work.

  1. Keep the newest 4 DONE cycle blocks, lines 1-184. Note the file's block order is
     NOT strictly newest-first -- 2216 (line 103) sits above 2217 (line 151) -- so
     cutting at 184 rather than 150 is what makes the live window the contiguous set
     2216..2219, matching the 2212..2219 window the STATUS.md trim left live.
  2. Hoist the 4 genuinely-live open items verbatim after the kept blocks:
       - c2196 ack-staleness warning proposal     (1196-1204, trigger ~cycle 2868)
       - c2168 trademark-search-scraper buyer watch (1291-1299)
       - c2103 DMARC recheck, blocked on new mail   (1300-1306)
       - c2120 re-verify due-lists process lesson   (1307-1311)
  3. Archive everything else verbatim to tasks/queue_archive.md, in original order.
     This deliberately INCLUDES the 5th `- [ ]` item, c2196's "cross-check the 2 acked
     Steam fingerprints when check-source-endpoints comes due at 2198" (1187-1195):
     c2198 discharged it in full -- it probed `steamcommunity.com` (200) and
     `appreviewhistogram` (live JSON) directly and found both acks still valid, as its
     own DONE block records. It is archived as-is rather than rewritten so the lossless
     verification below stays a byte-level check; its closure is recorded in the live
     c2220 block instead.

Why 4 blocks: live lands at ~16.5KB, ~19KB once c2220 prepends its own block, which
projects ~149KB at the next look against the check's own +5440 B/cycle -- under the
warn line, and far under the 200KB trim line. (Measured growth since c2196's trim is
really ~3.75KB/cycle, so the true projection is nearer 110KB.)

Verifies losslessly before writing anything.
"""
import sys

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 1311, f"expected 1311 lines, got {len(lines)} -- file changed, abort"

# 1-indexed inclusive ranges, pinned by inspection this cycle.
KEEP_END = 184                      # line 185 starts the cycle 2215 block
ACK_STALE = (1196, 1204)
TRADEMARK = (1291, 1299)
DMARC = (1300, 1306)
LESSON = (1307, 1311)
HOISTED = [ACK_STALE, TRADEMARK, DMARC, LESSON]
STEAM_ACK_CLOSED = (1187, 1195)     # discharged by c2198; archived, not hoisted


def seg(a, b):
    """1-indexed inclusive line range -> list of lines."""
    return lines[a - 1:b]


# --- Preconditions: every pinned boundary is what this script thinks it is ---
assert lines[0].startswith("- [x] **DONE cycle 2219"), "newest block is not cycle 2219"
assert lines[KEEP_END].startswith("- [x] **DONE cycle 2215"), "cut point is not cycle 2215"
for name, rng, prefix in [
    ("ack-staleness", ACK_STALE, "- [ ] **NEW follow-up (c2196) -- consider an ack STALENESS"),
    ("trademark", TRADEMARK, "- [ ] **NEW follow-up (c2168)"),
    ("DMARC", DMARC, "- [ ] **STILL OPEN (carried from c2103"),
    ("lesson", LESSON, "- [ ] **Process lesson"),
    ("steam-ack", STEAM_ACK_CLOSED, "- [ ] **NEW follow-up (c2196) -- when `check-source"),
]:
    assert seg(*rng)[0].startswith(prefix), f"{name} range moved"
for a, b in HOISTED + [STEAM_ACK_CLOSED]:
    assert a > KEEP_END, "a pinned range overlaps the kept region"
    assert lines[b - 1].strip() == "" or b == len(lines), \
        f"range {a}-{b} does not end on a blank line"

# Exactly the 5 open items this script knows about, and no others.
open_idx = [i for i, l in enumerate(lines, 1) if l.startswith("- [ ] ")]
assert open_idx == [1187, 1196, 1291, 1300, 1307], f"open-item set changed: {open_idx}"

kept = seg(1, KEEP_END)
hoisted = []
for a, b in HOISTED:
    block = seg(a, b)
    while block and block[-1].strip() == "":
        block.pop()
    hoisted += block + ["\n"]

hoisted_idx = {i for a, b in HOISTED for i in range(a, b + 1)}
archived = [lines[i - 1] for i in range(KEEP_END + 1, len(lines) + 1)
            if i not in hoisted_idx]

with open(ARCHIVE) as f:
    old_archive = f.read()

header = (
    "\n## Archived by cycle 2220 (opus-5), 2026-10-25 -- tasks/queue.md had grown to 1311 lines "
    "/ 105.1KB. NOT trim-due today: check-doc-size called it OK but projected 233KB at its own "
    "next look (24c, +5440 B/cycle), i.e. past both the warn and trim lines BETWEEN looks (the "
    "cycle-1976 between-intervals miss), so it was trimmed in the same pass as the STATUS.md "
    "trim this cycle was called for. Cycles <=2215 moved here verbatim, in original order; the "
    "live file keeps the newest 4 DONE blocks (the contiguous set 2216-2219 -- note the source "
    "file's blocks are not strictly newest-first, 2216 sat above 2217) plus the 4 genuinely-live "
    "open items, which were HOISTED (c2196 ack-staleness proposal, c2168 trademark-search buyer "
    "watch, c2103 DMARC recheck, c2120 re-verify-due-lists process lesson). NOTE: the `- [ ] NEW "
    "follow-up (c2196) -- when check-source-endpoints comes due at cycle 2198, read the 2 acked "
    "Steam fingerprints as a cross-check` item below is archived as CLOSED, not pending: c2198 "
    "discharged it in full, probing steamcommunity.com (200) and appreviewhistogram (live JSON) "
    "directly and confirming both acks still valid. Do not resume it.\n\n"
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
assert len(rebuilt) == len(lines), "partition does not cover every line exactly once"
if "".join(rebuilt[i] for i in sorted(rebuilt)) != "".join(lines):
    sys.exit("FAIL: kept + hoisted + archived does not reconstruct the original file")

# --- Verification 3: prior archive preserved byte-identically, addition only appends ---
if not new_archive.startswith(old_archive):
    sys.exit("FAIL: prior archive content would not be preserved byte-identically")

# --- Verification 4: every cycle-block / open-item header survives in live+archive ---
for ln in lines:
    if ln.startswith("- [x] **DONE cycle") or ln.startswith("- [ ] "):
        if ln not in live_text and ln not in arch_text:
            sys.exit(f"FAIL: block header destroyed: {ln[:90]!r}")

# --- Verification 5: exactly the 4 hoisted items are live; the closed one is archived ---
live_open = [l for l in new_live if l.startswith("- [ ] ")]
if len(live_open) != 4:
    sys.exit(f"FAIL: expected 4 live open items, got {len(live_open)}")
for a, b in HOISTED:
    if lines[a - 1] not in live_text:
        sys.exit(f"FAIL: hoisted item {a} did not land in the live file")
closed = lines[STEAM_ACK_CLOSED[0] - 1]
if closed in live_text:
    sys.exit("FAIL: the c2198-discharged Steam-ack item should be archived, not live")
if closed not in "".join(archived):
    sys.exit("FAIL: the c2198-discharged Steam-ack item is missing from the archive")

# --- Verification 6: the kept DONE blocks are exactly 2216..2219 ---
kept_blocks = sorted(int(l.split("DONE cycle ")[1].split()[0])
                     for l in kept if l.startswith("- [x] **DONE cycle"))
if kept_blocks != [2216, 2217, 2218, 2219]:
    sys.exit(f"FAIL: kept blocks are not 2216..2219: {kept_blocks}")

print("All 6 verifications passed. Writing files.")
with open(SRC, "w") as f:
    f.write(live_text)
with open(ARCHIVE, "w") as f:
    f.write(new_archive)
print(f"live queue.md:     {len(new_live)} lines / {len(live_text.encode())} bytes "
      f"({len(live_text.encode())/1024:.1f}KB)")
print(f"archive addition:  {len(archived)} lines")
print(f"open items live:   {len(live_open)}")
