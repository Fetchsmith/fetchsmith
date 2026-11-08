#!/root/agent/venv/bin/python
"""One-off: record c2902's varied_test audit on court-records-scraper.

Keyed d[slug]['varied_test'] -- slug at the TOP level, per the c2866 tooling
trap. File is written with ensure_ascii=True, so a plain json.load/json.dump
round-trip is safe.
"""
import json

P = "/root/agent/state/audit_dates.json"
SLUG = "court-records-scraper"

NOTE = (
    "cycle 2902 (2564 -> 2902, 338c/7d gap, one of two real fleet-rotation items DUE per "
    "audit-due --all -- the other, varied_test: uk-find-a-tender-scraper, 2566->2902, was "
    "left DUE and not touched this cycle; checks-due had check-doc-size DUE too, recorded "
    "separately via bin/checks-due --ran (TRIM SOON on both STATUS.md and queue.md, neither "
    "TRIM DUE, no trim action taken -- regular slot, not QUALITY/GROWTH). inbox-triage new "
    "NONE UNTRIAGED of 75. revenue unchanged $0 booked/27 Actors/50 users/825 runs30d/3 "
    "ext_bad30d -- no buyer signal, no owner email owed. "
    "FIRST-EVER LIVE PROOF of the webhookUrl completion-ping field end-to-end -- every prior "
    "varied_test on this Actor (1298/1634/1970/2198/2227/2564) exercised a search/watch filter "
    "composition but never set webhookUrl, and a fleet-wide grep of audit_dates.json/"
    "LEARNINGS.md found zero prior live verification of webhookUrl on ANY Actor sharing this "
    "shape (main.js's own comment at ~1147 names sam-gov-opportunities-scraper and "
    "uk-find-a-tender-scraper as sharing the identical completeness-contract/webhook design, "
    "cycle 653/h250). Picked recordType:dockets, courts:['cand'], filedAfter=filedBefore="
    "'2024-01-10' (the exact window c2227 used for the watch-mode test, 44 known matches) + "
    "maxResults:5 + webhookUrl set to a fresh webhook.site token created this cycle via "
    "POST https://webhook.site/token ($0, no auth, no PII). Predicted FREE first via a direct "
    "CourtListener v4 search call with CL_API_TOKEN: count still 44 (byte-identical to c2227, "
    "0 drift in 338 cycles), top 5 by relevance named exactly (Govea-Aviles 5:24-mj-70024 / "
    "Application...841-846 5:24-mj-70026 / In Re Search of Cell Phone 5:24-mj-70027 / "
    "Application...Information 5:24-mj-70023 / Application...1343 4:24-mj-70022, all filed "
    "2024-01-10). LIVE RUN via bin/run-charged (87B3dTWYtchpGpJuR, SUCCEEDED): 5/5 rows pushed, "
    "chargedEventCounts settled {result:5} == 5, 0 phantom charge; dataset rows matched the "
    "free prediction EXACTLY, same order, zero deviation. Polled webhook.site's "
    "/token/<uuid>/requests endpoint after the run: exactly 1 POST captured, content-type "
    "application/json, body byte-matches the predicted payload shape from main.js:1397-1420 -- "
    "actorRunId:'87B3dTWYtchpGpJuR' (matches the real run id), defaultDatasetId:'5fckz58M4eEEdPdAa' "
    "(matches the real dataset), pushed:5, scanned:5, pages:1, totalReported:44, watchLabel/"
    "watchNewCount/watchChangedCount/watchSeeding all null (correct, no watchLabel set), and a "
    "nested summary object byte-identical to the RUN_SUMMARY bin/run-charged printed from the "
    "SAME run (same keys, same values, including complete:false/incompleteReason:'max-results'/"
    "incompleteDetail naming the exact reason). The webhook fired exactly once, after the run's "
    "rows were already pushed and charged, matching the 'best-effort, fires last' design comment "
    "at main.js:1394-1396. Also read (not live-tested, low-risk local branch) the malformed/"
    "non-http(s) webhookUrl path at main.js:144-152: try/catch around new URL(), protocol "
    "allowlist, falls back to webhookUrl=null with a log.warning and the run proceeds "
    "unaffected -- consistent with the 'failures are a warning not a thrown error' design. "
    "**0 defects found across the whole webhookUrl path, no code/README change needed.** "
    "GAP STILL LEFT for a future cycle: the same webhookUrl shape is unverified live on "
    "sam-gov-opportunities-scraper, uk-find-a-tender-scraper and eu-ted-tenders-scraper (named "
    "by main.js's own comment as sharing this design) -- same $0 webhook.site method, one "
    "Actor per slot, do not batch. Spend this cycle: 5 charged rows at $0.002/result (~$0.01), "
    "well under the $25/cycle trip-wire."
)

with open(P, encoding="utf-8") as f:
    d = json.load(f)

entry = d[SLUG]
assert entry.get("varied_test") == 2564, entry.get("varied_test")
old_note = entry.get("varied_test_note", "")
entry["varied_test"] = 2902
entry["varied_test_note"] = NOTE + " | PRIOR " + old_note

with open(P, "w", encoding="utf-8") as f:
    json.dump(d, f, indent=2, ensure_ascii=True)
    f.write("\n")

print("wrote", P)
