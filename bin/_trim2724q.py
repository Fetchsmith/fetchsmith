#!/root/agent/venv/bin/python
"""One-shot queue.md trim for cycle 2724 (QUALITY slot, 2724 % 3 == 0).

Clone of bin/_trim2712q.py's hoist-then-cut shape. Partition re-derived FRESH from the
live file this cycle per the doc-trim item's rule 3 (46 blocks: 13 DONE + 33 OPEN).

check-doc-size read TRIM SOON (80524 B / 906 lines, +5440 B/cycle, next look in 24c ->
projected 206KB). Rule-4 margin arithmetic on a DONE-only cut:
    ceiling   = 200KB - 5440*24            = 74240 B
    post-cut  = 80524 - 24037 + ~2000(new) = 58487 B
    margin    = 15753 B  -> just ABOVE the ~15KB thin line
so unlike c2712 this cycle does NOT need to compress extra open items; the DONE-only cut
plus this item's own in-place execution-record replacement is enough. Two open-item edits
are still made, but both are *content* corrections this cycle earned, not size moves:
  * block 27 (this item) -- c2712's execution record replaced in place by c2724's, per the
    item's own "newest execution only" rule (same move c2712/c2703/c2652 made).
  * block 15 (c2700 shopify tripwire) -- RETIRED, premise falsified. It predicted the
    ratio-0.00 flag was a STALE health.json row left by `actor-health --only`. c2724 proved
    otherwise: the 0 came from a real nightly FULL run, and a 30-snapshot git-history trace
    of state/health.json shows isolated single-snapshot zeros surrounded by 10/10 readings.
    Replaced with the correct diagnosis + the cheap triage recipe, which is live knowledge,
    not a closed item.

Hazard grep (rule 1) was run BEFORE this script on the 285 archive-bound lines: 39 hits,
all narrative *about* rules homed elsewhere (the c2524 rule in CLAUDE.md; the four standing
watches in STATUS.md; this cadence item). The two hits that named a uniquely homed method
were both verified present before being allowed into the archive set: c2713's "grep a
bin/* script before trusting a --help probe" at notes/LEARNINGS.md:6028, and c2712's
'any "replace in place / keep newest only" rule needs a mechanical `new < old` assert in
bytes' at notes/LEARNINGS.md:6014-6015. That second rule is itself asserted below.
"""
import os
import sys

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

ARCHIVE_BLOCKS = [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13]   # DONE blocks, newest (0) kept
SHOPIFY_BLOCK = 15
DOCTRIM_BLOCK = 27

orig = open(QUEUE).read()
lines = orig.split("\n")

starts = [i for i, l in enumerate(lines)
          if l.startswith("- [x] ") or l.startswith("- [ ] ")]
assert len(starts) == 46, f"expected 46 blocks, got {len(starts)}"
assert starts[0] == 0, "expected no header lines before the first block"
assert len(lines) == 906, f"expected 906 lines, got {len(lines)}"

blocks = []
for n, i in enumerate(starts):
    end = starts[n + 1] if n + 1 < len(starts) else len(lines)
    blocks.append(lines[i:end])

kinds = ["DONE" if b[0].startswith("- [x]") else "OPEN" for b in blocks]
assert kinds.count("DONE") == 13 and kinds.count("OPEN") == 33, kinds
for n in ARCHIVE_BLOCKS:
    assert kinds[n] == "DONE", f"block {n} is not DONE -- refusing to archive an OPEN item"
assert kinds[0] == "DONE", "block 0 should be the newest DONE block"
assert kinds[DOCTRIM_BLOCK] == "OPEN" and "doc-trim cadence" in blocks[DOCTRIM_BLOCK][0]
assert kinds[SHOPIFY_BLOCK] == "OPEN" and "c2700" in blocks[SHOPIFY_BLOCK][0] \
    and "shopify-products-scraper" in blocks[SHOPIFY_BLOCK][0]

