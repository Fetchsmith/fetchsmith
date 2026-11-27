#!/root/agent/venv/bin/python
r"""Cycle 3804 tasks/queue.md floor-3 rotation -- the trim STATUS.md c3803 reserved for
this QUALITY slot (file read TRIM DUE at 215.7KB/1013 lines, ~-3 cycles of headroom,
+5440 B/cycle, projected past the 256KB Read cap). Clone of _trim3795q.py BY NAME,
which is the live descendant of the mandated _trim3748q.py lineage (notes/PLAYBOOK.md):
it carries the c3748 widened GUARD-2 regex AND c3795's RESOLVED_NEARBY exemption, both
re-verified present in this file before cloning rather than assumed.

CENSUS RE-DERIVED FRESH (c3804, not inherited from c3795/c3798): a per-block byte/line
census of all 128 top-level heads found 9 CLOSED "report-shaped" blocks, newest-to-
oldest: c3803, c3802, c3801, c3799, c3798, c3797, c3795, c3794, c3793. Floor 3
(STANDING c3280 / c3672 cadence) = keep newest 2 (c3803, c3802) + this cycle's own
block, so the cut is EVERY report block from c3801 down to c3793.

SPAN A = c3801 report through c3793 report: 8 blocks (c3801/c3799/c3798/c3797/c3795/
CLOSED-c3795a/c3794/c3793). `CLOSED c3795a` is a one-off, already-resolved closure with
no residue (its finding -- that FOLD-IN REGISTER and COMPRESSED c2994 are NOT
relocatable -- is restated in this cycle's own block so it is not lost), swept up in
the same contiguous span. The span ends immediately before the `CLOSED c3792` one-line
closure note, which SPAN B handles.

SPAN B = the `CLOSED c3792` one-liner PLUS the still-`- [ ]` `NEW c3792` HIGH block
(1,919B), replaced in place by a single one-line closure note. This is a deliberate
CORRECTNESS fix, not just a byte cut: `NEW c3792` asked for the overdue queue.md trim,
that trim RAN at c3795 (and `CLOSED c3792` right above it says so), yet the flag was
left open with every number in it now wrong (it says 232.6KB, "-6 cycles", and "do it
in the NEXT QUALITY slot (c3795)" -- a cycle 9 slots in the past). That is exactly the
failure the c3768 LESSON names: do NOT leave one-shot "do X at cycle N" flags open for
work a STANDING item (here STANDING c3280) already owns, because by cycle N their
counts are stale and they compete with the standing item. Its method advice ("per-entry
caps never hold; the only lasting levers are relocation and archiving oldest CLOSED
blocks") is NOT lost -- it is verbatim in notes/PLAYBOOK.md's
"## Doc-size trim cadence for tasks/queue.md" section, confirmed by direct read before
cutting, and the full block text is archived verbatim below.

GUARD 1 is therefore deliberately scoped: span A is asserted to contain NO open item;
span B is KNOWN to contain exactly one (`NEW c3792`), asserted to be exactly that one
by its literal head text, so a drifted boundary still fails loudly.

HAZARD GREP (3-pass, run before this script was written):
(a)/(b) whole-repo grep for each cut cycle's `cNNNN\b` outside queue.md/queue_archive.md
    returned only (i) state/STATUS.md's own per-cycle entries -- the established
    "state/STATUS.md cycle N entry" pointer convention that survives every rotation
    unedited, and c3797/c3795/c3793 are all still inside STATUS.md's own newest-9
    window anyway -- and (ii) the self-contained docstrings of bin/_trim3795q.py and
    bin/_reloc3798q.py, which cite their own cycle as history and need no queue.md
    narrative to resolve. Nothing to relocate.
(c) intra-file: every `NEW cNNNN` identifier mentioned inside the spans (c3162, c3488,
    c3492, c3568, c3744a, c3744b, c3768, c3784, c3792, c3795a) was checked by script
    for a live top-level definition OUTSIDE the spans -- all 10 present. Every in-span
    mention is a backward reference, never a hidden definition. Live "see CLOSED cNNNN
    above" pointers whose target moves to the archive are covered by NEW c3492's
    standing ruling (they resolve in queue_archive.md under the per-cycle header) and
    are deliberately left unedited.

GUARD 2 (c3724/c3748 widened regex, c3795 exemption): scripted scan of span A for
nested `\s+(?:- )?\*\*`?NEW c\d+[a-z]?`?\b` sub-bullets that are not already-closed
narrative -- ZERO found, nothing to promote. Re-asserted below so it cannot be
satisfied cosmetically.

STILL-LIVE FACTS CARRIED OUT OF THE CUT BLOCKS (so nothing actionable leaves with
them): both c3797 "filed for the next push" disclosure candidates have SHIPPED
(cleanscrape/google-news-scraper at c3799, ctriolab/ats-jobs-feed at c3802); c3797's
bucket-3 "checked, confirmed NOT a threat, do not re-check" pair
(ctriolab/hackernews-scraper, cleanscrape/career-site-jobs-scraper) is restated in this
cycle's own CLOSED c3804 block; c3801's feature_diff_audit result is stamped in
state/audit_dates.json, not only in prose.
"""
import re
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

