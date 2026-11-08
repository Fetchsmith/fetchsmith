#!/root/agent/venv/bin/python
"""One-off: record c2899's varied_test audit on substack-scraper.

Keyed d[slug]['varied_test'] -- slug at the TOP level, per the c2866 tooling
trap. File is written with ensure_ascii=True, so a plain json.load/json.dump
round-trip is safe.
"""
import json

P = "/root/agent/state/audit_dates.json"
SLUG = "substack-scraper"

NOTE = (
    "cycle 2899 (2563 -> 2899, 336c/7d gap, one of two real fleet-rotation items DUE per "
    "audit-due --all; the other, unreachable_remedy: trademark-search-scraper, was DECLINED "
    "again -- c2894-c2898 already burned 5 slots on it for $0 yield and c2895's own filed "
    "follow-up says do not retry its recipe near-term, so it remains the fleet's single oldest "
    "open item. checks-due had check-dead-endpoint-docs DUE and that was closed this cycle too "
    "(1 retired endpoint 'appreviews' found in Actor source, 4 blog mentions checked, 0 "
    "undisclosed, clean -- recorded via bin/checks-due --ran, next due cycle 2923). "
    "inbox-triage new NONE UNTRIAGED of 75. revenue unchanged $0 booked/27 Actors/50 users/825 "
    "runs30d/3 ext_bad30d -- no buyer signal, no owner email owed). "
    "Closed a genuinely untested composition: requirePodcast + requirePaymentsEnabled "
    "together (discoverPublications, main.js ~767-768), never jointly exercised live by any "
    "prior varied_test on this Actor -- 2563 covered searchQuery+contentType, 2225 covered "
    "includeComments/maxCommentsPerPost/minCommentCount/postUrls, 2197 covered "
    "minReactionCount+minRestackCount+includePublicationInfo, 1969 covered "
    "leaderboardOnly+discoverCategories (podcast contentType) and found the bare-handle-redirect "
    "bug, 1633 covered isRestack+date filters, 1295 covered minWordCount+audienceFilter alone -- "
    "requirePodcast/requirePaymentsEnabled (shipped c2418, per the main.js comment at line 115) "
    "had only ever been code-reviewed/field-presence-checked, never run through a real platform "
    "call with both filters active together. "
    "METHOD, predicted FREE before any paid run (direct curl to substack.com/api/v1/category/"
    "public/podcast/all?page=0&limit=25, no key, no Apify spend): of the 25 leaderboard entries "
    "on page 0, 17 pass BOTH podcast_enabled/has_podcast AND payments_state=='enabled'; with the "
    "schema-default maxPublicationsPerCategory:10, the discoverPublications loop caps found[] at "
    "10 without a second page fetch (found.length reaches 10 at rank 15 of 25, so the "
    "`found.length < maxPublicationsPerCategory` loop condition goes false before page 1). "
    "Predicted exact ordered set (rank, name, host): (1,Letters from an American,"
    "heathercoxrichardson.substack.com), (3,Hope for America with Heather Delaney Reese,"
    "www.heatherdelaneyreese.com), (4,Blocked and Reported,www.blockedandreported.org), "
    "(5,The Warning with Steve Schmidt,steveschmidt.substack.com), (7,Lenny's Newsletter,"
    "www.lennysnewsletter.com), (8,The Jim Acosta Show,www.jimacosta.com), (10,The Fifth Column "
    "(A Podcast),www.wethefifth.com), (12,The Pragmatic Engineer,newsletter.pragmaticengineer.com), "
    "(13,The Wright Report,wrightreport.substack.com), (15,thediaryofanadultteenager,"
    "thediaryofanadultteenager.substack.com); skippedByAttr (fails either filter, counted across "
    "the full 25-entry page) = 8. "
    "LIVE RUN (bin/run-charged, {discoverCategories:['podcast'], leaderboardTier:'all', "
    "leaderboardOnly:true, requirePodcast:true, requirePaymentsEnabled:true, "
    "maxPublicationsPerCategory:10}, run YM4XoedxqiOsoeu0h, SUCCEEDED): 10 rows pushed, "
    "chargedEventCounts settled {leaderboard-row:10} == 10 pushed exactly, 0 phantom charge. "
    "Fetched the dataset and compared row-for-row: all 10 ranks, names and publicationUrls "
    "matched the free prediction EXACTLY, in the same order. ZERO deviation. "
    "**0 defects found, no code/README change needed.** Also notable but not a bug: of the 17 "
    "page-0 publications that pass both filters, 7 are silently dropped by the "
    "maxPublicationsPerCategory cap with no dedicated counter (they are neither in found[] nor "
    "skippedByAttr) -- this is the same, already-documented 'raising maxPublicationsPerCategory "
    "will not help once the leaderboard page is exhausted' cap behavior every other discover "
    "filter shares, not a new gap specific to this combination. node --check not run (no edit "
    "made); check-charges/check-registry-fields not re-run (pure verification, 0 diff, no build "
    "owed). Spend: 10 leaderboard-row charges, well under $0.01, well under the $25/cycle "
    "trip-wire. GAP STILL LEFT for a future cycle (per 2563's own note, carried forward): the "
    "null-on-failure commentDepth path, and splitExhausted-style interactions with watchChanges "
    "on OTHER Actors noted at c2898, remain unexercised; on substack-scraper specifically, "
    "maxWordCount alone (only ever tested paired with minWordCount) and includeBodyText/"
    "includeBodyHtml composed with contentType='podcast' are still untested."
)

with open(P, encoding="utf-8") as f:
    d = json.load(f)

entry = d[SLUG]
assert entry.get("varied_test") == 2563, entry.get("varied_test")
old_note = entry.get("varied_test_note", "")
entry["varied_test"] = 2899
entry["varied_test_note"] = NOTE + " | PRIOR " + old_note

with open(P, "w", encoding="utf-8") as f:
    json.dump(d, f, indent=2, ensure_ascii=True)
    f.write("\n")

print("wrote", P)
