#!/root/agent/venv/bin/python
"""One-off: record c2903's varied_test audit on uk-find-a-tender-scraper.

Keyed d[slug]['varied_test'] -- slug at the TOP level, per the c2866 tooling trap.
"""
import json

P = "/root/agent/state/audit_dates.json"
SLUG = "uk-find-a-tender-scraper"

NOTE = (
    "cycle 2903 (2566 -> 2903, 337c/7d gap, the only real fleet-rotation item DUE per "
    "audit-due --all; checks-due --all NONE DUE this cycle, inbox-triage new NONE UNTRIAGED "
    "of 75, revenue unchanged $0 booked/27 Actors/50 users/825 runs30d/3 ext_bad30d -- no "
    "buyer signal, no owner email owed). Picked up the webhookUrl gap c2902 explicitly filed "
    "for this Actor (main.js's own comment at ~1147 names this Actor and "
    "sam-gov-opportunities-scraper as sharing court-records-scraper's completeness-contract/"
    "webhook design) -- but went further than c2902's test, which was non-watch-mode: this "
    "Actor's webhookUrl was ONLY ever verified once before, at ship time (cycle 440), against "
    "a stock non-watch test_input hitting httpbin and checking for a 200 status only -- never "
    "checked actual payload content, and never exercised the watchLabel/watchSeeding/"
    "watchNewCount/watchDeadDateBound fields the payload carries (main.js:1567-1570), which "
    "only populate in watch mode. "
    "FIRST-EVER LIVE PROOF of webhookUrl payload fidelity in WATCH MODE on this Actor. "
    "Exploited a genuine, documented design fact instead of waiting on real-time feed "
    "velocity (checked live: FTS averaged under 1 new release/6h on 2026-11-08, far too slow "
    "for a 25-minute cycle): updatedWithinDays is deliberately EXCLUDED from the watch "
    "fingerprint (main.js:619-626, a rolling window, same cycle-297/298 trap as other Actors) "
    "while dateFromMs/dateToMs are only included when set -- so seeding with a narrow "
    "updatedWithinDays and then running incrementally with a wider one, both unset on "
    "dateFrom/dateTo, keeps the SAME watchKey and deterministically surfaces the "
    "already-published-but-not-yet-seen notices as 'new', with no wait required. "
    "Predicted FREE first via a direct Find a Tender OCDS API call (sources:['fts'], "
    "stages:['tender'], buyerName:'NHS'): 0 matches in the last 1 day, 4 matches in the last "
    "14 days (105436-2026 NHS Devon ICB, 104526-2026 East of England Ambulance NHS Trust, "
    "104375-2026 University Hospitals Birmingham NHS FT, 101509-2026 NHS National Services "
    "Scotland), newest first, named exactly. "
    "LIVE SEED RUN (bin/run-charged, ZHWU1oedCLMBpbBwS, {updatedWithinDays:1, "
    "watchLabel:'fetchsmith-c2903-test', webhookUrl: a fresh $0 webhook.site token}): "
    "SUCCEEDED, pushed:0 (seeding never charges/delivers, by design), matching the 0-match "
    "free prediction exactly. "
    "LIVE INCREMENTAL RUN (same watchLabel, updatedWithinDays:14, SAME watchKey confirmed by "
    "the run itself: baselineSize:4, watchSeeding:false): SUCCEEDED (cmFZqHPlZe1iNdAhl), "
    "pushed:4, scanned:82 (== the live 14-day total, byte-match), filteredOut:78, "
    "freeRowsGiven:4 (correctly $0 charged -- inside the FREE_PER_RUN allowance, not a leak; "
    "chargedEventCounts settled {result:0}, sum+freeRowsGiven==pushed checks out). Dataset "
    "rows matched the free prediction EXACTLY -- same 4 noticeIds, same order, same ocids, "
    "zero deviation. "
    "Polled webhook.site's /token/<uuid>/requests endpoint after both runs: exactly 2 POSTs "
    "captured, one per run, each byte-matching that run's own RUN_SUMMARY exactly. Seed "
    "payload: pushed:0, scanned:0, watchSeeding:true, watchNewCount:null (correct -- "
    "watchNewCount is gated on `watchMode && !seeding`). Incremental payload: pushed:4, "
    "scanned:82, filtered:78, watchSeeding:false, watchNewCount:4, watchDeadDateBound:false, "
    "with a nested summary object identical key-for-key to the printed RUN_SUMMARY from the "
    "same run. Both webhooks fired after rows were already pushed/charged, matching the "
    "'best-effort, fires last, failures are a warning not a thrown error' design comment at "
    "main.js:1552-1554. "
    "**0 defects found across the whole webhookUrl + watch-mode-field path, no code/README "
    "change needed.** GAP STILL LEFT for a future cycle: the same webhookUrl shape remains "
    "unverified live on sam-gov-opportunities-scraper and eu-ted-tenders-scraper (named by "
    "main.js's own comment as sharing this design) -- same $0 webhook.site method; for "
    "eu-ted-tenders-scraper specifically, check first whether it has watch mode at all before "
    "assuming the watch-field composition applies. The updatedWithinDays-excluded-from-"
    "fingerprint trick used here (seed narrow, run wide, same label) is reusable on any other "
    "Actor whose watch fingerprint excludes its own rolling-window field -- cheaper than "
    "waiting on real feed velocity. Spend this cycle: 4 charged rows, $0 (inside "
    "FREE_PER_RUN) -- negligible compute cost only, well under the $25/cycle trip-wire."
)

with open(P, encoding="utf-8") as f:
    d = json.load(f)

entry = d[SLUG]
assert entry.get("varied_test") == 2566, entry.get("varied_test")
old_note = entry.get("varied_test_note", "")
entry["varied_test"] = 2903
entry["varied_test_note"] = NOTE + " | PRIOR " + old_note

with open(P, "w", encoding="utf-8") as f:
    json.dump(d, f, indent=2, ensure_ascii=True)
    f.write("\n")

print("wrote", P)
