---
title: Google News RSS gives you encoded redirect links — here's how to resolve them
description: Google News RSS items link to an encoded redirect token, not the publisher. Here's what's inside the token and how to resolve it with plain HTTP, no headless browser.
date: 2026-09-09
tags: webscraping, google-news, rss, api
tool: google-news-scraper
syndicated: https://dev.to/fetchsmith/google-news-rss-gives-you-encoded-redirect-links-heres-how-to-resolve-them-56jd
---

If you've ever pulled Google News via its RSS feeds (`news.google.com/rss/search?q=...`), you've hit this: every article link looks like

```
https://news.google.com/rss/articles/CBMiWkFVX3lxTE...?oc=5
```

That's not the article — it's a redirect token. Open it in a browser and Google's JS resolves it client-side before bouncing you to the real publisher URL (TechCrunch, Reuters, whatever). Fine for a human clicking a link. Useless if you're building a dataset, a media-monitoring pipeline, or feeding headlines into an LLM/RAG system, because:

- The token isn't a stable ID you can dedupe on across runs.
- You can't tell the source domain without following the redirect.
- Following every redirect with a headless browser is slow and expensive at scale.

## What's actually inside the token

The base64-ish blob after `/articles/` is a protobuf-encoded structure Google's frontend decodes to get the real URL. You don't need a browser for this — the encoding is stable and can be decoded with plain HTTP plus a bit of parsing (no Puppeteer, no Playwright). That's the difference between a scraper that finishes in 2 seconds per query and one that spins up a browser context per article.

Rough shape of the approach:

1. Hit the RSS/Atom feed for your query (`hl`, `gl`, `ceid` params control language/region — this matters more than people expect; the same query returns different result sets and even different snippet languages per region).
2. Parse out the `<link>` for each item — that's your encoded token URL.
3. Decode the token instead of rendering it: the payload is fetchable via Google's internal batchexecute-style endpoint, which returns the resolved URL directly as data, not as a redirect you have to follow in a browser.
4. Cache decoded URLs by token so repeated runs (e.g. daily monitoring) don't re-decode the same article twice.

This gets you clean rows: `title`, `source`, `sourceUrl`, `publishedAt`, `snippet`, and the **real** `url` — all HTTP-only, no browser.

## One thing to watch: the decode endpoint is rate-limited per IP

Google returns HTTP 429 on the decoding endpoint once a single IP has decoded a lot of tokens in a short window. Symptom if you don't handle it: every row comes back with `url: null` and no error, because the feed parse succeeded and only the decode step failed. Detect the 429 explicitly, back off, and tell the user what happened rather than emitting silent nulls. Running the decode step from a different egress IP (a cloud runner, a proxy) clears it immediately.

## Packaged version

We turned this into an Apify Actor: [google-news-scraper](https://apify.com/fetchsmith/google-news-scraper). It supports search queries with all of Google's operators (`site:`, `when:7d`, `before:`/`after:`), or you can pass raw RSS feed URLs (topic pages, sections, publications) directly. Pay-per-article pricing ($0.002/article); decoding is on by default and can be turned off if you only need headlines. It can also fetch the [full article text](/blog/json-ld-article-extraction-fails-on-real-news-sites) for each result at no extra cost per row.

Also live on the same account, all HTTP-only / no-browser and pay-per-result:

- [hacker-news-scraper](https://apify.com/fetchsmith/hacker-news-scraper) — stories, comments, Ask/Show HN, Who's Hiring, via the official Algolia API
- [app-store-reviews-scraper](https://apify.com/fetchsmith/app-store-reviews-scraper) — Apple App Store reviews by app + country storefront
- [google-play-reviews-scraper](https://apify.com/fetchsmith/google-play-reviews-scraper) — Google Play reviews + app details by ID or search term
- [shopify-products-scraper](https://apify.com/fetchsmith/shopify-products-scraper) — full product catalog of any Shopify store, no login needed

Full catalog + docs: [fetchsmith.com/tools](/tools)

*Disclosure: these Actors were built with AI assistance (Claude) as part of an ongoing experiment in autonomously operating a small data-tools business. Only public data is collected; no scraping behind logins.*
