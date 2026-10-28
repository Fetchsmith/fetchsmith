#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2387 (77.6KB / 831 lines).

Same trigger as this cycle's STATUS.md trim (bin/_trim2387.py): check-doc-size
read TRIM SOON (~23c headroom today, but projecting ~205KB at its own next
look, 24c -- past the trim line between looks). check-doc-size itself
recommends trimming proactively in a QUALITY slot; 2387%3==2 is that slot.

Uses the c2161/c2196/c2220/c2244/c2268/c2292/c2316/c2341/c2366 HOIST-THEN-CUT
method, not a keep-newest-N cut: queue.md interleaves standing `- [ ]` open
items among completed `- [x]` cycle blocks, so a naive line-number cut would
silently delete live open work.

  1. Keep the 6 DONE blocks matching the live STATUS.md window (2382..2386;
     cycle 2385 has TWO separate DONE items -- the revisit-trigger grep and
     the sub-20-user-count regression check, both done in that cycle's BUILD
     slot -- so the kept set is {2386, 2385(x2), 2384, 2383, 2382}).
  2. Hoist the 13 genuinely-still-live open items verbatim, in source order:
     the c2385 sub-20 watch item, the c2383 scope-count standing method, the
     c2380 growing-niches follow-up, and the 9 long-standing tail items
     (dev.to c2368, ext_bad30d tripwire c2336, feed-pickup c2332, scholarship
     c2312, publish-before-push lesson, tool-page-CTA c2276, ack-staleness
     c2196, revenue-trigger c2168/c2268, DMARC-accumulate c2371) plus the
     audit-due-yourself process lesson c2120.
  3. TWO open items are archived as CLOSED-BUT-UNCHECKED, not hoisted,
     because each is now fully resolved and keeping it live would mislead a
     future cycle into re-deriving already-finished or moot work:
       - (68-76) the c2384 "trademark-search-scraper README is one word
         ahead of its build" note -- its own text says not to treat this as
         drift, the next build on that Actor for any other reason carries
         the word; nothing left to act on.
       - (628-654) the ORIGINAL c2376 follow-up spec, kept only for context
         after it was closed -- the kept c2386 DONE block (617-627) is the
         actual closure and already summarizes it; the long original spec
         duplicates detail that is now historical, not actionable.
  4. Everything else -- every other DONE block older than the kept window,
     including the long c2360 campaign-retro block (453-491, whose durable
     screening questions already live in notes/LEARNINGS.md's cycle-2360
     entry) and the old c2371 DMARC-receiver-fix DONE block (792-811) --
     moved here verbatim, in original order.

Live lands at ~26KB (6 kept DONE blocks + 13 hoisted items), well under the
150KB warn line.

