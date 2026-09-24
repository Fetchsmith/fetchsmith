# EU & European Tenders (TED) — Public Procurement & Government Tenders Europe Scraper

Search **TED (Tenders Electronic Daily)**, the EU's official public-procurement journal, and get clean, structured JSON back — no EU login, no scraping tricks, just the official free `api.ted.europa.eu` Search API normalized into a usable shape.

## Use cases
- **Bid/lead monitoring** — track new contract notices in your CPV codes and countries so a sales team hears about a tender the day it's published, not weeks later browsing ted.europa.eu by hand.
- **Government-spending research & journalism** — pull every notice for a buyer, country or sector over a date range with contract value, buyer and deadline already flattened into one row.
- **Market-sizing** — aggregate `totalValue`/`totalValueCurrency` across CPV codes or countries to estimate how much a government is spending in a given category.
- **Lead generation** — `buyerEmail`/`buyerPhone`/`buyerUrl` give a direct contact point for the procurement office behind each notice, most of them real role mailboxes (`einkauf@…`, `vergabestelle@…`).
- **Bid pipeline / deadline tracking** — `deadlineDate` (earliest submission deadline across all lots), `daysUntilDeadline` and `deadlineReceiptRequestDate` let you build a reminder feed instead of re-checking the site. Set `onlyOpenDeadlines` to get only tenders you can still bid on, and `minDaysUntilDeadline: 14` to skip the ones closing too soon to prepare a bid for.
- **Corrigendum tracking** — a filter for `noticeTypes` plus `procedureIdentifier` lets you group a notice with any corrigenda published against the same procedure, and `changeReasonDescription` tells you in plain text what changed (deadline, specs, opening date) without opening the PDF.

