# FDA Recall Scraper API — Food, Drug, Device Enforcement Reports

Search every US FDA product recall from the official **openFDA enforcement API** — food, drug and device — and get it back as flat, typed JSON/CSV/Excel rows.

This Actor covers **all three FDA recall types in a single run and a single schema**, interleaved and tagged with `productType`, so a compliance sweep is one job instead of three. Drug recalls additionally come with the barcode identifiers you need to match a recall against your own catalogue: **NDC, package NDC, UPC**, brand and generic name, manufacturer and substance. Every row can also carry a `riskScore` (0-100) — a documented, deterministic severity/recency/scope formula, not a black-box "AI" claim. Name a `watchLabel` and every later run on the same saved search returns **only recalls new since the last run**, so a scheduled job never re-delivers or re-charges for the same recall twice; add `watchChanges` and it also catches a recall's **status changing** (e.g. Ongoing → Terminated) or **FDA reclassifying its severity** (e.g. Class II → Class I). At **$0.0035/result on the free plan and $0.0024 on Gold and above, with no start fee**, it undercuts every all-three-types competitor we checked — the highest-volume one charges $0.05/result for the same raw openFDA data (their live pricing re-verified 2026-09-17).

The openFDA enforcement API above is complete but slow — its newest reports typically lag the real recall announcement by **over a week** (measured 11 days on 2026-09-20), a gap every FDA-recall Actor on the Store shares, us included, because everyone reads the same lagging API. Set `includePressReleases: true` and this Actor also fetches FDA's own recall press-release feed, which had an item **9 days ahead** of the enforcement API in that same measurement — the recall the day FDA announces it, not the day the enforcement paperwork catches up.

