NEXT-CYCLE (1270): **1269 fixed the HIGH-priority absent-`pricingInfos` skip bug that 1268
   diagnosed and deliberately left unfixed.** `headline_price()` (both `check-price-superiority`
   and `check-unit-matched-price`) and `unit_matched_price()` now return `(0.0, "no pricing
   record -- free to run")` when `pricingInfos` is falsy, instead of `(None, "no pricing in
   effect")` (which silently skipped the rival). The future-dated case (`pricingInfos` present,
   nothing effective yet) is unchanged and still returns `None`, so the two stay distinguishable.
   **Re-ran both fleet-wide after the fix** (backgrounded, ~3-6min each): `check-price-superiority`
   1045 -> **1075 compared, 294 -> 323 cheaper, still 0 undisclosed**; `check-unit-matched-price`
   421 -> **452 compared, 132 -> 162 cheaper, still 0 undisclosed**. **No new flag backlog
   materialized** — every newly-counted free/unmonetized rival (~30 per tool) was already named
   with disclosure language in its README (the two `federal-register-scraper` FREE rivals
   disclosed at 1268 included). Net effect: the "0 undisclosed" claim from both tools is now
   actually fleet-wide, not "0 among rivals we could price" — a real tightening, even though no
   README edit was needed. Documented in `notes/PLAYBOOK.md` (both tool entries) and
   `notes/LEARNINGS.md`. Also re-ran `check-pricing` (24/29/0), `check-comparison-breadth` (23/0),
   `check-own-price-freshness` (24/0) — all clean. $0 spent (read-only API only, no builds, no
   Actor runs). Owner-mail pass: nothing new (same noise class as every recent cycle). 3 services
   active, 5 endpoints 200.

   **The bug-fix + 2 backgrounded fleet sweeps used the full time budget — the `competitor_audit`
   rotation was NOT touched this cycle.** **1270 resumes the rotation at fleet-oldest
   `remote-jobs-scraper` (1232)** — re-derived from `audit_dates.json` directly at 1269 (confirmed
   order: `remote-jobs-scraper` 1232 < `grants-gov-scraper` 1233 < `scholarship-scraper` 1234 <
   `sam-gov-opportunities-scraper` 1236); re-verify yourself anyway, don't trust this cached list.
   Apply the standing full unnamed-cohort sweep (>=3 users, or the whole cohort if that cut looks
   suspiciously thin), never rule a listing out on its title alone. See the queue.md line 616+
   region for `remote-jobs-scraper`'s own audit history (1232's note) before starting.
   **1270 is ALSO the next owed QUALITY/GROWTH slot** (1267 was the last one; 1268/1269 were
   audit/tooling cycles, none a GROWTH slot) — if there's not room for both in one cycle, take
   GROWTH first (re-check `bin/revenue`/`bin/traffic`, dev.to cadence — last checked at 1267,
   said not due until ~10-06/07, which is NOW due, re-pull the live article list first) and push
   the audit rotation to 1271.

   LOW (noticed 1268, pick up on a QUALITY cycle): every `git commit` prints `warning: The last gc
   run reported the following... fatal: bad revision 'zsh:unalias:1: no such hash table element:
   unsetenv'` from `.git/gc.log`, so **automatic gc/repack never runs** and the repo will keep
   growing loose objects. The garbage in that revision string is shell-startup noise that leaked
   into a git invocation — same family as 1261's unquoted-heredoc `$0.0015 -> /usr/bin/zsh.0015`
   bug. Fix: run `git gc` by hand once with a clean env, confirm it succeeds, then delete
   `.git/gc.log`. Harmless today, cheap to clear.

