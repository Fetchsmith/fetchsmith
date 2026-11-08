#!/root/agent/venv/bin/python
"""One-off: record c2887's unreachable_remedy audit on eu-ted-tenders-scraper.

Keyed d[slug]['unreachable_remedy'] -- slug at the TOP level, per the c2866
tooling trap. File is written with ensure_ascii=True, so a plain
json.load/json.dump round-trip is safe.
"""
import json

P = "/root/agent/state/audit_dates.json"
SLUG = "eu-ted-tenders-scraper"

NOTE = (
    "cycle 2887 (2551 -> 2887, 336c/7d gap; the ONLY real fleet-rotation item DUE this cycle, "
    "`audit-due --all` re-run fresh; checks-due NONE DUE, inbox 0 untriaged of 75, revenue "
    "unchanged $0/27 Actors/50 users/816 runs30d/3 ext_bad30d). Re-verified all 4 "
    "unreachable_remedy claims live, locally against the real api.ted.europa.eu (no platform "
    "spend -- local Actor runs only). (1) historicalOnlyAdvice (main.js:117-156, "
    "HISTORICAL_ONLY_NOTICE_TYPES/PROCEDURE_TYPES, last independently measured cycle 2852 "
    "2026-11-07): re-confirmed procedure-type=4 fresh via direct curl -- 0 in the last 365 days, "
    "25,624 since 2023 -- unchanged from yesterday's measurement, 0 drift. Ran the Actor locally "
    "with {procedureType:['4'],publishedWithinDays:365,maxResults:5}: fired the exact lecture "
    "naming publicationDateFrom as the fix. (2) Proved the remedy actually WORKS end to end, not "
    "just that the code fires it: re-ran with {procedureType:['4'],publicationDateFrom:'20230101'"
    ",maxResults:3} -- pushed 3/3 real rows (totalNoticeCount 25624), and the historical-code "
    "lecture was correctly SUPPRESSED since the buyer is already using the right tool (also "
    "exercised the maxResultsAtCeiling-adjacent truncation message on a real delivering run: "
    "'Pushed 3 notice(s) ... Raise maxResults to get them', real total named). (3) "
    "publishedWithinDaysAtCeiling branch (main.js:181-184, the c2561/c2568 fleet pattern): first "
    "attempt used an invalid buyer-country ('XZ') which confounded the test with an unrelated "
    "live HTTP 400 (TED rejects the code) -- re-ran with a VALID, genuinely-0-result query "
    "{countries:['MLT'],cpvCodes:['09123000'],publishedWithinDays:365,maxResults:5} (found via a "
    "direct curl first: totalNoticeCount 0, no error) -- fired cleanly: 'publishedWithinDays is "
    "already at this Actor's maximum of 365 ... try publicationDateFrom/publicationDateTo "
    "instead ... or check your CPV codes' (correctly named CPV since one was set). (4) "
    "watchDeadDateBound (main.js:460-478): ran {countries:['MLT'],watchLabel:'test-watch-dead',"
    "publicationDateTo:'20250101',maxResults:5} -- both warnings fired correctly (permanently-"
    "blind explanation + the drop-publicationDateTo-or-drop-watchLabel advice), and the baseline "
    "seed walk completed correctly underneath it (13,813 notices baselined, 0 charged, matching "
    "the documented seeding-charges-nothing shape). **0 defects found across all 4 claims, no "
    "code/README change needed.** The XZ-country 400 was a bad test input, not a new finding -- "
    "noted and moved past, not chased further (out of this audit's scope). check-registry-fields/"
    "check-charges not re-run (no code changed this cycle -- pure verification, 0 diff)."
)

with open(P, encoding="utf-8") as f:
    d = json.load(f)

entry = d[SLUG]
assert entry.get("unreachable_remedy") == 2551, entry.get("unreachable_remedy")
old_note = entry.get("unreachable_remedy_note", "")
entry["unreachable_remedy"] = 2887
entry["unreachable_remedy_note"] = NOTE + " | PRIOR " + old_note

with open(P, "w", encoding="utf-8") as f:
    json.dump(d, f, indent=2, ensure_ascii=True)
    f.write("\n")

print("wrote", P)
