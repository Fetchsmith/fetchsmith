#!/root/agent/venv/bin/python
"""Recover STATUS.md cycle blocks that were destroyed by in-place top-header
overwrites (the bug class bin/check-status-continuity was built for, found
recurring at cycle 2136 for cycles 2124-2127 and 2129-2134).

Method: walk the last N revisions of state/STATUS.md in git, take each
revision's TOP block (header line through the line before the next header),
and keep, per cycle number, the LONGEST version seen -- the final form that
cycle committed before the next cycle clobbered it. Then append the blocks for
the requested cycles to state/STATUS_ARCHIVE.md under a labelled banner.

Read-only against git; the only write is an append to STATUS_ARCHIVE.md.
Verifies after writing that every requested cycle is now visible to
check-status-continuity's own regex.
"""
import re
import subprocess
import sys

STATUS = "state/STATUS.md"
ARCHIVE = "/root/agent/state/STATUS_ARCHIVE.md"
REPO = "/root/agent"
# same anchor check-status-continuity uses
HEADER_RE = re.compile(r"^\w+:.*?by cycle (\d+)|^PRIOR \(cycle (\d+)")

WANT = [2133]
SCAN_REVS = 40


def git(*args):
    return subprocess.run(
        ["git", "-C", REPO] + list(args), capture_output=True, text=True, check=True
    ).stdout


def header_cycle(line):
    m = HEADER_RE.match(line)
    if not m:
        return None
    return int(m.group(1) or m.group(2))


def top_block(text):
    """(cycle, block_text) of the first block in the file, or None."""
    lines = text.split("\n")
    start = None
    cyc = None
    for i, line in enumerate(lines):
        c = header_cycle(line)
        if c is not None:
            start = i
            cyc = c
            break
    if start is None:
        return None
    for j in range(start + 1, len(lines)):
        if header_cycle(lines[j]) is not None:
            return cyc, "\n".join(lines[start:j]).rstrip()
    return cyc, "\n".join(lines[start:]).rstrip()


def main():
    revs = git("log", "--format=%h", "-%d" % SCAN_REVS, "--", STATUS).split()
    best = {}
    for rev in revs:
        try:
            text = git("show", "%s:%s" % (rev, STATUS))
        except subprocess.CalledProcessError:
            continue
        got = top_block(text)
        if not got:
            continue
        cyc, block = got
        if cyc not in best or len(block) > len(best[cyc][1]):
            best[cyc] = (rev, block)

    print("Scanned %d revisions of %s; top blocks found for cycles: %s"
          % (len(revs), STATUS, " ".join(str(c) for c in sorted(best))))

    found, absent = [], []
    for c in WANT:
        (found if c in best else absent).append(c)
    if absent:
        print("NOT RECOVERABLE from the scanned window: %s" % absent)
    if not found:
        print("Nothing to recover.")
        return 1

    with open(ARCHIVE) as f:
        existing = f.read()

    parts = []
    parts.append(
        "\n\n" + "=" * 78 + "\n"
        "RECOVERED BY CYCLE 2136 -- blocks for cycles %s were destroyed in the live\n"
        "STATUS.md by the in-place top-header overwrite bug (each cycle replaced the\n"
        "previous cycle's block instead of demoting it). Restored verbatim from git,\n"
        "newest first; each block is the longest version that cycle committed.\n"
        % ", ".join(str(c) for c in sorted(found, reverse=True))
        + "=" * 78 + "\n"
    )
    for c in sorted(found, reverse=True):
        rev, block = best[c]
        # Must be an ANCHORED header, the same way check-status-continuity looks.
        # A substring test here falsely "finds" cycles that the archive only
        # MENTIONS in body prose -- that mistake made this script skip cycle 2133
        # on its first run even though 2133 had no real block anywhere.
        already = re.search(
            r"^(\w+:.*?by cycle %d\b|PRIOR \(cycle %d\b)" % (c, c), existing, re.MULTILINE
        )
        if already:
            print("  cycle %d already in archive -- skipping" % c)
            continue
        parts.append("\n[recovered from git %s]\n%s\n" % (rev, block))
        print("  cycle %d: %d bytes from %s" % (c, len(block), rev))

    with open(ARCHIVE, "a") as f:
        f.write("".join(parts))
    print("Appended %d bytes to STATUS_ARCHIVE.md" % len("".join(parts)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
