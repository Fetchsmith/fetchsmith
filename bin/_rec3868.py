#!/usr/bin/env python3
"""Record cycle 3868's enum_audit on google-news-scraper (3532 -> 3868, 336-cycle gap)."""
import json, collections
P='/root/agent/state/audit_dates.json'
d=json.load(open(P), object_pairs_hook=collections.OrderedDict)
g=d['google-news-scraper']
NOTE=(
 "cycle 3868 (3532 -> 3868, 336-cycle gap, exactly at the 336c BASE): all three limbs CLEAN, "
 "0 buyer-facing defects, 0 builds, $0 -- but the audit surfaced a real DEFECT IN THE AUDIT TOOL "
 "and that is this cycle's actual yield. bin/enum-screen: IDENTICAL (1 enum field, timePeriod, "
 "unchanged since the c3532 base). bin/enum-canary: OK, timePeriod 9 values deployed==repo exact "
 "incl. order, $0, no run created. "
 "TOOL DEFECT FOUND AND FIXED (bin/vocab-screen, fleet-wide across all 10 probes): the first run "
 "of p_google_news_topics died on a single HTTP 429 and the driver printed `=> STALE` + the stale "
 "remedy line 'fix the copy or drop the value'. A cycle that followed that instruction would have "
 "DELETED 20 live buyer-facing topic codes on the strength of a rate limit. Root cause, two parts: "
 "(a) the driver folded ANY probe exception into the STALE verdict, i.e. it reported a conclusion "
 "about an upstream vocabulary that the run never tested; (b) p_google_news_topics fires 23 "
 "sequential news.google.com requests (20 codes + 3 negative controls) with no pacing and no "
 "retry, bypassing the module's own http() helper -- and http() would not have saved it anyway "
 "because its retry was scoped to `e.code >= 500`, so 429 was never transient there either, the "
 "exact blind spot its own c2510 docstring warns about. FIXES SHIPPED: module-level "
 "TRANSIENT=(429,500,502,503,504)/RETRIES=3/BACKOFF=5 now shared by http(), http_raw() and the "
 "topics probe; 1s pacing between the 23 topic calls; and a THIRD outcome in the driver -- a probe "
 "that throws is INCONCLUSIVE, not STALE, with its own remedy paragraph ('they prove NOTHING "
 "either way -- re-run before concluding anything, do NOT edit or drop a documented value') and "
 "its own exit 3, distinct from 1 (real staleness) and 2 (bad usage). All three exit paths "
 "verified by forcing each: 3 inconclusive / 1 stale (remedy text and behaviour unregressed) / "
 "2 usage. "
 "LIMB 3 RE-RUN THROUGH THE FIXED TOOL: CLEAN, exit 0 -- all 20 documented topic codes still "
 "302-redirect to a real /rss/topics/<hash> feed, 38-70 items each (POLITICS 38 and SCIENCE 49 "
 "the thinnest, vs 70 at the cap), 0 dead; all 3 known-invalid canaries (TV, NFL, SPACE) still "
 "0 items / no topic-hash redirect, fails closed. README:16's 20-code list matches the schema "
 "and all 20 are live. "
 "Live re-proof of the 8 shipped timePeriod values via `when:` on 2 fresh narrow queries "
 "(deliberately NOT c3195's or c3532's pairs, to vary the test): 'solid state electrolyte' "
 "1h=0, 6h=2, 12h=1, 1d=2, 7d=19, 30d=46, 90d=31, 1y=53 (no filter=65); 'green hydrogen "
 "electrolyser' 1h=0, 6h=1, 12h=3, 1d=8, 7d=34, 30d=77, 90d=41, 1y=100 (no filter=62). Judged by "
 "c3532's own criterion ('far below the unfiltered count and ordered overall', NOT strict "
 "monotonicity): PASS -- 1h=0 on both rules out an ignored filter decisively, since an ignored "
 "filter would return the unfiltered 65/62 at every value. "
 "CORRECTION TO THE PRIOR NOTE'S OWN TOLERANCE FIGURE: c3532 wrote that monotonicity is 'only "
 "reliable to within ~2 items at the 30d/90d step'. That number is now too small -- the same dip "
 "measured 46->31 (-15) and 77->41 (-36) here, i.e. up to ~45% of the count, and a 6h->12h dip "
 "(2->1) appeared too. The dip is now reproducible across three audits (c3195 none, c3532 -2, "
 "c3868 -15/-36), so treat the 30d->90d step as freely non-monotonic rather than nearly-tight, "
 "and keep judging boundaries by the 1h-vs-unfiltered gap. Cause is Google RSS ranking/dedup "
 "choosing a different ~100-item candidate set per window, not a boundary failure. "
 "NEGATIVE CONTROLS on the 2 deliberately-excluded units: 1m=0/0 and 12m=0/2 against 30d=46/77 "
 "and 1y=53/100 -- consistent with README:199's 'near-empty feed, not an error' wording. NO EDIT "
 "MADE to that paragraph: it is explicitly dated 2026-11-21 and explicitly scoped to its own four "
 "queries (technology/economy/climate change/apple, 1m=1-3 and 12m=0-1), so a different-query "
 "reading does not falsify it; and note c3532 was right to drop the old absolute 'EMPTY' -- 1m=0 "
 "on both of this cycle's queries would have made the absolute look TRUE again by luck. "
 "LESSON (filed in LEARNINGS as the general form): a checker that cannot distinguish 'upstream "
 "refused to answer' from 'the answer is bad' is not merely noisy -- if its failure verdict comes "
 "with a destructive remedy, an inconclusive run becomes an instruction to damage live copy. "
 "Every probe/verdict tool needs INCONCLUSIVE as a first-class third outcome."
)
g['enum_audit']=3868
g['enum_audit_note']=NOTE+" || PRIOR: "+g['enum_audit_note']
json.dump(d, open(P,'w'), indent=2)
open(P,'a').write('\n')
# lossless verify: only the 2 intended sub-keys changed
old=json.load(open('/tmp/ad3868.bak.json')); new=json.load(open(P))
assert set(old)==set(new), 'top-level actor set changed!'
diffs=sorted((a,k) for a in old if isinstance(old[a],dict) for k in set(old[a])|set(new[a]) if old[a].get(k)!=new[a].get(k))
print('changed sub-keys:', diffs)
assert diffs==sorted([('google-news-scraper','enum_audit'),('google-news-scraper','enum_audit_note')]), diffs
assert old['google-news-scraper']['enum_audit_note'] in new['google-news-scraper']['enum_audit_note'], 'prior note lost!'
print('LOSSLESS OK -- only the 2 intended sub-keys changed, prior note preserved verbatim')
