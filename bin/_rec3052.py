#!/usr/bin/env python3
"""cycle 3052 -- measure `NEW c3047` step (a): does a UNION of two differently-biased
sentinel'd `after:` requests actually beat the best single request on the
`publishedBefore`-only branch of google-news-scraper, after de-dup by article id?

Measurement only -- free public Google News RSS GETs, no Apify run, no code shipped.
Mirrors the Actor's own semantics:
  - feed URL shape: main.js:463  (q + timeSuffix, hl/gl/ceid)
  - in-window test: main.js:197 dropBeforeMs = cutoff + 86_400_000 (one full day of
    tolerance, because Google evaluates before: in US/Pacific while publishedAt is UTC)
  - dedup id:      main.js:414-456 decode path keys off the /articles/<id> segment;
                   RSS <guid> carries the same id, so we key on both and compare.
"""
import re, sys, time, json, urllib.parse, urllib.request
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

UA = 'Mozilla/5.0 (compatible; FetchSmithMeasure/1.0)'
DAY = 86_400_000

# 5 query shapes. `trump` is deliberately EXCLUDED: c3047 measured it as saturated at the
# ~100 ceiling regardless of sentinel, so it cannot discriminate (reusable test-design note
# from LEARNINGS ## cycle 3047). Four shapes are carried over from c3047 so the numbers are
# directly comparable; `electric vehicles` is fresh, to avoid overfitting to the c3047 set.
SHAPES = [
    ('climate',           '2015-01-01'),
    ('bitcoin',           '2016-01-01'),
    ('python',            '2020-01-01'),
    ('web scraping',      '2020-01-01'),
    ('electric vehicles', '2019-01-01'),
]


def years_before(date_str, n):
    y, m, d = date_str.split('-')
    return f'{int(y) - n:04d}-{m}-{d}'


def fetch(q):
    url = ('https://news.google.com/rss/search?q=' + urllib.parse.quote(q)
           + '&hl=en-US&gl=US&ceid=US:en')
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read().decode('utf-8', 'replace')


def items(xml):
    """-> list of (article_id, guid, published_ms). Mirrors the Actor's id derivation."""
    out = []
    for block in re.findall(r'<item>(.*?)</item>', xml, re.S):
        link = re.search(r'<link>(.*?)</link>', block, re.S)
        guid = re.search(r'<guid[^>]*>(.*?)</guid>', block, re.S)
        pub = re.search(r'<pubDate>(.*?)</pubDate>', block, re.S)
        if not pub:
            continue
        try:
            ms = int(parsedate_to_datetime(pub.group(1).strip()).timestamp() * 1000)
        except Exception:
            continue
        aid = None
        if link:
            seg = link.group(1).split('/articles/')
            if len(seg) > 1:
                aid = seg[1].split('?')[0]
        g = guid.group(1).strip() if guid else None
        out.append((aid or g, g, ms))
    return out


def probe(q, drop_before_ms, label, results):
    xml = fetch(q)
    its = items(xml)
    ids = {i[0] for i in its if i[0]}
    inw = {i[0] for i in its if i[0] and i[2] <= drop_before_ms}
    results[label] = {'query': q, 'raw': len(its), 'ids': ids, 'in_window': inw,
                      'no_id': sum(1 for i in its if not i[0])}
    print(f'    {label:<10} raw={len(its):>3} ids={len(ids):>3} in_window={len(inw):>3}  {q}')
    time.sleep(1.5)
    return results[label]


def main():
    print(f'cycle 3052 union-of-sentinels sweep  {datetime.now(timezone.utc).isoformat()}')
    print('narrow sentinel = cutoff-2y, wide sentinel = cutoff-20y (the two extremes '
          'c3047 measured as per-query opposite winners)\n')
    rows = []
    for term, cutoff in SHAPES:
        drop_before = int(datetime.fromisoformat(cutoff).replace(tzinfo=timezone.utc)
                          .timestamp() * 1000) + DAY
        print(f'  {term!r} before:{cutoff}  (drop_before = cutoff + 1d)')
        r = {}
        bare = probe(f'{term} before:{cutoff}', drop_before, 'bare', r)
        narrow = probe(f'{term} after:{years_before(cutoff, 2)} before:{cutoff}',
                       drop_before, 'narrow', r)
        wide = probe(f'{term} after:{years_before(cutoff, 20)} before:{cutoff}',
                     drop_before, 'wide', r)

        union_in = narrow['in_window'] | wide['in_window']
        overlap = narrow['in_window'] & wide['in_window']
        best_single = max(len(narrow['in_window']), len(wide['in_window']))
        union_all = narrow['ids'] | wide['ids']
        rows.append({
            'term': term, 'cutoff': cutoff,
            'bare_raw': bare['raw'], 'bare_in': len(bare['in_window']),
            'narrow_in': len(narrow['in_window']), 'wide_in': len(wide['in_window']),
            'overlap_in': len(overlap), 'union_in': len(union_in),
            'best_single_in': best_single,
            'gain_vs_best_single': len(union_in) - best_single,
            'gain_vs_bare': len(union_in) - len(bare['in_window']),
            'union_all_ids': len(union_all),
            'no_id_items': bare['no_id'] + narrow['no_id'] + wide['no_id'],
            'jaccard_in': round(len(overlap) / len(union_in), 3) if union_in else None,
        })
        print(f'    -> union_in={len(union_in)} overlap={len(overlap)} '
              f'best_single={best_single} GAIN={len(union_in) - best_single} '
              f'(vs bare {len(bare["in_window"])}: {len(union_in) - len(bare["in_window"]):+d})\n')

    print('=' * 100)
    hdr = ('term', 'bare_in', 'narrow_in', 'wide_in', 'ovl', 'union_in', 'gain_vs_best', 'gain_vs_bare', 'jacc')
    print('{:<18}{:>9}{:>11}{:>9}{:>6}{:>10}{:>14}{:>14}{:>8}'.format(*hdr))
    for r in rows:
        print('{:<18}{:>9}{:>11}{:>9}{:>6}{:>10}{:>14}{:>14}{:>8}'.format(
            r['term'], r['bare_in'], r['narrow_in'], r['wide_in'], r['overlap_in'],
            r['union_in'], f"{r['gain_vs_best_single']:+d}", f"{r['gain_vs_bare']:+d}",
            r['jaccard_in'] if r['jaccard_in'] is not None else '-'))
    print('=' * 100)
    monotone = all(r['gain_vs_best_single'] >= 0 for r in rows)
    strict = [r['term'] for r in rows if r['gain_vs_best_single'] > 0]
    print(f'union >= best single on every shape: {monotone}  '
          f'(strictly better on {len(strict)}/{len(rows)}: {strict})')
    print(f'items with NO derivable id (would break dedup): '
          f'{sum(r["no_id_items"] for r in rows)}')
    json.dump(rows, open('/tmp/rec3052.json', 'w'), indent=1)
    print('raw rows -> /tmp/rec3052.json')


if __name__ == '__main__':
    sys.exit(main())
