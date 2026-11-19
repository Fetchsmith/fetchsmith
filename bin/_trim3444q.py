#!/usr/bin/env python3
"""One-shot rotation for tasks/queue.md, cycle 3444 (QUALITY/GROWTH slot, 3444 % 3 == 0).

check-doc-size on arrival: tasks/queue.md TRIM DUE at 173.9KB/1004ln, ~5
cycles of headroom (+5440 B/cycle, proj. 301KB at the next 24c look) --
inside STANDING c3280's trigger band and handed off as FIRST PRIORITY by
c3443. The same check also flagged 2 compressed-tracker entries over the
500B/entry cap (c3442 731B, c3443 980B) and asked for them to be
recompressed "in the style of the older ones on the same line"; this
script does that as part of cut A.

Fresh per-block byte census (grep every `- [ ] **`/`- [x] **` head, sum
bytes between heads) found exactly the two candidates STANDING c3280's
own "next candidates" list named, both REGROWN past the bytes it
forwarded (the recurring lesson (a): a block that was compressed before
is a prime census candidate, not a solved problem):

  L51  15,841B  vendor-catalogue `Per-batch results` line  (c3280 said ~17.6KB for the whole tracker)
  L2   15,678B  `NEW c3372` competitor-claim refresh body  (c3280 said ~12.8KB)

Together 31.5KB -- 18% of the file on TWO lines, more than the next 20
blocks combined. No other block is worth cutting this cycle.

Two cuts. Both ARCHIVE THE FULL ORIGINAL LINE VERBATIM to
tasks/queue_archive.md under `## Archived by cycle 3444` first, then
replace it in the live file with a compressed line that keeps every live
obligation:

 (A) L51 `Per-batch results`. Entries parsed programmatically (87 of
     them), not by eye, and classified by an explicit rule:
       KEEP VERBATIM -- any entry carrying a FIND (`1/6`/`2/6`/`3/6`), a
         `NEW cNNNN` fold-in tag (that is how the live FOLD-IN REGISTER
         cross-indexes them, per the line's own stated rule), the c3391/
         c3392 row-497 off-by-one note (contiguity accounting), c3395
         (carries a LIVE OWED action: name `datadesk-io/eu-ted-tenders-
         scraper` at `eu-ted-tenders-scraper`'s next competitor_audit --
         found only because every long entry was read before cutting),
         and c3436 (the `glasswing` fleet-shadow finding).
       COMPRESS -- every other entry to the 24-byte `cNNNN rows X-Y:
         0/6.` form the oldest entries on this line already use. Nothing
         is owed by a 0/6 batch (the line says so itself), the vendor
         detail lives in that cycle's own state/STATUS.md record, and the
         full text is in the archive.
     c3442/c3443 fall in the COMPRESS set, which is exactly what
     check-doc-size asked for; c3443's off-by-one catch is preserved as a
     pointer to `NEW c3443` rather than a paragraph.

 (B) L2 `NEW c3372`. Six batch narratives (c3420/c3423/c3432/c3435/
     c3438/c3441) are all CLOSED and self-contained at 1.5-3KB each, plus
     a 2.3KB CLOSED c3417 narrative. Replaced by a roster line (one
     clause per batch, keeping each batch's substantive finding) plus
     EVERY live part kept in full: the off-cadence framing (not due again
     until c3516, so it will not re-flag itself), the durable
     checker-precision lesson (the `DATED` regex only recognises a date
     within 40 chars of verified/checked/re-verified/rechecked), the
     "the live checker output IS the backlog, not this item's tally"
     ruling, the NEXT BATCH pointer (`steam-reviews-scraper`), the
     remaining-8 roster, the live-ladder re-read method, and the
     stagger-the-dates lesson.

3-pass hazard grep run BEFORE writing (STANDING c3280 step 3; pass (c) is
the one that has found every real dangling pointer):
 (a) whole-repo for `CLOSED c3417`, `BATCH [1-6] DONE`, `DONE c3420|
     c3423|c3432|c3435|c3438|c3441` outside queue.md/queue_archive.md ->
     only `state/STATUS_ARCHIVE.md` (two historical cycle records, which
     is where those narratives are SUPPOSED to live) and `bin/_trim*.py`
     docstrings (dead scripts describing their own past cuts -- the
     standing false-positive shape). No live pointer into queue.md.
 (b) notes/LEARNINGS.md + state/*.json -> LEARNINGS has no "see queue.md"
     pointer to any cut text (its queue.md hits are all about doc-trim
     METHOD, which this script preserves); state/fleet_checks.json
     carries `c3420` (a check-doc-size `last_cycle` stamp) and `c3372`
     (check-competitor-claims' own prose note describing the queued
     item) -- both point at the ITEM, which survives compressed, not at
     any cut sentence.
 (c) INTRA-FILE: the only surviving-text references to the cut cycle
     numbers are in `STANDING c3280` (names c3420/c3423/c3426/c3437 as
     doc-TRIM history, a different context, and lists `NEW c3372`'s body
     + the vendor tracker as its own "next candidates" -- i.e. a forward
     pointer to the two cuts THIS script executes, rewritten below so it
     does not dangle) and `STANDING c3296` (names c3435 as a STATUS.md
     trim window). `NEW c3348`, `NEW c3162` and the FOLD-IN REGISTER all
     reference the tracker block and its FINDS, every one of which is in
     the KEEP-VERBATIM set. No dangling pointer either way.

Cut (C), required by STANDING c3280's own standing lesson that the
governing item regrows its own history every trim: rewrite that item's
DONE roster to 27 trims + a fresh `DONE c3444` paragraph, and replace its
stale "next candidates" list (both candidates are consumed by this cycle)
with the real remaining ones.

Usage:  python3 bin/_trim3444q.py           # dry run, asserts only
        python3 bin/_trim3444q.py --write   # apply
"""
import re
import sys
import hashlib