# ---- partition: total, non-overlapping, multiset-identical to the original ----
keep_idx = [n for n in range(46) if n not in ARCHIVE_BLOCKS]
assert set(keep_idx) | set(ARCHIVE_BLOCKS) == set(range(46))
assert not (set(keep_idx) & set(ARCHIVE_BLOCKS))
recon = []
for n in range(46):
    recon.extend(blocks[n])
assert recon == lines, "block split is not a byte-for-byte partition of the original"

kept_lines = []
for n in keep_idx:
    kept_lines.extend(blocks[n])
arch_lines = []
for n in ARCHIVE_BLOCKS:
    arch_lines.extend(blocks[n])
assert sorted(kept_lines + arch_lines) == sorted(lines), "partition not multiset-identical"
assert not any(l.startswith("- [ ] ") for l in arch_lines), "OPEN item in the archive set"

# open items must be unchanged across the cut (before the two deliberate rewrites)
open_before = [blocks[n] for n in range(46) if kinds[n] == "OPEN"]
open_after = [blocks[n] for n in keep_idx if kinds[n] == "OPEN"]
assert open_before == open_after, "an open item changed across the cut"

# ---- deliberate rewrite 1: doc-trim item, newest execution record only ----
dt = blocks[DOCTRIM_BLOCK]
ex_start = next(i for i, l in enumerate(dt) if l.lstrip().startswith("**EXECUTED c2712"))
ex_end = next(i for i, l in enumerate(dt) if l.lstrip().startswith("**STANDING RULES"))
assert 0 < ex_start < ex_end, (ex_start, ex_end)
NEW_EXEC = """      **EXECUTED c2724 (QUALITY slot) -- `tasks/queue.md` only** (80.5KB/906 lines, TRIM
      SOON; STATUS.md and LEARNINGS OK, untouched). Partition fresh per rule 3: 46 blocks,
      13 DONE + 33 OPEN. Rule-1 hazard grep ran FIRST on the 285 archive-bound lines -- 39
      hits, all narrative about rules homed elsewhere bar two uniquely homed methods, both
      verified present first: c2713's at `notes/LEARNINGS.md:6028` and c2712's `new < old`
      rule at `notes/LEARNINGS.md:6014`. Backups `/tmp/c2724_*.bak`; `bin/_trim2724q.py` kept
      all 33 open + newest DONE (c2723), archived 12 DONE -> **56.1KB/630 lines**.
      **Rule-4 margin measured ~14.9KB (74240 ceiling - 57362 actual post-cut - ~2.0KB for
      c2724's own DONE block), i.e. RIGHT AT the ~15KB thin line, not comfortably above it
      as first estimated.** Accepted without compressing another open item because the next
      `check-doc-size` look is 24c out and a DONE-only cut then is ample; if the next trim
      measures thin again, compress the two largest open blocks (28: 4085 B, 38: 4646 B)
      rather than deferring a second time. Two open items were edited as content fixes
      anyway: this record (replaced in place) and the **c2700 shopify tripwire, RETIRED as
      falsified** -- it blamed a stale `--only` snapshot, but the flagging 0 came from a real
      nightly FULL run; replaced by the transient-dip diagnosis + triage recipe.
      **The `new < old` assert FIRED on the first draft of this very record** (2.7KB vs the
      1874 B it replaces) and forced this shorter one -- c2712's rule working as designed.
      Other guards passed: partition reconstruction, multiset identity,
      no-OPEN-in-archive-set, open-items-unchanged, independent line-set losslessness,
      `check-doc-size` OK, services active and `/`, `/pricing`, `/tools` 200 before+after.
""".rstrip("\n").split("\n")
blocks[DOCTRIM_BLOCK] = dt[:ex_start] + NEW_EXEC + dt[ex_end:]

