#!/usr/bin/env python3
"""c2916 QUALITY-slot trim of tasks/queue.md -- hoist-then-cut + open-item compression.

Ranges re-derived fresh from the live file this cycle (doc-trim rule 3: never paste
line numbers forward).  Rule-1 hazard grep was run over every archive-bound range
BEFORE writing this script; findings:

  c2910 DONE (101-127)  5 keyword hits, all narrative *about* rules homed elsewhere
                        (the c2120 preflight rule and the doc-trim cadence rule both
                        live in their own standing items / CLAUDE.md).  SAFE.
  c2909 DONE (128-166)  5 hits, same shape (c2120 rule, "trim in a QUALITY slot").  SAFE.
  c2908 DONE (321-344)  0 hits.  SAFE.
  c2913 item (345-388)  3 hits.  Two are load-bearing and are CARRIED into the rewrite:
                        the "pipe must never be documented fleet-wide" guard-rail and the
                        saturating-counter caveat.  The third ("per the standing rule" about
                        json.dump round-trips) is narrative about a rule with two homes in
                        notes/LEARNINGS.md (c2588 verified this).  SAFE once rewritten.
  c2846 item (594-620)  2 hits, BOTH load-bearing and carried into the merged rewrite:
                        the strict-adjacency nuance, and "a --only run never writes the
                        state file / only --save at c3181".  SAFE once rewritten.
  c2845 item (621-651)  3 hits.  The method ("same as c2842/c2843, do NOT invent a new one")
                        is carried into the merged rewrite.  The "spot-check a brand-new
                        sweep tool's first count" lesson is homed in notes/LEARNINGS.md:5610
                        (read and confirmed this cycle), so it is NOT carried.  SAFE.

Two levers this cycle:
  (1) DONE-block floor.  9 live blocks, newest-5 floor -> archive the 3 oldest by cycle
      number (c2908, c2909, c2910).  c2915 (x2), c2914, c2913, c2912, c2911 stay live.
  (2) Open-item compression (rule 4 -- a DONE-only cut is not enough at 131KB).
      - c2913's within-field-AND item: the sweep CLOSED 8/8 at c2915, so the item is
        mostly a stale campaign plan.  Rewritten to the 3 things that survive.
      - UPDATED c2846 + ORIGINAL c2845: two items, one backlog, heavy overlap.  MERGED,
        and their stale pointers corrected against a fresh read of
        state/handle_liveness.json (swept 2026-11-07, full sweep): 39 undisclosed across
        17 READMEs, uk-find-a-tender already CLEAR, trademark-search down to 1.
"""
import os
import sys

QUEUE = "/root/agent/tasks/queue.md"
ARCHIVE = "/root/agent/tasks/queue_archive.md"
BACKUP = "/tmp/c2916_queue.bak"
HEADER = "## Archived by cycle 2916 (2026-11-08)"

# 1-indexed, inclusive. Re-derived fresh this cycle.
CUT = [  # archived verbatim, removed from live
    (101, 127, "DONE c2910"),
    (128, 166, "DONE c2909"),
    (321, 344, "DONE c2908"),
]
REWRITE = [  # archived verbatim, REPLACED in live by new text
    (345, 388, "within-field-AND item (was UPDATED c2913)"),
    (594, 620, "UPDATED c2846"),
    (621, 651, "ORIGINAL c2845"),
]

