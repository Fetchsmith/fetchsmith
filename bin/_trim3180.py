#!/root/agent/venv/bin/python
"""One-shot lossless trim for cycle 3180 (QUALITY slot, 3180 % 3 == 0).

`check-doc-size` reported BOTH byte docs TRIM DUE via the forward-looking branch
(STATUS.md 166.3KB proj. 272KB, queue.md 178.1KB proj. 306KB, both past the 256KB
Read cap before the next 24c look).

STATUS.md: pure keep-newest-9 block cut (so this cycle's own prepended block lands
the file at exactly 10 -- the c3144 correction, not a +1 overshoot). Blocks are
separated by '---'; cut is lines 102-545 (c3169 back to c3147).

queue.md: RULE 6b rotation DOWN TO four live cycle blocks (so this cycle's block
lands it at exactly 5) PLUS the RULE 4 tail pass `NEW c3172` explicitly asked the
next trim to do instead of another bare rotation. Four cut ranges + one in-place
pointer repair:
  R1 41-76   CLOSED c3175/c3172/c3174/c3173, NEW c3172 (consumed -- this cycle IS
             its RULE 4 pass), CLOSED c3171/c3170/c3169, and the standalone
             `- [x] DONE at c3166` marker (travels with the cut: the item it closes,
             NEW c3160 (MEDIUM), is cut in R4 -- c3172's boundary rule)
  R2 79-90   CLOSED c3168   (its live children, `NEW c3168 (handoff)` at 91 and
             `NEW c3168 findings` at 94, deliberately SURVIVE)
  R3 123-126 NEW c3164 + NEW c3163 (consumed handoffs: both target cycles ran and
             closed; every third of `NEW c3160 (HIGH)` they carried is CLOSED --
             substack at c3165 (STATUS.md:135), google-news at c3164 (:153))
  R4 129-130 NEW c3160 (MEDIUM) (CLOSED as EXCLUDED at c3166, STATUS.md:127)
  REWRITE 91 repairs a pointer that would dangle: it cites "`CLOSED c3168 findings`
             below", but the surviving bullet is titled `NEW c3168 findings` and
             `CLOSED c3168` itself is being archived in R2.

Also appends STANDING.md's prior `EXECUTED c3156` paragraph verbatim to the archive
(the doc-trim item's newest-execution-only shape); the replacement paragraph is
written separately so it cannot break the multiset identity asserted here.

Dry-run by default; pass --write to apply. Every partition is asserted total,
non-overlapping and multiset-identical to the original before anything is written.
"""
import sys, os

ROOT = "/root/agent"
WRITE = "--write" in sys.argv

HDR = ("## Archived by cycle 3180 (opus-5), 2026-11-14 -- {label}: {why} "
       "Moved here VERBATIM, newest-first, same order as the source file.\n")


def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.readlines()


def write(p, text):
    if not WRITE:
        return
    with open(os.path.join(ROOT, p), "w", encoding="utf-8") as f:
        f.write(text)


def append(p, text):
    if not WRITE:
        return
    with open(os.path.join(ROOT, p), "a", encoding="utf-8") as f:
        f.write(text)


def kb(s):
    return len(s.encode()) / 1024


problems = []


def check(cond, msg):
    if not cond:
        problems.append(msg)
        print(f"  FAIL: {msg}")
    return cond


# ---------------------------------------------------------------- STATUS.md
print("== state/STATUS.md: keep-newest-9 block cut ==")
s = read("state/STATUS.md")
FIRST_MOVE = 91           # 1-indexed first line to move (the c3170 block header)
i = FIRST_MOVE - 1
s_keep, s_moved = s[:i], s[i:]

check(s_keep[0].startswith("Updated: 2026-11-14 UTC by cycle 3179"),
      f"STATUS keep does not start at c3179: {s_keep[0][:60]!r}")
check("cycle 3170" in s_moved[0],
      f"STATUS first moved line is not the c3170 header: {s_moved[0][:70]!r}")
# 9 kept blocks = 9 'Updated:' headers, c3179 down to c3171. NOTE the c3172/c3171
# boundary carries no '---' separator (a pre-existing c3172 formatting lapse, not
# unwound here -- the continuity guards match the anchored 'Updated:' header), so
# the kept blocks CANNOT be counted off the separators. Count headers.
kept_heads = [l for l in s_keep if l.startswith("Updated: ")]
check(len(kept_heads) == 9, f"STATUS kept {len(kept_heads)} blocks, expected 9")
check(not any(l.startswith("Updated: ") and any(f"cycle {c}" in l for c in range(3171, 3180))
              for l in s_moved), "STATUS is moving a block newer than c3170")

