# FEC Campaign Finance Scraper – Candidates, Donors, Committee Spending & Outside Money

Search US federal candidates (House, Senate, President) by name, state, office, party and election cycle, with each candidate's campaign financial totals — receipts, disbursements, cash on hand, individual contributions — in one row. Or switch `searchMode` to `contributions` to search individual donor contributions directly: donor name, employer, occupation, amount, date and receiving committee. Two more modes follow the money back out again: `disbursements` (Schedule B — every payment a committee made, to whom, when and what for) and `independentExpenditures` (Schedule E — outside spending *for* or *against* a named candidate, the super-PAC ad money). Powered by the FEC's official `api.open.fec.gov` disclosure API. No login, no browser, no API key of your own required.

## Use cases
- **Political/campaign research** — pull every Senate candidate in a state with their fundraising totals in a single dataset instead of clicking through fec.gov one candidate at a time.
- **Donor research** — search by donor name, employer, occupation, city or ZIP code (`searchMode: "contributions"`) to see every itemized federal contribution someone, some company's employees, or a whole profession has made, with amount, date and receiving committee.
- **Journalism & fact-checking** — compare receipts, burn rate (`disbursements` vs `receipts`) and war chests (`cashOnHandEnd`) across a race, with the FEC page URL attached to each row for citation.
- **Watchdog & transparency dashboards** — schedule a run per cycle and diff the totals to track who is raising money and how fast.
- **Small-dollar vs. large-dollar analysis** — `individualUnitemizedContributions` (small-dollar giving as the FEC itself computes it, no subtraction required) against `individualItemizedContributions` (the >$200-aggregate subset) shows how much of a campaign's money comes from grassroots donors versus large ones.
- **Candidate list building** — enumerate everyone who has ever filed for a given office/state/cycle, including long-shot and prior candidates.
- **Campaign vendor & burn-rate analysis** — `searchMode: "disbursements"` with `recipientName` shows who a campaign actually paid: ad buyers, consultants, payroll, venues, airlines. Filter by `committeeId` for one committee's whole ledger.
- **Outside-money / super-PAC tracking** — `searchMode: "independentExpenditures"` with `candidateId` and `supportOppose` separates money spent *supporting* a candidate from money spent *attacking* them, with the payee, the amount and the dissemination date on every row.
- **Donor alerts** — set `watchLabel` on a saved donor/employer search (contributions mode) to get only the contributions that are new since your last run, instead of re-scraping the same donors every time.
- **PAC vs. candidate-committee classification** — every contribution, disbursement and independent-expenditure row includes `committeeType`/`committeeDesignation`, the FEC's own official classification (e.g. `"Super PAC (Independent Expenditure-Only)"` vs. `"House"`), so you can tell what kind of committee moved the money without a separate lookup.

## Input
| Field | Type | Description |
|---|---|---|
| `searchMode` | string | `"candidates"` (default), `"contributions"` (Schedule A donations), `"disbursements"` (Schedule B committee spending) or `"independentExpenditures"` (Schedule E outside spending for/against a candidate). |
| `candidateName` | string | Candidates mode: full or partial name to search for (default `"Warren"`). Matches any part of the name — see the FAQ. |
| `donorName` | string | Contributions mode: donor name to search for, e.g. `"Elon Musk"`. |
| `donorEmployer` | string | Contributions mode: filter by the donor's self-reported employer, e.g. `"Google"`. |
| `donorOccupation` | string | Contributions mode: filter by the donor's self-reported occupation, e.g. `"Physician"`, `"Software Engineer"`. |
| `donorCity` | string | Contributions mode: filter by the donor's self-reported city, e.g. `"Seattle"`. |
| `donorZip` | string | Contributions mode: filter by the donor's self-reported ZIP code, e.g. `"90210"`. Matches both plain 5-digit and ZIP+4 records that start with it. |
| `recipientName` | string | Disbursements mode: who was paid, e.g. `"META"`, `"ActBlue"`. |
| `payeeName` | string | Independent expenditures mode: the vendor paid to run the ad/mailer. |
| `candidateId` | string | Independent expenditures mode: only spending naming this FEC candidate ID, e.g. `"P80001571"`. |
| `supportOppose` | string | Independent expenditures mode: `S` (spent supporting the candidate), `O` (spent opposing), empty for both. |
| `committeeId` | string | Disbursements / independent expenditures modes: only rows filed by this committee, e.g. `"C00744946"`. Ignored with a warning in contributions mode — the FEC's Schedule A endpoint times out on it. |
| `minAmount` | integer | Any transaction mode: only return rows at or above this dollar amount (contribution, disbursement or expenditure amount). |
| `maxAmount` | integer | Any transaction mode: only return rows at or below this dollar amount. Combine with `minAmount` for a range. |
| `contributionDateFrom` / `contributionDateTo` | string | Any transaction mode: `YYYY-MM-DD` window on the transaction date — contribution receipt date, disbursement date or expenditure date depending on the mode. Either or both may be set. A value that is not a real `YYYY-MM-DD` calendar date **stops the run** with an error naming it, rather than being ignored — ignoring a date bound would widen the search to every matching row and charge you for the difference. |
| `state` | string | 2-letter state code, e.g. `"CA"`. Candidates or donor address, depending on mode. Optional. |
| `office` | string | `H` (House), `S` (Senate), `P` (President). Candidates mode only. |
| `party` | string | Party code, e.g. `DEM`, `REP`, `IND`, `LIB`. Candidates mode only. |
| `electionYear` | integer | Even-numbered election cycle, e.g. `2024`. Candidates mode: optional, leave empty for all cycles. Contributions mode: required by the FEC API to keep the query fast — defaults to the current even year if left empty. |
| `includeTotals` | boolean | Candidates mode: fetch financial totals per candidate (default `true`). Costs one extra request per candidate. |
| `maxResults` | integer | Stop after this many rows (default `20`, max `500`). |
| `watchLabel` | string | Any transaction mode (contributions, disbursements, independentExpenditures). Set a name for this saved search to turn on watch mode — see "Watch mode" below. |
| `webhookUrl` | string | Optional. An http(s) URL to POST a small JSON completion summary to when the run finishes — see FAQ. |

