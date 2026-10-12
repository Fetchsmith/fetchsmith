# Google Play has no reviews API — and the endpoint it does have can't tell a typo from an empty app

There is no `developer.google.com` endpoint for "give me the public reviews on this app." What the Play Store website itself calls, under the hood, to render the reviews tab is Google's internal `batchexecute` RPC layer — the same protocol behind a chunk of Google's web UIs. It's undocumented, but it's plain JSON over HTTPS, no API key, no auth, no browser. We build on top of it via the `google-play-scraper` npm package, which wraps the RPC calls. Three things worth knowing if you're going to rely on it — every number below was re-measured live today before posting, 31 days after the original write-up.

## The `num` parameter isn't a page size, it's a real total

Ask for `num: 500` reviews and you might expect one page's worth, or a client-side truncation. Neither — the library follows Google's internal pagination token for you until it hits the number you asked for:

```
num: 300  -> 300 rows returned  (0.4s)
num: 500  -> 500 rows returned  (0.8s)
num: 5000 -> 5000 rows returned (6.2s)
```

All pulled live against Spotify's Android app (`com.spotify.music`), from a 1 vCPU box, no browser anywhere in the stack. There's no documented hard ceiling we hit at 5000; we cap our own scraper at 5000 reviews per app mostly to keep a single run predictable, not because Google stops you sooner.

## `country` and `language` aren't a display filter — they're a different review set

The obvious assumption is that Play Store reviews are one global pool and `country`/`language` just localize formatting. They don't. Pulling the same app's 20 newest reviews for `country=us&lang=en` versus `country=de&lang=de` gives you **zero overlapping review IDs** between the two sets — not translated duplicates, not a subset, a fully disjoint pool of reviewers:

```
us/en: 20 rows
de/de: 20 rows
overlapping review ids: 0
```

If you need global coverage, you run once per locale you care about; there's no "give me everything" mode.

## The error asymmetry that will produce a misleading message if you don't check for it

Fetch app details for a package name that doesn't exist and the library throws cleanly:

```
gplay.app({ appId: 'com.totally.fake.app.doesnotexist12345' })
-> Error: App not found (404)
```

Fetch *reviews* for that exact same bad ID, and it does not throw. It returns a normal, successful response with an empty array:

```
gplay.reviews({ appId: 'com.totally.fake.app.doesnotexist12345', num: 5 })
-> { data: [] }   // no error, no warning, nothing
```

That's the same shape you get from a *real* app that genuinely has zero reviews in the locale you asked for. If your code only looks at the reviews call, a typo'd package name and "this app has no German reviews" are indistinguishable, and the honest fix — telling the user their app ID is wrong — depends entirely on cross-checking the details call, which is the one endpoint that actually validates the ID.

We shipped this exact ambiguity in earlier builds: a bad `appId` with app details enabled would fail the details call silently (just a log line) and then report "Google Play returned zero reviews — try a different country/language," which sends a user with a simple typo down the wrong path entirely. Fixed by making the details-call failure authoritative when it's specifically a 404: we now report "these appIds don't exist on Google Play" instead, and only fall back to the country/language suggestion when the app is confirmed real and the reviews call itself came back empty.

## Two smaller things worth noting

- `installs` is a formatted display string (`"1,000,000,000+"`); the field to actually sort or filter on is `minInstalls`, a plain integer (`1000000000` for the same app, measured today).
- The reviews array has no rating-count promise attached to it — `reviewsCount` on the app-details record can be in the millions while the reviews endpoint, like every Play Store client, only ever surfaces a bounded slice of written reviews. A short review count relative to the app's total rating count is normal, not a sign anything failed.

## Packaged version

[google-play-reviews-scraper on Apify](https://fetchsmith.com/go/google-play-reviews-scraper) wraps app details and reviews behind one input — package ID or search term, any Play Store locale, server-side filtering by star rating, keyword and date range so you're only charged for rows you actually want, and the invalid-app-id message fixed above.

If you also pull App Store or Steam reviews, see [how each platform's "empty" means something different](https://fetchsmith.com/blog/app-store-review-apis-three-silent-empties) — Google Play's is an identity problem, only solvable by cross-checking the details call.

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; every number and error message above comes from live calls made while writing this post.*
