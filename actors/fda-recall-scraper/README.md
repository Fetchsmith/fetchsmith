# FDA Recall Scraper — Food, Drug & Device Enforcement Reports

Search every US FDA product recall from the official **openFDA enforcement API** — food, drug and device — and get it back as flat, typed JSON/CSV/Excel rows.

This Actor covers **all three FDA recall types in a single run and a single schema**, interleaved and tagged with `productType`, so a compliance sweep is one job instead of three. Drug recalls additionally come with the barcode identifiers you need to match a recall against your own catalogue: **NDC, package NDC, UPC**, brand and generic name, manufacturer and substance. At **$0.0035/result on the free plan and $0.0024 on Gold and above, with no start fee**, it undercuts every all-three-types competitor we checked — the most-used one charges $0.05/result for the same raw openFDA data plus an AI severity score we don't attempt to replicate.

No API key, no login, no browser. Public US government open data ([openFDA licence](https://open.fda.gov/license/)).

## What you can do with it

- **Retailers and distributors** — pull every Class I recall for your state or category and check it against the products you carry.
- **Compliance and QA teams** — monitor `status: "Ongoing"` recalls in your product category on a schedule.
- **Product-liability and personal-injury firms** — search recall reasons and firm names across the full history.
- **Pharmacy and healthcare** — match drug recalls to your inventory by **NDC or UPC**, not by fuzzy product-name matching.
- **Insurers and risk analysts** — build a recall time series by firm, classification or distribution pattern.
- **Newsrooms and researchers** — track "what got recalled this week" across all three FDA centres at once.

## Input

All fields are optional; with an empty input you get the last year of food, drug and device recalls, newest first.

| Field | Type | Description |
|---|---|---|
| `productTypes` | array | `food`, `drug`, `device`. Default: all three. Results are interleaved, not one type after another. |
| `dateField` | string | Which date `reportDateFrom`/`reportDateTo` filter on: `report_date` (default, when FDA published the report), `recall_initiation_date` (when the recall actually started), or `termination_date` (when it closed out). |
| `reportDateFrom` | string | Earliest date for the field above, `YYYY-MM-DD` or `YYYYMMDD`. Default: one year ago. |
| `reportDateTo` | string | Latest date for the field above. Default: today. |
| `classifications` | array | `Class I` (reasonable probability of serious harm or death), `Class II` (temporary/reversible), `Class III` (unlikely to cause harm). Empty = all. |
| `states` | array | Two-letter state codes of the **recalling firm**. Empty = all. |
| `status` | string | `Ongoing`, `Completed`, `Terminated`, `Pending`. Empty = all. |
| `recallingFirm` | string | Filter to one firm, e.g. `Tyson Foods`. Narrower than `searchQuery`, which also matches product description and recall reason. |
| `city` | string | Filter to recalls whose recalling firm is in this city, e.g. `Chicago`. |
| `voluntaryMandated` | string | `Voluntary: Firm initiated` or `FDA Mandated` (rare, under 2% of recalls). Empty = both. |
| `searchQuery` | string | Free-text phrase matched against product description, reason for recall and recalling firm. |
| `order` | string | `desc` (newest first, default) or `asc` — sorts by whichever field `dateField` selects. |
| `maxResults` | integer | Total rows across all selected product types. Default 100. |

Filters are **ANDed**. A search query plus a state plus a classification over a short date window often has zero real matches — drop one filter and retry.

### Example: Class I food and drug recalls in California this year

```json
{
  "productTypes": ["food", "drug"],
  "classifications": ["Class I"],
  "states": ["CA"],
  "reportDateFrom": "2026-01-01",
  "maxResults": 500
}
```

## Output

33 fields per row. Every date is converted from openFDA's `YYYYMMDD` strings to ISO `YYYY-MM-DD`.

**All product types:** `productType`, `recallNumber`, `eventId`, `status`, `classification`, `voluntaryMandated`, `initialFirmNotification`, `recallingFirm`, `city`, `state`, `country`, `productDescription`, `productQuantity`, `reasonForRecall`, `distributionPattern`, `codeInfo`, `moreCodeInfo`, `reportDate`, `recallInitiationDate`, `centerClassificationDate`, `terminationDate`.

**Drug recalls only** (see the FAQ): `brandName`, `genericName`, `manufacturerName`, `substanceName`, `productNdc`, `packageNdc`, `upc`, `applicationNumber`, `drugRoute`, `rxcui`, `unii`, `splSetId`.

### Sample row (drug recall, trimmed)

```json
{
  "productType": "drug",
  "recallNumber": "D-0785-2026",
  "eventId": "99584",
  "status": "Ongoing",
  "classification": "Class II",
  "voluntaryMandated": "Voluntary: Firm initiated",
  "initialFirmNotification": "Letter",
  "recallingFirm": "ACCORD HEALTHCARE, INC.",
  "city": "Raleigh",
  "state": "NC",
  "country": "United States",
  "productDescription": "Levothyroxine Sodium Tablets, USP, 200 mcg (0.2 mg), packaged in a) 90-count bottles (NDC 16729-457-15) and b) 1000-count bottles (NDC 16729-457-17), ...",
  "productQuantity": "N/A",
  "reasonForRecall": "Subpotent Drug",
  "distributionPattern": "Nationwide within the United States",
  "codeInfo": "a) Lot # D2402430, D2402431, Exp Date: 10/31/2026. ...",
  "reportDate": "2026-09-02",
  "recallInitiationDate": "2026-08-06",
  "centerClassificationDate": "2026-08-21",
  "terminationDate": null,
  "brandName": "LEVOTHYROXINE SODIUM",
  "genericName": "LEVOTHYROXINE SODIUM",
  "manufacturerName": "Accord Healthcare Inc.",
  "substanceName": ["LEVOTHYROXINE SODIUM"],
  "productNdc": ["16729-447", "16729-458", "16729-448"],
  "packageNdc": ["16729-458-15", "16729-458-17"],
  "upc": ["0316729447157", "0316729449151"],
  "applicationNumber": "ANDA212399",
  "drugRoute": ["ORAL"],
  "rxcui": ["892246", "892251"],
  "unii": ["9J765S329G"],
  "splSetId": "a6233381-3043-4e9a-aaa6-a6b105e5142b"
}
```

## Pricing

Pay per result: **$0.0035 per recall on the free plan, dropping to $0.0024 on Gold and above** (Bronze $0.003, Silver $0.0027), with no Actor-start fee. 1,000 recalls costs $3.50 on the free plan, $2.40 on Gold. You are charged only for rows actually delivered to your dataset.

## FAQ

**Why are the NDC/UPC/brand-name fields empty on my food and device rows?**
Because FDA only publishes them for drugs. The `openfda` block that carries those identifiers is populated on drug enforcement reports and empty on food and device ones — verified on live samples, not an assumption. The fields are always present in the schema so your CSV columns stay stable; they are simply `null` or `[]` outside drug rows.

**In what order do results come back?**
Interleaved across the product types you selected — one row per type per round — so a small `maxResults` gives you a mix rather than filling the whole quota from `food`. Within each product type, rows are ordered by `reportDate`.

**What is the difference between `reportDate` and `recallInitiationDate`?**
`recallInitiationDate` is when the firm started the recall; `reportDate` is when FDA published the enforcement report, which is often weeks or months later. The date filters apply to **`reportDate` by default** — set `dateField: "recall_initiation_date"` to filter on when the recall actually began instead, or `"termination_date"` to find recalls that closed out in a window.

**Can I get more than 25,000 rows from one filter?**
Yes. openFDA refuses to page past row 25,000 (`skip` is hard-capped), so when a query matches more than that the Actor automatically splits it into narrower `reportDate` windows and pages each one — the year-boundary split was verified to sum exactly to the unsplit total, with no duplicated or dropped rows. If one single window still exceeds the cap, the run logs a warning telling you to narrow the date range.

**Does `states` mean where the product was sold?**
No — it is the recalling firm's own state. For distribution, read the `distributionPattern` field (e.g. "Nationwide within the United States", or a list of states).

**Is this legal / does it need an API key?**
It reads openFDA, the FDA's own public open-data API, which requires no key and is explicitly published for reuse. Rows are firm and product safety data, not personal data.

**My run returned zero rows.**
The log explains why in order of likelihood. Usually it is ANDed filters that have no real intersection, or a `reportDate` window that is too narrow. Try one distinctive word in `searchQuery` rather than a long phrase.

**How does this compare to other FDA recall scrapers?**
Checked live pricing again on 2026-09-13, against the real leader by volume (`scrapers_lat/openfda-food-recalls-scraper`, food-only): they charge $0.01/result tapering to $0.008 on Gold+, **plus a separate $0.004→$0.001 Actor-start fee** — we are $0.0035/result on the free plan and $0.0024 on Gold and above, **with no start fee**, cheaper at every run size, and we cover drug and device recalls too, not just food. Their one real feature edge — filtering by recalling firm, city, voluntary/mandated status, and choosing which date field to filter on (report vs. initiation vs. termination date) — is now matched (`recallingFirm`, `city`, `voluntaryMandated`, `dateField` above).

## Related guides

- [All FetchSmith scrapers](https://fetchsmith.com/tools) — 17 HTTP-only Actors for public data sources, no browser required.
- [The FDA publishes every product recall as JSON — but you can't page past row 25,000, and only drugs come with a barcode](https://fetchsmith.com/blog/fda-openfda-recall-json-api) — the full write-up of the 25,000-row skip cap, the date-chunking workaround and the drug-only `openfda` barcode fields.
- [Scraping USAspending's federal awards JSON API](https://fetchsmith.com/blog/usaspending-federal-awards-json-api) — the same "US government publishes it as keyless JSON" pattern, applied to federal contracts and grants.

Source code: https://github.com/Fetchsmith/fetchsmith/tree/main/actors/fda-recall-scraper
