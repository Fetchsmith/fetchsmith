# Trademark Search Scraper — USPTO, EUIPO & 70+ Offices (TMview)

Search registered trademarks across **70+ national and regional trademark offices** — USPTO (US), EUIPO (EM), UK, DE, FR, JP, CN, WIPO (WO) and more — through the official [TMview](https://www.tmdn.org/tmview/) database. One search covers every office you select in a single run; no need to query each country's own registry separately.

## What it does
- Sends your search term to TMview's public search API and returns matching trademarks as structured JSON, one row per mark.
- Filter by office (country/region), Nice classification class, trademark status (TMview's four values: `Registered`, `Filed`, `Ended`, `Expired`), and mark type (`Word`, `Figurative`, `Combined`, and others — see `tmTypes`).
- Pay per result: you are charged only for rows actually returned. HTTP-only (no browser), so runs are fast and cheap.

## Input
| Field | Type | Description |
|---|---|---|
| `searchTerm` | string | Word or brand to search for (contains-match by default — see `matchMode`). Default `"coffee"`. |
| `matchMode` | string | How `searchTerm` is matched: `contains` (default, plain substring, no word boundary — `"solar"` also matches `SOLARWINDS`), `startsWithPrefix` (**the true "begins with" mode, and the right one for clearance** — `"coff"` matches `COFF`, `COFFEE` and `ＣＯＦＦ`, but not `HAIR SYRUP coff`; filtered client-side, so non-matches are never charged), `startsWith` (**whole word anywhere in the name**, not just at the start — `"syrup"` matches `SYRUP`, `HAIR SYRUP` and `Coff Syrup` alike, while `"coff"` matches `Coff Chi` but **not** `COFFEE`) or `endsWith` (**plain suffix letters**, no word boundary — `"offee"` matches `toffee`, `woffee` and `COFFEE`). Both value names are historical and describe neither behaviour exactly; see the FAQ below before using either for clearance. An unrecognised value falls back to `contains` with a warning. |
| `offices` | array | Two-letter office codes, e.g. `US` (USPTO), `EM` (EUIPO), `GB`, `DE`, `FR`, `JP`, `CN`, `WO` (WIPO). Case-insensitive — TMview itself matches these case-sensitively, so a lowercase or mixed-case code (e.g. `us`, `De`) is corrected for you automatically. TMview covers exactly 81 offices; an unrecognised code (common mix-ups: `UK` should be `GB`, `EU` should be `EM`) matches no trademark at all, so the run warns and tells you in its status message instead of just returning an empty dataset. Leave empty to search all 81 offices. |
| `niceClasses` | array | Restrict to Nice classification classes, e.g. `"25"` (clothing), `"9"` (software). The Nice Classification has 45 classes (1-34 goods, 35-45 services); zero-padded forms like `"09"` work too. A value outside 1-45 matches no trademark at all, so the run warns you rather than silently returning nothing. Leave empty for all classes. |
| `statuses` | array | Restrict to statuses. TMview recognises exactly four: `Registered`, `Filed`, `Ended`, `Expired`. A differently-cased match (e.g. `registered`) is corrected for you automatically; a value that isn't one of the four at all (e.g. `Opposed`, `Pending`, `Withdrawn` — TMview has no such statuses) matches nothing — the run warns and says so in its status message rather than silently returning an empty dataset. Leave empty for all. |
| `tmTypes` | array | Restrict to mark types, e.g. `Word` or `Figurative`. 10 values are live-confirmed: `Word`, `Combined`, `Figurative`, `Undefined`, `Other`, `Stylized characters`, `Colour`, `3-D`, `Hologram`, `Position`. Case-insensitive — corrected for you automatically, same as `statuses`. **Unlike `offices`/`niceClasses`/`statuses`, this list is known to be incomplete** (the 10 confirmed values' individual counts don't add up to the unfiltered total — see FAQ), so an unrecognised value is still sent to TMview as-is rather than treated as a dead filter; it may be a real type this Actor hasn't confirmed yet. Leave empty for all types. |
| `maxResults` | integer | Stop after this many trademarks (default 50, max 5000). |
| `watchLabel` | string | Optional watch-mode label. The first run under a label seeds a baseline (0 rows returned, 0 charged); every later run on the same label + search returns and charges only marks not already delivered — a scheduled "alert me on new filings" feed instead of the same full result set every time. Leave unset for a plain, repeatable search. |
| `watchChanges` | boolean | Optional, requires `watchLabel`. Also re-deliver a mark you already have if its `status` changed since you last saw it (e.g. `Filed` → `Registered`) instead of only ever reporting brand-new filings. Default `false` — see FAQ. **Do not combine with the `statuses` filter — see "don't filter on the field you're watching" below.** |
| `webhookUrl` | string | Optional. POST a small JSON completion summary (marks pushed, marks scanned, dataset ID, watch new/changed/skipped counts) here when the run finishes — see FAQ. |

## Output
One item per trademark with **22 fields**: `id`, `st13`, `url` (link to the office's own record), `trademarkName`, `office`, `status`, `trademarkType`, `applicationNumber`, `registrationNumber`, `applicationDate`, `registrationDate`, `expirationDate`, `oppositionPeriodStart`, `oppositionDeadline`, `seniorityClaimed`, `applicantNames`, `niceClasses`, `viennaCodes`, `territories`, `markImageUrl`, `detailImageUrl`, and `watchLabel` when set.

**Watch-mode change fields, only on a `watchChanges` re-delivery**: `_watchChangeType` (currently always `["status"]`), `_watchPrevious` (`{ "status": "<previous value>" }`).

Sample row:
```json
{
  "id": "004176283",
  "st13": "004176283",
  "url": "https://www.tmdn.org/tmview/#/tmview/detail/EM500000004176283",
  "trademarkName": "SOLARWINDS",
  "office": "EM",
  "status": "Registered",
  "trademarkType": "Word",
  "applicationNumber": "004176283",
  "registrationNumber": "004176283",
  "applicationDate": "2004-11-22",
  "registrationDate": "2005-08-30",
  "expirationDate": "2034-11-22",
  "oppositionPeriodStart": "2005-01-15",
  "oppositionDeadline": "2005-04-15",
  "seniorityClaimed": false,
  "applicantNames": ["SolarWinds Worldwide, LLC"],
  "niceClasses": ["9", "42"],
  "viennaCodes": [],
  "territories": ["EM"],
  "markImageUrl": null,
  "detailImageUrl": null
}
```

## FAQ

**I got 0 results and the run still says "Succeeded" — what happened?**
A run that returns nothing always tells you which of the three reasons applied, in its status message, and you are charged nothing in every case. (1) **An invalid filter value** — a value no trademark can carry, e.g. `UK` instead of `GB` for an office, a Nice class outside 1-45, or a status that isn't one of the four TMview recognises. The message names each bad value and says it's a filter-value problem, not an empty search. (`tmTypes` is the one exception — see the next FAQ entry — since an unrecognised value there is NOT asserted to be a dead filter.) (2) **A cap you set** — `maxResults` or the run's own Apify cost limit stopped it early; the message reports how many matches TMview declared so you know what raising the cap would buy. (3) **A genuinely empty search** — every value you gave is valid and TMview simply holds no matching mark. Here the message distinguishes the two cases that need different fixes: if you *did* set filters it names them and tells you to drop or widen them one at a time (the office filter is usually the narrowest); if you set *none*, it says so explicitly, because there is then no filter to widen and the term itself is what needs changing — check the spelling or try a shorter stem, since matching is "name contains", not exact. Note that `offices` defaults to `["US", "EM"]`, so unless you clear it the message will name those two as the filter narrowing your search even though you never typed them — clearing `offices` widens the run to all 81. `RUN_SUMMARY` carries the same facts as data (`declaredMatches`, `scanned`, `delivered`, and the `unknownOffices`/`unknownNiceClasses`/`unknownStatuses`/`unknownTmTypes` arrays). Watch-mode runs are different by design: a run under a `watchLabel` returning 0 rows usually means "nothing new since last time", which is the expected result most of the time — see `watchLabel` below.

**I got a "Could not reach TMview through any network path" FAILED run — is this Actor broken?**
Fixed cycle 2441. TMview's search API sits behind a bot-detection sensor that, as of late October 2026, requires a session cookie — one that only a prior plain GET to the TMview search page sets — before it will answer the search API with real JSON; without it, every request (from this box directly, from Apify's datacenter proxy, and from residential proxy alike) got a 200 OK containing a JS challenge page instead of data. This run now does that GET first and carries the resulting cookie through the search request, same cookie jar re-primed on every proxy rotation. The *remaining* cause of this message is the pre-existing, unrelated issue it was originally written for: an individual Apify proxy exit node that cannot reach TMview at all (a transport-level timeout, not a WAF challenge) — the run already rotates through multiple exit nodes and a direct connection before giving up, so seeing this message means all of them failed in the same run; it fails safely, charging nothing, and a plain re-run almost always lands on a working exit node.

**Why does `tmTypes` warn instead of rejecting an unrecognised value outright, unlike `offices`/`niceClasses`/`statuses`?** Added cycle 2406. TMview's mark-type filter (`fTMType`) is real and server-side — live-confirmed against `basicSearch: "solar"` (69,710 unfiltered matches), where `tmTypes: ["Word"]` alone narrows that to 28,833 — but unlike the other three filters, this cycle could not confirm the enum is *closed*. The 10 confirmed values (`Word`, `Combined`, `Figurative`, `Undefined`, `Other`, `Stylized characters`, `Colour`, `3-D`, `Hologram`, `Position`) individually narrow the baseline but sum to only 68,741 — 969 marks short of 69,710 — so at least one more real type value exists that this cycle's probing did not reach. Treating the 10-value list as complete and rejecting anything outside it (the way `statuses`' closed four-value set does) risked silently blocking a real buyer search. So an unrecognised `tmTypes` value is warned about but still forwarded to TMview as-is — if it's a typo it will match nothing (same outcome as the closed filters), but if it's one of the still-unconfirmed real values, the search works anyway.

**Why are `viennaCodes` and `markImageUrl` empty on some rows?**
`viennaCodes` (figurative-element classification) only exists for `trademarkType: "Figurative"` marks — a plain word or stylized-character mark has no image elements to classify, so it's correctly empty. `markImageUrl`/`detailImageUrl` are populated for most records regardless of type (TMview generates a thumbnail URL per record), but a handful of older or office-specific entries omit it upstream — treat a `null` there as "no image on file at the source office," not a bug.

**Why does the same brand appear more than once?**
Trademarks are filed per office and per class. A global brand typically holds a separate registration in each office it operates in, and sometimes multiple classes within one office — each is a distinct legal record with its own `id`.

**Does this replace a formal trademark clearance search?**
No. This is a fast screening tool over TMview's public index. For legal clearance opinions or freedom-to-operate analysis, consult a trademark attorney or the offices' own certified search tools.

**How does `watchLabel` decide what's "new"?**
It keys a baseline by `st13` (the stable per-record id) against the exact combination of `searchTerm`/`offices`/`niceClasses`/`statuses` you pass — change any of those and the label starts a fresh baseline. Plain `watchLabel` tracks new-to-the-baseline marks (e.g. a fresh filing that now matches your search); set `watchChanges: true` to also catch a status move on a mark you already have. `matchMode` and `tmTypes` only join that combination when you set them to something other than their defaults — a label created before either input existed, or one that never sets them, keeps its original baseline untouched; setting `tmTypes` on an existing label starts a fresh one, same as changing any other filter.

**What happens if I start two runs on the same `watchLabel` at once?**
As of build 0.1.79, the second one fails immediately with "already being processed by another run" and is charged nothing — before this, two overlapping runs on the same label (a buyer starting a second run manually while the first was still going, or a scheduled run firing before the previous one finished) both read the same baseline, both independently decided the same marks were "new," and both charged and delivered them: a real double charge, not a cosmetic duplicate row. A per-label lock (a separate key-value record, never the baseline itself) now blocks a concurrent run on that same label before it reads or charges anything. The lock self-expires after 2 hours, so a crashed run can never wedge a label shut — only the Actor itself should ever hold it. This only protects runs sharing the exact same `watchLabel` + search criteria; two different labels, or the same label with a different `searchTerm`/`offices`/`niceClasses`/`statuses` (a different baseline fingerprint), never contend with each other.

**What does `matchMode` actually change, and why would I use it?**
`searchTerm` is always matched against the trademark name, never exact — the question is *where*. `contains` (default) is a pure substring with no word boundary: searching `"solar"` matches every name containing those five letters anywhere, including `ALÔ SOLAR`, `SOLARWINDS` and `SOLAR ALPS`.

`startsWithPrefix` is the **true "begins with" mode**, and the one to use for clearance. The other two are **named after what TMview's own undocumented `criteria` codes are called, not after what they do** — re-verified live (cycle 2500, GB office, 5–10 rows per probe):

| Value | What it actually matches | Live probe |
| --- | --- | --- |
| `startsWithPrefix` | The name **begins with** the term — including inside a longer word, which is the whole point. Leading quotes/dashes and full-width (JP/KR) letter forms are normalised first, so a decorated name still matches. | `"coff"` → `COFF`, `COFFEE`, `Coff Chi`, `ＣＯＦＦ　ＣＯＦＦＥＥ` — and **not** `HAIR SYRUP coff`. `"acme"` → `ACME`, `"ACME"`, `-Acme Group`, `ＡＣＭＥ`. |
| `startsWith` | The term as a **complete word anywhere in the name** — first word or last, it makes no difference. A prefix of a longer word is *not* a word and does not match. | `"syrup"` → `SYRUP`, `SYRUP DROPS`, `HAIR SYRUP`, `Coff Syrup`. `"coff"` → `Coff Chi`, `COFF STOP`, `Coff Syrup` — and **not** `COFFEE`. `"zzle"` → only `POO-ZZLE`. |
| `endsWith` | The **last letters of the name**, as a plain substring with no word boundary at all. | `"offee"` → `toffee`, `woffee`, `Qoffee`, `COFFEE`. `"zzle"` → `Dizzle`, `RAZZLE`, `DAZZLE`. |

So the half-word fragment `"solarw"` returning **zero** under both (it matches 829 marks under `contains`) is two different facts, not one: there is no *word* `solarw` for `startsWith`, and no name *ending* in `solarw` for `endsWith`.

**For brand clearance, use `startsWithPrefix`.** A mark that begins with your proposed name inside a longer word — `COFFEE` when you search `"coff"` — is invisible to `startsWith`, and is exactly the mark you most need to see; `contains` does show it, but buried in every mid-name hit. `startsWithPrefix` answers the clearance question directly. Use `startsWith` when you want the term as its own word and nothing else (it cuts `SOLARWINDS`-style compounds out of a noisy `contains` result), `endsWith` to check a suffix convention across a brand family, and `contains` when you want the widest possible net and will sift it yourself.

**Two things to know about `startsWithPrefix`, because TMview has no prefix search of its own.** This Actor asks TMview for `contains` (the narrowest superset of a prefix match that TMview supports) and applies the prefix test here, which means: (1) **rejected marks are never pushed and never charged** — you pay the same $0.002/result for prefix hits only; and (2) the run **reads more pages per delivered row**, so give it 300s+ under *Input → Run options* on a broad term. The match count in the log is then TMview's wider pre-filter `contains` total, and the run says so; `RUN_SUMMARY` breaks it down into `scanned`, `prefixFiltered`, `prefixConsidered` and `delivered`, with `declaredMatchesIsPreFilter: true`. A clean clearance result — TMview has marks containing your term but none beginning with it — finishes **SUCCEEDED with 0 rows and nothing charged**, and the run's status message says so explicitly rather than looking like an error.

**What does `watchChanges` add, and does it cost extra?**
No extra fee — a changed mark is billed at the same per-row price as a new one. Plain `watchLabel` stays silent forever about a mark it already delivered, even once its `status` moves from `Filed` to `Registered`, or into `Ended`/`Expired` — exactly the moment an opposition or renewal watch cares about most. Set `watchChanges: true` and each run also compares every already-delivered mark's `status` against what it looked like last time; if it moved, the row is re-delivered tagged with `_watchChangeType: ["status"]` and `_watchPrevious: { "status": "<old value>" }`. Off by default so existing watch labels keep their current behaviour; a label created before this shipped just starts detecting status drift from its next run onward, not an artificial backlog of every status move since the baseline was first seeded.

**Don't filter on the field you're watching.** `statuses` is sent to TMview as a *server-side* filter, and `status` is also the only field `watchChanges` compares. So a run with `statuses: ["Filed"]` and `watchChanges: true` can never tell you a mark moved to `Registered`: the moment its status stops being `Filed`, the row stops matching your search, is never returned, and there is nothing left to compare — the run just reports "nothing new". Verified live cycle 1561: a baseline seeded with `statuses: ["Filed"]`, holding a mark that has since moved to `Registered`, returned **0** changed rows; the identical run with no `statuses` filter returned exactly **1** row tagged `_watchChangeType: ["status"]`. **What to do about it.** Run `watchChanges` without the `statuses` filter and filter the delivered rows on your own side — every row carries `status`, so nothing is lost. Or keep two scheduled runs: a filtered one for brand-new marks, and an unfiltered `watchChanges` one for status transitions. Any run with this problem says so: two warnings in the log, a note appended to the "nothing new" message so a permanently-blind run can't masquerade as a healthy quiet one, and `watchChangeBlindFilters` in `RUN_SUMMARY` (`null` when `watchChanges` is off, `[]` when the run is clean, otherwise `["status"]`).

**Baseline size cap.** The recorded baseline holds at most 20,000 mark ids per label; once a label's cumulative baseline grows past that, the oldest ids are dropped to bound the record's size. A dropped id is treated as "new" again on a later run and re-charged, even though you already paid for it. This only bites a label with a very high cumulative volume of matches over many runs — narrowing the search (tighter `searchTerm`, fewer `offices`, specific `niceClasses`/`statuses`) keeps a baseline well under the cap. A run that actually drops ids says so explicitly in its log and status message, and reports the exact counts as `baselineTruncated`/`baselineTruncatedTotal` in the `webhookUrl` payload.

**Why are `expirationDate`, `oppositionPeriodStart`, `oppositionDeadline` and `seniorityClaimed` null on some rows?**
Not every office publishes every date through TMview, and availability is a property of the **office**, not of the record. Measured 2026-09-24 on 50 rows per office for the same search: `expirationDate` was present on 49/50 GB rows and 30/50 EM rows but **0/50 US and 0/50 DE** rows; `seniorityClaimed` on 50/50 GB and DE but 0/50 US; `oppositionDeadline` on 47/50 EM and 0/50 US. So a US record rarely carries `expirationDate` while a UK or EU record almost always does, and `oppositionDeadline` only exists once a mark has actually passed through publication (an application still pending examination has no opposition window yet). `seniorityClaimed` is `null` when the office doesn't expose the field at all, and `false`/`true` when it does. Treat `null` as "not published for this office/record," not a data error.

**Why use this instead of USPTO's own API?**
As of October 2026, every official USPTO trademark API route we checked requires a registered API key: TSDR (`tsdrapi.uspto.gov`) returns `401` with a notice to register at `account.uspto.gov`, the newer Open Data Portal (`api.uspto.gov`) returns `401`/`403` on every path we tried (including just listing datasets), and the old bulk-data endpoint (`developer.uspto.gov/ds-api`) now redirects into that same gated portal. TMview is run by EUIPO, not USPTO, but it ingests USPTO's own register as one of its 70+ offices — restrict `offices` to `["US"]` and you get the same official records with no key, no account, and no login. See [USPTO's own trademark APIs now all require a key](https://fetchsmith.com/blog/uspto-trademark-api-needs-a-key) for the measurements.

**What about EUIPO's own API?** Also gated, checked live against two separate products (`trademark-search_110` and `design-search`) — both return `401 Invalid client id or secret` with no free tier on Sandbox or Production. EUIPO runs TMview too, so restricting `offices` to `["EM"]` here gets the same EU register with no account or app registration. See [EUIPO's own trademark API is gated too](https://fetchsmith.com/blog/euipo-trademark-api-needs-a-key) for the measurements.

**How is `webhookUrl` different from Apify's own platform webhooks?**
Apify's platform webhooks are configured separately per Task/Actor via the Console or the Webhooks API — useful if you already live in the Apify Console, but extra setup if you're calling this Actor's API directly and just want a completion ping. `webhookUrl` is a plain input field: set it on the run itself and it POSTs a JSON body (`actorRunId`, `defaultDatasetId`, `finishedAt`, `pushed`, `scanned`, and — if `watchLabel` is set — `watchSeeding`/`watchNewCount`/`watchChangedCount`/`watchSkippedCount`/`baselineTruncated`/`baselineTruncatedTotal`) once the run finishes and every mark is already pushed and charged. Especially useful with `watchLabel` on a scheduled filing alert: your endpoint is told how many new marks landed without polling the dataset, and `watchSeeding: true` distinguishes "this was the free baseline run" from "your watch is live and quiet" — both report zero new marks otherwise. It's best-effort — a slow or failing webhook only logs a warning, it never fails the run, changes the result set, or affects billing.

## Use cases
- **Brand clearance screening** — check a proposed name against 70+ offices before filing, in one search instead of dozens. Use `matchMode: "startsWithPrefix"` for this: it is the only mode that answers "is there already a mark whose name *begins* with mine", including inside a longer word (`COFFEE` for `"coff"`), without burying it in mid-name noise. Use `contains` if you want the widest net and will sift it yourself; see the `matchMode` FAQ for why `startsWith` is a whole-word filter, not a prefix one.
- **Opposition watch** — set `watchLabel` and re-run a competitor's or your own portfolio's search on a schedule to get alerted only on newly-filed marks matching it, instead of re-downloading and re-paying for the same result set every run. `oppositionPeriodStart`/`oppositionDeadline` tell you the exact window still open on each newly-filed mark. Add `watchChanges` to also get alerted the moment a watched mark's own status moves — into `Registered` (opposition window closing), or into `Ended`/`Expired` — instead of only on brand-new filings. Leave the `statuses` filter empty on this run — filtering by status is exactly what makes a status *change* undetectable, see "don't filter on the field you're watching" in the FAQ.
- **Renewal tracking** — filter your own portfolio search to `Registered` marks and sort by `expirationDate` to see which registrations need renewing next, per office.
- **Competitor portfolio mapping** — pull every mark an applicant holds by searching their brand name and reviewing `applicantNames`/`office`/`niceClasses` across results.

## Pricing
`result` — charged per returned trademark record, from $0.002/result. The run start is free, and watch-mode baseline runs return and charge nothing.

**Niche size verified live 2026-10-30; the per-listing prices in this paragraph verified live 2026-10-06.** The same 20-term Store sweep now sees **2,401** distinct listings and **154** that mention trademarks somewhere in their copy, up from 145 on 2026-10-23 and from the 114-of-543 reading this paragraph carried from 2026-10-06 to 2026-10-30; the older figures are corrected here rather than quietly re-dated, and the sweeps dated below record what each re-count found. Of the 2026-10-06 reading's 114, **89** were genuinely trademark products (the rest are unrelated scrapers — ZipRecruiter, Redfin, ImportYeti, TripAdvisor and the like — whose descriptions merely carry "all trademarks are the property of their owners" boilerplate). The in-effect price was pulled live for every one of the 89 — not just the leader, and not only the ones that happen to search the same register we do. Both figures grew on the 2026-10-06 re-sweep (from 108 mentions / 84 real trademark products on 2026-10-04); the earlier counts stood in this section until then and are corrected here rather than quietly re-dated. Previous re-checks corrected three statements (`parseforge`'s dearest-per-row superlative, `sian.agency`'s tier breakdown, and `automation-lab`'s FREE rate), added three multi-office listings that had never been named, and pinned the exact filed price changes at `jungle_synthesizer/euipo-trademark-scraper` and both `dev00` listings.

**The multi-office listings**, which is the only group doing the same job as this Actor (all prices below verified live 2026-10-03). `scrapers_lat/tmview-global-trademarks-scraper` is the closest structural match at 77 offices and tiers $0.015 (FREE) down to $0.012 (DIAMOND), 6–7.5× ours, in exchange for goods-and-services wording, opposition and register-event detail we do not return. `dltik` (148 users, `dltik/euipo-trademarks-scraper`, the busiest TMview-based listing) charges $0.01/result plus a $0.00005 start — 5× ours — and bills separately for detail enrichment ($0.01/mark), applicant→company resolution ($0.005) and AI brand-clearance scoring ($0.02), three things it does that this Actor does not; its US sibling `dltik/uspto-trademarks-scraper` has the same shape against one register. `parseforge/tmview-trademarks-scraper` (27 users) is the second-busiest TMview-based listing and the dearest of the TMview-based listings per row: $0.021/result (FREE) down to $0.019 (DIAMOND) **plus** a tiered $0.02–$0.0178 start fee, so a 50-row search costs about $1.07 there against $0.10 here. (An earlier version of this sentence called it "the dearest way to buy this data per row" outright. That was wrong and is corrected: `nexgendata/euipo-esearch-trademarks` at $0.10/trademark and `nexgendata/trademark-patent-search-api` at $0.05–$0.15/record, both named below, are dearer per row than parseforge — the superlative only ever held within the TMview-based group.) `hanamira` (81 users, `hanamira/patent-trademark-search`) is the single biggest trademark listing on the Store but mixes patents and trademarks rather than searching a register, and charges $0.004/result plus start — double our rate. `zinin/trademark-multiregistry` spans several registries at $0.01 (FREE) to $0.008 plus a $0.005 start, 4–5× ours. `jdepablos/trademark-watch-tmview` prices watching rather than rows, and its scheduled increase took effect **2026-10-01**: $0.035 per watched term plus $0.10 per match found, up from $0.02 per term. Our `watchLabel` mode charges only the $0.002 row rate, and only on marks you have not already been given.

Three further multi-office listings, none of them named here before the 2026-10-03 sweep and all dearer than us (prices verified live 2026-10-03). `s-r/trademark-search` is the closest never-named structural match — one row per mark from USPTO, TMview, Madrid and IP Australia — at a flat $0.006 per trademark with no start fee, 3× ours, in exchange for goods-and-services text and per-source status flags. `everyotherfriday/trademark-search` reads TMview and USPTO directly for US/EU/UK coverage at $0.008 per returned record, no start fee, 4× ours. `nexgendata/trademark-patent-search-api` is the widest listing in the niche by source count — you pick one of 18 registries per run (USPTO, EUIPO, WIPO PATENTSCOPE, UK IPO, CNIPA, JPO, KIPO, India, HK and more) — but bills per record by source, $0.05 for a USPTO trademark and $0.10 for an EUIPO one (up to $0.15 for some patent sources), plus a $0.005 start: 25–50× our row rate for trademark data, and one source per run rather than all of them in one result set.

**The single-register listings** are cheaper to build and mostly dearer to buy; none of them reaches past one office, where this Actor searches 70+ in a single call (verified live 2026-10-03). US-only: `alizarin_refrigerator-owner/uspto-api---patent-trademark-data` (64 users) charges a $0.10 start fee plus $0.01 per trademark search or detail lookup — and, which the previous version of this section did not say, only $0.00001 per returned row, so counting its $0.10 start and one $0.01 search its total ($0.11 + $0.00001/row) drops below ours ($0.002/row, no start) above about 55 rows in a single run; `dev00/uspto-trademark-api` (106 users, count re-verified live 2026-10-06) is $0.003 per batch check today, and its filed change for **2026-10-14** turns that flat price into a tiered one — $0.10 on FREE, $0.003 unchanged on BRONZE and above — so from that date it is 50× our row rate for anyone on the free plan and unchanged for everyone else; its sibling `dev00/uspto-trademark-text-check-api` ($0.005 per text check) carries the identical change on the same date; `fortuitous_pirate/uspto-trademark-scraper` (57 users) is $0.00279/result plus a $0.001 start, about 1.4× ours; `nexgendata/uspto-trademark-search` (49 users) is $0.05/record and $0.05 per watch check, 25× ours; `memo23/uspto-trademark-scraper` (47 users, up from 43, re-verified live 2026-10-29) is $0.007/record plus a $0.005 start, price unchanged; `scrapesage/uspto-trademark-scraper` is $0.004/record with no start fee, plus brand-owner ($0.004) and IP-attorney ($0.005) lead enrichment we do not offer; `sheshinmcfly/uspto-trademark-checker` and `glistening_film/uspto-trademark-lookup` both match our $0.002 exactly, the first adding a $0.00005 start and the second nothing at all. EU-only: `nexgendata/euipo-esearch-trademarks` (43 users) is $0.10/trademark plus a $0.005 start and $0.05 per watch check — 50× our row rate; `ryanclinton/euipo-trademark-search` matches our $0.002/record exactly, adding a $0.00005 start.

The previous version of this section called that `nexgendata` listing "the dearest listing in the whole niche". On the full niche set **that is false** and is withdrawn (all prices in this paragraph verified 2026-10-03): `nexgenwatch/trademark-gazette-issue-digest` and `nexgenwatch/trademark-portfolio-report` charge **$15 per record** on FREE, tiering down to $10.05, and `ryanclinton/brand-protection-monitor` ($0.50/brand), `brasildados/cnpj-trademarks-patents` ($0.30 per tax ID), `irreplaceable_chevrotain/trademark-clearance-mcp` ($0.25/call) and `aurorasys/spain-trademark-watch-oepm` (up to $2.50 for a viability report) all price above it. Those are report and alerting products rather than per-row register searches, which is why a row-rate comparison with them is not very meaningful — but "dearest in the niche" was still the wrong thing to say, so it is gone rather than re-scoped.

We are **not** the cheapest listing here, and would rather say so than hide it (also verified live 2026-10-06). Seven listings undercut us, and here is the full set. The bookkeeping, re-derived mechanically on 2026-10-06 rather than carried forward: of the niche's 89 trademark listings, this section named **58** by name going into that sweep, and the in-effect price of all **31** it did not was pulled live, every charge event and every plan tier. Not one of the 31 undercuts our $0.002 per returned trademark, so the set below is still complete. (An earlier version of this paragraph said "37 of 84 … all 47 that it does not". Those were cycle-1212 figures and the niche has grown since; the three numbers are re-counted here, not re-dated.) The 31 are all small listings (1–2 users), and the closest any of them comes is `unrivaled_fortress/wipo-global-trademark-brand-watch` at $0.0026 per row on GOLD and above — about 1.3× ours — followed by `axiomworks/uspto-trademark-search-scraper` at $0.002975 on GOLD and above. Among the listings this section *does* name, the closest non-undercutters are `sian.agency/uspto-trademark-search-status-scraper` at $0.00234 per status record and `silentflow/uspto-scraper` at $0.002507.

Eight listings in the previously-unnamed set do advertise a charge event below $0.002 (every price in this paragraph verified live 2026-10-04), and **every one of them is an Actor-start fee rather than a row price** — typically $0.00005 to $0.001 to begin a run, after which the actual data event costs $0.003 or more (for example `khadinakbar/uspto-trademark-batch-search` pairs a $0.00005 start with $0.005 per trademark result, and `nexgendata/india-trademark-search` pairs the same $0.00005 start with $0.05 per record). Reading the cheapest event on a listing as its row rate is the single easiest way to publish a competitor comparison that flatters us, so we price the data event and say so. The same applies to three listings this section does name: `luminar/uspto-trademark-monitor` bills $0.000475 for an *unchanged*-target watch check (its actual record price is $0.01425), `technicaldost/uspto-trademark-status-monitor` $0.0005 for a single known-serial status check (records are $0.003), and `zentrafoundry/uspto-trademark-patent-watcher` $0.0001 for internal bookkeeping events (a matched IP record is $0.01).

**Cheaper than us from the first row, in exchange for covering exactly one office each.** `jungle_synthesizer/dpma-trademark-patent-de-scraper` is $0.0004/record (FREE) down to $0.00032 (GOLD+) with a $0.0001 start — five to six times cheaper than our $0.002, for the German DPMA register only. `getascraper/dpma-trademark-register-scraper` is cheaper still on the same register, $0.00035 (FREE) to $0.00026 (GOLD+) with no start fee at all. `jungle_synthesizer/ip-australia-trademark-scraper` is $0.001 to $0.0008 plus a $0.0001 start, half our rate, for IP Australia only. If Germany or Australia alone is all you need, those are the cheaper buy and we will not pretend otherwise; what you pay us for is `DE` or `AU` arriving in the same result set as `US`, `EM`, `GB`, `JP`, `CN` and 65 more from a single call.

**Eight more single/multi-office listings, never named before, all confirmed dearer at every tier (verified live 2026-10-04, cycle 1239).** A fresh 20-term sweep found 536 distinct listings (up from 526), 110 of which mention trademarks (up from 108) — none of the drift moved any verdict below. USPTO-only: `foxlabs/uspto-trademark-leads` is $0.006/result plus a $0.00005 start, 3× ours, and adds contact-enrichment on new filings we do not do; `parseforge/uspto-trademark-scraper` (assignment records only — a narrower data type than a full registration search) tiers $0.0065 (FREE) to $0.006 (GOLD+) plus a $0.02–$0.0178 start, 3× ours; `crawlerbros/uspto-trademark-search-scraper` tiers $0.005 (FREE) to $0.003 (GOLD+) plus a $0.005 start, 1.5–2.5× ours; `abcdemprendes/uspto-trademark-search-ai` does not price by row at all — $0.05 per basic search plus a $0.005 start, then up to $0.48 per Claude-powered du Pont or TTAB analysis event, so it is dearer than us from the first search regardless of row count. `nexgendata/ttab-trademark-opposition-tracker` is a different data type (TTAB inter-partes disputes, not registration search) at $0.10/proceeding plus a $0.005 start — 50× our row rate. Single-office, not US: `nexgendata/uk-trademark-search` (UKIPO only) is $0.05/record plus a $0.005 start, 25× ours. International: `scrapers_lat/wipo-madrid-trademarks-scraper` tiers $0.015 (FREE) to $0.01275 (GOLD+), 6–7.5× ours; `parseforge/ip-australia-trademarks-scraper` (a second, never-named IP Australia-only listing alongside the already-named `jungle_synthesizer` one) tiers $0.005 (FREE) to $0.00375 (GOLD+), 1.9–2.5× ours. None of these eight undercuts us at any tier or volume.

**The 1–2-user tail, finished (verified live 2026-10-05, cycle 1278).** All 40 remaining unnamed listings that mention trademarks at 1–2 users were live-priced, not just skimmed by title — the USPTO/EUIPO/Canada-CIPO/Peru/Brazil/Argentina/Japan/Korea/Hong-Kong/Spain watch, status, TTAB, MCP and IP-intelligence variants this section had deferred since cycle 1239. None of them undercuts our $0.002/result: the closest is `noahadler/euipo-uspto-trademark-search`, which prices its row at exactly $0.002 but adds a $0.00005 Actor-start fee, so it ties us at volume and is marginally dearer on a single-row run — an exact tie, not an undercutter, named here so it is not mistaken for one later. Every other listing in the tail is a watch/alert product billing per delta or per tool-call rather than per search result (`nexgenwatch`'s CIPO/USPTO gazette watches at $0.054–$0.10, `paulovitor18/inpi-trademark-watch` at $0.15–$0.75, `thequietstack`/`glistening_film`/`outstanding_vegetable`'s USPTO watches at $0.02–$0.03), a single-office search dearer than ours by 1.5×–50× (`axiomworks`, `thoob`, `recordsdata`, `ivosandoval/spain-oepm-scraper`, `scrapers_lat`'s Peru/Argentina/Canada/WIPO-Madrid/TTAB listings, `nexgendata`'s Japan/Korea/Hong-Kong listings), or a differently-shaped product entirely (`shane_reich/name-clearance-verdict` and `protocol/brand-name-ip-screener` are flat-fee clearance/screening reports against a curated seed set rather than a full-register search; `maged120/brand-username-checker` bundles social/domain checks; `nexgendata/patent-trademark-rag` converts documents to RAG chunks; `second_coming/patent-search-tool` charges a flat $0.02 per scan regardless of row count; `solidcode`/`seibs.co` bundle patents and trademarks together). Two listings in the tail turned out not to be trademark products at all once read live, despite names that say otherwise — a fresh instance of the cycle-1212/1277 lesson that a listing's scope must be confirmed from its own description, not its title: `nexgendata/patents-trademarks-ip-mcp-server` states in its own description "patents only — no trademark tools"; `zentrafoundry/uspto-trademark-patent-watcher-v2` states "Google Patents xhr for NVIDIA GPU. Not a USPTO trademark conflict watch." Neither belongs in this niche's count. No README price change results from this sweep — completeness holds, the 7-undercutter set named above is still the full set — but the deferred tail is now closed.

**Thirteen more listings, never named here before, all confirmed dearer than us at every tier (verified live 2026-10-06, cycle 1324).** The niche grew again (84 → 89 real trademark products) and the 2026-10-06 sweep re-priced the whole 31-listing un-named remainder; these are the ones worth naming. Full-register US searches: `devilscrapes/uspto-trademark-scraper` is $0.005/result — 2.5× ours — and its in-effect block also carries a **$0.20 Actor-start fee**, the dearest start fee anywhere in this niche, so a 10-row search costs about $0.25 there against $0.02 here; `scrapers_lat/uspto-trademarks-scraper` tiers $0.008 (FREE) to $0.0068 (GOLD+), 3.4–4× ours; `neuton/uspto-trademark-keyword-search` is a flat $0.025/result, 12.5× ours, and describes its own searches as "bounded"; `neverempty/uspto-trademark-search-monitor` is the closest in shape — a real USPTO text/owner/class search with a monitoring mode — at $0.008 (FREE) to $0.005 (GOLD+) per returned trademark, 2.5–4× ours, plus $0.0005 per monitoring check (that $0.0005 is a check, not a row price, so it is not an undercut). EU: `crawlerbros/euipo-trademark-design-search-scraper` covers EUTM plus registered Community designs at $0.005 (FREE) to $0.003 (GOLD+) plus a $0.005 start, 1.5–2.5× ours. Watch and feed products, which bill per delta rather than per search result: `unrivaled_fortress/wipo-global-trademark-brand-watch` (newly registered WIPO-international and US filings) at $0.004 (FREE) to $0.0026 (GOLD+) plus a $0.0001 start — the closest row rate in the un-named set at 1.3× ours, but a new-filings feed rather than a register search; `accountable_eel/trademark-filing-watch` (USPTO **and** EUIPO new applications by Nice class) at $0.01 (FREE) to $0.005 (GOLD+) per matched filing plus a $0.00005 start; `automation_studio/uspto-trademark-radar` at $0.005 (FREE) to $0.003 (GOLD+) plus a $0.001 start; `friendlyapi/uspto-trademark-scraper` sells the USPTO daily firehose keyed by serial at $0.005 (FREE) to $0.003 (GOLD+) per serial checked and $0.02–$0.012 per 100 delivered events; `nexgendata/trademark-conflict-watch` bills $0.02 per watched item checked plus $0.10 per watch run and $0.10 per conflict match; `stefano_seggio/kipris-patent-trademark-status-monitor` (Korea KIPRIS) is $0.02 per new filing or status change and $0.008 per non-status field update. Different data types: `openrows/us-trademark-status` is a TSDR status lookup against serial or registration numbers you already hold — $0.006 per mark, 3× ours, and not a search at all; `nexgenwatch/trademark-dispute-mcp` answers TTAB and Canadian opposition questions as an MCP tool at $0.05 per tool call plus a $0.05 start. Seven of the 31 advertise a charge event below $0.002 and **not one of them is a row price** — six are Actor-start fees ($0.00005 to $0.001 at `unrivaled_fortress`, `accountable_eel`, `thequietstack`, `stefano_seggio`, `nexgendata/hk-trademark-search` and `automation_studio`) and the seventh is `neverempty`'s $0.0005 monitoring check. Reading the cheapest event on a listing as its row rate is the easiest way to publish a comparison that flatters us, so the data event is what gets priced here.

**The full unnamed tail re-priced on 2026-10-07 (cycle 1360): the listings that undercut our $0.002
are, with one exception, not trademark products at all.** A fresh 20-term sweep saw 546 distinct
listings, 114 of which mention trademarks anywhere in their copy (name/title-only matching returns
88 — the gap is description boilerplate, see below). **41** of the 114 are not named in this section
by full `owner/slug` handle, and the in-effect price of all 41 was pulled live and scored tier by
tier, every charge event included (verified live 2026-10-07). Seven of the 41 price a row below our
$0.002 on some plan tier, and **six of those seven are not trademark tools in any sense** — they
match this niche only because their description carries the standard "all trademarks belong to their
respective owners" affiliation disclaimer: `haketa/ziprecruiter-scraper` (job listings),
`haketa/healthgrades-scraper` (doctor directory), `logiover/tripadvisor-scraper`,
`lentic_clockss/instacart-scraper` and `getascraper/teamblind-reviews-scraper` (employee reviews) all
tier down to $0.0015–$0.00165 on the upper plans, and `haketa/redfin-scraper` plus
`scrapesage/cargurus-scraper` tie our $0.002 flat. Each was read from its own live description rather
than its title, the standing rule in this section.

The seventh, `crawlerbros/importyeti-scraper`, was a genuine partial undercut at 88 users — half our
rate on GOLD/PLATINUM/DIAMOND for the `trademarks` field among its ImportYeti US import/export records
— but **is gone from the Store as of 2026-10-09** (`GET /v2/acts/crawlerbros~importyeti-scraper` now
404s, a removal rather than a rename, confirmed directly against the API). A fresh resweep for a
replacement at those top three tiers is still owed; this retracts the specific undercutter without
claiming nothing beats us there. (It could never search a register by word mark, owner, Nice class or
serial number in any office, which is the job this Actor does — that gap stands regardless of who
occupies the price slot.)

Three real trademark products in the tail are named here for the first time, all dearer than us at
every tier (verified live 2026-10-07). `lexis-solutions/data-inpi-fr-scraper` reads the French INPI
register — companies, trademarks, patents and designs — at $0.009 (FREE) tapering to $0.0064 (GOLD+),
3.2–4.5× ours; **France is a new office for this comparison**, which until now covered INPI only via
`paulovitor18`'s Brazilian watch. `deepmine/meta-brand-mention-monitor` sells trademark watching over
the Meta Ads Library rather than a register, $0.005 (FREE) to $0.0035 (GOLD+), and tracks brand
mentions in ads, not filings. `nexgendata/legal-mcp-server` exposes case law, court dockets, FINRA
BrokerCheck and trademark data as ten MCP tools at $0.02 per tool call — 10× our row rate. One
listing the pricer declined to score was resolved by hand: `outstanding_vegetable/uspto-trademark-watch`
pairs a conventionally-named `apify-actor-start` event ($0.005) with a $0.02 alert event, but its
start event is not flagged one-time, so two events read as recurring with no primary declared. Read
live it is $0.005 to start plus $0.02 per alert, 10× our row rate — consistent with the $0.02–$0.03
quoted for it above. **Bottom line unchanged by this sweep:** no listing that actually searches a
trademark register undercuts our flat $0.002/result at any plan tier beyond the set already named.

**The full unnamed tail re-priced again on 2026-10-08 (cycle 1398): one genuine new undercutter.**
The niche grew again — a fresh 20-term sweep saw 548 distinct listings, 117 of which mention
trademarks (up from 114 at cycle 1360) — and this section already named 86 of them going in. The
in-effect price of the remaining 31 was pulled live via the shared `bin/_unit_price.py` helper
(also repointed this cycle, closing this Actor's slice of `0-TODO-h1396-repoint-batch-pricers`),
every charge event and plan tier included. One is a genuine undercut and is disclosed here:
`thriftykiwi/trademark-search-aggregator` (2 users) reads the USPTO trademark search and EUIPO
TMview together — status, owner, Nice classes and the official record link — for a flat $0.001 per
returned mark with no start fee, half our $0.002 at every tier. It is a real substitute if USPTO
and TMview-covered EU offices are all you need; what you pay us for is those two plus 68 more
offices in the same call.

Eight more real trademark products are named here for the first time, all confirmed dearer at
every tier (verified live 2026-10-08): three watch feeds from `nexgenwatch` — `canada-cipo-trademark-decision-watch` ($0.1
FREE to $0.067 GOLD+, plus a $0.02 start), `cipo-trademark-watch` and `uspto-trademark-watch`
(both $0.08 FREE to $0.0536 GOLD+, plus a $0.02 start) — 27–50× ours; `thoob/uspto-trademark-feed`
($0.004 flat, no start, 2× ours, with a what-changed-since-last-run mode); `recordsdata/uspto-
trademark-status-scraper` ($0.02 FREE to $0.0175 GOLD+, no start, 8.75–10× ours); `topapi/uspto-
trademark-scraper` ($0.0028 flat, no start, 1.4× ours); and two listings that price patents and
trademarks the same regardless of office, `seibs.co/uspto-patent-intel` ($0.004 flat, no start, 2×
ours) and `solidcode/uspto-patent-trademark-scraper` ($0.0048 FREE to $0.004 GOLD+, plus a $0.005
start, 2–2.4× ours). `scrapers_lat` alone adds five never-named single-register listings, all
dearer and none with a start fee: `indecopi-trademarks-scraper` (Peru) and `euipo-trademarks-
scraper` both tier $0.015 to $0.01275; `canada-cipo-ip-scraper` and `inpi-argentina-trademarks-
scraper` tier the same $0.015 to $0.01275; `uspto-ttab-proceedings-scraper` (TTAB disputes, not a
registration search) tiers $0.0165 to $0.015 — 6.4–8.25× our rate across the five. `nexgendata/
japan-jpo-jplatpat-patents-trademarks` and `nexgendata/korea-kipo-kipris-plus-patents-trademarks`
each charge a flat $0.05–$0.1 per combined patent-or-trademark record plus a $0.005 start, 25–50×
ours. (`thequietstack/uspto-trademark-watch` and `glistening_film/uspto-trademark-watch`, also in
this 31, are already named by owner above at the identical $0.03 and $0.02 FREE rates quoted there
— no new disclosure needed.)

The remaining 13 of the 31 are out of scope on their own live description, not a title guess
(verified live 2026-10-08).
Three share the shape already disclosed above for `crawlerbros/importyeti-scraper`: `khadinakbar/
importyeti-scraper`, `alwaysprimedev/importyeti-scraper` and `devilscrapes/importyeti-alternative-
scraper` all carry a `trademarks` field inside US import/export trade data, not a register search.
The other ten match this niche only via disclaimer boilerplate or a trademark field buried inside
an unrelated product — `piotrv1001/ziprecruiter-jobs-scraper` and `parseforge/ziprecruiter-scraper`
(both job listings), `parseforge/sunbiz-
florida-business-scraper` and `rl1987/fl-sunbiz-mcp` (Florida business registry, trademark is one
of nine search types), `scrapesage/redfin-scraper` (real estate), `gio21/instacart-storefront-
scraper` (grocery items), `zentrafoundry/company-name-normalizer` (GLEIF legal-name lookup),
`spider_studio/tianyancha-dimension` (Chinese corporate-risk aggregator), `captainhandsome/
courtlistener-case-search` (US case law and dockets), `crawlerbros/hawaii-business-express-
scraper` (Hawaii business registry) and `ivosandoval/datamon-premium` (Spanish public-data
aggregator, OEPM trademarks is one of six sources) — none of them searches a trademark register.
(`parseforge/ziprecruiter-scraper`, 2026-10-09 sweep, same disclaimer-boilerplate shape as
`piotrv1001`'s listing and no relation to `parseforge`'s genuine trademark products named above.)
**Bottom line: the undercutter set grows by exactly one.** `thriftykiwi` joins `crawlerbros/
importyeti-scraper` (partial, GOLD+ and above only) as the niche's only two undercuts; every
full-register competitor still prices at or above our $0.002/result. (That last clause held
on 2026-10-09 and **no longer does** — `scrapewise/uspto-trademark-scraper`, found in the
2026-10-16 sweep below, is a full-register search priced under us on every paid plan tier.
The sentence is left standing as the dated finding it was, with the correction attached
here rather than silently rewritten.)

**The first full-register undercutter, found on a corrected re-sweep (2026-10-16, cycle 1784).**
Every niche count in the paragraphs above was produced by a Store sweep that silently asked for
only the first 100 results per search term — a tool bug fixed on 2026-10-15, which means those
sweeps could only ever see a fraction of the matchable Store and their "the set below is still
complete" verdicts were never completeness proofs. Re-swept at the corrected depth: **2261
distinct listings seen** across the same 20 queries (not 543) and **126 of them mention
trademarks** (not 114). Thirteen of the 126 had never been named here. All thirteen were
live-priced — every charge event, every plan tier, read from the listing rather than inferred
from its title — and every description was read in full before a price was trusted. Two of the
thirteen undercut us:

- `scrapewise/uspto-trademark-scraper` is a **genuine full-register competitor priced below us**
  (verified live 2026-10-16), and the first one this niche has produced: a real USPTO search by
  mark, owner, goods, serial or
  registration number returning status, classes, dates, owners, attorney and image, with name
  availability checks, Nice class suggestions, renewal deadlines and new-filing monitoring on top.
  One charge event, **no start fee**, tiered $0.002 (FREE — an exact tie with us) → $0.0019
  (BRONZE) → $0.0018 (SILVER) → $0.0017 (GOLD, PLATINUM and DIAMOND). So it is 5%, 10% and 15%
  under our flat rate for anyone on a paid Apify plan, at every volume, with no fee to amortise.
  What it does not do is leave the US register — this Actor searches 70+ offices in one call,
  where a buyer who needs EUIPO, UK, DE, JP or WIPO coverage would have to pair it with something
  else — and it returns no opposition window, seniority claim, Vienna codes or territories, and
  has no incremental watch mode.
- `blackfalcondata/uspto-trademark-scraper` scrapes tmsearch.uspto.gov for US records by mark,
  owner, serial or registration number, adding owner country, attorney email and TSDR prosecution
  history. Its row price is $0.00153 (flat, all plans — the "$1.53" in its own title is per 1,000
  rows), but it also charges a **$0.01 Actor-start fee**, which our $0.002 has nothing to repay.
  The two cost the same at about **22 rows** ($0.01 ÷ $0.00047); below that we are cheaper, above
  it they are, reaching roughly 24% under us at 1,000 rows. USPTO-only, like `scrapewise`.

Eight of the thirteen are dearer than us at every tier (all prices in this paragraph verified
live 2026-10-16). The one worth naming first is
`foxlabs/euipo-trademark-data` — **the closest structural match in this tail and the only other
TMview-based listing found in it**: same source, same "EUIPO + 70 national offices in one search",
and a near-identical field set (mark name, applicant, application and registration numbers,
status, filing and registration dates, Nice classes, office, mark image), at a flat $0.003 per
trademark with no start fee, 1.5× ours. It returns no opposition window, seniority claim, Vienna
codes or territories, and has no watch mode. Then `dev00/wipo-trademark-search` (WIPO Madrid and
national records) and `dev00/euipo-trademark-search` (EU marks, Community designs, BoA/CJEU case
law and visual similarity matching), both $0.10 per query on FREE dropping to $0.005 on BRONZE and
above — the same free-plan-penalty tiering `dev00`'s two USPTO listings named earlier adopted on
2026-10-14, so 2.5× ours for a paying buyer and 50× on the free plan. The remaining five are
trademark products of a different shape, all dearer: `delta_tools/trademark-clearance-checker`
($0.01 FREE → $0.008 GOLD+ per candidate name screened, plus a $0.0007 start — one research
summary per name, not a row of register data), `lone_rachis/us-trademark-status-watch` ($0.01 FREE
→ $0.008 GOLD+ per mark plus a $0.00005 start — a TSDR status lookup on serials you already hold,
with computed Section 8 and renewal deadlines), `zinin/trademark-class-overlap-review` ($0.025
FREE → $0.0175 GOLD+ per result, a class-overlap assessment rather than a search),
`vncntlabs/pod-trademark-checker` ($0.01 per listing checked — a high/medium/low risk score per
phrase for Etsy/Merch/KDP sellers) and `replay/inpi-veille-marques` ($0.03 per similarity alert on
new French INPI filings, and it runs on your own INPI credentials rather than fetching for you).

**Three of the thirteen are not trademark products at all** (verified live 2026-10-16), despite
matching the sweep, and one
of them is exactly the trap this section keeps warning about. `vncntlabs/keyword-ideas` prices its
`keyword-idea` event at **$0.002 — identical to our row rate** — and `vncntlabs/keyword-search-volume`
prices `google-volume` at $0.003; both are Google/Amazon keyword research tools for print-on-demand
sellers that happen to attach a USPTO trademark-risk flag to each keyword. Neither sells a row of
register data, so neither is a tie or a near-miss on our price — reading that $0.002 as a competing
trademark rate would have put a false equivalence in this section. `sian.agency/t-shirt-design-and-
listing-generator` ($1.05 FREE → $0.28 DIAMOND per cleared phrase, plus a $0.005 start) is a POD
artwork-and-listing generator that screens slogans against the US register as one step of a larger
job. None of the three belongs in a row-rate comparison.

**Our own price was re-read live during this sweep and is unchanged**: a single `result` event at
a flat $0.002 on every plan tier, no start fee.

**Pricing decision (2026-10-16, cycle 1786): holding flat $0.002, not tiering.** Re-verified live 2026-10-16:
`scrapewise/uspto-trademark-scraper` still 3 users as of 2026-10-25 three weeks after its
2026-09-30 launch, still USPTO-only, still no opposition window, seniority claim, Vienna codes,
territories or watch mode. That is a materially weaker signal than the one that triggered
`app-store-reviews-scraper`'s account-plan tiering in cycle 1781 — that niche had **14**
undercutters and every serious named rival already tiered by plan, so our flat rate was quietly
the dearest option industry-wide. Here there is exactly **one** full-register undercutter, it
is narrower in scope than us, and the only other listing that matches us structurally —
`foxlabs/euipo-trademark-data`, same TMview source, same 70+-office breadth — prices **above**
us at a flat $0.003 with no start fee. (**That "exactly one" count held on 2026-10-16 and is now
out of date: there are three full-register undercutters as of 2026-10-28, one of them free. The
decision to hold flat $0.002 is re-affirmed on those current facts — and the revisit conditions
restated — in the "Five-day recheck" paragraph further down; read the two together.**) A buyer who needs more than USPTO is still cheaper here
than anywhere else found in this niche; a USPTO-only buyer on a paid Apify plan saves at most
15% by switching to a 2-user listing with none of our watch mode, validation or hosted-API
coverage. Adding plan tiers here would shave margin off every buyer, on every plan, to match a
competitor whose adoption after three weeks has not moved, in exchange for closing a gap that
breadth and features already cover. Revisit if any of: `scrapewise` crosses 20 users (passes
the standing publish-a-count threshold and stops being a thin signal), `foxlabs` cuts below our
$0.002, or a second full-register undercutter appears in a future resweep.

**Resweep confirms no change (2026-10-16, cycle 1803).** A fresh 20-term sweep saw 2,268 distinct
listings (vs cycle 1784's 2,261 — the Store-search depth fix has now settled, no further
truncation jump) and 125 mention trademarks (vs 126), 101 by strict name/title match. Every one of
the 125 is already named or excluded in this section (`niche-unnamed`: 0 of 125 unnamed). Both
disclosed undercutters are unchanged at 2 users each (`scrapewise/uspto-trademark-scraper`,
`blackfalcondata/uspto-trademark-scraper`, re-verified live), so neither has crossed the 20-user
revisit threshold from the pricing decision above — still holding flat $0.002, no tiering. Our own
price re-read live and unchanged.

**New sweep finds real growth and two genuine new undercutters (2026-10-23, cycle 2139).** A fresh
20-term sweep returns **145** Store listings matching "trademark" (up from 125 at cycle 1803,
2,337 distinct listings seen, up from 2,268) — the first real growth in this niche since it
settled at the corrected-depth count. `niche-unnamed` found 21 never-named handles (17 NONE, 4
OWNER). All 17 NONE handles were live-priced via the shared `bin/_batch_price_tms3.py`; the 4
OWNER handles were hand-verified to confirm the existing rule-out/naming still covers them.

Two genuine new undercutters (both re-verified live 2026-10-25, still 2 users each, unchanged):
- `scrapersdelight/euipo-trademark-scraper` (2 users) is the **second full-breadth TMview
  competitor this niche has produced** (after `foxlabs/euipo-trademark-data`, named above at
  $0.003): its own description claims "EUIPO and 70+ offices via TMview", the same breadth this
  Actor searches. One `trademark` event, **no start fee**, flat **$0.0018/trademark** — 10%
  under our $0.002 at every tier, no crossover needed. It returns mark name, owner, status, Nice
  classes, filing/registration/expiry dates, office and record URL, but no opposition window,
  seniority claim, Vienna codes, territories or watch mode.
- `northbell/us-trademark-search` (2 users) tiers **$0.001 (FREE/BRONZE) down to $0.0008
  (GOLD+)** per trademark record, half our rate at every tier, but carries a real **$0.01
  Actor-start fee** our $0.002 has nothing to repay — the two cost the same at about **10 rows
  on FREE/BRONZE, 8 rows on GOLD+**; below that we are cheaper, above it they are. USPTO-only,
  like `scrapewise` and `blackfalcondata` (both named above).

One single-office listing, cheaper only within its own narrower scope: `scrapersdelight/uk-trademark-scraper`
(2 users) is a UK-IPO-only search at a flat **$0.0009/trademark**, no start fee — less than half
our rate, for UK coverage alone.

Two listings tie our row rate exactly but are dearer in practice once their fee is counted:
`trev0n/tmview-scraper` (2 users, ~80 offices via TMview — the closest breadth match in this
tail) ties our $0.002/mark but adds a $0.005 Actor-start fee, so it costs $0.005 more at every
volume (it also sells a separate $0.002 "full details" add-on event this Actor does not charge
for). `devilscrapes/euipo-trademark-search-scraper` (2 users, same owner as
`devilscrapes/uspto-trademark-scraper` named above) also ties $0.002/mark but repeats that
owner's **$0.20 Actor-start fee**, the dearest start fee anywhere in this niche.

One tie on price but a narrower data type: `pink_comic/uspto-trademark-assignment-search` (2
users) charges $0.002/row — an exact tie — plus a $0.0001 start, but for USPTO **assignment**
records (ownership transfers), not a registration search — the same narrower-data-type
distinction already drawn for `parseforge/uspto-trademark-scraper` above.

One AMBIGUOUS listing hand-read: `zet46/uspto-trademark-scraper` (1 user) has a single recurring
`status` event with no primary flag; read live it bills **$0.0005 per record, cheaper than our
$0.002**, but it is a TSDR status lookup **by serial or registration number you already hold**,
not a search by mark, owner or class — the same not-a-search distinction already drawn for
`openrows/us-trademark-status` above.

Remaining listings confirmed dearer or differently shaped, all read live 2026-10-23:
`magnova/uspto-trademark-search` ($0.004 FREE → $0.0028 GOLD+, USPTO-only, 1.4–2× ours);
`scrape-smith/uspto-trademark-status` ($0.004 flat, a TSDR-by-serial lookup like `zet46`, not a
search); `actor-forge/uspto-trademark-search` ($0.03/result, a phrase-clearance checker);
`glasswing/uspto-trademark-scraper` ($0.0025 FREE/BRONZE → $0.002 GOLD+, tying only on the top
three tiers, plus a $0.004 start fee our flat rate has nothing to repay, so dearer at every
volume in practice); `data-done-right/trademark-search` ($0.006 FREE → $0.0048 GOLD+, USPTO+
Australia, 2.4–3× ours); `kdhan/uspto-trademark-search` ($0.004 flat plus a $0.005 start);
`quillstone-labs/uspto-trademark-search` ($0.01 FREE → $0.003 BRONZE+); `reaperoak`'s two
listings — `uspto-trademark-checker-bulk` and `uspto-trademark-watch-new-filings` — both $0.02
FREE → $0.017 GOLD+, a phrase-checker and a new-filing-alert product, neither a register search;
`titan_coder/uspto-patent-assignment-ownership-radar` ($0.04/result, patent-and-trademark
ownership-transfer tracking, a different data type again); `zaiq/domain-hunter` ($1.49 FREE →
$1.192 GOLD+, a domain-name generator that happens to mention trademark checks, not a register
search at all).

The 4 OWNER-bucket handles were each hand-verified live 2026-10-23 to confirm the existing
rule-out still covers them, not re-counted from an old title: `getascraper/wildberries-seller-scraper`
(29 users) bills $0.00225–$0.003/row for Russian marketplace seller identity data with a
`trademark` field among nine others, the same field-not-register shape already excluded for
other `getascraper` listings; `maged120/social-username-checker` (19 users) is a 60-site
username checker with an optional US trademark check as one add-on, the same bundled-product
shape already excluded for `maged120/brand-username-checker`; `devilscrapes/euipo-trademark-search-scraper`
is the new tie-but-dearer listing named above, not a rule-out; `fetchsmith/trademark-search-scraper`
is this Actor's own Store listing.

Our own price was re-read live during this sweep and is unchanged: a single `result` event at a
flat $0.002 on every plan tier, no start fee.

**Five-day recheck finds two more undercutters and one listing the 2026-10-23 sweep missed
(all prices verified live 2026-10-28, cycle 2384).** This is a cheap one-term recheck rather than a
full multi-term audit: one `trademark scraper` Store query (97 live listings) diffed against every
handle this section names, leaving 46 unnamed, and the in-effect price of all 46 was pulled live —
every charge event, every plan tier. Most of the 46 are the usual non-register boilerplate matches
already excluded above (Crunchbase, ImportYeti, Sunbiz, Wildberries, Meta/Google ad-library and
TikTok listings whose copy merely carries a trademark notice), and the `scrapers_lat` Peru/
Argentina/Canada/TTAB/EUIPO listings, the `nexgenwatch` CIPO and USPTO watches and
`recordsdata/uspto-trademark-status-scraper` are all already ruled out or priced by owner above
and re-confirmed dearer here ($0.015–$0.0128, $0.08–$0.0536 and $0.02–$0.0175 respectively).
Four listings are genuinely new to this section:

- `rbbscrap/fast-uspto-trademark-scraper` is a **FREE** listing — `pricingModel: FREE`, no pricing
  record at all, so it advertises **no charge event of any kind** and undercuts our $0.002 from
  the first row with nothing to amortise. It is USPTO-only (wordmarks, serial and registration
  numbers, LIVE/DEAD TSDR status, Nice classes, owners, attorney leads) where this Actor searches
  70+ offices in one call, and it returns no opposition window, seniority claim, Vienna code,
  territory or watch mode. It was **created 2026-10-24**, one day after the 2026-10-23 sweep, so
  it is a new entrant rather than a miss — but it is the most aggressive price in this niche's
  history and is named first for that reason.
- `jungle_synthesizer/j-platpat-patent-crawler` searches Japan's J-PlatPat (patents, utility
  models, trademarks and designs) and tiers **$0.001 (FREE/BRONZE), $0.0009 (SILVER), $0.0008
  (GOLD+)** per record plus a $0.0001 start — half our rate or better, for the JP register alone.
  **Created 2026-10-24**, also after the last sweep. It is the third single-office undercutter from
  this owner alongside the German DPMA and IP Australia listings named above, and the same trade
  applies: cheaper if one office is all you need, dearer than one call here the moment you want
  `JP` in the same result set as `US`, `EM`, `GB`, `DE` and the rest.
- `topapi/uspto-trademark-scraper` is a **genuine miss, not a new entrant**: a full USPTO register
  search by brand, owner, goods, class or serial with a new-filings monitor, **created 2026-10-05
  and priced 2026-10-07** — both well before the 2026-10-23 sweep that did not name it. It charges
  **$0.0028 per trademark record** (1.4× ours) plus $0.0019 per TSDR detail event, so it is dearer
  than us at every tier and every volume; recorded here because a missed listing that happens to
  be dearer is still a gap in this section's completeness claim.
- `automation-lab/canadian-trademarks-database-search` is a Canada-only register search (mark,
  owner, application and registration identifiers) at a **$0.005 start plus $0.00644 (FREE)
  tiering to $0.00336 (GOLD+)** per exported trademark — dearer than us at every tier before the
  start fee is even counted. **Created 2026-10-23**, the same day as the last sweep. It is a
  different listing from the same owner's `automation-lab/euipo-tmview-trademarks-scraper` named
  below, which is the cheap-per-row, dear-per-start shape; this one is dear on both.

One listing in the 46 came back `AMBIGUOUS: 2 recurring events, no primary flag` and was
hand-read rather than dropped: `workstream/google-ads-transparency-scraper` bills $0.0015 per ad
and $0.002 per ad-detail — but it scrapes the Google Ads Transparency Center, not any trademark
register, so it leaves the niche on scope and never reaches a row-rate comparison.

**The 2026-10-16 pricing decision's revisit trigger has now fired, and the decision is
re-affirmed on current facts rather than left standing on stale ones.** That paragraph above
holds flat $0.002 partly because "here there is exactly **one** full-register undercutter" — that
sentence was true on 2026-10-16 and is **no longer true**: `scrapersdelight/euipo-trademark-scraper`
(2026-10-23) was the second, and `rbbscrap/fast-uspto-trademark-scraper` (2026-10-28) is the
third. The conclusion does not change, for a reason the original trigger did not anticipate: the
new undercutters are a **free** USPTO-only listing and a **free-to-$0.0008 JP-only** listing, and
plan tiering cannot answer either — no ladder we could publish undercuts $0.00, and shaving our
rate for every buyer on every plan to chase two single-office listings would give up margin
without closing the only gap they actually have on us, which is scope, not price. What a buyer
pays us for remains 70+ offices in one result set plus opposition windows, seniority claims,
Vienna codes, territories and watch mode. The revisit conditions are restated accordingly: tier
if a **multi-office** listing (not a single-register one) undercuts our $0.002 at any tier, if
`foxlabs/euipo-trademark-data` cuts below $0.002, or if any undercutter here crosses 20 users.

**Fresh full-cohort sweep finds one genuine new undercutter (all prices verified live 2026-10-30,
cycle 2484).** The 20-term sweep above now matches 154 listings, of which this section already
named 150 handles; the nine it had never named were pulled live — every charge event, every plan
tier, none unresolvable. Seven of the nine have an owner who appears nowhere else in this section;
the other two belong to owners named above but are **distinct Actor IDs**, so they were re-priced
under their own IDs rather than inheriting a sibling's verdict. Our own price was re-read live
before the comparison and is unchanged: one `result` event at a flat $0.002 on every plan tier, no
start fee. One of the nine undercuts us:

- `alexmorain/inpi-trademark-scraper` tiers **$0.001 (FREE), $0.00085 (BRONZE), $0.0007 (SILVER),
  $0.0005 (GOLD and above)** per mark plus a **$0.002 start fee** — half our rate on FREE and a
  quarter of it on the top three tiers. It searches France's INPI register (French marks plus the
  EU and international marks with effect in France) through INPI's own API, and its headline
  feature is paging past the 200-per-page limit that otherwise drops 30–45% of a result set. Two
  things keep it a narrow-scope undercutter rather than a replacement: it reaches one office's
  register where this Actor searches 70+ in a single call, and **it runs on the buyer's own free
  INPI account** — a credential you have to register for and keep, where nothing here needs a key.
  Its $0.002 start equals exactly one row of ours, so on FREE the two cost the same at about **2
  rows** and it is cheaper above that; on GOLD and above its start is repaid inside the first 2
  rows. It is the niche's first French-register undercutter.

Five of the nine are in scope and dearer than us at every tier. `olliolli/eu-trademark-watch` is
the closest to us by source — EUIPO and Benelux via TMview, with similar-name, phonetic and Nice-
class comparison plus opposition deadlines — at **$0.03/result plus a $0.05 start**, 15× our row
rate before the start fee; `atesen-software/trademark-phrase-risk-check` is $0.05 per phrase
checked (bulk print-on-demand phrase screening, not a register search by applicant or class), 25×
ours; `chaptersoft/trademark-watch` tiers $0.01 (FREE) to $0.008 (GOLD+) per USPTO filing or
similar-mark alert, 4–5× ours; `maliksaid/uspto-trademark-watch` is a flat $0.006 per watched
filing or opposition event, 3× ours; `barefoot_grade/uspto-trademarks-scraper` is $0.004 per mark
plus a $0.005 start, 2× ours before the start fee, and says in its own copy that it is "text
matching only; no legal clearance or similarity scoring".

Three of the nine leave the niche on scope, and the scope read was taken from each listing's own
description rather than its title — the standing cycle-1212/1277 lesson. Only one of the three is
even cheaper per unit: `ahmed_jasarevic/importyeti-scraper` tiers $0.0012 (FREE/BRONZE) to $0.0011
(GOLD+) per importer profile, below our row rate, but it sells ImportYeti US customs bill-of-lading
data in which "trademarks" is one field inside a supplier profile — not a trademark register search,
so it never reaches a row-rate comparison (the same exclusion already applied to
`crawlerbros/importyeti-scraper` above). The other two are dearer as well as out of scope:
`vncntlabs/amazon-book-tshirt-niche-analyzer` is $0.15 per analysis of Amazon KDP/merch demand, and
`parseforge/colorado-business-registry-scraper` tiers $0.0045 (FREE) to $0.0024 (DIAMOND) per
Colorado business-entity record.

**The price decision is unchanged, and the 2026-10-16 revisit trigger did not fire.** That trigger
says to tier our flat rate if a **multi-office** listing undercuts $0.002 at any tier, if
`foxlabs/euipo-trademark-data` cuts below $0.002, or if any disclosed undercutter crosses 20 users.
`alexmorain/inpi-trademark-scraper` is a single-register listing (INPI's own database, France-
centric even where it returns EU and WIPO marks), it is at the 2-user floor like every other
undercutter in this niche, and it requires a buyer credential we do not — so it is the fourth
single-scope undercutter rather than the multi-office one the trigger is watching for, and shaving
our rate fleet-wide would give up margin without closing its only real gap on us, which is scope.
Holding flat **$0.002/result, no start fee**.

**Cheaper than us once a run is big enough to amortise their start fee** (all four verified 2026-10-03). `automation-lab` (66 users as of 2026-10-25, re-verified live 2026-10-09, `automation-lab/euipo-tmview-trademarks-scraper`) charges a $0.005 start plus $0.0000355/record (FREE, down to $0.00001 on DIAMOND), so any run returning more than about 3 records costs less there — and it also offers application-date bounds and several search terms per run, which this Actor currently does not. `fetch_cat/uspto-trademarks-scraper` is the same shape against USPTO only: $0.005 start plus $0.00002875/record (FREE, to $0.000015 on GOLD+), crossing us at about 3 rows. `sian.agency/uspto-trademark-scraper` (30 users) undercuts us only on the upper plans: its record price tiers from $0.009 (FREE, 4.5× ours) through $0.003 (BRONZE) and $0.00225 (SILVER) down to $0.0015 on **GOLD, PLATINUM and DIAMOND** — an earlier version of this sentence said PLATINUM and DIAMOND only, which understated by one plan — and on those three tiers its $0.005 start is repaid at about 10 rows; on FREE, BRONZE or SILVER it costs more than we do at every volume, and its start fee is itself tiered at **$0.05 on FREE** (not the $0.005 this section used to quote flat, which is the BRONZE-and-above figure). It never leaves the US register, but it adds availability checks, class suggestions and a detail event. `jungle_synthesizer/euipo-trademark-scraper` matches our $0.002 on FREE, and its $0.10 start fee means it undercuts us only on large runs on its top tiers. Its filed price change took effect at **09:23 UTC on 2026-10-04**, and it moves against the buyer, not for them: FREE/BRONZE ($0.002), SILVER ($0.0018) and GOLD ($0.0016) are untouched, while PLATINUM went $0.0014 → $0.0016 and DIAMOND $0.0012 → $0.0016. Before that moment its DIAMOND rate of $0.0012 beat ours above roughly 125 rows; from it, the three top tiers are flattened onto one $0.0016 price and the volume at which it undercuts us moves out to about **250 rows**. Both schedules were read live from the listing on 2026-10-04 and are filed exactly as described here.

**2026-10-07 cleanup:** dropped every sub-20-user rival count from this README per the standing rule (an exact count is only published at 20+ users, since `totalUsers` churns in both directions and a one-user tick under 20 is automatically STALE at the checker's 10% tolerance) — 35 bare counts removed across the sweeps above, every price claim, scope exclusion and feature comparison left intact. Four of the 35 were decorated in shapes a plain `` `owner/slug` (N users) `` grep cannot see and were caught by reading the paragraphs: two where the count sits between a bare owner handle and the full slug (`scrapers_lat`, `jdepablos`, both of which now lead with the slug instead) and two bare-comma prose mentions (`khadinakbar/uspto-trademark-batch-search`, `nexgendata/india-trademark-search`). Where a count shared its parentheses with a scope or price note, only the count went: `unrivaled_fortress/wipo-global-trademark-brand-watch` still reads "(newly registered WIPO-international and US filings)", `accountable_eel/trademark-filing-watch` "(USPTO **and** EUIPO new applications by Nice class)", `stefano_seggio/kipris-patent-trademark-status-monitor` "(Korea KIPRIS)" and `dev00/uspto-trademark-text-check-api` "($0.005 per text check)". No superlative in this section was premised on a sub-20 count, so none needed rewording — the three that are premised on a count (`dltik/euipo-trademarks-scraper` busiest TMview-based, `parseforge/tmview-trademarks-scraper` second-busiest, `hanamira/patent-trademark-search` biggest trademark listing on the Store) all sit well above the threshold. Counts at 20 and above are untouched (`hanamira` 81, `crawlerbros/importyeti-scraper` 88, `dltik/euipo-trademarks-scraper` 73, `dev00/uspto-trademark-api` 68, `alizarin_refrigerator-owner` 64, `fortuitous_pirate` 57, `nexgendata/uspto-trademark-search` 49, `nexgendata/euipo-esearch-trademarks` 38, `sian.agency/uspto-trademark-scraper` 30, `memo23` 29, `parseforge/tmview-trademarks-scraper` 24, `automation-lab` 23), as are the sweeps' structural cohort statements about where the small competition sits (the "1–2 users" bands and the "1–2-user tail" heading), which are dated findings about a swept cohort rather than live per-listing claims. This edit only removes numbers, it does not restate any — but every count left standing was re-verified against the live Store records on 2026-10-07, and none of them is stale.

What you get from us instead: no start fee at all, a flat rate that does not depend on your Apify plan, 70+ offices in one call, per-label incremental watch mode with status-change alerts and opposition deadlines, validation that tells you when an office, Nice class or status value can never match anything, and a hosted REST API at https://fetchsmith.com for the same data.

## Notes
Only public data from the official TMview database is collected. Respect the source's terms of use when using the output. Issues or feature requests: support@fetchsmith.com. Also available as a hosted API at https://fetchsmith.com

## Related guides
- [USPTO's own trademark APIs now all require a key — the keyless answer is a different office's database](https://fetchsmith.com/blog/uspto-trademark-api-needs-a-key) — TSDR, the Open Data Portal, the old bulk-data API and the search SPA all measured live, all gated as of October 2026; TMview answers the same USPTO register with no key
- [EUIPO's own trademark API is gated too — the same federated index answers it keyless](https://fetchsmith.com/blog/euipo-trademark-api-needs-a-key) — `api.euipo.europa.eu`'s `trademark-search_110` and `design-search` products both measured live, both requiring a Client ID/Secret with no free tier; TMview (also run by EUIPO) answers the EU register with no key
- [One key-free API searches trademarks in 70+ offices — and its worst failure returns no HTTP status at all](https://fetchsmith.com/blog/tmview-trademark-search-api-no-key) — the TMview endpoint this Actor is built on: why it resets the connection instead of returning 403, why every date is anchored at midday UTC, and measured per-office fill rates for `expirationDate`/`oppositionDeadline`/`seniorityClaimed`
- [TMview's trademark search has three match modes, not one — and two of them are misnamed](https://fetchsmith.com/blog/tmview-search-criteria-undocumented-modes) — the undocumented `criteria` values (`C`/`E`/`W`) TMview's own UI never varies, verified live, plus the 2026-10-31 correction: `W` is a whole-word match at any position (not a prefix) and `E` is a plain suffix match (not word-bounded), which is why cycle 2504 added a real client-side prefix mode (`startsWithPrefix`) as the recommended one for clearance
- [Eight ways an "only new since last run" watch mode silently stops working](https://fetchsmith.com/blog/incremental-api-watch-mode-four-traps) — how this Actor's `watchLabel` mode keys its baseline on TMview's own `st13` id, and what `watchChanges` does and does not track
- [We nearly charged our own buyers twice for rows they'd already paid for](https://fetchsmith.com/blog/watch-baseline-eviction-rebilling) — a capped watch-mode baseline can silently evict old-but-current ids on a high-volume run, re-delivering (and re-billing) rows already paid for.
- [FetchSmith blog](https://fetchsmith.com/blog) — data-source guides and API notes
- See more tools like this at [fetchsmith.com/tools](https://fetchsmith.com/tools).