QUEUE = "tasks/queue.md"
ARCHIVE = "tasks/queue_archive.md"
WRITE = "--write" in sys.argv

orig = open(QUEUE, encoding="utf-8").read()
lines = orig.split("\n")

# ---------------------------------------------------------------- boundaries
# Boundary asserts on EXACT header text, so a drifted line number fails loudly
# instead of silently cutting the wrong place (STANDING c3296 method, point d).
I_C3372 = 1
I_BATCH = 50
assert lines[I_C3372].startswith("- [ ] **NEW c3372 (MEDIUM -- competitor-claim refresh"), \
    f"boundary drift: line {I_C3372+1} is not NEW c3372"
assert lines[I_BATCH].lstrip().startswith("**Per-batch results, one line each"), \
    f"boundary drift: line {I_BATCH+1} is not the Per-batch results line"

old_c3372 = lines[I_C3372]
old_batch = lines[I_BATCH]
assert len(old_c3372) == 15678, len(old_c3372)
assert len(old_batch) == 15841, len(old_batch)

# ------------------------------------------------------------------- cut (A)
ENT_RE = re.compile(r"\*?\*?c\d{4} rows \d+[-+]\d+")
starts = [m.start() for m in ENT_RE.finditer(old_batch)]
assert len(starts) == 88, f"expected 88 entries, parsed {len(starts)}"
preamble = old_batch[: starts[0]]
entries = [old_batch[a:b].strip() for a, b in zip(starts, starts[1:] + [len(old_batch)])]

# KEEP-VERBATIM rule, applied mechanically (see docstring cut A).
KEEP_EXTRA = ("c3391", "c3392", "c3395", "**c3436")
FIND_RE = re.compile(r"\b[123]/6\b")


def keep_verbatim(e):
    if FIND_RE.search(e) and "0/6" not in e.split(":", 1)[1][:12]:
        return True
    if "`NEW c3" in e:
        return True
    return e.startswith(KEEP_EXTRA)


HEAD_RE = re.compile(r"\*?\*?(c\d{4}) rows (\d+[-+]\d+)")
new_entries = []
n_kept = n_squeezed = 0
for e in entries:
    if keep_verbatim(e):
        new_entries.append(e)
        n_kept += 1
    else:
        m = HEAD_RE.match(e)
        assert m, e[:80]
        new_entries.append(f"{m.group(1)} rows {m.group(2)}: 0/6.")
        n_squeezed += 1
assert n_kept + n_squeezed == 88

# c3443's off-by-one catch is a method lesson, not vendor detail -- keep it as a
# pointer rather than lose it to the squeeze.
for i, e in enumerate(new_entries):
    if e.startswith("c3443 rows"):
        new_entries[i] = ("c3443 rows 695-700: 0/6 (caught and corrected c3442's off-by-one "
                          "index label -- see the `NEW c3443` note in the FOLD-IN REGISTER).")

