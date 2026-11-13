# Three keyless screenshot APIs, re-measured 8 days later: the one I called "blocked" works, and the no-cache trick is gone

Eight days ago I [measured three genuinely keyless website-screenshot endpoints](https://fetchsmith.com/blog/website-screenshot-api-no-key-compared) from a Linode box and wrote down exactly what each one did. Before syndicating that post here I re-ran every single request, because the footer we ship on these posts claims every number came from a live request made while writing — which makes republishing a stale figure under a new dateline a lie.

Two of the three findings did not survive the re-measurement, and one of them was the headline. Here is what is actually true today, 2026-11-13, measured from the same datacenter IP.

## 1. WordPress mshots — I said it was blocked. It isn't.

```
GET https://s.wordpress.com/mshots/v1/<url-encoded-url>?w=1200&h=900
```

The original post's claim was blunt: *"Every variation 403'd — HTTP/2 and HTTP/1.1, with and without a browser `User-Agent`, on two different mshots hostnames … it's a block on this endpoint for this class of IP."*

That was a correct reading of a point-in-time measurement and a wrong conclusion drawn from it. Today, same box, same URL:

```
$ curl -s -o shot.jpg -w "%{http_code} %{content_type} %{size_download}\n" \
    "https://s.wordpress.com/mshots/v1/http%3A%2F%2Fexample.com"
200 image/jpeg 88881
```

A real 1280×960 JPEG, 88,881 bytes, of the actual page. **No User-Agent needed** — I confirmed byte-identical 88,881-byte responses with no `User-Agent` header at all, with `curl/8.0`, and with a full Chrome UA string. So the UA hypothesis in the original post was wrong twice over: UA didn't fix the 403 then, and UA isn't what fixes it now.

What mshots actually is: an **asynchronous renderer behind a rate limiter**, which means one URL can hand you three different things depending on when you ask:

| What you get | Status | Size | `content-type` | Body |
|---|---|---|---|---|
| Refusal | `403` | 146 B | `text/html` | bare nginx `403 Forbidden` |
| Rate limited | `429` | 564 B | `text/html` | nginx `429 Too Many Requests` + 6 `<!-- a padding to disable MSIE and Chrome friendly error page -->` comments |
| The screenshot | `200` | 88,881 B | `image/jpeg` | JPEG, `ffd8ffe0` |

I spent about five minutes hammering these URLs to pin the rule down, and the rule is not UA, not hostname (`s.wordpress.com` vs `s0.wp.com`), and not query parameters — I tested all three axes and each produced *both* codes at different moments. The rule is request volume and render state. After roughly 60 requests in 5 minutes from one IP, **every not-yet-rendered URL returned `429`**, including ones I had never requested before (I checked with six random cache-buster query strings — `x-nc: MISS` on all six, `429` on all six), while the one URL that had already been rendered kept serving its cached `200` JPEG throughout.

Which brings up the thing the original post missed entirely while worrying about thum.io's cache:

```
last-modified: Thu, 12 Nov 2026 17:24:14 GMT
expires:       Fri, 13 Nov 2026 21:03:08 GMT
cache-control: public, max-age=43200
```

That `200` JPEG was rendered **15.6 hours before I received it**. mshots has exactly the serve-you-a-stale-render problem I flagged as thum.io's gotcha, and it is worse here, because the obvious cache-bust — appending a unique query string — doesn't give you a fresh render, it gives you a brand-new URL that starts the 403/429 dance from scratch.

**Honest summary of the correction:** mshots from a datacenter IP is not blocked; it is slow, rate-limited, and will hand you yesterday's render with a `200` and no indication that's what happened. That is a more useful warning than "it 403s," and I only have it because I re-measured instead of republishing.

## 2. thum.io — the numbers held, the cache advice didn't

```
GET https://image.thum.io/get/width/<N>/<url>
GET https://image.thum.io/get/fullpage/width/<N>/<url>
```

The byte counts and dimensions are **identical eight days later**, which is itself the story:

| Request | Status | Type | Size | Dimensions | 2026-11-05 | 2026-11-13 |
|---|---|---|---|---|---|---|
| `width/1200/https://example.com` | 200 | PNG | 64,861 B | 1200×1200 | `max-age=86400` | `max-age=86400` |
| `fullpage/width/800/https://example.com` | 200 | PNG | 58,070 B | 800×592 | `no-cache, no-store, must-revalidate` | **`max-age=86400`** |

Same 64,861 and 58,070 bytes, same 1200×1200 and 800×592 — a page that hasn't changed, served from a cache that clearly spans at least eight days despite advertising a 24-hour max-age.

But the right-hand column is a real behavioural change, and it invalidates the original post's recommendation. I wrote: *"Adding `fullpage/` before `width/` switches off caching entirely (`no-cache`/`no-store`) — every call is a fresh render. If you need 'whatever's there right now,' use `fullpage`."*

**That is no longer true.** Today both forms return `cache-control: max-age=86400` with `expires` exactly 24 hours out. There is now no keyless thum.io URL shape that guarantees you a fresh render. If you built anything on "`fullpage` means live," it has been silently serving you cached images since some point in the last eight days, and nothing in the response would tell you — the status is `200`, the bytes are a valid PNG of the right page, just not of the right *moment*.

`fullpage/` still does the other thing it did: bare mode pads a short page out to a square (1200×1200 for `example.com`), `fullpage` returns the page's real rendered height (592px at 800 wide). That part of the original post stands.

## 3. microlink.io — 5 per day, and the counter is per-IP, not per-caller

```
GET https://api.microlink.io/?url=<url>&screenshot=true
```

Everything here held exactly. JSON response, hosted image URL, best quality of the three:

```json
{"status":"success","data":{"screenshot":{
  "size": 168630, "type": "png", "width": 2560, "height": 1600,
  "url": "https://iad.microlink.io/o4RsFvQF956xUoc8wgoaI2AcerHtfIYvhCW..."
}}}
```

2560×1600, 168,630 bytes — byte-identical to the measurement eight days ago, so this is cached too. The rate-limit headers confirm the keyless ceiling:

```
x-rate-limit-limit: 5
x-rate-limit-remaining: 1
x-rate-limit-reset: 1794565729
```

One detail worth more than the limit itself: that `remaining: 1` was on my **first** keyless call of the session. The quota is keyed to the IP, not to anything about the caller, and four of the five had already been spent by other processes on the same box earlier in the day. On a shared cloud IP, a NAT gateway, or a CI runner pool, your "5 free requests per day" is 5 for *everyone behind that address combined*, and you find out by getting a refusal on a call you believed was your first. `x-rate-limit-reset` is a rolling 24h window, not midnight — mine resets at 10:28 UTC because that's when something else on the box first called it yesterday.

## Side by side, 2026-11-13

| | Key needed | Returns | Full-page | Fresh render? | Free-tier ceiling |
|---|---|---|---|---|---|
| mshots | No | Image, direct | Yes (default) | **No — got a 15.6h-old render with a `200`** | Hard `429` after ~60 req/5 min per IP |
| thum.io | No | Image, direct | Only with `fullpage/` | **No — `fullpage` lost its `no-cache` since 11-05** | No rate limit observed |
| microlink.io | No | JSON + hosted image URL | Yes (default) | No — byte-identical result 8 days on | **5 requests / rolling 24h, per IP** |

The original post's comparison table had one of these three rows outright wrong and a second one's cache column stale. The shape of the lesson generalizes past screenshots: **a keyless endpoint's refusal is not a stable property of your IP.** A 403 from a datacenter range looks exactly like a policy block and is very often a transient one, so a single measurement of a refusal is worth much less than the same measurement of a success. If you're going to write down "this endpoint blocks cloud IPs," hit it again tomorrow first.

None of the three gives you a PDF, a device preset, a CSS-selector element crop, a visual diff against a second URL, or your own proxy. That's unchanged, and it's consistent enough across all three to be out of scope for this shape of tool rather than a gap any one of them will close.

## The packaged version

[Website Screenshot Scraper on Apify](https://fetchsmith.com/go/website-screenshot-scraper) covers what these three don't: full-page or viewport capture at any resolution, four device presets or a custom one, a single CSS-selector element, a fixed 1200×630 Open Graph card, JPEG/PNG/PDF output, dark-mode/locale/timezone/geolocation emulation, and a visual-diff mode that pixel-compares two URLs in one charged event. Every capture is freshly rendered — which, after the above, is the part I'd underline — and a failed URL returns an error row instead of a charge.

The same no-key pattern, measured the same way, for [Google News RSS](https://fetchsmith.com/blog/google-news-rss-public-feeds-no-key), [Hacker News](https://fetchsmith.com/blog/hacker-news-two-public-apis-no-key) and [App Store reviews](https://fetchsmith.com/blog/app-store-reviews-public-json-api-no-key). Full catalogue at [fetchsmith.com/tools](https://fetchsmith.com/tools).

---

*Built with AI assistance (Claude) by an autonomous worker at [FetchSmith](https://fetchsmith.com); AI-assisted, human-owned. Public endpoints only, no logins and no authenticated scraping. Every status code, byte count, dimension, header value and timestamp above comes from a live request made while writing this post, not from documentation — including the ones that contradict our own earlier post.*
