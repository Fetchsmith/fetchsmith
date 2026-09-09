# Google News Scraper

Search Google News and get clean, structured articles as JSON, CSV or Excel: title, publisher, publish time, snippet and the **real publisher URL** (Google's encoded redirect links are resolved for you). Optionally extract the **full article text** — body, author, image, keywords and section — from the publisher's page. Works for any language and country. Pay only per article returned.

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
| `fetchArticleBody` | boolean | Open each publisher page and extract the full article text, author, image, keywords and section (default false) |
| `articleBodyMaxChars` | integer | Truncate `articleBody` to this length (default 20000) |
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

With `fetchArticleBody: true` each item also carries:

```json
{
  "articleBody": "Apify, the web scraping and automation platform, said on Tuesday...",
  "articleWordCount": 812,
  "articleBodyTruncated": false,
  "articleBodySource": "jsonld",
  "articleAuthor": "Jane Doe",
  "articleImage": "https://techcrunch.com/wp-content/uploads/2026/09/apify.jpg",
  "articleKeywords": ["funding", "web scraping"],
  "articleSection": "Startups",
  "articleDescription": "The platform raised a new round to...",
  "articlePublishedAt": "2026-09-02T07:00:00Z",
  "articleModifiedAt": "2026-09-02T09:14:00Z",
  "articleFetchStatus": "ok"
}
```

`articleFetchStatus` always tells you where the text came from or why it is missing: `ok`, `blocked` (publisher refused the request, e.g. hard paywall), `no-body` (page had no readable article text), `error` (request failed) or `no-url` (Google's redirect could not be resolved). Body extraction reads the page's Article JSON-LD first and falls back to the article paragraphs; publishers that serve different HTML to different clients are retried under several request fingerprints, and the one that works is reused for the rest of that publisher's articles.

## Pricing
`result` — charged per article returned. Failed feeds and duplicates are free, and full article text costs nothing extra. HTTP-only, no browser, so runs finish in seconds.

## Tips
- Combine `queries` with `when:1d` to get only fresh news for daily runs.
- Use `rssUrls` for topic feeds, e.g. `https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=en-US&gl=US&ceid=US:en`.
- Turn off `decodeUrls` for the fastest runs if you only need headlines and sources.
- `fetchArticleBody` adds one request per article, so it is slower — but it costs no extra: you are still charged once per article returned, body or no body.
- Hard-paywalled publishers will come back as `blocked` or with a short teaser body; filter on `articleWordCount` if you only want complete articles.

## FAQ
**Why is `url` null on some articles?** Google occasionally rate-limits the redirect-resolving endpoint; `googleNewsUrl` still works, and the run status message tells you how many articles were affected.
**Does `fetchArticleBody` cost more?** No — you pay once per article returned whether or not the body was fetched.
**Why does `articleFetchStatus` say `blocked` or `no-body`?** The publisher likely paywalls the article or serves it without readable paragraph text; both are reported explicitly instead of a silently empty `articleBody`.
**Why did a run return 0 articles with status SUCCEEDED?** The status message distinguishes "Google returned nothing for this query" from "every result was a duplicate of another feed" from "the request failed" — check it before assuming your query is wrong.

Only publicly available data is collected. Questions or feature requests: support@fetchsmith.com. Also available as a hosted API at https://fetchsmith.com/tools/google-news-scraper

Source code: https://github.com/Fetchsmith/fetchsmith/tree/main/actors/google-news-scraper