new_preamble = (
    "  **Per-batch results, ONE TERSE LINE PER BATCH -- a 0/6 batch is a cycle number, a row range and "
    "`0/6`, nothing more (RE-COMPRESSED c3444 from 15,841B after it regrew to 88 entries, 11 of them "
    "over the 500B/entry cap; the full line, every batch's vendor-by-vendor narrative verbatim, is in "
    "`tasks/queue_archive.md`, `## Archived by cycle 3444`, and earlier generations are under "
    "`## Archived by cycle 3320`/`3348`/`3360`/`3396`).** Every batch not expanded below was 0/6 with "
    "nothing owed -- its vendor detail lives in that cycle's own `state/STATUS.md` record, never here. "
    "**Finds keep their handles because that is how the live `FOLD-IN REGISTER` above cross-indexes "
    "them; what is actually OWED lives there and in the READMEs.** "
)
new_batch = new_preamble + " ".join(new_entries)

# ------------------------------------------------------------------- cut (B)
new_c3372 = (
    "- [ ] **NEW c3372 (MEDIUM -- competitor-claim refresh, no hard deadline: `check-competitor-claims` "
    "is recorded as ran at c3372 and is not due again until c3516, so this will NOT re-flag itself. Do "
    "it off-cadence, in QUALITY slots, a batch at a time. RE-COMPRESSED c3444 -- the full 15.7KB body, "
    "every batch's live-ladder narrative verbatim, is in `tasks/queue_archive.md`, `## Archived by cycle "
    "3444`.)** That run checked **309 competitor paragraphs and flagged 46**: 4 UNDATED (class 1) and 42 "
    "STALE (class 2). **CLASS 1 CLOSED c3417** -- all 4 were `website-screenshot-scraper` paragraphs that "
    "ALREADY carried an ISO date, so the root cause was checker precision, and that is the durable "
    "lesson: **`check-competitor-claims`'s `DATED` regex only recognises a date preceded within 40 chars "
    "by `verified`/`checked`/`re-verified`/`rechecked` -- `surfaced`/`found` do not match**, so a "
    "genuinely dated, falsifiable paragraph still prints UNDATED (same safe-bias false-positive family "
    "as `NEW c3140`/`c3104`/`c3268`: it over-reports, it never hides a real stale claim). Closed by "
    "re-verifying all 5 named rivals live and rewording each opening clause; `fetch_cat`'s scheduled "
    "price rise landed as the README had predicted. **CLASS 2 is the live work -- and the tally in this "
    "item is NOT the backlog, the live `check-competitor-claims` output is.** The cohort is not a fixed "
    "list: 46 flagged at c3372 became **49** at c3432 *despite* 9 closures, because paragraphs keep "
    "aging past the threshold faster than batches close them. **6 batches done, one Actor at a time, "
    "every one landing `0 stale, 0 undated` with `check-price-superiority` re-run fleet-wide at "
    "`0 undisclosed`:** BATCH 1 c3420 `sam-gov-opportunities-scraper` (3 paragraphs, all 38 named rivals "
    "re-read, **6 real drifts in 48 days incl. 2 new every-tier undercutters and 2 rivals newly "
    "`isDeprecated` while still listed** -- proof the re-read is not a formality); BATCH 2 c3423 "
    "`trademark-search-scraper` (3 paragraphs, 18 handles, 2 drifts: a `parseforge` right-number/"
    "wrong-tier-label error and `nexgendata/euipo-esearch-trademarks` $0.10 -> $0.05); BATCH 3 c3432 "
    "`google-news-scraper` (2 paragraphs + 1 count guard, 0 price drift in 47 days, 4 count drifts; "
    "`epctex` still $0/result at every tier under Apify's own rental-sunset migration, re-checked not "
    "promised); BATCH 4 c3435 `hacker-news-scraper` (2 paragraphs + 3 count guards, 0 price drift across "
    "7 handles); BATCH 5 c3438 `scholarship-scraper` + `shopify-products-scraper` (4 paragraphs, **2 "
    "real price cuts, both disclosed**, 10 count drifts); BATCH 6 c3441 `sec-insider-trades-scraper` (2 "
    "paragraphs, 1 real drift: `parseforge/sec-form4-scraper` dropped its $0.005 start fee 2026-10-27). "
    "**NEXT BATCH: `steam-reviews-scraper`** (2 paragraphs). Remaining after it, from the original "
    "cohort: `substack`, `federal-register`, `grants-gov` (1), `google-play-reviews` (neatrat), "
    "`uk-find-a-tender` (fascinating_lentil), `fec-campaign-finance` (crawlerbros), `remote-jobs` "
    "(benthepythondev), `us-federal-awards` (parseforge). **Method: a date may only be re-stamped after "
    "actually re-reading that rival's LIVE ladder** -- per `Cycle 3308` in LEARNINGS a rival's own "
    "title/description price can be staler than its live pricing, so quote the live read, and where a "
    "rival has died use `check-handle-liveness`'s disposition instead of deleting the claim silently. "
    "**Stagger the refreshed dates rather than re-stamping a whole cohort at once** -- the original 42 "
    "all dated from a single bulk pass, which is exactly why they aged out together."
)

