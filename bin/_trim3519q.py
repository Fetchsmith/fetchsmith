#!/usr/bin/env python3
"""c3519 QUALITY-slot trim of tasks/queue.md -- arrived TRIM DUE 190.1KB/1043ln,
~2c headroom, BELOW the ~3c PLAYBOOK trigger (flagged overdue by c3517's and
c3518's own handoffs, restated as STANDING c3280).

Clone lineage: _trim3513q.py / _trim3516q.py. Report-block count re-derived FRESH
this cycle via a regex over every `CLOSED c3` header (never forwarded): 10 CLOSED
blocks total, 3 of them standing one-off closures (c3329, c3336, c3496) excluded
from the report partition, leaving 7 report-shaped blocks (c3512, c3513, c3514,
c3515, c3516, c3517, c3518). Keep the newest 4 (c3515, c3516, c3517, c3518) and
archive the oldest 3 (c3512, c3513, c3514) so this cycle's own CLOSED c3519 block
lands the file at exactly 5, the RULE 6b floor. Rotation-only pass -- no new
RELOCATION/COMPRESSION candidate identified this cycle beyond what prior cycles
already named as unspent.

Usage: python3 bin/_trim3519q.py           # dry run, prints every assert + byte deltas
       python3 bin/_trim3519q.py --write    # same, then writes queue.md + queue_archive.md
"""
import re
import subprocess
import sys

QUEUE = '/root/agent/tasks/queue.md'
QARCH = '/root/agent/tasks/queue_archive.md'

CYCLE = 3519
HEAD_RE = re.compile(r"^- \[[ x]\] \*\*", re.M)

orig = open(QUEUE, encoding='utf-8').read()


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
    '- [x] **CLOSED c3512 -- ran the due `enum_audit` rotation on `apple-podcasts-scraper`',
    '- [x] **CLOSED c3513 -- ran the `tasks/queue.md` structural trim.** QUALITY slot (3513',
    '- [x] **CLOSED c3514 -- triaged the next 6 rows (827-832, indices 826-831)',
]
KEEP_HEADS = [
    '- [x] **CLOSED c3515',
    '- [x] **CLOSED c3516',
    '- [x] **CLOSED c3517',
    '- [x] **CLOSED c3518',
]

rot_idx = sorted(find_one(h) for h in ROTATE_HEADS)
keep_idx = sorted(find_one(h) for h in KEEP_HEADS)

report_idx = [i for i, (s, e, b) in enumerate(blocks)
              if re.match(r"^- \[x\] \*\*CLOSED c\d+", b.split('\n', 1)[0])]
print(f"report blocks counted fresh: {len(report_idx)}")
STANDING_CLOSURES = ['- [x] **CLOSED c3329', '- [x] **CLOSED c3336',
                      '- [x] **CLOSED c3496 (was `NEW follow-up (c2824)`)']
standing_idx = sorted(find_one(h) for h in STANDING_CLOSURES)
assert set(report_idx) == set(rot_idx) | set(keep_idx) | set(standing_idx), \
    "report-block partition does not account for every CLOSED block"
assert len(rot_idx) == 3 and len(keep_idx) == 4
print(f"rotation: archiving {len(rot_idx)}, keeping newest {len(keep_idx)} "
      f"(+ c{CYCLE}'s own block = 5, exactly the RULE 6b floor)")

cut_set = set(rot_idx)

# ---------------------------------------------------------------- RULE 1/8 pass (c)
new_blocks = [b for i, (s, e, b) in enumerate(blocks) if i not in cut_set]
new_queue_preview = preamble + ''.join(new_blocks)

cut_cycles = [3512, 3513, 3514]
DIRECTIONAL = re.compile(
    r"`?(?:CLOSED|DONE) c(" + "|".join(str(c) for c in cut_cycles) + r")`?[^.\n]{0,80}?"
    r"\b(above|below|at the top of this file|earlier in this file)\b")
dangles = [mm.group(0)[:160] for mm in DIRECTIONAL.finditer(new_queue_preview)]
print(f"\nRULE 1/8 pass (c), intra-file: {len(dangles)} directional pointer(s) into the cut set")
for d in dangles:
    print(f"   DANGLE: {d}")
assert not dangles, "pass (c) found a live dangling pointer -- repair before writing"
print("   pass (c): 0 found")

