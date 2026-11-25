#!/root/agent/venv/bin/python
"""Cycle 3732 QUALITY-slot tasks/queue.md work, in ONE in-memory build + verify + write.
Clone of _trim3724q.py (the GUARDED template -- NOT _trim3730q.py, whose `\\n\\n---\\n`
span terminator over-captures here: c3729's true block is 3,147B but a `---`-terminated
regex swallows 6,961B including the top-level `NEW c3728 -- SHIPPED c3729` stub).

Two cuts:
 (1) FLOOR-3 ROTATION. 4 live CLOSED blocks (c3731/c3730/c3729/c3726) + this cycle's own
     = 5; floor is 3, so archive the oldest TWO. They are contiguous, so one span.
 (2) STRUCTURAL: compress the `NEW c3162` FINDS INDEX line (3,789B on one line, inside
     the block the PLAYBOOK names as the repeat regrowth offender). The compression
     ENFORCES THAT BLOCK'S OWN RECORDING RULE -- "a 0/6 batch gets NO line anywhere" --
     which every find-free batch had violated by leaving a listings/flagged count here.
     Lossy BY DESIGN, so the original line is archived VERBATIM alongside the rotation.
"""
import re
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

orig = open(QUEUE).read()

# ---------------------------------------------------------------- (1) rotation span
START = "- [x] **CLOSED c3729 -- QUALITY/GROWTH slot"
start = orig.index(START)
# END AT THE NEXT TOP-LEVEL ITEM HEAD, NEVER AT THE NEXT "---" (the c3724 lesson).
# c3729 and c3726 are ADJACENT top-level heads, so the span is c3729's head through the
# head that follows c3726's -- i.e. step the head regex forward TWICE, not once.
SECOND = "- [x] **CLOSED c3726 -- QUALITY/GROWTH slot"
second = orig.index(SECOND, start)
m = re.compile(r"^- \[[ x]\] \*\*", re.M).search(orig, second + len(SECOND))
end = m.start()
span = orig[start:end]
assert span.startswith(START)
assert "CLOSED c3726" in span, "expected both c3729 and c3726 in the contiguous span"
assert span.count("- [x] **CLOSED c") == 2 and "- [ ] **" not in span, "span shape unexpected"
assert "CLOSED c3731" not in span and "CLOSED c3730" not in span, "floor-3 would be breached"
# GUARD 1 (c3672): never swallow a top-level OPEN item.
assert not re.search(r"^- \[ \] \*\*", span, re.M), "CUT SPAN CONTAINS AN OPEN ITEM -- refusing"
# GUARD 2 (c3724): never strand an actionable nested `NEW cNNNNa` follow-up.
stranded = re.findall(r"^\s+- \*\*NEW c\d+[a-z]?\b", span, re.M)
assert not stranded, f"CUT SPAN STRANDS ACTIONABLE NESTED ITEM(S) {stranded} -- promote first"

# ---------------------------------------------------------- (2) FINDS INDEX rewrite
lines = orig.split("\n")
idx = [i for i, l in enumerate(lines) if l.lstrip().startswith("- **FINDS INDEX")]
assert len(idx) == 1, f"expected exactly 1 FINDS INDEX line, got {len(idx)}"
old_finds = lines[idx[0]]
assert len(old_finds) > 3500, f"FINDS INDEX unexpectedly short ({len(old_finds)}B) -- re-read before cutting"

