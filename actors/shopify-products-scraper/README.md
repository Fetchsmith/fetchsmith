# Shopify Products Data Scraper

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
| `vendors` | array | Only keep products whose vendor/brand contains one of these (case-insensitive OR — e.g. `["Allbirds","Rothy's"]`). Combines with every other filter via AND. Ignored on direct product URLs. |
| `productTypes` | array | Only keep products whose product type contains one of these (case-insensitive OR), e.g. `["Shoes","Sandals"]`. Combines with every other filter via AND. Ignored on direct product URLs. |
| `maxProductsPerStore` | integer | Cap per store (default 500) |
| `includeDescription` | boolean | Plain-text description (default true) |
| `includeVariants` | boolean | Full variants array with SKU, price, options, availability (default true) |
| `onlyAvailable` | boolean | Skip sold-out products |
| `minPrice` | integer | Only keep products with a variant at or above this price (matches when the product's own price range overlaps the window — a $40-$120 hoodie matches `minPrice: 100`). Store's own currency, no FX conversion. Filtered-out products are never charged. |
| `maxPrice` | integer | Only keep products with a variant at or below this price (same range-overlap rule). Store's own currency, no FX conversion. Filtered-out products are never charged. |
| `onSaleOnly` | boolean | Only keep products currently discounted — a compare-at price set above the current price, the same condition as the `isOnSale` output field. Filtered-out products are never charged. |
| `minDiscountPercent` | integer | Only keep products discounted by at least this percentage (checks the `discountPercent` output field). Stricter than `onSaleOnly`, which accepts any discount; products with no discount at all (`discountPercent: null`) are excluded, not treated as 0%. Filtered-out products are never charged. |
| `maxResults` | integer | Total cap |
| `proxyConfiguration` | object | Route storefront requests through Apify Proxy (default on). Use a country-specific residential group to read that country's prices and currency, or to get past IP rate-limiting. Accounts without proxy access fall back to a direct connection instead of failing. |
| `detailLevel` | string | `"basic"` (default) reads only the products feed. `"full"` also fetches each product's live page **and** its per-product `.js` route for `barcode`, `inventoryQuantity`, `inventoryManagement`, `inventoryPolicy`, `quantityRule`, `totalInventory`, `seoTitle`, `seoDescription`, `ratingValue`, `reviewCount`, `hasSubscriptionOption` and `subscriptionPlans` — none of which the bulk `products.json` feed carries — priced as one extra event per product (see Pricing). Both requests run in parallel, so it costs no extra wall-clock. |
| `watchLabel` | string | Turn the run into a **catalog watch**. The first run under a label records every product's price and availability and returns nothing (charges nothing); later runs under the same label return only products that are new, changed price, or changed stock status. See *Watch mode* below. |
| `watchEvents` | array | Restrict a watch to some change types only: `new`, `priceDrop`, `priceIncrease`, `backInStock`, `outOfStock`. Empty (default) reports all five. Ignored without `watchLabel`. |
| `webhookUrl` | string | Optional http(s) URL that receives a small JSON POST when the run finishes (products pushed, per-change-type counts, dataset id). Best-effort — a failing webhook never fails the run or changes the bill. |

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
  "variants": [{ "id": 1, "title": "8 / Natural Grey", "sku": "WR-8-NG", "price": 98, "compareAtPrice": 125, "available": true, "grams": 340, "requiresShipping": true, "taxable": true, "position": 1, "featuredImage": "https://cdn.shopify.com/s/files/....jpg", "barcode": "196942208243", "inventoryQuantity": 15, "inventoryManagement": "shopify", "inventoryPolicy": "deny", "quantityRule": null }],
  "description": "Our classic everyday sneaker ...",
  "descriptionHtml": "<p>Our classic everyday sneaker ...</p>",
  "createdAt": "2025-01-10T12:00:00Z",
  "updatedAt": "2026-08-01T09:30:00Z",
  "store": "https://www.allbirds.com",
  "seoTitle": "Men's Wool Runner Shoes | Allbirds",
  "seoDescription": "Our best-selling sneaker, made from sustainably sourced merino wool.",
  "ratingValue": 4.6,
  "reviewCount": 51,
  "hasSubscriptionOption": true,
  "subscriptionPlans": [{ "name": "Subscribe & Save 20%", "plans": [{ "name": "Delivered every 30 days", "recurringDeliveries": true, "discountPercent": 20 }] }]
}
```
`barcode`/`inventoryQuantity`/`inventoryManagement`/`inventoryPolicy`/`quantityRule` (per variant), `totalInventory`/`hasSubscriptionOption`/`subscriptionPlans` (per product), `seoTitle`, `seoDescription`, `ratingValue` and `reviewCount` are only present when `detailLevel` is `"full"` (see Input) — Shopify's bulk `products.json` feed carries none of them.

`quantityRule` (`{min, max, increment}`) is only populated for a real, non-default rule — a minimum order quantity, a case-pack increment, or a per-order cap — Shopify's own implicit default (`min:1, max:null, increment:1`) is reported as `null` instead so it doesn't look like every product has a "rule". `hasSubscriptionOption`/`subscriptionPlans` cover both Shopify's native subscriptions and app-backed ones like Recharge (verified live on both); `subscriptionPlans[].plans[].discountPercent` is `null` when a plan doesn't use a flat percentage discount (e.g. a fixed-price override).

**How complete the stock fields are is a per-store setting, not something any scraper controls.** Measured live: allbirds.com publishes real per-variant quantities *and* UPC barcodes; brooklinen.com publishes a barcode but no quantity; rothys.com publishes barcodes but no quantities. Missing values come back as `null` rather than a guess. `barcode` is whatever the merchant typed into that field — a GTIN/UPC on most stores, an internal SKU on some. `totalInventory` counts only variants Shopify actually tracks stock for, so untracked items (`inventoryManagement: null`, which report a 999999 sentinel) can't inflate it; it is `null` — not `0` — when a store tracks none, keeping "sold out" distinguishable from "this store doesn't publish stock".

`watchLabel`, `watchChange`, `watchChanges`, `previousPriceMin`, `previousAvailable` and `priceChange` are only present on rows returned by a run with `watchLabel` set (see *Watch mode* below); a normal one-off scrape never emits them.

## Watch mode — pay only for what changed
Scraping a competitor's catalog every morning normally means re-buying the same 500 products every morning. Set `watchLabel` and you buy the diff instead:

```json
{ "storeUrls": ["https://www.allbirds.com"], "maxProductsPerStore": 5000,
  "watchLabel": "allbirds-prices", "watchEvents": ["priceDrop", "backInStock"] }
