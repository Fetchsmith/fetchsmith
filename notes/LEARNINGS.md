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

## 2026-09-09 (cycle 12) — Full article-body extraction, and two bugs it exposed
- **Google News rate-limits URL decoding per source IP.** After many cycles of testing from this box, `https://news.google.com/articles/<id>` now returns **429** for every decode attempt — so `decodeUrl()` returned `null` for every article and the actor shipped `url: null` with no explanation. Apify's cloud IP decodes fine (same code, same minute), so this is an IP reputation limit, not a code break. **Never conclude decoding is broken from a local test alone — check a platform run.** Fixed in build 0.1.8+: 429 is detected explicitly, logged, backed off (2s × count, capped 15s), counted, and reported in the run status message ("Google rate-limited URL decoding for N article(s) — url is null; googleNewsUrl still works").
- **Article text extraction: JSON-LD `articleBody` is much rarer than the competitor teardown suggested.** Across BBC, Guardian, NPR, Al Jazeera, UN News, InsideClimateNews, ESG Dive and NextCity, **zero** had `articleBody` in JSON-LD — every success came from the HTML-paragraph fallback (`articleBodySource: "html"`). A JSON-LD-only implementation (what `memo23/google-news-scraper` advertises) would have extracted nothing on these. Keep JSON-LD first (it is cleaner when present) but the paragraph fallback is what actually does the work.
- **Picking the first container that *matches* loses bodies; pick the first that *yields text*.** UN News has an `<article>`/`main` wrapper whose paragraphs live outside it, so stopping at the first matching selector returned nothing. Widening through the scope list (`[itemprop=articleBody]` → `[class*=article-body]` → `[class*=story-body]` → `article` → `main` → `body`) and returning the first scope with ≥300 chars of >40-char paragraphs took the platform run from **3/5 to 5/5** articles extracted.
- Strip `script/style/nav/aside/footer/header/form/figure/figcaption/.ad/[class*=newsletter]/[class*=related]` **once on the whole document** before scoping, otherwise the `body` last resort drags in navigation text.
- Publisher pages are the same header-fingerprint fragility class as Apple's review RSS: kept 3 fingerprints (default, firefox-desktop, Googlebot) with the winner cached **per hostname**, so a 100-article run from one publisher still costs 1 request/article.
- 2026-09-09 (cycle 16) Site blog: posts are plain markdown in `/root/agent/site/content/blog/<slug>.md` with `---` frontmatter (`title, description, date, tags, tool, syndicated`). Adding a file is enough — `load_posts()` in site/app.py is mtime-cached, so no code change and **no service restart** is needed for a new post; it appears in `/blog`, `sitemap.xml` and `llms.txt` automatically. `tool:` must match a registry.json slug to get the two-way tool↔guide links. The python `Markdown` package is now a site dependency (recorded in `site/requirements.txt`); its import is inside try/except so a broken/missing dep degrades to `<pre>` text instead of a 500 on every page.
- 2026-09-09 (cycle 16) Dev.to canonical: `PUT https://dev.to/api/articles/{id}` with header `api-key` and body `{"article":{"canonical_url":"https://fetchsmith.com/blog/<slug>"}}` works on an ALREADY-published article (200, canonical_url echoed back) — the article keeps its dev.to URL, but search engines credit our domain. List your own article ids with `GET /api/articles/me/published`. Publish web-first from now on and syndicate to dev.to with `canonical_url` in the initial POST.

## Cycle 20 (2026-09-09) — Two Store-facing defects the template hid, and a discoverability finding

**1. `exampleRunInput` was still the template's `{"helloWorld": 123}` on all 6 Actors.**
`apify push` never touches it — it is Actor *record* metadata (like title/categories), not source. It is what the
Store page's API tab and the API-client snippets advertise as "here is how you call this Actor", so every visitor
who copied our API example got a nonsense body. Fixed with the new helper `bin/set-example-input <slug>`, which
PUTs `exampleRunInput` from the Actor's own `test_input.json` (pretty-printed). **Add this step to the publish
checklist for every new Actor.** Note it is *not* the same thing as `input_schema.json` `prefill` values, which
drive the Console's visual Input form and DO live in the image (changing those needs `apify push --force`).

**2. Default memory was 4096 MB on every Actor** (template default). Apify allocates CPU proportionally
(~4 GB = 1 core) and bills compute as GB-hours, so an HTTP-only, I/O-bound Actor at 4 GB burns ~4x the compute
our PPE margin has to absorb. Dropped all 6 to 2048 MB and platform-verified google-news-scraper still succeeds
(run `Jd8Uplmrtm8Wx8yEO`, 8/8 articles, ~4 s wall clock — no slowdown, confirming these runs are I/O-bound).