### Example: donor research by employer

```json
{
  "searchMode": "contributions",
  "donorEmployer": "Google",
  "electionYear": 2024,
  "minAmount": 1000,
  "maxResults": 25
}
```

### Example: Massachusetts Senate Democrats in the 2024 cycle

```json
{
  "state": "MA",
  "office": "S",
  "party": "DEM",
  "electionYear": 2024,
  "includeTotals": true,
  "maxResults": 50
}
```

Leave `candidateName` empty to browse by filters alone instead of searching by name.

## Output

Row shape depends on `searchMode`: one item per candidate below, per contribution, per disbursement or per independent expenditure in the three transaction modes (each documented in its own section).

One item per candidate:

| Field | Description |
|---|---|
| `candidateId` | FEC candidate ID, e.g. `S2MA00170`. Stable across cycles — use it as your join key. |
| `name` | Name as filed, `LAST, FIRST MIDDLE`, uppercase. |
| `party` | Full party name, e.g. `DEMOCRATIC PARTY`. |
| `office` | `House`, `Senate` or `President`. |
| `state`, `district` | State code and 2-digit district (`00` for President, Senate and at-large House). |
| `incumbentChallenge` | `Incumbent`, `Challenger` or `Open seat` (`null` for some older filings). |
| `candidateStatus` | One-letter FEC code — see the FAQ for the decode table. |
| `electionYears` | Years this person has actually been a candidate for. |
| `cycles` | Every two-year cycle the FEC holds data for. Not the same as `electionYears`. |
| `firstFileDate` | Date of their first FEC filing. |
| `fecUrl` | Link to the candidate's page on fec.gov. |
| `receipts`, `disbursements` | Total raised and total spent for the covered period, in USD. |
| `cashOnHandEnd` | Cash on hand at the close of the covered period. |
| `individualContributions` | All contributions from individuals. |
| `individualItemizedContributions` | The itemized (>$200 aggregate) subset of the above. |
| `individualUnitemizedContributions` | The unitemized (small-dollar, ≤$200 aggregate) subset — the FEC's own computed figure, not derived by subtraction. |
| `refundedIndividualContributions` | Individual contributions refunded back to donors during the period. |
| `coverageStartDate`, `coverageEndDate` | The reporting period these totals cover, as ISO timestamps. |

Financial fields are `null` when `includeTotals` is `false` or the candidate has never filed a financial report.

### Contributions mode output

One item per itemized donor contribution:

| Field | Description |
|---|---|
| `contributorName`, `contributorEmployer`, `contributorOccupation` | Donor name and self-reported employer/occupation, as filed. |
| `contributorCity`, `contributorState`, `contributorZip` | Donor's reported city/state/ZIP. |
| `contributionAmount`, `contributionDate` | Amount in USD and the date the committee received it. |
| `contributorAggregateYtd` | This donor's running total given to the same committee this cycle, as computed by the FEC. |
| `committeeId`, `committeeName` | The receiving committee. |
| `committeeType`, `committeeDesignation` | The FEC's own committee classification, e.g. `"Super PAC (Independent Expenditure-Only)"`, `"PAC - Qualified"`, `"House"` (a candidate's principal committee) and `"Unauthorized"`/`"Principal campaign committee"`/`"Joint fundraiser"`. Straight from the FEC's own codes, not a guess — see the FAQ. |
| `candidateId` | The committee's associated candidate, when the committee is a candidate committee (`null` for PACs/parties). |
| `imageNumber`, `pdfUrl` | The FEC's own scanned-image identifier for the original filing, and a direct link to that PDF page — the primary source document behind the row. |

### Sample row, contributions mode

```json
{
  "contributorName": "SCHMIDT, KEITH",
  "contributorEmployer": "GOOGLE INC.",
  "contributorOccupation": "SOFTWARE ENGINEER",
  "contributorCity": "CHICAGO",
  "contributorState": "IL",
  "contributorZip": "606141234",
  "contributionAmount": 50.0,
  "contributionDate": "2024-12-31",
  "contributorAggregateYtd": 175.0,
  "committeeId": "C00019331",
  "committeeName": "DEMOCRATIC PARTY OF WISCONSIN FEDERAL",
  "committeeType": "Party - Qualified",
  "committeeDesignation": "Unauthorized",
  "candidateId": null,
  "imageNumber": "202609149904200417",
  "pdfUrl": "https://docquery.fec.gov/cgi-bin/fecimg/?202609149904200417"
}
```

### Disbursements mode output (Schedule B)

`searchMode: "disbursements"` returns one row per payment a committee reported making, 18 fields:

| Field | Description |
|---|---|
| `committeeId`, `committeeName` | The committee that made the payment. |
| `committeeType`, `committeeDesignation` | The FEC's own classification of that committee, e.g. `"House"`/`"Principal campaign committee"` for a candidate committee, `"PAC - Nonqualified"` for a PAC. |
| `recipientName`, `recipientCity`, `recipientState` | Who was paid, as filed. |
| `disbursementAmount`, `disbursementDate` | Amount in USD and the date of the payment. |
| `disbursementDescription` | The filer's own free-text purpose, e.g. `SOCIAL MEDIA ADVERTISEMENTS`. |
| `disbursementPurposeCategory` | The FEC's normalized purpose bucket, e.g. `ADVERTISING`, `OTHER`. |
| `disbursementCategory` | Category code decoded, when the filer supplied one (`null` is common). |
| `lineNumberLabel` | Which line of the form it was reported on, e.g. `Operating Expenditures`. |
| `candidateId`, `candidateName` | The candidate the payment relates to, when the filing names one. |
| `electionCycle` | The two-year transaction period the row belongs to. |
| `imageNumber`, `pdfUrl` | The scanned original filing and a direct link to it. |

```json
{
  "committeeId": "C00744946",
  "committeeName": "HARRIS VICTORY FUND",
  "committeeType": "PAC - Nonqualified",
  "committeeDesignation": "Joint fundraising committee",
  "recipientName": "META PLATFORMS, INC.",
  "recipientCity": "CHICAGO",
  "recipientState": "IL",
  "disbursementAmount": 5000000.0,
  "disbursementDate": "2024-06-26",
  "disbursementDescription": "ONLINE FUNDRAISING",
  "disbursementPurposeCategory": "OTHER",
  "lineNumberLabel": "Other Federal Operating Expenditures",
  "electionCycle": 2024,
  "pdfUrl": "https://docquery.fec.gov/cgi-bin/fecimg/?202407159661138582"
}
```

### Independent expenditures mode output (Schedule E)

`searchMode: "independentExpenditures"` returns one row per reported independent expenditure — outside money spent for or against a candidate, not coordinated with them — 23 fields:

| Field | Description |
|---|---|
| `committeeId`, `committeeName` | The super PAC or other committee that spent the money. |
| `committeeType`, `committeeDesignation` | The FEC's own classification — this is how you tell a `"Super PAC (Independent Expenditure-Only)"` from a `"Hybrid PAC"` or any other filer type without guessing from the name. |
| `candidateId`, `candidateName` | The candidate the spending is about. |
| `candidateOffice`, `candidateOfficeState`, `candidateParty` | `H`/`S`/`P`, the state of the race, and the candidate's party. |
| `supportOppose` | `"support"` or `"oppose"` — whether the money was spent for or against that candidate. |
| `payeeName` | The vendor paid to produce or place the ad/mailer. |
| `expenditureAmount` | Amount in USD. |
| `expenditureDate` | The date as filed. Occasionally mistyped by the filer (`3024-07-18` is real FEC data) — see the FAQ. |
| `disseminationDate` | When the communication actually ran. Usually the more reliable of the two dates. |
| `expenditureDescription`, `expenditureCategory` | What it was, as filed, plus the decoded category code when supplied. |
| `officeTotalYtd` | The committee's year-to-date total spent on that office, as computed by the FEC. |
| `electionType` | Primary/general/runoff, when supplied. |
| `filingForm`, `isNotice` | The form it arrived on (`F24` = a 24/48-hour notice, `F3X` = a periodic report), and whether this row is such a notice. |
| `electionCycle`, `imageNumber`, `pdfUrl` | Cycle and the original scanned filing. |

```json
{
  "committeeId": "C00804856",
  "committeeName": "REPUBLICAN ACCOUNTABILITY PAC",
  "committeeType": "Super PAC (Independent Expenditure-Only)",
  "committeeDesignation": "Unauthorized",
  "candidateId": "P80001571",
  "candidateName": "TRUMP, DONALD J",
  "candidateOffice": "P",
  "candidateParty": "REP",
  "supportOppose": "oppose",
  "payeeName": "EXTREME REACH, INC.",
  "expenditureAmount": 100.0,
  "disseminationDate": "2024-07-17",
  "expenditureDescription": "ADVERTISING - EXTREMEREACH AZ",
  "officeTotalYtd": 112395.99,
  "filingForm": "F24",
  "isNotice": true
}
```

### Sample row (real output, Elizabeth Warren, Senate)

```json
{
  "candidateId": "S2MA00170",
  "name": "WARREN, ELIZABETH",
  "party": "DEMOCRATIC PARTY",
  "office": "Senate",
  "state": "MA",
  "district": "00",
  "incumbentChallenge": "Incumbent",
  "candidateStatus": "C",
  "electionYears": [2012, 2018, 2024, 2030],
  "cycles": [2012, 2014, 2016, 2018, 2020, 2022, 2024, 2026],
  "firstFileDate": "2011-08-19",
  "fecUrl": "https://www.fec.gov/data/candidate/S2MA00170/",
  "receipts": 4413931.4,
  "disbursements": 4109645.05,
  "cashOnHandEnd": 3754333.02,
  "individualContributions": 4234605.7,
  "individualItemizedContributions": 1373252.85,
  "individualUnitemizedContributions": 2861352.85,
  "refundedIndividualContributions": 30368.08,
  "coverageStartDate": "2025-01-01T00:00:00",
  "coverageEndDate": "2026-06-30T00:00:00"
}
```

## Watch mode

Set `watchLabel` (any transaction mode: contributions, disbursements, independentExpenditures) to a name for a saved search, e.g. `"acme-corp-employees"`. The first run for a given label + filter combination is a **free baseline**: it records every contribution currently matching your filters and returns zero rows (charged nothing). Run the same label and filters again later — on a schedule, typically — and you get back only the contributions that are **new** since the last run; anything already delivered is skipped and not charged. Changing any filter — or the mode itself — starts a fresh baseline under that label.

Not available in candidates mode: it always returns the same fixed roster of people for a given filter set, not a stream of discrete new events, so "new since last time" has no natural meaning there — setting `watchLabel` alongside `searchMode: "candidates"` logs a warning and is ignored.

**Baseline size cap.** A baseline holds up to **20,000** ids in one saved record. If a label's baseline grows past that, the oldest-first-seen ids are dropped — and a dropped id is no longer recognised, so it comes back as "new" on a later run **and is charged again**. The run that drops them says so explicitly: a warning in the log, a note on the run's status message, and `baselineTruncated` / `baselineTruncatedTotal` (this run / the whole life of the label) on the `webhookUrl` payload and the saved record. If you see it, narrow the filters (donorName, donorEmployer, state, the amount window, the date window) or split the watch across several labels so each baseline stays under the cap.

## Pricing
`result` — you are charged per row actually returned (one candidate, contribution, disbursement or independent expenditure). Starting a run is free, and a run that finds no matches costs nothing (this includes every watch-mode baseline run). HTTP-only (no browser), so runs are fast and cheap.

## FAQ