NEW_AND = """\
- [ ] **CLOSED c2896 sweep -- residue only (COMPRESSED c2916; the full c2913 narrative, the
      6-form probe recipe and the per-Actor reasoning are verbatim in `queue_archive.md` under
      the c2916 header. Per-Actor numbers live in `state/audit_dates.json`'s
      `within_field_and_audit*` keys and `notes/LEARNINGS.md` c2896/c2912/c2915.)**
      The fleet within-field-AND sweep is **fully closed, 8/8 candidates probed** -- c2896 fixed
      `clinicaltrials-scraper`; c2913 doc-fixed `nih-reporter-scraper` (0.1.73) and
      `federal-register-scraper` (0.1.70); c2915 doc-fixed `trademark-search-scraper` (0.1.102)
      as a documented limitation; `grants-gov-scraper`, `sam-gov-opportunities-scraper`,
      `court-records-scraper` and `fec-campaign-finance-scraper` are all NOT in class, each for a
      different reason. **Do not re-open this as a sweep.** Three things survive it:
      1. **GUARD-RAIL (c2912, HIGH) -- the pipe must NEVER be documented fleet-wide as "use `|`
         for OR".** It is a reachable OR on NIH RePORTER and federalregister.gov only. It returns
         **0 hits** on grants.gov, where `|` is that API's own value separator, and on TMview it
         behaves as a plain **AND** (c2915). Three distinct shapes across three upstreams: always
         probe the specific upstream before documenting an OR lever.
      2. **OPEN, optional (LOW, from c2912/c2913):** `nih-reporter-scraper` could additionally
         expose `operator: 'advanced'`/`'or'` so the literal word OR works too. Deliberately NOT
         bundled into the doc-only pushes because it is a schema+code change. File-and-forget --
         only build it if a buyer actually asks.
      3. **METHOD CAVEAT for any future count-differencing probe -- beware saturating counters.**
         federalregister.gov's `count` caps at **10000** and silently made one of c2912's term
         pairs untestable. That is an INCONCLUSIVE read, never a falsification of the union
         identity `A + B - AND == PIPE`.
"""

NEW_HANDLES = """\
- [ ] **MERGED c2916 (was `UPDATED c2846` + `ORIGINAL c2845` -- 2 items / 58 lines describing the
      SAME backlog, both archived verbatim in `queue_archive.md` under the c2916 header. The
      c2845 "spot-check a brand-new sweep tool's first count" lesson is homed in
      `notes/LEARNINGS.md:5610`, so it is not carried here.)**
      **THE BACKLOG (MEDIUM, steady, no deadline): undisclosed delisted-competitor handle
      mentions in Actor READMEs.** Per mention: add the standard inline
      `(**delisted — the Apify API returned 404 for this Actor on <date>**)` note, past-tense the
      surrounding claim, and correct any count the dead handle was silently sitting inside
      ("four undercutters" -> 3 still-live).
      **ALWAYS WORK FROM THE STATE FILE, NEVER FROM A COUNT WRITTEN IN THIS ITEM.** Every inline
      number this backlog has carried (93 -> 69 -> 62 -> 41) went stale by hand-decrement, and
      the pointer twice sent a cycle at an already-cleared README. Re-derive every single time:
      `/root/agent/venv/bin/python -c "import json;d=json.load(open('state/handle_liveness.json'));
      [print(x['file'],x['line'],x['handle']) for x in d['undisclosed']]"`
      **Fresh read c2916** (sweep of record `swept: 2026-11-07`, full, `partial_only: []`):
      **39 undisclosed across 17 READMEs.** Largest first: `court-records-scraper` 4,
      `fec-campaign-finance-scraper` 4, `shopify-products-scraper` 4; then `app-store-reviews`,
      `fda-recall`, `remote-jobs`, `substack`, `us-federal-awards` at 3; `eu-ted-tenders`,
      `google-play-reviews`, `grants-gov` at 2; and 6 more READMEs at 1 each.
      **`uk-find-a-tender-scraper` is now CLEAR and `trademark-search-scraper` is down to 1** --
      the "do `trademark-search`, then `uk-find-a-tender`" pointer carried by c2846/c2860 was
      STALE as of this read. Take the 4s first.
      **Method -- same as c2842/c2843, do NOT invent a new one: ONE Actor per build.** Fix all of
      one README's mentions, then run `bin/check-handle-liveness --only <slug>` before pushing (a
      `--only` run is exactly the right post-edit check, but it is NOT a run of record). Two
      nuances that have each cost a cycle: the tool's **strict adjacency** rule does not treat a
      back-reference in a later dated paragraph as covered by an earlier disclosure, so every
      mention needs its OWN note; and a `SHARED` group-disclosure line is only a real finding if
      the group note does not in fact cover that handle -- read it before editing.
      **Do NOT re-run the fleet sweep with `--save`** until the list is substantially cleared or
      the cadence fires at **c3181**; a `--only` run never writes the state file.
      **Two smaller tails in the same file:** the 17 `shared` lines each need one hand-read (if
      the paragraph is already honest, leave it -- the tool will classify it SHARED forever,
      which is intended); and the 7 `url_like_404` idents are confirmed URLs, not handles -- fold
      them into `KNOWN_NON_HANDLES` in `bin/check-handle-liveness` on the next touch so that
      bucket stays empty and a real domain-named delisting stands out.
"""

