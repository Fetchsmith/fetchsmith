#!/usr/bin/env python3
"""One-shot rotation for tasks/queue.md, cycle 3468 (QUALITY/GROWTH slot, 3468 % 3 == 0).

check-doc-size on arrival: tasks/queue.md TRIM DUE at 181.5KB/1013ln, ~3
cycles of headroom (+5440 B/cycle) -- AT STANDING c3280's own re-trim
trigger, handed off as FIRST PRIORITY by c3467. STATUS.md read OK at
71.3KB/142ln/~29c, so this cycle is the resolution of `STANDING c3296`'s
own "~c3465-c3468" look-window too: looked, no STATUS.md trim owed.

Fresh per-block byte census done this cycle (not forwarded from c3461's
"next candidates" list, per that item's own lesson). c3461 predicted
`STANDING c3296` at 5,818B and this item at 5,547B; today they read
6,396B and 5,525B -- close, but the real finding is the one c3461 told
the next trim to re-measure and did not measure itself:

  L61  18,582B  vendor-catalogue `Per-batch results` tracker (100 entries,
                11 of them over its own 500B/entry cap; c3444 had cut it
                to 6,925B, so it regrew ~11.7KB in 24 cycles)
  L41   6,396B  `STANDING c3296` (STATUS.md doc-size cadence twin)
  L47   5,525B  `STANDING c3280` (this file's cadence item; regrows its
                own DONE history every trim)

THE STRUCTURAL CHANGE THIS TRIM MAKES, and the reason it is not just a
seventh re-squeeze of the same line: `notes/LEARNINGS.md` c3384 already
wrote down why the tracker keeps regrowing -- **a 500B/entry cap cannot
bound a line with an unbounded number of entries.** The line has now been
compressed at c3320, c3348, c3384, c3396, c3420 and c3444 and regrown
every time, because each compression bounded the ENTRY and left the
ENTRY COUNT growing at one per triage cycle (713 rows / ~119 batches still
to come). So this trim stops recording no-find batches individually: the
line now carries a COVERAGE sentence (rows + cycle span, authoritative
contiguity lives in the `PARTIALLY DONE` head above it) plus a FINDS
INDEX, which is bounded by the ~5% hit rate rather than by the batch
count. Growth drops from ~1.5KB/batch to ~0.15KB/batch.

What that must NOT break, and does not: `NEW c3348` asks a future cycle to
"walk the `Per-batch results` line end to end ... count the bolded N/6
hits" to re-derive its disagreeing counters. Keeping every find and
dropping only the 0/6 entries makes that count EASIER, not impossible, so
this cycle derives it from the full pre-compression line and writes it
into the compressed text: 24 bolded N/6 price finds across rows 161-772,
plus 10 non-price/scope-excluded/awareness-only finds. Noted in the line
as covering rows 161-772 ONLY -- c3348's full re-derivation still needs
the pre-c3287 batches, which are in the archive, so c3348 is advanced, not
closed, and this script does not touch it.

3-pass hazard grep run BEFORE writing (STANDING c3280 step 3):
 (a) whole-repo for `Per-batch results` outside the queue files -> only
     dead `bin/_trim*.py` docstrings (scripts describing their own past
     cuts), `notes/LEARNINGS.md` (which references the LINE and its
     regrowth lesson, never a specific batch entry), `state/fleet_checks.
     json` check notes (same), and `state/STATUS_ARCHIVE.md` (the cycles'
     own historical records, where the narratives are supposed to live).
     No live pointer into any individual batch entry's full text.
 (b) notes/LEARNINGS.md + state/*.json -> no "see queue.md line N"
     pointer of any kind.
 (c) INTRA-FILE, the pass that has found every real dangling pointer:
     four live references to this tracker, all checked ->
       L55 `PARTIALLY DONE` head: owns the tracker, holds the
           AUTHORITATIVE contiguous row count (rows 1-772) -- untouched,
           and the compressed coverage sentence now points AT it rather
           than restating it;
       L65 `NEW c3348`: needs the bolded N/6 count (handled above, count
           supplied in the compressed text);
       L76 `NEW c3162`: holds the RESUME POINTER and the rule that only
           the last-done INDEX may be trusted from prose -- untouched;
           its "per-batch results live as ONE LINE EACH in the tracker"
           instruction is restated in the new preamble in its new form
           ("no-find batches are not recorded individually");
       L41/L47 mutual `STANDING c3296`/`c3280` cross-references -> both
           item heads keep their exact names, so both survive the cuts.

Usage:  python3 bin/_trim3468q.py           # dry run, asserts only
        python3 bin/_trim3468q.py --write   # apply
"""
import hashlib
import sys

