# Website Screenshot Scraper

Capture a screenshot or PDF of any public URL using a real Chromium browser. Device presets, element capture, Open Graph card sizing and raw-HTML rendering are built in — the free official `apify/screenshot-url` Actor covers none of these.

## What it does
- Renders a public URL (or raw HTML you provide) in headless Chromium and captures a JPEG, PNG or PDF.
- Full-page or viewport-only capture, a single CSS-selector element, or a fixed 1200x630 Open Graph card.
- Device presets (desktop, iPhone 14, Pixel 7, iPad) or a custom viewport size.
- Optional `waitForSelector` to capture only once a specific element has rendered — more precise than a fixed delay or `networkidle` for single-page apps.
- **Visual diff mode**: set `compareUrl` and each URL is captured twice (yours and the comparison target), pixel-diffed, and returned with the differing-pixel count, change percentage and a highlighted diff image — staging vs production, or a page before vs after a deploy. One charged event per comparison, not two.
- Emulate dark mode (`colorScheme`), a locale/timezone (`locale`/`timezoneId`), touch support (`hasTouch`), or a GPS location (`geolocation`) before capturing, for pages that render differently based on any of these.
- Optional proxy (`proxyConfiguration`) — Apify Proxy or your own proxy URLs, with a fresh IP drawn per URL so a long list is spread across the pool instead of hitting a rate limit from one address.
- Optional custom HTTP headers (`headers`) and cookies (`cookies`) for pages that need your own API key or an existing logged-in session to render correctly — not a login or paywall bypass.
- Pay per successful capture: a URL that fails to load (timeout, DNS error, 4xx/5xx) returns an error row and is **never charged**.
- The run start is free; you only pay for screenshots actually returned.

## Input
| Field | Type | Description |
|---|---|---|
| `urls` | array of strings | Pages to screenshot (default `["https://example.com"]`) |
| `html` | string | Render this raw HTML instead of fetching a URL (ignores `urls`, produces one row; ignored in visual diff mode) |
| `format` | string | `jpeg` (default, recommended), `png` (lossless), or `pdf` |
| `quality` | integer | JPEG quality 10-100 (default 80) |
| `fullPage` | boolean | Capture full scrollable height, not just the first screen (default true) |
| `devicePreset` | string | `custom`, `desktop`, `iphone`, `pixel`, `ipad` |
| `viewportWidth` / `viewportHeight` | integer | Used when `devicePreset` is `custom` |
| `selector` | string | CSS selector to capture a single element instead of the whole page |
| `ogCard` | boolean | Force a 1200x630 viewport capture for social-share previews |
| `waitUntil` | string | `load` (default), `domcontentloaded`, or `networkidle` |
| `delayMs` | integer | Extra wait after load before capturing (0-15000ms) |
| `waitForSelector` | string | CSS selector to wait for (up to 10s) before capturing, e.g. `.chart-loaded` |
| `compareUrl` | string | Turns on visual diff mode: pixel-compare every URL in `urls` against this one (always PNG, one charge per comparison) |
| `diffThreshold` | number | Diff sensitivity 0-1 (default 0.1). Lower is stricter; 0.02 catches antialiasing shifts, 0.3+ only large colour blocks |
| `colorScheme` | string | `light` (default), `dark`, or `no-preference` — emulates the OS dark-mode setting for pages that use `prefers-color-scheme` |
| `hasTouch` | boolean | Override touch-support emulation (default: on for iPhone/Pixel/iPad presets, off otherwise) |
| `locale` | string | BCP 47 locale to emulate, e.g. `fr-FR` (affects `navigator.language`, number/date formatting) |
| `timezoneId` | string | IANA timezone to emulate, e.g. `America/New_York` (affects locally-rendered times/dates) |
| `geolocation` | object | GPS coordinates to emulate, e.g. `{"latitude": 48.8566, "longitude": 2.3522, "accuracy": 10}` — only affects pages that call the browser Geolocation API themselves |
| `proxyConfiguration` | object | Route the browser through Apify Proxy or your own proxy URLs (off by default). A fresh IP per URL; in compare mode both captures of a pair share one IP |
| `headers` | object | Extra HTTP headers sent with every request, e.g. `{"Authorization": "Bearer ..."}` |
| `cookies` | array | Cookies to send, e.g. `[{"name": "session", "value": "..."}]` — add `domain`/`path` to scope beyond the captured URL |

## Output
One row per URL (or one row for raw HTML):