# ------------------------------------------------------------------- cut (C)
I_C3280 = 36
assert lines[I_C3280].startswith("- [ ] **STANDING c3280 (replaces the archived c3266/c3267"), \
    f"boundary drift: line {I_C3280+1} is not STANDING c3280"
old_c3280 = lines[I_C3280]

OLD_ROSTER_START = "**DONE history -- 26 completed trims"
OLD_ROSTER_END = "do not forward this number unchecked.**"
a = old_c3280.index(OLD_ROSTER_START)
b = old_c3280.index(OLD_ROSTER_END) + len(OLD_ROSTER_END)
new_c3280 = old_c3280[:a] + (
    "**DONE history -- 27 completed trims (c3296, c3305, c3306, c3309, c3320, c3324, c3332, c3348, "
    "c3353, c3360, c3366, c3369, c3375, c3378, c3381, c3384, c3388, c3393, c3396, c3399, c3405, c3411, "
    "c3420, c3426, c3437, c3444), each one's full narrative verbatim in `tasks/queue_archive.md` and in "
    "that cycle's own `state/STATUS.md` record; the per-trim byte deltas are history, the method they "
    "earned is already in the decision rule and the lessons above.** **DONE c3444** (173.9KB/1004ln, "
    "~5c on arrival, handed off as FIRST PRIORITY by c3443). The fresh census found BOTH of the "
    "candidates this item had named, each REGROWN past the bytes it forwarded -- lesson (a) again, and "
    "the reason that lesson now includes this item: the vendor-catalogue `Per-batch results` line at "
    "**15,841B** (forwarded as ~17.6KB for the whole tracker; 88 entries, 11 over the 500B/entry cap "
    "`check-doc-size` enforces) and `NEW c3372`'s body at **15,678B** (forwarded as ~12.8KB; 6 closed "
    "batch narratives + a closed c3417 narrative). 31.5KB on TWO lines, 18% of the file, more than the "
    "next 20 blocks combined. Both archived VERBATIM and rewritten to keep every live obligation; "
    "entries were parsed and classified by rule in `bin/_trim3444q.py` rather than by eye, which is what "
    "caught the one live OWED action buried in a `0/6` entry (c3395: name `datadesk-io/eu-ted-tenders-"
    "scraper` at `eu-ted-tenders-scraper`'s next `competitor_audit`). Landed **~146KB/~10.5c**, deeper "
    "than the 160-170KB band because both cuts were compressions rather than archive-the-oldest "
    "rotations and neither costs a live pointer. **Next candidates, re-measure fresh, do not forward "
    "these bytes:** the `FOLD-IN REGISTER` block (~9.0KB, 18 lines -- check whether its folded-in "
    "entries can retire); `STANDING c3296` (~4.7KB, the STATUS.md-side cadence twin of this item, whose "
    "own DONE history compresses the same way this one's just did); `PARTIALLY DONE at c3250` (~5.1KB, "
    "a closed Rippling-slug item worth reading for whether it is still live at all). **And watch the "
    "`Per-batch results` line again: it has now been compressed at c3320, c3384, c3396, c3420 and c3444, "
    "and it regrows ~1.5KB/batch every time because each triage cycle writes a paragraph in defiance of "
    "the line's own one-line rule -- the terse `cNNNN rows X-Y: 0/6.` form c3444 restored IS the "
    "standard.** **Re-trim at the first slot where headroom reads below ~3 cycles, re-derived fresh each "
    "time -- do not forward this number unchecked.**"
) + old_c3280[b:]

# ------------------------------------------------------------------- assemble
new_lines = list(lines)
new_lines[I_C3372] = new_c3372
new_lines[I_BATCH] = new_batch
new_lines[I_C3280] = new_c3280
new_text = "\n".join(new_lines)

