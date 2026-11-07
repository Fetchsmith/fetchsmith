#!/root/agent/venv/bin/python
"""One-off: record c2871's unreachable_remedy audit on court-records-scraper.

Keyed d[slug]['unreachable_remedy'] -- slug at the TOP level, per the c2866
tooling trap. Keys are asserted unchanged before/after, and bin/audit-due
--type unreachable_remedy is re-run immediately after to re-assert the state.
"""
import json

P = "/root/agent/state/audit_dates.json"
SLUG = "court-records-scraper"

NOTE = (
    "cycle 2871 (2535 -> 2871, 336c/7d gap, DUE per audit-due --all): resweep of the 5-point "
    "zero-row warning (src/main.js ~1287-1299), using genuinely fresh probes distinct from both "
    "c1313 and c2535 (different court id, different docket number, different party name). "
    "(2) unrecognised court id ('xyzfakecourt789', tested on type=o this time, prior entries "
    "used type=r) -> HTTP 200, count:0 -- still silent no-match, not rejected. "
    "(3) opinions/dockets remain genuinely separate indexes: a fresh real docket "
    "(1:26-cv-09769, Kumar v. Meta Platforms, nysd, filed today) returns count:3 on type=r "
    "(dockets) and count:0 on the identical docket_number filter against type=o (opinions) -- "
    "present in one index, absent from the other. "
    "(4) docket_number office-prefix lever still reachable on this same fresh case: "
    "'1:26-cv-09769' (with prefix) -> 3, '26-cv-09769' (without) -> 7 (broader) -- dropping the "
    "prefix still returns more matches, confirming the remedy's advice is a real lever. "
    "(5) party_name is still RECAP-docket-only: party_name=Google on type=r (dockets) returns a "
    "real filtered count (12,359); the identical filter on type=o (opinions) returns 8,338,947 -- "
    "byte-identical to the unfiltered type=o&q=* baseline (also 8,338,947) -- CourtListener "
    "still silently IGNORES party_name on the opinions index rather than erroring. "
    "(1) (ANDed filters narrowing to zero) stays structural, not separately falsifiable, same "
    "carve-out c1313/c2535 used. No drift, no code/README change needed. Calls spaced ~15s "
    "apart on the shared quota out of caution; no 429 hit this run. CL_API_TOKEN confirmed live "
    "and working throughout (owner-supplied since 2026-10-28); this axis is not blocked."
)


def main():
    d = json.load(open(P))
    before = sorted(d.keys())
    assert SLUG in d, "slug missing at top level -- do not write"
    assert "unreachable_remedy" in d[SLUG], "unexpected shape -- do not write"
    prior = d[SLUG].get("unreachable_remedy_note")
    d[SLUG]["unreachable_remedy"] = 2871
    d[SLUG]["unreachable_remedy_note"] = (
        NOTE + (" | " + prior if prior else "")
    )
    json.dump(d, open(P, "w"), indent=2, sort_keys=True)
    after = json.load(open(P))
    assert sorted(after.keys()) == before, "top-level keys changed -- investigate"
    print("keys unchanged: %d; %s unreachable_remedy -> %s"
          % (len(before), SLUG, after[SLUG]["unreachable_remedy"]))


if __name__ == "__main__":
    main()
