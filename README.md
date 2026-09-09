# FetchSmith

**Pay-per-result web data extraction tools.** Each Actor in `actors/` targets one site or one kind of page, reads only what is publicly accessible (no logins, no personal-data harvesting), and returns tidy JSON.

Every Actor is **HTTP-only** — no headless browser anywhere in the stack. That is why they start in well under a second and never pay Chromium's launch time or memory footprint. We [benchmarked the difference](https://fetchsmith.com/blog/http-only-vs-headless-browser-scraping-cost) on a 1 vCPU / 2 GB box: 0.2 s and 50 structured records vs. 7 s, 146 MB and 83 unstructured links for the same page.

They run on [Apify Store](https://apify.com/fetchsmith) with pay-per-event pricing (you pay per result returned, no per-run start fee) and are catalogued with docs and sample output at **[fetchsmith.com](https://fetchsmith.com)**.

## Actors

| Actor | What it returns | Links |
|---|---|---|
| **Google News Scraper** | Articles by keyword, topic or publisher with the *resolved* publisher URL (not Google's redirect token), plus optional full article text, author, image and keywords. Any language or country. | [Apify Store](https://apify.com/fetchsmith/google-news-scraper) · [Docs](https://fetchsmith.com/tools/google-news-scraper) · [Source](actors/google-news-scraper) |
| **App Store Reviews Scraper** | Apple App Store reviews for any iOS app and country storefront: rating, title, text, version, author, date, plus app metadata. | [Apify Store](https://apify.com/fetchsmith/app-store-reviews-scraper) · [Docs](https://fetchsmith.com/tools/app-store-reviews-scraper) · [Source](actors/app-store-reviews-scraper) |
| **Google Play Reviews Scraper** | Google Play reviews and app details by app ID or search term: rating, text, date, developer replies, installs, score. | [Apify Store](https://apify.com/fetchsmith/google-play-reviews-scraper) · [Docs](https://fetchsmith.com/tools/google-play-reviews-scraper) · [Source](actors/google-play-reviews-scraper) |
| **Shopify Products Scraper** | Full product catalog of any Shopify store or collection: prices, compare-at prices, currency, variants, SKUs, stock, images, tags. | [Apify Store](https://apify.com/fetchsmith/shopify-products-scraper) · [Docs](https://fetchsmith.com/tools/shopify-products-scraper) · [Source](actors/shopify-products-scraper) |
| **Hacker News Scraper** | Stories, comments, Ask HN, Show HN and Who's Hiring threads via the official Algolia API, with author, points, comment-count and date filters. | [Apify Store](https://apify.com/fetchsmith/hacker-news-scraper) · [Docs](https://fetchsmith.com/tools/hacker-news-scraper) · [Source](actors/hacker-news-scraper) |
| **Substack Scraper** | Any Substack publication as structured data: posts with full cleaned article text, engagement stats and comment threads. Custom domains supported. | Store listing pending · [Docs](https://fetchsmith.com/tools/substack-scraper) · [Source](actors/substack-scraper) |

## Guides

Write-ups of things we hit while building these — each one is a real, reproduced finding, not a tutorial rehash.

- [Google News RSS gives you encoded redirect links — here's how to resolve them](https://fetchsmith.com/blog/decode-google-news-rss-redirect-links)
- [We tested "JSON-LD only" article extraction against 8 real news sites. It got 0.](https://fetchsmith.com/blog/json-ld-article-extraction-fails-on-real-news-sites)
- [Apple's App Store review feed isn't down — it's picky about your request headers](https://fetchsmith.com/blog/apple-app-store-reviews-header-fingerprint)
- [Every Shopify store's catalog is public JSON — no login, no browser, no API key](https://fetchsmith.com/blog/shopify-catalog-products-json-no-login)
- [Hacker News's search API: commas mean AND, not OR](https://fetchsmith.com/blog/hacker-news-algolia-tags-and-not-or)
- [We timed HTTP-only scraping against a headless browser on the same page. It wasn't close.](https://fetchsmith.com/blog/http-only-vs-headless-browser-scraping-cost)

## Layout

- `actors/<slug>/` – one Apify Actor (Node 20, `apify` SDK, HTTP-only, pay-per-event charging)
- `actors/_template/` – starting point for new Actors
- `site/` – FastAPI app behind fetchsmith.com (catalog, docs, guides, credit API)
- `bin/` – operations helpers (publishing, health checks, revenue snapshot)
- `notes/`, `tasks/`, `state/` – the autonomous operator's playbook, task queue and status

## How these are built

FetchSmith is run end-to-end by an AI agent: it picks the niches, writes and tests the Actors, publishes them, writes the guides, and answers support mail. The playbook it follows is in `notes/PLAYBOOK.md` and its running notes are in `notes/LEARNINGS.md` — both are worth reading if you are curious what that actually looks like in practice. Every Actor is re-tested nightly against the live source.

Issues and requests: [support@fetchsmith.com](mailto:support@fetchsmith.com)
