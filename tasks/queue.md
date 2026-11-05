- [x] **DONE cycle 2742 (QUALITY/GROWTH slot, 2742 % 3 == 0) -- a REAL Actor failure outranked the
      planned queue.md trim; root-caused it and shipped the customer-facing half.**
      Preflight: `checks-due --all` NONE DUE (soonest `store-anon-rank` in 2c, c2744); `audit-due --all`
      NONE DUE across all 16 types; `inbox-triage new` NONE UNTRIAGED of 74; `bin/revenue` $0 booked,
      25 Actors, 47 users, 803 runs30d, `ext_bad30d` 4; `apify-spend` $6.6408/$85 (87.6% elapsed,
      projection $7.58); services all active; `/`, `/pricing`, `/tools`, `/blog` all 200. Buyer-intent
      funnel flat (tools 34/33 engaged 7/6, pricing 4/4 engaged 3/3, checkout 3/2 engaged 0/0) -- far
      below the >100/day Polar gate, correctly no owner email.
      **1. Root-caused the `shopify-products-scraper` nightly failure, and it is NOT the c2724
      transient dip.** Ran c2724's own recipe: the live `--recheck` still failed, and the health-history
      trace (deduped by inner `ts`, not by commit -- counting commits overstates the sample because
      most commits carry an unchanged snapshot) shows 7 zeros in ~119 distinct runs with **the last two
      consecutive runs both zero**, which is c2724's stated "real signal" trigger. The Apify run log is
      explicit: 403 bot/IP block, 0 products, and the Actor reports it cleanly -- **the code is correct
      and was not touched.** Four platform runs in ~4 min proved the block is **store-independent and
      time-varying on Apify's shared IPs**: 4 stores 403, 1 429, and `deathwishcoffee.com` served
      products twice then 403'd 3 minutes later unchanged. So **no demo-store swap was made** -- it
      would relocate the same failure while looking like a fix. Remedies filed with costs in the open item.
      **2. Fixed and PUBLISHED a now-false customer-facing README claim that the same measurements
      falsified.** The FAQ said (measured 2026-11-04) that `allbirds.com`/`deathwishcoffee.com` "both
      returned products fine over a direct connection" and that a fleet-wide 403 is "usually the
      datacenter pool being blocked" -- as of 2026-11-05 the DIRECT path is blocked intermittently too,
      so that advice sent buyers to change settings when the right first move is to re-run later.
      Rewrote it with today's numbers, kept the genuine store-level case (`gymshark.com`) and the
      nothing-is-charged point, and explicitly noted the superseded measurement rather than silently
      swapping it. One batched README-only push, build **0.1.111**; verified via the `latest` build's
      `readme` field over the API (not the CDN-cached page, per PLAYBOOK): new text present, old claim
      absent. Post-push checks: `check-readme-samples` 39 blocks/106 bullets/0 drift,
      `check-expired-dates` 0 unresolved.
      **3. Deferred the queue.md trim, legitimately and once.** `check-doc-size` reads TRIM SOON
      (76.2KB/865 lines, ~23c headroom, proj. 204KB at next look) -- still OK, not DUE. This was its
      FIRST flagged QUALITY slot, and doc-trim rule 2 permits exactly one deferral, **which this cycle
      has now consumed: the trim is MANDATORY at c2745.** A real Actor failure with a published false
      claim attached outranks a proactive cut that still has positive headroom.
      **Not expanded into scope:** `check-competitor-claims` (144c cadence, not due) surfaced 5
      pre-existing guarded STALE rival user-counts in `ats-jobs-scraper` and `court-records-scraper`
      READMEs -- unrelated to this cycle's change, filed below, not fixed here.
      $0 spend beyond one ~$0.005 build + API reads; $0 revenue change; no owner email.

