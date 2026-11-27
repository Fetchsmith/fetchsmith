# Competitor audit history — trademark-search-scraper

Relocated verbatim from `README.md` at cycle 3813 (`NEW c3808a`), because the README had grown past Apify's 99,999-byte Store-page render cap. This is the dated `competitor_audit` resweep trail for 2026-10-03 through 2026-11-13 (cycles 1212 through 3158) — nothing paraphrased, nothing re-dated. The current niche baseline (cycle 3497, 2026-11-20 onward) lives in `README.md`'s Pricing section.

**Niche size verified live 2026-10-30; the per-listing prices in this paragraph verified live 2026-10-06.** The same 20-term Store sweep now sees **2,401** distinct listings and **154** that mention trademarks somewhere in their copy, up from 145 on 2026-10-23 and from the 114-of-543 reading this paragraph carried from 2026-10-06 to 2026-10-30; the older figures are corrected here rather than quietly re-dated, and the sweeps dated below record what each re-count found. Of the 2026-10-06 reading's 114, **89** were genuinely trademark products (the rest are unrelated scrapers — ZipRecruiter, Redfin, ImportYeti, TripAdvisor and the like — whose descriptions merely carry "all trademarks are the property of their owners" boilerplate). The in-effect price was pulled live for every one of the 89 — not just the leader, and not only the ones that happen to search the same register we do. Both figures grew on the 2026-10-06 re-sweep (from 108 mentions / 84 real trademark products on 2026-10-04); the earlier counts stood in this section until then and are corrected here rather than quietly re-dated. Previous re-checks corrected three statements (`parseforge`'s dearest-per-row superlative, `sian.agency`'s tier breakdown, and `automation-lab`'s FREE rate), added three multi-office listings that had never been named, and pinned the exact filed price changes at `jungle_synthesizer/euipo-trademark-scraper` and both `dev00` listings.

**The multi-office listings**, which is the only group doing the same job as this Actor (all prices below re-verified live 2026-11-19). `scrapers_lat/tmview-global-trademarks-scraper` is the closest structural match at 77 offices and tiers $0.015 (FREE) down to $0.012 (DIAMOND), 6–7.5× ours, in exchange for goods-and-services wording, opposition and register-event detail we do not return. `dltik` (186 users, up from 167, `dltik/euipo-trademarks-scraper`, the busiest TMview-based listing) charges $0.01/result plus a $0.00005 start — 5× ours — and bills separately for detail enrichment ($0.01/mark), applicant→company resolution ($0.005) and AI brand-clearance scoring ($0.02), three things it does that this Actor does not; its US sibling `dltik/uspto-trademarks-scraper` has the same shape against one register. `parseforge/tmview-trademarks-scraper` (27 users) is the second-busiest TMview-based listing and the dearest of the TMview-based listings per row: $0.021/result (FREE) down to $0.019 (GOLD), and — per a 2026-10-30 enterprise-discount filing that undercuts its own GOLD rung, caught this cycle — down further to $0.0152 (DIAMOND, was $0.019), **plus** a tiered $0.02–$0.0178 start fee, so a 50-row search costs about $1.07 there against $0.10 here. (An earlier version of this sentence called it "the dearest way to buy this data per row" outright. That was wrong and is corrected: `nexgendata/euipo-esearch-trademarks` at $0.05/trademark (cut from $0.10 on 2026-10-07) and `nexgendata/trademark-patent-search-api` at $0.05–$0.15/record, both named below, are dearer per row than parseforge — the superlative only ever held within the TMview-based group.) `hanamira` (81 users, `hanamira/patent-trademark-search`) is the single biggest trademark listing on the Store but mixes patents and trademarks rather than searching a register, and charges $0.004/result plus start — double our rate. `zinin/trademark-multiregistry` spans several registries at $0.01 (FREE) to $0.008 plus a $0.005 start, 4–5× ours. `jdepablos/trademark-watch-tmview` prices watching rather than rows, and its scheduled increase took effect **2026-10-01**: $0.035 per watched term plus $0.10 per match found, up from $0.02 per term. Our `watchLabel` mode charges only the $0.002 row rate, and only on marks you have not already been given.

