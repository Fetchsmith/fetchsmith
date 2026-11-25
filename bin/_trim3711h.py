#!/root/agent/venv/bin/python
"""Cycle 3711, structural half: compress STANDING c3280's own line in
tasks/queue.md. That single line (the biggest in the file, ~5.4KB) had
accreted 3 generations of superseded "LIVE NUMBERS REWRITTEN"/"DONE" trim
narratives (c3672, c3684, c3701) that are pure history -- recoverable via
git and via tasks/queue_archive.md -- the same treatment c3701 already gave
NEW c3162's narrative. Compress to: the one live method pointer, an archive
pointer for the history, and the current measured state.

Build both new file texts as STRINGS, assert everything in memory first
(_trim3492q.py lesson), compare by VALUE, write only if every check passes.
"""
import os
import sys

ROOT = "/root/agent"
QUEUE = os.path.join(ROOT, "tasks/queue.md")
ARCHIVE = os.path.join(ROOT, "tasks/queue_archive.md")

OLD_HEAD = "- [ ] **STANDING c3280 -- `tasks/queue.md` doc-size trim cadence:"
ARCHIVE_HEADER = "## Archived by cycle 3711 (STANDING c3280 history compression)"

NEW_LINE = (
    "- [ ] **STANDING c3280 -- `tasks/queue.md` doc-size trim cadence: "
    "RELOCATED c3498 to `notes/PLAYBOOK.md`, `## Doc-size trim cadence for "
    "tasks/queue.md`, verbatim (decision rule, census method, 3-pass hazard "
    "grep, and the 30-trim DONE history). Read it there before any future "
    "trim -- do not re-derive the arithmetic. The `CLOSED cNNNN` floor on "
    "this file is 3 (cut from 5 at c3672; it cannot be cut again -- that is "
    "newest 2 plus the running cycle's own block).** **HISTORY COMPRESSED "
    "c3711: the c3672/c3684/c3701 \"LIVE NUMBERS REWRITTEN\"/\"DONE\" trim "
    "narratives this line used to carry verbatim are now in "
    "`tasks/queue_archive.md`, `## Archived by cycle 3711 (STANDING c3280 "
    "history compression)` -- read there for the floor-cut story and the "
    "measured-exhaustion signal (c3688: 5 straight rotations each landing "
    "at ~1 cycle headroom), not here.** **CURRENT STATE (c3711): the "
    "floor-3 rotation ran again this cycle (`bin/_trim3711q.py`, archived "
    "`CLOSED c3708`) -- still only buys ~1 cycle before the next rotation "
    "is owed, confirming rotation alone remains insufficient on its own "
    "(same signal c3688/c3700/c3704/c3709/c3710 already measured). "
    "STILL-OPEN relocation items from `NEW c3705b`, not yet done: "
    "`FOLD-IN REGISTER` (compress per-entry narrative, keep every handle "
    "and price, ~9.9KB, never an archive candidate since `NEW c3632`/"
    "`c3640`/`c3652`/`c3664` cross-index it) and `NEW c3372`/`COMPRESSED "
    "c2994` (re-read `notes/STANDING.md:12` and `_trim3540q.py`'s REJECTED "
    "list first). Next QUALITY slot: take one of those two, not another "
    "bare rotation.**"
)


def main():
    orig = open(QUEUE).read()
    orig_lines = orig.split("\n")
    arch_orig = open(ARCHIVE).read()

    starts = [i for i, ln in enumerate(orig_lines) if ln.startswith(OLD_HEAD)]
    assert len(starts) == 1, f"expected exactly 1 STANDING c3280 head, got {len(starts)}"
    idx = starts[0]
    old_line = orig_lines[idx]

    for marker in ("c3672", "c3684", "c3701", "LIVE NUMBERS REWRITTEN"):
        assert marker in old_line, f"old line missing expected marker {marker!r}"

    new_lines = list(orig_lines)
    new_lines[idx] = NEW_LINE
    new_queue = "\n".join(new_lines)

    new_arch = (
        arch_orig.rstrip("\n") + "\n\n" + ARCHIVE_HEADER + "\n\n" + old_line + "\n"
    )

    assert old_line in new_arch, "old line not found verbatim in new archive text"
    assert new_queue.count(OLD_HEAD) == 1, "compressed line missing or duplicated"
    assert len(new_queue) < len(orig), "compression must shrink the live file"
    saved = len(orig.encode()) - len(new_queue.encode())
    assert saved > 2000, f"expected a real saving, only got {saved}B"

    open(QUEUE, "w").write(new_queue)
    open(ARCHIVE, "w").write(new_arch)

    live = open(QUEUE).read()
    arch = open(ARCHIVE).read()
    assert old_line in arch, "POST-WRITE: old line missing from archive"
    assert NEW_LINE in live, "POST-WRITE: new compressed line missing from live file"
    assert old_line not in live, "POST-WRITE: old verbose line still present in live file"

    print(
        f"queue.md {len(orig.encode())}B -> {len(live.encode())}B "
        f"({len(live.encode()) - len(orig.encode()):+d}B); STANDING c3280's "
        f"history line compressed, full old text archived verbatim, lossless verified"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
