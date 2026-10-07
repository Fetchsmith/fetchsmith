# Federal Register – Proposed Rules Scraper & Public Inspection

Pulls US **Federal Register** documents — final rules, proposed rules, notices and presidential documents — from the Federal Register's own official public API (federalregister.gov, run by NARA and the GPO) and returns them as one flat, typed dataset.

No API key, no login, no proxy. Public government data only.

## What you get

37 flat fields per document, including the ones most Federal Register Actors leave out:

| Field | Why it matters |
| --- | --- |
| `commentsCloseOn` | The public-comment deadline — **when you have to act by**. Present on 92% of proposed rules and about a third of notices (measured on a live 200-row sample per type). |
| `significant` | The Executive Order 12866 "significant rule" flag. Only ever non-null on final and proposed rules, and even there it's present on just ~45%/40% of them (measured, see FAQ) — always null on notices and presidential documents. |
| `regulationIdNumbers` | RIN — joins a document to its entry in reginfo.gov's Unified Agenda. |
| `docketIds` | Regulations.gov docket IDs, so you can pull the comment file. |
| `cfrReferences` | Flattened to readable strings like `40 CFR 257`. |
| `referencedCitations` | The Federal Register never edits a published document — a correction, comment-period extension or effective-date postponement always ships as a **separate** document that cites the original by its own `"NN FR NNNNN"` citation. This field pulls that citation out of the new document's text, so you can link it back to the original without reading `datesText` by hand. Empty on the ~90% of documents that don't amend anything. |
| `agencyNames` / `agencySlugs` / `parentAgencyNames` | One document usually lists a department *and* the bureau that wrote it; both are kept, split by level. |
| `fullTextUrl` | Public URL of the complete document body as plain text. Free to fetch yourself — we don't charge you a second row for it. |
| `url`, `pdfUrl`, `citation`, `startPage`, `endPage`, `pageLength` | Cite it in a memo without a second lookup. |
| `filedAt`, `filingType`, `numPages`, `editorialNote`, `onPublicInspection` | Only on `dataset: "publicInspection"` rows (null otherwise) — see **Advance notice** below. |
| `subtype`, `signingDate` | Only on `documentTypes: ["PRESDOCU"]` rows (proclamations, executive orders, memoranda) — measured 100% filled on 40 live presidential documents, 0% on 40 each of rules/proposed rules/notices. Always null when you don't ask for presidential documents. |
| `executiveOrderNumber` | A further subset of presidential documents — only executive orders get a number (proclamations and memoranda don't). Measured ~28% of presidential documents (11/40 live sample). |

Plus `documentNumber`, `type`, `subtype`, `title`, `abstract`, `action`, `datesText`, `publicationDate`, `effectiveOn`, `signingDate`, `topics`, `president`, `executiveOrderNumber`, `excerpt`, `jsonUrl`.

## Who uses this

- **Regulatory-affairs and compliance teams** tracking every rule touching their sector, with the comment deadline attached.
- **Trade and customs consultancies** watching tariff, AD/CVD and export-control notices.
- **Law firms and lobbyists** monitoring a docket or RIN from proposed rule to final rule.
- **Industry associations** building a weekly "what changed" digest for members.

## Input

```json
{
  "documentTypes": ["RULE", "PRORULE"],
  "agencies": ["Environmental Protection Agency"],
  "commentsOpenOnly": true,
  "maxResults": 100
}
```

| Input | Notes |
| --- | --- |
| `dataset` | `published` (default) searches the full archive back to 1994. `publicInspection` returns documents that are **filed but not published yet** — see **Advance notice** below. |
| `documentTypes` | `RULE`, `PRORULE`, `NOTICE`, `PRESDOCU`. All four by default. |
| `presidentialDocumentTypes` | Narrow `PRESDOCU` rows to a subtype: `executive_order`, `proclamation`, `memorandum`, `notice`, `determination`, `other`. Server-side filter, verified live (real counts: 1,567 / 4,436 / 807 / 784 / 801 / 60). Empty = all subtypes; no effect unless `PRESDOCU` is in `documentTypes`; ignored on the Public Inspection desk. |
| `agencies` | Slug (`environmental-protection-agency`) **or** full name — both are resolved against the official 473-agency list, and anything unrecognised is reported in the log instead of silently returning zero rows. **Filtering by a parent agency includes its sub-agencies**: `homeland-security-department` also returns Coast Guard, FEMA, CBP, TSA and USCIS documents. |
| `publicationDateFrom` / `publicationDateTo` | `YYYY-MM-DD`. Defaults to the last 90 days; the archive goes back to **1994-01-03**. Defaults are Eastern calendar days — the Federal Register publishes its issue at 8:45 a.m. ET, so that is the calendar its dates are on. |
| `searchQuery` | Full-text search across title and body — it matches a single passing mention anywhere in the document, not just the subject. For a topical search pair it with `order: "relevance"` (see the FAQ). |
| `significantOnly` | EO 12866 significant rules only — overwhelmingly rules and proposed rules, but not zero on Notices (verified live: ~6-16/year). Throws if `documentTypes` is limited to `["PRESDOCU"]` alone — presidential documents never carry this flag. |
| `commentsOpenOnly` | Only documents whose comment period closes today or later — **"today" in Eastern time**, the clock the 11:59 p.m. deadline itself runs on, so a run scheduled for the small hours UTC still returns the documents closing that same ET day. Throws if `documentTypes` is limited to `["PRESDOCU"]` alone — presidential documents are never opened for public comment. |
| `cfrTitle` / `cfrPart` | Filter to documents affecting a specific Code of Federal Regulations title (1-50) and, optionally, a part within it (e.g. title `40`, part `60` = 40 CFR Part 60, New Source Performance Standards). Verified live: a single title alone narrows the 10,000-clamped baseline to a few hundred/year; adding a part narrows further into the dozens. `cfrPart` requires `cfrTitle` — the API has no title-less part lookup and 400s on one, so this Actor fails loudly client-side instead. |
| `order` | `newest`, `oldest`, `relevance`, or `executive_order_number`. The last one only sorts meaningfully with `documentTypes: ["PRESDOCU"]` + `presidentialDocumentTypes: ["executive_order"]` — outside that scope almost every row has no EO number assigned and the run logs a warning. Verified live 2026-09-29. |
| `maxResults` | Up to 50,000. |
| `watchLabel` | Optional. Name a saved query and get **only what is new since your last run** — see below. |
| `webhookUrl` | Optional. POST a small JSON completion summary (documents pushed, rows scanned, pages walked, dataset ID, watch new-count) here when the run finishes — see FAQ. |

## Advance notice: the Public Inspection desk (`dataset: "publicInspection"`)

By the time a rule appears in the Federal Register it is already law of record. Before that it sits on the **Public Inspection desk** — filed by the agency, scheduled, and publicly readable **1-3 business days early**. Set `dataset: "publicInspection"` and you get those documents, with the same field names as a published row plus:

| Field | Notes |
| --- | --- |
| `filedAt` | Exact UTC timestamp the agency filed it. |
| `publicationDate` | The date it is **scheduled** to publish — usually the next business day. |
| `filingType` | `regular`, or `special` when an agency asked for early public availability (about 4% of the desk). |
| `numPages`, `editorialNote` | Page count, and the Office of the Federal Register's own note when there is one — e.g. a withdrawal request received after filing. |
| `onPublicInspection` | `true` on these rows, `false` on published rows, so a mixed dataset stays unambiguous. |

Three things to know. The desk holds **one issue at a time** (~100-150 documents, mostly notices) and is empty on weekends and federal holidays, so run it on a daily schedule with a `watchLabel` rather than expecting a hit on any single run. It supports `documentTypes`, `agencies`, `searchQuery` and `maxResults` **only** — there is no date range, significance flag, comment deadline, CFR index or sort order on the desk, and this Actor drops those inputs with a warning in the log instead of passing them through. (That last part matters: the desk's own `available_on` parameter does not narrow a query, it *replaces* it — asking for one issue plus one agency returns the whole issue. Verified live 2026-09-17.) And the desk has a **daily blackout window, undocumented in the schema**: verified live 2026-09-24 at 05:01 Eastern, the API's own `meta.pil_unavailability_message` said the list "is unavailable after 12AM Eastern time and will return... at 8:45AM Eastern time" — yet the request still returned 3 documents rather than an empty list, all carrying yesterday's `last_public_inspection_issue` date. If you poll before ~8:45am Eastern, compare `last_public_inspection_issue` to today's date before treating a result as the current issue — see [the dedicated guide](https://fetchsmith.com/blog/federal-register-public-inspection-early-access) for the live proof and a worked example of a document reading in full a day before it exists on the official `published` endpoint.

```json
{
  "dataset": "publicInspection",
  "agencies": ["environmental-protection-agency"],
  "watchLabel": "epa-filed-today",
  "maxResults": 100
}
```

A `watchLabel` used on the desk gets its own baseline, separate from the same label on published documents — a Public Inspection row and its later published row share a document number, so mixing them would silently hide the publication you switched modes to catch.

## Only what's new since last run (`watchLabel`)

A rule-watching job is a *subscription*, not a search: you want the documents published since you last looked, not the same 400 rows re-delivered (and re-charged) every morning.

Set `watchLabel` to a name for the query — `epa-air-rules`, say — and this Actor keeps track of which documents it has already given you under that name:

- **The first run on a new label is a free baseline.** It records what already matches, returns **zero** results and charges **nothing**. It walks ids only, not full documents.
- **Every run after that returns only the new documents.** Already-delivered rows are dropped before they are built or billed, so you never pay for the same document twice.
- **A document counts as delivered only once it has actually been charged.** Anything cut off by `maxResults` or a charge limit stays "new" for the next run rather than vanishing.
- **Changing a filter starts a fresh baseline** — a different filter is a different question, so you don't get a dump of everything the old, narrower query happened to exclude.
- **The rolling 90-day default date window is deliberately *not* part of that identity.** It moves every day; if it counted, a daily schedule would re-seed forever and never deliver anything. Dates you set *explicitly* do count.

The baseline lives in a key-value store named `fetchsmith-fedreg-watch` on your own account, so it survives between runs and you can inspect or reset it yourself. Point an Apify schedule at the Actor and you have a Federal Register alert.

**Baseline size cap.** A baseline holds up to **60,000** ids in one saved record. If a label's baseline grows past that, the oldest-first-seen ids are dropped — and a dropped id is no longer recognised, so it comes back as "new" on a later run **and is charged again**. The run that drops them says so explicitly: a warning in the log, a note on the run's status message, and `baselineTruncated` / `baselineTruncatedTotal` (this run / the whole life of the label) in `RUN_SUMMARY` and the `webhookUrl` payload. If you see it, narrow the query (an agency, a document type, a shorter publication-date window) or split it across several labels so the baseline stays under the cap. This is separate from `seedCapped` in `RUN_SUMMARY`, which means the one-time baseline *walk* stopped at the 20,000-document `SEED_CAP` before it finished reading the whole current match set.

**If the baseline run itself hits an upstream error partway through, it saves nothing and the run fails.** A baseline walk that stopped early because the Federal Register API errored is not the same as one that finished — if the partial id set were saved and marked "seeded", the next run would treat every document past the stopping point as new and **charge for all of them**. Instead the run fails outright (a baseline charges nothing either way, so re-running it is free) and `RUN_SUMMARY.incompleteReason` is `source-error`. Just re-run the same label and filters once the source recovers.

Note: unlike some of our other government-data Actors, there is no `watchChanges` option here — a Federal Register document's own record never mutates after publication (see `referencedCitations` above for how amendments actually surface).

## Sample output

```json
{
  "documentNumber": "2026-18552",
  "type": "Proposed Rule",
  "title": "Wisconsin: Approval of State Coal Combustion Residuals Permit Program",
  "publicationDate": "2026-09-11",
  "commentsCloseOn": "2026-11-10",
  "agencyNames": ["Environmental Protection Agency"],
  "docketIds": ["EPA-HQ-OLEM-2026-4324", "FRL-13374-01-OLEM"],
  "cfrReferences": ["40 CFR 257"],
  "citation": "91 FR 57842",
  "referencedCitations": [],
  "url": "https://www.federalregister.gov/documents/2026/09/11/2026-18552/wisconsin-approval-of-state-coal-combustion-residuals-permit-program",
  "fullTextUrl": "https://www.federalregister.gov/documents/full_text/text/2026/09/11/2026-18552.txt"
}
```

## No 10,000-row wall

The Federal Register API's page-based paging stops hard at 10,000 rows (`page=11` at `per_page=1000` is an HTTP 400), and its `count` field is clamped at 10,000 even when far more documents match. This Actor pages with the API's own `search_after_cursor` instead, which walks straight past that limit — verified by pulling 14,000 consecutive rows in one run. Set `maxResults` to what you actually want; you will not hit a hidden ceiling at 10,000.

## Pricing

**$0.0008 per result, no Actor-start fee, the same on every Apify plan tier.** 1,000 documents costs $0.80.

We re-priced the whole niche live against every listing's in-effect `pricingInfos` (per-row rates re-verified 2026-10-03, sweep re-run 2026-10-05): **94** Store listings mention the Federal Register, and 87 of them carried a comparable per-event price at the 2026-10-03 pricing pass. **We are not the cheapest Federal Register Actor in the Store.** Four listings undercut our $0.0008/row and one ties it — an earlier version of this page claimed we were cheapest on the Free and Bronze tiers, which was wrong, and the claim is gone. A further seven beat us only from a specific Apify plan tier or run size up; they are listed as tiered partial undercutters further down. The paid niche runs $0.00002–$0.05 per row, **three** rivals are on Apify's FREE model at $0, and 47 of the 87 add an Actor-start fee on top of their per-row rate.

Who beats us, with the arithmetic:

- `bikram07/federal-register-monitor` is **free** — Apify's FREE pricing model, $0 — and reads the same official API, capped at 5,000 records per run. Nothing we charge beats free.
- `teodor_banea/federal-register-monitor` bills $0.00035/row plus a $0.00005 start fee: 56% under our rate on every plan tier, and it is cheaper than us from the very first row ($0.35 vs our $0.80 per 1,000 documents). Its `maxResults` ceiling is 100,000 — double ours — so the row-cap mitigator that blunts other cheap rivals here does not apply to it.
- `mrprince90/regulatory-change-monitor` bills $0.005 per run plus $0.00002/row, so we are cheaper only on runs of 6 rows or fewer and it wins on anything larger ($0.025 vs our $0.80 per 1,000). It caps at 500 rows per run and is multi-jurisdiction — EU Official Journal, UK and Indonesia alongside the US Federal Register.
- `jungle_synthesizer/whitehouse-executive-actions-crawler` bills $0.0005/row but charges $0.10 on every run, so we are cheaper up to 333 documents and it is cheaper above that. It covers presidential actions only (executive orders, proclamations, memoranda, determinations), not the full Register.
- `automly/federal-register-notices-api` matches our $0.0008/row exactly with no start fee. It caps `maxResults` at 100 and covers notices only. All five of these rivals' prices and caps were re-verified live 2026-10-03 with **no change to any of the five** — `bikram07` is still on the FREE model, and the other four still charge exactly the rates quoted above.

Among the rest: `koalastuff/federal-register-rule-monitor` is tiered — $0.001/row on Free, $0.0009 Bronze, $0.0008 Silver, $0.0007 Gold and above — plus a $0.00005 start fee, so it is dearer than us on Free and Bronze, ties us per row on Silver, and sits $0.0001 under us on Gold+; but its schema caps `maxResults` at **100**, which tops that advantage out at about one cent on a full run ($0.07005 vs our $0.08000), and it cannot run a larger job at all. The niche's most common rate is $0.001/row flat with no start fee, 25% above us — `agentictools/federal-register-monitor` (caps `maxItems` at 1,000) and `chrisp1211/federal-register-scraper-max` (no cap) among them. At the expensive end, `nexgendata/federal-register-rules-scraper` charges a flat $0.05/row and `nexgensignal/federal-rulemaking-records` is tiered from $0.05/row on Free down to $0.0335 on Gold and above (an earlier version of this page called both "flat $0.05/row" — wrong for the second one, fixed), and the single-vertical `zentrafoundry` Federal Register watchers charge $0.02/row. There are **13** of those in this niche, not the three an earlier version of this page listed: `zentrafoundry/workplace-safety-inspection-delta-monitor`, `zentrafoundry/solar-interconnection-queue-watcher`, `zentrafoundry/public-debarment-sanctions-lite-monitor`, `zentrafoundry/ferc-docket-filing-change-radar`, `zentrafoundry/fcc-equipment-authorization-competitor-launch-tracker`, `zentrafoundry/hhs-ocr-hipaa-breach-delta-monitor`, `zentrafoundry/340b-opais-delta-monitor`, `zentrafoundry/cms-coverage-decision-change-watcher`, `zentrafoundry/faa-airworthiness-directive-fleet-watcher`, `zentrafoundry/usda-fsis-export-requirement-change-tracker`, `zentrafoundry/aphis-export-requirement-tracker`, `zentrafoundry/fda-warning-letter-category-monitor` and `zentrafoundry/bis-entity-list-supplier-exposure-watcher`. Each one filters the Federal Register down to a single regulatory vertical (FERC, FCC, HIPAA breaches, 340B, CMS coverage, FAA airworthiness, FSIS/APHIS export rules, FDA warning letters, BIS entity list) at 25x our per-document rate. Watch the shape of their records: since a 2026-10-01 repricing each one carries a stack of $0.0001 events (`dataset-processed`, `record-saved`, `enriched-record`, a vertical `*-scan` or `*-delta`) alongside the real `result-delivered` charge at $0.02, so a tool that reads the *cheapest* event on the record scores them as 8x cheaper than us when they are 25x dearer. Their own READMEs confirm the $0.02 ("**$0.02 / FR document**"), as does `isPrimaryEvent`. `nexgenwatch/us-federal-register-rule-event-watch` bills a different shape entirely: $0.02 per run plus $0.067–$0.10 per source check and $0.0034–$0.005 per rule-event delta, before any document is delivered. Pricing and input-schema caps re-verified live 2026-10-03.

A widened, 15-term Store sweep (re-run 2026-10-03, 90 matching listings — unchanged from the count above) turned up four more listings never named on this page, none of them cheaper: `ryanclinton/federal-register-search` (14 users, 1 new in the last 30 days — the single biggest listing in this niche by users, bigger than every rival named above) charges $0.002/document plus a $0.00005 start fee, 2.5x our rate; `pink_comic/federal-register-search` (6 users) charges $0.002/row plus a $0.0001 start fee, same multiple; `benthepythondev/federal-register-intelligence` (4 users) is tiered $0.002 (Free) down to $0.0014 (Diamond), still 1.75x-2.5x us; `ai_solutionist/regulatory-intelligence-api` (3 users) charges $0.002/row plus a $0.005 start fee but is a different product — each row is an AI-enriched regulation summary with requirements, citations and RAG chunks, not a plain document export. All four checked and priced live 2026-10-03.

A second pass on 2026-10-03 priced **every one of the 89 matching listings** rather than stopping at the top of the niche, and named six more that this page had never mentioned. **None of them undercuts us either**, so the count above still holds — four listings cheaper, one tie:

- `challenge_logic/federal-register-deadline-monitor` (2 users, 1 new in the last 30 days) charges $0.0015/row plus a $0.00005 start fee, 1.9x our rate (verified 2026-10-03). It is the closest feature rival on this page: it exists only to track comment-close and effective-date deadlines, which we expose as flat fields on every document rather than as a separate product.
- `malonestar/adcvd-trade-remedy-tracker` (2 users) is tiered $0.008/row on Free, $0.0064 Bronze, $0.0056 Silver, $0.0044 Gold, $0.0032 Platinum, $0.0024 Diamond, plus a $0.00005 start fee — **dearer than us on every tier**, 3x at the very best and 10x at worst. It covers antidumping/countervailing-duty notices only.
- `brightpath-data/federal-register-search` (2 users) charges $0.0015/row plus a $0.0001 start fee, 1.9x us, and caps `maxResults` at 100.
- `sovereign_workspace/federal-register-monitor` (2 users) charges **$0.01 per document matched** plus a $0.00005 start fee — 12.5x us. Its record also carries a $0.00001 dataset-item event, but its own README states the charge plainly: "`document-matched`: $0.01 per document returned."
- `george.the.developer/federal-register-monitor` (2 users) charges $0.02 per document, 25x us, with a $0.05 `full-text-brief` add-on for full metadata. Its README advertises a $0.25 start fee and a $0.10 brief, both dearer than what the live record actually bills — where the two disagree, the live record is what you are charged.
- `copious_atoll/federal-register-scraper` (1 user) charges $0.001/row plus a $0.00005 start fee, 1.25x us.

Every per-event price on this page was read from each listing's live in-effect `pricingInfos` on 2026-10-03, and cross-checked against that listing's own published pricing table wherever it has one.

A third pass on 2026-10-04 (cycle 1231) ran the full `niche-unnamed` diff against the current 91-listing sweep (up from 89/90 above — the niche keeps growing) and live-priced the remaining unnamed tail: 57 listings, every one of them sitting at 1-2 users, confirming this niche is saturated enough that user count no longer separates signal from noise (Apify pins a new listing at ~2 users, so a user floor here is really an age floor). That tail turned up **five more tiered partial undercutters**, none disclosed before, each beating us only from a specific Apify plan tier or run size up rather than at every tier the way `teodor_banea` does above:
- `scrapesage/federal-register-scraper` (2 users) is tiered $0.001 (Free) -> $0.00085 (Bronze) -> $0.0007 (Silver) -> $0.00055 (Gold) -> $0.00038 (Platinum) -> $0.00025 (Diamond), no start fee: dearer than us on Free/Bronze, cheaper from Silver up.
- `hipersoft/federal-register-scraper` (2 users) is tiered $0.001 -> $0.0008 -> $0.00065 -> $0.0005 -> $0.0005 -> $0.0005 plus a $0.00005 start fee: dearer on Free, ties us exactly on Bronze, cheaper from Silver up.
- `arman-bd/federal-register-scraper` (1 user) is tiered $0.0015 -> $0.0011 -> $0.00075 -> $0.00056 -> $0.00048 -> $0.00027 plus a $0.00005 start fee: dearer on Free/Bronze, cheaper from Silver up.
- `themineworks/federal-register-scraper` (1 user) is tiered $0.001 -> $0.0009 -> $0.00075 -> $0.0006 -> $0.0006 -> $0.0006 on a flat $0.005 start fee: dearer on Free/Bronze at any size; on Silver it only overtakes us past ~100 documents in one run, and on Gold and above past ~25.
- `automation-lab/federal-register-rules-notices` (2 users) is tiered $0.0029 -> $0.0025 -> $0.00198 -> $0.00153 -> $0.00102 -> $0.00071 on a flat $0.005 start fee: dearer at every tier except Diamond, where it overtakes us only past ~57 documents in one run.

All five were read live via `pricingInfos` on 2026-10-04; none ties or beats us on the Free tier, the plan nearly every small buyer starts on. That pass also left roughly 45 listings in the tail ruled out *by their Store title or apparent product shape* rather than by a live price call — the fourth pass below priced all of them and found that ruling-out was wrong three times over.

A fourth pass on 2026-10-05 (cycle 1268) re-ran the sweep (now **94** matching listings, 55 of them never named on this page) and live-priced **every single one of the 55**, including the tail the third pass had dismissed on title/shape. Three of those previously dismissed listings turn out to be real, cheaper substitutes:

- `constant_quadruped/regulatory-change-monitor` (2 users, 27 successful runs in the last 30 days, last run 2026-10-04) is on Apify's **FREE** pricing model — $0, so it beats every rate we charge by definition. It is a scheduled Federal Register monitor built on the same official API, filtering by agency slug and keyword, with cross-run deduplication (`onlyNew`) and an optional RAG-ready markdown field; it also folds in SEC/FINRA/state RSS feeds. What we have against it is depth rather than price: the Public Inspection desk, 37 flat fields, comment-close and EO 12866 significance as queryable filters, and a 50,000-row ceiling versus its fixed look-back window.
- `martc03/regulatory-monitor-mcp` (1 user, 7 runs lifetime, last run 2026-09-08) is also on the **FREE** model at $0 — an MCP server giving AI assistants full-text Federal Register search by keyword, agency and document type. A per-tool-call MCP shape is not a reason to leave it out: for a buyer who wants the Register inside an LLM workflow it is a free substitute for this Actor.
- `arman-bd/govinfo-documents-scraper` (1 user) is tiered $0.0015 (Free) -> $0.0011 (Bronze) -> $0.00075 (Silver) -> $0.00056 (Gold) -> $0.00048 (Platinum) -> $0.00027 (Diamond) plus a $0.00005 start fee: dearer than us on Free and Bronze, cheaper from Silver up. It reaches the Register through GovInfo rather than federalregister.gov — `FR: Federal Register` is one of the 18 collection codes in its own input schema — so it returns GovInfo package metadata with PDF/text links, not the normalized document fields here, and it has no Public Inspection desk or comment-deadline filter. Same tier ladder as its sibling `arman-bd/federal-register-scraper` above.

The other 52 unnamed listings were all priced live and none of them undercuts us: 8 sit at $0.0009–$0.001/row, 19 between $0.0013 and $0.0025, and the remaining 25 from $0.003 to $0.05. The two listings titled "...No Login, $1.86/1k" do bill $0.00186/document as advertised (`quarterly_jingo/federal-register-scraper` and `fortuitous_pirate/federal-register-scraper`, both flat at that rate plus a $0.001 start fee) — but that was confirmed from their live pricing records, not taken from the title.

A fifth pass on 2026-10-07 (cycle 1353) re-ran the sweep (now **97** matching listings, 53 never named on this page) and live-priced every one of the 53. The `>=3`-user cohort stayed thin — only `logiover/federal-register-scraper` at 3 users — so the whole tail was priced regardless of user count, 1-user floor included. **Completeness holds outright: 0 of the 53 undercuts us at any size.** The cheapest five (`adobeflex/federal-register-lite` 3u, `brick_joey_yto/federal-register-monitor` 2u, `jungle_synthesizer/dea-arcos-prescriber-crawler` 1u, `s-r/federalregister-scraper` 2u, `scrapeworks/federal-register` 2u) all bill a flat $0.001/row, 25% above our rate; the rest run $0.0013-$0.25/row. None is on the FREE pricing model. The niche keeps growing (94 -> 97 matching listings since the fourth pass) but the price floor has not moved.

So at $0.0008/row what we actually offer is not the lowest sticker price: it is no start fee at any volume, the Public Inspection desk (a rule 1–3 days before it publishes), 37 flat fields including the comment-close deadline and EO 12866 significance, and a 50,000-row cursor-paged ceiling that walks past the API's own 10,000-row wall.

## FAQ

**Why did I get zero rows?**
The filters are ANDed. A `searchQuery` plus an agency plus `significantOnly` over a short date window often genuinely matches nothing — drop one filter. `significantOnly` is overwhelmingly rules and proposed rules, but it is **not** always zero on Notices — verified live, about 6-16 Notices a year carry the EO 12866 significance flag, so `documentTypes: ["NOTICE"]` + `significantOnly` over a wide enough date window can genuinely match. `documentTypes` limited to `["PRESDOCU"]` alone combined with `significantOnly` or `commentsOpenOnly` throws immediately instead — verified live, 0 matches across the Federal Register's entire 1994-2026 history for either, because presidential documents never carry a significance flag or a comment-close date. The run log spells out which cause applies.

**Why did my `publicInspection` run return nothing?**
The desk is small and resets every business day — a narrow agency or `searchQuery` legitimately matches nothing most days, and it is empty on weekends and federal holidays. Schedule it daily with a `watchLabel` instead of running it once. The log says which of these applies.

**My `searchQuery` results are not about my search term. Why?**
Because `searchQuery` is a whole-document full-text search and the default sort is `newest`, so you get the most recent documents that mention the term *anywhere*, including a single passing reference. Verified live on 2026-09-28: `searchQuery: "COVID-19"` with the default order returned 10/10 recent documents on unrelated subjects (antidumping duty investigations, pilot oxygen requirements, hazardous-materials paperwork) that each mention COVID-19 once in the body. The same query with `order: "relevance"` put the genuinely COVID-19 documents on top ("Termination of Three Declarations Authorizing Emergency Use of Medical Devices During the COVID-19 Pandemic", and similar). **Rule of thumb: use `order: "relevance"` when the query is a topic, and the default `newest` when the query is a name or identifier you expect to match exactly.** Adding a `publicationDateFrom`/`publicationDateTo` window around the period the topic was actually active narrows it further — for reference, the Federal Register carries 3,651 COVID-19 documents published in 2020 and 4,340 in 2021, against 207 so far in 2026.

**What timezone are the dates on?**
Eastern, because that is the timezone the Federal Register itself publishes on — an issue goes live at 8:45 a.m. ET and a comment period closes at 11:59 p.m. ET on its `commentsCloseOn` date. Actor runs execute in UTC, which is 4–5 hours ahead, so this Actor resolves "today" (for `commentsOpenOnly` and for the default `publicationDateFrom`/`publicationDateTo` window) against the Eastern calendar rather than the UTC one. It matters if you schedule runs in the small hours UTC: on 2026-09-29 there were 15 documents whose comment period closed that ET day, and a UTC-anchored run at 01:00 UTC would have dropped all 15 while they still had six hours left to comment on. Dates you pass in yourself are used exactly as written.

**Is `significant` reliable?**
Where it's non-null, yes — but non-null is rarer than you'd expect. Measured live on 200 final rules and 200 proposed rules (2025-01 through 2026-09): only **~45% of rules and ~40% of proposed rules** carry an explicit `true`/`false`; the rest are `null`. A `null` on a rule does **not** mean "not significant" — most rules are simply never submitted for EO 12866 review, so the flag was never assigned to them. If you need confirmed-significant documents, use `significantOnly` (which filters server-side to `true` only) rather than reading `significant` yourself and treating `null` as a negative. It is always `null` by design on notices and presidential documents.

**Does it fetch the full document text?**
No. Each row carries `fullTextUrl`, the public plain-text URL, so you fetch bodies only for the documents you care about instead of paying for text on every row.

**Is this legal?**
Yes. federalregister.gov publishes this API for public reuse, the content is US-government work in the public domain, and no row contains personal data.

**Why did my first `watchLabel` run return nothing?**
That is what a baseline run does: it records what already matches so that "new" means something, returns zero rows and charges you zero. The next run on the same label and filters returns only what has been published since.

**Can I reset or inspect a watch baseline?**
Yes. It is a plain JSON record in the `fetchsmith-fedreg-watch` key-value store on your own account, keyed by your label plus a fingerprint of the filters. Delete the record to start over, or read `seenIds` to see exactly what has been delivered.

**A rule I'm tracking got its effective date postponed — will `watchLabel` catch that?**
Not on the original document, because the Federal Register itself never edits it. What happens instead is a brand-new document (e.g. "Postponement of Effective Date") gets published citing the original by its `"NN FR NNNNN"` citation — `watchLabel` will deliver that new document like any other, and its `referencedCitations` field will contain the citation of the rule it postpones, so you can match it back yourself.

**How is `webhookUrl` different from Apify's own platform webhooks?**
Apify's platform webhooks are configured separately per Task/Actor via the Console or the Webhooks API — useful if you already live in the Apify Console, but extra setup if you're calling this Actor's API directly and just want a completion ping. `webhookUrl` is a plain input field: set it on the run itself and it POSTs a JSON body (`actorRunId`, `defaultDatasetId`, `finishedAt`, `pushed`, `scanned`, `pages`, and — if `watchLabel` is set — `watchSeeding`/`watchNewCount`) once the run finishes and every row is already pushed and charged. It's best-effort — a slow or failing webhook only logs a warning, it never fails the run, changes the result set, or affects billing.

## Related guides
- [Eight government JSON APIs that need no key — and the specific way each one lies to you](https://fetchsmith.com/blog/free-government-data-json-apis-no-key) — how this API's silent-failure shape compares across all eight free government JSON APIs we scrape.
- [The Federal Register tells you tomorrow's rules today — but only for 16 hours a day](https://fetchsmith.com/blog/federal-register-public-inspection-early-access) — live proof a Public Inspection document reads in full a full day before it exists on the official archive endpoint (404), plus the undocumented daily blackout window (midnight–8:45am Eastern) where the desk keeps serving yesterday's leftover filings instead of an empty result.
- [The Federal Register API says it has 10,000 documents. It doesn't — and the fix is already in the response](https://fetchsmith.com/blog/federal-register-documents-json-api) — the full write-up of the clamped `count`, the 10,000-row offset wall and the `search_after_cursor` that walks past it, the per-document-type field-population table, and why a mistyped agency slug 400s the whole query.
- [The FDA publishes every product recall as JSON — but you can't page past row 25,000](https://fetchsmith.com/blog/fda-openfda-recall-json-api) — the same "US government publishes it as keyless JSON" pattern, with a pagination wall that has no cursor escape hatch.
- [Eight ways an "only new since last run" watch mode silently stops working](https://fetchsmith.com/blog/incremental-api-watch-mode-four-traps) — how `watchLabel` is built, including the two paging bugs this API's `next_page_url` shapes caused and why a rolling date default must never enter the criteria fingerprint.
- [We nearly charged our own buyers twice for rows they'd already paid for](https://fetchsmith.com/blog/watch-baseline-eviction-rebilling) — a capped watch-mode baseline can silently evict old-but-current ids on a high-volume run, re-delivering (and re-billing) rows already paid for.
- [All FetchSmith tools](https://fetchsmith.com/tools)
- [Source code](https://github.com/Fetchsmith/fetchsmith/tree/main/actors/federal-register-scraper)