Verifies losslessly before writing anything.
"""
import sys

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 831, f"expected 831 lines, got {len(lines)} -- file changed, abort"


def seg(a, b):
    return lines[a - 1:b]


# 1-indexed inclusive ranges, pinned by inspection this cycle.
KEPT_BLOCKS = [(1, 67), (77, 84), (85, 105), (114, 152), (162, 183), (617, 627)]
HOISTED = [(106, 112), (153, 160), (242, 275), (655, 672), (674, 693), (695, 707),
           (709, 730), (732, 736), (738, 761), (763, 770), (772, 790), (812, 825),
           (827, 830)]
CLOSED_UNCHECKED = [(68, 75), (628, 653)]

for cyc, a in [(2384, 1), (2385, 77), (2385, 85), (2383, 114), (2382, 162), (2386, 617)]:
    assert seg(a, a)[0].startswith(f"- [x] **DONE cycle {cyc}"), f"block {cyc} moved from {a}"

for name, rng, prefix in [
    ("sub20-watch", (106, 112), "- [ ] **NEW follow-up (c2385, low priority)"),
    ("scope-count-method", (153, 160), "- [ ] **STANDING METHOD (c2383)"),
    ("growing-niches", (242, 275), "- [ ] **FOLLOW-UP from c2380"),
    ("devto", (655, 672), "- [ ] **NEW follow-up (c2368)"),
    ("tripwire", (674, 693), "- [ ] **NEW STANDING TRIPWIRE (c2336)"),
    ("feed-pickup", (695, 707), "- [ ] **NEW follow-up (c2332)"),
    ("scholarship", (709, 730), "- [ ] **NEW follow-up (c2312)"),
    ("publish-order", (732, 736), "- [ ] **Process lesson to apply on any cycle that changes BOTH"),
    ("cta-measure", (738, 761), "- [ ] **NEW follow-up (c2276)"),
    ("ack-stale", (763, 770), "- [ ] **NEW follow-up (c2196)"),
    ("revenue-trigger", (772, 790), "- [ ] **NEW follow-up (c2168, REWRITTEN c2268"),
    ("DMARC", (812, 825), "- [ ] **NEW follow-up (c2371)"),
    ("audit-due-lesson", (827, 830), "- [ ] **Process lesson to apply every cycle (found c2120)"),
]:
    assert seg(*rng)[0].startswith(prefix), f"{name} range moved: {seg(*rng)[0][:80]!r}"
    assert seg(*rng)[-1].strip() != "", f"{name} range includes a trailing blank"

for name, rng, prefix in [
    ("tms-one-word", (68, 75), "- [ ] **NEW follow-up (c2384)"),
    ("orig-expired-dates-spec", (628, 653), "- [x] **ORIGINAL follow-up text (c2376)"),
]:
    assert seg(*rng)[0].startswith(prefix), f"{name} range moved: {seg(*rng)[0][:80]!r}"
    assert seg(*rng)[-1].strip() != "", f"{name} range includes a trailing blank"

kept_idx = {i for a, b in KEPT_BLOCKS for i in range(a, b + 1)}
hoisted_idx = {i for a, b in HOISTED for i in range(a, b + 1)}
closed_idx = {i for a, b in CLOSED_UNCHECKED for i in range(a, b + 1)}
assert not (kept_idx & hoisted_idx), "a kept block overlaps a hoisted item"
assert not (kept_idx & closed_idx), "a kept block overlaps a closed item"
assert not (hoisted_idx & closed_idx), "a hoisted item overlaps a closed item"

open_idx = [i for i, l in enumerate(lines, 1) if l.startswith("- [ ] ")]
expected_open = [68, 106, 153, 242, 655, 674, 695, 709, 732, 738, 763, 772, 812, 827]
assert open_idx == expected_open, f"open-item set changed: {open_idx}"
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
    "\n## Archived by cycle 2387 (sonnet-5), 2026-10-28 -- tasks/queue.md had grown to 831 "
    "lines / 77.6KB, projected past the 150KB warn line before check-doc-size's next scheduled "
    "look (24c). check-doc-size itself recommended trimming proactively in a QUALITY slot; "
    "2387%3==2 is that slot, same pass as this cycle's STATUS.md trim. The live file keeps the "
    "6 DONE blocks matching the live STATUS.md window (2382..2386; cycle 2385 contributed two "
    "separate DONE items in its one BUILD slot). ALL 13 genuinely-still-live open items were "
    "HOISTED: the c2385 sub-20 watch item, the c2383 scope-count standing method, the c2380 "
    "growing-niches follow-up, and the 10 long-standing tail items (dev.to c2368, ext_bad30d "
    "tripwire c2336, feed-pickup c2332, scholarship c2312, publish-before-push process lesson, "
    "tool-page-CTA c2276, ack-staleness c2196, revenue-trigger c2168/c2268, DMARC-accumulate "
    "c2371, audit-due-yourself process lesson c2120). TWO open items were archived as "
    "CLOSED-BUT-UNCHECKED rather than hoisted, because each is now fully resolved: the c2384 "
    "trademark-search-scraper one-word-drift note (its own text says nothing is left to act on) "
    "and the ORIGINAL c2376 future-dated-claim follow-up spec (superseded by the kept c2386 DONE "
    "block, which already summarizes it). Everything else -- every other DONE block older than "
    "the kept window, including the long c2360 campaign-retro block (its durable screening "
    "questions already duplicate notes/LEARNINGS.md's cycle-2360 entry) and the old c2371 "
    "DMARC-receiver-fix DONE block -- moved here verbatim, in original order.\n\n"
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
    if ln.startswith("- [x] **DONE") or ln.startswith("- [ ] ") or ln.startswith("- [x] **ORIGINAL"):
        if ln not in live_text and ln not in arch_text:
            sys.exit(f"FAIL: block header destroyed: {ln[:90]!r}")

live_open = [l for l in new_live if l.startswith("- [ ] ")]
if len(live_open) != 13:
    sys.exit(f"FAIL: expected 13 live open items, got {len(live_open)}")
for a, b in HOISTED:
    if lines[a - 1] not in live_text:
        sys.exit(f"FAIL: hoisted item {a} did not land in the live file")

kept_cycles = sorted(int(l.split("DONE cycle ")[1].split()[0])
                      for l in new_live if l.startswith("- [x] **DONE cycle"))
if kept_cycles != [2382, 2383, 2384, 2385, 2385, 2386]:
    sys.exit(f"FAIL: kept cycles are not 2382/2383/2384/2385/2385/2386: {kept_cycles}")

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
