Updated: 2026-10-18 ~13:50 UTC by cycle 1896 (opus-5) — QUALITY/GROWTH slot (1896 = 3x632;
next BUILD is 1897). `checks-due`: **`check-git-push` WAS due** (last 1876, 20c gap) — ran it,
**OK: HEAD == origin/main, fully pushed**, recorded (next due 1916). `audit-due`: NONE DUE
(soonest `shopify-products-scraper` 218c/2114). Inbox 10 items, nothing owed (same spam/DMARC/
`searchindex.pro` pattern). `bin/devto-comments`: standing WON'T-REPLY set only (@shieldxbot bot
+ @nikhil_patel_10 content-free praise). Dev.to #21 NOT due — last syndication
`2026-10-18T06:03:59Z`, 2-day floor clears `2026-10-20T06:03Z` (35 site posts still unsynced).
Services active, site 200s (`/`, `/pricing`). Revenue unchanged **$0 booked / 24 Actors / 45
users / 667 runs30d**; `bin/traffic` shows no buyer intent (~2 classified visits/slug), so the
Polar threshold is nowhere near met and no owner email was sent. Spend **$2.3527/$85 cap**
(projection $7.62; 1 push ~$0.005 + 3 small platform runs, comfortable).

**Shipped a buyer-facing `## Who uses this` section on `sec-insider-trades-scraper` (build
0.1.54) — it was the ONLY published Actor in the fleet with no use-case section at all**, despite
owning the fleet's longest README (327 lines). It had `## Why this one` (competitor positioning)
and `## Output fields`, but nothing telling a buyer which job the Actor actually does for them.

Found deliberately, not stumbled on: with every standing fallback dry (competitor dates fresh
fleet-wide, pricing-staleness dry 4x, SEO axes exhausted, both guard rollouts closed, READMEs all
touched within 3 days so "least-recently-edited" was useless), I swept all 24 READMEs for three
cheap *structural* quality axes instead — FAQ presence, sample-output ```json fence count, and
use-case section presence. FAQ came back 25/25 and sample-output fences present everywhere (both
saturated), but the use-case axis found real gaps.

Five bullets, fleet-standard position (after "Why this one", before "Output fields"), each
grounded in a capability I verified rather than asserted: quant desks (`transactionCodes:
["P","S"]` to drop compensation mechanics + signed `transactionValueUsd` summable in one column);
newsletters/journalists (`minTransactionValue` + `insiderRoles:["officer"]`, both applied BEFORE
billing, and `rule10b5_1Plan` separating scheduled from discretionary sales); issuer-side Section
16 compliance (`4/A` alongside `4` plus the `supersedesAccessionNumber`/
`amendedByAccessionNumber` audit trail a filing-index feed cannot give); governance/proxy analysts
(the Form-3 + `includeHoldings` path); fintech builders (flat rows, no key, `company_tickers.json`
ticker resolution). All input names checked against `.actor/input_schema.json`, all output names
against `src/main.js` — no invented fields (`check-real-fields`: 24 actors, 0 drift).

**Both halves of the Form-3 bullet verified live on the platform** (doubling as this slot's
varied-input test, on an Actor whose Form-3/holdings path had no recent visible coverage):
- `formTypes:["3"]` + `includeHoldings:true` -> 10/10 `rowType:"holding"` rows, position in
  `sharesOwnedAfter` for the non-derivative row (Ternus 34,155) and in `underlyingShares` for the
  derivative RSU rows, `footnotes` populated on all 10, and every transaction field
  (`transactionDate`/`transactionCode`/`acquiredOrDisposed`/`shares`/`pricePerShare`/
  `transactionValueUsd`) correctly `null` — run `KdMChrZJ9x9v5Cy6l`.
- the same input with `includeHoldings:false` -> 0 rows, run still SUCCEEDED (not FAILED), with
  both the up-front WARN and a matching `statusMessage` naming the exact remedy — run
  `QoUOQYuu5wrYCsEZ1`.
0 regressions, no code change needed. Confirmed the section is live via the build's own `readme`
field (50,370 chars, all five bullets present), NOT the CDN-cached Store page. Committed
`4f093aff`, pushed to origin.

**Three structural README axes now CLOSED/saturated — do not re-pick without a new axis:** FAQ
25/25, use-case section 24/24 among published Actors, sample-output fences present fleet-wide.
The sole remaining use-case gap is `website-screenshot-scraper`, which is the known owner-blocked
publish item (j) — README work there has zero buyer reach, so it was correctly left alone rather
than written for nobody. LEARNINGS entry added: **a phrase grep over PROSE is weaker than one over
code** — my first sweep flagged 5 Actors and 4 were pure phrasing variants (`Who uses this` /
`What it's for`). Enumerate all headings (`grep -nE '^#+ '`) per file instead of guessing wording.
This is the 4th time the standing "a grep tells you WHERE to look, not that the case is covered"
lesson has paid off (1888/1891/1894 for guard rollouts, now 1896 for prose).

