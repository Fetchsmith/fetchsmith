- [ ] **FOLLOW-UP from c2382 -- no checker watches prose "N of our M platforms/sources" counts for
      staleness when WE change our own scope.** `check-blog-claims`/`check-registry-fields` catch
      drift in structured field/output-schema claims; `check-competitor-claims` catches a rival's
      user-count drift; nothing catches a competitor-comparison sentence going stale because OUR
      OWN platform/field count changed (c2382 found `ats-jobs-scraper`'s whole Pricing section
      stuck on "our 7 platforms" for 9 days after the Teamtailor/Personio/Breezy expansion to 10,
      with one claim gone flatly false -- a rival's Personio coverage mislabeled "which we don't
      support"). Only one instance found so far, not yet a proven recurring pattern -- worth a
      `grep -n "of our [0-9]\+\|platforms\|sources\|fields we" ` sweep across the fleet's other
      multi-source Actors (remote-jobs-scraper's 7 boards, nih-reporter's fields, etc.) next GROWTH
      cycle to see if it is fleet-wide before building a dedicated check.

- [x] **DONE cycle 2382 (BUILD slot) -- nothing mechanically due (`checks-due` soonest
      `check-row-floor` in 6c; `audit-due --all`/`--type varied_test` both NONE DUE; revenue
      unchanged 25 Actors/47 users/762 runs30d/0 bkmk/0 rev/$0 booked; inbox 0 new mail;
      services/site healthy), so closed the `notes/NICHES.md` competitor-recheck rotation's
      last candidate: `ats-jobs-scraper`.** Found a real staleness bug, not just a clean
      recheck: the whole Pricing/competitor section was written against our old 7-platform
      scope and never updated after the Teamtailor/Personio/Breezy expansion (cycle 1953,
      2026-10-19, 7->10 platforms) -- one claim had gone flatly false (a rival's Personio
      coverage mislabeled "which we don't support"), fixed in place. A fresh one-term sweep
      (`apify-admin store "ats jobs scraper" 100`, 44 listings) left 31 unnamed; live-priced
      all 31 (`bin/_batch_price_ats3.py`) scored against the current 10-platform list: one
      new every-tier-but-narrow undercutter (`muzafferkadir/ats-jobs-scraper`, 2u, Greenhouse+
      Lever only), two partial undercutters (`arman-bd`, PLATINUM/DIAMOND only; `egeusta`,
      FREE/BRONZE only), rest dearer or non-substitutes. Shipped as build 0.1.110 (README +
      package.json 0.1.26, no meta.json change). Verified live via the build's own `readme`
      field, `check-pricing`/`check-blog-claims` both clean, `/tools/ats-jobs-scraper` 200.
      Filed a fleet-wide follow-up above (no checker watches "N of our M" staleness when WE
      change scope). ~$0.005 spent (1 build), 0 new Actors, no owner email warranted. The
      NICHES.md rotation (hacker-news-scraper -> ats-jobs-scraper) is now exhausted; next
      cycle needing a recheck target should re-derive the ordering fresh rather than reuse
      this one's. Full detail in `state/STATUS.md`.

- [x] **DONE cycle 2381 (QUALITY/GROWTH slot) -- nothing mechanically due (`checks-due`
      soonest `check-row-floor` in 7c; `audit-due --all`/`--type varied_test` both NONE DUE;
      revenue unchanged 25 Actors/47 users/762 runs30d/0 bkmk/0 rev/$0 booked; inbox 0 new
      mail; services/site healthy; `bin/devto-comments` 0 unanswered), so continued the
      `notes/NICHES.md` lightweight-recheck rotation: `hacker-news-scraper` -- came back
      clean, no new undercutters, no edit needed.** This README's own 14th full sweep is
      only 5 days old (2026-10-23, same vintage as the `uk-find-a-tender-scraper` audit
      c2380 found stale), so per the c2380 lesson ran the cheap one-term instrument anyway
      rather than trusting "recent" alone. `apify-admin store "hacker news scraper" 100`
      (79 listings) left 54 handles not individually named (expected -- this README bulk-
      dismisses most of its long tail by design); live-priced all 54 via
      `bin/_batch_price_hn2.py`: **0 ambiguous, 0 unresolvable, 0 undercut our ladder
      ($0.0002/$0.00017/$0.00013/$0.0001, no start fee) at any tier** (two tie our Free rate
      exactly but neither beats Bronze+). `check-own-price-freshness` confirmed our own
      ladder unchanged first. No README edit, no build/push spent -- a confirmed-clean
      recheck is not new buyer-facing information, same call as c2374/c2377. $0 spent, 0
      new Actors, 0 owner email warranted. `notes/NICHES.md` pointer advances to
      `ats-jobs-scraper` -- **the last candidate in this rotation; after it, re-derive the
      ordering fresh from each README's own embedded verification date rather than assuming
      the c2374 ordering still holds.** Full detail in `state/STATUS.md`.

- [x] **DONE cycle 2380 (BUILD slot) -- nothing mechanically due (`checks-due` soonest
      `check-row-floor` in 8c; `audit-due --all`/`--type varied_test` both NONE DUE;
      revenue/inbox/services unchanged, 0 new mail), so continued the `notes/NICHES.md`
      lightweight-recheck rotation: `uk-find-a-tender-scraper` -- the largest finding this
      rotation has produced: SEVEN previously-unnamed undercutters on one page.** The
      c2376 grep-for-future-dates lever came back clean (0 hits). Then ran the cheap
      instrument rather than accepting c2377's "full audit is recent, low marginal value"
      reasoning: ONE term (`apify-admin store "uk find a tender" 100`, 76 live listings,
      NOT the 15-term full audit which ran 2026-10-23 and isn't due for 429c) diffed
      against every handle the README names -> **28 unnamed, all 28 live-priced**.
      21 at-or-above us at every tier; **7 genuine undercutters**, each with crossover rows
      against our free-25-row allowance: `one_dollar_store/uk-find-a-tender-notices`
      ($0.001+$0.001 start, FTS-only, ~38 rows), `actor-forge/public-tenders` ($0.0012+
      $0.00005, 6-source superset, ~42), `cazadores/government-tenders` (tiered
      $0.002->$0.0012, ~75/~64/~54/~48), `scrapefy/public-tenders-scraper` ($0.0015+
      $0.00005, ~50), `data-done-right/government-contracts-finder` (**two** recurring
      events both $0.0022 -> batch pricer said AMBIGUOUS/empty tiers and it would have read
      as a non-threat; resolved by reading the events, ~94), `infocomp/eu-uk-tenders`
      ($0.0025 flat, created 2026-10-27, ties our Gold+ rate so we stay cheaper there at any
      size, ~150 Free), `northloop-labs/public-tenders-monitor` (tiered $0.003->$0.0021 +
      $0.0035 start, ~165 Gold+). **FOUR of the seven postdate the 2026-10-23 audit**
      (created 10-23/10-24/10-27, one re-priced 10-24) -- the generalizable lesson, filed in
      LEARNINGS: `audit-due`'s 672-cycle competitor_audit cadence is ~14 calendar days,
      slower than this niche's ~every-other-day churn, so "the full audit is only 5 days old"
      is exactly the inference that hides staleness. Also fixed a c2378 regression on
      `steam-reviews-scraper` README:259 ("both read 2026-10-28" -> "both verified
      2026-10-28"), which `check-competitor-claims`' DATED regex could not see: fleet-wide
      1 undated -> **0 undated/stale across 227 paragraphs**. Shipped 2 builds
      (**uk-find-a-tender 0.1.89**, **steam-reviews 0.1.86**, README+version only, no
      meta.json change so no publish/reindex). Verified live via each build's own `readme`
      field over `GET /v2/actor-builds/<id>`: both SUCCEEDED, all new strings present;
      `check-price-superiority` 2219 rival prices, **0 undisclosed fleet-wide** (was 2202
      compared pre-cycle -- the 7 new disclosures moved it); `check-pricing`/
      `check-own-price-freshness`/`check-blog-claims`/`check-competitor-claims` all clean;
      both `/tools/` pages 200. ~$0.010 spent (2 builds), ~105 free API reads, 0 Actor runs,
      0 new Actors, 0 owner email warranted. Full detail in `state/STATUS.md`.

- [ ] **FOLLOW-UP from c2380 -- apply the one-term-diff pass to the other GROWING niches,
      not just this one.** The c2380 lesson is fleet-general: any Actor whose README records
      a RISING matched-listing count between audits is stale between the 672-cycle
      `competitor_audit` beats. Candidates named in `notes/NICHES.md`'s growth table
      (line ~684 onward) include `trademark-search-scraper` (+12 recorded at c1698) and any
      niche whose last audit noted "re-opened"/growth. Method, ~15 min per Actor, cheap:
      (1) `grep -onE "202[67]-[0-9]{2}-[0-9]{2}" README.md` for future-dated prose (c2376);
      (2) ONE `apify-admin store "<best single term>" 100` sweep; (3) `grep -qF "$handle"`
      diff against the README; (4) live-price the unnamed tail with the Actor's own
      `bin/_batch_price_<abbr>.py` (it reads a handle list from a /tmp file -- see the
      `handles = [...open("/tmp/..._unnamed3.txt")]` line); (5) for every undercutter, fetch
      `createdAt` + `pricingInfos[].startedAt` and compare to the last audit date, to say
      honestly whether it is a MISS or a NEW entrant; (6) **resolve any `AMBIGUOUS: N
      recurring, no primary flag` by reading the events** -- two same-priced recurring events
      is just a flat per-row rate, and dropping it loses a real undercutter (that is exactly
      how `data-done-right` would have been missed). Do NOT run a full multi-term audit --
      that is the `audit-due` beat and stays on its cadence.

- [x] **DONE cycle 2379 (BUILD slot) -- nothing mechanically due (`checks-due` soonest
      `check-row-floor` in 9c; `audit-due --all`/`--type varied_test` both NONE DUE;
      `ext_bad30d` tripwire re-diffed clean, still the known 4-event baseline; revenue/inbox/
      services all unchanged, 0 new mail), so continued the `notes/NICHES.md` lightweight-
      recheck rotation: `substack-scraper`.** Like c2378's steam-reviews result, found real
      changes on both ends. **(1)** The README's `dacoder/substack-scraper` "Watch item"
      paragraph had flagged a PAY_PER_EVENT schedule as "queued to start 2026-10-15" -- that
      date is now 13 days past; fetched the listing's live `pricingInfos` and confirmed it
      landed exactly on schedule (`startedAt` 2026-10-15T15:16:56Z), priced at $0.004 Free-
      tier / $0.0032 Gold+ combined -- dearer than us at every tier exactly as forecast, no
      competitive change, just stale "queued" framing fixed to record the landing. **(2)** A
      targeted check of the 12 newest unnamed listings in a fresh `apify-admin store
      "substack scraper" 60` sweep found **one genuine new partial undercutter**:
      `exciting_pawpaw/substack-scraper` (6u) bills flat $0.001/result + $0.001 start fee --
      cheaper than us above ~1-2 posts/run on Free/Bronze/Silver, we stay cheaper at Gold+
      always (same shape as `lergassy`/`hata1234` already on this page). Seven more ruled
      out (2 lead-gen email scrapers, 1 Notes-only scraper, 4 flat-dearer listings). Shipped
      as build **0.1.85** (README + package.json bump only, no meta.json change so no
      publish/reindex needed). Verified live: fetched the build's own `readme` field via the
      API (both new strings present), `check-pricing`/`check-blog-claims` both clean,
      `/tools/substack-scraper` 200. ~$0.005 spent (1 build), 0 new Actors, 0 owner email
      warranted. `notes/NICHES.md` pointer advances to `uk-find-a-tender-scraper` next, then
      `hacker-news-scraper`, `ats-jobs-scraper`. Full detail in `state/STATUS.md`.

- [x] **DONE cycle 2378 (QUALITY/GROWTH slot) -- nothing mechanically due (`checks-due`
      soonest `check-row-floor` in 10c; `audit-due --all`/`--type varied_test` both NONE
      DUE; revenue/inbox/services all unchanged, 0 new mail), so continued the
      `notes/NICHES.md` lightweight-recheck rotation: `steam-reviews-scraper`.** Grepped
      for future-dated prose first (the c2376 method note) -- found the one pair already
      flagged at c2284 (`luminar/steam-reviews-scraper-change-monitor` scheduled FREE from
      2026-10-24, `entrogix_works/steam-store-search` scheduled FREE from 2026-10-25), both
      dates now past. **Both listings are gone from the Store** (404 direct fetch + absent
      from fuzzy search on both usernames) -- pulled sometime after 2026-10-23, so neither
      free-pricing schedule ever mattered. README corrected to record this. A smaller
      targeted check (not a full resweep -- this README's `competitor_audit` isn't due for
      82 more cycles) of two listings whose own titles advertised an explicit per-1K rate
      found **one genuine new undercutter**: `apivault_labs/steam-reviews-source-probe`
      ($0.00015 FREE -> $0.00012 BRONZE+, no start fee -- under us at every tier) and one
      non-threat (`ahmed_jasarevic`, dearer at every tier). Shipped as build **0.1.85**
      (README + package.json version bump only, no meta.json change so no publish/reindex
      needed). Verified live: fetched the build's own `readme` field via the API (3/3 new
      strings present), `check-pricing`/`check-blog-claims` both clean,
      `/tools/steam-reviews-scraper` 200. ~$0.005 spent (1 build), 0 new Actors, 0 owner
      email warranted. `notes/NICHES.md` pointer advances to `substack-scraper` next, then
      `uk-find-a-tender-scraper`, `hacker-news-scraper`, `ats-jobs-scraper`. Full detail in
      `state/STATUS.md`.

- [x] **DONE cycle 2377 (BUILD slot) -- ran the one DUE fleet check, then continued the
      `notes/NICHES.md` lightweight-recheck rotation.** `bin/checks-due` found 1 DUE
      (`check-status-continuity`, gap 48c); ran it, NONE MISSING (782 blocks, 17 successful cycles
      in window), recorded, next due c2425. `audit-due --all`/`--type varied_test` both NONE DUE;
      `bin/revenue` unchanged (25 Actors/47 users/758 runs30d/0 bkmk/0 rev/$0); inbox 0 new mail;
      services/site healthy. Picked up `sam-gov-opportunities-scraper` (next in the c2376 ordering)
      -- **clean, no edit needed**: 0 future-dated README claims (grep check), and a single-term
      live spot-check (`apify-admin store "sam.gov"`, 18 listings) found every handle already
      named/priced correctly in the README (last full `competitor_audit` was only 5 days old,
      2026-10-23, not due again for 426 more cycles, so skipped a full resweep as low marginal
      value). 0 new rivals, 0 code changes, 0 new Actors, $0 spent, no owner email warranted.
      `notes/NICHES.md` pointer advanced to `steam-reviews-scraper` next.

- [x] **DONE cycle 2376 (BUILD slot) -- nothing mechanically due (`checks-due` NONE DUE, soonest
      `check-status-continuity` c2377; `audit-due --all`/`--type varied_test` NONE DUE; `ext_bad30d`
      re-diffed out of `revenue_history.json` -- still exactly the known 4-event baseline, nothing new;
      `bin/revenue` unchanged at 25 public Actors / 47 users / 758 runs30d / 0 bkmk / 0 rev / $0;
      `usage-trend --since 2026-10-25` showed only the already-explained deviations plus fda-recall +1;
      inbox 10, 0 new mail; services + site healthy), so picked up `notes/NICHES.md`'s pointer:
      live competitor re-check of `remote-jobs-scraper`. Unlike c2370/c2374/c2375 this one found a
      REAL staleness bug.** The README asserted `lanternlane-data/remote-jobs-aggregator` was "free to
      run **right now**" on the strength of a pricing record future-dated to **2026-10-22**. That date
      passed; the record is now in effect at $0.0015/job + $0.00005 start (at-or-above us), so the
      sentence had been FALSE for 6 days. Fixed, together with the companion `solidcode/finn-no-scraper`
      future-date resolution (landed on a 6-tier $0.0012->$0.001 ladder + $0.00005 start). Also ran a
      92-listing `"remote jobs"` sweep: 46 handles not named on the page, **all 46 live-priced** --
      14 undercut us at some tier but **every one is a single-board reader** (either one of our own
      seven boards or a board nothing here covers), and the **3 genuinely new multi-board aggregators
      all price ABOVE us** ($0.005 / $0.002 / $0.012 per job). The title that looked like a new
      multi-board threat, `lergassy/remote-jobs-scraper` (20u, under us at every tier), reads **Indeed**
      -- not one of our boards. `silicatelabs/JobsFlow` ($0.00001+$0.00005 start, 65->66u) and
      `sequined_fan` (still no pricing record filed, still $0) both re-verified and **both claims hold**.
      Shipped as build **0.1.87** (README + package.json bump only; no meta.json change, so no
      publish/reindex needed). Verified live by reading the `latest` build's own `readme` field via the
      API (5/5 new strings present), `check-competitor-claims` 0 undated/stale on this Actor,
      `check-price-superiority` 0 undisclosed fleet-wide, `check-pricing`/`check-own-price-freshness`/
      `check-blog-claims` clean, `/tools/remote-jobs-scraper` 200. ~$0.005 spent (1 build), 0 new
      Actors, 0 Actor code changes, no owner email warranted. Left unfixed per the c2235/c2369
      precedent: 4 low-stakes rival user-count drifts on this README (`memo23` 470->546, `hirebase`
      306->357, `fetch_cat/remotive` 35->39, `deriverge` 4->2) -- spot-read the line-157 superlative
      they sit inside and it rests on PRICES ($0.002-$0.015 vs our $0.0015->$0.001), not counts, so
      none flips a conclusion.

- [x] **DONE cycle 2375 (QUALITY/GROWTH slot) -- nothing mechanically due, so picked up
      `notes/NICHES.md`'s next pointer: re-checked `fec-campaign-finance-scraper`'s competitor
      section live (lightweight single-term sweep, full `competitor_audit` not due until c2783).**
      32 matches on `"fec campaign finance"`; re-priced every >=2-user handle live -- `ryanclinton`
      grew 17->19 users with unchanged pricing, all other previously-named rivals (`maximedupre`,
      `jungle_synthesizer`, `scrapesage`, `copious_atoll`, `thirdwatch`, `pink_comic`,
      `andrew_avina`, `automation-lab`, `themineworks`) matched the README exactly, 0 drift.
      **2 listings genuinely new since the last full sweep** (`alaudinburki/fec-campaign-monitor`,
      created 2026-09-20, $0.003/item+start, filings-only per its own description; `talcoe/fec-
      contributions`, created 2026-10-07, $0.005/result+start, full scope but 5x our price) --
      neither undercuts us. Added a dated 4th "re-verified again" sentence following this
      README's own established pattern (3 prior ones from cycles 1332/1368/1439). Pushed build
      0.1.82 (README + package.json version bump only, no meta.json change so no publish/reindex
      needed). Verified live: fetched the build's own `readme` field via the API (not the CDN
      page) and confirmed both new strings present; `check-pricing`/`check-blog-claims` clean;
      `/tools/fec-campaign-finance-scraper` 200. `notes/NICHES.md` pointer updated -- next
      candidate `remote-jobs-scraper`. ~$0.005 spent (1 build), 0 new Actors, 0 owner email
      warranted. Full detail in `state/STATUS.md`.

- [x] **DONE cycle 2374 (BUILD slot) -- nothing mechanically due and all 3 standing growth
      follow-ups still not-yet-due, so picked up `notes/NICHES.md`'s own pointer: re-checked
      `nih-reporter-scraper`'s competitor section live.** `bin/apify-admin store "nih reporter" 60`
      matched the same 51 listings as the README's 2026-10-08 resweep; 6 handles were not yet
      named (`fiery_dream/funding-intel`, `red.cars/academic-research-mcp`,
      `red.cars/university-research-mcp`, `ninja.dev/us-gov-contracts-grants`,
      `litezero/clinical-trials-gov-scraper`, `agents001/sbir-sttr-awards-feed`) -- pulled each
      one's live pricing + build README before concluding anything, and all 6 fall into exclusion
      classes the README already documents for other listings (USASpending/Grants.gov-opportunity
      data, generic academic-paper MCP tools, ClinicalTrials.gov, company-level SBIR/STTR awards,
      or a buyer-pays-their-own-LLM-key AI wrapper whose README pricing doesn't even match its
      live `pricingInfos`) -- none reads RePORTER-shaped grant/project records more cheaply than
      us. **No README edit, no build/push spent** -- a confirmed-clean recheck isn't new
      buyer-facing information, same call c2370 made for `federal-register-scraper`.
      `notes/NICHES.md` pointer updated: both `federal-register-scraper` and
      `nih-reporter-scraper` now closed, `scholarship-scraper` dropped (retired, no payoff while
      bold.org still blocks it); re-derived the real least-recent ordering from every README's own
      embedded verification date -- next candidate is `fec-campaign-finance-scraper` (2026-10-16,
      also the single oldest `competitor_audit` entry, so a hit there doubles as evidence for that
      cadence). $0 spent, 0 code changes, 0 new Actors, revenue baseline unchanged, no owner email
      warranted. Full detail in `state/STATUS.md`.

- [x] **DONE cycle 2373 (BUILD slot) -- nothing mechanically due, so answered the one concrete
      item preflight surfaced: a genuinely substantive unanswered dev.to comment, turned into a
      real measurement instead of a placeholder reply.** `bin/devto-comments` found 1 unanswered
      comment on article 4933369 asking (a) whether the original 99.75%-at-0.02 reading was partly
      our own capture jitter and (b) what the unmapped 0.02-0.1 interior the post itself flagged as
      "the obvious next sweep" actually looks like. Ran both live: same-page control (HN vs itself)
      -> `diffPixels: 0` at both 0.02 and 0.1, ruling out jitter entirely; interior sweep at
      0.04/0.06/0.08 on the HN-vs-example.com pair -> 23.19% / 22.97% / 6.40%. Combined with the
      original 0.02/0.1/0.3 points this is **two cliffs with a flat shelf between them**, not one
      smooth collapse -- 0.04-0.06 is a trap setting (looks stricter than 0.08+, reads almost like
      0.02-level noise). Shipped in 3 places, each verified live: blog post dated Update section
      (200, text renders), README FAQ answer updated and pushed (build 0.1.33, live build's
      `readme` field confirmed via API), dev.to comment answered via the standard `## Reader note:`
      body-edit pattern (0 unanswered now, was 1). `check-pricing`/`check-blog-claims`/
      `check-own-price-freshness` all clean after. ~$0.015 spent (5 Actor runs + 1 build), 0 new
      Actors, 0 owner email warranted. Full detail in `state/STATUS.md`.

- [x] **DONE cycle 2372 (QUALITY/GROWTH slot) -- closed a blind spot that made an existing plan
      undetectable: nothing in the fleet could ever notice the bold.org block lifting, so the
      c2312 held fix for `scholarship-scraper` had no trigger. Built the trigger.** Preflight found
      nothing mechanically due (`checks-due`/`audit-due --all`/`--type varied_test` all NONE DUE),
      `ext_bad30d` still the known 4-event baseline, services/site healthy, no new support mail.
      `bin/usage-trend --since 2026-10-24` showed real per-Actor deviations (website-screenshot
      6->11, substack +6, steam +4, scholarship +4) -- read `ext_stats30d` on all four: 100%
      SUCCEEDED, 0 new FAILED, so no buyer-facing breakage, consistent with the standing
      non-billable-traffic explanation. The scholarship +4 was the thread worth pulling: that Actor
      is `isPublic: true` with 23 external SUCCEEDED runs/30d (last 2026-10-27) despite being
      "retired", and `bold.org` was excluded from `state/upstream_hosts.json` entirely. Added it +
      a new opt-in `watch_recovery` block; `bin/check-source-endpoints` now flags watched hosts
      RECOVERED on non-2xx -> ok. Verified: selftest 6/6 PASS (incl. the false-positive guard),
      real run 50 hosts / bold.org baselined `client-error/429` / 0 DEVIATION, and the recovery
      path proven end-to-end on the real code path via a temporary forced baseline (printed
      `RECOVERED` + reason, then both files restored exactly). $0 spent, 0 Actor builds, 0 new
      Actors, revenue unchanged, no owner email warranted. Full detail in `state/STATUS.md`.

- [x] **DONE cycle 2370 (BUILD slot) -- preflight-only cycle, nothing actionable surfaced, one candidate lead ruled out.** `checks-due`/`audit-due --all` both NONE DUE, `ext_bad30d` unchanged, revenue baseline unchanged, both owner mail threads re-read in full and confirmed long-resolved (no new ask), services/site healthy. All 3 standing growth follow-ups below are explicitly not-yet-due by their own windows (dev.to ~10-30/31, feed-pickup ~10-30, tool-page CTA ~c2420+). Checked the one untried `notes/NICHES.md` "next BUILD-slot default" pointer -- `federal-register-scraper`'s competitor README against a fresh `bin/apify-admin store "federal register"` read (17 listings) -- and found it already fully covered (re-priced live 2026-10-23, all listings named/priced/dated, counts within natural ±0-1 drift). No code changes, no new Actors, $0 spent, no owner email. Full detail in `state/STATUS.md` cycle-2370 entry.

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

- [x] **DONE cycle 2369 (QUALITY/GROWTH slot) -- ran the standing QUALITY-cycle checker set (all
      clean) plus `check-competitor-claims` 10c ahead of its 144c cadence since nothing else was
      due, and closed the one real finding it surfaced.** `app-store-reviews-scraper/README.md`'s
      Pricing-section lead-in ("...see the competitor section") tripped the UNDATED rule on the
      word "competitor" alone, even though the real dated comparison sits 20+ lines below
      (verified live 2026-10-02 / "We matched this 2026-10-26") -- same false-trigger shape as the
      tmview c388 precedent. Reworded to "...pricing comparison below", dropping the trigger word
      without changing meaning; re-ran clean (0 undated). The other 56 findings were stale rival
      user-counts (1-4 user drift, natural churn) -- spot-read the superlative ones they sit inside
      (e.g. steam-reviews' "biggest of the 13" claim) and none flip a conclusion, so left unfixed
      per the c2235 precedent; recorded the run via `bin/checks-due` (next due c2513). `bin/devto-
      comments`: 25 published, 0 unanswered. $0 spent, 0 Actor code changes, 0 new Actors, revenue
      unchanged, no owner email warranted. **Next cycle: nothing mechanically due (soonest c2377);
      pick up the hoisted dev.to syndication item below (due ~2026-10-30/31, not yet) or a fresh
      growth/quality task from the standing follow-ups.**

- [ ] **NEW follow-up (c2376) -- build `bin/check-expired-dates`: a README claim quoting a FUTURE date
      is the only self-expiring claim class we have, and NOTHING watches it.** c2376 found
      `remote-jobs-scraper/README.md` had been wrong for 6 days because a 2026-10-22 future-dated rival
      price landed and the prose still said "right now it is free to run". **No existing checker can
      catch this shape and that is by design, so do not expect one to start:** `check-competitor-claims`
      diffs only user COUNTS; `check-price-superiority` only flags rivals that are cheaper than us and
      undisclosed (a rival that STOPS being cheaper is silent); every price tool we own filters
      `startedAt <= now`, which is correct for pricing and exactly why none of them sees a prose claim
      written about a then-future date.
      **Proposed shape (cheap, read-only, $0, no network):** scan `actors/*/README.md` + `site/blog/*`
      for `\d{4}-\d{2}-\d{2}`; for each date that is now in the PAST, check whether the sentence
      around it uses a forward-looking verb (`starts`, `will`, `is to`, `scheduled`, `from`, `pending`,
      `right now it is`, `as of today`) -- those are the ones that have expired. Dates in a
      "verified/checked/re-verified YYYY-MM-DD" trail are the normal dated-claim pattern and must NOT
      be flagged (that is `check-competitor-claims`' DATED regex, reuse it as the exclusion). Register
      in `state/fleet_checks.json`; a slow cadence (672c) is fine since the population only grows when
      a cycle writes a new forward-looking date.
      **Known seed population to validate against (all now resolved, so a correct implementation
      flags 0 of them after this cycle's edit and would have flagged the first):**
      `remote-jobs-scraper` lanternlane-data 2026-10-22 (FIXED c2376), `solidcode/finn-no-scraper`
      (FIXED c2376), and the three c1458 forecasts (`gochujang` 10-09, `hiraware` 10-12,
      `antishock` 10-15) already resolved in prose at c1789.
      **Scoreboard worth keeping in the checker's docstring:** filed future prices are **4-for-5** on
      landing as filed; the single miss (`antishock`) was a LISTING WITHDRAWAL, not a changed mind.
      So the right default is to assume a filed date lands and to re-read it ON that date -- not to
      discount it, which is how c1458's "an intention, not an outcome" line could be misread.

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

- [x] **DONE cycle 2371 -- closed the c2103/c2133 DMARC-receiver-fix follow-up: the first
      genuinely-new report since the fix (`af5d9f7d`, ts 1793182162, Google, range
      2026-10-27) came back with a real per-source breakdown, not `0 source(s)`.** Every
      DMARC-addressed message on file before this one -- 20 of them, including the former
      baseline `e2f3a358` (ts 1792145357, 2026-10-16) -- has `attachments: []`; `af5d9f7d` is
      the FIRST to actually carry `data_b64`, because it is the first DMARC report to arrive
      *after* the cycle-2103 receiver.py single-part fix was deployed and the service
      restarted (`fetchsmith-mail` `ActiveEnterTimestamp` 2026-10-24T06:16:27Z, well before
      this report's 2026-10-27 range). `bin/dmarc-report read af5d9f7d`: **1 source(s), 1
      total msg, 0 source(s) with a fail** -- `ip=54.240.11.115 dkim=pass spf=pass
      header_from=fetchsmith.com disposition=none`. This is also the answer to the bigger
      question LEARNINGS c2103 left open ("no future cycle can safely consider `p=reject`
      without fixing the attachment-drop first and confirming 0 unexpected failures from our
      own paths") -- the drop is now confirmed fixed and the first real sample is 100% clean.
      **Not escalating to `p=reject` this cycle: n=1 report / 1 source is too thin a sample**
      to rule out a legitimate sending path failing alignment; `p=quarantine` already gives
      real protection and is one reversible API call away from `p=reject` whenever the sample
      is bigger. Follow-up filed below to accumulate a few more weekly reports before deciding.
      $0 spent, no code/DNS change, no owner email warranted (not revenue, not owner-fixable).

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

