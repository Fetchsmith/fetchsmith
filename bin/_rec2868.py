#!/root/agent/venv/bin/python
"""One-off: record c2868's enum_audit on app-store-reviews-scraper.

Keyed d[slug]['enum_audit'] -- slug at the TOP level, per the c2866 tooling trap
(a first attempt that cycle wrote d['enum_audit'][slug] and silently recorded
nothing). Keys are asserted unchanged before/after, and bin/audit-due --type
enum_audit is re-run immediately after to re-assert the state (c2864 rule).
"""
import json

P = "/root/agent/state/audit_dates.json"
SLUG = "app-store-reviews-scraper"

NOTE = (
    "c2868: all 4 declared `sort` values live-reproved on id=1232780281 (Notion), US "
    "storefront. Upstream vocabulary CLEAN: sortBy=mostRecent and sortBy=mostHelpful both "
    "HTTP 200 / 50 reviews and genuinely distinct (disjoint top-3 review ids). The documented "
    "vote mechanism (main.js:85-88 + README FAQ, last measured 2026-09-18) re-verified live: "
    "mostRecent carries a flat voteSum 0 on every row, mostHelpful carries real votes "
    "(4,1,14,38,16 on the first 5), so the minVoteSum/minVoteCount warning at main.js:146 is "
    "still correct and still needed. favorable/critical are client-side only (RATING_SORTS, "
    "main.js:60-62/145/419-422), never sent upstream, and the input_schema enum means Apple "
    "can never receive an unrecognised token from us -- fails CLOSED at the schema. "
    "ONE DRIFT FOUND, README-only, NOT yet shipped: README ~line 634 says Apple's "
    "mostFavorable/mostCritical 'come back as an empty feed'. Today they return HTTP 500 with "
    "a 34-byte non-JSON '<!-- Empty -->' body -- byte-identical to an arbitrary bogus token "
    "(mostFavorable, mostCritical, mostfavorable, mostcritical and bogusSort all give the same "
    "500/34 bytes). The load-bearing claim (only mostRecent/mostHelpful return entries, so "
    "rating sort must be client-side) still holds and is in fact strengthened; the mechanism "
    "sentence 'empty feed' is imprecise. Queued for a README-only build."
)


def main():
    d = json.load(open(P))
    before = sorted(d.keys())
    assert SLUG in d, "slug missing at top level -- do not write"
    assert "enum_audit" in d[SLUG], "unexpected shape -- do not write"
    prior = d[SLUG].get("enum_audit_note")
    d[SLUG]["enum_audit"] = 2868
    d[SLUG]["enum_audit_note"] = (
        NOTE + ("  [prior note preserved] " + prior if prior else "")
    )
    json.dump(d, open(P, "w"), indent=2, sort_keys=True)
    after = json.load(open(P))
    assert sorted(after.keys()) == before, "top-level keys changed -- investigate"
    print("keys unchanged: %d; %s enum_audit -> %s"
          % (len(before), SLUG, after[SLUG]["enum_audit"]))


if __name__ == "__main__":
    main()
