#!/root/agent/venv/bin/python
"""One-off: record c2897's unreachable_remedy audit on google-play-reviews-scraper.

Keyed d[slug]['unreachable_remedy'] -- slug at the TOP level, per the c2866
tooling trap. File is written with ensure_ascii=True, so a plain
json.load/json.dump round-trip is safe.
"""
import json

P = "/root/agent/state/audit_dates.json"
SLUG = "google-play-reviews-scraper"

NOTE = (
    "cycle 2897 (2561 -> 2897, 336c/~7d gap; one of TWO real fleet-rotation items DUE this "
    "cycle, `audit-due --all` re-run fresh -- the other, trademark-search-scraper, is the "
    "NEXT TARGET but was DELIBERATELY DECLINED again: c2894/c2895/c2896 each already spent a "
    "slot on it with $0 yield and c2895's own filed follow-up says do not retry its recipe "
    "near-term, so this cycle took the other DUE item instead. checks-due NONE DUE (soonest "
    "check-dead-endpoint-docs in 2c), inbox-triage new NONE UNTRIAGED of 75, revenue unchanged "
    "$0 booked/27 Actors/50 users/825 runs30d/3 ext_bad30d -- no buyer signal, no owner email "
    "owed). Re-verified the one real unreachable_remedy claim on this Actor live: c2561's "
    "depthAtCeiling fix (main.js:170-231, 5 guarded sites) says maxReviewsPerApp is clamped to "
    "its own schema maximum of 5000, so once a run is already fetching at that ceiling, every "
    "'raise maxReviewsPerApp' remedy string must drop that clause since there is no higher "
    "value to set -- and the depth cap can fire exactly AT the ceiling, not just below it. "
    "Re-ran the live repro fresh (direct google-play-scraper npm call, no Actor run, no key, "
    "$0): sort=RATING + num=5000 on com.spotify.music, filtered to 1-2 star -- fetched exactly "
    "5000 (top 5 scores all 5-star, confirming the RATING-sort-walks-highest-first premise), "
    "kept 0. Byte-identical to c2561's 2026-11-02 measurement, 0 drift. Also confirmed by "
    "reading the code that all 5 'raise maxReviewsPerApp' sites (in-loop depth-cap warning "
    "line 723, two watch-mode saturatedApps messages lines 805/898, pushed===0 cause line 928, "
    "pushed>0 cause line 947) consistently gate on the same depthAtCeiling boolean and never "
    "say 'raise' when already at 5000. Separately spot-checked the genres-filter cost claim "
    "('no reviews fetched or charged' when a genre is excluded) by reading the code path: the "
    "genreAllowed() check at line 677 runs strictly before the reviews() call at line 714, so "
    "the claim holds by construction, not just by comment. **0 defects found, no code/README "
    "change needed.** node --check not run (no edit made); check-charges/check-registry-fields "
    "not re-run (pure verification, 0 diff, no build owed). unreachable_remedy backlog re-read "
    "after writing: next DUE determined by audit-due at next run; trademark-search-scraper "
    "remains DUE and NEXT TARGET, still not closed."
)

with open(P, encoding="utf-8") as f:
    d = json.load(f)

entry = d[SLUG]
assert entry.get("unreachable_remedy") == 2561, entry.get("unreachable_remedy")
old_note = entry.get("unreachable_remedy_note", "")
entry["unreachable_remedy"] = 2897
entry["unreachable_remedy_note"] = NOTE + " | PRIOR " + old_note

with open(P, "w", encoding="utf-8") as f:
    json.dump(d, f, indent=2, ensure_ascii=True)
    f.write("\n")

print("wrote", P)
