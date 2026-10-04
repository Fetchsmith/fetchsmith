# Court Records & Case Law Scraper — Dockets + Opinions

Search **US federal court dockets** (the PACER/RECAP mirror) and **published court opinions** through CourtListener's public API and get flat, sortable JSON/CSV/Excel rows back.

**No API key. No registration. No captcha.** The search index this Actor is built on is fully anonymous — many CourtListener wrappers assume a token is required, because the `/dockets/` and `/opinions/` *detail* endpoints do need one. The *search* index does not, so nothing here depends on you creating an account. (Verified live 2026-09-17.)

**$0.002 per result, no run-start fee.** You pay for rows you actually receive and nothing else.

## What you get

Two CourtListener indexes, one unified table:

- **Dockets (`recordType: "dockets"`)** — the RECAP archive, a free mirror of federal PACER dockets. Parties, attorneys, law firms, assigned and referred judges, nature of suit, cause of action, jurisdiction type, jury demand, bankruptcy chapter, PACER case ID, and per-filing entries (description, date filed, page count, whether the PDF is actually available, a **direct PDF link** and the **OCR'd text of the filing** where RECAP has it).
- **Opinions (`recordType: "opinions"`)** — published decisions. Reported citations, cite count (how many later opinions cite this one), authoring judge, status, opinion snippet and the download URL where CourtListener has the document. Editorial extras — `syllabus`, `proceduralHistory`, `panelNames`, `neutralCite`, `lexisCite` — are emitted when the court publishes them, which is a minority of rows; see **Honest limitations** for measured rates before you build on them.
- **Court jurisdiction on every row** — `courtJurisdiction` gives the court's tier as a readable label (`Federal District`, `Federal Appellate`, `Federal Bankruptcy`, `State Supreme`, `State Appellate`, `Tribal Appellate`, `Military Appellate`, ...) on **both** dockets and opinions, so you can group or filter federal vs. state vs. bankruptcy without keeping a court-code lookup table of your own.
- **`recordType: "both"`** returns both in one run, in one schema, with type-specific fields left `null` rather than omitted — so a CSV export has stable columns.

Search is full text across case names, party and attorney names, docket text and opinion bodies, with quoted phrases (`"fair use"`) and boolean operators (`AND`, `OR`, `NOT`).

## Input

| Field | Type | Description |
|---|---|---|
| `query` | string | Full-text query. Default `"patent infringement"`. Leave empty to browse by filters alone. |
| `recordType` | enum | `both` (default), `opinions`, or `dockets`. |
| `courts` | array | CourtListener court IDs — the slug in a `courtlistener.com/court/<id>/` URL: `scotus`, `ca9`, `cand`, `nysd`, `cacb`, … 3,359 federal, state and specialty courts. Empty = all courts. An ID CourtListener does not publish is not rejected upstream — it silently matches nothing — so the run log warns and names any unrecognised ID. |
| `partyName` | string | RECAP dockets only. Server-side search over the parties on a docket. Quote for an exact name (`"Google LLC"`), combine with `OR` for several. |
| `attorneyName` | string | RECAP dockets only. Server-side search over the attorneys of record. Same quoting/`OR` rules. |
| `docketNumber` | string | Case-number lookup, e.g. `1:20-cv-03590`. Real field search on **both** indexes, not full text. |
| `judge` | string | Opinions only. Server-side search over the authoring judge(s), e.g. `Posner`. |
| `filedAfter` / `filedBefore` | string | `YYYY-MM-DD` filing-date bounds, both **inclusive**. Strictly parsed — an unreadable date stops the run rather than being ignored. See below. |
| `opinionStatus` | enum | Opinions mode only. `published` (default), `unpublished`, or `any`. See below — the default silently excludes a real chunk of matches unless you know to change it. |
| `sortBy` | enum | `relevance` (default), `dateFiledDesc`, or `dateFiledAsc`. Real server-side sort, verified live — see below. |
| `startUrl` | string | Paste a courtlistener.com search or API URL instead of filling in the fields above — see below. |
| `maxResults` | integer | Default 100. With `both`, the budget is split evenly between the two indexes, and whatever one index leaves unused goes to the other. |
| `watchLabel` | string | Incremental mode — see below. |
| `watchChanges` | boolean | Only with `watchLabel`. Off by default. When on, a docket you already saw is re-delivered (and charged again) if its case is terminated since — see below. |
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

### Opinion status: the default hides a real, query-dependent chunk of matches

CourtListener's opinion index defaults to **published** opinions unless you say otherwise — verified live across 4 topic queries, the hidden share is **not a fixed number**: "patent infringement" 5.7%, "employment discrimination" 18.8%, "qualified immunity" 13.7%, "immigration" 37.2% of true matches missing from a plain search, with no indication in the response that anything was left out. Set `opinionStatus` to `"unpublished"` to see only opinions courts didn't designate for publication (often the more interesting ones — sanctions orders, informal rulings, unusual fact patterns), or `"any"` for the complete set.

**`"any"` means every real status, not just published + unpublished.** CourtListener's opinion `status` field has 5 more real values we found by testing each `stat_*` flag individually: `Errata`, `Separate`, `In-chambers`, `Relating-to`, and `Unknown`. The first four are small (0-27 matches each on "immigration"), but `Unknown` is not — 31,096 real, dated opinions (2023-2025 district-court rows, not placeholders) on that one query alone, ~17.7% on top of published+unpublished combined. `opinionStatus: "any"` now requests all 7 flags so it actually returns everything; earlier builds only requested published+unpublished. Ignored (with a warning) when `recordType` is `"dockets"`, since RECAP dockets have no publication-status concept. Every opinion row already carries a `status` field either way, so you can always tell which bucket a row came from.

### Filing dates: both bounds inclusive, and a bad date stops the run

`filedAfter` and `filedBefore` are both **inclusive**. Verified live against CourtListener: `filedAfter` and `filedBefore` both set to `2024-06-13` returns the 6 SCOTUS opinions filed that day, `2024-06-14` alone returns 9, and `2024-06-13 .. 2024-06-14` returns 15 — 6 + 9, so neither endpoint is dropped.

Write them as `YYYY-MM-DD`. `2024-6-5`, `2024/6/5`, `2024.06.05` and bare `20240605` are all accepted and normalized for you. **Anything else stops the run with an error** — it is not quietly ignored. That is deliberate, and it is the opposite of how `opinionStatus` behaves: a bad `opinionStatus` falls back to the default, which *narrows* your results, whereas a dropped date bound *widens* the search to the entire archive — back to the 1700s — and you would be charged for every one of those rows. This Actor used to do exactly that: `filedAfter: "2024-6-5"`, `filedBefore: "2024-6-9"` lost both filters and returned ten SCOTUS opinions filed between **1795 and 1831**, all billable, with nothing in the log to say the window had been discarded. Fixed in v0.1.20.

US-style `06/15/2024` is rejected on purpose rather than guessed at, because `06/15` and `15/06` cannot be told apart and guessing wrong would silently return the wrong quarter. Impossible calendar dates (`2024-06-31`, `2023-02-29`) are rejected here too, with a useful message — CourtListener itself answers them with a bare HTTP 400.

### Sort by filing date

`sortBy` defaults to relevance, the same order a plain search has always returned. Set it to `dateFiledDesc` or `dateFiledAsc` to sort by filing date instead — a real server-side sort verified live (identical total match count either way, just reordered). It's restricted to filing date because that's the one sort field confirmed to behave correctly on **both** indexes; CourtListener's citation-count sort is opinions-only and returns a server error when sent to the docket index. With `recordType: "both"`, each index is sorted on its own — opinions (sorted) up to their share of `maxResults`, then dockets (sorted) — not merged into one table sorted end to end. Avoid `dateFiledAsc` together with `watchLabel`: an incremental run walks from the oldest match forward, so on an established watch label it may page through a long run of already-delivered records before reaching anything new. `dateFiledDesc` or the default relevance sort don't have that problem.

### Incremental "watch" mode

Set `watchLabel` to any name and schedule the Actor. The **first** run on that label records the current match set as a baseline, returns **zero** results and charges you **nothing**. Every run after that returns only records that appeared since — so a daily watch on `court: ["cand"], query: "trade secret"` costs you a couple of rows a day instead of the whole back catalogue every morning. Changing any filter starts a fresh baseline under the same label, so you never get flooded with rows an older, narrower filter had excluded. `sortBy` does not affect the baseline — it reorders the same matches, it never changes which records match, so switching it doesn't start a fresh baseline.

**Baseline size cap.** A baseline holds up to **60,000** record ids in one saved record. If a label's baseline grows past that, the oldest-first-seen ids are dropped — and a dropped id is no longer recognised, so that opinion/docket comes back as "new" on a later run **and is charged again**. The run that drops them says so explicitly: a warning in the log, a note on the run's status message, and `baselineTruncated` / `baselineTruncatedTotal` (this run / the whole life of the label) in `RUN_SUMMARY`, on the `webhookUrl` payload and in the saved record. If you see it, narrow the watch query (a court, fewer `recordTypes`, a shorter filed-date window) or split it across several labels so each baseline stays under the cap. A baseline run also stops recording at 20,000 records, and already warns separately when it hits that.

**A docket's own id never changes when its case closes — set `watchChanges` to hear about that too.** By default, watch mode only ever tells you about brand-new records: a docket you were already delivered stays silent forever after, even the day the case is dismissed or a judgment issues, because CourtListener keeps the same `docket_id` for the life of the case. Set `watchChanges: true` and a docket whose `dateTerminated` moves from empty to a real date since you last saw it is re-delivered — charged again, same as a new row — tagged with `_watchChangeType: ["dateTerminated"]` and `_watchPrevious: { dateTerminated: null }` (or whatever the earlier value was) so you don't have to diff it against your own last-seen copy. Only dockets can fire this; opinions have no comparable field and are unaffected whether `watchChanges` is on or off. A baseline seeded before this option existed keeps working unchanged — it just starts tracking terminations from the run you first turn it on, not retroactively.

### Webhook notification on completion

Set `webhookUrl` to an http(s) URL and this Actor POSTs a small JSON summary there when the run finishes — `actorRunId`, `defaultDatasetId`, `finishedAt`, `pushed`, `scanned`, `pages`, `totalReported`, a `summary` object (identical to the `RUN_SUMMARY` record below), and — if `watchLabel` is set — `watchSeeding`/`watchNewCount`/`watchChangedCount`. This is a plain input field, not an Apify platform webhook (those are configured separately per Task/Actor via the Console or Webhooks API) — set it on the run itself for a quick completion ping without extra setup. It's best-effort: a failed or slow webhook only logs a warning, fired after every record is already pushed and charged, so it never affects the result set or your bill.

### Did this run get everything? Check `RUN_SUMMARY`

Every run writes a `RUN_SUMMARY` record to its key-value store (`GET /v2/actor-runs/<runId>/key-value-store/records/RUN_SUMMARY`) with a top-level `complete` boolean and, when `complete` is `false`, an `incompleteReason` (`max-results`, `charge-limit`, `seed-cap` or `source-error`). It also breaks the run down **per index** under `recordTypes.opinions`/`recordTypes.dockets`: `exhausted` is `true` only if that index was read all the way to the end of its matches — when it's `false`, a low `delivered` count for that index means "we don't know", not "the court had few matches". This matters because CourtListener's opinions and dockets indexes are walked independently: a mid-walk error on one (a 5xx, a timeout) does not stop the other, so a run can finish SUCCEEDED with rows from one index and total silence from the other unless you check `recordTypes.<kind>.failed`/`lastError`. A run that goes incomplete also sets the Actor's run status message, visible in the Apify Console without opening the key-value store.

## Sample row (docket)

```json
{
  "recordType": "docket",
  "id": "r-68922376",
  "caseName": "Gen Digital, Inc. v. Sycomp, a Technology Company, Inc.",
  "court": "District Court, N.D. California",
  "courtId": "cand",
  "courtJurisdiction": "Federal District",
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
  "courtJurisdiction": "Federal Appellate",
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

All 41 fields are listed with types and examples in the **Output schema** tab.

## Use cases

- **Competitive and IP monitoring** — watch every new patent, trademark or trade-secret docket in the districts your industry litigates in, and get alerted the day one is filed.
- **Law-firm business development** — pull the firms and attorneys appearing opposite a target client, by court and nature of suit.
- **Bankruptcy and credit risk** — filter `recordType: "dockets"` on a bankruptcy court (`cacb`, `nysb`, `deb`) and read `chapter`, `dateFiled` and `dateTerminated` straight off the row.
- **Legal research pipelines** — pull opinions by query and court, sort by `citeCount` to find the load-bearing precedents, and follow `downloadUrl` for the full text.
- **Docket analytics** — nature-of-suit and cause-of-action distributions by court and year, from `suitNature`, `cause` and `jurisdictionType` (all three are docket-only fields — they are `null` on opinion rows, so run with `recordType: "dockets"`). For splits that should span **both** record types — federal vs. state vs. bankruptcy caseload, or appellate-vs-trial mix — group on `courtJurisdiction` instead: it is populated on opinion and docket rows alike.

## Honest limitations

- **RECAP is a mirror of PACER, not PACER.** It holds what its contributors have purchased and donated, so coverage is deep in heavily-litigated districts and thin elsewhere. It is free; PACER is not.
- **`documents[].isAvailable` is often false.** CourtListener frequently has a docket *entry* without the PDF behind it — 30 of 72 filing entries were available in a live N.D. Cal. sample (2026-09-17). Check the flag rather than assuming every row comes with a downloadable document.
- **`documents[].textSnippet` is an excerpt, not the whole filing.** CourtListener's search index returns roughly the first 500 characters of a document's OCR'd text, and only for documents where `isAvailable` is true. The *complete* plain text sits behind the token-gated `/api/rest/v4/recap-documents/` endpoint (anonymous requests get `401`); this Actor needs no key, so it gives you the excerpt plus `pdfUrl` — the PDF bucket at `storage.courtlistener.com` is public and needs no token either, so you can fetch and parse the full document yourself.
- **Several opinion fields are sparse, and how sparse depends on the court.** CourtListener's search index returns these fields for every opinion row, but the value is empty unless the publishing court supplied it. Measured over 240 live opinion rows across 12 court/date slices (2026-09-19): `neutralCite` **25%**, `judge` **16%**, `syllabus` **12%**, `panelNames` **4%**, `lexisCite` **2%**, `proceduralHistory` **<1%**. The distribution is strongly court-dependent rather than random — Ohio and Illinois appellate rows carried `syllabus`/`neutralCite` on **20/20**, while `ca9`, `ca2`, `ny` and `scotus` carried none. If your pipeline needs one of these, filter `courts` to a court that publishes it and check a small run first. Nothing is dropped or charged differently because a field is empty — you always pay $0.002 per row returned.
- **`posture` was removed from the schema (2026-09-19)**, not just left sparse. It measured 0% across 320 opinion rows spanning 13 court/date slices — including pre-1970 SCOTUS opinions and a recent-SCOTUS control — so age and court choice don't explain it. CourtListener does carry procedural posture on its authenticated `/clusters/` detail endpoint, but that endpoint 401s without a CourtListener API key, and this Actor is deliberately anonymous/keyless (see above) — so the field was permanently empty for every buyer, not just sparse. Dropped rather than kept as a column that can never have a value.
- **`cause` and `juryDemand` are sparse fleet-wide, regardless of court — `chapter` is not.** Measured over 240 live docket rows across 12 courts (2026-09-22, mixing 6 district and 6 bankruptcy courts, 20 rows each, no query filter): `chapter` **38%** overall, but that number is really two extremes hiding inside one average — **0%** on every district-court row sampled (`nysd`, `cand`, `ilnd`, `txnd`, `flsd`, `nyed`, `mad`) and **75–100%** on every bankruptcy-court row sampled (`cacb`, `nysb`, `deb`, `ilnb`, `txsb`) — it is populated exactly where it can be (bankruptcy filings carry a chapter; civil filings don't) and nowhere else. `cause` and `juryDemand` did not follow that pattern: **1%** each, non-zero only on two of the twelve courts (`nysd`, `cand`) and absent even from other district courts in the same sample (`ilnd`, `txnd`, `flsd`, `nyed`, `mad`) — RECAP's civil-cover-sheet extraction that would populate these two apparently doesn't run consistently across districts. If your use case is bankruptcy analytics, filter `courts` to bankruptcy court IDs and expect `chapter` reliably; don't build on `cause`/`juryDemand` being present anywhere.
- **`jurisdictionType` is now docket-only (changed 2026-09-19).** On docket rows it is PACER's readable text for the basis of the court's jurisdiction over the *case* — `"Diversity"`, `"Federal Question"`. It previously also carried a value on opinion rows, but that value was a **different quantity under the same name**: CourtListener's `court_jurisdiction`, which classifies the *court* (`"F"` = Federal Appellate, `"FD"` = Federal District, `"S"` = State Supreme). Mixing the two in one column meant a `recordType: "both"` run produced a field you could not group on. It was also near-empty — 20/140 opinion rows across 8 court slices, and 21/240 across 12 slices, essentially SCOTUS-only. Opinion rows now return `jurisdictionType: null`, the same as the other docket-only columns (`cause`, `juryDemand`, `chapter`). Run with `recordType: "dockets"` for case-jurisdiction analytics — and use the new **`courtJurisdiction`** field (below) for the court-classification quantity, which is now available on *every* row rather than SCOTUS-only.
- **`jurisdictionType` casing is normalized (changed 2026-09-19).** PACER's own data is inconsistent across courts — the same category comes back as `"Federal Question"` from one court and `"Federal question"` from another (measured live: 429 rows across 20 districts turned up both, plus `"U.S. Government Defendant"` vs `"Government plaintiff"`). This Actor now title-cases every value so grouping by `jurisdictionType` doesn't silently split into duplicate buckets for the same category. It does **not** merge genuinely different upstream phrasings — `"Diversity"` and `"Diversity of citizenship"` stay separate, since collapsing those would be a guess about PACER's own categorization, not a casing fix.
- **`courtJurisdiction` covers 3,358 courts — both in-use and not-in-use (expanded 2026-09-28)** — and is `null` only for the small remainder. The label comes from a static map harvested from CourtListener's own `/courts/` API (472 `in_use=true` courts, 2026-09-19, plus 2,887 `in_use=false` courts, 2026-09-28 — historical courts like `ptab`, `bpai` and `ag` that are no longer accepting new filings but still hold real, searchable opinions/dockets), with the 23 code->label pairs taken from that endpoint's `OPTIONS` schema — so all of it is CourtListener's values, not our guesses. It measured **100% fill** on a live `recordType: "both"` run against in-use courts, and non-null on a not-in-use control (`ag`) verified live post-expansion. Only a court genuinely absent from CourtListener's own `/courts/` listing, or one of the rare courts CourtListener itself ships with no jurisdiction on file, returns `null`. The map is a snapshot: a court added upstream after these dates reads `null` until the map is refreshed.
- **Dockets and opinions are separate indexes.** A case present in one is often absent from the other; use `both` when unsure.
- The query is a **full-text search**, not a case-number lookup. For a docket number, put it in `query` as-is and widen the court filter.

## Pricing

`$0.002` per result, **no run-start fee**. 1,000 records costs $2.00.

For comparison, re-verified **2026-10-03** against live in-effect pricing — searching the Store for "court records", "courtlistener", "pacer", "docket" **and** "case law" rather than one or three terms, since a narrower search term is exactly how a rival gets missed: `nexgendata/court-records-search` (61 users) still charges a flat **$0.10 per result** plus a $0.00005 start fee, unchanged since 2026-07-17 — 50× this Actor. `automation-lab/court-records-scraper` (71 users) still charges a **$0.005 run-start fee plus $0.0023/record** on the Free plan, tapering to $0.00056 on Diamond; cheaper per record at very high volume on a paid Apify plan, more expensive for the small and mid-size runs most buyers actually make, and it bills you before it returns a single row. `fortuitous_pirate/courtlistener-legal-data` (21 users, not previously named) covers the same nationwide CourtListener dockets+opinions+RECAP+oral-arguments scope at a flat $0.02 start + $0.004/record — 2× this Actor's per-record rate before the start fee is even added; its own `pricingInfos` already schedules the start fee down to $0.005 on 2026-10-13, which narrows but doesn't close the gap (still 2× per record).

Five listings are narrower in scope than a nationwide dockets+opinions search (re-verified live 2026-10-04): `parseforge/harris-county-court-records-scraper` (29 users) is Harris County, TX only, at $0.01199–0.01599/record plus a tiered **$0.02 FREE→$0.015 GOLD+** start fee — 6–8× this Actor's rate for one county (its 2026-10-04 restructure has now landed: the flat $0.005 start fee was replaced by that tiered Actor Start event, the per-record rate is unchanged, and a new optional `case-details` event bills $0.005 FREE→$0.00375 GOLD+ once per record, only when an opt-in party-lookup enrichment actually returns data). `fortuitous_pirate/florida-court-records-scraper` (14 users) is Florida only, at $0.05 start + $0.0035/record. `andrew_avina/pacer-intelligence-mcp` (13 users) is a PACER-only MCP server at a flat $0.003/record, no start fee — closer to our rate but MCP-only, no plain Actor run, and it has no opinions coverage at all. `pink_comic/bankruptcy-filing-search` (23 users) ties this Actor's $0.002/record exactly but only ever returns RECAP dockets in open bankruptcy chapters — no opinions, no civil/criminal dockets. `parseforge/business-bankruptcy-filings-scraper` (11 users, not previously named, same vendor pattern as `parseforge/harris-county` above) covers the identical bankruptcy-only RECAP slice at $0.005 start + a tiered $0.01599 FREE→$0.01199 GOLD+ per record — 6–8× this Actor's rate for a narrower dataset than `pink_comic` already undercuts at parity.

A wider sweep (`court records` + `courtlistener` + `pacer` + `docket` + `case law`, re-verified 2026-10-03) also turned up listings over the same nationwide CourtListener dockets+opinions scope this Actor covers, none previously named: `seibs.co/court-records-intel` (11 users) charges a flat **$0.005/record**, 2.5× this Actor's rate, so not an undercutter. `martc03/court-records-mcp` (33 users — more users than every rival in this section except the two biggest) is on Apify's **FREE** pricing model: $0, the cheapest any rival can be. It is MCP-only — a tool-call interface for AI assistants, not a plain Actor run, with no CSV/Excel export, no `startUrl` paste-in, no `watchLabel` incremental mode and no bulk `maxResults` export of the kind a legal-ops pipeline needs — so free is the headline, not a direct substitute for a dataset export. Disclosed here rather than omitted because it is the single biggest unnamed listing in the niche by user count. `maydit/us-court-cases-scraper` (4 users), billed as a "PACER Alternative API", tiers $0.003/record on Free down to $0.0018/record on Gold+ plus a flat $0.00005 start fee — pricier than this Actor at every tier. `alwaysprimedev/courtlistener-scraper` (6 users, 3 new in 30 days) charges a flat $0.0025/record plus a $0.00005 start fee — also pricier than us at every tier, no undercut. Two single-index sibling listings mirror ones already named above: `nexgendata/courtlistener-federal-docket-scraper` (13 users) is the RECAP-dockets-only counterpart to the already-named `nexgendata/court-records-search`, same $0.00005 start fee and the identical flat **$0.10/record** rate; `pink_comic/courtlistener-legal-opinions` (6 users) is the opinions-only counterpart to the already-named `pink_comic/recap-federal-court-dockets`, same $0.0001 start fee and the identical flat $0.002/record rate that ties us.

**Two listings the broader search turned up are a genuine undercut.** `themineworks/courtlistener-court-records` (10 users) scrapes the exact same CourtListener dockets-and-opinions scope this Actor does — its own title says "Opinions & Dockets" — at $0.005 start plus a tiered $0.001/record on Free down to $0.0006/record on Diamond. On a 100-row run that's $0.105 against this Actor's $0.20 — roughly half, at every tier, despite the start fee. Its own listing title advertises 16 output fields against this Actor's 41. `scrapesage/court-records-scraper` (4 users, not previously named) splits dockets and opinions into separate tiered charge events with no start fee — opinions taper $0.004 (Free) → $0.001 (Diamond), dockets taper $0.006 (Free) → $0.0015 (Diamond) — crossing under our flat $0.002 on opinions from Platinum up ($0.00152, $0.001) and on dockets only on Diamond ($0.0015); every tier below that is pricier than us on both record types. It also prices three record types this Actor does not offer at all — judge/judicial-profile, oral-argument and financial-disclosure records — each its own tiered event $0.00125–$0.005. Two more sit close to parity rather than beating us outright: `pink_comic/recap-federal-court-dockets` (15 users) ties this Actor's $0.002/record exactly but is RECAP dockets only (no opinions) and adds a $0.0001 start fee; `haketa/federal-court-records-scraper` (9 users) undercuts only on its Diamond tier ($0.0018/record, which needs a paid Apify plan) and is pricier than us on every tier below that. *(Competitor pricing verified live 2026-10-03.)*

**What we do not claim:** this is not the cheapest nationwide CourtListener-based Actor in the Store. `themineworks/courtlistener-court-records` beats our per-record rate at every tier, by roughly half, and `scrapesage/court-records-scraper` beats us on opinions from Platinum up and on dockets at Diamond. What this Actor has that theirs doesn't, per the sections above: both record types in one schema sharing a `courtJurisdiction` label across 3,358 courts, real boolean-operator and quoted-phrase search, a `startUrl` paste-in from CourtListener's own search page, `watchChanges` for docket-termination detection, and roughly 2.5× the output fields (41 vs. their own claimed 16) — `scrapesage` needs a paid Apify plan to beat us at all, and only on part of its range. If price per row is what matters most for your use case on a Free/Bronze plan, check `themineworks` first. Verified live 2026-10-03.

## Data source, legality and privacy

Data comes from [CourtListener](https://www.courtlistener.com/) / the [Free Law Project](https://free.law/), a non-profit that publishes US court records as open data, via its documented public REST API. No login is used, no paywall is bypassed, and no page is scraped behind authentication.

Every name in the output — parties, attorneys, law firms, judges — appears on a **public court record** and is a professional or institutional participant in a public proceeding. The API returns no email addresses and no phone numbers, and this Actor adds none.

## Source code

<https://github.com/Fetchsmith/fetchsmith/tree/main/actors/court-records-scraper>

## Related guides
- [Eight ways an "only new since last run" watch mode silently stops working](https://fetchsmith.com/blog/incremental-api-watch-mode-four-traps) — the fleet-wide survey of watch-mode failure shapes across all nineteen incremental Actors, this one included.
- [CourtListener's court-records API needs no key — except for the one endpoint most wrapper docs point you at first](https://fetchsmith.com/blog/courtlistener-search-api-two-auth-tiers)
- [CourtListener's "any" opinion status wasn't any — and the published-only default hides a different share every time](https://fetchsmith.com/blog/court-records-opinion-status-any-is-not-any)
- [We nearly charged our own buyers twice for rows they'd already paid for](https://fetchsmith.com/blog/watch-baseline-eviction-rebilling) — a capped watch-mode baseline can silently evict old-but-current ids on a high-volume run, re-delivering (and re-billing) rows already paid for. Reproduced on this Actor, closed with truncation tracking.
- [All FetchSmith tools and APIs](https://fetchsmith.com/tools)