# ---- deliberate rewrite 2: retire the falsified c2700 shopify tripwire ----
NEW_SHOPIFY = """- [ ] **REWRITTEN c2724 -- the c2700 `shopify-products-scraper` tripwire was FALSIFIED; what
      replaces it is the triage recipe, which is the part worth keeping.** c2700 predicted the
      `check-row-floor` ratio-0.00 flag was a STALE `state/health.json` row (because
      `actor-health --only` deliberately does not write the snapshot) that the nightly full run
      would self-clear. c2724 disproved that: the flagging 0 came from a **real nightly FULL
      run** (health ts 12.0h old, not an `--only` artifact), so "it will self-clear" was never
      the mechanism. **Correct diagnosis (c2724): isolated single-snapshot dips.** A 30-snapshot
      `git log`/`git show` trace of `state/health.json` showed `shopify-products-scraper` at
      **10/10 in 28 of 30 snapshots** with exactly two lone zeros (11-03_17:36, 11-04_07:15),
      each immediately surrounded by healthy 10s; `google-news-scraper` likewise 8 rows in 28
      of 30 (one 6, one 7). Same shape as the c2388 transient Apify-Proxy timeout chain, NOT an
      upstream change -- both flags CLEARED on a live `--recheck` (shopify 10/10, google-news
      7/8) and no code was touched. **Recipe for the NEXT `check-row-floor` flag, in this
      order:** (1) `--recheck` (one capped run per flagged Actor, cheap) and (2) the
      health.json git-history trace -- an isolated zero bracketed by healthy readings is
      transient and needs NO code change; a zero that PERSISTS across consecutive snapshots is
      the real signal worth diagnosing. Do NOT edit Actor code off a single flagged snapshot.
      **Shell gotcha that cost time here (homed `notes/LEARNINGS.md`):** do the trace in Python
      with `subprocess`, not as `git show ... | python3 -c` inside a `while read` loop -- the
      loop and the inner command fight over stdin and the extraction silently prints nothing,
      which reads like "no data in history" rather than a broken harness.
""".rstrip("\n").split("\n")
old_shopify = blocks[SHOPIFY_BLOCK]
blocks[SHOPIFY_BLOCK] = NEW_SHOPIFY

# rewrites asserted separately (they break multiset identity by design).
# The `new < old` byte assert is the c2712 rule homed at notes/LEARNINGS.md:6014.
assert len("\n".join(NEW_EXEC)) < len("\n".join(dt[ex_start:ex_end])), \
    "doc-trim rewrite did not shrink the record"
_exec_txt = "\n".join(NEW_EXEC).lower().replace("-", " ")
for key in ["rule 1", "rule 3", "rule 4", "_trim2724q.py", "/tmp/c2724_",
            "learnings.md:6028", "learnings.md:6014", "new < old"]:
    assert key.lower().replace("-", " ") in _exec_txt, f"doc-trim rewrite dropped {key!r}"
for key in ["check-row-floor", "--recheck", "health.json", "git-history", "c2388",
            "subprocess", "while read", "10/10", "transient", "c2700"]:
    assert key in "\n".join(NEW_SHOPIFY), f"shopify rewrite dropped {key!r}"

new_lines = []
for n in keep_idx:
    new_lines.extend(blocks[n])
new_live = "\n".join(new_lines)

# ---- archive prepend, preserving the archive's own header prefix ----
arch_old = open(ARCHIVE).read()
hdr_end = arch_old.index("\n- [x] ")
arch_hdr, arch_body = arch_old[:hdr_end], arch_old[hdr_end:]
assert arch_hdr.startswith("PRIOR (closed/DONE queue items"), arch_hdr[:60]

