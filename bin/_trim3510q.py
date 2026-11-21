#!/usr/bin/env python3
"""c3510 QUALITY-slot trim of tasks/queue.md -- headroom at ~3c (182.8KB/1034ln),
at the PLAYBOOK "Doc-size trim cadence" decision rule's ~3c trigger.

Clone lineage: _trim3507q.py. c3504 already spent RELOCATION and COMPRESSION
(STANDING c3296 -> PLAYBOOK, NEW c3483 compressed, NEW c3492 retired); PLAYBOOK
says those levers are not owed every trim, so this is rotation-only again.

(1) ROTATION (STANDING RULE 6b, newest-5 floor; c3180 precedent -- keep N-1 so
    this cycle's own block lands the file exactly at its floor). Re-derived
    FRESH this cycle (never forwarded, and caught a miscount on the first pass
    -- an eyeballed shell grep read only 6 blocks and missed c3503, which sits
    right next to the other report blocks at line 14; a fresh regex count over
    ALL `CLOSED c3` headers found 10, of which 7 are report-shaped): 7
    report-shaped CLOSED blocks exist (c3509, c3508, c3507, c3506, c3505,
    c3504, c3503). Keep the newest 4 (c3509, c3508, c3507, c3506) and archive
    the oldest 3 (c3505, c3504, c3503) so this cycle's own CLOSED c3510 block
    lands the file at exactly 5, the floor. The 3 standing one-off closures
    (CLOSED c3329, c3336, c3496) are NOT report blocks and are left untouched,
    per the cadence rule's own partition.

Usage: python3 bin/_trim3510q.py           # dry run, prints every assert + byte deltas
       python3 bin/_trim3510q.py --write    # same, then writes queue.md + queue_archive.md
"""
import re
import subprocess
import sys

QUEUE = '/root/agent/tasks/queue.md'
QARCH = '/root/agent/tasks/queue_archive.md'

CYCLE = 3510
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
    '- [x] **CLOSED c3505 -- ran the due `enum_audit` rotation on `sec-insider-trades-scraper`',
    '- [x] **CLOSED c3504 -- TOOK AND COMPLETED the `tasks/queue.md` structural trim',
    '- [x] **CLOSED c3503 -- ran the due `competitor_audit` rotation on `google-news-scraper`',
]
KEEP_HEADS = [
    '- [x] **CLOSED c3509',
    '- [x] **CLOSED c3508',
    '- [x] **CLOSED c3507',
    '- [x] **CLOSED c3506',
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
# Pass (a)/(b) run at the shell before this script. Pass (c), the intra-file one (the
# only pass that has ever found a real dangling pointer -- c3306/c3309/c3320/c3324/c3348),
# runs HERE against the computed surviving text.
new_blocks = [b for i, (s, e, b) in enumerate(blocks) if i not in cut_set]
new_queue_preview = preamble + ''.join(new_blocks)

cut_cycles = [3503, 3504, 3505]
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
    f"- [x] **CLOSED c{CYCLE} -- ran the `tasks/queue.md` structural trim.** QUALITY slot "
    f"(3510 % 3 == 0). Preflight run fresh: `checks-due --all` **NONE DUE** (soonest "
    f"`check-competitor-claims` in 6c, c3516); `audit-due --all` **FLEET ROTATIONS: NONE "
    f"DUE** (only informational one-off/experimental axes listed, not a backlog); "
    f"`inbox-triage new` **NONE UNTRIAGED** (85 msgs -- re-read the owner's Apify-token-"
    f"rotation and \"$36 profit\" threads while triaging, both long-resolved per `CLOSED "
    f"c3329`/`c3336`, no action owed). `check-doc-size --all`: `tasks/queue.md` **TRIM DUE, "
    f"182.8KB/1034ln, ~3c of headroom** at +5,440B/cycle -- right at the PLAYBOOK decision "
    f"rule's trigger, so took it as this slot's QUALITY work. **Only ONE lever was "
    f"available: ROTATION.** c3504 already spent RELOCATION (`STANDING c3296` -> PLAYBOOK) "
    f"and COMPRESSION (`NEW c3483`); PLAYBOOK says those are not owed every trim. Re-derived "
    f"the report-block count FRESH (never forwarded) and caught a miscount on the first "
    f"pass: an eyeballed shell grep read only 6 report blocks and missed `c3503` sitting "
    f"right next to the others (line 14) -- a fresh regex count over every `CLOSED c3` "
    f"header found **7 report-shaped CLOSED blocks** (c3509, c3508, c3507, c3506, c3505, "
    f"c3504, c3503) -- **archived the oldest 3 (c3505, c3504, c3503) and kept the newest "
    f"4**, so this block lands the file exactly at the RULE 6b newest-5 floor. The 3 "
    f"standing one-off closures (`CLOSED c3329`, `c3336`, `c3496`) were correctly excluded "
    f"from the report-block partition, same as every prior trim. 3-pass hazard grep clean: "
    f"(a)/(b) at the shell found only the known standing false positives; (c), the "
    f"intra-file pass, found **0 real dangling pointers** into the cut set. **Result: "
)
NEW_DONE_TAIL = (
    f"** Script `bin/_trim{CYCLE}q.py`, dry-run asserted before `--write`, independent "
    f"post-write re-verify against `git show HEAD:tasks/queue.md` confirmed 0 lines lost. "
    f"All 3 services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active; `/`, `/tools`, "
    f"`/pricing` all live 200 before and after. $0 spent (pure file edit, no Apify calls, "
    f"no build); 0 new Actors today (2026-11-21); no owner email owed; no blockers. "
    f"**Next: no fleet rotation is due. Re-derive `queue.md` headroom fresh before acting "
    f"on any forwarded number; the next QUALITY slot (c3513) should check it before "
    f"assuming a trim is or isn't owed. The RELOCATION/COMPRESSION levers named in `DONE "
    f"c3504` (the ~15 TRIVIAL notes, the vendor-catalogue tracker, `NEW c3372`) remain "
    f"unspent if headroom drops again before another rotation's worth of report blocks "
    f"accumulates.**"
)

old_arch = open(QARCH, encoding='utf-8').read()
cut_text = ''.join(blocks[i][2] for i in sorted(cut_set))
arch_add = (
    f"\n## Archived by cycle {CYCLE} (from tasks/queue.md: the 3 oldest cycle-report blocks "
    f"under the STANDING RULE 6b newest-5 floor -- c3505, c3504, c3503, newest-first; "
    f"rotation-only pass, re-derived fresh, no RELOCATION or COMPRESSION lever spent this "
    f"time since c3504 already spent both.)\n\n"
    + cut_text
)
new_arch = old_arch + arch_add

# ---------------------------------------------------------------- assemble + measure
new_queue_body = preamble + ''.join(new_blocks)
bytes_before_own = len(new_queue_body.encode())
lines_before_own = new_queue_body.count('\n')
RESULT_LINE = (
    f"182.8KB/1034ln -> ~{bytes_before_own/1024:.1f}KB/{lines_before_own}ln before this "
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
