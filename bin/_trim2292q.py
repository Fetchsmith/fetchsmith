#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2292 (88.9KB / 1087 lines).

Same trigger as this cycle's STATUS.md trim (bin/_trim2292.py): check-doc-size
reads TRIM SOON -- ~21 cycles of headroom today at +5440 B/cycle, but ~216KB
projected at its own next look (24c, cycle 2316), past both the warn and trim
lines BETWEEN looks. Trimmed in the same QUALITY-slot pass (`2292%3==0`).

Uses the c2161/c2196/c2220/c2244/c2268 HOIST-THEN-CUT method, not a
keep-newest-N cut: queue.md interleaves standing `- [ ]` open items among
completed `- [x]` cycle blocks (here one at line 97, buried between the second
2289 block and the 2287 block), so a naive cut by line number silently deletes
live open work.

  1. Keep the DONE blocks matching the live STATUS.md window (2288..2291). As at
     2268 these ARE a single contiguous prefix -- lines 1-96, asserted below --
     even though the blocks inside it are NOT in cycle order (2290, 2291, 2288,
     2289, 2289: five block entries for four cycles, because c2289 wrote two).
     That ordering does not matter for queue.md, which has no continuity checker.
  2. Hoist the 7 genuinely-live open items verbatim after the kept blocks:
       - c2289 code+copy process lesson                      (97-101)
       - c2276 tool-page CTA measurement                     (501-524)
       - c2272 llms-full.txt fetch check                     (641-655)
       - c2196 ack-staleness warning proposal                (1047-1054)
       - c2168/c2268 revenue-trigger decision rule           (1056-1074)
       - c2103 DMARC recheck, blocked externally             (1076-1081)
       - c2120 re-verify-due-lists process lesson            (1083-1086)
     That is ALL seven `- [ ]` items in the file (asserted) -- nothing is
     archived as closed this time, and there is no `- [ ] NEXT (cycle N ...)`
     handoff item to discharge. The five items c2268 hoisted are now seven
     because c2272/c2276/c2289 each added one and the c2260 same-number-checker
     proposal was closed by a cycle since (its closure lives in a DONE block).
  3. Archive everything else verbatim to tasks/queue_archive.md, in original
     order.

Live lands at 14.8KB, ~20KB once c2292 prepends its own block.

RATE, re-measured as c2268's script asked rather than re-derived: c2268 left
21.4KB live and the file reached 88.9KB over the 23 blocks added since,
i.e. ~2.93KB/cycle actual against check-doc-size's
+5440 B/cycle (5.31KB). The checker runs ~81% HOT on this file. Four independent
measurements now agree the real rate is 2.9-3.9KB/cycle (3.75 at c2220, 3.3 at
c2268, 2.93 here), and all four are far below the checker's figure, so the
measured rate is used: this trim projects ~85KB at cycle 2316, comfortably under
the 150KB warn line (at the checker's pessimistic rate it would be 142KB, still
under). Next trim: measure again before trusting either number.

