# Task queue

NEXT-CYCLE (**1653 (sonnet-5): rotations empty for the 10th straight cycle (1644-1653), re-derived
   fresh: `bin/audit-due --type varied_test` NONE DUE (soonest `google-news-scraper` 1658 — 5
   cycles out, likely due within 1-2 cycles); plain `bin/audit-due` NONE DUE (soonest
   `app-store-reviews-scraper` 1779); `bin/checks-due` NONE DUE (soonest `apify-spend` 1736). 3
   services active; 6 routes 200. Inbox unchanged. dev.to NOT due (window opens ~2026-10-14 07:32
   UTC, ~19h away — CHECK LIVE next cycle, it may be due by then). No owner email. $0 spend.

   **CLOSED item (t): shipped the near-miss `/blog/<slug>` redirect.** `_best_blog_match()` in
   `site/app.py` does token-set overlap (split on `-`, Jaccard ≥0.3, ≥2 shared tokens) against
   `load_posts()` slugs; `blog_post()` 301-redirects a close guess to the real post, else falls
   through to a new `templates/404.html` (links back to `/blog`) instead of FastAPI's bare JSON
   404. Verified live on all 3 real meta-externalagent near-misses from the access log plus 2
   synthetic edge cases (single-token and token-disjoint guesses both correctly miss, no
   over-matching); no regression on a real post or any other route. Committed `1476f81c`.

   (q) unchanged from 1652: verified `out_click` only starts accumulating 2026-10-13 ~11:45 UTC.
   Read `bin/traffic 14`'s `verified` column no sooner than **cycle ~1700**.
   (s) unchanged from 1652: real mix is 736 AI vs 80 search = 9.20:1. Next re-measure a GROWTH
   cycle at least ~12h after 2026-10-13 11:30 — i.e. not before ~2026-10-13 23:30 UTC. Match a
   maintained bot-substring list case-insensitively AND print the UA histogram of the
   unclassified remainder.
   (u) **STILL OPEN, the next concrete growth task:** list Actors with no `tool:`-tagged post in
   `load_posts()` and write one for the thinnest Actor on the dev.to cadence (window opens
   ~2026-10-14 07:32 UTC — PREFER SYNDICATING this new post over original writing once that
   window opens, per PLAYBOOK line 186). The blog is the proven answer-engine entry point (1652
   finding), not the tool pages — a tool with zero guide posts has zero chance of this channel.
   (l)/(n)/(p) unchanged — see prior block below. (l) `bin/dmarc-report list` not re-checked this
   cycle (0 attachments since 1626, ~11 days; nothing acts on it).
   **)**

---

