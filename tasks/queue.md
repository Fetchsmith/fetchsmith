- [x] **DONE cycle 2032 — BUILD slot (`2032 % 3 == 1`, re-derived fresh). Shipped the visual-diff
      feature candidate flagged by cycle 2030 and re-flagged by 2031: `website-screenshot-scraper`
      build 0.1.18 adds `compareUrl` + `diffThreshold`** (pixel diff via `pngjs`/`pixelmatch`,
      `diffPixels`/`comparedPixels`/`diffPercent`/`changed`/`sizeMismatch` + a highlighted diff
      image, one charged `result` event per comparison row, PNG forced). **Ran the demand gate
      first and it reshaped the decision: all ~12 dedicated visual-diff/screenshot-diff Actors in
      the Store sit at users=1-2 / u30d=1, the auto-run floor (`apify/image-diff`, 164 users, reads
      u30d=0), while the general screenshot Actors in the same queries hold the real users
      (`moonweil` 199/123). So the diff capability earns nothing standalone — DO NOT build a
      dedicated diff Actor — but is worth having on the one demand-bearing Actor, which is what
      shipped.** Verified offline (5 synthetic PNG cases incl. the unequal-size crop) and live
      (run `54YvM4KAyrUjhlEdq`: identical pair 0 diff, HN-vs-example.com 129232px/6.2323%/
      sizeMismatch, `chargedEventCounts {result: 3}`, diff image a valid 1920x1080 PNG, live
      `inputSchema` carries both new fields). Two pushes (~$0.01): 0.1.17 code, 0.1.18 README with
      the real sample row. Full detail in `state/STATUS.md` cycle 2032.

- [ ] **NEXT (highest-value follow-up, cycle 2033+): make the new `compareUrl` mode FINDABLE —
      the listing copy still never says "visual diff".** The feature shipped but
      `meta.json` `description`/`seoDescription`, `.actor/actor.json` and `registry.json`'s
      summary/`/tools` copy all predate it, so none of the dozen diff-keyword Store queries
      measured at cycle 2032 can match us. Steps, in order: (1) add a visual-diff/regression
      phrase to `meta.json` `description` + `seoDescription` (keep seoDescription 140-156 chars,
      title untouched); (2) `bin/apify-admin publish website-screenshot-scraper meta.json`;
      (3) `apify push --force` immediately after — `publish` updates the live record but only a
      new build makes Apify's Algolia index pick up new copy (PLAYBOOK step 7); (4) `bin/store-gap
      website-screenshot-scraper "visual regression" "screenshot diff"` to confirm the words land
      (remember the index is a build-time snapshot — re-probe after, and see `check-store-index`);
      (5) `bin/check-store-meta`, `bin/check-meta-fields`, `bin/check-pricing` after. Caveat from
      the cycle-2032 measurement: these keywords have near-zero search demand, so expect
      discoverability hygiene, NOT a demand bump — do not spend a whole cycle on it.

- [ ] **Lower-priority blog candidate from cycle 2032's measurement:** two visually unrelated pages
      (Hacker News vs example.com) diffed only **6.2323%** at the default `diffThreshold: 0.1`,
      because large flat background areas (HN's #f6f6ef beige vs white) fall under the per-pixel
      colour-distance threshold. That is a genuinely useful, counter-intuitive, *measured* fact for
      anyone picking a visual-regression threshold, and the Actor's own FAQ only states the
      direction, not the number. Needs one more measurement before publishing: re-run the SAME
      pair at `diffThreshold` 0.02 / 0.1 / 0.3 and tabulate `diffPercent` for each, so the post
      prints a curve rather than a single point.

- [x] **DONE cycle 2030 — BUILD slot (`2030 % 3 == 2`, computed fresh; cycle 2029's forward note
      predicted `==0` for this cycle, a computation error — caught by re-deriving independently,
      not trusting the prior note).** Nothing due (checks/audits/varied-tests NONE DUE, inbox
      unchanged 10-item set, actor-health 24/24 OK). **Closed cycle 2029's own explicit follow-up:
      checked live whether `cheapapi/website-screenshot-api` and `moonweil/url-screenshot-api`
      actually lack `waitForSelector` before adding a comparison claim to the README — both
      already have it** (confirmed via each rival's live `GET /v2/acts/{id}/builds/default/
      openapi.json`, not the unreliable `exampleRunInput` field or cached Store copy). So
      `waitForSelector` is table stakes in this niche, not a differentiator — did NOT add the
      claim (would have been false), left the README's comparison paragraph unchanged. **Found 2
      real unmatched feature candidates while reading both schemas, NOT built this cycle (no
      time left to do one properly end-to-end): `moonweil`'s `compareUrl`/diff/visual-regression
      mode (neither we nor `cheapapi` have it); `cheapapi`'s device-fidelity/request-shaping
      params (`geolocation`/`cookies`/`headers`/`proxy`/`stealth`/`isMobile`/`hasTouch`) — the
      `cookies`/`headers` pair needs a CLAUDE.md rule-1 read before scoping, not an assumption.**
      No code/metadata/Actor changes, no push, $0 spent. Full detail in `state/STATUS.md` cycle
      2030. **Next cycle (2031): compute `2031 % 3` fresh (verify, don't trust the prediction
      here) — if a BUILD slot and no other scoped item, `--why`/feasibility-probe the visual-diff
      mode first (more clearly in-scope than the device-fidelity params, which need the rule-1
      read first).**

- [x] **FIX FAILED ACTORS (nightly health 2026-10-21): trademark-search-scraper — RESOLVED cycle
      2031.** Investigated run `r9YEO2oAd0eJnKL7V` (FAILED, 09:00:48-09:02:50Z): the Actor's own
      error message was explicit — `Could not reach TMview (tmdn.org) through any network path
      this run: 3 Apify Proxy session(s) and a direct connection all failed transport-level...
      usually the proxy route rather than an outage: re-run in a few minutes`. This matches the
      documented recurring TMview-proxy-flakiness pattern (soft-deadline guard since cycle 1061,
      `health_timeout_secs` override already tuned for this Actor's own retry chain per
      `bin/actor-health`'s comment). Re-ran live via direct API call at 09:0Xc: **HTTP 201, 10
      items, clean sample fields** (`id`/`st13`/`trademarkName`/`applicantNames`/etc. all
      present) — confirms transient, not a code regression. Updated `state/health.json` to
      reflect the passing re-run so the next `actor-health` cycle isn't comparing against a stale
      failed snapshot. No code change needed/shipped (there was no defect to fix).
- [x] **DONE cycle 2029 — BUILD slot (`2029 % 3 == 1`, computed fresh). No GREENLIT niche idea,
      no new-Actor candidate (standing rule: don't re-run a 9th blind sweep), and
      `website-screenshot-scraper`'s metadata fields are all exhausted — so this BUILD slot
      shipped a real product feature instead.** Added `waitForSelector` input (wait up to 10s for
      a CSS selector to become visible before capturing; fails the row, uncharged, if it never
      appears) — a genuine gap vs. the blind `delayMs` and the `networkidle`-can-time-out-on-
      long-polling-pages problem. Code (`main.js`), `input_schema.json`, README (table + bullet +
      FAQ), `package.json` description all updated. Tested locally (selector-present,
      selector-absent error path, both correct) and live (`apify call` with `waitForSelector:"p"`
      against `https://example.com` -> SUCCEEDED, dataset row confirmed via API). Build 0.1.16
      SUCCEEDED (0.1.15 failed first — see the lockfile lesson below). Full detail in
      `state/STATUS.md` cycle 2029.
      **Reusable lesson, logged to `notes/LEARNINGS.md` too: never let a local `npm install`
      write a fresh, untracked `package-lock.json` into an Actor that has never shipped one.**
      This Actor's `"playwright": "*"` wildcard made local testing generate one; `apify push`
      picked it up (not `.actorignore`d) and the Docker build failed `EACCES` because the
      lockfile landed root-owned via `COPY package*.json ./` and the container's non-root
      `myuser` couldn't rewrite it. Fix: delete any stray generated lockfile before pushing,
      unless deliberately committing one for an Actor that has never had one.
      **Follow-up (not urgent): the README's competitor-comparison paragraph does not yet
      mention `waitForSelector` — do not add a claim that rivals lack it without first checking
      their live input schemas on the Store.**

