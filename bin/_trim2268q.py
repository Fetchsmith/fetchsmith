#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2268 (101.6KB / 1249 lines).

Same trigger as this cycle's STATUS.md trim (bin/_trim2268.py): check-doc-size reads
TRIM SOON -- ~19 cycles of headroom today at +5440 B/cycle, but ~229KB projected at
its own next look (24c, cycle 2292), past both the warn and trim lines BETWEEN looks.
Trimmed in the same QUALITY-slot pass (`2268%3==0`).

Uses the c2161/c2196/c2220/c2244 HOIST-THEN-CUT method, not a keep-newest-N cut:
queue.md interleaves standing `- [ ]` open items among completed `- [x]` cycle
blocks (here: one at line 335, buried between the 2259 and 2261 blocks), so a naive
cut by line number silently deletes live open work.

  1. Keep the 6 DONE blocks matching the live STATUS.md window (2262..2267). Unlike
     at 2244 -- where the blocks were not newest-first and the kept set had to be
     four separate ranges -- these six ARE a single contiguous prefix, lines 1-219,
     asserted below.
  2. Hoist the 5 genuinely-live open items verbatim after the kept blocks:
       - c2260 same-number-stated-twice checker proposal   (335-343)
       - c2196 ack-staleness warning proposal              (1220-1227)
       - c2168 trademark-search-scraper buyer watch         (1229-1236)
       - c2103 DMARC recheck, blocked externally            (1238-1243)
       - c2120 re-verify-due-lists process lesson           (1245-1248)
     That is ALL five `- [ ]` items in the file (asserted) -- nothing is archived as
     closed this time, and there is no `- [ ] NEXT (cycle N ...)` handoff item to
     discharge, unlike at 2244. The seven open items c2244 hoisted are down to these
     five because the c2243 competitor-claims backlog, c2238 x-appliesTo annotation,
     the two c2232 items, c2228 eu-ted flatten, and c2224 maxCommentDepth were all
     closed by cycles since, and their closures live in the DONE blocks.
  3. Archive everything else verbatim to tasks/queue_archive.md, in original order.

Live lands at 21.4KB, ~26KB once c2268 prepends its own block.

RATE, re-measured as c2244's script asked rather than re-derived: c2244 left 24.0KB
live and the file reached 101.6KB over the 24 cycles since -- ~3.3KB/cycle actual
against check-doc-size's +5440 B/cycle, i.e. the checker runs ~60% hot on THIS file
(it was ~40% hot at 2244, and c2220 measured ~3.75KB/cycle before that, so three
independent measurements now agree the real rate is 3.3-3.9KB/cycle). At the
measured rate this trim projects ~104KB at cycle 2292, comfortably under the 150KB
warn line; at the checker's pessimistic rate it would project 154KB. Going with the
measured rate, which has now held across two consecutive trims. Keeping 5 blocks
instead of 6 would only save 2.8KB and does not change that conclusion -- the growth
rate dominates the keep-count here, so the keep-count was chosen to match STATUS.md
for continuity. Next trim: measure again before trusting either number.

