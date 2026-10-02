# ClinicalTrials.gov Scraper – Patient Recruitment & NCT IDs

Pulls studies from **ClinicalTrials.gov**, the US NIH/NLM clinical trial registry, using its own official API v2 — a clinical research API with no key, no login and no proxy. 602,520+ clinical trials covered.

## What you get

34 flat fields per study, including the ones most ClinicalTrials.gov Actors skip:

| Field | Why it matters |
| --- | --- |
| `rowsPerStudy: "site"` mode | One row per **trial site** instead of one per study — facility name, city, state, country and lat/lon, so a site-selection or patient-recruitment buyer doesn't have to explode the array themselves. A study averages 5 sites (max seen: 110), so this mode returns roughly 5x more billable rows for the same query. |
| `phases`, `studyType`, `overallStatus` | Filterable and returned flat, not nested. |
| `enrollmentCount`, `sex`, `minimumAge`, `maximumAge`, `healthyVolunteers`, `standardAges` | The eligibility snapshot without parsing free-text criteria. `enrollmentType` says whether that count is `ACTUAL` or `ESTIMATED` — an estimate on a running trial is a target, not a headcount. `standardAges` is the registry's own `CHILD`/`ADULT`/`OLDER_ADULT` bucketing, the same vocabulary the `ageGroups` filter uses. |
| `eligibilityCriteria` | The full inclusion/exclusion text as the registry publishes it. We deliberately **don't** pre-split it into separate inclusion and exclusion lists the way some competitors do: the split is a guess at prose with no fixed format, and mislabelling an exclusion criterion as an inclusion one is the one error a trial-screening buyer cannot afford. |
| `primaryOutcomes`, `secondaryOutcomes` | What the trial actually measures — `measure`, `timeFrame` and `description` per endpoint. These are what the `outcomeMeasure` filter searches, so you can see which endpoint matched your query instead of taking the filter on faith (the API searches the description too, not just the measure title). |
| `resultsFirstPostDate` | When the results section was first posted — the field the `resultsFirstPostedDateFrom`/`To` window ranges over. Null until a trial actually posts results. |
| `leadSponsorClass` | The lead sponsor's organization type (`NIH`, `INDUSTRY`, `FED`, etc.) — filterable via `funderTypes`. |
| `hasResults` | Whether the trial has posted a results section — filterable via `resultsAvailability` (with **or** without). |
| `interventions` | Type + name for every drug/device/procedure arm. |
| `studyUrl` | Direct link to the public study page. |

With `hasResults`, `primaryOutcomes` and `resultsFirstPostDate` flat on every row, this doubles as a study results API: set `resultsAvailability` to return only trials that have actually reported, or only the ones that never did.

**We do not ship contact people, phone numbers or emails — ever.** ClinicalTrials.gov's own API returns named individuals and personal email addresses in `centralContacts`/location `contacts` (we found a real `@gmail.com` in a live sample). Several competitor Actors resell that as a "contact finder." We deliberately drop it; `locations`/`site` carries facility, city, state, country and geo-coordinates only. A medical data API can be useful without reselling named individuals.

Name a `watchLabel` and every later run on the same saved search returns **only studies new since the last run**, so a scheduled competitive-intelligence pull never re-delivers or re-charges for the same trial twice; add `watchChanges` and it also catches a study's **status changing** (e.g. Recruiting → Completed/Terminated), a **protocol amendment updating its enrollment count**, or its **completion date slipping**.

## Who uses this

- **Pharma / CRO business development** tracking competitor trials by condition or sponsor.
- **Site-selection teams** finding which facilities run trials for a given condition (`rowsPerStudy: "site"`).
- **Investor / market research** watching a sponsor's pipeline by phase and status; add `watchChanges` to get alerted when a trial they already logged is upgraded, terminated, or has its readout date slip.
- **Patient-advocacy and recruitment groups** finding actively recruiting trials near a location.
- **COVID-19 and long-COVID researchers** pulling COVID trials by status, phase and site: `conditions: "COVID-19"` matches 10,246 registered studies (338 currently recruiting) and `"long COVID"` matches 733, and the COVID data comes back as the registry's own record — see the FAQ below.

