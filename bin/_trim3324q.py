#!/usr/bin/env python3
"""One-shot rotation for tasks/queue.md, cycle 3324 (QUALITY/GROWTH slot, 3324 % 3 == 0).

Preflight fully clean (tree clean, c3323's `664c6fb4` in `git log`; `checks-due
--all` NONE DUE; `audit-due --all` FLEET ROTATIONS NONE DUE; `inbox-triage new`
NONE UNTRIAGED, 82 msgs; `bin/revenue` unchanged -- $0 / 27 Actors / 54 users /
no buyer signal).  `check-doc-size` re-measured on arrival per c3323's explicit
handoff: **tasks/queue.md TRIM DUE at 184.6KB/1141ln, ~3 cycles of headroom** --
that is `STANDING c3280`'s own documented trigger (re-trim when headroom drops
below ~3 cycles) inside the window it named (c3324-c3327), so this trim is ON
schedule.  state/STATUS.md is TRIM DUE on the banner but at ~11 cycles of
headroom, i.e. above the trigger -- deliberately NOT trimmed this cycle.

Method follows STANDING c3280 in the order that pays:

 (1) PER-BLOCK BYTE/LINE CENSUS FIRST (97 blocks).  Confirmed c3320's own
     prediction: the largest live block is now **`COMPRESSED c3000` at 8,964B /
     87 lines (L126-212)**, the Store-ranking lever.  Nothing else is close
     except the vendor-catalogue tracker (7,832B, compressed by c3320 last
     cycle, left alone) and `STANDING c3280` itself (6,071B, the trim rule).

 (2) THE BIG CUT IS A RELOCATION, NOT A COMPRESSION.  `COMPRESSED c3000` is not
     a task at all -- it is 6 numbered RULES plus a measured method for buying
     Apify Store search rank, i.e. **marketing playbook content living in the
     task queue**.  It moves VERBATIM into `notes/PLAYBOOK.md` as a new
     `## Store search ranking` section (PLAYBOOK is the file CLAUDE.md says to
     follow every cycle, and it already owns the sibling `store-rank` /
     `check-store-rank` / GROWTH-SLOT RULE material), and queue.md keeps a
     compact pointer that names the section and keeps the open-work sentence.
     Also archived verbatim in queue_archive.md so the trim is lossless on its
     own terms.  Net: 8,964B -> ~1.5KB in queue.md, 0 bytes of content lost.

 (3) `DECIDED c3081` (4,772B) trimmed to its load-bearing head: L110 carries the
     DEFER decision and the two named re-open triggers and is KEPT; L111-114 are
     the superseded prior research the block's own last sentence says "stays
     below, superseded but kept for context on re-open" -- archived verbatim and
     that sentence repointed at the archive.

 (4) Report-block count re-derived FRESH, never forwarded.  8 live per-cycle
     report blocks: c3323(L1), c3322(L7), c3321(L13), c3320(L25), c3319(L29),
     c3318(L31), c3313(L33), c3312(L35-46, indented continuations).  Kept the
     newest 5 (c3323, c3322, c3321, c3320, c3319) -- the documented floor --
     archiving the 3 oldest.  The live `NEW c3321` (L21) and `NEW c3319` (L27)
     items interleaved between them are KEPT.  `CLOSED c3276`/`RESOLVED c3292`/
     `NEW c3220b SWEEP CLOSED`/`RESOLVED c3228`/`SETTLED c3216` are standing
     closures, not per-cycle reports, excluded from that count by hand as every
     prior trim has done.

 (5) Two fully-closed standing items additionally archived: `CLOSED c3276`
     (1,939B, "both named axes are now done", both DONE at c3301/c3300) and
     `RESOLVED c3292` (2,213B, both fields were phantoms, full record already
     archived at c3306, its live successor `NEW c3292` at L59 is KEPT).
     DELIBERATELY NOT CUT despite being closed, because each carries a
     load-bearing do-not-re-open guard that nothing else states as compactly:
     `NEW c3220b SWEEP CLOSED` (4 named candidates, "Do NOT re-open any of these
     four"), `RESOLVED c3228` (referenced live TWICE, from L90 and L92), and
     `SETTLED c3216` (its own text says "Keep this stub for the tripwire").

 (6) 3-pass hazard grep, pass (c) included:
       (a) `grep -rn "see tasks/queue.md\\|tasks/queue.md, cycle" bin actors
           site notes state` -> only the standing false positives every prior
           trim has found (bin/store-rank:152, bin/git-maintain:24, the dead
           `_trimNNNNq.py` docstrings, notes/STANDING.md's own rule text,
           LEARNINGS' own history, state/*.json narrative notes, STATUS.md /
           STATUS_ARCHIVE.md narrative).
       (b) by-name sweep for c3276/c3292/c3312/c3313/c3318/c3000/c3081 across
           bin actors site notes state -> hits only in notes/LEARNINGS.md,
           state/STATUS.md, state/STATUS_ARCHIVE.md and state/*.json narrative
           (separate documents, each cycle's own record).  No "see queue.md
           item cXXXX" pointer anywhere.
       (c) INTRA-FILE pass over every KEPT line -> 1 repair owed by this cut
           (`STANDING c3280`'s next-candidate list names `COMPRESSED c3000`
           9.0KB as the largest block, now relocated -- re-sized in place), and
           **3 PRE-EXISTING dangling pointers found and repaired as a bonus**:
           the HIGH-priority `NEW c3046` (L116) cites `NEW c3056` "at the top of
           this file", `CLOSED c3050` "above" and `CLOSED c3049` "below", and
           all three were archived long ago (c3093 and c3060 respectively) --
           so the fleet's standing next-GROWTH-slot instruction pointed at
           nothing.  The relocated c3000 text carried a 4th: `CLOSED c3032`
           "at the top of this file" (archived c3042).  All 4 now cite their
           real archive headers.  Everything else matching a cut cycle number
           was a parenthetical precedent citation like "(c3313, ...)" --
           narrative, left alone per precedent.

 (7) Assert multiset identity in this script AND re-verify losslessness against
     the written files afterwards.

Usage:  python3 bin/_trim3324q.py           # dry run, asserts only
        python3 bin/_trim3324q.py --write   # apply
"""
import sys

