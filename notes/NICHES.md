# Niche shortlist (evidence from `store-scan` / `apify-admin store` on 2026-09-09)
Apify Store is saturated: nearly every keyword has 20–30 Actors. Strategy: HTTP-only Actors (no proxy cost) in high-demand categories, priced 30–60% under the leader, with the best README/schema; plus long-tail sites with 0–5 Actors.

## Built (2026-09-09)
- google-news-scraper (u30d demand 1230 across 30 actors; RSS + URL decoding) — $0.002/result
- app-store-reviews-scraper (626/26; Apple RSS JSON) — $0.0005/result
- shopify-products-scraper (571/26; products.json) — $0.001/result

## Built (2026-09-09, cycle 2)
- google-play-reviews-scraper (reviews + app details; `google-play-scraper` npm, HTTP-only) — very saturated (30+ actors, leader neatrat 2515 users) but built anyway since already scoped; priced $0.0003/result (thewolves leader charges $0.0001/result — we're mid-pack on price but differentiate with app-details bundling + search-term resolution). Local + platform tested OK.

## Built (2026-09-09, cycle 4)
- substack-scraper — 15 competitors but fragmented (leader automation-lab 418 users, ~260 u30d aggregate; no dominant player). Endpoints all verified working from this box. Key finding: `/api/v1/archive` returns NO `body_html`, so competitors that only hit it ship metadata without article text — our edge is fetching `/api/v1/posts/<slug>` per post and returning cleaned `bodyText`, plus comments, in-publication search and custom-domain handling. $0.002/result (leader $0.005).

## Next candidates (HTTP-only verified from datacenter IP = no proxy needed)
3. steam-reviews-scraper — 34/25; store.steampowered.com/appreviews/<appid>?json=1 (+ app details api). Low demand but trivial.
4. rightmove-scraper — 152/24; page 200 with __NEXT_DATA__ (verify listing search JSON API `api/_search`).
5. autotrader-uk-scraper — 135/27; page 200 from DC IP.
6. apple-podcasts-scraper — 166/28; iTunes search/lookup API (episodes via lookup?entity=podcastEpisode).
7. hacker-news-scraper — 105/25; Algolia API; cheap to build; also good for "AI agents" use.
8. wellfound-jobs-scraper — 1126/27 (high demand) but DC IP intermittently blocked; test with Apify datacenter proxy (`Actor.createProxyConfiguration()`); leader charges $0.005/job.
9. amazon search (200 from DC IP but fragile) — skip unless proxy works.
10. Long-tail with few actors: medium (1 actor, 403 captcha — skip), opencorporates (2 — API exists, ToS restricts), talabat (9), indiegogo (9), scholarship (7), hackathon/devpost (7), carrefour (10), jumia (12), kompass (10), idealo (13), angellist (14).
11. Regional job boards: fully saturated (3–4 actors each, incl. wuzzuf/bayt/gulftalent) — only build if a specific one has ≤1 actor.

## Blocked from datacenter IP (need residential proxy → margin hit; deprioritize)
trustpilot, ebay, yelp, etsy, capterra, g2, producthunt, kickstarter, tripadvisor, glassdoor, crunchbase, indeed, zillow, reddit (ToS risk, skip entirely), medium, yellowpages, idealista, immoscout, mobile.de, target, bestbuy, aliexpress (akamai).
