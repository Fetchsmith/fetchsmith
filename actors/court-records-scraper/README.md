# Court Records & Case Law Scraper — Dockets + Opinions

Search **US federal court dockets** (the PACER/RECAP mirror) and **published court opinions** through CourtListener's public API and get flat, sortable JSON/CSV/Excel rows back.

**No API key. No registration. No captcha.** The search index this Actor is built on is fully anonymous — many CourtListener wrappers assume a token is required, because the `/dockets/` and `/opinions/` *detail* endpoints do need one. The *search* index does not, so nothing here depends on you creating an account. (Verified live 2026-09-17.)

**$0.002 per result, no run-start fee.** You pay for rows you actually receive and nothing else.

## What you get

Two CourtListener indexes, one unified table:

- **Dockets (`recordType: "dockets"`)** — the RECAP archive, a free mirror of federal PACER dockets. Parties, attorneys, law firms, assigned and referred judges, nature of suit, cause of action, jurisdiction type, jury demand, bankruptcy chapter, PACER case ID, and per-filing entries (description, date filed, page count, whether the PDF is actually available, a **direct PDF link** and the **OCR'd text of the filing** where RECAP has it).
- **Opinions (`recordType: "opinions"`)** — published decisions. Reported citations, cite count (how many later opinions cite this one), authoring judge, status, opinion snippet and the download URL where CourtListener has the document. Editorial extras — `syllabus`, `posture`, `proceduralHistory`, `panelNames`, `neutralCite`, `lexisCite` — are emitted when the court publishes them, which is a minority of rows; see **Honest limitations** for measured rates before you build on them.
- **`recordType: "both"`** returns both in one run, in one schema, with type-specific fields left `null` rather than omitted — so a CSV export has stable columns.

Search is full text across case names, party and attorney names, docket text and opinion bodies, with quoted phrases (`"fair use"`) and boolean operators (`AND`, `OR`, `NOT`).

## Input

| Field | Type | Description |
|---|---|---|
| `query` | string | Full-text query. Default `"patent infringement"`. Leave empty to browse by filters alone. |
| `recordType` | enum | `both` (default), `opinions`, or `dockets`. |
| `courts` | array | CourtListener court IDs — the slug in a `courtlistener.com/court/<id>/` URL: `scotus`, `ca9`, `cand`, `nysd`, `cacb`, … 400+ federal and state courts. Empty = all courts. |
| `partyName` | string | RECAP dockets only. Server-side search over the parties on a docket. Quote for an exact name (`"Google LLC"`), combine with `OR` for several. |
| `attorneyName` | string | RECAP dockets only. Server-side search over the attorneys of record. Same quoting/`OR` rules. |
| `docketNumber` | string | Case-number lookup, e.g. `1:20-cv-03590`. Real field search on **both** indexes, not full text. |
| `judge` | string | Opinions only. Server-side search over the authoring judge(s), e.g. `Posner`. |
| `filedAfter` / `filedBefore` | string | `YYYY-MM-DD` filing-date bounds. |
| `opinionStatus` | enum | Opinions mode only. `published` (default), `unpublished`, or `any`. See below — the default silently excludes a real chunk of matches unless you know to change it. |
| `sortBy` | enum | `relevance` (default), `dateFiledDesc`, or `dateFiledAsc`. Real server-side sort, verified live — see below. |
| `startUrl` | string | Paste a courtlistener.com search or API URL instead of filling in the fields above — see below. |
| `maxResults` | integer | Default 100. With `both`, the budget is split evenly between the two indexes, and whatever one index leaves unused goes to the other. |
| `watchLabel` | string | Incremental mode — see below. |
| `webhookUrl` | string | Optional. POST a small JSON completion summary (records pushed, rows scanned, pages, CourtListener's reported total, dataset ID) here when the run finishes — see FAQ. |

### Paste a CourtListener search URL

Already built the search on courtlistener.com? Paste the address bar into `startUrl` instead of re-entering the filters — e.g. `https://www.courtlistener.com/?q=patent&type=r&court=cand&filed_after=2024-01-01`. An API URL (`https://www.courtlistener.com/api/rest/v4/search/?q=patent&type=o`) works too; both use the identical `q`/`type`/`court`/`filed_after`/`filed_before`/`party_name`/`atty_name`/`docket_number`/`judge` parameters. Whatever the URL mentions replaces the matching field above; anything it doesn't mention still comes from the fields above, and `maxResults`/`watchLabel` always apply. Only Opinions (`type=o`) and RECAP (`type=r`) URLs are supported — CourtListener's Oral Arguments, Judges and Parenthetical searches are different record shapes this schema doesn't cover, and a URL for one of those logs a warning and falls back to the `recordType` field instead.

### Search by party, attorney, docket number or judge

`query` is full text over case bodies and metadata; these four are **field** searches, which is a different and much sharper thing — "every case where Google LLC is a party" is a question full text answers badly (it also matches every opinion that merely cites Google) and a party search answers exactly. All four are applied server-side, so you are never charged for rows that get filtered out afterwards.

They are not interchangeable across the two indexes, and this matters:

- `partyName` and `attorneyName` exist only on **RECAP dockets**. The opinion index carries no party or attorney data.
- `judge` exists only on **opinions**. RECAP dockets record an assigned judge but the index doesn't search on it.
- `docketNumber` works on both.

CourtListener doesn't reject a field the index can't honour — it ignores it. A `type=o&party_name=…` search therefore returns the *entire* opinion corpus rather than an error. So when you set a docket-only filter with `recordType: "both"`, this Actor drops the opinion half of the run (and says so in the log) instead of sending the filter blind and billing you for 8 million unfiltered rows; `judge` does the same in reverse. Setting a filter against the one index it can't work on (`partyName` with `recordType: "opinions"`) is an upfront error, as is combining `partyName`/`attorneyName` with `judge` — no single index carries both, so that search can never match anything.

If a `docketNumber` returns nothing, try it without the office prefix (`20-cv-03590` rather than `1:20-cv-03590`) — the format varies by court.

### Opinion status: the default hides ~1 in 4 real matches

CourtListener's opinion index defaults to **published** opinions unless you say otherwise — verified live: a 2024+ "climate" query returned 545 published opinions, 191 unpublished, and the true total (736) only when both are requested. That's roughly 26% of real matches silently absent from a plain search, with no indication in the response that anything was left out. Set `opinionStatus` to `"any"` to get the complete set, or `"unpublished"` to see only opinions courts didn't designate for publication (often the more interesting ones — sanctions orders, informal rulings, unusual fact patterns). Ignored (with a warning) when `recordType` is `"dockets"`, since RECAP dockets have no publication-status concept. Every opinion row already carries a `status` field either way, so you can always tell which bucket a row came from.

### Sort by filing date

`sortBy` defaults to relevance, the same order a plain search has always returned. Set it to `dateFiledDesc` or `dateFiledAsc` to sort by filing date instead — a real server-side sort verified live (identical total match count either way, just reordered). It's restricted to filing date because that's the one sort field confirmed to behave correctly on **both** indexes; CourtListener's citation-count sort is opinions-only and returns a server error when sent to the docket index. With `recordType: "both"`, each index is sorted on its own — opinions (sorted) up to their share of `maxResults`, then dockets (sorted) — not merged into one table sorted end to end. Avoid `dateFiledAsc` together with `watchLabel`: an incremental run walks from the oldest match forward, so on an established watch label it may page through a long run of already-delivered records before reaching anything new. `dateFiledDesc` or the default relevance sort don't have that problem.

### Incremental "watch" mode

Set `watchLabel` to any name and schedule the Actor. The **first** run on that label records the current match set as a baseline, returns **zero** results and charges you **nothing**. Every run after that returns only records that appeared since — so a daily watch on `court: ["cand"], query: "trade secret"` costs you a couple of rows a day instead of the whole back catalogue every morning. Changing any filter starts a fresh baseline under the same label, so you never get flooded with rows an older, narrower filter had excluded. `sortBy` does not affect the baseline — it reorders the same matches, it never changes which records match, so switching it doesn't start a fresh baseline.

### Webhook notification on completion

Set `webhookUrl` to an http(s) URL and this Actor POSTs a small JSON summary there when the run finishes — `actorRunId`, `defaultDatasetId`, `finishedAt`, `pushed`, `scanned`, `pages`, `totalReported`, and — if `watchLabel` is set — `watchSeeding`/`watchNewCount`. This is a plain input field, not an Apify platform webhook (those are configured separately per Task/Actor via the Console or Webhooks API) — set it on the run itself for a quick completion ping without extra setup. It's best-effort: a failed or slow webhook only logs a warning, fired after every record is already pushed and charged, so it never affects the result set or your bill.

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
    { "documentId": 479225638, "entryNumber": 90, "description": "Order", "entryDateFiled": "2026-08-10", "pageCount": 8, "isAvailable": true, "textSnippet": "Case 1:12-cv-00854-LPS Document 13 Filed 07/07/14 Page 1 of 6 PageID #: 573\n\nIN THE UNITED STATES DISTRICT COURT…", "pdfUrl": "https://storage.courtlistener.com/recap/gov.uscourts.ded.49136/gov.uscourts.ded.49136.13.0.pdf", "url": "https://www.courtlistener.com/docket/…" }
  ],
  "downloadUrl": "https://storage.courtlistener.com/recap/gov.uscourts.ded.49136/gov.uscourts.ded.49136.13.0.pdf",
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
- **Docket analytics** — nature-of-suit and cause-of-action distributions by court and year, from `suitNature`, `cause` and `jurisdictionType` (all three are docket-row fields; run with `recordType: "dockets"`).

## Honest limitations

- **RECAP is a mirror of PACER, not PACER.** It holds what its contributors have purchased and donated, so coverage is deep in heavily-litigated districts and thin elsewhere. It is free; PACER is not.
- **`documents[].isAvailable` is often false.** CourtListener frequently has a docket *entry* without the PDF behind it — 30 of 72 filing entries were available in a live N.D. Cal. sample (2026-09-17). Check the flag rather than assuming every row comes with a downloadable document.
- **`documents[].textSnippet` is an excerpt, not the whole filing.** CourtListener's search index returns roughly the first 500 characters of a document's OCR'd text, and only for documents where `isAvailable` is true. The *complete* plain text sits behind the token-gated `/api/rest/v4/recap-documents/` endpoint (anonymous requests get `401`); this Actor needs no key, so it gives you the excerpt plus `pdfUrl` — the PDF bucket at `storage.courtlistener.com` is public and needs no token either, so you can fetch and parse the full document yourself.
- **Several opinion fields are sparse, and how sparse depends on the court.** CourtListener's search index returns these fields for every opinion row, but the value is empty unless the publishing court supplied it. Measured over 240 live opinion rows across 12 court/date slices (2026-09-19): `neutralCite` **25%**, `judge` **16%**, `syllabus` **12%**, `panelNames` **4%**, `lexisCite` **2%**, `proceduralHistory` **<1%**, `posture` **0%**. The distribution is strongly court-dependent rather than random — Ohio and Illinois appellate rows carried `syllabus`/`neutralCite` on **20/20**, while `ca9`, `ca2`, `ny` and `scotus` carried none. If your pipeline needs one of these, filter `courts` to a court that publishes it and check a small run first. Nothing is dropped or charged differently because a field is empty — you always pay $0.002 per row returned.
- **`jurisdictionType` is a docket field.** On docket rows it is PACER's readable text (`"Diversity"`, `"Federal Question"`). On opinion rows it carries CourtListener's raw one-letter court code (`"F"`) and is null on ~91% of rows — use it for docket analytics, not opinion analytics.
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
