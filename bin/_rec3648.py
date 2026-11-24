#!/usr/bin/env python3
"""One-off: record c3648's varied_test audit on clinicaltrials-scraper.

Clone of bin/_rec2898.py's shape. Writes varied_test=3648 plus a newest-first
`varied_test_note`, then the caller re-runs `bin/audit-due --type varied_test
--all` to confirm the rotation actually closed.
"""
import json, shutil

P = "/root/agent/state/audit_dates.json"
SLUG = "clinicaltrials-scraper"
NOTE = (
    "c3648: two filter claims re-verified, 0 drift, 0 defects. "
    "(a) README:70's FDAAA-violation COUNTS re-measured FREE upstream "
    "(countTotal=true, no paid run): aggFilters=violation:y = 11 registry-wide, "
    "+COMPLETED = 6, +TERMINATED = 5, +cond=cancer = 2 -- all four identical to the "
    "2026-11-15 figures, so the README numbers stand; only the verification dates were "
    "refreshed. (b) funderTypes filter<->output agreement tested with ONE capped paid run "
    "(bin/varied-test, maxResults:10): funderTypes:[INDIV] + overallStatus:[RECRUITING] "
    "returned exactly 8 rows, matching the upstream count of 8 for the same pair "
    "(561 INDIV studies registry-wide), and all 8 rows came back leadSponsorClass=INDIV "
    "AND overallStatus=RECRUITING. Design makes a PASS informative: a silently-ignored "
    "filter would have hit the 10-row cap with mixed classes instead of stopping at 8. "
    "Both measurements shipped into README (build 0.1.108, README-only push, verified "
    "live via the build's own actorDefinition.readme at 83,190 chars)."
)

d = json.load(open(P))
shutil.copy2(P, P + ".c3648.pre")
e = d[SLUG]
assert e.get("varied_test") == 3312, e.get("varied_test")
e["varied_test"] = 3648
old = e.get("varied_test_note", "")
e["varied_test_note"] = NOTE + ((" | " + old) if old else "")
json.dump(d, open(P, "w"), indent=2, sort_keys=True)
print("recorded varied_test=3648 for %s (was 3312)" % SLUG)
