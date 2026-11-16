#!/usr/bin/env python3
"""One-shot rotation for tasks/queue.md, cycle 3306 (regular slot, 3306 % 3 == 0... wait
3306 % 3 == 0 is QUALITY/GROWTH; this is executed as the top-priority item the
`STANDING c3280` doc-trim item named for "the next cycle with no higher-priority
mail/checks backlog" -- preflight was fully clean: `checks-due --all` NONE DUE (soonest
`check-dead-endpoint-docs`, c3307), `audit-due --all` FLEET ROTATIONS NONE DUE,
`inbox-triage new` NONE UNTRIAGED (82 msgs), `bin/revenue` unchanged ($0/27 Actors/54
users/no buyer signal). `check-doc-size` read `tasks/queue.md` TRIM DUE at
189.4KB/1073ln, ~2 cycles of headroom -- exactly the trigger `STANDING c3280` set.

Method, same as c3280/c3295 (clone + hazard grep + multiset assert):
 (1) Per-block byte/line census (99 top-level blocks) found the 14 live
     "CLOSED cNNNN -- <slot> ... Preflight ..." cycle-report blocks (NOT a
     chronological prefix -- `NEW c3304`, `STANDING c3280`, `RESOLVED c3292`
     etc. are interleaved between them). `CLOSED c3289` and `CLOSED c3276`
     matched a loose regex but are standing-item closures, not per-cycle
     preflight reports -- excluded from the rotation on manual read.
 (2) Kept the newest 7 (c3305, c3304, c3303, c3301, c3300, c3296, c3295),
     archiving the oldest 6: c3294, c3293, c3292, c3291, c3290, c3288.
 (3) 3-pass hazard grep:
       (a) `grep -rn "see tasks/queue.md\\|tasks/queue.md, cycle" bin actors
           site notes state` -> only the long-standing false positives inside
           dead `_trimNNNNq.py` docstrings, same as every prior trim.
       (b) by-name sweep for c3294/c3293/c3292/c3291/c3290/c3288 across
           `bin actors site notes state` (excluding dead `_trim*/_triage*`
           scripts) -> hits only in each cycle's own `state/STATUS.md`,
           `notes/LEARNINGS.md` narrative, `state/fleet_checks.json`, and
           unrelated source-code comments -- none a live pointer into
           queue.md.
       (c) INTRA-FILE pass (scanned every KEPT line for the 6 target
           strings) -- 9 raw hits, of which 7 are narrative/historical
           mentions (safe to leave) and 2 are real dangling pointers,
           repaired below BEFORE the cut:
             L51 (`RESOLVED c3292`): "Full record in `CLOSED c3292` at the
               top of this file" -> repointed at the archive.
             L63 (vendor-catalogue `PARTIALLY DONE` tracker): "full detail
               in its own `CLOSED c3290` block above" -> repointed at the
               archive.
 (4) Assert multiset identity in this script, re-verify losslessness against
     the written files after.

Usage:  python3 bin/_trim3306q.py           # dry run, asserts only
        python3 bin/_trim3306q.py --write   # apply
"""
import sys

QUEUE = 'tasks/queue.md'
ARCHIVE = 'tasks/queue_archive.md'
CYCLE = 3306

# 1-indexed inclusive line ranges of the 6 oldest cycle-report blocks, newest-first.
CUTS = [(19, 20), (17, 18), (31, 32), (33, 34), (35, 36), (37, 46)]

CITATION_FIXES = {
    51: (
        "Full record in `CLOSED c3292` at the top of this file.",
        "Full record in `CLOSED c3292`, archived at c3306 -- see "
        "`tasks/queue_archive.md`, `## Archived by cycle 3306`.",
    ),
    63: (
        "full detail in its own `CLOSED c3290` block above",
        "full detail in its own `CLOSED c3290` block, archived at c3306 -- "
        "see `tasks/queue_archive.md`, `## Archived by cycle 3306`",
    ),
}


def main():
    write = '--write' in sys.argv
    with open(QUEUE, encoding='utf-8') as f:
        orig = f.read()
    lines = orig.split('\n')
    orig_lineset = sorted(l for l in lines if l.strip())

    # Apply citation fixes first (both are inside KEPT lines, not cut ranges).
    fixed = dict(lines=list(lines))
    for ln, (old, new) in CITATION_FIXES.items():
        idx = ln - 1
        assert old in fixed['lines'][idx], f"citation fix target not found on line {ln}"
        fixed['lines'][idx] = fixed['lines'][idx].replace(old, new)
    lines = fixed['lines']

    cut_set = set()
    for a, b in CUTS:
        for i in range(a, b + 1):
            cut_set.add(i)

    archived_blocks = []
    for a, b in CUTS:
        block_lines = lines[a - 1:b]
        archived_blocks.append('\n'.join(block_lines))

    kept_lines = [l for i, l in enumerate(lines, start=1) if i not in cut_set]
    # collapse any resulting double-blank-lines left by adjacent cuts
    new_text_lines = []
    for l in kept_lines:
        if l == '' and new_text_lines and new_text_lines[-1] == '':
            continue
        new_text_lines.append(l)
    new_queue_text = '\n'.join(new_text_lines)

    header = (
        f"\n## Archived by cycle {CYCLE} (from tasks/queue.md, the 6 oldest of the 14 "
        "live CLOSED cycle-report blocks -- c3294, c3293, c3292, c3291, c3290, c3288 -- "
        "archived verbatim to restore `check-doc-size` headroom per the c3280/c3295 "
        "standing doc-trim rule. Kept the newest 7 (c3305, c3304, c3303, c3301, c3300, "
        "c3296, c3295) live, above the documented floor of 5. Hazard-grepped first: Pass A "
        "(`see tasks/queue.md`/`tasks/queue.md, cycle`) returned only the same standing "
        "false positives every prior trim has found; Pass B (by-name sweep for "
        "c3288/c3290-c3294 across bin/actors/site/notes/state) found hits only inside dead "
        "`_trimNNNNq.py`/`_triageNNNN.py` docstrings and each cycle's own "
        "state/STATUS.md`/`notes/LEARNINGS.md` narrative (separate documents, not live "
        "queue.md pointers); Pass C (intra-file) found 2 real dangling pointers -- repaired "
        "in place (L51 `RESOLVED c3292`, L63 the vendor-catalogue tracker) BEFORE the cut, "
        "both now citing this archive header. Newest-first, verbatim.) ##\n\n"
        + '\n\n'.join(archived_blocks) + '\n'
    )

    # Multiset identity check: every non-blank original line must be findable
    # in kept+archived content (allowing for the 2 citation-fix lines, which
    # are intentionally rewritten, not moved).
    combined = new_queue_text + '\n' + header
    combined_lineset = set(l for l in combined.split('\n') if l.strip())
    missing = []
    for ln_num, l in enumerate(lines, start=1):
        if not l.strip():
            continue
        if ln_num in CITATION_FIXES:
            continue
        if l not in combined_lineset:
            missing.append((ln_num, l[:80]))
    assert not missing, f"LOSSY CUT, missing lines: {missing}"

    print(f"orig queue.md: {len(orig.encode('utf-8'))} bytes, {len(lines)} lines")
    print(f"new queue.md:  {len(new_queue_text.encode('utf-8'))} bytes, {len(new_text_lines)} lines")
    print(f"archive append: {len(header.encode('utf-8'))} bytes")
    print("multiset check: OK, 0 missing lines")

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
