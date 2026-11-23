#!/usr/bin/env python3
"""_trim3624q.py -- cycle 3624 QUALITY-slot trim of tasks/queue.md.

Clone of bin/_trim3621q.py (assert-exact-boundary pattern), with ONE addition:
this trim is not rule-6b-only. It does BOTH halves in one write, because the
5-block floor alone sheds less than measured growth (the known `## c3600`
ratchet) and the file arrived at 197.8KB / ~0 cycles of headroom.

PART A (RULE 6b floor-5 rotation): the fresh census found 8 contiguous
`CLOSED cNNNN` blocks (c3623, c3622, c3621, c3618, c3619, c3620, c3617,
c3616 -- note the file order is NOT chronological). Rotate the OLDEST 3 BY
POSITION (c3620, c3617, c3616; lines 28-45) and keep the newest 5 by position
(c3623, c3622, c3621, c3618, c3619), so c3624's own block makes 6.

PART B (structural compression, the lever the method says is the only lasting
one): `NEW c3162` censused at 5,945B on ONE line -- the 3rd largest block in
the file. Archive it verbatim and replace it with a compressed form. What is
cut is (a) the c3622/c3623 per-batch recap PARAGRAPHS, which are exactly what
that block's own closing rule forbids and are already triple-recorded (each
cycle's state/STATUS.md record, its `CLOSED cNNNN` block, and the tracker's
FINDS INDEX -- VERIFIED this cycle: line 137 carries both handles with their
terse parentheticals), (b) the dead top-20-by-users starter list (rows 1-880
are long done), and (c) the c3332/c3492 archival meta-history. The RESUME
POINTER is carried over BYTE-FOR-BYTE by slicing it out of the original line,
never retyped -- it is the only resumption authority in the file.

Per the c3492 lesson (grep for the METHOD and LESSON sentences inside a block
before archiving it, not just its topic): the one method sentence in the cut
region that had no second copy anywhere -- the `cps`-is-check-price-superiority
-not-_unit_price.py module-identity note -- was RELOCATED VERBATIM to
notes/PLAYBOOK.md, `## Vendor-catalogue triage -- the fixed per-batch method`,
in a separate edit BEFORE this script ran.
"""
import os
import re
import shutil
import sys
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
CYCLE = 3624

raw = open(QUEUE, "rb").read()
pre_lines = raw.split(b"\n")
pre_bytes = len(raw)

# ---------------- PART A boundaries: assert, never trust a line number -----
A_START = 27   # 0-indexed; live line 28
A_END = 44     # 0-indexed inclusive; live line 45
assert pre_lines[A_START].startswith(
    b"- [x] **CLOSED c3620 -- BUILD slot (3620 % 3 == 2)."
), pre_lines[A_START][:120]
assert pre_lines[33].startswith(
    b"- [x] **CLOSED c3617 -- BUILD slot (3617 % 3 == 2)."
), pre_lines[33][:120]
assert pre_lines[39].startswith(
    b"- [x] **CLOSED c3616 -- BUILD slot (3616 % 3 == 1)."
), pre_lines[39][:120]
assert pre_lines[A_END] == b"", repr(pre_lines[A_END])
assert pre_lines[A_END - 1] == b"---", repr(pre_lines[A_END - 1])
# the block immediately after the cut must be a live (unchecked) item, i.e. we
# are not eating into the kept CLOSED set or into an open task
assert pre_lines[A_END + 1].startswith(b"- [ ] **NEW c3620 (LOW"), pre_lines[A_END + 1][:80]
# and the 5 blocks we KEEP must all still be CLOSED blocks after the cut
for idx, tag in ((0, b"c3623"), (3, b"c3622"), (9, b"c3621"), (15, b"c3618"), (21, b"c3619")):
    assert pre_lines[idx].startswith(b"- [x] **CLOSED " + tag), pre_lines[idx][:60]

part_a = pre_lines[A_START:A_END + 1]
assert len(part_a) == 18, len(part_a)

