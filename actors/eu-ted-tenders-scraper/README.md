# EU TED Tenders — Public Procurement Notice Scraper

Search **TED (Tenders Electronic Daily)**, the EU's official public-procurement journal, and get clean, structured JSON back — no EU login, no scraping tricks, just the official free `api.ted.europa.eu` Search API normalized into a usable shape.

## Use cases
- **Bid/lead monitoring** — track new contract notices in your CPV codes and countries so a sales team hears about a tender the day it's published, not weeks later browsing ted.europa.eu by hand.
- **Government-spending research & journalism** — pull every notice for a buyer, country or sector over a date range with contract value, buyer and deadline already flattened into one row.
- **Market-sizing** — aggregate `totalValue`/`totalValueCurrency` across CPV codes or countries to estimate how much a government is spending in a given category.
- **Lead generation** — `buyerEmail`/`buyerPhone`/`buyerUrl` give a direct contact point for the procurement office behind each notice, most of them real role mailboxes (`einkauf@…`, `vergabestelle@…`).
- **Deadline tracking** — `deadlineDate` (earliest of any per-lot deadline) and `deadlineReceiptRequestDate` let you build a reminder feed instead of re-checking the site.

## Input
| Field | Type | Description |
|---|---|---|
| `countries` | array | ISO 3166-1 alpha-3 buyer country codes (e.g. `DEU`, `FRA`). Empty = all. |
| `cpvCodes` | array | 8-digit CPV codes to filter by (e.g. `72000000` for IT services). Empty = all. |
| `noticeTypes` | array | TED notice-type codes (e.g. `cn-standard`, `can-standard`, `pin-standard`). Empty = all. |
| `publishedWithinDays` | integer | Only notices published in the last N days. Default 7. Ignored if `publicationDateFrom`/`publicationDateTo` is set. |
| `publicationDateFrom` / `publicationDateTo` | string | Absolute date window, `YYYYMMDD` or `YYYY-MM-DD`. Either or both — overrides `publishedWithinDays`. |
| `keywords` | string | Free-text search across the notice's title, description and buyer name (TED's `FT~` operator). |
| `expertQuery` | string | Raw TED expert-query string — overrides all the filters above entirely. |
| `maxResults` | integer | Stop after this many notices. Default 100. |
| `outputLanguage` | string | Preferred language for `title`/`description`/`buyerName`/`buyerCity`/`noticeUrl` (24 EU languages, e.g. `deu`, `fra`, `spa`). Default `eng`. Falls back to English, then to whatever TED provided, if a notice has no translation into your chosen language. |

### Example: German construction/engineering notices from the last 2 weeks

```json
{
  "countries": ["DEU"],
  "cpvCodes": ["71000000"],
  "publishedWithinDays": 14,
  "maxResults": 100
}
```

Multiple values within one field (e.g. two country codes) are OR'd together; different fields (country AND CPV code) are AND'd. Leave every filter empty to pull all recent notices across the whole EU/EEA.

## Output

One row per notice:

| Field | Description |
|---|---|
| `publicationNumber` | TED's own ID for the notice, e.g. `596425-2026`. |
| `noticeType`, `noticeSubtype`, `procedureType` | TED's notice-type code, subtype code, and procedure type (e.g. `open`, `restricted`). |
| `title`, `titleLanguage` | Notice title in your chosen `outputLanguage` (or its fallback), and which language it actually came back in. |
| `buyerName`, `buyerCountry`, `buyerCity` | The contracting authority and its location. |
| `buyerEmail`, `buyerPhone`, `buyerUrl` | The buyer's own published contact details, when TED has them. |
| `placeOfPerformanceCountry`, `placeOfPerformanceCity` | Where the contract is performed (arrays, deduplicated — TED repeats these per lot). |
| `contractNature`, `cpvCodes` | e.g. `["services"]`, `["71000000"]` (arrays, deduplicated). |
| `description` | Free-text lot description, in `outputLanguage`. |
| `totalValue`, `totalValueCurrency` | Contract value, when the notice type carries one — see the FAQ. |
| `deadlineDate`, `deadlineReceiptRequestDate` | Earliest submission deadline across all lots, and the tender-documents-request deadline. |
| `publicationDate` | When TED published the notice. |
| `noticeUrl` | Link to the notice's PDF (or XML) on ted.europa.eu, in your chosen language when available. |