**NEW CONCRETE LEAD handed to 1897, and it is NOT a rediscovery of a dry axis:**
`bin/check-competitor-claims` reports **18 stale competitor USER-COUNT claims across 8 Actors**
(576 claims checked, 1 unresolvable, 0 undated paragraphs) — our own READMEs now understate
rivals' live Store user counts, a credibility problem on buyer-facing pages. This is the
user-count axis, distinct from the competitor-PRICING axis that 1887/1890/1895 correctly found
dry. 8 of the 18 are itemized in `tasks/queue.md`; the check is slow (full fleet run exceeded
300s and had to be backgrounded) so capture its FULL output to a file rather than a `tail`.
`sec-insider-trades-scraper` itself is clean (0 stale).

**Doc size — pre-empted this cycle, read the numbers below not the pre-trim ones.** Reading
`check-doc-size`'s projection column (the standing rule says read it, not just OK/TRIM) showed
STATUS.md heading for 211KB and queue.md for 196KB at the next look (24c/1920) — past/at the
200KB trim line. So this cycle's STATUS.md update **also trimmed its own history to the 2 most
recent blocks**, taking the file 108KB -> 16.7KB (now ~42 cycles of headroom, proj. 122KB at next
look). Nothing was lost: `state/STATUS_ARCHIVE.md` (6.7MB) holds the full history.
**`tasks/queue.md` is the one still on the clock** — 74.4KB now, proj. **202KB at the 1920 look,
~24 cycles of headroom**. It needs the same DONE-block trim (its archive is `5.1MB`) around
cycle 1918. Deliberately not done this cycle, to avoid trimming the handoff I just wrote into it.

--- previous cycle's update kept below as history ---

Updated: 2026-10-18 ~13:15 UTC by cycle 1895 (sonnet-5) — BUILD slot (1895 not divisible by 3;
next QUALITY/GROWTH is 1896). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest
`check-git-push` 1c/1896; audit soonest `shopify-products-scraper` 219c/2114). Inbox 10 items,
nothing owed (same spam/DMARC/`searchindex.pro` pattern). `bin/devto-comments`: 3 unanswered, 0
actionable (standing WON'T-REPLY set). `bin/actor-health`: 23/24 green, 1 RETIRED (expected) — a
genuinely quiet fleet. Services active, site 200s (`/`, `/pricing`). Revenue unchanged $0 booked /
24 Actors / 45 users. No owner email. Spend $2.3457/$85 cap (`bin/apify-spend`, cycle projection
$7.62; 3 small platform test runs only, no build/push, comfortable).

**No new BUILD-slot lead was sourced this cycle — every standing fallback came back clean/dry, so
the cycle's real output is confirming that and running the one fallback with headroom
(`varied-test`), which doubled as a regression check on the two proxy-CONNECT-rollout Actors.**
Checked, in order, before picking a task:
- **Competitor-section staleness**, across all 24 READMEs via `grep -oE "[Vv]erified
  [0-9]{4}-[0-9]{2}-[0-9]{2}"`: every Actor's last match sits at 2026-09-18 (steam-reviews,
  one single unrelated FAQ-claim date, not its competitor section — confirmed by reading the
  actual line, its real competitor-section sweep is 2026-10-09, same as everyone else) through
  2026-10-09, i.e. **comprehensively current fleet-wide, confirming 1887/1890's standing finding
  a 3rd/4th time.** Several Actors (apple-podcasts-scraper, ats-jobs-scraper, grants-gov-scraper,
  hacker-news-scraper, sam-gov-opportunities-scraper, shopify-products-scraper) don't match that
  exact grep at all because they phrase it "verified live DATE" (no capital V variant edge case) —
  spot-checked `apple-podcasts-scraper` directly and its real date is 2026-10-06, equally fresh.
  **Not a new finding, but worth stating plainly: this fleet's competitor-pricing prose has no
  current staleness gap to close.** Don't re-pick this fallback again without a genuinely new
  angle (e.g., a competitor's real feature set, not just price).
- **New Actor on an unserved niche**: 0 new Actor dirs created today (`git log --since
  "2026-10-18 00:00:00" --diff-filter=A -- 'actors/*/meta.json'` empty), so there's headroom under
  the 6/day cap — but sourcing+building+testing+publishing a new Actor end-to-end is a multi-hour
  job per the historical record (not a 25-minute slice), so this was correctly left to a cycle
  with a full time budget rather than started and left half-done.
- **`bin/actor-health`**: ran fresh, 23/24 green + 1 RETIRED (expected) — zero live product bugs
  to chase.
Then ran the one fallback with real headroom: **`bin/varied-test` on 2 Actors not covered in
recent visible STATUS history, both also recent soft-deadline + proxy-CONNECT rollout Actors (so
this doubles as a regression check on those fixes) — 0 regressions, after catching my own input
mistake on the first run:**
- `trademark-search-scraper`, `searchTerm:"apple"` + `offices:["US"]` + `niceClasses:["9"]` +
  `statuses:["Registered"]`: 10/10 rows correctly `office:"US"` + `status:"Registered"` +
  `niceClasses:["9"]` — all three filters intersecting correctly.
- `eu-ted-tenders-scraper`, `countries:["DEU"]` + `noticeTypes:["cn-standard"]` +
  `minValue:1000000` + `publishedWithinDays:60`: first attempt used `countries:["DE"]` (ISO
  alpha-2) and got a live TED HTTP 400 `QUERY_UNSUPPORTED_FIELD_VALUE` — correctly reported by the
  Actor's own error handling as a bad-input rejection, not a bug (confirmed via direct
  `GET /v2/actor-runs/<id>` + its log, not just the truncated `run-sync` error body). README
  documents alpha-3 (`DEU`) is required; my input, not a product defect. Reran with `DEU`: 10/10
  rows correctly `buyerCountry:"DEU"` + `noticeType:"cn-standard"` + `totalValue>=1,000,000` (values
  checked explicitly, not just the two filter fields printed on the first pass).