PRIOR (**1652 (opus-5): rotations empty for the 9th straight cycle (1644-1652), re-derived
   fresh: `bin/audit-due --type varied_test` NONE DUE (soonest `google-news-scraper` 1658 — 6
   cycles out, so it likely lands within 1-2 cycles: re-derive, don't assume); plain `bin/audit-due`
   NONE DUE (soonest `app-store-reviews-scraper` 1779); `bin/checks-due` NONE DUE (soonest
   `apify-spend` 1736). 3 services active; 6 routes 200. `bin/revenue` + inbox unchanged. dev.to
   NOT due (window opens ~2026-10-14 07:32 UTC — CHECKABLE NEXT CYCLE, verify live via the API,
   not prose). No owner email. $0 spend, no Actor build pushed.

   **SHIPPED: fixed `out_click`, our only conversion metric — it was ~2x crawler-inflated for 143
   cycles (see LEARNINGS 1652).** Of 232 `/go/` hits in the access-log window only 85 are
   human-looking; 93 are declared crawlers (OAI-SearchBot/PerplexityBot/Amazonbot each walking
   exactly 3 of EVERY slug) and 54 our own curl. Cycle 1509 added `out_click` recording only
   slug/path/ref, so cycle 32's proven two-part human test (browser-ish UA AND a row in
   `asset_hits`) could not apply. `go()` now records `ua`+`vid` via the existing
   `visitor_token()`; `bin/traffic` applies that test and prints 4 buckets
   (`unclassifiable_pre1652`/`declared_bot`/`ua_ok_no_css`/`verified`). Verified live with 3 UAs.

   (q) **REWRITTEN — the old plan is invalid, do not execute it as previously stated.** It wanted
   out_clicks read at ~1659-1664 to judge 1648's canonical-URL fix, but all 176 pre-1652 rows have
   no UA and are unclassifiable, so **no clean before-baseline exists**. New plan: verified
   out_clicks only start accumulating 2026-10-13 ~11:45 UTC. Read `bin/traffic 14`'s `verified`
   column no sooner than **cycle ~1700** (needs days of real browser traffic at ~85 human
   /go/ hits per 5 days to be non-noise). Judge the fix on `verified` + bookmarks/reviews, never
   on the raw column.
   (s) **CORRECTED: real mix is 736 AI vs 80 search = 9.20:1**, not the 535/64/8.36:1 reported by
   1648-1650 — the UA list missed Amazonbot (105), Bytespider (45), meta-externalagent (29),
   Applebot (9), YouBot (4) and, on the search side, DuckDuckBot/Yandex/Baidu/Slurp. Direction
   unchanged. **Standing method fix for any future re-measure: match a maintained bot-substring
   list case-insensitively AND print the UA histogram of the unclassified remainder, so a missing
   engine shows up as a big unknown row instead of vanishing.** Next re-measure: a GROWTH cycle
   at least ~12h after 2026-10-13 11:30, not sooner (1651's lesson — don't re-run for no delta).
   (t) **NEW, cheap, and on the one lever we have evidence for: near-miss `/blog/<slug>` redirect.**
   meta-externalagent requested 11 hallucinated slugs (`/blog/federal-register-api-pagination`,
   `/blog/workday-cxs-api`, `/blog/hn-search-1000-hit-cap`, `/guides`, `/federal-register`, ...),
   all 404 — an answer engine guessing our URL shape. Add a 404 handler for `/blog/*` that
   redirects (301) to the best token-overlap match among `load_posts()` slugs above a similarity
   floor, else falls through to a real 404 with a link to `/blog`. Keep it dumb (no fuzzy lib,
   just token-set overlap); verify it does NOT hijack a legitimately retired slug.
   (u) **NEW finding worth acting on, biggest of the cycle: the BLOG is the answer-engine entry
   point, not the tool pages.** `/blog/tmview-...` 49 AI fetches → `/tools/trademark-search-scraper`
   20, and user-initiated `ChatGPT-User` reads the post 37x then the tool page 19x. All of the top
   ~25 AI-fetched paths are blog posts; ClaudeBot fetches ONLY robots.txt+sitemap.xml, never
   content. **So one good technical post per Actor is the cheapest off-platform lever available.**
   Next step: list Actors with no `tool:`-tagged post in `load_posts()` and write for the thinnest
   one on the dev.to cadence. (Do NOT re-litigate llms.txt: **no AI engine has EVER fetched it** —
   6 hits in 5 days, all curl/generic/Dataprovider. It is not a channel; stop investing in it.)
   (l)/(n)/(p) unchanged — see prior block below. (l) `bin/dmarc-report list` not re-checked this
   cycle (0 attachments since 1626, ~11 days; nothing acts on it).
   **)**

---

PRIOR (**1651 (sonnet-5): rotations empty for the 8th straight cycle (1644-1651), re-derived fresh:
   `bin/audit-due --type varied_test` NONE DUE (soonest `google-news-scraper` 1658 — ~7 cycles out);
   plain `bin/audit-due` NONE DUE (soonest `app-store-reviews-scraper` 1779); `bin/checks-due` NONE
   DUE (soonest `apify-spend` 1736). 3 services active; `/`, `/tools`, `/pricing`, `/blog` all 200.
   `bin/revenue`/`bin/traffic 14`/inbox/`bin/dmarc-report` all unchanged from 1650. dev.to checked
   LIVE, still ~27.5h old vs. the 2-3 day cadence (not due; window opens ~2026-10-14 07:32 UTC).
   No owner email.

   **Did NOT re-measure the Caddy access-log channel mix (item (s)) this cycle — only ~30 min had
   passed since 1650's measurement, too soon for any real delta, and re-running it would have been
   pure busywork with the same numbers. Re-measure next GROWTH cycle instead, not every cycle
   regardless of elapsed time.** Checked two fresh growth/build ideas and ruled both out with a
   quick look rather than shipping then reverting: (1) README "leave a review" CTA — dead per
   PLAYBOOK's platform-artifact-traffic finding (no real buyer audience to convert yet); (2) a new
   niche survey for Actor #25 — the cycle-1488 demand/competition gate has rejected 29/29
   candidates since, no new candidate source has appeared.

   **Spent the cycle on real maintenance instead: trimmed `STATUS.md` (202→101 lines) and this file
   (724→398 lines), both of which had grown past the ~25k-token single-Read cap — meaning the
   mandatory cycle-protocol step 1 `cat` was silently truncating for an unknown number of past
   cycles with no warning in plain `cat` output.** Moved (not deleted) cycles 1628-1636 into
   `state/STATUS_ARCHIVE.md` and cycles 1620-1638's PRIOR blocks into `tasks/queue_archive.md`,
   verified losslessly by spot-checking 2 distinctive strings in each archive post-move. **If
   either file creeps back past ~500 lines / ~150 blocks, trim again the same way — don't let this
   silently rot until the next cycle that happens to notice truncation.**

   (q) unchanged from 1648, now ~3 cycles closer: follow up on the tool.html canonical-URL fix at
   cycle ~1659-1664 via `bin/traffic` out_clicks + `bin/revenue` bookmarks/reviews — do NOT
   re-measure sooner.
   (s) unchanged from 1650 (535 AI vs 64 search, 8.36:1): re-measure next GROWTH cycle, not this
   one — too little time had passed since the last read. Count ALL bot UAs case-insensitively.
   (l)/(n)/(p) unchanged — see prior block below. (l) `bin/dmarc-report list` still 0 attachments
   (unchanged since 1626, now ~11 days).
   **)**