# ---------------- PART B boundaries ----------------------------------------
B = 148  # 0-indexed; live line 149
assert pre_lines[B].startswith(
    b"- [ ] **NEW c3162 (MEDIUM) -- triage `state/audit_data/c3162_vendor_catalogue.json`"
), pre_lines[B][:120]
assert pre_lines[B - 1] == b"", repr(pre_lines[B - 1])
assert pre_lines[B + 1] == b"", repr(pre_lines[B + 1])
old_c3162 = pre_lines[B]
assert len(old_c3162) > 5000, len(old_c3162)

# Carry the RESUME POINTER over byte-for-byte: slice, do not retype.
old_txt = old_c3162.decode("utf-8")
# NB: in the pre-image the RESUME POINTER's opening `**` is closed by the `**`
# that opens the (now-archived) c3622 recap, so the slice itself is unbalanced
# markdown -- re-close it explicitly rather than editing the carried bytes.
_i = old_txt.index("**RESUME POINTER (updated c3623,")
_j = old_txt.index("). **c3622 (rows 869-874)") + 2
resume = old_txt[_i:_j]
assert resume.count("**") == 1, resume.count("**")
resume += "**"
assert "881 `northbell/job-dedupe-merge`" in resume
assert "886 `northbell/internshala-scraper`" in resume
assert len(resume) > 1200, len(resume)

new_c3162 = (
    "- [ ] **NEW c3162 (MEDIUM) -- triage `state/audit_data/c3162_vendor_catalogue.json` "
    "(1,485 rows, already sorted by `users` descending) top-down.** Read each row's own LIVE "
    "README/pricing (confirm it is actually public and not deprecated, read past the title for "
    "scope exclusions, and check whether our own README's existing generic prose already covers "
    "it before calling it \"new\"). 6 rows is the standing batch size; this is a FALLBACK for "
    "cycles with no real backlog, never a reason to skip one. "
    "**COMPRESSED c3624 -- the full 5,945B predecessor of this block is verbatim in "
    "`tasks/queue_archive.md`, `## Archived by cycle 3624`.** What was cut: (a) the c3622/c3623 "
    "per-batch recap PARAGRAPHS, which are exactly the batch paragraphs this block's own closing "
    "rule forbids and which are already triple-recorded (each cycle's `state/STATUS.md` record, "
    "its `CLOSED cNNNN` block, and the tracker's FINDS INDEX above -- verified at c3624, both "
    "handles present there with their terse parentheticals); (b) the dead top-20-by-users starter "
    "list (rows 1-880 are long done); (c) the c3332/c3492 archival meta-history. "
    "**The `cps`-vs-`bin/_unit_price.py` module-identity note that used to sit here was the ONLY "
    "copy of a real method gotcha, so it is RELOCATED c3624 to `notes/PLAYBOOK.md`, "
    "`## Vendor-catalogue triage -- the fixed per-batch method`, VERBATIM** (the c3492 lesson: "
    "grep for the METHOD sentences inside a block before archiving the narrative around them). "
    "**ALL OF THE METHOD LIVES IN `notes/PLAYBOOK.md` AND ALL OF IT IS MANDATORY, NOT OPTIONAL: "
    "`## Vendor-catalogue triage -- the 7 standing ruling buckets`** (reach for a bucket before "
    "writing a new ruling; run its two cheap pre-screens and buckets 7 and 8 BEFORE drafting any "
    "disclosure paragraph -- they are the ones that most often turn a \"real find\" into a "
    "non-event), **`### The pointer-verify step -- RUN IT BEFORE EVERY BATCH`** (print "
    "`rows[idx-1]` through `rows[idx+5]` fresh; trust a previous cycle's prose for nothing but "
    "its last-done INDEX, never its handle label -- c3443 caught a real off-by-one that way), "
    "**`## Vendor-catalogue triage -- the fixed per-batch method`**, and **`## Vendor-catalogue "
    "triage -- why the per-batch line keeps regrowing (the c3468/c3516 recording rules)`**. "
    "**RECORDING, in brief: a 0/6 batch gets NO line anywhere** -- it is recorded by its own "
    "cycle's `state/STATUS.md` record plus the tracker's advanced COVERAGE row range, and you "
    "advance the range instead of appending prose. **A batch WITH a find gets ONE TERSE CLAUSE "
    "(handle + at most a short parenthetical) in the tracker's FINDS INDEX, so the `FOLD-IN "
    "REGISTER` can cross-index it. Under no rule, old or new, does a batch PARAGRAPH belong in "
    "this block or in the tracker** -- c3332 re-archived two of them (3.4KB), c3492 re-archived "
    "three more (~5.6KB), and c3624 re-archived the c3622/c3623 pair. Do not paste one here "
    "again. Expect a high false-positive rate from the OWNER-bucket gap documented in "
    "`CLOSED c3162` (archived by the c3172 trim): many rows are already disclosed generically, "
    "just not under their exact slug. " + resume
).encode("utf-8")

