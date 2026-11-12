# ClinicalTrials.gov MCP Server

An **MCP server** (Apify Standby mode) that lets an AI agent search **ClinicalTrials.gov**,
the official US NIH/NLM clinical trial registry, directly from a tool call — no scraping, no
dataset to download, no separate Actor run to poll. Point your MCP client at this Actor's
Standby URL and call `search_clinical_trials` like any other tool.

**$0.005 per answered call, flat. No Actor-start fee. No result, no charge.**

## Tool: `search_clinical_trials`

| Argument | Type | Notes |
| --- | --- | --- |
| `condition` | string, optional\* | Medical condition, e.g. `"asthma"` |
| `intervention` | string, optional\* | Drug, device or procedure, e.g. `"semaglutide"` |
| `maxResults` | number, optional | Default 10, max 1000 |

\* **At least one of `condition` or `intervention` is required.** With neither, the registry API
returns an arbitrary slice of all ~550k studies, which reads like a real answer to an agent but
isn't one — so the tool refuses the call instead, and that refusal is not charged.

Returns a JSON array of studies, each with `nctId`, `title`, `status` (the registry's
`overallStatus`, e.g. `RECRUITING`, `COMPLETED`, `NOT_YET_RECRUITING`) and a canonical
`url`.

### Example tool-call request

```json
{"name": "search_clinical_trials",
 "arguments": {"intervention": "semaglutide", "maxResults": 2}}
```

### Example output

```json
[
  {
    "nctId": "NCT00813020",
    "title": "A Clinical Trial Investigating the Comparison of Three Different Concentrations of NN9535 in Healthy Male Subjects",
    "status": "COMPLETED",
    "url": "https://clinicaltrials.gov/study/NCT00813020"
  },
  {
    "nctId": "NCT05567796",
    "title": "A Research Study to See How Well CagriSema Helps People With Excess Body Weight Lose Weight",
    "status": "ACTIVE_NOT_RECRUITING",
    "url": "https://clinicaltrials.gov/study/NCT05567796"
  }
]
```

Live output, captured 2026-11-05 against the published Standby URL.

## What it is for

- **Patient/trial triage mid-conversation** — an agent asked "are there recruiting trials for
  this condition?" answers in one tool call instead of running a batch scrape and waiting.
- **Pharma and biotech competitive questions** — "what trials involve this drug?" without
  standing up a pipeline.
- **Grounding a medical answer in a citable registry record** — every row carries its `nctId`
  and canonical ClinicalTrials.gov URL, so the agent can cite rather than assert.
- **Cheap breadth checks before committing to a bulk pull** — probe a condition for $0.005,
  then switch to the batch Actor below if the answer is worth 39 fields.

## Pricing and how we compare

Pay-per-event, a flat **$0.005** per call that returned at least one study. No start fee, no
platform run to babysit, no per-study multiplier — a call returning 500 studies costs the same
as one returning 1.

**This is the only MCP server on the Apify Store dedicated to ClinicalTrials.gov** (checked
2026-11-05, re-verified live 2026-11-12, across the `clinical trial`, `mcp server`, `medical mcp`
and `pubmed` queries — the other ClinicalTrials.gov listings are all batch scrapers, a different
product shape). Trial search does exist as *one tool inside* a broader compliance bundle, and
that is the honest comparison to make. Prices read live from each Actor's own `pricingInfos`
record on 2026-11-05, re-verified live 2026-11-12, not from Store marketing copy:

| Actor | Users (u30d) | Closest event | Price/call | vs. ours |
| --- | --- | --- | --- | --- |
| **fetchsmith/clinicaltrials-mcp-server** | — | `tool-call` | **$0.005** | — |
| `red.cars/healthcare-compliance-mcp` | 2 (1) | `search_clinical_trials` | $0.05 + $0.00005 start fee | **10x** dearer, plus a start fee we don't charge |
| `red.cars/pharma-pipeline-intelligence-mcp` | 8 (1) | `search_drug_pipeline` | $0.05 | **10x** dearer |
| `themineworks/academic-research-mcp` | 33 → 38 (29 → 33) users as of 2026-11-05 → 2026-11-12 | `search_pubmed` | $0.0625 + $0.005 start fee (now tiered FREE-DIAMOND $0.0625→$0.04375, re-verified 2026-11-12) | **12.5x** dearer at its FREE tier, plus a start fee we don't charge |

All three are genuinely broader than this Actor. `healthcare-compliance-mcp` exposes 9 tools
over FDA MAUDE adverse events, 510(k) clearances and recalls — including a
`search_clinical_trials` of its own at $0.05 and a `get_trial_details` at $0.03;
`pharma-pipeline-intelligence-mcp` exposes 8 (competitive landscape, adverse-event signals,
patent exclusivity); `academic-research-mcp` exposes 6 across
OpenAlex/Crossref/arXiv/OpenCitations/PubMed. If you want a device-compliance workflow or a
multi-source literature report, buy theirs — this Actor does not try to be that.

What this Actor is, that none of them are: **the registry lookup on its own, at a tenth of the
price, with no start fee and no charge when the search finds nothing.** If your agent asks
trial questions often, the per-call difference is the whole cost of the feature.

## Source and limits

Backed by ClinicalTrials.gov's own **public API v2** — no API key, no login, no proxy, no
scraping, no ToS grey area. `maxResults` is clamped to 1000 because `pageSize=1001` returns
`200` with only the first 1000 rows honored, so a higher value would silently under-deliver.
Results are the registry's own relevance order; this tool does not paginate beyond the first
page, by design (an agent asking a live question wants the top matches, not a bulk export).

Same source as our [`clinicaltrials-scraper`](https://fetchsmith.com/tools/clinicaltrials-scraper)
Actor. **Use that one instead** if you need the full 39-field dataset, site-level rows,
eligibility criteria, sponsors, or a scheduled/watched pull; use this MCP server when an agent
needs to ask a live question mid-conversation.

## FAQ

**Do I need an Anthropic/OpenAI key for this?**
No. An MCP server serves *tools*; your agent brings its own model. This Actor makes zero
inference calls and has no LLM in it — you are paying for registry access, not for tokens.

**What happens if ClinicalTrials.gov is down or slow?**
The tool returns an MCP error result saying so, and **does not charge** you. Requests time out
at 20 seconds. Retry the call.

**Am I charged for a search that finds nothing?**
No. A zero-match search is free, as is a call rejected for a bad or missing argument. You are
only charged for a call that returned at least one study.

**Which MCP clients work?**
Any client speaking Streamable HTTP MCP — Claude Desktop/Code, Cursor, Codex, and the Apify
MCP tooling. Point it at this Actor's Standby URL with `/mcp` as the path and your Apify token.

**Why only four fields?**
Because an agent reading a tool result pays for every token of it. `nctId`, `title`, `status`
and `url` are what a live question needs, and the `url` is the escape hatch to the full record.
If you need the other 35 fields in bulk, the batch Actor above is the cheaper way to get them.

## Related guides

- [fetchsmith.com/tools](https://fetchsmith.com/tools)
- [clinicaltrials-scraper](https://fetchsmith.com/tools/clinicaltrials-scraper) — batch, 39 fields
- [An MCP tool that refuses bad calls instead of guessing — and doesn't charge for the refusal](https://fetchsmith.com/blog/mcp-tool-refuses-instead-of-guessing)
- [The ClinicalTrials.gov API silently caps pageSize at 1000 — and its phase filter doesn't exist where you'd look for it](https://fetchsmith.com/blog/clinicaltrials-gov-json-api)
- [A 4-day window on ClinicalTrials.gov returns more trials than a 21-day one](https://fetchsmith.com/blog/clinicaltrials-month-precision-dates)
