# USAspending — US Federal Contracts & Grants Scraper

Search **every US federal award** — contracts, IDVs, grants, direct payments, other financial assistance and loans — straight from the official **USAspending.gov** awards API, and get flat JSON rows you can drop into a CRM, a spreadsheet or a model.

No API key, no login, no proxy: this Actor uses the US government's public open-data API (`api.usaspending.gov`), so the data is authoritative and there is nothing to violate. Awards data covers recipients (companies, universities, state agencies), not individuals.

## What you can do with it

- **Federal-contractor lead lists** — every company that won work from a given agency, with UEI, address and NAICS/PSC codes.
- **Competitor tracking** — pull one recipient's full award history by name keyword and watch amounts, agencies and end dates (recompete timing).
- **Grant prospecting** — filter to grants and cooperative agreements by CFDA/Assistance Listing program and state.
- **Market sizing** — how much a given agency obligated on solar, cyber, AI or any keyword over any window since 2007.
- **Recompete alerts** — sort by end date and find contracts about to expire in your NAICS.

## Input

| Field | Type | Default | Notes |
|---|---|---|---|
| `awardCategories` | array | `["contracts"]` | `contracts`, `idvs`, `grants`, `direct_payments`, `other_financial_assistance`, `loans`. Pick several — each is fetched separately and merged. |
| `startDate` / `endDate` | string | last 365 days | `YYYY-MM-DD`, filters on award action date. Nothing exists before `2007-10-01`; earlier dates are clamped. |
| `keywords` | array | – | Free text over description, recipient and agency. Multiple keywords are ORed. |
| `agencies` | array | – | **Exact** top-tier agency names, e.g. `Department of Energy`. Abbreviations like `DOE` match nothing. |
| `placeOfPerformanceStates` | array | – | Two-letter USPS codes for where the work happens (`CA`, `TX`). |
| `recipientStates` | array | – | Two-letter USPS codes for the recipient's own address. |
| `minAwardAmount` / `maxAwardAmount` | integer | – | Obligated amount bounds in USD. |
| `sortBy` | string | `awardAmount` | `awardAmount`, `lastModifiedDate`, `startDate`, `recipientName`. |
| `order` | string | `desc` | `desc` or `asc`. |
| `maxResults` | integer | `100` | Total across all selected categories. |
| `maxPagesPerCategory` | integer | `50` | Depth cap, 100 awards per page. |

All filters are ANDed. Awards filtered out are never pushed and never charged.

## Output

One flat row per award:

| Field | Example |
|---|---|
| `awardId` | `89243425FEE000489` |
| `awardUrl` | `https://www.usaspending.gov/award/CONT_AWD_89243425FEE000489_8900_…` |
| `awardCategory` / `awardType` | `contracts` / `BPA CALL` |
| `recipientName`, `recipientUei`, `recipientId` | `ENERGY TECHNOLOGY ALLIANCE LLC`, `WDTLX4NKRKC8` |
| `recipientAddress`, `recipientCity`, `recipientState`, `recipientCountry` | `920 NW BOND ST STE 204`, `BEND`, `OR`, `UNITED STATES` |
| `awardingAgency`, `awardingSubAgency`, `fundingAgency`, `fundingSubAgency` | `Department of Energy` |
| `description` | `SCIENTIFIC, ENGINEERING AND TECHNICAL SUPPORT (SETS) FOR DOE EERE'S SOLAR ENERGY TECHNOLOGIES OFFICE…` |
| `awardAmount`, `totalOutlays` | `7909335.88`, `7909335.88` |
| `loanValue`, `subsidyCost` | loans only — face value and subsidy cost |
| `startDate`, `endDate`, `baseObligationDate`, `lastModifiedDate` | `2025-04-30`, `2026-04-30` |
| `placeOfPerformanceCity/State/Zip/Country` | `GOLDEN`, `CO`, `80401`, `USA` |
| `naicsCode`, `naicsDescription`, `pscCode`, `pscDescription` | `562910`, `REMEDIATION SERVICES`, `R425`, `SUPPORT- PROFESSIONAL: ENGINEERING/TECHNICAL` |
| `cfdaNumbers`, `cfdaProgramTitles` | grants/loans — e.g. `["93.778"]`, `["GRANTS TO STATES FOR MEDICAID"]` |
| `disasterEmergencyFundCodes` | `["Q"]` |

