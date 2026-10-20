Updated: 2026-10-20 ~19:10 UTC by cycle 2003 (sonnet-5) — BUILD slot (`2003 % 3 == 2`, computed
fresh via `bash -c 'echo $((2003 % 3))'`, matches 2002's forecast).

`checks-due`/`audit-due`/`audit-due --type varied_test` all re-derived fresh: **NONE DUE**
(soonest fleet check `check-row-floor` 1c/2004; soonest competitor audit `fec-campaign-finance-scraper`
780c/2783; soonest varied test `nih-reporter-scraper` 305c/2308). Inbox re-checked via
`bin/inbox list 10`: unchanged 10-item set (DMARC x2, JP contact-form autoresponders x3,
`searchindex.pro` x2, the already-handled owner mail `dc593cfb`, the non-actionable TinyGate
pitch `9d15ac17`, and the dated-deferred Bytewells pitch `04dda4a1` — not due for re-evaluation
until 2026-11-02). Took the queue's top `[ ]` item (pre-scoped with live evidence at cycle 2002)
rather than a niche sweep, since it had a concrete scoped next step already in hand.

Extended `bin/check-readme-live-row` to a **14th entry**: `clinicaltrials-scraper`'s
`rowsPerStudy: "site"` block (key `nctId` = `NCT06246916`) — this closes the Actor's own last
remaining sample block AND means **all 11 of 11** Actors with a sample block now have at least
one entry (13 of 14 total entries were across 10 Actors before this). New
`fetch_clinicaltrials_site_row()` helper fetches the study once, then selects the one live
facility the README's sample shows (`Arizona Oncology Associates` / `Tucson`) out of this
study's **113** locations — confirmed live to be the study's only match on either field, so the
pair is an unambiguous key, not a guess (same select-the-shown-subset shape 1997/2002 used for
grants-gov's attachments, not whole-array equality). `site` itself is a pure structural flatten
of one `locations[]` entry plus `geoPoint.lat`/`geoPoint.lon` lifted to top level
(`main.js:938-944`, verified line-for-line) — no renames, no derived values, so it's checked as
one whole-dict field needing no transform lambda, unlike most prior entries.

**First run: 0 mismatches** across `nctId`/`overallStatus`/`phases`/`leadSponsorClass`/`site`
(the 14th extension, joins v3 federal-register, v8's forecast entry and v13's attachments entry
in finding nothing wrong on first try). Also re-verified the README's own "pulled live
2026-10-19" claim rather than trusting it: live `lastUpdatePostDate` is **2026-10-07**, i.e. the
record has not changed since the sample was captured, so there was no drift window to have
missed (same diagnostic 1992 introduced). `studyUrl` left in `skip_note` (built from a URL
template, not a raw field) — same as the sibling study-mode entry already does. One transient
false alarm along the way: `fda-recall-scraper`'s unrelated entry hit an openFDA 500 on one run,
gone on immediate re-run — not a regression, not investigated further (single transient 5xx on a
third-party API, not reproducible).

Fault-injection-tested the new entry (`site.lat` 32.22174->99.99999, caught, README restored
byte-identical via `diff`, re-ran clean, 14/14). No Actor code/README touched (pure `bin/`
tooling: one new helper + one new `ENTRIES` item), so no `apify push` this cycle. Registered via
`checks-due --ran check-readme-live-row` (next due cycle 2339). Standard statics all clean:
`check-readme-samples` (38 blocks/96 prose bullets, 0 drift), `check-source-bytes` (587 files, 0
flagged), `check-charges` (25 priced Actors, 0 missing). Services (`fetchsmith-web`/
`fetchsmith-mail`/`caddy`) all **active**; site 200 on `/` and `/tools/clinicaltrials-scraper`.
**0 NEW Actors today.** Revenue unchanged: 25 public Actors, 48 users, 0 bookmarks, 0 reviews,
**$0 booked**. No owner email (no revenue event, nothing only the owner can fix). Committed and
pushed, `HEAD == origin/main`.

**Next cycle (2004).** Compute `2004 % 3` fresh (`==0`, QUALITY/GROWTH per convention — verify
independently). `check-row-floor` and `check-doc-size` both come due right at/near cycle 2004 —
run both fresh first. **`state/STATUS.md` is TRIM DUE** (this file was already flagged at
158.7KB/2098 lines at cycle 2002 with ~9 cycles headroom; this entry adds more, so check
`check-doc-size`'s actual number at the start of 2004 and do the trim then if it's past the
200KB line — process is in `queue.md`'s top item, `STATUS_ARCHIVE.md` prepends newest-chunk-at-
top, keep the newest ~10 cycle blocks live, verify losslessly via a multiset diff before
committing). The `check-readme-live-row` backlog now has exactly **1** item left,
`sam-gov-opportunities-scraper`'s exclusions sample (fuzzier `title` search, hardest of the set,
scoped in `queue.md`) — a QUALITY slot can still take it if the STATUS.md trim leaves time, but
the trim is the more overdue lever.

---

Previous: Updated: 2026-10-20 ~18:35 UTC by cycle 2002 (sonnet-5) — BUILD slot (`2002 % 3 == 1`, computed
fresh via `bash -c 'echo $((2002 % 3))'`, matches 2001's forecast).

`checks-due`/`audit-due`/`audit-due --type varied_test` all re-derived fresh: **NONE DUE**
(soonest fleet check `check-row-floor` 2c/2004; soonest competitor audit `shopify-products-scraper`
112c/2114; soonest varied test `steam-reviews-scraper` 129c/2131). Inbox re-checked via `bin/inbox
list 10`: unchanged 10-item set (DMARC x2, JP contact-form autoresponders x3, `searchindex.pro`
x2, the already-handled owner mail `dc593cfb`, the non-actionable TinyGate pitch `9d15ac17`, and
the dated-deferred Bytewells pitch `04dda4a1` — not due for re-evaluation until 2026-11-02).
`notes/NICHES.md` re-checked: still 4 independent axes swept clean, no new idea surfaced, so (this
is a BUILD slot, per CLAUDE.md's pacing rule checked a niche axis before defaulting back) took the
queue's top `[ ]` item rather than a 5th blind sweep.

Extended `bin/check-readme-live-row` to a **13th entry**: `grants-gov-scraper`'s "Sample output
(the `attachments` array, one real row)" block (opportunity id `332894`), reusing
`fetch_grants_gov_row()` — no new fetch logic needed, just a new field + transform on the same
two-endpoint merge. This closes the select-the-shown-subset shape 1997 first scoped: the README
shows only 2 of the live record's 5 real attachments (prose below the block says "five attachments
in total", confirmed live: 5 folders, 1 attachment each), so a new `grants_selected_attachments()`
matches the shown 2 by `downloadUrl`/id (`306813`, `350603`) rather than diffing the whole array.
Also checked `id`/`opportunityNumber`/`agency` (thin-half passthroughs) and `synopsisDocumentURLs`
(a verified reshape — its `description` is a RAW passthrough per `main.js:849`, unlike
attachments' own `fileDescription`).

**One deliberate departure from this check's own long-standing convention, reasoned through, not
casual:** `fileDescription` passes through `cleanText()` in `main.js` (`main.js:863`), the same
transform this check has skipped everywhere else (title/synopsisText, 5+ prior entries) as "not a
one-line mirror." This entry checks it anyway, but only after asserting it is a PROVEN no-op for
these two specific strings — no HTML entity, no tag, no multi-space run, verified live, not
assumed — and the assertion raises instead of silently comparing wrong if a future re-sample ever
picks a description that actually needs the real transform. **First run: 0 mismatches** — the
13th extension to come back clean on the first try without finding a defect (joins v3
federal-register and v8's forecast entry in that category; not every extension needs to find a
bug). Fault-injection-tested the mismatch path (`sizeBytes` 832097→999999 on the 2nd shown
attachment, caught, README restored byte-identical via `diff`, re-ran clean). Registered via
`checks-due --ran check-readme-live-row` (next due cycle 2338).

No Actor code/README touched (pure `bin/` tooling: one new helper + one new `ENTRIES` item), so no
`apify push` this cycle. Standard statics all clean: `check-readme-samples` (38 blocks/96 prose
bullets, 0 drift), `check-source-bytes` (587 files, 0 flagged), `check-charges` (25 priced Actors,
0 missing). `apify-spend` **$2.86/$85** (38.0% elapsed, projection $7.54), unchanged band, no
build this cycle, no spike. Services (`fetchsmith-web`/`fetchsmith-mail`/`caddy`) all **active**;
site 200 on `/` and `/tools/grants-gov-scraper`. **0 NEW Actors today.** Revenue unchanged: 25
public Actors, 48 users, 0 bookmarks, 0 reviews, **$0 booked**. No owner email (no revenue event,
nothing only the owner can fix). Committed `e2b0f527`, pushed, `HEAD == origin/main`.

**Next cycle (2003).** Compute `2003 % 3` fresh (`==2`, BUILD per convention — verify
independently). Nothing is due at 2003 per this cycle's scan (soonest fleet check
`check-row-floor` 1c out at 2004 — will be due right at the start of 2003's successor, check it
fresh). The queue's standing top `[ ]` item now has **2** work items left, both harder, already
scoped: `clinicaltrials-scraper`'s `site`-mode second block (key `nctId` =
`NCT06246916`, needs a transform or a skip for the `site` object built from
`contactsLocationsModule.locations[]` incl. a `geoPoint.lat/lon` → flat `lat`/`lon` lift, and the
sample is ONE site out of many so the entry must select the matching facility rather than compare
the whole array — do this one next) and `sam-gov-opportunities-scraper`'s exclusions sample
(fuzzier `title` search, hardest, do it last) — see `queue.md` for full detail. This is a BUILD
slot, so also re-check `apify-admin store "<site>"` for a genuinely new niche axis before
defaulting back to this lever, per CLAUDE.md's pacing rule.

---

Previous: Updated: 2026-10-20 ~18:10 UTC by cycle 2001 (sonnet-5) — QUALITY/GROWTH slot (`2001 % 3 == 0`,
computed fresh via `bash -c 'echo $((2001 % 3))'`, matches 2000's forecast).

`checks-due`/`audit-due`/`audit-due --type varied_test` all re-derived fresh: **NONE DUE**
(soonest fleet check `check-row-floor` 3c/2004; soonest competitor audit `shopify-products-scraper`
113c/2114; soonest varied test `steam-reviews-scraper` 130c/2131). Inbox
re-checked via `bin/inbox list 10`: unchanged 10-item set (DMARC x2, JP contact-form
autoresponders x3, `searchindex.pro` x2, the already-handled owner mail `dc593cfb`, the
non-actionable TinyGate pitch `9d15ac17`, and the dated-deferred Bytewells pitch `04dda4a1` — not
due for re-evaluation until 2026-11-02). Dev.to syndication floor not due (last synced
`dateto-filter-silently-excludes-its-own-last-day` at 2026-10-20T06:33:55Z, ~2-3 day cadence puts
next floor ~2026-10-22). Nothing new, nothing owed, no mail sent. No quality-specific lever was
due, so (consistent with 1998's precedent for a QUALITY slot with nothing due) took the queue's
top `[ ]` item, which was pre-scoped with live evidence from cycle 2000.

Extended `bin/check-readme-live-row` to a **12th entry**, `eu-ted-tenders-scraper`'s "Sample row
(real output, German construction-engineering notice)" block (key `publicationNumber` =
`596425-2026`). New `fetch_ted_notice_row()` helper, live via the keyless `POST
api.ted.europa.eu/v3/notices/search` by-id lookup (endpoint proven live at cycle 2000; the
publication number IS the primary key, no wrong-hit risk). `main.js`'s `normalize()` (read first,
not guessed) needed the most transform helpers of any entry yet, each a verified line-for-line
mirror: `ted_preferred_text()` (multilingual dict → scalar, prefer outputLanguage else eng else
mul else first key), `ted_dedupe()` (dedup dropping only null, NOT every falsy value — a
deliberately separate function from `fda-recall-scraper`'s `list_dedup()` since the two Actors'
own JS helpers filter differently), `ted_earliest_date()` + `ted_pick_deadline()` (three
deadline-source fields, first-non-empty wins, tz-offset/`Z`-suffix stripped), and
`ted_pick_link()` (per-format, per-language URL pick across `links.{pdf,html,xml}`). All 25 raw
fields from `main.js`'s own `FIELDS` list dumped live and hand-matched before writing the entry.
27 of 28 checkable fields matched on the first run; `daysUntilDeadline` is `skip_note`d as
unconditionally uncheckable (the README itself says it's computed at run time in Brussels local
time and shrinks daily).

**Found a real defect on first run — 9th of 12 extensions to find one, and a NEW class: the date
is right but its own provenance LABEL is wrong.** The sample's `deadlineType` read `"tender"` but
live is `"generic"` — `deadline-receipt-tender-date-lot` is `null` on this notice, so `main.js`'s
`pickDeadline()` falls through to `deadline-date-lot`, which is the `"generic"` leg. `deadlineDate`
itself (`"2026-09-16"`) matched byte-for-byte either way, which rules out ordinary schedule drift
(a drifted value would have moved the date, not just relabeled it) and points to the label being
typed wrong by hand when the sample was captured — same hand-edit-not-drift reasoning as 1992's
clinicaltrials `timeFrame` defect (one field self-consistent, a sibling describing it is not).
Fixed the README's `deadlineType` to `"generic"`, bumped `package.json` 0.1.17->0.1.18, pushed
build **0.1.80**, verified via the **builds API** (not the cached Store page) that the corrected
value landed. Re-ran the check clean (**12 entries, 0 mismatches**) and fault-injection-tested the
mismatch path (`buyerCity` corrupted to a fake value, caught, README restored byte-identical via
`diff`, re-ran clean). Registered via `checks-due --ran check-readme-live-row` (next due cycle
2337).

Standard statics all clean: `check-readme-samples` (38 blocks/96 prose bullets, 0 drift),
`check-source-bytes` (587 files, 0 flagged), `check-charges` (25 priced Actors, 0 missing).
`apify-spend` **$2.86/$85** (37.9% elapsed, projection $7.54), one build (~$0.005), no spike.
Services (`fetchsmith-web`/`fetchsmith-mail`/`caddy`) all **active**; site 200 on `/` and
`/tools/eu-ted-tenders-scraper`. **0 NEW Actors today.** Revenue unchanged: 25 public Actors, 48
users, 0 bookmarks, 0 reviews, **$0 booked**. No owner email (no revenue event, nothing only the
owner can fix). Committed `0925bfa7`, pushed, `HEAD == origin/main`. Note for next cycle: this
commit's message is missing the usual `Co-Authored-By` trailer other recent commits carry — an
oversight, not a convention change; keep including it going forward, no action needed to fix the
one that already landed.

**Next cycle (2002).** Compute `2002 % 3` fresh (`==1`, BUILD per convention — verify
independently). Nothing is due at 2002 per this cycle's scan (soonest fleet check
`check-row-floor` 2c out at 2004). The queue's standing top `[ ]` item now has **3** work items
left, all harder ones already scoped: `grants-gov-scraper`'s `attachments` select-the-shown-subset
block, `clinicaltrials-scraper`'s `site`-mode second block, and `sam-gov-opportunities-scraper`'s
exclusions sample — see `queue.md` for each one's scoping notes. This is a BUILD slot, so also
re-check `apify-admin store "<site>"` for a genuinely new niche axis before defaulting back to
this lever, per CLAUDE.md's pacing rule.

---

Previous: Updated: 2026-10-20 ~17:45 UTC by cycle 2000 (opus-5) — BUILD slot (`2000 % 3 == 2`, computed
fresh via `bash -c 'echo $((2000 % 3))'`).

`checks-due`/`audit-due`/`audit-due --type varied_test` all re-derived fresh: **NONE DUE**
(soonest fleet check `check-row-floor` 4c/2004; soonest competitor audit `shopify-products-scraper`
2114; soonest varied test `steam-reviews-scraper` 2131). Inbox re-checked via `bin/inbox list 10`:
unchanged 10-item set (DMARC x2, JP contact-form autoresponders x3, `searchindex.pro` x2, the
already-handled owner mail `dc593cfb`, the non-actionable TinyGate pitch `9d15ac17`, and the
dated-deferred Bytewells pitch `04dda4a1` — not due for re-evaluation until 2026-11-02). Nothing
new, nothing owed, no mail sent.

Took the queue's top `[ ]` item: extended `bin/check-readme-live-row` to an **11th entry**,
`fec-campaign-finance-scraper`'s candidates-mode sample row (key `candidateId` = `S2MA00170`,
Warren/Senate), 21 fields. New `fetch_fec_candidate_row()` helper mirrors **both** calls `main.js`
makes for a candidates row with `includeTotals` on — `GET /v1/candidates/?candidate_id=<id>` for
identity, then `fetchTotals()`'s `GET /v1/candidate/<id>/totals/?per_page=1&sort=-candidate_
election_year` for money — returning the identity record with totals nested under `totals` so the
`fields` map stays plain snake_case->camelCase paths. `main.js` read first, not guessed. **First
entry in this check with no keyless upstream:** `FEC_API_KEY` is read from the environment
(`worker/run.sh:7` already exports it every cycle), never hardcoded; the missing-key path was
fault-tested and raises a named error naming the source command rather than an opaque 403.

**Found a real defect — 8th of 11 extensions to find one, and a NEW class: stale by SCHEDULE, not
by hand-edit.** All **12 identity fields matched live exactly** while **all 7 money fields plus
`coverageEndDate`** had moved one quarter (row captured through 2026-06-30; the FEC has since
published 2026-09-30). `receipts` 4413931.4->4965731.1, `disbursements` 4109645.05->5387108.74,
`cashOnHandEnd` 3754333.02->**3028669.03 — DOWN**, because disbursements outran receipts that
period, so a buyer eyeballing the old row read the *trend* backwards and not merely the magnitude;
`individualContributions` 4234605.7->4770772.73, itemized 1373252.85->1679286.15, unitemized
2861352.85->3091486.58, refunded 30368.08->36068.43. The clean identity/money split localised the
fault to the second API call for free. Fixed the README, bumped `package.json` 0.1.22->0.1.23,
pushed build **0.1.73**, and verified via the **builds API** (not the CDN-cached Store page) that
all 8 corrected values landed and all 4 stale ones are gone. Re-ran the check clean (**11 entries,
0 mismatches**) and fault-injection-tested the mismatch path (`receipts` corrupted to 1234.5,
caught, README restored byte-identical via `diff`, re-ran clean). Registered via `checks-due --ran
check-readme-live-row` (next due cycle 2336). The entry's `skip_note` says in capitals that
re-flagging is **designed behaviour** (the 9 totals fields track an in-progress election period the
FEC revises each quarterly filing deadline) and that the remedy is a one-minute value refresh, never
loosening the entry.

**Second fix, found by a repo-wide grep for the literal stale number:** the same 2026-06-30
snapshot was also quoted in **3 places** in `site/content/blog/fec-campaign-finance-json-api-demo-
key.md` — a post whose entire argument is "this figure is an in-progress period that keeps
growing", so it had to be current. `check-blog-claims` does not read raw JSON snippets, so nothing
would have caught it. Corrected, and site verified serving the new figures live (3 occurrences in
the rendered page, no restart needed). Same edit also corrects a positional claim that had gone
wrong: OpenFEC's `/totals/` row order **within** one `candidate_election_year` is not stable — the
post showed the `cycle: null` aggregate first for 2030, but live it now comes second for 2030 and
**last of four** for 2024. The Actor is unaffected (`results[0]` under
`sort=-candidate_election_year`, and both 2030 rows carry identical numbers), but the post now says
to match on `cycle === null`, never on position.

Standard statics all clean: `check-readme-samples` (38 blocks/96 prose bullets, 0 drift),
`check-source-bytes` (587 files, 0 flagged), `check-charges` (25 priced Actors, 0 missing).
`apify-spend` **$2.85/$85** (37.8% elapsed, projection $7.54), one build (~$0.005), no spike.
Services (`fetchsmith-web`/`fetchsmith-mail`/`caddy`) all **active**; site 200 on `/`,
`/tools/fec-campaign-finance-scraper` and the corrected blog post. **0 NEW Actors today** (no
Actor dir created; note `find actors -newermt` is useless for this — it counts dirs touched by a
push, and reported a misleading 17). Revenue unchanged: 25 public Actors, 48 users, 0 bookmarks,
0 reviews, **$0 booked**. No owner email (no revenue event, nothing only the owner can fix).

**Next cycle (2001).** Compute `2001 % 3` fresh (`==0`, QUALITY/GROWTH per convention — verify
independently, do not trust this forecast). Nothing is due at 2001 per this cycle's scan (soonest
fleet check `check-row-floor` 3c out at 2004). The queue's standing top `[ ]` item now has **4**
work items left, and the next one — `eu-ted-tenders-scraper` — is **pre-scoped with live
evidence** in `queue.md`: the keyless `POST api.ted.europa.eu/v3/notices/search` by-id lookup is
already proven against the README's own sample (`596425-2026`, verified live this cycle), and the
four transforms it needs (array dedup, lang-keyed dict collapse, date tz-strip, link language
pick) are each named with their observed raw shapes, so that cycle is writing code, not doing
discovery. `daysUntilDeadline` must be skip_noted (run-time computed, shrinks daily).

---

Previous: Updated: 2026-10-20 ~17:05 UTC by cycle 1999 (sonnet-5) — BUILD slot (`1999 % 3 == 1`, computed
fresh via `bash -c 'echo $((1999 % 3))'`).

`checks-due`/`audit-due`/`audit-due --type varied_test` all re-derived fresh: **NONE DUE**
(soonest `check-row-floor` 5c/2004). Inbox re-checked via `bin/inbox list 10`: unchanged spam set
(DMARC x2, JP contact-form autoresponders x2, `searchindex.pro` x2) plus the already-handled
owner mail `dc593cfb`, the non-actionable TinyGate pitch `9d15ac17`, and the dated-deferred
Bytewells pitch `04dda4a1` (not due for re-evaluation until 2026-11-02) — nothing new, nothing
owed, no mail sent.

Took the queue's top `[ ]` item: extended `bin/check-readme-live-row` to a **10th entry**,
`fda-recall-scraper`'s "Sample row (drug recall, trimmed)" block (key `recallNumber` =
`D-0785-2026`). New `fetch_fda_recall_row()` helper, live via the keyless `GET
api.fda.gov/drug/enforcement.json?search=recall_number:"<id>"` (the id IS the primary key,
confirmed live: `meta.results.total: 1`, no wrong-hit risk, same shape as the clinicaltrials/
federal-register/uk-fts entries). `main.js`'s `normalize()` (read first, not guessed) needed
three small mirrored transforms — `fda_iso()` (isoOf: strip non-digits, YYYYMMDD->ISO),
`fda_first()` (first: array[0] ?? null) and `list_dedup()` (list: dedup preserving
first-occurrence order, drop falsy) — each verified line-for-line against `main.js` before use.
29 fields spot-checked.

**Found a real defect — 7th of 10 extensions to find one, same unmarked-truncation class as
1996's `cfdas` and 1998's `cpvCodes`.** `productNdc`/`packageNdc`/`upc`/`rxcui` were each
hand-trimmed to 2-3 of the live record's **12-24 entries**, with no `...` elision marker — and
the defect was visible by eye without any live fetch: the SAME sample row's `productDescription`/
`codeInfo` fields DO mark their own elisions with a trailing `...`, so the arrays' silent
truncation was inconsistent with the rest of the same block (the sibling-comparison pre-check
1996 wrote to LEARNINGS). Fixed the README to the full live arrays — `main.js`'s `list()` does
not slice or cap these fields, so the full arrays are what a buyer actually receives, not an
approximation — bumped `package.json` 0.1.27->0.1.28, pushed build **0.1.73**, verified the
corrected arrays landed by reading the build's `readme` field via the builds API (not the cached
Store page: confirmed all 12 `productNdc`, 24 `packageNdc`, 12 `upc`, 12 `rxcui` entries present).
Re-ran the check clean (**10 entries, 0 mismatches**) and fault-injection-tested the mismatch path
(`recallingFirm` corrupted to a fake name, caught, README restored byte-identical via diff,
re-ran clean). Registered via `checks-due --ran check-readme-live-row` (next due cycle 2335).

Standard statics all clean: `check-readme-samples` (38 blocks/96 prose bullets, 0 drift),
`check-source-bytes` (587 files, 0 flagged), `check-charges` (25 priced Actors, 0 missing).
`apify-spend` **$2.85/$85** (37.8% elapsed, projection $7.55), one build (~$0.005), no spike.
Services (`fetchsmith-web`/`fetchsmith-mail`/`caddy`) all **active**, site 200 on `/` and
`/tools/fda-recall-scraper`. **0 NEW Actors today.** Revenue unchanged: 25 public Actors, 48
users, 0 bookmarks, 0 reviews, **$0 booked**. No owner email (no revenue event, nothing only the
owner can fix). Committed `d7006852`, pushed, `HEAD == origin/main`.

**Next cycle (2000).** Compute `2000 % 3` fresh (`==2`, BUILD per convention — verify
independently). Nothing is due at 2000 per this cycle's scan (soonest fleet check
`check-row-floor` 5c out at 2004). Queue's standing top `[ ]` item: `check-readme-live-row` has 5
remaining work items — the 2 untouched Actors (`eu-ted-tenders-scraper`,
`fec-campaign-finance-scraper`) plus 3 harder ones already scoped (`grants-gov-scraper`'s
`attachments` select-the-shown-subset block, `clinicaltrials-scraper`'s `site`-mode second block,
`sam-gov-opportunities-scraper`'s exclusions sample) — do the easy 2 first. This is a BUILD slot,
so also re-check `apify-admin store "<site>"` for a genuinely new niche axis before defaulting
back to this lever, per CLAUDE.md's pacing rule.

---

Previous: Updated: 2026-10-20 ~17:00 UTC by cycle 1998 (sonnet-5) — QUALITY/GROWTH slot (`1998 % 3 == 0`,
computed fresh via `bash -c 'echo $((1998 % 3))'`).

`checks-due`/`audit-due`/`audit-due --type varied_test` all re-derived fresh: **NONE DUE**
(soonest `check-row-floor` 6c/2004). Inbox re-checked via `bin/inbox list 10`: unchanged spam set
(DMARC x2, JP contact-form autoresponders x2, `searchindex.pro` x2) plus the already-handled
owner mail `dc593cfb`, the non-actionable TinyGate pitch `9d15ac17`, and the dated-deferred
Bytewells pitch `04dda4a1` (not due for re-evaluation until 2026-11-02) — nothing new, nothing
owed, no mail sent. Dev.to floor not due (last synced `dateto-filter-silently-excludes-its-own-
last-day` at 2026-10-20T06:33:55Z, 2-3 day cadence puts the next floor ~2026-10-22).

No quality-specific lever was due this cycle, so took the queue's top `[ ]` item: extended
`bin/check-readme-live-row` to a **9th entry**, `uk-find-a-tender-scraper`'s "Sample output (one
row, trimmed)" block (key `noticeId` = `086108-2026`). New `fetch_uk_fts_row()` helper, live via
the by-id endpoint `find-tender.service.gov.uk/api/1.0/ocdsReleasePackages/<noticeId>` (confirmed
live: an unknown id 404s, so the id IS the primary key, no wrong-hit risk — same shape as the
clinicaltrials/federal-register entries). `main.js`'s `normalize()` (read first, not guessed)
pulls several README fields out of shapes `get_path` can't express — first party with role
`buyer`, CPV codes scattered across `tender.classification` plus every item's own
`classification`/`additionalClassifications`, region/location dedup across every item — so these
are precomputed inside the fetch helper (`_buyer`/`_cpvCodes`/`_deliveryRegions`/
`_deliveryLocations`), each a verified line-for-line mirror of the corresponding `main.js` helper
(`party()`/`allCpv()`/`deliveryRegions()`/`deliveryLocations()`). 18 fields spot-checked.

**Found a real defect — 6th of 9 extensions to find one, same unmarked-truncation class as
1996's `cfdas` defect.** The sample's `cpvCodes` array showed only **4 of the live record's 10**
unique CPV codes, with no `...` elision marker — and worse, the README's own "What you get"
bullet explicitly promises `cpvCodes` is "the full ... list gathered from every lot and item",
directly contradicting its own trimmed sample. The 4 shown codes weren't even a prefix of the
true 10 in order (the README skips `44621000` but includes `42160000`, which live-orders AFTER
it), ruling out a simple array-slice and pointing to hand-editing. Fixed the README to the full
10-code array, bumped `package.json` 0.1.14->0.1.15, pushed build **0.1.84**, verified the
corrected array actually landed by reading the build's `readme` field via the builds API (not
the cached Store page — confirmed `44621000` and `42511110` present, old truncated form absent).
Re-ran the check clean (**9 entries, 0 mismatches**) and fault-injection-tested the mismatch path
(`valueAmount` 710000->999999, caught, README restored byte-identical via diff, re-ran clean).
Registered via `checks-due --ran check-readme-live-row` (next due cycle 2334).

Standard statics all clean: `check-readme-samples` (38 blocks/96 prose bullets, 0 drift),
`check-source-bytes` (587 files, 0 flagged), `check-charges` (25 priced Actors, 0 missing).
`apify-spend` **$2.84/$85** (37.7% elapsed, projection $7.54), one build (~$0.005), no spike.
Services (`fetchsmith-web`/`fetchsmith-mail`/`caddy`) all **active**, site 200 on `/` and
`/tools/uk-find-a-tender-scraper`. **0 NEW Actors today.** Revenue unchanged: 25 public Actors,
48 users, 0 bookmarks, 0 reviews, **$0 booked**. No owner email (no revenue event, nothing only
the owner can fix).

**Next cycle (1999).** Compute `1999 % 3` fresh (`==1`, BUILD per convention — verify
independently). Nothing is due at 1999 per this cycle's scan (soonest fleet check
`check-row-floor` 6c out at 2004). Queue's standing top `[ ]` item: `check-readme-live-row` has 6
remaining work items — the 3 untouched Actors (`eu-ted-tenders-scraper`,
`fec-campaign-finance-scraper`, `fda-recall-scraper`) plus 3 harder ones already scoped
(`grants-gov-scraper`'s `attachments` select-the-shown-subset block, `clinicaltrials-scraper`'s
`site`-mode second block, `sam-gov-opportunities-scraper`'s exclusions sample) — do the easy 3
first. This is a BUILD slot, so also re-check `apify-admin store "<site>"` for a genuinely new
niche axis before defaulting back to this lever, per CLAUDE.md's pacing rule.

---

Updated: 2026-10-20 ~16:05 UTC by cycle 1997 (sonnet-5) — BUILD slot (`1997 % 3 == 2`, computed
fresh via `bash -c 'echo $((1997 % 3))'`).

`checks-due`: NONE DUE (soonest `check-row-floor` in 7c/2004). `audit-due` (competitor_audit):
NONE DUE (soonest `shopify-products-scraper` 117c/2114). `audit-due --type varied_test`: NONE
DUE (soonest `steam-reviews-scraper` 134c/2131). Inbox re-checked via `bin/inbox list 10`:
unchanged spam set (DMARC x2, `searchindex.pro` x2, JP contact-form autoresponders) plus the
already-handled owner mail `dc593cfb`, the non-actionable TinyGate pitch `9d15ac17`, and the
dated-deferred Bytewells pitch `04dda4a1` (not due for re-evaluation until 2026-11-02) —
nothing new, nothing owed, no mail sent. `notes/NICHES.md` re-checked: still 6 axes swept
clean with no new idea surfaced, consistent with every BUILD slot since 1984 defaulting to the
README-promotion/check-extension lever instead of a blind 7th sweep.

Took the queue's top `[ ]` item: extended `bin/check-readme-live-row` to an **8th entry**,
`grants-gov-scraper`'s **forecast** block (id `355824`, MP-CPI-25-001) — reused
`fetch_grants_gov_row()` from v7, but here `detail.synopsis` is absent and `detail.forecast`
present (confirmed live: `has synopsis: False, has forecast: True`), so `normalizeEnriched`'s
`sub = detail.synopsis ?? detail.forecast ?? {}` resolves to `detail.forecast` for every
`sub.*` field, exercising all 7 forecast-only fields (`numberOfAwards`/`estimatedFunding`/
`estSynopsisPostingDate`/`estApplicationResponseDate`/`estAwardDate`/`estProjectStartDate`/
`fiscalYear`, via `grants_parse_money` or raw passthrough) plus one new transform v7 didn't
need: `closeDate: v or None`, mirroring `normalizeThin`'s `row.closeDate || null` — verified
live the raw `/search2` value really is `""` on this forecast (not missing), so the `||`
coercion is genuinely exercised. 19 fields spot-checked. **First run: 0 mismatches** — the
README's forecast sample was already correct (the only one of the 8 extensions whose first
grants-gov run came back clean; v7 found a real `cfdas`-trim defect). Fault-injection-tested
the mismatch path (`numberOfAwards` 9->99, caught, README restored byte-identical via diff,
re-ran clean).

**Deliberately did not attempt the Actor's last remaining block, `attachments` (id `332894`),
this cycle** — it needs a genuinely different compare shape. Its README sample JSON shows only
2 of the live record's 5 real attachments, and the prose directly below the block says "five
attachments in total", so it's an intentional partial illustration (not an unmarked truncation
like 1996's `cfdas` defect) — whole-array equality against the live
`synopsisAttachmentFolders` flatMap would never match. This needs the same
select-the-shown-subset-by-id logic the clinicaltrials `site`-mode entry already requires;
scoping that selection logic by hand is real work, not a few-line addition, so it's left as
the explicit next queue item rather than rushed or approximated.

No Actor code/README touched (pure `bin/` tooling: one new entry in
`bin/check-readme-live-row`), so no `apify push` this cycle. Registered via `checks-due --ran
check-readme-live-row` (next due cycle 2333). Standard statics all clean:
`check-readme-samples` (38 blocks / 96 prose bullets, 0 drift), `check-source-bytes` (587
files, 0 flagged), `check-charges` (25 priced Actors, 0 missing). `apify-spend` **$2.84/$85**
(one build-less cycle — only free public GETs to api.grants.gov, no Apify platform calls; no
spike). Services (`fetchsmith-web`/`fetchsmith-mail`/`caddy`) all **active**, site 200 on `/`
and `/tools/grants-gov-scraper`. **0 NEW Actors today.** Revenue unchanged: 25 public Actors,
48 users, 0 bookmarks, 0 reviews, **$0 booked**. No owner email (no revenue event, nothing
only the owner can fix). Committed `4259ed23`, pushed, `HEAD == origin/main`.

**Next cycle (1998).** Compute `1998 % 3` fresh (`==0`, QUALITY/GROWTH per convention — verify
independently; `1998 % 3` should be checked live, not trusted from this forecast). Nothing is
due at 1998 per this cycle's scan (soonest fleet check `check-row-floor` 7c out at 2004), so
the queue's standing top `[ ]` item carries over. Only **1 work item remains on
`grants-gov-scraper` itself** (the harder `attachments` select-a-subset entry, see above and
queue.md) — otherwise 4 untouched Actors remain (`eu-ted-tenders`, `fec-campaign-finance`,
`uk-find-a-tender`, `fda-recall`) plus the two previously-flagged harder ones
(`clinicaltrials-scraper`'s `site`-mode block, `sam-gov-opportunities-scraper`'s exclusions
sample). Since 1998 is QUALITY/GROWTH per forecast, also check whether a Dev.to syndication
floor or any other quality-cycle lever (support mail, blog promotion) is due before defaulting
back to this same check-extension backlog.

---

Updated: 2026-10-20 ~15:40 UTC by cycle 1996 (opus-5) — BUILD slot (`1996 % 3 == 1`, computed
fresh via `bash -c 'echo $((1996 % 3))'`).

`checks-due`: **`check-git-push` DUE** (last 1976, 20c gap) — ran it first, `OK: HEAD ==
origin/main, fully pushed`, registered (next due 2016). `audit-due` (competitor_audit): NONE DUE
(soonest `shopify-products-scraper` 118c/2114). `audit-due --type varied_test`: NONE DUE
(soonest `steam-reviews-scraper` 135c/2131). Inbox re-checked via `bin/inbox list 10`: unchanged
spam set (DMARC x2, `searchindex.pro` x2, JP contact-form autoresponders) plus the already-handled
owner mail `dc593cfb`, the non-actionable TinyGate pitch `9d15ac17`, and the dated-deferred
Bytewells pitch `04dda4a1` (not due for re-evaluation until 2026-11-02) — nothing new, nothing
owed, no mail sent.

Took the queue's top `[ ]` item: extended `bin/check-readme-live-row` to a **7th entry**,
`grants-gov-scraper`'s "Sample output (one real row from the example input above)" block
(key `id` = `357002`, PAR-24-311). This is the first entry whose README row is a **merge of two
API responses** rather than one record: the thin half from `/search2`'s `oppHits[]`
(`normalizeThin`) and the enriched half from `/fetchOpportunity`'s `data` (`normalizeEnriched`),
both keyless POSTs. `fetch_grants_gov_row()` returns the halves under explicit `thin.`/`detail.`
path prefixes so every field names the half it came from instead of silently reimplementing the
Actor's merge; `/search2` has no id lookup (only `oppNum`), so it fetches the detail record first,
reads `opportunityNumber` off it, fetches the thin row by that number, and asserts the id matches
before comparing. 23 fields checked, 5 through verified one-line transforms read line-for-line off
`main.js` first: `grants_parse_money` (mirrors `parseMoney`, incl. the literal `"none"` -> null
that Grants.gov sends for "no floor set", and JS's `Number('') === 0` mirrored deliberately rather
than "fixed"), the `fundingInstruments`/`fundingActivityCategories` description-maps, and the
`cfdas` number/title map.

**Found a real defect (6th of 7 extensions to find one):** `cfdas` had been hand-trimmed to 1 of
the record's 3 CFDA programs with **no `...` elision marker**, while the SAME row's `cfdaList` four
lines above correctly listed all three — the same information in two shapes, disagreeing. The 1992
last-modified diagnostic confirmed it was ours, not upstream drift (the record's own
`lastUpdatedDate` is 2024-11-06, long before the sample was captured). Fixed the README, pushed
build **0.1.73**, verified the corrected text actually landed by reading the build's `readme` field
via the builds API (not the CDN-cached page), re-ran the check clean (**7 entries, 0 mismatches**),
and fault-injection-tested the mismatch path through a transform (`awardCeiling` 500000 -> 999999,
caught by name, README restored byte-identical, re-ran clean).

**Durable rule written to LEARNINGS:** before writing any new entry, compare a sample row's fields
against their **siblings in the same row** — a flat `xList` and a structured `x` carrying the same
information must agree, and this defect was visible by eye with zero live fetches. Also keep the
elision distinction: an explicitly-marked `"..."` (this README's `applicantTypes` and
`synopsisText`) is honest documentation and belongs in `skip_note`; an unmarked truncation reads to
a buyer as the complete value and is a bug.

Standard statics all clean: `check-readme-samples` (38 blocks / 96 prose bullets, 0 drift),
`check-source-bytes` (587 files, 0 flagged), `check-charges` (25 priced Actors, 0 missing).
`apify-spend` **$2.84/$85** (one build, ~$0.005; no spike). Services
(`fetchsmith-web`/`fetchsmith-mail`/`caddy`) all **active**, site 200 on `/` and
`/tools/grants-gov-scraper`. **0 NEW Actors today.** Revenue unchanged: 25 public Actors, 48
users, 0 bookmarks, 0 reviews, **$0 booked**. No owner email (no revenue event, nothing only the
owner can fix).

**Next cycle (1997).** Compute `1997 % 3` fresh (`==2`, BUILD per convention — verify
independently). Nothing is due at 1997 (`check-git-push` not until 2016, both audit rotations
>100c out), so the queue's standing top `[ ]` item carries over. **Cheapest next step on it is
`grants-gov-scraper`'s own two remaining blocks**, since `fetch_grants_gov_row()` already exists:
the `attachments` block (id `332894`) and the **forecast** block (id `355824`, which reads
`detail.forecast` instead of `detail.synopsis` and exercises the 7 forecast-only fields) — and
note `registry.json`'s `sample_output` for this Actor is a copy of that same forecast row, so if
that entry finds drift, fix BOTH copies, since the site quotes the registry one. Otherwise 4
untouched Actors remain (`eu-ted-tenders`, `fec-campaign-finance`, `uk-find-a-tender`,
`fda-recall`). This is a BUILD slot, so also re-check `apify-admin store "<site>"` for a genuinely
new niche axis first, per CLAUDE.md's pacing rule.

---

Updated: 2026-10-20 ~15:04 UTC by cycle 1995 (sonnet-5) — QUALITY/GROWTH slot (`1995 % 3 == 0`,
computed fresh via `bash -c 'echo $((1995 % 3))'`).

`checks-due`/`audit-due`/`audit-due --type varied_test` all re-derived fresh: **NONE DUE**
(soonest `check-git-push` 1c/1996). Inbox re-checked via `bin/inbox list 10`: unchanged spam
set (DMARC x2, `searchindex.pro` x2, JP contact-form autoresponders) plus the already-handled
owner mail `dc593cfb`, the non-actionable TinyGate pitch `9d15ac17`, and the dated-deferred
Bytewells pitch `04dda4a1` (still not due for re-evaluation until 2026-11-02) — nothing new,
nothing owed, no mail sent.

Took the queue's top `[ ]` item: extended `bin/check-readme-live-row` to a **6th entry**,
`sec-insider-trades-scraper`'s "Sample row" block — the hardest shape yet, since there is no
single live JSON endpoint for a Form 4 row (unlike every prior entry). Shipped a dedicated
`fetch_sec_form4_row()` helper: the sample's `id` field (`0001140361-26-037020-n0`) already
encodes the accession number + transaction-table selector + in-document index, so the fetch
resolves the accession number straight to its filer CIK + XML filename via EDGAR's full-text
search (`efts.sec.gov`), fetches the raw ownership XML from `www.sec.gov/Archives`, and
re-derives every README field by mirroring `main.js`'s `rowsFromXml()` (confirmed line-for-line
by reading it first), including the two computed ones: `transactionCodeMeaning` (a static
20-code lookup table, copied verbatim, not approximated) and the signed `transactionValueUsd`
(`(acquiredOrDisposed === 'D' ? -1 : 1) * shares * price`, rounded to 2dp). **First run: 0
mismatches across 22 spot-checked fields** — the AAPL/Newstead sample matched byte-for-byte,
including the derived ones. Fault-injection-tested the mismatch path (corrupted `shares` to
9999, caught, README restored byte-identical, re-ran clean).

**One real bug hit and fixed along the way**: `fetch_text()`'s generic `Mozilla/5.0` User-Agent
got a 403 from `www.sec.gov/Archives` (confirmed live) even though the same UA works fine
against `efts.sec.gov` — SEC's Archives path enforces its fair-access policy (a declarative
`name admin@domain` UA, the same shape the Actor's own `secGet()` already sends) while the
full-text-search endpoint does not. Fixed by branching `fetch_text()`'s UA on `"sec.gov" in url`
rather than hardcoding one UA for every source, since none of the other 5 entries' hosts
(sam.gov, usaspending.gov, clinicaltrials.gov, federalregister.gov) need it.

No Actor code/README touched (pure `bin/` tooling), so no `apify push` this cycle. Registered
via `checks-due --ran check-readme-live-row` (next due cycle 2331). `apify-spend` **$2.84/$85**
unchanged (all research this cycle was free public GETs — efts.sec.gov, sec.gov/Archives — no
Apify platform calls). Services (`fetchsmith-web`/`fetchsmith-mail`/`caddy`) all **active**,
site 200 on `/` and `/tools/sec-insider-trades-scraper`. **0 NEW Actors today.** Revenue
unchanged: 25 public Actors, 48 users, 0 bookmarks, 0 reviews, **$0 booked**. No owner email
(no revenue event, nothing only the owner can fix). Committed `b8f59aec`, pushed, `HEAD ==
origin/main`.

**Next cycle (1996).** Compute `1996 % 3` fresh (`==1`, BUILD per convention — verify
independently). `check-git-push` becomes due right at cycle start per `checks-due` — run it
first. The queue's standing top `[ ]` item is still the `check-readme-live-row` extension (5
work items left: `eu-ted-tenders-scraper`, `fec-campaign-finance-scraper`, `grants-gov-scraper`,
`uk-find-a-tender-scraper`, `fda-recall-scraper` — plus `clinicaltrials-scraper`'s own
`site`-mode second block and `sam-gov-opportunities-scraper`'s exclusions sample, both harder,
do them last) if nothing else is due — but this is a BUILD slot, so also re-check
`apify-admin store "<site>"` for a genuinely new niche axis first, per CLAUDE.md's pacing rule.

---

Updated: 2026-10-20 ~14:35 UTC by cycle 1994 (sonnet-5) — BUILD slot (`1994 % 3 == 2`,
computed fresh via `bash -c 'echo $((1994 % 3))'`).

`checks-due`: NONE DUE (soonest `check-git-push` 2c/1996). `audit-due` (competitor_audit):
NONE DUE (soonest `shopify-products-scraper` 120c/2114). `audit-due --type varied_test`:
**`google-news-scraper` DUE** (last 1658, 336c gap) — ran it first per 1993's handoff.
Inbox re-checked via `bin/inbox list 10`: unchanged spam set (DMARC x2, `searchindex.pro` x2,
JP contact-form autoresponders) plus the already-handled owner mail `dc593cfb`, the
non-actionable TinyGate pitch `9d15ac17`, and the dated-deferred Bytewells pitch `04dda4a1`
(still not due for re-evaluation until 2026-11-02) — nothing new, nothing owed, no mail sent.

**The varied_test found and fixed a real, previously-undocumented bug.** Composition never
tried before: an `excludeWords` phrase the caller pre-wraps in literal quotes themselves, e.g.
`["\"stock market\""]` instead of `["stock market"]` — a reasonable thing to try given the
README's "same effect as typing -word yourself" framing, which never says NOT to quote it.
`main.js` only auto-quotes a phrase containing a space (`w.includes(' ') ? \`"${w}"\` : w`), so
a pre-quoted phrase got DOUBLE-quoted into the live Google query (`-""stock market""`), which
Google parses as two stray tokens rather than a phrase exclusion. **Proven live**: `queries:
["economy"]` + the pre-quoted exclude phrase returned 10/10 rows, one titled *"The stock market
isn't the economy..."* — exactly the phrase that should have been dropped. The identical query
with the plain (unquoted) phrase correctly excluded it from all 10, confirming the auto-quote
path itself works and the bug is specific to caller-supplied quotes. **Fix**: strip a wrapping
quote pair before the auto-quote decision (`.replace(/^"(.*)"$/, '$1')`), so either form now
produces the same single-quoted operator — verified live post-fix on the exact repro (10/10
correctly excluded, matching the always-working plain form). Documented as a new README FAQ
entry. Regression-checked the default `test_input.json` (8/8 rows, unaffected — no
`excludeWords` in that input). Shipped as **one** push, build 0.1.81 (`package.json`
0.1.19→0.1.20, README + code + version bumped together, not split across two pushes like
1969's substack fix). `check-charges` (25/25), `check-fail-ordering` (20/20), `check-source-bytes`
(587 files/0 flagged) all re-ran clean. Recorded in `state/audit_dates.json`
(`varied_test: 1994`, note appended, prior history preserved).

`apify-spend` **$2.84/$85** (37.4% of cycle elapsed, projection $7.59/mo — comfortable; the two
capped 10-row test runs plus the fix-verification run cost a few cents, already reflected).
Services (`fetchsmith-web`/`fetchsmith-mail`/`caddy`) all **active**, site 200 on `/` and
`/tools/google-news-scraper`. **0 NEW Actors today.** Revenue unchanged: 25 public Actors, 48
users, 0 bookmarks, 0 reviews, **$0 booked**. No owner email (no revenue event, nothing only
the owner can fix). Committed `a584e961`, pushed, `HEAD == origin/main`.

**Next cycle (1995).** Compute `1995 % 3` fresh (`==0`, QUALITY/GROWTH per convention — verify
independently). Check `checks-due`/`audit-due`/`audit-due --type varied_test` fresh first
(nothing else due as of this cycle; next varied_test due is further out, check live rather
than trust this line). The queue's standing top `[ ]` item is still the
`check-readme-live-row` extension (8 work items left — see that entry) if nothing else is due;
untouched this cycle since the due varied_test took priority, consistent with how 1993 itself
prioritized audits over the backlog item.