# drop the trailing separator so the live file ends on real content
while s_keep and s_keep[-1].strip() in ("", "---"):
    s_keep.pop()
dropped = i - len(s_keep)
check(dropped <= 3, f"STATUS dropped {dropped} separator lines, expected <=3")

s_keep_txt = "".join(s_keep)
if not s_keep_txt.endswith("\n"):
    s_keep_txt += "\n"
s_moved_txt = "".join(s_moved)
print(f"  {len(s)} lines / {kb(''.join(s)):.1f}KB -> {len(s_keep)} kept / "
      f"{kb(s_keep_txt):.1f}KB, {len(s_moved)} moved, {dropped} separator dropped")

# ---------------------------------------------------------------- queue.md
print("== tasks/queue.md: newest-4 rotation + RULE 4 tail pass ==")
q = read("tasks/queue.md")
CUTS = [(41, 76), (79, 90), (123, 126), (129, 130)]
# every item head expected inside the cuts, in file order
EXPECT_HEADS = [
    "- [ ] **CLOSED c3175", "- [ ] **CLOSED c3172", "- [ ] **CLOSED c3174",
    "- [ ] **CLOSED c3173", "- [ ] **NEW c3172", "- [ ] **CLOSED c3171",
    "- [ ] **CLOSED c3170", "- [ ] **CLOSED c3169", "- [x] **DONE at c3166",
    "- [ ] **CLOSED c3168",
    "- [ ] **NEW c3164", "- [ ] **NEW c3163",
    "- [ ] **NEW c3160 (MEDIUM)",
]
# heads that MUST survive (RULE 7/8: live work must not ride along)
MUST_SURVIVE = [
    "- [ ] **CLOSED c3179", "- [ ] **CLOSED c3178", "- [ ] **CLOSED c3177",
    "- [ ] **CLOSED c3176", "- [ ] **NEW c3176", "- [x] **PARTIALLY DONE at c3167",
    "- [ ] **NEW c3168 (handoff", "- [ ] **NEW c3168 findings",
    "- [ ] **NEW c3167 (handoff", "- [ ] **NEW c3162 (MEDIUM)",
    "- [x] **DONE at c3162", "- [ ] **NEW c3148", "- [ ] **NEW (c2478",
]

cut_idx = set()
for a, b in CUTS:
    check(a <= b, f"bad range {a}-{b}")
    cut_idx |= set(range(a - 1, b))
check(len(cut_idx) == sum(b - a + 1 for a, b in CUTS), "queue cut ranges overlap")

q_moved = [q[k] for k in sorted(cut_idx)]
q_keep = [l for k, l in enumerate(q) if k not in cut_idx]

# RULE 7 (c3048 adaptation): every item head in the cut must be an EXPECTED one
found = [l for l in q_moved if l.startswith("- [ ] ") or l.startswith("- [x] ")]
check(len(found) == len(EXPECT_HEADS),
      f"queue cut holds {len(found)} item heads, expected {len(EXPECT_HEADS)}")
for got, want in zip(found, EXPECT_HEADS):
    check(got.startswith(want), f"unexpected head in cut: {got[:70]!r} (wanted {want!r})")
for want in MUST_SURVIVE:
    check(sum(1 for l in q_keep if l.startswith(want)) == 1,
          f"must-survive head missing/duplicated after cut: {want!r}")

# multiset identity: keep + moved == original, exactly
check(sorted(q_keep + q_moved) == sorted(q), "queue partition is not multiset-identical")

# in-place pointer repair (breaks the identity by design, so applied AFTER the check)
OLD_P = "the verbatim output is in `CLOSED c3168 findings` below"
NEW_P = "the verbatim output is in the `NEW c3168 findings` item below"
hits = [k for k, l in enumerate(q_keep) if OLD_P in l]
check(len(hits) == 1, f"pointer repair matched {len(hits)} lines, expected 1")
if len(hits) == 1:
    q_keep[hits[0]] = q_keep[hits[0]].replace(OLD_P, NEW_P)

q_keep_txt = "".join(q_keep)
q_moved_txt = "".join(q_moved)
print(f"  {len(q)} lines / {kb(''.join(q)):.1f}KB -> {len(q_keep)} kept / "
      f"{kb(q_keep_txt):.1f}KB, {len(q_moved)} moved "
      f"({kb(q_moved_txt):.1f}KB), 1 pointer repaired")
