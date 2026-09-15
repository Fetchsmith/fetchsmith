# Federal Register Scraper – Agency, Type & Comment Deadlines

Pulls US **Federal Register** documents — final rules, proposed rules, notices and presidential documents — from the Federal Register's own official public API (federalregister.gov, run by NARA and the GPO) and returns them as one flat, typed dataset.

No API key, no login, no proxy. Public government data only.

## What you get

30 flat fields per document, including the ones most Federal Register Actors leave out:

| Field | Why it matters |
| --- | --- |
| `commentsCloseOn` | The public-comment deadline — **when you have to act by**. Present on 92% of proposed rules and about a third of notices (measured on a live 200-row sample per type). |
| `significant` | The Executive Order 12866 "significant rule" flag. Set on final and proposed rules only (~40% of them); always null on notices and presidential documents. |
| `regulationIdNumbers` | RIN — joins a document to its entry in reginfo.gov's Unified Agenda. |
| `docketIds` | Regulations.gov docket IDs, so you can pull the comment file. |
| `cfrReferences` | Flattened to readable strings like `40 CFR 257`. |
| `agencyNames` / `agencySlugs` / `parentAgencyNames` | One document usually lists a department *and* the bureau that wrote it; both are kept, split by level. |
| `fullTextUrl` | Public URL of the complete document body as plain text. Free to fetch yourself — we don't charge you a second row for it. |
| `url`, `pdfUrl`, `citation`, `startPage`, `endPage`, `pageLength` | Cite it in a memo without a second lookup. |

Plus `documentNumber`, `type`, `subtype`, `title`, `abstract`, `action`, `datesText`, `publicationDate`, `effectiveOn`, `signingDate`, `topics`, `president`, `executiveOrderNumber`, `excerpt`, `jsonUrl`.

## Who uses this

- **Regulatory-affairs and compliance teams** tracking every rule touching their sector, with the comment deadline attached.
- **Trade and customs consultancies** watching tariff, AD/CVD and export-control notices.
- **Law firms and lobbyists** monitoring a docket or RIN from proposed rule to final rule.
- **Industry associations** building a weekly "what changed" digest for members.

## Input

```json
{
  "documentTypes": ["RULE", "PRORULE"],
  "agencies": ["Environmental Protection Agency"],
  "commentsOpenOnly": true,
  "maxResults": 100
}
```

| Input | Notes |
| --- | --- |
| `documentTypes` | `RULE`, `PRORULE`, `NOTICE`, `PRESDOCU`. All four by default. |
| `agencies` | Slug (`environmental-protection-agency`) **or** full name — both are resolved against the official 472-agency list, and anything unrecognised is reported in the log instead of silently returning zero rows. **Filtering by a parent agency includes its sub-agencies**: `homeland-security-department` also returns Coast Guard, FEMA, CBP, TSA and USCIS documents. |
| `publicationDateFrom` / `publicationDateTo` | `YYYY-MM-DD`. Defaults to the last 90 days; the archive goes back to **1994-01-03**. |
| `searchQuery` | Full-text search across title and body. |
| `significantOnly` | EO 12866 significant rules only. |
| `commentsOpenOnly` | Only documents whose comment period closes today or later. |
| `cfrTitle` / `cfrPart` | Filter to documents affecting a specific Code of Federal Regulations title (1-50) and, optionally, a part within it (e.g. title `40`, part `60` = 40 CFR Part 60, New Source Performance Standards). Verified live: a single title alone narrows the 10,000-clamped baseline to a few hundred/year; adding a part narrows further into the dozens. `cfrPart` requires `cfrTitle` — the API has no title-less part lookup and 400s on one, so this Actor fails loudly client-side instead. |
| `order` | `newest`, `oldest` or `relevance`. |
| `maxResults` | Up to 50,000. |
| `watchLabel` | Optional. Name a saved query and get **only what is new since your last run** — see below. |

## Only what's new since last run (`watchLabel`)

A rule-watching job is a *subscription*, not a search: you want the documents published since you last looked, not the same 400 rows re-delivered (and re-charged) every morning.

Set `watchLabel` to a name for the query — `epa-air-rules`, say — and this Actor keeps track of which documents it has already given you under that name:

- **The first run on a new label is a free baseline.** It records what already matches, returns **zero** results and charges **nothing**. It walks ids only, not full documents.
- **Every run after that returns only the new documents.** Already-delivered rows are dropped before they are built or billed, so you never pay for the same document twice.
- **A document counts as delivered only once it has actually been charged.** Anything cut off by `maxResults` or a charge limit stays "new" for the next run rather than vanishing.
- **Changing a filter starts a fresh baseline** — a different filter is a different question, so you don't get a dump of everything the old, narrower query happened to exclude.
- **The rolling 90-day default date window is deliberately *not* part of that identity.** It moves every day; if it counted, a daily schedule would re-seed forever and never deliver anything. Dates you set *explicitly* do count.

The baseline lives in a key-value store named `fetchsmith-fedreg-watch` on your own account, so it survives between runs and you can inspect or reset it yourself. Point an Apify schedule at the Actor and you have a Federal Register alert.

## Sample output

```json
{
  "documentNumber": "2026-18552",
  "type": "Proposed Rule",
  "title": "Wisconsin: Approval of State Coal Combustion Residuals Permit Program",
  "publicationDate": "2026-09-11",
  "commentsCloseOn": "2026-11-10",
  "agencyNames": ["Environmental Protection Agency"],
  "docketIds": ["EPA-HQ-OLEM-2026-4324", "FRL-13374-01-OLEM"],
  "cfrReferences": ["40 CFR 257"],
  "citation": "91 FR 57842",
  "url": "https://www.federalregister.gov/documents/2026/09/11/2026-18552/wisconsin-approval-of-state-coal-combustion-residuals-permit-program",
  "fullTextUrl": "https://www.federalregister.gov/documents/full_text/text/2026/09/11/2026-18552.txt"
}
```

## No 10,000-row wall

The Federal Register API's page-based paging stops hard at 10,000 rows (`page=11` at `per_page=1000` is an HTTP 400), and its `count` field is clamped at 10,000 even when far more documents match. This Actor pages with the API's own `search_after_cursor` instead, which walks straight past that limit — verified by pulling 14,000 consecutive rows in one run. Set `maxResults` to what you actually want; you will not hit a hidden ceiling at 10,000.

## Pricing

**$0.0008 per result, no Actor-start fee** — the cheapest per-row price of any Federal Register Actor in the Store at the time of writing (the rest run $0.001–$0.005 per row, most with a start fee on top). 1,000 documents costs $0.80.

## FAQ

**Why did I get zero rows?**
The filters are ANDed. A `searchQuery` plus an agency plus `significantOnly` over a short date window often genuinely matches nothing — drop one filter. Also note `significantOnly` only ever matches rules and proposed rules, so pairing it with `documentTypes: ["NOTICE"]` always returns nothing. The run log spells out which cause applies.

**Is `significant` reliable?**
It is reliable where it exists — on final and proposed rules. It is `null` by design on notices and presidential documents, so don't read null as "not significant" outside rules.

**Does it fetch the full document text?**
No. Each row carries `fullTextUrl`, the public plain-text URL, so you fetch bodies only for the documents you care about instead of paying for text on every row.

**Is this legal?**
Yes. federalregister.gov publishes this API for public reuse, the content is US-government work in the public domain, and no row contains personal data.

**Why did my first `watchLabel` run return nothing?**
That is what a baseline run does: it records what already matches so that "new" means something, returns zero rows and charges you zero. The next run on the same label and filters returns only what has been published since.

**Can I reset or inspect a watch baseline?**
Yes. It is a plain JSON record in the `fetchsmith-fedreg-watch` key-value store on your own account, keyed by your label plus a fingerprint of the filters. Delete the record to start over, or read `seenIds` to see exactly what has been delivered.

## Related guides

- [The Federal Register API says it has 10,000 documents. It doesn't — and the fix is already in the response](https://fetchsmith.com/blog/federal-register-documents-json-api) — the full write-up of the clamped `count`, the 10,000-row offset wall and the `search_after_cursor` that walks past it, the per-document-type field-population table, and why a mistyped agency slug 400s the whole query.
- [The FDA publishes every product recall as JSON — but you can't page past row 25,000](https://fetchsmith.com/blog/fda-openfda-recall-json-api) — the same "US government publishes it as keyless JSON" pattern, with a pagination wall that has no cursor escape hatch.
- [All FetchSmith tools](https://fetchsmith.com/tools)
- [Source code](https://github.com/Fetchsmith/fetchsmith/tree/main/actors/federal-register-scraper)
