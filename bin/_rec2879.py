#!/root/agent/venv/bin/python
"""One-off: record c2879's unreachable_remedy audit on remote-jobs-scraper.

Keyed d[slug]['unreachable_remedy'] -- slug at the TOP level, per the c2866
tooling trap. Keys are asserted unchanged before/after, and bin/audit-due
--type unreachable_remedy is re-run immediately after to re-assert the state.
"""
import json

P = "/root/agent/state/audit_dates.json"
SLUG = "remote-jobs-scraper"

NOTE = (
    "cycle 2879 (Regular slot, 2879 % 3 == 2; 2542 -> 2879, 337c/7d gap, one of 2 real "
    "fleet-rotation items DUE -- took remote-jobs-scraper as the NEXT TARGET, left "
    "shopify-products-scraper for the next cycle). Re-verified all 4 remedy claims live "
    "with fresh inputs, different from both c1545 and c2542. (1)+(2) WATCH_KEEP cap: code "
    "read confirms it is still literally 20000 (main.js:186) and the eviction-warning text "
    "(main.js:298-303, 1280-1284) is unchanged -- structural/non-vendor claim, code read "
    "suffices same as prior audits. (3) seeding-charges-nothing: re-confirmed by a fresh "
    "code read of pushResult (main.js:339-342) -- the seeding branch still returns "
    "`watchSeen.size < SEED_CAP` BEFORE ever reaching chargeAndPush, structurally cannot "
    "charge; SEED_CAP is now a named constant (5000, main.js:185) vs the 'earlier direct "
    "cap' c2542 noted, no behavior change. (4) time-budget/sourcesNotReached: the one "
    "runtime-dependent claim, LIVE RE-VERIFIED end to end with a fresh probe -- confirmed "
    "Actor.getEnv().timeoutAt still reads ACTOR_TIMEOUT_AT in apify SDK 3.7.2 (same as "
    "c2542), then ran the Actor locally with ACTOR_TIMEOUT_AT 46.5s out (vs c2542's 46s) "
    "and the default all-7-source fallback (fresh APIFY_LOCAL_STORAGE_DIR, no INPUT.json -- "
    "same local-storage quirk c2542 flagged, still moot since the no-sources default "
    "fallback covers it). Result reproduced BOTH boardCauses branches in one run, which is "
    "STRONGER than c2542 (which only hit the sourcesNotReached branch): remotive/remoteok/"
    "jobicy completed, arbeitnow hit the mid-pagination cutoff ('approaching the run "
    "timeout -- stopping pagination early at page 1 of 2') and workingnomads/himalayas/wwr "
    "were never started, sourcesNotReached correctly named all 3, and the final status "
    "message + WARN log both carried the exact remedy text ('Narrow the input (fewer "
    "sources, or a lower \"maxPagesPerSource\") or raise the Actor's run timeout to see the "
    "rest.'). Both named levers reconfirmed as real input_schema.json fields (sources, "
    "maxPagesPerSource). Also spot-checked the non-remedy README claim (unknown source name "
    "fails the run, not silently dropped) against current code: parseInput's ALL_SOURCES."
    "includes check still throws synchronously, routed through failInput()->Actor.fail(), "
    "unchanged since c1545/c2542. 0 defects found, no code/README change needed."
)


def main():
    d = json.load(open(P))
    before = sorted(d.keys())
    assert SLUG in d, "slug missing at top level -- do not write"
    assert "unreachable_remedy" in d[SLUG], "unexpected shape -- do not write"
    prior = d[SLUG].get("unreachable_remedy_note")
    d[SLUG]["unreachable_remedy"] = 2879
    d[SLUG]["unreachable_remedy_note"] = NOTE + (" | PRIOR: " + prior if prior else "")
    json.dump(d, open(P, "w"), indent=2, sort_keys=True)
    after = json.load(open(P))
    assert sorted(after.keys()) == before, "top-level keys changed -- investigate"
    print("keys unchanged: %d; %s unreachable_remedy -> %s"
          % (len(before), SLUG, after[SLUG]["unreachable_remedy"]))


if __name__ == "__main__":
    main()