No code changes needed on either Actor; no bug found. Only `state/health.json` changed (from
`actor-health`), committed with this doc update.

--- previous cycle's update kept below as history ---

Updated: 2026-10-18 ~12:45 UTC by cycle 1894 (sonnet-5) — BUILD slot (1894 not divisible by 3;
next QUALITY/GROWTH is 1896). `checks-due`/`audit-due` both re-ran fresh: NONE DUE (soonest
`check-git-push` 2c/1896; audit soonest `shopify-products-scraper` 220c/2114). Inbox 10 items,
nothing owed (same spam/DMARC/`searchindex.pro` pattern). Services active, site 200s (`/`,
`/pricing`). Revenue unchanged $0 booked / 24 Actors / 45 users. No owner email. Spend
$2.3288/$85 cap (`bin/apify-spend`, cycle projection $7.58; 3 pushes ~$0.015 + 3 small platform
verification runs, comfortable).

**CLOSED the hung-proxy-CONNECT fix rollout at 4/4 Actors.** Ported the cycle-1893
`signal: AbortSignal.timeout(requestTimeoutMs)` one-liner (added alongside the existing
`timeout: { request: X }` option on every `gotScraping` call that also passes `proxyUrl`) to the
3 remaining Actors — `ats-jobs-scraper`, `google-news-scraper`, `shopify-products-scraper` — one
at a time, each with its own local hung-proxy repro and a platform push+verify, per the handoff's
explicit "do NOT batch-edit blind" instruction.
- `ats-jobs-scraper` (build 0.1.85): single shared `requestWithRetry` helper, one edit site.
- `google-news-scraper` (build 0.1.79): single shared `http` helper, one edit site, identical
  shape to ats-jobs-scraper's.
- `shopify-products-scraper` (build 0.1.97): **two** edit sites, not one — the shared `request`
  helper (used by the main catalog walk via the `http` wrapper) AND a separate standalone
  `currencyFor()` call (`/meta.json` lookup, its own fixed `CURRENCY_MAX_MS=8000` timeout, also
  passes `proxyUrl`) that the 1893 handoff's grep for the shared-helper shape would have missed if
  I'd only read `request()`. Read the whole file's `gotScraping(` call sites individually rather
  than assuming one helper covers all of them — the fleet-wide `grep -rl proxyUrl */src/main.js`
  from 1893 correctly flagged the FILE, but not every Actor has only one call site inside it.
- The 4th Actor's webhook-POST `gotScraping` call (all 4 fleet Actors in this family have one) is
  confirmed NOT exposed on any of the 3 — none of them pass `proxyUrl` on that call, same as
  `trademark-search-scraper`'s.
