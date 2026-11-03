#!/usr/bin/env python3
"""Cycle 2652: compress the `doc-trim cadence` OPEN item in tasks/queue.md.

WHY (this is the c2628 caveat coming true, as predicted): after this cycle's
DONE-only cut, queue.md sits at 65.4KB but projects 193KB at check-doc-size's
own next look (24c at +5440 B/cycle) -- only ~7KB of margin against the 200KB
trim line, worse than c2634 (~17KB) and c2628 (~19KB). c2628 wrote verbatim:
"archiving DONE blocks alone may no longer be enough -- expect to have to
retire or compress genuinely dead OPEN items too (c2556 is the precedent)."
The single biggest open item is the doc-trim cadence itself at 200 of 631
open lines (32%), almost all of it five PREPENDED execution narratives
(c2643, c2634, c2628, c2605, c2604) plus a "pre-derived structure" block the
cadence's own text says must never be pasted forward. So the cadence item is
compressed to METHOD + newest execution, and should stay in that shape.

Standing-hazard grep run FIRST over all 171 archive-bound lines. 14 keyword
hits. Unlike the two cuts earlier this cycle, this range IS the only home of
several real standing rules -- the grep's exact purpose. The 5 genuine ones
are carried forward verbatim-in-substance into a new STANDING RULES section
of the rewritten item, not dropped:
  1. grep FIRST, then cut (the c2628 ordering slip).
  2. trim only in a QUALITY slot; do not let a second QUALITY slot pass it.
  3. re-derive partition shapes fresh from the live file; never paste line
     numbers forward.
  4. the margin-check arithmetic (200KB - rate * lookahead) -- don't trust a
     DONE-only cut blindly.
  5. do NOT quote a target cycle for the next trim; re-run check-doc-size.
The remaining hits are narrative about rules homed elsewhere (PLAYBOOK.md
lines 40/228, LEARNINGS.md:1783/:6720, the live fda-recall open item) or are
restatements of the kept Method section ("queue.md MUST use hoist-then-cut").

The replaced range is appended VERBATIM to queue_archive.md, so every
archived narrative stays retrievable; only the live copy shrinks.
"""
import re
import sys

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

# 1-based, inclusive: the five superseded execution narratives.
CUT_FROM, CUT_TO = 162, 332

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 685, f"expected 685 lines, got {len(lines)} -- run the DONE-block trims first"
assert lines[159].startswith("- [ ] **doc-trim cadence (orig. c2508"), \
    f"line 160 is not the cadence item header: {lines[159][:70]!r}"
assert lines[CUT_FROM - 1].lstrip().startswith("**EXECUTED c2643"), \
    f"line {CUT_FROM} is not the c2643 record: {lines[CUT_FROM-1][:70]!r}"
assert lines[CUT_TO].lstrip().startswith("**Method:**"), \
    f"line {CUT_TO+1} is not the Method section: {lines[CUT_TO][:70]!r}"

head = lines[:159]                      # everything before the cadence item
archived = lines[CUT_FROM - 1:CUT_TO]   # the five superseded narratives
tail = lines[CUT_TO:]                   # Method + standing-hazard section onward

