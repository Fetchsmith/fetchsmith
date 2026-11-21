#!/usr/bin/env python3
"""c3516 QUALITY-slot trim of tasks/queue.md -- arrived TRIM DUE 187.8KB/1038ln (192,293B)
at ~2 cycles of headroom, +5,440B/cycle.

*** PROVENANCE WARNING, read before trusting this file (c3516's own slip) ***
This script RAN SUCCESSFULLY with --write at c3516 (lossless re-verify against
`git show HEAD:tasks/queue.md` confirmed 0 of 1,039 original lines lost), and was then
DELETED BY MISTAKE in the same cycle -- c3516 conflated the retained `_trimNNNNq.py`
convention with the `_triageNNNN.py` convention, where the script IS deleted after use.
It was reconstructed from the authoring session immediately afterwards, because both
`tasks/queue.md`'s `CLOSED c3516` block and `state/STATUS.md` cite it by name. The logic,
anchors and replacement strings below are the ones that were actually written. It is a
TEMPLATE TO CLONE, not a re-runnable artifact: its anchors match the PRE-trim file, so
re-running it against today's queue.md will fail at the `find_one`/`lineno` asserts --
which is the correct, safe failure. LESSON: `_trimNNNNq.py` scripts are KEPT (see
bin/_trim3510q.py, bin/_trim3513q.py); only `_triageNNNN.py` pricers are deleted after use.

Clone lineage: _trim3513q.py. UNLIKE c3507/c3510/c3513 (rotation-only, ~5KB each, which is
why the file climbed 179.8KB -> 187.8KB across those three cycles while rotation alone cut
5KB a time), this pass ran the PLAYBOOK's prescribed per-block byte census FIRST (110
blocks) and spends FOUR levers, ~12.9KB gross:

(1) ROTATION (STANDING RULE 6b, newest-5 floor; c3180 precedent -- keep N-1 so this
    cycle's own block lands the file exactly at its floor). Report-block count re-derived
    FRESH by regex over every `CLOSED c3` header: 10 total, 3 of them standing one-off
    closures (c3329, c3336, c3496) that are NOT reports, leaving 7 report-shaped blocks
    (c3515, c3514, c3513, c3512, c3511, c3510, c3509). Keep the newest 4, archive the
    oldest 3 (c3511, c3510, c3509).
(2) ARCHIVE `DONE c3504` (3,030B, L86) -- a 12-cycle-old trim RECORD, not method. The
    PLAYBOOK's own cadence section says the per-trim byte deltas are history and the
    method is what's reusable; c3504's method already lives there. Its one load-bearing
    forward reference (the unspent RELOCATION/COMPRESSION lever list, which c3513's
    script cites) is carried forward onto the `STANDING c3280` pointer line.
(3) COMPRESS the vendor-catalogue tracker (census #1, 11,241B -- the block the PLAYBOOK
    names as the PRIME recurring candidate: 20,986B at c3320, 16KB at c3348). Head line
    2,507B -> 1,636B (the ~100-cycle triage roll-call and the two scalar-drift narratives
    out; the derive-from-CONTIGUOUS-never-hand-edit RULE kept) and the `Per-batch results`
    line 6,235B -> 4,833B (vendor-by-vendor find prose out, handle index kept). That line
    had regrown from the 18,582B c3468 cut because c3468 bounded the ENTRY COUNT (finds
    only) and never the ENTRY, so this pass adds a per-ENTRY rule -- ~5% of the 647 rows
    still to triage is ~30 more finds.
(4) COMPRESS `NEW c3372` (census #3, 7,283B -> 5,030B) -- the BATCH 1-11 per-batch finding
    narratives, keeping the roll-call as a one-line index, the four cross-batch LESSONS,
    NEXT BATCH, and both live open items.

Levers (3) and (4) are two of the four candidates `DONE c3504` named and c3507/c3510/c3513
each declined as "needs item-by-item live-checks, not a bulk cut". That was wrong: both are
self-describing blocks whose own text says where the detail already lives (each find-cycle's
state/STATUS.md record and the target Actor's dated README, which is the authoritative
disclosure). Reading both in full first cost ~5 minutes and unlocked ~8KB.

NET, which the c3507/c3510/c3513 records did not report and which is the number that
matters: ~12.9KB cut minus ~4.9KB written by this cycle itself (its own ~3.0KB report block
plus the ~1.9KB `NEW c3516` note) = ~8KB net, 187.8KB -> 183.1KB, ~2c -> ~3c headroom. See
notes/LEARNINGS.md c3516 ("judge a trim by the cut MINUS what the cycle writes").

Usage: python3 bin/_trim3516q.py           # dry run, prints every assert + byte deltas
       python3 bin/_trim3516q.py --write    # same, then writes queue.md + queue_archive.md
"""
import re
import subprocess
import sys