```

- **Run 1** records each product's price and availability and returns **0 products, charged $0** — it's a baseline.
- **Every run after that** returns only the products that moved. Each row is a normal product row plus `watchChange` (`new` / `priceDrop` / `priceIncrease` / `backInStock` / `outOfStock`), `watchChanges` (all changes on that product), `previousPriceMin`, `previousAvailable` and `priceChange` (the signed difference).
- Unchanged products are never pushed and **never charged**, so a daily watch on a stable catalog costs nothing on quiet days.
- Adding a store URL to an existing label baselines **just that store**, so you aren't billed for its whole catalog as "new". Changing a filter (`onlyAvailable`, `searchQuery`, `vendors`, `productTypes`, `minPrice`, `maxPrice`, `onSaleOnly`, `minDiscountPercent`) starts a fresh baseline, since it's a different watched set.
- In watch mode `maxProductsPerStore` caps how many products are **scanned** per store (the diff has to walk the feed), so set it above the store's catalog size; the log warns when the sweep was cut short.
- Pair it with `webhookUrl` and Apify's scheduler to get a ping only when something actually changes.

## Pricing
`result` — charged per product returned, **$0.001/product on the Free plan, tapering to $0.00085/product on Gold and above.** No per-run "Actor Start" fee at all — every competitor we've checked in this niche still charges one, however small, before any data is delivered; ours is genuinely zero (their live pricing re-verified 2026-09-17). Stores that block the public catalog return nothing and cost nothing.
`productDetail` — charged **once** per product (not once per extra request) only when `detailLevel` is `"full"` **and** the extra fetches actually found stock, SEO or rating data, at the same tiered rate as `result` ($0.001 Free → $0.00085 Gold+). A product that yields none of them — no rating app installed, no meta description, store doesn't publish stock — costs nothing.

## FAQ
**Does it work on custom domains, not just `*.myshopify.com`?** Yes — pass any storefront domain that runs Shopify; no need to resolve it to the `myshopify.com` backend first.
**What if the same store ends up in `storeUrls` twice?** Deduped automatically by the resolved endpoint (so `https://store.com` and `https://store.com/` count as one) — you're never charged twice for the same store.
**Can I tell which products are on sale?** Yes, each item includes `isOnSale` (true when `compareAtPriceMin` is above `priceMin`) and `discountPercent` — the percentage off the cheapest variant's own list price, so it never mixes two different variants — plus store `currency`.
**Does `searchQuery` handle accented words correctly?** Yes, as of v0.1.29 — the query and the product text it's matched against are Unicode-normalized before comparing, so an accented word (e.g. "café") matches regardless of which of Unicode's two equivalent representations (composed vs. decomposed) you typed it in.
**Do I get the description as HTML?** Both: `description` is plain text and `descriptionHtml` is the store's raw `body_html`, so you can keep the formatting when re-publishing a catalog.
**Can I get the product's SEO title/description and star rating?** Yes, set `detailLevel: "full"`. Those aren't in Shopify's `products.json` feed at all — they only live on the rendered product page (`<title>`/meta description tags and, when the store runs a review app like Judge.me or Yotpo, a `ratingValue`/`reviewCount` in the page's structured data), so getting them costs one extra HTTP request per product and is priced as its own event.
**Can I get real inventory counts and barcodes?** Yes, set `detailLevel: "full"`. Shopify's bulk `products.json` feed strips `barcode`, `inventory_quantity`, `inventory_management` and `inventory_policy` out of every variant, but the per-product JSON route still serves them on the same variant ids, so they merge back in exactly. How much a given store exposes is that store's own setting (see the note under Output) — you get real values where they are published and `null` where they are not, never a guess. No login or Admin API token is involved; this is the same data a logged-out shopper's browser receives.
**Can I pass one product URL instead of a whole store?** Yes — a `/products/<handle>` URL returns exactly that one product, with the same fields (and the same per-result price) as it would have from a full-store run. Fixed in v0.1.33: Shopify serves single products through a different, older serializer than the bulk feed, and two of its quirks used to corrupt that path — a comma-joined `tags` string instead of a list, and no per-variant availability flag at all.
**When is `available` `null` instead of `true`/`false`?** Only when the store publishes nothing to decide it from: stock tracking is on for the variant but quantities are withheld. Untracked variants and stores that allow overselling are reported `true`, tracked ones as `inventoryQuantity > 0`, and `detailLevel: "full"` resolves the remaining unknowns from the storefront's own `.js` route at no extra request. `null` always means "this store doesn't say", never "sold out".
**Can I tell if a product is sold as a subscription, and how big the discount is?** Yes, set `detailLevel: "full"` — `hasSubscriptionOption` and `subscriptionPlans` cover both Shopify's own native subscriptions and app-backed ones (e.g. Recharge), including each plan's delivery frequency and percentage discount, read straight from the storefront's own `.js` route.
**Can I tell if a product has a minimum order quantity or case-pack size (wholesale/B2B)?** Yes, set `detailLevel: "full"` — each variant's `quantityRule` reports a real `{min, max, increment}` only when the store has actually configured one; Shopify's meaningless universal default (order 1 at a time, no cap) comes back as `null`, not a fake "rule".
**Does it bypass password-protected or dev stores?** No — only publicly reachable catalogs are read, same as a logged-out shopper would see.
**A store returned nothing — how do I tell "empty catalog" from "wrong URL"?** The run log says which, by name. Shopify answers `products.json` with a status code that identifies the problem, and as of v0.1.43 each one gets its own message: **401** the storefront is password-protected ("Opening soon" page up), **402** the store is frozen or closed (lapsed plan), **404** there is no Shopify store at that domain (usually a typo), **403** a bot check or geo/IP block — re-run with `proxyConfiguration`, **429** rate-limited. Only a genuine `200` carrying `{"products":[]}` is reported as an empty store or collection, and that one is re-checked on three separate attempts before we believe it. Nothing is charged in any of these cases.
**Can I search a store for a keyword instead of scraping its whole catalog?** Yes, set `searchQuery` (e.g. `"wool"` or `"merino sweater"`) — it matches against title, vendor, product type and tags (all words must appear). It's a client-side filter, not a separate search API call, since Shopify's public feed has no server-side keyword search; a store with a large catalog still takes the same time to scan as an unfiltered run of the same store.
**How does a price window handle products whose variants have different prices?** A product is a price *range*, not a single price, so `minPrice`/`maxPrice` keep a product when its range overlaps your window: a $40-$120 hoodie matches `maxPrice: 50` (there is a buyable $40 variant) and also `minPrice: 100` (there is a $120 one). Prices are compared in the store's own currency — the `currency` output field tells you which — and no FX conversion is done, so the same window means different things on a USD and a EUR store. Products whose price can't be read at all are dropped rather than passed through, so a price-filtered run never returns a row the filter couldn't be evaluated against. Both bounds are applied *before* billing, so you are never charged for a product the filter removed.
**Can I get only the discounted products?** Yes, set `onSaleOnly: true` — it keeps products where the store set a compare-at price above the current price (identical to the `isOnSale` output field), with `discountPercent` on every row computed from the cheapest variant's own compare-at price. Products the store never put a compare-at price on are excluded, since there is no evidence of a discount to report.
**Can I set a minimum discount instead of "any discount"?** Yes, set `minDiscountPercent` (e.g. `30` for "30% off or more") — it reads the same `discountPercent` field `onSaleOnly` checks, just with a floor. A product with no compare-at price at all is excluded, not treated as a 0% discount that happens to fail the floor.
**Can I filter to specific brands or product types without a keyword search?** Yes — `vendors` and `productTypes` are OR-matched lists (e.g. `vendors: ["Allbirds","Rothy's"]` returns products from either brand), unlike `searchQuery`, which is AND-of-words across a single combined haystack and can't express "brand A or brand B". Both read fields already on every row, so there's no extra request cost, and both combine with every other filter (including each other) via AND — only the entries within one list are OR'd together.

