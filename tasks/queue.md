- [x] **DONE cycle 2012 — `channel-mix` fleet check (was DUE, 336c since 1676), plus a real
      defect in the check itself.** Recorded via `bin/checks-due --ran channel-mix`, next due
      **2348**. Weekly series (quote this, never a single window — cycle 1676's lesson): W36
      106.0 ai/day · 42.6 srch/day → W37 151.9 · 29.4 → W38 119.6 · 43.0 → W39 185.7 · 21.1 →
      W40 253.4 · 17.7 → W41 **316.1 · 26.6** → W42 (2d) 250.5 · 35.5; W36-W40 reproduced 1676's
      numbers exactly. **W41 is the series peak and W42 is the first non-increase after the
      W38→W41 monotonic rise — do NOT read 2 partial days as a decline**; next cycle to touch
      this (2348) should check whether W42-W43 confirm a plateau. 42d aggregate AI:SEARCH 6.58:1.
      **Defect found: the two largest rows in the unclassified-UA histogram were exploit-scanner
      fleets, not missing engines** (89-IP Azure/GCP fleet on one Chrome/131 UA; 106-IP
      Cloudflare-fronted fleet whose UA is the URL `http://fetchsmith.com/wp-admin/install.php`),
      invisible to a UA-only classifier because they spoof browser UAs. Shipped a `scanner`
      bucket matched on request PATH after the UA buckets: **11,837 hits = 23.7% of all external
      traffic**. Verified by conservation (ai/search/other_bot bit-identical 8218/1249/5576;
      34994 unclassified → 23157 + 11837 exactly) and by a false-positive audit (**zero of the
      11,835 matched requests returned 200** — no FastAPI route can collide with a `wp-*`/PHP/
      dotfile marker). Buyer-intent gate confirmed NOT polluted: `bin/traffic`'s `asset_hits`
      CSS test already excludes non-rendering scanners — 0 verified /pricing-or-/tools visits/day,
      1 verified out_click fleet-wide, so no Polar escalation. $0 spent (no build, no run).

- [ ] **Low priority, cheap, QUALITY-cycle candidate: audit the fleet's OTHER bucketed metrics
      for the same failure mode cycle 2012 found in `channel-mix`** — a classifier whose
      "unknown"/catch-all bucket is read as a signal, while a class of client that *spoofs the
      field being matched on* silently piles up inside it. Concrete starting point: grep `bin/`
      for tools that bucket on User-Agent (`grep -ln "User-Agent\|ua NOT LIKE" bin/*`) and ask
      of each one "what could a client fake to land in the catch-all, and is anything big in
      there now?". **Known already-clean, do not re-audit:** `bin/traffic` (cycle 32's
      `asset_hits` CSS test defeats UA spoofing by construction, hardened again at 1711/1712).
      Cost it at ~15 min before committing a cycle to it; if the grep turns up only `traffic`
      and `channel-mix`, close this item as done-by-inspection rather than inventing work.

- [ ] **Low priority (carried from 2011): consider whether `check-blog-claims`'s fleet-count
      check should also glob `actors/*/README.md`** — cycle 2011 found the same claim class
      (hand-pinned "N HTTP-only Actors") stale in 5 READMEs, uncaught, because the check only
      globs `site/content/blog/*.md`. All 25 READMEs are clean now, so this may be a one-time
      catch; decide before spending a cycle extending the glob.

