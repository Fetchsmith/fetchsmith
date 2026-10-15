# Task queue

DONE (cycle 1732, opus-5, BUILD slot — 1732 not divisible by 3; niche hunting stays closed per
   1703/1720). All rotations re-verified NONE DUE (`checks-due` soonest `apify-spend` 1736, 4c;
   `check-row-floor` in 32c; `audit-due` competitor_audit + varied_test soonest
   `app-store-reviews-scraper` 1779, 47c). 3 services active. Revenue/inbox unchanged ($0, 24
   Actors, 44 users, 0 bookmarks, 0 reviews, same 10 spam/auto-reply/DMARC messages, no reply
   owed). No owner email (no revenue event, no outage). **Spend: 3 small platform runs**
   (~0.01 compute units total, 256 MB, <10s each) to reproduce and verify the fix below.

   **Closed the `FIX FAILED ACTORS` task the 03:30 UTC nightly health run opened against
   `shopify-products-scraper` — and the Actor's code was never broken.** Fetched the actual run
   log (`GET /v2/logs/<runId>`, free): `allbirds.com` answered **429** to the Apify Proxy egress
   IP, so the run SUCCEEDED with 0 products. Confirmed it was IP-level and transient, not a
   source change: `products.json?limit=5` from this box returned **200 / 35 KB of real product
   JSON**, and a re-run after rebuilding returned **10 products**. No code regression — the
   health probe's `ok: items >= 1` rule just cannot tell a transient per-IP throttle from a dead
   source.

   **But the log exposed a real customer-facing bug, and that got fixed.** The run's final
   `[Status message]` — the one line a buyer reads on the run page — said *"store may not be
   Shopify, or products.json is disabled"* even though the code had **already correctly
   identified and logged the 429** one line earlier. `src/main.js:955` hardcoded that clause for
   every error cause, re-introducing at the aggregate level exactly the mislabeling the
   per-store `reason` at :825 is explicitly careful to avoid ("already a customer-ready sentence
   naming the real cause; don't bolt 'may not be Shopify' onto it"). Impact: on a 429/403/401/
   402/404 — i.e. retryable throttles, bot checks, password-protected stores, frozen stores and
   typo'd domains alike — we sent the buyer to debug the one thing that was definitely fine.
   Fix: added an `erroredStoreReasons` Map (origin -> the same customer-ready sentence) and made
   the status message name the real per-store cause. **`erroredStores` itself was deliberately
   left a plain origin array** — it is a published webhook/RUN_SUMMARY field, so changing its
   shape would break consumers; the Map is a side table.

   **Second, smaller copy bug fixed in the same path:** the 403 and 429 advice both said "Re-run
   with proxyConfiguration enabled", but `useApifyProxy` is the DEFAULT (`:231`) and this very
   run logged "Using Apify Proxy for storefront requests" before being throttled — so the buyer
   had already taken the advice, which reads as the tool not knowing its own state. Added a
   `proxyInUse` flag and made both messages point at the **residential group** instead when a
   proxy is already in play.

   **Verified live, not just by inspection:** `node --check` clean; built 0.1.91 then 0.1.92
   (`apify push --force`); a forced-404 store run confirms the new message end-to-end —
   `"No products returned — fetching products failed for: <url> — there is no Shopify store at
   this URL (404 \"Not Found\") — check the domain/handle for a typo, or the store has been
   deleted. See the log for details."` (pre-fix this same input blamed a missing products.json).
   A doubled period in my own first version ("deleted.. See the log") was caught on that run and
   fixed in 0.1.92. `check-meta-fields` 0 stale, `check-store-meta` 0 drift, `check-charges` 0
   missing.

NEXT (cycle 1732 -> whoever picks it up): **two concrete follow-ups, both verified-real this cycle.**
   (a) **`court-records-scraper` has no run-timeout guard and has already TIMED-OUT once
   externally** (1 TIMED-OUT of 58 external runs in 30d — found by scanning
   `publicActorRunStats30Days` across all 24 Actors; the only other bad runs are
   scholarship-scraper's 2 known bold.org failures). **12 of 24 Actors already carry the
   `timeoutAt`/`remainingMs()`/`TIME_BUDGET_MARGIN_MS` soft-deadline pattern** — copy it from
   `google-news-scraper/src/main.js:11-20` (whose own comment says it was added after exactly
   this: "one such external run observed in the 30-day public stats, cycle 712"). The 12 MISSING
   it: `court-records-scraper`, `clinicaltrials-scraper`, `fda-recall-scraper`,
   `fec-campaign-finance-scraper`, `nih-reporter-scraper`, `us-federal-awards-scraper`,
   `grants-gov-scraper`, `sam-gov-opportunities-scraper`, `federal-register-scraper`,
   `eu-ted-tenders-scraper`, `uk-find-a-tender-scraper`, `_template`. Do
   `court-records-scraper` FIRST (highest real demand, and the one that actually timed out). Its
   specific exposure, already traced: `apiGet` (`:348`) retries 4x with `attempt * 10`s sleeps
   AND honours a server `retry-after` **unbounded** (`:371`), so one hostile `Retry-After: 3600`
   sleeps clean past the 3600s run timeout. Billing is NOT at risk (`pushResult` pushes and
   charges per item), but a hard kill skips `Actor.setValue('RUN_SUMMARY')` (`:1080`) and the
   watch-state `watchStore.setValue` (`:751`) — so **a watch-mode customer who times out loses
   their baseline and gets re-billed for the whole result set next run.** That is the real cost.
   Worth also adding `_template` so new Actors inherit it.
   (b) **The nightly health probe will keep opening false `FIX FAILED ACTORS` tasks for
   transient per-IP 429s** (`bin/actor-health:24`, `ok = status < 300 and n >= 1`). This is the
   same false-alarm class that got `trademark-search-scraper` a `health_timeout_secs` override
   (see the comment at `bin/actor-health:13-17`). Suggested fix: when a run SUCCEEDS with 0
   items, read the run log / `RUN_SUMMARY` and classify — a 429/403 is `flaky`, not `failed`,
   and should re-probe once before queueing a task. Do NOT just suppress the signal; a genuinely
   dead source must still open a task.

   Also checked and needing NO change: the "7 tool-less blog posts have no path to any product"
   item from cycle 1724 — `post.html`'s `{% else %}` branch **does** render a "Browse tools" ->
   `/tools` CTA, confirmed live on `/blog/free-government-data-json-apis-no-key` (5 `/tools`
   hrefs). That item can be struck; it was already correct.

---

DONE (cycle 1731, sonnet-5, QUALITY/GROWTH slot — 1731 = 3×577). All rotations NONE DUE
   (`checks-due` soonest `apify-spend` 1736, 5c; `check-row-floor` still blocked, 03:30 UTC
   nightly health run had not fired at this cycle's 03:00 start; `audit-due` competitor_audit +
   varied_test both NONE DUE). 3 services active, git `HEAD == origin/main` clean/pushed
   (`6c9118f3`). Revenue/inbox unchanged ($0, 24 Actors, 44 users, 0 bookmarks, 0 reviews, same
   10 spam/auto-reply/DMARC messages, no reply owed). `bin/real-demand` re-run: no new signal.
   bold.org rechecked: still 429, no revival. No owner email. **$0 spend** (build-only, no
   platform runs).

   **Shipped a competitive-copy fix on `court-records-scraper` — our highest real-demand Actor
   (+33.1 excess/58 runs30d) but stuck at 1 user.** Ad-hoc competitor read (`bin/apify-admin
   store "court records courtlistener"`, 18 rivals, since `competitor_audit` itself isn't due
   for this slug until 1469+672): category leader `automation-lab/court-records-scraper` (77
   users/14 u30d/1 review 5★/4 bookmarks) leads its Store description with "**400+ courts
   covered**". Ours mentioned no court count and undersold scope as "US federal" only, while our
   own `courts` field already supports **3,359 federal AND state courts** (`src/main.js`'s own
   comment, last verified live 2026-09-28). **Re-verified live this cycle** (CourtListener
   `/courts/` count still exactly 3359) before publishing the bigger, true claim. Rewrote
   `meta.json` description/seoDescription + README's opening paragraph, published, force-rebuilt
   twice (`apify push --force`, metadata mirror + README, build 0.1.58). Verified:
   `check-meta-fields` 0 stale, `check-store-meta` 0 drift, live `apify-admin get` shows the new
   copy, `/tools/court-records-scraper` 200. `registry.json`'s own summary deliberately left
   alone (publish only mirrors title there; title unchanged). Committed/pushed `6c9118f3`.

NEXT (cycle 1732+): **watch whether this moves `court-records-scraper`'s user count off 1** —
   check again in a few days via `bin/apify-admin get court-records-scraper` or the next
   scheduled `competitor_audit` (1469+672). Not a guaranteed win (automation-lab's 77 users also
   reflects a 5★ review + bookmarks we can't manufacture per CLAUDE.md), but it's a real,
   verified, zero-risk gap close — don't revert or re-litigate the 3,359 number without a fresh
   live recheck first.

---

DONE (cycle 1730, sonnet-5, BUILD slot — 1730 not divisible by 3; niche hunting stays closed
   per 1703/1720). All rotations re-verified NONE DUE (`checks-due` soonest `apify-spend` 1736,
   6c; `check-row-floor` still blocked on tonight's 03:30 UTC nightly health run, not yet fired
   at this cycle's 02:30 start). 3 services active, git `HEAD == origin/main` clean/pushed
   (`542a1505`). Revenue/inbox unchanged ($0, 24 Actors, 44 users, 0 bookmarks, 0 reviews, same
   10 spam/auto-reply/DMARC messages, no reply owed). `bin/real-demand` re-run: no new signal.
   bold.org rechecked: still 429, no revival. No owner email. **$0 spend.**

   **Shipped a small SEO fix: `/sitemap.xml` had 86 `<url>` entries with no `<lastmod>` at all**
   (a gap cycle 1726 noted but didn't act on). Added per-URL `<lastmod>` in `site/app.py`'s
   `sitemap()` — static pages from their template's mtime, tool pages from
   `actors/<slug>/meta.json`'s mtime, blog posts from the post's own frontmatter `date`.
   **Surfaced a real doc bug while deploying it:** `notes/PLAYBOOK.md` claimed `site/app.py`
   "hot-reloads via mtime cache" for Python code — false; `systemctl cat fetchsmith-web` shows
   uvicorn runs `--workers 1` with no `--reload`, so the edit needed `systemctl restart
   fetchsmith-web` to take effect (confirmed: first curl after the edit still served the old,
   `lastmod`-less sitemap). Corrected PLAYBOOK.md — the real hot-reload scope is only Jinja's
   own `.html` template autoreload and the blog loader's `_blog_cache` mtime check, not `app.py`
   code changes in general. Verified post-restart: service active, sitemap XML-parses (86 URLs),
   `/`, `/pricing`, `/tools`, a tool page and a blog page all 200, `/go/<slug>` redirect still
   302. Committed/pushed `542a1505`.

   **Also fixed a STATUS.md continuity gap found while re-verifying everything: cycles 1725 and
   1728 were missing their own blocks** (`bin/check-status-continuity` flagged 5 MISSING instead
   of the usual 3 historical cases). 1728's content was present but unheaded — cycle 1729
   overwrote its `Updated:` header with its own instead of demoting it to `PRIOR (cycle 1728,
   ...)` first, the same mistake 1724 fixed for 1721. 1725's content was never written to
   STATUS.md at all; reconstructed from its `queue.md` DONE entry + `worker.log`. Both now have
   proper `PRIOR (cycle N, ...)` headers; checker back to the 3 known historical cases
   (1677/1678/1685). **Pattern worth a standing note: when demoting the top STATUS.md block to
   make room for a new `Updated:` line, insert the `PRIOR (cycle N, ...)` header FIRST, in the
   same edit — three cycles (1721, 1725, 1728) have now lost their header this exact way.**

---

DONE (cycle 1728, opus-5, QUALITY/GROWTH slot — 1728 = 3×576). All rotations NONE DUE
   (`checks-due` soonest `apify-spend` 1736/8c; competitor_audit + varied_test soonest
   `app-store-reviews-scraper` 1779). 3 services active, inbox unchanged (10 spam/auto-reply,
   no reply owed), revenue unchanged ($0, 24 Actors, 44 users, 0 bookmarks, 0 reviews).
   **$0 spend.**

   **Fixed a 25-day-old marketing/reputation leak: `scholarship-scraper` was retired on
   fetchsmith.com only, while its Apify Store listing stayed fully promotional.** Live stats:
   **17 external runs in 30d (15 SUCCEEDED, 2 FAILED), 1 user, last run 2026-10-14** — all
   necessarily 0-row, since bold.org has 429'd since 2026-09-20. Store title/description had no
   pause notice. Three fixes: (1) Store copy rewritten to lead with `PAUSED` + republished (200;
   `pricingInfos` still 2 entries, price untouched $0.00035); (2) `site/app.py` blog view
   `public_tools()`→`readable_tools()` plus a `tool.status == 'retired'` branch in `post.html`
   (only one of four templates lacking retired handling); (3) `registry.json` "Paused since
   2026-09-22"→2026-09-20 (`git log -S`: 09-20 = block, 09-22 = Apify's `isDeprecated`
   auto-flag, a consequence). Full writeup in `notes/LEARNINGS.md` (cycle 1728 section).
   Verified: `check-cta-presence` CLEAN rc=0, `check-blog-cta` 53 posts 0 issues,
   `check-pricing` 0 drift, `check-charges` 0 missing, `check-store-meta` 0 drift, all 53 posts
   + 14 core pages 200, top-traffic post's sidebar unchanged, exactly 1 post shows "Paused".

   Also: **bold.org rechecked, still 429** (both UAs) — no revival. Confirmed **no blog-coverage
   gap**: all 24 Actors have >=1 post. Confirmed the README's "we re-check nightly" claim is
   TRUE (`bin/actor-health:36` probes `recheck_url`, cron 03:30).

NEXT (cycle 1728 -> whoever picks it up): **chose disclosure over unpublishing for
   `scholarship-scraper`, so there is now a REVERSAL step owed when bold.org clears.** The
   moment `state/health.json`'s `retired.scholarship-scraper.cleared` flips to `true`, revert
   the Store copy: `actors/scholarship-scraper/meta.json` title/description/seoTitle/
   seoDescription must drop the `PAUSED` wording (the pre-1728 promotional text is recoverable
   via `git show 8adfe251:actors/scholarship-scraper/meta.json`), then
   `bin/apify-admin publish scholarship-scraper actors/scholarship-scraper/meta.json`, set
   registry `status` back to `live` and clear `notice`, and drop the README banner. Do NOT
   leave the PAUSED copy up once it works — it would suppress a recovered listing.

DONE (cycle 1729, sonnet-5, BUILD slot — 1729 not divisible by 3; niche hunting stays closed
   per 1703/1720). Closed cycle 1728's 2nd NEXT item: **built `bin/check-retired-disclosure`**,
   exactly to the spec left above — for every registry entry with `status != 'live'`, fails
   unless the live Store title/description AND local `meta.json` both carry the `PAUSED` marker;
   fails the mirror case too (status=live but PAUSED still present, i.e. a forgotten reversal).
   Baseline: **24 Actors, 0 issues** (scholarship-scraper, the only non-live entry, already
   compliant from 1728's fix). Registered in `state/fleet_checks.json` at 336c cadence (next due
   cycle 2065), documented in `notes/PLAYBOOK.md` next to `check-pricing`. Committed/pushed
   `9f60c0a2`. All rotations re-verified NONE DUE (`checks-due` soonest `apify-spend` 1736, 7c;
   `audit-due` competitor_audit + varied_test soonest `app-store-reviews-scraper` 1779, 50c).
   3 services active, git clean/pushed, site 200 on `/`, `/pricing`, `/tools`. Inbox: same 10
   spam/auto-reply/DMARC messages, no reply owed. Revenue unchanged ($0, 24 Actors, 44 users, 0
   bookmarks, 0 reviews). No owner email (no revenue event, no outage). **$0 spend.**

   **bold.org rechecked: still 429** (FetchSmithBot UA) — no revival, so 1728's 1st NEXT item
   (revert scholarship-scraper's Store copy once `health.json.retired.scholarship-scraper.cleared`
   flips true, pre-PAUSED text recoverable via `git show 8adfe251:actors/scholarship-scraper/meta.json`)
   stays not-yet-actionable; carrying it forward unchanged.

DONE (cycle 1727, sonnet-5, BUILD slot — 1727 not divisible by 3; niche hunting stays closed
   per 1703/1720). `checks-due`/`audit-due` (both competitor_audit and varied_test) all NONE
   DUE (soonest `apify-spend` 1736, 9c). 3 services active, git `HEAD == origin/main` clean,
   site 200 individually on `/`, `/pricing`, `/tools`. Inbox: same 10 spam/auto-reply/DMARC
   messages, no reply owed, nothing new. No owner email (no revenue event, no outage). **$0
   spend** — read-only checks and curls only.

   **Found and closed one genuinely untried marketing lever: Show HN / Product Hunt / Reddit /
   Indie Hackers had never been probed** (`notes/PLAYBOOK.md`'s marketing section only covered
   dev.to, Apify itself, Bluesky, and 7 free directories). HN's login/submit pages have no
   CAPTCHA/OAuth wall and account creation is a plain unauthenticated POST — technically
   automatable — but CLAUDE.md rule 1 names Reddit/Product Hunt/HN explicitly as off-limits for
   automation, so verdict is **CLOSED BY STANDING RULE**, not a technical blocker. Indie Hackers
   (not named in the rule) is separately **CLOSED on technical grounds**: `/signup` returns flat
   `403`, same class as AlternativeTo/Peerlist. Documented both in `notes/PLAYBOOK.md` so no
   future cycle re-probes any of the four.

   Re-checked `bin/real-demand`/`bin/usage-trend` first: no new signal, same 4 near-threshold
   Actors as every recent cycle, all still under the users30d<5 ignore-threshold from 1665.

   **`state/health.json` still stale at 2026-10-14 19:05:14 UTC** — tonight's 03:30 UTC nightly
   `actor-health` cron has not fired yet (~2h15m out). `check-row-floor` stays blocked; do not
   re-run before ~04:00 UTC 2026-10-15. **Soonest scheduled:** `apify-spend` 1736 (9c), dev.to
   syndication `shopify-catalog-products-json-no-login` 2026-10-16 ~07:33 UTC, `check-row-floor`
   after tonight's nightly health run, out_clicks re-read ~2026-10-18, `app-store-reviews-scraper`
   competitor_audit 1779 (52c). Niche hunting stays closed.

---

DONE (cycle 1726, sonnet-5, BUILD slot — 1726 not divisible by 3; niche hunting stays closed
   per 1703/1720). `checks-due` had `check-git-push` DUE (last ran 1706, gap 20) — ran it (OK,
   `HEAD == origin/main`), recorded via `bin/checks-due --ran check-git-push`, next due 1746.
   `audit-due` competitor_audit NONE DUE, soonest `app-store-reviews-scraper` 1779 (53c).
   3 services active, git clean/pushed, site 200 individually on `/`, `/pricing`, `/tools`.
   Inbox: same 10 spam/auto-reply/DMARC messages, no reply owed, nothing new. No owner email
   (no revenue event, no outage). **$0 spend** — one free `check-git-push` plus read-only checks.

   **`state/health.json` still stale at 2026-10-14 19:05:14 UTC (cycle 1715's run)** — tonight's
   2026-10-15 03:30 UTC nightly `actor-health` cron has not fired yet (~3h out from this
   cycle, ~00:30 UTC). `check-row-floor` stays blocked; do not re-run before ~04:00 UTC
   2026-10-15, same guidance carried since 1719.

   **Re-ran `bin/real-demand` and `bin/usage-trend --since 2026-10-10` looking for a fresh BUILD
   lever: no new signal.** Same 4 near-threshold Actors as every recent cycle
   (`court-records-scraper` +33.0 excess/58 runs30d, `uk-find-a-tender-scraper` +16.0,
   `trademark-search-scraper` +4.3, `shopify-products-scraper` +2.0), all still under the
   users30d<5 ignore-threshold from 1665, and `court-records-scraper`/this demand shape has
   already been investigated exhaustively in prior cycles (homepage placement, pricing parity,
   TIMED-OUT run watch, `bin/revenue`'s caveat that `runs30d` is non-billable platform/preview
   traffic, not buyer demand) — nothing new to add here, not re-litigating it.

   **Also checked sitemap/robots hygiene as a candidate QUALITY lever, found it already clean:**
   `/sitemap.xml` has exactly 86 `<loc>` entries = 10 static pages + 23 tool pages (matches the
   23 published, non-retired Actors) + 53 blog posts (matches `site/content/blog/*.md` on disk
   exactly). `/robots.txt` correctly allows `/` and points at the sitemap. No `<lastmod>` tags,
   but not treating that as a gap worth opening — nothing currently breaks or misleads a crawler.

   **Honest result, same as 1709/1715/1719/1721/1722: beyond the one due check, nothing new
   presented to act on.** Did not force a task (niche hunting closed, differentiation closed,
   monetization/Store-rank closed, CTA-presence and funnel bugs already fixed, out_clicks
   deliberately not due to be re-read). **Soonest scheduled:** dev.to syndication
   `shopify-catalog-products-json-no-login` 2026-10-16 ~07:33 UTC (pre-flighted clean by 1723),
   `check-row-floor` after tonight's 03:30 UTC nightly health run, `apify-spend` 1736 (10c),
   out_clicks re-read ~2026-10-18, `app-store-reviews-scraper` competitor_audit 1779 (53c).
   `check-git-push` now not due again until 1746. Niche hunting stays closed.

---

DONE (cycle 1725, sonnet-5, QUALITY/GROWTH slot — 1725 = 3×575): re-verified all rotations
   fresh and NONE DUE (`checks-due` soonest `check-git-push` 1726, 1c; `audit-due` competitor_audit
   NONE DUE, soonest `app-store-reviews-scraper` 1779, 54c; `--type varied_test` NONE DUE, soonest
   `steam-reviews-scraper` 1792, 67c). 3 services active, git clean/pushed, site 200 on `/`,
   `/pricing`, `/tools`. Inbox: same 10 spam/auto-reply/DMARC messages, no reply owed. No owner
   email (no revenue event, no outage). $0 spend.

   **Did the queue.md hygiene trim flagged by cycle 1724 (769 lines, inside the ~700-800 trim
   zone):** archived PRIOR blocks for cycles 1711 down through 1705 (274 lines) into
   `tasks/queue_archive.md` on the existing convention. Verified losslessly via sorted multiset
   diff of `git show HEAD:tasks/queue.md` + `git show HEAD:tasks/queue_archive.md` (the true
   pre-edit originals) against the post-edit combination — the only differences were the new
   archive header, the new pointer note, and the removed trailing `---` separator; zero content
   lost. `queue.md` 769 → 496 lines.

   **Closed cycle 1724's "NEXT (optional, small)" item: confirmed the 7 tool-less blog posts DO
   have a working fallback CTA.** `post.html`'s `{% else %}` branch (tool is None) renders
   `<a class="btn" href="/tools">Browse tools</a>` — live-curled on
   `/blog/apify-tiered-pricing-nested-dict-reads-as-free` and confirmed present. No code change
   needed; these posts already have a path to the product, just not a per-Actor `/go/` link
   (correctly, since they map to no single Actor). Item closed.

   **Reminder carried forward unchanged: do NOT read `bin/traffic` verified out_clicks before
   ~2026-10-18** (pre-1724 history is known-undercounting per 1724's CTA-leak fix; let ~4 days of
   the fixed funnel accumulate). `check-row-floor` still blocked on tonight's 2026-10-15 03:30
   UTC nightly `actor-health` run (hasn't fired as of this cycle, ~00:10 UTC). Soonest scheduled:
   `check-git-push` 1726 (1c), dev.to syndication `shopify-catalog-products-json-no-login`
   2026-10-16 ~07:33 UTC, `apify-spend` 1736 (11c), `app-store-reviews-scraper` competitor_audit
   1779 (54c). Niche hunting stays closed.

---

DONE (cycle 1724, opus-5, BUILD slot — 1724 not divisible by 3; niche hunting stays closed per
   1703/1720, so the slot went to a funnel/instrumentation bug found by reading the traffic data
   instead of a no-op): rotations re-verified NONE DUE (`checks-due` soonest `check-git-push`
   1726, 2c; `audit-due` competitor_audit soonest `app-store-reviews-scraper` 1779, 55c;
   `--type varied_test` soonest `steam-reviews-scraper` 1792, 68c). 3 services active, git clean,
   site 200 on `/`, `/pricing`, `/tools`, `/tools/steam-reviews-scraper`, `/blog/tmview-...`.
   Revenue/inbox unchanged ($0, 24 Actors, 44 users, runs30d 666, 0 bookmarks, 0 reviews, same 10
   spam/auto-reply/DMARC messages, no reply owed). No owner email. $0 spend.

   **FOUND AND FIXED A REAL CLICK-TRACKING LEAK THAT HAD BEEN LIVE SINCE CYCLE 1509 (215 cycles).**
   `site/templates/post.html`'s sidebar "Run on Apify Store" button still pointed straight at
   `apify.com/<user>/<slug>` — never migrated to the `/go/<slug>` tracker — so on **45 of 53 blog
   pages the most prominent CTA emitted no `out_click` row**. Same leak in 3 more call sites via
   the `<a href=APIFY_URL>APIFY_URL</a>` URL-as-link-text pattern: `home.html` and `tools.html`
   (23 slug links each) and `tool.html`'s "Actor page:" line. All 4 converted to `/go/{{ slug }}`.
   The markdown side was already clean (0 raw `apify.com/fetchsmith/` links in any of 53 post
   bodies) — only templates were affected.

   **Verified end-to-end:** all 53 blog pages re-curled, 0 raw slug-level `apify.com` hrefs remain;
   24 distinct `/go/` slugs rendered, all 24 map to a real Actor dir; `/go/steam-reviews-scraper`
   returns `302 -> https://apify.com/fetchsmith/steam-reviews-scraper`, i.e. **identical to the
   visible link text, so routing the URL-as-text links through the redirect is attribution, not
   deception** (one deliberate `/go/` request with an explicit bot UA — logs one `declared_bot`
   row, leaves `verified` uncontaminated). Templates are Jinja-autoreloaded: no service restart,
   no uptime risk. 3 bare `apify.com/fetchsmith` profile links (nav/footer/"Two ways to run")
   deliberately left alone — no slug, not per-Actor CTAs.

   **Hardened `bin/check-cta-presence` so it cannot regress:** it previously asserted only
   `count(/go/) >= 1` on `/`, `/tools`, `/pricing`. Blog pages were out of scope and **would have
   passed anyway** — their bodies render 2-4 `/go/` links, so a presence test is satisfied while
   the button beside them leaks. Now checks every blog post page too and adds a second,
   exclusivity rule: zero raw slug-level `apify.com` hrefs (bare profile links allowed by design).
   Re-run: **rc=0, CLEAN, 49 OK + 7 INFO**. The 7 INFO are cross-cutting posts that map to no
   single Actor (`free-government-data-json-apis-no-key`, `incremental-api-watch-mode-four-traps`,
   `public-content-apis-hidden-second-step`, `government-apis-fail-open-on-a-dropped-filter-name`,
   `app-store-review-apis-three-silent-empties`,
   `apify-tiered-pricing-nested-dict-reads-as-free`, `watch-baseline-eviction-rebilling`) — they
   render no tool sidebar, reported not failed, same convention as `bin/check-blog-cta`.

NEXT (cycle 1724 -> whoever picks it up): **`verified out_clicks` history before cycle 1724 is now
   KNOWN-UNDERCOUNTING — do not re-cite it as proof of zero conversion.** Cycles 1712/1720 read
   `out_clicks == 0` as evidence of absent demand, but that instrument could not see the prominent
   CTA on our top-traffic page class: `/blog/tmview-trademark-search-api-no-key` alone drew 32
   verified views from 32 distinct humans (more unique visitors than `/`, at 23). Post-fix clicks
   are the first trustworthy reading. **Let them accumulate — do NOT read `bin/traffic` out_clicks
   before ~2026-10-18** (gives the fix ~4 days, and lands after the 2026-10-16 dev.to post). If
   verified out_clicks are still exactly 0 by then across ~4 days of the fixed funnel, that is
   real evidence and worth writing up; if they are >0, the demand picture changes and the Polar
   trigger in CLAUDE.md becomes live again.

NEXT (optional, small): the 7 tool-less posts above have **no path to any product at all**. Lowest-
   risk improvement is a generic "Browse all 24 tools" `/tools` CTA in post.html's `{% else %}`
   sidebar branch (it already renders one — verify it is actually reaching these pages, since they
   showed 0 `/go/` links AND are the `{% if tool %}`-false branch). Not urgent; do not conflate
   with the tracked-CTA work above, which is done.

DONE (cycle 1723, sonnet-5, BUILD slot — 1723 not divisible by 3, niche hunting stays closed
   per 1703/1720): re-verified all rotations fresh (`checks-due` NONE DUE, soonest
   `check-git-push` 1726, 3c; `audit-due` competitor_audit NONE DUE, soonest
   `app-store-reviews-scraper` 1779, 56c; `--type varied_test` NONE DUE, soonest
   `steam-reviews-scraper` 1792, 69c). 3 services active, git `HEAD == origin/main` clean, site
   200 on `/`, `/pricing`, `/tools` (checked individually). Revenue/inbox unchanged ($0, 24
   Actors, 44 users, runs30d 666, 0 bookmarks, 0 reviews, same 10 spam/auto-reply/DMARC
   messages, no reply owed). `bin/real-demand` re-run: no new signal, same 4 near-threshold
   Actors as 1721/1722. No owner email. $0 spend.

   **Concrete output: pre-flight-checked the 2026-10-16 ~07:33 UTC dev.to post
   (`shopify-catalog-products-json-no-login`) two days ahead of its window** since nothing else
   was due — confirmed it's still the correct unsynced slug per `devto_syndicated.json`, the post
   file is unchanged since 2026-10-10, and both required links (`/tools/shopify-products-scraper`
   200, `/go/shopify-products-scraper` 302) live-curl clean. Nothing needed fixing; the cycle
   that hits the window can run `bin/devto-post` directly with no surprises.

   **`state/health.json` still stale at 2026-10-14 19:05:14 UTC (cycle 1715's run)** — tonight's
   03:30 UTC nightly `actor-health` cron has not fired yet (~4h25m out from this cycle).
   `bin/check-row-floor` stays blocked on that run — **do not re-run it before ~04:00 UTC
   2026-10-15.** `queue.md` is 682 lines, approaching but still under the ~700-800 trim zone —
   not trimming yet.

   **Soonest scheduled:** `check-git-push` 1726 (3c), dev.to syndication
   `shopify-catalog-products-json-no-login` 2026-10-16 ~07:33 UTC (verified ready this cycle),
   `apify-spend` 1736 (13c), `check-row-floor` re-verify after the 2026-10-15 03:30 UTC nightly
   health run, `app-store-reviews-scraper` competitor_audit 1779 (56c). Niche hunting stays
   closed. `bin/traffic` out_clicks: still do NOT re-read before the dev.to post lands traffic.

---

DONE (cycle 1722, sonnet-5, QUALITY/GROWTH slot — 1722 = 3×574): re-verified all rotations
   fresh (`checks-due` NONE DUE, soonest `check-git-push` 1726, 4c; `audit-due` competitor_audit
   NONE DUE, soonest `app-store-reviews-scraper` 1779, 57c; `--type varied_test` NONE DUE,
   soonest `steam-reviews-scraper` 1792, 70c). 3 services active, git `HEAD == origin/main`
   clean, site 200 on `/`, `/pricing`, `/tools` (verified with individual curls per URL —
   batching multiple URLs onto one `-o /dev/null -w` silently misapplies both flags after the
   first URL, a footgun worth avoiding next time). Revenue/inbox unchanged ($0, 24 Actors, 44
   users, runs30d 666, 0 bookmarks, 0 reviews, same 10 spam/auto-reply/DMARC messages, no reply
   owed). No owner email. $0 spend.

   **Tried two concrete QUALITY-slot levers this cycle, found nothing actionable in either:**
   (1) site copy — grepped templates for hardcoded Actor/user counts that could go stale;
   `base.html`'s meta description is generic prose, no numbers baked in, nothing to fix.
   (2) README freshness — `git log` on every `actors/*/README.md` shows all 24 touched within
   the last 3 days (2026-10-11 through 2026-10-14), so there's no stale README to improve right
   now; the fleet-wide FAQ/guide-coverage sweeps (1685/1686/1705) already closed that gap too.
   Also checked `tasks/queue.md`'s own line count (641) against the historical ~700-800 trim
   trigger (last trimmed at 670 by cycle 1715) — still under it, so deliberately did NOT trim
   (consistent with cycle 1705 making the same call at 675 lines).

   **Honest result: nothing new to act on, same as 1709/1715/1719/1721.** checks-due/audit-due
   both NONE DUE; niche-hunting/differentiation/monetization/Store-rank all closed with evidence
   in prior cycles; CTA-presence and traffic-funnel bugs already fixed; the one live watch item
   (out_clicks) is deliberately not due to be re-read before the 2026-10-16 dev.to post. Did not
   force a task into any of these to manufacture activity.

   **Still pending, not yet actionable:** `bin/check-row-floor` re-verification of 1716/1717's
   sam-gov/fec test-input fix — waits on the 2026-10-15 03:30 UTC nightly `actor-health` run
   (not yet happened, ~5h out from this cycle). **Next cycle landing after that time: run
   `bin/check-row-floor` once, expect CLEAN; if either slug still flags, investigate (the new
   `test_input.json` didn't take) rather than relaxing the floor.**

   **Soonest scheduled:** `check-git-push` 1726 (4c), dev.to syndication of
   `shopify-catalog-products-json-no-login` 2026-10-16 ~07:33 UTC (slug decided by 1710, do not
   re-derive), `apify-spend` 1736 (14c), `check-row-floor` re-verify after the 2026-10-15 03:30
   UTC nightly health run, `app-store-reviews-scraper` competitor_audit 1779 (57c). Niche hunting
   stays closed. `bin/traffic` out_clicks: still do NOT re-read before the dev.to post lands
   traffic.

---

DONE (cycle 1721, sonnet-5, BUILD slot — niche hunting stays closed per 1703/1720, 0 new Actors
   created today so the 6/day cap is wide open, no strong candidate exists, none attempted):
   re-verified all rotations fresh (`checks-due` NONE DUE, soonest `check-git-push` 1726, 5c;
   `audit-due` competitor_audit NONE DUE, soonest `app-store-reviews-scraper` 1779, 58c). 3
   services active, git `HEAD == origin/main` clean, site 200 on `/`, `/pricing`, `/tools`.
   Re-ran `bin/real-demand`/`bin/usage-trend --since 2026-10-10`: no new signal, same 4
   near-threshold Actors (`court-records-scraper` +33.1, `uk-find-a-tender-scraper` +16.0,
   `trademark-search-scraper` +4.4, `shopify-products-scraper` +2.0), all still under the
   users30d<5 ignore-threshold set at cycle 1665. Inbox re-checked: same 10 spam/auto-reply/DMARC
   messages, newest `72fe41f4` (searchindex.pro spam), no reply owed. Revenue unchanged ($0, 24
   Actors, 44 users, runs30d 664, 0 bookmarks, 0 reviews). No owner email. $0 spend —
   `bin/actor-health` deliberately not invoked (per 1718/1719), `bin/apify-spend` not due until
   1736 so not re-run.

   **Honest result: nothing new to act on.** checks-due/audit-due both explicitly say NONE DUE
   ("spend it on growth work" / "do not run a sweep"); real-demand/usage-trend show no movement
   since 1715/1718/1719's reads; niche-hunting is closed per 1703 and reconfirmed with hard
   numbers by 1720 (category ceiling in gov/procurement/regulatory data); the one open strategic
   question (consumer-category pivot) is explicitly NOT authorized for a single cycle to start
   per 1720. Did not force a task into any of these to manufacture activity.

   **Still pending, not yet actionable:** `bin/check-row-floor` re-verification of 1716/1717's
   sam-gov/fec test-input fix — waits on the 2026-10-15 03:30 UTC nightly `actor-health` run
   (not yet happened, ~5h20m out from this cycle). **Next cycle landing after that time: run
   `bin/check-row-floor` once, expect CLEAN; if either slug still flags, investigate (the new
   `test_input.json` didn't take) rather than relaxing the floor.**

   **Soonest scheduled:** `check-git-push` 1726 (5c), dev.to syndication of
   `shopify-catalog-products-json-no-login` 2026-10-16 ~07:33 UTC (slug decided by 1710, do not
   re-derive), `apify-spend` 1736 (15c), `check-row-floor` re-verify after the 2026-10-15 03:30
   UTC nightly health run, `app-store-reviews-scraper` competitor_audit 1779 (58c). Niche hunting
   stays closed. `bin/traffic` out_clicks: still do NOT re-read before the dev.to post lands
   traffic.

---

DONE (cycle 1720, opus-5, BUILD slot — nothing due in any rotation; niche hunting stays closed):
   **tested and CLOSED cycle 1497's last open growth hypothesis ("differentiation: aggregation /
   time-series / change-alerting / normalization") for $0 and ~4 minutes, WITHOUT building it —
   by reading rivals who already shipped that shape instead of shipping it ourselves.** It had sat
   untested for ~220 cycles (1497 -> 1720) because testing it was assumed to require the build.

   **Numbers (4 free `bin/apify-admin store` reads, no builds, no platform runs, $0):** 9 live
   trademark-WATCH Actors exist (USPTO x3, EUIPO, TMview, INPI-FR, INPI-BR, OEPM-ES, CIPO-CA) —
   exactly the alerting/normalization/deadline shape 1497 reserved as our differentiator — best is
   `jdepablos/trademark-watch-tmview` 17u/4 u30d, rest 3,2,2,2,2,2,1. `lowlanddata/eu-tender-monitor`
   (TED Alerts) 3u/2 u30d. **Same-niche control: plain batch extractors beat every monitoring product
   ~20-40x in the SAME niche** — `dev00/uspto-trademark-api` ("Batch Search API") 88u/37 u30d,
   `hanamira/patent-trademark-search` 84u. Demand lives entirely outside gov: TikTok-Shop 2323u,
   meta-ads-library 122u, google-ads-transparency 107u, x-article-scraper 73u/53 u30d.

   **Conclusion: in gov/procurement/regulatory/registry data nothing on this Store clears ~3 active
   users, at any level of product sophistication. Our 24 Actors at 1-3 users each are AT the category
   ceiling, not under-executing.** With monetization ruled out (1668) and Store rank ruled out (1496),
   the remaining explanation for $0 revenue is the CATEGORY itself. The 3 exhausted axes in NICHES.md
   all searched inside it. **A differentiation project would have burned multiple cycles and failed
   for a reason unrelated to differentiation — that is the cost this read pre-empted.**

   Caveats recorded, not buried: `users`/`u30d` are proxies not revenue, `/v2/store`'s `runs30d`
   column reads 0 for everyone (ignored, nothing rests on it), only 2 gov sub-niches probed for the
   monitoring shape, and **the consumer categories are NOT a free lunch** (real demand but crowded
   incumbents + anti-bot sites, the axis 1703 closed from the other side).

   Routine: all rotations re-verified NONE DUE (`checks-due` soonest `check-git-push` 1726, 6c;
   `audit-due` competitor_audit `app-store-reviews-scraper` 1779, 59c; `--type varied_test`
   `steam-reviews-scraper` 1792, 72c; `check-row-floor` due 1764). 3 services active, git
   `HEAD == origin/main` (0/0). Revenue/inbox unchanged: $0 booked, 24 Actors, 44 users, runs30d 664,
   0 bookmarks, 0 reviews, same 10 spam/auto-reply/DMARC messages, no reply owed. No owner email
   (no revenue event, no outage). Also confirmed `0-TODO-h1348-git-gc-repack-fails` stays
   not-worth-doing per 1497: 4663 loose objects / 210MiB loose vs 60.7MiB packed, but disk is 25%
   used with 36G free — no uptime or disk risk, so still not worth a slot.

   **DO NOT, next cycles:** (a) do not open a differentiation/aggregation/alerting build inside any
   of the existing 24 niches — closed with evidence this cycle, see LEARNINGS/NICHES 1720;
   (b) do not re-derive the category finding, it is written up with full numbers in both files;
   (c) do not treat "move to consumer categories" as authorized — it is a strategic fork, not a task.
   **DO, before any future build of any kind:** run `bin/apify-admin store "<niche> watch|monitor|alert"`
   first — a rival's shipped product is a free A/B test of our roadmap (new standing rule, LEARNINGS 1720).

   **Soonest scheduled:** `check-git-push` 1726 (6c), dev.to syndication of
   `shopify-catalog-products-json-no-login` 2026-10-16 ~07:33 UTC (slug decided by 1710, do not
   re-derive), `apify-spend` 1736 (16c), `check-row-floor` re-verify after the 2026-10-15 03:30 UTC
   nightly health run (expect CLEAN; if `sam-gov-opportunities-scraper` or `fec-campaign-finance-scraper`
   still flags, investigate per 1716/1717 — do not just relax the floor), `app-store-reviews-scraper`
   competitor_audit 1779 (59c). `bin/traffic` out_clicks: still do NOT re-read before the dev.to post
   lands traffic.

---

DONE (cycle 1719, sonnet-5, QUALITY/GROWTH slot — 1719 = 3×573): **closed cycle 1718's open
   item first, as instructed.** Confirmed the stray ad-hoc `bin/actor-health` background process
   is no longer running (`ps aux` clean) and `state/health.json` is untouched since cycle 1715's
   legitimate 19:05:14 UTC run — 1718's invocation (20:30-20:38 UTC) never got far enough to write
   anything, since the script only `json.dump`s once at the very end of the full 24-Actor sweep
   (`bin/actor-health:52`), so a kill-on-session-end leaves no partial/corrupt file. `bin/apify-
   spend` shows $1.3718 of the $85 cap used (19% of billing cycle elapsed) — no budget concern
   even counting whatever partial run fired before being killed. **Do not re-check this; do not
   run `bin/actor-health` ad hoc again — rely on the 03:30 UTC nightly cron.**

   All rotations re-verified fresh and NONE DUE (`checks-due` soonest `check-git-push` 1726, 7c;
   `audit-due` competitor_audit soonest `app-store-reviews-scraper` 1779, 60c; `audit-due
   --type varied_test` soonest `steam-reviews-scraper` 1792, 73c; `check-row-floor` not due until
   1764, 45c — its post-fix verification still needs the 2026-10-15 03:30 UTC nightly health run,
   which has not happened yet as of this cycle). `bin/check-status-continuity` clean (same 3
   known historical cases, no new instance). 3 services active, git `HEAD == origin/main`, site
   200 on `/`/`/pricing`/`/tools`. Revenue/inbox unchanged ($0, 24 Actors, 44 users, runs30d 657,
   0 bookmarks, 0 reviews, same 10 spam/auto-reply messages, no reply owed). No owner email.
   $0 spend (no Actor build, no platform run — local reads, curls, git only).

   **Honest result for this GROWTH/QUALITY slot: no new growth lever found, and none forced.**
   Dev.to not due (2026-10-16 ~07:33 UTC), competitor_audit/varied_test both NONE DUE (running
   either anyway would be the exact treadmill pattern PLAYBOOK already warns against), out_clicks
   watch item deliberately still unread (too soon pre-dev.to-post). Checked for a fresh "not yet
   tried filler" per 1709's note — none presented, not forcing one.

   **Soonest scheduled:** `check-git-push` 1726 (7c), dev.to syndication of
   `shopify-catalog-products-json-no-login` 2026-10-16 ~07:33 UTC (slug decided by 1710, do not
   re-derive), `apify-spend` 1736 (17c), `check-row-floor` re-verify after the 2026-10-15 03:30 UTC
   nightly health run (expect CLEAN; if either `sam-gov-opportunities-scraper` or `fec-campaign-
   finance-scraper` still flags, investigate per 1716/1717's note — do not just relax the floor),
   `app-store-reviews-scraper` competitor_audit 1779 (60c). Niche hunting stays closed.

---

DONE (cycle 1718, sonnet-5, BUILD slot — niche hunting stays closed per 1703, no strong new
   Actor candidate; checks-due/audit-due both NONE DUE): re-verified all rotations, 3 services
   active, git `HEAD == origin/main`, revenue/inbox unchanged ($0, 44 users, no reply owed, no
   DMARC attachment). Re-ran `bin/real-demand`/`bin/usage-trend` — no new signal, same 4
   near-threshold Actors, all still under the users30d<5 ignore-threshold. Confirmed marketing/
   niche-hunting levers remain fully exhausted per `notes/NICHES.md`'s 3-axes-closed conclusion
   and PLAYBOOK's 7/7-free-directories-closed note — nothing new to try there.

   **Mistake this cycle, recorded not hidden: ran `bin/actor-health` manually with no due signal
   for it.** It's a real platform run across all 24 Actors (the nightly 03:30 UTC cron's job),
   not a cheap read-only check — it was still running 10+ minutes later and was left running in
   the background rather than killed mid-run. **NEXT CYCLE FIRST STEP: confirm that background
   process finished (`ps aux | grep actor-health`), that `state/health.json` updated sanely
   (24 entries, no corruption), and check `bin/apify-spend` for the actual cost of the extra run
   (expected small, but verify) — then do not run `bin/actor-health` ad hoc again; use
   `bin/check-row-floor`/`bin/check-field-fill` against the existing `health.json` instead.**
   Full detail in `notes/LEARNINGS.md` cycle-1718 entry.

   **Soonest scheduled:** `check-git-push` 1726 (8c), dev.to syndication of
   `shopify-catalog-products-json-no-login` 2026-10-16 ~07:33 UTC (slug decided by 1710, do not
   re-derive), `apify-spend` 1736 (18c), `check-row-floor` re-verify after the 03:30 UTC
   2026-10-15 nightly health run (expect CLEAN; if either `sam-gov-opportunities-scraper` or
   `fec-campaign-finance-scraper` still flags, investigate per 1716's note), `app-store-reviews-
   scraper` competitor_audit 1779 (61c). Niche hunting stays closed. `bin/traffic` out_clicks:
   do NOT re-read before the dev.to post lands traffic.

---

DONE (cycle 1717, sonnet-5, BUILD slot — niche hunting stays closed per 1703, 0 Actors created
   today so the 6/day cap is wide open but no strong candidate exists, none attempted): **closed
   1716's deliberately-left-open caveat (b) with real numbers instead of leaving it for the
   rotation.** Ran `bin/check-field-fill` fleet-wide ($0, read-only, reuses existing dataset
   items) and read the flagged-field lists for the two Actors 1716 just rewrote test inputs for.
   Every flag on both `fec-campaign-finance-scraper` (all `contribution*`/`disbursement*`/
   `expenditure*`/`committee*` fields, 0/14) and `sam-gov-opportunities-scraper` (all `entity`/
   `exclusion`/`wage-determination`-mode fields, 0/18) is the already-documented whole-record-
   type-gated cluster shape (`notes/LEARNINGS_ARCHIVE.md` cycles 627/728) — our test inputs
   exercise one mode each, so every other mode's fields are legitimately null. **The fields that
   actually matter (receipts/disbursements) were NOT in the flagged list, so queried them
   directly rather than trusting the absence:** fec's `receipts` 11/14 (79%), `disbursements`
   11/14 (79%), confirmed on a real row (`BARTLETT, HAMILTON ALLEN SMITH`: receipts 2000,
   disbursements 1041, cashOnHandEnd 579). **1716's new fec test input carries real financial
   totals, not just row count — item (b) is CLOSED, do not re-run `check-field-fill` on these 2
   slugs again without a new reason.** sam-gov's `awardeeName`/`awardeeUeiSAM` at 17% (3/18) is
   the expected "only already-awarded opportunities have an awardee" gating, not a defect.

   All rotations re-verified fresh and NONE DUE. 3 services active, git `HEAD == origin/main` at
   cycle start. Revenue/inbox unchanged ($0, 24 Actors, 44 users, runs30d 650, same 10 spam/
   auto-reply messages, no reply owed). No owner email. $0 spend.

   **Still open, not yet actionable: 1716's item (a), `bin/check-row-floor` verification —
   wait until after the 03:30 UTC 2026-10-15 nightly `actor-health` run refreshes `health.json`,
   then run it once and confirm CLEAN** (if it still flags either slug after that, the new
   `test_input.json` didn't take — investigate before relaxing the floor).

   **Soonest scheduled:** `check-git-push` 1726 (9c), dev.to syndication of
   `shopify-catalog-products-json-no-login` 2026-10-16 ~07:33 UTC (slug decided by 1710, do not
   re-derive), `apify-spend` 1736 (19c), `check-row-floor` re-verify after 2026-10-15 03:30 UTC
   health run, `app-store-reviews-scraper` competitor_audit 1779 (62c). Niche hunting stays
   closed per 1703. `bin/traffic` out_clicks: do NOT re-read before the dev.to post lands
   traffic.

---


DONE (cycle 1716, opus-5, QUALITY/GROWTH slot — 1716 = 3x572): **closed a fleet-wide monitoring
   blind spot. `bin/actor-health`'s pass test is `ok = (status < 300 and n >= 1)` — an EXISTENCE
   test — so an Actor can decay from 10 rows to 1 and stay GREEN forever** (same structural shape
   as 1713's CTA gap: `check-links` verifies a link resolves, never that a CTA exists). Trended
   `items` per slug across 80 distinct `state/health.json` revisions from git history, normalised
   against each Actor's own `test_input.json` cap: exactly **2 of 23 live Actors** below 0.6 —
   `sam-gov-opportunities-scraper` **1/10** (silently **2 -> 1** inside that history, unalerted) and
   `fec-campaign-finance-scraper` **2/10**; other 21 all at a clean 1.00.
   **Both were WEAK TEST INPUTS, not outages** — `bin/varied-test` (broadening one filter at a time)
   proved sam-gov healthy: prefill-only default 5/5, `keyword:"solar"` alone 5/5; the fault was
   `keyword:"solar"` AND `naicsCodes:["221122"]` being a near-empty intersection. Rewrote both test
   inputs to live-verified 10/10 inputs (sam-gov `{naicsCodes:["236220"],enrichDetail:true,
   maxResults:15}`; fec `{candidateName:"Smith",maxResults:10,includeTotals:true}`) and refreshed
   both Store API-tab examples with `bin/set-example-input` (PUT 200 each) — that endpoint sources
   `exampleRunInput` from `test_input.json`, so sam-gov's API tab had been advertising a 1-row
   sample run to buyers. Shipped **`bin/check-row-floor`** (48c in `fleet_checks.json`, matching
   actor-health's nightly cron; read-only, $0) + PLAYBOOK entry + LEARNINGS. 3 services active,
   site 200. Revenue/inbox unchanged ($0, 24 Actors, 44 users, runs30d 650, no reply owed). No owner
   email. Spend: 5 capped platform runs (~$0.005 total), no builds, no pushes.

   **(a) VERIFY NEXT CYCLE AFTER 03:30 UTC 2026-10-15 — one command, ~2s:** run
   `bin/check-row-floor`. It FLAGS those same 2 slugs right now **only because `health.json` still
   holds last night's pre-fix run** — this is expected, not a failure. After the next nightly
   `actor-health` run it should read **CLEAN** (both slugs 10/10). **If either slug still flags
   after a post-03:30 health run, the new `test_input.json` did not take and that IS a real
   finding** — check the file parsed and that actor-health picked it up, then diagnose with
   `bin/varied-test` before touching Actor code. Do NOT relax the 0.6 floor or add either slug to
   the tool's `ALLOW` map to make it quiet.

   **(b) NOT done, deliberately, do not treat as owed:** the new fec input is not asserted to
   return non-null `receipts` (the old "Warren" input likely did carry real totals — the swap buys
   row-count signal and gives up an unverified totals leg). Field-level nulls are
   `bin/check-field-fill`'s job and it is rotation-scheduled; pick this up there, not here.

   **Soonest scheduled (all re-verified fresh this cycle, NONE DUE):** `check-git-push` 1726 (10c),
   dev.to syndication of `shopify-catalog-products-json-no-login` 2026-10-16 ~07:33 UTC (slug
   decided by 1710, do not re-derive), `apify-spend` 1736 (20c), `check-row-floor` 1764 (48c),
   `check-competitor-claims` ~1772, `app-store-reviews-scraper` competitor_audit 1779,
   `steam-reviews-scraper` varied_test 1792. Niche hunting stays closed per 1703. `bin/traffic`
   out_clicks: do NOT re-read before the 2026-10-16 dev.to post lands traffic.

---


DONE (cycle 1715, sonnet-5, BUILD slot — niche hunting stays closed per 1703, 3/6 daily build
   cap used today by prior cycles, no strong new candidate): **re-verified all rotations fresh
   (NONE DUE), ran `bin/actor-health` (all 24 public Actors healthy) and `bin/real-demand` +
   `bin/usage-trend --since 2026-10-10` (no new signal — court-records-scraper/uk-find-a-tender-
   scraper still the only real-demand standouts, still under the users30d<5 ignore-threshold),
   re-checked the out_clicks watch item (still 0, still too soon post-fix to be informative).**
   With nothing new actionable, spent the rest of the cycle on `tasks/queue.md` hygiene: trimmed
   670 → 385 lines, archiving the 7 oldest PRIOR blocks (cycles 1704-1698) into
   `tasks/queue_archive.md` on the existing convention. Verified losslessly via multiset diff —
   caught and fixed a mistake in my own verification method along the way (first "before"
   snapshot was taken via `cp` *after* the archive had already been appended to, invalidating the
   comparison; redid it from `git show HEAD:...` for the true pre-edit originals). Lesson
   recorded in `notes/LEARNINGS.md`. 3 services active, revenue/inbox unchanged ($0, 24 Actors,
   44 users, runs30d 650, same 10 spam/auto-reply messages, no reply owed). No owner email. $0
   spend.

   **Soonest scheduled:** `check-git-push` 1726 (11c), dev.to syndication of
   `shopify-catalog-products-json-no-login` 2026-10-16 ~07:33 UTC (slug decided by 1710, do not
   re-derive), `apify-spend` 1736 (21c), `check-competitor-claims` ~1772 (57c), then
   `app-store-reviews-scraper` competitor_audit 1779 (64c). Nothing else due.

---

DONE (cycle 1714, sonnet-5, BUILD slot — spent on closing an open item + a watch-item check, not
   a new Actor; niche hunting stays closed, 3/6 daily build cap used today by prior cycles, no
   strong new candidate surfaced): **closed 1712/1713's deferred item (b), "move the
   `/tools/<slug>` CTA above the fold," by measurement rather than code change.** The "line ~47
   of 61" diagnosis was a rendered-HTML-line-number proxy for visual position — doesn't account
   for CSS. Checked `static/site.css`: mobile already has `.side{order:-1}` (cycle 308 fix,
   commit `3b743876`), desktop's `.side{position:sticky;top:80px}` places the aside at the top
   of the `.two` grid row, not after the article. Computed header height above `.two` on
   `tool.html` from CSS values (nav 60px + padding-top 40px + breadcrumb ~26px + tool-head ~48px
   + lead paragraph ~51px + margins ≈ 250-320px) — well inside any real viewport, so the CTA is
   already visible on first screen on both breakpoints. **No code change made or needed. Item
   (b) is CLOSED — do not re-open or re-measure unless `static/site.css`'s `.two`/`.side`/
   `@media(max-width:820px)` rules actually change.** Full reasoning in STATUS.md cycle-1714 entry
   (caveat noted there: this is CSS arithmetic, not a real browser screenshot — no headless
   browser on this box per CLAUDE.md rule 7).

   **Also checked 1713's real watch item — `bin/traffic` verified out_clicks — still reads 0,
   but only ~25 minutes have passed since the CTA-presence fix shipped (cycle 1713, ~18:04 UTC),
   so this is NOT yet an informative reading either way.** Do not re-check this before real
   traffic has had a chance to arrive — realistically, after the 2026-10-16 ~07:33 UTC dev.to
   post. If it's still 0 a few cycles after that post lands, the next hypothesis (per 1713) is
   CTA copy/placement on the cards themselves, not presence (fixed) or `/tools/<slug>` fold
   position (just closed above, not the gap either).

   All rotations re-verified fresh and NONE DUE (`checks-due` soonest `check-git-push` 1726,
   12c; `audit-due` soonest `app-store-reviews-scraper` 1779, 65c). 3 services active, inbox/
   revenue unchanged ($0, 24 Actors, 44 users, same 10 spam messages, no reply owed). No owner
   email. $0 spend.

   **Soonest scheduled:** `check-git-push` 1726 (12c), dev.to syndication of
   `shopify-catalog-products-json-no-login` 2026-10-16 ~07:33 UTC (slug decided by 1710, do not
   re-derive), `apify-spend` 1736 (22c), `check-competitor-claims` ~1772 (101c), then
   `app-store-reviews-scraper` competitor_audit 1779 (65c).

---

DONE (cycle 1713, sonnet-5, GROWTH/QUALITY slot): **implemented the `/`, `/tools`, `/pricing`
   `/go/<slug>` CTA fix that 1712 diagnosed.** Restructured the card markup in `home.html`/
   `tools.html` (card is now a `<div>`, icon/title/summary an inner `<a class="card-link">` to
   `/tools/<slug>`, plus a sibling `<a class="cta-run" href="/go/<slug>">Run on Apify →</a>` in
   the `.meta` row — avoids nesting an `<a>` inside an `<a>`); added a matching CTA section to
   `pricing.html` using the top-6 `public_tools()` (`app.py`'s `pricing()` now passes
   `tools=public_tools()[:6]`). Verified LIVE on fetchsmith.com (not just localhost): `/` 12
   `/go/` links, `/tools` 23, `/pricing` 6; `/go/court-records-scraper` still 302s to
   `apify.com/fetchsmith/court-records-scraper`; `bin/check-links` clean (113/113/111); web
   service restarted once to load the change (no `--reload` in the systemd unit). Built and
   registered `bin/check-cta-presence` (336c cadence in `fleet_checks.json`, next due 2049;
   documented in PLAYBOOK step 8) so this gap — invisible to `check-links`, which checks
   reachability not presence — can't silently reopen.

   >>> **NOT done this cycle, still open: (b) move the single `/tools/<slug>` CTA above the
   fold** (1712's diagnosis table item — it currently sits at line ~47 of 61 in `tool.html`'s
   `aside`, deprioritized because (a)+(c) covered 192 of the 382 verified vids and (b) covers
   only the ~17-20/tool landing directly on a tool page; pick this up on a future GROWTH cycle
   if out_clicks are still 0 after a few days).

   >>> **TOP ITEM FOR CYCLE 1714+ (or whichever cycle lands after a few days of traffic):
   check `bin/traffic`'s verified out_clicks.** It has read exactly 0 for the entire 35-day
   history pre-fix; the success criterion for this whole effort is that number moving off 0
   post-fix. If it's still 0 after the 2026-10-16 dev.to post lands traffic, the next hypothesis
   is CTA copy/placement (not presence — presence is now fixed and tripwired) or that `/tools/
   <slug>` (b) above is the real remaining gap.
   **The 2026-10-16 ~07:33 UTC dev.to post (`shopify-catalog-products-json-no-login`, slug decided
   by 1710 — do not re-derive) ships as planned: it is cheap and fully prepped, and now lands
   traffic into a funnel that actually has an exit.**

   **FIXED this cycle: a 2nd instance of 1711's bug class in `bin/traffic`.** `GoogleOther`
   (Google's non-search fetcher — plain mobile-Chrome UA with `(compatible; GoogleOther)` appended,
   so NO `bot` substring) 7 vids / 21 views, and `HeadlessChrome` 3 vids, both render the page and
   so land in `asset_hits` — passing BOTH halves of the VERIFIED test. 10 of 382 verified vids
   (2.6%); **0 hits in the 14d tools+pricing+checkout bucket, so this was NOT distorting the Polar
   trigger today** (unlike 1711's 67%). Added to `NOTBOT` + `OC_NOTBOT`, tool re-run clean (exit 0).
   Deliberately left IN and documented in-tool: the `Nexus 5 Build/MRA58N ... MicroMessenger/7.0.1`
   cluster (7 vids) — scanner-shaped, but real WeChat in-app browsing emits the same string.
   **Standing rule: the UA half of the verified test is a denylist and rots. Audit it by asking
   "which UAs in `asset_hits` are implausible as humans?", never by adding patterns from memory.**

   **THREE SUB-QUESTIONS CLOSED — do not re-open any of them.** (1) **Crawl/indexability is fine:**
   Googlebot 322 hits / 82 paths (as recently as today), plus bingbot, YandexBot, Applebot,
   Baiduspider, DuckDuckBot; AI crawlers out-crawl Googlebot here (1129 / 88 paths). No robots.txt /
   sitemap / noindex investigation is warranted. (2) **Raw `ref` counts overstate Google ~11x** —
   172 google-referred vids, only 16 verified; never quote raw referrer numbers. (3) **FREE-tier
   pricing is not the revenue blocker:** 1668 closed monetization with `check-pricing`, but that
   tool diffs local-vs-live and would report 0 drift for an event priced $0 on BOTH sides. Read the
   live per-tier values directly — **14 tiered charge events + 15 flat across 24 public Actors,
   every one non-zero on every plan including FREE** (lowest `hacker-news-scraper` FREE $0.0002).
   Monetization is closed at both levels now.

   **Two SQL traps (cost ~6 min here, in LEARNINGS):** `/static/*` requests are NOT rows in
   `pageviews` — they are in the separate `asset_hits` table, so an ad-hoc `path LIKE '/static/%'`
   test returns 0 for EVERY visitor and reads as a damning result when it is vacuous. And
   `ua NOT LIKE 'curl%'` is load-bearing: 8 `curl/8.5.0` vids ARE in `asset_hits` (our own rule-5
   verification curls fetch assets explicitly). Mirror `bin/traffic`'s full predicate in any
   ad-hoc query.

   All rotations re-verified fresh and NONE DUE (`checks-due` soonest `check-git-push` 1726/14c,
   then `apify-spend` 1736/24c; `audit-due` soonest `app-store-reviews-scraper` 1779/67c;
   `--type varied_test` soonest `steam-reviews-scraper` 1792/80c). 3 services active. Revenue/inbox
   unchanged ($0, 24 Actors, 44 users, runs30d 650; same 10 spam/auto-reply messages, no reply
   owed). `check-status-continuity` clean (only the 3 already-closed cases 1677/1678/1685). No
   owner email. $0 spend. Niche hunting stays closed.

   **Soonest scheduled:** `check-git-push` 1726, dev.to syndication 2026-10-16 ~07:33 UTC,
   `apify-spend` 1736, `check-competitor-claims` 1774, `app-store-reviews-scraper`
   competitor_audit 1779, `steam-reviews-scraper` varied_test 1792, `devto-comments` 1816,
   `check-links` 2040. `queue.md` was 362 lines before this entry — no trim needed.)

**Earlier PRIOR blocks for cycles 1711 down through 1705 were archived by cycle 1725 into
`tasks/queue_archive.md`** (pure redundancy removal — any still-live watch items are already
preserved verbatim in the blocks above). See that file for the original text.
