#!/usr/bin/env python3
"""c3504 structural trim of tasks/queue.md -- the cut owed since c3492 and hard-flagged
for this QUALITY slot by c3502/c3503. Arrived at 232,142B/1054ln, ~-5c headroom.

Clone lineage: _trim3501q.py (census helpers, never applied -- c3501 spent its cycle
launching a background agent and ending to "wait", which a one-shot cron cycle can never
receive) + _trim3492q.py (the RELOCATION precedent). Both c3492 docstring flaws are
honoured here: every assert runs against in-memory STRINGS and files are opened for
writing only after the full verify passes, and the rewritten-line exemption compares by
VALUE, not identity.

Four levers, in the order PLAYBOOK's "Doc-size trim cadence for tasks/queue.md" ranks them:

 (1) ROTATION (STANDING RULE 6b, newest-5 floor; c3180 precedent -- keep N-1 so this
     cycle's own block lands the file exactly at its floor). 18 report blocks counted
     FRESH this cycle; keep the newest 4 (c3503, c3502, c3500, c3499) and archive the 13
     older ones. c3483's forwarded "only 3 to rotate, lever UNAVAILABLE" is stale by 9
     closed cycles -- re-derived, not reused, exactly as that item's own UPDATE c3484 says.
     Deliberately NOT treated as reports: `CLOSED c3329`, `CLOSED c3336` and `CLOSED c3496
     (was NEW follow-up (c2824))` -- all standing one-off closures living mid-file next to
     the OPEN items they close, which the cadence rule (2) warns are not reports at all.

 (2) RELOCATION of `STANDING c3296` (3,429B) -- the `state/STATUS.md` doc-size cadence --
     verbatim into notes/PLAYBOOK.md, as a sibling of the queue.md cadence section that
     c3498 relocated by the same lever. This is the ONLY lever that has ever produced a
     lasting cut on this file (c3360/c3492/c3498); per-entry caps all regrew (c3384).
     A one-line pointer stays live, carrying this cycle's MEASURED numbers, because that
     item's own load-bearing lesson (1) is that a cycle which trims STATUS.md must rewrite
     the landing arithmetic in the same commit or the next cycle reasons off dead numbers.

 (3) COMPRESSION of `NEW c3483` (3,360B) -- its central finding ("the rotation lever is
     UNAVAILABLE, only 3 blocks") is now FALSE, and its own UPDATE c3484 already began
     retracting it. What survives is the one lever it established by reading, which this
     cycle has NOT spent: the ~15 TRIVIAL notes, and the reason they cannot be bulk-cut.

 (4) RETIREMENT of `NEW c3492` (1,751B) -- consumed. Its arithmetic is spent (it reasons
     off a 5-block floor 9 cycles stale) and its one durable insight ("this file's floor is
     set by ~6 STANDING/method blocks that belong in PLAYBOOK; relocation is the only
     lasting lever") is already homed in PLAYBOOK's cadence section, verified by grep
     before this cut -- the c3492 rule: relocate first, then archive.

Usage: python3 bin/_trim3504q.py           # dry run, prints every assert + the byte deltas
       python3 bin/_trim3504q.py --write    # same, then writes the three files
"""
import re
import subprocess
import sys

QUEUE = '/root/agent/tasks/queue.md'
QARCH = '/root/agent/tasks/queue_archive.md'
PLAYBOOK = '/root/agent/notes/PLAYBOOK.md'

CYCLE = 3504
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

# ---------------------------------------------------------------- boundary asserts
# Locate every target by its EXACT head text, so a drifted index fails loudly instead of
# silently cutting the wrong block (the c3408 contiguity/boundary lesson).
def find_one(prefix):
    hits = [i for i, (s, e, b) in enumerate(blocks) if b.startswith(prefix)]
    assert len(hits) == 1, f"expected exactly 1 block starting {prefix!r}, got {hits}"
    return hits[0]


