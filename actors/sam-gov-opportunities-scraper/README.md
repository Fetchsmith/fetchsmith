# SAM.gov Scraper – US Federal Contracts, Bids, Wage Determinations & Grants

Scrape live US federal contracting opportunities from SAM.gov — presolicitations, solicitations, combined synopses, sources sought, special notices and award notices — with **no API key, no login, no proxy and no browser**. Filter by keyword, NAICS code, set-aside type, notice type, place-of-performance state and issuing organization, and optionally enrich every row with the contracting officer's contact details, NAICS codes, set-aside and place of performance.

## What it does
- **Six public SAM.gov datasets, one Actor, no key.** `dataType` picks which one: `opportunities` (default — solicitations, presolicitations, sources sought, awards), one of three Department of Labor wage-determination sets SAM.gov publishes — `wage-determinations-dbra` (Davis-Bacon Act, construction), `wage-determinations-sca` (Service Contract Act, services) and `wage-determinations-cba` (collective bargaining agreements) — `assistance-listings`, the Catalog of Federal Domestic Assistance (CFDA) grant/loan/direct-payment programs, or `exclusions`, the federal debarment/suspension list (organizations only — see below). All six come off the same keyless public search backend, so none of them needs a registered API key.
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

## Wage determinations
Set `dataType` to one of the three wage-determination options and the same filters you already know (`keyword`, `states`, `activeOnly`, `maxResults`, `watchLabel`, `watchChanges`, `webhookUrl`) apply to Department of Labor determinations instead of solicitations.

| `dataType` | What it returns | Live record count |
|---|---|---|
| `wage-determinations-dbra` | Davis-Bacon Act determinations — construction, with `constructionTypes` (Building / Heavy / Highway / Residential) | ~85,400 (~4,200 active) |
| `wage-determinations-sca` | Service Contract Act determinations — services, with a `services[]` list of covered categories | ~2,700 (~1,500 active) |
| `wage-determinations-cba` | Collective bargaining agreement determinations | ~107,600 (~10,100 active) |

- **Coverage is normalized across all three.** SAM.gov returns the covered geography in three different shapes (DBRA nests a single `location.state`, CBA an array of `location.states`, SCA an array whose counties split into `include`/`exclude` lists). Every row here carries the same flat `coverage` array of `{ stateCode, stateName, isStateWide, counties, excludedCounties }`, plus `stateCodes` and `countyCount` for filtering. SCA's *excluded* counties are kept in their own field rather than merged into the covered list — an excluded county is the opposite of a covered one.
- **Dates are normalized too.** `publishDate` comes back as an ISO string on CBA rows but as epoch milliseconds on DBRA/SCA rows; this Actor emits ISO 8601 for every row so you are not parsing two formats.
- **`states` filters on the state the determination covers**, and multiple states OR together the same way: measured live, `AL` → 3,509 and `TX` → 6,909 CBA determinations, `["AL","TX"]` → 10,415 (the 3 determinations covering both states are returned once, not twice).
- **`activeOnly` means "currently in force"** — a determination superseded by a later revision has `isActive: false`. Combine with `watchLabel` + `watchChanges` and a run tells you when a determination you track is revised (`revisionNumber` moves) or goes inactive.
- **`keyword` searches the reference number, not trades.** On these indices `q` matches the determination's own number (e.g. `AK20260001`), so `q=roofing` returns zero against 85,000+ live Davis-Bacon records. Filter by state and construction/service type instead, and leave `keyword` empty to get the whole set.
- **What this does NOT include: per-occupation hourly wage rate tables.** SAM.gov does not publish the rate schedule on any of the three search indices, so every row has `wageRates: null`. This Actor gives you the determination *index* — which determination applies to which state and counties, its revision number, its construction/service scope and whether it is current — which is what you need to pick the right determination; read the rates themselves from the determination's own page on sam.gov.
- `naicsCodes`, `setAsideTypes`, `noticeTypes`, `organizationId` and `enrichDetail` are opportunity-only. If you set one in a wage-determination run it is ignored and the run logs a warning saying so, rather than silently returning an unfiltered set that looks filtered.

### Example wage-determination input
```json
{
  "dataType": "wage-determinations-dbra",
  "states": ["TX", "NM"],
  "activeOnly": true,
  "maxResults": 500
}
```

