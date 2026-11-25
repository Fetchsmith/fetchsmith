#!/root/agent/venv/bin/python
"""Cycle 3708: STANDING c3280 floor-3 CLOSED rotation on tasks/queue.md.

Clone of bin/_trim3704q.py with one difference: this cycle's own `CLOSED c3708` /
`NEW c3708` blocks were already prepended before this script ran, so the script does
ONLY the rotation. Entering the rotation the live file carries c3708/c3707/c3706/c3705,
so c3705 (oldest of four) leaves, leaving the floor of 3 newest.

Per the two _trim3492q.py bugs in notes/PLAYBOOK.md: (1) build both new file texts as
STRINGS and run every assert IN MEMORY before opening anything for writing, so a failed
check leaves both files untouched and the run is retryable; (2) compare lines by VALUE,
never with `is`.

Only CLOSED cycle records rotate. The standing non-report `- [x]` blocks are never in a
cut span -- asserted below, along with the rule that no OPEN `- [ ]` item is cut.
"""
import os
import sys

ROOT = "/root/agent"
QUEUE = os.path.join(ROOT, "tasks/queue.md")
ARCHIVE = os.path.join(ROOT, "tasks/queue_archive.md")

CUT_HEAD = "- [x] **CLOSED c3705 -- QUALITY slot (3705 % 3 == 0)."
ARCHIVE_HEADER = "## Archived by cycle 3708 (CLOSED c3705, floor-3 rotation)"


def main():
    orig = open(QUEUE).read()
    orig_lines = orig.split("\n")
    arch_orig = open(ARCHIVE).read()

    starts = [i for i, ln in enumerate(orig_lines) if ln.startswith(CUT_HEAD)]
    assert len(starts) == 1, f"expected exactly 1 CLOSED c3705 head, got {len(starts)}"
    start = starts[0]
    end = start + 1
    while end < len(orig_lines) and not (
        orig_lines[end].startswith("- [ ] **") or orig_lines[end].startswith("- [x] **")
    ):
        end += 1
    span_end = end
    while span_end - 1 > start and orig_lines[span_end - 1].strip() == "":
        span_end -= 1
    cut = orig_lines[start:span_end]

    for ln in cut:
        assert not ln.startswith("- [ ] **"), f"cut span contains an OPEN item: {ln[:80]}"
    for marker in ("NEW c3681", "RESOLVED c3672", "PARTIALLY DONE", "DECIDED c3081"):
        assert not any(ln.startswith(f"- [x] **{marker}") for ln in cut), \
            f"cut span contains standing non-report block {marker}"
    assert any("CLOSED c3705" in ln for ln in cut)
    assert sum(1 for ln in cut if ln.startswith("- [x] **")) == 1, "span must hold exactly 1 block"

    new_lines = orig_lines[:start] + orig_lines[span_end:]
    new_queue = "\n".join(new_lines)
    new_arch = arch_orig.rstrip("\n") + "\n\n" + ARCHIVE_HEADER + "\n\n" + "\n".join(cut) + "\n"

    for ln in orig_lines:
        if ln.strip() == "":
            continue
        assert ln in new_lines or ln in new_arch.split("\n"), f"LOST LINE: {ln[:120]}"
    assert not any(l.startswith(CUT_HEAD) for l in new_lines), "c3705 block still in live file"
    for c in ("CLOSED c3708", "CLOSED c3707", "CLOSED c3706"):
        assert new_queue.count(c) >= 1, f"floor-3 block {c} must stay live"
    assert new_arch.count(ARCHIVE_HEADER) == 1
    assert len(new_queue) < len(orig), "rotation must shrink the live file"

    open(QUEUE, "w").write(new_queue)
    open(ARCHIVE, "w").write(new_arch)

    live = open(QUEUE).read()
    arch = open(ARCHIVE).read()
    for ln in orig_lines:
        if ln.strip() == "":
            continue
        assert ln in live or ln in arch, f"POST-WRITE LOST LINE: {ln[:120]}"
    assert not any(l.startswith(CUT_HEAD) for l in live.split("\n")), "c3705 survived the write"
    assert any(l.startswith(CUT_HEAD) for l in arch.split("\n")), "c3705 missing from archive"
    print(f"queue.md {len(orig)}B -> {len(live)}B ({len(live) - len(orig):+d}B); "
          f"archived {len(cut)} line(s) of CLOSED c3705; lossless verified pre- and post-write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