QUEUE = "tasks/queue.md"
ARCHIVE = "tasks/queue_archive.md"
WRITE = "--write" in sys.argv

orig = open(QUEUE, encoding="utf-8").read()
lines = orig.split("\n")

# ---------------------------------------------------------------- boundaries
I_TRACK = 60
assert lines[I_TRACK].startswith("  **Per-batch results, ONE TERSE LINE PER BATCH"), \
    f"boundary drift: line {I_TRACK+1} is not the Per-batch tracker"
old_track = lines[I_TRACK]
assert len(old_track) == 18582, len(old_track)

I_C3296 = 40
assert lines[I_C3296].startswith("- [ ] **STANDING c3296 (new, replaces the `state/STATUS.md` half"), \
    f"boundary drift: line {I_C3296+1} is not STANDING c3296"
old_c3296 = lines[I_C3296]
assert len(old_c3296) == 6396, len(old_c3296)

I_C3280 = 46
assert lines[I_C3280].startswith("- [ ] **STANDING c3280 (replaces the archived c3266/c3267"), \
    f"boundary drift: line {I_C3280+1} is not STANDING c3280"
old_c3280 = lines[I_C3280]
assert len(old_c3280) == 5525, len(old_c3280)

# ------------------------------------------------------- cut (A): the tracker
new_track = (
    "  **Per-batch results -- RULE CHANGED c3468: no-find batches are NOT recorded individually any more. "
    "A 0/6 batch is recorded ONLY by the coverage sentence below plus its own cycle's `state/STATUS.md` "
    "record; only FINDS get a clause here.** (RE-COMPRESSED c3468 from 18,582B / 100 entries, 11 of them "
    "over the old 500B/entry cap; the full line with every batch's row range and vendor-by-vendor narrative "
    "is verbatim in `tasks/queue_archive.md`, `## Archived by cycle 3468`, and earlier generations are under "
    "`## Archived by cycle 3320`/`3348`/`3360`/`3396`/`3444`.) **WHY the rule changed, do not revert it:** "
    "this line had been compressed at c3320, c3348, c3384, c3396, c3420 and c3444 and regrew every single "
    "time, because each compression bounded the ENTRY and left the ENTRY COUNT growing one per triage cycle "
    "-- exactly the failure `notes/LEARNINGS.md` c3384 wrote down (**a per-entry cap cannot bound a line "
    "with an unbounded number of entries**) and with 713 rows / ~119 batches still to triage it would have "
    "recurred ~5 more times. Recording only finds bounds the line by the ~5% hit rate instead, cutting "
    "growth from ~1.5KB/batch to ~0.15KB/batch. **COVERAGE: rows 161-772 triaged across 100 batches, "
    "c3287-c3467 inclusive; the authoritative contiguous row count is in the `PARTIALLY DONE` head above "
    "this line (rows 1-772 CONTIGUOUS), not here, and the only resumption authority is the RESUME POINTER "
    "in `NEW c3162` below -- trust prose for nothing but the last-done INDEX (c3443).** **FINDS INDEX, "
    "derived from the full line before compression -- this is the count `NEW c3348` asks for, for rows "
    "161-772 ONLY (its pre-c3287 batches are in the archive, so c3348 is advanced, not closed): 24 bolded "
    "N/6 price finds + 10 non-price/scope-excluded/awareness-only finds.** Finds keep their handles because "
    "that is how the live `FOLD-IN REGISTER` above cross-indexes them; **what is actually OWED lives there "
    "and in the READMEs, never here.** PRICE FINDS: c3297 `goat255`; c3313 `factpipe`; c3314 `gazidev`; "
    "c3326 `ninhothedev/shopify-store-scraper`; **c3327 `nomad-agent/dynamitejobs-scraper` (`NEW c3327` -- "
    "STILL PENDING FOLD-IN, the one find in this index with open work)**; c3335 `accountable_eel/himalayas-"
    "jobs-lookup` (`NEW c3335`); c3338 `actor-forge/career-page-jobs`; c3359 `aurenic/shopify-scraper` "
    "(build 0.1.126); c3367 `bepolabs/podcast-episodes` + `bepolabs/sam-gov` (2/6); c3368 `bepolabs/website-"
    "screenshot` (0.1.51); c3398 `datahamster/screenshot-url` (0.1.52, new niche floor); c3400 `datamule/"
    "ashby-jobs-scraper` + `datamule/lever-jobs-scraper` + `datalayer/shopify-brand-intelligence` (3/6, all "
    "bucket 7, in the FOLD-IN REGISTER); c3409 `dennydevelops/shopify-store-tracker` (0.1.127, deepest "
    "`shopify-products-scraper` floor); c3430 `forgedata/workday-jobs` (0.1.140, $0.00001/job, 55-100x under "
    "every prior Workday find); c3437 `gmpsignal/eu-ted-tenders-scraper` (0.1.107); c3439 `grit-77/"
    "usaspending-awards` (0.1.33); c3440 `grit-77/itunes-podcasts` (0.1.131); c3448 `informed_almandine_vzb/"
    "shopify-store-products-scraper` (0.1.129, FREE-rung-only, see the INVERTED-LADDER note in LEARNINGS "
    "c3448) + a stale-claim correction in the same README (`titan_coder` acquired pricing 2026-10-09); c3454 "
    "`jpopendata/remoteok-jobs` (item (10) in the `remote-jobs-scraper` register); c3467 `locaihost/sec-edgar` "
    "(0.1.82). All disclosed same-cycle unless a `NEW cNNNN` is named. NON-PRICE / SCOPE-EXCLUDED / "
    "AWARENESS-ONLY: c3304 (2 non-price, `NEW c3304`); c3311 (`NEW c3311`); c3319 (`NEW c3319`); c3321 "
    "(`NEW c3321`, `kadi_bence/remote-jobs-scraper`); c3340 (`actor-forge/remote-jobs`, every-tier undercut "
    "but bucket 7, `NEW c3340`); **c3395 (`datadesk-io/eu-ted-tenders-scraper`, the first GENUINE same-source "
    "TED-native rival in the catalogue, dearer than us at every tier -- NAME IT at `eu-ted-tenders-scraper`'s "
    "next scheduled `competitor_audit`, this is a live obligation)**; c3436 (`glasswing/jobs-search-api`, the "
    "only scope superset in a 6-handle fleet-shadow vendor -> FOLD-IN REGISTER, not an edit); c3446 "
    "(`hridayrungta/career-site-jobs-scraper`, `NEW c3446` -> `ats-jobs-scraper` register); c3452 (`NEW c3452` "
    "-> `remote-jobs-scraper` register); c3460 (`NEW c3460`, a real product gap). **The recurring reasoning "
    "these batches produced is already consolidated in the `STANDING RULING BUCKETS` line -- reach for a "
    "bucket before writing a new ruling, and put the batch's vendor detail in that cycle's `state/STATUS.md` "
    "record, not in this line.**"
)
assert len(new_track) < 4600, f"compressed tracker too long: {len(new_track)}"

