# Grants.gov Scraper – Status, Eligibility & Award Details

Search US federal grant opportunities from Grants.gov's official public API — no API key, no login, no proxy. Filter by keyword, agency, status, eligibility, funding category and instrument, and optionally enrich each result with award ceiling/floor, eligibility text, funding instrument/category and the full synopsis.

## What it does
- Calls Grants.gov's own `search2`/`fetchOpportunity` endpoints (the same API that powers grants.gov/search-grants), not HTML scraping.
- Search results alone carry only 10 thin fields (id, number, title, agency, dates, status). Turn on `enrich` (default) to join each row with a second call for the money fields a grant seeker actually decides on: `awardCeiling`, `awardFloor`, `applicantEligibilityDesc`, `applicantTypes`, `fundingInstruments`, `fundingActivityCategories`, and the full synopsis text.
- **Agency codes are resolved and expanded**, not passed through blind: Grants.gov's parent agency codes (e.g. `"USDA"`, `"DOD"`) do **not** automatically include their sub-agencies in a search — unlike some other government APIs. This Actor expands a parent code you supply into all of its real sub-agency codes (e.g. `"USDA"` → `USDA-NIFA`, `USDA-FS`, `USDA-APHIS`, …) so filtering by department actually works. An unrecognised code is dropped with a named warning instead of silently returning zero rows.
- **Opportunity-number lookup ignores your other filters.** Grants.gov ANDs `oppNum` with every other filter, including its own default status filter — looking up a *closed* or *archived* opportunity by its exact number normally returns nothing. Set `oppNum` and this Actor searches all statuses and ignores keyword/agency/eligibility filters, so an exact-number lookup always finds the opportunity if it exists.
- **`postedWithinDays` for cheap incremental pulls** — Grants.gov's own "Posted Date" filter accepts any positive number of days, not just its site's 3/7/14/21-day preset buttons (verified live). Use it instead of re-scanning the whole index on a daily/weekly cron.
- **`postedFrom`/`postedTo` for a fixed calendar window** — Grants.gov's API has no absolute-date filter server-side, so this Actor applies the range client-side against each row's own open date (already present on every result, no extra detail lookups needed). Use this for historical reporting ("everything posted in Q1") where `postedWithinDays`' relative-to-today window doesn't fit. If both are set, `postedFrom`/`postedTo` wins and `postedWithinDays` is ignored (with a warning).
- **`minAwardAmount`/`maxAwardAmount` filter on award ceiling** — forces `enrich` on since the amount only exists in the per-opportunity detail record. Grants.gov returns award amounts as strings, and roughly a third to half of posted opportunities have no ceiling set at all (the API spells this as the literal string `"none"`, not null or absent) — this Actor normalizes both into real numbers or `null`, and the amount filter correctly drops the `"none"` rows rather than treating them as zero.
- **`watchLabel` — only what's new since your last run.** Name a saved search and every run after the first returns just the opportunities not already delivered under that label and filter combination, instead of the whole match set every time. The first run for a label is a free baseline (0 results, 0 charged); it records what already matches in a key-value store on your own Apify account, keyed by the label plus a fingerprint of your other filters, so editing a filter starts a fresh baseline instead of dumping every previously-excluded opportunity as "new". Built for a daily/weekly scheduled run.
- Pay per result: charged only for rows actually returned.

## Use cases
- **Grant-seeking pipelines** — pull every open opportunity a nonprofit, university or small business is eligible for (`eligibilities` + `fundingCategories`), already joined with award ceiling/floor so you can triage by money without a second lookup.
- **Daily/weekly funding alerts** — run `postedWithinDays: 1` on a cron and only pay for the handful of opportunities posted since yesterday, instead of re-scanning the whole index.
- **Award-size screening** — `minAwardAmount: 500000` to surface only large awards, or `maxAwardAmount` to find the small ones a single PI can realistically manage.
- **Grants-landscape research** — filter by `agencies` (parent codes expand to every sub-agency) and `postedFrom`/`postedTo` to reconstruct a fixed historical window, e.g. everything a department posted last quarter.
- **Enriching an existing list** — set `oppNum` to look up one opportunity by its exact number and get the full record back, even if it is closed or archived.

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
| `minAwardAmount` | integer | Minimum award ceiling (USD); forces `enrich` on, excludes opportunities with no ceiling set |
| `maxAwardAmount` | integer | Maximum award ceiling (USD); same exclusions as `minAwardAmount` |
| `maxResults` | integer | Stop after this many opportunities (default 100) |
| `watchLabel` | string | Optional. Name a saved search to get only opportunities new since your last run under that label — see FAQ |

## Output (thin fields, always present)
`id`, `opportunityNumber`, `title`, `agencyCode`, `agency`, `openDate`, `closeDate`, `oppStatus`, `docType`, `cfdaList`, `url`

## Output (enriched fields, when `enrich: true`)
`agencyName`, `agencyCode`, `topAgencyName`, `topAgencyCode`, `opportunityCategory`, `postingDate`, `responseDate`, `archiveDate`, `costSharing`, `awardCeiling`, `awardFloor`, `applicantEligibilityDesc`, `applicantTypes`, `fundingInstruments`, `fundingActivityCategories`, `synopsisText`, `cfdas`, `fundingDescLinkUrl`, `synopsisDocumentURLs`, `assistURL`, `lastUpdatedDate`, `modComments`

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

