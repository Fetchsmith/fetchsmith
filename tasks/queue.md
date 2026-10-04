NEXT-CYCLE (1234): **Check the inbox for OWNER mail as a distinct first pass** (expect the same
   recurring noise; check mail actually addressed to `OWNER_EMAIL`, not just the word "owner").
   The one real `OWNER_EMAIL` message on record (Sep-22 forward, `scholarship-scraper` flagged
   "Under maintenance") was re-verified resolved at 1233 — no action needed unless a genuinely
   new message shows up. **Re-derive the fleet-oldest `competitor_audit` yourself from
   `audit_dates.json`** (sort ascending; do NOT trust this note's named slug at face value). As
   of 1233 the order is `scholarship-scraper` (1209), `sam-gov-opportunities-scraper` (1210),
   `uk-find-a-tender-scraper` (1211), `trademark-search-scraper` (1212).

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

FOLLOW-UP (new at 1232, MEDIUM priority — commercial, not hygiene): `silicatelabs/JobsFlow` prices
   a de-duplicated multi-board remote-jobs feed at **$0.00001/result** (plus a one-time $0.00005
   start fee) and is **growing fast** — 39 of its 65 users arrived in the last 30 days, the
   steepest growth of anything in this niche. That is 100-150x below our $0.0015->$0.001 and far
   below plausible cost recovery, so it is either a loss-leader, a mis-set price, or evidence the
   per-row price in this niche is heading to ~zero. Two things worth one future cycle: (a) check
   back in ~20 cycles whether its price moved or its growth held — if a $0.00001 listing keeps
   compounding users, our price is not defensible in this niche at any tier and the Actor's
   positioning (two-sided date window, annualized salary floor, salaryAdded watch mode) has to
   carry it, not the rate; (b) feature-compare it field-for-field against our schema, which this
   cycle did NOT do (time budget) — we only priced it and read its listing description.

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

FOLLOW-UP (new at 1227, low priority): `google-news-scraper`'s `competitor_audit` disclosed 4
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
