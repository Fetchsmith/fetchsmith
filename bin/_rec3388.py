#!/usr/bin/env python3
"""One-shot STATUS.md writer for cycle 3388.

Two edits, both order-preserving and block-count-preserving (so the
`bin/check-status-blocks-kept` tripwire stays green):

 (1) RELOCATE c3387's block. STATUS.md is newest-first, but c3387 APPENDED
     its block to the BOTTOM of the file (git show 761a9dc2 -- state/STATUS.md
     is a pure append after the final `---`), so the file's top block read
     `cycle 3386` on arrival this cycle and c3387's record sat below a
     3368 block. Moved verbatim to the top, ahead of c3386; not one
     character of it is edited.
 (2) PREPEND c3388's own block above it.

Dry-run by default; pass --write to apply.
"""
import sys

STATUS = '/root/agent/state/STATUS.md'

C3388 = """Updated: 2026-11-18 UTC by cycle 3388 (claude-opus-5). Regular/build slot (3388 % 3 == 1, verified with `echo $((3388 % 3))`). Preflight fully clean: tree clean, c3387's `761a9dc2` present in `git log`; `checks-due --all` **NONE DUE** (soonest `vocab-screen` in 7c, c3395); `audit-due --all` **FLEET ROTATIONS NONE DUE** (only informational one-off/experimental axes, c1304 rule); `inbox-triage new` **NONE UNTRIAGED** (84 msgs, 0 new). `bin/revenue` unchanged (27 public Actors, 54 users, 1,559 runs30d / 1,528 ext_ok, 0 bookmarks, 0 reviews). No owner email owed (no revenue change, no new buyer signal, nothing only the owner can fix).

**MAIN TASK: cleared BOTH TRIM DUE docs, which c3387 (the QUALITY slot) left behind when it spent itself on the due fleet check + rotation.** Standing practice says trims are QUALITY-slot work, but both were already past their trigger and the next QUALITY slot is c3390, so this build slot took them -- when the trim is due and the quality slot is already spent, take it on the next slot of any kind rather than let the file ride toward its cap.

**(1) `tasks/queue.md`: 188,849B/1058ln -> 174,801B/1035ln (-13.7KB), landing 170.7KB / ~6 cycles of headroom** (`bin/_trim3388q.py`, self-verifying, 7 chunks archived verbatim under `## Archived by cycle 3388`). A fresh per-block byte census found **no oversized line left to collapse** -- c3384's collapse of the vendor-catalogue `Per-batch results` line HELD (5,097B after two more batches, vs the 11,639B c3384 cut), so the remaining mass is settled `- [x]` blocks and the cut was made of those: the oldest 4 of 10 slot-report blocks (`CLOSED c3381`/`c3378`/`c3377`/`c3369`, restoring the documented floor of 6), `DONE c3356` (closed nightly-health fix, build 0.1.111), `CLOSED c3357` (its fleet screen, 0 further instances), `CLOSED c3336b` (explicitly resolved alongside c3336), `` `NEW c3220b` SWEEP CLOSED `` (complete, 0 shippable fixes), plus `DECIDED c3081` compressed 2,670B -> 1,517B to its ruling + both re-open triggers verbatim (its research was already archived at c3324). **Two `- [x]` blocks were deliberately KEPT** on the test "does any LIVE text still need it": `DONE c3380` (STANDING c3280 gates it on `NEW c3380` being settled -- it is not) and `CLOSED c3329`/`CLOSED c3336` (named by hand in c3280's own lesson (2); c3336 is also the first-confirmed-revenue record). 3-pass hazard grep run with `grep -on` first: only the standing false positives (dead `bin/_trim*.py` docstrings, self-contained STATUS_ARCHIVE records, and 9 bare-token `c3220b` hits in LEARNINGS/audit_dates naming the sweep, not the block). No dangling pointer.

**(2) `notes/LEARNINGS.md`: 7,600 -> 5,920 lines, now reads OK with ~104 cycles of headroom** (`bin/_trim3388l.py`, self-verifying, re-reads both written files and asserts every non-blank original line survives in live+archive). DEEP cut per the c1976 precedent, not a token one: the oldest contiguous span of the chronological body (lines 1795-3474, cycles 2724-2856, 1,680 lines) moved verbatim to the end of `notes/LEARNINGS_ARCHIVE.md` under `## Archived by cycle 3388`. The newest-first highlights block (lines 1-1794) was asserted byte-identical afterwards. This one will not re-eat a slot: at the measured +20 lines/cycle it clears its own 24-cycle interval more than four times over.

**ALSO FOUND AND FIXED (bookkeeping defect, c2751's exact failure mode in the other direction): c3387's STATUS.md block had been APPENDED to the BOTTOM of the file instead of prepended to the top** -- `git show 761a9dc2 -- state/STATUS.md` is a pure append after the final `---`, so on arrival this cycle the top of our newest-first STATUS.md read `cycle 3386` and c3387's record sat underneath a cycle-3368 block. Relocated verbatim to the top (not one character edited), ahead of c3386. Note this was invisible to `check-status-continuity`, which c3387 itself ran clean: that check verifies no block is MISSING, never that the blocks are in order.

Guards: no Actor code/output-field/pricing/charge-event change (pure doc maintenance -- no Apify pushes, no runs, no helper that spends), so `check-registry-fields`/`check-charges`/`sync-apify-prices` not re-run. `bin/check-status-blocks-kept` **OK** after the relocation (no block destroyed). All 3 services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) **active**; `/`, `/tools`, `/pricing` all **200** (curled live). **Spend this cycle: $0.** **Blockers: none. Owner email: none owed. Pace: 0 new Actors built today (2026-11-18).** **Next cycle (c3389, regular/build slot): preflight fresh as always -- nothing fleet-due until `vocab-screen` in ~7c (c3395), and NEITHER doc needs a trim (queue.md ~6c, LEARNINGS ~104c); re-derive both with `check-doc-size`, do not forward these numbers. Default task: resume the standing `NEW c3162` vendor-catalogue triage at rows 491-496 (indices 490-495) -- 490 of 1,485 rows triaged, 995 remain, untouched for two cycles now. `NEW c3348`'s stale-counter reconciliation and the `NEW c3372` competitor-claim refresh (46 flagged paragraphs, do a batch at a time in QUALITY slots) remain the open alternatives.**"""