Three further multi-office listings, none of them named here before the 2026-10-03 sweep and all dearer than us (prices re-verified live 2026-11-19, unchanged). `s-r/trademark-search` is the closest never-named structural match — one row per mark from USPTO, TMview, Madrid and IP Australia — at a flat $0.006 per trademark with no start fee, 3× ours, in exchange for goods-and-services text and per-source status flags. `everyotherfriday/trademark-search` reads TMview and USPTO directly for US/EU/UK coverage at $0.008 per returned record, no start fee, 4× ours. `nexgendata/trademark-patent-search-api` is the widest listing in the niche by source count — you pick one of 18 registries per run (USPTO, EUIPO, WIPO PATENTSCOPE, UK IPO, CNIPA, JPO, KIPO, India, HK and more) — but bills per record by source, $0.05 for a USPTO trademark and $0.10 for an EUIPO one (up to $0.15 for some patent sources), plus a $0.005 start: 25–50× our row rate for trademark data, and one source per run rather than all of them in one result set.

**The single-register listings** are cheaper to build and mostly dearer to buy; none of them reaches past one office, where this Actor searches 70+ in a single call (verified live 2026-10-03). US-only: `alizarin_refrigerator-owner/uspto-api---patent-trademark-data` (64 users) charges a $0.10 start fee plus $0.01 per trademark search or detail lookup — and, which the previous version of this section did not say, only $0.00001 per returned row, so counting its $0.10 start and one $0.01 search its total ($0.11 + $0.00001/row) drops below ours ($0.002/row, no start) above about 55 rows in a single run; `dev00/uspto-trademark-api` (106 users, count re-verified live 2026-10-06) is $0.003 per batch check today, and its filed change for **2026-10-14** turns that flat price into a tiered one — $0.10 on FREE, $0.003 unchanged on BRONZE and above — so from that date it is 50× our row rate for anyone on the free plan and unchanged for everyone else; its sibling `dev00/uspto-trademark-text-check-api` ($0.005 per text check) carries the identical change on the same date; `fortuitous_pirate/uspto-trademark-scraper` (64 users, up from 57) **raised its price on 2026-11-03** (the change was filed 2026-10-19 and took effect that date) and is now $0.003488/result plus a $0.00465 start — about **1.7× our row rate**, with a start fee 4.65× what it was. This section carried its previous $0.00279/result plus $0.001 start (1.4× ours, in effect from its 2026-09-17 revision) for 11 days after that change, so the old figures are corrected here rather than quietly re-dated; note that its own listing title still advertises the superseded "$2.79/1k" rate, so the title is not a safe source for its price (re-verified live 2026-11-14); `nexgendata/uspto-trademark-search` (49 users) is $0.05/record and $0.05 per watch check, 25× ours; `memo23/uspto-trademark-scraper` (59 users, up from 53, re-verified live 2026-11-12) is $0.007/record plus a $0.005 start, price unchanged; `scrapesage/uspto-trademark-scraper` is $0.004/record with no start fee, plus brand-owner ($0.004) and IP-attorney ($0.005) lead enrichment we do not offer; `sheshinmcfly/uspto-trademark-checker` and `glistening_film/uspto-trademark-lookup` both match our $0.002 exactly, the first adding a $0.00005 start and the second nothing at all. EU-only: `nexgendata/euipo-esearch-trademarks` (48 users) cut its row price from $0.10 to $0.05 on 2026-10-07 (re-verified live 2026-11-19) — plus a $0.005 start and $0.05 per watch check, now 25× our row rate (was 50×); `ryanclinton/euipo-trademark-search` matches our $0.002/record exactly, adding a $0.00005 start.

The previous version of this section called that `nexgendata` listing "the dearest listing in the whole niche". On the full niche set **that is false** and is withdrawn (all prices in this paragraph re-verified live 2026-11-19, unchanged): `nexgenwatch/trademark-gazette-issue-digest` and `nexgenwatch/trademark-portfolio-report` charge **$15 per record** on FREE, tiering down to $10.05, and `ryanclinton/brand-protection-monitor` ($0.50/brand), `brasildados/cnpj-trademarks-patents` ($0.30 per tax ID), `irreplaceable_chevrotain/trademark-clearance-mcp` ($0.25/call) and `aurorasys/spain-trademark-watch-oepm` (up to $2.50 for a viability report) all price above it. Those are report and alerting products rather than per-row register searches, which is why a row-rate comparison with them is not very meaningful — but "dearest in the niche" was still the wrong thing to say, so it is gone rather than re-scoped.

We are **not** the cheapest listing here, and would rather say so than hide it (also verified live 2026-10-06). Seven listings undercut us, and here is the full set. The bookkeeping, re-derived mechanically on 2026-10-06 rather than carried forward: of the niche's 89 trademark listings, this section named **58** by name going into that sweep, and the in-effect price of all **31** it did not was pulled live, every charge event and every plan tier. Not one of the 31 undercuts our $0.002 per returned trademark, so the set below is still complete. (An earlier version of this paragraph said "37 of 84 … all 47 that it does not". Those were cycle-1212 figures and the niche has grown since; the three numbers are re-counted here, not re-dated.) The 31 are all small listings (1–2 users), and the closest any of them comes is `unrivaled_fortress/wipo-global-trademark-brand-watch` at $0.0026 per row on GOLD and above — about 1.3× ours — followed by `axiomworks/uspto-trademark-search-scraper` at $0.002975 on GOLD and above. Among the listings this section *does* name, the closest non-undercutters are `sian.agency/uspto-trademark-search-status-scraper` at $0.00234 per status record and `silentflow/uspto-scraper` at $0.002507.

