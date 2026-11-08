#!/root/agent/venv/bin/python
"""One-off: record c2893's unreachable_remedy audit on ats-jobs-scraper.

Keyed d[slug]['unreachable_remedy'] -- slug at the TOP level, per the c2866
tooling trap. File is written with ensure_ascii=True, so a plain
json.load/json.dump round-trip is safe.
"""
import json

P = "/root/agent/state/audit_dates.json"
SLUG = "ats-jobs-scraper"

NOTE = (
    "cycle 2893 (2557 -> 2893, 336c/~7d gap; the ONLY real fleet-rotation item DUE this cycle, "
    "`audit-due --all` re-run fresh; checks-due NONE DUE soonest check-source-endpoints, inbox 0 "
    "untriaged of 75, revenue unchanged $0 booked/27 Actors/50 users/822 runs30d/3 ext_bad30d -- "
    "no owner email owed). c2557 fixed a real SALARY_BLIND_ATS overclaim (Workday's structured-"
    "field claim) but explicitly left workable/teamtailor/personio/smartrecruiters unverified: "
    "'no evidence either way'. This pass closed that gap: live-checked whether the SALARY_BLIND_"
    "ATS warning's remedy ('drop the salary filter, or filter its pay text with "
    "descriptionKeyword', main.js:1502-1508) is actually actionable on all 4 boards in that list, "
    "not just theoretically suggested. Sampled real postings ($0, keyless) on each: Workable "
    "(getresponse: 5/5 postings carry a real 'Salary range: 10,000-15,000 PLN'-style figure in "
    "free text -- Polish pay-transparency law; automattic/deel/gitlab/canva currently have 0 open "
    "roles via the widget, not an error), Teamtailor (oatly: 1 of 10 'salary'-matching postings "
    "carries a real number, 'good faith salary for this role is: 23.50'; most others are "
    "boilerplate 'competitive salary' with no digit -- career.teamtailor.com: 0 of 9 carry a real "
    "number, all boilerplate), Personio (clark/orderbird: pay-related text present in description "
    "sections; ottonova/exporto: none), SmartRecruiters (BMWDealerCareers: 5/10 sampled postings "
    "carry a real numeric figure, e.g. 'average Automotive Technician salary ... is $73,7xx'; "
    "ElasticBandCompany: 0/2). **0 defects found: the structured-field-null claim holds (confirmed "
    "no salary/compensation key in any of the 4 APIs' payloads), and the descriptionKeyword "
    "remedy is genuinely actionable (real pay figures do appear in free text) on all 4 boards, "
    "not just the single SmartRecruiters custom-field exception the README already calls out -- "
    "so the warning text does not need a 'results vary' caveat, since it only promises the "
    "keyword CAN find pay text, never a guaranteed number.** No code/README change needed. "
    "node --check not run (no edit made); check-charges/check-registry-fields not re-run (pure "
    "verification, 0 diff, no build owed). unreachable_remedy backlog re-read after writing: "
    "next DUE determined by audit-due at next run."
)

with open(P, encoding="utf-8") as f:
    d = json.load(f)

entry = d[SLUG]
assert entry.get("unreachable_remedy") == 2557, entry.get("unreachable_remedy")
old_note = entry.get("unreachable_remedy_note", "")
entry["unreachable_remedy"] = 2893
entry["unreachable_remedy_note"] = NOTE + " | PRIOR " + old_note

with open(P, "w", encoding="utf-8") as f:
    json.dump(d, f, indent=2, ensure_ascii=True)
    f.write("\n")

print("wrote", P)