### Sample row

```json
{
  "awardId": "89243425FEE000489",
  "awardUrl": "https://www.usaspending.gov/award/CONT_AWD_89243425FEE000489_8900_89243423AEE000008_8900",
  "awardCategory": "contracts",
  "awardType": "BPA CALL",
  "recipientName": "ENERGY TECHNOLOGY ALLIANCE LLC",
  "recipientUei": "WDTLX4NKRKC8",
  "recipientCity": "BEND",
  "recipientState": "OR",
  "awardingAgency": "Department of Energy",
  "awardingSubAgency": "Department of Energy",
  "description": "SCIENTIFIC, ENGINEERING AND TECHNICAL SUPPORT (SETS) FOR DOE EERE'S SOLAR ENERGY TECHNOLOGIES OFFICE (SETO)",
  "awardAmount": 7909335.88,
  "totalOutlays": 7909335.88,
  "startDate": "2025-04-30",
  "endDate": "2026-04-30",
  "placeOfPerformanceCity": "GOLDEN",
  "placeOfPerformanceState": "CO",
  "naicsCode": "562910",
  "pscCode": "R425",
  "disasterEmergencyFundCodes": ["Q"]
}
```

## Pricing

Pay per result: **$0.004 per award**, **no Actor-start fee**. You only pay for awards actually written to the dataset.

## FAQ

**Why can't I mix contracts and grants in one search on USAspending's own site?**
You can here. The underlying API rejects a request whose `award_type_codes` span two groups (`must only contain types from one group`), so this Actor runs one query per category you select and merges the results into a single dataset, deduplicated by the award's stable internal id.

**Why did my search return zero awards?**
The filters are ANDed. A keyword plus a state plus a minimum amount over a short window is often genuinely empty — drop one filter first. The other common cause is an agency name that isn't the exact top-tier spelling (`Department of Energy`, not `DOE`).

**How far back does the data go?**
`2007-10-01`. The API refuses earlier start dates, so this Actor clamps them instead of failing.

**Are loan amounts in `awardAmount`?**
No. Loans report `loanValue` (face value) and `subsidyCost` instead of an obligated amount — that is how the API models them, and both fields are passed through unchanged.

**Why does `startDate` on a row show a date decades before my search window?**
`startDate`/`endDate` filter on the award's *action date* (when it was last modified), not on `startDate`'s own value. A long-running contract (e.g. a national-lab management contract) can have a 1978 period-of-performance start and still match a 2025-2026 filter window because it was modified this year — `lastModifiedDate` is what actually falls inside your range. Sort by `lastModifiedDate` instead of `startDate` if you want the most recently active awards first.

**Is this the same as SAM.gov?**
No. SAM.gov lists pre-award *opportunities* you can bid on; USAspending lists *awards already made*. This Actor covers awards — who won, how much, which agency, and when the work ends.

**Does it need a proxy?**
No. Plain HTTPS to a public government API, so runs are fast and cheap.

**How does this compare to other USAspending scrapers?**
Checked the real `pricingInfos` and depth of the top competitors on Apify Store (2026-09-10). Pricing is bimodal: the two highest-traction players — `parseforge` (25 users, the most of any competitor) at $0.012/result + $0.16 start, and `benthepythondev` (17 users, 292 runs/30d, the most active) at $0.005/result + start — are both pricier than our $0.004/result with no start fee. Two lower-traction entrants (`copious_atoll`, 10 users; `themineworks`, 3 users) charge $0.001/result, cheaper than us on price alone — but `themineworks`' own listing advertises "18 Fields"; this Actor returns **37 typed fields across 6 award categories** (contracts, IDVs, grants, direct payments, other financial assistance, loans), each category with its own correct field mapping (loans carry `loanValue`/`subsidyCost`, not `awardAmount`) rather than one generic shape stretched across every award kind.

Source code: https://github.com/Fetchsmith/fetchsmith/tree/main/actors/us-federal-awards-scraper
