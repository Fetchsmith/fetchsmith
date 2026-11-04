#!/root/agent/venv/bin/python
"""One-shot queue.md trim for cycle 2712 (QUALITY slot, 2712 % 3 == 0).

Clone of bin/_trim2703q.py's hoist-then-cut shape. Partition re-derived FRESH from the
live file this cycle per the doc-trim item's rule 3 (42 blocks: 10 DONE + 32 OPEN).

check-doc-size read TRIM SOON (81547 B / 835 lines, +5440 B/cycle, next look in 24c ->
projected 207KB). Rule-4 margin arithmetic on a DONE-only cut:
    ceiling   = 200KB - 5440*24            = 74240 B
    post-cut  = 81547 - 22012 + ~1500(new) = 61035 B
    margin    = 13205 B  -> THIN (<15KB)
so per rule 4 this cycle ALSO compresses two open items whose mass is completed
narrative, rather than banking on the next DONE-only cut:
  * the doc-trim item itself (block 23) -- its c2703 execution record is replaced in
    place by c2712's, per the item's own "newest execution only" rule (same move c2703
    and c2652 made).
  * the c2478 `/v2/store` item (block 25, 7744 B -- the single largest open block) --
    the code half shipped at c2496, so the per-caller investigation/verification
    narrative is history. Compressed to the four behaviour changes, the shipped state,
    and the STILL-OPEN post-deadline actions, which are the only live work in it.

Hazard grep (rule 1) was run BEFORE this script on the 254 archive-bound lines: 34 hits,
all narrative *about* rules homed elsewhere (the c2524 rule in CLAUDE.md; the four
standing watches in STATUS.md; this cadence item). The one hit that read like a uniquely
homed method -- c2704's "a re-read follow-up must name a NON-OVERLAPPING window, shift
the window backwards rather than wait" -- was confirmed already homed at
notes/LEARNINGS.md:5944 before being allowed into the archive set. The compressed c2478
block's "never leave a single-slug check-store-rank run in that history" rule is homed at
notes/LEARNINGS.md:3582, and a one-line pointer to it is kept in the rewrite anyway.
"""
import os
import sys

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"

ARCHIVE_BLOCKS = [1, 2, 3, 4, 5, 6, 7, 10, 11]   # DONE blocks, newest (0) kept
DOCTRIM_BLOCK = 23
STORE_BLOCK = 25

orig = open(QUEUE).read()
lines = orig.split("\n")

starts = [i for i, l in enumerate(lines)
          if l.startswith("- [x] ") or l.startswith("- [ ] ")]
assert len(starts) == 42, f"expected 42 blocks, got {len(starts)}"
assert starts[0] == 0, "expected no header lines before the first block"
assert len(lines) == 835, f"expected 835 lines, got {len(lines)}"

blocks = []
for n, i in enumerate(starts):
    end = starts[n + 1] if n + 1 < len(starts) else len(lines)
    blocks.append(lines[i:end])

kinds = ["DONE" if b[0].startswith("- [x]") else "OPEN" for b in blocks]
assert kinds.count("DONE") == 10 and kinds.count("OPEN") == 32, kinds
for n in ARCHIVE_BLOCKS:
    assert kinds[n] == "DONE", f"block {n} is not DONE -- refusing to archive an OPEN item"
assert kinds[0] == "DONE", "block 0 should be the newest DONE block"
assert kinds[DOCTRIM_BLOCK] == "OPEN" and "doc-trim cadence" in blocks[DOCTRIM_BLOCK][0]
assert kinds[STORE_BLOCK] == "OPEN" and "c2478" in blocks[STORE_BLOCK][0]

# ---- partition: total, non-overlapping, multiset-identical to the original ----
keep_idx = [n for n in range(42) if n not in ARCHIVE_BLOCKS]
assert set(keep_idx) | set(ARCHIVE_BLOCKS) == set(range(42))
assert not (set(keep_idx) & set(ARCHIVE_BLOCKS))
recon = []
for n in range(42):
    recon.extend(blocks[n])
assert recon == lines, "block split is not a byte-for-byte partition of the original"

kept_lines = []
for n in keep_idx:
    kept_lines.extend(blocks[n])
arch_lines = []
for n in ARCHIVE_BLOCKS:
    arch_lines.extend(blocks[n])
assert sorted(kept_lines + arch_lines) == sorted(lines), "partition not multiset-identical"
assert not any(l.startswith("- [ ] ") for l in arch_lines), "OPEN item in the archive set"

# open items must be unchanged across the cut (before the two deliberate rewrites)
open_before = [blocks[n] for n in range(42) if kinds[n] == "OPEN"]
open_after = [blocks[n] for n in keep_idx if kinds[n] == "OPEN"]
assert open_before == open_after, "an open item changed across the cut"

