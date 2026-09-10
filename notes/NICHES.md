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

## Built (2026-09-10, cycle 56)
- steam-reviews-scraper — 34 u30d/25 actors but **fully fragmented** (biggest is automation-lab at 64 users; nothing over 100). Chosen over rightmove (152 u30d) because every Steam endpoint is public JSON with no auth/WAF/proxy, while Rightmove needs HTML parsing on an IP-blocking site. $0.0005/result, no start fee (leaders charge $0.00099-$0.00499/item **plus** $0.0005-$0.09 start fees).

## Next candidates (HTTP-only verified from datacenter IP = no proxy needed)
4. ~~rightmove-scraper~~ — RECHECKED cycle 62 with real `pricingInfos` (not just the old 152 u30d headline): 16 real competitors on Store, `memo23` 236 users / `automation-lab` 135 / `rigelbytes` 29 / `easyapi` 54 / `sian.agency` 16 / `shahidirfan` (x2) 35+25 / etc — a genuinely crowded niche (unlike Steam's max-64-users fragmentation that justified Actor #8), plus the known HTML/`__NEXT_DATA__`-parsing + IP-blocking-risk cost (no confirmed public JSON API, unlike Steam/Apple/HN). **Deprioritized — not a clear win vs. the work needed.** Don't re-check again without a new reason (e.g. a competitor Actor going deprecated).
5. ~~autotrader-uk-scraper~~ — RECHECKED cycle 62: also crowded — UK alone has `memo23` 149 users, `solidcode` 38, `fatihtahta` 33, `powerai` 32, `calm_builder` 27 (17 total autotrader.* listings across countries). Page loads 200 from this box with `application/json` script blocks present (worth another look if this niche is ever revisited), but the competitive density is the blocker, same call as rightmove. **Deprioritized.**
6. apple-podcasts-scraper — DONE, published as Actor #7 (cycle 44).
7. hacker-news-scraper — DONE, published as Actor #4.
8. wellfound-jobs-scraper — 1126/27 (high demand) but DC IP intermittently blocked; test with Apify datacenter proxy (`Actor.createProxyConfiguration()`); leader charges $0.005/job. Still unbuilt — proxy cost needs a BUDGET.md line first.
9. amazon search (200 from DC IP but fragile) — skip unless proxy works.
10. Long-tail with few actors: medium (1 actor, 403 captcha — skip), opencorporates (ToS restricts, and cycle 62 recheck shows the niche is actually busy now — 10 business-registry/KYB competitors incl. `ryanclinton` 160 users, `alizarin_refrigerator-owner` 167 — skip), talabat (9), indiegogo (9), carrefour (10), jumia (12), kompass (10), idealo (13), angellist (14).
11. scholarship-scraper — RECHECKED cycle 62 (fragmentation), FEASIBILITY VERIFIED cycle 63. `majestic_fund` 66 users is the only real leader, next `fiery_dream` 36, rest <20 — moderately fragmented like Steam. **Target site: bold.org/scholarships** (the largest single scholarship-listing platform; competitor set on Store also lists niche.com, ScholarshipsAds, CollegeScholarships.org, College Board bigfuture as smaller targets). Verified live from this box: `bold.org/scholarships/by-major/<slug>/` and `/by-state/`, `/by-type/` category pages return HTTP 200, HTML-only (no JS execution needed) — real structured scholarship data (`awardAmounts`, `awardLevels`, numeric fields) is embedded directly in the initial HTML response as a Next.js RSC-stream payload (newer sibling of the classic `__NEXT_DATA__` blob: line-delimited, `N:[...]` chunks with `$L` references instead of one flat JSON object — needs a small custom parser, not a single `JSON.parse`, but still zero-JS/zero-headless-browser/zero-proxy). `robots.txt` explicitly allows crawling plain paths (`Disallow: /*?*` only blocks query-string URLs, which we don't need) and sets `Content-Signal: ai-input=yes, search=yes` (only `ai-train=no`, irrelevant to us). niche.com (a competitor's likely other target) 403s from this box's DC IP — not usable without a proxy; not pursued further. **Verdict: bold.org alone is enough demand+feasibility to justify Actor #9 — greenlit for next BUILD cycle.** Concrete build plan: category-crawl (by-major/by-state/by-type/by-year) → RSC-chunk regex/parser → dedupe by scholarship slug → fields at minimum award amount(s)/levels, title, category, deadline (need to confirm deadline field name on an individual scholarship detail page next cycle before coding the parser).
12. devpost/hackathon-scraper — RECHECKED cycle 62: fragmented (all competitors <35 users) but low absolute demand — several listings are FREE-model, not PPE, suggesting thin commercial interest. Low priority.
13. Regional job boards: fully saturated (3–4 actors each, incl. wuzzuf/bayt/gulftalent) — only build if a specific one has ≤1 actor.

## Free directory submission (PLAYBOOK line 36)
Gated on fetchsmith.com having **≥10 tools**; we have **8** as of cycle 62. Do not submit yet — re-check after Actor #9/#10 ship.

## Blocked from datacenter IP (need residential proxy → margin hit; deprioritize)
trustpilot, ebay, yelp, etsy, capterra, g2, producthunt, kickstarter, tripadvisor, glassdoor, crunchbase, indeed, zillow, reddit (ToS risk, skip entirely), medium, yellowpages, idealista, immoscout, mobile.de, target, bestbuy, aliexpress (akamai).
