#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2316 (75.0KB / 912 lines).

Same trigger as this cycle's STATUS.md trim (bin/_trim2316.py): check-doc-size
reads TRIM SOON -- ~24 cycles of headroom today at +5440 B/cycle, but ~203KB
projected at its own next look (24c, cycle 2340), past both the warn and trim
lines BETWEEN looks. Trimmed in the same QUALITY-slot pass (`2316%3==0`).

Uses the c2161/c2196/c2220/c2244/c2268/c2292 HOIST-THEN-CUT method, not a
keep-newest-N cut: queue.md interleaves standing `- [ ]` open items among
completed `- [x]` cycle blocks (here one at line 117, buried between the 2312
block and the 2314 block), so a naive cut by line number silently deletes live
open work.

  1. Keep the DONE blocks matching the live STATUS.md window (2312..2315). As at
     2292 these are NOT a single contiguous prefix: the c2312 open item sits at
     117-123, between the 2312 block (83-115) and the 2314 block (125-181). The
     blocks inside the window are also not in cycle order (2315, 2313, 2312,
     2314), which does not matter for queue.md -- it has no continuity checker.
  2. Hoist the 8 genuinely-live open items verbatim after the kept blocks:
       - c2312 scholarship-scraper unpushed fix              (117-123)
       - c2289 code+copy process lesson                      (820-824)
       - c2276 tool-page CTA measurement                     (826-849)
       - c2272/c2307 llms-full.txt fetch check               (851-870)
       - c2196 ack-staleness warning proposal                (872-879)
       - c2168/c2268 revenue-trigger decision rule           (881-899)
       - c2103 DMARC recheck, blocked externally             (901-906)
       - c2120 re-verify-due-lists process lesson            (908-911)
     That is ALL eight `- [ ]` items in the file (asserted) -- nothing is
     archived as closed this time, and there is no `- [ ] NEXT (cycle N ...)`
     handoff item to discharge. The seven items c2292 hoisted are now eight
     because c2312 added one (the unpushed scholarship-scraper fix) and no open
     item has been closed since.
  3. Archive everything else verbatim to tasks/queue_archive.md, in original
     order.

Live lands at 22.9KB, ~28KB once c2316 prepends its own block. (The first draft
of this docstring estimated ~19KB; the kept c2314 block is the single largest in
the file at 57 lines, which accounts for the difference.)

RATE, re-measured as c2292's script asked rather than re-derived: c2292 left
14.8KB live and the file reached 75.0KB over the 23 blocks added since, i.e.
~2.62KB/cycle actual against check-doc-size's +5440 B/cycle (5.31KB). The
checker runs ~103% HOT on this file. Five independent measurements now agree the
real rate is 2.6-3.9KB/cycle (3.75 at c2220, 3.3 at c2268, 2.93 at c2292, 2.62
here), and all five are far below the checker's figure, so the measured rate is
used: this trim projects ~86KB at cycle 2340, comfortably under the 150KB warn
line. At the checker's own pessimistic rate it would be 150KB -- right ON the
warn line, which is exactly why the measured rate matters on this file. Next
trim: measure again before trusting either number.

