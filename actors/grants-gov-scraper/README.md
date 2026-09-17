# Grants.gov Scraper – Status, Eligibility & Award Details

Search US federal grant opportunities from Grants.gov's official public API — no API key, no login, no proxy. Filter by keyword, agency, status, eligibility, funding category and instrument, and optionally enrich each result with award ceiling/floor, eligibility text, funding instrument/category and the full synopsis.

## What it does
- Calls Grants.gov's own `search2`/`fetchOpportunity` endpoints (the same API that powers grants.gov/search-grants), not HTML scraping.
- Search results alone carry only 10 thin fields (id, number, title, agency, dates, status). Turn on `enrich` (default) to join each row with a second call for the money fields a grant seeker actually decides on: `awardCeiling`, `awardFloor`, `applicantEligibilityDesc`, `applicantTypes`, `fundingInstruments`, `fundingActivityCategories`, and the full synopsis text.
- **Forecasted opportunities (`docType: "forecast"`) are enriched too**, not just posted ones — roughly half of the default `oppStatuses` result set. Grants.gov gives a forecast its own estimated award ceiling/floor, applicant types and funding instruments/categories under the same field names as a posted synopsis, plus forecast-only fields: `numberOfAwards`, `estimatedFunding`, `estSynopsisPostingDate`, `estApplicationResponseDate`, `estAwardDate`, `estProjectStartDate`, `fiscalYear`.
- **Agency codes are resolved and expanded**, not passed through blind: Grants.gov's parent agency codes (e.g. `"USDA"`, `"DOD"`) do **not** automatically include their sub-agencies in a search — unlike some other government APIs. This Actor expands a parent code you supply into all of its real sub-agency codes (e.g. `"USDA"` → `USDA-NIFA`, `USDA-FS`, `USDA-APHIS`, …) so filtering by department actually works. An unrecognised code is dropped with a named warning instead of silently returning zero rows.
- **Opportunity-number lookup ignores your other filters.** Grants.gov ANDs `oppNum` with every other filter, including its own default status filter — looking up a *closed* or *archived* opportunity by its exact number normally returns nothing. Set `oppNum` and this Actor searches all statuses and ignores keyword/agency/eligibility filters, so an exact-number lookup always finds the opportunity if it exists.
- **`postedWithinDays` for cheap incremental pulls** — Grants.gov's own "Posted Date" filter accepts any positive number of days, not just its site's 3/7/14/21-day preset buttons (verified live). Use it instead of re-scanning the whole index on a daily/weekly cron.
- **`postedFrom`/`postedTo` for a fixed calendar window** — Grants.gov's API has no absolute-date filter server-side, so this Actor applies the range client-side against each row's own open date (already present on every result, no extra detail lookups needed). Use this for historical reporting ("everything posted in Q1") where `postedWithinDays`' relative-to-today window doesn't fit. If both are set, `postedFrom`/`postedTo` wins and `postedWithinDays` is ignored (with a warning).
- **`closeDateFrom`/`closeDateTo` filter on the application deadline** — the question a grant seeker actually asks ("what closes in the next 30 days?") is about the deadline, not the posting date. Grants.gov's API can *sort* by close date but cannot *filter* on it, so this is applied client-side against each row's own close date (already on every thin result row, no extra lookups, no extra cost). Be aware what has no deadline: a forecast never has one (Grants.gov returns an empty close date on 100% of `docType: "forecast"` rows), and neither do rolling/continuous announcements and RFIs (~18% of posted rows on an unfiltered sample). Those are dropped by this filter and reported under their own count in the run summary, and the Actor warns up front if you leave `forecasted` in `oppStatuses` while filtering on a deadline.
- **`minAwardAmount`/`maxAwardAmount` filter on award ceiling** — forces `enrich` on since the amount only exists in the per-opportunity detail record. Grants.gov returns award amounts as strings, and roughly a third to half of posted opportunities have no ceiling set at all (the API spells this as the literal string `"none"`, not null or absent) — this Actor normalizes both into real numbers or `null`, and the amount filter correctly drops the `"none"` rows rather than treating them as zero.
- **`watchLabel` — only what's new since your last run.** Name a saved search and every run after the first returns just the opportunities not already delivered under that label and filter combination, instead of the whole match set every time. The first run for a label is a free baseline (0 results, 0 charged); it records what already matches in a key-value store on your own Apify account, keyed by the label plus a fingerprint of your other filters, so editing a filter starts a fresh baseline instead of dumping every previously-excluded opportunity as "new". Built for a daily/weekly scheduled run.
- **`watchChanges` — also catch a deadline extension, a status change, or a forecast turning real.** Add this to `watchLabel` and an opportunity you already have gets re-delivered (at the normal per-row price, tagged `_watchChangeType`/`_watchPrevious`) if its closing date, `docType` (forecast → posted) or `oppStatus` (posted → closed/archived) changes since you last saw it — not just brand-new opportunities. Off by default so existing watches keep their current behaviour.
- Pay per result: charged only for rows actually returned.