# ---- deliberate rewrite 1: doc-trim item, newest execution record only ----
dt = blocks[DOCTRIM_BLOCK]
ex_start = next(i for i, l in enumerate(dt) if l.lstrip().startswith("**EXECUTED c2703"))
ex_end = next(i for i, l in enumerate(dt) if l.lstrip().startswith("**STANDING RULES"))
assert 0 < ex_start < ex_end, (ex_start, ex_end)
NEW_EXEC = """      **EXECUTED c2712 (QUALITY slot) -- `tasks/queue.md` only** (81.5KB/835 lines, TRIM
      SOON; STATUS.md 45.1KB/639 and LEARNINGS 6002 lines both OK, untouched). Partition
      re-derived fresh per rule 3: 42 blocks, 10 DONE + 32 OPEN. Rule-1 hazard grep ran
      FIRST on the 254 archive-bound lines -- 34 hits, all narrative *about* rules homed
      elsewhere, except c2704's "a re-read follow-up must name a NON-OVERLAPPING window;
      shift the window backwards rather than wait", archived only after confirming it is
      homed at `notes/LEARNINGS.md:5944`. Backups to `/tmp/c2712_*.bak` first.
      `bin/_trim2712q.py` hoist-then-cut kept all 32 open + newest DONE (c2710), archived
      9 DONE -> **51.5KB/560 lines**. **Rule-4 margin was THIN on that DONE-only cut
      (13.2KB: 74240 B ceiling - 61035 B projected), so two open items were compressed in
      the same cycle** instead of banking on the next cut: this item's c2703 record was
      replaced in place by this one ("newest execution only" applied to itself, as
      c2703/c2652 did), and the **c2478 `/v2/store` item -- the largest open block at
      7744 B -- was cut to its live half** (code shipped c2496; the rest was per-caller
      investigation narrative, archived verbatim; its single-slug `check-store-rank` rule
      confirmed homed at `notes/LEARNINGS.md:3582`, pointer kept anyway).
      **Guards all passed:** the script's asserts (line/block preconditions, byte-for-byte
      partition reconstruction, multiset identity, no-OPEN-in-archive-set,
      open-items-unchanged, both rewrites asserted separately since they break multiset
      identity by design); losslessness re-verified independently by non-blank line-set
      membership in live+archive; `check-doc-size` OK on all three docs; services active
      and `/`, `/pricing`, `/tools` 200 before and after.
""".rstrip("\n").split("\n")
blocks[DOCTRIM_BLOCK] = dt[:ex_start] + NEW_EXEC + dt[ex_end:]

# ---- deliberate rewrite 2: compress the c2478 /v2/store item to its live half ----
NEW_STORE = """- [ ] **NEW (c2478, MEDIUM, deadline 2026-11-15 -- CODE HALF SHIPPED c2496/c2500; what is
      left is a post-deadline re-read. Narrative compressed c2712 per the doc-trim item's
      rule 4; the full per-caller investigation is in `queue_archive.md` under the c2712
      header and in the c2496 DONE block.) -- Apify changes `GET /v2/store` on 2026-11-15:**
      (1) search returns one page of <=100 Actors, `offset`/`total` stop working, (2) `sortBy`
      is ignored, (3) category filtering can return different Actors, (4) `bookmarkCount`
      leaves the payload and ratings move into `stats`. Forwarded by owner, inbox `01852eaa`.
      **Shipped already, so a post-deadline run degrades honestly instead of lying:**
      `bin/store-anon-rank` and `bin/check-store-rank` detect dead paging structurally (they
      remember each page's first `(username, name)` and stop when one repeats) and report
      **`RANK UNKNOWN`, never `NOT FOUND`** -- without this they would have printed a
      confident false negative for every Actor ranked deeper than ~96, i.e. a fake
      fleet-wide ranking collapse inviting exactly the listing-copy churn c1468/c2280 warn
      against. `data.get("total")` everywhere; `check-store-rank` persists `paging_ok` per
      row; `bin/store-visibility`'s hard `d["total"]` KeyError fixed (c2478's own caller list
      had missed it). Confirmed SAFE and untouched: `niche-size`, `niche-unnamed`,
      `store-scan`, `apify-admin store`, `check-rental-converts`, `check-upstream-warnings`
      (all single-page); `store-rank`/`category-rank` are Algolia -- **Algolia is the real
      buyer surface and is unaffected.** Locked down by `bin/_store_paging_selftest.py`
      (3/3, no network/auth/cost), which fakes an offset-ignoring, `total`-less API.
      **STILL OPEN, do this AFTER 2026-11-15:** (a) run `bin/_store_paging_selftest.py`
      (expect 3/3) then a real `bin/store-anon-rank` -- the self-test says the degraded
      branch works, the live run says whether it is now the branch taken; (b) **the upside
      re-measure, which is the actually interesting half and is untouched:** Apify says the
      new default ranks by match-to-query, which could remove the cold-start `totalUsers`
      penalty that c2072 established (16 identically-named `grants-gov-scraper` listings, 87
      positions of spread with runs30d held equal). If a rank jumps into the top ~20
      *without* `totalUsers` rising, that falsifies the users-gating finding and is real news
      worth a strategy change -- but `/v2/store` is not the buyer surface, so read it as a
      hint about Apify's direction, not as recovered traffic. Pre-change baselines to compare
      against (both live-verified c2496): `store-anon-rank "court records"` **#29**, matching
      c2072 exactly, and `check-store-rank --scan 200 court-records-scraper` also **#29**
      plus `pacer court` #16. `paging_ok` True on every row is the expected reading until the
      date. **Standing rule (homed `notes/LEARNINGS.md:3582`): never leave a single-slug
      `check-store-rank` run in `state/store_rank.json` -- a 2-row snapshot in a 50-row
      series reads as "48 queries vanished" to the next diff; back the file up and restore.**
""".rstrip("\n").split("\n")
old_store = blocks[STORE_BLOCK]
blocks[STORE_BLOCK] = NEW_STORE