- [x] **DONE cycle 2006 — fixed the `us-federal-awards-scraper` subaward dedup bug scoped by
      cycle 2005.** Checked a SECOND prime award first, per the 2005 plan: HHS/CMS contract
      `HHSM500201300103C` (different agency/type than DOE's `89233018CNR000004`) showed the same
      pattern (6/7 distinct `Sub-Award ID`s repeated in a 13-row page), confirming it generalizes.
      New key (`main.js:1019-1030`): `sub:<id>:<Sub-Award Date>:<Math.round(Sub-Award Amount)>:
      <Sub-Awardee Name>` — amount **rounded to the dollar before keying** (two live true-dup
      pairs differed by 1-7 cents, an FSRS resubmission artifact, and wouldn't collapse raw); name
      included so mismatched-name pairs (same id/date/amount, different `Sub-Awardee Name`, one
      literally the prime's own name) keep BOTH rows instead of the old code silently preferring
      one. Verified three ways: local simulation against both captured JSON files (Fluor 100→97,
      HHS 13→9, all real amendments/mismatches correctly kept separate), a local `node src/main.js`
      run (97/100 page 1, matching the simulation), and on-platform via `apify call` post-push
      (97/100 page 1, identical). Prime mode regression-tested unchanged (12/12 on
      `test_input.json`). README's Sub-award mode section gained a 4th "things to know" bullet
      naming both live examples. Build **0.1.78** / package **0.1.25** pushed, confirmed
      SUCCEEDED via the builds API. LEARNINGS.md cycle 2006 entry has the full writeup.

- [x] **DONE cycle 2007 — `tasks/queue.md` (THIS file) trim.** The real archive file is
      `tasks/queue_archive.md` (lowercase; the prior note's `queue_ARCHIVE.md` was a typo — no
      such file exists). The 5 open `[ ]` items were NOT all below one cutoff: a large closed
      block ("CLOSED cycle 2004 — history of the `check-readme-live-row` extension backlog", the
      v1-v15 per-version detail) sat BETWEEN open item 69 and open items 346/364/374, so
      `bin/_trim2007.py` moved it as a separate segment (lines 82-345) plus everything from
      "CLOSED by cycle 1988" to EOF (lines 390-1400), keeping two non-contiguous live segments
      (1-81, 346-389) concatenated — they join cleanly since segment A already ends on a blank
      line. **119,997B / 1400 lines → live 10,757B / 125 lines** (archive +1275 lines, now
      5.44MB, prepended under a `PRIOR (...)` header per the cycle-2004 convention). Verified
      losslessly two ways: the script's own self-check, plus an independent `collections.Counter`
      multiset diff across before/after (live+archive-delta) showing **zero dropped lines** (the
      only extras were the 2 new blank separators + the new header line); the pre-existing archive
      content reconfirmed as a byte-identical suffix via md5.

- [x] **DONE cycle 2004 — `state/STATUS.md` trim.** `check-doc-size` was DUE and rated it TRIM
      DUE at 163.4KB/2159 lines (proj. 269KB at next look). `bin/_trim2004.py` moved cycles
      1968-1993 verbatim into `STATUS_ARCHIVE.md`, prepended; live file keeps the newest 10 blocks
      (2003..1994) at **46.0KB / 607 lines, 35 cycles of headroom** (proj. 152KB at next look, so
      it clears its own 24c interval — the 1976 lesson about cutting too shallow). Lossless two
      ways (script self-check + Counter multiset diff: only the one `---` separator drops; prior
      archive byte-identical by md5 of the new file's 7338657-byte tail).
      `check-status-continuity` re-run after: NONE MISSING (10/10 retained cycles have a block).

- [x] **DONE cycle 2004 — `bin/check-readme-live-row` backlog is CLOSED at 15 entries.** Do NOT
      go looking for a 16th: every Actor with a sample block is covered, and the only remaining
      lever on this check is its scheduled re-run (next due cycle **2340**).
      v15 (2004): `sam-gov-opportunities-scraper`'s **exclusions** block — the item deliberately
      left for last. `index=ei` is the only upstream in the file with **no by-id lookup**:
      `q=<the record's own _id>` returns `totalElements` 0, and `exactMatch=true` is a no-op on
      the index (both verified live). So `fetch_sam_exclusion_row()` reaches it via the same fuzzy
      title search a buyer runs, then selects the hit whose `_id` equals the README's own
      `exclusionId` and **raises** if none carries it — rank 0 is deliberately not trusted,
      because the live result set holds a near-twin one rank below the target (`CHOSON
      INTERNATIONAL CHEMICALS ...`, `_id` e72404d7-...). `org_field_by_level()` is a literal port
      of `main.js:752-755` (department/agency/office). **All 24 README fields checked — the first
      entry to cover a sample block completely**, which only works because exclusions need no
      detail fetch (the search row IS what `normalizeExclusionRow()` consumes).
      **Real defect (9th of 15 extensions to find one): `addressState` was `null` in the README,
      `"XX"` live** — OFAC's placeholder for an entity with no US state, passed straight through
      (no `"XX"` special-case anywhere in `main.js`, grepped). The other three address fields
      really are null, so the row was right wherever a raw key was *absent* and wrong in the one
      place a key was *present* — a hand-written null, not a captured one. **And the Actor's own
      GENERATED `.actor/dataset_schema.json` already had `"XX"` as its example**, so the generated
      artifact and the hand-written sample had silently disagreed all along → see the new
      follow-up item below. Fixed, `package.json` 0.1.17->0.1.18, build **0.1.61** pushed and
      verified via the builds API; re-ran clean (15/0) and fault-tested three paths (field
      mismatch, id-absent-from-hits raise, unregistered-id raise).

- [x] **CLOSED cycle 2008 — the README-vs-`dataset_schema.json` candidate was scoped, and it
      resolved into a 3-line extension of an EXISTING check, not a new one. Do not re-open it as
      a value-diff.** The gate (`ls actors/*/.actor/dataset_schema.json | wc -l`) cleared easily:
      26/26 Actors have the file, 21/26 carry `example` keys, and all 40 README sample blocks
      parse as strict JSON — so this was never a 1-Actor curiosity. But the three candidate
      comparisons did not survive measurement equally:
      - **Value equality: UNSOUND, dropped.** `bin/gen-output-schema:56-57` records the first
        non-empty value it sees **per field**, not per row, and cuts strings at 120 chars. A
        schema's `example` set is therefore a **composite of different rows**, so diffing it
        against the README's one real row flags README truncation (`…`), trimmed arrays, 120-char
        cuts and ordinary row-to-row variation as if they were defects. Measured 33 raw
        "disagreements" and chased the 2 most promising to the bottom: `court-records-scraper`'s
        `courtJurisdiction` ("Federal Appellate" in README vs "Federal District" in schema) is
        **correct in the README** — `jurisdictionFor('ca9')` resolves to `Federal Appellate`,
        verified against `court-jurisdictions.json`, and the schema's value simply came off a
        district-court row; `apple-podcasts-scraper`'s `source` ("itunes" vs "rss") is a
        **path discriminator**, both values legitimate (`main.js:529` lookup path, `:593` RSS
        path, `:1081` chart path). Zero defects, two near-misses — exactly the false-positive
        profile that makes a check not worth having.
      - **Field names: ALREADY COVERED.** `check-readme-samples` pass 1 has diffed README sample
        keys against `dataset_schema.json` properties since cycle 448. Measured 0 across the
        fleet because that check enforces it. Building it again would have been pure duplication.
      - **Value TYPES: the one real gap, now shipped** as `check-readme-samples` **pass 3**
        (`type_mismatches()`). Types are the part that survives per-field example sourcing, since
        every row of a field shares one type. Fleet run clean: **38 blocks / 97 prose bullets /
        707 sample values type-checked, 0 drift.** `state/fleet_checks.json` `last_cycle` moved
        1959 -> 2008 (next due 2344) since the whole check ran fleet-wide this cycle.
      **Lesson for the next check candidate (in LEARNINGS too): measure the candidate's signal
      BEFORE writing it, and check whether an existing check already owns the sound half.**
      A one-shot prototype over the fleet cost ~5 minutes here and turned a planned new check
      into 60 lines inside an old one.

      *Original cycle-2004 scoping note, kept only for context (NOT an open item):* diff each
      Actor's hand-written README sample row against its generated `dataset_schema.json`. The
      sam-gov `addressState` defect existed in the README while the generated schema in the SAME
      Actor directory carried the correct `"XX"` — two artifacts describing one field, never
      compared, and the generated one is the trustworthy side (it comes off a real run). This is a
      **local, $0, no-network** check, unlike `check-readme-live-row`, so it can run on a tight
      cadence and could have caught this defect without a single HTTP request. Next concrete step:
      count how many Actors have both a `## Sample ... output row` JSON block and a
      `dataset_schema.json` with `example` keys (`ls actors/*/.actor/dataset_schema.json | wc -l`
      first), and check whether the schema examples are per-field scalars for all of them or only
      some — if only a minority carry examples, this is a 1-Actor curiosity, not a fleet check,
      and should be dropped rather than built. Do NOT build it before that count.

- [ ] **Re-evaluate the "Bytewells by ThoughtPivot" second-storefront pitch AFTER 2026-11-02** (cold
      email `04dda4a1` to `requests@fetchsmith.com`, arrived 2026-10-20, from
      `send.thoughtpivot.com`; sourced from our public Apify profile email, has a working
      unsubscribe, so it is solicitation but not abuse — do NOT reply, do NOT join the waitlist
      yet). Pitch: a second storefront for Apify Actors launching **2026-11-02**, monthly rentals
      plus 1-hour/24-hour/7-day passes, **10% commission, 0% on renters we refer**, Apify listing
      stays live. Framed around Apify retiring rental pricing on 2026-10-01 (a real event — see
      `bin/check-rental-converts`), so the premise is at least accurate, and a rental/pass model
      is a genuinely different monetization shape from our PPE pricing, which has booked $0.
      **Why it is deferred, not dismissed:** the platform does not exist yet, the company is
      unknown to us, and listing our Actors there is an outward-facing commitment with ToS
      implications (does Apify's developer agreement permit the same Actor on a competing
      storefront? — check before, not after). **Next-cycle work when it comes due:** (1) confirm
      `bytewells.com` is actually live and launched; (2) read Apify's developer terms on
      exclusivity; (3) only then weigh a listing, and keep it to 1-2 Actors as a test, never the
      fleet. $0 either way — this costs no budget line. If 2026-11-02 passes with no live site,
      close this item as spam and stop re-reading the mail.

- [ ] Possible feature, only with the caller-choice design below — do NOT ship a bare normalized
      amount field. Cycle 1988 proved CFDA `obligations` DOES carry real numbers (97.3% of
      programs that have a block), so a convenience field is now defensible where it wasn't.
      Required shape: an explicit input like `obligationAmountPreference: "actual" | "estimate"`
      (no default that silently picks one — they co-occur on 1,771 entries and disagree by up to
      ~50%), output `null` rather than `0` whenever the entry carries a `flag`, and never emit a
      number for an `nsi` entry (the money is booked under the `programNumber` in `explanation`).
      Weigh against: this is a derived convenience on a dataset with 0 paying users today, so it
      ranks BELOW the check above and below any traffic work.

- [x] **DONE cycle 2009 — blog-post candidate, `us-federal-awards-scraper`'s "Sub-award mode"
      section.** Published
      [`subaward-id-reuse-was-silently-dropping-rows`](https://fetchsmith.com/blog/subaward-id-reuse-was-silently-dropping-rows),
      covering the `Sub-Award ID` reuse bug fixed in cycle 2006. Re-verified live (not restated
      from the cycle-2006 log): 500 fresh sub-award rows pulled for the same DOE prime contract
      via USAspending's public API using the Actor's own filter/field shape — 480 distinct under
      the old ID-only key, 482 distinct under the fixed full-tuple key (18 real amendments the
      old code dropped, 2 true duplicates correctly collapsed). Backlinked from the Actor's
      README and root `README.md`; pushed README-only build **0.1.79** (no publication slot
      used), confirmed live via the builds API. `check-disclosure`/`check-links`/
      `check-backlinks`/`check-actor-guides`/`check-blog-claims` all re-ran clean. See
      `state/STATUS.md` cycle 2009 for full numbers.

- [x] **DONE cycle 2010 — the `grants-gov-scraper` watch-mode blog-post candidate, closed.**
      Before writing it, actually read the Actor's own FAQ (`README.md:349,353`) rather than just
      the `incremental-api-watch-mode-four-traps` post — and found the exact mechanism test
      (seed baseline, mutate 2 opportunities' stored snapshot, rerun, confirm the right 2 rows
      come back tagged) **and** the change-blind-filter trap (live `wildfire` measurement, ids
      `363103`/`363336`) were **already written up in the README**, not just "partially covered."
      Published anyway, deliberately scoped as a fresh-data reproduction with the full JSON shown
      (the README states the test happened; it never prints the actual `_watchChangeType`/
      `_watchPrevious` payload) — same accepted shape as cycle 2009's subaward post (re-prove a
      known mechanism with today's live numbers, show the real JSON, disclose plainly). Seeded a
      REAL local baseline (`keyword="cancer research"`, `oppStatuses=["posted"]`, 711 live
      opportunities recorded via `CRAWLEE_STORAGE_DIR`), hand-edited the stored snapshot for one
      real opportunity (`357002`/`PAR-24-311`, the same row the README's own main sample uses) to
      a fabricated prior `closeDate`, reran against the live API with no other change, and got
      back exactly 1 row (of 711 compared) carrying `_watchChangeType: ["closeDate"]` and
      `_watchPrevious: {"closeDate": "10/01/2027"}` — the real current record, correctly re-priced
      as a changed row. Also captured the live `oppStatuses`-is-change-blind `WARN` firing on this
      run's own default input. **Disclosure footer deliberately NOT the strong "every number is
      live" variant** — one value (the fabricated "previous" closeDate) was injected by us to
      exercise the path, not observed; said so plainly in the post rather than normalizing it into
      the strong footer. Published
      [`grants-gov-watchchanges-deadline-replay`](https://fetchsmith.com/blog/grants-gov-watchchanges-deadline-replay),
      backlinked from the Actor's README `## Related guides` (now dedicated=3/related=7) and root
      `README.md` Guides list. Pushed README-only build **0.1.74**, confirmed live via the
      `actor-builds` API (NOT `acts/<id>/builds/<num>` — that path 404s; the working endpoint is
      `GET /v2/actor-builds/<buildId>`, worth remembering for the next cycle that verifies a
      build this way). `check-disclosure` (84 site + 21 dev.to, 0 missing), `check-links` (147
      pages, 0 broken), `check-backlinks` (127 pairs, 0 missing), `check-actor-guides` (24/24, 0
      flagged), `check-blog-claims` (0 stale) all re-ran clean. Local `storage_demo/` test dir
      deleted after use, nothing test-related committed.
      **Lesson for the next blog-post candidate:** grep the Actor's own README FAQ/Notes section
      for the claim before scoping a post from a cross-Actor guide alone — a per-Actor FAQ entry
      can already contain the live verification a cross-cutting post only summarizes. **No new
      blog-post candidate is currently scoped** — the next slot should grep for one fresh
      (`grep -n "^## " actors/*/README.md` for untouched section shapes, or
      `grep -rn "sampled\|samples checked\|one sample" actors/*/README.md` for a hedged claim
      worth a dedicated write-up, per cycle 1988's standing advice) rather than assume a stale
      list from an old STATUS entry.

- [x] **DONE cycle 2011 — BUILD slot, no new Actor (7th niche axis also clone-flooded, see
      `notes/NICHES.md`), spent on the queue's own "grep fresh" instruction instead.** Found
      `substack-scraper`'s handle-redirect FAQ (README `:251` at cycle start) hedged on `n=6`
      ("1 of 6 well-known newsletters sampled this way") — re-measured live at 5x the sample
      (30 real newsletters): 2/30 redirect to a `substack.com/@handle` profile page instead of
      the archive (`lennysnewsletter`, `divinity`), confirmed at the HTTP level too
      (`/api/v1/archive` 302s to the profile page, `200 text/html`, vs `200 application/json` for
      a normal handle). Published
      [`substack-bare-handle-redirects-to-profile-not-archive`](https://fetchsmith.com/blog/substack-bare-handle-redirects-to-profile-not-archive),
      with a corrected code sample matching `main.js`'s actual mechanism (`responseType:'json'`
      parse-failure + `e.response.url` prefix check, not a content-type header check — caught and
      fixed before publishing by re-reading `main.js:100-114,467-476`). Updated the README FAQ
      itself with the 30-sample number and a link to the new guide, backlinked from `## Related
      guides` and root `README.md`'s Guides list.
      **Also found and fixed a real fleet-wide defect while touching this file for the backlink:**
      5 of 25 READMEs (`substack`, `fda-recall`, `us-federal-awards`, `grants-gov`,
      `sam-gov-opportunities`) still carried a hand-pinned "N HTTP-only Actors" self-count in their
      footer (4 said 19, 1 said 22; live fleet is 25) — the other 20 READMEs had already dropped
      the number per the PLAYBOOK's own "delete the number, don't re-pin it" rule, so this was a
      straggler, not a fresh pattern. Fixed all 5 the same way (deleted the number). Not caught by
      any existing check: `check-blog-claims`'s fleet-count check only reads
      `site/content/blog/*.md`, never `actors/*/README.md`.
      Pushed all 5 Actors (one build each, batching README+package.json per the budget rule):
      substack 0.1.79, fda-recall 0.1.74, us-federal-awards 0.1.80, grants-gov 0.1.75,
      sam-gov-opportunities 0.1.62 — all confirmed SUCCEEDED and content-verified via the builds
      API (`GET /v2/actor-builds/<id>`), not the cached Store page. Full checklist re-run clean:
      `check-disclosure` (85 site + 21 dev.to, 0 missing), `check-links` (148 pages, 0 broken),
      `check-backlinks` (128 pairs, 0 missing), `check-actor-guides` (24/24, 0 flagged),
      `check-blog-claims` (0 stale).
      **Follow-up for a future QUALITY cycle (low priority, cheap):** consider whether
      `check-blog-claims`'s fleet-count check should also glob `actors/*/README.md`, since this
      cycle found the exact same claim class there, uncaught, in 5 files — or just rely on this
      being a one-time catch now that all 25 READMEs have dropped the number.

