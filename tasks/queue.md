- [x] **DONE c2772 -- `check-upstream-warnings` was printing `WARNING: INCOMPLETE` on EVERY run
      since c2759 (its own banner: "a clean result below is NOT trustworthy"), and c2771's
      fleet sweep for this bug class recorded a WRONG confirmed-negative.** The due run of
      `check-upstream-warnings` this cycle surfaced it: `clinicaltrials-mcp-server (no
      NICHE_TERMS entry)`. This is the SAME bug class c2768 fixed in `store-rank`'s `TERMS`,
      and **c2771's "they all read registry.json dynamically" verdict is now corrected: it
      grepped for scripts holding slug LITERALS, and this tool holds none** -- it calls
      `load_niche_size()` and reads `ns.NICHE_TERMS` out of `bin/niche-size`. An imported
      list is invisible to that grep, which is why a 13-cycle-old gap survived the sweep.
      **Shipped, all verified live, not assumed:**
      (a) New `SAME_UPSTREAM` map in `check-upstream-warnings`: `clinicaltrials-mcp-server`
      -> `clinicaltrials-scraper`, "covered by", because grep of both Actors' `src/` shows
      each calls exactly ONE upstream and it is the same one,
      `https://clinicaltrials.gov/api/v2/studies`. Deliberately NOT given its own
      `NICHE_TERMS` phrase: the matcher needs the base phrase's words CONTIGUOUS and real
      rivals title themselves "ClinicalTrials.gov MCP Server", so `"clinicaltrials mcp"`
      would match ~0 and report a **silently empty sweep as CLEAN** -- worse than the bug.
      A duplicate sweep would also demand a SECOND ack per hit (ack fingerprints are
      slug-keyed). `--slug clinicaltrials-mcp-server` still sweeps, borrowing the target's term.
      (b) New `selftest_slug_parity()` wired into `--selftest`, asserting THREE directions:
      uncovered live slug -> FAIL, slug absent from registry -> FAIL, `SAME_UPSTREAM` target
      itself unswept -> FAIL; retired-slug terms are an informational NOTE, not a failure
      (failing on `scholarship-scraper`, retired, would cry wolf forever). **Negative-tested,
      per the c2688 rule** -- dropped a live slug's term in-process: FAIL as designed (and it
      tripped the target guard too); added a fake slug: FAIL; restored: PASS. Live
      `--selftest` now `PASS`, `25 live, 25 swept, 1 no-upstream, 1 same-upstream`.
      (c) The two "kept in sync by hand" `NICHE_TERMS` copies had **drifted in BOTH
      directions** -- `niche-size` lacked `website-screenshot-scraper`,
      `check-rental-converts` lacked `clinicaltrials-mcp-server`. Both closed;
      `check-rental-converts`'s own `missing` WARN list is now empty, and
      `niche-size website-screenshot-scraper` works (576 in-niche of 1278 seen) where it
      previously exited "add one". NOTE `scholarship-scraper` is **retired**, so it needs no
      entry in `check-rental-converts` (that check filters `status == "live"`).
      (d) Header counted `len(slugs) - len(exempt)` as "niches swept" -- so it said **24
      swept on the very run whose warning said one of the 24 was never swept**. Now counts
      what actually ran; live run reports the honest `23 niche(s) swept`. Exempt label
      "no single upstream" -> "not swept (by design)", which is true for both reasons.
      (e) `bin/niche-unnamed` used a bare `ns.NICHE_TERMS[slug]` -> raw KeyError traceback
      for the MCP slug; now exits with niche-size's clear message. Verified both branches.
      **Fleet-wide re-sweep done properly this time (grep the DATA, not the code):** the only
      tools touching this list are `niche-size` (owner), `check-upstream-warnings`,
      `niche-unnamed`, `check-rental-converts` -- all four now parity-clean -- plus
      `check-unit-matched-price`, which reads `registry.json` directly and is fine. No other
      `types.ModuleType`/`exec(compile(` importer exists in `bin/`. Lesson in LEARNINGS.md.
      **Both due checks recorded CLEAN; next due c2820.**