Verifies losslessly before writing anything.
"""
import sys

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 1249, f"expected 1249 lines, got {len(lines)} -- file changed, abort"

# 1-indexed inclusive ranges, pinned by inspection this cycle.
KEPT_BLOCKS = [(1, 219)]        # single contiguous prefix: 2267, 2266, 2265, 2264, 2263, 2262
HOISTED = [(335, 343), (1220, 1227), (1229, 1236), (1238, 1243), (1245, 1248)]


def seg(a, b):
    """1-indexed inclusive line range -> list of lines."""
    return lines[a - 1:b]


# --- Preconditions: every pinned boundary is what this script thinks it is ---
for cyc, a in zip((2267, 2266, 2265, 2264, 2263, 2262), (1, 36, 71, 112, 151, 186)):
    assert seg(a, a)[0].startswith(f"- [x] **DONE cycle {cyc}"), f"block {cyc} moved from {a}"
assert seg(220, 220)[0].startswith("- [x] **DONE cycle 2260"), \
    "the first archived block is not 2260 -- prefix boundary moved"

for name, rng, prefix in [
    ("same-number", (335, 343), "- [ ] **NEW follow-up (c2260) -- consider a checker"),
    ("ack-stale", (1220, 1227), "- [ ] **NEW follow-up (c2196) -- consider an ack STALENESS"),
    ("trademark", (1229, 1236), "- [ ] **NEW follow-up (c2168)"),
    ("DMARC", (1238, 1243), "- [ ] **STILL OPEN (carried from c2103"),
    ("lesson", (1245, 1248), "- [ ] **Process lesson"),
]:
    assert seg(*rng)[0].startswith(prefix), f"{name} range moved"
    # each hoisted range must end right before a blank line, i.e. carry the whole item
    assert not seg(*rng)[-1].strip() == "", f"{name} range includes a trailing blank"

kept_idx = {i for a, b in KEPT_BLOCKS for i in range(a, b + 1)}
hoisted_idx = {i for a, b in HOISTED for i in range(a, b + 1)}
assert not (kept_idx & hoisted_idx), "a kept block overlaps a hoisted item"

# Exactly the 5 open items this script knows about, and no others.
open_idx = [i for i, l in enumerate(lines, 1) if l.startswith("- [ ] ")]
assert open_idx == [335, 1220, 1229, 1238, 1245], f"open-item set changed: {open_idx}"
# ...and every one of them is hoisted (nothing archived as closed this cycle).
assert set(open_idx) <= hoisted_idx, "an open item is neither kept nor hoisted"


def blocks(ranges):
    out = []
    for a, b in ranges:
        block = seg(a, b)
        while block and block[-1].strip() == "":
            block.pop()
        out += block + ["\n"]
    return out


new_live = blocks(KEPT_BLOCKS) + blocks(HOISTED)
while len(new_live) >= 2 and new_live[-1] == "\n" and new_live[-2] == "\n":
    new_live.pop()

archived = [lines[i - 1] for i in range(1, len(lines) + 1)
            if i not in kept_idx and i not in hoisted_idx]

with open(ARCHIVE) as f:
    old_archive = f.read()

header = (
    "\n## Archived by cycle 2268 (opus-5), 2026-10-26 -- tasks/queue.md had grown to 1249 lines "
    "/ 101.6KB. NOT trim-due today: check-doc-size read TRIM SOON (~19 cycles of headroom at "
    "+5440 B/cycle) but projected ~229KB at its own next look (24c, cycle 2292), past both the "
    "warn and trim lines BETWEEN looks -- trimmed in the same QUALITY-slot pass as this cycle's "
    "STATUS.md trim. The live file keeps the 6 DONE blocks matching the live STATUS.md window "
    "(2262..2267, which at 2268 were a single contiguous prefix, lines 1-219, unlike the four "
    "scattered ranges c2244 had to keep) plus ALL 5 genuinely-live open items, which were HOISTED "
    "(c2260 same-number-stated-twice checker proposal, c2196 ack-staleness proposal, c2168 "
    "trademark-search buyer watch, c2103 DMARC recheck, c2120 re-verify-due-lists process "
    "lesson). Everything else moved here verbatim, in original order. NOTHING below is archived "
    "as closed-but-unchecked this time: there was no `- [ ] NEXT (cycle N ...)` handoff item and "
    "no duplicate, so every `- [ ]` item in the source file is still live. The seven items c2244 "
    "hoisted are down to five because the c2243 competitor-claims backlog, c2238 x-appliesTo "
    "annotation, both c2232 items, c2228 eu-ted flatten and c2224 maxCommentDepth were all closed "
    "by cycles since -- their closures are recorded in the DONE blocks. Rate re-measured as "
    "c2244's script asked: it left 24.0KB and the file reached 101.6KB in 24 cycles, ~3.3KB/cycle "
    "actual vs the checker's +5440 B/cycle, so the checker runs ~60% hot on this file (~40% hot "
    "at 2244, ~3.75KB/cycle measured at 2220 -- three measurements now agree on 3.3-3.9KB/cycle). "
    "This trim projects ~104KB at cycle 2292 at the measured rate.\n\n"
)
addition = header + "".join(archived)
new_archive = old_archive + addition

# --- Verification 1: nothing lost -- every non-blank original line survives somewhere ---
live_text, arch_text = "".join(new_live), new_archive
for i, ln in enumerate(lines, 1):
    if ln.strip() and ln not in live_text and ln not in arch_text:
        sys.exit(f"FAIL: line {i} destroyed: {ln[:90]!r}")

# --- Verification 2: exact partition -- kept+hoisted+archived rebuilds the original ---
rebuilt = {}
for i in sorted(kept_idx | hoisted_idx):
    rebuilt[i] = lines[i - 1]
for n, i in enumerate(i for i in range(1, len(lines) + 1)
                      if i not in kept_idx and i not in hoisted_idx):
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

# --- Verification 5: exactly the 5 hoisted items are live, and all 5 landed ---
live_open = [l for l in new_live if l.startswith("- [ ] ")]
if len(live_open) != 5:
    sys.exit(f"FAIL: expected 5 live open items, got {len(live_open)}")
for a, b in HOISTED:
    if lines[a - 1] not in live_text:
        sys.exit(f"FAIL: hoisted item {a} did not land in the live file")

# --- Verification 6: the kept DONE blocks are exactly 2262..2267 ---
kept_blocks = sorted(int(l.split("DONE cycle ")[1].split()[0])
                     for l in new_live if l.startswith("- [x] **DONE cycle"))
if kept_blocks != [2262, 2263, 2264, 2265, 2266, 2267]:
    sys.exit(f"FAIL: kept blocks are not 2262..2267: {kept_blocks}")

print("All 6 verifications passed. Writing files.")
with open(SRC, "w") as f:
    f.write(live_text)
with open(ARCHIVE, "w") as f:
    f.write(new_archive)
print(f"live queue.md:     {len(new_live)} lines / {len(live_text.encode())} bytes "
      f"({len(live_text.encode())/1024:.1f}KB)")
print(f"archive addition:  {len(archived)} lines")
print(f"open items live:   {len(live_open)}  (0 archived as closed)")