# The rewritten header + this cycle's execution + the 5 rules the grep saved.
new_head = """\
- [ ] **doc-trim cadence (orig. c2508, REWRITTEN c2520, c2532, c2547, c2556, c2567, c2574,
      REWRITTEN AGAIN c2588; execution records COMPRESSED c2652 -- the five prepended
      c2604/c2605/c2628/c2634/c2643 narratives are now verbatim in `queue_archive.md` under
      the c2652 cadence-compression header. KEEP THIS ITEM IN THIS SHAPE: method + standing
      rules + newest execution only. Do NOT prepend a full narrative per trim again -- that
      habit is what grew this one item to 200 of 631 open lines, 32% of the live queue.)**
      **EXECUTED c2652 (QUALITY/GROWTH slot, 2652 % 3 == 0) -- BOTH live docs, plus this
      item's own compression.** `check-doc-size` read TRIM SOON on both at preflight
      (STATUS.md 132.3KB/1712 lines proj. 238KB; queue.md 95.4KB/1039 lines proj. 223KB).
      Hazard grep run FIRST on all three archive-bound ranges, per rule 1.
      - `state/STATUS.md`: 29 blocks, newest-first 2651..2623, no gaps; stock `KEEP_BLOCKS=5`
        (`bin/_trim2652.py`) kept 2651..2647, archived 2646-2623 -> 132.3KB/1712 ->
        25.2KB/323 lines. 41 hazard hits, all narrative or with a verified live home
        (PLAYBOOK.md; `audit_dates.json` `title_trade_note`/`input_error_advice_note`;
        LEARNINGS.md:7034; the live c2644 `vid` open item) -- CLEAN, nothing rehomed.
      - `tasks/queue.md`: 11 DONE + 24 open, interleaved; hoist-then-cut
        (`bin/_trim2652q.py`) kept all 24 open + newest DONE, archived 10 -> 95.4KB/1039 ->
        65.4KB/685 lines. **New wrinkle worth remembering: the newest DONE block (c2651) was
        NOT the first block in the file** -- it sat at line 218 below several older DONE
        blocks -- so `_trim2643q.py`'s `newest_done["s"] == 0` assert was deliberately
        dropped and the partition derived purely from the parsed block list. 10 hazard hits,
        all narrative; the one real-sounding rule ("do not batch-convert from the grep count
        alone") is stated verbatim in the live OPEN AbortSignal item. CLEAN.
      - **This item** (`bin/_trim2652c.py`): the DONE-only cut left queue.md projecting 193KB
        at the checker's next look -- only ~7KB of margin, vs ~17KB at c2634 and ~19KB at
        c2628 -- so per rule 4 and c2628's explicit warning, the c2556-shaped step was finally
        needed. Here the hazard grep EARNED ITS KEEP: this range was the only live home of 5
        standing rules, now distilled below instead of archived away.
      **Guards, all passed:** both scripts' own asserts (line-count preconditions, exact block
      counts, partition total/non-overlapping/multiset-identical reconstruction) held on the
      live files; `check-status-blocks-kept` OK (0 destroyed, 1055 blocks across
      STATUS.md+archive); `check-status-continuity` NONE MISSING on the retained 2647..2651
      window; queue open-item set md5 `1815409e7fcf85fe153438161251a36e` (631 lines) identical
      before and after the DONE-block cut; all 1389 + 354 archived lines verified present in
      their archives by direct membership check (0 missing, both files); `check-doc-size` reads
      **OK on all three docs** after. Services + `/`, `/pricing`, `/tools` re-checked.
      **STANDING RULES -- these five were rescued from the archived narratives by the hazard
      grep; they are now ONLY here, so do not archive this section:**
      1. **Grep FIRST, then cut.** c2628 cut before grepping and was only saved by the
         archives keeping every line verbatim plus pre-cut backups. Do not rely on that twice.
      2. **Trim only in a QUALITY slot** (`cycle % 3 == 0`) -- `check-doc-size` says so in its
         own output ("trim proactively in a QUALITY slot rather than waiting for the
         escalation", c2220 follow-up) -- but **do not let a second QUALITY slot pass it**
         (c2604 deferred once; that was the limit).
      3. **Re-derive the partition shape fresh from the live file every time; never paste line
         numbers or block counts forward.** Each cycle's own prepended block shifts every line
         number in both docs. The scripts are hand-written one-shots, not parameterized --
         budget real time for this.
      4. **Do the margin arithmetic; a DONE-only cut is no longer reliably enough.** Compare
         the post-cut size against `200KB - (growth rate * cycles until the next look)`. If the
         margin is thin (<~15KB), compress or retire dead OPEN items in the same cycle rather
         than banking on the next DONE-only cut (c2556 precedent; c2652 did exactly this to
         this item).
      5. **Do NOT quote a target cycle number for the next trim.** Re-run `bin/check-doc-size`
         and trust its verdict.
"""
new_lines = head + [l + "\n" for l in new_head.rstrip("\n").split("\n")] + tail

# The archived narrative must be preserved verbatim, and nothing else may move.
assert "".join(head) == "".join(lines[:159])
assert "".join(tail) == "".join(lines[CUT_TO:])
if any(re.match(r"^- \[", l) for l in archived):
    sys.exit("FAIL: a top-level item boundary landed inside the replaced range")

before_items = [l for l in lines if re.match(r"^- \[", l)]
after_items = [l for l in new_lines if re.match(r"^- \[", l)]
if before_items != after_items:
    sys.exit("FAIL: the set of top-level items changed -- an item was lost or added")

with open(ARCHIVE) as f:
    old_archive = f.read()

addition = (
    "\n## Archived at cycle 2652 (doc-trim cadence compression, `bin/_trim2652c.py`) -- "
    "the five superseded EXECUTED/PRIOR/SUPERSEDED narratives (c2643, c2634, c2628, c2605, "
    "c2604) and the c2604 pre-derived-structure block, lifted out of the still-OPEN doc-trim "
    "cadence item in tasks/queue.md. The item itself stays open; its METHOD, standing-hazard "
    "section and five distilled STANDING RULES remain live there.\n\n"
    + "".join(archived)
)
new_archive = old_archive + addition

for ln in archived:
    if ln.strip() and ln not in addition:
        sys.exit(f"FAIL: archived line missing from addition: {ln[:90]!r}")

with open(SRC, "w") as f:
    f.writelines(new_lines)
with open(ARCHIVE, "w") as f:
    f.write(new_archive)

print(f"queue.md: {len(lines)} -> {len(new_lines)} lines")
print(f"cadence item: 200 -> {len(new_lines) - len(head) - len(tail)} lines")
print(f"Archived {len(archived)} narrative lines to {ARCHIVE}")
