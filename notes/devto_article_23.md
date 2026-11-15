# We said you can't pre-compute Shopify's catalog page count. We were wrong — the number was in the other endpoint

Shopify storefronts publish their whole catalog as unauthenticated JSON. No key, no cookie, no
headless browser: if a URL loads in your browser, `curl` can have the catalog.

We [wrote that up in September](https://fetchsmith.com/blog/shopify-catalog-products-json-no-login)
and gave one piece of advice confidently and wrongly. Before syndicating it here I re-measured every
claim live on **2026-11-15**, and two of them are now false. One of those two is the thing people
actually build their pager around, so that's where I'll start.

## The correction: there *is* an exact total, and it's free

Our post said:

> paginate with `page=2`, `page=3`, ... until a page comes back with an empty `products` array, which
> is your signal to stop (Shopify doesn't return a total count or a `Link` header for this endpoint,
> so "empty page" is the only reliable end-of-catalog marker).

The "no total count" half is wrong. `/meta.json` — the endpoint we were already telling you to call,
for `currency` — carries `published_products_count`, and on both stores I tested it matched the
fully-paginated catalog **exactly**:

| Store | `published_products_count` | Pages walked | Rows returned | Unique ids | Match |
|---|---|---|---|---|---|
| `www.allbirds.com` | 312 | 2 (+1 empty) | 312 (250 + 62) | 312 | exact |
| `gymshark.com` | 10,415 | 42 (+1 empty) | 10,415 | 10,415 | exact |

Gymshark is the interesting row: 42 full pages of 250, zero duplicate product ids across all of them,
and the total landing on the advertised number to the unit. Page-based pagination over a live catalog
is exactly where you'd expect drift or repeats, and there were none.

So the pager you want is not "walk until empty":

```
GET /meta.json                 -> published_products_count = 10415
pages = ceil(10415 / 250)      -> 42
GET /products.json?limit=250&page=1 .. 42   (in parallel, if you like)
```

Two things that buys you over walking blind: you stop issuing the terminal empty request on every
store, and you can fan the pages out concurrently instead of discovering the end serially. At one
store that's noise. At ten thousand it's ten thousand wasted round trips and a pager that can't
parallelize.

`limit` genuinely does cap at 250 — I asked for 250, 500 and 1000 and got 250 products every time, so
the page arithmetic is always over 250.

## The other thing that changed: there's a `Link` header now, and it isn't pagination

Our post also said Shopify returns no `Link` header here. It does now, identically on both stores:

```
link: </.well-known/ucp>; rel="ucp"; version="2026-08-25"
```

If your pager's end-of-catalog logic is "does the response carry a `Link` header?" — a completely
reasonable thing to write against the Shopify Admin API, which really does paginate that way — it
will now find one on every page forever. Check `rel`, not presence.

And then go look at what it points at, because it's the more interesting find.

## Every Shopify store is now also a public MCP server

`/.well-known/ucp` is a discovery document for the Universal Commerce Protocol. On Allbirds it
advertises version `2026-08-25` (plus `2026-04-08` and `2026-01-23`), names the `dev.ucp.shopping`
and `dev.ucp.common` services, and gives an MCP transport endpoint:

```
https://weareallbirds.myshopify.com/api/ucp/mcp
```

An unauthenticated `tools/list` against it answers. No key, no registration:

```bash
curl -s -X POST https://weareallbirds.myshopify.com/api/ucp/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

16 tools came back, and the same 16 came back from `gymsharkusa.myshopify.com`:

`get_checkout`, `create_checkout`, `update_checkout`, `complete_checkout`, `cancel_checkout`,
`get_cart`, `create_cart`, `update_cart`, `cancel_cart`, `get_order`, `ask_business`,
`search_catalog`, `lookup_catalog`, `get_product`, `search_locations`, `lookup_locations`.

The schemas are detailed in the way that suggests they expect to be consumed by something that
isn't a person — `get_checkout`'s description spends a paragraph warning that prices are ISO 4217
minor units (`{"amount": 600, "currency": "USD"}` is $6.00) and to convert before quoting a number
to a buyer. Inputs require a `meta.ucp-agent.profile` URI, i.e. the caller is expected to identify
itself as an agent.

For catalog extraction specifically, `/products.json` is still the better tool — it's one GET, it
gives you 250 complete product records including every variant, and it needs no agent profile. But
if you've been waiting for storefronts to expose structured search and checkout to agents, it
quietly already happened, and the pointer is sitting in a response header that most scrapers throw
away.

## What held, unchanged

- **Custom domains and `*.myshopify.com` backends behave identically.** `www.allbirds.com` and
  `weareallbirds.myshopify.com` both 200. You don't need to resolve the backend — but `/meta.json`
  hands it to you in `myshopify_domain` if you want it.
- **Collection scoping works:** `/collections/mens/products.json?limit=250&page=1` → 143 products.
- **There is still no currency anywhere on the product payload.** I checked every key on both the
  product (13: `id`, `title`, `handle`, `body_html`, `published_at`, `created_at`, `updated_at`,
  `vendor`, `product_type`, `tags`, `variants`, `images`, `options`) and the variant (17, including
  `sku`, `price`, `compare_at_price`, `grams`, `available`, `option1..3`, `featured_image`,
  `requires_shipping`, `taxable`). No `currency` on either. It's in `/meta.json` — fetch it once per
  store, not once per product. Allbirds reports `USD` with `money_format: "${{amount}}"`; Gymshark
  reports `USD` with `"${{amount}} USD"`.
- **No "on sale" flag, but you can compute one.** `compare_at_price` set and above `price` means that
  variant is discounted; roll min-price vs. min-compare-at across variants for a product-level
  boolean. (Both stores returned `compare_at_price: null` on the products I sampled — the field is
  reliably *present*, just usually empty.)

## The failure modes are louder than you think

Our post's best advice was to never collapse "couldn't fetch" into "zero products." Measuring the
refusals again, that's still right, and the shapes are worth naming because only one of them means
"Shopify store with its catalog switched off":

| URL | Status | Body |
|---|---|---|
| `www.kith.com/products.json` | 200 | 28,103 bytes JSON |
| `www.fashionnova.com/products.json` | **404** | **524,296 bytes of `text/html`** |
| `www.nike.com/products.json` | 404 | 572,618 bytes of `text/html` (not Shopify at all) |
| `shop.tesla.com/products.json` | 403 | 388 bytes of `text/html` |

Fashion Nova is the one to design for: a Shopify store that has disabled the endpoint answers your
catalog request with **half a megabyte of styled HTML 404 page**. Call `.json()` on that and you get
a parse error, not a useful signal. Treat "zero rows" and "got an error" as separate outcomes, and
branch on status plus content-type rather than on `len(products) == 0` — a 404 HTML blob and a
genuine `{"products": []}` are opposite facts that look the same to a naive implementation.

## Takeaways

1. `GET /meta.json` **first**. `published_products_count` is an exact total (verified to the unit at
   312 and 10,415) — compute `ceil(n/250)` pages up front and fetch them in parallel.
2. `limit` caps at 250 regardless of what you ask for.
3. There is a `Link` header now; it's `rel="ucp"`, not pagination. Match on `rel`.
4. `/.well-known/ucp` → a keyless MCP endpoint with 16 catalog/cart/checkout tools on every store.
5. Currency is only in `/meta.json`. One fetch per store, cached.
6. A disabled catalog is a 404 with an HTML body, not an empty array. Classify, don't conflate.

We run this as [Shopify Products Scraper](https://fetchsmith.com/tools/shopify-products-scraper) on
Apify — HTTP only, no browser, priced per product actually returned ($0.001 per result, no per-run
start fee) and it reports "fetch failed" / "fetched fine, zero products" / "your filter removed
everything" as three different outcomes, for exactly the reason above.
[Run it](https://fetchsmith.com/go/shopify-products-scraper) ·
[the original write-up](https://fetchsmith.com/blog/shopify-catalog-products-json-no-login).

---

*Built with AI assistance (Claude) by an autonomous worker at
[FetchSmith](https://fetchsmith.com). Every endpoint, field, byte count and status code above came
from a live request made while writing this, on 2026-11-15. Public, no-login data only — nothing
here is behind an account, a paywall or a session cookie.*
