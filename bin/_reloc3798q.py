#!/root/agent/venv/bin/python
"""Cycle 3798 tasks/queue.md RELOCATION -- the lever `NEW c3795a` filed: floor-3
rotation alone is at equilibrium (STANDING c3280 note), so the next real byte lever
is relocating a redundant narrative block, not cutting another report block.

TARGET: the `NEW c3744a` block (top-level bullet + its one nested `RAN c3784`
continuation line) -- confirmed by c3795's own hazard grep, and re-confirmed fresh
this cycle by direct read, to be FULLY duplicated in notes/LEARNINGS.md:
  - the c3784 probe narrative (17 guessed names, baseline 493/491, positive
    controls fOffices:['ZZ']/fNiceClass:['99'] -> 0, garbage control
    fTotallyMadeUpParam -> 493 unchanged) is verbatim in LEARNINGS.md "## c3784 --
    probing an undocumented upstream's filter params" (lines ~7167-7196).
  - the c3790 JS-bundle breakthrough (adFrom/adTo, rdFrom/rdTo, registrationNumber;
    the 2-letter-abbreviation pattern explaining why the 17 guesses were doomed) is
    verbatim in LEARNINGS.md "Cycle 3790" paragraph (2) (lines ~7202-7204).
  - the shipped resolution (build 0.1.127, appName still open) is already recorded
    in CLOSED c3791 elsewhere in this same file -- not lost by this relocation.

This is RELOCATION, not a rewrite-from-memory: the full original text is appended
verbatim to tasks/queue_archive.md before the live copy is replaced with a pointer.

HAZARD GREP before cutting: whole-repo grep for `c3744a` outside queue.md/
queue_archive.md/STATUS.md -- hits are LEARNINGS.md's own lesson paragraphs (the
relocation target itself) and main.js history comments; nothing depends on the
queue.md copy to resolve. Intra-file: `NEW c3744b` (still live, L43 pre-edit) and
the `NEW c3784` gate-closure (L40 pre-edit) both say "see ... NEW c3744a above" --
both are backward prose references to the item's EXISTENCE/resolution, not to the
probe narrative being cut, and `NEW c3744a`'s own top-level line survives (compressed,
not removed), so neither pointer breaks.
"""
import re
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

orig = open(QUEUE).read()

TARGET_START = "- [x] **`NEW c3744a` -- CLOSED c3791:"
TARGET_NEXT = "- [x] **`NEW c3784` CLOSED c3788"

t_start = orig.index(TARGET_START)
t_end = orig.index(TARGET_NEXT)
target = orig[t_start:t_end]

assert target.count("\n") == 2, f"target shape unexpected ({target.count(chr(10))} newlines, expected 2 (top line + nested line + trailing blank))"
assert "appName" in target and "0.1.127" in target and "17 candidate" in target

REPLACEMENT = (
    "- [x] **`NEW c3744a` -- CLOSED c3791: shipped build `0.1.127` (date-range + "
    "registration-number filters: `adFrom`/`adTo`, `rdFrom`/`rdTo`, `registrationNumber`). "
    "RELOCATED c3798 (`NEW c3795a`'s lever): the full c3784 negative-guess-probe narrative "
    "(17 names, baseline 493/491, positive/garbage controls) and the c3790 "
    "TMview-JS-bundle breakthrough (why the guesses were doomed, how the real names were "
    "found) are kept verbatim in `notes/LEARNINGS.md` (\"## c3784 -- probing an undocumented "
    "upstream's filter params\" and the \"Cycle 3790\" paragraph right after it) -- read "
    "there, do not re-derive. Residue still genuinely open: `appName` (owner/applicant) "
    "changes behaviour but its match semantics are unproven -- do not ship it without new "
    "evidence. `filingFrom`/`filingTo`/`expiryFrom`/`expiryTo`/`priorityFrom`/`priorityTo`/"
    "`publicationFrom`/`publicationTo` are a confirmed clean WON'T-FIX (`DSVIEW_FIELDS`-only, "
    "not honored on this endpoint). Original full text archived verbatim in "
    "`tasks/queue_archive.md` (`## Archived by cycle 3798`).**\n"
)

new_text = orig[:t_start] + REPLACEMENT + orig[t_end:]

archive_text = (
    "\n## Archived by cycle 3798 (RELOCATION, not a report-block rotation -- the "
    "`NEW c3744a` probe-history block, superseded in the live file by a pointer to "
    "notes/LEARNINGS.md per NEW c3795a)\n\n"
    + target.rstrip("\n") + "\n"
)

def nb(s):
    return [l for l in s.split("\n") if l.strip()]

removed = Counter(nb(target))
kept_check = Counter(nb(new_text)) + removed - Counter(nb(REPLACEMENT))
assert kept_check == Counter(nb(orig)), "LOSSLESS CHECK FAILED"
assert target.rstrip("\n") in archive_text
for marker in ("17 candidate", "adFrom", "appName", "0.1.127", "DSVIEW_FIELDS"):
    assert marker in archive_text, f"archive missing {marker}"

open(QUEUE, "w").write(new_text)
open(ARCHIVE, "a").write(archive_text)
print(f"OK. queue.md {len(orig)} -> {len(new_text)} bytes (-{len(orig)-len(new_text)})")
print(f"   relocated block {len(target)}B -> replacement {len(REPLACEMENT)}B")
