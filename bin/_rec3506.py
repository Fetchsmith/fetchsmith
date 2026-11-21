#!/usr/bin/env python3
"""One-off stamp for cycle 3506's enum_audit rotation on court-records-scraper."""
import json
R = "/root/agent"
p = R + "/state/audit_dates.json"
d = json.load(open(p))
e = d["court-records-scraper"]
prior = e["enum_audit"]
e["enum_audit"] = 3506
e["enum_audit_note"] = (
    "cycle 3506 (3170 -> 3506, 336c gap, DUE per audit-due --type enum_audit): "
    "bin/enum-screen said IDENTICAL again (3 declared enum fields -- recordType, "
    "opinionStatus, sortBy -- unchanged since c3170's base rev). Went past the surface "
    "diff per the c3170 standing practice and re-ran bin/vocab-screen on the courts "
    "vocabulary against CourtListener live: live /courts/ total 3363 == baked 3363 "
    "(unchanged since c3170 added the 4 missing in_use=false ids that cycle), live "
    "in_use=true 472 == baked 472, 5 spot-check ids (scotus/ca9/cand/nysd/cacb) all "
    "resolve with matching jurisdiction, negative control 404s. ALL CLEAN, 0 drift "
    "since c3170 -- genuinely clean this rotation, not just unexamined; no code/README "
    "change needed. All 3 declared enum values (recordType: both/opinions/dockets; "
    "opinionStatus: published/unpublished/any; sortBy: relevance/dateFiledDesc/"
    "dateFiledAsc) have each been live-exercised historically per varied_test cycles "
    "1298/1634/1970/2198/2227/2564/2902 -- no untested branch like c3505 found on "
    "sec-insider-trades-scraper. Cost $0 (both tools are free/local or free live API "
    "reads, no charged platform run). Prior note preserved below."
    "\n\nPRIOR: " + e["enum_audit_note"]
)
json.dump(d, open(p, "w"), indent=2, sort_keys=True)
print("stamped enum_audit: %d -> 3506" % prior)
