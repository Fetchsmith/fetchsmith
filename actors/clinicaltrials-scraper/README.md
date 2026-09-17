# ClinicalTrials.gov Scraper – Condition, Phase & Site Mode

Pulls studies from **ClinicalTrials.gov**, the US NIH/NLM registry of clinical trials, using its own official API v2 — no API key, no login, no proxy. 602,520+ studies covered.

## What you get

25 flat fields per study, including the ones most ClinicalTrials.gov Actors skip:

| Field | Why it matters |
| --- | --- |
| `rowsPerStudy: "site"` mode | One row per **trial site** instead of one per study — facility name, city, state, country and lat/lon, so a site-selection or patient-recruitment buyer doesn't have to explode the array themselves. A study averages 5 sites (max seen: 110), so this mode returns roughly 5x more billable rows for the same query. |
| `phases`, `studyType`, `overallStatus` | Filterable and returned flat, not nested. |
| `enrollmentCount`, `sex`, `minimumAge`, `maximumAge`, `healthyVolunteers` | The eligibility snapshot without parsing free-text criteria. |
| `leadSponsorClass` | The lead sponsor's organization type (`NIH`, `INDUSTRY`, `FED`, etc.) — filterable via `funderTypes`. |
| `hasResults` | Whether the trial has posted a results section — filterable via `resultsAvailability` (with **or** without). |
| `interventions` | Type + name for every drug/device/procedure arm. |
| `studyUrl` | Direct link to the public study page. |

**We do not ship contact people, phone numbers or emails — ever.** ClinicalTrials.gov's own API returns named individuals and personal email addresses in `centralContacts`/location `contacts` (we found a real `@gmail.com` in a live sample). Several competitor Actors resell that as a "contact finder." We deliberately drop it; `locations`/`site` carries facility, city, state, country and geo-coordinates only.

Name a `watchLabel` and every later run on the same saved search returns **only studies new since the last run**, so a scheduled competitive-intelligence pull never re-delivers or re-charges for the same trial twice; add `watchChanges` and it also catches a study's **status changing** (e.g. Recruiting → Completed/Terminated), a **protocol amendment updating its enrollment count**, or its **completion date slipping**.

## Who uses this

- **Pharma / CRO business development** tracking competitor trials by condition or sponsor.
- **Site-selection teams** finding which facilities run trials for a given condition (`rowsPerStudy: "site"`).
- **Investor / market research** watching a sponsor's pipeline by phase and status; add `watchChanges` to get alerted when a trial they already logged is upgraded, terminated, or has its readout date slip.
- **Patient-advocacy and recruitment groups** finding actively recruiting trials near a location.

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
| `phases` | `EARLY_PHASE1`..`PHASE4`, `NA`. Only meaningful for interventional studies — about 1 in 5 studies overall have no phase at all. |
| `resultsAvailability` | `with` = only studies that posted a results section; `without` = only studies that never reported (the FDAAA-compliance question). Blank = both. Supersedes the older boolean `hasResultsOnly`, which still works. |
| `ageGroups` | Standard age groups the study enrols: `CHILD` (0–17), `ADULT` (18–64), `OLDER_ADULT` (65+). Multiple = OR. Coarser and more reliable than `ageRangeFromYears`/`ageRangeToYears`, which only match studies that state a numeric bound. |
| `documentTypes` | Only studies that uploaded one of these documents: `prot` (study protocol), `sap` (statistical analysis plan), `icf` (informed consent form). Multiple = OR. About 9% of studies have any. |
| `fdaRegulationViolation` | Only studies carrying an FDA regulation (FDAAA 801) violation notice — 8 registry-wide as of 2026-09-13. |
| `sex` | `FEMALE` or `MALE` — restrict to studies whose eligibility criteria specify that sex. Leave blank for all. |
| `acceptsHealthyVolunteers` | Only studies that accept healthy volunteers, not just patients with the condition. |
| `lastUpdatePostedDateFrom` / `lastUpdatePostedDateTo` | Absolute `YYYY-MM-DD` window on the record's last-updated date — a repeatable "what changed since I last pulled" query, either bound optional. Setting `From` after `To` fails fast with an error instead of silently returning 0 rows. |
| `ageRangeFromYears` / `ageRangeToYears` | Only studies whose stated minimum/maximum eligibility age falls in this range, either bound optional. E.g. `ageRangeToYears: 65` excludes studies with no senior-age cap. Setting `From` above `To` in the same unit fails fast with an error instead of silently returning 0 rows. |
| `ageRangeFromUnit` / `ageRangeToUnit` | Unit for the two bounds above: `Years` (default), `Months`, `Weeks`, `Days`. Whole years are too coarse for neonatal and infant trials — `ageRangeToYears: 18` + `ageRangeToUnit: "Months"` finds the studies that stop enrolling before the second birthday (108 alongside a cancer query, vs 2,229 for the 18-**years** reading of the same number). Each bound carries its own unit. |
| `studyStartDateFrom` / `studyStartDateTo` | Absolute `YYYY-MM-DD` window on the study's **start date**. Either bound optional. |
| `primaryCompletionDateFrom` / `primaryCompletionDateTo` | Window on the **primary completion** date — the readout date a competitive-intelligence pull is usually actually about. |
| `studyCompletionDateFrom` / `studyCompletionDateTo` | Window on the **overall completion** date. |
| `firstPostedDateFrom` / `firstPostedDateTo` | Window on the date the study was **first posted** to ClinicalTrials.gov — the "newly registered trials" query. |
| `resultsFirstPostedDateFrom` / `resultsFirstPostedDateTo` | Window on the date **results** were first posted. Pairs with `resultsAvailability: "with"`. |
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