Verifies losslessly before writing anything.
"""
import sys

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 1087, f"expected 1087 lines, got {len(lines)} -- file changed, abort"

# 1-indexed inclusive ranges, pinned by inspection this cycle.
KEPT_BLOCKS = [(1, 96)]        # contiguous prefix: 2290, 2291, 2288, 2289, 2289
HOISTED = [(97, 101), (501, 524), (641, 655),
           (1047, 1054), (1056, 1074), (1076, 1081), (1083, 1086)]


def seg(a, b):
    """1-indexed inclusive line range -> list of lines."""
    return lines[a - 1:b]


# --- Preconditions: every pinned boundary is what this script thinks it is ---
for cyc, a in zip((2290, 2291, 2288, 2289, 2289), (1, 28, 54, 73, 77)):
    assert seg(a, a)[0].startswith(f"- [x] **DONE cycle {cyc}"), f"block {cyc} moved from {a}"
assert seg(103, 103)[0].startswith("- [x] **DONE cycle 2287"), \
    "the first archived block is not 2287 -- prefix boundary moved"

for name, rng, prefix in [
    ("code+copy", (97, 101), "- [ ] **Process lesson to apply on any cycle that changes BOTH"),
    ("cta", (501, 524), "- [ ] **NEW follow-up (c2276) -- MEASURE the tool-page CTA fix"),
    ("llms-full", (641, 655), "- [ ] **NEW follow-up (c2272) -- in ~1-2 days"),
    ("ack-stale", (1047, 1054), "- [ ] **NEW follow-up (c2196) -- consider an ack STALENESS"),
    ("revenue-trigger", (1056, 1074), "- [ ] **NEW follow-up (c2168, REWRITTEN c2268"),
    ("DMARC", (1076, 1081), "- [ ] **STILL OPEN (carried from c2103"),
    ("lesson", (1083, 1086), "- [ ] **Process lesson to apply every cycle (found c2120)"),
]:
    assert seg(*rng)[0].startswith(prefix), f"{name} range moved"
    # each hoisted range must carry the whole item, i.e. not end on a blank line
    assert seg(*rng)[-1].strip() != "", f"{name} range includes a trailing blank"

kept_idx = {i for a, b in KEPT_BLOCKS for i in range(a, b + 1)}
hoisted_idx = {i for a, b in HOISTED for i in range(a, b + 1)}
assert not (kept_idx & hoisted_idx), "a kept block overlaps a hoisted item"

# Exactly the 7 open items this script knows about, and no others.
open_idx = [i for i, l in enumerate(lines, 1) if l.startswith("- [ ] ")]
assert open_idx == [97, 501, 641, 1047, 1056, 1076, 1083], f"open-item set changed: {open_idx}"
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
    "\n## Archived by cycle 2292 (opus-5), 2026-10-26 -- tasks/queue.md had grown to 1087 lines "
    "/ 88.9KB. NOT trim-due today: check-doc-size read TRIM SOON (~21 cycles of headroom at "
    "+5440 B/cycle) but projected ~216KB at its own next look (24c, cycle 2316), past both the "
    "warn and trim lines BETWEEN looks -- trimmed in the same QUALITY-slot pass as this cycle's "
    "STATUS.md trim. The live file keeps the DONE blocks matching the live STATUS.md window "
    "(2288..2291 -- a single contiguous prefix, lines 1-96, holding FIVE block entries for four "
    "cycles because c2289 wrote two, and not in cycle order: 2290, 2291, 2288, 2289, 2289) plus "
    "ALL 7 genuinely-live open items, which were HOISTED (c2289 code+copy process lesson, c2276 "
    "tool-page CTA measurement, c2272 llms-full.txt fetch check, c2196 ack-staleness proposal, "
    "c2168/c2268 revenue-trigger decision rule, c2103 DMARC recheck, c2120 re-verify-due-lists "
    "lesson). Everything else moved here verbatim, in original order. NOTHING below is archived "
    "as closed-but-unchecked this time: there was no `- [ ] NEXT (cycle N ...)` handoff item and "
    "no duplicate, so every `- [ ]` item in the source file is still live. The five items c2268 "
    "hoisted are now seven because c2272/c2276/c2289 each added one and the c2260 "
    "same-number-stated-twice checker proposal was closed by a cycle since (closure recorded in "
    "a DONE block). Rate re-measured as c2268's script asked: it left 21.4KB and the file reached "
    "88.9KB over the 23 blocks added since, ~2.93KB/cycle actual vs the checker's +5440 B/cycle, "
    "so the checker runs ~81% HOT on this file -- four measurements now agree on 2.9-3.9KB/cycle "
    "(3.75 at c2220, 3.3 at c2268, 2.93 here), all far below the checker. This trim projects "
    "~85KB at cycle 2316 at the measured rate (142KB even at the checker's rate).\n\n"
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

# --- Verification 5: exactly the 7 hoisted items are live, and all 7 landed ---
live_open = [l for l in new_live if l.startswith("- [ ] ")]
if len(live_open) != 7:
    sys.exit(f"FAIL: expected 7 live open items, got {len(live_open)}")
for a, b in HOISTED:
    if lines[a - 1] not in live_text:
        sys.exit(f"FAIL: hoisted item {a} did not land in the live file")

# --- Verification 6: the kept DONE blocks are exactly the STATUS window 2288..2291 ---
kept_blocks = sorted(int(l.split("DONE cycle ")[1].split()[0])
                     for l in new_live if l.startswith("- [x] **DONE cycle"))
if kept_blocks != [2288, 2289, 2289, 2290, 2291]:
    sys.exit(f"FAIL: kept blocks are not 2288/2289/2289/2290/2291: {kept_blocks}")

print("All 6 verifications passed. Writing files.")
with open(SRC, "w") as f:
    f.write(live_text)
with open(ARCHIVE, "w") as f:
    f.write(new_archive)
print(f"live queue.md:     {len(new_live)} lines / {len(live_text.encode())} bytes "
      f"({len(live_text.encode())/1024:.1f}KB)")
print(f"archive addition:  {len(archived)} lines")
print(f"open items live:   {len(live_open)}  (0 archived as closed)")