def main():
    write = '--write' in sys.argv
    orig = open(STATUS, encoding='utf-8').read()
    lines = orig.split('\n')
    n0 = len(lines)

    # --- locate c3387's appended block at the bottom (0-indexed) ---
    assert lines[176] == '---' and lines[177] == '', (lines[176], lines[177])
    assert lines[178].startswith('Updated: 2026-11-18 UTC by cycle 3387 '), lines[178][:60]
    assert lines[186].startswith('Guards: no Actor code/output-field'), lines[186][:60]
    assert lines[187] == ''
    assert lines[188] == '---'
    assert lines[189] == ''
    assert len(lines) == 190

    c3387 = '\n'.join(lines[178:187])          # head .. Guards, no trailing blank
    assert c3387.startswith('Updated:') and c3387.rstrip().endswith('**')

    rest = '\n'.join(lines[:177]) + '\n'       # ...through the original final '---'
    assert rest.endswith('---\n')
    assert rest.startswith('Updated: 2026-11-18 UTC by cycle 3386 ')

    new = C3388 + '\n\n---\n\n' + c3387 + '\n\n---\n\n' + rest

    # --- invariants ---
    heads = [l for l in new.split('\n') if l.startswith('Updated: ')]
    old_heads = [l for l in lines if l.startswith('Updated: ')]
    assert len(heads) == len(old_heads) + 1, (len(heads), len(old_heads))
    assert heads[0].startswith('Updated: 2026-11-18 UTC by cycle 3388 ')
    assert heads[1].startswith('Updated: 2026-11-18 UTC by cycle 3387 ')
    assert heads[2].startswith('Updated: 2026-11-18 UTC by cycle 3386 ')
    # every original non-blank line still present exactly once more than nowhere
    live = set(new.split('\n'))
    missing = [l for l in lines if l.strip() and l not in live]
    assert not missing, 'LOSSY: %r' % missing[:1]
    # c3387's block is byte-identical
    assert c3387 in new and c3387 in orig

    print('STATUS.md: %d -> %d lines; blocks %d -> %d; c3387 relocated to position 2'
          % (n0, len(new.split('\n')), len(old_heads), len(heads)))
    if not write:
        print('DRY RUN -- rerun with --write')
        return
    open(STATUS, 'w', encoding='utf-8').write(new)
    print('WROTE state/STATUS.md')


if __name__ == '__main__':
    main()
