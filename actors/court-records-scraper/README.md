# Court Records & Case Law Scraper — Dockets + Opinions

Search **US federal court dockets** (the PACER/RECAP mirror) and **published court opinions** through CourtListener's public API and get flat, sortable JSON/CSV/Excel rows back.

**No API key. No registration. No captcha.** The search index this Actor is built on is fully anonymous — many CourtListener wrappers assume a token is required, because the `/dockets/` and `/opinions/` *detail* endpoints do need one. The *search* index does not, so nothing here depends on you creating an account. (Verified live 2026-09-17.)

**$0.002 per result, no run-start fee.** You pay for rows you actually receive and nothing else.

## What you get

Two CourtListener indexes, one unified table:

- **Dockets (`recordType: "dockets"`)** — the RECAP archive, a free mirror of federal PACER dockets. Parties, attorneys, law firms, assigned and referred judges, nature of suit, cause of action, jurisdiction type, jury demand, bankruptcy chapter, PACER case ID, and per-filing entries (description, date filed, page count, and whether the PDF is actually available).
- **Opinions (`recordType: "opinions"`)** — published decisions. Reported citations, cite count (how many later opinions cite this one), judge and panel, status, posture, procedural history, syllabus, opinion snippet and the download URL where CourtListener has the document.
- **`recordType: "both"`** returns both in one run, in one schema, with type-specific fields left `null` rather than omitted — so a CSV export has stable columns.

Search is full text across case names, party and attorney names, docket text and opinion bodies, with quoted phrases (`"fair use"`) and boolean operators (`AND`, `OR`, `NOT`).

## Input

| Field | Type | Description |
|---|---|---|
| `query` | string | Full-text query. Default `"patent infringement"`. Leave empty to browse by filters alone. |
| `recordType` | enum | `both` (default), `opinions`, or `dockets`. |
| `courts` | array | CourtListener court IDs — the slug in a `courtlistener.com/court/<id>/` URL: `scotus`, `ca9`, `cand`, `nysd`, `cacb`, … 400+ federal and state courts. Empty = all courts. |
| `filedAfter` / `filedBefore` | string | `YYYY-MM-DD` filing-date bounds. |
| `startUrl` | string | Paste a courtlistener.com search or API URL instead of filling in the fields above — see below. |
| `maxResults` | integer | Default 100. With `both`, the budget is split evenly between the two indexes, and whatever one index leaves unused goes to the other. |
| `watchLabel` | string | Incremental mode — see below. |

### Paste a CourtListener search URL

Already built the search on courtlistener.com? Paste the address bar into `startUrl` instead of re-entering the filters — e.g. `https://www.courtlistener.com/?q=patent&type=r&court=cand&filed_after=2024-01-01`. An API URL (`https://www.courtlistener.com/api/rest/v4/search/?q=patent&type=o`) works too; both use the identical `q`/`type`/`court`/`filed_after`/`filed_before` parameters. Whatever the URL mentions replaces the matching field above; anything it doesn't mention still comes from the fields above, and `maxResults`/`watchLabel` always apply. Only Opinions (`type=o`) and RECAP (`type=r`) URLs are supported — CourtListener's Oral Arguments, Judges and Parenthetical searches are different record shapes this schema doesn't cover, and a URL for one of those logs a warning and falls back to the `recordType` field instead.

### Incremental "watch" mode

Set `watchLabel` to any name and schedule the Actor. The **first** run on that label records the current match set as a baseline, returns **zero** results and charges you **nothing**. Every run after that returns only records that appeared since — so a daily watch on `court: ["cand"], query: "trade secret"` costs you a couple of rows a day instead of the whole back catalogue every morning. Changing any filter starts a fresh baseline under the same label, so you never get flooded with rows an older, narrower filter had excluded.

## Sample row (docket)

```json
{
  "recordType": "docket",
  "id": "r-68922376",
  "caseName": "Gen Digital, Inc. v. Sycomp, a Technology Company, Inc.",
  "court": "District Court, N.D. California",
  "courtId": "cand",
  "docketNumber": "3:24-cv-04106",
  "dateFiled": "2024-07-08",
  "judge": "Charles R. Breyer",
  "parties": ["North American Systems International, Inc.", "Gen Digital, Inc.", "Sycomp, a Technology Company, Inc."],
  "attorneys": ["Craig J. Mariam", "Anthony David Phillips", "Michael William Stebbins"],
  "firms": ["Gordon and Rees Scully Mansukhani", "Maslon LLP", "Carr McClellan P.C.", "Fox Rothschild LLP"],
  "suitNature": "190 Contract: Other",
  "cause": "28:1332 Diversity-Breach of Contract",
  "jurisdictionType": "Diversity",
  "juryDemand": "None",
  "pacerCaseId": "…",
  "documentCount": 3,
  "documents": [
    { "entryNumber": 90, "description": "Order", "entryDateFiled": "2026-08-10", "pageCount": 8, "isAvailable": true, "url": "https://www.courtlistener.com/docket/…" }
  ],
  "url": "https://www.courtlistener.com/docket/68922376/…"
}
```

