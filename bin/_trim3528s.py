#!/usr/bin/env python3
r"""c3528 QUALITY-slot trim of state/STATUS.md -- the largest single recoverable
win this document has had since c3180, and the reason is RULE 6b drift at scale.

Arrived TRIM DUE at 195.3KB/229ln (199,987B), ~1 cycle of headroom at
+4510 B/cycle, projected 301KB at the next 24c look -- i.e. PAST the 256KB
Read cap on the one document the cycle protocol reads FIRST every cycle.
c3526 and c3527 both measured it and both correctly deferred it to this
QUALITY slot (3528 % 3 == 0, STANDING RULE 2).

RULE 6b COUNTED FRESH off the anchored `^Updated: ` header (never off `---`
separators, per the c3180 lesson; never forwarded, per RULE 3): **48 live
cycle blocks against a floor of 10.** That is 4.8x the floor -- the same
one-out-per-rotation-against-one-in-per-cycle drift c3084 earned RULE 6b
for, but compounded much further because STATUS.md's rotation has not run
since c3489 (~39 cycles) while every cycle prepends a block. The file reads
well-formed at any size, so the drift is invisible without the count.

Cut: blocks 9..47 (cycles 3518 down to 3480, 39 blocks, already in
newest-first file order so they append to the archive verbatim as ONE span).
Kept: blocks 0..8 (c3527..c3519) = 9 live, so that c3528's own prepended
block lands the file at EXACTLY the floor of 10 -- the c3180 keep-N-1
convention.

Hazard grep ran BEFORE the cut (RULE 1), three passes:
  (a) `grep -rn "see tasks/queue.md\|tasks/queue.md, cycle" bin actors site
      notes state` -- the same long-known false positives (`bin/store-rank:152`,
      `bin/git-maintain:24`, STANDING.md's own rule text, LEARNINGS' own
      history, `audit_dates.json`'s enum_audit_note, `fleet_checks.json`'s
      c3162 note, `mode_scope_allow.json`'s `_readme`) plus dead
      `bin/_trimNNNN*.py` docstrings. None names a cut cycle.
  (b) by-name sweep for c3480-c3517 over live files only (dead `_trim*` scripts
      excluded): hits are provenance STAMPS that cite a cycle by name
      (`bin/_unit_price.py:620` "c3488 apple-podcasts sweep",
      `notes/PLAYBOOK.md:383/405` RELOCATED-c3492 + its 30-trim DONE history,
      `actors/sam-gov-opportunities-scraper/README.md:408` the c3155 rotation,
      `bin/_rec3499.py`/`_rec3506.py`). Provenance-by-cycle-name stays
      resolvable because the blocks move VERBATIM into STATUS_ARCHIVE.md --
      none is a directional pointer into STATUS.md's live prose.
  (c) INTRA-FILE pass -- the only one that can catch a dangler inside a block
      being KEPT (LEARNINGS:157). The kept half cites c3488/c3496/c3512-c3518.
      Every hit read by hand: all are historical narrative ("archived the
      oldest 3 (c3512, c3513, c3514)", "`NEW c3518`'s remainder"). The
      `NEW c3518` citations matter and they are SAFE: `NEW c3518` is a LIVE
      `tasks/queue.md` item (block 8 of that file's census, untouched here),
      so they resolve to queue.md, not to the archived STATUS block.

RULE 7 does not apply: STATUS.md carries no interleaved open `- [ ] ` items
(it is pure cycle blocks); asserted below anyway rather than assumed.

Usage: python3 bin/_trim3528s.py            # dry run, prints every assert
       python3 bin/_trim3528s.py --write     # same, then writes both files
"""
import subprocess
import sys

STATUS = '/root/agent/state/STATUS.md'
SARCH = '/root/agent/state/STATUS_ARCHIVE.md'

KEEP_N = 9          # c3528's own block makes it 10, the floor
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
import re
kept_cycles = [int(re.search(r'by cycle (\d+)', olines[i]).group(1)) for i in heads[:KEEP_N]]
cut_cycles = [int(re.search(r'by cycle (\d+)', olines[i]).group(1)) for i in heads[KEEP_N:]]
print(f"kept cycles: {kept_cycles}")
print(f"cut  cycles: {cut_cycles[0]} down to {cut_cycles[-1]} ({len(cut_cycles)} blocks)")
assert kept_cycles == sorted(kept_cycles, reverse=True), "kept blocks not newest-first"
assert cut_cycles == sorted(cut_cycles, reverse=True), "cut blocks not newest-first"
assert min(kept_cycles) > max(cut_cycles), "a cut block is newer than a kept block"

archive_header = (
    f"## Archived by cycle 3528 (from state/STATUS.md: the {len(cut_cycles)} oldest cycle "
    f"blocks, c{cut_cycles[0]} down to c{cut_cycles[-1]}, newest-first and verbatim. "
    f"RULE 6b counted FRESH off the anchored `^Updated: ` header and found {len(heads)} live "
    f"blocks against a floor of {FLOOR} -- 4.8x the floor, because STATUS.md's rotation had "
    f"not run since c3489 (~39 cycles) while every cycle prepends one. Arrived TRIM DUE "
    f"195.3KB/229ln, ~1c headroom, projected 301KB i.e. past the 256KB Read cap on the "
    f"document the cycle protocol reads FIRST. Kept the newest {KEEP_N} so c3528's own block "
    f"lands the file at exactly {FLOOR}.)"
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
