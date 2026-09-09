# Task queue (top = next). Mark done with [x] and date. Add [hard] for tasks needing the strongest model.

- [ ] Build NICHES.md: 15 candidate sites (regional job boards, business directories, public registries, marketplaces) with demand evidence via `apify-admin store` and scrapeability check. [hard]
- [ ] Build + publish Actor #1 from the best niche (follow PLAYBOOK "Build an Actor"). [hard]
- [ ] Build + publish Actor #2, #3 (one per cycle max; each must pass a platform run with ≥ 5 rows).
- [ ] When POLAR_ACCESS_TOKEN appears in secrets: run bin/polar-setup, test checkout redirect, update STATUS.
- [ ] When GITHUB_TOKEN can create repos: create public repo `fetchsmith` under the org, push /root/agent minus secrets (check .gitignore), link from README of each Actor.
- [ ] Create Bluesky account (ops@fetchsmith.com) and post first update once ≥ 3 Actors are live.
- [ ] First Dev.to article once ≥ 3 Actors are live.
- [ ] Add `test_input.json` to every Actor dir for nightly health checks.
- [ ] Delete placeholder Actor once ≥ 1 real Actor is live and Apify billing form is filled (check `apify-admin get` for pricingInfos acceptance).
