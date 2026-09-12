# UK Public Contracts — Find a Tender + Contracts Finder (OCDS API)

Search **UK public-sector procurement notices** — live tender opportunities, contract awards and pipeline notices — from **both official UK portals**, and get them back as flat, ready-to-use JSON rows in one merged, deduplicated feed.

- **Find a Tender (FTS)** publishes **above-threshold** contracts. It is an authoritative but thin feed — roughly 7–8 tender-stage notices a day.
- **Contracts Finder (CF)** publishes the far larger **sub-threshold** flow — the sub-£139k central-government and sub-£214k wider-public-sector contracts that never reach Find a Tender. Typically ~18 tender-stage and 100+ award notices a day.

Searching only one portal means missing most of the UK market. This Actor queries both by default, normalizes them into a single row shape, dedupes them, and tags every row with a `source` field (`fts` / `cf`) so you always know which portal it came from.

Both portals speak [OCDS](https://standard.open-contracting.org/) — deeply nested release packages where the buyer's email is four levels down inside a `parties[]` array, the CPV codes are scattered across `tender.items[].additionalClassifications[]`, and the awarded value usually isn't on the award at all. The two portals also disagree in small ways (Contracts Finder has no lots and puts SME suitability and the contract period on the tender; Find a Tender puts them per lot). This Actor flattens and reconciles all of it into one row per notice.

**Post-Brexit UK notices are not in EU TED**, so this is additive coverage if you already track EU procurement (see our [EU TED Tenders Scraper](https://apify.com/fetchsmith/eu-ted-tenders-scraper)).

## What you get

One row per notice, including:

- **Buyer contact details** — `buyerName`, `buyerEmail`, `buyerPhone`, `buyerUrl`, full postal address and UK NUTS region. This is what turns a notice into a lead.
- **The opportunity** — `title`, `description`, `status`, `procurementMethod`, `mainProcurementCategory`, `legalBasis`.
- **Money** — `valueAmount` / `valueCurrency` for tenders; `awardValueAmount` / `awardValueCurrency` for awards.
- **Timing** — `deadlineDate` (submission deadline), `awardPeriodStart`, `contractStartDate`, `contractEndDate`, `contractDateSigned`.
- **Classification** — `cpvCode` + `cpvDescription` plus the full `cpvCodes` list gathered from every lot and item.
- **Lots** — `lotCount`, `lotTitles`, `suitableForSme`, `suitableForVcse` (read per-lot on Find a Tender, tender-level on Contracts Finder).
- **Awards** — `awardedSuppliers` (who won), `awardStatus`, `contractCount`.
- **Delivery** — `deliveryRegions` (NUTS codes) and `deliveryLocations` (free text).
- `source` / `sourceName` — which portal the row came from (`fts` / `cf`).
- `noticeUrl` — the public notice page on the portal it came from.

## Use cases

- **Bid pipeline / lead generation.** Filter to your CPV codes and `openOnly: true` and you get every live UK opportunity in your sector, with the buyer's email address attached.
- **Competitor intelligence.** Set `stages: ["award"]` to see who is winning contracts, for how much, from which buyers.
- **Market sizing.** Pull a year of awards for a CPV family and total the contract values.
- **Alerting.** Run on a schedule with `updatedWithinDays: 1` and push new matches into your CRM or Slack.

## Input

| Field | Type | Default | Notes |
|---|---|---|---|
| `sources` | array | `["fts","cf"]` | Which portals to search. `cf` = Contracts Finder (sub-threshold, high volume), `fts` = Find a Tender (above-threshold, thin). Both by default. |
| `stages` | array | `["tender"]` | `planning`, `tender` (opportunities) and/or `award` (winners). |
| `updatedWithinDays` | integer | `7` | Only notices published/updated in the last N days. Newest first. |
| `dateFrom` / `dateTo` | string | — | Absolute date window, e.g. `2026-08-01` (or a full ISO datetime). Setting either one **overrides** `updatedWithinDays`. Both portals enforce this server-side, so nothing is fetched and discarded. A bare date means midnight, so `dateTo: "2026-08-31"` excludes the 31st — use `2026-09-01` to include it. |
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

**What is the difference between the two portals?**
Find a Tender carries **above-threshold** UK public contracts (the post-Brexit replacement for the UK's TED publication), including Scotland, Wales and Northern Ireland. Contracts Finder carries the **sub-threshold** contracts below those limits — a much larger flow, and the one most SMEs actually bid on. They are separate systems with separate APIs; a contract normally appears on one or the other, not both. Rows are deduplicated on `ocid` and notice id regardless.

**Why does a 10-day Find-a-Tender-only query only return ~75 notices?**
Because that is genuinely how many there are — Find a Tender carries roughly 7–8 new tender-stage notices a day, and none on weekends. This is exactly why the Actor searches Contracts Finder too by default. Widen `updatedWithinDays` (or use `dateFrom`/`dateTo`) for a bigger set, or leave `sources` at its default.

**In what order do results come back?**
Newest-first within each portal, but the two portals are interleaved row-by-row when both are selected — so even a small `maxResults` gets a mix of both instead of one portal filling the whole quota first. Set `sources: ["cf"]` or `["fts"]` if you want rows from only one portal.

**Why is `awardValueAmount` sometimes missing on award notices?**
Because the buyer did not publish a value. Where a value exists it is usually attached to the signed contract rather than the award, so this Actor reads `contracts[].value` and totals it (`contractCount` tells you how many contracts were summed, and `awardValueSource` says whether the number came from the award or the contracts).

**Do you need a proxy or an API key?**
No. Both portals' OCDS APIs are free, key-free and open-licensed (Open Government Licence v3). The Actor self-throttles per portal to stay under each API's rate limit and backs off politely if it still hits one.

**Is this legal?**
Yes — it reads two official UK government open-data APIs under the OGL v3 licence. The contact details published on a notice are organisational procurement contacts, published by the buyer for exactly this purpose.

## Source code

https://github.com/Fetchsmith/fetchsmith/tree/main/actors/uk-find-a-tender-scraper

## Related guides
Engineering write-ups behind this Actor:
- [The UK publishes every public contract as OCDS JSON — and the money isn't where you'd look](https://fetchsmith.com/blog/uk-find-a-tender-ocds-json-api)

More tools: [fetchsmith.com/tools](https://fetchsmith.com/tools)
