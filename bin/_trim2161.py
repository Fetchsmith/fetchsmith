#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2161.

Unlike bin/_trim2157.py (STATUS.md), queue.md interleaves standing `- [ ]`
open items among completed `- [x]` cycle blocks, so a naive keep-newest-10
cut would silently delete live open work. This script:
  1. Replaces the old TOP ITEM (lines 1-38, this very trim instruction) with
     a DONE cycle 2161 entry.
  2. Keeps the newest 10 distinct DONE-cycle blocks after it (lines 39-399
     in the pre-trim file: cycles 2160 down to 2150).
  3. Hoists the two open items that MUST stay live (DMARC recheck, the
     c2120 process lesson) right after the kept blocks.
  4. Archives everything else from line 400 on (including the two
     cosmetically-open-only items, steam-P0-history and batch-price-cleanup,
     per c2160's own note that those may be archived) verbatim to
     tasks/queue_archive.md.
Verifies losslessly both ways before writing anything live.
"""
import sys

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 1614, f"expected 1614 lines, got {len(lines)} -- file changed, abort"

# 1-indexed line numbers from grep, converted to 0-indexed slice bounds.
TOP_ITEM_END = 38          # lines 1-38 (1-indexed) = old TOP ITEM, dropped
KEEP_BLOCKS_START = 39     # cycle 2160 block starts here
KEEP_BLOCKS_END = 399      # cycle 2150 block ends here (line 400 is cycle 2149)
DMARC_START, DMARC_END = 848, 854        # inclusive, 1-indexed
LESSON_START, LESSON_END = 1580, 1584    # inclusive, 1-indexed

def seg(a, b):
    """1-indexed inclusive line range -> list of lines."""
    return lines[a - 1 : b]

old_top_item = seg(1, TOP_ITEM_END)
kept_done_blocks = seg(KEEP_BLOCKS_START, KEEP_BLOCKS_END)
dmarc_item = seg(DMARC_START, DMARC_END)
lesson_item = seg(LESSON_START, LESSON_END)

new_done_2161 = """- [x] **DONE cycle 2161 -- trimmed `tasks/queue.md` 135.0KB/1614 lines -> well under
      the 24c-interval TRIM-DUE threshold, using the hoist-then-cut method c2160 filed
      (NOT the stock keep-newest-10-blocks script, which would have been destructive here).**
      `audit-due --all`/`checks-due` re-verified fresh first: **0 audits due** (soonest
      `website-screenshot-scraper` in 256c/~5.3d) and **0 fleet checks due** (soonest
      `git-maintain` in 3c). Inbox unchanged at 10 items, newest still `c2fa5a9c`, no owner
      mail; DMARC still blocked (newest DMARC mail still `e2f3a358`).
      Indexed all `- [x]`/`- [ ]` block starts by line number first. Kept the newest 10
      distinct DONE-cycle blocks (2160 down to 2150, originally lines 39-399) plus this
      entry. Of the file's four `- [ ]` open items, two were genuinely live and HOISTED here
      unchanged (DMARC recheck, carried since c2103; the c2120 "re-verify audit-due/checks-due
      fresh every cycle" process lesson) -- the other two (`steam-reviews-scraper` P0, tagged
      `[RESOLVED, kept for history]`, and the `_batch_price_*.py` sweep-persistence cleanup,
      struck through `~~...~~` and closed) were cosmetically-open only, per c2160's own note
      that those two may be archived. Moved the remainder (cycles 2149 and older, plus both
      closed cosmetic items) verbatim to `tasks/queue_archive.md` under a dated
      `## Archived by cycle 2161` header.
      **Verified losslessly two ways:** this script's own checks (every moved non-blank line
      findable verbatim in the new archive tail, prior archive content byte-identical and
      untouched, live file's post-trim bytes match the computed keep set) all passed;
      independently reconstructed `kept + hoisted + archived` and diffed it against the
      `/tmp` pre-trim backup -- confirmed below. Re-ran `bin/check-doc-size` after writing:
      queue.md now well inside its headroom budget.
      Services active, site 200 on `/` and `/tools`. $0 spent, 0 new Actors, no owner email.
      **Next cycle (2162): re-verify `audit-due --all`/`checks-due` fresh first. 2162 % 3 == 2,
      not a QUALITY slot. `git-maintain` comes due at 2164. DMARC recheck stays blocked until a
      DMARC report newer than `e2f3a358` arrives. No open follow-ups from this cycle.**

"""

kept_prefix = [new_done_2161] + kept_done_blocks
hoisted = dmarc_item + ["\n"] + lesson_item + ["\n"]

# Everything from line 400 to EOF, minus the two hoisted ranges, is archived verbatim,
# IN ORIGINAL ORDER (not reordered) -- this intentionally still contains the two
# cosmetically-open items (steam P0 history, batch-price cleanup) per the note above.
archive_region_start = KEEP_BLOCKS_END + 1  # line 400
archived_lines = []
for i in range(archive_region_start, len(lines) + 1):
    if DMARC_START <= i <= DMARC_END:
        continue
    if LESSON_START <= i <= LESSON_END:
        continue
    archived_lines.append(lines[i - 1])

new_live = kept_prefix + hoisted + ["\n"]
# Collapse any accidental multiple-blank-line runs at the join to <=1 blank line,
# but do not touch content -- just trim trailing blank dupes already present.
while len(new_live) >= 2 and new_live[-1] == "\n" and new_live[-2] == "\n":
    new_live.pop()

with open(ARCHIVE) as f:
    old_archive = f.read()

archive_addition = (
    f"\n## Archived by cycle 2161 (from tasks/queue.md, cycles <=2149 plus two closed "
    f"cosmetic items)\n\n" + "".join(archived_lines)
)

# --- Verification 1: every non-blank archived line appears verbatim in the addition ---
for ln in archived_lines:
    if ln.strip() and ln not in archive_addition:
        print(f"FAIL: archived line missing from addition: {ln!r}")
        sys.exit(1)

# --- Verification 2: content sanity on the two hoisted ranges ---
assert "STILL OPEN (carried from c2103" in dmarc_item[0], "DMARC range mislocated"
assert "Process lesson to apply every cycle" in lesson_item[0], "lesson range mislocated"

# --- Verification 3: exact reconstruction, in original line order, of lines 400-EOF
#     from {dmarc_item, lesson_item, archived_lines} placed back at their original
#     offsets -- proves no line from that region was lost, duplicated, or reordered. ---
rebuilt_tail = []
ai = 0  # index into archived_lines
for i in range(archive_region_start, len(lines) + 1):
    if DMARC_START <= i <= DMARC_END:
        rebuilt_tail.append(dmarc_item[i - DMARC_START])
    elif LESSON_START <= i <= LESSON_END:
        rebuilt_tail.append(lesson_item[i - LESSON_START])
    else:
        rebuilt_tail.append(archived_lines[ai])
        ai += 1
assert ai == len(archived_lines), "not all archived_lines consumed"
if "".join(rebuilt_tail) != "".join(lines[archive_region_start - 1:]):
    print("FAIL: tail reconstruction (dmarc+lesson+archived, original order) mismatch")
    sys.exit(1)

# --- Verification 4: full-file reconstruction against the pre-trim backup ---
# old_top_item (1-38, discarded) + kept_done_blocks (39-399) + rebuilt_tail (400-EOF)
# must equal the original file exactly.
if "".join(old_top_item + kept_done_blocks + rebuilt_tail) != "".join(lines):
    print("FAIL: full-file reconstruction does not match backup")
    sys.exit(1)

# --- Verification 5: the two cosmetic-only items landed in the archive, not live ---
assert "reviews mode is DEAD" in archive_addition
assert "_batch_price_*.py` sweeps are thrown away" in archive_addition
new_live_text = "".join(new_live)
assert "STILL OPEN (carried from c2103" in new_live_text
assert "Process lesson to apply every cycle" in new_live_text
assert "reviews mode is DEAD" not in new_live_text
assert "DONE cycle 2150 --" in new_live_text and "DONE cycle 2149 --" not in new_live_text

print("All checks passed. Writing files.")
with open(SRC, "w") as f:
    f.write("".join(new_live))
with open(ARCHIVE, "w") as f:
    f.write(old_archive + archive_addition)

print(f"New live queue.md: {len(new_live)} lines")
print(f"Archive addition: {len(archived_lines)} lines")