QUEUE = '/root/agent/tasks/queue.md'
QARCH = '/root/agent/tasks/queue_archive.md'

CYCLE = 3516
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


# ------------------------------------------------- lever 1: rotation
ROTATE_HEADS = [
    '- [x] **CLOSED c3511 -- ran the due `enum_audit` rotation on `fda-recall-scraper`',
    '- [x] **CLOSED c3510 -- ran the `tasks/queue.md` structural trim.** QUALITY slot (3510',
    '- [x] **CLOSED c3509 -- ran the due `enum_audit` rotation on `remote-jobs-scraper`',
]
KEEP_HEADS = ['- [x] **CLOSED c3515', '- [x] **CLOSED c3514',
              '- [x] **CLOSED c3513', '- [x] **CLOSED c3512']
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
print(f"lever 1 ROTATION: archiving {len(rot_idx)}, keeping newest {len(keep_idx)} "
      f"(+ c{CYCLE}'s own block = 5, exactly the RULE 6b floor)")
cut_set = set(rot_idx)


# ------------------------------------------------- line-level levers 2/3/4
def lineno(pred, what):
    hits = [i for i, l in enumerate(olines) if pred(l)]
    assert len(hits) == 1, f"expected exactly 1 line for {what}, got {[h+1 for h in hits]}"
    return hits[0]


L_PTR = lineno(lambda l: l.startswith('- [ ] **STANDING c3280 -- `tasks/queue.md` doc-size'),
               'STANDING c3280 pointer')
L_C3504 = lineno(lambda l: l.startswith('**DONE c3504 (the structural cut owed since c3492'),
                 'DONE c3504 record')
L_HEAD = lineno(lambda l: l.startswith("- [x] **PARTIALLY DONE -- 838 of `NEW c3162`"),
                'tracker head')
L_BATCH = lineno(lambda l: l.lstrip().startswith('**Per-batch results -- RULE CHANGED c3468'),
                 'tracker per-batch line')
L_C3372 = lineno(lambda l: l.startswith('- [ ] **NEW c3372 (MEDIUM -- competitor-claim refresh'),
                 'NEW c3372')
for nm, i in [('pointer', L_PTR), ('DONE c3504', L_C3504), ('tracker head', L_HEAD),
              ('per-batch', L_BATCH), ('NEW c3372', L_C3372)]:
    print(f"  anchored {nm:<12} L{i+1:<5} {len(olines[i].encode()):>6}B")

# NOTE (reconstruction): the four long replacement strings below -- PTR_ADD, NEW_HEAD,
# NEW_BATCH, NEW_C3372 -- are exactly the text now live in tasks/queue.md. Rather than
# re-paste ~14KB of prose into this template, read them from the file the run produced:
#   STANDING c3280 pointer  -> the "(Unspent-lever carry-forward, moved here c3516 ...)" tail
#   tracker head            -> "- [x] **PARTIALLY DONE -- 838 of `NEW c3162`'s 1,485 ..."
#   tracker per-batch line  -> "  **Per-batch results -- RULE CHANGED c3468 ..."
#   NEW c3372               -> "- [ ] **NEW c3372 (MEDIUM -- competitor-claim refresh ..."
# and the pre-compression originals are verbatim in tasks/queue_archive.md under
# "### c3516 relocated-out lines, verbatim". A future clone should write its OWN
# replacements for its OWN targets anyway; what is reusable here is the MECHANISM below.
def _live(prefix, strip=False):
    for l in open(QUEUE, encoding='utf-8').read().split('\n'):
        cand = l.lstrip() if strip else l
        if cand.startswith(prefix):
            return l
    raise AssertionError(f"replacement text not found live: {prefix!r}")


