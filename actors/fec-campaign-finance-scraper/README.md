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

## Status: NOT YET PUBLISHED (draft, 2026-09-12)
Code is written and locally verified against real FEC data. **Blocked on getting a personal `api.data.gov` key** — the shared `DEMO_KEY` this code currently uses is capped at 40 calls/hour globally, which is far too low for a public Actor (a handful of runs with `includeTotals` on would exhaust it). See `/root/agent/tasks/queue.md` for the exact blocker and next steps before pushing/publishing.
