# Trademark Search Scraper — USPTO, EUIPO & 70+ Offices (TMview)

Search registered trademarks across **70+ national and regional trademark offices** — USPTO (US), EUIPO (EM), UK, DE, FR, JP, CN, WIPO (WO) and more — through the official [TMview](https://www.tmdn.org/tmview/) database. One search covers every office you select in a single run; no need to query each country's own registry separately.

## What it does
- Sends your search term to TMview's public search API and returns matching trademarks as structured JSON, one row per mark.
- Filter by office (country/region), Nice classification class, and trademark status (Registered, Filed, Expired, Ended, Withdrawn, ...).
- Pay per result: you are charged only for rows actually returned. HTTP-only (no browser), so runs are fast and cheap.

## Input
| Field | Type | Description |
|---|---|---|
| `searchTerm` | string | Word or brand to search for (contains-match). Default `"coffee"`. |
| `offices` | array | Two-letter office codes, e.g. `US` (USPTO), `EM` (EUIPO), `GB`, `DE`, `FR`, `JP`, `CN`, `WO` (WIPO). Leave empty to search all 70+ offices. |
| `niceClasses` | array | Restrict to Nice classification classes, e.g. `"25"` (clothing), `"9"` (software). Leave empty for all classes. |
| `statuses` | array | Restrict to statuses, e.g. `Registered`, `Filed`, `Expired`, `Ended`, `Withdrawn`. Leave empty for all. |
| `maxResults` | integer | Stop after this many trademarks (default 50, max 5000). |
| `watchLabel` | string | Optional tag copied onto every row, so scheduled runs can be told apart downstream. |

## Output
One item per trademark with **18 fields**: `id`, `st13`, `url` (link to the office's own record), `trademarkName`, `office`, `status`, `trademarkType`, `applicationNumber`, `registrationNumber`, `applicationDate`, `registrationDate`, `applicantNames`, `niceClasses`, `viennaCodes`, `territories`, `markImageUrl`, `detailImageUrl`, and `watchLabel` when set.

Sample row:
```json
{
  "id": "004176283",
  "st13": "004176283",
  "url": "https://www.tmdn.org/tmview/#/tmview/detail/EM500000004176283",
  "trademarkName": "SOLARWINDS",
  "office": "EM",
  "status": "Registered",
  "trademarkType": "Word",
  "applicationNumber": "004176283",
  "registrationNumber": "004176283",
  "applicationDate": "2004-11-22",
  "registrationDate": "2005-08-30",
  "applicantNames": ["SolarWinds Worldwide, LLC"],
  "niceClasses": ["9", "42"],
  "viennaCodes": [],
  "territories": ["EM"],
  "markImageUrl": null,
  "detailImageUrl": null
}
```

## FAQ

**Why are `viennaCodes` and `markImageUrl` empty on some rows?**
`viennaCodes` (figurative-element classification) only exists for `trademarkType: "Figurative"` marks — a plain word or stylized-character mark has no image elements to classify, so it's correctly empty. `markImageUrl`/`detailImageUrl` are populated for most records regardless of type (TMview generates a thumbnail URL per record), but a handful of older or office-specific entries omit it upstream — treat a `null` there as "no image on file at the source office," not a bug.

**Why does the same brand appear more than once?**
Trademarks are filed per office and per class. A global brand typically holds a separate registration in each office it operates in, and sometimes multiple classes within one office — each is a distinct legal record with its own `id`.

**Does this replace a formal trademark clearance search?**
No. This is a fast screening tool over TMview's public index. For legal clearance opinions or freedom-to-operate analysis, consult a trademark attorney or the offices' own certified search tools.

## Use cases
- **Brand clearance screening** — check a proposed name against 70+ offices before filing, in one search instead of dozens.
- **Opposition watch** — track a competitor's or your own portfolio's application status (`Filed` → `Registered`/`Withdrawn`) with scheduled runs and `watchLabel`.
- **Competitor portfolio mapping** — pull every mark an applicant holds by searching their brand name and reviewing `applicantNames`/`office`/`niceClasses` across results.

## Pricing
`result` — charged per returned trademark record, from $0.002/result. The run start is free.

## Notes
Only public data from the official TMview database is collected. Respect the source's terms of use when using the output. Issues or feature requests: support@fetchsmith.com. Also available as a hosted API at https://fetchsmith.com

## Related guides
See more tools like this at [fetchsmith.com/tools](https://fetchsmith.com/tools).
