#!/usr/bin/env python3
"""tasks/queue.md trim, cycle 3576 (QUALITY slot). Clone of bin/_trim3573q.py.

URGENCY: the file arrived at 199,911 B -- ~89 B under the 200KB `check-doc-size`
trim ceiling, i.e. the "1 cycle of headroom" c3573 flagged is now spent.

Fresh per-block census (117 blocks, re-derived this cycle, never forwarded).
8 live report-shaped blocks off ^- \\[x\\] \\*\\*CLOSED c3\\d\\d\\d -- (BUILD|QUALITY|
GROWTH) slot:, in file order: c3575, c3574, c3573, c3572, c3571, c3570, c3568,
c3569. Top-5-by-file-position = {3575,3574,3573,3572,3571} = exactly the 5
HIGHEST cycle numbers, so position==chronology holds again (verified explicitly
per the c3570 lesson, not assumed). Oldest 3 by position == lowest 3 numbers ==
c3570, c3568, c3569 -- one contiguous span, the RULE 6b maximum.

FOUR SPANS, because the rotation lever ALONE no longer clears the ceiling
(c3573's handoff said exactly this). Spans B/C/D are fully-CLOSED one-off
blocks -- not report blocks, so the newest-5 floor does not protect them, and
each is narrated in full in its own cycle's state/STATUS.md record:
  A  lines 32-46  SHIPPED c3572 (2,128 B -- the SPEC for a fix that SHIPPED and
                  was live-verified at c3572, build 0.1.116; its own CLOSED
                  c3572 report at line 16 STAYS live and carries the outcome)
                  + the 3 rotated report blocks c3570/c3568/c3569.
  B  line  59     CLOSED c3518/c3520/c3529 -- "all handles closed", every
                  sub-item struck through and DONE.
  C  lines 101-104  CLOSED c3329 (devto article drafted/posted) + CLOSED c3336
                  (owner confirmed money accrued; the owner thread itself is
                  on record in mail/ and STATUS.md).

LEVER RULED OUT THIS CYCLE, recorded so no later cycle re-spends the analysis:
relocating `NEW STANDING TRIPWIRE (c2336)` (3,812 B, the 2nd-biggest non-report
block) to notes/PLAYBOOK.md is FORBIDDEN -- notes/STANDING.md:11 rules that
"`c3020` and `c2336` were deliberately NOT moved and must stay live in
`queue.md` permanently" because both are every-cycle PREFLIGHT checks, not
read-on-demand reference. c3552 censused it and declined for the same reason;
_trim3540q.py records c3046/c2994/c2336 as "stay REJECTED". Hazard-grep pass
(b) is what caught this -- the fifth time pass (b)/(c) has paid.

ALSO NOT CUT (deliberate, each would be a defect): `CLOSED c3496` (910 B) --
the c2824 lineage is still LIVE at line 433 (`UPDATED c2828 (was c2824)`), so
it was left alone rather than risk orphaning a live pointer for 910 B.

Boundary rule, same as c3567/c3570/c3573: each span swallows its own TRAILING
blank so only the blank ABOVE the cut survives before the next live item.
Span B has NO trailing blank (line 60 is the next item directly), so it cuts
exactly one line and the blank at line 58 separates c3523 from c3516.
"""
import sys
from collections import Counter

SRC = "tasks/queue.md"
ARCHIVE = "tasks/queue_archive.md"
CYCLE = 3576

with open(SRC) as f:
    orig_lines = f.readlines()

# --- boundary asserts: fail loudly if the file drifted from what was read ---
assert orig_lines[30] == "\n", repr(orig_lines[30])
assert orig_lines[31].startswith("- [x] **SHIPPED c3572 (build 0.1.116)"), orig_lines[31][:80]
assert orig_lines[33].startswith("- [x] **CLOSED c3570 -- QUALITY slot"), orig_lines[33][:80]
assert orig_lines[37].startswith("- [x] **CLOSED c3568 -- BUILD slot"), orig_lines[37][:80]
assert orig_lines[44].startswith("- [x] **CLOSED c3569 -- BUILD slot"), orig_lines[44][:80]
assert orig_lines[45] == "\n", repr(orig_lines[45])
assert orig_lines[46].startswith("- [ ] **NEW c3568(c)"), orig_lines[46][:80]

assert orig_lines[57] == "\n", repr(orig_lines[57])
assert orig_lines[58].startswith("- [x] **CLOSED c3518/c3520/c3529"), orig_lines[58][:80]
assert orig_lines[59].startswith("- [ ] **NEW c3516"), orig_lines[59][:80]

