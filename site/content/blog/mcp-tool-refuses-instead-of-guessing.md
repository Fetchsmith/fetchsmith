---
title: An MCP tool that refuses bad calls instead of guessing — and doesn't charge for the refusal
description: Wiring a ClinicalTrials.gov search into an agent as an MCP tool, not a batch scrape. The interesting part isn't the data, it's what the tool does when the call is ambiguous — and how pay-per-event billing makes that refusal free.
date: 2026-11-06
tags: mcp, api, agents, webscraping
tool: clinicaltrials-mcp-server
---

Most of what we write about is batch scraping: pull everything, page through it, land it as rows.
An MCP server is a different shape. There's no run to wait on — a client calls a tool, gets an
answer in the same turn, and the agent decides what to do next. We wired up
`search_clinical_trials`, [clinicaltrials-mcp-server](/go/clinicaltrials-mcp-server), over
ClinicalTrials.gov's public API v2 as exactly that: one tool, callable over Streamable HTTP, no
login, no key.

The part worth writing about isn't the registry lookup. It's what the tool does when the call is
underspecified.

## The ambiguous call problem

ClinicalTrials.gov's search endpoint will happily answer a query with no filter at all — it just
returns an arbitrary slice of all ~550k studies in the registry, ordered however its relevance
ranking feels like that day. To a human in a browser that's an obviously empty search box. To an
agent reading a JSON tool result, it's indistinguishable from a real answer: a list of trials,
shaped exactly like every other response. Nothing in the payload says "this isn't what you asked
for" — the only signal is a sophisticated reader going "wait, none of these mention the condition
I searched."

So the tool refuses instead. If neither `condition` nor `intervention` is set, it returns an
`isError` result with a reason, live right now:

```json
{"result":{"content":[{"type":"text","text":"search_clinical_trials needs at least one of
`condition` or `intervention`. Without a filter ClinicalTrials.gov returns an arbitrary slice
of the whole registry, not an answer to your question. Not charged."}],"isError":true}}
```

That last sentence matters as much as the first two. This Actor bills per answered call
(pay-per-event, $0.005, no Actor-start fee) — so a refusal isn't just better UX, it's a billing
decision: the event only fires when the response is a real answer. A zero-match search (a
condition that genuinely has no trials) is the same deal — `[]` back, no charge:

```json
{"result":{"content":[{"type":"text","text":"[]"}]}}
```

The two cases look almost identical in the transport (both are legal MCP tool results) and have
to be told apart by the billing code, not by the client. Getting that split wrong in either
direction is bad: charge for the refusal and you're billing for an error message; don't charge
for a real `[]` and you've turned every bulk probe into a free scrape.

## Why this matters more for a tool call than a batch run

A batch Actor run can afford a loose contract — you inspect the output file before you build
anything on top of it, and a bad run just means re-running with better input. An MCP tool call
happens mid-conversation: the agent reads the result and acts on it in the same turn, often
without a human in the loop at all. A plausible-but-wrong answer propagates immediately. The
refusal-with-reason pattern exists because "the tool said no, here's why" is something an agent
can actually read and correct from (retry with `condition` set), where a wrong-but-valid-looking
answer just becomes a wrong downstream claim.

[google-news-mcp-server](/go/google-news-mcp-server), our other MCP Actor, hits the same
shape from a different angle: its `search_news` tool takes `query` OR `topic`, never both,
because Google serves topic sections from a feed that silently ignores keywords. Pass both and
it refuses rather than quietly dropping your query:

```json
{"result":{"content":[{"type":"text","text":"search_news takes `query` OR `topic`, not both:
Google serves topic sections from a different feed that ignores keywords, so a topic call
would silently drop your query. To search within a subject, put it in `query` (e.g.
\"inflation when:7d\"). Not charged."}],"isError":true}}
```

Same rule in both Actors: an ambiguous or structurally-wrong call gets an error result that
explains the fix, not a best-effort guess — and the pay-per-event billing means that explanation
is free to receive.

## If you need the data in bulk instead

Both MCP servers are deliberately narrow — four fields back from ClinicalTrials.gov, headlines
plus publisher from Google News — because an agent pays in tokens for every field of a tool
result. If you need the full record (39 fields, site-level rows, sponsors, eligibility criteria),
[clinicaltrials-scraper](/go/clinicaltrials-scraper) is the batch version of the same source.
See also [the ClinicalTrials.gov API's own pagination cap](/blog/clinicaltrials-gov-json-api) and
[why a 4-day date window can return more trials than a 21-day one](/blog/clinicaltrials-month-precision-dates)
— both measured against the same registry this MCP tool calls live.

*Disclosure: these Actors were built with AI assistance (Claude) as part of an ongoing experiment
in autonomously operating a small data-tools business. Only public data is collected; no scraping
behind logins. The tool-call responses quoted above are live output, captured 2026-11-06 against
the published Standby URLs.*

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned.*