**Can I monitor a store for price drops instead of re-scraping the whole catalog?** Yes — set `watchLabel` (optionally narrowed with `watchEvents`). The first run under that label is a free baseline that returns nothing; every later run returns only new products, price changes and stock flips, each row carrying `watchChange`, `previousPriceMin`, `previousAvailable` and `priceChange`. Products that didn't move are never pushed and never charged, so a scheduled daily watch costs nothing on days when the store doesn't change. See *Watch mode* above.

## Related guides
Engineering write-ups behind this Actor:
- [Every Shopify store's catalog is public JSON — no login, no browser](https://fetchsmith.com/blog/shopify-catalog-products-json-no-login)
- [Shopify's bulk products.json hides stock counts and barcodes — the per-product endpoint doesn't](https://fetchsmith.com/blog/shopify-inventory-barcode-per-product-json)
- [HTTP-only vs headless browser scraping: a timed benchmark](https://fetchsmith.com/blog/http-only-vs-headless-browser-scraping-cost)
- [Four ways an invisible character makes a scraper return zero rows](https://fetchsmith.com/blog/invisible-characters-return-zero-rows)

Only publicly available data is collected. Support: support@fetchsmith.com · Hosted API: https://fetchsmith.com/tools/shopify-products-scraper

Source code: https://github.com/Fetchsmith/fetchsmith/tree/main/actors/shopify-products-scraper
