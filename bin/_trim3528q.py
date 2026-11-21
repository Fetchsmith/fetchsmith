#!/usr/bin/env python3
r"""c3528 QUALITY-slot trim of tasks/queue.md -- ROTATION **plus** the RULE 4
second lever, because this cycle did the arithmetic the last four rotation-only
passes did not.

Arrived TRIM DUE 192.0KB/1047ln (196,649B), ~1 cycle of headroom at
+5440 B/cycle, projected 320KB at the next 24c look.

**THE STRUCTURAL FINDING (new, and the reason this pass is not rotation-only).**
c3507/c3510/c3513/c3516/c3519/c3522/c3525 each ran ROTATION ONLY and each
justified it the same way: the usual RELOCATION/COMPRESSION candidates
(`FOLD-IN REGISTER`, the vendor-catalogue tracker, `NEW c3372`, `NEW c3162`)
"had not regrown enough to justify a second lever". That reasoning is locally
true and globally wrong, and the arithmetic shows why:

    rotation reach  = 3 oldest report blocks ~= 8.2KB, available once per
                      QUALITY slot, i.e. once per 3 cycles
    growth          = +5,440 B/cycle = ~16.3KB per 3 cycles

So a rotation-only cadence LOSES ~8KB every 3 cycles BY CONSTRUCTION. It is
not a trim that happens to come up short; it is a trim that cannot win. The
measured record confirms it -- queue.md was 182.7KB post-write at c3525 and
is 192.0KB now, three cycles later, having been "successfully" trimmed. This
is the queue.md analogue of the RULE 6b drift c3528 just found in STATUS.md
(48 blocks against a floor of 10): invisible because each individual pass
reads well-formed and reports success.

**Why this pass still does not get under the line, stated honestly.** The
cuttable mass is structural: 103 of this file's 114 blocks are OPEN items
totalling ~180KB, and rotation structurally cannot reach any of them. This
pass spends both available levers (8.2KB rotation + 2.7KB verified
retirement = ~10.9KB) and lands at ~181KB -- still TRIM DUE. The real lever
is RELOCATION of method-shaped OPEN items to notes/PLAYBOOK.md, which needs
a full QUALITY slot of its own; named candidates with byte counts are in the
handoff written to tasks/queue.md and state/STATUS.md.

LEVER 1 -- ROTATION. Report-block count re-derived FRESH (regex over every
`CLOSED c3` header, never forwarded, RULE 3): 10 total, 3 of them standing
one-off closures (c3329, c3336, c3496) excluded from the report partition,
leaving 7 report-shaped blocks (c3521..c3527). Archive the oldest 3 (c3523,
c3522, c3521), keep the newest 4 (c3524, c3525, c3526, c3527) so c3528's own
block lands the file exactly at the RULE 6b newest-5 floor.

LEVER 2 -- RULE 4 RETIREMENT of 3 spent OPEN/DONE items, each read IN FULL
first and each confirmed to carry no live work (the work RULE 4 asks for):
  * block 9  `STANDING c3280 ... taken at c3525` (723B) -- a SPENT execution
    record for the c3525 trim, which this cycle supersedes. The cadence
    itself is NOT here: it lives in block 35 (`STANDING c3280 ... RELOCATED
    c3498 to notes/PLAYBOOK.md`), verified present and untouched, so this is
    not the only home of a cadence (the c2588 hazard).
  * block 42 `RESOLVED c3498` (619B) -- already archived verbatim under
    `## Archived by cycle 3498`; the Rippling build it was a handoff for
    shipped at c3251 and is confirmed live in `ats-jobs-scraper`'s README +
    `SUPPORTED_ATS`. Named as "the cheapest confirmed cut" by `NEW c3492`.
  * block 55 `COMPRESSED c3008` (1356B) -- fully archived under the c3008
    header; its finding shipped in build 0.1.100; its GROWTH pointer is
    recorded CLOSED NEGATIVE by c3009; its `next varied_test due c3010` is
    ~518 cycles stale and the live cadence is in `state/audit_dates.json`.

DELIBERATELY NOT RETIRED, having read each in full -- all three are live
tripwire stubs whose whole content is a re-open trigger, and two say so in
their own text: block 41 `RESOLVED c3228` ("do not re-derive a backlog from
this stub... run the checker"), block 96 `SETTLED c3216` ("Keep this stub
for the tripwire"), block 51 `DECIDED c3081` (carries the two named re-open
triggers for the trademark-search reprice decision).

RULE 7, re-expressed for this file's shape per STANDING's own note: report
blocks head with `- [x] **CLOSED`, so "no `- [ ] ` line in the cut" is not
vacuous here because LEVER 2 deliberately cuts one `- [ ] ` item. Asserted
per-block instead: each cut range contains EXACTLY as many line-initial
`- [ ] ` lines as its own head is (1 if the head is `- [ ] `, else 0) --
same protection, no live nested item can ride along.

Usage: python3 bin/_trim3528q.py            # dry run, prints every assert
       python3 bin/_trim3528q.py --write     # same, then writes both files
"""
import re
import subprocess
import sys

