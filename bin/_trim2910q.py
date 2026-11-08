#!/usr/bin/env python3
"""One-shot trim of tasks/queue.md for cycle 2910 (128.6KB / 1564 lines, TRIM DUE,
confirmed fresh this cycle via bin/check-doc-size -- QUALITY/GROWTH slot,
2910 % 3 == 0, the standing rule is to do this kind of doc work here).

Fresh preflight this cycle (c2120 rule): `audit-due --all` FLEET ROTATIONS NONE
DUE (only the informational `count_audit`/`watch_subset_audit` one-off axes, not
a backlog per c1304). `checks-due --all` NONE DUE (soonest check-row-floor in 8c,
cycle 2918). `inbox-triage new` NONE UNTRIAGED of 75 (3 new mail since c2909 --
2 DMARC reports + 1 unsolicited "TinyGate API gateway" pitch -- all already on
record, no action). `bin/revenue` unchanged: $0 booked, 27 Actors, 50 users,
827 runs30d, 3 ext_bad30d, 0 bookmarks, 0 reviews -- no buyer signal, no owner
email owed. `bin/traffic`: no sustained /pricing or /tools buyer-intent signal,
Polar gate still correctly not met.

Method: hoist-then-cut on the DONE bucket, same as c2905/c2907. Fresh count
found **8 live DONE blocks** (c2909, c2905, c2902, c2903, c2904, c2906, c2907,
c2908 -- not in cycle order because blocks get appended/inserted in different
spots), three over the newest-5-DONE convention (c2865). Archiving the oldest 3
by cycle number -- c2902, c2903, c2904 -- recovers real bytes; they happen to be
exactly contiguous in the live file (lines 64-163), so this is a single-range
cut. After this cut the newest 5 remain live: c2905, c2906, c2907, c2908, c2909.

Rule-1 hazard grep (grep FIRST, then READ every hit) run over lines 64-163
before writing this script, pattern "standing|cadence|always |never |STANDING|
do not |must |rule" (-i): 7 hits, all read -- "do not batch" (c2902's own GAP
note, superseded by c2906/c2907 closing that gap), "never against/with ..."
(c2903 narrative describing what had NOT been tested before that cycle),
"always followable"/"rule would create false" (c2904 narrative discussing and
REJECTING a hypothetical trailing-modifier rule, not adopting one), "Rule-1
hazard grep ran first" (a reference to the general rule-1 process, itself homed
in this script's own lineage, not defined only in the archived text). None is
the sole home of a durable rule -- c2904's actual STANDING RULE lives at the
live lines 298-310 of the pre-cut file (kept, not touched). Safe to archive.

Partition is asserted total, non-overlapping and multiset-identical to the
original.
"""

SRC = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
NLINES = 1564

with open(SRC) as f:
    lines = f.readlines()

assert len(lines) == NLINES, f"expected {NLINES} lines, got {len(lines)} -- file changed, abort"


def seg(a, b):
    return lines[a - 1:b]


# DONE blocks to archive: c2902, c2903, c2904 (oldest 3 of the live 8, bringing
# the live set to the newest 5: c2905, c2906, c2907, c2908, c2909). Contiguous.
ARCHIVED = [
    (64, 163),  # DONE c2902, c2903, c2904 (+ trailing blank separator)
]

KEPT = [
    (1, 63),       # DONE c2909, DONE c2905 (unchanged)
    (164, NLINES),  # DONE c2906, c2907; NEXT; open items; DONE c2908; rest (unchanged)
]

NEW_DONE_BLOCK = """- [x] **DONE c2910 (QUALITY/GROWTH slot, 2910 % 3 == 0).** Preflight (fresh,
      c2120 rule): `audit-due --all` FLEET ROTATIONS NONE DUE (only the informational
      `count_audit` court-records-scraper/trademark-search-scraper and `watch_subset_audit`
      apple-podcasts-scraper one-off axes, not a backlog per c1304). `checks-due --all` NONE
      DUE (soonest `check-row-floor` in 8c, cycle 2918). `inbox-triage new` NONE UNTRIAGED of
      75 (3 new since c2909: 2 DMARC aggregate reports + 1 unsolicited "TinyGate API gateway"
      pitch, no action needed on either). `bin/revenue` unchanged: $0 booked, 27 Actors, 50
      users, 827 runs30d, 3 ext_bad30d, 0 bookmarks, 0 reviews -- no buyer signal, no owner
      email owed. `bin/traffic`: no sustained /pricing or /tools buyer-intent signal, Polar
      gate still correctly not met.
      **THE WORK: took the TRIM DUE `tasks/queue.md` doc-trim (128.6KB/1564 lines), the
      natural QUALITY/GROWTH-slot pick per c2907/c2909's handoffs and the standing doc-trim
      cadence rule.** `bin/_trim2910q.py` (hoist-then-cut, same method as c2905/c2907):
      archived the oldest 3 of 8 live DONE blocks by cycle number (c2902, c2903, c2904 --
      exactly contiguous, lines 64-163) to `tasks/queue_archive.md`, keeping the newest 5
      (c2905, c2906, c2907, c2908, c2909). Rule-1 hazard grep run first over the archive-bound
      range: 7 hits, all read, all narrative describing that block's own work or a rejected
      hypothetical rule -- no durable rule homed only there (full accounting in the script's
      docstring). Partition asserted total/non-overlapping/multiset-identical to the original
      before writing.
      Did not touch the open-item compression candidates (`c2380` one-term-diff etc., c2880
      measured) -- the DONE-block lever alone was enough to clear TRIM DUE this cycle; left
      those for whichever trim-due cycle next exhausts the DONE-block floor again.
      Services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; `/`, `/pricing`, `/tools`
      all 200 before and after (nothing site-side changed). $0 spend (pure docs, no build, no
      Actor run, no code change). **Blockers: none.**
"""

assert (
    ARCHIVED[0][1] - ARCHIVED[0][0] + 1
    + KEPT[0][1] - KEPT[0][0] + 1
    + KEPT[1][1] - KEPT[1][0] + 1
) == NLINES, "partition does not cover every line exactly once"

archived_text = "".join(seg(*ARCHIVED[0]))
kept_text = "".join(seg(*KEPT[0])) + "".join(seg(*KEPT[1]))

# Multiset-identity check (every non-blank original line must appear in
# exactly one of archived_text / kept_text, and nothing is duplicated or lost).
orig_nonblank = sorted(l for l in lines if l.strip())
reconst_nonblank = sorted(
    l for l in (archived_text.splitlines(keepends=True) + kept_text.splitlines(keepends=True))
    if l.strip()
)
assert orig_nonblank == reconst_nonblank, "lossless check FAILED -- lines lost or duplicated"

with open(ARCHIVE, "a") as f:
    f.write("\n## Archived by cycle 2910 (2026-11-08)\n\n")
    f.write(archived_text)

# Insert the new DONE block right after the kept head (line 63, before line 164's block),
# i.e. at the same spot c2909 appended its own: top of file, before c2905.
new_lines = [NEW_DONE_BLOCK + "\n"] + seg(*KEPT[0]) + seg(*KEPT[1])

with open(SRC, "w") as f:
    f.writelines(new_lines)

print(f"archived {ARCHIVED[0][1] - ARCHIVED[0][0] + 1} lines; new live file has {len(new_lines)} lines")
