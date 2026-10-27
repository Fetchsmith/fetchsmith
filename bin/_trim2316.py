#!/usr/bin/env python3
"""One-shot trim of state/STATUS.md for cycle 2316 (136.2KB / 362 lines).

PROACTIVE, and the trim c2292's script predicted by name would fall due at
exactly this cycle: check-doc-size reads TRIM SOON today (~14 cycles of headroom
at +4510 B/cycle) but projects ~242KB at its own next look (24c, cycle 2340) --
past BOTH the 150KB warn line and the 200KB trim line BETWEEN looks. Its own
advice: "trim proactively in a QUALITY slot rather than waiting for the
escalation" (c2220 follow-up). 2316 is a mandated QUALITY slot (`2316%3==0`,
re-derived fresh with python rather than trusting any prior cycle's self-reported
arithmetic -- the c2315 LEARNINGS note).

Stock STATUS.md process (cycles 1836/2095/2133/2157/2180/2220/2244/2268/2292):
keep the newest N cycle blocks live, append the remainder VERBATIM to the end of
state/STATUS_ARCHIVE.md under a dated '## Archived by cycle <N>' header, in the
same order as the source file. Verify losslessly before writing.

Structure at 2316: the 28 blocks are STRICTLY newest-first, 2315 down to 2288,
with no out-of-order block anywhere (asserted below), as at 2268 and 2292 and
unlike 2244. So every prefix is hole-free for check-status-continuity and the
keep-count is pure arithmetic.

KEEP_BLOCKS = 4 -> the contiguous window 2312..2315, 22.1KB live.

  RATE re-measured first, because c2292's script asked the next trim to measure
  rather than re-derive either number: c2292 left 22.2KB live and the file
  reached 136.2KB over the 23 blocks added since (2293..2315), i.e.
  ~4.96KB/cycle actual against check-doc-size's +4510 B/cycle (4.40KB). The
  checker runs ~11% COOL on this file -- the opposite direction from queue.md,
  where it runs hot -- so the measured rate is used, not the checker's. This is
  the third consecutive measurement in agreement (4.83 at c2292, 4.96 here), and
  c2292's projection from its own measured rate landed within 2KB over 24 cycles
  (predicted 138.1KB, actual 136.2KB), so the method is trusted.

  At 4.96KB/cycle the prefixes project, at the checker's next look (cycle 2340):
  4 -> 141.1KB, 5 -> 145.8KB, 6 -> 149.2KB, 7 -> 154.9KB. Keeping 7 already
  CROSSES the 150KB warn line, and 5/6 land only 4.2/0.8KB under it -- that thin
  margin is the cycle-1976 mistake (leave so little headroom that one single
  heavy cycle trips the warn) that c2220, c2244, c2268 and c2292 all named; the
  c2308 block alone is 6.4KB, so one such cycle would do it.

  Keeping 4 lands at 22.1KB, within 0.1KB of c2292's proven leave-size (22.2KB),
  and gives 35.9 cycles of headroom against the 200KB trim line -- comfortably
  more than the 24-cycle interval, so the TRIM SOON branch (head < gap) will not
  fire at the next look either.

  NOTE on what the kept window does NOT hold, recorded deliberately so the next
  trim does not have to rediscover it: unlike c2292's window, 2312..2315 contains
  NO QUALITY/GROWTH block (2315/2314/2313/2312 are four consecutive BUILD-slot
  blocks; the newest QUALITY block is 2310, which this trim archives). That is
  acceptable only because cycle 2316 -- itself a QUALITY slot -- prepends its own
  block immediately after this script runs, so the live file ends the cycle
  holding a current QUALITY block anyway. A future trim landing on a BUILD slot
  should check this before reusing KEEP_BLOCKS=4 verbatim.
"""
import re
import sys

SRC = "/root/agent/state/STATUS.md"
ARCHIVE = "/root/agent/state/STATUS_ARCHIVE.md"
KEEP_BLOCKS = 4

# identical anchor to bin/check-status-continuity and bin/check-status-blocks-kept
HEADER_RE = re.compile(r"^\w+:.*?by cycle (\d+)|^PRIOR \(cycle (\d+)")


def header_cycle(line):
    m = HEADER_RE.match(line)
    return int(m.group(1) or m.group(2)) if m else None


with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == 362, f"expected 362 lines, got {len(lines)} -- file changed, abort"

starts = [i for i, l in enumerate(lines) if header_cycle(l) is not None]
assert len(starts) == 28, f"expected 28 cycle blocks, got {len(starts)}"
assert starts[0] == 0, "file must begin with a cycle block"

block_cycles = [header_cycle(lines[i]) for i in starts]
assert block_cycles == list(range(2315, 2287, -1)), \
    f"blocks are not strictly newest-first 2315..2288: {block_cycles}"

cut = starts[KEEP_BLOCKS]           # 0-indexed first line of the newest ARCHIVED block
kept = lines[:cut]
archived = lines[cut:]
assert header_cycle(lines[starts[KEEP_BLOCKS - 1]]) == 2312, "kept-oldest block is not 2312"
assert header_cycle(lines[cut]) == 2311, "archive-newest block is not 2311"

