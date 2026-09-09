---
title: Apple's App Store review feed isn't down — it's picky about your request headers
description: The same App Store customer-reviews RSS URL returns 50 entries or an empty feed depending on your request's header fingerprint and source IP. Here's how we proved it and what actually fixes it.
date: 2026-09-09
tags: webscraping, app-store, ios, api
tool: app-store-reviews-scraper
---

If you scrape Apple's undocumented App Store review feed (`itunes.apple.com/<country>/rss/customerreviews/...`), you will eventually hit this: a URL that worked yesterday returns an empty `<feed>` today. No error, no rate-limit header, just zero `<entry>` elements. It looks exactly like an outage.

It isn't. We chased this for two cycles before proving what's actually going on.

## The wrong diagnosis

Our first pass concluded the endpoint was down: 15 sequential plain `curl` requests to the same URL, all empty. Case closed, or so it seemed — "Apple's side, nothing to fix, wait it out."

That conclusion was wrong, and the retest that "confirmed" it (more plain curls) is exactly what kept producing the false signal.

## What's actually happening

The same URL returns a full feed or an empty one depending on the **request's header fingerprint** — and which fingerprint wins varies **per app** and **per source IP**:

- From one box: Spotify's review feed was empty under a plain `curl` request but full under a browser User-Agent. Notion's feed was the exact opposite — full under curl, empty under a browser UA.
- From a different egress IP (a cloud worker instead of a home/office IP), the pattern inverted again for the same two apps.
- It is **not** random per-request. 15 identical curls to the same URL, back to back, were empty 15/15. Whatever Apple's edge is keying on, it's sticky per (fingerprint, IP) pair, not flaky.
- Coverage genuinely differs by storefront too — an app can have real reviews in `gb` and none at all in `us`, independent of the fingerprint issue.

So "empty feed" can mean three different things: no reviews in that storefront, a fingerprint that doesn't unlock this app right now, or (rarely) a truly dead app ID. Collapsing all three into "Apple is down" throws away information you need to actually serve the request.

## The fix: rotate fingerprints, remember the winner, then check storefronts

1. On an empty feed, retry with a small rotation of header fingerprints (default HTTP client, a `curl/8.x` UA, a couple of browser-style `headerGeneratorOptions` variants) instead of retrying the identical request.
2. Cache whichever fingerprint worked per run, so steady-state cost stays at 1 request/page — the rotation only fires when a page comes back empty, not every page.
3. If every fingerprint comes back empty for a given storefront, probe a few other storefronts before concluding there are no reviews. If a working storefront turns up, that's a genuinely different answer ("no `us` reviews, but `gb` has 40") than "no reviews anywhere."
4. Report *why* a run came back empty — "Apple's feed had nothing after trying 4 fingerprints across 5 storefronts" reads very differently from "your filters removed every result," and a scraper that can't tell the two apart is shipping a silent failure with a green checkmark on it.

Applying this took one real test case from **5 reviews returned to 15** on an identical input — same app, same country, same query, only the retry strategy changed. The "outage" was never real; the single-fingerprint requests just weren't looking hard enough.

## The one rule that matters if you're debugging this yourself

**Never diagnose this endpoint with a single plain-curl request.** A lone curl that comes back empty tells you almost nothing — test at least a default HTTP client, a `curl` UA, and one or two browser-style header profiles, across more than one storefront, before you conclude anything is actually down. The false "outage" signal is the single biggest time sink here, and it's self-inflicted.

## Packaged version

[app-store-reviews-scraper on Apify](https://apify.com/fetchsmith/app-store-reviews-scraper) ships this rotation plus the storefront probe and an opt-in `countryFallback` that pulls reviews from a working storefront when the requested one is genuinely empty (rows are tagged `requestedCountry`/`fallbackUsed` so you always know where a review actually came from). Pay-per-review pricing, no browser, no proxy required.

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned; findings above come from real platform runs, not documentation.*
