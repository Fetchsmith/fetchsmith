- 2026-09-09 Apify input schema validation: EVERY property needs a 'description' (build fails otherwise). Add .actorignore (node_modules, storage, test_input.json, meta.json).
- 2026-09-09 Local git repo had no user.name/email configured -> `git commit` failed with "Author identity unknown" even though prior commits existed (made via a session that had it set some other way). Fixed with `git config user.name/user.email` (local, not --global) using the same identity as prior commits: fetchsmith <agent@fetchsmith.com>. Check this early in a cycle if a commit unexpectedly fails.
- 2026-09-09 HN Store search shows several competitors already at 100-135 users for "hacker news scraper" — market isn't empty, but Algolia's official search API makes it a trivial, maintenance-free build, so still worth it as a portfolio-filler; differentiate via combined stories+comments+Who's-Hiring tag/date filters in one Actor rather than separate niche Actors.
- 2026-09-09 Store publishing REQUIRES an output schema (.actor/output_schema.json referenced via actor.json "output") — run bin/gen-output-schema <dir> after the local test, before push. Also owner must accept Store terms once (error store-terms-not-accepted).
- 2026-09-09 (cycle 3) All 5 built Actors flipped to isPublic:true with pricingInfos set between cycle 2 and 3 — owner finished Apify billing/payout setup. Confirm with `apify-admin get <slug>` (check both isPublic and pricingInfos, not just isPublic) before assuming monetization is fully live.
- 2026-09-09 (cycle 3) Dev.to publishing: use /root/agent/venv/bin/python (has httpx); system python3 does not have httpx installed. POST https://dev.to/api/articles with header api-key=$DEVTO_API_KEY, body {article:{title, body_markdown, published:true, tags:[...]}}. Returns 201 with the live URL in one call — no draft/publish two-step needed.

## 2026-09-09 (cycle 4)
- **Apify caps Actor publications at 5 per rolling 24 h** (`429 daily-publication-limit-exceeded`). We hit it publishing substack-scraper because all 5 earlier Actors were published in cycle 3. Building is unlimited; only the publish step is capped. Plan: build ≤5/day AND stagger `apify-admin publish` across days, or queue the publish for the next cycle after the window resets.
- `meta.json` `categories` accepts **max 3 values** (`400 schema-validation`). Four categories is rejected outright.
- Substack public JSON API (works from a datacenter IP, no proxy, no login):
  - `<origin>/api/v1/archive?sort=new&offset=&limit=` — post list, **`body_html` is empty here**; article text needs a second call.
  - `<origin>/api/v1/posts/<slug>` — full post incl. `body_html`, `wordcount`. Paywalled posts return metadata with no public body.
  - `<origin>/api/v1/post/<id>/comments?token=&all_comments=true&sort=best_first` — nested comment tree under `.comments`, children in `.children`, parent chain in `ancestor_path`.
  - In-publication search is `sort=new&search=<q>`; `sort=search` is rejected (`Invalid value`). The global `substack.com/api/v1/post/search` returned empty results — don't rely on it.
  - `<handle>.substack.com` 301s to custom domains, so `followRedirect: true` is required; pass the handle or the custom domain, both work.
- Most Substack competitors (15 Actors, leader 418 users, no dominant player) return archive metadata only. Full cleaned `bodyText` + comments + in-publication search is our differentiator at $0.002/result vs the usual $0.005.

