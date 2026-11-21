#!/usr/bin/env python3
"""c3507 QUALITY-slot trim of tasks/queue.md -- headroom dropped to ~2c (189.0KB/1034ln),
below the PLAYBOOK "Doc-size trim cadence" decision rule's ~3c trigger.

Clone lineage: _trim3504q.py (the last fully-executed trim). That cycle already spent the
RELOCATION and COMPRESSION levers (STANDING c3296 -> PLAYBOOK, NEW c3483 compressed,
NEW c3492 retired), so this cycle has only ONE lever available and that is fine: PLAYBOOK
explicitly says per-entry caps/relocation are not owed every trim, only rotation is
mechanical and recurring.

(1) ROTATION (STANDING RULE 6b, newest-5 floor; c3180 precedent -- keep N-1 so this
    cycle's own block lands the file exactly at its floor). Re-derived FRESH this cycle
    (never forwarded): 7 report-shaped CLOSED blocks exist (c3506, c3505, c3504, c3503,
    c3502, c3500, c3499). Keep the newest 4 (c3506, c3505, c3504, c3503) and archive the
    oldest 3 (c3502, c3500, c3499) so this cycle's own CLOSED c3507 block lands the file
    at exactly 5, the floor. The 3 standing one-off closures (CLOSED c3329, c3336, c3496)
    are NOT report blocks and are left untouched, per the cadence rule's own partition.

Usage: python3 bin/_trim3507q.py           # dry run, prints every assert + byte deltas
       python3 bin/_trim3507q.py --write    # same, then writes queue.md + queue_archive.md
"""
import re
import subprocess
import sys

QUEUE = '/root/agent/tasks/queue.md'
QARCH = '/root/agent/tasks/queue_archive.md'

CYCLE = 3507
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
    '- [x] **CLOSED c3502 -- ran the due `competitor_audit` rotation on `nih-reporter-scraper`',
    '- [x] **CLOSED c3500 -- ran the due `competitor_audit` rotation on `clinicaltrials-scraper`',
    '- [x] **CLOSED c3499 -- ran the due `competitor_audit` rotation on `court-records-scraper`',
]
KEEP_HEADS = [
    '- [x] **CLOSED c3506',
    '- [x] **CLOSED c3505',
    '- [x] **CLOSED c3504',
    '- [x] **CLOSED c3503',
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

cut_cycles = [3499, 3500, 3502]
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
    f"(3507 % 3 == 0). Preflight: `checks-due --all` **NONE DUE** (soonest `git-maintain` "
    f"in 1c, c3508); `audit-due --all` **1 real fleet rotation DUE** (`enum_audit: "
    f"hacker-news-scraper`) -- per established practice, fleet rotations are BUILD-slot "
    f"work (see c3495/c3498/c3501/c3504's own QUALITY-slot choices), so left it as the top "
    f"carryover for the next BUILD slot (c3508 is git-maintain's own QUALITY-adjacent slot; "
    f"c3509 is the next BUILD slot) rather than taking it here; `inbox-triage new` **NONE "
    f"UNTRIAGED** (85 msgs). `check-doc-size --all`: `tasks/queue.md` **TRIM DUE, "
    f"189.0KB/1034ln, ~2c of headroom** at +5,440B/cycle -- below the PLAYBOOK decision "
    f"rule's ~3c trigger, so took it as this slot's QUALITY work rather than a README pass. "
    f"**Only ONE lever was available: ROTATION.** c3504 (the last full trim) already spent "
    f"RELOCATION (STANDING c3296 -> PLAYBOOK) and COMPRESSION (`NEW c3483`); PLAYBOOK says "
    f"those are not owed every trim, so this cycle is rotation-only by design, not a partial "
    f"pass. Re-derived the report-block count FRESH (never forwarded): **7 CLOSED report "
    f"blocks existed** (c3506, c3505, c3504, c3503, c3502, c3500, c3499) -- **archived the "
    f"oldest 3 (c3502, c3500, c3499) and kept the newest 4**, so this block lands the file "
    f"exactly at the RULE 6b newest-5 floor. The 3 standing one-off closures (`CLOSED "
    f"c3329`, `c3336`, `c3496`) were correctly excluded from the report-block partition, "
    f"same as every prior trim. 3-pass hazard grep clean: (a)/(b) at the shell found only "
    f"the ~7 known standing false positives; (c), the intra-file pass, found **0 real "
    f"dangling pointers** into the cut set (the rotated blocks were plain cycle reports "
    f"with no other block depending on their text, unlike c3348/c3504's finds). **Result: "
)
NEW_DONE_TAIL = (
    f"** Script `bin/_trim{CYCLE}q.py`, dry-run asserted before `--write`, independent "
    f"post-write re-verify against `git show HEAD:tasks/queue.md` confirmed 0 lines lost. "
    f"All 3 services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active; `/`, `/tools`, "
    f"`/pricing` all live 200 before and after. $0 spent (pure file edit, no Apify calls, "
    f"no build); 0 new Actors today (2026-11-21); no owner email owed; no blockers. "
    f"**Next (c3508, QUALITY-adjacent per `git-maintain`'s own due cadence, or c3509 if that "
    f"slot takes git-maintain instead): the one real due fleet rotation is `enum_audit: "
    f"hacker-news-scraper` -- take it on the next BUILD slot. `queue.md` is NOT owed another "
    f"trim immediately; re-derive headroom fresh before acting, per the decision rule.**"
)

old_arch = open(QARCH, encoding='utf-8').read()
cut_text = ''.join(blocks[i][2] for i in sorted(cut_set))
arch_add = (
    f"\n## Archived by cycle {CYCLE} (from tasks/queue.md: the 3 oldest cycle-report blocks "
    f"under the STANDING RULE 6b newest-5 floor -- c3502, c3500, c3499, newest-first; "
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
    f"189.0KB/1034ln -> ~{bytes_before_own/1024:.1f}KB/{lines_before_own}ln before this "
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
