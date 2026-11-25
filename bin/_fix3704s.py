#!/root/agent/venv/bin/python
"""Cycle 3704: fix the one OUT OF ORDER pair `bin/check-status-continuity` reports in
state/STATUS.md -- the cycle-3693 block sits at the BOTTOM of the file, below cycle 3663,
in a file that is strictly newest-first.

Pre-existing defect, not introduced this cycle (the c3693 block was appended to the end
instead of the top by its own cycle -- the same failure mode queue `NEW c3388` records for
c3387). The check's own instruction is to move the block VERBATIM by hand and never to
sort, because which block is newest is a judgement call; here it is unambiguous from the
cycle number, so the move is mechanical: 3693 belongs between 3694 and 3692.

Verbatim move only -- no text of any block is altered, and the assert set proves it:
same line multiset before and after, same block count, and strictly descending cycle
numbers afterwards. Builds the new text in memory and asserts before writing
(`_trim3492q.py` bug 1).
"""
import sys

PATH = "/root/agent/state/STATUS.md"
MOVE = 3693
BEFORE = 3692  # the block the moved one must land immediately above


def heads(lines):
    out = []
    for i, ln in enumerate(lines):
        if ln.startswith("Updated: ") and " by cycle " in ln:
            out.append((i, int(ln.split(" by cycle ")[1].split()[0])))
    return out


def main():
    orig = open(PATH).read()
    lines = orig.split("\n")
    hd = heads(lines)
    order = [c for _, c in hd]
    assert order.count(MOVE) == 1 and order.count(BEFORE) == 1
    assert order[-1] == MOVE, f"expected cycle {MOVE} to be the LAST block, got {order[-1]}"

    # span of the block to move: its header, back up through the preceding `---` + blank
    # separator, and forward to end of file (it is the last block).
    start = next(i for i, c in hd if c == MOVE)
    sep = start
    while sep - 1 >= 0 and lines[sep - 1].strip() == "":
        sep -= 1
    assert lines[sep - 1].strip() == "---", f"expected --- separator above the block, got {lines[sep-1]!r}"
    span = lines[sep:]              # blank(s) + header + body (+ trailing --- / blanks)
    kept = lines[:sep]              # everything above, ending at the `---`

    # insertion point: immediately above the BEFORE block's own `---` separator
    tgt = next(i for i, c in heads(kept) if c == BEFORE)
    ins = tgt
    while ins - 1 >= 0 and kept[ins - 1].strip() == "":
        ins -= 1
    assert kept[ins - 1].strip() == "---", "expected --- separator above the target block"
    ins -= 1                        # land above that separator, mirroring the span shape

    new_lines = kept[:ins] + span + kept[ins:]
    new_text = "\n".join(new_lines)

    # --- asserts, all in memory
    assert sorted(new_lines) == sorted(lines), "line multiset changed -- not a verbatim move"
    new_order = [c for _, c in heads(new_lines)]
    assert len(new_order) == len(order), "block count changed"
    assert new_order == sorted(new_order, reverse=True), \
        f"still not strictly descending: {new_order[:14]}"
    assert new_order.index(MOVE) == new_order.index(BEFORE) - 1, "3693 not directly above 3692"

    open(PATH, "w").write(new_text)
    after = [c for _, c in heads(open(PATH).read().split("\n"))]
    assert after == sorted(after, reverse=True), "post-write order regressed"
    print(f"moved cycle {MOVE} block ({len(span)} lines) from the file tail to above "
          f"cycle {BEFORE}; {len(after)} blocks now strictly descending: {after[:6]}...")
    return 0


if __name__ == "__main__":
    sys.exit(main())