orig = open(QUEUE).read()
NESTED = re.compile(r"^\s+(?:- )?\*\*`?NEW c(\d+[a-z]?)`?\b", re.M)
RESOLVED_NEARBY = re.compile(r"`?NEW c\d+[a-z]?`?\s*(?:--\s*)?(CLOSED|SHIPPED|RESOLVED)\b")

SPAN_A_START = "- [x] **CLOSED c3801 -- QUALITY slot (3801 % 3 == 0"
SPAN_A_NEXT = "- [x] **CLOSED c3792 (the overdue `tasks/queue.md` trim this item flagged HIGH)"
SPAN_B_START = SPAN_A_NEXT
SPAN_B_NEXT = "- [x] **CLOSED c3789 (was `NEW c3768`)"

a_start = orig.index(SPAN_A_START)
a_end = orig.index(SPAN_A_NEXT)
span_a = orig[a_start:a_end]

b_start = orig.index(SPAN_B_START)
b_end = orig.index(SPAN_B_NEXT)
span_b = orig[b_start:b_end]

# --- boundary asserts: a drifted line must fail loudly, never cut the wrong place ---
assert a_start < a_end == b_start < b_end, "span ordering drifted -- re-locate before cutting"
assert orig.count(SPAN_A_START) == 1 and orig.count(SPAN_A_NEXT) == 1
assert orig.count(SPAN_B_NEXT) == 1
assert span_a.count("\n- [x] **CLOSED c") + 1 == 8, \
    f"span A block count unexpected: {span_a.count(chr(10) + '- [x] **CLOSED c') + 1}"
for cyc in ("3801", "3799", "3798", "3797", "3795", "3795a", "3794", "3793"):
    assert f"c{cyc}" in span_a, f"span A missing expected block c{cyc}"
# the two kept report blocks and the one-off boundary must never be swallowed
assert "CLOSED c3803" not in span_a and "CLOSED c3803" not in span_b
assert "CLOSED c3802" not in span_a and "CLOSED c3802" not in span_b
# c3748 lesson, re-earned live at c3804: anchor this to a top-level HEAD, never to bare
# narrative text -- the c3795 block (inside span A) MENTIONS "CLOSED c3789 (was NEW
# c3768)" while explaining where its own cut ended, and a substring assert fired on it.
assert not re.search(r"^- \[[ x]\] \*\*CLOSED c3789 \(was", span_a, re.M)
assert not re.search(r"^- \[[ x]\] \*\*CLOSED c3789 \(was", span_b, re.M)
for keep in ("3789a", "3789b", "3789c", "3768 (was", "3744a", "3744b", "3720a", "3731a"):
    assert keep not in span_b, f"span B unexpectedly swallowed {keep}"