## Input

```json
{
  "conditions": "breast cancer",
  "overallStatus": ["RECRUITING"],
  "phases": ["PHASE3"],
  "maxResults": 100
}
```

Or skip the form entirely and paste the search URL from clinicaltrials.gov:

```json
{
  "startUrl": "https://clinicaltrials.gov/search?cond=asthma&intr=budesonide&aggFilters=status:rec,phase:3&start=2020-01-01_",
  "maxResults": 100
}
```

| Input | Notes |
| --- | --- |
| `startUrl` | Build the search on clinicaltrials.gov, copy the address bar, paste it here — the condition, other terms, intervention, sponsor, location, title, outcome, lead sponsor and study-ID boxes plus every sidebar filter (status, phase, study type, funder, sex, age, results, documents, FDAAA violations) and every date window come across as-is. An API URL (`https://clinicaltrials.gov/api/v2/studies?query.cond=asthma&...`) works too. The URL's **search terms replace** the matching fields below; anything it doesn't mention (`maxResults`, `rowsPerStudy`, `watchLabel`, and any filter below the URL doesn't carry) still applies. A non-clinicaltrials.gov URL fails fast instead of quietly scraping nothing. |
| `nctIds` | Comma/space/newline-separated NCT IDs (e.g. `NCT04368728, NCT03854955`) for a direct lookup by ID instead of a search — what other Actors call "search by direct URL". **Exclusive mode**: when set, every filter below is ignored (so a mixed batch of unrelated trials all come back), and a malformed or nonexistent ID is dropped individually with a named warning instead of failing the whole batch. |
| `conditions` / `interventions` / `sponsors` / `locations` | Free-text, each maps to the API's own `query.cond` / `query.intr` / `query.spons` / `query.locn`. ANDed together. |
| `searchQuery` | General free-text search across titles, outcomes and eligibility text. |
| `overallStatus` | e.g. `RECRUITING`, `COMPLETED`, `TERMINATED`. All 14 official values supported. |
| `studyTypes` | `INTERVENTIONAL`, `OBSERVATIONAL`, `EXPANDED_ACCESS`. |
| `phases` | `EARLY_PHASE1`..`PHASE4`, `NA`. Only meaningful for interventional studies — about 1 in 5 studies overall have no phase at all. A study matches if the phase is anywhere in its phase list, so `["PHASE2"]` also returns combined `["PHASE1","PHASE2"]` trials. |
| `resultsAvailability` | `with` = only studies that posted a results section; `without` = only studies that never reported (the FDAAA-compliance question). Blank = both. Supersedes the older boolean `hasResultsOnly`, which still works. `without` cannot be combined with a `resultsFirstPostedDate` window — see the FAQ. |
| `ageGroups` | Standard age groups the study enrols: `CHILD` (0–17), `ADULT` (18–64), `OLDER_ADULT` (65+). Multiple = OR. Coarser and more reliable than `ageRangeFromYears`/`ageRangeToYears`, which only match studies that state a numeric bound. |
| `documentTypes` | Only studies that uploaded one of these documents: `prot` (study protocol), `sap` (statistical analysis plan), `icf` (informed consent form). Multiple = OR. About 9% of studies have any. |
| `fdaRegulationViolation` | Only studies carrying an FDA regulation (FDAAA 801) violation notice — 8 registry-wide, re-verified live 2026-09-26. Combine it with nothing else or you will get zero rows. |
| `sex` | `FEMALE` or `MALE` — restrict to studies whose eligibility criteria specify that sex. Leave blank for all. |
| `acceptsHealthyVolunteers` | Only studies that accept healthy volunteers, not just patients with the condition. |
| `lastUpdatePostedDateFrom` / `lastUpdatePostedDateTo` | Absolute `YYYY-MM-DD` window on the record's last-updated date — a repeatable "what changed since I last pulled" query, either bound optional. Setting `From` after `To` fails fast with an error instead of silently returning 0 rows. |
| `ageRangeFromYears` / `ageRangeToYears` | Only studies whose stated minimum/maximum eligibility age falls in this range, either bound optional. E.g. `ageRangeToYears: 65` excludes studies with no senior-age cap. Setting `From` above `To` in the same unit fails fast with an error instead of silently returning 0 rows. |
| `ageRangeFromUnit` / `ageRangeToUnit` | Unit for the two bounds above: `Years` (default), `Months`, `Weeks`, `Days`. Whole years are too coarse for neonatal and infant trials — `ageRangeToYears: 18` + `ageRangeToUnit: "Months"` finds the studies that stop enrolling before the second birthday (108 alongside a cancer query, vs 2,229 for the 18-**years** reading of the same number). Each bound carries its own unit. |
| `studyStartDateFrom` / `studyStartDateTo` | Absolute `YYYY-MM-DD` window on the study's **start date**. Either bound optional. Month-precision dates anchor to the 1st — see the partial-date FAQ below. |
| `primaryCompletionDateFrom` / `primaryCompletionDateTo` | Window on the **primary completion** date — the readout date a competitive-intelligence pull is usually actually about. Month-precision dates anchor to the 1st — see the partial-date FAQ below. |
| `studyCompletionDateFrom` / `studyCompletionDateTo` | Window on the **overall completion** date. Month-precision dates anchor to the 1st — see the partial-date FAQ below. |
| `firstPostedDateFrom` / `firstPostedDateTo` | Window on the date the study was **first posted** to ClinicalTrials.gov — the "newly registered trials" query. |
| `resultsFirstPostedDateFrom` / `resultsFirstPostedDateTo` | Window on the date **results** were first posted. Pairs with `resultsAvailability: "with"` (or a blank `resultsAvailability`). Pairing it with `"without"` fails fast with an error instead of silently returning 0 rows — see the FAQ. |
| `facilityName` | Only studies running at a facility whose name matches, e.g. `Mayo Clinic`. This is the **site/hospital name**, not the city — `locations` is the city/state/country field. Multi-word values are matched as a phrase, not as loose terms. |
| `leadSponsorName` | Only studies whose **lead** sponsor matches, e.g. `Pfizer`. Narrower than `sponsors`, which also matches collaborators. |
| `funderTypes` | Lead sponsor organization type: `NIH`, `FED` (other US federal), `OTHER_GOV`, `INDUSTRY`, `NETWORK`, `INDIV`, `OTHER` (academic/nonprofit), `UNKNOWN`, `AMBIG`. |
| `titleOrAcronym` | Search only the official/brief title and acronym — narrower than `searchQuery`. |
| `outcomeMeasure` | Search only the study's stated outcome measures, e.g. "overall survival". |
| `sortBy` | Order results before `maxResults` truncates them: most recently updated, most recently first-posted, or largest enrollment first. Default is the API's own relevance order. |
| `rowsPerStudy` | `"study"` (default) or `"site"`. |
| `maxResults` | Up to 50,000. Token-based paging, no offset wall. |
| `watchLabel` | Name a saved search to get only studies new since this label's last run (see FAQ). Leave empty for the normal full-match-set behaviour. Ignored when `nctIds` is set. |
| `watchChanges` | boolean | Optional, requires `watchLabel`. Also re-deliver an already-seen study if its `overallStatus`, `lastUpdatePostDate`, `enrollmentCount`, `primaryCompletionDate` or `completionDate` changed (default `false`) — see FAQ. |
| `webhookUrl` | Optional. POST a small JSON completion summary (rows pushed, studies scanned, pages walked, dataset ID, watch new/changed counts, plus the full `summary` completeness object) here when the run finishes — see FAQ. |

## Sample output (`rowsPerStudy: "study"`)

```json
{
  "nctId": "NCT04137653",
  "briefTitle": "Treatment of Triple-negative Breast Cancer With Albumin-bound Paclitaxel as Neoadjuvant Therapy",
  "overallStatus": "RECRUITING",
  "studyType": "INTERVENTIONAL",
  "phases": ["PHASE3"],
  "enrollmentCount": 1498,
  "enrollmentType": "ESTIMATED",
  "leadSponsor": "Shengjing Hospital",
  "conditions": ["Breast Cancer"],
  "interventions": [{"type": "DRUG", "name": "nab-Paclitaxel+carboplatin"}],
  "primaryOutcomes": [{"measure": "Pathologic complete response (PCR)", "timeFrame": "1 year", "description": "Pathologic complete remission refers to no invasive tumor cell remnants in the pathological examination of the primary mammary gland and axillary lymph nodes surgically removed..."}],
  "standardAges": ["ADULT", "OLDER_ADULT"],
  "eligibilityCriteria": "Inclusion Criteria:\n\n* breast cancer is confirmed by the mammography, and the im...",
  "resultsFirstPostDate": null,
  "locationCount": 1,
  "studyUrl": "https://clinicaltrials.gov/study/NCT04137653"
}
```

**Watch-mode change fields, only on a `watchChanges` re-delivery:** `_watchChangeType` (array, one or more of `overallStatus`/`lastUpdatePostDate`/`enrollmentCount`/`primaryCompletionDate`/`completionDate`), `_watchPrevious` (object with the previous value(s) for each changed field).

## The pageSize trap

Ask the API for `pageSize=1001` and it doesn't 400 — it silently returns **200 with only 1000 rows**, no warning. This Actor always clamps to 1000 and pages with the API's own `nextPageToken`, which has no offset wall (5,000+ unique rows walked in one run during testing, no rate limiting).

## Pricing

**$0.0015 per result, no Actor-start fee.** The niche's Store leader by users, `parseforge/clinicaltrials-scraper` (46 users), charges $0.16 to start plus $0.012/result on its free tier — about 8x more per row, with a start fee we don't charge at all. 1,000 studies costs $1.50 here vs. $12.16 there. All prices on this page were read from each Actor's live in-effect pricing record, verified 2026-10-02.

ClinicalTrials.gov is one of the most crowded niches on the Store — 40+ listings — so here is the wider field rather than one flattering comparison. **Dearer than us at every tier:** `logiover/clinicaltrials-gov-scraper` (24 users, the niche's second-largest listing) at $0.005/row (FREE) down to $0.003 (GOLD+), no start fee — 3.3x our rate at FREE, 2x at the best tier; `bovi/clinicaltrials-scraper` (4 users) at $0.0119 down to $0.011305; `scrapesage/clinical-trials-scraper` (2 users) at $0.004/trial, $0.008/site lead, $0.006/sponsor record; `dataio/clinicaltrials-sites-investigators` (2 users) at $0.006 down to $0.004 per trial site; `malonestar/clinical-trials-meta-search` (2 users) at $0.006 down to $0.0018; `thirdwatch/clinical-trials-gov-scraper` (2 users) at $0.004 down to $0.002; `themineworks/clinicaltrials-scraper` (2 users) at $0.0035 down to $0.0025 plus a $0.005 start fee; `scrapepilot/clinicaltrials-gov-aggregator-pharma-biotech-intelligence` (4 users) at $0.003 plus a $0.02 start fee; `devilscrapes/clinicaltrials-gov-scraper` (3 users) at $0.002 plus a $0.20 start fee; `ryanclinton/clinical-trial-tracker` (7 users) and `pink_comic/clinicaltrials-gov-search` (4 users) at $0.002. Two listings market themselves on price and are still dearer than us: `delectable_incubator/clinicaltrials-scraper-low-cost` (2 users) charges $0.00199 down to $0.00179, and `scrapestorm/clinicaltrials-gov-listings-scraper---cheap` (2 users) charges $0.00299.

**What we do not claim.** We are not the cheapest ClinicalTrials.gov Actor on the Store and we don't pretend to be. `webdata_labs/clinical-trials-api` (2 users) charges $0.001/record (FREE) down to $0.00075 (GOLD+) with no start fee — cheaper than us at every tier and every volume. `alizarin_refrigerator-owner/clinicaltrials-gov-api---clinical-study-data` (12 users) prices a run instead of a row — $0.10 to start plus $0.01 per search call plus $0.00001 per dataset item — so we are cheaper on small pulls but they are cheaper past roughly 75 rows in a single search ($0.12 vs. our $1.50 for 1,000 studies). Three listings carry Apify's FREE pricing model and charge no per-result fee at all, leaving you only the platform compute: `labrat011/clinical-trials-scraper` (4 users), `bikram07/clinical-trials-feed` (2 users) and `scrupulous_waterbird_m4w/clinical-trials-gov` (2 users). And `labrat011/clinical-trial-site-contact-finder` (5 users) undercuts our `rowsPerStudy: "site"` mode at $0.0007/row — but that is the contact-reselling product described above, which we deliberately do not ship. We have not run any of these Actors ourselves; we read their published prices, not their output quality, field coverage or reliability. What we do claim is what the field table above lists: 34 flat fields, site-level rows, `watchLabel`/`watchChanges` incremental delivery, no contact PII, and no start fee.

## FAQ

**I already have a list of NCT IDs — can I just fetch those?**
Yes, set `nctIds` (e.g. `"NCT04368728, NCT03854955"`) instead of the search filters. ClinicalTrials.gov's own API 400s the *entire* request if even one ID in a batch is malformed or doesn't exist — we've verified this live and handle it for you: bad IDs are dropped individually with a named warning, and the rest of your batch still comes back.

**Does this cover COVID-19 and long-COVID trials?**
Yes — COVID is just another condition here, so `conditions: "COVID-19"` matches 10,246 registered studies (338 of them currently recruiting, measured live 2026-09-28) and `conditions: "long COVID"` matches 733. Narrow with the ordinary filters: `overallStatus: ["RECRUITING"]` for open enrolment, `phases` for interventional stage, `rowsPerStudy: "site"` for one row per participating facility. Every row is copied straight from the registry, so the COVID data you get back is the sponsor's own record — no modelling and no case-count estimates — and that is why COVID trials, post-acute-sequelae (PASC) studies and vaccine follow-up studies all come through the same single condition filter.

**Why did I get zero rows?**
Filters are ANDed — combining a narrow condition, sponsor and location at once often genuinely matches nothing. Drop one filter and retry. Also, `phases` only applies to interventional studies with a phase assigned; pairing it with `studyTypes: ["OBSERVATIONAL"]` always returns nothing.

**Why can't I combine `resultsAvailability: "without"` with a `resultsFirstPostedDate` window?**
Because nothing can match it, so we stop the run and tell you instead of billing you for a search that was never going to return a row. `"without"` means the study has posted **no** results section, and a study with no results section has no results-posted date at all — there is nothing for the window to range over. Measured live registry-wide on 2026-09-30: `resultsAvailability: "without"` alone matches 524,648 studies and the widest conceivable results-posted window (1900→2100) matches 80,302, but the two **together** match **0** — as does an open-ended window with only a `From` or only a `To` bound. If you want trials that reported in a given period, use `resultsAvailability: "with"` (or leave it blank) with the window; if you want the FDAAA-compliance set of trials that never reported, keep `"without"` and filter on `studyCompletionDateFrom`/`To` or `primaryCompletionDateFrom`/`To` instead — those are the dates that actually exist on an unreported trial.

**There are six date filters — which one do I want?**
`firstPosted*` = when the trial was registered (new-trial alerts). `studyStart*` = when dosing/enrolment begins. `primaryCompletion*` = the primary-endpoint readout date, which is the one most competitive-intelligence pulls actually mean. `studyCompletion*` = last visit of the last patient. `resultsFirstPosted*` = when results were published. `lastUpdatePosted*` = when the record changed at all, which is the right one for an incremental "what's new since my last pull" job. Every pair is independent, ANDed with the rest, and either bound can be left blank for an open range.

**Why did a date window skip trials whose date looks like it's inside it?**
Because ClinicalTrials.gov lets sponsors enter a **month without a day**, and a month-precision date behaves as the **1st of that month** in every date window. Measured live (lung cancer, recruiting, Phase 2): `primaryCompletionDateFrom: "2026-06-01"` / `To: "2026-06-04"` — a four-day window — returns the trials whose `primaryCompletionDate` is the bare string `"2026-06"` (NCT05902988, NCT05913089), while `From: "2026-06-05"` / `To: "2026-06-25"` returns **only** full-date rows and drops them. So a "second half of June" query silently misses every June trial that never stated a day.

Which fields this hits: the three **sponsor-entered** dates — `startDate`, `primaryCompletionDate`, `completionDate` — are frequently month-only (on one live 10-row recruiting sample: `completionDate` 6/10, `startDate` 1/10). The three **registry-generated** dates — `studyFirstPostDate`, `lastUpdatePostDate`, `resultsFirstPostDate` — were full `YYYY-MM-DD` on 10/10 of that same sample, so `firstPostedDate*`, `lastUpdatePostedDate*` and `resultsFirstPostedDate*` windows are exact. Workaround for the sponsor-entered three: start the window on the **1st of the month** (widening it at most to the start of that month) and filter the rows yourself afterwards, since the row carries the date exactly as the registry publishes it.

**What's the difference between `facilityName` and `locations`?**
`locations` is the city/state/country text ("Boston, Massachusetts"); `facilityName` is the site name ("Mayo Clinic"). Use `facilityName` for site-selection and KOL work where you care which institution is running the trial, not where it sits. Multi-word values are sent as a quoted phrase, so `Mayo Clinic` does not also match a study at "Cleveland Clinic" in Mayo, Florida.

**Are `phases`, `maximumAge` and `collaborators` always present?**
No. Measured on a live 50-study sample: `phases` populated on ~70%, `maximumAge` on ~48%, `collaborators` on ~24%. Don't treat a missing value as a scraping error — most studies genuinely don't set these fields. `phases` is also a **list**, and the filter matches if your value is anywhere in it: filtering `["PHASE2"]` legitimately returns rows reading `["PHASE1","PHASE2"]` (2 of 10 on a live lung-cancer run), because ClinicalTrials.gov tags a combined Phase 1/2 trial with both.

**Does this return contact names, phone numbers or emails?**
No, by design — see above. If you need to contact a trial's coordinator, use the `studyUrl` to view the listing directly on ClinicalTrials.gov.

**Is this legal?**
Yes. ClinicalTrials.gov is run by the US National Library of Medicine and publishes this API for public reuse. All returned data (excluding the contact fields we deliberately drop) is public-interest study/sponsor/site metadata, not personal data about trial participants.

**How do I get only new studies on a schedule, not the whole match set every time?**
Set `watchLabel` to any name, e.g. `"my-oncology-watch"`. The first run under that label is a free baseline: it records every study currently matching your other filters and returns **zero rows, charged nothing**. Every later run with the same label AND the same other filters returns only studies not already recorded — new since the last run — and only those are charged. Change any filter (a condition, a status, a date window) and that combination gets its own fresh baseline, since it's now a different saved search. The baseline lives in your own Apify account, not ours, so it survives between scheduled runs. Ignored (with a warning) if `nctIds` is set — a direct-id lookup always returns exactly the ids you asked for, so there's no "new since last run" concept for it.

**Baseline size cap.** A baseline holds up to **60,000** nctIds in one saved record. If a label's baseline grows past that, the oldest-first-seen ids are dropped — and a dropped id is no longer recognised, so that study comes back as "new" on a later run **and is charged again**. The run that drops them says so explicitly: a warning in the log, a note on the run's status message, and `baselineTruncated` / `baselineTruncatedTotal` (this run / the whole life of the label) in `RUN_SUMMARY`, on the `webhookUrl` payload and in the saved record. If you see it, narrow the watch query (conditions, interventions, sponsors, locations, `overallStatus`, `phases`, the date windows) or split it across several labels so each baseline stays under the cap. A baseline run also stops recording at 20,000 studies, and already warns separately when it hits that.

**Does `rowsPerStudy: "site"` change what `watchLabel` tracks?**
No — "new" is always decided per **study** (`nctId`), never per site row. A trial that was already delivered stays excluded even if `rowsPerStudy` or another display-only setting changes between runs; only filters that change which studies match start a fresh baseline.

**What does `watchChanges` add, and does it cost extra to turn on?**
No extra fee — a changed study is billed at the same per-row price as a new one (exploded per-site same as any other row if `rowsPerStudy: "site"`). Plain `watchLabel` only ever tells you about studies it has never delivered before; it stays silent forever about one it already sent you, even if that trial later stops recruiting or its enrollment target changes. Set `watchChanges: true` and each run also compares every already-delivered study's `overallStatus`, `lastUpdatePostDate`, `enrollmentCount`, `primaryCompletionDate` and `completionDate` against what they looked like last time; if any moved, the row is re-delivered tagged with `_watchChangeType` (which field(s) changed) and `_watchPrevious` (what they used to be). Verified live: seeding a baseline, editing 2 studies' recorded status/enrollment count directly, then rerunning returned exactly those 2 rows with the correct change tags and nothing else — and a plain unchanged rerun after that returned 0 rows again. Existing watch labels created before this feature shipped work immediately; the first run under `watchChanges` just starts detecting drift from that point forward rather than reporting an artificial backlog.

**Important: don't filter on the field you're watching for changes (`overallStatus` catches most people).**
Change detection can only compare a study that is still **in this run's match set** — so a filter on a field `watchChanges` tracks is self-defeating: the very change you're watching for is what removes the row from view, and you never hear about it. The clearest case: a watch scoped to `overallStatus: ["RECRUITING"]` (the exact "watch a sponsor's pipeline" use case this README advertises) can never report a study moving Recruiting → Completed/Terminated, because that move is what drops it out of the filter. The same trap applies to `lastUpdatePostedDateTo` (a fresh update pushes `lastUpdatePostDate` past your upper bound and the study vanishes — `lastUpdatePostedDateFrom` is safe, since an update only ever moves the date later) and to `primaryCompletionDateFrom`/`primaryCompletionDateTo`/`studyCompletionDateFrom`/`studyCompletionDateTo` (a revised readout date moves outside the window). None of these filters is on by default, so you have to opt into the trap, but it's easy to do without noticing.

**What to do:** for each field you want alerts on, drop or widen the filter on *that field* for this watch label and filter your own copy of the rows afterward instead. **Widening costs nothing to backfill:** a label's first run on a new filter set is a free baseline (0 studies charged), so every historical study the wider query newly matches lands in that baseline for free and is never charged; only genuinely new and genuinely changed studies are billed from then on. Each run that has a change-blind filter set says so in two log warnings and lists them in `RUN_SUMMARY.watchChangeBlindFilters` (an empty array means nothing is blinding change detection), so a scheduled caller can assert on that field before trusting a quiet "no changes this run".

**How is `webhookUrl` different from Apify's own platform webhooks?**
Apify's platform webhooks are configured separately per Task/Actor via the Console or the Webhooks API — useful if you already live in the Apify Console, but extra setup if you're calling this Actor's API directly and just want a completion ping. `webhookUrl` is a plain input field: set it on the run itself and it POSTs a JSON body (`actorRunId`, `defaultDatasetId`, `finishedAt`, `pushed`, `scanned`, `pages`, a full `summary` object identical to the `RUN_SUMMARY` record below, and — if `watchLabel` is set — `watchSeeding`/`watchNewCount`/`watchChangedCount`) once the run finishes and every row is already pushed and charged. It's best-effort — a slow or failing webhook only logs a warning, it never fails the run, changes the result set, or affects billing.

**How do I tell a complete result set from a truncated one?**

Read the `RUN_SUMMARY` key-value record — no webhook needed:

```
GET https://api.apify.com/v2/actor-runs/<runId>/key-value-store/records/RUN_SUMMARY
```

```json
{
  "mode": "search",
  "declaredMatches": 123498,
  "scanned": 5,
  "delivered": 5,
  "pages": 1,
  "complete": false,
  "incompleteReason": "max-results",
  "incompleteDetail": "maxResults=5",
  "maxResults": 5,
  "watchChangeBlindFilters": null
}
```

`declaredMatches` is **ClinicalTrials.gov's own `totalCount`** for your filters — the number the registry says matches — so `delivered` vs `declaredMatches` is a comparison you can make in code rather than by eye. It is `null` when no total was ever obtained, and is **never `0`** in that case: a request that failed cannot support the claim "the registry has no such trial". `complete` is deliberately separate from the run's status, because a run can SUCCEED and be truncated at the same time — that pair is exactly what this record exists for. When `complete` is `false` the run's status message says so too.

| `incompleteReason` | What happened |
| --- | --- |
| `max-results` | Your `maxResults` stopped the run before the match set ran out. |
| `charge-limit` | The run hit the charging limit set on it. |
| `seed-cap` | A `watchLabel` baseline walk hit the 20,000-study seed cap. |
| `search-request-failed` | ClinicalTrials.gov stopped answering mid-walk (after 4 retries). **The rows you got are real, but they are not all of them.** |
| `lookup-request-failed` | One or more `nctIds` could never be checked. |
| `empty-page-with-token` | A page came back empty while pagination said there was more. |

`watchChangeBlindFilters` (`null` unless `watchChanges` is on) lists any filter in this run that narrows on a field `watchChanges` tracks and therefore hides those changes — an empty array means nothing is blinding change detection this run; see "don't filter on the field you're watching" above.

**In `nctIds` mode, what's the difference between `notFoundIds`, `malformedIds` and `failedIds`?**
They are three different facts and folding them together produces a false one. `notFoundIds` means we asked, the registry answered, and it does not hold that study — a fact you can act on. `malformedIds` means ClinicalTrials.gov rejected the id's format outright. `failedIds` means we never got an answer for it (timeout or repeated 5xx): those studies are **not** known to be missing, and re-running for just those ids is usually all that's needed. `notReachedIds` lists ids the run never got to because `maxResults` or a charge limit stopped it first — their absence from the other three lists would otherwise read as "we checked and there was nothing there".

## Related guides
- [Eight government JSON APIs that need no key — and the specific way each one lies to you](https://fetchsmith.com/blog/free-government-data-json-apis-no-key) — how this API's silent-failure shape compares across all eight free government JSON APIs we scrape.
- [The ClinicalTrials.gov API silently caps pageSize at 1000 — and its phase filter doesn't exist where you'd look for it](https://fetchsmith.com/blog/clinicaltrials-gov-json-api)
- [A 4-day window on ClinicalTrials.gov returns more trials than a 21-day one — because 42% of its dates have no day](https://fetchsmith.com/blog/clinicaltrials-month-precision-dates) — month-only completion dates collapse onto the 1st inside a `RANGE[]` filter, so a window starting after the 1st silently drops them.
- [Eight ways an "only new since last run" watch mode silently stops working](https://fetchsmith.com/blog/incremental-api-watch-mode-four-traps) — the general failure modes `watchLabel` is built to avoid.
- [We nearly charged our own buyers twice for rows they'd already paid for](https://fetchsmith.com/blog/watch-baseline-eviction-rebilling) — a capped watch-mode baseline can silently evict old-but-current ids on a high-volume run, re-delivering (and re-billing) rows already paid for. Reproduced on this Actor, closed with truncation tracking.
- [All FetchSmith tools](https://fetchsmith.com/tools)
- [Source code](https://github.com/Fetchsmith/fetchsmith/tree/main/actors/clinicaltrials-scraper)
