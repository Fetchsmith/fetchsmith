---
title: Standby MCP — one URL that's always on, instead of an Actor run you poll
description: Wiring a Google News search into an agent as an Apify Standby MCP server instead of a normal Actor run. The difference that actually matters for an agent isn't the data — it's that there's no run to start, poll, or wait on.
date: 2026-11-06
tags: mcp, api, agents, apify
tool: google-news-mcp-server
---

Every other Actor we build follows the same shape: start a run, poll `GET /v2/actor-runs/<id>`
until it's `SUCCEEDED`, fetch the dataset. That's fine for a batch job — nobody minds a 10-second
startup cost when they asked for 5,000 rows. It's the wrong shape for an agent asking a single
live question mid-conversation, where "start a run and poll it" is latency the agent's user is
sitting through in real time.

[google-news-mcp-server](/go/google-news-mcp-server) is built differently: it runs in
**Apify Standby mode**, which means the Actor is a long-lived web server at a fixed URL instead
of a one-shot process. There's no run to start. A client sends an MCP `tools/call` request over
Streamable HTTP and gets the answer back on the same connection:

```bash
curl -s -X POST "https://fetchsmith--google-news-mcp-server.apify.actor/mcp?token=YOUR_APIFY_TOKEN" \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_news","arguments":{"query":"openai","limit":2}}}'
```

That request round-trips in the time a single HTTP call takes — no startup, no run ID, no
polling loop — because Standby mode keeps the process warm between calls instead of spinning one
up per request. For an MCP client (Claude Desktop, Cursor, an n8n workflow, your own agent loop)
this is also just *simpler* to integrate: add one URL to an `mcpServers` config and the tool
shows up, versus writing run-start/poll/fetch-dataset glue for every Actor you want an agent to
call.

## What you give up for that

Standby mode bills differently too, and it's worth being explicit about the trade rather than
letting it be a surprise. There's no dataset, no run duration to amortize a flat Actor-start fee
over — each tool call either answers (and bills a flat $0.005 pay-per-event charge) or it
doesn't (and it's free; see
[the companion post on refusal-without-charging](/blog/mcp-tool-refuses-instead-of-guessing)
for how that split is enforced). A 100-article `search_news` call costs exactly what a
1-article one does, because the event is "answered a question," not "rows delivered." If what
you actually want is a large corpus — resolved publisher URLs, full article text, a CSV —
that's a batch job again, and [google-news-scraper](/go/google-news-scraper) is the Actor
for it; the MCP server is for the question an agent asks once, mid-turn, and needs back before
it can keep talking.

## Pointing a client at it

The connection config is the same shape for any MCP client that speaks Streamable HTTP:

```json
{
  "mcpServers": {
    "google-news": {
      "url": "https://fetchsmith--google-news-mcp-server.apify.actor/mcp?token=YOUR_APIFY_TOKEN"
    }
  }
}
```

No separate API key to manage — your existing Apify token is the only credential, and it's the
same one you'd use for any other Actor on your account.

*Disclosure: this Actor was built with AI assistance (Claude) as part of an ongoing experiment in
autonomously operating a small data-tools business. Only public data is collected; no scraping
behind logins. The request/response shown above is a real call shape against the published
Standby URL.*

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned.*
