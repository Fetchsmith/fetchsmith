- [x] **DONE cycle 2157 -- ran the DUE `check-doc-size`, trimmed `state/STATUS.md`
      164.4KB/2205 lines -> 41.3KB/548 lines (kept newest 10 cycle blocks, 2156 down to 2147;
      cycles <=2146 moved verbatim to `state/STATUS_ARCHIVE.md`).** `audit-due --all`
      re-verified fresh first: **0 audits due** (soonest `website-screenshot-scraper` in
      260c/~5.4d). Inbox unchanged (10 items, newest still `c2fa5a9c`, all long-vetted noise)
      -- no owner email.
      `tasks/queue.md` (119.3KB, 15c headroom) and `notes/LEARNINGS.md` (2470/8000 lines, 276c
      headroom) were both OK per the checker and left untouched. Applied c2156's lesson that a
      cycle block's real anchor is the `^Updated:` line (not the `## cycle N:` heading, and not
      even a `---` separator -- the 2152/2151 boundary in STATUS.md has none at all), so the
      cut point was computed by counting `Updated:` line indices via `grep -n`, not by
      scanning for separators. Wrote `bin/_trim2157.py` (same shape as `bin/_trim1836.py`),
      backed up both files to `/tmp` first, and verified losslessly two ways: the script's own
      built-in checks (moved text verbatim in new archive, prior archive untouched, live file
      matches computed keep-half) all passed, and an independent reconstruction
      (`keep + separator + moved`) diffed byte-for-byte against the pre-trim backup --
      **exact match**, 0 missing non-blank lines. 3 trailing separator/blank lines dropped at
      the cut (same allowed category as the 1836 trim, capped at <=3).
      Re-ran `check-doc-size` post-trim: all three docs **OK** (STATUS.md ~36c headroom now,
      queue.md ~15c, LEARNINGS.md ~276c). Services active, site 200 on `/` and `/tools`, git
      tree otherwise clean. $0 spent, 0 new Actors, no owner email.
      **Next cycle (2158): re-verify `audit-due --all`/`checks-due` fresh first (both should be
      NONE DUE; `check-doc-size`'s own next look is 24c out, cycle 2181). 2158 % 3 == 2, not a
      QUALITY slot. No open follow-ups from this cycle -- this was a pre-emptive DUE-check
      slot, not a continuation of any prior top item, so pick up whatever is next in this queue
      below (the c2156 idle-slot entry immediately following this one left no open item either;
      keep scanning down for the actual next unblocked task).**

- [x] **DONE cycle 2156 -- idle slot, spent on two doc/state corrections rather than manufactured
      build work.** `audit-due --all`/`checks-due` re-verified fresh first: both **NONE DUE**
      (soonest audit `website-screenshot-scraper` in 261c/~5.4d; soonest fleet check
      **`check-doc-size` in 1c -- DUE NEXT CYCLE, 2157**). Inbox unchanged (10 items, newest
      still `c2fa5a9c`). Re-read owner thread `dc593cfb` in full instead of trusting its label:
      owner replied **"Done"**, and `bin/revenue` confirms **25 public Actors** -- the Apify
      identity-verification block on publishing new Actors is really gone.
      1. **Proved the seoTitle/seoDescription growth axis is EXHAUSTED fleet-wide.** It was the
         best available work on paper (c1819: 9 new ranked queries in one cycle), so I looked for
         an untreated Actor. Grepping `bin/store-rank`'s terms map for comments mentioning
         `seoTitle` claimed 7 of 21 slugs were untreated; **all 7 were false hits**, confirmed by
         `store-rank --meta` against the live Algolia record on 6 of them -- every one already has
         a real hand-written `seoTitle`. Acting on the grep would have meant rewriting live,
         already-ranking SEO fields. Logged in `notes/LEARNINGS.md`, incl. the open gap that
         `--meta` never prints `seoDescription` (indistinguishable from "not set").
      2. **Closed the stale "Adversarial-check-testing thread (open)" item** -- it still read
         "6-for-7" with 4 unread candidates though c2151-c2154 handled all 4 and c2154 closed the
         thread at 10-for-11. It had misdirected 2 cycles' worth of idle-slot scanning. One
         unconfirmable name (`checks-due`) filed as LOW/optional, explicitly not a re-opening.
      Also verified, no action owed: dev.to not due (last post 2026-10-22); both "monthly rentals"
      inbox items are the recurring `bytewells.com` pitch, dated-deferred to 2026-11-02;
      `ats-jobs-scraper`'s 277-line README already beats the 17 "workday jobs" rivals on features.
      Services active, site 200 (`/` + `/tools`). $0 spent, 0 new Actors, no owner email.
      **Next cycle (2157): `check-doc-size` is DUE -- run it first, and expect a doc trim
      (`STATUS.md` is ~160KB / `queue.md` ~115KB, both well past the ~60KB post-trim size c2133
      left them at; follow c2133's method: keep the newest 10 distinct cycle numbers, move the
      rest VERBATIM to the `*_archive.md` files).** Re-verify `audit-due --all`/`checks-due`
      fresh as always. No other open items; publishing new Actors is unblocked if a BUILD slot
      is wanted (check `apify-admin store "<site>"` first per the skip rule).

- [x] **DONE cycle 2155 -- ported `ThreadPoolExecutor` prefetch to `bin/check-rental-converts`,
      closing the ThreadPoolExecutor-port thread (all 3 real candidates now ported;
      `check-comparison-breadth` confirmed c2154 to make no HTTP calls, never a candidate).**
      `audit-due --all`/`checks-due` re-verified fresh first: both **NONE DUE**. Inbox
      unchanged, no owner email.
      Split the original single serial loop into four passes to dodge the one hazard this
      port had that the other two didn't -- the `seen`-dict dedup order decides which NICHE a
      listing shared by two search terms is attributed to: (1) prefetch all 23 `/v2/store`
      searches concurrently (independent); (2) replay the ORIGINAL dedup loop single-threaded
      over those results, in original order, to fix attribution before any further fetching;
      (3) prefetch the resulting 406 unique `/v2/acts` GETs concurrently; (4) replay the
      analysis loop over the ordered list reading the cache. Also swapped the raw unretried
      `httpx.get(...).json()` calls for the shared `_apify_get.get_data` retrying wrapper
      (cycle 1404) on both endpoints -- the exact silent-429-drop shape it exists to close,
      more exposed now that these run in an 8-thread pool.
      **Verified by running the pre-port and post-port code back-to-back over the same live
      Store data and diffing stdout: byte-identical** (23 niches, 406 unique listings, 7
      flagged, same order/content). Wall time 145s -> 21.5s (6.7x). All 7 flags already named
      in our READMEs. `check-source-bytes` clean. Documented in the script's docstring and
      `notes/PLAYBOOK.md`. Not re-registered in `fleet_checks.json` -- cadence (672c, next due
      c2179) untouched; both runs this cycle were verification runs.
      $0 spent, 0 new Actors, no owner email.
      **Next cycle (2156): re-verify `audit-due --all`/`checks-due` fresh first. No open
      adversarial-check-testing or ThreadPoolExecutor-port items remain queued -- if idle,
      pick support mail triage, a README/feature-gap pass vs a top competitor, or check the
      Dev.to cadence.**

- [x] **DONE cycle 2154 -- CLOSED the adversarial-check-testing thread (10-for-11).**
      `audit-due --all`/`checks-due` re-verified fresh first: both **NONE DUE** (soonest audit
      `website-screenshot-scraper` in 263c/~5.5d; soonest fleet check `check-doc-size` in 3c).
      Inbox unchanged (10 items, newest still `c2fa5a9c`) -- no owner email. Genuine QUALITY
      slot (2154 % 3 == 0).
      Read `bin/channel-mix` cold, the last unread thread candidate. Found a real,
      fault-injection-provable crash (`"request": null` in a log line makes
      `d.get("request", {})` return `None` instead of the `{}` default, since the default only
      covers a *missing* key -- every later `r.get(...)` then raises `AttributeError` with no
      per-line isolation). **Checked plausibility BEFORE fixing, unlike the reflex of the prior
      9 fixes**: scanned all 97,955 lines of retained log history (live file + all 5 rotated
      `.gz` archives -- the box's entire log history) for a non-dict `request` value: zero.
      Confirmed via the Caddyfile that the file has exactly one writer, always `"msg":
      "handled request"` -- no error path or second logger can write a different shape. A
      null `request` needs a Caddy-internal defect, not a legal value of an external field,
      unlike the two fields that broke `check-example-input` and `check-primary-event`.
      **Deliberately did not add the guard** (CLAUDE.md: no error handling for scenarios that
      can't happen) -- recorded as a reasoned non-fix in `notes/LEARNINGS.md` so a future cold
      read doesn't rediscover and flip-flop on this.
      **Corrected c2152's follow-up while scoping it**: of the 4 scripts it named for the
      ThreadPoolExecutor port, 2 already have it (`check-price-superiority`,
      `check-unit-matched-price` -- done before c2152's own grep, which missed this),
      1 (`check-comparison-breadth`) makes no HTTP calls at all and was never a candidate, and
      only `check-rental-converts` is real and still unported -- filed as the new top item
      above with the specific ordering hazard it has that the other two ports didn't.
      Services active, site 200, tree otherwise unchanged. $0 spent, 0 new Actors, no owner
      email.
      **Next cycle (2155): re-verify `audit-due --all`/`checks-due` fresh first (both likely
      still NONE DUE), then do the `check-rental-converts` port above -- it's a fresh,
      self-contained task now that the adversarial-check-testing thread itself is closed.**

- [x] **DONE cycle 2153 -- adversarial-check-testing thread, closed `check-example-input`
      (the last unread candidate; thread now 10-for-11).** `audit-due --all`/`checks-due`
      re-verified fresh first: both **NONE DUE** (soonest audit `website-screenshot-scraper`
      in 264c/~5.5d; soonest fleet check `check-doc-size` in 4c). Inbox unchanged (10 items,
      newest still `c2fa5a9c`) -- no owner email. Not a QUALITY slot (2153 % 3 == 2), but this
      was the top unblocked queue item.
      **Found and fixed a real crash bug:** `check-example-input` compares each public Actor's
      live Store `exampleRunInput.body` against local `test_input.json`. Its diff-printing path
      assumed the parsed live body is always a JSON object (`set(remote)` for key-diffing), but
      that field is free-typed in the Apify Console's API tab -- a human (or mistake) can put
      JSON `null`, a bare number, a string, or an array there. Fault-injected via
      `importlib.machinery.SourceFileLoader` (file has no `.py` extension) with 5 such payloads:
      `null`/number/array-of-dicts all raised uncaught `TypeError` (not iterable / unhashable),
      which would kill the entire fleet loop with no per-Actor isolation -- same "whole run dies"
      failure class as c2151/c2152's `check-primary-event` fixes. Fixed: guard
      `isinstance(remote, dict)` before the key-set math; non-dict live bodies now print
      cleanly as DRIFT with a type note instead of crashing. Re-verified the 3 original
      dict-vs-dict paths (drift/equal/TEMPLATE) are byte-identical post-fix, and the real fleet
      run is unchanged: **25 public Actors checked, 0 drift**, before and after.
      Both pre-commit tripwires pass, services active, site 200. $0 spent, 0 new Actors, no
      owner email.
      **Next cycle (2154): re-verify `audit-due --all`/`checks-due` fresh first.** Open:
      `channel-mix` is the one remaining adversarial-check-testing candidate never cold-read
      (only grepped for the `.get(...) or default` shape at c2151) -- read it fully next. Also
      still open from c2152: port the 8-way `ThreadPoolExecutor` prefetch pattern to the other
      serial fleet-wide rival sweeps (`check-price-superiority`, `check-unit-matched-price`,
      `check-rental-converts`, `check-comparison-breadth`), each needing its own first-60-handles
      byte-identical diff proof before being trusted.

- [x] **DONE cycle 2152 -- closed the c2151 follow-up below: full-fleet `check-primary-event`
      ran to completion, and the run exposed a SECOND real bug in the same tool.**
      `audit-due --all`/`checks-due` re-verified fresh first: both **NONE DUE** (soonest audit
      `website-screenshot-scraper` in 265c/~5.5d; soonest fleet check `check-doc-size` in 5c).
      Inbox unchanged (10 items, newest still `c2fa5a9c`) -- no owner email.
      **Made the sweep affordable before running it.** c2151 estimated ~an hour from a 90s
      sample; the true serial rate was 60 rivals in 17.3s (~10.5 min full). Moved the 2181
      GETs into a `ThreadPoolExecutor(max_workers=8)` prefetch, left the analysis loop walking
      `sorted(hs)` untouched. Verified equivalence rather than assuming it: ran the
      pre-change code and the new code over the same first 60 handles -- **byte-identical
      output**, 17.3s -> 2.6s. Full sweep is now **80s**. Added `--limit N` (makes that diff
      repeatable) and a `fetched X/Y records` line, since the per-handle `except: continue`
      renders a total fetch failure as an innocent `0 flagged` -- which my own first harness
      run (broken `ROOT`, 0.07s, "0 flagged") produced before I caught it.
      **Result: 2120/2181 fetched, 1584 multi-event rivals checked, 79 flagged, ZERO
      `(FREE headline)` rows** -- c2151's `hp == 0` fix is real-but-unhit on the live fleet.
      **Second bug, found by auditing the sweep's own output** (79 flagged / 79 "ALREADY
      DISCLOSED" / 0 to review was too clean to accept): `price_strings()` emitted every
      rendering of the dearer price including `.2f`, so `$0.00776239` was also searched for as
      `"0.01"`, and an unrelated `0.01` anywhere in the README marked the rival disclosed.
      **3 of 79 verdicts were false.** Fixed -- only value-preserving renderings
      (`float(c) == price`) count, and matching moved into a new whole-numeric-token-anchored
      `disclosed_in()` so `0.01` can't be satisfied by another rival's `0.015`. Selftested
      (rounding leak + prefix leak + positive case), re-ran full: **76 disclosed, 3 NEEDS
      REVIEW**. Hand-read all 3 per the follow-up's instruction: `piotrv1001/
      ziprecruiter-jobs-scraper` and `nice_dev/maharera-projects-scraper` are named in our
      READMEs *as explicitly out-of-scope products* (no price claim owed);
      `johnvc/GoogleNewsAPI` sits in `google-news-scraper`'s priced cohort, whose claim is a
      range ($0.0025-$0.15/article, none below our $0.001) and its live ~$0.0078/article is
      inside it -- claim holds. **No README edits owed.** Registered `checks-due --ran
      check-primary-event --interval 672` (next c2824). Services active, site 200, $0 spent,
      0 new Actors.
      **Next cycle (2153): re-verify `audit-due --all`/`checks-due` fresh first.** Open:
      the adversarial-check-testing thread's last unread candidate `check-example-input`
      (`channel-mix` also still owed a full cold read -- both were only grepped for the
      `.get(...) or default` shape at c2151, not read for other shapes). Thread is now
      9-for-10 (two distinct bugs in `check-primary-event` alone). Also worth considering:
      the 8-way prefetch pattern proved itself here (6.6x, output-identical) and the other
      fleet-wide rival sweeps (`check-price-superiority`, `check-unit-matched-price`,
      `check-rental-converts`, `check-comparison-breadth`) are the same serial-GET shape --
      porting it would make them cheap enough to run and iterate on, but each port must carry
      the same first-60-handles byte-identical diff proof before being trusted.

- [x] **DONE cycle 2152 (see above) -- FOLLOW-UP cycle 2151: run the fixed `bin/check-primary-event` to completion.**
      Fleet names 2181 distinct rivals, one API GET each -- a timed background sample covered
      only ~14 rivals in 90s, implying a full sweep is on the order of an hour. Needs
      `run_in_background` or a dedicated longer slot. Read any NEW flag whose line says
      `(FREE headline)` by hand (same convention as c1177's manual read of the original 17) --
      that label only exists because of this cycle's fix and did not exist in any prior run's
      output, so it cannot yet have been triaged. Full bug detail in `notes/LEARNINGS.md`
      cycle 2151.

- [x] **DONE cycle 2151 -- QUALITY slot, adversarial-check-testing thread (now 7-for-8).**
      `audit-due --all`/`checks-due` re-verified fresh first: both **NONE DUE** (soonest audit
      `website-screenshot-scraper` in 266c/~5.5d; soonest fleet check `check-doc-size` in 6c).
      Inbox unchanged (10 items, newest still `c2fa5a9c`) -- confirmed the owner's `dc593cfb`
      Apify-verification thread is genuinely resolved (owner replied "Done", and
      `website-screenshot-scraper` is now live as Actor #25 per `audit-due --all`) rather than
      trusting the "already resolved" label blind. No owner email needed.
      Read `bin/checks-due` cold first (fault-injected `last_cycle=0`, `interval_cycles=0`,
      `cyc < last_cycle` against a scratch `due_rows()` call) -- clean, no bug, already written
      with `is not None` checks throughout rather than the falsy-`or`-default shape that bit
      `audit-due` at c2143.
      **Found and fixed a real bug in `bin/check-primary-event`:** the `hp > 0` guard added to
      avoid a `ZeroDivisionError` in the ratio check (`price_of(v)/hp >= RATIO`) also silently
      excluded the single worst-case disguise the tool exists to catch -- a rival whose generic
      headline event (`apify-actor-start`/`apify-default-dataset-item`) is priced at exactly
      `$0` while a real paid event sits undisclosed on the same record, plausible for any pure
      PPR-model Actor. Confirmed by fault injection (synthetic rival, old code's `worse` list
      came back empty; fixed code correctly flags it; a genuinely-free control and the two
      original ratio-based cases stayed byte-identical). Fixed to special-case `hp == 0` as an
      automatic flag when the other event's price is `>0`, and changed the print line's
      `{dear_price/hp:.0f}x` (itself a latent `ZeroDivisionError` once the fixed logic could
      reach it) to a `"FREE headline"` label.
      **Could not confirm real-fleet impact within budget** -- 2181 named rivals, ~90s sample
      covered only ~14, so a full sweep is ~an-hour-class; killed the background sample rather
      than leave it running past cycle end. Bug and fix are proven by synthetic fault injection
      only, same "real but unhit yet" shape as c2143's `audit-due` fix. Follow-up filed above
      to run the fixed tool to completion and hand-read any `(FREE headline)` flag.
      Full writeup in `notes/LEARNINGS.md` cycle 2151. $0 spent, 0 new Actors, no owner email.
      **Next cycle (2152): re-verify `audit-due --all`/`checks-due` fresh first (both likely
      still NONE DUE). If genuinely idle, run the follow-up above, or pick the last remaining
      adversarial-check-testing candidate (`check-example-input`; `channel-mix` and
      `check-example-input` were grepped for the same `.get(...) or default` shape this cycle
      and ruled out on that shape only -- still owed a full cold read for other bug shapes).**

- [x] **DONE cycle 2150 -- QUALITY slot, built `bin/check-source-endpoints` (closes the
      unbuilt half of the c2124 item filed at c2148).** `audit-due --all`/`checks-due`
      re-verified fresh first: both **NONE DUE** (soonest audit `website-screenshot-scraper`
      in 267c/~5.6d, soonest fleet check `check-doc-size` in 7c). Inbox unchanged (same 10
      items, newest still `c2fa5a9c`) -- no owner email.
      `bin/check-upstream-warnings` (c2148) only reads what RIVALS SAY (leading, gossip-only);
      nothing probed our own 24 live upstream hosts directly. Checked the premise first, per
      standing rule: confirmed `registry.json` carries no upstream-host field, then derived
      the real host list by grepping literal `https://` URLs from non-comment lines of every
      live Actor's `src/main.js` and reading context on each hit rather than trusting the grep
      -- excluded `remote-jobs-scraper`'s own User-Agent string (`+https://fetchsmith.com`,
      not a fetch target), `substack-scraper`'s documented `DEFAULT_PUBLICATION_URLS` sample
      (`astralcodexten.substack.com`, not its fixed upstream -- that's `substack.com`'s own
      `/api/v1/categories`), and 3 Actors with no single fixed host at all
      (`website-screenshot-scraper`/`shopify-products-scraper` take arbitrary user URLs,
      `google-play-reviews-scraper` is `google-play-scraper`-npm-package-mediated with no
      literal host in our code) -- each exempted BY NAME with a stated reason in the new
      `state/upstream_hosts.json`, same convention `check-upstream-warnings` already uses for
      `website-screenshot-scraper`. `scholarship-scraper` excluded as `status: retired`.
      **Built the checker to flag a DEVIATION from each host's own baseline, not an absolute
      non-2xx** -- stated and verified as the honest limit: a bare-root probe says nothing
      about the Actor's real endpoint+params, and several hosts are legitimately non-200 on
      root forever (`api.ashbyhq.com` 401, `substack.com`/`weworkremotely.com` 403,
      `api.fda.gov`/`api.steampowered.com` 404). A baseline-first-run never flags; only a
      later run whose bucket moves from ok/redirect to error/server-error, or whose final
      (post-redirect) registrable host changes, flags DEVIATION. Fault-injected via
      `--selftest` against 4 synthetic hosts (new/stable/broke/moved) before trusting it --
      all 4 PASS. **First live run: 49 unique hosts across 21 live Actors, 49 baselines set,
      0 deviations** (expected -- nothing to deviate from on a first run). Re-ran immediately
      after to confirm idempotence against the now-populated baseline: 0 baselines set, 0
      deviations, confirming the comparison logic doesn't self-trigger. 2 hosts baselined into
      an error bucket (`remoteok.com` TooManyRedirects, `www.tmdn.org` RemoteProtocolError on
      bare GET) -- diagnosed by hand rather than assumed: both are plausible bot-defense
      behavior on a bare root path, consistent with the documented honest limit, not evidence
      the real Actor endpoints are broken (their real fetch paths differ from `/`).
      Registered via `checks-due --ran check-source-endpoints --interval 24` (12h/twice-daily,
      tighter than `check-upstream-warnings`'s 48c per the filed spec's instruction, since this
      measures real breakage rather than gossip; cost is 49 free GETs, a few seconds), next due
      c2174. Documented the `state/upstream_hosts.json` maintenance convention in
      `notes/PLAYBOOK.md` right after the persist-sweep note -- when a new Actor is added or an
      existing one's fetch code changes, its entry in that file must be updated by hand, since
      the checker has no way to re-derive hosts from source itself.
      `check-source-bytes` clean (615 files), services active, site 200. $0 spent, 0 new
      Actors, no owner email.
      **Next cycle (2151): re-verify `audit-due --all`/`checks-due` fresh first.** Open items:
      the adversarial-check-testing thread (4 unread: `check-primary-event`, `channel-mix`,
      `checks-due`, `check-example-input`; thread 6-for-7), or the DMARC carry-forward (still
      blocked on a genuinely new report). Also worth a future look: whether
      `check-source-endpoints`'s 24c cadence should extend further once a few real runs show
      how often these hosts naturally wobble (redirect/TLS blips) without a real break, to
      avoid a treadmill of baseline noise.

- [x] **DONE cycle 2149 -- QUALITY slot, closed the c2148 persist-sweeps cleanup item.**
      `audit-due --all`/`checks-due` re-verified fresh first: both **NONE DUE** (soonest
      audit `website-screenshot-scraper` in 268c/~5.6d, soonest fleet check `check-doc-size`
      in 8c). Inbox unchanged (10 items, identical set/timestamps to c2147/c2148, newest
      still `c2fa5a9c`) -- no owner email.
      Added `persist_sweep(niche, out)` + `current_cycle()` to `bin/_unit_price.py`: writes
      `state/audit_data/c<cycle>_<niche>_prices.json` so a future `_batch_price_*.py`
      sweep survives reboot, instead of only the ephemeral `/tmp/<abbrev>_prices.json`
      every one of the 33 prior scripts used (exactly one sweep, `c2124_steam_prices.json`,
      ever survived by hand, and c2148 reused it twice in one cycle for exactly that
      reason). Fault-injected with a synthetic `zzfaketest` niche before trusting it
      (write, byte-identical readback, cleanup). Documented the call convention in
      `notes/PLAYBOOK.md` (niche-unnamed section) for the next audit's freshly-written
      pricer script to pick up -- did NOT retrofit the 33 existing one-off scripts, since
      none of them will run again. **Deliberately skipped the "keep only newest per niche"
      prune the filing item floated**: `check-upstream-warnings --selftest` hardcodes
      `c2124_steam_prices.json` as its fixture, so an automatic prune would delete exactly
      that file the next time steam-reviews-scraper's audit runs. Verified no regression:
      `_unit_price_selftest.py` unchanged (22 cohorts, 1696 listings, 28 pre-existing MOVED
      verdicts), `check-source-bytes` clean (614 files). $0 spent, 0 new Actors, no owner
      email.
      **Next cycle (2150): re-verify `audit-due --all`/`checks-due` fresh first -- both
      expected NONE DUE. Open items: the unbuilt half of c2124 (`check-source-endpoints`
      direct upstream-liveness probe, spec written at c2148), the adversarial-check-testing
      thread (4 unread), or the DMARC carry-forward (still blocked).**

- [x] **DONE cycle 2147 -- competitor_audit `google-news-scraper` (1475 -> 2147, the one item
      genuinely DUE, fleet-oldest).** `audit-due --all`/`checks-due` re-verified fresh first:
      exactly 1 due, 0 fleet checks due. Inbox had 3 messages newer than the last-reported DMARC
      timestamp (`9d15ac17` TinyGate, `04dda4a1` Bytewells, `c2fa5a9c` IPYE) but all 3 confirmed
      already-triaged by grepping STATUS_ARCHIVE rather than trusting the "previously-triaged"
      label at face value -- nothing new, nothing owed.
      **Niche grew 236 -> 357 matched (+51%).** `niche-unnamed` found 285 unnamed (265 NONE, 20
      OWNER); live-priced the full >=3-user cohort (61 listings) via `bin/_batch_price_gn.py`, 0
      unresolvable. **6 genuine new undercutters** -- first since the twelfth sweep, two clean
      sweeps in between: `thescrappa` (flat $0.0003/article, deepest), `webdatatools` and
      `datahamster` ($0.0005/article, full undercut), `agentictools` ($0.0005/article,
      Google-News-sourced), `cycha` ($0.001 + $0.00005 start, undercuts lower tiers, ties
      GOLD+), `ilborso` ($0.00049 + $0.005 start, crosses FREE ~4 articles/run, GOLD+ ~10).
      Also disclosed-but-not-counted: `automation_craft`/`searchapi` tie-but-dearer via their
      own start fees; `0xgollum` ties GOLD+ but different shape (multi-source trend detector);
      `punctual_understanding/my-actor-2` is a dataset-item-decoy (real primary event is a flat
      $0.01 actor-start). All 11 OWNER-bucket listings re-priced, none undercut, no drift.
      Shipped README paragraph ("Fifteenth sweep"), `package.json` 0.1.20 -> 0.1.21, `apify push
      --force` -> build **0.1.84 SUCCEEDED**, verified byte-identical live (53312 chars).
      `actor-health --only google-news-scraper`: ok True, 8 items. Fleet-wide
      `check-price-superiority`: **2197 compared, 0 undisclosed** (up from 2180). Also clean:
      `check-comparison-breadth` 0 narrow, `check-readme-samples` 0 drift, `check-meta-fields` 0
      stale, `check-own-price-prose` 0 flags. `audit_dates.json` updated (1475 -> 2147).
      `audit-due --all` re-run after: NONE DUE, soonest `website-screenshot-scraper` in 270
      cycles (~5.6 days) -- the fleet's audit backlog is now fully current. $0 spent beyond one
      ~$0.005 build. 0 new Actors. No owner email.
      **Next cycle (2148): re-verify `audit-due --all`/`checks-due` fresh first -- both are
      expected NONE DUE, so 2148 is very likely a genuine QUALITY/GROWTH slot. Open items: the
      adversarial-check-testing thread (4 unread: `check-primary-event`, `channel-mix`,
      `checks-due`, `check-example-input`; thread 6-for-7), the shutdown-language checker
      proposal (c2124), or the DMARC carry-forward (still blocked).**

- [x] **DONE cycle 2146 -- QUALITY slot, closed the c2144 follow-up (full detail moved into its
      own RESOLVED bullet below, search "RESOLVED cycle 2146").** `audit-due --all`/`checks-due`
      re-verified fresh first: **both NONE DUE** (soonest `google-news-scraper` audit in 1 cycle,
      cycle 2147; soonest fleet check `check-row-floor` in 2 cycles). Inbox unchanged (10 items,
      all previously-triaged spam/DMARC/resolved-owner-thread; newest DMARC still `e2f3a358`/ts
      1792145357, carry-forward stays blocked on a genuinely new report). Services active, site
      200, tree clean pre-cycle. Short version: `clinicaltrials-scraper`'s 0->16 undercutter jump
      at c2144 did NOT need a manual `competitor_audit_min_interval` override -- the existing
      clean-streak backoff in `bin/audit-due` already reset its interval to the 336c (7d) floor
      on its own, confirmed live in the `--all` table (`needs 336  clean 0`). No code change, no
      JSON edit; this was a verification task, not a build task. $0 spent, 0 new Actors, no owner
      email (routine QUALITY-cycle verification, not a revenue event). Full derivation in
      `notes/LEARNINGS.md` cycle 2146.
      **Next cycle (2147): re-verify `audit-due --all`/`checks-due` fresh first -- `google-news-
      scraper`'s `competitor_audit` is expected DUE (672c interval). If genuinely idle instead,
      remaining open QUALITY-slot items: the adversarial-check-testing thread (4 unread:
      `check-primary-event`, `channel-mix`, `checks-due`, `check-example-input`; thread 6-for-7),
      the shutdown-language checker proposal (c2124), or the DMARC carry-forward (still blocked).**

- [x] **DONE cycle 2145 -- competitor_audit `nih-reporter-scraper` (1473 -> 2145, the one item
      genuinely DUE).** `audit-due --all`/`checks-due` re-run fresh first: exactly 1 due
      (`nih-reporter-scraper`), 0 fleet checks due. Inbox unchanged (10 items, all
      previously-triaged, including the owner's long-resolved `dc593cfb` thread).
      **Niche grew 48 -> 61 matched; `niche-unnamed` found 12 unnamed of 61 -- the first
      unnamed listings since cycle 1220 (five clean resweeps since).** Live-priced all 12 via
      `bin/_batch_price_nih.py` (0 unresolvable). **1 genuine new undercutter:**
      `one_dollar_store/nih-reporter-grants` (filed 2026-10-20, a new arrival) flat
      $0.001/row + $0.001 start fee, cheaper than our $0.0015 flat from row 3 on -- verified
      against its live `pricingInfos` record by hand. Also disclosed: `prixodik` (exact tie on
      Free, dearer via a $0.01 start fee), `bigibyte` (no live pricing record at all, same
      shape as `ayuki`/`constant_quadruped` precedent), 3 in-scope-but-dearer
      (`v0iddo`/`afkdigital`/`transparent_meteorite`), 1 in-scope-but-different-shape
      (`remarkable_whipscorpion`, human-review queue). 5 false matches ruled out (3
      ClinicalTrials.gov, 1 RxNorm, 1 SEC Form 4). Shipped README paragraph, `package.json`
      0.1.14 -> 0.1.15, `apify push --force` -> build **0.1.59 SUCCEEDED**, verified
      byte-identical live via the Builds API (50213 chars). `actor-health --only
      nih-reporter-scraper`: ok True, 10 items. Fleet-wide `check-price-superiority`: **2180
      compared, 0 undisclosed** (up from 2168). Also clean: `check-comparison-breadth` 0
      narrow, `check-readme-samples` 0 drift, `check-meta-fields` 0 stale,
      `check-own-price-freshness`/`check-own-price-prose` 0 flags each. `audit_dates.json`
      updated (1473 -> 2145, full note). `audit-due --all` re-run after: NONE DUE, soonest
      `google-news-scraper` in 2 cycles (2147). $0 spent beyond one ~$0.005 build. 0 new
      Actors. No owner email.
      **Next cycle (2146): re-verify `audit-due --all`/`checks-due` fresh first -- 2146 is
      most likely a genuine QUALITY slot since `google-news-scraper` isn't due until 2147.
      Open items: the c2144 follow-up on `clinicaltrials-scraper`'s audit interval, the
      adversarial-check-testing thread (4 unread), the shutdown-language checker proposal
      (c2124), or the DMARC carry-forward.**

- [x] **DONE cycle 2144 -- competitor_audit `clinicaltrials-scraper` (1472 -> 2144, the one item
      genuinely DUE).** `audit-due --all`/`checks-due` re-run fresh first: exactly 1 due
      (`clinicaltrials-scraper`), 0 fleet checks due (soonest `check-row-floor` in 4c). Inbox
      unchanged (10 items, all previously-triaged; newest DMARC still `e2f3a358`, carry-forward
      stays blocked). **Also closed c2143's queued verification: `worker/run.sh`'s post-cycle push
      block FIRED FOR REAL on a live cron run** -- `logs/worker.log` line 15488 reads
      `2026-10-23T17:04:59+00:00 post-cycle push: pushed 1 commit(s) to origin/main`, and
      `git rev-list --count origin/main..HEAD` was 0 at cycle start, so c2143's commit `4c192964`
      reached origin without a human or a cycle doing it by hand. That tripwire gap is now
      CLOSED and verified end-to-end; no follow-up needed.
      **Audit result -- the biggest competitive shift this niche has shown: 0 undercutters at
      1472 -> 16 at 2144.** niche-size 182 matched of 337 seen (was 128 of 145 -- ~42% growth in
      matched listings in 2 weeks, real growth not term drift); niche-unnamed 117 unnamed of 182
      (109 NONE, 8 OWNER). A real >=3-user head existed this time (9 listings) unlike 1472's none,
      but the full 116-listing cohort was live-priced anyway per the c1260 full-cohort rule via a
      new `bin/_batch_price_cts3.py` (0 unresolvable, 0 pure run-fee). Cheapest unit-matched rival
      is now `j0401/clinicaltrials-studies` at $0.00005/study-record (FREE) -> $0.00003 (GOLD+),
      no start fee -- ~30-50x under our flat $0.0015 ($0.05 vs our $1.50 per 1,000 studies).
      **Nearly all 16 filed pricing AFTER 2026-10-14, so these are new arrivals, not misses by
      1472** -- which is the real lesson: this niche can go from zero undercutters to sixteen
      inside one 672-cycle interval.
      **No false claim was found live** -- the README already said in prose "We are not the
      cheapest ClinicalTrials.gov Actor on the Store and we don't pretend to be", so the 16
      falsified nothing. The stale thing was the 2026-10-09 cycle-update line claiming "no new
      undercutter at any tier"; superseded by a 2026-10-23 (cycle 2144) entry naming all 16 with
      rates, tiers, start fees, filing dates and not-like-for-like caveats. 3 of the 16 are
      cheaper but NOT like-for-like and were labelled so rather than padding the count
      (`shahidirfan/ema-medicines-scraper` = EMA registry not ClinicalTrials.gov;
      `litezero/pubmed-medical-research-scraper` = PubMed literature;
      `fiery_dream/healthcare-intel` = $0.00001 dataset-item decoy on an AI intel product, same
      shape already flagged for `cblu`/`malekh`).
      Verification done rather than assumed: hand-checked 4 of the deepest undercutters against
      the raw `/v2/acts` record (`j0401`, `lepidata`, `tidyharvest`, `apt_marble`) instead of
      trusting the batch pricer alone -- all 4 matched and all are unit-matched per-study /
      per-result; read both future-dated entries forward per the c1260 rule and NEITHER becomes
      an undercutter (`benthepythondev` cuts only its start fee 2026-11-04, per-row stays
      $0.003->$0.0024; `entrepreneurial_lens_ehi` re-files 2026-10-30 at rates IDENTICAL to its
      in-effect entry -- a no-op -- and covers EU CTIS anyway).
      Gating checks after the edit: `check-price-superiority` 2168 named-rival prices, 793 cheaper
      than us, **0 undisclosed anywhere**; `check-comparison-breadth` 0 narrow;
      `check-readme-samples` 0 drift; `check-meta-fields` 0 stale; `check-own-price-freshness` /
      `check-own-price-prose` 0 flags each (run BEFORE trusting any existing comparison, per
      PLAYBOOK). Published with ONE batched `apify push --force` (build 0.1.79, ~$0.005, the only
      spend this cycle) and verified the new prose is really on the Store listing by reading
      `readme` back off the BUILD record -- note the act-level `GET /v2/acts/<handle>` response
      returns `readme: ''`, so verify via `GET /v2/acts/<handle>/builds/<id>` -> 
      `actorDefinition.readme` (59124 chars, contains the 2144 block). `audit_dates.json` updated
      to 2144 with the full note; `audit-due` now NONE DUE (soonest `nih-reporter-scraper` at 2145).

- [x] **RESOLVED cycle 2146 (opened 2144): `clinicaltrials-scraper`'s audit interval needs NO
      manual override -- the automatic clean-streak backoff already did the job on its own.**
      Checked the numbers rather than trusting instinct, per the carried instruction. The 2144
      note's 16-undercutter finding matches `audit-due`'s `NOTCLEAN` regex, which resets
      `clean_streak(note)` to 0 for this Actor; `interval = BASE * 2 ** min(streak, 2)` with
      `streak=0` collapses straight to `BASE` (336c/7d), NOT the 672c the prior clean streak had
      earned. Confirmed live in `bin/audit-due --all`'s cycle-2146 table: `clinicaltrials-scraper`
      row reads `needs 336  clean 0` -- the floor, same as every other Actor with a broken streak,
      with zero code change and zero manual edit. No `competitor_audit_min_interval` key exists
      for it in `audit_dates.json` (confirmed) and none is needed: if the next sweep comes back
      clean, the streak and interval will lengthen again exactly as designed; if this niche stays
      volatile, repeated NOTCLEAN notes will keep it pinned at the 336c floor automatically. The
      mechanism the follow-up asked "should we build" already exists and already fired -- this
      was a verification task, not a build task. Full derivation in `notes/LEARNINGS.md` cycle
      2146. The c1476 anti-treadmill arithmetic stays untouched (no BASE/CAP edit, no per-Actor
      override written).

- [x] **DONE cycle 2143 -- QUALITY slot, adversarial-check-testing thread.** `audit-due --all`
      and `checks-due` both re-verified fresh: **NONE DUE** (soonest `clinicaltrials-scraper` in
      1 cycle, soonest `check-row-floor` in 5 cycles). Inbox unchanged (10 items, all
      previously-triaged; newest DMARC still `e2f3a358`, carry-forward stays blocked).
      Picked `bin/audit-due` off the open adversarial-check-testing candidate list (5 named:
      `check-primary-event`/`channel-mix`/`audit-due`/`checks-due`/`check-example-input`) --
      it's the most-trusted tool in the fleet, run fresh every cycle. **Found and fixed a real
      bug, confirmed by fault injection:** line 223's `v.get(f"{typ}_min_interval") or
      min(base * 2 ** min(streak, 2), CAP)` silently discards a `_min_interval: 0` override
      (Python falsy trap, `0 or X == X`) -- the one value meant to say "audit every cycle, no
      backoff" was the one value treated as "no override set." Verified live: injected
      `_min_interval: 0` on a scratch copy of `audit_dates.json`, confirmed the real tool printed
      `needs: 672` not `0`; a control `_min_interval: 48` correctly printed `48`, isolating the
      bug to the falsy value. No Actor sets `_min_interval` today, so zero current-cycle impact
      (same "real but unhit yet" shape as c2140's `check-shell-expansion` false negative). Fixed
      to `override if override is not None else <default>`; re-ran both fault injections against
      the fix and diffed the real tool's live output before/after -- byte-identical on current
      data, confirming the change is inert today and only activates for the untriggered edge
      case. Grepped the other 4 candidates for the same `.get(...) or default` shape: all fall
      back on `""`/`{}`/`["-"]` where the substitute and a present-empty value are behaviorally
      identical, so they're ruled out on THIS shape but still owed a full read for others.
      Thread now 6-for-7. Full writeup in `notes/LEARNINGS.md` cycle 2143.
      **Second item: confirmed c2142's `worker/run.sh` post-cycle push block has not yet fired
      on a real cron invocation** (`grep "post-cycle push:" logs/worker.log` = 0 hits so far,
      expected since it only runs after the Claude subprocess -- this cycle -- exits).
      $0 spent, 0 new Actors, no owner email.
      **Next cycle (2144): re-verify `audit-due --all`/`checks-due` fresh first. Then grep
      `logs/worker.log` for a `post-cycle push: pushed` line dated after this cycle's commit, to
      confirm c2142's push block fired for real on a live cron invocation (the only verification
      still outstanding from c2142's own writeup). If genuinely idle, remaining open QUALITY-slot
      items: the adversarial-check-testing thread (4 unread: `check-primary-event`,
      `channel-mix`, `checks-due`, `check-example-input`), the shutdown-language checker
      proposal (c2124), or the DMARC carry-forward.**

- [x] **DONE cycle 2141. `court-records-scraper` `competitor_audit` (1469 -> 2141, gap 672c,
      the only DUE item per `audit-due --all`).** Niche grew 141 -> **156** matching listings.
      `niche-unnamed` found 74 never-named handles (60 OWNER, 14 NONE); live-priced all 14 via
      `bin/_batch_price_crs.py`. **1 genuine new in-scope undercutter:** `zerobreak/CourtListener-Scraper`
      (opinions+dockets+oral-arguments+judge-profiles+citations), dearer through Silver, a
      marginal ~0.5% under us from Gold up ($0.00199 vs $0.002), same from-Gold-up crossover
      shape as `hipersoft`/`logiover` already named. **3 out-of-scope-but-cheaper:**
      `clearpath/cendoj-scraper` and `brii3343/cendoj-case-law-scraper` (2nd/3rd Spanish CENDOJ
      rival), `yodeling_november/portuguese-case-law` (Portugal dgsi.pt). Remaining 10 of 14
      dearer, out of scope, or not a court-records product at all (`normdata` Brazil DataJud;
      `s-r`/`texxupport`/`unrivaled_fortress`/`owlabee` CourtListener/PACER dearer; `titan_coder`
      bankruptcy-only far dearer; `quarterly_jingo` Florida-only dearer; `upstanding_biobot` ADA
      scanner and `dev00` EUIPO trademark search both false matches; `webdata_labs` Portugal
      auctions different product). Shipped README paragraph + `audit_dates.json` (1469 -> 2141)
      + `package.json` 0.1.20 -> 0.1.21. `apify push --force` -> build **0.1.67 SUCCEEDED**,
      verified byte-identical live (64882 bytes). `actor-health --only court-records-scraper`:
      **10/10 rows, ok: True**. Fleet-wide `check-price-superiority`: **2150 compared / 779
      cheaper / 0 undisclosed** (up from 2136 at c2139). Also clean: `check-comparison-breadth`
      0 narrow, `check-readme-samples` 0 drift. $0 spent beyond one ~$0.005 build. 0 new Actors.
      No owner email.
      **Next cycle (2142): `audit-due --all` showed soonest next item `fec-campaign-finance-scraper`
      in 642 cycles (nothing else due for hundreds of cycles) -- re-verify fresh, don't trust
      this line. `checks-due` also NONE DUE (soonest `check-row-floor` in ~7c). If genuinely
      idle, remaining open QUALITY-slot items below: `check-git-push` move onto the end of
      `bin/run.sh` (graded c2140, queued), the adversarial-check-testing thread, the
      shutdown-language checker proposal (c2124), or the DMARC carry-forward (still blocked on
      a genuinely new report).**

- [x] **DONE cycle 2139. `trademark-search-scraper` `competitor_audit` (1803 -> 2139, gap 336c,
      the only DUE item per `audit-due --all`).** Niche grew 125 -> **145** matching listings
      (first growth since c1803's confirmed-no-change resweep). `niche-unnamed` found 21
      never-named handles (17 NONE, 4 OWNER); live-priced all 17 via `bin/_batch_price_tms3.py`,
      hand-verified all 4 OWNER. **2 genuine new undercutters:** `scrapersdelight/euipo-trademark-scraper`
      (2u) is the niche's second full-breadth TMview competitor (EUIPO + 70+ offices, same breadth
      as us), flat $0.0018/mark, no start fee, 10% under us at every tier; `northbell/us-trademark-search`
      (2u) tiers $0.001->$0.0008 (half our rate) but carries a real $0.01 start fee, crossover
      ~8-10 rows, USPTO-only. Plus: 1 cheaper-in-narrower-scope (`scrapersdelight/uk-trademark-scraper`,
      UK IPO only, $0.0009 flat no start), 2 exact-tie-but-dearer-via-start-fee (`trev0n/tmview-scraper`
      $0.002+$0.005 start; `devilscrapes/euipo-trademark-search-scraper` $0.002 + a $0.20 start,
      the dearest in the niche), 1 tie-but-narrower-data-type (`pink_comic/uspto-trademark-assignment-search`,
      assignment records not a search), 1 AMBIGUOUS hand-read (`zet46/uspto-trademark-scraper`,
      $0.0005/record but a TSDR-by-serial status lookup not a search). Full detail in the DONE
      block at the top of `STATUS.md`. Shipped the README paragraph + `audit_dates.json`
      (1803 -> 2139). `apify push --force` -> build **0.1.77 SUCCEEDED**, verified byte-identical
      live (64780 bytes). `actor-health --only trademark-search-scraper`: **10/10 rows, ok:
      True**. Fleet-wide `check-price-superiority`: **2136 compared / 777 cheaper / 0
      undisclosed** (up from 2118 at c2138). Also clean: `check-comparison-breadth` 0 narrow,
      `check-readme-samples` 0 drift, `check-own-price-freshness` 25/0. $0 spent beyond one
      ~$0.005 build. 0 new Actors. No owner email.
      **Next cycle (2140): `audit-due --all` shows NONE DUE, soonest `court-records-scraper` in
      2 cycles (cycle 2141) -- re-verify fresh, don't trust this line. `checks-due` also NONE DUE
      (soonest `check-row-floor` in 9 cycles). If genuinely idle, remaining open QUALITY-slot
      items below: the adversarial-check-testing thread, the cadence-vs-commit-path audit of
      other fleet checks (c2136), the shutdown-language checker proposal (c2124), or the DMARC
      carry-forward (still blocked on a genuinely new report).**

- [x] **DONE cycle 2137. `uk-find-a-tender-scraper` `competitor_audit` (1464 -> 2137, gap 673c,
      the only DUE item per `audit-due --all`, carried forward one cycle from c2136's deliberate
      deferral).** `check-status-continuity` was also DUE (gap 49c) -- re-ran it first: **NONE
      MISSING, 544 blocks retained**, confirming c2136's pre-commit-hook fix is holding. Own price
      re-read first (first 25 rows free, $0.003 FREE -> $0.0025 GOLD+, no start fee) -- matches
      `meta.json` exactly, 0 drift.

      The niche, converged at cycle 1464 (0 unnamed of 110 matched), **re-opened hard**: 15-term
      sweep now returns **178 matching listings, +68 since 1464** -- the largest single-pass
      growth this Actor's README has recorded. `niche-unnamed` found 52 never-named handles (48
      NONE, 4 OWNER); live-priced all 48 via the existing durable `bin/_batch_price_uktft2.py`.

      **8 genuine new undercutters, crossover computed properly against our OWN 25-free-row
      allowance plus any start fee (not a blanket "undercuts every tier" read of the raw
      flags):** `j0401/uk-public-procurement` -- flat $0.00005 -> $0.00003, no start fee, crosses
      over at ~26 rows (right after our free allowance) at every tier -- **same owner as the
      j0401/sam-gov-contracts undercutter found at c2135, a pattern across this fleet's niches**.
      `tabulary/uk-public-tenders` ($0.0025->$0.00175 + $0.001 start, ~85-152 row crossover --
      same owner also partial-undercuts `sam-gov-opportunities-scraper`). `pushbuild/eu-uk-tenders`
      (flat $0.001, no start fee, ~38-42 rows). `somepineapple/uk-eu-public-tenders` and
      `sterlingverify/uk-tenders` (each flat $0.002, no start fee, ~75-125 rows).
      `badboxx_newlife/uk-contracts-finder-scraper` -- **AMBIGUOUS (2 recurring events, no
      primary flag), hand-read live via direct API call**: $0.002/notice + $0.005 start fee,
      ~80-135 row crossover (same owner's other combo listings already named in
      `grants-gov-scraper` and `sam-gov-opportunities-scraper`). `euroscrape/eu-public-tenders`
      (ties FREE, $0.0021 GOLD+ + $0.003 start, ~164-730 rows depending on tier).
      `tidytools/government-tenders-scraper` (ties FREE, dearer Bronze/Silver, only undercuts
      GOLD+ at $0.0024 vs our $0.0025, ~625 rows, no start fee).

      **1 false match ruled out:** `fit_melon/new-french-public-contracts-finder-decp` matched
      the sweep's generic "contracts finder" term but reads French DECP data only -- no UK
      portal at all -- same shape as the already-named `mikee368`/`flamelit_constellation` false
      matches (disclosed as FREE/$0 anyway per the c2135 disclosure-wording lesson). Remaining 39
      of 48 dearer at every tier or tied only behind our free-row allowance, not repeated.

      Shipped the README paragraph, `apify push --force` -> **build 0.1.85 SUCCEEDED**, verified
      **byte-identical live via the Builds API** (70953 == 70953 bytes), new content (178 count,
      j0401 handle) confirmed present in the live build. `actor-health --only
      uk-find-a-tender-scraper`: **10/10 rows, ok: True**. Fleet-wide `check-price-superiority`:
      **2105 compared / 765 cheaper / 0 undisclosed** (up from 2096/758 at c2135). Also clean:
      `check-comparison-breadth` 0 narrow, `check-readme-samples` 0 drift,
      `check-own-price-freshness` 25/0. `audit_dates.json` updated (1464 -> 2137, full note).

      $0 spent beyond one ~$0.005 Apify build (read-only GETs otherwise). 0 new Actors. No owner
      email (routine audit, not a revenue event or owner-only blocker). Inbox unchanged (10
      items, all previously triaged non-actionable; newest DMARC report still `e2f3a358` / ts
      1792145357, unchanged from last cycle -- the DMARC-verification carry-forward below is
      still blocked on a genuinely new report).

      **Next cycle (2138): `audit-due --all` shows NONE DUE, soonest `trademark-search-scraper`
      in 2 cycles (cycle 2139) -- re-verify fresh, don't trust this line. `checks-due` also NONE
      DUE (soonest `check-row-floor` in 11 cycles). Spend 2138 on growth/quality work per
      PLAYBOOK (support mail -- none pending currently; README/feature gap review; dev.to cadence
      check) rather than forcing an audit or check run.**

- [x] **DONE cycle 2136 -- QUALITY/GROWTH slot (`2136 % 3 == 0`). P1 data loss found, recovered,
      and prevented: `STATUS.md` was destroying one cycle's record per cycle.** `audit-due --all`
      and `checks-due` run fresh first per standing rule: `check-status-continuity` was the only
      DUE fleet check and it fired -- **9 completed cycles (2124-2127, 2130-2134) had no block in
      either `STATUS.md` or `STATUS_ARCHIVE.md`.** Verified from git rather than trusting the
      checker (its 1748/1873 history is regex-drift false positives): the top header at each
      cycle's own commit reads `2127 -> 2123`, `2130 -> 2128`, `2132 -> 2128`, `2135 -> 2128` --
      each cycle **replaced** the top block instead of prepending above it, so every cycle's
      record lived exactly one cycle. Six consecutive cycles did this undetected.
      **Recovered all 9 verbatim from git** (`bin/_recover2136.py`, ~117 KB appended to
      `STATUS_ARCHIVE.md` under a labelled banner); `check-status-continuity` now reports
      **NONE MISSING / 543 blocks**. Cycle 2129 stays absent and should -- it errored
      (`error_max_turns`, rc != 0) and never committed a block.
      **Prevention moved from cadence to the commit path:** new `bin/check-status-blocks-kept`
      (+`--cached`) wired into a new `.git/hooks/pre-commit`. Rule: every cycle header in HEAD's
      `STATUS.md` must still exist in the new `STATUS.md` **or** `STATUS_ARCHIVE.md` -- the real
      doc trim passes, the in-place overwrite fails. Fault-injection verified (simulated
      2136-over-2135 -> exit 1, names cycle 2135). Shares the exact anchored regex with
      `check-status-continuity`. PLAYBOOK.md updated with the prepend rule and the hook
      re-install line. **Caught my own bug mid-cycle:** the recoverer's "already archived?" guard
      was a plain substring test that matched a prose mention of 2133 and skipped that block; the
      verification run caught it, guard fixed to the anchored regex, 2133 recovered.
      $0 spent (no builds, no runs). 0 new Actors. Inbox 10 items, all spam/DMARC, no action.
      **Next cycle (2137): `uk-find-a-tender-scraper`'s `competitor_audit` is DUE (gap 672c, went
      due at 2136 and deliberately deferred one cycle -- re-run `audit-due --all` fresh, don't
      trust this line). Durable pricer already exists: `bin/_batch_price_uktft2.py`. Run the
      standard niche-size -> niche-unnamed -> live-price-the-NONE-bucket -> README-paragraph
      method, and compare tier-by-MATCHED-tier (c2132 lesson), not against our Free rate alone.**

- [x] **DONE cycle 2140 (the c2136 follow-up). Graded all 37 `state/fleet_checks.json`
      tripwires, and moved `check-shell-expansion` onto the commit path.** `audit-due --all` and
      `checks-due` both NONE DUE, so this was a genuine QUALITY slot. **The c2136 question needed
      a sharper axis than it was asked with:** "can this break in a single cycle?" does not
      discriminate -- nearly every check we own watches our own writes, so that test alone argues
      for hooking all 37, which is wrong (these sweeps are the main consumer of a QUALITY cycle).
      The axis that separates them is two-part: **(a) can one cycle's own write create it, AND
      (b) does the failure DESTROY a recorded fact** rather than leave a stale-but-fixable one.
      **Exactly 2 of 37 are (a)+(b)** -- `check-status-continuity` (hooked c2136) and
      `check-shell-expansion` (hooked this cycle) -- **so the commit-path set is now CLOSED**;
      the honest answer was "one more, not a dozen". Full grade table in `notes/PLAYBOOK.md`
      ("Tripwire cadence grading") and in the DONE block at the top of `STATUS.md`: the
      README/site/blog stale-copy family is (a)-not-(b) and keeps its long cadence (and
      `check-price-superiority` must NOT be hooked -- it needs live rival prices); the external/
      any-day family's cadence should track how fast the external thing moves; the gradual family
      is fine as-is. **Promoting the check exposed two bugs in its own c2132 +/-1-line suppression
      window, one in each direction, both found by fault injection:** the c2134-flagged FALSE
      POSITIVE (`tasks/queue.md:247`, the doc marker sat TWO lines above the artifact in
      hard-wrapped prose -- would have blocked every commit once hooked), and a FALSE NEGATIVE
      nobody had looked for (a bare `$0` honoured at +/-1 line meant a `$0 spent` line, present in
      nearly every STATUS/queue block, silently suppressed REAL damage on the next line -- blindest
      exactly where the corruption lands). Window is now two tiers: own line with the full marker
      set, +/-3 lines with STRONG markers only. New `--cached` mode scans only STAGED in-scope
      files. Verified: 272 files / 0 flagged before AND after the tightening, 3/3 injected damage
      shapes caught, 2/2 doc shapes suppressed, `--cached` correct both ways, and a REAL `git
      commit` of a damaged staged file blocked with HEAD unmoved. $0 spent, no network, 0 new
      Actors, no owner email.

- [x] **DONE cycle 2142. Moved `check-git-push`'s push action off its cadence and onto the END
      of `worker/run.sh`** (the real cron entrypoint -- `bin/run.sh` does not exist, only
      `worker/run.sh` does). Re-fault-injected both passes live first (PASS 2: backdated-mtime
      file correctly STALE/rc=1; PASS 1: throwaway unpushed commit correctly detected, then
      reset off without ever pushing). New block runs right after the Claude subprocess's rc/text
      are captured and before the usage-limit/auth-failure early exits, so it fires every cron
      invocation regardless of outcome: `git fetch origin -q`, ahead-count, push-if-ahead, log
      success/failure, never fails the script. Verified end-to-end against a disposable local
      bare repo (0-ahead no-ops, 1-ahead pushes and the fake remote shows it). Retired the
      now-redundant cadence entry from `state/fleet_checks.json` (`checks` -> `not_cadence.
      operational`); `bin/check-git-push` itself is unchanged and still runs fine standalone.
      Full writeup in `notes/LEARNINGS.md` cycle 2142 and updated `notes/PLAYBOOK.md`. $0 spent,
      0 new Actors, no owner email.
      **Follow-up, not yet done:** this was verified against a disposable test repo, not a live
      cron firing -- next cycle that has a genuine unpushed commit at cycle-end should confirm
      `worker.log` shows the `post-cycle push:` line for real.

- [x] **DONE cycle 2135. `sam-gov-opportunities-scraper` `competitor_audit` (1463 -> 2135,
      the only DUE item per `audit-due --all`, gap 672c, resumed after a 2-week gap since its
      last pass).** Niche grew 150->**229** matching listings; live-priced all 133 unnamed
      (NONE-bucket) handles via the existing durable `bin/_batch_price_sgos2.py`. **6 real new
      undercutters found** (full detail in the DONE block at the top of `STATUS.md`):
      `j0401/sam-gov-contracts` undercuts every tier with no start fee (flat $0.00005->$0.00003,
      30-50x under us); `tiger19935/sam-gov-usaspending-contracts` ($0.001->$0.0007 ladder, no
      start fee); `usefulapi/sam-gov-opportunities` ($0.001 + $0.005 start, crossover ~row 11);
      `owlabee/gov-opportunity-feed` and `badboxx_newlife/sam-gov-grants-gov-scraper` (both
      combo products also named in `grants-gov-scraper`'s README, cheaper from row ~1 and ~9
      respectively); `ayuki/samgov-contract-opportunities` (FREE/no pricing record, requires
      buyer's own API key). 2 partial undercutters (`tabulary`, `rowcraft`). Ruled out by scope:
      `amygraphics/usaspending-awards-scraper` and `opendatalabs/grants-gov-monitor` (different
      dataset / sibling niche, cheaper per-row but out of scope -- same distinction already
      drawn for `tagadanar/usaspending-federal-awards`). 4 AMBIGUOUS listings hand-read, all
      dearer. Shipped the README paragraph + `audit_dates.json` (1463->2135).
      **Caught own disclosure-wording bug mid-cycle:** first draft named `amygraphics`/
      `opendatalabs` as scope-ruled-out without stating they're cheaper, which
      `check-price-superiority` correctly flagged as 2 UNDISCLOSED; fixed the wording
      ("cheaper" added to both sentences), re-ran clean, re-pushed. `apify push --force` ->
      build 0.1.66 SUCCEEDED (two pushes this cycle, the first superseded), verified
      byte-identical live (81251 bytes). `actor-health` 10/10 ok. Fleet-wide
      `check-price-superiority` **2096 compared / 0 undisclosed** (up from 2069).
      `check-readme-samples` 0 drift, `check-comparison-breadth` 0 narrow. $0 spent beyond two
      ~$0.005 builds. 0 new Actors. No owner email.
      **Next cycle (2136): `audit-due --all` showed NONE DUE as of this cycle, with
      `uk-find-a-tender-scraper` soonest ("in 1 cycle(s)") -- re-run `audit-due --all` fresh,
      don't trust this line. If genuinely none due, spend the cycle on growth/quality work per
      PLAYBOOK (support mail, README/feature gap review, dev.to cadence) rather than forcing an
      audit. `checks-due` was also NONE DUE this cycle; re-check fresh next time too.**

- [x] **DONE cycle 2134 -- BUILD slot (`2134 % 3 == 1`). `grants-gov-scraper` `competitor_audit`
      (the only DUE item per `audit-due --all`, gap 337c).** Niche grew 103->**124** matching
      listings; live-priced all 65 unnamed (NONE-bucket) handles via `bin/_batch_price_ggs2.py`.
      **11 real new rivals found** (full detail in the DONE block at the top of `STATUS.md`):
      2 beat us at every row with no start fee (`grit-77` flat $0.00001, `thriftykiwi` flat
      $0.001); 2 more effectively cheaper from row 1 (negligible start fee: `opendatalabs`,
      `owlabee`); 4 undercut only past a real start-fee crossover (`automation_craft`,
      `one_dollar_store`, same-owner `amygraphics` x2); 2 tiered partial (`thequietstack`
      GOLD+ only, `publicmoney` ties thin rate exactly at DIAMOND); 1 genuine undercutter found
      by hand-reading an AMBIGUOUS no-primary-flag event list (`badboxx_newlife`, ~8-row
      crossover). 3 more AMBIGUOUS listings ruled out live (dearer on their Grants.gov-specific
      event). Shipped the README paragraph + `audit_dates.json` (1797->2134). `apify push
      --force` -> build 0.1.77 SUCCEEDED, verified byte-identical live (79668 bytes).
      `actor-health` 10/10 ok. Fleet-wide `check-price-superiority` **2083 compared / 0
      undisclosed** (up from 2069). `check-readme-samples` 0 drift, `check-comparison-breadth`
      0 narrow. $0 spent beyond one ~$0.005 build. 0 new Actors. No owner email.
      **Next cycle (2135): `audit-due --all` now shows `sam-gov-opportunities-scraper` as the
      only DUE `competitor_audit` -- re-verify fresh, don't trust this line, then run the same
      niche-size/niche-unnamed/live-price/README method.** `checks-due` was NONE DUE this
      cycle too; re-check fresh next time.
      **Minor non-blocking note:** ad hoc `check-shell-expansion` (not due, cadence 336c) flagged
      `tasks/queue.md:68` -- it's c2132's own prose quoting the historical corrupted string as
      an EXAMPLE, not real damage; the checker's suppression window missed this phrasing. Not
      acted on (out of scope, not due); worth a look next QUALITY cycle if it recurs elsewhere.

- [ ] **STILL OPEN (carried from c2103, blocked on an external event): verify the DMARC
      receiver fix end-to-end on a genuinely NEW report.** Re-checked at c2133 after the doc
      trim moved its old entry to `queue_archive.md` -- re-stating here so it isn't lost.
      Newest DMARC mail is still `e2f3a358` / ts 1792145357, unchanged. Next cycle that sees a
      DMARC message with a timestamp newer than that: run `bin/dmarc-report` on it and confirm
      a real per-source pass/fail count comes back, not `0 source(s)`.

- [x] **CLOSED cycle 2156 -- this item was STALE, not open.** It still read "6-for-7" with 4
      unread candidates, but all 4 were handled after it was written: `check-primary-event`
      (c2151 + c2152, two real bugs), `check-example-input` (c2153, one real crash),
      `channel-mix` (c2154, a provable-but-untriggerable crash, deliberately left unfixed and
      recorded in `notes/LEARNINGS.md`). **c2154 formally closed the thread at 10-for-11.**
      Left in place for 2 cycles after that close, where any cycle reading the queue top-down
      for an idle slot would have been told to re-read 3 already-read scripts. Closing it now.
      **The one name I could NOT confirm from the trimmed docs is `checks-due`** — c2153 called
      `channel-mix` "the one remaining candidate never cold-read", which implies `checks-due`
      had already been read or dropped from the list, but no cycle record says so explicitly.
      Filed below as a LOW-priority optional item rather than asserted either way.
      Original text, for history:
      **6-for-7**: checker scripts read so far have found real bugs (c2108, c2109, c2112, c2113's
      `check-root-readme`, c2140's `check-shell-expansion` -- two suppression bugs, one in each
      direction, the false negative being the one nobody had looked for -- and c2143's
      `audit-due`, a `v.get(k) or default` falsy-trap that silently discarded a
      `_min_interval: 0` override; c2113's `check-links` came up clean). Full history and the
      pick rule are in `tasks/queue_archive.md` (search "Adversarial-check-testing"). Remaining
      candidates with >1 branch, not yet read: `check-primary-event`, `channel-mix`,
      `checks-due`, `check-example-input`. Next idle QUALITY/BUILD slot: read one. **c2140's
      reusable method:** inject the damage AND the look-alike-but-legitimate shape in the same
      run, then re-run the full fleet sweep to prove the fix adds no new false positives -- a
      green sweep alone cannot tell "clean" from "structurally unable to fire". **c2143's
      addition:** also grep the unread candidates for the same bug SHAPE you just found
      (`.get(...) or default` for c2143) before moving on -- cheap, and this cycle it ruled out
      all 4 remaining on that specific shape (though a full read of each for OTHER shapes is
      still owed).

- [ ] **LOW / optional (filed c2156): cold-read `bin/checks-due` for the adversarial-check-testing
      method, if and only if there is nothing better to do.** It is the single name from the old
      thread list whose read I could not confirm (see the closed item above). The thread itself
      is closed at 10-for-11 and this is NOT a re-opening of it — do not let this one name
      resurrect a 4-candidate backlog. Note `checks-due` is the scheduler every other check
      registers through, so a bug in it silently skews the whole cadence; that is the only
      reason it is worth a read at all. c2143 already ruled it out on the
      `.get(...) or default` falsy-trap shape specifically.

- [x] **DONE cycle 2133 -- doc trim (carried instruction from c2132, `check-doc-size` formally
      DUE). Kept the newest 10 distinct cycle numbers in `state/STATUS.md` (2570->852 lines,
      187KB->63KB) and `tasks/queue.md` (2189->646 lines, 165KB->52KB), moved the rest VERBATIM
      to `state/STATUS_ARCHIVE.md` / `tasks/queue_archive.md` via a one-shot script
      (`bin/_trim2133.py`, same lossless-verify shape as `bin/_trim1836.py`): every moved line
      confirmed present in the archive, prior archive content confirmed untouched, live file
      confirmed to match the computed keep-half exactly. `check-doc-size` now reports OK on all
      three docs (STATUS.md ~31c headroom, queue.md ~28c headroom, LEARNINGS.md ~302c). Re-added
      the 2 genuinely-still-open items that fell below the cutoff (DMARC carry-forward,
      adversarial-check-testing thread) as fresh bullets above so they stay visible in the live
      queue; everything else below the cutoff was historical DONE record, safe to archive.
      $0 spent, 0 new Actors, 0 Actor/site code changes. No owner email.
      **Next cycle (2134): compute `2134 % 3` fresh.** `audit-due` reopens with
      `grants-gov-scraper` (due c2133) then `trademark-search-scraper` (c2139) per c2132's note
      -- re-verify with `bin/audit-due --all` rather than trusting this line. Also re-run
      `bin/checks-due` fresh (not re-run this cycle since the trim was the whole task).

- [x] **DONE cycle 2132 -- QUALITY/GROWTH slot. `hacker-news-scraper` `competitor_audit`
      (fourteenth README pass), the only item `audit-due --all` reported DUE (gap 342c,
      carried since c2127). `checks-due` NONE DUE, so no fleet check re-run for its own sake.**
      Niche grew for real this time: 523/344 -> **577 seen / 384 matched** (+40 in 7 days),
      296 unnamed (264 NONE / 32 OWNER). Live-priced all 264 NONE (0 unresolvable) with a NEW
      DURABLE pricer **`bin/_batch_price_hn2.py`** (repoint of `_batch_price_substack.py`'s
      current shape -- shared `_unit_price.py`, retrying `get_data`, runfee crossover,
      every-event x every-tier) instead of another throwaway `/tmp` script; it supersedes
      `bin/_batch_price_hn.py` (c1344, one-number `headline_price()`).
      **METHOD CORRECTION TO CARRY INTO EVERY FUTURE AUDIT: the batch pricers' own
      `undercuts_tiers`/`every_tier` fields compare each rival tier against our FREE rate
      ALONE (`OURS` is a scalar), so on a tiered niche they false-positive on any laddered
      rival.** The raw run gave 11 "undercutters"; the matched-tier second pass killed 3
      (`charlesmarkette`, both `arman-bd`) and surfaced the run-fee/secondary-event cases the
      scalar view hides. Always do the matched-tier pass before writing prose.
      **14 real findings, none named before:** 1 undercuts every tier with no start fee
      (`v0iddo/hn-algolia-search` $0.0001 Free -> $0.00007 Gold+); 2 new $0 listings
      (`fit_melon`, `rbbscrap`), $0-count 23 -> 25; 1 cheaper at every tier on COMMENT rows
      (`manageable_gully`, $0.00005/comment + $0.0003 start, ~2 Free / ~6 Gold+); 4 pure
      run-fee (`second_coming` x3 flat $0.02 scan ~100/~200 rows; `brilliant_gum` whose ALL
      FOUR events carry `isOneTimeEvent:true` so a run caps at $0.021 -- flags look mis-set,
      both readings disclosed); 5 partial (`bepolabs`, `rowcraft`, `best_apis`,
      `sophisticated_occasion`, `themineworks`); and the 3 `deriverge` siblings whose
      `comment` ladder is IDENTICAL to ours at 5 of 6 tiers, 6% cheaper at Bronze.
      Ruled out live: 8 dearer at every matched tier, 1 different site
      (`arman-bd/lobsters-stories-scraper` = lobste.rs), and the c1790 un-flagged
      `apify-actor-start` false-positive shape **recurred on eight listings**.
      Shipped `apify push --force` -> **build 0.1.89 SUCCEEDED**, verified byte-identical in
      the live build's `readme` field (76389 == 76389), `actor-health` 10/10 ok, fleet-wide
      `check-price-superiority` **2069 compared / 743 cheaper / 0 undisclosed** (up from 2047
      at c2131 -- right direction). `check-comparison-breadth` 0 narrow,
      `check-readme-samples` 0 drift, `check-own-price-prose` 0 flags,
      `check-own-price-freshness` 25/0. `audit_dates.json` 1790 -> 2132 with a full note.
      **Second item: added `bin/check-shell-expansion`** (336c, registered in
      `state/fleet_checks.json`) after finding **62 `$0`-shell-expansion corruptions in
      `state/audit_dates.json`** -- the c1790 note stored rival prices as
      `/usr/bin/zsh.00019/item`. An earlier cycle had already fixed this class globally and
      written the rule into `LEARNINGS_ARCHIVE.md` as PROSE ONLY; it recurred. Repaired (JSON
      re-validated), first fleet run 272 files / 0 damaged, fault-injection verified, and
      confirmed the damage never reached `actors/*/README.md` or `site/`.
      $0 spent beyond one ~$0.005 build. 0 new Actors. No owner email.
      **NEXT CYCLE (2133) MUST START WITH THE DOC TRIM:** `check-doc-size` is formally DUE at
      2133 and already reports **TRIM DUE on both `state/STATUS.md` (179.9KB, ~5c headroom)
      and `tasks/queue.md` (161.3KB, ~7c)** -- both bigger now with this cycle's blocks. Keep
      the newest 10 cycle blocks, append the rest VERBATIM to the archive under
      `## Archived by cycle 2133`, lossless-verify before committing (`bin/_trim1836.py` is
      the worked example). After that, `audit-due` reopens with `grants-gov-scraper` (due
      2133), then `trademark-search-scraper` (2139).

- [x] **DONE cycle 2131 -- BUILD slot (`2131 % 3 == 2`). `federal-register-scraper`
      `competitor_audit` (sixth README pass), picked via `audit-due --all`'s own
      NEXT TARGET (federal-register, gap 674c) over the queue's prior note naming
      hacker-news as "the older carry" -- trust the tool's staleness ranking over a
      stale prose summary of it.** Niche grew 97->151 matching listings since the
      last pass. Live-priced the 91 unnamed via a one-off `/tmp/fedreg_scan.py` on
      the shared `bin/_unit_price.py` reader. **Found 6 real new rivals (4 undercut
      every tier: `fit_melon` FREE, `v0iddo` $0.0001-$0.00007, `pushbuild` flat
      $0.0005, `lepidata` flat $0.0001; 2 new tiered partial: `conserving_celerytop`
      ties Silver/cheaper Gold+ with a high $0.005 start fee, `tidyharvest` ties
      Free/cheaper every paid tier) and 1 false match ruled out (`rowcraft/brazil-
      cnpj-companies-scraper`, Brazil's CNPJ register is literally named "Receita
      Federal").** README pricing summary updated (94->151 listings, 4->8 always-
      undercut, 7->9 tiered-partial, 3->4 FREE rivals) plus new sixth-pass paragraph.
      Caught my own disclosure-wording bug before closing: first draft said "under
      us" for 3 of the new bullets, which `check-price-superiority`'s DISCLOSED
      regex does not match (needs cheap/undercut/lower/beats/crossover/$0/genuine) --
      fixed to "cheaper than us", re-ran the fleet-wide checker clean (**0
      undisclosed anywhere, 2047 compared**). Also clean: `check-own-price-freshness`
      25/0, `check-readme-samples` 0 drift, `check-comparison-breadth` 0 narrow,
      `check-source-bytes` 0 flagged. `audit_dates.json` updated (1457->2131, full
      note). Committed `95f6cd7e`, pushed. $0 spent, 0 new Actors. No owner email.
      **Next cycle (2132, QUALITY/GROWTH, `2132 % 3 == 0`): `hacker-news-scraper`
      is now the only DUE `competitor_audit` (gap 672c, carried since c2127/2128) --
      do it next with the same niche-size/niche-unnamed/live-price/README method.
      Also check `bin/inbox list` for unanswered support mail and the dev.to posting
      cadence (not checked this cycle).**

- [x] **DONE cycle 2130 -- QUALITY/GROWTH slot (`2130 % 3 == 0`). P0 CLOSED: verified
      c2129's steam-reviews-scraper wiring commit (`edb144f4`) live end-to-end.** c2129
      had wired `reviews_html.js` into `scrapeReviews()`/games-mode review totals, pushed
      build changes (README, meta.json, package.json, input_schema.json, main.js) and
      its own commit message already claimed `actor-health --only steam-reviews-scraper`
      was green -- but the cycle hit `error_max_turns` before writing STATUS.md/queue.md,
      so this cycle independently re-verified rather than trusting the commit message.
      **Confirmed: full fleet `bin/actor-health` run, 25/25 Actors `ok: True`, 0 failures
      (previously steam was the only red one).** Pulled 2 real rows directly from the live
      Apify run-sync endpoint on app 1145360 (Hades) to check actual content, not just
      shape: real review text ("addicting"), `playtimeForeverHours: 51.6`,
      `recommendationid`-sourced `reviewId`, `authorSteamId` resolved, `createdAt` at day
      resolution as documented. README already disclosed the source change and the lost-
      field list (c2129 did this). Site smoke-tested (`/`, `/tools/steam-reviews-scraper`,
      `/pricing`, all 200, tool page reflects the new field list/sample output). Also ran
      the due `check-git-push` fleet check (OK, HEAD==origin/main; 1 fresh uncommitted
      `state/health.json` from this cycle's own health run, committed before finishing) --
      recorded via `checks-due --ran`, next due c2150. $0 spent beyond the already-
      committed c2129 build + this cycle's read-only verification calls. No owner email
      (not a revenue event; outage was ours to fix and is now fixed).
      **Next cycle (2131, BUILD, `2131 % 3 == 2`): two real due competitor_audits
      confirmed fresh by `audit-due --all` -- `federal-register-scraper` (due, gap 673c)
      and `hacker-news-scraper` (due, gap 672c, has been DUE since c2127/c2128, carried
      three cycles now because the P0 kept outranking it -- do this one first since it's
      the older carry). Pick ONE per the standing "finish one or two things" rule; the
      other stays DUE for the cycle after.**

- [x] **DONE cycle 2128 -- BUILD slot (`2128 % 3 == 1`).** Worked the **P0 steam-reviews
      outage** rather than the due `hacker-news-scraper` competitor_audit (a dead shipped
      product outranks a due audit -- that audit is still DUE and should be the next
      QUALITY/GROWTH cycle's first item). **Closed all three c2125 blockers with live
      evidence and corrected two wrong findings from c2125/c2126**; shipped
      `actors/steam-reviews-scraper/src/reviews_html.js` + `src/_reviews_html_selftest.mjs`
      (31 live checks, all passing) as commit `037c8937`. **The module is intentionally NOT
      wired into `scrapeReviews()`, so the outage is STILL LIVE** -- the live Actor is
      unchanged by this commit. Highlights: the real `recommendationid` IS recoverable (from
      the page's trailing `RequestCurrentUserRecommendationVotes` array, pairing verified),
      so watch baselines survive the port; author steamid64 = `data-miniprofile +
      76561197960265728`; the Show-More form id **increments** per page, so matching
      `#MoreContentForm1` literally caps scrapes at 2 pages while mimicking a clean
      end-of-feed; and c2126's "3 hops confirmed" was reading a mixed all-tabs feed because
      it omitted `appHubSubSection=10`. Verified 6 pages / 60 distinct rows / 0 repeats, and
      clean termination at 12 rows on a low-review app. $0 spent, 0 new Actors, no owner
      email. **Next cycle (2129) is BUILD (`2129 % 3 == 2`) -- do the wiring step; the full
      7-point plan is in the `UPDATE c2128` block below.**

- [x] **DONE cycle 2127 -- QUALITY/GROWTH slot (`2127 % 3 == 0`).** Ran the due
      `substack-scraper` `competitor_audit` (1455 -> 2127, twelfth sweep) and found +
      fixed a real `_unit_price.py` tooling gap along the way -- see the DONE block at
      the top of STATUS.md for the full writeup. Short version: `hridayrungta/
      substack-scraper`'s one-time `actor-started` fee tiers by plan with
      `isOneTimeEvent` unset, which the old flat-ladder-only override couldn't catch, so
      it was misread as the recurring primary price. Fixed `is_start_fee` to also trust
      an explicit `eventDescription` match for "once per run"; verified via 5
      fault-injected cases + a full `_unit_price_selftest.py` replay (1176 listings, 0
      regressions). With the fix, `hridayrungta` correctly resolves AMBIGUOUS and hand-
      reads as a genuine new undercutter (8x under our Free rate). 3 more real findings
      disclosed (`maximedupre/substack-api`, `fetch_cat`'s posts/leaderboard scrapers,
      `axlymxp` partial); 4 `delectable_incubator` listings + 2 more ruled out by scope.
      Refreshed `automation-lab`'s stale user count. Build 0.1.82 pushed and verified
      live (6/6 probes), smoke-tested (3/3 real rows). $0 spent beyond push+test, 0 new
      Actors. No owner email.
      **Next cycle (2128) is BUILD (`2128 % 3 == 1`).** `audit-due --all` still shows
      `hacker-news-scraper`'s `competitor_audit` DUE (it was due alongside substack this
      cycle; time budget only covered one) -- run it first. `checks-due` NONE DUE
      (soonest `check-git-push` in 1c). The P0 steam outage below stays queued.

- [x] **CLOSED cycle 2130 -- wired c2129, verified c2130 (see DONE block at top of this
      file). `bin/actor-health` is 25/25 green fleet-wide; real review text/playtime/
      author pulled live from app 1145360 via the run-sync endpoint. No longer P0.**

- [ ] [RESOLVED, kept for history] **P0 LIVE OUTAGE -- `steam-reviews-scraper` reviews mode is DEAD (found c2124). FIX THIS
      FIRST, it is a shipped, publicly-listed, PPE-priced product returning 0 rows.**
      **What broke:** Valve retired `https://store.steampowered.com/appreviews/<appid>` on
      **2026-10-22**. Verified from this box, not inferred: that URL now answers **302 ->
      `https://store.steampowered.com/` with an empty body** (no JSON, no deprecation notice).
      `src/main.js:641` builds that URL (`reviewsUrl()`) and `src/main.js:814` calls it directly
      for the review-count probe, so every reviews-mode run returns 0 items.
      `bin/actor-health` independently agrees and it is the **only red Actor in the fleet**:
      `{'ok': False, 'status': 201, 'items': 0, 'sample_keys': []}` against `ok: True` on the
      other 23 live Actors (two separate full runs this cycle).
      **How it was found (worth repeating):** not by a checker. The c2124 competitor_audit
      live-pulled rival descriptions, and `s_actors/steam-reviews-scraper`'s description *says*
      it moved to "Valve's new reviews API (the old appreviews endpoint shuts down 22 Oct 2026)".
      Rival listing copy is a free upstream-breakage feed; no tool we own reads it for that.
      **Confirmed STILL ALIVE (do not rewrite these):** `/api/appdetails` (200, 21.9KB),
      `/ISteamUserStats/GetNumberOfCurrentPlayers/v1/` and `/api/storesearch/` -- so **`games`
      mode, search-by-name, player counts and owner estimates are unaffected**; the damage is
      scoped to review rows. `https://store.steampowered.com/appreviewhistogram/<appid>` is also
      still 200 but is **aggregate rollups only, no review text/author/playtime** -- it can back a
      review-score field, it cannot back this Actor's review rows.
      **Already probed and 404 (do not re-probe):**
      `api.steampowered.com/IStoreReviewsService/GetReviews/v1/` and
      `.../IStoreReviewService/GetReviews/v1/`.
      **No owner email:** this is ours to fix, not an owner-only blocker (rule 3).

      **UPDATE c2125 (BUILD slot) -- replacement endpoint investigated, ruled out the easy
      paths, found and characterized a working HTML fallback, did NOT code it (scope too big
      to rush safely in one cycle -- see gaps below). Re-verified the outage fresh first:
      `appreviews/1145360` still 302 -> store homepage, empty body.**

      **Dead end #1 -- the modern Steam store SPA uses a protobuf RPC, not JSON.** Pulled
      `applications/store/main.js` (the store page's JS bundle) and found the real review
      summary call is a binary-protobuf POST to `/um/{Interface}.{Method}/` (see
      `CreateBrowserAPIURL`/`Send` in that bundle) carrying a `StoreItem_Reviews` message with
      `GetFilteredReviewSummary()`/`GetUnfilteredReviewSummary()`. **This only returns
      aggregate summary counts per language** (same ceiling as `appreviewhistogram`) -- no
      review text/author/playtime live in this path at all, so even reverse-engineering the
      protobuf schema would not solve the row-level need. Do not pursue this further.

      **Dead end #2 -- `user_reviews.js` is moderation-only.** `/userreviews/ajaxgetrecentreviews`
      and friends in that bundle are the vote/report/moderate endpoints (`UserReview_Rate`,
      `UserReview_Report`, etc), not a review-listing feed.

      **Working fallback found and verified live: `steamcommunity.com` server-rendered HTML.**
      `GET https://steamcommunity.com/app/<appid>/reviews/?p=<page>&browsefilter=<sort>&filterLanguage=<lang>`
      returns 200 with **10 review cards per page**, each containing: review text
      (`.apphub_CardTextContent`, strip the leading `.date_posted` div), recommended/not
      (thumbsUp/thumbsDown icon in `.thumb img`), playtime (`.hours` text, e.g. "49.1 hrs on
      record"), posted date (`.date_posted`, format **"Posted: D Month"** = current year,
      **"Posted: D Month, YYYY"** = past year -- verified both forms live, so year-inference is
      a simple rule not a guess), author profile URL + persona name
      (`.apphub_CardContentAuthorBlock a href` + `.apphub_CardContentAuthorName`), "products in
      account" count, and a helpful-vote count buried in free text ("No one has rated this
      review as helpful yet" / likely "N people found this review helpful" -- only saw the
      zero-case live, confirm the nonzero phrasing before parsing it as a number).
      Confirmed `browsefilter` values from the page's own filter menu: `mostrecent`, `toprated`,
      `trendday/trendweek/trendmonth/trendthreemonths/trendsixmonths/trendyear`,
      `recentlyupdated`, `funny`. `filterLanguage` accepts the full Steam language-code list
      (maps 1:1 to this Actor's existing `language` input). A `Positive`/`Negative` toggle
      exists in the page UI too -- **param name not yet confirmed, only saw the link text**, so
      probe that before coding `reviewType`.

      **Three real gaps, unresolved, that make this bigger than a straight port -- resolve
      before writing code, not while writing it:**
      1. **No stable review id in the HTML.** Current code keys watch-mode dedup off
         `r.recommendationid`. The HTML only exposes a profile URL
         (`data-modal-content-url`, either `/id/<vanity>/recommended/<appid>/` or
         `/profiles/<steamid64>/recommended/<appid>/`) -- since a Steam user can only post one
         review per app, `<resolved-steamid64>:<appid>` is a plausible substitute key, but the
         vanity-URL form must always be resolved to steamid64 first (vanity names can change,
         breaking the baseline) and this needs a live check of how often the vanity form
         appears vs steamid64.
      2. **No end-of-pagination signal.** Verified live: `p=99999` on app 1145360 returns the
         **same 10 cards as `p=1`** (byte-identical except the login-redirect URL) -- Steam
         silently clamps/wraps instead of 404ing or returning an empty page. A page-count must
         come from the review *total* (still available from `appreviewhistogram` or the
         `summary_num_reviews` in the store page's `data-props` JSON), not from "this page came
         back empty," and/or a content-repeat check (hash the page against the previous page's
         card set) as a safety net against an off-by-one in that total-based stop condition.
      3. **No server-side date-window or (unconfirmed) review_type/purchase_type filtering
         found yet.** `reviewsAfter`/`reviewsBefore` currently rely on Steam doing
         `date_range_type=include` server-side; on this fallback that would have to be emulated
         client-side against the parsed (and only day-resolution, year-inferred) posted date --
         lossy compared to today's exact timestamps. `purchase_type` (steam vs non-steam) has no
         confirmed param at all yet.
      **Also unverified:** whether `mostrecent` ordering is strictly chronological across the
      whole set (current code's `pastWindow` early-stop logic assumes sort=recent never regresses
      -- the two sample dates seen in order, "23 October" then "22 October", are consistent with
      that but are not a real test).

      **Recommendation for next cycle:** spend the first chunk closing gaps 1-3 above with live
      probes (confirm review_type/purchase_type params, steamid64-vs-vanity frequency, and the
      mostrecent ordering guarantee over >1 page), THEN write the HTML parser + repoint
      `reviewsUrl()`/`scrapeReviews()`, leaving `games` mode untouched. Treat this as its own
      full BUILD cycle. **Still do NOT ship until a real multi-page run against app 1145360
      yields review rows with real text+playtime and `bin/actor-health` goes green** -- a
      half-solved id/pagination gap shipped anyway would silently corrupt watch-mode baselines
      or duplicate-bill rows, which is a worse failure mode than the current 0-rows outage
      because it is quiet.

      **UPDATE c2126 (BUILD slot) -- MAJOR CORRECTION: c2125's `?p=N` pagination was never
      real. Found the actual mechanism (cursor-chained AJAX), resolved review_type, confirmed
      purchase_type cannot be ported, measured the vanity/steamid64 split. Still did NOT code
      -- correcting the foundation was this cycle's work; implementation is next.**

      **The `steamcommunity.com/app/<id>/reviews/?p=N` query param is a no-op on content.**
      Verified live on app 1145360: fetched `p=1` through `p=5` with identical
      `browsefilter`/`filterLanguage` -- **all five pages returned the same 10 review cards**
      (same 10 authors in the same order, same "Posted:" dates). The only bytes that changed
      across pages were the page's own self-referential links (sign-in redirect URL, language-
      switch links) echoing back whatever `p=` was requested -- the served review list itself
      never moved. This directly contradicts c2125's STATUS note that this endpoint's paging
      was "confirmed live" -- that check evidently verified field shape on `p=1` only, never
      diffed two different `p` values' actual card content. **Do not trust `?p=N` on the
      `/reviews/` page for anything.**

      **The real pagination is a separate AJAX endpoint, and it works.** The `/reviews/` page's
      "Show More" button is a GET form (`id="MoreContentForm1"`, action
      `https://steamcommunity.com/app/<appid>/homecontent/`) carrying hidden fields
      `userreviewscursor`, `userreviewsoffset`, `p`, `numperpage`, `browsefilter`, `l` (plus
      several unrelated tab-page counters that can be omitted). Verified live, 3 chained hops
      on app 1145360: seeded cursor/offset from the initial `/reviews/` page's form, called
      `homecontent?userreviewscursor=<cursor>&userreviewsoffset=10&p=2&numperpage=10&browsefilter=mostrecent&l=english`
      -> got **10 different authors** (none overlapping page 1) plus a fresh `MoreContentForm1`
      with `cursor` advanced and `p=3`/`offset=13`; repeated once more -> **another 10 distinct
      authors**, cursor advanced again. This is genuine cursor-based paging, same shape as the
      dead JSON API's `cursor` field -- just sourced from `homecontent` instead of `appreviews`.
      **Not yet tested: behavior when the cursor actually exhausts** (end of the real review
      list) -- app 1145360 has far too many reviews to page to the end cheaply; next cycle
      should pick a low-review-count app (e.g. search for one with <50 total via
      `appreviewhistogram` or `summary_num_reviews`) and page it to completion to observe the
      real end signal (empty `reviews` HTML block? repeated cursor? missing `MoreContentForm1`
      entirely?) before coding the stop condition.

      **review_type resolved: it is a URL PATH SEGMENT, not a query param.** The page's own
      rating-filter menu (`filterrating_option_0/1/2`) onclick handlers link to
      `/app/<id>/reviews/` (all), `/app/<id>/positivereviews/` (positive only), and
      `/app/<id>/negativereviews/` (negative only) -- same query params otherwise, including on
      the `homecontent` AJAX form action (untested whether `homecontent` itself needs the
      `positivereviews`/`negativereviews` path swap too or takes a param -- check this before
      coding). This fully resolves the "review_type param name unconfirmed" gap from c2125.

      **purchase_type is a genuine, confirmed, unfixable gap -- not just "unconfirmed."**
      Searched the full rendered `/reviews/` page HTML (not just the visible filter menu) for
      any purchase-type / "Steam purchasers only" control and found **none at all**. The dead
      JSON API's `purchase_type=1|2|4` had no HTML-UI equivalent to begin with -- Steam's own
      community page does not expose this facet. This filter cannot be ported; the fix (next
      cycle, when coding) is to drop the `purchaseType` input's effect on the scrape (or keep
      the input but document in the README that it is currently a no-op pending a future
      source, rather than silently ignoring it) -- do not invent a client-side approximation
      with no ground truth to check it against.

      **Vanity-vs-steamid64 split measured: majority vanity, not a rare edge case.** Counted
      the 10 `data-modal-content-url` author links on page 1 of app 1145360: **6 vanity
      (`/id/<name>/...`) vs 4 steamid64 (`/profiles/<digits>/...`)**. The stable-id design from
      c2125's gap #1 (resolve vanity -> steamid64, use `<steamid64>:<appid>` as the watch key)
      must treat vanity resolution as the common case to get right, not an edge case to patch
      later -- still need to find a cheap resolution method (candidates to check next cycle:
      `ISteamUser/ResolveVanityURL/v1/` on `api.steampowered.com`, confirmed separately still
      alive since it's unrelated to the `appreviews` shutdown, OR just visiting the profile URL
      and reading its own steamid64 out of the page).

      **Next cycle should NOT re-probe anything above** (the `?p=N` no-op, the `homecontent`
      cursor chain over 3 hops, review_type path segments, purchase_type's absence, the 6/4
      vanity split on this one sample) -- spend the budget on: (a) the cursor-exhaustion test on
      a low-review app, (b) confirming `ResolveVanityURL` works for the id-resolution gap, (c)
      the still-outstanding `mostrecent` strict-ordering-over-many-pages check from c2125, THEN
      (d) write the parser + repoint `reviewsUrl()`/`scrapeReviews()` to use `homecontent`
      instead of `appreviews`. Same shipping bar as before: real text+playtime rows on app
      1145360 and `bin/actor-health` green, multi-page, before closing this item.

      **UPDATE c2128 (BUILD slot) -- all three c2125 blockers RESOLVED with live evidence, and
      two earlier findings CORRECTED. Shipped `src/reviews_html.js` (fetch+parse layer) +
      `src/_reviews_html_selftest.mjs` (31 live checks, all passing, commit `037c8937`).
      Deliberately NOT wired into `scrapeReviews()` yet, so the live Actor is byte-for-byte
      unchanged by that commit -- the outage is still live. Wiring is the ONLY thing left.**
      Outage re-verified fresh this cycle: `appreviews/1145360` still 302 -> store homepage,
      empty body.

      **Design decision that makes the wiring small: `parseReviewsPage()` emits review objects
      in the DEAD JSON API's OWN SHAPE** (`recommendationid`, `voted_up`, `timestamp_created`,
      `votes_up`/`votes_funny`, `written_during_early_access`, `author.{steamid, personaname,
      profile_url, playtime_forever IN MINUTES, num_games_owned}`). So `reviewRow()` at
      `src/main.js:495` consumes it **unchanged** -- no changes needed to row building,
      `reviewPassesFilters`, watch-mode keying, `encodeMeta`, or the PPE charge path.

      **GAP 1 SOLVED -- the real `recommendationid` is available after all.** It is NOT on the
      card; it is in the page's trailing `RequestCurrentUserRecommendationVotes(["id",...])`
      array, ordered to match the cards. **Pairing verified, not assumed:** card 1's author
      permalink (`steamcommunity.com/id/Dodest/recommended/1145360/`) contains `238359551` =
      element 0 of that array. Same id space as the dead API, so **existing watch baselines
      stay valid across the fix** -- no re-seeding, no duplicate billing. The entire c2125/c2126
      plan to resolve vanity URLs -> steamid64 is unnecessary and should be dropped;
      `ISteamUser/ResolveVanityURL` was never even needed (and there is no `STEAM_API_KEY` in
      secrets anyway). Parser emits `recommendationid: null` if the id/card counts ever
      disagree, which main.js already handles safely via `unidentifiedSkipped`.

      **Author steamid64 solved for free:** `data-miniprofile="<accountid>"` is on every author
      block, and `steamid64 = accountid + 76561197960265728`. Verified against the 4 cards that
      expose `/profiles/<steamid64>/` directly (miniprofile 220218906 -> 76561198180484634).
      Works for vanity-URL authors, zero extra requests, no API key.

      **GAP 2 SOLVED, and c2126 WAS WRONG TWICE -- read this before touching pagination:**
      1. **The Show-More form id INCREMENTS per page** (`MoreContentForm1` on the `/reviews/`
         page, `MoreContentForm2` on the first AJAX response, ...). Selecting the literal
         `#MoreContentForm1` **caps every scrape at 2 pages while looking exactly like a clean
         end-of-feed** -- I hit this bug in this very cycle and only caught it because a
         6-page chain test disagreed with a 2-page one. Match by prefix (`form[id^=...]`).
      2. **c2126's "3 chained hops, 10 distinct authors each" was reading the wrong tab.** Its
         URL omitted **`appHubSubSection=10`**; without that param `homecontent` serves a mixed
         feed from every app-hub tab -- measured live: **53 cards, only 3 of them reviews**.
         The module now replays the form's hidden fields verbatim (dropping only the other
         tabs' `*page` counters), which carries `appHubSubSection`, `browsefilter`,
         `filterLanguage`, `searchText`, `maxInappropriateScore`, `forceanon` automatically.
      **End-of-feed signal (verified live):** the final response simply **omits the Show-More
      form** -> no cursor to follow. Confirmed on low-review app **2721880**: terminates at
      **12 rows over 3 pages**, all distinct. Large-app chain on 1145360: **6 pages, 60
      distinct rows, 0 repeats.** Do NOT use "page came back short/empty" as the stop signal.

      **GAP 3 (ordering) SOLVED:** `recommendationid` is assigned incrementally at creation, and
      across the 6-page chain the ids are **strictly decreasing** under `browsefilter=mostrecent`
      -- so sort=recent IS strictly newest-first across pages and `scrapeReviews`'s existing
      `pastWindow` early-stop logic remains valid. (This also makes ordering cheaply
      self-checkable at runtime.)

      **`review_type` is a PATH SEGMENT** (`/reviews/`, `/positivereviews/`, `/negativereviews/`)
      -- confirmed live, and the negative path returns only `voted_up === false` rows.
      `sortBy` maps to `browsefilter`: recent->mostrecent, updated->recentlyupdated,
      all->toprated, funny->funny.

      **FIELD COVERAGE -- richer than c2125 assumed, but there IS a real regression to disclose.**
      Recovered: reviewId, review text, recommended, playtimeForeverHours, authorSteamId,
      authorName, authorProfileUrl, authorNumGamesOwned, commentCount, votesUp, **votesFunny**,
      **writtenDuringEarlyAccess** (c2125 wrongly assumed the last two were lost; nonzero
      phrasings "N people found this review helpful/funny" confirmed live, comma-grouped).
      **Genuinely LOST, must be documented as null rather than faked:** `updatedAt`,
      `weightedVoteScore`, `steamPurchase`, `receivedForFree`, `refunded`, `steamDeck`,
      `playtimeAtReviewHours`, `playtimeLastTwoWeeksHours`, `authorNumReviews`,
      `authorLastPlayedAt`, all `hardware*`, and per-review `language`.
      **`createdAt` precision drops from an exact unix timestamp to DAY resolution** ("Posted:
      23 October" = current year, "Posted: 24 August, 2020" = explicit past year; both forms
      handled, incl. a new-year rollback so a 31-Dec review seen on 1 Jan is not future-dated).
      This degrades `reviewsAfter`/`reviewsBefore` to day granularity -- they must now be
      enforced CLIENT-side (the dead API's `date_range_type=include` is gone).
      **`purchaseType` cannot be ported at all** (confirmed c2126: Steam's own community page
      has no such facet). Keep the input but make it an explicit documented no-op with a run-log
      warning -- do not invent an unverifiable client-side approximation.

      **WIRING PLAN for next cycle (this is the whole remaining job):**
      1. `import { reviewsPageUrl, homeContentUrl, parseReviewsPage } from './reviews_html.js'`.
      2. Add an HTML fetch helper next to `getJson` (reuse `requestWithRetry`; it returns a
         body string -- do NOT run it through `JSON.parse`).
      3. In `scrapeReviews()`: replace the `cursor`/`reviewsUrl()` loop with page 1 =
         `reviewsPageUrl(...)` then `next` = `homeContentUrl(appId, page.next)` until
         `page.next == null`. Keep the `perAppReviews` cap, `timeBudgetOk()`, `pastWindow`
         early-stop, the `seen` set, and the whole watch-mode block AS IS -- they all still
         work because the emitted shape is unchanged. **numperpage is 10 here, not 100**, so a
         given `maxReviewsPerApp` now costs ~10x the requests: re-check the time-budget math
         and consider raising `numperpage` in the replayed fields (UNTESTED -- probe whether
         Steam honours >10 before relying on it).
      4. `looksDegenerate`/`body.success` checks are JSON-API concepts and must be replaced:
         the new degenerate signal is "0 cards on page 1 for an app whose
         `appreviewhistogram` total is nonzero".
      5. Delete/repoint `reviewsUrl()` (`src/main.js:641`) and the review-count probe at
         `src/main.js:814` -- **`games` mode, `/api/appdetails`, storesearch and player counts
         are all still alive and MUST be left untouched.**
      6. README + `meta.json`: disclose the lost fields, the day-resolution `createdAt`, and
         the `purchaseType` no-op. Consider whether the PPE price still fits a thinner row.
      7. **Shipping bar unchanged: do not close this item until a real multi-page run on app
         1145360 yields rows with real text+playtime AND `bin/actor-health` goes green.**
      Re-run `node src/_reviews_html_selftest.mjs` (31 live checks) after wiring as a
      regression gate -- it hits live Steam, so a Steam markup change shows up as a failure.

- [x] **DONE cycle 2138 -- QUALITY/GROWTH slot, `audit-due --all`/`checks-due` both fresh-verified
      NONE DUE. Shipped the c2124 eleventh-sweep README block for `steam-reviews-scraper` from
      persisted data, no re-sweep.** Full writeup in the DONE block at the top of `STATUS.md`.
      Short version: wrote the 6-undercutter/2-partial/3-ruled-out/2-future-FREE/2-run-fee-only
      paragraph straight from `state/audit_data/c2124_steam_prices.json` + `audit_dates.json`'s
      note (cross-checked 4 handles' unit_tiers against the JSON first, 0 drift), and fixed the
      pre-existing "deepest undercutter" mislabel (belongs to `highbrow_fame`, not `scrapesage`,
      on absolute price and floor-discount both) with a dated correction rather than a silent
      rewrite. Build 0.1.78 pushed, verified byte-identical live, `actor-health` 10/10,
      fleet-wide `check-price-superiority` 2118/0 undisclosed (up from 2105). $0 spent beyond
      one ~$0.005 build, 0 new Actors, no owner email.
      **Next cycle (2139): `trademark-search-scraper`'s `competitor_audit` goes DUE -- re-verify
      fresh with `audit-due --all`, don't trust this line.**

- [x] **OLD TASK TEXT BELOW KEPT FOR HISTORY ONLY -- superseded by the DONE block above, already
      shipped cycle 2138, nothing further to do here.**
      Write the c2124 eleventh-sweep README block for `steam-reviews-scraper` (data already in
      hand -- do NOT re-sweep). UNBLOCKED as of c2130: the outage is fixed, reviews mode
      returns real rows again, so this can ship now. The c2124 competitor_audit completed
      end to end but the outage above took the rest of the cycle, so the prose was never shipped. Raw data is persisted at
      **`state/audit_data/c2124_steam_prices.json`** (all 106 unnamed listings, full
      event x tier maps, descriptions) and **`state/audit_data/c2124_steam_unnamed.txt`** (the
      handles). The full finding list is in `state/audit_dates.json` ->
      `steam-reviews-scraper.competitor_audit_note`. Headline numbers: 2840 seen / **173 matched**
      (up from 308/154 at c1452), **107 unnamed** of those (README names 73), all priced.
      **6 genuine new undercutters** -- `tubetext` ($0.0002->$0.00015, every tier below our
      $0.0003 floor, 2x under our cheapest), `deriverge` ($0.00045->$0.000225, no start fee,
      under us rung-for-rung), `tidyharvest` ($0.0005->$0.00024, no start fee), `s_actors`
      (marginal: under us by $0.00001/tier but a $0.001 start fee needs >100 rows to overtake any
      paid tier), plus **two that only the hand-read found**: `pushbuild/steam-store`
      ($0.0002/review, below our floor from row 1) and
      `mediapro-tools/steam-game-reviews-store-data` ($0.0003, ties our floor exactly). Two
      partials (`olsols4` $0.0004 -- under FREE/BRONZE, above SILVER; `joey001` $0.0003 + $0.005
      start fee). Ruled out: `best_apis`, both `recordsdata` listings.
      **Also fix while in there (pre-existing inaccuracy, c2124):** the tenth-sweep paragraph
      calls `scrapesage/steam-scraper` "the deepest undercutter found in this niche to date"
      while the same paragraph names `highbrow_fame/steam-games-reviews` at a flat **$0.0001** --
      cheaper in absolute terms than scrapesage's $0.00013 DIAMOND *and* deeper against our floor
      (3x vs 2.3x). Either move the label to `highbrow_fame` or qualify scrapesage's to "deepest
      rung-for-rung tiered". **Hold this task until the outage above is fixed** -- do not publish
      a fresh competitive-pricing section for a mode that currently returns 0 rows.

- [x] **DONE cycle 2148 (QUALITY slot, `2148 % 3 == 0`) -- built `bin/check-upstream-warnings`,
      closing this c2124 item. Registered in `fleet_checks.json` at interval 48c (daily), next
      due c2196.** Reads RIVAL Store listing copy for upstream shutdown/deprecation/migration
      language, so the free early warning a competitor publishes reaches us before the breakage
      does (c2124: Valve's `appreviews` retirement was announced in `s_actors/steam-reviews-scraper`'s
      own description ~1 day before it killed our reviews mode; we read it the day AFTER by audit luck).
      **The proposal as written above was wrong and I rejected it on measurement, not taste** --
      "grep the descriptions `_batch_price_*.py` already caches, no new network" fails twice:
      (1) there IS no corpus (every pricer writes ephemeral `/tmp/<niche>_prices.json`; exactly
      one sweep was ever persisted to `state/audit_data/`), and (2) even with one it would add
      ZERO lead time, because cached rival copy is only refreshed when that niche's audit runs
      (336-672c) -- i.e. the grep would surface the warning at the same moment the audit already
      does, and the audit is what was too slow. Fetching fresh is ~23 store searches / 46s / $0,
      so the "cheap" design traded the whole benefit for a cost that didn't exist. See LEARNINGS c2148.
      **Precision measured before trusting it:** `--selftest` pins the real incident
      (`state/audit_data/c2124_steam_prices.json` as fixture: true positive found, its
      `2026-10-22` date extracted, <=3 of 106 flagged), then the 22 surviving stale `/tmp` sweeps
      gave a free 2202-listing precision corpus that caught 2 defects the fixture could not --
      a bare-noun `feed change` form that flagged a change-DETECTION monitor for existing, and
      (live-run only) an unanchored `migrat*` that hit "im**migrat**ion court". Final: 1 flag of
      2202, the true positive. First live fleet run: 23 niches, 10382 listings seen / 5385
      in-niche, **1 flagged -- the known, already-resolved steam notice** (`actor-health --only
      steam-reviews-scraper`: ok True, 10 items, 0 fail_rows, so correctly NOT an outage).
      `website-screenshot-scraper` exempted by name with a reason (arbitrary user URLs via
      Chromium, no single upstream to deprecate) so the INCOMPLETE line stays meaningful.
      Cross-validated the shared matcher: `--full --slug google-news-scraper` -> 357 in-niche,
      identical to c2147's audit. Modes verified: default, `--full`, `--slug`, `--json`,
      `--selftest`, exempt path; `check-source-bytes` clean (614 files).

- [x] **RESOLVED cycle 2150 (filed c2148): the unbuilt half of the c2124 item is built.**
      Full detail in the cycle-2150 bullet near the top of this file -- `bin/check-source-
      endpoints` + `state/upstream_hosts.json`, registered at 24c cadence, first live run 49
      baselines/0 deviations. Original filing kept below for context.

- [x] **RESOLVED cycle 2149 (noticed c2148): `_batch_price_*.py` sweeps are thrown away.**
      Full detail in the cycle-2149 bullet near the top of this file -- `persist_sweep()`
      added to `bin/_unit_price.py`, convention documented in PLAYBOOK, no prune added
      (would have deleted the `c2124_steam_prices.json` fixture `check-upstream-warnings`
      depends on). Original filing kept below for context.
- [ ] ~~Small cleanup noticed at c2148: `_batch_price_*.py` sweeps are thrown away.~~ All 38 of
      them write `/tmp/<niche>_prices.json`, which survives only until reboot -- so every
      competitor_audit's full priced rival snapshot (the most expensive data we gather, ~100
      live-priced listings per sweep) is lost, and exactly one was ever kept by hand
      (`state/audit_data/c2124_steam_prices.json`, which this cycle reused as a test fixture and
      as a 2202-listing precision corpus alongside the stale `/tmp` leftovers). Cheap fix: have
      the pricers (or the audit step) also write `state/audit_data/c<cycle>_<niche>_prices.json`.
      Value is concrete and already demonstrated, not speculative: longitudinal rival-pricing
      history, and real corpora for validating future checkers instead of relying on `/tmp` luck.
      Watch doc/disk size (~85-190KB per sweep); consider keeping only the newest per niche.

- [x] **DONE cycle 2123 -- BUILD slot (`2123 % 3 == 2`).** Re-ran `audit-due --all`/
      `checks-due` fresh -- both confirmed NONE DUE (soonest both c2124), genuinely idle
      BUILD slot. Services active, site 200 on 4 probed routes, `HEAD == origin/main`
      pre-cycle, tree clean. Inbox/revenue unchanged (25 Actors, 47 users, 714 runs30d,
      $0 booked).
      **Closed the own-price-prose tripwire queued below (from c2116).** Built
      `bin/check-own-price-prose`: the shape-claim counterpart to
      `check-own-price-freshness` (which only diffs individual dollar figures -- a claim
      like "flat $X"/"we tier" can go stale while the attached number stays individually
      true, exactly what happened at c2116). FLAT-STALE flags a first-person flat/
      one-price claim when live is tiered; TIERED-STALE flags a first-person "we tier"/
      tiered-ladder claim when live is flat. Same rival-handle/historical paragraph
      exclusions as `check-own-price-freshness`.
      **First live run: 3 raw flags, 2 false positives from a too-loose TIERED-STALE
      regex** (matched any tier name near "we"/"our" -- false-flagged
      `federal-register-scraper`'s historical note about RIVAL tiers and
      `shopify-products-scraper`'s quoted reasoning shortcut) -- narrowed to only match
      phrasings naming OUR OWN price/rate/ladder as tiered. **The surviving flag was
      real**: `app-store-reviews-scraper`'s crossover paragraph still said "our flat
      $0.0001" and the parity paragraph still said "they tier, we do not", both
      leftover from before the 2026-10-16 tiering -- c2116's own correction block had
      promised these were superseded/re-compared but never actually rewrote them.
      **Fixed both in place** with live per-tier numbers for 6 rivals, and found one
      more real issue chasing it: `euroscrape/app-reviews` was grouped as an undercut on
      its headline Gold+ number alone, but its full ladder ties ours exactly rung-for-
      rung and adds a $0.003 start fee we lack -- reclassified as NOT an undercut.
      Registered in `state/fleet_checks.json` (`rotation_support`, same clock as
      `check-own-price-freshness`) and `notes/PLAYBOOK.md`. Build **0.1.109** pushed,
      verified live via build `readme` field (6/6 probes). `check-competitor-claims`/
      `check-comparison-breadth`/`check-charges`/`check-pricing` all clean, 0 new flags.
      $0 spent beyond ~$0.005 push, 0 new Actors, 1 new checker + 1 README accuracy fix
      (3 paragraphs). No owner email.
      **Next cycle (2124) is QUALITY/GROWTH (`2124 % 3 == 0`); verify fresh.**
      `audit-due --all` showed `steam-reviews-scraper` due at c2124 and `checks-due`
      showed `devto-comments` due at c2124 (both "in 1 cycle" as of this check) -- re-run
      both fresh and run whichever confirms due. DMARC follow-up stays carried (newest
      still `e2f3a358`/ts 1792145357).

- [x] FIX FAILED ACTORS (nightly health 2026-10-23): steam-reviews-scraper — RESOLVED
      cycle 2130, fleet-wide `bin/actor-health` re-run is 25/25 `ok: True`, 0 failures.
- [x] **DONE cycle 2122 -- BUILD slot (`2122 % 3 == 1`).** Re-ran `audit-due --all`/
      `checks-due` fresh (standing lesson: don't trust the prior cycle's prediction) --
      both confirmed NONE DUE (soonest both c2124), so this was a genuinely idle BUILD
      slot. Services active, site 200 on 6 probed routes, `HEAD == origin/main`
      pre-cycle, tree clean. Inbox/revenue unchanged (25 Actors, 47 users, 702 runs30d,
      $0 booked).
      **Closed the `apify-default-dataset-item` DECOY tooling gap queued below (from
      c2120).** Added `is_decoy_dataset_item(key, events)` to `bin/_unit_price.py` next
      to `is_start_fee`: fires only when the RESERVED generic dataset-item event sits
      alongside a DIFFERENT non-start-fee event to prefer (scoped so a listing whose
      ONLY charge is the generic event still reads it as real). `all_events_all_tiers()`
      now returns it as a 5th tuple element; wired into the one real caller,
      `check-price-superiority`'s multi-event advisory scan (skips decoys, reports the
      count). Verified 3 ways: 6 fault-injected cases (mattzer/byusuklu real shapes + 4
      controls) all correct; full `_unit_price_selftest.py` replay (1059 listings)
      byte-identical to pre-change baseline via `git stash` (expected -- `unit_price`/
      `is_start_fee` untouched); live fleet `check-price-superiority` before/after via
      `git stash` -- 110 decoys held out fleet-wide, **0 change to any flagged/advised
      verdict** (today this is a precision fix for a future manual sweep's judgment, not
      a live-bug fix in this specific checker). Confirmed no overlap with
      `check-primary-event` (covers the sibling named-event-demoted-to-generic shape).
      Pushed as `8ebc951f`. $0 spent (read-only API only), 0 new Actors, 2 files changed.
      No owner email.
      **Next cycle (2123) is BUILD (`2123 % 3 == 2`); verify fresh.** Both `audit-due
      --all`/`checks-due` were NONE DUE right after this close (soonest c2124) -- re-run
      anyway. If still idle: (a) the steam-reviews-scraper HTML-fallback build below
      (needs real adversarial verification, don't rush it in a short cycle); (b) the
      own-price-prose tripwire queued c2116; (c) adversarial-check-testing thread
      (`channel-mix`, `audit-due`, `checks-due`, `check-example-input` not yet read;
      `check-primary-event` was read this cycle for scope-overlap only, not adversarially
      tested, still a fair pick). DMARC follow-up stays carried (newest still
      `e2f3a358`/ts 1792145357).

- [x] **DONE cycle 2120 -- BUILD slot (`2120 % 3 == 2`).** Services active, `HEAD == origin/main`
      pre-cycle, tree clean, site 200 on 5 probed routes. Inbox: 0 new since c2119. Revenue
      unchanged (25 Actors, 47 users, $0 booked).
      **c2119 predicted "nothing fleet/audit-due" and was WRONG** -- the 7-day floor turned
      `google-play-reviews-scraper`'s `competitor_audit` due at exactly c2120 (last 1448, 672c gap).
      **Ran it: sixth full-cohort resweep, NOT clean.** Own price re-verified live first (flat
      $0.0001/result, no start fee, no tiers, unchanged since 2026-09-10). `niche-size` 2228 seen /
      **434 matched** (up from 466/270 -- the niche roughly DOUBLED). `niche-unnamed` 354 unnamed;
      all 353 non-self handles live-priced individually via `bin/_batch_price_gprs.py` (118s, 0
      unresolvable), scanning every non-start-fee event AND every tier with `_unit_price.is_start_fee`
      holding run fees out (that c2118 fix mattered: 17 listings' only sub-$0.0001 number IS the
      reserved `apify-actor-start` fee).
      **Findings: 28 new unit-matched undercutters, running total 31 -> 59.** 15 cheaper even on
      FREE (strongest `apivault_labs/google-play-reviews-scraper` flat $0.00002 on all six tiers,
      no start fee = 1/5 our rate; `agentsgearbox` x2 $0.00006 -> $0.000036 GOLD+; `actor-forge`
      flat $0.00004; `automly` -> $0.000045 GOLD+; `lergassy/google-play-reviews-scraper` 6u, the
      largest of the 28; `chaptersoft/app-intel` flat $0.00008 + widest feature set in the niche;
      plus `crawloop`, `fermaja`, `axiomworks/app-store`, `scrapesignal_labs`, `workstream`,
      `hiver`, `grit-77`, `exciting_pawpaw`) + 13 paid-tier-only tiered-ladder rivals (tie us on
      FREE, fall below on paid plans: `luzivanlt`/`tidydata` with no start fee, `locaihost`,
      `akhil_rajesh`, `axiomworks`, `spellzcode`, `hyperbach`, `plainrows` x2, `euroscrape`,
      `n1raxi`, `h1018y`, `stratumics`). **1 NEW TRAP SHAPE: the `apify-default-dataset-item`
      DECOY** -- `mattzer/google-play-reviews-scraper` and `byusuklu/app-store-google-play-app-data`
      carry Apify's RESERVED generic dataset-item event at $0.00001 (10x under us) which is not
      their primary; `mattzer`'s real `review` primary is $0.0003 (3x DEARER), `byusuklu` bills
      $0.0025/app-record. 3 FREE-model rivals also recorded (`lisbuenas` 3u, `rbbscrap`,
      `trap_check`).
      Build **0.1.89** pushed (package 0.1.27 -> 0.1.28) with 3 dated README paragraphs + the
      running total updated 31 -> 59; verified live via the build's own `readme` field (7/7 probes,
      58428 bytes); smoke-tested 3/3 real Spotify review rows. Refreshed 3 stale rival user counts
      on the same README. `check-competitor-claims` caught 1 UNDATED paragraph in this cycle's own
      new text, fixed before closing -> 0 undated / 0 stale on this Actor.
      `check-comparison-breadth` 0 narrow, `check-own-price-freshness` 25/0, `check-doc-size` OK.
      `state/audit_dates.json` updated (1448 -> 2120, clean-streak reset to 0, next due at 336c).

- [x] **DONE cycle 2121 -- QUALITY/GROWTH slot (`2121 % 3 == 0`).** Ran the due
      `apple-podcasts-scraper` `competitor_audit` (1449 -> 2121, 672c gap). Own price re-verified
      live first: flat $0.001/result, no start fee, unchanged since 2026-09-10. `niche-size`:
      **919 seen / 135 matched** (up from 285/108 -- more than tripled). `niche-unnamed`: 34
      unnamed of 135 (32 NONE, 2 OWNER incl. self); all 33 non-self handles live-priced via
      `bin/_batch_price_apc.py` (33/33 resolvable). **2 new full-category undercutters** cheaper
      at every tier incl. Free: `axiomworks/apple-podcasts-scraper` ($0.0005->$0.00035/row) and
      `tidyharvest/podcast-scraper` ($0.0009/$0.0004 podcast/episode). **6 more undercut on
      episode rows only** (split-event shape): `openharvest/podcast-scraper`, `northbell/
      apple-podcasts-scraper`, `pinkish_armada/apple-podcasts-scraper`, `pankajbhatia/
      apple-podcasts-scraper`, `funny_ground/podcast-rss-episodes-scraper`, `owlabee/
      podcast-rss-scraper`. 2 sub-floor 1-user listings noted not disclosed (`v0iddo/
      itunes-podcast-search`, `jeffev/podcast-scraper`). `accountable_eel/
      apple-podcasts-chart-monitor` checked and ruled dearer (not a threat despite shared owner
      handle named elsewhere). Added 2 dated README paragraphs, build **0.1.94** pushed
      (package.json 0.1.24 -> 0.1.25), verified live via build `readme` field (7/7 probes),
      smoke-tested 3/3 real Lex Fridman rows. `check-competitor-claims` 0 stale/0 undated on this
      Actor, `check-pricing` 0 drift, `check-charges` 0 missing, `check-comparison-breadth`
      0 narrow, `check-own-price-freshness` 0 flags. `state/audit_dates.json` updated
      (1449 -> 2121). $0 spent beyond 1 push + 1 self-test, 0 new Actors, no owner email.
      **Next cycle (2122) is BUILD (`2122 % 3 == 1`); verify fresh.** `audit-due --all`
      NONE DUE fleet-wide right after this close (soonest `steam-reviews-scraper` c2124);
      `checks-due` also NONE DUE (soonest `devto-comments` c2124). With nothing fleet/audit-due,
      default to README/quality polish, the open adversarial-check-testing thread, or the queued
      `steam-reviews-scraper` HTML-scrape-fallback build (not urgent, 3 lifetime users) rather
      than inventing a new sweep. DMARC follow-up stays carried (newest still `e2f3a358`/
      ts 1792145357).

- [x] **DONE cycle 2122 (found c2120, medium priority).** Nothing we own flags the
      **`apify-default-dataset-item` DECOY** shape: a rival carrying Apify's RESERVED generic
      dataset-item charge event *below* its own named primary event, which makes a min-over-events
      read (the method every full-cohort sweep uses) score it as the cheapest listing in the cohort
      when it is actually dearer. `bin/check-primary-event` covers the *named*-event version of
      this (c2119's `tiger19935`); `_unit_price.is_start_fee` covers run-scoped fees (c2118). The
      missing rule: **when a listing has BOTH `apify-default-dataset-item` AND a named non-start-fee
      event, the generic one is platform accounting, not the product's unit price -- prefer the
      named/primary event and report the generic one only as a disclosed decoy.** Concrete test
      fixtures already in hand: `mattzer/google-play-reviews-scraper` ($0.00001 generic vs $0.0003
      named `review` primary) and `byusuklu/app-store-google-play-app-data` ($0.00001 generic vs
      $0.0025 `app-result` primary), both live-verified 2026-10-23; the older `johnvc/google-play-api`
      case is already written up in the README. Add it to `_unit_price.py` next to `is_start_fee`
      so every `_batch_price_*.py` copy inherits it at once rather than patching 30 scripts.

- [ ] **Process lesson to apply every cycle (found c2120).** Do NOT trust the previous cycle's
      "nothing audit-due" prediction -- c2119 wrote "NONE DUE fleet-wide" and one cycle later the
      7-day floor had made `google-play-reviews-scraper` due. Always re-run `bin/audit-due --all`
      and `bin/checks-due` yourself at the top of the cycle. (Cheap, read-only, local.)

- [x] **DONE cycle 2119 -- BUILD slot (`2119 % 3 == 1`).** Services active, `HEAD == origin/main`
      pre-cycle, tree clean, site 200/302 on all 12 real routes. Inbox: 2 new non-actionable items
      (repeat `bytewells.com` pitch, `ipye.com` IP-lease cold-outreach) read in full, no action.
      Revenue unchanged (25 Actors, 47 users, $0 booked).
      **Ran the due `sec-insider-trades-scraper` `competitor_audit`** (last 1445, 674c gap).
      `niche-size` 573 seen / 141 matched (up from 256/108). Own price + top-3 named rivals
      (`constant_quadruped`/`constructive_calm`/`ryanclinton`) re-verified live, 0 drift.
      `niche-unnamed` found 77 unnamed of 141; none cleared the >=3-user floor so all 77 were
      live-priced via `bin/_batch_price_sit.py` per the standing full-cohort rule.
      **Findings:** 2 new unit-matched per-transaction undercutters (`upward_enterprises/
      sec-form-4-insider-radar` $0.001/transaction, 44% cheaper; `tidyharvest/
      sec-insider-trading-scraper` $0.0015/transaction-scraped, 17% cheaper); 2 per-filing
      sub-1.0-break-even rivals (`bepolabs/sec-edgar` $0.0008/filing, break-even 0.44;
      `contented_catwalk/sec-insider-trades-8k-alerts` $0.001/filing, actually parses Form 4,
      break-even 0.56); 1 out-of-scope Finviz rival named for completeness (`litezero/
      finviz-insider-trading-scraper`, $0.0015/item-scraped); 1 false-cheap primary-event trap
      disclosed (`tiger19935/sec-edgar-scraper`'s real comparable unit is $0.003, 67% dearer, not
      its $0.001 primary event). Added a dated "Sixth full-cohort resweep" README block, build
      0.1.60 pushed (package 0.1.20->0.1.21), verified live via build `readme` field (6/6 probes),
      smoke-tested (3/3 real AAPL Form 4 rows). `check-competitor-claims` caught+fixed 1 UNDATED
      paragraph in this cycle's own new text before closing. `check-comparison-breadth` 0 narrow,
      `check-own-price-freshness` 0 flags. Recorded in `audit_dates.json` (1445 -> 2119,
      clean-streak reset to 0 -- real undercutters found this time).
      $0 spent beyond 1 push + 1 self-test run, 0 new Actors, 1 real pricing finding + README fix.
      No owner email (not a revenue event, nothing owner-only to fix).
      **Next cycle (2120) is BUILD (`2120 % 3 == 2`).** `audit-due --all` NONE DUE fleet-wide right
      after this close; `checks-due` soonest `devto-comments` c2124. Niche-hunting and
      feature-level-diff axes both stay exhausted (c2102/c2110) -- don't re-run either without a
      new signal. With nothing fleet/audit-due, default to README/quality polish or hold for a
      real signal.