Eight listings in the previously-unnamed set do advertise a charge event below $0.002 (every price in this paragraph re-verified live 2026-11-19, unchanged), and **every one of them is an Actor-start fee rather than a row price** — typically $0.00005 to $0.001 to begin a run, after which the actual data event costs $0.003 or more (for example `khadinakbar/uspto-trademark-batch-search` pairs a $0.00005 start with $0.005 per trademark result, and `nexgendata/india-trademark-search` pairs the same $0.00005 start with $0.05 per record). Reading the cheapest event on a listing as its row rate is the single easiest way to publish a competitor comparison that flatters us, so we price the data event and say so. The same applies to three listings this section does name: `luminar/uspto-trademark-monitor` (**delisted — the Apify API returned 404 for this Actor on 2026-11-07**) billed $0.000475 for an *unchanged*-target watch check (its actual record price was $0.01425), `technicaldost/uspto-trademark-status-monitor` $0.0005 for a single known-serial status check (records are $0.003), and `zentrafoundry/uspto-trademark-patent-watcher` $0.0001 for internal bookkeeping events (a matched IP record is $0.01).

**Cheaper than us from the first row, in exchange for covering exactly one office each.** `jungle_synthesizer/dpma-trademark-patent-de-scraper` is $0.0004/record (FREE) down to $0.00032 (GOLD+) with a $0.0001 start — five to six times cheaper than our $0.002, for the German DPMA register only. `getascraper/dpma-trademark-register-scraper` is cheaper still on the same register, $0.00035 (FREE) to $0.00026 (GOLD+) with no start fee at all. `jungle_synthesizer/ip-australia-trademark-scraper` is $0.001 to $0.0008 plus a $0.0001 start, half our rate, for IP Australia only. If Germany or Australia alone is all you need, those are the cheaper buy and we will not pretend otherwise; what you pay us for is `DE` or `AU` arriving in the same result set as `US`, `EM`, `GB`, `JP`, `CN` and 65 more from a single call.

**Eight more single/multi-office listings, never named before, all confirmed dearer at every tier (per-listing prices re-verified live 2026-11-19, 0 drift found; sweep counts below from cycle 1239).** A fresh 20-term sweep found 536 distinct listings (up from 526), 110 of which mention trademarks (up from 108) — none of the drift moved any verdict below. USPTO-only: `foxlabs/uspto-trademark-leads` is $0.006/result plus a $0.00005 start, 3× ours, and adds contact-enrichment on new filings we do not do; `parseforge/uspto-trademark-scraper` (assignment records only — a narrower data type than a full registration search) tiers $0.0065 (FREE) to $0.006 (GOLD+) plus a $0.02–$0.0178 start, 3× ours; `crawlerbros/uspto-trademark-search-scraper` (**delisted — the Apify API returned 404 for this Actor on 2026-11-07**) tiered $0.005 (FREE) to $0.003 (GOLD+) plus a $0.005 start, 1.5–2.5× ours; `abcdemprendes/uspto-trademark-search-ai` does not price by row at all — $0.05 per basic search plus a $0.005 start, then up to $0.48 per Claude-powered du Pont or TTAB analysis event, so it is dearer than us from the first search regardless of row count. `nexgendata/ttab-trademark-opposition-tracker` is a different data type (TTAB inter-partes disputes, not registration search) at $0.10/proceeding plus a $0.005 start — 50× our row rate. Single-office, not US: `nexgendata/uk-trademark-search` (UKIPO only) is $0.05/record plus a $0.005 start, 25× ours. International: `scrapers_lat/wipo-madrid-trademarks-scraper` tiers $0.015 (FREE) to $0.01275 (GOLD+), 6–7.5× ours; `parseforge/ip-australia-trademarks-scraper` (a second, never-named IP Australia-only listing alongside the already-named `jungle_synthesizer` one) tiers $0.005 (FREE) to $0.00375 (GOLD+), 1.9–2.5× ours. None of these eight undercuts us at any tier or volume.