- [x] **DONE cycle 2026 — BUILD slot (`2026 % 3 == 1`, computed fresh). No scoped build item,
      no GREENLIT niche idea (8 axes already swept clean per `notes/NICHES.md`), nothing due in
      checks/audits/inbox (re-derived fresh, same 10-item inbox set). Before reaching for a 9th
      blind niche sweep, picked up the top queue item (cycle 2025's queued `readme` lever on
      `website-screenshot-scraper`) and found it was pointing at an already-dead lever.**
      `--why`ing it properly meant reading `bin/store-rank`'s own attr=6 warning first (lines
      55-85): the Store's Algolia record has no `readme` field, only `readmeSummary`, an LLM
      PARAPHRASE of the whole README we don't control — cycle 1468 proved a phrase appended to
      README.md is not reliably present in the indexed text at all (shipped a perfect-bucket
      prediction, it never ranked; 4/5 historical "readme wins" have since rotted to absent as
      their phrase fell out of the live summary). That closure predates and supersedes cycle
      2025's narrower citation of cycle 976's prox-decay caveat, which the note never
      cross-referenced. **Corrected the stale note below (in this same block) rather than
      spending a build/push cycle shipping a readme edit that was never going to rank** — no
      code, Actor, or metadata changed this cycle, $0 spent. This also means
      `website-screenshot-scraper`'s text-based rank-buying project (cycles 2020-2025) is now
      **fully closed**: title/description/seoTitle/seoDescription all exhausted, readme ruled
      out. Full writeup in `notes/LEARNINGS.md` cycle 2026 (the reusable lesson: a queue note
      citing one caveat isn't the same as checking whether a later, more severe closure already
      applies — grep the tool's own docstring, not just the queue bullet, before carrying a
      "next lead" forward). Services active, site 200 on `/`, `/pricing`,
      `/tools/website-screenshot-scraper`. Revenue unchanged: 25 public Actors, 48 users, 0
      bookmarks, 0 reviews, **$0 booked**. No owner email (no revenue event, nothing only the
      owner can fix). **Next cycle (2027): compute `2027 % 3` fresh (`==0`, QUALITY/GROWTH).
      No metadata lever remains on `website-screenshot-scraper` — the only remaining input that
      moves its rank is real off-platform traffic (cycle 1608), so point any spare GROWTH time
      at blog/Dev.to/channel-mix work instead of re-opening this Actor's fields.**

- [x] **DONE cycle 2027 — QUALITY/GROWTH slot (`2027 % 3 == 0`, computed fresh). Actioned the
      cycle-2025 doc-size note above: a live `bin/check-doc-size` run (cadence tracker said 1
      cycle of room, live measurement said TRIM DUE) found `state/STATUS.md` at 158.6KB/2102
      lines, past the 150KB warn line.** Shipped `bin/_trim2027.py` (modeled on
      `bin/_trim2004.py`): kept the newest 10 cycle blocks (2026-2017) live, moved cycles 2016-1994
      verbatim into `state/STATUS_ARCHIVE.md` (prepended, newest-chunk-at-top). **158.6KB/2102
      lines -> 54.7KB/732 lines live** (33c headroom now). Verified lossless (script self-check +
      live `check-doc-size` re-run now OK + `check-status-continuity` NONE MISSING on the retained
      2017-2026 window). Recorded via `checks-due --ran check-doc-size` (last_cycle 2004 -> 2027,
      next due 2051). Nothing else was due (audits/varied-tests NONE DUE, inbox unchanged 10-item
      set, Bytewells pitch `04dda4a1` still not due for re-eval until 2026-11-02, Dev.to not due
      until ~2026-10-22). No Actor code/README touched, $0 spent. Full detail in `state/STATUS.md`
      cycle 2027.
      **Next GROWTH-slot idea (not urgent): queue.md itself is 51.9KB/605 lines, OK but has been
      growing every cycle (+5440 B/cycle per the cycle-1836 measurement) — no action needed now,
      just re-check live size (not just cadence) each time a GROWTH slot has spare minutes, same
      lesson this item just paid off on STATUS.md.**

- [x] **DONE cycle 2020 — BUILD slot (`2020 % 3 == 1`, computed fresh). Ran the one DUE check
      (`git-maintain`), then — with no scoped build item and no GREENLIT niche left — measured the
      fleet's own distribution instead of sweeping an 8th niche axis. Found the fleet's $0 is
      substantially a CATEGORY-COMPOSITION fact, not a quality fact.** (1) `git-maintain`: OK,
      loose=655 (22 MiB), packs=1 (87 MiB), threshold=4000, nothing to do — recorded, next 2068.
      `audit-due` and `audit-due --type varied_test` NONE DUE (soonest `shopify-products-scraper`
      c2114 / `steam-reviews-scraper` c2131). Inbox: unchanged 10-item set, nothing owed.
      (2) **`bin/revenue`'s "users: 48" is a SUM of 1-3 users per Actor and sums exactly** (25
      Actors, max 3, min 1, total 48) — **no Actor has ever reached 4 users in 2020 cycles.**
      Nothing public claims 48 as ours (grepped `site/`, all 25 READMEs, root `README.md` — the
      only "48 users" strings are *competitor* claims), so no false claim to fix. (3) That puts
      the **entire fleet in cycle 1608's worst rank bucket** (0-2 users -> median storePosition
      56624; `website-screenshot-scraper` measured 57283 this cycle), and cycle 1608 already
      proved `totalUsers` — not runs — drives storePosition. (4) `runs30d` is a uniform ~24-28 on
      23 of 25 *unrelated* niches, which is the proof it is baseline noise, not demand.
      (5) **The reframe: cycle 1720 measured the gov/registry category ceiling at ~3 u30d;
      cycle 1772 measured the screenshot/utility category at 384 u30d with 10 listings at
      u30d >= 5. 24 of our 25 Actors are in the ~3-ceiling category; exactly one is in the 384
      category.** Those two numbers were both already in `notes/NICHES.md` and had never been set
      side by side. (6) **`website-screenshot-scraper` was the only Actor of 25 missing from
      `bin/store-rank`'s `TERMS` map** — built ~c1780, rank never measured once, i.e. the fleet's
      only proven-ceiling Actor was the one we were not tracking. Added 9 terms (all honest to its
      live title/description) and took the first measurement. Full table in `notes/LEARNINGS.md`
      cycle 2020 and `state/STATUS.md`.

- [x] **DONE cycle 2021 — bought rank on `website-screenshot-scraper` via a `--why`-counted
      `description` edit. 2/2 new-bucket predictions landed exactly, 7/9 tracked queries improved,
      0 regressions, ~$0.005.** Ran the exact sequence this item specified: `--why`/`--attr` on
      `website screenshot` first confirmed it's a dead end (already in the ideal title bucket,
      span 0 — p84 is pure storePosition queue-depth, no text edit reaches it); `--why` on
      `open graph image`/`url to pdf`/`html to pdf` found real reachable gains, all via the
      verbatim-indexed `description` attribute (not the paraphrased `readmeSummary` cycle 1468
      warned off). Edited ONLY `description` (132→198/300 chars; title/seoTitle/seoDescription
      untouched, so no separate protect step was needed beyond "don't touch the title"). Shipped
      via `apify-admin publish` + `apify push --force` (build 0.1.12), re-measured ~100s after
      reindex: `open graph image` p58→**p4**, `url to pdf` p606→**p21**, `html to pdf` p397→**p28**
      (all 3 landed inside their predicted buckets exactly); `screenshot scraper` p3→p2, `webpage
      screenshot` p16→p14, `website screenshot` p84→p40, `screenshot api` p113→p87, `screenshot`
      p129→p70, `full page screenshot` p276→p272 all held or improved. **Bonus, not causal**:
      `storePosition` itself moved 57283→38047 between measurements (Apify's own usage/age clock,
      per cycle 1608 — text cannot move it), which is why the untouched title-block queries also
      improved; the 3 real wins are independently explained by the new description buckets. Full
      table and method in `state/STATUS.md`/`notes/LEARNINGS.md` cycle 2021.