```json
{
  "url": "https://example.com",
  "format": "jpeg",
  "success": true,
  "error": null,
  "imageUrl": "https://api.apify.com/v2/key-value-stores/.../records/screenshot-....jpg",
  "screenshotKey": "screenshot-1760000000000-0.jpg",
  "contentType": "image/jpeg",
  "byteSize": 84213,
  "capturedAt": "2026-10-16T12:00:00.000Z"
}
```
A failed URL returns `success: false`, `error` set to the failure reason, and `imageUrl: null` — it is not counted as a charged result.

### Visual diff mode output
With `compareUrl` set, each row carries the same fields plus the comparison:

```json
{
  "url": "https://news.ycombinator.com",
  "format": "png",
  "success": true,
  "error": null,
  "imageUrl": "https://api.apify.com/v2/key-value-stores/.../records/screenshot-1792575281654-2.png",
  "screenshotKey": "screenshot-1792575281654-2.png",
  "contentType": "image/png",
  "byteSize": 235200,
  "capturedAt": "2026-10-21T09:34:41.995Z",
  "compareUrl": "https://example.com",
  "compareImageUrl": "https://api.apify.com/v2/key-value-stores/.../records/compare-1792575281762-2.png",
  "compareScreenshotKey": "compare-1792575281762-2.png",
  "diffImageUrl": "https://api.apify.com/v2/key-value-stores/.../records/diff-1792575281915-2.png",
  "diffScreenshotKey": "diff-1792575281915-2.png",
  "diffPixels": 129232,
  "comparedPixels": 2073600,
  "diffPercent": 6.2323,
  "changed": true,
  "baselineWidth": 1920,
  "baselineHeight": 1215,
  "compareWidth": 1920,
  "compareHeight": 1080,
  "sizeMismatch": true
}
```
Real row from run `54YvM4KAyrUjhlEdq` (build 0.1.17, 2026-10-21): Hacker News compared against `example.com` at the default `diffThreshold: 0.1`. The same run compared `example.com` against itself and returned `diffPixels: 0`, `changed: false`, `sizeMismatch: false` — an unchanged page reads as exactly zero, not as rendering noise.

`changed` is simply `diffPixels > 0` at your chosen `diffThreshold`. `diffPercent` is measured over `comparedPixels`, which is the overlapping top-left region of the two captures: full-page screenshots of two pages rarely have identical heights, so when the dimensions differ the Actor diffs the overlap and sets `sizeMismatch: true` (with all four dimensions in the row) rather than failing the comparison. For a like-for-like comparison of two long pages, set `fullPage: false` or a fixed `viewportWidth`/`viewportHeight` so both captures are the same size.

## Pricing
`result` — $0.002 per successful screenshot/PDF, charged only when a capture succeeds. No start fee.
Repeated URLs in one `urls` list are captured and charged once, not once per copy (see the FAQ).

**Where this sits in the market. Features and pricing verified live 2026-10-19** against each
Actor's current Store listing, not marketing copy. The free official `apify/screenshot-url`
(8,789 users) only does full-page/viewport PNG or JPEG — no element selector, device presets,
OG-card preset, raw-HTML input or PDF. Among paid rivals with real feature overlap,
`cheapapi/website-screenshot-api` (302 users as of 2026-10-25) and `moonweil/url-screenshot-api` (216 users) both
already never charge for a failed capture and both support full-page, element and device-preset
capture — that is table stakes in this niche now, not an edge, and we don't claim otherwise.
Where the three of us actually differ: `cheapapi/website-screenshot-api` has no raw-HTML-input
mode and no dedicated 1200x630 OG-card preset, but tiers from $0.00089/result down to
$0.00061/result on its higher plans — cheaper than our flat $0.002/result, so if plain URL-to-
image is all you need, it's the better price. `moonweil/url-screenshot-api` matches our feature
set closely (raw HTML, OG preset, device presets, PDF) but charges a flat $0.004/result, twice
ours — if you want the HTML-input or OG-preset feature set at the lower price, we're the fit.
The one feature `moonweil` had and we didn't was visual diffing; as of build 0.1.17 (2026-10-21)
`compareUrl` closes that, so the diff mode is now available at half its per-result price.
`cheapapi/website-screenshot-api` has no diff mode at all — both rivals' input schemas were read
live from their own build OpenAPI documents on 2026-10-21, not from Store marketing copy.