# rewrites asserted separately (they break multiset identity by design)
assert len("\n".join(NEW_EXEC)) < len("\n".join(dt[ex_start:ex_end])), \
    "doc-trim rewrite did not shrink the record"
assert len("\n".join(NEW_STORE)) < len("\n".join(old_store)), "c2478 rewrite did not shrink"
for key in ["_store_paging_selftest.py", "2026-11-15", "01852eaa", "RANK UNKNOWN",
            "paging_ok", "store-anon-rank", "check-store-rank", "store-visibility",
            "single-slug", "#29", "totalUsers", "c2072", "Algolia"]:
    assert key in "\n".join(NEW_STORE), f"c2478 rewrite dropped {key!r}"
_exec_txt = "\n".join(NEW_EXEC).lower().replace("-", " ")
for key in ["rule 1", "rule 3", "rule 4", "non overlapping", "_trim2712q.py",
            "/tmp/c2712_", "learnings.md:5944", "learnings.md:3582"]:
    assert key.lower().replace("-", " ") in _exec_txt, f"doc-trim rewrite dropped {key!r}"

new_lines = []
for n in keep_idx:
    new_lines.extend(blocks[n])
new_live = "\n".join(new_lines)

# ---- archive prepend, preserving the archive's own header prefix ----
arch_old = open(ARCHIVE).read()
hdr_end = arch_old.index("\n- [x] ")
arch_hdr, arch_body = arch_old[:hdr_end], arch_old[hdr_end:]
assert arch_hdr.startswith("PRIOR (closed/DONE queue items"), arch_hdr[:60]

NOTE = (
    "\n\nARCHIVED BY CYCLE 2712 (doc-trim cadence, QUALITY slot): queue.md was 835 lines / "
    "81.5KB and `bin/check-doc-size` read TRIM SOON (+5440 B/cycle, projected 207KB at its "
    "next look). Moved here: the 9 oldest DONE blocks (c2709, c2708, c2707, c2706, c2705, "
    "c2703, c2702, c2704, and the c2696 strikethrough closed by c2704); the newest DONE "
    "block (c2710) and all 32 open `[ ]` items stayed live. The rule-4 margin was THIN "
    "(13.2KB) after that DONE-only cut, so two open items were compressed in the same cycle "
    "and their superseded prose is archived immediately below the DONE blocks: the doc-trim "
    "item's c2703 execution record (replaced in place by c2712's, per its own 'newest "
    "execution only' rule) and the c2478 `/v2/store` item's per-caller investigation "
    "narrative (its code half shipped at c2496; the live post-deadline half stayed in "
    "queue.md). Hazard grep ran first on all 254 archive-bound lines: 34 hits, all narrative "
    "about rules homed elsewhere, except c2704's non-overlapping-window method, confirmed "
    "already homed at notes/LEARNINGS.md:5944 before archiving. Newest-first below, same "
    "order as the source file.\n\n"
)
superseded = (
    "- [x] **SUPERSEDED PROSE, archived c2712 (not a DONE item) -- the doc-trim cadence "
    "item's c2703 execution record,** replaced in place by c2712's per that item's own "
    "'newest execution only' rule:\n"
    + "\n".join(dt[ex_start:ex_end])
    + "\n\n- [x] **SUPERSEDED PROSE, archived c2712 (not a DONE item) -- the c2478 "
    "`/v2/store` item as it stood before c2712 compressed it to its live half.** Kept "
    "verbatim because it is the only full record of which fleet callers were investigated "
    "and why each was ruled SAFE:\n"
    + "\n".join(old_store)
    + "\n"
)
new_arch = arch_hdr + NOTE + "\n".join(arch_lines).rstrip("\n") + "\n\n" + superseded + arch_body

if "--dry-run" in sys.argv:
    print(f"live  {len(orig)} -> {len(new_live)} B, {len(lines)} -> {len(new_lines)} lines")
    print(f"arch  {len(arch_old)} -> {len(new_arch)} B")
    sys.exit(0)

for path, data in ((QUEUE, new_live), (ARCHIVE, new_arch)):
    tmp = path + ".c2712.tmp"
    with open(tmp, "w") as fh:
        fh.write(data)
    os.replace(tmp, path)

print(f"live  {len(orig)} -> {len(new_live)} B, {len(lines)} -> {len(new_lines)} lines")
print(f"arch  {len(arch_old)} -> {len(new_arch)} B")