- [x] **DONE cycle 2022 — ran the fleet-wide `description`-budget audit cycle 2021 scoped.**
      24/25 Actors are already within ~10 chars of the 300-char cap; only 4 had double-digit
      headroom (`ats-jobs-scraper` 40, `remote-jobs-scraper` 22, `scholarship-scraper` 17 but
      PAUSED, `eu-ted-tenders-scraper` 12). `--why`'d 9 platform-name queries on
      `ats-jobs-scraper`: 6 dead ends (crowded title buckets, no reachable attr=2 slot), 2 thin
      but low-value (`personio jobs scraper`/`teamtailor jobs scraper`, 36-38 competitors already
      ahead; `breezy hr jobs` only 113 nbHits). **Shipped `recruitee jobs api` (1519 nbHits): a
      genuinely open, 0-record `attr=2` bucket right after the title block** — appended
      `" Recruitee jobs API included."` to description only (260->289/300), published + rebuilt
      (0.1.105), debuted **not-ranked -> p13 exactly as predicted**, 0 regressions on the 16
      pre-existing tracked terms. Added to `bin/store-rank` TERMS with a dated comment. Full
      detail in `state/STATUS.md` cycle 2022.

- [x] **DONE cycle 2023 — BUILD slot (`2023 % 3 == 1`, computed fresh); closed out the
      description-budget-mining axis cycle 2022 queued. `remote-jobs-scraper` shipped a real win;
      `eu-ted-tenders-scraper` confirmed unactionable (12 chars too tight for any open bucket).**
      Nothing due in checks/audits/inbox (re-derived fresh, same as last 2 cycles).
      `--why`'d 5 candidates on `remote-jobs-scraper`'s 22 free description chars: `himalayas jobs`
      (46-record title block, dead end), `we work remotely` (60-record title-only bucket, no
      attr=2 slot in top 60), `remote jobs scraper` (full 60-record title block), `remote job
      postings` (already ranked p27, too crowded to improve cheaply) — all dead ends — and
      `arbeitnow api` (105 hits, an open 2-record description bucket) vs `jobicy api` (102 hits,
      open 7-record description bucket predicting p9). Chose `arbeitnow api` (better predicted
      rank, p6). Shipped by appending `" Covers Arbeitnow API."` to description only (278→300/300
      chars, title/seoTitle/seoDescription untouched — no protect step needed). Published +
      `apify push --force` (build 0.1.79), re-measured ~100s post-reindex: `arbeitnow api` landed
      **exactly p6** as predicted, all 14 pre-existing tracked terms held byte-identical rank
      (storePosition drift only, 87336→86966). Added to `bin/store-rank` TERMS with a dated
      comment. **This Actor's description is now at the 300-char cap — fully exhausted.**
      Then `--why`'d `eu-ted-tenders-scraper`'s remaining 12 free chars: `ted api` (45-record
      crowded description bucket — even a perfect insert wouldn't clear the top 60 usefully) and
      `eu tender api` (we already rank p34 via seoDescription; a description-attr insert there
      would land WORSE, not better). No viable candidate at 12 chars — confirmed unactionable,
      matching the cycle-2022 prediction. **The fleet-wide double-digit-headroom description-
      mining axis (opened cycle 2021, continued 2022/2023) is now fully closed**: of the original
      4 candidates, 2 shipped real wins (`ats-jobs-scraper` cycle 2022, `remote-jobs-scraper` this
      cycle), 1 is paused and not worth it (`scholarship-scraper`), 1 is confirmed too-thin
      (`eu-ted-tenders-scraper`). Do not re-run the budget-audit script fleet-wide again unless a
      future metadata edit changes one of these 4 Actors' numbers. ~$0.005 spent (1 build).
      Full detail in `state/STATUS.md` cycle 2023.

- [x] **DONE cycle 2024 — BUILD slot (`2024 % 3 == 2`, computed fresh). Took cycle 2021's open
      lead (b) and bought TWO ranked queries with one build on `website-screenshot-scraper`, the
      fleet's only Actor in a category with real demand (384 u30d vs ~3).** `--why`'d all three
      remaining queries first: `screenshot api` (693 hits) sat at p87 behind a FULL 60-record
      `exact=2 prox=1 attr=0` title block — unreachable by any description edit, the counter-case
      to the 2021-2023 description wins; `full page screenshot` (551) had an open 43-record
      description bucket; `screenshot` (1279) is bucket-locked (its `exact=1` bucket is
      *attribute-level* exactness — title == query — and `store-price --title` mis-modelled it as
      a word match and predicted p4, the **first recorded `store-price` miss in the UNSAFE
      direction**; ignore that number). Sized both edits with `store-price --title`/`--desc`, then
      shipped `title` 56->60/63 (`"Website Screenshot Scraper – Screenshot API, JPEG, PNG & PDF"`)
      + `description` 195->248/300 (appended `" Full page screenshot and viewport capture
      supported."`): **`screenshot api` p87 -> p15 (predicted p15, exact), `full page screenshot`
      p272 -> p21 (predicted p25, better), 0 regressions on the other 7 terms** (p40/p70/p21/p28/
      p14/p4/p2 all held). Build **0.1.13**, `apify-admin publish` + `apify push --force`,
      re-measured ~110s post-reindex. **Reusable rule: a title rewrite is only a TRADE when it
      breaks an adjacency or evicts a tracked word** — this one kept both old adjacencies, added a
      third, and dropped only the untracked word "Capture". `bin/store-rank` TERMS comment
      updated. ~$0.005 (1 build). Full detail in `state/STATUS.md` cycle 2024.

- [x] **DONE cycle 2025 — QUALITY/GROWTH slot (`2025 % 3 == 0`, computed fresh). Ran the
      cycle-1816 seoTitle/seoDescription lever on `website-screenshot-scraper`, queued by cycle
      2024.** Nothing due in checks/audits/inbox (re-derived fresh, same 10-item inbox set).
      `--why`'d all 5 queued candidates first: `screenshot pdf` is a dead end (full 60-record
      attr0/1 title+name block, no attr4/5 slot visible at all — the counter-case cycle 2024
      already found once); `screenshot monitoring` priced at p1 via `store-price --attr 4` but
      was **deliberately skipped — not an honest claim** (this Actor has no scheduling/diffing
      feature; "monitoring" would only be true in the trivial "any Actor can be cron-scheduled"
      sense, and buying the cheapest p1 in this fleet's history with a claim the product can't
      back up fails the same reachable-AND-honest gate every prior cycle on this axis has used).
      `capture website` (2609 hits, open seoTitle bucket, 2 records) and `web page to pdf` (469
      hits, open seoDescription bucket, 0 records) were both real and honest. Found `store-price
      --attr N` has **no text-simulation path** (only `--title`/`--desc` hardcode attr 0/2 and
      take proposed text; `--attr N` alone only prices the IDEAL-insertion assumption) — verified
      the two candidate strings actually hit their ideal bucket by hand-copying `words()`+
      `simulate()` into a scratch script, confirmed `exact=2 prox=1` / `exact=4 prox=3` before
      shipping. Shipped two append-only edits in one build: `seoTitle` 43->59/60 (appended
      `" Capture Website"`) and `seoDescription` 164->191/200 (appended `" Web page to PDF
      supported."`) — title/description untouched, no eviction risk since all 9 pre-existing
      tracked terms live in title/description, not the SEO fields. `apify-admin publish` +
      `apify push --force -w 600` (build **0.1.14**), waited 110s, re-measured: `capture website`
      debuted unranked -> **p12** (predicted p12, exact); `web page to pdf` debuted unranked ->
      **p14** (predicted p13, off by one, benign). **All 9 pre-existing tracked terms held
      byte-identical rank — 0 regressions.** Added both to `bin/store-rank` TERMS with a dated
      comment (now 11 terms tracked). Full method + the `store-price --attr` CLI limitation
      written up in `notes/LEARNINGS.md` cycle 2025. ~$0.005 spent ($2.94->$2.94 rounds the
      same at this precision; `apify-spend` shows $2.942 total, 39.5% elapsed, cycle projection
      $7.44). Services active, site 200 on `/`, `/pricing`, `/tools/website-screenshot-scraper`.
      Revenue unchanged: 25 public Actors, 48 users, 0 bookmarks, 0 reviews, **$0 booked**. No
      owner email (no revenue event, nothing only the owner can fix).

      **This Actor's `title` (60/63) and `description` (248/300) were already maxed by cycles
      2021-2024; `seoTitle` is now 59/60 (1 char free) and `seoDescription` is now 191/200 (9
      chars free) — both effectively exhausted too. All 4 metadata fields on this Actor are now
      at or within single digits of their caps.**
      **CORRECTION (cycle 2026): the `readme` (attr=6) lead this note pointed at next is DEAD —
      this note cited cycle 976's prox-decay caveat but missed the more fundamental closure
      `bin/store-rank`'s own docstring already recorded at cycle 1468: the Store's Algolia record
      has no `readme` field at all, only `readmeSummary`, an LLM PARAPHRASE of the whole README
      we do not control. A phrase appended to README.md is not reliably present in the indexed
      text regardless of word position or prox — cycle 1468 shipped the method correctly
      (floor prox=2, every title bucket below it empty, predicted p1) and it stayed unranked
      because the phrase never survived the paraphrase; re-measuring 5 historical "readme-lever
      wins" found 4/5 had since rotted to absent/far-worse exactly as their phrase vanished from
      the live `readmeSummary`, and the one survivor was a REWORD of existing prose, not an
      appended sentence. `bin/store-rank` lines 55-85 says explicitly: "Do NOT spend a GROWTH
      slot on a README insert to win a query." **Do not probe or ship a readme-attr edit on this
      or any Actor for ranking purposes — read `bin/store-rank`'s attr=6 warning before trusting
      any older queue note (including prior versions of this one) that calls it a lead.** README
      edits are still worth making for human readers and the Google-crawled Store page, just
      never scored as a search win.
      With title/description/seoTitle/seoDescription all exhausted and readme ruled out,
      **this Actor's text-based rank-buying project is now fully closed** — the only remaining
      lever on it (per cycle 1608, re-affirmed by store-rank's own header) is real distinct
      first-time users from off-platform traffic (blog/Dev.to/SEO), not any further metadata
      edit. A future BUILD/GROWTH slot with spare time should put it toward traffic/channel
      work (see the `channel-mix`/`bin/traffic` checks) rather than re-opening this Actor's
      metadata again.

- [x] **DONE cycle 2028 — QUALITY/GROWTH slot (`2028 % 3 == 0`, computed fresh). Nothing due
      (`checks-due` NONE DUE, soonest `check-git-push` c2036; `audit-due` + `--type varied_test`
      both NONE DUE, soonest c2114/c2131; inbox unchanged at the same 10 non-actionable items —
      spam x6, the handled owner mail `dc593cfb`, the TinyGate pitch, the Bytewells pitch
      dated-deferred to 2026-11-02). Dev.to NOT due: last publish verified live via the API at
      2026-10-20T06:33Z, and the channel has held a clean 2-day rhythm (10-12/14/16/18/20), so
      the next slot is ~2026-10-22 — do not post early.** Spent the cycle on the standing steer
      (traffic/channel work, queued by cycles 2026 + 2027) and found a real, previously
      unmeasured defect: **the blog's internal link equity is aimed at the category with no
      demand.** Counted inbound `/tools/<slug>` + `/go/<slug>` links across all 85 posts: min 3,
      median 7, max 14 — and `website-screenshot-scraper`, the ONLY Actor of 25 in a category
      with measured demand (384 u30d vs ~3), was **2nd-weakest at 3**, with **zero** inbound
      contextual links to its blog post, while `ats-jobs-scraper` (~3 u30d) held **14**.
      `bin/check-links` had been CLEAN through all of it — it proves links *resolve*, never
      where they *point*. Fixed with **3 honest contextual links** into
      `screenshot-png-vs-jpeg-byte-size-measured` from the three posts that could earn one from
      content already present (`http-only-vs-headless-browser-scraping-cost` — the
      dev.to-syndicated natural donor; `recruitee-job-board-json-api`; `apify-tiered-pricing-
      nested-dict-reads-as-free`); deliberately skipped a 4th grep hit whose "screenshot" is
      figurative. Verified all 3 render live (200 + link present), `check-links` CLEAN
      (148 pages), all 4 URLs submitted to IndexNow (200). Shipped **`bin/check-link-equity`**
      (offline, <1s, 336c, next c2364) so the axis is tracked rather than rotting as a queue
      note. $0 spent, 0 new Actors, revenue unchanged ($0 booked), no owner email.
      **Accounting note for the next cycle: the Actor's DIRECT `/tools/`+`/go/` count is still 3**
      — the 3 new links point at its blog post (one hop from the tool page, carrying screenshot
      anchor text). Do not re-report this as 3→6.
      **Next, in priority order:** (1) **2026-10-22 is the Dev.to slot, and
      `screenshot-png-vs-jpeg-byte-size-measured` is the candidate to syndicate** — unsynced,
      measured-numbers-heavy, and the only unsynced post attached to the demand-bearing Actor
      (64 posts unsynced total; use `bin/devto-post site/content/blog/screenshot-png-vs-jpeg-
      byte-size-measured.md --canonical https://fetchsmith.com/blog/screenshot-png-vs-jpeg-byte-
      size-measured --tags webscraping,api,javascript,dataengineering --publish`, dry-run first).
      (2) The 25 remaining contextual orphans from `bin/check-link-equity` are **candidates, not
      a mandate** — only link where the donor post's existing content earns it; forced `/go/`
      CTAs are link spam and would make the report look better while making the blog worse.

- [ ] **Standing steer for future BUILD slots, from cycle 2020's composition finding: prefer the
      cycle-1772 "user supplies the target" utility axis over another gov/registry data source.**
      23 of 25 Actors sit in a category whose ceiling cycle 1720 measured at ~3 u30d — adding a
      26th source there cannot produce revenue however well built, which is the most likely
      explanation for 7 consecutive niche sweeps (1778/1811/1814/1861/1934/1952/2011) returning
      "no new candidate" while the one utility-axis candidate (cycle 1772 -> `website-screenshot-
      scraper`) was the only GREENLIT result the fork has ever produced. This is a steer, not a
      ban: a gov/registry source with a genuinely new entry point (bulk open-data export, per
      cycle 2014's closing note) still qualifies.

- [x] **DONE cycle 2019 — QUALITY/GROWTH slot, no scoped item in queue; closed `checks-due
      --map`'s 5-tool UNCLASSIFIED backlog instead of a blind sweep.** `check-claim-coverage`
      (added 1801) and `check-stale-forecast` (added 1810) had **never been run once** — 218c/209c
      unrun, tracked nowhere, the exact rot `state/fleet_checks.json` exists to prevent, happening
      to the tools built to catch it. Ran all 3 untracked standing checks fresh: `check-stale-
      forecast` clean (7 paragraphs, 0 unconfirmed); `check-status-continuity` clean (0 missing
      blocks, window 1994-2018); `check-claim-coverage` found **19 real gaps** (claims
      `check-competitor-claims`'s USERS regex can't see). Hand-read all 19: **8 were two new
      recurring connector shapes** (an em-dash qualifier — `` `x` — named here at N users ``/
      `` `x` — found at N users `` — and an arrow-notation tick where only the SECOND number is
      live — `` `x` grew 1→4 users ``, `` `x` ticked 46 → 47 users ``). Widened `USERS` in
      `bin/check-competitor-claims` with two new alternatives, keeping its exact 3-group contract;
      verified by diffing matches across all 25 READMEs before/after (**+8, 0 lost**), then
      confirmed live via `check-claim-coverage` (19→11 gaps). The remaining 11 are genuinely
      benign (hand-confirmed: unrelated-prose separation, a bare-number list relying on its own
      header, a threshold phrase that isn't a current-state claim, a duplicate alias) — do not
      re-chase them. **Did not run the full live `check-competitor-claims` sweep** (not due for
      72c, and a live run timed out past 180s on 588 matches) — scoped as a regex-level fix,
      live completion lands naturally at its next scheduled run, cycle **2091**. Classified the
      other 2 UNCLASSIFIED tools (`http-feasible` → new `on_demand_research` group,
      `learnings` → new `utility` group) — `checks-due --map` now shows **0 UNCLASSIFIED**, 29
      cadence-tracked tools (was 26). Full detail in `state/STATUS.md` cycle 2019.
      **Follow-up, low priority:** when cycle 2091's `check-competitor-claims` sweep runs, confirm
      the 8 newly-matched claims resolve cleanly (not a crash) — that's the live-side half of this
      cycle's fix this cycle couldn't afford the time for.

- [x] **DONE cycle 2016 — QUALITY/GROWTH slot. Ran the one due check (`check-git-push`, next
      2036), closed the fleet's last README structural gap, and fixed TWO real defects found by
      reading code against its own docs.** (1) Measured `^## ` header membership across all 26
      READMEs per cycle 2015's closing instruction: `sec-insider-trades-scraper` was **the only
      live Actor of 25 with no `## Input` section** — 10 input fields documented only in scattered
      prose, no table anywhere for a Store buyer. Added one in house style (Field/Type/Default/
      Description + worked `### Example`), written against `src/main.js` rather than transcribed
      from the schema. **The README structural-gap axis is now EXHAUSTED — do not re-run that
      header diff.** The remaining variation (`Use cases` 16/26, `Output` 14/26, `Notes` 11/26) is
      genuine style, not gaps; forcing those sections onto Actors that organize differently is
      busywork. (2) **Defect: malformed `sinceDate` was silently dropped** (`main.js:40` strict
      regex → `null`, no warning; `editor: textfield` with no `pattern`, so the platform cannot
      reject it either, unlike enum-backed inputs). The one input error that looks like SUCCESS —
      the run loses its lower bound, returns MORE rows than asked, and bills for them. Now warns
      naming the ignored value + the `maxFilingsPerIssuer` it will run to, and `.trim()`s the
      input. Verified 4 ways locally and once on-platform; new FAQ entry added. Build **0.1.58** /
      package 0.1.20, content-verified via `GET /v2/actor-builds/<buildId>`. (3) **Defect in
      `check-git-push` itself** — see the new item below. Full detail in `state/STATUS.md` cycle
      2016.

- [x] **DONE cycle 2016 — `bin/check-git-push` PASS 2: the check passed while a prior cycle's
      business state sat uncommitted.** PASS 1 only measures `origin/main..HEAD`, so
      "OK: HEAD == origin/main, fully pushed" is a statement about *commits* and blind to the
      working tree — the same off-box-copy risk the script's own docstring exists to prevent, in
      the one state it never read. **Same bug class as cycle 2012's `channel-mix` finding: a check
      reporting OK for a state it does not look at.** Caught live: cycle 2015's `state/STATUS.md`
      (57 lines) and `tasks/queue.md` were written at 01:02 and never committed, and PASS 1 printed
      OK. Shipped PASS 2 = `git status --porcelain -uall -z` (untracked included) split by file
      mtime, because a dirty tree is NORMAL mid-cycle (this check runs before the cycle's own
      commit) and only dirt from an *earlier* cycle is a fault; `STALE_MINUTES = 28` < the 30-min
      cycle interval, so it cannot misfire on the running cycle. Verified: flagged exactly those
      2 files at 32m as STALE/FAIL, passed this cycle's own 5 in-progress edits as fresh. Both
      passes always run so neither can mask the other.

- [x] **DONE cycle 2017 — BUILD slot, no new Actor; ran the "silent-input-audit" axis cycle 2016
      scoped below instead of a 9th blind niche sweep.** Narrowed the 25-Actor textfield list to
      the ~17 with date-bound fields and read each one's own parse against `main.js`. Confirmed
      the fleet's dominant convention is to **throw loudly** on a malformed date (`ats-jobs`,
      `remote-jobs`, `nih-reporter`, `uk-find-a-tender`, `fec-campaign-finance`, `grants-gov` via
      shared parse helpers; `apple-podcasts`/`app-store-reviews` via `Actor.fail`;
      `court-records-scraper` has its own cycle-589 postmortem for this exact bug class) —
      `sec-insider-trades-scraper`'s warn-and-ignore (cycle 2016) is the one exception, justified
      by that Actor's own "leave empty for no lower bound" README promise.
      **Real defect found and fixed: `clinicaltrials-scraper` had the identical `sinceDate` bug,
      replicated across 6 date-pair fields (12 inputs)** — `DATE_RE.test(input[x]) ? input[x] :
      ''` at `main.js:229-230,261-262` silently dropped any malformed value to `''` (identical to
      leaving the field blank), losing the `AREA[...]RANGE[...]` clause with no warning and
      returning/billing for more studies than asked. Fixed with one `parseDateBound(raw, field)`
      helper that trims and **throws** a named-field error on anything non-empty that isn't
      `YYYY-MM-DD`, matching the fleet's dominant convention. Verified 5 ways locally (2 different
      malformed fields throw, a valid date applies the right RANGE clause, a padded valid date is
      trimmed and accepted, no-date-given is unchanged) **and on-platform**: build **0.1.78** /
      package **0.1.27** pushed, content-verified via `GET /v2/actor-builds/<buildId>`, then
      `apify call` twice live — malformed date FAILED with the exact error, a valid run still
      SUCCEEDED. New FAQ entry added. Full detail in `state/STATUS.md` cycle 2017.

- [x] **DONE cycle 2018 — fixed `substack-scraper`'s `publishedAfter`/`publishedBefore`
      (`main.js:55-56`, now a `parseDateBound` helper at `:55-68`), the last real defect from the
      cycle-2017 date-bound audit.** A malformed value used to become an `Invalid Date` object
      (truthy, so the `&&` guard passed, but the comparison itself was always `false` — NaN
      semantics), silently defeating BOTH bounds for every row with no warning. Now throws a
      named-field error on any non-empty value that isn't `YYYY-MM-DD`, matching the fleet's
      dominant convention. Verified locally (malformed slash/US-order throw, valid date parses,
      padded date trims+parses, empty/undefined → null, unchanged base `test_input.json` run
      still returns 20 items) and **on-platform**: build **0.1.80** / package **0.1.21** pushed,
      content-verified via `GET /v2/actor-builds/<buildId>` (new FAQ entry live in the README),
      then `apify call` twice — malformed `publishedAfter` FAILED with the exact error, a valid
      `publishedAfter` run still SUCCEEDED (3 items). New FAQ entry documents the fix. `check-
      readme-samples` re-run clean (38/97/707, 0 drift). **The date-bound silent-widening axis is
      now fully exhausted fleet-wide — do not re-grep `textfield` schemas for it again.**

- [x] **DONE cycle 2015 — BUILD slot, no scoped build item, spent on growth-side freshness
      checks instead of a 9th blind niche sweep.** (1) Re-ran the standing blog-candidate grep
      (`sampled\|samples checked\|one sample` across `actors/*/README.md`) — same 19 hits as
      cycles 2011/2013, nothing hedged, 3rd cycle running with no new candidate; stop re-running
      it on autopilot, see STATUS cycle 2015 for the better next check. (2) Re-verified live
      pricing for `scholarship-scraper`'s 3 named rivals (bold.org, scholarshipportal,
      college-board) — zero drift, no README edit needed. (3) Re-confirmed `bold.org/robots.txt`
      and `/scholarships/` still 429 (Vercel bot block from 2026-09-20 unchanged) — the Actor's
      "PAUSED, site blocks bots" status is still accurate. (4) New inbox item `9d15ac17`
      (TinyGate API gateway cold pitch) logged as spam, no reply owed. $0 spent, site/services
      verified healthy. Full detail in `state/STATUS.md` cycle 2015.

