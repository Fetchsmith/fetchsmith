---
title: "Hacker News's search API: commas mean AND, not OR — and it changes how you should query it"
description: "The Algolia-powered HN Search API silently treats tags=story,ask_hn as an intersection, not a union. Verified live against 44.7M vs 2.25M hit counts, plus how Who's Hiring threads and their replies are tagged."
date: 2026-09-09
tags: webscraping, hacker-news, api, algolia
tool: hacker-news-scraper
---

Hacker News doesn't have an official public API for search — what everyone actually uses is Algolia's `hn.algolia.com/api/v1/search`, the same backend that powers hn.algolia.com itself. It's fast, reliable, and needs no key. But its `tags` parameter has a syntax gotcha that will silently return the wrong result set if you assume comma means "or."

## Comma is AND

`tags=story,ask_hn` does not mean "stories or Ask HN posts." It means the **intersection**: items tagged both `story` AND `ask_hn`. We verified this against real hit counts:

| Query | `nbHits` |
|---|---|
| `tags=story` | 44,728,722 |
| `tags=ask_hn` | 2,253,271 |
| `tags=story,ask_hn` | 2,253,271 |

The intersection count exactly equals the smaller set (every Ask HN post is also tagged `story`), which is exactly what an AND should produce. If you wanted "stories or Ask HN posts" and used a comma expecting OR, you'd have silently gotten the smaller, more restrictive set with no error — the request still succeeds, so nothing tells you the logic was inverted from what you intended.

The same AND behavior is what makes `author` and `minComments` filters composable in [Hacker News Scraper](/tools/hacker-news-scraper): `tags=story,author_pg` returns only items where `author` is literally `pg` (verified: 5/5 hits authored by `pg`), and combining it with a `numericFilters=num_comments>=1000` clause ANDs a third condition on top with no extra request.

## Parentheses mean OR

To actually get a union, wrap the alternatives in parentheses: `tags=(story,ask_hn)`. That returns items with *either* tag — verified live, the hit list mixes plain stories with no `ask_hn` tag alongside genuine Ask HN posts, unlike the comma form which returned only items carrying both tags.

The rule generalizes: commas at the top level of a `tags` value AND together; a parenthesized, comma-separated group ORs together the values inside it. Mixing the two lets you express queries like "(`story` or `job`) AND `author_whoishiring`" in one request instead of fetching pages and filtering client-side.

## How Who's Hiring threads and their replies are actually tagged

The monthly "Ask HN: Who is hiring?" threads are themselves stories, but the account that owns them (`author_whoishiring`) is a queryable tag. This is real output against the live index:

```
tags=story,author_whoishiring, query="Who is hiring"
→ "Ask HN: Who is hiring? (September 2026)"      2026-09-01T15:01:17Z
→ "Ask HN: Who wants to be hired? (September 2026)" 2026-09-01T15:01:17Z
→ "Ask HN: Who is hiring? (August 2026)"          2026-08-03T15:00:54Z
```

To pull every reply to a specific thread (i.e. every job posting in that month's thread), AND `comment` with the parent story's numeric ID: `tags=comment,story_<id>`. That's the same AND semantics as above — it's an intersection of "is a comment" and "belongs to this specific story" — and it's how [Hacker News Scraper](/tools/hacker-news-scraper) pulls a full month of postings without scraping the HTML thread page or guessing at pagination.

## Practical takeaways

- `tags=a,b` is AND (intersection). `tags=(a,b)` is OR (union). Getting this backwards doesn't error — it just quietly returns the wrong, usually smaller, result set.
- `author` and `minComments`/`numericFilters` compose cleanly on top of tag AND-logic — no need for client-side filtering or extra requests.
- Who's Hiring / Who Wants to Be Hired threads are ordinary stories owned by `author_whoishiring`; their replies are reachable by ANDing `comment` with `story_<parent id>`, not by parsing the thread page.
- This is Algolia's search-index API, not HN's live site — it's read replica data, not scraping, so there's no fragility tied to HN's HTML changing.

This is exactly the query logic behind [Hacker News Scraper](/tools/hacker-news-scraper)'s `tags`, `author`, and `minComments` inputs — pay only for items actually returned, no charge for empty queries.

A silently-wrong query is the same failure shape as three other content APIs' silently-stubbed responses — see the [roundup](/blog/public-content-apis-hidden-second-step) for Substack, Apple Podcasts and Google News.

*Built by [FetchSmith](/) — HTTP-only Apify Actors, AI-assisted development, disclosed.*

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned.*
