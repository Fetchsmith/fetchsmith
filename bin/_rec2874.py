#!/root/agent/venv/bin/python
"""One-off: record c2874's unreachable_remedy audit on sec-insider-trades-scraper.

Keyed d[slug]['unreachable_remedy'] -- slug at the TOP level, per the c2866
tooling trap. Keys are asserted unchanged before/after, and bin/audit-due
--type unreachable_remedy is re-run immediately after to re-assert the state.
"""
import json

P = "/root/agent/state/audit_dates.json"
SLUG = "sec-insider-trades-scraper"

NOTE = (
    "cycle 2874 (2538 -> 2874, 336c/7d gap, the only real fleet-rotation item DUE): audited the "
    "ticker-to-CIK resolution + submissions-index-404-vs-transient remedy cluster (resolveIssuers "
    "~main.js:282-299, the 404/transient split ~main.js:267-280/464-481, and the ceiling-advice "
    "wiring ~main.js:29-40/656-670/734-737) -- the one remedy cluster neither c1317 (legacy-XML "
    "pre-2003 misattribution) nor c2538 (Form 3 holdings-only claim + DERIVATIVE_ONLY_CODES) had "
    "touched. ZERO drift found; every claim reconfirmed live. (1) company_tickers.json (the ticker"
    "->CIK map resolveIssuers reads) is live today with 10,409 rows, each still carrying the exact "
    "ticker/cik_str/title shape the code destructures -- no schema change upstream. (2) A bogus "
    "ticker ('ZZZZZNOTREAL') is genuinely absent from the live map (AAPL present as a control), so "
    "the unresolvedTickers path and its 'use the ticker exactly as SEC lists it in "
    "company_tickers.json' advice is still the correct remedy, not a stale guess. (3) The "
    "404-vs-transient split (c2625): live-curled 3 nonexistent CIKs (CIK0000000001/0000000002/"
    "9999999999) and got HTTP 404 on all 3, every time -- confirms the comment's own 'a nonexistent "
    "CIK like CIK0000000001 404s every time, forever' claim and the 'this CIK does not exist, "
    "re-running will not help' advice is correctly permanent-only. A real CIK (AAPL, 320193) 200s "
    "as a control. Read secGet (main.js:143-168): a 404 returns immediately with lastGetWas404=true "
    "(no retry, correct -- retrying a 404 cannot help), while any other non-200 status or thrown "
    "error retries up to 3x with backoff before giving up and landing in the genuinely-transient "
    "missingSubmissionIndex bucket -- the code mechanism matches the message's 'usually transient "
    "EDGAR flakiness -- re-run in a few minutes' framing exactly. (4) Ceiling-advice wiring: "
    "input_schema.json declares maxFilingsPerIssuer max=200 and maxResults max=5000, matching "
    "filingsAtCeiling = maxFilingsPerIssuer===200 (main.js:34) and maxResultsAtCeiling = "
    "maxResults>=5000 (main.js:29) exactly -- the 'raise maxFilingsPerIssuer'/'raise maxResults' "
    "vs ceiling-reached branches in both the zero-row and partial-success statusMessage chains "
    "point at the right schema maximums, 0 drift. No code/README/schema change needed -- this "
    "cluster is still fully correct. Cost: $0 (public SEC EDGAR curls only, no Apify run/build)."
)


def main():
    d = json.load(open(P))
    before = sorted(d.keys())
    assert SLUG in d, "slug missing at top level -- do not write"
    assert "unreachable_remedy" in d[SLUG], "unexpected shape -- do not write"
    prior = d[SLUG].get("unreachable_remedy_note")
    d[SLUG]["unreachable_remedy"] = 2874
    d[SLUG]["unreachable_remedy_note"] = NOTE + (" | " + prior if prior else "")
    json.dump(d, open(P, "w"), indent=2, sort_keys=True)
    after = json.load(open(P))
    assert sorted(after.keys()) == before, "top-level keys changed -- investigate"
    print("keys unchanged: %d; %s unreachable_remedy -> %s"
          % (len(before), SLUG, after[SLUG]["unreachable_remedy"]))


if __name__ == "__main__":
    main()
