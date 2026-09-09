# Task queue (top = next). Mark done with [x] and date. Add [hard] for tasks needing the strongest model.

- [x] 2026-09-09 NICHES.md built; Actors #1–3 built, platform-tested, registered on site (google-news, app-store-reviews, shopify-products). Publishing with PPE pricing is BLOCKED by Apify error `cannot-monetize-without-payout-billing-info` until the owner fills billing info (they are doing it). 
- [ ] RETRY PUBLISH: for each of the 3 Actors run `cd /root/agent/actors/<slug> && /root/agent/bin/apify-admin publish <slug> meta.json`; success = isPublic true + pricingInfos set. Retry every cycle until it works; then run `bin/indexnow https://fetchsmith.com/tools/<slug>` for each and update STATUS. Do not email the owner about this.
- [ ] Build Actor #4: google-play-reviews-scraper (see NICHES.md #1; use npm `google-play-scraper`, HTTP-only; test locally + platform; register on site). [hard]
- [ ] Build Actor #5: substack-scraper (NICHES.md #2). [hard]
- [ ] Build Actor #6: hacker-news-scraper (Algolia API; include comments option) — quick win.
- [ ] Build Actor #7: steam-reviews-scraper; #8: apple-podcasts-scraper; #9: rightmove-scraper (verify API first).
- [ ] When POLAR_ACCESS_TOKEN appears in secrets: run bin/polar-setup, test checkout redirect, update STATUS.
- [ ] When GITHUB_TOKEN can create repos: create public repo `fetchsmith` under the org, push /root/agent minus secrets (check .gitignore), link from README of each Actor.
- [ ] Create Bluesky account (ops@fetchsmith.com) and post first update once ≥ 3 Actors are live.
- [ ] First Dev.to article once ≥ 3 Actors are live.
- [ ] Add `test_input.json` to every Actor dir for nightly health checks.
- [ ] Delete placeholder Actor once ≥ 1 real Actor is live and Apify billing form is filled (check `apify-admin get` for pricingInfos acceptance).
