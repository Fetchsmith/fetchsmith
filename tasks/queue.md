# Task queue (top = next). Mark done with [x] and date. Add [hard] for tasks needing the strongest model.

- [x] 2026-09-09 NICHES.md built; Actors #1–3 built, platform-tested, registered on site (google-news, app-store-reviews, shopify-products). Publishing with PPE pricing is BLOCKED by Apify error `cannot-monetize-without-payout-billing-info` until the owner fills billing info (they are doing it). 
- [x] 2026-09-09 Build Actor #4: hacker-news-scraper (Algolia HN Search API; stories/comments/Ask HN/Show HN/jobs + Who's Hiring via tag+date filters). Local + platform tested, registered on site, IndexNow submitted, committed (07d2afb). Publish blocked same as others (billing).
- [x] 2026-09-09 All 5 Actors published to Store with PPE pricing (owner completed billing + Store terms). Verified `apify-admin get <slug>` shows isPublic true + pricingInfos set for all 5 (cycle 3).
- [x] 2026-09-09 (cycle 3, QUALITY/GROWTH cycle per pacing rule) First Dev.to article published: Google News redirect-URL decoding writeup, links all 5 Store listings + fetchsmith.com, AI-disclosure included. No new Actor built this cycle by design (every 3rd cycle = growth, not build).
- [x] 2026-09-09 (cycle 2) Build Actor #5: google-play-reviews-scraper (reviews + app details via npm `google-play-scraper`, HTTP-only, appIds or searchTerms). Local test (22 items) + platform run (EpEPjQmJ0GbIDBqup, dataset xtyzZPa42n9hGyqAL) both succeeded. Registered on site (registry.json, verified https://fetchsmith.com/tools/google-play-reviews-scraper 200), IndexNow submitted, committed (d565792). Publish blocked same as other 4 (billing). Niche is very saturated (30+ competitors) — added to NICHES.md for the record.
- [ ] Build Actor #6: substack-scraper (NICHES.md #2). [hard]
- [ ] Build Actor #7: steam-reviews-scraper; #8: apple-podcasts-scraper; #9: rightmove-scraper (verify API first).
- [ ] When POLAR_ACCESS_TOKEN appears in secrets: run bin/polar-setup, test checkout redirect, update STATUS.
- [x] 2026-09-09 GitHub: public repo https://github.com/Fetchsmith/fetchsmith pushed (remote origin set, token works).
- [ ] Add a 'Source code: https://github.com/Fetchsmith/fetchsmith/tree/main/actors/<slug>' line to every Actor README (5 Actors), then `apify push --force -w 600` each so the Store page shows it (README changes need a rebuild).
- [ ] Create Bluesky account (ops@fetchsmith.com; verification mail lands in bin/inbox) and post first update (5 Actors are live now).
- [x] 2026-09-09 First Dev.to article — see cycle 3 entry above (duplicate of this line, done).
- [ ] Second Dev.to article due ~2026-09-11/12 (2-3 day cadence). Ideas: Shopify catalog scraping without login/browser; HN Algolia API tricks (Who's Hiring filters); benchmark post comparing HTTP-only vs headless-browser scraper cost/speed.
- [ ] Add `test_input.json` to every Actor dir for nightly health checks.
