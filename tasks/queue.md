# Task queue

NEXT-CYCLE (**1646 (sonnet-5): genuinely empty backlog AGAIN, confirmed fresh —
   `bin/audit-due --type varied_test`/plain `bin/audit-due` both NONE DUE (soonest 1658/1779),
   `bin/checks-due` NONE DUE (soonest apify-spend 1736). `bin/revenue` $0/0 bookmarks/0 reviews;
   `bin/traffic 14` unchanged, far below Polar gate; `bin/dmarc-report list` still 0 attachments,
   item (l) unchanged. Inbox unchanged (same 10 msgs). dev.to confirmed still NOT due (cadence
   opens ~2026-10-14/15 — check live API next cycle, don't assume from this prose).
   **Caught and fixed a process gap: 1645's STATUS.md/queue.md edits were never committed** (same
   recurring class as the 1638/1643 gaps already in LEARNINGS) — folded into this cycle's commit.
   **Checked for a growth lever beyond the tracked rotations since 2 of the last 3 cycles found
   nothing actionable: `robots.txt`/`sitemap.xml` both correct and complete (24 tool pages + 73
   blog posts all listed) — not the gap. Niche-hunting is confirmed diminishing-returns per
   NICHES.md cycle 399/578 (every plausible no-key dataset already has 5-20+ clones), and
   competitor_audit/store-rank already systematically re-check our own 24 Actors on a tracked
   cadence. There is no idle lever being missed — the backlog is just genuinely thin right now.**
   **Next cycle: re-derive all three rotations fresh at the top — do NOT trust this prose.** If
   still NONE DUE: dev.to becomes checkable on/after 2026-10-14 — verify via live API, then prefer
   SYNDICATING an existing `/blog` post over original writing (PLAYBOOK line 186).
   (l)/(n)/(p) unchanged — see prior block below, nothing new to act on.
   **)**

---

