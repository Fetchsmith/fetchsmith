# FEC Campaign Finance Scraper – Candidates & Financial Totals

Search US federal candidates (House, Senate, President) by name, state, office, party and election cycle, and get each candidate's campaign financial totals — receipts, disbursements, cash on hand, individual contributions — in one row. Powered by the FEC's official `api.open.fec.gov` disclosure API. No login, no browser, no API key of your own required.

## Use cases
- **Political/campaign research** — pull every Senate candidate in a state with their fundraising totals in a single dataset instead of clicking through fec.gov one candidate at a time.
- **Journalism & fact-checking** — compare receipts, burn rate (`disbursements` vs `receipts`) and war chests (`cashOnHandEnd`) across a race, with the FEC page URL attached to each row for citation.
- **Watchdog & transparency dashboards** — schedule a run per cycle and diff the totals to track who is raising money and how fast.
- **Small-dollar vs. large-dollar analysis** — `individualUnitemizedContributions` (small-dollar giving as the FEC itself computes it, no subtraction required) against `individualItemizedContributions` (the >$200-aggregate subset) shows how much of a campaign's money comes from grassroots donors versus large ones.
- **Candidate list building** — enumerate everyone who has ever filed for a given office/state/cycle, including long-shot and prior candidates.

## Input
| Field | Type | Description |
|---|---|---|
| `candidateName` | string | Full or partial name to search for (default `"Warren"`). Matches any part of the name — see the FAQ. |
| `state` | string | 2-letter state code, e.g. `"CA"`. Optional. |
| `office` | string | `H` (House), `S` (Senate), `P` (President). Optional. |
| `party` | string | Party code, e.g. `DEM`, `REP`, `IND`, `LIB`. Optional. |
| `electionYear` | integer | Even-numbered election cycle, e.g. `2024`. Optional. |
| `includeTotals` | boolean | Fetch financial totals per candidate (default `true`). Costs one extra request per candidate. |
| `maxResults` | integer | Stop after this many candidates (default `20`, max `500`). |

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

## Pricing
`result` — you are charged per candidate row actually returned. Starting a run is free, and a run that finds no matching candidates costs nothing. HTTP-only (no browser), so runs are fast and cheap.

## FAQ

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
Not from this Actor. It returns candidate-level aggregates only.

## Notes
Only public data from the FEC's own public disclosure API. Issues or feature requests: support@fetchsmith.com. Also available as a hosted API at https://fetchsmith.com

## Related guides
- [FEC Campaign Finance JSON API — what the DEMO_KEY actually lets you do](https://fetchsmith.com/blog/fec-campaign-finance-json-api-demo-key)
- [All FetchSmith tools](https://fetchsmith.com/tools)

## Source code
https://github.com/Fetchsmith/fetchsmith/tree/main/actors/fec-campaign-finance-scraper