## Use cases
- **Grant-seeking pipelines** — pull every open opportunity a nonprofit, university or small business is eligible for (`eligibilities` + `fundingCategories`), already joined with award ceiling/floor so you can triage by money without a second lookup.
- **Daily/weekly funding alerts** — run `postedWithinDays: 1` on a cron and only pay for the handful of opportunities posted since yesterday, instead of re-scanning the whole index.
- **Deadline triage** — `closeDateFrom`/`closeDateTo` to list only what a team can still realistically apply for ("everything closing between today and 30 days out"), instead of paging through opportunities whose deadline has already passed or is a year away.
- **Award-size screening** — `minAwardAmount: 500000` to surface only large awards, or `maxAwardAmount` to find the small ones a single PI can realistically manage.
- **Grants-landscape research** — filter by `agencies` (parent codes expand to every sub-agency) and `postedFrom`/`postedTo` to reconstruct a fixed historical window, e.g. everything a department posted last quarter.
- **Enriching an existing list** — set `oppNum` to look up one opportunity by its exact number and get the full record back, even if it is closed or archived.
- **Deadline-amendment / forecast-to-posted alerts** — `watchLabel` + `watchChanges` on a saved search flags an agency extending a deadline or a forecast finally posting, without re-fetching and diffing the whole result set yourself.

### Example input
```json
{
  "keyword": "cancer research",
  "oppStatuses": ["posted"],
  "minAwardAmount": 500000,
  "maxResults": 3
}
```

## Input
| Field | Type | Description |
|---|---|---|
| `keyword` | string | Full-text search across title and synopsis |
| `oppStatuses` | array | `forecasted`, `posted`, `closed`, `archived` (default: forecasted + posted) |
| `agencies` | array | Agency codes, e.g. `NSF`, `USDA-NIFA`, `DOD-AMC`; parent codes are expanded to sub-agencies |
| `eligibilities` | array | Restrict to applicant types (state govt, nonprofit, small business, individuals, …) |
| `fundingCategories` | array | Restrict to funding activity categories (Health, Education, Environment, …) |
| `fundingInstruments` | array | Grant / Cooperative Agreement / Procurement Contract / Other |
| `cfda` | string | Restrict to one Assistance Listing (CFDA) number |
| `oppNum` | string | Look up one opportunity by exact number — ignores all other filters |
| `sortBy` | string | `openDate\|desc`, `openDate\|asc`, `closeDate\|desc`, `closeDate\|asc` |
| `enrich` | boolean | Join each row with award/eligibility/synopsis detail (default `true`) |
| `postedWithinDays` | integer | Only opportunities posted in the last N days — cheap incremental pull |
| `postedFrom` | string | Only opportunities opened on/after this date (`YYYY-MM-DD`); overrides `postedWithinDays` |
| `postedTo` | string | Only opportunities opened on/before this date (`YYYY-MM-DD`); overrides `postedWithinDays` |
| `closeDateFrom` | string | Only opportunities whose deadline falls on/after this date (`YYYY-MM-DD`); excludes rows with no deadline |
| `closeDateTo` | string | Only opportunities whose deadline falls on/before this date (`YYYY-MM-DD`); same exclusions |
| `minAwardAmount` | integer | Minimum award ceiling (USD); forces `enrich` on, excludes opportunities with no ceiling set |
| `maxAwardAmount` | integer | Maximum award ceiling (USD); same exclusions as `minAwardAmount` |
| `maxResults` | integer | Stop after this many opportunities (default 100) |
| `watchLabel` | string | Optional. Name a saved search to get only opportunities new since your last run under that label — see FAQ |
| `watchChanges` | boolean | Optional, requires `watchLabel`. Also re-deliver an already-seen opportunity if its closing date, `docType` or `oppStatus` changed (default `false`) — see FAQ |

## Output (thin fields, always present)
`id`, `opportunityNumber`, `title`, `agencyCode`, `agency`, `openDate`, `closeDate`, `oppStatus`, `docType`, `cfdaList`, `url`

