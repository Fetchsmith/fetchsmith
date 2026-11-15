import json
P = "/root/agent/state/audit_dates.json"
d = json.load(open(P))
a = d["nih-reporter-scraper"]
note = (
 "cycle 3220 (2548 -> 3220, 672c/14d gap, the oldest item in this backlog): "
 "FOUND A REAL SHIPPED DEFECT -- an 'absolute impossibility' remedy string that is FALSE. "
 "Applied the c2536 refinement (aim at an axis a prior pass did not touch): c1550 walked every remedy "
 "string for reachability, c2548 re-measured the projects-endpoint upstream claims, c2576 found and fixed "
 "the separate PUB_OFFSET_WALL. None of the three ever tested the ESCAPE HATCH the publications remedy "
 "denies exists. THE DEFECT: reportTruncated() (src/main.js:~902) tells the buyer their publicationCount "
 "'is a floor, not a total. There is no cursor on this endpoint, so the rest cannot be reached.' The second "
 "sentence is wrong, and it is the strongest class of claim an Actor can make (nothing can be done). "
 "MEASURED LIVE TODAY, keyless read-only curls on api.reporter.nih.gov/v2/publications/search, $0, no Actor "
 "runs. Negative control first: core_project_nums [P30CA008748] limit 1 -> HTTP 200, meta.total 32739 (was "
 "32598 at c2576, normal drift), so the endpoint was genuinely answering for every probe. "
 "(1) PUB_OFFSET_WALL=10000 HOLDS exactly as c2576 measured: offset 9999 limit 500 -> 200 with 1 row; "
 "offset 10000 limit 1 -> clean 400 whose body is self-documenting (\"System doesn't support offset value "
 "greater than 9,999. Please narrow down your search criteria.\"). The 'no cursor' half of the claim also "
 "holds -- meta.search_id is present but always null. "
 "(2) THE PART THAT IS WRONG: meta ECHOES sort_field/sort_order (default coreproject/desc), and both are "
 "honored as INPUTS, not ignored -- sort_field 'pmid' + sort_order asc starts at pmid 1293087, desc starts "
 "at 42956294, and a bogus sort_field ('zzz_bogus') returns HTTP 500, which proves the field is validated "
 "rather than silently dropped. So a REVERSE-SORTED second walk reaches a whole second block of 10,000 rows. "
 "Proven disjoint, not assumed: asc ranks 1-500 and 9501-10000 vs desc ranks 1-500 and 9501-10000 on the same "
 "project -> overlap exactly 0 pmids, and desc's deepest reached pmid (36000006) is strictly PAST the asc "
 "walk's horizon (max 28899556). CONSEQUENCE: for any single project with total <= 20000 papers the count is "
 "NOT a floor at all -- it is fully reachable (asc covers ranks 1..10000, desc covers total-9999..total, and "
 "those union to 1..total whenever total <= 20000); above 20000 the floor still doubles from 10000 to 20000. "
 "(3) FIX-SAFETY PREMISE CHECKED (this is what makes the fix shippable rather than a guess): pmid-sorted "
 "paging is STABLE and monotonic, so the two walks are true mirrors -- asc offset 0 limit 500's tail (ranks "
 "496-500 = 3860841/3863119/3863134/3865190/3873074) is byte-identical to offset 495 limit 10's head, each "
 "page is sorted ascending, and 0 duplicate pmids within a page. Note the current walk passes NO sort_field, "
 "so it pages on the DEFAULT coreproject sort -- within a single project every row ties on that key, so "
 "today's forward paging has no guaranteed total order either; moving both walks to pmid is a determinism "
 "improvement independent of the wall fix. "
 "NOT FIXED THIS CYCLE, DELIBERATELY: walkPubBatch is in the hot path of every run with publications "
 "enabled, and a paging-core change plus a build push needed more regression budget than the slot had left "
 "after the measurement. Filed as `NEW c3220` in tasks/queue.md with the exact fix shape, the reachability "
 "arithmetic, the tie hazard and the regression set. The audit itself is CLOSED -- the defect is identified, "
 "measured and bounded, not merely suspected. check-zero-row-message 24 Actors / 63 pushed===0 branches / "
 "0 MISS (it does not and cannot catch this class: the string is present and well-formed, it is the FACT "
 "inside it that is false). No code, README, build or registry change this cycle, $0 spend."
)
a["unreachable_remedy"] = 3220
a["unreachable_remedy_note"] = note + " | PRIOR " + a["unreachable_remedy_note"]
json.dump(d, open(P, "w"), indent=1, sort_keys=True)
print("recorded; note chars:", len(a["unreachable_remedy_note"]))
