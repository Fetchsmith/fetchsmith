# TITLE

DESCRIPTION

## What it does
- Reads publicly available pages from SOURCE and returns structured JSON.
- Pay per result: you are charged only for rows actually returned.
- HTTP-only (no browser), so runs are fast and cheap.

## Input
| Field | Type | Description |
|---|---|---|
| `query` | string | What to search for |
| `maxResults` | integer | Stop after this many results (default 50) |

## Output
One item per row with fields: ...

## Pricing
`result` — charged per returned item. The run start is free.

## Notes
Only public data is collected. Respect the source site's terms of use when using the output. Issues or feature requests: support@fetchsmith.com. Also available as a hosted API at https://fetchsmith.com
