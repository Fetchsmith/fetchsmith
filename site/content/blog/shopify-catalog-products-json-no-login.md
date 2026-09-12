---
title: Every Shopify store's catalog is public JSON — no login, no browser, no API key
description: "/products.json and /meta.json expose a Shopify store's full catalog, prices, variants and currency to anyone, paginated, with zero authentication. Here's the shape of it and what most scrapers still get wrong."
date: 2026-09-09
tags: webscraping, shopify, ecommerce, api
tool: shopify-products-scraper
---

Shopify storefronts ship their entire product catalog as plain JSON, at a URL every store has, with no authentication and no rate-limit key. If you can load the store's homepage in a browser, you can fetch its full catalog with `curl`.

## The endpoint

Every Shopify store exposes:

```
GET https://<store-domain>/products.json?limit=250&page=1
```

This works identically on `*.myshopify.com` backends and on custom storefront domains (`www.allbirds.com`, `gymshark.com`, whatever the merchant put on their DNS) — Shopify doesn't gate the endpoint behind the domain type. `limit` caps out at 250 per page; paginate with `page=2`, `page=3`, ... until a page comes back with an empty `products` array, which is your signal to stop (Shopify doesn't return a total count or a `Link` header for this endpoint, so "empty page" is the only reliable end-of-catalog marker).

Scope to a single collection instead of the whole store by inserting the collection handle:

```
GET https://<store-domain>/collections/<handle>/products.json?limit=250&page=1
```

Each product in the response carries `variants[]` (SKU, price, weight in grams, availability, option values like size/color) and `images[]`. There's no `currency` field on the product payload itself — for that you need a second, separate request:

```
GET https://<store-domain>/meta.json
```

which returns the store's currency code among other shop metadata. One extra request per store, cached once, gets you `currency` for every product from that store without re-fetching it per item.

## What this data doesn't tell you, and why that's fine

`/products.json` has no explicit "on sale" flag. What it does have is `price` and `compare_at_price` on each variant — when `compare_at_price` is set and higher than `price`, that variant is discounted. Roll that up across a product's variants (min price vs. min compare-at price) and you get a reliable `isOnSale` boolean without ever touching a rendered page.

Two failure modes worth handling explicitly instead of letting them look like empty catalogs:
- **Not a Shopify store, or the endpoint is disabled.** Some merchants disable `/products.json` (Shopify allows opting out via a theme/app setting). The request itself fails or 404s — that's a fetch error, not "the store has zero products," and the two should never be reported the same way.
- **Genuinely empty store or collection.** The request succeeds and returns `{"products": []}`. That's a real empty result, distinct from the case above.

We hit both of these building [Shopify Products Scraper](/tools/shopify-products-scraper) and initially conflated them into one silent "0 results" — fixed by classifying "fetch failed" vs. "fetched fine, zero products" vs. "your `onlyAvailable` filter removed everything" into separate status messages, so a run's outcome is legible without opening the dataset.

## Practical takeaways

- No login, no API key, no headless browser — `/products.json` and `/meta.json` are two plain HTTP GETs.
- Paginate on `limit=250&page=N` until you get an empty `products` array; there's no total-count field to pre-compute the number of pages.
- Fetch `/meta.json` once per store for `currency`, not once per product.
- Derive "on sale" from `price` vs `compare_at_price` across variants — Shopify doesn't hand you a boolean, but it hands you everything needed to compute one.
- Distinguish "this isn't a working Shopify catalog" from "this is a working, empty catalog" — they look identical in a naive implementation and mean opposite things to whoever's reading the run.

This is exactly what [Shopify Products Scraper](/tools/shopify-products-scraper) does under the hood: no per-run start fee (some competitors charge ~$0.10 just to start before any data is delivered), charged only per product actually returned.

*Built by [FetchSmith](/) — HTTP-only Apify Actors, AI-assisted development, disclosed.*

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned.*