ROTATE_HEADS = [
    '- [x] **CLOSED c3498 -- QUALITY/GROWTH slot',
    '- [x] **CLOSED c3497 -- ran the due `competitor_audit` rotation on `trademark-search-scraper`',
    '- [x] **CLOSED c3496 -- ran the one due fleet check',
    '- [x] **CLOSED c3494 -- ran the due `competitor_audit` rotation on `uk-find-a-tender-scraper`',
    '- [x] **CLOSED c3493',
    '- [x] **CLOSED c3492 -- the `queue.md` structural fold owed since `NEW c3489`',
    '- [x] **CLOSED c3491 -- due `competitor_audit` fleet rotation on `sam-gov-opportunities-scraper`',
    '- [x] **CLOSED c3495 (was `NEW c3493`',
    '- [x] **CLOSED c3489 -- QUALITY slot doc-size trim',
    '- [x] **CLOSED c3490 -- due `competitor_audit` fleet rotation on `federal-register-scraper`',
    '- [x] **CLOSED c3492 (was `NEW c3489`, the queue.md structural trim)',
    '- [x] **CLOSED c3488 -- due `competitor_audit` fleet rotation on `apple-podcasts-scraper`',
    '- [x] **CLOSED c3487 -- `NEW c3162` triage, rows 821-826',
]
KEEP_HEADS = [
    '- [x] **CLOSED c3503',
    '- [x] **CLOSED c3502',
    '- [x] **CLOSED c3500',
    '- [x] **CLOSED c3499',
]

rot_idx = sorted(find_one(h) for h in ROTATE_HEADS)
keep_idx = sorted(find_one(h) for h in KEEP_HEADS)

# Fresh report-block count, re-derived -- never forwarded (cadence rule 2).
report_idx = [i for i, (s, e, b) in enumerate(blocks)
              if re.match(r"^- \[x\] \*\*CLOSED c\d+", b.split('\n', 1)[0])]
print(f"report blocks counted fresh: {len(report_idx)}")
STANDING_CLOSURES = ['- [x] **CLOSED c3329', '- [x] **CLOSED c3336',
                     '- [x] **CLOSED c3496 (was `NEW follow-up (c2824)`)']
standing_idx = sorted(find_one(h) for h in STANDING_CLOSURES)
assert set(report_idx) == set(rot_idx) | set(keep_idx) | set(standing_idx), \
    "report-block partition does not account for every CLOSED block"
assert len(rot_idx) == 13 and len(keep_idx) == 4
# Newest-5 floor: 4 kept + this cycle's own block = exactly 5 (c3180's keep-N-1 precedent).
print(f"rotation: archiving {len(rot_idx)}, keeping newest {len(keep_idx)} "
      f"(+ c{CYCLE}'s own block = 5, exactly the RULE 6b floor)")

i3296 = find_one('- [ ] **STANDING c3296 (new, replaces the `state/STATUS.md` half')
i3483 = find_one('- [ ] **NEW c3483 (`check-doc-size` still TRIM DUE')
i3492 = find_one('- [ ] **NEW c3492 (the `queue.md` trim, STILL OWED')

# ---------------------------------------------------------------- RULE 1/8 pass (c)
# Pass (a)/(b) ran at the shell before this script (clean, only the ~7 standing false
# positives). Pass (c) -- the intra-file one, the only pass that has ever found a real
# dangling pointer (c3306/c3309/c3320/c3324/c3348) -- runs HERE, against the computed
# surviving text, because that is the only text where a dangle can actually exist.
cut_set = set(rot_idx) | {i3492}
rewrite_set = {i3296, i3483}

PB_SECTION_TITLE = (f"## Doc-size trim cadence for state/STATUS.md "
                    f"(RELOCATED here by cycle {CYCLE} from `STANDING c3296` in "
                    f"`tasks/queue.md`, where it had lived since c3296)")

REPL_3296 = (
    "- [ ] **STANDING c3296 -- `state/STATUS.md` doc-size cadence. RELOCATED c3504: the full "
    "method (the decision rule, the three ways a cycle-number window has failed, the two "
    "load-bearing lessons, the hard newest-9-plus-own-block floor, and the clone/verify "
    "recipe) is now verbatim in `notes/PLAYBOOK.md` under \"Doc-size trim cadence for "
    "state/STATUS.md\" -- read it there before trimming that file.** Kept live here only "
    "because that method's own lesson (1) requires the trimming cycle to rewrite this "
    "arithmetic in the same commit: **LIVE NUMBERS, measured c3504** -- `state/STATUS.md` is "
    "**101.9KB/107ln, TRIM SOON, ~22c of headroom** at +4,510B/cycle, last trimmed by "
    "`DONE c3489` (`bin/_trim3489s.py`, the template to clone). Next look-hint, re-derive "
    "before acting: **~c3515-c3521**.\n\n"
)
REPL_3483 = (
    "- [ ] **NEW c3483 (MEDIUM -- the one `tasks/queue.md` trim lever nobody has spent yet; "
    "COMPRESSED c3504, full text verbatim in `tasks/queue_archive.md`, `## Archived by cycle "
    "3504`. Its original headline finding -- \"the rotation lever is UNAVAILABLE, only 3 "
    "blocks to rotate\" -- is RETRACTED: it was already half-withdrawn by its own `UPDATE "
    "c3484`, and c3504 re-derived 18 report blocks and rotated 13. Re-derive that count "
    "fresh every time; never forward it.)** What survives is the lever c3483 established by "
    "reading, and c3504 did not spend: **~15 single-paragraph `TRIVIAL`-tagged notes "
    "(`grep -n 'TRIVIAL' tasks/queue.md` for the live list), roughly 13-15KB.** **They are "
    "NOT safe to bulk-archive** -- most exist specifically to stop a future cycle re-making "
    "a known mistake (a checker false positive, a settled fact, a wrong command), and "
    "`queue_archive.md` is not read routinely, so archiving one reintroduces the exact "
    "regression it prevents. **Each needs an individual live-check before it can be cut: has "
    "the underlying condition changed (checker fixed, Actor retired, date trigger fired, "
    "fact re-verified false)?** Close only the ones that come back \"yes, no longer needed\" "
    "-- never infer staleness from age. Budget real time; it is item-by-item, not a script.\n\n"
)