No API key, no login, no browser. Public US government open data ([openFDA licence](https://open.fda.gov/license/)).

## What you can do with it

- **Retailers and distributors** — pull every Class I recall for your state or category and check it against the products you carry.
- **Compliance and QA teams** — monitor `status: "Ongoing"` recalls in your product category on a schedule, using `watchLabel` so each scheduled run returns only what's new; add `watchChanges` to also get alerted when a recall you already logged is upgraded to a more serious classification or is finally terminated.
- **Product-liability and personal-injury firms** — search recall reasons and firm names across the full history.
- **Pharmacy and healthcare** — match drug recalls to your inventory by **NDC or UPC**, not by fuzzy product-name matching.
- **Insurers and risk analysts** — build a recall time series by firm, classification or distribution pattern.
- **Newsrooms and researchers** — track "what got recalled this week" across all three FDA centres at once.

## Input

All fields are optional; with an empty input you get the last year of food, drug and device recalls, newest first.

| Field | Type | Description |
|---|---|---|
| `productTypes` | array | `food`, `drug`, `device`. Default: all three. Results are interleaved, not one type after another. |
| `dateField` | string | Which date `reportDateFrom`/`reportDateTo` filter on: `report_date` (default, when FDA published the report), `recall_initiation_date` (when the recall actually started), or `termination_date` (when it closed out). |
| `reportDateFrom` | string | Earliest date for the field above, `YYYY-MM-DD` or `YYYYMMDD`. Default: one year ago. |
| `reportDateTo` | string | Latest date for the field above. Default: today. |
| `classifications` | array | `Class I` (reasonable probability of serious harm or death), `Class II` (temporary/reversible), `Class III` (unlikely to cause harm). Empty = all. |
| `states` | array | Two-letter state codes of the **recalling firm**. Empty = all. |
| `countries` | array | Country names of the **recalling firm**, exactly as FDA writes them (`United States`, `Canada`, `Israel`, ...). Most recalls are US firms; foreign firms whose products entered the US market show up too. Empty = all. |
| `recallNumber` | string | Look up one recall by its exact FDA recall number, e.g. `F-1233-2022`. Overrides every filter above except `productTypes`, and automatically searches full history regardless of `reportDateFrom`/`reportDateTo`. |
| `eventId` | string | Look up every product recalled under one FDA event ID, e.g. `90105` (one event can cover several products, each its own row). Same override/full-history behaviour as `recallNumber`. |
| `status` | string | `Ongoing`, `Completed`, `Terminated`, `Pending`. Empty = all. `Pending` is in FDA's own vocabulary but has never appeared in openFDA's enforcement data (verified 2026-09-25) — expect zero rows if you select it. |
| `recallingFirm` | string | Filter to one firm, e.g. `Tyson Foods`. Narrower than `searchQuery`, which also matches product description and recall reason. |
| `city` | string | Filter to recalls whose recalling firm is in this city, e.g. `Chicago`. |
| `brandName` | string | **Drug recalls only.** Filter by drug brand name, e.g. `Nurtec`. openFDA only cross-references brand/generic/manufacturer name for drug recalls — food and device recalls never match these three filters. |
| `genericName` | string | **Drug recalls only.** Filter by generic/active-ingredient name, e.g. `ibuprofen`. |
| `manufacturerName` | string | **Drug recalls only.** Filter by manufacturer name, e.g. `Pfizer`. Not the same as `recallingFirm` (the firm that issued the recall, any product type) — a drug's manufacturer and the firm recalling it can differ. |
| `voluntaryMandated` | string | `Voluntary: Firm initiated` or `FDA Mandated` (rare, under 2% of recalls). Empty = both. |
| `searchQuery` | string | Free-text phrase matched against product description, reason for recall and recalling firm. |
| `order` | string | `desc` (newest first, default) or `asc` — sorts by whichever field `dateField` selects. |
| `maxResults` | integer | Total rows across all selected product types. Default 100. |
| `includeRiskScore` | boolean | Add the `riskScore` field (see Output/FAQ). Default `true`. |
| `includePressReleases` | boolean | Also fetch FDA's recall press-release feed — up to 9 days ahead of the enforcement API, but only a rolling ~20-item/few-weeks window (see FAQ). Default `false`. Automatically skipped, with a log warning, if you also set a filter the feed can't support (see FAQ). |
| `watchLabel` | string | Name a saved search to get only recalls new since this label's last run (see FAQ). Leave empty for the normal full-match-set behaviour. |
| `watchChanges` | boolean | Optional, requires `watchLabel`. Also re-deliver an already-seen recall if its `status` or `classification` changed (default `false`) — see FAQ. |
| `webhookUrl` | string | Optional. POST a small JSON completion summary (recalls pushed, rows scanned, dataset ID, watch new/changed counts) here when the run finishes — see FAQ. |

Filters are **ANDed**. A search query plus a state plus a classification over a short date window often has zero real matches — drop one filter and retry.

### Example: Class I food and drug recalls in California this year

```json
{
  "productTypes": ["food", "drug"],
  "classifications": ["Class I"],
  "states": ["CA"],
  "reportDateFrom": "2026-01-01",
  "maxResults": 500
}
```

## Output

37 fields per row. Every date is converted from openFDA's `YYYYMMDD` strings (or the press-release feed's RFC-822 timestamp) to ISO `YYYY-MM-DD`.

**All product types:** `source` (`"enforcement"` or `"press_release"`, see below), `productType`, `recallNumber`, `eventId`, `status`, `classification`, `voluntaryMandated`, `initialFirmNotification`, `recallingFirm`, `city`, `state`, `country`, `productDescription`, `productQuantity`, `reasonForRecall`, `distributionPattern`, `codeInfo`, `moreCodeInfo`, `reportDate`, `recallInitiationDate`, `centerClassificationDate`, `terminationDate`, `riskScore`.

**Drug recalls only** (see the FAQ): `brandName`, `genericName`, `manufacturerName`, `substanceName`, `productNdc`, `packageNdc`, `upc`, `applicationNumber`, `drugRoute`, `rxcui`, `unii`, `splSetId`.

**`includePressReleases` rows only** (`source: "press_release"`, see FAQ): `pressReleaseTitle` (the FDA headline, also duplicated into `productDescription`), `sourceUrl` (link to the FDA press release). Every field above that the feed doesn't carry — `recallNumber`, `classification`, `eventId`, `status`, `distributionPattern`, all drug-only fields, `riskScore` — is explicit `null` on these rows, never guessed.

**Watch-mode change fields, only on a `watchChanges` re-delivery:** `_watchChangeType` (array, one or both of `status`/`classification`), `_watchPrevious` (object with the previous value(s) for each changed field).

### Sample row (drug recall, trimmed)

```json
{
  "source": "enforcement",
  "productType": "drug",
  "recallNumber": "D-0785-2026",
  "eventId": "99584",
  "status": "Ongoing",
  "classification": "Class II",
  "voluntaryMandated": "Voluntary: Firm initiated",
  "initialFirmNotification": "Letter",
  "recallingFirm": "ACCORD HEALTHCARE, INC.",
  "city": "Raleigh",
  "state": "NC",
  "country": "United States",
  "productDescription": "Levothyroxine Sodium Tablets, USP, 200 mcg (0.2 mg), packaged in a) 90-count bottles (NDC 16729-457-15) and b) 1000-count bottles (NDC 16729-457-17), ...",
  "productQuantity": "N/A",
  "reasonForRecall": "Subpotent Drug",
  "distributionPattern": "Nationwide within the United States",
  "codeInfo": "a) Lot # D2402430, D2402431, Exp Date: 10/31/2026. ...",
  "reportDate": "2026-09-02",
  "recallInitiationDate": "2026-08-06",
  "centerClassificationDate": "2026-08-21",
  "terminationDate": null,
  "riskScore": 80,
  "brandName": "LEVOTHYROXINE SODIUM",
  "genericName": "LEVOTHYROXINE SODIUM",
  "manufacturerName": "Accord Healthcare Inc.",
  "substanceName": ["LEVOTHYROXINE SODIUM"],
  "productNdc": ["16729-447", "16729-458", "16729-448"],
  "packageNdc": ["16729-458-15", "16729-458-17"],
  "upc": ["0316729447157", "0316729449151"],
  "applicationNumber": "ANDA212399",
  "drugRoute": ["ORAL"],
  "rxcui": ["892246", "892251"],
  "unii": ["9J765S329G"],
  "splSetId": "a6233381-3043-4e9a-aaa6-a6b105e5142b",
  "pressReleaseTitle": null,
  "sourceUrl": null
}
```

### Sample row (`includePressReleases: true`, trimmed)

```json
{
  "source": "press_release",
  "productType": null,
  "recallNumber": null,
  "classification": null,
  "status": null,
  "recallingFirm": null,
  "productDescription": "GF Blends Recalls Truly AIP All Purpose Flour and Bread Mix, and EAT G.A.N.G.S.T.E.R. Flat Bread Pizza Mix Due to Potential Undeclared Wheat Gluten",
  "reasonForRecall": "GF Blends is recalling Truly AIP All Purpose Flour and Bread Mix and EAT G.A.N.G.S.T.E.R. Flat Bread Pizza Mix listed below due to potential undeclared wheat gluten. ...",
  "distributionPattern": null,
  "reportDate": "2026-09-18",
  "riskScore": null,
  "pressReleaseTitle": "GF Blends Recalls Truly AIP All Purpose Flour and Bread Mix, and EAT G.A.N.G.S.T.E.R. Flat Bread Pizza Mix Due to Potential Undeclared Wheat Gluten",
  "sourceUrl": "http://www.fda.gov/safety/recalls-market-withdrawals-safety-alerts/gf-blends-recalls-truly-aip-all-purpose-flour-and-bread-mix-and-eat-gangster-flat-bread-pizza-mix"
}
```

This press release was live in the feed on 2026-09-18 — 2 days before this Actor's enforcement-API rows for the same window were captured, and well before the recall would typically clear openFDA's own pipeline.

## Pricing

Pay per result: **$0.0035 per recall on the free plan, dropping to $0.0024 on Gold and above** (Bronze $0.003, Silver $0.0027), with no Actor-start fee. 1,000 recalls costs $3.50 on the free plan, $2.40 on Gold. You are charged only for rows actually delivered to your dataset.

## FAQ

**Why are the NDC/UPC/brand-name fields empty on my food and device rows?**
Because FDA only publishes them for drugs. The `openfda` block that carries those identifiers is populated on drug enforcement reports and empty on food and device ones — verified on live samples, not an assumption. The fields are always present in the schema so your CSV columns stay stable; they are simply `null` or `[]` outside drug rows.

**In what order do results come back?**
Interleaved across the product types you selected — one row per type per round — so a small `maxResults` gives you a mix rather than filling the whole quota from `food`. Within each product type, rows are ordered by `reportDate`.

**What is the difference between `reportDate` and `recallInitiationDate`?**
`recallInitiationDate` is when the firm started the recall; `reportDate` is when FDA published the enforcement report, which is often weeks or months later. The date filters apply to **`reportDate` by default** — set `dateField: "recall_initiation_date"` to filter on when the recall actually began instead, or `"termination_date"` to find recalls that closed out in a window.

**Why is `terminationDate` almost always null, and `moreCodeInfo` too?**
Both are real openFDA fields, not bugs, and both are genuinely sparse — measured live, not assumed. `terminationDate` only gets a value once a recall's `status` flips to `Terminated`: sampled 30/30 Terminated-status rows filled across drug, food, and device, versus 0/30 for `Ongoing` and ~0-3% for `Completed`. Since the default sort returns the newest recalls first and most freshly-reported recalls are still `Ongoing`, `terminationDate` reads as almost-always-empty in a default query — set `status: "Terminated"` if you specifically want closed-out recalls with a termination date. `moreCodeInfo` is a free-text overflow field FDA rarely uses at all: sampled hundreds of rows with the field technically present in the API response, and it was an empty string in every drug and food row checked, non-empty in only a small fraction of device rows. Both fields are kept (not removed) because they are real, occasionally-populated upstream data, not an artifact of any input filter you chose.

**Can I get more than 25,000 rows from one filter?**
Yes. openFDA refuses to page past row 25,000 (`skip` is hard-capped), so when a query matches more than that the Actor automatically splits it into narrower `reportDate` windows and pages each one — the year-boundary split was verified to sum exactly to the unsplit total, with no duplicated or dropped rows. If one single window still exceeds the cap, the run logs a warning telling you to narrow the date range.

**Does `states` mean where the product was sold?**
No — it is the recalling firm's own state. For distribution, read the `distributionPattern` field (e.g. "Nationwide within the United States", or a list of states).

**I have a recall number or event ID from another source — can I just look it up directly?**
Yes. Set `recallNumber` (e.g. `F-1233-2022`) or `eventId` (e.g. `90105`) and every other filter is ignored except `productTypes` — set that too if you know which endpoint the recall lives on, since recall numbers aren't unique across food/drug/device. The date window is also automatically widened to full history so an old recall isn't silently missed by the default one-year lookback; this costs one extra lookup request internally, not a full history scan, since the exact-match query itself stays cheap however wide the window is.

**Is this legal / does it need an API key?**
It reads openFDA, the FDA's own public open-data API, which requires no key and is explicitly published for reuse. Rows are firm and product safety data, not personal data.

**My run returned zero rows.**
The log explains why in order of likelihood. Usually it is ANDed filters that have no real intersection, or a `reportDate` window that is too narrow. Try one distinctive word in `searchQuery` rather than a long phrase.

**What exactly is `riskScore` and why isn't it called "AI"?**
It's a plain weighted formula, computed with no external calls and no model: 45% classification severity (Class I=100, II=60, III=25), 30% recency (linear decay from 100 at today's date to 0 at two years old), 25% distribution scope (100 for nationwide/international language in `distributionPattern`, scaling down by how many distinct US state codes are mentioned, down to 30 for a single state/city). Rounded to an integer 0-100. We could have marketed this as "AI-powered" like a competitor does for the same idea, but it isn't AI, and saying so would be misleading — this is what it actually computes. Set `includeRiskScore: false` to skip it.