### Sample wage-determination output row
```json
{
  "wageDeterminationId": "AK20260001",
  "referenceNumber": "AK20260001",
  "shortReferenceNumber": "AK1",
  "title": "AK20260001",
  "actCode": "DBA",
  "actName": "Davis-Bacon Act",
  "recordType": "wdDBRA",
  "isActive": true,
  "isStandard": true,
  "revisionNumber": 2,
  "year": 2026,
  "publishDate": "2026-09-17T04:00:00.000Z",
  "modifiedDate": "2026-09-17T00:00:00-04:00",
  "constructionTypes": ["Building", "Heavy"],
  "services": null,
  "coverage": [
    {
      "stateCode": "AK",
      "stateName": "Alaska",
      "isStateWide": null,
      "counties": ["Anchorage", "Matanuska-Susitna", "Fairbanks North Star", "Juneau"],
      "excludedCounties": []
    }
  ],
  "stateCodes": ["AK"],
  "countyCount": 28,
  "wageRates": null
}
```

## Assistance listings (CFDA)
Set `dataType` to `assistance-listings` to pull the Catalog of Federal Domestic Assistance — ~7,400 federal grant/loan/direct-payment programs (~2,900 currently active), each with its objective, eligibility rules, funding-obligation history, related programs and the agency's own published program contact.

- **Supports `keyword`, `organizationId`, `activeOnly`, `maxResults`, `watchLabel`, `watchChanges`, `webhookUrl`.** `naicsCodes`, `setAsideTypes`, `noticeTypes` and `states` are opportunity-only and are ignored (with a log warning) here — assistance-listing programs are nationwide, not filtered by place of performance. `enrichDetail` is also ignored: the search row already carries the full record.
- **`keyword` matches title, objective and program number** (e.g. `q=flood` → 60 of 7,392 programs), not a reference-number-only match like the wage-determination indices.
- **`programNumber`** (e.g. `"12.103"`) is the CFDA number buyers actually search by — the natural reference for cross-checking against grants.gov or an agency's own NOFO.
- **`obligations`** is shipped as SAM.gov's own raw per-assistance-type funding history (`{ assistanceType, values: [{ year, flag }], additionalInfo }`) rather than normalized into a single amount field — the sampled records carry only a `flag` (e.g. `"ena"` = estimate not available) per year, not a consistent numeric amount, so a normalized field would either be frequently null or silently wrong.
- **`contacts`** is the agency's own published program contact (name/title/phone/address) from the public listing, the same disclosure class as opportunities' `pointOfContact`.
- **`watchChanges` on assistance listings** re-delivers a program if its active or funded status, modified date, or historical-index entry count has changed since you last saw it — there is no revision number or response deadline on this dataset, so funded/active status is the closest signal to "this program moved."

### Example assistance-listings input
```json
{
  "dataType": "assistance-listings",
  "keyword": "broadband",
  "activeOnly": true,
  "maxResults": 100
}
```

### Sample assistance-listings output row
```json
{
  "assistanceListingId": "8d745b5ad52a421dbf9483c7451adec1",
  "programNumber": "12.002",
  "title": "Procurement Technical Assistance For Business Firms",
  "alternativeNames": ["APEX Accelerator Program/Procurement Technical Assistance Program (PTAP))"],
  "objective": "Building a strong and sustainable U.S. supply chain and supporting a wide range of diverse businesses by providing procurement assistance to businesses...",
  "isActive": true,
  "isFunded": true,
  "isLatest": true,
  "publishDate": "2026-01-16T00:02:55-05:00",
  "modifiedDate": "2026-01-16T00:02:55-05:00",
  "department": "DEPT OF DEFENSE",
  "agency": "WASHINGTON HEADQUARTERS SERVICES (WHS)",
  "assistanceTypes": [["Financial", "Cooperative Agreement"]],
  "eligibleApplicants": ["Nonprofit Organization", "Tribal", "..."],
  "eligibleApplicantsNote": "Eligible applicants. Only those entities listed in this section are eligible to apply...",
  "eligibleBeneficiaries": ["Anyone/general public", "State", "Local"],
  "eligibleBeneficiariesNote": null,
  "obligations": [{ "assistanceType": { "code": "F001", "value": "Grant" }, "values": [{ "flag": "ena", "year": 2025 }], "additionalInfo": null }],
  "contacts": [{ "name": null, "title": null, "phone": null, "address": "Commander, U.S. Army Corps of Engineers, Attn: CECW-OE, Washington, DC 20314-1000." }],
  "relatedPrograms": ["12.104", "12.105"],
  "website": "http://www.usace.army.mil/business.html.",
  "historicalIndexCount": 6,
  "sourceUrl": "https://sam.gov/fal/8d745b5ad52a421dbf9483c7451adec1/view"
}
```

