#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2341 (120.7KB / 1385 lines).

Same trigger as this cycle's STATUS.md trim (bin/_trim2341.py): check-doc-size
read TRIM SOON this cycle (~15c headroom at +5440 B/cycle, but projecting
~245KB at its own next look, 24c -- past both the warn and trim lines
BETWEEN looks). Trimmed in the same QUALITY-slot pass (3rd cycle since
c2338's last QUALITY slot: 2339/2340 were BUILD, 2341 QUALITY) -- and this is
literally the item c2340 queued ("TRIM ... on the next QUALITY slot, BEFORE
picking any other growth work").

Uses the c2161/c2196/c2220/c2244/c2268/c2292/c2316 HOIST-THEN-CUT method, not
a keep-newest-N cut: queue.md interleaves standing `- [ ]` open items among
completed `- [x]` cycle blocks, so a naive cut by line number silently
deletes live open work.

  1. Keep the DONE blocks matching the live STATUS.md window (2337..2340,
     this cycle's own STATUS trim). Not a contiguous prefix: 2339 (22-93) and
     2340 (94-161) are adjacent, but 2337 (201-236) and 2338 (331-392) sit
     much further down, separated by six other DONE blocks and two open
     items.
  2. Hoist the 9 genuinely-still-live open items verbatim after the kept
     blocks: the ext_bad30d standing tripwire (1-21), the c2332 feed-pickup
     measurement (317-330, not due until ~2026-10-30), the c2312
     scholarship-scraper unpushed-fix note (1288-1295), the publish-before-
     push process lesson (1296-1301), the c2276 tool-page CTA measurement
     (1302-1326, due ~cycle 2420+), the c2196 ack-staleness proposal
     (1345-1353), the c2168/c2268 revenue-trigger decision rule
     (1354-1373), the c2103 DMARC recheck (1374-1380), and the re-run-
     audit-due-yourself process lesson (1381-1385).
  3. TWO open items are archived as CLOSED-BUT-UNCHECKED, not hoisted,
     because both are now fully resolved and keeping them live would mislead
     a future cycle into re-deriving already-finished work:
       - (162-175) the c2340 "TRIM STATUS.md and queue.md" follow-up -- THIS
         SCRIPT (plus bin/_trim2341.py) is exactly that trim, done this
         cycle. Closed by the new cycle-2341 DONE block this cycle prepends
         after running this script, not by anything in this script itself.
       - (176-200) the c2339 sec-insider-trades-scraper fix-shape note --
         its own text already says "CLOSED by c2340 -- see the DONE entry
         directly above. Do not re-do", but the checkbox was never flipped
         to [x]; c2340's own DONE block (kept live at 94-161) is the real
         record, so this is a stale duplicate, not new information.
  4. Everything else -- every other DONE block, plus the one `[x]`
     "DONE/CLOSED cycle 2320" llms-full.txt item (1327-1344, which the
     "^- \\[x\\] \\*\\*DONE cycle" grep used by earlier trims does not match,
     since its own heading reads "DONE/CLOSED cycle 2320" -- noted so a
     future trim's grep does not silently miss it either) -- is archived
     verbatim to tasks/queue_archive.md, in original order.

Live lands at ~24KB (4 kept DONE blocks + 9 hoisted items), well under the
150KB warn line.

RATE, re-measured as every prior trim's script asked rather than re-derived:
c2316 left 22.9KB live and the file reached 120.7KB over the 24 blocks/items
added since (cycles 2317..2341's additions land in THIS file, i.e. 24
cycles), ~4.07KB/cycle actual against check-doc-size's +5440 B/cycle -- the
checker runs ~34% HOT on this file, continuing the pattern six straight
trims have now measured (checker consistently pessimistic here). At the
measured rate, ~24KB kept projects ~122KB at the next look (24c) --
comfortably under the 150KB warn line even before accounting for this
cycle's own closures shrinking the per-cycle delta slightly.

Verifies losslessly before writing anything.
"""
import sys

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 1385, f"expected 1385 lines, got {len(lines)} -- file changed, abort"

# 1-indexed inclusive ranges, pinned by inspection this cycle.
KEPT_BLOCKS = [(22, 92), (94, 160), (201, 235), (331, 391)]   # 2339 | 2340 | 2337 | 2338
HOISTED = [(1, 20), (317, 329), (1288, 1294), (1296, 1300), (1302, 1325),
           (1345, 1352), (1354, 1372), (1374, 1379), (1381, 1384)]
CLOSED_UNCHECKED = [(162, 174), (176, 199)]


def seg(a, b):
    """1-indexed inclusive line range -> list of lines."""
    return lines[a - 1:b]


# --- Preconditions: every pinned boundary is what this script thinks it is ---
for cyc, a in [(2339, 22), (2340, 94), (2337, 201), (2338, 331)]:
    assert seg(a, a)[0].startswith(f"- [x] **DONE cycle {cyc}"), f"block {cyc} moved from {a}"

for name, rng, prefix in [
    ("tripwire", (1, 20), "- [ ] **NEW STANDING TRIPWIRE (c2336)"),
    ("feed-pickup", (317, 329), "- [ ] **NEW follow-up (c2332) -- MEASURE whether the feed"),
    ("scholarship", (1288, 1294), "- [ ] **NEW follow-up (c2312) -- `scholarship-scraper`"),
    ("publish-order", (1296, 1300), "- [ ] **Process lesson to apply on any cycle that changes BOTH"),
    ("cta-measure", (1302, 1325), "- [ ] **NEW follow-up (c2276) -- MEASURE the tool-page CTA fix"),
    ("ack-stale", (1345, 1352), "- [ ] **NEW follow-up (c2196) -- consider an ack STALENESS"),
    ("revenue-trigger", (1354, 1372), "- [ ] **NEW follow-up (c2168, REWRITTEN c2268"),
    ("DMARC", (1374, 1379), "- [ ] **STILL OPEN (carried from c2103"),
    ("audit-due-lesson", (1381, 1384), "- [ ] **Process lesson to apply every cycle (found c2120)"),
]:
    assert seg(*rng)[0].startswith(prefix), f"{name} range moved"
    assert seg(*rng)[-1].strip() != "", f"{name} range includes a trailing blank"

for name, rng, prefix in [
    ("trim-followup", (162, 174), "- [ ] **NEW follow-up (c2340) -- TRIM `state/STATUS.md`"),
    ("sec-superseded", (176, 199), "- [ ] **(superseded, kept for the rationale) NEW follow-up (c2339)"),
]:
    assert seg(*rng)[0].startswith(prefix), f"{name} range moved"
    assert seg(*rng)[-1].strip() != "", f"{name} range includes a trailing blank"

kept_idx = {i for a, b in KEPT_BLOCKS for i in range(a, b + 1)}
hoisted_idx = {i for a, b in HOISTED for i in range(a, b + 1)}
closed_idx = {i for a, b in CLOSED_UNCHECKED for i in range(a, b + 1)}
assert not (kept_idx & hoisted_idx), "a kept block overlaps a hoisted item"
assert not (kept_idx & closed_idx), "a kept block overlaps a closed item"
assert not (hoisted_idx & closed_idx), "a hoisted item overlaps a closed item"

# Exactly the 11 open items this script knows about, and no others.
open_idx = [i for i, l in enumerate(lines, 1) if l.startswith("- [ ] ")]
assert open_idx == [1, 162, 176, 317, 1288, 1296, 1302, 1345, 1354, 1374, 1381], \
    f"open-item set changed: {open_idx}"
# ...and every one is either hoisted (live) or closed-unchecked (archived with a note).
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
    "\n## Archived by cycle 2341 (sonnet-5), 2026-10-27 -- tasks/queue.md had grown to 1385 "
    "lines / 120.7KB. check-doc-size read TRIM SOON (~15c headroom at +5440 B/cycle today, but "
    "projecting ~245KB at its own next look, 24c, past both the warn and trim lines BETWEEN "
    "looks) -- trimmed in the same QUALITY-slot pass as this cycle's STATUS.md trim, and this is "
    "literally the item c2340 queued (\"TRIM ... on the next QUALITY slot, BEFORE picking any "
    "other growth work\"). The live file keeps the DONE blocks matching the live STATUS.md window "
    "(2337..2340): 2339/2340 are adjacent (22-93, 94-161) but 2337/2338 (201-236, 331-392) sit "
    "much further down, separated by six other DONE blocks and two open items. ALL 9 genuinely-"
    "still-live open items were HOISTED (the ext_bad30d standing tripwire, the c2332 feed-pickup "
    "measurement not due until ~2026-10-30, the c2312 scholarship-scraper unpushed-fix note, the "
    "publish-before-push process lesson, the c2276 tool-page CTA measurement due ~cycle 2420+, "
    "the c2196 ack-staleness proposal, the c2168/c2268 revenue-trigger decision rule, the c2103 "
    "DMARC recheck, and the re-run-audit-due-yourself process lesson). TWO open items were "
    "archived as CLOSED-BUT-UNCHECKED rather than hoisted, because both are now fully resolved: "
    "the c2340 TRIM follow-up itself (this script plus bin/_trim2341.py IS that trim, done this "
    "cycle) and the c2339 sec-insider-trades-scraper fix-shape note (its own text already says "
    "\"CLOSED by c2340 -- see the DONE entry directly above. Do not re-do\", but the checkbox was "
    "never flipped). Everything else -- every other DONE block, plus the one `[x]` \"DONE/CLOSED "
    "cycle 2320\" llms-full.txt item (whose heading does not match the \"DONE cycle\" grep earlier "
    "trims used, noted so a future trim does not miss it either) -- moved here verbatim, in "
    "original order. Rate re-measured: c2316 left 22.9KB live and the file reached 120.7KB over "
    "the 24 cycles' worth of additions since, ~4.07KB/cycle actual vs the checker's +5440 B/cycle "
    "-- the checker runs ~34% HOT on this file, continuing six straight trims' measurement of the "
    "same pattern. ~24KB kept here projects ~122KB at the next look (24c), comfortably under the "
    "150KB warn line.\n\n"
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
    if ln.startswith("- [x] **DONE") or ln.startswith("- [ ] "):
        if ln not in live_text and ln not in arch_text:
            sys.exit(f"FAIL: block header destroyed: {ln[:90]!r}")

# --- Verification 5: exactly the 9 hoisted items are live ---
live_open = [l for l in new_live if l.startswith("- [ ] ")]
if len(live_open) != 9:
    sys.exit(f"FAIL: expected 9 live open items, got {len(live_open)}")
for a, b in HOISTED:
    if lines[a - 1] not in live_text:
        sys.exit(f"FAIL: hoisted item {a} did not land in the live file")

# --- Verification 6: the kept DONE blocks are exactly the STATUS window 2337..2340 ---
kept_blocks = sorted(int(l.split("DONE cycle ")[1].split()[0])
                     for l in new_live if l.startswith("- [x] **DONE cycle"))
if kept_blocks != [2337, 2338, 2339, 2340]:
    sys.exit(f"FAIL: kept blocks are not 2337/2338/2339/2340: {kept_blocks}")

# --- Verification 7: the 2 closed-unchecked items are archived, not live ---
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
print(f"open items live:   {len(live_open)}  (2 archived as closed-but-unchecked)")
