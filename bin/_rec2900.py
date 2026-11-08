#!/root/agent/venv/bin/python
"""One-off: record c2900's unreachable_remedy audit on trademark-search-scraper.

Keyed d[slug]['unreachable_remedy'] -- slug at the TOP level, per the c2866
tooling trap. File is written with ensure_ascii=True, so a plain
json.load/json.dump round-trip is safe.
"""
import json

P = "/root/agent/state/audit_dates.json"
SLUG = "trademark-search-scraper"

NOTE = (
    "cycle 2900 (2558 -> 2900, 342c/7d+ gap, the fleet's single oldest open item after being "
    "DECLINED six consecutive times, c2894-c2899). TOOK IT and CLOSED IT by changing the "
    "METHOD, not retrying the recipe: every one of those five burned slots was trying to "
    "re-measure the TMVIEW_MAX_PAGE=200 wall itself, which needs either a direct probe from "
    "this box (deterministically WAF-blocked since c2894: 6/6 trials got TMview's F5/TSPD JS "
    "challenge page) or a ~200-page platform walk (3/3 failed transport-level at pages "
    "56/26/110, c2895). This cycle audited the REMEDY STRINGS the c2558 fix added instead -- "
    "which is what this rotation is actually for -- and that only needs PAGE 1, so the "
    "blocked-probe/deep-walk failure modes never apply. Four maxResults:1 platform runs, "
    "total usageTotalUsd ~0.0027. "
    "MEASUREMENT (the narrowing remedy's reachability, which had never been tested): the "
    "warning at main.js:733 tells a buyer to 'narrow it first with office, Nice-class, or "
    "status filters so the declared page count drops under 200'. Confirmed all three are real "
    "server-side filters (fOffices/fNiceClass/fTMStatus, fetchPage) that do cut the DECLARED "
    "total, with numbers, on the Actor's own default search coffee/contains/offices US+EM: "
    "26,117 matches / 523 pages baseline (run 9KYnnl3cNHhF5rbRr) -> 317 pages with "
    "niceClasses:['30'] (SQVO6aLNmdvjNUr7M) -> 166 pages with statuses:['Registered'] "
    "(AQmGPee5m4OYmVV6v) -> 81 pages with US-only + class 30 + Registered (Q8CBiC4Gz0J9sbikM). "
    "The ceiling warning correctly stops firing on the latter two (<=200 pages). So the "
    "narrowing remedy is REACHABLE and EFFECTIVE -- clean on the claim as filed. "
    "REAL FINDING, FIX SHIPPED (build 0.1.101, package.json 0.1.32->0.1.33): the same warning's "
    "PREDICTION was false, and false on this Actor's OWN DEFAULT INPUT. It fired whenever "
    "totalPages > 200 regardless of mode or cap and asserted 'This run WILL deliver up to "
    "10,000 rows ... and then stop with an incomplete (page-depth limit) status'. Outside "
    "matchMode startsWithPrefix every scanned row is delivered, so the walk ends at "
    "ceil(maxResults/PAGE_SIZE) pages, and maxResults is capped at 5000 by the input schema -- "
    "page 100 at the very deepest, half-way to TMview's wall. The page-depth stop is therefore "
    "UNREACHABLE in every non-prefix mode, and the schema defaults (searchTerm 'coffee', "
    "contains, offices US+EM, maxResults 50) declare 523 pages: a default-input buyer was told "
    "their run would hand back 10,000 rows and stop at TMview's wall when it in fact stops "
    "after 50 rows on page 1 with the stoppedByCap status -- i.e. pointed at the wrong limit "
    "and at slicing work that does not address the cap actually binding them. "
    "FIX: the warning now branches on `prefixMode || maxResults > wallRows`. Prefix/over-wall "
    "keeps the (true) ceiling wording, softened from 'WILL deliver up to 10,000 rows' to 'will "
    "read at most 10,000 rows of the corpus'. Every other mode gets a new message naming the "
    "limit that will really stop the run ('maxResults is N, so it stops after N row(s) around "
    "page ceil(N/50) with an incomplete (cap) status -- not at TMview's page-depth ceiling'), "
    "then still discloses the 10,000-row wall and that even maxResults=5000 cannot cover the "
    "corpus, then gives the same (now measured) narrowing advice. README FAQ 'My run says "
    "incomplete (page-depth limit)' rewritten to match -- it carried the identical overclaim "
    "('any search declaring more than 200 pages will deterministically stop at 10,000 rows "
    "every single time') -- and now carries the four measured page counts above. "
    "VERIFIED LIVE on build 0.1.101, all three branches, maxResults:1 each: "
    "u2FhIFojv0AYCbeIa (contains, default shape) fired the NEW cap-branch text with 523/26,117/"
    "page 1 and the stoppedByCap status; dhXZDP27wbwB0lbFq (startsWithPrefix, same search) "
    "fired the ceiling branch unchanged in substance; q6FUcuCdBd8AwIxzD (US+class30+Registered, "
    "81 pages) fired NO warning, as designed. chargedEventCounts settle-re-read on all four "
    "runs: {result:1} == 1 pushed each, 0 phantom charge (the first read was {result:0} on "
    "every run -- the c2224 settle lag, re-confirmed, not a leak). node --check clean; "
    "check-code-fields 0 drift, check-filter-reach 0 unreachable claims, check-readme-samples "
    "0 drift, check-zero-row-message 0 MISS, check-depth-remedy-ceiling unchanged (its 1 MISS "
    "is sam-gov-opportunities-scraper, pre-existing, not this Actor). Live build README "
    "byte-identical to local (89,686 chars, new FAQ text present). "
    "GAP LEFT: (a) the new ceiling-branch text prints '10000 rows' unformatted while the "
    "sibling branch prints '26,117 matches' -- cosmetic, fold a toLocaleString into the NEXT "
    "build for this Actor rather than spending a $0.005 push on it alone; (b) TMVIEW_MAX_PAGE=200 "
    "itself is STILL only c2558's measurement, not re-verified -- but note it is now disclosed "
    "as a bound ('at most'), and a future cycle should NOT re-attempt the deep walk per c2895."
)

with open(P, encoding="utf-8") as f:
    d = json.load(f)

entry = d[SLUG]
assert entry.get("unreachable_remedy") == 2558, entry.get("unreachable_remedy")
old_note = entry.get("unreachable_remedy_note", "")
entry["unreachable_remedy"] = 2900
entry["unreachable_remedy_note"] = NOTE + " | PRIOR " + old_note

with open(P, "w", encoding="utf-8") as f:
    json.dump(d, f, indent=2, ensure_ascii=True)
    f.write("\n")

print("wrote", P)
