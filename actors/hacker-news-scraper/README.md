# Hacker News Scraper

Search or browse Hacker News (stories, comments, Ask HN, Show HN, jobs, and monthly **Who's Hiring** threads) using the official Algolia Search API — fast, reliable, no scraping fragility. Pay only per item returned.

## Use cases
- Track mentions of your product, company or keyword on HN
- Pull the newest **Who's Hiring** / **Who Wants to Be Hired** threads for job-market research
- Feed trending tech discussions into AI agents, newsletters or dashboards
- Build datasets of Show HN launches or Ask HN discussions by topic

## Input
| Field | Type | Description |
|---|---|---|
| `queries` | array | Keywords to search. Leave empty to just browse by tag/date. |
| `tags` | array | `story`, `comment`, `poll`, `ask_hn`, `show_hn`, `job` (default `["story"]`) |
| `includeComments` | boolean | Fetch comment text when `tags` includes `comment` |
| `sortBy` | string | `relevance` or `date` (newest first) |
| `minPoints` | integer | Only items with at least this many points |
| `postedAfter` / `postedBefore` | string | ISO date bounds |
| `maxItemsPerQuery` | integer | Cap per query (up to 1000) |
| `maxResults` | integer | Overall cap |

## Output (one item per story/comment)
```json
{
  "id": "41930211",
  "type": "story",
  "title": "Show HN: FetchSmith – pay-per-use scraper APIs",
  "url": "https://fetchsmith.com",
  "hnUrl": "https://news.ycombinator.com/item?id=41930211",
  "author": "someuser",
  "points": 142,
  "numComments": 38,
  "createdAt": "2026-09-01T12:00:00.000Z",
  "query": "fetchsmith"
}
```

## Pricing
`result` — charged per item returned. Empty queries and failed pages are free.

## Tips
- For the current "Who is hiring?" thread: set `queries` to `["Ask HN: Who is hiring"]`, `tags: ["story"]`, `sortBy: "date"`, `maxItemsPerQuery: 1` to find the thread, or use `tags: ["comment"]` with `postedAfter` set to the 1st of the month to pull all replies.
- Use `sortBy: "date"` for a live monitoring feed of new mentions of your keyword.

Only publicly available data is collected via HN's official search API. Questions or feature requests: support@fetchsmith.com. Also available as a hosted API at https://fetchsmith.com/tools/hacker-news-scraper

Source code: https://github.com/Fetchsmith/fetchsmith/tree/main/actors/hacker-news-scraper
