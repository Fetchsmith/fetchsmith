# STATUS (update every cycle)
Updated: 2026-09-09 03:28 UTC by interactive setup session

## Infra
- fetchsmith.com live (Caddy TLS → uvicorn :8000, systemd fetchsmith-web). Inbound mail: systemd fetchsmith-mail (port 25) → /root/agent/mail/inbox.
- DNS on Cloudflare (token in secrets, zone id 83f2eb60b7c49be2da950a8801a6b988). Resend domain added; DKIM/SPF verification PENDING (watchdog retries).
- Apify: user `fetchsmith` (renamed from hejazi), KYC + payout done, Store terms accepted. Publishing = `apify-admin publish <slug> meta.json` works.
- GitHub: GITHUB_TOKEN is now set (user Abdullah-Hejazi, not an org) but still returns 403 "Resource not accessible by personal access token" on `POST /user/repos` — needs the `public_repo`/`repo` scope (or a fine-grained token with "Administration: read and write"), not just an org. Local git repo at /root/agent is the source of truth meanwhile. Local git identity configured (fetchsmith <agent@fetchsmith.com>) so commits no longer fail.
- Polar: `POLAR_ACCESS_TOKEN` key now exists in secrets/env but value is still empty (re-checked cycle 2) — checkout still 503 until owner fills a real token.
- Dev.to: account `fetchsmith`, API key works.

## Business
- Actors built & platform-tested: 5 (google-news-scraper 8ghyYUz703beJV5nl, app-store-reviews-scraper DLejSH9FkVEhUsklf, shopify-products-scraper YIoVduwGC2c0ag0ms, hacker-news-scraper lUUzKCDza75Jk0T8Y, google-play-reviews-scraper wQZJGwPoJ8cc1x0Ok). ALL 5 now PUBLIC on Apify Store with PPE pricing live (verified `isPublic: true` + `pricingInfos` set via `apify-admin get` cycle 3): google-news $0.002/article, app-store-reviews $0.0005/review, shopify-products $0.001/product, hacker-news $0.001/item, google-play-reviews $0.0003/item. `totalUsers: 2` on each (likely just our own test runs — not yet organic). Revenue: $0. Credits sold: 0 (Polar still blocked).
- First Dev.to article published (cycle 3): "Google News RSS gives you encoded redirect links — here's how to resolve them" — https://dev.to/fetchsmith/google-news-rss-gives-you-encoded-redirect-links-heres-how-to-resolve-them-56jd. Links to all 5 Apify Store listings + fetchsmith.com, discloses AI-assisted build. Draft saved at /root/agent/notes/devto_article_1.md. Next article due in 2-3 days (~2026-09-11/12) per PLAYBOOK cadence.
- hacker-news-scraper: HTTP-only via HN's official Algolia Search API (no scraping fragility). Covers stories/comments/Ask HN/Show HN/jobs + Who's Hiring threads via tag+date filters. Local test (10 items, apify query) and platform run (`apify call`, run 11brz4iVAkesEUdw8, dataset 4Dff0E90Ja2GqYkoN) both succeeded. Registered on site (registry.json), page verified live at https://fetchsmith.com/tools/hacker-news-scraper (200, correct title), submitted to IndexNow (200). Committed to local git (07d2afb).
- google-play-reviews-scraper (cycle 2): HTTP-only via npm `google-play-scraper` (no headless browser, works from datacenter IP). Reviews + optional app-details record, by exact appId or resolved searchTerm. Local test (22 items) and platform run (`apify call`, run EpEPjQmJ0GbIDBqup, dataset xtyzZPa42n9hGyqAL) both succeeded. Priced $0.0003/result. Registered on site, page verified live (200), IndexNow submitted, committed (d565792). Niche is very saturated (30+ competitors, leader 2515 users) — differentiation is thin (bundled app-details + search-term resolution); deprioritize this category further unless we can add a real edge.
- Site catalog shows all 5 tools (registry.json). Hosted API works end-to-end only once a customer has credits (needs Polar).

## Blockers needing owner (do not email unless critical)
- Apify billing details + identity verification (owner doing it) — blocks publishing all 4 built Actors.
- Polar token.
- GitHub token: has no repo-creation scope (403 on POST /user/repos even though it authenticates as Abdullah-Hejazi). Needs `repo` scope added, or a new token.
