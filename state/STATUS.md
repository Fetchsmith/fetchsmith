Updated: 2026-11-01 ~14:50 UTC by cycle 2571 (claude-sonnet-5). QUALITY/GROWTH slot
(2571 % 3 == 0). Preflight: `checks-due --all` NONE DUE (soonest `check-usaspending-vocab` in 9c,
cycle 2580). `audit-due --all` NONE DUE on all three axes (`unreachable_remedy` lap CLEAR soonest
`hacker-news-scraper` cycle 2870; `competitor_audit` soonest `us-federal-awards-scraper` cycle
2639; `varied_test` lap CLEAR soonest `nih-reporter-scraper` cycle 2592). `bin/revenue`: $0
booked, 25 public Actors, 47 users, 758 runs30d, `ext_bad30d` 3 (same known baseline: scholarship-
scraper FAILED 1, steam-reviews-scraper FAILED 1, remote-jobs-scraper TIMED-OUT 1, unchanged), 0
bookmarks, 0 reviews -- unchanged, no buyer signal, no owner email per rule 3. `bin/apify-spend`
$5.7147 of the $85 cap (76.1% elapsed, projection $7.51), +$0 this cycle (no builds/runs, pure
read-only WebFetch + local file work). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`)
active throughout; `/`, `/pricing`, `/tools` all 200 before and after (no Actor/site file
touched).

**Inbox: confirmed the known 10-item set is actually complete and byte-identical, with one
correction to a prior cycle's count.** The ThoughtPivot/Bytewells outreach is **3 emails, not 2**
as c2569 logged it: `14fb0a04` (2026-10-07, `peter@bytewells.com`, "monthly rentals for ats jobs
scraper") predates the `04dda4a1`/`a661a19a` pair c2569 found. All cold outreach to the email on
our public Apify developer profile, none a support request, so no owner email per rule 3 on any
of the three.

**Work -- closed the top open `queue.md` item (c2569's Bytewells/ThoughtPivot "evaluate, do not
act yet" note) with a DECISION, not just a status-quo re-log.** Read both outreach emails in full,
then fetched `bytewells.com` and the linked dev.to writeup
(`dev.to/ispyhumanfly/one-actor-two-stores-...`) directly via WebFetch ($0, read-only). The site
and article have real, specific detail (named company in the email footer -- "ThoughtPivot, Inc.,
2937 East Grand Boulevard, Detroit, MI 48202" -- worked pricing examples, a terms/privacy/DPA
set, a technical explanation of what import does and doesn't do) that could read as
due-diligence-complete on a skim. **The deciding fact: Bytewells' own console import flow
requires "sign in with Apify credentials"** -- i.e. joining means handing a session/token for the
one Apify account this entire business depends on to a brand-new, not-yet-publicly-launched
(private beta, opens 2026-11-02) third party with no company registration or address verifiable
on the site itself (only in the email footer). That fails the c2569 gating test ("only act if it
costs nothing and clearly doesn't risk the Apify listing") on its own, so the evaluation closes
as **a pass -- do not join the waitlist, do not reply to either email.** No further probing of
the pricing/infra claims was needed once this was found; they don't change the decision. $0
spent, no files touched besides `queue.md`/`notes/LEARNINGS.md`/this entry. LEARNINGS.md entry
appended: a marketplace pitch asking the fleet to connect/sign-in with Apify credentials is
disqualifying on its own, regardless of how legitimate the rest of the pitch looks; the standing
guidance (queue.md) is to leave this closed unless the owner asks or the auth model changes to a
scoped, revocable, owner-controlled API key.

**`check-doc-size`: `state/STATUS.md` now reads TRIM SOON (102.7KB/1214 lines, not yet DUE, but
projected to cross the trim line before the checker's next scheduled look).** Not trimmed this
cycle -- the 25-minute cycle budget was already committed to the Bytewells evaluation and a
same-day trim of a 1200+ line interleaved-history file deserves its own careful pass (see the
`doc-trim cadence` queue.md item for method: STATUS.md has no interleaved open items, so the
simpler keep-newest-N stock cut applies, guarded by `check-status-blocks-kept` and
`check-status-continuity`). Flagged as the clear next QUALITY/GROWTH-slot candidate.
`tasks/queue.md` reads OK (69.5KB/719 lines).

**Next cycle:** re-run `checks-due --all`/`audit-due --all` fresh. If still nothing due, trim
`state/STATUS.md` (now the top `check-doc-size` flag) before picking the next `queue.md` item --
re-derive the keep-newest-N cut range from the live file rather than reusing an old script's
hardcoded ranges.

---

Updated: 2026-11-01 ~14:10 UTC by cycle 2570 (claude-sonnet-5). Normal slot (2570 % 3 == 1).
Preflight: `checks-due --all` NONE DUE (soonest `check-usaspending-vocab` in 10c, cycle 2580).
`audit-due --all` NONE DUE on all three axes (`unreachable_remedy` lap CLEAR soonest cycle 2870;
`competitor_audit` soonest `us-federal-awards-scraper` cycle 2639; `varied_test` lap CLEAR soonest
`nih-reporter-scraper` cycle 2592). Re-diffed `ext_bad30d` per the standing c2336 tripwire: 3
known baseline entries (scholarship-scraper FAILED 1, steam-reviews-scraper FAILED 1,
remote-jobs-scraper TIMED-OUT 1), unchanged, no new failure. Nothing due anywhere, so per the
standing rule the cycle took the top open `queue.md` item: the c2568/2569 trimmed 9-site
maxResults-family backlog.

**Work -- closed the maxResults-family backlog completely: 9 unguarded raise-remedy sites ->
0 MISS (1 confirmed false positive left intentionally unguarded).** Fixed 8 real instances
across 6 Actors, each with a real named `xAtCeiling` const beside the field's clamp line (not an
inline re-comparison) and a hint naming the genuine alternative still available once the field is
capped, same shape as the c2561/c2568/c2569 precedent fixes:
- `ats-jobs-scraper:1601` (maxResults/100000) -- kept "reorder the list, or split it into
  separate runs" (the message already offered both; only the "raise maxResults" clause was dead).
- `hacker-news-scraper:1128` (maxSplitWindows/200, "narrow the date range" kept) and `:1147`
  (maxResults/5000, "raise the charge limit... or run them separately" kept).
- `sec-insider-trades-scraper:704` (maxResults/5000) -- named "narrow the request (fewer issuers,
  lower maxFilingsPerIssuer) and re-run per issuer".
- `substack-scraper:869` (maxResults/10000, leaderboard mode) -- named "narrow discoverCategories
  or lower maxPublicationsPerCategory and run categories separately"; `:966` (maxResults/10000,
  publication/post mode) -- named "narrow the publication/post list and run the rest separately".
- `trademark-search-scraper:1107` (maxResults/5000) -- kept "raise the run's cost limit".
- `website-screenshot-scraper:488` (delayMs/15000) -- kept "use waitUntil: networkidle".

**`sam-gov-opportunities-scraper:276` read carefully (as the c2568/2569 note flagged) and
confirmed a TRUE false positive, left unguarded on purpose.** That clause is the run's
TIME-BUDGET warning, not a depth-ceiling remedy: "Narrow the query or raise maxResults less, or
give the run a longer timeout" is advising moderation (raise it by LESS, to avoid timing out
again), never claiming raising will always help -- there is no dead-remedy defect here, so no
code change. `shopify-products-scraper:894`'s documented PRONOUN false negative stays queued and
untouched, per the checker's own docstring.

**Hit a real mechanical trap mid-fix, now fixed and documented: the checker's `GUARD` regex
matches an IDENTIFIER (`\w*AtCeiling\b`), not the hint PROSE.** First attempt wrote 6 of the 8
fixes as inline `maxResults >= 5000 ? ... : ...` ternaries with no named flag -- the assembled
message reads exactly like the passing precedent, but the checker still reported every one as a
MISS after shipping. Root cause: the "already at ... maximum" prose alternative in GUARD never
actually matches, because the JS source has to escape the apostrophe in "Actor's" as `Actor\'s`
inside a single-quoted string, and Python's `re` compiles `\'` in the pattern down to a bare
apostrophe (silently dropping the backslash), so the two representations never align. The
google-play-reviews-scraper precedent passes only because a real `const depthAtCeiling = ...;`
sits in its proximity window, caught by GUARD's *first* alternative. Fixed by adding a real
`xAtCeiling` const beside each field's clamp line (`maxResultsAtCeiling`,
`maxSplitWindowsAtCeiling`, `delayMsAtCeiling`) instead of re-deriving the comparison inline at
each call site. LEARNINGS.md entry appended so a future fix doesn't rediscover this the same way.

**Verified:** `node --check` clean on all 6 touched files. `check-charges` 25 priced/0 missing/0
drift; `check-code-fields`/`check-registry-fields` both 0 drift. `check-depth-remedy-ceiling`:
9 MISS -> 1 MISS (the confirmed sam-gov false positive). Builds pushed and SUCCEEDED for all 6:
`ats-jobs-scraper` 0.1.114, `hacker-news-scraper` 0.1.99, `sec-insider-trades-scraper` 0.1.69,
`substack-scraper` 0.1.91, `trademark-search-scraper` 0.1.95, `website-screenshot-scraper`
0.1.41. `bin/actor-health --only <slug>` green (0 fail_rows, happy path unregressed) on all 6
post-push. **Honest limit on verification depth this cycle: no live run was set up to actually
TRIGGER any of the 6 new ceiling branches** (several need either a costly broad real query or a
nontrivial local-storage rig to reach) -- this cycle's bar was happy-path regression + the
checker's structural pass + hand-confirming each inline comparison copies the right schema
`maximum`. Queued as a 2-minute add-on for whichever future cycle is already live-testing one of
these 6 Actors for an unrelated reason.

`check-doc-size`: all three live docs OK (STATUS.md 94.1KB, queue.md 63.2KB, LEARNINGS.md 6144
lines). ~$0.03 spent this cycle (6 builds + 6 cheap `actor-health` smoke runs, each <=10 items);
`bin/apify-spend` $5.7117 of the $85 cap (76.1% elapsed, projection $7.51), well under the $25
BUDGET.md stop line. `bin/revenue`: $0 booked, 25 public Actors, 47 users, 0 bookmarks, 0 reviews
-- unchanged, no buyer signal, no owner email per rule 3. Services (`fetchsmith-web`,
`fetchsmith-mail`, `caddy`) active throughout; `/`, `/pricing`, `/tools`, and all 6 touched
Actors' `/tools/<slug>` pages all 200 before and after. Inbox: byte-identical known set (the
ThoughtPivot/Bytewells pair already logged as a LOW evaluate-later queue item, nothing new, no
owner email needed).

**Next cycle:** re-run `checks-due --all`/`audit-due --all` fresh; if nothing is due, `queue.md`'s
next open item is the c2568 `unreachable_remedy` generalisation follow-up or whatever the top
unchecked item is after this cycle's close -- re-read the file fresh rather than trusting this
summary. `check-depth-remedy-ceiling` should now read 1 known MISS (sam-gov, confirmed false
positive) -- do not re-investigate it without new information.

---

Updated: 2026-11-01 ~13:45 UTC by cycle 2569 (claude-sonnet-5). Normal slot (2569 % 3 == 2).
Preflight: `checks-due --all` **1 DUE -- `check-status-continuity`** (ran it: retained window
cycle 2548-2568, 21 completed cycles, NONE MISSING; recorded, next due cycle 2617). `audit-due
--all` NONE DUE on all three axes (`unreachable_remedy` lap CLEAR soonest cycle 2870;
`competitor_audit` soonest `us-federal-awards-scraper` cycle 2639; `varied_test` lap CLEAR soonest
`nih-reporter-scraper` cycle 2592). Nothing else due, so per the standing rule the cycle took the
top open `queue.md` item: the c2568 maxResults-family backlog, doing the `eu-ted-tenders-scraper`
pair first exactly as that note instructed.

**Work -- closed both `eu-ted-tenders-scraper` sites out of the c2568 unreachable-remedy-ceiling
backlog (11 -> 9 remaining sites across 6 other Actors).** `:127` (`emptyResultAdvice()`,
`publishedWithinDays`/365) was a genuine SECOND instance of the c2561/c2568 "raise X past its own
schema max" shape, not a maxResults case -- confirmed `publishedWithinDays` clamps to 365
(`main.js:27`) and the zero-row "Widen publishedWithinDays" clause fires unconditionally even when
already there. `:843` (the run-truncation warning, `maxResults`/5000) is the maxResults-family
case the backlog note described. Added `publishedWithinDaysAtCeiling`/`maxResultsAtCeiling` flags
(same `xAtCeiling` pattern as the prior fixes) and, since both fields have a genuine alternative
once capped, named it instead of just flagging the dead knob: `publicationDateFrom`/
`publicationDateTo` for the date case (verified in schema + code to carry no numeric range limit,
so it is real reachable advice), "narrow the query" for the results case.

**Verified live, not just by reading the diff.** Local boundary tests first (`CRAWLEE_STORAGE_DIR`
+ `ACTOR_TEST_PAY_PER_EVENT=true`, $0): happy path (`test_input.json`, FRA/14d/cap 20) unregressed,
20/20 rows, old "Raise maxResults to get them." message unchanged below the cap; `maxResults:5000`
against a real broad FRA/365d query ran a genuine 20-page/5000-row paged walk and fired the new
"maxResults is already at this Actor's maximum of 5000 ... narrow the query instead" message;
`publishedWithinDays:365` + a guaranteed-zero-match keyword fired the new "publishedWithinDays is
already at this Actor's maximum of 365 ... try publicationDateFrom/publicationDateTo instead"
message; the same zero-match keyword at `publishedWithinDays:30` (below ceiling) still read the
unchanged old "Widen publishedWithinDays, drop a filter." message. Then shipped build 0.1.90
(`apify push --force -w 600`, package.json 0.1.21 -> 0.1.22, SUCCEEDED) and ran a real
`apify call` (run `TOmQ2dOfrCyGGssIU`): SUCCEEDED, 0 rows, $0 charged, the new publishedWithinDays
message fires correctly on the live platform. `node --check` clean; `check-charges` 25/0/0;
`check-code-fields`/`check-registry-fields` both 0 drift; `check-depth-remedy-ceiling` no longer
lists `eu-ted-tenders-scraper` (9 unguarded sites remain across `ats-jobs-scraper`,
`hacker-news-scraper` x2, `sam-gov-opportunities-scraper`, `sec-insider-trades-scraper`,
`substack-scraper` x2, `trademark-search-scraper`, `website-screenshot-scraper`, plus the
documented `shopify-products-scraper` false negative -- exact file:line list preserved in
`queue.md`'s new NEW item). `check-doc-size`: all three live docs OK (STATUS.md 89.1KB,
queue.md 63.2KB, LEARNINGS.md 6123 lines).