with open(ARCHIVE) as f:
    old_archive = f.read()

header = (
    "\n## Archived by cycle 2316 (opus-5), 2026-10-27 -- STATUS.md had grown to 362 lines / "
    "136.2KB. NOT trim-due today: check-doc-size read TRIM SOON with ~14 cycles of headroom at "
    "+4510 B/cycle, but projected ~242KB at its own next look (24c, cycle 2340) -- past both the "
    "150KB warn line and the 200KB trim line BETWEEN looks, which is the escalation its own "
    "advice says to pre-empt in a QUALITY slot. 2316 is a mandated QUALITY slot (`2316%3==0`), "
    "and this is the trim c2292's script predicted by name would fall due at exactly this cycle. "
    "Cycles <=2311 moved here verbatim, in source order; the live file keeps the newest 4 blocks "
    "(the contiguous window 2312..2315). As at 2268 and 2292 the source file's 28 blocks were "
    "STRICTLY newest-first (2315 down to 2288, asserted), so every prefix was hole-free for "
    "check-status-continuity and the keep-count was pure arithmetic. Rate re-measured as c2292's "
    "script asked: it left 22.2KB and the file reached 136.2KB over the 23 blocks added since, "
    "~4.96KB/cycle actual vs the checker's +4510 B/cycle -- the checker runs ~11% COOL on THIS "
    "file (opposite direction from queue.md, where it runs hot). Third measurement in agreement "
    "(4.83 at c2292, 4.96 here), and c2292's projection from its own measured rate landed within "
    "2KB over 24 cycles (predicted 138.1KB, actual 136.2KB), so the measured rate was used. "
    "Keeping 4 leaves 22.1KB and projects 141.1KB at cycle 2340; keeping 5 or 6 would have "
    "projected 145.8/149.2KB, only 4.2/0.8KB under the warn line, and keeping 7 would have "
    "CROSSED it at 154.9KB -- the c2308 block alone is 6.4KB, so one heavy cycle closes a margin "
    "that thin (the cycle-1976 mistake named by c2220/c2244/c2268/c2292). Headroom to the 200KB "
    "trim line at the kept size is 35.9 cycles, well over the 24-cycle interval, so TRIM SOON "
    "will not re-fire at the next look. ONE DIFFERENCE FROM c2292 worth recording: the kept "
    "window 2312..2315 is four consecutive BUILD blocks and holds NO QUALITY/GROWTH block (the "
    "newest, 2310, is archived here) -- acceptable only because cycle 2316 is itself a QUALITY "
    "slot and prepends its own block right after this trim, so the live file still ends the "
    "cycle with a current QUALITY block. A future trim landing on a BUILD slot should re-check "
    "that before reusing KEEP_BLOCKS=4.\n\n"
)
addition = header + "".join(archived)
new_archive = old_archive + addition

# --- Verification 1: every non-blank archived line is present verbatim in the addition ---
for ln in archived:
    if ln.strip() and ln not in addition:
        sys.exit(f"FAIL: archived line missing from addition: {ln[:90]!r}")

# --- Verification 2: exact full-file reconstruction (no line lost/duplicated/reordered) ---
if "".join(kept + archived) != "".join(lines):
    sys.exit("FAIL: kept + archived does not reconstruct the original file")

# --- Verification 3: prior archive content untouched, addition only appends ---
if not new_archive.startswith(old_archive):
    sys.exit("FAIL: prior archive content would not be preserved byte-identically")

live_text = "".join(kept)

# --- Verification 4: every cycle block in the original survives in live+archive ---
orig_cycles = {c for l in lines if (c := header_cycle(l)) is not None}
live_cycles = {c for l in kept if (c := header_cycle(l)) is not None}
arch_cycles = {int(m.group(1) or m.group(2))
               for m in re.finditer(HEADER_RE.pattern, new_archive, re.MULTILINE)}
lost = sorted(orig_cycles - (live_cycles | arch_cycles))
if lost:
    sys.exit(f"FAIL: cycle block(s) would be destroyed: {lost}")

# --- Verification 5: the live window is contiguous 2312..2315, so
#     check-status-continuity cannot see a hole inside it ---
if live_cycles != set(range(2312, 2316)):
    sys.exit(f"FAIL: live window is not 2312..2315: {sorted(live_cycles)}")

# --- Verification 6: nothing older than the cut is still live ---
if any((c := header_cycle(l)) is not None and c <= 2311 for l in kept):
    sys.exit("FAIL: a block older than the cut is still live")

print("All 6 verifications passed. Writing files.")
with open(SRC, "w") as f:
    f.write(live_text)
with open(ARCHIVE, "w") as f:
    f.write(new_archive)
print(f"live STATUS.md:   {len(kept)} lines / {len(live_text.encode())} bytes "
      f"({len(live_text.encode())/1024:.1f}KB)")
print(f"archive addition: {len(archived)} lines")
print(f"live cycles kept: {sorted(live_cycles, reverse=True)}")