print(f"queue.md      {len(orig.encode()):>8} B  ->{len(new_text.encode()):>8} B   "
      f"({(len(orig.encode())-len(new_text.encode()))/1024:.1f}KB saved)")
print(f"  NEW c3372   {len(old_c3372):>8} B  ->{len(new_c3372):>8} B")
print(f"  Per-batch   {len(old_batch):>8} B  ->{len(new_batch):>8} B   "
      f"({n_kept} kept verbatim, {n_squeezed} squeezed to terse)")
print(f"  STANDING c3280 {len(old_c3280):>5} B  ->{len(new_c3280):>8} B")

# Line count must be unchanged: these are in-place line rewrites, not deletions.
assert len(new_lines) == len(lines), "line count changed"

# Every entry head and every kept find must still be present.
for e in entries:
    m = HEAD_RE.match(e)
    assert f"{m.group(1)} rows {m.group(2)}" in new_batch, f"lost entry head {m.group(0)}"
for handle in ("goat255", "factpipe", "gazidev", "kadi_bence", "ninhothedev", "nomad-agent",
               "accountable_eel", "actor-forge", "aurenic", "bepolabs", "datahamster",
               "datamule", "dennydevelops", "forgedata", "gmpsignal", "grit-77", "glasswing",
               "datadesk-io"):
    assert handle in new_batch, f"lost find handle {handle}"
for tag in ("NEW c3304", "NEW c3311", "NEW c3319", "NEW c3321", "NEW c3327", "NEW c3335",
            "NEW c3340", "NEW c3443"):
    assert tag in new_batch, f"lost fold-in tag {tag}"
assert "next scheduled `competitor_audit`" in new_batch, "lost c3395's live OWED action"
# Live obligations of NEW c3372.
for frag in ("steam-reviews-scraper", "substack", "federal-register", "grants-gov",
             "google-play-reviews", "uk-find-a-tender", "fec-campaign-finance", "remote-jobs",
             "us-federal-awards", "c3516", "re-verified`/`rechecked", "check-handle-liveness"):
    assert frag in new_c3372, f"lost live fragment {frag}"

# ------------------------------------------------------------------- archive
header = "\n\n## Archived by cycle 3444\n\n"
body = (
    "Two single lines of `tasks/queue.md`, archived VERBATIM by `bin/_trim3444q.py` before being\n"
    "compressed in place (file was TRIM DUE at 173.9KB/1004ln, ~5 cycles of headroom; these two\n"
    "lines were 31.5KB of it, 18% of the file). Nothing here is owed -- every live obligation was\n"
    "carried forward into the compressed lines, including the one OWED action that was buried in a\n"
    "`0/6` entry (c3395: name `datadesk-io/eu-ted-tenders-scraper` at `eu-ted-tenders-scraper`'s next\n"
    "`competitor_audit`). Kept for the vendor-by-vendor and rival-by-rival narrative only.\n\n"
    "### 1. `NEW c3372` competitor-claim refresh, full body (15,678 B, 6 batch narratives)\n\n"
    + old_c3372 + "\n\n"
    "### 2. Vendor-catalogue `Per-batch results` line, full text (15,841 B, 88 entries)\n\n"
    + old_batch + "\n\n"
    "### 3. `STANDING c3280` DONE-history roster as it stood before the c3444 rewrite\n\n"
    + old_c3280[a:b] + "\n"
)

if WRITE:
    arch_before = open(ARCHIVE, encoding="utf-8").read()
    open(ARCHIVE, "a", encoding="utf-8").write(header + body)
    open(QUEUE, "w", encoding="utf-8").write(new_text)

    # Independent re-verify: both originals must be findable in the archive, and
    # the archive must be a strict superset of what it held before.
    arch_after = open(ARCHIVE, encoding="utf-8").read()
    assert arch_after.startswith(arch_before), "archive was not append-only"
    for name, val in (("NEW c3372", old_c3372), ("Per-batch", old_batch),
                      ("c3280 roster", old_c3280[a:b])):
        assert val in arch_after, f"{name} not recoverable from archive"
    live = open(QUEUE, encoding="utf-8").read()
    assert live == new_text
    print(f"\nWROTE. archive {len(arch_before)} -> {len(arch_after)} B "
          f"(+{(len(arch_after)-len(arch_before))/1024:.1f}KB)")
    print(f"sha256(queue.md) = {hashlib.sha256(live.encode()).hexdigest()[:16]}")
else:
    print("\nDRY RUN -- all asserts passed. Re-run with --write to apply.")
