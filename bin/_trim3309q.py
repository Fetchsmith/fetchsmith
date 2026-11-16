#!/usr/bin/env python3
"""One-shot rotation for tasks/queue.md, cycle 3309 (QUALITY/GROWTH slot,
3309 % 3 == 0). Preflight was fully clean (tree clean, c3308's 85ab66d3 present
in git log; checks-due --all NONE DUE; audit-due --all FLEET ROTATIONS NONE DUE;
inbox-triage new NONE UNTRIAGED, 82 msgs; bin/revenue unchanged, $0/27
Actors/54 users/no buyer signal). check-doc-size read tasks/queue.md TRIM DUE
at 176.8KB/1056ln, ~4 cycles of headroom -- STANDING c3280's own note said to
re-measure at this QUALITY slot and trim if headroom < ~3 cycles; 4 is close
enough given c3311 (apify-spend) is the only thing due soon and would add
another block before the next QUALITY slot.

Method, same family as _trim3306q.py/_trim3280q.py (census + hazard grep +
multiset assert):
 (1) Fresh per-block census: `grep -n '^- \\[.\\] \\*\\*CLOSED c3[0-9]\\{3\\}'`
     (note the `[.]` -- c3304's checkbox is a stray `[ ]` despite being
     closed) found 9 live per-cycle report blocks, NOT a chronological
     prefix: c3308(L1), c3307(L2), c3305(L4), c3304(L6-9, has a short
     indented continuation), c3303(L16), c3301(L18), c3295(L20, worded
     "took the NEW c3294 DOC-SIZE item" instead of "<slot> slot" but
     confirmed a real per-cycle report by c3306's own header), c3296(L22),
     c3300(L24). `CLOSED c3276` (L32) and `CLOSED c3289` are standing-item
     closures, not per-cycle reports -- excluded by hand, same as c3306.
 (2) Kept the newest 5 (c3308, c3307, c3305, c3304, c3303) -- above the
     documented floor of 5 -- archiving the oldest 4 (c3301, c3295, c3296,
     c3300), lines 18-24 inclusive (4 single-line blocks + 3 blank
     separators, confirmed no continuation lines by reading 16-26 directly).
 (3) 3-pass hazard grep:
       (a) `grep -rn "see tasks/queue.md\\|tasks/queue.md, cycle" bin actors
           site notes state` -> only the same standing false positives every
           prior trim has found (bin/store-rank:152, bin/git-maintain:24,
           notes/STANDING.md's own rule text, LEARNINGS' own history,
           audit_dates.json's enum_audit_note, fleet_checks.json's c3162
           note, mode_scope_allow.json's _readme).
       (b) by-name sweep for c3301/c3295/c3296/c3300 across bin/actors/
           site/notes/state (excluding dead _trim*/_triage* scripts) ->
           hits only in state/audit_dates.json, notes/LEARNINGS.md,
           state/STATUS.md, state/STATUS_ARCHIVE.md -- all narrative
           mentions in SEPARATE documents (that cycle's own report, or a
           later cycle discussing it), none a "see queue.md item cXXXX"
           pointer.
       (c) INTRA-FILE pass over every kept line for the 4 target strings ->
           1 real dangling pointer found: L32 (`CLOSED c3276`, a standing
           closure, kept live) says "DONE c3301 -- CLEAN, no defect; see
           `CLOSED c3301` above" and "DONE c3300 -- ...; see `CLOSED c3300`
           above" -- both repaired below, BEFORE the cut, to cite the
           archive instead. L26/L30 (STANDING c3296/c3280) only NAME
           c3295/c3296 in their own titles/update history, not "see X
           above" pointers -- left alone per precedent (narrative mentions
           are fine).
 (4) Assert multiset identity in this script, re-verify losslessness against
     the written files after.

Usage:  python3 bin/_trim3309q.py           # dry run, asserts only
        python3 bin/_trim3309q.py --write   # apply
"""
import sys

QUEUE = 'tasks/queue.md'
ARCHIVE = 'tasks/queue_archive.md'
CYCLE = 3309

# 1-indexed inclusive line range of the 4 oldest cycle-report blocks
# (c3301, c3295, c3296, c3300) plus their 3 internal blank separators.
CUT_START, CUT_END = 18, 24

CITATION_FIXES = {
    32: (
        "see `CLOSED c3301` above, recorded as `varied_test: 3301`",
        "see `CLOSED c3301`, archived at c3309 -- `tasks/queue_archive.md`, "
        "`## Archived by cycle 3309` -- recorded as `varied_test: 3301`",
    ),
}
CITATION_FIXES_2 = {
    32: (
        "see `CLOSED c3300` above, recorded as `watch_subset_audit: 3300`",
        "see `CLOSED c3300`, archived at c3309 -- `tasks/queue_archive.md`, "
        "`## Archived by cycle 3309` -- recorded as `watch_subset_audit: 3300`",
    ),
}


