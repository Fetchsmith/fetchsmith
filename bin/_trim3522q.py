#!/usr/bin/env python3
"""c3522 QUALITY-slot trim of tasks/queue.md -- arrived TRIM DUE 191.3KB/1042ln
at ~2 cycles of headroom, +5,440B/cycle, flagged overdue by c3521's own handoff.

Rotation-only pass (same shape as c3507/c3510/c3513/c3519): fresh per-block byte
census (113 blocks) found the usual non-report candidates (`FOLD-IN REGISTER`
9,013B, the vendor-catalogue tracker 8,968B, `NEW c3372` 5,032B, `NEW c3162`
4,881B) unchanged in size since c3516/c3519 last looked at them -- none had
regrown enough since the last compression to justify a second lever this
cycle, so only ROTATION was spent, matching c3519's call to leave bulk cuts
for a cycle that finds genuine regrowth.

Report-block count re-derived FRESH (regex over every `CLOSED c3` header,
never forwarded): 10 total, 3 of them standing one-off closures (c3329, c3336,
c3496) excluded from the report partition, leaving 7 report-shaped blocks
(c3515, c3516, c3517, c3518, c3519, c3520, c3521). Archived the oldest 3
(c3515, c3516, c3517) and kept the newest 4 (c3518, c3519, c3520, c3521), so
this cycle's own block lands the file exactly at the RULE 6b newest-5 floor.

Usage: python3 bin/_trim3522q.py           # dry run, prints every assert + byte deltas
       python3 bin/_trim3522q.py --write    # same, then writes queue.md + queue_archive.md
"""
import re
import subprocess
import sys

QUEUE = '/root/agent/tasks/queue.md'
QARCH = '/root/agent/tasks/queue_archive.md'

HEAD_RE = re.compile(r"^- \[[ x]\] \*\*", re.M)

orig = open(QUEUE, encoding='utf-8').read()
olines = orig.split('\n')


def split_blocks(text):
    m = list(HEAD_RE.finditer(text))
    out = []
    for i, x in enumerate(m):
        s = x.start()
        e = m[i + 1].start() if i + 1 < len(m) else len(text)
        out.append((s, e, text[s:e]))
    return text[:m[0].start()], out


preamble, blocks = split_blocks(orig)
print(f"arrived: {len(orig.encode())}B / {orig.count(chr(10))}ln / {len(blocks)} blocks")


def find_one(prefix):
    hits = [i for i, (s, e, b) in enumerate(blocks) if b.startswith(prefix)]
    assert len(hits) == 1, f"expected exactly 1 block starting {prefix!r}, got {hits}"
    return hits[0]


ROTATE_HEADS = [
    "- [x] **CLOSED c3517 -- ran the due `check-handle-liveness`",
    "- [x] **CLOSED c3516 -- ran the due `check-competitor-claims`",
    "- [x] **CLOSED c3515 -- triaged the next 6 rows",
]
KEEP_HEADS = [
    "- [x] **CLOSED c3521", "- [x] **CLOSED c3520",
    "- [x] **CLOSED c3519", "- [x] **CLOSED c3518",
]
STANDING_CLOSURES = [
    "- [x] **CLOSED c3329", "- [x] **CLOSED c3336",
    "- [x] **CLOSED c3496 (was `NEW follow-up (c2824)`)",
]

rot_idx = sorted(find_one(h) for h in ROTATE_HEADS)
keep_idx = sorted(find_one(h) for h in KEEP_HEADS)
standing_idx = sorted(find_one(h) for h in STANDING_CLOSURES)

report_idx = [i for i, (s, e, b) in enumerate(blocks)
              if re.match(r"^- \[x\] \*\*CLOSED c\d+", b.split('\n', 1)[0])]
print(f"report blocks counted fresh: {len(report_idx)}")
assert set(report_idx) == set(rot_idx) | set(keep_idx) | set(standing_idx), \
    "report-block partition does not account for every CLOSED block"
