Updated: 2026-10-24 ~15:03 UTC by cycle 2187 (sonnet-5) -- not a QUALITY slot (2187%3==1), inbox unchanged (10 items, no owner mail; DMARC carry-forward still blocked at `e2f3a358`), 0 audits due (soonest `website-screenshot-scraper`, 230c, cycle 2417), 0 fleet checks due (soonest `check-term-anchor`, 5c, cycle 2192): continued the PPE `chargedEventCounts` rotation per c2186's handoff -- `remote-jobs-scraper` was the sole fleet-oldest `varied_test` (1839) AND the natural next PPE pick. Stacked `companyKeyword` + `locationKeyword` for the first time ever on this Actor (prior entries covered jobTypeKeyword/wwr, seniorityKeyword+date window, sources/postedAfter/postedBefore/salaryOnly/minSalaryAnnual -- never company+location together). Predicted free via Jobicy's public API directly: `companyName='Zscaler'` has 4 live postings, `jobGeo` values `'Ireland,  UK'`/`'Netherlands'`/`'UK'`/`'Ireland'` -> `locationKeyword:'uk'` substring match keeps exactly 2. Live run `{sources:[jobicy], companyKeyword:'zscaler', locationKeyword:'uk', maxResults:10}` -> HTTP 201, **2/2 exact match** on company/location/title. Negative control (nonsense companyKeyword, same locationKeyword) -> 0 rows, fails closed. PPE check folded in free: both runs read via `GET /v2/actor-runs/<runId>` per c2184's lesson (not the misleading runs-list endpoint) -- filtered run `{job:2}` exactly matches the 2 delivered rows, negative control `{job:0}`, 0 leak either direction. Clean, **0 defects, no code change**. `state/audit_dates.json` updated (`remote-jobs-scraper.varied_test` 1839 -> 2187) via a targeted `Edit` (4-line diff), prior note preserved below the new one. PPE rotation now 19/24 -> **20/24**, 4 left: `nih-reporter-scraper`, `sec-insider-trades-scraper`, `us-federal-awards-scraper`, `website-screenshot-scraper`. ~$0.0001 spent (2+0 charged rows), Apify spend $3.83/$85, 0 new Actors, no owner email.
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200 (`/`, `/tools`, `/pricing`), `HEAD == origin/main` before this cycle's edits.

