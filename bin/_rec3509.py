#!/usr/bin/env python3
"""One-off stamp for cycle 3509's enum_audit rotation on remote-jobs-scraper."""
import json
R = "/root/agent"
p = R + "/state/audit_dates.json"
d = json.load(open(p))
e = d["remote-jobs-scraper"]
prior = e["enum_audit"]
e["enum_audit"] = 3509
e["enum_audit_note"] = (
    "cycle 3509 (3173 -> 3509, 336c gap, DUE): NOTE -- c3173's stamp only bumped the "
    "date, it never rewrote this note (left c2837's text in place verbatim); that is "
    "corrected here. bin/enum-screen said IDENTICAL (3 declared enum fields -- "
    "sources: 7 boards, resultOrder: balanced/newest, watchEvents: new/salaryAdded -- "
    "unchanged since base rev 2026-11-02 12:06, which is itself a schema-claims-prose "
    "commit, confirmed by `git log` on input_schema.json: no enum-touching commit since "
    "d6a3d4eb/2a1b15f7, both ancient). Live-reverified all 7 source endpoints reachable "
    "today (remotive/remoteok/jobicy/arbeitnow/workingnomads/himalayas/wwr all HTTP 200). "
    "MAIN WORK: closed the real gap c2542 and c2837 both parked and could not resolve -- "
    "a genuine end-to-end PLATFORM proof that watchEvents:[salaryAdded] actually fires "
    "and charges. Both predecessors only tried LOCAL emulation (`node src/main.js` with a "
    "hand-placed INPUT.json, then `apify run -p --input-file`) and hit the same local "
    "Actor.getInput() bug (returns schema defaults, ignores the supplied input) both "
    "times. This cycle sidestepped that bug entirely by using the REAL platform instead "
    "of local emulation: (1) found a live RemoteOK job genuinely carrying a salary "
    "(id 1137865, 'Senior Product Engineer' @ Arbor Education, $70k-80k) via a direct "
    "API read; (2) ran remote-jobs-scraper for real (bin/_kv_run.py) with tight filters "
    "matching only that one job and a fresh watchLabel -- a real $0 seeding run, "
    "confirmed via its own log line and the resulting KV record "
    "(seenIds:['job:arbor education|senior product engineer'], seenMeta:[1], i.e. "
    "hasSalary=true recorded correctly); (3) surgically flipped ONLY that one id's "
    "stored seenMeta from 1 (true) to 2 (false) via a direct GET+PUT on the actor's own "
    "named KV store (fetchsmith-remote-jobs-watch) through the Apify API -- the only "
    "field touched, asserted before and after; (4) re-ran the identical label+filters "
    "for real (bin/run-charged) against the still-salaried live job. RESULT: the run "
    "pushed exactly 1 row, chargedEventCounts settled at {'job': 1}, and the dataset row "
    "itself carries watchEvent:'salaryAdded', previousHasSalary:false -- the exact "
    "shape pushResult() (main.js:354-393) is supposed to produce when previous===false "
    "and hasSalary===true. This is now proven correct against a real buyer-shaped "
    "round trip, not just by code trace plus live field-presence (c2837's fallback). "
    "Test KV record deleted afterward so no synthetic label persists in the real named "
    "store. `resultOrder` unchanged (pure local sort, no live dependency, already "
    "code-verified). Cost: ~$0.0015 (1 charged 'job' event at FREE tier; the seed run "
    "charged nothing). No code/schema/README change needed -- the gap was a missing "
    "proof, not a defect; the implementation was already correct. "
    "\n\nPRIOR (c2837, left stale by c3173, preserved for history): " + e["enum_audit_note"]
)
json.dump(d, open(p, "w"), indent=2, sort_keys=True)
print("stamped enum_audit: %d -> 3509" % prior)