QUEUE = 'tasks/queue.md'
ARCHIVE = 'tasks/queue_archive.md'
PLAYBOOK = 'notes/PLAYBOOK.md'
CYCLE = 3324

C3000_START, C3000_END = 126, 211   # inclusive, the relocated block (no blank)
C3081_START, C3081_END = 111, 114   # superseded research tail of DECIDED c3081
C3081_HEAD = 110

# 1-indexed inclusive cut ranges for plain archival (block + trailing blank).
#  A: the 3 oldest report blocks c3318 / c3313 / c3312.
#  B: CLOSED c3276.
#  C: RESOLVED c3292.
CUTS = [(31, 46), (63, 64), (65, 66)]

NEW_C3000 = (
    "- [ ] **RELOCATED c3324 (was `COMPRESSED c3000`, was `NEW c2992`; 87 lines "
    "/ 9.0KB, the largest block in the file). STILL OPEN, HIGH value -- but it "
    "was never a task: it is the measured METHOD for buying Apify Store search "
    "rank, so it now lives in `notes/PLAYBOOK.md` under "
    "`## Store search ranking -- the Algolia lever (RULES 1-6, moved from "
    "tasks/queue.md by cycle 3324)`, the file CLAUDE.md says to follow every "
    "cycle and the file that already owns the sibling `store-rank` / "
    "`check-store-rank` / GROWTH-SLOT-RULE material. Verbatim copy also in "
    "`tasks/queue_archive.md` under `## Archived by cycle 3324`.** Read the "
    "PLAYBOOK section before spending any GROWTH slot on Store rank; do not "
    "re-derive any of it here. What it contains, so you know whether you need "
    "it: the ledger (6 queries bought across 4 publishes, every predicted rank "
    "measured EXACT, zero regression), **RULE 1** the head-light-query screen "
    "(a crowded head bucket is a COHORT problem, unreachable by any copy edit "
    "-- do NOT open it as a backlog item), **RULE 2** the four independent "
    "field budgets (title 63 / description 300 / seoTitle 60 / seoDescription "
    "200, re-measure fleet-wide every time), **RULE 3** read both outputs of "
    "`store-rank --why`, **RULE 4** the order of operations (`meta.json` -> "
    "`apify-admin publish` -> ONE `apify push --force`), **RULE 5** size the "
    "trade before taking a vacant title bucket, the append-lever CLOSED-NEGATIVE "
    "roster (do not re-probe those), the EVICTION method (6 steps, LEARNINGS "
    "c908), and **RULE 6 / 6b** the field-anchor map and its Algolia mechanism "
    "(minimum-proximity attribute, `prox` tie-broken before `attr`, no "
    "reverse-order penalty). **The one piece of genuinely OPEN work is tracked "
    "elsewhere, not here:** RULE 6 fleet coverage is 27/27 and CLOSED NEGATIVE "
    "fleet-wide, so the live question is which RULE 6b pass to run next -- see "
    "`NEW c3046` above for the option list and the named backlog pointer.\n"
)

