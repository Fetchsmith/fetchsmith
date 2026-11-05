# Google News MCP Server for AI Agents

An **MCP (Model Context Protocol) server** that gives your AI agent one tool: live news search over
Google News. Ask a question, get current headlines back in the same turn — no API key, no scraping
setup, no browser, no monthly plan.

This Actor runs in **Apify Standby mode**: it is a web server at a fixed URL that speaks MCP over
streamable HTTP. Point Claude Desktop, Cursor, VS Code, n8n, LangChain or your own agent at it and
`search_news` appears in its tool list.

**You bring the model; we serve the data.** This server performs no inference of its own, so you are
never paying for somebody else's tokens on top of your own.

## The tool

### `search_news`

| Argument | Type | Description |
|---|---|---|
| `query` | string | Keyword or phrase, e.g. `"openai funding"`. Google News search operators work: `when:1d`, `site:reuters.com`, `-word`, `OR`, `"exact phrase"`. |
| `topic` | enum | Browse a section instead of searching: `WORLD`, `NATION`, `BUSINESS`, `TECHNOLOGY`, `ENTERTAINMENT`, `SCIENCE`, `SPORTS`, `HEALTH`, `POLITICS`, `ECONOMY`, `REAL_ESTATE`, `JOBS`, `EDUCATION`, `AUTOS`, `MOVIES`, `MUSIC`, `CELEBRITIES`, `ARTS`, `SOCCER`, `BASKETBALL`. |
| `limit` | number | Max articles (default 10, max 100). |
| `language` | string | e.g. `"en-US"`, `"de"`, `"fr"` (default `"en-US"`). |
| `country` | string | Edition, e.g. `"US"`, `"GB"`, `"DE"` (default `"US"`). |

Pass **either** `query` **or** `topic`, not both — Google serves topic sections from a different
feed that ignores keywords, so accepting both would silently drop your query and hand your agent a
plausible-looking wrong answer. The tool refuses instead, and does not charge.

## Sample output

A real response to `search_news({ query: "openai", limit: 2 })`:

```json
[
  {
    "title": "OpenAI kicks off charm offensive to change voters' view of data centers",
    "publisher": "Reuters",
    "publisherDomain": "reuters.com",
    "url": "https://news.google.com/rss/articles/CBMirgFBVV95cUxNT3pvX1Vf...",
    "publishedAt": "2026-11-05T19:34:01.000Z",
    "relatedCoverage": [
      { "title": "OpenAI pledges to halt NDAs in new data center policy proposal after election rebuke", "publisher": "CNBC" },
      { "title": "OpenAI Pledges to Give Locals More Say in Data Center Projects", "publisher": "The New York Times" }
    ]
  }
]
```

`relatedCoverage` is the field most agents end up leaning on: it is **the same story as reported by
other publishers**, which is what you need to tell a real consensus from one outlet's framing.

## Pricing and how we compare

**$0.005 per `search_news` call that returns at least one article** — flat, however many articles it
returns, and **no Actor-start fee**.

**No result, no charge.** A search with zero matches, a call rejected for a bad or missing argument,
and a call where Google News itself did not answer are all free. You are billed for answers, not
attempts.

A 100-article call costs the same $0.005 as a 1-article call, so set `limit` to what you actually
want to read.

Prices read live from each Actor's own `pricingInfos` record (checked 2026-11-05, re-confirmed on
the `latest news mcp` / `news mcp server` / `google news mcp` queries):

| Actor | Users (u30d) | Closest event | Price/call | vs. ours |
| --- | --- | --- | --- | --- |
| **fetchsmith/google-news-mcp-server** | — | `search_news` | **$0.005** | — |
| `mrbridge/latest-news-mcp-server` | 118 (35) | `tool-read` | $0.008 (FREE) tiered down to $0.005 (GOLD+), plus a second `tool-enriched` event at $0.015→$0.008 and a $0.00005 start fee | **matches** our price only at its best tier; 60% dearer on a FREE-plan caller, plus a start fee we don't charge |
| `nexgendata/news-mcp-server` | 20 (4) | `tool-call` | $0.02 + $0.00005 start fee | **4x** dearer, plus a start fee we don't charge |
| `quodlibetical_buffalo/google-news-mcp` | 2 (1) | — (no PPE pricing record found) | — | direct title collision, but no measurable traction or disclosed price to compare |

