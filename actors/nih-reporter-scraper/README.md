# NIH RePORTER Scraper – Federal Research Funding API, No 15k Row Cap, PubMed Join

Export **every NIH-funded research project** from the official [NIH RePORTER](https://reporter.nih.gov) API — 2.9M+ project records going back to 1985 — filtered by keyword, fiscal year, institute (IC), activity code, organization, state or principal investigator. Each project comes back with its award amounts, PI and program officer, institution, study section and congressional district, plus an optional join to **the PubMed papers that project produced**.

No API key, no login, no proxy. Public data only.

It is a grant data API for NIH RePORTER: pass a keyword, fiscal year or institute and get research grants data back as flat rows — award amount, PI, organization, administering institute, congressional district — with no web form, no pagination and no 15,000-row wall. NIH is the largest public funder of biomedical research in the world, so this is one of the broadest public sources of science funding data there is, and it is research funding data you can join directly to the PubMed papers each award produced. It behaves like a grant database API rather than a scraper: every field comes straight from NIH's own JSON.

## What it's for

- **Biotech / pharma competitive intelligence** — who is NIH-funded in your therapeutic area, at what dollar level, and which papers came out of it.
- **University research offices & grant consultants** — benchmark awards by institute, activity code (R01 vs R21 vs SBIR R43/R44) or peer institution.
- **Research-tooling and CRO sales teams** — find labs that just received a new (`awardType: "1"`) award in your space, with the institution and city attached.
- **Bibliometrics / science-of-science** — a funding-to-publication link for a whole field in one dataset.
- **COVID-19 research funding tracking** — NIH RePORTER carries **58,561 projects** matching COVID-19 in the title, terms or abstract (verified live via `keyword: "COVID-19"`); pair it with `fiscalYears` to see funding shift year over year as the pandemic response evolved.

## Three things this Actor does that the API doesn't

**1. It gets past the 15,000-row wall.** NIH RePORTER caps `offset + limit` at 15,000 and offers no cursor — a single fiscal year already holds 83,000+ projects, so a broad query is simply untraversable against the raw API. This Actor detects when a query exceeds the wall and automatically splits it across fiscal year, then administering institute, then award type, merging and de-duplicating on `appl_id` so you never pay twice for the same record.

**2. It refuses to silently ignore your filter.** NIH RePORTER accepts an unrecognised criteria *field name* with HTTP 200 and returns the entire unfiltered index as if the filter had worked — "success" that quietly means "everything". Every criteria key is validated against an allowlist before the request is sent, so a filter either applies or the run fails loudly. The same silent-empty-search trap exists one level down, on the *value* of `activityCodes`: a well-formed but nonexistent code (e.g. a typo like `R101`) gets HTTP 200 with zero matching rows, indistinguishable from a genuinely empty search. This Actor checks every supplied activity code against a live-observed list of ~201 real codes (sampled directly from NIH RePORTER's own data — NIH publishes no reference endpoint for this vocabulary) and warns in the run's log if one isn't recognised, though it still sends the value as-is in case it's a real, very-rare code our sample missed.

**3. It remembers what it already sent you (`watchLabel`).** Give a query a name — `watchLabel: "crispr-nci-weekly"` — and the Actor keeps a per-label record of the projects it has already delivered to you, so a scheduled run returns *only what is new since last time* and you are charged for nothing else. The first run on a new label is a **free baseline run**: it records what already matches, returns zero results, and charges nothing. Every run after that returns new projects only. This is your own baseline, not NIH's: `newlyAddedOnly` uses RePORTER's stateless "recently added to the index" flag, which keeps re-returning the same projects on every run until they age out of it. Change any other filter and the label starts a fresh baseline, so "new" always means new *for the exact query you are watching*.

- **`watchChanges` — also catch a no-cost extension, an administrative supplement, or a project ending.** Add this to `watchLabel` and a project you already have gets re-delivered (at the normal per-row price, tagged `_watchChangeType`/`_watchPrevious`) if its project end date, budget end date, award amount or active flag changes since you last saw it — not just brand-new projects. NIH itself confirms a no-cost extension updates the *same* award record's end date rather than minting a new `appl_id` (unlike a competing/non-competing renewal, which always gets a fresh `appl_id`), so this is a real, detectable signal, not a guess. Off by default so existing watches keep their current behavior.

### Skip the form: paste your RePORTER search URL (`startUrl`)

Build the search on reporter.nih.gov the way you normally would, then paste the address bar into `startUrl`:

```
https://reporter.nih.gov/search/FIJedD1bG0epAlP7QhG9lw/projects
```

That `search_id` in the path is a handle NIH stores on its own side, and NIH's public API accepts it in place of a criteria object — so the Actor runs *exactly* the search you built in the browser, including filters this Actor's own inputs don't expose. Any tab of a shared search works (`/projects`, `/charts`, `/publications`, …), and a bare search id on its own works too.

Two things to know:

- **A saved search replaces the filter fields, it does not combine with them.** NIH discards any criteria sent alongside a search id (silently — this Actor does not pass them and the run log names any you left filled in). `maxResults`, `includeAbstract`, `includePublications` and `watchLabel` still apply normally, and a `watchLabel` baseline is keyed to the specific search id, so two different pasted links never share one baseline.
- **NIH doesn't promise a shared link lives forever.** If a link stops resolving, the run fails with a message that says so instead of returning an empty dataset. Re-run the search on reporter.nih.gov and paste the fresh link.

The 15,000-row wall still applies to a pasted search and cannot be worked around: the automatic chunking below rewrites the query's filters, and a saved search doesn't expose any to rewrite. If your link matches more than that, the log says so — narrow it on reporter.nih.gov, or use the filter fields instead.

## Input

| Field | Type | Description |
| --- | --- | --- |
| `startUrl` | string | Paste a reporter.nih.gov search link instead of re-typing its filters — see below. **Replaces every filter field in this table** |
| `keyword` | string | Full-text over project title, abstract and NIH terms (default `"cancer"`) |
| `fiscalYears` | array | e.g. `[2024, 2025]`. Empty = all years |
| `agencyIcCodes` | array | Administering institute, e.g. `["NCI","NIAID"]` |
| `activityCodes` | array | Award mechanism, e.g. `["R01","R21","R43"]` |
| `awardTypes` | array | `1` new, `2` renewal, `3` supplement, `5` continuation, … |
| `orgNames` | array | Funded organization, partial match |
| `orgStates` | array | Two-letter US state codes |
| `piNames` | array | PI name contains, e.g. `["Doudna"]` |
| `minAwardAmount` | integer | Only awards of at least this many dollars (e.g. `1000000`) |
| `maxAwardAmount` | integer | Only awards of at most this many dollars — combine with the minimum for an exact band |
| `awardNoticeDateFrom` | string | Only projects officially awarded on/after this date, `YYYY-MM-DD` — see FAQ |
| `awardNoticeDateTo` | string | Only projects officially awarded on/before this date, `YYYY-MM-DD` — combine for an exact window |
| `projectNums` | array | Exact lookup — **ignores every other filter** |
| `activeOnly` | boolean | Currently active projects only |
| `newlyAddedOnly` | boolean | Only projects recently added to RePORTER — cheap incremental pulls |
| `watchLabel` | string | Name a saved query to get **only projects new since its last run** — see below |
| `watchChanges` | boolean | Optional, requires `watchLabel`. Also re-deliver an already-seen project if its end date, budget end, award amount or active flag changed (default `false`) — see FAQ |
| `webhookUrl` | string | Optional. POST a small JSON completion summary (projects pushed, watch new/changed counts, dataset ID) here when the run finishes — see FAQ. |
| `excludeSubprojects` | boolean | Drop P01/U54 subproject duplicates (default `true`) |
| `includePublications` | boolean | Join linked PubMed PMIDs (default `true`) |
| `includeAbstract` | boolean | Include abstract + public-health relevance (default `true`) |
| `maxResults` | integer | Stop after this many records (default 100) |

`projectNums` is an exclusive mode on purpose: looking up `R01CA234538` while a fiscal-year or institute filter is set would otherwise return zero rows, which is indistinguishable from a typo. Ask by number, get that project.

## Output

`applId`, `projectNum`, `coreProjectNum`, `subprojectId`, `fiscalYear`, `projectTitle`, `activityCode`, `awardType`, `fundingMechanism`, `awardAmount`, `directCostAmt`, `indirectCostAmt`, `isActive`, `isNew`, `projectStartDate`, `projectEndDate`, `budgetStart`, `budgetEnd`, `awardNoticeDate`, `dateAdded`, `agencyCode`, `icCode`, `icAbbreviation`, `icName`, `icFundings[]`, `opportunityNumber`, `cfdaCode`, `studySection`, `spendingCategoriesDesc`, `contactPiName`, `principalInvestigators[]`, `programOfficers[]`, `orgName`, `orgCity`, `orgState`, `orgCountry`, `orgZip`, `orgDeptType`, `orgUei`, `orgType`, `congDist`, `latitude`, `longitude`, `terms[]`, `url`, `abstractText`, `publicHealthRelevance`, `publicationCount`, `pubmedIds[]`

Sample row (trimmed):

```json
{
  "projectNum": "5R01CA279801-02",
  "coreProjectNum": "R01CA279801",
  "fiscalYear": 2024,
  "projectTitle": "Orthogonal CRISPR GEMMs",
  "activityCode": "R01",
  "awardAmount": 635830,
  "directCostAmt": 393703,
  "icAbbreviation": "NCI",
  "studySection": "Genomics, Computational Biology and Technology Study Section[GCAT]",
  "contactPiName": "MCMANUS, MICHAEL T",
  "orgName": "UNIVERSITY OF CALIFORNIA, SAN FRANCISCO",
  "orgState": "CA",
  "congDist": "CA-11",
  "publicationCount": 0,
  "pubmedIds": [],
  "url": "https://reporter.nih.gov/project-details/10794392"
}
```

### Field population — read this before you build on a field

Grant records (R/P/U/K/F activity codes) populate almost everything. **R&D contract records (`N01`, `funding_mechanism: "R and D Contracts"`) are much thinner** — verified live: `publicHealthRelevance`, `awardType`, `opportunityNumber`, `cfdaCode` and `studySection` all come back `null`, and `directCostAmt`/`indirectCostAmt` are usually absent on older rows too. Filter on `fundingMechanism` if you need a uniformly populated set.

`publicationCount` is legitimately `0` for many recent projects — papers take years to appear, so a 2024 new award usually has none yet. It is not a join failure. `publicationCount: null` means something different and is never mixed up with `0`: the PubMed lookup for that project didn't get an answer from NIH, so the count is *unknown*, not zero. The run log names every project it happened to and `RUN_SUMMARY.publicationLookupBatchesFailed` counts them.

## FAQ

**Does it need an NIH account or API key?** No. NIH RePORTER's API is fully public.

**How do I get more than 15,000 rows?** Just raise `maxResults`; the chunking is automatic. If a query is so broad that even chunking can't reach the rest, the log says so explicitly rather than silently truncating.

**Why does one project appear several times?** NIH RePORTER records one row per *fiscal year of funding*. `R01CA234538` returns six rows for its six funded years. De-duplicate on `coreProjectNum` if you want one row per project.

**Can I filter by award size?** Yes — `minAwardAmount` and `maxAwardAmount`, either alone or as a band. One caveat we measured rather than assumed: NIH RePORTER excludes projects with **no award amount recorded** from any amount-filtered query — about 2.8% of a 500-row FY2024 sample, matching a 2.6% drop in the reported total. So an amount filter is slightly narrower than "every project in that range"; the run log warns you whenever one is active.

**Does `activeOnly` narrow down a `fiscalYears` filter, or replace it?** It narrows it — this Actor handles it for you. We measured NIH RePORTER's own API live and found it **unions** `activeOnly` with `fiscalYears` server-side instead of intersecting them (on a narrow agency, ~6k FY2025-alone + ~7.6k active-alone combined into ~12.1k together — close to the sum, not a subset of either). Since build 0.1.4x, when you set both, this Actor no longer sends `include_active_projects` to NIH at all; instead it queries `fiscalYears` alone and filters `isActive === true` on the results itself, so you get the true intersection. The one side effect: the run may deliver fewer rows than `declaredMatches` reports (the same way `minAwardAmount`/`maxAwardAmount` above can), because `declaredMatches` describes NIH's count for the fiscalYears-only query, and the isActive filter narrows further on top of that. `newlyAddedOnly` never had this quirk; it correctly intersects with `fiscalYears` on NIH's side already.

**Can I filter by the actual award date instead of fiscal year?** Yes — `awardNoticeDateFrom`/`awardNoticeDateTo`, e.g. "grants awarded in June 2024". This is a different axis from `fiscalYears`: a project's NIH fiscal year rarely lines up with its calendar award date (a project awarded late in FY2024 might carry a notice date in mid-2024 but effective dates that read like FY2025). Both fields must be `YYYY-MM-DD` — NIH RePORTER's API silently ignores any other date format rather than rejecting it, so this Actor validates the format itself and fails the run loudly instead of quietly returning an unfiltered result set.

**How do I pull only what's new since my last run?** Two options. `watchLabel` is the precise one: name your query, and the Actor returns only the projects it has not already delivered under that name (first run = free baseline, zero results). `newlyAddedOnly: true` is the coarse one — RePORTER's own "recently added to the index" flag, about 8.9k projects index-wide when measured, almost all current-fiscal-year. Use `watchLabel` for a scheduled alert on a specific query; use `newlyAddedOnly` for a cheap sweep of whatever NIH just published. They combine fine.

**What does `watchChanges` add, and does it cost extra to turn on?** No extra fee — a changed project is billed at the same per-row price as a new one, so you only pay when there is actually something to see. Plain `watchLabel` only ever tells you about projects it has never delivered before; it stays silent forever about one it already sent you, even if NIH later grants a no-cost extension, processes an administrative supplement, or the project ends. Set `watchChanges: true` and each run also compares every already-delivered project's end date, budget end, award amount and active flag against what they looked like last time; if any moved, the row is re-delivered tagged with `_watchChangeType` (which field(s) changed) and `_watchPrevious` (what they used to be). This is a real signal, not a guess: NIH's own eRA Commons documentation confirms a no-cost extension updates the *same* award record's project period end date rather than creating a new `appl_id` — unlike a competing or non-competing renewal, which always gets a fresh `appl_id` per fiscal year. Verified live: seeding a baseline, editing 2 projects' recorded end date and active flag directly, then rerunning returned exactly those 2 rows with the correct change tags and nothing else — and a plain unchanged rerun after that returned 0 rows again. Existing watch labels created before this feature shipped work immediately; the first run under `watchChanges` just starts detecting drift from that point forward rather than reporting an artificial backlog.

**Where is the watch baseline kept, and can I reset it?** In a named key-value store, `fetchsmith-nih-watch`, **on your own Apify account** — one record per label + filter combination, holding the `appl_id`s already sent plus the last run time. Delete the record (or just use a new label) to start over. Nothing about your saved queries leaves your account. Two caveats worth knowing: a project that was skipped because it fell outside `maxResults` is *not* marked as delivered, so it comes back on the next run; and a baseline caps at 15,000 projects (RePORTER's own paging wall), so watch a query narrow enough to fit under that — the run log warns you if it doesn't.

**Baseline size cap.** Separately from the 15,000-project seeding wall above, the *saved record itself* holds up to **60,000** appl_ids for one label. If a long-running label's baseline grows past that, the oldest ids are dropped — and a dropped id is no longer recognised, so it comes back as "new" on a later run **and is charged again**. The run that drops any says so explicitly: a warning in the log, a note appended to the seeding/incremental log line, a status message on an otherwise-complete run, and `baselineTruncated`/`baselineTruncatedTotal` (this run / the whole life of the label) in the saved record and in `RUN_SUMMARY`. If you see it, narrow the query (a fiscal year, IC or state) or split it across several labels so each baseline stays under the cap.

**Is any personal contact data collected?** No. The NIH RePORTER schema contains no email or phone field at all. PI and program-officer **names** are included because they are statutory public disclosure, published on every reporter.nih.gov project page — the same class of data as a federal contract awardee's name.

**How do I know the run returned everything it should have — in code, not by reading the log?**
Every run writes a `RUN_SUMMARY` record to its key-value store, readable with no webhook set up:

```
GET https://api.apify.com/v2/actor-runs/<runId>/key-value-store/records/RUN_SUMMARY?token=<token>
```

```json
{
  "mode": "search",
  "declaredMatches": 19126,
  "reachableMatches": 19126,
  "unreachableMatches": 0,
  "scanned": 5,
  "delivered": 5,
  "pages": 1,
  "complete": false,
  "incompleteReason": "max-results",
  "incompleteDetail": "maxResults=5",
  "maxResults": 5,
  "chunksPlanned": 39,
  "chunksScanned": 1,
  "chunksEmpty": 0,
  "chunksCountFailed": 0,
  "publicationLookupBatchesFailed": 0,
  "watchLabel": null,
  "baselineSize": null,
  "baselineTruncated": null,
  "baselineTruncatedTotal": null
}
```

`declaredMatches` is NIH RePORTER's own `meta.total` for your filters, so `delivered` vs `declaredMatches` is the shortfall, computed against NIH rather than against our own paging. `complete: false` is not a failure — a run capped by `maxResults` is short on purpose — it means *don't treat this dataset as the whole answer*. `incompleteReason` is one of `max-results`, `charge-limit`, `seed-cap`, `offset-wall` (matches past NIH's hard 15,000-row paging wall), `count-request-failed`, `search-request-failed`, `empty-page-before-total`, `not-reached`. A short run also sets the Apify status message, so the shortfall is visible in the Console without opening the log.

**Important:** a number is never invented from a failure. If NIH doesn't answer a count query, `declaredMatches` is `null` — never `0` — and if it stops answering mid-walk the run says `search-request-failed` instead of reporting a partial page set as the complete result. The same rule applies to a chunked query: a sub-query whose count fails is paged anyway and counted in `chunksCountFailed`, so a single failed request can't quietly delete an entire NIH institute from your results.

**I run this on a schedule as a watch — what should my pipeline check?**
`complete`. A watch baseline (`mode: "watch-seed"`) that was cut short records fewer already-seen projects than really match, and every project it missed looks brand new — and gets charged — on the next incremental run. When that happens the run logs a `BASELINE INCOMPLETE` warning, sets `complete: false`, and stores `lastRunComplete: false` in the watch record, so re-seed before trusting the next run. On a healthy seed, `baselineSize` equals `declaredMatches`. Also check `baselineTruncated`/`baselineTruncatedTotal` (watch mode only) — a non-zero value means the 60,000-id record cap dropped older ids this run, and those will be re-delivered and charged again next run; see the "Baseline size cap" FAQ above.

**How is `webhookUrl` different from Apify's own platform webhooks?**
Apify's platform webhooks are configured separately per Task/Actor via the Console or the Webhooks API — useful if you already live in the Apify Console, but extra setup if you're calling this Actor's API directly and just want a completion ping. `webhookUrl` is a plain input field: set it on the run itself and it POSTs a JSON body (`actorRunId`, `defaultDatasetId`, `finishedAt`, `pushed`, the full `summary` object described above, and — if `watchLabel` is set — `watchSeeding`/`watchNewCount`/`watchChangedCount`) once the run finishes and every row is already pushed and charged. It's best-effort — a slow or failing webhook only logs a warning, it never fails the run, changes the result set, or affects billing.

## Pricing

`result` — **$0.0015 per returned item, no Actor-start fee.** There is nothing to pay before the first row arrives, and the price is flat: it does not depend on which Apify plan you are on.

**Where that sits in the niche (all prices read from each listing's live Apify pricing record, verified 2026-10-03).** A seven-term Store sweep finds that 51 Store listings mention NIH or RePORTER in their name, title or description (a deeper paginated sweep of the same terms reaches 53, our own two listings included), and we priced every one of them live. Most are more expensive than this Actor per row: `nexgendata/us-grants-funding-tracker` (61 users — the niche's largest listing by users) and `nexgendata/nih-reporter-grants-scraper` both charge $0.05 per award record, over 30× our price; `red.cars/nih-grants-mcp` charges $0.05 per grant search; `nexgenwatch/grant-funding-report` charges $15 per report plus a $0.05 start fee, and `nexgenwatch/nih-reporter-grant-award-delta` charges a mandatory $0.1 (Free) down to $0.067 (Gold and above) source-check fee on every run, on top of $0.15 (Free) down to $0.1005 (Gold and above) per award delta and a $0.02 start fee; `taroyamada/nih-grant-publication-output-report` ($0.008/row) and `taroyamada/nih-research-funding-landscape-report` ($0.005/row) both also sell $8–$15 report and export events; `scrapers_lat/usa-nih-reporter-scraper` is $0.012/row; `parseforge/nih-reporter-scraper` (3 users) is tiered $0.0065 (Free) down to $0.006 (Gold and above); `dataio/nih-reporter-funded-investigators` is $0.006/row and `devilscrapes/nih-reporter-grants-scraper` $0.006/row plus a $0.20 start fee; `crawlerbros` sells two listings, `crawlerbros/nih-reporter-scraper` and `crawlerbros/nih-reporter-grants-scraper`, both $0.005/row on the free plan tapering to $0.003 on Gold and above, each plus a $0.005 start fee; `scrapemint/nih-grant-finder`, `foo121/nih-reporter-scraper` and `thirdwatch/nih-reporter-projects-scraper` are all $0.004/row on the free plan; `tagadanar/us-grants-monitor` is $0.003 per award record plus a $0.001 start fee; `andrew_avina/nih-reporter-mcp`, `foxlabs/nih-reporter-organization-data` and `knotty_mistveil/nih-reporter-projects` are $0.003/row; `benthepythondev/nih-funded-projects-scraper` is $0.0025/row on the free plan ($0.00175 on Diamond); `chrisp1211/nih-grants-scraper-max` and `pink_comic/nih-reporter-search` are both $0.002/row, the latter plus a $0.0001 start fee; `fortuitous_pirate/nih-reporter-scraper` and `quarterly_jingo/nih-reporter-scraper` are $0.00186/row plus a $0.001 start fee; `maximedupre/nih-reporter` is $0.0018/row and `parseforge/nih-reporter-publications-scraper` is tiered $0.0018 (Free) down to $0.00163 (Diamond); and `caffein.dev/grants-actor` (3 users, never named before — reads NIH RePORTER plus Grants.gov and Duke Research Funding in one unified dataset) charges $0.002 per NIH/Grants.gov result plus a $0.00005 start fee. Against that set we are the cheapest per-row price. We do **not** claim to be the cheapest in the niche overall — seven listings beat us in real scenarios, and they are named below.

**What we do not claim.** We are not the cheapest option for every job. Seven rival listings genuinely beat us in specific situations, each one's pricing record read live and verified 2026-10-03. One is simply free: `constant_quadruped/research-grant-aggregator` (13 users — the second-largest listing in this sweep) carries no Apify pricing record at all, which means it runs on Apify's free pricing model and charges nothing per row beyond the platform compute your own account uses; it searches NIH, NSF, Grants.gov and USASpending in one query, so if price is your only criterion, start there. Two undercut our flat rate on ordinary runs: `themineworks/nih-reporter-grants` charges $0.001 per grant on Free, $0.0009 on Bronze, $0.00075 on Silver and $0.0006 on Gold and above, plus a $0.005 start fee — cheaper than us past roughly 10 rows per run on Free, 9 on Bronze, 7 on Silver and 6 on Gold and above; and `publicmoney/nih-reporter-grants-scraper` (4 users) prices its `Grant` event per Apify plan — $0.002 on Free, $0.0015 on Bronze (a tie with us), then $0.00125 on Silver, $0.001 on Gold, $0.00085 on Platinum and $0.0007 on Diamond — so on any paid Apify plan above Bronze it is cheaper per row than we are, though it adds a $0.00005 start fee. Four more trade a fixed per-run or per-scan fee for a near-zero row price, which wins on larger pulls: `datasignalslab/nih-research-funding-monitor` — previously misread by this README as a flat "$0.02/row" — actually charges that $0.02 **per organization or topic scanned**, not per row (its own event description says so), plus a separate $0.00001 per matched grant row and a $0.00005 start fee, which makes it cheaper than our flat $0.0015/row past roughly 14 grants returned per scan, the same headline-number trap documented elsewhere in this fleet; `jungle_synthesizer/nih-reporter-grants-publications-scraper` charges $0.10 per run plus $0.0005 per record, making it cheaper than us past roughly 100 rows; `alizarin_refrigerator-owner/nih-grants-api-research-funding-data-for-grants-publications` charges $0.10 per run plus $0.01 per search operation and only $0.00001 per row, making it cheaper than us past roughly 75 rows — about $0.12 against our $1.50 for a 1,000-row pull; and `zentrafoundry/nih-reporter-competitor-grant-win-alert` (repriced 2026-10-01) charges $0.01 per award scan plus $0.0001 per matched, saved or enriched award record, which on its published event prices works out cheaper than us past roughly 10 awards per run. If your workload is one big export and price per row is the only thing you care about, those are the honest alternatives. We are the better pick for small pulls and for repeated incremental runs where a per-run fixed fee is charged over and over (ours is $0.0015 flat with no start fee, so a 5-row watch run costs $0.0075 and nothing else), for anyone on Apify's Free or Bronze plan, and for the filtering, validation and change-detection described next — which is the real reason to pick this Actor over a cheaper row price.

Beyond price, this Actor adds award-amount/award-date range filters, an org-state filter, activity-code validation (with an unrecognised-code warning against a live-sampled 201-code list), an optional PubMed publication join, auto-chunking past the API's 15,000-row offset wall, and watch-mode change detection (new projects plus no-cost extensions/budget/status changes on ones you've already seen). We read every rival listing's public Store page while pricing it and found none that documents all of those together — though several document some of them, and `constant_quadruped/research-grant-aggregator` covers more *sources* than we do (NSF, Grants.gov and USASpending alongside NIH) rather than more depth within RePORTER. Every competitor price above re-verified live 2026-10-02.

## Notes

Only public data from NIH RePORTER's official API is collected. Issues or feature requests: support@fetchsmith.com. Also available as a hosted API at https://fetchsmith.com

## Related guides
- [Eight government JSON APIs that need no key — and the specific way each one lies to you](https://fetchsmith.com/blog/free-government-data-json-apis-no-key) — how this API's silent-failure shape compares across all eight free government JSON APIs we scrape.
- https://fetchsmith.com/blog/nih-reporter-grants-json-api
- https://fetchsmith.com/blog/nih-reporter-search-id-vs-criteria
- https://fetchsmith.com/blog/grants-gov-federal-grant-opportunities-json-api
- [Eight ways an "only new since last run" watch mode silently stops working](https://fetchsmith.com/blog/incremental-api-watch-mode-four-traps) — how `watchLabel` is built, why `newly_added_projects_only` is not the same thing, and the three-run test that proves a baseline is complete.
- [We nearly charged our own buyers twice for rows they'd already paid for](https://fetchsmith.com/blog/watch-baseline-eviction-rebilling) — a capped watch-mode baseline can silently evict old-but-current ids on a high-volume run, re-delivering (and re-billing) rows already paid for. Reproduced on this Actor, closed with truncation tracking.
- https://fetchsmith.com/tools

## Source code

https://github.com/Fetchsmith/fetchsmith/tree/main/actors/nih-reporter-scraper
