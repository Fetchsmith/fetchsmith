#!/usr/bin/env python3
r"""c3564 QUALITY-slot trim of state/STATUS.md -- the second lever this cycle
(the urgent `tasks/queue.md` rotation ran first, 187.0KB -> 175.5KB).

Arrived TRIM DUE at 176.2KB/381ln, ~5 cycles of headroom at +4510 B/cycle,
projected 282KB at the next 24c look -- i.e. PAST the 256KB Read cap on the
one document the cycle protocol reads FIRST every cycle.  c3563, c3562,
c3560 and c3557 each measured it and each correctly deferred it to a QUALITY
slot (3564 % 3 == 0, STANDING RULE 2).  Taking it now rather than at the
~1c wire, because the projection -- not the current reading -- is what the
24c look interval actually has to survive.

RULE 6b COUNTED FRESH off the anchored `^Updated: ` header (never off `---`
separators, per the c3180 lesson; never forwarded, per RULE 3).  Keep the
newest 9 so c3564's own prepended block lands the file at EXACTLY the floor
of 10 -- the c3180 keep-N-1 convention.

Hazard grep ran BEFORE the cut (RULE 1), three passes:
  (a) directional-pointer sweep: `grep -rn "STATUS.md cycle 35\|STATUS.md,
      cycle 35\|state/STATUS.md c35"` over bin/actors/site/notes/state/tasks
      (dead `_trim*` scripts excluded) -- ZERO hits.  Nothing anywhere points
      at a STATUS.md cycle block by location.
  (b) by-name sweep for the cut range c3519-c3554 over live files: hits are
      `tasks/queue.md` (26), `notes/LEARNINGS.md` (27), `notes/PLAYBOOK.md`
      (9) and three dead one-off scripts (`_reloc3531.py`, `_fec3548_walk.py`,
      `_rec3532.py`), all provenance STAMPS that cite a cycle BY NAME, which
      stays resolvable because the blocks move VERBATIM into
      STATUS_ARCHIVE.md.  (`actors/*/node_modules/form-data/CHANGELOG.md`
      hits are coincidental version strings, not cycle references.)
  (c) INTRA-FILE pass -- the only one that can catch a dangler inside a block
      being KEPT (LEARNINGS:157).  The kept half (lines 1-81) cites cut
      cycles at lines 27/54/56/62/64/72/78.  Every hit read by hand: all are
      historical narrative ("archived the oldest 3 (`c3555`, `c3554`,
      `c3553`)", "the c3547 rule that a guard's numbers have an expiry
      date").  The ones that carry live WORK forward -- c3552's pre-censused
      per-SPAN relocation candidates at lines 56 and 64 -- inline the
      candidate names themselves (`NEW c3372`, `NEW c3162`, `NEW c3046`,
      `COMPRESSED c3000`), so nothing a future cycle needs lives only in a
      cut block.

RULE 7 does not apply: STATUS.md carries no interleaved open `- [ ] ` items
(it is pure cycle blocks); asserted below anyway rather than assumed.

Usage: python3 bin/_trim3564s.py            # dry run, prints every assert
       python3 bin/_trim3564s.py --write     # same, then writes both files
"""
import re
import subprocess
import sys

STATUS = '/root/agent/state/STATUS.md'
SARCH = '/root/agent/state/STATUS_ARCHIVE.md'

KEEP_N = 9          # c3564's own block makes it 10, the floor
FLOOR = 10

orig = open(STATUS, encoding='utf-8').read()
olines = orig.split('\n')

heads = [i for i, l in enumerate(olines) if l.startswith('Updated: ')]
print(f"arrived: {len(orig.encode())}B / {len(olines)}ln / {len(heads)} live cycle blocks")
assert heads[0] == 0, f"file must start with a cycle block, got head at line {heads[0]}"
assert len(heads) > FLOOR, f"nothing to rotate: {len(heads)} blocks vs floor {FLOOR}"
print(f"RULE 6b: {len(heads)} live vs floor {FLOOR} -- "
      f"{len(heads) - KEEP_N} blocks to archive, keeping newest {KEEP_N}")

cut_start = heads[KEEP_N]
keep_text = '\n'.join(olines[:cut_start])
cut_text = '\n'.join(olines[cut_start:])

# ---- partition is total and non-overlapping, byte-exactly
assert keep_text + '\n' + cut_text == orig, "partition is not byte-exact"
print(f"keep: {len(keep_text.encode())}B / {keep_text.count(chr(10)) + 1}ln")
print(f"cut : {len(cut_text.encode())}B / {cut_text.count(chr(10)) + 1}ln")

