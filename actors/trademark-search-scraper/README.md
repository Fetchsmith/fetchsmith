# Trademark Search Scraper — USPTO, EUIPO & 70+ Offices (TMview)

Search registered trademarks across **70+ national and regional trademark offices** — USPTO (US), EUIPO (EM), UK, DE, FR, JP, CN, WIPO (WO) and more — through the official [TMview](https://www.tmdn.org/tmview/) database. One search covers every office you select in a single run; no need to query each country's own registry separately.

## What it does
- Sends your search term to TMview's public search API and returns matching trademarks as structured JSON, one row per mark.
- Filter by office (country/region), Nice classification class, and trademark status (TMview's four values: `Registered`, `Filed`, `Ended`, `Expired`).
- Pay per result: you are charged only for rows actually returned. HTTP-only (no browser), so runs are fast and cheap.

## Input
| Field | Type | Description |
|---|---|---|
| `searchTerm` | string | Word or brand to search for (contains-match). Default `"coffee"`. |
| `offices` | array | Two-letter office codes, e.g. `US` (USPTO), `EM` (EUIPO), `GB`, `DE`, `FR`, `JP`, `CN`, `WO` (WIPO). Case-insensitive — TMview itself matches these case-sensitively, so a lowercase or mixed-case code (e.g. `us`, `De`) is corrected for you automatically. Leave empty to search all 70+ offices. |
| `niceClasses` | array | Restrict to Nice classification classes, e.g. `"25"` (clothing), `"9"` (software). The Nice Classification has 45 classes (1-34 goods, 35-45 services); zero-padded forms like `"09"` work too. A value outside 1-45 matches no trademark at all, so the run warns you rather than silently returning nothing. Leave empty for all classes. |
| `statuses` | array | Restrict to statuses. TMview recognises exactly four: `Registered`, `Filed`, `Ended`, `Expired`. A differently-cased match (e.g. `registered`) is corrected for you automatically; a value that isn't one of the four at all (e.g. `Opposed`, `Pending`, `Withdrawn` — TMview has no such statuses) matches nothing — the run warns and says so in its status message rather than silently returning an empty dataset. Leave empty for all. |
| `maxResults` | integer | Stop after this many trademarks (default 50, max 5000). |
| `watchLabel` | string | Optional watch-mode label. The first run under a label seeds a baseline (0 rows returned, 0 charged); every later run on the same label + search returns and charges only marks not already delivered — a scheduled "alert me on new filings" feed instead of the same full result set every time. Leave unset for a plain, repeatable search. |
| `watchChanges` | boolean | Optional, requires `watchLabel`. Also re-deliver a mark you already have if its `status` changed since you last saw it (e.g. `Filed` → `Registered`) instead of only ever reporting brand-new filings. Default `false` — see FAQ. |
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

**Why are `viennaCodes` and `markImageUrl` empty on some rows?**
`viennaCodes` (figurative-element classification) only exists for `trademarkType: "Figurative"` marks — a plain word or stylized-character mark has no image elements to classify, so it's correctly empty. `markImageUrl`/`detailImageUrl` are populated for most records regardless of type (TMview generates a thumbnail URL per record), but a handful of older or office-specific entries omit it upstream — treat a `null` there as "no image on file at the source office," not a bug.

**Why does the same brand appear more than once?**
Trademarks are filed per office and per class. A global brand typically holds a separate registration in each office it operates in, and sometimes multiple classes within one office — each is a distinct legal record with its own `id`.

**Does this replace a formal trademark clearance search?**
No. This is a fast screening tool over TMview's public index. For legal clearance opinions or freedom-to-operate analysis, consult a trademark attorney or the offices' own certified search tools.

**How does `watchLabel` decide what's "new"?**
It keys a baseline by `st13` (the stable per-record id) against the exact combination of `searchTerm`/`offices`/`niceClasses`/`statuses` you pass — change any of those and the label starts a fresh baseline. Plain `watchLabel` tracks new-to-the-baseline marks (e.g. a fresh filing that now matches your search); set `watchChanges: true` to also catch a status move on a mark you already have.

**What does `watchChanges` add, and does it cost extra?**
No extra fee — a changed mark is billed at the same per-row price as a new one. Plain `watchLabel` stays silent forever about a mark it already delivered, even once its `status` moves from `Filed` to `Registered`, or into `Ended`/`Expired` — exactly the moment an opposition or renewal watch cares about most. Set `watchChanges: true` and each run also compares every already-delivered mark's `status` against what it looked like last time; if it moved, the row is re-delivered tagged with `_watchChangeType: ["status"]` and `_watchPrevious: { "status": "<old value>" }`. Off by default so existing watch labels keep their current behaviour; a label created before this shipped just starts detecting status drift from its next run onward, not an artificial backlog of every status move since the baseline was first seeded.

**Baseline size cap.** The recorded baseline holds at most 20,000 mark ids per label; once a label's cumulative baseline grows past that, the oldest ids are dropped to bound the record's size. A dropped id is treated as "new" again on a later run and re-charged, even though you already paid for it. This only bites a label with a very high cumulative volume of matches over many runs — narrowing the search (tighter `searchTerm`, fewer `offices`, specific `niceClasses`/`statuses`) keeps a baseline well under the cap. A run that actually drops ids says so explicitly in its log and status message, and reports the exact counts as `baselineTruncated`/`baselineTruncatedTotal` in the `webhookUrl` payload.

**Why are `expirationDate`, `oppositionPeriodStart`, `oppositionDeadline` and `seniorityClaimed` null on some rows?**
Not every office publishes every date through TMview, and availability is a property of the **office**, not of the record. Measured 2026-09-24 on 50 rows per office for the same search: `expirationDate` was present on 49/50 GB rows and 30/50 EM rows but **0/50 US and 0/50 DE** rows; `seniorityClaimed` on 50/50 GB and DE but 0/50 US; `oppositionDeadline` on 47/50 EM and 0/50 US. So a US record rarely carries `expirationDate` while a UK or EU record almost always does, and `oppositionDeadline` only exists once a mark has actually passed through publication (an application still pending examination has no opposition window yet). `seniorityClaimed` is `null` when the office doesn't expose the field at all, and `false`/`true` when it does. Treat `null` as "not published for this office/record," not a data error.

**How is `webhookUrl` different from Apify's own platform webhooks?**
Apify's platform webhooks are configured separately per Task/Actor via the Console or the Webhooks API — useful if you already live in the Apify Console, but extra setup if you're calling this Actor's API directly and just want a completion ping. `webhookUrl` is a plain input field: set it on the run itself and it POSTs a JSON body (`actorRunId`, `defaultDatasetId`, `finishedAt`, `pushed`, `scanned`, and — if `watchLabel` is set — `watchSeeding`/`watchNewCount`/`watchChangedCount`/`watchSkippedCount`/`baselineTruncated`/`baselineTruncatedTotal`) once the run finishes and every mark is already pushed and charged. Especially useful with `watchLabel` on a scheduled filing alert: your endpoint is told how many new marks landed without polling the dataset, and `watchSeeding: true` distinguishes "this was the free baseline run" from "your watch is live and quiet" — both report zero new marks otherwise. It's best-effort — a slow or failing webhook only logs a warning, it never fails the run, changes the result set, or affects billing.

## Use cases
- **Brand clearance screening** — check a proposed name against 70+ offices before filing, in one search instead of dozens.
- **Opposition watch** — set `watchLabel` and re-run a competitor's or your own portfolio's search on a schedule to get alerted only on newly-filed marks matching it, instead of re-downloading and re-paying for the same result set every run. `oppositionPeriodStart`/`oppositionDeadline` tell you the exact window still open on each newly-filed mark. Add `watchChanges` to also get alerted the moment a watched mark's own status moves — into `Registered` (opposition window closing), or into `Ended`/`Expired` — instead of only on brand-new filings.
- **Renewal tracking** — filter your own portfolio search to `Registered` marks and sort by `expirationDate` to see which registrations need renewing next, per office.
- **Competitor portfolio mapping** — pull every mark an applicant holds by searching their brand name and reviewing `applicantNames`/`office`/`niceClasses` across results.

## Pricing
`result` — charged per returned trademark record, from $0.002/result. The run start is free, and watch-mode baseline runs return and charge nothing.

**Verified live 2026-09-30** against every trademark listing on the Store with real traction, not just the leader. The two biggest by users both price above us: `hanamira` (81 users, `hanamira/patent-trademark-search`, patents and trademarks mixed rather than a register search) charges $0.004/result plus a $0.00005 start fee — double our rate; `dltik` (72 users, `dltik/euipo-trademarks-scraper`, the busiest TMview-based listing) charges $0.01/result plus start — 5× ours, and bills separately for detail enrichment ($0.01/mark), applicant→company resolution ($0.005) and AI brand-clearance scoring ($0.02), three things it does that this Actor does not. The two USPTO-only listings are `dev00` (57 users, `dev00/uspto-trademark-api`, $0.003 per batch check) and `nexgendata` (49 users, `nexgendata/uspto-trademark-search`, $0.05/record and $0.05 per watch check — 25× our rate); neither reaches beyond the US register, where this Actor searches 70+ offices in one call. `scrapers_lat` (8 users, `scrapers_lat/tmview-global-trademarks-scraper`) is the closest structural match at 77 offices and tiers $0.015 (FREE) down to $0.012 (DIAMOND), 6–7.5× ours, in exchange for goods-and-services wording, opposition and register-event detail we do not return. `jdepablos` (14 users, `jdepablos/trademark-watch-tmview`) prices watching rather than rows: $0.02 per watched term in effect today, rising to $0.035 per term plus $0.10 per match under a price change it has already scheduled for 2026-10-01; our `watchLabel` mode charges only the $0.002 row rate on marks you have not already been given.

We are **not** the cheapest listing here, and would rather say so than hide it (also verified live 2026-09-30): `automation-lab` (19 users, `automation-lab/euipo-tmview-trademarks-scraper`) charges a $0.005 Actor-start fee plus $0.0000354/record on the FREE tier (down to $0.00001 on DIAMOND), so any run returning more than about 3 records costs less there than here — and it also offers application-date bounds and several search terms per run, which this Actor currently does not. What you get from us instead: no start fee at all, per-label incremental watch mode with status-change alerts and opposition deadlines, validation that tells you when a Nice class or status value can never match anything, and a hosted REST API at https://fetchsmith.com for the same data.

## Notes
Only public data from the official TMview database is collected. Respect the source's terms of use when using the output. Issues or feature requests: support@fetchsmith.com. Also available as a hosted API at https://fetchsmith.com

## Related guides
- [One key-free API searches trademarks in 70+ offices — and its worst failure returns no HTTP status at all](https://fetchsmith.com/blog/tmview-trademark-search-api-no-key) — the TMview endpoint this Actor is built on: why it resets the connection instead of returning 403, why every date is anchored at midday UTC, and measured per-office fill rates for `expirationDate`/`oppositionDeadline`/`seniorityClaimed`
- [Eight ways an "only new since last run" watch mode silently stops working](https://fetchsmith.com/blog/incremental-api-watch-mode-four-traps) — how this Actor's `watchLabel` mode keys its baseline on TMview's own `st13` id, and what `watchChanges` does and does not track
- [We nearly charged our own buyers twice for rows they'd already paid for](https://fetchsmith.com/blog/watch-baseline-eviction-rebilling) — a capped watch-mode baseline can silently evict old-but-current ids on a high-volume run, re-delivering (and re-billing) rows already paid for.
- [FetchSmith blog](https://fetchsmith.com/blog) — data-source guides and API notes
- See more tools like this at [fetchsmith.com/tools](https://fetchsmith.com/tools).
