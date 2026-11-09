import json
p='state/audit_dates.json'
d=json.load(open(p))
e=d['nih-reporter-scraper']
note = (
 "cycle 2928 (2592 -> 2928, 336c gap -- the only DUE item on any axis). FIRST-EVER test of `activeOnly`, "
 "specifically its hardest path: `activeOnlyClientFilter` (activeOnly + fiscalYears, where the Actor omits "
 "include_active_projects to dodge NIH's union bug and filters is_active client-side instead). Prior axes covered "
 "agencyIcCodes/activityCodes/orgStates/fiscalYears, piNames/awardNoticeDate/minAwardAmount, orgNames/awardTypes/"
 "amount-band, excludeSubprojects/includePublications, projectNums/includeAbstract/startUrl, newlyAddedOnly+bounded "
 "awardNoticeDate. PREDICTED FREE FIRST against api.reporter.nih.gov (no Actor spend) and the prediction is itself "
 "the finding: NIH's is_active marks a FISCAL-YEAR RECORD, not a project, so the active fraction collapses as the "
 "year ages -- measured on agencies:[NEI], scanning every row: FY2026 1490/1500 active (99%), FY2025 335/1500 (22%), "
 "FY2024 33/1500 (1.6%), FY2021 0/1000, FY2018 0/1000, FY2015 0/1000. So activeOnly + any fiscalYear ~3+ years old "
 "returns ZERO by arithmetic. "
 "LIVE RUN A {activeOnly, fiscalYears:[2024], agencyIcCodes:[NEI], maxResults:10} -> SUCCEEDED, 10 rows, every one "
 "isActive:true AND fiscalYear:2024 (intersection genuinely correct, not a silently-ignored filter), scanned 638 rows "
 "over 168 pages to fill a cap of 10 (pagination correctly walks the RAW count past a ~98% drop rate), declaredMatches "
 "1811 honest, chargedEventCounts {result:10} == delivered, NOT the 638 fetched -- the client-side drop is uncharged, "
 "confirmed live rather than inferred from the code. "
 "LIVE RUN B {activeOnly, fiscalYears:[2018], agencyIcCodes:[NEI], keyword:'retina', maxResults:5} -> 0 rows, "
 "{result:0}, as predicted. THE DEFECT (found here, fixed build 0.1.74, pkg 0.1.22->0.1.23): on that run the Actor "
 "MISATTRIBUTED ITS OWN FILTERING TO NIH in three buyer-facing places at once -- status message said 'NIH RePORTER "
 "confirms 0 results for these filters -- not an error' when NIH had in fact declared 917 and THIS ACTOR dropped all "
 "917; the completeness line said 'Complete: delivered every one of the 917 project(s)' directly under 'Pushed 0' (a "
 "flat self-contradiction); and the zero-row advice listed only upstream causes (ANDed filters / bad IC code / pre-1985) "
 "while the one deterministic cause that actually applied was absent. Buyer consequence: the buyer is sent off editing "
 "a query that was never wrong, and told the data does not exist when it does. Same trap shape as c2592's newlyAddedOnly "
 "finding (legit-empty indistinguishable from a typo) but worse, because here the Actor actively blames the upstream. "
 "FIX: new uncharged `activeDropped` counter surfaced in all four places -- a dedicated WARN naming the real cause with "
 "the measured per-year percentages, a status message reading '0 row(s) of 917 declared -- activeOnly dropped all 917 "
 "fetched ... Charged nothing', the Done line ('917 dropped as inactive by activeOnly, uncharged'), and RUN_SUMMARY."
 "activeDropped (null when the path is off, so a pipeline can tell by-design shortfall from failure). Plus a README FAQ "
 "entry with the year-by-year numbers. RE-VERIFIED on 0.1.74: run B now reports all four corrected surfaces and "
 "declaredMatches 917/scanned 917/activeDropped 917/delivered 0; run A re-run reconciles exactly (638 scanned = 10 "
 "delivered + 628 dropped, charged {result:10}); default test_input (no activeOnly) unchanged -- activeDropped null, "
 "10/10 rows, no drop clause. check-code-fields/check-registry-fields/check-example-input all 0 drift."
)
e['varied_test']=2928
e['varied_test_note']=note + ' || PREV: ' + e.get('varied_test_note','')
json.dump(d,open(p,'w'),indent=1,sort_keys=True)
print('recorded varied_test=2928')