- [x] **DONE cycle 2744 (NORMAL slot, 2744 % 3 == 2) -- shipped all 5 flagged counts; the item's
      "5 STALE" turned out to be an UNDERCOUNT, see the follow-up below.** All 5 live-verified off
      `GET /v2/acts/<handle>` `stats.totalUsers` before editing, then hand-edited per the guard
      (`ats-jobs-scraper:227` greenhouse 3->1, ashby 1->2; `court-records-scraper:172` nexgendata
      61->69, automation-lab 71->81; `:174` pink_comic 23->27). **Every one of the 5 trend claims is
      about PRICE, not users** ("have both dropped to the FREE model", "still charges ... unchanged
      since 2026-07-17", "ties this Actor's $0.002/record exactly"), so no count swap could falsify
      one -- but I used the c2240 `as of 2026-11-05` form **scoped to the count** so the paragraphs'
      own price-verification dates (2026-10-30 / 2026-10-03) are NOT restamped onto facts they do
      not attest to. **Checked the one real cross-reference by hand before editing:** `:235`'s
      `martc03/court-records-mcp` superlative ("more users than every rival in this section except
      the two biggest") still holds -- the two biggest are exactly the two I raised (69, 81) and
      martc03 is live 34, third largest. Re-ran the checker: all 5 cleared, remaining count is
      26 = 22 ats-jobs + 4 court-records, exactly the originals minus my 5. Shipped as builds
      **0.1.119** (ats-jobs) and **0.1.77** (court-records), one push each, and verified the new
      strings present / old strings absent in each `latest` build's `readme` field over the API
      (not the CDN-cached page). ~$0.01 in builds, $0 revenue change, no owner email.

- [ ] **NEW note (c2744, LOW -- read this BEFORE treating a `check-competitor-claims` stale count
      as news, which is the mistake I started to make this cycle).** The c2742 item's "5 STALE"
      was a scoped reading, and a wider sweep this cycle looks alarming at first (40 STALE in
      `app-store-reviews-scraper` 12 / `apple-podcasts-scraper` 4 / `ats-jobs-scraper` 24, plus 7
      not 3 in `court-records-scraper`). **It is not news. It is a KNOWN, DELIBERATELY DEFERRED
      backlog with a standing decision behind it** -- `state/fleet_checks.json`'s own note records
      c2657 finding "125 remain stale but all guarded (hand-review needed)" out of 877 claims, and
      c2235/c2369/c2513 each independently chose to leave the guarded small-drift counts unfixed on
      the stated grounds that they are low-stakes, re-drift within days, and none flips a pricing or
      ranking conclusion. Remaining after this cycle's 5 fixes: ats-jobs 22, court-records 4,
      app-store-reviews 12, apple-podcasts 4 (21 of 40 carry the `superlative` guard, 12 the `trend
      claim` guard; most deltas are 2->1 / 1->2 churn that only trips the 10% tolerance because the
      base is tiny). **So do NOT open a campaign against the count.** The only two classes worth a
      cycle, both of which DO change what a buyer reads: (a) the 2 `gone from the Store` lines, where
      a README still names a rival that no longer exists -- `app-store-reviews-scraper:478`
      (`gh0st1k/app-store-reviews-scraper`) and `court-records-scraper:240`
      (`steadfetch/cendoj-jurisprudence-monitor`); and (b) the big movers sitting inside superlative
      paragraphs, where the new number really can falsify the prose -- `app-store-reviews-scraper`
      (`thewolves` 2688->3153, `johnvc` 550->648, `sourabhbgp` 223->270) and `ats-jobs-scraper`
      (`fantastic-jobs/career-site-job-listing-api` 8067->9166, `jobo.world/ats-jobs-api` 769->890,
      `openclawai` 51->75). Do (a) first -- it is prose, not arithmetic, and needs no live lookup.
      One Actor per cycle, batched into ONE push.

- [ ] **NEW note (c2744, TRIVIAL -- saves the next cycle a wasted 5 minutes and a wrong conclusion).**
      `check-competitor-claims` makes one live API call per backticked rival handle and the READMEs
      now name ~880 of them, so a fleet-wide run takes **far longer than a 300s `Bash` timeout** --
      mine got through only 3 of 25 Actors (alphabetically) before being backgrounded, and a 2-Actor
      `--only` run checked 107 claims in most of 280s. **I briefly concluded from this that the
      fleet run "can never complete" and that the 144c cadence record must be partial. That was
      wrong** -- `state/fleet_checks.json` shows completed fleet runs at c2657 (877 claims), c2513
      (876), c2369 (714) and c2092 (589). The check is fine; it just needs **`run_in_background: true`
      and a long timeout**, not a fix. Last run c2657, 144c interval, so next due **c2801** -- and
      note I did NOT record a run this cycle, correctly: a truncated fleet run plus two `--only`
      runs is not a valid run of record (the tool's own docstring says so), so the cadence is
      untouched and still reads not-due.

- [x] **DONE cycle 2741 (NORMAL slot, 2741 % 3 == 2) -- genuinely clean preflight, nothing
      due, nothing manufactured.** `checks-due --all` had exactly one DUE: `check-citable` --
      ran it (93 blog posts + `/pricing` 6 cards + `/tools` 24 cards, every price-bearing
      card/page carries its own Actor's apify.com URL as text, CLEAN) and recorded it via
      `checks-due --ran`, next due c3077. `audit-due --all` NONE DUE across all 16 types
      (`competitor_audit` soonest in 12 cycles, `website-screenshot-scraper`); `inbox-triage
      new` NONE UNTRIAGED of 74 (spot-checked the inbox-list mail that looked new --
      `a661a19a`/`5ce80b92`/`6acc123f` -- all already dispositioned, nothing owed a reply);
      `bin/revenue` $0 booked, 25 Actors, 47 users, 803 runs30d, `ext_bad30d` 4; `apify-spend`
      $6.6286/$85 (87.6% elapsed, projection $7.57); services `fetchsmith-web`/`fetchsmith-mail`/
      `caddy` all active; `/`, `/pricing`, `/tools`, `/blog` all 200. All four standing watches
      re-verified live and unchanged: `eu-ted-tenders-scraper` users 1/1/1, bookmarks 0, runs30d
      TOTAL 45; `bold.org/scholarships/` still 429; DMARC same 2 reports, 1 source/0 fail;
      `bin/traffic` buyer-intent funnel flat (tools 34/33 engaged 7/6, pricing 4/4 engaged 3/3,
      checkout 3/2 engaged 0/0) -- far below the >100/day Polar gate, correctly no owner email.
      **Re-diffed the c2336 `ext_bad30d` tripwire by hand (not just the count): still exactly the
      same 4 lifetime entries as c2662** (`steam-reviews-scraper` FAILED 1 2026-10-27,
      `court-records-scraper` TIMED-OUT 1 2026-10-27, `remote-jobs-scraper` TIMED-OUT 1
      2026-10-29, `nih-reporter-scraper` FAILED 1 2026-11-03) -- no NEW entry.
      **Checked whether anything else was actually actionable before concluding there wasn't:**
      the c2380 one-term-diff lever is mid-cooldown (last re-grepped c2739, revised wait is
      ~50-60 cycles); confirmed via a quick `grep -oE "202[67]-[0-9]{2}-[0-9]{2}"` sweep across
      11 un-swept-by-this-specific-lever niches' READMEs that every one has a "checked live"/
      dated entry within the last ~1-9 days (the regular 336-672c `competitor_audit` rotation is
      keeping the whole fleet fresher than the one-term-diff lever would add value over right
      now) -- so applying it to a new niche this cycle would likely have been confirmatory-only,
      the kind of zero-finding sweep c2524's anti-manufactured-work rule warns against running
      just to look busy. `check-doc-size` OK on all three docs (queue.md 72.4KB/822 lines, ~24c
      headroom at the current growth rate, projected to land almost exactly on the 200KB trim
      line at the next look -- **flagging for the next QUALITY slot (c2742) to treat queue.md
      as the standing trim candidate it already was**, not a new finding). Piggybacked the two
      $0 latent tripwire checks since nothing else needed the time: `check-citable` (above) and
      the c2552 FDA `Not Yet Classified` curl -- see that item's own entry for the one real
      datum found (`drug` 2 -> 1, still not 0, no action). $0 spent beyond normal API reads, $0
      revenue change, no owner email.

- [x] **DONE cycle 2740 (NORMAL slot, 2740 % 3 == 1) -- shipped the real fix for the
      c2737 flat-rival `every_tier` bug, because c2737's own stated trigger ("if a second
      one turns up in another niche's batch pricer") FIRED.** Preflight: one check DUE,
      `git-maintain` -- ran it (TRIP loose 87MiB >= 64MiB, repacked loose 1195->0, pack
      120->124MiB, `.git` 127M, all 3 services active after) and recorded it (next due
      c2788). Everything else clean: `audit-due --all` NONE DUE across all 16 types,
      `inbox-triage new` NONE UNTRIAGED of 74, `bin/revenue` $0 booked / 25 Actors / 47
      users / 803 runs30d / `ext_bad30d` 4, `apify-spend` $6.6274/$85 (proj. $7.57),
      services + `/`, `/pricing`, `/tools`, `/blog` all 200. Buyer-intent funnel flat
      (tools 34/33 engaged 7/6, pricing 4/4 engaged 3/3, checkout 3/2 engaged 0/0) -- far
      below the >100/day Polar gate, correctly no owner email.
      **Found instances 2 and 3 offline, $0, zero API calls, by replaying the saved
      `/tmp/*_prices*.json` cohorts** -- `madeingermany/apify-hiring-cafe-scraper` (flat
      $0.00125, dearer than our remote-jobs SILVER/GOLD+) and `civitab/uk-tenders-ocds`
      (flat $0.0025, exactly TIES our find-a-tender GOLD+ floor; a tie is not an undercut).
      2 bad of 66 flat-priced rivals in the 3 affected niches. Probe kept as
      `bin/_flat_tier_probe.py`.
      **c2737's "fleet-general" sizing was wrong in a useful way: the bug can only mis-fire
      where OUR OWN price is TIERED**, since against a flat `OURS` the one-key comparison is
      already exact. Only `ats3`/`rjs`/`uktft2` qualify; the other seven tiered-dict copies
      (`crs`, `cts2/3/4`, `nih2`, `tms2/3`) have a flat `OURS` and were never affected.
      **NO shipped README ever carried the false claim** -- `uk-find-a-tender-scraper`'s
      README already says `civitab` "ties our Gold-and-above floor exactly, so it only
      undercuts the Free/Bronze/Silver tiers" (the hand-read step overrode the bad flag) and
      `madeingermany` was never named at all. So this was a tool-correctness chore, not a
      published-accuracy incident -- no Actor push, no listing-copy edit, nothing
      manufactured (c2524).
      **Fix:** `expand_flat()` / `undercut_tiers()` / `beats_every_tier()` added to
      `bin/_unit_price.py` (the shared module, so future copies inherit it); a partial tier
      map RAISES rather than resolving, so the helpers can never flip into UNDER-flagging
      (licensed by measurement: across 303 rivals in 5 cohorts `len(unit_tiers)` is only
      ever 0, 1 or 6). `ats3`/`rjs`/`uktft2` now call them and keep
      `legacy_every_tier_one_key` + `legacy_undercuts_tiers` alongside to measure the delta
      (the `_batch_price_substack2.py` shape). Patch script `/tmp/c2740_patch.py` (asserts
      one match per line, backups `/tmp/c2740_{ats3,rjs,uktft2}.bak`).
      **Live-verified on `rjs`** against a 3-handle list: `madeingermany` every_tier
      True->False and `undercuts_tiers` ['FREE']->['BRONZE','FREE'] (the legacy test was
      also UNDER-listing the tier list while over-stating every_tier), while the genuine
      every-tier undercutter `forgedata/remote-jobs-aggregator` still reads True -- no
      regression on the case the flag exists to catch. The `/tmp/rjs_prices.json` 39-row
      cohort was backed up before the run and restored after (verified 39 rows / 44526 B),
      per the `store_rank.json` standing rule -- a 3-row file would have broken
      `_unit_price_selftest.py`'s replay and the next sweep's diff.
      **LEFT FOR A FUTURE CYCLE (precise, LOW):** (a) `ats3` and `uktft2` are byte-identical
      in the patched region and compile clean, but are UNEXERCISED since the patch -- their
      `/tmp/*_unnamed*.txt` input lists are gone, so the first real run of either should
      sanity-read the two `legacy_*` fields rather than assuming; (b) the other 17 pricers
      with an `every_tier`-family flag still carry their own inline test -- port each to the
      helpers opportunistically when its niche's `competitor_audit` comes due, same gating as
      the c2464 item below, NOT as a standalone refactor.
      **Process lesson homed in LEARNINGS: never hand-type a rival handle from README prose
      -- read it from the cohort JSON.** I probed `quiethand098~remote-jobs-scraper` /
      `geese_chief~remote-jobs-scraper`, got 404 on both, and briefly had a tempting "two
      rivals c2738 named have already vanished" finding; the c2536 negative control killed it
      (our own listing and `forgedata` returned 200, so the token was fine) -- the real slugs
      end `-aggregator`, which is exactly how the README already spells them, and both return
      200. `/v2/acts/<handle>` gives a bare 404 for a nonexistent handle, indistinguishable at
      the status-code level from a delisted Actor.

- [x] **DONE cycle 2743 (NORMAL slot, 2743 % 3 == 1) -- shipped remedy (b) from the c2742
      `shopify-products-scraper` item: `actor-health` now treats a 403/429-only run as
      INCONCLUSIVE, not FAILED, fleet-wide, $0.** Preflight clean: `checks-due --all`/
      `audit-due --all` both NONE DUE (soonest `store-anon-rank` in 1c, c2744); `inbox-triage
      new` NONE UNTRIAGED of 74; `bin/revenue` $0 booked, 25 Actors, 47 users, 803 runs30d,
      `ext_bad30d` 4; `apify-spend` $6.6547/$85 before, $6.6555/$85 after (two extra `--only`
      health probes, +$0.0008) (87.7% elapsed, projection $7.59); services
      `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active; `/`, `/pricing`, `/tools`, `/blog`
      all 200.
      **Mechanism:** `run-sync-get-dataset-items` returns no run-id header, so on a `not ok`
      result the new `inconclusive_blocked(slug)` helper looks up the Actor's own most-recent
      run (`GET /v2/acts/<user>~<slug>/runs?desc=true&limit=1` -- safe because `run.sh`'s lock
      keeps this to one worker/one run at a time) and reads that run's `RUN_SUMMARY` KV record.
      If `sources` is a non-empty list, EVERY entry's `complete` is false, and EVERY entry's
      `reason` text names HTTP 403 or 429 (regex `\((\d{3})\)` against the Actor's own
      customer-facing sentence, e.g. "this storefront refused the request (403)"), the result
      is marked `inconclusive: true` and excluded from the `failed` list that mints the FIX
      FAILED ACTORS task. Any other shape -- a different code (401/402/404/503), a source that
      DID complete, or no RUN_SUMMARY at all (most Actors don't write one) -- leaves `ok`
      exactly as before, so the change can only soften a false alarm, never hide a real one.
      **Live-verified, `--only` so health.json/queue.md untouched:** `shopify-products-scraper`
      -- re-ran the exact failing case, confirmed still live: `{'ok': False, 'inconclusive':
      True, 'status': 201, 'items': 0, ...}`, and its `RUN_SUMMARY` read back
      `incompleteDetail: "https://allbirds.com: this storefront refused the request (403) —
      a bot check or a geo/IP block..."` (run `ZqQHgwxIzi8XnK01B`). Healthy control
      `hacker-news-scraper` -> `{'ok': True, 'inconclusive': False, ...}` unchanged (the
      helper is short-circuited by `(not ok) and ...`, so passing Actors cost zero extra API
      calls). Ran the helper standalone against `remote-jobs-scraper`/`nih-reporter-scraper`
      (both currently healthy/no matching RUN_SUMMARY shape) -> both `False`, confirming the
      fallback is safe rather than just untested.
      **Scope note for future cycles:** this is additive and fleet-wide by construction, but
      today only `shopify-products-scraper`'s code writes this exact `RUN_SUMMARY.sources[]`
      shape, so it is the only Actor this can currently soften. If another Actor's nightly
      health flips FAILED on an upstream 403/429 and it already has (or gets) a `RUN_SUMMARY`
      with per-source `reason` text, it benefits automatically with no further code change.
      **Baseline to re-check after a few nightly runs:** before this fix, 7/119 zeros on
      `shopify-products-scraper` all minted a FIX FAILED ACTORS line; after, a 403/429-only
      night should mint none (no code regression expected since the Actor's own logic is
      untouched -- only `bin/actor-health`'s classification changed). (a) residential proxy
      remains blocked on a `BUDGET.md` line and `password_set: false`, unchanged, not pursued
      this cycle. $0 revenue change, no owner email.

- [x] **DONE cycle 2736 (QUALITY/GROWTH slot, 2736 % 3 == 0) -- executed the mandated
      `tasks/queue.md` trim, the deferral c2733/c2734 said must not slip a second QUALITY
      slot.** Preflight clean: `checks-due --all` NONE DUE (soonest `check-retired-disclosure`
      in 1c, cycle 2737), `audit-due --all` NONE DUE across all 16 types, `inbox-triage new`
      NONE UNTRIAGED of 74, `bin/revenue` $0 booked / 25 Actors / 47 users / 803 runs30d /
      `ext_bad30d` 4, services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all active, `/`,
      `/pricing`, `/tools`, `/blog` all 200. All four standing watches re-verified live and
      unchanged: `eu-ted-tenders-scraper` users 1/1/1, `bookmarkCount` 0, `runs30d` TOTAL 45;
      `bold.org/scholarships/` still 429 (`scholarship-scraper`'s held c2312 fix stays
      unpushed); DMARC same 2 reports, 1 source / 0 fail; `bin/traffic` buyer-intent funnel
      flat (tools 35/34 engaged 8/7, pricing 5/5 engaged 4/4, checkout 1/1 engaged 0/0) -- far
      below the >100/day Polar gate, correctly no owner email.
      **Trim result: 87.2KB/999 lines -> 60.1KB/677 lines, TRIM SOON -> OK** (~26c headroom,
      proj. 188KB at the next look). Partition re-derived fresh per cadence rule 3; rule-1
      hazard grep ran first and rescued nothing (both rule-shaped hits already homed in
      LEARNINGS). Archived cycles 2733/2732/2731/2730/2728/2727/2726/2725/2724/2723 + the
      interleaved 2729 (282 lines) verbatim, keeping 2735/2734 live. **Because a DONE-only cut
      left only a ~6KB margin (rule 4), three fat OPEN items were compressed in place as well**
      -- the c2716 head-term lever (5041->3185 B), the c2380 sweep header (4047->2527 B) and
      the doc-trim item's own execution record (2220->1902 B) -- with every dropped detail
      verified already homed verbatim in `notes/LEARNINGS.md` first, their pre-compression text
      appended to `queue_archive.md`, and all instructions/gates/baselines retained. Guards:
      move-partition asserted total/non-overlapping/multiset-identical, each rewrite asserted
      strictly smaller (the doc-trim one FAILED this assert on the first run at 2553 B and was
      rewritten -- the guard earned its keep), **33 open items before and after**, every
      pre-trim open-item first line still present verbatim except the two intentional rewrites,
      `queue_archive.md` confirmed append-only and byte-identical at the prefix,
      `check-doc-size` OK on all three docs after. Also repaired the blank-line separator the
      cut removed before the c2700 item, plus one PRE-EXISTING missing separator before the
      c2464 item (unrelated to this trim, found by the same invariant check). $0 spent beyond
      normal API reads, $0 revenue change, no owner email. **Follow-up recorded in the doc-trim
      item: queue.md is now ~90% open items, so the next trim of it must plan on compressing
      or retiring open items rather than banking on a DONE-only cut.**

- [x] **DONE cycle 2735 (NORMAL slot, 2735 % 3 == 2) -- preflight clean (`audit-due --all`
      NONE DUE; 0 untriaged mail of 74 -- re-read the two owner-forwarded threads
      (`2b237f1b` court-records CourtListener token, `01852eaa` the `/v2/store` Nov-15
      ranking change) in full and confirmed both are stale/already-handled: the token was
      wired in and verified at cycle 2362, and the Store API change's code half shipped at
      c2496/c2500 with its post-deadline re-read correctly gated to after 2026-11-15, 10
      days out; `bin/revenue` $0 booked, 25 Actors, 47 users, 803 runs30d, `ext_bad30d` 4;
      `apify-spend` was the one DUE check (soonest in the 44-tool fleet-check table) --
      ran it ($6.6149/$85, 87.2% elapsed, projection $7.59) and recorded via `checks-due
      --ran`, next due cycle 2831; services `fetchsmith-web`/`fetchsmith-mail`/`caddy` all
      active; `/`, `/pricing`, `/tools`, `/blog` all 200. All four standing watches
      re-verified live: `eu-ted-tenders-scraper` users 1/1/1, `bookmarkCount` 0, runs30d
      TOTAL 45; `bold.org/scholarships/` still 429; DMARC unchanged; `bin/traffic`
      buyer-intent funnel flat (tools 35/34 engaged 8/7, pricing 5/5 engaged 4/4, checkout
      1/1 engaged 0/0) -- far below the >100/day Polar gate, correctly no owner email.**
      With the c2716 head-term gap list closed (c2734) and no other checker/audit DUE, this
      NORMAL slot went to the next open growth-sweep item instead: the c2380 one-term-diff
      pass on `clinicaltrials-scraper` (see that item's own rewritten entry below for the
      full measured detail -- `apify-admin store "clinicaltrials" 200` -> 176 listings, 99
      unnamed, the four highest-traction (3-user) unnamed listings all live-priced dearer
      than our unchanged $0.0015/row flat rate, no new undercutter, no README edit).
      **Narrowed the candidate list for next time to `ats-jobs-scraper` and
      `remote-jobs-scraper`.** Spend $6.6149/$85 (no push this cycle, no code/content
      shipped -- a confirmatory sweep only). $0 revenue change, no owner email.

- [x] **DONE cycle 2734 (NORMAL slot, 2734 % 3 == 1) -- preflight fully clean (checks-due/
      audit-due --all both NONE DUE, 0 untriaged mail of 74, apify-spend $6.6093/$85 at 87.1%
      elapsed proj $7.59, services/pages 200, all four standing watches re-verified live and
      unchanged -- no owner email), so the slot went to growth: published head-term guide #93,
      `/blog/website-screenshot-api-no-key-compared`, closing the last open Actor
      (`website-screenshot-scraper`) on the c2716/c2732 head-term-titling gap list. See the
      rewritten c2716 follow-up item below for the full measured detail (three keyless
      screenshot endpoints compared: mshots 403s from this box's datacenter IP, thum.io's bare
      mode is 24h CDN-cached vs always-fresh with `fullpage/`, microlink.io caps keyless calls
      at 5/24h via its own rate-limit headers). Backlinked both ways, shipped as build **0.1.43**
      -- verified via the build's own `readme` field (25,618 bytes, new link present) plus
      `taggedBuilds.latest.buildNumber`/`isPublic`. Pushed to IndexNow (200). Six checkers re-ran
      clean and recorded via `checks-due --ran`: `check-links` (93 posts/157 pages CLEAN),
      `check-disclosure` (93 site + 28 dev.to, 0 missing), `check-backlinks` (136 pairs/93 posts,
      0 missing/0 unresolved), `check-actor-guides` (24 Actors, 0 flagged), `check-blog-cta` (93
      posts, 0 missing-CTA/0 bad-slug/0 dead-link), `check-blog-claims` (0 stale of 6+19+3+8).
      All four standing watches re-verified live, unchanged: TED tenders `eu-ted-tenders-scraper`
      users 1/1/1, `bookmarkCount` 0, runs30d TOTAL 45 (off `data.stats`, correct nesting); DMARC
      same 2 reports (`af5d9f7d`/`202905fb`, 1 source/0 fail); `bold.org/scholarships/` still 429;
      `bin/traffic` buyer-intent funnel flat (tools 35/34 engaged 8/7, pricing 5/5 engaged 4/4,
      checkout 1/1 engaged 0/0) -- far below the >100/day Polar gate, correctly no owner email.
      Spend $6.6088/$85 (+$0.0005 for the one push) -> $6.6093/$85. $0 revenue change, no owner
      email. **`tasks/queue.md` itself is STILL TRIM SOON** (was 80.0KB/914 lines at c2733, grew
      further with this cycle's edits) -- this is a NORMAL slot so per the doc-trim cadence
      (trim only in a QUALITY slot) it was correctly left untouched; its first flagged deferral
      was already logged at c2733 (rule 2 permits one more QUALITY slot to pass), so the next
      QUALITY slot (2736) must treat the trim as due, not optional -- a second deferral past
      2736 would break the rule.

- [ ] **NEW follow-up (c2716, MEDIUM -- the first new growth lever found in ~50 cycles, but
      it must be re-read before it drives a content pivot). Re-measure the organic
      head-term-vs-gotcha split once the 90d window has genuinely rolled over, i.e. NOT before
      ~cycle 2790** (c2704's rule: "re-read it later" is meaningless if the window hasn't
      moved). Run `bin/traffic` and read the `ORGANIC SEARCH landing paths` section; the c2716
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
      **THE GAP LIST IS CLOSED -- do not re-open it.** All five Actors have a head-term post:
      `sec-insider-trades-scraper` c2720 (#89), `app-store-reviews-scraper` c2728 (#90),
      `hacker-news-scraper` c2731 (#91), `google-news-scraper` c2732 (#92),
      `website-screenshot-scraper` c2734 (#93). Guide #93 was the deliberate test of whether
      the lever generalises past no-key data sources -- "screenshot API" is a COMMERCIAL head
      term, not an informational one like the government/public-API terms that produced the
      original signal, so expect it to rank worse and read that as information about the
      lever's scope, not as a failure (measured detail: LEARNINGS c2734). The next growth
      action for this channel is the re-measure above, not another new post, unless a fresh
      by-TITLE pass finds a new gap.
      **Keep this lesson, it will recur: `check-actor-guides` counts dedicated posts and README
      bullets, it cannot see what a post is TITLED**, so it can never audit a lever that is
      about head-term framing -- re-derive any future version of this list from post TITLES
      (one pass over the `tool:`->filename map), never from the checker's counts and never from
      a previous cycle's say-so (c2731 logged the list closed on its own say-so and was wrong;
      caught c2732).
      **FIVE new head-term posts inside 14 cycles means the ~c2790 re-measure is now confounded
      by our own publishing** -- #89-#93 will be ~1-2 months indexed by then, i.e. YOUNGER than
      the Sept head-term batch and OLDER than the Oct gotcha batch, so age-control the diff
      against the 2026-09-30 post-date cutoff that c2716 used and do not let the five new posts
      quietly inflate the head-term side.

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
      **Re-checked live again c2741 (free, piggybacked on this cycle's otherwise-idle preflight,
      no Actor touched): food 1 (unchanged), device 1 (unchanged), `drug` moved 2 -> 1** -- the
      first count change since c2552. Still n=1, not 0, so the enum value is still reachable and
      the tripwire has NOT fired; no comment edit needed. But `drug` is now down to the same
      single-remaining-row state as `food`/`device`, so all three endpoints are one reclassification
      away from losing the value. Re-check again next time this Actor is touched, or opportunistically.

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

- [ ] **doc-trim cadence (orig. c2508, REWRITTEN c2520-c2588; execution records COMPRESSED
      c2652, re-compressed c2736 -- the c2604/c2605/c2628/c2634/c2643 narratives and the c2733
      STATUS.md execution record are verbatim in `queue_archive.md` under the c2652 and c2736
      headers. KEEP THIS ITEM IN THIS SHAPE: method + standing rules + newest execution only.
      Do NOT prepend a full narrative per trim -- that habit grew this one item to 32% of the
      live queue.)**
      **MANDATORY AT c2745 -- `tasks/queue.md`, no further deferral available.** c2742 read TRIM SOON
      on it (76.2KB/865 lines, ~23c headroom, proj. 204KB at its next look) and used the single
      deferral rule 2 permits, because a real `shopify-products-scraper` nightly failure with a false
      published README claim attached outranked a proactive cut that still had positive headroom. The
      next QUALITY slot must execute it. Per rule 5, still re-run `bin/check-doc-size` first and trust
      its verdict -- do NOT reuse the c2742 numbers above; c2742 ADDED a DONE block and a long
      re-diagnosis to this file, so it is bigger now than those numbers say.
      **But treat `tasks/queue.md` as the standing next candidate even while it reads OK:** the
      c2736 cut landed at 60.1KB with a projected 188KB at the next look, i.e. a ~12KB margin,
      still marginally under rule 4's ~15KB bar even AFTER compressing three open items. The
      structural reason is that this file is now ~90% open items (33 of them) and only two DONE
      blocks, so a DONE-only cut can no longer buy much here -- the next trim of this file must
      plan on compressing or RETIRING open items, and the honest place to look first is the
      long tail of LOW/gated/latent items below c2456, several of which have never fired.
      **EXECUTED c2736 (QUALITY slot) -- `tasks/queue.md` only** (87.2KB/999 lines, ~21c
      headroom), at its second flagged QUALITY slot; c2733 was the single deferral rule 2
      permits. Rule-1 hazard grep ran FIRST: two hits read like standing rules outside their own
      narrative (c2524 anti-manufactured-work; c2732 "`check-actor-guides` cannot see titling"),
      both already homed at `notes/LEARNINGS.md:5774`/`:6148` and `:6293` -- nothing rescued.
      **Deliberately NOT a DONE-only cut, and that is the reusable part:** archiving every DONE
      block but the newest two left 63.7KB against a 69.5KB ceiling (200KB - 24c * 5440 B), a
      ~6KB margin that rule 4 calls thin -- so three fat OPEN items (c2716 lever, c2380 sweep
      header, this execution record) were compressed in the same cycle, each one's dropped
      measured detail verified already homed in LEARNINGS first, every instruction/gate/baseline
      retained. `bin/_trim2736q.py`, backups `/tmp/c2736_*.bak`. Guards: move-partition asserted
      total/non-overlapping/multiset-identical with the three rewrites asserted separately and
      each required to shrink; no `- [ ]` in the archive partition; services/pages 200 after.
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
      **c2740 made this port CHEAPER -- do not re-derive the comparison by hand.** `bin/_unit_price.py`
      now exports `expand_flat()` / `undercut_tiers(ut, OURS)` / `beats_every_tier(ut, OURS)`, which are
      rung-for-rung AND flat-rival-correct, so porting a niche is: give that file a tiered `OURS` dict,
      call the two helpers, keep the old expression as `legacy_*` for the delta. `ats3`/`rjs`/`uktft2`
      are already done this way -- copy one of them. NOTE the two bugs are independent: c2740 fixed the
      RIVAL-side flat under-check, this item is still open for the 15 files whose OUR-side `OURS` is a
      scalar, and those are mostly a DIFFERENT set (overlap is `asr`, `ggs2`, `hn2`, `sgos2`, `substack`,
      `ted` -- all Family-B scalar files, none of which c2740 touched).

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
      not just this one. STILL OPEN.** Done so far: `uk-find-a-tender-scraper` (c2380, +29),
      `trademark-search-scraper` (c2384, the richest result -- 46 unnamed on one term, 2 new
      undercutters including a `pricingModel: FREE` listing, 1 genuine sweep MISS predating the
      2026-10-23 audit by 18 days, and a false claim about our own pricing position),
      `federal-register-scraper` (c2389, 97->151 -- 0 real undercutters, but it did surface a
      real stale "gone from the Store" claim while re-pricing), `fec-campaign-finance-scraper`
      (c2727), `us-federal-awards-scraper` (c2730, confirmatory -- 44 unnamed listings, all at
      the 2-user floor with 0 runs30d) and `clinicaltrials-scraper` (c2735, confirmatory -- 99
      of 176 listings never named on the README; the four highest-traction unnamed ones, each
      at this batch's 3-user ceiling, live-priced in full at 2-13x our own unchanged
      $0.0015/row flat rate with no start fee). Both confirmatory passes found the same
      clone-flood shape and made **no README edit -- nothing found, nothing manufactured, per
      the standing c2524 rule.** Full measured detail: LEARNINGS c2730 and c2735.
      `ats-jobs-scraper` (c2737, a real signal this time -- the same one-term query that found
      44 listings at c2382 found **80** at c2737, 355 cycles later; live-priced the 62 unnamed
      handles, found two genuine 6-of-10-platform matches (`bigibyte` free, `api-co` partial),
      one 3-platform partial undercutter, resolved an AMBIGUOUS batch-pricer flag by hand, and
      caught a fleet-general batch-pricer bug along the way -- see README + LEARNINGS c2737 for
      full detail. Pushed as build 0.1.118, verified live.) and now `remote-jobs-scraper`
      (c2738, first time this specific lever was applied -- its last full sweep was the
      different-method `competitor_audit` at c2461, only 6 days earlier). `apify-admin store
      "remote jobs" 150` found 129 listings, up from 92 at the cycle-2376 spot-check (+40% in
      8 days) -- real growth, same staleness shape. Diffed all 129 against the README by exact
      handle: 62 unmatched, 23 of those second/third listings from owners already named, 39
      from genuinely new owners. Live-priced all 39 via `bin/_batch_price_rjs.py`: one real
      undercutter, `forgedata/remote-jobs-aggregator` (5 of our 7 boards + 390 career sites,
      flat $0.00001/job -- hand-verified via raw `pricingInfos` history, which showed 4 price
      records in 4 days, so it is a brand-new listing (3 users) still actively repricing, not
      a settled rival), plus two near-full-parity aggregators that priced ABOVE us
      (`quiethand098` 7/7 boards, `geese_chief` 6/7 boards). No pricing change warranted --
      same reasoning as the `grants-gov-scraper` decision below (1-3 users, $0 booked here,
      14-day irreversible price-cut mechanics against unmeasurable elasticity). Written up in
      the README, pushed as build 0.1.95, verified live (`forgedata` present in the shipped
      `readme` field). **Both `ats-jobs-scraper` and `remote-jobs-scraper` are now done --
      this one-term-diff lever has no remaining untried candidate in the three niches it was
      scoped to (`ats-jobs-scraper`/`clinicaltrials-scraper`/`remote-jobs-scraper`).** Next
      time this item comes up, either widen the candidate list to a new niche or treat it as
      a recurring per-niche re-check (the ats case showed real growth in ~1 week, so an 8-10
      day cadence per niche, not a one-shot, is probably the right frame -- re-derive from
      each Actor's own last-swept date rather than assuming). (Per-execution
      narrative capped at the newest at c2685 and re-capped at c2736, same pattern as the
      doc-trim cadence item -- full history of c2583/c2635/c2654/c2662/c2681 is verbatim in
      `queue_archive.md` under the c2685 header.)
      **Re-grepped fresh again at c2739 (38 cycles after c2701, inside the revised ~25-30c
      window): tightened the pattern to require "listings"/"matched" directly adjacent to the
      arrow (not just nearby), which cuts the false-positive noise from unrelated "N users"/"N
      platforms" number-pairs that the looser c2701 grep was pulling in (41KB of matches on the
      loose form vs. 4 lines on the tight one).** Only 2 README files matched at all
      (`fec-campaign-finance-scraper`'s own "a 2→1 or 2→3 move is noise" caveat, not a listing
      count, and `federal-register-scraper`'s two already-written-up `94->97`/`97->151` lines
      from c2389) -- both already closed, zero fresh candidates. **Five consecutive
      0-candidate reads (c2654, c2662, c2681, c2701, c2739).** Separately confirmed the 8-10 day
      per-niche recheck cadence this item also names has nothing due either: `ats-jobs-scraper`
      (c2737, 2c ago), `remote-jobs-scraper` (c2738, 1c ago) and `clinicaltrials-scraper` (c2735,
      4c ago) are all far inside the ~384-480c (8-10 day) window, so none is ready for a recheck
      yet. **Revised cadence guidance: widen the wait to ~50-60 cycles before the next retry
      given the fifth straight empty read (doubling again, same backoff shape `audit-due` uses
      elsewhere in this file), and re-grep fresh with the TIGHT pattern above, not the loose
      c2701 one** -- do not trust any cached list, any README could grow the shape between
      cycles, but don't burn QUALITY-slot time wading through loose-pattern noise either.
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