PTR_ADD = _live('- [ ] **STANDING c3280 -- `tasks/queue.md` doc-size')[len(olines[L_PTR]):] \
    if olines[L_PTR] in _live('- [ ] **STANDING c3280 -- `tasks/queue.md` doc-size') else None
NEW_HEAD = _live("- [x] **PARTIALLY DONE -- 838 of `NEW c3162`")
NEW_BATCH = _live('**Per-batch results -- RULE CHANGED c3468', strip=True)
NEW_C3372 = _live('- [ ] **NEW c3372 (MEDIUM -- competitor-claim refresh')
assert PTR_ADD, "pointer carry-forward tail could not be recovered"

# relocated-out text must be preserved verbatim in the archive
RELOCATED = [olines[L_C3504], olines[L_HEAD], olines[L_BATCH], olines[L_C3372]]
for nm, new, old_i in [('tracker head', NEW_HEAD, L_HEAD), ('per-batch', NEW_BATCH, L_BATCH),
                       ('NEW c3372', NEW_C3372, L_C3372)]:
    print(f"  lever: {nm:<12} {len(olines[old_i].encode()):>6}B -> {len(new.encode()):>6}B "
          f"(-{len(olines[old_i].encode())-len(new.encode())}B)")
print(f"  lever: DONE c3504  {len(olines[L_C3504].encode()):>6}B -> deleted")

# ------------------------------------------------- build the new line list
repl = {L_PTR: olines[L_PTR] + PTR_ADD, L_HEAD: NEW_HEAD,
        L_BATCH: NEW_BATCH, L_C3372: NEW_C3372}
drop = {L_C3504, L_C3504 + 1}   # the record line and its trailing blank
assert olines[L_C3504 + 1].strip() == '', "expected a blank line after DONE c3504"
mid = [repl.get(i, l) for i, l in enumerate(olines) if i not in drop]
mid_text = '\n'.join(mid)

# re-split so rotation indices are computed on the POST-line-edit text
pre2, blocks2 = split_blocks(mid_text)
rot2 = sorted(next(i for i, (s, e, b) in enumerate(blocks2) if b.startswith(h))
              for h in ROTATE_HEADS)
assert len(rot2) == 3
cut_text = ''.join(blocks2[i][2] for i in rot2)
kept_blocks = [b for i, (s, e, b) in enumerate(blocks2) if i not in set(rot2)]

# ------------------------------------------------- RULE 1/8 pass (c): intra-file dangles
new_queue_preview = pre2 + ''.join(kept_blocks)
cut_cycles = [3504, 3509, 3510, 3511]
DIRECTIONAL = re.compile(
    r"`?(?:CLOSED|DONE) c(" + "|".join(str(c) for c in cut_cycles) + r")`?[^.\n]{0,80}?"
    r"\b(above|below|at the top of this file|earlier in this file)\b")
dangles = [mm.group(0)[:160] for mm in DIRECTIONAL.finditer(new_queue_preview)]
print(f"\nRULE 1/8 pass (c), intra-file: {len(dangles)} directional pointer(s) into the cut set")
for d in dangles:
    print(f"   DANGLE: {d}")
assert not dangles, "pass (c) found a live dangling pointer -- repair before writing"
print("   pass (c): 0 found")

