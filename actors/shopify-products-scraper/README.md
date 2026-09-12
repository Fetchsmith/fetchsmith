# Shopify Products Scraper

Extract the full product catalog of any Shopify store (or a single collection or product) into JSON, CSV or Excel: title, vendor, type, tags, prices, compare-at prices, availability, images, options, variants with SKUs, and description. Works on any Shopify storefront, no login, no browser. Pay only per product returned.

## Use cases
- Competitor price and assortment monitoring
- Building product feeds, catalogs and dropshipping research datasets
- Tracking new launches and stock changes on a schedule
- Feeding product data into AI agents and recommendation systems

## Input
| Field | Type | Description |
|---|---|---|
| `storeUrls` | array | Store homepages, `/collections/<handle>` URLs, or `/products/<handle>` URLs |
| `maxProductsPerStore` | integer | Cap per store (default 500) |
| `includeDescription` | boolean | Plain-text description (default true) |
| `includeVariants` | boolean | Full variants array with SKU, price, options, availability (default true) |
| `onlyAvailable` | boolean | Skip sold-out products |
| `maxResults` | integer | Total cap |
| `proxyConfiguration` | object | Route storefront requests through Apify Proxy (default on). Use a country-specific residential group to read that country's prices and currency, or to get past IP rate-limiting. Accounts without proxy access fall back to a direct connection instead of failing. |

## Output (one item per product)
```json
{
  "id": 6543210987,
  "title": "Men's Wool Runner",
  "handle": "mens-wool-runners",
  "url": "https://www.allbirds.com/products/mens-wool-runners",
  "vendor": "Allbirds",
  "productType": "Shoes",
  "tags": ["men", "runners"],
  "currency": "USD",
  "priceMin": 98,
  "priceMax": 98,
  "compareAtPriceMin": 125,
  "compareAtPriceMax": 125,
  "isOnSale": true,
  "discountPercent": 21.6,
  "available": true,
  "availableVariantCount": 9,
  "variantCount": 12,
  "images": [{ "src": "https://cdn.shopify.com/s/files/....jpg", "alt": "Men's Wool Runner in Natural Grey" }],
  "imageUrl": "https://cdn.shopify.com/s/files/....jpg",
  "imageCount": 6,
  "variants": [{ "id": 1, "title": "8 / Natural Grey", "sku": "WR-8-NG", "price": 98, "compareAtPrice": 125, "available": true, "grams": 340, "requiresShipping": true, "taxable": true, "position": 1, "featuredImage": "https://cdn.shopify.com/s/files/....jpg" }],
  "description": "Our classic everyday sneaker ...",
  "descriptionHtml": "<p>Our classic everyday sneaker ...</p>",
  "createdAt": "2025-01-10T12:00:00Z",
  "updatedAt": "2026-08-01T09:30:00Z",
  "store": "https://www.allbirds.com"
}
```

## Pricing
`result` — charged per product returned, at $0.001/product. No per-run "Actor Start" fee (some competitors charge ~$0.10 just to start a run before any data is delivered). Stores that block the public catalog return nothing and cost nothing.

## FAQ
**Does it work on custom domains, not just `*.myshopify.com`?** Yes — pass any storefront domain that runs Shopify; no need to resolve it to the `myshopify.com` backend first.
**Can I tell which products are on sale?** Yes, each item includes `isOnSale` (true when `compareAtPriceMin` is above `priceMin`) and `discountPercent` — the percentage off the cheapest variant's own list price, so it never mixes two different variants — plus store `currency`.
**Do I get the description as HTML?** Both: `description` is plain text and `descriptionHtml` is the store's raw `body_html`, so you can keep the formatting when re-publishing a catalog.
**Does it bypass password-protected or dev stores?** No — only publicly reachable catalogs are read, same as a logged-out shopper would see.

## Related guides
Engineering write-ups behind this Actor:
- [Every Shopify store's catalog is public JSON — no login, no browser](https://fetchsmith.com/blog/shopify-catalog-products-json-no-login)
- [HTTP-only vs headless browser scraping: a timed benchmark](https://fetchsmith.com/blog/http-only-vs-headless-browser-scraping-cost)

Only publicly available data is collected. Support: support@fetchsmith.com · Hosted API: https://fetchsmith.com/tools/shopify-products-scraper

Source code: https://github.com/Fetchsmith/fetchsmith/tree/main/actors/shopify-products-scraper