def main():
    write = '--write' in sys.argv
    with open(QUEUE, encoding='utf-8') as f:
        orig = f.read()
    lines = orig.split('\n')

    # Apply both citation fixes first (both inside line 32, a KEPT line).
    for fixes in (CITATION_FIXES, CITATION_FIXES_2):
        for ln, (old, new) in fixes.items():
            idx = ln - 1
            assert old in lines[idx], f"citation fix target not found on line {ln}: {old!r}"
            lines[idx] = lines[idx].replace(old, new)

    # Sanity: boundary assert on the exact header text of the cut range.
    assert 'CLOSED c3301' in lines[CUT_START - 1], "CUT_START drifted"
    assert 'CLOSED c3300' in lines[CUT_END - 1], "CUT_END drifted"

    cut_set = set(range(CUT_START, CUT_END + 1))
    archived_block = '\n'.join(lines[CUT_START - 1:CUT_END])

    kept_lines = [l for i, l in enumerate(lines, start=1) if i not in cut_set]
    # collapse the resulting double-blank left between L17 and L25
    new_text_lines = []
    for l in kept_lines:
        if l == '' and new_text_lines and new_text_lines[-1] == '':
            continue
        new_text_lines.append(l)
    new_queue_text = '\n'.join(new_text_lines)

    header = (
        f"\n## Archived by cycle {CYCLE} (from tasks/queue.md, the 4 oldest of the 9 "
        "live CLOSED cycle-report blocks -- c3301, c3295, c3296, c3300 -- archived "
        "verbatim to restore check-doc-size headroom per the STANDING c3280 doc-trim "
        "rule (176.8KB/1056ln, ~4 cycles of headroom on arrival). Kept the newest 5 "
        "(c3308, c3307, c3305, c3304, c3303) live, at the documented floor of 5. "
        "Hazard-grepped first: Pass A (`see tasks/queue.md`/`tasks/queue.md, cycle`) "
        "returned only the same standing false positives every prior trim has found; "
        "Pass B (by-name sweep for c3295/c3296/c3300/c3301 across bin/actors/site/"
        "notes/state) found hits only inside each cycle's own state/STATUS.md / "
        "notes/LEARNINGS.md / state/STATUS_ARCHIVE.md narrative (separate documents, "
        "not live queue.md pointers); Pass C (intra-file) found 1 real dangling "
        "pointer -- `CLOSED c3276` (a standing closure, kept live) cited both "
        "`CLOSED c3301` and `CLOSED c3300` as \"above\" -- repaired in place BEFORE "
        "the cut, both now citing this archive header. Newest-first, verbatim.) ##\n\n"
        + archived_block + '\n'
    )

    # Multiset identity check: every non-blank original line must be findable
    # in kept+archived content (allowing for the 2 citation-fix spans on L32,
    # which are intentionally rewritten, not moved).
    combined = new_queue_text + '\n' + header
    combined_lineset = set(l for l in combined.split('\n') if l.strip())
    missing = []
    orig_lines = orig.split('\n')
    for ln_num, l in enumerate(orig_lines, start=1):
        if not l.strip():
            continue
        if ln_num == 32:
            continue  # rewritten in place, checked separately below
        if l not in combined_lineset:
            missing.append((ln_num, l[:80]))
    assert not missing, f"LOSSY CUT, missing lines: {missing}"

    # L32 check: both old substrings gone, both new substrings present, in the
    # kept file (not the archive).
    l32_new = new_text_lines[[i for i, l in enumerate(new_text_lines) if l.startswith('- [x] **CLOSED c3276')][0]]
    for fixes in (CITATION_FIXES, CITATION_FIXES_2):
        old, new = fixes[32]
        assert old not in l32_new, "old citation text still present on L32"
        assert new in l32_new, "new citation text missing on L32"

    print(f"orig queue.md: {len(orig.encode('utf-8'))} bytes, {len(lines)} lines")
    print(f"new queue.md:  {len(new_queue_text.encode('utf-8'))} bytes, {len(new_text_lines)} lines")
    print(f"archive append: {len(header.encode('utf-8'))} bytes")
    print("multiset check: OK, 0 missing lines; L32 citation fix verified")

    if write:
        with open(QUEUE, 'w', encoding='utf-8') as f:
            f.write(new_queue_text)
        with open(ARCHIVE, 'a', encoding='utf-8') as f:
            f.write(header)
        print("WRITTEN.")
    else:
        print("dry run only -- pass --write to apply")


if __name__ == '__main__':
    main()
