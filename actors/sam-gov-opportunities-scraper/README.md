# SAM.gov Opportunities Scraper – US Federal Contracts & Bids

Scrape live US federal contracting opportunities from SAM.gov — presolicitations, solicitations, combined synopses, sources sought, special notices and award notices — with **no API key, no login, no proxy and no browser**. Filter by keyword, NAICS code, set-aside type, notice type, place-of-performance state and issuing organization, and optionally enrich every row with the contracting officer's contact details, NAICS codes, set-aside and place of performance.

## What it does
- Calls the same backend that powers sam.gov's own public opportunity search page, so results match what you see on the site. **SAM.gov's official developer API (`api.sam.gov/opportunities/v2`) requires a free registered API key — this Actor needs none.** You do not have to register with GSA, wait for key approval, or rotate a key across a team.
- **`enrichDetail` joins each row with the per-opportunity record**, which is where the fields a bidder actually qualifies on live: `naicsCodes`, `setAside`, `placeOfPerformanceState`/`placeOfPerformanceCountry`, and `pointOfContact` (the contracting officer's name, email and phone, primary and secondary). None of these are on the search row. Off by default because it costs one extra HTTP call per row; turn it on when you are qualifying, not just listing.
- **Multi-value filters really OR.** `naicsCodes: ["541511", "541512"]` returns the union of both, not just the first. This is worth stating because SAM.gov's backend silently accepts a repeated query parameter and then honours only the first value — verified live: `naics=541511` → 607 hits, `naics=541512` → 312, repeated-key form → 607 (wrong, and no error), comma-joined form → exactly 919. This Actor sends the comma-joined form for every multi-value filter (`naicsCodes`, `setAsideTypes`, `noticeTypes`, `states`), so a two-code search does not quietly drop half your pipeline.
- **`noticeTypes` uses SAM's own notice-type codes** — `p` presolicitation, `o` solicitation, `k` combined synopsis/solicitation, `r` sources sought, `a` award notice, `s` special notice, `g` sale of surplus, `i` intent to bundle, `u` justification. Every row also comes back with both the raw `noticeTypeCode` and the human-readable `noticeType`.
- **`states` filters on place of performance, not the issuing office.** SAM's official API calls this `state`; on this backend that parameter name is silently ignored and returns zero rows, a trap this Actor sidesteps by sending `pop_state`.
- `activeOnly` (default on) restricts to opportunities still open for response. Turn it off for historical and award research.
- Pay per result: charged only for rows actually returned, **with no Actor-start fee** — a search that matches nothing costs nothing.
- **`watchLabel` — only what's new since your last run.** Name a saved search and every run after the first returns just the opportunities not already delivered under that label and filter combination. The first run for a label is a free baseline (0 results, 0 charged); it records what already matches in a key-value store on your own Apify account, keyed by the label plus a fingerprint of your other filters, so editing a filter starts a fresh baseline instead of dumping every previously-excluded opportunity as "new". Built for a daily/weekly scheduled run.
- **`description` is the full solicitation text**, not a truncated snippet — the same original HTML SAM.gov itself stores, which can run to several thousand characters on a detailed notice.
- **`watchChanges` — also catch a deadline extension, a lifecycle transition, or an award landing.** Add this to `watchLabel` and an opportunity you already have gets re-delivered (at the normal per-row price, tagged `_watchChangeType`/`_watchPrevious`) if its `isActive` flag, `noticeTypeCode` (a presolicitation turning into a solicitation, or a solicitation turning into an award), `responseDate` (deadline moved), `modifiedDate`, `modificationsCount` or `awardeeName` (an award landing) has changed since you last saw it — not just brand-new opportunities. Off by default so existing watches keep their current behaviour.

## Use cases
- **GovCon bid pipelines** — pull every active solicitation in your NAICS codes and set-aside category (`naicsCodes` + `setAsideTypes` + `noticeTypes: ["o", "k"]`) into a CRM, already qualified by place of performance.
- **Small-business / 8(a) / SDVOSB capture** — filter to the set-asides you actually hold and stop reading opportunities you are not eligible for.
- **Contracting-officer outreach on sources-sought notices** — `noticeTypes: ["r"]` plus `enrichDetail` gives you the pre-RFP notices where a vendor can still shape the requirement, together with the officer's published contact details.
- **Competitive award research** — `activeOnly: false` with `noticeTypes: ["a"]` returns award notices including `awardeeName` and `awardeeUeiSAM`, so you can see who is winning in your NAICS.
- **Agency- or state-specific monitoring** — `organizationId` for one department/agency, or `states` for the geographies your team can actually staff.
- **Daily cron alerts** — `watchLabel` on a narrow keyword/NAICS search on a schedule returns only the handful of new notices, instead of refreshing sam.gov by hand or re-paying for the whole result set every run.
- **Deadline-extension / lifecycle alerts** — `watchLabel` + `watchChanges` flags a presolicitation turning into a solicitation, a deadline extension, or an award landing on a solicitation you're already tracking.

### Example input
```json
{
  "keyword": "solar",
  "naicsCodes": ["221122"],
  "maxResults": 15,
  "enrichDetail": true
}
```

## Input
| Field | Type | Description |
|---|---|---|
| `keyword` | string | Full-text search across the opportunity index (default `contract`) |
| `naicsCodes` | array | NAICS codes, e.g. `["541511", "541512"]` — multiple codes are ORed |
| `setAsideTypes` | array | Set-aside codes, e.g. `["SBA"]` — multiple values are ORed |
| `noticeTypes` | array | Notice-type codes `p`/`o`/`k`/`r`/`a`/`s`/`g`/`i`/`u` — multiple values are ORed |
| `states` | array | Two-letter **place-of-performance** state codes, e.g. `["TX", "CA"]` — ORed |
| `organizationId` | string | Restrict to one issuing department/agency/office by SAM organization id |
| `activeOnly` | boolean | Only opportunities still open for response (default `true`) |
| `enrichDetail` | boolean | Join each row with NAICS / set-aside / place of performance / contacts (default `false`) |
| `maxResults` | integer | Cap on rows returned (default `200`) |
| `watchLabel` | string | Optional. Name a saved search to get only opportunities new since your last run under that label — see FAQ |
| `watchChanges` | boolean | Optional, requires `watchLabel`. Also re-deliver an already-seen opportunity if `isActive`, `noticeTypeCode`, `responseDate`, `modifiedDate`, `modificationsCount`, `awardeeName` or `description` changed (default `false`) — see FAQ |
| `webhookUrl` | string | Optional. POST a small JSON completion summary (opportunities pushed, rows scanned, dataset ID, watch new/changed/skipped counts) here when the run finishes — see FAQ |

## Sample output row
```json
{
  "opportunityId": "c8092b56b2c14be9bea3ac6081207963",
  "title": "This is a sources sought to identify contractors who possess the capabilities to provide CFE and associated EACs produced using domestically-manufactured solar panel systems.",
  "solicitationNumber": "47PA0723SS0001",
  "noticeTypeCode": "r",
  "noticeType": "Sources Sought",
  "isActive": true,
  "isCanceled": false,
  "publishDate": "2023-07-12T19:23:54+00:00",
  "modifiedDate": "2023-07-12T19:23:54+00:00",
  "responseDate": "2023-06-27T20:00:00+00:00",
  "responseDateActual": "2023-06-27T16:00:00-04:00",
  "responseTimeZone": "America/New_York",
  "department": "GENERAL SERVICES ADMINISTRATION",
  "agency": "PUBLIC BUILDINGS SERVICE",
  "office": "PBS R00 CPF CLEAN ENERGY",
  "description": "<p><strong>THIS IS A SOURCES SOUGHT ANNOUNCEMENT ONLY - </strong>A solicitation is not available at this time...",
  "awardeeName": null,
  "awardeeUeiSAM": null,
  "modificationsCount": 0,
  "sourceUrl": "https://sam.gov/opp/c8092b56b2c14be9bea3ac6081207963/view",
  "naicsCodes": ["221122"],
  "setAside": null,
  "placeOfPerformanceState": null,
  "placeOfPerformanceCountry": "USA",
  "pointOfContact": [
    { "name": "Bonnie Bueter", "email": "bonnie.bueter@gsa.gov", "phone": "202-227-1635", "type": "primary" }
  ]
}
```

## FAQ
**Do I need a SAM.gov API key?** No. The official `api.sam.gov` developer API does require a free registered key, but this Actor uses the unauthenticated backend behind sam.gov's own public search page instead. Nothing to register, nothing to rotate.

**Is there a posted-date range filter?** Not on this backend — it exposes no `postedFrom`/`postedTo` equivalent. Use `activeOnly` to separate open from closed opportunities, and filter on the `publishDate` / `modifiedDate` fields on each row afterwards. (`responseDate` is the deadline.)

**Is `description` the full notice text?** Yes — the full solicitation description as SAM.gov itself stores it (original HTML markup preserved), not a truncated snippet; it can run to several thousand characters on a detailed notice. Any attachments (drawings, full statements of work as separate documents) still live only on the notice page, linked via `sourceUrl`.

**How deep can a search go?** The backend caps paging at 10,000 rows per query, so a very broad keyword will stop there. Narrow with `naicsCodes`, `noticeTypes` or `states` rather than trying to page past it.

**Is `pointOfContact` personal data?** These are government contracting officers' official work contact details, published by the agency itself as a required part of the statutory public notice — the same disclosure class as the contacts on our NIH RePORTER and EU TED Actors. They are returned as SAM.gov publishes them; they are not aggregated across sources, cross-referenced with any other dataset, or resold as a people-lookup product.

**How does the price compare?** $0.0015 per returned row with **no Actor-start fee**. The comparable paid SAM.gov Actors on the Store charge $0.003–$0.008 per row, and several add a $0.01 per-run start fee on top.

**How does `watchLabel` know what's already new, and where is that baseline stored?** In a key-value store on your own Apify account, keyed by the label plus a fingerprint of `keyword`/`naicsCodes`/`setAsideTypes`/`noticeTypes`/`states`/`organizationId`/`activeOnly`. The first run for a label just records every currently-matching opportunity id and returns zero rows (you pay nothing); every run after that returns only ids not already in that record. Changing any of those filters starts a fresh baseline under the same label instead of comparing against the old filter's results.

**Does `watchChanges` cost extra?** No extra fee — a changed opportunity is billed at the same $0.0015/row as a new one, so you only pay when there's actually something to see. Plain `watchLabel` never re-delivers an opportunity it has already sent you, even if the agency later extends the deadline or the notice moves from presolicitation to solicitation to award. Set `watchChanges: true` and each run also compares every already-delivered opportunity's `isActive`/`noticeTypeCode`/`responseDate`/`modifiedDate`/`modificationsCount`/`awardeeName` (plus an internal fingerprint of `description`) against what it looked like last time; if anything moved, the row is re-delivered tagged with `_watchChangeType` (which field(s) changed) and `_watchPrevious` (their prior values — `description`'s previous value is a fixed note, since only a fingerprint of that text is stored, never the full text). Verified live: seeding a baseline, editing a delivered opportunity's recorded `isActive` flag and `responseDate` directly in the stored snapshot, then rerunning returned exactly those 2 rows with the correct change tags and nothing else — and a plain unchanged rerun after that returned 0 rows again.

**How do I know a run returned everything, without reading the log?** Every run writes a `RUN_SUMMARY` record to its own key-value store — fetch it with `GET https://api.apify.com/v2/actor-runs/<runId>/key-value-store/records/RUN_SUMMARY` (no webhook needed; it's also sent as `summary` on any `webhookUrl` POST). It carries `declaredMatches` (what SAM.gov itself says matches your filters — `null`, never `0`, if the search never answered with a count), `reachableMatches` (those minus anything past SAM.gov's 10,000-row depth cap), `scanned`, `delivered`, `pages`, `pagesFailed`, `duplicateRowsDropped` and a boolean `complete`. When `complete` is `false`, `incompleteReason` is one of `upstream-error` (SAM.gov stopped answering mid-walk, after 4 retries), `short-page` (SAM.gov returned an empty page before its own declared total was reached), `depth-cap` (the query is deeper than the 10,000 rows this backend will serve), `duplicate-rows` (SAM.gov served its whole result set but repeated rows across pages, so there were fewer distinct opportunities than it declared), `max-results` (your `maxResults` is below the match count — the common, harmless one), `charge-limit` (the run's pay-per-event limit stopped it), or `enrich-failed` (`enrichDetail` was on and some detail lookups failed, so their `naicsCodes`/`setAside`/`pointOfContact` are `null` for that reason rather than because SAM.gov has none). `incompleteDetail` spells out the numbers and `lastApiError` gives the underlying HTTP cause. A short run still finishes as `SUCCEEDED` — the rows it did return are real — so this record, plus the run's status message, is how a pipeline tells "200 of 200 matches" apart from "200 of 12,297".

**Can the same opportunity come back twice (and be charged twice)?** No. SAM.gov's backend pages by offset over a live, relevance-sorted index, so rows genuinely do repeat across pages — measured on a 19,834-match query, a full 10,000-row walk contained only 8,990 distinct opportunity ids, about 10% repeats. Repeats are dropped inside the walk, before any `Actor.charge()` call, so you are only ever billed for distinct `opportunityId` values; `RUN_SUMMARY.duplicateRowsDropped` tells you how many there were. This is also why a very broad query can return fewer rows than `declaredMatches` even when nothing failed — that case reports `incompleteReason: "duplicate-rows"` rather than pretending the backend broke.

**What happens if a watch baseline run doesn't finish?** It is flagged rather than silently trusted. A baseline that stopped early would report everything past the stopping point as brand new — and charge for it — on your first incremental run, so an incomplete seed saves with `lastRunStatus: "seeded-incomplete"`, logs a `BASELINE INCOMPLETE` warning naming the reason, and sets a run status message telling you to re-seed before scheduling. `RUN_SUMMARY` reports `mode: "watch-seed"`, `complete: false` and `baselineSize` so you can check it from code. The same applies if a baseline ever outgrows the 60,000-entry record cap (`baselineTruncated`).

**How is `webhookUrl` different from Apify's own platform webhooks?** Apify's platform webhooks are configured separately per Task/Actor via the Console or the Webhooks API — useful if you already live in the Apify Console, but extra setup if you're calling this Actor's API directly and just want a completion ping. `webhookUrl` is a plain input field: set it on the run itself and it POSTs a JSON body (`actorRunId`, `defaultDatasetId`, `finishedAt`, `pushed`, `rowsScanned`, the full `summary` object described above, and — if `watchLabel` is set — `watchSeeding`/`watchNewCount`/`watchChangedCount`/`watchSkippedCount`) once the run finishes and every opportunity is already pushed and charged. Especially useful with `watchLabel` on a scheduled bid alert: your endpoint is told how many new solicitations landed without polling the dataset, and `watchSeeding: true` distinguishes "this was the free baseline run" from "your watch is live and quiet" — both report zero new rows otherwise. It's best-effort — a slow or failing webhook only logs a warning, it never fails the run, changes the result set, or affects billing.

## Related guides
- https://fetchsmith.com/blog/usaspending-federal-awards-json-api
- https://fetchsmith.com/blog/grants-gov-federal-grant-opportunities-json-api
- https://fetchsmith.com/tools

## Source code
https://github.com/Fetchsmith/fetchsmith/tree/main/actors/sam-gov-opportunities-scraper

More tools: [fetchsmith.com/tools](https://fetchsmith.com/tools) — 22 HTTP-only Actors for public data sources, no browser required.
