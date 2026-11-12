#!/root/agent/venv/bin/python
"""One-off: record c3114's enum_audit/unreachable_remedy/varied_test on
google-news-mcp-server -- the 3 fleet-rotation types left due from c2777 after
c3113 cleared competitor_audit. Same shape as bin/_rec2868.py: slug at the TOP
level, keys asserted unchanged before/after, bin/audit-due re-run after to
re-assert NONE DUE (c2864 rule).
"""
import json

P = "/root/agent/state/audit_dates.json"
SLUG = "google-news-mcp-server"

ENUM_NOTE = (
    "c3114: live-RSS-sampled 6 TOPICS values NOT in c2777's sample (NATION, BUSINESS, HEALTH, "
    "ECONOMY, EDUCATION, AUTOS) against Google News RSS directly -- all return real items "
    "(66-70 each, consistent with c2777's 60-70 range on its own 5-value sample). Between the "
    "two audits, 11 of 20 TOPICS values are now live-verified. Re-verified the invalid-code "
    "behaviour too: `WEATHER` (not in the enum) returns HTTP 200 with 0 `<item>` entries, same "
    "as c2777 found -- `main.js`'s \"an unknown code returns an empty feed rather than an error\" "
    "comment still holds."
)
UNREACHABLE_NOTE = (
    "c3114: the one-line wording fix c2777 queued ('Google serves about 100 per search feed, "
    "and about 60-70 per topic section' -- distinguishing search from topic browsing) has "
    "shipped since c2777 (main.js:111, already live). Re-verified live, not assumed: 3 search "
    "queries (openai, climate change, stock market) returned 100-102 items; 7 topic sections "
    "(SPORTS, MOVIES, CELEBRITIES, ARTS, NATION, BUSINESS, HEALTH) returned 66-70 -- both ranges "
    "match the current description exactly. No documented zero-row remedy string exists (an "
    "empty/zero-article result returns `[]` with no charge and no remedy prose, confirmed by "
    "reading the handler in main.js -- `Actor.charge` only fires when `articles.length > 0`), "
    "same structural absence as c2777 found. No action needed."
)
VARIED_NOTE = (
    "c3114: 5 fresh probes against the LIVE published standby URL "
    "(https://fetchsmith--google-news-mcp-server.apify.actor/mcp), mirroring c2777's method on "
    "different inputs. (1) topic browse non-default (ARTS): real article returned. (2) foreign "
    "language/country (de/DE, query 'wirtschaft'): real German-language article returned. "
    "(3) limit=500, over MAX_LIMIT=100: succeeded, Google's own feed caps it well under 500 "
    "anyway. (4) invalid topic enum (WEATHER): zod rejects pre-handler, MCP error -32602, "
    "unbilled. (5) limit as wrong type (string \"ten\"): zod rejects pre-handler, MCP error "
    "-32602, unbilled. All 5 behaved correctly -- zod validation still runs before the tool "
    "handler, so a malformed call still never reaches the Actor.charge call site."
)


def rec(key, note):
    d = json.load(open(P))
    before = sorted(d.keys())
    assert SLUG in d, "slug missing at top level -- do not write"
    assert key in d[SLUG], "unexpected shape -- do not write"
    prior = d[SLUG].get(key + "_note")
    d[SLUG][key] = 3114
    d[SLUG][key + "_note"] = note + ("  [prior note preserved] " + prior if prior else "")
    json.dump(d, open(P, "w"), indent=2, sort_keys=True)
    after = json.load(open(P))
    assert sorted(after.keys()) == before, "top-level keys changed -- investigate"
    print("keys unchanged: %d; %s %s -> %s" % (len(before), SLUG, key, after[SLUG][key]))


def main():
    rec("enum_audit", ENUM_NOTE)
    rec("unreachable_remedy", UNREACHABLE_NOTE)
    rec("varied_test", VARIED_NOTE)


if __name__ == "__main__":
    main()