**How do I get only new recalls on a schedule, not the whole match set every time?**
Set `watchLabel` to any name, e.g. `"my-class-i-watch"`. The first run under that label is a free baseline: it records every recall currently matching your other filters and returns **zero rows, charged nothing**. Every later run with the same label AND the same other filters returns only recalls not already recorded — new since the last run — and only those are charged. Change any filter (a state, a classification, the date window) and that combination gets its own fresh baseline, since it's now a different saved search. The baseline lives in your own Apify account, not ours, so it survives between scheduled runs.

**Baseline size cap.** A baseline holds up to **60,000** recall ids in one saved record. If a label's baseline grows past that, the oldest ids are dropped — and a dropped id is no longer recognised, so it comes back as "new" on a later run **and is charged again**. The run that drops them says so explicitly: a warning in the log, a note on the run's status message, and `baselineTruncated` / `baselineTruncatedTotal` (this run / the whole life of the label) in the saved record, on the `webhookUrl` payload, and in `RUN_SUMMARY`. If you see it, narrow the watch query (`productTypes`, `states`, `classifications`, `searchQuery`, the date window) or split it across several labels so each baseline stays under the cap.

**Does changing `reportDateFrom`/`reportDateTo` from a rolling default break `watchLabel`?**
No — leaving both empty (the default one-year rolling window) is treated as "no explicit date filter" for the purpose of deciding whether your search changed, not as a specific date that changes every day. A recall that only enters the rolling window on a later run is correctly reported as new then, which is exactly what a watch should do.

