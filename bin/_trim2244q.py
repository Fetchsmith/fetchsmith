#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2244 (113.5KB / 1410 lines).

Same trigger as this cycle's STATUS.md trim (bin/_trim2244.py): check-doc-size reads
TRIM SOON -- ~16 cycles of headroom today at +5440 B/cycle, but ~241KB projected at
its own next look (24c, cycle 2268), past both the warn and trim lines BETWEEN looks.
Trimmed in the same QUALITY-slot pass.

Uses the c2161/c2196/c2220 HOIST-THEN-CUT method, not a keep-newest-N cut: queue.md
interleaves standing `- [ ]` open items among completed `- [x]` cycle blocks, so a
naive cut by line number silently deletes live open work.

  1. Keep the 5 DONE blocks matching the live STATUS.md window (2239..2243). The
     file's block order is NOT newest-first -- 2240 (39) sits above 2236 (78), 2237
     (130), 2238 (151), 2241 (180), 2242 (199), and 2239 is far below at 279 -- so
     these are four separate kept ranges, not one prefix. A prefix cut deep enough to
     include 2239 would also drag 2236/2237/2238 along (29.7KB live, projecting
     162KB at the next look on the check's own rate); keeping exactly the STATUS
     window is both smaller and the same story in both files.
  2. Hoist the 10 genuinely-live open items verbatim after the kept blocks:
       - c2236->c2243 competitor-claims backlog      (233-261)
       - c2238 x-appliesTo schema annotation         (262-278)
       - c2232 5 unjudged check-mode-scope flags     (488-508)
       - c2232 check-disclosure unregistered         (509-517)
       - c2228 eu-ted flatten / webhookUrl           (710-739)
       - c2224 maxCommentDepth null-on-failure       (994-1011)
       - c2196 ack-staleness warning proposal        (1381-1389)
       - c2168 trademark-search-scraper buyer watch  (1390-1398)
       - c2103 DMARC recheck, blocked externally     (1399-1405)
       - c2120 re-verify-due-lists process lesson    (1406-1410)
  3. Archive everything else verbatim to tasks/queue_archive.md, in original order.
     This deliberately archives two of the twelve `- [ ]` items rather than hoisting:

       a. **1187->27, the `- [ ] NEXT (cycle 2244 ...)` handoff item.** Discharged by
          this cycle, whose own DONE block replaces it. Archived as-is rather than
          rewritten so the verification below stays a byte-level check -- the same
          treatment c2220 gave the c2198-discharged Steam-ack item.
       b. **929, a verbatim DUPLICATE of the hoisted 994.** Both are "prove
          maxCommentDepth's null-on-failure path live on hacker-news-scraper" from
          c2224; 994 is the superset (it adds the `bin/run-charged` instruction) and
          929 adds nothing 994 lacks. Found while auditing open items for this trim.
          Two copies of one task were being carried as two tasks for 20 cycles.

Live lands at ~24.0KB, ~29KB once c2244 prepends its own block. check-doc-size's
+5440 B/cycle projects ~156KB at the next look, but that rate is pessimistic for this
file and measurably so: c2220 left 19KB live and the file reached 113.5KB over 24
cycles, i.e. ~3.9KB/cycle actual, which projects ~123KB -- comfortably under the
150KB warn line. (c2220's script made the same observation at ~3.75KB/cycle and it
held.) Recorded here so the next trim can check the rate again rather than re-derive
it.

Verifies losslessly before writing anything.
"""
import sys

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 1410, f"expected 1410 lines, got {len(lines)} -- file changed, abort"

# 1-indexed inclusive ranges, pinned by inspection this cycle.
KEPT_BLOCKS = [(1, 26), (39, 77), (180, 232), (279, 312)]   # 2243 | 2240 | 2241+2242 | 2239
HOISTED = [
    (233, 261), (262, 278), (488, 508), (509, 517), (710, 739),
    (994, 1011), (1381, 1389), (1390, 1398), (1399, 1405), (1406, 1410),
]
NEXT_DISCHARGED = (27, 38)      # the `- [ ] NEXT (cycle 2244 ...)` item, done this cycle
DUPLICATE = (929, 945)          # verbatim duplicate of the hoisted 994 item


def seg(a, b):
    """1-indexed inclusive line range -> list of lines."""
    return lines[a - 1:b]


# --- Preconditions: every pinned boundary is what this script thinks it is ---
for cyc, (a, _) in zip((2243, 2240, 2241, 2239), KEPT_BLOCKS):
    assert seg(a, a)[0].startswith(f"- [x] **DONE cycle {cyc}"), f"block {cyc} moved from {a}"
assert lines[199 - 1].startswith("- [x] **DONE cycle 2242"), "2242 is not inside the 180-232 range"
for name, rng, prefix in [
    ("backlog", (233, 261), "- [ ] **CARRIED follow-up (c2236 -> c2243, MEDIUM)"),
    ("x-appliesTo", (262, 278), "- [ ] **NEW follow-up (c2238, MEDIUM-HIGH"),
    ("mode-scope", (488, 508), "- [ ] **NEW follow-up (c2232, MEDIUM;"),
    ("disclosure", (509, 517), "- [ ] **NEW follow-up (c2232, LOW)"),
    ("eu-ted", (710, 739), "- [ ] **NEW follow-up (c2228, low priority)"),
    ("depth-keep", (994, 1011), "- [ ] **NEW follow-up (c2224, still open, low priority)"),
    ("ack-stale", (1381, 1389), "- [ ] **NEW follow-up (c2196) -- consider an ack STALENESS"),
    ("trademark", (1390, 1398), "- [ ] **NEW follow-up (c2168)"),
    ("DMARC", (1399, 1405), "- [ ] **STILL OPEN (carried from c2103"),
    ("lesson", (1406, 1410), "- [ ] **Process lesson"),
    ("next-item", NEXT_DISCHARGED, "- [ ] **NEXT (cycle 2244,"),
    ("duplicate", DUPLICATE, "- [ ] **NEW follow-up (c2224) -- prove `maxCommentDepth`"),
]:
    assert seg(*rng)[0].startswith(prefix), f"{name} range moved"

kept_idx = {i for a, b in KEPT_BLOCKS for i in range(a, b + 1)}
hoisted_idx = {i for a, b in HOISTED for i in range(a, b + 1)}
assert not (kept_idx & hoisted_idx), "a kept block overlaps a hoisted item"
for rng in (NEXT_DISCHARGED, DUPLICATE):
    assert not (set(range(rng[0], rng[1] + 1)) & (kept_idx | hoisted_idx)), \
        f"archived-on-purpose range {rng} overlaps kept/hoisted"

# Exactly the 12 open items this script knows about, and no others.
open_idx = [i for i, l in enumerate(lines, 1) if l.startswith("- [ ] ")]
assert open_idx == [27, 233, 262, 488, 509, 710, 929, 994, 1381, 1390, 1399, 1406], \
    f"open-item set changed: {open_idx}"

# The duplicate claim is load-bearing: 929's body must add nothing 994's does not.
# Compared on punctuation-stripped words, because the only two differences are
# punctuation artifacts of the rewrite -- 929's header reads `(c2224)` where 994's
# reads `(c2224,` ("still open, low priority"), and 929 ends a sentence `tightly.`
# where 994 continues it `tightly -- use bin/run-charged ...`. Stripping punctuation
# rather than dropping the assertion keeps it able to catch a real extra sentence.
def words(ranges):
    return {w.strip(".,;:()`*-") for l in seg(*ranges) for w in l.split()} - {""}


extra = words(DUPLICATE) - words((994, 1011))
assert not extra, f"929 is NOT a subset of 994 -- hoist it too, it says: {sorted(extra)}"


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
    "\n## Archived by cycle 2244 (opus-5), 2026-10-25 -- tasks/queue.md had grown to 1410 lines "
    "/ 113.5KB. NOT trim-due today: check-doc-size read TRIM SOON (~16 cycles of headroom at "
    "+5440 B/cycle) but projected ~241KB at its own next look (24c, cycle 2268), past both the "
    "warn and trim lines BETWEEN looks -- trimmed in the same QUALITY-slot pass as this cycle's "
    "STATUS.md trim. The live file keeps the 5 DONE blocks matching the live STATUS.md window "
    "(2239..2243 -- four separate kept ranges, since the source file's blocks are not "
    "newest-first: 2240 sat above 2236/2237/2238/2241/2242 and 2239 was far below them) plus the "
    "10 genuinely-live open items, which were HOISTED (c2243 competitor-claims backlog, c2238 "
    "x-appliesTo annotation, c2232 5 unjudged mode-scope flags, c2232 check-disclosure "
    "unregistered, c2228 eu-ted flatten/webhookUrl, c2224 maxCommentDepth null-on-failure, c2196 "
    "ack-staleness proposal, c2168 trademark-search buyer watch, c2103 DMARC recheck, c2120 "
    "re-verify-due-lists process lesson). Everything else moved here verbatim, in original "
    "order. TWO of the twelve `- [ ]` items below are archived as CLOSED, not pending -- do not "
    "resume either: (a) the `- [ ] NEXT (cycle 2244 ...)` handoff item, discharged by cycle 2244 "
    "itself, whose DONE block replaces it; (b) the `- [ ] NEW follow-up (c2224) -- prove "
    "`maxCommentDepth`'s null-on-failure path live` item, a verbatim DUPLICATE of the c2224 item "
    "hoisted into the live file (asserted a strict word-level subset before archiving). The same "
    "task had been carried as two separate open items since c2224, ~20 cycles.\n\n"
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

# --- Verification 5: exactly the 10 hoisted items are live; the 2 closed ones are archived ---
live_open = [l for l in new_live if l.startswith("- [ ] ")]
if len(live_open) != 10:
    sys.exit(f"FAIL: expected 10 live open items, got {len(live_open)}")
for a, b in HOISTED:
    if lines[a - 1] not in live_text:
        sys.exit(f"FAIL: hoisted item {a} did not land in the live file")
for name, (a, _) in (("NEXT", NEXT_DISCHARGED), ("duplicate", DUPLICATE)):
    if lines[a - 1] in live_text:
        sys.exit(f"FAIL: the {name} item should be archived, not live")
    if lines[a - 1] not in "".join(archived):
        sys.exit(f"FAIL: the {name} item is missing from the archive")

# --- Verification 6: the kept DONE blocks are exactly 2239..2243 ---
kept_blocks = sorted(int(l.split("DONE cycle ")[1].split()[0])
                     for l in new_live if l.startswith("- [x] **DONE cycle"))
if kept_blocks != [2239, 2240, 2241, 2242, 2243]:
    sys.exit(f"FAIL: kept blocks are not 2239..2243: {kept_blocks}")

print("All 6 verifications passed. Writing files.")
with open(SRC, "w") as f:
    f.write(live_text)
with open(ARCHIVE, "w") as f:
    f.write(new_archive)
print(f"live queue.md:     {len(new_live)} lines / {len(live_text.encode())} bytes "
      f"({len(live_text.encode())/1024:.1f}KB)")
print(f"archive addition:  {len(archived)} lines")
print(f"open items live:   {len(live_open)}  (2 archived as closed: NEXT handoff, duplicate)")
