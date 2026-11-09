import json
p='state/audit_dates.json'
d=json.load(open(p))
e=d['apple-podcasts-scraper']
note = (
 "cycle 2932 (2595 -> 2932, 337c gap, the top DUE varied_test). Picked the axis by counting every input key against "
 "the whole varied_test note history programmatically (same method as c2595): THREE keys had zero prior coverage ever "
 "-- searchLimit, includePodcastInfo, maxReviewsPerPodcast. Tested the first two in 2 capped runs; maxReviewsPerPodcast "
 "is still uncovered and is the natural c3268-ish target. "
 "AXIS 1, searchLimit -- PASS, no defect. Verified the upstream contract FREE first (curl itunes.apple.com/search "
 "limit=2 for 'bitcoin' and 'gardening' -> resultCount 2 each), so a row-count mismatch could only be ours. LIVE RUN "
 "{dataType:'podcasts', searchTerms:['bitcoin','gardening'], searchLimit:2, maxResults:10} -> 4 rows, exactly 2 per "
 "term, each row's searchTerm column correctly attributing it to the term that found it (Simply Bitcoin / The Wolf Of "
 "All Streets; Garden Girls Podcast / The joe gardener Show). Designed so a pass is informative: a silently-ignored "
 "searchLimit would have given 10 rows (default 10/term, clipped by maxResults) heavily skewed to the first term, so "
 "4-split-2-2 discriminates honoured-per-term from ignored AND from misread-as-a-global-cap. "
 "AXIS 2, includePodcastInfo -- REAL BUYER-FACING CLAIM DEFECT FOUND AND FIXED (docs, build 0.1.121). Read the row "
 "builders first and predicted the asymmetry from code: episodeRow (src/main.js ~645) emits podcastName from the "
 "episode's OWN e.collectionName and feedUrl from e.feedUrl, unconditionally, with `...(info || {})` spread last -- so "
 "info only ADDS fields. LIVE RUN {podcasts:[lex-fridman id1434243584], dataType:'episodes', maxEpisodesPerPodcast:3, "
 "maxResults:3, includePodcastInfo:false} -> 3 rows; varied-test's NOT-A-FIELD split (absent key vs real null, the "
 "c2160 guard) confirmed exactly the prediction: artistName/primaryGenre/episodeCount/podcastUrl ABSENT from all 3 "
 "rows, while podcastName ('Lex Fridman Podcast') and feedUrl ('https://lexfridman.com/feed/podcast/') were still "
 "THERE. Both the input_schema description and README input-table row claimed the toggle attaches 'show name, host, "
 "genre, RSS feed and episode count to every row' -- i.e. the documented effect was WRONG IN 3 OF 5 MODES, read off "
 "the code: (a) episodes via Apple lookup -- podcastName and feedUrl survive the toggle, only the other four drop; "
 "(b) episodes with useRssForFullArchive -- rssEpisodeRow (~701) reads podcastName/feedUrl FROM info, so there all six "
 "DO drop, i.e. the same toggle on the same dataType behaves differently depending on the source; (c) reviews -- the "
 "inline review item (~1066) carries no show fields of its own and `...(info || {})` is the only source, so all six "
 "drop; (d) podcasts and publisher -- podcastRow (~626) never consults includePodcastInfo at all, so the toggle is a "
 "pure NO-OP there, yet README said 'every row'; (e) charts -- genuinely honoured (~1254 skips the per-show detail "
 "lookup) and already documented correctly at README:127. "
 "FIX IS DOCS ONLY, DELIBERATELY: the behaviour is correct and strictly better than documented -- podcastName/feedUrl "
 "ride along free on Apple's episode payload and cost no extra request, so stripping them to match the old prose would "
 "make the product worse for every buyer and help nobody. Rewrote the input_schema description and the README input "
 "table row to state the per-mode truth. Buyer consequence of the old copy: anyone setting includePodcastInfo:false to "
 "shed show metadata (row size, privacy of pipeline shape) was told podcastName and feedUrl would be gone when they "
 "are not, and anyone setting it on dataType podcasts/publisher expected a change that cannot happen. "
 "PROCESS NOTE worth reusing: do NOT round-trip .actor/input_schema.json through json.dump to edit one string -- the "
 "file is 2-space-indented with ensure_ascii-style \\u2014 escapes, so a dump at indent=4 reformatted all 438 lines "
 "(869-line diff) and even indent=2 with ensure_ascii=False still rewrote 187 lines by unescaping the em-dashes. "
 "git checkout + a surgical text replace of the one description line gave the correct 1-line diff. "
 "VERIFIED LIVE after push (build 0.1.121, latest tag): build readme 73792 bytes live == 73792 local, byte-identical "
 "(compared as encoded UTF-8, the c2595 lesson), and actorDefinition.input.properties.includePodcastInfo.description "
 "identical to local. No-regression run on the unchanged default test_input.json -> 5/5 episodes, and with the toggle "
 "ON artistName='Lex Fridman'/primaryGenre='Technology' are present -- the exact mirror of the toggle-OFF run, so the "
 "two runs together are the evidence for the new copy. Guards after: check-charges 27/0/0, check-registry-fields 0 "
 "drift, check-meta-fields 9 claims/0 stale, check-example-input 25/0 drift. test_input.json untouched, so no "
 "set-example-input needed. Spend: 1 build + 3 tiny capped runs (12 result events total), ~$0.005."
)
e['varied_test']=2932
e['varied_test_note']=note + ' || PREV: ' + e.get('varied_test_note','')
json.dump(d,open(p,'w'),indent=1,sort_keys=True)
print('recorded varied_test=2932 for apple-podcasts-scraper')