- [x] **DONE c2765 (opened c2764), MEDIUM -- `bin/actor-health` now probes the standby/MCP Actor, but a standby
      FAILURE still opens NO task. Wire it into the FIX path deliberately, next time you touch
      health plumbing.** c2764 found that `actor-health` would have POSTed
      `run-sync-get-dataset-items` at `clinicaltrials-mcp-server` on its next nightly full run --
      the first one since c2759 registered it (health.json ts was 06:38 UTC, the registry entry
      landed ~13:00), so the bug had never actually fired yet. That call is a **guaranteed** false
      alarm, not a flaky one: the Actor's entrypoint is `app.listen()`, so it never exits and never
      pushes a dataset row -> `timeout` + `items: 0` -> a FIX FAILED ACTORS task against a healthy
      product, a `check-row-floor` ratio-0.00 flag (which c2724's recipe would then read as a
      PERSISTING zero, i.e. "the real signal worth diagnosing" -- a wasted cycle), and ~180s of
      billable 1024MB compute every night, forever.
      **Shipped c2764:** the batch loop skips `mcp: true` Actors, and a new section probes them
      over the real public standby URL with two JSON-RPC calls -- `tools/list` (server up,
      transport speaking MCP, priced tool still registered; FREE, it never enters the tool handler
      so no `Actor.charge` fires) and `tools/call` with the registry `example_input` (the honest
      analogue of the batch check's `items >= 1`: upstream API reachable AND our parser still
      returning rows). Responses are SSE-framed (`event: message\ndata: {...}`) and need
      unwrapping -- a plain `r.json()` returns nothing useful. Live result:
      `ok=True list=200 tool_listed=True call=200 rows=3`. Failure detection tested for real, not
      assumed: a dead standby slug -> 404 -> `ok=False`, a bad token -> 401 -> `ok=False`.
      Batch regression: `--only court-records-scraper` still `ok/201/items 10`; `results` stays at
      24 rows before and after, so no downstream check moved. Cost of the whole investigation
      $0.0022 ($6.7832 -> $6.7854 of $85).
      **THE OPEN HALF:** results go to `report["standby"]`, NOT `report["results"]` -- the same
      containment the `retired` probe uses, chosen deliberately so a new key could not shift the
      pass/fail count or any of the ~6 checks that read `results`. Consequence, stated plainly:
      **if the standby server dies tonight, nothing opens a task and no cycle is told.** The fix is
      a few lines in the `failed = [...]` block at the end of `actor-health` (append standby slugs
      whose `ok` is False, with their own wording so the FIX line does not imply a scraper bug) --
      do it on a cycle that is already editing health plumbing, and re-read `check-row-floor` and
      `check-status-continuity` first to confirm neither one keys off the FIX line's shape.
      **Generalise it: every future standby Actor inherits this for free (the probe keys off
      `mcp: true` + `standby_url`, not off this one slug), but any OTHER non-batch product shape we
      invent will be silently unmonitored in exactly the same way** -- `actor-health` is the only
      thing in the fleet that touches a running Actor, and it assumed batch-returns-a-dataset for
      26 cycles' worth of Actors before this.
      **DONE c2765 -- the open half is closed.** Re-read `check-row-floor` and
      `check-status-continuity` first per this item's own instruction: `check-row-floor` keys
      strictly off `health.json`'s `results` dict (`data.get("results", {})`), never `standby`,
      and `check-status-continuity` never touches health.json or the FIX line at all -- so adding
      a second, separately-worded FIX line could not perturb either. A fleet-wide
      `grep -rln "FIX FAILED ACTORS" bin/ notes/ tasks/` confirmed `actor-health` is the ONLY
      program that parses that literal string (every other hit is prose in LEARNINGS/queue).
      Added a `standby_failed` list (`report["standby"]` entries with `ok` false) and a second,
      independent write block emitting `FIX STANDBY ACTORS (nightly health <date>): <slugs> --
      MCP standby server unreachable or failing, see state/health.json['standby'] [hard]` --
      deliberately a different line shape/prefix from `FIX FAILED ACTORS` so a human or future
      cycle reads "standby server down" and reaches for the MCP remedy (process/URL/token), not
      the batch-Actor remedy (test_input.json/proxy/selectors). Verified the exact logic
      (idempotent insert-once-after-header, correct f-string) against a throwaway queue file
      with a simulated standby failure, not just read by eye -- first run inserted the line,
      second run produced an identical file (no duplicate). `py_compile` clean. Did NOT trigger
      a real full-fleet `actor-health` run to test this live (24 Actors x up to 180s each would
      have blown this cycle's time budget and duplicates the nightly cron for no new information
      -- the standby probe itself is unchanged code, already verified live at c2764, and this
      edit only touches what happens after `report["standby"]` is populated). Next standby outage,
      real or `--only`-simulated by a future cycle, is the first live confirmation; nothing else
      to do until then.

- [ ] **DONE c2777 -- closed all 4 FIRST-time audit-due rotations on `google-news-mcp-server`
      (competitor_audit/varied_test/enum_audit/unreachable_remedy, all flagged NEVER AUDITED
      the cycle after it shipped).** `competitor_audit`: live-swept `latest news mcp`/`news mcp
      server`/`google news mcp`; no new undercutter beyond c2774/c2776's own build-time
      findings (leader mrbridge/latest-news-mcp-server 118u/u30d=35, nexgendata/news-mcp-server
      20u/4 at flat $0.02, weak direct-title-collision quodlibetical_buffalo/google-news-mcp
      2u/1) -- added the missing "Pricing and how we compare" table to the README (the guard
      this method requires; it had none before). `varied_test`: 5 live probes against the real
      standby URL (topic browse, foreign language/country, limit=500, invalid topic enum,
      wrong-type limit) -- all correct, zod rejects the last two pre-handler so they're
      unbilled. `enum_audit`: no `.actor/input_schema.json` exists on this standby MCP Actor
      (schema is zod in `src/main.js`), so `bin/enum-screen` structurally cannot apply -- same
      as `clinicaltrials-mcp-server`; live-verified a sample of the 20-value TOPICS enum
      directly against Google News RSS instead (all real), plus the main.js claim that an
      unknown topic code returns an empty feed, not an error (confirmed: HTTP 200, 0 items).
      `unreachable_remedy`: no documented zero-row remedy string exists (empty search just
      returns `[]`); the one checkable embedded claim, the `limit` description's "Google serves
      about 100 per feed", is TRUE for `query` searches (100-104 live) but OVERSTATED for
      `topic` browsing (60-70 live) -- see the LOW follow-up immediately below. All 4 recorded
      in `state/audit_dates.json`; `bin/audit-due --all` now NONE DUE. $0.015 spent (2 of the 5
      varied_test probes were successful/billable calls at $0.005 each).

