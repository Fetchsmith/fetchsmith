# EU TED Tenders — Public Procurement Notice Scraper

Search **TED (Tenders Electronic Daily)**, the EU's official public-procurement journal, and get clean, structured JSON back — no EU login, no scraping tricks, just the official free API normalized into a usable shape.

## What it does
- Queries the official `api.ted.europa.eu` Search API (no key, no auth required).
- Filters by buyer country, CPV code, notice type and publication date, or drop in a raw TED expert-query string for full control.
- Normalizes TED's raw response: notices come back as multilingual maps (`{"deu": ["..."]}`) with heavily duplicated per-lot arrays (the same CPV code repeated a dozen times). This Actor flattens each notice to one row with an English-preferred title/buyer name, deduplicated CPV/contract-nature arrays, and the earliest deadline date.
- Pay per result: you are charged only for notices actually returned.
- HTTP-only (no browser), so runs are fast and cheap.

## Input
| Field | Type | Description |
|---|---|---|
| `countries` | array | ISO 3166-1 alpha-3 buyer country codes (e.g. `DEU`, `FRA`). Empty = all. |
| `cpvCodes` | array | 8-digit CPV codes to filter by (e.g. `72000000` for IT services). Empty = all. |
| `noticeTypes` | array | TED notice-type codes (e.g. `cn-standard`, `can-standard`, `pin-standard`). Empty = all. |
| `publishedWithinDays` | integer | Only notices published in the last N days. Default 7. |
| `expertQuery` | string | Raw TED expert-query string — overrides the filters above entirely. |
| `maxResults` | integer | Stop after this many notices. Default 100. |

## Output
One row per notice: `publicationNumber`, `noticeType`, `procedureType`, `title` (+ `titleLanguage`), `buyerName`, `buyerCountry`, `buyerCity`, `contractNature` (array), `cpvCodes` (array), `description`, `totalValue` + `totalValueCurrency`, `deadlineDate`, `deadlineReceiptRequestDate`, `publicationDate`, `noticeUrl`.

## Pricing
`result` — $0.003 per returned notice. The run start is free, no minimum spend.

## FAQ
**Why not just call the TED API myself?** You can — it's free and public. What you get here is normalization: TED's raw fields are multilingual maps and duplicated per-lot arrays, which are painful to consume directly. This Actor gives you one flat row per notice with an English-preferred title, a deduplicated CPV list and a single deadline date.

**Does this cover contract value?** Yes, when TED has it (`totalValue`/`totalValueCurrency`) — not every notice type carries a value (e.g. prior-information notices often don't).

**Can I search full text?** Not directly in the simple filters yet — use `expertQuery` with TED's expert-search syntax for anything beyond country/CPV/type/date.

## Notes
Only public data from an official EU government API is collected — no ToS or anti-bot risk. Issues or feature requests: support@fetchsmith.com. Also available as a hosted API at https://fetchsmith.com
