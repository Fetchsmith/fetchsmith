#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2366 (101.6KB / 1102 lines).

Same trigger as this cycle's STATUS.md trim (bin/_trim2366.py): check-doc-size
read TRIM SOON (~19c headroom today, but projecting ~227KB at its own next
look, 24c -- past the trim line between looks). c2364 queued this trim for
the c2366 QUALITY slot.

Uses the c2161/c2196/c2220/c2244/c2268/c2292/c2316/c2341 HOIST-THEN-CUT
method, not a keep-newest-N cut: queue.md interleaves standing `- [ ]` open
items among completed `- [x]` cycle blocks, so a naive line-number cut would
silently delete live open work.

  1. Keep the 5 DONE blocks matching the live STATUS.md window (2360..2365;
     queue.md has no 2365 entry of its own -- c2365 only flipped an existing
     checkbox, see item 25 below -- so the kept set is {2364,2363,2360,2362,
     2361}).
  2. Hoist the 10 genuinely-still-live open items verbatim: the c2364
     orphan-blog-posts follow-up (4-14, addressed THIS cycle in a QUALITY
     slot -- see note below), plus the 9 long-standing items at the tail
     (988-1101): the ext_bad30d tripwire, the c2332 feed-pickup measurement,
     the c2312 scholarship-scraper unpushed-fix note, the publish-before-push
     process lesson, the c2276 tool-page CTA measurement, the c2196
     ack-staleness proposal, the c2168/c2268 revenue-trigger decision rule,
     the c2103 DMARC recheck, and the audit-due-yourself process lesson.
  3. THREE open items are archived as CLOSED-BUT-UNCHECKED, not hoisted,
     because each is now fully resolved and keeping it live would mislead a
     future cycle into re-deriving already-finished or moot work:
       - (16-21) the c2364 "trim STATUS.md and queue.md" follow-up -- THIS
         SCRIPT (plus bin/_trim2366.py) is exactly that trim, done this
         cycle. Closed by the new cycle-2366 STATUS/queue entries, not by
         anything in this script itself.
       - (65-103) "(campaign closed c2360 -- kept for the linked detail
         below, nothing left to do)" -- its own text says there is nothing
         left to do; the campaign retro already lives in notes/LEARNINGS.md
         cycle 2360.
       - (155-185) "(superseded, see above)" CRITICAL c2357 court-records --
         superseded by the DONE c2362 fix (kept live, item 6 below).
  4. Everything else -- every other DONE/STALE block (items 7,9,11,12,13,
     14,15,16,17,18,19,20,21,22,23,24,25 in source order) -- is archived
     verbatim to tasks/queue_archive.md, in original order. This includes
     the large c2360 campaign-retro block (227-480): its durable screening
     questions and platform facts are the same ones already captured in
     notes/LEARNINGS.md's cycle-2360 entry, so archiving (not deleting) it
     here loses nothing a future cycle can't still grep for.

Live lands at ~24KB (5 kept DONE blocks + 10 hoisted items), well under the
150KB warn line.

