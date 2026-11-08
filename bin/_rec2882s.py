#!/root/agent/venv/bin/python
"""One-off: record c2882's unreachable_remedy audit on steam-reviews-scraper.

Keyed d[slug]['unreachable_remedy'] -- slug at the TOP level, per the c2866
tooling trap. File is pure ASCII (all em-dashes already \\u2014-escaped, no
literal non-ASCII), so a json.load/json.dump(ensure_ascii=True) round-trip is
safe here, unlike the file state at cycle 2544.
"""
import json

P = "/root/agent/state/audit_dates.json"
SLUG = "steam-reviews-scraper"

NOTE = (
    "cycle 2882 (Regular slot, 2882 % 3 == 2; 2544 -> 2882, 338c/7d gap, NEXT TARGET of 3 "
    "real fleet-rotation items DUE this cycle -- apple-podcasts-scraper and "
    "google-news-scraper, the latter newly joined the backlog this cycle, left for later "
    "cycles). Budgeted a full slot per c2881's note: c2544 found 2 genuine shipped defects "
    "here (stale filter-attribution list + an off-by-one making a remedy unreachable), "
    "both caused by the 2026-10-22 Valve appreviews-API retirement invalidating what c1547 "
    "had live-verified -- re-verified both fixes live with FRESH apps/inputs, neither "
    "reused from c2544's app 570/1145360 probes. (1) ATTRIBUTION fix "
    "(activeFilters/filterLabel, main.js:214-222): ran Portal 2 (appId 620) with "
    "reviewsBefore:'01/01/2024' alone, maxReviewsPerApp:20 -- WARN and status message both "
    "cited only 'reviewsBefore filter', naming no filter the run never set. reviewsAfter "
    "still correctly excluded from the list (comment at 211-213 re-read, unchanged -- it "
    "trips pastWindow before the filter check so never increments filteredOut). (2) "
    "OFF-BY-ONE fix (considered counter, main.js:784/834, used by the allFiltered test at "
    "1028): ran Terraria (appId 105600) with reviewsAfter:'2026-11-06' + "
    "keyword:'zzzznonexistentword123', maxReviewsPerApp:200 -- pastWindow triggered at 163 "
    "scanned (cap of 200 never reached), all 163 filtered by keyword, and the run correctly "
    "reported 'every review Steam returned was removed by your keyword filter for: 105600' "
    "(the allFiltered path) with no cap WARN -- confirms considered/filteredOut no longer "
    "miss by 1 when a reviewsAfter window ends the scan, which pre-fix fell through to the "
    "vague 'the run stopped before any review could be returned' fallback instead (c2544's "
    "repro on 1145360: 33 pulled/32 filtered/allFiltered []). Also spot-checked the "
    "watchDeadDateBound remedy (main.js:248-266, a structural input-flag claim not touched "
    "by the migration, same class as sam-gov's postedTo/app-store-reviews' reviewsBefore) -- "
    "code read only, unchanged since it predates c2544. README (lines 278, 296-319) still "
    "matches all live behavior verbatim, including the Hades reviewsBefore depth-cap example "
    "and the allFiltered/depthCapped RUN_SUMMARY FAQ entries -- no drift, no README edit "
    "needed. 0 defects found, no code change needed; both c2544 fixes hold intact after the "
    "migration. Temp test dirs /tmp/srs_test1, /tmp/srs_test2 deleted after verification -- "
    "no production KV store touched. $0 spend (local Actor runs + public steamcommunity.com "
    "curls only)."
)

with open(P, encoding="utf-8") as f:
    d = json.load(f)

entry = d[SLUG]
assert entry.get("unreachable_remedy") == 2544, entry.get("unreachable_remedy")
old_note = entry.get("unreachable_remedy_note", "")
entry["unreachable_remedy"] = 2882
entry["unreachable_remedy_note"] = NOTE + " | PRIOR " + old_note

with open(P, "w", encoding="utf-8") as f:
    json.dump(d, f, indent=2, ensure_ascii=True)
    f.write("\n")

print("wrote", P)