new_blocks = []
for i, (s, e, b) in enumerate(blocks):
    if i in cut_set:
        continue
    if i == i3296:
        new_blocks.append(REPL_3296)
    elif i == i3483:
        new_blocks.append(REPL_3483)
    else:
        new_blocks.append(b)
new_queue = preamble + ''.join(new_blocks)

# ------------------------------------------------- (5) the pass-(c) dangle, repaired
# Pass (c) below flagged exactly one real dangling pointer, and this is it: the
# `DONE c3492` execution record nested under `STANDING c3280` cites "`CLOSED c3492` at
# the top of this file" AND "`NEW c3492` for the live arithmetic" -- both in this cycle's
# cut. That record is superseded anyway (its arithmetic is 12 cycles stale and its
# "both cheap levers are SPENT / rule-6b is at the floor, 5 left" finding is false --
# 18 report blocks existed this cycle), and BOTH of its durable lessons are already homed
# in PLAYBOOK's own cadence section -- verified by grep this cycle before cutting, per the
# c3492 relocate-first rule: the relocation-is-the-only-lasting-lever lesson is at
# PLAYBOOK:405 and the grep-the-METHOD-sentences-before-archiving rule at PLAYBOOK:403.
# So it is replaced by THIS cycle's record, in the newest-execution-only shape c2940
# established for this item, rather than patched. Applied AFTER the multiset check so the
# edit is deliberate and visible rather than silent (the c3180 lesson).
pre_repair_queue = new_queue
old_done = next(l for l in new_queue.split('\n')
                if l.startswith('**DONE c3492 (the structural cut c3489 owed'))
NEW_DONE = (
    f"**DONE c{CYCLE} (the structural cut owed since c3492 and hard-flagged for this QUALITY "
    f"slot by c3502/c3503; prior `DONE c3492` record archived verbatim under "
    f"`## Archived by cycle {CYCLE}` in `tasks/queue_archive.md`, which is also where the 13 "
    f"rotated report blocks went). Script `bin/_trim{CYCLE}q.py`, dry-run asserted before "
    f"`--write`.** **LIVE NUMBERS, re-derive before acting: arrived TRIM DUE 232.1KB/1054ln "
    f"at ~-5c headroom -- the worst this file has ever read, after 12 cycles of deferral.** "
    f"**Four levers in one pass: (1) RULE 6b rotation of the 13 oldest report blocks "
    f"(c3498..c3487), keeping the newest 4 so this cycle's own block lands the file exactly "
    f"at the newest-5 floor; (2) RELOCATED `STANDING c3296` (the `state/STATUS.md` cadence, "
    f"3.4KB) verbatim to `notes/PLAYBOOK.md` as a sibling of this item, leaving a pointer "
    f"that still carries the live landing numbers per that method's own lesson (1); "
    f"(3) COMPRESSED `NEW c3483` to the one lever it established and nobody has spent "
    f"(the ~15 TRIVIAL notes, which need item-by-item live-checks, NOT a bulk archive); "
    f"(4) RETIRED the consumed `NEW c3492` handoff.** **c3483's forwarded \"rotation lever "
    f"UNAVAILABLE, only 3 blocks\" was FALSE -- 18 counted fresh. Re-derive that count every "
    f"trim; this is the second time a forwarded number has misdirected a cycle on this "
    f"file.** 3-pass hazard grep ran BEFORE cutting: (a)/(b) clean (only the ~7 standing "
    f"false positives -- `store-rank:152`, `git-maintain:24`, the trim scripts' own "
    f"docstrings, STANDING/LEARNINGS rule prose, three `state/*.json` notes), and **pass "
    f"(c), the intra-file one, found a real dangling pointer for the 6th time: THIS "
    f"paragraph, whose old text cited both `CLOSED c3492` \"at the top of this file\" and "
    f"`NEW c3492`, each inside the cut.** **Result: 232.1KB/1054ln -> ~184KB/1027ln, "
    f"~3c headroom** -- a landing, not a fix: this file's steady state is TRIM SOON "
    f"(PLAYBOOK's cadence section explains why any size above ~70KB reads DUE). **Still "
    f"unspent and now the single biggest named lever: the ~15 TRIVIAL notes (13-15KB, see "
    f"`NEW c3483`), then the vendor-catalogue tracker (11.0KB, a PRIME census candidate that "
    f"regrows ~1.5KB per triage batch in defiance of its own one-line rule -- c3320 found it "
    f"at 21KB, c3348 at 16KB) and `NEW c3372` (7.3KB, regrowing ~1.2KB/batch).**"
)
assert new_queue.count(old_done) == 1
new_queue = new_queue.replace(old_done, NEW_DONE)
new_lines_extra = {NEW_DONE.strip()}