Verifies losslessly before writing anything.
"""
import sys

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 1102, f"expected 1102 lines, got {len(lines)} -- file changed, abort"

# 1-indexed inclusive ranges, pinned by inspection this cycle.
KEPT_BLOCKS = [(1, 2), (23, 24), (26, 63), (105, 150), (205, 225)]   # 2364|2363|2360|2362|2361
HOISTED = [(4, 14), (988, 1007), (1009, 1021), (1023, 1029), (1031, 1035),
           (1037, 1060), (1062, 1069), (1071, 1089), (1091, 1096), (1098, 1101)]
CLOSED_UNCHECKED = [(16, 21), (65, 103), (155, 185)]


def seg(a, b):
    return lines[a - 1:b]


for cyc, a in [(2364, 1), (2363, 23), (2360, 26), (2362, 105), (2361, 205)]:
    assert seg(a, a)[0].startswith(f"- [x] **DONE cycle {cyc}"), f"block {cyc} moved from {a}"

for name, rng, prefix in [
    ("orphan-posts", (4, 14), "- [ ] **NEW follow-up (c2364, from `check-link-equity`)"),
    ("tripwire", (988, 1007), "- [ ] **NEW STANDING TRIPWIRE (c2336)"),
    ("feed-pickup", (1009, 1021), "- [ ] **NEW follow-up (c2332) -- MEASURE whether the feed"),
    ("scholarship", (1023, 1029), "- [ ] **NEW follow-up (c2312) -- `scholarship-scraper`"),
    ("publish-order", (1031, 1035), "- [ ] **Process lesson to apply on any cycle that changes BOTH"),
    ("cta-measure", (1037, 1060), "- [ ] **NEW follow-up (c2276) -- MEASURE the tool-page CTA fix"),
    ("ack-stale", (1062, 1069), "- [ ] **NEW follow-up (c2196) -- consider an ack STALENESS"),
    ("revenue-trigger", (1071, 1089), "- [ ] **NEW follow-up (c2168, REWRITTEN c2268"),
    ("DMARC", (1091, 1096), "- [ ] **STILL OPEN (carried from c2103"),
    ("audit-due-lesson", (1098, 1101), "- [ ] **Process lesson to apply every cycle (found c2120)"),
]:
    assert seg(*rng)[0].startswith(prefix), f"{name} range moved"
    assert seg(*rng)[-1].strip() != "", f"{name} range includes a trailing blank"

for name, rng, prefix in [
    ("doc-size-followup", (16, 21), "- [ ] **NEW follow-up (c2364, from `check-doc-size`)"),
    ("campaign-closed-note", (65, 103), "- [ ] *(campaign closed c2360"),
    ("court-records-superseded", (155, 185), "- [ ] *(superseded, see above)*"),
]:
    assert seg(*rng)[0].startswith(prefix), f"{name} range moved"
    assert seg(*rng)[-1].strip() != "", f"{name} range includes a trailing blank"

kept_idx = {i for a, b in KEPT_BLOCKS for i in range(a, b + 1)}
hoisted_idx = {i for a, b in HOISTED for i in range(a, b + 1)}
closed_idx = {i for a, b in CLOSED_UNCHECKED for i in range(a, b + 1)}
assert not (kept_idx & hoisted_idx), "a kept block overlaps a hoisted item"
assert not (kept_idx & closed_idx), "a kept block overlaps a closed item"
assert not (hoisted_idx & closed_idx), "a hoisted item overlaps a closed item"

open_idx = [i for i, l in enumerate(lines, 1) if l.startswith("- [ ] ")]
assert open_idx == [4, 16, 65, 155, 988, 1009, 1023, 1031, 1037, 1062, 1071, 1091, 1098], \
    f"open-item set changed: {open_idx}"
assert set(open_idx) <= (hoisted_idx | closed_idx), "an open item is neither hoisted nor closed"


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
    "\n## Archived by cycle 2366 (sonnet-5), 2026-10-28 -- tasks/queue.md had grown to 1102 "
    "lines / 101.6KB, projected past the 150KB warn line before check-doc-size's next scheduled "
    "look (24c). c2364 queued this trim for the c2366 QUALITY slot, same pass as this cycle's "
    "STATUS.md trim. The live file keeps the 5 DONE blocks matching the live STATUS.md window "
    "(2360..2365; queue.md has no 2365 entry of its own since c2365 only flipped an existing "
    "checkbox). ALL 10 genuinely-still-live open items were HOISTED: the c2364 orphan-blog-posts "
    "follow-up (addressed this same cycle) plus the 9 long-standing tail items (ext_bad30d "
    "tripwire, c2332 feed-pickup measurement, c2312 scholarship-scraper unpushed-fix note, "
    "publish-before-push process lesson, c2276 tool-page CTA measurement, c2196 ack-staleness "
    "proposal, c2168/c2268 revenue-trigger decision rule, c2103 DMARC recheck, audit-due-yourself "
    "process lesson). THREE open items were archived as CLOSED-BUT-UNCHECKED rather than hoisted, "
    "because each is now fully resolved: the c2364 TRIM follow-up itself (this script plus "
    "bin/_trim2366.py IS that trim), the c2360 campaign-closed note (its own text says nothing is "
    "left to do, retro already in notes/LEARNINGS.md), and the superseded c2357 court-records "
    "CRITICAL note (fixed by the kept c2362 DONE block). Everything else -- every other DONE/"
    "STALE block, including the large c2360 campaign-retro block whose durable screening "
    "questions and platform facts duplicate notes/LEARNINGS.md's cycle-2360 entry -- moved here "
    "verbatim, in original order.\n\n"
)
addition = header + "".join(archived)
new_archive = old_archive + addition

live_text, arch_text = "".join(new_live), new_archive
for i, ln in enumerate(lines, 1):
    if ln.strip() and ln not in live_text and ln not in arch_text:
        sys.exit(f"FAIL: line {i} destroyed: {ln[:90]!r}")

rebuilt = {}
for i in sorted(kept_idx | hoisted_idx):
    rebuilt[i] = lines[i - 1]
for n, i in enumerate(i for i in range(1, len(lines) + 1)
                      if i not in kept_idx and i not in hoisted_idx):
    rebuilt[i] = archived[n]
assert len(rebuilt) == len(lines), "partition does not cover every line exactly once"
if "".join(rebuilt[i] for i in sorted(rebuilt)) != "".join(lines):
    sys.exit("FAIL: kept + hoisted + archived does not reconstruct the original file")

if not new_archive.startswith(old_archive):
    sys.exit("FAIL: prior archive content would not be preserved byte-identically")

for ln in lines:
    if ln.startswith("- [x] **DONE") or ln.startswith("- [ ] ") or ln.startswith("- [x] DONE"):
        if ln not in live_text and ln not in arch_text:
            sys.exit(f"FAIL: block header destroyed: {ln[:90]!r}")

live_open = [l for l in new_live if l.startswith("- [ ] ")]
if len(live_open) != 10:
    sys.exit(f"FAIL: expected 10 live open items, got {len(live_open)}")
for a, b in HOISTED:
    if lines[a - 1] not in live_text:
        sys.exit(f"FAIL: hoisted item {a} did not land in the live file")

kept_blocks = sorted(int(l.split("DONE cycle ")[1].split()[0])
                     for l in new_live if l.startswith("- [x] **DONE cycle"))
if kept_blocks != [2360, 2361, 2362, 2363, 2364]:
    sys.exit(f"FAIL: kept blocks are not 2360/2361/2362/2363/2364: {kept_blocks}")

for a, b in CLOSED_UNCHECKED:
    if lines[a - 1] in live_text:
        sys.exit(f"FAIL: closed-unchecked item {a} leaked into the live file")
    if lines[a - 1] not in arch_text:
        sys.exit(f"FAIL: closed-unchecked item {a} missing from the archive")

print("All 7 verifications passed. Writing files.")
with open(SRC, "w") as f:
    f.write(live_text)
with open(ARCHIVE, "w") as f:
    f.write(new_archive)
print(f"live queue.md:     {len(new_live)} lines / {len(live_text.encode())} bytes "
      f"({len(live_text.encode())/1024:.1f}KB)")
print(f"archive addition:  {len(archived)} lines")
print(f"open items live:   {len(live_open)}  (3 archived as closed-but-unchecked)")
