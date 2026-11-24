#!/root/agent/venv/bin/python
"""Cycle 3684 trim on tasks/queue.md -- two passes, both lossless, both verified from disk.

The file was already OVER the line at preflight (200,527B before this cycle's own block),
so the ordinary rotation alone cannot clear it -- same situation c3672/c3676/c3680 each hit.

PASS 1 (ordinary floor-3 rotation, per the c3672 cadence in notes/PLAYBOOK.md): with this
cycle's own `CLOSED c3684` about to be prepended the file holds 4 CLOSED blocks (c3684,
c3683, c3682, c3681). Archive the single oldest -- `CLOSED c3681` -- verbatim, to hold the
floor at 3. That is the whole rotation lever at floor 3; it yields ~2.6KB.

PASS 2 (structural): ENFORCE THE FILE'S OWN c3516 RECORDING RULE on the `Per-batch results`
FINDS INDEX line (6,394B, the largest line in the file). That rule, quoted in the line's own
head, is "a find gets its HANDLE and at most a short parenthetical, never a price/tier/shape
narrative" -- and eight entries in the PRICE FINDS / NON-PRICE lists violate it with full
price-ladder narratives that each end by declaring themselves closed ("disclosed same-cycle,
build 0.1.NNN, no pending obligation"). The line ALSO states its own retention rationale
explicitly: "Handles are kept because the live `FOLD-IN REGISTER` above cross-indexes them;
what is actually OWED lives THERE and in the READMEs, never here." So the HANDLE and the
cycle tag are the live part and are preserved byte-for-byte in place (every cross-index grep
still hits); only the narrative prose is relocated. The whole pre-image line is written to
the archive verbatim, so losslessness is structural, not argued.

Deliberately NOT cut, though both are large and tempting: the `TWO LIVE OBLIGATIONS`
sentence (the only open work the line carries -- c3327's pending fold-in and the three TED
rivals owed a joint naming at the next `eu-ted-tenders-scraper` rotation), the FINDS INDEX
counts (`NEW c3348` is still open and asks for exactly those), and the c3448 INVERTED-LADDER
pointer into LEARNINGS (a method pointer, not a find narrative -- grepped first, it is live).

Rewritten lines are compared BY VALUE (the _trim3492q.py lesson), not by multiset identity.
"""
from collections import Counter

QUEUE = "/root/agent/tasks/queue.md"
ARCH = "/root/agent/tasks/queue_archive.md"
HEADER = "## Archived by cycle 3684"

orig = open(QUEUE).read()
lines = orig.split("\n")


def block(head_prefix, src):
    start = next(i for i, l in enumerate(src) if l.startswith(head_prefix))
    end = start + 1
    while end < len(src) and not src[end].startswith(("- [ ] **", "- [x] **")):
        end += 1
    assert src[end - 1].strip() == "", repr(src[end - 1])
    return start, end


# ---------- PASS 1: floor-3 rotation ----------
closed_now = [l for l in lines if l.startswith("- [x] **CLOSED c")]
assert len(closed_now) == 3, [l[:30] for l in closed_now]   # c3683, c3682, c3681 censused fresh

work = list(lines)
s, e = block("- [x] **CLOSED c3681 --", work)
cut = work[s:e - 1]                      # body only, no separating blank
work = work[:s] + work[e - 1:]
assert cut[0].startswith("- [x] **CLOSED c3681 --")
moved = Counter(lines) - Counter(work)
assert moved == Counter(cut), moved

# ---------- PASS 2: enforce the c3516 recording rule on the FINDS INDEX line ----------
ln = next(i for i, l in enumerate(work)
          if l.startswith("  **Per-batch results -- RULES (c3468"))
pre = work[ln]
assert "FINDS INDEX" in pre and "TWO LIVE OBLIGATIONS" in pre

