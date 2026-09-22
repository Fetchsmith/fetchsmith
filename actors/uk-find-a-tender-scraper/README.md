# UK Public Sector Tenders — Find a Tender & Contracts Finder (OCDS API)

Search **UK public-sector procurement notices** — live tender opportunities, contract awards and pipeline notices — from **both official UK portals**, and get them back as flat, ready-to-use JSON rows in one merged, deduplicated feed.

- **Find a Tender (FTS)** publishes **above-threshold** contracts. It is an authoritative but thin feed — roughly 7–8 tender-stage notices a day.
- **Contracts Finder (CF)** publishes the far larger **sub-threshold** flow — the sub-£139k central-government and sub-£214k wider-public-sector contracts that never reach Find a Tender. Typically ~18 tender-stage and 100+ award notices a day.

Searching only one portal means missing most of the UK market. This Actor queries both by default, normalizes them into a single row shape, dedupes them, and tags every row with a `source` field (`fts` / `cf`) so you always know which portal it came from.

Both portals speak [OCDS](https://standard.open-contracting.org/) — deeply nested release packages where the buyer's email is four levels down inside a `parties[]` array, the CPV codes are scattered across `tender.items[].additionalClassifications[]`, and the awarded value usually isn't on the award at all. The two portals also disagree in small ways (Contracts Finder has no lots and puts SME suitability and the contract period on the tender; Find a Tender puts them per lot). This Actor flattens and reconciles all of it into one row per notice.

**Post-Brexit UK notices are not in EU TED**, so this is additive coverage if you already track EU procurement (see our [EU TED Tenders Scraper](https://apify.com/fetchsmith/eu-ted-tenders-scraper)).

## What you get

One row per notice, including:

- **Buyer contact details** — `buyerName`, `buyerEmail`, `buyerPhone`, `buyerUrl`, full postal address and UK NUTS region. This is what turns a notice into a lead.
- **The opportunity** — `title`, `description`, `status`, `procurementMethod`, `mainProcurementCategory`, `legalBasis`.
- **Money** — `valueAmount` / `valueCurrency` for tenders; `awardValueAmount` / `awardValueCurrency` for awards.
- **Timing** — `deadlineDate` (submission deadline), `awardPeriodStart`, `contractStartDate`, `contractEndDate`, `contractDateSigned`.
- **Classification** — `cpvCode` + `cpvDescription` plus the full `cpvCodes` list gathered from every lot and item.
- **Lots** — `lotCount`, `lotTitles`, `suitableForSme`, `suitableForVcse` (read per-lot on Find a Tender, tender-level on Contracts Finder).
- **Awards** — `awardedSuppliers` (who won), `awardStatus`, `contractCount`.
- **Delivery** — `deliveryRegions` (NUTS codes) and `deliveryLocations` (free text).
- `source` / `sourceName` — which portal the row came from (`fts` / `cf`).
- `noticeUrl` — the public notice page on the portal it came from.

## Use cases

- **Bid pipeline / lead generation.** Filter to your CPV codes and `openOnly: true` and you get every live UK opportunity in your sector, with the buyer's email address attached.
- **Competitor intelligence.** Set `stages: ["award"]` to see who is winning contracts, for how much, from which buyers.
- **Market sizing.** Pull a year of awards for a CPV family and total the contract values.
- **Alerting.** Run on a schedule with `updatedWithinDays: 1` and push new matches into your CRM or Slack, or use `watchLabel` below to get only what's new automatically.

## Input

| Field | Type | Default | Notes |
|---|---|---|---|
| `sources` | array | `["fts","cf"]` | Which portals to search. `cf` = Contracts Finder (sub-threshold, high volume), `fts` = Find a Tender (above-threshold, thin). Both by default. |
| `stages` | array | `["tender"]` | `planning`, `tender` (opportunities) and/or `award` (winners). |
| `updatedWithinDays` | integer | `7` | Only notices published/updated in the last N days. Newest first. |
| `dateFrom` / `dateTo` | string | — | Absolute date window, e.g. `2026-08-01` (or a full ISO datetime). Setting either one **overrides** `updatedWithinDays`. Both portals enforce this server-side, so nothing is fetched and discarded. A bare date means midnight, so `dateTo: "2026-08-31"` excludes the 31st — use `2026-09-01` to include it. |
| `cpvCodes` | array | `[]` | e.g. `72000000`. A code matches its whole CPV subtree and nothing outside it — `72000000` matches every `72xxxxxx` code, `80000000` matches `80xxxxxx` only. Matched against every CPV on the notice, not just the headline one. |
| `searchQuery` | string | — | Every word must appear in title, description, buyer name, CPV description or lot titles (AND logic). |
| `keywordsAny` | array | `[]` | Alternative to `searchQuery` for OR logic: a notice matches if it contains **any** of these phrases (each can be multi-word) in the same fields. Use this to cover several unrelated opportunity types in one run, e.g. `["software", "IT support", "cyber"]` — `searchQuery` can only express AND-of-words within a single phrase. Set both if you want "any of these phrases, AND also these words". |
| `buyerName` | string | — | Case-insensitive substring match on the buying authority's name only, e.g. `NHS`, `Ministry of Defence`. Narrower than `searchQuery` — use it to get a buyer's own notices rather than every notice that mentions them. |
| `regions` | array | `[]` | OR-matched filter on delivery region/location text, e.g. `["London", "Scotland", "North West"]`. Matches against the notice's own `deliveryRegions`/`deliveryLocations`. Notices with no delivery-region data are excluded when this is set. |
| `minValueGbp` / `maxValueGbp` | integer | — | Contract-value bounds. Notices with no published value are excluded when either is set. |
| `openOnly` | boolean | `false` | Only notices whose submission deadline is still in the future. |
| `maxResults` | integer | `100` | Hard stop. |
| `maxPagesScanned` | integer | `50` | Safety cap on API pages read while looking for matches. Raise it for narrow filters over long date ranges. |
| `includeRawOcds` | boolean | `false` | Attach the complete, unmodified OCDS 1.1 release JSON as a `rawOcds` field on every row, alongside the normalized fields — for pipelines that want the full nested government data (all parties, all documents, amendment history), not just the flattened columns. |
| `watchLabel` | string | — | Turn this run into an **alert**: see "Watch mode" below. |
| `webhookUrl` | string | — | Optional. POST a small JSON completion summary (notices pushed, releases scanned/filtered, pages, dataset ID, watch new count, plus the full `RUN_SUMMARY` completeness object) here when the run finishes — see FAQ. |

### Example

```json
{
  "stages": ["tender"],
  "updatedWithinDays": 30,
  "cpvCodes": ["72000000"],
  "openOnly": true,
  "maxResults": 200
}
```

## Sample output (one row, trimmed)

```json
{
  "ocid": "ocds-h6vhtk-06f762",
  "noticeId": "086108-2026",
  "noticeUrl": "https://www.find-tender.service.gov.uk/Notice/086108-2026",
  "stage": ["tender"],
  "title": "Maryhill Housing Association - Heating Maintenance 2026 - 2031",
  "status": "active",
  "procurementMethod": "open",
  "mainProcurementCategory": "services",
  "cpvCode": "50720000",
  "cpvDescription": "Repair and maintenance services of central heating",
  "cpvCodes": ["50720000", "44621200", "44620000", "42160000"],
  "valueAmount": 710000,
  "valueCurrency": "GBP",
  "deadlineDate": "2026-10-12T17:00:00+01:00",
  "buyerName": "Maryhill Housing Association",
  "buyerEmail": "enquiries@maryhill.org.uk",
  "buyerPhone": "+44 1419462466",
  "buyerPostalCode": "G20 8RG",
  "deliveryRegions": ["UKM82"],
  "deliveryLocations": ["Maryhill & Ruchill areas of Glasgow"]
}
```

## Only what's new since last run (`watchLabel`)

A bid-monitoring job is a *subscription*, not a search: you want the notices published since you last looked, not the same hundreds of rows re-delivered (and re-charged) every morning.

Set `watchLabel` to a name for the query — `nhs-cleaning`, say — and this Actor keeps track of which notices it has already given you under that name:

- **The first run on a new label is a free baseline.** It scans both selected portals for everything currently matching your filters, records it, returns **zero** results and charges **nothing**.
- **Every run after that returns only the new notices.** Already-delivered rows are dropped before they are pushed or billed, so you never pay for the same notice twice — across either portal.
- **A notice counts as delivered only once it has actually been charged.** Anything cut off by `maxResults` or a charge limit stays "new" for the next run rather than vanishing.
- **Changing a filter starts a fresh baseline** — a different filter is a different question, so you don't get a dump of everything the old, narrower query happened to exclude.
- **The rolling `updatedWithinDays` window is deliberately *not* part of that identity.** It moves every day; if it counted, a daily schedule would re-seed forever and never deliver anything. `dateFrom`/`dateTo`, when you set them explicitly, do count.

The baseline lives in a key-value store named `fetchsmith-uk-tender-watch` on your own account, so it survives between runs and you can inspect or reset it yourself. Point an Apify schedule at the Actor and you have a UK procurement alert covering both portals.

**Baseline size cap.** A watch record holds at most **60,000** notice ids. Past that, the oldest ids fall off first — and a notice whose id has fallen off is no longer recognised as already-delivered, so a later run hands it over and **charges for it again**. As of v0.1.30 this is never silent: the run logs a warning, sets a status message in the Apify Console, records `truncatedLastRun`/`truncatedTotal` in the watch record itself, and reports `baselineTruncated`/`baselineTruncatedTotal` in `RUN_SUMMARY` and on the `webhookUrl` payload. All of them stay at `0` unless something was actually dropped. If you see a non-zero count, narrow the watch — a `cpvCodes` value, a `buyerName`, a shorter `updatedWithinDays`, or one portal in `sources` — so the result set stays under the cap. Note that the separate `seed-cap` bound (20,000) is what stops the *first* baseline walk; this cap is about the *stored* record growing over many runs.

## Pricing

**The first 25 matching records of every run are free.** After that, **$0.003 per result on the free plan, dropping to $0.0025 on Gold and above** (Bronze $0.0028, Silver $0.0026), no start fee. You are charged only for rows that actually land in your dataset — notices filtered out by `cpvCodes`, `searchQuery`, the value bounds or `openOnly` are **never charged**, even though the Actor had to read them from the API to decide.

## FAQ

**How do I know a run returned everything — and that "0 from Find a Tender" means that portal really had nothing?**
Every run writes a machine-readable `RUN_SUMMARY` record to its key-value store (v0.1.27+). Fetch it with no webhook needed:

```
GET https://api.apify.com/v2/actor-runs/<runId>/key-value-store/records/RUN_SUMMARY
```

```json
{
  "mode": "search",
  "sources": {
    "fts": { "label": "Find a Tender", "pages": 1, "scanned": 2, "delivered": 2,
             "exhausted": false, "failed": true, "lastError": "HTTP 503: Service Unavailable" },
    "cf":  { "label": "Contracts Finder", "pages": 2, "scanned": 4, "delivered": 4,
             "exhausted": true, "failed": false, "lastError": null }
  },
  "sourcesFailed": ["fts"],
  "delivered": 6, "filteredOut": 0, "pages": 3, "pageCap": 50, "undelivered": 0,
  "complete": false,
  "incompleteReason": "source-failed",
  "incompleteDetail": "Find a Tender stopped answering after 1 page(s) (HTTP 503: ...)"
}
```

The field that matters is **`sources.<portal>.exhausted`**: it is `true` only when that portal answered until its feed ran out. When it is `false`, that portal's `delivered` count is a **lower bound, not a total** — which is the whole point, because Find a Tender is a thin feed (~7–8 tender-stage notices a day), so a genuine `0` and a dead portal produce the same number. `complete: false` also sets the run's status message in the Apify Console, with `incompleteReason` one of `source-failed`, `page-cap`, `max-results`, `charge-limit`, `seed-cap` or `no-sources`. Reading both feeds to the end is **not** the same as delivering everything: a short date window often fits in one page per portal, so a run can exhaust both feeds and still be cut short by `maxResults` — when that happens `undelivered` is the exact number of matching notices that were fetched but not handed over (raise `maxResults` by that much to get them). A short run still **succeeds** — the notices it did return are real and already charged — so `complete` is the only reliable check. The same object is included as `summary` on the `webhookUrl` payload. On a `watchLabel` run the record also carries `baselineSize`, `skippedSeen` and `baselineTruncated`/`baselineTruncatedTotal` (see "Baseline size cap" above) — all `null` on a plain search run.

**What is the difference between the two portals?**
Find a Tender carries **above-threshold** UK public contracts (the post-Brexit replacement for the UK's TED publication), including Scotland, Wales and Northern Ireland. Contracts Finder carries the **sub-threshold** contracts below those limits — a much larger flow, and the one most SMEs actually bid on. They are separate systems with separate APIs; a contract normally appears on one or the other, not both. Rows are deduplicated on `ocid` and notice id regardless.

**Does `searchQuery`/`buyerName` handle accented words correctly?** Yes, as of v0.1.13 — both fields and the notice text they're matched against are Unicode-normalized before comparing, so an accented word matches regardless of which of Unicode's two equivalent representations (composed vs. decomposed) you typed it in.

**Does selecting more than one `stages` value work on Find a Tender?** Yes, as of v0.1.18 — Find a Tender's own API silently returns zero results for a comma-joined multi-stage value (it wants each stage as its own repeated query parameter), so any run with `stages: ["tender", "award"]` or similar came back empty from that portal only, with no error. Fixed; Contracts Finder was never affected. Also as of v0.1.18: `watchLabel` now tracks delivery per notice (`noticeId`), not per procurement (`ocid`) — neither portal ever edits a published notice in place, so a later award or amendment always arrives as a new notice sharing the original's `ocid`, and the old ocid-keyed baseline would have silently swallowed it as "already delivered".

**What's the difference between `searchQuery` and `keywordsAny`?** `searchQuery` is AND logic: every word in it must appear somewhere in the notice. `keywordsAny` is OR logic: the notice matches if it contains at least one of the phrases in the list. So `searchQuery: "IT support"` requires both words to appear (anywhere, not necessarily adjacent), while `keywordsAny: ["software", "IT support", "cyber"]` matches a notice mentioning any one of those three phrases — useful when you want everything across several related-but-different opportunity types without running the Actor three times. Set both together to combine them (AND of the `searchQuery` words, AND at least one `keywordsAny` phrase).

**How exactly does a `cpvCodes` entry match?**
A code matches its whole CPV subtree and nothing outside it. CPV is hierarchical — first 2 digits are the division, then group, class and category — and trailing zeros are padding, so `72000000` (IT services) matches every `72xxxxxx` code, and `72267000` also matches its children `72267100` and `72267200`. The division is the widest a filter can ever go: `80000000` returns education notices only, never `85xxxxxx` health ones. **Fixed in v0.1.25** — before that, a division code whose second digit is 0 (`30000000`, `50000000`, `60000000`, `70000000`, `80000000`, `90000000`) collapsed to a single digit and matched ten divisions at once. Measured on live data: `cpvCodes: ["80000000"]` returned 9 of 10 rows with no education CPV at all (they were `85xxxxxx` health and social work), and `["70000000"]` returned 0 of 10 rows in division 70 — engineering design, interpretation, R&D and payroll services instead. Codes like `72000000`, `45000000` and `85000000`, whose second digit is non-zero, were always correct. Note the subtree rule is the Actor's own client-side filter, applied to every CPV on the notice (headline plus all lot and item codes), so a notice qualifies if any one of its codes falls in the subtree.

**Why does a 10-day Find-a-Tender-only query only return ~75 notices?**
Because that is genuinely how many there are — Find a Tender carries roughly 7–8 new tender-stage notices a day, and none on weekends. This is exactly why the Actor searches Contracts Finder too by default. Widen `updatedWithinDays` (or use `dateFrom`/`dateTo`) for a bigger set, or leave `sources` at its default.

**In what order do results come back?**
Newest-first within each portal, but the two portals are interleaved row-by-row when both are selected — so even a small `maxResults` gets a mix of both instead of one portal filling the whole quota first. Set `sources: ["cf"]` or `["fts"]` if you want rows from only one portal.

**Why is `awardValueAmount` sometimes missing on award notices?**
Because the buyer did not publish a value. Where a value exists it is usually attached to the signed contract rather than the award, so this Actor reads `contracts[].value` and totals it (`contractCount` tells you how many contracts were summed, and `awardValueSource` says whether the number came from the award or the contracts).

**Why isn't there a `tenderStartDate` field?**
It used to exist (`tender.tenderPeriod.startDate` in the raw OCDS feed) but was removed as of v0.1.22 — measured 0/808 filled across 9 independent live slices spanning 2025-01 through 2026-08, on both Find a Tender and Contracts Finder, tender-stage and award-stage alike. UK buyers publish a submission deadline (`deadlineDate`) but essentially never publish a tender-window start date on either portal. `deadlineDate` remains, unaffected.

**Do you need a proxy or an API key?**
No. Both portals' OCDS APIs are free, key-free and open-licensed (Open Government Licence v3). The Actor self-throttles per portal to stay under each API's rate limit and backs off politely if it still hits one.

**Is this legal?**
Yes — it reads two official UK government open-data APIs under the OGL v3 licence. The contact details published on a notice are organisational procurement contacts, published by the buyer for exactly this purpose.

**Why did my first `watchLabel` run return nothing?** By design — the first run on a new label + filter combination is a baseline: it records everything currently matching so the *next* run can tell you what's new, and charges nothing.

**Can I reset or inspect a watch baseline?** Yes. It is a plain JSON record in the `fetchsmith-uk-tender-watch` key-value store on your own account, keyed by your label plus a fingerprint of your filters. Delete the record to start over, or read `seenIds` to see exactly what has been delivered.

**How is `webhookUrl` different from Apify's own platform webhooks?**
Apify's platform webhooks are configured separately per Task/Actor via the Console or the Webhooks API — useful if you already live in the Apify Console, but extra setup if you're calling this Actor's API directly and just want a completion ping. `webhookUrl` is a plain input field: set it on the run itself and it POSTs a JSON body (`actorRunId`, `defaultDatasetId`, `finishedAt`, `pushed`, `scanned`, `filtered`, `pagesScanned`, `summary` — the same object as the `RUN_SUMMARY` record — and, if `watchLabel` is set, `watchSeeding`/`watchNewCount`) once the run finishes and every row is already pushed and charged. Especially useful with `watchLabel` on a scheduled run: your endpoint gets told how many brand-new notices landed without polling the dataset. It's best-effort — a slow or failing webhook only logs a warning, it never fails the run, changes the result set, or affects billing.

## Source code

https://github.com/Fetchsmith/fetchsmith/tree/main/actors/uk-find-a-tender-scraper

## Related guides
Engineering write-ups behind this Actor:
- [The UK publishes every public contract as OCDS JSON — and the money isn't where you'd look](https://fetchsmith.com/blog/uk-find-a-tender-ocds-json-api)
- [When a dateTo filter silently excludes its own last day — and which government-data APIs actually do this](https://fetchsmith.com/blog/dateto-filter-silently-excludes-its-own-last-day)
- [Eight ways an "only new since last run" watch mode silently stops working](https://fetchsmith.com/blog/incremental-api-watch-mode-four-traps) — how `watchLabel` is built and the traps it has to avoid.

More tools: [fetchsmith.com/tools](https://fetchsmith.com/tools)