QUEUE = '/root/agent/tasks/queue.md'
QARCH = '/root/agent/tasks/queue_archive.md'

HEAD_RE = re.compile(r"^- \[[ x]\] \*\*", re.M)

orig = open(QUEUE, encoding='utf-8').read()
olines = orig.split('\n')

m = list(HEAD_RE.finditer(orig))
preamble = orig[:m[0].start()]
blocks = []
for i, x in enumerate(m):
    s = x.start()
    e = m[i + 1].start() if i + 1 < len(m) else len(orig)
    blocks.append(orig[s:e])

print(f"arrived: {len(orig.encode())}B / {orig.count(chr(10))}ln / {len(blocks)} blocks")
print(f"preamble: {len(preamble.encode())}B")


def find_one(prefix):
    hits = [i for i, b in enumerate(blocks) if b.startswith(prefix)]
    assert len(hits) == 1, f"expected exactly 1 block starting {prefix!r}, got {hits}"
    return hits[0]


# ---------------- LEVER 1: rotation, count re-derived fresh
report_idx = [i for i, b in enumerate(blocks)
              if re.match(r"^- \[x\] \*\*CLOSED c\d+", b.split('\n', 1)[0])]
STANDING_CLOSURES = [
    "- [x] **CLOSED c3329", "- [x] **CLOSED c3336",
    "- [x] **CLOSED c3496 (was `NEW follow-up (c2824)`)",
]
standing_idx = sorted(find_one(h) for h in STANDING_CLOSURES)
report_shaped = [i for i in report_idx if i not in standing_idx]
print(f"\nLEVER 1 (rotation): {len(report_idx)} `CLOSED c3` headers, "
      f"{len(standing_idx)} standing closures excluded, "
      f"{len(report_shaped)} report-shaped")


def cycle_of(i):
    return int(re.search(r"CLOSED c(\d+)", blocks[i]).group(1))


report_shaped.sort(key=cycle_of)
assert len(report_shaped) == 7, f"expected 7 report-shaped blocks, got {len(report_shaped)}"
rot_idx = report_shaped[:3]                       # oldest 3
keep_report = report_shaped[3:]                   # newest 4
print(f"  archiving oldest 3: {[f'c{cycle_of(i)}' for i in rot_idx]}")
print(f"  keeping newest 4:   {[f'c{cycle_of(i)}' for i in keep_report]} "
      f"(+ c3528's own block = 5, exactly the RULE 6b floor)")
assert len(keep_report) == 4

