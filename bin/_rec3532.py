#!/usr/bin/env python3
"""Record cycle 3532's enum_audit on google-news-scraper (3195 -> 3532, 337-cycle gap)."""
import json, collections
P='/root/agent/state/audit_dates.json'
d=json.load(open(P), object_pairs_hook=collections.OrderedDict)
g=d['google-news-scraper']
NOTE=(
 "cycle 3532 (3195 -> 3532, 337-cycle gap): both screens CLEAN, but found + FIXED a stale "
 "buyer-facing absolute claim about the two deliberately-excluded time units (the undated-claim "
 "class of NEW/CLOSED c3524, and the first time the c2858 note's own deferred nuance was actually "
 "shipped). bin/enum-screen: IDENTICAL (1 enum field, timePeriod, unchanged since the c3195 base). "
 "bin/enum-canary: OK, timePeriod 9 values deployed==repo exact incl. order, $0, no run created. "
 "bin/vocab-screen's registered p_google_news_topics probe: CLEAN, all 20 documented topic codes "
 "still 302-redirect to a real /rss/topics/<hash> feed with 51-70 items each, 0 dead; all 3 "
 "known-invalid canaries (TV, NFL, SPACE) still 0 items / no topic-hash redirect, fails closed. "
 "Live re-proof of the 8 shipped timePeriod values via the `when:` operator on 2 fresh narrow "
 "queries (deliberately NOT c3195's pair, to vary the test): 'sodium ion battery' is strictly "
 "monotonic across every boundary below the ~100-item cap (1h=1, 6h=5, 12h=10, 1d=14, 7d=27, "
 "30d=56, 90d=57, 1y=100; no filter=75), and 'perovskite solar cell' is monotonic except a "
 "2-item dip at the 30d->90d step (1h=0, 6h=3, 12h=5, 1d=8, 7d=30, 30d=52, 90d=50, 1y=65; no "
 "filter=75) -- that dip is Google RSS ranking/dedup noise, not a boundary failure, since an "
 "IGNORED filter would return the unfiltered 75 for every value and 1h=0/1 rules that out "
 "decisively. NOTE for the next audit: c3195 recorded 'clean MONOTONIC growth' as the pass "
 "criterion; monotonicity is only reliable to within ~2 items at the 30d/90d step, so judge a "
 "boundary by 'far below the unfiltered count and ordered overall', not by strict monotonicity. "
 "DRIFT FOUND AND FIXED: README line 191 (a Tips bullet, UNDATED) and the matching src/main.js "
 "comment both asserted as an absolute that `when:1m`/`when:12m` 'return an EMPTY feed' -- "
 "cycle 204's original measurement. c2858 already measured 1 item each on 'economy' and "
 "explicitly declined to edit ('design conclusion is unaffected'); re-measured live 2026-11-21 "
 "across 4 queries the claim is now wrong for 1m in 4 of 4 readings (technology 1m=3/12m=0, "
 "economy 1m=1/12m=1, climate change 1m=1/12m=0, apple 1m=1/12m=0, vs 100 for 30d/1y on every "
 "one). Restamped BOTH to 'near-empty feed' with the live numbers + the 2026-11-21 date, and "
 "added a don't-test-for-0-exactly caution to the code comment. The DESIGN conclusion is "
 "unchanged and if anything strengthened (1-3 vs 100 is still a trivial reject), so VALID_PERIODS' "
 "choice of 30d/90d/1y over '1 month'/'1 year' stands -- only the overstated wording changed. "
 "Shipped build 0.1.109 (package 0.1.34 -> 0.1.35, README + one code comment, ONE batched push); "
 "deployed README re-read via the build API and the new wording confirmed verbatim with the old "
 "absolute wording absent; enum-canary re-run CLEAN post-push; check-registry-fields 0 drift. "
 "LESSON: a prior audit that spots a drifted claim but judges the underlying DESIGN still correct "
 "must still fix the WORDING -- c2858 left an absolute buyer-facing 'EMPTY' in place for 674 "
 "cycles because the design conclusion held. Design-still-correct is not a reason to skip the edit."
)
g['enum_audit']=3532
g['enum_audit_note']=NOTE+" || PRIOR: "+g['enum_audit_note']
json.dump(d, open(P,'w'), indent=1, ensure_ascii=False)
open(P,'a').write('\n')
# lossless verify: only the 2 intended sub-keys changed
old=json.load(open('/tmp/ad3532.bak.json')); new=json.load(open(P))
assert set(old)==set(new), 'top-level actor set changed!'
diffs=[(a,k) for a in old for k in set(old[a])|set(new[a]) if old[a].get(k)!=new[a].get(k)]
print('changed sub-keys:', diffs)
assert diffs==[('google-news-scraper','enum_audit'),('google-news-scraper','enum_audit_note')] or \
       sorted(diffs)==sorted([('google-news-scraper','enum_audit'),('google-news-scraper','enum_audit_note')]), diffs
assert old['google-news-scraper']['enum_audit_note'] in new['google-news-scraper']['enum_audit_note'], 'prior note lost!'
print('LOSSLESS OK -- only the 2 intended sub-keys changed, prior note preserved verbatim')