## Input
| Field | Type | Description |
|---|---|---|
| `countries` | array | ISO 3166-1 alpha-3 buyer country codes (e.g. `DEU`, `FRA`). Empty = all. |
| `cpvCodes` | array | 8-digit CPV codes to filter by (e.g. `72000000` for IT services). Empty = all. **TED matches the entire CPV subtree under each code you supply, at every level of the hierarchy — there is no exact-code match.** `72000000` returns notices tagged only `72313000` or `72220000`, and even a narrow code like `72267000` returns its children `72267100`/`72267200`. See the FAQ below for the measurement and the workaround. |
| `noticeTypes` | array | TED notice-type codes (e.g. `cn-standard`, `can-standard`, `pin-standard`). Empty = all. |
| `procedureType` | array | TED procedure-type codes (e.g. `open`, `restricted`, `neg-w-call`, `neg-wo-call`, `comp-dial`). Empty = all. Server-side filter, same OR-group as `noticeTypes`. |
| `publishedWithinDays` | integer | Only notices published in the last N days. Default 7. Ignored if `publicationDateFrom`/`publicationDateTo` is set. |
| `publicationDateFrom` / `publicationDateTo` | string | Absolute date window, `YYYYMMDD` or `YYYY-MM-DD`. Either or both — overrides `publishedWithinDays`. |
| `keywords` | string | Free-text search across the notice's title, description and buyer name (TED's `FT~` operator). |
| `expertQuery` | string | Raw TED expert-query string — overrides all the filters above entirely. |
| `maxResults` | integer | Stop after this many notices. Default 100. |
| `minValue` / `maxValue` | integer | Only keep notices whose `totalValue` falls in this range. Compares the raw number regardless of currency (TED reports EUR, CZK, RON, SEK, etc. per notice — check `totalValueCurrency`). Roughly half of all notices carry no value at all; those are dropped whenever either is set. |
| `onlyOpenDeadlines` | boolean | Keep only notices whose submission deadline is today or later — the tenders you can still bid on. Notices with no published deadline (award/result notices, most prior-information notices) are dropped while this is on, since an absent deadline can't be shown to be open. |
| `minDaysUntilDeadline` | integer | Keep only notices with at least this many whole days left before the deadline (`daysUntilDeadline` in the output), counted in UTC. Implies `onlyOpenDeadlines`. |
| `outputLanguage` | string | Preferred language for `title`/`description`/`buyerName`/`buyerCity`/`noticeUrl` (24 EU languages, e.g. `deu`, `fra`, `spa`). Default `eng`. Falls back to English, then to whatever TED provided, if a notice has no translation into your chosen language. |
| `flatten` | boolean | Default `false` (JSON arrays). Set `true` to join `cpvCodes`, `contractNature`, `placeOfPerformanceCountry` and `placeOfPerformanceCity` into a single comma-separated string per field, instead of a JSON array — cleaner for CSV/Excel export (Apify's default array export otherwise splits each into numbered `field/0`, `field/1` columns that shift between rows with different array lengths). |
| `watchLabel` | string | Optional. Name a saved query and get **only what is new since your last run** — see below. |
| `webhookUrl` | string | Optional. POST a small JSON completion summary (notices pushed, pages scanned, TED's reported total, dataset ID, watch new count) here when the run finishes — see FAQ. |

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

## Only what's new since last run (`watchLabel`)

A bid-monitoring job is a *subscription*, not a search: you want the notices published since you last looked, not the same hundreds of rows re-delivered (and re-charged) every morning.

Set `watchLabel` to a name for the query — `de-it-services`, say — and this Actor keeps track of which notices it has already given you under that name:

- **The first run on a new label is a free baseline.** It records what already matches, returns **zero** results and charges **nothing**. It walks notice ids only, not full notices.
- **Every run after that returns only the new notices.** Already-delivered rows are dropped before they are built or billed, so you never pay for the same notice twice.
- **A notice counts as delivered only once it has actually been charged.** Anything cut off by `maxResults` or a charge limit stays "new" for the next run rather than vanishing.
- **Changing a filter starts a fresh baseline** — a different filter is a different question, so you don't get a dump of everything the old, narrower query happened to exclude. Setting `expertQuery` also starts its own baseline, keyed on the raw query string.
- **The rolling `publishedWithinDays` window is deliberately *not* part of that identity.** It moves every day; if it counted, a daily schedule would re-seed forever and never deliver anything. `publicationDateFrom`/`publicationDateTo`, when you set them explicitly, do count.

The baseline lives in a key-value store named `fetchsmith-ted-watch` on your own account, so it survives between runs and you can inspect or reset it yourself. Point an Apify schedule at the Actor and you have a TED procurement alert.

**Baseline size cap.** A baseline holds up to **60,000** notice ids in one saved record. If a label's baseline grows past that, the oldest-first-seen ids are dropped — and a dropped id is no longer recognised, so that notice comes back as "new" on a later run **and is charged again**. The run that drops them says so explicitly: a warning in the log and `baselineTruncated` / `baselineTruncatedTotal` (this run / the whole life of the label) in the saved record and on the `webhookUrl` payload. If you see it, narrow the query (a country, a CPV code, a shorter publication-date window) or split it across several labels so each baseline stays under the cap. A baseline run also stops walking at 20,000 notice ids, and already warns separately when it hits that.

### Why there's no snapshot-diff `watchChanges` here — and what to use instead

Some of our other Actors (grants.gov, openFDA recalls, USAspending, ClinicalTrials.gov, NIH RePORTER) offer a `watchChanges` input that re-delivers a record when a field on the *same id* mutates. TED doesn't work that way: we checked live before building anything, and TED never edits a published notice. A correction (deadline moved, specs revised, opening date pushed back) is published as a **brand-new notice with its own `publicationNumber`** — the original notice's own record never changes, so there is nothing for a snapshot diff to catch. (Confirmed on real examples: publication `493171-2026` was corrected twice, by `566391-2026` and `625075-2026`, and `493171-2026` itself never mutated — three separate publication numbers, one shared `procedureIdentifier`.)

`watchLabel` already surfaces a corrigendum correctly, since it's a genuinely new `publicationNumber` your baseline hasn't seen. What's new in this version is **`changeReasonDescription`** — on a corrigendum notice, TED's own field explaining exactly what changed, e.g. *"Deadline for receipt of tenders: INSTEAD OF 24/08/2026 PLEASE READ 10/09/2026"* — and **`procedureIdentifier`**, a stable UUID shared by a notice and every corrigendum against it, so you can group them into one procurement thread instead of treating each as unrelated. Zero extra API calls: both fields ride along on the same page fetch every other field already uses.

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
| `deadlineDate`, `daysUntilDeadline`, `deadlineType` | Earliest submission deadline across all lots, how many whole days are left before it (negative = already closed, `null` = no deadline published), and which TED field the date came from: `tender` (the tender-receipt deadline — 48/50 live call-for-competition notices in a fresh measurement, see [the deadline-fields guide](https://fetchsmith.com/blog/eu-ted-deadline-lives-in-a-different-field)), `generic` (1/50), or `expressions` (the expressions-of-interest deadline on two-stage procedures, 0/50). Result/award notices (`can-standard`) carry none of the three fields — 0/50 in the same measurement — which is why `onlyOpenDeadlines` treats "no deadline published" as closed. |
| `deadlineReceiptRequestDate` | The separate tender-documents/information-request deadline, where TED publishes one. |
| `publicationDate` | When TED published the notice. |
| `noticeUrl` | Link to the notice's PDF (or XML) on ted.europa.eu, in your chosen language when available. Kept for backward compatibility — prefer the three fields below for a specific format. |
| `pdfUrl`, `htmlUrl`, `xmlUrl` | The same notice as a downloadable PDF, a browsable HTML page, and machine-readable XML, each in your chosen language when available. `null` for a format TED doesn't publish for that notice. |
| `procedureIdentifier` | A stable UUID shared by a notice and every corrigendum published against it — group them into one procurement thread. |
| `changeReasonDescription` | TED's own plain-text explanation of what changed. Only present on corrigendum notices; `null` on an original notice. |

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
  "deadlineType": "tender",
  "daysUntilDeadline": 12,
  "deadlineReceiptRequestDate": "2026-09-29",
  "publicationDate": "2026-08-31",
  "noticeUrl": "https://ted.europa.eu/en/notice/596425-2026/pdf",
  "pdfUrl": "https://ted.europa.eu/en/notice/596425-2026/pdf",
  "htmlUrl": "https://ted.europa.eu/en/notice/-/detail/596425-2026",
  "xmlUrl": "https://ted.europa.eu/en/notice/596425-2026/xml",
  "procedureIdentifier": "8041f035-c752-48c6-8772-62de0a83aa8b",
  "changeReasonDescription": null
}
```

`totalValue` is `null` here because this particular notice type doesn't carry one — see the FAQ. `daysUntilDeadline` is computed at run time (whole days, UTC), so the same notice returns a smaller number each day and goes negative once it closes. `changeReasonDescription` is `null` because this is an original notice, not a corrigendum; on a corrigendum it reads like *"Deadline for receipt of tenders: INSTEAD OF 24/08/2026 16:00 +02:00 PLEASE READ 10/09/2026 16:00 +02:00"*.

## Pricing
`result` — $0.003 per returned notice. The run start is free, no minimum spend.

## FAQ
**Why not just call the TED API myself?** You can — it's free and public. What you get here is normalization: TED's raw fields are multilingual maps and duplicated per-lot arrays, which are painful to consume directly. This Actor gives you one flat row per notice with an English-preferred title, a deduplicated CPV list and a single deadline date.

**Does this cover contract value?** Yes, when TED has it (`totalValue`/`totalValueCurrency`) — not every notice type carries a value (e.g. prior-information notices often don't). Use `minValue`/`maxValue` to filter on it directly instead of filtering the output yourself; notices with no value are dropped whenever either is set.

**Can I filter by procedure type (open vs. restricted vs. negotiated)?** Yes — set `procedureType` to any TED procedure-type codes (e.g. `open`, `restricted`, `neg-w-call`). It's a server-side filter sent straight to TED alongside `noticeTypes`/`cpvCodes`/`countries`, so it doesn't cost extra requests. About 90% of notices carry this field in a recent live sample; the rest have no procedure-type recorded by TED and are excluded from any `procedureType` match the same way an unset value would exclude them from any other filter.

**Can I search full text?** Yes — set `keywords` (e.g. `"cloud hosting"`), which is sent as TED's `FT~` full-text operator against title/description/buyer name. For anything beyond that, `expertQuery` gives raw access to TED's expert-search syntax.

**Can I pull a specific historical month or quarter, not just "the last N days"?** Yes — set `publicationDateFrom`/`publicationDateTo` (either or both) to an absolute `YYYYMMDD` window; it overrides `publishedWithinDays`.

**Can I get titles/descriptions in a language other than English?** Yes — set `outputLanguage` to any of 24 EU language codes (e.g. `deu`, `fra`, `spa`, `pol`). TED publishes every notice in every EU language, so this returns the same notice in your chosen language instead of English, including a matching-language notice URL. Notices without a translation into that language fall back to English automatically.

**How do multiple filters combine — AND or OR?** Values within the same field are OR'd (`countries: ["DEU", "FRA"]` matches either), and different fields are AND'd (country + CPV code together narrows, doesn't widen). Set `expertQuery` if you need anything more precise than that — it replaces all the filters above with TED's own raw expert-search syntax.

**Is `buyerEmail`/`buyerPhone` a personal contact?** No — these are the contracting authority's own published contact point for the procedure (`organisation-email-buyer`/`organisation-tel-buyer` in TED's schema), republished verbatim from an official EU government source. Most are role mailboxes (`vergabestelle@…`, `einkauf@…`); we don't enrich or cross-reference them.

**Why did my first `watchLabel` run return nothing?** By design — the first run on a new label + filter combination is a baseline: it records everything currently matching so the *next* run can tell you what's new, and charges nothing.

**Can I reset or inspect a watch baseline?** Yes. It is a plain JSON record in the `fetchsmith-ted-watch` key-value store on your own account, keyed by your label plus a fingerprint of your filters. Delete the record to start over, or read `seenIds` to see exactly what has been delivered.

**A tender I'm tracking got its deadline extended — will `watchLabel` catch that?** Yes, but as a new row, not an edited one: TED publishes the extension as a corrigendum with its own `publicationNumber`, so on your next watch run it arrives as a genuinely new notice. Match it back to the original via `procedureIdentifier` (both share it), and read `changeReasonDescription` for TED's own explanation of exactly what changed — no need to diff the two rows yourself.

**Why do my results carry CPV codes I never asked for — and sometimes not the one I did?** Because TED's `classification-cpv` filter matches the whole CPV *subtree* beneath the code you supply, at every level of the hierarchy, and a notice is usually tagged with several codes. There is no exact-code mode in TED's API, so there isn't one here either. Measured live on 2026-09-21 (publication window 2025-03-01..2025-03-31, 10 notices each): `cpvCodes: ["72000000"]` returned 10/10 notices carrying at least one `72…` code but only **5/10** carrying the literal `72000000` (the rest were tagged `72313000`, `72220000`, `72200000`, `72262000`); `cpvCodes: ["72220000"]` returned only **5/10** with the literal code (others: `72222100`, `72222300`, `72224000`); and even the narrow-looking `cpvCodes: ["72267000"]` returned only **6/10** with the literal code, because its children `72267100`/`72267200` match too. Picking a longer code narrows the subtree but never collapses it to a single code — a code only matches exactly when the CPV hierarchy gives it no children at all, and you can't tell which those are from the code alone. **Workaround:** filter the `cpvCodes` output array yourself after the run (e.g. keep rows where `cpvCodes` contains your exact code), or use `expertQuery` if you need TED's raw syntax.

**Can the same notice be returned — and charged — twice in one run?** No. TED is paged by page number over a live index and its search endpoint takes no sort parameter, so a notice published while a walk is in progress shifts later rows onto a page that was already read, and TED then serves the same `publication-number` on two pages. Every repeat is dropped before it is normalized, pushed or charged, so you pay for each notice exactly once; the run log names the count when it happens (`N notice(s) were served more than once by TED's own paging`) and the `webhookUrl` payload carries it as `duplicateRowsDropped`. Measured live on 2026-09-22 — 2,000 rows over 8 pages of a 4,486-match query, 0 repeats — so on short walks this is rare; the guard exists because the rate depends on how busy TED is while your run is walking, and a silent double charge is not something you should have to audit for yourself.

**I'm exporting to Excel/CSV and the CPV codes column looks broken.** That's Apify's default array export splitting `cpvCodes` (and the 3 other array fields) into numbered columns like `cpvCodes/0`, `cpvCodes/1` that shift position between rows with different counts. Set `flatten: true` and re-run — those 4 fields become a single comma-separated string column instead.

**Why are `deadlineReceiptRequestDate`/`changeReasonDescription` null on most rows?** Both are gated by notice type, not a bug or a filter you're missing. Measured directly against TED's own API (250-notice live sample, last 30 days, all countries): `deadline-receipt-request-date-lot` fills on **8.3% of `cn-standard`** (open contract notices — TED lets a buyer publish a separate request-to-participate deadline distinct from the tender deadline, but most don't) and **0% of `can-standard`** (award notices — the tender window is already closed, there's nothing left to request). `change-reason-description` fills on **20% of `cn-standard`** (a contract notice with a live corrigendum against it) and **~0-1% of `can-standard`/`can-modif`**. Neither field is meaningful on an award notice; if you want them populated, filter `noticeTypes: ["cn-standard"]`.

**How is `webhookUrl` different from Apify's own platform webhooks?**
Apify's platform webhooks are configured separately per Task/Actor via the Console or the Webhooks API — useful if you already live in the Apify Console, but extra setup if you're calling this Actor's API directly and just want a completion ping. `webhookUrl` is a plain input field: set it on the run itself and it POSTs a JSON body (`actorRunId`, `defaultDatasetId`, `finishedAt`, `pushed`, `pagesScanned`, `duplicateRowsDropped`, `totalNoticeCount`, and — if `watchLabel` is set — `watchSeeding`/`watchNewCount`/`baselineTruncated`/`baselineTruncatedTotal`) once the run finishes and every row is already pushed and charged. It's best-effort — a slow or failing webhook only logs a warning, it never fails the run, changes the result set, or affects billing.

## Notes
Only public data from an official EU government API is collected — no ToS or anti-bot risk. Issues or feature requests: support@fetchsmith.com. Also available as a hosted API at https://fetchsmith.com

Source code: https://github.com/Fetchsmith/fetchsmith/tree/main/actors/eu-ted-tenders-scraper

## Related guides
Engineering write-ups behind this Actor:
- [The EU publishes every public contract as JSON — in 24 languages, with the CPV code repeated eight times](https://fetchsmith.com/blog/eu-ted-tenders-public-json-api)
- [The EU's tender deadline isn't in the field called "deadline" — 48/50 live in a different one](https://fetchsmith.com/blog/eu-ted-deadline-lives-in-a-different-field) — which of TED's three deadline fields to trust, measured by notice type.
- [Eight ways an "only new since last run" watch mode silently stops working](https://fetchsmith.com/blog/incremental-api-watch-mode-four-traps) — how `watchLabel` is built and the traps it has to avoid.
- [We nearly charged our own buyers twice for rows they'd already paid for](https://fetchsmith.com/blog/watch-baseline-eviction-rebilling) — a capped watch-mode baseline can silently evict old-but-current ids on a high-volume run, re-delivering (and re-billing) rows already paid for. Reproduced on this Actor, closed with truncation tracking.

More tools: [fetchsmith.com/tools](https://fetchsmith.com/tools)
