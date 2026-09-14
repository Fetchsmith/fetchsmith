# FEC Campaign Finance Scraper – Candidates & Financial Totals

Search US federal candidates (House, Senate, President) by name, state, office, party and election cycle, with each candidate's campaign financial totals (receipts, disbursements, cash on hand, individual contributions) included — via the FEC's official `api.open.fec.gov` API. No API key needed for casual use, no login required.

## What it does
- Searches `GET /v1/candidates/` by name/state/office/party/cycle, then (optionally) fetches each candidate's most recent financial totals from `GET /v1/candidate/<id>/totals/`.
- Pay per result: you are charged only for candidate rows actually returned.
- HTTP-only (no browser), so runs are fast and cheap.

## Input
| Field | Type | Description |
|---|---|---|
| `candidateName` | string | Full/partial name to search for (default `"Warren"`) |
| `state` | string | 2-letter state code, optional |
| `office` | string | `H` (House), `S` (Senate), `P` (President), optional |
| `party` | string | Party code, e.g. `DEM`, `REP`, optional |
| `electionYear` | integer | Election cycle year, optional |
| `includeTotals` | boolean | Fetch financial totals per candidate (default true) |
| `maxResults` | integer | Stop after this many candidates (default 20) |

## Output
One item per candidate: `candidateId`, `name`, `party`, `office`, `state`, `district`, `incumbentChallenge`, `candidateStatus`, `electionYears`, `cycles`, `firstFileDate`, `fecUrl`, `receipts`, `disbursements`, `cashOnHandEnd`, `individualContributions`, `individualItemizedContributions`, `coverageStartDate`, `coverageEndDate`.

## Pricing
`result` — charged per returned candidate row. The run start is free.

## Notes
Only public data collected from the FEC's own public disclosure API (campaign finance totals are federally mandated public records). Issues or feature requests: support@fetchsmith.com. Also available as a hosted API at https://fetchsmith.com

## Status: NOT YET PUBLISHED (draft; blocker re-measured 2026-09-14, cycle 252)
Code is written and verified against real FEC data. **Blocked on getting a personal `api.data.gov` key.** The blocker is worse than the earlier "40 calls/hour" note claimed — measured live against `api.open.fec.gov`, one response carries three contradictory limits:

- `x-ratelimit-limit: 10` (counted down 9, 8, 7 … to 0 over single requests, then `429`)
- error body: `"your rate limit of 40 calls per hour for the DEMO_KEY"`
- `retry-after: 57263` — **15.9 hours**, not the one hour the message promises

The quota is shared per egress IP, and `includeTotals` makes each result cost 2 requests (1 search + 1 `/candidate/{id}/totals/`), so a single default run (20 candidates = 21 requests) exhausts every published ceiling. Publishing on `DEMO_KEY` would ship an Actor that 429s for real users. Fix is a personal key (1000/hour, free at https://api.data.gov/signup/) wired in place of the hardcoded `API_KEY`.

Write-up of the API's behaviour: https://fetchsmith.com/blog/fec-campaign-finance-json-api-demo-key
