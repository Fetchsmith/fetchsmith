- [x] **DONE cycle 2366 (QUALITY/GROWTH slot) -- did the trim c2364 queued for this slot (`bin/_trim2366.py` + `bin/_trim2366q.py`) and ran the one due fleet check.** `state/STATUS.md` (144.2KB->23.9KB, kept window 2360..2365) and `tasks/queue.md` (101.6KB->24.6KB, hoist-then-cut: 5 kept DONE blocks + 10 hoisted live open items, 3 archived as closed-but-unchecked since already resolved, rest moved verbatim to `tasks/queue_archive.md`) both trimmed proactively -- `check-doc-size` had read TRIM SOON on both (not yet over the 150KB warn line, but projected past it before the checker's next look). Both trim scripts verified lossless reconstruction before writing; `check-doc-size`/`check-status-continuity`/`check-status-blocks-kept` all clean after. `check-source-endpoints` (24c due) run: 49 hosts probed, 1 DEVIATION (`rss.marketingtools.apple.com` ReadTimeout) -- re-tested live (3 direct curls: 200/timeout/timeout) and via `bin/actor-health --only apple-podcasts-scraper` (`ok:true, items:5`), confirmed transient upstream flakiness already absorbed by the Actor's own retry logic, not a regression; recorded, next due c2390. Full detail in `state/STATUS.md` cycle-2366 entry. $0 spent, 0 code changes, 0 new Actors, revenue unchanged, no owner email warranted. **Deferred to next cycle for time-budget reasons: the orphan-blog-posts follow-up (hoisted this trim, still open below the kept DONE blocks).**

- [x] **DONE cycle 2364 -- closed the c2363 FEC rate-limit follow-up, and the answer was better than "swap the numbers".** The `1,000/hr vs 40/hr` ceilings in `fec-campaign-finance-scraper`'s 429 message, its code comment, the DEMO_KEY `log.info`, and THREE README passages all traced back to one source: the prose inside the FEC's own 429 error body (`"40 calls per hour for the DEMO_KEY, 1000 calls per hour for a personal key, or 120 calls per minute for an upgraded key"`). Our OWN blog post `fec-campaign-finance-json-api-demo-key` had already established, from a live capture, that that prose is decoration and `x-ratelimit-limit` is the only enforced number (body said 40, header said 10 on the same response) -- we were quoting the thing we told readers not to trust, and the post itself then repeated the 1000/hour figure one paragraph later. Measured live instead (2026-10-28): registered key `x-ratelimit-limit: 60`, DEMO_KEY `10`. **Window resolved too, which c2363 left open:** burned the registered key to `remaining: 56`, idled 165s with ZERO requests, re-requested -> `remaining: 59`, i.e. a full refill -- so it is a minute-scale budget, NOT the hour the body claims nor the 15.9h `Retry-After` claims. (DEMO_KEY is the opposite: its counter kept declining 8 -> 7 across minutes, matching api.data.gov's documented per-hour/per-day per-IP shape at a FEC-lowered ceiling.) Also confirmed from api.data.gov's developer manual that the platform DEFAULTS -- 1,000/hr per key, 30/hr + 50/day for DEMO_KEY -- do not apply here; its own "rate limits may vary by service" clause covers the FEC's override. Fixed in one push (build 0.1.81, code + README together, no `meta.json` change so no `publish`/reindex needed): 429 message now quotes 60/10 and tells a rate-limited buyer to retry in a minute or two, the comment block records the measurement and why the body prose is not usable, and the blog post got a dated Update block applying its own thesis to the personal key. Verified: live `taggedBuilds.latest.readme` carries the new text and zero stale `1,000/hour` strings remain; blog post renders 200. `check-pricing` (30 events, 0 drift), `check-charges` (25 Actors, 0 missing), `check-blog-claims` (all 4 claim classes, 0 stale) clean after.
      **Durable lesson, worth applying beyond this Actor:** when an upstream API states a limit in TWO places that disagree, do not pick the one that sounds authoritative -- measure the refill directly (burn down, idle a known interval, re-read `remaining`). And grep buyer-facing copy for numbers sourced from upstream PROSE; three README passages and an error string had all silently inherited one unverified sentence.

- [x] **DONE cycle 2363 -- closed 2 of the c2362 follow-ups.** (1) `/blog/courtlistener-search-api-two-auth-tiers`'s stale "no key" framing fixed with a dated correction note + a matching edit to the closing "Packaged version" section (title/slug left alone, no SEO value in churning it). Verified rendered (200, note is the first paragraph). (2) The `FEC_API_KEY` end-to-end-verification gap (raised by the c2362 CL_API_TOKEN gotcha: an envVar confirmed present via the API is NOT the same as confirmed reaching the running container) closed for real: curled `api.open.fec.gov` with the real key vs `DEMO_KEY` (x-ratelimit-limit 60 vs 10, proving the key is registered/real), then added a permanent `log.info` in `src/main.js` naming which key is active (build 0.1.80), triggered a live platform run (`eSTotj7t6cOPoG2II`), and read the log: `Using FEC_API_KEY (this Actor's own personal api.data.gov key).` Confirmed. `check-pricing`/`check-charges`/`check-fail-ordering` clean after. Full detail in `state/STATUS.md` cycle-2363 entry.
      **New follow-up filed by this verification, not yet fixed:** `src/main.js`'s 429-handling comment/error text claims 1,000/hr (personal key) vs 40/hr (DEMO_KEY) ceilings; the live `x-ratelimit-limit` header measured this cycle says 60 vs 10 (possibly a per-MINUTE window, not per-hour — needs confirming against api.data.gov's own docs or another rate-limit header before editing buyer-facing text). Low urgency (only shown on an actual 429), but the number shown to a rate-limited buyer is currently wrong. Whoever picks this up: read the api.data.gov rate-limit docs or look for an `x-ratelimit-reset`/period header on a real response before rewriting the error message, don't just swap in the new numbers blind.

- [x] **DONE cycle 2360 -- CAMPAIGN COMPLETE. `uk-find-a-tender-scraper`, the last Actor on the list,
      audited: found a REAL billing-correctness bug (the FIFTH distinct mechanism for the same shape),
      fixed, build 0.1.88, verified live on 4 platform runs. The ~19-cycle, 22-Actor fleet-wide
      `setStatusMessage`/input-validation audit (c2342-c2360) is finished and the retro is written into
      `notes/LEARNINGS.md` (cycle 2360 entry: 5 bugs / 2 clean negatives, the 3 durable platform facts,
      the standard fix template, and the process lesson). Do NOT re-open this campaign; pick a new
      audit target from the follow-ups below.**
      The bug on this Actor: every filter here is applied CLIENT-SIDE as `if (x.length) { ... }` in
      `matches()`, and every list input was normalised with `.map(trim).filter(Boolean)`. So an
      all-blank `cpvCodes:["  "]` / `keywordsAny:[""]` / `regions:["   "]` emptied the list and the
      filter DISAPPEARED -- not zero rows, the whole unfiltered two-portal feed, every row pushed and
      charged at $0.003 (default `maxResults:100` = 75 charged rows past the 25 free, none asked for).
      The scalar text filters had the same shape one level down: `searchQuery:"   "` / `buyerName:"   "`
      are truthy, so they passed the `input.x ? ... : null` guard and then `.trim()` emptied them.
      Notably this Actor's own `malformedCpvCodes` comment explicitly defends against the *widening*
      version of this hazard for wrong-digit-count codes ("an all-malformed cpvCodes list still
      correctly filters everything out") -- while the `.filter(Boolean)` one line above it broke the
      same line for blank ones. Second Actor in a row (after sam-gov c2356) where a defensive comment
      named the class and the normalisation step above it was the hole: screening question 2 again.
      Reachability verified live BEFORE writing any code (5 probe runs created then aborted, $0):
      the platform ACCEPTS `cpvCodes:["  "]`, `keywordsAny:[""]`, `regions:["   "]`, `searchQuery:"   "`,
      and REJECTS `stages:["zzz-bogus"]` with HTTP 400 `invalid-input` -- `stages`/`sources` are the
      only two inputs here carrying an `items.enum`. Third live confirmation of the c2356 fleet rule.
      Fix (build 0.1.88, the standard template): `arrayFilterInput(name, mapEntry)` + `textFilterInput(name)`
      helpers; `Actor.fail()` pre-charge when the raw input was non-empty but normalises to empty;
      partial drops stay a warning and surface in three places (`log.warning`, `blankDropNote()` on all
      status-message arms incl. a NEW arm for the healthy delivering run, `RUN_SUMMARY.blankFilterEntriesDropped`).
      Deliberately NOT failing on an empty string `""` for `searchQuery`/`buyerName` -- that is how the
      Console and most pipelines send a cleared optional field, so failing it would be a regression;
      only a non-empty string that trims away is unambiguous. Written into the LEARNINGS template.
      Verified live post-fix (4 runs): `cpvCodes:["  "]` -> FAILED, full explanatory `statusMessage`,
      `chargedEventCounts {result: 0}`, 0 items; `searchQuery:"   "` -> same; partial
      `cpvCodes:["72000000","  "]` -> SUCCEEDED, 5 rows, note appended to the status message,
      `RUN_SUMMARY.blankFilterEntriesDropped {cpvCodes: 1}`; clean `cpvCodes:["72000000"]` -> SUCCEEDED,
      5 rows. **The partial and the clean run returned byte-identical rows and identical
      `scanned`/`filteredOut` (200/62)** -- proof the surviving value is still applied and the note is
      the only behavioural difference. `bin/check-fail-ordering` re-run: this Actor `ok` (0 fail-before-save).
      README FAQ entry added in the same push ("What if a filter value is blank or just spaces").

- [x] **DONE cycle 2362 -- owner replied with a CourtListener API token (mail `2b237f1b`, same day
      as the c2358 ask) and the fix shipped end-to-end: `court-records-scraper` is restored,
      build 0.1.71, verified live.** `CL_API_TOKEN` added to `secrets/env` and wired as an
      `Authorization: Token <token>` header on every `apiGet()` call; `await Actor.fail()` pre-charge
      if the var is ever missing from a deployment (a config problem, never buyer-fixable). Added
      proactive self-throttling against the free tier's 5/min, 50/hr, **125/day** limits -- shared
      by this ONE account token across every buyer's run, not per-run -- via a persisted
      `fetchsmith-courtlistener-ratelimit` key-value store (same pattern as `WATCH_STORE`):
      `paceRequest()` sleeps before a request already at the trailing-window cap (capped by
      `remainingMs()`, same shape as the existing retry backoff); a new `rateLimited`/
      `rateLimitExceeded` pair mirrors the existing `timedOut`/`timeBudgetExceeded` one exactly and
      feeds a new `markIncomplete('rate-limit', ...)` cause wired into every place `'time-budget'`
      already was (`seedFailure` set, both buyer-facing ternaries, RUN_SUMMARY). README's "no API
      key" claims (headline, FAQ, data-source section, two field-removal footnotes) updated to stay
      accurate -- buyers still need no account, but the *mechanism* changed and a very-large
      `maxResults` run can now occasionally hit the shared daily cap.
      **Non-obvious gotcha that cost real time, written into `notes/LEARNINGS.md` cycle 2362:**
      setting the secret via `PUT /v2/acts/{id}/versions/0.1 {"envVars":[...]}` (the documented
      cycle-255 pattern) did NOT take effect on the build that had already been pushed -- a real
      platform run still hit the Actor's own "CL_API_TOKEN is not configured" guard even though the
      API confirmed the envVar was saved. It only reached the container's `process.env` after a
      SECOND `apify push --force` (0.1.70 -> 0.1.71) with no source change. **Order matters: set the
      envVar, THEN build -- not the other way round.** Flagged a likely-related fleet risk: `fec-
      campaign-finance-scraper`'s `FEC_API_KEY` (set cycle 255, same mechanism) has a silent `??
      'DEMO_KEY'` fallback that would mask this exact failure mode and has never been end-to-end
      verified to actually reach the container. **Follow-up for a future cycle:** check a real
      platform run's `api.data.gov` rate-limit response headers against the much-lower shared
      `DEMO_KEY` ceiling to confirm `FEC_API_KEY` is actually being used, not silently falling back.
      Verified live end-to-end: `apiGet` via API-POST run (`o5Gn16d7TsMxz4w31`, build 0.1.71)
      SUCCEEDED, 6 real Ninth-Circuit opinion/docket rows (not placeholders), `chargedEventCounts
      {result: 0}` (expected, own-token test run); `bin/actor-health --only court-records-scraper`
      now `ok:true, items:10` (was 0 since the c2357 nightly flag). Daily-exhaustion path verified
      LOCALLY only (pre-seeded 120 fake timestamps into the rate-limit KV store, re-ran, got the
      correct `rate-limit` incomplete reason with 0 requests sent / 0 charged) -- not reproduced on
      the real platform, since that would mean actually spending the shared account's real quota.
      `node --check` clean; `bin/check-fail-ordering` 20/20 clean (0 suspects, including this
      Actor's 2 `Actor.fail()` sites); `check-pricing`/`check-charges`/`check-meta-fields` all clean.
      Committed and pushed (`d6a0126b`). **Not done this cycle, left as follow-ups (see below):**
      the `/blog/courtlistener-search-api-two-auth-tiers` post title is now stale (claims "needs no
      key" fleet-wide) and needs a correction note; re-evaluate whether the now-authenticated token
      could restore the `posture` field (dropped c2 for being permanently 0% while anonymous) if the
      budget allows one `/clusters/` call per row on a small-maxResults run; the owner's free-tier
      CourtListener account itself may be worth a `bin/notify` heads-up if it ever shows signs of
      being near a *monthly* (not just daily) cap, which hasn't been checked since this account is
      brand new.
      Original c2357 diagnosis (superseded, kept for context):

- [x] **DONE cycle 2361 -- closed the c2357 `apple-podcasts-scraper` fail-ordering follow-up.** It
      was a pure line-shift false alarm, not a new bug: the h289 seed gate already allowlisted since
      cycle 696 (and re-verified 7 times since) sits at a line number the checker keys its allowlist
      on, and c2337's "name-in-podcasts silently dropped" fix added 13 lines above it, so the key
      went stale (`1391` vs the code's new `1404`) and the checker correctly re-flagged it per its own
      documented design ("a moved call must be re-read, not auto-trusted"). Re-traced the full
      no-charge chain fresh from the charge site outward (not just re-read the guard text): sole
      `Actor.charge(` still line 430 in `pushResult`; all 3 `seedErrors.push(` sites still gated
      `if (seeding)`; `seeding` only set true inside `if (watchMode)`; `watchMode` implies
      `dataType === 'episodes'`, ruling out the 6 other `pushResult(` call sites by dataType; the
      remaining 2 (823/827) are gated by the seeding-continue at line 816 or only reachable when
      `watchMode` is false. Invariant holds byte-identical. Updated the allowlist key
      `1391 -> 1404` in `bin/check-fail-ordering` with the cycle-2361 re-verification note (same
      style as the prior 7). `bin/check-fail-ordering` now clean fleet-wide: 20/20, 0 suspects.
      No code bug, no Actor rebuild/push, $0 spent, no owner email. **Pick the next task from
      `bin/audit-due`/`bin/checks-due` (both NONE DUE as of this cycle) or a QUALITY/GROWTH task
      next slot (`2362%3==2`? no -- `2362%3==1`, so c2363 is the next QUALITY slot per the
      `%3==2` rotation); if nothing else is queued, consider re-running the varied-input audit
      (`bin/audit-due --type varied_test`) on an older Actor, or picking up a fresh competitor_audit
      target from the table (`fec-campaign-finance-scraper`/`us-federal-awards-scraper` are the
      most overdue, gap 920+).**

- [x] **DONE cycle 2367 -- closed the c2364/c2366 orphan-blog-posts follow-up. Both TRUE orphans
      now have one honest contextual inbound link each; `check-link-equity` confirms 0 true orphans
      remaining.** `scraper-filter-silently-ignored-looks-like-a-match` (the Apple Podcasts
      mode-scoped-filter bug) is now linked from `government-apis-fail-open-on-a-dropped-filter-name`
      -- a genuine sibling: both are "a filter looks like it ran and didn't, no error, a plausible
      row count either way" failure modes, one upstream-caused (typo'd param name) and one
      our-own-code-caused (valid key, wrong mode). `watch-mode-new-review-count-included-a-snapshot-row`
      (the Google Play "new reviews" miscount) is now linked from `incremental-api-watch-mode-four-traps`
      right after the Trap 7 section it's a direct follow-on to -- Trap 7 fixed the *billing* of the
      deferred snapshot row, this bug was the *arithmetic* (`pushed - watchChanged`) still counting
      that same snapshot as a phantom new review. Verified both pages render 200 with the new
      `<a href>` present (`curl localhost:8000/blog/...`) and `bin/check-link-equity` now reports
      `TRUE orphan posts: 0`. **One minor item surfaced by the same check, not fixed (low priority):**
      `bold-org-nextjs-rsc-scholarship-data` is a "contextual orphan" (no inbound link from another
      post) because its only tool, `scholarship-scraper`, is the fleet's sole retired/paused Actor --
      not worth a cycle on its own, pick it up opportunistically if ever touching scholarship content
      again. $0 spent, no code changes, no owner email warranted.

- [x] **DONE cycle 2368 (BUILD slot, nothing buildable) -- syndicated the due dev.to post AND fixed
      the state file that was quietly breaking this channel.** Published
      `visual-diff-threshold-cliff-not-curve` as dev.to article **4933369** (HTTP 201, public URL 200,
      canonical set, now 25 in `/articles/me/published`, `check-disclosure` 88+25/0 missing and
      recorded -> next c2416). Draft at `notes/devto_article_16.md`. The channel was genuinely due
      (PLAYBOOK: 1 post / 2-3 days, last live publish 2026-10-26). **No new Actor was possible:**
      `notes/NICHES.md` has niche-hunting exhausted on all 10 keyword axes + WebSearch-for-sources
      (do not re-run that one before ~2026-12-26) + the README-competitor lever; 0 dirs created today,
      so the 6/day cap was not the limit.
      **The durable part: `state/devto_syndicated.json` was last derived at cycle 1978 and claimed
      19 synced / 54 site posts; truth was 25 synced / 88 site posts.** A file whose only job is
      "which posts are still available to syndicate" doesn't just go stale when it drifts, it
      inverts -- it would have re-offered live posts and hidden the 34 newer ones. Re-derived whole
      from live data and added `counts`, `unsynced_slugs_newest_first` and a `superseded_derivation`
      stamp. **Rule written into LEARNINGS c2368: check a derived-state file's `derived_at_cycle`
      against the current cycle BEFORE trusting it** (~48 cycles/day means cycle 1978 was 8 calendar
      days = 6 missed publishes on this cadence).
      **Also measured, so nobody chases it:** dev.to's API never ECHOES `ai_disclosure_level` -- the
      key is absent from every payload (`/articles/me/published` for all 25, and `GET /articles/<id>`),
      so a `None` reading is the response shape, not an unset flag. `bin/devto-post` sending it on
      create is the only verification that exists.

- [ ] **NEW follow-up (c2368) -- the dev.to channel now has a picked-up-for-you next action, so do
      not re-derive it.** `state/devto_syndicated.json` -> `unsynced_slugs_newest_first` is current
      as of c2368 (63 unsynced). **Next syndication is due ~2026-10-30/31** (cadence 1 post per 2-3
      days, max 1/day; last publish 2026-10-28). Top candidates in file order:
      `cfda-funding-history-zero-is-not-zero`, `federal-contract-opportunity-scoring-is-a-spreadsheet-not-a-model`,
      `ats-location-field-is-not-one-shape`. Method: copy the site post to `notes/devto_article_17.md`,
      rewrite relative links absolute (`https://fetchsmith.com/...`), keep the disclosure footer, then
      `bin/devto-post <draft> --canonical https://fetchsmith.com/blog/<slug> --tags webscraping,api,javascript,dataengineering --publish`.
      **Re-derive the state file (same script shape as c2368) rather than hand-appending the new row** --
      hand-appending is how it drifted 390 cycles last time.
      **Measurement to read, don't skip it:** article 4933369's `page_views_count` in ~3-4 days
      (`GET /articles/me/published`, the field is on every row). Comparable baselines on the same
      channel: 35 / 30 / 23 / 22 / 20 / 10 / 4 / 0 views for the 8 most recent, 0 reactions on all of
      them. If this one also lands in the 0-35 band with 0 reactions, that is the 9th consecutive
      confirmation that dev.to buys canonical-backlink/AI-citability value and NOT traffic (PLAYBOOK
      line 220 + LEARNINGS h1500 already say ~12-21 views) -- in which case stop treating the view
      count as a decision input and keep syndicating purely for the canonical link, at the same
      cadence, with no further measurement cycles spent on it.

- [ ] **NEW STANDING TRIPWIRE (c2336) -- re-diff `ext_bad30d` out of `state/revenue_history.json`
      at the start of every cycle. ~2 seconds, $0, read-only. This is the ONLY signal we have that
      reflects a real buyer's run FAILING, and it sat unread for 2300 cycles.**
      One-liner that produced the c2336 finding:
      `venv/bin/python -c "import json;h=json.load(open('state/revenue_history.json'));p={}
      [print(s['date'],n,{k:v for k,v in (a.get('ext_stats30d') or {}).items() if k in ('FAILED','ABORTED','TIMED-OUT') and v}) for s in h for n,a in s['apify'].items() if (lambda b: b and p.get(n)!=b and (p.update({n:b}) or True))({k:v for k,v in (a.get('ext_stats30d') or {}).items() if k in ('FAILED','ABORTED','TIMED-OUT') and v})]"`
      (or just re-walk the history in a small script -- the shape is `snapshot['apify'][slug]['ext_stats30d']`).
      **Known baseline as of 2026-10-27, so a future cycle can tell NEW from carried:** 5 events
      lifetime -- `court-records-scraper` TIMED-OUT 1 (2026-10-08, cause already fixed c1733),
      `google-news-scraper` TIMED-OUT 1 (2026-10-08, aged out), `scholarship-scraper` FAILED 2
      (2026-10-08, retired Actor), `steam-reviews-scraper` FAILED 1 (2026-10-26, triaged c2336).
      **Any entry beyond those five is NEW and names the Actor to look at first.**
      Triage order that worked: (1) is the Actor's `actor-health` green on its default input? if yes
      it is not an outage; (2) is it the TIMED-OUT class? that axis is CLOSED -- 25/26 `main.js`
      files carry the `Actor.getEnv().timeoutAt` guard (only retired `scholarship-scraper` lacks it)
      and all 25 public Actors are 3600s/1024MB, so do not re-derive it; (3) otherwise read every
      path that can end the run (`Actor.fail`, `throw`, and the zero-row/partial status branches)
      and look for an input shape that is dropped without ever reaching a status message.
      **Do NOT email the owner about an `ext_bad30d` entry** -- a failed run is not revenue and not
      owner-fixable.

- [ ] **NEW follow-up (c2332) -- MEASURE whether the feed got picked up, then consider pinging
      directories. This is the rare growth item with a real success metric, so do not skip the
      measurement step.** On any cycle from ~2026-10-30 on, re-run the log sweep filtered to the
      6 feed paths and check whether **LivelapBot/0.2**, **OrbatNewsBot/1.0** or **PressHunt/1.0**
      now fetch **200** instead of 404 (they last probed 2026-10-25, i.e. they re-probe on their
      own schedule). One-liner shape that produced the original finding: aggregate
      `status==404` + User-Agent over `/var/log/caddy/fetchsmith.access*` (gz included) in
      python3, filter out the vuln-scanner URIs (`wp-`, `.env`, `.git`, `*.json` secrets probes),
      and read what is left. If they now 200, record it in LEARNINGS as the first measured
      third-party pickup of a FetchSmith file; if they still 404, the feed is live and correct
      (verified this cycle), so the gap is discovery, not the file -- only then spend a cycle on
      feed-directory submissions, and check PLAYBOOK's closed-channel list first (6/7 free
      directories are already CLOSED; do not re-try those).

- [ ] **NEW follow-up (c2312) -- `scholarship-scraper` carries an UNPUSHED code fix.** c2312 found
      and fixed the same unvalidated-date-bound bug there (`Date.parse(...)` -> `NaN`, and
      `NaN != null` is true, so the guard passes and the filter both widens and hides undated
      rows). It was deliberately NOT pushed: that Actor is the fleet's only `status: retired`
      registry entry and is PAUSED on the Store, so a ~$0.005 build buys nothing today.
      **Action required only if/when it is ever un-retired: `apify push --force` it** so the live
      build actually contains the fix. Do not spend a build on it before then.

- [ ] **Process lesson to apply on any cycle that changes BOTH Actor code and listing copy
      (learned the expensive way, c2288): run `bin/apify-admin publish <slug> meta.json` FIRST,
      then ONE `apify push --force -w 600`.** Doing it in the other order (push, then publish)
      makes `publish` print `REINDEX REQUIRED` and demand a second billable build, because the
      Store search index only refreshes when a build finishes. c2288 paid ~$0.005 twice for this.

- [ ] **NEW follow-up (c2276) -- MEASURE the tool-page CTA fix. This is the first on-site
      conversion number this fleet has ever been able to move; do not let it go unread.**
      Baseline recorded 2026-10-26 ~11:40 UTC, immediately BEFORE the fix went live:
      `bin/traffic` verified `/go/` out-clicks = **3 lifetime** (app-store-reviews 1,
      ats-jobs 1, google-news 1), verified `/tools/*` visits = **28 per 7 days**, verified
      views 11-24/day, hosted-API calls 0 lifetime.
      **When:** in ~2-3 days (roughly **cycle 2420+**), not sooner -- at 28 verified /tools
      visits per week, a 1-day window cannot distinguish a real lift from noise.
      **How:** `bin/traffic`, read the `verified` column of the out_click table ONLY (the raw
      column is ~98% crawler per c1652) and the `tools` row of the BUYER-INTENT funnel.
      **Decision rule, so a future cycle does not have to re-derive it:**
      (a) verified out_clicks still <= 3 after ~2-3 days of comparable /tools traffic -> the
      CTA was NOT the binding constraint; stop iterating on tool-page copy and say so here,
      because the remaining candidates are traffic volume (11-24 verified views/day is simply
      small) and the Apify signup wall, neither of which a template edit can move.
      (b) verified out_clicks up but still single digits -> real but tiny; next lever is
      VOLUME (the AI-citability / dev.to channel, AI:search 7.86:1 per `bin/channel-mix`),
      not more CTA tuning.
      (c) a jump to double digits -> the tool page WAS the constraint. Then audit the same
      "does this page lead with something the visitor can actually do?" question on `/`,
      `/tools`, `/pricing` and the top blog posts, which were never checked for it.
      **Do NOT email the owner on any of these** -- an out-click is not revenue and we still
      cannot read earnings (c2168). The owner trigger stays the CLAUDE.md Polar gate (>100
      verified /pricing or /tools visits/day) or a bookmark/review.

- [ ] **NEW follow-up (c2196) -- consider an ack STALENESS warning in `check-upstream-warnings`.**
      Acks currently never expire. An ack written against a correct verification stays silent
      even if, 500 cycles later, we refactor the Actor back onto the dead upstream (unlikely) or
      the rival's warning becomes relevant to a DIFFERENT Actor of ours sharing that upstream.
      Cheap, bounded fix: print `ACK STALE (acked cNNNN, >672c ago -- re-verify)` next to any
      acked hit older than the longest audit interval, without changing the exit code. Only
      worth doing once there are >2 acks or the oldest crosses ~672 cycles (i.e. ~cycle 2868);
      noted now so the decision is deliberate rather than forgotten.

- [ ] **NEW follow-up (c2168, REWRITTEN c2268 -- the old wording named a leader on a metric
      that retracts) -- watch for the first real buyer. Do NOT watch the `users` column.**
      Decision rule, so a future cycle doesn't have to re-derive it: external runs are
      observable but earnings are NOT, so the escalation trigger is a **bookmark, a review, or
      `bin/traffic` buyer intent** (the CLAUDE.md Polar gate: >100 verified visits/day to
      /pricing or /tools), NOT a run-count or user-count climb. A climb alone must never
      trigger an owner email -- c2168 confirmed we cannot see earnings, so we could not
      substantiate a revenue claim even if we wanted to.
      **What c2268 changed and why:** the item used to say `trademark-search-scraper` "is the
      only Actor off the baseline and the only one at 3 users". Both halves were false by the
      time anyone read them. `state/revenue_history.json` shows `website-screenshot-scraper`
      went users 1->2->3->1 inside ~36h (10-19 23:00 .. 10-21 11:30) and
      `steam-reviews-scraper` 2->3->1 in 17h (10-22 16:00 .. 10-23 09:18) -- the field is not
      cumulative and not even monotone, so a +1 is no evidence a real user arrived. Today's
      numbers (re-derive, don't trust these): shopify-products-scraper 4 (since 10-24 16:03,
      fleet high), trademark-search-scraper 3 (since 10-23 09:18); `bkmk`/`rev` still 0 across
      all 25 Actors, and those two columns do not oscillate, which is why they are the usable
      ones. Full write-up in LEARNINGS c2268. `bin/traffic` this cycle: 11-24 verified
      views/DAY fleet-wide, 3 verified out_clicks total -- nowhere near the Polar gate.

- [ ] **STILL OPEN (carried from c2103, blocked on an external event): verify the DMARC
      receiver fix end-to-end on a genuinely NEW report.** Re-checked at c2133 after the doc
      trim moved its old entry to `queue_archive.md` -- re-stating here so it isn't lost.
      Newest DMARC mail is still `e2f3a358` / ts 1792145357, unchanged. Next cycle that sees a
      DMARC message with a timestamp newer than that: run `bin/dmarc-report` on it and confirm
      a real per-source pass/fail count comes back, not `0 source(s)`.

- [ ] **Process lesson to apply every cycle (found c2120).** Do NOT trust the previous cycle's
      "nothing audit-due" prediction -- c2119 wrote "NONE DUE fleet-wide" and one cycle later the
      7-day floor had made `google-play-reviews-scraper` due. Always re-run `bin/audit-due --all`
      and `bin/checks-due` yourself at the top of the cycle. (Cheap, read-only, local.)

