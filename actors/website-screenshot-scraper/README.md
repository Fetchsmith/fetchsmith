# Website Screenshot Scraper

Capture a screenshot or PDF of any public URL using a real Chromium browser. Device presets, element capture, Open Graph card sizing and raw-HTML rendering are built in — the free official `apify/screenshot-url` Actor covers none of these.

## What it does
- Renders a public URL (or raw HTML you provide) in headless Chromium and captures a JPEG, PNG or PDF.
- Full-page or viewport-only capture, a single CSS-selector element, or a fixed 1200x630 Open Graph card.
- Device presets (desktop, iPhone 14, Pixel 7, iPad) or a custom viewport size.
- Pay per successful capture: a URL that fails to load (timeout, DNS error, 4xx/5xx) returns an error row and is **never charged**.
- The run start is free; you only pay for screenshots actually returned.

## Input
| Field | Type | Description |
|---|---|---|
| `urls` | array of strings | Pages to screenshot (default `["https://example.com"]`) |
| `html` | string | Render this raw HTML instead of fetching a URL (ignores `urls`, produces one row) |
| `format` | string | `jpeg` (default, recommended), `png` (lossless), or `pdf` |
| `quality` | integer | JPEG quality 10-100 (default 80) |
| `fullPage` | boolean | Capture full scrollable height, not just the first screen (default true) |
| `devicePreset` | string | `custom`, `desktop`, `iphone`, `pixel`, `ipad` |
| `viewportWidth` / `viewportHeight` | integer | Used when `devicePreset` is `custom` |
| `selector` | string | CSS selector to capture a single element instead of the whole page |
| `ogCard` | boolean | Force a 1200x630 viewport capture for social-share previews |
| `waitUntil` | string | `load` (default), `domcontentloaded`, or `networkidle` |
| `delayMs` | integer | Extra wait after load before capturing (0-15000ms) |

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

## Pricing
`result` — $0.002 per successful screenshot/PDF, charged only when a capture succeeds. No start fee.

## FAQ
**Why JPEG by default instead of PNG?** JPEG at quality 80 is visually indistinguishable from PNG for a normal web page screenshot but 5-10x smaller, especially on long, text-heavy pages. Use `format: "png"` only if you need pixel-exact/lossless output (e.g. comparing against a reference image).

**Can I screenshot just one element, like a pricing table?** Yes — set `selector` to any CSS selector (e.g. `#pricing-table`). This takes priority over `fullPage`.

**Does it work for pages that need JavaScript to render?** Yes, it uses a real Chromium browser. Set `waitUntil: "networkidle"` for JS-heavy single-page apps that load content after the initial page load.

**What if a URL fails to load?** You get a row with `success: false` and an `error` message describing why (timeout, DNS failure, HTTP error, etc.) — the run continues to the next URL and you are not charged for the failure.

**Can I render my own HTML instead of fetching a URL?** Yes — set `html` to a raw HTML string (e.g. an email template or an Open Graph card you built) and leave `urls` unset; it's rendered directly with no network request.

## Notes
Only public pages you have a right to view/fetch should be submitted — this Actor does not bypass logins or paywalls. Issues or feature requests: support@fetchsmith.com. Also available as a hosted API at https://fetchsmith.com

## Related guides
- https://fetchsmith.com/tools
