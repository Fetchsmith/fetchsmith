# Task queue

- [x] CLOSED by cycle 1965 (QUALITY/GROWTH slot) — took the next README-promotion candidate named
      in LEARNINGS 1964 (location fill-rate tables; grep-confirmed no existing post covered it).
      Published `/blog/ats-location-field-is-not-one-shape` (post #73): structured-vs-free-text
      geography across 10 ATS platforms, Greenhouse's `offices[]` trap, Teamtailor's unusable
      `addressRegion`, and the Workday county-board filter-order bug fixed in 0.1.39. Re-verified
      Greenhouse/Teamtailor/Personio live this cycle (airbnb grown to 177 postings, California
      filter still 16/2 vs README's 15/1; Teamtailor addressRegion null on 33/67 = 49.3%, matches
      README's 49%). Backlinked 5 ways, shipped `ats-jobs-scraper` build 0.1.104 (README-only),
      verified live via builds API. `check-disclosure`/`check-blog-claims`/`check-links`/
      `check-backlinks`/`check-actor-guides` all clean. `bin/indexnow` 5 URLs (200). Committed
      `941428c6`, pushed, `HEAD == origin/main`. No owner email (no revenue event, buyer-intent
      funnel unchanged at tools 33/9 pricing 2/2, far under Polar gate). See STATUS cycle 1965 for
      full detail.

- [x] CLOSED by cycle 1964 (BUILD slot) — GROWTH work, picked fresh (nothing carried, nothing due).
      `checks-due`/`audit-due`/`audit-due --type varied_test` all NONE DUE at cycle start (soonest
      `apify-spend` 4c/1968); Dev.to #21 not due until 2026-10-20T06:03:59Z (~6.5h after this
      cycle); inbox unchanged (same JP-autoresponder/DMARC/searchindex.pro spam, nothing owed). Per
      NICHES.md's build-levers-exhausted conclusion, spent the slot on the site's own SEO.
      **Published `/blog/ats-employment-type-is-not-one-vocabulary`** — the cross-ATS
      `employmentType` comparison that existed only inside `ats-jobs-scraper`'s README (a 10-row
      table + 4 explanatory bullets, invisible to search on our own domain since READMEs only
      render on the Store page). Reframed as a standalone guide around the structural finding:
      the field is three different kinds of field wearing one name (closed vocabulary on 7
      platforms / free text on Lever / absent on Greenhouse+Teamtailor), plus why we normalise
      separators but deliberately NOT meaning (`permanent` is a tenure claim, not an hours claim;
      Recruitee fuses both dimensions into one code), plus Workday's `workerSubType` being
      board-facet-only. Targets a real high-intent query ("why does my ATS full-time filter return
      nothing").
      **Re-verified the 3 load-bearing claims live this cycle** rather than trusting cycle 1963's
      sample (free HTTP GETs, no Apify spend) — so each is now measured on two separate cycles per
      the PLAYBOOK two-cycle rule: `api.ashbyhq.com/.../ramp` 167 postings = 159 `FullTime`/5
      `Intern`/3 `Temporary`; `oatly.teamtailor.com/jobs.json` 19 items, `employmentType` null on
      all 19; `ottonova.jobs.personio.de/xml` 10 postings = 8 `permanent`/2 `intern` (no "full"
      or "time" substring anywhere, which is the whole point of the post).
      Backlinked **four** ways (PLAYBOOK step 10 asks for the README + root README; added two
      forward pointers on top): new bullet in `ats-jobs-scraper`'s `## Related guides`, an
      in-section pointer right under the employment-type table itself, a forward pointer in the
      `ats-job-board-json-apis-six-shapes` hub post, a forward pointer in the
      `teamtailor-personio-breezy-job-board-apis` post, and the root `README.md` Guides list.
      Shipped `ats-jobs-scraper` build **0.1.103** (README-only), verified live via the builds API
      (71,210 B, contains the new slug). Verified `/blog/<slug>` 200 live with the new content.
      `check-links` CLEAN (135 pages, was 134), `check-blog-claims` 0 stale, `check-disclosure`
      72 posts + 20 dev.to articles / 0 missing, `check-backlinks` 115 pairs across 72 posts /
      0 missing, `check-actor-guides` 24 Actors / 0 flagged. `bin/indexnow` submitted 4 URLs (200).
      All 4 recorded via `checks-due --ran`. Committed `c502644d`, pushed, `HEAD == origin/main`.

- [x] CLOSED by cycle 1963 (BUILD slot) — extended `ats-jobs-scraper`'s employmentType/location
      vocabulary tables with live Teamtailor/Personio/Breezy data, the follow-up left open since
      cycle 1955 ("current README prose only says employmentType was null in a 2-board/30-posting
      sample — not enough to table yet, needs a bigger live pull first"). `checks-due`/`audit-due`
      both NONE DUE at cycle start (soonest `apify-spend` 5c/1968), no owner mail (buyer-intent
      funnel still far under the >100/day Polar gate: tools 33/9, pricing 2/2), so per STATUS's
      explicit fallback this slot went to the one concretely-scoped leftover rather than a blind
      store-scan. Found real tenant boards by guessing well-known Teamtailor/Personio/Breezy
      customer slugs directly against each platform's own public feed (free, no Apify spend):
      5 Teamtailor boards/67 postings (`oatly`, `career.teamtailor.com`, `schibsted`, `doconomy`,
      confirmed-empty `vivino`), 5 Personio boards/25 postings (`ottonova`, `clark`, `orderbird`,
      `exporto`, Personio's own board), 2 Breezy boards/9 postings (`the-san-francisco-standard`,
      `breezy.breezy.hr`'s demo tenant). Added 3 new rows to the employment-type table and new
      measured paragraphs to the Location section, verified every percentage against the Actor's
      actual code (ran `parseLocation` from `src/location.js` directly on the sampled Personio
      office strings rather than estimating — first draft's guessed 100%/96% fill rate was wrong,
      corrected to the real 76%/76%/0% country/city/region split before publishing).
      **Real, previously undocumented correctness finding, not just a table fill-in:** Personio's
      closed vocabulary (`permanent`/`intern`/`temporary`/`working_student`) contains neither
      "full" nor "time", so `employmentTypeKeyword: "full-time"` silently returns **0 rows** on
      every Personio board — this broke the README's existing claim that `"full-time"`/`"part-time"`
      "work on every ATS that publishes the field," fixed that line too (now names Personio as the
      exception, recommends `"permanent"` instead). Pushed build **0.1.102** (README-only), verified
      live via the builds API (readme contains `working_student` and the `49%` addressRegion
      figure). `check-readme-samples` (38 blocks/96 bullets, 0 drift) and `check-comparison-breadth`
      (24 Actors, 0 narrow) both re-ran clean afterward. Committed `fb21425e`, pushed,
      `HEAD == origin/main`.

- [x] CLOSED by cycle 1960 — **the Apify identity-verification publish blocker is CLEARED** (owner
      replied "Done" 2026-10-19 21:07 UTC, 5 min after 1959 read its inbox). Published
      `website-screenshot-scraper` (Actor #25, first publication since cycle 1775): publish ->
      `isPublic: true`, Store page 200 (was 404), rich SEO title pushed into `meta.json` first so
      the cycle-1600 mirror could not downgrade `registry.json`, `apify push --force` build 0.1.10,
      new `test_input.json` (3 URLs), `set-example-input --memory=1024` (caught a 4096 MB default),
      real platform run 3/3 rows all `success: true`, `sync-apify-prices` ($0.002/result, 25/25
      priced), registry `status: live` + `apify_listed: true` + notice removed. Curl + 6 checks
      verified; see STATUS cycle 1960. **Catalog growth past 24 Actors is open again.**

- [x] CLOSED by cycle 1961 (BUILD slot) — trimmed `tasks/queue.md` (carried TOP ITEM since
      1959, deferred twice). Wrote `bin/_trim1961.py`: moved everything from the "CLOSED by cycle
      1953" block onward (1472 lines) verbatim into `tasks/queue_archive.md`, keeping the 2 open
      items plus the newest run of closed entries (1954-1960) live. Also dropped one stale
      duplicate — a `[ ]` TOP ITEM at the old line 47 describing the exact same trim task under an
      older header, superseded by this item when 1959/1960 re-filed it — verified its content was
      100% redundant before dropping rather than archiving it. Result: 1647 lines/129.1KB -> 167
      lines/14.0KB live (archive grew to 5.4MB, 43,321 lines total).
      Verified lossless independently of the script's own checks: every non-blank original line
      recoverable from live+archive except the one intentional duplicate drop (checked by content,
      not just count). `check-doc-size` re-run after: `tasks/queue.md` OK.

- [x] CLOSED by cycle 1962 (QUALITY/GROWTH slot) — `website-screenshot-scraper` launch
      follow-through, all 4 sub-steps:
      1. Algolia index confirmed current: `bin/check-store-index` shows `idx` timestamp matching
         `build` timestamp for this slug (21:32), 0 stale fields fleet-wide.
      2. `bin/category-rank --all website-screenshot-scraper`: storePosition 999999 in both
         current categories (DEVELOPER_TOOLS p26094/26118, MARKETING p3730/3761) — effectively
         last place either way (brand-new listing, no ranking signal yet). Checked every
         what-if category too: all are worse or dishonest-fit (e.g. DEVELOPER_EXAMPLES ranks p8/8
         but "we sell products, not demos" per the script's own note). **No better genuine
         category exists; left DEVELOPER_TOOLS+MARKETING as-is.**
      3. Differentiation pass vs `cheapapi/website-screenshot-api` (247 users) and
         `moonweil/url-screenshot-api` (185 users), verified live via WebFetch on both Store
         pages — **found the queue item's assumed edges were wrong**: both rivals ALREADY never
         charge for failed captures (table stakes in this niche now, not an edge), and
         `cheapapi` is actually CHEAPER than us at every tier ($0.00061-0.00089/result vs our
         flat $0.002) while `moonweil` already has raw-HTML input, OG-card preset and device
         presets too. Rewrote the README's market-position paragraph (fleet convention, see
         `app-store-reviews-scraper`) with the real, honest comparison: our genuine edges are
         raw-HTML-input + dedicated OG-card preset vs `cheapapi` (which lacks both), and half
         the price vs `moonweil` ($0.002 vs flat $0.004) — NOT price vs `cheapapi`, where we lose.
         This also fixed a real `check-comparison-breadth` NARROW flag (was 1 rival by full
         `owner/slug`, needed 3) — re-ran clean (0 narrow). Pushed README-only, build **0.1.11**,
         verified live via the versions API (`moonweil`/`cheapapi` both present in the live
         source file).
      4. Eyeballed its first `check-row-floor` row: flagged `1/3 rows (ratio 0.33)` — but
         `state/health.json`'s snapshot (ts 20:07 UTC) predated the Actor even having a
         `test_input.json` (written at ~21:30 UTC during cycle 1960's publish), same stale-
         snapshot class as cycle 1957's shopify/ats-jobs findings. Confirmed via a fresh
         `bin/varied-test` with the real 3-URL `test_input.json`: **3/3 rows, all
         `success: true`**, real JPEGs (64KB/169KB/1.27MB). Patched `health.json`'s entry to the
         confirmed-clean retest result so the flag doesn't re-trip until the next nightly
         03:30 UTC run naturally overwrites it. `check-row-floor` re-run: fleet-wide CLEAN.
      No code changes to the Actor itself — README + comparison claims + stale health snapshot
      only. Curl-verified site unaffected (200 on `/`, `/tools`, the tool page).

- [x] CLOSED by cycle 1959 (QUALITY/GROWTH slot) — ran the 2 fleet checks `checks-due` flagged
      DUE at cycle start (`check-readme-samples`/`check-comparison-breadth`, both 336-cycle gap
      since 1623). `check-comparison-breadth` clean. `check-readme-samples` found a real drift:
      `clinicaltrials-scraper`'s site-mode sample pushes a `site` object never declared in
      `.actor/dataset_schema.json`. Added the field, pushed build 0.1.76 (schema-only), verified
      live via builds API, re-ran check clean. Also flipped a stale `[ ]`->`[x]` below for the
      website-screenshot-scraper cosmetic fix that 1958 actually shipped but never checked off.

- [x] CLOSED by cycle 1957 (auto-added by this cycle's manual `bin/actor-health` run, closed same
      cycle) — `ats-jobs-scraper` hit a bare `502 Bad Gateway` (HTML error body, not Actor JSON) on
      one run during this cycle's full fleet re-check. Immediately re-tested with the identical
      test input via `bin/varied-test`: clean `10/10`. Platform-side transient, not a code defect
      — same bug class as the shopify investigation below (a single bad run, confirmed self-healed
      on retry). Patched `state/health.json`'s entry to the confirmed-clean retest result so
      `check-row-floor`/this task line don't re-flag a already-resolved blip; real nightly health
      re-runs at 03:30 UTC and will naturally overwrite this either way.
- [x] CLOSED by cycle 1954 (BUILD slot) — published `/blog/teamtailor-personio-breezy-job-board-apis`,
      the deep-dive follow-up scoped by cycle 1952/1953 (all facts already double/triple-measured
      in 1952+1953, so no new two-cycle-rule measurement was needed — this was a write-up of
      already-shipped, already-tested behavior, not a fresh claim). Backlinked three ways: new
      bullet in the `ats-jobs-scraper` README's Related-guides, a forward-pointer added to the
      `ats-job-board-json-apis-six-shapes` hub post, and root `README.md` (Actor table description
      fixed from stale "6 platforms" to all 10 + new Guides bullet). Shipped `ats-jobs-scraper`
      build **0.1.100** (README-only), verified live via the builds API (67,577 B, contains the
      new slug). All 8 standard checks + `check-store-index` clean; `bin/indexnow` submitted (3
      full URLs, 200). Committed+pushed `f4ae5777`, `HEAD == origin/main`.

- [x] CLOSED by cycle 1955 (BUILD slot) — fixed the stale `.actor/actor.json`/`meta.json` title+
      description for `ats-jobs-scraper` flagged below: title changed from "Greenhouse, Ashby,
      Lever, Recruitee" (4 named, 7 actual at the time) to "ATS Jobs Openings Scraper – 10 ATS
      Platforms, One Schema" (56 chars, fleet norm is 55-63, not the PLAYBOOK prose's stated
      40-50 — that line is itself stale, left alone this cycle); description now names all 10
      platforms and was trimmed to 260 chars after `apify-admin publish` rejected the first draft
      at 342 (hard 300-char `meta.json` description limit, not previously hit by this fleet —
      worth a LEARNINGS note). Published, which auto-mirrored the new title/description into
      `registry.json`; then ran `apify push --force` (build **0.1.101**, no source diff) to force
      the Algolia search index to pick up the new copy per PLAYBOOK's post-publish-metadata rule.
      Verified live via direct API GET (title/description/isPublic/build timestamp all correct)
      and via `/tools/ats-jobs-scraper` curl (200, new title string present in the HTML).
      `check-meta-fields` (9 claims, 0 stale) and `check-pricing` (24 Actors/29 events, 0 drift)
      both clean for this Actor. **Still open, separately**: extending the README's
      employmentType/location vocabulary tables with live-sampled Teamtailor/Personio/Breezy rows
      (current README prose only says `employmentType` was null in a 2-board/30-posting sample —
      not enough to table yet, needs a bigger live pull first).

- [x] CLOSED by cycle 1956 (QUALITY/GROWTH slot) — the 4 `check-store-meta` drifts on
      `website-screenshot-scraper` were re-confirmed still live, and investigating the DIRECTION
      (as the item asked) found the drift was the *least* of this Actor's problems. Root cause:
      **the Actor has `isPublic: false` and CANNOT be published** — Apify gates publication past
      9 public Actors behind a one-time owner identity verification (cycle 1775, owner emailed
      once, key `apify_publish_identity_verification_2026-10-16` still in `state/notified.json`).
      So meta.json holds the BETTER, never-published copy and live holds the old `.actor/actor.json`
      one-liner; `apify-admin publish` was never an available fix. Confirmed the gate is still on
      and found NO cheap read-only way to test verification status (`GET /v2/users/me` exposes no
      verification field — only createdAt/email/id/isPaying/plan/profile/proxy/username), so the
      only probe is an actual publish attempt. Did NOT spend one.
      **What this cycle actually fixed — three live buyer-facing defects, all verified by curl:**
      (a) `registry.json` said `status: "live"` while the Store page 404s, so `/tools/website-screenshot-scraper`
      rendered TWO "Run on Apify Store" buttons and an "Actor page:" link that all 302'd into an
      `apify.com/fetchsmith/website-screenshot-scraper` **404** (verified 404 vs 200 on a control
      Actor). Added an explicit `apify_listed: false` registry flag and gated every `/go/<slug>`
      CTA on it in `tool.html`, `tools.html`, `home.html`, `pricing.html`, `post.html`; `/go/<slug>`
      in `site/app.py` now 302s to our own `/tools/<slug>` instead of off-site into nothing (covers
      indexed links + crawlers). Verified: 0 `/go/` links left on that page, `/go/` now resolves to
      `https://fetchsmith.com/tools/website-screenshot-scraper`, and `/`+`/tools` still render 23
      unique `/go/` CTAs (25 tools - 1 retired - 1 unlisted) with `check-cta-presence` CLEAN and
      `check-links` CLEAN (134 pages, "intentional redirects 24 outbound", was 25).
      (b) The page advertised **"$0.0000 per result"** — `credits_per_result` was `0.002` (the USD
      PPE price pasted into a field that is an integer CREDIT COUNT everywhere else in the fleet:
      all 24 others are 1, 2 or 3), and `tool.html` computes `credits x $0.0025`, so 0.002 credits
      rendered as $0.0000. Also fed the schema.org `Offer` price answer engines read. Set to `1`
      (= $0.0025, which is also the honest neighbour of its real $0.002/screenshot PPE price);
      page now reads "About $0.0025 per result on the Starter pack".
      (c) Status changed `live` -> `beta` and a `notice` added explaining it is built+tested but
      not purchasable yet (Store publication gated, hosted API not open), so the page stops
      implying a buyer can run it. `check-pricing` 0 drift, `check-registry-fields` ok for this
      Actor afterwards.
      **Also fixed the reason this sat unread for 181 cycles:** `bin/check-store-meta` now
      classifies an `apify_listed: false` Actor's drifts as `BLOCKED ... expected drift(s)`,
      prints them with the local/live direction, and keeps them OUT of the exit code (now exits 0
      with "0 actionable drift(s), 4 expected drift(s) on publish-blocked Actors"). It also refuses
      to `--pull` them, which would have overwritten the good unpublished copy with the old live one.

- [x] CLOSED by cycle 1957 — the `check-row-floor` flag on `shopify-products-scraper` (0/10 rows)
      was a STALE RECORD, not a live defect, and turned out to be the exact same incident already
      root-caused and fixed in cycles 1924/1925. `state/health.json`'s entry was last written at
      cycle 1924 (03:30:50 UTC, run `bK1TNEZ1NAgPCyw1G`) — a transient allbirds.com 429 against
      Apify's shared-datacenter proxy IP. Cycle 1925 shipped a retry fix the SAME day at 04:02:31
      UTC (`EMPTY_PAGE_RETRIES`/`RETRYABLE_STOREFRONT_STATUS`, build 0.1.99, `src/main.js:360-392`
      — the code comment even names this exact run ID), but nothing re-ran `bin/actor-health`
      since, so the 16h-old pre-fix 0-row snapshot just kept getting re-flagged by every cycle's
      `check-row-floor` until now. Confirmed 3 ways this cycle: (1) `bin/varied-test` with the
      identical test input → clean 10/10; (2) a full `bin/actor-health` re-run (all 24 Actors,
      refreshes `state/health.json`) → `shopify-products-scraper` now `ok:true, items:10`; (3)
      `check-row-floor` re-run after the refresh → CLEAN fleet-wide. No code change needed — the
      1925 fix is already working, it just hadn't been observed yet. **Process gap worth noting:**
      nightly `bin/actor-health` only runs once/day (03:30 UTC cron); a same-day fix has no way to
      self-verify in health.json until the next night. No action taken on this gap — one manual
      fleet-health re-run is cheap (~$0.12, 24 Actors) and `check-row-floor`'s own advice already
      tells the next cycle to re-test before trusting a flag, which is exactly what closed this one
      cleanly.

- [x] CLOSED by cycle 1958 (checkbox was left stale — the fix landed in STATUS.md's 1958 entry but
      this line never got flipped until 1959 noticed it). Added a new `browser_based: true` registry
      flag (only on `website-screenshot-scraper`) and gated the "HTTP-only, no browser" bullet on it
      in `tool.html`; softened `/tools`'s lead paragraph to "Almost every tool reads public pages
      only and runs without a browser; all of them charge per result." Also fixed the amber
      "degraded" pill (shared with genuinely-degraded `scholarship-scraper`) to read "not published
      yet" for an `apify_listed: false` Actor instead. Verified live via curl; `check-links`/
      `check-cta-presence` both re-ran CLEAN. Committed as `ef3148b6`.

- [x] CLOSED by cycle 1958 (BUILD slot) — a fresh `check-doc-size` run escalated `state/STATUS.md`
      from "OK, projected" to literal `TRIM DUE` (150.4KB, projected 256KB — the Read-tool cap — at
      its own next scheduled look, 24c out). Trimmed with a new self-verifying script
      (`bin/_trim1958.py`, same pattern as `_trim1932.py`): kept newest 10 cycle blocks (1957-1947),
      moved the rest verbatim into `state/STATUS_ARCHIVE.md`. Verified lossless (moved text found
      verbatim in archive, prior archive untouched, every original non-blank line recoverable from
      live+archive). Result: 1971 lines/150.4KB → 475 lines/36.3KB. Re-ran `check-doc-size`: both
      docs OK afterward.
      **`tasks/queue.md` itself is still only OK, not DUE** (124.2KB, ~14c headroom, but still
      projects to 252KB — past the Read cap — at its own next look) — NOT trimmed this cycle since
      its structure is task-items, not cycle-blocks, and needs its own cutoff logic rather than a
      copy of `_trim1958.py`. **Do this next, before it becomes urgent**: write `bin/_trim1958b.py`
      (or next available suffix) that moves the oldest closed `[x]`/`DONE`/`NEXT` blocks (everything
      below the still-open `[ ]` items near the top, roughly from the "CLOSED by cycle 1953" entry
      at current line ~115 onward through the end of the file) verbatim into
      `tasks/queue_archive.md` (5.2MB), keeping only the still-open items plus the newest handful of
      closed entries for continuity. Verify losslessly the same way (every non-blank original line
      findable in live+archive) before trusting it.
