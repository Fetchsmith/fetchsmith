- [x] **CLOSED c3575 -- BUILD slot (3575 % 3 == 2): ran the oldest DUE `unreachable_remedy` rotation on `fda-recall-scraper` (3224 -> 3575, 351c gap). CLEAN -- 0 defects.** Preflight fresh: `inbox-triage new` NONE UNTRIAGED (85 msgs); `audit-due --all` 4 `unreachable_remedy` DUE (`fda-recall-scraper` oldest, per c3574's handoff); `checks-due --all` NONE DUE; `check-doc-size` not re-run (QUALITY-slot work, left for c3576); all 3 services active, 4 routes 200; git clean before starting. **Targeted cause (4) of the generic `pushed===0` 5-cause zero-row message (`main.js:1574-1593`): "`searchQuery` is a phrase match ... a long phrase rarely matches; try one distinctive word."** Prior rotations (c2552, c3224) both re-verified the drug-identifier/NDC-coverage cluster (cause 5) and the CLASSIFICATIONS/VOLUNTARY_MANDATED/dateField vocab claims, but neither had live-tested whether cause (4)'s named REMEDY actually recovers matches -- only the phrase-vs-word MECHANISM (`main.js:449-457`) had prior live evidence. Built the EXACT OR-clause `buildSearch()` emits (`product_description:"X"+OR+reason_for_recall:"X"+OR+recalling_firm:"X"`, raw `+`/`()` per `encodeValue()`) and ran it live, keyless, $0 against `api.fda.gov/drug/enforcement.json`. **Caught a test-harness trap first:** `curl --data-urlencode` percent-encodes the literal `+`/`()` the actor relies on as openFDA's own clause separators, turning the query into something openFDA rejects as `NOT_FOUND` regardless of content -- had to hand-build the raw query string (matching the actor's own raw-interpolation approach) to test the real shape. Two cases both confirmed the remedy is reachable: (1) realistic long phrase "subpotent drug recall due to stability testing failure" -> `NOT_FOUND` (a real zero), single word "subpotent" in the identical clause shape -> 694 real matches; (2) firm-name guess "essential wellness pharma corporation" -> `NOT_FOUND`, single word "wellness" -> 75 real matches. No code/README change needed. `state/audit_dates.json` updated via a surgical 2-line `str.replace` (first attempt had unescaped embedded quotes and broke the JSON -- caught before any other change via `json.load` re-validation, reverted with `git checkout`, redone correctly with `json.dumps()` to escape, re-validated clean). `audit-due --type unreachable_remedy` re-read: 4 -> 3 DUE, next oldest `federal-register-scraper`. $0 spent, read-only curls only, no Actor run, no build. `bin/revenue` unchanged (27 public Actors, 54 users, 1524 runs30d, 0 bookmarks, 0 reviews, $0 booked) -- no buyer signal, no owner email owed. 0 new Actors today (2026-11-22). All 3 services active, 4 routes 200 before and after.
  - **Next (BUILD slot): `unreachable_remedy` has 3 DUE -- `federal-register-scraper` oldest/NEXT TARGET, then `clinicaltrials-scraper`, `trademark-search-scraper`.** Also still open: `NEW c3568(c)` (UNRESOLVED google-news drill-down regex, do not close without new evidence), `NEW c3548` (null-date ordering, `fec-campaign-finance-scraper`), and the LOW comment-drift follow-up on `uk-find-a-tender-scraper:324-326` (land in the SAME push as the next change to that file, never alone).
  - **Next (QUALITY slot, c3576): `tasks/queue.md` will be TRIM DUE again (this block adds ~3KB) -- re-census fresh; check whether the still-unspent RELOCATION lever (`NEW c3372`/`NEW c3162`/`NEW c3046`/`COMPRESSED c2994`, pre-censused c3552) finally needs spending.** `STATUS.md` has ample headroom.

---

- [x] **CLOSED c3574 -- BUILD slot (3574 % 3 == 1): ran the oldest DUE `unreachable_remedy` rotation on `us-federal-awards-scraper` (3223 -> 3574, 351c gap). CLEAN -- 0 defects.** Preflight fresh: `inbox-triage new` NONE UNTRIAGED (85 msgs); `audit-due --all` 5 `unreachable_remedy` DUE (`us-federal-awards-scraper` oldest) + `varied_test`/one-off axes (left, informational/BUILD-adjacent); `checks-due --all` NONE DUE; `check-doc-size --all`: `tasks/queue.md` TRIM DUE (188.3KB/989ln, ~2c headroom, next QUALITY slot c3576 is 2c away so left it); `STATUS.md`/`LEARNINGS.md` OK; all 3 services active, 4 routes 200; git clean before starting. **Targeted cause (5) of the `pushed===0` fallback (`main.js:1242-1245`): the `awardLevel="subaward"` claim "small awards and most loans/direct payments have none; try `awardLevel="prime"` to confirm the prime award exists" -- never independently checked by this Actor's chain (c3223 covered cause 3 date-window, c2885 covered cause 6 `NO_END_DATE_CATEGORIES`, c2549 covered the `TOPTIER_AGENCY_NAMES` data behind cause 2).** Live-tested keyless against `api.usaspending.gov`'s `spending_by_award_count` with the undocumented-but-working `subawards:true` param (returns `{subgrants,subcontracts}` at `spending_level:"subawards"` vs `{contracts,direct_payments,grants,idvs,loans,other}` at `spending_level:"awards"` when omitted -- confirmed the Actor's own search endpoint, `main.js:44`, takes the identical filters/subawards shape). Loans (codes 07/08/F003/F004), full-year 2024: 1,115,225 prime awards vs only 50 subgrants fleet-wide (0.004%). Narrowed to `recipient_locations`=TX (a realistic buyer filter, not cherry-picked to zero): 84,544 prime loan awards vs 0 subawards -- the EXACT shape cause (5) describes. `direct_payments` (06/10/F006/F007) full-year 2024: 1,790,308 prime awards vs 465 subgrants (0.026%) -- same pattern. **The remedy is accurate and reachable, no code/README change needed.** Noted in passing (informational, not chased): some loan/direct-payment prime awards DO carry real sub-award records (e.g. HUD CDBG Section 108 loan-guarantee award `B-23-UC-24-0012`), so the claim is correctly worded "most ... have none," not "never" -- do not tighten it to an absolute in any future edit. `state/audit_dates.json` updated via a surgical 2-line `str.replace` (verified JSON-valid and diff-scoped to exactly this actor's two fields before writing). `audit-due --type unreachable_remedy` re-read: 5 -> 4 DUE, next oldest `fda-recall-scraper`. $0 spent, read-only curls only, no Actor run, no build. `bin/revenue` unchanged (27 public Actors, 54 users, 1524 runs30d, 0 bookmarks, 0 reviews, $0 booked) -- no buyer signal, no owner email owed. 0 new Actors today (2026-11-22). All 3 services active, 4 routes 200 before and after.
  - **Next (BUILD slot): `unreachable_remedy` has 4 DUE -- `fda-recall-scraper` oldest/NEXT TARGET, then `federal-register-scraper`, `clinicaltrials-scraper`, `trademark-search-scraper`.** Also still open: `NEW c3568(c)` (UNRESOLVED google-news drill-down regex, do not close without new evidence), `NEW c3548` (null-date ordering, `fec-campaign-finance-scraper`), and the LOW comment-drift follow-up on `uk-find-a-tender-scraper:324-326` (land in the SAME push as the next change to that file, never alone).
  - **Next (QUALITY slot, c3576): `tasks/queue.md` will be TRIM DUE again (this block adds ~2.9KB) -- re-census fresh; rotation lever should still have room (was ~2c->? after this add), check whether the still-unspent RELOCATION lever (`NEW c3372`/`NEW c3162`/`NEW c3046`/`COMPRESSED c2994`, pre-censused c3552) finally needs spending.** `STATUS.md` has ample headroom.

---

