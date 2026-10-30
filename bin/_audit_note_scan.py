#!/root/agent/venv/bin/python
"""Regression check for `bin/audit-due`'s note parsing (cycle 2472). Read-only.

Imports the LIVE `bin/audit-due` so it can never drift from the tool it checks, and
reports the two defects cycle 2472 closed:

  (1) segments scored CLEAN only because of a bare `0 drift` -- which is what every
      note writes for the `check-registry-fields` GUARD result, not an audit outcome.
      Expected: 0.
  (2) segments that still hold MORE THAN ONE report header, i.e. two concatenated
      reports that `note_segments()` failed to split, which lets an OLD report's
      wording decide the CURRENT clean_streak. Expected: 6, and all 6 are genuine
      mid-sentence citations ("fixed ... at cycle 826 (RUN_SUMMARY ...)"), not
      missing separators -- see the KNOWN_CITATIONS allowlist below. Anything NOT on
      that list is a new separator convention this parser does not know about yet.

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
NON_DRIFT_CLEAN = re.compile(r"clean (no-op|resweep|negative)|0 unnamed|"
                             r"0 new undercutter|0 undercutters|no undercutter", re.I)
# (Actor, note key) pairs whose surviving multi-header segment was hand-read at
# cycle 2472 and confirmed to be a mid-sentence CITATION, not a missing separator.
KNOWN_CITATIONS = {
    ("app-store-reviews-scraper", "note"),
    ("federal-register-scraper", "note"),
    ("nih-reporter-scraper", "note"),
    ("nih-reporter-scraper", "watch_subset_audit_note"),
    ("substack-scraper", "note"),
    ("trademark-search-scraper", "count_audit_note"),
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