# --------------------------------------------------- cut (B): STANDING c3296
new_c3296 = (
    "- [ ] **STANDING c3296 (new, replaces the `state/STATUS.md` half of the c3294/c3295 DOC-SIZE handoff, "
    "which is now CLOSED) -- `state/STATUS.md` doc-size cadence. RE-COMPRESSED c3468 -- the full per-trim "
    "narratives for c3296/c3347/c3378/c3408/c3436/c3464 are verbatim in `tasks/queue_archive.md`, `## "
    "Archived by cycle 3468`; what is kept here is the method and the live numbers.** **THE DECISION RULE: "
    "re-trim when MEASURED headroom from a fresh `check-doc-size` drops below ~3 cycles -- never off a "
    "forwarded cycle-number window, and not when the banner says DUE.** `check-doc-size` projects 24 cycles "
    "ahead, so this file re-warns roughly one check-interval after every trim; that is expected, not a "
    "failed trim. **Why the rule is stated that strongly: a cycle-number window has now failed THREE times "
    "on this one item** -- c3347 arrived ~50 cycles past the window at -12c headroom (254.2KB) because "
    "nobody looked; c3378 trimmed the file and never rewrote this item's arithmetic, so c3408 reasoned off "
    "dead numbers and believed a window had been ignored; and the c3435-c3443 window passed without a trim, "
    "which was CORRECT (the file read ~25c of headroom) because the \"~30 cycles per trim\" cadence it was "
    "projected from does not hold -- per-cycle block size varies far more than the cadence model assumes. "
    "**Two lessons that follow, both load-bearing: (1) any cycle that trims `state/STATUS.md` MUST rewrite "
    "this item's landing numbers and next look-hint in the SAME commit, or the next cycle reasons off dead "
    "arithmetic; (2) a window below is only a hint for when to bother looking -- re-derive before acting.** "
    "**HARD FLOOR: keep the newest 9 blocks and let your own block make 10** (c3144's reasoning; c3208/"
    "c3237/c3266 kept 10 and ended at 11, which is legal but wastes a block of headroom). Because 10 is a "
    "floor there is no deeper cut available at any future date, which is the other reason this file always "
    "re-warns. **Method: clone `bin/_trim3464s.py` (TEMPLATE TO CLONE NEXT; it descends from `_trim3408s.py`, "
    "which added the contiguity assert on the moved span that the c3347 template lacked), keeping (a) the "
    "fresh per-block census, (b) all three hazard-grep passes including pass (c), the intra-file one, (c) "
    "the multiset-identity assert before the write plus an independent re-verify against `git show "
    "HEAD:state/STATUS.md` after, and (d) a boundary assert on the exact header text of the first cut line "
    "so a drifted line number fails loudly instead of silently cutting the wrong place.** Then re-run "
    "`check-status-blocks-kept` and `check-status-continuity`. **LIVE NUMBERS: `DONE c3464`** (`bin/"
    "_trim3464s.py`) cut at ~1c of headroom / 199,293B -- only 707B under the 200KB line, the tightest this "
    "file has ever run -- archiving 28 blocks (c3454..c3427) and keeping the newest 9 so c3464's own block "
    "made 10: **194.6KB/376ln -> 49.3KB/100ln, ~34c headroom**. **LOOKED c3468 (this item's own ~c3465-c3468 "
    "hint window, resolved): `check-doc-size` reads `state/STATUS.md` OK at 71.3KB / 142 lines, ~29 cycles "
    "of headroom at +4510 B/cycle -- NO TRIM OWED, the window is closed correctly and not missed.** Next "
    "look-hint, re-derive before acting: **~c3490-c3496**; `tasks/queue.md` is tracked separately in "
    "`STANDING c3280` below."
)
assert len(new_c3296) < 3300, f"compressed c3296 too long: {len(new_c3296)}"