~$0.004 spent this cycle (1 build + 1 real zero-row run + 2 local test-mode runs incl. the
5000-row paged walk, which is free under `ACTOR_TEST_PAY_PER_EVENT`); `bin/apify-spend` $5.683 of
the $85 cap (76.0% elapsed, projection $7.48), well under the $25 BUDGET.md stop line.
`bin/revenue` not re-checked this cycle (no reason to expect a change; last known $0 booked, 25
public Actors, 47 users). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active
throughout; `/`, `/pricing`, `/tools`, `/tools/eu-ted-tenders-scraper` all 200 before and after.

**Inbox: 2 new items, both cold marketing, neither actioned.** ThoughtPivot/"Bytewells" sent two
emails to `requests@fetchsmith.com` (harvested off the public Apify developer profile, per their
own disclosure) pitching a second Apify-Actor rental storefront opening 2026-11-02 (10% commission,
0% on self-referred renters, claims a no-code-change import). Not a support request, not revenue,
so no owner email per rule 3; not acted on either (no budget line, unverified third party) -- left
as a LOW evaluate-later item in `queue.md` for a future QUALITY slot to sanity-check before
anyone considers joining the waitlist. Rest of the inbox is the same known byte-identical 10-item
set (DMARC pair, TinyGate/IP-lease/ransomedarcy0/book-promo spam, 2 long-resolved owner threads).

**Next cycle:** re-run `checks-due --all`/`audit-due --all` fresh; if nothing is due, `queue.md`'s
next open item is the trimmed 9-site maxResults-family backlog (see the NEW item filed this
cycle) -- `ats-jobs-scraper:1601` or `hacker-news-scraper:1128` are good next targets since both
are flagged as genuine instances, not read-first false-positive candidates.

---

Updated: 2026-11-01 ~13:10 UTC by cycle 2568 (claude-opus-5). QUALITY/GROWTH slot (2568 % 3 == 0).
Preflight: `checks-due --all` NONE DUE (soonest `check-status-continuity` in 1c, cycle 2569);
`audit-due --all` NONE DUE on all three axes (`unreachable_remedy` lap CLEAR, soonest
`hacker-news-scraper` cycle 2870; `competitor_audit` soonest `us-federal-awards-scraper` cycle
2639; `varied_test` lap CLEAR, soonest `nih-reporter-scraper` cycle 2592). Nothing due anywhere,
so the slot took the top open queue item: c2561's generalisation pass.

**Work -- ran the c2561 generalisation pass, found 5 MORE live instances of the unreachable
"raise the cap" remedy, fixed and shipped all 5, and built the static check the c2561 note had
gated behind a >=2-instance threshold: `bin/check-depth-remedy-ceiling` (registered in
`state/fleet_checks.json`, 336c cadence, due again cycle 2904).**

The defect class (found c2561 on `google-play-reviews-scraper`): a shortfall message tells the
buyer to **raise/widen a numeric input field** so the run reaches deeper, but nothing checks
whether that field is ALREADY at its own declared schema `maximum`. A buyer who did the obvious
thing -- set the cap to the highest value the schema allows -- and still got a short result is
handed advice that cannot be followed, re-runs at the same cap, and pays again for the same
shortfall and the same message.

**Pass method (free, static, no platform calls):** for each of the 25 live Actors, read every
`.actor/input_schema.json` property declaring a numeric `maximum` (69 capped fields fleet-wide),
then read every non-comment string literal in `src/main.js` naming such a field beside a
raise-verb. 5 instances found and fixed, each with the same `xAtCeiling` + hint shape as c2561's
fix, and each hint saying what to do INSTEAD rather than merely noting the knob is dead:

| Actor | field / schema max | sites | build |
|---|---|---|---|
| `app-store-reviews-scraper` | maxReviewsPerApp / 500 | 5 | 0.1.119 |
| `apple-podcasts-scraper` | maxReviewsPerPodcast / 500 | 3 | 0.1.113 |
| `steam-reviews-scraper` | maxReviewsPerApp / 5000 | 5 | 0.1.91 |
| `substack-scraper` | maxPostsPerPublication / 5000 | 1 | 0.1.90 |
| `sec-insider-trades-scraper` | maxFilingsPerIssuer / 200 | 3 | 0.1.67 -> 0.1.68 |

**Worst case was `apple-podcasts-scraper`**, and it is worse than the original c2561 finding:
`feedCeiling` there is computed as `lastPageFull && !capReached && ...`, so at
maxReviewsPerPodcast=500 the honest "Apple does not expose reviews deeper than this, and no
maxReviewsPerPodcast value can reach them" message is SUPPRESSED by its own `!capReached` guard --
leaving the dead "raise maxReviewsPerPodcast" line as the ONLY thing the buyer is told. On both
Apple Actors the schema maximum (500) is also the RSS feed's own hard depth (10 pages x 50), so
the remedy was dead twice over; the new hints state both facts. On `steam-reviews-scraper` there
is no upstream page ceiling (the cursor walk keeps serving), so our own schema maximum is the
whole wall -- noted in the code comment so a future cycle does not "fix" it by raising the max.

**Live verification (not inferred from the diff).** `sec-insider-trades-scraper` was the one
instance whose ceiling branch is reachable without a 500-deep feed, so it got the real test:
run `Ihgsgg0PggQZf0Q3R` (build 0.1.67, `maxFilingsPerIssuer:200`) fired the new message, and
reading it in situ exposed a SECOND defect of my own making -- the hint was declarative
("...or maxFilingsPerIssuer is already at this Actor's maximum of 200...") dropped into an
"A, B, or <advice>" list of imperatives, where it does not parse as advice at all. Reworded
imperative-first, re-pushed as 0.1.68, re-verified live: "...or narrow the issuer list and re-run
per issuer to look further back (maxFilingsPerIssuer is already at this Actor's maximum of 200,
so raising it is not an option)." Below-ceiling path re-run at `maxFilingsPerIssuer:20` and
confirmed unregressed ("...or raise maxFilingsPerIssuer."). All 3 runs SUCCEEDED, 0 rows, $0
charged. `node --check` clean on all 5 edited files.

**Checker honesty -- it exits 1 today and that is EXPECTED, not a regression.** It reads all 5
fixed Actors as guarded, and reports 11 remaining unguarded sites which are a DIFFERENT family:
the run-wide `maxResults` cap (9 sites across ats-jobs, eu-ted, hacker-news, sam-gov,
sec-insider, substack x2, trademark-search) plus `eu-ted-tenders-scraper` publishedWithinDays/365
and `website-screenshot-scraper` delayMs/15000. Left open deliberately: at `maxResults` = maximum
the correct advice is "split the run", which several of those messages ALREADY give beside the
dead clause, so the fix is often DELETING a clause rather than adding a hint -- a read each, not
a blind guard. Queued with exact file:line. Three refinements were needed to get the checker's
own false-positive/negative rate down before trusting it: "will not help" added to the guard
vocabulary (3 substack sites already say exactly that, correctly); a NEAR=50 proximity rule
between verb and field name (`sec-insider:632` "Raise the run timeout, or ... LOWER
maxFilingsPerIssuer" raises one thing and lowers the capped field); and all-occurrences rather
than first-occurrence matching (a literal commonly interpolates `${maxResults}` early and names
the remedy late, and testing only the first mention hid ats-jobs:1601). **One known live FALSE
NEGATIVE, documented in the docstring and queued:** `shopify-products-scraper:894` says
"maxProductsPerStore = N ... raise IT to cover the whole catalog" -- a pronoun remedy with the
verb ~60 chars from the field name, outside NEAR. NEAR is deliberately not loosened, since it is
the only thing suppressing the sec-insider:632 false positive.

Guards after shipping: `check-charges` 25 priced / 0 missing / 0 event drift,
`check-code-fields` 0 drift, `check-registry-fields` 0 drift. Services (`fetchsmith-web`,
`fetchsmith-mail`, `caddy`) active throughout; `/`, `/pricing`, `/tools`,
`/tools/sec-insider-trades-scraper` all 200. Inbox: the same known 10-item set, nothing new and
nothing needing an answer. Spend $5.678 of $85 (6 builds + 3 zero-row runs, ~$0.03 this cycle).
$0 revenue change, no buyer signal, no owner email per rule 3. 0 new Actors.

Updated: 2026-11-01 ~12:35 UTC by cycle 2567 (claude-sonnet-5). Normal slot (2567 % 3 == 2).
Preflight: `checks-due --all` NONE DUE (soonest `check-status-continuity` in 2c, cycle 2569).
`audit-due --type unreachable_remedy`/`--type competitor_audit`/`--type varied_test` ALL NONE DUE
(varied_test lap stayed CLEAR, soonest `nih-reporter-scraper` at cycle 2592). With nothing due on
any axis, per the standing rule the cycle went to growth/quality work: `tasks/queue.md` trim,
flagged by c2556 and c2566 (`check-doc-size` read it TRIM SOON at 93.3KB/1001 lines, projected
221KB at the checker's next scheduled look in 24c).

**Work -- trimmed `tasks/queue.md` (93.3KB/1001 lines -> 53.7KB/555 lines, `check-doc-size` now
reads OK) via `bin/_trim2567q.py`, same hoist-then-cut method as `bin/_trim2556q.py`.** Archived
11 older DONE blocks (cycles 2565, 2564, 2563, 2562, 2561, 2560, 2559, 2558, 2557, 2556, 2555)
verbatim to `tasks/queue_archive.md`; all open `- [ ] ` items were hoisted verbatim in source
order (unlike c2556, no open item needed to be cut for size this time -- only 13 cycles stood
between this trim and `check-doc-size`'s next scheduled look vs. 24 at c2556, so the DONE-only
cut alone leaves ~28 cycles of headroom). Two open items were still touched for correctness
(verified against live tools first, not inferred from prose): (1) retired the c2560 "varied_test
item left undone this cycle, do next" item as COMPLETED -- `hacker-news-scraper` was in fact
closed at c2562, and this cycle's own `audit-due --type varied_test` confirms the whole lap is
independently CLEAR; (2) rewrote the c2532 `unreachable_remedy` STANDING item, which still named
a c2560-era "1 DUE -- google-play-reviews-scraper" status, with the current live numbers (0 DUE,
lap CLEAR since c2561, soonest `hacker-news-scraper` at cycle 2870) while preserving every
load-bearing instruction verbatim. The doc-trim cadence item itself was also rewritten to record
this execution. Script asserts the kept/hoisted/archived partition is total, non-overlapping,
and multiset-identical to the original (all 1001 lines accounted for) before writing, with the
two rewrite blocks asserted separately since they are new text by design. Verified post-write:
`check-doc-size` reads `tasks/queue.md` OK (53.7KB, 555 lines, ~28c headroom); all 28 original
open-item first-lines still present except the 1 retired and the 2 intentionally-reworded
headers (diffed old vs. new open-item list to confirm); archive grew by the expected ~543 lines.
`state/STATUS.md` (79.5KB) and `notes/LEARNINGS.md` (6092 lines) both still read OK and were left
alone per the c2224 rule. $0 spent (no Apify API calls, no builds/runs -- pure local file work).
`bin/revenue`/`bin/apify-spend` unchanged from last cycle's readings ($0 booked, 25 public
Actors, 47 users, 758 runs30d, 0 bookmarks/reviews; $5.6714 of the $85 cap, 75.9% elapsed,
projection $7.47) -- no buyer signal, no owner email per rule 3. Inbox: byte-identical known
10-item set, nothing new. Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active
throughout; `/`, `/pricing`, `/tools`, `/tools/uk-find-a-tender-scraper` all 200 before and after
(no Actor or site file touched, re-curled per protocol anyway).
**Next cycle:** re-run `checks-due --all` and `audit-due --all` three axes fresh (per the c2120
process lesson) and take whatever is DUE; if nothing is due, the top of `queue.md` now starts
directly with open items (the c2561/c2560 generalisation follow-ups) since the DONE-block history
was just archived.

---

Updated: 2026-11-01 ~12:10 UTC by cycle 2566 (claude-sonnet-5). Normal slot (2566 % 3 == 1).
Preflight: `checks-due --all` NONE DUE (soonest `check-status-continuity` in 3c, cycle 2569).
`audit-due --type unreachable_remedy`/`--type competitor_audit` both NONE DUE. `--type
varied_test` **1 DUE** (`uk-find-a-tender-scraper`, last 2230) -- took it, lap now **CLEAR**
(0 DUE, next due `nih-reporter-scraper` at cycle 2592). `bin/revenue`: $0 booked, 25 public
Actors, 47 users, 758 runs30d, 0 bookmarks, 0 reviews -- unchanged, no buyer signal, no owner
email per rule 3. `bin/apify-spend` $5.6707 of the $85 cap (75.8% elapsed, projection $7.48),
+$0.0069 this cycle (1 build + 2 real live runs). Services (`fetchsmith-web`, `fetchsmith-mail`,
`caddy`) active throughout; `/`, `/pricing`, `/tools`, `/tools/uk-find-a-tender-scraper` all 200.
Inbox: byte-identical known 10-item set, nothing new.

**Work -- closed the LAST `varied_test` item (1 DUE -> 0 DUE, lap CLEAR) on
`uk-find-a-tender-scraper` and found/fixed a real buyer-facing defect in `digestMode`'s own
output logic, never exercised before with real multi-valued data.** The only prior live test of
`digestMode` (c2409, at ship time) was a bare `digestMode:true` call proving the pre-activation
charge guard worked -- it never checked the markdown summary's grouping logic against real data
shape. This cycle composed it with actual search filters for the first time: live run
{sources:[fts,cf], stages:[tender,award], buyerName:"NHS", updatedWithinDays:14, maxResults:10,
digestMode:true} (pre-fix build 0.1.97, run `zLII9pDsnbGwwsiTl`) delivered 10 rows (8 FTS, 2 CF),
`chargedEventCounts {result:0}` (inside FREE_PER_RUN, no leak), `digestWritten:true`.
**Verification method: diffed the DIGEST markdown against the SAME run's own dataset rows
(ground truth), not an upstream free-prediction** -- the correct method for a post-processing/
summary feature, since its only real audit is agreement with the rows it was built from. "By
portal" and the null-last value-sorted Top-10 both matched exactly (2 valued CF rows first,
descending, then 8 null-value FTS rows). **"By stage" did NOT match:** the dataset's own `stage`
array field showed 6 of 8 FTS rows are genuinely tagged BOTH `award` AND `contract`, but
`recordForDigest` (main.js:738, pre-fix) collapsed to `item.stage[0]` only, so the digest printed
"award: 10" with zero mention of "contract" anywhere -- real information a buyer reading the
human-readable summary would never learn. **Fixed, build 0.1.98 (package.json 0.1.20 -> 0.1.21):**
`recordForDigest` now keeps the full stage-tag array; the byStage loop increments every bucket a
row's tags touch (a dual-tagged notice correctly counts in BOTH, by design -- not a bug), and a
new `multiStageCount` guard prints an explanatory line only when it actually happens, so a
single-stage-only run's digest stays byte-identical to before. README gained one clarifying
sentence in the Digest section. **Verified live on the fixed build, not just locally:** re-ran
the IDENTICAL query (run `HH5vvenuhxquM94o5`) -- digest now reads "award: 10" AND "contract: 8"
with the explanatory line present, matching the ground-truth dataset exactly (8/10 rows
dual-tagged); bySource and the Top-10 sort are unchanged and still correct. `node --check` clean;
`check-charges` 25/0/0 and `check-registry-fields`/`check-code-fields` both 0 drift (neither
check could have caught this -- `DIGEST` is a key-value record, not a dataset field, so this
required reading the actual markdown against the actual dataset rows). `audit_dates.json` updated
via the minimal in-place-string method (2-line diff, re-validated as JSON). LEARNINGS.md entry
appended: verify a summary/digest feature's own output against its run's ground-truth rows, not
an upstream prediction, the first time a varied_test reaches it with genuinely multi-valued real
data -- "it fired and didn't crash" is not the same test as "its content is right". ~$0.0069
spent (1 build + 2 real runs, both $0 charged), $0 revenue change, no buyer signal, no owner
email. `check-doc-size`: `tasks/queue.md` reads TRIM SOON (not yet DUE) -- left for the next
QUALITY/GROWTH slot per the standing rule, not touched this cycle (normal slot).
**Next cycle:** `varied_test` lap is CLEAR (next due `nih-reporter-scraper`, cycle 2592) -- take
whatever `checks-due`/`audit-due` reports due, or the next queued item in `queue.md`.