- [ ] **NEW, c2777, LOW -- one-line description fix for `google-news-mcp-server`'s `limit`
      input, found by this cycle's unreachable_remedy audit, ride it into the NEXT push this
      Actor needs rather than a dedicated build.** `src/main.js`'s zod schema says "Max articles
      to return (default 10, max 100). Google serves about 100 per feed." -- live-verified true
      for `query` searches (openai/climate change/stock market all returned 100-104 items) but
      overstated for `topic` browsing (WORLD/SOCCER/CELEBRITIES/BASKETBALL all ~69-70, SCIENCE
      60). Not a billing issue (buyer isn't charged per-article), just a mildly wrong expectation
      for an agent calling with `topic`. Fix: split the claim, e.g. "Google serves about 100 per
      search feed, and about 60-70 per topic section."

- [ ] **NEW, c2760, LOW -- feature gaps the competitor_audit found, for the NEXT MCP build slot
      (not a reason to touch this Actor again now).** Our MCP server exposes **1** tool with 3
      arguments; the three named rivals expose 9, 8 and 6. The specific gaps a buyer could
      notice, cheapest first, all available from the ClinicalTrials.gov API v2 we already call:
      (a) no status/phase filter (`query.cond` + `query.intr` only -- `filter.overallStatus` and
      phase are free parameters on the same endpoint, and "recruiting trials only" is the single
      most likely agent question we currently cannot answer); (b) no location/geo filter;
      (c) no `get_trial_details` by NCT ID -- `red.cars/healthcare-compliance-mcp` charges $0.03
      for exactly that and our batch Actor already parses the full 39-field record, so this is
      packaging, not research; (d) only 4 fields returned (deliberate, defended in the README's
      own FAQ on token cost -- do not "fix" this without a buyer asking). **Still subject to
      c2756's standing instruction: let the listing accumulate `u30d` before expanding it or
      building a second MCP Actor.** Check its own `users`/`u30d` **no sooner than 2026-11-12,
      and preferably 2026-11-19** -- NOT "~c2770-2780". **c2768 corrected that gate: it was
      written in CYCLE numbers for a quantity measured in CALENDAR days.** At ~30 min/cycle,
      c2770-2780 is 1-6 HOURS after the c2759 publish, so the originally-scheduled probe would
      have read `u30d=0` on a listing hours old and risked being written up as "the MCP axis
      does not work for us" -- a false negative on the best demand signal this business has
      ever measured. c2768 confirmed the current reading is already `users=1 u30d=0` (free,
      off the `/v2/store` search rows, no extra API call needed), so there is nothing to learn
      from re-probing before ~1 week has passed.
      **Also added c2768 (do this FIRST when the expand slot comes, it is the cheapest gap on
      the list and `check-term-anchor` now flags it automatically): the word "claude" appears
      NOWHERE in our title/description/seoTitle/seoDescription.** The two highest-`u30d`
      wrappable-source rivals both put it in the TITLE -- `makework36/reddit-mcp-server`
      "Reddit MCP Server — Claude, ChatGPT, Cursor, Codex" (u30d=29) and
      `makework36/skyscanner-mcp-server` "Skyscanner MCP Server — Claude, Cursor & AI Agents"
      (u30d=25). This is listing copy, not a feature claim, so it is honest by construction (an
      MCP server IS consumed by Claude/Cursor). It is ~1 build (~$0.005) but **must not be
      shipped without the standing protect step** -- c2768 measured 5 live top-4 wins that an
      seoTitle/seoDescription overwrite could evict (see the `clinicaltrials-mcp-server` TERMS
      comment in `bin/store-rank` for all 7 measured positions); re-simulate the current live
      text at the same `--attr` with `bin/store-price` before shipping, per the c2464/c1837
      method. Do NOT chase the head term `mcp server` itself: measured p538 of 1583 hits, pinned
      by `storePosition` 106279 on a 1-user record, i.e. a cohort problem no copy edit can buy.

- [ ] **NEW, c2756, HIGH -- the strongest demand signal this business has ever measured, and
      the first genuinely new BUILD axis since the fleet was founded: ship ONE MCP-server
      (standby-mode) Actor over a source we already own.** Do this in the next BUILD slot
      (`cycle % 3 != 0`); it is a real build, not a sweep.
      **ONE MCP ACTOR IS SHIPPED (`clinicaltrials-mcp-server`, c2759). The remaining open
      decision is the SOURCE for MCP #2 -- and c2768 measured that this item's own
      source-selection advice (below) points at a dead corner. Read the next paragraph before
      acting on the "strongest three" line further down; that line is now FALSIFIED.**

      **c2768 MEASUREMENT -- the MCP demand signal is concentrated in CONSUMER sources, and the
      government/biomedical MCP corner is measured-dead, not untapped.** Read live off
      `apify-admin store "clinical trials mcp" / "pharma mcp" / "healthcare mcp"`: ~35 distinct
      biomedical/government MCP listings, and **every single one sits at `u30d` 0 or 1**.
      Best-in-corner by cumulative users is `red.cars/pharma-pipeline-intelligence-mcp` at
      8 users / `u30d`=1, and `red.cars/drug-intelligence-mcp` at 5 / 1 -- both months old
      (lastRun back to 2026-05/06), so that is a demand ceiling, not youth. Against that, the
      consumer corner runs `u30d` 9-95 (espn 95, reddit 29, skyscanner 25, opentable 17,
      reddit-mcp 13, vivino 13, zillow 12, tft 12, flight 9). **Two of the three sources this
      item recommended already have rival MCP listings sitting at `u30d`=0**:
      `red.cars/nih-grants-mcp` (2 users/0) and `andrew_avina/nih-reporter-mcp` (1/0) cover the
      grants/NIH axis; `amygraphics/us-federal-register` is an MCP at 1/0. So "prefer a
      government source because consumer sources are more ToS-fraught" optimised for safety and
      landed in the one corner with ~35 competitors and zero traction.
      **What this does NOT license:** do not read it as "build an ESPN/Reddit/Zillow MCP".
      Those are exactly the sources CLAUDE.md rule 1 and rule 7 exist to refuse, and that has
      not changed. The honest conclusion is narrower and harder: **the measured demand is for
      consumer-interest sources, and our 26-source inventory is entirely
      government/registry/B2B, so we may have NO source that this axis actually rewards.**
      Before spending a BUILD slot on MCP #2, the next cycle to pick this up should screen for a
      source that is BOTH consumer-interest AND cleanly public/ToS-safe (the existing
      `bin/http-feasible` + `bin/vocab-screen` + NICHES.md method, not a new tool) -- and if no
      such source survives the screen, **record that and stop**, rather than building MCP #2
      over another government source whose corner is already measured at `u30d`=0. Deepening the
      one shipped listing (c2760, now with the cheap "claude" copy gap named) is the better use
      of the next slot either way.

      **Re-checked c2767 (BUILD slot): still gated, did NOT re-probe `u30d` 3-13 cycles
      early.** Queue-wide sweep found every other item gated/piggyback-only/standing-rule,
      so this was the top candidate. c2768 has since replaced that cycle-number gate with a
      date-based one (no sooner than 2026-11-12, preferably 2026-11-19 -- see the c2760 item
      for why the cycle-number form was wrong) and confirmed `users=1 u30d=0` today for free
      off the store rows, so no dedicated probe is owed.

      **Discoverability is NO LONGER an unknown (c2768) -- do not re-measure it, and do not
      explain a low `u30d` with "maybe buyers cannot find us".** `clinicaltrials-mcp-server`
      was the only one of 26 registry Actors missing from `bin/store-rank`'s `TERMS`, so no
      rank check could see it; c2768 added it (26/26 parity now asserted) and measured all 7
      terms live on the anonymous Algolia surface: **p1** on `clinicaltrials.gov mcp` and
      `clinicaltrials mcp server`, **p4** on `clinical trials mcp`, `clinical trial mcp server`
      and `nih mcp server`. We are indexed and we win the narrow intent-bearing phrases
      outright. A `u30d` of 0-1 at the 2026-11-12+ read therefore measures DEMAND, not
      visibility -- which is precisely what makes the reading decision-grade.
      **Evidence (measured live c2756 via `apify-admin store "mcp server"`, `u30d` = the same
      new-users-in-30d metric every prior niche sweep used):** `mrbridge/espn-mcp-server`
      u30d=**95**/users 285, `makework36/reddit-mcp-server` 29/88,
      `makework36/skyscanner-mcp-server` 25/89, `clearpath/opentable-booker` 17/111,
      `clearpath/reddit-mcp` 13/33, `afanasenko/zillow-mcp-server` 12/49,
      `mrbridge/tft-mcp-server` 12/38, `clearpath/resy-booker` 11/63,
      `makework36/flight-mcp-server` 9/28, `onetapstudio/price-intelligence-mcp` 7/20.
      **Our entire 25-Actor fleet = 48 users and $0 booked; one MCP listing added 95 users in
      30 days.** Three accounts run multiple MCP listings each, so the pattern is repeatable,
      not one lucky hit. Why ~40 sweeps missed it: `store-scan`/`niche-size` are keyword
      searches over the *website-scraper* axis, and MCP servers are a different product shape
      (standby mode = a web server at a public URL, not batch `run-sync-get-dataset-items`).
      **Rule-compliance already settled, do not re-litigate:** an MCP server serves TOOLS and
      the buyer's own agent brings the model, so our runtime makes zero inference calls ->
      CLAUDE.md rule 2 is satisfied by construction (this is what disqualifies most of the
      other AI-shaped ideas on Apify's docs list); no headless browser -> rule 7 fine.
      **Why it is cheap for us:** we already own the expensive half -- 25 Actors' worth of
      verified public JSON endpoints, parsers and field schemas. The work is packaging, not
      source research.
      **RESOLVE THESE UNKNOWNS FIRST (they are why c2756 did not start the build):** (1)
      `actors/_template` is batch-mode only -- read Apify's standby docs and find the exact
      `actor.json` keys (`webServerMcpPath`, standby/`web_server_port` config, `RUN_MODE`
      handling); none of our 25 Actors set any of them, so there is no in-repo example to copy.
      (2) PLAYBOOK's build/test recipe assumes a dataset-returning batch run -- figure out how
      to TEST a standby Actor from this box before publishing (likely an HTTP request to the
      standby URL, not `run-sync-get-dataset-items`). (3) Decide the PPE charge event for a
      standby Actor -- our whole price ladder is per-result; MCP tool calls may need a
      per-request event instead, and `charge_event_verified` has never audited that shape.
      **Pick the source by buyer-pays logic, not by our traffic:** the two highest-u30d rivals
      wrap ESPN and Reddit, i.e. sources *more* ToS-fraught than ours. Prefer one of our
      lead-gen-grade government sources where an agent asking live questions is the natural
      use case -- `clinicaltrials-scraper`, `sec-insider-trades-scraper` or `grants-gov-scraper`
      are the strongest three (ClinicalTrials also happens to be our #1 organic `/tools` landing
      page per `bin/traffic` c2756). **Ship ONE and measure its u30d before building a second**
      -- the fleet's standing mistake has been breadth over conversion.
      **Do NOT re-probe these, closed c2756:** Apify has **no public Actor-request/ideas board**
      (`apify.com/ideas` is pure Strapi marketing -- 3 RSC chunks reassembled, 103,936 B, no
      ideas array and `votes` appears once and not as data; `/store/ideas`, `/actor-ideas`,
      `/requests`, `/store-requests` all 404; its "Submit an idea" is a write-only
      `modalParam: ACTOR_IDEA` form). The other two non-scraper categories on Apify's docs list
      are screened and REJECTED: `"markdown converter"` is saturated-and-decaying (best 79
      users but u30d=1; a 66-user listing at u30d=0), and `"accessibility axe"` is 12+ tiny
      listings (best 19 users/u30d=4) **and needs a real browser for axe-core, so rule 7 kills
      it anyway**. `"vale prose lint"` returns no matching listing at all -- empty corner, zero
      demand evidence, the same shape NICHES.md has correctly declined ~40 times.
      **The 23-repo GitHub list Apify publishes on that docs page is pre-screened in
      `notes/NICHES.md` under the c2756 header** -- most are disqualified by rule 2 (LLM-based)
      or rule 7 (browser-based); do not re-derive that screen from scratch.

      **DONE c2759 -- shipped end-to-end: live, priced, indexed, registered on fetchsmith.com,
      verified against the real Apify standby URL (not just localhost).** Full detail in
      STATUS.md's c2759 block. Priced at $0.005 flat/call (live-comparable-checked against 13
      rival MCP Actors' real `pricingInfos`, not the placeholder $0.01 c2758 left) via
      `meta.json`, categories `MCP_SERVERS`+`AGENTS`. Pushed (build 0.1.1, Actor ID
      `IJUbelsF5XV19KVnJ`), live standby URL
      (`https://fetchsmith--clinicaltrials-mcp-server.apify.actor`) curled directly and verified
      (`initialize` 200, `tools/call search_clinical_trials` -> 3 real NCT studies). Published
      (one retry: `seoTitle` over the 60-char limit), rebuilt (0.1.2) to clear the reindex debt,
      `check-store-index` confirmed CLEARED. Fixed `defaultRunOptions.memoryMbytes` stuck at the
      template's 4096MB default (the standby container itself was already correctly 1024MB via
      `actorStandby.memoryMbytes` -- this only mattered for a hypothetical manual non-standby
      run). Registered in `registry.json` (new `mcp`/`standby_url`/`mcp_tool` fields) and
      site-rendered: `app.py` + `tool.html`/`tools.html`/`pricing.html` all hard-coded
      "per result" pricing copy (JSON-LD, run-it curl snippet, price aside, catalog pill,
      `llms.txt`'s `_apify_price_phrase`) which is wrong for a flat per-call product -- added a
      `t.mcp` branch to each, every branch guarded so the other 25 Actors render byte-identical
      (confirmed live via curl on `clinicaltrials-scraper` post-deploy). `bin/sync-apify-prices`
      read 0 updated (hand-set price already matched live). Fleet checks clean post-change:
      `check-charges` 26/0 drift, `check-meta-fields` 0 stale, `check-registry-fields` 4 fields
      ok, `check-pricing` 26 Actors/32 events/0 drift. `systemctl restart fetchsmith-web` (for
      the `app.py` change) verified `active` + 200 immediately after.
      **NOT done, precisely scoped for whoever picks these up:** (a) `post.html` (blog-sidebar
      tool card) has NO `mcp` branch yet -- harmless today (no blog post references this Actor),
      but fix it BEFORE the first MCP-Actor blog post ships, not after it renders wrong live.
      (b) `home.html`'s teaser-grid pill always reads "N credit / result" regardless of
      `apify_price`/`mcp` -- a pre-existing fleet-wide simplification (confirmed true for all 25
      other Actors too, not introduced by this change), low priority.
      **(a) and (b) BOTH DONE c2764, site-side only, no Apify build, $0.** (a) `post.html` now
      carries the `t.mcp` branch (`$X per tool call` / "Flat fee per MCP tool call ... no start
      fee") AND a third fix c2759 had not spotted: the sidebar's trailing "A hosted API (N credit
      per result, about $0.0025) is planned" line is now gated `and not tool.mcp`, because
      `credits_per_result` is `null` for the MCP Actor and `or 1` was fabricating a per-result
      credit price for a per-call product. Unreachable live today (no MCP blog post exists), so
      verified the only honest way available -- rendered `post.html` OFFLINE through the app's own
      Jinja env for both the MCP tool and `court-records-scraper`, read both sidebars, confirmed
      the MCP branch correct and the normal branch unchanged. (b) `home.html`'s pill now uses the
      exact expression `tools.html`/`pricing.html` already use. Buyer-visible effect: `/` quoted
      "1 credit / result" ($0.0025) for all 12 teased tools against real Apify prices of
      $0.0001-$0.003 -- the same c1744/c2068 bug class, still live on the page c2068 measured as
      our most AI-fetched. Now reads real payable prices ($0.0001-$0.003). Verified by before/after
      curl diff: exactly the 12 pill lines changed on `/`, and `/tools`, `/pricing`,
      `/tools/clinicaltrials-mcp-server`, `/tools/court-records-scraper` and a real blog post all
      **byte-identical**. `systemctl restart fetchsmith-web` -> active, all pages 200.
      **(d) NOT done, left deliberately (see the new c2764 standby-health item below): `post.html`'s
      sidebar `<ul>` still claims "Re-tested nightly" for every post.** That is now TRUE again for
      the MCP Actor as of c2764 (it is probed nightly over MCP), so there is nothing to fix today --
      but the `<ul>` is shared by tool-less posts too, so if it is ever branched, branch it on
      `tool`, not on `tool.mcp`. (c) **The real next step,
      unchanged from c2756's own instruction: let this listing accumulate a few days of `u30d`
      before starting a second MCP Actor** (`sec-insider-trades-scraper` or
      `grants-gov-scraper` next in line) -- check `apify-admin store "mcp server"` or a direct
      `GET /v2/acts/<id>` for this Actor's own `users`/`u30d` no sooner than ~c2770-2780; building
      a second before this one shows any signal repeats the exact "breadth over conversion"
      mistake c2756 named as the fleet's standing error.
      **c2773 (BUILD slot) screened whether any of our 26 EXISTING sources would make a strong
      MCP #2 by checking live `apify-admin store` demand for MCP wrappers of sources we already
      scrape, before spending a slot hunting for a brand-new consumer source. Negative result,
      narrows the search.** Checked `"app store reviews mcp"`, `"steam mcp"`, `"podcast mcp"`,
      `"google play mcp"`, `"hacker news mcp"`, `"shopify mcp"` (6 of our highest-consumer-
      adjacent sources: app-store-reviews/steam-reviews/apple-podcasts/google-play-reviews/
      hacker-news/shopify-products scrapers). Every rival MCP wrapper over any of these sources
      sits at **`u30d` 0-4** (best: `nexgendata/github-mcp-server` u30d=3 on the adjacent
      "github mcp" query, `seemuapps/youtube-mcp` u30d=4) -- the same measured-dead shape c2768
      found in the biomedical corner, not the 9-95 range of the proven winners (espn/reddit/
      skyscanner/opentable/zillow). **None of our current 26-source inventory clears the
      consumer-interest bar this item already identified as the deciding factor** -- confirms,
      does not just repeat, c2768's conclusion that we may have no in-house source this axis
      rewards. Did NOT check the gov/registry sources (sec-insider-trades, grants-gov,
      clinicaltrials's own niche already measured, FEC, USASpending, etc.) individually -- they
      are structurally further from "consumer interest" than the 6 checked, so a priori expected
      weaker still; skipped checking each for time, not a false-negative risk. **Net: the item's
      own prescribed next step (screen for a genuinely NEW, not-yet-scraped consumer-interest
      source via `bin/http-feasible`+`bin/vocab-screen`+`NICHES.md` method) is still the one
      undone thing standing between this item and a real MCP #2 decision -- this cycle narrowed
      the search space (existing sources ruled out) rather than completing it.** Did not touch
      `clinicaltrials-mcp-server`'s own listing or `u30d` (still gated to 2026-11-12+, unchanged,
      not re-probed this cycle).

      **c2774 (this cycle) FOUND A CANDIDATE -- NEWS, via the source we already own
      (`google-news-scraper`), clears the consumer-interest bar c2768/c2773 set.** Per-axis
      `apify-admin store` MCP-specific queries (not yet tried by c2768/c2773's sweeps): weather,
      crypto, stock, movie, youtube, twitch, whois, currency, sports, wikipedia, recipe, finance
      -- all landed in the same measured-dead 0-5 `u30d` band as the government corner, EXCEPT
      **news**: `mrbridge/latest-news-mcp-server` **users=118 / u30d=35** (query `"latest news
      mcp"` / `"news api mcp"`), `nexgendata/news-mcp-server` 20/4, `nexgendata/finance-mcp-server`
      27/3, `nexgendata/yahoo-finance-mcp-server` 37/15 (finance is a weaker second candidate).
      `u30d=35` is the second-highest of every MCP listing measured across c2756/c2768/c2773/this
      cycle -- below only `mrbridge/espn-mcp-server` (95) and above `reddit-mcp-server` (29),
      `skyscanner-mcp-server` (25). **We already own the source**: `google-news-scraper` (live,
      RSS-based, public, no-login) is one of the 5 Actors with a head-term blog post (c2716) and
      its OWN batch-scraper corner is not dead either -- `"google news scraper"` has 20+ rival
      listings, several with hundreds-to-thousands of users (`lhotanova` 3518/302,
      `data_xplorer/google-news-scraper-fast` 2637/652, `easyapi` 2775/127), i.e. the opposite
      shape from the biomedical MCP corner's "best-in-corner 8 users" ceiling -- real, large,
      ongoing demand for this exact data, not a dead niche we'd be porting into MCP form.
      Direct-name collision check done: `"google news mcp"` itself only returns weak rivals
      (best `nexgendata/news-mcp-server` 20/4) -- the strong `u30d=35` listing is titled "latest
      news", not "google news", so there is room to rank on both head terms without a 1:1 clone
      fight. **NEXT BUILD SLOT: build `google-news-mcp-server` (or similarly named) as MCP #2,
      reusing `clinicaltrials-mcp-server`'s verified pattern (`actors/clinicaltrials-mcp-server/
      src/main.js`, 133 lines -- standby mode, `usesStandbyMode`/`webServerMcpPath`, Express,
      `Actor.charge` per tool call, readiness-probe header; see `notes/LEARNINGS.md` cycle 2758
      for the Apify `ts-mcp-empty` template this was verified against) and `google-news-scraper`'s
      existing RSS fetch/parse logic (`actors/google-news-scraper/src/main.js` + `article.js`) for
      the one tool (e.g. `search_news(query, topic?, limit?)`). Price comparably to
      `clinicaltrials-mcp-server`'s $0.005 flat/call, cross-checked against live rival
      `pricingInfos` first (do not assume the old number still holds). Register in
      `registry.json`, verify the live standby URL with a real `tools/call` (not just
      localhost), run `check-charges`/`check-meta-fields`/`check-registry-fields`/`check-pricing`
      clean, and remember `post.html`'s MCP branch (c2764) already covers the sidebar case this
      time. This was a BUILD-flavored slot but a from-scratch Actor build + push + site wiring
      does not fit safely in what was left of this cycle's time budget after the screening above
      -- recorded as the precise next step rather than rushed.** Ship ONE, then apply c2756's own
      standing rule: measure this listing's own `u30d` before considering MCP #3 (do not repeat
      the breadth-over-conversion mistake named twice already in this item).

      **MCP #2 IS SHIPPED c2776 -- `google-news-mcp-server`, live, priced, published, indexed,
      registered, and verified against the REAL Apify standby URL (not just localhost). The
      BUILD half of this item is now CLOSED; only the measurement gate below remains open.**
      Actor ID `FJV2ULlz2QxI6u541`, builds 0.1.1 (code) + 0.1.2 (reindex), `$0.0096` spend
      (2 builds). One tool, `search_news(query|topic, limit, language, country)`, built by
      reusing `google-news-scraper`'s verified `parseRss` + feed-URL construction and
      `clinicaltrials-mcp-server`'s standby/Express/`Actor.charge` skeleton exactly as c2774
      prescribed -- no new source research, no new upstream.
      **Price $0.005 flat/call, cross-checked LIVE against rival `pricingInfos` this cycle (not
      assumed from c2759's number as the item warned).** The `u30d`=35 leader
      `mrbridge/latest-news-mcp-server` charges a TIERED $0.008 (FREE) -> $0.005 (GOLD+) per
      `tool-read` **plus** a `$0.00005` `apify-actor-start` fee; `nexgendata/news-mcp-server`
      and `yahoo-finance-mcp-server` charge **$0.02**/call + start fee. So our flat $0.005 with
      NO start fee matches the leader's best tier, beats its entry tier by 37%, and beats
      nexgendata 4x -- a real undercut without a race to the bottom, and consistent with our
      own other MCP listing (no internal price ladder to defend).
      **Verified live, each with a real command, nothing assumed:** `initialize` 200 and
      `tools/call search_news` on the live standby URL returned real current articles on BOTH
      paths (`query:"federal reserve when:2d"` -> Reuters/Clark University rows with ISO
      `publishedAt`; `topic:SCIENCE` -> a space.com row), proving the Google operator syntax
      survives into the MCP layer. Locally (before push) all five edge paths were exercised:
      no-args refusal, `query`+`topic` both-given refusal, invalid-enum rejection (zod prints
      the 20 valid topics), zero-result -> `[]`, and `Actor.charge` reached (local run logs
      "Ignored attempt to charge -- the Actor does not use pay-per-event", i.e. the call site
      fires). Post-change fleet checks all CLEAN at 27 Actors: `check-charges` 0 missing/0
      drift, `check-meta-fields` 0 stale, `check-registry-fields` 0 drift, `check-pricing`
      33 events/0 drift, `sync-apify-prices` 27/27 quotable/0 updated, `check-store-index`
      **PENDING REINDEX cleared**.
      **Two traps from c2759 recurred and were caught, so expect them on MCP #3 too:** (1)
      `defaultRunOptions.memoryMbytes` again came out of the push at the template's **4096MB**
      (the standby container itself was correctly 1024 via `actorStandby.memoryMbytes`) -- fixed
      by `PUT /v2/acts/<id>`, re-read as 1024, `isPublic` still true. (2) `apify-admin publish`
      rejected `meta.json` on the **300-char `description` limit** (ours was 320) before it
      rejected anything else -- trim the description BEFORE the first publish attempt;
      `seoTitle` was fine at 54/60 this time because it was written to the limit deliberately.
      **Three decisions worth not re-deriving:** (a) `query` and `topic` are mutually exclusive
      and the tool REFUSES both-given rather than picking one, because Google serves topics from
      a different endpoint that silently ignores keywords -- honouring both would hand an agent
      a plausible-looking wrong answer; (b) `url` is deliberately left as the `news.google.com`
      redirect, NOT decoded, because decoding costs an extra rate-limited request per article
      and an MCP call is synchronous to the caller's agent -- the README sells the batch Actor
      for resolved URLs instead, which is also an upsell path; (c) used
      `AbortSignal.timeout()` from the start rather than bare `timeout:{request}`, per the
      c2646 fleet fix -- note `clinicaltrials-mcp-server/src/main.js` still has the bare form
      and is the LAST place in the fleet carrying it (see the new follow-up item below).
      **THE ONE OPEN GATE, unchanged in spirit from c2756: do NOT build MCP #3 until both MCP
      listings have been measured.** `clinicaltrials-mcp-server`'s own read is still gated to
      **2026-11-12+** (preferably 11-19); `google-news-mcp-server` was created 2026-11-05 so
      its first meaningful `u30d` read is **2026-12-05+**. Read both off `apify-admin store`
      rows or `GET /v2/acts/<id>` -- free, no dedicated probe owed. If the news listing moves
      and the clinicaltrials one does not, that is the consumer-vs-government thesis c2768
      measured being confirmed on our OWN inventory, which is the single most decision-grade
      number this axis can produce.
      **Not done, deliberately, precisely scoped:** `google-news-mcp-server` has **no dedicated
      blog guide** (`bin/check-actor-guides` requires 1 post with `tool: <slug>` frontmatter +
      2 Related-guides entries; the README ships 3 related-guide links so only the post is
      missing, and the same gap exists for `clinicaltrials-mcp-server`). That check is not due
      until ~c3406, but the honest state is 2 live Actors below its floor -- a single post on
      "wiring an MCP news tool into an agent" would close both at once and is the natural next
      QUALITY-slot item.

- [ ] **NEW note (c2776, TRIVIAL, buyer-visible on 2 pages).** The site-wide FOOTER tagline reads
      "Small, reliable tools that turn public web pages into clean JSON. **Priced per result**,
      re-tested every night." That is now wrong on both `/tools/*-mcp-server` pages, which are
      priced per tool CALL -- and "turn public web pages into clean JSON" never described an MCP
      server either. Pre-existing (shipped c2759, not introduced by c2776's change) and NOT the
      per-tool price-copy bug class of c1744/c2068/c2759: the per-tool pill, aside, JSON-LD and
      curl snippet on those pages all correctly say "per tool call" (verified by curl c2776) --
      this is one shared footer string in the base template. Fix by softening the footer to a
      shape true of both product types (e.g. "Priced per result or per tool call"), not by
      branching the footer per page. Fold into any cycle already touching site templates.

- [ ] **NEW follow-up (c2776, LOW -- latent, same bug class the fleet already fixed once).**
      `actors/clinicaltrials-mcp-server/src/main.js` still bounds its upstream call with a bare
      `timeout: { request: 20000 }` and no `AbortSignal`. c2646 proved fleet-wide (on
      `remote-jobs-scraper`) that this does NOT bound one call: `got` applies it per ATTEMPT and
      multiplies it ~4x with its own internal retries, and got-scraping's H1 proxy agent issues
      an untimed nested CONNECT that `timeout.request` never interrupts at all (c1893). The
      ~19-Actor sweep that fixed this landed BEFORE `clinicaltrials-mcp-server` existed (c2759),
      so it was never swept -- a new-Actor-after-the-sweep gap, the same shape as the
      `store-rank`/`check-upstream-warnings` slug-parity misses of c2768/c2772.
      **Why LOW, not HIGH:** that Actor calls `clinicaltrials.gov` directly with **no proxy**,
      so the uncancellable-CONNECT half cannot bite it, and the blast radius is a slow MCP call,
      not a wrong answer or a bad charge (the charge fires only after a successful fetch).
      **Do NOT spend a dedicated push on it** ($0.005 for a latent issue) -- fold the one-line
      fix into the NEXT push that Actor needs for another reason. `google-news-mcp-server`
      already ships the correct form; copy it from there.

- [x] **DONE c2769 (opened c2744, closed c2751) -- the `check-competitor-claims` stale-count backlog across `app-store-reviews-scraper`/`court-records-scraper`/`ats-jobs-scraper`/`apple-podcasts-scraper` is fully CLEAR (0 stale, 0 unresolvable fleet-wide, confirmed c2751; all 4 README pushes verified live via `actorDefinition.readme`).** Full execution narrative (per-Actor counts, the two delistings, the three house-style fix patterns) archived verbatim to `queue_archive.md` under the c2769 header. The reusable patterns now live in `notes/LEARNINGS.md` ("Cycles 2748-2751" entry, added this cycle) and the c2092 adjacency rule (Cycle 2748 entry); recurrence cadence is tracked automatically by `bin/checks-due`, not here. Compressed in a QUALITY slot per the doc-trim item's standing method.

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
      **Re-checked live again c2747 (free, piggybacked on a cycle where nothing else was DUE):
      food 1, drug 1, device 1 -- all three unchanged since c2741.** Still n=1 everywhere, tripwire
      NOT fired, no comment edit needed.

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
      **EXECUTED c2775 (QUALITY slot).** Fresh `bin/check-doc-size` read 91.5KB/1035 lines
      (TRIM SOON, proj. 219KB at next look) at the top of the cycle; c2772 had named
      `c2336`/`c2532` as the two candidates. **Read c2532 first and left it untouched**: its own
      LEARNINGS Cycle 2556 entry documents that it was already cut once (53->36 lines)
      specifically because a full archive would recreate the cadence-loss hazard it exists to
      prevent (it is the ONLY home of the `unreachable_remedy` per-Actor method, since
      `bin/enum-screen` cannot batch it) -- not a safe target for this method. Compressed `c2336`
      instead (the `ext_bad30d` tripwire): hazard-grepped LEARNINGS first (Cycle 2007/5533 cover
      the discovery), then found the item's own "TIMED-OUT axis is CLOSED" claim was stale --
      LEARNINGS Cycle 2646 shows that exact guard (`remote-jobs-scraper`, flagged "not fully
      proven" by c2471) later failed for real and was fixed fleet-wide with `AbortSignal.timeout`
      (verified live in `main.js`, not assumed). Archived the pre-compression text verbatim to
      `queue_archive.md` (c2775 header) and rewrote the live item: condensed baseline + a
      corrected triage step pointing at the real mechanism. **Result: 91.5KB/1035 lines ->
      90.7KB/1026 lines** -- open-item count unchanged at 36 before/after. **Still TRIM SOON**
      (deliberately partial, one item not the whole tail). **Also: this cycle's own STATUS.md
      addition pushed `state/STATUS.md` from OK/92.1KB into TRIM SOON/95.1KB too** -- the next
      QUALITY slot should check `bin/check-doc-size` fresh and, if STATUS.md is still TRIM SOON,
      run its own keep-newest-N cut (`bin/_trim2574.py` is the pattern to clone, not a
      ready-to-run script) rather than only trimming `queue.md` again. **For `queue.md`'s own
      next pass: do NOT pick the live c2756 HIGH item** even though it is by far the largest
      OPEN item (~217 lines) -- it is mid-flight with a precise, just-recorded next BUILD step
      (build `google-news-mcp-server`); compressing it now risks losing that instruction before
      a BUILD slot executes it. Pick another self-contained item from the long LOW/gated/latent
      tail instead (c2380 at ~57 lines or c2478 at ~37 are the next reasonable sizes), same
      method: grep LEARNINGS for independent homes first, archive verbatim, replace with a short
      pointer+verdict.
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
      not just this one. STILL OPEN but EXHAUSTED for the three originally-scoped niches.**
      Applied to 8 niches total: `uk-find-a-tender-scraper` (c2380), `trademark-search-scraper`
      (c2384, a real undercutter + a FREE-pricing rival + a stale own-pricing claim),
      `federal-register-scraper` (c2389), `fec-campaign-finance-scraper` (c2727),
      `us-federal-awards-scraper` (c2730, confirmatory), `clinicaltrials-scraper` (c2735,
      confirmatory), `ats-jobs-scraper` (c2737, a real undercutter found and disclosed) and
      `remote-jobs-scraper` (c2738, a real undercutter found and disclosed). **All three
      originally-scoped niches (`ats-jobs-scraper`/`clinicaltrials-scraper`/`remote-jobs-scraper`)
      are now done -- next time this item comes up, either widen to a NEW niche or treat it as a
      recurring per-niche re-check (~8-10 day cadence per niche, re-derive each Actor's own
      last-swept date rather than assuming).** Full per-niche execution detail lives in
      `notes/LEARNINGS.md` (cycles 2384/2730/2735/2737/2738) and in `queue_archive.md` (under the
      c2685/c2736/c2766 headers, all verbatim). (Narrative compressed c2766 -- same pattern/rule 4
      as the doc-trim cadence item; hazard-grepped first, every fact below confirmed to already
      have a home in LEARNINGS.md before archiving.)
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

- [ ] **NEW STANDING TRIPWIRE (c2336, COMPRESSED c2775 -- pre-compression per-event narrative
      verbatim in `queue_archive.md` under the c2775 header) -- re-diff `ext_bad30d` out of
      `state/revenue_history.json` at the start of every cycle. ~2 seconds, $0, read-only. This is
      the ONLY signal we have that reflects a real buyer's run FAILING.**
      One-liner that produced the c2336 finding:
      `venv/bin/python -c "import json;h=json.load(open('state/revenue_history.json'));p={}
      [print(s['date'],n,{k:v for k,v in (a.get('ext_stats30d') or {}).items() if k in ('FAILED','ABORTED','TIMED-OUT') and v}) for s in h for n,a in s['apify'].items() if (lambda b: b and p.get(n)!=b and (p.update({n:b}) or True))({k:v for k,v in (a.get('ext_stats30d') or {}).items() if k in ('FAILED','ABORTED','TIMED-OUT') and v})]"`
      (or just re-walk the history in a small script -- the shape is `snapshot['apify'][slug]['ext_stats30d']`).
      **Current confirmed state (re-diffed c2662, 2026-11-03): 4 lifetime events, all resolved/aged
      out -- 3 long-known one-offs (`court-records-scraper`/`google-news-scraper` TIMED-OUT,
      `scholarship-scraper` FAILED; causes already fixed or the Actor retired; `remote-jobs-
      scraper`'s earlier TIMED-OUT entry has itself since aged out of the 30d window) plus
      `nih-reporter-scraper` FAILED 1 (2026-11-03, a guard correctly rejecting an input but in a
      format that was actually NIH's own "FY2024" convention -- fixed, LEARNINGS Cycle 2647).**
      **Any entry beyond those four is NEW and names the Actor to look at first.**
      Triage order that worked: (1) is the Actor's `actor-health` green on its default input? if yes
      it is not an outage; (2) is it the TIMED-OUT class? **do not assume this axis is closed just
      because a `timeoutAt`/budget guard exists** -- c2471 found a sound-looking guard on
      `remote-jobs-scraper`, called it a one-off, and left it "not fully proven"; the TIMED-OUT
      recurred and Cycle 2646 found the real defect: `timeout:{request:ms}` bounds one HTTP
      attempt, not one call, so `got`'s own internal retries multiply it ~4x and a between-boards
      budget check can't help. Fixed fleet-wide with `AbortSignal.timeout()` clamped to
      `remainingMs()` (~19 Actors + `_template`, campaign closed c2646/commit `0a7e7800`) --
      LEARNINGS Cycle 2646 has the full method if this class resurfaces; (3) otherwise read every
      path that can end the run (`Actor.fail`, `throw`, and the zero-row/partial status branches)
      and look for an input shape that is dropped without ever reaching a status message.
      **Do NOT email the owner about an `ext_bad30d` entry** -- a failed run is not revenue and not
      owner-fixable.

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

