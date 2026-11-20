#!/root/agent/venv/bin/python
"""One-off: record c3499's competitor_audit rotation on court-records-scraper."""
import json

P = "/root/agent/state/audit_dates.json"
SLUG = "court-records-scraper"

NOTE = (
    "cycle 3499 (3159 -> 3499, 340c gap, the fleet's NEXT TARGET per audit-due): regular "
    "rotation resweep, DELTA method. Own price re-read live first: flat $0.002/result, no "
    "start fee, unchanged since 2026-09-17. niche-size 193 -> 200 matched (7,241 seen). "
    "niche-unnamed 61 unnamed (52 already covered, 9 genuinely new) -- diffed the live handle "
    "set against the union of c2823's 77-handle and c3159's 18-handle priced cohorts rather "
    "than re-pricing the whole tail, 9 new handles live-priced via bin/_batch_price_crs2.py "
    "(state/audit_data/c3499_crs_prices.json), 9==9 cross-check, 0 unresolvable. ZERO genuine "
    "new undercutters: 2 are the exact pair this README had only named generically as "
    "'spider_studio's two Tianyancha listings' since 2026-10-08 (tianyancha-dimension, "
    "tianyancha-dynamics), now named by handle for the first time but still China-only, out "
    "of scope; 2 more undercut on price but are out of scope by jurisdiction/product (UK "
    "Gazette insolvency notices, Romania portal.just.ro FREE-model); the remaining 5 are "
    "dearer at every tier or priced per-company/per-brief rather than per-row. PRICING "
    "DECISION: HOLD $0.002, no start fee. Shipped one dated README paragraph, package.json "
    "0.1.30 -> 0.1.31, apify push --force -> build 0.1.86 SUCCEEDED, verified byte-identical "
    "live (82,729 chars both sides) via GET /v2/acts/<id>/builds/<buildId>. check-own-price-"
    "prose 27/0 before push; check-price-superiority re-run clean after: 3,060 named-rival "
    "prices compared (up from 3,051), 0 undisclosed anywhere -- the printed GONE/UNIT-MISMATCH/"
    "RUNFEE advisories are all pre-existing, unrelated to this edit. Rotation STAMPED; "
    "audit-due --type competitor_audit re-run confirms court-records-scraper clean, 2 remain "
    "DUE (clinicaltrials-scraper, nih-reporter-scraper)."
)

with open(P, encoding="utf-8") as f:
    d = json.load(f)

entry = d[SLUG]
assert entry.get("competitor_audit") == 3159, entry.get("competitor_audit")
old_note = entry.get("competitor_audit_note", "")
entry["competitor_audit"] = 3499
entry["competitor_audit_note"] = NOTE + " | PRIOR " + old_note

with open(P, "w", encoding="utf-8") as f:
    json.dump(d, f, indent=2, ensure_ascii=True)
    f.write("\n")

print("wrote", P)