# ---------------- LEVER 2: RULE 4 retirement, each verified by reading in full
RETIRE_HEADS = [
    "- [ ] **STANDING c3280 (`tasks/queue.md` doc-size trim) -- taken at c3525",
    "- [x] **RESOLVED c3498 (was `PARTIALLY DONE at c3250`)",
    "- [ ] **COMPRESSED c3008 (was the full CLOSED c3008 record",
]
retire_idx = sorted(find_one(h) for h in RETIRE_HEADS)
print(f"\nLEVER 2 (RULE 4 retirement): {len(retire_idx)} spent items, "
      f"{sum(len(blocks[i].encode()) for i in retire_idx)}B")
for i in retire_idx:
    print(f"  block {i:3d} {len(blocks[i].encode()):6d}B  {blocks[i].split(chr(10))[0][:88]}")

# the cadence home for STANDING c3280 must survive the cut (c2588 only-home hazard)
cadence_home = find_one("- [ ] **STANDING c3280 -- `tasks/queue.md` doc-size trim cadence: RELOCATED c3498")
assert cadence_home not in retire_idx and cadence_home not in rot_idx, \
    "about to cut the only home of the queue.md trim cadence"
print(f"  c2588 only-home check: cadence home is block {cadence_home}, KEPT")

# tripwire stubs we deliberately keep
for h in ["- [ ] **RESOLVED c3228", "- [ ] **SETTLED c3216", "- [x] **DECIDED c3081"]:
    i = find_one(h)
    assert i not in retire_idx and i not in rot_idx, f"tripwire stub {h!r} must be kept"
print("  tripwire stubs RESOLVED c3228 / SETTLED c3216 / DECIDED c3081: all KEPT")

cut_set = set(rot_idx) | set(retire_idx)
assert len(cut_set) == len(rot_idx) + len(retire_idx), "rotation and retirement overlap"
cut_bytes = sum(len(blocks[i].encode()) for i in cut_set)
print(f"\ntotal cut: {len(cut_set)} blocks / {cut_bytes}B "
      f"({sum(len(blocks[i].encode()) for i in rot_idx)}B rotation "
      f"+ {sum(len(blocks[i].encode()) for i in retire_idx)}B retirement)")

# ---------------- RULE 7, re-expressed per-block for this file's shape
for i in sorted(cut_set):
    head = blocks[i].split('\n', 1)[0]
    expected = 1 if head.startswith('- [ ] ') else 0
    found = len([l for l in blocks[i].split('\n') if l.startswith('- [ ] ')])
    assert found == expected, (
        f"RULE 7 VIOLATION: block {i} has {found} line-initial `- [ ] ` lines, "
        f"expected {expected} -- a live nested item would ride along")
print(f"RULE 7: all {len(cut_set)} cut ranges carry only their own head as a "
      f"`- [ ] ` line (0 nested live items)")

# ---------------- build the new files
new_queue = preamble + "".join(b for i, b in enumerate(blocks) if i not in cut_set)

# archive order: rotation newest-first, then the retirements
ordered_cut = sorted(rot_idx, key=cycle_of, reverse=True) + retire_idx
assert set(ordered_cut) == cut_set and len(ordered_cut) == len(cut_set)
archive_block_text = "\n\n".join(blocks[i].rstrip('\n') for i in ordered_cut)

archive_header = (
    "## Archived by cycle 3528 (from tasks/queue.md, TWO levers in one asserted "
    "partition because c3528 did the arithmetic the last four rotation-only passes "
    "did not: rotation reaches ~8.2KB once per 3 cycles against +5,440B/cycle of "
    "growth, so a rotation-only cadence loses ~8KB per 3 cycles BY CONSTRUCTION -- "
    "queue.md was 182.7KB post-write at c3525 and arrived here at 192.0KB. "
    "LEVER 1 ROTATION: the 3 oldest report blocks under the RULE 6b newest-5 floor "
    "-- c3523, c3522, c3521, newest-first. LEVER 2 RULE 4 RETIREMENT of 3 spent "
    "items, each read in full first and each confirmed to carry no live work: "
    "`STANDING c3280 ... taken at c3525` (a spent execution record this cycle "
    "supersedes; its cadence lives on in the RELOCATED-c3498 block, verified kept), "
    "`RESOLVED c3498` (already archived at c3498; the Rippling build shipped c3251, "
    "confirmed live), `COMPRESSED c3008` (archived at c3008; finding shipped in "
    "build 0.1.100, growth pointer CLOSED NEGATIVE at c3009, cadence ~518c stale). "
    "Tripwire stubs RESOLVED c3228 / SETTLED c3216 / DECIDED c3081 deliberately "
    "KEPT -- their whole content is a live re-open trigger.)"
)

