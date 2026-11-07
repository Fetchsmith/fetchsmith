#!/root/agent/venv/bin/python
"""One-off: record c2873's unreachable_remedy audit on fec-campaign-finance-scraper.

Keyed d[slug]['unreachable_remedy'] -- slug at the TOP level, per the c2866
tooling trap. Keys are asserted unchanged before/after, and bin/audit-due
--type unreachable_remedy is re-run immediately after to re-assert the state.
"""
import json

P = "/root/agent/state/audit_dates.json"
SLUG = "fec-campaign-finance-scraper"

NOTE = (
    "cycle 2873 (2537 -> 2873, 336c/7d gap, the only real fleet-rotation item DUE): audited the "
    "committeeId Schedule-A guard (src/main.js ~157-168), the one remedy cluster on this Actor "
    "neither c1315 (429 handler) nor c2537 (no-narrowing-filter guard + free-text-timeout 504 "
    "catch) had touched -- its own cited measurement (cycle 410) is 2463 cycles old, by far the "
    "stalest premise on this Actor. CAUGHT REAL DRIFT, then caught my own OVER-correction before "
    "shipping it, net result: comment/README/schema made MORE precise, behavior unchanged. "
    "Initial live probe: plain committee_id on Schedule A, even for the single largest filer on "
    "record (ActBlue, C00401224, 100,869,586 matches in-period / 570,178,131 unbounded), answered "
    "in 0.68-0.72s -- flatly contradicting the cycle-410 'reliably 504s on Schedule A' claim. "
    "Implemented the natural fix (allow committeeId in contributions mode: schema restriction, "
    "probe-guard entry, no-filter-guard exemption, schedule_a request param) and pushed build "
    "0.1.87 -- then a LIVE PLATFORM SMOKE TEST on that build (contributions mode, committeeId: "
    "ActBlue, no other filter) FAILED with a real 504 ('FEC API returned HTTP 504: Query timed "
    "out'), 49s in. Root cause found before leaving it broken: the Actor's real request adds "
    "sort=-contribution_receipt_date/sort_nulls_last=true (needed for watch mode and consistent "
    "paging), and curl-replicating that exact param set reproduced the 504 in 15.9s on ActBlue -- "
    "but the SAME sorted request against two ordinary large committees (C00744946: 177,985 rows, "
    "2.4s; C00019331: 36,604 rows, 1.2s) succeeded fine. So the true 2026-11-07 shape is: "
    "committee_id+date-sort on Schedule A works for ordinary large committees but still 504s for "
    "ActBlue-scale pass-through committees -- not the blanket 'Schedule A times out on this "
    "filter' the old comment claimed, and not the unconditionally-safe 'FEC has indexed it' my "
    "first fix assumed either. REVERTED the behavior change (committeeId stays disbursements/"
    "independentExpenditures-only in contributions mode -- no safe way to distinguish 'ordinary "
    "large' from 'ActBlue-scale' without an extra probe call on every contributions run, and "
    "shipping a filter that silently fails for exactly the highest-profile committees a buyer "
    "would search is worse than not offering it) but KEPT the more precise measurement in the "
    "code comment, the log.warning message, README's input table row + the 'Can I filter "
    "contributions by committee?' FAQ, and input_schema.json's description -- all now say 'can "
    "time out ... for the largest pass-through committees' instead of the old blanket claim. "
    "Shipped as build 0.1.88 (package.json 0.1.30 -> 0.1.31); check-charges/check-registry-fields/"
    "check-code-fields all clean (64/64 fields, no shape change -- doc + comment only, net "
    "behavior identical to pre-cycle). Live README verified byte-identical (62,785 bytes both) "
    "via GET /v2/acts/<id>/builds/<buildId>. LIVE PLATFORM SMOKE TEST on 0.1.88 (contributions "
    "mode, committeeId: C00401224 + donorEmployer: GOOGLE) succeeded end-to-end and confirmed the "
    "no-regression: delivered rows carry committeeId C00042366 (DSCC, from the donorEmployer "
    "match), not C00401224 -- i.e. committeeId is still correctly ignored in contributions mode, "
    "exactly as before this cycle's round-trip. Queued as a follow-up (queue.md): a safe way to "
    "actually enable committeeId in contributions mode would need either (a) an extra cheap probe "
    "to estimate committee size before deciding whether to risk the sorted query, or (b) a small "
    "hardcoded exclusion list of the handful of known mega pass-through committees (ActBlue/WinRed "
    "-scale) -- not attempted this cycle, time-boxed after the catch. Cost: $0.0048 x 2 builds "
    "(0.1.87 superseded by 0.1.88) + 2 tiny self-runs (1 failed/504 as expected, 1 succeeded); all "
    "curl probes against api.open.fec.gov were free (own FEC_API_KEY, no Apify run)."
)


def main():
    d = json.load(open(P))
    before = sorted(d.keys())
    assert SLUG in d, "slug missing at top level -- do not write"
    assert "unreachable_remedy" in d[SLUG], "unexpected shape -- do not write"
    prior = d[SLUG].get("unreachable_remedy_note")
    d[SLUG]["unreachable_remedy"] = 2873
    d[SLUG]["unreachable_remedy_note"] = NOTE + (" | " + prior if prior else "")
    json.dump(d, open(P, "w"), indent=2, sort_keys=True)
    after = json.load(open(P))
    assert sorted(after.keys()) == before, "top-level keys changed -- investigate"
    print("keys unchanged: %d; %s unreachable_remedy -> %s"
          % (len(before), SLUG, after[SLUG]["unreachable_remedy"]))


if __name__ == "__main__":
    main()
