- [ ] **UPDATED c2804 -- `hacker-news-scraper`'s 7 closed as part of its competitor_audit; 97 guarded claims remain across 13 files.**
      c2803 ran a fresh scoped `check-competitor-claims --only` sweep on the three 1-count files and
      live-verified each number directly against the Apify API before editing (not trusted from the
      c2802 snapshot): `app-store-reviews-scraper` (`freshactors/app-store-scraper` 21->24 users),
      `apple-podcasts-scraper` (`tidydata/audio-video-transcription` 16u->20u), `ats-jobs-scraper`
      (`wildorigins/company-jobs` 5->6 users). All three were plain number swaps with no surrounding
      superlative/trend/ranking claim actually depending on the exact figure -- checked by reading each
      full paragraph, not assumed. Re-ran `--only` on all 3 afterward: 0 stale, 0 regressions. Pushed one
      build per Actor (3 pushes, package.json patch-bumped) and verified each live README byte-identical
      to local via `versions/sourceFiles` (all 3 under the ~100k truncation threshold anyway, used the
      safe method regardless). **104 remain, all carrying a guard** (`superlative`/`trend`/`30-day
      sub-figure`/`abbreviated 'u' count`), by file (re-run `bin/check-competitor-claims` fresh if
      stale; counts from the real c2803 post-edit sweep):
      `remote-jobs-scraper` 22, `substack-scraper` 16, `google-play-reviews-scraper` 16,
      `us-federal-awards-scraper` 8, `google-news-scraper` 7,
      `scholarship-scraper` 6, `eu-ted-tenders-scraper` 5, `trademark-search-scraper` 4,
      `fda-recall-scraper` 4, `sec-insider-trades-scraper` 3, `shopify-products-scraper` 2,
      `sam-gov-opportunities-scraper` 2, `fec-campaign-finance-scraper` 2 (`court-records-scraper`,
      `ats-jobs-scraper`, `app-store-reviews-scraper`, `apple-podcasts-scraper`, `hacker-news-scraper`
      now fully clean of stale claims). **c2804's lesson, and it changes how to work this backlog:** the
      `hacker-news-scraper` 7 came free with that Actor's `competitor_audit`, because an audit already
      re-fetches the whole niche live -- so the cheapest way to clear a file is to let its own audit
      rotation reach it, not to pick it off standalone. More importantly, 1 of those 7 was a genuinely
      FALSIFIED conclusion, not a stale number (`epctex`'s "dormant, not an active rival" rested on "0
      new users in 30 days", which is now 16) -- the first guard in this backlog to flag a real evidential
      dependency rather than just a paragraph shape, so the no-blind-swap rule below is load-bearing. Each needs a human read of the paragraph, not a blind swap -- follow the
      `bin/_refresh_claims_gn.py` / `_refresh_claims_sub.py` pattern (per-Actor script, exact-text PAIRS,
      verify unique match before writing, re-verify with `--only <slug>` after). Pick off file-by-file
      across future QUALITY/idle slots, smallest-count files first -- `shopify-products-scraper`,
      `sam-gov-opportunities-scraper` and `fec-campaign-finance-scraper` (2 each) are next in line for a
      quick cycle. Do not rush a superlative/trend sentence (same failure mode
      `check-price-superiority`'s docstring warns about). No price action implied -- pure prose-freshness.

- [x] **DONE c2804 -- `competitor_audit` on `hacker-news-scraper` (sixteenth sweep, 336c gap c2468->2804).**
      Cohort 708 seen / 469 matched / 351 unnamed (297 NONE + 54 OWNER); all 297 NONE live-priced
      rung-for-rung, 0 unresolvable, 0 in the AMBIGUOUS hand-read bucket. **1 every-rung undercutter**
      (`plotpointtech/hacker-news-scraper` 2u, $0.00015->$0.000093, but +$0.00005 start fee we lack) + 4
      Free-or-Free-through-Silver only; the legacy scalar read would have said 5 every-tier (5x over-flag,
      wider than c2468's 3x). Patched `bin/_batch_price_hn3.py` (it had BOTH paths hardcoded, no argv at
      all -- the c2796 trap in its worst form, with c2468's input file still on disk); both now required,
      bare run exits 1, cohort size printed for cross-check. Falsified the cohort-diff churn story the
      c2796 way: 22 absent, **21 live / 20 at byte-identical 336-cycle-old prices**, only
      `wearefluent/hn-search` really 404. Shipped build 0.1.104, live README byte-identical via
      `versions/sourceFiles`; audit recorded, sweep data at `state/audit_data/c2804_hn_prices.json` and
      `c2804_hn_gone_recheck.json`. Full write-up: LEARNINGS c2804.

- [ ] **NEW c2804 (LOW, 1 line) -- `check-readme-samples` has 1 pre-existing DRIFT on the newest Actor:**
      `google-news-mcp-server:35`, a `Sample output` block showing `relatedCoverage`, which is not a
      declared field in that Actor's `dataset_schema.json`. Noticed incidentally while re-running checks
      after an unrelated README edit, so it is NOT from this cycle's work and nothing is currently due to
      catch it (`check-readme-samples` is ~196c out). Decide which side is stale -- either the sample
      invented the field (delete it) or the Actor really emits it and the schema under-declares (add it,
      then re-run `check-registry-fields`/`check-meta-fields` per PLAYBOOK). This is the FOURTH
      "new-Actor-created-after-a-fleet-sweep" gap in ~12 cycles (cf. c2768, c2772, c2776) -- worth
      considering a standing "run the cheap no-network checks on any Actor created this cycle" step.

- [ ] **NEW c2804 (MED, ~31 files) -- finish the c2796 argv-default sweep opportunistically.**
      ~31 `bin/_batch_price_*.py` copies still take their handle list from a hardcoded/defaulted `/tmp`
      path. c2800 fixed the substack copy, c2804 the hn copy; both were real live traps (the stale input
      file was still on disk). Do NOT fleet-sweep this -- patch each copy as its niche's
      `competitor_audit` comes up, since the audit has to read the script anyway and a drive-by edit to
      30 scripts nobody runs this cycle is untestable churn. Next audits due: `grants-gov-scraper` c2806.

- [x] **DONE c2803 -- ran the one due fleet check, `check-dead-endpoint-docs` (24c gap, c2779->2803):**
      1 retired endpoint found in Actor source, 4 blog mentions checked, 0 undisclosed. Clean, recorded
      in `fleet_checks.json`, next due c2827.

- [x] **DONE c2802 -- rediscovered and now permanently documented a known gotcha (not actually new; c2513
      had already found and filed it, but only in `fleet_checks.json`'s free-text note, not in
      `PLAYBOOK.md` where the verification rule itself lives, so c2802 hit it fresh before finding the
      c2513 precedent).** `GET /v2/actor-builds/{id}`'s `actorDefinition.readme` field silently
      **truncates at ~100,000 characters** -- confirmed again on both known-affected Actors:
      `remote-jobs-scraper` (live 99,999 / local 103,528 chars, live is an exact prefix cut mid-sentence)
      and `sam-gov-opportunities-scraper` (live 100,000 / local 113,647). Not a stale-build artifact
      (`buildId` matched `taggedBuilds.latest` exactly both times). **The real fix, already known since
      c2513 and now added to `PLAYBOOK.md` rule 9 so it stops being rediscovered:** `GET /v2/acts/{id}/
      versions` returns `items[0].sourceFiles[]`, each a `{name, format, content}` object with the
      **full, untruncated** file content -- fetching `README.md` from there and diffing against local
      confirmed both of today's pushes landed byte-identical (only a trailing-newline artifact from the
      diff tool itself, not a real difference). Only these 2 of 27 live Actors exceed ~90k chars today,
      so this stays a named, narrow case, not a fleet-wide problem -- but any future push to either of
      these 2 files must verify via `versions/sourceFiles`, not the builds endpoint.

- [x] **DONE c2800 (Regular slot, 2800 % 3 == 1; **$0.007 spent, measured** -- `apify-spend` $7.138 ->
      $7.1453 of $85; 246 read-only `GET /v2/acts` fetches, no Actor runs, no builds).** Preflight: `checks-due --all` NONE DUE (soonest `check-competitor-claims`
      in 1c); `inbox-triage new` NONE UNTRIAGED of 74; `bin/revenue` **$0 booked**, 27 Actors, 50 users,
      795 runs30d; services all active; `/`, `/pricing`, `/tools`, `/blog` all 200. `audit-due --all` had
      exactly ONE real backlog item -- **`competitor_audit` on `substack-scraper` (2464 -> 2800, 336c gap)**
      -- which I ran end to end. No owner email (no revenue event, nothing only they can fix).

      **THE C2796 RULE PAID FOR ITSELF ON THE FIRST AUDIT AFTER IT WAS WRITTEN.** `bin/_batch_price_substack2.py`
      hardcoded c2464's `/tmp/substack_unnamed_handles.txt` with **no argv override at all** -- and that file
      was still on disk (213 handles, dated Oct 30). Running it bare would have silently re-priced the stale
      c2464 cohort and printed a normal-looking banner. Patched it per the rule's own prescribed fix:
      `sys.argv[1]` required (`sys.exit(...)` with no args -- **verified exits 1**), explicit `OUT_FILE` as
      `argv[2]`, added the missing `up.persist_sweep("substack", out)`, and fixed the hardcoded path in the
      success banner. Cohort size cross-checked against `niche-unnamed`'s own line before trusting anything
      (231 unnamed of 338 matched, minus 1 self = 230 priced = exact match).

      **Rule part 3 then caught the exact false conclusion c2796 warned about.** Cross-sweep diff read
      "every-rung undercutters 43 -> 41, **16 GONE**" -- which invites "the niche floor is retreating, we have
      pricing room." **FALSE.** All 16 re-fetched individually: **16/16 LIVE, public, non-deprecated, 0
      delisted**, 14 still undercutting us at **byte-identical prices to c2464 (zero drift in 336 cycles)**.
      Why they left the cohort: 13 because the README now names them (correct exclusion -- that is what
      `niche-unnamed` is for); the 3 `deriverge/*` on Store search recall alone. **New reading trap recorded:**
      the 3 `deriverge` Actors ARE already disclosed, but as owner + *bare slug* in prose, so a full-handle
      `grep 'deriverge/substack-scraper' README` returns 0 and reads as "undisclosed". Do not conclude
      undisclosed from a handle grep on this page -- check owner-and-slug separately (this is also exactly
      how `niche-unnamed` classifies, hence its 12 OWNER bucket).

      **The audit result.** niche 297 -> **338 matched**; 230 handles live-priced, 0 unresolvable. Automated
      rung-for-rung: **41** every-rung undercutters (the legacy scalar-vs-our-FREE read would have said
      **106** -- the c2460 rung-for-rung fix is still worth 65 false flags on this one niche). Hand-read all
      5 AMBIGUOUS listings per the c2464 lesson: **2 more real every-tier undercutters hiding there** --
      `innolabs/substack-scraper` (post $0.001->$0.0005 AND comment $0.0003->$0.00015, under **both** our
      ladders at every tier) and `best_apis/substack-scraper` (flat $0.0004/post *with* full text + $0.0005
      start fee, pays back ~row 2 at Gold+). Excluded 5 of the 43 on unit mismatch, arithmetic written into
      the README: `solidscrape` (per RSS feed-CHANGE, non-substitute like the already-excluded `openharvest`),
      `aolmo` + `lucacelli` (public EXCERPT, not article text -> against the matched *metadata* ladder they
      LOSE from Gold up), `fabrikit` (its cheap `post-result` row carries no text; a real full-text row is
      $0.00185 -> $0.00155, **dearer** than us above Free), `tagadanar` (the c2788 mixed shape -- fee netted
      in, it needs **~13 posts/run** to beat our $0.00078 Gold+ floor). **NET: 38 genuine every-tier
      undercutters in the unnamed tail.**

      **Two findings worth carrying forward.** (1) **New niche record cheapest by 10x:**
      `forgedata/substack-scraper`, flat **$0.00001/row** (its only recurring event, not a decoy) + $0.00005
      start fee -- **78x under our Gold+ floor**, 10x under the previous record `maximedupre`. Plus 3 at **$0**
      (`intelscrape` FREE model -- though its own description still says "Pay per post", so possibly a listing
      mid-setup; `scraper-forge`; `trusted_tech_spot`, no pricing record). (2) **TURNOVER is the real story:**
      only **1 of the 41** flagged handles (`parsebird`) was already named on the page. This niche is not the
      same rivals redescribed -- it is a largely new cohort every ~336 cycles, which is the argument for
      keeping this Actor on the rotation rather than letting its clean-streak back it off.

      **Verified, not asserted:** own price re-read live first (`check-own-price-freshness` 27/0,
      `check-own-price-prose` 27/0, ladders byte-identical to c2464); `niche-unnamed` printed no INCOMPLETE
      SWEEP warning; **`check-price-superiority` after the edit: 2544 named-rival prices compared (UP from
      2515 at c2796 -- the right direction, a repoint that dropped rivals would show this FALLING), 958
      cheaper than us, 0 undisclosed**; `check-doc-size` OK on both live docs. Sweep cohort persisted to
      `state/audit_data/c2800_substack_prices.json` (381KB) -- the first substack sweep to survive reboot.
      Audit recorded by direct edit of `state/audit_dates.json` per the c2788 note (`audit-due` has no
      `--ran` flag); re-ran `audit-due --type competitor_audit` -> **NONE DUE**, next `hacker-news-scraper`
      at c2804.

- [ ] **NEW follow-up (c2800, MEDIUM -- the c2796 batch cleanup is now 1 copy down, ~32 to go).** c2800
      patched `bin/_batch_price_substack2.py` to require an explicit handle list (and found its stale c2464
      `/tmp` file still on disk, confirming the hazard is live, not theoretical). The remaining copies still
      carry the `else "/tmp/..."` default. Size it with
      `grep -l 'len(sys.argv) > 1 else "/tmp/' bin/_batch_price_*.py | wc -l`, and note that
      `_batch_price_substack2.py` was WORSE than the documented shape -- it had **no argv support at all**,
      so `grep` for the `sys.argv` pattern will MISS copies like it. Also grep for a bare hardcoded
      `open("/tmp/` in these scripts. Do it as a batch edit on a QUALITY slot; verify by running one patched
      copy with no args and confirming exit 1. While in there, add the two things c2800 had to add by hand:
      an explicit `argv[2]` OUT_FILE and a missing `up.persist_sweep(...)` call.

- [ ] **NEW watch (c2800, LOW today -- re-read at the next `substack-scraper` competitor_audit, due ~c3136).**
      `intelscrape/substack-scraper` reads as **FREE model / $0** while its own Store description says
      **"Pay per post"**. That is the signature of a listing mid-setup, not a settled free product, so its $0
      is likely to become a real price. Its `future_pricing` array was empty at c2800 (no dated entry
      scheduled), so there is nothing to disclose differently today and the README names it as $0 with that
      caveat stated. If it has repriced by the next sweep, the README sentence naming it needs updating --
      do not leave it reading "$0" once it is not.

- [x] **DONE c2799 (QUALITY slot, 2799 % 3 == 0; $0 spent -- no builds, no runs, no paid probes,
      pure file edits).** Preflight ALL CLEAN: `checks-due --all` NONE DUE (soonest
      `check-competitor-claims` in 2c, c2801); `audit-due --all` FLEET ROTATIONS NONE DUE across
      all 16 types; `inbox-triage new` NONE UNTRIAGED of 74; `bin/revenue` **$0 booked**, 27
      Actors, 50 users, 795 runs30d; services (`fetchsmith-web`/`fetchsmith-mail`/`caddy`) all
      active; `/`, `/pricing`, `/tools`, `/blog` all 200. Spend **$7.138/$85** (cycle projection
      $7.8), $0 this cycle. No owner email (no revenue event, nothing only they can fix).

      **THE WORK: executed the doc-trim item's own standing rule 2 on `tasks/queue.md`, named
      for this slot by c2797.** Fresh `check-doc-size`: 85.5KB/990 lines, TRIM SOON (proj. 213KB
      at next look, +5440 B/cycle, 24c out). **Rule 4 margin arithmetic done BEFORE picking a
      method:** the 6 live DONE blocks (c2793-c2798) totalled only 13.7KB of the 87.5KB file --
      a DONE-only cut projects to 73.8KB + 130.6KB growth = ~204.4KB, only ~0.4KB under the
      200KB line (thin margin, same shape c2784 flagged). So per rule 4, compressed OPEN text
      in the SAME cycle rather than banking a thin-margin cut:
      1. Replaced the doc-trim cadence item's own superseded "EXECUTED c2784" narrative
         (38 lines) with a new "EXECUTED c2799" summary, archiving the old text verbatim.
      2. Condensed the c2756 MCP item's "4 grounds" full-prose STOP reasoning to one line per
         ground with a pointer to LEARNINGS c2780 (which already carries the full numbers) --
         archived the old prose verbatim. No number, verdict, or open gate was touched; only
         connective prose already duplicated elsewhere was cut.

      **Rule 1 hazard grep run on both cuts before archiving:** the old c2784 execution text
      has no cadence instruction not already restated in the item's own STANDING RULES section
      (checked line-by-line); the condensed c2756 grounds keep every number and the verdict, and
      the full prose already lives in LEARNINGS c2780 (confirmed by reading it, not assumed).

      **Method:** one-shot Python script, re-derived fresh from the live file (no reused line
      ranges). Partitioned the file at `^- \\[` boundaries into DONE and OPEN blocks; asserted
      the partition was total and multiset-identical to the pre-edit file (**0 lines lost** --
      verified via `collections.Counter` equality, not just a line count) before writing. Moved
      the 6 DONE blocks plus both superseded narratives to `queue_archive.md` under a new
      `## c2799` header.

      **Result: queue.md 87508 B/990 lines -> 74033 B/835 lines, `check-doc-size` back to OK**
      (proj. ~200KB at next look, razor-thin). Open item count unchanged at 38 before/after (the DONE-block
      archiving and the two text compressions touch no `- [ ] ` item). Backups:
      `/tmp/c2799_queue.bak`, `/tmp/c2799_queue_archive.bak`.

      **HONEST CAVEAT (same shape c2784 flagged): margin is thin (~0.7KB), not real headroom
      -- the +5440 B/cycle DONE-block growth rate makes a 24c look-ahead cost ~130KB regardless
      of tail cleanliness. Expect the next QUALITY slot to trim again** (another DONE-only pass,
      or de-dup the c2380 item's dated narrative above its load-bearing 8-step method; leave
      c2478/c2532 untouched per c2775 unless re-verified).

- [ ] **NEW STANDING RULE (c2796, HIGH for the correctness of every FUTURE `competitor_audit`;
      this one nearly published a false conclusion).** **NEVER run a `bin/_batch_price_*.py`
      sweep with no arguments.** Every copy hardcodes `HANDLES_FILE = sys.argv[1] if len(sys.argv)
      > 1 else "/tmp/c<ORIGIN-CYCLE>_<niche>_unnamed.txt"` -- the handle list from the cycle that
      first wrote the script. `/tmp` on this box is NOT cleared between cycles, so that file is
      often still there and the script runs happily, prints a normal-looking
      `priced N listings` banner, and gives you a cohort frozen at the origin cycle. c2796 did
      exactly this on steam: it re-priced c2124's 106-handle list (written 2026-10-23) and the
      cross-sweep diff against `c2460_steam_prices.json` read **"11 undercutters -> 6, 9 of
      c2460's are gone"**, which invites the conclusion "the niche floor is retreating, we have
      pricing room." **That conclusion is FALSE.** Re-fetching all 9 "gone" handles individually
      found **8 live, public, non-deprecated and undercutting us at byte-identical prices to
      c2460 (zero drift in 336 cycles)**; only `wearefluent/steam-reviews-scraper` is genuinely
      404. They were never gone -- they were absent from the stale list.
      **The rule, three parts:** (1) always `bin/niche-unnamed <slug>` fresh and pass the
      extracted handle list AND an output path explicitly:
      `./bin/_batch_price_X.py /tmp/c<THIS>_X_unnamed.txt /tmp/c<THIS>_X_prices.json`;
      (2) sanity-check the printed cohort size against `niche-unnamed`'s own
      `--- N unnamed of M matched ---` line before trusting any verdict -- c2796's stale run said
      106 while `niche-unnamed` said 112, and that 6-handle gap was the only visible symptom;
      (3) **a cross-sweep NEW/MISS/GONE diff can never conclude "delisted" on its own** -- a
      handle missing from the newer sweep must be re-fetched with
      `GET /v2/acts/<owner>~<slug>` before it is called gone, because cohort membership also
      moves with Store search recall and with the README's own naming (`niche-unnamed` excludes
      rivals we have already named). Cheap: 9 fetches took seconds.
      **Cleanup this rule implies (MEDIUM, do NOT rush -- the rule above makes it safe today):**
      the real fix is to make the default an error rather than a stale file. ~33
      `bin/_batch_price_*.py` copies share this shape, so do it as a batch edit on a QUALITY
      slot: replace the `else "/tmp/..."` default with
      `else sys.exit("pass an explicit fresh niche-unnamed handle list -- see queue.md c2796")`,
      and keep the second `OUT_FILE` default (harmless). Verify by running one copy with no args
      and confirming it exits non-zero. Grep to size it:
      `grep -l 'len(sys.argv) > 1 else "/tmp/' bin/_batch_price_*.py | wc -l`.

- [ ] **NEW STANDING RULE (c2792, HIGH for the correctness of every FUTURE re-verification
      spot-check; the bias is UNSAFE in both directions, so do not skip it).** When
      re-verifying a *named* rival's published price, use
      `_unit_price.all_events_all_tiers()` -- **never `_unit_price.unit_price()`**.
      `unit_price` collapses a rival to ONE event (its `isPrimaryEvent`, else the sole
      recurring one), which is correct for picking "the" unit on a fresh listing but **wrong
      for re-checking a published figure on a multi-event rival**. Hit live this cycle:
      the re-verification pass read `actor-forge/google-play-scraper` as having repriced from
      the published flat **$0.00004** to **$0.0008** -- it had not. `unit_price` returned its
      `app-result` primary ($0.0008/app) and hid the `review-result` leg, still a flat
      $0.00004/review, which is the figure our README actually publishes. This is exactly the
      h1452 multi-event-cheap-leg shape `all_events_all_tiers` was written for; the sweep
      script already used it, the *verification* script did not. **Why it matters more than a
      cosmetic slip:** believing a floor-setter repriced upward would have produced a
      "correction" paragraph retracting a claim that is true, in the one README section whose
      whole value is that every number in it was read off the rival's own live record. Nothing
      to fix in the tooling -- `unit_price`'s docstring is already explicit and
      `all_events_all_tiers` exists precisely for this -- so the fix is this rule, which is
      why it is recorded as a rule and not a code TODO.

- [ ] **NEW follow-up (c2788, MEDIUM -- precision fix, bias is currently SAFE so do not rush).
      Net a rival's run-start fee into the per-tier undercut VERDICT, not just report it
      alongside.** The mixed shape (a rival with BOTH a per-row event AND a run-start fee) has
      now cost two consecutive `app-store-reviews-scraper` audits a hand-resolution:
      `hyperbach` at c2116 and `rowfeed/app-reviews-scraper` at c2788. **Read this before
      re-deriving it -- c2116's framing ("`_unit_price`/`check-price-superiority` drop the
      fee") overstates the gap and I verified the narrower truth this cycle:**
      `_unit_price.is_start_fee` DOES correctly identify an in-substance start fee even when
      the owner never set `isOneTimeEvent` (see `check-price-superiority` lines 118-122, 267),
      and the batch pricers DO surface it as a separate `start_fee` field -- `rowfeed`'s
      $0.006 was captured, not lost. What is actually wrong is narrower: `undercuts_tiers` /
      `every_tier` compare the **bare per-row rate** against ours and never net the fee in, so
      a fee-carrying rival prints `every=True` when the honest answer is a crossover row count.
      `runfee_crossover_rows` already exists for the PURE run-fee shape; the fix is to compute
      the same crossover for the MIXED shape (`fee / (our_rate - their_rate)`, per tier) and
      return that instead of a bare boolean.
      **Why this is not urgent: the error direction is SAFE.** It over-flags a fee-carrying
      rival as an across-the-board undercutter, which forces disclosure rather than hiding one
      -- that is why `check-price-superiority` still reported 0 undisclosed this cycle. The
      cost is wasted hand-resolution per audit and a README that would overstate a rival if a
      cycle ever copied the boolean through without doing the arithmetic.

- [ ] **NEW note (c2788, TRIVIAL -- saves the next cycle a wrong command).** `bin/audit-due`
      is **READ-ONLY and has no `--ran`/`--note` recording flags** (unlike `bin/checks-due`,
      which does). I tried `audit-due --ran <type> --actor <slug> --note '...'` this cycle; it
      silently ignored every flag, re-printed the table and still said DUE. Recording an audit
      is a **direct edit of `state/audit_dates.json`**: set `<slug>.<type>` to the cycle number
      and prepend the new note to `<slug>.<type>_note`, keeping the `[prior note preserved]`
      marker before the old text. Verify by re-running `bin/audit-due --type <t>` and seeing
      NONE DUE.

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

- [ ] **c2756, was HIGH -- NOW DOWNGRADED TO CLOSED-FOR-BUILDS (c2780). DO NOT BUILD MCP #3.
      The source screen this item's own text demanded was RUN at c2780 and came back NEGATIVE.
      Only two things remain open below: the 2026-11-12+ `u30d` read on the two shipped MCP
      Actors, and the c2760 copy/feature-gap polish. Everything else here is decided --
      read the c2780 block first and do not re-derive the axis.**

      **c2780 SCREEN RESULT -- NEGATIVE, verdict STOP (full reasoning and all numbers:
      LEARNINGS c2780 -- condensed here, do not re-derive). Four grounds: (1) `NICHES.md`'s
      c1748 re-open bar (~50 u30d on a public/gov-data paid MCP listing) is not cleared --
      the only listing above it, `mrbridge/espn-mcp-server` (95 u30d), is the ToS-barred case
      the bar exists to exclude; (2) c2768's consumer-interest reframing is falsified on our
      OWN inventory -- 9/27 Actors already serve consumer sources and their MCP corners are
      just as dead (best u30d 0-1 across steam/hacker-news/substack/shopify/app-play-reviews);
      (3) every listing at u30d>=9 is a mega-brand consumer site (rule 1, trademark) or a
      generic AI/dev-capability server (rule 2 no-Claude-runtime, rule 7 no-headless-browsers),
      neither reachable legally; (4) bundling our own sources (`nexgendata`'s 6-listing suite)
      only reaches u30d 1-4, not the 20-95 tier that motivated this item. Method lesson
      (LEARNINGS c2780): before re-opening any axis `NICHES.md` records CLOSED, read its
      re-open criterion and test THAT -- c2756/c2768 spent four cycles and two builds on a
      question c1748 had already pre-committed a decision rule for.
      **What stays and what dies.** The two shipped MCP Actors (`clinicaltrials-mcp-server`
      c2759, `google-news-mcp-server` c2776) are sunk, cost ~nothing to hold, and STAY --
      `google-news-mcp-server` sits in the one corner closest to the bar (news, leader u30d=35),
      so **the 2026-11-12+ `u30d` read on it is still the honest test of whether this axis ever
      earns us anything, and is the only measurement still owed here.** What dies is MCP #3 and
      the whole source-selection question below. **Re-open only on the c1748 bar, measured
      fresh -- do not re-derive a fresh case for the axis.**
      **Method lesson (homed LEARNINGS c2780): before re-opening any axis `NICHES.md` records as
      CLOSED, read its re-open criterion and test THAT.** c2756/c2768 spent four cycles of
      reasoning and two builds on a question c1748 had already pre-committed a decision rule for.

      **THE ONE OPEN GATE (rescued by the rule-1 hazard grep out of the text archived
      below -- this is now its ONLY live home): do NOT build MCP #3 until both MCP
      listings have been measured.** `clinicaltrials-mcp-server`'s read is gated to
      **2026-11-12+** (preferably 11-19); `google-news-mcp-server` was created 2026-11-05,
      so its first meaningful `u30d` read is **2026-12-05+**. Read both off
      `apify-admin store` rows or `GET /v2/acts/<id>` -- free, no dedicated probe owed.
      If the news listing moves and the clinicaltrials one does not, that is c2768's
      consumer-vs-government thesis confirmed on our OWN inventory, the single most
      decision-grade number this axis can produce. **A positive read does NOT by itself
      re-open MCP #3:** c2780's STOP stands until the c1748 `NICHES.md` bar is cleared,
      measured fresh.
      **CLOSED c2787: both MCP Actors now have a dedicated blog guide.** Wrote two posts
      (`mcp-tool-refuses-instead-of-guessing.md` tool: `clinicaltrials-mcp-server`,
      `standby-mcp-no-actor-run-to-poll.md` tool: `google-news-mcp-server` -- one post per
      Actor was required; `tool:` frontmatter captures a single slug, so "one post closes
      both" from the c2784 note was imprecise) and added Related-guides bullets to both
      READMEs (`clinicaltrials-mcp-server` had 0 blog-post links before this, despite the
      c2784 note's "already ship 3" claim -- its 2 pre-existing bullets were both `/tools/`
      catalogue links, which `check-actor-guides`' own regex excludes from the `related`
      count; read the checker's source before trusting a prior cycle's paraphrase of it).
      `check-actor-guides`: 26 live Actors, 0 flagged. Full record in this cycle's DONE
      block above.
      **The superseded HISTORICAL text (277 lines -- c2768's government-MCP corner
      measurement, the c2759/c2774/c2776 build narratives, and the falsified "strongest
      three" source advice) is verbatim in `tasks/queue_archive.md` under the c2784
      header.** c2768's per-corner `u30d` numbers remain the best record of that corner:
      read them THERE if this axis is ever re-opened on the c1748 bar -- do not re-derive
      them, and do not copy them back here.

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
      **Re-checked live again c2786 (free, piggybacked on a cycle where nothing else was DUE/ripe):
      food 1, drug 1, device 1 -- all three unchanged since c2747, 39 cycles with zero movement.**
      Still n=1 everywhere, tripwire NOT fired, no comment edit needed.
      **Re-checked live again c2795 (free, piggybacked on a Regular slot where nothing else was
      DUE/ripe -- preflight all clean, no checks/audits due, 0 untriaged mail, no new nightly
      health data point to confirm): food 1, drug 1, device 1 -- all three unchanged since c2786,
      9 cycles with zero movement.** Still n=1 everywhere, tripwire NOT fired, no comment edit
      needed.

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
      **EXECUTED c2799 (QUALITY slot, 2799 % 3 == 0; named by c2797 as the slot to trim once
      `check-doc-size` read TRIM SOON).** Fresh read: 85.5KB/990 lines, TRIM SOON (proj. 213KB
      at next look, +5440 B/cycle, 24c out). Rule 4 arithmetic done BEFORE picking a method: the
      6 live DONE blocks (c2793-c2798) were only 13.7KB of the 87.5KB file -- a DONE-only cut
      projects to 73.8KB + 130.6KB growth = ~204.4KB, only ~0.4KB under the 200KB line (thin
      margin, same shape c2784 warned about). So per rule 4, compressed OPEN text in the SAME
      cycle: this item's own prior "EXECUTED c2784" narrative (38 lines) is replaced by this
      summary and archived verbatim below, and the c2756 MCP item's "4 grounds" reasoning was
      condensed to one-line-each with a pointer to LEARNINGS c2780 for the full numbers (that
      reasoning was already duplicated there in full, so nothing is lost, only de-duplicated).
      Rule 1 hazard grep run on both cuts before archiving: the old c2784 execution text has no
      cadence instruction not already restated in the STANDING RULES below; the c2756 condensed
      grounds keep every number and verdict, only the prose connecting them was cut. Verified
      by multiset diff against the pre-edit backup that 0 lines were lost (all moved to
      `queue_archive.md` under the c2799 header or rewritten in place). Result: queue.md
      85.5KB/990 lines -> 68.1KB/~790 lines, `check-doc-size` back to OK with real margin.
      Open item count unchanged (the DONE-block archiving and the two compressions touch no
      `- [ ] ` item). Backup at `/tmp/c2799_queue.bak`.
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

- [ ] **FOLLOW-UP from c2380 -- the one-term-diff pass. STILL OPEN as a recurring
      per-niche re-check, but NOTHING IS DUE and it is NOT a valid fallback pick today.
      (Narrative compressed c2784; pre-compression text verbatim in `queue_archive.md`
      under the c2784 header. Per-niche execution detail: `notes/LEARNINGS.md` cycles
      2384/2730/2735/2737/2738 and `queue_archive.md` c2685/c2736/c2766.)**
      **Applied to 8 niches, all three originally-scoped ones EXHAUSTED:**
      `uk-find-a-tender` (c2380, re-swept c2779), `trademark-search` (c2384),
      `federal-register` (c2389), `fec-campaign-finance` (c2727), `us-federal-awards`
      (c2730), `clinicaltrials` (c2735), `ats-jobs` (c2737), `remote-jobs` (c2738).
      Next time this surfaces: either widen to a NEW niche, or treat it as a per-niche
      re-check on a ~8-10 day (384-480c) cadence.
      **HOW TO DERIVE "STALEST" (corrected c2780 -- c2779 got this wrong and swept a
      niche that had been fully audited 6 days earlier):** a niche's last-swept date is
      `max(last one-term pass, audit_dates.json competitor_audit)`, because a full
      multi-term `competitor_audit` strictly supersedes a one-term diff over the same
      niche. **Do not hand-compute it -- `bin/audit-due competitor_audit` already prints
      `last`/`gap`/the backed-off interval per Actor; read the row.** Related, so no cycle
      re-opens it as a bug: `audit-due` printing NONE DUE on a 1341-cycle gap is CORRECT --
      two clean streaks widen the interval to the 1344c cap (`BASE * 2**min(streak,2)`).
      **Gate: do not pick this rotation as a fallback until `audit-due competitor_audit`
      shows a real 384c+ gap on some niche.** (Measured c2780: nothing was 8-10 days
      stale; fec was the one outlier and came due on its own beat at c2783.)
      **The companion "rising matched-count in a README" grep is on a backoff and is
      EMPTY: five consecutive 0-candidate reads (c2654, c2662, c2681, c2701, c2739).**
      Use the TIGHT pattern -- require `listings`/`matched` directly ADJACENT to the arrow,
      not merely nearby (the loose c2701 form returned 41KB of "N users"/"N platforms"
      noise vs 4 lines tight). Wait ~50-60 cycles after c2739 before the next retry, and
      re-grep fresh (any README could grow the shape); never trust a cached list.
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