Verifies losslessly before writing anything.
"""
import sys

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 912, f"expected 912 lines, got {len(lines)} -- file changed, abort"

# 1-indexed inclusive ranges, pinned by inspection this cycle.
KEPT_BLOCKS = [(1, 115), (125, 181)]   # 2315, 2313, 2312 | 2314
HOISTED = [(117, 123), (820, 824), (826, 849), (851, 870),
           (872, 879), (881, 899), (901, 906), (908, 911)]


def seg(a, b):
    """1-indexed inclusive line range -> list of lines."""
    return lines[a - 1:b]


# --- Preconditions: every pinned boundary is what this script thinks it is ---
for cyc, a in zip((2315, 2313, 2312, 2314), (1, 41, 83, 125)):
    assert seg(a, a)[0].startswith(f"- [x] **DONE cycle {cyc}"), f"block {cyc} moved from {a}"
assert seg(183, 183)[0].startswith("- [x] **DONE cycle 2308"), \
    "the first archived block is not 2308 -- kept-window boundary moved"

for name, rng, prefix in [
    ("scholarship", (117, 123), "- [ ] **NEW follow-up (c2312) -- `scholarship-scraper`"),
    ("code+copy", (820, 824), "- [ ] **Process lesson to apply on any cycle that changes BOTH"),
    ("cta", (826, 849), "- [ ] **NEW follow-up (c2276) -- MEASURE the tool-page CTA fix"),
    ("llms-full", (851, 870), "- [ ] **NEW follow-up (c2272, RE-CHECKED interim at c2307"),
    ("ack-stale", (872, 879), "- [ ] **NEW follow-up (c2196) -- consider an ack STALENESS"),
    ("revenue-trigger", (881, 899), "- [ ] **NEW follow-up (c2168, REWRITTEN c2268"),
    ("DMARC", (901, 906), "- [ ] **STILL OPEN (carried from c2103"),
    ("lesson", (908, 911), "- [ ] **Process lesson to apply every cycle (found c2120)"),
]:
    assert seg(*rng)[0].startswith(prefix), f"{name} range moved"
    # each hoisted range must carry the whole item, i.e. not end on a blank line
    assert seg(*rng)[-1].strip() != "", f"{name} range includes a trailing blank"

kept_idx = {i for a, b in KEPT_BLOCKS for i in range(a, b + 1)}
hoisted_idx = {i for a, b in HOISTED for i in range(a, b + 1)}
assert not (kept_idx & hoisted_idx), "a kept block overlaps a hoisted item"

# Exactly the 8 open items this script knows about, and no others.
open_idx = [i for i, l in enumerate(lines, 1) if l.startswith("- [ ] ")]
assert open_idx == [117, 820, 826, 851, 872, 881, 901, 908], \
    f"open-item set changed: {open_idx}"
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
    "\n## Archived by cycle 2316 (opus-5), 2026-10-27 -- tasks/queue.md had grown to 912 lines "
    "/ 75.0KB. NOT trim-due today: check-doc-size read TRIM SOON (~24 cycles of headroom at "
    "+5440 B/cycle) but projected ~203KB at its own next look (24c, cycle 2340), past both the "
    "warn and trim lines BETWEEN looks -- trimmed in the same QUALITY-slot pass as this cycle's "
    "STATUS.md trim. The live file keeps the DONE blocks matching the live STATUS.md window "
    "(2312..2315), which as at 2292 are NOT a contiguous prefix: the c2312 open item sits at "
    "117-123, between the 2312 block and the 2314 block, and the window's blocks are not in "
    "cycle order (2315, 2313, 2312, 2314). ALL 8 genuinely-live open items were HOISTED (c2312 "
    "scholarship-scraper unpushed fix, c2289 code+copy process lesson, c2276 tool-page CTA "
    "measurement, c2272/c2307 llms-full.txt fetch check, c2196 ack-staleness proposal, "
    "c2168/c2268 revenue-trigger decision rule, c2103 DMARC recheck, c2120 re-verify-due-lists "
    "lesson). Everything else moved here verbatim, in original order. NOTHING below is archived "
    "as closed-but-unchecked this time: there was no `- [ ] NEXT (cycle N ...)` handoff item and "
    "no duplicate, so every `- [ ]` item in the source file is still live. The seven items c2292 "
    "hoisted are now eight because c2312 added one and no open item has been closed since. Rate "
    "re-measured as c2292's script asked: it left 14.8KB and the file reached 75.0KB over the 23 "
    "blocks added since, ~2.62KB/cycle actual vs the checker's +5440 B/cycle, so the checker "
    "runs ~103% HOT on this file -- five measurements now agree on 2.6-3.9KB/cycle (3.75 at "
    "c2220, 3.3 at c2268, 2.93 at c2292, 2.62 here), all far below the checker. This trim "
    "projects ~82KB at cycle 2340 at the measured rate (146KB even at the checker's rate).\n\n"
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

# --- Verification 5: exactly the 8 hoisted items are live, and all 8 landed ---
live_open = [l for l in new_live if l.startswith("- [ ] ")]
if len(live_open) != 8:
    sys.exit(f"FAIL: expected 8 live open items, got {len(live_open)}")
for a, b in HOISTED:
    if lines[a - 1] not in live_text:
        sys.exit(f"FAIL: hoisted item {a} did not land in the live file")

# --- Verification 6: the kept DONE blocks are exactly the STATUS window 2312..2315 ---
kept_blocks = sorted(int(l.split("DONE cycle ")[1].split()[0])
                     for l in new_live if l.startswith("- [x] **DONE cycle"))
if kept_blocks != [2312, 2313, 2314, 2315]:
    sys.exit(f"FAIL: kept blocks are not 2312/2313/2314/2315: {kept_blocks}")

print("All 6 verifications passed. Writing files.")
with open(SRC, "w") as f:
    f.write(live_text)
with open(ARCHIVE, "w") as f:
    f.write(new_archive)
print(f"live queue.md:     {len(new_live)} lines / {len(live_text.encode())} bytes "
      f"({len(live_text.encode())/1024:.1f}KB)")
print(f"archive addition:  {len(archived)} lines")
print(f"open items live:   {len(live_open)}  (0 archived as closed)")