**Competitor audit, verified live 2026-10-22**: a full re-sweep of the Store's `screenshot` listings (21
candidates, live pricing pulled from each Actor's own `pricingInfos`) found one real new
undercutter: `onescales/website-screenshot-pro` (136 users) tests across multiple device sizes —
real feature overlap, not a bare screenshotter — and its PAY_PER_EVENT ladder drops to
**$0.001/result at GOLD and above**, half our flat $0.002, for any buyer doing enough volume to
reach that tier. Three cheaper-looking listings were checked and ruled out as narrower, not
undercutting the same product: `room_js/url-screenshot-generator` ($0.001/result + a one-time
$0.005 start fee, 84 users) and `viralanalyzer/screenshot-url` (flat $0.001/result, 21 users) are
both plain full-page/viewport PNG-or-JPEG capture with no element selector, device preset,
raw-HTML input or PDF — the same gap the free official Actor has, just cheaper; and
`leadsbrary/screenshot-html-file-from-url` ($0.001/result at GOLD+, 63 users) adds PDF and an
HTML-file export but still has no element selector, device preset or diff mode. `cheapapi` and
`moonweil`'s own prices re-verified unchanged (tiers $0.00089→$0.00061 and flat $0.004
respectively) — no drift since 2026-10-19.

**Two more rivals surfaced 2026-10-24** by Apify's rental-pricing-deprecation auto-conversion
(both were FLAT_PRICE_PER_MONTH rentals until 2026-10, invisible to every per-result price
comparison before that): `dz_omar/ultimate-screenshot` (263 users) has real overlap — 100+
device presets and, unlike us, video (MP4) and GIF export — but its PAY_PER_EVENT ladder charges
$0.007/page-capture at its lowest tier down to $0.005 at GOLD and above, 2.5x–3.5x our flat
$0.002; it's a feature add for buyers who need video/GIF, not a price threat.
`scrapeai/screenshot-downloader` (6 users, flat $0.00249/result) is a bare full-or-partial PNG/
JPEG capture with no element selector, device preset, raw-HTML input, PDF or diff mode — the
same narrow gap as the three already-ruled-out listings above, just newly visible. Both
re-verified live 2026-10-25: user counts and tiered pricing unchanged for each.

## FAQ
**Why JPEG by default instead of PNG?** JPEG at quality 80 is visually indistinguishable from PNG for a normal web page screenshot and never larger, so it is the safer default. How much smaller depends on the page: measured on a long text-heavy Wikipedia article (black text on flat white, PNG's best case) the saving was only 15% — 2.41 MB to 2.04 MB. Measured on a photo-heavy page (a Wikipedia gallery of large photographs) the saving was 63% — 1.95 MB to 725 KB. Expect more savings the more photos/gradients a page has, least on flat text/UI pages. Use `format: "png"` only if you need pixel-exact/lossless output (e.g. comparing against a reference image).

**What actually makes a screenshot smaller?** Cropping, not the format. On that same article, `fullPage: false` took the JPEG from 2.04 MB to 274 KB — a 7.4x cut, versus 15% for the format switch. If you only need to show what the top of the page looked like, set `fullPage: false`. Every output row carries `byteSize` so you can measure this on your own pages.

**Can I screenshot just one element, like a pricing table?** Yes — set `selector` to any CSS selector (e.g. `#pricing-table`). This takes priority over `fullPage`.

**Does it work for pages that need JavaScript to render?** Yes, it uses a real Chromium browser. Set `waitUntil: "networkidle"` for JS-heavy single-page apps that load content after the initial page load. If the page keeps a background connection open (polling, websockets, analytics beacons) `networkidle` can time out even after your content is ready — set `waitForSelector` to a selector that only exists once the real content has rendered (e.g. a chart container or the last row of a table) instead; it's a more precise signal than a fixed delay or network state.

**What if a URL fails to load?** You get a row with `success: false` and an `error` message describing why (timeout, DNS failure, HTTP error, etc.) — the run continues to the next URL and you are not charged for the failure.

**What if the same URL appears twice in my `urls` list?** It is captured once and charged once. As of build 0.1.32 the Actor de-duplicates the list before any browser work starts and logs `Skipped N duplicate URL(s) in \`urls\` -- each unique URL is captured and charged exactly once.` Before that build, a list pasted from a spreadsheet export, a sitemap dump or two concatenated lists would capture the same page twice and bill two `result` events for a byte-identical screenshot. Matching is on the exact URL string after trimming surrounding whitespace, so `https://x.com/a` and ` https://x.com/a ` collapse. It deliberately does **not** fold case or trailing slashes — `/Path` vs `/path` and `/x` vs `/x/` are treated as different URLs and both captured, because many servers genuinely serve different content at those, and silently dropping one you meant to capture would be the worse failure.

**How do I check whether a deploy changed a page?** Put the production URL in `urls` and the staging/preview URL in `compareUrl`. You get one row per pair with `diffPercent`, `diffPixels` and a diff image where every changed pixel is highlighted. For a *time*-based check (same URL, before vs after), screenshot it now, then on a later run compare the live URL against the stored baseline image's URL. Note the Actor compares two live URLs, not a URL against an uploaded image file.

**Why do I get a non-zero diff on a page I did not change?** Fonts, antialiasing, lazy-loaded images, carousels, ad slots, timestamps and animations all shift between two loads of the same page. Raise `diffThreshold` (0.2-0.3) to ignore rendering noise, set `waitForSelector` so both captures happen at the same render state, and prefer `fullPage: false` for pages with infinite scroll. A sub-0.1% diff on a dynamic page is usually noise, not a regression.

**Am I charged twice in compare mode?** No. A comparison captures two screenshots and writes three images (baseline, comparison, diff) but charges a single `result` event — $0.002 per comparison row. A comparison that fails returns an error row and is not charged at all.

**How much does `diffThreshold` actually change the reading?** We measured it, not just described the direction: on the same Hacker News vs `example.com` pair, `diffThreshold: 0.02` read **99.75%** different, `0.1` (the default) read **6.22%**, and `0.3` read **4.47%**. Most of the slider's effect sits in the narrow 0.02-0.1 range — below that, near-black and near-white pixel pairs that are merely *different*, not *visibly* different, all count as changed, so two unrelated pages read as "almost entirely different" regardless of how different they actually look. Above 0.1 the reading is comparatively flat. If you're comparing two genuinely different pages, 0.02 is too strict to be informative; use it only for same-page-over-time checks where you want to catch a single shifted element.

**Can I render my own HTML instead of fetching a URL?** Yes — set `html` to a raw HTML string (e.g. an email template or an Open Graph card you built) and leave `urls` unset; it's rendered directly with no network request.

**Can I capture a page's dark-mode or a different locale/timezone appearance?** Yes — set `colorScheme: "dark"` for pages that style themselves via `prefers-color-scheme`, or `locale`/`timezoneId` for pages that branch on either (date/number formatting, geo-targeted copy, a timestamp rendered in the visitor's local time). All three are plain browser emulation settings, verified by checking the actual rendered pixels/`navigator` values, not just passed through. An invalid `timezoneId` returns a clean error row rather than a silently-wrong capture.

