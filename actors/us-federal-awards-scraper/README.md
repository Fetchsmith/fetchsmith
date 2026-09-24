# USAspending — US Federal Contracts, Grants & Subawards Scraper

Search **every US federal award** — contracts, IDVs, grants, direct payments, other financial assistance and loans — straight from the official **USAspending.gov** awards API, and get flat JSON rows you can drop into a CRM, a spreadsheet or a model.

No API key, no login, no proxy: this Actor uses the US government's public open-data API (`api.usaspending.gov`), so the data is authoritative and there is nothing to violate. Awards data covers recipients (companies, universities, state agencies), not individuals.

## What you can do with it

- **Federal-contractor lead lists** — every company that won work from a given agency, with UEI, address and NAICS/PSC codes.
- **Competitor tracking** — pull one recipient's full award history by exact name (`recipients`) and watch amounts, agencies and end dates (recompete timing).
- **Grant prospecting** — filter to grants and cooperative agreements by CFDA/Assistance Listing program and state.
- **Market sizing** — how much a given agency obligated on solar, cyber, AI or any keyword over any window since 2007.
- **Recompete alerts** — `expiringWithinDays` finds contracts, grants and IDVs whose period of performance ends soon (a real re-bid/renewal radar), and `expiringAfterDays` skips anything ending too soon to realistically bid on.
- **Single-award lookup** — already have a PIID/FAIN/URI from a solicitation or a news story? `awardIds` fetches that exact award, ignoring every other filter.
- **Pass-through grant tracing** — `fundingAgencies` finds awards where the money's actual source agency differs from the agency that administers the award (common on formula/block grants routed through a state).
- **Sub-award / subcontractor mining** — set `awardLevel` to `subaward` and get the FSRS sub-contracts and sub-grants filed *under* prime awards: who the prime contractor actually paid, how much, and for what. Every sub-award row carries the prime award's ID and URL, so you can join it straight back to a prime-level run. This is the tier-2 supplier list that never appears in prime-award data.
- **New-award alerts** — set `watchLabel` on a saved search (any filter combination, prime or sub-award mode) to get only the awards/sub-awards that are new since your last run, instead of re-pulling the same agency/NAICS/recipient search on a schedule.
- **Award-change alerts** — add `watchChanges` (prime mode) to also get re-alerted when an already-delivered award's last-modified date, amount, outlays or end date moves — contract modifications, option exercises, period-of-performance extensions — instead of only ever hearing about brand-new awards.
- **Opportunity triage** — set `includeOpportunityScore` to add a 0-100 score to every row so you can sort a big pull by "worth pursuing" instead of just amount — see [Opportunity score](#opportunity-score).

## Input

| Field | Type | Default | Notes |
|---|---|---|---|
| `startUrl` | string | – | Paste a usaspending.gov Advanced Search "share" link (`usaspending.gov/search?hash=...` or `usaspending.gov/search/...`) instead of picking `keywords`/`awardCategories` by hand — this resolves the site's own saved-search hash via its public `/api/v2/references/hash/` endpoint and applies its keyword and award-type filters, overriding those two inputs. Agency/location/NAICS/PSC/award-amount/date-range filters set in that search are **not** carried over yet (no live example was available to confirm their nested shapes against) — a warning in the run log names any of those it finds so you can set the matching input yourself. |
| `awardLevel` | string | `prime` | `prime` = the federal award itself. `subaward` = the sub-contracts/sub-grants reported under prime awards. Every filter below works in both modes — see [Sub-award mode](#sub-award-mode). |
| `awardCategories` | array | `["contracts"]` | `contracts`, `idvs`, `grants`, `direct_payments`, `other_financial_assistance`, `loans`. Pick several — each is fetched separately and merged. |
| `startDate` / `endDate` | string | last 365 days | `YYYY-MM-DD`, passed to USAspending's award-level `time_period` filter. It is a coarse recency bound, **not** a strict window — no date on the returned row is guaranteed to fall inside it (measured; see the FAQ). Nothing exists before `2007-10-01`; earlier dates are clamped. |
| `keywords` | array | – | Free text over description, recipient and agency. Multiple keywords are ORed. |
| `recipients` | array | – | Free-text recipient name search, e.g. `Lockheed Martin`. Multiple values are ORed. |
| `agencies` | array | – | **Exact** top-tier *awarding* agency names, e.g. `Department of Energy`. Abbreviations like `DOE` match nothing. |
| `fundingAgencies` | array | – | **Exact** top-tier *funding* agency names — the agency whose budget pays, which can differ from `agencies` on pass-through grants. Same exact-name rule. |
| `awardIds` | array | – | Exact PIID/FAIN/URI values, e.g. `N0001917C0001`. **Exclusive mode**: set this and every other filter (including the date window) is ignored so the exact award can never be hidden by an unrelated filter. |
| `placeOfPerformanceStates` | array | – | Two-letter USPS codes for where the work happens (`CA`, `TX`). |
| `recipientStates` | array | – | Two-letter USPS codes for the recipient's own address. |
| `recipientTypes` | array | – | USAspending business-type categories, e.g. `small_business`, `woman_owned_business`, `veteran_owned_business`, `minority_owned_business`, `nonprofit`, `higher_education`, `sole_proprietorship`, `manufacturer_of_goods` (live-verified 2026-09-18; USAspending has more categories beyond these). Multiple values are ORed. A misspelled category returns zero rows silently — check spelling against USAspending's advanced search if a run comes back empty. |
| `naicsCodes` | array | – | NAICS industry codes, 2-6 digit prefixes (`5415` matches every 6-digit code under it). Multiple values are ORed. No effect on grants/direct payments/other financial assistance/loans — they carry no NAICS. |
| `pscCodes` | array | – | Product or Service Codes (PSC), 1-4 character prefixes (`R425` one leaf code, `R4` every professional-services code, `R` the whole services letter, `10` every weapons product). Multiple values are ORed. Only contracts and IDVs carry a PSC, so grants/loans/direct payments return nothing. |
| `minAwardAmount` / `maxAwardAmount` | integer | – | Obligated amount bounds in USD. |
| `expiringWithinDays` | integer | – | Recompete finder: only awards whose period of performance ends within this many days from today. Prime mode, contracts/grants/IDVs only (not loans, not sub-awards — neither reports a period-of-performance end date). Applied after fetching, since USAspending's own filters can only search by award *action* date, not end date. |
| `expiringAfterDays` | integer | – | Skip awards expiring sooner than this many days out — bid lead time. Requires `expiringWithinDays`, and must be smaller than it. |
| `sortBy` | string | `awardAmount` | `awardAmount`, `lastModifiedDate`, `startDate`, `recipientName`. |
| `order` | string | `desc` | `desc` or `asc`. |
| `maxResults` | integer | `100` | Total across all selected categories. |
| `maxPagesPerCategory` | integer | `50` | Depth cap, 100 awards per page. |
| `watchLabel` | string | – | Set a name for this saved search to turn on watch mode — see [Watch mode](#watch-mode) below. |
| `watchChanges` | boolean | `false` | Prime mode only. Also re-alert (and charge) on an already-delivered award whose last-modified date, amount, outlays or end date changed — see [Watch mode](#watch-mode). |
| `includeOpportunityScore` | boolean | `false` | Prime mode only. Adds a 0-100 `opportunityScore` field to every row — see [Opportunity score](#opportunity-score). |
| `webhookUrl` | string | – | Optional. POST a small JSON completion summary (awards/sub-awards pushed, rows scanned, dataset ID, watch new/changed counts) here when the run finishes — see FAQ. |

All filters are ANDed. Awards filtered out are never pushed and never charged.

## Output

One flat row per award:

| Field | Example |
|---|---|
| `awardId` | `89243425FEE000489` |
| `awardUrl` | `https://www.usaspending.gov/award/CONT_AWD_89243425FEE000489_8900_…` |
| `awardLevel` | `prime` — lets you tell a prime row apart from a `subaward` row (below) after merging runs from both modes into one table. |
| `awardCategory` / `awardType` | `contracts` / `BPA CALL` |
| `recipientName`, `recipientUei`, `recipientId` | `ENERGY TECHNOLOGY ALLIANCE LLC`, `WDTLX4NKRKC8` |
| `recipientAddress`, `recipientCity`, `recipientState`, `recipientCountry` | `920 NW BOND ST STE 204`, `BEND`, `OR`, `UNITED STATES` |
| `awardingAgency`, `awardingSubAgency`, `fundingAgency`, `fundingSubAgency` | `Department of Energy` |
| `description` | `SCIENTIFIC, ENGINEERING AND TECHNICAL SUPPORT (SETS) FOR DOE EERE'S SOLAR ENERGY TECHNOLOGIES OFFICE…` |
| `awardAmount`, `totalOutlays` | `7909335.88`, `7909335.88` |
| `loanValue`, `subsidyCost` | loans only — face value and subsidy cost |
| `startDate`, `endDate`, `baseObligationDate`, `lastModifiedDate` | `2025-04-30`, `2026-04-30` |
| `placeOfPerformanceCity/State/Zip/Country` | `GOLDEN`, `CO`, `80401`, `USA` |
| `naicsCode`, `naicsDescription`, `pscCode`, `pscDescription` | `562910`, `REMEDIATION SERVICES`, `R425`, `SUPPORT- PROFESSIONAL: ENGINEERING/TECHNICAL` |
| `cfdaNumbers`, `cfdaProgramTitles` | grants/loans — e.g. `["93.778"]`, `["GRANTS TO STATES FOR MEDICAID"]` |
| `disasterEmergencyFundCodes` | `["Q"]` |

## Sub-award mode

With `awardLevel: "subaward"` the same six categories, the same date window and the same filters are applied to USAspending's sub-award (FSRS) data instead, and each row is one sub-contract or sub-grant:

| Field | Example |
|---|---|
| `awardLevel`, `kind` | `subaward`, `subaward` |
| `subAwardId`, `subAwardType` | `200155`, `sub-contract` |
| `subAwardDate`, `subAwardAmount` | `2025-05-30`, `1154736350` |
| `subAwardDescription` | `CONSTRUCTION SUBCONTRACT (CS)-111G BUILDING OUTFITTING` |
| `subRecipientName`, `subRecipientUei` | `KIEWIT POWER CONSTRUCTORS CO`, `CFCCZHPBR445` |
| `primeAwardId`, `primeRecipientName`, `primeRecipientUei`, `primeRecipientId` | `89233018CNR000004`, `FLUOR MARINE PROPULSION, LLC`, `CWHMVCX7K1N6` |
| `primeAwardGeneratedInternalId`, `primeAwardUrl` | `CONT_AWD_89233018CNR000004_8900_-NONE-_-NONE-`, `https://www.usaspending.gov/award/CONT_AWD_89233018CNR000004_8900_…` |
| `awardingAgency`, `awardingSubAgency`, `awardCategory` | `Department of Energy`, `Department of Energy`, `contracts` |

`primeAwardGeneratedInternalId` is the **same value** as a prime row's `generatedInternalId`, so the two modes join cleanly on it (or on `primeAwardUrl` = `awardUrl`).

Three things to know:

- **Filters retarget to the sub-recipient.** `recipients`, `recipientStates` and `recipientTypes` match the sub-awardee, not the prime contractor; `agencies`/`fundingAgencies`, `keywords`, `placeOfPerformanceStates`, `naicsCodes`, `pscCodes` and the amount bounds work as usual (matching the **prime** award's NAICS/PSC, since sub-awards carry neither of their own). `awardIds` matches the **prime** award ID and returns every sub-award filed under it — the fastest way to see who a given prime contractor subcontracted to.
- **`sortBy: lastModifiedDate` falls back to the sub-award date**, because sub-award records carry no last-modified timestamp.
- **Coverage is narrower than prime awards.** Only prime recipients required to file FSRS reports have sub-awards, so small awards, most loans and most direct payments return nothing here. An empty sub-award result does not mean the prime award doesn't exist — re-run with `awardLevel: "prime"` to confirm.

### Sample row

```json
{
  "awardId": "89243425FEE000489",
  "awardUrl": "https://www.usaspending.gov/award/CONT_AWD_89243425FEE000489_8900_89243423AEE000008_8900",
  "awardCategory": "contracts",
  "awardType": "BPA CALL",
  "recipientName": "ENERGY TECHNOLOGY ALLIANCE LLC",
  "recipientUei": "WDTLX4NKRKC8",
  "recipientCity": "BEND",
  "recipientState": "OR",
  "awardingAgency": "Department of Energy",
  "awardingSubAgency": "Department of Energy",
  "description": "SCIENTIFIC, ENGINEERING AND TECHNICAL SUPPORT (SETS) FOR DOE EERE'S SOLAR ENERGY TECHNOLOGIES OFFICE (SETO)",
  "awardAmount": 7909335.88,
  "totalOutlays": 7909335.88,
  "startDate": "2025-04-30",
  "endDate": "2026-04-30",
  "placeOfPerformanceCity": "GOLDEN",
  "placeOfPerformanceState": "CO",
  "naicsCode": "562910",
  "pscCode": "R425",
  "disasterEmergencyFundCodes": ["Q"]
}
```

## Watch mode

Set `watchLabel` to a name for a saved search, e.g. `"doe-solar-contracts"`. The first run for a given label + filter combination is a **free baseline**: it records every award (or sub-award, in sub-award mode) currently matching your filters and returns zero rows, charged nothing. Run the same label and filters again later — on a schedule, typically — and you get back only what's **new** since the last run; anything already delivered is skipped and not charged. Works in both `prime` and `subaward` mode: a prime-mode watch alerts on new awards matching your filter, a sub-award-mode watch alerts on new sub-contracts/sub-grants filed under it (including under an exact `awardIds` lookup, e.g. "tell me when this prime contractor subcontracts something new").

Changing any filter (categories, keywords, agencies, recipients, states, NAICS/PSC codes, amount bounds, or award IDs) starts a fresh baseline under that label. Leaving `startDate`/`endDate` on their rolling defaults (last 365 days / today) does **not** — those inputs move on their own every day, so pinning the baseline to their resolved value would force a fresh baseline daily; only an *explicitly set* start or end date counts toward the fingerprint. `maxPagesPerCategory` is your own scan-depth cost cap, so it's left alone on incremental runs, but a baseline run scans deeper than it (up to 1,000 pages per category) so a small cap set for normal runs can't make the baseline miss awards that exist right now.

**Baseline size cap.** A baseline holds up to **20,000** ids in one saved record. If a label's baseline grows past that, the oldest-first-seen ids are dropped — and a dropped id is no longer recognised, so it comes back as "new" on a later run **and is charged again**. The run that drops them says so explicitly: a warning in the log, a note on the run's status message, and `baselineTruncated` / `baselineTruncatedTotal` (this run / the whole life of the label) on the `webhookUrl` payload and the saved record. If you see it, narrow the watch query (agencies, keywords, state, `minAmount`, the date window, `awardTypes`) or split it across several labels so each baseline stays under the cap. A baseline run also stops recording at 20,000, and already warns separately when it hits that.

**`watchChanges` (prime mode only)** turns on a second kind of alert: an award that was already delivered under this label is re-delivered (charged again) if it changed since you last saw it — USAspending's own `lastModifiedDate` moved, or `awardAmount`/`totalOutlays` (contracts and assistance), `loanValue`/`subsidyCost` (loans), or `endDate` differ from the stored snapshot. The re-delivered row is tagged with `_watchChangeType` (which field(s) moved) and `_watchPrevious` (their old value(s)), so you don't have to diff it against your own last-seen copy. Not offered in sub-award mode — a sub-award is a static FSRS filing with no reliable "this changed" signal to track, so setting the flag there is a no-op (logged, not silently ignored). Every award's snapshot is refreshed on every run regardless of the flag, so turning `watchChanges` on later only detects drift from that point forward, never a backlog against changes it never captured.

## Opportunity score

Set `includeOpportunityScore` (prime mode only) to add a 0-100 `opportunityScore` field — a fixed, published formula, **never an AI/LLM call**, so it's fully reproducible from the row's own fields:

| Factor | Max points | How it's scored |
|---|---|---|
| Award size | 40 | Log-scaled on `awardAmount`, so a $50M+ mega-award doesn't swamp every other factor the way a linear scale would. $0 scores 0; $50M+ scores the full 40. |
| Tech/priority-sector keyword match | 25 | 25 if `description`/`naicsDescription`/`pscDescription` contains one of your own `keywords` (if you set any — it already searched on them), otherwise a fixed list: AI, machine learning, cyber(security), cloud, solar/renewable/clean energy, quantum, robotics, autonomous, biotech, semiconductor, data analytics. Otherwise 0. |
| Award category | 15 / 12 / 8 / 6 / 5 / 4 | IDVs (15) and contracts (12) score highest — an ongoing multi-year vehicle or a re-biddable contract is a real business-development target; grants (8), other financial assistance (6), direct payments (5) and loans (4) score lower since this formula is aimed at pursue/recompete opportunities, not funding awards. |
| Recompete urgency | 20 | Scales from 20 (ending today) down to 0 (365+ days out, or already past its end date), same `endDate` math as `expiringWithinDays` above. |

Off by default, so it never changes the default row shape. Prime mode only — sub-award records report no period-of-performance end date to score urgency from, so setting the flag in `awardLevel: "subaward"` mode is a no-op (logged, not silently ignored), same pattern as `expiringWithinDays`.

## Pricing

Pay per result: **$0.004 per award on the free plan, dropping to $0.0025 on Gold and above** (Bronze $0.0035, Silver $0.003), **no Actor-start fee**. You only pay for awards actually written to the dataset.

## FAQ

**Why can't I mix contracts and grants in one search on USAspending's own site?**
You can here. The underlying API rejects a request whose `award_type_codes` span two groups (`must only contain types from one group`), so this Actor runs one query per category you select and merges the results into a single dataset, deduplicated by the award's stable internal id.

**Why did my search return zero awards?**
The filters are ANDed. A keyword plus a state plus a minimum amount over a short window is often genuinely empty — drop one filter first. The other common cause is an agency name that isn't the exact top-tier spelling (`Department of Energy`, not `DOE`).

**How do I filter by PSC, and where do I find the code?**
`pscCodes: ["R425"]`. PSC is a 4-level hierarchy and you can stop at any level: `R` (all services), `R4` (professional services), `R425` (engineering/technical support). Product codes are numeric (`10` weapons, `1005` guns through 30mm); R&D codes start with `A` (`AA` agriculture R&D, `AA1`, `AA11`). Codes are case-insensitive here — `r425` is uppercased for you. Browse the live tree at `api.usaspending.gov/api/v2/references/filter_tree/psc/`.

**My `pscCodes` run came back empty — why no error?**
A PSC that is well-formed but doesn't exist returns zero rows rather than failing, so a typo looks like "no matching awards". The run log prints `pscCodes=[...]` exactly as sent; check it against the tree above. Also remember PSC only exists on contracts and IDVs — combining `pscCodes` with `awardCategories: ["grants"]` is always empty by definition.

**How far back does the data go?**
`2007-10-01`. The API refuses earlier start dates, so this Actor clamps them instead of failing.

**Are loan amounts in `awardAmount`?**
No. Loans report `loanValue` (face value) and `subsidyCost` instead of an obligated amount — that is how the API models them, and both fields are passed through unchanged.

**Why does `startDate` on a row show a date decades before my search window?**
Because `startDate`/`endDate` are not a strict window on anything the row shows. They are passed straight through to USAspending's award-level `time_period` filter, and that filter is looser than it looks. Measured live on 2026-09-21 (contracts, CA recipients, NAICS 541512, `minAwardAmount` 1,000,000): a **two-day** window (`2024-03-01`..`2024-03-02`) returned the *same* top awards as the whole of 2024 — including one whose period of performance ran 2018-05-15..2023-09-30 and whose 47 transactions contain no 2024 action date at all. Moving the window's *end* does change the result set (a 2026-09 window returns different awards); narrowing its *start* barely does.

So treat the window as a coarse recency bound, not a filter:

- Do not assume any date on the row falls inside it. In that same 10-row sample only 1 of 10 `lastModifiedDate` values did; the other 9 were *later* than the window.
- Filter precisely yourself on the date field you actually care about. `expiringWithinDays`/`expiringAfterDays` already do that for period-of-performance ends (before charging), and `sortBy: "lastModifiedDate"` orders by most recently modified.
- This is upstream behaviour, not something this Actor adds: the identical filters posted directly to `POST /api/v2/search/spending_by_award/` reproduce it exactly.

**How do I find contracts coming up for recompete?**
Set `expiringWithinDays` (e.g. `180`) to only get awards whose period of performance ends within that window — USAspending has no filter for this itself (its date filters only search by *action* date, not end date), so this Actor fetches normally and filters client-side on the `endDate` field it already returns for every contract/grant/IDV row, before charging. Add `expiringAfterDays` (e.g. `90`) to also skip anything ending too soon to realistically prepare a bid for. Neither applies to loans (no period-of-performance end date reported for that category) or `awardLevel: "subaward"` (sub-award records report no end date either) — both are warned and ignored rather than silently returning nothing.

**Is `opportunityScore` an AI/LLM score?**
No. It's a fixed formula over fields this Actor already returns — award size (log-scaled), a tech/priority-sector keyword match, award category, and recompete urgency from `endDate` — spelled out in full in [Opportunity score](#opportunity-score) above so you can reproduce or re-weight it yourself. No external call is made to compute it.

**Is this the same as SAM.gov?**
No. SAM.gov lists pre-award *opportunities* you can bid on; USAspending lists *awards already made*. This Actor covers awards — who won, how much, which agency, and when the work ends.

**Does it need a proxy?**
No. Plain HTTPS to a public government API, so runs are fast and cheap.

**Can I get alerted when an award I already know about changes, not just when a new one appears?**
Yes — set `watchChanges` alongside `watchLabel` (prime mode only). An award whose last-modified date, amount, outlays or end date has moved since you last saw it is re-delivered and charged again, tagged `_watchChangeType`/`_watchPrevious` with exactly what changed. Off by default, so a plain `watchLabel` only ever alerts on brand-new awards.

**Can I get alerted only when a new award appears, instead of re-pulling the same search?**
Yes — set `watchLabel`, see [Watch mode](#watch-mode). The first run records a baseline for free; every run after that on the same label and filters returns only what's new, and skips (without charging) anything already delivered.

**How does this compare to other USAspending scrapers?**
Checked against every competitor's real live `pricingInfos`, re-verified 2026-09-17. The two highest-traction players are both pricier than us at every buyer plan tier: `parseforge` (the most users of any competitor) charges **$0.012/result plus a $0.16 run-start fee** on the free plan ($0.008 + $0.05 on Gold and above), and `benthepythondev` charges **$0.005/result** on the free plan, tapering to $0.004 on Gold and $0.0035 on Diamond, plus a small start fee on every run. Ours is **$0.004/result on the free plan, $0.0025 on Gold and above, and no start fee at all**. Two low-traction entrants are cheaper per row — `copious_atoll` at $0.001/result and `themineworks` at $0.001 tapering to $0.0006 — but `themineworks` has already scheduled a **$0.005 run-start fee** to take effect 2026-09-22, and its own listing advertises "18 Fields"; this Actor returns **37 typed fields across 6 award categories** (contracts, IDVs, grants, direct payments, other financial assistance, loans), each category with its own correct field mapping (loans carry `loanValue`/`subsidyCost`, not `awardAmount`) rather than one generic shape stretched across every award kind.

**How is `webhookUrl` different from Apify's own platform webhooks?**
Apify's platform webhooks are configured separately per Task/Actor via the Console or the Webhooks API — useful if you already live in the Apify Console, but extra setup if you're calling this Actor's API directly and just want a completion ping. `webhookUrl` is a plain input field: set it on the run itself and it POSTs a JSON body (`actorRunId`, `defaultDatasetId`, `finishedAt`, `pushed`, `scanned`, and — if `watchLabel` is set — `watchSeeding`/`watchNewCount`/`watchChangedCount`/`baselineTruncated`/`baselineTruncatedTotal`) once the run finishes and every row is already pushed and charged. It's best-effort — a slow or failing webhook only logs a warning, it never fails the run, changes the result set, or affects billing.

Source code: https://github.com/Fetchsmith/fetchsmith/tree/main/actors/us-federal-awards-scraper

## Related guides
Engineering write-ups behind this Actor:
- [The US publishes every federal award as JSON — but you can't ask for a contract and a grant in the same request](https://fetchsmith.com/blog/usaspending-federal-awards-json-api) — why each award type has its own field mapping, and how this Actor handles all six in one run.
- [Grants.gov's search API never returns an error — a typo in your filter just silently returns zero results](https://fetchsmith.com/blog/grants-gov-federal-grant-opportunities-json-api) — the pre-award side: opportunities you can still bid on, rather than awards already made.
- [Eight ways an "only new since last run" watch mode silently stops working](https://fetchsmith.com/blog/incremental-api-watch-mode-four-traps) — how `watchLabel`/`watchChanges` are built, and why a cheap id-only baseline still has to apply every client-side filter.
- [We nearly charged our own buyers twice for rows they'd already paid for](https://fetchsmith.com/blog/watch-baseline-eviction-rebilling) — a capped watch-mode baseline can silently evict old-but-current ids on a high-volume run, re-delivering (and re-billing) rows already paid for.

More tools: [fetchsmith.com/tools](https://fetchsmith.com/tools) — 19 HTTP-only Actors for public data sources, no browser required.
