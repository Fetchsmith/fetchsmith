---
title: "Shopify's bulk products.json hides stock counts and barcodes — the per-product endpoint doesn't"
description: "products.json?limit=250 strips inventory_quantity, inventory_management, inventory_policy and barcode from every variant. The per-product /products/<handle>.json endpoint (same auth, same key-free access) carries all four. Here's what actually differs and what to watch for."
date: 2026-09-14
tags: webscraping, shopify, ecommerce, api
tool: shopify-products-scraper
---

We wrote about [Shopify's public `/products.json` catalog feed](/blog/shopify-catalog-products-json-no-login) as if it were the complete picture: paginate `products.json?limit=250&page=N`, get every product, no auth, no key. That's still true for prices, variants, images and options. It is not true for stock levels and barcodes — and the fix isn't a different site, it's a different endpoint on the same store.

## Two public, key-free endpoints, two different variant schemas

```
GET https://<store-domain>/products.json?limit=250&page=1        # bulk, paginated
GET https://<store-domain>/products/<handle>.json                 # one product
```

Both require zero authentication. But the bulk feed's `variants[]` omits `inventory_quantity`, `inventory_management`, `inventory_policy` and `barcode` entirely — those four keys are just not present in the JSON, not null, not empty. The per-product endpoint returns the same variant `id`s with all four fields populated (when the store publishes them).

Verified live against `allbirds.com/products/mens-strider-explore.js` and its `.json` counterpart: real UPC barcode (`196942208243`), real `inventory_quantity: 0` on a sold-out variant, `inventory_management: "shopify"`, `inventory_policy: "deny"` — matched id-for-id against the bulk feed's variant ids, 13 for 13. The `.js` and `.json` per-product routes agree on every field we compared; we use `.json` for consistency with the rest of the scrape.

## Exposure is a per-store setting, not a per-endpoint one

Whether a store publishes real numbers has nothing to do with which endpoint you call — it's a merchant/theme setting, and it varies:

- **allbirds.com** — real quantities and real UPC barcodes.
- **brooklinen.com** — a barcode field populated, but it's an internal SKU (`COR-T1`), not a GTIN, and no quantity.
- **rothys.com** — barcodes present, quantities absent.

So "get real inventory counts" can only ever ship with a "when the store publishes them" hedge. Treat a missing field as `null`, never as `0` or a guess — `0` is a real, meaningful value (sold out) and conflating it with "not published" is worse than not shipping the field at all.

## The trap: untracked variants report a sentinel, not a real number

The first real test run surfaced this the hard way: one allbirds product ("Free Returns Coverage," a digital add-on with `inventory_management: null`) reported an `inventory_quantity` of **999999**. Roll that into a naive per-product stock total and a real catalog's total inventory comes out as 1,981,856 — off by six orders of magnitude on exactly the kind of number a buyer might screenshot and trust.

The fix: only sum quantities for variants where `inventory_management` is actually set (`"shopify"`, or a fulfillment service name). Untracked variants keep their raw per-variant value if you want to expose it verbatim, but never fold them into a roll-up total. If you're aggregating stock across variants for any Shopify store, gate on `inventory_management` first — one untracked variant will silently swamp the whole sum.

## Practical takeaways

- `/products.json` (bulk) and `/products/<handle>.json` (per-product) are both public and key-free, but only the per-product route carries `inventory_quantity`, `inventory_management`, `inventory_policy` and `barcode`.
- Fetching per-product detail already costs one request per product if you're doing it for anything else (SEO metadata, ratings) — merging in the stock/barcode fields from the same response is free; you don't need a second extra request.
- A missing field means "this store doesn't publish it," not zero — keep that `null`, not `0`.
- Any inventory roll-up across variants must exclude variants with no `inventory_management` set, or a single untracked/digital variant's sentinel value will corrupt the total.

This is exactly what [Shopify Products Scraper](/tools/shopify-products-scraper)'s `detailLevel: "full"` mode does now: per-variant `barcode`, `inventoryQuantity`, `inventoryManagement`, `inventoryPolicy`, and a store-honest `totalInventory` roll-up — at the same per-product price as before, no extra charge for the extra fields.

*Built by [FetchSmith](/) — HTTP-only Apify Actors, AI-assisted development, disclosed.*

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned.*
