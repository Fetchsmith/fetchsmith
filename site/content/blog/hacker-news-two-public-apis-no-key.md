---
title: "Hacker News has two public JSON APIs, and neither one needs a key"
description: "Firebase's v0 API (official, items/users/live lists by id) and Algolia's Search API (official, full-text search) are both free and keyless. Measured live: what each returns, what neither one can do, and when to use which."
date: 2026-11-04
tags: webscraping, hacker-news, api, algolia
tool: hacker-news-scraper
---

Hacker News runs two separate public JSON APIs, both maintained by HN itself, both free, and neither one asking for a key, a login, or a quota signup. They do different jobs, and picking the wrong one for a task either can't be done, or costs far more requests than it should.

## Firebase v0: items, users, and live front-page lists — by id only

```
GET https://hacker-news.firebaseio.com/v0/item/<id>.json
GET https://hacker-news.firebaseio.com/v0/user/<username>.json
GET https://hacker-news.firebaseio.com/v0/topstories.json      # id list
GET https://hacker-news.firebaseio.com/v0/newstories.json      # id list
GET https://hacker-news.firebaseio.com/v0/askstories.json      # id list
GET https://hacker-news.firebaseio.com/v0/maxitem.json         # highest id ever assigned
GET https://hacker-news.firebaseio.com/v0/updates.json         # recently changed items/profiles
```

Measured live while writing this: `topstories.json` and `newstories.json` each return exactly **500** ids; `askstories.json` returns **39**. A single item (`item/50371633.json`, a comment) comes back as 456 bytes — `by`, `id`, `kids`, `parent`, `text`, `time`, `type`, nothing else. A user profile (`user/pg.json`) carries `karma` (157,316), `created` (a Unix timestamp), `about`, and a `submitted` array of **15,565** item ids — every post and comment that user has ever made, oldest-looking entries included, with no cap. `updates.json` right now lists 70 recently-changed item ids and 15 changed profile ids — this is how a long-running process can poll for edits without re-fetching everything.

The catch: **there is no search, and no bulk fetch.** Every id list gives you ids only — to get titles, points, or text you fan out one `item/<id>.json` request per id. Want "every story mentioning a keyword"? Firebase cannot do that at all; you'd have to walk `maxitem.json` downward and inspect every single item yourself, which is `maxitem` minus however far back you want to go, in HTTP requests. Firebase is correct for "what are today's front-page ids" or "get me item 50371633," and wrong for anything that needs filtering.

No `User-Agent` required, either — an explicitly empty one still returns `200`:

```
$ curl -s -A "" -o /dev/null -w "%{http_code}\n" \
    "https://hacker-news.firebaseio.com/v0/item/50371633.json"
200
```

## Algolia Search: full-text search, filters, and pagination — but capped at 1,000 hits

```
GET https://hn.algolia.com/api/v1/search?query=<term>&tags=<tag>&hitsPerPage=<n>&page=<n>
```

This is the backend behind hn.algolia.com itself, run by HN, not a third party — and it's the one [Hacker News Scraper](/tools/hacker-news-scraper) is built on, per the Actor's own README, specifically because it supports keyword search, date sorting, and tag filtering in one request instead of Firebase's one-id-at-a-time model. A live query for `apify` under `tags=story` returns `nbHits: 295` across `nbPages: 15` at the default page size — real numbers, not a sample. It also needs no `User-Agent` (empty one: `200`, same as Firebase) and no key.

The limit that matters: Algolia's own `search` endpoint **refuses to serve past the 1,000th hit of any single query**, no matter how high `nbHits` claims the true count is — verified in detail, including the exact plain-English message Algolia returns on the page past the edge, in [the dedicated write-up on the ceiling](/blog/hacker-news-1000-hit-search-ceiling). The fix is slicing a hot query by date window so each slice's `nbHits` stays under 1,000, not something either API tells you to do on its own.

## Which one to reach for

| Need | Use |
|---|---|
| Today's front page / Ask HN / Show HN ids | Firebase `topstories`/`askstories`/`showstories` |
| One specific item or user profile by id | Firebase `item/<id>`, `user/<username>` |
| Poll for recently-changed items without re-fetching everything | Firebase `updates.json` |
| Keyword search, date range, points/comments threshold | Algolia `search` (slice by date past 1,000 hits) |
| Filter by author, tag combination, or domain | Algolia `search` — see [the comma-means-AND gotcha](/blog/hacker-news-algolia-tags-and-not-or) before combining tags |

Neither API requires registration, and nothing about either one is rate-limited in a way that showed up while writing this — but both are a single shared backend serving the entire site's own traffic, so the courteous ceiling is "as few requests as the task actually needs," not "as many as the API will tolerate."

## Packaged version

[Hacker News Scraper on Apify](/go/hacker-news-scraper) wraps the Algolia side: keyword search, tag filtering, author/domain/date filters, a `watchLabel` mode for "only new since last run," and GitHub-repo enrichment on Show HN links — plus the date-slicing workaround for the 1,000-hit ceiling (`autoSplitLargeQueries`) built in, so a broad query doesn't quietly truncate. Pay only per item returned, no API key, no headless browser.

The same no-key pattern holds for [SEC Form 4 insider trades](/blog/sec-form-4-insider-trades-public-json-api-no-key) and [App Store reviews](/blog/app-store-reviews-public-json-api-no-key); the full catalogue is at [fetchsmith.com/tools](https://fetchsmith.com/tools).

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every status code, count and byte number above comes from a live request made while writing this post, not from documentation.*