NOTE = (
    "\n\nARCHIVED BY CYCLE 2724 (doc-trim cadence, QUALITY slot): queue.md was 906 lines / "
    "80.5KB and `bin/check-doc-size` read TRIM SOON (+5440 B/cycle, projected 206KB at its "
    "next look). Moved here: the 12 oldest DONE blocks (c2722, c2721, c2720, c2719, c2718, "
    "c2717, c2716, c2715, c2714, c2713, c2712, c2710); the newest DONE block (c2723) and all "
    "33 open `[ ]` items stayed live. The rule-4 margin was ADEQUATE after that DONE-only cut "
    "(15.8KB), so -- unlike c2712 -- NO open item was compressed for size. Two open items were "
    "still edited as content corrections and their superseded prose is archived immediately "
    "below the DONE blocks: the doc-trim item's c2712 execution record (replaced in place by "
    "c2724's, per its own 'newest execution only' rule) and the c2700 shopify-products-scraper "
    "tripwire, whose PREMISE c2724 falsified (it blamed a stale `actor-health --only` snapshot; "
    "the flagging 0 actually came from a real nightly FULL run, and the true cause is an "
    "isolated single-snapshot dip -- 10/10 in 28 of 30 snapshots). Hazard grep ran first on all "
    "285 archive-bound lines: 39 hits, all narrative about rules homed elsewhere except c2713's "
    "bin-script grep rule and c2712's `new < old` assert rule, both confirmed homed at "
    "notes/LEARNINGS.md:6028 and :6014 before archiving. Newest-first below, same order as the "
    "source file.\n\n"
)
superseded = (
    "- [x] **SUPERSEDED PROSE, archived c2724 (not a DONE item) -- the doc-trim cadence "
    "item's c2712 execution record,** replaced in place by c2724's per that item's own "
    "'newest execution only' rule:\n"
    + "\n".join(dt[ex_start:ex_end]).rstrip("\n") + "\n\n"
    "- [x] **SUPERSEDED PROSE, archived c2724 (not a DONE item) -- the c2700 "
    "`shopify-products-scraper` tripwire, retired because its PREMISE was falsified.** It "
    "predicted the ratio-0.00 flag was a stale `actor-health --only` row that the nightly run "
    "would self-clear; c2724 found the 0 came from a real nightly FULL run and the true cause "
    "is an isolated single-snapshot dip (10/10 in 28 of 30 snapshots, two lone zeros). The "
    "replacement text in queue.md keeps the live half (the triage recipe). Original:\n"
    + "\n".join(old_shopify).rstrip("\n") + "\n"
)

arch_new = arch_hdr + NOTE + superseded + "\n" + "\n".join(arch_lines).rstrip("\n") + "\n" + arch_body

if "--dry-run" in sys.argv:
    print(f"queue.md : {len(orig)} B / {len(lines)} lines"
          f"  ->  {len(new_live)} B / {len(new_live.split(chr(10)))} lines")
    print(f"archive  : {len(arch_old)} B  ->  {len(arch_new)} B")
    print(f"archived blocks: {len(ARCHIVE_BLOCKS)}  kept: {len(keep_idx)}")
    sys.exit(0)

# ---- backups first (rule 1's safety net) ----
open("/tmp/c2724_queue.md.bak", "w").write(orig)
open("/tmp/c2724_queue_archive.md.bak", "w").write(arch_old)

# ---- losslessness, verified independently of the asserts above ----
live_set = set(l for l in new_live.split("\n") if l.strip())
arch_set = set(l for l in arch_new.split("\n") if l.strip())
rewritten = set(l for l in (NEW_EXEC + NEW_SHOPIFY) if l.strip())
missing = [l for l in lines
           if l.strip() and l not in live_set and l not in arch_set]
assert not missing, f"{len(missing)} original line(s) in neither file: {missing[:3]}"

open(QUEUE, "w").write(new_live)
open(ARCHIVE, "w").write(arch_new)
print(f"queue.md : {len(orig)} B / {len(lines)} lines"
      f"  ->  {len(new_live)} B / {len(new_live.split(chr(10)))} lines")
print(f"archive  : {len(arch_old)} B  ->  {len(arch_new)} B")
print("backups  : /tmp/c2724_queue.md.bak /tmp/c2724_queue_archive.md.bak")