**What does `watchChanges` add, and does it cost extra to turn on?**
No extra fee — a changed recall is billed at the same per-row price as a new one. Plain `watchLabel` only ever tells you about recalls it has never delivered before; it stays silent forever about one it already sent you, even if that recall later gets terminated or FDA upgrades it to a more serious class. Set `watchChanges: true` and each run also compares every already-delivered recall's `status` and `classification` against what they looked like last time; if either moved, the row is re-delivered tagged with `_watchChangeType` (which field(s) changed) and `_watchPrevious` (what they used to be). Verified live: seeding a baseline, editing 2 recalls' recorded status and classification directly, then rerunning returned exactly those 2 rows with the correct change tags and nothing else — and a plain unchanged rerun after that returned 0 rows again. Existing watch labels created before this feature shipped work immediately; the first run under `watchChanges` just starts detecting drift from that point forward rather than reporting an artificial backlog.

**What is `includePressReleases` and when should I turn it on?**
The openFDA enforcement API (everything else in this README) is the authoritative historical record, but it is slow: FDA finishes the paperwork and publishes the structured enforcement report anywhere from days to months after the recall is first announced (measured 11 days stale for the newest report on 2026-09-20). FDA's own recall press-release RSS feed carries the announcement itself, and had an item 9 days ahead of the enforcement API in that same check. Set `includePressReleases: true` to also pull that feed. Two things to know: (1) it's a **rolling window of the ~20 most recent press releases** (a few weeks of history), not an archive — use it for freshness, layered on top of the enforcement API's completeness, not as a replacement; (2) the same recall typically shows up **twice**, once as `source: "press_release"` within days of the announcement and again as `source: "enforcement"` weeks later once openFDA catches up — that is intentional (see the next question), not a duplicate-data bug, since there's no reliable shared key to merge them on.

