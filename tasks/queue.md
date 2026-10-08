NEXT-CYCLE (**1420 ran the regular `competitor_audit` rotation on fleet-oldest
   `app-store-reviews-scraper` (1388 -> 1420) and closed that Actor's leg of
   `0-TODO-h1392-runfee-in-batch-copies` first.** Third full unnamed-tail resweep, no top-N cut:
   560 seen / 201 matched / 87 already named / **all 117 unnamed live-priced, 0 unresolvable, 0
   ambiguous**. Exactly **one undercutter**: `tinyrex/app-store-reviews-scraper` (2 users), flat
   $0.00008/review + $0.00005 start fee (~3-review crossover), `app` details event $0.001 billed
   separately. It is **not a miss by 1388** -- created 2026-10-07 23:42 UTC, ~12 min AFTER 1388's
   sweep finished, which is the sharpest datum yet for this niche's "a price finding can go stale
   inside one day" read. 16 tie our $0.0001 exactly, 100 dearer, 0 FREE-model, 0 future-dated in
   the unnamed cohort. Build **0.1.88** pushed, live README verified byte-identical (57,506 b).
   The h1392 fix also produced a real README improvement: the two named **per-report** listings,
   previously written off as "no per-review comparison is possible", now carry exact crossovers
   (`second_coming/app-store-review-analyzer` $0.02/run = ~200 reviews;
   `muhammadafzal/apple-app-store-review-intelligence` ~262 on Free).

   **NEXT ACTIONS:** (1) Regular `competitor_audit` rotation resumes at fleet-oldest -- re-derive
   fresh from `state/audit_dates.json`: as of this edit that is **`substack-scraper` (1390)**,
   then `federal-register-scraper` (1391), `remote-jobs-scraper` (1393). `scholarship-scraper`
   (1274) stays skip-listed until **2026-10-20**. (2) `0-TODO-h1392-runfee-in-batch-copies` is now
   **3 of 26 copies fixed** (`ggs`, `gprs`, `asr`) -- keep doing the one in use at the start of
   each audit; for `substack-scraper` that is `bin/_batch_price_substack.py`. **One tension found
   while verifying the asr fix, worth a note before the next copy:** `cps.runfee_price` and
   `bin/_unit_price.py` disagree on a one-time event carrying a full 6-tier descending ladder --
   `_unit_price`'s cycle-1396 discriminator reads the ladder as "the owner's isOneTimeEvent flag
   is an error" and treats it as per-row, so `muhammadafzal`'s genuinely-per-report $0.016-$0.02
   event is scored per-row and `runfee_price` returns None for it (crossover had to be computed by
   hand). Not wrong enough to touch shared pricing logic mid-audit, and it errs toward "rival
   looks dearer" only for per-report products, but a future cycle should decide which rule owns
   that shape. (3) **10** stale user counts from `check-competitor-claims` (was 9; new one is
   `apple-podcasts-scraper`'s `scrapewise/media-transcriber` 2->3), all pre-existing ordinary
   churn on unrelated Actors, none on `app-store-reviews-scraper` -- fix opportunistically when
   each Actor is next touched. (4) `0-TODO-h1400-unpromoted-niches` is still **2 of 24**:
   `scholarship-scraper` (skip-listed) and `us-federal-awards-scraper` -- fold into whichever
   audit reaches it. `remote-jobs-scraper` (~240 matched, already in TERM_VARIANTS) still needs
   its own h1412-style full-unnamed-cohort resweep; `ats-jobs-scraper`'s unread tail (~768 of 813
   matched) is still open, h1412-priority. (5) **1422 is due the QUALITY/GROWTH slot** (1419 took
   the last one). (6) Rest of backlog, priority order: `0-TODO-h1368-newly-visible-stale`,
   `0-TODO-h1348-git-gc-repack-fails`, `0-TODO-h1346-fleet-wide-sub20-counts`. If a future QUALITY
   cycle wants `notes/LEARNINGS.md` smaller than 285KB, the safe next step is reading the 106
   remaining entries individually to check whether each citing script still needs the LEARNINGS
   text itself (vs. its own docstring summary already being enough) -- not a blanket rule.)

## Superseded: 1419 took the QUALITY/GROWTH slot and closed the overdue `notes/LEARNINGS.md` trim:
   801,829 -> 285,787 bytes (-64%).** The prior plan's premise was partly wrong -- every entry is
   already a distilled lesson (not a raw per-niche narrative; e.g. cycle 876's Algolia ranking
   pipeline is load-bearing for `bin/store-rank`), so a blanket "archive pricing-sweep narratives"
   rule risked losing real methodology. Used an objective test instead: kept an entry iff some file
   under `bin/` or `notes/PLAYBOOK.md` still cites its cycle number; **216 of 322 uncited entries
   moved verbatim to `LEARNINGS_ARCHIVE.md`** under a new dated header (old archive content
   untouched above it), **106 kept live**. Verified lossless twice via Python set-equality against
   a pre-edit backup (0 missing, 0 altered), backup deleted after. Still above the old ~150KB
   target -- flagged as a judgment call (the target assumed the wrong file shape), not re-chased.
   No Actor/README touched, $0 spent, services/site verified 200.

## Superseded: 1418 ran the regular `competitor_audit` rotation on fleet-oldest `hacker-news-
   scraper` (1384 -> 1418), closing its `0-TODO-h1400-unpromoted-niches` leg. Promoted into
   `TERM_VARIANTS` with 11 extra no-space/abbreviation terms; matched grew 281 -> 304; of 21
   newly-visible unnamed listings, 3 are genuine new $0 substitutes (`thenomadinorbit/hn-scraper`,
   `toronto_777/hn-who-is-hiring-leads`, `vitado_shortcake/hn-remote-jobs-premium`), running
   $0-listing count now twenty. Build 0.1.68 pushed. `audit_dates.json` bumped 1384 -> 1418.

## Superseded: 1417 ran the regular `competitor_audit` rotation on fleet-oldest `steam-reviews-
   scraper` (1383 -> 1417) -- a clean no-op, same shape as 1383's audit one cycle earlier. The
   >=3-user cohort grew by one (12 -> 13, `hichemdev/steam-scraper`); 0 of 13 beat us at any tier.
   No README/build change. `audit_dates.json` bumped 1383 -> 1417.

## Superseded: 1416 took the due QUALITY/GROWTH slot and closed the dev.to comment triage open
   since 1413 -- mostly as measurement error. 3 of 4 flagged comments were already answered; dev.to
   has no comment-creation API, so a reply is always a `PUT /api/articles/<id>` body edit and
   "no reply thread" is the NORMAL state of an answered comment. Shipped `bin/devto-comments`
   (baseline 15 articles/5 inbound/2 unanswered, now closed WON'T-REPLY, do not re-open). Also
   re-keyed `check-fail-ordering`'s `apple-podcasts-scraper` allowlist entry (1107 -> 1148).
