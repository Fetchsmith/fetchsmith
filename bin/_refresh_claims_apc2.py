#!/usr/bin/env python3
"""Refresh apple-podcasts-scraper/README.md's stale competitor user-count claims
(cycle 1791). Same treatment rule as bin/_refresh_claims_{gn,rjs,ats,sub}.py: only the
volatile HEADCOUNT is touched, every price/feature/date claim in the same sentence is
left exactly as written. 6 claims flagged by bin/check-competitor-claims. Live values
fetched 2026-10-16:

  >=20 -> refresh to live value, dated:
    sourabhbgp/apple-podcast-scraper          51 -> 58
    logiover/apple-podcasts-episode-scraper   54 -> 62
    seemuapps/spotify-podcast-scraper         41 -> 50

  sub-20 -> DROP the count per the standing 2026-10-07 rule:
    scrapewise/media-transcriber                4 ->  6
    spokentext/spotify-podcast-transcript       3 ->  6
    seemuapps/podcast-transcript-scraper        2 ->  3
"""
import sys

PAIRS = [
    ("is `sourabhbgp` (51 users, `sourabhbgp/apple-podcast-scraper`) at $0.003/result",
     "is `sourabhbgp` (58 users, re-verified live 2026-10-16, "
     "`sourabhbgp/apple-podcast-scraper`) at $0.003/result"),

    ("The fastest-growing rival in the niche is `logiover` (54 users, 16 of them in the "
     "last 30 days, `logiover/apple-podcasts-episode-scraper`), and it is episodes-only",
     "The fastest-growing rival in the niche is `logiover` (62 users, 16 of them in the "
     "last 30 days, re-verified live 2026-10-16, "
     "`logiover/apple-podcasts-episode-scraper`), and it is episodes-only"),

    ("`seemuapps/spotify-podcast-scraper` (41 users) covers Spotify, a different "
     "platform this Actor does not touch",
     "`seemuapps/spotify-podcast-scraper` (50 users, re-verified live 2026-10-16) "
     "covers Spotify, a different platform this Actor does not touch"),

    ("Ruled out of scope as non-competitors: `northglasslabs/podcast-transcript-scraper` "
     "and `scrapewise/media-transcriber` (4u) are speech-to-text/transcription products "
     "billing per audio-minute",
     "Ruled out of scope as non-competitors: `northglasslabs/podcast-transcript-scraper` "
     "and `scrapewise/media-transcriber` are speech-to-text/transcription products "
     "billing per audio-minute"),

    ("Ruled out of scope on billing unit, not price: `spokentext/spotify-podcast-"
     "transcript` (3u), `fguiraud/podcast-transcript-scraper` (1u) and "
     "`seemuapps/podcast-transcript-scraper` (2u) bill per transcribed audio-minute",
     "Ruled out of scope on billing unit, not price: `spokentext/spotify-podcast-"
     "transcript`, `fguiraud/podcast-transcript-scraper` (1u) and "
     "`seemuapps/podcast-transcript-scraper` bill per transcribed audio-minute"),
]

path = "/root/agent/actors/apple-podcasts-scraper/README.md"
text = open(path, encoding="utf-8").read()
orig = text
fails = []
for old, new in PAIRS:
    n = text.count(old)
    if n != 1:
        fails.append(f"{n} matches for: {old[:90]}")
        continue
    text = text.replace(old, new)
if fails:
    print("ABORT -- non-unique/missing anchors:")
    for f in fails:
        print("  " + f)
    sys.exit(1)

open(path, "w", encoding="utf-8").write(text)
print(f"applied {len(PAIRS)} replacements; {len(orig)} -> {len(text)} bytes")
