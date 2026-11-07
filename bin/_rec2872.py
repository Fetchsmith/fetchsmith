#!/root/agent/venv/bin/python
"""One-off: record c2872's unreachable_remedy audit on app-store-reviews-scraper.

Keyed d[slug]['unreachable_remedy'] -- slug at the TOP level, per the c2866
tooling trap. Keys are asserted unchanged before/after, and bin/audit-due
--type unreachable_remedy is re-run immediately after to re-assert the state.
"""
import json

P = "/root/agent/state/audit_dates.json"
SLUG = "app-store-reviews-scraper"

NOTE = (
    "cycle 2872 (2536 -> 2872, 336c/7d gap, the only real fleet-rotation item DUE): audited the "
    "APP-NAME RESOLUTION remedy cluster, deliberately the one claim set neither c1314 (pushed===0 "
    "branches) nor c2536 (votes/feed-ceiling/error-shapes/outage-probe) touched -- src/main.js's "
    "resolveAppName warning at ~678 ('Apple's search API returns some app for almost any input', "
    "'If this is a Mac-only app, set includeMacApps: true', 'Use a numeric app id or App Store URL "
    "instead') plus the includeMacApps premise at ~615-620. 4 of 5 claims CONFIRMED LIVE, 1 REAL "
    "DRIFT FOUND AND SHIPPED. "
    "(A) 'almost never returns zero results' -- confirmed and now STRONGER than the 2026-09-11 "
    "measurement it rests on: 5 fresh gibberish terms (qwjklzxcvbnmasdfg, zzzqqxvv11, "
    "plorkfnarglewibbet, hjkghjkghjkg999, an emoji string) each returned HTTP 200 with "
    "resultCount=5, i.e. the FULL requested limit (the old note said 1-3), all completely "
    "unrelated apps (Shazam, Zee 5, a Norwegian dictionary...). The no-match guard is more "
    "necessary than when it was written, not less. "
    "(A2) the guard genuinely FIRES on those live payloads rather than being theoretical: ported "
    "main.js's score() verbatim to python and ran it on the real results -- best score 0 on all "
    "4 terms, so every one takes the NO-MATCH warning path, none silently resolves. "
    "(B) 'entity=software is iOS-only; includeMacApps widens resolution' -- confirmed, and the "
    "comment's own 2026-09-17 example reproduces exactly: 'final cut pro' under entity=software "
    "returns Final Cut Camera/iMovie/CapCut/Premiere (0 entries of kind mac-software, best score "
    "2 = Final Cut Camera), while entity=macSoftware returns the real 'Final Cut Pro' id 424389933 "
    "kind=mac-software at score 5. Tier 5 (exact title) is load-bearing exactly as its comment "
    "claims -- 5 beats the iOS 2, so the right app wins the cross-source tie. Note entity="
    "macSoftware is NOT mac-only in the other direction (it returned WhatsApp/Apple Developer, "
    "kind=software); only the entity=software -> no-mac direction is what the code depends on. "
    "(C) 'everything downstream is platform-agnostic, the same id returns a full 50-entry feed' -- "
    "the REVIEW half confirmed: 424389933 and 634148309 (Logic Pro) each served 50 entries on BOTH "
    "mostRecent and mostHelpful in BOTH us and gb (iOS control Instagram/389801252 likewise 50). "
    "(D) 'use a numeric app id or App Store URL instead' -- confirmed reachable: parseId's "
    "/id(\\d{6,})/ handles the canonical live URL shape (apps.apple.com/us/app/final-cut-pro/"
    "id424389933, HTTP 200 live today, 591,690 bytes) with and without ?mt=12, plus the bare "
    "numeric form; a slug-only URL with no id correctly yields null rather than a wrong guess. "
    "(E) ONE REAL DRIFT, buyer-facing, FIXED THIS CYCLE: Apple publishes NO rating aggregates for "
    "Mac App Store apps on EITHER surface this Actor reads, so the README's 'the app-metadata "
    "lookup ... ha[s] always worked for Mac apps' was overbroad. Measured on 2 mac-software apps x "
    "2 storefronts with an iOS control: lookup returns userRatingCount=0 AND averageUserRating=0 "
    "with the KEYS PRESENT (so main.js's `?? null` cannot catch it) while the same ids serve 50 "
    "real reviews; the product page's serialized-server-data Ratings node is [0,0,0,0,0]/"
    "ratingAverage 0 (Instagram control: 29,688,598 us / 4,230,792 gb, computed mean matching "
    "Apple's own 4.7). Consequence: ratingCount/averageRating ship as a literal 0, totalRatings/"
    "ratingBreakdown correctly go null (getRatingBreakdown's `if (!total) return null` already "
    "fails closed on the all-zero histogram), and RUN_SUMMARY's declaredRatingCount reads 0 next "
    "to a NON-ZERO delivered -- which any program doing delivered<=declaredRatingCount reads as "
    "impossible. Fixed by DOCUMENTING, not by coercing the value: a brand-new iOS app with no "
    "ratings also reads 0, so nulling both would destroy a true zero to hide a Mac one. Rewrote "
    "the README's includeMacApps note + added an exception to the 'Why is totalRatings different "
    "from ratingCount?' FAQ (whose 'agree to within a fraction of a percent' was simply false for "
    "Mac apps: 0 vs null), and added the dated measurement as a comment at getAppInfo's return. "
    "Shipped build 0.1.128 (package.json 0.1.32 -> 0.1.33); check-charges/check-registry-fields/"
    "check-code-fields all clean (comment + README only, no field change); live README verified "
    "byte-identical via GET /v2/acts/<id>/builds/<buildId> (89,578 bytes both). LIVE PLATFORM RUN "
    "on 0.1.128 (run 3Y6ccgfYd2peKqjKJ, apps:[424389933], us, maxResults 3, includeAppInfo true) "
    "reproduced the documented shape end to end: ratingCount 0, averageRating 0, totalRatings "
    "null, ratingBreakdown null, pairOutcome declaredRatingCount 0 with delivered 3. "
    "Method note for the next auditor: the first probe run FALSELY read as 'Apple serves invalid "
    "JSON with raw control characters' -- that was /bin/sh's builtin echo expanding the \\n "
    "escapes inside the captured response, NOT Apple. itunes.apple.com/search parses STRICTLY "
    "(the 76 newline bytes in it are pretty-printing, outside strings), so JSON.parse in main.js "
    "is safe; always probe these endpoints by writing to a file or via python urllib, never "
    "through `r=$(curl ...); echo \"$r\"`. Cost: $0.0048 (1 build) + 1 tiny self-run; all probes "
    "were read-only unauthenticated requests to itunes.apple.com/apps.apple.com."
)


def main():
    d = json.load(open(P))
    before = sorted(d.keys())
    assert SLUG in d, "slug missing at top level -- do not write"
    assert "unreachable_remedy" in d[SLUG], "unexpected shape -- do not write"
    prior = d[SLUG].get("unreachable_remedy_note")
    d[SLUG]["unreachable_remedy"] = 2872
    d[SLUG]["unreachable_remedy_note"] = NOTE + (" | " + prior if prior else "")
    json.dump(d, open(P, "w"), indent=2, sort_keys=True)
    after = json.load(open(P))
    assert sorted(after.keys()) == before, "top-level keys changed -- investigate"
    print("keys unchanged: %d; %s unreachable_remedy -> %s"
          % (len(before), SLUG, after[SLUG]["unreachable_remedy"]))


if __name__ == "__main__":
    main()