live_blocks = sum(1 for l in q_keep if l.startswith("- [ ] **CLOSED c3"))
print(f"  live cycle blocks after cut: {live_blocks} (floor 5; this cycle's own "
      f"block makes it {live_blocks + 1})")
check(live_blocks == 4, f"expected 4 live blocks after cut, got {live_blocks}")

# ------------------------------------------- STANDING.md prior EXECUTED paragraph
st = read("notes/STANDING.md")
ex = [l for l in st if "**EXECUTED c3156" in l]
check(len(ex) == 1, f"found {len(ex)} EXECUTED c3156 paragraphs in STANDING.md, expected 1")
ex_txt = "".join(ex)

if problems:
    print(f"\nABORT: {len(problems)} assertion(s) failed, nothing written.")
    sys.exit(1)

if not WRITE:
    print("\nDRY RUN OK -- all assertions passed. Re-run with --write to apply.")
    sys.exit(0)

# ---------------------------------------------------------------- write
sa_before = "".join(read("state/STATUS_ARCHIVE.md"))
append("state/STATUS_ARCHIVE.md", "\n" + HDR.format(
    label="state/STATUS.md", why=f"had grown to {len(s)} lines / {kb(''.join(s)):.0f}KB, "
    "projected past the 256KB Read cap before check-doc-size's next 24c look; the live "
    "file keeps the newest 9 cycle blocks (c3179 down to c3170) so cycle 3180's own "
    "block lands it at exactly 10. Cycles <=3169 moved here.") + "\n" + s_moved_txt)
write("state/STATUS.md", s_keep_txt)

qa_before = "".join(read("tasks/queue_archive.md"))
append("tasks/queue_archive.md", "\n" + HDR.format(
    label="tasks/queue.md", why="RULE 6b rotation down to four live cycle blocks PLUS the "
    "RULE 4 tail pass `NEW c3172` asked for. Cut: CLOSED c3175/c3174/c3173/c3172/c3171/"
    "c3170/c3169/c3168; RETIRED as consumed: NEW c3172 (this cycle executed it), NEW c3164 "
    "and NEW c3163 (both target cycles ran and closed; every third of NEW c3160 (HIGH) is "
    "closed -- substack c3165, google-news c3164), NEW c3160 (MEDIUM) (closed as EXCLUDED "
    "at c3166) and its `- [x] DONE at c3166` marker.") + "\n" + q_moved_txt
    + "\n## Archived by cycle 3180 -- notes/STANDING.md's prior `EXECUTED c3156` paragraph "
      "of the doc-trim-cadence item, replaced in place by `EXECUTED c3180` "
      "(newest-execution-only shape).\n\n" + ex_txt)
write("tasks/queue.md", q_keep_txt)

# ---------------------------------------------------------------- verify
ok = True
sa_after = "".join(read("state/STATUS_ARCHIVE.md"))
qa_after = "".join(read("tasks/queue_archive.md"))
s_after = "".join(read("state/STATUS.md"))
q_after = "".join(read("tasks/queue.md"))

for name, moved, arch_before, arch_after, live_after, keep_txt in [
    ("STATUS.md", s_moved, sa_before, sa_after, s_after, s_keep_txt),
    ("queue.md", q_moved, qa_before, qa_after, q_after, q_keep_txt),
]:
    if "".join(moved) not in arch_after:
        print(f"  FAIL {name}: moved text not verbatim in archive"); ok = False
    if arch_before not in arch_after:
        print(f"  FAIL {name}: pre-existing archive altered"); ok = False
    missing = [l for l in moved if l.strip() and l not in arch_after]
    if missing:
        print(f"  FAIL {name}: {len(missing)} moved lines missing from archive"); ok = False
    if live_after != keep_txt:
        print(f"  FAIL {name}: live file != computed keep half"); ok = False
    print(f"  {name}: OK lossless -- live {kb(live_after):.1f}KB, "
          f"archive {kb(arch_before):.0f}KB -> {kb(arch_after):.0f}KB")

if ex_txt not in qa_after:
    print("  FAIL: STANDING.md EXECUTED c3156 paragraph not in queue_archive"); ok = False
else:
    print("  STANDING.md EXECUTED c3156: OK archived verbatim")

print("\nWROTE." if ok else "\nWROTE WITH FAILURES -- investigate before committing.")
sys.exit(0 if ok else 1)
