# Apple Podcasts has four public JSON APIs, no key required — and a fifth everyone assumes exists

Scraping Apple Podcasts looks like a browser job. The web player is a JavaScript app, show pages render client-side, and the reflex is to reach for Playwright.

You don't need it. Everything worth having sits behind four public JSON endpoints that take no key, no token and no cookie, and answer a plain `GET` from any IP. We built an [Apple Podcasts scraper](https://apify.com/fetchsmith/apple-podcasts-scraper) on exactly these — HTTP-only, no headless browser anywhere.

Here's the map, and the two failure modes that will ship silently if you don't look for them.

## 1. Charts

```
https://rss.marketingtools.apple.com/api/v2/us/podcasts/top/50/podcasts.json
```

Swap `us` for any storefront (`gb`, `de`, `jp`). Returns `feed.results` as an ordered array — **the rank is the array position, there is no rank field**, which is easy to lose if you map the objects and drop the order. `feed.updated` carries a real freshness stamp; when we pulled it while writing this it was about a minute old.

Rows are thin: `id`, `name`, `artistName`, `url`, `genres`, `artworkUrl100`. No feed URL, no episode count, no description — join on `id` against endpoint 3 for those.

## 2. Search

```
https://itunes.apple.com/search?term=true+crime&media=podcast&country=us&limit=25
```

The old iTunes Search API is still up and still free. `media=podcast` returns full show records — same shape as lookup — so a search doubles as a metadata fetch. No second call per hit.

## 3. Show metadata

```
https://itunes.apple.com/lookup?id=1434243584&country=us
```

One full record: `collectionName`, `artistName`, `primaryGenreName`, `genres`, `trackCount`, `releaseDate`, `artworkUrl600`, content advisory — and `feedUrl`, the publisher's actual RSS feed, if you want to leave Apple's ecosystem entirely.

## 4. Episodes — the one that saves the most work

```
https://itunes.apple.com/lookup?id=1434243584&country=us&entity=podcastEpisode&limit=100
```

One request returns **the show record and its recent episodes together**. In our check, `limit=5` came back with `resultCount: 6` — one `wrapperType: "track"` (the show) plus five `wrapperType: "podcastEpisode"` rows. Always filter on `wrapperType` instead of assuming `results` is homogeneous, and note you get the show metadata free in the same response.

Each episode row carries ~26 fields, and the valuable one is **`episodeUrl`: the direct audio file**. Not a player page — the actual MP3, usually on the publisher's CDN. Watch the naming: there is no `audioUrl`. The MP3 is `episodeUrl`, the human-readable Apple page is `trackViewUrl`. We had these backwards on the first pass and only caught it by reading a real output row instead of trusting the field name we expected.

`limit` caps out well short of "every episode ever", so treat this as a recent-episodes feed. For a full back catalogue, take `feedUrl` and parse the publisher's RSS.

## 5. Reviews, and why the feed looks broken when it isn't

```
https://itunes.apple.com/us/rss/customerreviews/id=1434243584/sortBy=mostRecent/page=1/json
```

Up to 50 entries per page, roughly 10 pages deep. Everything is wrapped in `{"label": ...}` objects, so plan on an unwrapping helper, and when a feed has exactly one review, `feed.entry` is an **object, not an array** — normalize it or your `.map()` throws.

The real trap: this feed is full of **holes**. For a given id/storefront/sort, some page numbers return a well-formed but empty feed while *later* pages return a full 50 — page 1 empty and page 5 full is common. It's sticky rather than random (repeat the request, get the same empty result), which is exactly why it reads as an outage and sends people hunting for a fingerprinting fix.

The fix is not a browser and not UA rotation. **Scan the whole 1–10 page range and skip the holes** instead of `break`ing on the first empty page, then dedupe by review id. If you `break` on empty — which is the natural way to write pagination — you will conclude a show has zero reviews when it has hundreds.

(There is a second, separate effect: an iPhone/iPad User-Agent gets a different, independently paginated index over the same review pool. On one title, a `curl` sweep and an iOS sweep returned 50 and 200 unique reviews with *zero* overlap. Union both if you want maximum coverage.)

## The endpoint that doesn't exist: genre charts

Every few weeks someone wants "top 50 Comedy podcasts in Germany". It looks like it should work — Apple has genre IDs, they appear in every record, and the older iTunes RSS generator did have genre-scoped chart feeds. So people guess at URLs. We tried the plausible shapes:

| URL shape | Result |
|---|---|
| `.../top/5/genre=1489/podcasts.json` | 404 |
| `.../top/5/1489/podcasts.json` | 404 |
| `.../top-shows/5/genre=1489/podcasts.json` | 404 |
| `.../top/5/podcasts.json?g=1489` | **200 — same list, same order as the unfiltered chart** |

That last row is the whole problem. The query-param form doesn't error. It silently ignores your filter and hands back the overall chart. Build a "top comedy podcasts" pipeline on it and you get a plausible 200 with completely wrong data and no signal anything went wrong.

We proved it by diffing the two responses: same ids in the same order, and identical field-for-field once you drop `feed.updated` — which is a per-second freshness stamp, so a naive byte-comparison of two sequential requests can disagree for reasons that have nothing to do with your filter. That's worth knowing before you build the diff check this post is about to recommend: **strip the timestamps before you compare, or you'll conclude a parameter worked when it did nothing.**

There is no public deep-genre chart. The honest path is to pull the overall chart, join each `id` against `lookup`, and filter on `primaryGenreName` — accepting you can only surface genre leaders that already rank overall.

One more silent one: an invalid storefront (`.../api/v2/zz/...`) returns **HTTP 500 with an HTML error page**, not a JSON error. Pipe that straight into a JSON parser and your user gets a `SyntaxError` about an unexpected `<`, which tells them nothing about the actual problem — their country code. Sniff the status or content type first.

## The general lesson

Two of the five findings above are negative results, and both would ship silently: the genre chart that 200s with wrong data, and the review pagination that reports zero because you stopped at the first hole.

When you're mapping an undocumented API, **a `200` is not evidence that your parameter did anything.** Change the parameter, diff the response against the unparameterized call, and if they're identical your filter was ignored. Same discipline on pagination: prove an empty page means "end of data" before you let it terminate your loop.

Full write-up with the endpoint-by-endpoint detail is [on our blog](https://fetchsmith.com/blog/apple-podcasts-public-json-api); the packaged version is [apple-podcasts-scraper on Apify](https://apify.com/fetchsmith/apple-podcasts-scraper) — charts, shows, episodes and reviews behind one input, HTTP-only, no browser, no proxy required.

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every endpoint, status code and field name above comes from live requests, not from documentation.*
