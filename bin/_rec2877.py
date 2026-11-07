#!/root/agent/venv/bin/python
"""One-off: record c2877's unreachable_remedy audit on uk-find-a-tender-scraper.

Keyed d[slug]['unreachable_remedy'] -- slug at the TOP level, per the c2866
tooling trap. Keys are asserted unchanged before/after, and bin/audit-due
--type unreachable_remedy is re-run immediately after to re-assert the state.
"""
import json

P = "/root/agent/state/audit_dates.json"
SLUG = "uk-find-a-tender-scraper"

NOTE = (
    "cycle 2877 (QUALITY/GROWTH slot, 2877 % 3 == 0; 2541 -> 2877, 336c/7d gap, the only real "
    "fleet-rotation item DUE): re-walked the 5-cause zeroRowMessage block (main.js ~1263-1332) "
    "with fresh live probes against both portals, different inputs than c1544/c2541 (14-day "
    "window ending 2026-11-07 instead of 2026-10/09-28/31). Causes (1)/(2)/(4) STILL ACCURATE: "
    "(1) tender.classification.description (cpvDescription) populated on 82/82 fresh FTS "
    "tender-stage releases (window 2026-10-24..11-07) incl. 5 distinct real descriptions "
    "('IT services: consulting, software development...', 'Community health services', ...) -- "
    "the 5-field TEXT_FIELDS haystack claim holds; (2) 0 non-8-digit CPV ids across all 82 "
    "releases (tender- and item-level classification), cpvPrefixes trailing-zero matching "
    "unchanged; (4) updatedWithinDays monotonic growth reconfirmed on FTS tender-stage: 8 rows "
    "(1-day) -> 41 (7-day) -> 82 (14-day). Cause (3) tender-side reconfirmed (81/82 FTS "
    "tender-stage releases carry a FUTURE tenderPeriod.endDate, 1 past as noise -- matches "
    "1544/2541's near-100% finding); the CF award-side half of cause (3) and the portal-volume "
    "half of cause (5) could NOT be independently re-measured this cycle -- see the real finding "
    "below, which made CF unsafe to keep probing. No code/README change from causes (1)/(2)/(3)/(4).\n\n"
    "REAL DRIFT FOUND AND FIXED (unrelated to the 5 causes, found while probing for them): "
    "Contracts Finder's live API answered a rapid probe sequence with the EXACT SAME 429 body "
    "FTS's own code comment documents only for FTS -- 'Rate limit of 12 exceeded. Please retry "
    "after 120 seconds.' -- but main.js:361 (pre-fix) set CF's self-throttle to rateMax: 20, "
    "above the live 12-request limit. Verified live: 6 back-to-back CF requests to the same "
    "endpoint drew 429 with that literal body and a `retry-after: 120` header. Fixed by setting "
    "CF's rateMax to 10 (main.js, matching FTS's existing proven-safe margin under 12) and "
    "correcting both source comments to document the shared limit instead of attributing it to "
    "FTS alone. Shipped as build 0.1.103 (package.json 0.1.25, unchanged -- no output-field "
    "change). Live platform smoke test on 0.1.103 (run-sync-get-dataset-items, "
    "stages:['tender'], updatedWithinDays:7, maxResults:5): HTTP 201, 5 real rows delivered "
    "(e.g. noticeId 105838-2026, 'Retail Data Management, Analytics and Automation', published "
    "2026-11-06) -- no regression. A first narrower smoke test (searchQuery:'road maintenance') "
    "legitimately returned 0 and was not mistaken for a bug.\n\n"
    "SEPARATE, NOT YET FIXED -- flagged as the top queue item for next cycle: while probing CF "
    "under the same load that produced the 429 above, it ALSO returned, several times, an HTTP "
    "200 with a well-formed OCDS envelope, an EMPTY `releases: []`, and its own echoed `uri` "
    "field silently missing the `publishedFrom`/`stages` params that were actually sent (and "
    "`limit` clamped to 100 regardless of what was requested) -- i.e. a soft-degrade tier that "
    "looks exactly like a legitimate zero-row response with no error signal at all, sitting "
    "below the hard 429 tier. Reproduced 3+ times today (2026-11-07), always after recent CF "
    "traffic (my own probes, and once right after the 0.1.103 smoke-test run), never on a cold "
    "first request. fetchPage() (main.js ~806-898) only branches on statusCode (200/429/other) "
    "and then trusts any 200 body as real data -- it has no detection for this signature, so a "
    "real buyer run that hit it mid-pagination would see a confident but WRONG zeroRowMessage "
    "('no notices matched: causes are field/CPV/stage/window/sources') instead of a retry. Not "
    "fixed this cycle (time-boxed, and fixing it safely needs a cooldown period free of my own "
    "test traffic to confirm the exact trigger threshold without further hammering the live "
    "portal). Suggested fix for next cycle: in fetchPage, after a 200, check whether the parsed "
    "body's own `uri` field contains the `publishedFrom`/`stages` params the request actually "
    "sent (or just check `releases.length === 0 && !resp.body.includes('publishedFrom')` when "
    "publishedFrom was set) and treat that as retry-eligible like a 429, not a trusted result. "
    "No code changed for this part -- documentation only, in this note and queue.md."
)


def main():
    d = json.load(open(P))
    before = sorted(d.keys())
    assert SLUG in d, "slug missing at top level -- do not write"
    assert "unreachable_remedy" in d[SLUG], "unexpected shape -- do not write"
    prior = d[SLUG].get("unreachable_remedy_note")
    d[SLUG]["unreachable_remedy"] = 2877
    d[SLUG]["unreachable_remedy_note"] = NOTE + (" | PRIOR: " + prior if prior else "")
    json.dump(d, open(P, "w"), indent=2, sort_keys=True)
    after = json.load(open(P))
    assert sorted(after.keys()) == before, "top-level keys changed -- investigate"
    print("keys unchanged: %d; %s unreachable_remedy -> %s"
          % (len(before), SLUG, after[SLUG]["unreachable_remedy"]))


if __name__ == "__main__":
    main()
