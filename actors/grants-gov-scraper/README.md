# Grants.gov Scraper – Status, Eligibility & Award Details

Search US federal grant opportunities from Grants.gov's official public API — no API key, no login, no proxy. Filter by keyword, agency, status, eligibility, funding category and instrument, and optionally enrich each result with award ceiling/floor, eligibility text, funding instrument/category and the full synopsis.

## What it does
- Calls Grants.gov's own `search2`/`fetchOpportunity` endpoints (the same API that powers grants.gov/search-grants), not HTML scraping.
- Search results alone carry only 10 thin fields (id, number, title, agency, dates, status). Turn on `enrich` (default) to join each row with a second call for the money fields a grant seeker actually decides on: `awardCeiling`, `awardFloor`, `applicantEligibilityDesc`, `applicantTypes`, `fundingInstruments`, `fundingActivityCategories`, and the full synopsis text.
- **Agency codes are resolved and expanded**, not passed through blind: Grants.gov's parent agency codes (e.g. `"USDA"`, `"DOD"`) do **not** automatically include their sub-agencies in a search — unlike some other government APIs. This Actor expands a parent code you supply into all of its real sub-agency codes (e.g. `"USDA"` → `USDA-NIFA`, `USDA-FS`, `USDA-APHIS`, …) so filtering by department actually works. An unrecognised code is dropped with a named warning instead of silently returning zero rows.
- **Opportunity-number lookup ignores your other filters.** Grants.gov ANDs `oppNum` with every other filter, including its own default status filter — looking up a *closed* or *archived* opportunity by its exact number normally returns nothing. Set `oppNum` and this Actor searches all statuses and ignores keyword/agency/eligibility filters, so an exact-number lookup always finds the opportunity if it exists.
- Pay per result: charged only for rows actually returned.

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
| `maxResults` | integer | Stop after this many opportunities (default 100) |

## Output (thin fields, always present)
`id`, `opportunityNumber`, `title`, `agencyCode`, `agency`, `openDate`, `closeDate`, `oppStatus`, `docType`, `cfdaList`, `url`

## Output (enriched fields, when `enrich: true`)
`agencyName`, `agencyCode`, `topAgencyName`, `topAgencyCode`, `opportunityCategory`, `postingDate`, `responseDate`, `archiveDate`, `costSharing`, `awardCeiling`, `awardFloor`, `applicantEligibilityDesc`, `applicantTypes`, `fundingInstruments`, `fundingActivityCategories`, `synopsisText`, `cfdas`, `fundingDescLinkUrl`, `synopsisDocumentURLs`, `assistURL`, `lastUpdatedDate`, `modComments`

**Privacy note:** Grants.gov's detail API also carries an `agencyContactName`/`agencyContactEmail`/`agencyContactPhone` block and a `synopsis.agencyName`/`agencyPhone`/`agencyAddressDesc` block that are agency-entered free text — sometimes a department name, sometimes a named individual program officer with a direct phone and email. Because the two cases can't be told apart per row, none of those fields are ever emitted. Organisational contact info (`agencyName`/`agencyCode` from the structured agency lookup) is included instead.

## Pricing
`result` — $0.0015 per returned item, no start fee. Meaningfully cheaper than the largest pure-Grants.gov listing on Apify ($0.009/result) and the only in-niche listing to charge no Actor-start fee at all.

## Notes
Only public data from Grants.gov's official API is collected. Issues or feature requests: support@fetchsmith.com. Also available as a hosted API at https://fetchsmith.com

## Related guides
- https://fetchsmith.com/blog/grants-gov-federal-grant-opportunities-json-api
- https://fetchsmith.com/blog/nih-reporter-grants-json-api

## Source code
https://github.com/Fetchsmith/fetchsmith/tree/main/actors/grants-gov-scraper
