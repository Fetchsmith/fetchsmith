# UK Find a Tender — Public Contract Notices (OCDS API)

Search **UK public-sector procurement notices** — live tender opportunities, contract awards and pipeline notices — from the UK government's **official Find a Tender OCDS API**, and get them back as flat, ready-to-use JSON rows.

Find a Tender is where every above-threshold UK public contract is published. The raw API speaks [OCDS](https://standard.open-contracting.org/) — deeply nested release packages where the buyer's email is four levels down inside a `parties[]` array, the CPV codes are scattered across `tender.items[].additionalClassifications[]`, and the awarded value usually isn't on the award at all. This Actor flattens all of that into one row per notice.

**Post-Brexit UK notices are not in EU TED**, so this is additive coverage if you already track EU procurement (see our [EU TED Tenders Scraper](https://apify.com/fetchsmith/eu-ted-tenders-scraper)).

## What you get

One row per notice, including:

- **Buyer contact details** — `buyerName`, `buyerEmail`, `buyerPhone`, `buyerUrl`, full postal address and UK NUTS region. This is what turns a notice into a lead.
- **The opportunity** — `title`, `description`, `status`, `procurementMethod`, `mainProcurementCategory`, `legalBasis`.
- **Money** — `valueAmount` / `valueCurrency` for tenders; `awardValueAmount` / `awardValueCurrency` for awards.
- **Timing** — `deadlineDate` (submission deadline), `awardPeriodStart`, `contractStartDate`, `contractEndDate`, `contractDateSigned`.
- **Classification** — `cpvCode` + `cpvDescription` plus the full `cpvCodes` list gathered from every lot and item.
- **Lots** — `lotCount`, `lotTitles`, `suitableForSme`, `suitableForVcse`.
- **Awards** — `awardedSuppliers` (who won), `awardStatus`, `contractCount`.
- **Delivery** — `deliveryRegions` (NUTS codes) and `deliveryLocations` (free text).
- `noticeUrl` — the public Find a Tender page for the notice.

## Use cases

- **Bid pipeline / lead generation.** Filter to your CPV codes and `openOnly: true` and you get every live UK opportunity in your sector, with the buyer's email address attached.
- **Competitor intelligence.** Set `stages: ["award"]` to see who is winning contracts, for how much, from which buyers.
- **Market sizing.** Pull a year of awards for a CPV family and total the contract values.
- **Alerting.** Run on a schedule with `updatedWithinDays: 1` and push new matches into your CRM or Slack.

## Input

| Field | Type | Default | Notes |
|---|---|---|---|
| `stages` | array | `["tender"]` | `planning`, `tender` (opportunities) and/or `award` (winners). |
| `updatedWithinDays` | integer | `7` | Only notices published/updated in the last N days. Newest first. |
| `cpvCodes` | array | `[]` | e.g. `72000000`. Trailing zeros are treated as a prefix, so `72000000` matches every `72xxxxxx` code. Matched against every CPV on the notice, not just the headline one. |
| `searchQuery` | string | — | Every word must appear in title, description, buyer name, CPV description or lot titles. |
| `minValueGbp` / `maxValueGbp` | integer | — | Contract-value bounds. Notices with no published value are excluded when either is set. |
| `openOnly` | boolean | `false` | Only notices whose submission deadline is still in the future. |
| `maxResults` | integer | `100` | Hard stop. |
| `maxPagesScanned` | integer | `50` | Safety cap on API pages read while looking for matches. Raise it for narrow filters over long date ranges. |

### Example

```json
{
  "stages": ["tender"],
  "updatedWithinDays": 30,
  "cpvCodes": ["72000000"],
  "openOnly": true,
  "maxResults": 200
}
```

## Sample output (one row, trimmed)

```json
{
  "ocid": "ocds-h6vhtk-06f762",
  "noticeId": "086108-2026",
  "noticeUrl": "https://www.find-tender.service.gov.uk/Notice/086108-2026",
  "stage": ["tender"],
  "title": "Maryhill Housing Association - Heating Maintenance 2026 - 2031",
  "status": "active",
  "procurementMethod": "open",
  "mainProcurementCategory": "services",
  "cpvCode": "50720000",
  "cpvDescription": "Repair and maintenance services of central heating",
  "cpvCodes": ["50720000", "44621200", "44620000", "42160000"],
  "valueAmount": 710000,
  "valueCurrency": "GBP",
  "deadlineDate": "2026-10-12T17:00:00+01:00",
  "buyerName": "Maryhill Housing Association",
  "buyerEmail": "enquiries@maryhill.org.uk",
  "buyerPhone": "+44 1419462466",
  "buyerPostalCode": "G20 8RG",
  "deliveryRegions": ["UKM82"],
  "deliveryLocations": ["Maryhill & Ruchill areas of Glasgow"]
}
```

## Pricing

**$0.004 per result**, no start fee. You are charged only for rows that actually land in your dataset — notices filtered out by `cpvCodes`, `searchQuery`, the value bounds or `openOnly` are **never charged**, even though the Actor had to read them from the API to decide.

## FAQ

**Which notices are in Find a Tender?**
Above-threshold UK public contracts (the post-Brexit replacement for the UK's TED publication), including Scotland, Wales and Northern Ireland. Lower-value notices generally go to Contracts Finder instead.

**Why does a 10-day tender-stage query only return ~75 notices?**
Because that is genuinely how many there are — Find a Tender carries roughly 7–8 new tender-stage notices a day. Widen `updatedWithinDays` for a bigger set.

**Why is `awardValueAmount` sometimes missing on award notices?**
Because the buyer did not publish a value. Where a value exists it is usually attached to the signed contract rather than the award, so this Actor reads `contracts[].value` and totals it (`contractCount` tells you how many contracts were summed, and `awardValueSource` says whether the number came from the award or the contracts).

**Do you need a proxy or an API key?**
No. Find a Tender's OCDS API is free, key-free and open-licensed (Open Government Licence v3). The Actor self-throttles to stay under the API's rate limit and backs off politely if it still hits one.

**Is this legal?**
Yes — it reads an official UK government open-data API under the OGL v3 licence. The contact details published on a notice are organisational procurement contacts, published by the buyer for exactly this purpose.

## Source code

https://github.com/Fetchsmith/fetchsmith/tree/main/actors/uk-find-a-tender-scraper
