#!/root/agent/venv/bin/python
"""Regression check for `bin/audit-due`'s note parsing (cycle 2472). Read-only.

Imports the LIVE `bin/audit-due` so it can never drift from the tool it checks, and
reports the two defects cycle 2472 closed:

  (1) segments scored CLEAN only because of a bare `0 drift` -- which is what every
      note writes for the `check-registry-fields` GUARD result, not an audit outcome.
      Expected: 0.
  (2) segments that still hold MORE THAN ONE report header, i.e. two concatenated
      reports that `note_segments()` failed to split, which lets an OLD report's
      wording decide the CURRENT clean_streak. Expected: 8 (6 at c2472; 10 at c2579,
      of which c2580 fixed 2 at the source and allowlisted 2), and all 8 are genuine
      mid-sentence citations ("fixed ... at cycle 826
      (RUN_SUMMARY ...)"), not missing separators -- see the KNOWN_CITATIONS
      allowlist below. Anything NOT on that list is a new separator convention this
      parser does not know about yet.

Run after touching REPORT_HEAD / SEP / CLEAN in bin/audit-due.
"""
import importlib.machinery, importlib.util, json, re, sys

STATE = "/root/agent/state/audit_dates.json"
_loader = importlib.machinery.SourceFileLoader("audit_due", "/root/agent/bin/audit-due")
_spec = importlib.util.spec_from_loader("audit_due", _loader)
ad = importlib.util.module_from_spec(_spec)
_loader.exec_module(ad)

HEAD = re.compile(r"\bcycle \d{3,4}\s*(?::|\()", re.I)
BARE_DRIFT = re.compile(r"\b(?:zero|0) drift\b", re.I)
# CLEAN alternatives that are NOT about drift -- if one of these is present the
# segment is legitimately clean and the bare `0 drift` next to it is irrelevant.
# cycle 2579: mirrors the enum_audit/unreachable_remedy/count_audit idiom added to
# audit-due's own CLEAN (see that file's c2579 comment) -- without this mirror,
# check (1) below misreads e.g. "CLEAN RE-CONFIRMATION, 0 drift" as scored clean
# ONLY by the bare drift phrase, when it is really scored by "re-confirmation" (a
# real audit verdict) with an unrelated bare-drift mention sitting next to it.
NON_DRIFT_CLEAN = re.compile(r"clean (no-op|resweep|negative|re-confirmation)|"
                             r"0 unnamed|0 new undercutter|0 undercutters|"
                             r"no undercutter|genuinely clean|result clean|"
                             r"closed clean|no defects? found|0 defects found", re.I)
# (Actor, note key) pairs whose surviving multi-header segment was hand-read at
# cycle 2472 and confirmed to be a mid-sentence CITATION, not a missing separator.
KNOWN_CITATIONS = {
    ("app-store-reviews-scraper", "note"),
    ("federal-register-scraper", "note"),
    ("nih-reporter-scraper", "note"),
    ("nih-reporter-scraper", "watch_subset_audit_note"),
    ("substack-scraper", "note"),
    ("trademark-search-scraper", "count_audit_note"),
    # cycle 2492: hand-read, same benign class. c2475 guessed the cause was the
    # note's "cycle 2473: BACKFILL, not a new sweep --" opener failing REPORT_HEAD;
    # that guess was WRONG. The opener matches fine and seg0 DOES split as its own
    # segment -- the second header is a mid-sentence citation of the cycle that did
    # the real work ("...but cycle 2303 (commit 3c98af03, ...) already ran a full
    # fresh niche-unnamed resweep here..."), which REPORT_HEAD must not split on.
    # No new separator convention exists here, so REPORT_HEAD stays untouched.
    ("us-federal-awards-scraper", "competitor_audit_note"),
    # cycle 2580: hand-read the remaining 4 UNKNOWNs c2579 left open. TWO were
    # genuine mid-sentence citations and are allowlisted here; the other two were
    # REAL separator failures and were fixed at the source instead of allowlisted
    # (see the c2580 blocks in bin/audit-due and this cycle's STATUS.md):
    #   * hacker-news-scraper/varied_test_note -- a 6th separator convention,
    #     `[prior note preserved below]`, which _BOUND's bracket arm required
    #     `preserved` to sit flush against the `]` to match. _BOUND widened.
    #   * us-federal-awards-scraper/enum_audit_note -- no separator convention at
    #     all, just a dropped sentence-ending period ("...regression run
    #     unaffected cycle 2514 (1520 -> 2514):"), which starved the `(?<=\.)\s+`
    #     boundary. Repaired the one missing character in state/audit_dates.json
    #     rather than loosening the boundary to bare whitespace -- that loosening
    #     would have split every "at cycle NNNN (" citation, including the two
    #     directly below.
    # eu-ted: "...already found CLEAN once by direct curl at cycle 1017 (TED
    # server-validates classification-cpv...)" -- one cycle-2515 report citing the
    # earlier cycle that first established the mechanism.
    ("eu-ted-tenders-scraper", "enum_audit_note"),
    # sec-insider-trades: "...was already substantively proven live under the
    # varied_test type at cycle 2218 (single- and multi-candidate cases...)" -- one
    # cycle-2497 report, and its trailing "No defects found, nothing shipped"
    # verdict is genuinely 2497's own, so the clean_streak of 1 here is correct.
    ("sec-insider-trades-scraper", "enum_audit_note"),
}


def main():
    d = json.load(open(STATE))
    bare, multi = [], []
    for slug, v in sorted(d.items()):
        if not isinstance(v, dict):
            continue
        for k, note in sorted(v.items()):
            if not k.endswith("note") or not note:
                continue
            for i, seg in enumerate(ad.note_segments(note)):
                if (ad.CLEAN.search(seg) and not ad.NOTCLEAN.search(seg)
                        and BARE_DRIFT.search(seg) and not NON_DRIFT_CLEAN.search(seg)
                        and not re.search(r"(?:zero|0) (?:real )?price drift", seg, re.I)):
                    bare.append((slug, k, i))
                if len(HEAD.findall(seg)) > 1:
                    multi.append((slug, k, i))

    print("=== (1) segments CLEAN only via a bare `0 drift` (expect 0) ===")
    for slug, k, i in bare:
        print(f"  FAIL {slug:34s} {k:28s} seg{i}")
    print(f"  {len(bare)} found")

    print("\n=== (2) segments still holding >1 report header ===")
    unknown = 0
    for slug, k, i in multi:
        tag = "known citation" if (slug, k) in KNOWN_CITATIONS else "UNKNOWN -- NEW SEPARATOR?"
        if (slug, k) not in KNOWN_CITATIONS:
            unknown += 1
        print(f"  {slug:34s} {k:28s} seg{i}  {tag}")
    print(f"  {len(multi)} found, {unknown} unexplained")
    return 1 if bare or unknown else 0


if __name__ == "__main__":
    sys.exit(main())
