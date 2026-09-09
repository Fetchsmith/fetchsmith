# Google News Scraper

Search Google News and get clean, structured articles as JSON, CSV or Excel: title, publisher, publish time, snippet and the **real publisher URL** (Google's encoded redirect links are resolved for you). Works for any language and country. Pay only per article returned.

## Use cases
- Media monitoring and brand mentions for any keyword, in any market
- Feeding news into AI agents, RAG pipelines and newsletters
- Competitor and industry tracking (`site:` and `when:7d` operators supported)
- Building datasets of headlines by topic, region or publisher

## Input
| Field | Type | Description |
|---|---|---|
| `queries` | array | Search terms. Operators work: `"exact phrase"`, `site:reuters.com`, `when:7d`, `before:2026-01-01`, `after:2026-06-01` |
| `rssUrls` | array | Optional Google News RSS feed URLs (topics, sections, publications) |
| `language` | string | `hl` code such as `en-US`, `de`, `fr`, `pt-BR`, `ar`, `ja` (default `en-US`) |
| `country` | string | `gl` code such as `US`, `GB`, `DE`, `IN` (default `US`) |
| `maxItemsPerQuery` | integer | Up to 100 (Google's feed limit) |
| `decodeUrls` | boolean | Resolve the publisher URL for each article (default true) |
| `maxResults` | integer | Total cap across queries |

## Output (one item per article)
```json
{
  "title": "Apify raises new funding to scale web data platform - TechCrunch",
  "url": "https://techcrunch.com/2026/09/02/apify-funding/",
  "googleNewsUrl": "https://news.google.com/rss/articles/CBMi...",
  "source": "TechCrunch",
  "sourceUrl": "https://techcrunch.com",
  "publishedAt": "2026-09-02T07:00:00.000Z",
  "snippet": "Apify raises new funding to scale web data platform",
  "query": "apify",
  "language": "en-US",
  "country": "US"
}
```

## Pricing
`result` — charged per article returned. Failed feeds and duplicates are free. HTTP-only, no browser, so runs finish in seconds.

## Tips
- Combine `queries` with `when:1d` to get only fresh news for daily runs.
- Use `rssUrls` for topic feeds, e.g. `https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=en-US&gl=US&ceid=US:en`.
- Turn off `decodeUrls` for the fastest runs if you only need headlines and sources.

Only publicly available data is collected. Questions or feature requests: support@fetchsmith.com. Also available as a hosted API at https://fetchsmith.com/tools/google-news-scraper