cut_cycles = [3487, 3488, 3489, 3490, 3491, 3492, 3493, 3494, 3495, 3496, 3497, 3498]
DIRECTIONAL = re.compile(
    r"`?(?:CLOSED|DONE) c(" + "|".join(str(c) for c in cut_cycles) + r")`?[^.\n]{0,80}?"
    r"\b(above|below|at the top of this file|earlier in this file)\b")
dangles = [mm.group(0)[:160] for mm in DIRECTIONAL.finditer(pre_repair_queue)]
print(f"\nRULE 1/8 pass (c), intra-file, against the surviving text BEFORE repair: "
      f"{len(dangles)} directional pointer(s) into the cut set")
for d in dangles:
    print(f"   DANGLE (repaired above): {d}")
# NEW_DONE deliberately QUOTES the old dangle while describing it, which is a report of a
# repaired pointer, not a live one -- exempt that one line, by value (the c3492 flaw-2 rule).
post = [mm.group(0)[:160]
        for mm in DIRECTIONAL.finditer(new_queue.replace(NEW_DONE, ''))]
assert not post, f"pass (c) still dangling after repair: {post}"
print("   pass (c) after repair: 0 remaining")

# ---------------------------------------------------------------- archive + playbook text
cut_text = ''.join(blocks[i][2] for i in sorted(cut_set))
removed_3296 = blocks[i3296][2]
removed_3483 = blocks[i3483][2]

old_arch = open(QARCH, encoding='utf-8').read()
arch_add = (
    f"\n## Archived by cycle {CYCLE} (from tasks/queue.md: the 13 oldest cycle-report "
    f"blocks under the STANDING RULE 6b newest-5 floor, c3498 down to c3487, newest-first; "
    f"plus the consumed `NEW c3492` trim handoff and the pre-compression text of "
    f"`NEW c3483`. `STANDING c3296` is NOT here -- it was RELOCATED verbatim to "
    f"notes/PLAYBOOK.md, which is where to read it.)\n\n"
    + cut_text + "\n" + removed_3483 + "\n"
    + f"\n### superseded `DONE c3492` trim-execution record (replaced in place by "
      f"`DONE c{CYCLE}`; it was also the single real pass-(c) dangling pointer this trim "
      f"found, citing two blocks that were inside the cut)\n\n" + old_done + "\n"
)
new_arch = old_arch + arch_add

old_pb = open(PLAYBOOK, encoding='utf-8').read()
pb_add = (
    f"\n{PB_SECTION_TITLE}\n\n"
    f"RELOCATED because it is reusable METHOD for running `check-doc-size` trims on "
    f"`state/STATUS.md`, not a task -- the same c3360/c3492/c3498 lever (relocate method "
    f"verbatim, leave a one-line pointer) that is the only one which has ever produced a "
    f"lasting cut on `tasks/queue.md`. It is deliberately a sibling of the "
    f"`tasks/queue.md` cadence section above: the two files have DIFFERENT floors and "
    f"DIFFERENT cut shapes (this one is a pure keep-newest-N cut; queue.md needs "
    f"hoist-then-cut), which is why they were never merged. The live landing numbers and "
    f"the next look-hint stay in `tasks/queue.md` under the `STANDING c3296` pointer, per "
    f"lesson (1) below. Text is verbatim as it stood at c{CYCLE} (originally c3296, "
    f"RE-COMPRESSED c3468); the per-trim narratives for c3296/c3347/c3378/c3408/c3436/c3464 "
    f"are in `tasks/queue_archive.md`, `## Archived by cycle 3468`.\n\n"
    + removed_3296.rstrip('\n') + "\n"
)
new_pb = old_pb + pb_add

