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
  "compareAtPriceMin": null,
  "isOnSale": false,
  "available": true,
  "variantCount": 12,
  "images": [{ "src": "https://cdn.shopify.com/s/files/....jpg", "alt": "Men's Wool Runner in Natural Grey" }],
  "imageUrl": "https://cdn.shopify.com/s/files/....jpg",
  "variants": [{ "id": 1, "title": "8 / Natural Grey", "sku": "WR-8-NG", "price": 98, "available": true, "grams": 340, "requiresShipping": true }],
  "description": "Our classic everyday sneaker ...",
  "createdAt": "2025-01-10T12:00:00Z",
  "updatedAt": "2026-08-01T09:30:00Z",
  "store": "https://www.allbirds.com"
}
```

## Pricing
`result` — charged per product returned, at $0.001/product. No per-run "Actor Start" fee (some competitors charge ~$0.10 just to start a run before any data is delivered). Stores that block the public catalog return nothing and cost nothing.

## FAQ
**Does it work on custom domains, not just `*.myshopify.com`?** Yes — pass any storefront domain that runs Shopify; no need to resolve it to the `myshopify.com` backend first.
**Can I tell which products are on sale?** Yes, each item includes `isOnSale` (true when `compareAtPriceMin` is above `priceMin`) plus store `currency`.
**Does it bypass password-protected or dev stores?** No — only publicly reachable catalogs are read, same as a logged-out shopper would see.

Only publicly available data is collected. Support: support@fetchsmith.com · Hosted API: https://fetchsmith.com/tools/shopify-products-scraper

Source code: https://github.com/Fetchsmith/fetchsmith/tree/main/actors/shopify-products-scraper