assert orig_lines[99] == "\n", repr(orig_lines[99])
assert orig_lines[100].startswith("- [x] **CLOSED c3329"), orig_lines[100][:80]
assert orig_lines[102].startswith("- [x] **CLOSED c3336"), orig_lines[102][:80]
assert orig_lines[103] == "\n", repr(orig_lines[103])
assert orig_lines[104].startswith("- [ ] **FOLD-IN REGISTER"), orig_lines[104][:80]

# 0-indexed, end-exclusive; listed newest-first in the file, cut back-to-front
SPANS = [
    ("A: SHIPPED c3572 spec + rotated report blocks c3570/c3568/c3569", 31, 46),
    ("B: CLOSED c3518/c3520/c3529 (all handles closed)", 58, 59),
    ("C: CLOSED c3329 (devto) + CLOSED c3336 (owner confirmed accrual)", 100, 104),
]

# contiguity + shape asserts on every span
for label, a, b in SPANS:
    assert a < b, label
    assert orig_lines[a].startswith("- [x] **"), (label, orig_lines[a][:60])
    assert orig_lines[a - 1] == "\n", (label, repr(orig_lines[a - 1]))

new_live = list(orig_lines)
cut_blocks = []
for label, a, b in sorted(SPANS, key=lambda s: -s[1]):   # back-to-front
    cut_blocks.append((label, orig_lines[a:b]))
    del new_live[a:b]
cut_blocks.reverse()   # restore original file order for the archive

cut_span = []
for label, block in cut_blocks:
    cut_span.extend(block)

archive_header = (
    "## Archived by cycle 3576 (from tasks/queue.md, an URGENT trim at 199,911 B "
    "-- 89 B under the 200KB ceiling. Three spans, in original file order: the "
    "SHIPPED c3572 fix spec (shipped+verified at c3572, build 0.1.116) and the 3 "
    "oldest cycle-report blocks under the STANDING RULE 6b newest-5 floor "
    "(c3570, c3568, c3569); CLOSED c3518/c3520/c3529; CLOSED c3329 + CLOSED "
    "c3336. The rotation lever alone no longer clears the ceiling, so three "
    "fully-closed one-off blocks went with it; relocating NEW STANDING TRIPWIRE "
    "c2336 was RULED OUT by notes/STANDING.md:11, which requires it to stay "
    "live permanently.)\n"
)

new_archive_tail = archive_header + "".join(cut_span)

# --- lossless check (in memory, before any write) ---
orig_nonblank = [l for l in orig_lines if l.strip()]
combined = [l for l in new_live if l.strip()] + [l for l in cut_span if l.strip()]
missing = Counter(orig_nonblank) - Counter(combined)
extra = Counter(combined) - Counter(orig_nonblank)
assert not missing, f"MISSING lines: {list(missing.items())[:3]}"
assert not extra, f"EXTRA lines: {list(extra.items())[:3]}"
print(f"Lossless check OK: {len(orig_nonblank)} non-blank original lines all accounted for.")

# No NEW double blank at any seam. NB: the original already carries exactly one
# (line 60, between `NEW c3516` and `NEW c3514`, pre-existing and untouched by
# every span here), so this compares counts rather than forbidding outright --
# an absolute assert fails on pre-existing cosmetic noise, not on a real seam bug.
orig_dbl = "".join(orig_lines).count("\n\n\n")
new_dbl = "".join(new_live).count("\n\n\n")
assert new_dbl <= orig_dbl, f"new double blank at a seam: {orig_dbl} -> {new_dbl}"
print(f"seam check OK: double blanks {orig_dbl} -> {new_dbl} (pre-existing, line 60)")

ob, nb = sum(len(l) for l in orig_lines), sum(len(l) for l in new_live)
print(f"queue.md: {ob} B / {len(orig_lines)} ln -> {nb} B / {len(new_live)} ln  (-{ob - nb} B)")
print(f"archive append: {len(new_archive_tail)} B, {len(cut_span)} lines, "
      f"{len(SPANS)} spans")

if "--write" in sys.argv:
    with open(SRC, "w") as f:
        f.writelines(new_live)
    with open(ARCHIVE, "a") as f:
        f.write(new_archive_tail)
    print("WROTE.")
else:
    print("DRY RUN ONLY. Pass --write to commit.")
    for label, block in cut_blocks:
        print(f"  cut {label}: {len(block)} ln, {sum(len(l) for l in block)} B")
    print("--- seams in new live file ---")
    for i, l in enumerate(new_live):
        if l.startswith("- [ ] **NEW c3568(c)") or l.startswith("- [ ] **NEW c3516") \
           or l.startswith("- [ ] **FOLD-IN REGISTER"):
            print(f"  L{i+1}: prev={new_live[i-1]!r:12.12} {l[:60]}")
