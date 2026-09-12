---
title: Substack, Apple Podcasts, Google News and Hacker News — four free APIs where the first response isn't the finished product
description: All four platforms expose public JSON with no key, but none of them hand you the usable artifact on the first call — a null field, an encoded token, a thin stub record, or a query-syntax trap stand between you and the real data, and each fails silently.
date: 2026-09-12
tags: webscraping, api, publishing, json
---

Substack, Apple Podcasts, Google News and Hacker News all publish public content as plain JSON, no key, no login, no browser required. We build and maintain Actors against all four. They're unrelated products, but they share a specific shape of trap: **the first response you get back is a pointer to the content, a thin stub of it, or a query you've phrased wrong — never the finished thing — and getting the follow-up step wrong doesn't error, it just quietly gives you something other than what you asked for.**

## The four endpoints

| Platform | Endpoint | Auth | What the first call gives you |
|---|---|---|---|
| Substack | `GET <handle>.substack.com/api/v1/archive` | none | Post list with the body field present but always `null` |
| Apple Podcasts | `rss.marketingtools.apple.com/api/v2/.../podcasts.json` | none | Thin chart rows: id, name, artist — no feed URL, no episode count |
| Google News | `news.google.com/rss/search` | none | Article list where every link is an encoded redirect token, not a URL |
| Hacker News | `hn.algolia.com/api/v1/search` | none | Real hits — if your `tags` syntax means what you think it means |

## Two ways the trap shows up

### The content is one hop away, and the first response doesn't tell you that

Three of the four hand back something that *looks* complete but is a stub:

- **Substack's archive listing carries a `body_html` key on every row, and it is `null` on every single one** — regardless of word count or paywall status. The real article text is a second, per-post call away (`/api/v1/posts/<slug>`), same field name, this time populated. [Full write-up →](/blog/substack-full-text-json-api)
- **Apple Podcasts' chart endpoint gives you an ordered list of thin records** — id, name, artist, artwork, nothing else. No feed URL, no episode count, no description. Getting the actual show record (or its episodes, with the real MP3 URL) means joining each chart `id` against the separate `lookup` endpoint. [Full write-up →](/blog/apple-podcasts-public-json-api)
- **Google News RSS links are a base64-ish redirect token, not the publisher URL.** A browser resolves it client-side before bouncing you along; a scraper has to decode the token against Google's own endpoint to get the real `url` — and that decode step is rate-limited per IP, failing as a silent `url: null` with no error if you don't detect the 429 explicitly. [Full write-up →](/blog/decode-google-news-rss-redirect-links)

**Assert on:** don't treat "the key exists" as "the field is populated." Check the length of the string (or that the URL isn't the token you started with) before shipping a row as complete.

### The query itself has a syntax trap, and the wrong phrasing just returns a different, smaller answer

**Hacker News's Algolia-backed search API treats `tags=story,ask_hn` as an intersection, not a union** — commas AND together, and only a parenthesized group (`tags=(story,ask_hn)`) ORs. Get it backwards and the request still succeeds; you silently get the narrower, wrong result set with no error telling you the logic inverted. The same AND-composition is what lets `author` and `numericFilters` stack cleanly for things like pulling every reply in a specific Who's Hiring thread. [Full write-up →](/blog/hacker-news-algolia-tags-and-not-or)

Apple Podcasts has a version of this same trap on top of its stub problem: its chart endpoint silently **ignores** a genre query parameter and returns the unfiltered chart byte-for-byte, rather than erroring on an endpoint that was never built to filter by genre.

**Assert on:** never trust that a 200 with plausible-looking data means your parameter did anything. Change the parameter and diff the response against the unparameterized call — if they're identical, or if the result set only shrank, verify the direction of the filter before trusting it.

## A checklist that covers all four

1. **Check field length/content, not just field presence**, on any list/index endpoint before treating a row as complete — `body_html: null` and `body_html: "<p>..."`  both pass a naive "key exists" check.
2. **If a platform hands you a token or ID instead of a URL, resolve it before storing the row** — and detect rate-limit responses on the resolve step explicitly, since a silent failure there looks identical to "no data available."
3. **When a query language uses set operators (AND/OR), verify with real hit counts before trusting the syntax** — a smaller-than-expected result set that returns with no error is the signature of a boolean operator that didn't mean what you assumed.
4. **Diff a parameterized call against its unparameterized baseline.** If they match, your filter was silently ignored, not silently unmatched.

## Packaged versions

Each Actor below already does the extra hop or the correct query syntax for you — per-post fetch for Substack's real body text, chart-to-lookup joins for full podcast records, redirect-token decoding with 429 handling for Google News, and pre-built AND/OR-correct tag composition for Hacker News. HTTP-only, no browser, no proxy, priced per result with no start fee:

- [substack-scraper](/tools/substack-scraper) — full post text, comment trees, search
- [apple-podcasts-scraper](/tools/apple-podcasts-scraper) — charts, search, episodes with direct MP3 URLs, reviews
- [google-news-scraper](/tools/google-news-scraper) — resolved article URLs, full article text, all search operators
- [hacker-news-scraper](/tools/hacker-news-scraper) — stories, comments, Ask/Show HN, Who's Hiring, via the official Algolia API

The rest of the write-ups are on [the blog](/blog); the full Actor list is on [the tools page](/tools).

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned.*