**The 1–2-user tail, finished (verified live 2026-10-05, cycle 1278).** All 40 remaining unnamed listings that mention trademarks at 1–2 users were live-priced, not just skimmed by title — the USPTO/EUIPO/Canada-CIPO/Peru/Brazil/Argentina/Japan/Korea/Hong-Kong/Spain watch, status, TTAB, MCP and IP-intelligence variants this section had deferred since cycle 1239. None of them undercuts our $0.002/result: the closest is `noahadler/euipo-uspto-trademark-search`, which prices its row at exactly $0.002 but adds a $0.00005 Actor-start fee, so it ties us at volume and is marginally dearer on a single-row run — an exact tie, not an undercutter, named here so it is not mistaken for one later. Every other listing in the tail is a watch/alert product billing per delta or per tool-call rather than per search result (`nexgenwatch`'s CIPO/USPTO gazette watches at $0.054–$0.10, `paulovitor18/inpi-trademark-watch` at $0.15–$0.75, `thequietstack`/`glistening_film`/`outstanding_vegetable`'s USPTO watches at $0.02–$0.03), a single-office search dearer than ours by 1.5×–50× (`axiomworks`, `thoob`, `recordsdata`, `ivosandoval/spain-oepm-scraper`, `scrapers_lat`'s Peru/Argentina/Canada/WIPO-Madrid/TTAB listings, `nexgendata`'s Japan/Korea/Hong-Kong listings), or a differently-shaped product entirely (`shane_reich/name-clearance-verdict` and `protocol/brand-name-ip-screener` are flat-fee clearance/screening reports against a curated seed set rather than a full-register search; `maged120/brand-username-checker` (**delisted — the Apify API returned 404 for this Actor on 2026-11-14**) bundled social/domain checks; `nexgendata/patent-trademark-rag` converts documents to RAG chunks; `second_coming/patent-search-tool` charges a flat $0.02 per scan regardless of row count; `solidcode`/`seibs.co` bundle patents and trademarks together). Two listings in the tail turned out not to be trademark products at all once read live, despite names that say otherwise — a fresh instance of the cycle-1212/1277 lesson that a listing's scope must be confirmed from its own description, not its title: `nexgendata/patents-trademarks-ip-mcp-server` states in its own description "patents only — no trademark tools"; `zentrafoundry/uspto-trademark-patent-watcher-v2` states "Google Patents xhr for NVIDIA GPU. Not a USPTO trademark conflict watch." Neither belongs in this niche's count. No README price change results from this sweep — completeness holds, the 7-undercutter set named above is still the full set — but the deferred tail is now closed.

**Thirteen more listings, never named here before, all confirmed dearer than us at every tier (verified live 2026-10-06, cycle 1324).** The niche grew again (84 → 89 real trademark products) and the 2026-10-06 sweep re-priced the whole 31-listing un-named remainder; these are the ones worth naming. Full-register US searches: `devilscrapes/uspto-trademark-scraper` is $0.005/result — 2.5× ours — and its in-effect block also carries a **$0.20 Actor-start fee**, the dearest start fee anywhere in this niche, so a 10-row search costs about $0.25 there against $0.02 here; `scrapers_lat/uspto-trademarks-scraper` tiers $0.008 (FREE) to $0.0068 (GOLD+), 3.4–4× ours; `neuton/uspto-trademark-keyword-search` is a flat $0.025/result, 12.5× ours, and describes its own searches as "bounded"; `neverempty/uspto-trademark-search-monitor` is the closest in shape — a real USPTO text/owner/class search with a monitoring mode — at $0.008 (FREE) to $0.005 (GOLD+) per returned trademark, 2.5–4× ours, plus $0.0005 per monitoring check (that $0.0005 is a check, not a row price, so it is not an undercut). EU: `crawlerbros/euipo-trademark-design-search-scraper` (**delisted — the Apify API returned 404 for this Actor on 2026-11-07**) covered EUTM plus registered Community designs at $0.005 (FREE) to $0.003 (GOLD+) plus a $0.005 start, 1.5–2.5× ours. Watch and feed products, which bill per delta rather than per search result: `unrivaled_fortress/wipo-global-trademark-brand-watch` (newly registered WIPO-international and US filings) at $0.004 (FREE) to $0.0026 (GOLD+) plus a $0.0001 start — the closest row rate in the un-named set at 1.3× ours, but a new-filings feed rather than a register search; `accountable_eel/trademark-filing-watch` (USPTO **and** EUIPO new applications by Nice class) at $0.01 (FREE) to $0.005 (GOLD+) per matched filing plus a $0.00005 start; `automation_studio/uspto-trademark-radar` at $0.005 (FREE) to $0.003 (GOLD+) plus a $0.001 start; `friendlyapi/uspto-trademark-scraper` sells the USPTO daily firehose keyed by serial at $0.005 (FREE) to $0.003 (GOLD+) per serial checked and $0.02–$0.012 per 100 delivered events; `nexgendata/trademark-conflict-watch` bills $0.02 per watched item checked plus $0.10 per watch run and $0.10 per conflict match; `stefano_seggio/kipris-patent-trademark-status-monitor` (Korea KIPRIS) is $0.02 per new filing or status change and $0.008 per non-status field update. Different data types: `openrows/us-trademark-status` is a TSDR status lookup against serial or registration numbers you already hold — $0.006 per mark, 3× ours, and not a search at all; `nexgenwatch/trademark-dispute-mcp` answers TTAB and Canadian opposition questions as an MCP tool at $0.05 per tool call plus a $0.05 start. Seven of the 31 advertise a charge event below $0.002 and **not one of them is a row price** — six are Actor-start fees ($0.00005 to $0.001 at `unrivaled_fortress`, `accountable_eel`, `thequietstack`, `stefano_seggio`, `nexgendata/hk-trademark-search` and `automation_studio`) and the seventh is `neverempty`'s $0.0005 monitoring check. Reading the cheapest event on a listing as its row rate is the easiest way to publish a comparison that flatters us, so the data event is what gets priced here.