**How is `webhookUrl` different from Apify's own platform webhooks?**
Apify's platform webhooks are configured separately per Task/Actor via the Console or the Webhooks API — useful if you already live in the Apify Console, but extra setup if you're calling this Actor's API directly and just want a completion ping. `webhookUrl` is a plain input field: set it on the run itself and it POSTs a JSON body (`actorRunId`, `defaultDatasetId`, `finishedAt`, `pushed`, the full `summary` object described above, and — if `watchLabel` is set — `watchSeeding`/`watchNewCount`/`watchSkipped`/`baselineTruncated`/`baselineTruncatedTotal`) once the run finishes and every row is already pushed and charged. It's best-effort — a slow or failing webhook only logs a warning, it never fails the run, changes the result set, or affects billing.

**Which mode should I use for "how much did this campaign spend on Facebook ads"?**
`searchMode: "disbursements"` with `recipientName: "META"` and the committee's `committeeId`. Disbursements are money the campaign itself paid out. `independentExpenditures` is a different thing: money spent by *outside* groups for or against a candidate, which the candidate's own committee never reports.

**Why is an `expenditureDate` sometimes in the year 3024?**
Because the filer typed it that way. Schedule E dates are transcribed from the committee's own filing and the FEC publishes them as filed, typos included (`3024-07-18` on a real 2024 row). Use `disseminationDate` — when the ad actually ran — when you need a date you can sort on, and treat far-future `expenditureDate` values as data-entry errors rather than dropping the row.

**Is `committeeType` computed by this Actor, or is it real FEC data?**
It's the FEC's own official classification, read straight off the `committee` object every transaction schedule already embeds (`committee_type_full`/`designation_full`) — not a name-pattern guess. So `"Super PAC (Independent Expenditure-Only)"`, `"PAC - Qualified"`, `"Hybrid PAC (with Non-Contribution Account)"`, `"House"`/`"Senate"`/`"Presidential"` (candidate committees) and `"Party - Qualified"` are all values the FEC itself assigns when a committee registers, available in contributions, disbursements and independent expenditures modes.

**Can I filter contributions by committee?**
Not in contributions mode. `committeeId` is a fast filter on Schedules B and E and is supported there, but the FEC's Schedule A endpoint reliably times out on it (verified on both large and small committees), so it is ignored with a warning rather than producing a failed run.

**Why does searching "Warren" return people who aren't named Warren?**
The FEC's search matches the token anywhere in the filed name, including middle names. A Senate search for `Warren` returns 27 candidates, and the first ones alphabetically are `BOYANTON, RICHARD WARREN` and `BROWN, WARREN P` — not Elizabeth Warren. Search the full name (`"Elizabeth Warren"`) to narrow it: all tokens must match.

**What do the `candidateStatus` letters mean?**
Straight from the FEC: `C` = present candidate, `F` = future candidate, `N` = not yet a candidate, `P` = prior candidate. `party`, `office` and `incumbentChallenge` are already decoded to readable text for you; this one field stays as the FEC's raw code so it round-trips cleanly back into FEC queries.

**Why is `district` `"00"` for a Senator?**
`00` is the FEC's placeholder for offices that have no House district — President, Senate, and at-large House seats.

**Are `receipts` lifetime totals?**
No. The FEC stores one totals record per election cycle, and this Actor returns the **most recent** one, with `coverageStartDate`/`coverageEndDate` telling you exactly which period it covers. Elizabeth Warren, for example, has 12 separate totals records on file. If you need a specific past cycle, set `electionYear`.

**Do I have to compute small-dollar giving myself?**
No. `individualUnitemizedContributions` is the FEC's own ≤$200-aggregate figure, returned straight from the same totals record as `individualItemizedContributions` — you don't need to subtract one from `individualContributions` to get it.

**Why do `electionYears` and `cycles` differ?**
`electionYears` are the years the person was on the ballot; `cycles` are every two-year window the FEC holds data for, which includes the off-years in between. In the sample above that's `[2012, 2018, 2024, 2030]` versus `[2012 … 2026]`.

**Do I need my own FEC API key?**
No. The Actor ships with its own `api.data.gov` key, so you are not sharing the throttled public `DEMO_KEY` with every other caller on the internet.

**Is this legal?**
Yes. Federal campaign finance filings are public records that candidates are legally required to disclose, and this reads them from the FEC's own public API. No login, no scraping behind authentication.

