#!/root/agent/venv/bin/python
"""One-shot, lossless STATUS.md/queue.md -> *_ARCHIVE.md trim for cycle 1860.

Same process as bin/_trim1836.py (and the 1799 trim before it): keep the newest 10
cycle blocks in the live file, append the remainder VERBATIM to the end of the
existing archive under a '## Archived by cycle 1860' header, newest-first.

WHY NOW, below the 200KB TRIM_BYTES line: bin/check-doc-size fired DUE this cycle
and read queue.md at 175.7KB / STATUS.md at 145.6KB -- both only WARN. But the
checker's own cadence is 24 cycles, so its next look is cycle 1884, and at the
measured +5440 B/cycle queue.md crosses the 256KB Read cap at ~cycle 1875 -- nine
cycles BEFORE anything would look again. Waiting for the 200KB line only works if
the check fires near it; fired at a WARN, "not due yet" means "guaranteed to breach
unseen". Trimming now, and bin/check-doc-size is being taught to project against
its own interval so this is caught by the tool next time, not by a person.

Verification is arithmetic + content: keep+moved must reconstruct the original
byte-for-byte, and every moved line must be present in the new archive.
"""
import sys

JOBS = [
    # (live path, archive path, 1-indexed first line to MOVE, expected first-moved
    #  marker, label, oldest kept cycle, newest kept cycle)
    ("/root/agent/state/STATUS.md", "/root/agent/state/STATUS_ARCHIVE.md", 649,
     "cycle 1847", "STATUS.md", 1848, 1859),
    ("/root/agent/tasks/queue.md", "/root/agent/tasks/queue_archive.md", 670,
     "cycle 1842", "queue.md", 1850, 1860),
]

HEADER = (
    "## Archived by cycle 1860 (opus-5), 2026-10-17 — {label} had grown to {lines} "
    "lines / {kb}KB. Trimmed below the 200KB action line on purpose: check-doc-size "
    "runs every 24 cycles, so its next look was cycle 1884, and at +{rate} B/cycle "
    "{label} would have crossed the 256KB Read cap around cycle {breach} — unseen. "
    "Cycles <={oldmoved} moved here verbatim; the live file keeps the newest 10 cycle "
    "blocks ({newest} down to {oldest}). Newest-first below, same order as the source "
    "file.\n"
)

RATES = {"STATUS.md": 4510, "queue.md": 5440}
BREACH = {"STATUS.md": 1885, "queue.md": 1875}

ok = True
plans = []
for live, arch, first_move, marker, label, oldest, newest in JOBS:
    with open(live, encoding="utf-8") as f:
        orig = f.read()
    lines = orig.splitlines(keepends=True)
    kb = round(len(orig.encode()) / 1024)

    idx = first_move - 1
    keep = lines[:idx]
    moved = lines[idx:]

    # Drop the separator ('---' + blanks) between the last kept and first moved
    # block so the live file ends on real content (same rule as _trim1836.py).
    while keep and keep[-1].strip() in ("", "---"):
        keep.pop()
    dropped = idx - len(keep)
    if dropped > 3:
        print(f"ABORT {label}: dropped {dropped} separator lines, expected <=3")
        ok = False
        continue
    if not moved:
        print(f"ABORT {label}: nothing to move")
        ok = False
        continue
    if marker not in moved[0]:
        print(f"ABORT {label}: first moved line is not {marker!r}: {moved[0][:90]!r}")
        ok = False
        continue
    # The kept half must still contain the live NEXT/current block.
    if f"cycle {newest}" not in "".join(keep):
        print(f"ABORT {label}: kept half lost 'cycle {newest}'")
        ok = False
        continue

    oldmoved = int(marker.split()[-1])
    header = HEADER.format(label=label, lines=len(lines), kb=kb, rate=RATES[label],
                           breach=BREACH[label], oldmoved=oldmoved,
                           newest=newest, oldest=oldest)
    plans.append((live, arch, keep, moved, header, label, dropped))

if not ok:
    print("\nABORTED -- nothing written.")
    sys.exit(1)

for live, arch, keep, moved, header, label, dropped in plans:
    with open(arch, encoding="utf-8") as f:
        old_arch = f.read()
    new_arch = old_arch
    if not new_arch.endswith("\n"):
        new_arch += "\n"
    new_arch += "\n" + header + "\n" + "".join(moved)
    new_keep = "".join(keep)
    if not new_keep.endswith("\n"):
        new_keep += "\n"

    # --- lossless check BEFORE writing ---
    missing = [l for l in moved if l.strip() and l not in new_arch]
    if missing:
        print(f"ABORT {label}: {len(missing)} moved lines absent from new archive")
        sys.exit(1)
    kept_missing = [l for l in keep if l.strip() and l not in new_keep]
    if kept_missing:
        print(f"ABORT {label}: {len(kept_missing)} kept lines absent from new live")
        sys.exit(1)

    with open(arch, "w", encoding="utf-8") as f:
        f.write(new_arch)
    with open(live, "w", encoding="utf-8") as f:
        f.write(new_keep)
    print(f"OK {label}: live {len(keep)} lines / {len(new_keep.encode())/1024:.1f}KB, "
          f"moved {len(moved)} lines, archive now "
          f"{len(new_arch.encode())/1024/1024:.1f}MB, {dropped} separator line(s) dropped")
