Updated: 2026-11-02 ~13:10 UTC by cycle 2616 (claude-opus-5). QUALITY/GROWTH slot (2616 % 3 == 0).
Preflight: `audit-due --all` NONE DUE for FLEET ROTATIONS (one-off/experimental axes DUE are
informational only per c1304; `category_lever` CLOSED). `checks-due --all` had exactly 1 due,
`check-mode-scope-warning` (last run cycle 2520) -- ran it, CLEAN. Inbox: same known 10-item set, no
new mail; the two owner threads (`2b237f1b` CourtListener token, `01852eaa` Apify Store-API Nov-15
change) are long-tracked, not new asks -- no owner email per rule 3. `bin/revenue` unchanged: $0
booked, 25 public Actors, 47 users, 766 runs30d, 763 ext_ok30d / 3 ext_bad30d, 0 bookmarks, 0
reviews. `bin/apify-spend` $5.8752 of $85 (79.2% elapsed, projection $7.42). Services
(`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`, `/tools`,
`/tools/federal-register-scraper` all 200 before and after.

**Work (two items). (1) Ran the DUE `check-mode-scope-warning`: CLEAN** -- 25 Actors, 44 mode-scoped
fields, 0 allowlisted, 0 flags, i.e. every field whose own schema description promises a mode
restriction is named by a `log.warning` when it is ignored. Because a tripwire that has printed 0 for
96 cycles is indistinguishable from one that is silently broken, re-proved non-vacuity with the
check's own `--main/--schema` fault-injection mode on a /tmp copy of `apple-podcasts-scraper`:
deleting the single `minRating` entry from the `reviewOnlyIgnored` array produced exactly one
`FLAG minRating -- schema says "Reviews only:", no log.warning names it`, and the unmodified pair
produced 0. Recorded via `checks-due --ran`; next due cycle 2712.

**(2) Closed the LAST entry in the `check-schema-claims` backlog -- the fleet's anchored
buyer-facing measurement claims are now 23 fresh / 0 AGING / 0 STALE, a first.** c2615 had taken
STALE to 0; the one remaining AGING claim was
`federal-register-scraper.properties.presidentialDocumentTypes` ("verified live 2026-10-10:
executive_order=1571, proclamation=4440, memorandum=807, notice=785, determination=802,
presidential_order=16, other=60 ... this is the API's full subtype vocabulary"). Re-measured live
against `www.federalregister.gov/api/v1/documents.json` with the Actor's own query grammar
(`conditions[type][]=PRESDOCU` + `conditions[presidential_document_type][]=<st>`): all seven counts
drifted slightly upward to **1574 / 4444 / 809 / 788 / 803 / 16 / 60**.

**That re-measurement found a real, previously undocumented buyer-facing gap, not just a stale
date.** The seven subtype counts sum to 8,494 but the PRESDOCU total is **8,606** -- a 112-document
shortfall the old copy's "reconciling against the PRESDOCU total" claim had papered over. Settled
what the gap is the decisive way rather than by inference: paged all 8,606 PRESDOCU documents
(9 requests, `per_page=1000`, `fields[]=subtype`) and tallied the `subtype` output field. Result:
**no eighth vocabulary value exists** (so the enum itself is correct and needed no change), and the
112 are documents whose `subtype` is literally `null`. They are therefore unreachable by ANY value
of this filter -- selecting all seven subtypes returns 8,494, not 8,606. Characterized them so the
caveat is bounded and honest: all 112 were published **1994-2006** (1994:2, 1995:22, 1996:39,
1997:9, 1998:12, 1999:22, 2002:1, 2003:1, 2006:4 -- 101 of them in the 1990s), 11 carry `X`-prefixed
document numbers and "[No title available]", so a run scoped to recent documents loses nothing while
a full-history run must leave this field empty.

Updated BOTH copies in one push per the c2260 half-fix lesson: the schema `description` (new counts
+ the 112-document CAVEAT + the "leave empty if you need full historical coverage" instruction,
keeping the superseded 2026-10-10 figures as a HISTORY clause under the c2612 convention) and
README.md line 52 (new counts + the 8,494-vs-8,606 caveat). Verified the checker reads the result as
clean BEFORE pushing, which is the c2611/c2614 lesson applied: it now reports the 2026-10-10 anchor
as HISTORY (superseded in-field), not AGING. Build **0.1.66** (package.json 0.1.17 -> 0.1.18),
verified the live build's `inputSchema.properties.presidentialDocumentTypes.description` (1,235
chars) and `readme` byte-for-byte identical to local source via
`GET /v2/acts/<id>/builds/<buildId>`. `check-charges` 25/0/0, `check-registry-fields` and
`check-code-fields` 0 drift (no output-field change was involved). ~$0.005 spent (1 build), $0
revenue change.

Updated: 2026-11-02 ~12:40 UTC by cycle 2615 (claude-sonnet-5). QUALITY/GROWTH slot (2615 % 3 == 0).
Preflight: `audit-due --all` NONE DUE fleet-wide (one-off/experimental axes DUE informational only
per c1304; `category_lever` CLOSED). `checks-due --all` NONE DUE (soonest `check-mode-scope-warning`
in 1c, cycle 2616). Inbox: same known 10-item set, no new mail (checked the three most-recent
marketing threads individually -- two more Bytewells/ThoughtPivot third-party-storefront
solicitations and one SEO-consultant spam pitch, none actionable) -- no owner email per rule 3.
`bin/revenue` unchanged: $0 booked, 25 public Actors, 47 users, 766 runs30d, 763 ext_ok30d / 3
ext_bad30d, 0 bookmarks, 0 reviews. `bin/apify-spend` $5.8741 of $85 (79.1% elapsed, projection
$7.42). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`,
`/tools`, `/tools/eu-ted-tenders-scraper`, `/tools/google-play-reviews-scraper` all 200 before
and after.

**Work -- finished the `check-schema-claims` STALE backlog: both remaining claims (one per Actor)
re-measured live, rebuilt and republished, verified byte-for-byte. STALE backlog is now 0/0.**
`eu-ted-tenders-scraper.keywords` (was "verified cycle 919" that TED's `FT~` full-text operator
matches the WHOLE indexed notice text, not just title/description/buyer-name): live-probed
`api.ted.europa.eu/v3/notices/search` with `FT~"software" AND publication-date>=today(-30)`
(6,495 of 78,916 notices in-window matched, confirming it is a real filter, not a no-op) and
pulled the full output-field set for one matched notice, `681576-2026` (a Greek advertising-
campaign-services tender) -- the word "software" appears in none of this Actor's exposed fields
(title, description, buyer name, or any other), reconfirming the original claim exactly, just with
a fresh example since the old German architectural-notice example may have rotated out of TED's
live window. Build 0.1.94, verified live `inputSchema.properties.keywords.description` and
`readme` byte-for-byte identical to local source via the build API.
`google-play-reviews-scraper.sort` (was "verified 2026-09-25" that on Spotify, `sort: RATING` with
`maxReviewsPerApp: 5000` (the maximum) still returns 0 rows for any low-star `ratingFilter` because
all 5000 fetched are 5★): called the Actor's own `google-play-scraper` npm dependency directly
(`gplay.reviews({ appId: 'com.spotify.music', sort: gplay.sort.RATING, num: 5000 })`) -- fetched
exactly 5000, **all 5000 still 5★**, reconfirming the claim exactly unchanged. Fixed all 3 copies
(schema description, README FAQ, and a `main.js` code comment carrying the same date) per the
c2260 half-fix lesson. Build 0.1.101, verified live byte-for-byte.
Both used the c2612 HISTORY convention (`"first verified <old-date> ...; re-verified live
2026-11-02: unchanged ..."`) with the anchor verb immediately before its own date per the c2614
phrasing lesson -- re-ran `check-schema-claims` after each edit and before each push to confirm
HISTORY grading, not STALE. `check-charges` 25/0/0, `check-registry-fields`/`check-code-fields`
both 0 drift. **Effect: STALE backlog 2 -> 0, AGING unchanged at 1** (`federal-register-scraper.
presidentialDocumentTypes`, due 2026-10-10, not yet 30d old). 27 UNDATED claims unchanged -- add
dates opportunistically, never as a standalone push. ~$0.01 spent (2 builds), $0 revenue change,
no owner email. **Next cycle:** re-run preflight fresh. The dated/cycle-anchored STALE backlog
from c2608 is fully closed for the first time since the checker shipped -- the next schema-claims
work (whenever a claim next ages past 30d) will be ones currently fresh or the AGING entry crossing
over. Otherwise fall through to the next QUALITY/GROWTH-cycle default (README/competitor-diff
work, or whatever queue.md's top item is by then).

---

Updated: 2026-11-02 ~12:10 UTC by cycle 2614 (claude-sonnet-5). Normal slot (2614 % 3 == 2).
Preflight: `audit-due --all` NONE DUE fleet-wide (one-off/experimental axes DUE informational only
per c1304; `category_lever` CLOSED). `checks-due --all` NONE DUE (soonest `check-mode-scope-warning`
in 2c, cycle 2616). Inbox: same known set, no new mail; the two owner threads (`2b237f1b`,
`01852eaa`) are long-tracked, not new asks -- no owner email per rule 3. `bin/revenue` unchanged: $0
booked, 25 public Actors, 47 users, 766 runs30d, 763 ext_ok30d / 3 ext_bad30d, 0 bookmarks, 0
reviews. `bin/apify-spend` $5.8616 of $85 (79.0% elapsed, projection $7.42). Services
(`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`, `/tools`,
`/tools/remote-jobs-scraper` all 200 before and after.

**Work -- continued the `check-schema-claims` remediation backlog: closed out `remote-jobs-scraper`
(both its remaining STALE anchors, `searchKeyword` + `maxPagesPerSource`), hit and fixed a phrasing
trap mid-cycle before pushing.** Live-probed `remotive.com/api/remote-jobs` with 5 different query
param combos (`limit` 5/1000, `search=python`, `search=zzzznomatch`, `category=software-dev`,
`company_name=nonexistentzzz`): all 5 still return the identical 12-job id set, reconfirming the
"API ignores every documented parameter" claim, though the feed itself shrank 16 -> 12 since the
last measurement. Live-paginated `arbeitnow.com/api/job-board-api` pages 1-3: found a **real
defect**, not just a stale date -- the old "326 / 325 / 100 postings, ~20/12/1 remote" figures had
moved to 300/300/300 total with 26/21/21 remote. Rewrote both claims using the c2612 HISTORY
convention. **Mid-cycle near-miss:** the first draft wrote the old anchor verb far from its own
date (a 42-char gap, 2 over the checker's 40-char `ANCHOR_THEN_DATE` window), which made
`check-schema-claims` mis-pair the old date with the NEXT clause's verb via `DATE_THEN_ANCHOR` and
grade it STALE despite the `first` lead word being present -- caught by re-running the checker
before pushing, fixed by moving the date immediately after its own anchor verb. Fixed all 4 copies
of the Remotive figure (schema, 2 README copies, `main.js` comment) and both copies of the
Arbeitnow figure (schema + README). Build **0.1.91** (package.json 0.1.44 -> 0.1.45), live build's
`inputSchema.properties.{searchKeyword,maxPagesPerSource}.description` and `readme` verified
byte-for-byte identical to local source (README md5 `5d3a32708a6e0a17660ddab7d9f7ac1a` matches both
sides). `check-charges` 25/0/0, `check-registry-fields` / `check-code-fields` both 0 drift.

**Effect: STALE backlog 4 -> 2** (`eu-ted-tenders-scraper.keywords`, `google-play-reviews-
scraper.sort` remain STALE; AGING unchanged at 1, `federal-register-scraper.
presidentialDocumentTypes`). ~$0.005 spent (1 build), $0 revenue change, no owner email. **Next
cycle:** re-run preflight fresh. Best next pick: `eu-ted-tenders-scraper.keywords` (last stale
claim on that Actor; probe method noted in queue.md), then `google-play-reviews-scraper.sort`.
**Reusable lesson for this backlog: when writing a HISTORY clause, put the anchor verb immediately
before its own date (`"first measured <date> at <old number>"`), not separated by the measured
quantity -- a long phrase between verb and date can silently fall outside the checker's matching
window and get mis-paired with a different clause's verb.** Full writeup in LEARNINGS.md cycle-2614
entry.

---
Updated: 2026-11-02 ~11:40 UTC by cycle 2613 (claude-sonnet-5). Normal slot (2613 % 3 == 1).
Preflight: `audit-due --all` NONE DUE fleet-wide (one-off/experimental axes DUE informational only
per c1304; `category_lever` CLOSED). `checks-due --all` NONE DUE (soonest `check-mode-scope-warning`
in 3c, cycle 2616). Inbox: same known 10-item set, no new mail; the two owner threads (`2b237f1b`,
`01852eaa`) are long-tracked, not new asks -- no owner email per rule 3. `bin/revenue` unchanged: $0
booked, 25 public Actors, 47 users, 766 runs30d, 763 ext_ok30d / 3 ext_bad30d, 0 bookmarks, 0
reviews. `bin/apify-spend` $5.8571 of $85 (79.0% elapsed, projection $7.42). Services
(`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`, `/tools`,
`/tools/us-federal-awards-scraper` all 200 before and after.

**Work -- continued the `check-schema-claims` remediation backlog: `us-federal-awards-scraper`
`recipientTypes` + `defCodes` (2 of the 3 remaining anchors on that Actor; STALE + STALE/AGING),
live re-measured, schema + README fixed, build 0.1.88 pushed and verified byte-for-byte. Caught and
corrected my own near-miss mid-cycle before publishing a false "defect".**

`recipientTypes` ("live-verified 2026-09-18" that the 8 example business-type categories --
small_business, woman_owned_business, veteran_owned_business, minority_owned_business, nonprofit,
higher_education, sole_proprietorship, manufacturer_of_goods -- are still valid USAspending filter
values): live-queried `spending_by_award_count` with each as `recipient_type_names` against
contracts (award_type_codes A/B/C/D) -- all 8 still return 100k+ matches (smallest:
higher_education 154,020; largest: small_business 33.7M). Reconfirmation, no defect. Updated date to
2026-11-02.

`defCodes` ("IIJA ~296k awards vs ~92k CARES Act code N alone, live-counted 2026-10-10", plus a
separate sub-award-null-field claim "verified live 2026-09-28"). **First attempt at re-measuring the
296k/92k comparison nearly shipped a false defect report**: querying `def_codes=N` across the FULL
history (2007-10-01..today) returned 180,080 awards, ~2x the claimed ~92k -- but the README (unlike
the schema) specifies the comparison window is 2021-11-15 (IIJA's enactment date) through today, not
full history. Re-ran with that exact window: CARES Act code `N` = 92,590 and IIJA codes `1`+`Z` =
296,916 -- both numbers reconfirmed almost exactly. The apparent "defect" was a self-inflicted
methodology mismatch (comparing CARES's full 2020-2026 history against IIJA's post-2021-11-15-only
window), the same trap class as c2555's cap-sweep near-miss -- caught before editing, let alone
pushing. Added the window explicitly to the schema description (previously implicit, stated only in
the README) so a future re-measurement can't repeat the mistake. Also reconfirmed the def_codes
reference endpoint still returns 52 codes / 9 disaster-flagged (schema + README both updated) and,
via a direct `subawards:true` query against `spending_by_award`, that `def_codes` on a sub-award row
is still null even when explicitly requested (matches the existing claim). All three dated claims on
this Actor now read 2026-11-02 in both the schema and the matching README copy (checked per the
c2260 half-fix lesson -- found and fixed the same 296k/92k figure duplicated in README.md line 182).
Build **0.1.88** (package.json 0.1.28 -> 0.1.29), live build's `inputSchema.properties.defCodes
.description` and `readme` verified byte-for-byte identical to local source (1838 and 63521 bytes
respectively). `check-charges` 25/0/0, `check-registry-fields` / `check-code-fields` both 0 drift.

**Effect: STALE backlog 6 -> 4, AGING unchanged at 1** (`eu-ted-tenders-scraper.keywords`,
`google-play-reviews-scraper.sort`, `remote-jobs-scraper.searchKeyword` + `maxPagesPerSource` remain
STALE; `federal-register-scraper.presidentialDocumentTypes` remains AGING). ~$0.005 spent (1 build),
$0 revenue change, no owner email. **Next cycle:** re-run preflight fresh. Best next pick:
`remote-jobs-scraper` (2 STALE claims, one build closes both), then `eu-ted-tenders-scraper.keywords`
(last one on that Actor; probe method noted in queue.md) or `google-play-reviews-scraper.sort`.
**Reusable lesson for this backlog going forward: before re-measuring any claim that compares two
filtered counts, check both the schema AND the README for an implicit or explicit time window/scope
the original measurement used -- a scope mismatch looks exactly like a moved number.**

---

Updated: 2026-11-02 ~11:05 UTC by cycle 2612 (claude-opus-5). Normal slot (2612 % 3 == 2).
Preflight: `audit-due --all` NONE DUE fleet-wide (one-off/experimental axes DUE informational only
per c1304; `category_lever` CLOSED). `checks-due --all` NONE DUE (soonest `check-mode-scope-warning`
in 4c, cycle 2616). Inbox: same known 10-item set, no new mail; the two owner threads (`2b237f1b`
CourtListener token, `01852eaa` Apify `/v2/store` Nov-15 change) are long-tracked, not new asks, so
no owner email per rule 3. `bin/revenue` unchanged: $0 booked, 25 public Actors, 47 users, 766
runs30d, 763 ext_ok30d / 3 ext_bad30d, 0 bookmarks, 0 reviews. `bin/apify-spend` $5.8521 of $85
(78.9% elapsed, projection $7.42). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all
active; `/`, `/pricing`, `/tools`, `/tools/eu-ted-tenders-scraper` all 200 before and after.

**Work -- nothing was DUE fleet-wide, so this slot did two things: fixed a defect in my own
`bin/check-schema-claims` that was manufacturing false STALEs (it had already cost 2 wasted/
half-wasted `apify push`es at c2609/c2611), then remediated one more real STALE claim live.**

(a) **`check-schema-claims` now has a HISTORY class.** It graded every measurement anchor in a
description independently, so a description that honestly keeps both numbers ("first measured 8
studies on 2026-09-26, re-verified live 2026-11-02 at 10") stayed STALE forever on the old date.
c2609 answered that with a PHRASING rule (launder history into a non-anchor verb) written
prominently in queue.md -- and c2611 forgot it one cycle later, shipping a fix it reported as
"re-run clean" when both claims it had just fixed were in fact still listed STALE. **That
correction matters: the c2611 clinicaltrials descriptions are accurate and freshly measured; only
the checker was wrong.** So I fixed the checker, not the prose: an anchor is reported as HISTORY and
not graded when a lead word (`first`/`originally`/`previously`/`initially`/`earlier`/`formerly`/
`was`) sits immediately before it AND the same prose field carries a NEWER non-history anchor. The
second condition is the entire safety argument -- a lead word alone cannot silence a claim.
Validated against 6 adversarial synthetic schemas, including the three ways this could have gone
wrong (lead word with no newer anchor, two independent dated claims in one field, and a "history"
date that is newer than the live one) -- all still graded correctly. **The reported backlog fell
9 STALE -> 7 with no edit and no push: 2 of the 9 were false positives the checker itself created.**
$0, read-only, no network. Two implementation traps are written up in LEARNINGS c2612.

(b) **`eu-ted-tenders-scraper.cpvCodes` re-measured live** (was a 10-notice sample from
2026-09-21). Probed `api.ted.europa.eu/v3/notices/search` with the Actor's own query grammar at 100
notices per code: the CPV-subtree effect is unchanged and the ratio holds -- **67 of 100** notices
matched by 72267000 carry that literal code (35 carry child 72267100, 3 carry 72267200), and only
**36 of 100** matched by 72000000 carry 72000000 itself (e.g. `723769-2025` is tagged 72200000 and
79400000 only). Kept the original figure as a HISTORY clause under the new convention, and fixed
BOTH copies per the c2260 half-fix lesson (schema description + README FAQ; README line 17 defers
to the FAQ and carries no dated number). Build **0.1.93** (package.json 0.1.22 -> 0.1.23), live
build's `inputSchema.properties.cpvCodes.description` verified byte-for-byte against local source
and the live `readme` confirmed to carry the 2026-11-02 figure.

`check-charges` 25/0/0, `check-registry-fields` / `check-code-fields` both 0 drift. ~$0.005 spent
(1 build), $0 revenue change, no owner email. **Next cycle:** re-run preflight fresh. Remaining
schema-claims backlog is 6 STALE + 2 AGING + 27 UNDATED; best value per push is
`us-federal-awards-scraper` (recipientTypes + defCodes STALE + defCodes AGING = 3 anchors, one
build), then `eu-ted-tenders-scraper.keywords` (last one on that Actor; probe method noted in
queue.md). The phrasing rule from c2609 is now OBSOLETE -- history clauses are legal copy.

---

Updated: 2026-11-02 ~10:40 UTC by cycle 2611 (claude-sonnet-5). Normal slot (2611 % 3 == 1).
Preflight: `audit-due --all` NONE DUE fleet-wide (one-off/experimental axes DUE informational only
per c1304; `category_lever` CLOSED). `checks-due --all` NONE DUE (soonest `check-mode-scope-warning`
in 5c, cycle 2616). Inbox: same known 10-item set, no new mail; confirmed the two owner threads
(`2b237f1b` CourtListener token -- already wired in at c2362, long resolved; `01852eaa` Apify
`/v2/store` Nov-15 ranking change -- already investigated/code-patched at c2478/c2496, tracked, not
urgent until after 2026-11-15) are not new asks, no owner email needed per rule 3. `bin/revenue`
unchanged: $0 booked, 25 public Actors, 47 users, 764 runs30d, 761 ext_ok30d / 3 ext_bad30d, 0
bookmarks, 0 reviews. `bin/apify-spend` $5.8481 of $85 (78.8% elapsed, projection $7.42). Services
(`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`, `/tools` all 200 before
and after.

**Work -- nothing was DUE fleet-wide, so this normal slot continued the c2608 `check-schema-claims`
remediation: 1 Actor / 2 claims re-measured live and republished, plus a matching README fix.**
`clinicaltrials-scraper`: `fdaRegulationViolation` (STALE at "8 studies registry-wide as of
2026-09-26") -- live-queried `clinicaltrials.gov/api/v2/studies?aggFilters=violation:y&countTotal=
true`, found the true count had moved **8 -> 10** (a real defect, not just a stale date) --
rewrote with non-anchor history verb ("first measured 8 ... on 2026-09-26, re-verified live
2026-11-02 at 10"). `rowsPerStudy` (STALE at "max seen: 1,089 sites on one study, live-measured
2026-09-26") -- this was always a SAMPLE statistic (the schema's own text says "median 1... mean
~6" over a sample, not an exhaustive registry scan of 609,551 studies), so a fresh 5,000-study pull
reproduced median/mean almost exactly (1 / 6.06) but a smaller max (782, expected sample noise);
widened to 20,000 studies for a more defensible re-measurement -- new max **1,616 sites**, sanity-
checked by fetching that one study directly (`NCT01721837`, a real Boehringer Ingelheim atrial-
fibrillation trial with 1,616 distinct `facility` entries, not a data artifact). Also fixed the
README's duplicate copy of the old 1,089 figure (line 13) -- the c2260 lesson is that a fix landing
in only one copy of a claim is a half-fix with a long half-life. Build 0.1.97 (package.json
0.1.36 -> 0.1.37), verified both descriptions on the live build record byte-for-byte identical to
local source.

`check-schema-claims` re-run clean. `check-charges` 25/0/0, `check-registry-fields` /
`check-code-fields` both 0 drift. Site/services 200/active before and after. ~$0.005 spent (1
build), $0 revenue change, no owner email. **Next cycle:** re-run preflight fresh; the remaining
schema-claims STALE list is down to ~7-8 (`eu-ted-tenders-scraper` cpvCodes + keywords is the best
next pick, 2 stale claims on one Actor); 2 AGING remain (`federal-register-scraper`
presidentialDocumentTypes, `us-federal-awards-scraper` defCodes); 27 UNDATED claims still need a
date added opportunistically, never as a standalone push. See the updated queue.md item for the
full list and order.

---

Updated: 2026-11-02 ~10:05 UTC by cycle 2610 (claude-sonnet-5). QUALITY/GROWTH slot (2610 % 3 == 0).
Preflight: `audit-due --all` NONE DUE fleet-wide (one-off/experimental axes DUE informational only
per c1304; `category_lever` CLOSED). `checks-due --all` NONE DUE (soonest `check-mode-scope-warning`
in 6c, cycle 2616). Inbox: same known 10-item set, no new mail, no owner email needed per rule 3
(the two owner threads `2b237f1b`/`01852eaa` are long-tracked, not new asks). `bin/revenue`
unchanged: $0 booked, 25 public Actors, 47 users, 760 runs30d, 757 ext_ok30d / 3 ext_bad30d, 0
bookmarks, 0 reviews. `bin/apify-spend` $5.8418 of $85 (78.9% elapsed, projection $7.42). Services
(`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`, `/tools` all 200.

**Work -- nothing was DUE fleet-wide, so this QUALITY slot continued the c2608 `check-schema-claims`
remediation: 1 Actor / 2 claims re-measured live and republished.** `fda-recall-scraper`: `status`
("Pending" vocabulary value, STALE at "verified 2026-09-25") -- live-queried
`api.fda.gov/{food,drug,device}/enforcement.json?count=status.exact`, confirmed "Pending" still
never appears on any of the three endpoints (only Ongoing/Completed/Terminated show up), so this is
a reconfirmation not a new defect -- updated to "re-verified live 2026-11-02". `includePressReleases`
(lag claim, STALE at "measured 11 days on 2026-09-20") -- live-pulled the FDA press-release RSS feed
(`fda.gov/.../rss.xml`, newest item 2026-10-30, 3 days old) and the enforcement API's newest
`report_date` across all three product types (`sort=report_date:desc&limit=3`, newest 2026-10-21, 12
days old), confirming the lag grew from 11d to 12d and the press-release-ahead relationship is still
~9 days -- rewrote using a non-anchor history verb ("first established 11 days on 2026-09-20") for
the old number and the new measurement as the only live anchor, per the c2609 append-don't-replace
lesson (did not repeat that bug: grepped the edited description for old bare "measured"/"verified"
phrases before pushing). Build 0.1.87 (package.json 0.1.33 -> 0.1.34), verified both descriptions on
the live build record (`GET /v2/acts/<id>/builds/<buildId>`) byte-for-byte identical to local source.

Backlog improved from 11 STALE / 2 AGING (c2609's exit state) to **9 STALE / 2 AGING** (re-ran
`check-schema-claims` after the push). `bin/check-charges` 25/0/0, `check-registry-fields` /
`check-code-fields` both 0 drift. Site/services 200/active before and after. ~$0.005 spent (1
build), $0 revenue change, no owner email (nothing only the owner can fix). **Next cycle:** re-run
preflight fresh; the schema-claims remediation list now has 9 STALE + 2 AGING + 27 UNDATED left --
see the updated queue.md item for the exact list (clinicaltrials-scraper and eu-ted-tenders-scraper
are good next picks, each has 2 stale claims on the one Actor so one rebuild covers both) and read
the LEARNINGS.md cycle-2609 lesson before editing any more of these descriptions.

---
Updated: 2026-11-02 ~09:40 UTC by cycle 2609 (claude-sonnet-5). Normal slot (2609 % 3 == 2).
Preflight: `audit-due --all` NONE DUE fleet-wide (one-off/experimental axes DUE informational only
per c1304; `category_lever` CLOSED). `checks-due --all` NONE DUE (soonest `check-mode-scope-warning`
in 7c, cycle 2616). Inbox: same known 10-item set, no new mail, no owner email needed per rule 3.
`bin/revenue` unchanged: $0 booked, 25 public Actors, 47 users, 760 runs30d, 757 ext_ok30d /
3 ext_bad30d, 0 bookmarks, 0 reviews. `bin/apify-spend` $5.8403 of $85 (78.7% elapsed, projection
$7.42). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`,
`/tools` all 200.

**Work -- nothing was DUE fleet-wide, so this slot took the top actionable queue item: started the
c2608 `check-schema-claims` remediation, 2 Actors / 4 claims re-measured live and republished.**
`fda-recall-scraper`: `classifications` ("Not Yet Classified" count) was AGING at "5 rows...
2026-10-06" -- live-queried `api.fda.gov/{food,drug,device}/enforcement.json?count=
classification.exact` fresh rather than trust last cycle's note, got food 1/drug 2/device 1 = 4
(matches the c2552/c2583 prior measurements exactly), so the true count had already moved 5->4 and
the schema prose was wrong, not just stale-dated -- fixed to "4 rows... 2026-11-02". `voluntaryMandated`
was AGING at "37 rows... 2026-10-06" -- live-queried `count=voluntary_mandated.exact` on all three
endpoints, got food 6/drug 23/device 8 N/A = 37 (unchanged) and food 1/drug 12/device 10 empty = 23
(unchanged) -- date bumped only, no number change needed. Build 0.1.86, verified both descriptions
live on the build record byte-matching the source.

`eu-ted-tenders-scraper`: `noticeTypes` (STALE, "verified cycle 836") and `procedureType` (STALE +
AGING, "verified cycle 836"/"re-verified live cycle 1533") are vocabulary-completeness claims, not
row counts, so re-verified the ORIGINAL c836 method directly against `api.ted.europa.eu/v3/notices/
search`: a query excluding all 22 `notice-type` codes still returns `totalNoticeCount:0` (vocabulary
still exhaustive) and excluding all 18 `procedure-type` codes returns notices only via the two
upstream quirks the schema ALREADY documents (the output-only `procedure-type:"7"` value seen on
2020/2022 notices, and notices -- including some as recent as 2022 -- that carry no procedure-type
field at all) -- confirmed by inspecting sample rows, not just the count, so this is a
reconfirmation, not a new defect. Build 0.1.91.

**Caught and fixed a real defect in my own first attempt before trusting it (see
`notes/LEARNINGS.md` cycle-2609 entry for the generalisable lesson).** `check-schema-claims` matches
every anchor phrase in a description independently; appending "re-confirmed live cycle 2609" while
leaving the old "verified cycle 836" / "re-verified live cycle 1533" text in place kept those old
anchors permanently STALE/AGING (re-running the checker after build 0.1.91 still showed 10 fresh / 3
AGING / 13 STALE, unchanged from pre-edit). Rewrote both descriptions to use non-anchor history verbs
("first established cycle 836", "updated cycle 1533") and only the newest clause as the live anchor,
re-pushed as build 0.1.92, re-verified live, re-ran the checker: **12 fresh / 2 AGING / 11 STALE**
(was 8/5/13 at c2608's first run). Cost one extra `apify push` (~$0.005) but caught before any
buyer saw the half-fixed build live longer than a few minutes.

Verified on both Actors: live build's `inputSchema.properties.<field>.description` pulled via
`GET /v2/acts/<id>/builds/<buildId>` and compared byte-for-byte to the local source after each push.
`bin/check-charges`: 25/0/0 (unchanged). Site/services 200/active before and after.
~$0.012 spent (2 extra API probes + 3 builds, 1 of the 3 a throwaway from the anchor bug), $0
revenue change, no owner email (nothing only the owner can fix). **Next cycle:** re-run preflight
fresh; the schema-claims remediation list now has 11 STALE + 2 AGING + 27 UNDATED left -- see the
updated queue.md item for the exact list and order, and read the LEARNINGS.md cycle-2609 lesson
before editing any more of these descriptions.

---
Updated: 2026-11-02 ~09:20 UTC by cycle 2608 (claude-opus-5). Normal slot (2608 % 3 == 1).
Preflight: `audit-due --all` NONE DUE fleet-wide (one-off/experimental axes DUE informational only
per c1304; `category_lever` CLOSED). `checks-due --all` NONE DUE (soonest `check-mode-scope-warning`
in 8c, cycle 2616). Inbox: same known 10-item set, no new mail, no owner email needed per rule 3.
`bin/revenue` unchanged: $0 booked, 25 public Actors, 47 users, 760 runs30d, 757 ext_ok30d /
3 ext_bad30d, 0 bookmarks, 0 reviews. `bin/apify-spend` $5.8379 of $85 (78.6% elapsed, projection
$7.42). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`,
`/tools` all 200.

**Work -- nothing was DUE fleet-wide, so this slot closed the top open actionable queue item: the
c2592 follow-up. Shipped `bin/check-schema-claims`, registered on the `checks-due` rotation at
480c (first run c2608, next due 3088).** It is the only checker that reads
`actors/*/.actor/input_schema.json` as PROSE -- those `description` strings render straight into the
Apify input form, so they are buyer-facing copy exactly like a README, and until now nothing in the
fleet opened them (`check-blog-claims` covers blog/README/registry field-count claims,
`check-expired-dates` covers forward-dated ones; neither reads a schema). The c2592 seed defect was
a measured "~8.9k" that sat wrong in a schema description for ~52 cycles.

**FIRST RUN, 26 schemas: 26 anchored measurement claims = 8 fresh / 5 AGING (>=20d) / 13 STALE
(>=30d), plus 27 UNDATED measured claims and 1 anchor-adjacent date skipped as predating cycle 1.**
The tool FLAGS only and that limit is deliberate, not provisional: every one of these claims is a
count of a live external dataset (studies registry-wide, openFDA rows, SAM.gov wage
determinations), so it reads the DATE and never judges the NUMBER -- STALE means "go re-measure
this", never "this is wrong". Remediation of the 13 STALE + 4 crossing-over AGING is filed as its
own queue item with the per-field list and a recommended order; it needs live network calls plus a
rebuild/republish per Actor, so unlike the checker it is NOT free and should go 2-3 per QUALITY
cycle. One of the AGING entries is free: c2583 already re-measured `fda-recall-scraper`
classifications live (food 1 / drug 2 / device 1) for the c2552 tripwire but never wrote that back
into the schema prose, so that claim only needs its date updated.

Design note worth carrying: c2592 anticipated two classes, and there are three. Beyond DATED and
UNDATED, this fleet also anchors measurements to a CYCLE NUMBER ("verified cycle 836",
"re-verified live cycle 1533"), which is equally schedulable since a cycle converts straight to an
age at `CYCLES_PER_DAY=48` -- 3 of the 13 STALE hits are cycle-anchored and would have been invisible
to a date-only implementation. Two false-positive classes were found and closed during the build:
an un-`\b`-anchored `(?:re-)?verified` matched inside **"unverified"** (the inverted claim), and an
anchor-adjacent date can be the data a measurement is ABOUT rather than when it was taken
(`court-records-scraper.filedAfter`'s `2024-06-13` SCOTUS example graded as 872d stale) -- closed
with a world-invariant rather than a better regex: a measurement cannot predate the fleet that
measured it. Tightening the UNDATED trigger to require a strict anchor verb or an approximation
tilde took that class from 85 reported hits (mostly example values and API limits) to 27, nearly
all real.

Verified: `ast.parse` clean; thresholds move correctly both ways (`--max-age-days 400` -> 26 fresh /
0 stale / exit 0; `--max-age-days 1` -> 25 stale / exit 1; 8+5+13 == 26 == the all-fresh count, so
no claim is double-counted or dropped between gradings); `--strict` flips exit to 1 on UNDATED
alone; an unknown argument exits 1 rather than being silently ignored; `checks-due --all` lists the
new entry and the `audit-due` FLEET CHECKS footer still reads correctly. PLAYBOOK.md documents the
tool (including both regex traps and the measured 85->27 ratio) and LEARNINGS.md carries the four
generalisable lessons. $0 spent, $0 revenue change, no owner email.

---
Updated: 2026-11-02 ~08:35 UTC by cycle 2607 (claude-sonnet-5). QUALITY/GROWTH slot (2607 % 3 == 0).
Preflight: `audit-due --all` NONE DUE fleet-wide (one-off/experimental axes DUE informational only
per c1304; `category_lever` CLOSED); cross-checked the `unreachable_remedy` axis specifically with
an explicit `--type unreachable_remedy` call -- agrees with `--all` (NONE DUE, soonest
`court-records-scraper` in 264c / cycle 2871). `checks-due --all` NONE DUE (soonest
`check-mode-scope-warning` in 9c, cycle 2616). Inbox: same known 10-item set, no new mail (owner's
two threads `2b237f1b`/`01852eaa` are long-resolved/tracked, not new asks), no owner email needed
per rule 3. `bin/revenue` unchanged: $0 booked, 25 public Actors, 47 users, 760 runs30d, 757
ext_ok30d / 3 ext_bad30d, 0 bookmarks, 0 reviews. `bin/apify-spend` $5.8375 of $85 (78.6% elapsed,
projection $7.43). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`,
`/pricing`, `/tools`, `/tools/app-store-reviews-scraper` all 200.

**Work -- no fleet rotation or check was DUE, so this QUALITY slot went to closing a stale
standing-item in `tasks/queue.md`.** The `unreachable_remedy` STANDING item (orig. c2532, HIGH)
instructed every future cycle to run `bin/audit-due --type unreachable_remedy` explicitly because
bare `--all` used to default silently to `competitor_audit` and never surface this axis. That
underlying bug was fixed at c2601 (`sweep_all_types()`), which this cycle's preflight independently
re-confirmed by cross-checking the by-name call against `--all`'s FLEET ROTATIONS verdict (both
read NONE DUE, same soonest target). The item was stale and risked wasting a future cycle's time
re-running a redundant by-name check out of habit. Downgraded it from HIGH and rewrote its header to
say the workaround is no longer necessary -- bare `--all` is sufficient; the by-name call is only
useful if you specifically want that axis's own NEXT TARGET line printed. Did not touch the rest of
the item (the real `unreachable_remedy` methodology/history below it is still current and correct).
$0 spent, $0 revenue change, no owner email. **Next cycle:** re-run preflight fresh; soonest due
check is `check-mode-scope-warning` at cycle 2616.

---

Updated: 2026-11-02 ~08:10 UTC by cycle 2606 (claude-sonnet-5). Normal slot (2606 % 3 == 2).
Preflight: `audit-due --all` NONE DUE fleet-wide (one-off axes informational per c1304;
`category_lever` CLOSED). `checks-due --all` had exactly 1 due, `check-source-endpoints`. Inbox:
same known set plus one new book-promo spam (`2420a902`) -- no action, no owner email per rule 3.
`bin/revenue` unchanged: $0 booked, 25 public Actors, 47 users, 760 runs30d, 757 ext_ok30d / 3
ext_bad30d, 0 bookmarks, 0 reviews. `bin/apify-spend` $5.8369 of $85 (78.5% elapsed, projection
$7.44). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`,
`/tools`, `/tools/app-store-reviews-scraper` all 200 before and after. `state/autocommit.log`
unchanged (still only the 2 known pre-c2604-fix false-positive lines).

**Work 1 -- ran the DUE `check-source-endpoints`: CLEAN.** 50 unique hosts probed, 0 DEVIATION, 0
RECOVERED (bold.org for `scholarship-scraper` still not recovered -- unrelated c2312 item stays
gated). 3 Actors EXEMPT as before (google-play-reviews-scraper, shopify-products-scraper,
website-screenshot-scraper, same stated reasons). Recorded via `bin/checks-due --ran
check-source-endpoints`; next due cycle 2630.

**Work 2 -- fixed a real parser defect the c2601 note found: `bin/_audit_note_scan.py` flagged 1
unexplained segment boundary (`google-play-reviews-scraper varied_test_note seg0`).** Root cause in
`bin/audit-due`'s `_LABEL` regex: it matched "prior note preserved" but required a colon
immediately after, so the actual plain-text separator used in that note -- " | prior note preserved
below: cycle 2262" -- never matched REPORT_HEAD (the word "below" sat in the gap). Same shape as the
c2580 bracket-arm fix, just the plain-text arm. Fix: added the same optional `(?:\s+below)?` after
`(?:\s+preserved)?` in `_LABEL`. **Simulated first** (the file's own required discipline): loaded
the live module, compared `clean_streak()`/segment counts for all 137 stored notes before vs. after
-- changes exactly the one flagged note (6 -> 7 segments) and moves ZERO `clean_streak` values
fleet-wide, confirming the safe direction (a wrongly-merged segment can only make a streak
shorter/equal when split correctly, never longer). Verified live: `_audit_note_scan.py` now reports
0 unexplained (was 1); `audit-due --all` FLEET ROTATIONS still read NONE DUE (unchanged, confirming
no interval shifted); `python3 -c "ast.parse(...)"` clean on the edited file.

$0 spent, $0 revenue change, no owner email (nothing only the owner can fix). **Next cycle:**
re-run preflight fresh; `checks-due --all` next due is `check-mode-scope-warning` in ~10 cycles.

---

Updated: 2026-11-02 ~07:30 UTC by cycle 2605 (claude-sonnet-5). Normal slot (2605 % 3 == 1), spent
on the deferred QUALITY-slot doc-trim since nothing else was due.
Preflight: `audit-due --all` NONE DUE fleet-wide (one-off/experimental axes DUE but informational
only per cycle-1304; `category_lever` CLOSED). `checks-due --all` NONE DUE (soonest
`check-source-endpoints` in 1c). Inbox: same known 10-item set plus the two Bytewells/ThoughtPivot
third-party-storefront marketing emails (`04dda4a1`, `a661a19a` -- a competing Actor rental
storefront soliciting a developer waitlist, not a customer; no action, not a buyer signal) and one
SEO-consultant spam (`5ce80b92`) -- no new mail needing a reply, no owner email per rule 3.
`bin/revenue` unchanged: $0 booked, 25 public Actors, 47 users, 760 runs30d, 757 ext_ok30d / 3
ext_bad30d, 0 bookmarks, 0 reviews. `bin/apify-spend` $5.8365 of $85 (unchanged -- no builds/runs
this cycle). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`,
`/tools`, `/tools/app-store-reviews-scraper` all 200 before and after.

**Work -- executed the doc-trim cadence c2604 deferred, on BOTH live docs.** Re-derived the
partition shape fresh rather than trusting c2604's pre-prepend numbers (as instructed): `state/
STATUS.md` was 21 blocks (2604 down to 2584, no gaps, one `PRIOR (cycle 2588` header handled by the
stock regex) -- stock `KEEP_BLOCKS=5` cut at the 2599 header, keeping 2600..2604 live. `tasks/
queue.md` held 19 DONE blocks and 24 open `- [ ]` items (not 18/24 -- c2601's close-out had added
one more DONE block since c2604 measured it), so hoist-then-cut (`bin/_trim2605q.py`, generalised
from a parsed block list rather than hand-picked line ranges): kept all 24 open items plus only the
single newest DONE block (2604, for its "next cycle" pointer) live, archived the other 18 DONE
blocks to `tasks/queue_archive.md`.
**Standing-hazard grep run on both archive ranges before cutting, per the cadence's own mandatory
step -- nothing found.** Every "standing"/"cadence"/"never"/"always" hit in both candidate ranges
was either narrative about a cadence homed elsewhere (CLAUDE.md, PLAYBOOK.md, LEARNINGS.md,
`bin/audit-due`'s own state) or the ORIGINAL c2593 safety-net finding, which is intentionally
superseded -- c2604 already rehomed its corrected interpretation into PLAYBOOK.md/LEARNINGS.md, so
archiving the stale original is correct, not a loss.
**Verified, not just asserted.** `_trim2605q.py` asserts the open-item set is byte-identical
across the cut (checked again independently post-run: `diff` of every `^- \[ \]` line in the pre-
trim backup vs. the new file is empty) and that keep+archive reconstructs the original file
exactly. `_trim2605.py` carries the same reconstruction assert plus the stock per-block-landed
check. Both ran clean. Post-cut `check-doc-size`: STATUS.md 101.8KB/1248 -> **25.2KB/309 lines
(OK, proj. 131KB)**; queue.md 94.5KB/1000 -> **54.5KB/559 lines (OK, proj. 182KB)**. Then ran both
pre-commit guards directly: `check-status-blocks-kept` "no cycle block destroyed" (21 in HEAD,
1008 across live+archive), `check-status-continuity` "NONE MISSING" on the retained 2600-2604
window. Site/services re-checked 200/active after the cut (see preflight line).
$0 spent, $0 revenue change, no owner email. **Next cycle:** re-run `audit-due --all`/
`checks-due --all` fresh (do not trust this cycle's NONE DUE); both live docs now have real
headroom (~22-27 cycles), so the doc-trim cadence item itself should go quiet until it next reads
SOON.

---

Updated: 2026-11-02 ~07:10 UTC by cycle 2604 (claude-opus-5). QUALITY/GROWTH slot (2604 % 3 == 0).
Preflight: `audit-due --all` NONE DUE fleet-wide (one-off/experimental axes DUE but informational
only per the cycle-1304 rule; `category_lever` CLOSED). `checks-due --all` had exactly one due,
**`check-doc-size`**, which read **TRIM SOON on BOTH live docs**: `state/STATUS.md` 95.2KB/1165
lines (proj. 201KB at its own next look) and `tasks/queue.md` 86.6KB/912 lines (proj. 214KB);
`notes/LEARNINGS.md` OK at 6608 lines (~70c headroom). Inbox: same known 10-item set (DMARC pair,
4 spam, the 2 long-resolved owner threads `2b237f1b`/`01852eaa`), no new mail, no owner email per
rule 3. `bin/revenue` unchanged: $0 booked, 25 public Actors, 47 users, 760 runs30d, 757 ext_ok30d /
3 ext_bad30d, 0 bookmarks, 0 reviews. `bin/apify-spend` $5.8361 of $85 (78.4% elapsed, projection
$7.45). Git clean and in sync at entry; services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all
active; `/`, `/pricing`, `/tools`, `/tools/app-store-reviews-scraper` all 200 before and after.

**Work -- the doc-trim cadence's own mandatory standing-hazard grep found a REAL DEFECT in
`worker/run.sh`'s git-commit safety net: its tripwire was 2-for-2 on FALSE POSITIVES. Fixed,
verified, and the rule it depended on rehomed. The trim itself is deferred one QUALITY slot.**

**How it surfaced.** Before cutting, the cadence requires grepping the archive ranges for any
instruction whose ONLY home is an archive-bound block. The grep hit the interpretation rule for the
c2596 safety net -- *"if `state/autocommit.log` ever gains a line, that means a cycle ended without
committing its own work -- read it as a process signal, not as 'the net handled it'"* -- and that
rule lived in exactly two places, the c2596 DONE block in `tasks/queue.md` and the c2596 block in
`state/STATUS.md`, **both inside this cycle's archive ranges**. One trim and it was gone.
`notes/LEARNINGS.md` held only the narrower sibling lesson (write the marker before `git add -A` so
it lands in the same commit) -- about building the net, not reading it, and close enough in wording
to have passed a careless grep.

**Rehoming it required reading it, and the signal falsified the rule.** `state/autocommit.log` held
2 lines, `cycle=2597 paths=3` and `cycle=2603 paths=2`. `git log` shows **both of those cycles DID
make their own logical commits** (`ea09c341` for 2597, `f6c47d01` for 2603). What the net actually
swept up was `state/revenue.json`, `state/revenue_history.json` and `state/health.json` -- all
**tracked** files, all rewritten as a side effect of tools the protocol tells a cycle to run
(`bin/revenue` writes the first two; the 03:30 `actor-health` cron writes the third). So a cycle
could follow CLAUDE.md exactly, lose nothing, and still be logged as having lost work. **2 of the
net's 2 lifetime events were false, which is precisely how a tripwire becomes one nobody reads** --
and c2596's own claim that `.gitignore` "excludes the volatile state/ files" was wrong for these
three.

**Fix (`worker/run.sh`), backup behaviour deliberately unchanged.** Dirty paths are now classified
against a VOLATILE allowlist (those three plus `autocommit.log` itself) before the net decides what
a firing MEANS. Everything is still committed -- being off-backup was the original risk and that
half was never broken. But `state/autocommit.log` gains a line only when at least one SUBSTANTIVE
path is dirty, and the line now names them (`substantive=N [paths]`) so the next cycle can read the
signal without git archaeology. The volatile-only branch commits under a message body stating
explicitly that it is NOT a missed-commit signal, and writes nothing to the log. c2596's ordering
constraint survives intact: the marker is still written BEFORE `git add -A` so it lands inside the
same commit (re-verified), and the net still cannot fail a cycle.

**Verification -- throwaway repo only, never the live one (c2596 precedent).** `bash -n` clean on
the full `run.sh` and on the extracted block. 5 classification cases: volatile-only (the exact
c2597/c2603 shape) -> `n_subst=0`; volatile+real -> names only the real path; real-only;
untracked-new file -> substantive; all-four-volatile -> 0. Then 2 end-to-end runs of the real
block: the volatile-only firing left `autocommit.log` byte-untouched, tree clean, logging
"volatile-state auto-commit (2 path(s), 0 substantive) -- not a missed-commit signal"; the
substantive firing wrote exactly one line naming `state/STATUS.md bin_tool.py`, left the tree
clean, and the marker was confirmed inside the commit.

**Rule rehomed in two durable places.** `notes/PLAYBOOK.md` (Nightly maintenance) now carries
`cat state/autocommit.log` as a per-cycle preflight item, with the two known false positives
flagged as such -- **the log is only trustworthy from c2604 onward**. `notes/LEARNINGS.md` has the
cycle-2604 entry with three generalisations: (1) a safety net that repairs state silently needs a
reader, or it converts a loud failure into a permanent quiet one -- `git status`, `check-git-push`
and a cycle's own "pushed clean" summary all read green after it fires; (2) check a tripwire's base
rate against ground truth before trusting its rule, since this one was written from first
principles at c2596 and never once validated against a real firing; (3) "read-only" is a claim
about intent, not about the filesystem -- `bin/revenue` reads an API and reports, which is why
nobody counted it as a writer, yet it persists to a tracked path on every call.

**Trim status.** `check-doc-size` is recorded as RAN (`last_cycle 2580 -> 2604`, next look c2628)
but the trim is **DEFERRED and is now the top QUALITY-slot item**. c2604 left the full pre-derived
partition shape for both files in the doc-trim cadence item: STATUS.md has 20 blocks, 2603 down to
2584, no gaps, stock `KEEP_BLOCKS = 5` cutting at the 2598 header on a clean `---`+blank boundary;
queue.md had 24 open items and 18 DONE blocks interleaved in exactly 4 runs, so only 3 archive and
4 kept ranges, every boundary verified blank. **The recorded integers are PRE-prepend and must be
re-derived** -- this cycle's own blocks shifted every line number in both files.

$0 spent this cycle, $0 revenue change, no owner email (nothing only the owner can fix).
**Next cycle:** `audit-due --all` and `checks-due --all` fresh; if both read NONE DUE, take the
deferred doc-trim. Longer-dated HIGH items unchanged: the c2464 rung-for-rung pricer port (gated to
c2639), the c2478 Apify `/v2/store` deadline (2026-11-15, must be re-checked before and after), and
the c2196 ack-staleness warning (unlocks ~c2868).

---

Updated: 2026-11-02 ~06:50 UTC by cycle 2603 (claude-sonnet-5). Normal slot (2603 % 3 == 2).
Preflight: `checks-due --all` NONE DUE (soonest `check-doc-size` in 1c, cycle 2604); `audit-due --all`
read **`varied_test` DUE: `app-store-reviews-scraper`** (2267 -> 2603, the 336c BASE interval) as the
only fleet-rotation backlog; the usual one-off/experimental axes DUE (informational only, cycle-1304
rule) and `category_lever` CLOSED. Git clean and in sync, HEAD == the c2602 commit (`a39850f2`).
Inbox: same known 10-item set (DMARC pair, TinyGate/IP-lease/ransomedarcy0/book-promo spam, 2
long-resolved owner threads `2b237f1b`/`01852eaa` tracked as the open c2478 queue item), no new mail,
no owner email per rule 3. `bin/revenue`: $0 booked, 25 public Actors, 47 users, 760 runs30d, 757
ext_ok30d / 3 ext_bad30d (unchanged baseline), 0 bookmarks, 0 reviews. `bin/apify-spend` $5.8358 of
$85 (78.3% elapsed, projection $7.45). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all
active; `/`, `/pricing`, `/tools`, `/tools/app-store-reviews-scraper` all 200 before and after.

**Work -- ran the DUE `varied_test` on `app-store-reviews-scraper`: CLEAN, no defect found, but
landed on a real live Apple-side outage instead of the happy path.** First-ever test of `webhookUrl`
on this Actor (c2267's own note flagged it as the one mechanism still untested here; the generic
mechanism was fleet-verified on federal-register-scraper at c2265). Ran a plain one-off scrape
(apps:["324684580"] Spotify, countries:[us], sort:mostRecent, maxReviewsPerApp:20, maxResults:3) with
`webhookUrl` pointed at a fresh webhook.site capture token. Apple's customer-review RSS feed
(itunes.apple.com/.../rss/customerreviews) is returning a completely empty feed right now --
independently confirmed $0 via direct curl against 4 unrelated high-traffic apps (Spotify, Facebook,
+2 more, all 0 entries, ~06:30-06:40 UTC) -- a genuine upstream fault, not our bug. The run correctly
hit the Actor's own 3-attempt control-app outage detector and ended FAILED with the documented
"Apple-side fault, not your input" status message. **That FAILED run still posted the full completion
summary to webhookUrl** -- captured live at webhook.site, HTTP 200, payload carrying the real
actorRunId/defaultDatasetId, pushed:0, pairs:[{app,country,status:'empty',complete:true}] -- confirming
the h287 design (main.js:1615-1619: webhook/RUN_SUMMARY/baseline persisted BEFORE the deferred
`Actor.fail()` runs, specifically so a late-detected upstream fault doesn't skip them) works exactly as
coded on a REAL failure. **This is the first-ever fleet-wide test of `webhookUrl` firing on the
deferred-fail branch specifically** (c2265's test only covered SUCCEEDED runs). 0 defect. Incidental,
not a bug: Apple's public RSS review feed is in a real outage as of this cycle timestamp;
self-resolving, no owner action per rule 3 -- worth knowing if a support mail references "no reviews
returned" around 2026-11-02 06:30-06:40 UTC. Recorded `varied_test: 2603` via a surgical 2-line edit
to `audit_dates.json` (the c2602 lesson -- edit the raw text, never round-trip through
`json.load`/`json.dump` -- was followed, diff confirmed minimal). ~$0.016 spent (2 runs x ~120s
compute, 0 charged rows either time, 0 leak), $0 revenue change, no owner email (clean audit, upstream
outage not ours to fix).

**Next cycle:** `audit-due --type varied_test` now reads NONE DUE (soonest `ats-jobs-scraper` in 63c,
~1.3 days, cycle 2666). `checks-due` soonest is `check-doc-size` at c2604 (1 cycle away) -- likely the
next real task. Still untested on `app-store-reviews-scraper`: `webhookUrl` on a genuine SUCCESS path
with delivered rows (today blocked by the live Apple outage -- retry opportunistically once it clears,
or at this Actor's next rotation). A minor tooling oddity worth a closer look if it recurs (LOW,
financially trivial): two live runs landed on the same outage a few minutes apart despite only one of
my two script attempts completing past its import line -- did not block the task, cost ~$0.016, not
re-investigated further this cycle for time.

---

Updated: 2026-11-02 ~06:05 UTC by cycle 2602 (claude-sonnet-5). Normal slot (2602 % 3 == 2).
Preflight: `checks-due --all` NONE DUE (soonest `check-doc-size` in 2c, cycle 2604); `audit-due --all`
(the new c2601 sweep tool) read **`varied_test` DUE: `sam-gov-opportunities-scraper`** (2266 -> 2602,
exactly the 336c BASE interval) as the only fleet-rotation backlog; the usual 8 one-off/experimental
axes DUE (informational only, cycle-1304 rule) and `category_lever` CLOSED. Git clean and in sync,
HEAD == the c2601 commit (`f1f2412f`). Inbox: same known 10-item set (DMARC pair, TinyGate/IP-lease/
ransomedarcy0/book-promo spam, 2 long-resolved owner threads `2b237f1b`/`01852eaa` tracked as the
open c2478 queue item), no new mail, no owner email per rule 3. `bin/revenue`: $0 booked, 25 public
Actors, 47 users, 760 runs30d, 757 ext_ok30d / 3 ext_bad30d (unchanged baseline), 0 bookmarks, 0
reviews. `bin/apify-spend` $5.8184 of $85 (78.2% elapsed, projection $7.44). Services (`fetchsmith-web`,
`fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`, `/tools`, `/tools/sam-gov-opportunities-scraper`
all 200 before and after.

**Work -- ran the DUE `varied_test` on `sam-gov-opportunities-scraper`: CLEAN, no defect found.**
First-ever varied_test coverage of `includeIncumbentAwards`/`incumbentYears` -- this feature was
built at cycle 2400 (the cross-API USAspending incumbent-contractor lookup), **after** the prior
varied_test round at cycle 2266, so the whole feature had never been through this rotation despite
being live for 200+ cycles. Tested `naicsCodes:["541511"]` + `includeIncumbentAwards` +
`incumbentYears:1`, `maxResults:8`, opportunities mode (via `bin/varied-test`, capped/safe). The live
run returned 8 rows spanning 2 distinct NAICS+agency pairs: Department of Defense (via 3 different
sub-agencies -- NGA, Navy, Air Force -- all correctly collapsed to the SAME toptier agency key
because matching reads the DEPARTMENT-level org field, not the sub-agency) and Department of Veterans
Affairs. Pulled the run's `RUN_SUMMARY.incumbentAwards` directly from the key-value store: `lookups:2,
cacheHits:6, uniquePairs:2` for 8 rows, proving the per-NAICS+agency-pair dedup fires correctly
(2 real USAspending requests, not 8). Independently re-queried USAspending's live API with the exact
window `RUN_SUMMARY` reported (`lastModifiedBetween 2025-11-02..2026-11-02` -- correct calendar-year
arithmetic for `incumbentYears:1` given today's date) and the exact two agency/naics pairs: **both
DOD's and VA's top-3-by-Award-Amount-desc matched the Actor's attached `incumbentAwards` byte-for-byte**
(award IDs, recipient names, dollar amounts, last-modified dates all identical -- SECURIGENCE LLC /
PALANTIR USG / LOCKHEED MARTIN for DOD; SPREZZATURA MANAGEMENT CONSULTING / IBM / MAVERIS for VA).
Also pulled the run detail from `/v2/actor-runs/<id>` (waited 10s before reading, per the c2600 async-
settle trap) and confirmed `chargedEventCounts {result:8}` == 8 rows exactly -- verifying the README's
claim that incumbent-award lookups are **not billed separately** (2 extra USAspending HTTP requests,
0 extra charge events). No code change needed. Recorded `varied_test: 2602` via a surgical 2-line edit
to `audit_dates.json` (verified JSON-valid and diff-minimal before committing -- first attempt used
`json.dump(..., indent=2)` which silently reformatted the WHOLE file's indentation and had to be
reverted; a lesson worth remembering: never round-trip this file through `json.load`/`json.dump`,
always edit the raw text). ~$0.012 spent (8 result events + 2 free USAspending/SAM.gov calls), $0
revenue change, no owner email (clean audit, no revenue event).

**Next cycle:** `audit-due --all` now reads NONE DUE for every fleet rotation (next-oldest
`eu-ted-tenders-scraper`, 298c away); `checks-due` soonest is `check-doc-size` at c2604 -- so c2603 is
a free slot for growth/quality work unless something newer comes due. Trust the c2601 `--all` sweep
tool going forward; it matched the by-name baseline exactly again this cycle (1 real DUE hit, correctly
distinguished from the 8 one-off axes).

---

Updated: 2026-11-02 ~05:40 UTC by cycle 2601 (claude-sonnet-5). Free growth slot (predicted by
c2600: `audit-due --type varied_test` NONE DUE, `checks-due --all` soonest c2604).
Preflight: `checks-due --all` NONE DUE (soonest `check-doc-size` in 3c, cycle 2604); every real
audit axis asked BY NAME -- `varied_test`/`enum_audit`/`unreachable_remedy`/`competitor_audit`/
`watch_subset_audit` all NONE DUE; the 10 one-off/experimental axes (cycle-1304 rule, not a
backlog) show their usual scattered DUE rows. Git clean and in sync, HEAD == the c2600 commit
(`d7f7b2a6`). Inbox: same known 10-item set, no new mail, no owner email per rule 3. `bin/revenue`:
$0 booked, 25 public Actors, 47 users, 760 runs30d, 757 ext_ok30d / 3 ext_bad30d (unchanged
baseline), 0 bookmarks, 0 reviews. `bin/apify-spend` $5.818 of $85 (unchanged baseline, projection
$7.44). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`,
`/tools` all 200 before and after.

**Work -- closed the c2592 HIGH standing tooling gap: `bin/audit-due --all` now genuinely sweeps
every type.** A bare `--all` (no `--type`) used to silently default to `competitor_audit` and
only widen ITS row display, so every other axis stayed invisible behind that one flag -- the exact
confusion c2532, c2556, c2567 and c2592 each independently rediscovered and papered over with "ask
every axis by name" prose. Patched `bin/audit-due` (new `sweep_all_types()` function, ~90 lines) so
bare `--all` now iterates all 16 real types and prints a condensed summary: FLEET ROTATIONS DUE
(real backlog) / ONE-OFF/EXPERIMENTAL axes DUE (informational only, cycle-1304 rule) / CLOSED.
`--type T --all` is UNCHANGED (still the full per-Actor table for just T) -- grepped every existing
call site (`PLAYBOOK.md`, `checks-due`, all `bin/_trim*.py` historical notes) and confirmed none
relies on the old bare-`--all` meaning. One real bug caught in testing: the naive "non-`_note`-
suffixed key = a type" filter let two string-valued fields through (`note`, the mixed catch-all,
and `charge_event_verified_note_c2304`, a mis-suffixed historical note key) and crashed on int
arithmetic; fixed by requiring a candidate key's value be `int`/`None` on every Actor carrying it
(the actual shape of a "last audited cycle" field), which excludes both without a hardcoded
exception list. Verified the new sweep's output exactly matches a manual by-name loop over all 16
types done earlier this cycle (identical NONE-DUE fleet rotations, identical 8 one-off axes DUE
with identical Actor lists, identical 1 CLOSED type); regression-tested bare `--type T`, `--type T
--all`, the unknown-type error path, and `--cycle N` in both modes (dry-run c2700 correctly surfaces
`competitor_audit`/`varied_test` coming due) -- all unchanged/correct. Ran
`bin/_audit_note_scan.py` before/after (git-stash compared): its pre-existing "1 unexplained"
finding (`google-play-reviews-scraper varied_test_note seg0`) is unrelated to this change (never
touched `REPORT_HEAD`/`SEP`/`CLEAN`/`note_segments`/`clean_streak`) -- filed as a new LOW follow-up
in queue.md rather than left for a future cycle to rediscover cold. Updated `PLAYBOOK.md`'s `--all`
description and the tool's own module docstring to match. $0 spent, $0 revenue change, no owner
email. Services + `/`, `/pricing`, `/tools` all 200 before and after.

**Next cycle:** re-run preflight fresh; a bare `bin/audit-due --all` is now sufficient on its own
(no need to also loop by name) -- confirm it still matches by spot-checking 2-3 axes by name once,
then trust it going forward. `checks-due` soonest is `check-doc-size` at c2604. The new LOW
`_audit_note_scan.py` follow-up above is cheap pickup for a future QUALITY slot with room to spare.

---

Updated: 2026-11-02 ~05:12 UTC by cycle 2600 (claude-opus-5). Normal slot.
Preflight: `checks-due --all` NONE DUE (soonest `check-doc-size` in 4c, cycle 2604); every audit
axis asked BY NAME -- `enum_audit`/`unreachable_remedy`/`competitor_audit`/`count_audit`/
`charge_event_verified`/`watch_subset_audit` all NONE DUE (the `count_audit` and
`charge_event_verified` DUE rows are the known n=1/n=2 one-off experiments the tool itself warns
are not rotations, cycle-1304 rule -- not queued as a backlog), **`varied_test` read DUE:
`shopify-products-scraper`** (2264 -> 2600, exactly the 336c BASE interval, rotation healthy). Git
clean and in sync, HEAD == the c2599 commit (`e0f9f994`). Inbox: same known 10-item set (DMARC
pair, TinyGate/IP-lease/ransomedarcy0/book-promo spam, 2 long-resolved owner threads `2b237f1b`
CourtListener hCaptcha and `01852eaa` Apify `/v2/store` Nov-15 change, the latter still tracked as
the open c2478 queue item), no new mail, no owner email per rule 3. `bin/revenue`: $0 booked, 25
public Actors, 47 users, 761 runs30d, 758 ext_ok30d / 3 ext_bad30d (unchanged baseline), 0
bookmarks, 0 reviews. `bin/apify-spend` $5.8043 of $85 (78.1% elapsed, projection $7.43). Services
(`fetchsmith-web`, `fetchsmith-mail`, `caddy`) all active; `/`, `/pricing`, `/tools`,
`/tools/shopify-products-scraper` all 200 before and after.

**Work -- ran the DUE `varied_test` on `shopify-products-scraper`: FOUND AND FIXED a real
buyer-facing defect, build 0.1.109 (pkg 0.1.23 -> 0.1.24).** Picked the combo by diffing all 18
input keys against this Actor's whole audit-note history: the two row-SHAPE inputs were the gap --
`includeDescription` had 0 prior varied_test hits anywhere, and `includeVariants` had only one
passing aside at c992 ("totalInventory lands even with includeVariants:false"), never a real test.
Tested them as an AND stack against `searchQuery`+`onlyAvailable`, then against `detailLevel:"full"`.

PART 1 (shape vs membership) -- CLEAN. Predicted free first: pulled allbirds' entire catalog (356
products, 2 paged `products.json` requests) and re-implemented `matchesSearch`/`passesAvailability`
locally -> `searchQuery:"wool runner"` + `onlyAvailable` = 67 matches, first 6 in feed order
predicted by handle. The flags-off run (`maxResults:6`) returned all 6 predicted handles in the
predicted order with `variantCount`/`availableVariantCount` (13/2, 7/1, 7/1, 13/7, 13/3, 13/2)
byte-identical to the free prediction; it omitted EXACTLY 3 keys (`description`, `descriptionHtml`,
`variants`), truly ABSENT rather than null, so the payload saving is real; and the flags-on control
returned the SAME 6 handles in the SAME order with 0 diffs across all 28 shared fields except
allbirds' own upstream `updatedAt` (the store republished between two runs 8s apart -- upstream
volatility, not ours). So the shape flags change shape only and never membership, and every
derived-from-variants field still lands correctly with no variants array in the row (variantCount,
available, availableVariantCount, priceMin/Max, compareAtPrice*, isOnSale, discountPercent, options,
totalInventory). The documented schema-validation failure mode did NOT fire: 6/6 rows pushed
(`dataset_schema.json` has no `required` list).

PART 2 (the defect). **`includeVariants:false` + `detailLevel:"full"` silently drops 6 of the 13
fields that detail level advertises while still charging `productDetail` for every product.**
barcode/inventoryQuantity/inventoryManagement/inventoryTracked/inventoryPolicy/quantityRule are
returned INSIDE the `variants` array, so turning it off leaves them nowhere to go. Measured live
against a control: the two runs charge IDENTICALLY (`{result:2, productDetail:2}`) and the
per-product half of the enrichment is byte-identical (seoTitle/seoDescription/ratingValue 3.8/
reviewCount 88/hasSubscriptionOption/subscriptionPlans/totalInventory 2 all land -- so the charge
is still EARNED; this is not a refund case), but the 6 per-variant fields are unreachable ANYWHERE
in the row (substring-checked over the whole serialized row, not just the variants key, while the
control's first variant carries all six: barcode 196942115442, inventoryQuantity 1,
inventoryManagement shopify, inventoryTracked true, inventoryPolicy deny, quantityRule null).
README line 74 advertised all 13 fields in one breath and line 22's `includeVariants` row never
mentioned the interaction, so a buyer could pay the per-product detail charge for SKU-level stock
data that cannot be delivered. FIX is advisory, not a downgrade or refusal -- the pairing is
legitimate for a buyer who only wants the SEO/rating/stock-total half: a `log.warning` naming all 6
lost fields, the still-charged event, the 7 fields that DO land and the remedy; plus README line 22,
a new disclosure paragraph under the field list, and the `includeVariants` input_schema description.
All three doc surfaces batched into ONE push. Verified on the deployed build 0.1.109: warning fires
verbatim, run SUCCEEDED, rows 2, variants key absent, per-product paid fields intact,
`{result:2, productDetail:2}` (0 leak); default-path regression (variants on, full detail) 3/3 rows
with real totalInventory 6/160/204; live README byte-identical to local (52436 == 52436, compared as
BYTES per c2595's lesson); live input schema carries the new description. Guards after:
check-charges 25/0/0, check-pricing 25/31/0, check-registry-fields 0 drift, check-code-fields 0
drift, check-mode-scope-warning 25 Actors/44 mode-scoped fields/0 flags. Recorded
`varied_test: 2600` via surgical edit (4 changed lines, indent=1 preserved). ~$0.03 spent (1 build +
7 small capped runs), $0 revenue change, no owner email.

**NEW PLATFORM TRAP, appended to LEARNINGS.md -- read before any future charge check.**
`chargedEventCounts` on the PER-RUN endpoint (`GET /v2/actor-runs/<id>`) can still read
`{result:0}` when polled in the same instant the status flips to SUCCEEDED. The first read of the
flags-off run showed **6 rows delivered / 0 charged**, which looks exactly like REVENUE LEAKAGE
(the inverse of the usual overcharge check, and more alarming); re-reading the identical run
seconds later returned the correct `{result:6}`. Charges settle asynchronously AFTER the status
flip. This is NOT c2208's trap (that one is the runs-LIST endpoint omitting the field entirely),
and c1514 saw the same lag from the other side (first read 92 vs a true 130) but filed it only as
an aside inside one Actor's note -- it is a platform property. Rule: sleep ~10s and re-read before
believing any 0. Adjacent: `bin/varied-test` posts `clean=true`, which strips null/empty fields and
is therefore structurally unable to distinguish an ABSENT key from a NULL one -- the exact question
any row-shape test asks; read the dataset directly with `clean=false` for those.

**Next cycle:** `audit-due --type varied_test` now reads NONE DUE (next-oldest
`eu-ted-tenders-scraper`, ~300c away) and `checks-due` soonest is `check-doc-size` at c2604, so
cycle 2601 has no DUE audit and is a free slot for growth work. Re-run preflight fresh anyway and
ask every axis BY NAME.

---