**Why doesn't `includePressReleases` deduplicate against the enforcement rows?**
A press release and its later enforcement report share no common identifier — no recall number, no event ID, nothing but a firm name and a product description in free text, and fuzzy-matching those reliably enough to auto-merge risked silently dropping a real, distinct recall. We chose the safe failure mode: you may see the same real-world recall twice, tagged with two different `source` values and two different dates, rather than risk it being incorrectly merged away. Filter or dedupe downstream by firm/product text if your use case needs one row per recall.

**Why is `includePressReleases` sometimes skipped even when I turn it on?**
The press-release feed is unstructured — it has no classification, state/country, firm name field, drug identifiers, or product-type split (one feed covers food, drug and device announcements together). If you also set a filter that field depends on (`classifications`, `states`, `countries`, `status`, `recallingFirm`, `city`, `voluntaryMandated`, `brandName`/`genericName`/`manufacturerName`, an exact `recallNumber`/`eventId` lookup, `productTypes` narrowed to fewer than all three, or `dateField` set to anything but the default `report_date`), the Actor skips the press-release source entirely for that run and logs exactly which filter caused it, rather than silently returning zero press releases and letting you think none matched.

**How does this compare to other FDA recall scrapers?**
Checked live pricing and features again on 2026-09-15 against the highest-user leader (`benthepythondev/fda-recall-intelligence`, 11 users): they charge $0.05/result tapering to $0.035 on Diamond, **plus a per-GB Actor-start fee** — we are $0.0035/result on the free plan and $0.0024 on Gold and above, **with no start fee**, 10-20x cheaper at every tier. Their input set (8 fields) is a subset of ours (20 fields: three date-field choices instead of one, city, voluntary/mandated, free-text search across three fields, state and country, exact recall-number/event-ID lookup, drug-specific brand/generic/manufacturer name filters, and no 1,000-row cap — ours goes to 50,000). Their one real feature, an "AI-powered intelligence score", is now matched by `riskScore` above — ours is fully documented instead of a black box. Also checked against the real leader by volume (`scrapers_lat/openfda-food-recalls-scraper`, food-only, checked 2026-09-13, input-schema re-diffed 2026-09-17): they charge $0.01/result tapering to $0.008 on Gold+, **plus a separate $0.004→$0.001 Actor-start fee** — cheaper at every run size, and we cover drug and device recalls too, not just food. The 2026-09-17 re-check found `country`/`recallNumber`/`eventId` filters we lacked (they were already present as *output* fields, just not filterable on) — closed as `countries`, `recallNumber`, `eventId` above; a 2026-09-18 re-check of the same benthepythondev listing found `brandName`/`genericName`/`manufacturerName` were the same "computed-but-unfilterable" gap, closed the same way, so no remaining input-parity gap against either competitor. A 2026-09-20 audit found every FDA-recall Actor on the Store, including our own prior version, reads only the same lagging openFDA enforcement API — `includePressReleases` (above) is the one feature none of them currently has: the recall the week FDA announces it, not the week the enforcement paperwork catches up.

