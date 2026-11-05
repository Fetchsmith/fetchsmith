# ClinicalTrials.gov MCP Server

An **MCP server** (Apify Standby mode) that lets an AI agent search **ClinicalTrials.gov**,
the official US NIH/NLM clinical trial registry, directly from a tool call — no scraping, no
dataset to download, no separate Actor run to poll. Point your MCP client at this Actor's
Standby URL and call `search_clinical_trials` like any other tool.

## Tool: `search_clinical_trials`

| Argument | Type | Notes |
| --- | --- | --- |
| `condition` | string, optional | Medical condition, e.g. `"asthma"` |
| `intervention` | string, optional | Drug, device or procedure, e.g. `"semaglutide"` |
| `maxResults` | number, optional | Default 10, max 1000 |

Returns a JSON array of studies: `nctId`, `title`, `status`, `url`.

Backed by ClinicalTrials.gov's own public API v2 (no key, no login, no proxy) — the same
source our [`clinicaltrials-scraper`](https://fetchsmith.com/tools/clinicaltrials-scraper)
Actor uses for batch pulls. Use that Actor instead if you need the full 39-field dataset,
site-level rows, or a scheduled/watched pull; use this MCP server when an agent needs to ask
a live question mid-conversation.

## Pricing

Pay-per-event: a flat fee per tool call, charged once regardless of how many studies that
call returns. No start fee, no platform run to babysit.

## Related guides

- [fetchsmith.com/tools](https://fetchsmith.com/tools)