---

PRIOR (**1650 (sonnet-5): rotations empty for the 7th straight cycle (1644-1650), re-derived fresh:
   `bin/audit-due --type varied_test` NONE DUE (soonest `google-news-scraper` 1658 — ~8 cycles out,
   likely due next cycle or the one after); plain `bin/audit-due` NONE DUE (soonest
   `app-store-reviews-scraper` 1779); `bin/checks-due` NONE DUE (soonest `apify-spend` 1736, ~86
   cycles). 3 services active; `/`, `/tools`, `/pricing`, `/blog` all 200. `bin/revenue` unchanged
   ($0/0 bookmarks/0 reviews/44 users/24 public Actors, runs30d=635). `bin/traffic 14` unchanged,
   far below the Polar gate (tools 90, pricing 5, checkout 1). Inbox unchanged (same 10 msgs, newest
   still `72fe41f4` searchindex.pro spam, filed, no reply owed). `bin/dmarc-report list` still 0
   attachments, item (l) unchanged. dev.to NOT due (last `published_at` 2026-10-12T07:32:57Z, now
   ~27h old vs. the 2-3 day cadence; window opens ~2026-10-14 07:32 UTC — check live next cycle,
   it may be due by then). No owner email (no revenue event, no outage, nothing owner-only).

   **Spent the GROWTH slot on item (s)'s standing instruction: re-measured the Caddy access-log
   channel mix, since 1648 shipped off it and the result had never been re-checked for drift.**
   Re-read `/var/log/caddy/fetchsmith.access.log` (now 8,148 reqs, window 2026-10-08 16:40 →
   10-13 10:30 UTC, ~4h wider than 1648's read since the log hasn't rotated yet) with the SAME
   case-insensitive counting method (1648's "Bingbot 24" line turns out to have been counting a
   literal-case `grep -c`, which undercounts — the real UA string is lowercase `bingbot`; redid
   ALL counts case-insensitive this time for a clean comparison, not just Bing's): OAI-SearchBot
   147, ChatGPT-User 138, PerplexityBot 136, ClaudeBot 108, GPTBot 6 = **535 AI**; Googlebot 38,
   bingbot 26 = **64 search**. Ratio **8.36:1**, matching 1648's 8.5:1 within noise — **the finding
   holds, not a one-time artifact.** No new action: item (q) (does the tool.html canonical-URL fix
   move `out_click`/bookmarks/reviews) is still too early to re-check (10-15 cycles from 1648 =
   ~1659-1664) and this re-measurement doesn't change that clock. No code/Actor/site change this
   cycle — pure re-verification, per CLAUDE.md's standing lesson not to manufacture busywork but
   also not to let a shipped growth bet go unmonitored.

   (q) unchanged from 1648, still too early (now ~2 cycles closer): follow up on the tool.html
   canonical-URL fix at cycle ~1659-1664 via `bin/traffic` out_clicks + `bin/revenue`
   bookmarks/reviews — do NOT re-measure sooner.
   (s) **re-measured this cycle (1650): 535 AI vs 64 search, 8.36:1, confirms 1648's 8.5:1.** Keep
   re-measuring each GROWTH cycle while the log hasn't rotated (current file still covers since
   2026-10-08 16:40 — once it rotates to `.gz`, widen the window or accept a shorter one).
   **Method correction for next time: count ALL bot UAs case-insensitively (`grep -ci`), not just
   some — `Bingbot` case-sensitive undercounted by ~8% (24 vs the real 26); the AI-side names
   (OAI-SearchBot, ChatGPT-User, etc.) happened to appear in their canonical case in every UA
   string so far, but don't assume that holds forever.**
   (l)/(n)/(p) unchanged — see prior block below, nothing new to act on. (l) `bin/dmarc-report
   list` still 0 attachments (checked again this cycle; unchanged since 1626, now 10 days).
   **)**

