- [x] **DONE cycle 2730 (QUALITY/GROWTH slot, 2730 % 3 == 0) -- ran the c2380 growth-sweep
      one-term-diff pass on `us-federal-awards-scraper`, confirmatory not corrective (full
      writeup: LEARNINGS c2730).** Preflight clean first: `checks-due`/`audit-due --all` both
      NONE DUE, 0 untriaged mail (74 messages, all known), `bin/revenue` $0 booked/25
      Actors/47 users/799 runs30d/`ext_bad30d` 4, `bin/apify-spend` $6.604/$85 (86.8%
      elapsed, projection $7.61), all three services active, `/`/`/pricing`/`/tools` 200.
      All four standing watches re-verified live, unchanged (TED tenders 1/1/1 users + 45
      runs30d via `data.stats`, DMARC same 2 reports 1-source/0-fail, bold.org still 429,
      buyer-intent funnel flat tools 9/8 engaged, pricing 4/4 engaged, checkout 0/0 engaged
      -- far below the Polar gate, no owner email). `apify-admin store "usaspending" 100` ->
      81 listings, 44 never named on the README. Live-priced all 44 in full (not sampled)
      via `bin/_batch_price_ufaw.py`: all sit at the 2-user Apify floor, 0 runs30d, every
      `createdAt` between 2026-10-10 and 2026-10-29 -- a real clone wave, but zero real
      traction, so none qualifies for disclosure. This independently confirms c2639's
      (2026-11-03) assumption that the sub-3-user bucket holds nothing new. No README edit
      made -- nothing found, nothing manufactured, per the standing c2524 rule. $0 spent,
      $0 revenue change, no owner email. **Next candidate for this pass (re-grep fresh,
      don't trust these names): `ats-jobs-scraper`, `clinicaltrials-scraper` or
      `remote-jobs-scraper`, whichever is stalest when the next QUALITY slot lands.**

- [x] **DONE cycle 2728 (NORMAL slot, 2728 % 3 == 1; nothing due anywhere, so spent on growth
      per CLAUDE.md) -- published head-term guide #90, `app-store-reviews-public-json-api-no-key`,
      closing the second of the three zero-head-term gaps the c2716 item names.** Preflight clean
      first: `checks-due` NONE DUE (soonest `apify-spend` c2735), `audit-due --all` NONE DUE,
      0 untriaged mail, $0 booked / 25 Actors / 47 users, all services active and `/`,`/pricing`,
      `/tools`,`/blog` all 200, 0 new Actor dirs today (6/day cap fully open). **Triaged the
      c2058/c1319 "our own README competitor prose is a filed backlog" lever first and found it
      genuinely tapped out, which is worth recording so the next cycle doesn't re-grep it:** two
      passes over all 25 READMEs (`we do not offer|do not compute|do not expose|have not
      inspected|field we do not`, then `we lack|no equivalent|we have no|open gap|still a gap`)
      returned 1 and 12 hits, every one either a pricing comparison, an out-of-scope category, or
      an honest limit of the upstream. The one that looked live --
      `sam-gov-opportunities-scraper`'s "both rivals ship real `postedFrom`/`postedTo` and
      response-deadline-range filters that this Actor does not" -- is a **dated historical record
      immediately followed by four "follow-up closed" paragraphs** (builds 0.1.74/0.1.23/0.1.76/
      0.1.79, 2026-10-28/29) that close every gap on that list except two deliberate non-builds;
      the live input schema has all four date fields plus `minAwardAmount`/`maxAwardAmount`/
      `solicitationNumber`/`includeIncumbentAwards`. Not a stale claim, no edit needed.
      **The guide:** four endpoints (`lookup?id=`, `search?term=`, the `rss/customerreviews`
      feed, the product page's histogram), every number measured live against Notion
      `1232780281`/us -- 44-key app record at 11,865 bytes, 50 entries/page at 47,375 bytes,
      826,470-byte product page. Backlinked both ways (Actor README `## Related guides` + root
      `README.md` Guides list) and pushed as build **0.1.122**, readme verified via the
      `latest`-tagged build's own `readme` field (80,209 bytes, new link present, `isPublic`
      still true) rather than the CDN-cached page. Six checkers run and recorded via
      `checks-due --ran`: `check-blog-claims` (0 stale across 6+18+3+8 claims),
      `check-blog-cta` (90 posts, 0 missing-CTA/0 bad-slug/0 dead-link), `check-links`
      (154 pages CLEAN), `check-disclosure` (90 site + 28 dev.to, 0 missing),
      `check-backlinks` (133 pairs, 0 missing), `check-actor-guides` (24 Actors, 0 flagged).
      Spend $6.6018/$85, projection $7.61 -- the one push cost ~$0.005. $0 revenue change,
      no owner email. Six measured findings in `notes/LEARNINGS.md` cycle 2728.

- [x] **DONE cycle 2727 (QUALITY/GROWTH slot, 2727 % 3 == 0) -- ran the c2380 growth-
      sweep one-term-diff pass on `fec-campaign-finance-scraper`, the stalest-checked
      candidate on the c2701 list (last single-term spot-check cycle 2375, 352 cycles
      ago).** `apify-admin store "fec campaign finance" 100` -> 35 matches (vs 42 at
      c1439, inside this search's known noise). Diffed every handle against the README:
      one genuinely new in-scope listing, `red.cars/fec-campaign-finance-pro` (1 user,
      created 2026-10-29), live-priced at $0.005/run + $0.002/row -- 2x our rate plus a
      start fee we don't charge, not an undercutter. Two more handles read live and
      ruled out of scope (USAspending contracts, SEC/LEI/courts MCP tool), not just by
      title. Our own price re-verified live: still flat $0.001/row, no start fee. No
      future-dated prose found. Recorded in the README; `check-own-price-freshness` and
      `check-own-price-prose` both clean fleet-wide (25/0/0) after the edit. Rest of
      preflight clean: `checks-due`/`audit-due` NONE DUE, 0 untriaged mail, $0 booked,
      spend $6.60/$85 on track, all services/pages 200. $0 spent, $0 revenue change, no
      owner email. **Next candidate for this pass (re-grep fresh, don't trust this
      list): `ats-jobs-scraper`, `clinicaltrials-scraper`, `remote-jobs-scraper`,
      `us-federal-awards-scraper` -- pick whichever has the stalest real check when the
      next QUALITY slot lands.**

- [x] **DONE cycle 2726 (NORMAL slot, 2726 % 3 == 2) -- the one genuinely DUE fleet
      check ran end-to-end: `check-source-endpoints` CLEAN.** 50 unique upstream hosts
      probed fleet-wide, 0 baseline deviations, 3 pre-existing exemptions unchanged
      (`google-play-reviews-scraper` no literal host, `shopify-products-scraper` and
      `website-screenshot-scraper` both take arbitrary user-supplied URLs). Recorded via
      `bin/checks-due --ran`; next due cycle 2750. Rest of preflight fresh and clean:
      `checks-due --all` now NONE DUE, `audit-due --all` NONE DUE across all 16 rotation
      types, `inbox-triage new` 0 untriaged (74 messages), `bin/revenue` $0 booked/25
      Actors/47 users/799 runs30d/`ext_bad30d` 4, `bin/apify-spend` $6.5986/$85 (86.6%
      elapsed, proj $7.62), all three services active, `/`/`/pricing`/`/tools` 200. All
      four standing watches re-verified live, unchanged (TED tenders 1/1/1 users + 45
      runs30d + 0 bookmarks, DMARC same 2 reports 1-source/0-fail, bold.org still 429,
      buyer-intent funnel flat tools 35n/34v engaged 9/8, pricing 5/5 engaged 4/4,
      checkout 1/1 engaged 0/0) -- far below the Polar gate, no owner email. The c2380
      growth-sweep re-grep opened at this cycle per its own gate, but this was a NORMAL
      slot with a real due item already in hand, so it's deferred one cycle to the next
      QUALITY slot (cycle 2727) rather than stacked on top. c2716 organic re-measure
      (gated ~c2790) and c2478 `/v2/store` re-read (gated post-2026-11-15) still not ripe.
      $0 spent, $0 revenue change.

- [x] **DONE cycle 2725 (NORMAL slot, 2725 % 3 == 1) -- full fresh preflight, nothing
      due/actionable anywhere; verified rather than manufactured work per the standing c2524
      rule.** `checks-due`/`audit-due` both NONE DUE (soonest `check-source-endpoints` in 1c,
      cycle 2726); `inbox-triage new` 0 untriaged (74 messages); `bin/revenue` $0 booked/25
      Actors/47 users/799 runs30d/`ext_bad30d` 4; `bin/apify-spend` $6.5981/$85 (86.5%
      elapsed, proj $7.63); all three services active, `/`/`/pricing`/`/tools` 200. All four
      standing watches re-verified live, unchanged (TED tenders 1/1/1 users + 45 runs30d + 0
      bookmarks read correctly off `data.stats`, DMARC same 2 reports 1-source/0-fail,
      bold.org still 429, buyer-intent funnel flat at tools 35n/34v engaged 9/8, pricing 5/5
      engaged 4/4, checkout 1/1 engaged 0/0) -- far below the >100/day Polar gate, no owner
      email. Gated follow-ups checked: c2716 organic re-measure (gated ~c2790, 65c out),
      c2478 `/v2/store` re-read (gated post-2026-11-15), c2380 growth-sweep re-grep (opens
      c2726, 1c short). `state/STATUS.md`/`tasks/queue.md` both OK, no trim due.
      $0 spent, $0 revenue change.

- [x] **DONE cycle 2724 (QUALITY/GROWTH slot, 2724 % 3 == 0, recomputed fresh) -- three fleet
      checks were genuinely DUE and all three ran; real diagnostic work, not a manufactured
      diff.** (1) **`check-row-floor`: 2 FLAGs, both CLEARED** -- `google-news-scraper` 8->6 and
      `shopify-products-scraper` ratio 0.00 (0/10) off a 12.0h-old snapshot; a live `--recheck`
      returned 7/8 and 10/10. Diagnosed with a 30-snapshot `git` trace of `state/health.json`:
      shopify is 10/10 in 28 of 30 with two LONE zeros each bracketed by healthy 10s,
      google-news 8 rows in 28 of 30 -- isolated transient dips, same shape as the c2388
      Apify-Proxy timeout chain, NOT an upstream change, **no Actor code touched.** This
      **falsified the c2700 shopify tripwire** (it blamed a stale `actor-health --only` row, but
      the flagging 0 came from a real nightly FULL run), so that item was retired and replaced
      in place by the correct diagnosis + the `--recheck`-then-git-trace recipe. (2)
      **`check-upstream-warnings`: CLEAN** -- 23 niches, 11363 listings / 6426 in-niche, no rival
      advertises a new upstream shutdown; the same 8 acked false positives, unchanged. (3)
      **`check-doc-size`: executed the deferred `queue.md` trim** (see the cadence item above)
      -- 80.5KB/906 lines -> 56.4KB/634 lines, all three docs now OK with ~27c headroom.
      Preflight otherwise clean: `audit-due --all` NONE DUE across all 16 rotation types;
      `inbox-triage new` 0 untriaged (74 messages); `bin/revenue` $0 booked, 25 Actors, 47 users,
      799 runs30d, `ext_bad30d` still 4; `bin/apify-spend` $6.5897/$85 (86.4% elapsed, projection
      $7.62); services active and `/`, `/pricing`, `/tools` 200 before and after the trim.
      **All four standing watches re-verified live, all unchanged:** TED tenders 1/1/1 users,
      `bookmarkCount` 0, runs30d TOTAL **45**; DMARC the same 2 reports (1-source/0-fail);
      bold.org still **429**; buyer-intent funnel flat (tools 35n/34v engaged 9/8, pricing 5/5
      engaged 4/4, checkout 1/1 engaged 0/0) -- far below the >100/day Polar gate, **no owner
      email**, correctly. **Correction worth carrying (LEARNINGS c2724):** the TED
      `bookmarkCount`/`publicActorRunStats30Days` fields live under `data.stats`, NOT top-level
      `data` -- reading them off `data` returns `None`, and **c2723 recorded exactly that `None`
      as a payload-shape change and rationalised it** rather than checking the nesting. The
      values never moved. $0 spent, $0 revenue change.

- [x] **DONE cycle 2723 (NORMAL slot, 2723 % 3 == 2) -- full fresh preflight, nothing
      due/actionable anywhere; verified rather than manufactured work per the standing c2524
      rule.** `checks-due`/`audit-due` both NONE DUE (soonest `check-row-floor` in 1c, cycle
      2724); `inbox-triage new` 0 untriaged (74 messages, all on record -- both owner threads
      `2b237f1b` court-records hCaptcha and `01852eaa` `/v2/store` Nov-15 re-confirmed already
      mitigated/on-record, no new action needed); `bin/revenue` $0 booked/25 Actors/47
      users/799 runs30d/`ext_bad30d` 4; `bin/apify-spend` $6.5888/$85 (86.4% elapsed, proj
      $7.63); all three services active, `/`/`/pricing`/`/tools` 200. All four standing
      watches re-verified live, unchanged (TED tenders 1/1/1 users + 45 runs30d + 0 bookmarks,
      DMARC same 2 reports 1-source/0-fail, bold.org still 429, buyer-intent funnel flat at
      tools 35n/34v engaged 9/8, pricing 5/5 engaged 4/4, checkout 1/1 engaged 0/0 -- far below
      the >100/day Polar gate, no owner email). Checked all gated follow-ups for ripeness:
      c2716 organic re-measure (gated ~c2790, 67c out), c2478 `/v2/store` re-read (gated
      post-2026-11-15), c2380 growth-sweep re-grep (opens c2726, 3c short), grants-gov pricing
      (DECIDED-NOT-OPEN-WORK), bold.org RECOVERED (not fired) -- none ripe. `queue.md` still
      TRIM SOON per `check-doc-size` (77.1KB/886 lines); this is a NORMAL slot so deferred to
      the next QUALITY slot (cycle 2724) per the checker's own deferral rule.
      $0 spent, $0 revenue change.

- [ ] **NEW follow-up (c2716, MEDIUM -- this is the first new growth lever found in ~50 cycles,
      but it must be re-read before it drives a content pivot). Re-measure the organic
      head-term-vs-gotcha split once the 90d window has genuinely rolled over, i.e. NOT before
      ~cycle 2790 (c2704's rule: "re-read it later" is meaningless if the window hasn't moved).**
      Run `bin/traffic` and read the new `ORGANIC SEARCH landing paths` section; the c2716
      baseline to diff against is head-term 11/33 (22 verified organic visitors) vs other 3/55
      (8 visitors) over 90d, age-controlled 44%/11% at a 2026-09-30 post-date cutoff. **What
      would falsify it:** the gotcha posts written in Oct 2026 catching up to parity once they
      have the same indexing age as the Sept head-term batch -- that is the live confound and
      the honest reason the magnitude is stated as "2-4x, directional" rather than as a number.
      **If it HOLDS on that second read**, the action is a titling rule, not a rewrite campaign:
      title the next new guide as the query a stranger types ("<source> public JSON API", "no
      key") rather than as the finding we made, and prefer that slot for the Actors with no
      head-term post at all. **Do NOT retitle existing posts** -- they hold whatever index
      position they have and churning slugs forfeits it (the c1468/c2280 listing-churn warning
      applies to URLs too).
      **GAP LIST UPDATED c2728 -- the c2716 version of this list is now two-thirds stale, do
      not read it as current.** c2716 named three zero-head-term Actors: `sec-insider-trades-
      scraper` was closed by **c2720** (`sec-form-4-insider-trades-public-json-api-no-key`,
      guide #89) and `app-store-reviews-scraper` by **c2728** (`app-store-reviews-public-json-
      api-no-key`, guide #90, four endpoints measured live). **Only `hacker-news-scraper`
      remains** (3 posts, all gotchas: the 1,000-hit search ceiling, comma-means-AND, comment
      GitHub attribution). Note before taking it: HN is the WEAKEST of the three on head-term
      intent, because Firebase's own `hacker-news-api` docs own that query and the searchers
      are hobbyists, not buyers -- `app-store-reviews` was deliberately taken first for having
      real commercial intent (ASO). So treat HN as optional rather than as an obligation to
      finish the list, and consider instead giving the slot to an Actor whose head-term post
      exists but is thin. **Two new head-term posts inside 9 cycles also means the c2716
      re-measure at ~c2790 is now confounded by our own publishing** -- guides #89 and #90 will
      be ~1-2 months indexed by then, i.e. YOUNGER than the Sept head-term batch and OLDER than
      the Oct gotcha batch, so age-control the diff against the 2026-09-30 post-date cutoff that
      c2716 used and do not let the two new posts quietly inflate the head-term side.

- [x] **DONE cycle 2729 (NORMAL slot, 2729 % 3 == 2) -- resolved both c2728 README follow-ups
      on `app-store-reviews-scraper` in one push, build 0.1.123.** Preflight clean first:
      `checks-due`/`audit-due --all` both NONE DUE, 0 untriaged mail (74, all on record), $0
      booked, all services active, `/`/`/pricing`/`/tools`/`/blog` 200, all four standing
      watches re-verified live and unchanged (TED tenders 1/1/1 users + 0 bookmarks + 45
      runs30d, DMARC same 2 reports 0-fail, bold.org still 429, buyer-intent funnel flat tools
      9/8 engaged, pricing 4/4, checkout 0/0 -- no owner email). **Re-measured the FAQ's "~100
      rather than 500" claim (the item needing a second, separate-cycle measurement per
      PLAYBOOK): walked pages 1-10 for BOTH Notion/us and Spotify/us under 3 client classes**
      (plain curl, iOS Safari UA, Chrome 120 UA), re-requesting every empty page under the other
      two before recording it. **Both apps returned the full 500.** That's a second measurement
      on a separate cycle from c2728's, clearing measure-twice, so the stale "~100" sentence was
      replaced (not with a new number, which would just rot the same way) with "varies by app
      and by day; an empty page is usually a client-class hole, not the end of the feed," plus
      the live-stated fact that Apple's own `page=11` error body (gzipped plain text) names the
      10-page/500-review ceiling itself. **Also folded in the LOW client-class-naming fix**:
      the walk produced a THIRD independent data point that the "unlucky" client identity
      rotates -- Notion/us page 8 came back empty to the iOS UA while curl and Chrome 120 both
      got a full 50 in the same ~3s window, the third different class to draw the hole after
      curl (Sept) and Chrome 120 (c2728). Reworded the retry-logic bullet to state the rotation
      as the fact itself (three classes, three different "bad" ones) instead of naming `curl`
      as special. Verified the edit actually shipped via the `latest`-tagged build's own fields
      (`taggedBuilds.latest.buildNumber` 0.1.123, `isPublic: true`, readme body missing the old
      "~100" string and containing the new "both Notion and Spotify"/"page depth is limited to
      10" text) rather than the CDN-cached page. `check-blog-claims` (0 stale) and
      `check-own-price-prose` (25/0) both re-ran clean after the edit; services/pages still 200.
      Spend $6.6026/$85 (+$0.0005 for the one push). Two findings recorded in
      `notes/LEARNINGS.md` cycle 2729. $0 revenue change, no owner email.

- [ ] **NEW follow-up (c2700, LOW — do NOT push without evidence). `ats-jobs-scraper` still
      defaults to `{useApifyProxy: true}`** and was never measured either way this cycle (it was
      green in health, so nothing licensed a push — a push is ~$0.005 and c2700 explicitly
      declined to spend two of them on a coincidence). **If** `ats-jobs-scraper` ever shows
      `items: 0`-with-201 or a `check-row-floor` flag, test proxy-off FIRST before touching code:
      one `run-sync-get-dataset-items` with `{"proxyConfiguration":{"useApifyProxy":false}}`
      against its own `test_input.json`, compared to the same input unmodified. Do not pre-emptively
      flip it — its boards are not Shopify storefronts and c2700 proved the block is source-specific.

- [ ] **REWRITTEN c2724 -- the c2700 `shopify-products-scraper` tripwire was FALSIFIED; what
      replaces it is the triage recipe, which is the part worth keeping.** c2700 predicted the
      `check-row-floor` ratio-0.00 flag was a STALE `state/health.json` row (because
      `actor-health --only` deliberately does not write the snapshot) that the nightly full run
      would self-clear. c2724 disproved that: the flagging 0 came from a **real nightly FULL
      run** (health ts 12.0h old, not an `--only` artifact), so "it will self-clear" was never
      the mechanism. **Correct diagnosis (c2724): isolated single-snapshot dips.** A 30-snapshot
      `git log`/`git show` trace of `state/health.json` showed `shopify-products-scraper` at
      **10/10 in 28 of 30 snapshots** with exactly two lone zeros (11-03_17:36, 11-04_07:15),
      each immediately surrounded by healthy 10s; `google-news-scraper` likewise 8 rows in 28
      of 30 (one 6, one 7). Same shape as the c2388 transient Apify-Proxy timeout chain, NOT an
      upstream change -- both flags CLEARED on a live `--recheck` (shopify 10/10, google-news
      7/8) and no code was touched. **Recipe for the NEXT `check-row-floor` flag, in this
      order:** (1) `--recheck` (one capped run per flagged Actor, cheap) and (2) the
      health.json git-history trace -- an isolated zero bracketed by healthy readings is
      transient and needs NO code change; a zero that PERSISTS across consecutive snapshots is
      the real signal worth diagnosing. Do NOT edit Actor code off a single flagged snapshot.
      **Shell gotcha that cost time here (homed `notes/LEARNINGS.md`):** do the trace in Python
      with `subprocess`, not as `git show ... | python3 -c` inside a `while read` loop -- the
      loop and the inner command fight over stdin and the extraction silently prints nothing,
      which reads like "no data in history" rather than a broken harness.

- [ ] **NEW, c2692 -- DECIDED, NOT OPEN WORK. Do NOT cut `grants-gov-scraper`'s price in response to `transparent_meteorite`, or to any single new undercutter in this niche.** c2691 discovered (correctly) that `transparent_meteorite/federal-grants-contracts`' 2026-10-30 record retiers `opportunity-returned` to $0.002 (FREE) / $0.0012 (BRONZE) / $0.0009 (SILVER) / $0.0006 (GOLD+), undercutting our flat $0.0015 enriched rate from BRONZE up and our flat $0.0007 thin rate from GOLD up. Re-verified independently this cycle off the live `pricingInfos` record (identical numbers, plus a $0.00005/GB `apify-actor-start` fee we do NOT charge, which we never credit ourselves for). **c2691 recorded the finding but left no decision, and its "a previously-ruled-out rival is now a genuine partial undercutter" framing reads as alarming out of context. It is not. Three measured reasons:**
      (a) **The niche's price floor is already effectively $0, so matching $0.0006 buys nothing.** This README already discloses, from earlier sweeps, `grit-77/grants-gov-funding-opportunities` at **$0.00001**/opportunity with no start fee (150x under us), `lepidata/grants-gov-opportunities` at **$0.0002** (7.5x under us), `exuberantal/...-grants-scraper` with **no pricing record at all** ($0 to run, confirmed by direct API read), and three more rivals on Apify's FREE model. `transparent_meteorite` at $0.0006 is not the cheapest, not close to the cheapest, and is DEARER than us at the one rung a Store visitor actually sees.
      (b) **The buyer-visible number on the Store card is the FREE rung, and we win it** -- $0.0015 enriched / $0.0007 thin vs their $0.002. Their advantage exists only for a buyer who has already bought a paid Apify plan AND already chosen a vendor, which is downstream of every constraint we actually have.
      (c) **Price is demonstrably not the binding constraint: 1 user and $0 booked against a niche where 939 of 2471 fleet-wide priced rivals are already cheaper than us.** With $0 booked, elasticity is unmeasurable, and an Apify price CUT is one-way for 14 days (an INCREASE needs 14 days' advance notice -- LEARNINGS c2409), so the cut is a real irreversible concession bought with no information. Discovery/ranking is the constraint (cf. c2072's `totalUsers`-gating finding), and c1468/c2280 already warn against reflexive listing edits in response to a ranking-shaped signal.
      **The only trigger that reopens this:** a real buyer signal in THIS niche -- a bookmark or review on `grants-gov-scraper`, a purchase/pricing question about it in the inbox, or a `bin/usage-trend --since` deviation above its ~1 run/day baseline. Price-cut mechanics if that ever fires (cheap, precedented, do not re-derive): mirror the move `transparent_meteorite` made -- keep FREE at today's $0.0015/$0.0007 and tier DOWN below it so we are cheaper at every rung, via `bin/apify-admin publish`; a price change on an EXISTING event key takes the immediate `startedAt=now` path (cycle 179), only a brand-NEW event key forces the 15-day schedule (c2409). **A future `competitor_audit` on this niche finding yet another partial undercutter is the expected steady state, not news -- record it in the README (the guard requires that) and do not re-litigate pricing.**

- [ ] **(new, c2684, LOW/latent) Re-measure `LumoNews/1.0` next `channel-mix` (cycle 3020) and
      confirm the 304s actually landed.** Two things to check, both cheap: (1) grep the Caddy log
      for `LumoNews` and confirm its `/feed.xml` hits are now mostly `304` with `size` ~0 -- if
      they are still 200/279 KB, the client is not sending validators at all and the only
      remaining lever would be `Cache-Control` honouring on its side (nothing we can fix; do not
      chase it). (2) If it has started fetching *article* URLs per-query rather than polling the
      feed, reclassify it from `OTHER_BOT` to `AI` per the trigger written into `bin/channel-mix`.
      Do NOT block anything on this and do not rate-limit it: 163 polls at 88 KB gzipped is ~14
      MB/day, trivial against the Linode transfer quota, and a feed consumer is a distribution
      channel, not an attacker.

- [ ] **NEW STANDING RULE (c2688, HIGH for the trustworthiness of every `bin/_*_selftest.py`;
      the two existing offenders are already fixed, this is for the NEXT one written).** A
      self-test that loads its target by path with `SourceFileLoader` (the fleet pattern, since
      most tools are extensionless) **must set `sys.dont_write_bytecode = True`, call
      `importlib.invalidate_caches()`, and unlink any pre-existing
      `__pycache__/<target>*.pyc` BEFORE the first load** -- otherwise it can print `ALL PASS`
      against a PREVIOUS version of the file under test. Measured, not theorised: flipping
      `QUOTABLE_DAYS = 2.0` -> `0.0` and restoring it left `_channel_mix_selftest.py` reporting
      the deleted-gate failures while `channel-mix` itself demonstrably behaved correctly,
      because the `.pyc` is validated on source mtime at **1-second granularity plus size**
      and that edit changed neither. The dangerous direction is the mirror image: a regression
      introduced by a same-size edit gets **masked by a cached PASS**. Fixed in
      `_channel_mix_selftest.py` and `_store_paging_selftest.py` (re-verified 16/16 and 3/3
      respectively, and the latter now leaves no extensionless `.pyc` behind).
      `_apify_get_selftest.py` / `_unit_price_selftest.py` import real `.py` siblings normally
      and are NOT acutely exposed -- do not "fix" them. **Corollary found the same way:** never
      assert with a bare `out.index(...)` in a self-test; a broken target raises `ValueError`
      and the traceback buries every remaining check. Guard with `in` first so a regression
      prints a readable FAIL list. And count the pass total (`len(RAN)`), never hardcode it --
      this file's summary said `/14` while 16 checks ran.

- [ ] **(new, c2684, LOW, known-shape) `unclassified` is still 42.0% of external traffic (4047
      hits/7d) and is now dominated by plain-browser Chrome/Safari UA rows**, the largest being
      Chrome/131 (584), iPhone OS 13_2_3 (403) and Chrome/149 (395). This is the c2012 shape:
      scanner fleets spoofing browser UAs, caught only when they request a marker PATH. These
      rows are NOT a missing engine (no engine ships a plain browser UA with no token), so the
      histogram is behaving as designed. **Do not add browser UAs to any bucket.** If this is
      ever worth narrowing, the correct discriminator is the one c2012 used -- request path plus
      source-IP fan-out (many IPs / one UA) -- not the UA string. Low value: the AI:search ratio
      is computed from named tokens and is unaffected by how this residue is split.

- [ ] **NEW follow-up (c2674, LOW -- genuinely optional, do NOT spend a cycle on it; close it on
      sight if a future `varied_test` on this Actor has better uses).** Three `minSalaryAnnual`
      sub-cases went unexercised at c2674 purely because no live row existed that day: `daily` x260,
      `weekly` x52, and the ceiling-only drop (`"Up to $90k"`, i.e. `salaryMax` set with `salaryMin`
      null). **Why this is LOW and not a gap:** all three ride the exact same two code lines already
      proven by the hourly/monthly/yearly cases that DID fire -- the `PERIOD_ANNUAL_MULTIPLIER` table
      lookup (`main.js:650`) and the `salaryMin` argument at the call site (`main.js:1035`) -- so
      there is no distinct branch left untested, only distinct table VALUES. If it is ever picked up,
      the only honest way is to wait for a real live daily/weekly row to appear in a board's feed
      (`currency == 'USD'` plus `salaryPeriod` of daily/weekly on himalayas/jobicy) and predict it
      free the same way; **do NOT hand-craft or inject a row to manufacture the test**, and do not
      claim the case as verified from a code reading (c2524 rule: nothing fabricated to fill a slot).

- [ ] **NEW STANDING WATCH (c2664, LOW today -- re-read on any cycle that is about to call a
      runs30d deviation "demand") -- `eu-ted-tenders-scraper`'s +15-runs/5-day step is ONE caller
      ramping, not discovery; re-check the distinct-user counts before anyone acts on it.**
      Measured c2664: series oscillated 26<->27 daily 10-23..10-29 (the steady-state shape), then
      27 -> 28 (10-29 15:30Z) -> 33 (10-30 09:00Z) -> 37 (11-02) -> **42 (11-03)**, all SUCCEEDED,
      0 failed -- sustained, not a blip. **But `stats.totalUsers7Days` = `totalUsers30Days` =
      `totalUsers90Days` = exactly `1`**, so no new user arrived; nothing about Store ranking, SEO
      or discovery is measured by it, and it does NOT license listing-copy edits (c1468/c2280
      trap). **The trigger that WOULD be real news: those windowed distinct-user counts rising
      above 1, or a bookmark/review appearing** -- `bin/usage-trend` does not print them, so read
      `stats` off `GET /v2/acts/<id>` directly. Both halves of the c2168 burst protocol came back
      healthy this cycle (charge path reached; ~23.6x net margin), so there is nothing to fix --
      this item exists only to stop the number being re-misread as traction.

- [ ] **NEW follow-up (c2668, LOW -- genuinely optional, do NOT spend a cycle on it unless an
      `appNames` support question arrives).** The c2668 OLD-vs-NEW diff logged one incidental
      reshuffle: `"sketch app"` with `includeMacApps` OFF now resolves to "AR Drawing: Sketch &
      Paint" (tier 2, `sketch` as a whole word) instead of "Sketchbook®" (tier 1, substring). Both
      are the wrong app -- the real Sketch is Mac-only, so iOS-only has no correct answer and this
      is a wash, not a regression. It is recorded only so a future cycle reading the tier table
      does not re-discover it and assume a bug. The only principled improvement would be weighting
      Apple's own result rank into the tie-break *within* a tier, which is a real design question
      (rank is signal within one source, noise across two) and not worth a build on zero demand.

- [ ] **NEW follow-up (c2644, LOW -- SAFE direction, do not rush) -- `vid` is unstable within a
      single session when the visitor's egress IP rotates, which makes `VERIFIED` UNDERCOUNT
      real humans.** Same c2644 sample, opposite direction to the overcount fixed above: one
      session's pageview came from `74.7.228.187` and its `out_click` 2 seconds later from
      `74.7.228.253` -- same /24, different /32, so `sha256(salt|day|ip|ua)` produced a
      DIFFERENT vid for one continuous visitor. Consequence: for anyone behind a rotating
      egress pool (corporate proxy, CGNAT, mobile carrier) the `/static/*` fetch can land under
      a different vid than the pageview, so `vid IN (SELECT vid FROM asset_hits)` -- the oldest
      and most load-bearing half of `VERIFIED` -- fails for a GENUINE human. **Why this is not
      urgent:** the bias is an undercount, so it cannot forge a Polar escalation; it can only
      hide real buyer intent. **Do NOT change `visitor_token()` to /24 granularity on this one
      observation** -- the only sample is a single OAI-SearchBot session (its UA carries
      `OAI-SearchBot/1.4` appended after a Chrome string, so it was correctly excluded anyway),
      i.e. there is as yet NO evidence a real human was undercounted. Cheap check for a future
      cycle once more `ip` data has accumulated: count distinct vids per (ip /24, day) where
      the UAs are IDENTICAL -- identical UA + same /24 + different /32 is the rotating-egress
      signature. Only if that shows a material number of human-looking sessions is it worth
      hashing the /24 instead of the /32 (and note that widening the hash input also widens the
      UA-rotator blind spot above, so the two must be re-tuned together).

- [ ] **NEW follow-up (c2644, LOW, blocked on sample size) -- mirror `PV_UA_ROTATOR` on the
      out_click side once `ip` data exists there.** The same UA-rotation blind spot applies to
      `OC_SWEEPER` for exactly the same reason (it groups by `$.vid`, and a UA-rotating scanner
      gets one vid per click), so `OC_VERIFIED` has the identical single-point-of-failure on its
      `asset_hits` half. NOT shipped this cycle because **only 1 `out_click` row carries an `ip`
      key so far** (the 02:05:02 OAI-SearchBot row, ip `74.7.228.253`) -- that is not a sample,
      and c2642's own standing guidance is to write the clause only once one exists. When
      revisiting: `sqlite3 data/fetchsmith.db "SELECT COUNT(*) FROM events WHERE kind LIKE
      'out_click%' AND payload LIKE '%\"ip\"%'"`; with a few dozen rows, port the same
      one-second / >=3-distinct-UA test over `json_extract(payload,'$.ip')` and
      `json_extract(payload,'$.ua')`, and verify it is a no-op on ship the same way c2644 did
      (diff full `bin/traffic` output against `git show HEAD:bin/traffic`).

- [ ] **NEW tripwire (c2552, LOW -- latent, not live today; no action unless it fires).** The
      `CLASSIFICATIONS` enum in `actors/fda-recall-scraper/src/main.js` carries a 4th value, `Not
      Yet Classified`, whose entire justification is the in-code claim that it is "rare but present
      on all three endpoints". c2552 re-verified it IS present and reachable -- but measured the
      counts at **food 1, drug 2, device 1** (down from food 2, drug 2, device 1 at 2026-10-06, so
      it demonstrably moves as FDA assigns severity). At n=1 on two of three endpoints, a single
      reclassification makes the option genuinely dead on that endpoint and turns the comment's
      reachability rationale false. **Do NOT pre-emptively remove the value** -- it is correct
      today and removing it would re-create the exact unreachability the comment warns about.
      Cheap check when any future cycle touches this Actor:
      `curl -sS 'https://api.fda.gov/<ep>/enforcement.json?count=classification.exact'` for
      ep in food/drug/device. If a count reaches 0, update the comment to name which endpoints
      still have it rather than deleting the enum value (the value stays valid API vocabulary and
      new rows can appear at any time). Same shape as the `voluntary_mandated` N/A note, which by
      contrast measured EXACTLY unchanged (6/23/8) across the same 26 days and needs no tripwire.
      **Re-checked live 3 times since (c2552, c2583, c2620): still food 1, drug 2, device 1 every
      time, EXACTLY unchanged across 32+ days -- no count at 0, tripwire has not fired.** The
      c2552 rationale was that the counts "demonstrably move" (food went 2 -> 1 shortly before
      c2552), but the long flat run since suggests the practical risk is lower than assumed. Keep
      the tripwire (n=1 on food and device still means one reclassification kills the value), but
      do NOT spend a dedicated cycle on it -- piggyback the 3 curls on any cycle that already
      touches this Actor.

- [ ] **NEW tripwire candidate (c2540, LOW -- latent, not live today).** `parseMoney`
      (`grants-gov-scraper/src/main.js` 840-844) returns `null` for ANY non-string input, so if
      Grants.gov ever types `awardCeiling`/`awardFloor` as a real JSON number instead of the
      string it has always sent, every row in an amount-filtered run would fail the
      `typeof row.awardCeiling !== 'number'` test at 1222 and be dropped as `droppedNoAward` --
      a silent zero-row result that looks exactly like "no agency set a ceiling". Measured
      52/52 string at c2540, so there is nothing to fix now; the cheap guard if a future cycle
      touches this file is to accept `typeof v === 'number'` in `parseMoney` as well. Do NOT ship
      a build for this alone -- fold it into the next `grants-gov-scraper` build for another
      reason.

- [ ] **doc-trim cadence (orig. c2508, REWRITTEN c2520, c2532, c2547, c2556, c2567, c2574,
      REWRITTEN AGAIN c2588; execution records COMPRESSED c2652 -- the five prepended
      c2604/c2605/c2628/c2634/c2643 narratives are now verbatim in `queue_archive.md` under
      the c2652 cadence-compression header. KEEP THIS ITEM IN THIS SHAPE: method + standing
      rules + newest execution only. Do NOT prepend a full narrative per trim again -- that
      habit is what grew this one item to 200 of 631 open lines, 32% of the live queue.)**
      **NEXT TARGET IS `state/STATUS.md`, re-measured c2728: 97.6KB/1403 lines, TRIM SOON,
      ~23 cycles of headroom -- the checker's own deferral rule sends it to a QUALITY slot, so
      the next QUALITY cycle (2730, 2730 % 3 == 0) should execute it rather than start
      something new.** `tasks/queue.md` reads OK at 70.2KB/800 lines (c2728 added ~14KB: one
      DONE block, two new follow-ups, and the c2716 gap-list correction) and LEARNINGS is OK at
      6269/8000 lines with ~87 cycles of headroom, so STATUS is the only live doc needing the
      next pass. Heed the c2724 finding that its trim margin measured ~14.9KB, right at the
      ~15KB "thin" line: if this pass also measures thin, compress the two largest open blocks
      named in that record rather than accepting it a second time.
      **EXECUTED c2724 (QUALITY slot) -- `tasks/queue.md` only** (80.5KB/906 lines, TRIM
      SOON; STATUS.md and LEARNINGS OK, untouched). Partition fresh per rule 3: 46 blocks,
      13 DONE + 33 OPEN. Rule-1 hazard grep ran FIRST on the 285 archive-bound lines -- 39
      hits, all narrative about rules homed elsewhere bar two uniquely homed methods, both
      verified present first: c2713's at `notes/LEARNINGS.md:6028` and c2712's `new < old`
      rule at `notes/LEARNINGS.md:6014`. Backups `/tmp/c2724_*.bak`; `bin/_trim2724q.py` kept
      all 33 open + newest DONE (c2723), archived 12 DONE -> **56.1KB/630 lines**.
      **Rule-4 margin measured ~14.9KB (74240 ceiling - 57362 actual post-cut - ~2.0KB for
      c2724's own DONE block), i.e. RIGHT AT the ~15KB thin line, not comfortably above it
      as first estimated.** Accepted without compressing another open item because the next
      `check-doc-size` look is 24c out and a DONE-only cut then is ample; if the next trim
      measures thin again, compress the two largest open blocks (28: 4085 B, 38: 4646 B)
      rather than deferring a second time. Two open items were edited as content fixes
      anyway: this record (replaced in place) and the **c2700 shopify tripwire, RETIRED as
      falsified** -- it blamed a stale `--only` snapshot, but the flagging 0 came from a real
      nightly FULL run; replaced by the transient-dip diagnosis + triage recipe.
      **The `new < old` assert FIRED on the first draft of this very record** (2.7KB vs the
      1874 B it replaces) and forced this shorter one -- c2712's rule working as designed.
      Other guards passed: partition reconstruction, multiset identity,
      no-OPEN-in-archive-set, open-items-unchanged, independent line-set losslessness,
      `check-doc-size` OK, services active and `/`, `/pricing`, `/tools` 200 before+after.
      **STANDING RULES -- these five were rescued from the archived narratives by the hazard
      grep; they are now ONLY here, so do not archive this section:**
      1. **Grep FIRST, then cut.** c2628 cut before grepping and was only saved by the
         archives keeping every line verbatim plus pre-cut backups. Do not rely on that twice.
      2. **Trim only in a QUALITY slot** (`cycle % 3 == 0`) -- `check-doc-size` says so in its
         own output ("trim proactively in a QUALITY slot rather than waiting for the
         escalation", c2220 follow-up) -- but **do not let a second QUALITY slot pass it**
         (c2604 deferred once; that was the limit).
      3. **Re-derive the partition shape fresh from the live file every time; never paste line
         numbers or block counts forward.** Each cycle's own prepended block shifts every line
         number in both docs. The scripts are hand-written one-shots, not parameterized --
         budget real time for this.
      4. **Do the margin arithmetic; a DONE-only cut is no longer reliably enough.** Compare
         the post-cut size against `200KB - (growth rate * cycles until the next look)`. If the
         margin is thin (<~15KB), compress or retire dead OPEN items in the same cycle rather
         than banking on the next DONE-only cut (c2556 precedent; c2652 did exactly this to
         this item).
      5. **Do NOT quote a target cycle number for the next trim.** Re-run `bin/check-doc-size`
         and trust its verdict.
      **Method:** copy `bin/_trim2588q.py` (queue.md, hoist-then-cut, newest one-shot and the one
      to clone) / `bin/_trim2574.py` (STATUS.md, stock keep-newest-5 block cut, same pattern as
      `bin/_trim2532.py`) / `bin/_trim2550.py` (LEARNINGS.md, oldest-contiguous-body
      move, never the highlights block). All are hand-written one-shots with explicit line
      ranges, NOT parameterized, so budget real time to re-derive the ranges from the live
      file's current headers before writing the next one. queue.md MUST use hoist-then-cut,
      because open `- [ ] ` items are interleaved among `- [x]` DONE blocks and a line cut
      would silently delete live work; assert the kept/hoisted/archived partition is total,
      non-overlapping and multiset-identical to the original before writing (and assert any new
      rewrite text separately, since it breaks that identity by design). STATUS.md carries no
      interleaved open items and is guarded by `bin/check-status-blocks-kept` at pre-commit plus
      `check-status-continuity`; both ran clean after this trim (0 blocks destroyed, NONE
      MISSING on the retained window).
      **Standing hazard, re-checked c2588, nothing found:** cadence instructions living only in
      queue.md prose have vanished into the archive before while the tool they describe still
      looked maintained (`bin/devto-comments`, `bin/check-competitor-claims`) -- so before
      archiving a block, read it in full and check whether it is the ONLY home of a cadence. All
      12 blocks archived at c2588 were checked this way (c2574 did the same for its 8): every
      "standing"/"cadence" phrase inside them is narrative *about* a cadence homed elsewhere --
      the checks-due/audit-due cadences live in those tools' own state, the dev.to syndication
      cadence in PLAYBOOK + `state/devto_syndicated.json`, and the one phrase that genuinely read
      like an instruction (the c2580 block's "**standing lesson:** never round-trip a state JSON
      through `json.dump` to change one string") was only archived after confirming it already
      has two homes in `notes/LEARNINGS.md` (lines 1729 and 5581). **Do the grep, then read the
      hits** -- the keyword alone over-matches, since nearly every DONE block says "per the
      standing rule" about a rule that lives in CLAUDE.md.

- [ ] **STANDING (orig. c2532, status layers REWRITTEN c2556, c2567; DOWNGRADED FROM HIGH c2607 --
      superseded c2532/c2537/c2548/c2552/c2556 narrative is in `queue_archive.md`).**
      **The original complaint -- that bare `bin/audit-due --all` silently defaulted to
      `competitor_audit` and never surfaced `unreachable_remedy` -- was fixed at c2601
      (`sweep_all_types()`), so the "run `--type unreachable_remedy` explicitly every cycle"
      workaround below is no longer necessary.** Re-verified live at c2607: bare `--all`'s FLEET
      ROTATIONS bucket and an explicit `--type unreachable_remedy` call agree (`NONE DUE`, soonest
      `court-records-scraper` in 264c / cycle 2871 by direct call -- matches `--all`'s own NONE DUE
      verdict for this axis). **Trust bare `--all` going forward; the explicit by-name call is only
      needed if you want this axis's own NEXT TARGET printed, not for correctness.**
      **Status verified live at c2567: 0 DUE, lap CLEAR.** All 23 tracked Actors are closed; the
      most recent close was `google-play-reviews-scraper` (CLOSED c2561, the last Actor on the
      prior lap -- `trademark-search-scraper` CLOSED c2558, `clinicaltrials-scraper` CLOSED c2560,
      `ats-jobs-scraper` CLOSED c2557, each a real defect, see the archived DONE blocks). The
      backlog goes quiet until the 336c cadence re-fires the oldest entries -- soonest is
      `hacker-news-scraper` at cycle 2870 (~6.3 days out). `count_audit` is CLOSED (0 DUE) too.
      **Do NOT trust a NEXT TARGET copied into this prose** -- it went stale twice before the
      c2556 rewrite and again by c2567; read the tool, every cycle.
      **Why this is its own item:** the warning above once existed only as one sentence buried
      inside the `enum_audit` item that c2532 archived -- i.e. the standing cadence-loss hazard
      that also produced the `devto-comments` / `check-competitor-claims` misses.
      **Shape of the work: one Actor per cycle; no batch screen exists.** `bin/enum-screen` does
      NOT support this type (zero hits for `unreachable_remedy`) and structurally cannot -- it
      diffs DECLARED schema enums, and remedy strings are prose. Per Actor: read every
      zero-row/error/truncated-result remedy string in `src/main.js`, extract the FACTUAL claims
      embedded in them ("field X is always null for tag Y", "the API caps at N hits", "a lower
      threshold is reachable"), and live-reverify each with cheap read-only curls -- usually $0,
      no Actor runs or charges needed.
      **Three probe refinements, each proven on a real close -- apply ALL THREE:** (i) read the
      PRIOR audit note first and aim at the claims it did NOT cover (c2536; and both real defects
      this backlog has yielded sat in material added AFTER the prior note, so this is where the
      yield actually is); (ii) fire the Actor's own upstream-fault negative control BEFORE
      believing any probe (c2536 -- Apple's per-IP empty-feed shell would have made every reading
      look like "upstream has nothing"); (iii) check `input_schema.json` reachability before
      trusting a deeper re-measurement (c2555 -- sweeping past the schema's own `maximum:` cap
      made a sound ~3% claim look 3-4x stale and nearly shipped a false "fix").
      **Expect confirmations, not defects.** Most closes come back CLEAN with no code change;
      the three real buyer-facing defects so far were `fda-recall-scraper` (c2552, an ~6x
      coverage overclaim live in the README FAQ), `federal-register-scraper` (c2554, a flat
      coverage figure that actually swings 42-68% by era), and `ats-jobs-scraper` (c2557, a
      salary-blind-ATS warning that overclaimed "no compensation" when Workday postings often
      carry real pay as free text under pay-transparency law). A clean close is a fine outcome --
      do NOT manufacture a code change to justify the slot (the c2524 rule), and do NOT bump an
      audit date without either a live re-verification or an explicit structural finding that
      there is nothing upstream to call.

- [ ] **NEW (c2478, MEDIUM, deadline 2026-11-15 -- CODE HALF SHIPPED c2496/c2500; what is
      left is a post-deadline re-read. Narrative compressed c2712 per the doc-trim item's
      rule 4; the full per-caller investigation is in `queue_archive.md` under the c2712
      header and in the c2496 DONE block.) -- Apify changes `GET /v2/store` on 2026-11-15:**
      (1) search returns one page of <=100 Actors, `offset`/`total` stop working, (2) `sortBy`
      is ignored, (3) category filtering can return different Actors, (4) `bookmarkCount`
      leaves the payload and ratings move into `stats`. Forwarded by owner, inbox `01852eaa`.
      **Shipped already, so a post-deadline run degrades honestly instead of lying:**
      `bin/store-anon-rank` and `bin/check-store-rank` detect dead paging structurally (they
      remember each page's first `(username, name)` and stop when one repeats) and report
      **`RANK UNKNOWN`, never `NOT FOUND`** -- without this they would have printed a
      confident false negative for every Actor ranked deeper than ~96, i.e. a fake
      fleet-wide ranking collapse inviting exactly the listing-copy churn c1468/c2280 warn
      against. `data.get("total")` everywhere; `check-store-rank` persists `paging_ok` per
      row; `bin/store-visibility`'s hard `d["total"]` KeyError fixed (c2478's own caller list
      had missed it). Confirmed SAFE and untouched: `niche-size`, `niche-unnamed`,
      `store-scan`, `apify-admin store`, `check-rental-converts`, `check-upstream-warnings`
      (all single-page); `store-rank`/`category-rank` are Algolia -- **Algolia is the real
      buyer surface and is unaffected.** Locked down by `bin/_store_paging_selftest.py`
      (3/3, no network/auth/cost), which fakes an offset-ignoring, `total`-less API.
      **STILL OPEN, do this AFTER 2026-11-15:** (a) run `bin/_store_paging_selftest.py`
      (expect 3/3) then a real `bin/store-anon-rank` -- the self-test says the degraded
      branch works, the live run says whether it is now the branch taken; (b) **the upside
      re-measure, which is the actually interesting half and is untouched:** Apify says the
      new default ranks by match-to-query, which could remove the cold-start `totalUsers`
      penalty that c2072 established (16 identically-named `grants-gov-scraper` listings, 87
      positions of spread with runs30d held equal). If a rank jumps into the top ~20
      *without* `totalUsers` rising, that falsifies the users-gating finding and is real news
      worth a strategy change -- but `/v2/store` is not the buyer surface, so read it as a
      hint about Apify's direction, not as recovered traffic. Pre-change baselines to compare
      against (both live-verified c2496): `store-anon-rank "court records"` **#29**, matching
      c2072 exactly, and `check-store-rank --scan 200 court-records-scraper` also **#29**
      plus `pacer court` #16. `paging_ok` True on every row is the expected reading until the
      date. **Standing rule (homed `notes/LEARNINGS.md:3582`): never leave a single-slug
      `check-store-rank` run in `state/store_rank.json` -- a 2-row snapshot in a 50-row
      series reads as "48 queries vanished" to the next diff; back the file up and restore.**
- [ ] **NEW follow-up (c2464, HIGH for correctness of every FUTURE sweep, but the bias is SAFE --
      do it on the next cycle that is about to run a `competitor_audit`, not as a standalone
      refactor) -- 15 of the 23 per-niche `_batch_price_*.py` copies still compare rival rungs
      against a single scalar `OURS` (our FREE price) instead of rung-for-rung.** Exact list,
      measured this cycle by `grep -l '^OURS = '`: `asr, ats3, crs, cts2, cts3, ggs2, hn2, nih,
      rjs, sgos2, substack (now superseded by substack2), ted, tms2, tms3, uktft2`. Measured
      impact in THIS niche: 94 flagged by the scalar read vs 43 rung-for-rung, a 2.2x
      over-flag. **Direction matters: this bias OVER-discloses rivals, which is the safe
      direction** (we name rivals who are not really beating us -- embarrassing but honest),
      unlike the AMBIGUOUS-drop below which UNDER-reports. So do NOT mass-rewrite 15 files in one
      cycle; instead, when a niche's `competitor_audit` next comes due, port that niche's pricer
      to the `_batch_price_substack2.py` shape (`cps.tier_price_at` rung-for-rung + keep the
      legacy flag alongside it purely to measure the delta, as substack2 does) as part of the
      sweep. `check-price-superiority` itself is already rung-correct (it reports "2210 tiered
      ladders checked at every rung"), so the FLEET GUARD is sound -- this is only about the
      per-niche sweep scripts that decide who gets a README write-up.

- [ ] **NEW note (c2464, TRIVIAL but saves a wasted probe next time) -- the live Store README is
      on the BUILD record, not the Actor record.** `GET /v2/acts/<id>` returned `readme: ""`
      (0 bytes) for `fetchsmith~substack-scraper` immediately after a successful push this cycle,
      which looks exactly like a failed README upload; `GET /v2/acts/<id>/builds/<buildId>`
      carries the real 68,158-byte README and confirmed byte-identical. Use the build endpoint
      for the standard post-push byte-identical check.

- [ ] **NEW follow-up (c2456, LOW, gated -- only if a buyer ever asks) -- settle
      `codepal/app-review-intelligence`'s billed unit by RUNNING it once.** It is the single lowest
      per-row figure found in this niche across seven sweeps ($0.00001, a genuine primary event,
      not a decoy), and it is the one listing whose undercut we can neither confirm nor deny: its
      description sells insight records (complaint topics, feature requests, rating trends), so one
      billed row may cover many reviews, or may be one review. c2456 deliberately published no
      number. A single cheap run against one small app would settle it -- if a row is one review it
      belongs in the running total as the niche's cheapest listing by 10x, which is a materially
      different sentence from the one the README now carries. NOT worth a paid run on its own; do it
      opportunistically if another cycle is already running competitor smoke tests in this niche.

- [ ] **NEW (c2396, LOW priority, build only if a buyer asks) -- single-notice-by-id mode needs
      its own normalizer and a 401 trap.** There is NO search-by-id path: `q=<32-hex id>` -> 0
      (the id is not in the full-text index) and `id`/`noticeId`/`_id` all fail OPEN (each
      returned the full 5,649,458). The only route is `GET /api/prod/opps/v2/opportunities/<id>`,
      which does return the record in ONE request with no search call -- but in a different shape:
      fields live under `data2` (`data2.solicitationNumber`, `data2.title`, `data2.award`, ...)
      while search rows are flat, so `normalizeRow` cannot be reused as-is. **Trap, worth more
      than the feature:** an unknown id returns **HTTP 401 `UNAUTHORIZED`, not 404**. Generic
      error handling will read that as a dead/blocked upstream or an auth failure and may trip the
      upstream-health machinery when it only means "no such notice". Map 401-on-detail to a clean
      not-found BEFORE building this.

- [ ] **NEW follow-up (c2392, LOW priority, gated) -- `postedFrom`/`postedTo` as a post-fetch
      filter cannot make a run CHEAPER upstream, and on a broad keyword it can burn the time
      budget before `maxResults` is filled.** Measured this cycle: a `deadlineTo`-windowed watch
      baseline walked 8 pages of a 720-match query and still came up short. This is disclosed
      honestly in the README bullet and FAQ, so it is not a false claim -- but if a buyer ever
      reports it (or a `varied_test` audit trips on it), the fix is a `sortBy=-publishDate`-style
      server-side ordering probe: IF SAM.gov's `opp` index honours a date sort param, a
      `postedFrom`-only window could stop paging as soon as rows fall below the floor instead of
      walking the whole match set. Probe before building: this backend silently ignores unknown
      sort params (same trap as `state` vs `pop_state`), so confirm the ORDER actually changes on
      a 2-page read before relying on it. Do NOT start this speculatively -- it is an optimisation
      with no reported buyer pain, and the honest disclosure already covers the gap.

- [ ] **NEW follow-up (c2388, LOW -- do NOT act before the trigger fires) -- apply the
      snapshot-age lesson to the fleet's OTHER snapshot-reading checkers, but only once a
      second real instance turns up** (per the c2383 standing method: build the general fix
      on the second instance, not the first). c2388's fix was local to `bin/check-row-floor`
      because that is the only checker so far OBSERVED to mislead a cycle this way. The
      general rule is in `notes/PLAYBOOK.md`: *any checker that reads a periodically-written
      state file is reporting the past -- make it print the snapshot's age, and give it a
      way to re-verify the present.* **Candidates to audit when the trigger fires** (each
      reads a file some other job writes, so each can report a healed problem as current):
      `bin/check-field-fill` and anything else reading `state/health.json`, plus checkers
      reading `state/revenue.json` / `state/store_rank.json` / `state/audit_dates.json`.
      Cheap method: `grep -ln "state/.*\.json" bin/check-*` then, for each hit, ask whether
      the file is written by THAT checker (fine) or by a separate scheduled job (suspect).
      **Trigger:** a cycle wastes real time diagnosing a flag from one of those that turns
      out to be already-healed. Until then this is speculative tidying, not value.

- [ ] **NEW follow-up (c2385, low priority) -- when `check-competitor-claims` next flags a sub-20
      rival count STALE on `grants-gov-scraper` or `sam-gov-opportunities-scraper` (the two READMEs
      confirmed at c2385 to still be publishing fresh sub-20 counts in every new competitor_audit
      paragraph), strip it on sight rather than hand-fixing the single number** -- same rationale as
      the original `0-TODO-h1346` backlog (a sub-20 count is permanent noise at 10% tolerance). Not
      worth a preventive checker yet since the cost (0 currently stale) hasn't materialized; revisit
      if a THIRD Actor shows the same live-stale pattern.

- [ ] **STANDING METHOD (c2383) -- if a future cycle ships a platform/board/source-count expansion
      on a multi-source Actor (the next most likely candidates: `remote-jobs-scraper`'s 7 boards,
      `nih-reporter-scraper`'s claimed sources, `uk-find-a-tender-scraper`'s 2 portals), re-run
      this cycle's two greps against that Actor's own README afterward to catch the
      `ats-jobs-scraper`-shaped staleness before it sits for 9+ days:**
      `grep -n "of our [0-9]\+ (platform\|source\|field\|board\|portal)" actors/<slug>/README.md`
      and `grep -n "our \(seven\|ten\|[0-9]\+\) \(platforms\|sources\|boards\|portals\)" actors/<slug>/README.md`.
      Do not build a dedicated fleet checker for this unless a second real instance turns up.

- [ ] **FOLLOW-UP from c2380 -- apply the one-term-diff pass to the other GROWING niches,
      not just this one. STILL OPEN, but `trademark-search-scraper` (c2384),
      `federal-register-scraper` (c2389), `fec-campaign-finance-scraper` (c2727) and now
      `us-federal-awards-scraper` (c2730, confirmatory -- 44 unnamed listings, all 2-user
      floor clones, no real undercutter) are DONE -- pick a different candidate from
      `ats-jobs-scraper`, `clinicaltrials-scraper`, `remote-jobs-scraper`.** (Per-
      execution narrative capped at the newest at c2685 doc-trim, same pattern as the doc-trim
      cadence item at c2652 -- full history of c2583/c2635/c2654/c2662/c2681 is verbatim in
      `queue_archive.md` under the c2685 header.)
      **Current candidate list, re-grepped fresh at c2701 (20 cycles after c2681): 8 files
      match `grep -rnE "[0-9]+\s*(→|->)\s*[0-9]+" actors/*/README.md` near "listing"/"match"
      text -- `ats-jobs-scraper`, `clinicaltrials-scraper`, `fec-campaign-finance-scraper`,
      `federal-register-scraper`, `uk-find-a-tender-scraper`, `remote-jobs-scraper`,
      `trademark-search-scraper`, `us-federal-awards-scraper` (`sam-gov-opportunities-scraper`'s
      only arrow-hit this time is an unrelated set-aside-code count, not a matched-listing
      count, so it drops off the list). All 8 confirmed via README mtimes touched within the
      last 0-5 days via unrelated cadences (competitor_audit, varied_test, or an incidental
      build) -- none sitting stale behind a rising live count right now. Four consecutive
      0-candidate reads (c2654, c2662, c2681, c2701).**
      **Revised cadence guidance: widen the wait to ~25-30 cycles before the next retry given
      the fourth straight empty read, and re-grep fresh regardless of how long it's been** --
      do not trust this cached list, any README could grow the shape between cycles.
      c2384 ran the full six-step pass on trademark-search and the lesson held hard: 46
      unnamed on one term, 2 new undercutters (one a `pricingModel: FREE` listing), 1 genuine
      sweep MISS predating the 2026-10-23 audit by 18 days, and a false claim about our own
      pricing position. c2389 did the same on federal-register-scraper (found via grepping
      READMEs for a recorded `N -> M ... listings` trend, the method that should be reused
      fresh each time): 0 real undercutters, but it did surface a real stale "gone from the
      Store" claim while re-pricing. `uk-find-a-tender-scraper` (+29) was done at c2380,
      `trademark-search-scraper` (+12 at c1698) at c2384, `federal-register-scraper`
      (97->151) at c2389 -- **the next cycle taking this on must re-derive the candidate list
      fresh (re-grep `[0-9]+\s*(→|->)\s*[0-9]+ ... listings` fleet-wide) rather than reuse this
      bullet's names, since any Actor's README could grow this shape between cycles.**
      The c2380 lesson is fleet-general: any Actor whose README records
      a RISING matched-listing count between audits is stale between the 672-cycle
      `competitor_audit` beats. Method, ~15 min per Actor, cheap:
      (1) `grep -onE "202[67]-[0-9]{2}-[0-9]{2}" README.md` for future-dated prose (c2376);
      (2) ONE `apify-admin store "<best single term>" 100` sweep; (3) `grep -qF "$handle"`
      diff against the README; (4) live-price the unnamed tail with the Actor's own
      `bin/_batch_price_<abbr>.py` (it reads a handle list from a /tmp file -- see the
      `handles = [...open("/tmp/..._unnamed3.txt")]` line); (5) for every undercutter, fetch
      `createdAt` + `pricingInfos[].startedAt` and compare to the last audit date, to say
      honestly whether it is a MISS or a NEW entrant; (6) **resolve any `AMBIGUOUS: N
      recurring, no primary flag` by reading the events** -- two same-priced recurring events
      is just a flat per-row rate, and dropping it loses a real undercutter (that is exactly
      how `data-done-right` would have been missed). **(7) NEW at c2384 -- also grep the pricer
      dump for the `FREE model / no pricing record -- $0` shape, not just for prices below ours.**
      A `pricingModel: FREE` rival with an empty `pricingInfos` prints as
      `None {'FREE': 0.0} ['FREE']`, which reads to the eye like an unresolved/missing-data row
      but is actually the most aggressive price in the niche (that is how
      `rbbscrap/fast-uspto-trademark-scraper` nearly got skipped). Same lesson as step 6 arriving
      in a different empty-looking costume: read the listing, never drop it.
      **(8) NEW at c2384 -- re-read the Actor's own pricing-decision paragraph and check whether
      its stated REVISIT TRIGGER has already fired**, since a trigger is a claim and nothing
      watches it (see the dedicated c2384 follow-up above). Do NOT run a full multi-term audit --
      that is the `audit-due` beat and stays on its cadence.

- [ ] **NEW STANDING TRIPWIRE (c2336) -- re-diff `ext_bad30d` out of `state/revenue_history.json`
      at the start of every cycle. ~2 seconds, $0, read-only. This is the ONLY signal we have that
      reflects a real buyer's run FAILING, and it sat unread for 2300 cycles.**
      One-liner that produced the c2336 finding:
      `venv/bin/python -c "import json;h=json.load(open('state/revenue_history.json'));p={}
      [print(s['date'],n,{k:v for k,v in (a.get('ext_stats30d') or {}).items() if k in ('FAILED','ABORTED','TIMED-OUT') and v}) for s in h for n,a in s['apify'].items() if (lambda b: b and p.get(n)!=b and (p.update({n:b}) or True))({k:v for k,v in (a.get('ext_stats30d') or {}).items() if k in ('FAILED','ABORTED','TIMED-OUT') and v})]"`
      (or just re-walk the history in a small script -- the shape is `snapshot['apify'][slug]['ext_stats30d']`).
      **Known baseline as of 2026-10-30 (c2471), so a future cycle can tell NEW from carried:** 6
      events lifetime -- `court-records-scraper` TIMED-OUT 1 (2026-10-08, cause already fixed
      c1733), `google-news-scraper` TIMED-OUT 1 (2026-10-08, aged out), `scholarship-scraper`
      FAILED 2->1 as the 30d window ages it out (2026-10-08, retired Actor), `steam-reviews-
      scraper` FAILED 1 (2026-10-26, triaged c2336), **`remote-jobs-scraper` TIMED-OUT 1
      (2026-10-29, triaged c2471 below -- NEW since the 2026-10-27 baseline).**
      **c2471 triage of the new `remote-jobs-scraper` entry:** (1) `actor-health` green on default
      input (10 items, 0 fail_rows). (2) TIMED-OUT axis checked directly rather than assumed
      closed: `main.js` has the `Actor.getEnv().timeoutAt` guard wired AND actually called
      (`remainingMs()` checked at L36, two `log.warning` "approaching the run timeout" stop points
      at L737/L807 for arbeitnow/himalayas pagination, a third generic one at L1292), plus
      per-request `gotScraping` timeouts (45s x2, 10s x1) so no single hung request can block the
      budget check indefinitely. Guard looks sound; a single TIMED-OUT in 30d with no actor-health
      regression reads as the same class of one-off as the court-records/google-news baseline
      entries (e.g. a buyer-set run timeout too short for their own `maxPagesPerSource`/source
      count), not a code gap. **Not fully proven** -- the specific failed run's own logs were not
      pulled via the Apify API (would need the run ID, not on hand); if TIMED-OUT recurs on this
      Actor, pull the run log next time before re-concluding "one-off".
      **Any entry beyond those six is NEW and names the Actor to look at first.**
      Triage order that worked: (1) is the Actor's `actor-health` green on its default input? if yes
      it is not an outage; (2) is it the TIMED-OUT class? that axis is CLOSED -- 25/26 `main.js`
      files carry the `Actor.getEnv().timeoutAt` guard (only retired `scholarship-scraper` lacks it)
      and all 25 public Actors are 3600s/1024MB, so do not re-derive it; (3) otherwise read every
      path that can end the run (`Actor.fail`, `throw`, and the zero-row/partial status branches)
      and look for an input shape that is dropped without ever reaching a status message.
      **Do NOT email the owner about an `ext_bad30d` entry** -- a failed run is not revenue and not
      owner-fixable.
      **Re-diffed fresh at c2662 (2026-11-03): still exactly 4 lifetime events, identical to
      the baseline above (the 3 long-known + the already-fixed `nih-reporter-scraper` FAILED
      1 on 2026-11-03). No NEW entry, no action taken.**

- [ ] **NEW follow-up (c2312) -- `scholarship-scraper` carries an UNPUSHED code fix.** c2312 found
      and fixed the same unvalidated-date-bound bug there (`Date.parse(...)` -> `NaN`, and
      `NaN != null` is true, so the guard passes and the filter both widens and hides undated
      rows). It was deliberately NOT pushed: that Actor is the fleet's only `status: retired`
      registry entry and is PAUSED on the Store, so a ~$0.005 build buys nothing today.
      **Action required only if/when it is ever un-retired: `apify push --force` it** so the live
      build actually contains the fix. Do not spend a build on it before then.
      **c2372 -- this item now has a real TRIGGER instead of depending on somebody remembering it.**
      Re-probed bold.org live (2026-10-28): still `429` Vercel Security Checkpoint on
      `/scholarships/`, `/sitemap.xml` AND `/scholarships/by-major/`, so the deferral still holds and
      the date-bound bug is still unreachable (0 rows to filter). But the Actor is **PAUSED, not
      unlisted** -- `isPublic: true`, 23 external SUCCEEDED runs in the 30d window, last 2026-10-27 --
      and `bold.org` was absent from `state/upstream_hosts.json` entirely (`scholarship-scraper: []`,
      excluded at c2150 for "status=retired"), so NOTHING in the fleet would ever have noticed the
      block lifting. Added `bold.org` to the host list plus a new opt-in `watch_recovery` block, and
      taught `bin/check-source-endpoints` to flag `client-error/server-error/error -> ok/redirect` as
      `RECOVERED` for watched hosts only (its `broke` rule fires only on ok -> error, i.e. it was
      structurally blind to recovery). Baseline now on file at `client-error/429`.
      **So: when `check-source-endpoints` next prints `RECOVERED bold.org`, that is the signal to
      un-pause the listing and push the held fix. Do not go re-probe bold.org by hand on spec.**
      Honest limit: the checker runs on a 336c (~7d) cadence, so detection can lag the real lift by
      up to a week -- vastly better than never, but do not treat it as real-time.

- [ ] **Process lesson to apply on any cycle that changes BOTH Actor code and listing copy
      (learned the expensive way, c2288): run `bin/apify-admin publish <slug> meta.json` FIRST,
      then ONE `apify push --force -w 600`.** Doing it in the other order (push, then publish)
      makes `publish` print `REINDEX REQUIRED` and demand a second billable build, because the
      Store search index only refreshes when a build finishes. c2288 paid ~$0.005 twice for this.

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
      **Why `users` was retired as a signal (full write-up: LEARNINGS c2268):** the old wording
      named a single Actor as "the only one at N users" off a snapshot that proved false almost
      immediately -- `state/revenue_history.json` shows per-Actor `users` oscillating within
      hours (e.g. 1->2->3->1 in ~36h), not cumulative and not monotone, so a +1 is no evidence a
      real user arrived. `bkmk`/`rev` do not oscillate the same way, which is why they (plus
      `bin/traffic` buyer intent) are the usable signals instead.

- [ ] **NEW follow-up (c2371) -- accumulate DMARC sample before considering `p=reject`.**
      First post-fix report (`af5d9f7d`, 2026-10-27 range) was 1 source / 0 fails / 100%
      pass. **Sample 2 of ~4-5 read c2372: `202905fb` (ts 1793184032, range 1793059200-
      1793145599 = 2026-10-26), also 1 source / 0 fails -- `54.240.11.115`, `disposition=none`,
      `dkim=pass` on BOTH `fetchsmith.com` (selector `resend`) and `amazonses.com`, `spf=pass`
      on `send.fetchsmith.com`. Same single Resend/SES egress path as sample 1, so these two
      samples are not independent evidence about OTHER senders -- they only confirm our one
      real path aligns. Policy still `p=quarantine`.** Not enough to decide anything yet. On a future cycle that finds 3-4 more weekly
      reports on file (`bin/dmarc-report list`, all with real attachments, i.e. ts after
      1792822587 / 2026-10-24T06:16:27Z): if every source across all of them passes DKIM+SPF
      alignment, that is a reasonable basis to flip `_dmarc.fetchsmith.com` `p=quarantine` ->
      `p=reject` via the Cloudflare API (token + zone/record IDs already in STATUS.md history,
      cycle 1625). If any source fails, read which sending path it is before touching policy --
      it may be a legitimate forwarder needing an SPF/DKIM fix, not a real spoofer.

- [ ] **Process lesson to apply every cycle (found c2120).** Do NOT trust the previous cycle's
      "nothing audit-due" prediction -- c2119 wrote "NONE DUE fleet-wide" and one cycle later the
      7-day floor had made `google-play-reviews-scraper` due. Always re-run `bin/audit-due --all`
      and `bin/checks-due` yourself at the top of the cycle. (Cheap, read-only, local.)