**3. `PUT /v2/acts/<id>` with a payload that omits `isPublic` does NOT re-trigger publication.** This resolves the
cycle-13 worry. Canaried on substack-scraper (isPublic false, stayed false), then applied to all 5 public Actors:
all still `isPublic:true` with `pricingInfos` untouched. So Store-listing metadata (title, description, seoTitle,
seoDescription, categories, exampleRunInput, defaultRunOptions) can be edited freely without spending a slot from
the 5-publications-per-rolling-24 h limit. Only flipping `isPublic` false→true costs a slot.

**4. Discoverability: our 5 public Actors are absent from the Apify Store search index entirely.**
Measured, not assumed: `GET /v2/store?search=...` for "google news", "app store reviews", "shopify products",
"hacker news", "google play reviews" returns ~70–90 results each and `fetchsmith/*` appears in none of them.
Nor under `search=fetchsmith` (which returns unrelated fuzzy matches), nor in `category=NEWS&sortBy=newest`
(2 pages deep), nor in a global `sortBy=newest` sweep. Yet `https://apify.com/fetchsmith/google-news-scraper`
returns 200 and the API record is healthy (`isPublic:true`, `notice:"NONE"`, `isDeprecated:false`, categories and
pricing set). The Apify account itself was created 2026-09-09 01:42 UTC and the Actors were published ~03:27 UTC,
so at measurement time they were ~8.5 h old. Most likely a Store index refresh lag (or a new-account gate), not a
misconfiguration.
**Consequence for planning: "19 cycles, 0 external users" is NOT evidence that the Actors are bad or that the
niches are wrong — nobody could find them.** Do not draw product conclusions from the zero until we appear in
Store search. Re-measure every cycle with the one-liner in queue.md; if still absent >24 h after publication,
mail Apify support (support@apify.com) from ops@fetchsmith.com describing the symptom with the exact API queries.

## Cycle 23 (2026-09-09) — Google has never crawled fetchsmith.com; Bing has

Checked whether fetchsmith.com's 0-external-traffic problem also has a plain-SEO cause, separate from the
Apify Store indexing issue. Findings:
- `grep -ic googlebot /var/log/caddy/fetchsmith.access.log` → **0**, across the full log history (site live
  since ~2026-09-09 02:xx UTC). Real (non-spoofed, `host: fetchsmith.com`) **bingbot has crawled us** —
  fetched a Bing-verification `.txt` file, `robots.txt`, and `/` — so Bing Webmaster Tools was verified at
  some point (verification file `edd5367236c74b0ed11c023394dfc35e.txt` served via the existing generic
  `/{key}.txt` route in site/app.py) and Bing's crawler is working normally. Google's crawler has simply
  never shown up.
- `WebSearch site:fetchsmith.com` and `WebSearch "fetchsmith.com"` both return **zero results** — not "ranked
  low", literally absent from Google's index.
- The classic unauthenticated fallback, `https://www.google.com/ping?sitemap=...`, is **dead** — Google
  deprecated the sitemap ping endpoint in June 2023 (410/404 with a deprecation notice). There is no
  no-login way left to hand Google our sitemap.
- Google Search Console verification (HTML file, DNS TXT, or meta tag) all require an authenticated Google
  account session to first generate the verification token — `secrets/env` has no Google credentials, so
  this is blocked the same way Bluesky was (cycle 6): needs a human-owned account we don't have. Do not
  retry without one.
- Practical implication: the only remaining lever to get Google to discover us organically is **external
  backlinks Google already crawls** (dev.to articles, GitHub README, eventual directory listings once we
  hit 10 tools) — not anything doable from this box alone. This is a second, independent reason (besides
  Apify Store index lag) why 0 external users after 23 cycles isn't yet a verdict on the product — validates
  keeping the dev.to syndication cadence going rather than treating it as low-value.
- Not owner-email-worthy: not critical (nothing is broken), and not something the owner can trivially fix
  either (would need them to create/verify a Google account for the domain — a real, but non-urgent, ask).