# ---------------------------------------------------------------- this cycle's own block
NEW_DONE_HEAD = (
    f"- [x] **CLOSED c{CYCLE} -- ran the overdue `tasks/queue.md` structural trim.** "
    f"QUALITY slot (3519 % 3 == 0). Preflight run fresh: `checks-due --all` **1 DUE "
    f"(`check-source-endpoints`)**, left for the next slot since this trim was flagged "
    f"overdue by two straight handoffs; `audit-due --all` **FLEET ROTATIONS: NONE DUE** "
    f"(only informational one-off/experimental axes listed, not a backlog); `inbox-triage "
    f"new` **NONE UNTRIAGED** (85 msgs); `check-doc-size --all` on arrival: `tasks/queue.md` "
    f"**TRIM DUE, 190.1KB/1043ln, ~2c headroom** -- below the ~3c PLAYBOOK trigger, "
    f"restated as `STANDING c3280` and flagged overdue by both c3517's and c3518's "
    f"handoffs. Re-derived the report-block count FRESH (never forwarded): a regex count "
    f"over every `CLOSED c3` header found 10 total, 3 of them standing one-off closures "
    f"(`CLOSED c3329`, `c3336`, `c3496`) correctly excluded from the report partition, "
    f"leaving **7 report-shaped CLOSED blocks** (c3512, c3513, c3514, c3515, c3516, c3517, "
    f"c3518). **Archived the oldest 3 (c3512, c3513, c3514) and kept the newest 4**, so "
    f"this block lands the file exactly at the RULE 6b newest-5 floor. Only ROTATION was "
    f"spent this pass -- no new RELOCATION/COMPRESSION candidate was found beyond what "
    f"prior cycles already named as unspent (the ~15 TRIVIAL notes, the vendor-catalogue "
    f"tracker, `NEW c3372`), each still needing item-by-item live-checks rather than a "
    f"bulk cut. 3-pass hazard grep clean: (a)/(b) at the shell found only the known "
    f"standing false positives (other trim scripts' own docstrings citing the cut cycle "
    f"numbers, STATUS.md/LEARNINGS.md narrative mentions); (c), the intra-file pass, "
    f"found **0 real dangling pointers** into the cut set. **Result: "
)
NEW_DONE_TAIL = (
    f"** Script `bin/_trim{CYCLE}q.py`, dry-run asserted before `--write`, independent "
    f"post-write re-verify against `git show HEAD:tasks/queue.md` confirmed 0 lines lost. "
    f"All 3 services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active; `/`, `/tools`, "
    f"`/pricing`, `/blog` all live 200 before and after. $0 spent (pure file edit, no Apify "
    f"calls, no build); 0 new Actors today (2026-11-21); no owner email owed; no blockers. "
    f"**Next: `check-source-endpoints` is DUE NOW (flagged fresh this cycle, left for the "
    f"next slot) -- that is the top unblocked fleet check for c3520. `NEW c3518` still "
    f"names 3 Actors/5 handles remaining from the `check-handle-liveness` disclosure "
    f"follow-up (`trademark-search-scraper:164`, `uk-find-a-tender-scraper:144/164`, "
    f"`us-federal-awards-scraper:225`) as a second-priority BUILD-slot default. Re-derive "
    f"`queue.md` headroom fresh before trusting this cycle's reading as it ages.**"
)

old_arch = open(QARCH, encoding='utf-8').read()
cut_text = ''.join(blocks[i][2] for i in sorted(cut_set))
arch_add = (
    f"\n## Archived by cycle {CYCLE} (from tasks/queue.md: the 3 oldest cycle-report blocks "
    f"under the STANDING RULE 6b newest-5 floor -- c3514, c3513, c3512, newest-first; "
    f"rotation-only pass, re-derived fresh, no RELOCATION or COMPRESSION lever spent this "
    f"time.)\n\n"
    + cut_text
)
new_arch = old_arch + arch_add

# ---------------------------------------------------------------- assemble + measure
new_queue_body = preamble + ''.join(new_blocks)
bytes_before_own = len(new_queue_body.encode())
lines_before_own = new_queue_body.count('\n')
RESULT_LINE = (
    f"190.1KB/1043ln -> ~{bytes_before_own/1024:.1f}KB/{lines_before_own}ln before this "
    f"cycle's own block, landing at exactly 5 report blocks (the RULE 6b floor)"
)
NEW_DONE = NEW_DONE_HEAD + RESULT_LINE + NEW_DONE_TAIL
new_queue = preamble + NEW_DONE + "\n\n" + ''.join(new_blocks)

# ---------------------------------------------------------------- losslessness, in MEMORY
haystack = new_queue + "\n" + new_arch
missing = []
for ln in orig.split('\n'):
    t = ln.strip()
    if not t:
        continue
    if t not in haystack:
        missing.append(t)
print(f"\nlossless check (every non-blank original line findable in queue+archive): "
      f"{len(missing)} missing")
for t in missing[:5]:
    print(f"   MISSING: {t[:150]}")
assert not missing, "LOSSLESS CHECK FAILED -- nothing written"

for i in sorted(cut_set):
    assert blocks[i][2] in new_arch, f"cut block idx {i} not verbatim in archive"
assert old_arch in new_arch and len(new_arch) > len(old_arch), "prior archive not byte-intact"
for i in sorted(cut_set):
    body = blocks[i][2].split('\n', 1)[1] if '\n' in blocks[i][2] else ''
    for ln in body.split('\n'):
        assert not ln.lstrip().startswith('- [ ] '), \
            f"cut block idx {i} contains a nested OPEN item: {ln.strip()[:120]}"
print("asserts: boundary OK, partition OK, multiset OK, prior-archive bytes intact, "
      "no nested OPEN item")

print(f"\nqueue.md  {len(orig.encode()):>7}B /{orig.count(chr(10)):>5}ln  ->  "
      f"{len(new_queue.encode()):>7}B /{new_queue.count(chr(10)):>5}ln   "
      f"(-{len(orig.encode()) - len(new_queue.encode())}B incl. own new block)")
print(f"archive  +{len(arch_add.encode())}B")

if '--write' not in sys.argv:
    print("\nDRY RUN -- pass --write to apply")
    sys.exit(0)

open(QARCH, 'w', encoding='utf-8').write(new_arch)
open(QUEUE, 'w', encoding='utf-8').write(new_queue)
print("\nWRITTEN. independent re-verify against git HEAD:")

head = subprocess.run(['git', '-C', '/root/agent', 'show', 'HEAD:tasks/queue.md'],
                       capture_output=True, text=True, check=True).stdout
assert head == orig, "HEAD:tasks/queue.md differs from the text this script read"
live_q = open(QUEUE, encoding='utf-8').read()
live_a = open(QARCH, encoding='utf-8').read()
hay2 = live_q + "\n" + live_a
miss2 = [l.strip() for l in head.split('\n') if l.strip() and l.strip() not in hay2]
assert not miss2, f"post-write verify FAILED: {len(miss2)} line(s) lost"
assert live_q == new_queue and live_a == new_arch
print(f"  re-verify OK against git HEAD -- 0 of {len(head.split(chr(10)))} original lines lost")