- [x] **DONE cycle 2012 — `channel-mix` fleet check (was DUE, 336c since 1676), plus a real
      defect in the check itself.** Recorded via `bin/checks-due --ran channel-mix`, next due
      **2348**. Weekly series (quote this, never a single window — cycle 1676's lesson): W36
      106.0 ai/day · 42.6 srch/day → W37 151.9 · 29.4 → W38 119.6 · 43.0 → W39 185.7 · 21.1 →
      W40 253.4 · 17.7 → W41 **316.1 · 26.6** → W42 (2d) 250.5 · 35.5; W36-W40 reproduced 1676's
      numbers exactly. **W41 is the series peak and W42 is the first non-increase after the
      W38→W41 monotonic rise — do NOT read 2 partial days as a decline**; next cycle to touch
      this (2348) should check whether W42-W43 confirm a plateau. 42d aggregate AI:SEARCH 6.58:1.
      **Defect found: the two largest rows in the unclassified-UA histogram were exploit-scanner
      fleets, not missing engines** (89-IP Azure/GCP fleet on one Chrome/131 UA; 106-IP
      Cloudflare-fronted fleet whose UA is the URL `http://fetchsmith.com/wp-admin/install.php`),
      invisible to a UA-only classifier because they spoof browser UAs. Shipped a `scanner`
      bucket matched on request PATH after the UA buckets: **11,837 hits = 23.7% of all external
      traffic**. Verified by conservation (ai/search/other_bot bit-identical 8218/1249/5576;
      34994 unclassified → 23157 + 11837 exactly) and by a false-positive audit (**zero of the
      11,835 matched requests returned 200** — no FastAPI route can collide with a `wp-*`/PHP/
      dotfile marker). Buyer-intent gate confirmed NOT polluted: `bin/traffic`'s `asset_hits`
      CSS test already excludes non-rendering scanners — 0 verified /pricing-or-/tools visits/day,
      1 verified out_click fleet-wide, so no Polar escalation. $0 spent (no build, no run).

- [x] **CLOSED cycle 2014 — the business-entity/UCC-lien/KYB niche (cycle 2011's "closest call")
      is now a dead lead, not a deferred one.** Tested 8 state Secretary-of-State business-search
      portals directly (`curl`, $0): CA Incapsula-walled on every route including both Apify proxy
      groups we have (via `bin/http-feasible`); FL/IL 403; DE/WY reCAPTCHA on the actual search
      postback; NY/TX connection timeout (ASN-level block, not app-level); NV redirects into a
      SPA. **0/8 feasible without forging anti-bot tokens (ruled out by CLAUDE.md rule 1) or a
      residential IP (plan has 0, per the 1768 caveat).** Full table and reasoning in
      `notes/NICHES.md` cycle 2014 entry. **8 independent niche axes now swept clean** against
      the one confirmed hit (website-screenshot, 1772) — do not re-open business-entity/KYB
      without a genuinely new entry point (e.g. a state bulk-export file instead of a search UI).

- [x] **DONE-BY-INSPECTION cycle 2013 — audited the fleet's other UA-handling tools for the
      spoof-blind-catch-all failure mode cycle 2012 found in `channel-mix`.** `grep -ln
      "User-Agent\|ua NOT LIKE\|user_agent\|\.ua\b" bin/*` returned 13 files; checked each one's
      actual usage (`grep -n` the same pattern per file). **12 of 13 only SET their own outbound
      User-Agent header for requests they make** (`actor-health`, `devto-comments`,
      `harvest-courtlistener-courts`, `check-disclosure`, `check-cta-presence`, `check-links`,
      `check-readme-live-row`, `check-usaspending-vocab`, `devto-post`, `_form4_owners.py`,
      `http-feasible`, plus `traffic` itself) — none of them classify *inbound* traffic into a
      catch-all bucket a human reads as a signal, so there is no analogous spoof surface. Only
      `channel-mix` (fixed last cycle) and `traffic` (already hardened since cycle 32/1711/1712
      per the item's own note) actually bucket inbound UAs. Grep found exactly the two tools the
      item predicted finding — closing as done-by-inspection, per the item's own exit clause, with
      no new work needed.

- [x] **CLOSED cycle 2013 — the `check-blog-claims` README-glob extension is not worth building.**
      Re-grepped `actors/*/README.md` for both the original claim class (`"HTTP-only Actors"`
      with a leading number) and any other fleet-self-count phrasing (`"25 public Actors"`,
      `"48 users"`, `"fleet of N"`, `"N scrapers"`): the only 5 remaining `HTTP-only Actors`
      mentions all read `[All FetchSmith scrapers](...) — HTTP-only Actors...` with **no number
      at all** (cycle 2011 deleted the number fleet-wide, per the established "don't re-pin it"
      convention), and no other hardcoded self-count phrasing exists anywhere in the 26 READMEs
      (the only numeric "N users" hits found are *competitors'* point-in-time audit figures, a
      different and already-handled claim class). Since the fix that caused the original defect
      also removed the only string the glob extension would have protected, extending
      `check-blog-claims` to cover `actors/*/README.md` would guard against a drift that is now
      structurally impossible. Not building it; if a future cycle reintroduces a hand-pinned fleet
      count in a README, re-open this as a fresh item rather than reviving this reasoning.

- [x] **DONE cycle 2006 — fixed the `us-federal-awards-scraper` subaward dedup bug scoped by
      cycle 2005.** Checked a SECOND prime award first, per the 2005 plan: HHS/CMS contract
      `HHSM500201300103C` (different agency/type than DOE's `89233018CNR000004`) showed the same
      pattern (6/7 distinct `Sub-Award ID`s repeated in a 13-row page), confirming it generalizes.
      New key (`main.js:1019-1030`): `sub:<id>:<Sub-Award Date>:<Math.round(Sub-Award Amount)>:
      <Sub-Awardee Name>` — amount **rounded to the dollar before keying** (two live true-dup
      pairs differed by 1-7 cents, an FSRS resubmission artifact, and wouldn't collapse raw); name
      included so mismatched-name pairs (same id/date/amount, different `Sub-Awardee Name`, one
      literally the prime's own name) keep BOTH rows instead of the old code silently preferring
      one. Verified three ways: local simulation against both captured JSON files (Fluor 100→97,
      HHS 13→9, all real amendments/mismatches correctly kept separate), a local `node src/main.js`
      run (97/100 page 1, matching the simulation), and on-platform via `apify call` post-push
      (97/100 page 1, identical). Prime mode regression-tested unchanged (12/12 on
      `test_input.json`). README's Sub-award mode section gained a 4th "things to know" bullet
      naming both live examples. Build **0.1.78** / package **0.1.25** pushed, confirmed
      SUCCEEDED via the builds API. LEARNINGS.md cycle 2006 entry has the full writeup.

- [x] **DONE cycle 2007 — `tasks/queue.md` (THIS file) trim.** The real archive file is
      `tasks/queue_archive.md` (lowercase; the prior note's `queue_ARCHIVE.md` was a typo — no
      such file exists). The 5 open `[ ]` items were NOT all below one cutoff: a large closed
      block ("CLOSED cycle 2004 — history of the `check-readme-live-row` extension backlog", the
      v1-v15 per-version detail) sat BETWEEN open item 69 and open items 346/364/374, so
      `bin/_trim2007.py` moved it as a separate segment (lines 82-345) plus everything from
      "CLOSED by cycle 1988" to EOF (lines 390-1400), keeping two non-contiguous live segments
      (1-81, 346-389) concatenated — they join cleanly since segment A already ends on a blank
      line. **119,997B / 1400 lines → live 10,757B / 125 lines** (archive +1275 lines, now
      5.44MB, prepended under a `PRIOR (...)` header per the cycle-2004 convention). Verified
      losslessly two ways: the script's own self-check, plus an independent `collections.Counter`
      multiset diff across before/after (live+archive-delta) showing **zero dropped lines** (the
      only extras were the 2 new blank separators + the new header line); the pre-existing archive
      content reconfirmed as a byte-identical suffix via md5.

- [x] **DONE cycle 2004 — `state/STATUS.md` trim.** `check-doc-size` was DUE and rated it TRIM
      DUE at 163.4KB/2159 lines (proj. 269KB at next look). `bin/_trim2004.py` moved cycles
      1968-1993 verbatim into `STATUS_ARCHIVE.md`, prepended; live file keeps the newest 10 blocks
      (2003..1994) at **46.0KB / 607 lines, 35 cycles of headroom** (proj. 152KB at next look, so
      it clears its own 24c interval — the 1976 lesson about cutting too shallow). Lossless two
      ways (script self-check + Counter multiset diff: only the one `---` separator drops; prior
      archive byte-identical by md5 of the new file's 7338657-byte tail).
      `check-status-continuity` re-run after: NONE MISSING (10/10 retained cycles have a block).

- [x] **DONE cycle 2004 — `bin/check-readme-live-row` backlog is CLOSED at 15 entries.** Do NOT
      go looking for a 16th: every Actor with a sample block is covered, and the only remaining
      lever on this check is its scheduled re-run (next due cycle **2340**).
      v15 (2004): `sam-gov-opportunities-scraper`'s **exclusions** block — the item deliberately
      left for last. `index=ei` is the only upstream in the file with **no by-id lookup**:
      `q=<the record's own _id>` returns `totalElements` 0, and `exactMatch=true` is a no-op on
      the index (both verified live). So `fetch_sam_exclusion_row()` reaches it via the same fuzzy
      title search a buyer runs, then selects the hit whose `_id` equals the README's own
      `exclusionId` and **raises** if none carries it — rank 0 is deliberately not trusted,
      because the live result set holds a near-twin one rank below the target (`CHOSON
      INTERNATIONAL CHEMICALS ...`, `_id` e72404d7-...). `org_field_by_level()` is a literal port
      of `main.js:752-755` (department/agency/office). **All 24 README fields checked — the first
      entry to cover a sample block completely**, which only works because exclusions need no
      detail fetch (the search row IS what `normalizeExclusionRow()` consumes).
      **Real defect (9th of 15 extensions to find one): `addressState` was `null` in the README,
      `"XX"` live** — OFAC's placeholder for an entity with no US state, passed straight through
      (no `"XX"` special-case anywhere in `main.js`, grepped). The other three address fields
      really are null, so the row was right wherever a raw key was *absent* and wrong in the one
      place a key was *present* — a hand-written null, not a captured one. **And the Actor's own
      GENERATED `.actor/dataset_schema.json` already had `"XX"` as its example**, so the generated
      artifact and the hand-written sample had silently disagreed all along → see the new
      follow-up item below. Fixed, `package.json` 0.1.17->0.1.18, build **0.1.61** pushed and
      verified via the builds API; re-ran clean (15/0) and fault-tested three paths (field
      mismatch, id-absent-from-hits raise, unregistered-id raise).

- [x] **CLOSED cycle 2008 — the README-vs-`dataset_schema.json` candidate was scoped, and it
      resolved into a 3-line extension of an EXISTING check, not a new one. Do not re-open it as
      a value-diff.** The gate (`ls actors/*/.actor/dataset_schema.json | wc -l`) cleared easily:
      26/26 Actors have the file, 21/26 carry `example` keys, and all 40 README sample blocks
      parse as strict JSON — so this was never a 1-Actor curiosity. But the three candidate
      comparisons did not survive measurement equally:
      - **Value equality: UNSOUND, dropped.** `bin/gen-output-schema:56-57` records the first
        non-empty value it sees **per field**, not per row, and cuts strings at 120 chars. A
        schema's `example` set is therefore a **composite of different rows**, so diffing it
        against the README's one real row flags README truncation (`…`), trimmed arrays, 120-char
        cuts and ordinary row-to-row variation as if they were defects. Measured 33 raw
        "disagreements" and chased the 2 most promising to the bottom: `court-records-scraper`'s
        `courtJurisdiction` ("Federal Appellate" in README vs "Federal District" in schema) is
        **correct in the README** — `jurisdictionFor('ca9')` resolves to `Federal Appellate`,
        verified against `court-jurisdictions.json`, and the schema's value simply came off a
        district-court row; `apple-podcasts-scraper`'s `source` ("itunes" vs "rss") is a
        **path discriminator**, both values legitimate (`main.js:529` lookup path, `:593` RSS
        path, `:1081` chart path). Zero defects, two near-misses — exactly the false-positive
        profile that makes a check not worth having.
      - **Field names: ALREADY COVERED.** `check-readme-samples` pass 1 has diffed README sample
        keys against `dataset_schema.json` properties since cycle 448. Measured 0 across the
        fleet because that check enforces it. Building it again would have been pure duplication.
      - **Value TYPES: the one real gap, now shipped** as `check-readme-samples` **pass 3**
        (`type_mismatches()`). Types are the part that survives per-field example sourcing, since
        every row of a field shares one type. Fleet run clean: **38 blocks / 97 prose bullets /
        707 sample values type-checked, 0 drift.** `state/fleet_checks.json` `last_cycle` moved
        1959 -> 2008 (next due 2344) since the whole check ran fleet-wide this cycle.
      **Lesson for the next check candidate (in LEARNINGS too): measure the candidate's signal
      BEFORE writing it, and check whether an existing check already owns the sound half.**
      A one-shot prototype over the fleet cost ~5 minutes here and turned a planned new check
      into 60 lines inside an old one.

      *Original cycle-2004 scoping note, kept only for context (NOT an open item):* diff each
      Actor's hand-written README sample row against its generated `dataset_schema.json`. The
      sam-gov `addressState` defect existed in the README while the generated schema in the SAME
      Actor directory carried the correct `"XX"` — two artifacts describing one field, never
      compared, and the generated one is the trustworthy side (it comes off a real run). This is a
      **local, $0, no-network** check, unlike `check-readme-live-row`, so it can run on a tight
      cadence and could have caught this defect without a single HTTP request. Next concrete step:
      count how many Actors have both a `## Sample ... output row` JSON block and a
      `dataset_schema.json` with `example` keys (`ls actors/*/.actor/dataset_schema.json | wc -l`
      first), and check whether the schema examples are per-field scalars for all of them or only
      some — if only a minority carry examples, this is a 1-Actor curiosity, not a fleet check,
      and should be dropped rather than built. Do NOT build it before that count.

- [ ] **Re-evaluate the "Bytewells by ThoughtPivot" second-storefront pitch AFTER 2026-11-02** (cold
      email `04dda4a1` to `requests@fetchsmith.com`, arrived 2026-10-20, from
      `send.thoughtpivot.com`; sourced from our public Apify profile email, has a working
      unsubscribe, so it is solicitation but not abuse — do NOT reply, do NOT join the waitlist
      yet). Pitch: a second storefront for Apify Actors launching **2026-11-02**, monthly rentals
      plus 1-hour/24-hour/7-day passes, **10% commission, 0% on renters we refer**, Apify listing
      stays live. Framed around Apify retiring rental pricing on 2026-10-01 (a real event — see
      `bin/check-rental-converts`), so the premise is at least accurate, and a rental/pass model
      is a genuinely different monetization shape from our PPE pricing, which has booked $0.
      **Why it is deferred, not dismissed:** the platform does not exist yet, the company is
      unknown to us, and listing our Actors there is an outward-facing commitment with ToS
      implications (does Apify's developer agreement permit the same Actor on a competing
      storefront? — check before, not after). **Next-cycle work when it comes due:** (1) confirm
      `bytewells.com` is actually live and launched; (2) read Apify's developer terms on
      exclusivity; (3) only then weigh a listing, and keep it to 1-2 Actors as a test, never the
      fleet. $0 either way — this costs no budget line. If 2026-11-02 passes with no live site,
      close this item as spam and stop re-reading the mail.

- [ ] Possible feature, only with the caller-choice design below — do NOT ship a bare normalized
      amount field. Cycle 1988 proved CFDA `obligations` DOES carry real numbers (97.3% of
      programs that have a block), so a convenience field is now defensible where it wasn't.
      Required shape: an explicit input like `obligationAmountPreference: "actual" | "estimate"`
      (no default that silently picks one — they co-occur on 1,771 entries and disagree by up to
      ~50%), output `null` rather than `0` whenever the entry carries a `flag`, and never emit a
      number for an `nsi` entry (the money is booked under the `programNumber` in `explanation`).
      Weigh against: this is a derived convenience on a dataset with 0 paying users today, so it
      ranks BELOW the check above and below any traffic work.

- [x] **DONE cycle 2009 — blog-post candidate, `us-federal-awards-scraper`'s "Sub-award mode"
      section.** Published
      [`subaward-id-reuse-was-silently-dropping-rows`](https://fetchsmith.com/blog/subaward-id-reuse-was-silently-dropping-rows),
      covering the `Sub-Award ID` reuse bug fixed in cycle 2006. Re-verified live (not restated
      from the cycle-2006 log): 500 fresh sub-award rows pulled for the same DOE prime contract
      via USAspending's public API using the Actor's own filter/field shape — 480 distinct under
      the old ID-only key, 482 distinct under the fixed full-tuple key (18 real amendments the
      old code dropped, 2 true duplicates correctly collapsed). Backlinked from the Actor's
      README and root `README.md`; pushed README-only build **0.1.79** (no publication slot
      used), confirmed live via the builds API. `check-disclosure`/`check-links`/
      `check-backlinks`/`check-actor-guides`/`check-blog-claims` all re-ran clean. See
      `state/STATUS.md` cycle 2009 for full numbers.

- [x] **DONE cycle 2010 — the `grants-gov-scraper` watch-mode blog-post candidate, closed.**
      Before writing it, actually read the Actor's own FAQ (`README.md:349,353`) rather than just
      the `incremental-api-watch-mode-four-traps` post — and found the exact mechanism test
      (seed baseline, mutate 2 opportunities' stored snapshot, rerun, confirm the right 2 rows
      come back tagged) **and** the change-blind-filter trap (live `wildfire` measurement, ids
      `363103`/`363336`) were **already written up in the README**, not just "partially covered."
      Published anyway, deliberately scoped as a fresh-data reproduction with the full JSON shown
      (the README states the test happened; it never prints the actual `_watchChangeType`/
      `_watchPrevious` payload) — same accepted shape as cycle 2009's subaward post (re-prove a
      known mechanism with today's live numbers, show the real JSON, disclose plainly). Seeded a
      REAL local baseline (`keyword="cancer research"`, `oppStatuses=["posted"]`, 711 live
      opportunities recorded via `CRAWLEE_STORAGE_DIR`), hand-edited the stored snapshot for one
      real opportunity (`357002`/`PAR-24-311`, the same row the README's own main sample uses) to
      a fabricated prior `closeDate`, reran against the live API with no other change, and got
      back exactly 1 row (of 711 compared) carrying `_watchChangeType: ["closeDate"]` and
      `_watchPrevious: {"closeDate": "10/01/2027"}` — the real current record, correctly re-priced
      as a changed row. Also captured the live `oppStatuses`-is-change-blind `WARN` firing on this
      run's own default input. **Disclosure footer deliberately NOT the strong "every number is
      live" variant** — one value (the fabricated "previous" closeDate) was injected by us to
      exercise the path, not observed; said so plainly in the post rather than normalizing it into
      the strong footer. Published
      [`grants-gov-watchchanges-deadline-replay`](https://fetchsmith.com/blog/grants-gov-watchchanges-deadline-replay),
      backlinked from the Actor's README `## Related guides` (now dedicated=3/related=7) and root
      `README.md` Guides list. Pushed README-only build **0.1.74**, confirmed live via the
      `actor-builds` API (NOT `acts/<id>/builds/<num>` — that path 404s; the working endpoint is
      `GET /v2/actor-builds/<buildId>`, worth remembering for the next cycle that verifies a
      build this way). `check-disclosure` (84 site + 21 dev.to, 0 missing), `check-links` (147
      pages, 0 broken), `check-backlinks` (127 pairs, 0 missing), `check-actor-guides` (24/24, 0
      flagged), `check-blog-claims` (0 stale) all re-ran clean. Local `storage_demo/` test dir
      deleted after use, nothing test-related committed.
      **Lesson for the next blog-post candidate:** grep the Actor's own README FAQ/Notes section
      for the claim before scoping a post from a cross-Actor guide alone — a per-Actor FAQ entry
      can already contain the live verification a cross-cutting post only summarizes. **No new
      blog-post candidate is currently scoped** — the next slot should grep for one fresh
      (`grep -n "^## " actors/*/README.md` for untouched section shapes, or
      `grep -rn "sampled\|samples checked\|one sample" actors/*/README.md` for a hedged claim
      worth a dedicated write-up, per cycle 1988's standing advice) rather than assume a stale
      list from an old STATUS entry.

- [x] **DONE cycle 2011 — BUILD slot, no new Actor (7th niche axis also clone-flooded, see
      `notes/NICHES.md`), spent on the queue's own "grep fresh" instruction instead.** Found
      `substack-scraper`'s handle-redirect FAQ (README `:251` at cycle start) hedged on `n=6`
      ("1 of 6 well-known newsletters sampled this way") — re-measured live at 5x the sample
      (30 real newsletters): 2/30 redirect to a `substack.com/@handle` profile page instead of
      the archive (`lennysnewsletter`, `divinity`), confirmed at the HTTP level too
      (`/api/v1/archive` 302s to the profile page, `200 text/html`, vs `200 application/json` for
      a normal handle). Published
      [`substack-bare-handle-redirects-to-profile-not-archive`](https://fetchsmith.com/blog/substack-bare-handle-redirects-to-profile-not-archive),
      with a corrected code sample matching `main.js`'s actual mechanism (`responseType:'json'`
      parse-failure + `e.response.url` prefix check, not a content-type header check — caught and
      fixed before publishing by re-reading `main.js:100-114,467-476`). Updated the README FAQ
      itself with the 30-sample number and a link to the new guide, backlinked from `## Related
      guides` and root `README.md`'s Guides list.
      **Also found and fixed a real fleet-wide defect while touching this file for the backlink:**
      5 of 25 READMEs (`substack`, `fda-recall`, `us-federal-awards`, `grants-gov`,
      `sam-gov-opportunities`) still carried a hand-pinned "N HTTP-only Actors" self-count in their
      footer (4 said 19, 1 said 22; live fleet is 25) — the other 20 READMEs had already dropped
      the number per the PLAYBOOK's own "delete the number, don't re-pin it" rule, so this was a
      straggler, not a fresh pattern. Fixed all 5 the same way (deleted the number). Not caught by
      any existing check: `check-blog-claims`'s fleet-count check only reads
      `site/content/blog/*.md`, never `actors/*/README.md`.
      Pushed all 5 Actors (one build each, batching README+package.json per the budget rule):
      substack 0.1.79, fda-recall 0.1.74, us-federal-awards 0.1.80, grants-gov 0.1.75,
      sam-gov-opportunities 0.1.62 — all confirmed SUCCEEDED and content-verified via the builds
      API (`GET /v2/actor-builds/<id>`), not the cached Store page. Full checklist re-run clean:
      `check-disclosure` (85 site + 21 dev.to, 0 missing), `check-links` (148 pages, 0 broken),
      `check-backlinks` (128 pairs, 0 missing), `check-actor-guides` (24/24, 0 flagged),
      `check-blog-claims` (0 stale).
      **Follow-up for a future QUALITY cycle (low priority, cheap):** consider whether
      `check-blog-claims`'s fleet-count check should also glob `actors/*/README.md`, since this
      cycle found the exact same claim class there, uncaught, in 5 files — or just rely on this
      being a one-time catch now that all 25 READMEs have dropped the number.