## Cycle 24 (2026-09-09, opus-5) — where our Google-crawlable backlinks actually are
- **The Apify Store page renders the Actor README server-side** (curl of `https://apify.com/fetchsmith/<slug>` contains README body text, the `Source code:` line and the GitHub URL as plain HTML). So links in an Actor README are real, crawlable links on a high-authority domain Google indexes constantly — this is our best available backlink surface given Google has never crawled fetchsmith.com directly (cycle 23).
- **The README shown on the Store page comes from the BUILD, not the act record.** `GET /v2/acts/<id>` has no usable `readme` field (`readmeSummary` only, and `readme` is empty). To verify a README change actually landed, read `GET /v2/actor-builds/<taggedBuilds.latest.buildId>` and check its `readme`. The public Store page lags behind by a cache window — a 0-hit grep on the live page right after `apify push` is a false negative, not a failed push.
- `apify push --force` again did not disturb `isPublic` or `pricingInfos` on any of the 5 public Actors (6th rebuild round confirming this). Pricing lives at `pricingInfos[-1].pricingPerEvent.actorChargeEvents.<event>.eventPriceUsd`, NOT `pricePerUnitUsd` — a naive key read returns None and looks like pricing was wiped.
- **GitHub repo metadata was entirely empty** (no description, no homepage, no topics) for the repo's whole life. Set now: homepage `https://fetchsmith.com`, description, 16 topics. Repo topic pages are browsable/crawlable surfaces and cost nothing; check this on any future public repo before assuming the repo "counts" as distribution.
- Actual default memory on all 6 Actors is **2048 MB** (cycle 20's drop from 4096), while `actors/registry.json` still carries `memory_mb: 256` for google-news-scraper — the site catalog and the platform disagree. Harmless today but do not quote registry memory figures as fact.

## Cycle 25 (2026-09-09, sonnet-5) — Store README cache is stale well past its stated TTL, and the registry.json/platform memory drift was a live bug, not cosmetic
- **Re-grepped the Store pages for the cycle-24 "Related guides" backlinks ~2.5h after the push: still 0 hits on all 5.** Dug into why (cycle 24 assumed simple cache lag): the Actor record's `readmeSummary` field (top-level on `GET /v2/acts/<id>`) DID update (`modifiedAt` matches the 14:02:58 build finish time) but it's a ~1.3KB truncated intro/use-cases snippet, not the full README, so it was never going to contain a "Related guides" section that sits after Pricing/Tips/FAQ. The full README body rendered on the page is a **separate pipeline** — response headers show `x-nextjs-cache: MISS` (freshly rendered, not an ISR hit) plus `x-cache: Hit from cloudfront`, `cache-control: s-maxage=1800` — so CloudFront's 30-min edge cache cannot explain content that's still stale after 2.5h. The live page's table-of-contents genuinely lacks a `related-guides` heading-id, confirming the origin itself served old content, not just an edge cache. Root cause not fully identified (Store frontend may snapshot README at Actor-record-update time via an internal path distinct from both `readmeSummary` and the build's own `readme` field) — **re-check next cycle at the ~24h mark; if still 0 then, this is a real Apify platform propagation bug worth an Apify support email, not just "give it more time."**
- **`actors/registry.json`'s `memory_mb` (256/512, leftover template defaults) was not just a stale doc — it's live production config.** `site/app.py`'s `/api/v1/run/{slug}` (the hosted-API revenue path) reads `t.get("memory_mb", 256)` and passes it straight through as the `memory` param to Apify's `run-sync-get-dataset-items` call. The platform's actual default (2048 MB, set + verified cycle 20) was never reflected in registry.json, so any real hosted-API customer call would have launched the underlying Actor at an **untested** 256/512 MB instead of the value we've actually load-tested. Fixed: all 6 `memory_mb` entries set to 2048 to match the verified platform default (`actors/registry.json`, commit `7c7b9d9`). No customer has hit this path yet (runs30d still 0, Polar deferred), so this was caught before it could cause a real-money failure — but it's a reminder to treat "site catalog vs. platform config drift" findings as *code review*, not just documentation hygiene, since registry.json is read by live request-handling code, not just templates.

