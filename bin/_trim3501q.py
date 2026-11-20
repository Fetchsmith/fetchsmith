#!/usr/bin/env python3
"""
One-off trim script for cycle 3501 (QUALITY slot), tasks/queue.md doc-size trim.
Follows the "Doc-size trim cadence for tasks/queue.md" method in notes/PLAYBOOK.md:
  1. Per-block byte/line census (every "- [ ] **" / "- [x] **" head).
  2. Fresh report-block (CLOSED cNNNN) count/census.
  3. 3-pass hazard grep before archiving anything (incl. intra-file pass).
  4. Assert multiset identity (nothing silently dropped); re-verify losslessness
     against the actual written files afterwards.

Lesson from c3492 applied: build new file texts as STRINGS, assert against them,
and only THEN open files for writing (verify in memory, then write).
Lesson from c3492 (2): compare values, not `is`, in the lossless check.

Usage:
  python3 bin/_trim3501q.py census        # print per-block byte/line census, sorted desc
  python3 bin/_trim3501q.py find <cNNNN>  # print all blocks whose head mentions cNNNN
  python3 bin/_trim3501q.py apply         # perform the trim (archive + relocate), write files
"""
import re
import sys
import os

ROOT = "/root/agent"
QUEUE = os.path.join(ROOT, "tasks/queue.md")
ARCHIVE = os.path.join(ROOT, "tasks/queue_archive.md")

HEAD_RE = re.compile(r"^- \[[ x]\] \*\*", re.M)


def load_queue():
    with open(QUEUE, "r") as f:
        return f.read()


def split_blocks(text):
    """Split queue.md body into (preamble, [ (head_line_start, block_text) ... ])."""
    matches = list(HEAD_RE.finditer(text))
    blocks = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        blocks.append((start, end, text[start:end]))
    preamble = text[: matches[0].start()] if matches else text
    return preamble, blocks


def block_label(block_text):
    # First line, trimmed, used as a label.
    first_line = block_text.split("\n", 1)[0]
    return first_line[:160]


def census(text=None):
    text = text if text is not None else load_queue()
    preamble, blocks = split_blocks(text)
    rows = []
    for start, end, bt in blocks:
        nbytes = len(bt.encode("utf-8"))
        nlines = bt.count("\n")
        rows.append((nbytes, nlines, block_label(bt)))
    rows.sort(key=lambda r: -r[0])
    return rows, preamble, blocks


def cmd_census():
    rows, preamble, blocks = census()
    total_bytes = len(load_queue().encode("utf-8"))
    print(f"TOTAL file bytes: {total_bytes}  blocks: {len(blocks)}  preamble bytes: {len(preamble.encode('utf-8'))}")
    print(f"{'bytes':>8} {'lines':>6}  label")
    for nbytes, nlines, label in rows[:40]:
        print(f"{nbytes:8d} {nlines:6d}  {label}")


def cmd_find(tag):
    text = load_queue()
    preamble, blocks = split_blocks(text)
    for idx, (start, end, bt) in enumerate(blocks):
        if tag in block_label(bt) or (tag in bt.split("\n", 1)[0]):
            nbytes = len(bt.encode("utf-8"))
            nlines = bt.count("\n")
            print(f"--- block idx {idx}: {nbytes}B / {nlines}ln ---")
            print(bt[:4000])
            print("... [truncated]" if len(bt) > 4000 else "")


REPORT_RE = re.compile(r"^- \[x\] \*\*CLOSED c\d+")


def cmd_report_census():
    text = load_queue()
    preamble, blocks = split_blocks(text)
    reports = []
    for idx, (start, end, bt) in enumerate(blocks):
        first_line = bt.split("\n", 1)[0]
        if REPORT_RE.match(first_line):
            cid = re.search(r"CLOSED c(\d+)", first_line).group(1)
            reports.append((int(cid), idx, len(bt.encode("utf-8"))))
    reports.sort()
    print(f"Report (CLOSED cNNNN) blocks found: {len(reports)}")
    for cid, idx, nbytes in reports:
        print(f"  c{cid:5d}  idx={idx:4d}  {nbytes:6d}B")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "census":
        cmd_census()
    elif cmd == "find":
        cmd_find(sys.argv[2])
    elif cmd == "reportcensus":
        cmd_report_census()
    else:
        print("unknown command", cmd)
        sys.exit(1)
