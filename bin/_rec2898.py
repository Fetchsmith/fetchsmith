#!/root/agent/venv/bin/python
"""One-off: record c2898's varied_test audit on hacker-news-scraper.

Keyed d[slug]['varied_test'] -- slug at the TOP level, per the c2866 tooling
trap. File is written with ensure_ascii=True, so a plain json.load/json.dump
round-trip is safe.
"""
import json

P = "/root/agent/state/audit_dates.json"
SLUG = "hacker-news-scraper"

NOTE = (
    "cycle 2898 (2562 -> 2898, 336c/7d gap, the sole real fleet-rotation varied_test item "
    "DUE this cycle per audit-due --all; the other DUE item, unreachable_remedy: "
    "trademark-search-scraper, was DECLINED again -- c2894/c2895/c2896/c2897 already burned "
    "4 slots on it for $0 yield and c2895's own filed follow-up says do not retry its recipe "
    "near-term. checks-due NONE DUE (soonest check-dead-endpoint-docs in 1c), inbox-triage new "
    "NONE UNTRIAGED of 75, revenue unchanged $0 booked/27 Actors/50 users/825 runs30d/3 "
    "ext_bad30d -- no buyer signal, no owner email owed). "
    "Closed the exact gap c2562's own note left open: autoSplitLargeQueries' "
    "splitExhausted='max-split-windows' branch (maxSplitWindows set too low to finish "
    "splitting) and the sortBy:date pairing, both never exercised live by any prior "
    "varied_test entry on this Actor (1256/1618/1830/2195/2224/2562 covered "
    "queries/tags/filters/usernames/maxCommentDepth/watchChanges/the halving loop itself, but "
    "always with the schema default maxSplitWindows:24, which that query never exhausted, and "
    "always with sortBy left at the relevance default). "
    "METHOD, predicted FREE before any paid run (direct curl against hn.algolia.com, no key): "
    "query 'ai' tags:[story], Aug 2025 whole month (postedAfter 2025-07-31T23:59:59Z / "
    "postedBefore 2025-08-31T00:00:00Z -> baseWindowFrom=1754006400/baseWindowTo=1756598400 "
    "exactly, verified against parseDateBound's created_at_i>X/+1 half-open math) totals "
    "nbHits=4325, well past the 1000-hit ceiling. Bisecting it at the exact midpoint the code "
    "itself computes (1755302400) gives two halves of 2258 and 2067 -- BOTH still past 1000, "
    "so with maxSplitWindows forced to its schema-documented floor of 3 (main.js:52, "
    "Math.max(3, ...)), the first split must exhaust: window 1 (unsplit) hits the ceiling and "
    "splits (roomForTwoMore 1+0+2<=3 true, windowsSearched=1, windowsSplit=2); window 2 (the "
    "first popped half) hits the ceiling again but can't split further (roomForTwoMore "
    "2+1+2<=3 false -> splitExhausted='max-split-windows', windowsSearched=2); window 3 (the "
    "second half) same (windowsSearched=3). Predicted final: windowsSearched=3, "
    "windowsSplit=2, declaredMatches=4325, splitExhausted='max-split-windows', scanned capped "
    "at scanCap=ALGOLIA_MAX_HITS*maxSplitWindows=3000. "
    "COST CONTROL (the reusable technique worth keeping): excludeKeywords is applied in the "
    "per-hit loop strictly AFTER scanned/fetchedInWindow/uniqueFetched increment but BEFORE "
    "pushResult (main.js:974-1009), so it cannot affect server-side nbHits or the "
    "ceiling/split detection, only which scanned rows actually get billed. Sampled 50 real "
    "hits from the target window first and confirmed 'ai' appears in literally 50/50 titles "
    "(query keyword, near-tautological), then set excludeKeywords:['ai'] to exercise the full "
    "3000-item scan/split machinery for a fraction of the $0.0002/0.0001-tiered PAY_PER_EVENT "
    "cost a buyer-realistic row count would imply. "
    "LIVE RUN (bin/run-charged, sortBy:date, autoSplitLargeQueries:true, maxSplitWindows:3, "
    "maxItemsPerQuery/maxResults:5000, excludeKeywords:['ai'], run wDjHnRopSYTfoUN2z, "
    "SUCCEEDED): windowsSearched=3, windowsSplit=2, declaredMatches=4325 (byte-exact match to "
    "the free prediction), scanned=3000 (== scanCap exactly), uniqueScanned=2000 (confirms "
    "1000 of the 3000 total hits were dedup'd re-scans -- the unsplit pass and the newer half "
    "cover overlapping newest-first territory under sortBy:date, exactly as the windowStack "
    "half-open-bounds comment implies), splitExhausted='max-split-windows' exactly as "
    "predicted, hitPaginationCeiling=true. Only 299 of the 2000 unique hits survived the "
    "excludeKeywords filter (delivered), pushed=299, chargedEventCounts settled {result:299} "
    "== 299 pushed exactly -- 0 phantom charge, confirming the exclusion-before-billing "
    "invariant holds even mid-split. ZERO deviation from the free prediction on every "
    "structural field (windowsSearched/windowsSplit/declaredMatches/splitExhausted). "
    "**0 defects found, no code/README change needed.** node --check not run (no edit made); "
    "check-charges/check-registry-fields not re-run (pure verification, 0 diff, no build "
    "owed). Spend: ~299 charged rows at the $0.0002/0.0001 tiered rate, roughly $0.03-0.06, "
    "well under the $25/cycle trip-wire. GAP STILL LEFT for a future cycle (per c2562's own "
    "note, now narrower): the null-on-failure commentDepth path and splitExhausted's sibling "
    "branch combined with watchChanges are both still unexercised live."
)

with open(P, encoding="utf-8") as f:
    d = json.load(f)

entry = d[SLUG]
assert entry.get("varied_test") == 2562, entry.get("varied_test")
old_note = entry.get("varied_test_note", "")
entry["varied_test"] = 2898
entry["varied_test_note"] = NOTE + " | PRIOR " + old_note

with open(P, "w", encoding="utf-8") as f:
    json.dump(d, f, indent=2, ensure_ascii=True)
    f.write("\n")

print("wrote", P)
