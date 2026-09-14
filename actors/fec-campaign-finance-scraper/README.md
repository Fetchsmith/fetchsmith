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

## Status
Unblocked 2026-09-14 (cycle 253): the shared `DEMO_KEY` (10-40 calls/hour, per egress IP — see the write-up below) was replaced with a personal `api.data.gov` key, wired in as a secret Actor environment variable (`FEC_API_KEY`, not committed to source). Measured live: the personal key's own ceiling is `x-ratelimit-limit: 60`, not shared with any other tenant, so a default run (20 candidates, `includeTotals` on = 21 requests) no longer exhausts the quota.

Write-up of the API's behaviour (rate limits, `/totals/` double-counting, the `q` full-text quirk): https://fetchsmith.com/blog/fec-campaign-finance-json-api-demo-key

## Related guides
- [FEC Campaign Finance JSON API — what the DEMO_KEY actually lets you do](https://fetchsmith.com/blog/fec-campaign-finance-json-api-demo-key)
- [All FetchSmith tools](https://fetchsmith.com/tools)

## Source code
https://github.com/Fetchsmith/fetchsmith/tree/main/actors/fec-campaign-finance-scraper