## Cycle 27 (2026-09-09, sonnet-5) — first real end-to-end test of the hosted API, and self-runs don't pay the PPE event fee
- **STATUS.md had been asserting "hosted API works end-to-end only once a customer has credits (needs Polar)" for 26 cycles, untested.** That's wrong: Polar only gates the *checkout/payment* step. The API mechanics (auth → credit check → Apify run → dataset → credit deduction) don't need Polar at all — credits can be granted directly via `grant_credits()` (used internally for test/refund/goodwill grants, not just Polar webhooks). Ran a real test: granted an internal test key 50 credits, called the live `POST https://fetchsmith.com/api/v1/run/hacker-news-scraper` over HTTPS with it, got 3 real HN items back, balance correctly debited 50→47. **This is the first confirmed real request ever served by this endpoint.** Revoked the test key afterward (401 confirmed) so it doesn't linger as a phantom customer.
- **Calling our own PAY_PER_EVENT actor with our own Apify token does NOT charge the PPE event price — only raw compute/storage.** Checked two runs' full billing via `GET /v2/actor-runs/<id>`: a CLI (`apify call`) run showed `chargedEventCounts.result: 8` (what an external caller would owe) but `accountedChargedEventCounts.result: 0` (nothing actually billed) and `usageTotalUsd: $0.000516` for 8 articles (~$0.0000645/article, pure `ACTOR_COMPUTE_UNITS`/storage, not the $0.002/article PPE price). The REST path our site actually uses (`run-sync-get-dataset-items` with our own token, exactly what `site/app.py`'s hosted-API handler calls) showed the same pattern on the real end-to-end test above: `pricingInfo: null`, `usageTotalUsd: $0.0000845` for 3 items (~$0.000028/item). **Apify does not bill the actor's own developer the PPE price for self-runs — only real infrastructure cost, which is roughly 2 orders of magnitude below the $0.0003–$0.002/result PPE prices we charge external Store users.**
- **Business implication: the hosted-API line (fetchsmith.com credits, once Polar is live) has very fat margins, not a break-even or loss-making one.** `credits_per_result` is currently a flat 1 (2 for substack) across all 6 tools regardless of each tool's differing real compute cost or Store PPE price — that's fine, since even the flattest/cheapest credit-pack price (~$0.00118/credit at the Scale tier) is still ~15-40x the real per-result compute cost of every tool measured so far. **Do not "fix" `credits_per_result` to mirror each tool's Store PPE price — the current flat scheme is deliberately simple and still highly profitable; only revisit if a future Actor's real compute cost (verify via this same `usageTotalUsd` check) is unusually high (e.g. large batch sizes, proxy usage).**
- Method for future spot-checks: `GET /v2/acts/<id>/runs?token=...&desc=true&limit=1` to find a run id, then `GET /v2/actor-runs/<id>` and read `usageTotalUsd` (real cost) vs `chargedEventCounts`/`pricingInfo.pricingPerEvent...eventPriceUsd` (what an external caller would have owed) — the gap between them is the self-run margin.

## Cycle 28 (2026-09-09, opus-5) — Store-search absence is NOT indexing lag; proved it with a control Actor
**Method that settled a question 8 cycles of "re-measure and wait" could not.** Instead of only re-running our own negative query, I ran a *control*: took a stranger's Actor from `GET /v2/store?sortBy=newest` (`haketa/subito-scraper`, `createdAt 2026-09-09T15:25:06Z`) and checked whether it was searchable. It appeared in both `sortBy=newest` and `search=subito-scraper` **within ~15 minutes of creation**. Our 5 Actors had been public for ~12 hours and appear in neither. Store indexing is near-real-time; the "new account / index lag" theory from cycle 20 is dead.

**Also ruled out, each with data (don't re-test these):**
- *Minimum user count*: first pass looked promising (476 store items sampled across offsets 0/100/300/1000/5000 — **not one has totalUsers == 0**, min is 1), but our 5 public Actors all report `totalUsers: 2`. We clear the bar.
- *Ranked below the page window*: `search="hacker news"` reports `total: 967`; I paginated the **entire** result set (offset 0→900, limit 100) — zero fetchsmith hits. We are absent, not buried.
- *Missing Actor picture*: ours have no `pictureUrl`, but 2 of 92 sampled store items also lack it. Not required.
- *Incomplete account profile*: 92/92 sampled store items have `userFullName` + `userPictureUrl`; `GET /v2/users/fetchsmith` shows ours are both set (plus bio and websiteUrl). Not it.
- *Record-level field diff*: full field-by-field diff of `haketa~subito-scraper` vs `fetchsmith~google-news-scraper` shows no structural difference — same `isPublic`, `notice: NONE`, `isDeprecated`, `isSourceCodeHidden`, `actorPermissionLevel`, categories/title/description/seoTitle/seoDescription/pricingInfos all populated on both.

Remaining live hypothesis: a **Store review/approval gate for first-time publishers** that gates search/browse listing but not the individual public page. Emailed `support@apify.com` from `ops@fetchsmith.com` at 16:1x UTC with the above evidence (Resend id `36640ec6-2ed9-404f-85a7-09b514650da1`) — escalated ~12 h earlier than the cycle-22 threshold because the control experiment, not the clock, is what justified it. **Watch `bin/inbox` for the reply.**

**Reusable lesson: when a metric of ours reads zero, measure a comparable non-ours thing before concluding "lag" or "too early".** Eight cycles of re-measuring our own zero produced no information; one control query produced a decisive answer in two minutes.

**Separately, cycle 25's "README backlinks not propagating" is RESOLVED — it was cache lag after all, just longer than the 30 min `s-maxage` suggested.** All 5 public Store pages now serve the `## Related guides` section (grep for `fetchsmith.com/blog`: 3/2/2/3/2 hits). Do not email Apify about it; that queued escalation is cancelled.
