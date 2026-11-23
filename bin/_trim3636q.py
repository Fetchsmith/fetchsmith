#!/usr/bin/env python3
"""_trim3636q.py -- cycle 3636 QUALITY-slot TWO-PART trim of tasks/queue.md.

Clone of bin/_trim3633q.py, which ran a rotation-only pass. This cycle pairs
the rotation WITH the structural cut, per STANDING c3280's standing finding
that the rotation lever alone keeps undershooting ~5.4KB/cycle growth and
per c3633's explicit deferral of exactly this candidate ("overdue two cycles
running").

Fresh census (c3636): 208,498B/976ln, ~-1c headroom per `check-doc-size`.
8 contiguous `CLOSED cNNNN` blocks, file order IS chronological this time
(c3635, c3634, c3633, c3632, c3631, c3630, c3629, c3628).

PART A -- RULE 6b floor-5 rotation: archive the oldest 3 BY POSITION
(c3630, c3629, c3628; lines 22-39) and keep the newest 5 (c3635..c3631) so
this cycle's own CLOSED c3636 block makes 6.

PART B -- structural re-census of `NEW c3372` (5,427B on ONE line, line 87).
Its METHOD/LESSON sentences were RELOCATED VERBATIM to notes/PLAYBOOK.md by
bin/_reloc3636.py in a SEPARATE, EARLIER write (the c3492 lesson: relocate
first, then cut), and verified present there before this script runs. What
is CUT here is only what is now duplicated in PLAYBOOK.md. What STAYS is
sliced out of the original line BYTE-FOR-BYTE inside this script, never
retyped -- the batches-done coverage list, the NEXT BATCH pointer and the
still-open substack-scraper drift are the block's only live state.
"""
import os
import shutil
import sys
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
PLAYBOOK = "/root/agent/notes/PLAYBOOK.md"
CYCLE = 3636

raw = open(QUEUE, "rb").read()
pre_lines = raw.split(b"\n")
pre_bytes = len(raw)

# ---------------------------------------------------------------- PART A
A_START = 21   # 0-indexed; live line 22 (CLOSED c3630)
A_END = 38     # 0-indexed inclusive; live line 39 (blank after c3628's ---)
assert pre_lines[A_START].startswith(
    b"- [x] **CLOSED c3630 -- QUALITY slot (3630 % 3 == 0)."
), pre_lines[A_START][:120]
assert pre_lines[27].startswith(
    b"- [x] **CLOSED c3629 -- BUILD slot (3629 % 3 == 1)."
), pre_lines[27][:120]
assert pre_lines[33].startswith(
    b"- [x] **CLOSED c3628 -- BUILD slot (3628 % 3 == 1)."
), pre_lines[33][:120]
assert pre_lines[A_END] == b"", repr(pre_lines[A_END])
assert pre_lines[A_END - 1] == b"---", repr(pre_lines[A_END - 1])
assert pre_lines[A_END + 1].startswith(b"- [ ] **NEW c3620 (LOW"), pre_lines[A_END + 1][:80]
assert pre_lines[A_START - 1] == b"", repr(pre_lines[A_START - 1])
assert pre_lines[A_START - 2] == b"---", repr(pre_lines[A_START - 2])
# the 5 blocks we KEEP must all be CLOSED blocks, newest-5 by position
for idx, tag in ((0, b"c3635"), (6, b"c3634"), (8, b"c3633"), (11, b"c3632"), (15, b"c3631")):
    assert pre_lines[idx].startswith(b"- [x] **CLOSED " + tag), pre_lines[idx][:60]

part_a = pre_lines[A_START:A_END + 1]
assert len(part_a) == 18, len(part_a)

# ---------------------------------------------------------------- PART B
B_IDX = 86  # 0-indexed; live line 87
src = pre_lines[B_IDX].decode("utf-8")
assert src.startswith("- [ ] **NEW c3372 (MEDIUM -- competitor-claim refresh"), src[:90]
assert len(src.encode()) == 5427, len(src.encode())


def take(start_anchor, end_anchor):
    """Slice [start_anchor, end_anchor) out of the original line, verbatim."""
    i = src.index(start_anchor)
    j = src.index(end_anchor, i + len(start_anchor))
    return src[i:j].rstrip()


keep_tally = take("That run checked", "**CLASS 1 CLOSED c3417**")
keep_class2 = take("**CLASS 2 is the live work", "**11 BATCHES DONE")
keep_batches = take("**11 BATCHES DONE", "**THE FOUR CROSS-BATCH LESSONS")
keep_next = take("**NEXT BATCH:**", "**METHOD: a date may only be re-stamped")
for name, seg in (("tally", keep_tally), ("class2", keep_class2),
                  ("batches", keep_batches), ("next", keep_next)):
    assert seg and seg in src, name
assert "google-play-reviews" in keep_batches and keep_batches.count("c34") >= 10
assert "substack-scraper/README.md:215" in keep_next