Updated: 2026-10-24 ~14:36 UTC by cycle 2186 (sonnet-5) -- not a QUALITY slot (2186%3==2), inbox unchanged (10 items, no owner mail; DMARC carry-forward still blocked at `e2f3a358`), 0 audits due (soonest `website-screenshot-scraper`, 231c, cycle 2417), 0 fleet checks due (soonest `check-term-anchor`, 6c, cycle 2192): continued the PPE `chargedEventCounts` rotation, pairing it for free with the `varied_test` age ranking per standing tactic -- `ats-jobs-scraper` was tied fleet-oldest `varied_test` (1839, with `remote-jobs-scraper`) AND one of the 6 PPE-rotation Actors left. Stacked `minSalary` + `descriptionKeyword` for the first time ever on this Actor (prior entries covered department/location/remote/employmentType/compound-zero-row-cause, never a salary-range filter combined with a text filter). Predicted free via a direct Ashby `posting-api` call on `jobs.ashbyhq.com/ramp` (167 live postings, `includeCompensation=true`): `descriptionPlain` containing "fraud" -> 7 rows, then applying the Actor's own overlap semantics (`jobMax >= minSalary`, read from `main.js:1286-1291`, not a naive `jobMin` check) -> exactly 5 survive. Live run `{companies:[{ats:ashby,slug:ramp}], descriptionKeyword:"fraud", minSalary:150000, maxResults:10}` -> HTTP 201, **5/5 exact match** on `jobId`/`title`/`salaryMin`/`salaryMax`. Negative control (nonsense keyword, same `minSalary`) -> 0 rows, fails closed. PPE check read both runs via `GET /v2/actor-runs/<runId>` per c2184's lesson (not the misleading runs-list endpoint): single flat `job` event (`main.js:368`) -- filtered run `{job:5}` exactly matches delivered rows, negative control `{job:0}`, 0 leak. Clean, **0 defects, no code change**. `state/audit_dates.json` updated (`ats-jobs-scraper.varied_test` 1839 -> 2186) via a targeted `Edit`, prior note preserved below the new one. PPE rotation now 18/24 -> **19/24**, 5 left: `nih-reporter-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `us-federal-awards-scraper`, `website-screenshot-scraper`. `remote-jobs-scraper` is now the sole fleet-oldest `varied_test` (1839) and is also in the PPE list -- natural next pick. ~$0.0001 spent (5+0 charged rows), Apify spend $3.83/$85, 0 new Actors, no owner email.
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200 (`/`, `/tools`, `/pricing`), `HEAD == origin/main` before this cycle's edits.

Updated: 2026-10-24 ~14:10 UTC by cycle 2185 (sonnet-5) -- not a QUALITY slot (2185%3==1), inbox unchanged (10 items, no owner mail; DMARC carry-forward still blocked at `e2f3a358`): ran the DUE `check-status-continuity` fleet check (48c gap) -- retained window cycle 2175-2184, 10/10 rc=0 cycles have a STATUS.md block, none missing, clean, recorded via `bin/checks-due --ran`, next due cycle 2233. 0 audits due (soonest `website-screenshot-scraper`, 232c, cycle 2417). Continued the PPE `chargedEventCounts` rotation per c2184's handoff note: `grants-gov-scraper` (2nd-oldest `varied_test`, 1833, also still unverified for charges -- the same free-pairing tactic). This Actor is the first in the rotation that forks price PER ROW by data richness (enriched `result` $0.0015 vs thin `opportunity-thin` $0.0007, main.js:940-970), never exercised by any prior varied_test entry. 3 live runs, all read via `GET /v2/actor-runs/<runId>` per c2184's lesson (not the misleading runs-list endpoint): (1) `{keyword:"cancer research", oppStatuses:["closed"], enrich:false, maxResults:5}` -> 5 rows all closed, `chargedEventCounts {result:0, opportunity-thin:5}` -- exact match. (2) negative control (nonsense keyword) -> 0 rows, `{result:0, opportunity-thin:0}`, fails closed. (3) `{..., minAwardAmount:1000000, maxResults:3}` (forces enrich on per schema) -> 3 rows all `awardCeiling>=1000000`, `{result:3, opportunity-thin:0}` -- enriched path billed correctly, 0 cross-contamination between the two charge events. Clean, **0 defects, no code change**. `state/audit_dates.json` updated (`varied_test` 1833 -> 2185) via a targeted `Edit`. PPE rotation now 17/24 -> **18/24**, 6 left: `ats-jobs-scraper`, `nih-reporter-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`, `us-federal-awards-scraper`, `website-screenshot-scraper`. ~$0.0013 spent (5 thin + 3 enriched charged rows), Apify spend $3.83/$85, 0 new Actors, no owner email.
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200 (`/`, `/tools`, `/pricing`), `HEAD == origin/main` before this cycle's edits.

Updated: 2026-10-24 ~13:45 UTC by cycle 2184 (opus-5) -- mandated QUALITY slot (2184%3==0), inbox unchanged (10 items, no owner mail; DMARC carry-forward still blocked at `e2f3a358`), 0 audits due / 0 fleet checks due (soonest `check-status-continuity`, 1c, cycle 2185): varied-tested `sam-gov-opportunities-scraper` (tied fleet-oldest `varied_test`, 1830, 354 cycles stale) with the **first ever platform test of the wage-determination family** -- 3 of its 6 dataTypes had never been exercised, the exact gap cycle 1830's own note named. Predicted the full answer FREE first via direct sam.gov API calls (`index=dbra&state=MT&is_active=true` -> total 79, top 5 ids), with free controls proving both filters real (MT alone 1463, active alone 4235, canary 0 = fails closed); the billable run matched **exactly 5/5 on ids AND order**, and the run log's "+79 rows" matched the predicted total. Also tested the ignored-filter path main.js:366-381 warns about (adding `naicsCodes`+`enrichDetail` to wd): rows byte-identical, both WARN lines verbatim, echoed input showed `enrichDetail:false`, i.e. the ignore is really applied, not just announced. Clean, **0 defects, no code change**; `isLatest`/`wageRates` nulls are SAM.gov's own shape (declared nullable in `dataset_schema.json`). PPE charge-path rotation folded in free, 16/24 -> **17/24** (7 left). New durable lesson: **`chargedEventCounts` is absent from the runs-LIST endpoint** (reads as a misleading `null`) -- use `GET /v2/actor-runs/<runId>`. `scholarship-scraper`'s NEVER-varied-tested record re-confirmed intentional (retired; bold.org re-curled live this cycle, still 429). ~$0.0005 spent (10 charged rows, 0 builds), Apify spend $3.83/$85, 0 new Actors, no owner email.
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200 (`/`, `/tools`, `/pricing`), `HEAD == origin/main` (pending this cycle's commit).

Updated: 2026-10-24 ~13:10 UTC by cycle 2183 (sonnet-5) -- not a QUALITY slot (2183%3==2), inbox unchanged (10 items, no owner mail; DMARC carry-forward still blocked at `e2f3a358`): ran the DUE `check-doc-size` fleet check (24c gap) -- all 3 live docs OK, well under the trim line (STATUS.md 34.2KB, queue.md 110.3KB pre-edit, LEARNINGS.md 3099 lines), no trim needed, recorded via `bin/checks-due --ran`, next due cycle 2207. 0 audits due. Continued the PPE `chargedEventCounts` rotation: spot-checked `eu-ted-tenders-scraper` and `steam-reviews-scraper` (the 2 highest-`totalRuns` of the 10 remaining after c2181), both single-event with no free-row floor -- one small filtered run + one negative control each, both clean, 0 leaks, confirmed live via `chargedEventCounts` matching delivered row count exactly (`{result:4}`/4 rows both times, 0/0 on both negative controls). Rotation 14/24 -> 16/24, 8 Actors left (`ats-jobs-scraper`, `grants-gov-scraper`, `nih-reporter-scraper`, `remote-jobs-scraper`, `sam-gov-opportunities-scraper`, `sec-insider-trades-scraper`, `us-federal-awards-scraper`, `website-screenshot-scraper`). Two small traps resolved without filing false bugs: `eu-ted-tenders-scraper`'s `keywords` field takes a plain STRING not an array (400 on first attempt, fixed by re-reading the schema); `steam-reviews-scraper`'s first keyword choice ("smooth") was just too rare in CS2 reviews (0 rows, not a bug) -- retried with "good". ~$0.001 spent, Apify spend $3.82/$85, 0 new Actors, no owner email.
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200 (`/`, `/tools`, `/pricing`), `HEAD == origin/main` (pending this cycle's commit).

Updated: 2026-10-24 ~12:33 UTC by cycle 2182 (sonnet-5) -- not a QUALITY slot (2182%3==1), inbox unchanged (10 items, no owner mail; DMARC carry-forward still blocked at `e2f3a358`): closed the OPEN half of c2181 with a fresh `varied_test` on `app-store-reviews-scraper`, the other fleet-oldest record (1827). Combo: `reviewsAfter`/`reviewsBefore` as exact timestamps (not bare dates) + `minRating:4` + `keyword:"love"` on Spotify/us, 4-hour window -- no prior varied_test on this Actor (833/1089/1517/1827) had touched the date filters at all. Tried the usual pre-compute-first technique via a separate offline RSS fetch, but Apple's feed had moved between that fetch and the billable run, so verified instead by reading every delivered row's own fields against all 3 filters. `bin/varied-test` printed `rows: 10` but `chargedEventCounts` read `{result:13}` -- its display cap hid 3 rows; pulled the full dataset directly and confirmed all 13 genuinely matched (rating>=4, inside the window, "love" present), charged count == delivered count, 0 leak. Negative control (`keyword:"zzznotfoundxyz123"`) -> 0 rows, `{result:0}` charged. Clean, no code change; new reusable lesson in `notes/LEARNINGS.md` cycle 2182 (always cross-check `chargedEventCounts`/true dataset size against `varied-test`'s printed row count). PPE rotation tally unchanged at 14/24 (this Actor was already counted at c2176; this was a re-confirmation under a different filter shape). `state/audit_dates.json` updated (varied_test 1827 -> 2182) via a targeted `Edit`. $0.0009 spent (13+0 charged rows), Apify spend $3.82/$85, 0 new Actors, no owner email. Next due fleet check: `check-doc-size` in 1 cycle (2183).
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200 (`/`, `/tools`, `/pricing`), `HEAD == origin/main` (pending this cycle's commit).

Updated: 2026-10-24 ~12:08 UTC by cycle 2181 (sonnet-5) -- mandated QUALITY slot (2181%3==0), inbox unchanged (10 items, no owner mail; DMARC carry-forward still blocked at `e2f3a358`; the owner's "Done" reply on the Apify identity-verification thread, `dc593cfb`, is old news already acted on -- the fleet is at 27 Actors, well past the 9-Actor verification gate, so no action owed): ran a fresh `varied_test` on `federal-register-scraper`, one of the fleet's two tied-oldest records (1827, with `app-store-reviews-scraper` left open for next cycle). Combo: `documentTypes:["NOTICE"]` + `significantOnly` together for the first time ever in this Actor's varied_test history (prior entries only paired `significantOnly` with RULE/PRORULE; the README already documents the NOTICE+significantOnly combo as real-but-rare, ~6-16/year). Predicted the top 5 via a free direct `federalregister.gov` API call (exact document numbers + dates). First live run (no `publicationDateFrom`) came back 0 rows -- investigated rather than filed as a bug: the schema's documented 90-day default date window has 0 significant Notices in it right now (confirmed on the direct API too), so the empty result was correct, not a defect. Re-ran with `publicationDateFrom:"2020-01-01"` explicitly: 5/5 rows, exact match on every field against the prediction. Folded the PPE `chargedEventCounts` rotation into the same 2 runs for free (13/24 -> 14/24, 9 left: `ats-jobs-scraper`, `eu-ted-tenders-scraper`, `grants-gov-scraper`, `nih-reporter-scraper`, `remote-jobs-scraper`, `sam-gov-opportunities-scraper`, `sec-insider-trades-scraper`, `steam-reviews-scraper`, `us-federal-awards-scraper`, `website-screenshot-scraper`) -- `{result:5}`/`{result:0}`, both charges exactly right, 0 leak. No code or README change needed. `state/audit_dates.json` updated (varied_test 1827 -> 2181) via a targeted line edit, not a full re-serialize, after a full-file `json.dump` round-trip reformatted every entry's indentation (1-space -> 2-space) for a 612-line diff on a 2-line change -- caught before committing and reverted; targeted `Edit` used instead. ~$0.0005 spent (2 capped runs), Apify spend $3.82/$85, 0 new Actors, no owner email.
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200 (`/`, `/tools`, `/pricing`), `HEAD == origin/main` (pending this cycle's commit).

Updated: 2026-10-24 ~11:40 UTC by cycle 2180 (opus-5) -- not a QUALITY slot (2180%3==2), nothing due (0 audits, 0 fleet checks), inbox unchanged, no owner mail: closed the open half of c2178 with a live `varied_test` on `shopify-products-scraper`, the fleet's sole oldest at 1824 (356 cycles stale). Tested the never-stacked 4-filter combo `searchQuery` + `productTypes` + `onSaleOnly` + `minDiscountPercent` (the discount floor had never been exercised as a FILTER at all, only documented). Pre-computed the expected answer from the live feed before spending the billable run (c1514 technique): pulled allbirds' whole 397-product catalog locally, re-implemented the Actor's own priceMin -> cheapest-variant-compare_at_price -> discountPercent chain, predicted exactly 4 matches -- the live run delivered exactly those 4, same handles, same percentages (50/50.4/31/30). CLEAN, 0 defects, no code change. Two things that LOOKED like bugs and were not, both resolved by reading rather than assuming: (a) one matching row has neither search word in its TITLE -- it matched via the documented tags haystack (`allbirds::material => tree`, `allbirds::silhouette => dasher`), so a title-only eyeball would have filed a false positive; (b) the run scanned 397 products with `maxProductsPerStore:250` set -- outside watch mode that key caps products DELIVERED, not scanned, so walking to the end of a 99%-filtered feed is correct. PPE charge path re-verified under heavy filtering (new beyond c2176's unfiltered check): `{result:4, productDetail:0}` vs `{result:0, productDetail:0}` on the negative control -- the 393 scanned-but-discarded products were NOT charged (per-run GET required; the /runs LIST endpoint omits `chargedEventCounts`, same omission shape as c2170's INPUT lesson). Negative control (`minDiscountPercent:80`, above the catalog max of 70.4) returned 0 rows, $0 charged, and its zero-row WARN named only the 4 filters actually set, with values. Both runs used the DEFAULT datacenter proxy with no 403 -- c1514's allbirds datacenter-403 note did not reproduce. `state/audit_dates.json` updated (varied_test 1824 -> 2180). ~$0.0002 spent (2 capped runs, 0 builds), Apify spend $3.82/$85, 0 new Actors, no owner email. `bin/usage-trend` glanced per the c2168 watch: `trademark-search-scraper` unchanged (54 runs, +2/24h, 3 users, 0 bookmarks/reviews) -> no escalation.
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200 (`/`, `/tools`, `/pricing`), `HEAD == origin/main` (pending this cycle's commit).

Updated: 2026-10-24 ~11:10 UTC by cycle 2179 (sonnet-5) -- not a QUALITY slot (2179%3==1), inbox unchanged, no owner mail: ran the DUE `check-rental-converts` fleet check (672c gap) and found + fixed a real fleet-coverage gap -- `website-screenshot-scraper` had NO `NICHE_TERMS` entry at all, so it had been invisible to this sweep since its 2026-10-16 launch (0/24 niches covered for it, silently skipped not erroring, exactly the "loud warning, not a verdict" trap the tool's own docstring names). Added `"screenshot"`, re-ran: surfaced 2 genuinely NOT-YET-NAMED rental-converted rivals for that Actor -- `dz_omar/ultimate-screenshot` (263 users, real feature overlap via 100+ device presets + video/GIF export we lack, but priced $0.005-0.007/page-capture vs our flat $0.002, so a feature gap not a price threat) and `scrapeai/screenshot-downloader` (6 users, narrow bare-capture, ruled out like 3 prior narrow rivals). Updated the Actor's README competitor section with both, `apify push --force` (build 0.1.28), verified the new names landed in the live build's `README.md` source file (the account's top-level `readme` field is empty/deprecated on this Actor -- had to read `versions[].sourceFiles` instead, a correction to the "verify via the live readme field" habit prior cycles used). Other 7 flagged listings across 5 niches were all already named. Recorded via `bin/checks-due --ran`, next due cycle 2851. `bin/usage-trend` glanced per the c2168 watch: `trademark-search-scraper` unchanged (+2/24h, 3 users, 0 bookmarks/reviews) -> no escalation. $0.005 spent (1 README-only build), Apify spend $3.82/$85 (well inside CLAUDE.md's $300 cap), 0 new Actors, no owner email.
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200 (`/`, `/tools`, `/pricing`, `/tools/website-screenshot-scraper`), `HEAD == origin/main` (pending this cycle's commit).

## cycle 2184: first ever varied_test of sam-gov-opportunities-scraper's wage-determination family (3 of 6 dataTypes, never exercised); predicted free, matched 5/5 exactly; ignored-filter path proven applied-not-just-warned; clean, 0 defects; PPE rotation 16/24 -> 17/24

Fresh verification first: `bin/audit-due --all` **0 due** (soonest `website-screenshot-scraper`,
233c, cycle 2417); `bin/checks-due` **0 due** (soonest `check-status-continuity`, 1c, cycle 2185).
Inbox unchanged (10 items, newest still the `c2fa5a9c` IP-lease spam, no owner mail; the older
`dc593cfb` owner reply on the Apify identity-verification thread is long-resolved news, fleet is
at 27 Actors; DMARC carry-forward still blocked at `e2f3a358`). Mandated QUALITY slot
(`2184 % 3 == 0`). 3 services active, site 200 on `/` `/tools` `/pricing`, `HEAD == origin/main`
before this cycle's edits.

**A NEVER-varied-tested record checked before trusting the rotation.** `scholarship-scraper` sorts
as `NEVER` on `varied_test`, which is the shape of the c2080/c2179 blind-spot bugs, so it was read
rather than skipped. It is **intentional, not a gap**: the Actor is registry `status=retired`
because its only source (bold.org) has served a Vercel JS-proof-of-work 429 to every non-browser
request since 2026-09-20, and cycle 1516 already taught `audit-due` to rank retired Actors as
RETIRED instead of first-in-line. Re-curled bold.org live this cycle anyway (free, one request):
still `429`. No action owed; `bin/actor-health`'s `recheck_url` probe remains the mechanism that
will notice the day it clears. The real fleet-oldest `varied_test` pair is therefore
`hacker-news-scraper` / `sam-gov-opportunities-scraper`, both 1830 (354 cycles stale).

**Picked `sam-gov-opportunities-scraper` deliberately**: it is also one of the 8 Actors left in the
PPE `chargedEventCounts` rotation, so one set of runs advances both items for free (same tactic as
c2178/c2181). Read its own `varied_test_note` first to avoid repeating a combo — cycles 1043/1292
covered `opportunities`, 1628 `assistance-listings`, 1830 `exclusions`, and 1830's note named the
remainder precisely: *"organizationId-as-filter and the wage-determinations-* branches remain
untested by varied-test"*. The wd family is **3 of the 6 dataTypes** and had never been exercised
on the platform at all.

**Predicted the entire answer for free before spending a billable row.** Read `buildSearchUrl`'s wd
branch (`main.js:488+`) for the real param names — `state`, not the opportunity index's
`pop_state`; `is_active` — then curled `sam.gov/api/prod/sgs/v1/search/` directly:
`index=dbra&state=MT&is_active=true` -> `totalElements` **79**, top 5 `fullReferenceNumber`s
MT20260001 / MT20260010 / MT20260011 / MT20260012 / MT20260013. Three more free controls to prove
both filters are genuinely applied rather than coincidence: `state=MT` alone -> **1463**,
`is_active=true` alone -> **4235**, `state=<canary>` -> **0** (fails CLOSED, so the name is
honoured, not dropped).

**Run (1)** `{dataType:"wage-determinations-dbra", states:["MT"], activeOnly:true, maxResults:5}`
-> HTTP 201, 5 rows, **exact 5/5 match on ids AND order** against the prediction. Full dataset read
directly (per c2182's lesson, not off `varied-test`'s printed cap): `stateCodes:["MT"]`,
`recordType:"wdDBRA"`, `actCode:"DBA"`, `isActive:true` on every row. Run log `Page 0: +79 rows`
matched the predicted total exactly, and `Pushed 5 ... (scanned 79 row(s))` with
`chargedEventCounts {result:5}` gives the full **scanned 79 / delivered 5 / charged 5** triple —
the 74 scanned-but-discarded rows were not billed. The Actor's own canary guard also fired and
passed here (`Verified SAM.gov still honours the "state" filter`), confirming
`assertFilterNamesApplied` is live on the wd family and not only on `opportunities`.

**Run (2) tested the ignored-filter path, the exact risk `main.js:366-381` warns about** ("silently
ignoring them would return a full 10,000-row unfiltered set that LOOKS filtered -- and every row is
billed"). Re-ran identical input plus `naicsCodes:["541511"]` and `enrichDetail:true`: 5 rows
identical in ids and order to run (1) — neither narrowed nor widened — both WARN lines emitted
verbatim, and crucially the echoed input line shows `"enrichDetail":false`, i.e. the ignore is
really **applied**, not merely announced. `chargedEventCounts {result:5}`, 0 leak.

**Two nulls checked rather than assumed to be parser misses.** `isLatest` and `wageRates` are null
on all wd rows; `dataset_schema.json` declares both nullable (`["boolean","null"]` /
`["array","null"]`) and `main.js:739-744` documents that per-occupation rate schedules are absent
from the search row on all three wd indices. SAM.gov's own data shape — same class of finding as
1628's EPA `agency`-null. **No defect, no code change.**

**New durable lesson (LEARNINGS.md).** The charge check was first run against the runs-LIST
endpoint (`/v2/acts/<user>~<slug>/runs?limit=1`), which returned `chargedEventCounts: null` on a
run that had definitely billed 5 rows. Not a billing anomaly — the list endpoint serves an abridged
record that omits the field; `GET /v2/actor-runs/<runId>` returned the real `{result:5}`. Same trap
class as c2179's missing top-level `readme` field. **Never read charge/pricing fields off a
runs-list response.** Also noted: `varied-test`'s output-key guard correctly flagged my guessed
`fullReferenceNumber`/`state`/`dataType` as NOT A FIELD (real names `referenceNumber`/`stateCodes`/
`recordType`) — the c2160 guard doing its job, and it prevented two false "returns nothing here"
bugs.

PPE rotation now **17/24**; 7 left (`ats-jobs-scraper`, `grants-gov-scraper`,
`nih-reporter-scraper`, `remote-jobs-scraper`, `sec-insider-trades-scraper`,
`us-federal-awards-scraper`, `website-screenshot-scraper`). `state/audit_dates.json` updated
(`sam-gov-opportunities-scraper.varied_test: 1830 -> 2184`, full note, prior preserved) via a
targeted `Edit` — 2-line diff, per c2181's full-`json.dump`-reformat near-miss. ~$0.0005 spent
(10 charged rows, 0 builds), `bin/apify-spend` **$3.83/$85** hard cap. 0 new Actors, no owner email.

**Next cycle (2185): `check-status-continuity` is due (1c gap) — run it first. `2185 % 3 == 1`, not
a QUALITY slot.** Open items: PPE rotation 17/24 (7 listed above); fleet-oldest `varied_test` is now
`hacker-news-scraper` (1830), with `grants-gov-scraper`/`trademark-search-scraper` (1833) next —
note `grants-gov-scraper` is also in the PPE rotation, so it pairs the two items for free again;
`sam-gov-opportunities-scraper`'s remaining untested surface is the `cba`/`sca` wd siblings and
`organizationId`-as-filter (opportunities/cfda only — proven an ignored no-op on wd this cycle);
DMARC recheck still blocked on a report newer than `e2f3a358`; `trademark-search-scraper`
buyer-intent watch (run-count alone never escalates).

## cycle 2179: ran the DUE check-rental-converts fleet check, found and fixed a real coverage gap (website-screenshot-scraper had never had a NICHE_TERMS entry), surfaced + documented 2 new rental-converted rivals for it

Fresh verification first: `bin/audit-due --all` **0 due** (soonest `website-screenshot-scraper`,
238c, cycle 2417); `bin/checks-due` **1 due: `check-rental-converts`** (672c gap, last run cycle
1507) -- the natural pick per c2178's own next-cycle note. Inbox unchanged (10 items, newest
still the `c2fa5a9c` IP-lease spam, no owner mail; DMARC carry-forward still blocked at
`e2f3a358`). Not a QUALITY slot (`2179 % 3 == 1`). Services and git state verified: 3 services
active, site 200 on `/` `/tools` `/pricing`, tree clean before this cycle's edits.

**`check-rental-converts` is read-only (GETs only, no Actor runs, no writes) per its own
docstring, so it was run directly without extra caution.** First pass: 23 niches searched, 407
listings checked, 7 flagged as newly rental-converted, all tagged "already named" (real rivals
already written into the relevant Actor READMEs). But the run also emitted `WARN: no
NICHE_TERMS search term for: website-screenshot-scraper -- not swept` -- a loud warning, not a
failure, exactly as the script's docstring says it's designed to do for a slug missing from its
hand-curated `NICHE_TERMS` map.

**Read the warning rather than letting it pass silently, since that's precisely the shape of bug
this fleet has been burned by before (c2080's audit-due blind-spot for a brand-new Actor).**
Checked `NICHE_TERMS`: `website-screenshot-scraper` (live since 2026-10-16, Actor #25) was never
added. That means this fleet check had swept 0/24 niches for it since launch -- 8 days of zero
rental-conversion coverage for an Actor whose own `competitor_audit` note (c2081) already
confirmed "screenshot" is the right query term (used manually that cycle). Added
`"website-screenshot-scraper": "screenshot"` to the dict, `python3 -m py_compile` clean, re-ran.

**Second pass: 24/24 niches, 422 listings, 9 flagged.** The same 7 "already named" hits recurred
(unchanged) plus 2 new ones for the now-covered niche, both genuinely NOT YET NAMED:
- `dz_omar/ultimate-screenshot` (263 users, 10/30d) -- real feature overlap (100+ device
  presets, plus video/MP4 and GIF export, which we don't offer at all), converted to
  PAY_PER_EVENT 2026-10-16. Read its full tiered pricing live rather than trust the Store
  listing: `page-capture` is $0.007 at the FREE tier down to $0.005 at GOLD+, 2.5x-3.5x our flat
  $0.002 -- a genuine feature differentiator, not a price threat. Decided it still belongs in
  the README (263 users is bigger than 3 of the 6 rivals already named there) so a buyer
  comparing options sees the real tradeoff (cheaper here, video/GIF there).
- `scrapeai/screenshot-downloader` (6 users, flat $0.00249/result) -- bare full-or-partial
  PNG/JPEG capture, no element selector, device preset, raw-HTML input, PDF or diff mode. Same
  narrow gap as the three rivals the c2081 competitor_audit already ruled out for the identical
  reason -- noted, not added to the README (consistent with that precedent).

**README updated and pushed.** Added a dated 2026-10-24 paragraph to
`actors/website-screenshot-scraper/README.md`'s competitor section (after the existing
2026-10-22 `competitor_audit` paragraph, same style) naming both findings with the reasoning
above. `apify push --force` -> build **0.1.28**, SUCCEEDED.

**Verification caught a stale habit from prior cycles.** Tried to verify the backlink the usual
way (`GET /v2/acts/<slug>` -> read the top-level `readme` field, as c2173/c2173 described doing
for other Actors) -- it came back empty (key absent, defaulted to `''`). Read the full actor
record's keys instead of assuming a transient glitch: there is no top-level `readme` field on
this account's response at all. The real content lives in `versions[0].sourceFiles`, one entry
per file in the pushed source, `name == "README.md"`. Read that instead: both `dz_omar` and
`scrapeai` strings present, confirming the push landed. **Correction for future verification
steps:** check `versions[].sourceFiles` for `README.md`, not a top-level `readme` field, which
may not exist on every account/Actor combination.

Recorded via `bin/checks-due --ran check-rental-converts`, full note, next due cycle 2851 (a
672-cycle gap matching the tool's cadence). `bin/usage-trend` glanced per the c2168 standing
watch: `trademark-search-scraper` unchanged (+2/24h, 3 users, 54 total, 0 bookmarks/0 reviews)
-- no escalation, a run-count climb alone never triggers an owner email.

$0.005 spent (1 README-only `apify push --force` build, no live Actor runs); `bin/apify-spend`
$3.82/$85 hard cap, well inside CLAUDE.md's $300 total budget. 0 new Actors, no owner email.
Services active, site 200 on `/` `/tools` `/pricing` and `/tools/website-screenshot-scraper`.

**Next cycle (2180): re-verify `audit-due --all`/`checks-due` fresh first. `2180 % 3 == 2`, not
a QUALITY slot. `check-rental-converts` is not due again until cycle 2851 -- far out. Open items
unchanged: PPE `chargedEventCounts` rotation (13/24, remaining 11 listed on its queue.md item,
`eu-ted-tenders-scraper`/`steam-reviews-scraper` highest-traffic), `shopify-products-scraper`'s
`varied_test` still open from c2178 (genuinely-new combo candidates noted there), DMARC recheck
(blocked on a report newer than `e2f3a358`), `trademark-search-scraper` buyer-intent watch
(run-count alone never escalates). If nothing else is due and `2181` (the next mandated QUALITY
slot) hasn't arrived, the PPE rotation or the open shopify `varied_test` are the natural picks.**

Updated: 2026-10-24 ~10:40 UTC by cycle 2178 (sonnet-5) -- mandated QUALITY slot (2178%3==0), inbox unchanged, no owner mail: varied-tested `fec-campaign-finance-scraper`'s fleet-tied-oldest `varied_test` record (1824) with a genuinely new 5-filter disbursements stack (committeeId+recipientState+minAmount+maxAmount+date range+explicit electionYear) -- cycle 945 had only ever combined 3 filter groups in that mode, never `state`. Predicted exactly via a free direct FEC API curl, matched live 5/5 after discovering (not a bug) that the Actor defaults `electionYear` to the current cycle so it must be passed explicitly to test a past year's date window; negative control (absurd amount range) correctly collapsed to 0. Folded the PPE `chargedEventCounts` rotation into the same run for free (12/24 -> 13/24). `shopify-products-scraper` (also tied at 1824) is left open for next cycle. $0.0007 spent, 0 new Actors, no owner email.
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200 (`/`, `/tools`, `/pricing`), `HEAD == origin/main`.

## cycle 2178: varied-tested fec-campaign-finance-scraper's disbursements mode with a new 5-filter stack (committeeId+state+amount range+date range+electionYear); clean, 0 defects; PPE rotation 12/24 -> 13/24

Fresh verification first: `bin/audit-due --all` **0 due** (soonest `website-screenshot-scraper`,
239c, cycle 2417); `bin/checks-due` **0 due** (soonest `check-rental-converts`, 1c, cycle 2179).
Inbox unchanged (10 items, newest still the `c2fa5a9c` IP-lease spam, no owner mail; DMARC
carry-forward still blocked at `e2f3a358`). Mandated QUALITY slot (`2178 % 3 == 0`). Services and
git state verified: 3 services active, site 200 on `/` `/tools` `/pricing`, tree clean before
this cycle's edits.

**Task picked.** `state/audit_dates.json` confirmed `fec-campaign-finance-scraper` and
`shopify-products-scraper` tied at the fleet's oldest `varied_test` (both 1824), per c2177's
pointer. Picked `fec-campaign-finance-scraper` first; `shopify-products-scraper` left open
(its PPE charge-path check already ran at c2176, only its filter-combo sweep is outstanding).

**`fec-campaign-finance-scraper`, disbursements mode: a 5-filter stack never tried together.**
Read the Actor's own prior notes first: cycle 945 (the only prior disbursements-mode test)
combined `committeeId` + a date range + an amount range (3 filter groups), never `state`.
Picked `committeeId` + `state` (recipientState) + `minAmount` + `maxAmount` +
`contributionDateFrom`/`To`, plus an explicit `electionYear` (see gotcha below). Predicted for
free via a direct curl to `api.open.fec.gov/v1/schedules/schedule_b/` with identical params
(`committee_id=C00401224`, `recipient_state=VA`, `min_amount=1000`, `max_amount=50000`,
`min_date=2024-01-01`, `max_date=2024-12-31`): count 6299 (exact), first 5 rows by
`-disbursement_date` — ONE GIANT LEAP PAC $10000, FRIENDS OF DON BEYER $2500, CONNOLLY FOR
CONGRESS $1000, ONE GIANT LEAP PAC $7500, DEMOCRATIC PARTY OF VIRGINIA $1000.

**Gotcha hit and resolved, not a bug.** The first live Actor run with the identical filters
(no `electionYear`) returned 0 rows. Reading the run log explained it immediately: the Actor
defaults `electionYear` to the *current* cycle (2026), and the FEC's own
`two_year_transaction_period` scoping for schedule_b then excludes 2024 dates entirely — a
correct, already-intentional default, just one this test needed to override to match a past
year's date window. Re-ran with `electionYear:2024` set explicitly: **5/5 rows matched the
direct-API prediction exactly**, same order, every field (recipientName/disbursementAmount/
disbursementDate/recipientState, all `VA`) confirmed via the dataset API read, not just the
printed summary. Negative control (`minAmount:999999`, `maxAmount:9999999`, same other
filters): 0 rows — genuine AND composition across all 5 filters, not a vacuous pass. **CLEAN,
no code change.** Also caught my own output-key typo mid-task (asked `bin/varied-test` for
`state`, the real field is `recipientState`) via its NOT-A-FIELD guard — re-checked correctly
before concluding anything, not filed as a bug.

**PPE rotation folded in for free.** `chargedEventCounts {result:5}` == 5 pushed rows on the
real test run (the 0-row negative control pushed and charged nothing). Rotation now **13/24**.

`state/audit_dates.json` updated (`fec-campaign-finance-scraper.varied_test: 1824 -> 2178`,
full note, prior preserved). `bin/usage-trend` glanced per the c2168 watch:
`trademark-search-scraper` unchanged shape, 0 bookmarks/reviews -> no escalation.

$0.0007 spent (1 real 5-row run; the negative control charged $0), 0 new Actors, 0 builds, no
owner email. Services active, site 200 on `/` `/tools` `/pricing`.

**Next cycle (2179): re-verify `audit-due --all`/`checks-due` fresh first. `check-rental-
converts` fleet check is DUE (0c away) — the natural pick. If time remains, close this cycle's
open half: `shopify-products-scraper`'s `varied_test` is still unrun (it got its PPE
charge-path check at c2176, cycle 1514 covered multi-storeUrls dedup + `detailLevel:"full"`) —
`searchQuery`+`vendors`+`minPrice`/`maxPrice`+`onlyAvailable` stacked, or `onSaleOnly`+
`minDiscountPercent`+`productTypes` stacked, look like genuinely-new ground; check
`audit_dates.json`'s full note history first. `2179 % 3 == 1`, not a mandated QUALITY slot.
Rotation has 11 PPE Actors left (`eu-ted-tenders-scraper` and `steam-reviews-scraper` highest-
traffic). DMARC recheck stays blocked on a report newer than `e2f3a358`.**

Updated: 2026-10-24 ~10:15 UTC by cycle 2177 (sonnet-5) -- not a QUALITY slot (2177%3==2), inbox unchanged, no owner mail: continued the PPE `chargedEventCounts` charge-path rotation on 2 more Actors (`substack-scraper`, `google-news-scraper`), picked per c2176's next-highest-`totalRuns` pointer. Both clean, 0 leaks; rotation 10/~26 -> 12/24 (corrected denominator: excludes `_template` and retired `scholarship-scraper`). `substack-scraper` is the rotation's 2nd multi-event Actor (result/post-metadata/comment/leaderboard-row) -- verified the earned-charge condition (real non-empty `bodyText`) per the c2176 rule, not just the counter. $0.00135 spent, 0 new Actors, no owner email.
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200 (`/`, `/tools`, `/pricing`), `HEAD == origin/main` (pending this cycle's commit).

## cycle 2177: PPE charge-path rotation -- substack-scraper (2nd multi-event Actor) + google-news-scraper, both clean, rotation 10/~26 -> 12/24

Fresh verification first: `bin/audit-due --all` **0 due** (soonest `website-screenshot-scraper`,
240c, cycle 2417); `bin/checks-due` **0 due** (soonest `check-rental-converts`, 2c, cycle 2179).
Inbox unchanged (10 items, newest still the `c2fa5a9c` IP-lease spam, no owner mail; DMARC
carry-forward still blocked at `e2f3a358`). Not a QUALITY slot (`2177 % 3 == 2`). Services and
git state verified: 3 services active, site 200 on `/` `/tools` `/pricing`, tree clean before
this cycle's edits.

**Task picked.** c2176's next-cycle note named the rotation's next-highest-`totalRuns`
unverified PPE Actors: `substack-scraper` (777), `steam-reviews-scraper` (764),
`google-news-scraper` (763), `eu-ted-tenders-scraper` (745). Picked `substack-scraper` and
`google-news-scraper`. Grepped both for `FREE_PER_RUN`/`freeGiven` first per the c2171 trap --
neither has a free floor, so small `maxResults` is safe.

**Denominator correction, recorded before using it:** `grep -l isPayPerEvent
actors/*/src/main.js` returns 26 hits, but `_template` is not a real Actor and
`scholarship-scraper` is RETIRED (not billable) -- the real population is **24 active PPE
Actors**, not ~26. Rotation is now 12/24, exactly half.

**`substack-scraper` -- the rotation's 2nd multi-event Actor** (after `shopify-products-scraper`
at c2176). Four possible events: `result` (full-text post), `post-metadata` (metadata-only
post), `comment`, `leaderboard-row` (only in `leaderboardOnly` mode). Test run
(`includeBodyText:true`, `includeComments:true`, `maxCommentsPerPost:2`, `maxResults:3` on
`astralcodexten`): `chargedEventCounts {result:1, 'post-metadata':0, 'leaderboard-row':0,
comment:2}` against a 3-row dataset (1 post + 2 comments) -- exact match. Per the c2176
earned-charge rule (a per-row count equal to the row count isn't self-evidently right, read the
delivered fields): the post row's `bodyText` field was genuinely non-empty, confirming `result`
(the full-text rate) rather than the cheaper `post-metadata` was the correct charge. Both
unused events (`post-metadata`, `leaderboard-row`) correctly read 0 since this run's mode never
reaches them. **Clean, 0 leaks.**

**`google-news-scraper` -- single-event (`result` only, confirmed by reading every
`pushResult`/`Actor.charge` call site, there is exactly one).** Test run (`queries:["web
scraping"]`, `maxItemsPerQuery:4`, `maxResults:4`): `chargedEventCounts {result:4}` against 4
dataset rows, each a real, distinct article title (`"Meta quietly delays controversial
update..."`, `"Publishers and Lawmakers Just Forced Meta..."`, etc.) -- not 4 copies of one
row. **Clean, 0 leaks.**

Both runs re-polled 4x over ~50-60s per the c2171 counter-lag trap; both were already stable at
the first poll.

`bin/usage-trend` glanced per the c2168 standing watch: `trademark-search-scraper` unchanged
shape, still 0 bookmarks/0 reviews -> no escalation (a run-count climb alone never triggers an
owner email, per that item's own rule).

$0.00135 spent (2 capped live runs, measured `usageTotalUsd` 0.000247 + 0.001106); `bin/apify-
spend` $3.81/$85 hard cap, 49.7% through the billing cycle, projection $7.66 -- comfortably
inside CLAUDE.md's $300 total. 0 new Actors, 0 builds, no owner email. Services active, site
200 on `/` `/tools` `/pricing`.

**Next cycle (2178): re-verify `audit-due --all`/`checks-due` fresh first. `2178 % 3 == 0` IS a
mandated QUALITY slot: fleet-oldest `varied_test` is `fec-campaign-finance-scraper` +
`shopify-products-scraper` (both 1824) -- note shopify already had its charge check done
(c2176) but not its `varied_test`, so only the `varied_test` is open there. Could fold the PPE
rotation into that `varied_test` work per the c2172 efficiency lesson (a `varied-test` call is
already billable; read `chargedEventCounts` right after at zero marginal cost). Rotation has 12
PPE Actors left: `ats-jobs-scraper`, `eu-ted-tenders-scraper`, `fec-campaign-finance-scraper`,
`federal-register-scraper`, `grants-gov-scraper`, `nih-reporter-scraper`,
`remote-jobs-scraper`, `sam-gov-opportunities-scraper`, `sec-insider-trades-scraper`,
`steam-reviews-scraper`, `us-federal-awards-scraper`, `website-screenshot-scraper`
(`eu-ted-tenders-scraper` and `steam-reviews-scraper` are the highest-traffic of these).
`check-rental-converts` fleet check due cycle 2179. DMARC recheck stays blocked on a report
newer than `e2f3a358`.**

Updated: 2026-10-24 ~09:50 UTC by cycle 2176 (opus-5) -- BUILD slot (2176%3==1) with no build candidate (niche-hunting closed at NICHES.md c2093), inbox unchanged, no owner mail: spent it on the revenue-PROTECTING `chargedEventCounts` rotation instead, on the 3 unverified PPE Actors with the most `totalRuns` (`shopify-products-scraper` 810, `hacker-news-scraper` 796, `app-store-reviews-scraper` 785). All 3 charge paths correct, 0 leaks; rotation 7/~26 -> 10/~26. Found and closed a real gap in the rotation's own method: for a CONDITIONAL billable event, `charged == rows` is the suspicious reading, not the passing one (see cycle 2176 block). 0 new Actors, $0.0015 spent, no owner email.
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200 (`/`, `/tools`, `/pricing`), `HEAD == origin/main` (pending this cycle's commit).

## cycle 2176: charge-path spot-checked the 3 highest-traffic unverified PPE Actors (shopify-products, hacker-news, app-store-reviews); all clean, rotation 10/~26; tightened the rotation's assertion for multi-event Actors

Fresh verification first: `bin/audit-due --all` **0 due** (soonest `website-screenshot-scraper`,
241c, cycle 2417); `bin/checks-due` **0 due** (soonest `check-rental-converts`, 3c, cycle 2179).
Inbox unchanged (10 items, newest still the `c2fa5a9c` IP-lease spam, no owner mail; DMARC
carry-forward still blocked at `e2f3a358`). Not a QUALITY slot (`2176 % 3 == 1`).

**Why a BUILD slot became rotation work, stated so a future cycle doesn't re-litigate it:**
`bin/revenue` reads 25 Actors / 46 users / **0 bookmarks / 0 reviews / $0 booked**, and
`NICHES.md` c2093 closed niche-hunting across every axis tried (the two keywords that cleared the
demand bar, zillow and etsy, are walled by PerimeterX/DataDome). A 26th Actor has near-zero
expected value. By contrast an Actor whose charge path is silently broken earns $0 forever and we
**cannot** detect it from earnings — Apify exposes no earnings endpoint at all (`bin/revenue:76`)
— so `chargedEventCounts` is the only observable proxy, and 19 of ~26 PPE Actors were still
unverified at cycle start. Picked the 3 with the highest `totalRuns`, where a leak would cost most.

**Method and the two documented traps, both handled:** grepped all 3 for
`FREE_PER_RUN`/`freeGiven` before sizing the runs (c2171's free-floor trap) — none has a free
floor, so `maxResults: 3-4` is safe; all 3 charge-before-push on `eventName:'result'`. Re-polled
every run 4x over ~75s (c2171's counter-lag trap) — all counters were already final at first poll
and stable across all 4.

**Results — 3 capped live runs, all SUCCEEDED, 0 defects:**
- `shopify-products-scraper` (`detailLevel:"full"`): `{result:3, productDetail:3}` vs 3 rows
- `hacker-news-scraper`: `{result:4}` vs 4 rows
- `app-store-reviews-scraper`: `{result:4}` vs 4 rows

**The finding worth keeping: the rotation's original assertion is insufficient for conditional
events.** `shopify-products-scraper` is the first MULTI-event Actor the rotation has reached
(`result` per product + `productDetail` per enriched product). `productDetail` is charged only
when at least one detail-only field came back (`src/main.js:657` returns early otherwise), so
`productDetail == rowCount` is correct *only if every row really carries detail data* — and it is
also exactly what a missing `return` in that guard would produce. The counter cannot tell the two
apart. Checked the delivered rows instead: all 3 had a real `seoTitle`, all 3 a real
`totalInventory` (8 / 172 / 211 — a `.js`-route-only field the bulk `products.json` feed does not
carry), one a real `ratingValue: 5`. Genuinely earned, no over-charging. Rule recorded in
`queue.md` + `LEARNINGS.md` for the remaining 16: classify each event as per-row or conditional
first; for conditional events `charged < rows` is the reassuring reading and `charged == rows` is
the one that needs a field-level check.

`bin/usage-trend` glanced per the c2168 buyer watch: `trademark-search-scraper` 54 runs30d
(+2/24h), still 3 users, **0 bookmarks / 0 reviews** — no escalation, per that item's own rule
that a run-count climb alone can never substantiate a revenue claim (we cannot read earnings).

$0.0015 spent (measured `usageTotalUsd` 0.0009 + 0.0002 + 0.0004), 0 new Actors, 0 builds, no
owner email. Services active, site 200 on `/` `/tools` `/pricing`.

Updated: 2026-10-24 ~09:05 UTC by cycle 2175 (sonnet-5) -- mandated QUALITY slot (2175%3==0), inbox unchanged, no owner mail: platform-tested the fleet's two tied-oldest varied_test Actors (`fda-recall-scraper` + `google-play-reviews-scraper`, both 1821 -> 2175, 354c stale) across previously-untested filter combos; all correct, 0 defects. Folded the PPE `chargedEventCounts` rotation into the same billable runs (now 7/~26 PPE Actors verified). 0 new Actors, ~$0.001 spent, no owner email.
Services active (`fetchsmith-web`, `fetchsmith-mail`, `caddy`), site 200 (`/`, `/tools`, `/pricing`), `HEAD == origin/main`.

## cycle 2175: varied-tested fda-recall-scraper (genericName+manufacturerName+dateField) and google-play-reviews-scraper (country/language+replyFilter+minReviewLength+default includeAppDetails); both clean, 0 defects; PPE rotation now 7/~26

Fresh verification first: `bin/audit-due --all` **0 due** (soonest `website-screenshot-scraper`,
242c, cycle 2417); `bin/checks-due` **0 due** (soonest `check-rental-converts`, 4c, cycle 2179).
Inbox unchanged (10 items, newest still the `c2fa5a9c` IP-lease spam, no owner mail; re-confirmed
the `dc593cfb` owner thread is long-resolved). Mandated QUALITY slot (`2175 % 3 == 0`): picked
cycle 2174's own next-cycle pointer, the fleet-oldest `varied_test` pair confirmed via
`state/audit_dates.json` (`fda-recall-scraper` and `google-play-reviews-scraper`, both last
tested cycle 1821, next-oldest is 1824).

**`fda-recall-scraper`**: first-ever combined test of the drug-only cross-referenced fields
(`genericName` + `manufacturerName`) stacked with `dateField="recall_initiation_date"` -- prior
audits covered `classifications`+`voluntaryMandated` (c1075) and `status`+`dateField=
termination_date`+`classifications`, never `brandName`/`genericName`/`manufacturerName` at all.
Predicted via 2 free direct openFDA API calls (no Actor cost): `genericName="metformin"` AND
`manufacturerName="AstraZeneca Pharmaceuticals LP"` = 2 rows (both a combined-ingredient name,
`"DAPAGLIFLOZIN AND METFORMIN HYDROCHLORIDE"`, confirming the whole-word phrase search matches
inside a multi-ingredient name); same `genericName` + `manufacturerName="Pfizer"` (a real
manufacturer with no metformin recalls) = 0. Live-verified with 2 capped Actor runs: test run
delivered exactly 2 rows (same genericName/manufacturerName, `recallInitiationDate:2021-03-15`,
`classification:"Class II"`), control run delivered 0 -- proving genuine AND composition, not an
OR or a silently-ignored filter. `chargedEventCounts` matched the dataset row count on both runs
(`{result:2}` and `{result:0}`). CLEAN, no code change, 0 defects.

**`google-play-reviews-scraper`**: first-ever combined test of `country`/`language`
(app-resolution-adjacent) with `replyFilter` + `minReviewLength` (review filters) AND, critically,
the real DEFAULT of `includeAppDetails` (schema default `true`, code `input.includeAppDetails !==
false`) -- prior audits (c1513) always explicitly set it `false`, so the default-on path had
never been exercised alongside review filters. Input: `com.spotify.music`, `country:"gb"`,
`language:"en"`, `replyFilter:"hasReply"`, `minReviewLength:40`. Result: row 0 was the
app-details record (`recordType:"app"`, decimal `score` = app average rating, `thumbsUp`/
`replyText`/`text` all null as expected since it carries no review fields) and correctly
bypassed both review-only filters rather than being dropped or crashing; the other 9/9 rows all
had non-null `replyText` (real multi-language developer replies) and text far over 40 characters.
Control run (`replyFilter:"noReply"`, `includeAppDetails:false`): 6/6 rows null `replyText`,
confirming the opposite set and that `includeAppDetails:false` correctly suppresses the extra
record. `country`/`language` returned real GB-market reviews, not empty or an error. `charged
EventCounts` matched the dataset row count on BOTH runs (`{result:10}` test, `{result:6}`
control) -- confirming the app-details record is itself a billed result event, consistent with
its own schema description ("push one extra item"). CLEAN, no code change, 0 defects.

**PPE rotation advanced for free** (c2172's efficiency lesson: fold the spot-check into the
`varied_test` runs instead of spending separate ones): both Actors' charge paths verified live
and correct across 4 total runs this cycle. Rotation now **7/~26** (prior 5: `trademark-search-
scraper`, `court-records-scraper`, `uk-find-a-tender-scraper`, `apple-podcasts-scraper`,
`clinicaltrials-scraper`).

`state/audit_dates.json` updated for both slugs (`varied_test: 1821 -> 2175`, full notes
prepended, history preserved).

$0.001 spent (4 small capped runs), 0 new Actors, no owner email. Services active, site 200 on
`/` `/tools` `/pricing`.

**Next cycle (2176): re-verify `audit-due --all`/`checks-due` fresh first. `2176 % 3 == 1`, not a
QUALITY slot. Fleet-oldest `varied_test` is now `fec-campaign-finance-scraper` + `shopify-
products-scraper` (both 1824, per `audit_dates.json`) for the next QUALITY slot (2178). Open
items unchanged: the PPE `chargedEventCounts` rotation (7/~26, fold into future `varied_test`
runs), DMARC recheck (blocked on a report newer than `e2f3a358`), the `trademark-search-scraper`
buyer-intent watch (run-count climb alone never triggers an owner email -- see c2168).
`check-rental-converts` fleet check due at cycle 2179.**

