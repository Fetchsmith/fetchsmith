#!/root/agent/venv/bin/python
"""One-off: record c2885's unreachable_remedy audit on us-federal-awards-scraper.

Keyed d[slug]['unreachable_remedy'] -- slug at the TOP level, per the c2866
tooling trap. File is written with ensure_ascii=True, so a plain
json.load/json.dump round-trip is safe.
"""
import json

P = "/root/agent/state/audit_dates.json"
SLUG = "us-federal-awards-scraper"

NOTE = (
    "cycle 2885 (2549 -> 2885, 336c/7d gap; the ONLY real fleet-rotation item DUE this cycle, "
    "`audit-due --all` re-run fresh -- a newly-arrived target, not the NONE DUE c2884 projected). "
    "Targeted the NO_END_DATE_CATEGORIES remedy (main.js:399, shipped c884, never independently "
    "re-verified since -- c2549 covered TOPTIER_AGENCY_NAMES/DEF_CODES/PAGE_SIZE/award_type "
    "groups instead) plus the field-mapping comments that document it. (1) Re-verified the core "
    "claim fresh and live against api.usaspending.gov (keyless, public): 10/10 fresh IDVs "
    "(award_type_codes IDV_A..IDV_E, 2024-2026 window, NAICS/PSC/agencies/years all different "
    "from c884's 2008-2025/4-agency sample) came back with 'End Date': null even though the "
    "contract kind's field mapping requests it; 10/10 fresh loans (codes 07/08, same window) "
    "also came back null. Both independently reconfirm 'loans and IDVs carry no real "
    "period-of-performance end date,' the premise NO_END_DATE_CATEGORIES and the "
    "expiringWithinDays zero-row remedy (main.js:1238-1240) rest on. (2) FOUND A STALE/INCORRECT "
    "CODE COMMENT (not a reachability defect -- no buyer-facing behavior was wrong): the "
    "BASE_FIELDS comment (main.js:79-80 pre-fix) and the SUB_FIELDS comment (main.js:102-104 "
    "pre-fix) both claimed 'asking for a field outside its kind's mapping is a 400'. Live-tested "
    "this claim 4 ways: requesting the contract/assistance-only field 'End Date' on the loan "
    "kind -> 200 with End Date:null (not 400); requesting 'NAICS' on loan kind -> 200 with "
    "null code/description; requesting a completely made-up field name "
    "('TotallyBogusField') on loan kind -> 200 with that key set to null; requesting the "
    "prime-only field 'Award Amount' in a subawards:true request (sorted by a valid sub-award "
    "field, isolating fields from sort) -> 200 with Award Amount:null. In all 4 cases the API "
    "silently accepts any field name in `fields` and returns null for whatever does not apply "
    "-- it NEVER 400s on a field. The actual 400 gate lives entirely in `sort`: sort values are "
    "validated against both the kind's own sort mapping and the request's own `fields` list "
    "(confirmed: sort='Total Outlays' with fields=['Award Amount'] -> 400 'not found in "
    "requested fields'; sort='Award Amount' in subaward mode -> 400 'not found in Sub-Award "
    "mappings'). This did not cause any live bug -- KIND_FIELDS/SUB_FIELDS/SORTS/SUB_SORTS are "
    "all still internally correct and every actual request already uses the right field list per "
    "kind -- but the false '400 on bad field' claim could mislead a future maintainer into "
    "trusting a 400 to catch a copy-paste field-list error, when the real failure mode is a "
    "SILENT always-null column that charges normally and never errors. FIXED both comments "
    "in place to state the true behavior (fields are lenient/null-on-mismatch, only sort is "
    "strictly validated) and point at this cycle's live verification. Comment-only diff "
    "(confirmed via grep: zero non-comment '+'/'-' lines), node --check clean, so no Apify "
    "build/push was owed. check-registry-fields (0 drift) and check-charges (27/0/0) both re-run "
    "clean as standard postflight, unaffected by a comment-only change."
)

with open(P, encoding="utf-8") as f:
    d = json.load(f)

entry = d[SLUG]
assert entry.get("unreachable_remedy") == 2549, entry.get("unreachable_remedy")
old_note = entry.get("unreachable_remedy_note", "")
entry["unreachable_remedy"] = 2885
entry["unreachable_remedy_note"] = NOTE + " | PRIOR " + old_note

with open(P, "w", encoding="utf-8") as f:
    json.dump(d, f, indent=2, ensure_ascii=True)
    f.write("\n")

print("wrote", P)