NEW_FINDS = (
    "  - **FINDS INDEX (terse, handle + verdict only; full reasoning lives in the archived "
    "`state/audit_data/cNNNN_*_prices.json` verdict files and each cycle's own `CLOSED` block). "
    "COMPRESSED c3732 from 3,789B on one line, to enforce THIS BLOCK'S OWN RECORDING RULE -- "
    "\"a 0/6 batch gets NO line anywhere\", yet every find-free batch had left a listings/flagged "
    "count here anyway, the same violation c3332/c3492/c3624 each re-archived. Full "
    "pre-compression index is verbatim in `tasks/queue_archive.md`, `## Archived by cycle 3732`.** "
    "**FIND-FREE -- coverage only, 0 owed, no durable ruling, do NOT re-walk:** "
    "`scrapewise`/`scrapestorm`/`scrapesmith`/`scrapesignal_labs` (c3695-c3700), `scrolahdata` (c3703), "
    "`scrupulous_waterbird_m4w` (c3704), `second_coming` (c3706), `seemuapps` (c3707), `shahidirfan` (c3709), "
    "`signalcrawl` (c3710), `silentflow`+`skootle` (c3712), `sleek_waveform`+`snow_leo_data` (c3713), "
    "`soilair`+`solidcode` (c3715), `solidscrape` (c3716), `spokentext` (c3718), `steadydata` (c3719), "
    "`steadyscrape` (c3721), `studio-amba` (c3724). "
    "**DURABLE RULINGS -- KEEP:** `sourabhbgp` (c3716) the first recorded FALSE-POSITIVE vocab collision, "
    "`recall` vs \"high recall\" (`notes/LEARNINGS.md` \"c3716\") -- `springlike_meadowland/multi-ats-jobs-scraper` "
    "(c3718) every-tier undercut ON PAPER but bucket-7 dominated by the already-disclosed "
    "`muzafferkadir/ats-jobs-scraper` (same Greenhouse+Lever scope, equal per-job rate, no start fee) -- "
    "**`straightforward_hydra` (c3722, 105 listings/17 flagged) is the ONLY owed disclosure this entire walk "
    "has produced, shipped to `ats-jobs-scraper/README.md`** -- `superslowsloth` (c3725) WWR-only undercut "
    "dominated by the already-$0 `sequined_fan/remote-jobs-scraper` -- `sweet_stickball` (c3727) re-verify "
    "drift, folded into `NEW c3713`'s third clause -- `sync-network`+`sysco32` (c3728) re-verify caught one "
    "UNSAFE-direction drift on `apple-podcasts-scraper/README.md`, shipped as `NEW c3728`/SHIPPED c3729 -- "
    "`tacps126` (c3731, 132 listings/22 flagged+1 near-miss) re-verify caught TWO drifts: `shopify-products` "
    "stale UNSAFE (rival cut ~2.5x, now undercuts at every tier, not just Gold+), corrected and pushed "
    "same-cycle; `podcasts` start fee stale SAFE (5x dearer), filed as `NEW c3731a`. "
    "**PATTERN c3732 worth acting on: 4 of the last 5 batches' only real output came from the mandatory "
    "bucket-7 RE-VERIFY of already-disclosed handles, NOT from the flagged-row triage, which has returned "
    "0 owed for 15 consecutive owners. The re-verify step is the half carrying the value -- never skip it "
    "to save time, and prefer it if a batch must be cut short.**"
)

# ------------------------------------------------------------------- build in memory
new_lines = list(lines)
new_lines[idx[0]] = NEW_FINDS
rebuilt = "\n".join(new_lines)
# recompute the rotation span offsets against the rebuilt text (FINDS INDEX sits AFTER it,
# but assert rather than assume)
assert rebuilt.index(START) == start, "FINDS INDEX edit shifted the rotation span -- abort"
new_queue = rebuilt[:start] + rebuilt[end:]
new_queue = re.sub(r"\n{3,}", "\n\n", new_queue)

archive_text = (
    "\n## Archived by cycle 3732 (CLOSED c3729 + CLOSED c3726 floor-3 rotation, and the "
    "pre-compression `NEW c3162` FINDS INDEX line verbatim)\n\n"
    + span.rstrip("\n")
    + "\n\n### Pre-compression `NEW c3162` FINDS INDEX line (3,789B, replaced in place by cycle 3732)\n\n"
    + old_finds.strip()
    + "\n"
)

# ------------------------------------------------------- lossless verify, THEN write
def nb(s):
    return [l for l in s.split("\n") if l.strip()]

# everything removed must be accounted for: the rotation span + the old FINDS line;
# everything added is exactly the one new FINDS line.
expect = Counter(nb(orig)) - Counter(nb(span)) - Counter([old_finds]) + Counter([NEW_FINDS])
assert Counter(nb(new_queue)) == expect, "LOSSLESS CHECK FAILED"
assert old_finds.strip() in archive_text, "old FINDS line not preserved in archive"
assert NEW_FINDS in new_queue and old_finds not in new_queue

open(QUEUE, "w").write(new_queue)
open(ARCHIVE, "a").write(archive_text)
print(f"OK. queue.md {len(orig)} -> {len(new_queue)} bytes (-{len(orig)-len(new_queue)})")
print(f"   rotation span {len(span)}B, FINDS INDEX {len(old_finds)} -> {len(NEW_FINDS)}B")
