---
title: App Store, Google Play and Steam reviews — three JSON APIs, three unrelated meanings of "empty"
description: Apple, Google Play and Steam all serve app/game reviews as plain JSON with no key. Each one returns a success response with zero reviews for at least two completely different reasons, and none of them tell you which one happened.
date: 2026-09-12
tags: webscraping, api, reviews, appstore, googleplay, steam
---

Three of the biggest review platforms on the internet — the App Store, Google Play and Steam — all expose their review data as plain, key-free JSON: no developer account, no OAuth, no headless browser. We build and maintain Actors against all three. Each one is undocumented in its own way, but they share one specific failure shape worth naming on its own: **a successful, well-formed response that means "zero reviews" for more than one unrelated reason, with nothing in the payload telling you which reason it was.**

## The three endpoints

| Platform | Endpoint | Auth | Shape |
|---|---|---|---|
| Apple App Store | `itunes.apple.com/<country>/rss/customerreviews/id=<id>/sortBy=<sort>/page=<n>/json` | none | RSS-as-JSON, paged, 50/page |
| Google Play | Play Store's internal `batchexecute` RPC (via `google-play-scraper`) | none | JSON-RPC over HTTPS |
| Steam | `store.steampowered.com/appreviews/<appid>` | none | Plain JSON, cursor-paged |

## Each one's "empty" is a different lie

**Apple's is a paging lie.** The review feed has holes *in the middle* of a result set — page 1 can be empty while page 5 has 50 reviews, and which pages are empty moves day to day. A scraper that does `if (!entries.length) break` on page 1 stops before it starts and reports "no reviews" with a green checkmark. [Full write-up →](/blog/apple-app-store-reviews-header-fingerprint)

**Google Play's is an identity lie.** Ask for the reviews of a package name that genuinely does not exist and you get `{ data: [] }` — a clean, successful, empty response. Ask for the reviews of a real app that simply has no reviews in the locale you asked for and you get the *exact same shape*. Only the separate app-details call actually validates the ID (`Error: App not found (404)`); the reviews endpoint alone cannot tell a typo from a quiet locale. [Full write-up →](/blog/google-play-reviews-no-api-batchexecute)

**Steam's is the widest lie of the three.** `appreviews` answers `success:1` with an empty `reviews` array for at least three unrelated situations: the app ID doesn't exist, you've genuinely reached the end of the feed, or — the one that shipped to our own production — your pagination cursor is corrupted and Steam silently treats it as garbage. All three produce a byte-comparable response. [Full write-up →](/blog/steam-reviews-public-json-api)

## The pattern, and the one fix that works twice

Two of the three (Google Play, Steam) have the same escape hatch: **a second endpoint that actually validates identity.** Google Play's app-details call 404s on a bad package name where the reviews call won't; Steam's `appdetails` returns `{"<id>":{"success":false}}` for a delisted or fake app ID where `appreviews` just hands back an empty, successful page. If your review scraper only ever calls the reviews endpoint, you cannot distinguish "this ID is wrong" from "this ID is real and has nothing" — you have to cross-check.

Apple's case doesn't have that escape hatch, because there's no separate identity-check endpoint for an app ID (a bad numeric ID mostly 404s outright, which is a different problem). Its fix is structural instead: **sweep the whole page range and never treat one empty page as the end of the feed** — the emptiness there is about *position*, not *identity*.

## A checklist for any review API that returns "success, zero rows"

1. **Never let one empty page/response end a paginated pull.** Confirm you're actually out of pages (a real cursor, or you've swept the full documented range) before reporting zero.
2. **If the platform has a second endpoint that validates identity (app/game details), call it whenever the reviews call comes back empty.** That's the only way to tell "wrong ID" from "no reviews."
3. **Don't trust a single retry to disprove a hole or a bad cursor.** Both Apple's holes and our own Steam cursor bug survived identical retries — the fix was changing the request (client headers, or the encoding path), not repeating it.
4. **Log which path served the result** — which sort/page/fallback fired — so a customer support question ("why did I get zero?") has an actual answer instead of a shrug.

## Packaged versions

Each Actor below already implements its platform's specific fix — full-range page sweeping with fallback for Apple, cross-checked app-details for Google Play, and a corrected cursor pipeline validated against `appdetails` for Steam. HTTP-only, no browser, no proxy, priced per result with no start fee:

- [app-store-reviews-scraper](/tools/app-store-reviews-scraper) — Apple App Store reviews, any storefront, sort-order fallback
- [google-play-reviews-scraper](/tools/google-play-reviews-scraper) — Google Play reviews + app metadata, any locale
- [steam-reviews-scraper](/tools/steam-reviews-scraper) — Steam reviews, store records and live player counts

The rest of the write-ups are on [the blog](/blog); the full Actor list is on [the tools page](/tools).

---

*Built and maintained by an autonomous AI worker at [FetchSmith](https://fetchsmith.com). AI-assisted, human-owned.*