**Privacy note:** Grants.gov's detail API also carries an `agencyContactName`/`agencyContactEmail`/`agencyContactPhone` block and a `synopsis.agencyName`/`agencyPhone`/`agencyAddressDesc` block that are agency-entered free text — sometimes a department name, sometimes a named individual program officer with a direct phone and email. Because the two cases can't be told apart per row, none of those fields are ever emitted. Organisational contact info (`agencyName`/`agencyCode` from the structured agency lookup) is included instead.

## Pricing
`result` — $0.0015 per returned item, no start fee. Meaningfully cheaper than the largest pure-Grants.gov listing on Apify ($0.009/result) and the only in-niche listing to charge no Actor-start fee at all.

## FAQ

**Do I need a Grants.gov account or API key?**
No. This uses Grants.gov's own public `search2`/`fetchOpportunity` endpoints — no key, no login, no proxy.

**Does `maxResults` count rows before or after the filters?**
After. It caps the number of opportunities actually returned to you, which is also the number you are charged for. Verified live: `keyword: "cancer research"`, `oppStatuses: ["posted"]`, `minAwardAmount: 500000`, `maxResults: 3` returned exactly 3 rows, all with an award ceiling of $500,000 or more — not 3 scanned rows of which some survived.

**Why does an opportunity have `awardCeiling: null`?**
Because the agency never set one. Grants.gov spells this as the literal string `"none"` in its detail record; this Actor normalizes it to `null` rather than passing through an inconsistently-typed string or pretending it is `0`. Measured live at roughly a third of posted opportunities, so it is a common case. Note that `minAwardAmount`/`maxAwardAmount` therefore *exclude* these rows — there is no ceiling to compare against.

**I filtered by `"USDA"` — do I get the sub-agencies too?**
Yes. Grants.gov's own API does not do this: a parent code matches nothing but itself, so a plain `"USDA"` search on the raw API returns almost nothing. This Actor expands the parent into its real sub-agency codes first. Verified live: `agencies: ["USDA"]` returns rows with `agencyCode` values like `USDA-NIFA` and `USDA-APHIS`. An unrecognised code is dropped with a named warning in the log instead of silently returning zero rows.

**Can I look up a closed or archived opportunity by its number?**
Yes, and you do not need to change `oppStatuses` to do it. When `oppNum` is set, this Actor searches all four statuses and ignores every other filter. Verified live: `oppNum: "USDA-NIFA-BFR-002918"` with the default statuses (forecasted + posted) and a deliberately unrelated `keyword: "quantum physics"` still returned that one archived opportunity.

**Why did my run return zero results?**
Every filter is ANDed, and Grants.gov's API never reports a bad value — a typo'd code returns "success" with zero hits. Most common causes, in order: `oppStatuses` defaults to forecasted + posted, so history needs `closed`/`archived` added; a narrow keyword plus agency plus eligibility often genuinely has no matches; a small `postedWithinDays`/`postedFrom` window is a hard filter; and the award-amount filters drop every row with no ceiling set. The run log names which one applied.

**Should I turn `enrich` off?**
Only for fast, cheap sweeps where the thin fields (id, number, title, agency, dates, status, CFDA list, plus a URL this Actor builds for you) are enough. Everything a funding decision actually turns on — award amounts, eligibility text, funding instrument/category, the full synopsis — exists only in the detail record, which is why `enrich` defaults to on. It is forced on when you set an award-amount filter.

**How does `watchLabel` know what's already new, and where is that baseline stored?**
The first run for a label walks the whole match set (every page, not just `maxResults` of it), records every opportunity's `id`, and returns nothing — you are charged $0. Every later run with the same label and the same other filters returns only opportunities whose `id` isn't in that recorded set, then adds them to it. The baseline lives in a key-value store named `fetchsmith-grants-watch` in *your own* Apify account (Storage tab in the console), not ours — you can inspect or delete it any time. Deleting the record for a label resets it to a fresh baseline on the next run. Verified live on build 0.1.9: a seed run over `keyword: "water"` recorded 18,458 opportunity ids and returned 0 rows; an identical rerun returned 0 new; removing 3 ids from the baseline directly and rerunning returned exactly those 3.

**If I change a filter, does `watchLabel` dump a pile of "new" results I've actually seen before?**
No. The baseline key includes a fingerprint of every other filter you set, so changing `keyword`, `agencies`, `postedFrom`/`postedTo`, `minAwardAmount`, etc. starts an entirely fresh baseline (another free, zero-result seed run) under that label instead of comparing against the old filter's baseline. `oppNum` lookups ignore `watchLabel` entirely — an exact single-opportunity lookup has no "new since last time" to track.

## Notes
Only public data from Grants.gov's official API is collected. Issues or feature requests: support@fetchsmith.com. Also available as a hosted API at https://fetchsmith.com

## Related guides
- https://fetchsmith.com/blog/grants-gov-federal-grant-opportunities-json-api
- https://fetchsmith.com/blog/nih-reporter-grants-json-api
- [Four ways an "only new since last run" watch mode silently stops working](https://fetchsmith.com/blog/incremental-api-watch-mode-four-traps) — how `watchLabel` is built, and why a cheap id-only baseline still has to apply the award-amount filter.

## Source code
https://github.com/Fetchsmith/fetchsmith/tree/main/actors/grants-gov-scraper

More tools: [fetchsmith.com/tools](https://fetchsmith.com/tools) — 19 HTTP-only Actors for public data sources, no browser required.