**The full unnamed tail re-priced on 2026-10-07 (cycle 1360): the listings that undercut our $0.002
are, with one exception, not trademark products at all.** A fresh 20-term sweep saw 546 distinct
listings, 114 of which mention trademarks anywhere in their copy (name/title-only matching returns
88 — the gap is description boilerplate, see below). **41** of the 114 are not named in this section
by full owner/slug handle, and the in-effect price of all 41 was pulled live and scored tier by
tier, every charge event included (verified live 2026-10-07). Seven of the 41 price a row below our
$0.002 on some plan tier, and **six of those seven are not trademark tools in any sense** — they
match this niche only because their description carries the standard "all trademarks belong to their
respective owners" affiliation disclaimer: `haketa/ziprecruiter-scraper` (job listings),
`haketa/healthgrades-scraper` (doctor directory), `logiover/tripadvisor-scraper`
(**delisted — the Apify API returned 404 for this Actor on 2026-11-21**),
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
`thriftykiwi/trademark-search-aggregator` (3 users as of 2026-11-09) reads the USPTO trademark search and EUIPO
TMview together — status, owner, Nice classes and the official record link — for a flat $0.001 per
returned mark with no start fee, half our $0.002 at every tier. It is a real substitute if USPTO
and TMview-covered EU offices are all you need; what you pay us for is those two plus 68 more
offices in the same call.

Eight more real trademark products are named here for the first time, all confirmed dearer at
every tier (verified live 2026-10-08): three watch feeds from `nexgenwatch` — `canada-cipo-trademark-decision-watch` ($0.1
FREE to $0.067 GOLD+, plus a $0.02 start), `cipo-trademark-watch` and `uspto-trademark-watch`
(both $0.08 FREE to $0.0536 GOLD+, plus a $0.02 start) — 27–50× ours; `thoob/uspto-trademark-feed`
($0.004 FREE to $0.0028 GOLD+, no start, 2× ours falling to 1.4× — **corrected 2026-11-25** off a
live re-read of its own Actor record; this line previously read "$0.004 flat ... 2× ours", which
overstated what it charges a plan holder, though it stays dearer than our flat $0.002 at every
tier — with a what-changed-since-last-run mode); `recordsdata/uspto-
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
Three share the shape already disclosed above for `crawlerbros/importyeti-scraper` (now delisted
— see above): `khadinakbar/
importyeti-scraper`, `alwaysprimedev/importyeti-scraper` and `devilscrapes/importyeti-alternative-
scraper` all carry a `trademarks` field inside US import/export trade data, not a register search.
The other ten match this niche only via disclaimer boilerplate or a trademark field buried inside
an unrelated product — `piotrv1001/ziprecruiter-jobs-scraper` and `parseforge/ziprecruiter-scraper`
(both job listings; the `parseforge` one is **delisted — the Apify API returned 404 for this Actor
on 2026-11-07**, so only the `piotrv1001` listing is still live, and neither was ever in scope
here), `parseforge/sunbiz-
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
  **PRICE CUT 2026-11-16, re-read live 2026-11-25 — it is now cheaper than this ladder says, and
  it no longer ties us on FREE; see the dated correction below for the current numbers.**
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
  **SUPERSEDED 2026-11-25 — it raised its row price on 2026-11-05 and is no longer an
  undercutter at any volume; see the dated correction below.**

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

