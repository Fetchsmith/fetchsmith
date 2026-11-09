#!/usr/bin/env python3
"""c2958 trim of tasks/queue.md, part 2 -- a REWRITE, not a pure cut.

The first c2958 pass (bin/_trim2958q.py, DONE-block floor cut) brought queue.md to
132.3KB/1607ln but check-doc-size still read TRIM DUE: the forward-looking projection
(+5440 B/cycle over its 24c interval) puts it at ~260KB at the checker's next look,
just over the 256KB Read cap, so margin-arithmetic rule 4 applies ("compress or retire
dead OPEN items in the same cycle rather than banking on the next DONE-only cut").

The c2953 backlog item (live lines 1-136, 136 lines / ~7KB) is the largest open item in
the file and is ripe: cycles 2954/2955/2956/2957 have each closed a chunk of it in place
with ~~strikethrough~~ DONE markers, so the bulk of its bytes are now a closure history
that is ALSO fully narrated in this file's own still-live c2954/c2955/c2956/c2957 DONE
blocks (lines 137-240) and in queue_archive.md / STATUS.md. Rewriting it to just the
current remainder (same shape as c2940's c2809 rewrite) loses no live information.

Original archived verbatim (rule 1 applies to a rewrite too: read it in full first).
"""
import os
import re
import sys
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
BACKUP = "/tmp/c2958_queue2.bak"
HEADER = "## Archived by cycle 2958 part 2 (2026-11-09) -- REWRITE, not a cut"

A, B = 1, 136  # the c2953 backlog item, blank line 136 included... wait verify below

NEW_TEXT = """\
- [ ] **NEW c2953 backlog (REWRITTEN c2958 -- full per-handle history for the CLOSED
      chunks below is archived verbatim; this item now carries only the open remainder).
      Fleet sweep after the cross-paragraph-disagreement check found 22 stale + 12
      disagree + 16 undated. Same shape as the closed c2809 backlog -- pick up in a
      QUALITY slot.**
      **Closed so far, full narrative in each cycle's own still-live DONE block above
      or in `queue_archive.md`/`STATUS.md`:** `sam-gov-opportunities-scraper`'s
      `fortuitous_pirate`/`jungle_synthesizer` pair (DONE c2954, a checker
      handle-resolution bug, not a content error) and 2 of its 3 UNDATED paragraphs;
      `hacker-news-scraper`'s `carmine_tennis`/`rbbscrap` pair (DONE c2955, one genuine
      whole-account removal, one already-disclosed rename needing only a pointer);
      `google-news-scraper` completely -- its 1 DISAGREE + 6 UNDATED (DONE c2956, now
      0/0/0/0 of 77 claims); `google-play-reviews-scraper`'s 8-DISAGREE cluster (DONE
      c2957 -- 7 of 8 were a PHANTOM, correctly self-dated monotonic growth sequences,
      not contradictions; the 1 genuine fix was `apivault_labs` 3->1 users, a real
      same-day decrease).
      **Remainder (arithmetic, NOT a fresh sweep -- RE-MEASURE before trusting, c2809
      lesson (a)): ~20 STALE (1-13 unit drifts, natural, hand-fix) + ~4 real DISAGREE
      (`apple-podcasts-scraper`'s 3: `sourabhbgp` 75v71, `ryanclinton/podcast-directory-
      scraper` 216/207/217, `automation-lab/podcast-scraper` 117v124; plus
      `scholarship-scraper`'s known `majestic_fund` 71v79 standing hold) + ~9 UNDATED
      paragraphs scattered across apple-podcasts/court-records/nih-reporter/remote-jobs/
      trademark-search/uk-find-a-tender/sam-gov-opportunities (2 remaining there).**
      **Standing lesson (c2952, re-confirmed c2957): before fixing a DISAGREE, check
      whether each paragraph carries its OWN date and the values are in date order --
      if so it is a correct growth record, not a bug, same class as the superlative-
      sweep phantom.** No single remaining cluster stands out as the obvious next pick
      -- re-sweep the full fleet fresh first and take the smallest clean file.
"""

orig = open(QUEUE).read()
lines = orig.split("\n")
n = len(lines)

# locate the item end fresh (rule 3: never paste line numbers forward blindly --
# re-derive by finding the next top-level bullet after line 1)
assert lines[0].startswith("- [ ] **NEW c2953 backlog"), f"L1 mismatch: {lines[0][:60]!r}"
end = None
for i in range(1, n):
    if lines[i].startswith("- ["):
        end = i  # 0-indexed; this line starts the NEXT item
        break
assert end is not None, "could not find the next top-level bullet"
assert lines[end - 1].strip() == "", f"L{end} (0-idx) should be the blank line before the next item"
b = end  # 1-indexed inclusive end of the old item = `end` (0-indexed blank line)
print(f"rewriting lines 1-{b} ({b} lines)")

old_block = lines[0:b]

# rule 1: hazard grep the block being rewritten/archived
hazard = re.compile(r"standing|cadence|always |never |do not |must |\brule\b", re.I)
hits = [(i + 1, l) for i, l in enumerate(old_block) if hazard.search(l)]
print(f"rule-1 hazard grep: {len(hits)} hit(s)")
for i, l in hits:
    print(f"  L{i}: {l.strip()[:150]}")
# All standing-hold/lesson references here (majestic_fund, copious_atoll, c2809
# lesson (a), the c2952 dated-growth-record lesson) are independently documented
# live elsewhere in queue.md (verified by grep before writing this script) and are
# also restated in NEW_TEXT below, so archiving the full original is safe.

marker = "<!-- c2958 part 2: REWRITE of the c2953 backlog item, original queue.md lines 1-%d -->" % b
archive_text = "\n".join([HEADER, "", marker] + old_block + [""])

new_lines = NEW_TEXT.rstrip("\n").split("\n") + lines[b:]
new_live = "\n".join(new_lines)

def nb(text):
    return Counter(l for l in text.split("\n") if l.strip())

# Old block minus new block = what moved to archive-only; assert it is fully
# present in archive_text (lossless for the ARCHIVED side); the new text is a
# deliberate rewrite so is NOT asserted equal to the old (rule: assert rewrite
# text separately, per the Method note).
archived_only = nb("\n".join(old_block))
assert nb(archive_text) - nb(marker) - nb(HEADER) == archived_only, "archive is missing original lines"

assert "**NEW STANDING NOTE (c2952, HIGH value" in new_live, "the c2952 standing note (now right after this item) must survive untouched"
assert sum("DONE c2957 (regular slot" in l for l in new_lines) == 1, "the live c2957 DONE block must survive untouched"
assert sum("NEW c2953 backlog" in l for l in new_lines) == 1, "rewritten header must appear exactly once"

if "--dry-run" in sys.argv:
    print(f"\nDRY RUN: {len(orig)}B/{n}ln -> {len(new_live)}B/{len(new_lines)}ln "
          f"({len(orig) - len(new_live)}B saved); archive +{len(archive_text)}B")
    raise SystemExit

open(BACKUP, "w").write(orig)
assert os.path.exists(ARCHIVE), "archive missing -- do not create a second one, investigate"
with open(ARCHIVE, "a") as f:
    f.write("\n" + archive_text + "\n")
open(QUEUE, "w").write(new_live)
print(f"\nqueue.md: {len(orig)}B/{n}ln -> {len(new_live)}B/{len(new_lines)}ln "
      f"({len(orig) - len(new_live)}B saved). Backup {BACKUP}")