## Cycle 5 (2026-09-09)
- **Apify API gotcha**: `GET /v2/acts?my=true` (list endpoint) does NOT return `isPublic`, `stats.totalUsers`, etc. — only a slim shape (id, name, title, stats.totalRuns/lastRunStartedAt). Only `GET /v2/acts/{id}` (single-actor endpoint) returns the full object. Any script that needs isPublic/totalUsers must fetch each actor individually (fine at our scale, <10 actors). `bin/revenue` had this bug since cycle 1 — it always reported 0 public actors and 0 users, meaning the "first users" owner-notify could never have fired. Fixed in commit ccc472e.
- Apify `totalUsers` on our own Actors counts our own CLI/console test runs too (each of our 5 public Actors shows exactly `totalUsers: 2` — almost certainly one console run + one CLI run by us, not organic). Don't treat totalUsers > 0 as a revenue/growth signal until it exceeds the self-testing baseline recorded in `state/revenue_history.json`.
- `apify push --force` (rebuild/redeploy code) is a distinct action from `apify-admin publish` (PUT isPublic:true) — pushing new builds to an already-public Actor does NOT count against the "5 Actor publications per 24h" cap, so README/code updates can still ship even while that daily cap is blocking a *new* Actor's first publish.
- 2026-09-09 (cycle 6) Bluesky signup (bsky.social) requires phone verification (`describeServer` -> `phoneVerificationRequired: true`) even though `inviteCodeRequired: false`. We have no phone number to receive an SMS, so automated account creation is blocked, not just "needs an API call" as PLAYBOOK assumed. Don't retry this without a real phone number; not worth an owner email (not critical, low priority per rule 3). Removed from active queue; revisit only if a phone-verification workaround (e.g. a paid SMS-receiving service with a budget line) is ever approved.
- 2026-09-09 (cycle 6) Competitor gap-check via public Apify Store API (`GET /v2/acts/{owner}~{name}`) is a good zero-auth way to read a rival's title/description/readmeSummary/exampleRunInput/pricingInfos/stats — no login needed, all public marketplace data. Used it against trovevault/shopify-products-scraper (585 users) and found real gaps: they charge a $0.10 flat "Actor Start" event PLUS $0.005/product (we only charge $0.001/product, no start fee — already a differentiator, now documented in our README), and their output includes `currency`, sale-detection, and image alt text that ours lacked. Added all three (cheap: one extra `/meta.json` request per store for currency, rest was free from Shopify's existing product JSON).

## 2026-09-09 (cycle 7) — Apple customer-reviews RSS endpoint went empty mid-cycle
`https://itunes.apple.com/<cc>/rss/customerreviews/id=<id>/sortBy=.../page=N/json` returned a
well-formed feed with **no `entry` field at all** (not an error, not a 4xx) for every app/country
tried (Notion 1232780281, Spotify 324684580; us + gb), reproduced from three different sources:
our Linode box directly (curl), Apify's cloud infra (`apify call`), and app-store-reviews-scraper's
own code. A run of the SAME actor against the SAME app at 2026-09-09T03:30 UTC (2h earlier) had
returned real reviews fine — so this is an Apple-side change/outage of an undocumented endpoint,
not a bug in our code, our IP, or the filter changes made this cycle. No official alternative
free/public endpoint exists (the `itunes.apple.com/lookup` app-metadata API is unaffected and
still works). Action: don't chase this with a code fix — it's very likely transient (this endpoint
has no SLA and is known to be flaky). **Next cycle: retest the exact curl above; if entries are
back, no action needed. If still empty after ~24h, this becomes a real product risk** (the Actor
silently returns 0 reviews instead of erroring) — worth adding a "zero reviews across all pages
despite non-zero ratingCount" warning/soft-fail so buyers get a clear signal instead of an empty
but "SUCCEEDED" dataset.

## 2026-09-09 (cycle 8) — Apple review RSS "outage" was misdiagnosed; it is per-request shard flakiness
Cycle 7 concluded Apple's `itunes.apple.com/<cc>/rss/customerreviews/...` endpoint was globally down (zero `entry` items everywhere). That was wrong, and the retest command in queue.md (plain `curl`) is what produced the false signal.
What is actually happening, measured this cycle:
- The SAME url returns 50 entries or an empty feed depending on the request's header fingerprint, and which fingerprint works differs **per app** and **per source IP**. Example from this box: Spotify(324684580)/us was empty under plain curl but full under a browser UA; Notion(1232780281)/us was the exact opposite; from Apify's cloud the pattern inverted again.
- It is *not* random-per-request: 15 sequential identical curls to the same url were all empty. So blind retries of the same request do nothing — you must vary the fingerprint.
- Coverage also genuinely differs per storefront (an app can have reviews in `gb` and none in `us`).
**Rule: never diagnose this endpoint with a single plain-curl request.** Test at least: default gotScraping, a `curl/8.5.0` UA, and a couple of `headerGeneratorOptions` variants, across 2+ storefronts.
Fix shipped in app-store-reviews-scraper (build 0.1.12): `fetchEntries()` retries an empty feed across 4 header fingerprints and remembers the one that worked (`preferredVariant`, so the steady state is still 1 request/page); an empty storefront then probes 4 others and logs which ones have reviews; opt-in `countryFallback` scrapes from a working storefront, tagging rows `requestedCountry`/`fallbackUsed`; `Actor.setStatusMessage` now explains an empty run (Apple's feed vs the user's own filters). Platform run went from 5/15 to 15/15 reviews on the same input. This is a genuine differentiator — competitors return an empty dataset with a green SUCCEEDED run.
General lesson for other Actors: a "SUCCEEDED with 0 rows" run is a buyer-facing failure. Distinguish "source had nothing" from "your filters removed everything" in both logs and the run status message.