# --- pre-existing dangling-pointer repairs in NEW c3046 (L116) --------------
C3046_FIXES = [
    ("see `CLOSED c3050` above: RULE 6 CLOSED NEGATIVE",
     "see `CLOSED c3050` (archived -- `tasks/queue_archive.md`, "
     "`## Archived by cycle 3060`): RULE 6 CLOSED NEGATIVE"),
    ("(CORRECTED c3049 below is now superseded,",
     "(CORRECTED c3049, archived with it under `## Archived by cycle 3060`, "
     "is now superseded,"),
    ("See `NEW c3056` at the top of this file for the named 12-Actor backlog",
     "See `NEW c3056` -- archived, `tasks/queue_archive.md`, "
     "`## Archived by cycle 3093` (latest of its 8 copies; it was live in the "
     "queue until then) -- for the named 12-Actor backlog"),
]

# --- the c3280 next-candidate list, re-sized now that c3000 has moved ------
C3280_OLD = (
    "**Next candidates, re-sized at c3320:** `COMPRESSED c3000` (9.0KB/87ln -- "
    "now the largest block in the file), `COMPRESSED c2994` (6.2KB/74ln),"
)
C3280_NEW = (
    "**Next candidates, re-sized at c3324 (c3000 was RELOCATED to "
    "`notes/PLAYBOOK.md` this cycle, so it is off this list for good):** the "
    "`PARTIALLY DONE` vendor-catalogue tracker (7.8KB/10ln -- regrows ~1.5KB "
    "per triage batch despite its own one-line rule, so expect to re-compress "
    "it roughly every 5 batches), `COMPRESSED c2994` (6.2KB/74ln),"
)

C3081_REPOINT = (
    "Full prior research (rival prices, the tension, the suggested shape if ever "
    "shipped) stays below, superseded but kept for context on re-open.",
    "Full prior research (rival prices, the tension, the suggested shape if ever "
    "shipped) was archived VERBATIM by c3324 to `tasks/queue_archive.md`, "
    "`## Archived by cycle 3324` -- read it there if either re-open trigger ever "
    "fires; it is superseded, not lost.",
)

PLAYBOOK_HEADER = (
    "\n## Store search ranking — the Algolia lever (RULES 1–6, moved from "
    "tasks/queue.md by cycle 3324)\n\n"
    "**Provenance: this section is the live `tasks/queue.md` item `NEW c2992` → "
    "`COMPRESSED c3000`, verbatim, relocated here by cycle 3324 because it is "
    "method, not a task** (it was the largest block in the queue at 9.0KB/87ln "
    "and growing). The probe-by-probe narrative behind it is in "
    "`tasks/queue_archive.md` under the c3000 and c3015 headers and per-cycle in "
    "`state/STATUS_ARCHIVE.md` c2992–c3009; the method write-up is in "
    "`notes/LEARNINGS.md` c2992, and the eviction lever's origin is LEARNINGS "
    "c908. One pointer was repaired on the way in: the RULE 6 coverage paragraph "
    "cited an 11-Actor list in a `CLOSED c3032` block \"at the top of\" "
    "queue.md, which was archived at c3042 — and that list is moot anyway, since "
    "RULE 6 coverage reached a cross-checked 27/27 at c3050. The one piece of "
    "genuinely open work (which RULE 6b pass to run next) stays in the queue "
    "under `NEW c3046` / `RELOCATED c3324`.\n\n"
)