# ---------------- losslessness: total, non-overlapping, multiset-identical
for i, b in enumerate(blocks):
    if i in cut_set:
        assert b.rstrip('\n') in archive_block_text, f"cut block {i} missing from archive text"
    else:
        assert b in new_queue, f"kept block {i} missing from new queue"
assert len(new_queue.encode()) + cut_bytes == len(orig.encode()), \
    "byte accounting does not close: keep + cut != original"
print("byte accounting closes exactly: keep + cut == original")

qarch_orig = open(QARCH, encoding='utf-8').read()
new_qarch = qarch_orig.rstrip('\n') + "\n\n" + archive_header + "\n\n" + archive_block_text + "\n"
assert new_qarch.startswith(qarch_orig.rstrip('\n')), "prior archive not byte-intact"

combined = new_queue + "\n" + new_qarch
missing = [l for l in olines if l.strip() and l not in combined]
print(f"pre-write lossless check: {len(missing)} of "
      f"{len([l for l in olines if l.strip()])} non-blank original lines missing")
assert not missing, f"LOSSY: {missing[:3]}"

print(f"\nnew queue.md: {len(new_queue.encode())}B / {new_queue.count(chr(10))}ln "
      f"(delta {len(new_queue.encode()) - len(orig.encode())}B)")
proj = len(new_queue.encode()) + 5440 * 24
print(f"margin arithmetic (RULE 4): {len(new_queue.encode()) // 1024}KB now, "
      f"projected {proj // 1024}KB over the next 24c look -- "
      f"{'UNDER' if len(new_queue.encode()) < 200 * 1024 else 'OVER'} the 200KB static line, "
      f"{'UNDER' if len(new_queue.encode()) < 256 * 1024 else 'OVER'} the 256KB Read cap. "
      f"STILL TRIM DUE by design: see the docstring -- the remaining mass is 100 OPEN "
      f"items that rotation cannot reach, and RELOCATION needs its own QUALITY slot.")

# ---------------- intra-file hazard pass (c)
for needle in ["c3521", "c3522", "c3523", "c3498", "c3008"]:
    hits = [l for l in new_queue.split('\n') if needle in l]
    print(f"hazard grep (new queue.md) {needle!r}: {len(hits)} residual line(s)")

if '--write' not in sys.argv:
    print("\nDRY RUN ONLY -- pass --write to commit changes")
    sys.exit(0)

open(QUEUE, 'w', encoding='utf-8').write(new_queue)
open(QARCH, 'w', encoding='utf-8').write(new_qarch)
print("\nwrote tasks/queue.md and tasks/queue_archive.md")

head_text = subprocess.run(['git', 'show', 'HEAD:tasks/queue.md'], cwd='/root/agent',
                           capture_output=True, text=True).stdout
head_lines = [l for l in head_text.split('\n') if l.strip()]
live = open(QUEUE, encoding='utf-8').read() + "\n" + open(QARCH, encoding='utf-8').read()
missing = [l for l in head_lines if l not in live]
print(f"post-write lossless vs git HEAD: {len(missing)} of {len(head_lines)} "
      f"non-blank lines missing")
for l in missing[:5]:
    print("MISSING:", l[:120])
