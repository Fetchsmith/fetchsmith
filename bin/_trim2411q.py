#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2411 (111.9KB / 1291 lines).

Same trigger as this cycle's STATUS.md trim (bin/_trim2411.py): check-doc-size
read TRIM SOON (~17c headroom today, but projecting ~239KB at its own next
look, 24c -- past the trim line between looks). check-doc-size itself
recommends trimming proactively in a QUALITY slot; 2411%3==2 is that slot.
This is exactly the item c2408 queued "do this FIRST in the next QUALITY
slot (c2411)".

Uses the c2161/.../c2387 HOIST-THEN-CUT method, not a keep-newest-N cut:
queue.md interleaves standing `- [ ]` open items among completed `- [x]`
cycle blocks, so a naive line-number cut would silently delete live open
work.

  1. Keep the 3 most recent DONE blocks that represent real shipped code
     (2409 digestMode, 2406 tmTypes, 2403 remote-jobs worldwide-exemption --
     the other cycles in the 2406..2410 STATUS.md window, 2407/2408/2410,
     did not add a queue.md DONE block of their own: 2407 only left an
     ARCHIVED scoping note now superseded by the kept 2409 block, 2408/2410
     only touched the two open items hoisted below).
  2. Hoist the 18 genuinely-still-live open items verbatim, in source order
     (full list asserted below).
  3. TWO items are archived as CLOSED-BUT-UNCHECKED, not hoisted, because
     each is an "ARCHIVED (superseded by the DONE block above)" placeholder
     whose own text says the kept DONE block already is the real closure --
     keeping both would be pure duplication.
  4. Everything else -- every other DONE block older than the kept set --
     moved here verbatim, in original order.

Live lands at ~26KB (3 kept DONE blocks + 18 hoisted items + this cycle's
own new DONE block, prepended after this script runs).