# ---------------- build the new live file ---------------------------------
post_lines = list(pre_lines)
post_lines[B] = new_c3162
del post_lines[A_START:A_END + 1]
post = b"\n".join(post_lines)

# ---------------- losslessness: multiset identity BEFORE the write --------
archived = part_a + [old_c3162]
pre_nb = Counter(l for l in pre_lines if l.strip())
post_nb = Counter(l for l in post_lines if l.strip())
arch_nb = Counter(l for l in archived if l.strip())
missing = pre_nb - (post_nb + arch_nb)
assert not missing, "WOULD LOSE LINES: %r" % [l[:90] for l in missing]
added = (post_nb + arch_nb) - pre_nb
assert list(added) == [new_c3162], "unexpected new content: %r" % [l[:90] for l in added]

if "--dry-run" in sys.argv:
    print("DRY RUN ok: %d -> %d bytes (%+d), %d -> %d lines; archiving %d lines"
          % (pre_bytes, len(post), len(post) - pre_bytes,
             len(pre_lines), len(post_lines), len(archived)))
    sys.exit(0)

# ---------------- write: archive FIRST, then the live file -----------------
shutil.copy2(QUEUE, QUEUE + ".c3624.pre")
header = "\n\n## Archived by cycle %d\n\n" % CYCLE
body = (
    "### PART A -- RULE 6b floor-5 rotation: the 3 oldest-by-position `CLOSED` blocks "
    "(c3620, c3617, c3616), verbatim\n\n"
    + "\n".join(l.decode("utf-8") for l in part_a)
    + "\n\n### PART B -- the full pre-compression `NEW c3162` block (5,945B on one line), "
      "verbatim\n\n"
    + old_c3162.decode("utf-8")
    + "\n"
)
with open(ARCHIVE, "a", encoding="utf-8") as fh:
    fh.write(header + body)
with open(QUEUE, "wb") as fh:
    fh.write(post)

# ---------------- independent post-write re-verify ------------------------
live_now = open(QUEUE, "rb").read().split(b"\n")
arch_now = open(ARCHIVE, "rb").read().split(b"\n")
have = Counter(l for l in live_now if l.strip()) + Counter(l for l in arch_now if l.strip())
still_missing = [l for l in pre_nb if have[l] < 1]
assert not still_missing, "POST-WRITE LOSS: %r" % [l[:90] for l in still_missing]
print("WROTE. %d -> %d bytes (%+.1f KB), %d -> %d lines. 0 lines lost (re-verified "
      "against the pre-image, %d distinct non-blank lines checked)."
      % (pre_bytes, len(post), (len(post) - pre_bytes) / 1024.0,
         len(pre_lines), len(post_lines), len(pre_nb)))
print("archive now %.1f MB" % (os.path.getsize(ARCHIVE) / 1048576.0))