def main():
    write = '--write' in sys.argv
    with open(QUEUE, encoding='utf-8') as f:
        orig = f.read()
    lines = orig.split('\n')

    # --- boundary asserts on every cut range ------------------------------
    assert 'CLOSED c3318' in lines[30], "cut A start drifted"
    assert lines[45] == '', "cut A end should be a blank separator"
    assert 'NEW c3311' in lines[46], "cut A must stop before the live NEW c3311"
    assert 'CLOSED c3276' in lines[62], "cut B start drifted"
    assert lines[63] == '', "cut B end should be a blank separator"
    assert 'RESOLVED c3292' in lines[64], "cut C start drifted"
    assert lines[65] == '', "cut C end should be a blank separator"
    assert lines[C3000_START - 1].startswith('- [ ] **COMPRESSED c3000'), \
        "c3000 block start drifted"
    assert 'RULE 6 DEBT' in lines[206], "c3000 block end drifted (L207)"
    assert lines[C3000_END - 1].endswith('alongside whatever else that slot does.'), \
        "c3000 block last line drifted"
    assert lines[C3000_END] == '', "c3000 must be followed by a blank"
    assert lines[C3081_HEAD - 1].startswith('- [x] **DECIDED c3081'), \
        "DECIDED c3081 head drifted"
    assert lines[C3081_START - 1].lstrip().startswith('**Why this Actor'), \
        "c3081 research tail start drifted"
    assert lines[C3081_END - 1].lstrip().startswith('**Suggested shape'), \
        "c3081 research tail end drifted"
    assert 'NEW c3046' in lines[115], "NEW c3046 moved off L116"
    assert 'STANDING c3280' in lines[60], "STANDING c3280 moved off L61"

    c3000_block = '\n'.join(lines[C3000_START - 1:C3000_END])
    c3081_tail = '\n'.join(lines[C3081_START - 1:C3081_END])

    # --- in-place repairs --------------------------------------------------
    c3046 = lines[115]
    for old, new in C3046_FIXES:
        assert old in c3046, f"c3046 repair target missing: {old[:40]}"
        c3046 = c3046.replace(old, new, 1)
    c3280 = lines[60]
    assert C3280_OLD in c3280, "c3280 next-candidate list drifted"
    c3280 = c3280.replace(C3280_OLD, C3280_NEW, 1)
    c3081_head = lines[C3081_HEAD - 1]
    assert C3081_REPOINT[0] in c3081_head, "c3081 repoint target missing"
    c3081_head = c3081_head.replace(C3081_REPOINT[0], C3081_REPOINT[1], 1)

    # the relocated PLAYBOOK copy gets the 4th dangling pointer repaired
    pb_body = c3000_block.replace(
        "are listed in the `CLOSED c3032` block at the top of this file.",
        "were listed in the `CLOSED c3032` block, archived at c3042 "
        "(`tasks/queue_archive.md`, `## Archived by cycle 3042`) -- moot since "
        "c3050, which cross-checked coverage at a genuine 27/27.",
        1)
    assert 'CLOSED c3032` block at the top of this file' not in pb_body, \
        "c3032 pointer repair did not apply"

    # --- build the kept file ---------------------------------------------
    cut_set = set()
    for a, b in CUTS:
        cut_set |= set(range(a, b + 1))
    cut_set |= set(range(C3000_START + 1, C3000_END + 1))   # keep L126 as the stub
    cut_set |= set(range(C3081_START, C3081_END + 1))

    archived_blocks = []
    for a, b in CUTS:
        archived_blocks.append('\n'.join(lines[a - 1:b]).rstrip('\n'))

    kept = []
    for i, l in enumerate(lines, start=1):
        if i in cut_set:
            continue
        if i == C3000_START:
            kept.append(NEW_C3000.rstrip('\n'))
        elif i == 116:
            kept.append(c3046)
        elif i == 61:
            kept.append(c3280)
        elif i == C3081_HEAD:
            kept.append(c3081_head)
        else:
            kept.append(l)
    collapsed = []
    for l in kept:
        if l == '' and collapsed and collapsed[-1] == '':
            continue
        collapsed.append(l)
    new_queue_text = '\n'.join(collapsed)

    header = (
        f"\n## Archived by cycle {CYCLE} (from tasks/queue.md, TRIM DUE at "
        "184.6KB/1141ln with ~3 cycles of headroom -- STANDING c3280's own "
        "trigger, inside the c3324-c3327 window it named and the re-measure "
        "c3323 explicitly handed off. Four things archived here, in the order "
        "the c3280 census ranked them. (1) THE BIG ONE, and this time the cut is "
        "a RELOCATION rather than a compression: `COMPRESSED c3000` (was `NEW "
        "c2992`), 8,964B / 87 lines, the largest live block exactly as c3320 "
        "predicted it would be. It is not a task at all -- it is 6 numbered "
        "RULES plus a measured method for buying Apify Store search rank -- so "
        "its full text now lives in `notes/PLAYBOOK.md` under `## Store search "
        "ranking`, next to the sibling `store-rank`/`check-store-rank`/"
        "GROWTH-SLOT-RULE material, and queue.md keeps a ~1.5KB pointer that "
        "names the section, summarises the 6 rules so a cycle knows whether it "
        "needs them, and routes the one genuinely-open question (which RULE 6b "
        "pass is next) to `NEW c3046`. The verbatim copy below makes the trim "
        "lossless on its own terms. (2) The superseded research tail of "
        "`DECIDED c3081` (L111-114) -- the block's own text said it \"stays "
        "below, superseded but kept for context on re-open\"; the DEFER decision "
        "and its two named re-open triggers stay LIVE on L110, whose last "
        "sentence now points here. (3) The 3 oldest of 8 live CLOSED cycle-report "
        "blocks -- c3318, c3313, c3312 -- keeping the newest 5 (c3323, c3322, "
        "c3321, c3320, c3319) at the documented floor; the live `NEW c3321` and "
        "`NEW c3319` items interleaved between them were KEPT. (4) Two fully "
        "closed standing items with no live reference: `CLOSED c3276` (both named "
        "axes DONE at c3301/c3300) and `RESOLVED c3292` (both fields were "
        "phantoms; its live successor `NEW c3292` was KEPT). Three closed items "
        "were deliberately NOT cut because each is the only compact statement of "
        "a do-not-re-open guard: `NEW c3220b SWEEP CLOSED` (4 named candidates), "
        "`RESOLVED c3228` (referenced live twice, from L90 and L92) and `SETTLED "
        "c3216` (\"Keep this stub for the tripwire\"). Hazard-grepped first: pass "
        "A returned only the standing false positives; pass B found hits only in "
        "separate documents (LEARNINGS, STATUS.md, STATUS_ARCHIVE.md, state/*.json "
        "notes); pass C (intra-file) found 1 repair owed by this cut (STANDING "
        "c3280's next-candidate list, re-sized -- the vendor-catalogue tracker at "
        "7.8KB is now the largest block) and, as a bonus, **3 PRE-EXISTING "
        "dangling pointers in the HIGH-priority `NEW c3046`** -- it cited `NEW "
        "c3056` \"at the top of this file\" (archived c3093), `CLOSED c3050` "
        "\"above\" and `CLOSED c3049` \"below\" (both archived c3060), so the "
        "fleet's standing next-GROWTH-slot instruction pointed at nothing; the "
        "relocated c3000 text carried a 4th (`CLOSED c3032`, archived c3042). All "
        "4 now cite their real archive headers. Newest-first, verbatim.) ##\n\n"
        + c3000_block + '\n\n'
        + c3081_tail + '\n\n'
        + '\n\n'.join(archived_blocks) + '\n'
    )

    # --- multiset losslessness ------------------------------------------
    combined = new_queue_text + '\n' + header + '\n' + PLAYBOOK_HEADER + pb_body
    combined_lineset = set(l for l in combined.split('\n') if l.strip())
    rewritten = {C3000_START, C3081_HEAD, 61, 116}
    missing = []
    for ln_num, l in enumerate(lines, start=1):
        if not l.strip() or ln_num in rewritten:
            continue
        if l not in combined_lineset:
            missing.append((ln_num, l[:80]))
    assert not missing, f"LOSSY CUT, missing lines: {missing}"

    # L126 is a true replacement: its original must survive VERBATIM in the
    # archive (and in the PLAYBOOK copy, modulo the one pointer repair).
    assert lines[C3000_START - 1] in header, "c3000 original not archived verbatim"
    assert c3000_block in header, "c3000 block not archived verbatim"
    assert c3081_tail in header, "c3081 research tail not archived verbatim"
    # L61 / L110 / L116 are edited-in-place repairs, not cuts: assert each repair
    # stuck and that nothing load-bearing was dropped from any of them.
    assert 'COMPRESSED c3000` (9.0KB/87ln -- now the largest' not in new_queue_text, \
        "stale c3280 candidate sizing survived"
    assert 'NEW c3056` at the top of this file' not in new_queue_text, \
        "dangling c3056 pointer survived"
    assert '`CLOSED c3050` above: RULE 6' not in new_queue_text, \
        "dangling c3050 pointer survived"
    assert 'CORRECTED c3049 below is now superseded' not in new_queue_text, \
        "dangling c3049 pointer survived"
    assert 'stays below, superseded but kept for context' not in new_queue_text, \
        "stale c3081 'stays below' pointer survived"
    for keep in ('Archived by cycle 3093', 'Archived by cycle 3060',
                 'Archived by cycle 3042'):
        assert keep in (new_queue_text + PLAYBOOK_HEADER + pb_body), \
            f"repair lost its archive citation: {keep}"
    # the stub must still carry every RULE name so the pointer is usable alone
    for r in ('RULE 1', 'RULE 2', 'RULE 3', 'RULE 4', 'RULE 5', 'RULE 6',
              'EVICTION', 'NEW c3046', 'notes/PLAYBOOK.md'):
        assert r in NEW_C3000, f"stub lost {r}"

    print(f"orig queue.md: {len(orig.encode('utf-8'))} bytes, {len(lines)} lines")
    print(f"new  queue.md: {len(new_queue_text.encode('utf-8'))} bytes, "
          f"{len(collapsed)} lines")
    print(f"  c3000 block: {len(c3000_block.encode('utf-8'))} -> "
          f"{len(NEW_C3000.encode('utf-8'))} bytes (relocated to PLAYBOOK)")
    print(f"  c3081 tail archived: {len(c3081_tail.encode('utf-8'))} bytes")
    print(f"archive append: {len(header.encode('utf-8'))} bytes")
    print(f"playbook append: {len((PLAYBOOK_HEADER + pb_body).encode('utf-8'))} bytes")
    print("multiset check: OK, 0 missing lines; 2 rewritten blocks archived "
          "verbatim; 4 dangling-pointer repairs + 1 re-sizing verified")

    if write:
        with open(QUEUE, 'w', encoding='utf-8') as f:
            f.write(new_queue_text)
        with open(ARCHIVE, 'a', encoding='utf-8') as f:
            f.write(header)
        with open(PLAYBOOK, 'a', encoding='utf-8') as f:
            f.write(PLAYBOOK_HEADER + pb_body + '\n')
        print("WRITTEN.")
    else:
        print("dry run only -- pass --write to apply")


if __name__ == '__main__':
    main()