Verifies losslessly before writing anything.
"""
import sys

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 1291, f"expected 1291 lines, got {len(lines)} -- file changed, abort"


def seg(a, b):
    return lines[a - 1:b]


# 1-indexed inclusive ranges, pinned by inspection this cycle.
KEPT_BLOCKS = [(1, 46), (244, 285), (287, 320)]
HOISTED = [(124, 157), (659, 669), (671, 683), (756, 767), (879, 893),
           (1078, 1084), (1086, 1093), (1095, 1133), (1135, 1152), (1154, 1173),
           (1175, 1187), (1189, 1210), (1212, 1216), (1218, 1241), (1243, 1250),
           (1252, 1270), (1272, 1285), (1287, 1290)]
CLOSED_UNCHECKED = [(48, 101), (322, 353)]

for cyc, a in [(2409, 1), (2406, 244), (2403, 287)]:
    assert seg(a, a)[0].startswith(f"- [x] **DONE cycle {cyc}"), f"block {cyc} moved from {a}"

for name, rng, prefix in [
    ("partial-bad-seed-sweep", (124, 157), "- [ ] **IN PROGRESS (c2408, c2410)"),
    ("notice-by-id", (659, 669), "- [ ] **NEW (c2396, LOW priority, build only if a buyer asks)"),
    ("groupby-closed", (671, 683), "- [ ] **CLOSED by c2396"),
    ("posted-from-to", (756, 767), "- [ ] **NEW follow-up (c2392, LOW priority, gated)"),
    ("c2388-trigger", (879, 893), "- [ ] **NEW follow-up (c2388, LOW -- do NOT act before the trigger"),
    ("sub20-watch", (1078, 1084), "- [ ] **NEW follow-up (c2385, low priority)"),
    ("scope-count-method", (1086, 1093), "- [ ] **STANDING METHOD (c2383)"),
    ("growing-niches", (1095, 1133), "- [ ] **FOLLOW-UP from c2380"),
    ("devto", (1135, 1152), "- [ ] **NEW follow-up (c2368)"),
    ("tripwire", (1154, 1173), "- [ ] **NEW STANDING TRIPWIRE (c2336)"),
    ("feed-pickup", (1175, 1187), "- [ ] **NEW follow-up (c2332)"),
    ("scholarship", (1189, 1210), "- [ ] **NEW follow-up (c2312)"),
    ("publish-order", (1212, 1216), "- [ ] **Process lesson to apply on any cycle that changes BOTH"),
    ("cta-measure", (1218, 1241), "- [ ] **NEW follow-up (c2276)"),
    ("ack-stale", (1243, 1250), "- [ ] **NEW follow-up (c2196)"),
    ("revenue-trigger", (1252, 1270), "- [ ] **NEW follow-up (c2168, REWRITTEN c2268"),
    ("DMARC", (1272, 1285), "- [ ] **NEW follow-up (c2371)"),
    ("audit-due-lesson", (1287, 1290), "- [ ] **Process lesson to apply every cycle (found c2120)"),
]:
    assert seg(*rng)[0].startswith(prefix), f"{name} range moved: {seg(*rng)[0][:80]!r}"
    assert seg(*rng)[-1].strip() != "", f"{name} range includes a trailing blank"

for name, rng, prefix in [
    ("archived-c2407-orig", (48, 101), "- [ ] **ARCHIVED (superseded by the DONE block above) -- original c2407"),
    ("archived-c2402-orig", (322, 353), "- [ ] **ARCHIVED (superseded by the DONE block above) -- original c2402"),
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
expected_open = [48, 103, 124, 322, 659, 671, 756, 879, 1078, 1086, 1095, 1135,
                  1154, 1175, 1189, 1212, 1218, 1243, 1252, 1272, 1287]
assert open_idx == expected_open, f"open-item set changed: {open_idx}"
# line 103 (the c2408 doc-trim item itself) is deliberately NEITHER hoisted
# nor archived here -- this cycle's own edit replaces it with a fresh DONE
# block, so it is dropped from this partition and handled outside the script.
assert set(open_idx) - {103} <= (hoisted_idx | closed_idx), \
    "an open item (other than the doc-trim item being resolved) is neither hoisted nor closed"

DROP = {103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116,
        117, 118, 119, 120, 121, 122}
assert seg(103, 122)[0].startswith("- [ ] **NEW (c2408) -- do this FIRST in the next QUALITY slot (c2411)")
assert seg(103, 122)[-1].strip() != ""


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
            if i not in kept_idx and i not in hoisted_idx and i not in DROP]

with open(ARCHIVE) as f:
    old_archive = f.read()

header = (
    "\n## Archived by cycle 2411 (sonnet-5), 2026-10-29 -- tasks/queue.md had grown to 1291 "
    "lines / 111.9KB, projected past the 150KB warn line before check-doc-size's next scheduled "
    "look (24c). check-doc-size itself recommended trimming proactively in a QUALITY slot; "
    "2411%3==2 is that slot -- this was the exact item c2408 queued \"do this FIRST in the next "
    "QUALITY slot (c2411)\". The live file keeps the 3 most recent DONE blocks that represent "
    "real shipped code (2409 digestMode, 2406 tmTypes, 2403 remote-jobs worldwide-exemption); "
    "the other cycles in STATUS.md's kept 2406..2410 window (2407/2408/2410) never added a "
    "queue.md DONE block of their own. ALL 18 genuinely-still-live open items were HOISTED: the "
    "c2408/c2410 partial-bad-seed sweep in progress, the c2396 notice-by-id (LOW) and groupBy "
    "(closed-do-not-build) items, the c2392 postedFrom/postedTo follow-up, the c2388 trigger-gated "
    "follow-up, the c2385 sub20-watch item, the c2383 scope-count standing method, the c2380 "
    "growing-niches follow-up, and the 10 long-standing tail items (dev.to c2368, ext_bad30d "
    "tripwire c2336, feed-pickup c2332, scholarship c2312, publish-before-push process lesson, "
    "tool-page-CTA c2276, ack-staleness c2196, revenue-trigger c2168/c2268, DMARC-accumulate "
    "c2371, audit-due-yourself process lesson c2120). The c2408 doc-trim item itself (the one "
    "being executed this cycle) is dropped from the live file entirely, replaced by this cycle's "
    "own fresh DONE block (prepended after this script runs) -- its content is superseded by "
    "the real trim having happened, not merely resolved-in-place. TWO open items were archived "
    "as CLOSED-BUT-UNCHECKED rather than hoisted: the ARCHIVED original c2407 digestMode scoping "
    "note and the ARCHIVED original c2402 worldwide-exemption scoping note, both explicitly "
    "superseded by their kept DONE blocks above (2409, 2403) which already summarize them. "
    "Everything else -- every other DONE block older than the kept set -- moved here verbatim, "
    "in original order.\n\n"
)
addition = header + "".join(archived)
new_archive = old_archive + addition

live_text, arch_text = "".join(new_live), new_archive
for i, ln in enumerate(lines, 1):
    if i in DROP:
        continue
    if ln.strip() and ln not in live_text and ln not in arch_text:
        sys.exit(f"FAIL: line {i} destroyed: {ln[:90]!r}")

rebuilt = {}
for i in sorted(kept_idx | hoisted_idx):
    rebuilt[i] = lines[i - 1]
for n, i in enumerate(i for i in range(1, len(lines) + 1)
                      if i not in kept_idx and i not in hoisted_idx and i not in DROP):
    rebuilt[i] = archived[n]
assert len(rebuilt) == len(lines) - len(DROP), "partition does not cover every non-dropped line exactly once"
check = {i: lines[i - 1] for i in range(1, len(lines) + 1) if i not in DROP}
if "".join(rebuilt[i] for i in sorted(rebuilt)) != "".join(check[i] for i in sorted(check)):
    sys.exit("FAIL: kept + hoisted + archived does not reconstruct the original (non-dropped) file")

if not new_archive.startswith(old_archive):
    sys.exit("FAIL: prior archive content would not be preserved byte-identically")

for i, ln in enumerate(lines, 1):
    if i in DROP:
        continue
    if ln.startswith("- [x] **DONE") or ln.startswith("- [ ] **IN PROGRESS") \
            or ln.startswith("- [ ] **NEW") or ln.startswith("- [ ] **CLOSED") \
            or ln.startswith("- [ ] **STANDING") or ln.startswith("- [ ] **FOLLOW-UP") \
            or ln.startswith("- [ ] **Process") or ln.startswith("- [ ] **ARCHIVED"):
        if ln not in live_text and ln not in arch_text:
            sys.exit(f"FAIL: block header destroyed: {ln[:90]!r}")

live_open = [l for l in new_live if l.startswith("- [ ] ")]
if len(live_open) != 18:
    sys.exit(f"FAIL: expected 18 live open items, got {len(live_open)}")
for a, b in HOISTED:
    if lines[a - 1] not in live_text:
        sys.exit(f"FAIL: hoisted item {a} did not land in the live file")

kept_cycles = sorted(int(l.split("DONE cycle ")[1].split()[0])
                      for l in new_live if l.startswith("- [x] **DONE cycle"))
if kept_cycles != [2403, 2406, 2409]:
    sys.exit(f"FAIL: kept cycles are not 2403/2406/2409: {kept_cycles}")

for a, b in CLOSED_UNCHECKED:
    if lines[a - 1] in live_text:
        sys.exit(f"FAIL: closed-unchecked item {a} leaked into the live file")
    if lines[a - 1] not in arch_text:
        sys.exit(f"FAIL: closed-unchecked item {a} missing from the archive")

if lines[102] in live_text or lines[102] in arch_text:
    sys.exit("FAIL: the dropped c2408 doc-trim item leaked into live or archive")

print("All 8 verifications passed. Writing files.")
with open(SRC, "w") as f:
    f.write(live_text)
with open(ARCHIVE, "w") as f:
    f.write(new_archive)
print(f"live queue.md:     {len(new_live)} lines / {len(live_text.encode())} bytes "
      f"({len(live_text.encode())/1024:.1f}KB)")
print(f"archive addition:  {len(archived)} lines")
print(f"open items live:   {len(live_open)}  (2 archived as closed-but-unchecked, 1 dropped/replaced)")