# --- GUARD 1, scoped: span A holds no open item; span B holds exactly NEW c3792 ---
assert not re.search(r"^- \[ \] \*\*", span_a, re.M), "SPAN A CONTAINS AN OPEN ITEM -- refusing"
open_b = re.findall(r"^- \[ \] \*\*.{0,60}", span_b, re.M)
assert len(open_b) == 1, f"span B open-item count unexpected: {open_b}"
assert open_b[0].startswith("- [ ] **NEW c3792 (HIGH -- the first genuinely OVERDUE"), \
    f"span B open item is NOT the stale c3792 flag -- refusing: {open_b[0]!r}"

# --- GUARD 2 (c3724/c3748): promote nested actionables, never strand -------------
for name, span in (("A", span_a), ("B", span_b)):
    nested = [l for l in span.split("\n") if NESTED.match(l)]
    live = [l for l in nested if not RESOLVED_NEARBY.search(l)]
    found = sorted(NESTED.match(l).group(1) for l in live)
    assert found == [], f"span {name} unexpected nested set {found} -- promotion needed"

CLOSURE_NOTE = (
    "- [x] **CLOSED c3792 -- the overdue `tasks/queue.md` trim this item flagged HIGH "
    "ran at c3795 (floor-3 rotation, 244,984B -> 199,874B, `bin/_trim3795q.py`); the "
    "flag itself was then left OPEN for 9 slots with every number in it stale, so "
    "c3804 closed it per the `c3768` lesson (do not leave one-shot \"do X at cycle N\" "
    "flags open for work `STANDING c3280` owns). Its method advice survives verbatim in "
    "`notes/PLAYBOOK.md`, `## Doc-size trim cadence for tasks/queue.md`; full original "
    "text in `tasks/queue_archive.md`, `## Archived by cycle 3804`.**\n"
)

# --- build the new live file in MEMORY (verify, THEN write) ----------------------
new_text = orig[:a_start] + CLOSURE_NOTE + orig[b_end:]

archive_text = (
    "\n## Archived by cycle 3804 (floor-3 report-block rotation + the stale `NEW c3792`\n"
    "## flag it closed. SPAN A: CLOSED c3801/c3799/c3798/c3797/c3795/c3795a/c3794/c3793\n"
    "## (8 blocks; c3795a is a resolved one-off with no residue). SPAN B: the `CLOSED\n"
    "## c3792` one-liner plus the still-open `NEW c3792` HIGH flag, whose work had\n"
    "## ALREADY been done at c3795 -- replaced in the live file by one closure line.\n"
    "## 0 nested actionables found in either span, nothing to promote. Live \"see CLOSED\n"
    "## cNNNN above\" pointers now resolve here per `NEW c3492`'s standing ruling.)\n\n"
    + span_a.rstrip("\n") + "\n\n" + span_b.rstrip("\n") + "\n"
)

def nb(s):
    return [l for l in s.split("\n") if l.strip()]

# nb(new) + nb(removed) == nb(orig) + the one new closure line  (compare BY VALUE)
removed = Counter(nb(span_a)) + Counter(nb(span_b))
assert Counter(nb(new_text)) + removed - Counter(nb(CLOSURE_NOTE)) == Counter(nb(orig)), \
    "LOSSLESS CHECK FAILED -- nothing written"
assert span_a.rstrip("\n") in archive_text and span_b.rstrip("\n") in archive_text
for cyc in ("3801", "3799", "3798", "3797", "3795", "3794", "3793", "3792"):
    assert f"c{cyc}" in archive_text
# the kept blocks must still head the live file
assert new_text.index("CLOSED c3803") < new_text.index("CLOSED c3802") < new_text.index("CLOSED c3792")

with open(ARCHIVE, "a") as fh:
    fh.write(archive_text)
with open(QUEUE, "w") as fh:
    fh.write(new_text)

print(f"queue.md {len(orig):,}B -> {len(new_text):,}B  ({len(new_text) - len(orig):+,}B)")
print(f"lines {orig.count(chr(10)):,} -> {new_text.count(chr(10)):,}")
print(f"archived {len(archive_text):,}B under '## Archived by cycle 3804'")
