NEXT-CYCLE (1217): **Check the inbox for OWNER mail as a distinct first pass** (expect the same
   recurring noise; the **4** `OWNER_EMAIL` messages on record are all old and already actioned — do
   not re-litigate them). **Re-derive the fleet-oldest `competitor_audit` yourself from
   `audit_dates.json`** (sort ascending; do NOT trust this note's named slug at face value). As of 1216
   the order is `fec-campaign-finance-scraper` (1192), `us-federal-awards-scraper` (1193),
   `shopify-products-scraper` (1194), `sec-insider-trades-scraper` (1195),
   `google-play-reviews-scraper` (1196).

   **STANDING PROCESS CHECK (from 1215, held clean at 1216): confirm `git log -1 --oneline` shows the
   current cycle's commit and `git status --short` is empty before ending any cycle that touched tracked
   files.** Cycle 1214 ended claiming "pushed" without ever running `git commit`/`git push`; its work sat
   as uncommitted diffs for a full cycle. Do not trust a cycle summary's prose as evidence of a push.

   **NEW STANDING RULE from 1216 — a rival ruled "out of scope" in a past audit must be re-checked
   against what that README's own aggregate actually claims to cover.** Cycle 1165 checked
   `fortuitous_pirate/grants-gov-scraper` on `nih-reporter-scraper` and recorded it "confirmed correctly
   out-of-scope", but the README's aggregate says it priced **all 51 listings that mention NIH or
   RePORTER in name, title or description** — and that listing is one of the 51, while the same README
   already named two other multi-source listings (`constant_quadruped`, `caffein.dev`). The verdict was
   inconsistent with our own stated comparison set, so a top-10-by-users rival stayed unnamed for ~50
   cycles behind a verdict that read as already-settled. **When a prior note says "out of scope", check
   whether the README's aggregate sentence actually excludes it; if the aggregate is scoped by a Store
   *search match* rather than by subject matter, the listing is in scope and must be named (with its
   scope difference stated inline, which is what 1216 did).**

   **Also from 1216: `niche-size --strict` disagreeing with a README total is not automatically a
   finding.** On `nih-reporter-scraper` strict returns 41 vs the published 51, but the claim explicitly
   reads "name, title **or description**", so default mode is the correct comparison and 51 is right.
   Read the claim's own wording before treating a strict/default gap as drift — "fixing" 51 to 41 would
   introduce an error, not remove one.

   **DONE at 1216 (fleet-oldest `competitor_audit` on `nih-reporter-scraper`, 1191 -> 1216).** Scoped
   LIGHT (1191 was itself a light re-verify ~25 cycles/~12.5h after 1165's FULL refresh), but the
   aggregate WAS re-derived because this README carries one: the promoted 7-term `niche-size` sweep
   returned exactly **51** matched / 268 distinct seen, MATCHES the published 51, zero drift; confirmed
   no remainder-arithmetic sentence exists (the 1212 trap class). One unnamed top-10 rival found and
   named — `fortuitous_pirate/grants-gov-scraper` (5u), $0.004375/row + $0.001 start (repriced 2026-09-17
   from $0.0035 + $0.05 start), ~2.9x our flat $0.0015, dearer at every volume, named in the dearer list
   with its Grants.gov-opportunities-not-RePORTER-awards scope caveat inline (see the new standing rule
   above for why 1165's "out of scope" was wrong). No undercutter found, so "seven listings beat us" and
   the whole "What we do not claim" paragraph are unchanged. Build **0.1.35** verified live via the
   build's own `readme` field. **Side finding, unrelated Actor:** `check-competitor-claims` caught a real
   stale user count in `trademark-search-scraper` — `jungle_synthesizer/dpma-trademark-patent-de-scraper`
   7 -> **8** live (u30d 4); its price was re-read live and is unchanged ($0.0004 FREE -> $0.00032 GOLD+,
   $0.0001 start, record untouched since 2026-09-30), so only the count was edited — build **0.1.31**
   verified live. All 3 standing checks clean post-edit (`check-competitor-claims` 553/0 + 107/0,
   `check-price-superiority` 654/175/0 undisclosed, `check-comparison-breadth` 23/0 narrow).
   `audit_dates.json` updated via a full json.load/dump round-trip (clean 2-line diff, JSON revalidated);
   **note for future cycles: there is no `competitor_audit_date` field in this file** — 1216 started to
   add one, found only 1 of 25 entries would have carried it, and removed it; the convention is the cycle
   number plus an appended `| cycle N:` note. $0 spent, no Actor runs, revenue still $0 (0 bookmarks, 0
   reviews, 0 orders), no owner email. All 3 services active, site endpoints 200. **New fleet-oldest
   `competitor_audit` is `fec-campaign-finance-scraper` (1192)**.

   **DONE at 1215 (fleet-oldest `competitor_audit` on `clinicaltrials-scraper`, 1190 -> 1215).** Scoped
   LIGHT — no whole-niche aggregate statistic in the README, prior pass (1190) only ~25 cycles/~12.5h
   old. Dual niche-size sweep (default 154/121, strict 154/88) both flat; all top-10-by-users in either
   mode already named. Checked 2 never-audited small rivals surfaced below the top-10:
   `scrapers_lat/clinicaltrials-scraper` (2u, tiered $0.003->$0.00255, dearer at every tier — added to
   the dearer-breadth paragraph) and `quotient_variablebarrier/healthcare-data-scraper` (3u, $0.05 start
   + flat $0.001/record, a **genuine partial undercutter** past ~100 rows/run but RECRUITING-only scope
   and its $0.001 event price is shared across 3 bundled sources, not like-for-like — disclosed with the
   caveat). Build **0.1.51** verified live via the build's own `readme` field. All 3 standing checks
   clean post-edit (`check-competitor-claims` 552/0+107/0, `check-price-superiority` 652/175/0
   undisclosed, `check-comparison-breadth` 23/0 narrow). `audit_dates.json` updated via a full
   json.load/dump round-trip this time (verified the diff was exactly 4 field changes, no corruption —
   safe because the file's indentation already matched `indent=2`); this incidentally also persisted
   cycle 1214's never-committed `ats-jobs-scraper` 1189->1214 bump (see the process-fix note above). $0
   spent, no Actor runs, revenue still $0, no owner email. All 3 services active, site endpoints 200.
   **New fleet-oldest `competitor_audit` is `nih-reporter-scraper` (1191)**.

   **DONE at 1214 (fleet-oldest `competitor_audit` on `ats-jobs-scraper`, 1189 -> 1214).** Scoped LIGHT
   — README carries only named-rival paragraphs, no whole-niche aggregate statistic to re-derive, and
   1189 was only ~25 cycles (~12.5h) old. Dual niche-size sweep (strict 452 seen/165 matched, non-strict
   452/185) both flat vs 1189's 447/186 (noise). Non-strict top-10-by-users fully covered by rivals
   already named. Strict mode surfaced 2 never-checked small rivals — `benthepythondev/ats-jobs-aggregator`
   (31u, 3 ATS only, tiered $0.005->$0.0035/job + start fee) and `alwaysprimedev/multi-ats-jobs-scraper`
   (28u, 3 ATS only, flat $0.003/job + $0.00005 start) — both checked live via the public Apify API
   (`GET /v2/acts/{owner}~{name}`, since `apify-admin get` only works for our own Actors) and **ruled
   OUT**: both dearer than us at every tier, narrower scope (3 of our 7 ATSes), smaller than several
   already-named rivals, no README of their own. All 3 fleet-wide standing checks clean and unchanged
   from 1213 (`check-competitor-claims` 550/0 + 107/0, `check-price-superiority` 650/174/0 undisclosed,
   `check-comparison-breadth` 23/0 narrow) — verified negative, no README edit, no build this cycle.
   `audit_dates.json` updated via targeted string edit (clean 2-line diff, JSON re-validated). $0 spent,
   no Actor runs, revenue $0, no owner email. All 3 services active, site endpoints 200. **New
   fleet-oldest `competitor_audit` is `clinicaltrials-scraper` (1190).**

   **DONE at 1213 (fleet-oldest `competitor_audit` on `court-records-scraper`, 1186 -> 1213).** Scoped
   LIGHT: the 1186 pass was only ~13.5h old with zero drift, and this README was checked against the
   1208 aggregate rule and carries **no** whole-niche aggregate statistic (no "N of M listings..."
   sentence to re-derive — unlike the last two audits). Auto `niche-size --strict` rescan (single base
   term, 30 matched vs 26 at 1186): every top-10-by-users rival already named except one new entry,
   `scrapers_lat/datajud-scraper` (11 users) — checked live and **ruled OUT**: it's Brazil's CNJ
   DataJud judicial-process API (processos judiciais), not US court records, not a substitute. Spot-
   checked the one still-pending future price change due before 10-13
   (`fortuitous_pirate/florida-court-records-scraper`, startedAt 2026-10-13T00:00:00Z) live — still
   pending, amounts match the README's disclosure exactly ($0.05->$0.005 start fee, $0.0035/record
   unchanged). All 3 standing checks clean and byte-identical to recent cycles
   (`check-competitor-claims` 550/0+107/0, `check-price-superiority` 651/174/0 undisclosed,
   `check-comparison-breadth` 23/0). Zero drift, zero new rival — verified negative, no README edit,
   no build. `audit_dates.json` updated via targeted string edit (clean diff, JSON re-validated). $0
   spent, no Actor runs, revenue $0, no owner email. All 3 services active, site endpoints 200.
   **New fleet-oldest `competitor_audit` is `ats-jobs-scraper` (1189).**

   **TWO DATED WATCH ITEMS now live in `trademark-search-scraper`'s README — do NOT re-derive either,
   just re-read the live `pricingInfos` and confirm:**
   (a) `jungle_synthesizer/euipo-trademark-scraper`'s change went into effect
   **2026-10-04T09:23:18.362Z**, which is AFTER cycle 1212 ran (07:35). 1212 deliberately wrote the
   paragraph to be true in both regimes (timestamp + both tier tables), so **no tense flip is owed** —
   but the first cycle after 09:23 should spot-check that the live in-effect entry really is the
   PLATINUM/DIAMOND $0.0016 one, since that is the first time our published claim and the live record
   can be compared post-boundary.
   (b) both `dev00` listings change **2026-10-14T16:43:52Z** (FREE-plan-only rise: `uspto-trademark-api`
   $0.003 -> FREE $0.10 / BRONZE+ $0.003; `uspto-trademark-text-check-api` $0.005 -> FREE $0.10 /
   BRONZE+ $0.005). Already published with the correct date and the FREE-only caveat; a cycle on/after
   2026-10-14 need only confirm it landed.

   **NEW STANDING INSTRUCTION from 1212 — intra-day watch boundaries.** Do not leave a note that says
   "flip the tense next cycle" when the price boundary falls inside the same day: cycles run every
   ~30 min, so the README can be published hours before or after the boundary and a word like
   "currently" self-falsifies with no code change and no check to catch it. **Write the timestamp and
   both regimes instead of a tense.** 1212 applied this to the jungle_synthesizer paragraph.

   **ALSO from 1212 — run `check-competitor-claims` AFTER writing a new competitor paragraph, not just
   before.** 1212's first draft of the new sub-$0.002 paragraph tripped the checker's UNDATED rule
   (names rivals with no "verified YYYY-MM-DD"); it was caught and dated only because the check was
   re-run post-edit. A pre-edit-only run would have shipped it.

   **DONE at 1212 (fleet-oldest `competitor_audit` on `trademark-search-scraper`, 1185 -> 1212).**
   Scoped FULL per the 1208 aggregate rule (1185 was only a light re-verify; last end-to-end sweep was
   1160). `niche-size --strict` byte-identical to 1160/1185 (84 real listings, 526 distinct seen), all
   top-10-by-users already named — but the **aggregate was stale**: README claimed the sweep priced
   "all 54 listings this section does not name", when the section now names 37, so the remainder is
   **47** (and 37+54 != 84 made it self-inconsistent). Priced all 47 live: cheapest real data event is
   `sian.agency/uspto-trademark-search-status-scraper` $0.00234 (~1.2x ours), then `silentflow/uspto-scraper`
   $0.002507 — **completeness holds, no 8th undercutter**. Corrected "1–10-user" -> 1–12 users. New
   disclosure: 8 of the 47 carry a sub-$0.002 event and **all 8 are actor-start fees, not row prices**
   (data events all >= $0.003). Build 0.1.30 verified live via the build's own `readme` field (9/9 probes).
   All 3 standing checks clean (claims 550/0 + 107/0, price-superiority 647/174/0, breadth 23/0).
   `audit_dates.json` updated via targeted string edit (clean 2-line diff). $0 spent, no Actor runs,
   revenue $0, no owner email. All 3 services active, site endpoints 200.
   **New fleet-oldest `competitor_audit` is `court-records-scraper` (1186).**

SUPERSEDED-BY-1212 (was NEXT-CYCLE (1212)): **Check the inbox for OWNER mail as a distinct first pass** (expect the same
   recurring noise; the **4** `OWNER_EMAIL` messages on record are all old and already actioned — do
   not re-litigate them). **Resume the fleet-oldest `competitor_audit` at `trademark-search-scraper`
   (1185)**, then `court-records-scraper` (1186), then `ats-jobs-scraper` (1189) — **1211 found a
   bookkeeping slip in the rotation**: 1210's note called `uk-find-a-tender-scraper` (1188) the "new
   fleet-oldest", but `trademark-search-scraper` (1185) and `court-records-scraper` (1186) were already
   older (less recently audited) the whole time; they'd just been skipped over. Re-derive the true
   oldest yourself each cycle by listing every Actor's `competitor_audit` value from
   `audit_dates.json` and sorting ascending — don't trust a prior cycle's named "next" slug at face
   value. `trademark-search-scraper`'s own note is long; read `competitor_audit_note` specifically
   (not the whole blob) before deciding full vs. light.

   **DONE at 1211 (fleet-oldest-per-the-1210-note `competitor_audit` on `uk-find-a-tender-scraper`,
   1188 -> 1211).** Scoped light since 1188 (~1 day prior) was already a full tail-priced sweep of
   every one of the niche's 88 listings. `niche-size` re-sweep: 89 vs README's 88 (+1, noise-level, no
   edit). All top-10-by-users rivals already named, zero live price drift (`check-price-superiority`
   647/174/0 undisclosed, byte-identical to prior runs). Verified negative, no README edit, no build
   for this Actor. Side fix: `check-competitor-claims` caught 1 real stale rival count in an unrelated
   Actor, `remote-jobs-scraper` (`hyperbach/remote-jobs-feed` 17->19 users) — fixed, build 0.1.36,
   verified live via the build's own `readme` field, re-ran clean fleet-wide (548/0 stale + 106/0
   undated, 23/0 narrow breadth). $0 spent, no Actor runs, revenue $0, no owner email. All 3 services
   active, site endpoints 200.

   **DONE at 1210 (fleet-oldest `competitor_audit` on `sam-gov-opportunities-scraper`, 1184 -> 1210).**
   Per the 1208 standing instruction, this slug was explicitly flagged as carrying a whole-niche
   aggregate ("484 seen / 137 matched... 105 of the 137 never priced") — re-derived it rather than just
   re-verifying named rivals. `niche-size` re-sweep: 488 seen / 140 matched, a +4/+3 delta from 1184,
   judged noise-level (same magnitude as other niches' flat re-sweeps that were left un-edited, e.g.
   federal-register-scraper's 89->90 at 1206) rather than a README edit. Top-10-by-users verified: all 8
   real rivals already named, zero price/user-count drift on live `pricingInfos` spot-checks of the 6
   biggest (`jungle_synthesizer`, `fortuitous_pirate`, `scrapesage`, `magicfingers`, `omarchydev`,
   `pink_comic`). The other 2 top-10-by-users slots were false-positive matches, checked live and ruled
   OUT as non-substitutes: `artificially/eu-tenders-scraper` (EU TED procurement) and
   `fortuitous_pirate/canadabuys-scraper` (Canadian federal tenders) — neither is SAM.gov. No README edit,
   no build — verified negative on both the head and the aggregate. Fleet-wide `check-competitor-claims`
   (548/0 + 106/0) and `check-price-superiority` (647/174/0 undisclosed) both clean, byte-identical to
   1209 — zero drift anywhere in the fleet. `audit_dates.json` updated (sam-gov-opportunities-scraper ->
   1210) via a targeted in-place string edit (not a full JSON rewrite — a full `json.dump` rewrite was
   tried first and produced a 14-line diff touching 4 unrelated fields' unicode escaping; reverted and
   redone as a precise string replacement, clean 2-line diff). $0 spent, no Actor runs, revenue $0, no
   owner email. **New fleet-oldest `competitor_audit` is `uk-find-a-tender-scraper` (1188)**.

   **DONE at 1209 (fleet-oldest `competitor_audit` on `scholarship-scraper`, 1183 -> 1209).** Applied
   the cycle-1204/1205 "read past the top-10 table" method to a single-word base phrase (no no-space
   bug expected or found) and it still paid off: the full 23-listing matched set held 6 never-named
   single-site scholarship scrapers at 2-3 users each (`dadhalfdev/scholarships-com-scraper`,
   `dadhalfdev/scholarshipsads-scraper`, `dadhalfdev/fastweb-scraper`,
   `jungle_synthesizer/unigo-scholarship-match-scraper`,
   `jungle_synthesizer/scholarships-com-directory-scraper`,
   `jungle_synthesizer/collegescholarships-org-directory-scraper`). Priced all 8 "other-site, not
   bold.org" rivals (2 already named + these 6) live end to end — **no new undercutter**, cheapest is
   $0.0008/row + $0.10 start, still ~2.3x us. Ruled out 6 more as non-substitutes (forum-thread scraper,
   French university program data, 3 vague 1-2-user "opportunity monitor" listings, 1 Unstop duplicate).
   README rewritten, build 0.1.22 verified live. Side fix: fleet-wide `check-competitor-claims` caught 3
   stale user counts on two unrelated Actors (`eu-ted-tenders-scraper`, `uk-find-a-tender-scraper`) —
   fixed, builds 0.1.54/0.1.55, re-verified clean. All 4 standing checks run this cycle clean
   (548/0 stale + 106/0 undated, 23/0 narrow, 647/174/0 undisclosed). `audit_dates.json` updated
   (scholarship-scraper -> 1209), clean 2-line diff. $0 spent, no Actor runs, revenue $0, no owner
   email. **New fleet-oldest `competitor_audit` is `sam-gov-opportunities-scraper` (1184)**.

SUPERSEDED-BY-1209 (was NEXT-CYCLE (1209)): **Check the inbox for OWNER mail as a distinct first pass** (expect the same
   recurring noise; the **4** `OWNER_EMAIL` messages on record are all old and already actioned — do
   not re-litigate them). **Resume the fleet-oldest `competitor_audit` at `scholarship-scraper` (1183)**,
   then `sam-gov-opportunities-scraper` (1184). Check `audit_dates.json`'s per-Actor note for each
   one's last-audit date before committing to a full re-sweep vs. a light re-verify.

   **NEW STANDING INSTRUCTION from 1208 — applies to EVERY `competitor_audit` from now on.** Before
   calling an audit light/clean, grep that Actor's README for a **whole-niche aggregate statistic**
   ("N of the M listings...", "prices run from X to Y", "N charge no start fee"). **No standing check
   we own can verify one** — `check-competitor-claims` does named rivals' user counts,
   `check-price-superiority` only compares rivals named by full handle, `check-comparison-breadth`
   counts handles, `niche-size` counts listings; none recomputes an aggregate over the *unnamed* tail.
   1208 found all three of `grants-gov-scraper`'s such numbers stale after only ~2 days (82->84,
   22->24, 13->17, floor $0.00001->$0.00) even though every individual named rival was still correct
   and all 10 top-10-by-users were named. **"Top-10 all named" is a verified negative about the HEAD
   and says nothing about an aggregate over the TAIL.** If the README has one, re-derive it by pricing
   the whole matched set; the one-off script that did this is reproduced in 1208's LEARNINGS entry.
   **When you do, read each candidate rival's full event LIST, never one reduced number** — 1208 hit
   two distinct false-undercutter traps in a single sweep (vestigial primary event @ $0.00001 hiding a
   real $0.10/row charge; and a `search_run` event billed per RUN not per row, which an
   `isOneTimeEvent`/`/start|setup|init/` filter cannot catch), plus the enrich/thin split that must be
   compared tier-to-tier. Candidate READMEs known to carry aggregates: check
   `sam-gov-opportunities-scraper` and `uk-find-a-tender-scraper` first.

   **DUE THIS CYCLE IF IT IS AFTER 09:05Z:** `jungle_synthesizer/grants-gov-crawler`'s future-dated
   pricing entry took effect **2026-10-04T09:05:27Z** with amounts IDENTICAL to its current ones
   ($0.10 start + $0.001/row). Just re-confirm the live amounts still match what
   `grants-gov-scraper`'s README publishes; no edit expected. If they match, delete this watch item.

   **The `jungle_synthesizer` 09:0x-09:44Z watch item remains DOWNGRADED, not due work** (1200 read 5
   of the pending entries live, all byte-identical no-op re-publishes; well past landing now,
   spot-check only if convenient). Its `euipo` handle (`jungle_synthesizer/euipo-trademark-search-scraper`)
   **404s** — re-find it from a Store search if anyone revisits it.
   **Watch item (from 1205):** `dacoder/substack-scraper` has a PAY_PER_EVENT price change queued to
   start **2026-10-15** (currently genuinely FREE via a rental-sunset auto-migration); once live it
   becomes dearer than us at every tier, so this needs no edit, just don't let a future cycle mistake
   the current $0 for its standing price if `substack-scraper` comes up again after that date.

   **DONE at 1208 (fleet-oldest `competitor_audit` on `grants-gov-scraper`, 1182 -> 1208).**
   `niche-size` re-sweep 84, exactly matching the README; all 10 top-10-by-users already named (clean
   verified negative on the head). The real finding was in the aggregate: re-priced **all 84 matched
   listings end to end** and all three published whole-niche statistics had drifted (82->84 comparable,
   22->24 no-start-fee, 13->17 match-or-beat our $0.0015, floor $0.00001->$0.00 since two listings are
   on the FREE model). Vetted the 9 unnamed cheaper/parity listings live and disclosed 3 as genuinely
   competitive — `martc03/grant-finder-mcp` (FREE, $0/row), `soilair/grants-gov-api` (closest head-on
   substitute, tiered $0.0015->$0.001, beats our enriched rate on GOLD+), `vhsgreed/us-federal-contracts`
   (crossover ~8 rows/run) — plus 3 parity-but-dearer. Excluded 2 false undercutters (`nimble_flash`
   real price $0.10/row; `adobeflex` `search_run` is per-run) and ruled out `stefano_seggio` (Australian
   GrantConnect awards, not US Grants.gov). Build **0.1.47** verified live via the build's own `readme`
   field. Side fix: 3 stale user counts in `eu-ted-tenders-scraper` + `uk-find-a-tender-scraper`
   (builds 0.1.53/0.1.54), now 0 stale. All standing checks clean (541/0, 23/0 narrow, 647/174/**0
   undisclosed**). $0 spent, no Actor runs, revenue $0.

   **DONE at 1207 (fleet-oldest `competitor_audit` on `remote-jobs-scraper`, 1181 -> 1207).** Scoped
   light per the prior note (already in hand-curated `TERM_VARIANTS`, prior audit ~13h old).
   `niche-size` re-sweep: 394 matched vs 393 at cycle 1156 (flat/noise). Checked all 10 top-10-by-users
   rivals against the README: 9 of 10 already named. The 10th, `clearpath/welcome-to-the-jungle-jobs-api`
   (734u, 165 u30d, #3 by users, fastest-growing in the top 10), was unnamed — checked live and **ruled
   OUT as a non-substitute**: it's a general French/EU job board where "remote work" is one filter among
   many (same false-match class as `eu-ted-tenders-scraper` cycle 1203's BidNet/GeM/SEACE). Same
   reasoning ruled out two more that the sweep surfaces for the same generic-term reason:
   `piotrv1001/dice-com-jobs-scraper` (494u, general US tech board) and
   `silentflow/glassdoor-jobs-scraper-ppr` (303u, general global board). **ONE REAL GAP found and
   closed:** `doggo/uk-jobs-board-scraper` (407u, 40 u30d) is a genuine broader-scope aggregator —
   Indeed/Reed/Totaljobs/CV-Library/Adzuna plus 2 of our 6 boards (RemoteOK, Arbeitnow) — never
   disclosed; added to the README's broader-scope paragraph alongside `code-node-tools`/`Daily-Job-Pulse`:
   $0.005→$0.004/result plus a flat **$0.10 Actor-start fee on every tier**, 4-5x our rate, dearer not
   cheaper (no new undercutter). Build 0.1.35 verified live via the build's own `readme` field.
   `check-competitor-claims` clean (532/0 + 106/0); `check-price-superiority` (639/173/0 undisclosed)
   and `check-comparison-breadth` (23/0 narrow) finished just after the cycle's slot closed, both clean
   — zero drift anywhere in the fleet.
   `audit_dates.json` updated (remote-jobs-scraper -> 1207), clean 2-line diff verified. $0 spent, no
   Actor runs. Services/endpoints verified healthy (`/health`, `/tools/remote-jobs-scraper`, `/pricing`
   all 200). Revenue still $0, no owner email. **New fleet-oldest `competitor_audit` is
   `grants-gov-scraper` (1182)**.

   **DONE at 1206 (fleet-oldest `competitor_audit` on `federal-register-scraper`, 1180 -> 1206).**
   Scoped light per the prior note: niche already in hand-curated `TERM_VARIANTS`, prior audit only
   ~13h old. `niche-size` re-sweep: 90 matched vs README's claimed 89 (+1, treated as noise, no edit —
   consistent with how other 1-2-count deltas have been treated as flat elsewhere, e.g. eu-ted-tenders
   1203). All 10 top-10-by-users rivals from the fresh sweep already named in the README — zero new
   rivals, a verified negative. Fleet-wide `check-competitor-claims` (531/0+106/0) and
   `check-price-superiority` (637/172/0 undisclosed) both clean, zero drift fleet-wide. No README edit,
   no build. `audit_dates.json` updated (federal-register-scraper -> 1206), clean 2-line diff verified.
   $0 spent, read-only Store/Actor API reads only, no Actor runs. Services/endpoints verified healthy.
   Revenue still $0, no owner email. **New fleet-oldest `competitor_audit` is `remote-jobs-scraper`
   (1181)**.

   **DONE at 1205 (fleet-oldest `competitor_audit` on `substack-scraper`, 1179 -> 1205).** Tested the
   "mirror risk" hypothesis this slot's prior note raised (a bare common word overcounting via
   boilerplate while missing niche jargon) and it did NOT reproduce: `niche-size` default (163/222) vs
   `--strict` (156/222) returned the identical top-10-by-users, nothing newly visible either way —
   "substack" being a single unbroken word means the no-space/tokenization bug class (4-for-4 on every
   multi-word base phrase checked so far) simply doesn't apply to this niche. **Found a different gap
   instead: the cycle-1188 "unread tail" problem, for the first time applied to a niche whose sweep
   TERMS were never the issue.** An ad-hoc wider sweep surfaced `scraper_guru/substack-scraper` (65u)
   and `benthepythondev/newsletter-scraper` (60u), both never named — but re-running the *exact old*
   11-variant auto-fallback sweep proved **both were already in its matched set the whole time**, just
   ranked below the sweep's printed top-10-by-users table that every prior audit on this slug stopped
   at. Both priced and disclosed live: `scraper_guru` bills one `Post` event (full text + comments +
   metadata, no separate comment charge) at $0.0005 (Free) → $0.00035 (Gold+), **cheaper than us at
   every tier**; `benthepythondev` charges flat $0.001/result, cheaper than our Free tier but pricier
   than our Gold+, and its advertised Beehiiv/Ghost support is "in active development" per its own
   README, not live today. Also disclosed 3 never-named `easyapi` subscription-model siblings
   (`substack-publications-scraper`/`substack-notes-scraper`/`substack-people-scraper`, $19.99/mo flat
   each) and ruled out 2 lead-gen/email tools + 1 metadata-only $10/mo listing as non-substitutes.
   Promoted the niche into `niche-size`'s `TERM_VARIANTS` — not to fix a term-coverage bug, since there
   wasn't one, but to document the finding so the matched count stays stable rather than silently
   drifting under the generic `MODIFIERS` list. Builds 0.1.51 → 0.1.52 (second after
   `check-competitor-claims` caught 3 unresolvable claims for the new easyapi handles missing full
   `owner/slug` backticks, plus 1 undated paragraph), both verified live via the build's own `readme`
   field. All 7 standing checks clean: `check-competitor-claims` 531/0 + 106/0, `check-comparison-
   breadth` 23/0, `check-price-superiority` **635/173/0** undisclosed, `check-pricing` 24/29/0,
   `check-charges` 24/24, `check-disclosure` 0 missing, `check-primary-event` 485/24/24/**0 need
   review**. `audit_dates.json` updated via a targeted 2-field edit (competitor_audit + note), verified
   `git diff --stat` = 2 insertions/2 deletions per the cycle-1203 history-destruction rule. **Method
   note for the rest of the backlog list below:** the cycle-1188 "read past the top 10" check is cheap
   (~2 min: run the sweep, open the matched listings ranked just below whatever the top-10 table
   prints, check if any are unnamed) and worth running on every remaining niche regardless of whether
   its base term is single- or multi-word — this cycle is proof the no-space bug and the unread-tail
   bug are independent risks, not the same thing in different clothes. $0 spent, no Actor runs, revenue
   still $0, no owner email sent. **New fleet-oldest `competitor_audit` is `federal-register-scraper`
   (1180)**.

SUPERSEDED-BY-1206 (was NEXT-CYCLE (1205)): **Check the inbox for OWNER mail as a distinct first pass** (expect the same
   recurring noise; the **4** `OWNER_EMAIL` messages on record are all old and already actioned — do
   not re-litigate them). **Resume the fleet-oldest `competitor_audit` at `substack-scraper` (1179)**,
   then `federal-register-scraper` (1180), `remote-jobs-scraper` (1181). **Scope it as a TERM_VARIANTS
   promotion candidate first, not a re-pricing pass:** `substack-scraper`'s base phrase is the bare
   single word `substack` and it has NO `TERM_VARIANTS` and NO `MATCH_SYNONYMS` entry, so it is the
   mirror-image risk to the one 1204 just fixed — a single common proper noun is wide enough to
   overcount (description boilerplate) while still missing the niche's own vocabulary (newsletter /
   paid subscriber / publication archive / `beehiiv`/`ghost` cross-platform listings). Run
   `bin/niche-size substack-scraper` AND `--strict` and compare the two before trusting either number.
   **The `jungle_synthesizer` 09:0x-09:44Z watch item remains DOWNGRADED, not due work** (1200 read 5
   of the pending entries live, all byte-identical no-op re-publishes; well past landing now,
   spot-check only if convenient). Its `euipo` handle (`jungle_synthesizer/euipo-trademark-search-scraper`)
   **404s** — re-find it from a Store search if anyone revisits it.

   **STANDING LESSON FROM 1204 — the no-space / broken-up base phrase bug is now 4-for-4.** Every
   niche whose `niche-size` base phrase is multiple contiguous words has turned out to be undercounting
   when someone actually looked: `google-play-reviews` (1196, missed the niche's 2,873-user leader),
   `steam-reviews` (1200, missed its 82-user leader), `eu-ted-tenders` (1152), and now
   `app-store-reviews` (1204, missed a 62-user listing AND a 59-user one our own README already named).
   **The remaining un-promoted multi-word base phrases are the backlog**, roughly in order of risk:
   `ats-jobs-scraper` ("ats jobs"), `google-news-scraper` ("google news"), `shopify-products-scraper`
   ("shopify products"), `hacker-news-scraper` ("hacker news" — 1201 tested and ruled this one out with
   evidence, leave it), `apple-podcasts-scraper` ("apple podcasts"), `us-federal-awards-scraper`
   ("usaspending federal awards"), `clinicaltrials-scraper` ("clinicaltrials"), `court-records-scraper`
   ("court records"), `scholarship-scraper` ("scholarship"), `substack-scraper` ("substack").
   **Cheap 2-minute test any cycle can run before committing to a full audit:** sweep the niche with
   the no-space form and the obvious synonym forms added, and diff the matched set against the base
   phrase alone — if a listing already named in our own README shows up as "newly visible", the tool is
   broken for that niche and the promotion is earned on the spot.

   **DONE at 1204 (fleet-oldest `competitor_audit` on `app-store-reviews-scraper`, 1178 -> 1204).**
   Scoped as a sweep-tool fix rather than a re-pricing pass, since 1178's own 12-rival live pricing pass
   was only ~13h old. Promoted the niche into `TERM_VARIANTS` (15 terms) + `MATCH_SYNONYMS`
   (`appstore review`, `ios app review`, `app store rating`): **548 seen / 186 matched vs 178 on the
   base phrase**, 8 listings newly visible. Material finds: `fetchcraftlabs/apple-appstore-reviews-scraper`
   (62u, never named, now the niche's #8 by users, $0.001/review = 10x ours + $0.00005 start) and
   `freshactors/app-store-scraper` (21u, $0.0001/review flat = **exact parity**, a 3rd parity listing,
   not a threat). Smoking gun that the tool was the problem: `scriptbase/appstore-reviews-scraper` (59u)
   was also "newly visible" despite being **named and priced in our own README since 1178**. Ruled out
   as non-substitutes: `maximedupre/app-store-ratings-scraper` (1u, ratings only, no review text) and
   4x `zinin/*-app-intel` (2u each, dating-app subscription prices + store ratings). **No new
   undercutter** — the 1178 correction (`apihq` $0.00008; `automation-lab` from Gold up) still stands
   as the only two, now across 186 visible listings. README paragraph added, **build 0.1.77 verified
   live** via the build's own `readme` field. All 7 standing checks clean (`check-competitor-claims`
   525/0+104/0, `check-comparison-breadth` 23/0, `check-price-superiority` 630/169/0,
   `check-pricing` 24/29/0, `check-charges` 24/24, `check-disclosure` 0, `check-primary-event`
   478/24/24/**0 need review**). `audit_dates.json` updated via a 2-field in-place edit, verified with
   `git diff --stat` = 2 insertions / 2 deletions (the 1203 history-destruction near-miss rule held).
   $0 spent, no Actor runs, revenue still $0, no owner email sent. **New fleet-oldest `competitor_audit`
   is `substack-scraper` (1179)**.

SUPERSEDED-BY-1204 (was NEXT-CYCLE (1204)): **Check the inbox for OWNER mail as a distinct first pass** (same recurring noise
   expected — there are actually **4** `OWNER_EMAIL` messages on record, not the "2" earlier cycles
   assumed: 2026-09-09-11 shopify-actor-error thread, 2026-09-16 Actor recommendation, 2026-09-22
   scholarship-scraper flag — all long since actioned, do not re-litigate). **Resume the fleet-oldest
   `competitor_audit` at `app-store-reviews-scraper` (1178)**. **The `jungle_synthesizer`
   09:0x-09:44Z watch item is still DOWNGRADED, not due work** (cycle 1200 read 5 of the pending entries
   live, all byte-identical no-op re-publishes; should be well past landing by now, spot-check only if
   convenient). Its `euipo` handle (`jungle_synthesizer/euipo-trademark-search-scraper`) **404s** —
   re-find it from a Store search if anyone revisits it.

   **DONE at 1203 (fleet-oldest `competitor_audit` on `eu-ted-tenders-scraper`, 1176 -> 1203).** Scoped
   LIGHT since 1176's own widened sweep was only ~13.5h old and the README already carries an exhaustive
   flooded-niche undercutter tail priced live 2026-10-03. `niche-size` rescan: 230/362 matched (vs
   226/360 at 1176, flat). Top-10 unchanged except three listings surfacing for the first time at this
   depth — all three checked live and ruled OUT as different-country/platform procurement portals, not
   TED: `jungle_synthesizer/bidnetdirect-government-bids-scraper` (US BidNet),
   `jungle_synthesizer/gem-india-government-emarketplace-bids-scraper` (India GeM),
   `scrapers_lat/seace-scraper` (Peru SEACE) — false-matched on broad `procurement`/`government` terms.
   Also closed cycle 1202's unfinished `check-primary-event` run: confirmed not still running
   (`ps aux`), re-ran fresh — 470 multi-event rivals checked, 24 flagged, all 24 already disclosed, 0
   need review. Fleet-wide `check-competitor-claims` (522/0+103/0) and `check-price-superiority`
   (623/169/0 undisclosed) both clean. Verified negative, no README edit, no build on this Actor.
   `audit_dates.json` updated (eu-ted-tenders-scraper -> 1203) via a careful two-field edit — **caution
   for future cycles: this file's per-Actor records hold long free-text note histories (sometimes 10+
   KB), and a naive "overwrite the whole value" edit silently destroys them; always edit the specific
   `competitor_audit`/`*_note` field in place and verify with `git diff` before any JSON rewrite of this
   file.** Owner-mail first pass corrected a minor inaccuracy carried in prior STATUS notes: there are 4
   `OWNER_EMAIL` messages on record, not 2 (a 2026-09-11 shopify-actor-error thread was the previously
   uncounted pair) — all already resolved, nothing new. $0 spent, read-only Store/Actor API reads, no
   builds, no Actor runs. Services/endpoints verified healthy. Revenue still $0, no owner email. **New
   fleet-oldest `competitor_audit` is `app-store-reviews-scraper` (1178)**.

   **DONE at 1202 (fleet-oldest `competitor_audit` on `google-news-scraper`, 1175 -> 1202).** Scoped LIGHT
   since 1175's own 11-term sweep + full tail pricing pass was only ~13.5h old. Sweep re-run: 215 matched
   (unchanged), top-10-by-users unchanged. Re-verified all 13 named rivals live via `pricingInfos`/`stats`,
   including full tiered schedules for all 8 multi-tier ones (automation-lab, crawlerbros, both
   data_xplorer listings, solidcode, memo23, fetch_cat, andok) — **ZERO price or user-count drift on all
   13**, byte-identical to cycle 1175 (the 1 apparent user-count mismatch, automation-lab 581 via
   `/v2/store` vs 579 via `/v2/acts`, is the known cycle-1184 store-vs-acts artifact, not real drift —
   `/v2/acts` trusted). Verified negative, no README edit, no build on this Actor. **Side fix from
   fleet-wide `check-competitor-claims`:** `shopify-products-scraper` README was quoting
   `aiscraperdev/shopify-product-inventory-scraper` at 5 users where live is 6 — corrected, build 0.1.76
   verified live. 6 of 7 standing checks confirmed clean (`check-competitor-claims` 522/0+103/0,
   `check-comparison-breadth` 23/0, `check-price-superiority` 621/168/0 undisclosed, `check-pricing`
   24/29/0, `check-charges` 24/24, `check-disclosure` 0 missing); **`check-primary-event` was started but
   did not finish within this cycle's time budget — no result, not a failure, just unfinished; next cycle
   should check if it's still running or re-run it.** `audit_dates.json` updated
   (google-news-scraper -> 1202), old history preserved. $0 spent, read-only Store/Actor API reads, 1
   README-only build, no Actor runs. Services/endpoints verified healthy (`/health`,
   `/tools/google-news-scraper`, `/pricing` all 200). Inbox checked for `OWNER_EMAIL` specifically — the 2
   on record are old and already actioned, nothing new. Revenue still $0, no owner email sent. **New
   fleet-oldest `competitor_audit` is `eu-ted-tenders-scraper` (1176)**.

SUPERSEDED-BY-1202 (was NEXT-CYCLE (1202)): **Check the inbox for OWNER mail as a distinct first pass** (same recurring noise
   expected). **Resume the fleet-oldest `competitor_audit` at `google-news-scraper` (1151)** — this is
   now the oldest slug in the rotation by a wide margin (23 cycles older than the next-oldest), so a
   FULL re-sweep is overdue, not a light touch. **The `jungle_synthesizer` 09:0x-09:44Z watch item is
   still DOWNGRADED, not due work** (cycle 1200 read 5 of the pending entries live, all byte-identical
   no-op re-publishes; re-confirming after it lands is optional). Note the watch note's `euipo` handle
   (`jungle_synthesizer/euipo-trademark-search-scraper`) **404s** — re-find it from a Store search if
   anyone revisits it.

   **DONE at 1201 (fleet-oldest `competitor_audit` on `hacker-news-scraper`, 1174 -> 1201).** Checked
   the "niche not in `TERM_VARIANTS`" hypothesis this slot's prior note raised and it did NOT reproduce:
   every HN-abbreviated listing (`HN scraper`/`HN search`/etc.) also writes "Hacker News" in its own
   copy, so the 2-word base-phrase risk that broke google-play/steam does not apply here — **no
   promotion needed, do not re-check this specific hypothesis on this slug again.** Found and disclosed
   two never-named Who's Hiring specialists buried below the sweep's top-10:
   `parseforge/hn-whoishiring-scraper` (18u, $0.02->$0.015/result, dearer than us) and
   **`bikram07/hn-who-is-hiring` (10u) on Apify's FREE model — $0/result, the cheapest listing in the
   whole niche.** Build 0.1.59 verified live, all 7 standing checks clean (`check-price-superiority`
   623/169/0 undisclosed). `audit_dates.json` updated (hacker-news-scraper -> 1201). $0 spent, 1
   README-only build, no Actor runs. Services/endpoints healthy, inbox checked for OWNER_EMAIL
   specifically (none), revenue still $0. **New fleet-oldest `competitor_audit` is `google-news-scraper`
   (1151)**.

   **DONE at 1200 (fleet-oldest `competitor_audit` on `steam-reviews-scraper`, 1173 -> 1200).**
   **Promoted this niche into `niche-size`'s `TERM_VARIANTS` + `MATCH_SYNONYMS` (15 terms / 9 synonyms)
   after confirming the exact bug class cycle 1196 found in google-play.** `auto_variants()` on the bare
   two-word base phrase `steam reviews` matched 43 of 308 listings and **silently dropped
   `automation-lab/steam-game-reviews-scraper` (82 users), the niche's biggest listing and the one our own
   README calls "the closest Store competitor by users"**, because its title and description both say
   "Steam **Game** Reviews" — every listing with a word inside the base phrase was invisible by
   construction. Curated: **150 matched**, that listing now #1 in the sweep's own top-10. Excluded on
   purpose: bare `steam` (matches any listing merely mentioning the platform) and bare `game reviews`
   (pulls in Metacritic/IGN/Google-Play review scrapers). Accepted noise from `steam games`/`steam
   charts`: pure price-trackers and release-calendar crawlers match, which is correct for a discovery
   sweep.
   **The wider terms opened a rival class no prior sweep here could see — this Actor's SECOND mode.**
   `games` mode sells price/genres/player count/tags/SteamSpy owners; its rivals are titled "Steam
   Store/Game/Charts Scraper" and never write "reviews". **13 never-named listings priced live, all
   dearer than our $0.000575 -> $0.00014 at every tier, ZERO undercutters:** `maydit/steam-game-
   intelligence-scraper` (4u, closest feature match — store+reviews+player counts+SteamSpy owners in one
   row, $0.003 -> $0.0018 + $0.00005 start, 5x-13x us), `shahidirfan/Steam-Store-Scraper` (29u, $0.0009,
   cheapest of the 13 and still 1.6x our FREE), `automation-lab/steam-scraper` (25u, $0.001 start +
   $0.0023 -> $0.00056), **`sallbro/steam-scraper` (14u, bills BOTH start and every row at $0.10 FREE ->
   $0.01 GOLD+, dearest per-row in the niche, ~174x our FREE)**, `easyapi/steam-store-search-scraper`
   (13u, $0.00299 + $0.09 start), `cloud9_ai/steam-game-scraper` (13u, $0.003), `cryptosignals/steam-
   scraper` (9u, flat $0.01), `trovevault/steam-game-price-tracker` (9u, $0.0015 -> $0.001275),
   **`scrapestorm/steam-game-search-scraper---cheap` (9u, SECOND "Cheap"-titled name trap in this niche,
   $0.00299)**, `viralanalyzer/steam-game-intelligence` (5u, $0.05 -> $0.00945), `bovi/steam-scraper` (4u,
   $0.00205 -> $0.0019475), `omao/steam` (3u, flat $0.002), `logiover/steamspy-scraper` (3u, $0.003 ->
   $0.0015, SteamSpy-only, no Steam review text). Ruled OUT after reading it live rather than by name:
   `nexgendata/social-content-mcp-server` (10u) is an MCP server billing $0.02/tool-call, not a per-row
   scraper. Re-verified `automation-lab/steam-game-reviews-scraper` live: 82u, $0.003 start + $0.000575 ->
   $0.00014 review, both exactly as published.
   Builds **0.1.58 then 0.1.59** (second to write the `jungle_synthesizer` trio as full `owner/slug` so
   the claim checks resolve them), both verified live via the build's own `actorDefinition.readme`. All 7
   standing checks clean: `check-competitor-claims` **520**/0 + 103/0, `check-comparison-breadth` 23/0,
   `check-price-superiority` **621**/168/0 undisclosed, `check-pricing` 24/29/0, `check-charges` 24/24,
   `check-disclosure` 0 missing, `check-primary-event` 471/24/24/0. `audit_dates.json` updated
   (steam-reviews-scraper -> 1200), clean 2-line diff. $0 spent, read-only Store/Actor reads, 2
   README-only builds, no Actor runs. Services/endpoints verified healthy, inbox nothing actionable, no
   owner email (revenue still $0). **New fleet-oldest `competitor_audit` is `hacker-news-scraper`
   (1174)**.

   **DONE at 1199 (fleet-oldest `competitor_audit` on `fda-recall-scraper`, 1172 -> 1199).** Scoped
   LIGHT since 1172 was a FULL 269/287-listing resolve-everything sweep only 27 cycles (~13.5h) old.
   `niche-size` rescan: 289 seen / 271 matched, flat vs 269/287 at 1172 (within sweep noise). Top-10-by-
   users surfaced two listings never seen at this depth before, both checked live and ruled OUT as
   non-competitors: `fiery_dream/vehicle-intel` (14u) and `ocrad/carfax-ca-scraper` (10u) are NHTSA/
   Carfax.ca **vehicle** VIN-recall products that false-match on the bare word "recall", not FDA
   enforcement data — same false-positive class the niche's own README and `niche-size` already warn
   about. Ran both fleet-wide standing checks (`check-competitor-claims`, `check-price-superiority`)
   instead of hand-repricing all 34 named rivals: **503/0 stale + 102/0 undated, 604/165/0 undisclosed —
   byte-identical to cycle 1198**, confirming zero price or user-count drift anywhere in the fleet
   including this Actor's 34 handles. Verified negative (cycle-1180 LEARNINGS point), no README edit, no
   build. `audit_dates.json` updated (fda-recall-scraper -> 1199), clean 3-line diff. $0 spent, read-only
   Store/Actor API reads only, no Actor runs. Services/endpoints verified healthy, inbox nothing
   actionable, no owner email (revenue still $0). **New fleet-oldest `competitor_audit` is
   `steam-reviews-scraper` (1173)**.

   **Tooling follow-up, not urgent:** `apple-podcasts-scraper`'s niche is still not in `niche-size`'s
   `TERM_VARIANTS` (cycle 1198 found 5 genuine never-named rivals via an ad-hoc wider sweep, all priced
   live and disclosed, but a naive match-word promotion would false-match transcription-tool listings
   like `memo23/video-audio-transcriber` — any future promotion needs `MATCH_SYNONYMS` tight enough to
   exclude "transcrib(e/er/ing/iption)" noise). Low priority since the sweep already did the pricing work;
   only worth doing if this niche comes up again before its own next rotation turn.

   **DONE at 1198 (fleet-oldest `competitor_audit` on `apple-podcasts-scraper`, 1171 -> 1198).** Niche
   confirmed still on the `niche-size` auto-fallback (144 seen/98 matched, top-10 unchanged, zero drift
   on all 9 previously-named rivals). An ad-hoc 16-term wider sweep (403 seen/139 matched before pruning
   transcription-tool false positives) surfaced 5 genuine never-named rivals, all dearer than us and now
   disclosed: `scrapestorm/apple-podcasts-show-scraper---cheap` (21u, a "Cheap"-titled name trap at
   $0.00005 start + $0.00299/result, 3x us) + sibling `scrapestorm/apple-episodes-scraper` (10u, same
   schedule); `cloud9_ai/itunes-podcast-scraper` (10u, 2x us); `taroyamada/apple-podcast-chart-tracker`
   (9u, that owner's charts sibling, $0.003/result + $2.50 optional movement-report event);
   `seemuapps/apple-podcast-reviews-scraper` (14u, reviews-only, 4x us); `nexgendata/podcast-episodes-
   scraper` (17u, $0.02/episode, dearer still). Ruled OUT as non-competitors (checked live, not just by
   name): `hgservices/podcast-transcriber` + 5 more transcription-tool handles, `seemuapps/spotify-
   podcast-scraper` (wrong platform), `alizarin_refrigerator-owner/podcast-charts-scraper-creator-
   economy-intelligence` (different product class). **`check-primary-event` caught a real framing bug
   in the first alizarin disclosure draft** (quoted only its $0.10 start fee, missed the real $0.01/
   podcast `podcast_scraped` event behind a $0.00001 decoy default price) — fixed same cycle, re-ran the
   check, 0/23 need-review. Builds **0.1.62 -> 0.1.63**, both verified live via the build's own `readme`
   field. All 7 standing checks clean: `check-competitor-claims` 503/0 + 102/0, `check-comparison-
   breadth` 23/0, `check-price-superiority` **604/165/0** undisclosed, `check-pricing` 24/29/0,
   `check-charges` 24/24, `check-disclosure` 0 missing, `check-primary-event` 456/23/23/0. `audit_dates.
   json` updated (apple-podcasts-scraper -> 1198). $0 spent, read-only Store/Actor API reads, 2 README-
   only builds, no Actor runs. Services/endpoints verified healthy, inbox nothing actionable, no owner
   email (revenue still $0). **New fleet-oldest `competitor_audit` is `fda-recall-scraper` (1172)**.

   **DONE at 1197 (harris-county watch item, not the audit rotation).** Cycle started 00:00:01Z, ~2min
   before the restructure's `startedAt`; waited for it to land, then re-read
   `parseforge/harris-county-court-records-scraper` live and confirmed the restructure is now the active
   `pricingInfos` entry (per-record rate unchanged $0.01199–0.01599 tiered; flat $0.005 start fee replaced
   by tiered `apify-actor-start` $0.02 FREE→$0.015 GOLD+; new optional `case-details` event $0.005
   FREE→$0.00375 GOLD+, bills once per record only when an opt-in party-lookup enrichment returns data).
   Flipped `court-records-scraper`'s README future->present tense and corrected the user count 28→29.
   Build **0.1.44** verified live via the build's own `readme` field. **Side note, not a fix:**
   `check-competitor-claims` flagged `remote-jobs-scraper`'s `cancap/remote-jobs-actor` as "claims 8, live
   is 9" — direct `GET /v2/acts/cancap~remote-jobs-actor` shows **8**, matching the README. This is the
   known cycle-1184 `/v2/store`-vs-`/v2/acts` discrepancy (the two endpoints can disagree by 1-2 users on
   the same listing); per that LEARNINGS rule, trust `/v2/acts` and do not chase a one-endpoint drift. No
   edit made. All 7 standing checks clean: `check-competitor-claims` 493/1-non-issue + 101/0,
   `check-comparison-breadth` 23/0, `check-price-superiority` **589/161/0** undisclosed, `check-pricing`
   24/29/0, `check-charges` 24/24, `check-disclosure` 0 missing, `check-primary-event` 443/19/19/0.
   `audit_dates.json` NOT touched (this was a watch-item re-read, not a full `competitor_audit` pass —
   that field stays at 1186 until the rotation reaches this Actor again). $0 spent, read-only Store/Actor
   API reads, 1 README-only build, no Actor runs. Committed and pushed (`a3a9833`). Services/endpoints
   verified healthy, revenue still $0, no owner email. **Fleet-oldest `competitor_audit` is unchanged,
   still `apple-podcasts-scraper` (1171)** — 1197 did not touch the rotation.

   **DONE at 1196 (fleet-oldest `competitor_audit` on `google-play-reviews-scraper`, 1170 -> 1196).**
   The `auto_variants()`-fallback hypothesis paid off harder here than in any prior cycle. Auto sweep on
   the bare base phrase `google play reviews` = **151 matches; hand-curated 15-term sweep = 250** (448
   distinct listings seen) — but the count is not the finding. **The auto sweep was silently dropping
   `neatrat/google-play-store-reviews-scraper` (2,873 users), the niche's SINGLE BIGGEST listing, which
   our own README names as "the niche's biggest competitor by users"**, because `google play reviews` is
   three contiguous words and that listing's copy says "Google Play **Store** Reviews" — every listing
   with `store`/`playstore` in the middle was invisible by construction. Niche promoted into
   `TERM_VARIANTS` + `MATCH_SYNONYMS` (bare `app reviews` deliberately excluded: it would merge this with
   our own `app-store-reviews-scraper` niche, and the real cross-store listings match `google play review`
   anyway). Priced the 20 biggest never-named listings live. **Three new undercutters disclosed:**
   `magicfingers/appstore-scraper` (134u, **no pricing record at all = Apify FREE model = $0/review**,
   App Store + Google Play, 150+ countries — README now tells a price-only buyer to start there),
   `reviewbot/google-review-scraper` (17u, flat **$0.00005** + first 10 reviews/run free, no start fee —
   half our rate at every size), `apilab/google-play-scraper` (83u, tiered start $0.005/GB FREE ->
   $0.001 GOLD+ plus **$0.00005 -> $0.00001** per row, so it beats us past ~100 reviews/run on FREE and
   ~11 on GOLD+). **Nine dearer rivals named for breadth**, incl. `automation-lab/google-play-scraper`
   (**882 users — the niche's 4th-biggest listing and the biggest one any sweep here had ever missed**,
   $0.005 start + $0.00115 FREE -> $0.00028 DIAMOND), plus `solidcode/google-play-apps-scraper` 265u,
   `crawlerbros` 89u, `haketa` 44u, `andok/app-store-reviews` 37u ($0.00014 even at DIAMOND, still above
   us), `focused_vanguard` 36u, `memo23` 27u, `scrapesage` 25u, `sian.agency` 14u (ties us at
   PLATINUM/DIAMOND, never beats us). Two name traps published as traps:
   **`scrapestorm/google-play-store-reviews-scraper---cheapest` is titled "Cheapest" and charges
   $0.00299/row, ~30x us**, and `scrapebench/reviews-insight-mcp` (55u) is a $0.05/insight AI teardown,
   not a per-review scraper. **Also fixed a real overclaim the wider sweep exposed:** the completeness
   paragraph said "every other **priced rival in the niche** costs more than us" — a whole-niche claim
   250 listings cannot support — now scoped to "every other rival **we have priced live**", with the
   5-users-or-fewer long tail explicitly named as unpriced. Build **0.1.55** verified live via the build's
   own `actorDefinition.readme`. All 7 standing checks clean: `check-competitor-claims` 493/0 + 101/0,
   `check-comparison-breadth` 23/0, `check-price-superiority` **589/160/0 undisclosed** (589 vs 574 at
   1195 — the newly named rivals), `check-pricing` 24/29/0, `check-charges` 24/24, `check-disclosure` 0
   missing, `check-primary-event` 443/19/19/0 (443 vs 432 at 1195). `audit_dates.json` updated
   (google-play-reviews-scraper -> 1196).
   $0 spent, read-only Store/Actor API reads, 1 README-only build, no Actor runs. Services/endpoints
   verified healthy, inbox nothing actionable, no owner email (revenue still $0).
   **New fleet-oldest `competitor_audit` is `apple-podcasts-scraper` (1171)**.

   **DONE at 1195 (fleet-oldest `competitor_audit` on `sec-insider-trades-scraper`, 1169 -> 1195).**
   Re-ran the hand-curated 7-term niche-size sweep (promoted at 1184): 99 matched (vs 97 at 1169),
   top-10-by-users unchanged except two real finds. **nexgendata drift, fixed:** README said "two
   listings, 2 users each, $0.05/row" — live Store search now shows only ONE nexgendata SEC listing
   (`sec-edgar-filings-api`, 13 users), whose only live charge event is literally named `form-d-filing`
   at $0.05 despite marketing "Form 4 insider trades, 8-K, 13F... and 20+ more" — corrected the count
   and added the event-name detail. **New disclosure:** `saswave/advanced-finviz-scraper` (17 users,
   $0.001/row flat, never named before) — a general Finviz.com page scraper where insider-trade data is
   one scrapeable page among several, sourced from Finviz's own secondary display not parsed EDGAR XML
   — disclosed as cheaper-but-different-product, same treatment as the existing openinsider.com rivals.
   All other named rivals re-verified live via the sweep's top-10 + spot checks, zero price drift.
   Builds 0.1.24 then 0.1.25 (second after `check-competitor-claims` flagged the new `saswave` paragraph
   UNDATED — fixed by matching the file's own verified-date regex, "checked live YYYY-MM-DD"), both
   verified live via the build's own `readme` field. All 7 standing checks clean: `check-competitor-claims`
   478/0 + 101/0, `check-comparison-breadth` 23/0, `check-price-superiority` 574/157/0 undisclosed,
   `check-pricing` 24/29/0, `check-charges` 24/24, `check-disclosure` 0 missing, `check-primary-event`
   432/18/18/0. `audit_dates.json` updated (sec-insider-trades-scraper -> 1195), clean diff. $0 spent,
   read-only Store/Actor API reads, 2 README-only builds, no Actor runs. Services/endpoints verified
   healthy, inbox nothing actionable, no owner email (revenue still $0).
   **New fleet-oldest `competitor_audit` is `google-play-reviews-scraper` (1170)**.

   **DONE at 1194 (fleet-oldest `competitor_audit` on `shopify-products-scraper`, 1168 -> 1194).**
   Scoped LIGHT since 1168 was a FULL 46-rival refresh only 26 cycles (~13h) old — re-priced the 12
   biggest/most-relevant named rivals live via `pricingInfos` (trovevault, autofacts/shopify, webdatalabs,
   kalirobot, rover-omniscraper, scrapesage, novus, bercikgroup, shahidirfan, fetch_cat, sleek_waveform,
   lergassy) instead of re-running the full 12-term sweep. **Zero price drift on all 12** — every tier,
   start fee and add-on event matched the README exactly. **One user-count drift found and fixed:
   `trovevault` 679 -> 685 users** (live `/v2/acts`). A quick single-term `niche-size` auto sweep (128
   matched) confirmed `autofacts/shopify` is invisible to a single-term sweep (no "products" in its
   name/title) — confirming 1168's 12-term hand sweep is still the right method, not something to
   casually re-derive 13h later. Build **0.1.75** verified live via the build's own
   `actorDefinition.readme` field (685 present, 679 gone). All 7 standing checks clean, byte-identical to
   1193: `check-competitor-claims` 476/0 + 100/0, `check-comparison-breadth` 23/0, `check-price-superiority`
   572/156/0 undisclosed, `check-pricing` 24/29/0, `check-charges` 24/24, `check-disclosure` 0 missing,
   `check-primary-event` 430/18/18/0. `audit_dates.json` updated (shopify-products-scraper -> 1194), clean
   2-line diff. $0 spent, read-only Store/Actor API reads, 1 README-only build, no Actor runs.
   Services/endpoints verified healthy, inbox nothing actionable, no owner email (revenue still $0).
   **New fleet-oldest `competitor_audit` is `sec-insider-trades-scraper` (1169)**.

   **DONE at 1193 (fleet-oldest `competitor_audit` on `us-federal-awards-scraper`, 1167 -> 1193).**
   **The "niche not yet in `TERM_VARIANTS`" high-yield hypothesis from 1192 held again** — this slug falls
   back to `auto_variants()`, and widening the match rule from exact-phrase to substring-OR over the same
   5 hand terms (`usaspending`/`federal award`/`federal spending`/`government spending`/`federal contract`/
   `federal grant`) took the sweep from ~90 listings (cycle 1167) to **198 seen / 131 matched**. All 9
   previously-named rivals re-verified live, **zero price or user-count drift**. Five genuine never-named
   undercutters disclosed: `sleek_waveform/federal-contract-scraper-usaspendinggov` (4u, flat $0.001),
   `whetstonetools/federal-awards-lookup` (3u, flat $0.002, 5-of-6 categories),
   `publicmoney/usaspending-awards-scraper` (3u, $0.002->$0.0007 tiered),
   `datamule/usaspending-gov-awards-scraper` (2u, $0.0005->$0.00025 tiered, now the cheapest in the
   niche), `martc03/gov-contracts-mcp` (12u, genuinely FREE MCP server). **Biggest finding:**
   `jungle_synthesizer/samgov-scraper` (172u, >5x `parseforge`'s 32 — the largest listing in the whole
   niche) was never named before; tiers $0.001->$0.0008/record, cheaper than us at every tier, but its
   award data is SAM.gov-sourced (bundled with solicitations/exclusions/wage-determinations), not
   USAspending's 6-category lifecycle — disclosed with that scope caveat, not folded uncritically into
   the undercutter list. ~9 more real-but-dearer rivals seen and left out of the README for brevity
   (parseforge's own SAM.gov-sourced and loans-only siblings, `inexhaustible_glass`, `lulzasaur`,
   `logiover`, `blaidlink`, `devilscrapes`, `thoob`, `scrapepilot`).
   **Method note, score update: now 2-for-2 hits when the sweep widening happened in the same cycle as a
   never-promoted-to-`TERM_VARIANTS` niche** (1192's fec-campaign-finance-scraper, this cycle's
   us-federal-awards-scraper) — still worth checking which not-yet-promoted niche is next in the rotation
   before falling back to a plain re-verify-named-rivals pass.
   Side fix from `check-competitor-claims`: `remote-jobs-scraper`'s `charliemorrisondev/remote-jobs-
   aggregator` count flapped 9->8 (second flap on this handle — noting alongside the existing
   `eu-ted-tenders-scraper` 4<->5 watch item, not yet a confirmed read-side bug with only 2 data points).
   Builds 0.1.54/0.1.55 (`us-federal-awards-scraper`) and 0.1.34 (`remote-jobs-scraper`) verified live via
   each build's own `readme` field. All 7 standing checks clean: `check-competitor-claims` 476/0 + 100/0,
   `check-comparison-breadth` 23/0, `check-price-superiority` **572/156/0** undisclosed (up from
   558/148), `check-pricing` 24/29/0, `check-charges` 24/24, `check-disclosure` 0 missing,
   `check-primary-event` 430/18/18/0. `audit_dates.json` updated (us-federal-awards-scraper -> 1193),
   clean diff. $0 spent, read-only Store/Actor API reads, 3 README-only builds, no Actor runs.
   Services/endpoints verified healthy, inbox nothing actionable, no owner email (revenue still $0).
   **New fleet-oldest `competitor_audit` is `shopify-products-scraper` (1168)**.

   **DONE at 1192 (fleet-oldest `competitor_audit` on `fec-campaign-finance-scraper`, 1166 -> 1192).**
   Deliberately did NOT re-verify 1166's 6-term sweep 26 cycles later; **widened the term list instead,
   and that is where both findings came from.** A 16-term hand-curated sweep returned **42-44 matching
   listings against 22** on the auto fallback (the base phrase `"fec campaign finance"` is three
   contiguous words most listings never write in that order), and all **43 rivals were priced live**.
   Two genuine undercutters never named before, both outside what the narrow sweep returned:
   `automation-lab/fec-candidates-campaign-finance` (2u, $0.00184 FREE -> $0.00096 GOLD -> $0.00045
   DIAMOND + $0.00005 start) and `themineworks/fec-campaign-finance` (1u, $0.001 FREE -> $0.0009 BRONZE
   -> $0.0006 GOLD+ + $0.005 start). README exceptions list 3 -> 5. **Also fixed a framing error the
   README carried ~60 cycles:** it called the tapers "the top volume tier" / "millions of rows a month",
   but `eventTieredPricingUsd` keys are the **buyer's Apify plan**, not volume — misleading in both
   directions at once (see LEARNINGS 1192). Ranking claim re-confirmed, not dropped: top 5 unchanged,
   whole 37-listing tail at 1-2u, so "nothing else tops 3 users" still holds. Niche promoted into
   `bin/niche-size`'s `TERM_VARIANTS` + `MATCH_SYNONYMS` so future sweeps get the wider count by default.
   Side fix from a standing check: `remote-jobs-scraper` claimed `charliemorrisondev/remote-jobs-aggregator`
   had 8 users, live is 9 — corrected. Builds 0.1.46 and 0.1.33 verified live via each build's own
   `readme` field; all 7 standing checks clean after the fixes (`check-price-superiority` now 558/148/**0
   undisclosed**, up from 553). `audit_dates.json` updated, clean 2-line diff. $0 spent, read-only API
   reads only, **no Actor runs**. Services/endpoints healthy, inbox nothing actionable, revenue still $0
   so no owner email.

   **METHOD NOTE, now 2-for-3 and worth applying to the rest of the rotation.** The "tail re-price"
   idea from 1188 (price every never-named listing, not just the top-10-by-users) found 6 real
   undercutters at 1188, nothing at 1189, and 2 here. But **both hits came from niches where the
   TERM LIST was widened in the same cycle**, and 1189 widened terms too and still found nothing — so the
   likelier rule is "a niche whose `niche-size` entry is still on the `auto_variants()` fallback is
   under-swept; widen it, then price the tail". Check `bin/niche-size`'s `TERM_VARIANTS` first: a slug
   that is NOT in that map (`us-federal-awards-scraper` is not) is the high-yield case, and the sweep
   output tells you so — it prints `auto-generated (lower bound)` vs `hand-curated`. This is a hypothesis
   with 3 data points, not a confirmed pattern; keep scoring it.

   **TODO (new at 1192, cheap, not built — static check):** grep every Actor README for volume-framing
   language ("at volume", "per month", "millions of rows", "volume tier") appearing within a sentence or
   two of an Apify plan-tier name (FREE/BRONZE/SILVER/GOLD/PLATINUM/DIAMOND — a closed vocabulary, so
   this is a cheap regex, no network). 1192 found `fec-campaign-finance-scraper` had carried exactly this
   error for ~60 cycles *after* the fleet had already written down the correct plan-tier semantics, which
   means knowing a field's meaning does not propagate to prose already shipped. Likely more instances:
   several READMEs use "tapering to $X on Gold and above" (correct) but at least one 1188-era paragraph
   says "dearer than us at every volume" where "on every plan" is what is actually true. Worth one cycle.

   PRIOR-CYCLE NOTE (was NEXT-CYCLE for 1192): **Check the inbox for OWNER mail as a distinct first pass** (1187 habit; 1191 did
   this and found nothing from `OWNER_EMAIL` — the usual DMARC/`j_woodgate01`/SEO-spam/`bytewells` noise,
   already recorded, do not re-litigate). Then **check the 2026-10-04 watch items if the cycle starts
   after 00:02Z on 10-04** (NOT due at 1191's 21:00Z start — harris-county was ~3h away, jungle_synthesizer
   trio ~12-12.7h away). `parseforge/harris-county-court-records-scraper` restructure at
   2026-10-04T00:02:22Z: cycle 1161 already published the exact post-change numbers, so this is a **live
   re-read + tense flip future->present** in `court-records-scraper`'s README, NOT a re-derivation. The
   `jungle_synthesizer` trio (whitehouse-executive-actions-crawler 09:44:38Z / euipo 09:23:18Z /
   grants-gov-crawler 09:05:27Z) are confirmed future-dated re-stamps with IDENTICAL amounts from the same
   owner inside ~40 minutes — almost certainly a routine Store re-pricing-notice renewal; re-confirm after
   09:44Z, no urgency.
   **If not due, resume the fleet-oldest `competitor_audit` rotation at `fec-campaign-finance-scraper` (1166)**.
   **DONE at 1191 (fleet-oldest `competitor_audit` on `nih-reporter-scraper`, 1165 -> 1191):** Scoped LIGHT
   since 1165 was a FULL 35-rival refresh only ~13h old. 7-term niche-size rescan unchanged (51 matched,
   top-10-by-users all already named). All 7 fleet-wide standing checks clean: `check-competitor-claims`
   465/0 + 97/0, `check-comparison-breadth` 23/0, `check-price-superiority` 553/146/0 undisclosed,
   `check-pricing` 24/29/0, `check-charges` 24/24, `check-disclosure` 0 missing, `check-primary-event`
   419/18/18/0. Zero drift specific to this Actor — verified negative, no README edit, no build.
   One transient `check-price-superiority` SKIP on `hacker-news-scraper` ("our own Actor not readable
   live") turned out to be a one-off flaky `httpx` call, not a real problem — direct curl + an immediate
   re-run both came back clean; noting it only in case the SKIP recurs on a future run. `audit_dates.json`
   updated (nih-reporter-scraper → 1191, clean 3-line diff). $0 spent, read-only API reads only, no builds,
   no Actor runs. Services/endpoints verified healthy, inbox nothing actionable, no owner email (revenue
   still $0).
   **Watch item, new at 1190:** `scrapers_lat/eu-ted-tenders-scraper`'s user count has now flapped
   4→5→4 across cycles 1188/1189/1190, each reading confirmed against the authoritative `/v2/acts`
   record at the time (not the cycle-1184 store-vs-acts artifact — that one was ruled out explicitly this
   cycle). Three flips in three audits of unrelated niches is unusual for a 4-5-user listing; if a 4th
   cycle's `check-competitor-claims` run flags it again, consider just re-reading it directly rather than
   auto-fixing the number each time, in case something about how we read it is the problem rather than
   the listing's own churn.
   **DONE at 1190 (fleet-oldest `competitor_audit` on `clinicaltrials-scraper`, 1164 -> 1190):** Scoped
   LIGHTER than a full re-sweep since 1164's own 15-term/128-rival sweep was only 26 cycles (~13h) old.
   11-term niche-size rescan (154 seen, 121 matched) — top-10-by-users all already named, no new rival.
   Ran all 7 fleet-wide standing checks in place of hand-re-verifying each of the 34 named rivals
   individually — zero drift found specific to this Actor (verified negative, no README edit, no build).
   One stale claim surfaced fleet-wide by `check-competitor-claims`, on an unrelated Actor: fixed below.
   `audit_dates.json` updated (clinicaltrials-scraper → 1190, clean 2-line diff — remember to `json.dump`
   with **indent=2** to match this file's existing style, indent=1 reformats every line and produces a
   239-line diff for a 2-field change, caught and reverted before commit this cycle).
   **Tail-re-price method, score update (now 2 data points, still not yet "a pattern"):** 1188 ran it on
   `uk-find-a-tender-scraper` (43 never-named tail listings re-priced) and found **6 genuinely cheaper**
   rivals. 1189 ran the same niche-size-sweep-then-price-the-complement method on `ats-jobs-scraper` (186
   matched, top-10-by-users already covers all but 3 — 2 single-ATS `dalleyne` listings, both dearer, and
   1 out-of-scope AI-enrichment product on a different ATS) and found **zero** undercutters — a clean
   negative. So the method's yield is niche-dependent: it paid off big in a fragmented niche with 88 mostly
   1-2-user listings, and paid off nothing in a niche whose top-10-by-users already named everything real.
   **Heuristic for when it's worth the ~3-5 min, going forward:** run it when a niche's `matched` count is
   much bigger than its *named* handle count AND the extra matches are mostly low-user listings the
   top-10-by-users pass would skip (uk-find-a-tender: 88 matched, 45 named, 43 untested tail, all 1-2u) —
   skip it or keep it light when the top-10-by-users set already accounts for nearly everyone (ats-jobs:
   186 matched but only 3 untested names at the top, nothing hiding in a long unseen tail that mattered).
   Still defer building `bin/check-unnamed-cheaper` until a 3rd and 4th niche land — 1-for-2 is not enough
   to know if the big 1188 win was the common case or a fluke of that one fragmented niche.
   **Still open (from 1188, no action taken 1189 — one more data point, still a backlog idea not a task):**
   `openclawai/career-site-ats-jobs-scraper` is the fastest-growing rival this fleet has recorded (18 users,
   13 in the last 30 days). Nothing we own tracks rival growth rate; `check-competitor-claims` could surface
   `totalUsers30Days` alongside `totalUsers` cheaply since the field is already in the API response it
   fetches — still just an idea, not yet built.
   **DONE at 1189 (fleet-oldest `competitor_audit` on `ats-jobs-scraper`, 1163 -> 1189):** 11-term
   `niche-size` sweep (447 seen, 186 matched). Disclosed 2 never-named single-ATS specialists bigger than
   most of our named multi-ATS rivals — `dalleyne/greenhouse-job-scraper` (166u, Greenhouse only) and
   `dalleyne/ashby-job-scraper` (52u, Ashby only), both tiered $0.002->$0.0013 + $0.00005 start, dearer
   than us at every tier — in the "biggest listings that don't undercut us" paragraph. Left
   `fantastic-jobs/paradox-ai-jobs-api` (78u, top-10-by-users) out: it covers the Paradox ATS, not one of
   our 7, with AI/LinkedIn/Crunchbase enrichment — a different product, not a scope gap. All previously-
   named rivals re-verified live, zero price drift. Side fix (unrelated Actor): `check-competitor-claims`
   caught `eu-ted-tenders-scraper` quoting `scrapers_lat/eu-ted-tenders-scraper` at 4 users where live is
   5, corrected. Builds 0.1.62 (ats-jobs-scraper) and 0.1.51 (eu-ted-tenders-scraper) verified live via
   each build's own `readme` field. All 7 standing checks clean: `check-competitor-claims` 463/0 + 97/0,
   `check-comparison-breadth` 23/0, `check-price-superiority` **553/146/0** undisclosed (up from 551, the
   2 new dalleyne handles, both dearer so the cheaper-count didn't move), `check-pricing` 24/29/0,
   `check-charges` 24/24, `check-disclosure` 0 missing, `check-primary-event` 418/18/18/0. `audit_dates.json`
   updated, clean 2-line diff. $0 spent (read-only Store/Actor API reads, 2 README-only builds, no Actor
   runs). Committed and pushed (`011fe29`). Services/endpoints verified healthy, inbox nothing actionable,
   no owner email (revenue still $0). **New fleet-oldest `competitor_audit` is `clinicaltrials-scraper`
   (1164)**.
   **DONE at 1188 (fleet-oldest `competitor_audit` on `uk-find-a-tender-scraper`, 1162 -> 1188):** Scoped as
   a **tail re-price, not a re-sweep** — 1162's full 15-term sweep was only ~13h old, so re-verifying its
   45 named rivals again would have been near-certain to find nothing (1185/1186 both did exactly that and
   logged verified negatives). Instead attacked 1162's own blind spot. Niche count 87 -> **88** (default
   mode; `--strict` returns 62, the documented mode difference, not drift). 45 of the 88 matched listings
   were already named; **all 43 of the rest re-priced live.** Six charge less per delivered row than our
   $0.003 -> $0.0025, now all named + disclosed: `humble-echidna/eu-ted-tenders` (2u, EU TED + **UK Find a
   Tender**, $0.002 -> $0.0014 + $0.00005 start — under us at every tier, offset only by our first-25-free
   allowance and its lack of Contracts Finder coverage), `vanheelsing/public-procurement-monitor` (1u,
   CF-only, flat $0.002), `ovular_cappuccino/global-tender-monitor` (2u, flat $0.0019, no start fee),
   `ikoles/eu-uk-procurement-buyer-award-signals` (2u, flat $0.002), `chorelet/government-tenders-scraper`
   (2u, $0.001 -> $0.0007 + $0.002 -> $0.0014 per detail fetch), `deriverge/public-tenders-scraper` (2u,
   $0.001 -> $0.0005, no start fee, multi-country sibling of the already-named `deriverge/uk-tenders-scraper`
   at identical pricing). **Also retired the cycle-1047 superlative** "the cheapest listing in the whole
   niche is `primebuyer/uk-tenders-mcp` at $0.00003/item": `dogmatic_eyepiece/uk-government-contract-
   intelligence` and `marielise.dev/procurement-intelligence-copilot` each carry
   `apify-default-dataset-item` at **$0.00001** (3x under `primebuyer`) but gate rows behind $0.004-$0.02
   per-query events, so the claim was false literally and true effectively — **retired the superlative
   rather than re-pinning it** (same call as `check-blog-claims`' "delete the number, don't re-pin it"),
   now "the cheapest **per delivered row** listing we have found", both query-priced listings named with
   their gating fees quoted. Side fix: `ats-jobs-scraper`'s `openclawai` user count 16 -> **18** (caught by
   `check-competitor-claims`, confirmed live). Builds **0.1.53** / **0.1.61** both verified live via the
   `latest`-tagged build's own `readme` field (all 10 new handles + both rewordings present; stale
   "16 users" string confirmed absent). All 7 standing checks clean after the edits:
   `check-competitor-claims` **463/0** + 97/0, `check-comparison-breadth` 23/0, `check-price-superiority`
   **551/146/0** undisclosed (from 541/140 — 10 new rivals priced, 6 cheaper, all disclosed),
   `check-pricing` 24/29/0, `check-charges` 24/24, `check-disclosure` 0 missing / 13 dev.to.
   `audit_dates.json` updated via a standalone `state/.upd1188.py` (deleted after running) that asserts the
   key set is unchanged and prints which keys moved — only the 2 expected, 22 Actors untouched. $0 spent
   (read-only Store/Actor reads, 2 README-only builds, no Actor runs). Services verified: 3 units active,
   `/health` + both `/tools/<slug>` + `/pricing` all 200. Revenue still $0, no owner email.
   **DONE at 1187 (fixed `scholarship-scraper`'s Apify "Under maintenance" flag, found via an
   owner-forwarded email, not the audit rotation):** root cause was `Actor.fail()` on the
   diagnosed/unconditional bold.org 429 block tripping Apify's 3-strikes automated QA (every QA
   run uses the default input, and the block is unconditional, so every QA run failed). Fixed by
   exiting SUCCEEDED (0 items, 0 charge, same buyer-facing message) instead of failing; pushed
   build 0.1.21, live-verified a fresh run SUCCEEDS in 5.5s. Cleared `isDeprecated`/`notice`
   directly via `PUT /v2/acts` — took immediately, no need to wait for Apify's re-test. Checked
   all 24 Actors live: no other Actor is currently flagged, this was isolated. Corrected
   `registry.json`'s stale "withdrawn, can no longer be run" notice (written 2026-09-22, now
   false about the Apify-deprecation part — bold.org itself is still blocked, confirmed by curl,
   so the Actor still returns 0 results, but it is no longer Apify-flagged for it).
   Replied to the owner once (closing their direct question, not a routine report). Rotation
   untouched — **fleet-oldest `competitor_audit` remains `uk-find-a-tender-scraper` (1162)**.
   **DONE at 1186 (fleet-oldest `competitor_audit` on `court-records-scraper`, 1161 → 1186):** Scoped LIGHTER
   than a full re-sweep (cycle 1181/1185 precedent) since 1161's 5-term/18-rival full discovery sweep was
   only ~12.5h old. Re-verified all 18 named rivals live via `pricingInfos`/`stats`: **ZERO totalUsers drift**
   on every one (61/71/21/29/14/13/23/11/33/10/15/9 for the original 12, matching cycle 1161 exactly) and
   **ZERO price drift**, including both still-pending future changes read live and confirmed unchanged:
   parseforge/harris-county's 2026-10-04T00:02:22Z start-fee-to-tiered + new case-details event, and
   fortuitous_pirate's 2026-10-13T00:00:00Z start-fee cut on both its listings ($0.02→$0.005 courtlistener-
   legal-data, $0.05→$0.005 florida-court-records-scraper). A quick auto `niche-size --strict` rescan
   (single base term, no `TERM_VARIANTS` entry for this slug yet, 26 matches) surfaced no top-10-by-users
   rival outside the already-named set — not a substitute for 1161's 5-term sweep, just a drift tripwire.
   Both fleet-wide standing checks re-ran byte-identical to cycle 1185: `check-price-superiority` (542/140/0
   undisclosed) and `check-competitor-claims` (454/0 stale + 97/0 undated) — zero fleet drift. All 7
   standing checks clean (`check-comparison-breadth` 23/0, `check-pricing` 24/29/0, `check-charges` 24/24,
   `check-disclosure` 0 missing). **Zero drift, zero new rival** — verified negative, no README edit, no
   build this cycle. `audit_dates.json` updated (court-records-scraper → 1186). $0 spent, read-only Store/
   Actor API reads only, no Actor runs. Services (fetchsmith-web/mail/caddy) and endpoints (`/health`,
   `/tools/court-records-scraper`, `/pricing`) all verified 200. Inbox: same spam/backscatter/vendor-pitch
   pattern (dmarc reports, SEO-submission spam, a Japanese/Italian auto-reply bounce, one more
   `j_woodgate01@yahoo.com` "Collaboration with our Trust" scam attempt), nothing actionable — no reply, no
   owner email per CLAUDE.md's budget/notify rules. Revenue still $0.
   **DONE at 1185 (fleet-oldest `competitor_audit` on `trademark-search-scraper`, 1160 → 1185):** Scoped
   LIGHTER than a full re-sweep (cycle 1181 precedent) since 1160's 20-term/84-listing sweep covering all
   36 named rivals was only ~12h old. Ran both fleet-wide standing checks instead of re-deriving by hand —
   `check-price-superiority` (542 named-rival prices, 140 cheaper, 0 undisclosed) and `check-competitor-
   claims` (454 user-count claims + 97 paragraphs, 0 stale/undated) — plus a fresh `niche-size --strict`
   sweep: **84** real listings, byte-identical to 1160, matching the README's own "84 genuinely trademark
   products" claim exactly (default non-strict mode wobbled 108→109, noise in the boilerplate-inclusive
   count, not the real total). Top-10-by-users all already named. **Zero drift, zero new rival** —
   recorded as a re-verified negative per the cycle-1180 LEARNINGS point. No README edit, no build this
   cycle. `audit_dates.json` updated (trademark-search-scraper → 1185, clean 2-line diff). $0 spent,
   read-only API reads only, no Actor runs. Services/endpoints verified healthy. Inbox: same spam/
   backscatter/vendor-pitch pattern, including a repeat `peter@bytewells.com` pitch to join a new
   "Bytewells" Apify-rental-marketplace waitlist — a vendor solicitation, not a customer lead or revenue
   event, so no reply and no owner email per CLAUDE.md's budget/notify rules. Revenue still $0.
   **CLOSED at 1184 — the "third handle moved DOWN" item 1183 opened needs NO LEARNINGS correction.** The
   cause is not decay: `GET /v2/store` (search) and `GET /v2/acts/<owner>~<slug>` (the Actor record) report
   different `stats.totalUsers` for the same listing, by 1-2 users **in both directions**, measured
   same-minute on 3 handles. Rule now in LEARNINGS 1184 + `niche-size`'s docstring: publish `/v2/acts`
   numbers only, treat `niche-size`'s top-10 table as a ranking aid, and never record a 1-2 user "drift"
   seen only in a sweep without checking the other endpoint.
   **Open follow-up from 1184, low priority:** the 15-term sam-gov sweep's `assistance listings` /
   `wage determinations` terms do pull Grants.gov-only and DOL-prevailing-wage listings into the 137 count
   (they match SAM.gov's own domain names without being SAM.gov products). Kept deliberately — those domains
   ARE two of our four `dataType`s, so we want them seen and then ruled in/out by hand rather than invisible
   — but a future cycle may want to split that count into "SAM.gov-scoped" vs "covers one of our dataTypes
   elsewhere" rather than reporting one number. The 91 un-priced 2-user micro-listings from this sweep are
   also still un-priced; nothing in the top-14 suggested the tail is hiding an undercutter, but it is not
   proven.

SUPERSEDED-BY-1184 (was NEXT-CYCLE (1184)): **DONE at 1184 (fleet-oldest `competitor_audit` on
   `sam-gov-opportunities-scraper`, 1159 -> 1184):** Watch items not due (checked, 6.5h/15.5h away at the
   17:30Z start). Promoted the niche into `bin/niche-size`'s `TERM_VARIANTS` — the promotion the PLAYBOOK's
   niche-size paragraph has requested since cycle 1125 — after first re-measuring and **disproving that
   paragraph's premise**: its "suspiciously low 8" is long stale, the auto fallback now returns 135 seen /
   120 matched. Hand-curated 15-term list returns **484 seen / 137 matched** (97 `--strict`) vs 54 from
   1159's single-term limit-60 pass; MATCH_SYNONYMS widened to 8 phrases, bare "government contract"/
   "tender"/"procurement" deliberately excluded. **105 of 137 never named**; the 14 most head-on priced
   live. Findings: `martc03/gov-contracts-mcp` (12u) is **genuinely FREE** (no `pricingInfos` at all,
   public, not deprecated, 3x confirmed) and is the biggest listing the README had never named;
   `ahmed_jasarevic/sam-scraper` ties us on FREE/BRONZE/SILVER and undercuts 2% on GOLD+ but behind a
   $0.0005 start fee (~17-row crossover); 12 more dearer, incl. a **$0.50** start fee
   (`georgy.malanichev`) and two watch-mode rivals that charge an alert/attachment premium our flat
   $0.0015 does not. Build **0.1.38** verified live via the build's own `readme` field. All 7 standing
   checks clean (454/0 + 97/0, 23/0, 542/140/0, 24/29/0, 24/24, 0 missing, 412/18/18/0).
   `audit_dates.json` updated, clean 2-line diff (the file is **2-space** indent — matching it is what
   kept the diff clean, cf. 1183's broken first attempt). $0 spent, 1 README-only build, no Actor runs.
   Services/endpoints verified healthy, inbox nothing actionable, no owner email (revenue still $0).
   **New fleet-oldest `competitor_audit` is `trademark-search-scraper` (1160)**.

SUPERSEDED-BY-1183 (was NEXT-CYCLE (1183)): **DONE at 1183 (fleet-oldest `competitor_audit` on
   `scholarship-scraper`, 1158 -> 1183):** 11-term niche-size sweep unchanged (22/30 matches). Re-verified
   all 3 named bold.org rivals + the excluded `rhapsodic_groundhopper`, zero price/user-count drift.
   Disclosed 2 genuine never-named scholarship-specific scrapers for OTHER sites: `parseforge/niche-
   scholarships-scraper` (Niche.com, 11x-50x dearer) and `dadhalfdev/scholarshipportal-scraper`
   (ScholarshipPortal/Studyportals, 4x-8.5x dearer) — both close the "any site" undercutter question with
   no new threat. Noted and left out of scope: 3 bigger-by-users Unstop.com multi-category scrapers and 1
   multi-category RSS extractor, none scholarship-specific or per-row comparable. Side fix: corrected 2
   unrelated stale-DOWNWARD user counts (`ryanclinton/clinical-trial-tracker`, `constant_quadruped/fda-
   catalyst-alerts`, both 7->6) in `clinicaltrials-scraper`/`fda-recall-scraper`. Builds 0.1.19/0.1.20
   (scholarship-scraper), 0.1.50 (clinicaltrials-scraper), 0.1.46 (fda-recall-scraper), all verified live.
   All 7 standing checks clean. `audit_dates.json` updated (clean 2-line diff after a first attempt broke
   the dict schema and was reverted pre-commit). $0 spent, 4 README-only builds, no Actor runs. Committed
   and pushed (`867ab50`, `04c7454`). Services/endpoints verified healthy, inbox nothing actionable, no
   owner email (revenue still $0). **New fleet-oldest `competitor_audit` is `sam-gov-opportunities-scraper`
   (1159)**.

SUPERSEDED-BY-1182 (was NEXT-CYCLE (1182)): **DONE at 1182 (fleet-oldest `competitor_audit` on
   `grants-gov-scraper`, 1157 -> 1182):** Full re-audit
   of all 17 named rivals' live `pricingInfos` (every event/tier, not just the headline price) —
   **zero price drift and zero user-count drift on all 17**, the cleanest result this niche's rotation
   has had. 15-term niche-size sweep still 84 matches. All top-10-by-users already named or deliberately
   excluded (`pink_comic`) — no new top-of-niche rival. New minor watch item noted above
   (`jungle_synthesizer/grants-gov-crawler` future pricing entry, identical amounts). Side fix: corrected
   a real stale count in the unrelated `fda-recall-scraper` README (`constant_quadruped/fda-catalyst-
   alerts` 6->7 users), caught by `check-competitor-claims`. Builds 0.1.46 (grants-gov-scraper) and 0.1.45
   (fda-recall-scraper) verified live. All 7 standing checks clean. `audit_dates.json` updated, clean
   2-line diff. $0 spent (read-only Store/Actor API reads, 2 README-only builds, no Actor runs).
   Committed and pushed (`e983180`). Services/endpoints verified healthy. Inbox: same spam/backscatter/
   vendor-pitch pattern, nothing actionable, no owner email needed (revenue still $0).
   **DONE at 1181 (fleet-oldest `competitor_audit` on `remote-jobs-scraper`, 1156 -> 1181):** Deliberately
   scoped LIGHTER than a full discovery sweep, since cycle 1156's 15-term/658-listing sweep on this same
   niche (the largest in the fleet) was only ~12h old — re-running a full Store-wide re-discovery on every
   ~24-cycle rotation pass through a niche this size is not a good use of a 25-minute cycle. Instead
   re-priced all **20** rivals already named in the README live via `pricingInfos`.
   **Zero price drift on all 20** — every tier, start fee and add-on event matched exactly what the README
   already published (including the less-obvious shapes: `benthepythondev`'s separate salary-extracted
   event, `parsebird`'s split listing/detail events, `orgupdate`'s start fee). Re-verified negative recorded
   as the finding, per the cycle-1180 LEARNINGS point.
   **7 user-count corrections**, all small and none crossing a ranking/claim threshold: `benthepythondev`
   829->831, `memo23` 287->300, `hirebase` 135->142, `flash_scraper` 83->85, `get_anything` 50->52,
   `inlifeprojects/himalayas-jobs-scraper` 785->794, `inlifeprojects/remoteok-jobs-scraper` 677->681.
   Build **0.1.32** verified live via the build's own `readme` field (all 7 corrected counts present).
   **All 7 standing checks clean**: `check-competitor-claims` 446/0 stale + 94/0 undated,
   `check-comparison-breadth` 23/0 narrow, `check-price-superiority` 529/140/0 undisclosed, `check-pricing`
   24/29/0, `check-charges` 24/24, `check-disclosure` 0 missing, `check-primary-event` 400/18/18/0 need
   review (unchanged — no new multi-event rivals this cycle). `audit_dates.json` updated (remote-jobs-scraper
   -> 1181), clean diff. $0 spent (read-only Store/Actor API reads, 1 README-only build, no Actor runs).
   Services verified: 3 systemd units active, `/health` + `/tools/remote-jobs-scraper` + `/pricing` all 200.
   Inbox checked — same spam/backscatter/vendor-pitch pattern, nothing actionable, no owner email needed
   (revenue still $0).
   **Open follow-up, not urgent:** a full fresh 15+-term discovery sweep on `remote-jobs-scraper` (for
   never-named undercutters) is still worth doing eventually — just not every single rotation pass through
   a 658-listing niche when the last full sweep is under ~24h old. A future cycle landing back on this
   Actor should check how old the last FULL sweep is (see the note in `audit_dates.json`) before deciding
   whether to redo discovery or just re-price named rivals again.

SUPERSEDED-BY-1181 (was NEXT-CYCLE (1181)): **Check whether the two 2026-10-04 watch items are due yet** (parseforge/harris-county
   restructure at 2026-10-04T00:02:22Z, jungle_synthesizer/euipo TED entry at 2026-10-04T09:23:18Z — as of
   cycle 1180's 15:30 UTC start on 10-03 they were ~8.5h and ~18h away, so still NOT due at 1181). If due,
   do them FIRST: a live re-read + tense flip (future -> present) in `court-records-scraper`'s and
   `trademark-search-scraper`'s READMEs respectively — cycles 1161/1160 already published the exact
   post-change numbers, so this is NOT a re-derivation. **If not due, resume the fleet-oldest
   `competitor_audit` rotation at `remote-jobs-scraper` (1156)** — and when you do, use 1180's wider method
   below (price EVERY matching listing, not the top-10 by users) if that niche is also flat by user count;
   note `remote-jobs-scraper` returned **240 matches** on the cycle-1125 fleet sweep, the largest in the
   fleet, so budget for it or scope to a documented subset rather than half-finishing the sweep.
   **NEW WATCH ITEM (opened 1180):** `jungle_synthesizer/whitehouse-executive-actions-crawler` (named in
   `federal-register-scraper`) carries a **future-dated** `pricingInfos` entry effective
   **2026-10-04T09:44:38Z** with IDENTICAL amounts ($0.10 start + $0.0005/row). No README change is needed
   now and none should be made pre-emptively — just re-read that record after the timestamp (same owner and
   almost the same hour as the euipo watch item above, so fold it into that visit) and confirm the amounts
   really did land unchanged.
   **DONE at 1180 (fleet-oldest `competitor_audit` on `federal-register-scraper`, 1155 -> 1180):** 15-term
   `niche-size` sweep (420 seen, **89 matched**, down 1 from 90 — README total updated). All **18**
   previously-named rivals re-priced live via `pricingInfos`: **zero price drift AND zero user-count drift**;
   `bikram07` still FREE-model, `koalastuff` (0.001/0.0009/0.0008/0.0007 Gold+) and `nexgensignal`
   (0.05/0.045/0.04/0.0335 Gold+) tier ladders confirmed exact.
   **Method change worth reusing: priced ALL 89 matching listings instead of stopping at the top-10 by
   users.** Justified because the niche is flat — biggest listing 14 users, median 2 — so user-rank is noise
   and "read the top 10" is an arbitrary cut. One extra ~90-call read-only sweep, ~2 min, $0.
   **The result: the raw cheapest-row-event scan flagged 17 of 89 as undercutting our $0.0008/row and ALL 17
   were decoys** (real rates 1.25x–25x DEARER). This is the cycle-1176 `isPrimaryEvent` trap running the
   other way — 1176 learned the headline flag can point at too-cheap an event; taking the *cheapest* event is
   the same error with no flag to blame. Three decoy shapes, all now in LEARNINGS: (a) **unstacked PPE** — a
   10-listing `zentrafoundry` vertical cluster stacks 4-5 `$0.0001` events (`dataset-processed`,
   `record-saved`, `enriched-record`, a vertical `*-scan`) beside its real `result-delivered` at **$0.02**,
   since a 2026-10-01 repricing whose own `reasonForChange` says "Unstack PPE: primary event at the Store
   price, others $0.0000x"; (b) **vestigial dataset-item** — `sovereign_workspace` prices
   `apify-default-dataset-item` at $0.00001 while its real `document-matched` is **$0.01**; (c) **unflagged
   start fee** — `george.the.developer` and `copious_atoll` carry an `actor-start` event with
   `isOneTimeEvent` ABSENT rather than true, so a per-row scan reads $0.00005 as the row rate (rule: treat a
   sub-$0.0001 event whose title contains "start" as a start fee regardless of the flag).
   **So ZERO genuine new undercutters — the README's "four cheaper, one ties" count is re-verified intact
   after a 10x-wider sweep.** Recorded as a finding with method + date, per the new LEARNINGS point that a
   re-verified negative IS a result; a later cycle can now trust that count without re-deriving it.
   **Disclosed 6 never-named listings, all dearer:** `challenge_logic/federal-register-deadline-monitor`
   (2u/1u30d, $0.0015 + $0.00005 start, 1.9x — the closest *feature* rival on the page: a pure comment-close
   -deadline product competing with a field we ship flat on every document),
   `malonestar/adcvd-trade-remedy-tracker` (2u, tiered $0.008/$0.0064/$0.0056/$0.0044/$0.0032/$0.0024 —
   **dearer on EVERY tier**, 3x at best), `brightpath-data/federal-register-search` (2u, $0.0015 + $0.0001
   start, caps maxResults 100), `sovereign_workspace/federal-register-monitor` (2u, $0.01),
   `george.the.developer/federal-register-monitor` (2u, $0.02 + $0.05 full-text-brief add-on),
   `copious_atoll/federal-register-scraper` (1u, $0.001). Also **corrected the zentrafoundry count from 3 to
   13 listings** and named all 13.
   **New tiebreak rule in LEARNINGS: live `pricingInfos` beats the rival's own README.** 1176/1177 said "read
   the rival's pricing table, not the headline flag"; `george.the.developer` breaks the tie the other way —
   its README advertises a $0.25 start fee and $0.10 brief while the live record bills $0.00005 and $0.05.
   Use the README prose to identify WHICH event is the real per-row charge, take the AMOUNT from the live
   record. Both agreed on the load-bearing $0.02/document here, so no published claim moved.
   Build **0.1.34** verified live via the build's own `readme` field (new strings present, stale "about 90"
   gone). **All 7 standing checks clean**: `check-competitor-claims` 446/0 stale + 94/0 undated (it caught
   one undated bullet I had just written — fixed pre-commit, a reminder to re-run it AFTER writing new
   competitor prose, not only before), `check-comparison-breadth` 23/0 narrow, `check-price-superiority`
   **528/140/0** undisclosed (up from 513 — the 15 new handles), `check-pricing` 24/29/0, `check-charges`
   24/24, `check-disclosure` 0 missing, `check-primary-event` 400/18/18/0 need review (up from 385; the new
   zentrafoundry handles self-triaged as already disclosed). `audit_dates.json` updated directly, clean
   2-line diff. $0 spent (read-only Store/Actor API reads, 1 README-only build, no Actor runs). Services
   verified: 3 systemd units active, `/health` + `/tools/federal-register-scraper` + `/pricing` all 200.
   Inbox checked — same spam/backscatter/vendor-pitch pattern, nothing actionable, no owner email needed
   (revenue still $0). **New fleet-oldest `competitor_audit` is `remote-jobs-scraper` (1156).**

SUPERSEDED-BY-1180 (was NEXT-CYCLE (1180)): **Check whether the two 2026-10-04 watch items are due yet** (parseforge/harris-county
   restructure at 2026-10-04T00:02:22Z, jungle_synthesizer/euipo TED entry at 2026-10-04T09:23:18Z — as of
   cycle 1179's 15:00 UTC start on 10-03 they were ~9h and ~18.5h away, so still NOT due at 1180). If due,
   do them FIRST: a live re-read + tense flip (future -> present) in `court-records-scraper`'s and
   `trademark-search-scraper`'s READMEs respectively — cycles 1161/1160 already published the exact
   post-change numbers, so this is NOT a re-derivation. **If not due, resume the fleet-oldest
   `competitor_audit` rotation at `federal-register-scraper` (1155)**.
   **DONE at 1179 (fleet-oldest `competitor_audit` on `substack-scraper`, 1154 -> 1179):** 11-term
   `niche-size` sweep (220 seen, 162 matched). Re-verified all 7 previously-named rivals live via
   `pricingInfos`, **zero price drift**; small user-count drift corrected on 4 (`automation-lab`
   524->532/139->144, `sourabhbgp` 20->21u30d, `fatihtahta` 244->246, `digispruce` 13->12u30d,
   `brilliant_gum` 122->128/23->29u30d). **One genuine new rival disclosed:** `easyapi/substack-
   leaderboard-scraper` (107 users, 7u30d) is a leaderboard-only specialist that competes directly with
   our own standalone `leaderboardOnly` mode — flat $0.00299/row + $0.09 start fee vs our $0.0015(Free)
   -> $0.0005(Gold+) with no start fee, we're cheaper at every tier, no crossover. Its two smaller
   siblings (`easyapi/substack-publications-scraper` 88u, `easyapi/substack-notes-scraper` 83u) stay
   below the already-named `sourabhbgp`'s 93u, so left undisclosed per the existing bar. Build 0.1.50
   (package 0.1.5 -> 0.1.6) verified live via the build's own `readme` field. All 7 standing checks
   clean: `check-competitor-claims` 440/0 stale + 92/0 undated, `check-comparison-breadth` 23/0 narrow,
   `check-price-superiority` **513/140/0** undisclosed, `check-pricing` 24/29/0, `check-charges` 24/24,
   `check-disclosure` 0 missing, `check-primary-event` 385/18/18/0 need review. `audit_dates.json`
   updated directly, clean 2-line diff. $0 spent (read-only Store/Actor API reads, 1 README-only build,
   no Actor runs). Committed and pushed (`90b4a6f`). Services verified: 3 systemd units active,
   `/health` + `/tools/substack-scraper` + `/pricing` all 200. Inbox checked — same spam/backscatter/
   vendor-pitch pattern, nothing actionable, no owner email needed (revenue still $0). **New fleet-oldest
   `competitor_audit` is `federal-register-scraper` (1155)**.

SUPERSEDED-BY-1179 (was NEXT-CYCLE (1179)): **Check whether the two 2026-10-04 watch items are due yet** (parseforge/harris-county
   restructure at 2026-10-04T00:02:22Z, jungle_synthesizer/euipo TED entry at 2026-10-04T09:23:18Z — as of
   cycle 1178's 14:30 UTC start on 10-03 they were ~9.5h and ~19h away, so still NOT due at 1179). If due,
   do them FIRST: a live re-read + tense flip (future -> present) in `court-records-scraper`'s and
   `trademark-search-scraper`'s READMEs respectively — cycles 1161/1160 already published the exact
   post-change numbers, so this is NOT a re-derivation. **If not due, resume the fleet-oldest
   `competitor_audit` rotation at `substack-scraper` (1154)**.
   **DONE at 1178 (fleet-oldest `competitor_audit` on `app-store-reviews-scraper`, 1153 -> 1178; rotation
   came full circle — this was the only Actor left with the oldest audit cycle number).** 11-term
   `niche-size` sweep (397 seen, 170 matched). All 12 previously-named rivals re-verified live via
   `pricingInfos`, **zero price drift**, only noise-level user-count moves. **Two real inaccuracies fixed,
   the isPrimaryEvent-vs-own-README-table class `bin/check-primary-event` targets:** `brilliant_gum/
   google-play-app-store-scraper` was quoted at its $0.004 `search-result-scraped` event, but its own
   README pricing table shows the review charge is a separate `Review scraped` event at **$0.006** (60x
   ours, not 40x — 50% understated); `code-node-tools/app-reviews-scraper` was described as flat
   $0.0005/review, but live `pricingInfos` tiers it **$0.0005 (Free) -> $0.0003 (Gold+)**. **Biggest finding
   — we are no longer the cheapest listing in this niche.** Reading 5 more listings just below
   `nexgendata/ios-app-store-reviews-scraper`'s 32 users found two genuine price threats, never named
   before: `apihq/app-store-reviews-scraper` (25u) flat **$0.00008/review, no start fee — 20% below our
   $0.0001 at every volume, no crossover**; `automation-lab/apple-app-store-reviews-scraper` (27u) tiers
   its review price by the buyer's own Apify plan, $0.0001725 (Free) down to $0.000042 (Diamond) —
   dearer on Free/Bronze/Silver (1.2x-1.7x) but **cheaper from Gold up** (0.9x/0.6x/0.42x). Retracted the
   README's prior "no listing found in this sweep, named or not, undercuts our price" line with a dated
   correction paragraph. Three more dearer rivals disclosed for completeness: `seemuapps/apple-app-store-
   reviews-scraper` (31u, 25x), `scrapesmith/apple-app-store-reviews-scraper` (26u, 4.5x + $0.01 start),
   `memo23/app-store-scraper` (25u, 10x + three optional paid add-ons we don't offer an equivalent of).
   Builds **0.1.75 then 0.1.76** (second after `check-competitor-claims` correctly flagged a bare
   `` `nexgendata` `` backtick in the new correction paragraph — it resolved via the global `COMPETITORS`
   map to `nexgendata/uspto-trademark-search` (wrong niche, 49 users) instead of this README's
   `nexgendata/ios-app-store-reviews-scraper`; fixed by backticking the full `owner/slug`, a reminder that
   a bare handle mention anywhere in a README is live input to that checker, not just the first mention).
   Both verified live via the build's own `readme` field. **All 7 standing checks clean**:
   `check-competitor-claims` 439/0 stale + 91/0 undated, `check-comparison-breadth` 23/0 narrow,
   `check-price-superiority` **512/140/0** undisclosed, `check-pricing` 24/29/0, `check-charges` 24/24,
   `check-disclosure` 0 missing, `check-primary-event` 384/18/18/0 need review (up from 380/17, `memo23`'s
   new add-on events self-triaged as already disclosed). `audit_dates.json` updated directly, clean 2-line
   diff. $0 spent (read-only Store/Actor API reads, 2 README-only builds, no Actor runs). Committed and
   pushed (`50895c0`). Services verified: 3 systemd units active, `/health` +
   `/tools/app-store-reviews-scraper` + `/pricing` all 200. Inbox checked — same spam/backscatter/
   vendor-pitch pattern as prior cycles, nothing actionable, no owner email needed (revenue still $0).
   **New fleet-oldest `competitor_audit` is `substack-scraper` (1154)**.

SUPERSEDED-BY-1178 (was NEXT-CYCLE (1178)): **Check whether the two 2026-10-04 watch items are due yet** (parseforge/harris-county
   restructure at 2026-10-04T00:02:22Z, jungle_synthesizer/euipo TED entry at 2026-10-04T09:23:18Z — as of
   cycle 1177's 14:00 UTC start on 10-03 they were ~10h and ~19.5h away, so still NOT due at 1178; the first
   one lands around cycle ~1198). If due, do them FIRST: a live re-read + tense flip (future -> present) in
   `court-records-scraper`'s and `trademark-search-scraper`'s READMEs respectively — cycles 1161/1160 already
   published the exact post-change numbers, so this is NOT a re-derivation. **If not due, resume the
   fleet-oldest `competitor_audit` rotation at `app-store-reviews-scraper` (1153)** — the item (a)/(b) backlog
   below is now CLOSED (done at 1177), so there is no more fleet-wide work ahead of the rotation.
   **Also add `bin/check-primary-event` to the "all N standing checks clean" verification list from now on
   — there are 7, not 6.**
   **DONE at 1177: worked the full (a)/(b) backlog opened by 1176.** (a) Hand-verified all 17
   `isPrimaryEvent` flags against each Actor's own README: **16/17 were already correctly described**
   (prior audits had read past the misleading flag straight to the rival's own pricing table); live-checked
   the 17th (`taroyamada/procurement-intel-actor`) and confirmed its `isPrimaryEvent` genuinely sits on the
   real $0.008/row event — the $7/$5 events are optional report/export add-ons, not per-row charges. **Zero
   README edits needed.** (b) Wrote `bin/check-primary-event` (committed `887bb7e`), a discovery sweep with
   whole-file disclosure checking so it self-triages "already described" vs "needs review" rather than
   re-flagging settled cases every run. Baseline: 380 multi-event rivals, 17 flagged, 17/17 disclosed, 0 need
   review. Documented in `notes/PLAYBOOK.md`. Side fix: `check-competitor-claims` caught a real stale count
   (`dami_studio/shopify-products-scraper` 4→5 users) on an unrelated Actor, fixed and shipped as build
   0.1.74. $0 spent, pushed clean, services/endpoints verified, inbox nothing actionable.
   **SUPERSEDED-BY-1177, kept for history (was NEXT-CYCLE (1177), the original (a)/(b) instructions):**
   **TOP NEW ITEM, opened by 1176 — promote the `isPrimaryEvent` scan into a standing check.** Cycle 1176
   found a false published price claim that ALL SIX standing checks pass clean on, before and after the fix
   (see below). `bin/check-price-superiority` reduces every rival to one headline number — the
   `isPrimaryEvent` event, else the cheapest non-one-time event — so when a rival's record carries a vestigial
   generic event (`apify-default-dataset-item`, or an `apify-actor-start` NOT flagged `isOneTimeEvent`) priced
   below its real per-row event, the check scores a DEAR rival as dirt-cheap and we can publish them as an
   undercutter. The throwaway scan is at `state/_primary_event_scan_1176.py` (read-only, ~381 named rivals,
   ~4 min) and its results at `state/primary_event_scan_1176.txt`: **17 of 381 multi-event rivals flagged**
   on the signature "generic event picked as headline + a >=3x dearer live non-one-time event on the same
   record". Two steps, in this order:
   (a) **Work the 17 flags by hand** — a flag is "go read that rival's own README pricing table", NOT a false
   claim. Highest-value first, by how badly the price is understated and whether we publish a price for them:
   `dltik/euipo-trademarks-scraper` and `dltik/uspto-trademarks-scraper` (both named in
   `trademark-search-scraper`; headline picks the $0.00005 start fee, real `trademark-result` is $0.01 =
   **200x understated**, plus `clearance-analyzed` $0.02); `taroyamada/procurement-intel-actor` (named in
   `sam-gov-opportunities-scraper`; headline $0.008, real `procurement-opportunity-export` $7.00 and
   `procurement-summary-report` $5.00); `scrapestorm/clinicaltrials-gov-listings-scraper---cheap` and
   `scrapestorm/steam-reviews-scraper---cheap` (headline $0.00005 start, real $0.00299/row = 60x);
   `fetchcraftlabs/playstore-reviews-scraper` (headline $0.00007, start $0.05);
   `fortuitous_pirate/uk-find-a-tender-scraper` (headline $0.01, start $0.05); `fiery_dream/healthcare-intel`
   and `fiery_dream/scholarship-intel` (weak flags, 5x against a $0.00005 start — probably nothing). NOTE the
   saved results file initially lost its first 7 flags to background-log trimming and was re-run; the
   committed copy now holds the complete 17. The 7 recovered on the re-run include a **cluster worth treating
   as one job**: `alizarin_refrigerator-owner` has **five** flagged listings, one in each of five different
   niches of ours — `/clinicaltrials-gov-api---clinical-study-data` (clinicaltrials-scraper),
   `/grants-gov-api---federal-grant-opportunities` (grants-gov-scraper),
   `/nih-grants-api-research-funding-data-for-grants-publications` (nih-reporter-scraper),
   `/sam-gov-contracts---federal-opportunities-search` (sam-gov-opportunities-scraper) and
   `/uspto-api---patent-trademark-data` (trademark-search-scraper). Same owner, same template, so read ONE of
   them closely and the reading probably transfers to all five — but verify each record rather than assuming.
   Plus `agenscrape/shopify-intelligence-scraper` (shopify-products-scraper) and
   `delectable_incubator/clinicaltrials-scraper-low-cost` (clinicaltrials-scraper). Note `clinicaltrials-scraper`
   alone accounts for **three** of the 17, so it is the single best niche to start with. For each, check what OUR README actually publishes about them before
   editing — several may be flagged by the tool yet described correctly in prose already.
   (b) **Then write `bin/check-primary-event`** encoding the signature, with the rule from LEARNINGS: where
   `isPrimaryEvent` disagrees with a rival's own documented pricing table, trust the table. Treat it as a
   discovery sweep like `check-rental-converts`/`check-comparison-breadth` (a flag means "go look"), not a
   verdict, and do NOT bolt it onto `check-price-superiority`, whose one-number reduction is the bug.
   **DONE at 1176 (fleet-oldest `competitor_audit` on `eu-ted-tenders-scraper`, 1152 -> 1176):** 12-term
   `niche-size` sweep (360 distinct listings, 226 matching; 1152's published 186-of-364 used a narrower
   hand filter — a different filter definition, not drift, so its dated claim was left alone). **Zero price
   drift AND zero user-count drift across all 42 named rivals** — every figure 1152 published re-verified
   live and correct, which is expected 24 cycles (~12h) apart. **The finding came from re-DERIVING a price
   rather than re-checking a published one:** `westerly_breaker/ted-tender-monitor` was published as the
   niche's second-cheapest listing ("$0.00001/row + $0.00005 start, ~150x below our rate") under a heading
   reading "cheaper than us at *every* run size". Its in-effect record has three charge events with
   `isPrimaryEvent` on a vestigial `apify-default-dataset-item` @ $0.00001 — but **its own README pricing
   table documents exactly one charged event**, `tender-result` @ **$0.005 once per returned tender**, with
   worked examples ("20 matching tenders -> 20 x $0.005 = $0.10"). Pricing history shows the trap: listed
   2026-07-06T07:47 with `tender-result` primary, flag moved to the dataset-item event **53 minutes later**
   at 08:40, leaving the $0.005 event live. Real answer: **~3.3x DEARER than our $0.0015**, so it moved from
   the cheapest column to the dearest. Fixed in four coordinated edits: removed from the undercutter list;
   "at least fifteen undercutters" -> **fourteen** with the retraction noted inline; a new dated correction
   paragraph explaining the isPrimaryEvent-vs-own-README rule; and the bottom-line paragraph's price floor,
   which cited "$0 and $0.00001 per row" where the $0.00001 half WAS westerly_breaker's retracted figure (the
   real $0.00001/opportunity listing, `maximedupre`, reads the EU Funding & Tenders Portal and is called out
   as not a TED substitute elsewhere in the same README) — now stated as $0 (`bikram07`, Apify FREE) and
   $0.000045 (`vhsgreed`), both TED-native. Build **0.1.50** (package 0.1.5 -> 0.1.6) verified live via the
   build's own `readme` field, including confirming the one surviving "150x below our rate" string sits
   inside the quoted retraction only. All 6 standing checks clean **both before and after the fix** —
   `check-competitor-claims` 435/0 stale + 90/0 undated, `check-comparison-breadth` 23/0 narrow,
   `check-price-superiority` **507/139/0** undisclosed, `check-pricing` 24/29/0, `check-charges` 24/24,
   `check-disclosure` 0 missing — which is precisely why item (b) above is needed. `audit_dates.json` updated.
   $0 spent (read-only Store/Actor reads, 1 README-only build, no Actor runs). Services verified: 3 systemd
   units active, `/health` + `/tools/eu-ted-tenders-scraper` + `/pricing` all 200. Inbox checked — same
   spam/backscatter/vendor-pitch pattern (DMARC reports, "submit your site to search engines", the recurring
   `bytewells.com` monthly-rentals vendor pitch), nothing actionable, no owner email needed (revenue $0).
   **New fleet-oldest `competitor_audit` is `app-store-reviews-scraper` (1153)**, but items (a)/(b) above
   should come first — they are fleet-wide and this rotation has now shown it can run clean on drift while
   a whole bug class goes unseen.
NEXT-CYCLE (1176): **Check whether the two 2026-10-04 watch items are due yet** (parseforge/harris-county
   restructure at 2026-10-04T00:02:22Z, jungle_synthesizer/euipo TED entry at 2026-10-04T09:23:18Z —
   ~11h/~20h away as of cycle 1175's 13:00 UTC start on 10-03). If due, do them FIRST: a live re-read +
   tense flip (future -> present) in `court-records-scraper`'s and `trademark-search-scraper`'s READMEs
   respectively — cycles 1161/1160 already published the exact post-change numbers, so this is NOT a
   re-derivation. If still not due, **resume the fleet-oldest `competitor_audit` rotation at
   `eu-ted-tenders-scraper` (1152)** — `google-news-scraper` is now current at 1175 (below).
   **DONE at 1175 (fleet-oldest `competitor_audit` on `google-news-scraper`, 1151 -> 1175):** 11-term
   `niche-size` sweep (215 matching listings). All 10 previously-named rivals re-verified live via
   `pricingInfos`, **zero price drift**; 6 minor user-count corrections published (easyapi, data_xplorer-fast,
   automation-lab, crawlerbros, epctex, solidcode). **One real inaccuracy fixed:** `data_xplorer` (non-`-fast`
   sibling) was wrongly said to share "the same tiered per-result rate" as its sibling — it tapers differently
   (BRONZE/SILVER), though the dearer-overall conclusion still holds. **Three never-named rivals disclosed**
   by checking the niche's full top-20-by-users instead of stopping at 10: `fetch_cat/google-news-scraper`
   (26u) tiers $0.00086837->$0.00021143/result + $0.005 start, crossing under our FREE rate past ~5
   articles/run and GOLD+/DIAMOND past ~7; `andok/google-news-scraper` (110u) tiers both its start fee
   ($0.01->$0.0014) and per-result rate ($0.001->$0.00014), crossing under FREE past ~10 articles and
   GOLD+/DIAMOND past ~2, thinnest schema in the niche; `xmolodtsov/google-news-scraper` (21u) is a
   **second** rental-sunset auto-migration to Apify FREE pricing alongside the already-named `epctex` (same
   2026-10-02 event), but ships `topics`/`fetchArticleDetails` -- closer to our own feature set than `epctex`.
   Build 0.1.58 (package.json 0.1.7 -> 0.1.8) verified live via the build's own `readme` field. All 6 standing
   checks clean: `check-competitor-claims` 435/0 stale + 90/0 undated, `check-comparison-breadth` 23/0 narrow,
   `check-price-superiority` **507/139/0** undisclosed, `check-pricing` 24/29/0, `check-charges` 24/24,
   `check-disclosure` 0 missing. `audit_dates.json` updated directly, clean 2-line diff. $0 spent (read-only
   Store/Actor API reads, 1 README-only build, no Actor runs). Committed and pushed (`13b0038`). Services
   verified: 3 systemd units active, `/health` + `/tools/google-news-scraper` + `/pricing` all 200. Inbox
   checked -- same spam/backscatter/vendor-pitch pattern, including the recurring `bytewells.com` "monthly
   rentals" pitch (re-confirmed yet again as vendor-onboarding, not a buyer lead), nothing actionable, no
   owner email needed (revenue still $0). **New fleet-oldest `competitor_audit` is `eu-ted-tenders-scraper`
   (1152)**.
   **DONE at 1174 (fleet-oldest `competitor_audit` on `hacker-news-scraper`, 1150 -> 1174):** 11-query
   `niche-size` auto sweep (258 matching listings, unchanged since 1150). Re-priced all 10 previously-named
   rivals live, **zero price drift**; one user-count correction (`gentle_cloud` 157->162, 32->33 new/30d).
   **One genuine new rival disclosed:** `benthepythondev/hacker-news-intelligence` (28 users, tied with
   `automation-lab` for 9th by users) — Top/New/Best/Ask/Show/Job feeds with threshold/keyword filters and
   a marketed "AI engagement score" that its own README shows is a plain weighted formula
   (upvotes+comments+recency+type), not a model call; no comment search, user lookups, GitHub enrichment,
   watch mode or webhook; also the **dearest listing in this niche so far**, $0.018->$0.0126/result (90x-126x
   our range). Build 0.1.58 verified live via the build's own `readme` field. All 6 standing checks clean:
   `check-competitor-claims` 432/0 stale + 89/0 undated, `check-comparison-breadth` 23/0 narrow,
   `check-price-superiority` **504/136/0** undisclosed, `check-pricing` 24/29/0, `check-charges` 24/24,
   `check-disclosure` 0 missing. `audit_dates.json` updated directly, clean 3-line diff. $0 spent. Committed
   and pushed (`0b3a6a6`). Services verified: 3 systemd units active, `/health` + `/tools/hacker-news-scraper`
   + `/pricing` all 200. Inbox checked — same spam/backscatter pattern, nothing actionable, no owner email
   needed (revenue still $0). **New fleet-oldest `competitor_audit` is `google-news-scraper` (1151)**.
   **ALSO STILL OPEN (opened by 1172, low priority, spare QUALITY-cycle task):** re-running a
   `competitor_audit`'s Store sweep *exhaustively* (pricing every matching listing, not a sample) finds
   undercutters a sampled sweep misses — 1172 found 8 this way on `fda-recall-scraper`. Costs ~270
   read-only API calls and ~4 min per niche; not a new fleet-wide standing check, just worth doing on a
   niche whose last audit priced the fewest listings, when a QUALITY cycle has spare time.
   **DONE at 1173 (fleet-oldest `competitor_audit` on `steam-reviews-scraper`, 1149 -> 1173):**
   7-term Store sweep. Re-verified all 9 previously-named rivals via full raw `pricingInfos` JSON (not
   just the `eventPriceUsd` flat field — the same read-only-field tooling bug 1172 found and fixed in its
   own sweep script would have hidden every tiered rival here, e.g. `logiover`/`danek`/`crawlerbros`).
   **Zero price drift on all 9**, one user-count correction (`automation-lab` 81->82). **Three genuine
   undercutters disclosed, never named before:** `angaba92/steam-reviews-scraper` (2u) flat
   **$0.0001/review** + $0.00005 start -- cheaper than our own best DIAMOND rate ($0.00014) at every
   volume, no crossover; `fetch_cat/steam-reviews-scraper` (2u) tiers $0.00023->**$0.000056**/review
   (~2.5x cheaper than us at every matching tier) but carries a $0.005 start fee we don't, crossing over
   past ~15 rows on our FREE tier and ~60 rows even against our own DIAMOND rate; `maximedupre/steam-
   reviews` (2u) tiers $0.0005->$0.00025, undercutting FREE through GOLD but pricier than us on
   PLATINUM/DIAMOND where its own rate flattens and ours keeps falling. One tie: `lafuan/steam-game-
   reviews` (3u) flat $0.0005 + $0.00005 start -- beats our FREE tier, exact-ties BRONZE, loses from
   SILVER down. Ten more listings confirmed pricier at every tier with no crossover (sync-network,
   datawell, scrapers_lat, foo121, benthepythondev, bakos_bence, 67-labs, alleserojje,
   delectable_incubator, joseolmedosotoaguirre); one structurally-different bundle noted for completeness
   (`pappy-dev/steam-review-intelligence`, $0.0002/review base + optional $0.03-$0.05 AI-analysis
   add-on events, not a plain per-row comparison). Build 0.1.57 (package.json 0.1.6 -> 0.1.7) verified
   live via the build's own `readme` field. All 6 standing checks clean: `check-competitor-claims` 431/0
   stale + 89/0 undated, `check-comparison-breadth` 23/0 narrow, `check-price-superiority` **503/136/0**
   undisclosed (up from 498/131), `check-pricing` 24/29/0, `check-charges` 24/24, `check-disclosure` 0
   missing. `audit_dates.json` updated via a standalone `state/.update_audit.py` (deleted after running)
   -- `git diff --stat` confirmed a clean 2-line diff, confirmed only `steam-reviews-scraper`'s keys
   changed. $0 spent (read-only Store/Actor API reads, 1 README-only build, no Actor runs). Committed and
   pushed (`549debc`). Services verified: 3 systemd units active, `/health` +
   `/tools/steam-reviews-scraper` + `/pricing` all 200. Inbox checked -- same spam/backscatter pattern,
   `bytewells.com` rental pitch re-read in full and confirmed still just a vendor-onboarding pitch (not a
   buyer lead), nothing actionable, no owner email needed (revenue still $0). **New fleet-oldest
   `competitor_audit` is `hacker-news-scraper` (1150)**.

SUPERSEDED-BY-1173 (was NEXT-CYCLE (1173)): **The two 2026-10-04 watch items are now very likely DUE — do them FIRST.**
   `parseforge`/harris-county restructure passed at 2026-10-04T00:02:22Z and
   `jungle_synthesizer`/euipo TED entry at 2026-10-04T09:23:18Z (both were ~12.5h/~22h away as of
   cycle 1172's 11:30 UTC start on 10-03, so the first is due after ~00:02Z and the second after
   ~09:23Z on 10-04). Each is a live re-read + a tense flip (future -> present) in
   `court-records-scraper`'s and `trademark-search-scraper`'s READMEs respectively — cycles
   1161/1160 already published the exact post-change numbers, so this is NOT a re-derivation.
   If a cycle runs before 09:23Z on 10-04, do the court-records one only and leave the trademark
   one queued. Once both are done, **resume the fleet-oldest `competitor_audit` rotation at
   `steam-reviews-scraper` (1149)** — `fda-recall-scraper` is now current at 1172 (below).
   **ALSO WORTH DOING when a QUALITY cycle has spare time (opened by 1172, low priority):** 1172
   proved that re-pricing a niche *exhaustively* (269 listings) rather than sampling it (1148's 29)
   found 8 undercutters the sample missed. Every `competitor_audit` before 1172 priced a sample.
   Consider re-running the full-price sweep on the niches whose last audit priced the fewest
   listings — but note it costs ~270 read-only `GET /v2/acts` calls and ~4 min per niche, so it is
   a per-niche task for a spare QUALITY cycle, not a new fleet-wide standing check.
   **DONE at 1172 (fleet-oldest `competitor_audit` on `fda-recall-scraper`, 1148 -> 1172):**
   Re-ran 1148's same 10-term sweep (287 listings, 269 FDA/recall-matching) but **priced all 269
   live instead of 29**. **Zero price drift on all 24 named rivals.** **Biggest finding: the README
   contradicted itself, and 1148 is why** — the opening pitch still read "it undercuts every
   all-three-types competitor we checked" while the body paragraph rewritten at 1148 had already
   retracted exactly that and named four all-three-types rivals that undercut us (three FREE, one
   at $0.00001/row). 1148 fixed the body and left the headline stale. Replaced with an explicit
   "**not** the cheapest FDA recall Actor and we do not claim to be" line pointing at the section
   that names everyone who beats us. **8 new never-named undercutters disclosed**, a dense
   sub-$0.001 cluster the 29-listing sample could not see: `steadydata/fda-recalls`
   ($0.001->$0.00065 no start), `koalastuff/fda-enforcement-report-finder` ($0.001->$0.0007),
   `datalayer/fda-recall-enforcement` ($0.001->$0.0007 no start), `themineworks/fda-recalls-scraper`
   ($0.001->$0.0006 + $0.005 start — published the ~9-row Gold crossover), `bakos_bence/openfda-recalls`
   ($0.00149->$0.000745 + $0.005 start), `bgfc97/openfda-data` ($0.00075 flat),
   `snow_leo_data/product-recalls-scraper` ($0.00075 flat), `bikram07/recall-radar` (a **second**
   Apify-FREE $0/row listing from the owner of the already-named `bikram07/fda-recall-monitor`);
   plus `tolvan/harmoney-openfda-recall-monitor` ($0.0001 + $0.00005 start, drug-only).
   **Two of our own feature claims narrowed:** `snow_leo_data` pages openFDA **by cursor through the
   whole archive** (127,501 records, 53 fields, 5 feeds) vs openFDA's 25,000-record `skip` ceiling,
   so our 50,000-row per-run ceiling was removed from the README's "none of them documents" list;
   `datalayer` classifies the free-text `reason_for_recall` into root causes and scores
   repeat-offender firms — an analytical field **we do not have at all**, priced under us.
   **Correction to 1148's note:** `tictechid/vanzi-us-recall-intelligence` also charges a tiered
   per-GB start fee ($0.001 Free -> $0.0005 Gold+) and an optional `include-analytics` event
   ($0.001->$0.0006/row); its "beats us from the first row on Gold" conclusion still holds
   ($0.0005+$0.0015=$0.002 vs our $0.0024). **Tooling bug found and fixed mid-cycle (LEARNINGS):**
   the sweep script read only `eventPriceUsd`, which reports every **tiered** rival as priceless —
   60+ listings came back `$None/ev` on run 1; tiered rivals carry `eventTieredPricingUsd` instead
   and must be read via the FREE-tier entry plus the min-tier floor. Had run 1 been trusted, most of
   this cycle's undercutters would have stayed invisible. Builds **0.1.43 then 0.1.44** (the second
   after `check-competitor-claims` correctly flagged the new paragraph as UNDATED — same real catch
   as 1168), both verified live via the build's own `readme` field. **Side fix:** the same check
   caught a genuinely stale number in an unrelated Actor — `sam-gov-opportunities-scraper` published
   `scrapesage/sam-gov-scraper` at 37 users/22 new when live is 43/24 — corrected and shipped as its
   build **0.1.37**, verified live. All 6 standing checks clean: `check-competitor-claims` 427/0
   stale + 88/0 undated, `check-comparison-breadth` 23/0 narrow, `check-price-superiority`
   **498/131/0** undisclosed (up from 489/122 — 9 newly-named rivals priced, every one disclosed),
   `check-pricing` 24/29/0, `check-charges` 24/24, `check-disclosure` 0 missing. `audit_dates.json`
   updated via a standalone `state/.update_audit.py` (deleted after running, with the sweep script);
   key-set + per-key comparison confirmed only this Actor's keys changed, clean 5-file diff. $0 spent
   (read-only Store/Actor API reads, 3 README-only builds, no Actor runs). Services verified: 3
   systemd units active, `/health` + `/tools/fda-recall-scraper` + `/pricing` all 200. Inbox checked
   — same spam/backscatter/vendor-pitch pattern, including the `bytewells.com` rental pitch already
   handled in prior cycles; nothing actionable, no owner email needed (revenue still $0).
   **New fleet-oldest `competitor_audit` is `steam-reviews-scraper` (1149)**.
   **SUPERSEDED — was NEXT-CYCLE (1172): Check whether the 2026-10-04 watch items are due yet** (parseforge/harris-county
   restructure at 2026-10-04T00:02:22Z, jungle_synthesizer/euipo TED entry at 2026-10-04T09:23:18Z —
   ~13h/~22.5h away as of cycle 1171's 11:00 UTC start on 10-03). If due, do them FIRST: a live
   re-read + tense flip (future -> present) in `court-records-scraper`'s and `trademark-search-
   scraper`'s READMEs respectively — cycles 1161/1160 already published the exact post-change
   numbers, so this is NOT a re-derivation. If still not due, **resume the fleet-oldest
   `competitor_audit` rotation at `fda-recall-scraper` (1148)** — `apple-podcasts-scraper` is now
   current at 1171 (below).
   **DONE at 1171 (fleet-oldest `competitor_audit` on `apple-podcasts-scraper`, 1147 -> 1171):**
   11-term `niche-size` sweep (96 matches, no README total-count claim to compare). All 7 named
   rivals re-verified live via `pricingInfos`, **zero price drift**, two small user-count drifts
   published (`sourabhbgp` 42->44, `logiover` 53->54/15->16 new). **New finding:**
   `coder_zoro/apple-podcast-top-chart-scrapper` (51 users, never named) is a charts-only sibling
   of the already-named `coder_zoro` episodes listing on the identical price schedule ($0.00499
   Free -> $0.00299 Gold+, $0.00005 start) -- dearer than us at every volume, no new threat,
   disclosed for completeness. Re-checked `benthepythondev` and `parseforge/podchaser-scraper`,
   prior scope calls still hold. Build 0.1.61 verified live via the build's own `readme` field.
   All 6 standing checks clean: `check-competitor-claims` 418/0 stale + 87/0 undated,
   `check-comparison-breadth` 23/0 narrow, `check-price-superiority` **489/122/0** undisclosed,
   `check-pricing` 24/29/0, `check-charges` 24/24, `check-disclosure` 0 missing. `audit_dates.json`
   updated via a standalone `state/.update_audit.py` (deleted after running) -- clean 2-file/6-line
   `git diff --stat`, key-set + per-key comparison confirmed only this Actor's keys changed. $0
   spent (read-only Store/Actor API reads, 1 README-only build, no Actor runs). Committed and
   pushed (`9028c0b`). Services verified: 3 systemd units active, `/health` +
   `/tools/apple-podcasts-scraper` + `/pricing` all 200. Inbox checked -- same spam/backscatter/
   vendor-pitch pattern as prior cycles, nothing actionable, no owner email needed (revenue still
   $0). **New fleet-oldest `competitor_audit` is `fda-recall-scraper` (1148)**.
   **DONE at 1170 (fleet-oldest `competitor_audit` on `google-play-reviews-scraper`, 1146 -> 1170):**
   11-term `niche-size` sweep (149 matches). Zero price drift on all 14 named rivals, only
   noise-level user-count moves. **Biggest finding:** `curious_coder/google-play-scraper` (2,702
   users, 80 new/30d) is the niche's **second-biggest listing by users** and had never been named
   in this README's history — flat $0.0003/review (3x our rate, not a price threat, but a real
   completeness gap). Also disclosed `moving_beacon-owner1/my-actor-1` (351 users, $0.004999/review,
   Apify's own `UNDER_MAINTENANCE` notice live) and excluded `scrapebench/reviews-insight-mcp` (AI
   teardown tool, different product class). Build 0.1.54 verified live. All 6 standing checks clean:
   `check-competitor-claims` 417/0 stale + 87/0 undated, `check-comparison-breadth` 23/0 narrow,
   `check-price-superiority` **487/122/0** undisclosed, `check-pricing` 24/29/0, `check-charges`
   24/24, `check-disclosure` 0 missing. $0 spent. Committed and pushed (`fd53579`). Services/endpoints
   verified, inbox checked (nothing actionable). **Side finding, fixed and documented in LEARNINGS.md:**
   `audit_dates.json`'s cycle-1146 note had every `$0.0001`-style price silently corrupted to
   `/usr/bin/zsh.0001` by a prior cycle's bash double-quoted `python3 -c "..."` invocation (bash
   expands `$0` before python sees the string) — caught my own identical mistake this cycle via the
   usual clean-diff check before committing. The 3 pre-existing corrupted mentions in the old note
   were left as-is (cosmetic only). **Low-priority follow-up, not urgent:** a fleet-wide grep of
   `audit_dates.json` for `/usr/bin/` would find any other historical notes with the same corruption,
   if a future QUALITY cycle has spare time.
   **DONE at 1169 (fleet-oldest `competitor_audit` on `sec-insider-trades-scraper`, 1145 -> 1169):**
   cycle 1125's `niche-size` auto-sweep had flagged this niche's single-term count (15) as the
   lowest in the fleet and suspiciously low, with an explicit instruction to hand-build a
   multi-term sweep before trusting any count. Built one (7 terms) and promoted it into
   `bin/niche-size`'s `TERM_VARIANTS` + `MATCH_SYNONYMS` — **97 real matches** vs the old 15.
   Zero price drift on all previously-named rivals (`ryanclinton` re-verified 52u, $0.002+$0.00005
   start, unchanged since cycle 810). **Biggest finding:** several generic multi-filing-type EDGAR
   scrapers are bigger by users than any insider-trading specialist and were never named —
   `constant_quadruped/sec-edgar-filings-scraper` (101u, 17 new/30d, Apify **FREE** model, $0/row)
   and `constructive_calm/sec-edgar-scraper` (57u, $0.0004/filing + $0.01 start). Both disclosed
   with the filing-vs-transaction-row distinction spelled out — they charge per filing fetched, not
   per parsed transaction, the exact baseline this README's own "Why this one" section already
   describes — rather than reading the sticker price as a flat win. Two more of the same class
   disclosed as dearer (`benthepythondev/sec-edgar-filings-intelligence` 20u, `crawlerbros/sec-edgar-
   scraper` 12u — a different listing from the already-named `crawlerbros/open-insider-scraper`,
   itself newly disclosed as a dearer sibling of `entrepreneurial_lens_ehi/openinsider-scraper`).
   Builds 0.1.22 then 0.1.23 (second fixed an UNDATED flag), verified live via the build's own
   `readme` field. All 6 standing checks clean: `check-competitor-claims` 416/0 stale + 87/0
   undated, `check-comparison-breadth` 23/0 narrow, `check-price-superiority` **486/122/0**
   undisclosed, `check-pricing` 24/29/0, `check-charges` 24/24, `check-disclosure` 0 missing.
   `audit_dates.json` updated via a standalone `state/.update_audit.py` (deleted after running) —
   `git diff --stat` confirmed a clean 7-line diff, key-set + per-key comparison against
   `git show HEAD:` confirmed only this Actor's keys changed. $0 spent (read-only Store/Actor API
   reads, 2 README-only builds, no Actor runs). Services verified: 3 systemd units active,
   `/health` + `/tools/sec-insider-trades-scraper` + `/pricing` all 200. Committed and pushed
   (`1e7945a`). Inbox checked — re-read the recurring `bytewells.com` "monthly rentals" email in
   full this cycle: confirmed it is a third-party marketplace's vendor-onboarding pitch (join a
   waitlist, 10% commission, no exclusivity), not a buyer lead — same read as prior cycles, still
   not actionable, no budget line. Rest of inbox is the usual DMARC/backscatter/SEO-submission
   spam. No owner email needed (revenue still $0). **New fleet-oldest `competitor_audit` is
   `google-play-reviews-scraper` (1146)**.

SUPERSEDED-BY-1169 (was NEXT-CYCLE (1169)): **The 2026-10-04 watch items are NOW DUE (parseforge/harris-county restructure at
   2026-10-04T00:02:22Z, jungle_synthesizer/euipo TED entry at 2026-10-04T09:23:18Z) — do them FIRST, ahead
   of the audit rotation**, exactly as described in the un-renumbered paragraph further below. Cycles 1161/1160
   already published the post-change numbers in both READMEs, so this is a **live re-read + tense flip, NOT a
   re-derivation**: confirm each entry's values on the live record, flip the README's "will change on
   2026-10-04" wording to past tense, push a README-only build and verify it via the build's own
   `actorDefinition.readme` field. If the cycle somehow starts before 09:23:18Z, do the harris-county one
   (already past) and leave euipo for the next run. **After the watch items, resume the fleet-oldest
   `competitor_audit` rotation at `sec-insider-trades-scraper` (1145)** — `shopify-products-scraper` is now
   current at 1168 (below). Note `sec-insider-trades-scraper` returned only **15** matches on cycle 1125's
   `bin/niche-size` fleet run, the lowest in the fleet and suspiciously low for the niche, so treat the auto
   base term as broken and hand-build a multi-term sweep (form 4 / insider trading / insider transactions /
   sec filings / edgar / officer-director trades …) before trusting any count — then promote the validated
   list into `niche-size`'s `TERM_VARIANTS`.
   **DONE at 1168 (GROWTH/BUILD slot): fleet-oldest `competitor_audit` on `shopify-products-scraper`**
   (1144 -> 1168; neither 10-04 watch item was due at 09:30 UTC on 10-03). **Zero price drift on all 25
   previously-named rivals**; only two user-count moves (`autofacts/shopify` 2302 -> 2304, `webdatalabs/
   shopify-product-scraper` 399 -> 400), both published exactly. **The defect was COMPARISON BREADTH, not
   accuracy** (1104/1108/1140 class): the README published "a sweep of 37 Shopify catalog rivals" and named
   25, but a 12-term sweep saw 500 distinct listings / **397 Shopify-mentioning**; priced 22 never-named
   listings live and named all of them, taking the README from 25 to **46** rivals (grep-verified against the
   published sentence). **Three genuine new undercutters:** `kalirobot/shopify-scraper` (5u) flat
   **$0.00049/product, no start fee at all** -- under our $0.001 Free AND $0.00085 Gold+ rate, cheaper at
   EVERY tier with no crossover; `rover-omniscraper/shopify-scraper` (12u) $0.0009 + $0.0003 start, cheaper
   past ~3 products and the closest new rival on FEATURES too; `scrapesage/shopify-store-scraper` (6u)
   tiered the opposite way from us, $0.002 FREE -> $0.00076 PLAT -> **$0.0005 DIAMOND**, no start fee, so it
   undercuts us on the top two plans only. **Corrected our own start-fee claim**: four rivals with no start
   fee was really NINE. **Priced our watch mode against dedicated rivals for the first time**:
   `scrapebench/shopify-change-tracker` (58u) $0.01 per change detected, `technicaldost/
   shopify-price-delta-monitor` (3u) $0.005/product -- we are ~10x and ~5x cheaper per reported change, and
   neither is a catalog exporter (the real differentiator). **SCOPE RULING — do not undo it:**
   `apivault_labs/woocommerce-product-scraper` (31u) advertises "Shopify CSV & Product Feed | $0.9/1K" in its
   TITLE at $0.0009/product (under our Free rate) but scrapes WOOCOMMERCE and only EXPORTS in Shopify's
   import-CSV format -- correctly NOT named; a future sweep must not add it on the title alone. Same for the
   App Store / lead-email / product-review clusters (none export a catalog). **New watch item, already
   resolved as a no-op:** `fortuitous_pirate/shopify-store-scraper` has a future `pricingInfos` entry
   effective **2026-10-13T00:00:00Z** whose values are key-for-key IDENTICAL to the current one -- dumped and
   compared, **no action needed on that date**. Builds 0.1.72 then 0.1.73 (the second after
   `check-competitor-claims` correctly flagged the novus/bercikgroup bullet UNDATED), verified live via the
   build's own `readme` field. All 6 standing checks clean: `check-competitor-claims` 411/0 stale + 86/0
   undated, `check-comparison-breadth` 23/0 narrow, `check-price-superiority` **482/121/0** undisclosed
   (460 -> 482 comparisons), `check-pricing` 24/29/0, `check-charges` 24/24, `check-disclosure` 0 missing.
   `audit_dates.json` updated via a standalone `state/.update_audit.py` (deleted after running) -- clean
   6-line `git diff --stat`, and a key-set + per-key comparison against `git show HEAD:` confirmed only
   `shopify-products-scraper`'s two keys changed. $0 spent (read-only API reads, 2 README-only builds, no
   Actor runs). 3 services active; `/health` + `/tools/shopify-products-scraper` + `/pricing` all 200. Inbox
   checked -- same spam/backscatter/vendor-pitch pattern, nothing actionable, no owner email (revenue $0).

SUPERSEDED-BY-1168 (was NEXT-CYCLE (1168)): **The 2026-10-04 watch items are DUE or imminent (parseforge/harris-county restructure at
   2026-10-04T00:02:22Z, jungle_synthesizer/euipo TED entry at 2026-10-04T09:23:18Z) — do them FIRST, ahead of
   the audit rotation**, exactly as described in the un-renumbered paragraph a few items below. If still
   before those timestamps, resume the fleet-oldest `competitor_audit` rotation at **`shopify-products-
   scraper` (1144)** — `us-federal-awards-scraper` is now current at 1167 (below).
   **DONE at 1167 (GROWTH/BUILD slot): fleet-oldest `competitor_audit` on `us-federal-awards-scraper`** (1142
   -> 1167; picked off the tie with `fec-campaign-finance-scraper`, already done at 1166). 5-term Store sweep
   (usaspending / federal awards / federal spending / government spending / federal contracts grants, ~90
   distinct listings seen, almost all 1-5-user templated clones). All 6 previously-named rivals re-verified
   live via `pricingInfos`, **zero price drift**; `copious_atoll` 9 users (was 10, a one-user flap the "under
   10 users" wording already covers). `constant_quadruped/research-grant-aggregator` still has no
   `pricingModel`/`pricingInfos` at all (still effectively free) — unchanged. **Three genuine new rivals
   disclosed:** `fortuitous_pirate/usaspending-scraper` (3 users, titled "No Login, $0.93/1k" — the headline
   figure matches its live price) at a flat **$0.00093/result** + $0.001 one-time start fee, the cheapest
   rival on the page at every tier, beating even `copious_atoll` and `themineworks`'s free-plan rate;
   `pink_comic/usaspending-federal-spending-search` (5 users) at a flat **$0.002/result** + $0.0001 start,
   which beats our $0.004 free-plan AND $0.0025 Gold+ rate since it has no tiers; and `haketa/usaspending-
   scraper` (4 users) at $0.004 -> $0.0025 — an **exact tier-for-tier tie** with our own ladder, with fewer
   fields and no sub-award/watch/opportunity-score modes. Build 0.1.53 (package 0.1.12 -> 0.1.13) verified
   live via the build's own `readme` field (all 3 new handles + "nine competitors" present). All 6 standing
   checks clean: `check-competitor-claims` 386/0 stale + 83/0 undated, `check-comparison-breadth` 23/0 narrow,
   `check-price-superiority` **460/119/0** undisclosed, `check-pricing` 24/29/0, `check-charges` 24/24,
   `check-disclosure` 0 missing. `audit_dates.json` updated via a standalone `state/.update_audit.py` script
   (deleted after running) — `git diff --stat` confirmed a clean 6-line diff, and a key-set + per-key
   comparison against `git show HEAD:` confirmed only `us-federal-awards-scraper`'s keys changed, 23 other
   Actors untouched. $0 spent (read-only Store/Actor API reads, 1 README-only build, no Actor runs). Services
   verified: 3 systemd units active, `/health` + `/tools/us-federal-awards-scraper` + `/pricing` all 200.
   Committed and pushed (`884d605`). Inbox checked — same spam/backscatter/vendor-pitch pattern as prior
   cycles, nothing actionable, no owner email needed (revenue still $0). **New fleet-oldest `competitor_audit`
   is `shopify-products-scraper` (1144)**.

SUPERSEDED-BY-1167 (was NEXT-CYCLE (1167)): **The 2026-10-04 watch items are DUE or imminent (parseforge/harris-county restructure at
   2026-10-04T00:02:22Z, jungle_synthesizer/euipo TED entry at 2026-10-04T09:23:18Z) — do them FIRST, ahead of
   the audit rotation**, exactly as described in the un-renumbered paragraph a few items below (cycle 1161/1160
   already published the post-change numbers in both READMEs; this is a live re-read + tense flip, NOT a
   re-derivation). If still before those timestamps, resume the rotation at the new fleet-oldest,
   **`us-federal-awards-scraper` (1142)** — `fec-campaign-finance-scraper` is now current at 1166 (below).
   **DONE at 1166 (QUALITY slot): fleet-oldest `competitor_audit` on `fec-campaign-finance-scraper`** (1142 ->
   1166; picked off the tie with `us-federal-awards-scraper`, both at 1142). 6-term Store sweep (fec campaign
   finance / campaign finance scraper / fec api / political donations / federal election commission / campaign
   contributions scraper). All 4 previously-named rivals re-verified live via `pricingInfos`, **zero price
   drift**: `ryanclinton/fec-campaign-finance` $0.002/record + $0.00005 start, `parseforge/fec-campaign-finance-
   contributions-scraper` $0.0027 FREE -> $0.0018 GOLD+ + tiered-per-GB start, `crawlerbros/fec-campaign-
   finance-scraper` $0.005 FREE -> $0.003 GOLD+ + $0.005 start, `hanamira/political-donations-search`
   $0.004/record + $0.00005 start. **One new tied-for-3rd rival disclosed:** `fortuitous_pirate/fec-spending-
   scraper` (3 users, same count as `crawlerbros`, never named before) is a generic templated scraper at
   $0.00186/result + $0.001 start, dearer than us at every volume — corrects the README's "no other listing
   tops 3 users besides the four now named" sentence, which was false by a tie (completeness/accuracy fix,
   not a competitive threat). Checked its sibling listings (`fortuitous_pirate/fec-donations-scraper`,
   `quarterly_jingo/fec-spending-scraper` + `fec-donations-scraper`, apparent template clones) — all 1-2
   users, same price, no further disclosure warranted. Build 0.1.44 (package 0.1.13 -> 0.1.14) verified live
   via the build's own `readme` field. All 6 standing checks clean: `check-competitor-claims` 382/0 stale +
   83/0 undated, `check-comparison-breadth` 23/0 narrow, `check-price-superiority` **458/117/0** undisclosed,
   `check-pricing` 24/29/0, `check-charges` 24/24, `check-disclosure` 0 missing. `audit_dates.json` updated via
   a standalone `/tmp/update_audit.py` script (deleted after running) — `git diff --stat` confirmed a clean
   3-line diff. $0 spent (read-only Store/Actor API reads, 1 README-only build, no Actor runs). Services
   verified: 3 systemd units active, `/health` + `/tools/fec-campaign-finance-scraper` + `/pricing` all 200.
   Committed and pushed (`4e1826f`). Inbox checked — same spam/backscatter/vendor-pitch pattern (DMARC reports,
   "Collaboration with our Trust" spam x2, two SEO-submission spam, two foreign-language contact-form spam,
   repeat `bytewells.com` rental pitch), nothing actionable, no owner email needed (revenue still $0). **New
   fleet-oldest `competitor_audit` is `us-federal-awards-scraper` (1142).**

SUPERSEDED-BY-1166 (was NEXT-CYCLE (1166)): **The 2026-10-04 watch items are DUE or imminent (parseforge/harris-county restructure at
   2026-10-04T00:02:22Z, jungle_synthesizer/euipo TED entry at 2026-10-04T09:23:18Z) — do them FIRST, ahead of
   the audit rotation**, exactly as described in the un-renumbered paragraph just below (cycle 1161/1160 already
   published the post-change numbers in both READMEs; this is a live re-read + tense flip, NOT a re-derivation).
   If still before those timestamps, skip and resume the rotation at the new fleet-oldest, **`fec-campaign-
   finance-scraper` / `us-federal-awards-scraper` (tied at 1142)** — pick either; `nih-reporter-scraper` is now
   current at 1165 (below).
   **DONE at 1165 (GROWTH/BUILD slot): fleet-oldest `competitor_audit` on `nih-reporter-scraper`** (1140 -> 1165;
   neither 10-04 watch item was due yet at 08:00 UTC on 10-03, so the oldest-first rotation ran as scheduled).
   Re-ran the promoted 7-term niche-size sweep: 51 matching listings, unchanged, README's own count claim still
   MATCHES. Re-priced all 33 previously-named rivals live via `pricingInfos`: **zero price/user-count drift**
   except two flat-vs-tiered misreads fixed (`parseforge/nih-reporter-scraper` $0.0065 flat -> tiered to $0.006
   Gold+; `parseforge/nih-reporter-publications-scraper` $0.0018 flat -> tiered to $0.00163 Diamond — neither
   changes the competitive conclusion, both stay dearer than our $0.0015).
   **Real finding, in our own favour's opposite direction:** `nexgenwatch/nih-reporter-grant-award-delta` was
   missing a mandatory per-run "source-check" fee ($0.1 Free -> $0.067 Gold+) on top of its stated $0.15/delta +
   $0.02 start — it is dearer than we'd said, a correction against our own comparison, not for it.
   **Biggest finding:** `datasignalslab/nih-research-funding-monitor` had been mis-stated as flat "$0.02/row"
   since at least cycle 1140. Its live `pricingInfos` shows the $0.02 `query-analyzed` event (`isPrimaryEvent`)
   is charged **per organization or topic scanned, not per row** — the real per-row event is $0.00001 + a
   $0.00005 start fee — which actually crosses **under** our flat $0.0015/row past ~14 grants returned per scan.
   Moved from the dearer-rivals list into the disclosed-undercutter paragraph with the crossover math shown —
   the same headline-number-trap class as cycle 1164's clinicaltrials audit, this time flattering a mistake we
   fixed anyway (see LEARNINGS item 5). One new never-named rival disclosed: `caffein.dev/grants-actor` (3
   users, NIH RePORTER + Grants.gov + Duke Research Funding in one dataset, $0.002/result + $0.00005 start,
   dearer than us, no threat). `fortuitous_pirate/grants-gov-scraper` (5u, Grants.gov-focused, NIH only as a
   filter value) checked and confirmed correctly out of scope. Build 0.1.34 verified live via the build's own
   `readme` field (all edits present). All 6 standing checks clean: `check-competitor-claims` 380/0 stale + 83/0
   undated, `check-comparison-breadth` 23/0 narrow, `check-price-superiority` **457/117/0** undisclosed,
   `check-pricing` 24/29/0, `check-charges` 24/24, `check-disclosure` 0 missing. `audit_dates.json` updated via a
   standalone `state/.update_audit.py` script (deleted after running) — `git diff --stat` confirmed a clean
   2-line diff, and a key-set + per-key comparison against `git show HEAD:` confirmed only `nih-reporter-
   scraper`'s keys changed, 23 other Actors untouched. $0 spent (read-only Store/Actor API reads, 1 README-only
   build, no Actor runs). Services verified: 3 systemd units active, `/health` + `/tools/nih-reporter-scraper` +
   `/pricing` all 200. Inbox checked — same spam/backscatter pattern plus a `bytewells.com` rental-marketplace
   cold pitch (already noted at 1163), nothing actionable, no owner email needed (revenue still $0). **New
   fleet-oldest `competitor_audit` is `fec-campaign-finance-scraper` / `us-federal-awards-scraper` (tied at
   1142).**

PRIOR-NEXT-CYCLE (1165, superseded above): **The 2026-10-04 watch items are now DUE or imminent — do them FIRST, ahead of the audit
   rotation.** (a) `parseforge/harris-county-court-records-scraper` restructures at 2026-10-04T00:02:22Z (start
   fee $0.005 flat -> tiered $0.02 FREE/$0.015 GOLD+, per-record rate unchanged, new optional
   $0.005->$0.00375 `case-details` event); cycle 1161 already published the exact post-change numbers in
   `court-records-scraper`'s README, so this is a live re-read for confirmation plus a future->present tense
   flip, NOT a re-derivation. (b) `jungle_synthesizer/euipo-trademark-scraper`'s TED entry takes effect
   2026-10-04T09:23:18Z; cycle 1160 already published its post-change numbers, so flip one sentence in
   `trademark-search-scraper`'s README from future to present tense, cheaply. If 1165 still runs before
   00:02:22Z on 10-04, skip both and resume the rotation. **Then resume the fleet-oldest `competitor_audit`
   rotation at `nih-reporter-scraper` (1140, now fleet-oldest)** — note cycle 1108 flagged it as having named
   1 rival of 21 with an unnamed listing at 7.6x the users it called "the niche's Store leader", so expect a
   real finding there. Also newly opened by this cycle: **`labrat011/clinical-trial-site-contact-finder`'s
   start fee rises $0.00005 -> $0.005 on 2026-10-10T17:29:25Z** (per-row $0.0007 unchanged, so it stays
   cheaper than us per site row) — `clinicaltrials-scraper`'s README already states this in future tense;
   after that date it is a one-sentence tense flip. Two standing watch items remain from earlier cycles:
   `fortuitous_pirate` (court-records) 2026-10-13 and both `dev00` trademark listings 2026-10-14.
   **DONE at 1164 (QUALITY slot): fleet-oldest `competitor_audit` on `clinicaltrials-scraper`** (1139 -> 1164).
   Neither 10-04 watch item had arrived (cycle started 07:30 UTC on 10-03). 15-term Store sweep: **203 distinct
   listings, 128 naming clinical trials in their own name/title** — the README had claimed "40+" since cycle
   1104 and now states 128. **Retracted a superlative**: `martc03/nih-clinical-trials` was published as "the
   cheapest listing found anywhere in this niche" but `maximedupre/clinicaltrials-gov` (2u) charges the same
   $0.00001/study with **no start fee at all** (strictly cheaper at every volume) and
   `constant_quadruped/clinical-trials-fda-scraper` (2u) is on Apify's **FREE** model at $0/row while covering
   CT.gov *and* openFDA — the README now carries a dated Correction paragraph, not a quiet edit. **Eight more
   never-named undercutters disclosed**, all cheaper than our $0.0015 at every tier: `copious_atoll`
   ($0.0005 + $0.00005 start), `datalayer/clinical-trials-failure-intel` ($0.001 FREE -> $0.0007 GOLD+, no
   start fee, plus `whyStopped` classification we don't do), `agentictools` + `thriftykiwi` + `brick_joey_yto`
   (flat $0.001, no start fee), `jovian_explorer` + `alleserojje` (flat $0.001 + $0.00005 start), and
   `hipersoft` (cheaper only from BRONZE down, $0.0016 FREE -> $0.0008 GOLD+, plus $0.0005/API-request on top).
   **Headline-number trap now documented in the README itself**: `cblu/clinical-trials-scraper` advertises a
   $0.00001 `apify-default-dataset-item` event but its real per-study charge is a separate `study-record` event
   at **$0.003** (2x our rate) — any price-sorted comparison, including this sweep's own first pass, reads it as
   the niche's cheapest; `hipersoft`'s $0.0005 `api-request` event has the identical shape. **Zero price drift
   and zero user-count drift on all 23 previously-named rivals**, with one near-miss: `GET /v2/store`'s stats
   payload said `bovi` had 4 users while `GET /v2/acts` says 5, and `check-competitor-claims` caught the edit I
   made from the store payload — **the act record is authoritative for a user count, the store search payload
   is not.** Build 0.1.48 (package.json 0.1.9 -> 0.1.10) verified live via the build's own `readme` field (all
   11 new handles + the 128 count + the correction paragraph present). All 6 standing checks clean:
   `check-competitor-claims` 378/0 stale + 83/0 undated, `check-comparison-breadth` 23/0 narrow,
   `check-price-superiority` **456/117/0** undisclosed, `check-pricing` 24/29/0, `check-charges` 24/24,
   `check-disclosure` 0 missing. `audit_dates.json` updated via a throwaway `/tmp/upd.py` (deleted after
   running) that **appends** to the existing `note` and uses `ensure_ascii=True` to match the file's existing
   escaping — the first attempt overwrote the note and flipped `—` to a literal em dash fleet-wide, turning
   a 2-line change into a 6-line diff across two unrelated Actors; reverted and redone, `git diff --stat`
   confirmed a clean 2-line diff. $0 spent (read-only Store/Actor API reads, 1 README-only build, no Actor
   runs). Services verified: 3 systemd units active, `/health` + `/tools/clinicaltrials-scraper` + `/pricing`
   all 200. Inbox checked — same spam/backscatter/vendor-pitch pattern as prior cycles, nothing actionable, no
   owner email needed (revenue still $0). **New fleet-oldest `competitor_audit` is `nih-reporter-scraper`
   (1140).**

PRIOR-CYCLE (1164): **The court-records watch item is DUE 2026-10-04 — whoever runs on/after that date must do
   it FIRST**, ahead of the audit rotation: `parseforge/harris-county-court-records-scraper`'s restructure
   (start fee $0.005 flat -> tiered $0.02 FREE/$0.015 GOLD+, per-record rate unchanged, new optional
   $0.005->$0.00375 `case-details` event) takes effect 2026-10-04T00:02:22Z. Cycle 1161 already read the filed
   entry and published the exact post-change numbers in `court-records-scraper`'s README, so 2026-10-04's job
   is a live re-read for confirmation and a tense flip (future -> present), NOT a re-derivation. The same cycle
   should also re-read the `jungle_synthesizer/euipo-trademark-scraper` TED entry (effective
   2026-10-04T09:23:18Z, see the 1160 note) and, **cheaply**, flip one sentence in `trademark-search-scraper`'s
   README from future to present tense — cycle 1160 already published the exact post-change numbers, so that
   too is a tense edit and a live re-read for confirmation, NOT a re-derivation. Otherwise resume the
   fleet-oldest `competitor_audit` rotation at **`clinicaltrials-scraper` (1139, now fleet-oldest)**.
   **DONE at 1163 (GROWTH/BUILD slot): fleet-oldest `competitor_audit` on `ats-jobs-scraper`** (1138 -> 1163).
   8-term `apify-admin store` sweep (ats jobs / greenhouse lever ashby / multi-ats scraper / job board scraper /
   greenhouse jobs scraper / ashby jobs scraper / workday jobs scraper / recruitee workable) against the 13
   previously-named rivals plus 10 new candidates, live `pricingInfos` pulled for all. **Three genuine new
   undercutters disclosed, each beating everything previously named in this niche:**
   `openclawai/career-site-ats-jobs-scraper` (16u) auto-detects 60+ ATSes including all 7 of ours at a flat
   $0.0005/job with **no start fee** — a third of our FREE rate and still half our GOLD+ rate, at every
   volume, though it does no department/location normalisation and has no salary-aware watch mode.
   `fetch_cat/ats-jobs-scraper` (8u, 5 new/30d, 407 successful runs that period) covers 6 of our 7 ATSes
   (Personio instead of Workable, no Workday) at $0.005 start + tiered $0.000115/job (FREE) down to
   $0.000028/job (DIAMOND) — crosses our no-start-fee FREE rate at ~4 jobs/run, 35x cheaper than our DIAMOND
   rate at scale; its own start fee is the only thing keeping it from beating us on literally every job.
   `wickfeed/ats-job-aggregator` (21u) covers 5 of our 7 ATSes at a flat $0.001/job, no start fee, plus an
   optional pay-only-for-new-jobs diff/monitor mode — cheaper at FREE/BRONZE/SILVER, ties at GOLD+. All 13
   previously-named rivals re-verified live, **zero price drift**; user-count drift corrected on 6
   (`webdata_labs` 66->68, `k1ra` 45->47, `i-scraper` 41->42, `bovi` 473->476, `jobo.world` 759->763, `memo23`
   197->200). Build 0.1.60 (package.json 0.1.11->0.1.12) verified live via the build's own `readme` field (all
   3 new handles + corrected counts + updated date present). All 6 standing checks clean:
   `check-competitor-claims` 367/0 stale + 82/0 undated, `check-comparison-breadth` 23/0 narrow,
   `check-price-superiority` **446/109/0** undisclosed, `check-pricing` 24/29/0, `check-charges` 24/24,
   `check-disclosure` 0 missing. `audit_dates.json` updated via a standalone `state/.update_audit.py` script
   (deleted after running, per the 1159-1162 lesson) — `git diff --stat` confirmed a clean 2-line diff, and a
   key-set + per-key comparison against `git show HEAD:` confirmed only this Actor's `competitor_audit`/`note`
   keys changed, 23 other Actors untouched. $0 spent (read-only Store/Actor API reads, 1 README-only build,
   no Actor runs). Services verified: 3 systemd units active, `/health` + `/tools/ats-jobs-scraper` + `/pricing`
   all 200. Inbox checked — same spam/backscatter/vendor-pitch pattern as prior cycles plus a new
   `bytewells.com` cold pitch (rental-billing marketplace soliciting us to list there) — not actionable, no
   budget line, no owner email needed (revenue still $0). **New fleet-oldest `competitor_audit` is
   `clinicaltrials-scraper` (1139)**.
   **DONE at 1162 (QUALITY slot): fleet-oldest `competitor_audit` on `uk-find-a-tender-scraper`** (1136 -> 1162).
   15-term niche-size sweep (hand-curated at 1100): 87 matching listings, README's own "86" claim within normal
   one-day churn, updated to 87. Top 10 by users all already named — no large missed rival this time, a sign
   the niche's `TERM_VARIANTS` curation from cycles 1047/1100 is still holding. **One genuine new undercutter:**
   `accountable_eel/uk-tender-alerts` (2 users, never named before) is a dual-portal (FTS+CF) monitoring/alerts
   product tiered $0.003/notice FREE down to $0.0015 GOLD+ plus a $0.00005 start fee — crosses under our
   $0.003->$0.0025 tiered rate at ~280 rows on Bronze, ~100 on Silver, ~63 on Gold and above (our 25-free-row
   allowance keeps us ahead on the Free tier itself, so it is not an across-the-board beat like `deriverge`).
   **9 more never-named rivals disclosed for completeness**, all dearer at every realistic volume: 6
   single-portal Find-a-Tender-only listings (`nexgenwatch/uk-fts-tender-award-watch`,
   `civicrows/uk-find-a-tender-notices` — an FTS-only sibling of the already-named `civicrows/uk-unified-
   tender-feed`, `fortuitous_pirate/uk-find-a-tender-scraper`, `ukopendata/uk-public-tenders-find-a-tender`,
   `kaz_kakyo/uk-tender-notices`, `ausgovdata/uk-find-a-tender`) and 3 multi-country Contracts-Finder-only
   aggregators that happen to touch the UK among several other countries (`jungle_synthesizer/eu-national-
   procurement-portals-scraper`, `parseforge/us-gov-contract-watch-scraper`, `georgy.malanichev/govtender-
   scraper`). Zero price/user-count drift found on any of the 28 previously-named rivals. Build 0.1.52 verified
   live via the build's own `readme` field (all 10 new handles + both updated dates present). All 6 standing
   checks clean: `check-competitor-claims` 364/0 stale + 82/0 undated, `check-comparison-breadth` 23/0 narrow,
   `check-price-superiority` **443/107/0** undisclosed, `check-pricing` 24/29/0, `check-charges` 24/24,
   `check-disclosure` 0 missing. `audit_dates.json` updated via a standalone `state/.update_audit.py` script
   (deleted after running, per the 1159/1160/1161 lesson) — `git diff --stat` confirmed a clean 2-line diff, and
   a key-set + per-key comparison against `git show HEAD:` confirmed only this Actor's `competitor_audit`/
   `competitor_audit_note` keys changed, 23 other Actors untouched. $0 spent (read-only Store/Actor API reads,
   1 README-only build, no Actor runs). Services verified: 3 systemd units active, `/health` +
   `/tools/uk-find-a-tender-scraper` + `/pricing` all 200. Inbox checked — same spam/backscatter/vendor-pitch
   items as prior cycles, nothing actionable, no owner email needed (revenue still $0). **New fleet-oldest
   `competitor_audit` is `ats-jobs-scraper` (1138)**.
   **DONE at 1161 (GROWTH/BUILD slot): fleet-oldest `competitor_audit` on `court-records-scraper`** (1134 -> 1161).
   5-term Store sweep (`court records`/`courtlistener`/`pacer`/`docket`/`case law`, 60-result limit per term).
   All 12 previously-named rivals re-verified live via `pricingInfos`: **zero price drift and zero user-count
   drift on every single one** — `nexgendata/court-records-search` 61u, `automation-lab/court-records-scraper`
   71u, `fortuitous_pirate/courtlistener-legal-data` 21u, `parseforge/harris-county-court-records-scraper` 28u,
   `fortuitous_pirate/florida-court-records-scraper` 14u, `andrew_avina/pacer-intelligence-mcp` 13u,
   `pink_comic/bankruptcy-filing-search` 23u, `seibs.co/court-records-intel` 11u, `martc03/court-records-mcp`
   33u, `themineworks/courtlistener-court-records` 10u, `pink_comic/recap-federal-court-dockets` 15u,
   `haketa/federal-court-records-scraper` 9u. Both filed-but-not-yet-effective future changes read live and
   confirmed byte-accurate against what the README already says prospectively (the `parseforge/harris-county`
   2026-10-04 restructure above, and `fortuitous_pirate`'s 2026-10-13 start-fee cuts on both its
   `courtlistener-legal-data` and `florida-court-records-scraper` listings).
   **Six never-named rivals disclosed.** Five dearer-for-completeness: `maydit/us-court-cases-scraper` (4u,
   "PACER Alternative API", tiered $0.003->$0.0018/record + $0.00005 start); `alwaysprimedev/courtlistener-scraper`
   (6u, 3 new/30d, flat $0.0025/record + $0.00005 start); `nexgendata/courtlistener-federal-docket-scraper` (13u)
   — the RECAP-dockets-only sibling of the already-named `nexgendata/court-records-search`, same $0.00005 start
   fee and the identical flat $0.10/record rate; `pink_comic/courtlistener-legal-opinions` (6u) — the
   opinions-only sibling of the already-named `pink_comic/recap-federal-court-dockets`, same $0.0001 start fee
   and the identical flat $0.002/record rate that ties us; `parseforge/business-bankruptcy-filings-scraper`
   (11u, same vendor pattern as `parseforge/harris-county`, bankruptcy-only RECAP slice at $0.005 start + tiered
   $0.01599 FREE -> $0.01199 GOLD+). **One genuine partial undercutter, not previously named:**
   `scrapesage/court-records-scraper` (4u) splits dockets and opinions into separate tiered charge events with
   **no start fee** — opinions taper $0.004 (Free) -> $0.001 (Diamond), dockets taper $0.006 (Free) -> $0.0015
   (Diamond) — crossing under our flat $0.002/record on opinions from Platinum up ($0.00152, $0.001) and on
   dockets only at Diamond ($0.0015); every tier below that stays pricier than us on both record types. It also
   prices three record types this Actor does not offer at all — judge/judicial-profile, oral-argument and
   financial-disclosure records, each its own tiered event $0.00125-$0.005. The README's "What we do not claim"
   section now names `scrapesage` alongside `themineworks` as a rival that beats us on a paid Apify plan, for
   part of its range.
   Build **0.1.43** verified live via the build's own `readme` field (all 6 new handles, both future-change
   sentences, and the 2026-10-03 verification dates all present — the first push, 0.1.42, tripped
   `check-competitor-claims`'s UNDATED check on one of the two edited paragraphs; fixed by adding an inline date
   and re-pushed as 0.1.43, same gotcha item 6/item-9-class already documents). All 6 standing checks clean:
   `check-competitor-claims` **354**/0 stale + **81**/0 undated, `check-comparison-breadth` 23/0 narrow,
   `check-price-superiority` **433/106/0** undisclosed, `check-pricing` 24/29/0, `check-charges` 24/24,
   `check-disclosure` 0 missing. `audit_dates.json` updated via a standalone `state/.update_audit.py` script
   (per the 1159/1160 lesson — note text has backticks/`$`-prices), matched the existing `indent=2`,
   `git diff --stat` confirmed a clean 2-line diff, and a key-set + per-key comparison against `git show HEAD:`
   confirmed only `court-records-scraper`'s `competitor_audit`/`competitor_audit_note` keys changed, the script
   deleted after running. $0 spent (read-only Store/Actor API reads, 2 README-only builds, no Actor runs).
   Services verified: 3 systemd units active, `/health` + `/tools/court-records-scraper` + `/pricing` all 200.
   Inbox checked — same 10 spam/backscatter/vendor-pitch items as prior cycles, nothing actionable, no owner
   email needed (revenue still $0). **New fleet-oldest `competitor_audit` is `uk-find-a-tender-scraper` (1136)**.
   **NEW WATCH ITEM (opened 1160, due on/after 2026-10-14):** both `dev00` trademark listings have the
   same change filed for 2026-10-14 — `dev00/uspto-trademark-api`'s `trademark-verify` goes from a flat
   $0.003 to tiered **FREE $0.10 / BRONZE+ $0.003**, and the sibling `dev00/uspto-trademark-text-check-api`
   (3u, $0.005, named in our README for the first time at 1160) carries the identical change. It is a
   FREE-plan-only 33x increase with paid tiers untouched — `trademark-search-scraper`'s README already
   says exactly that prospectively; on/after 2026-10-14 re-read both live `pricingInfos` and flip the
   tense. Do not read it as a general price rise across their plans.
   **DONE at 1160 (QUALITY slot): fleet-oldest `competitor_audit` on `trademark-search-scraper`**
   (1132 -> 1160). The court-records watch item is due 2026-10-04 and had not arrived, so the rotation ran
   as scheduled. 20-term strict sweep re-confirmed the niche at **84 real trademark listings** (520 distinct
   seen), identical to 1132, so the README's own count claim still MATCHES live. Live in-effect
   `pricingInfos` pulled for **all 30 named rivals AND all 54 never-named listings** — the second half is
   what produced most of this cycle's findings.
   **One superlative retracted:** `parseforge/tmview-trademarks-scraper` was published as "the dearest way
   to buy this data per row". False — `nexgendata/euipo-esearch-trademarks` ($0.10/trademark), which our own
   README already names one paragraph later, and the newly-found `nexgendata/trademark-patent-search-api`
   ($0.05–$0.15/record) are both dearer. Rescoped to "the dearest of the TMview-based listings", which is
   true, with the correction stated in place rather than silently swapped. **Note the shape of this defect:
   the contradicting rival was already named in our own file** — no price check we own compares two rivals
   against each other, only each rival against us, so an internally inconsistent superlative is invisible to
   all six standing checks by construction. Worth looking for on other READMEs that rank rivals.
   **Two price errors fixed on `sian.agency/uspto-trademark-scraper`, both of which had been in OUR favour**
   (the class `check-price-superiority` cannot detect, same as 1156's `orgupdate` overstatement): its record
   price reaches $0.0015 on **GOLD** as well as PLATINUM/DIAMOND (we said top two plans only, understating
   its undercut by a whole plan), and its start fee is **tiered $0.05 on FREE / $0.005 BRONZE+**, not the
   flat $0.005 we quoted. Also corrected `automation-lab`'s FREE rate $0.0000354 -> $0.0000355 (live
   3.5454e-05, a truncation not a drift).
   **Three new multi-office rivals disclosed — the first ever added to the group our README calls "the only
   group doing the same job as this Actor"**, all dearer than us: `s-r/trademark-search` (2u, USPTO + TMview
   + Madrid + IP Australia in one listing, flat $0.006/trademark with no start fee, 3x ours — the closest
   never-named structural match we have found in this niche), `everyotherfriday/trademark-search` (2u, reads
   TMview and USPTO directly for US/EU/UK, $0.008/record no start, 4x ours), and
   `nexgendata/trademark-patent-search-api` (1u, the widest listing in the niche by source count at 18
   registries — but **one source per run**, not all in one result set — $0.05 for a USPTO trademark and $0.10
   for an EUIPO one plus a $0.005 start, 25–50x our row rate).
   **Watch item resolved EARLY, by reading the filed entry a day before it lands:**
   `jungle_synthesizer/euipo-trademark-scraper`'s change effective **2026-10-04T09:23:18Z** moves AGAINST the
   buyer — FREE/BRONZE $0.002, SILVER $0.0018 and GOLD $0.0016 untouched, while PLATINUM rises $0.0014 ->
   $0.0016 and DIAMOND rises $0.0012 -> $0.0016, flattening the top three tiers onto one price. Its $0.10
   start is unchanged, so the volume at which it undercuts us moves from ~125 rows out to **~250 rows**,
   DIAMOND only. The README now carries those exact numbers prospectively, which is why 1161's job here is a
   tense flip and not an audit.
   **Completeness confirmed, with a trap recorded:** none of the 54 never-named listings undercuts our $0.002
   per returned trademark, so the 7-undercutter set published in the README is still the full set. **Three of
   the 54 do carry a sub-$0.002 charge event and none of them is a row price** —
   `luminar/uspto-trademark-monitor` bills $0.000475 for an *unchanged*-target watch check while its actual
   record price is $0.01425; `technicaldost/uspto-trademark-status-monitor` $0.0005 for a single known-serial
   status check against $0.003/record; `zentrafoundry/uspto-trademark-patent-watcher` $0.0001 for internal
   bookkeeping events against $0.01 per matched record. This is precisely the min-across-events collapse
   `check-price-superiority` documents as a blind spot, so all three are disclosed in the README with the
   reasoning rather than either ignored or miscounted as undercutters. **If a future cycle names any of
   those three, do not quote the cheap event as their price.**
   User-count drift corrected on 4 rivals (`memo23` 27->29, `nexgendata/euipo-esearch` 37->38,
   `scrapers_lat/tmview` 9->10, `sian.agency` 29->30). Build **0.1.29** verified live via the build's own
   `readme` field (all 3 new handles, both corrected tier sentences, the 250-row figure and the 54-listing
   completeness sentence all present). All 6 standing checks clean: `check-competitor-claims` **348/0** stale
   + **80/0** undated, `check-comparison-breadth` 23/0 narrow, `check-price-superiority` **427/106/0**
   undisclosed, `check-pricing` 24/29/0, `check-charges` 24/24, `check-disclosure` 0 missing.
   `audit_dates.json` updated via a standalone `state/.update_audit.py` script file per the 1159 shell-quoting
   lesson (note text is full of backticks and `$`-prefixed prices) — and note a **second formatting trap hit
   this cycle**: the first run wrote the file with `json.dump(..., indent=1)` when the file is `indent=2`,
   which reformatted all 244 lines and buried the real 2-line change in a whole-file diff. Caught via
   `git diff --stat`, reverted with `git checkout`, redone with `indent=2` -> a clean 2-line diff. A
   key-set + per-key comparison against `git show HEAD:` confirmed only this Actor's
   `competitor_audit`/`note` fields changed, 24 other Actor keys untouched. **Match the existing indent when
   rewriting a JSON state file, and always read `git diff --stat` before committing one.**
   $0 spent (read-only Store/Actor API reads, 1 README-only build, no Actor runs). Services verified: 3
   systemd units active, `/health` + `/tools/trademark-search-scraper` + `/pricing` all 200. Inbox checked —
   same 10 spam/backscatter/vendor-pitch items as 1159, nothing new, nothing actionable, no owner email
   needed (revenue still $0). **New fleet-oldest `competitor_audit` is `court-records-scraper` (1134)**,
   which is also the Actor the 2026-10-04 watch item is about — those two jobs are the same Actor and should
   be done together next cycle.
   **DONE at 1159 (GROWTH/BUILD slot): fleet-oldest `competitor_audit` on `sam-gov-opportunities-scraper`**
   (1130 -> 1159). Re-swept `sam.gov` with the Store search `limit` bumped from the default 20 to 60 —
   **54 listings came back instead of 18**, almost all 2-user micro-listings that relevance ranking had
   been cutting off (a narrower-but-different flavor of the item-4 enumeration-cap bug: this time the tool's
   *limit*, not the search term, was capping the count). All 13 previously-named rivals re-verified live
   straight from `pricingInfos`, **zero price drift**. Found one filed-but-not-yet-effective change:
   `fortuitous_pirate/sam-gov-scraper`'s Actor-start fee drops $0.01 -> $0.005 on **2026-10-13** (per-row
   $0.003 unchanged) — still pricier than us after the cut, no competitive-position change, re-read on/after
   that date. **Three genuine new undercutters disclosed**, all 2-user listings surfaced only by the widened
   limit: `yourwingman/usa-federal-contracts-scraper` ($0.0005/row flat + $0.00005 start — a third of our
   rate at every volume, the 3rd-biggest undercut in this niche after `jungle_synthesizer`/`scrapesage`),
   `factpipe/sam-gov-contracts` (tiered $0.002 FREE -> $0.0014 GOLD+, no start fee, undercuts from GOLD+),
   `bakos_bence/sam-gov-opportunities` (tiered $0.00249 -> $0.001245 but behind a $0.02 -> $0.003 start fee,
   crosses our flat rate only past ~12 rows/run on GOLD+). **Two exact ties disclosed:**
   `adobeflex/sam-opportunities-lite` ($0.0015/row primary event, though a separate $0.001 "search run" event
   plus a $0.00005 start fee make it dearer in practice) and `andrew_avina/federal-contracts-mcp` (flat
   $0.0015/row, no other fees — a genuine tie). **Checked and deliberately left unpriced as out of this
   Actor's 4-dataset SAM.gov scope, not an oversight:** wage-determination-only (`wishbone_data`),
   exclusions-only (`nexgendata`, `maximedupre/sam-gov-exclusions`), contractor lead-gen/registration
   monitoring (`lead.gen.labs`'s 3 listings), a bundled amendment-detection product (`blaidlink`, $0.02-0.03
   per event), and 5 multi-country tender aggregators that only mention SAM.gov in passing alongside EU
   TED/UK (`practicalmodules`, `gazidev`, `chorelet`, `snow_leo_data`, `apeye`). Build 0.1.36 verified live
   via the build's own `readme` field (all 6 new handles + both dates present). All 6 standing checks clean:
   `check-competitor-claims` 344/0 stale + 79/0 undated, `check-comparison-breadth` 23/0 narrow,
   `check-price-superiority` **420/106/0** undisclosed, `check-pricing` 24/29/0, `check-charges` 24/24,
   `check-disclosure` 0 missing. `audit_dates.json` updated via a one-off Python script (not an inline
   backtick-heavy shell string — see the fix note below) — `git diff` confirmed only this Actor's
   `competitor_audit`/`competitor_audit_note` fields changed, 24 other keys untouched.
   **Incidental fleet fix, found while running the standing checks:** `check-competitor-claims`'s
   `live_users()` "gone from the Store" transient (tracked since 1145, recurred 1148) flaked a **3rd time**
   this cycle on an unrelated listing (`artificially/eu-tenders-scraper` in `eu-ted-tenders-scraper`'s
   README) — a direct re-check confirmed it's still live/public/40 users. Per the 1148 note's own
   if-it-recurs-a-3rd-time instruction, added a retry-once (2s pause) around the non-200 case in
   `live_users()` before it declares a listing gone; re-ran the full checker clean (344/0) immediately after.
   Do not re-add manual re-confirmation for this specific flake class going forward — the retry now handles it.
   **Shell gotcha hit and fixed this cycle, worth remembering:** editing `state/audit_dates.json`'s note field
   via `python3 -c "...` inside a double-quoted heredoc let the shell command-substitute every backtick
   (`` `owner/slug` ``) and variable-expand every `$0.00xx` price in the note text before Python ever saw it,
   silently corrupting the JSON value (caught via `git diff` before committing, reverted with `git checkout`,
   redone by writing the update as a standalone `.py` file and running `python3 state/.update_audit.py`
   instead). Any future note text with backticks or `$`-prefixed dollar amounts must go through a script
   file, never an inline `python3 -c "..."` with those characters unescaped.
   $0 spent (read-only Store/Actor API reads, 1 code fix, no Actor runs). Services verified: 3 systemd units
   active, `/health` + `/tools/sam-gov-opportunities-scraper` + `/pricing` all 200. Inbox checked — 1 new item
   since 1158 (`wordpress@co-sol.ca` "CO-Sol Canada Inquiry Confirmation" — backscatter spam, someone used our
   address as a fake sender against a Canadian contact form, same pattern as the Japanese/Italian backscatter
   already in the inbox), nothing actionable, no owner email needed (revenue still $0). **New fleet-oldest
   `competitor_audit` is `trademark-search-scraper` (1132)**.
   **DONE at 1158 (QUALITY slot): fleet-oldest `competitor_audit` on `scholarship-scraper`** (1129 -> 1158).
   11-term `niche-size` sweep re-run (base phrase "scholarship", not yet in `TERM_VARIANTS`): 30 seen, **22
   matching**, identical to 1129 — README claim MATCHES live. All 3 previously-named rivals re-verified live
   from `pricingInfos`, **zero price drift**: `jungle_synthesizer/bold-org-scholarship-database-scraper`
   ($0.10 start + $0.001/record — a filed future `pricingInfos` entry dated 2026-10-04 is byte-identical, no
   change expected), `majestic_fund/the-scholarship-scraper-actor` ($0.0005 start + $0.00035/record, ties our
   rate), `fiery_dream/scholarship-intel` ($0.00005 start + $0.00001/record). **One new entrant, checked and
   deliberately left unnamed:** `rhapsodic_groundhopper/buildher-compass-opportunity-intelligence` (6u, 0u30d)
   collects internships/fellowships/scholarships/bootcamps/hackathons for African women in tech from
   unspecified sources — demographic-targeted, multi-category, not bold.org-specific, and priced at
   $0.2/item + $0.00005 start (~570x our rate) so no threat even in scope; disclosed in the README with
   reasoning (same scope-judgment pattern as 1157's `pink_comic/irs-990` call). A direct "bold.org" Store
   search found no rival beyond the already-named `jungle_synthesizer` listing. Build 0.1.18 verified live via
   the build's own `readme` field (new handle + both new sentences present). All 6 standing checks clean:
   `check-competitor-claims` 344/0 stale + 78/0 undated, `check-comparison-breadth` 23/0 narrow,
   `check-price-superiority` **406/104/0** undisclosed, `check-pricing` 24/29/0, `check-charges` 24/24,
   `check-disclosure` 0 missing. `audit_dates.json` updated — `git diff` confirmed only `scholarship-scraper`'s
   `competitor_audit`/`competitor_audit_note` fields changed (2 lines, 25 Actor keys untouched). **Incidental
   fix found by the standing-checks re-run, unrelated to this niche:** `uk-find-a-tender-scraper`'s README
   claimed `nefes-tools/uk-tenders` has 2 users, live is 3 — one-line fix, build 0.1.51 pushed and verified
   live; did NOT bump that Actor's own `competitor_audit` date since it was a drift fix, not a full re-audit.
   $0 spent (read-only Store/Actor API reads, 2 README-only builds, no Actor runs). Services verified: 3
   systemd units active, `/health` + `/tools/scholarship-scraper` + `/pricing` all 200. Inbox checked — same
   10 spam/backscatter/vendor-pitch items as prior cycles, nothing actionable, no owner email needed (revenue
   still $0). **New fleet-oldest `competitor_audit` is `sam-gov-opportunities-scraper` (1130)**.
   **DONE at 1157 (GROWTH/BUILD slot): fleet-oldest `competitor_audit` on `grants-gov-scraper`** (1128 -> 1157).
   15-term `niche-size` sweep re-run (already hand-curated at 1128): still **84 listings**, README's own
   claim MATCHES live. All 12 previously-named rivals re-verified live from `pricingInfos`, **zero price
   drift**. **One inaccuracy fixed, no competitive-position change:** `shahidirfan/Grants-gov-Scraper` and
   `chorelet/government-tenders-scraper` were grouped as flat "$0.001/row behind a start fee" but are
   actually TIERED (shahidirfan $0.001->$0.0008; chorelet $0.001->$0.0007 base row + a separate detail event
   $0.002->$0.0014) — reworded, both remain at/below our $0.0015 enriched rate at every plan either way.
   **Five never-named rivals disclosed, all dearer:** `scrapepilot/grant-foundation-opportunities-scraper`
   (11u, genuinely reads Grants.gov among other portals, thin 6-field export, $0.004 + a steep $0.05 start,
   just switched off a flat $7.99/mo subscription on 2026-09-24), `fortuitous_pirate/grants-gov-scraper`
   (5u, exact-name rival, own title advertises "$4.38/1k" = $0.004375 + $0.001 start),
   `parseforge/grants-gov-scraper` (4u, exact-name rival, tiered result $0.0075->$0.007 + detail
   $0.005->$0.00445), `aurumworks/us-federal-grant-scraper` (14u, flat $0.009 + $0.0005 start),
   `signalcrawl/federal-grant-fit-finder` (6u, 3 new/30d — fastest-growing in this comparison — a
   scored-match product like the already-named `fiery_dream/scholarship-intel`, $0.002 + $0.00005 start).
   **Checked, deliberately left unnamed:** `pink_comic/irs-990-nonprofit-search` (24u, the biggest unpriced
   listing this sweep turned up) reads IRS Form 990/ProPublica charity filings for KYB/EIN lookup — a
   different data source for a different question than Grants.gov opportunity search, despite name-dropping
   Grants.gov in its own listing copy — a scope judgment, not an oversight; do not mistake it for a miss on
   a future audit. Build 0.1.45 verified live via the build's own `readme` field. All 6 standing checks
   clean: `check-competitor-claims` 343/0 stale + 77/0 undated, `check-comparison-breadth` 23/0 narrow,
   `check-price-superiority` **406/103/0** undisclosed, `check-pricing` 24/29/0, `check-charges` 24/24,
   `check-disclosure` 0 missing. `audit_dates.json` updated — **caution for future cycles:** only the
   `grants-gov-scraper` object's `competitor_audit`/`competitor_audit_note` keys were touched; an earlier
   attempt this cycle wrote a whole-object replacement that would have silently deleted that Actor's
   `enum_audit`/`varied_test`/`watch_subset_audit` history, caught via `git diff` before committing and
   reverted with `git checkout` — always merge into the existing per-Actor object, never overwrite it
   wholesale. $0 spent (read-only Store/Actor API reads, 1 README-only build, no Actor runs). Services
   verified: 3 systemd units active, `/health` + `/tools/grants-gov-scraper` + `/pricing` all 200. Inbox
   checked — same 10 spam/backscatter/vendor-pitch items as prior cycles, nothing actionable, no owner email
   needed (revenue still $0). **New fleet-oldest `competitor_audit` is `scholarship-scraper` (1129).**
   **NEW WATCH ITEM (opened 1156, due on/after 2026-10-14):** `flash_scraper/remote-job-aggregator` has a
   pricing change already filed on the platform effective **2026-10-14** — its ladder stops falling at
   $0.0021/job from Gold up instead of reaching $0.0015 on Diamond, and a $0.00005 start fee is added, so it
   gets **dearer**. `remote-jobs-scraper`'s README already states this prospectively; on/after 2026-10-14
   re-read the live `pricingInfos` and flip that sentence from future to present tense. Note its own
   `reasonForChange` says "Per-job prices unchanged", which its own live ladder contradicts — do not trust a
   rival's change note over the ladder.
   **DONE at 1156 (QUALITY slot): fleet-oldest `competitor_audit` on `remote-jobs-scraper`** (1126 -> 1156).
   **Tooling first:** promoted the niche into `bin/niche-size` `TERM_VARIANTS` (15 hand-read terms) and widened
   `MATCH_SYNONYMS` with all six board names (`we work remotely`/`weworkremotely`/`remoteok`/`remote ok`/
   `himalayas`/`jobicy`/`remotive`/`arbeitnow`/`working nomads`) plus `remote work` and `work from home` —
   **246 -> 393 matched of 658 distinct listings seen**. Root cause is the item-4 class again: the base phrase
   `"remote jobs"` is two contiguous words, and every rival in this niche names itself after a specific board, so
   a listing titled "WeWorkRemotely Job Scrapper" matched nothing. All 12 previously-named rivals re-verified
   live straight from `pricingInfos`, 11 with zero drift (`hirebase` 136 -> 135 users, a 1-user delta left
   corrected while in the file).
   **One real overstatement retracted, and it was in our favour:** `orgupdate/remote-co-jobs-scraper` was
   published at "$0.14–$0.2 per record … 100x+ pricier than any row on this page" but live is **$0.012/record
   + $0.02 start** — roughly a tenth of the figure we printed. Still the dearest single-board reader on the page,
   but 8–12x us, not 100x+. Overstating a rival's price flatters our own comparison, so the README now carries
   the correction explicitly rather than a silent number swap.
   **One unqualified claim broken by a new undercutter:** `code-node-tools/job-listings-scraper` (54 users, **28 of
   them new in 30 days — the fastest-growing listing anywhere in this comparison**) reads 180+ boards and ATS
   platforms (Greenhouse, Lever, Workday, Ashby, **RemoteOK**, hh.ru …) at $0.001 -> $0.0007 + $0.00005 start:
   **below us at EVERY tier.** The "cheapest multi-board aggregator" claim is now scoped to *remote-specific*
   aggregators and that exception is argued openly in its own paragraph (it has no remote filter, no cross-board
   dedup and no normalized salary scale — but it wins on price-per-row and we say so).
   **Disclosed undercutters went 2 -> 6.** Added `code-node-tools` (every tier), `delightful_unicorn/remote-jobs-aggregator`
   (17u, flat $0.001 + $0.00001 start, 3 boards), `feedforge/remote-jobs-scraper` (7u, flat $0.001 + $0.00005 start,
   4 boards) and `newbs/RemoteOk-Premium-Job-Scraper` (102u but **0 new in 30 days**, flat $0.001, no start fee,
   RemoteOK only) alongside the already-named `nivlekk` and `hyperbach`. Also noted `scrapesage/remote-jobs-scraper`
   (9u, 7 boards) which starts at $0.004 and steepens to **exactly our $0.001 on Diamond**.
   **Three big never-named listings disclosed:** `lenient_grove/Daily-Job-Pulse-Multi-Source-Job-Opportunity-Aggregator`
   (**618 users — the 4th-biggest listing in the whole sweep**, 25+ general platforms incl. LinkedIn/Indeed/Glassdoor/
   RemoteOK, $0.08 -> $0.05/result = **33–53x us, the dearest listing found in this niche**),
   `logiover/himalayas-remote-jobs-scraper` (316u, a second Himalayas-only reader, $0.003 -> $0.0021 + $0.00005 start)
   and `parsebird/wwr-jobs-scraper` (302u, We Work Remotely — a 7th board we do **not** read — $0.004/listing +
   $0.035/full detail). Nine more checked-and-dearer handles listed compactly (`scrapemint` 45u, `nomad-agent/
   remote-boards-scraper` 16u whose $0.005 start fee is **not** flagged one-time so it bills per GB,
   `nexgendata/job-market-mcp-server` 13u, `nomad-agent/ml-ai-dev-bundle` 10u, `cancap` 8u, `charliemorrisondev` 8u,
   `actorworks` 6u, `straightforward_hydra` 5u, `techforce.global` 4u).
   Build **0.1.31** verified live via the build's own `readme` field (all 10 probe strings present). All 6 standing
   checks clean: `check-competitor-claims` 337/0 stale + 76/0 undated, `check-comparison-breadth` 23/0 narrow,
   `check-price-superiority` **401 compared / 104 cheaper / 0 undisclosed**, `check-pricing` 24/29/0,
   `check-charges` 24/24, `check-disclosure` 0 missing. `audit_dates.json` -> 1156. $0 spent (read-only Store/Actor
   API reads, 1 README-only build, no Actor runs). Services verified: 3 systemd units active, `/health` +
   `/tools/remote-jobs-scraper` + `/pricing` all 200. Inbox checked — same 10 spam/backscatter/vendor-pitch items,
   nothing actionable, no owner email needed (revenue still $0). **New fleet-oldest `competitor_audit` is
   `grants-gov-scraper` (1128).**
   **DONE at 1155 (GROWTH/BUILD slot): fleet-oldest `competitor_audit` on `federal-register-scraper`**
   (1124 -> 1155). Re-ran the existing 15-term `niche-size` sweep (already hand-curated at cycle 1124):
   90 matching listings, unchanged, README's own "about 90 Store listings" claim still MATCHES live.
   All 14 previously-named rivals re-verified live straight from `pricingInfos`: **one real inaccuracy
   fixed** — `nexgensignal/federal-rulemaking-records` was described alongside `nexgendata` as flat
   $0.05/row, but it is actually TIERED, FREE $0.05 down to GOLD-and-above $0.0335 (still far dearer than
   us everywhere, no competitive-position change). **Four never-named rivals disclosed**, surfaced by
   reading the niche-size top-by-users list rather than trusting the stale 2026-10-02 pricing paragraph
   alone: `ryanclinton/federal-register-search` (14 users, 1 new/30d — **the single biggest listing in
   this niche by users**, bigger than every rival already named on the page — $0.002/doc + $0.00005
   start, 2.5x us), `pink_comic/federal-register-search` (6u, $0.002/row + $0.0001 start), `benthepythondev/
   federal-register-intelligence` (4u, tiered $0.002->$0.0014), `ai_solutionist/regulatory-intelligence-api`
   (3u, $0.002/row + $0.005 start, a different product — AI-enriched regulation summaries with RAG chunks,
   not a plain document export). None of the four undercut us. Build 0.1.33 verified live via the build's
   own `readme` field. All standing checks clean: `check-competitor-claims` 319/0 stale + 75/0 undated,
   `check-comparison-breadth` 23/0 narrow, `check-price-superiority` 383/99/0 undisclosed, `check-pricing`
   24/29/0, `check-charges` 24/24. `audit_dates.json` -> 1155. $0 spent (read-only Store/Actor API reads,
   1 README-only build, no Actor runs). Services verified: 3 systemd units active, `/health` +
   `/tools/federal-register-scraper` + `/pricing` all 200. Inbox checked — same spam/backscatter/vendor-
   pitch items as prior cycles (dmarc reports, 2 SEO-submission spam, a repeat "Collaboration with our
   Trust!!" phish, a Japanese/Italian contact-form auto-reply backscatter pair), nothing actionable, no
   owner email needed (revenue still $0). **New fleet-oldest `competitor_audit` is `remote-jobs-scraper`
   (1126).**
   **DONE at 1154 (QUALITY slot): fleet-oldest `competitor_audit` on `substack-scraper`** (1123 -> 1154).
   `niche-size` one-word sweep ("substack", safe base term): 220 seen / 159 matched. All 6 named rivals
   re-verified live, 0 meaningful drift (two sub-1%/sub-10% deltas on `sourabhbgp` u30d and `brilliant_gum`
   total users left unedited per standing tolerance). **Two real inaccuracies fixed, no retraction:**
   `automation-lab/substack-scraper`'s tier floor was wrongly attributed to "Gold and above" when live
   Gold is $0.0012 and only Diamond is $0.00056 (our OWN tiers plateau at Gold, which is presumably where
   the mix-up came from — theirs don't); `fatihtahta/substack-scraper` was called "flat $0.00199 at every
   tier" when live Free is actually $0.0025, only Bronze+ is the flat $0.00199. Both reworded; same
   competitive conclusion (both still dearer than us everywhere) either way. **One new rival disclosed
   for completeness:** `cryptosignals/substack-scraper` (72u, 6u30d, never named) at flat $0.005/result, no
   start fee — dearer than us at every tier. Three easyapi sibling listings (leaderboard-only/
   publications-only/Notes-only, all $0.00299+$0.09 start) checked and deliberately left unnamed — scope
   judgment (single-purpose products, dearer than our equivalent mode wherever we offer the same feature),
   not an oversight. **Flagged but NOT acted on (see LEARNINGS cycle 1154 and item 12 below):**
   `brilliant_gum/substack-insights-scraper`'s live `pricingInfos` marks its own per-entity charge event
   `isOneTimeEvent: true` (same flag as its start fee) — if Apify enforces that literally, its real price
   is a flat ~$0.025/run, not "$0.015/entity" as published, which would make it far cheaper than our README
   currently states ("7x-19x our rate"). Confirming needs a paid test run (no `BUDGET.md` line for probing
   a competitor's Actor) or Apify docs on the flag's runtime behavior — neither done this cycle; see
   LEARNINGS cycle 1154 for the full writeup, revisit if `substack-scraper` comes up again. Build 0.1.49 verified
   live via the build's own `readme` field. All 6 standing checks clean: `check-competitor-claims` 315/0
   stale + 74/0 undated, `check-comparison-breadth` 23/0 narrow, `check-price-superiority` 380/100/0
   undisclosed, `check-pricing` 24/29/0, `check-charges` 24/24, `check-disclosure` 0 missing.
   `audit_dates.json` -> 1154. $0 spent (read-only Store/Actor API reads, 1 README-only build, no Actor
   runs). **New fleet-oldest `competitor_audit` is `federal-register-scraper` (1124).**
   **ALSO NOTE for 1154+: two `jungle_synthesizer` TED listings have a pricing change scheduled for
   2026-10-04** (`eu-national-procurement-portals-scraper` and `ted-eu-procurement-full-scraper`, both
   currently $0.10 start + $0.001/record). Read live on 2026-10-03 the future `pricingInfos` entry was
   byte-identical to the current one (same $0.10 start, same $0.001 primary, `reasonForChange: null`),
   so no README change is expected — but re-read it on/after 2026-10-04 while doing the court-records
   item, since both handles are named in `eu-ted-tenders-scraper`'s README.
   **DONE at 1153 (GROWTH/BUILD slot): fleet-oldest `competitor_audit` on `app-store-reviews-scraper`**
   (1122 -> 1153). This README was already thorough (last touched 1122, verified live 2026-10-02) so this
   audit came back largely clean rather than a retraction. `niche-size` 11-term sweep: 399 seen / 169
   matched. All 9 previously-named rivals (thewolves 2371u, theagents 818u, easyapi 545u, johnvc 484u,
   sourabhbgp 141u, jdtpnjtp 163u, brilliant_gum 160u, code-node-tools 158u, scriptbase 59u) re-verified
   live, **zero price drift**. **One real inaccuracy fixed:** `benthepythondev/appstore-reviews-scraper`
   (152u) was described as "$0.002/review flat" — live `pricingInfos` shows it's actually tiered $0.002
   (FREE) down to $0.0014 (Diamond); reworded, still 14x-20x our rate, no competitive-position change.
   **Three new dearer rivals disclosed for completeness** (none undercut us): `fatihtahta/app-store-
   global-reviews-scraper` (59u, tied with scriptbase, $0.0004/review, 4x ours), `powerai/app-store-
   reviews-scraper-ppr` (34u, 0 new/30d, tiered $0.00499->$0.00199 + a $0.09 start fee), `nexgendata/
   ios-app-store-reviews-scraper` (32u, flat $0.1/review + $0.005 start, ~1,000x our rate, dearest found
   in this niche). Build 0.1.74 verified live via the build's own `readme` field. All 6 standing checks
   clean: `check-competitor-claims` 314/0 stale + 74/0 undated, `check-comparison-breadth` 23/0 narrow,
   `check-price-superiority` 379/100/0 undisclosed, `check-pricing` 24/29/0, `check-charges` 24/24,
   `check-disclosure` 0 missing. `audit_dates.json` -> 1153. $0 spent (read-only Store/Actor API reads,
   1 README-only build, no Actor runs). Committed and pushed (`b54343c`). **New fleet-oldest
   `competitor_audit` is `substack-scraper` (1123).**
   -11. **DONE at 1152 (QUALITY slot): fleet-oldest `competitor_audit` on `eu-ted-tenders-scraper`** (1121 -> 1152).
   **Biggest claim retraction of the rotation so far, and it lands one day after a price cut made on the
   bad data.** Cycle 1151's auto `niche-size` sweep of this niche returned 158 listings / 91 matches; a
   hand-curated 12-term sweep returned **364 listings / 228 matches**, and **all 186 TED/EU-specific ones
   were price-checked live**. Root cause, exactly the item-4 class: the base phrase `"eu ted tenders"` is
   THREE contiguous words that essentially never appear verbatim in a listing's copy, so the niche was
   matching on its two synonyms (`ted europa`, `public procurement`) and nothing else — a listing titled
   "EU Tenders Scraper" whose description says "contract notices from TED" matched neither.
   **Finding: we are NOT the cheapest TED Actor — ~15 listings undercut $0.0015/notice**, most never named.
   Cheaper at EVERY run size: `bikram07/eu-tenders-feed` (1u, Apify **FREE** model, $0/row — the cycle-1104
   lesson again), `westerly_breaker/ted-tender-monitor` (2u, $0.00001/row, ~150x below us),
   `highbrow_qualification_z7w/eu-tenders-monitor` (2u, $0.0001/row, DACH-only scope),
   `getascraper/eu-ted-tender-monitor` (2u, $0.00053 -> $0.0004), `thriftykiwi/eu-ted-tenders-scraper`
   (2u, flat $0.001, **no start fee, no minimum**). Cheaper past a few rows: `vhsgreed/eu-ted-tenders-api-fresh`
   (~2 rows), `guyweitzman/eu-tenders-scraper` and `rod_analytics/ted-tenders` (~3), `soilair/ted-eu-tenders-api`
   + `rigelbytes/eu-tenders-scraper` + `koalastuff/eu-ted-tender-monitor` (~1), `8tp/eu-ted-tender-lot-award-collector`
   (~5), `deriverge/eu-tenders-scraper` (~14, $0.02 run minimum), `logiover/global-public-tenders-scraper`
   (8u, ~14 rows on Gold+), `jungle_synthesizer/eu-national-procurement-portals-scraper` (past ~200 rows),
   `steadydata/eu-tenders` (2u, no start fee, beats us from Gold up). **Published conclusion is now
   "we are not the cheapest EU TED Actor at any run size and we do not intend to compete on price here"**
   — differentiation rests on the documented CPV-subtree behaviour, the complete 22-notice-type/17-procedure-type
   dropdowns, measured fill rates, deadline filtering, watch mode and the duplicate-row charge guard.
   **Explicit decision recorded: do NOT cut this Actor's price again.** The 2026-10-02 $0.003 -> $0.0015 cut
   was made against the 7-rival view; the real distribution has rivals at $0 and $0.00001/row, so no price wins here.
   **Also newly named (not price threats):** `parseforge/ted-eu-procurement-scraper` (15u, the niche's
   5th-biggest listing, never named before, $0.006 -> $0.0055 = ~4x us) and `lofomachines/public-tenders-scraper`
   (74u, 5 new/30d — the **biggest** listing in the broadened sweep, but a 7-country aggregator, not a TED
   reader, and dearer at every tier), plus 14 checked-and-dearer handles (alwaysprimedev, nerdrx, scrapepilot,
   parseforge x2, ikoles, straightforward_hydra, alex_r_ai, siccscha, pappy-dev, euroscrape, mtellez23,
   fuyuki0, nexgendata, omarchydev). All 9 previously-named rivals (foxlabs, dltik, artificially, adobeflex,
   scrapers_lat, memo23, jungle_synthesizer, publicmoney, maximedupre) re-verified live with **0 price drift**.
   **Structural finding worth carrying: this niche is being flooded.** Every undercutter found set its current
   price between 2026-07-06 and 2026-09-29 and has 1-2 users — new cheap entrants are arriving faster than any
   of them gains customers. Expect the same shape in other government-API niches.
   **Tooling improved (verified by re-run):** promoted `eu-ted-tenders-scraper` into `bin/niche-size`
   `TERM_VARIANTS` (12 hand-read terms) AND widened its `MATCH_SYNONYMS` (+`tenders electronic daily`,
   `eu tender`, `european tender`, `eu procurement`, `european procurement`, `ted eu`, `cpv`): 91 -> 228
   matched (119 `--strict`). `federal-register-scraper` re-run as a regression check, unchanged at 90.
   Build **0.1.49** verified live via the build's own `readme` field (all new handles + both retraction
   sentences present; 0.1.48 was the first push, 0.1.49 added `lofomachines` after the widened re-run
   surfaced it). **Incidental fix on an unrelated Actor:** `shopify-products-scraper`'s
   `apivault_labs/shopify-product-scraper` 8 -> 10 users, build 0.1.71 verified live.
   All 6 standing checks clean: `check-competitor-claims` **311**/0 stale + 73/0 undated,
   `check-comparison-breadth` 23/0 narrow, `check-price-superiority` **376**/100/0 undisclosed,
   `check-pricing` 24/29/0, `check-charges` 24/24, `check-disclosure` 0 missing. `audit_dates.json` -> 1152.
   $0 spent (read-only Store/Actor API reads, 3 README-only builds, no Actor runs). Services verified:
   3 systemd units active, `/health` + `/tools/eu-ted-tenders-scraper` + `/pricing` all 200 before and after.
   Inbox unchanged (same 10 spam/backscatter/vendor-pitch items as 1140-1151) — nothing actionable, no reply
   owed, no owner email (revenue flat at $0). **New fleet-oldest `competitor_audit` is
   `app-store-reviews-scraper` (1122).**
   **DONE at 1151 (GROWTH/BUILD slot): fleet-oldest `competitor_audit` on `google-news-scraper`** (1118 -> 1151).
   `niche-size` auto sweep ("google news", 11 queries) surfaced 372 listings, 214 matching. Headline find:
   **`epctex/google-news-scraper` (599 users, 885 builds, 8 reviews/5 stars, 25 bookmarks — bigger than
   both `automation-lab` and `crawlerbros`, already-named undercutters, and never named before) was
   automatically migrated to Apify's FREE pricing model on 2026-10-02 (Apify's rental-sunset
   auto-migration, not a deliberate price cut)** — $0/result at any volume, undercutting this Actor at
   every tier. Its input schema is materially narrower (no topic/section codes, no excludeWords/
   siteFilter/excludeSites, no full-article-text extraction, no ticker extraction, no leaked-date-window
   protection) but it does resolve publisher URLs. Flagged for re-check next audit since an auto-migrated
   FREE price could change if the owner sets their own tiers. Also disclosed 3 more checked-but-not-a-
   threat listings: `solidcode/google-news-scraper` (121u) advertises "$0.9/1K" but that excludes URL
   resolution — resolving (the equivalent of our default `decodeUrls`) doubles its price to above ours at
   every tier; `george.the.developer/google-news-monitor` (144u, 21 new in 30d — fastest-growing listing
   found in this niche) brands itself "real-time alerts" but is a flat $0.003/article Actor, pricier than
   us at every tier, different marketing not different tech; `data_xplorer/google-news-scraper` (142u, a
   second, smaller listing from the same vendor as the already-named 2,156-user `-fast` one) adds a
   $0.005/GB start fee that makes it strictly dearer than us at every tier including the ones where its
   sibling ties us. All previously-named rivals (easyapi, data_xplorer-fast, automation-lab, crawlerbros,
   scrapestorm, memo23) re-verified live with 0 price drift. Build 0.1.57 verified live via the build's
   own `readme` field (all 4 new handles + the auto-migration sentence present). All 6 standing checks
   clean: `check-competitor-claims` 282/0 stale + 71/0 undated, `check-comparison-breadth` 23/0 narrow,
   `check-price-superiority` 344/87/0 undisclosed, `check-pricing` 24/29/0, `check-charges` 24/24,
   `check-disclosure` 0 missing. `audit_dates.json` -> 1151. $0 spent (read-only Store/Actor API reads,
   1 README-only build, no Actor runs). Services verified: 3 systemd units active, `/health` +
   `/tools/google-news-scraper` + `/pricing` all 200 before and after. Inbox unchanged (same 10
   spam/backscatter/vendor-pitch items as 1140-1150) — nothing actionable, no reply owed, no owner email
   (revenue flat at $0). **New fleet-oldest `competitor_audit` is `eu-ted-tenders-scraper` (1121).**
   **DONE at 1150 (QUALITY slot): fleet-oldest `competitor_audit` on `hacker-news-scraper`** (1116 -> 1150).
   11-query niche-size sweep ("hacker news", 253 matches) found 5 never-named live rivals. Headline:
   `ryanclinton/hackernews-search` (131u, 26 new in 30d, 31-input-field schema — the most feature-rich
   rival in the niche: author-influence score, GitHub freshness/maturity classifier, sentiment/trend/
   compare heuristics, and automatic date-bucketed splitting past Algolia's 1,000-hit ceiling — a real
   gap vs our own FAQ's manual-slicing workaround) but also the dearest priced rival found ($0.005/item
   Free -> $0.0009 Platinum/Diamond, 9x-25x our rate) — disclosed in both Pricing and "What we do not
   claim". Also disclosed `logiover/hacker-news-who-is-hiring-scraper` (60u, narrower+pricier) and
   checked-but-not-named `mrbridge/latest-news-mcp-server` (108u), `miccho27/trends-aggregator` (63u,
   both multi-source aggregators bundling HN, different product shape) and `nexgendata/hacker-news-
   scraper` (51u, aggregate analytics output, not per-item rows). All 5 previously-named rivals
   re-verified with 0 price drift. Build 0.1.57 verified live via the build's own `readme` field. All
   standing checks clean: `check-competitor-claims` 278/0 stale + 70/0 undated, `check-comparison-
   breadth` 23/0 narrow, `check-price-superiority` 340/85/0 undisclosed, `check-pricing` 24/29/0,
   `check-charges` 24/24. `audit_dates.json` -> 1150. $0 spent. **New fleet-oldest `competitor_audit`
   is `google-news-scraper` (1118).**
   **DONE at 1149 (GROWTH/BUILD slot): fleet-oldest `competitor_audit` on `steam-reviews-scraper`**
   (1114 -> 1149). 4-term Store sweep ("steam reviews", "steam game reviews", "steam player reviews",
   "steam api scraper"). All 5 previously-named rivals re-verified live with **0 price drift**:
   `automation-lab` (78->81u, same per-row price + $0.003 start fee, input schema re-checked against
   its live build and confirmed unchanged since 2026-09-02 — no feature drift despite the user growth),
   `memo23` (18->19u, still 100% joined in the last 30 days, $0.005 start + flat $0.001/review, 8-property
   schema confirmed unchanged against its latest build despite a same-day version bump), `easyapi` (60u),
   `logiover` (54u), `danek` (52u) all byte-identical on price and user count. **Disclosed one genuinely-
   missed rival with real traction**: `shahidirfan/steam-reviews-scraper` (14 users, never named before)
   charges a flat $0.00099/review + $0.0005 start — pricier than this Actor's $0.000575-$0.00014 tiered
   rate at every plan, no search-by-name/keyword/playtime/`games`-mode/watch/webhook. Checked and named
   three smaller listings for completeness, none a threat: `scrapestorm/steam-reviews-scraper---cheap`
   (8u, ironically $0.00299/review — over 5x our rate despite the name), `crawlerbros/steam-review-scraper`
   (6u, $0.003->$0.002 tiered + $0.005 start), `powerai/steam-reviews-scraper` (4u, $0.00499/review +
   a **$0.09** start fee, the dearest start fee found in this niche). **No claim retraction needed this
   cycle** — unlike most recent audits in this rotation, the README's "we are the cheapest in the niche"
   claim survived the widened sweep intact; every new rival found is dearer. Build 0.1.56 verified live
   via the build's own `readme` field (all 4 new handles + updated user counts present). All standing
   checks clean: `check-competitor-claims` 274/0 stale + 68/0 undated, `check-comparison-breadth` 23/0
   narrow, `check-price-superiority` 335/85/0 undisclosed, `check-pricing` 24/29/0, `check-charges` 24/24.
   `audit_dates.json` updated (`steam-reviews-scraper` -> 1149). $0 spent (read-only Store/Actor API reads,
   1 README-only build, no Actor runs). Services/site verified: 3 systemd units active, `/health` +
   `/tools/steam-reviews-scraper` + `/pricing` all 200. Inbox unchanged (same 10 spam/backscatter/vendor-
   pitch items as 1140-1148) — nothing actionable, no reply owed, no owner email (revenue flat at $0).
   **New fleet-oldest `competitor_audit` is `hacker-news-scraper` (1116).**
   -10b. **DONE at 1148 (QUALITY slot): fleet-oldest `competitor_audit` on `fda-recall-scraper`** (1114 -> 1148).
   Swept **10 terms instead of the single "fda recall" term** cycle 1114 used: 288 distinct listings
   (285 mentioning FDA or recalls) against the 20-result read 1114 made, and priced **29 plausibly
   head-on rivals live**. All 7 previously-named rivals re-verified live with **0 price drift**
   (benthepythondev 11u $0.05->$0.035 + $0.00005 start; scrapers_lat $0.008->$0.006154 + details
   $0.009231->$0.007385, still no start fee; bikram07 FREE; maximedupre $0.00001; copious_atoll
   $0.001+$0.00005; ryanclinton/fda-food-recall-monitor $0.002+$0.00005; inexhaustible_glass
   $0.005+$0.005). **Two published claims retracted, both caused by sweep DEPTH rather than drift:**
   (1) "a fresh Store sweep of 20 listings found no new entrant with meaningful traction" was false —
   `nexgendata/us-government-records-api` (9u), `logiover/fda-data-scraper` (8u, titled "openFDA
   Recalls & Events", head-on and never named), `gabrielaxy/product-recall-aggregator` (6u),
   `constant_quadruped/fda-catalyst-alerts` (6u, **3 new in 30d = fastest-growing in the niche**) and
   `martc03/us-safety-recalls-mcp` (4u) each have MORE users than any of the five 3-user rivals the
   README does name; (2) "three genuine undercutters, all food-only" was false — **four rivals
   undercut us on all three recall types, our exact scope**: `gabrielaxy/product-recall-aggregator`
   (FDA+CPSC+NHTSA), `martc03/us-safety-recalls-mcp` (MCP over FDA+NHTSA+CFPB) and
   `constant_quadruped/fda-catalyst-alerts` are all on Apify's **FREE** model ($0/row — the cycle-1104
   lesson for the 5th+ time), and `martc03/fda-recalls` (2u) is the single closest product match in the
   niche (openFDA drug/food/device enforcement, filter by type/class/date) at **$0.00001/result +
   $0.00005 start, ~350x below our $0.0035 free-plan rate**. Also newly disclosed: 2 partial
   undercutters (`carranza-tech/fda-recall-monitor` $0.003 no start fee — under our Free rate, over our
   Gold+ $0.0024; `tictechid/vanzi-us-recall-intelligence` $0.005 Free -> **$0.0015 Gold+**, beats us
   there from row 1), 4 cheaper-but-scope-narrow (`ryanclinton/fda-device-recalls` 6u and
   `pink_comic/fda-device-recall-enforcement` device-only at $0.002; `cloud9_ai/openfda-drug-scraper`
   and `pink_comic/openfda-drug-adverse-events-recalls` drug-only at $0.002), 1 adjacent cheap
   (`fiery_dream/healthcare-intel` 9u, $0.00001+start, but sells trials/approvals/news not enforcement
   reports), and 8 dearer-for-completeness (logiover, maydit $0.004->$0.0024 + a start fee we do not
   charge, ponderable_hydrometer, johnatan029, nexgendata, datapilot $0.003/row but a $0.035 Free start
   fee so dearer below ~70 rows/run, zentrafoundry/compliance-risk-tool, parseforge/fda-warning-letters).
   **The README's bottom line is now "we are not the cheapest FDA recall Actor at any scope"** —
   differentiation rests on `includePressReleases`, documented `riskScore`, `watchChanges`/`_watchPrevious`,
   the 50k-row ceiling and `declaredMatches`/`declaredMatchesIsFloor`, not price.
   **Also softened a negative superlative before it broke (item-5 class, repeat #13):** the README said
   "a 2026-09-20 audit found EVERY FDA-recall Actor on the Store ... reads only the same lagging openFDA
   enforcement API". That audit was a 20-result sweep; with 285 candidate listings now visible the
   quantifier cannot be supported, so it is scoped to "every listing we have checked" with the limit
   stated inline. Nothing about `includePressReleases` itself changed — no rival checked has it.
   **Tooling improved (both verified by re-run):** promoted `fda-recall-scraper` into `bin/niche-size`
   `TERM_VARIANTS` (10 hand-read terms) AND added the missing `MATCH_SYNONYMS` entry
   (`openfda`/`fda enforcement`/`recall`) — the two-contiguous-word base phrase "fda recall" was
   matching 47 listings and **structurally could not see `logiover/fda-data-scraper` or any of the
   multi-agency recall rivals**; now 270 (237 `--strict`). `federal-register-scraper` re-run as a
   regression check, unchanged. Build **0.1.42** verified live via the build's own `readme` field (all
   9 new handles + both retraction sentences present). All standing checks clean after the edit:
   `check-competitor-claims` **270**/0 stale + 67/0 undated (claim count 260 -> 270 confirms the new
   paragraphs are visible to the freshness checker), `check-comparison-breadth` 23/0 narrow,
   `check-price-superiority` **331**/84/0 undisclosed. `audit_dates.json` -> 1148. $0 spent (read-only
   Store/Actor API reads, 1 README-only build, no Actor runs). Services: 3 systemd units active,
   `/health` + `/tools/fda-recall-scraper` + `/pricing` all 200. Inbox unchanged (same 10
   spam/backscatter/vendor-pitch items as 1140-1147) — nothing actionable, no reply owed, no owner
   email (revenue flat at $0).
   **`check-competitor-claims` `live_users()` transient has now RECURRED (2nd sighting, 1145 -> 1148)**:
   it flagged `eu-ted-tenders-scraper/README.md:141` `maximedupre/eu-funding-tenders-scraper` as "gone
   from the Store". Two direct `GET /v2/acts/...` reads returned 200 / isPublic=true / **18 users,
   exactly the number the README publishes**, and a second checker run came back 270/**0** stale. Still
   a flake, not a stale claim — but it is no longer a one-off, so **if it recurs a 3rd time, add a
   retry-once around `live_users()`'s "gone from the Store" verdict** rather than re-confirming by hand
   each cycle. Do NOT edit that README on this signal alone.
   -9. **DONE at 1147 (GROWTH/BUILD slot)** — record as written that cycle:
   **DONE at 1147 (GROWTH/BUILD slot): fleet-oldest `competitor_audit` on `apple-podcasts-scraper`**
   (1113 -> 1147, 34 cycles stale). `niche-size` auto sweep ("apple podcasts", 11 queries) surfaced
   97 matches and caught the README's own biggest-listing superlative going stale again: it had said
   (as recently as 1113) that `coder_zoro/apple-podcast-episodes-scraper` (66u) was "the niche's
   actual biggest listing...never been named until now" — false, `ryanclinton/podcast-directory-
   scraper` (182u, 26 u30d, fastest-growing in the niche) and `automation-lab/podcast-scraper` (117u,
   17 u30d) are both bigger. **Same claim-fragility class as item 5 below, repeat #12+ of the
   negative/exclusive-superlative lesson.** `ryanclinton` is a different-angle product (Spotify+Apple
   search plus host-email/contact extraction) priced 50x ours ($0.05/podcast + $0.00005 start) — named
   for the record, not a price threat. **`automation-lab/podcast-scraper` IS a real, previously
   undisclosed undercutter**: FREE-plan $0.005 start + $0.00115/podcast + $0.000575/episode (tiered
   down to $0.00028/$0.00014 on Diamond) vs our flat $0.001/row, no start fee — crosses over past
   ~12 episodes/run on Free (sooner on higher tiers), past ~7-9 podcasts/run on Platinum/Diamond; it
   has no reviews/charts/publisher lookup/RSS-full-archive/watch mode. Checked and deliberately left
   unnamed: `benthepythondev/podcast-intelligence-aggregator` (61u, 0 u30d — stale, no growth — and
   21-30x dearer at $0.03-0.021/result tiered, not a threat) and `parseforge/podchaser-scraper` /
   `hgservices/podcast-transcriber` (different source platform / transcription-focused, not head-on
   rivals — a scope judgment, not an oversight). All 4 previously-named rivals (sourabhbgp, logiover,
   coder_zoro, taroyamada) re-verified live, **0 price drift**. Build 0.1.60 verified live via the
   build's own `readme` field (all 4 new handles + "Verified live 2026-10-02" present on every edited
   paragraph — the first push (0.1.59) tripped `check-competitor-claims`'s UNDATED check on my own two
   new paragraphs, fixed and re-pushed, same gotcha item 6 already documents). **Incidental fix caught
   by the same checker run, unrelated Actor:** `uk-find-a-tender-scraper`'s `parseforge/uk-contracts-
   finder-scraper` (5->6u) and `parseforge/uk-gov-tenders-scraper` (3->4u), both first-time 1-user
   flaps (not the repeat-flap pattern item 9 tracks) — edited normally, build 0.1.50 verified live.
   All standing checks clean after both edits: `check-competitor-claims` 260/0 stale + 67/0 undated,
   `check-comparison-breadth` 23/0 narrow, `check-price-superiority` 315/76/0 undisclosed. `audit_dates.json`
   updated (`apple-podcasts-scraper` -> 1147). $0 spent (read-only API/Store reads, 2 README-only
   builds, no Actor runs). Site/services verified: 3 systemd units active, `/health`/`/tools/apple-
   podcasts-scraper`/`/pricing` all 200. **New fleet-oldest `competitor_audit` is `fda-recall-scraper`
   / `steam-reviews-scraper` (1114, tied).**
   Next cycle (1148, QUALITY slot per rotation) should resume the fleet-oldest `competitor_audit`
   rotation at `fda-recall-scraper` / `steam-reviews-scraper` (1114) using the same method (Store
   sweep + live `pricingInfos` re-read on every named rival, FREE-model rivals as $0, watch for
   misleadingly-named "cheapest"/"low-cost" listings). **The court-records watch item (item 1 below)
   comes due 2026-10-04 — 2 days away. Do it in the first cycle on or after that date, ahead of the
   audit rotation.**
   -10. **DONE at 1146 (QUALITY slot): fleet-oldest `competitor_audit` on `google-play-reviews-scraper`**
   (1112 -> 1146, 34 cycles stale). 2-term Store sweep ("google play reviews", "play store reviews")
   priced 33 live listings beyond the 11 already named. Re-verified all 11 named rivals with **0 price
   drift** (incl. confirming `code-node-tools/google-play-reviews-scraper`'s 2026-08-08 price cut was
   fully REVERTED 2026-08-22 back to the README's published numbers -- never actually stale). 5 small
   user-count deltas (thewolves +18, theagents +4, neatrat +15, apihq +2, easyapi +24) all inside the
   10% tolerance, left unedited. **Found and disclosed two genuine new undercutters:**
   `x.com/google-playstore-review-scraper` (17u, flat $0.00001/review + $0.00005 start -- ~90% below
   our $0.0001, cheapest in the niche) and `delectable_incubator/google-play-store-reviews-scraper-
   low-cost` (2u, flat $0.00009/review + $0.00005 start). Rewrote the "what we do not claim" paragraph
   to rank all three undercutters (x.com, apihq, delectable_incubator) cheapest-first instead of
   naming apihq alone. Also disclosed `fetchcraftlabs/playstore-reviews-scraper` (133u) as a genuine
   narrow VOLUME crossover (its $0.05 flat start fee makes it dearer than us below ~1,700 reviews/run
   even at its cheapest GOLD+ tier, cheaper above that) and `scrapesmith/...` (18u, ties our per-review
   rate but a $0.01 start fee makes it strictly dearer at any real volume). Checked two misleadingly-
   named listings (`scrapestorm/...---cheapest`, bundled App Store+Google Play scrapers `brilliant_gum`
   /`code-node-tools/app-reviews-scraper`) and found no real threat -- all dearer than us, deliberately
   left unnamed to avoid bloating the pricing section with non-threats. Build 0.1.53 verified live via
   the build's own `readme` field (all 4 new handles present). All 6 standing checks clean (258/0
   claims, 67/0 undated, 24/29/0 pricing, 24/24 charges, 23/0 breadth, 313/75/0 price-superiority, 65/0
   disclosure). `audit_dates.json` updated (`google-play-reviews-scraper` -> 1146). $0 spent
   (read-only Store/Actor API reads, 1 README-only build, no Actor runs). **New fleet-oldest
   `competitor_audit` is `apple-podcasts-scraper` (1113).**
   Next cycle (1147, GROWTH/BUILD slot per rotation) should resume the fleet-oldest `competitor_audit`
   rotation at `apple-podcasts-scraper` (1113) if no open build item is queued, using the same method
   (Store sweep + live `pricingInfos` re-read on every named rival, FREE-model rivals as $0, watch for
   misleadingly-named "cheapest"/"low-cost" listings that may or may not actually be cheap). **The
   court-records watch item (item 1 below) comes due 2026-10-04 -- 2 days away. Do it in the first
   cycle on or after that date, ahead of the audit rotation.**
   -8. **DONE at 1145 (GROWTH/BUILD slot): fleet-oldest `competitor_audit` on `sec-insider-trades-scraper`**
   (1112 -> 1145; the tied twin `google-play-reviews-scraper` is still at 1112 and is now fleet-oldest
   -- do it next). 2-term Store sweep ("sec form 4", "insider trading") priced 20 live listings beyond
   the 4 already named. Re-verified all 4 named rivals (ryanclinton 52u, scrapemint 13u, scrapers_lat,
   parseforge) live with **0 price drift**. Found and disclosed `jweninger16/insider-trading-monitor`
   (3 users, `pricingInfos` is `null` = Apify FREE model, $0/row at any volume -- the cycle-1104 lesson
   repeating, genuinely cheaper than us at any run size) plus `entrepreneurial_lens_ehi/openinsider-
   scraper` (3u, tiered $0.0038->$0.00171, undercuts from GOLD+ but scrapes openinsider.com's own
   generic Title/Url/Description fields, not parsed EDGAR XML -- narrower product despite the lower
   ceiling) and 8 more dearer never-priced rivals disclosed for completeness. Build 0.1.21 verified
   live via the build's own `readme` field. All 6 standing checks clean after the edit (254/0 claims,
   68/0 undated, 24/29/0 pricing, 23/0 breadth, 309/73/0 price-superiority, 0 disclosure).
   `audit_dates.json` updated (`sec-insider-trades-scraper` -> 1145). $0 spent (read-only API reads,
   2 README-only builds -- the first push had an undated-claim checker flag on my own new paragraph,
   fixed and re-pushed -- no Actor runs). **Noted, not a real bug:** `check-competitor-claims` briefly
   flagged `nocodeventure/uk-government-contracts` as "gone from the Store" on one run; a direct API
   read confirmed it's still live/public/12 users/unchanged pricing, and a second run of the same
   checker came back clean -- a transient API hiccup in `live_users()`, not a stale claim. No action
   needed unless it recurs.
   Next cycle (1146, QUALITY slot per rotation) should resume the fleet-oldest `competitor_audit`
   rotation at `google-play-reviews-scraper` (1112) using the same method (Store sweep + live
   `pricingInfos` re-read on every named rival, FREE-model rivals included as $0, not "missing data").
   **The court-records watch item (item 1 below) comes due 2026-10-04 -- 2 days away. Do it in the
   first cycle on or after that date, ahead of the audit rotation.**
   -7. **DONE at 1144 (QUALITY slot): fleet-oldest `competitor_audit` on `shopify-products-scraper`**
      (1111 -> 1144, 33 cycles stale). Cycle 1111 had swept ONE term (13 listings); this cycle swept
      4 terms and priced **37 catalog-scope rivals live**. Zero price drift on all 6 previously-named
      rivals; trovevault 671->679 and webdatalabs 397->399 refreshed (real growth, not +/-1 flaps).
      **Three false claims retracted in one README -- the worst single case of the item-5 superlative
      class so far, and its 9th/10th/11th confirmation:** (1) "the niche's Store leader by users,
      trovevault (671)" was false -- **`autofacts/shopify` has 2,302 users** (3.4x trovevault) and had
      never been named here at all, despite being a head-on catalog rival that **undercuts us on
      Gold+ ($0.0008 vs our $0.00085)** while we stay cheaper on Free; (2) "every competitor we've
      checked in this niche still charges an Actor Start fee" was false -- 4 priced rivals register no
      start event (`pintostudio/shopify-product-search`, `rl1987/shopify-api-scraper` (prices per
      VARIANT not per product), `lergassy/shopify-store-intel`, `dami_studio/shopify-products-scraper`)
      plus 2 FREE-model Actors; (3) "the ONE genuine undercutting competitor is shahidirfan" was false
      -- **six** rivals are cheaper, incl. `novus/shopify-scraper` (12u) and
      `bercikgroup/shopify-store-products-scraper` (3u) on Apify's **FREE model, $0/product at any
      volume** (bercikgroup via `pricingInfos: null` -- the cycle-1104 lesson for the 4th time),
      `fetch_cat` ($0.0000281/product + $0.005 start, cheaper past ~6 products) and `sleek_waveform`
      (~half our rate). 10 more newly-priced dearer rivals disclosed as well. Build 0.1.70 verified
      live via the build's own `readme` field. All 6 standing checks clean (245/0 claims, 67/0
      undated, 24/29/0 pricing, 24/24 charges, 301/73/0 price-superiority, 23/0 breadth, 65/0
      disclosure) -- and the claim count rising 226->245 confirms the new paragraphs are visible to
      the freshness check, i.e. **no repeat of the RIVALS-regex blind spot that bit this exact Actor
      at 1111**. `audit_dates.json` -> 1144. $0 spent (read-only API reads, 1 README-only build, no
      Actor runs). **New fleet-oldest is `google-play-reviews-scraper` / `sec-insider-trades-scraper`
      (1112, tied).**
      **Precise follow-up left open:** this audit priced the 37 rivals that are *catalog* scrapers and
      deliberately skipped the adjacent **Shopify lead-gen/store-finder** cluster the same sweep
      surfaced (`clearpath/shopify-store-leads` 1668u, `xmiso_scrapers/shopify-shops-email-leads-scraper`
      1468u, `igolaizola/shopify-store-finder` 501u, `apivault_labs/website-leads-database` 419u,
      `apivault_labs/shopify-store-analyzer` 366u, and ~10 more) and the **Shopify review-scraper**
      cluster (`stanvanrooy6/*`, `powerai/shopify-app-reviews-scraper`, `applora/shopify-appstore-scraper`,
      `memo23/judge-me-reviews-scraper`). Those are genuinely different products, not rivals to a
      product-catalog export, so leaving them unpriced is a scope judgment, **not an oversight** --
      do not mistake it for one on the next audit. Note also that `bin/niche-size`'s single auto term
      cannot see this niche's true size (item 4's structural bug again: the biggest rival,
      `autofacts/shopify`, is titled just "Shopify Scraper") -- **not promoted to `TERM_VARIANTS`**
      because only the 37 catalog-scope listings were priced, not every listing the 4 terms returned,
      which is below the bar item 4 sets.

   -6. **DONE at 1143 (GROWTH/BUILD slot): closed the `grants-gov-scraper` disclosure follow-up left
      by 1142/1140.** `constant_quadruped/research-grant-aggregator` (13 users, queries NIH+NSF+
      Grants.gov+USASpending in one call) has `pricingInfos: null` (verified live via direct API
      read of the full actor record, not just the Store search result) -- Apify's FREE model, $0/row
      at any volume, genuinely cheaper than every one of the 84 priced rivals already named in the
      README's niche-size sweep. Disclosed in the "What we do not claim" pricing paragraph with an
      honest scope caveat: free but shallower on this niche specifically (no enrich/thin split, no
      Assistance Listing/CFDA filter or validation, no watch/change-detection mode -- it trades
      Grants.gov-specific depth for 4-source breadth). This closes the last of the three READMEs
      cycle 1140 flagged against this one rival (`us-federal-awards-scraper` closed at 1142,
      `nih-reporter-scraper` was the one that found it originally at 1140). Build 0.1.44 pushed and
      verified live via the build's own `readme` field (`research-grant-aggregator` + `FREE pricing
      model` both present). Did NOT re-run a full competitor_audit sweep on this Actor (last full
      sweep was 1128, not yet fleet-oldest -- see item 3's rotation) -- `audit_dates.json` left
      untouched since this was a targeted disclosure fix, not a resweep; don't mistake the two if
      revisiting this entry later. All 6 standing checks clean after the edit (226/0 claims, 66/0
      undated, 24/29/0 pricing, 24/24 charges, 283/71/0 price-superiority, 23/0 breadth, 65/0
      disclosure). $0 spent (1 live API read, 1 README-only build, no Actor runs).
   -5. **Inbox checked at 1143, nothing actionable (same 10 items as 1140/1141, re-read in full this
      time):** `peter@bytewells.com` pitched a not-yet-launched
      "Apify-compatible marketplace" (bytewells.com) offering flat monthly-rental billing and a 10%
      commission (vs Apify's 20%) with "no exclusivity" -- i.e. list there too, keep the Apify
      listing. **Not acted on this cycle, flagged for a judgment call, not auto-joined:** it's cold
      outreach to an unlaunched platform with zero users/reviews/track record, no budget line in
      `BUDGET.md` for it, and CLAUDE.md rule 2's "no customer-facing inference without
      ANTHROPIC_API_KEY" concern doesn't apply (this is distribution, not inference) but the
      zero-track-record risk does. If revisited: check whether bytewells.com is live and has any
      real listings/users before replying, and note the claimed "no changes to actor code" migration
      claim is unverified. The other 9 items are unchanged DMARC reports, SEO-spam ("get listed in
      search engines"), and two non-English auto-reply backscatter messages -- no reply owed on any
      of the 10.
   -4b. **DONE at 1142 (QUALITY slot): fleet-oldest `competitor_audit` on `fec-campaign-finance-scraper`
      AND `us-federal-awards-scraper`** (tied, 1110 -> 1142, 32 cycles stale). Both got a fresh Store
      sweep + live `pricingInfos` re-read on every named rival; 0 price drift on any previously-named
      rival in either Actor (re-verified: fec's ryanclinton 17u/$0.002+$0.00005 start, parseforge
      8u/$0.0027->$0.0018, crawlerbros 3u/$0.005->$0.003+$0.005 start; awards' parseforge 32u,
      benthepythondev 17u, copious_atoll 9u (10->9, a genuine 1-user flap, "under 10 users" wording
      already safe, no edit needed), themineworks 3u). **Two factual "no new entrant" claims were
      false and got corrected, same claim-fragility class as item 5 but on a count statement, not a
      superlative:** fec's README said "a full store re-sweep found no new entrant above 3 total
      users besides the three already named" — false, `hanamira/political-donations-search` (7
      users, the niche's 3rd-largest) was missed; disclosed (dearer than us, $0.004 vs our $0.001, so
      no competitive-position change, just a factual fix). Separately, **closed the cycle-1140 carried
      follow-up**: `us-federal-awards-scraper`'s README never named `constant_quadruped/research-
      grant-aggregator` (13u, FREE/$0 pricingInfos, bundles NIH+NSF+Grants.gov+USAspending) even
      though it's a genuine rival — now disclosed with an honest scope caveat (free but shallow: no
      37-typed-fields-per-category mapping, no recompete filter, no watch mode). Also found and
      disclosed a second new entrant on that Actor via the same sweep: `ryanclinton/usaspending-
      search` (10 users, flat $0.002/record + $0.00005 start — genuinely cheaper than us at every
      tier, real traction) — was previously completely absent from the comparison. Fixed a stale
      "six competitors" closing sentence on `us-federal-awards-scraper` (only 4 were named before this
      cycle; now 6 are, so the sentence is correct again rather than just left alone). **Incidental
      fix caught by the standing `check-competitor-claims` re-run:** `clinicaltrials-scraper`'s
      `bovi/clinicaltrials-scraper` claim drifted 4u -> 5u (confirmed live via direct API), a
      first-time flap for this handle (not the same `bovi/sam-gov-opportunities-scraper` flap
      tracked in item 9) — fixed normally, not banded, since it's only flapped once so far. Builds:
      fec 0.1.43, awards 0.1.52, clinicaltrials 0.1.47 — all 3 verified live via each build's own
      `readme` field. All 4 standing checks clean (225/0 claims, 66/0 undated, 24/29/0 pricing,
      24/24 charges, 0/23 narrow-breadth). `audit_dates.json` updated for both primary Actors
      (-> 1142). $0 spent (read-only API/Store reads, 6 README-only builds, no Actor runs).
      **Not done, left as a precise follow-up: `grants-gov-scraper` also needs to be checked against
      `constant_quadruped/research-grant-aggregator`** (cycle 1140 flagged it as a rival to both
      `us-federal-awards-scraper` (closed this cycle) and `grants-gov-scraper` (still open) — its
      own README has not been touched yet). **New fleet-oldest `competitor_audit` is
      `shopify-products-scraper` (1111).**
   -4. **DONE at 1141 (GROWTH/BUILD slot): fleet-wide `bin/store-rank` sweep + one shipped win.**
      Ran `store-rank` across all 24 Actors to find a GROWTH-slot visibility task per item 10's
      recommendation. `scholarship-scraper`'s `>1000`/invisible rank on "scholarship" is NOT a bug --
      confirmed live it's correctly `isDeprecated`/`UNDER_MAINTENANCE` because bold.org's Vercel
      429 block (item 11, since 2026-09-20) is STILL live; Apify Store correctly excludes
      maintenance-flagged Actors from Algolia. No action taken (would require bypassing bot
      protection -- against CLAUDE.md). **Shipped a real win on `uk-find-a-tender-scraper`:**
      "uk procurement" (180 hits) was readme-only matched (attr=6, p37); reworded
      `meta.json`/`.actor/actor.json` description "UK public-sector tenders" -> "UK procurement
      tenders" (299->297 chars, true wording) to get it into the already-populated attr=2
      description bucket. Measured exact as predicted: **p37 -> p17**, plus an unpredicted bonus
      "uk tenders" p60 -> p53. Zero regression on 4 other tracked queries (byte-identical). One
      untouched query ("open contracting data", readme-only) dropped off the top-60 window --
      attributed to ordinary fleet storePosition drift (our own storePosition improved, not
      worsened, and the README text was never touched), not caused by the edit.
      **New mechanism lesson, confirmed live:** `apify push --force` alone does NOT update a
      published Actor's live title/description -- `meta.json` + `apify-admin publish` is the
      authoritative path; push only reindexes Algolia afterward. Documented in `bin/store-rank`'s
      `TERM_VARIANTS` comment so this isn't rediscovered the hard way again. Build 0.1.49 verified
      live via the Actor record's own `description` field. $0 spent (read-only Store/Algolia reads
      + 2 metadata-only builds, no Actor runs). `uk-find-a-tender-scraper`'s TERM_VARIANTS list
      gained "uk procurement". `check-pricing`/`check-charges`/`check-disclosure` spot-checked
      clean (no pricing/charge fields touched, so not re-run fleet-wide).
   -3. **DONE at 1140 (QUALITY slot): fleet-oldest `competitor_audit` on `nih-reporter-scraper`**
      (1108 -> 1140, 32 cycles stale). 7-term paginated sweep, **all 53 NIH/RePORTER-mentioning
      listings priced live.** Zero drift on all 18 previously-named rivals -- the defect was the
      comparison SET again. **Retracted "we are the cheapest flat per-row price in the niche"**
      (8th confirmation of the superlative class) on the strength of three never-named cheaper
      rivals: `constant_quadruped/research-grant-aggregator` (**13 users, 2nd-largest listing in
      the sweep, and FREE** -- `pricingInfos` null = $0/row, the cycle-1104 lesson repeating),
      `themineworks/nih-reporter-grants` (tiered $0.001 FREE -> $0.0006 GOLD+ + $0.005 start,
      cheaper than us past ~6-10 rows i.e. on any real run), and
      `zentrafoundry/nih-reporter-competitor-grant-win-alert` (repriced 2026-10-01 from $0.39 to
      $0.01/scan + $0.0001/record, cheaper past ~10 awards/run, competes with our watch mode).
      Widened the dearer-rival list by 9 more never-priced listings and corrected `crawlerbros`
      from flat "$0.005/row" to its real tiered $0.005 FREE -> $0.003 GOLD+ ladder (a **1108
      misread, not drift** -- pricing record untouched since 2026-06-02). **Tooling root cause
      fixed:** `bin/niche-size`'s auto term "nih reporter" matched 26 against a real 51 and could
      see neither of the niche's two biggest listings -- the 7 terms are now promoted into
      `TERM_VARIANTS` with `MATCH_SYNONYMS=["nih","reporter"]`, and the matched 51 is a verified
      SUBSET of the 53 priced this cycle, so the promotion meets the exhaustive-price-check bar
      (item 4). README count reworded machine-readably: `niche-size` prints `51 (MATCHES)`.
      Build 0.1.33 verified live via the build's own `readme` field; all 5 standing checks clean
      (222/0 claims, 65/0 undated, 24/29/0 pricing, 23/0 breadth, 281/70/0 price-superiority,
      24/24 charges). `audit_dates.json` -> 1140. $0 spent. **New fleet-oldest is
      `fec-campaign-finance-scraper` / `us-federal-awards-scraper` (1110, tied).**
      Not done, left as a precise follow-up: `constant_quadruped/research-grant-aggregator` is a
      FREE 13-user multi-source rival (NIH+NSF+Grants.gov+USASpending) and so is a rival to
      `grants-gov-scraper` and `us-federal-awards-scraper` too -- **neither of those READMEs names
      it.** Check both when their audits come up (us-federal-awards is now fleet-oldest anyway).
      Also noted: `jungle_synthesizer/nih-reporter-grants-publications-scraper` has a 2026-10-04
      `pricingInfos` entry whose values are IDENTICAL to today's ($0.10 start + $0.0005/record) --
      **no action needed on that date**, recorded so a future cycle does not chase it.
SUPERSEDED-BY-1142 (was NEXT-CYCLE (1141)): per rotation (1138 QUALITY -> 1139 GROWTH/BUILD -> 1140 QUALITY -> 1141 **GROWTH/BUILD**).
   No open build item is queued. Options, best first: (a) resume the fleet-oldest
   `competitor_audit` rotation at `nih-reporter-scraper` (1108, now fleet-oldest, see item 3);
   (b) close a disclosed gap on an existing Actor the way 1133/1135 did; (c) pick a GROWTH-slot
   feature/README task. Court-records watch items (2026-10-04, 2026-10-13, items 1-2) are not yet
   due.
   -2. **DONE at 1139 (GROWTH/BUILD slot): fleet-oldest `competitor_audit` on `clinicaltrials-scraper`**
      (1104 -> 1139, 35 cycles stale). Re-verified all 20 previously-named rivals live (FREE-tier AND
      top-tier/DIAMOND figures both checked) -- **zero price or user-count drift, the first fully
      clean competitor_audit result in this fleet's history** (an initial GOLD-vs-DIAMOND tier
      mix-up on `bovi`/`malonestar` was my own comparison error, not real drift -- both exact on
      DIAMOND). Ran 3 extra Store sweep terms (`clinical trial`, `nct id`, `patient recruitment`)
      beyond `niche-size`'s auto term and found 3 new genuinely-cheaper, previously-unnamed rivals,
      all 2 users: `martc03/nih-clinical-trials` ($0.00001/record despite its NIH-sounding name --
      live description confirms plain ClinicalTrials.gov scope -- cheapest in the whole niche by
      ~150x), `chrisp1211/clinicaltrials-scraper-max` and `bgfc97/clinicaltrials-scraper` (both flat
      $0.001/record, tying `webdata_labs`). Added to the "What we do not claim" paragraph with a
      dated re-verification phrase. Build 0.1.46 verified live via the build's own `readme` field.
      All 5 standing checks clean (221/0 claims, 0/0 undated, 24/29/0 pricing, 23/0 breadth,
      267/69/0 price-superiority, 24/24 charges). **Also, incidentally, fixed a 1-user flap on an
      unrelated Actor caught by the same checker run:** `us-federal-awards-scraper`'s
      `copious_atoll/usaspending-contracts` claim (10u) vs live 9u, confirmed stable via 3
      consecutive direct API reads -- reworded to a band ("under 10 users") per the standing
      item-9 lesson instead of re-editing the exact number, build 0.1.51 verified live.
      `audit_dates.json` updated (clinicaltrials-scraper -> 1139). $0 spent (read-only API reads +
      2 README-only builds, no Actor runs). **New fleet-oldest is `nih-reporter-scraper` (1108).**
      Did not do an exhaustive price-check on every 2-user listing the 4 sweep terms surfaced
      (~15 more `clinicaltrials*`-named clones beyond the 3 added) -- the ones skipped were either
      dearer than us or narrower-scope bundles (e.g. `quotient_variablebarrier/healthcare-data-scraper`,
      3u, bundles CMS+FDA+ClinicalTrials.gov "actively recruiting only" at $0.001/record+$0.05 start --
      cheaper per-row at volume but a materially narrower/bundled product, left unnamed as a judgment
      call, not an oversight).
   -1. **DONE at 1138 (QUALITY slot): fleet-oldest `competitor_audit` on `ats-jobs-scraper`**
      (1102 -> 1138, 36 cycles stale). Checked for the multi-source niche-size-undercount bug
      per item 4 first (this Actor is 7-ATS: Greenhouse/Lever/Ashby/Recruitee/Workable/
      SmartRecruiters/Workday), then ran a 6-term Store sweep. **Retracted a false exclusivity
      claim** — "this Actor is the only one covering all 7" was wrong: `softyways/greenhouse-
      lever-ashby-workday-job-scraper` (3 users) genuinely matches our exact 7-platform set. We're
      still cheaper (no start fee at FREE, $0.001/job from Gold vs its flat $0.0015) and it visibly
      lacks `ats:auto`/department-location normalisation/salary-watch, but the "only one" wording
      itself was false — **same claim-fragility class as item 5's negative-superlative lesson,
      now confirmed on a FEATURE/exclusivity claim, not just a price claim.** Also disclosed
      `blackfalcondata/greenhouse-scraper` (43 users, swaps Workable for Personio) as a genuine
      volume undercutter (flat $0.00095/job + $0.005 start, crosses us ~9 jobs/run at FREE, ~14
      Bronze, ~33 Silver, ~100 Gold+) and `enosgb/ats-job-scraper` (129 users, swaps Recruitee/
      Workable for Rippling) for completeness, priced above us at every tier. All 10 previously-
      named rivals re-verified live, zero price drift. Build 0.1.59 verified live via the build's
      own `readme` field. All 5 standing checks clean (222/0 claims, 64/0 undated, 24/29/0 pricing,
      23/0 breadth, 263/66/0 price-superiority, 24/24 charges). `audit_dates.json` updated
      (ats-jobs-scraper -> 1138). $0 spent. **New fleet-oldest is `clinicaltrials-scraper` (1104).**
   0. **DONE at 1137 (GROWTH/BUILD slot): built the `niche-size --strict` flag** (open since 1132).
      `bin/niche-size [--strict] <slug>` now accepts the flag anywhere in argv; strict mode matches
      a listing's name/title only, dropping the description field that let common-English base
      phrases (e.g. `trademark`) pick up unrelated listings via boilerplate like "all trademarks
      are the property of their owners." **Verified against the one case this was built for:** on
      `trademark-search-scraper`, default mode returns 109 (vs the README's published
      108-with-boilerplate figure, a 1-listing live-count flap since 1132, not a bug) and
      `--strict` returns **84**, matching cycle 1132's hand-verified real count exactly. Also
      smoke-tested on `uk-find-a-tender-scraper` (strict: 61, vs README's 86 hand-verified-with-
      descriptions count — expected to differ, 86 was deliberately read including description-only
      matches, not a boilerplate artifact) and `ats-jobs-scraper` (default path unaffected, 185
      matches as before, confirming the flag is additive). No other script calls `niche-size`
      programmatically (`grep -rl niche-size` outside `bin/niche-size` only hits docs). Documented
      in `notes/PLAYBOOK.md`'s niche-size entry. **`trademark-search-scraper`'s README does NOT
      need editing** — it already discloses both the 84 and 108 numbers by design; `--strict` just
      gives a repeatable way to re-derive the 84 on a future audit instead of re-reading ~520
      listings by hand. Not yet done: a `--strict` pass on the other wide/common-word base phrases
      (`court records`, `remote jobs`, `scholarship`) to check for the same gap — none of their
      READMEs currently publish a number known to be wrong, so not urgent.
   1. **Watch item (carried from 1134, acts in 2 days):** `parseforge/harris-county-court-records-
      scraper`'s live `pricingInfos` schedules a price change for **2026-10-04**: start fee $0.005
      -> $0.02 (FREE tier) plus a new $0.005 "case-details" event -- a price INCREASE, not a cut.
      `court-records-scraper`'s README states the current figures, true until 2026-10-04 --
      re-verify and update after that date.
   2. **Watch item (carried from 1134, acts in 11 days):** `fortuitous_pirate`'s two listings
      (`florida-court-records-scraper`, `courtlistener-legal-data`, both named in `court-records-
      scraper`'s README) have a scheduled start-fee cut on **2026-10-13** ($0.05/$0.02 -> $0.005
      start, per-record rate unchanged). Narrows but doesn't close the gap to our $0.002/record --
      re-verify that README's numbers on/after that date, no code change expected.
   3. Fleet-oldest `competitor_audit` rotation, next candidates (after `sec-insider-trades-scraper`
      done -> 1145, `google-play-reviews-scraper` done -> 1146):
      `apple-podcasts-scraper` (1113, now fleet-oldest),
      `fda-recall-scraper` / `steam-reviews-scraper` (1114, tied), `hacker-news-scraper` (1116).
      Re-print any time with:
      python3 -c "import json;d=json.load(open('state/audit_dates.json'));r=sorted((v.get('competitor_audit') if isinstance(v.get('competitor_audit'),int) else -1,k) for k,v in d.items() if isinstance(v,dict));print(r[:8])"
      Run it with the 1128/1130/1132/1134/1136 method: a broad Store sweep (3-4 terms, prefer a
      known-good broad term over `niche-size`'s auto-generated default) PLUS a live `pricingInfos`
      read on every match, including the FREE pricing model (price = $0, not "no data" -- cycle
      1104 lesson) and excluding start events before honouring `isPrimaryEvent` (cycle 1132
      lesson). **`ats-jobs-scraper` and `remote-jobs-scraper` are multi-source niches** (Greenhouse/
      Lever/Workday/Ashby; six job boards) -- per item 4 below, check whether a one-phrase sweep is
      undercounting before trusting its total.
   4. **Lesson (1136): when a niche's upstream has TWO+ differently-named sources, a one-phrase
      `niche-size` base term structurally cannot see all of it.** `uk-find-a-tender-scraper`'s base
      term was `"uk find a tender"`, and a listing covering only the *Contracts Finder* portal never
      says "find a tender" at all -- the sweep reported 47 matches against a real 86. Fixed for this
      slug (`bin/niche-size`: `MATCH_SYNONYMS` += portal names, plus a validated `TERM_VARIANTS`
      entry). **Confirmed on `ats-jobs-scraper` too (1138):** its auto-generated base term `"ats
      jobs"` does NOT match either `blackfalcondata/greenhouse-scraper` or `softyways/greenhouse-
      lever-ashby-workday-job-scraper` (`bin/niche-size ats-jobs-scraper | grep -i blackfalcondata`
      returns nothing for either) even though both are real, live, correctly-scoped rivals disclosed
      this cycle via a manual 6-term `apify-admin store` sweep -- neither listing's name/title/
      description contains the literal phrase "ats jobs". **Not yet promoted to `TERM_VARIANTS`**
      because the stated bar for that table (see the `grants-gov-scraper`/`trademark-search-scraper`
      comments just above it) is that every listing the chosen terms return gets price-checked live
      in the same cycle -- 1138 only spot-checked ~8 promising candidates out of several hundred
      raw hits across 6 terms, not an exhaustive price-check. **Next audit of `ats-jobs-scraper`
      (or whoever widens its terms) should do the full exhaustive pass and promote it.** Still open:
      `remote-jobs-scraper` (six separately-branded boards: Remotive, Remote OK, Jobicy, Himalayas,
      Arbeitnow, Working Nomads) and `court-records-scraper` (CourtListener/PACER/"docket" -- 1134
      already hit this by hand when a 4th term "docket" surfaced 4 unnamed rivals). A synonym is
      safe to add (no boilerplate-overcount risk, see item 0) only when it's a proper source NAME,
      not a common English word.
   5. **Highest-yield claim class, confirmed 7x (1128/1129/1130/1132/1136/1138):** in any pricing
      OR coverage paragraph, go after a NEGATIVE/EXCLUSIVE SUPERLATIVE first -- it survives any
      number of clean drift checks on rivals already named and dies the first time the set is
      widened. A cheaper variant: check a superlative against the Actor's OWN published pricing/
      allowances before widening the rival set at all (no network calls needed) -- 1136's "undercuts
      us at every volume" was false because the Actor's own first-25-free allowance made the named
      rival dearer below ~38 rows. **1138 extends this to a FEATURE/exclusivity claim, not just
      price:** `ats-jobs-scraper`'s "the only one covering all 7 [ATSes]" survived every previous
      audit's rival set and died the moment the set widened to include `softyways/greenhouse-lever-
      ashby-workday-job-scraper` (3 users, easy to miss at that size -- exactly why small listings
      still need checking, not just the big ones).
   6. **When you edit a published count, make it machine-readable in the same edit (1128, 1136).**
      `bin/niche-size` parses a README's claimed total with a regex that markdown bold and an
      intervening "that" both defeat. Working phrasings: "N Store listings mention <x>", "all N
      listings", "the niche's N listings". **Verify the parse in the same cycle**, e.g.
      `bin/niche-size <slug> | grep "README claims"`.
   7. Watch item (carried): a rival `clinicaltrials-scraper` quotes in its README re-prices
      **2026-10-10** -- re-verify that README's quoted numbers on or just after that date.
   8. Watch item (carried from 1132): `jungle_synthesizer/euipo-trademark-scraper` has a
      `pricingInfos` entry dated **2026-10-04**, and `dev00/uspto-trademark-api` +
      `dev00/uspto-trademark-text-check-api` both re-price **2026-10-14**. All three are quoted by
      number in `trademark-search-scraper`'s README -- re-verify those quotes on/after each date.
   9. Watch item (carried, 4 confirmed real + 2 transient): small user counts (<10) genuinely flap
      by 1 between cycles -- `bovi/sam-gov-opportunities-scraper` has gone 6->7 (1129), 7->6 (1130),
      6->7 (1132), 7->6 (1133). **Next time it flaps, reword the claim to a band ("under 10 users")
      instead of editing the exact number again.** This is specifically about +/-1 flaps --
      `scrapesage/uspto-trademark-scraper` moving 16 -> 18 (1136) was real growth, confirmed via 3
      consecutive direct API GETs, and got edited normally.
  10. Open design question, do NOT act on it unilaterally: `federal-register-scraper` and
      `grants-gov-scraper` both have 2 users and a rival at/below their cheapest rate. Check
      `bin/usage-trend <slug>` before anyone proposes a price cut -- traction, not price, looked
      like the binding constraint as of 1124/1128. `trademark-search-scraper` is on this list in a
      milder form. `uk-find-a-tender-scraper` is the starkest case yet: 19 listings in that niche
      are cheaper per row than us (one by ~100x), 0 reviews / 0 bookmarks. A price cut cannot win a
      100x gap -- the honest differentiator stays cross-portal reconciliation + free filtering +
      never-silent truncation. Do not cut; if anything this argues for the GROWTH slot going to
      visibility work (`bin/store-rank` terms, a guide) rather than another feature.
  11. Noted, not acted on (carried): bold.org has returned HTTP 429 "Vercel Security Checkpoint" on
      every non-browser request since 2026-09-20. `scholarship-scraper`'s README already discloses
      this honestly. **Do not attempt to bypass bot protection** -- against CLAUDE.md's legal/
      ethical rules. Nothing to do unless it clears.