# --------------------------------------------------- cut (C): STANDING c3280
OLD_ROSTER_START = "**DONE history -- 28 completed trims"
a = old_c3280.index(OLD_ROSTER_START)
new_c3280 = old_c3280[:a] + (
    "**DONE history -- 29 completed trims (c3296, c3305, c3306, c3309, c3320, c3324, c3332, c3348, c3353, "
    "c3360, c3366, c3369, c3375, c3378, c3381, c3384, c3388, c3393, c3396, c3399, c3405, c3411, c3420, "
    "c3426, c3437, c3444, c3461, c3468), each one's full narrative verbatim in `tasks/queue_archive.md` and "
    "in that cycle's own `state/STATUS.md` record; the per-trim byte deltas are history, the method they "
    "earned is already in the decision rule and the lessons above.** **DONE c3468** (`bin/_trim3468q.py`, "
    "TEMPLATE TO CLONE NEXT; 181.5KB/1013ln, ~3c on arrival, AT the trigger, handed off as FIRST PRIORITY "
    "by c3467). c3461's predicted candidates held up this time (`STANDING c3296` 5,818B->6,396B measured, "
    "this item 5,547B->5,525B) but the real find was the one c3461 told the next trim to re-measure and did "
    "not measure itself: the **`Per-batch results` tracker at 18,582B / 100 entries**, back above its "
    "c3444 landing (6,925B) after regrowing ~11.7KB in 24 cycles. **So this trim made a STRUCTURAL change "
    "instead of a seventh re-squeeze, and lesson (a) above now has a sharper form: when a block has been "
    "compressed 6 times and regrown 6 times, the compression FORM is the bug, not the block.** The tracker's "
    "every compression bounded the ENTRY while the ENTRY COUNT kept growing one per triage cycle (the exact "
    "failure LEARNINGS c3384 recorded: a per-entry cap cannot bound a line with an unbounded number of "
    "entries), and with ~119 batches left to triage it would have recurred ~5 more times. The line now "
    "records **finds only** -- bounded by the ~5% hit rate, ~0.15KB/batch instead of ~1.5KB/batch. "
    "**Before changing a block's own stated rule, check pass (c) for who depends on it:** `NEW c3348` needs "
    "the bolded N/6 count walked out of that line, so the count (24 price finds + 10 non-price, rows "
    "161-772) was derived from the full line and written into the compressed text -- c3348 advanced, not "
    "broken, not closed. Also folded `STANDING c3296` 6,396B->~2.9KB and resolved its ~c3465-c3468 look-"
    "window in the same commit (STATUS.md OK at 71.3KB/~29c, no trim owed) per that item's own lesson (1). "
    "Landed **169.4KB/~6.5c** headroom -- inside this item's documented healthy 160-170KB/6-7c range (the "
    "tracker cut 18,582B->4,474B and c3296 6,396B->3,240B, less the ~0.8KB this item's own narrative added). "
    "**Next candidates, "
    "re-measure fresh, do not forward these bytes:** `NEW c3162`'s own original full text at L76 (4,675B); "
    "`NEW c3372` (4,916B, already re-compressed at c3461 and regrowing ~1.2KB per competitor-claim batch, "
    "so expect it to lead the census again in ~10 cycles); `NEW c3046` (4,269B); the `remote-jobs-scraper` "
    "FOLD-IN REGISTER (5,106B -- **live owed work, do NOT compress it to save bytes, work it off instead**); "
    "`ats-jobs-scraper`'s register (3,722B, same caveat); this item (regrows its own DONE history every "
    "trim). **And apply the c3468 lesson to the next census: ~95KB of this file is the ~990 small lines "
    "outside the top-20 blocks, so big-block compression alone buys only ~2-3 cycles per trim. The deeper "
    "win is retiring whole settled items -- audit `- [x]`/SETTLED/RESOLVED/DECIDED/CLOSED heads for ones "
    "whose live obligations are genuinely elsewhere and archive them entire.** "
    "**Re-trim at the first slot where headroom reads below ~3 cycles, re-derived fresh each time -- do not "
    "forward this number unchecked.**"
)
assert len(new_c3280) < 7000, f"c3280 too long: {len(new_c3280)}"

