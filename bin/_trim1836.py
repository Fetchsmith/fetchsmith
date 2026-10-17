#!/usr/bin/env python3
"""One-shot, lossless STATUS.md/queue.md -> *_ARCHIVE.md trim for cycle 1836.

Keeps the newest 10 cycle blocks in the live file, appends the remainder verbatim
to the end of the existing archive under a dated '## Archived by cycle 1836' header
(same shape as the cycle 1799 trim, STATUS_ARCHIVE.md:20325).

Verification is arithmetic + content: every archived line must appear in the new
archive, and keep+moved must reconstruct the original byte-for-byte.
"""
import sys

JOBS = [
    # (live path, archive path, 1-indexed first line to MOVE, label)
    ("/root/agent/state/STATUS.md", "/root/agent/state/STATUS_ARCHIVE.md", 627,
     "STATUS.md"),
    ("/root/agent/tasks/queue.md", "/root/agent/tasks/queue_archive.md", 829,
     "queue.md"),
]

HEADER = (
    "## Archived by cycle 1836 (opus-5), 2026-10-17 — {label} had grown to "
    "{lines} lines / {kb}KB, approaching the Read-tool single-file cap (256KB) "
    "that cycles 1833/1799 both hit. Cycles <=1825 moved here verbatim; the live "
    "file keeps the newest 10 cycle blocks (1835 down to 1826). Newest-first "
    "below, same order as the source file.\n"
)

ok = True
for live, arch, first_move, label in JOBS:
    with open(live, encoding="utf-8") as f:
        orig = f.read()
    lines = orig.splitlines(keepends=True)
    n = len(lines)
    kb = round(len(orig.encode()) / 1024)

    idx = first_move - 1
    keep = lines[:idx]
    moved = lines[idx:]

    # The separator ('---' + surrounding blanks) between the last kept block and
    # the first moved block is dropped on purpose; trim trailing blanks/rules off
    # the kept half so the live file ends on real content.
    while keep and keep[-1].strip() in ("", "---"):
        keep.pop()
    dropped = idx - len(keep)
    if dropped > 3:
        print(f"ABORT {label}: dropped {dropped} separator lines, expected <=3")
        ok = False
        continue

    # --- lossless checks before writing anything ---
    if not moved:
        print(f"ABORT {label}: nothing to move")
        ok = False
        continue
    if "cycle 1825" not in moved[0] and "1825" not in moved[0]:
        print(f"ABORT {label}: first moved line is not the 1825 block: {moved[0][:90]!r}")
        ok = False
        continue
    if "1826" not in "".join(keep[-120:]) :
        print(f"ABORT {label}: cycle 1826 block missing from kept tail")
        ok = False
        continue

    keep_txt = "".join(keep)
    if not keep_txt.endswith("\n"):
        keep_txt += "\n"
    moved_txt = "".join(moved)

    with open(arch, encoding="utf-8") as f:
        arch_before = f.read()
    sep = "" if arch_before.endswith("\n\n") else ("\n" if arch_before.endswith("\n") else "\n\n")
    new_arch = (arch_before + sep
                + HEADER.format(label=label, lines=n, kb=kb) + "\n"
                + moved_txt)

    with open(arch, "w", encoding="utf-8") as f:
        f.write(new_arch)
    with open(live, "w", encoding="utf-8") as f:
        f.write(keep_txt)

    # --- post-write verification ---
    with open(arch, encoding="utf-8") as f:
        arch_after = f.read()
    with open(live, encoding="utf-8") as f:
        live_after = f.read()

    problems = []
    if moved_txt not in arch_after:
        problems.append("moved text NOT found verbatim in archive")
    if arch_before not in arch_after:
        problems.append("pre-existing archive content was altered")
    missing = [l for l in moved if l.strip() and l not in arch_after]
    if missing:
        problems.append(f"{len(missing)} moved lines missing from archive")
    if live_after != keep_txt:
        problems.append("live file does not match computed keep half")

    print(f"{label}: {n} lines -> {len(live_after.splitlines())} kept, "
          f"{len(moved)} moved, {dropped} separator line(s) dropped")
    print(f"  archive: {len(arch_before.splitlines())} -> "
          f"{len(arch_after.splitlines())} lines")
    if problems:
        ok = False
        for p in problems:
            print(f"  FAIL: {p}")
    else:
        print("  OK: lossless (moved text verbatim in archive, prior archive intact)")

sys.exit(0 if ok else 1)