## Sample output (`rowsPerStudy: "study"`)

```json
{
  "nctId": "NCT04137653",
  "briefTitle": "Treatment of Triple-negative Breast Cancer With Albumin-bound Paclitaxel as Neoadjuvant Therapy",
  "overallStatus": "RECRUITING",
  "studyType": "INTERVENTIONAL",
  "phases": ["PHASE3"],
  "enrollmentCount": 1498,
  "leadSponsor": "Shengjing Hospital",
  "conditions": ["Breast Cancer"],
  "interventions": [{"type": "DRUG", "name": "nab-Paclitaxel+carboplatin"}],
  "locationCount": 1,
  "studyUrl": "https://clinicaltrials.gov/study/NCT04137653"
}
```

**Watch-mode change fields, only on a `watchChanges` re-delivery:** `_watchChangeType` (array, one or more of `overallStatus`/`lastUpdatePostDate`/`enrollmentCount`/`primaryCompletionDate`/`completionDate`), `_watchPrevious` (object with the previous value(s) for each changed field).

## The pageSize trap

Ask the API for `pageSize=1001` and it doesn't 400 — it silently returns **200 with only 1000 rows**, no warning. This Actor always clamps to 1000 and pages with the API's own `nextPageToken`, which has no offset wall (5,000+ unique rows walked in one run during testing, no rate limiting).

## Pricing

**$0.0015 per result, no Actor-start fee.** The 41-user Store leader in this niche charges **$0.16 to start plus $0.012/result** — about 8x more per row, with a start fee we don't charge at all. 1,000 studies costs $1.50 here vs. $12.16 there.

## FAQ

**I already have a list of NCT IDs — can I just fetch those?**
Yes, set `nctIds` (e.g. `"NCT04368728, NCT03854955"`) instead of the search filters. ClinicalTrials.gov's own API 400s the *entire* request if even one ID in a batch is malformed or doesn't exist — we've verified this live and handle it for you: bad IDs are dropped individually with a named warning, and the rest of your batch still comes back.

**Why did I get zero rows?**
Filters are ANDed — combining a narrow condition, sponsor and location at once often genuinely matches nothing. Drop one filter and retry. Also, `phases` only applies to interventional studies with a phase assigned; pairing it with `studyTypes: ["OBSERVATIONAL"]` always returns nothing.