**Correction: both disclosed undercutters moved, in opposite directions (re-read live 2026-11-25,
cycle 3700, during the fleet's standing vendor-catalogue triage of owner `scrapewise`). Our own
price was re-read first and is unchanged: flat $0.002 per trademark, one charge event, no
Actor-start fee.** Each rival's price comes from its own live pricing record — the
`isPrimaryEvent`-flagged recurring event, with its revision date — not from its title or a
marketing figure.

- `blackfalcondata/uspto-trademark-scraper` (2 users) **raised its row price from $0.00153 to a
  flat $0.0036 on 2026-11-05 and is no longer an undercutter at any volume.** It still charges
  the same $0.01 Actor-start fee on top. Its row rate alone is now **1.8x ours**, so the ~22-row
  crossover named above no longer exists in either direction: it is dearer at 1 row ($0.0136 vs
  our $0.002) and still dearer at 1,000 rows ($3.61 vs $2.00). The count in the paragraph above —
  "two of the thirteen undercut us" — is therefore **one** as of this date.
- `scrapewise/uspto-trademark-scraper` (3 users) **cut its price on 2026-11-16 and now undercuts
  this Actor more deeply than the ladder above records, including on FREE, where it used to tie
  us exactly.** Its single `resultado-entregue` event, still with no start fee, now reads
  **$0.0018 (FREE) → $0.00171 (BRONZE) → $0.001539 (SILVER) → $0.001368 (GOLD, PLATINUM,
  DIAMOND)** — 10%, 14.5%, 23% and **31.6%** under our flat $0.002, at every volume, where the
  figures above say 0%, 5%, 10% and 15%. The scope ruling above is unchanged and was re-read: it
  is still USPTO-only against this Actor's 70+ offices, with no opposition window, seniority
  claim, Vienna codes, territories or watch mode.

**The pricing decision above still holds at flat $0.002, and the deeper cut does not change it,
because none of its three stated revisit triggers has fired** — all three were checked live on
this date, not assumed. `scrapewise` is at **3 users**, nowhere near the 20-user threshold that
would make its adoption more than a thin signal (it was 3 users at the 2026-10-16 decision too,
so eight weeks of a deeper discount have moved it by zero). `foxlabs/euipo-trademark-data` is
still a flat **$0.003** with no start fee (1 user), above our $0.002, so it has not cut below us.
And no second *full-register* undercutter has appeared: `blackfalcondata` has gone the other way,
and the two TMview-breadth rivals named further down (`scrapersdelight/euipo-trademark-scraper`,
`trev0n/tmview-scraper`) were already counted at their own sweeps. A 31.6% discount held by a
3-user listing is a price signal with no demonstrated demand behind it; tiering against it would
cut margin on every buyer on every plan to match it.

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
(1 user) is a UK-IPO-only search at a flat **$0.0009/trademark**, no start fee — less than half
our rate, for UK coverage alone.

Two listings tie our row rate exactly but are dearer in practice once their fee is counted:
`trev0n/tmview-scraper` (9 users, up from 6, ~80 offices via TMview — the closest breadth match in this
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
`titan_coder/uspto-patent-assignment-ownership-radar` (**$0.03 per
`patent-assignment-delivered` row plus a $0.02 Actor Start fee, re-verified live 2026-11-25** —
this paragraph said "$0.04/result" from 2026-10-23 until today, which overstated its per-row rate
and omitted its start fee; the correction cuts both ways, since the start fee makes it dearer than
the old figure for runs of one or two rows and cheaper above that, and it remains far dearer than
our flat rate either way; patent-and-trademark ownership-transfer tracking, a different data type
again); `zaiq/domain-hunter` ($1.49 FREE →
$1.192 GOLD+, a domain-name generator that happens to mention trademark checks, not a register
search at all).

The 4 OWNER-bucket handles were each hand-verified live 2026-10-23 to confirm the existing
rule-out still covers them, not re-counted from an old title: `getascraper/wildberries-seller-scraper`
(29 users) bills $0.00225–$0.003/row for Russian marketplace seller identity data with a
`trademark` field among nine others, the same field-not-register shape already excluded for
other `getascraper` listings; `maged120/social-username-checker` (28 users as of 2026-11-15, up from 25) is a 60-site
username checker with an optional US trademark check as one add-on, the same bundled-product
shape already excluded for `maged120/brand-username-checker` (delisted — 404 on 2026-11-14); `devilscrapes/euipo-trademark-search-scraper`
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

- `rbbscrap/fast-uspto-trademark-scraper` (**delisted — the Apify API returned 404 for this Actor
  on 2026-11-07**) was a **FREE** listing — `pricingModel: FREE`, no pricing record at all, so it
  advertised **no charge event of any kind** and undercut our $0.002 from the first row with
  nothing to amortise. It was USPTO-only (wordmarks, serial and registration numbers, LIVE/DEAD
  TSDR status, Nice classes, owners, attorney leads) where this Actor searches 70+ offices in one
  call, and it returned no opposition window, seniority claim, Vienna code, territory or watch
  mode. It was **created 2026-10-24**, one day after the 2026-10-23 sweep, so it was a new entrant
  rather than a miss — but it was the most aggressive price in this niche's history while it
  lasted.
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
(2026-10-23) was the second, and `rbbscrap/fast-uspto-trademark-scraper` (2026-10-28, **delisted
— see above**) was the third. The conclusion does not change, for a reason the original trigger
did not anticipate: the new undercutters were a **free** USPTO-only listing and a
**free-to-$0.0008 JP-only** listing, and plan tiering could not have answered either — no ladder
we could publish undercuts $0.00 — and, now that the free USPTO-only listing is delisted, only
one single-office listing (the JP-only one) remains live; shaving our rate for every buyer on
every plan to chase it would give up margin without closing the only gap it actually has on us,
which is scope, not price. What a buyer
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
filing or opposition event, 3× ours; `barefoot_grade/uspto-trademarks-scraper` (**delisted — the Apify
API returned 404 for this Actor on 2026-11-07**) was $0.004 per mark
plus a $0.005 start, 2× ours before the start fee, and said in its own copy that it was "text
matching only; no legal clearance or similarity scoring".

Three of the nine leave the niche on scope, and the scope read was taken from each listing's own
description rather than its title — the standing cycle-1212/1277 lesson. Only one of the three is
even cheaper per unit: `ahmed_jasarevic/importyeti-scraper` tiers $0.0012 (FREE/BRONZE) to $0.0011
(GOLD+) per importer profile, below our row rate, but it sells ImportYeti US customs bill-of-lading
data in which "trademarks" is one field inside a supplier profile — not a trademark register search,
so it never reaches a row-rate comparison (the same exclusion already applied to
`crawlerbros/importyeti-scraper` above, now delisted — see above). The other two are dearer as well as out of scope:
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

**Audit refreshed 2026-11-06 (cycle 2822): the niche grew to 172 matched listings (up from 154 at
cycle 2484), and one genuine new undercutter surfaced.** Own price re-read live first, unchanged:
flat $0.002/result on every plan tier, single primary `result` event, no start fee. 21 never-named
handles turned up (17 with no owner mention anywhere in this README, 4 where the owner is named
elsewhere but this exact Actor ID was not); four of the 21 left the niche on scope, read from each
listing's own description: `ultimatemc/textile-fiber-label-checker` sells textile fiber-content
labels, no trademark data at all; `nimbryxo-studio/importyeti-us-importer-and-global-supplier-search`
sells ImportYeti customs/importer profiles, the same exclusion already applied twice above to
`crawlerbros/importyeti-scraper` (now delisted — see above) and `ahmed_jasarevic/importyeti-scraper`; `pink_comic/oregon-
trademark-search` covers Oregon's **state** trademark registry, which TMview does not reach at all
— its 81-office list has one slot for the US (`US`, the federal USPTO register) and none for any
individual state; `accountable_eel/domain-availability-check` is an RDAP domain-name lookup, not a
trademark search. The remaining 17 were all live-priced (17==17 cross-check against the pre-screen
count). One undercuts us at every tier:

- `exuberantal/euipo-uspto-trademark-brand-owner-scraper` ("USPTO, EUIPO & Global Trademark
  Scraper") charges a **flat $0.00075 per row, no start fee** — 62.5% below our $0.002, still at
  the niche's 2-user floor. It is not a pure register search: its own description says it also
  returns "patent/IP assignees" and "federal IP notices" alongside trademark filings, so part of
  what it bills is outside this Actor's trademark-only scope, but the trademark-filing rows
  themselves are a genuine, cheaper match.

The other 16 are dearer than us at every tier or an exact tie, not an undercut (all prices verified live 2026-11-06): `red.cars/tmview-
trademarks-pro` (also built on TMview) and `plainrecordlabs/cancelled-us-trademarks` both charge
exactly $0.002/row flat, matching us with no start fee either side; `fabrikit/uspto-trademark-
scraper` tiers $0.00315 (FREE) down to $0.0022 (GOLD+), close but still above us on every rung;
`rbbscrap/euipo-trademarks-scraper` is $0.0029 flat; the rest range from $0.003 (`kingly_
contest_7cb/uspto-trademark-watch`, `frankely84/mexico-trademark-search`, `jwaiworks/uspto-
trademark-new-filings`) up to $0.02 (`jpmendes/brazil-trademark-search-inpi`, `sweet-orb/euipo-
trademarks`) — including both of this sweep's Mexico- and Brazil-register listings
(`jpmendes/mexico-trademark-search-impi`, `latsouth/brazil-trademark-filings`), both in scope
since TMview's office list includes `MX` and `BR`, and both dearer than searching those same two
offices here. **Pricing decision: HOLD $0.002, no start fee** — the one new undercutter sits at 2
users, far under this fleet's 20-user re-price threshold, and it is a multi-data-type bundle, not
a pure trademark-register competitor at our scope.

**Audit refreshed 2026-11-13 (cycle 3158): the niche grew to 187 matched listings (up from 172 at
cycle 2822), and six more undercutters surfaced, one of them genuinely free.** Own price re-read
live first, unchanged: flat $0.002/result, no start fee. **DELTA method** — c2822 already
live-priced 17 of the then-unnamed tail 336 cycles ago, so rather than re-price the whole 24-handle
unnamed cohort, this audit diffed the handle sets: **19 new since c2822** (the other 12 of the
earlier 17 have left the unnamed list, already accounted for by c2822's own disclosure or scope
exclusion above). All 19 live-priced (`state/audit_data/c3158_tms_prices.json`), **19==19**
cross-check against `niche-unnamed`'s own count, 0 unresolvable.

Six undercutters, all at the niche's 2-3-user floor: `dami_studio/trademark-search-scraper` is the
deepest, a flat **$0.00005 per record** ($0.05/1,000) plus a $0.0001 start — 40x under us.
`apex-b2b-data/uspto-trademark-brand-leads` tiers $0.0015 (FREE) down to $0.00105 (GOLD+) with a
$0.00005 start, undercutting at every tier, though its own description also bills "brand intent
score" and attorney-lead fields outside this Actor's pure-register scope. `apex-nexus/uspto-
trademark-application-monitor` carries no `pricingInfos` at all (confirmed live) and no description
text either, so it is genuinely **$0** on a title-only USPTO match. `aurelix/uspto-trademark-search`
tiers $0.001 (FREE) down to $0.00064 (GOLD+) behind a $0.0023 start fee, crossing under our
no-start-fee rate by about row 2-3 at every tier. `rbbscrap/uspto-trademark-scraper` is flat $0.0009
(FREE) to $0.00063 (GOLD+), no start fee — a second listing from a vendor account already named in
this README (`rbbscrap/euipo-trademarks-scraper`, $0.0029 flat, dearer) and now undercutting a
**fourth** unrelated niche across this fleet, alongside `sam-gov-opportunities-scraper`,
`fda-recall-scraper` and `apple-podcasts-scraper`. `thirdwatch/uspto-trademark-watch` is a narrower
shape — it compares Gazette/status records for serial numbers you already hold, not a name search —
tiered $0.0025 (FREE) down to $0.00175 (GOLD/PLATINUM/DIAMOND only, where it undercuts); FREE,
BRONZE and SILVER stay above our floor. `fanndev/trademark-search-scraper` is the closest structural
match (TMview, 70+ offices, like us) and ties our $0.002 flat on FREE — where our lack of a start
fee keeps us cheaper at any volume — but tiers down from there behind a $0.005 start fee: BRONZE
$0.0018 crosses under us around row 25, SILVER $0.0016 around row 13, GOLD/PLATINUM/DIAMOND $0.0014
around row 9.

The remaining 12 of 19 are dearer at every tier (`aboo.script/branddb-wipo-int-scraper` $0.0028-
$0.004, `greyridge-signals/uspto-trademark-batch` $0.003, `hydrocore/uspto-trademark-search`
$0.0045-$0.006, `pshivam/uspto-trademark-search-scraper` $0.014-$0.02, `rjmacarthy/uspto-trademark-
scraper` $0.005, `mosaicked_sponge/uspto-new-trademark-leads` $0.003, `leons0016/india-trademark-
journal-watch` $0.12-$0.15) or a different product entirely, matched on boilerplate or adjacent
wording rather than a register search: `ferrolark/brand-name-checker`, `luke-main/brand-domain-
availability-checker` and `turboextract/brand-availability-check` check domain/social-handle
availability, not trademark registers; `gmpsignal/global-trademark-brand-ip-monitor` monitors
Certificate Transparency logs and RDAP domain registries, not a trademark office; `deadmist/
microstock-metadata-generator` matched only on stock-photo keyword boilerplate and sells nothing
trademark-related. **Pricing decision: HOLD $0.002, no start fee** — every one of the six
undercutters sits at 2-3 users, far under this fleet's 20-user re-price threshold.