### Sample row (real output, German construction-engineering notice)

```json
{
  "publicationNumber": "596425-2026",
  "noticeType": "cn-standard",
  "procedureType": "restricted",
  "title": "Germany – Architectural, construction, engineering and inspection services – BLB NRW Köln / Universität Bonn / Neubau Molekulare Biologie (ImBIG) / Bauphysik",
  "titleLanguage": "eng",
  "buyerName": "Bau- und Liegenschaftsbetrieb NRW Köln",
  "buyerCountry": "DEU",
  "buyerCity": "Köln",
  "noticeSubtype": "16",
  "buyerEmail": "BLBVergabe@blb.nrw.de",
  "buyerPhone": "+49 0",
  "buyerUrl": "http://www.blb.nrw.de",
  "placeOfPerformanceCountry": ["DEU"],
  "placeOfPerformanceCity": ["Bonn"],
  "contractNature": ["services"],
  "cpvCodes": ["71000000"],
  "description": "Leistungen der Fachplanung Bauphysik (Wäreschutz, Raumakustik, Bauakustik)",
  "totalValue": null,
  "totalValueCurrency": null,
  "deadlineDate": "2026-09-16",
  "deadlineReceiptRequestDate": "2026-09-29",
  "publicationDate": "2026-08-31",
  "noticeUrl": "https://ted.europa.eu/en/notice/596425-2026/pdf"
}
```

`totalValue` is `null` here because this particular notice type doesn't carry one — see the FAQ.

## Pricing
`result` — $0.003 per returned notice. The run start is free, no minimum spend.

## FAQ
**Why not just call the TED API myself?** You can — it's free and public. What you get here is normalization: TED's raw fields are multilingual maps and duplicated per-lot arrays, which are painful to consume directly. This Actor gives you one flat row per notice with an English-preferred title, a deduplicated CPV list and a single deadline date.

**Does this cover contract value?** Yes, when TED has it (`totalValue`/`totalValueCurrency`) — not every notice type carries a value (e.g. prior-information notices often don't).

**Can I search full text?** Yes — set `keywords` (e.g. `"cloud hosting"`), which is sent as TED's `FT~` full-text operator against title/description/buyer name. For anything beyond that, `expertQuery` gives raw access to TED's expert-search syntax.

**Can I pull a specific historical month or quarter, not just "the last N days"?** Yes — set `publicationDateFrom`/`publicationDateTo` (either or both) to an absolute `YYYYMMDD` window; it overrides `publishedWithinDays`.

**Can I get titles/descriptions in a language other than English?** Yes — set `outputLanguage` to any of 24 EU language codes (e.g. `deu`, `fra`, `spa`, `pol`). TED publishes every notice in every EU language, so this returns the same notice in your chosen language instead of English, including a matching-language notice URL. Notices without a translation into that language fall back to English automatically.

**How do multiple filters combine — AND or OR?** Values within the same field are OR'd (`countries: ["DEU", "FRA"]` matches either), and different fields are AND'd (country + CPV code together narrows, doesn't widen). Set `expertQuery` if you need anything more precise than that — it replaces all the filters above with TED's own raw expert-search syntax.

**Is `buyerEmail`/`buyerPhone` a personal contact?** No — these are the contracting authority's own published contact point for the procedure (`organisation-email-buyer`/`organisation-tel-buyer` in TED's schema), republished verbatim from an official EU government source. Most are role mailboxes (`vergabestelle@…`, `einkauf@…`); we don't enrich or cross-reference them.

## Notes
Only public data from an official EU government API is collected — no ToS or anti-bot risk. Issues or feature requests: support@fetchsmith.com. Also available as a hosted API at https://fetchsmith.com

Source code: https://github.com/Fetchsmith/fetchsmith/tree/main/actors/eu-ted-tenders-scraper

## Related guides
Engineering write-ups behind this Actor:
- [The EU publishes every public contract as JSON — in 24 languages, with the CPV code repeated eight times](https://fetchsmith.com/blog/eu-ted-tenders-public-json-api)

More tools: [fetchsmith.com/tools](https://fetchsmith.com/tools)