**There are six date filters — which one do I want?**
`firstPosted*` = when the trial was registered (new-trial alerts). `studyStart*` = when dosing/enrolment begins. `primaryCompletion*` = the primary-endpoint readout date, which is the one most competitive-intelligence pulls actually mean. `studyCompletion*` = last visit of the last patient. `resultsFirstPosted*` = when results were published. `lastUpdatePosted*` = when the record changed at all, which is the right one for an incremental "what's new since my last pull" job. Every pair is independent, ANDed with the rest, and either bound can be left blank for an open range.

**What's the difference between `facilityName` and `locations`?**
`locations` is the city/state/country text ("Boston, Massachusetts"); `facilityName` is the site name ("Mayo Clinic"). Use `facilityName` for site-selection and KOL work where you care which institution is running the trial, not where it sits. Multi-word values are sent as a quoted phrase, so `Mayo Clinic` does not also match a study at "Cleveland Clinic" in Mayo, Florida.

**Are `phases`, `maximumAge` and `collaborators` always present?**
No. Measured on a live 50-study sample: `phases` populated on ~70%, `maximumAge` on ~48%, `collaborators` on ~24%. Don't treat a missing value as a scraping error — most studies genuinely don't set these fields.

**Does this return contact names, phone numbers or emails?**
No, by design — see above. If you need to contact a trial's coordinator, use the `studyUrl` to view the listing directly on ClinicalTrials.gov.

**Is this legal?**
Yes. ClinicalTrials.gov is run by the US National Library of Medicine and publishes this API for public reuse. All returned data (excluding the contact fields we deliberately drop) is public-interest study/sponsor/site metadata, not personal data about trial participants.

**How do I get only new studies on a schedule, not the whole match set every time?**
Set `watchLabel` to any name, e.g. `"my-oncology-watch"`. The first run under that label is a free baseline: it records every study currently matching your other filters and returns **zero rows, charged nothing**. Every later run with the same label AND the same other filters returns only studies not already recorded — new since the last run — and only those are charged. Change any filter (a condition, a status, a date window) and that combination gets its own fresh baseline, since it's now a different saved search. The baseline lives in your own Apify account, not ours, so it survives between scheduled runs. Ignored (with a warning) if `nctIds` is set — a direct-id lookup always returns exactly the ids you asked for, so there's no "new since last run" concept for it.

**Does `rowsPerStudy: "site"` change what `watchLabel` tracks?**
No — "new" is always decided per **study** (`nctId`), never per site row. A trial that was already delivered stays excluded even if `rowsPerStudy` or another display-only setting changes between runs; only filters that change which studies match start a fresh baseline.

**What does `watchChanges` add, and does it cost extra to turn on?**
No extra fee — a changed study is billed at the same per-row price as a new one (exploded per-site same as any other row if `rowsPerStudy: "site"`). Plain `watchLabel` only ever tells you about studies it has never delivered before; it stays silent forever about one it already sent you, even if that trial later stops recruiting or its enrollment target changes. Set `watchChanges: true` and each run also compares every already-delivered study's `overallStatus`, `lastUpdatePostDate`, `enrollmentCount`, `primaryCompletionDate` and `completionDate` against what they looked like last time; if any moved, the row is re-delivered tagged with `_watchChangeType` (which field(s) changed) and `_watchPrevious` (what they used to be). Verified live: seeding a baseline, editing 2 studies' recorded status/enrollment count directly, then rerunning returned exactly those 2 rows with the correct change tags and nothing else — and a plain unchanged rerun after that returned 0 rows again. Existing watch labels created before this feature shipped work immediately; the first run under `watchChanges` just starts detecting drift from that point forward rather than reporting an artificial backlog.

## Related guides

- [The ClinicalTrials.gov API silently caps pageSize at 1000 — and its phase filter doesn't exist where you'd look for it](https://fetchsmith.com/blog/clinicaltrials-gov-json-api)
- [Eight ways an "only new since last run" watch mode silently stops working](https://fetchsmith.com/blog/incremental-api-watch-mode-four-traps) — the general failure modes `watchLabel` is built to avoid.
- [All FetchSmith tools](https://fetchsmith.com/tools)
- [Source code](https://github.com/Fetchsmith/fetchsmith/tree/main/actors/clinicaltrials-scraper)