**How is `webhookUrl` different from Apify's own platform webhooks?**
Apify's platform webhooks are configured separately per Task/Actor via the Console or the Webhooks API — useful if you already live in the Apify Console, but extra setup if you're calling this Actor's API directly and just want a completion ping. `webhookUrl` is a plain input field: set it on the run itself and it POSTs a JSON body (`actorRunId`, `defaultDatasetId`, `finishedAt`, `pushed`, `scanned`, and — if `watchLabel` is set — `watchSeeding`/`watchNewCount`/`watchChangedCount`, plus the full `summary` object described in the next FAQ) once the run finishes and every row is already pushed and charged. Especially useful with `watchLabel`: your endpoint gets told how many brand-new or changed recalls landed without polling the dataset. It's best-effort — a slow or failing webhook only logs a warning, it never fails the run, changes the result set, or affects billing.

**How do I know the run returned everything that matched?**
Read the `RUN_SUMMARY` record from the run's key-value store — no webhook needed:

```
GET https://api.apify.com/v2/actor-runs/<runId>/key-value-store/records/RUN_SUMMARY?token=<token>
```

```json
{
  "finishedAt": "2026-09-22T12:03:58.593Z",
  "mode": "search",
  "declaredMatches": 14381,
  "scanned": 6,
  "delivered": 6,
  "complete": false,
  "incompleteReason": "max-results",
  "incompleteDetail": "Stopped at maxResults=6; matching recalls past this point were not returned.",
  "skippedSeen": 0,
  "changedCount": null,
  "baselineSize": null,
  "baselineTruncated": null,
  "baselineTruncatedTotal": null,
  "pressReleasesRequested": false,
  "pressReleasesIncluded": false,
  "productTypes": [
    { "productType": "food", "declaredMatches": 3976, "reachableMatches": 3976, "windowsPlanned": 1,
      "windowsScanned": 0, "scanned": 2, "delivered": 2, "skippedSeen": 0, "status": "ok",
      "complete": false, "incompleteReason": "max-results", "declaredMatchesIsFloor": false }
  ]
}
```

