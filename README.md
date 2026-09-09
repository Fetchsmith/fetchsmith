# FetchSmith

Pay-per-result web data extraction tools. Each Actor in `actors/` targets one site or one kind of page, reads only what is publicly accessible, and returns tidy JSON. They run on [Apify Store](https://apify.com/fetchsmith) with pay-per-event pricing and are also exposed as a hosted API at [fetchsmith.com](https://fetchsmith.com).

## Actors
| Actor | What it returns |
|---|---|
| [google-news-scraper](actors/google-news-scraper) | Google News articles with resolved publisher URLs, any language/country |
| [app-store-reviews-scraper](actors/app-store-reviews-scraper) | Apple App Store reviews for any app and storefront |
| [google-play-reviews-scraper](actors/google-play-reviews-scraper) | Google Play app reviews |
| [shopify-products-scraper](actors/shopify-products-scraper) | Full catalog of any Shopify store or collection |
| [hacker-news-scraper](actors/hacker-news-scraper) | Hacker News stories, comments, Ask/Show HN, Who's Hiring |

## Layout
- `actors/<slug>/` – one Apify Actor (Node 20, `apify` SDK, HTTP-only, pay-per-event charging)
- `actors/_template/` – starting point for new Actors
- `site/` – FastAPI app behind fetchsmith.com (catalog, docs, credit API)
- `bin/` – operations helpers (publishing, health checks, revenue snapshot)
- `notes/`, `tasks/`, `state/` – the autonomous operator's playbook, task queue and status

Built and maintained with heavy use of AI coding agents; every Actor is re-tested nightly. Issues and requests: support@fetchsmith.com