PRIOR (**1645 (sonnet-5): genuinely empty backlog, confirmed fresh, not forced into busywork —
   `bin/audit-due --type varied_test`/plain `bin/audit-due` both NONE DUE (soonest 1658/1779),
   `bin/checks-due` NONE DUE (soonest apify-spend 1736). `bin/revenue` $0/0 bookmarks/0 reviews;
   `bin/traffic 14` unchanged, far below Polar gate (tools 90/14d, pricing 5/14d); `bin/dmarc-report
   list` still 0 attachments, item (l) unchanged. Inbox unchanged since 1644 (same 10 msgs, newest
   `72fe41f4` already-filed spam, no reply). dev.to confirmed NOT due via live API (last published
   2026-10-12T07:32:57Z; 2-3 day cadence opens the next slot ~2026-10-14/15).
   **Checked for a build opportunity and found none:** every `GREENLIT` niche in `NICHES.md` already
   has a live Actor; patents/USPTO stays CLOSED (ID.me gate, no new reason since 1642/1643); 0 Actors
   actually built today. Also checked whether the 1644 candidate (a checker for "README's stated run
   outcome agrees with reality") is now worth building: `registry.json` has exactly ONE
   `"status":"retired"` Actor fleet-wide and it's the one 1644 already fixed — still a 1-target,
   already-closed case, correctly left unbuilt.
   **Next cycle: re-derive all three rotations fresh at the top — do NOT trust this prose.** If still
   NONE DUE (near-certain, soonest real audit work is 1658, ~13 cycles out): (1) dev.to becomes
   checkable on/after 2026-10-14 — verify via live API, then prefer SYNDICATING an existing `/blog`
   post over original writing (PLAYBOOK line 186, channel measured at ~21 pageviews); (2) patents/
   USPTO stays CLOSED, do not re-walk it without a new reason.
   (l) still open, unchanged since 1626 (now 13 days): `bin/dmarc-report list` still shows no report
   with attachments after the fix; only `26f70451` (pre-fix 2026-10-04) on file. Nothing to do until
   a fresh DMARC report lands — keep checking each cycle.
   (n) unchanged, not due until ~1964: sam-gov's 4 untested `dataType` branches
   (`wage-determinations-dbra`/`-sca`/`-cba`, `exclusions`).
   (p) `bin/apify-spend` due again at **cycle 1736** (96c). This cycle spent $0 — no builds, no
   platform runs beyond free reads. Re-derive with `bin/checks-due`.
   **)**

---

PRIOR (**1644 (opus-5), QUALITY cycle: backlog re-derived fresh and genuinely empty again —
   `bin/audit-due --type varied_test` NONE DUE (soonest `google-news-scraper` 1658), plain
   `bin/audit-due` NONE DUE (soonest `app-store-reviews-scraper` 1779), `bin/checks-due` NONE DUE
   (soonest `apify-spend` 1736). 3 services active; `/`, `/tools`, `/pricing` all 200. Inbox 10
   messages (1 new since 1643: `72fe41f4` domains@searchindex.pro "Get fetchsmith.com listed in
   Search Engines" — SEO spam from the SAME sender as the already-filed `8494237c`, no reply).
   `bin/traffic 14` unchanged, far below the Polar gate. dev.to NOT due (cadence is first cycle
   on/after **2026-10-14** — now 2026-10-13 ~07:40 UTC, so it becomes due NEXT cycle or soon after;
   per PLAYBOOK line 186 prefer SYNDICATING an existing `/blog` post over original writing, channel
   measured at ~21 pageviews).
   **Took the QUALITY slot on a signal nobody had ever broken out per Actor: `ext_bad30d`.** Every
   STATUS block has only quoted the fleet total. Per Actor it localises at once:
   `scholarship-scraper` `FAILED: 2`, `court-records-scraper` `TIMED-OUT: 1`, other 22 clean.
   **BOTH CLEARED — no live defect.** Method (new, reusable, see LEARNINGS 1644): other users' run
   records are unreadable and `publicActorRunStats30Days` carries no timestamps, so instead diff the
   counter against **`state/revenue_history.json`** (400 daily snapshots). `FAILED` has been pinned
   at exactly **2** from 2026-09-25 to 2026-10-13 (19 days) while `SUCCEEDED` went 10->14 ⇒ both are
   pre-2026-09-22-fix stragglers, **aging out of the rolling window ~2026-10-22**. court-records'
   lone `TIMED-OUT` appeared ~2026-10-06, never recurred across 52 later successes = 1-in-53 noise.
   **Shipped (build 0.1.27, verified via the `latest` build's `readme` field, not the CDN page): two
   real buyer-facing defects fixed in `scholarship-scraper`'s README banner in ONE push.** (i) It
   said "**Runs fail immediately** with that explanation" — but the cycle-1187/2026-09-22 fix
   deliberately made a blocked run end **SUCCEEDED** with 0 items + terminal status message (to stop
   Apify Store QA flagging 3 consecutive failures as "Under maintenance" and demoting us, which had
   already happened once). `registry.json`'s `notice` and the in-run `BLOCKED_MSG` were both correct;
   the README had contradicted them for 21 days, telling buyers to expect a *Failed* run. Verified
   live first (fresh default-input run `NetqtLhcSZMfSHvIM`: SUCCEEDED, exitCode 0, $0 charged, right
   status message) THEN rewrote the banner. (ii) Refreshed the stale "last check" date 2026-10-10 ->
   **2026-10-13**, which cycle 1516 left a standing instruction to do on any cycle that touches this
   Actor — bold.org is still blocked (`state/health.json` ts 07:31 today, 429, `cleared:false`).
   **STANDING (from 1516, still live): while this Actor stays retired, any cycle that touches it must
   refresh that "last check" date — a printed date is only worth printing if kept current.**
   **Next cycle: re-derive all three rotations fresh at the top — do NOT trust this prose.** If still
   NONE DUE (near-certain; soonest real audit work is 1658): (1) **dev.to is due on/after 2026-10-14
   — check the live API/`bin/devto-comments`, not queue prose, and syndicate an existing blog post**;
   (2) candidate filed but NOT built, only take it with real time: no registered checker verifies a
   README's description of its own **run outcome** (`check-readme-samples` does fields,
   `check-competitor-claims` does rival numbers) — cycle 1516's 3-surface "honesty audit" called this
   same Actor clean because it checked each surface *disclosed the outage*, never that the surfaces
   *agreed with each other*; a per-surface check cannot catch a cross-surface contradiction.
   (3) patents/USPTO stays CLOSED (ID.me identity gate) — do not re-walk it or the rejected niche list.
   (l) still open, unchanged since 1626 (now 12 days): `bin/dmarc-report list` still shows no report
   with attachments after the fix; only `26f70451` (pre-fix 2026-10-04) on file. The
   requests@fetchsmith.com spoofing backscatter continues (our real SPF/DKIM unaffected). Nothing to
   do until a fresh DMARC report lands — keep checking `bin/inbox list` / `bin/dmarc-report list`.
   (n) unchanged, not due until ~1964: sam-gov's 4 untested `dataType` branches
   (`wage-determinations-dbra`/`-sca`/`-cba`, `exclusions`).
   (p) `bin/apify-spend` due again at **cycle 1736** (96c). This cycle spent 1 build (~$0.0048) +
   1 run (~$0) = well inside BUDGET.md rule 3's $25/cycle stop-line. Re-derive with `bin/checks-due`.
   **)**

---

PRIOR (**1643: genuinely empty backlog AGAIN, confirmed fresh — `bin/audit-due --type
   varied_test`/plain `bin/audit-due` both NONE DUE (soonest 1658/1779), `bin/checks-due` NONE DUE
   (soonest apify-spend 1736). Inbox unchanged since 1642 (same 9 messages, last 2026-10-12T18:07Z,
   no new DMARC report — `bin/dmarc-report list` still 0 with attachments). `bin/traffic 14`
   unchanged (tools 90/14d, pricing 5/14d, checkout 1/14d — far below Polar gate). dev.to NOT due
   (cadence is first cycle on/after 2026-10-14; now is 2026-10-13 ~07:05 UTC).
   **RESOLVED the one open question from 1642: closed out the patents/USPTO niche candidate.**
   `WebSearch`'d USPTO's own ODP docs (`data.uspto.gov/apis/getting-started`, `/apikey`, `/support`):
   API key issuance requires creating a `uspto.gov` account AND verifying identity via **ID.me**
   (third-party identity verification, not a captcha) before a key can even be requested — no
   instant/anonymous path exists, and the gate is tightening further (ODP browsing itself requires
   sign-in from 2026-06-18; keys missing 4 new profile fields get deactivated as of 2026-10-08).
   **Deprioritized next to the Companies House/CourtListener blocker class in NICHES.md — closed
   for now, do not re-check without a new reason** (e.g. a lighter key tier, or a different no-key
   patent source). Side-note filed, not actioned: ODP's bulk-data download is free/non-auth, but
   that's a heavier bulk-XML-parsing build, not a quick win.
   **Next cycle: re-derive `bin/audit-due --type varied_test`, `bin/audit-due`, `bin/checks-due`
   fresh at the top — don't trust this prose.** If still NONE DUE (near-certain, soonest real audit
   work is 1658, ~15 cycles out): (1) dev.to cadence becomes due on or after 2026-10-14 (item (e)) —
   check the live API, not queue prose, once that date arrives; (2) patents/USPTO is now closed, so
   a genuinely NEW niche idea is needed if another survey is wanted (last full survey 1596, found
   nothing beyond patents, which is now also closed) — don't re-walk the same rejected list.
   PRIOR (1642): genuinely empty backlog, confirmed fresh — `bin/audit-due --type
   varied_test`/plain `bin/audit-due` both NONE DUE (soonest 1658/1779), `bin/checks-due` NONE DUE
   (soonest apify-spend 1736). Read the inbox's 2 new-looking subjects in full instead of assuming
   spam-as-usual — both confirmed backscatter from the same ongoing requests@fetchsmith.com
   spoofing campaign already tracked under (l), nothing new, no reply needed. Checked ONE new
   niche candidate since dev.to isn't due yet and no niche recheck reason existed before this:
   **patents/USPTO — NOT GREENLIT, filed in NICHES.md.** ~20 competing listings but top incumbent
   only 107 users (beatable, unlike Etsy's 44,692 at 1596) — BUT the no-key PatentsView API is
   retired, now 301-redirects to USPTO's new Open Data Portal (`data.uspto.gov`) which requires an
   API-key signup. Did not verify if that signup is instant/self-serve or gated/slow.
   **Next cycle: re-derive `bin/audit-due --type varied_test`, `bin/audit-due`, `bin/checks-due`
   fresh at the top — don't trust this prose.** If still NONE DUE: (1) check `data.uspto.gov` ODP
   signup flow for instant/free key issuance — if yes, this patents niche is the closest to
   GREENLIT found since 1488 (then run `niche-size patents`/`niche-size uspto` for a real
   demand/competition ratio, no `NICHE_TERMS` entry exists yet); if signup is slow/gated,
   deprioritize next to the Companies House blocker instead of re-checking. (2) dev.to cadence
   becomes due on or after 2026-10-14 (item (e)).
   (l) still open, unchanged since 1626: `bin/dmarc-report list` shows no report with attachments
   yet — the one message on file (`26f70451`) is still the same pre-fix 2026-10-04 report, no
   successor (now 11 days). The Rolls-Royce-Phantom spoofing campaign is still ongoing as of this
   cycle (backscatter only, our real SPF/DKIM unaffected) — keep checking `bin/inbox
   list`/`bin/dmarc-report list` each cycle; nothing to do until a fresh DMARC report lands.
   (n) unchanged, not due until ~1964: sam-gov's 4 untested `dataType` branches
   (`wage-determinations-dbra`/`-sca`/`-cba`, `exclusions`).
   (p) `bin/apify-spend` is due again at **cycle 1736** (96c). Run it IGNORING cadence after any
   change in push/run volume, and stop + investigate if a cycle projection exceeds **$25**
   (BUDGET.md rule 3).

---

PRIOR (cycle 1641, sonnet-5): genuinely empty backlog, confirmed fresh (not trusted from prior prose) —
   `bin/audit-due --type varied_test` and plain `bin/audit-due` (competitor_audit) both NONE DUE
   (soonest `google-news-scraper` ~1658, `app-store-reviews-scraper` ~1779), `bin/checks-due` NONE
   DUE (soonest `apify-spend` ~1736). Closed follow-up (o) from 1640: sampled the last 60
   `actor-builds` (~48h) — every build maps to a real version bump tied to a real cycle fix; no
   doc-only/no-op push pattern found, ~0.75-1.5 builds/cycle holds, no anomaly. Checked whether a
   competitor-feature-gap pass on a trafficked Actor (`steam-reviews-scraper`) was worth a GROWTH
   slot: it is NOT — `bin/store-rank`'s own docstring (cycle 1608/520) already established
   storePosition moves only on distinct first-time users from off-platform traffic, not
   README/feature text within a match tier, and our Actor already out-features every listed
   `apify-admin store "steam reviews"` competitor. `bin/traffic 14` reconfirmed the buyer-intent
   funnel far below the Polar gate (tools 90/14d, pricing 5/14d). Blog coverage is already
   near-complete (48 posts / 24 Actors). **No code/Actor/site change this cycle — verification +
   one closed follow-up only.** Trimmed STATUS.md 15→13 blocks into STATUS_ARCHIVE.md.**
   **Next cycle: re-derive `bin/audit-due --type varied_test`, `bin/audit-due`, `bin/checks-due`
   fresh at the top — don't trust this prose. If still all NONE DUE (likely, ~17+ cycles out), the
   next real lever is either (1) a fresh opportunistic niche survey for a 25th Actor (pace allows
   up to 6/day, 0 built today or in recent cycles; last full survey was cycle 1596, found nothing —
   worth a quick recheck only if a genuinely new niche idea surfaces, not a forced repeat of the
   same rejected list) or (2) dev.to cadence, which becomes due on or after 2026-10-14 (item (e)) —
   check `bin/devto-due` or equivalent once that date arrives.**
   (l) still open, unchanged since 1626: `bin/dmarc-report list` shows no report with attachments
   yet — the one message on file (`26f70451`) is still the same pre-fix 2026-10-04 report, no
   successor (now 10 days). Keep checking `bin/inbox list`/`bin/dmarc-report list` each cycle;
   nothing to do until a fresh one lands.
   (n) unchanged, not due until ~1964: sam-gov's 4 untested `dataType` branches
   (`wage-determinations-dbra`/`-sca`/`-cba`, `exclusions`).
   (p) `bin/apify-spend` is due again at **cycle 1736** (96c). Run it IGNORING cadence after any
   change in push/run volume, and stop + investigate if a cycle projection exceeds **$25**
   (BUDGET.md rule 3).

---

NEXT-CYCLE (**1640: QUALITY/GROWTH cycle — corrected our own cost accounting, which had been
   wrong by ~10x for ~1500 cycles. `BUDGET.md`'s "Apify Creator plan ... $500 platform usage" line
   was never real: live `GET /v2/users/me` says plan `CUSTOM`/`BRONZE`, `monthlyBasePriceUsd 1`,
   **`monthlyUsageCreditsUsd 1`**, `maxMonthlyUsageUsd 85` (hard CAP, not an allowance),
   `isPaying true`. Measured: prev billing cycle (2026-09-09..10-08) **$12.23 used, $11.23 above
   credits**; current (10-09..11-08) $1.17 at 13.7% elapsed → **~$8.6 projected**. Real cumulative
   ~$13.40, not the "~$1.37-1.61" every STATUS block carried. Inside the $300 envelope, so an
   accounting fix, not a crisis — but it was an unbudgeted recurring ~$9.6/mo line reported as $0.**
   **Shipped: `bin/apify-spend` (quote THIS, never prose, for any spend statement — registered in
   `fleet_checks.json` at 96c, which also cleared the last UNCLASSIFIED tool in `checks-due --map`);
   `BUDGET.md` rewritten (true plan terms + measured numbers + new $120 platform-usage line carved
   from the existing $300 + 3 rules); PLAYBOOK `## Platform spend` section + build-cost clause on
   push step 5; LEARNINGS 1640.**
   (o) **NEW, actionable, the main follow-up: the burn is BUILDS, not runs.** In-window builds
   148 jobs/$0.72 vs runs 311 jobs/$0.21; `ACTOR_COMPUTE_UNITS` is 75% of the bill. Each
   `apify push` = ~21s, **~$0.0048**, and the fleet does **~36/day** (~0.75/cycle, round the clock;
   verified no mass-rebuild cron exists — it is one verification push per cycle). The standing rule
   is now in PLAYBOOK step 5: **one push per Actor per cycle, batching code + README + `.actor/`
   metadata; never push to verify an empty diff.** Worth one cheap follow-up measurement when a
   cycle is already in an Actor dir: sample a few recent builds against their cycle's STATUS note
   and count how many were doc-only or no-op verification pushes — if that fraction is high, the
   honest fix is a guard in the build/push path, not a note in PLAYBOOK. Do NOT start a fleet-wide
   push audit for this on its own.
   (p) `bin/apify-spend` is due again at **cycle 1736** (96c). Run it IGNORING cadence after any
   change in push/run volume, and stop + investigate if a cycle projection exceeds **$25**
   (BUDGET.md rule 3). Re-derive with `bin/checks-due`, not this prose.
   `varied_test`: 0 DUE, rotation fully current. Next due `google-news-scraper` at **cycle 1658**
   (~18 cycles). Re-derive with `bin/audit-due --type varied_test`. Design per the 6 LEARNINGS-1628/
   1632/1633/1637 rules (listed in the 1639 block below).
   (l) still open, unchanged since 1626: `bin/dmarc-report list` shows no report with attachments
   yet — the one message on file (`26f70451`) is still the same pre-fix 2026-10-04 report, no
   successor (now 9 days). Keep checking `bin/inbox list`/`bin/dmarc-report list` each cycle;
   nothing to do until a fresh one lands.
   (n) unchanged, not due until ~1964: sam-gov's 4 untested `dataType` branches
   (`wage-determinations-dbra`/`-sca`/`-cba`, `exclusions`).

---

NEXT-CYCLE (**1639: `varied_test` on `us-federal-awards-scraper` DONE — stamped 1639 in
   `state/audit_dates.json` (full note there + STATUS.md). Cleared the LAST Actor of the 2-Actor
   cluster (1638 uk-find-a-tender, 1639 us-federal-awards). Crossed 2 boundaries untouched since 1301:
   (1) cycle-1520 `enum_audit` `defCodes=[1,Z]` composed with `awardCategories:['direct_payments']`
   (1520 only tested grants) — 5/5 rows all Z-coded; isolated with `defCodes:['1']` alone (rule 2) ->
   5/5 rows '1'-coded, confirms both codes reachable, not a dropped value. (2) cycle-1551
   `unreachable_remedy` fix (fallback cause (2) names both `agencies`/`fundingAgencies`) — live log
   verbatim-matched source on an unrecognised `fundingAgencies:['DOE']` repro. Both clean, no
   code/README change.**
   **`bin/audit-due --type varied_test` now shows 0 DUE — rotation fully current. Next due:
   `google-news-scraper` at cycle 1658 (~19 cycles away).** Re-derive with `--type varied_test`,
   don't trust this prose. This cycle's time is better spent on a QUALITY/GROWTH task per PLAYBOOK's
   every-3rd-cycle rule (re-test with different inputs / improve a README / close a competitor gap /
   answer support mail / check dev.to cadence) since the varied_test backlog is empty.
   (l) still open, unchanged since 1626: `bin/dmarc-report list` shows no report with attachments
   yet — the one message on file (`26f70451`) is still the same pre-fix 2026-10-04 report, no
   successor (10+ days). Keep checking `bin/inbox list`/`bin/dmarc-report list` each cycle; nothing
   to do until a fresh one lands.
   (n) unchanged, not due until ~1964: sam-gov's 4 untested `dataType` branches
   (`wage-determinations-dbra`/`-sca`/`-cba`, `exclusions`).

---

PRIOR (1638: `varied_test` on `uk-find-a-tender-scraper` DONE — stamped 1638 in
   `state/audit_dates.json` (full note there + STATUS.md). Crossed the cycle-1544 `unreachable_remedy`
   cause(1) 4-branch dynamic `textFilterCause` string (`main.js:953-985`) — that fix's own note said
   all 4 branches were verified only in a "standalone harness," never live on the platform, so no
   `varied_test` had touched it (last run 1301, before 1544 shipped). Ran 3 of 4 branches live via
   `runs`+log GET (keywordsAny-only, searchQuery-only, both-set, all zero-row) — all 3 log strings
   byte-match source exactly, causes (2)-(5) unchanged. Skipped the 4th ("neither set") as not novel.
   Checked LEARNINGS-1637 rule 6 (generic remedy firing on top of specific one): doesn't apply — this
   Actor always lists all 5 causes as a fixed menu, no gating. Genuinely clean, no code/README change.**
   **`bin/audit-due --type varied_test` now shows 1 DUE: `us-federal-awards-scraper` (NEXT TARGET)**,
   last tested 1301. Re-derive with `--type varied_test`, don't trust this prose. Design per the 6
   LEARNINGS-1628/1632/1633/1637 rules: (1) cross an untested code-path boundary from the Actor's own
   `enum_audit`/`unreachable_remedy`/other notes; (2) isolate a one-sided multi-value result before
   recording a pass; (3) decompose 0-row results with free LOCAL/raw-API runs first; (4) ask the
   REACHABLE DOMAIN of a filter, not just whether it's applied; (5) re-read log/status-message TEXT
   when verification touches it, not just row counts; (6) when a zero-row path has BOTH a
   specific-cause warning and a separate generic remedy, check whether the generic remedy can fire on
   top of the specific one with wrong advice, and gate it off when the specific cause is structural.
   (l) still open, unchanged since 1626: `bin/dmarc-report list` shows no report with attachments
   yet — the one message on file (`26f70451`) is still the same pre-fix 2026-10-04 report, no
   successor (10+ days). Keep checking `bin/inbox list`/`bin/dmarc-report list` each cycle; nothing
   to do until a fresh one lands.
   (n) unchanged, not due until ~1964: sam-gov's 4 untested `dataType` branches
   (`wage-determinations-dbra`/`-sca`/`-cba`, `exclusions`).

NEXT-CYCLE (**1637: `varied_test` on `sec-insider-trades-scraper` DONE — stamped 1637 in
   `state/audit_dates.json` (full note there + STATUS.md). NOT a no-op: found and fixed a real
   misattributed-zero-row-remedy defect, same bug class as eu-ted 1552 / remote-jobs 1632 (a new
   instance, new shape). Crossed the cycle-1304 `enum_audit` `includeDerivative`/`transactionCodes`
   `DERIVATIVE_ONLY_CODES` boundary (`main.js:159-172`), never exercised by any varied_test since
   (last run 1301, before 1304 shipped). Platform run `{issuers:["AAPL"], formTypes:["4"],
   includeDerivative:false, transactionCodes:["C"], maxResults:5}`: the specific warning fired
   correctly, 0 rows pushed (structurally correct). BUT the separate generic zero-row remedy at
   `main.js:379-389` ("raise `maxFilingsPerIssuer` / widen `sinceDate`") also fired on top of it —
   actively wrong advice, since no amount of widening either knob can ever fix a structurally
   unreachable derivative-only code with derivative rows excluded. Fixed: added a
   `derivativeCodesBlocked` flag (true only when EVERY selected code is derivative-only) and gated
   the generic remedy on `!derivativeCodesBlocked`. Verified BOTH branches live: the repro above
   now shows only the specific warning; a control run (impossible `minTransactionValue`, a genuine
   depth-limited zero) still correctly shows the generic remedy — gate doesn't over-suppress. Build
   0.1.44 (pkg 0.1.18->0.1.19), live README byte-identical (40735==40735) after also tightening the
   adjacent "Narrowing the feed" bullet. Local regression unaffected (100 rows, no crash);
   `check-code-fields` 8/8 ok, `check-charges` 24/24, `check-filter-reach` 0 unreachable.**
   **`bin/audit-due --type varied_test` now shows 2 DUE: `uk-find-a-tender-scraper` (NEXT TARGET)
   and `us-federal-awards-scraper`**, both last tested 1301. Re-derive with `--type varied_test`,
   don't trust this prose. Design per the 6 LEARNINGS-1628/1632/1633/1637 rules: (1) cross an
   untested code-path boundary from the Actor's own `enum_audit`/other notes; (2) isolate a
   one-sided multi-value result before recording a pass; (3) decompose 0-row results with free
   LOCAL/raw-API runs first; (4) ask the REACHABLE DOMAIN of a filter, not just whether it's
   applied; (5) re-read log/status-message TEXT when verification touches it, not just row counts;
   (6) when a zero-row path has BOTH a specific-cause warning and a separate generic remedy, check
   whether the generic remedy can fire on top of the specific one with wrong advice, and gate it
   off when the specific cause is structural (see LEARNINGS 1637 for the full writeup).
   (l) still open, unchanged since 1626: `bin/dmarc-report list` shows no report with attachments
   yet — the one message on file (`26f70451`) is still the same pre-fix 2026-10-04 report, no
   successor (10+ days). Keep checking `bin/inbox list`/`bin/dmarc-report list` each cycle; nothing
   to do until a fresh one lands.
   (n) unchanged, not due until ~1964: sam-gov's 4 untested `dataType` branches
   (`wage-determinations-dbra`/`-sca`/`-cba`, `exclusions`).

NEXT-CYCLE (**1635: `varied_test` on `eu-ted-tenders-scraper` DONE — stamped 1635 in
   `state/audit_dates.json` (full note there + STATUS.md). Crossed TWO boundaries untouched by
   any varied_test since 1298: (1) cycle-1533 `enum_audit` fix adding `procedureType:"comp-tend"`
   (18th code) — `{procedureType:["comp-tend"],maxResults:5}` -> 5/5 rows exactly `"comp-tend"`
   across 3 countries/3 dates, confirming it's live-filterable (procedure-type is exact-match,
   not subtree-matched like cpvCodes). (2) cycle-1552 `unreachable_remedy` fix (`emptyResultAdvice()`
   correctly blaming an explicit `publicationDateFrom`/`publicationDateTo` window instead of the
   ignored `publishedWithinDays`) — read via `runs`+log GET per LEARNINGS rule 5, not just row
   count: `{publicationDateFrom:"2030-01-01", publicationDateTo:"2030-01-02",
   publishedWithinDays:365, maxResults:5}` -> 0 rows, live statusMessage correctly named the two
   date filters, correctly said publishedWithinDays was "ignored", correctly omitted CPV (empty)
   — matches the 1552 fix's case (a) exactly, live for the first time since that fix shipped.
   Genuinely clean both runs, no code/README change.**
   **`bin/audit-due --type varied_test` now shows 1 DUE: `nih-reporter-scraper` (NEXT TARGET)**,
   last tested 1298. Then the 1637 cluster (`sec-insider-trades-scraper`,
   `uk-find-a-tender-scraper`, `us-federal-awards-scraper`). Re-derive with `--type varied_test`,
   don't trust this prose. Design per the 5 LEARNINGS-1628/1632/1633 rules: (1) cross an untested
   code-path boundary from the Actor's own `enum_audit`/other notes; (2) isolate a one-sided
   multi-value result before recording a pass; (3) decompose 0-row results with free LOCAL runs
   first; (4) ask the REACHABLE DOMAIN of a filter, not just whether it's applied; (5) re-read
   log/status-message TEXT when verification touches it, not just row counts.
   (l) still open, unchanged since 1626: `bin/dmarc-report list` shows no report with attachments
   yet — the one message on file (`26f70451`) is still the same pre-fix 2026-10-04 report, no
   successor (10+ days). Keep checking `bin/inbox list`/`bin/dmarc-report list` each cycle; nothing
   to do until a fresh one lands.
   (n) unchanged, not due until ~1964: sam-gov's 4 untested `dataType` branches
   (`wage-determinations-dbra`/`-sca`/`-cba`, `exclusions`).

NEXT-CYCLE (**1634: `varied_test` on `court-records-scraper` DONE — stamped 1634 in
   `state/audit_dates.json` (full note there + STATUS.md). Crossed the cycle-1307 `enum_audit`
   `docketOnlyFilters`-narrowing boundary (`partyName`/`attorneyName` restrict `recordType:"both"`
   to dockets, `main.js:300-312`) composed with the `sortBy`-two-index heads-up at `main.js:428-431`
   — neither touched by a varied_test since 1298 (pre-1307). Platform run `{recordType:"both",
   partyName:"Smith", sortBy:"dateFiledDesc", courts:["ca9"], maxResults:5}` (fetched via `runs` +
   a direct log GET, not `bin/varied-test`, specifically to read log text per LEARNINGS rule 5):
   narrowing warning fired correctly, and the sortBy info line correctly did NOT fire because
   narrowing runs first in source order and had already shrunk `recordTypes` to length 1 — confirms
   the heads-up reflects the post-narrowing index count, not the raw `"both"` request. 5/5 rows
   `docket`, all contain "smith" in parties/attorneys (substring match, not exact-name), `dateFiled`
   strictly descending (sortBy honoured). Genuinely clean, no code/README change.**
   **`bin/audit-due --type varied_test` now shows 2 DUE in this cluster: `eu-ted-tenders-scraper`
   (NEXT TARGET) and `nih-reporter-scraper`, both last tested 1298.** Then the next cluster at 1637
   (`sec-insider-trades-scraper`, `uk-find-a-tender-scraper`, `us-federal-awards-scraper`).
   Re-derive with `--type varied_test`, don't trust this prose. Design per the 5 LEARNINGS-1628/
   1632/1633 rules: (1) cross an untested code-path boundary from the Actor's own `enum_audit`/other
   notes; (2) isolate a one-sided multi-value result before recording a pass; (3) decompose 0-row
   results with free LOCAL runs first; (4) ask the REACHABLE DOMAIN of a filter, not just whether
   it's applied; (5) re-read log/status-message TEXT when verification touches it, not just row
   counts.
   (l) still open, unchanged since 1626: `bin/dmarc-report list` shows no report with attachments
   yet — the one message on file (`26f70451`) is still the same pre-fix 2026-10-04 report, no
   successor (10+ days). Keep checking `bin/inbox list`/`bin/dmarc-report list` each cycle; nothing
   to do until a fresh one lands.
   (n) unchanged, not due until ~1964: sam-gov's 4 untested `dataType` branches
   (`wage-determinations-dbra`/`-sca`/`-cba`, `exclusions`).

NEXT-CYCLE (**1633: `varied_test` on `substack-scraper` DONE — stamped 1633 in
   `state/audit_dates.json` (full note there + STATUS.md). Not a no-op: found and fixed a real
   buyer-facing defect, same bug CLASS as 1632's but a different instance. Crossed the cycle-1525
   `enum_audit` `isRestack` boundary (confirmed live, unregressed: 3/50 rows on `jcbruce`, matches
   the 1525 measurement) composed with the `publishedAfter`/`publishedBefore` date window (per the
   1632 follow-up (3)/(4) below — this Actor's date filter interacts with `maxPostsPerPublication`
   depth capping, not multi-source feed reach, but the same "what's the reachable domain" question
   applies). Found: the zero-row `statusMessage` never mentioned a reached depth cap even when it
   was pushed to `depthCapped[]` — only the non-zero-row branch (fixed at cycle 1555) checked it.
   Fixed: added the missing check to the zero-row causes array. Build 0.1.70 (package.json
   0.1.17->0.1.18), verified live (re-ran the exact repro, both causes now present in
   `statusMessage`). Free local regression clean (20/20), `check-code-fields` 64/64,
   `check-filter-reach` 0/0.**
   **`bin/audit-due --type varied_test` now shows 0 DUE — the 1631/1632/1633 trio is the whole
   current backlog, all three cleared.** Next due is a 3-Actor cluster at cycle 1634
   (`court-records-scraper`, `eu-ted-tenders-scraper`, `nih-reporter-scraper`), then another
   3-Actor cluster at 1637 (`sec-insider-trades-scraper`, `uk-find-a-tender-scraper`,
   `us-federal-awards-scraper`). Re-derive with `--type varied_test`, don't trust this prose.
   Design per the by-now-5 LEARNINGS-1628/1632 rules: (1) cross a code-path boundary some earlier
   fix created that no varied_test has re-run — read the Actor's own `enum_audit`/other notes in
   `audit_dates.json`; (2) if a multi-value filter returns only ONE requested value, isolate it
   before recording a pass; (3) decompose a 0-row result with free LOCAL runs before spending
   another platform call; (4) ask what the REACHABLE DOMAIN of a filter is, not just whether it's
   applied; (5) when verification touches LOG/status-message output, re-read the actual log/message
   text, not just the row count — that's what caught both 1632's and 1633's real findings.
   **Generalized follow-up (NOT blocking, still just opportunistic per 1632):** the "does the
   zero-row status message name every active cause, including a depth/reach cap" question is now
   2-for-2 (remote-jobs-scraper 1632, substack-scraper 1633) for finding a real gap. Worth a glance
   on any Actor with both a date/depth-style cap AND a multi-cause zero-row message whenever a
   cycle is already touching it for its own varied_test — do NOT start a dedicated fleet-wide sweep
   for this; let `audit-due` keep driving which Actor gets touched when.
   (l) still open, unchanged since 1626: `bin/dmarc-report list` shows no report with attachments
   yet — the one message on file (`26f70451`) is still the same pre-fix 2026-10-04 report, no
   successor (9+ days). Keep checking `bin/inbox list`/`bin/dmarc-report list` each cycle; nothing
   to do until a fresh one lands. Per the 1629 correction, do NOT try to answer the `p=quarantine`
   backscatter question from current silence — wait for the next real burst and compare its
   rate/senders to the pre-10/04 pattern.
   (n) unchanged, not due until ~1964: sam-gov's 4 untested `dataType` branches
   (`wage-determinations-dbra`/`-sca`/`-cba`, `exclusions`).

NEXT-CYCLE (**1631: `varied_test` on `ats-jobs-scraper` DONE — stamped clean cycle 1631 in
   `state/audit_dates.json`, full note there + STATUS.md. Tested `employmentTypeKeyword`
   (cycle-1528's enum_audit addition, never exercised by a varied_test run before): Ashby+
   SmartRecruiters match path, Greenhouse warn path, Workday match path, all clean. One rule-2
   isolation applied (smartrecruiters alone, confirmed genuine 0-match data not a dropped value).**
   **`bin/audit-due --type varied_test` still shows 2 DUE (same rotation, both last tested 1295
   same as ats-jobs-scraper was): `remote-jobs-scraper` (NEXT TARGET) and `substack-scraper`.
   Pick `remote-jobs-scraper` first next cycle. Design per the two LEARNINGS-1628 rules: (1)
   cross a known code-path boundary (read the Actor's `enum_audit`/other notes for one — e.g. a
   field/filter a past fix added that no varied_test has touched since), (2) if a multi-value
   filter test returns only ONE of the requested values, re-run with the missing value ALONE
   before recording a pass.**
   **Retired `wellfound-jobs-scraper` for good (NICHES.md item 8, stale since cycle ~62) — see
   LEARNINGS cycle 1630. Site now Turnstile-gated + niche now has an unbeatable 2414-user leader.
   Do not re-check without a new reason.**
   (l) still open, unchanged: `bin/dmarc-report list` shows no report with attachments yet — the
   one message on file (`26f70451`) is the same pre-fix 2026-10-04 report, no successor since.
   Keep checking `bin/inbox list`/`bin/dmarc-report list` each cycle; nothing to do until a fresh
   one lands.
   (n) unchanged, not due until ~1964: sam-gov's 4 untested `dataType` branches
   (`wage-determinations-dbra`/`-sca`/`-cba`, `exclusions`).

NEXT-CYCLE (**1629: no open backlog item (re-confirmed empty — `audit-due` default + `--type
   varied_test` both NONE DUE, `checks-due` NONE DUE, services/site healthy, traffic/dev.to
   unchanged). Spent the cycle on a real correction instead of forced busywork — see LEARNINGS
   cycle 1629 for full detail.**
   **(l) CORRECTED: the open question 1626 filed ("does `p=quarantine` reduce backscatter vs. a
   steady pre-tightening rate?") has NO premise to test.** A full timestamp-sorted dump of
   `mail/inbox/*.json` (not just `bin/inbox list 10`) shows the backscatter/autoreply cluster
   all arrived 2026-10-01 to 2026-10-04, then NOTHING of that shape since (9-day silence as of
   1629) — predating the 2026-10-12T22:10Z DMARC change by over a week. Every STATUS entry since
   ~1617 saying "same senders as cycle M" was reading a frozen last-10 view, not fresh mail.
   **Do not try to answer the quarantine question from current silence — wait for the next real
   burst, then compare its rate/senders to the pre-10/04 pattern.** `bin/dmarc-report list` still
   shows no report with attachments (the one real report, `26f70451`, is from 2026-10-04 with no
   successor in 9 days despite earlier ~daily cadence — not an outage, mail service confirmed
   active; just don't expect one imminently). Keep checking each cycle as before.
   **(m) `varied_test` NEXT DUE: `ats-jobs-scraper`, cycle 1631 (2 cycles away).** Re-derive with
   `bin/audit-due --type varied_test` (not plain `bin/audit-due`). Design per the two LEARNINGS-
   1628 rules: (1) cross a known code-path boundary (read the Actor's `enum_audit`/other notes
   for one), (2) if a multi-value filter test returns only ONE of the requested values, re-run
   with the missing value ALONE before recording a pass.
   **(n) Named follow-up target for sam-gov's own note (not due until ~1964):** 4 of 6 `dataType`
   branches still untested by varied-test (`wage-determinations-dbra`/`-sca`/`-cba`,
   `exclusions`). `assistance-listings` was done at 1628 (clean).

NEXT-CYCLE (**1628: WORKED THE `varied_test` ROTATION — all 3 due Actors cleared and stamped
   (grants-gov, sam-gov, trademark-search; all last tested cycle 1292). 5 capped platform runs,
   ~$0.02, all clean, no code/README change needed. `state/audit_dates.json` stamped
   `varied_test: 1628` + full notes; clean_streak 1 ⇒ interval now 672c on all three.**
   **(m) NEXT varied_test IS IMMINENT: `ats-jobs-scraper`, cycle 1631.** Re-derive with
   `bin/audit-due --type varied_test` (NOT plain `bin/audit-due` — that only prints
   `competitor_audit` and will say NONE DUE while a `--type` rotation is genuinely due;
   that flag is the whole reason this cycle found work). Design the input per the two
   LEARNINGS-1628 rules, do not just permute the same filters 1292-era tests used:
   (1) cross a known code-path boundary (a branch some earlier fix created and nothing has
   re-run since — read the Actor's OTHER audit notes, e.g. `enum_audit`, to find one);
   (2) if a multi-value filter test comes back showing only ONE of the requested values,
   re-run with the missing value ALONE before recording a pass — otherwise the result is
   indistinguishable from an Actor that drops every value after the first.
   **(n) Named follow-up target, from sam-gov's own note:** 4 of 6 `dataType` branches are
   STILL untested by varied-test (`wage-determinations-dbra`/`-sca`/`-cba`, `exclusions`).
   This cycle did `assistance-listings` (clean). Pick one of those 4 next time sam-gov comes
   due (~1964) rather than another opportunities-mode permutation. Note wage-determination
   modes support only keyword/state/activeOnly/maxResults — NAICS/setAside/noticeType/
   enrichDetail are opportunity-only and ignored with a warning, so don't read their absence
   as a defect.
   (l) below is STILL NOT RESOLVED at 1628: `bin/dmarc-report list` shows no report with
   attachments yet — keep checking each cycle.

NEXT-CYCLE (**1627: no open backlog item — confirmed empty, not assumed (re-checked `audit-due`
   all 4 types incl. `varied_test`, `checks-due` all 13 fleet checks, `state/health.json` 23/23
   OK, inbox, traffic, dev.to calendar — all NONE DUE / nothing actionable). (l) below is STILL
   NOT RESOLVED: `bin/dmarc-report list` shows no report with attachments yet — keep checking it
   each cycle until Google's next daily report lands, then read the per-source SPF/DKIM table.**
   **Closed a small real gap instead: `dmarc-report` was the one UNCLASSIFIED tool in
   `state/fleet_checks.json` / `bin/checks-due --map` (added cycle 1626, never classified).
   Filed as `operational` (event-triggered via the per-cycle `inbox list`, not a standalone
   clock) — `--map` now shows 0 unclassified.** Also trimmed `STATUS.md` 14→12 blocks (archived
   1609-1612 into `STATUS_ARCHIVE.md`, including a dangling headerless "PRIOR (cycle 1609):"
   stub a past trim had left behind — real 1609 content was already safely archived).
   Ran `bin/check-disclosure` as a spot-check (0/70 missing) — note for next cycle: it's
   classified `rotation_support` (gated by `competitor_audit`), so don't treat this run as
   having established a standalone cadence for it.

NEXT-CYCLE (**1626: closed (k) — `mail/receiver.py` now captures attachments (base64, 2 MiB
   cap), `bin/dmarc-report list`/`read` parses the gzip/zip DMARC XML into a per-source
   SPF/DKIM pass/fail table. Verified locally via smtplib against our own :25 listener (no
   external mail sent, test messages deleted); required and confirmed a `systemctl restart
   fetchsmith-mail`. The one pre-fix report (`26f70451`) is unrecoverable — raw bytes were
   never persisted — so (l) below still needs a FRESH report to resolve, not that one.**
   (l) **Re-check once a real DMARC report lands (Google typically sends daily — check
   `bin/dmarc-report list` each cycle until one appears with attachments):** read the
   per-source SPF/DKIM breakdown. If 0 unexpected failures from our own Resend/SES paths,
   that's the direct evidence 1625's `p=quarantine` move lacked — safe to consider `p=reject`
   next. Separately: does `p=quarantine` reduce the SEO-spam/Japanese-form-autoreply/DMARC-
   backscatter noise in `bin/inbox list` (steady ~10 msgs/cycle for 10+ cycles pre-tightening)?
   If it does NOT drop, that's a sign most backscatter originates from receivers that don't
   enforce DMARC at all (tightening further buys nothing there, just a one-time hygiene fix).
   No other open backlog item — everything else below is unchanged carryover from 1621-1624.

NEXT-CYCLE (**1624: no open backlog item of any kind (unchanged from 1621-1623). Closed 1623's
   filed follow-up, but NOT as filed — see (a). Shipped `state/fleet_checks.json` + `bin/checks-due`
   so fleet-wide checkers have a tracked cadence, and used the seeding scan to find and clear 3
   genuinely rotted checks.**
   (a) **DONE, with a correction to how 1623 filed it:** 1623 asked for a `competitor_claims` type in
   `audit_dates.json`. That is **unimplementable as written** — `audit_dates.json` is keyed PER ACTOR
   and a no-argument fleet-wide sweep has no per-Actor row (it would mean stamping one cycle number
   onto 24 Actors per run). Shipped as a sibling registry instead: `state/fleet_checks.json` (13
   cadence entries, each interval justified from measured drift in its own note) + `bin/checks-due`
   (`bin/checks-due` = what's due, `--ran <tool> --note '...'` = record a run IN THE SAME CYCLE,
   `--map` = the deliberate no-cadence classification of every other tool in `bin/`). `bin/audit-due`
   now prints a `FLEET CHECKS:` footer every run — that is the discovery hook, don't remove it.
   **Nothing is due until ~cycle 1767** (`check-competitor-claims`), so do NOT re-run these sweeps
   out of habit; `bin/checks-due` is the authority now, not queue prose.
   (b) **Seeding method worth reusing (LEARNINGS 1624):** the session transcripts
   `/root/.claude/projects/-root/*.jsonl` are a hard audit log of what past cycles actually ran —
   scan `"command"` strings for `bin/<tool>`, map file mtime to a cycle via `worker.log`'s
   `cycle=N ... start` lines (`/tmp/scan_tool_runs.py`, ~40 s for all 1442 files / 70 tools). It
   over-estimates recency (can't tell a run from `wc -l` on the script), so treat results as an
   upper bound. This beats grepping STATUS_ARCHIVE prose for claims *about* runs.
   (c) **Cleared by that scan this cycle:** `check-blog-cta` (108 cycles unrun) → 53 posts, 0
   missing-CTA/0 bad-slug/0 dead-link; `check-own-source-count` (118 unrun) → 7 phrases / 3 Actors,
   0 flagged. `check-rental-converts` (117 unrun, last 1507) is registered at 672c and is NOT due —
   it may be closeable outright once the 2026-10-01 rental-deprecation wave has clearly passed;
   decide that the next time it comes due rather than re-running it early.
   (d) **Audit rotations (`bin/audit-due`, re-derive at the top of the cycle that lands there):**
   `varied_test` soonest grants-gov-scraper ~cycle 1628 (NEAREST — this is the next real rotation
   work); `enum_audit` sec-insider-trades-scraper ~1640; `competitor_audit` app-store-reviews-scraper
   ~1779; `watch_subset_audit` fda-recall-scraper ~1896. `category_lever` stays CLOSED (1620) — do
   not re-open it.
   (e) **dev.to: not due by calendar.** Cadence is the first cycle landing ON OR AFTER 2026-10-14;
   today is 2026-10-12, so 1624 did not re-check the API. Re-check the live API (never queue.md
   prose) before writing. Note `devto-post` is deliberately classified `operational` in
   `fleet_checks.json` (its cadence is the editorial calendar, not a checker clock) — the cadence
   entry is `devto-comments`, 144c, next due ~1767.
   (f) **SUPERSEDED:** the old item (f) asking for `check-usaspending-vocab` every 20-30 cycles is
   now a registry entry at 480c, with the deviation and its reasoning recorded in the entry's note
   (0 drift at both 1616 and 1620 against a published federal code list; shorten it again only if a
   run comes back non-zero). Do not re-add the 20-30c figure from archived prose.
   (g) `readme_proximity` is NOT a growth lever (cycle 1468). `new-Actor search` is opportunistic
   only — formally closed at cycle 1497. 1617's dev.to/competitor-comparison candidate list was
   retracted at 1622 (all 4 Actors already exhaustively audited) — do not pick from it.
   (h) **Optional, low value, explicitly deferred (unchanged since 1620):** 9 Actors have an unused
   3rd category slot (ats-jobs, eu-ted, uk-find-a-tender, fec-campaign-finance, court-records,
   trademark-search, sam-gov, remote-jobs, sec-insider-trades). Browse value is provably ~0
   (`category_lever`, closed 1620); only do it as a cheap add-on if a cycle is already publishing
   that Actor for another reason.
   (i) Buyer-intent traffic NOT re-measured at 1624 (nothing suggests movement in 30 min); 1623's
   `bin/traffic 7`: `tools` 37/7d, `pricing` 1/7d, `checkout` 1/7d — far below the CLAUDE.md Polar
   gate. Always use `bin/traffic`'s bot-filtered numbers, never a raw `SELECT count(*) FROM
   pageviews` (~95% of raw /pricing hits are our own cron `curl` health checks).
   (j) **Process check (1622's lesson, applied):** run `git status` near the END of the cycle and
   confirm it is actually clean before writing "committed" anywhere. 1624 did; commit `33c1d003` (this hash-correction note is a follow-up commit on top).
   Routine checks at 1624 (21:3x-21:5x UTC 2026-10-12): 3 services active, site `/`, `/tools`,
   `/pricing` all 200, inbox 10 msgs all SEO-spam/form-autoreply/DMARC backscatter (same senders as
   1622/1623, nothing needing a reply), `audit-due` NONE DUE on all 4 real rotations, `checks-due`
   NONE DUE, $0 revenue, 24 Actors / 44 users / 0 bookmarks / 0 reviews, 647 runs30d (644 ext_ok / 3
   ext_bad). $0 spent — no Actor runs, no paid service; only local file edits, a local transcript
   scan, two local checkers and one `git commit`.

   **DONE this cycle (1624): shipped `state/fleet_checks.json` + `bin/checks-due` + the `audit-due`
   FLEET CHECKS footer (verified live), seeded from a transcript scan dating all 70 tools in `bin/`,
   and ran the two most-rotted fleet checks it surfaced (`check-blog-cta` 108c, `check-own-source-count`
   118c) — both clean, no README/code/site change. PLAYBOOK (Nightly maintenance) + LEARNINGS updated.**
   No owner email warranted (mechanism + routine verification, no revenue event, no outage, nothing
   owner-only-fixable).

---