**Can I screenshot through a proxy?** Yes — set `proxyConfiguration` to use Apify Proxy (pick groups/country in the input editor) or paste your own `proxyUrls`. It is **off by default**, because most public pages do not need it and a direct capture is faster. Turn it on when you are capturing a long URL list from one site and hitting per-IP rate limits, or when the page serves different content per country. The Actor draws a fresh IP per URL rather than per run, so the list is spread across the pool. One deliberate exception: in visual diff mode both captures of a pair go through the **same** IP — otherwise a geo-routed page would diff as "changed" when nothing had changed.

**Can I capture a page that needs an API key or my own logged-in session?** Yes — set `headers` for an API key or bearer token (e.g. `{"Authorization": "Bearer ..."}`), or `cookies` to send a session cookie you already have (e.g. `[{"name": "session", "value": "..."}]`). This is for pages you already have a legitimate right to access with your own credentials, like an internal dashboard, a staging environment behind basic headers, or your own account on a site — it does not log in for you or defeat any access control on content you don't already have permission to view. A malformed `headers`/`cookies` entry (missing `name`/`value`) fails the whole run with a clear message rather than a silent per-URL error.

**Can I emulate a different GPS location?** Yes — set `geolocation` to `{"latitude": ..., "longitude": ..., "accuracy": ...}`. This only changes what a page gets back if it calls the browser's own Geolocation API (`navigator.geolocation`) — most pages never do, so it has no visible effect on them. It's for geo-aware dashboards, maps, store locators and "near me" pages that branch on the visitor's coordinates. Verified end to end: a test page that calls `getCurrentPosition()` and renders its result rendered the exact coordinates supplied, not an IP-based guess. An out-of-range latitude/longitude (outside ±90/±180) fails the whole run with a clear message instead of a silently-wrong capture.

## Notes
Only public pages you have a right to view/fetch should be submitted — this Actor does not log you in or bypass a paywall/login you don't already have access to. `headers`/`cookies` let you pass credentials you already hold (an API key, your own session cookie); they do not grant access to anything you couldn't already reach yourself. Issues or feature requests: support@fetchsmith.com. Also available as a hosted API at https://fetchsmith.com

## Related guides
- https://fetchsmith.com/blog/screenshot-png-vs-jpeg-byte-size-measured — PNG vs JPEG vs viewport cropping on the same page, with the real byte sizes and billing lines
- https://fetchsmith.com/blog/http-only-vs-headless-browser-scraping-cost — when you need a browser at all, timed against HTTP-only extraction
- https://fetchsmith.com/blog/visual-diff-threshold-cliff-not-curve — `diffThreshold` swept 0.02/0.1/0.3 on the same pair: the reading drops from 99.75% to 6.22% in one notch, then barely moves
- https://fetchsmith.com/tools
