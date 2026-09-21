# Google News Scraper

Search Google News and get clean, structured articles as JSON, CSV or Excel: headline (raw *and* with the ` - Publisher` suffix stripped), publisher name and domain, publish time, feed rank and the **real publisher URL** (Google's encoded redirect links are resolved for you). Optionally extract the **full article text** — body, author, image, keywords and section — from the publisher's page. Works for any language and country. Pay only per article returned.

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
| `topics` | array | Optional: browse Google News' built-in sections without knowing an RSS URL — `WORLD`, `NATION`, `BUSINESS`, `TECHNOLOGY`, `ENTERTAINMENT`, `SCIENCE`, `SPORTS`, `HEALTH` |
| `excludeWords` | array | Words/phrases to drop from every query, e.g. `["iphone"]` on a query `apple` removes iPhone coverage. Same effect as typing `-word` yourself, just a manageable list. Does not apply to `rssUrls` (fixed feeds, not search terms) |
| `siteFilter` | array | Restrict every query to these publisher domains, e.g. `["nytimes.com", "reuters.com"]` (OR'd, filtered by Google itself — no extra requests, no under-filled results). Applies to `queries` only |
| `excludeSites` | array | Drop results from these publisher domains, e.g. `["pinterest.com"]`. Applies to `queries` only |
| `timePeriod` | string | Only articles published within this window: `1h`, `6h`, `12h`, `1d`, `7d`, `30d`, `90d`, `1y`. Filtered by Google itself, so it costs no extra requests and you are never charged for articles outside the window. Applies to `queries` only |
| `publishedAfter` | string | `YYYY-MM-DD` — only articles published on or after this date. Overrides `timePeriod`. Applies to `queries` only |
| `publishedBefore` | string | `YYYY-MM-DD` — only articles published before this date. Overrides `timePeriod`. Applies to `queries` only |
| `language` | string | `hl` code such as `en-US`, `de`, `fr`, `pt-BR`, `ar`, `ja` (default `en-US`) |
| `country` | string | `gl` code such as `US`, `GB`, `DE`, `IN` (default `US`) |
| `maxItemsPerQuery` | integer | Up to 100 (Google's feed limit). Default `25` — decoding the real publisher URL is a 2-request round trip per article, and Google's per-IP rate limit on that endpoint has gotten slower recently, so 50+ articles can now take 4-5 minutes |
| `decodeUrls` | boolean | Resolve the publisher URL for each article (default true) |
| `fetchArticleBody` | boolean | Open each publisher page and extract the full article text, author, image, keywords and section (default false) |
| `articleBodyMaxChars` | integer | Truncate `articleBody` to this length (default 20000) |
| `extractTickers` | boolean | Pull stock tickers into a `tickers` array from the title (and article body, if `fetchArticleBody` is on). Rule-based, no extra request, costs nothing extra (default false) |
| `maxResults` | integer | Total cap across queries |
| `proxyConfiguration` | object | Apify Proxy for Google/publisher requests (default: on). Rotating IPs is the real fix for Google's URL-decode rate limit — see FAQ |

## Output (one item per article)
```json
{
  "title": "Apify raises new funding to scale web data platform - TechCrunch",
  "titleClean": "Apify raises new funding to scale web data platform",
  "url": "https://techcrunch.com/2026/09/02/apify-funding/",
  "googleNewsUrl": "https://news.google.com/rss/articles/CBMi...",
  "source": "TechCrunch",
  "sourceUrl": "https://techcrunch.com",
  "sourceDomain": "techcrunch.com",
  "publishedAt": "2026-09-02T07:00:00.000Z",
  "snippet": "Apify raises new funding to scale web data platform",
  "relatedArticles": [
    { "title": "Apify closes funding round", "source": "Reuters", "googleNewsUrl": "https://news.google.com/rss/articles/CBMi..." }
  ],
  "position": 1,
  "query": "apify",
  "topic": null,
  "language": "en-US",
  "country": "US"
}
```

A few of these are worth knowing about:

- **`titleClean`** — Google News always appends ` - Publisher` to the headline. `title` keeps it exactly as Google sends it; `titleClean` is the same headline with that suffix removed, which is what you usually want in a dashboard or digest.
- **`sourceDomain`** — the publisher's bare domain (`www.` stripped), so you can group or filter by outlet without parsing URLs yourself.
- **`position`** — the article's 1-based rank inside its own feed, so Google's relevance/recency ordering survives export and re-sorting.
- **`relatedArticles`** — when Google groups several outlets covering the same story, the other outlets land here with their own title, source and Google News URL. Costs no extra requests. Most items have an empty array; expect it on roughly 1% of results for a typical search.
- **`snippet`** — kept for backward compatibility, but be aware Google News RSS ships **no real article summary**: this field always repeats the headline. For an actual summary, turn on `fetchArticleBody` and read `articleDescription`.

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

With `extractTickers: true` each item also carries:

```json
{ "tickers": ["TSLA"] }
```

Rule-based and free (no extra request): it catches a cashtag (`$TSLA`), an exchange prefix/suffix (`NASDAQ:AAPL`, `AAPL:NASDAQ`), or a capitalized name immediately followed by `(TICKER)` — the most common real convention in financial headlines, e.g. "Tesla, Inc. (TSLA)". It deliberately does **not** match a bare capitalized word (`TSLA Stock Rises`) — that would flood results with false positives from ordinary acronyms (`WSJ`, `IPO`, `EV`, `SEC`, `UN`...), which are also excluded by name when they appear in the `(XXX)` position. The tradeoff: plain-text mentions with no notation at all are missed. `tickers` is always `[]` when nothing matches, never omitted.

## Pricing
`result` — charged per article returned. Failed feeds and duplicates are free, and full article text costs nothing extra. HTTP-only, no browser, so runs finish in seconds.

## Tips
- Combine `queries` with `when:1d` to get only fresh news for daily runs.
- Use `excludeWords` to drop off-topic coverage that shares a keyword with your query (e.g. exclude `iphone` when tracking `apple` as a company, not a product line).
- Google News' RSS search only understands the hour, day and year units in a time filter. `when:1m` and `when:12m` come back as an **empty feed, not an error** — which looks exactly like "no articles matched". That is why `timePeriod` offers `30d`, `90d` and `1y` rather than a "last month" option. If you type `when:`/`after:`/`before:` directly into a query, that query keeps your operator and `timePeriod` is not applied on top of it.
- `publishedAfter`/`publishedBefore` are Google's own `after:`/`before:` operators, and Google evaluates the day boundary in its locale, not in UTC. Expect the edges to be loose by a few hours — a `before:2026-09-05` query can return an article stamped `2026-09-05T01:51Z` (observed live). If you need a hard UTC cut-off, filter the `publishedAt` field yourself after the run.
- Use `rssUrls` for topic feeds, e.g. `https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=en-US&gl=US&ceid=US:en`.
- Turn off `decodeUrls` for the fastest runs if you only need headlines and sources.
- `fetchArticleBody` adds one request per article, so it is slower — but it costs no extra: you are still charged once per article returned, body or no body.
- Hard-paywalled publishers will come back as `blocked` or with a short teaser body; filter on `articleWordCount` if you only want complete articles.

## FAQ
**Why is `url` null on some articles?** Google occasionally rate-limits the redirect-resolving endpoint per IP; `googleNewsUrl` still works, and the run status message tells you how many articles were affected. Every run routes through rotating Apify Proxy IPs by default specifically to avoid this — if you turned `proxyConfiguration` off, turn it back on first.
**Does `fetchArticleBody` cost more?** No — you pay once per article returned whether or not the body was fetched.
**Why does `articleFetchStatus` say `blocked` or `no-body`?** The publisher likely paywalls the article or serves it without readable paragraph text; both are reported explicitly instead of a silently empty `articleBody`.
**Why did a run return 0 articles with status SUCCEEDED?** The status message distinguishes "Google returned nothing for this query" from "every result was a duplicate of another feed" from "the request failed" — check it before assuming your query is wrong.
**What's the difference between `siteFilter` and typing `site:` into `queries`?** None functionally — `siteFilter` just OR's multiple domains together (`site:a.com OR site:b.com`) and applies them to every query in your list, so you don't have to hand-append the operator to each one.
**What happens if Google's RSS feed has a transient blip mid-run?** Every feed and article-URL-decoding request is retried up to 3 times on a connection-level failure (measured at roughly 1 fresh request in 4 for HTTP/2 faults across this fleet, 2026-09-21) before that feed is given up on and named in the status message — a single blip no longer silently empties a query's results into `erroredFeeds`.

## Related guides
Engineering write-ups behind this Actor:
- [How we resolve Google News's encoded redirect links](https://fetchsmith.com/blog/decode-google-news-rss-redirect-links)
- [Why "JSON-LD only" article extraction fails on real news sites](https://fetchsmith.com/blog/json-ld-article-extraction-fails-on-real-news-sites)
- [Google News RSS's &lt;description&gt; field carries no article summary — here's what's actually in it](https://fetchsmith.com/blog/google-news-rss-description-is-not-a-summary)
- [A Try-for-free click shouldn't cost a first-time buyer $1.26 and five minutes](https://fetchsmith.com/blog/default-inputs-should-not-cost-you-five-minutes)

Only publicly available data is collected. Questions or feature requests: support@fetchsmith.com. Also available as a hosted API at https://fetchsmith.com/tools/google-news-scraper

Source code: https://github.com/Fetchsmith/fetchsmith/tree/main/actors/google-news-scraper