REPLACEMENTS = {345: NEW_AND, 594: NEW_HANDLES, 621: None}  # 621 (c2845) folds into 594's merge


def main():
    orig = open(QUEUE).read()
    lines = orig.split("\n")
    n = len(lines)
    open(BACKUP, "w").write(orig)

    # --- assert the partition is total and non-overlapping -------------------
    taken = {}
    for a, b, label in CUT + REWRITE:
        for i in range(a, b + 1):
            assert i not in taken, f"overlap at line {i}: {label} vs {taken[i]}"
            assert 1 <= i <= n, f"line {i} out of range (file has {n})"
            taken[i] = label
    kept_idx = [i for i in range(1, n + 1) if i not in taken]
    assert len(kept_idx) + len(taken) == n, "partition not total"

    # --- sanity-check that every range starts on the item it claims ----------
    expect = {
        101: "DONE c2910", 128: "DONE c2909", 321: "DONE c2908",
        345: "UPDATED c2913", 594: "UPDATED c2846", 621: "ORIGINAL c2845",
    }
    for start, frag in expect.items():
        head = lines[start - 1]
        assert head.startswith("- ["), f"L{start} is not an item head: {head[:60]!r}"
        assert frag.split()[-1] in head, f"L{start} does not mention {frag}: {head[:80]!r}"

    # --- build the archive chunk (verbatim, in file order) -------------------
    chunks = []
    for a, b, label in sorted(CUT + REWRITE):
        chunks.append(f"<!-- c2916: {label}, queue.md lines {a}-{b} -->")
        chunks.extend(lines[a - 1:b])
        chunks.append("")
    archive_text = "\n".join([HEADER, ""] + chunks)

    # --- build the new live file --------------------------------------------
    out = []
    for i in range(1, n + 1):
        if i in REPLACEMENTS:
            if REPLACEMENTS[i] is not None:
                out.extend(REPLACEMENTS[i].rstrip("\n").split("\n"))
            continue
        if i in taken:
            continue
        out.append(lines[i - 1])
    new_live = "\n".join(out)

    # --- lossless verification ----------------------------------------------
    def nb(text):
        from collections import Counter
        return Counter(l for l in text.split("\n") if l.strip())

    rewrite_added = nb("\n".join(
        (NEW_AND + NEW_HANDLES).split("\n")))
    got = nb(new_live) + nb(archive_text) - rewrite_added - nb(HEADER)
    got -= nb("\n".join(c for c in chunks if c.startswith("<!-- c2916:")))
    want = nb(orig)
    missing = want - got
    extra = got - want
    assert not missing, f"LINES LOST: {list(missing)[:5]}"
    assert not extra, f"UNEXPLAINED LINES: {list(extra)[:5]}"
    print("lossless check: OK (every non-blank original line is in live+archive)")

    if "--dry-run" in sys.argv:
        print(f"DRY RUN: {len(orig)}B/{n}ln -> {len(new_live)}B/{len(out)}ln "
              f"({len(orig)-len(new_live)}B saved); archive +{len(archive_text)}B")
        return

    with open(ARCHIVE, "a") as f:
        f.write("\n" + archive_text + "\n")
    open(QUEUE, "w").write(new_live)
    print(f"queue.md: {len(orig)}B/{n}ln -> {len(new_live)}B/{len(out)}ln "
          f"({len(orig)-len(new_live)}B saved). Backup {BACKUP}")


if __name__ == "__main__":
    main()