`declaredMatches` is openFDA's own `meta.results.total` for your filters, so `delivered` vs `declaredMatches` answers the question directly, per product type as well as for the run. Six rows against 14,381 matches looks exactly like a complete result set in the dataset — this is where you find out it isn't. `mode` is `search`, `watch-seed` or `watch-incremental`.

`complete` is deliberately **not** folded into `status`: a product type can be perfectly `ok` and truncated at the same time. `incompleteReason` is one of:

| Reason | Meaning |
|---|---|
| `max-results` | Your `maxResults` stopped the walk before the match set ran out. |
| `charge-limit` | The run's maximum-cost limit stopped it; raise the limit to get the rest. |
| `seed-cap` | A `watchLabel` seed hit the 20,000-recall cap. Narrow the query and re-seed, or the first incremental run reports recalls past the cap as new. |
| `skip-ceiling` | A single date window holds more rows than openFDA will page through (`skip` cannot exceed 25,000). Narrow `reportDateFrom`/`reportDateTo`. |
| `search-request-failed` | openFDA stopped answering mid-walk. Rows past that point were never scanned — this is **not** evidence they don't exist. |
| `plan-request-failed` | openFDA never answered the initial count query for a product type, so nothing of that type was scanned. That type's `status` is `not-scanned` and its `declaredMatches` is `null`, never `0`. |

The `null`-vs-`0` distinction is the point: `declaredMatches: null` means *we never got an answer*, while `0` means *FDA has no matching recall*. `declaredMatchesIsFloor: true` means the window plan itself was cut short, so the real total is higher. When anything is incomplete the run also sets a human-readable status message, visible at the top of the run in the Apify Console. `baselineTruncated`/`baselineTruncatedTotal` (watch mode only) report the "Baseline size cap" defect above — see that FAQ entry.

## Related guides
- [Eight government JSON APIs that need no key — and the specific way each one lies to you](https://fetchsmith.com/blog/free-government-data-json-apis-no-key) — how this API's silent-failure shape compares across all eight free government JSON APIs we scrape.
- [All FetchSmith scrapers](https://fetchsmith.com/tools) — 19 HTTP-only Actors for public data sources, no browser required.
- [The FDA publishes every product recall as JSON — but you can't page past row 25,000, and only drugs come with a barcode](https://fetchsmith.com/blog/fda-openfda-recall-json-api) — the full write-up of the 25,000-row skip cap, the date-chunking workaround and the drug-only `openfda` barcode fields.
- [Scraping USAspending's federal awards JSON API](https://fetchsmith.com/blog/usaspending-federal-awards-json-api) — the same "US government publishes it as keyless JSON" pattern, applied to federal contracts and grants.
- [Eight ways an "only new since last run" watch mode silently stops working](https://fetchsmith.com/blog/incremental-api-watch-mode-four-traps) — how `watchLabel` is built, why the rolling 365-day default never enters the criteria fingerprint, and why the seed walk pages at 1000 regardless of `maxResults`.
- [We nearly charged our own buyers twice for rows they'd already paid for](https://fetchsmith.com/blog/watch-baseline-eviction-rebilling) — a capped watch-mode baseline can silently evict old-but-current ids on a high-volume run, re-delivering (and re-billing) rows already paid for. Reproduced on this Actor, closed with truncation tracking.

Source code: https://github.com/Fetchsmith/fetchsmith/tree/main/actors/fda-recall-scraper