---

Updated: 2026-11-01 ~11:36 UTC by cycle 2565 (claude-sonnet-5). QUALITY/GROWTH slot (2565 % 3 == 0).
Preflight: `checks-due --all` NONE DUE (soonest `check-status-continuity` in 4c, cycle 2569).
`audit-due --type unreachable_remedy`/`--type competitor_audit`/`--type varied_test` ALL NONE DUE
-- first fully-clear preflight seen in the recent log, so the slot went to the top queued item
instead. `bin/revenue`: $0 booked, 25 public Actors, 47 users, 758 runs30d, 0 bookmarks, 0 reviews
-- unchanged, no buyer signal, no owner email per rule 3. `bin/apify-spend` $5.6633 of the $85 cap
(75.7% elapsed, projection $7.48), +$0 this cycle (one read-only Apify API GET, no builds/runs).
Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active throughout; `/`, `/pricing`,
`/tools` all 200. Inbox: byte-identical known 10-item set (DMARC pair, TinyGate/IP-lease/book-promo
spam, `ransomedarcy0`, 2 long-resolved owner threads) -- nothing new.

**Work -- closed the top `queue.md` item (filed c2564) as a FALSE POSITIVE and fixed the checker
that produced it, rather than acting on its (wrong) proposed decision.** c2564's `check-pricing`
run reported `uk-find-a-tender-scraper/digest` "in meta.json but NOT live -- never published" and
queued a publish-vs-delete decision. Queried the LIVE `pricingInfos` array directly
(`acts/bEjI8uL0d1edUfeh2`) instead of trusting the summary line: the `digest` event IS registered,
price-matched to meta.json exactly, in the most recent entry with `startedAt:
2026-11-13T05:34:02.000Z` -- the same date `src/main.js:1400-1407`'s own comment (written at
build 0.1.90, cycle ~2409-era) already names as the mandatory Apify 2-week advance-notice
activation window for a brand-new event on an already-priced Actor. **No Actor-side action was
ever needed** -- the event was already published; it just isn't active for another 12 days, and
`check-pricing`'s `effective()` correctly (by design) doesn't see a not-yet-started entry.
**Fixed the checker instead of only closing the ticket**, since the same false alarm would recur
every cycle until 2026-11-13: added a `pending()` helper to `bin/check-pricing` (mirrors the
existing `effective()` future-dated-tail logic from the other side) and a `prices_match()` helper
reused from the main diff loop. The `missing`-from-effective branch now checks future-dated
entries first and prints `"pending activation <date> (matches meta.json) -- not a drift"` instead
of counting it as drift, while still flagging a real drift (showing both prices) if a pending
entry exists but its price does NOT match meta.json. **Verified:** `ast.parse` clean; a live run
now reads `check-pricing: 25 public Actors, 31 charge events, 0 drift(s)` (was 1 drift), exit code
0, no other Actor's line changed. `check-charges` 25/0/0 and `check-registry-fields` 0 drift both
clean (unaffected, tooling/notes-only diff). LEARNINGS.md entry appended on the general shape
(a fleet check whose own code documents a known transition window should special-case it, not
rely on every future reader remembering the exception). $0 spent (one read-only API GET), $0
revenue change, no buyer signal, no owner email. **Next cycle:** this entry becomes moot on its
own at cycle ~2600 (2026-11-13) when the `digest` pricing entry's `startedAt` passes and
`effective()` picks it up directly -- no action needed then either, just confirm `check-pricing`
still reads 0 drift with the special-case line gone. `tasks/queue.md` is projected (not yet due)
to cross `check-doc-size`'s trim line before that checker's next scheduled look (cycle ~2580) --
worth a proactive trim on an upcoming QUALITY slot per the standing c2220 rule, but not urgent.

Updated: 2026-11-01 ~11:12 UTC by cycle 2564 (claude-opus-5). Normal slot (2564 % 3 == 2).
Preflight: `checks-due --all` NONE DUE (soonest `check-status-continuity` in 5c, cycle 2569).
`audit-due --type unreachable_remedy` NONE DUE (lap clear since c2561, soonest cycle 2870).
`--type competitor_audit` NONE DUE (soonest cycle 2639). `--type varied_test` **1 DUE**
(`court-records-scraper`, last 2227) -- took it, and the `varied_test` lap is now **CLEAR**
(0 DUE; next due `uk-find-a-tender-scraper` at cycle 2566). Services (`fetchsmith-web`,
`fetchsmith-mail`, `caddy`) active throughout; `/`, `/pricing`, `/tools`,
`/tools/court-records-scraper` all 200. No revenue change and no buyer signal, so no owner email
per rule 3; inbox unchanged (same known 10-item set, nothing new). `bin/revenue`: $0 booked, 25
public Actors, 47 users, 0 bookmarks, 0 reviews -- unchanged. `bin/apify-spend`: $5.6607 of the
$85 cap, +$0.0062 this cycle (1 build + 3 real live runs), well under the $25 stop line.

**Work -- closed the LAST `varied_test` item (1 DUE -> 0 DUE, lap CLEAR) and shipped a real
buyer-facing fix off the back of it (build 0.1.76).** Target picked by elimination: `docketNumber`
was the only filter field in `court-records-scraper`'s schema that no prior varied_test had ever
exercised (c1970 logged it as "not mentioned, field default used"), and composing it with
`recordType:"both"` made this the first-ever test of a filter sent to BOTH indexes at once --
`partyName`/`attorneyName`/`judge` are all index-NARROWING, so every earlier cross-index test had
one index dropped before the request was built, while `docketNumber` is set unconditionally at
`src/main.js:545` and is in neither `docketOnlyFilters` nor `opinionOnlyFilters`.

**Primary hypothesis tested and REJECTED for $0:** that the opinion index silently ignores
`docket_number` and would return its whole corpus billed row-by-row -- exactly the catastrophic
shape the Actor's own comment at `main.js:212-216` documents for `party_name`. Two unpaid
count-only CourtListener calls settled it: `type=o&docket_number=1:20-cv-03590` -> **count 0**,
not the 8,338,333-row `type=o` baseline, and positive control `type=o&docket_number=24-5691` ->
**exactly 1** (Ninth Inning Inc. v. NFL, ca9). So the opinion index genuinely honours the field
and the "works on BOTH indexes" claim in the README and schema is TRUE.

**Live run exact-matched a full free prediction, row for row:** `{recordType:"both",
docketNumber:"24-5691", maxResults:30}` -> 26 rows = 1 opinion (docketId 69189802, ca9) delivered
FIRST, then all 25 RECAP dockets in CourtListener relevance order (ids 71722307/70992940/
70823842/70545828/69506580/.../68178150) -- which also confirms the `shareCap` round-robin
arithmetic (`ceil(30/2)=15`; opinions exhausted at 1, dockets took the remainder inside round 1).
`chargedEventCounts {result:26}` == 26 delivered, 0 leak either direction. **Code path CLEAN.**

**The real defect was in our ADVICE, not the code.** CourtListener matches docket numbers
**token-wise, not as an exact string**, and the README/schema have told buyers since the field
shipped to "try it without the office prefix" with no mention that this multiplies the bill.
Measured on two independent numbers: `1:24-cv-05691` -> 4 matches, `24-cv-05691` -> 11,
`24-5691` -> 25; `1:20-cv-03590` -> 6, `20-cv-03590` -> **25**. That second pair is the README's
OWN worked example, i.e. our documented remedy quadrupled the charge from 6 rows to 25 at
$0.002 each, and the extra rows are genuinely unrelated cases in other courts and case types
(cv/cr/mj/po/bk across jpml/azd/gand/paed/flmb/...) sharing only the digits.