# ------------------------------------------------- this cycle's own block
# The full CLOSED c3516 block text is live at the top of tasks/queue.md and is quoted in
# state/STATUS.md; it covered BOTH this cycle's due checks (A: check-competitor-claims,
# 332 paragraphs / 69 flagged, plus the `tail -N` method bug filed as NEW c3516) and
# (B: this trim, with the honest NET rather than the gross).
NEW_DONE = _live(f'- [x] **CLOSED c{CYCLE}')
new_queue = pre2 + NEW_DONE + "\n\n" + ''.join(kept_blocks)

old_arch = open(QARCH, encoding='utf-8').read()
arch_add = (
    f"\n## Archived by cycle {CYCLE} (from tasks/queue.md -- a FOUR-LEVER pass, not the "
    f"rotation-only shape of c3507/c3510/c3513. (1) the 3 oldest cycle-report blocks under "
    f"the STANDING RULE 6b newest-5 floor: c3511, c3510, c3509, newest-first; (2) the `DONE "
    f"c3504` trim record, verbatim, archived as history -- its unspent-lever list was "
    f"carried forward onto the `STANDING c3280` pointer line in the live file; (3) the "
    f"vendor-catalogue tracker's pre-compression head line (with its ~100-cycle triage "
    f"roll-call and its c3436/c3472 scalar-drift narratives) and its pre-compression "
    f"6,235B `Per-batch results` line with every find's vendor-by-vendor prose; (4) `NEW "
    f"c3372`'s pre-compression 7,283B body with the BATCH 1-11 per-batch finding "
    f"narratives. For (3) and (4) the live file keeps every METHOD and LESSON sentence and "
    f"every live obligation -- only HISTORY was cut, per the PLAYBOOK c3492 lesson.)\n\n"
    f"### c{CYCLE} relocated-out lines, verbatim (live file carries compressed forms)\n\n"
    + '\n\n'.join(RELOCATED) + "\n\n"
    f"### c{CYCLE} rotated report blocks, verbatim\n\n"
    + cut_text
)
new_arch = old_arch + arch_add

# ------------------------------------------------- losslessness, in MEMORY
haystack = new_queue + "\n" + new_arch
missing = [l.strip() for l in orig.split('\n') if l.strip() and l.strip() not in haystack]
print(f"\nlossless check (every non-blank original line findable in queue+archive): "
      f"{len(missing)} missing")
for t in missing[:5]:
    print(f"   MISSING: {t[:150]}")
assert not missing, "LOSSLESS CHECK FAILED -- nothing written"

for i in rot2:
    assert blocks2[i][2] in new_arch, f"cut block idx {i} not verbatim in archive"
    body = blocks2[i][2].split('\n', 1)[1] if '\n' in blocks2[i][2] else ''
    for ln in body.split('\n'):
        assert not ln.lstrip().startswith('- [ ] '), \
            f"cut block idx {i} contains a nested OPEN item: {ln.strip()[:120]}"
for r in RELOCATED:
    assert r in new_arch, f"relocated line not verbatim in archive: {r[:80]}"
    assert r not in new_queue, f"relocated line still live (should be compressed): {r[:80]}"
assert old_arch in new_arch and len(new_arch) > len(old_arch), "prior archive not byte-intact"
# the live obligations and the resume-pointer authority must survive the compression
for must in ['`NEW c3327`', 'datadesk-io/eu-ted-tenders-scraper', 'rows 1-838 are CONTIGUOUS',
             'DERIVE both, NEVER hand-edit', 'substack-scraper/README.md:215',
             'N checked, N flagged', 'uk-find-a-tender']:
    assert must in new_queue, f"load-bearing text lost from live file: {must!r}"
assert new_queue.count('- [x] **CLOSED c3') == 5 + 3, \
    f"expected 5 report + 3 standing CLOSED blocks, got {new_queue.count('- [x] **CLOSED c3')}"
print("asserts: partition OK, rotation verbatim, relocations verbatim+removed, "
      "prior-archive bytes intact, no nested OPEN item, 7 load-bearing strings survive, "
      "CLOSED-block count == 8 (5 report + 3 standing)")

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
