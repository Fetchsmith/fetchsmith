#!/usr/bin/env python3
"""_reloc3636.py -- cycle 3636 PART B step 1 of 2: relocate the METHOD/LESSON
sentences buried inside `NEW c3372` in tasks/queue.md to notes/PLAYBOOK.md,
VERBATIM, before anything is cut (the c3492 lesson: relocate first, then
archive). Only the live tracking state stays in the queue.

Pre-greps done this cycle, both mandatory per the trim cadence:
  * `grep c3372 notes/STANDING.md` -> 0 hits, so no must-stay-live ruling.
  * the METHOD sentences inside the block were grepped individually against
    LEARNINGS.md/PLAYBOOK.md: the DATED-regex lesson (LEARNINGS:4477) and
    the attribution lesson (LEARNINGS:4923) ARE already on file elsewhere,
    but cross-batch lessons (a)/(b)/(d) and the re-stamp/stagger METHOD
    sentences exist NOWHERE ELSE -- archiving the block would have destroyed
    them, same near-miss class as c3492.

Every segment below is SLICED out of the live line by exact substring match
(both end anchors asserted), never retyped.
"""
import sys

QUEUE = "/root/agent/tasks/queue.md"
PLAYBOOK = "/root/agent/notes/PLAYBOOK.md"

lines = open(QUEUE, encoding="utf-8").read().split("\n")
IDX = 86  # 0-indexed; live line 87
src = lines[IDX]
assert src.startswith("- [ ] **NEW c3372 (MEDIUM -- competitor-claim refresh"), src[:90]

def slice_between(start_anchor, end_anchor):
    i = src.index(start_anchor)
    j = src.index(end_anchor, i + len(start_anchor))
    return src[i:j].rstrip()

# --- segment 1: the CLASS 1 / DATED-regex lesson -------------------------
seg_class1 = slice_between(
    "**CLASS 1 CLOSED c3417**",
    "**CLASS 2 is the live work",
)
assert "within 40 chars" in seg_class1 and len(seg_class1) > 400, len(seg_class1)

# --- segment 2: the four cross-batch lessons -----------------------------
seg_lessons = slice_between(
    "**THE FOUR CROSS-BATCH LESSONS",
    "**NEXT BATCH:**",
)
assert seg_lessons.count("(d)") == 1 and "re-fetched" in seg_lessons, len(seg_lessons)

# --- segment 3: the re-stamp / stagger / no-truncation METHOD ------------
i = src.index("**METHOD: a date may only be re-stamped")
seg_method = src[i:].rstrip()
assert seg_method.endswith("`## Checker output hygiene`.**"), seg_method[-60:]

section = (
    "\n## Competitor-claim refresh method (`NEW c3372` batches) "
    "(RELOCATED here by cycle 3636 from `NEW c3372` in `tasks/queue.md`, "
    "where it had lived since c3372)\n\n"
    "RELOCATED because it is reusable METHOD for running competitor-claim "
    "refresh batches, not tracking state -- the same c3360/c3492/c3498/"
    "c3516/c3627/c3630 lever (relocate method verbatim, leave a one-line "
    "pointer) that is the only one which has ever produced a lasting cut on "
    "`tasks/queue.md`. `NEW c3372` keeps ONLY its live state: the "
    "batches-done coverage list, the NEXT BATCH pointer, and the still-open "
    "`substack-scraper/README.md:215` drift. Text below is verbatim as it "
    "stood at c3636 (block originally c3372, RE-COMPRESSED c3516, "
    "re-censused c3636).\n\n"
    "**The two lessons below that are ALSO on file in `notes/LEARNINGS.md` "
    "(the DATED-regex one at LEARNINGS:4477, the "
    "attribution one at LEARNINGS:4923) are kept here anyway because this "
    "section is where a batch-runner looks; the other four exist nowhere "
    "else.**\n\n"
    "### Class 1 (UNDATED) -- closed, and why the flag over-reports\n\n"
    + seg_class1 + "\n\n"
    "### The four cross-batch lessons (the reusable yield of 11 batches)\n\n"
    + seg_lessons + "\n\n"
    "### Re-stamping dates, and checker-output hygiene\n\n"
    + seg_method + "\n"
)

if "--dry-run" in sys.argv:
    print("DRY RUN ok. would append %d bytes to PLAYBOOK.md" % len(section.encode()))
    print("seg lens: class1=%d lessons=%d method=%d"
          % (len(seg_class1), len(seg_lessons), len(seg_method)))
    sys.exit(0)

with open(PLAYBOOK, "a", encoding="utf-8") as fh:
    fh.write(section)

# independent post-write verify: all three segments must be findable verbatim
pb = open(PLAYBOOK, encoding="utf-8").read()
for name, seg in (("class1", seg_class1), ("lessons", seg_lessons), ("method", seg_method)):
    assert seg in pb, "MISSING VERBATIM IN PLAYBOOK: " + name
print("APPENDED %d bytes to notes/PLAYBOOK.md; all 3 segments verified verbatim."
      % len(section.encode()))
print("class1=%dB lessons=%dB method=%dB" % (len(seg_class1), len(seg_lessons), len(seg_method)))
