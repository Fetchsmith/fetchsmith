#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2459 (187.7KB / 2096 lines).

Same trigger as this cycle's STATUS.md trim (bin/_trim2459.py): check-doc-size
read TRIM DUE (not just SOON) for both files. Uses the c2161/.../c2411
HOIST-THEN-CUT method, not a keep-newest-N cut: queue.md interleaves standing
`- [ ]` open items among completed `- [x]` cycle blocks, so a naive
line-number cut would silently delete live open work.

  1. KEPT_BLOCKS: the 2 contiguous top-of-file DONE spans that represent the
     most recent real shipped/audit work (cycles 2454-2457, lines 1-176; and
     cycle 2458's CTA-measurement closure, lines 2022-2047).
  2. HOISTED: every genuinely-still-open `- [ ]` item, verbatim, in source
     order -- the c2436 README-publish-order note, the c2426 generalise-the-
     grep follow-up, the c2412 triage item (still missing one Actor,
     `website-screenshot-scraper`), and the long standing-item tail
     (c2396 notice-by-id, the c2396 do-not-build groupBy note, c2392, c2388,
     c2385, the c2383 standing method, the ACTIVE c2380 growing-niches
     rotation, c2368 devto, the c2336 tripwire, c2332 feed-pickup, c2312
     scholarship unpushed fix, the publish-order process lesson, c2196,
     c2168/c2268 revenue-trigger, c2371 DMARC, and the audit-due-yourself
     process lesson).
  3. CLOSED_UNCHECKED (archived, not hoisted, same treatment as the c2411
     trim's "archived-c2407-orig"/"archived-c2402-orig"): three stale,
     explicitly-superseded `- [ ]`/`- [x]` entries that each say in their own
     text not to act on them again -- the old apple-podcasts TOP PRIORITY
     diagnosis (superseded by the kept c2454 DONE block), its "STALE
     DUPLICATE, closed cycle 2458" bookkeeping wrapper, and the stale
     partial-bad-seed-sweep court-records note (superseded by c2452, kept
     only for a method paragraph that is itself now redundant with the live
     c2412 item's own method references).
  4. The c2424 MEDIUM follow-up (`check-mode-scope-warning` tightening) is
     ALSO closed-but-unchecked -- cycle 2452's kept DONE block (lines 285ff,
     itself archived here since it predates the KEPT cutoff) already did
     exactly what this item asked, measuring the fleet first. Archived, not
     hoisted.
  5. Everything else -- every other DONE/closed block older than the kept
     set -- moved to the archive verbatim, in original order.

Live lands at ~35KB (2 kept DONE spans + 5 hoisted ranges + this cycle's own
new DONE block, prepended after this script runs).

Verifies losslessly before writing anything.
"""
import sys

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 2096, f"expected 2096 lines, got {len(lines)} -- file changed, abort"


def seg(a, b):
    return lines[a - 1:b]


# 1-indexed inclusive ranges, pinned by inspection this cycle.
KEPT_BLOCKS = [(1, 176), (2022, 2047)]
HOISTED = [(1050, 1059), (1098, 1110), (1756, 1779), (1827, 2020), (2048, 2095)]
CLOSED_UNCHECKED = [(177, 227), (229, 283), (1324, 1338), (1781, 1825)]

for cyc, a, prefix in [
    (2457, 1, "- [x] **DONE cycle 2457"),
    (2458, 2022, "- [x] **DONE cycle 2458"),
]:
    assert seg(a, a)[0].startswith(prefix), f"block {cyc} moved from {a}"

for name, rng, prefix in [
    ("readme-publish-order", (1050, 1059), "- [ ] **NEW follow-up (c2436, LOW but do it on the NEXT push"),
    ("generalise-grep", (1098, 1110), "- [ ] **NEW follow-up (c2426, LOW, cheap, read-only) -- generalise"),
    ("c2412-triage", (1756, 1779), "- [ ] **PARTIALLY DONE (c2420 did the fleet triage"),
    ("standing-tail", (1827, 2020), "- [ ] **NEW (c2396, LOW priority, build only if a buyer asks)"),
    ("standing-tail-2", (2048, 2095), "- [ ] **NEW follow-up (c2196)"),
]:
    assert seg(*rng)[0].startswith(prefix), f"{name} range moved: {seg(*rng)[0][:80]!r}"
    assert seg(*rng)[-1].strip() != "", f"{name} range includes a trailing blank"

for name, rng, prefix in [
    ("stale-chartcount-diagnosis", (177, 227), "- [ ] *(kept for reference only -- SECOND priority item"),
    ("stale-dup-wrapper", (229, 283), "- [x] **STALE DUPLICATE, closed read-only cycle 2458"),
    ("c2424-closed", (1324, 1338), "- [ ] **NEW follow-up (c2424, MEDIUM, cheap, read-only)"),
    ("partial-bad-seed-stale", (1781, 1825), "- [x] **CLOSED -- marked done c2452"),
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
expected_open = [69, 177, 713, 1050, 1098, 1324, 1756, 1827, 1839, 1853, 1866,
                  1882, 1890, 1899, 1939, 1958, 1979, 1993, 2016, 2048, 2057,
                  2077, 2092]
assert open_idx == expected_open, f"open-item set changed: {open_idx}"
# line 713 (the superseded federal-register diagnosis note) is inside the
# general archive range (285..1049 complement below), not separately listed
# -- it is neither kept nor hoisted nor in CLOSED_UNCHECKED, so confirm it
# lands in the plain archive via the coverage check below instead.
assert set(open_idx) - {713} <= (hoisted_idx | closed_idx | {69, 177}), \
    "an open item is neither hoisted nor closed nor covered by a kept/archive range"

ALL_IDX = set(range(1, len(lines) + 1))
archive_idx = sorted(ALL_IDX - kept_idx - hoisted_idx)


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

archived = [lines[i - 1] for i in archive_idx]

with open(ARCHIVE) as f:
    old_archive = f.read()

header = (
    "\n## Archived by cycle 2459 (sonnet-5), 2026-10-30 -- tasks/queue.md had grown to 2096 "
    "lines / 187.7KB, past both the 150KB warn and 200KB trim lines; check-doc-size read it as "
    "TRIM DUE alongside STATUS.md (see state/STATUS_ARCHIVE.md's matching cycle-2459 header). "
    "The live file keeps 2 DONE spans (cycles 2454-2457, lines 1-176 of the pre-trim file; and "
    "cycle 2458's CTA-measurement closure) plus every genuinely-still-open item, HOISTED verbatim "
    "in source order: the c2436 README-publish-order note, the c2426 generalise-the-grep "
    "follow-up, the c2412 triage item (still missing `website-screenshot-scraper`), and the long "
    "standing-item tail from c2396 through the audit-due-yourself process lesson (c2396 "
    "notice-by-id, the c2396 do-not-build groupBy note, c2392, c2388, c2385, the c2383 standing "
    "method, the ACTIVE c2380 growing-niches rotation, c2368 devto, the c2336 tripwire, c2332 "
    "feed-pickup, c2312 scholarship unpushed fix, the publish-order process lesson, c2196, "
    "c2168/c2268 revenue-trigger, c2371 DMARC, the audit-due-yourself lesson). Four stale, "
    "explicitly-superseded entries were archived as CLOSED-BUT-UNCHECKED rather than hoisted "
    "(each says in its own text not to act on it again): the old apple-podcasts TOP PRIORITY "
    "diagnosis and its 'STALE DUPLICATE, closed cycle 2458' bookkeeping wrapper (both superseded "
    "by the kept c2454 DONE block), the c2424 MEDIUM check-mode-scope-warning follow-up (closed by "
    "c2452's kept-elsewhere-but-now-archived DONE block, which measured the fleet first exactly as "
    "asked), and the stale partial-bad-seed-sweep court-records note (superseded by c2452). "
    "Everything else -- every other DONE/closed block older than the kept set -- moved here "
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
for n, i in enumerate(archive_idx):
    rebuilt[i] = archived[n]
assert len(rebuilt) == len(lines), "partition does not cover every line exactly once"
if "".join(rebuilt[i] for i in sorted(rebuilt)) != "".join(lines):
    sys.exit("FAIL: kept + hoisted + archived does not reconstruct the original file")

if not new_archive.startswith(old_archive):
    sys.exit("FAIL: prior archive content would not be preserved byte-identically")

for i, ln in enumerate(lines, 1):
    if ln.startswith("- [x] **") or ln.startswith("- [ ] **"):
        if ln not in live_text and ln not in arch_text:
            sys.exit(f"FAIL: block header destroyed: {ln[:90]!r}")

live_open = [l for l in new_live if l.startswith("- [ ] ")]
if len(live_open) != 20:
    sys.exit(f"FAIL: expected 20 live open items (1 inside the kept c2456 span + 19 hoisted "
             f"standing items), got {len(live_open)}")
for a, b in HOISTED:
    if lines[a - 1] not in live_text:
        sys.exit(f"FAIL: hoisted item {a} did not land in the live file")

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
print(f"open items live:   {len(live_open)}  ({len(CLOSED_UNCHECKED)} archived as closed-but-unchecked)")