## Sample row (opinion)

```json
{
  "recordType": "opinion",
  "id": "o-8493216",
  "caseName": "Phillips v. Mike Murdock Evangelistic Ass'n",
  "court": "Court of Appeals for the Ninth Circuit",
  "courtId": "ca9",
  "docketNumber": "No. 08-16925",
  "dateFiled": "2009-07-28",
  "citations": ["329 F. App'x 775"],
  "citeCount": 0,
  "judge": "Schroeder, Thomas, Wardlaw",
  "status": "Published",
  "snippet": "MEMORANDUM ** Cherie Phillips, author of the Wisdom Bible of God, appeals pro se from the district court's judgment in her trademark infringement action…",
  "opinionCount": 1,
  "url": "https://www.courtlistener.com/opinion/8493216/…"
}
```

All 39 fields are listed with types and examples in the **Output schema** tab.

## Use cases

- **Competitive and IP monitoring** — watch every new patent, trademark or trade-secret docket in the districts your industry litigates in, and get alerted the day one is filed.
- **Law-firm business development** — pull the firms and attorneys appearing opposite a target client, by court and nature of suit.
- **Bankruptcy and credit risk** — filter `recordType: "dockets"` on a bankruptcy court (`cacb`, `nysb`, `deb`) and read `chapter`, `dateFiled` and `dateTerminated` straight off the row.
- **Legal research pipelines** — pull opinions by query and court, sort by `citeCount` to find the load-bearing precedents, and follow `downloadUrl` for the full text.
- **Docket analytics** — nature-of-suit and cause-of-action distributions by court and year, from `suitNature`, `cause` and `jurisdictionType`.

## Honest limitations

- **RECAP is a mirror of PACER, not PACER.** It holds what its contributors have purchased and donated, so coverage is deep in heavily-litigated districts and thin elsewhere. It is free; PACER is not.
- **`documents[].isAvailable` is often false.** CourtListener frequently has a docket *entry* without the PDF behind it — 30 of 72 filing entries were available in a live N.D. Cal. sample (2026-09-17). Check the flag rather than assuming every row comes with a downloadable document.
- **Dockets and opinions are separate indexes.** A case present in one is often absent from the other; use `both` when unsure.
- The query is a **full-text search**, not a case-number lookup. For a docket number, put it in `query` as-is and widen the court filter.

## Pricing

`$0.002` per result, **no run-start fee**. 1,000 records costs $2.00.

For comparison, as of **2026-09-17**: `nexgendata/court-records-search` charges a flat **$0.10 per result** (raised from $0.002 on 2026-07-17) — 50× this Actor. `automation-lab/court-records-scraper` charges a **$0.005 run-start fee plus $0.0023/record** on the free tier, tapering to $0.00056 on Diamond; cheaper per record at very high volume on a paid Apify plan, more expensive for the small and mid-size runs most buyers actually make, and it bills you before it returns a single row. *(Competitor pricing verified 2026-09-17.)*

## Data source, legality and privacy

Data comes from [CourtListener](https://www.courtlistener.com/) / the [Free Law Project](https://free.law/), a non-profit that publishes US court records as open data, via its documented public REST API. No login is used, no paywall is bypassed, and no page is scraped behind authentication.

Every name in the output — parties, attorneys, law firms, judges — appears on a **public court record** and is a professional or institutional participant in a public proceeding. The API returns no email addresses and no phone numbers, and this Actor adds none.

## Source code

<https://github.com/Fetchsmith/fetchsmith/tree/main/actors/court-records-scraper>

## Related guides

- [CourtListener's court-records API needs no key — except for the one endpoint most wrapper docs point you at first](https://fetchsmith.com/blog/courtlistener-search-api-two-auth-tiers)
- [All FetchSmith tools and APIs](https://fetchsmith.com/tools)
