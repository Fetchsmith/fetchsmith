#!/root/agent/venv/bin/python
"""One-off: record c2896's unreachable_remedy audit on clinicaltrials-scraper.

Keyed d[slug]['unreachable_remedy'] -- slug at the TOP level, per the c2866
tooling trap. File is written with ensure_ascii=True, so a plain
json.load/json.dump round-trip is safe.
"""
import json

P = "/root/agent/state/audit_dates.json"
SLUG = "clinicaltrials-scraper"

NOTE = (
    "cycle 2896 (2560 -> 2896, 336c/7d gap; `audit-due --all` re-run fresh found TWO rotation "
    "items DUE -- this one and trademark-search-scraper, whose NEXT-TARGET priority was declined "
    "on purpose because c2894 AND c2895 both burned a full slot failing on it and c2895's own "
    "filed follow-up says do NOT retry its recipe near-term; checks-due NONE DUE, soonest "
    "check-dead-endpoint-docs in 3c; inbox 0 untriaged of 75; revenue unchanged $0 booked/27 "
    "Actors/50 users/825 runs30d/3 ext_bad30d -- no owner email owed). **REAL buyer-facing "
    "defect found and FIXED in build 0.1.100.** c1558 covered zero-row cause (3), c2560 covered "
    "cause (2); this pass took the last untouched one, cause (1) ('conditions/interventions/"
    "sponsors/locations/searchQuery are ANDed, so several narrow filters together often match "
    "nothing -- drop one and retry', main.js ~1584). The claim is TRUE but its REMEDY IS "
    "UNREACHABLE for the single most likely 0-row shape, because ClinicalTrials.gov ANDs the "
    "terms WITHIN one field too -- a fact stated nowhere in the Actor, the README or the input "
    "schema. Measured live 2026-11-08 ($0, countTotal only, no Actor runs; negative control "
    "passed first -- registry 610,756, query.cond=asthma 5,312, query.intr=metformin 3,138, "
    "both together 4, so upstream was answering normally): query.spons=`Pfizer, Moderna` = 0 "
    "while `Pfizer OR Moderna` = 6,111 (Pfizer alone 6,110); cond `melanoma, asthma` = 2 vs "
    "`melanoma OR asthma` = 9,092; intr `pembrolizumab, nivolumab` = 300 vs OR = 4,744; locn "
    "`Boston, Paris` = 1,992 (studies with a site in BOTH) vs OR = 34,551. Comma and bare space "
    "behave identically (`asthma diabetes` = `asthma, diabetes` = 106), and explicit OR works. "
    "So a buyer who typed a comma list into ONE box got 0 rows plus advice to 'drop one' filter "
    "they never set -- i.e. advice to delete their whole query, when the real fix is one word. "
    "Schema reachability per the c2555 rule: fully reachable, and the schema was actively "
    "TEACHING the comma habit -- the `locations` description's own example value is literally "
    "\"Boston, Massachusetts\" (a legitimate AND, 21,483 live). FIXED: (1) cause (1) is now "
    "rendered in whichever of three forms the input makes actionable -- comma-with-no-OR in a "
    "search box (names the field, gives the `A OR B` fix with the Pfizer/Moderna numbers), "
    ">1 field set (unchanged old 'drop one' wording), exactly 1 field set (no filter to drop, so "
    "it says check spelling / fewer words / `A OR B`); the uncapped log form always carries the "
    "full ordering plus a 'this run had a comma in <field>=<value>' line. Comma is the "
    "discriminator, NOT 'more than one word' -- a bare phrase like \"breast cancer\" is a "
    "legitimate within-field AND -- and the whole thing is scoped to pushed===0 runs, so it "
    "cannot over-fire on a comma value that works (`locations:\"Boston, Massachusetts\"` never "
    "reaches the branch). (2) input_schema descriptions for all 5 search fields now state the "
    "within-field AND + the OR form, with locations additionally explaining why its own comma "
    "example is a deliberate AND. (3) README filter table row + the 0-row FAQ answer carry the "
    "same correction with all four measured pairs. **500-char status-message cap re-verified as "
    "part of the fix, and it caught a regression of exactly the bug c1758/c2352 fixed here**: "
    "the first draft echoed `field=\"value\"` pairs into the compact message and measured 568 "
    "chars (589 with all 5 fields named), which clampStatusMessage would have cut -- silently "
    "deleting cause (3) again. Final form names ONE field and no values; all 5 branches "
    "re-measured by executing the real source lines verbatim in node against a 7-digit `scanned`: "
    "469/474/471/464/443 chars, every one under 500 with cause (3) present (26 chars spare in the "
    "worst case). Verified live post-build on 0.1.100 via a real `apify call`: trap input "
    "{\"sponsors\":\"Pfizer, Moderna\"} fired the new comma branch in both log and status message, "
    "0 rows so $0 charged; happy-path test_input.json unregressed (12/12 rows, same 'Incomplete: "
    "12 row(s) of 205 declared' message c1558/c2560 recorded). Guards clean: node --check, "
    "check-zero-row-message (2 branches, 0 MISS), check-charges (1 priced, 0 drift), "
    "check-filter-reach (0 unreachable), check-registry-fields (0 drift), check-code-fields (0 "
    "drift), check-doc-size OK. Live README confirmed byte-identical to local via the build's "
    "`readme` field (73,308 bytes, all 4 new passages present) and all 5 schema descriptions "
    "confirmed live in actorDefinition.input. README says 'As of v0.1.100' (the build the "
    "behaviour shipped in); README-only re-push landed as 0.1.101, 2 pushes total this cycle."
)

with open(P, encoding="utf-8") as f:
    d = json.load(f)

entry = d[SLUG]
assert entry.get("unreachable_remedy") == 2560, entry.get("unreachable_remedy")
old_note = entry.get("unreachable_remedy_note", "")
entry["unreachable_remedy"] = 2896
entry["unreachable_remedy_note"] = NOTE + " | PRIOR " + old_note

with open(P, "w", encoding="utf-8") as f:
    json.dump(d, f, indent=2, ensure_ascii=True)
    f.write("\n")

print("wrote", P)
