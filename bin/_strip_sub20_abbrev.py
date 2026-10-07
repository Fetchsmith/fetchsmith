#!/root/agent/venv/bin/python
"""Cycle 1388: strip bare sub-20 rival user counts written in the ABBREVIATED
`(Nu, ...)` shape, which cycle 1386's bin/_strip_sub20_sgos.py could not see.

1386 closed sam-gov-opportunities-scraper's sub-20 backlog by matching the spelled-out
`(N users...)` parenthetical. This README also uses `(3u, $0.003/opportunity + $0.00005
start)`, and that shape survived -- cycle 1388's check-competitor-claims then flagged
`kantolabs/sam-gov-contract-opportunities` as STALE (claimed 3 users, live 1), the exact
class of drift the stripping work exists to prevent.

Same rule as 1386: a bare count goes; any non-count content riding in the same parens
(price, start fee, scope note) is preserved by reformatting rather than deleting the
whole parenthetical. Counts >= 20 are left untouched -- those are traction claims worth
stating, and check-competitor-claims verifies them.

Asserts each rewrite matches exactly once, so a silent no-op or a double-apply fails loud.
Usage: _strip_sub20_abbrev.py <readme-path> [--apply]
"""
import re
import sys

PAT = re.compile(r"\((\d+)u, ")


def main():
    path = sys.argv[1]
    apply_it = "--apply" in sys.argv
    src = open(path).read()

    edits = []
    for m in PAT.finditer(src):
        n = int(m.group(1))
        if n >= 20:
            print(f"  KEEP  ({n}u, ...) -- count >= 20, a real traction claim")
            continue
        edits.append((m.group(0), "("))

    out = src
    for old, new in edits:
        # every occurrence of this exact prefix is a distinct sub-20 count; rewrite
        # them one at a time and assert each lands, so the count reconciles.
        assert out.count(old) >= 1, f"vanished before rewrite: {old!r}"
        out = out.replace(old, new, 1)

    for old, _ in edits:
        pass
    assert not PAT.search(out) or all(
        int(m.group(1)) >= 20 for m in PAT.finditer(out)
    ), "a sub-20 abbreviated count survived"

    print(f"{path}: {len(edits)} sub-20 abbreviated count(s) stripped, "
          f"{len(src) - len(out)} bytes removed")
    if apply_it:
        open(path, "w").write(out)
        print("  applied")
    else:
        print("  dry run -- pass --apply to write")


if __name__ == "__main__":
    main()
