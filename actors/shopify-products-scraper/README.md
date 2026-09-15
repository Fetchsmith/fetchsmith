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
| `searchQuery` | string | Only keep products whose title, vendor, product type or tags contain every word in the query (case-insensitive). Applied client-side after fetching — Shopify's public feed has no server-side search — so it still scans the whole store at the same request cost as an unfiltered run, but needs no collection URL guessing. Ignored on direct product URLs. |
| `maxProductsPerStore` | integer | Cap per store (default 500) |
| `includeDescription` | boolean | Plain-text description (default true) |
| `includeVariants` | boolean | Full variants array with SKU, price, options, availability (default true) |
| `onlyAvailable` | boolean | Skip sold-out products |
| `maxResults` | integer | Total cap |
| `proxyConfiguration` | object | Route storefront requests through Apify Proxy (default on). Use a country-specific residential group to read that country's prices and currency, or to get past IP rate-limiting. Accounts without proxy access fall back to a direct connection instead of failing. |
| `detailLevel` | string | `"basic"` (default) reads only the products feed. `"full"` also fetches each product's live page **and** its per-product JSON for `barcode`, `inventoryQuantity`, `inventoryManagement`, `inventoryPolicy`, `totalInventory`, `seoTitle`, `seoDescription`, `ratingValue` and `reviewCount` — none of which the bulk `products.json` feed carries — priced as one extra event per product (see Pricing). Both requests run in parallel, so it costs no extra wall-clock. |

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
  "totalInventory": 149,
  "images": [{ "src": "https://cdn.shopify.com/s/files/....jpg", "alt": "Men's Wool Runner in Natural Grey" }],
  "imageUrl": "https://cdn.shopify.com/s/files/....jpg",
  "imageCount": 6,
  "variants": [{ "id": 1, "title": "8 / Natural Grey", "sku": "WR-8-NG", "price": 98, "compareAtPrice": 125, "available": true, "grams": 340, "requiresShipping": true, "taxable": true, "position": 1, "featuredImage": "https://cdn.shopify.com/s/files/....jpg", "barcode": "196942208243", "inventoryQuantity": 15, "inventoryManagement": "shopify", "inventoryPolicy": "deny" }],
  "description": "Our classic everyday sneaker ...",
  "descriptionHtml": "<p>Our classic everyday sneaker ...</p>",
  "createdAt": "2025-01-10T12:00:00Z",
  "updatedAt": "2026-08-01T09:30:00Z",
  "store": "https://www.allbirds.com",
  "seoTitle": "Men's Wool Runner Shoes | Allbirds",
  "seoDescription": "Our best-selling sneaker, made from sustainably sourced merino wool.",
  "ratingValue": 4.6,
  "reviewCount": 51
}
```
`barcode`/`inventoryQuantity`/`inventoryManagement`/`inventoryPolicy` (per variant), `totalInventory` (per product), `seoTitle`, `seoDescription`, `ratingValue` and `reviewCount` are only present when `detailLevel` is `"full"` (see Input) — Shopify's bulk `products.json` feed carries none of them.

**How complete the stock fields are is a per-store setting, not something any scraper controls.** Measured live: allbirds.com publishes real per-variant quantities *and* UPC barcodes; brooklinen.com publishes a barcode but no quantity; rothys.com publishes barcodes but no quantities. Missing values come back as `null` rather than a guess. `barcode` is whatever the merchant typed into that field — a GTIN/UPC on most stores, an internal SKU on some. `totalInventory` counts only variants Shopify actually tracks stock for, so untracked items (`inventoryManagement: null`, which report a 999999 sentinel) can't inflate it; it is `null` — not `0` — when a store tracks none, keeping "sold out" distinguishable from "this store doesn't publish stock".

## Pricing
`result` — charged per product returned, **$0.001/product on the Free plan, tapering to $0.00085/product on Gold and above.** No per-run "Actor Start" fee (some competitors charge ~$0.10 just to start a run before any data is delivered). Stores that block the public catalog return nothing and cost nothing.
`productDetail` — charged **once** per product (not once per extra request) only when `detailLevel` is `"full"` **and** the extra fetches actually found stock, SEO or rating data, at the same tiered rate as `result` ($0.001 Free → $0.00085 Gold+). A product that yields none of them — no rating app installed, no meta description, store doesn't publish stock — costs nothing.

## FAQ
**Does it work on custom domains, not just `*.myshopify.com`?** Yes — pass any storefront domain that runs Shopify; no need to resolve it to the `myshopify.com` backend first.
**What if the same store ends up in `storeUrls` twice?** Deduped automatically by the resolved endpoint (so `https://store.com` and `https://store.com/` count as one) — you're never charged twice for the same store.
**Can I tell which products are on sale?** Yes, each item includes `isOnSale` (true when `compareAtPriceMin` is above `priceMin`) and `discountPercent` — the percentage off the cheapest variant's own list price, so it never mixes two different variants — plus store `currency`.
**Does `searchQuery` handle accented words correctly?** Yes, as of v0.1.29 — the query and the product text it's matched against are Unicode-normalized before comparing, so an accented word (e.g. "café") matches regardless of which of Unicode's two equivalent representations (composed vs. decomposed) you typed it in.
**Do I get the description as HTML?** Both: `description` is plain text and `descriptionHtml` is the store's raw `body_html`, so you can keep the formatting when re-publishing a catalog.
**Can I get the product's SEO title/description and star rating?** Yes, set `detailLevel: "full"`. Those aren't in Shopify's `products.json` feed at all — they only live on the rendered product page (`<title>`/meta description tags and, when the store runs a review app like Judge.me or Yotpo, a `ratingValue`/`reviewCount` in the page's structured data), so getting them costs one extra HTTP request per product and is priced as its own event.
**Can I get real inventory counts and barcodes?** Yes, set `detailLevel: "full"`. Shopify's bulk `products.json` feed strips `barcode`, `inventory_quantity`, `inventory_management` and `inventory_policy` out of every variant, but the per-product JSON route still serves them on the same variant ids, so they merge back in exactly. How much a given store exposes is that store's own setting (see the note under Output) — you get real values where they are published and `null` where they are not, never a guess. No login or Admin API token is involved; this is the same data a logged-out shopper's browser receives.
**Does it bypass password-protected or dev stores?** No — only publicly reachable catalogs are read, same as a logged-out shopper would see.
**Can I search a store for a keyword instead of scraping its whole catalog?** Yes, set `searchQuery` (e.g. `"wool"` or `"merino sweater"`) — it matches against title, vendor, product type and tags (all words must appear). It's a client-side filter, not a separate search API call, since Shopify's public feed has no server-side keyword search; a store with a large catalog still takes the same time to scan as an unfiltered run of the same store.

## Related guides
Engineering write-ups behind this Actor:
- [Every Shopify store's catalog is public JSON — no login, no browser](https://fetchsmith.com/blog/shopify-catalog-products-json-no-login)
- [Shopify's bulk products.json hides stock counts and barcodes — the per-product endpoint doesn't](https://fetchsmith.com/blog/shopify-inventory-barcode-per-product-json)
- [HTTP-only vs headless browser scraping: a timed benchmark](https://fetchsmith.com/blog/http-only-vs-headless-browser-scraping-cost)

Only publicly available data is collected. Support: support@fetchsmith.com · Hosted API: https://fetchsmith.com/tools/shopify-products-scraper

Source code: https://github.com/Fetchsmith/fetchsmith/tree/main/actors/shopify-products-scraper