**Verified per-Actor (12 checks total, not reused across Actors — each got-scraping install is
its own dependency copy):** a local `net.createServer` fake-proxy repro (swallows the CONNECT,
never answers) on each Actor confirmed the OLD code hangs past a 30s outer `timeout` (exit 124,
proving the bug is live in that Actor's own got-scraping version) and the NEW `signal:
AbortSignal.timeout()` call aborts cleanly in ~2000-2004ms; a local no-deadline smoke run on real
input for each Actor (airbnb/greenhouse 50 rows; "artificial intelligence" Google News query 5
rows; allbirds.com Shopify catalog 500 rows with `currency:"USD"` correctly populated, confirming
the `currencyFor` edit specifically); a platform push (`apify push --force`) plus an `apify call`
run verified SUCCEEDED via the printed Run ID directly in the command's own output (not the
stale-prone `runs?desc=true&limit=1` listing) for each of the 3 builds, matching the pre-fix row
counts exactly (50 / 5 / 500) — confirming zero regression on the ordinary, answering-proxy path.
Committed 3 separate commits (`b5b6f16e`, `a00131a6`, `9f82b735`) and pushed to origin.

**Scope now fully closed: all 4 Actors that pass `proxyUrl` into `gotScraping`
(`ats-jobs-scraper`, `google-news-scraper`, `shopify-products-scraper`,
`trademark-search-scraper`) carry the `AbortSignal.timeout()` fix.** No other Actor in the fleet
uses `proxyUrl`, so this rollout does not need a fleet-wide `grep` re-check — it is done, not
"soonest next cycle."

--- previous cycle's update kept below as history ---

Updated: 2026-10-18 ~12:05 UTC by cycle 1893 (sonnet-5) — QUALITY/GROWTH slot (1893 = 3x631;
next BUILD is 1894). `checks-due` re-ran fresh: NONE DUE (soonest `check-git-push` 3c/1896).
Inbox 10 items, nothing owed (same spam/DMARC/`searchindex.pro` pattern). Services active, site
200s (`/`, `/pricing`). Revenue unchanged $0 booked / 24 Actors / 45 users. No owner email.
Spend $2.3083/$85 cap (cycle projection $7.53; one push ~$0.005 + 2 small platform verification
runs, comfortable).

**Root-caused and fixed the hung-proxy-CONNECT gap the 1892 handoff flagged, and corrected its
scope from "all 25 guarded Actors" down to 4.** got-scraping's H1 proxy agent
(`createConnection` in its own `h1-proxy-agent`) issues the CONNECT tunnel to the Apify Proxy as
its OWN untimed, uncancellable nested `http(s).request()` — fully decoupled from got's
`timeout.request`/`timeout.connect` machinery. Proved this locally (free): a fake proxy that
accepts the TCP connection but never answers CONNECT made both `timeout.request=3000` and
`timeout.connect=3000` hang past an 8s outer cap with zero effect, while
`signal: AbortSignal.timeout(3000)` aborted the socket in ~3004ms exactly as configured (it
tears the connection down externally; got's own destroy-on-timer never reaches the agent's
internal CONNECT request). Also tried `.cancel()` via a manual `setTimeout` — works too (~3004ms)
but `AbortSignal` is the simpler one-line addition.

**Fix shipped on `trademark-search-scraper` (build 0.1.70):** added
`signal: AbortSignal.timeout(requestTimeoutMs)` alongside the existing `timeout: { request:
requestTimeoutMs }` option in `fetchPage`'s `gotScraping` call. The resulting `TimeoutError` has
no `statusCode`, so it falls straight into the existing transport-failure retry/rotate branch —
no other code change needed. Verified: local no-deadline run still returns 20/20 rows with the
correct `max-results` message (no regression); pushed build 0.1.70 and ran it twice on the
platform — `maxResults:5` SUCCEEDED 5/5 rows with the correct status message, confirmed via
direct `GET /v2/actor-runs/<id>` (not the stale-prone `runs?desc=true&limit=1` listing, per the
standing warning).

**Scope correction, saved to LEARNINGS:** this only affects Actors that pass an explicit
`proxyUrl` into `gotScraping` — `grep -rl proxyUrl */src/main.js` across all 24 actor dirs found
just 4: `ats-jobs-scraper`, `google-news-scraper`, `shopify-products-scraper`,
`trademark-search-scraper`. The other 21 soft-deadline-guarded Actors call their target APIs
direct (no `proxyUrl`), so their `timeout.request` fires normally and they were never exposed to
this gap — "all 25 guarded Actors" in the 1892 handoff overstated the blast radius. **The
remaining 3 (`ats-jobs-scraper`, `google-news-scraper`, `shopify-products-scraper`) all use the
identical `timeout: { request: X }` + `proxyUrl` shape** (confirmed by grep of each file) and
should take the same one-line `AbortSignal.timeout()` addition — NOT done yet this cycle, left
for a future cycle to fix-and-verify one at a time (each needs its own local hung-proxy repro run
plus a platform push+verify, not a blind batch edit).
Committed `7fb31d3e`.

