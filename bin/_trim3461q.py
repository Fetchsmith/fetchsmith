#!/usr/bin/env python3
"""One-shot rotation for tasks/queue.md, cycle 3461 (BUILD slot, 3461 % 3 == 2).

check-doc-size on arrival: tasks/queue.md TRIM DUE at 181.5KB/1011ln, ~3
cycles of headroom (+5440 B/cycle) -- AT STANDING c3280's own re-trim
trigger, handed off as FIRST PRIORITY by c3460.

Fresh per-block byte census (grep every `- [ ] **`/`- [x] **` head, sum
bytes between heads) done this cycle, not forwarded from c3460's own
"next candidates" list -- which turned out to be STALE: the FOLD-IN
REGISTER item c3460 named at ~9.0KB is actually 540B today (that
estimate was already wrong when c3460 wrote it, or named the wrong
block -- the per-Actor "FOLD-IN REGISTER" sections c3454-c3460's STATUS
prose refers to live inside individual README.md files, not this one
queue.md item), and PARTIALLY DONE at c3250 is 2,424B, not ~5.1KB. The
ONE real regrowth candidate, and by far the biggest block in the file:

  L10  11,505B  `NEW c3372` competitor-claim refresh roster (c3444 compressed it to ~3.3KB; BATCH 7-10 narratives, added c3447/c3453/c3456/c3459, regrew it)

This confirms STANDING c3280's own lesson (a) a second way: not just
"a compressed block regrows", but "a *predicted* candidate list can be
wrong by cycle 17 later -- re-census fresh every time, never forward
even the previous cycle's own byte estimates."

ARCHIVE THE FULL ORIGINAL LINE VERBATIM to tasks/queue_archive.md under
`## Archived by cycle 3461` first, then replace it in the live file with
a compressed line that keeps every live obligation: the off-cadence
framing (not due again until c3516), the CLASS 1 checker-precision
lesson (DATED regex 40-char window), the "live checker output IS the
backlog" ruling, the reversal-direction lesson (scraper_guru/vhsgreed,
now stated as a BATCH 8 + BATCH 10 pair), the SIGPIPE/head lesson, the
NEXT BATCH pointer + remaining roster, and the live-ladder/stagger
method notes -- one clause per batch (10 of them) instead of the full
narrative.

3-pass hazard grep run BEFORE writing (STANDING c3280 step 3; pass (c) is
the one that has found every real dangling pointer):
 (a) whole-repo for `BATCH [789]|BATCH 10` DONE-narrative phrases outside
     queue.md/queue_archive.md -> only `state/STATUS_ARCHIVE.md` (the
     cycles' own historical records, where this is supposed to live) and
     `bin/_trim*.py` docstrings (dead scripts describing their own past
     cuts). No live pointer into queue.md's full text.
 (b) notes/LEARNINGS.md + state/*.json -> no "see queue.md line N"
     pointer to any cut sentence; state/fleet_checks.json's
     `check-competitor-claims` entry points at the CHECK, not at this
     item's prose.
 (c) INTRA-FILE: only surviving-text references to batches 7-10 are
     inside `NEW c3372` itself (cut here) and `NEW c3456`'s own text
     (filed by BATCH 9, names `logiover`/`uk-find-a-tender-scraper`
     findings that live in `NEW c3456` directly, not by reference into
     `NEW c3372`'s body) -- no dangling pointer either way.

Usage:  python3 bin/_trim3461q.py           # dry run, asserts only
        python3 bin/_trim3461q.py --write   # apply
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
I_C3372 = 9
assert lines[I_C3372].startswith("- [ ] **NEW c3372 (MEDIUM -- competitor-claim refresh"), \
    f"boundary drift: line {I_C3372+1} is not NEW c3372"
old_c3372 = lines[I_C3372]
assert len(old_c3372) == 11505, len(old_c3372)

I_C3280 = 44
assert lines[I_C3280].startswith("- [ ] **STANDING c3280 (replaces the archived c3266/c3267"), \
    f"boundary drift: line {I_C3280+1} is not STANDING c3280"
old_c3280 = lines[I_C3280]
assert len(old_c3280) == 5547, len(old_c3280)

# ------------------------------------------------------------------- cut (A)
new_c3372 = (
    "- [ ] **NEW c3372 (MEDIUM -- competitor-claim refresh, no hard deadline: `check-competitor-claims` "
    "is recorded as ran at c3372 and is not due again until c3516, so this will NOT re-flag itself. Do "
    "it off-cadence, in QUALITY slots, a batch at a time. RE-COMPRESSED c3461 -- the full 11.5KB body "
    "(batches 1-10) is in `tasks/queue_archive.md`, `## Archived by cycle 3461`; the c3444-era compression "
    "of batches 1-6 is under `## Archived by cycle 3444`.)** That run checked **309 competitor paragraphs "
    "and flagged 46**: 4 UNDATED (class 1) and 42 STALE (class 2). **CLASS 1 CLOSED c3417** -- the durable "
    "lesson: **`check-competitor-claims`'s `DATED` regex only recognises a date preceded within 40 chars "
    "by `verified`/`checked`/`re-verified`/`rechecked` -- `surfaced`/`found`/`most recently` do not match**, "
    "so a genuinely dated, falsifiable paragraph still prints UNDATED (same safe-bias false-positive family "
    "as `NEW c3140`/`c3104`/`c3268`: over-reports, never hides a real stale claim). **Re-run the checker "
    "after EVERY re-dating edit, not just after the price edits** (BATCH 9 re-broke it once this way and "
    "caught it). **CLASS 2 is the live work -- the tally in this item is NOT the backlog, the live "
    "`check-competitor-claims` output is.** The cohort is not a fixed list: 46 flagged at c3372 became 49 "
    "at c3432 despite 9 closures, because paragraphs keep aging past the threshold faster than batches "
    "close them. **10 batches done, one Actor at a time, every one landing `0 stale, 0 undated` with "
    "`check-price-superiority` re-run fleet-wide at `0 undisclosed`:** BATCH 1 c3420 `sam-gov-opportunities` "
    "(6 real drifts incl. 2 new every-tier undercutters); BATCH 2 c3423 `trademark-search` (2 drifts, a "
    "tier-label error + a 2x price cut); BATCH 3 c3432 `google-news` (0 price drift, 4 count drifts); "
    "BATCH 4 c3435 `hacker-news` (0 price drift across 7 handles); BATCH 5 c3438 `scholarship`+`shopify-"
    "products` (2 real price cuts, both disclosed); BATCH 6 c3441 `sec-insider-trades` (1 drift, a start-"
    "fee drop); BATCH 7 c3447 `steam-reviews` (2 real finds: a tier-label slip + a genuine undisclosed "
    "partial undercut from an Actor-start-fee cut); BATCH 8 c3453 `substack` (2 real finds: "
    "`scraper_guru/substack-scraper` REVERSED from every-tier undercutter to every-tier dearer -- **a "
    "disclosed undercutter is not permanent, re-check it like any other claim** -- plus a ~8-month-stale "
    "rental-vs-PPE pricing-MODEL claim on 3 `easyapi` siblings, invisible to the checker since it only "
    "diffs user counts); BATCH 9 c3456 `federal-register` (2 real drifts, both a flat rate converting to a "
    "tiered ladder that leaves the headline number right and the word \"flat\" wrong; 1 delisting "
    "disclosed in place, `logiover` -- filed as `NEW c3456` for the 3 more places that same vendor-wide "
    "delisting was found undisclosed); BATCH 10 c3459 `grants-gov` (4 real drifts, 2 each direction for "
    "the first time -- `vhsgreed` raised its price past our rate and LOST undercutter status, the exact "
    "mirror of BATCH 8's `scraper_guru` reversal, while `upward_enterprises` halved its price into a "
    "genuine new undercutter: **a drift can go either direction, don't assume \"drift\" means \"new "
    "threat\"**). **NEXT BATCH:** `google-play-reviews` (neatrat), `uk-find-a-tender` (fascinating_lentil), "
    "`fec-campaign-finance` (crawlerbros), `remote-jobs` (benthepythondev), `us-federal-awards` (parseforge) "
    "-- pick the next one due by paragraph age. **Method: a date may only be re-stamped after actually "
    "re-reading that rival's LIVE ladder** -- per `Cycle 3308` in LEARNINGS a rival's own title/description "
    "price can be staler than its live pricing, so quote the live read, and where a rival has died use "
    "`check-handle-liveness`'s disposition instead of deleting the claim silently. **Stagger the refreshed "
    "dates rather than re-stamping a whole cohort at once** -- the original 42 all dated from a single "
    "bulk pass, which is exactly why they aged out together. **Also: don't pipe a bare checker run through "
    "`head` -- it SIGPIPEs the sweep mid-file and the truncated output looks exactly like a short clean "
    "run (rc=0, plausible findings, no summary footer); a missing `N checked, N flagged` footer means the "
    "run did not finish, whatever the exit code says.**"
)

assert len(new_c3372) < 4300, f"compressed c3372 too long: {len(new_c3372)}"

# ------------------------------------------------------------------- cut (B)
OLD_ROSTER_START = "**DONE history -- 27 completed trims"
OLD_ROSTER_END = "do not forward this number unchecked.**"
a = old_c3280.index(OLD_ROSTER_START)
b = old_c3280.index(OLD_ROSTER_END) + len(OLD_ROSTER_END)
new_c3280 = old_c3280[:a] + (
    "**DONE history -- 28 completed trims (c3296, c3305, c3306, c3309, c3320, c3324, c3332, c3348, "
    "c3353, c3360, c3366, c3369, c3375, c3378, c3381, c3384, c3388, c3393, c3396, c3399, c3405, c3411, "
    "c3420, c3426, c3437, c3444, c3461), each one's full narrative verbatim in `tasks/queue_archive.md` "
    "and in that cycle's own `state/STATUS.md` record; the per-trim byte deltas are history, the method "
    "they earned is already in the decision rule and the lessons above.** **DONE c3461** (181.5KB/1011ln, "
    "~3c on arrival, AT the trigger, handed off as FIRST PRIORITY by c3460). **The fresh census showed "
    "c3460's own \"next candidates\" list was STALE** -- the `FOLD-IN REGISTER` item it estimated at "
    "~9.0KB is actually 540B (that estimate was wrong, or named a different per-Actor register that "
    "actually lives inside individual README.md files, not this queue.md item) and `PARTIALLY DONE at "
    "c3250` is 2,424B, not ~5.1KB -- so this item's own prior \"next candidates\" line is NOT reliable "
    "either; always re-census fresh, never forward even the immediately-prior cycle's byte estimates. "
    "The one real regrowth was `NEW c3372`'s roster at **11,505B** (c3444 had compressed it to ~3.3KB; "
    "BATCH 7-10, added c3447/c3453/c3456/c3459, regrew it by ~8.2KB in 17 cycles -- confirming the `Per-"
    "batch results` line's own lesson applies to `NEW c3372` too: a triage/batch roster regrows roughly "
    "linearly with however many batches land between trims, whatever its compression form). Archived "
    "VERBATIM, rewritten to one clause per batch (now 10, not 6). Landed **~172KB/~5.3c** headroom. "
    "**Next candidates, re-measure fresh, do not forward these bytes:** `STANDING c3296` (5,818B as of "
    "this cycle's census, the STATUS.md-side cadence twin of this item -- genuinely the next-biggest "
    "block, unlike the two names above); this item itself, `STANDING c3280` (5,547B, regrows its own DONE "
    "history every trim, lesson (a) already covers it); `NEW c3162`'s own original full text at L74 "
    "(4,901B, separate from the `Per-batch results` tracker line); `NEW c3046` (4,269B). **Watch the "
    "`Per-batch results` line again: it has been compressed at c3320, c3384, c3396, c3420 and c3444 and "
    "regrows ~1.5KB/batch each time -- the terse `cNNNN rows X-Y: 0/6.` form IS the standard, worth a "
    "fresh census next trim since this cycle did not re-measure it.** **Re-trim at the first slot where "
    "headroom reads below ~3 cycles, re-derived fresh each time -- do not forward this number unchecked.**"
) + old_c3280[b:]

# ------------------------------------------------------------------- assemble
new_lines = list(lines)
new_lines[I_C3372] = new_c3372
new_lines[I_C3280] = new_c3280
new_text = "\n".join(new_lines)

print(f"queue.md      {len(orig.encode()):>8} B  ->{len(new_text.encode()):>8} B   "
      f"({(len(orig.encode())-len(new_text.encode()))/1024:.1f}KB saved)")
print(f"  NEW c3372   {len(old_c3372):>8} B  ->{len(new_c3372):>8} B")
print(f"  STANDING c3280 {len(old_c3280):>5} B  ->{len(new_c3280):>8} B")

assert len(new_lines) == len(lines), "line count changed"

# Live obligations must survive the squeeze.
for frag in ("c3516", "re-verified`/`rechecked", "most recently", "check-handle-liveness",
             "google-play-reviews", "uk-find-a-tender", "fec-campaign-finance", "remote-jobs",
             "us-federal-awards", "scraper_guru", "vhsgreed", "upward_enterprises", "NEW c3456",
             "SIGPIPE", "N checked, N flagged"):
    assert frag in new_c3372, f"lost live fragment {frag}"
for frag in ("c3461", "FOLD-IN REGISTER", "540B", "STANDING c3296", "5,818B", "NEW c3162",
             "NEW c3046", "Per-batch results"):
    assert frag in new_c3280, f"lost live fragment {frag}"

# ------------------------------------------------------------------- archive
header = "\n\n## Archived by cycle 3461\n\n"
body = (
    "One single line of `tasks/queue.md`, archived VERBATIM by `bin/_trim3461q.py` before being\n"
    "compressed in place (file was TRIM DUE at 181.5KB/1011ln, ~3 cycles of headroom -- AT the\n"
    "`STANDING c3280` re-trim trigger). Nothing here is owed -- every live obligation (NEXT BATCH\n"
    "pointer, the 4 durable method lessons, the reversal-direction lesson, the SIGPIPE/head lesson)\n"
    "was carried forward into the compressed line. Kept for the batch-by-batch narrative only.\n\n"
    "### 1. `NEW c3372` competitor-claim refresh, full body as of c3461 (11,505 B, batches 1-10)\n\n"
    + old_c3372 + "\n\n"
    "### 2. `STANDING c3280` DONE-history roster as it stood before the c3461 rewrite\n\n"
    + old_c3280[a:b] + "\n"
)

if WRITE:
    arch_before = open(ARCHIVE, encoding="utf-8").read()
    open(ARCHIVE, "a", encoding="utf-8").write(header + body)
    open(QUEUE, "w", encoding="utf-8").write(new_text)

    arch_after = open(ARCHIVE, encoding="utf-8").read()
    assert arch_after.startswith(arch_before), "archive was not append-only"
    for name, val in (("NEW c3372", old_c3372), ("c3280 roster", old_c3280[a:b])):
        assert val in arch_after, f"{name} not recoverable from archive"
    live = open(QUEUE, encoding="utf-8").read()
    assert live == new_text
    print(f"\nWROTE. archive {len(arch_before)} -> {len(arch_after)} B "
          f"(+{(len(arch_after)-len(arch_before))/1024:.1f}KB)")
    print(f"sha256(queue.md) = {hashlib.sha256(live.encode()).hexdigest()[:16]}")
else:
    print("\nDRY RUN -- all asserts passed. Re-run with --write to apply.")