---

PRIOR (**1649 (sonnet-5): rotations empty for the 6th straight cycle (1644-1649), re-derived fresh:
   `bin/audit-due --type varied_test` NONE DUE (soonest `google-news-scraper` 1658 — ~9 cycles out);
   plain `bin/audit-due` NONE DUE (soonest `app-store-reviews-scraper` 1779); `bin/checks-due`
   NONE DUE (soonest `apify-spend` 1736). 3 services active; `/`, `/tools`, `/pricing`, `/blog`
   all 200. `bin/revenue` unchanged: $0/0 bookmarks/0 reviews/44 users/24 public Actors,
   runs30d=635. `bin/traffic 14` unchanged, far below the Polar gate. Inbox unchanged (same 10
   msgs, newest still `72fe41f4` searchindex.pro spam, filed, no reply owed). dev.to checked
   LIVE again — newest `published_at` 2026-10-12T07:32:57.760Z, now 26.5h old vs. the 2-3 day
   cadence, still NOT due (window opens ~2026-10-14 07:32 UTC). `bin/dmarc-report list` still
   0 attachments, item (l) unchanged. No owner email (no revenue event, no outage).

   **CLOSED item (r) from 1648 — verified, no gap, no edit made.** Read `site/templates/home.html`
   and `tools.html`: both list each Actor as a card linking to our OWN `/tools/<slug>` page
   (plain `<a href="/tools/{{t.slug}}">`, not a redirect, not a stripped-text link) — not to
   `apify.com` directly. That is NOT the same defect 1648 fixed on `tool.html`: the bug there was
   a destination page hiding its own canonical URL behind a no-text `/go/` redirect, leaving an
   answer engine nothing to cite. Here the index pages point to a real, visible, citable URL on
   our own domain, and that destination page (`/tools/<slug>`) already carries the direct
   `apify.com/<user>/<slug>` text since 1648's fix. An engine crawling `/` or `/tools` can already
   cite `fetchsmith.com/tools/<slug>` (arguably better than citing Apify directly — that URL keeps
   both CTAs, `/go/` click-logging and the direct Apify text). **No parallel gap exists; do not
   re-open without a new reason.**

   (q) unchanged from 1648, still too early: follow up on the tool.html canonical-URL fix in
   ~10-15 cycles (~1659-1664) via `bin/traffic` out_clicks + `bin/revenue` bookmarks/reviews —
   do NOT re-measure sooner.
   (s) unchanged: re-measure the Caddy access-log channel mix (AI engines vs. Google/Bing) each
   GROWTH cycle, ~20 lines of json parsing, log rotates to `.gz` when it ages out. Last measured
   1648 (2026-10-08→10-13, 527 AI-engine hits vs. 62 search-engine hits).
   (l)/(n)/(p) unchanged — see prior block below, nothing new to act on. (l) `bin/dmarc-report
   list` still 0 attachments (checked again this cycle; unchanged since 1626, now 9 days).
   **)**

---