# (narrative-to-cut, short-replacement) -- each `old` asserted present exactly once.
SWAPS = [
    (" (10-14x every-tier undercut on `ats-jobs-scraper`, the largest single-platform "
     "undercut in this niche to date -- disclosed same-cycle, `ats-jobs-scraper/README.md`, "
     "build 0.1.147, no pending obligation)", " (closed, b0.1.147)"),
    (" (same vendor's broader 6-platform listing, undercuts our Gold+ tier by 29%, "
     "ties/beats us elsewhere once its start fee is folded in -- disclosed same-cycle, "
     "`ats-jobs-scraper/README.md`, build 0.1.148, no pending obligation)",
     " (closed, b0.1.148)"),
    (" (partial undercutter on `substack-scraper` -- flat rate beats our tiered "
     "post/comment/leaderboard ladders on Free/Bronze/Silver, we win all three at Gold+ -- "
     "disclosed same-cycle, build 0.1.113, no pending obligation)", " (closed, b0.1.113)"),
    (" (4-of-7-board partial undercutter on `remote-jobs-scraper`, real threat at any run "
     "size >=2-3 jobs -- disclosed same-cycle, build 0.1.112, no pending obligation)",
     " (closed, b0.1.112)"),
    (" (flat per-store fee crosses under our per-product rate past 200/42 products on "
     "Free/Gold+, same large-catalog trade as the already-named "
     "`nexgendata/shopify-store-analyzer` -- disclosed same-cycle, "
     "`shopify-products-scraper/README.md`, build 0.1.132, no pending obligation)",
     " (closed, b0.1.132)"),
    (", a second genuine same-source TED-native rival, $0.005/notice flat -- dearer than "
     "our $0.0015 at its only rung, same price point as the already-named "
     "`dltik/ted-europa-scraper`, no new information for a buyer; bundle into the existing "
     "TED competitor_audit obligation below rather than a separate one)",
     " -- TED rival, in the joint obligation below)"),
    (", a genuine same-shape screenshot-API rival but 16.75-25x dearer at every tier plus a "
     "$0.02 start fee we do not charge -- awareness-only for its SHA-256-per-capture "
     "\"evidence\" framing, which we neither ship nor name; see `NEW c3620`)",
     " -- awareness-only, see `NEW c3620`)"),
    (", the only scope superset in a 6-handle fleet-shadow vendor -> FOLD-IN REGISTER, "
     "not an edit)", " -- FOLD-IN REGISTER)"),
]
new_line = pre
for old, short in SWAPS:
    assert new_line.count(old) == 1, (new_line.count(old), old[:70])
    new_line = new_line.replace(old, short)
assert len(new_line) < len(pre)

new_lines = list(work)
new_lines[ln] = new_line
new_queue = "\n".join(new_lines)

reloc = [
    "**Relocated verbatim -- the whole pre-image of the `Per-batch results` FINDS INDEX line "
    "(6,394B). c3684 enforced the line's OWN c3516 recording rule on it (\"a find gets its "
    "HANDLE and at most a short parenthetical, never a price/tier/shape narrative\"): every "
    "handle and cycle tag survives in place in `tasks/queue.md`, and the eight per-find price "
    "narratives below -- each of which ended by declaring itself disclosed same-cycle with no "
    "pending obligation -- were shortened to a build/status tag. The FINDS INDEX counts, the "
    "`TWO LIVE OBLIGATIONS` sentence and the c3448 INVERTED-LADDER pointer were deliberately "
    "preserved in place, not cut.**",
    "",
    pre.strip(),
]

arch_orig = open(ARCH).read()
new_arch = (arch_orig.rstrip("\n") + "\n\n" + HEADER + "\n\n"
            + "\n".join(cut) + "\n\n" + "\n".join(reloc) + "\n")

# ---------- losslessness, BEFORE any write ----------
for l in cut:
    assert l in new_arch, l[:80]
assert pre.strip() in new_arch
for old, _ in SWAPS:
    assert old in new_arch, old[:60]
# every live survivor of the rewritten line must still be present in the queue
for keep in ("FINDS INDEX", "24 bolded N/6 price finds + 10 non-price",
             "TWO LIVE OBLIGATIONS", "`nomad-agent/dynamitejobs-scraper`",
             "`pankajbhatia/ted-eu-tenders-scraper`", "INVERTED-LADDER note in LEARNINGS c3448",
             "`nomad-agent/workable-jobs-scraper`", "`ryanclinton/shopify-store-intelligence`",
             "`glasswing/jobs-search-api`", "`nexgenwatch/website-screenshot-evidence-api`",
             "`neverempty/eu-tender-monitor`"):
    assert keep in new_queue, keep
# nothing else in the file moved
untouched_before = Counter(l for i, l in enumerate(work) if i != ln)
untouched_after = Counter(l for i, l in enumerate(new_lines) if i != ln)
assert untouched_before == untouched_after

open(QUEUE, "w").write(new_queue)
open(ARCH, "w").write(new_arch)

# ---------- independent post-write re-verify ----------
q2, a2 = open(QUEUE).read(), open(ARCH).read()
assert q2 == new_queue and a2 == new_arch
for l in cut:
    if l.strip():                        # blank separators are not unique content
        assert l not in q2.split("\n"), l[:80]
    assert l in a2.split("\n"), l[:80]
assert pre not in q2.split("\n") and pre.strip() in a2
for old, _ in SWAPS:
    assert old not in q2 and old in a2, old[:60]
assert len([l for l in q2.split("\n") if l.startswith("- [x] **CLOSED c")]) == 2
print(f"queue.md {len(orig)}B/{len(lines)}ln -> {len(q2)}B/{len(q2.split(chr(10)))}ln; "
      f"archive {len(arch_orig)}B -> {len(a2)}B; rotated CLOSED c3681 ({len(cut)} lines) and "
      f"shortened the FINDS INDEX line {len(pre)}B -> {len(new_line)}B, lossless.")
