#!/root/agent/venv/bin/python
"""One-off: record c2884's unreachable_remedy audit on google-news-scraper.

Keyed d[slug]['unreachable_remedy'] -- slug at the TOP level, per the c2866
tooling trap. File is written with ensure_ascii=True, so a plain
json.load/json.dump round-trip is safe.
"""
import json

P = "/root/agent/state/audit_dates.json"
SLUG = "google-news-scraper"

NOTE = (
    "cycle 2884 (2546 -> 2884, 338c/7d gap; the ONLY fleet-rotation item DUE this cycle, "
    "`audit-due --all` re-run fresh). FOUND AND FIXED A REAL SHIPPED DEFECT -- the first one "
    "this axis has found on this Actor since c1549 (2-for-3 now). THE DEFECT: windowNote (the "
    "always-appended out-of-window drop note, main.js:485-487 pre-fix) hard-coded BOTH of its "
    "attributions -- it always said the dropped articles fell outside 'your "
    "publishedAfter/publishedBefore window' and always blamed 'a known Google quirk when a date "
    "window is combined with \"Exclude these domains\"'. But the c933 feature means a customer "
    "can set the window by typing after:/before: INTO THE QUERY TEXT (policed via ownWindowMs) "
    "and can exclude a domain by typing -site: there too, setting NEITHER the publishedAfter/"
    "publishedBefore fields NOR excludeSites. Such a buyer was told 11 of their articles were "
    "dropped because of two input fields they had left completely empty -- the same status-"
    "message mis-attribution class as c2543 (shopify shared activeFilters) and c2544 (steam "
    "filter attribution). Same bug in the log line (main.js:484) and in the pushed===0 "
    "'every article fell outside ...' why-cause (main.js:514). LIVE REPRO (fresh inputs, "
    "different from c2546's economy/2026-10-20..27): query text "
    "'economy -site:reuters.com after:2026-10-01 before:2026-10-08', no publishedAfter/"
    "publishedBefore, no excludeSites -> 100 items, 11 dropped, status message read 'well "
    "outside your publishedAfter/publishedBefore window (a known Google quirk when a date "
    "window is combined with \"Exclude these domains\")'. THE FIX: record WHERE the window and "
    "the exclusion actually came from at the drop site, where both facts are in scope -- "
    "outOfWindowSources ('query' | 'fields', from the existing ownTimeOp flag) and "
    "outOfWindowExcl ('field' if excludeSites.length, else 'query' if /-site:/i matches the "
    "feed's query text, else 'none'), then derive windowLabel + windowQuirk once and use them "
    "in all three places (log line, windowNote, pushed===0 why-cause). VERIFIED LIVE, 4 shapes: "
    "(A) query-text window + query-text -site: -> 'well outside the after:/before: dates in "
    "your query (a known Google quirk when a date window is combined with a -site: exclusion in "
    "the query)' -- 11 dropped of 100, correct. (B) REGRESSION, schema fields + excludeSites "
    "field (inflation, 2026-09-15..22, excludeSites:[bbc.com]) -> wording byte-identical to "
    "pre-fix ('your publishedAfter/publishedBefore window' + the 'Exclude these domains' "
    "quirk), 18 dropped of 100. (C) query-text window with NO -site: anywhere -> 46 items, 0 "
    "dropped, NO windowNote at all, which independently re-confirms c788's core measurement "
    "(the leak needs a -site: exclusion; dates alone do not leak) and doubles as the happy-path "
    "regression. The 'none' quirk branch is therefore a defensive fallback live traffic "
    "essentially never reaches -- it is traced, not live-reproduced. (D) MIXED, two queries "
    "(one with its own after:/before:, one taking the schema window) + excludeSites field -> "
    "'well outside your publishedAfter/publishedBefore window and the after:/before: dates in "
    "your query', 29 dropped, both sources named. ALSO RE-VERIFIED c2546's claim (2) fresh: the "
    "c788 date-window + -site: leak is alive and worse than the 7-in-100 originally measured -- "
    "a plain curl of the Oct-1..8 2026 window returned items dated 2011-10-01 (x3), 2017-03-22, "
    "2018-06-19, 2020-06-09, 2022-12-15, 2025-12-03/04 and even 2026-11-07 (after the "
    "`before:`), so the backstop and its buyer-facing note remain necessary. Claim (1) "
    "(VALID_TOPICS enum) NOT re-touched this cycle -- c2546 spot-checked all 20 codes only 338c "
    "ago and the file has no code change in that area; the budget went to the defect instead. "
    "README line 175 already documented both window sources correctly, so only its last "
    "sentence was extended to say the status message now NAMES whichever window it policed. "
    "Shipped build 0.1.94 (package.json 0.1.24 -> 0.1.25), live src/main.js and README verified "
    "byte-identical to local via /v2/acts/<id>/versions sourceFiles (38,541 and 69,117 chars). "
    "Guard after shipping: check-zero-row-message 24 Actors / 63 pushed===0 branches / 0 MISS. "
    "No output-field change, so no registry/dataset-schema work. $0 cash beyond the one ~$0.005 "
    "build; the 4 verification runs were local (CRAWLEE_STORAGE_DIR, useApifyProxy:false)."
)

with open(P, encoding="utf-8") as f:
    d = json.load(f)

entry = d[SLUG]
assert entry.get("unreachable_remedy") == 2546, entry.get("unreachable_remedy")
old_note = entry.get("unreachable_remedy_note", "")
entry["unreachable_remedy"] = 2884
entry["unreachable_remedy_note"] = NOTE + " | PRIOR " + old_note

with open(P, "w", encoding="utf-8") as f:
    json.dump(d, f, indent=2, ensure_ascii=True)
    f.write("\n")

print("wrote", P)