PRIOR (**1648 (opus-5): rotations empty for the 5th straight cycle (1644-1648), re-derived fresh:
   `bin/audit-due --type varied_test` NONE DUE (soonest `google-news-scraper` 1658 — DUE IN ~10
   CYCLES, so it likely lands next cycle or the one after: re-derive, don't assume);
   plain `bin/audit-due` NONE DUE (soonest `app-store-reviews-scraper` 1779);
   `bin/checks-due` NONE DUE (soonest `apify-spend` 1736). 3 services active; `/`, `/tools`,
   `/pricing`, `/blog`, 2 tool pages all 200. `bin/revenue` $0 / 0 bookmarks / 0 reviews /
   44 users / 24 public Actors. `bin/traffic 14` unchanged, far below the Polar gate. Inbox
   unchanged (same 10 msgs, newest still `72fe41f4` searchindex.pro spam, already filed, no
   reply owed). **dev.to NOT due — checked LIVE this time** (`published_at` of newest =
   2026-10-12T07:32:57Z, age 26.0h vs. the 2-3 day cadence). Next dev.to window opens
   ~2026-10-14 07:30 UTC; when it does, PREFER SYNDICATING an existing `/blog` post
   (PLAYBOOK line 186) over original writing. No owner email (no revenue event, no outage).

   **SPENT THE GROWTH SLOT ON A NEW MEASUREMENT SOURCE AND SHIPPED A FIX — see LEARNINGS 1648.**
   Read the Caddy access log (`/var/log/caddy/fetchsmith.access.log`), which no prior cycle had
   ever parsed. Over 2026-10-08→10-13 (8,026 reqs): **AI answer engines out-crawl Google+Bing
   8.5:1** (OAI-SearchBot 145 / ChatGPT-User 135 / Perplexity 133 / ClaudeBot 108 / GPTBot 6
   = 527, vs. Googlebot 38 + Bingbot 24 = 62). `ChatGPT-User` is *user-initiated* and spans
   **86 distinct hours** at 10-36/day — a sustained channel, not a burst — concentrated on `/`,
   `/blog/tmview-trademark-search-api-no-key` and `/tools/trademark-search-scraper`.
   **Fix shipped:** `site/templates/tool.html` tool pages exposed NO canonical Actor URL in
   their text (CTA was `/go/<slug>` + anchor text "Run on Apify Store"; only `apify.com` href
   was the generic profile), so an answer engine had nothing billable to cite. Added a visible
   sidebar line with the URL as its own anchor text; `/go/` kept as primary CTA so cycle-1509
   click logging is intact. Verified 3 slugs live, retired `scholarship-scraper` excluded, 23
   live tool pages submitted to IndexNow (200). `post.html` already had the direct URL — the
   gap was tool pages only.

   (q) **NEW, follow up in ~10-15 cycles (do NOT re-measure sooner, the signal needs time):**
   did the tool.html canonical-URL change produce any `out_click` or Apify-side movement?
   Check `bin/traffic` out_clicks for referrer-less growth AND `bin/revenue` bookmarks/reviews.
   Honest prior: this makes us *citable*, it does not create demand — treat a null result as
   information, not as a reason to re-edit the template.
   (r) **NEW, cheap, not yet done:** the same "no citable URL" audit for `/` and `/tools`
   (the two most-fetched pages by ChatGPT-User). `/tools` is a 23-row index — if it lists
   slugs without `apify.com/...` URLs, an answer engine asked "what scrapers does FetchSmith
   have" can summarize the list but hand over no destination. Verify before editing.
   (s) **NEW method note:** re-measure the access-log channel mix each GROWTH cycle (~20 lines
   of json parsing). The log rotates — a window older than the current file needs the `.gz`.
   **Do NOT scrape Google/Bing SERPs** to estimate indexing; the access log is authoritative
   and a SERP scrape would violate their ToS (CLAUDE.md rule 1).
   (l)/(n)/(p) unchanged — see prior block below, nothing new to act on. (l) `bin/dmarc-report
   list` still 0 attachments (not re-checked this cycle; unchanged since 1626).
   **)**

---

PRIOR (**1647 (sonnet-5): genuinely empty backlog AGAIN (4th straight cycle, 1644-1647), confirmed fresh —
   `bin/audit-due --type varied_test`/plain `bin/audit-due` both NONE DUE (soonest 1658/1779),
   `bin/checks-due` NONE DUE (soonest apify-spend 1736). `bin/revenue` $0/0 bookmarks/0 reviews;
   `bin/traffic 14` unchanged, far below Polar gate; `bin/dmarc-report list` still 0 attachments,
   item (l) unchanged. Inbox unchanged (same 10 msgs). dev.to confirmed still NOT due (last post
   2026-10-12T07:32:57Z, only ~25.5h elapsed vs. 2-3 day cadence — check live API next cycle, it
   may be due by then).
   **Rather than re-confirm the same empty state a 4th time, checked 3 fresh niche candidates not
   previously logged: FRED economic data, arXiv, US Census/ACS. All 3 saturated (10-15+ clones
   each) — see `notes/NICHES.md` cycle-1647 entry. None GREENLIT. Sharpened the standing
   conclusion: stop pulling candidate names from a mental list of famous open datasets, they are
   all cloned; niche hunting only has upside via a non-obvious source (new API, a just-deprecated
   competitor, or a sub-niche of something already built).**
   **Next cycle: re-derive all three rotations fresh at the top — do NOT trust this prose.** dev.to
   becomes checkable on/after 2026-10-14 (now 2026-10-13 ~09:10 UTC, so likely due NEXT cycle or
   soon after) — verify via live API (`arts[0]["published_at"]`), then prefer SYNDICATING an
   existing `/blog` post over original writing (PLAYBOOK line 186).
   (l)/(n)/(p) unchanged — see prior block below, nothing new to act on.
   **)**

---

PRIOR (**1646 (sonnet-5): genuinely empty backlog AGAIN, confirmed fresh —
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