assert len(rot_idx) == 3 and len(keep_idx) == 4
print(f"ROTATION: archiving {len(rot_idx)}, keeping newest {len(keep_idx)} "
      f"(+ c3522's own block = 5, exactly the RULE 6b floor)")

cut_set = set(rot_idx)
cut_bytes = sum(len(blocks[i][2].encode()) for i in cut_set)
print(f"cut bytes: {cut_bytes}")

# newest-first order for the archive header, matching c3519's convention
archived_order = sorted(cut_set, key=lambda i: blocks[i][2], reverse=False)
# order by the cycle number embedded in the heads, newest first: c3517, c3516, c3515
cycle_order_heads = [
    "- [x] **CLOSED c3517",
    "- [x] **CLOSED c3516",
    "- [x] **CLOSED c3515",
]
ordered_cut_idx = [find_one(h) for h in cycle_order_heads]
assert set(ordered_cut_idx) == cut_set

archive_block_text = "\n\n".join(blocks[i][2].rstrip('\n') for i in ordered_cut_idx)
archive_header = (
    "## Archived by cycle 3522 (from tasks/queue.md: the 3 oldest cycle-report "
    "blocks under the STANDING RULE 6b newest-5 floor -- c3517, c3516, c3515, "
    "newest-first; rotation-only pass, re-derived fresh, no RELOCATION or "
    "COMPRESSION lever spent this time -- the usual non-report census candidates "
    "had not regrown enough since c3516/c3519 to justify a second lever.)"
)

# ------------------------------------------------- build new queue.md
new_blocks_text = []
for i, (s, e, b) in enumerate(blocks):
    if i in cut_set:
        continue
    new_blocks_text.append(b)
new_queue = preamble + "".join(new_blocks_text)

# losslessness check: every non-cut block's text must appear verbatim, and
# cut blocks must now live verbatim in the archive text.
for i, (s, e, b) in enumerate(blocks):
    if i in cut_set:
        assert b.rstrip('\n') in archive_block_text, f"block {i} missing from archive text"
    else:
        assert b in new_queue, f"block {i} missing from new queue text"

new_lines = new_queue.count('\n')
print(f"new queue.md: {len(new_queue.encode())}B / {new_lines}ln "
      f"(delta {len(new_queue.encode()) - len(orig.encode())}B)")

qarch_orig = open(QARCH, encoding='utf-8').read()
new_qarch = qarch_orig.rstrip('\n') + "\n\n" + archive_header + "\n\n" + archive_block_text + "\n"

# ------------------------------------------------- 3-pass hazard grep (report only; manual review below)
for needle in ["c3515", "c3516", "c3517"]:
    hits = [i for i, l in enumerate(new_queue.split('\n')) if needle in l]
    print(f"hazard grep (new queue.md) for {needle!r}: {len(hits)} residual hits (expected: rule-origin citations only, not report-block prose)")

if '--write' not in sys.argv:
    print("DRY RUN ONLY -- pass --write to commit changes")
    sys.exit(0)

open(QUEUE, 'w', encoding='utf-8').write(new_queue)
open(QARCH, 'w', encoding='utf-8').write(new_qarch)
print("wrote queue.md and queue_archive.md")

# independent post-write re-verify against git HEAD
head_text = subprocess.run(['git', 'show', 'HEAD:tasks/queue.md'], cwd='/root/agent',
                            capture_output=True, text=True).stdout
head_lines = [l for l in head_text.split('\n') if l.strip()]
live_text = open(QUEUE, encoding='utf-8').read() + "\n" + open(QARCH, encoding='utf-8').read()
missing = [l for l in head_lines if l not in live_text]
print(f"post-write lossless check: {len(missing)} of {len(head_lines)} original non-blank lines missing")
if missing:
    for l in missing[:5]:
        print("MISSING:", l[:120])