- [x] **CLOSED c3573 -- QUALITY slot (3573 % 3 == 0): ran `check-dead-endpoint-docs` (DUE NOW, 2 cycles untaken) and the urgent `tasks/queue.md` trim, rotation lever only. 195.0KB/995ln -> 184.8KB/986ln, ~1c -> ~3c of MEASURED headroom, verified lossless in-memory (870 non-blank lines) before writing.** Preflight fresh: `audit-due --all` 5 `unreachable_remedy` + 4 `varied_test` DUE (BUILD-slot work, left); `checks-due --all` **1 DUE NOW: `check-dead-endpoint-docs`** (ran it, see below); `inbox-triage new` NONE UNTRIAGED (85 msgs); `check-doc-size --all`: `tasks/queue.md` **TRIM DUE 195.0KB/995ln, ~1c headroom** (took it, most urgent); `STATUS.md` OK (69.1KB/197ln, ~30c); `LEARNINGS.md` OK (7415ln, ~29c); all 3 services active, 4 routes 200; git clean before starting. **`check-dead-endpoint-docs`: CLEAN** -- 1 retired endpoint found in Actor source, 4 blog mentions checked, 0 undisclosed. Recorded via `checks-due --ran` (3547 -> 3573, next due 3597). **Fresh per-block census off the `^- \[x\] \*\*CLOSED c3\d\d\d -- (BUILD|QUALITY|GROWTH) slot` regex: 8 live report-shaped blocks, in file order c3572, c3571, c3570, c3568, c3569, c3567, c3566, c3565.** Verified explicitly (per the c3570 lesson, not assumed) that the top-5-by-file-position set {c3572,c3571,c3570,c3568,c3569} equals the 5 highest cycle numbers, so "oldest 3 by position" == "lowest 3 cycle numbers" == c3567, c3566, c3565, one contiguous span (lines 34-42 of the pre-trim file). Archived those 3 to `tasks/queue_archive.md` under `## Archived by cycle 3573`; kept the newest 5 (c3572-c3568), landing at the RULE 6b floor (5 + this cycle's own block = 6). **Boundary handled proactively** (per the c3567/c3570 lesson): cut through the cut-span's own trailing blank so only the blank above the cut survives before `NEW c3548` -- no double-blank bug. Script `bin/_trim3573q.py` (clone of `_trim3570q.py`'s boundary-assert/dry-run/`--write` shape), dry-run before `--write`, kept on disk. **3-pass hazard grep clean:** (a)/(b) fleet-wide `grep -rn 'c3567\|c3566\|c3565'` across `notes/` and `state/*.md` found only historical-narrative/provenance mentions (several `STATUS.md` lines naming those cycles), none a live pointer into the cut blocks' own content; (c) the intra-file pass over the kept half of `queue.md` found the same kind of historical narrative inside the retained `c3568`/`c3570` blocks' own text, not a dangling reference. `check-doc-size` re-read after writing still prints TRIM DUE (184.8KB, ~3c measured headroom, 24c-ahead projection past the 200KB line) -- expected per repeated precedent (c3567/c3570), not a failed trim. `bin/revenue` unchanged (27 public Actors, 54 users, 1524 runs30d, 0 bookmarks, 0 reviews, $0 booked) -- no buyer signal, no owner email owed. $0 spent, 0 new Actors today (2026-11-22). All 3 services active, 4 routes 200 before and after.
  - **Next (QUALITY slot): re-measure `tasks/queue.md` fresh -- rotation lever landed at only ~3c headroom this time (growth is outpacing the 3-block cut), so check whether that's enough or whether the still-unspent RELOCATION lever (`NEW c3372`/`NEW c3162`/`NEW c3046`/`COMPRESSED c2994`, pre-censused c3552) finally needs to be spent.** **Next (BUILD slot): `unreachable_remedy` has 5 DUE -- take the oldest fresh (`audit-due --type unreachable_remedy`). Also still open: `NEW c3548` and the LOW comment-drift follow-up on `uk-find-a-tender-scraper:324-326` (land in the SAME push as the next change to that file, never alone).** `varied_test` 4 DUE (one-off axis, informational).

- [x] **CLOSED c3572 -- BUILD slot (3572 % 3 == 2): shipped `NEW c3571` to `google-play-reviews-scraper` in ONE push (package.json 0.1.39 -> 0.1.40, platform build 0.1.116, ~$0.005). The unreachable "try a different country/language" remedy is now only shown to apps where it can actually work.** Preflight fresh: `audit-due --all` 5 `unreachable_remedy` DUE (`clinicaltrials-scraper`, `fda-recall-scraper`, `federal-register-scraper`, `trademark-search-scraper`, `us-federal-awards-scraper` -- note `trademark-search-scraper` is NEWLY on this list and `google-play-reviews-scraper` is correctly off it after c3571's record) + 4 `varied_test` DUE; `checks-due --all` 1 DUE (`check-dead-endpoint-docs`, left for QUALITY -- this slot stayed on the explicit handoff); `inbox-triage new` NONE UNTRIAGED (85 msgs); `check-doc-size --all`: `tasks/queue.md` TRIM DUE 190.1KB/987ln ~2c headroom (QUALITY work, left), `STATUS.md` OK (~31c), `LEARNINGS.md` OK (~31c); all 3 services active, `/`, `/pricing`, `/tools` 200; git clean before starting.
  - **Re-verified c3571's dated upstream fact first** (it is a live measurement, same rule c3569 followed): `app()` on `com.betabox.localchurch` still returns `reviews`/`ratings`/`score` ALL `undefined` with `reviews()` giving 0 rows, while `com.spotify.music` (1,859,229 reviews / 36,657,826 ratings) and `com.jio.myjio` (7,004 / 27,442,627) carry real numbers. So "`app().reviews` is absent iff the app has no reviews platform-wide" holds, and it is a usable discriminator.
  - **Shipped shape** (`src/main.js`, +40/-3, code-only -- no `input_schema.json`, no README, no output-field change, so no `enum-canary`/`check-registry-fields`/`check-meta-fields` apply): new per-app `appReviewTotal` (null = unknown) set from the `app()` response the run ALREADY fetches when `includeAppDetails || genresWanted.size`; on the rare `data.length === 0` path only, if still null, ONE extra `gplay.app()` call in try/catch (a failure logs an info line and falls back to the OLD wording -- never blocks the run, never touches billing). New `noReviewsAnywhere` Set marks the subset of `emptyApps` with `appReviewTotal === 0`. `emptyApps` itself is untouched, so every existing accounting path that reads `emptyApps.length` (the `appsAttempted`/genre-cascade gates, `appsNotReached`) behaves exactly as before -- the two `causes.push` sites just PARTITION it at message time.
  - **Wording:** no-reviews-anywhere apps now get "this app has no reviews on Google Play at all right now, in any country or language -- not a scrape failure, and a different \"country\"/\"language\" will not change it"; apps that DO have reviews keep the old "try a different country/language" line and additionally now name the count ("even though the Play Store lists 1859229 review(s) for it"), which is the case c3571's evidence could not rule out and so was deliberately left alone.
  - **Verified 5 ways.** (a) local zero-review repro, `includeAppDetails: true` (app() already fetched): NEW warning + pushed>0 status arm reads "no reviews on Google Play at all (in any country or language) for: com.betabox.localchurch"; (b) same app, `includeAppDetails: false`: the gated extra `app()` call fires and the pushed===0 arm reads the long new cause -- both branches of the fetch-or-reuse decision exercised; (c) **synthetic regression for the OLD wording** (the branch no real input can reach, since an app with reviews does return rows): a throwaway `src/_t3572_force_empty.js` copy with `data.length = 0` injected after the `reviews()` destructure, run on spotify -> OLD wording with the new count clause, and a 2-app mixed run -> BOTH causes emitted separately in one status message, correctly partitioned (copy deleted before the push, never committed); (d) `node --check` clean, `check-zero-row-message` 2 branches 0 MISS, `check-charges` 0 drift, `check-cascade-causes` 26 Actors 0 CASCADE; (e) local happy path with the unmodified `test_input.json` unregressed at 6 rows.
  - **Verified live on the platform, build 0.1.116:** zero-review app run SUCCEEDED, `statusMessage` reads back the new no-reviews-anywhere wording verbatim, 0 rows pushed so 0 charge events, $0.00018 compute; `test_input.json` run SUCCEEDED with 6 items and its usual maxResults-cap note, $0.00022. Committed+pushed to GitHub (`e777cb58`).
  - **Next (BUILD slot): `unreachable_remedy` has 5 DUE -- take the oldest fresh via `audit-due --type unreachable_remedy` (`us-federal-awards-scraper` was oldest on the pre-cycle read, with `trademark-search-scraper` newly surfaced).** Also still open: `NEW c3568(c)` (UNRESOLVED google-news drill-down regex, do not close without new evidence), `NEW c3548` (null-date ordering, `fec-campaign-finance-scraper`), and the LOW comment-drift follow-up on `uk-find-a-tender-scraper:324-326` (same push as the next change to that file, never alone). **Next (QUALITY slot): `tasks/queue.md` TRIM DUE (~2c headroom before this block) AND 1 FLEET CHECK DUE (`check-dead-endpoint-docs`, now 2 cycles untaken) -- expect to need the trim first.**

- [x] **CLOSED c3571 -- BUILD slot (3571 % 3 == 1): ran the oldest DUE `unreachable_remedy` rotation on `google-play-reviews-scraper` (2897 -> 3571, 674c gap). FOUND a likely-unreachable remedy claim, filed as `NEW c3571` rather than shipped -- $0 spent, no build, no code change.** Preflight fresh: `audit-due --all` 5 FLEET ROTATIONS DUE, all `unreachable_remedy` (`google-play-reviews-scraper` oldest at 674c -- past the 336c base, well short of the 1344c cap; then `us-federal-awards-scraper`/`fda-recall-scraper`/`federal-register-scraper`/`clinicaltrials-scraper`); `varied_test` separately 4 DUE (one-off axis); `checks-due --all` 1 DUE (`check-dead-endpoint-docs`, not taken this cycle -- BUILD slot stayed on the fleet rotation); `inbox-triage`: 2 owner threads re-read (Apify token rotation, $36 Payouts confirmation) and reconfirmed already fully resolved in prior cycles, no reply owed; new SEO/directory-listing/DMARC/vendor-pitch mail (myslop.shop, Auctra MCP-gateway cold pitch, 3 DMARC reports) all routine, no action; all 3 services active, 4 routes 200; git clean before starting.
  - **Targeted a cluster no prior rotation of this type had touched.** c2561/c2897 covered the `maxReviewsPerApp`-ceiling (`depthAtCeiling`) and `RATING`-sort (`ratingSortUnreachable`) remedy classes; neither ever checked the `emptyApps` cluster's own remedy text (`main.js:810`/`930`: *"Google Play returned zero reviews for country=X lang=Y (try a different country/language, not a scrape failure)"*).
  - **Live-tested it for $0 (vendored `google-play-scraper` lib, no Actor run, no key):** found a real Play Store app with literally 0 total reviews (`com.betabox.localchurch` -- `app()` returns an empty rating histogram, no `.ratings`/`.reviews` field) and ran `reviews()` on it across 5 very different `country`/`lang` combos (us/en, gb/en, in/hi, de/de, jp/ja) -- 0 rows every time. Cross-checked on two apps that DO have reviews everywhere (`com.spotify.music`, `com.jio.myjio`, India-only) across 3-5 combos including nonsense codes (`country=zz`/`lang=zz`) -- identical counts every time, no variation at all.
  - **Read why: `node_modules/google-play-scraper/lib/reviews.js` sends `lang`/`country` only as `hl`/`gl` query params on the `batchexecute` RPC, which always calls the same `qnKhOb`/`UsvDTd` review feed** -- there is no code path by which varying them changes which reviews exist for a given app.
  - **Not shipped this cycle -- evidence is suggestive, not airtight** (2 apps tested, not exhaustive; the one untested case -- an app with many reviews in one script/language and genuinely 0ish in another locale's rendering -- could still make the remedy sometimes true). Exact next step filed as `NEW c3571` below rather than guessed at under time pressure.
  - Updated `state/audit_dates.json` (surgical 2-line edit, re-validated as JSON after writing; confirmed via `bin/audit-due --type unreachable_remedy` that the Actor dropped off the DUE list, 5 -> 4, next target `us-federal-awards-scraper`). `bin/revenue` unchanged (27 public Actors, 54 users, $0 booked) -- no buyer signal, no owner email owed. $0 spent, 0 new Actors today (2026-11-22). All 3 services active, 4 routes 200 before and after.
  - **Next (BUILD slot): `unreachable_remedy` has 4 DUE -- `us-federal-awards-scraper` oldest/NEXT TARGET, then `fda-recall-scraper`, `federal-register-scraper`, `clinicaltrials-scraper`. Also still open: `NEW c3571` (this cycle's filed fix, below), `NEW c3568(c)` (UNRESOLVED drill-down regex, do not close without new evidence), `NEW c3548` (null-date ordering, `fec-campaign-finance-scraper`), and the LOW comment-drift follow-up on `uk-find-a-tender-scraper:324-326`.** **Next (QUALITY slot): `tasks/queue.md` is TRIM DUE again (this block adds back the usual ~4-5KB) -- also 1 FLEET CHECK DUE (`check-dead-endpoint-docs`), not yet run.**

- [x] **SHIPPED c3572 (build 0.1.116) -- NEW c3571 -- `google-play-reviews-scraper`, exact fix for the next BUILD slot to take (or decline with a stated reason, same as c2894-c2896 did for `trademark-search-scraper`).** Before touching the live message, first settle the one open question cheaply: when `reviews()` returns 0 rows for an app (`main.js:808-810`), check whether `app()` was already fetched this run (`includeAppDetails || genresWanted.size`) -- if so, its response is already in scope and carries `.reviews`/`.ratings` (verified live: a 0-review app has NEITHER field; a reviewed app has both, as real numbers). If `app()` was NOT already fetched, add ONE extra `gplay.app({appId, lang, country})` call gated on `data.length === 0` only (rare path, not per-app overhead on every run) wrapped in try/catch (swallow failure, fall back to the current wording -- never let a details-lookup failure block or change billing). Then: if `!app.reviews` (no total review count at all), replace the `main.js:810` log line and the `main.js:930` `causes.push(...)` clause with wording that does NOT suggest country/language will help (e.g. "this app has no reviews on Google Play at all right now, in any country/language -- not a scrape failure"); otherwise (the app DOES have reviews somewhere) leave the existing "try a different country/language" wording in place, since that is the one case this cycle's evidence could not rule out. Verify with: (a) the `com.betabox.localchurch` zero-review repro from this cycle (now expect the NEW wording), (b) a regression check that a normal multi-review app's `emptyApps` path (if reachable at all -- may need a synthetic bad case) still gets the OLD wording, (c) `node --check`, `check-zero-row-message`, `check-charges`, local `test_input.json` happy-path unregressed. Ship as one build if clean; if the `app()`-already-fetched vs fresh-fetch branches turn out to interact awkwardly with `genreSkippedApps`/`genreUnknownApps` (which `continue` before reaching the reviews() call), re-read that control flow carefully before assuming the extra call is reachable in both branches.

- [x] **CLOSED c3570 -- QUALITY slot (3570 % 3 == 0): ran the overdue `tasks/queue.md` trim, rotation lever only. 189.9KB/983ln -> 179.6KB/973ln, ~2c -> ~4c of MEASURED headroom, verified lossless in-memory (859 non-blank lines) before writing.** Preflight fresh: `check-doc-size --all` `tasks/queue.md` **TRIM DUE 189.9KB/983ln, ~2c headroom** (took it); `STATUS.md` OK (59.4KB/167ln, ~32c headroom); `LEARNINGS.md` OK; `checks-due --all` **1 DUE NOW: `check-source-endpoints`** (ran it, see below); `audit-due --all` 5 `unreachable_remedy` + 3 `varied_test` rotations DUE (all BUILD-slot work, left); `inbox-triage new` NONE UNTRIAGED (85 msgs; re-confirmed, including the owner's buyer-signal and Apify-token threads, both pre-existing/closed); all 3 services active, 4 routes 200; git clean before starting. **Fresh per-block census off the `^- \[x\] \*\*CLOSED c3\d\d\d -- (BUILD|QUALITY|GROWTH) slot` regex: 8 live report-shaped blocks, in file order c3568, c3569, c3567, c3566, c3565, c3564, c3563, c3562.** Note for the next rotation: the top-of-file order is NOT strictly newest-first this time (c3568 sits above c3569, because c3569's closure block was inserted directly below the c3568 finding it was shipping, not re-prepended above it) -- but it is still true that the 5 HIGHEST cycle numbers occupy the top 5 FILE positions, so "oldest 3 by file position" and "lowest 3 cycle numbers" agreed (c3564, c3563, c3562). Verify this match explicitly next time rather than assuming position==chronology. Archived those 3 (one contiguous span, lines 21-29, including the internal blanks between them) to `tasks/queue_archive.md` under `## Archived by cycle 3570`; kept the newest 5 (c3568, c3569, c3567, c3566, c3565), landing at the RULE 6b floor (5 + this cycle's own block = 6). **Boundary handled proactively** (per the c3567 lesson): cut through the cut-span's own trailing blank (line 30) so only the blank above the cut (c3565's trailing separator) survives before `NEW c3548` -- no double-blank bug. Script `bin/_trim3570q.py` (clone of `_trim3567q.py`'s boundary-assert/dry-run/`--write` shape), dry-run before `--write`, kept on disk. **3-pass hazard grep clean:** (a)/(b) fleet-wide `grep -rn 'c3564\|c3563\|c3562'` across `notes/` and `state/` found only historical-narrative/provenance mentions (`LEARNINGS.md:7353`, a `state/fleet_checks.json` note describing an unrelated c3564 QUALITY-slot STATUS.md rotation by name), none a live pointer into the cut blocks' own content; (c) the intra-file pass found the same kind of historical narrative inside the retained `c3567` block's own text (describing its own prior census), not a dangling reference. `check-doc-size` re-read after writing still prints TRIM DUE (179.6KB, ~4c measured headroom, 24c-ahead projection 307KB past the 200KB line) -- expected per repeated precedent, not a failed trim. **Also ran the DUE-NOW fleet check `check-source-endpoints`: CLEAN** -- 50 unique hosts probed, 0 baselines set, 0 DEVIATION; the 3 EXEMPT Actors (google-play-reviews-scraper, shopify-products-scraper, website-screenshot-scraper) unchanged. Recorded via `bin/checks-due --ran` (3545 -> 3570, next due 3594). `bin/revenue` unchanged (27 public Actors, 54 users, 1524 runs30d, 0 bookmarks, 0 reviews, $0 booked) -- no buyer signal, no owner email owed. $0 spent, 0 new Actors today (2026-11-22). All 3 services active, 4 routes 200 before and after.
  - **Next (BUILD slot): `unreachable_remedy` has 5 DUE -- `clinicaltrials-scraper`, `fda-recall-scraper`, `federal-register-scraper`, `google-play-reviews-scraper`, `us-federal-awards-scraper` (take the oldest per `audit-due --type unreachable_remedy` fresh). `varied_test` separately has 3 DUE (`hacker-news-scraper`, `trademark-search-scraper`, `us-federal-awards-scraper`, one-off axis, informational).** Also still open: `NEW c3568(c)` (UNRESOLVED drill-down regex, do not close without new evidence), `NEW c3548` (null-date ordering, `fec-campaign-finance-scraper`), and the LOW comment-drift follow-up on `uk-find-a-tender-scraper:324-326` (land in the SAME push as the next change to that file, never alone).**
  - **Next (QUALITY slot): re-measure `tasks/queue.md` fresh -- rotation lever bought ~4c of measured headroom again this cycle (it was NOT actually at the RULE 6b floor, contrary to c3569's handoff note: 2 more BUILD-slot cycles had added 2 fresh blocks since the floor was last hit at c3567, giving the rotation lever room to run again). The per-SPAN RELOCATION lever (`NEW c3372`/`NEW c3162`/`NEW c3046`/`COMPRESSED c2994`, pre-censused c3552, still unspent after 6+ cycles) remains available if a future rotation ever lands back at the floor with insufficient headroom.** `STATUS.md` has ~32c headroom, nothing needed there for a while.

- [x] **CLOSED c3568 -- BUILD slot (3568 % 3 == 1): ran the oldest DUE `unreachable_remedy` rotation on `google-news-scraper` (3222 -> 3568, 346c gap). FOUND 2 REAL DOC-LEVEL OVERCLAIMS + 1 unresolved question, all written up as `NEW c3568`; $0 spent, no build, no code change.** Preflight fresh: `audit-due --all` 4 FLEET ROTATIONS DUE, all `unreachable_remedy` (`google-news-scraper` oldest at 346c, then `us-federal-awards-scraper`/`fda-recall-scraper`/`federal-register-scraper`); `varied_test` still DUE on `trademark-search-scraper` (one-off axis); `checks-due --all` NONE DUE (soonest `check-source-endpoints` in 1c); `inbox-triage new` NONE UNTRIAGED (85 msgs); `check-doc-size --all`: `tasks/queue.md` TRIM DUE 183.9KB/972ln ~3c headroom (QUALITY-slot work, left -- c3567 just ran the rotation lever), `STATUS.md` OK (50.9KB/143ln, ~34c headroom), `LEARNINGS.md` OK (7367ln, ~32c); all 3 services active, 4 routes 200; git clean before starting.
  - **Chose a cluster no prior rotation of this axis had touched.** c2884 and c3222 both worked the date-window/`windowNote` cluster; c3222 spot-checked the topic enum's GATE but never the two REMEDIES the `badTopics` warning (main.js:41) hands a buyer whose code we rejected. That warning is the whole axis in one sentence, so it was the right target.
  - **Enum and gate both still sound, 2736 cycles after the c832 claim.** All 20 `VALID_TOPICS` curled live: every one HTTP 200 with a non-empty feed (47-70 items, POLITICS lowest at 47). The 5 sampled "probed and are NOT sections" codes (NFL, CLIMATE, SPACE, CRIME, TRAVEL) plus BOGUSCODE123 all return HTTP 200 with ZERO items -- no Top-Stories fallback, so the "don't re-add them" list is still accurate. **Method note for the next rotation: `grep -c "<item>"` counts LINES, and a Google News feed is one long line, so it reports 1 for a 70-item feed and 0 for an HTTP 429 -- my first pass read 4 healthy topics as empty. Use `grep -o "<item>" | wc -l` AND print the HTTP code; this box gets 429-ed by news.google.com after ~5 rapid requests, so pace them (4s apart, retry 429 after 20s).**
  - **Remedy B verified reachable for ordinary sections** -- harvested hashes the way a buyer does (the `/topics/<HASH>` links in news.google.com/home's own server-rendered nav), then `/rss/topics/<HASH>`: Sports -> 200/70 items/channel "Sports - Latest - Google News", Health -> 200/70. c1798's claim holds.
  - **But Local news 404s, and the schema promises it doesn't.** Full evidence + the exact fix wording are in `NEW c3568` (a) and (b); the geo feed (`/rss/headlines/section/geo/<PLACE>`, 200/70 items for San Francisco and Chicago) is a reachable remedy that already works through the existing `rssUrls` field with zero code change and is named nowhere in our docs. The drill-down-regex question is logged UNRESOLVED in (c) rather than closed either way -- Rule 7 forbids the headless browser that would settle it.
  - Updated `state/audit_dates.json` (surgical 2-line edit, JSON re-validated after writing), `tasks/queue.md`, `state/STATUS.md`; appended the lesson to `notes/LEARNINGS.md`.

- [x] **CLOSED c3569 -- BUILD slot (3569 % 3 == 2): shipped both `NEW c3568` (a)+(b) doc-only fixes to `google-news-scraper` in ONE push (package.json 0.1.35 -> 0.1.36, platform build 0.1.110, ~$0.005).** Re-verified both dated upstream facts fresh first: Local topics page still 200/1.7MB (via a consent-redirect hop; this box's IP got geo-flipped to DE without cookies, unrelated to the finding), `/rss/topics/<same hash>` still 404; geo feed still 200/70 items for San Francisco and Chicago. Softened `topicsHashed`'s `input_schema.json` description (no longer claims "every section Google has"; now names Local news as the known gap and points at the geo feed), added a geo-feed clause to `rssUrls`' schema description, matching README input-table clauses, a new README FAQ entry ("How do I get local news for a city?"), and a geo-feed pointer on the `badTopics` warning (`main.js:41`). Verified live post-push via the build API: both schema descriptions read back exactly as shipped, README contains `geo/`. `enum-canary` re-run (schema changed): CLEAN, `timePeriod` 9/9 exact. `check-readme-samples` re-run: 0 new drift (1 pre-existing unrelated drift on `ats-jobs-scraper`). No output-field change, so `check-registry-fields`/`check-meta-fields` don't apply. Updated `state/audit_dates.json` via a surgical `str.replace` (not `json.dump` -- a first attempt with `json.dump` reformatted the whole 740-line file via an indent mismatch; reverted and redid it as a 2-line textual diff, re-validated as JSON after). All 3 services active, 4 routes 200 before/after.

- [ ] **NEW c3568(c) -- carried forward, UNRESOLVED, do NOT close as clean without new evidence -- the drill-down regex on `google-news-scraper`.** `main.js:45-46` claims `TOPIC_HASH_RE` accepts "any of its path shapes, e.g. the `.../topics/<HASH>/sections/<SECTION>` drill-down". Re-ran the live regex in node at c3568: a drill-down URL yields ONLY the parent hash and the `/sections/<SECTION>` half is dropped **silently**, so such a buyer would be served and charged for the PARENT section's feed while believing they asked for the sub-section. Whether any buyer can actually produce such a URL is UNPROVEN: on the live Sports page the sub-sections (NFL, NBA, MLB, NHL, NCAA Football/Basketball, Soccer, NASCAR, Golf, Tennis, WNBA) render as `role="tab"` buttons with no `/topics/` href at all (0 `/sections/` links in 4.3MB of HTML), and their internal jslog panel tokens HTTP 400 on both `/topics/` and `/rss/topics/`. Rule 7 forbids a headless browser on this box, so the address-bar shape could not be settled here. Cheapest next probe that does NOT need a browser: look for a `/sections/` URL in Google News' own sitemaps/AMP output or in a non-US `ceid`, or ask whether `/rss/topics/<P>/sections/<S>` answers 200 for any `<S>` harvested elsewhere. If a drill-down URL IS reachable, the right fix is to WARN when the regex drops a `/sections/` suffix (never silently downgrade a paid feed), not to try to support it.

- [ ] **NEW c3548 (MEDIUM -- measured upstream regression, documented in code but not yet acted on) -- `sort_nulls_last=true` is a NO-OP on the FEC's schedule_a endpoint, so contributions walks return the NULL-contribution-date block FIRST instead of last.** Proved live c3548 with two otherwise-identical requests (unfiltered, `two_year_transaction_period=2026`, `sort=-contribution_receipt_date`, `per_page=5`) differing only in whether `sort_nulls_last=true` was sent: **byte-identical results and identical `last_indexes`** (`{"last_index":"4010720261300203647","sort_null_only":true}`), all 5 dates `null` either way. This is a silent upstream regression of the ORDERING half of the cycle-856 fix (`src/main.js` ~878-885 schedule_b note + the schedule_a caveat comment added c3548). **Not a data-loss bug** -- the other half of that fix (echoing `sort_null_only` back in the cursor) still works, confirmed by the 2,000-row walk crossing into dated rows on page 4, so no rows are stranded. **Why it still matters to a buyer:** on a broadly-filtered contributions run with a small `maxResults` (default 20), the rows delivered and CHARGED FOR can be entirely dateless, amount-less partial filings -- the least useful slice of Schedule A. That is now the stated rationale for keeping guard (a), but guard (a) only covers the *fully* unfiltered case; a weakly-filtered run (e.g. `state: "CA"` alone) hits the same thing with no warning. **Options to weigh, none yet chosen:** (1) verify how far the null block extends under a realistic weak filter before deciding anything (cheap, ~5 calls, do this FIRST -- it may be short enough to ignore); (2) check whether `min_date` set to an early in-period date excludes the null-date rows upstream for free, which would be the clean fix; (3) emit a `RUN_SUMMARY` field + one `log.warning` when a high fraction of delivered rows have a null date, so the buyer at least knows why; (4) re-test `sort_nulls_last` periodically in case FEC restores it. Do NOT client-side-drop null-date rows -- they are real filings and dropping them after fetch would mean charging for rows we discard, or silently shrinking a paid result set. Note the FEC rate limit on our key is **60/hour**, so budget probes.

- [ ] **NEW c3544 (LOW) -- `ats-jobs-scraper` README:200 and README:203 still describe our own platform count as 7 ("the real 7-ATS rivals", "covers 5 of our 7 platforms"); it is 12.** Found by `check-own-source-count` adjacently (the checker only flags phrases next to a structured source list, so it did not flag these and will not catch them later). **Do NOT just substitute 12 for 7** -- each sentence states how many of OUR platforms a specific rival covers, so the fix needs a per-rival recount against the current 12-entry `SUPPORTED_ATS` (`src/main.js:14`), read from each rival's live listing, and that number must not be guessed. Rivals named in those two paragraphs: `softyways/greenhouse-lev...`, `openclawai/career-site-ats-jobs-scraper`, `wickfeed/ats-job-aggregator`, `webdata_labs/greenhouse-lever-ashby-jobs-scraper`, `automation-lab/multi-ats-jobs-scraper`. A QUALITY/GROWTH-slot job (live listing reads + one README-only push), and worth checking whether `competitor_audit` on this Actor should own it rather than a one-off note.

---

- [ ] **NEW c3536 -- fold the "grep every mention of the field, not just one surface" cross-check into the `enum_audit` procedure in `notes/PLAYBOOK.md`.** Cheap, $0, no network, and it found a 25-day-old false claim this cycle that three prior audits of the same Actor had walked past (c2861, c3198, and the commit that introduced it). The rule: when an `enum_audit` touches a field, `grep -n "<field>" README.md` and read EVERY hit -- a field table and its FAQ prose can disagree, and two mentions that disagree is a finding needing no live probe and no build to discover. Also worth stating the companion test this cycle established: before filing a wrong claim as "drift", run `git log -S` on BOTH the claim text and the feature it describes -- if the claim is NEWER than the feature, it was wrong on arrival, which means a date stamp/cadence is the WRONG remedy. Do this in a QUALITY slot alongside other PLAYBOOK work; it is a doc edit, no push.

- [ ] **NEW c3523 (LOW) -- complete `nih-reporter-scraper`'s README `awardTypes` legend (line 57), sourced from a primary NIH document, not a search summary.** Current text documents only codes 1/2/3/5 of the schema's 9-value enum, trailing `...`. This cycle's `enum_audit` confirmed those 4 against NIH's own ExPORTER data dictionary (verbatim, via a GitHub mirror + web search) and additionally found reasonably-sourced text for 3 more: `4 = Competing extension for an R37 award, or first non-competing year of a Fast-Track SBIR/STTR award`, `7 = Change of grantee institution`, `9 = Change of NIH awarding Institute or Division (on a competing continuation)`. **Codes 6 and 8 are NOT yet safe to ship** — the only source found was a single AI-generated search-engine summary (no primary NIH citation), and the two candidate primary PDFs (`api.reporter.nih.gov/documents/Data Elements for RePORTER Project API_V2.pdf`, UMich IRIS's `2020_Data_Dictionary.pdf`) both failed to parse via `WebFetch` (compressed/garbled text layer) — UMich's URL also 403'd on a second direct fetch. Before adding 6/8: try `curl`-ing the PDFs directly and running a local PDF text extractor instead of `WebFetch`'s AI summarizer (may recover the table where the summarizer couldn't), or search `grants.nih.gov`'s SF424 application-type guidance directly. If a primary source still can't be found after a real attempt, ship 1/2/3/4/5/7/9 only and leave 6/8 out of scope — do not guess at their wording from a single unsourced summary.

- [x] **CLOSED c3518/c3520/c3529 -- all handles closed.** ~~`trademark-search-scraper:164` `logiover/tripadvisor-scraper`~~ -- **DONE c3529** (build 0.1.117). ~~`uk-find-a-tender-scraper:144`/`:164`~~ -- **DONE c3520** (build 0.1.109). ~~`us-federal-awards-scraper:225` `logiover/usaspending-gov-scraper`~~ -- **DONE c3529** (build 0.1.96). `NEW c3456`'s vendor-wide `logiover` tracking item should drop these 2 as closed when next touched.
- [ ] **NEW c3516 (TRIVIAL/method, HIGH value for its cost -- a NEW member of the `NEW c3372` truncated-output family, and the old rule does NOT catch it).** `NEW c3372` says: *"don't pipe a bare checker run through `head` -- it SIGPIPEs the sweep mid-file and a missing `N checked, N flagged` footer means the run did not finish."* **That rule made `tail -N` look safe, and it is NOT.** `tail` reads to EOF, so the sweep completes, the footer IS printed, and the output passes the footer test -- while `tail` has silently discarded the FIRST N lines. c3516 ran `check-competitor-claims 2>&1 | tail -60` against a 69-flag fleet sweep and lost the first 10 lines, including the whole fleet-wide USER-COUNT stale section that `check-competitor-claims` prints BEFORE its paragraph section; the footer read `332 checked, 69 undated/stale` and looked perfectly complete. **RULE: never truncate a checker run at either end. Redirect the full output to a file and read the file** (`./bin/check-competitor-claims > /tmp/cc.txt 2>&1; wc -l /tmp/cc.txt`), or background it and read the captured output file. **The tell that would have caught it: the footer's own count did not match the number of flag lines visible (69 claimed vs 59 shown). Cross-check the footer count against the lines you can actually see -- the footer being PRESENT is necessary, not sufficient.** The c3516 gap was partly repaired with a targeted `--only app-store-reviews-scraper` re-run (recovering its 7 paragraph flags, plus 5 superlative-guarded stale user-counts: `thewolves` 3153->3533, `johnvc` 647->726, `apihq` 38->43, `lergassy` 24->32 x2), but **the FLEET user-count result for the c3516 run remains UNKNOWN** -- the next cycle to touch competitor claims should re-run the full sweep to a file before trusting any user-count claim to be clean. Fold this rule into `NEW c3372`'s method paragraph at its next compression. **SECOND c3516 slip, same note so it costs no extra block: I deleted `bin/_trim3516q.py` after a successful `--write`, conflating the `_trimNNNNq.py` convention with the `_triageNNNN.py` one. `_triageNNNN.py` pricers ARE deleted after use; `_trimNNNNq.py` trim scripts are KEPT (`bin/_trim3510q.py`, `bin/_trim3513q.py`) because the next trim clones the most recent one, and both `CLOSED c3516` and `state/STATUS.md` cite it by name. It was never committed, so it was unrecoverable from git and was RECONSTRUCTED from the authoring session with a PROVENANCE WARNING docstring; its four long replacement strings now read themselves back out of the live `queue.md` instead of re-pasting ~14KB of prose. It correctly fails at its first anchor assert when re-run against the post-trim file, so it is a template to clone, not a re-runnable artifact. **RULE: commit a trim script in the same commit as the trim it performed, and never `rm` a `_trim*` script.**


- [ ] **NEW c3514 (LOW -- a real feature gap found during `NEW c3162` vendor-catalogue triage, not yet a build decision).** `nefes-tools/eu-company-jobs` (2u, live, 530+ pre-curated companies across 10 ATS platforms: Greenhouse/Lever/Ashby/Workday/Personio +5 more) and `nefes-tools/workday-jobs` (2u, live, 2,000+ Workday sites) both sell **"search by keyword/country, no company list needed"** -- a buyer who doesn't already know a target company's ATS+slug can still find its jobs. Our `ats-jobs-scraper` has no equivalent: every call requires an explicit `companies` array of `{ats, slug}` pairs (or `ats:"auto"` if you already have the slug but not the platform) -- there is no keyword-only, bring-no-slug mode. Both rivals are still priced at or above us once their start fee is netted in (bucket 3, non-issue on price), so this is a pure feature/discoverability gap, not a price threat. **Action, when picked up:** check whether any inbox mail has ever asked for keyword-only/no-slug search (none has as of c3514) before sizing a build -- it would likely require us to maintain our own pre-crawled company index (the thing both rivals actually did), which is a much bigger lift than a normal README/field addition. File as a candidate for `ats-jobs-scraper`'s next scheduled `competitor_audit` rotation (not due as of c3514 -- `audit-due --all` showed no `competitor_audit` due anywhere), do not action off-cycle.

- [ ] **NEW c3512 (TRIVIAL/content -- a settled live measurement, so nobody re-derives it; it is also a REUSABLE RULE for any future Apple-endpoint work on this Actor).** Apple does **not** use one explicitness field or one spelling. Measured live 2026-11-21: `rss.marketingtools.apple.com` chart feeds carry `contentAdvisoryRating: 'Explict'` -- **misspelled, 30/100 US top shows, and it NEVER emits the correctly-spelled `'Explicit'`**; `itunes.apple.com/lookup?entity=podcastEpisode` carries `contentAdvisoryRating: 'Explicit'`/`'Clean'` (1,368 rows, zero misspellings); and the plain `itunes.apple.com/lookup` carries **`trackExplicitness: 'explicit'`/`'cleaned'`** while `collectionExplicitness` is **permanently `'notExplicit'`** -- it read `'notExplicit'` on 16/16 shows including all 12 that Apple's own chart rates explicit. Consequences: (a) `main.js:660`'s `collectionExplicitness === 'explicit' || trackExplicitness === 'explicit'` has a **DEAD first limb** -- do NOT "simplify" it by dropping the `trackExplicitness` half, and do not add a `collectionExplicitness`-only test anywhere; (b) do NOT "fix" the `'Explict'` spelling at `main.js:1290` -- it is Apple's typo, not ours, and removing it breaks explicit detection on the whole charts-without-`includePodcastInfo` path; (c) any NEW code reading explicitness must be told which endpoint it is reading first. All three current tests were verified correct this cycle, so **there is nothing to fix here** -- this exists only to stop a future cleanup from breaking one.

- [ ] **NEW c3492 (TRIVIAL/method, earned by two bugs in one script -- read before cloning any `_trimNNNN*.py`).** (1) **Verify in MEMORY, then write.** `bin/_trim3492q.py` appended the archive and wrote the queue before its lossless check, so when the check failed both files were already modified and the run could not simply be retried (a re-run would double-append the archive header). Build the new archive text as a STRING, run every assert against it, and only then open files for writing -- the docstring records this, and the rotation script in `CLOSED c3492` does it in the correct order. (2) **Never use `is` to exempt a rewritten line from a lossless check.** The exemption compared identity against strings the verify loop re-creates via its own `orig.split()`, so it never matched. Compare by VALUE. Both fixed in `_trim3492q.py` in place, with the correction noted at the fix site.
- [ ] **NEW c3492 (LOW/bookkeeping -- a pointer, so nobody re-discovers it as breakage).** Live cross-references to `c3483`, `c3484` and `c3486` remain in several blocks (notably `NEW c3483`, `NEW c3484`, `CLOSED c3487` and `STANDING c3280`), but those three `CLOSED` blocks were archived by the c3492 rule-6b rotation. **They resolve to `tasks/queue_archive.md`, `## Archived by cycle 3492 (rule-6b report-block rotation)`** -- the file's normal convention after every rotation, NOT dangling-pointer breakage. Refs were deliberately left unedited rather than spending bytes on inline "(archived)" markers.

- [ ] **NEW c3488 (MEDIUM -- roll `up.cheap_legs` into the remaining `_batch_price_*.py` pricers, ONE PER COMPETITOR_AUDIT, as each niche comes due. Do NOT do them all in one cycle.)** c3488 added `cheap_legs(events, ours_floor)` to `bin/_unit_price.py` and wired it into `_batch_price_apc2.py`; c3490 wired a 2nd, `_batch_price_fedreg2.py`; **c3491 wired a 3rd, `_batch_price_sgos3.py`** (verified live: scan found 6 vs `below_floor`'s 4, both extras correctly hand-ruled non-issues -- see `CLOSED c3491`). Every other pricer in `bin/_batch_price_*.py` still closes with a summary line derived from `unit_price`'s single selected event, which is the exact under-report c3488 measured at 3x (banner said 1 exposure, truth was 3). **The rollout is deliberately lazy, not a sweep:** wire it into a niche's pricer on the cycle that niche's `competitor_audit` is due, because that is the only cycle where the output can be checked against a hand-read of the same cohort -- a blind fleet-wide edit would ship 30 unverified summary lines and the whole point of the finding is that an unverified summary line is what failed. The wiring is 2 small hunks, copy them verbatim from `_batch_price_apc2.py`/`_batch_price_fedreg2.py`/`_batch_price_sgos3.py` (the persisted `cheap_legs` field inside the `out.append({...})` dict, and the `cl = [...]` + print block after the existing banner). **`uk-find-a-tender-scraper`'s rotation ran at c3494 but did NOT wire this in (time ran out) -- its pricer, `bin/_batch_price_uktft3.py`, is still unwired, and unlike the other 3 niches this one has a TIERED own-price ladder (not flat), so the wiring diff will need to compare `cheap_legs()` against OURS_TIERS per-tier rather than a single floor scalar -- read `_batch_price_sgos3.py`'s tiered-comparison branch (if any) or adapt from scratch.** Next due by `audit-due --type competitor_audit` is `trademark-search-scraper` (already DUE) -- check `audit-due --type competitor_audit` fresh each time rather than trusting this list. Note the helper issues NO verdict by design, so the hand-read is still owed every time -- c3488's own scan printed 4 listings where only 3 were real exposures, the 4th being a lead-gen rival whose cheap events are not data rows; c3490's printed 2 where only 1 was real, the 2nd billing a different UNIT entirely (a watch-cycle fee, not a per-document rate); c3491's printed 6 where only 4 were real, the 2 extras both billing a different-dataset (USAspending vs SAM.gov) secondary event -- three different near-miss shapes now on record, read all three before trusting a raw cheap_legs count as a verdict.

- [ ] **NEW c3488 (LOW, date/size-gated -- do nothing until the next `apple-podcasts-scraper` competitor_audit, ~c3824).** `actors/apple-podcasts-scraper/README.md` is now **86,970 bytes** after this cycle's resweep paragraph (was ~82KB). The last three competitor_audit paragraphs have each added ~4-5KB, so **the next one will very likely cross 95k**, at which point this Actor joins the versions-route-only README verification set described in `NEW c3148` -- `GET /v2/actor-builds/{id}`'s `actorDefinition.readme` truncates at ~100k and would silently report a false byte-identical match. c3488's own verification was still safe via the build record (86,970 both sides, sha match) and that is recorded so the next cycle does not re-derive it. **At that next audit, verify the push via `GET /v2/acts/{id}/versions` -> `items[].sourceFiles[]` -> the `README.md` entry's `content` instead**, same as `remote-jobs-scraper`, `sam-gov-opportunities-scraper` and `fda-recall-scraper`. Re-measure the byte count first; do not act on this paragraph's number.

- [ ] **NEW c3488 (TRIVIAL/checker precision -- a KNOWN FALSE POSITIVE, do NOT "fix" the README prose it flags).** `bin/niche-size apple-podcasts-scraper` prints `README claims: 30 (DIFFERS by +208) -- 'All 30 listings'` against its own 238 matched. The README sentence it scraped is **historically correct and must not be edited**: it reads "All 30 listings priced at cycle 2816 are now named above", a closed statement about that sweep's cohort, not a claim about the current size of the niche. The claim-extractor matches `All N listings` without reading the cycle qualifier after it. Bias is harmless (it over-reports a difference, it cannot hide one), so this is filed to stop a future cycle spending time "reconciling" the two numbers or deleting a true sentence. If the extractor is ever tightened, the discriminator is a `at cycle NNNN` / `priced at cycle` qualifier inside the same clause.

- [ ] **NEW c3488 (LOW -- a real feature gap, measured, not yet a decision).** `actorfactory/apple-podcasts` (found in this cycle's sweep) ships **chart rank-change tracking** (`trackChartChanges`, `monitorStoreName`, `includeDroppedShows` -- "also list shows that left the chart") against our `charts` mode, which returns a flat snapshot only. Our `watchLabel` watch mode is **episodes-only** (verified against our own live input schema this cycle), so a buyer asking "which shows entered or dropped out of the Business top 100 since last week" cannot be served by us at all today -- and `sourabhbgp`'s `trackDeltas` (already named in our README) does the same thing, so this is the second rival with it. The shape is close to what c3484 already shipped for `ats-jobs-scraper` (`watchEvents: ["closed"]` diffing disappearance against the fetcher's own output), so the design is largely precedented: diff chart membership per (country, genre, chartType) against a persisted baseline, bill the existing `result` event, make it opt-in. **Not started, and NOT a build commitment** -- file it as a candidate for a BUILD slot and check first whether any inbox mail has ever asked for chart deltas (none has as of c3488).

- [ ] **NEW c3488 (TRIVIAL -- a pre-existing checker DRIFT line that is NOT mine and NOT yet adjudicated, filed so the next cycle to run `check-readme-samples` does not re-discover it cold).** `bin/check-readme-samples` reports exactly 1 drift fleet-wide: `DRIFT ats-jobs-scraper:191 prose bullet names 'closed' -- not a declared input or output field`. It dates from c3484, which shipped the `watchEvents: ["closed"]` feature on that Actor: `closed` is an **enum VALUE of the `watchEvents` input array**, not a field name, so the checker's "declared input or output field" test cannot see it and this is very likely a false positive rather than a missing field. **Do not edit the README prose on the strength of this line alone** -- first confirm against `ats-jobs-scraper/.actor/input_schema.json` that `watchEvents` declares `closed` in its enum (c3484 recorded `enum-canary` as OK with 3 values in exact order, so it should), and if so the fix belongs in the checker (teach the prose-bullet test to accept an enum value of a declared array input), not in the Actor. Cheap either way; it is the only drift in 41 sample blocks / 107 prose bullets / 756 type-checked values.

- [ ] **NEW c3483 (MEDIUM -- the one `tasks/queue.md` trim lever nobody has spent yet; COMPRESSED c3504, full text verbatim in `tasks/queue_archive.md`, `## Archived by cycle 3504`. Its original headline finding -- "the rotation lever is UNAVAILABLE, only 3 blocks to rotate" -- is RETRACTED: it was already half-withdrawn by its own `UPDATE c3484`, and c3504 re-derived 18 report blocks and rotated 13. Re-derive that count fresh every time; never forward it.)** What survives is the lever c3483 established by reading, and c3504 did not spend: **~15 single-paragraph `TRIVIAL`-tagged notes (`grep -n 'TRIVIAL' tasks/queue.md` for the live list), roughly 13-15KB.** **They are NOT safe to bulk-archive** -- most exist specifically to stop a future cycle re-making a known mistake (a checker false positive, a settled fact, a wrong command), and `queue_archive.md` is not read routinely, so archiving one reintroduces the exact regression it prevents. **Each needs an individual live-check before it can be cut: has the underlying condition changed (checker fixed, Actor retired, date trigger fired, fact re-verified false)?** Close only the ones that come back "yes, no longer needed" -- never infer staleness from age. Budget real time; it is item-by-item, not a script.

- [ ] **NEW c3476 (LOW -- two small residues from closing the `competitor_audit` rotation on `hacker-news-scraper`. The rotation itself is STAMPED at c3476 and is NOT owed again until ~c3812, so do NOT re-run a sweep to "finish" this item. The paragraph-staleness residue is filed under `NEW c3372` instead, not here.)**
  (a) **The nineteenth sweep's cohort is a FLOOR, not a census, and the next sweep should not read its "0 head-on whole-ladder undercutters out of 360" as a clean census.** `bin/niche-unnamed` printed its POSSIBLY TRUNCATED warning on **all 22** search terms -- every term returned fewer items than its own `total` field (`hacker news` 674 of 853, `hackernews` 617 of 791, `hn search` 367 of 441, `hn api` 406 of 509, and so on, ~20-25% short across the board). This is the already-documented undiagnosed Store paging gap, not a sweep error, and the README says so in its own text, so nothing is overclaimed -- but it means ~130-180 matchable listings in this niche were never priced. **Do not spend a cycle trying to fix the paging gap from this Actor's side** (it is a platform-wide `GET /v2/store` behaviour affecting every niche's sweeps equally, and c3001 already recorded that the c1780 `limit=1000` fix is itself no longer sufficient). The useful follow-up, if any, is the generic one: a paging/recall diagnosis in `bin/niche-size` that would lift recall for ALL 27 niches at once, which is worth a real QUALITY slot and is NOT specific to `hacker-news-scraper`.
  (b) **`fluyeporlaweb/hacker-news-scraper` was found 404 and UNDISCLOSED at README:188 -- fixed in place this cycle, but the CLASS of gap it belongs to is still open fleet-wide.** That handle carried no explicit user-count claim, so `check-competitor-claims` never liveness-checked it; only the separate `check-handle-liveness` pass caught it. This is exactly the standing **c2816 gap** that `NEW c3456` item (a) is already tracking for `logiover`, and this cycle's fleet-wide `check-price-superiority` run still prints **10 named handles 404 and not yet disclosed** (plus 135 suppressed because the README already says so). Fold this finding into that item rather than opening a parallel track -- the method is identical (disclose in place with the 404 date, never delete a dead rival's dated claim silently) and the economical move is still to batch each Actor's dead handles into its own next README push rather than paying a build per handle. Worth noting for whoever picks it up: `fluyeporlaweb` was a **single-listing** removal with a live, pivoted owner account (7 Spanish public-procurement listings, zero HN products), which is a third disposition distinct from `crawlerbros`-style whole-account removal and `rbbscrap`-style rename -- so check the owner account before writing "whole-account removal".

- [ ] **NEW c3464 (MEDIUM -- one follow-up remains from closing the `competitor_audit` rotation on `google-play-reviews-scraper`; the rotation itself is STAMPED at c3464 and is NOT owed again until ~c3800, so do not re-run a sweep to "finish" this item). Item (b) RESOLVED at c3465, see below -- only (a) is still open.** **A real 15-term FULL-COHORT resweep is still owed on this Actor and nobody should read c3464 (or c3465) as having done one.** c3464 ran only a single-term `google play reviews` Store query (20 listings) to answer the rotation's new-entrant question, found 4 unnamed listings, priced all 4 live and confirmed **0 new undercutters** (all dearer than our flat $0.0001/review at every tier). The **running undercutter total is therefore still 79 as of the c2792/2026-11-06 sweep and was NOT re-derived** -- that number can only move on a real 15-term cohort pass (c2792 priced 352 non-self handles out of 526 matches). The README says so in its own text, so the file is not overclaiming; the gap is just unfinished work. Do this on a QUALITY slot with real time, not as a tail-end task.
  - ~~(b) live user-count discrepancy~~ **RESOLVED at c3465**: pulled `/v2/store` and `GET /v2/acts/<id>` side by side for `thewolves`/`theagents` -- **same field** (2,570/2,570 exact; 866/865, a 1-count live-counter drift between two calls a second apart, not a schema mismatch). The README's 2,433/840 vs today's 2,570/865 was 8 days of ordinary drift sitting inside `check-competitor-claims`' own 10% tolerance, correctly reported as 0 stale. The real defect was narrower: README line 134's "every user count in this sentence re-fetched live 2026-11-20" was only true for 3 of 7 named handles (c3462 had touched `neatrat`/`solidcode`/`code-node-tools` only) -- the other 4 (`thewolves`, `theagents`, `curious_coder`, `automation-lab`) silently carried 2026-11-12 numbers under a false "today" label. Fixed: live-refetched all 4, aligned all 10 mentions across the file, shipped build 0.1.114, live README verified byte-identical, `check-competitor-claims --only` now 0 stale/0 disagreements. Full writeup in `notes/LEARNINGS.md` (cycle 3465 entry) -- a two-endpoint "mismatch" needs a same-moment side-by-side pull before it's trusted as a schema difference, and a blanket "re-fetched live" qualifier covering N handles is a claim per handle, not per sentence.
- [ ] **NEW c3484 (LOW -- three residues from shipping the `closed` watch event on `ats-jobs-scraper`; the feature itself is DONE and live, do NOT re-implement it).** (a) **The `ats-jobs-scraper` `competitor_audit` rotation still owes `lepidata/career-site-jobs` a NAMED mention** -- c3460 said to ship the capability first and let the rotation name the rival, and that is now the state: the code is live but no README sentence names the handle we drew the feature from. Its price half is already filed in the FOLD-IN REGISTER's `ats-jobs-scraper` entry (6), so fold the closed-job-alert half in at the same time rather than as a standalone edit. Note the rival gives closures away at **$0** and we charge the normal `job` rate, so any sentence naming it must disclose that honestly -- the differentiator we actually have is the incomplete-board suppression (it reports closures only from a board that answered in full), not the price. (b) **The positive path has only ever been proven against INJECTED ids, never a posting that genuinely came down.** That is a real gap, not a formality: it means the id-shape and diff logic are proven but "Ashby silently stops listing a filled req" is still an assumption about upstream behaviour. The cheap way to close it is to seed a watch on a board with high turnover, leave the label alone for several days, and re-run -- so it is a two-cycle measurement, not a task to retry inline. Do NOT re-run the injected-id test to "confirm" it; that test is already recorded as passed. (c) **`pagingCutShort` is currently read ONLY by the closure suppression.** The same "paging stopped on the raw cap or the clock with pages unread" condition also silently undercounts a plain non-watch run on SmartRecruiters/Workday, where today it produces no cause line at all (`partial` means something narrower -- a page that FAILED after retries). Worth folding into `pushedCauses()` alongside `cappedCompanies`/`truncatedByMaxResultsCompanies` next time that function is touched; separate defect class from this cycle's work, so filed rather than fixed.

- [ ] **NEW c3458 (LOW, date-gated -- not due until 2026-11-22 or later, do not action early).** `shopify-products-scraper`'s `competitor_audit` rotation (this cycle) found `scrapebench/shopify-change-tracker`'s live `pricingInfos` carries a **not-yet-effective entry starting 2026-11-22** that renames its sole event from "Change detected" ($0.01) to **"License match"** ($0.004, "Charged once per licence returned") -- wording unrelated to Shopify, suggesting the handle may exit this niche entirely rather than cut its price. README corrected to the real current $0.01 and flagged; re-check this one handle live on/after 2026-11-22 and update the README accordingly (either a genuine price-cut disclosure or a delisting-from-niche note) -- full detail in `state/STATUS.md` cycle 3458 entry and `audit_dates.json`'s `shopify-products-scraper.competitor_audit_note`.

- [ ] **NEW c3456 (MEDIUM -- two real cross-fleet findings surfaced by the BATCH 9 preflight, neither in that batch's scope, both verified live this cycle. Do them in QUALITY slots.)**
  (a) **`logiover` has left Apify entirely -- a VENDOR-WIDE delisting, not one dead listing.** BATCH 9 disclosed `logiover/federal-register-scraper` (404) in `federal-register-scraper/README.md:190`, but `check-handle-liveness` reports the same handle 404 in three more places that still name it with no removal notice: `trademark-search-scraper/README.md:164` (`logiover/tripadvisor-scraper`), `us-federal-awards-scraper/README.md:225` (`logiover/usaspending-gov-scraper`), both UNDISCLOSED, plus `court-records-scraper/README.md:207` and `:224` (`logiover/courtlistener-scraper`), both SHARED -- "notice nearby but another handle intervenes, hand-read once". Disclose each in place with the 404 date (the method: never delete a dead rival's claim silently, since the claim is a dated fact about a past sweep). **Fold these into those three Actors' own competitor-claim batches rather than paying four separate build/push cycles** -- `us-federal-awards` and `fec-campaign-finance` are already on the BATCH roster in `NEW c3372`, and `logiover/usaspending-gov-scraper` is ALSO one of the 9 handles `check-price-superiority` prints as "404 on Apify and NOT yet disclosed" (the standing c2816 gap: a count-less mention is liveness-checked by neither `check-competitor-claims` nor anything else). Worth checking the other 8 of those 9 in the same pass.
  (b) **`check-own-price-freshness` has 2 live flags, both `uk-find-a-tender-scraper`: LIVE prices $0.04 and $0.05 appear NOWHERE in its README** (which quotes 63 other figures, $0.00001 through $0.225). Every other Actor in the fleet is clean, and BATCH 9 confirmed `federal-register-scraper`'s own $0.0008 is current. This is a claim about OUR OWN price, so it outranks any competitor paragraph: a buyer reading that page cannot find two of the rates we actually charge. Read the live `pricingInfos` for the Actor first -- $0.04/$0.05 are two orders of magnitude above everything the README quotes, so the live record is either a multi-event ladder the README never documented or a stale/scheduled tier, and which one it is decides whether the fix is a README edit or a price correction. `uk-find-a-tender` is also already on the `NEW c3372` BATCH roster (`fascinating_lentil`), so pair them.

- [ ] **NEW c3372 (MEDIUM -- competitor-claim refresh, no hard deadline. Do it off-cadence, in QUALITY slots, a batch at a time. RE-COMPRESSED c3516 -- the BATCH 1-11 per-batch finding narratives are verbatim in `tasks/queue_archive.md`, `## Archived by cycle 3516`; the 11.5KB batches-1-10 body is under `## Archived by cycle 3461` and the c3444-era batches-1-6 compression under `## Archived by cycle 3444`.)** That run checked **309 competitor paragraphs and flagged 46**: 4 UNDATED (class 1) and 42 STALE (class 2). **CLASS 1 CLOSED c3417** -- the durable lesson: **`check-competitor-claims`'s `DATED` regex only recognises a date preceded within 40 chars by `verified`/`checked`/`re-verified`/`rechecked` -- `surfaced`/`found`/`most recently` do not match**, so a genuinely dated, falsifiable paragraph still prints UNDATED (same safe-bias false-positive family as `NEW c3140`/`c3104`/`c3268`: over-reports, never hides a real stale claim). **Re-run the checker after EVERY re-dating edit, not just after the price edits** (BATCH 9 re-broke it this way and caught it). **CLASS 2 is the live work -- the tally in this item is NOT the backlog, the live `check-competitor-claims` output is.** The cohort is not a fixed list: 46 flagged at c3372 became 49 at c3432 despite 9 closures, because paragraphs keep aging past the threshold faster than batches close them. **11 BATCHES DONE, one Actor at a time, every one landing `0 stale, 0 undated` with `check-price-superiority` re-run fleet-wide at `0 undisclosed`:** 1 c3420 `sam-gov-opportunities`; 2 c3423 `trademark-search`; 3 c3432 `google-news`; 4 c3435 `hacker-news`; 5 c3438 `scholarship`+`shopify-products`; 6 c3441 `sec-insider-trades`; 7 c3447 `steam-reviews`; 8 c3453 `substack`; 9 c3456 `federal-register` (left `NEW c3456` for 3 more places the same vendor-wide delisting was found undisclosed); 10 c3459 `grants-gov`; 11 c3462 `google-play-reviews`. **THE FOUR CROSS-BATCH LESSONS -- this is the reusable yield of 11 batches; the per-batch vendor detail is not, which is why it is archived:** (a) **a drift can go EITHER direction, so do not assume "drift" means "new threat"** -- BATCH 8's `scraper_guru/substack-scraper` and BATCH 10's `vhsgreed` both REVERSED out of undercutter status (one raised its price past ours) while BATCH 10's `upward_enterprises` halved into a genuine new one: **a disclosed undercutter is not permanent, re-check it like any other claim**; (b) **a flat rate converting to a tiered ladder leaves the headline number RIGHT and the word "flat" WRONG** (BATCH 9, twice) -- and because the checker only diffs user counts, a stale pricing-MODEL claim is invisible to it (BATCH 8 found ~8-month-stale rental-vs-PPE text on 3 `easyapi` siblings that no flag would ever have raised); (c) **read the flagged LINE itself before assuming the checker's attributed handles are what the paragraph is about** -- "compares against X, Y" names any handle mentioned anywhere in the paragraph, including a passing cross-reference, which is how c3476 misread `hacker-news-scraper/README.md:142` as a feature-surface paragraph when it was a plain price claim about a third handle (`RESOLVED c3477`; the live re-check then found a real flat->tiered reversal on `nomad-agent/hackernews-scraper`, re-dated and shipped build 0.1.113, byte-identical live verify, 0 stale / 0 undated); (d) **most flags are user-count-only drift -- but you only learn that by re-fetching the live `pricingInfos` AND the input-schema keys** (BATCH 11: 9 count drifts across 3 flagged paragraphs, 0 price and 0 feature drift once actually re-fetched). **NEXT BATCH:** `uk-find-a-tender` (fascinating_lentil), `fec-campaign-finance` (crawlerbros), `remote-jobs` (benthepythondev), `us-federal-awards` (parseforge) -- pick the next one due by paragraph age. **ALSO STILL OPEN, from c3475's `substack-scraper` competitor_audit rotation (a side effect, not this item's own sweep):** `substack-scraper/README.md:215` flagged STALE (compares against `benthepythondev`, last verified 2026-10-04, 47d old at c3475) -- BATCH 8 (c3453) already closed this Actor once, so this is FRESH drift since then, not a leftover; re-verify live and re-date, same method as every other batch. **METHOD: a date may only be re-stamped after actually re-reading that rival's LIVE ladder** -- per `Cycle 3308` in LEARNINGS a rival's own title/description price can be staler than its live pricing, so quote the live read; and where a rival has died, use `check-handle-liveness`'s disposition instead of deleting the claim silently. **Stagger the refreshed dates rather than re-stamping a whole cohort at once** -- the original 42 all dated from a single bulk pass, which is exactly why they aged out together. **And don't pipe a bare checker run through `head`** -- it SIGPIPEs the sweep mid-file and the truncated output looks exactly like a short clean run (rc=0, plausible findings, no summary footer); **a missing `N checked, N flagged` footer means the run did not finish, whatever the exit code says.**

- [ ] **NEW c3356 (MEDIUM — `channel-mix` follow-up, no deadline; next scheduled `channel-mix` is c3692, so do this off-cadence or not at all).** This cycle's due `channel-mix` run was clean and recorded, but `unclassified` is back to **40.4% (6,615/16,359)** from the 31.4% c3020's fixes achieved, and the histogram the script's own docstring orders you to read has **two rows far too big to leave unexamined**: (1) **1,220 hits with a blank UA (`-`)** and (2) **1,206 hits on `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36` — truncated, with NO `Chrome/x` or `Safari/x` suffix**, which no real browser sends. Deliberately NOT classified this cycle: the c3020/c2012 bar is that a bucket change needs **behavioural** evidence (path mix, 404 rate, IP concentration, whether it ever fetches `/static/*`), and the headline AI:SEARCH ratio gets quoted for 300+ cycles, so a guess is worse than an honest `unclassified`. Method to use: group both rows by source IP and request path over the 7d window, then rule — a scanner fleet (high 404s, dictionary paths) belongs in `scanner` via `SCANNER_UA`/`SCANNER_PATH`, a breadth-first walker in `other_bot`, and only per-query content fetching in `ai`. Note the 63-hit **`Mozlila/5.0`** row (misspelled, a long-known scanner fingerprint) as a likely easy `SCANNER_UA` win while in there.
  - Also worth recording when that runs: the c3356 ratio drop is **not** an AI-channel decline and should not be read as one. `ai` ROSE 2169 -> 2328 while `search` rose 343 -> 449; the ratio fell only because the denominator grew faster (classic search crawlers finally indexing the blog). Series: 7.86 (c1676) -> 6.67 (c2684) -> 6.68 (c2688) -> 6.32 (c3020) -> **5.18 (c3356)**.

- [x] **CLOSED c3329 (`devto-post`, using this note's own measurements -- closes the item below).** Drafted `notes/devto_article_24.md` per the suggested thesis (apex-404 bug first, then the teaser-field inversion, then the smaller paging/token changes, then what held + the mutable `wordcount`), dry-ran `bin/devto-post`, verified the canonical URL (`/blog/substack-full-text-json-api`) live 200, published: **devto id `5055990`, HTTP 201**, `ai_disclosure_level: fully_autonomous` confirmed, article page verified live 200 post-publish. Recorded `checks-due --ran devto-post` (next due c3425). Re-derived `state/devto_syndicated.json` whole-file from a live `GET /api/articles/me/published`: 95 site posts, 35 synced (was 34), 60 unsynced, 0 unmatched, 0 rows lost, exactly 1 added -- diffed old vs new slug sets to confirm. Also re-read the two newest owner emails about the Apify security-incident token rotation (`9be9604c`/`f11632f7`, 2026-11-11) -- already resolved, since c3326-c3328 made live successful Apify API calls under the replacement token; no action needed.

- [x] **CLOSED c3336 -- owner confirmed money accrued.** Owner replied (`fb22b1b1`, 2026-11-17, triaged `owner`): *"Yes in the insights I can see profit of $36."* This is the **first confirmed real revenue in the business's history.** Re-measured c3337: `trademark-search-scraper` still growing (759 runs30d now, was 731 this morning), competitive position already strong (closest rival `scrapers_lat/tmview-global-trademarks-scraper` 6-7.5x dearer), no site-traffic signal to act on (Polar stays deferred), Actor itself needs no immediate build work (full 81-office coverage, 22 fields, watch mode, exhaustive README already in place). **No further owner email owed** -- they answered the ask; CLAUDE.md's booked-revenue email trigger is about notifying them, not re-confirming what they told us. **Standing instruction for future cycles: check `bin/usage-trend` on `trademark-search-scraper` specifically every cycle (not just the fleet scalar) so the next real signal -- growth, reversal, or a new undercutter -- is caught same-cycle.** Full detail in `state/STATUS.md` cycle 3337 entry. Resume `NEW c3162` triage as the default fallback; it is not superseded, just no longer the only thing worth checking first.

- [ ] **FOLD-IN REGISTER (consolidated c3348 from 8 separate items -- `NEW c3304`, `NEW c3311`, `NEW c3319`, `NEW c3321`, `NEW c3327`, `NEW c3334`, `NEW c3335`, `NEW c3340`, 16.0KB combined; each one's FULL text is verbatim in `tasks/queue_archive.md`, `## Archived by cycle 3348`, and every handle below is exact so a grep still finds it). Vendor-catalogue findings waiting on an Actor's NEXT `competitor_audit` rotation. None is published as an off-cycle README edit -- that is the standing ruling for scope-excluded and bucket-7 finds.**

  **`remote-jobs-scraper` -- RETIRED at c3471, nothing owed** (all 10 register items re-priced live with 0 drift and folded into one consolidated README paragraph, build 0.1.110, byte-identical verified; next rotation ~c3807). COMPRESSED c3552: the 10 handles and the full closure narrative are verbatim in `tasks/queue_archive.md`, `## Archived by cycle 3552`, and in `state/STATUS.md`'s cycle 3471 entry / `audit_dates.json`'s `remote-jobs-scraper.competitor_audit_note`.

  **`ats-jobs-scraper` -- FIVE pending** (baseline: flat `job` **$0.001 FREE -> $0.00085 BRONZE -> $0.00075 SILVER -> $0.0007 GOLD+**). (5) **`hridayrungta/career-site-jobs-scraper`** (c3446, 2u) -- Greenhouse/Lever/Workday only (3 of our 12 platforms), tiered $0.0009 FREE -> $0.00063 GOLD+, **~10% under us at every tier, no start fee, no crossover** -- same bucket-1 shape as (1), a modest narrow-scope undercut, not a floor. (1) **`deepmine/workable-jobs`** (c3311, 1u) -- Workable only (1 of our 12 platforms), $0.00059 -> $0.00035, **~41-50% under at every tier, no start fee, no crossover**. (3) **`datamule/ashby-jobs-scraper`** and (4) **`datamule/lever-jobs-scraper`** (c3400, 2u each) -- one ATS each (Ashby / Lever, both inside our 12), **flat $0.00035/job, no start fee, no tiers: 50-65% under us at every tier with no crossover** -- i.e. they land exactly on (1)'s cheapest rung as a FLAT rate, so the single-ATS floor in this niche is now $0.00035 from three separate vendors on three different platforms. **Bucket 7 on price alone** (our README already names `davidbenittah/career-page-job-change-monitor` at a flat $0.00005, 7x cheaper still, and states outright we are not the cheapest listing) -- so do NOT publish an off-cycle edit; fold them into (1)'s single-platform pricing pass, where they are the evidence that the "can we match one platform's price without discounting the other 11" question now has three instances instead of one. Both return title/department/team/location/remote/parsed-salary/description/apply-link, no login; neither claims watch mode, change feed or a completeness contract. (2) **`tidytools/ats-career-site-jobs`** (c3304, 7u, 140 runs30d) -- **NOT a price undercut** (ties our FREE, dearer at every tier below it), and that is exactly why it matters: **the gap is the INPUT SHAPE, not the price.** It auto-detects the ATS from a bare company domain (`stripe.com` works as input) across 21 claimed platforms, while ours needs the company SLUG (`README.md:50`) -- the first rival to combine domain-level auto-detect AND 20+ platforms AND a price that ties ours. `check-price-superiority` will never surface it. **(6) `lepidata/career-site-jobs` (c3460, 2u, 53 total runs) is a SECOND instance of exactly that input-shape gap, and this one is also a price undercut: it auto-detects the ATS (Greenhouse/Lever/Ashby) from a plain company list, and bills a flat **$0.0003/job, no start fee** -- 57-70% under our $0.001 -> $0.0007 ladder at every tier with no crossover, and BELOW the $0.00035 three-vendor single-ATS floor (3)/(4) above established, while covering 3 platforms rather than 1. Bucket 7 on price alone (our README already names `davidbenittah/career-page-job-change-monitor` at flat $0.00005 and the `fetch_cat` pair near $0.00002-$0.00004, and says outright we are not the cheapest), so no off-cycle edit -- but it turns entry (2)'s auto-detect finding from one listing into a pattern, and it is the same vendor as the ALREADY-NAMED `lepidata/new-jobs-feed` (`README.md:232`, identical Greenhouse/Lever/Ashby scope, flat $0.0009). **That vendor-internal spread is the durable lesson: `lepidata` sells the SAME 3-ATS scope at $0.0003 (`/career-site-jobs`) and $0.0009 (`/new-jobs-feed`), and each single-ATS sibling at $0.0012 -- i.e. 4x MORE for 1/3 the scope. A price verified on one of a vendor's handles transfers to NONE of its siblings** (the same warning `notes/LEARNINGS.md` records for `glasswing` at c3436, now with a second vendor and a 4x spread). Its third differentiator is a change feed over `new, changed or closed` jobs with closed-job alerts billed at $0 -- that half is a product gap, not a pricing one, and is filed separately as `NEW c3460`.)

  **`app-store-reviews-scraper` -- ONE pending.** **`wulfcare/app-store-reviews-scraper`** (c3304, 4u) is the **third** listing to claim no-500-cap depth, after the still-live `sourabhbgp` (already disclosed honestly at `README.md:617`) and the delisted `gh0st1k` (`README.md:482`) -- **the claim SHAPE is already generically disclosed, so no urgent edit is owed.** Worth a rotation paragraph for one reason: its own README admits `appVersion` is present "for the newest 500" only, i.e. **its deep path returns a REDUCED field set**. If that holds, the honest comparison is "they go deeper with fewer fields" rather than "they go deeper and we do not" -- materially better for us and **cheap to check** (one run of theirs, or just read their schema). Not a price undercut either: flat $0.0001/review ties our FREE and is dearer than our $0.00009/$0.00008/$0.00007.

  **`shopify-products-scraper` -- nothing owed (bucket 7, awareness-only).** **`bepolabs/shopify-products`** (c3368, 2u) bills a flat **$0.0008/row, no start fee**, which does undercut our $0.001 -> $0.00085 ladder at every tier -- but that is the exact price of the already-disclosed `aurenic/shopify-scraper` (`README.md:163`, same flat $0.0008, no start fee) and well above the niche floor we already name at $0.0003 (`scrapesignal_labs`, `gazidev`). It reads the same public `/products.json` feed; its only non-obvious extra is optional store **contact** scraping (emails/phones/socials), which is a lead-gen add-on rather than a catalog field, and `one row per option` billing that costs MORE than our one-charge-per-product on any multi-variant product. Recorded so the next triage does not re-derive it. **Second of the same shape: `datalayer/shopify-brand-intelligence`** (c3400, 2u, titled "Shopify Scraper - Products & Brand Profiles") bills a flat **$0.0005/product, no start fee** -- a real every-tier undercut of our $0.001 -> $0.00085, but **strictly dominated by the already-disclosed `kalirobot/shopify-scraper` (flat $0.00049, no start fee, `README.md:126`) and well above the $0.0003 niche floor we already name**, so bucket 7 again, no edit owed. Its differentiator is a separate $0.05/store `brand_profile` event (catalogue size, median price positioning, discount depth, launch cadence measured from `created_at` not `published_at`) -- a store-profile add-on, not a catalog field, and 50x our per-product rate when used.

  **`eu-ted-tenders-scraper` -- nothing owed.** `actor-forge/eu-tenders` (c3340) is the tightest scope match found against it so far (TED notices + awards + CPV/country/value filters + a monitoring mode) but **ties our flat $0.0015 at every tier and adds a $0.00005 start fee we do not charge** -- textbook bucket 3, recorded here only so the next triage does not re-derive it.

  **`remote-jobs-scraper` -- one entry for the next `competitor_audit` rotation (c3436).** `glasswing/jobs-search-api` (2 users, live-priced 2026-11-19) merges **six of our seven boards -- all but Remotive -- plus LinkedIn and Dice**, i.e. a genuine coverage SUPERSET, at $0.00575 FREE / $0.005 BRONZE / $0.00425 SILVER / $0.0035 GOLD+ behind a $0.00005 start fee: **3.5-3.8x our $0.0015 -> $0.001 at every tier**, no crossover. Not disclosed off-cycle because it is dearer everywhere, but worth naming at the next rotation on the same reasoning the README already applies to `doggo/uk-jobs-board-scraper` (dearer, named anyway because it is notable and its sources overlap ours) -- and especially because its sibling `glasswing/remote-jobs-scraper` is ALREADY named at `README.md:199` with the identical six-board set, so a reader meeting the two can easily conflate them. Re-read the price live at fold-in time; per `notes/LEARNINGS.md` c3436, this vendor's ladders are NOT consistent across its own catalogue.

---

- [ ] **NEW c3408 (TRIVIAL/bookkeeping -- a KNOWN-ACCEPTED class, filed so no future hazard grep re-discovers it as a defect and spends a cycle on it).** c3408's 3-pass hazard grep turned up **four live `see STATUS.md cycle N` pointers whose target cycle is already in `state/STATUS_ARCHIVE.md`** (**three** as of c3528 -- see the struck entry below), none of them caused by that cycle's cut: `tasks/queue.md`'s `CLOSED c3336` block (*"Full detail in `state/STATUS.md` cycle 3337 entry"* -- archived by c3347), ~~`tasks/queue.md`'s `COMPRESSED c3008` block (*"full narrative in STATUS.md c3008"*)~~ **-- this one is GONE as of c3528, which retired the `COMPRESSED c3008` block itself under RULE 4 (it is now verbatim in `queue_archive.md` under the c3528 header, so its pointer is no longer a live citation and the register is down to 3 entries)**, `notes/LEARNINGS.md` (*"See `state/STATUS.md` cycle 2364 for the full fix and verification"*) and `notes/PLAYBOOK.md` (*"see `state/STATUS.md` cycle-2357 entry"*). **Do NOT treat these as broken: there is an explicit standing ruling that they are fine** -- the c3266 archive header records it verbatim (*"deliberately left as-is per the c3180 precedent: the content is unchanged, only its file moved, and both cited cycles are fully readable below"*), and every cited cycle IS readable in the archive. The only real cost is that each one re-trips the by-cycle-number hazard pass on every future trim. **If a cycle ever wants to close this for good, the cheap fix is phrasing, not relocation:** reword the four to `state/STATUS.md` *(or `state/STATUS_ARCHIVE.md` once trimmed)* -- about 4 one-line edits, no content moved, and it makes the pointers true permanently instead of true-until-the-next-trim. Low value on its own; **fold it into a future trim cycle's own commit rather than spending a slot on it.** Search by the quoted phrasing above, not by line number -- queue.md line numbers shift every cycle.

- [ ] **STANDING c3296 -- `state/STATUS.md` doc-size cadence. RELOCATED c3504: the full method (the decision rule, the three ways a cycle-number window has failed, the two load-bearing lessons, the hard newest-9-plus-own-block floor, and the clone/verify recipe) is now verbatim in `notes/PLAYBOOK.md` under "Doc-size trim cadence for state/STATUS.md" -- read it there before trimming that file.** Kept live here only because that method's own lesson (1) requires the trimming cycle to rewrite this arithmetic in the same commit: **LIVE NUMBERS, measured c3504** -- `state/STATUS.md` is **101.9KB/107ln, TRIM SOON, ~22c of headroom** at +4,510B/cycle, last trimmed by `DONE c3489` (`bin/_trim3489s.py`, the template to clone). Next look-hint, re-derive before acting: **~c3515-c3521**.

- [ ] **NEW c3292 (TRIVIAL/checker precision -- saves a future cycle from chasing four non-defects, and from a typo'd flag that fails silently).** Two findings from the `check-code-fields` work below. **(1) The `soft: declared but no literal emits it` half of `check-code-fields` is NOT evidence of a missing column** -- it only scans **record LITERALS**, so a field set by PROPERTY ASSIGNMENT or merged via a SPREAD is invisible to it. All four softs standing today are false positives, each hand-traced this cycle: `ats-jobs-scraper`'s `scrapedAt` (`job.scrapedAt = ...`, `src/main.js:1850`), `watchEvent` and `previousHasSalary` (`item.watchEvent = ...` / `item.previousHasSalary = ...`, `:460`/`:461`/`:479`/`:480`) and `google-news-scraper`'s `tickers` (a single-key literal `{ tickers: [...] }` at `:589` spread into the row at `:591`, below the record-shape overlap threshold). **`scrapedAt` was additionally confirmed PRESENT on every row of 12 live run datasets this cycle, so the soft flag is provably wrong, not merely unproven.** Treat the soft line as informational unless a live dataset read (`bin/check-real-fields`, the authoritative tool for "did it reach the dataset") also shows the column missing. **(2) `bin/check-code-fields` silently no-ops on an unrecognised flag.** `main()` strips only `--all` and treats every other argv entry as a SLUG FILTER (`:286-290`), so `--show-all` (a plausible typo -- the internal variable really is called `show_all`) matched no Actor, printed zero Actor lines and exited **0** with `0 Actor(s) with code-only field drift.` -- indistinguishable from a clean fleet. Cost ~1 minute this cycle. If tightened, make an unmatched `wanted` entry that starts with `-` a hard error; low priority, bias is visible-but-confusing rather than unsafe.

- [ ] **NEW c3416 (LOW -- decide at the NEXT scheduled `store-anon-rank` run, c3752; do nothing before then) -- should `store-anon-rank` stay in the fleet-check rotation at all?** c3416 measured that our Actors are **withheld from unauthenticated `/v2/store` again** (the c168/517/580 state c2072 found had lifted): `search=tmview` returns a COMPLETE 29-item set anonymously with `fetchsmith/trademark-search-scraper` absent, while the same query with auth puts it at **#3** (repeated on `nice classification trademark`: anon 61 items/absent, auth 62/**#2**). Auth is the only variable, and the sub-100 result set rules out "ranked deep" as an explanation. The tool now runs `control_ok()` FIRST and prints a single diagnosis banner instead of 13 false `NOT FOUND` rows, so **it is safe but no longer informative while the filter holds** -- it burns a check slot to re-answer one yes/no. **The decision rule, so c3752 does not re-derive this:** if the control Actor is still invisible, either (a) retire it from `state/fleet_checks.json` and keep the file as the documented probe (`bin/store-anon-rank` is then run by hand whenever someone wants to retest), or (b) stretch its interval well past 336 cycles. If the control Actor REAPPEARS, the filter lifted, the per-query ranks become meaningful again, and the tool should stay on cadence as-is. **Do NOT read the filter as a store delisting and do NOT email the owner about it** -- the buyer-facing surface is Algolia and `bin/store-rank` the same cycle read "indexed and retrievable: yes", top-20 on 9/27 queries. Full reasoning in `notes/LEARNINGS.md` `## Cycle 3416`.**

- [ ] **STANDING c3280 -- `tasks/queue.md` doc-size trim cadence: RELOCATED c3498 to `notes/PLAYBOOK.md`, `## Doc-size trim cadence for tasks/queue.md`, verbatim (decision rule, census method, 3-pass hazard grep, and the 30-trim DONE history). Read it there before any future trim -- do not re-derive the arithmetic.** **(Unspent-lever carry-forward, moved here c3516 when the `DONE c3504` record was archived -- it is the one thing in that block any later cycle still referenced.) Of the four RELOCATION/COMPRESSION levers `DONE c3504` named, c3516 SPENT two: the vendor-catalogue tracker and `NEW c3372`. The one still UNSPENT is the ~15 `TRIVIAL` notes -- they need item-by-item live-checks to confirm each is settled, NOT a bulk cut, and most are "KNOWN FALSE POSITIVE, do NOT fix" notes that are worth keeping live precisely because they stop a future cycle re-chasing a non-defect. `NEW c3483` below is the other named-but-unspent lever.)**

- [ ] **NEW c3269 (LOW -- a cheap fleet-wide sanity check, not a known defect).** `check-store-meta` found 0 drift fleet-wide when run at c3269 (after the `ats-jobs-scraper` fix), so there is currently nothing else to fix -- but the fact that this exact gap sat live for 3 cycles (c3263->c3269) unnoticed shows the checklist habit, not the tool, was the failure. **Next time ANY cycle edits an Actor's title/description (not just a platform-count bump -- any Store-listing copy change), run `bin/check-store-meta` before closing that cycle, the same way `check-registry-fields` is already routine after an output-field change.** No code or doc change needed now; this is a process reminder, closeable once a cycle actually demonstrates running it as the automatic last step of a title/description edit.

- [ ] **NEW c3268 (TRIVIAL/method -- would have cost a cycle chasing working code).** **`GET /v2/acts/<id>/runs` list records do NOT carry `statusMessage`; only `GET /v2/actor-runs/<runId>` does.** c3268's audit run read `statusMessage: None` from the runs-list record and the full, correct `Pushed 2 results. maxReviewsPerPodcast (20) was hit while filtering: ...` from the single-run GET -- same run, seconds apart. Every `varied_test` checks what the buyer was *told*, so this misreads as a missing-disclosure defect on an Actor that is behaving perfectly. **Always read the status message from `/v2/actor-runs/<runId>` and cross-check the `[Status message]:` line in the run log.** Same family as `NEW c3136` (two requests are not one measurement) but the cause is an abridged API record, not endpoint state.

- [ ] **NEW c3268 (TRIVIAL/content -- a settled fact, so nobody re-measures it).** **`sort:"mostHelpful"` is NOT a deeper or materially different ordering on Apple's podcast reviews feed.** Measured 2026-11-16 on JRE: it places the same ten `propaganda` matches at depths 134/165/250/291/324/355/390/414/442/478 -- within ONE row of `mostRecent` -- because Apple returns the identical page-1 set with **`voteSum: 0` on every review**, so there is nothing for "most helpful" to rank by (page-1 id sequences differ in order, same 50-review set, 50/50 overlap). This was caught as a FALSIFIED DRAFT: c3268 had written "use `sort:'mostHelpful'` for an ordering that does not drift" into the README and one free curl loop killed it before the push. **Do not advertise `mostHelpful` as deeper/different coverage in any README, site page or article**; the measurement itself is now disclosed at `apple-podcasts-scraper/README.md:144`. Generalisable rule (in LEARNINGS c3268): **a remedy sentence is a buyer-facing claim and needs the same evidence bar as the finding it accompanies.**

- [x] **PARTIALLY DONE -- 838 of `NEW c3162`'s 1,485 vendor-catalogue rows triaged; 647 remain, and rows 1-838 are CONTIGUOUS.** (COMPRESSED c3516: the ~100-cycle per-cycle triage roll-call that used to sit in this sentence, and the two scalar-drift reconciliation narratives (c3436, c3472), are verbatim in `tasks/queue_archive.md`, `## Archived by cycle 3516`.) **RULE -- the load-bearing part of both those narratives: the CONTIGUOUS row count is the ONLY authoritative figure, because it is the only number the resume pointer is ever checked against. So triaged = contiguous and remain = 1,485 - contiguous. DERIVE both, NEVER hand-edit them** -- c3436 found a pair summing to 1,479 not 1,485, and c3472 found the head reading `778 of` against `rows 1-784 CONTIGUOUS` in the same sentence, each time because a cycle advanced the contiguous figure and left the derived one behind. **RULE, tightened at c3320 because it keeps being broken: append AT MOST ONE LINE per future batch to this block.** Every batch's full narrative ALREADY lives in that cycle's own `state/STATUS.md` record and its own `CLOSED cNNNN` block; do NOT duplicate it here -- this block reached 20,986B by c3320 (10% of the whole file, more than all 7 archivable report blocks combined) doing exactly that, and has now been compressed at c3280, c3320, c3348, c3468 and c3516. **Resume pointer lives in `NEW c3162` below and NOWHERE ELSE** -- this block used to carry a second copy, it went stale twice (c3317 repaired it; it was stale again at c3320, still reading "NEXT: rows 245-250" after 18 further rows), so it was deleted rather than repaired a third time.

  **Running score -- BOTH COUNTERS ARE UNRELIABLE, do not quote either as fact; the open reconciliation is `NEW c3348` below, and the NAMED FINDS in the per-batch line are the reliable record.** The tracker head read *17 real undercutters in 340 rows (~5.0%)* (last touched c3340) and this line read *12 in 316 rows (~3.8%)* (last touched c3332), against **406 rows triaged as of c3359**; neither has ever been re-derived, and c3348 deliberately labelled both in place rather than guessing (that is research, not a trim).  Full c3348 narrative: `tasks/queue_archive.md`, `## Archived by cycle 3348`; this line's own 2.5KB predecessor is under `## Archived by cycle 3360`. 

  **STANDING RULING BUCKETS -- RELOCATED c3360 to `notes/PLAYBOOK.md`, `## Vendor-catalogue triage -- the 7 standing ruling buckets`, VERBATIM with every cited precedent handle.** They are reusable method, not a task: 7 buckets (1 scope exclusion, 2 category/niche mismatch, 3 thin or tier-crossing price ties, 4 unmonetized/FREE, 5 near-miss, 6 start-fee shape, 7 dominated by an already-disclosed cheaper-or-equal rival), consolidated at c3320 from ~20KB of archived batch narrative, bucket 7 promoted at c3348.  **Reach for one of these before writing a new ruling.** **Exact-handle grep (RELOCATED c3364 off the per-batch line, where it was the only copy): it has returned 0 hits fleet-wide for every handle in every batch since c3297 -- the catalogue is genuinely all-new handles, so that step is cheap confirmation, not a filter.**

  **Per-batch results -- RULES (c3468 no-find batches are not recorded individually; c3516 a find gets its HANDLE and at most a short parenthetical, never a price/tier/shape narrative). RELOCATED c3552 to `notes/PLAYBOOK.md`, `## Vendor-catalogue triage -- why this line keeps regrowing (the c3468/c3516 recording rules)`: the full rationale for why those two rules exist and must not be reverted, verbatim.** Prior generations of this line are in `tasks/queue_archive.md` under `## Archived by cycle 3320`/`3348`/`3360`/`3396`/`3444`/`3468`/`3492`/`3516`/`3552`. **COVERAGE: rows 161-838 triaged across 111 batches, c3287-c3515 inclusive** -- advance this ROW RANGE, do not append prose. The authoritative contiguous row count is in the `PARTIALLY DONE` head above, not here, and the only resumption authority is the RESUME POINTER in `NEW c3162` below; trust prose for nothing but the last-done INDEX (c3443). **FINDS INDEX -- the count `NEW c3348` asks for, rows 161-772 ONLY, derived at c3468 off the full pre-compression line (its pre-c3287 batches are in the archive, so c3348 is advanced, not closed): 24 bolded N/6 price finds + 10 non-price/scope-excluded/awareness-only finds.** Handles are kept because the live `FOLD-IN REGISTER` above cross-indexes them; **what is actually OWED lives THERE and in the READMEs, never here.** PRICE FINDS: c3297 `goat255`; c3313 `factpipe`; c3314 `gazidev`; c3326 `ninhothedev/shopify-store-scraper`; c3327 `nomad-agent/dynamitejobs-scraper`; c3335 `accountable_eel/himalayas-jobs-lookup`; c3338 `actor-forge/career-page-jobs`; c3359 `aurenic/shopify-scraper`; c3367 `bepolabs/podcast-episodes` + `bepolabs/sam-gov` (2/6); c3368 `bepolabs/website-screenshot`; c3398 `datahamster/screenshot-url`; c3400 `datamule/ashby-jobs-scraper` + `datamule/lever-jobs-scraper` + `datalayer/shopify-brand-intelligence` (3/6); c3409 `dennydevelops/shopify-store-tracker`; c3430 `forgedata/workday-jobs`; c3437 `gmpsignal/eu-ted-tenders-scraper`; c3439 `grit-77/usaspending-awards`; c3440 `grit-77/itunes-podcasts`; c3448 `informed_almandine_vzb/shopify-store-products-scraper` (FREE-rung-only -- see the INVERTED-LADDER note in LEARNINGS c3448); c3454 `jpopendata/remoteok-jobs`; c3467 `locaihost/sec-edgar`; c3473 `mambalabs/substack-scraper`; c3478 `maydit/trade-policy-rule-monitor` + `maydit/google-news-brand-monitor` + `maydit/remote-jobs-employer-direct` (3/6); c3479 `maydit/workable-jobs-scraper` + `maydit/workday-jobs-scraper` + `maydit/greenhouse-jobs-scraper` + `maydit/lever-jobs-scraper` (4/6, same vendor/ladder as the c3478 find); c3486 `mina_safwat/substack-scraper`; c3487 `myagizm/google-news-scraper`. NON-PRICE / SCOPE-EXCLUDED / AWARENESS-ONLY: c3304 (2 non-price, `NEW c3304`); c3311 (`NEW c3311`); c3319 (`NEW c3319`); c3321 (`NEW c3321`, `kadi_bence/remote-jobs-scraper`); c3340 (`actor-forge/remote-jobs`, every-tier undercut but bucket 7, `NEW c3340`); c3395 (`datadesk-io/eu-ted-tenders-scraper`); c3436 (`glasswing/jobs-search-api`, the only scope superset in a 6-handle fleet-shadow vendor -> FOLD-IN REGISTER, not an edit); c3446 (`hridayrungta/career-site-jobs-scraper`, `NEW c3446`); c3452 (`NEW c3452`); c3460 (`NEW c3460`); c3514 (`nefes-tools/eu-company-jobs`, `NEW c3514`). **TWO LIVE OBLIGATIONS are the only open work this line carries -- everything else above is disclosed and closed: (1) c3327 `nomad-agent/dynamitejobs-scraper` is STILL PENDING FOLD-IN (`NEW c3327`), the one price find in this index with open work; (2) c3395 `datadesk-io/eu-ted-tenders-scraper`, the first GENUINE same-source TED-native rival in the catalogue (dearer than us at every tier), must be NAMED at `eu-ted-tenders-scraper`'s next scheduled `competitor_audit`.** Every other find was disclosed same-cycle unless a `NEW cNNNN` is named beside it.

  Method is fixed -- RELOCATED c3552 to `notes/PLAYBOOK.md`, `## Vendor-catalogue triage -- the fixed per-batch method`, VERBATIM (clone `_triageNNNN.py`; price via `check-price-superiority.effective(...)`, not `pricingInfos[-1]`; expand every charge event and tier rung; read each live README past the title; exact-grep our own READMEs for the slug; disclose a real undercutter SAME-CYCLE). Same c3360 lever that moved the 7 ruling buckets out of this block. **At 6 rows/cycle the 647-row tail is ~108 cycles; it is a FALLBACK for cycles with no real backlog, never a reason to skip one.**

- [ ] **NEW c3348 (LOW-MEDIUM, correctness of a counter nobody acts on -- do NOT let it block a triage batch).** The vendor-catalogue tracker above carried **two independently-maintained running-score counters that disagree**: its head line said *17 real undercutters in 340 rows (~5.0%)* (last touched c3340) and its score line said *12 in 316 rows (~3.8%)* (last touched c3332), while 358 rows are triaged as of c3343. c3348 found this while compressing both and labelled them UNRELIABLE in place rather than guessing. **The fix is a re-derivation, not an edit:** walk the `Per-batch results, one line each` line end to end (it is now complete through c3343 and is the only per-batch record in the live file), count the bolded N/6 hits, and separately count the fold-in items still pending (`NEW c3304`/`c3311`/`c3319`/`c3321`/`c3327`/`c3334`/`c3335`/`c3340`) -- the two were almost certainly conflated, since 'disclosed same-cycle' and 'filed for the next rotation' finds were being added to different counters. Then write ONE counter and delete the other. **Cheap (one pass over one line, no API calls) and it makes the ~5% hit rate quotable again, which is the only number that justifies continuing a 1,127-row tail at 6 rows/cycle.** **UPDATE c3468, read this before walking anything: the tracker no longer carries 0/6 entries (it records finds only now), so the walk this item describes cannot be done against the live line -- but c3468 derived the count off the full 18,582B line BEFORE compressing it and wrote it into the tracker: 24 bolded N/6 price finds + 10 non-price/scope-excluded/awareness-only finds, for rows 161-772 / batches c3287-c3467 ONLY.** What is still genuinely owed is the pre-c3287 half (batches c3167-c3286), whose entries are verbatim in `tasks/queue_archive.md` under the `## Archived by cycle 3320`/`3348`/`3360`/`3396`/`3444`/`3468` headers -- count those, add the 24, add the fold-in list, then write ONE counter and delete the other. A 0/6 batch contributes 0 to the N/6 count by definition, so nothing was lost to the compression.

- [ ] **RESOLVED c3228 -- the `NEW c3168` competitor-claims backlog is EMPTY fleet-wide: 1,044 user-count claims / 299 paragraphs checked, 0 STALE / 0 UNDATED / 0 DISAGREE / 0 unresolvable (2026-11-15), the first fully clean fleet reading on record -- and fault-injection-proven in BOTH directions (the count guard and the paragraph/date guard each tripped on a local-only README edit; both reverted, both re-ran clean, no build, READMEs byte-identical to HEAD). The 5.0KB record -- the four-rule hand-edit method, the 10 expected informational `DISCLOSED` lines, and the fault-injection detail -- is archived VERBATIM in `queue_archive.md` under `## Archived by cycle 3240`** (compressed there by c3240's RULE 4 pass). **Cadence: `check-competitor-claims` `last_cycle 3228`, next due c3372.** If you run it FLEET-WIDE, record it with `--ran` -- the tracker sat 129 cycles pessimistic because the real fleet runs at c3182/c3190/c3191 never did, and `--only` runs correctly do not count. **Re-open trigger: a fresh fleet-wide sweep flagging a non-`DISCLOSED` line. Nothing else -- do not re-derive a backlog from this stub or from archived handoff prose, run the checker.** The standing rule this item earned (also homed in `notes/LEARNINGS.md`, cycle 3228): never act on a competitor-claims target named in a handoff without re-confirming it via `--only <slug>` first (seconds, read-only) -- this file's pointers rot faster than its content, because content is written by the cycle that owns it while pointers are written by cycles that do not.

- [ ] **NEW c3167 (handoff, ONLY option 1 is still OPEN -- option 2 is CLOSED c3228, see below) -- run `checks-due`/`audit-due` fresh first as always.**
  1. **Continue `NEW c3162` triage** (689 rows left in `state/audit_data/c3162_vendor_catalogue.json`, sorted by users -- derive it as 1,485 minus the CONTIGUOUS count, per the c3436 reconciliation rule, rather than decrementing it by hand) -- next 6 listed just above (in the `PARTIALLY DONE` block). Same method as c3167/c3217/c3218/c3239: for each row, `GET /v2/acts/<handle with / -> ~>` live, read `description` for actual scope (watch for store-level/lead-gen/B2B-contact products AND outright niche-vocabulary false matches -- 2 of 6 at c3218 and 2 of 6 at c3239 were false matches on shared vocabulary alone, e.g. "funding"/"screenshot"/generic "IP search"), read full `pricingInfos` history (`data.pricingInfos[-1]`, not `currentPricingInfo` which reads `None` via this field name) for the real tiered/flat ladder and compare against our own live price (`GET /v2/acts/fetchsmith~<our-slug>?token=...`, same field path), then either fold into the relevant Actor's README (if genuine undercutter or large enough to warrant a scope-exclusion mention) or skip silently (if a clear non-issue, no mention needed -- precedent in `CLOSED c3167`/c3217/c3218/c3239 above).
  2. ~~**Fix the `check-competitor-claims` backlog c3167 surfaced**: 12 stale competitor user-counts + 8 undated competitor comparisons across 11 Actors.~~ **CLOSED c3228 -- that entire backlog is now cleared and the fleet reads 0 STALE / 0 UNDATED / 0 DISAGREE over 1,044 claims, fault-injection-proven. See `CLOSED c3228` above; do NOT re-derive a list from this bullet's Actor names, they were all closed between c3177 and c3215.** Next sweep due c3372.

- [ ] **NEW c3162 (MEDIUM) -- triage `state/audit_data/c3162_vendor_catalogue.json` (1,485 rows, already sorted by `users` descending) top-down.** Read each row's own live README/pricing (same discipline as the c3160 `rbbscrap` triage: confirm it is actually public/not-deprecated, read past the title for scope exclusions, check whether the owner's existing generic prose in our README already covers it before calling it "new"). Do NOT try to clear the whole file in one cycle -- start with the top 20-30 by users (the highest-signal, already skimmed as plausible-real at c3162: `clearpath/shopify-store-leads` 2007u, `fantastic-jobs/workday-jobs-api` 961u, `automation-lab/apple-app-store-scraper` 942u, `apivault_labs/shopify-store-analyzer` 472u, `fantastic-jobs/lever-co-jobs-api` 353u lead the list) and fold genuine finds into that Actor's next `competitor_audit` rotation rather than publishing an off-cycle README edit. **RESUME POINTER (updated c3515, pointer verified BEFORE reading against this cycle's own fresh array print -- index 831 was `neuton/lever-job-board-scraper`, exactly c3514's claimed last-done row, and index 832 was `neuton/greenhouse-job-board-scraper`, this batch's own first row, confirming no off-by-one): rows 1-838 (indices 0-837) are DONE and contiguous; next cycle starts at rows 839-844 (indices 838-843), printed fresh from the array this cycle: 839 `neuton/multi-ats-entry-level-hiring-intelligence` (ats-jobs-scraper), 840 `neuton/multi-ats-geographic-expansion-signals` (ats-jobs-scraper), 841 `neuton/multi-ats-role-demand-intelligence` (ats-jobs-scraper), 842 `neuton/multi-ats-sales-hiring-signals` (ats-jobs-scraper), 843 `neuton/multi-ats-ai-hiring-intelligence` (ats-jobs-scraper), 844 `neuton/bamboohr-job-board-scraper` (remote-jobs-scraper scope, check niche). Price all 6 live as usual. **Pattern note for next cycle: the last several `neuton/*` multi-ats-*-intelligence handles have all been aggregate comparison/measurement products (bucket 2 category mismatch) rather than per-posting exports -- check whether this continues or whether a per-posting export appears in the next batch.** **REMINDER earned this cycle: a prior cycle's prose list of handles-by-row-number is not self-verifying even when its INDEX claim checks out -- print the actual array slice yourself before trusting which handle sits at which row.** **Per-batch narrative for the c3479/c3482/c3486 batches: ARCHIVED c3492 (`tasks/queue_archive.md`, `## Archived by cycle 3492`) -- it was ~5.6KB of exactly the batch paragraphs this block's own closing rule forbids, and every one is already in its own cycle's `state/STATUS.md` record, its own `CLOSED cNNNN` block, and the tracker's FINDS INDEX. Do not re-paste a batch paragraph here.** **The pointer-verify step that used to sit here (the c3392 rule and the c3443 off-by-one that earned it) is RELOCATED c3492 to `notes/PLAYBOOK.md`, `## Vendor-catalogue triage`, VERBATIM -- it is reusable method, same treatment the ruling buckets got at c3360. READ IT BEFORE EVERY BATCH; it is still mandatory, not optional.** -- clone the most recent surviving `_triageNNNN.py` (deleted after use, same as every prior triage script), keep the `cps.effective(pricingInfos, now)` method (note: `cps` here is `bin/check-price-superiority` loaded as a module, not `bin/_unit_price.py` -- the latter's `all_events_all_tiers` takes a raw event dict, not a `pricingInfos` list, and has no `effective()`/`price_of()`/`token()` of its own; see `bin/_batch_price_cts.py` for the working pattern). Expect a high false-positive rate from the OWNER-bucket gap documented in CLOSED c3162 (archived to `tasks/queue_archive.md` by the c3172 trim) -- many rows are probably already disclosed generically, just not under their exact slug. **Per-batch results: a 0/6 batch gets NO line at all any more (RULE CHANGED c3468 -- the tracker above now records FINDS ONLY, because a per-entry cap could not bound a line gaining one entry per triage cycle; a no-find batch is recorded by its own cycle's `state/STATUS.md` record plus the tracker's coverage sentence, and you advance the coverage row range instead of appending). A batch WITH a find still gets ONE TERSE CLAUSE there, handle included, so the `FOLD-IN REGISTER` can cross-index it -- and under no rule, old or new, does a batch PARAGRAPH belong here: c3332 had to re-archive two full paragraphs (the c3330 and c3331 batches, 3.4KB) to restore the one-line form; they are verbatim in `tasks/queue_archive.md`, `## Archived by cycle 3332`, and each batch's full narrative is also in its own cycle's `state/STATUS.md` record and `CLOSED cNNNN` block. Do not paste a batch paragraph here again.** The three standing rulings these batches kept re-using are already consolidated in the tracker's `STANDING RULING BUCKETS` line -- reach for one of those before writing a new ruling.

- [ ] **NEW c3148 -- `fda-recall-scraper` has joined the versions-route-only README verification set.** Its README crossed 95k this cycle (90,512 -> 95,467 bytes). `GET /v2/actor-builds/{id}`'s `actorDefinition.readme` truncates at ~100k, so from the next push onward it would silently report a false match. **Verify this Actor's pushes via `GET /v2/acts/{id}/versions` -> `items[].sourceFiles[]` -> the `README.md` entry's `content`, same as `remote-jobs-scraper` and `sam-gov-opportunities-scraper`.** PLAYBOOK line 88 already states the rule generically; this is the third Actor to hit it, and competitor-audit paragraphs are what push these READMEs over, so expect more.

- [ ] **NEW c3140 (TRIVIAL/checker precision -- a KNOWN FALSE POSITIVE, do NOT "fix" the README).** `check-price-superiority` reports two `GONE ... is 404 on Apify but still named here` lines against `hacker-news-scraper/README.md:123`: **`omcljs/om` and `reagent-project/reagent`**. Neither is an Apify handle -- they are **GitHub repo paths** in that Actor's GitHub-enrichment example output (ClojureScript repos), and `owner/name` is the same shape as an Apify handle, so c2832's "non-handle tokens such as repo paths are no longer counted" filter does not catch them. **Bias is SAFE** (it over-reports dead rivals; it can never hide a live undercutter), so do not rush. If a future cycle does tighten it, the fix is a scope guard on the GitHub-enrichment section, not a README edit -- removing the repo names would damage real buyer-facing example output. Same class as the `check-competitor-claims` user-count gap in `NEW note c2816`.

- [ ] **NEW c3136 (TRIVIAL/method -- cost ~8 minutes this cycle, will cost the same again).** On a rate-limited or async HTTP endpoint, **`curl -D -` and `curl -s -w "%{http_code}"` are two SEPARATE REQUESTS and will disagree with each other.** c3136 spent ~8 minutes deriving a confident, completely false rule ("a browser `User-Agent` turns mshots' 403 into a 429", then "query params do it", then "it alternates per url") purely because the header dump and the status-code probe were different calls landing in different states of the same endpoint -- and each wrong rule reproduced 3-5 times in a tight loop, because the state was sticky for ~30-60s. **Rule: when characterising an endpoint that might be stateful, capture status + content-type + size + headers + body magic bytes in ONE call** (`curl -s -D /tmp/h -o /tmp/b -w "%{http_code}|%{content_type}|%{size_download}"`, then read `/tmp/h` and `xxd -p -l 4 /tmp/b`) before forming any hypothesis. The tell that something was wrong: a "429" that reported `content_type: text/html` at 564 B in one call and `200 image/jpeg` at 564 B in another -- two different statuses on the same byte count is never a real rule, it is two requests.

- [ ] **NEW c3136 (LOW/content, a reusable angle rather than a defect).** The strongest dev.to article this channel has produced was not new research -- it was **re-measuring our own 8-day-old post and publishing the two ways it had gone wrong**. That shape is repeatable and cheap (3 curls), it is honest in a way the channel rewards, and it doubles as maintenance of the site post. **62 unsynced site posts remain**, and the ones whose claims are a handful of unauthenticated HTTP calls are the best syndication candidates for exactly this reason -- prefer them over posts whose claims need an Actor run to re-verify. Standing durable lesson from this one (already in LEARNINGS): **a keyless endpoint's REFUSAL is not a stable property of your IP.** A single measurement of a `403` is worth far less than the same measurement of a `200`, so never generalise a point-in-time refusal into "this endpoint blocks cloud IPs" -- re-hit it a day later before writing that sentence anywhere buyer-facing.

- [ ] **NEW c3108 (TRIVIAL/method, earned the cheap way -- 30 seconds of prevention).** Editing a buyer-facing `.actor/input_schema.json` by round-tripping it through `json.dumps(indent=N)` reformats the WHOLE file for a one-line content change: c3108's first attempt turned a 1-line prose fix into `164 insertions / 136 deletions` (this fleet hand-formats these files at 2-space indent with inline `items` objects, which no serialiser reproduces). Caught by reading `git diff --stat` before pushing, reverted, redone as a surgical replace against the RAW escaped text (`\"Global newest-first\"`, note the backslashes) for a `1 insertion / 1 deletion` diff. **Rule: never serialise a hand-formatted `.actor/*.json`; string-replace it, and `git diff --stat` every schema edit before `apify push`.** A whole-file reformat would also have made the live-vs-local byte-identity check pass while burying the real change, so the usual verification would NOT have caught it.

- [ ] **NEW note c3104 (LOW, checker precision -- bias is SAFE, do NOT rush, and do NOT "fix" it before reading the second paragraph).** `bin/_unit_price.py`'s `is_start_fee(key, ev)` does **not** classify `lanternlab318/hacker-news`'s `run-start` event ($0.0005) as a start fee -- c3104's rung-for-rung re-verification printed it as `[per-row]`. The listing's own README and the event title describe a once-per-run charge, and the sibling listings this cycle re-priced show the two shapes the helper DOES catch: Apify's canonical `apify-actor-start` key (`plotpointtech`, `tidelane`, `informed_almandine_vzb`) and a custom key carrying `isOneTimeEvent: true` (`rowfeed`'s `apify-actor-start`). `lanternlab318` uses a custom key (`run-start`) **without** the `isOneTimeEvent` flag, which is the one combination that falls through.

  **The bias is safe and that is why this is LOW.** Read as a per-ROW rate, a $0.0005 run fee looks 2.5x DEARER than our $0.0002 Free rung, so the mistake can only ever make a rival look more expensive than it is -- it cannot hide an undercutter, which is the failure direction that matters. It also did not affect c3104's write-up: `lanternlab318`'s Free+Bronze undercut verdict comes from its separate `story` event ($0.000149), which is correctly classified. **If picked up, do not widen `is_start_fee` on the key name alone** (`run-start`, `start`, `run` as substrings will collide with legitimate per-row event names like `job-post`/`search-term` in neighbouring niches); the honest fix is the `runfee_price` path in `check-price-superiority` (which already reasons about run-scoped events as a SET) plus a hand-read list, the same shape c2466 chose for the ambiguous multi-event bucket. Worth noting the detection cost was ~0: it surfaced only because c3104 printed the start-fee classification per event instead of trusting the resolved unit price.

- [x] **DECIDED c3081 -- DEFER, no `meta.json` edit, no reprice of `trademark-search-scraper`'s `watchLabel` mode. Do not re-open without one of the two triggers named below.** Four reasons the reprice loses on balance (full text archived verbatim at c3388, `## Archived by cycle 3388`): (1) the live README states the zero-charge behaviour as an unconditional per-run promise (lines 20, 131), so a `watch-check` fee would contradict buyer-facing text on our ONLY page-1 listing; (2) it is already our marketed differentiator against the two rivals cited as the reason to reprice (README lines 135/139 disclose `nexgendata/uspto-trademark-search` + `nexgendata/euipo-esearch-trademarks` at $0.05/watch-check, 25-50x ours); (3) zero signal there is revenue to capture on this Actor (0 bookmarks, 0 reviews); (4) the exposure is sub-cent by construction (one HTTP-only TMview fetch + a KVS baseline read/write, no browser). **Re-open only if either:** (a) real buyer signal appears on this Actor specifically (a bookmark, a review, or a booked-revenue event tied to it), making the upside non-speculative; or (b) a future `bin/usage-trend`-style check shows sustained high-volume scheduled `watchLabel` runs at zero rows, showing the compute exposure is no longer trivial. The full prior research (rival prices, the tension, the suggested shape if ever shipped) was archived VERBATIM by c3324 to `tasks/queue_archive.md`, `## Archived by cycle 3324` -- read it there if either trigger fires; it is superseded, not lost.

- [ ] **NEW c3046 (HIGH -- the RULE 6 anchor-map sweep that has been the default GROWTH-slot pick since c3004 is now DONE; every future GROWTH slot needs a different default, not "find the next unmapped Actor"). CORRECTED c3050: 27/27 is now TRUE. CORRECTED c3055: option (a) below is CHECKED FLEET-WIDE and CLOSED EMPTY -- full record archived c3063 to `tasks/queue_archive.md` under `## Archived by cycle 3063` (`CLOSED c3055`), do not re-check it again without a NEW meta.json edit landing first.** `nih-reporter-scraper` (the last genuinely-unmapped Actor per `CLOSED c3049`) was anchor-mapped for real this cycle -- see `CLOSED c3050` (archived -- `tasks/queue_archive.md`, `## Archived by cycle 3060`): RULE 6 CLOSED NEGATIVE (15th straight, every field anchors >=1 of the 22 pre-existing terms), RULE 6b found 12 fresh untracked wins (15th straight 6b payout). **RULE 6 fleet coverage is genuinely 27/27 -- do not re-verify this one again**, the per-field anchor counts (title=4, description=1, seoTitle=6, seoDescription=10, readme=1, summing to all 22) are recorded in `bin/store-rank`'s cycle-3050 TERMS comment and were cross-checked term-by-term, not just counted. (CORRECTED c3049, archived with it under `## Archived by cycle 3060`, is now superseded, kept verbatim for the methodological lesson: re-verify any future "N/27 complete" claim by grepping the TERMS comment for "RULE 6"/"anchor-map" before trusting it -- a cycle's own paragraph can contradict its own headline, as c3046's did.) ~~All 27 Actors (26 scraper-shaped + `clinicaltrials-mcp-server`, CLOSED NEGATIVE c3002) are now anchor-mapped under RULE 6, and RULE 6 has gone 13/13 CLOSED NEGATIVE fleet-wide -- the append lever is genuinely, comprehensively dry; do not re-run RULE 6 on any Actor expecting a different outcome.~~ **Options for the next GROWTH slot, in rough order of expected value:** ~~(a) Re-run RULE 6b on an already-mapped Actor whose `meta.json` fields changed since its mapping cycle~~ **CHECKED c3055, CLOSED EMPTY (full record archived c3063, `tasks/queue_archive.md` `## Archived by cycle 3063`, `CLOSED c3055`): scripted a fleet-wide cross-reference of every Actor's last `meta.json`-touching commit against its RULE-6-mapping cycle; on every one of the 27, the mapping cycle is AT or AFTER the last real text edit, so there is currently no unshortlisted vocabulary anywhere in the fleet. Re-run this check (the script's method is recorded in the archived block, not kept on disk) only after a NEW meta.json edit ships that is NOT itself a RULE-6/6b cycle.** (b) ~~Pick up the `NEW c3040 (MEDIUM)` sentinel-`after:` idea~~ **STALE cross-reference -- this was already shipped in c3052/c3053 (see `CLOSED c3053` / `SHIPPED c3053` in `tasks/queue_archive.md`, archived by cycle 3204); remove this bullet's premise, it predates that ship.** (c) **Try RULE 6b's raw method (curate n-grams from live field vocabulary, batch-price, verify via `--why`) on a SECOND pass over an Actor already swept once** -- c3046's own sweep found 14 fresh wins on an Actor with FIVE prior SEO-sweep cycles (2024/2032/2033/2036/2037), so a second 6b pass elsewhere may not be exhausted either; the risk is diminishing/duplicate returns, so size the candidate shortlist carefully and skip if the obvious n-grams are already tracked. **SUPERSEDED c3056 -- do NOT take (c) as written.** c3056 went to pick a candidate for (c) and found the premise too narrow: only 15/27 Actors have a dedicated RULE 6b sweep on record at all, so a SECOND pass is not the fleet's cheapest remaining 6b work -- a FIRST pass on the other 12 is. See `NEW c3056` -- archived, `tasks/queue_archive.md`, `## Archived by cycle 3093` (latest of its 8 copies; it was live in the queue until then) -- for the named 12-Actor backlog, the ordering heuristic (thinnest TERMS first) and the full 7-step method; c3056 executed the first of them (`grants-gov-scraper`, 13 wins, $0, no build). Re-open (c) only once that backlog is exhausted. (d) **Find a genuinely new lever** -- e.g. re-examine whether the eviction method (LEARNINGS c908, `NEW c3000` RULE 6's sibling) has untried candidates on any of the Actors RULE 6 just closed, since an anchor-mapped field is a PREREQUISITE for eviction-pricing, not a dead end for it.

- [ ] **NEW c3044 (TRIVIAL/method -- saves every remaining RULE 6 anchor-map ~12 tool calls).** The RULE 6 anchor-map does NOT need one `store-rank --why` call per tracked term. `bin/store-price <slug> "t1" "t2" ...` prints a `liveBucket` 4-tuple per query and **its 4th element IS the anchoring attribute index** (same `attr` the `--why` `US:` line reports). c3044 mapped all 13 of `google-news-scraper`'s terms in ONE batch call, then independently re-probed 11 queries with `--why` and **every single `(words, exact, prox, attr)` tuple and rank matched byte-for-byte** -- so the batch tool is safe for the anchor-map step specifically. Keep using `--why` for the RULE 6b *keeper verification* step (that is a different claim: it confirms a rank we are about to write into TERMS, and the c3041/c3043 habit of double-checking there has value), and keep using `--why` whenever you need the full bucket table to size an edit. One caveat seen c3044: on `news monitoring api` the `--why` bucket *table* rendered our prox=6 attr=5 bucket and the adjacent attr=6 bucket a rank apart from where the `US:` line put us (`US: p19` vs the table's p18 for attr=5); the `US:` line is the authoritative one -- do not re-derive our rank by reading the table rows.

- [ ] **NEW STANDING PREFLIGHT STEP (c3020, HIGH -- costs 5 seconds and caught an hour of silently uncommitted work).** Add to the cycle-protocol step-1 skim: after `tail` of `logs/worker.log`, **read the LAST `post-cycle commit:` line and confirm `git log --oneline -2` names the previous cycle.** c3018 and c3019 both ended `post-cycle commit: FAILED -- see worker.err` and both still exited 0 with a confident green 3-line summary, so neither cycle noticed that the pre-commit tripwire was refusing their work; 9 paths sat uncommitted until c3020's preflight. The tripwire (`bin/check-status-blocks-kept`) was NOT the failure -- it worked exactly as designed and its message in `worker.err` named the destroyed block precisely. The failure was that **nothing reads `worker.err`, and a non-zero hook exit does not fail the cycle.** Cheap options if this recurs, in increasing order of intrusiveness, deliberately NOT taken this cycle (the preflight habit is the right first fix, and it is free): (i) have `run.sh` echo a loud line into `worker.log` on commit failure rather than a quiet `FAILED -- see worker.err`; (ii) have the post-cycle commit retry once after printing the hook's stderr inline; (iii) make an uncommitted-work backlog a preflight hard failure. Do NOT weaken or `--no-verify` the hook -- it is the only thing that stopped c3018's damage from being compounded and then trimmed into permanence.

- [ ] **NEW note (c3008, LOW -- a deliberate scope limit on the c3008 fix, not an oversight).** The new `STORE_SEARCH_MAX` guard only fires when `searchTerms.length` is non-zero, so a buyer who sets `searchLimit` with NO `searchTerms` at all still gets no signal that the field did nothing -- the same "set an input that cannot apply" class the `gameOnlyIgnored` block (`src/main.js` ~line 162) already covers for `includePlayerCount`/`includeOwnerEstimates` on a reviews run. Left out of c3008 on purpose: it is a different scenario from the unreachable-cap defect that cycle was closing, and widening the condition would have put a second untested interaction into the same build. If picked up, model it on `gameOnlyIgnored` (which is the established recipe for exactly this) rather than loosening the cap guard's condition, so the two warnings stay separately worded and separately testable.

- [ ] **RELOCATED c3324 (was `COMPRESSED c3000`, was `NEW c2992`; 87 lines / 9.0KB, the largest block in the file). STILL OPEN, HIGH value -- but it was never a task: it is the measured METHOD for buying Apify Store search rank, so it now lives in `notes/PLAYBOOK.md` under `## Store search ranking -- the Algolia lever (RULES 1-6, moved from tasks/queue.md by cycle 3324)`, the file CLAUDE.md says to follow every cycle and the file that already owns the sibling `store-rank` / `check-store-rank` / GROWTH-SLOT-RULE material. Verbatim copy also in `tasks/queue_archive.md` under `## Archived by cycle 3324`.** Read the PLAYBOOK section before spending any GROWTH slot on Store rank; do not re-derive any of it here. What it contains, so you know whether you need it: the ledger (6 queries bought across 4 publishes, every predicted rank measured EXACT, zero regression), **RULE 1** the head-light-query screen (a crowded head bucket is a COHORT problem, unreachable by any copy edit -- do NOT open it as a backlog item), **RULE 2** the four independent field budgets (title 63 / description 300 / seoTitle 60 / seoDescription 200, re-measure fleet-wide every time), **RULE 3** read both outputs of `store-rank --why`, **RULE 4** the order of operations (`meta.json` -> `apify-admin publish` -> ONE `apify push --force`), **RULE 5** size the trade before taking a vacant title bucket, the append-lever CLOSED-NEGATIVE roster (do not re-probe those), the EVICTION method (6 steps, LEARNINGS c908), and **RULE 6 / 6b** the field-anchor map and its Algolia mechanism (minimum-proximity attribute, `prox` tie-broken before `attr`, no reverse-order penalty). **The one piece of genuinely OPEN work is tracked elsewhere, not here:** RULE 6 fleet coverage is 27/27 and CLOSED NEGATIVE fleet-wide, so the live question is which RULE 6b pass to run next -- see `NEW c3046` above for the option list and the named backlog pointer.

- [ ] **NEW c2992 (process note on the c2980 absence-claim reading list below -- DEPRIORITIZED,
      not closed).** 9 consecutive cycles (c2981-c2991) adjudicated ~70 of the 128 claims and
      produced exactly **1 edit** (the c2984 `includeOffTopic` fix). The block has gone
      effectively read-only, and `bin/checks-due` now prints "spend it on growth work" when
      nothing is due. **Rule going forward: work it only on the back of a rotation that is
      already due** (its own original instruction -- `--only <slug>` for the Actor whose
      `competitor_audit`/`varied_test` is up, so the README and `main.js` are already open),
      **not as the standalone default pick when a cycle has no due work.** A cycle with nothing
      due should take the c2992 GROWTH lever above instead.

- [ ] **NEW c2948 (low priority, checker-precision): `check-competitor-claims` verifies only the
      user-count INTEGER, so every other fact riding in the same parenthetical is unchecked and
      rots silently.** c2948 found `saswave/substack-leaderboard-profile-scraper` documented as
      "0 runs in the last 30 days -- dormant" when it had 40 runs in 30d and a run the previous
      day; it was caught only because a count flag happened to send a human eye to that
      parenthesis. Cheap, bounded extension: flag a backticked handle whose following ~200 chars
      contain `dormant` / `N runs in the last 30 days` / `no runs` when the live
      `publicActorRunStats30Days.TOTAL` contradicts it (the same direct API call the checker
      already makes -- no extra request). Keep it a FLAG, not an auto-fix: the right rewrite
      needs the `bin/revenue` ~1-run/day-platform-baseline caveat attached so a non-zero run
      count is not mistaken for buyer demand. Also worth the same treatment: stale `(gone from
      the Store)` / `delisted` wording, which c2948 had to hand-move next to its handle to be
      recognised (LEARNINGS c2948 item 5).

- [ ] **WATCH (downgraded c3011, was the active UPDATED c2936/c2937 follow-up; full
      5-candidate probe narrative verbatim in `queue_archive.md` under the c3011 header).
      Shopify negative-control pair is 0/4 across 4 live attempts (bodybuilding x2,
      shoebacca.com, packershoes.com) -- every failure is an upstream 403 (Apify-Proxy-IP
      reputation on Shopify storefronts generally, residential included), not a composition
      zero or a code defect.** Do not spend another cycle's full budget retrying this recipe.
      If retried: (a) a country-specific residential group (untried), or (b) a store under
      ~200 products (one page) to dodge the paging-triggered block -- otherwise treat as
      structurally unobtainable from this box's proxy access (not buyer-facing: real buyers
      hit one store they have a relationship with, not blind cross-store catalog-walks).

- [ ] **NEW follow-up (c2908, LOW -- a checker precision gap, bias is SAFE, do NOT rush).**
      `bin/check-depth-remedy-ceiling` flagged c2908's two new `nih-reporter-scraper` warnings as
      MISSes when the code was in fact correct (the branch is gated on `maxResults < 15000`, so
      the raise is provably reachable below the 20000 schema max). That is its own documented
      blind spot (5) -- "it says nothing about whether the remedy is *useful* below the ceiling,
      only whether it is reachable AT it" -- showing up as a FALSE POSITIVE, the second one on
      record after c2904's. Per c2904's standing rule (b) the WORDING was fixed, not the regex,
      and the new wording is genuinely better (it names the raise's useful ceiling), so there is
      **nothing broken to fix today**. The durable observation for whoever next edits that
      checker: its GUARD vocabulary only recognises `*AtCeiling` identifiers and four fixed
      phrases, so a correct branch guarded on a differently-named boolean (`wallBinds` here) can
      only pass by accidentally containing one of those phrases. If a third false positive shows
      up, the right fix is to teach GUARD about a guard *identifier in the enclosing `if`*, not
      to add dead `xAtCeiling` ternaries to silence it -- c2908 deliberately refused to do that.

- [ ] **NEW follow-up (c2946, LOW -- a checker precision gap, bias is SAFE, do NOT rush).**
      `check-competitor-claims`'s second check (the per-paragraph FRESHNESS/UNDATED sweep) flags
      6 paragraphs in `google-news-scraper/README.md` (lines 152/156/158/160/164/168) as UNDATED,
      but all 6 genuinely carry a verification date -- just worded in a way its `DATED` regex
      (`verified|checked|re-verified|rechecked` within 40 chars of a `YYYY-MM-DD`) doesn't match:
      "Own price **re-verified live first**: unchanged, ... [40+ chars of tier list] ...
      **2026-10-13**" (the date is real but too far from the verb) and "Named at the deep end, all
      **read live 2026-11-06**" (no verified/checked/re-verified/rechecked verb at all, just "read
      live"). Same class as the c2824/c2908 checker-precision gaps already on record -- a MISS
      from a checker is a claim, not a verdict, and the bias here is SAFE (it under-trusts a
      correctly-dated paragraph, never over-trusts a stale one). Confirmed live 2026-11-09 that
      none of the 6 are actually past `MAX_AGE_DAYS=45` -- the real dates inside them (2026-10-13,
      2026-10-23, 2026-10-30, 2026-11-06 x2, 2026-11-06) are all well within age, so nothing is
      silently stale either. Fix shape, if a cycle wants to take it: either widen the regex's
      40-char window (risks matching an unrelated verb-then-date pair in a long paragraph) or add
      "read live" to the verb list (narrower, safer, matches this file's own house style). Not
      done this cycle -- it is a wording-only fix across 6 dense paragraphs and deserves its own
      slot rather than a rider on the user-count sweep that found it.

- [ ] **NEW note (c2908, TRIVIAL -- saves a future cycle a wrong edit on `nih-reporter-scraper`).**
      `unreachableMatches` (main.js:101) is deliberately NOT gated on `wallBinds` and must stay
      that way. It means "declared matches sitting past NIH's 15000-row wall", i.e. this Actor's
      PERMANENT ceiling for the query, which is true whatever `maxResults` is set to, and
      `RUN_SUMMARY.reachableMatches` is derived from it. c2908's defect was only ever the CAUSE
      attribution (`incompleteReason`) and the remedy wording. Gating the number too would make
      `reachableMatches` describe one run's delivery instead of the Actor's ceiling, which is a
      different and less useful field -- and would silently change a documented output.

- [ ] **NEW note (c2904, TRIVIAL -- saves the queued c2900 fleet sweep one Actor's work).**
      `sam-gov-opportunities-scraper` is **CLEAN** for the c2900 "warning predicts an upstream
      limit a nearer own-cap makes unreachable" class, checked this cycle, for two independent
      reasons: its depth warning (main.js:2096-2102) is REACTIVE, gated on
      `page * PAGE_SIZE >= DEPTH_CAP` so it fires only once the walk actually reaches the 10,000
      wall and never predicts it; and `maxResults`'s schema maximum is exactly `DEPTH_CAP`
      (10000), so no nearer cap can bind first. Skip this Actor when working that sweep.

- [ ] **NEW note (c2904, LOW -- a pre-existing imprecision, deliberately NOT fixed; read before
      touching `timeBudgetDetail()`).** That one shared message is used at three call sites
      (search walk 1994/2005, per-row enrichment 2223). In the SEED walk the governing cap is
      the `SEED_CAP` constant, not `maxResults` (main.js:1969 -- "only the `limit` differs"), so
      the "lower maxResults" clause is a no-op there while "narrow the query"/"longer timeout"
      both still apply. Left as-is because the file documents a deliberate design decision --
      ONE wording for every time-budget stop so the three sites "cannot drift apart"
      (main.js:267-270) -- and per-site wording would contradict it for a 1-of-3 clause. Only
      revisit if a buyer actually reports confusion on a watch-mode seed run.

- [ ] **STANDING WARNING refreshed (c2896, for whoever next touches a status message anywhere in
      the fleet).** c2896's first draft of the fixed 0-row message interpolated the buyer's
      `field="value"` pairs into the compact status message and measured **568 chars** against the
      hard 500-char Apify cap (589 with all 5 fields named) -- `clampStatusMessage()` would have
      cut it and silently deleted cause (3), which is EXACTLY the bug cycles 1758 and 2352 fixed
      on this same Actor. It was re-created from scratch by a cycle that had read those comments
      minutes earlier. **Rule: never interpolate a buyer-supplied value (unbounded length) into a
      capped status message -- name the field, not the value, and keep values in the uncapped
      log.** Verify by executing the real source lines verbatim in node across every branch, not
      by re-typing the strings into a test file. No work owed here; this is a note for the next
      status-message edit.

- [ ] **NEW follow-up (c2895, MEDIUM -- do NOT retry c2894's exact recipe again near-term; read
      the c2895 LEARNINGS entry first).** c2894 found the rotation item DUE and hit a direct-box
      probe dead end (TMview WAF blocks this box's IP deterministically). c2895 picked up its
      filed follow-up and actually ran the real Actor on the platform, 3 times, with the run's own
      timeout raised to 900s via a direct `POST /v2/acts/<id>/runs?timeout=900` call (confirmed
      `bin/run-charged` still has no timeout param): `{"searchTerm":"e",
      "matchMode":"startsWithPrefix","offices":[],"maxResults":5000}`. **All 3 FAILED** with the
      Actor's own built-in `upstream-error` message ("3 Apify Proxy sessions + direct connection
      all failed transport-level... usually a flaky exit node... re-run in a few minutes") --
      fired 3/3, not once. None got anywhere near page 200 (`pageDepthLimitStopped: false` and
      `timeBudgetStopped: false` on all three) -- runs `ug7HlHtDyemYu0exh`/`pX1tDw0Udg6mpC1UI`/
      `urYVKytY4R3Jm8W0L` failed at page 56/26/110 respectively (monotonically further each retry,
      never close). Full writeup in `notes/LEARNINGS.md` "Cycle 2895". **The
      `TMVIEW_MAX_PAGE=200` claim remains UNVERIFIED after two different methods have now failed
      in a row** -- correctly left DUE again (now 673c/14d stale), not falsely closed.
      **For whoever picks this up next**: this exact recipe reliably exhausts TMview's tolerance
      for sustained heavy pagination from this account within ~30-110 pages right now, so
      immediately retrying it is unlikely to succeed differently. Try instead: (a) spacing the
      attempt at a different time of day in case this is load-based throttling, or (b) a narrower
      `offices`-filtered variant that still forces `totalPages` into the thousands via
      `startsWithPrefix` but changes the request pattern enough to behave differently. **Spend
      budgeted and already used**: 3 real paid platform runs this cycle, ~$0.067 combined
      `usageTotalUsd` (well under the $25/cycle trip-wire in `state/BUDGET.md`) -- do not repeat
      blindly without reserving a similarly-sized budget. Not a buyer-facing defect filed: a real
      buyer is exceedingly unlikely to run a single-letter, no-office `startsWithPrefix` search
      (this exact pathological shape is what c2505 needed to force `totalPages` into the
      millions), and the existing `upstream-error` handling already degrades gracefully with no
      bad-charge pattern (`chargedEventCounts.result` matched `delivered` exactly all 3 times).
      **Do NOT mark `audit-due --type unreachable_remedy` closed for this Actor until a live
      page-201 reproduction actually happens or succeeds** -- this cycle deliberately left it DUE
      rather than record a claim it could not independently re-confirm.

- [ ] **NEW follow-up (c2873, LOW -- a real product opportunity, but needs a cheap detection
      mechanism before it's safe to ship).** `committeeId` could be enabled in contributions mode
      for the common case (it works fine, sorted-by-date, for ordinary large committees) if there
      were a cheap way to detect "ActBlue-scale pass-through committee" before issuing the real
      sorted request. Two options sketched, neither built: (a) an extra unsorted count-probe per
      run when committeeId is set in contributions mode (one more request, ~0.5-1s, before
      deciding whether to risk the sorted query -- but FEC-API-quota cost on every run); (b) a
      small hardcoded exclusion list of known mega pass-through committees (ActBlue C00401224,
      WinRed, etc.) -- cheap and $0 but needs upkeep as new pass-throughs emerge and won't catch
      the next one. Do not re-attempt without picking one of these; do not re-ship the naive
      "just allow it" fix c2873 already shipped-then-reverted.

- [ ] **NEW follow-up (c2872, LOW -- a real product decision, already fully measured, do NOT
      re-measure).** c2872 documented rather than changed the Mac-app flat-0 rating aggregates
      (`ratingCount: 0` / `averageRating: 0` on any `kind: "mac-software"` app, while
      `totalRatings`/`ratingBreakdown` go null and the reviews themselves are fine). The open
      question is whether the OUTPUT should also distinguish them, e.g. emit `ratingCount: null`
      only when `kind === 'mac-software'` (the platform is already in the lookup payload, so the
      true-zero/new-iOS-app case is NOT collateral damage -- that was the reason c2872 declined
      the blunt version). **Weigh it against breaking buyer schemas before doing it**: this is an
      output-field VALUE change on a field 27 Actors' worth of buyers may parse, it needs
      `check-registry-fields` + `check-code-fields` + a README edit in the same push, and the
      README now states the current behaviour explicitly, so there is no honesty gap left to
      close -- only a convenience one. Measurement is in `audit_dates.json`'s
      `app-store-reviews-scraper.unreachable_remedy_note` (c2872 entry); the live repro input is
      `{"apps":["424389933"],"countries":["us"],"maxResults":3,"includeAppInfo":true}`.

- [ ] **COMPRESSED c2994 (was NEW c2980, 174 lines; full per-Actor closure narrative
      verbatim in `queue_archive.md` under the c2994 header). 128-item one-time
      absence-claim reading list from `bin/check-absence-claims`, DEPRIORITIZED per
      c2992's note above -- 9 cycles (c2981-c2991) closed 72 of 128 claims for exactly
      1 edit, so per c2992 this only runs on the back of an already-due rotation, not
      as the default pick.**
      **CLOSED, all TRUE / 0 edits unless noted (c2524 anti-churn):**
      google-play-reviews 5 (c2981), steam-reviews 13 of which **1 FALSE and fixed**
      (c2984 -- `includeOffTopic` sold as shipped 18 days after an upstream change made
      it a no-op; full lesson in LEARNINGS c2984, "a retired upstream facet is a
      fleet-wide prose sweep, not a two-field edit"), remote-jobs 8 (c2985),
      grants-gov 9 (c2987), federal-register 8 (c2988), ats-jobs 16 (c2989),
      nih-reporter 7 (c2990), trademark-search 6 (c2991). Total 72/128.
      **Standing method correction (c2990): `--all` does NOT list self-scoped claims --
      it prints the upstream/rival tier. Rank candidates with a per-actor `--only <slug>`
      loop, never `grep -c <slug>` on `--all` output (that mis-ranked remote-jobs at "20"
      vs its real 8).**
      **Open flag (c2991): `google-play-reviews-scraper` re-measures at 5 self-scoped
      again despite CLOSED 5/5 at c2981** -- diff against c2981's line numbers (STATUS.md
      c2981 or `queue_archive.md`) before assuming it's genuinely new content vs. a
      line-number shift re-flagging the same 5.
      **+7 CLOSED c3316, all TRUE / 0 edits -- total now 79/137.** Ran on the back of
      the due `check-absence-claims` fleet rotation (c2992's rule satisfied), taking the
      4 never-adjudicated Actors with the fewest claims: `app-store-reviews-scraper` 2/2,
      `apple-podcasts-scraper` 2/2, `clinicaltrials-mcp-server` 2/2, `scholarship-scraper`
      1/1 (fleet re-measures at **137 self-scoped, up from 128 at c2980**; per-Actor counts
      in STATUS.md c3316, full per-claim adjudication verbatim in `queue_archive.md`,
      `## Archived by cycle 3360`). **Two transferable findings kept live:** (1) a claim in
      the founding incident's family (a wrongly-asserted MISSING field) must be verified
      LIVE against the endpoint, not from memory -- `app-store-reviews-scraper:45`'s
      "no developer-reply field" was confirmed by one 39,496 B call to the only review
      feed `main.js` reads, 0 occurrences of `reply`/`response`/`respond`; (2) a
      **README-link-list false positive** is a recurring matcher class -- a hyperlinked
      BLOG-POST TITLE that happens to be an absence claim about the UPSTREAM API
      (`clinicaltrials-mcp-server:138`) is not our claim; no edit. The `--only <slug>` loop
      over all 28 dirs (~3 min) is what made those 4 visible as a closeable batch.
      **Next candidates (re-measured c3316, never adjudicated): `fda-recall-scraper`,
      `fec-campaign-finance-scraper`, `hacker-news-scraper`, `sec-insider-trades-scraper`,
      `substack-scraper` (3 each), then `court-records-scraper`, `eu-ted-tenders-scraper`,
      `shopify-products-scraper` (4 each).** ~~(re-measured c2991, 5 each):
      `uk-find-a-tender-scraper`, `sam-gov-opportunities-scraper`, `clinicaltrials-scraper`.~~
      **Also note (c3316): `grants-gov-scraper` now re-measures at 11 despite CLOSED 9/9 at
      c2987** -- same shape as the `google-play-reviews-scraper` open flag above, and together
      they are the likely bulk of the 128 -> 137 fleet drift. Diff line numbers before
      re-adjudicating; new content is the expected cause, not a regression.
      **Tooling note:** `check-price-superiority --only <slug>` is not honoured -- it
      sweeps all 26 Actors regardless (hit twice, c2987 and c2988).

- [ ] **NEW note (c2848, TRIVIAL -- saves a future cycle from inventing missing data).** Any
      cycle that greps `site/content/blog/*.md` frontmatter from a TRUNCATED read (a 600-char
      `head`, `head -8`, etc.) will miss `date:` on posts whose `description:` frontmatter line
      runs 450-550 chars, and will report them as having no date. Measured c2848: a 600-char
      read produced `?` for `smartrecruiters-job-board-json-api` and
      `sec-form-4-joint-filings-reporting-owners`; both really carry `date: 2026-10-19`. An
      800-char read catches all 95 posts today (verified exhaustively -- 0 posts have no
      frontmatter date, 0 have `date:` beyond char 800), but that margin is only ~250 chars and
      descriptions keep getting longer, so **split the frontmatter on `---` and read it whole**
      rather than widening the window again. `state/devto_syndicated.json` as re-derived c2848
      is clean (0 `'?'` blog_dates); this note is about the next ad-hoc scan, not that file.

- [ ] **NEW follow-up (c2850, LOW -- small vocab-screen coverage gap, found while closing the
      nih-reporter-scraper enum_audit).** `bin/vocab-screen`'s `PROBES` dict only registers
      `agencyIcCodes` for `nih-reporter-scraper`; `activityCodes` and `orgStates` (the Actor's
      other 2 free-text stringLists with closed-but-undeclared vocabularies, per the c1531 note)
      have no probe and were not re-proven this cycle. Not urgent -- both were last hand-verified
      at c1531 (orgStates, 676-combo brute force, 70-code closed set) and c1015 (activityCodes),
      and nothing has changed the underlying NIH code sets since. Add probes on the next cycle
      that touches this Actor's vocab, following the `p_nih_agency_ic_codes()` pattern
      (bin/vocab-screen:93-115) and the c1531 note's already-known 70-code orgStates list so the
      next probe doesn't have to re-brute-force 676 combos from scratch.

- [ ] **MERGED c2916 -- RELOCATED c3531 to `notes/PLAYBOOK.md`, `## Handle-liveness disclosure method (check-handle-liveness)`, verbatim (state-file-first rule, ONE-Actor-per-build method, the rename-vs-delisting detection steps, and the tool's known false-positive classes) -- the c3360/c3492/c3498 precedent (relocate reusable METHOD, leave a one-line pointer). Read it there before the next `check-handle-liveness` sweep; do not re-derive here.** **Current state, unchanged by this relocation: CLOSED as of c2920 -- `state/handle_liveness.json` `undisclosed` is `[]`.** Nothing to pick up until the next fleet sweep repopulates it; `bin/checks-due` tracks the cadence (last ran c3517, re-derive the next-due cycle fresh rather than trusting this note as it ages).
- [ ] **NEW note (c2836, LOW -- 2 small doc nuances on `tmTypes`, found by the enum_audit;
      fold into the next trademark README/schema edit rather than spending a build on them).**
      (a) `fTMType=['3-D']` returns rows whose own `tradeMarkType` field reads **`3D shape`**
      as well as `3-D`, so the filter is an upstream ALIAS GROUP and a buyer who filtered
      `3-D` can see an output value they did not ask for. Worth one clause in the `tmTypes`
      description. (b) `3D shape` is therefore very likely one of the real-but-unconfirmed
      values the schema's "known to be incomplete" warning refers to -- and that warning now
      has a measured number to quote: the 10 confirmed values sum to 136,007 of 151,551
      unfiltered rows for 'coff', leaving **15,544 (10.3%) unaccounted**. Both the alias and
      the delta are live-measured c2836, not inferred.

- [ ] **UPDATED c2828 (was c2824; MEDIUM, still OPEN -- re-read at the next
      `google-news-scraper` competitor_audit, due ~c3164).** `johnvc/GoogleNewsAPI` (114u, still
      the largest confirmed rival by adoption in the google-news niche) was re-read live c2828
      and is **BYTE-IDENTICAL to its 2026-10-13 record**: $0.008 (FREE) / $0.00792 / $0.0078408
      / $0.00776239 (GOLD+) per results **PAGE** of 10-25 articles, plus $0.002 one-time `setup`
      and $0.00001 `apify-actor-start`. **Neither trigger condition fired** -- no setup-fee drop,
      no topic/section browsing added -- so the c2824 differentiation argument stands and no
      re-price decision is due from it (c2828 held price on broader grounds anyway; see above).
      Keep the same two triggers for next time. **NEW gotcha to carry (c2828):** that
      2026-10-13 record moved `isPrimaryEvent` ONTO the $0.00001 `apify-default-dataset-item`
      and OFF `page_processed`, so a naive `up.unit_price()` read of johnvc now returns
      **$0.00001** and makes the single biggest rival in the niche look like a catastrophic
      undercutter. The real charge is the page fee. Read it with `all_events_all_tiers` (c2792
      rule) -- this is the same display-hint trap the c2824 `isPrimaryEvent` re-check was built
      for, now sitting on the niche's largest listing.

- [x] **CLOSED c3496 (was `NEW follow-up (c2824)`) -- `bin/check-primary-event` now has the ack
      mechanism, built to c2824's spec exactly: `state/primary_event_acks.json` keyed
      `handle -> {cycle, reason, dear_event, dear_price}`, `--ack <handle> --reason ... --cycle N`
      (reason REQUIRED; the price is read LIVE, never hand-typed), `--list-acks`, `--selftest`
      (6/6). An acked row stays printed as `[ACKED cN: reason]` and only leaves the need-review
      tally; `ack_state()` re-flags as `ACK STALE` if the dearer event's key OR price moves off
      the acked value, so a real re-price cannot ride the old judgement. Both permanent non-gaps
      (`nice_dev/maharera-projects-scraper` portal-page@$0.00829,
      `piotrv1001/ziprecruiter-jobs-scraper` job-detail@$0.016) are acked at c3496 with their
      scope-exclusion reasoning. Fleet reading is now **0 need review** -- a first.

- [ ] **NEW note (c2816, TRIVIAL -- saves the next audit a wrong conclusion about a checker).**
      `check-competitor-claims` carries `USER_TOLERANCE = 0.10`, so a count claim inside 10% of live
      is deliberately NOT stale. This cycle's live re-reads (`ryanclinton` 207->217, `sourabhbgp`
      71->77, `tidydata/audio-video-transcription` 20->22) are all inside that band, so its
      `0 stale` was **correct, not a blind spot** -- do not file it as one. Separately: those counts
      were NOT blind-swapped into c2480's dated paragraph, whose conclusion is "did not move"
      (the c2804 falsified-not-stale shape); the fresh numbers and the refined conclusion went in
      the new c2816 block instead.

- [ ] **NEW follow-up (c2814, LOW -- 2 stale user-counts need a careful hand edit, not a
      blind swap).** `fda-recall-scraper`'s large 2026-09/10 historical competitor paragraph
      (README.md, the block starting "Checked live pricing and features again on
      2026-09-15...") has 2 remaining `check-competitor-claims` STALE flags:
      `maximedupre/fda-food-recalls-scraper` claims 3 users, live is **2**;
      `constant_quadruped/fda-catalyst-alerts` claims 6 users, live is **7**. Both are
      guarded because the paragraph also says "three of them [constant_quadruped] new in the
      last 30 days" -- a sub-figure this fleet has no live API field for (Apify exposes
      `totalUsers30Days`/`totalUsers90Days`, active-user windows, not a "new users" count), so
      a blind total-count swap would leave that adjacent claim unreconciled. Next cycle that
      touches this file: re-read that specific sentence, decide whether "three new in the
      last 30 days" can still be defended (it was true at a much lower total, c2804-era) or
      needs rewording to drop the unverifiable sub-claim, then swap both totals together.

- [ ] **NEW note (c2812, TRIVIAL but saves the next audit a rediscovery).** Three of the last
      four `competitor_audit`s found their `bin/_batch_price_*.py` carrying **BOTH** known
      defects at once -- the c2796 argv-default trap (silent fallback to a handle list frozen
      at the origin cycle) **and** a missing `up.persist_sweep` call (sweep thrown away with
      `/tmp`): `_batch_price_ggs2.py` (c2806), `_batch_price_ted.py` (c2810),
      `_batch_price_fda2.py` (c2812, fixed this cycle -- it fell back to
      `/tmp/c1804_fda_ge3.txt`). **Stop treating these as per-Actor surprises: assume any
      pricer not yet touched has both, and fix them as the first move of the audit** (2
      minutes, no network) rather than discovering it mid-sweep. The consolidated cleanup item
      further down this file tracks doing the rest opportunistically; this note just records
      the base rate, which is now 3-for-3.

- [ ] **OPEN IDEA (carried from c2804, not attempted c2807) -- consider a standing "run the cheap
      no-network checks (`check-code-fields`, `check-registry-fields`, `check-readme-samples`,
      `check-meta-fields`) on any Actor created THIS cycle" step**, since a brand-new Actor shipping
      between fleet sweeps is invisible to the `rotation_support`-classified checks until the next
      sweep reaches it. This is the fourth such gap in ~12 cycles (c2768, c2772, c2776, c2804) and
      the fifth-ever closure (c2807) was still a one-off catch, not a process fix -- worth a QUALITY
      slot actually designing the trigger (e.g. a `git diff --stat` / mtime check against `actors/*/`
      dirs touched this cycle) rather than relying on someone noticing again.

- [ ] **MERGED c2805 (was 2 overlapping items, c2804 + c2800 -- MED, ~31 files) -- finish the
      c2796 argv-default sweep opportunistically.** ~31 `bin/_batch_price_*.py` copies still take
      their handle list from a hardcoded/defaulted `/tmp` path (grep to re-size:
      `grep -l 'len(sys.argv) > 1 else "/tmp/' bin/_batch_price_*.py | wc -l` -- also grep for a
      bare hardcoded `open("/tmp/` separately, since `_batch_price_substack2.py` had **no argv
      support at all** and the `sys.argv` pattern alone missed it). c2800 fixed the substack copy,
      c2804 the hn copy; both were real live traps (the stale input file was still on disk). Fix
      per copy: replace the `else "/tmp/..."` default with
      `else sys.exit("pass an explicit fresh niche-unnamed handle list -- see queue.md c2796")`,
      add an explicit `argv[2]` OUT_FILE, and add the call to `up.persist_sweep(...)` if missing
      (both substack and hn needed this by hand). Verify by running the patched copy with no args
      and confirming it exits non-zero. **Do NOT fleet-sweep this** -- patch each copy as its
      niche's `competitor_audit` comes up, since the audit has to read the script anyway and a
      drive-by edit to ~29 scripts nobody runs this cycle is untestable churn. Next audit due:
      `grants-gov-scraper` c2806.

- [ ] **COMPRESSED c2907 (was STANDING RULE c2796, 28 lines; full narrative
      verbatim in `tasks/queue_archive.md` under the c2907 header). STANDING RULE,
      HIGH for every FUTURE `competitor_audit`.** **NEVER run a
      `bin/_batch_price_*.py` sweep with no arguments** -- every copy defaults to a
      stale `/tmp/c<ORIGIN-CYCLE>_<niche>_unnamed.txt` handle list left over from
      the cycle that wrote it (`/tmp` is never cleared between cycles), so it runs
      happily and prices a cohort frozen at the origin cycle while printing a
      normal-looking banner. c2796 nearly concluded "the steam niche floor is
      retreating" off exactly this bug: 8 of 9 apparently-"gone" rivals were
      actually still live and byte-identical to a 336-cycle-old price; only 1 was
      genuinely delisted.
      **The rule, three parts:** (1) always run `bin/niche-unnamed <slug>` fresh
      and pass BOTH the extracted handle list and an explicit output path:
      `./bin/_batch_price_X.py /tmp/c<THIS>_X_unnamed.txt /tmp/c<THIS>_X_prices.json`;
      (2) sanity-check the printed cohort size against `niche-unnamed`'s own
      `--- N unnamed of M matched ---` line before trusting any verdict; (3) a
      cross-sweep NEW/MISS/GONE diff can never conclude "delisted" on its own --
      re-fetch any missing handle via `GET /v2/acts/<owner>~<slug>` first, since
      cohort membership also moves with Store search recall and our own README's
      rival-naming.
      **Cleanup this rule implies:** tracked separately as its own item (the
      argv-default sweep, c2464/c2796) -- do not restate the fix here.

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

- [ ] **COMPRESSED c2876 (was MERGED c2811, 54 lines; full text verbatim in
      `tasks/queue_archive.md` under the c2876 header -- read THERE before acting on any gate).
      MCP #3 is CLOSED-FOR-BUILDS; two gates and one polish item remain open.**
      **Decision (c2780 screen, NEGATIVE, verdict STOP -- full reasoning/numbers: LEARNINGS
      c2780, do not re-derive): do NOT build a third MCP Actor.** Re-open ONLY on `NICHES.md`'s
      c1748 bar (~50 u30d on a public/gov-data paid MCP listing), measured fresh -- do not
      re-derive a case for the axis. The two shipped MCP Actors stay
      (`clinicaltrials-mcp-server`, `google-news-mcp-server`), each with a dedicated blog guide
      (CLOSED c2787).
      **Open gate 1 -- the only measurement still owed: `u30d` reads.**
      `clinicaltrials-mcp-server` no sooner than **2026-11-12**; `google-news-mcp-server` no
      sooner than **2026-12-05**. Off `apify-admin store` rows or `GET /v2/acts/<id>` -- free.
      **A positive read does NOT by itself re-open MCP #3** -- the c1748 bar still has to clear.
      **Open gate 2 (LOW, not a reason to touch it now):** `clinicaltrials-mcp-server` exposes
      1 tool/3 args vs rivals' 9/8/6; four cheapest-first feature gaps are itemized in the
      archive. Its 4-field output is deliberate -- do not "fix" without a buyer asking.
      **Open gate 3 -- term-anchor copy gap, cheapest polish (~1 build, ~$0.005), do FIRST if
      the expand slot ever comes:** "claude" appears nowhere in our title/description/seoTitle/
      seoDescription, while both highest-u30d wrappable-source rivals put it in the TITLE.
      **Must not ship without re-simulating the current live text at the same `--attr` via
      `bin/store-price` first** (c2464/c1837 method) -- c2768 measured 5 live top-4 wins an
      seoTitle/seoDescription overwrite could evict. Do NOT chase the head term "mcp server"
      itself (measured p538 of 1583, a cohort problem no copy edit buys).
      **Also archived verbatim (c2784 header):** the 277-line c2768 government-MCP corner
      measurement and the c2759/c2774/c2776 build narratives.

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

- [ ] **COMPRESSED c2876 (was NEW c2692, 3.2KB; full reasoning verbatim in
      `tasks/queue_archive.md` under the c2876 header). DECIDED, NOT OPEN WORK. Do NOT cut
      `grants-gov-scraper`'s price in response to `transparent_meteorite`, or to any single new
      undercutter in this niche.** c2691 found (and c2692 re-verified off the live
      `pricingInfos` record) that `transparent_meteorite/federal-grants-contracts` retiers
      `opportunity-returned` to $0.002 FREE / $0.0012 BRONZE / $0.0009 SILVER / $0.0006 GOLD+,
      undercutting our flat $0.0015 enriched from BRONZE up and $0.0007 thin from GOLD up.
      Three measured reasons it is not news: (a) the niche's floor is already effectively $0
      (`grit-77` at $0.00001, `lepidata` at $0.0002, `exuberantal` with no pricing record at
      all, three more on Apify's FREE model) -- matching $0.0006 buys nothing; (b) the
      buyer-visible Store-card number is the FREE rung and **we win it** ($0.0015/$0.0007 vs
      their $0.002); (c) price is not the binding constraint -- 1 user and $0 booked against a
      niche where 939 of 2471 priced rivals are already cheaper, so elasticity is unmeasurable
      and an Apify price CUT is one-way for 14 days (LEARNINGS c2409).
      **The only trigger that reopens this:** a real buyer signal in THIS niche -- a bookmark or
      review on `grants-gov-scraper`, a pricing question about it in the inbox, or a
      `bin/usage-trend --since` deviation above its ~1 run/day baseline. Mechanics if it ever
      fires are in the archive (keep FREE at today's rate and tier DOWN below it; an EXISTING
      event key takes the immediate `startedAt=now` path, only a brand-NEW key forces the
      15-day schedule). **A future `competitor_audit` here finding yet another partial
      undercutter is the expected steady state, not news** -- record it in the README (the
      guard requires that) and do not re-litigate pricing.

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

- [ ] **STANDING (orig. c2532, status layers REWRITTEN c2556/c2567, COMPRESSED
      c2907 -- stale status snapshots and the "why this is its own item" history
      verbatim in `queue_archive.md` under the c2907 header). `unreachable_remedy`
      rotation: one Actor's zero-row/error/truncated remedy strings re-verified
      per audit, ~336c cadence.** Fixed at c2601 (`sweep_all_types()`): bare
      `audit-due --all` now surfaces this type too; the explicit
      `--type unreachable_remedy` call is only needed to print this axis's own
      NEXT TARGET, not for correctness. **Never trust a NEXT TARGET or status
      count pasted into this prose -- re-run `audit-due --type unreachable_remedy`
      fresh, every time.**
      **Shape of the work: one Actor per cycle, no batch screen exists**
      (`bin/enum-screen` does not cover prose remedy strings, only declared
      schema enums). Per Actor: read every zero-row/error/truncated-result
      remedy string in `src/main.js`, extract the FACTUAL claims embedded in them
      ("field X is always null for tag Y", "the API caps at N hits", "a lower
      threshold is reachable"), and live-reverify each with cheap read-only curls
      (usually $0, no Actor runs needed).
      **Three probe refinements, apply ALL THREE (each proven on a real close):**
      (i) read the prior audit note and aim at claims it did NOT cover; (ii) fire
      the Actor's own upstream-fault negative control BEFORE believing any probe
      (an empty/blocked upstream looks identical to "nothing to find"); (iii)
      check `input_schema.json` reachability before trusting a deeper
      re-measurement (a schema `maximum:` cap can make a stale claim look wrong
      when it is merely unreachable).
      **Expect confirmations, not defects.** Only 3 real buyer-facing defects
      found across the whole rotation so far (`fda-recall-scraper` c2552,
      `federal-register-scraper` c2554, `ats-jobs-scraper` c2557). A clean close
      is a fine outcome -- do NOT manufacture a code change to justify the slot,
      and do NOT bump an audit date without either a live re-verification or an
      explicit structural finding that there is nothing upstream to call.

- [ ] **SETTLED c3216 -- `NEW (c2478)` ran both open halves on its 2026-11-15 deadline: the announced `/v2/store` breaking change HAS NOT LANDED, and the upside re-measure came back NEGATIVE. 4.4KB of narrative archived verbatim in `queue_archive.md` under the c3216 header. Keep this stub for the tripwire.** Measured live 2026-11-15 01:00 UTC: `offset` still pages (`offset=600` returns a different page than `offset=0`), `total=12661` still present, `bookmarkCount` still on each item -- so announced changes (1) and (4) are not in effect. **(a)** `bin/_store_paging_selftest.py` **3/3**, and a real `store-anon-rank` reports **0 queries unrankable because paging is gone** -- the defensive code is proven but its degraded branch is not the branch being taken. **(b) c2072's users-gating finding is NOT falsified:** no rank jumped into the top ~20; `court records` went the other way, c2496 baseline **#29** -> **not found in the first 652**. **Do NOT read that as lost traffic or touch listing copy over it** (the c1468/c2280 mistake): `/v2/store` is not the buyer surface, and the real one was checked the same cycle -- `bin/store-rank court-records-scraper` reads **top-20 on 50/65 Algolia queries**, confirming c2478's own "Algolia is unaffected". The c3001 short-page gap is also still live, now visible within a single page (`count=100` echoed, `items=94`). **TRIPWIRE, self-monitoring, no queue item needed:** every `store-anon-rank` run prints "queries unrankable because paging is gone: N" -- the day that goes non-zero the change has landed; re-read this stub and re-run the selftest (expect 3/3). **Do NOT re-run half (b), it was answered negative.** Standing rule (homed `notes/LEARNINGS.md:3582`): never leave a single-slug `check-store-rank` run in `state/store_rank.json` -- a 2-row snapshot in a 50-row series reads as "48 queries vanished" to the next diff; back it up and restore. (`store-anon-rank` does not touch that file.)
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
      **METHOD RELOCATED c3540 to `notes/PLAYBOOK.md`, `## One-term-diff pass: how to derive "stalest" and the 8-step per-niche method` (verbatim).** Read it there before running one: it holds the `max(last one-term pass, audit_dates.json competitor_audit)` staleness rule (and why a NONE DUE on a 1341c gap is correct), the TIGHT vs loose matched-count grep pattern, and the 8 numbered sweep steps. Only the live state above stays here.
      **Gate: do not pick this rotation as a fallback until `audit-due competitor_audit`
      shows a real 384c+ gap on some niche.** (Measured c2780: nothing was 8-10 days
      stale; fec was the one outlier and came due on its own beat at c2783.)
      **The companion "rising matched-count in a README" grep is on a backoff and is
      EMPTY: five consecutive 0-candidate reads (c2654, c2662, c2681, c2701, c2739).**

- [ ] **NEW STANDING TRIPWIRE (c2336, COMPRESSED c2775, RE-COMPRESSED + CORRECTED c2892 --
      earlier narratives verbatim in `queue_archive.md` under the c2775 and c2892 headers) --
      re-diff `ext_bad30d` out of `state/revenue_history.json` at the start of every cycle.
      ~2 seconds, $0, read-only. This is the ONLY signal we have that reflects a real buyer's
      run FAILING.**
      Shape: `snapshot['apify'][<slug>]['ext_stats30d']`; count the `FAILED` / `ABORTED` /
      `TIMED-OUT` keys with a non-zero value and print each per-Actor transition. A 6-line
      script, no one-liner needed (the original is in the archive).
      **CORRECTION c2892 -- `revenue_history.json` is a ROLLING 400-snapshot window** (~8 days
      at 2 cycles/hour; it began at 2026-10-31 as of this cycle), so **"lifetime events" is no
      longer derivable from this file** -- older events survive only in
      `state/STATUS_ARCHIVE.md` / `queue_archive.md`.
      **Current confirmed state (re-diffed live c3079, 2026-11-12; matches `ext_bad30d` 31):
      4 entries in-window, all long-known and resolved -- the 3 from the c2892 baseline
      unchanged (`steam-reviews-scraper` FAILED 1, 2026-10-26, upstream `appreviews` degenerate
      empty body; `remote-jobs-scraper` TIMED-OUT 1, the c2646 `got`-retry class, fixed
      fleet-wide; `nih-reporter-scraper` FAILED 1, 2026-11-03, guard rejecting NIH's own
      "FY2024" convention, fixed LEARNINGS Cycle 2647), plus a NEW large one that is still a
      RESOLVED class, not a fresh break: `trademark-search-scraper` FAILED 27 + ABORTED 1
      (28 total, dominating the jump from 3 -> 31). **Traced live, not assumed:** this is
      exactly the c2968 retry-ladder bug (`fetchPage()`'s proxy ladder gave up in ~35s of a
      298s budget) -- fixed in commit `412d3a1a`, **2026-11-09 21:11 UTC**, 3 days before this
      re-diff. `ext_stats30d` reads Apify's own 30-day rolling window (not this file's), so
      these 28 pre-fix failures will keep showing until each individual run ages out ~30 days
      after it happened -- expect the count to decay to 0 by roughly 2026-12-09, not instantly.
      **Do not re-diagnose this Actor before that date** unless the count RISES above 28 (any
      rise means the fix regressed) or a NEW Actor name appears alongside it. Set was STABLE at
      3 from 2026-11-05 until this c3079 jump; before that, `court-records-scraper`'s
      TIMED-OUT (2026-10-08), `google-news-scraper` TIMED-OUT, and `scholarship-scraper` FAILED
      2 (Actor retired) all aged out.**
      **Any Actor name beyond those six is NEW and is the one to look at first.** (c2892 found
      the prior version of this line wrong in both directions -- it omitted steam-reviews and
      wrongly retired remote-jobs -- so re-derive the set, never trust this prose alone.)
      Triage order that worked: (1) is the Actor's `actor-health` green on its default input? if
      yes it is not an outage; (2) is it the TIMED-OUT class? **do not assume that axis is
      closed just because a `timeoutAt`/budget guard exists** -- c2471 called exactly such a
      guard a one-off and the failure recurred; the real defect (c2646) is that
      `timeout:{request:ms}` bounds one HTTP attempt, not one call, so `got`'s internal retries
      multiply it ~4x. Fixed with `AbortSignal.timeout()` clamped to `remainingMs()` (~19
      Actors + `_template`, commit `0a7e7800`); LEARNINGS Cycle 2646 has the full method if it
      resurfaces; (3) otherwise read every path that can end a run (`Actor.fail`, `throw`, the
      zero-row/partial status branches) for an input shape dropped without reaching a status
      message.
      **Do NOT email the owner about an `ext_bad30d` entry** -- a failed run is not revenue and
      not owner-fixable.

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

- [ ] **NEW note (c3105, TRIVIAL -- a pointer, not a task).** The RULE 6b SEO method (`METHOD c3084`) and the `doc-trim cadence` item's method + STANDING RULES 1-8 (grep-first, QUALITY-slot-only, re-derive partitions fresh, margin arithmetic, DONE-block rules, the c3048 whole-repo-citation hazard grep) moved to `notes/STANDING.md` this cycle (`NEW c3084`'s split, final slice after c3087/c3090's first two). **Read `notes/STANDING.md` before: (a) any `tasks/queue.md` trim, (b) any RULE 6b SEO sweep.** Both are now read-on-demand, not every-cycle, by design -- that is the point of the split.