## Exclusions
Set `dataType` to `exclusions` to pull SAM.gov's federal debarment/suspension list — entities barred from receiving federal contracts, grants or other assistance — **restricted to organizations only (firms, vessels and special entity designations, ~35,200 records)**.

- **This Actor never returns the individual-person exclusion records SAM.gov also publishes.** SAM.gov's exclusions index carries 168,673 records total, and 79% of them (133,478) name a private person with a home city, state and zip — not a company. Turning that into a bulk-downloadable dataset would be a people-search product, which this Actor deliberately does not offer: the `classification` filter that separates organizations from individuals is hard-coded into every request this Actor makes, with no input anywhere that can widen it. If you need to check whether a specific named individual is excluded, look them up one at a time on [sam.gov/search](https://sam.gov/search/?index=ei) directly — SAM.gov's own public exclusions checker is exactly built for that single-lookup use case.
- **Supports `keyword` (matches the excluded entity's name), `organizationId`, `maxResults`, `watchLabel`, `watchChanges`, `webhookUrl`.** `naicsCodes`, `setAsideTypes`, `noticeTypes` and `states` are opportunity-only and are ignored (with a log warning) here. `activeOnly` has **no effect** on this dataset — SAM.gov's exclusions index does not support server-side active-status filtering, so every matching record is returned regardless of the setting; check each row's own `isActive`/`terminationDate` if you need to filter locally. `enrichDetail` is also ignored: the search row already carries the full record.
- **Rows SAM.gov itself flags "do not display" are dropped before you ever see them**, regardless of classification — a small number of exclusion records carry SAM.gov's own `noPublicDisplayFlag`, and this Actor honors it the same way sam.gov's own public search does.
- **`watchChanges` on exclusions** re-delivers a record if its active status or termination date has changed since you last saw it — the two signals that mean a debarment was lifted.

### Example exclusions input
```json
{
  "dataType": "exclusions",
  "keyword": "construction",
  "maxResults": 100
}
```

### Sample exclusions output row
```json
{
  "exclusionId": "4550ad9c-4b01-4e3d-bc94-716ee807836e",
  "title": "CHOSUN INTERNATIONAL CHEMICALS JOINT OPERATION COMPANY",
  "classificationCode": "Special Entity Designation",
  "ueiSam": "NTRNRHCG7L45",
  "cageCode": null,
  "samNumber": null,
  "addressCity": null,
  "addressState": null,
  "addressCountry": "USA",
  "addressZip": null,
  "exclusionTypeCode": "PR",
  "exclusionType": "Prohibition/Restriction",
  "exclusionProgram": "Reciprocal",
  "excludingAgency": "OFAC",
  "excludingAgencyDesc": "OFFICE OF FOREIGN ASSETS CONTROL",
  "department": "TREASURY, DEPARTMENT OF THE",
  "agency": "DEPARTMENTAL OFFICES",
  "office": "OFFICE OF FOREIGN ASSETS CONTROL",
  "isActive": true,
  "activationDate": null,
  "terminationDate": null,
  "isFascsaOrder": false,
  "sourceUrl": "https://sam.gov/exclusion/4550ad9c-4b01-4e3d-bc94-716ee807836e/view"
}
```

## Use cases
- **GovCon bid pipelines** — pull every active solicitation in your NAICS codes and set-aside category (`naicsCodes` + `setAsideTypes` + `noticeTypes: ["o", "k"]`) into a CRM, already qualified by place of performance.
- **Small-business / 8(a) / SDVOSB capture** — filter to the set-asides you actually hold and stop reading opportunities you are not eligible for.
- **Contracting-officer outreach on sources-sought notices** — `noticeTypes: ["r"]` plus `enrichDetail` gives you the pre-RFP notices where a vendor can still shape the requirement, together with the officer's published contact details.
- **Competitive award research** — `activeOnly: false` with `noticeTypes: ["a"]` returns award notices including `awardeeName` and `awardeeUeiSAM`, so you can see who is winning in your NAICS.
- **Agency- or state-specific monitoring** — `organizationId` for one department/agency, or `states` for the geographies your team can actually staff.
- **Daily cron alerts** — `watchLabel` on a narrow keyword/NAICS search on a schedule returns only the handful of new notices, instead of refreshing sam.gov by hand or re-paying for the whole result set every run.
- **Davis-Bacon compliance for construction bids** — `dataType: "wage-determinations-dbra"` with the states you build in tells you which determination covers each county and whether it is the current revision, so a bid is priced against a determination that is actually in force.
- **Service Contract Act scoping** — `dataType: "wage-determinations-sca"` returns the service categories each determination covers, so you can map a services solicitation to the right determination before pricing labour.
- **Wage-determination revision alerts** — `watchLabel` + `watchChanges` on a state-filtered wage-determination search re-delivers a determination only when its `revisionNumber`, active status or modified date moves — the signal that an in-flight bid or a running contract needs repricing.
- **Deadline-extension / lifecycle alerts** — `watchLabel` + `watchChanges` flags a presolicitation turning into a solicitation, a deadline extension, or an award landing on a solicitation you're already tracking.
- **Grant-eligibility screening** — `dataType: "assistance-listings"` with a keyword returns each matching program's `eligibleApplicants`/`eligibleBeneficiaries` and `objective`, so a grant writer can shortlist which CFDA programs a client actually qualifies for before drafting anything.
- **New/defunded grant program alerts** — `watchLabel` + `watchChanges` on `assistance-listings` flags a program going active, funded, or unfunded since your last check.

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
| `dataType` | string | Which SAM.gov dataset: `opportunities` (default), `wage-determinations-dbra`, `wage-determinations-sca`, `wage-determinations-cba`, `assistance-listings` |
| `keyword` | string | Full-text search across the opportunity index (default `contract`). On wage-determination types it matches the determination's reference number; on `assistance-listings` it matches title/objective/program number — leave empty for all |
| `naicsCodes` | array | NAICS codes, e.g. `["541511", "541512"]` — multiple codes are ORed. Opportunities only |
| `setAsideTypes` | array | Set-aside codes, e.g. `["SBA"]` — multiple values are ORed. Opportunities only |
| `noticeTypes` | array | Notice-type codes `p`/`o`/`k`/`r`/`a`/`s`/`g`/`i`/`u` — multiple values are ORed. Opportunities only |
| `states` | array | Two-letter state codes, e.g. `["TX", "CA"]` — ORed. Place of performance for opportunities; covered state for wage determinations; not supported for `assistance-listings` |
| `organizationId` | string | Restrict to one issuing department/agency/office by SAM organization id. Opportunities and `assistance-listings` only |
| `activeOnly` | boolean | Only opportunities still open for response — for wage determinations, only determinations currently in force; for `assistance-listings`, only currently-active programs (default `true`) |
| `enrichDetail` | boolean | Join each row with NAICS / set-aside / place of performance / contacts (default `false`). Opportunities only |
| `maxResults` | integer | Cap on rows returned (default `200`) |
| `watchLabel` | string | Optional. Name a saved search to get only records new since your last run under that label — see FAQ |
| `watchChanges` | boolean | Optional, requires `watchLabel`. Also re-deliver an already-seen record if a watched field changed — for opportunities: `isActive`, `noticeTypeCode`, `responseDate`, `modifiedDate`, `modificationsCount`, `awardeeName` or `description`; for wage determinations: `revisionNumber`, `isActive` or `modifiedDate`; for `assistance-listings`: `isActive`, `isFunded`, `modifiedDate` or `historicalIndexCount` (default `false`) — see FAQ |
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
- https://fetchsmith.com/blog/sam-gov-key-free-federal-datasets-one-endpoint
- https://fetchsmith.com/blog/usaspending-federal-awards-json-api
- https://fetchsmith.com/blog/grants-gov-federal-grant-opportunities-json-api
- [We nearly charged our own buyers twice for rows they'd already paid for](https://fetchsmith.com/blog/watch-baseline-eviction-rebilling) — a capped watch-mode baseline can silently evict old-but-current ids on a high-volume run, re-delivering (and re-billing) rows already paid for.
- https://fetchsmith.com/tools

## Source code
https://github.com/Fetchsmith/fetchsmith/tree/main/actors/sam-gov-opportunities-scraper

More tools: [fetchsmith.com/tools](https://fetchsmith.com/tools) — 22 HTTP-only Actors for public data sources, no browser required.