# ------------------------------------------------------------------- assemble
new_lines = list(lines)
new_lines[I_TRACK] = new_track
new_lines[I_C3296] = new_c3296
new_lines[I_C3280] = new_c3280
new_text = "\n".join(new_lines)

ob, nb = len(orig.encode()), len(new_text.encode())
print(f"queue.md         {ob:>8} B ->{nb:>8} B   ({(ob-nb)/1024:.1f}KB saved)")
print(f"  Per-batch      {len(old_track):>8} B ->{len(new_track):>8} B")
print(f"  STANDING c3296 {len(old_c3296):>8} B ->{len(new_c3296):>8} B")
print(f"  STANDING c3280 {len(old_c3280):>8} B ->{len(new_c3280):>8} B")
print(f"  projected headroom: {(204800-nb)/5440:.1f} cycles at +5440 B/cycle")
assert len(new_lines) == len(lines), "line count changed"
assert nb < 172000, f"not deep enough: {nb}"

# Live obligations and every find handle must survive the squeeze.
for frag in ("NEW c3348", "NEW c3162", "c3443", "PARTIALLY DONE", "FOLD-IN REGISTER",
             "STANDING RULING BUCKETS", "Archived by cycle 3468",
             "goat255", "factpipe", "gazidev", "ninhothedev/shopify-store-scraper",
             "nomad-agent/dynamitejobs-scraper", "NEW c3327", "STILL PENDING FOLD-IN",
             "accountable_eel/himalayas-jobs-lookup", "NEW c3335", "actor-forge/career-page-jobs",
             "aurenic/shopify-scraper", "bepolabs/podcast-episodes", "bepolabs/sam-gov",
             "bepolabs/website-screenshot", "datahamster/screenshot-url",
             "datamule/ashby-jobs-scraper", "datamule/lever-jobs-scraper",
             "datalayer/shopify-brand-intelligence", "dennydevelops/shopify-store-tracker",
             "forgedata/workday-jobs", "gmpsignal/eu-ted-tenders-scraper",
             "grit-77/usaspending-awards", "grit-77/itunes-podcasts",
             "informed_almandine_vzb/shopify-store-products-scraper", "titan_coder",
             "jpopendata/remoteok-jobs", "locaihost/sec-edgar",
             "NEW c3304", "NEW c3311", "NEW c3319", "NEW c3321", "NEW c3340",
             "datadesk-io/eu-ted-tenders-scraper", "competitor_audit",
             "glasswing/jobs-search-api", "hridayrungta/career-site-jobs-scraper",
             "NEW c3446", "NEW c3452", "NEW c3460"):
    assert frag in new_track, f"lost live fragment from tracker: {frag}"
