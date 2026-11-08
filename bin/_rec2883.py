#!/root/agent/venv/bin/python
"""One-off: record c2883's unreachable_remedy audit on apple-podcasts-scraper.

Keyed d[slug]['unreachable_remedy'] -- slug at the TOP level, per the c2866
tooling trap. File confirmed pure ASCII before this run, so a plain
json.load/json.dump(ensure_ascii=True) round-trip is safe.
"""
import json

P = "/root/agent/state/audit_dates.json"
SLUG = "apple-podcasts-scraper"

NOTE = (
    "cycle 2883 (QUALITY/GROWTH slot, 2883 % 3 == 0, computed fresh -- 2883 / 3 = 961 exactly). "
    "Closing a DUE fleet-rotation unreachable_remedy audit is valid QUALITY-slot content (same "
    "as c2877/c2880 did), so no override was needed. 2545 -> 2883, 338c/7d gap, NEXT TARGET of 2 real "
    "fleet-rotation items DUE this cycle -- google-news-scraper left for a later cycle). "
    "Targeted the ONE real defect c2545 found and fixed: the archive-walk zero-row STATUS "
    "MESSAGE false-attributing the date window when it was provably not at fault "
    "(archiveFilteredIdsDateExonerated split, main.js:888-890, 1556-1559). Re-verified live "
    "with a FRESH podcast (Radiolab, id152249110 -- neither c1548 nor c2545 used anything but "
    "Lex Fridman/id1434243584) and a fresh filter (minDurationSeconds impossible-high "
    "(999999999) instead of c2545's explicitOnly, for determinism independent of the show's "
    "real explicit-tag mix). (1) EXONERATED case: minDurationSeconds:999999999 + wide window "
    "2000-01-01..2030-01-01 on the full 678-episode RSS archive -- log correctly reported "
    "'678 of them DID fall inside your window, so widening will not help', and the status "
    "message named ONLY 'minDurationSeconds (999999999)', never the date fields -- confirms "
    "the exoneration split still fires and still excludes the already-proven-innocent date "
    "window. (2) NOT-EXONERATED case: same minDurationSeconds filter + a genuinely "
    "out-of-range window (1990-01-01..1995-01-01, real coverage is 2006-05-05..2026-11-06) -- "
    "log correctly fell back to the original 'none fell inside the requested window ... widen "
    "to [real range]' wording, and the status message named ALL THREE filters (duration + "
    "both date fields), since the date window genuinely was part of the cause this time -- "
    "confirms the split does not over-exonerate when the window really is empty. (3) Happy-"
    "path regression: test_input.json (Lex Fridman, 5 episodes) -- 5/5 pushed, no change. "
    "0 defects found, the c2545 fix holds intact, no code/README change needed. Temp test "
    "dirs /tmp/apc_test1..5 deleted after verification -- no production KV store touched. "
    "$0 spend (local Actor runs + public Apple RSS/lookup curls only)."
)

with open(P, encoding="utf-8") as f:
    d = json.load(f)

entry = d[SLUG]
assert entry.get("unreachable_remedy") == 2545, entry.get("unreachable_remedy")
old_note = entry.get("unreachable_remedy_note", "")
entry["unreachable_remedy"] = 2883
entry["unreachable_remedy_note"] = NOTE + " | PRIOR " + old_note

with open(P, "w", encoding="utf-8") as f:
    json.dump(d, f, indent=2, ensure_ascii=True)
    f.write("\n")

print("wrote", P)