**Can I get individual donors' names and addresses?**
Set `searchMode` to `"contributions"` to search individual itemized donor contributions directly (name, employer, occupation, city/state, amount, date, receiving committee) — this is the FEC's Schedule A data, the same public disclosure that fec.gov's own donor search reads from. Full street addresses aren't included, only city/state. Candidates mode still returns candidate-level aggregates only.

**Why does `electionYear` default to the current even year in contributions mode but not candidates mode?**
The FEC's Schedule A endpoint times out on a full-table scan (129,000+ rows even for a single popular employer, across all years) if you don't scope it to a two-year cycle. Candidates mode has no such requirement, so it stays optional there.

**How does watch mode decide what's "new"?** By the contribution's own FEC-assigned `sub_id`, which is stable and unique per itemized transaction. A baseline of ids you've already been sent is kept in a named key-value store on your own Apify account (`fetchsmith-fec-watch`) — it survives across runs even though the default per-run store does not.

**Can I search by a specific dollar range or date window?** Yes — `minAmount`/`maxAmount` bound the contribution amount (either or both) and `contributionDateFrom`/`contributionDateTo` bound the receipt date (`YYYY-MM-DD`, either or both). Contributions mode only.

**What happens if I typo a date?** The run stops immediately with an error naming the bad value, before any row is fetched or charged. This is deliberate: a date bound that cannot be parsed used to be dropped with a warning, which quietly turned "contributions in June 2024" into "every contribution ever" — a bigger, wrong, fully billable result set that looks normal in the log. Only strict `YYYY-MM-DD` is accepted, and it must be a real calendar date: `2024-02-30`, `2024-13-01`, `06/15/2024` and `2024-6-5` are all rejected rather than guessed at.

**How do I know a run returned everything, without reading the log?** Every run writes a `RUN_SUMMARY` record to its own key-value store — fetch it with `GET https://api.apify.com/v2/actor-runs/<runId>/key-value-store/records/RUN_SUMMARY` (no webhook needed; it's also sent as `summary` on any `webhookUrl` POST). It carries `declaredMatches` (what the FEC itself says matches your filters, from its own `pagination.count` — `null`, never `0`, if the API never answered with a count, and `declaredMatchesExact` is the FEC's own flag for whether that number is exact), `scanned`, `delivered`, `rowsNotReached`, `pages` and a boolean `complete`. When `complete` is `false`, `incompleteReason` is one of `upstream-error` (the FEC API failed mid-walk — `runError` has the message), `max-results` (your `maxResults` is below the match count — the common, harmless one), `charge-limit` (the run's pay-per-event limit stopped it), `seed-cap` (a watch baseline stopped at the 5,000-row cap) or `watch-page-cap` (a watch scan stopped at the 1,000-page cap). `incompleteDetail` spells out the numbers. A short run still finishes as `SUCCEEDED` — the rows it did return are real and already charged — so this record, plus the run's status message, is how a pipeline tells "20 of 20 matches" apart from "20 of 6,921". `max-results` is only reported when something was demonstrably left behind: a query with exactly `maxResults` matches reports `complete: true`.

**What happens if a run fails halfway through a watch?** Nothing you already paid for is charged twice. The run still ends `FAILED`, but before it does it saves the baseline including every row it had already delivered and charged for, with `lastRunStatus: "failed-incremental"` — so the next run treats those as already-seen instead of billing you for them again. The one exception is a **baseline** run that fails: a half-written baseline would make the next run an incremental one and charge you for everything the failed seed walk never reached, so no record is saved at all and the run tells you to simply seed again (baseline runs are free). `RUN_SUMMARY.baselineSaved` reports which of the two happened.

**My donor/employer filter is broad — will a watch run scan the whole Schedule A table every time?** It scans until it finds `maxResults` new contributions or exhausts the current match set (capped at 1000 pages, ~100,000 rows, per run — a safety valve, not something a normally-filtered watch should ever hit). A very broad, weakly-filtered watch (e.g. a common surname with no employer/state/amount filter) can page through a lot of already-seen contributions before finding something new; narrow the filters for a faster, cheaper watch.

## Notes
Only public data from the FEC's own public disclosure API. Issues or feature requests: support@fetchsmith.com. Also available as a hosted API at https://fetchsmith.com

## Related guides
- [FEC Campaign Finance JSON API — what the DEMO_KEY actually lets you do](https://fetchsmith.com/blog/fec-campaign-finance-json-api-demo-key)
- [All FetchSmith tools](https://fetchsmith.com/tools)

## Source code
https://github.com/Fetchsmith/fetchsmith/tree/main/actors/fec-campaign-finance-scraper