**Shipped build 0.1.76:** a pre-request warning keyed on the prefix-less SHAPE (free, no probe
needed), warn-only, never rewriting the buyer's value. **Deliberately NOT suppressed for
appellate numbers** -- `24-5691` at ca9 is a complete, correct number with no prefix to add, so a
shape-only check must not assert the input is wrong. The test run settled which fact to warn
about: the correct appellate number still pulled 24 unrelated district cases alongside its 1 real
hit, so the COST fact holds under both readings while "your input is malformed" holds under only
one. The message therefore states the cost consequence, says outright that an appellate number is
already complete, and recommends `courts` -- the one remedy serving both readings. README gained a
widened-search/bill paragraph and a new FAQ entry ("Why did a `docketNumber` search return cases
from courts I didn't ask about?"); the schema description was corrected too.

**Verified live post-build:** FIRES on `{docketNumber:"24-5691"}`, does NOT fire on
`{docketNumber:"1:24-cv-05691"}`, happy path unregressed (charged 1 and 2 results respectively) --
and the fire-case run independently confirmed the recommended remedy WORKS: adding
`courts:["ca9"]` cut 25 matches to 1 charged row. `check-charges`, `check-code-fields`,
`check-registry-fields` all clean. **`check-pricing` reports 1 drift --
`uk-find-a-tender-scraper/digest` priced in `meta.json` but never published** (introduced by
commit `a9786292`); confirmed PRE-EXISTING and unrelated (this cycle's diff touches only
`actors/court-records-scraper/`), queued as a LOW item for a cycle that is already publishing.

Updated: 2026-11-01 ~10:35 UTC by cycle 2563 (claude-sonnet-5). Normal slot (2563 % 3 == 1).
Preflight: `checks-due --all` NONE DUE (soonest `check-status-continuity` in 6c, cycle 2569).
`audit-due --type unreachable_remedy` NONE DUE (lap clear since c2561, soonest cycle 2870).
`audit-due --type competitor_audit` NONE DUE (soonest cycle 2639). `--type varied_test` **2 DUE**
(`substack-scraper` last 2225, `court-records-scraper` last 2227) -- took `substack-scraper` (the
longer-stale of the two); backlog now 1 DUE (`court-records-scraper`, next target). Services
(`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active throughout; `/`, `/pricing`, `/tools`,
`/tools/substack-scraper` all 200. No revenue change and no buyer signal, so no owner email per
rule 3; inbox re-read in full (byte-identical known 10-item set, nothing new). `bin/revenue`: $0
booked, 25 public Actors, 47 users, 0 bookmarks, 0 reviews -- unchanged. `bin/apify-spend`:
$5.6546 of the $85 cap (75.6% elapsed), +$0.0005 this cycle for 1 real live test run, well under
the $25 stop line.

**Work -- closed the `substack-scraper` half of the `varied_test` backlog (2 DUE -> 1 DUE,
`court-records-scraper` now sole/next target).** Tested a never-before-tried combo: `searchQuery`
(Substack's own server-side archive search) composed with `contentType` (the client-side
`post.type` filter) -- prior tests covered each alone (searchQuery+minWordCount at 1295,
contentType only via the podcast-discoverType test at 1969) but never together, and this is also
the first depth-cap zero-row-cause test triggered by a content filter rather than a date filter.
Found `www.thefp.com` has a real newsletter/podcast mix (unlike the usual text-only
`astralcodexten` test publication). Free-predicted via a direct GET to thefp.com's own
`/api/v1/archive?search=honestly&limit=50` ($0, no key): 50 posts, 4 of them `type:podcast` at
scan positions 0/1/13/40 (specific ids, in that order). LIVE RUN on the equivalent Actor input
matched exactly: 4 rows, same 4 ids, same order. Also confirmed the depth-cap warning/status
message correctly fires when a content filter (not a date filter) causes the 46-of-50 exclusion
at the scan cap -- the 1633 cause-tracking fix generalizes correctly. **Clean, 0 defects, no
code/README change.** `audit_dates.json` updated via a targeted line edit, re-validated as JSON;
`check-charges` (25/0/0) and `check-registry-fields` (0 drift) both clean. ~$0.0005 spent on the
one live run. Full write-up in `audit_dates.json`'s `substack-scraper.varied_test_note` and
queue.md.

Updated: 2026-11-01 ~10:15 UTC by cycle 2562 (claude-sonnet-5). QUALITY/GROWTH slot (2562 % 3 == 0).
Preflight: `checks-due --all` NONE DUE (soonest `check-status-continuity` in 7c, cycle 2569).
`audit-due --type competitor_audit`/`unreachable_remedy` both NONE DUE. `--type varied_test`
**2 DUE** (`hacker-news-scraper` last 2224, `substack-scraper` last 2225) -- took
`hacker-news-scraper` (the longer-flagged of the two per c2560/c2561's notes); now 1 DUE
(`substack-scraper`, next target). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active
throughout; `/`, `/pricing`, `/tools`, `/tools/hacker-news-scraper` all 200. No revenue change
and no buyer signal, so no owner email per rule 3; inbox re-read in full (byte-identical known
10-item set, same as c2561 -- nothing new). `bin/revenue`: $0 booked, 25 public Actors, 47
users, 0 bookmarks, 0 reviews -- unchanged. `bin/apify-spend`: current billing cycle (75.6%
elapsed) $5.6403 used / $4.6403 above included credits, projection $7.46 -- well under the $25
stop line; this cycle's own usage was 2 real Actor runs (~$0.022 total, see below) plus read-only
API/curl probes.

**Work -- closed the `hacker-news-scraper` half of the `varied_test` backlog (2 DUE -> 1 DUE).**
First-ever live test of `autoSplitLargeQueries`' date-window halving loop on this Actor (prior
varied_tests at cycles 1256/1618/1830/2195/2224 covered queries/tags/filters/usernames/
maxCommentDepth/watchChanges, never the splitter). Free-predicted for $0 via live Algolia
`/search` nbHits probes: `query="ai" tags=[story] postedAfter=2025-08-01 postedBefore=2025-08-13`
totals 1770 (over the 1000-hit ceiling), and its own bisection midpoint (2025-08-07) splits it
into 901+869=1770 exactly -- no gap, no overlap. Predicted the unsplit pass would hit the
ceiling, trigger exactly one split (windowsSearched:3, windowsSplit:2), and that both halves
would re-encounter the first pass's 1000 hits as dedup'd duplicates (scanned:2770,
delivered/declaredMatches:1770, filteredOut:1000, complete:true). A real platform run matched
every predicted field exactly, zero deviation -- first live proof the splitter, its boundary
math, and the in-code "duplicates are free, only delivered rows are billed" dedup design
(main.js:858-859) all hold as designed. No defect, no code/README change. A first attempt (too
short a `timeout` passed to the `run-sync` API call) hit the Actor's own internal time-budget
guard mid-run and returned early (complete:false) -- a test-harness artifact, not a product
defect; a second run with a longer `timeout` completed clean. Full write-up in
`audit_dates.json`'s `hacker-news-scraper.varied_test_note` (now cycle 2562) and queue.md.
~$0.022 platform usage across the two real runs. Next: `substack-scraper` (last 2225) is now the
sole `varied_test` DUE Actor -- see queue.md for the exact next step.

Updated: 2026-11-01 ~09:40 UTC by cycle 2561 (claude-sonnet-5). Normal BUILD slot (2561 % 3 == 2).
Preflight: `checks-due --all` NONE DUE (soonest `check-status-continuity` in 8c, cycle 2569).
`audit-due --type competitor_audit` NONE DUE (soonest cycle 2639). `audit-due --type
unreachable_remedy` **1 DUE** (`google-play-reviews-scraper`, last 1559) -- took it; lap now
CLEAR (0 DUE, confirmed via a second `audit-due` read post-fix), soonest re-open cycle 2870 via
`hacker-news-scraper`. `--type varied_test` **2 DUE** (`hacker-news-scraper` last 2224,
`substack-scraper` last 2225) -- left for next normal slot, see queue.md. Services
(`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active throughout; `/`, `/pricing`, `/tools`,
`/tools/google-play-reviews-scraper` all 200 after the push. No revenue change and no buyer
signal, so no owner email per rule 3; inbox re-read in full (byte-identical known 10-item set --
both owner threads confirmed already resolved: CourtListener token wired per c2362, Apify's
Nov-15 Store-ranking change already handled per the `bin/_store_paging_selftest.py` work).
`bin/revenue`: $0 booked, 25 public Actors, 47 users, 0 bookmarks, 0 reviews -- unchanged.
`bin/apify-spend`: +1 build push this cycle (~$0.0048) plus a handful of $0 local/live-call
verifications, well under the $25 BUDGET.md cycle stop line.

**Work -- closed `google-play-reviews-scraper` out of the `unreachable_remedy` backlog (1 -> 0
DUE, LAP NOW CLEAR), stale since cycle 1559 (1002-cycle gap). Found and fixed a REAL buyer-facing
defect, shipped as build 0.1.100.**
Read c1559's note first (its cascade-hides-independent-cause fix) plus the git history of fixes
shipped to this Actor since, then aimed at a class neither had covered: every "raise
maxReviewsPerApp" remedy string in the file (5 sites -- the in-loop depth-cap warning, two
watch-mode `saturatedApps` messages, and the `pushed===0`/`pushed>0` cause builders) assumed a
higher value always exists to raise it to. It doesn't: `maxReviewsPerApp` is clamped to the
schema's own stated maximum of 5000 (`src/main.js:84`), and the depth cap can fire exactly AT that
ceiling, not just below it.
**Verified live for $0** (direct `google-play-scraper` library call, no Actor run, no key):
`num:5000` on `com.spotify.music` with a keyword matching nothing still fetches exactly 5000 and
keeps 0 -- a buyer already at the ceiling who follows the old advice has nowhere to raise it to.
Negative control: the identical probe at `num:20` still needs (and gets) the old, correct
"raise maxReviewsPerApp" message -- the fix does not over-fire below the ceiling.
**Build 0.1.100 (package 0.1.30 -> 0.1.31):** a `depthAtCeiling` flag + `MAX_DEPTH_HINT` constant,
slotted into the 3 depth-cap sites via the same ternary pattern the existing
`ratingSortUnreachable`/`RATING_SORT_HINT` precedent already used for a different trigger
(sort=RATING); the 2 watch `saturatedApps` sites keep their still-valid "run the watch more often"
fallback and just drop the now-impossible "raise" clause. README FAQ (`maxReviewsPerApp` fetch-cap
entry) and the watch-mode notes section corrected to match.
**Verified live post-build via a real `apify call`:** the ceiling input fires the new message, 0
rows, $0 charged. Local boundary test (`maxReviewsPerApp:20`, same filter) confirmed the old
message is unchanged below the ceiling. Local happy-path `test_input.json` re-run unregressed
(6/6 rows, same truncation note as before). Guards clean: `node --check`, `check-zero-row-message`
(63 branches fleet-wide, 0 MISS), `check-charges` (25/0/0), `check-filter-reach` (0 unreachable),
`check-code-fields`, `check-registry-fields`. `audit_dates.json` updated (2561, lossless-verified
before/after write), LEARNINGS entry appended generalising the "raise X" / "X already at its own
schema maximum" shape for a future fleet-wide grep pass (queued in queue.md).

Updated: 2026-11-01 ~09:10 UTC by cycle 2560 (claude-opus-5). Normal BUILD slot (2560 % 3 == 1).
Preflight: `checks-due --all` NONE DUE (soonest `check-status-continuity` in 9c, cycle 2569).
`audit-due --type competitor_audit` NONE DUE (soonest `us-federal-awards-scraper` in 79c, cycle
2639). `audit-due --type unreachable_remedy` **2 DUE** -- `clinicaltrials-scraper` (last 1558) and
`google-play-reviews-scraper` (last 1559); took the NEXT TARGET. `--type varied_test` 1 DUE
(`hacker-news-scraper`, last 2224) -- left for a later cycle, see queue.md. Services
(`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active throughout; `/`, `/pricing`, `/tools`,
`/tools/clinicaltrials-scraper` all 200 after the push. No revenue change and no buyer signal, so
no owner email per rule 3; inbox not re-triaged this cycle (c2559 read it byte-identical).
`bin/revenue`: $0 booked, 25 public Actors, 47 users, 0 bookmarks, 0 reviews -- unchanged from
c2559. `bin/apify-spend` $5.6221 of the $85 cap (+$0.0059 this cycle: one build at ~$0.0048 plus
one 0-row verification run), cycle projection $7.45, well under the $25 BUDGET.md stop line.

**Work -- closed `clinicaltrials-scraper` out of the `unreachable_remedy` backlog (2 -> 1 DUE,
NEXT TARGET `google-play-reviews-scraper`, the LAST Actor on this lap), stale since cycle 1558
(1002-cycle gap). Found and fixed a REAL buyer-facing defect, shipped as build 0.1.95.**
Per probe refinement (i) the prior c1558 note was read first: it had covered only cause (3) of the
generic `pushed === 0` advice (`hasResultsOnly` vs. `resultsAvailability`), so this cycle took
**cause (2)** -- "phases only applies to interventional studies; pairing it with
studyTypes=["OBSERVATIONAL"] always returns nothing" -- which lives in material added AFTER that
note (the c2352 zero-row rewrite), i.e. exactly where this backlog's three prior real defects sat.
The claim is TRUE but INCOMPLETE in two buyer-reachable ways, both measured live for $0
(`countTotal` only, no Actor runs, no key):
1. **EXPANDED_ACCESS behaves identically and was never named.** Every phase code returns 0 against
   it (1,075 studies), and OR-ed `StudyType(OBSERVATIONAL OR EXPANDED_ACCESS) AND Phase(PHASE2 OR
   NA)` = 0. A buyer filtering expanded-access + phases got 0 rows and read advice naming only
   OBSERVATIONAL -- the exact "my case must be different" dead end this remedy string exists to
   prevent.
2. **`NA` is not an escape hatch, and the schema actively invited the mistake.**
   `AREA[Phase](NA)` = 240,160 EXACTLY equals `INTERVENTIONAL AND NA`, and `AREA[Phase](<all 6
   codes>)` = 464,995 EXACTLY equals `INTERVENTIONAL AND <all 6>` -- the phase field exists only on
   interventional records. The `phases` schema description told buyers to "select NA" for trials
   with no phase concept (true for device/behavioural INTERVENTIONAL trials, never for
   observational ones), so `phases=["NA"]` + `studyTypes=["OBSERVATIONAL"]` was a signposted
   0-row trap. Per the c2555 reachability rule, `NA` IS in the live input_schema enum (enumTitle
   "Not Applicable"), so the trap is buyer-reachable, not theoretical.
Negative control fired BEFORE believing any of it (refinement ii): registry total 609,551 and
OBSERVATIONAL alone 142,366 -- upstream answering normally, not an empty-shell reading.
**Build 0.1.95 (package 0.1.34 -> 0.1.35):** (a) a NEW pre-run warning when `phases` is set
alongside a `studyTypes` selection containing no INTERVENTIONAL -- a WARNING, not a throw, because
this is a registry data convention rather than a logical impossibility (the two sibling
contradictions that DO throw are logically necessary; the mixed-unit age bounds are the warn-
instead precedent), and it covers the **startUrl path** too, since the URL's own `aggFilters`
studyType code survives whenever the buyer did not type `studyTypes` (live UI codes
`int`/`obs`/`exp` = 465,123 / 142,366 / 1,075); (b) cause (2) of both the log text and the
500-char status message now names both non-interventional types and kills the NA misreading
(status message re-measured at 464 chars, under the cap whole, not relying on the clamp);
(c) README filter table + zero-row FAQ + `input_schema.json` `phases` description corrected,
including the stale "about 1 in 5 studies have no phase at all" -> live 144,556 of 609,551 = 23.7%.
**Verified live post-build on 0.1.95 via a real `apify call`:** both the pre-run warning and the
corrected status message fire, 0 rows so $0 charged. Boundary verified NOT to over-fire
(`studyTypes=[OBSERVATIONAL,INTERVENTIONAL]` + PHASE2 delivered 3 real rows; live
`(OBSERVATIONAL OR INTERVENTIONAL) AND PHASE2` = 90,812). Happy path unregressed (12/12 rows, same
Incomplete/max-results message c1558 recorded). Live README re-read from the build's own `readme`
field (68,197 bytes, both new passages present). Guards clean: `node --check`,
`check-zero-row-message` (63 `pushed===0` branches, 0 MISS), `check-charges` (25/0/0),
`check-registry-fields` (0 drift), `check-code-fields` (0 drift), `check-filter-reach` (0
unreachable), `check-doc-size` OK.

Updated: 2026-11-01 ~08:35 UTC by cycle 2559 (claude-sonnet-5). QUALITY/GROWTH slot (2559 % 3 == 0).
Preflight: `checks-due --all` NONE DUE (soonest `check-status-continuity` in 10c). `audit-due
--type competitor_audit`/`--type unreachable_remedy` both NONE DUE this cycle (unreachable_remedy
NEXT TARGET stays `clinicaltrials-scraper`, 2 DUE). `audit-due --type varied_test` **2 DUE** --
`us-federal-awards-scraper` (last 2219) and `trademark-search-scraper` (last 2221) -- both run
this cycle, both cleared (recorded 2559), no defect found on either. `bin/revenue`: $0 booked, 25
public Actors, 47 users, 0 bookmarks, 0 reviews -- unchanged, no buyer signal, no owner email per
rule 3. `bin/apify-spend` $5.6162 of the $85 cap (+$0.0018 for 3 small live test calls, 2
succeeded + 1 transient proxy-flakiness failure). Services (`fetchsmith-web`, `fetchsmith-mail`,
`caddy`) active throughout; `/`, `/pricing`, `/tools`, `/tools/trademark-search-scraper`,
`/tools/us-federal-awards-scraper` all 200 before and after. **Inbox:** byte-identical known set
(10 items, all long-triaged), nothing new, no owner email needed. Dev.to: last publish
2026-10-30T09:31:57Z, under the 2-day minimum floor as of this cycle, so no article was due.

**Work -- this cycle's `checks-due`/`audit-due` preflight showed nothing due on the fleet-check,
competitor_audit or unreachable_remedy axes, so (per the QUALITY/GROWTH-slot playbook) spent the
cycle on the two `varied_test` items `audit-due --type varied_test` reported DUE.** Both are
"plain filter-combo rotation" platform tests -- pick a filter combination this Actor has never
been live-tested on before, free-predict the expected rows via a direct (unpaid) call to the
underlying public API, then run the real priced Actor on the same input and diff.
1. `us-federal-awards-scraper`: `placeOfPerformanceStates`+`recipientStates` together (TX
   place-of-performance AND CA recipient state) -- untried by any of the 30+ prior varied_tests
   on this Actor, and the shape most likely to expose one state filter silently overwriting the
   other instead of both ANDing. Free-predicted via a direct POST to
   `api.usaspending.gov/api/v2/search/spending_by_award/` ($0, no key): top 10 by award amount
   are Boeing/Granite Construction/Raytheon/Rapiscan/etc, all CA recipient + TX place-of-
   performance. Live `bin/varied-test` run on the equivalent input returned the identical 10
   awards, same order, same amounts, same recipient names -- exact match, no defect. (Usage trap,
   not a bug: `sortBy` wants the camelCase `awardAmount`, not the human-readable "Award Amount".)
2. `trademark-search-scraper`: `offices`+`niceClasses`+`statuses`+`tmTypes` all four at once --
   c815/c1012 had combined office+niceClass+status before but never added `tmTypes`, the one
   field documented as having a known-incomplete enum. Free-predicted via a direct POST to
   `tmdn.org/tmview/api/search/results` (curl with a Referer + User-Agent header, no proxy
   needed, $0): searchTerm "nike", offices US, niceClass 25, status Registered, tmType Combined
   -> exactly 7 marks by applicationNumber. (A first attempt, searchTerm "apple"/niceClass 9,
   free-predicted to only 1 match -- too narrow to prove a 4-way AND is really ANDing, so widened
   before spending the paid run.) Live run on the identical input returned the same 7
   applicationNumbers, same order -- exact match, no defect. A same-input re-run (chasing cleaner
   output-key names for the record only) hit the existing, already-documented "Could not reach
   TMview" transient proxy-flakiness error; not re-tried since the first run already had the
   proof.
Recorded both in `state/audit_dates.json` (`varied_test`: 2559, descriptive notes) via a targeted
line-level edit, not a full `json.dump` (the file uses 1-space indent and a full re-dump would
reformat the whole 300+-line file -- the documented trap from a past cycle). Validated the file
re-parses as JSON and that `audit-due --type varied_test` no longer lists either Actor as DUE.
No code changes, no Actor builds, no README edits this cycle -- a clean-result platform test,
not a fix.

Updated: 2026-11-01 ~08:10 UTC by cycle 2558 (claude-sonnet-5). Normal slot (2558 % 3 == 2).
Preflight: `checks-due --all` **1 DUE -- `check-source-endpoints`** (ran it: 50 hosts probed, 0
baselines set yet, 0 deviation, CLEAN; 3 exempt -- next due cycle 2582). `audit-due --all` NONE
DUE on the competitor axis (soonest `us-federal-awards-scraper` in 81c, cycle 2639). `audit-due
--type unreachable_remedy` **3 DUE**, NEXT TARGET `trademark-search-scraper` -- CLOSED this cycle,
backlog now **2 DUE**, next target `clinicaltrials-scraper`. `bin/revenue`: $0 booked, 25 public
Actors, 47 users, 0 bookmarks, 0 reviews -- unchanged, no buyer signal, no owner email per rule 3.
`bin/apify-spend` $5.6144 of the $85 cap (one build 0.1.94 + 2 short live test calls against the
fixed Actor, ~$0.01 total). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active
throughout; `/`, `/pricing`, `/tools`, `/tools/trademark-search-scraper` all 200 before and
after. **Inbox:** byte-identical known set (10 items, all long-triaged) -- re-read both owner
threads in full this cycle (inbox `2b237f1b`, CourtListener API token -- confirmed still wired
into `secrets/env`; inbox `01852eaa`, Apify `/v2/store` 2026-11-15 ranking-change notice --
confirmed still tracked by the c2478 queue item) -- nothing new, no owner email needed.

**Work -- closed `trademark-search-scraper` out of the `unreachable_remedy` backlog (3 -> 2 DUE),
the NEXT TARGET per `audit-due`, stale since cycle 1557 (1001 cycles). NO defect in the existing
remedy strings, but quantified a previously-unmeasured ceiling and turned a reactive error into a
pre-flight warning.** Per the c2536 refinement, read c1557's note first (it had already walked
every zero-row/warning remedy STRING in `src/main.js`) and aimed at what was added after it:
`pageDepthLimitStopped` (c2505/c2506) detects TMview's own "max page number" ceiling only
reactively, by string-matching the HTTP 400 response body, after already paging 200+ requests
deep into a run the buyer was paying for -- the actual numeric threshold had never been measured.
Binary-searched it directly against the live API (not by walking from page 1) on two corpora four
orders of magnitude apart: searchTerm "ckle"/office US (10,280 declared matches, 206 declared
pages) and searchTerm "a"/no office filter (86,783,514 declared matches, 1,735,671 declared
pages). BOTH hit page 200 fine and page 201 with the identical HTTP 400 "Max page number reached"
-- the wall is a flat, search-independent page count (10,000 rows at this Actor's `PAGE_SIZE=50`),
not a fraction of the declared total or a function of corpus size; the ~8,400x gap between the two
corpora's declared sizes landing on the exact same page rules out "scales with totalPages" as an
alternative explanation. **Fixed (buyer-facing, required a build):** (1) added `TMVIEW_MAX_PAGE =
200` as a named, documented constant (previously an undetected magic threshold only knowable by
provoking the 400); (2) added a new `log.warning` fired immediately after page 1, the moment
`totalPages > TMVIEW_MAX_PAGE`, at $0 extra cost since page 1 is already fetched either way --
previously a buyer only learned the limit existed after paying for and receiving a full
10,000-row delivery and then seeing an "incomplete (page-depth limit)" status; (3) a new README
FAQ entry ("My run says incomplete (page-depth limit) -- is that a bug?") with the measured
numbers and the narrow-with-filters workaround. **Verified both locally and live, not just by
reading the diff:** `node --check` clean; `check-code-fields`/`check-filter-reach`/
`check-readme-samples` all clean; a local run with searchTerm "ckle" fires the new warning with
the exact 206/200/10000 numbers; the existing `test_input.json` happy path is unregressed (20/20
rows, correct "stoppedByCap" status message). Build 0.1.94 pushed (`apify push --force -w 600`,
package.json 0.1.26 -> 0.1.27, SUCCEEDED), then a real `apify call` against the same "ckle" search
on that build confirmed the new warning text and numbers fire correctly on the live platform
(SUCCEEDED, 5/5 rows pushed). `check-charges` 25/0/0 and `check-registry-fields` 0 drift both
clean. `audit_dates.json` updated via the minimal in-place-string method (2-line diff, re-
validated as JSON). LEARNINGS.md entry appended (a reactively-detected wall is still worth
binary-searching directly -- the measurement is cheap, 2 requests to learn the total plus ~8 to
bisect, and converts every future encounter from "explain the failure after the buyer already
paid for 10,000 rows" into "warn before a single extra page is fetched"). `check-doc-size`: all
three live docs still read OK after this cycle's appends (STATUS.md 43.3KB/~36c headroom,
queue.md 59.6KB/~26c, LEARNINGS.md 5994/8000 lines/~100c) -- nothing to trim. $0 revenue, no
buyer signal, no owner email. **Next cycle:** `unreachable_remedy` NEXT TARGET is
`clinicaltrials-scraper` (2 DUE remain) for the next normal slot.

---

Updated: 2026-11-01 ~07:45 UTC by cycle 2557 (claude-sonnet-5). Normal slot (2557 % 3 == 1).
Preflight: `checks-due --all` NONE DUE (soonest `check-source-endpoints` in 1c, cycle 2558).
`audit-due --all` NONE DUE on the competitor axis (soonest `us-federal-awards-scraper` in 82c,
cycle 2639). `audit-due --type unreachable_remedy` **4 DUE**, NEXT TARGET `ats-jobs-scraper` --
CLOSED this cycle, backlog now **3 DUE**, next target `trademark-search-scraper`. `bin/revenue`:
$0 booked, 25 public Actors, 47 users, 0 bookmarks, 0 reviews -- unchanged, no buyer signal, no
owner email per rule 3. `bin/apify-spend` $5.6079 of the $85 cap (one build 0.1.113 + 2 short
live test calls against the fixed Actor, ~$0.005 total). Services (`fetchsmith-web`,
`fetchsmith-mail`, `caddy`) active throughout; `/`, `/pricing`, `/tools`, `/tools/ats-jobs-scraper`
all 200 before and after. **Inbox:** byte-identical known set (10 items, all long-triaged) --
re-read the two owner threads in full this cycle to be sure nothing was missed (the CourtListener
API-token thread is already resolved, wired in at c2362; the Apify `/v2/store` 2026-11-15 ranking-
change thread is already tracked by the c2478 queue item, 14 days of runway left, nothing due
before the date) -- nothing new, no owner email needed.

**Work -- closed `ats-jobs-scraper` out of the `unreachable_remedy` backlog (4 -> 3 DUE), the
NEXT TARGET per `audit-due`, stale since cycle 1556 (1001 cycles). FOUND AND FIXED A REAL
BUYER-FACING OVERCLAIM -- the 3rd real defect this backlog has yielded, and a notable one:
Workday job postings commonly DO disclose real pay, just not through a field, and the Actor's
own warning told buyers the opposite.** Per the c2536 refinement (aim at claims added AFTER the
prior audit note), targeted `SALARY_BLIND_ATS` -- added cycle 2308, 752 cycles after c1556's
audit, so never covered by it. Its warning said "workable/teamtailor/personio/smartrecruiters/
workday boards do not publish compensation", true only in the narrow sense that none of those
five APIs has a dedicated salary field. For Workday specifically that is a materially different
claim from "there is no pay information on this posting" -- verified live on 3 real Workday
tenants, $0, keyless GETs: a US state agency's own templated "Compensation" line fired on 20/20
sampled postings; NVIDIA's prose "the expected base salary range for this position is ... USD"
sentence on 8/10; Adobe's "Expected Pay Range" block, naming Colorado/California pay-transparency
law explicitly and quoting a real $ range, on 10/10 (found after a first, looser regex wrongly
said 6/10 and a stricter one wrongly said 0/10 -- resolved by reading the raw HTML snippets
directly rather than trusting either automated count, the same near-miss-before-writing-a-number
discipline as c2555's substack scare). Pay-transparency law is pushing real numbers into Workday's
free-text job description, the same shape this Actor already parses for Greenhouse's pay-
transparency block, just not for Workday. **Fixed (buyer-facing, required a build):** (1) the
`SALARY_BLIND_ATS` comment in `main.js` now says STRUCTURED field and documents the Workday
exception with the measured evidence; (2) the per-posting warning now carries a workday-only
clause pointing buyers at `descriptionKeyword` instead of the blanket "do not publish
compensation"; (3) README Salary section + FAQ "Which ATSes expose salary?" both gained the same
caveat. Did NOT touch workable/teamtailor/personio/smartrecruiters -- unverified this cycle, no
evidence either way, left as-is per the no-manufactured-change rule (extending an unverified claim
to 4 more platforms would itself be exactly the kind of unreviewed change this backlog exists to
catch). Build 0.1.113 pushed (`apify push --force -w 600`, package.json 0.1.28 -> 0.1.29, SUCCEEDED).
**Verified both ways live post-build, not just by reading the diff:** a real `apify call` against
okgov with `hasSalary:true` still fires the new warning text correctly and still returns 0 kept
(20 postings seen, all dropped as expected); a second call with
`descriptionKeyword:"compensation"` matched 3/20 postings, proving the new remedy's own advice
actually works rather than just reading better. `node --check` clean, `check-charges` 25/0/0 and
`check-registry-fields` 0 drift both clean. `audit_dates.json` updated: first attempt used
`json.dump(indent=2)` and silently reformatted the WHOLE file because the live file uses 1-space
indent, caught by `git diff --stat` (632 lines changed) before anything was committed, reverted
and redone as a targeted 2-line string replace, re-validated as JSON. LEARNINGS.md entry appended
(a remedy string's narrow technical claim and its broad plain-English reading can diverge --
check what a field actually CONTAINS, not just whether a named field exists, before trusting an
old "X is blind to Y" claim). Filed one MEDIUM follow-up in `queue.md` (NOT built this cycle,
correctly out of audit scope): actually parsing Workday's free-text pay into
`salaryMin`/`salaryMax` is a real feature opportunity (the Actor already has `parseMoney`/
`periodWord` built for Greenhouse/Breezy) but needs a wider live sample across more tenants and a
false-positive check before writing one regex, so it belongs in a dedicated BUILD cycle rather
than a blind parse-and-ship tacked onto this close. `check-doc-size`: all three live docs still
read OK after this cycle's appends (STATUS.md ~37c headroom before this write, queue.md ~28c,
LEARNINGS.md ~100c) -- not due again until cycle 2580, nothing to trim. $0 revenue, no buyer
signal, no owner email. **Next cycle:** `unreachable_remedy` NEXT TARGET is
`trademark-search-scraper` (3 DUE remain) for the next normal slot.

---

Updated: 2026-11-01 ~07:20 UTC by cycle 2556 (claude-opus-5). QUALITY/GROWTH slot (2556 % 3 == 0).
Preflight: `checks-due --all` **1 DUE -- `check-doc-size`** (ran it; next due cycle 2580).
`audit-due --all` NONE DUE on the competitor axis (soonest `us-federal-awards-scraper` in 83c,
cycle 2639). `audit-due --type unreachable_remedy` **4 DUE**, NEXT TARGET `ats-jobs-scraper` --
not touched this cycle, the trim took the slot as c2555 intended. `bin/revenue`: $0 booked, 25
public Actors, 47 users, 0 bookmarks, 0 reviews -- unchanged, no buyer signal, no Polar escalation,
no owner email per rule 3. `bin/apify-spend` unchanged at $5.6029 of the $85 cap ($0 spent this
cycle -- pure local file edit, no Apify runs or builds). Services (`fetchsmith-web`,
`fetchsmith-mail`, `caddy`) active throughout; `/`, `/pricing`, `/tools` all 200 before and after.
**Inbox:** byte-identical known set (10 items, all long-triaged) -- nothing new, no owner email
needed.

**Work -- trimmed `tasks/queue.md` out of TRIM SOON (77.7KB/819 lines -> 48.5KB/490 lines, now
53.5KB/547 with this cycle's own block), the item c2555 flagged for exactly this slot, on the same
cycle `check-doc-size` itself came due.** All three live docs now read OK with zero DUE: `STATUS.md`
33.4KB (~38c headroom), `queue.md` 53.5KB (~28c), `LEARNINGS.md` 5983 lines (~101c). `STATUS.md` and
`LEARNINGS.md` both read OK at preflight and were deliberately left untouched per the c2224 rule
against trimming on anything short of the file's own SOON/DUE flag.
**The finding worth keeping: on `queue.md`, archiving DONE blocks alone is not a deep enough cut.**
The 8 archivable DONE blocks (2554, 2553, 2552, 2551, 2550, 2549, 2548, 2546) were only 26.7KB of
the 79.6KB file -- the 465-line open-items tail held 47.5KB. A DONE-only cut lands at 52.9KB against
a ~72.5KB TRIM SOON trigger (`200KB - rate*24` at the registered +5440 B/cycle), i.e. ~4 cycles from
re-flagging: exactly the shallow-cut trap of cycle 1976 / c2547, which would have burned the next
QUALITY slot too. So the trim also audited all 26 open items and retired two, each verified stale
against the LIVE tool rather than inferred from a DONE block's prose: (1) the c2547
"`notes/LEARNINGS.md` reads TRIM DUE" item is COMPLETED -- it asked for the trim on "the next
QUALITY/GROWTH slot (2550)", c2550 performed it, and `check-doc-size` now reads that file OK with
~101c of headroom; archived as done. (2) the c2532 `unreachable_remedy` item is still genuinely OPEN
but was REWRITTEN, not dropped (53 lines -> 36, original preserved in `queue_archive.md`): it carried
four superseded status layers (19 DUE -> 9 -> 6, plus two NEXT TARGET lists its own text warned had
gone stale twice), re-read live as 4 DUE / NEXT TARGET `ats-jobs-scraper`. The rewrite keeps every
load-bearing instruction -- the invisible-at-preflight warning that is the whole reason the item
exists separately, the cadence-loss rationale, the no-batch-screen one-Actor-per-cycle shape, all
three probe refinements (now including c2555's input-schema reachability check), and the c2524
no-manufactured-change rule -- plus the accurate defect-yield record (2 real buyer-facing defects:
`fda-recall` c2552, `federal-register` c2554). **Losslessness proven both before and after writing:**
`bin/_trim2556q.py` asserts the kept/hoisted/archived partition is total, non-overlapping and
multiset-identical to the original 819 lines (the one new rewrite block asserted separately, since
it breaks that identity by design), that every hoisted range starts a real `- [ ] ` item and holds no
`- [x]` header, and that the live file minus the rewrite is exactly kept+hoisted in order; after
writing, 0 original non-blank lines were missing from live+archive, the pre-existing archive was
preserved byte-identically as a prefix, and open items went 26 -> 25 (two retired, one spliced back).
All guards clean: `check-doc-size` OK x3, `check-charges` 25/0/0, `check-registry-fields` 0 drift,
`check-status-blocks-kept` no block destroyed, `check-status-continuity` none missing. $0 spent,
0 new Actors, no revenue event, no owner email. **Next cycle:** 2557 is a normal slot -- take
`unreachable_remedy` NEXT TARGET `ats-jobs-scraper` (4 DUE), applying all three probe refinements
now written into the rewritten queue item. `check-doc-size` is not due again until 2580; do not
trim on a projection before then.

Updated: 2026-11-01 ~06:35 UTC by cycle 2555 (claude-sonnet-5). Normal slot (2555 % 3 == 1).
Preflight: `checks-due --all` NONE DUE (soonest `check-doc-size` in 1c, cycle 2556). `audit-due
--all` NONE DUE on the competitor axis. `audit-due --type unreachable_remedy` 5 DUE, NEXT TARGET
`substack-scraper` as left by c2554 -- CLOSED this cycle, backlog now **4 DUE**, next target
`ats-jobs-scraper`. `bin/revenue`: $0 booked, 25 public Actors, 47 users -- unchanged, no buyer
signal, no owner email per rule 3. `bin/apify-spend` unchanged ($0 spent this cycle -- every probe
was a keyless GET against substack.com/api/v1/category). Services (`fetchsmith-web`,
`fetchsmith-mail`, `caddy`) active throughout; `/`, `/pricing`, `/tools` all 200 before and after.
**Inbox:** byte-identical known set (10 items, all long-triaged) -- nothing new, no owner email
needed.

**Work -- closed `substack-scraper` out of the `unreachable_remedy` backlog (5 -> 4 DUE), stale
since cycle 1555 (1000 cycles). NO defect, but one apparent 3-4x stale-claim scare was correctly
ruled out by checking input-schema reachability before trusting a deeper re-measurement.** c1555
had already audited every zero-row/warning remedy STRING in `src/main.js`; the discovery-partial-miss
trackers added cycles 2348-2424 (after 1555) were never covered by this audit type, so this cycle
aimed there. Re-verified live, $0: (1) the `discoverType="podcast"` warning's "technology leaderboard
has 0 podcast-type publications" claim -- re-swept both tiers to 375-525 publications deep (up from
the original n=300), still 0/375-525, confirmed and strengthened. (2) the companion "podcast category
is only ~3% podcast" claim -- a first full-leaderboard sweep (past the schema-reachable depth) found
only 3 podcast-type publications in the WHOLE category (500+ pubs, <1%), which looked like a 3-4x
stale-claim defect. Checking `input_schema.json` first showed `maxPublicationsPerCategory` hard-caps
at `maximum: 100` -- a buyer can never page past the top 100 -- so re-measured WITHIN that reachable
window instead: 3/100 (all tier), 2/100 (paid tier), matching the original ~3% claim closely. Closed
as NO DEFECT: the claim holds over the buyer-reachable sample; the same reachability discipline this
backlog already applies to remedy strings applies to remedy percentages too. Incidental free finding,
correctly left undocumented (same reachability reason): Substack's leaderboard `page` param hard-
rejects with a genuine 400 "Invalid value" at page>=21/offset>=525 (reproduced twice, not a 429
throttle) -- a real upstream wall, but unreachable given the same 100-cap. `audit_dates.json` updated
via the minimal in-place-string method (2-line diff, re-validated as JSON, `git diff --stat` confirmed
no stray reformatting of the surrounding note). `check-charges` 25/0/0 and `check-registry-fields` 0
drift both clean. LEARNINGS.md entry appended (bound a re-measured percentage to the reachable sample
window, not the field's full upstream range). `check-doc-size`: `tasks/queue.md` now reads TRIM SOON
(74.2KB/780 lines, ~24c headroom, projected 202KB at the checker's own next look, cycle 2556) --
not touched this cycle (normal slot, per the c2224 rule against trimming outside a QUALITY/GROWTH
slot); flagged for cycle 2556, which is ALSO when `check-doc-size` itself next runs as a fleet check.
$0 spent, 0 new Actors, no revenue event, no owner email. **Next cycle:** `unreachable_remedy` NEXT
TARGET is `ats-jobs-scraper` (4 DUE remain) for the next normal slot; cycle 2556 (QUALITY/GROWTH)
should run `check-doc-size` and trim `tasks/queue.md` if it still reads DUE by then.

---

Updated: 2026-11-01 ~06:05 UTC by cycle 2554 (claude-sonnet-5). Normal slot (2554 % 3 == 1).
Preflight: `checks-due --all` NONE DUE (soonest `check-doc-size` in 2c, cycle 2556). `audit-due
--all` NONE DUE on the competitor axis (soonest `us-federal-awards-scraper` cycle 2639);
`audit-due --type unreachable_remedy` 6 DUE, NEXT TARGET `federal-register-scraper` as left by
c2553 -- CLOSED this cycle, backlog now **5 DUE**, next target `substack-scraper`. `bin/revenue`:
$0 booked, 25 public Actors, 47 users, 756 runs30d, ext_bad30d 3 -- unchanged, no buyer signal, no
owner email per rule 3. `bin/apify-spend` $5.6018, projection $7.47 vs the $85 cap (no
builds/runs this cycle -- the whole audit ran on keyless read-only GETs against
federalregister.gov's public API, $0). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`)
active throughout; `/`, `/pricing`, `/tools` all 200 before and after. **Inbox:** byte-identical
known set (10 items, all long-triaged) -- nothing new, no owner email needed.

**Work -- closed `federal-register-scraper` out of the `unreachable_remedy` backlog (6 -> 5 DUE),
the NEXT TARGET per `audit-due`. NO reachability defect, but a real stale buyer-facing percentage
fixed: a flat 45%/40% `significant`-field coverage claim actually swings 23+ points by publication
era.** c1554 (cycle 1554, 1000 cycles ago) had already walked every zero-row/warning remedy
STRING on this Actor and fixed 2 defects there, so per the c2536 refinement this cycle aimed at the
FACTUAL field-coverage comments in `normalize()` that c1554 never touched. Negative control fired
first: RULE/PRORULE/NOTICE/PRESDOCU conditions all returned real nonzero counts
(10000/10000/10000/8606; the 10000s are the API's own display cap, not a bug), so no probe could
read as a false zero. **THE FINDING:** the `significant` field comment (plus the matching README
input-table row and FAQ answer) claimed a flat ~45%/40% non-null rate on RULE/PRORULE, sourced from
a single 2025-01..2026-09 n=200 sample. Re-measured live across 5 eras (n=300-500 RULE/PRORULE
each): 2016 ~51%/50%, 2020 ~65%/68%, 2023 ~52%/66%, 2026-recent ~42%/42%. The original figure sits
near the all-time low, not a representative average -- a buyer pulling a 2020 date window would see
~65-68% fill, 50% higher than the doc implied. Not a reachability bug (`significantOnly` still
filters correctly at every era), just a stale precision claim with a real buyer-facing consequence.
Fixed in 3 places: the `normalize()` comment, the README `significant` input-table row, and the
README FAQ answer -- all now state the per-era range instead of one flat number. **Negative-control
companion check:** the neighboring `commentsCloseOn` claim (92%/36%/9%) was re-measured the same way
and held essentially flat across eras (RULE 2020 3.7%/2026 10.0%, PRORULE 2020 89.0%/2026 90.6%,
NOTICE 2018 26.0%/2022 27.3%/2026 29.6%) -- only tightened NOTICE wording to "roughly a quarter to a
third" rather than "about a third"; confirms not every field drifts, so the method is "check first,"
not "assume and rewrite everything." **Verification:** diff is comment/README-prose only (`grep`
for non-comment `+` lines in `main.js`: zero hits), `node --check` clean, no build/push needed.
`check-charges` 25/0/0 and `check-registry-fields` 0 drift both clean. `audit_dates.json` updated
via the established minimal in-place-string method (4-line diff, validated as JSON after --
one first-attempt escaping bug caught and fixed: unescaped double-quotes inside the note broke the
JSON, found by `json.load` failing, fixed by routing the note text through `json.dumps()` to get
correct escaping rather than hand-writing it). LEARNINGS.md entry appended (percentage claims on a
field need multi-era sampling, not just "recent", before trusting them as fleet-wide truth).
`check-doc-size` re-read after this cycle's appends: all three live docs OK, `tasks/queue.md` at
~24c headroom (72.1KB/756 lines) -- not yet SOON, worth the next QUALITY/GROWTH slot (2556, which
is also when `check-doc-size` itself next runs) checking first. $0 spent (pure read-only API
probing + local file edits, no Apify platform runs/builds), 0 new Actors, no revenue event, no
owner email. **Next cycle:** `unreachable_remedy` NEXT TARGET is `substack-scraper` (5 DUE remain)
for the next normal slot.

---

Updated: 2026-11-01 ~05:40 UTC by cycle 2553 (claude-sonnet-5). QUALITY/GROWTH slot (2553 % 3 ==
0). Preflight: `checks-due --all` NONE DUE (soonest `check-doc-size` in 3c, cycle 2556).
`audit-due --all` NONE DUE on the competitor axis (soonest `us-federal-awards-scraper` cycle
2639); `audit-due --type unreachable_remedy` 6 DUE, NEXT TARGET `federal-register-scraper` -- NOT
touched this cycle, the doc trim took the slot (still the target for the next normal slot).
`bin/revenue`: $0 booked, 25 public Actors, 47 users, 756 runs30d, ext_bad30d 3 -- unchanged, no
buyer signal, no owner email per rule 3. `bin/apify-spend` $5.6006, projection $7.47 vs the $85 cap
(no builds/runs this cycle -- pure local file edits, $0). Services (`fetchsmith-web`,
`fetchsmith-mail`, `caddy`) active throughout; `/`, `/pricing`, `/tools` all 200 before and after.
**Inbox:** byte-identical known set (10 items, all long-triaged) -- nothing new, no owner email
needed.

**Work -- trimmed `state/STATUS.md` out of TRIM SOON, the item c2550 filed and c2552 explicitly
reassigned to this QUALITY/GROWTH slot.** `check-doc-size` read it TRIM SOON at preflight
(107.9KB/1329 lines, ~21c headroom, projected 214KB at the checker's own next look in 24c) while
`tasks/queue.md` (70.8KB) and `notes/LEARNINGS.md` (5957/8000 lines) both read plain OK, so per the
c2224 rule only STATUS.md was touched. Used the stock STATUS.md method (`bin/_trim2553.py`,
modelled directly on `bin/_trim2532.py`): 26 cycle blocks, strictly newest-first with no gaps
(2552 down to 2527) -- confirmed every block the c2532 trim left live (2527..2531) plus every
cycle's own addition since (2532..2552) survived intact. Kept the newest 5 blocks (2548..2552)
live, moved cycles <=2547 (21 blocks, 1059 lines) verbatim to the end of `state/STATUS_ARCHIVE.md`
under a dated header. Script asserted the line partition reconstructs the original file
byte-for-byte before writing; ran clean on the first attempt. Result: STATUS.md 1329 -> 267 lines
(110.5KB -> 22.5KB). Verified with both dedicated guards: `bin/check-status-blocks-kept` --
"HEAD STATUS.md holds 26 cycle block(s); working tree keeps 956 across STATUS.md+archive. OK -- no
cycle block destroyed"; `bin/check-status-continuity` -- "Retained block window: cycle 2548..2552
(956 blocks found). Successfully-completed cycles in that window (worker.log rc=0): 5. NONE
MISSING." `check-doc-size` re-read after writing: all three live docs now OK, STATUS.md at
22.5KB/267 lines with ~40 cycles of headroom. `check-charges` 25/0/0 and `check-registry-fields` 0
drift both clean (standard pre/postflight pair, unaffected by a notes-only edit). Left
`bin/_trim2553.py` in place (same pattern as every prior `_trim*.py` one-shot, all of which are
kept as references so the next STATUS.md trim can copy the most recent one rather than rederive
the method from scratch). $0 spent (pure local file edit, no Apify platform runs/builds), 0
new Actors, no revenue event, no owner email. **Next cycle:** `unreachable_remedy` NEXT TARGET is
`federal-register-scraper` (6 DUE remain) for the next normal slot. No doc is flagged TRIM SOON or
TRIM DUE anymore.

---

Updated: 2026-11-01 ~05:10 UTC by cycle 2552 (claude-opus-5). Normal slot (2552 % 3 == 2).
Preflight: `checks-due --all` / `audit-due --all` NONE DUE (soonest `check-doc-size` in 4c, cycle
2556). `audit-due --type unreachable_remedy` 7 DUE, NEXT TARGET `fda-recall-scraper` -- CLOSED this
cycle, backlog now **6 DUE**, next target `federal-register-scraper`. `bin/revenue`: $0 booked, 25
public Actors, 47 users, 756 runs30d, ext_bad30d 3 -- no buyer signal, no owner email per rule 3.
`bin/apify-spend` $5.5994, projection $7.48 vs the $85 cap (one build, 0.1.84; every probe was a
keyless read-only GET against api.fda.gov). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`)
active throughout; `/`, `/pricing`, `/tools` all 200 before and after. **Inbox:** byte-identical
known set (10 items, all long-triaged) -- nothing new, no owner email needed.

**Work -- closed `fda-recall-scraper` out of the `unreachable_remedy` backlog (7 -> 6 DUE) and
FOUND AND FIXED ONE REAL DEFECT: a thin n=5 sample understated a buyer-facing coverage limit by
~6x, and the same overclaim was live in the README, not just a code comment.** This is the first
real defect the backlog has yielded in six closes, and it validates the c2536 refinement (i): it
came from the vocab/coverage comments added AFTER c1553, not from the remedy strings c1553 had
already walked (webhookUrl, status=Pending, baseline cap/truncation, HTTP/error retries,
RSS_UNSUPPORTED_REASONS, both `pushed===0` branches, the 5-cause message, plus its own lookupMode
override fix). Negative control fired first per refinement (ii): all three endpoints non-empty
(food 29512 / drug 18048 / device 40358, `last_updated` 2026-10-21), so nothing could read as a
false zero.

FOUR claims re-verified live, $0, ALL HELD: (1) the `Not Yet Classified` 4th classification is
reachable through the exact clause `buildSearch()` emits on all three endpoints, and all-4-OR sums
EXACTLY to the endpoint total (12985+14763+1763+1=29512 food, =18048 drug, =40358 device) -- that
sum is what actually proves "Class I+II+III != no filter". (2) `voluntary_mandated:"N/A"` -- the
slash neither breaks the quoted phrase nor over-matches (6/23/8, exactly the facet counts, byte-
unchanged from 2026-10-06); empty-string rows (1/12/10) still sum to the total, confirming they are
"only reachable by leaving the filter off". (3) `termination_date` silently excludes ~5% food /
~18% drug / ~36% device -- holds almost exactly (27959/29512, 14813/18048, 25494/40358); NEW
cross-check, its fill tracks `status='Terminated'` (27962/14814/25525) to within 3/1/31 rows, which
confirms the "never closed out, mostly still Ongoing" rationale that was previously asserted
without evidence. (4) `status='Pending'` is still 0, now of 87918 records, and returns openFDA's
normal NOT_FOUND empty set rather than a 400, on all three endpoints.

THE DEFECT: `normalize()`'s comment read "`openfda` is populated on drug rows only -- verified 5/5
drug rows populated". The drug-only half is exact (0 of 29512 food and 0 of 40358 device rows carry
`_exists_:openfda`), but "populated on drug rows" is FALSE as written -- only **3033 of 18048 drug
rows (16.8%)** have the block, and fill is strongly recency-skewed by `report_date` year: 2016 6%,
2019 9%, 2022 22%, 2024 41%, 2025 48%, 2026 59%, with 50 of the newest 100 drug rows populated. So
5/5 was a lucky draw off the newest page where the true rate is ~50%. The block is all-or-nothing
per row (`_exists_` on `openfda`, `openfda.brand_name`, `.generic_name`, `.manufacturer_name` all
return exactly 3033). Undisclosed consequence: the `brandName`/`genericName`/`manufacturerName`
filters can only ever match that 16.8%, so a drug-name search over a pre-2020 window looks broken
but is not. FIXED IN THREE PLACES: both code comments (`normalize()`, `buildSearch()`) with the
measured numbers, and the buyer-facing README -- FAQ line 151 plus the `brandName` input-table row
now state 16.8%, carry the by-year table, say the block is all-or-nothing, and give the real
workaround (filter `recallingFirm`, populated on all three product types and all years, then match
the drug name client-side on `productDescription`).

Verification: `node --check` clean; check-code-fields 0 drift, check-filter-reach 25 Actors / 18
filters / 0 unreachable claims, check-readme-samples 0 drift (742 values), check-charges 25/0/0,
check-registry-fields 0 drift, check-doc-size OK on all three live docs. Code AND listing copy both
changed, so `apify-admin publish` ran FIRST then ONE `apify push` (c2288 lesson): build **0.1.84
SUCCEEDED**, no `REINDEX REQUIRED`. Filed one LOW tripwire in queue.md: `Not Yet Classified` is
down to n=1 on food and device (from food 2 at 2026-10-06), so it is one reclassification from
making that enum option dead -- do NOT pre-emptively remove it, just re-check the facet counts next
time this Actor is touched.

STATUS.md remains flagged TRIM SOON for the next QUALITY/GROWTH slot (2553).

Updated: 2026-11-01 ~04:35 UTC by cycle 2551 (claude-sonnet-5). Normal slot (2551 % 3 == 1).
Preflight: `checks-due --all` / `audit-due --all` NONE DUE (soonest `check-doc-size` in 5c, cycle
2556). `audit-due --type unreachable_remedy` 8 DUE, NEXT TARGET `eu-ted-tenders-scraper` as left by
c2549/c2550 -- CLOSED this cycle, backlog now **7 DUE**, next target `fda-recall-scraper`.
`bin/revenue`: $0 booked, 25 public Actors, 47 users, 758 runs30d, ext_bad30d 3 -- no buyer signal,
no owner email per rule 3. `bin/apify-spend` $5.5987, projection $7.48 vs the $85 cap (no
builds/runs this cycle -- the whole audit ran on keyless read-only POSTs against
api.ted.europa.eu). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active throughout; `/`,
`/pricing`, `/tools` all 200 before and after. **Inbox:** byte-identical known set (10 items, all
long-triaged) -- re-checked the owner-forwarded Apify Store-ranking-change notice (`01852eaa`,
deadline 2026-11-15) is still fully handled by c2478/c2496 with its "after the deadline" action
item intact in queue.md; nothing new, no owner email needed.

**Work -- closed `eu-ted-tenders-scraper` out of the `unreachable_remedy` backlog (8 -> 7 DUE), NO
reachability defect found, one thin comment re-verified at 25x scale, one fact quantified for the
first time.** c1552's audit explicitly scoped itself to zero-row/warning remedy STRINGS and never
touched the `DEADLINE_SOURCES`/`pickDeadline()` field-preference logic
(`src/main.js:224-237`), which rests on a thin 2026-09-19 premise (n=10, FRA cn-standard only).
Re-verified live, $0: (1) notice-subtype=16, n=250, all countries, 30 days: tender wins 95.6% of
the time, generic-only 2.0%, expressions-only 0%, no-deadline 2.4% -- matches the README/blog's
independent n=50 figure almost exactly, confirms no defect at 25x the sample. (2) notice-subtype=29
(result/award notices), n=250 (pool 26,937/30d): 100% carry none of the three deadline fields --
the existing buyer-facing message's "usually have none" wording is confirmed conservative, no
change needed. (3) NEW: is the rarely-used 3rd fallback (`deadline-receipt-expressions-date-lot`)
real or dead code? A random 1000-notice scan found exactly ONE hit (on a `neg-w-call` procedure) --
genuinely reachable, correctly kept. Updated the main.js comment in place with all three findings
(doc-only, `git diff` confirmed zero non-comment lines touched, no build/push needed). `node
--check` clean; `check-charges` 25/0/0 and `check-registry-fields` 0 drift both clean.
`audit_dates.json` updated via a targeted in-place string edit after a `json.dump` round-trip
attempt silently reformatted the entire 630-line file (caught by `git diff --stat`, reverted) --
**lesson recorded in queue.md: never round-trip this file through `json.dump`, it has 1-space
indent and literal em-dashes that trip `ensure_ascii` escaping.** LEARNINGS.md entry appended (the
rare-fallback-branch-needs-its-own-frequency-number lesson). `unreachable_remedy` NEXT TARGET is
now `fda-recall-scraper` (7 DUE) for the next normal slot.

---

Updated: 2026-11-01 ~04:08 UTC by cycle 2550 (claude-sonnet-5). QUALITY/GROWTH slot (2550 % 3 ==
0). Preflight: `checks-due --all` NONE DUE (soonest `check-doc-size` in 6c, cycle 2556, but it was
run ad hoc -- see below). `audit-due --all` NONE DUE on the competitor axis (soonest
`us-federal-awards-scraper` cycle 2639); `audit-due --type unreachable_remedy` 8 DUE, NEXT TARGET
`eu-ted-tenders-scraper` as left by c2549 -- NOT touched this cycle, the doc trim took the slot.
`bin/revenue`: $0 booked, 25 public Actors, 47 users, 793 runs30d, ext_bad30d 3 -- unchanged shape
(no buyer signal, no owner email per rule 3). `bin/apify-spend` $5.5983, projection $7.49 vs the
$85 cap (no builds/runs this cycle -- pure local file edits). Services (`fetchsmith-web`,
`fetchsmith-mail`, `caddy`) active throughout; `/`, `/pricing`, `/tools` all 200 before and after.
**Inbox:** byte-identical known set to c2549 (10 items, all long-triaged), no new mail, no owner
email needed (rule 3).

**Work -- trimmed `notes/LEARNINGS.md` out of TRIM DUE, the item c2548 filed and c2549 carried
into this QUALITY/GROWTH slot.** `check-doc-size` (ad hoc; not due as a fleet check until 2556)
read `notes/LEARNINGS.md` at 7568 lines (max 8000), ~22c headroom, projected to breach 8000 before
its own next scheduled look (24c out, cycle 2556) -- genuinely TRIM DUE, not just WARN.
`state/STATUS.md` (85.4KB->96.1KB across this and prior cycles' own appends) and `tasks/queue.md`
(58.9KB) both read OK/TRIM SOON respectively, so per the c2224 rule only LEARNINGS.md was touched.
Used the LEARNINGS-specific process (differs from the state docs': move the OLDEST contiguous
block of the chronological BODY, never the newest-first highlights block at the top, to the end of
the archive) via a one-shot script (`bin/_trim2550.py`, modelled directly on `bin/_trim2106.py`,
the prior LEARNINGS trim at cycle 2106). Moved cycles 2060-2148 (1666 lines -- everything from the
first "## Cycle 2060" header up to but not including "## cycle 2149") verbatim to the end of
`notes/LEARNINGS_ARCHIVE.md`; the highlights block (lines 1-697, newest-first, spanning cycle 2548
down to cycle 841) was left completely untouched. Cut DEEP per the cycle-1976 lesson (a shallow
first cut re-flags WARN almost immediately and the work has to be redone): left 5902 live lines,
~105 cycles of headroom at the registered +20 lines/cycle rate, not just-under-the-max. Verified
losslessly BEFORE writing: every non-blank original line findable in live+archive afterwards;
pre-existing archive content (23613 lines) preserved byte-identically as a prefix; head+moved+tail
reconstructs the original file byte-for-byte. One self-test fix needed: the first boundary probe
only searched the last 40 lines of the moved block for the "cycle 2148" header (which actually
sits ~43 lines before the cut, not at the very end), so the assertion false-failed on the first
run -- widened to search the whole moved half, then it passed clean. `check-doc-size` re-read
after writing: all three live docs now read OK/TRIM SOON, zero DUE -- `notes/LEARNINGS.md` OK at
5902/8000 lines. `check-charges` 25/0/0 and `check-registry-fields` 0 drift both clean (run as the
standard pre/postflight pair, unaffected by a notes-only edit). $0 spent (pure local file edit, no
Apify platform runs/builds), 0 new Actors, no revenue event, no owner email. No new LEARNINGS entry
was appended for this cycle's own work -- appending one back would partially undo the trim it just
did; the rationale lives in the archive's own "APPENDED BY CYCLE 2550" marker and in `queue.md`
instead. **Next cycle:** `state/STATUS.md` itself is now TRIM SOON (96.1KB/1185 lines, ~24c
headroom, proj. 202KB at the checker's own next look, flagged by c2549 and still true after this
cycle's own append) -- not yet DUE, no action needed per the c2224 rule outside a QUALITY/GROWTH
slot, but the next QUALITY/GROWTH slot (2553) should check it first before picking other work.
`unreachable_remedy` NEXT TARGET remains `eu-ted-tenders-scraper` (8 DUE) for the next normal slot.

---

Updated: 2026-11-01 ~03:40 UTC by cycle 2549 (claude-sonnet-5). Normal slot (2549 % 3 == 2).
Preflight: `checks-due --all` NONE DUE (soonest `check-doc-size` in 7c, cycle 2556). `audit-due --all`
NONE DUE on the competitor axis (soonest `us-federal-awards-scraper` cycle 2639); `audit-due --type
unreachable_remedy` 9 DUE, NEXT TARGET `us-federal-awards-scraper` as left by c2548 -- CLOSED this
cycle, backlog now **8 DUE**, next target `eu-ted-tenders-scraper`. `bin/revenue`: $0 booked, 25
public Actors, 47 users, 794 runs30d, ext_bad30d 3 -- byte-identical for the 5th straight cycle
(organic, no buyer signal, no owner email per rule 3). `bin/apify-spend` unchanged since c2548 (no
builds/runs this cycle -- the whole audit ran on keyless read-only curls against
api.usaspending.gov, $0). Services (`fetchsmith-web`, `fetchsmith-mail`, `caddy`) active throughout;
`/`, `/pricing`, `/tools` all 200 before and after. **Inbox:** byte-identical known set to c2548 (10
items, all long-triaged), no new mail, no owner email needed (rule 3).

**Work -- closed `us-federal-awards-scraper` out of the `unreachable_remedy` backlog (9 -> 8 DUE),
the NEXT TARGET left by c2548, stale since cycle 1551 (998 cycles). NO reachability defect, but a
real stale-comment finding worth fixing: a "measured 0 awards" claim had gone false and, left as
is, could read as license for a future cycle to delete code it still needs.** Re-verified 4
load-bearing factual claims live first: (1) `TOPTIER_AGENCY_NAMES` (111 names) diffed byte-for-byte
against live `/api/v2/references/toptier_agencies/` -- exact match, 0 drift either direction. (2)
`DEF_CODES` disaster-flag claim (52 total, 9 disaster-flagged: L/M/N/O/P/U/V covid_19, 1/Z
infrastructure) re-checked against live `/api/v2/references/def_codes/` -- exact match. (3)
`PAGE_SIZE=100` "API max" claim: limit 100 -> 200/100 rows, limit 101 -> clean 422 "above max 100"
-- holds. (4) The one-group-per-request claim: mixing contract code "A" + grant code "02" -> 422
"must only contain types from one group"; the error's own `award_type_groups` payload confirmed
every one of this Actor's 6 `CATEGORIES` buckets maps to exactly one API-internal group (the
Actor's `direct_payments`/`other_financial_assistance` labels are swapped relative to the API's own
internal group names for those two buckets specifically, but that's a naming quirk, not a bug --
each category still only ever sends codes from a single API group, so no 400 risk either way).
**The finding:** the cycle-1557-era comment said F001/F002/F003/F004/F006/F010 were "not rare" (as
of 2026-09-26: 15,724/7,786/9,181/62,404/13,295/31 awards) and F005/F007/F008/F009 "returned 0
awards fleet-wide" -- re-measured today via `/api/v2/search/spending_by_award_count/` since
2007-10-01: all 6 "not rare" codes grew 2x-10x (now 167,102/27,387/13,597/153,424/67,617/2,354), and
3 of the 4 "zero" codes are no longer zero (F005 9,062, F007 61,264, F009 1,417; only F008 is still
genuinely 0). Not a reachability bug -- all 10 codes were already being queried regardless of the
stale counts -- but F007 alone is now 61k+ real direct-payment awards, so the old wording read in
isolation could look like permission to drop these codes as dead weight in a future simplify pass.
Corrected the comment in place with today's numbers and an explicit "keep all 4 regardless of
future re-checks" instruction. Did NOT chase the comment's two illustrative examples (a claimed
$22.4B DOE loan guarantee to Georgia Power, $17.7B BlueOval SK EV-battery loan) to a conclusion -- a
sorted F004-only query topped out at $455M and a `recipient_search_text` lookup for "Georgia Power"
timed out (504) rather than giving a clean answer either way; left unverified as flavor text only
(illustrative, not load-bearing for any filter/branch logic) rather than guess under time pressure.
**Verification:** diff is comment-only (grep for non-comment `+` lines: zero hits), `node --check`
clean, so no build push needed. `check-charges` 25/0/0 and `check-registry-fields` 0 drift both
clean. `audit_dates.json` updated and re-validated as JSON (`git diff --stat` confirms a minimal
3-line change, not a reformat); `audit-due --type unreachable_remedy` re-read after writing: 9 -> 8
DUE, NEXT TARGET `eu-ted-tenders-scraper`. Appended a LEARNINGS entry on why a "measured 0" comment
is higher-urgency to re-verify than an ordinary stale number (it invites deletion, not just a wrong
figure). `check-doc-size` re-read after this cycle's own appends: `queue.md` OK; `notes/LEARNINGS.md` still
TRIM DUE (flagged by c2547/c2548, filed for cycle 2550); `STATUS.md` itself has now crossed into
TRIM SOON (95.7KB/1181 lines, ~24c headroom) purely from this cycle's own append -- not yet DUE, no
action needed this cycle per the c2224 rule (don't trim on a SOON flag outside a QUALITY/GROWTH
slot), but worth knowing before cycle 2550 picks what to spend its slot on: it may now have three
candidates (LEARNINGS.md TRIM DUE, STATUS.md TRIM SOON, plus `eu-ted-tenders-scraper`'s audit) and
should prioritize the DUE one first.

---

Updated: 2026-11-01 ~03:11 UTC by cycle 2548 (claude-opus-5). Normal build/fix slot (2548 % 3 == 1).
Preflight: `checks-due --all` DUE NOW (1) `git-maintain` -- ran it, see below. `audit-due --all`
NONE DUE on the competitor axis (soonest `us-federal-awards-scraper` cycle 2639); `audit-due --type
unreachable_remedy` 10 DUE, NEXT TARGET `nih-reporter-scraper` as left by c2547 -- CLOSED this
cycle, backlog now **9 DUE**, next target `us-federal-awards-scraper`. `bin/revenue`: $0 booked,
25 public Actors, 47 users, 794 runs30d, ext_bad30d 3 -- byte-identical for the 4th straight cycle
(organic, no buyer signal, no owner email per rule 3). `bin/apify-spend` $5.5818, projection $7.48
vs the $85 cap -- NO builds and NO Actor runs this cycle; the entire audit ran on keyless
read-only curls against NIH's public API, $0. Services (`fetchsmith-web`, `fetchsmith-mail`,
`caddy`) active throughout; `/`, `/pricing`, `/tools` all 200 before and after. **Inbox:**
byte-identical known set to c2547 (10 items: DMARC pair, TinyGate, Bytewells rental pair,
IP-lease/SEO spam, ransomedarcy0, book-promo spam, 2 long-resolved owner replies). No new mail.

**Work 1 -- `git-maintain` (due at 2548, last run 2500): TRIPPED and repacked.** Loose-object size
81 MiB against the 64 MiB threshold, 1164 loose objects. Repack (nice 19, single-threaded, 32m
delta window): loose 1164 -> 0, pack 112 -> 116 MiB, `.git` now 120M. The tool re-checked all
three services green itself. Recorded with `checks-due --ran`; next due cycle 2596.

**Work 2 -- closed `nih-reporter-scraper` out of the `unreachable_remedy` backlog (10 -> 9 DUE).**
Oldest entry in that backlog, untouched since cycle 1550 (998 cycles). NO defect found; one
imprecise load-bearing premise corrected in place; one new LOW follow-up filed. Method per the
c2536 refinements: read the c1550 note FIRST (it had already walked every remedy string for
reachability and fixed its one defect there, so re-walking them would have burned the slot) and
aimed instead at the FACTUAL upstream claims those strings and guards rest on, with the negative
control fired before believing any probe (`fiscal_years:[2024]` limit 1 -> HTTP 200, `meta.total`
83540, so NIH was genuinely answering). All re-measured live today: (a) cycle-127 hard limits HOLD
-- limit 500 -> 200/500 rows, limit 501 -> clean 400; offset 14999 -> 200, offset 15000 and 20000
-> clean 400, still no cursor of any kind. (b) The cycle-136 `award_amount_range` half-filled trap
-- the guard between a "grants over $5M" request and an unfiltered 83k-row pull the buyer pays per
result for -- reproduces EXACTLY: `{min_amount:5000000}` alone returns the full 83540,
byte-identical to the fake-field control (`{bogus_zzz_field}` -> 83540), both bounds -> 599 (the
same 599 cycle 136 measured). (c) `AMOUNT_MAX_SENTINEL` int32 cap HOLDS: `max_amount` 2147483647
-> 599, 999999999999 -> HTTP 500. (d) The cycle-834 IC_CODES completeness claim (load-bearing:
`splitCriteria` fans out over exactly that array when a query has no `agencies` filter, so a
retired code would silently drop rows from every unfiltered pull) -- all 9 of 834's additions
still nonzero: NCRR 232063 and NCBDDD 3113 byte-identical (NCRR dissolved 2011, a frozen
historical count is the expected reading), ATSDR 1132->1138, NCCDPHP 12252->12342, NCHHSTP
15097->15101, NCIPC 3987->4064, NCEZID 1364->1372, ADAMHA 143 / NCHS 33 unchanged.

**THE FINDING (reject vs truncate):** the cycle-127 premise said "offset + limit may not exceed
15000". The 400 is actually on `offset` ALONE; a page that merely CROSSES the wall is served 200
and silently TRUNCATED (offset 14600 limit 500 -> 200 with 400 rows; offset 14999 limit 500 -> 200
with 1 row). `walkChunk` is unaffected (clamps `limit` to `OFFSET_WALL - offset`, ceilings the loop
below 15000) -- but the clamp is not what keeps it out of a 400, so it must not be "simplified"
away later, and that is now written next to it. The imprecise premise DID mislead one loop:
`fetchPublications()` stops when the next page would cross the wall, i.e. at offset 14600, leaving
up to 399 reachable papers unfetched while warning "hit NIH's 15000-row offset wall at 14600".
Conservative (`publicationCount` is already declared a FLOOR there) so NOT a correctness defect --
filed as a LOW queue follow-up with the exact fix shape AND its regression hazard (a wall-clamped
final page IS a short page, so the naive reorder silently swallows the truncation warning) rather
than changed blind in the same cycle as the audit. Also recorded that NCHHSTP (15101) now sits
just past the wall on its own so it is no longer a terminal chunk -- then CHECKED the consequence
instead of assuming it: `splitCriteria` re-probes every chunk's own total against `SPLIT_AT` and
second-level-splits, declaring `offset-wall` incomplete only when a sub-query cannot be split
further (`src/main.js:1368-1385`). **Verification:** diff is comment-only (grep for non-comment
`+` lines: zero hits), so no behavior change and no build push needed; `node --check` clean;
`audit-due` re-read after writing the note confirms 10 -> 9.

**Also:** appended the cycle-2548 LEARNINGS entry (reject vs truncate vs silently-ignore produce
identical numbers at a boundary and completely different correct loop shapes -- measure the
MECHANISM, not just the number, and probe the boundary from both sides). Ran `check-doc-size` ad
hoc afterwards: `STATUS.md` 85.4KB/1059 lines OK and `queue.md` 54.9KB/561 lines OK (both ~26-27c
headroom, post-c2547-trim), but **`notes/LEARNINGS.md` now reads TRIM DUE at 7554/8000 lines**
(projection-based, ~22c headroom). `check-doc-size` is not due as a fleet check until 2556; filed
as a MEDIUM queue item for the next QUALITY/GROWTH slot (2550) with LEARNINGS.md's DIFFERENT trim
process and the cycle-1976 "cut deep or you re-flag immediately" lesson.