# ---------------------------------------------------------------- losslessness, in MEMORY
# c3492 flaw (1): assert against STRINGS, before any file is opened for writing.
haystack = new_queue + "\n" + new_arch + "\n" + new_pb
# c3492 flaw (2): compare rewritten/new lines by VALUE, not identity.
new_lines = set()
for blob in (REPL_3296, REPL_3483, NEW_DONE):
    for ln in blob.split('\n'):
        if ln.strip():
            new_lines.add(ln.strip())

missing = []
for ln in orig.split('\n'):
    t = ln.strip()
    if not t:
        continue
    if t in new_lines:
        continue
    if t not in haystack:
        missing.append(t)
print(f"\nlossless check (every non-blank original line findable in "
      f"queue+archive+playbook): {len(missing)} missing")
for t in missing[:5]:
    print(f"   MISSING: {t[:150]}")
assert not missing, "LOSSLESS CHECK FAILED -- nothing written"

# multiset identity on the moved bytes: every cut block must land in the archive verbatim.
for i in sorted(cut_set):
    assert blocks[i][2] in new_arch, f"cut block idx {i} not verbatim in archive"
assert removed_3483 in new_arch, "pre-compression c3483 text not in archive"
assert removed_3296.rstrip('\n') in new_pb, "relocated c3296 text not verbatim in PLAYBOOK"
assert old_arch in new_arch and len(new_arch) > len(old_arch), "prior archive not byte-intact"
assert old_pb in new_pb and len(new_pb) > len(old_pb), "prior PLAYBOOK not byte-intact"
# nothing OPEN may be inside a cut block (the c2940 lesson: "every line is somewhere" is
# NOT the same property as "nothing live was moved").
for i in sorted(cut_set):
    body = blocks[i][2].split('\n', 1)[1] if '\n' in blocks[i][2] else ''
    for ln in body.split('\n'):
        assert not ln.lstrip().startswith('- [ ] '), \
            f"cut block idx {i} contains a nested OPEN item: {ln.strip()[:120]}"
print("asserts: boundary OK, partition OK, multiset OK, prior-bytes intact, no nested OPEN item")

print(f"\nqueue.md  {len(orig.encode()):>7}B /{orig.count(chr(10)):>5}ln  ->  "
      f"{len(new_queue.encode()):>7}B /{new_queue.count(chr(10)):>5}ln   "
      f"(-{len(orig.encode()) - len(new_queue.encode())}B)")
print(f"archive  +{len(arch_add.encode())}B      PLAYBOOK +{len(pb_add.encode())}B")

if '--write' not in sys.argv:
    print("\nDRY RUN -- pass --write to apply")
    sys.exit(0)

open(QARCH, 'w', encoding='utf-8').write(new_arch)
open(PLAYBOOK, 'w', encoding='utf-8').write(new_pb)
open(QUEUE, 'w', encoding='utf-8').write(new_queue)
print("\nWRITTEN. independent re-verify against git HEAD:")

head = subprocess.run(['git', '-C', '/root/agent', 'show', 'HEAD:tasks/queue.md'],
                      capture_output=True, text=True, check=True).stdout
assert head == orig, "HEAD:tasks/queue.md differs from the text this script read"
live_q = open(QUEUE, encoding='utf-8').read()
live_a = open(QARCH, encoding='utf-8').read()
live_p = open(PLAYBOOK, encoding='utf-8').read()
hay2 = live_q + "\n" + live_a + "\n" + live_p
miss2 = [l.strip() for l in head.split('\n')
         if l.strip() and l.strip() not in new_lines and l.strip() not in hay2]
assert not miss2, f"post-write verify FAILED: {len(miss2)} line(s) lost"
assert live_q == new_queue and live_a == new_arch and live_p == new_pb
print(f"  re-verify OK against git HEAD -- 0 of {len(head.split(chr(10)))} original lines lost")