new_b = (
    "- [ ] **NEW c3372 (MEDIUM -- competitor-claim refresh, no hard deadline. "
    "Do it off-cadence, in QUALITY slots, a batch at a time. RE-COMPRESSED "
    "c3516; RE-CENSUSED c3636 -- the METHOD is now in `notes/PLAYBOOK.md`, "
    "`## Competitor-claim refresh method (`NEW c3372` batches)`: the CLASS 1 "
    "/ DATED-regex false-positive rule, the four cross-batch lessons, the "
    "live-ladder re-stamp rule, the date-staggering rule and the "
    "never-truncate-a-checker-run rule, all verbatim. **Read that section "
    "before running a batch -- do not re-derive it, and do not re-cut it: "
    "lessons (a)/(b)/(d) and the re-stamp METHOD existed NOWHERE ELSE when "
    "this block was censused.** The BATCH 1-11 per-batch finding narratives "
    "are verbatim in `tasks/queue_archive.md`, `## Archived by cycle 3516`; "
    "the 11.5KB batches-1-10 body is under `## Archived by cycle 3461` and "
    "the c3444-era batches-1-6 compression under `## Archived by cycle "
    "3444`.)** "
    + keep_tally + " "
    + keep_class2 + " "
    + keep_batches + " "
    + keep_next
)

post_lines = list(pre_lines)
post_lines[B_IDX] = new_b.encode("utf-8")
del post_lines[A_START:A_END + 1]
post = b"\n".join(post_lines)

# --------------------------------------------------- losslessness, by VALUE
# the rewritten PART B line is exempt (it is a rewrite, not a move); every
# segment kept from it is asserted present above, and every segment CUT from
# it is asserted present in PLAYBOOK.md below. Compare by VALUE, never `is`
# (the _trim3492q.py bug, PLAYBOOK `## Doc-size trim cadence`).
old_b = pre_lines[B_IDX]
pre_nb = Counter(l for l in pre_lines if l.strip())
post_nb = Counter(l for l in post_lines if l.strip())
arch_nb = Counter(l for l in part_a if l.strip())
exempt = Counter({old_b: 1})
missing = (pre_nb - exempt) - (post_nb + arch_nb)
assert not missing, "WOULD LOSE LINES: %r" % [l[:90] for l in missing]
added = (post_nb + arch_nb) - pre_nb - Counter({new_b.encode(): 1})
assert not added, "unexpected new content: %r" % [l[:90] for l in added]

# the cut halves of PART B must already be in PLAYBOOK.md (relocated earlier)
pb = open(PLAYBOOK, encoding="utf-8").read()
for anchor in ("within 40 chars", "a disclosed undercutter is not permanent",
               "headline number RIGHT and the word", "Stagger the refreshed dates",
               "most flags are user-count-only drift"):
    assert anchor in pb, "NOT RELOCATED: " + anchor

if "--dry-run" in sys.argv:
    print("DRY RUN ok: %d -> %d bytes (%+.1f KB), %d -> %d lines"
          % (pre_bytes, len(post), (len(post) - pre_bytes) / 1024.0,
             len(pre_lines), len(post_lines)))
    print("  PART A archives %d lines (c3630/c3629/c3628)" % len(part_a))
    print("  PART B: NEW c3372 %dB -> %dB (%+dB)"
          % (len(old_b), len(new_b.encode()), len(new_b.encode()) - len(old_b)))
    sys.exit(0)

shutil.copy2(QUEUE, QUEUE + ".c3636.pre")
header = "\n\n## Archived by cycle %d\n\n" % CYCLE
body = (
    "### PART A -- RULE 6b floor-5 rotation: the 3 oldest-by-position "
    "`CLOSED` blocks (c3630, c3629, c3628), verbatim\n\n"
    + "\n".join(l.decode("utf-8") for l in part_a)
    + "\n\n### PART B -- `NEW c3372` pre-image (5,427B, one line) before the "
    "c3636 re-census. Its METHOD/LESSON halves were relocated VERBATIM to "
    "`notes/PLAYBOOK.md`, `## Competitor-claim refresh method`, by "
    "`bin/_reloc3636.py` BEFORE this cut; the live state (tally, "
    "batches-done list, NEXT BATCH pointer, open substack drift) was sliced "
    "byte-for-byte into the surviving line.\n\n"
    + old_b.decode("utf-8") + "\n"
)
with open(ARCHIVE, "a", encoding="utf-8") as fh:
    fh.write(header + body)
with open(QUEUE, "wb") as fh:
    fh.write(post)

live_now = open(QUEUE, "rb").read().split(b"\n")
arch_now = open(ARCHIVE, "rb").read().split(b"\n")
have = Counter(l for l in live_now if l.strip()) + Counter(l for l in arch_now if l.strip())
still_missing = [l for l in pre_nb if have[l] < 1]
assert not still_missing, "POST-WRITE LOSS: %r" % [l[:90] for l in still_missing]
print("WROTE. %d -> %d bytes (%+.1f KB), %d -> %d lines. 0 lines lost "
      "(re-verified against the pre-image, %d distinct non-blank lines)."
      % (pre_bytes, len(post), (len(post) - pre_bytes) / 1024.0,
         len(pre_lines), len(post_lines), len(pre_nb)))
print("  PART A: archived %d lines. PART B: NEW c3372 %dB -> %dB."
      % (len(part_a), len(old_b), len(new_b.encode())))
print("archive now %.1f MB" % (os.path.getsize(ARCHIVE) / 1048576.0))