## Output (enriched fields, when `enrich: true`)
`agencyName`, `agencyCode`, `topAgencyName`, `topAgencyCode`, `opportunityCategory`, `postingDate`, `responseDate`, `archiveDate`, `costSharing`, `awardCeiling`, `awardFloor`, `applicantEligibilityDesc`, `applicantTypes`, `fundingInstruments`, `fundingActivityCategories`, `synopsisText`, `cfdas`, `fundingDescLinkUrl`, `synopsisDocumentURLs`, `assistURL`, `lastUpdatedDate`, `modComments`

## Output (watch-mode change fields, only on a `watchChanges` re-delivery)
`_watchChangeType` (array, one or more of `closeDate`/`docType`/`oppStatus`), `_watchPrevious` (object with the previous value(s) for each changed field)

On a `docType: "forecast"` row, `responseDate`/`archiveDate`/`applicantEligibilityDesc`/`fundingDescLinkUrl` are `null` (a forecast has no firm deadline or eligibility writeup yet) and seven forecast-only fields are added instead: `numberOfAwards`, `estimatedFunding`, `estSynopsisPostingDate` (Grants.gov's own estimate of when the real NOFO posts), `estApplicationResponseDate`, `estAwardDate`, `estProjectStartDate`, `fiscalYear`. These are `null` on synopsis-based (posted/closed/archived) rows.

### Sample output (one real row from the example input above)
```json
{
  "id": "357002",
  "opportunityNumber": "PAR-24-311",
  "title": "Molecular Imaging of Inflammation in Cancer (R01 Clinical Trial Not Allowed)",
  "agencyCode": "HHS-NIH11",
  "agency": "National Institutes of Health",
  "openDate": "11/06/2024",
  "closeDate": "01/07/2028",
  "oppStatus": "posted",
  "docType": "synopsis",
  "cfdaList": ["93.394", "93.395", "93.396"],
  "url": "https://www.grants.gov/search-results-detail/357002",
  "topAgencyName": "Department of Health and Human Services",
  "topAgencyCode": "HHS",
  "opportunityCategory": "Discretionary",
  "postingDate": "Nov 06, 2024 12:00:00 AM EST",
  "responseDate": "Jan 07, 2028 12:00:00 AM EST",
  "archiveDate": "Feb 12, 2028 12:00:00 AM EST",
  "costSharing": false,
  "awardCeiling": 500000,
  "awardFloor": null,
  "applicantTypes": ["State governments", "Small businesses", "Independent school districts", "..."],
  "fundingInstruments": ["Grant"],
  "fundingActivityCategories": ["Education", "Health"],
  "synopsisText": "The purpose of this Notice of Funding Opportunity (NOFO) is to invite research grant applications (R01) for the development and use of ...",
  "cfdas": [{ "number": "93.394", "title": "Cancer Detection and Diagnosis Research" }],
  "fundingDescLinkUrl": "http://grants.nih.gov/grants/guide/pa-files/PAR-24-311.html",
  "lastUpdatedDate": "Nov 06, 2024 10:10:59 AM EST"
}
```
Note `awardFloor: null` alongside a real `awardCeiling` — agencies often set only one of the two. Dates come back in Grants.gov's own two formats: `MM/DD/YYYY` on the thin search fields, and a long `MMM DD, YYYY hh:mm:ss AM/PM TZ` string on the enriched detail fields. Both are passed through as the API returns them.

### Sample output (a forecast, `oppStatuses: ["forecasted"]`)
```json
{
  "id": "355824",
  "opportunityNumber": "MP-CPI-25-001",
  "title": "Making America Healthy Again by Addressing Dementia Disparities",
  "agencyCode": "HHS-OPHS",
  "agency": "Office of the Assistant Secretary for Health",
  "openDate": "08/01/2024",
  "closeDate": null,
  "oppStatus": "forecasted",
  "docType": "forecast",
  "cfdaList": ["93.137"],
  "url": "https://www.grants.gov/search-results-detail/355824",
  "opportunityCategory": "Discretionary",
  "costSharing": false,
  "awardCeiling": 600000,
  "awardFloor": 450000,
  "applicantTypes": ["State governments", "Nonprofits having a 501(c)(3) status with the IRS, other than institutions of higher education", "..."],
  "fundingInstruments": ["Grant"],
  "fundingActivityCategories": ["Health"],
  "synopsisText": "The Office of Minority Health announces the anticipated availability of funds for Fiscal Year (FY) 2025 ...",
  "cfdas": [{ "number": "93.137", "title": "Community Programs to Improve Minority Health" }],
  "numberOfAwards": 9,
  "estimatedFunding": 5000000,
  "estSynopsisPostingDate": "Apr 14, 2025 12:00:00 AM EDT",
  "estApplicationResponseDate": "Jun 23, 2025 12:00:00 AM EDT",
  "estAwardDate": "Sep 15, 2025 12:00:00 AM EDT",
  "estProjectStartDate": "Sep 30, 2025 12:00:00 AM EDT",
  "fiscalYear": 2025
}
```
`responseDate`, `archiveDate`, `applicantEligibilityDesc` and `fundingDescLinkUrl` are omitted above because Grants.gov has no forecast equivalent — they read `null`, not missing.

**Privacy note:** Grants.gov's detail API also carries an `agencyContactName`/`agencyContactEmail`/`agencyContactPhone` block and a `synopsis.agencyName`/`agencyPhone`/`agencyAddressDesc` block that are agency-entered free text — sometimes a department name, sometimes a named individual program officer with a direct phone and email. Because the two cases can't be told apart per row, none of those fields are ever emitted. Organisational contact info (`agencyName`/`agencyCode` from the structured agency lookup) is included instead.

## Pricing
Two events, no start fee. **The price follows the data, per row** — you are never charged the enriched rate for a row that arrived thin.

| Event | Price | Charged when |
| --- | --- | --- |
| `result` (enriched) | $0.0015 per item | The row carries its full detail record: award ceiling/floor, eligibility text, funding instrument/category, synopsis |
| `opportunity-thin` | $0.0007 per item | `enrich: false`, **or** Grants.gov has no detail record for that opportunity (some archived ones don't) |

Cheaper than the largest pure-Grants.gov listing on Apify ($0.009/result) at either rate, and the only in-niche listing to charge no Actor-start fee at all. The run log prints the split (`Charged N as enriched "result" and M at the cheaper "opportunity-thin" rate`) so the invoice is checkable against the dataset.

## FAQ

**Do I need a Grants.gov account or API key?**
No. This uses Grants.gov's own public `search2`/`fetchOpportunity` endpoints — no key, no login, no proxy.

**Does `maxResults` count rows before or after the filters?**
After. It caps the number of opportunities actually returned to you, which is also the number you are charged for. Verified live: `keyword: "cancer research"`, `oppStatuses: ["posted"]`, `minAwardAmount: 500000`, `maxResults: 3` returned exactly 3 rows, all with an award ceiling of $500,000 or more — not 3 scanned rows of which some survived.

**Why does an opportunity have `awardCeiling: null`?**
Because the agency never set one. Grants.gov spells this as the literal string `"none"` in its detail record; this Actor normalizes it to `null` rather than passing through an inconsistently-typed string or pretending it is `0`. Measured live at roughly a third of posted opportunities, so it is a common case. Note that `minAwardAmount`/`maxAwardAmount` therefore *exclude* these rows — there is no ceiling to compare against. This applies equally to forecasts — a forecast can have `awardCeiling: null` too if the agency hasn't estimated one yet — but a forecast is never excluded just for *being* a forecast; its detail record is fetched and its `awardCeiling` compared the same as any posted opportunity's.

**Does the award-amount filter work on forecasted opportunities, or only posted ones?**
Both. Every `docType:"forecast"` row gets the same detail lookup as a posted one, and Grants.gov gives forecasts their own `awardCeiling`/`awardFloor` estimate under the same field names — so `minAwardAmount`/`maxAwardAmount` compare against it identically. (Fixed cycle 325: earlier builds silently treated every forecast as having no detail record at all, so `minAwardAmount`/`maxAwardAmount` dropped 100% of forecasts regardless of their real award ceiling. If you were filtering by amount before and never saw a forecast in your results, that's why — re-run now.)

**I filtered by `"USDA"` — do I get the sub-agencies too?**
Yes. Grants.gov's own API does not do this: a parent code matches nothing but itself, so a plain `"USDA"` search on the raw API returns almost nothing. This Actor expands the parent into its real sub-agency codes first. Verified live: `agencies: ["USDA"]` returns rows with `agencyCode` values like `USDA-NIFA` and `USDA-APHIS`. An unrecognised code is dropped with a named warning in the log instead of silently returning zero rows.

**Can I look up a closed or archived opportunity by its number?**
Yes, and you do not need to change `oppStatuses` to do it. When `oppNum` is set, this Actor searches all four statuses and ignores every other filter. Verified live: `oppNum: "USDA-NIFA-BFR-002918"` with the default statuses (forecasted + posted) and a deliberately unrelated `keyword: "quantum physics"` still returned that one archived opportunity.

**Why did my run return zero results?**
Every filter is ANDed, and Grants.gov's API never reports a bad value — a typo'd code returns "success" with zero hits. Most common causes, in order: `oppStatuses` defaults to forecasted + posted, so history needs `closed`/`archived` added; a narrow keyword plus agency plus eligibility often genuinely has no matches; a small `postedWithinDays`/`postedFrom` window is a hard filter; and the award-amount filters drop every row with no ceiling set. The run log names which one applied.

**Should I turn `enrich` off?**
Only for fast sweeps where the thin fields (id, number, title, agency, dates, status, CFDA list, plus a URL this Actor builds for you) are enough — those rows are billed at $0.0007 instead of $0.0015, because they cost no detail lookup to serve. Everything a funding decision actually turns on — award amounts, eligibility text, funding instrument/category, the full synopsis — exists only in the detail record, which is why `enrich` defaults to on. It is forced on when you set an award-amount filter.

**I left `enrich` on but some rows came back without award amounts — was I charged full price for them?**
No. Grants.gov has no detail record at all for a small number of opportunities (mostly archived ones with no synopsis or forecast record). When the detail lookup comes back empty, the row is still returned with its thin fields and billed as `opportunity-thin` ($0.0007), not `result` ($0.0015). The split is printed in the run log at the end of every run.

**How does `watchLabel` know what's already new, and where is that baseline stored?**
The first run for a label walks the whole match set (every page, not just `maxResults` of it), records every opportunity's `id`, and returns nothing — you are charged $0. Every later run with the same label and the same other filters returns only opportunities whose `id` isn't in that recorded set, then adds them to it. The baseline lives in a key-value store named `fetchsmith-grants-watch` in *your own* Apify account (Storage tab in the console), not ours — you can inspect or delete it any time. Deleting the record for a label resets it to a fresh baseline on the next run. Verified live on build 0.1.9: a seed run over `keyword: "water"` recorded 18,458 opportunity ids and returned 0 rows; an identical rerun returned 0 new; removing 3 ids from the baseline directly and rerunning returned exactly those 3.

**If I change a filter, does `watchLabel` dump a pile of "new" results I've actually seen before?**
No. The baseline key includes a fingerprint of every other filter you set, so changing `keyword`, `agencies`, `postedFrom`/`postedTo`, `minAwardAmount`, etc. starts an entirely fresh baseline (another free, zero-result seed run) under that label instead of comparing against the old filter's baseline. `oppNum` lookups ignore `watchLabel` entirely — an exact single-opportunity lookup has no "new since last time" to track.

**What does `watchChanges` add, and does it cost extra to turn on?**
No extra fee — a changed opportunity is billed at the same per-row price as a new one ($0.0015 enriched / $0.0007 thin), so you only pay when there is actually something to see. Plain `watchLabel` only ever tells you about opportunities it has never delivered before; it stays silent forever about one it already sent you, even if that agency later extends the deadline, closes it early, or turns a `forecast` into a real posted `synopsis`. Set `watchChanges: true` and each run also compares every already-delivered opportunity's `closeDate`/`docType`/`oppStatus` against what it looked like last time; if any of the three moved, the row is re-delivered tagged with `_watchChangeType` (which field(s) changed) and `_watchPrevious` (what they used to be). Verified live: seeding a baseline, editing 2 opportunities' recorded closing date and doc type directly, then rerunning returned exactly those 2 rows with the correct change tags and nothing else — and a plain unchanged rerun after that returned 0 rows again. Existing watch labels created before this feature shipped work immediately; the first run under `watchChanges` just starts detecting drift from that point forward rather than reporting an artificial backlog.

## Notes
Only public data from Grants.gov's official API is collected. Issues or feature requests: support@fetchsmith.com. Also available as a hosted API at https://fetchsmith.com

## Related guides
- https://fetchsmith.com/blog/grants-gov-federal-grant-opportunities-json-api
- https://fetchsmith.com/blog/nih-reporter-grants-json-api
- [Eight ways an "only new since last run" watch mode silently stops working](https://fetchsmith.com/blog/incremental-api-watch-mode-four-traps) — how `watchLabel` is built, and why a cheap id-only baseline still has to apply the award-amount filter.

## Source code
https://github.com/Fetchsmith/fetchsmith/tree/main/actors/grants-gov-scraper

More tools: [fetchsmith.com/tools](https://fetchsmith.com/tools) — 19 HTTP-only Actors for public data sources, no browser required.