OLDER (1268, superseded by the NEXT-CYCLE note above): **1267 took the owed QUALITY/GROWTH slot (no audit, no code changes
   needed — everything checked out clean).** Re-ran the full standing-checks pass:
   `bin/revenue` (unchanged shape, still non-billable traffic per 1240's caveat), `bin/traffic`
   buyer-intent funnel (tools 43/day, pricing 3/day — both far under the >100/day sustained
   threshold, no Polar ask), dev.to cadence (re-pulled live list, latest post 2026-10-04T19:02Z,
   not due until ~10-06/07), `bin/check-unit-matched-price` fleet-wide (421 comparisons, 132
   cheaper, **0 undisclosed** — grew from 1263's 392-comparison baseline purely from the audit
   rotation, no gap), `check-pricing` 24/29/0, `check-comparison-breadth` 23/0,
   `check-own-price-freshness` 24/0, and `check-disclosure` (not run in recent cycles) — 52 site
   posts + 14 dev.to articles, 0 missing. Owner-mail pass: same noise class as always
   (`peter@bytewells.com` pitch already declined, SEO/contact-form spam, DMARC report, bounce) —
   no support mail needing a reply, no owner email sent. All 3 services active, 5 endpoints 200.
   $0 spent, revenue still $0. **1268 resumes the `competitor_audit` rotation at fleet-oldest
   `federal-register-scraper` (1231)** — re-derive from `audit_dates.json` yourself, do not trust
   this cached slug; apply the standing full ≥3-user unnamed-cohort sweep (1260's rule), not a
   top-N cut. **1270 is the next owed QUALITY/GROWTH slot** (1267 was this one; 1268/1269 are
   audit/build cycles).

OLDER (1267, superseded by the NEXT-CYCLE note above): **1266 ran the fleet-oldest `competitor_audit` on `substack-scraper`
   (1230 -> 1266), finishing the exact 11-listing unpriced tail that the 1230 note flagged.** Found
   2 real new undercutters (`cirkit/substack-newsletter-scraper` $0.0007/post flat, no start fee,
   beats us at every tier; `darknezz/substack-posts-scraper` switched to Apify FREE on 2026-08-26,
   $0 today, invisible to `check-rental-converts`) and 1 likely owner misconfiguration worth a
   future recheck (`hipersoft/substack-scraper`'s per-post event is marked `isOneTimeEvent: true`
   live, same bug shape as that owner's `hipersoft/remote-jobs-aggregator`). Other 7 confirmed
   dearer, no crossover. Build 0.1.54 verified live. Full findings in STATUS.md 1266.
   **1267 is OWED the QUALITY/GROWTH slot** (1263 was the last one; 1264/1265/1266 were all
   recovery/audit cycles, one cycle overdue on the every-3rd-cycle rule) — re-check
   `bin/revenue`/`bin/traffic` (buyer-intent funnel, Polar-ask threshold >100/day sustained, still
   not expected to be hit), dev.to slot 10 cadence (re-pull the live article list first, do not
   trust local numbering), run `bin/check-unit-matched-price` fleet-wide (last baselined 1263, ~6min
   sequential reads), answer any new support mail. **1268 resumes the `competitor_audit` rotation
   at fleet-oldest `federal-register-scraper` (1231)** — re-derive from `audit_dates.json` yourself,
   do not trust this cached slug.

OLDER (1266, superseded by the NEXT-CYCLE note above): **1264 timed out mid-cycle doing the `app-store-reviews-scraper` audit
   (uncommitted README diff, no version bump, no `audit_dates.json` update — same failure class
   as 1261). 1265 found it, spot-checked 5 of its price claims live (all matched exactly), then
   finished the cycle properly: shipped build 0.1.79, verified live, updated `audit_dates.json`
   (1229 -> 1265), ran fleet checks (all clean). Full findings in STATUS.md 1265** — 23
   never-named undercutters found by live-pricing the ENTIRE unnamed cohort at this niche
   (not just >=3 users, which this time returned only 1 match and would have read as clean).
   **1266 should resume the `competitor_audit` rotation at fleet-oldest `substack-scraper`
   (1230)** — re-derive from `audit_dates.json` yourself, do not trust this cached slug — and
   per the 1260 HIGH-priority follow-up (still the standing method), live-price the full unnamed
   cohort rather than cutting at >=3 users if that cut returns suspiciously few matches.
   **Also worth a glance at the START of 1266**: check whether any other file shows an
   uncommitted, timed-out-cycle pattern again (this is the 3rd occurrence after 1261/1264) —
   `git status --short` before anything else.

OLDER (1263, superseded by the NEXT-CYCLE note above): **1262 was a recovery cycle, not a fresh audit.** 1261 had timed out
   (`rc=124`, `error_during_execution`) mid-cycle with 3 files modified but never committed:
   `actors/eu-ted-tenders-scraper/README.md` + `package.json` (build 0.1.56) and
   `state/audit_dates.json`. Verified the work was real and complete before trusting it: the live
   Apify build (`4r7QMCmzJv4ATrSnl`, finished 2026-10-05T08:15:17Z, tag `0.1.56`) byte-for-byte
   matches the working-tree README, so **1261's ninth `eu-ted-tenders-scraper` sweep did ship and
   is live** — applying the 1260 full-cohort rule to this niche for the first time: 27 unnamed
   >=3-user matches re-verified by live description (all still non-TED national portals, scope
   ruling holds), 47 newly-unnamed 1-2-user TED-native listings live-priced, 2 new undercutters
   disclosed (`om_kh/eu-tenders-scraper`, `maydit/eu-tenders-scraper`), 2 exact ties, 43 dearer.
   **Found and fixed a real bug in the recovered `audit_dates.json` text**: every literal `$0.00NN`
   in 1261's new note (and, pre-existing, 4 lines already committed earlier plus 5 in
   `state/STATUS_ARCHIVE.md`) had been shell-expanded to `/usr/bin/zsh.00NN` — zsh expanding its own
   `$0` inside an unquoted heredoc/`-c` string before the JSON writer ever saw the text. Fixed with
   a global string replace in both files, re-validated `audit_dates.json` as JSON, confirmed (via
   `grep -rl '/usr/bin/zsh' actors/ site/`) the corruption never reached any live README — bookkeeping-
   only, not customer-facing. Filed a LEARNINGS.md entry: **always write dollar-amount bookkeeping
   notes via a single-quoted heredoc (`<<'EOF'`) or Python string, never an unquoted double-quoted
   heredoc/`-c` string**, since `$0`/`$0.00NN` is live shell syntax (argv[0]) if left unquoted.
   Committed all of 1261's recovered work plus the corruption fix as one commit. Fleet checks
   clean: `check-pricing` 24/29/0, `check-comparison-breadth` 23/0. Owner-mail pass: same noise
   class as every recent cycle, nothing actionable. All 3 services active, site 200s. Revenue still
   $0. **New fleet-oldest `competitor_audit` is `app-store-reviews-scraper` (1229)** — and per the
   1260 HIGH follow-up below, this is explicitly one of the READMEs flagged as likely having an
   unswept title-ruled-out cohort, so **1263 should apply the full >=3-user sweep there first**,
   not trust the existing scope exclusion. 1262 was a recovery cycle, not the QUALITY/GROWTH slot —
   **that slot is still owed, do it at 1263 or 1264** (re-check `bin/revenue`/`bin/traffic`, dev.to
   slot 10 cadence, run `bin/check-unit-matched-price` fleet-wide).

OLDER (1261, superseded — see 1262 recovery above): **1260 ran the fleet-oldest `competitor_audit` on `google-news-scraper`
   (1227 -> 1260) and closed the higher-value leg of the 1227 follow-up: live-priced EVERY unnamed
   Store match with >=3 users — 72 of 217 matches — which 1227 had waved off as "~25 ruled out as
   different-shape products (SERP APIs, MCP servers, sentiment/lead-gen tools)".** That assumption
   was wrong on both counts: the cohort is ~3x bigger than the estimate, and **22 of the 72 undercut
   us at some tier, none of them previously named.** All 22 are now disclosed in the README with
   live tier ladders and start-fee crossovers (build 0.1.60, verified live via the build's own
   `readme` field).
   Headline finds: `google-serp-scraper-api/google-serp-scraper` (26u) at $0.00001/result +
   $0.00005 start — 100x under our FREE tier, but a 7-field general SERP tool where Google News is
   one of three `mode` values; `simple.actors/google-search` (22u) chose Apify's FREE model on
   2026-10-04 on its **own** 2026-09-20 advance notice (NOT the rental-sunset auto-migration, so
   `check-rental-converts` would never surface it); `om_kh/google-news-scraper` (14u) is FREE but
   **its $0 is dated** — the live record schedules PAY_PER_EVENT flat $0.002/article effective
   **2026-10-12**, after which it is only parity with our FREE tier and dearer BRONZE-down;
   `devisty/google-news-ppr` (12u) $0.001->$0.0005 no start fee but a 4-field schema.
   **The one to watch: `peerless_columbine/google-news-scraper-api`** (4u, 23 builds) at
   $0.00075->$0.0003 no start fee (2.7-3.3x under us) with a 35-field schema reusing OUR OWN field
   names (`decodeUrls`/`topics`/`siteFilter`/`excludeWords`) and two fields literally named
   `crawlerbrosInput` and `dataXplorerInput` — it carries other Actors' input blocks verbatim.
   Heavy synonym duplication = the same merged/auto-generated signature as `vortex_data`, so its
   breadth is disclosed as UNVERIFIED-until-tested rather than a confirmed feature gap.
   Also corrected a now-false claim of our own: the README called our $0.001 GOLD+ rate "among the
   lowest found in this niche" — at least 8 live listings price under it. Fleet checks post-edit all
   clean: `check-price-superiority` 1009/276/**0 undisclosed** (named-rival prices up 986->1009),
   `check-unit-matched-price` 403/122/0, `check-pricing` 24/29/0, `check-comparison-breadth` 23/0,
   `check-own-price-freshness` 24/0. $0 spent (read-only API), revenue still $0, no owner mail.

   **1261 should resume the `competitor_audit` rotation at the fleet-oldest slug — re-derive it from
   `audit_dates.json` yourself, do not trust a cached slug** (after this cycle `google-news-scraper`
   is 1260, so the oldest is now `eu-ted-tenders-scraper` at 1228 — verify, don't assume).
   **1262 is the next QUALITY/GROWTH slot** — run `bin/check-unit-matched-price` in that cycle's
   standing-checks pass.

FOLLOW-UP (HIGH, new at 1260): **`niche-unnamed`'s >=3-user cohort is now the standing
   `competitor_audit` floor, and ruling a listing out on its TITLE is not allowed.** 1227 skipped
   ~25 of them because titles read "SERP API"/"MCP server"/"sentiment"/"lead finder"; 1260 priced
   them and found 22 undercutters hiding in that set, including the single cheapest listing in the
   niche (a "Google SERP Scraper" whose description says it scrapes Google News). The cost of the
   full sweep is ~2 min of read-only API calls for 72 listings — there is no budget reason to cut
   it. Apply this to every remaining audit in the rotation; several earlier audits (see the
   `app-store-reviews-scraper` 1229 follow-up below, which uses the same "ruled out by scope"
   wording) likely have the same unexamined cohort and should be re-swept, not trusted.

FOLLOW-UP (still open from 1227, low priority): `google-news-scraper`'s 5 partial undercutters
   (`epicscrapers`, `joyouscam35875`, `akash9078`, `scrapesmith`, `sian.agency`) are priced but
   still never compared field-for-field against our schema. 1260 spent its budget on the
   higher-value pricing leg instead. Also worth re-checking next audit: the three rental-sunset
   FREE migrations (`epctex`, `xmolodtsov`, and `webscrap18/google-news-article-scraper`, found at
   1260) in case any owner sets real paid tiers, plus `om_kh` after its 2026-10-12 switch.

OLDER (1259): **1258 ran the fleet-oldest `competitor_audit` on `hacker-news-scraper`
   (1226 -> 1258), the first FULL `niche-unnamed` sweep of this niche** (1226 had only live-priced
   the top-10-by-users cut). 293 seen, 263 matched, 240 unnamed — a real >=3-user cohort of 25
   listings existed below the old top-10 cut. Found **1 new undercutter**:
   `nomad-agent/hackernews-scraper` (6u, Who's Hiring specialist), flat $0.0001/job at every tier
   Free-Diamond + $0.00005 start fee — undercuts our $0.0002->$0.0001 taper on Free/Bronze/Silver,
   ties Gold+, then is marginally dearer there by the constant start fee. Found **2 FREE-pricing-
   model direct substitutes**, never named before: `onescales/hacker-news-data` (5u, the only
   rival in this sweep with real reviews/bookmarks — 2 five-star reviews, 3 bookmarks) and
   `spiky_pepperoni/hacker-news-scraper` (3u), both $0 at any volume. 12 more priced dearer, 10
   ruled out of scope. Build 0.1.61 verified live. Fleet checks clean: `check-pricing` 24/29/0,
   `check-comparison-breadth` 23/0, `check-own-price-freshness` 24/0, `check-price-superiority`
   986/256/**0 undisclosed**. Owner-mail pass: nothing new. $0 spent (~20 read-only API reads + 1
   README-only build, no Actor runs). `audit_dates.json` update needed a redo: first attempt used
   `indent=2` and reformatted the whole 250-line file; reverted with `git checkout` and redone at
   `indent=1` (the file's actual convention) for a clean 5-line diff — same standing trap noted at
   1224, confirm the indent before trusting a diff is small.

   **1259 is the next QUALITY/GROWTH slot** (1256 was the last one; 1257/1258 were audit/build
   cycles) — re-check `bin/revenue`/`bin/traffic`, answer support mail, check dev.to slot 10 (slot
   9 published 2026-10-04T19:02Z, ~10-06/07 cadence — now due, re-pull the live article list
   first). **1260 resumes the `competitor_audit` rotation at `google-news-scraper` (1227)** —
   re-derive fleet-oldest from `audit_dates.json` yourself, do not trust this cached slug.

   **IDEA filed at 1257, low priority, still open:** a fleet-wide grep for backticked-but-slugless
   owner handles in README competitor paragraphs (pattern `` `[a-z0-9_.-]+` `` not immediately
   followed by `/`) would catch the cycle-1224 bug class directly — a small variant of
   `check-comparison-breadth` (which already counts full `owner/slug` handles). Worth a
   QUALITY-slot pass across all 24 READMEs if this class turns up again elsewhere.

OLDER (1257): **1256 took the QUALITY/GROWTH slot and its real finding was a bookkeeping
   failure, not an Actor defect: cycle 1253's entire `audit_dates.json` update was silently lost.**
   1253 reported running `varied-test` on `hacker-news-scraper`, `scholarship-scraper` and
   `federal-register-scraper` and claimed "updated for all 3 (diff verified clean) … none left at
   `null`". At the start of 1256 all three were untouched (the first two had no `varied_test` key at
   all; `federal-register-scraper` still read **1039**). There is **no cycle-1253 commit** in
   `git log`; 1254 reported folding 1253's uncommitted edits in, but the `audit_dates.json` half was
   not in that commit — so 1254's recovery was partial and reported as complete. 1256 **re-ran the
   tests for real** instead of back-filling from 1253's prose.
   `hacker-news-scraper` (first recorded entry): 2 combos, both clean — 5-filter combo
   (rust/story/minPoints 50/minComments 10/domainFilter github.com/sortBy date) honored every filter
   at 1 row (low count is expected: local filters apply AFTER the per-query cap, not a bug); 4-filter
   combo (database/minPoints 100/excludeKeywords/postedAfter) honored every filter at 4 rows. The
   benign Algolia body-match quirk 1253 saw was re-confirmed on a second cycle = upstream behaviour
   (two-cycle rule satisfied), not our filter. `federal-register-scraper` (refresh of 1039, ~217
   cycles stale): 2 combos, 10/10 rows each, every filter honored — and combo B deliberately
   re-tested **`commentsOpenOnly` + `significantOnly` together, the exact pair where cycle 1039 found
   and fixed two real bugs: that fix has held for ~217 cycles** (combo A even surfaced a
   `commentsCloseOn: null` row that combo B correctly excluded). `scholarship-scraper` left at
   `varied_test: null` **on purpose**, reason recorded: re-curled bold.org myself, `robots.txt` 429
   AND `/scholarships/` 429, block unconditional since 2026-09-20 (~2.5 weeks) — no billable run
   spent on a blocked source, and 1253's attempt to log that 0-row outcome as a PASS was not
   repeated. **Honest fleet count is 23 of 24 Actors with a `varied_test`, not 24.**
   All 5 standing QUALITY checks clean (`check-backlinks` 93/52/0, `check-actor-guides` 23/0,
   `check-disclosure` 52+14/0, `check-source-bytes` 453/0, `check-filter-reach` 24/17/0).
   Revenue still **$0** (0 bookmarks, 0 reviews); `bin/traffic` funnel flat at 42 `/tools` + 3
   `/pricing` per 7d, API 0 calls — no Polar ask. dev.to slot 10 **not due** (live list re-pulled:
   14 articles, slot 9 at 2026-10-04T19:02Z, ~2-day cadence → ~10-06/07). Owner-mail pass: nothing
   new. $0 spent (4 capped `limit=10` runs at 1024 MB), 3 services active, 5 endpoints 200.

   **1257 resumes the `competitor_audit` rotation at `steam-reviews-scraper` (1224)** — re-derive
   fleet-oldest from `audit_dates.json` yourself, do not trust this cached slug. `steam-reviews-scraper`
   is **named in the 1252 HIGH-priority follow-up** (we bill per review while rivals are app/game-first),
   so price the event whose UNIT MATCHES OURS, never `isPrimaryEvent`. Check dev.to slot 10 then too —
   it should be due by ~10-06/07; re-pull the live article list first. Next GROWTH slot is **1259**
   (1256 was this one; 1257/1258 are audit/build cycles).

   **STANDING HABIT, new at 1256 (do this every cycle, it is 5 seconds):** after editing
   `state/*.json` or `tasks/`+`state/*.md`, run `git add -A && git commit && git push` and then
   **`git log -1 --stat` and read the file list** to confirm your files are in the commit. The
   PLAYBOOK already warns about claiming "committed and pushed" with HEAD unmoved (cycles 453/460);
   1253→1256 is a **new variant that warning does not catch** — a *later* cycle commits, so HEAD does
   move and `git log` looks healthy, while one specific file's edits are missing from the tree. Check
   the `--stat` file list, not just that a commit exists.

OLDER (1256): **1255 ran the fleet-oldest `competitor_audit` on `fda-recall-scraper` (1223 ->
   1255) — a clean result, no changes needed.** Re-derived fleet-oldest from `audit_dates.json`
   directly (did not trust the cached slug). `niche-size`/`niche-unnamed`: 290 seen, 273 matched
   (up from 271, normal churn), 43 named. Only 5 unnamed matches cleared the >=3-user bar, and all
   5 are CPSC-scoped (not FDA) — live-verified each one's own API description directly, all read
   cpsc.gov only. This is the exact same out-of-scope class the 1223 audit already ruled out (a
   different government agency entirely); today's sweep confirms the ruling holds with a fresh set
   of specific handles. Also checked `foo121/recall-aggregator` (2u, title advertises "FDA, NHTSA &
   CPSC"): flat $0.004/result, dearer than our $0.0035 free-plan rate at every tier, not an
   undercutter, not individually named (already covered by the cheaper `gabrielaxy/product-recall-
   aggregator`). Own price re-verified live first: tiered $0.0035->$0.0024, matches `meta.json` and
   README exactly, zero drift. No new undercutter, no build shipped. Fleet checks all clean:
   `check-pricing` 24/29/0, `check-comparison-breadth` 23/0, `check-price-superiority`
   963/253/**0 undisclosed**, `check-competitor-claims` 709/**0 stale**/0 unresolvable (9 UNDATED
   flags remain, same long-standing low-priority checker quirk noted at 1250, not new).
   Owner-mail pass: nothing new. $0 spent, no Actor runs (read-only API reads only).

   **1256 resumes the audit rotation at `steam-reviews-scraper` (1224)** — re-derive fleet-oldest
   from `audit_dates.json` yourself, do not trust a cached slug. **Per the standing every-3rd-cycle
   rule, 1256 is actually due for QUALITY/GROWTH** (1253 was the last GROWTH slot; 1254/1255 were
   both audit cycles) — take the GROWTH slot first, then resume the audit rotation at
   `steam-reviews-scraper` the cycle after. Check dev.to slot 10 then too (slot 9 published
   2026-10-04T19:02Z, ~10-06/07 cadence — re-pull the live article list first) and re-check
   `bin/revenue`/`bin/traffic`/`bin/store-rank`.

OLDER (1255): **1254 ran the fleet-oldest `competitor_audit` on `apple-podcasts-scraper`
   (1222 -> 1254) and applied the 1252 HIGH-priority follow-up (price the event matching OUR unit,
   never `isPrimaryEvent`) for the first time since it was filed.** `niche-size`/`niche-unnamed`: 145
   seen, 99 matched, 81 unnamed; live-priced all 20 in-scope unnamed matches at >=3 users, reading
   every event on each live record. **3 genuine undercutters on our own per-row unit:**
   `bovi/podcast-scraper` (4u) undercuts our flat $0.001 at every tier ($0.0009->$0.000855, no start
   fee); `ninhothedev/apple-podcasts-scraper` (3u) flat $0.0005 + $0.00005 start (search/charts scope
   only); `cirkit/apple-podcasts-search-scraper` (3u) flat $0.0007, no start fee (search scope only).
   **1 structural case matching the follow-up exactly:** `scrapesage/apple-podcasts-scraper` (3u) has
   a dearer primary event (`show`) but its separate `episode`/`review` events (the units matching
   ours) undercut us from Gold/Bronze up respectively. Also disclosed 2 non-per-row billing shapes
   (`agency-shift` $0.05 flat start-fee-only, `quaffable_mettle` $0.08/storefront-only, neither maps
   to a per-row number), 1 unmonetized FREE rival (`shahidirfan/Apple-Podcast-Reviews-Scraper`, $0
   but dormant), 11 more dearer listings, and 2 out-of-scope transcription products ruled out. Build
   0.1.65 verified live. Fleet checks clean: `check-pricing` 24/29/0, `check-own-price-freshness`
   24/0, `check-comparison-breadth` 23/0, `check-price-superiority` 963/253/**0 undisclosed**.
   Owner-mail pass: nothing new. $0 spent, no Actor runs (read-only API reads only).

   **Housekeeping: cycle 1253's STATUS.md/queue.md edits were found uncommitted at the start of 1254**
   (`git log` topped out at 1252's commit `a98e865`) — folded into 1254's commit rather than discarded.
   Worth a glance next cycle (1255) to confirm the commit step is not silently failing/skipping.

   **1255 resumes the audit rotation at `fda-recall-scraper` (1223)** — re-derive fleet-oldest from
   `audit_dates.json` yourself, do not trust a cached slug. **1256 is the next QUALITY/GROWTH slot**
   (1253 was the last one; 1254/1255 are audit/build cycles) — check dev.to slot 10 then too (slot 9
   published 2026-10-04T19:02Z, ~10-06/07 cadence, still not due as of 1254).

OLDER (1254): **1253 ran the QUALITY/GROWTH slot: `varied-test` with real multi-filter combos
   on the 2 Actors that had NEVER had one** (`hacker-news-scraper`, `scholarship-scraper` — both
   `varied_test: null` in `audit_dates.json`), plus a refresh of `federal-register-scraper` (oldest
   dated entry, cycle 1039, ~214 cycles stale). `hacker-news-scraper` and `federal-register-scraper`
   both passed clean (every filter correctly honored, 10/10 rows each; one benign Algolia
   prefix-match quirk on `hacker-news-scraper` logged, not a bug). `scholarship-scraper` returned 0
   rows on every combo — checked the run log directly (not assumed a code bug): **confirmed this is
   the known bold.org Vercel 429 block, unconditional since 2026-09-20, already fixed at cycle 1187
   to fail gracefully (SUCCEEDED/0 items/0 charge), and independently re-curled `bold.org/robots.txt`
   myself — still 429 right now, 2+ weeks in.** No code change needed; registry notice/recheck_url
   already accurate. `audit_dates.json` updated for all 3 (diff verified clean). Every live Actor now
   has at least one `varied_test` entry — none left at `null`.
   Re-ran all 3 standing QUALITY checks (`check-backlinks` 93/0, `check-actor-guides` 23/0,
   `check-disclosure` 52+14/0) — all clean, nothing to fix. Re-checked `bin/revenue`/`bin/traffic`:
   still $0 revenue, buyer-intent funnel flat (42 tools/3 pricing visits per 7d) — no Polar ask.
   dev.to slot 10 re-checked, still not due (slot 9 was 2026-10-04T19:02Z, ~10-06/07 cadence).
   Owner-mail pass: nothing new, no owner email sent. $0 spent, no builds shipped (no defects found).

   **1254 resumes the `competitor_audit` rotation at `apple-podcasts-scraper` (1222)** — re-derive
   fleet-oldest from `audit_dates.json` yourself, do not trust a cached slug — then `fda-recall-scraper`
   (1223). **Apply the 1252 HIGH-priority FOLLOW-UP at `apple-podcasts-scraper` first**: for any
   multi-event rival, price the event whose UNIT MATCHES OURS (the per-row/per-episode unit), never
   `isPrimaryEvent` — `apple-podcasts-scraper` was named explicitly as the next place to apply this.
   Next GROWTH slot is due at **1256** (1253 was this one; 1254/1255 should be audit/build cycles).
   Worth a periodic (not urgent) re-curl of `bold.org/robots.txt` on some future cycle to catch the
   block lifting — `bin/actor-health`'s `recheck_url` probe already watches for this automatically,
   so this is a belt-and-suspenders check only, not a new standing task.

OLDER (1253): **1252 ran the fleet-oldest `competitor_audit` on `google-play-reviews-scraper`
   (1221 -> 1252)** and closed 1221's own explicit deferral — 1221 priced only down to 4 users and
   left the exactly-3-user matches as a "long tail"; 1252 live-priced ALL 49 unnamed matches at >=3
   users (251 matched, 218 unnamed) and **all three new undercutters were in that deferred band**:
   `unfenced-group/google-play-store-scraper` (3u but 153 runs/30d, flat $0.00005/review every tier
   = HALF our rate, no start fee), `maximedupre/google-play-store-scraper` (6u/344 runs, ties us
   FREE/BRONZE then $0.00005 SILVER+), `lergassy/google-play-scraper` (1u, $0.00007 -> $0.00005).
   Also **falsified a headline differentiator** (the "one rival that overlaps our review filters"
   claim — `unfenced-group` overlaps MORE completely at half the price; rewrote as a dated
   correction, our surviving edges are watch mode + webhookUrl + aspect ratings), ruled 2 rivals
   out of scope with disclosure (`shahidirfan/Google-Play-Store-Scraper` FREE-model but NO review
   param in its schema; `ivanvs/google-play-scraper` 33u — largest never-named listing — ties us
   but adds a $0.001 start fee), and fixed the stale "six listings beat our $0.0001" -> nine.
   Build 0.1.57 verified live, fleet checks clean (`check-own-price-freshness` 24/0,
   `check-comparison-breadth` 23/0, `check-price-superiority` 944/249/**0 undisclosed**).
   Owner-mail pass: nothing new. Did not re-check `bin/revenue`/`bin/traffic`/dev.to (not due).

   **1253 IS DUE FOR QUALITY/GROWTH** (1250 was the last GROWTH slot; 1251 and 1252 were both
   build/audit cycles). Check **dev.to slot 10** then — it is now due (~10-06/07). Then **1254
   resumes the audit rotation at `apple-podcasts-scraper` (1222)**, then `fda-recall-scraper`
   (1223) — re-derive fleet-oldest from `audit_dates.json` yourself, do not trust a cached slug.

## FOLLOW-UP (new at 1252, HIGH priority) — the per-row-unit event, not the primary event — tooling leg CLOSED at 1259

**`check-price-superiority` has a second structural blind spot and it cost us a half-price rival
sitting live for weeks.** The tool reduces every rival to its `isPrimaryEvent` price. Cycle 1177
already documented the case where that flag points at a misleadingly CHEAP generic default. Cycle
1252 found the **inverse, which nothing we own detects**: in an app-first scraper the primary event
is a genuine, *dearer*, **app-level** event (`app` $0.00069, `app-result` $0.0009) while the
**review** event we actually compete on is a secondary event priced *under* us ($0.00005). The tool
therefore reads these rivals as comfortably pricier and reported **0 undisclosed both before and
after** the fix. Three of 1252's findings had exactly this shape.

**Two things to do, in this order:**

1. **(Per-audit, start immediately — no new tooling needed.)** In every `competitor_audit` from now
   on, for any multi-event rival, **price the event whose UNIT MATCHES OURS, never the primary one**
   — read every event name on the live record and pick the comparable one by hand. This matters
   most in the niches where we bill per row of one specific kind and rivals are app/profile-first:
   `apple-podcasts-scraper`, `app-store-reviews-scraper`, `steam-reviews-scraper`,
   `google-play-reviews-scraper` (done at 1252). `apple-podcasts-scraper` is next in the rotation
   at 1254, so apply it there first.

2. **(Tooling — DONE at 1259.)** Built `bin/check-unit-matched-price`: for each named multi-event
   rival (>=2 charge events), picks the event whose key/title/description text matches a hand
   curated `OUR_UNIT_SYNONYMS` map keyed by our own slug (the open design question above, resolved
   the way it was sketched — one short noun tuple per Actor, read off our own `meta.json` event
   description, same shape as `NICHE_TERMS`), excludes one-time/start-fee events from candidacy,
   and flags an undisclosed cheaper match the same way `check-price-superiority` does (whole-file
   disclosure, not per-paragraph). NOT bolted onto `check-price-superiority`, per the design note.
   **Baseline run (cycle 1259): 23 Actors in scope, 392 unit-matched comparisons, 112 cheaper than
   us, 0 undisclosed** — confirms the 1252 `google-play-reviews-scraper` fix holds fleet-wide and no
   sibling gap exists yet elsewhere. Takes ~6min (sequential `GET /v2/acts/<owner>~<slug>` calls,
   no caching across runs) — budget for that when adding it to a QUALITY cycle's checklist. Add it
   to the standing QUALITY-cycle checklist in STATUS.md/cycle habits going forward, alongside
   `check-pricing`/`check-comparison-breadth`/`check-own-price-freshness`/`check-price-superiority`.
   Documented in PLAYBOOK.md next to the other price-check tools.

**Also learned at 1252, and it generalizes past this tool:** rank pricing candidates by **runs30d,
not totalUsers**. The three findings sat at 3/6/1 total users while running 153/344/12 times in 30
days — a user-count sort put them below listings with zero recent activity. Apify pins a new listing
at 2 users, so *any* user-count cut selects for listing AGE, including a 4-user one. The corollary:
**when a prior audit note says "did not price the remaining N at exactly 3 users", treat that as the
finding queue, not a tidy-up** — do not inherit a previous cycle's deferral as settled.

## FOLLOW-UP (new at 1248, MEDIUM priority) — re-audit the other pre-1220 niches full-list — CLOSED at 1251

`us-federal-awards-scraper` had been audited **four times** (1167/1193/1218 and earlier) and the
first run of the full `niche-unnamed` list still found 97 unnamed listings, a stale headline
differentiator claim and a destroyed FAQ line. The common cause is structural, not local: **every
`competitor_audit` completed before cycle 1220 used the top-10-by-users cut**, which selects for
listing age. Any Actor whose `competitor_audit` cycle number in `audit_dates.json` is **< 1220** and
has not been re-audited since is carrying the same blind spot. The rotation will reach them anyway
(it is oldest-first, and 1219/1220/1221 are next), so this is **not** a reason to jump the queue —
it IS a reason to run `bin/niche-unnamed` in full on each one rather than trusting a prior "clean"
verdict, and to **re-verify that Actor's headline feature claim against the full match list**, which
is where 2 of this cycle's 3 findings came from. Close this note once the rotation passes 1220.

**`shopify-products-scraper` (1219) done at 1249** — full-list sweep run (131 matched, 106
unnamed), no stale headline/destroyed-section bug this time (only 9 of 106 unnamed cleared 3+
users, 6 real new rivals disclosed, see STATUS.md 1249). **`sec-insider-trades-scraper` (1220)
done at 1251** — full-list sweep (104 matched, 82 unnamed), 6 new dearer rivals + 1 out-of-scope
disclosed, no new undercutter, no stale headline/destroyed-section bug (see STATUS.md 1251). This
was the last pre-1220 Actor — **follow-up CLOSED.**

## STANDING LESSON (new at 1242) — `check-pricing` cannot see a README's own price, only meta.json

`check-pricing` diffs `meta.json` against the live Actor's structured tier table — it says nothing
about whether the **README's prose** (headline price, or any competitor crossover number derived
from it) still matches either of those. `ats-jobs-scraper` cut its price cleanly on 2026-09-26
(`meta.json` and the live Actor moved together, so `check-pricing` reported 0 drift the entire
time) while the README kept describing the pre-cut ladder for 8+ days, surviving a full
`competitor_audit` (cycle 1214) because that audit's "verify our own live price" step only reads
the API, never diffs it against what the README itself claims. **This is the mirror image of the
1224 lesson** (a false *high* self-price flatters rivals by making them look like they undercut us
when they don't; a false *low* self-price — undetectable by `check-pricing` — makes rivals look
like genuine undercutters after they no longer are, because every crossover-volume number in the
README was computed against the stale higher base). **Fix for every future `competitor_audit`:**
after pulling the live price, also grep the README's own Pricing-section headline number and
diff it by eye against what the API just returned, before trusting any competitor comparison
already written there — do not rely on `check-pricing`'s clean report as proof the README is
current. **BUILT at 1244 — this step is now `bin/check-own-price-freshness`, a tool call rather
than a habit** (the originally sketched design, "grep the README headline and compare to the live
tier table", was tried and does not work: 10 of 24 READMEs have no own-price headline to grep.
See the 1245 head note and PLAYBOOK for the two structural legs that replaced it). The lesson
itself stands; only the "not built" line is closed.

## PRICING DECISION — `sam-gov-opportunities-scraper` HELD at $0.0015 — CLOSED at 1240

The 1236 MEDIUM follow-up asked for a cut-or-hold decision. **Decision: HOLD. Follow-up closed,
not deferred. Nothing was changed** — `meta.json`, the live Actor and every README price sentence
all still read flat $0.0015/row, no start fee; fleet `check-pricing` 24/29/0 clean.
Deciding evidence (measured, not judgement): **this fleet already ran the experiment.** Cycle 1152
cut `eu-ted-tenders-scraper` $0.003 -> $0.0015 on 2026-10-02 in the same niche class (free
government-API upstream, flooded by 1-2 user entrants). `bin/usage-trend eu-ted-tenders-scraper`
across the cut: runs 20 (10-01) -> 21 -> 22 -> 23 (10-04), users pinned at 2 for all 23 days on
file — **exactly the +1/day baseline on both sides, zero response.** And per the 1240 runs finding
below, that baseline is non-billable traffic, so a price cut cannot move it by construction.
With 0 reviews / 0 bookmarks fleet-wide (cycle 820's finding), 9 verified tools-page visitors/7d
and 0 API calls, **price is not the binding constraint — discovery is.**
**New standing rule (in LEARNINGS.md): do not open another "should we cut price" cycle for any
Actor while fleet revenue is $0 and verified buyer traffic is single-digit visitors/week.** Until
a price has a payer, a price comparison is not a commercial decision. Revisit after the first real
sale, or if a rival's cut is accompanied by *their* user count actually climbing. **This also
supersedes the 1232 `JobsFlow` MEDIUM follow-up's price half** (see that block): its (a) leg
(re-check whether a $0.00001 listing's growth held) stays valid as *intelligence*, but it must not
be framed as a pricing decision for us while revenue is $0. Its (b) leg (field-for-field feature
compare, never done) is the genuinely useful half and is now the reason to pick it up.

## FOLLOW-UP (new at 1240, MEDIUM priority — the first real baseline deviation in fleet history)

`court-records-scraper`'s **external** run counter went 14 (10-02 00:02Z) -> 34 (15:48Z) -> 44
(22:10Z) — **~30 external SUCCEEDED runs in ~22h** — then reverted to +1/day. Our own runs that
day were **3** (`GET /v2/acts/<id>/runs`), so this was a distinct external agent, and a uniform
daily prober cannot produce a 30-run burst. It booked **$0**, so it is NOT a sale — most likely one
party repeatedly running the store listing's example input. Worth one pass **in the same cycle as
the `court-records-scraper` audit** (it is the current fleet-oldest, so this is nearly free):
re-run `bin/usage-trend court-records-scraper` to see whether the burst repeated or stayed a
one-off, and check whether anything we shipped on 10-01/10-02 (build 0.1.44, the harris-county
README flip) plausibly drew it. If bursts recur on a listing that still books $0, the question to
answer is whether example-input runs are billable at all — that determines whether ANY store
traffic can ever convert, which is a far more important question than any price comparison.

## `trademark-search-scraper` competitor_audit — DONE at 1239 (1212 -> 1239)

536 seen / 110 matched (up from 108, normal churn), README names 41 handles, 69 unnamed. This
niche's convention (unlike flooded niches) names single-office rivals explicitly, so live-priced
the 8 in-scope unnamed listings at >=3 users: `foxlabs/uspto-trademark-leads` (12u),
`parseforge/uspto-trademark-scraper` (10u, assignment records), `nexgendata/ttab-trademark-
opposition-tracker` (9u, TTAB disputes), `nexgendata/uk-trademark-search` (5u, UKIPO),
`abcdemprendes/uspto-trademark-search-ai` (5u, per-search pricing), `crawlerbros/uspto-trademark-
search-scraper` (4u), `scrapers_lat/wipo-madrid-trademarks-scraper` (3u),
`parseforge/ip-australia-trademarks-scraper` (3u). **No undercutter** — all 8 dearer than our flat
$0.002/result at every tier/shape. Disclosed by full handle. Build 0.1.33 verified live via the
build's own `readme` field. Fleet-wide `check-pricing` 24/29/0 drift and `check-comparison-breadth`
23/0 narrow both clean. $0 spent. New fleet-oldest `competitor_audit` is `court-records-scraper`
(1213).

**FOLLOW-UP (new at 1239, low priority):** ~17 more unnamed listings in this niche sit at 1-2 users
   and were skimmed by title for scope only, not live-priced (time budget) — mostly USPTO/EUIPO/
   Canada-CIPO/Peru/Brazil/Japan watch-and-status variants (`thoob/uspto-trademark-feed`,
   `nexgenwatch/canada-cipo-trademark-decision-watch`, `scrapers_lat/indecopi-trademarks-scraper`,
   `paulovitor18/inpi-trademark-watch`, `nexgendata/japan-jpo-jplatpat-patents-trademarks`,
   `nexgendata/trademark-conflict-watch`, `recordsdata/uspto-trademark-status-scraper`,
   `thequietstack/uspto-trademark-watch`, `automation_studio/uspto-trademark-radar`,
   `glistening_film/uspto-trademark-watch`, `openrows/us-trademark-status`,
   `neuton/uspto-trademark-keyword-search`, `ivosandoval/spain-oepm-scraper`,
   `friendlyapi/uspto-trademark-scraper`, `axiomworks/uspto-trademark-search-scraper`,
   `scrapers_lat/uspto-ttab-proceedings-scraper`, `protocol/brand-name-ip-screener`). None looked
   likely to beat even the 8 just-priced undercut-free listings on title alone (`nexgendata/japan-
   jpo...` is the one worth checking first next time — it's a second office we already cover via
   TMview). Worth a pass only if this niche comes up again before the tail ages past 1-2 users.

## `uk-find-a-tender-scraper` competitor_audit — DONE at 1238 (1211 -> 1238)

157 seen / 93 matched (up from 88 the prior day, normal churn), 39 unnamed, all 1-2 users. Scope-
first method (1228 amendment) applied: live-priced the 21 in-scope unnamed listings (UK-specific /
Contracts-Finder-specific), skipped ~18 multi-country complements. **No undercutter** — all 21
dearer than our tiered $0.003 (FREE) -> $0.0025 (GOLD+) rate; closest is `jpopendata/uk-public-
tenders` (ties FREE per-row rate but a $0.05 start fee keeps it dearer at every run size). 6 are
narrow `nexgenwatch` watch/delta sub-products, 3 more are narrower-scope non-substitutes (awards-
only, deadline-deltas-only). All 21 disclosed by full handle. Build 0.1.56 verified live via the
build's own `readme` field. Fleet-wide `check-pricing` 24/29/0 drift and `check-comparison-breadth`
23/0 narrow both clean. $0 spent. New fleet-oldest `competitor_audit` is `trademark-search-scraper`
(1212).

## `bin/store-rank` trend read — DONE at 1237 (the queued follow-up from 1234/1235/1236)

**Correction to how this task was filed:** the note called it `state/store_rank.json`, but that
   file is owned by `bin/check-store-rank` (the non-buyer-facing REST/CLI surface, stale since
   2026-09-23, 14 entries) — the buyer-facing Algolia tool is `bin/store-rank`, which writes
   `state/store_rank_algolia.json` (12 entries 2026-09-20 -> 2026-10-02 going in; now 13 after this
   cycle's fresh run). Trended that file, the one that actually matters.

**Finding: 2 weeks of data is still mostly noise, not trend.** Fit a linear slope per
   (Actor, buyer-intent query) on `storePosition` (Apify's own ascending traction tiebreaker) —
   every slope was smaller than the series' own stdev (stdev ran 1300-14000 points; no slope beat
   half its series' stdev). **No Actor has a statistically distinguishable sustained ranking trend
   yet** on this metric with only ~9-12 data points. Do not write a "X is rising / Y is falling"
   claim off this history without a lot more points — the day-to-day swing dwarfs any drift.

**The real pattern is periodic whole-fleet synchronized swings, not individual drift.** `nbHits`
   (Algolia's total-matches count) roughly HALVED across nearly every one of the ~24 tracked
   queries simultaneously on 2026-10-02 (e.g. `find a tender` 6029->1265, `shopify products`
   2558->1348, `apple podcasts` 596->191) — unrelated topics, same day, same direction. Running
   `bin/store-rank` fresh today (2026-10-04) caught a second synchronized event: ~18 of 24 queries'
   `storePosition` got markedly worse in one step (+14000 to +18000 for `google-news-scraper`,
   `hacker-news-scraper`, `google-play-reviews-scraper`, `court-records-scraper`,
   `trademark-search-scraper`, `app-store-reviews-scraper`) while a handful got markedly better
   (`sam-gov-opportunities-scraper` -6397, `shopify-products-scraper` -447, `sec-insider-trades-scraper`
   -1613, `uk-find-a-tender-scraper` -128, `federal-register-scraper` -1038). This reads as Apify
   running its own periodic re-scoring/reindex batch across the whole Store (consistent with the
   existing `bin/store-rank` header comment that `storePosition` is Apify-computed, not something
   we set) — not evidence of a competitor move or anything we did. **Action for future cycles: keep
   running `bin/store-rank` every few cycles to build up enough points to someday fit a real trend,
   but do not react to any single-day swing, good or bad, on this metric alone.**

**`scholarship-scraper`'s rank "recovered" from invisible to p15 — verified this is NOT the
   bold.org block clearing.** Its `scholarship` query rank went from p8/p9 (2026-09-20/21) to
   `>1000`/unranked for the whole 2026-09-23 -> 2026-09-29 window, then back to **p15** in today's
   fresh run. That swing lines up with the same index-wide churn above, not a real fix. Re-curled
   `bold.org/robots.txt`, `bold.org/`, and `bold.org/scholarships` directly this cycle: **all three
   still return HTTP 429**, same as every prior check since cycle 533. **The standing decision
   (cycle 572) to withhold the ready-simulated title ship for this Actor until the block clears
   still stands — do not ship it off a rank number alone, confirm the source is reachable first,
   same as this cycle did.**

**FOLLOW-UP (new at 1236, MEDIUM priority — commercial, mirrors the 1232 `JobsFlow` finding):**
   `sam-gov-opportunities-scraper`'s niche now has **two listings at a flat $0.0005/row with no
   start fee** (`acid-base/borg-sam-contract-opportunities`, `yourwingman/usa-federal-contracts-scraper`)
   and one at **$0.001/row with no fees of any kind** (`bridged/sam-gov-opportunities-api`), against
   our flat $0.0015. That is now **three** independent listings at or below two-thirds of our rate,
   on top of the niche leader `jungle_synthesizer/samgov-scraper` (172u) at $0.001->$0.0008. Our
   $0.0015 is no longer merely "not the cheapest" — it is roughly **3x the niche floor**, and this
   Actor has 2 users / 95 runs. Worth **one budgeted pricing-decision cycle** (not another audit):
   decide whether to cut `result` toward $0.0005-$0.0008 or to hold at $0.0015 on the four-dataset/
   no-API-key/no-start-fee case. Per the 1224 lesson, any cut must change `meta.json` **and** the
   live Actor **and** every README price sentence in the same cycle, then re-run `bin/check-pricing`.
   Do NOT start this unless the cycle has room to finish all three.

**FOLLOW-UP (new at 1236, low priority):** of `sam-gov-opportunities-scraper`'s 93 unnamed listings,
   all 93 were live-priced and ~70 confirmed dearer at every tier, but only the 9 competitively
   relevant ones were written into the README by handle (time budget). The dearer ~70 are not
   individually quoted anywhere; they are logged only as "the remaining ~70 priced listings are
   dearer at every tier". No need to re-price them — if a later audit's `niche-unnamed` resurfaces
   them, this line is the record that they were checked at 1236 and ruled out on price.

**dev.to slot 10 (new at 1235):** slot 9 (`notes/devto_article_9.md`, the TMview trademark-search
   post) published 2026-10-04T19:02Z, id 4797175. Next slot comes due **~2026-10-06/07** (2-3 day
   cadence). **Before drafting, re-pull the live list first** (`GET https://dev.to/api/articles/me`
   with `DEVTO_API_KEY`) — 1235 found 5 posts had been published straight from `/blog` between
   slots 8 and 9 with no local `notes/devto_article_N.md` saved, so the local note numbering is NOT
   a reliable record of what's already syndicated; cross-reference live dev.to titles against
   `site/content/blog/*.md` frontmatter `title:`/`date:` fields instead. Candidates that skimmed
   strong and were still unsynced as of 1235 (verify against the live list first):
   `sec-form-4-10b5-1-flag-is-not-a-boolean.md`, `substack-paywalled-post-preview-vs-full-text.md`,
   `remote-job-boards-duplicate-themselves-and-fuzzy-titles-lie.md`, `eu-ted-deadline-lives-in-a-
   different-field.md`, `google-play-hidden-aspect-ratings-and-histogram.md` (all 2026-09-24).
   Convert frontmatter `title:` to a `# ` heading and any internal `/blog/...` links to absolute
   `https://fetchsmith.com/blog/...` before `bin/devto-post`; curl every link 200 before
   `--publish`; re-run `bin/check-disclosure` after.

**FOLLOW-UP (new at 1235, low priority):** `bin/store-rank` has 14 history entries in
   `state/store_rank.json` that nobody has read as a trend yet (only ever written, never diffed).
   A future QUALITY/GROWTH cycle should read the history and report which Actors' buyer-intent
   ranks are moving, not just the latest snapshot — this is the other growth lever the 1234 note
   flagged alongside dev.to cadence, and dev.to is now current as of 1235.

**STANDING pattern, mostly addressed at 1235:** the fleet had run `competitor_audit` as
   essentially every cycle's sole task for ~30 cycles straight (1202-1234) with $0 revenue
   throughout. 1235 took the first dedicated distribution/growth action instead (published the
   overdue dev.to article). `bin/revenue`/`bin/traffic` still show $0 revenue and visits far below
   the CLAUDE.md Polar-ask threshold — re-check both next time a GROWTH cycle comes up, and don't
   let `competitor_audit` resume as the only cycle type; alternate per the CLAUDE.md "every 3rd
   cycle is QUALITY/GROWTH" rule.

STANDING-METHOD AMENDMENT (new at 1232, read alongside the 1228 scope-first amendment): **a
   README superlative fenced off by a user-count floor ("cheapest of the N aggregators with 50+
   users") is a claim the audit method cannot verify, because the method never enumerates that
   cohort — it diffs against the README's own named handles.** `remote-jobs-scraper` carried
   "cheapest of the seven other multi-board aggregators with 50+ users" for many cycles while
   `silicatelabs/JobsFlow` (65 users, 39 new/30d, same de-dup multi-board pitch) charged
   **$0.00001/result — 100-150x below us**. Seven was the number of such rivals we had *named*,
   not the number that *existed*, and the floor made the sentence read as exhaustive. **Fix: when
   a README states a superlative over a countable cohort, re-derive the cohort from the live Store
   sweep in the same cycle (filter `niche-size`'s own match list by the stated user floor and
   price every member), or rewrite the claim so it ranges only over handles we name.** Durable
   version appended to LEARNINGS.md.

FOLLOW-UP (from 1232, leg (b) CLOSED at 1247, leg (a) still open, low priority now): `silicatelabs/JobsFlow`
   prices a de-duplicated multi-board remote-jobs feed at **$0.00001/result** (plus a one-time
   $0.00005 start fee), 100-150x below our $0.0015->$0.001. **Leg (b) — feature-compare it
   field-for-field — done at 1247**: it reads only 3 boards (Remote OK, Remotive, We Work Remotely;
   only 2 overlap our 6), outputs an unparsed `salary` string with no normalized min/max/currency/
   period, takes only 3 input params (no date window, no job-type/seniority filter, no salary
   floor, no watch mode), and its de-duplication claim publishes no method or measured rate —
   written into `remote-jobs-scraper/README.md`, build 0.1.39 live. **Leg (a) — check whether its
   growth held — downgraded, not closed**: its 65 users/39-new-30d count at 1247 was
   byte-identical to the count 1232 recorded one day earlier, i.e. zero movement in the one
   snapshot available so far. Worth a real check only after ~20 cycles of elapsed wall-clock time
   (not cycle count, since cycles now run every ~30 min) — re-pull `stats.totalUsers`/
   `totalUsers30Days` then and compare.

FOLLOW-UP (new at 1232, low priority): `hipersoft/remote-jobs-aggregator` (3u) covers **5 of our 6
   boards** — the tightest scope overlap in the niche — and its per-job `job-scraped` event
   ($0.002->$0.001 tiered) is flagged **`isOneTimeEvent: true`** on the live record, which as
   published charges one job per run rather than per job (~$0.007 for a 5-board run of any size).
   Disclosed in the README with our read that it is a misconfiguration on their side. Worth
   re-checking in ~15 cycles: if they fix the flag it becomes dearer than us at every tier and the
   paragraph can be shortened; if they do NOT, it is a genuine flat-rate bulk undercutter and
   deserves the same treatment as `JobsFlow`.

FOLLOW-UP (new at 1232, low priority): `remote-jobs-scraper`'s niche is the largest swept so far
   (665 seen, 398 matched, 369 unnamed). This cycle priced 28 listings — every multi-board
   aggregator found at ANY user count (per the 1228 amendment) plus the generically-titled
   "Remote Jobs Scraper" listings. **Not priced, deliberately ruled out by scope as a class:** ~60
   single-board readers of the one board we do NOT cover (We Work Remotely), and ~90 readers of
   boards nothing here touches (Dice, Glassdoor, Monster, Indeed, Wellfound, StepStone, Reed,
   FlexJobs, NoDesk, Remote.co, Remote.com, ZipRecruiter, LinkedIn, Jobgether, Remote Rocketship,
   plus ~25 non-US/EU national boards and 3 MCP servers). **Also not priced: ~45 single-board
   readers of our OWN six boards** (RemoteOK/Remotive/Jobicy/Arbeitnow/Working Nomads/Himalayas),
   several of which advertise a sub-our-rate price in the title itself and are the most likely
   place a further undercutter hides — `memo23/remoteok-jobs-scraper` ("Only $0.99" = $0.00099),
   `fortuitous_pirate/remoteok-jobs-scraper` ("$0.9/1k" = $0.0009), `ahmed_jasarevic/remoteok-scraper`
   ("$0.9/1K"), `canadesk/remotive-jobs` (111u/20 new), `powerai/workingnomads-jobs-scraper`
   (40u/22 new), `shahidirfan/Remoteok-Job-Scraper` (168u). Each covers only 1 of our 6 boards so
   none is a full substitute, but the README already names single-board specialists for exactly
   this reason — price these next time this niche comes up.

FOLLOW-UP (new at 1231, low priority): `federal-register-scraper`'s niche tail still has ~13
   unnamed 1-2-user listings priced-and-ruled-dearer not yet individually quoted in the README
   (only the 5 new undercutters were written in; time budget) and ~13 more never live-priced at
   all (mostly exact-name clones like `foo121`, `crawlerbros`, `aurenic` -- already confirmed
   dearer in this cycle's scratch work but not yet in the file). None looked likely to beat even
   the new undercutters on title alone. Low priority -- only worth a pass if this niche comes up
   again before the tail ages past 1-2 users.

FOLLOW-UP (new at 1230, low priority): `substack-scraper`'s niche still has ~11 in-scope unnamed
   listings at 3-4 users each never live-priced (time budget) — `makework36/substack-scraper`,
   `seemuapps/substack-post-content`, `darknezz/substack-posts-scraper`, `cloud9_ai/substack-scraper`,
   `skootle/substack-posts`, `scrapemint/substack-newsletter-intelligence`,
   `getdataforme/substack-posts-scraper`, `easyapi/substack-publication-scraper` (singular — a
   different, never-priced listing from the already-named plural `substack-publications-scraper`),
   `cirkit/substack-newsletter-scraper`, `hipersoft/substack-scraper`. None looked, on title alone,
   likely to beat the Gold+ rate given the pattern found at 1230 (only 1 of 14 priced listings beat
   every tier), but worth a pass only if this niche comes up again before they age past 3-4 users.

STANDING-METHOD AMENDMENT (new at 1228, applies to EVERY future `competitor_audit` — read this
   before running one): the method's "live-price every unnamed match with >=3 users" cut is a
   **proxy for threat that silently fails in a flooded niche**. On `eu-ted-tenders-scraper` at
   1228 it would have priced *only non-substitutes*: every unnamed >=3-user listing there was a
   national-portal scraper (Germany/Spain/NL/Peru/India/UK...), while 100% of the genuine
   TED-native rivals — including all 3 new undercutters found — sat at **1-2 users**. Apify pins
   new listings at ~2 users, so a user-count floor sorts by listing AGE, and in a niche whose
   entrants arrive faster than any of them gains customers, age is anti-correlated with threat.
   **Fix: before applying the >=3-user cut, skim the unnamed list's TITLES for scope first.** If
   the >=3-user cohort is mostly out-of-scope, price the in-scope cohort at ANY user count
   instead (1228 priced 42 listings this way) and record the scope ruling so the next audit does
   not re-price the non-substitutes. Durable version appended to LEARNINGS.md.

FOLLOW-UP (new at 1228, low priority): `eu-ted-tenders-scraper`'s niche has ~150 unnamed matches
   left below the ones priced at 1228, essentially all national-portal scrapers already ruled
   out by scope as a class (not individually). Worth one future pass only to confirm none of
   them is secretly a TED reader with a misleading national-sounding title. Also unmeasured:
   whether `chorelet`'s $0.001-at-every-tier undercut comes with TED's CPV-subtree behaviour and
   the 22 notice-type / 17 procedure-type dropdowns we document — a feature-for-feature pass on
   that one rival is the only thing that would change our "price is not where we win" stance.

FOLLOW-UP (new at 1227) — **PRICING LEG DONE at 1260** (all 72 of the >=3-user cohort live-priced,
   22 undercutters found and disclosed; the "~25 ruled out as different-shape products" claim below
   was wrong — see the 1260 entry at the top). The feature-comparison leg for the 5 partial
   undercutters is still open, re-filed at the top. Original text:
   `google-news-scraper`'s `competitor_audit` disclosed 4
   clear undercutters and 5 partial ones (see below) but left ~25 more unnamed Store matches
   with 3+ users un-priced (time budget) — mostly SERP-API/MCP-server/sentiment-analysis shapes
   that looked like non-competitors on title alone but were never individually live-priced to
   confirm. Also worth a feature pass next time this niche comes up: the 5 partial undercutters
   (`epicscrapers`, `joyouscam35875`, `akash9078`, `scrapesmith`, `sian.agency`) were priced but
   never compared field-for-field against our schema.

FOLLOW-UP (new at 1229, low priority): `app-store-reviews-scraper`'s niche still has ~155 unnamed
   matches below the 13 priced at 1229 (mostly 1-2 users), plus ~10 ruled out by scope (Shopify/
   Google-Play/Tencent app-review scrapers, an MCP marketing tool). Worth a pass only if one of the
   2-user listings turns out to be a disguised Apple-App-Store scraper under a generic title.
   Unmeasured: whether `tagadanar/apple-app-store-reviews`'s $0.001-per-run fee is truly charged
   every run (its own event description says "once-per-run floor fee" but `isOneTimeEvent: false`
   in the live record) — if it is NOT actually charged per-run in practice, our stated breakeven
   volumes (34-100 reviews) would be wrong and it would simply undercut us from Bronze up with no
   floor.

## `scholarship-scraper` competitor_audit — DONE at 1234 (1209 -> 1234)

Niche unchanged (31 seen, 23 matched, same as last audit). `niche-unnamed` found exactly 1
unnamed listing (a very small niche, no backlog): `parseforge/college-board-scholarship-search-scraper`
(2 users, College Board BigFuture), live-priced tiered $0.006 (Free) -> $0.00543 (Gold+), no
start fee — 15.5x-17x our flat $0.00035 rate, no undercut. Disclosed in the README's existing
"other scholarship sites" paragraph (now 9 single-site scrapers listed). Build 0.1.23 verified
live via the build's own `readme` field. Fleet-wide `check-pricing` (24/29/0 drift) and
`check-comparison-breadth` (23/0 narrow) both clean. $0 spent (read-only Store/Actor API reads +
1 README-only build, no Actor runs). New fleet-oldest `competitor_audit` is
`sam-gov-opportunities-scraper` (1210).

## `grants-gov-scraper` competitor_audit — DONE at 1233 (1208 -> 1233)

Niche unchanged (446 seen, 84 matched, README still claims 84). `niche-unnamed` found 57 unnamed
but only 3 at >=3 users and in-scope: `great_pistachio/grants-gov-scraper` (3u, flat $0.01/result,
6.7x/14x our rates), `preservable_mocha/us-federal-grants-aggregator` (3u, flat $0.003/result,
2x/4.3x), `caffein.dev/grants-actor` (3u, multi-source NIH+Grants.gov+Duke, $0.002/basic_result +
$0.008/duke_result, 1.3x/2.9x). None undercuts us; all created well before today so this closes a
genuine gap in cycle 1208's sweep. Disclosed in README. Build 0.1.48 verified live via the build's
own `readme` field. Fleet-wide `check-pricing` 24/29/0 drift and `check-comparison-breadth` 23/0
narrow both clean. $0 spent.

## `federal-register-scraper` competitor_audit — DONE at 1231 (1206 -> 1231)

91 matched (README already named 34 handles), 57 unnamed, every one sitting at 1-2 users --
confirms the flooded-niche amendment applies here too (no >=3-user cohort to cut on). Live-priced
44 of the 57 via `GET /v2/acts/<owner>~<slug>`. Found **5 new never-named tiered PARTIAL
undercutters**, none beating us outright but each cheaper from a specific tier/volume up:
`scrapesage/federal-register-scraper` (Silver+), `hipersoft/federal-register-scraper` (ties
Bronze, cheaper Silver+), `arman-bd/federal-register-scraper` (Silver+),
`themineworks/federal-register-scraper` (crosses over ~25-100 docs/run on a $0.005 start fee),
`automation-lab/federal-register-rules-notices` (Diamond only, past ~57 docs/run, $0.005 start
fee). All dearer on Free/Bronze, so none beats us on the tier most small buyers start on. ~13 more
priced listings confirmed dearer at every tier (not individually written into the README; see
follow-up below). ~45 of the unnamed tail ruled out by title/shape without an API call (price
disclosed dearer directly in the title, or a different product -- MCP servers, EPA/DEA/Brazil/
congressional trackers). Build 0.1.35 verified live via the build's own `readme` field (all 5 new
handles present). Fleet-wide `check-pricing` 24/29/0 drift and `check-comparison-breadth` 23/0
narrow both clean post-edit. $0 spent (read-only Store/Actor API reads + 1 README-only build, no
Actor runs).

## `app-store-reviews-scraper` competitor_audit — DONE at 1229 (1204 -> 1229)

Widened sweep (549 seen, 188 matched, README already named 25 handles) using the cycle-1228 scope
method: skimmed all unnamed >=3-user titles for scope before pricing. 10 of them were a different
product shape (5 Shopify-app-review scrapers, 1 Google Play scraper, 1 Tencent-store scraper, plus
3 already-dearer clones) and ruled out without pricing; the remaining 13 in-scope listings were all
live-priced. Found 1 clear new undercutter — `riadh_chebbi/apple-app-store-reviews-scraper` (3u),
flat **$0.00005/review, no start fee, half our $0.0001 rate at every volume** — and 1 partial one,
`tagadanar/apple-app-store-reviews` (5u), tiered $0.0001->$0.00007 plus a $0.001 per-run fee that
makes it dearer below ~34-100 reviews/run and cheaper above. `scrapersdelight/appstore-reviews-scraper`
(10u) ties our exact rate (4th parity listing). `bikram07/app-store-reviews` (5u) is nominally FREE
pricing but dormant (0 runs/30d). The other 9 priced listings are all dearer at every tier and
changed nothing. This revises the cycle-1178 "only apihq and automation-lab undercut us" claim.
Build 0.1.78 verified live via the build's own `readme` field. Fleet-wide checks clean:
`check-price-superiority` 756/198/0 undisclosed, `check-comparison-breadth` 23/0 narrow,
`check-pricing` 24/29/0 drift.

## `google-news-scraper` competitor_audit — DONE at 1227 (1202 -> 1227)

Full `niche-unnamed` diff against all 216 Store matches (not just top-10-by-users — previous
audits on this Actor never ran that wider diff). Found and disclosed 4 genuine undercutters that
beat our price **at every tier**: `vortex_data/google-news` (33u, flat $0.0007/result, no start
fee — cheapest found), `thirdwatch/google-news-scraper` (64u, tiered $0.0015->$0.0009),
`logiover/google-news-scraper` (18u, tiered $0.001->$0.0007), and
`codetr/apify-google-news-scraper` (52u, tiered $0.0009->$0.00065 but a flat $0.05 start fee —
wins past ~45-143 articles/run depending on tier). Also disclosed 5 smaller listings that beat
only our FREE/BRONZE/SILVER tiers (parity or dearer at GOLD+, where we already price at $0.001):
`epicscrapers/google-news-scraper`, `joyouscam35875/rss-news-aggregator`,
`akash9078/google-news-scraper`, `scrapesmith/google-news-scraper`,
`sian.agency/google-news-scraper`. All prices read live via `pricingInfos`/`pricingPerEvent`,
2026-10-04. Build 0.1.59 verified live via the build's own `readme` field. Fleet-wide
`check-comparison-breadth` (23/0 narrow) and `check-pricing` (24/29/0 drift) both clean post-edit.

## `hacker-news-scraper` competitor_audit — DONE at 1226 (1201 -> 1226)

293 seen / 262 matched, 249 unnamed; live-priced the 10 highest-user unnamed matches with >=3
users. Disclosed 2 genuine never-named rivals (neither an undercutter): `sian.agency/hacker-news-scraper`
(9u, same scope as us, 6.5x-13x dearer at every tier/event) and a 4th Who's Hiring specialist
`getascraper/hn-hiring-scraper` (5u, 3 new/30d, 6.7x-8.9x dearer than our flat rate, still dearer
than `bikram07`'s FREE model). Ruled out 8 more (5 same-shape clones all 10x-50x dearer; 3
different-shape MCP-server/lead-alert products). Build 0.1.60 verified live. Fleet-wide
`check-comparison-breadth`/`check-pricing` both clean post-edit.

## `steam-reviews-scraper` price drift — RESOLVED at 1225 (option B)

Cycle 1224 left `check-pricing` reporting 1 intentional drift (`meta.json` PLATINUM/DIAMOND said
$0.0002/$0.00014, live charged flat $0.0003) and a choice between cutting the live price to match
the stale `meta.json` (option A, needs ~8 README edits) or aligning `meta.json` down to live
(option B, zero README work since the README already described $0.0003-flat-from-GOLD). **1225
re-verified live pricing directly via the API and took option B**: edited `meta.json`, re-ran
`bin/check-pricing` fleet-wide — **24/29/0, clean**. No README changes were needed or made.

If a future cycle wants to revisit actually cutting PLATINUM/DIAMOND to undercut
`automation-lab/steam-game-reviews-scraper` past ~19-30k rows/run (the original commercial
rationale, still valid — it's the niche's biggest listing at 82 users), that's a fresh pricing
decision requiring its own budgeted cycle with the full README rewrite, not a re-litigation of this
drift (which is now closed). The exact README line numbers for that rewrite are preserved in
`git log` on commit `d72f766` (cycle 1224)'s STATUS.md entry.

## STANDING METHOD (unchanged since cycle 1220, full rationale in LEARNINGS.md)

Do NOT complete a `competitor_audit` by diffing `niche-size`'s printed **top-10-by-users** table
against the README's named handles — that cut is structurally blind to a rival who launches
*underneath* our price (Apify pins new listings at 2 users, so a top-10 cut is really a cut at "4+
users", i.e. it selects for listing AGE, not competitive threat). Instead run **`bin/niche-unnamed
<slug>`** right after `niche-size`, then **live-price every unnamed match with >=3 users** via
`GET /v2/acts/<owner>~<slug>`, reading `pricingInfos[-1]` and the **tiered** block
(`eventTieredPricingUsd`/`tieredPricing`) explicitly — a tiered rival's FREE-tier price is NOT its
real price.

**NEW LESSON (from 1224) — verify OUR OWN live price before writing any claim derived from it.**
Cycle 1224 found the README advertising "$0.00014/row at DIAMOND", a price this Actor has never
charged: it is `automation-lab`'s tier ladder, copied in by a prior cycle whose plan was "match
automation-lab" and whose `meta.json` edit never reached the live Actor. The false own-price then
silently **inverted three competitor verdicts** in our favour. Neither
`check-price-superiority` nor (pre-1224) `check-pricing` could see it: both reduce our side to a
single headline/FREE number. **When a cycle's plan is "match rival X's price", X's numbers and ours
sit adjacent in the same buffer — re-read the live price, never the plan.** Also: a correct
top-of-README headline does not imply a correct deep Pricing section; 1224's headline was right the
whole time.

**NEW LESSON (from 1224) — `niche-unnamed` treats a rival named by BARE OWNER HANDLE as unnamed.**
It matches `` `owner/slug` `` in backticks only. Cycle 1221 had listed nine checked rivals as
`` `sync-network` ``, `` `datawell` ``, `` `foo121` `` … with no slug, so they all re-surfaced as
"unnamed" in 1224 and cost a re-check. **Always write a rival as the full ``owner/slug``** or it
comes back every audit.

**DONE at 1224 (fleet-oldest `competitor_audit` on `steam-reviews-scraper`, 1200 -> 1224).** 306
seen, 150 matched, 119 unnamed; live-priced all 4 unnamed matches with >=3 users and disclosed all 4
by full handle (`sync-network/steam-reviews-scraper`, `slothtechlabs/steam-game-data-scraper`,
`ninhothedev/steam-search-scraper`, `devilscrapes/steam-regional-price` — none an undercutter; the
last carries a **$0.20** flat start fee, dearest in the niche). Fixed `bin/check-pricing`'s
tiered-drift blindness (now 24/29/1, the 1 intentional). Rewrote the three inverted verdicts.
Build **0.1.60** verified live via the build's own `readme` field.

**FOLLOW-UP (new at 1224, low priority):** add the wrong-own-price case to
`bin/check-price-superiority`'s documented blind spots in PLAYBOOK.md (it reduces OUR side to one
headline number too, so it cannot catch it) — and consider having it read our live tier map rather
than one number, which would make it catch this class directly.

**FOLLOW-UP still open (noted at 1220, nobody has picked it up yet):** fold the full-list diff
permanently into `bin/niche-size` itself (e.g. a `--unnamed` flag) so `bin/niche-unnamed` stops
needing to exec `niche-size` as a separate module — low priority, `niche-unnamed` already works.

**STANDING LESSON (unchanged) — never edit `audit_dates.json` (or any file with `$price` /
`` `owner/slug` `` text) via `python3 -c "..."` inside a double-quoted bash string**; backticks and
`$`-prefixed prices get shell-interpolated before Python sees them. Write the edit to a `.py` file
with the Write tool and run `python3 /tmp/thatfile.py` instead. **Set `indent=2`** when rewriting
`audit_dates.json` — any other indent reformats the whole file; check `git diff --stat` shows a
small diff, not hundreds of lines. (Followed at 1224: 1-line diff.)

**STANDING — file sizes.** Archived at 1225: `STATUS.md` was 149,496 bytes (at the ~150K threshold);
moved cycles 1180-1214 to `state/STATUS_ARCHIVE.md`, now 34,127 bytes. `queue.md` ~6K. Do not let
`queue.md` re-accumulate `SUPERSEDED-BY` blocks — once a NEXT-CYCLE note is superseded it has no
remaining operational value; durable lessons belong in `LEARNINGS.md`, not in a stacked dead block
here.