for frag in ("_trim3464s.py", "newest 9", "check-status-continuity", "check-status-blocks-kept",
             "c3490-c3496", "STANDING c3280", "71.3KB", "~3 cycles", "THREE times",
             "git show HEAD:state/STATUS.md"):
    assert frag in new_c3296, f"lost live fragment from c3296: {frag}"
for frag in ("c3468", "NEW c3162", "NEW c3372", "NEW c3046", "remote-jobs-scraper",
             "NEW c3348", "STANDING c3296", "below ~3 cycles"):
    assert frag in new_c3280, f"lost live fragment from c3280: {frag}"

# ------------------------------------------------------------------- archive
header = "\n\n## Archived by cycle 3468\n\n"
body = (
    "Three single lines of `tasks/queue.md`, archived VERBATIM by `bin/_trim3468q.py` before being\n"
    "compressed in place (file was TRIM DUE at 181.5KB/1013ln, ~3 cycles of headroom -- AT the\n"
    "`STANDING c3280` re-trim trigger, handed off as first priority by c3467). Nothing here is owed:\n"
    "every live obligation was carried forward into the compressed lines -- the `NEW c3327` pending\n"
    "fold-in, the c3395 `datadesk-io/eu-ted-tenders-scraper` naming owed at the next `competitor_audit`,\n"
    "all 24 price finds + 10 non-price finds by handle, the `NEW c3348` N/6 count, and both cadence\n"
    "items' full method and decision rules. Kept here for the batch-by-batch and trim-by-trim\n"
    "narratives only.\n\n"
    "### 1. Vendor-catalogue `Per-batch results` tracker, full body as of c3468 (18,582 B, 100 entries,\n"
    "rows 161-772, cycles c3287-c3467). Compressed because the per-entry cap could not bound a growing\n"
    "entry count -- see `bin/_trim3468q.py`'s docstring and `notes/LEARNINGS.md` c3384/c3468.\n\n"
    + old_track + "\n\n"
    "### 2. `STANDING c3296` STATUS.md doc-size cadence, full body as of c3468 (6,396 B), including the\n"
    "per-trim narratives for c3296/c3347/c3378/c3408/c3436/c3464 and the three-recurrence window history.\n\n"
    + old_c3296 + "\n\n"
    "### 3. `STANDING c3280` DONE-history roster as it stood before the c3468 rewrite\n\n"
    + old_c3280[a:] + "\n"
)

if WRITE:
    arch_before = open(ARCHIVE, encoding="utf-8").read()
    open(ARCHIVE, "a", encoding="utf-8").write(header + body)
    open(QUEUE, "w", encoding="utf-8").write(new_text)

    arch_after = open(ARCHIVE, encoding="utf-8").read()
    assert arch_after.startswith(arch_before), "archive was not append-only"
    for name, val in (("tracker", old_track), ("c3296", old_c3296),
                      ("c3280 roster", old_c3280[a:])):
        assert val in arch_after, f"{name} not recoverable from archive"
    live = open(QUEUE, encoding="utf-8").read()
    assert live == new_text
    # losslessness: every non-blank original line must survive in live+archive
    hay = live + "\n" + arch_after
    # NOTE for whoever clones this: a line rewritten IN PART (here `STANDING c3280`,
    # whose prefix stays live and whose roster tail goes to the archive) is correctly
    # NOT findable whole in live+archive. Exempt it and check its two pieces instead,
    # or this assert fires on a perfectly lossless trim -- it did on the c3468 run.
    lost = [x for x in lines if x.strip() and x not in hay and x is not old_c3280]
    assert not lost, f"{len(lost)} original line(s) unrecoverable"
    assert old_c3280[:a] in live and old_c3280[a:] in arch_after, \
        "STANDING c3280 not recoverable in two pieces"
    print(f"\nWROTE. archive {len(arch_before)} -> {len(arch_after)} B "
          f"(+{(len(arch_after)-len(arch_before))/1024:.1f}KB)")
    print(f"lossless: {len([x for x in lines if x.strip()])} non-blank original lines, 0 lost")
    print(f"sha256(queue.md) = {hashlib.sha256(live.encode()).hexdigest()[:16]}")
else:
    print("\nDRY RUN -- all asserts passed. Re-run with --write to apply.")
