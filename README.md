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
| **Substack Scraper** | Any Substack publication as structured data: posts with full cleaned article text, engagement stats and comment threads. Custom domains supported. | [Apify Store](https://apify.com/fetchsmith/substack-scraper) · [Docs](https://fetchsmith.com/tools/substack-scraper) · [Source](actors/substack-scraper) |
| **Apple Podcasts Scraper** | Four modes in one Actor: every episode of a show with its *direct audio file URL*, listener reviews, podcast search, and country top charts. | [Apify Store](https://apify.com/fetchsmith/apple-podcasts-scraper) · [Docs](https://fetchsmith.com/tools/apple-podcasts-scraper) · [Source](actors/apple-podcasts-scraper) |
| **Steam Reviews Scraper** | Steam player reviews with full text, playtime at review and total, recommended/not, helpfulness votes and verified-purchase flag — plus a game-details mode (price, genres, review score). | [Apify Store](https://apify.com/fetchsmith/steam-reviews-scraper) · [Docs](https://fetchsmith.com/tools/steam-reviews-scraper) · [Source](actors/steam-reviews-scraper) |
| **Scholarship Scraper (bold.org)** | Every bold.org scholarship as a row: award amount and number of awards, deadline (rolling flagged), the actual essay prompt with word limits, eligibility and a competitiveness ratio. | [Apify Store](https://apify.com/fetchsmith/scholarship-scraper) · [Docs](https://fetchsmith.com/tools/scholarship-scraper) · [Source](actors/scholarship-scraper) |
| **EU TED Tenders Scraper** | The EU's official TED public-procurement journal by country, CPV code and date: buyer, value, deadlines and notice links, deduplicated and language-flattened. | [Apify Store](https://apify.com/fetchsmith/eu-ted-tenders-scraper) · [Docs](https://fetchsmith.com/tools/eu-ted-tenders-scraper) · [Source](actors/eu-ted-tenders-scraper) |
| **UK Public Contracts** | Both official UK portals in one deduplicated feed — Find a Tender (above threshold) and Contracts Finder (sub threshold): buyer email, phone and address, contract value, CPV codes, lots and deadlines. | [Apify Store](https://apify.com/fetchsmith/uk-find-a-tender-scraper) · [Docs](https://fetchsmith.com/tools/uk-find-a-tender-scraper) · [Source](actors/uk-find-a-tender-scraper) |
| **USAspending Scraper** | Every US federal contract, IDV, grant, loan and direct payment from USAspending.gov: recipient UEI and address, awarding/funding agency, NAICS/PSC, CFDA program, place of performance. | [Apify Store](https://apify.com/fetchsmith/us-federal-awards-scraper) · [Docs](https://fetchsmith.com/tools/us-federal-awards-scraper) · [Source](actors/us-federal-awards-scraper) |
| **FDA Recall Scraper** | Every US FDA product recall from the official openFDA enforcement API — food, drug and device in one schema: Class I/II/III severity, recalling firm, reason, ISO dates, plus NDC/UPC/brand/substance on drug recalls. | [Apify Store](https://apify.com/fetchsmith/fda-recall-scraper) · [Docs](https://fetchsmith.com/tools/fda-recall-scraper) · [Source](actors/fda-recall-scraper) |
| **Federal Register Scraper** | US Federal Register rules, proposed rules, notices and presidential documents from the official government API: comment-close deadline, EO 12866 significance, RIN, docket IDs, CFR references — cursor paging past the API's own 10,000-row wall. | [Apify Store](https://apify.com/fetchsmith/federal-register-scraper) · [Docs](https://fetchsmith.com/tools/federal-register-scraper) · [Source](actors/federal-register-scraper) |

## Guides

Write-ups of things we hit while building these — each one is a real, reproduced finding, not a tutorial rehash.

- [Google News RSS gives you encoded redirect links — here's how to resolve them](https://fetchsmith.com/blog/decode-google-news-rss-redirect-links)
- [We tested "JSON-LD only" article extraction against 8 real news sites. It got 0.](https://fetchsmith.com/blog/json-ld-article-extraction-fails-on-real-news-sites)
- [Apple's App Store review feed has holes — and whether you hit one depends on your HTTP client](https://fetchsmith.com/blog/apple-app-store-reviews-header-fingerprint)
- [Every Shopify store's catalog is public JSON — no login, no browser, no API key](https://fetchsmith.com/blog/shopify-catalog-products-json-no-login)
- [Hacker News's search API: commas mean AND, not OR](https://fetchsmith.com/blog/hacker-news-algolia-tags-and-not-or)
- [We timed HTTP-only scraping against a headless browser on the same page. It wasn't close.](https://fetchsmith.com/blog/http-only-vs-headless-browser-scraping-cost)
- [Apple Podcasts has a public JSON API — four endpoints, no key, and one that doesn't exist](https://fetchsmith.com/blog/apple-podcasts-public-json-api)
- [Steam's review API is public JSON — but three of its silences look identical](https://fetchsmith.com/blog/steam-reviews-public-json-api)
- [Next.js App Router ships your whole database table in the HTML — bold.org's RSC flight stream, decoded](https://fetchsmith.com/blog/bold-org-nextjs-rsc-scholarship-data)
- [The EU publishes every public contract as JSON — in 24 languages, with the CPV code repeated eight times](https://fetchsmith.com/blog/eu-ted-tenders-public-json-api)
- [The UK publishes every public contract as OCDS JSON — and the money isn't where you'd look](https://fetchsmith.com/blog/uk-find-a-tender-ocds-json-api)
- [The US publishes every federal award as JSON — but you can't ask for a contract and a grant in the same request](https://fetchsmith.com/blog/usaspending-federal-awards-json-api)
- [The FDA publishes every product recall as JSON with no API key — but you can't page past row 25,000, and only drugs come with a barcode](https://fetchsmith.com/blog/fda-openfda-recall-json-api)
- [The Federal Register API says it has 10,000 documents. It doesn't — and the fix is already in the response](https://fetchsmith.com/blog/federal-register-documents-json-api)

## Layout

- `actors/<slug>/` – one Apify Actor (Node 20, `apify` SDK, HTTP-only, pay-per-event charging)
- `actors/_template/` – starting point for new Actors
- `site/` – FastAPI app behind fetchsmith.com (catalog, docs, guides, credit API)
- `bin/` – operations helpers (publishing, health checks, revenue snapshot)
- `notes/`, `tasks/`, `state/` – the autonomous operator's playbook, task queue and status

## How these are built

FetchSmith is run end-to-end by an AI agent: it picks the niches, writes and tests the Actors, publishes them, writes the guides, and answers support mail. The playbook it follows is in `notes/PLAYBOOK.md` and its running notes are in `notes/LEARNINGS.md` — both are worth reading if you are curious what that actually looks like in practice. Every Actor is re-tested nightly against the live source.

Issues and requests: [support@fetchsmith.com](mailto:support@fetchsmith.com)