`mrbridge/latest-news-mcp-server` is the clear demand leader in this corner (u30d=35, second only
to ESPN across every MCP listing we've measured) and the one worth beating: our flat $0.005 beats
its entry-tier FREE-plan price by 37% and never requires a start fee or a second enrichment charge
to reach parity. `nexgendata/news-mcp-server` is a flat 4x dearer. Neither offers `relatedCoverage`
(what other publishers ran the same story) or a `topic` browse mode — both are query-only.

## Use cases

- **News-aware agents** — let an assistant check what actually happened today before it answers,
  instead of asserting from stale training data.
- **Monitoring and alerting** — poll `search_news({ query: "<your brand> when:1d" })` on a schedule
  and have the agent decide whether anything is worth escalating.
- **Research and briefings** — pull a topic section, then use `relatedCoverage` to see which stories
  several outlets independently picked up.
- **Market and competitor tracking** — `site:` and `-` operators narrow a query to the publications
  you trust.
- **Sentiment and trend inputs** — headlines plus publishers plus timestamps, structured, for a
  downstream model.

## How to connect

Standby URL:

```
https://fetchsmith--google-news-mcp-server.apify.actor/mcp
```

Add it as a streamable-HTTP MCP server, with your Apify token as a bearer credential. In a
`mcpServers` config this looks like:

```json
{
  "mcpServers": {
    "google-news": {
      "url": "https://fetchsmith--google-news-mcp-server.apify.actor/mcp?token=YOUR_APIFY_TOKEN"
    }
  }
}
```

A raw check, if you want to see it answer before wiring an agent up:

```bash
curl -s -X POST "https://fetchsmith--google-news-mcp-server.apify.actor/mcp?token=YOUR_APIFY_TOKEN" \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_news","arguments":{"query":"openai","limit":2}}}'
```

## FAQ

**Is this legal / is it scraping?**
No scraping and nothing behind a login. It reads Google News' own **public RSS feeds** — the same
endpoints Google publishes for feed readers.

**Why is `url` a news.google.com link instead of the publisher's own URL?**
Because resolving Google's redirect costs an extra HTTP request per article and Google rate-limits
it. An MCP tool call is synchronous — your agent is waiting — so this server keeps the round trip
short. The link works: it opens the article. If you need **resolved publisher URLs and full article
text in bulk**, that is what the batch Actor below is for.

**Do I need an OpenAI/Anthropic key?**
No. This server returns data. Your agent already has whatever model it uses.

**How fresh is the data?**
Live. Every call hits Google News at that moment; nothing is cached on our side.

**Can I search non-English news?**
Yes — set `language` and `country` (e.g. `language: "de"`, `country: "DE"`).

**What if I need thousands of articles, full text, or a CSV?**
Use the batch Actor: [google-news-scraper](https://fetchsmith.com/tools/google-news-scraper) — pay
per article, resolved URLs, full article bodies, date windows, ticker extraction.

## Related guides

- [fetchsmith.com/tools](https://fetchsmith.com/tools)
- [google-news-scraper](https://fetchsmith.com/tools/google-news-scraper) — the batch version: full article text, resolved URLs, CSV export
- [Google News RSS: public feeds, no key](https://fetchsmith.com/blog/google-news-rss-public-feeds-no-key)
- [Why the Google News RSS `description` is not a summary](https://fetchsmith.com/blog/google-news-rss-description-is-not-a-summary)
- [Decoding Google News RSS redirect links](https://fetchsmith.com/blog/decode-google-news-rss-redirect-links)