# ---- RULE 7 (re-expressed for this file): no interleaved open items anywhere
open_items = [i for i, l in enumerate(olines) if l.startswith('- [ ] ')]
assert not open_items, f"unexpected open `- [ ] ` items in STATUS.md at {open_items}"
print("RULE 7: 0 interleaved open `- [ ] ` items in the whole file (STATUS.md is pure cycle blocks)")

# ---- the kept half must be exactly the newest 9 blocks, by cycle number
kept_cycles = [int(re.search(r'by cycle (\d+)', olines[i]).group(1)) for i in heads[:KEEP_N]]
cut_cycles = [int(re.search(r'by cycle (\d+)', olines[i]).group(1)) for i in heads[KEEP_N:]]
print(f"kept cycles: {kept_cycles}")
print(f"cut  cycles: {cut_cycles[0]} down to {cut_cycles[-1]} ({len(cut_cycles)} blocks)")
assert kept_cycles == sorted(kept_cycles, reverse=True), "kept blocks not newest-first"
assert cut_cycles == sorted(cut_cycles, reverse=True), "cut blocks not newest-first"
assert min(kept_cycles) > max(cut_cycles), "a cut block is newer than a kept block"
assert kept_cycles[0] == 3563, f"newest block should be c3563, got c{kept_cycles[0]}"
assert len(kept_cycles) == KEEP_N

archive_header = (
    f"## Archived by cycle 3564 (from state/STATUS.md: the {len(cut_cycles)} oldest cycle "
    f"blocks, c{cut_cycles[0]} down to c{cut_cycles[-1]}, newest-first and verbatim. "
    f"RULE 6b counted FRESH off the anchored `^Updated: ` header and found {len(heads)} live "
    f"blocks against a floor of {FLOOR}. Arrived TRIM DUE 176.2KB/381ln, ~5c headroom, "
    f"projected 282KB at the next 24c look -- past the 256KB Read cap on the document the "
    f"cycle protocol reads FIRST, which is why it was taken at ~5c rather than at the wire. "
    f"Second lever of the c3564 QUALITY slot; the `tasks/queue.md` rotation ran first. "
    f"Kept the newest {KEEP_N} so c3564's own block lands the file at exactly {FLOOR}.)"
)

new_status = keep_text + '\n'
sarch_orig = open(SARCH, encoding='utf-8').read()
new_sarch = sarch_orig.rstrip('\n') + "\n\n" + archive_header + "\n\n" + cut_text.rstrip('\n') + "\n"

# ---- losslessness: every non-blank original line findable in live+archive
combined = new_status + '\n' + new_sarch
missing = [l for l in olines if l.strip() and l not in combined]
print(f"pre-write lossless check: {len(missing)} of "
      f"{len([l for l in olines if l.strip()])} non-blank original lines missing")
assert not missing, f"LOSSY: {missing[:3]}"

# ---- prior archive must be byte-intact (append-only)
assert new_sarch.startswith(sarch_orig.rstrip('\n')), "prior archive not byte-intact"

print(f"\nnew STATUS.md: {len(new_status.encode())}B / {new_status.count(chr(10))}ln "
      f"(delta {len(new_status.encode()) - len(orig.encode())}B)")
print(f"new STATUS_ARCHIVE.md: {len(new_sarch.encode())}B "
      f"(+{len(new_sarch.encode()) - len(sarch_orig.encode())}B)")
proj = len(new_status.encode()) + 4510 * 24
print(f"margin arithmetic (RULE 4): {len(new_status.encode()) // 1024}KB now, "
      f"projected {proj // 1024}KB at +4510B/cycle over the next 24c look "
      f"-- {'UNDER' if proj < 200 * 1024 else 'OVER'} the 200KB trim line, "
      f"{'UNDER' if proj < 256 * 1024 else 'OVER'} the 256KB Read cap")

if '--write' not in sys.argv:
    print("\nDRY RUN ONLY -- pass --write to commit changes")
    sys.exit(0)

open(STATUS, 'w', encoding='utf-8').write(new_status)
open(SARCH, 'w', encoding='utf-8').write(new_sarch)
print("\nwrote state/STATUS.md and state/STATUS_ARCHIVE.md")

# ---- independent post-write re-verify against git HEAD, not against memory
head_text = subprocess.run(['git', 'show', 'HEAD:state/STATUS.md'], cwd='/root/agent',
                           capture_output=True, text=True).stdout
head_lines = [l for l in head_text.split('\n') if l.strip()]
live = open(STATUS, encoding='utf-8').read() + "\n" + open(SARCH, encoding='utf-8').read()
missing = [l for l in head_lines if l not in live]
print(f"post-write lossless vs git HEAD: {len(missing)} of {len(head_lines)} "
      f"non-blank lines missing")
for l in missing[:5]:
    print("MISSING:", l[:120])
assert not missing, "POST-WRITE LOSSLESS FAIL"
