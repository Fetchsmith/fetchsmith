#!/usr/bin/env python3
"""cycle 3052 -- follow-up to bin/_rec3052.py: is the union's measured gain made of REAL
new articles, or of the same article re-keyed under a second /articles/<id>?

_rec3052.py dedupes exactly the way the Actor would (by /articles/<id>, main.js:414-456).
If Google issues a different id for the same story depending on which `after:` sentinel
fetched it, the whole union gain is duplicate rows in the buyer's dataset -- worse than
the status quo, not better. So re-dedupe the same union by NORMALISED TITLE and compare.

Note on what counts as a duplicate: Google News RSS titles are "Headline - Publisher".
Two publishers covering one event are genuinely two articles (and the Actor has always
returned both), so the duplicate test is identical headline AND identical publisher.
"""
import re, sys, time, json, unicodedata
from datetime import datetime, timezone
from _rec3052 import SHAPES, fetch, years_before, DAY

TAG = re.compile(r'<[^>]+>')


def norm_title(t):
    t = unicodedata.normalize('NFKD', t)
    t = TAG.sub('', t).replace('&amp;', '&').replace('&#39;', "'").replace('&quot;', '"')
    t = re.sub(r'[^a-z0-9 ]+', ' ', t.lower())
    return re.sub(r'\s+', ' ', t).strip()


def rich_items(xml):
    """-> list of (article_id, normalised 'headline|publisher', published_ms)."""
    out = []
    for block in re.findall(r'<item>(.*?)</item>', xml, re.S):
        link = re.search(r'<link>(.*?)</link>', block, re.S)
        title = re.search(r'<title>(.*?)</title>', block, re.S)
        src = re.search(r'<source[^>]*>(.*?)</source>', block, re.S)
        pub = re.search(r'<pubDate>(.*?)</pubDate>', block, re.S)
        if not (link and title and pub):
            continue
        from email.utils import parsedate_to_datetime
        try:
            ms = int(parsedate_to_datetime(pub.group(1).strip()).timestamp() * 1000)
        except Exception:
            continue
        seg = link.group(1).split('/articles/')
        aid = seg[1].split('?')[0] if len(seg) > 1 else link.group(1).strip()
        key = norm_title(title.group(1)) + '|' + norm_title(src.group(1) if src else '')
        out.append((aid, key, ms))
    return out


def main():
    print(f'cycle 3052 union DUPLICATE-CHECK  {datetime.now(timezone.utc).isoformat()}')
    print('question: of the items the union adds over the best single request, how many are '
          'genuinely new articles (novel headline+publisher) vs the same story re-keyed?\n')
    rows = []
    for term, cutoff in SHAPES:
        drop_before = int(datetime.fromisoformat(cutoff).replace(tzinfo=timezone.utc)
                          .timestamp() * 1000) + DAY
        sets = {}
        for label, sent in (('narrow', years_before(cutoff, 2)), ('wide', years_before(cutoff, 20))):
            its = rich_items(fetch(f'{term} after:{sent} before:{cutoff}'))
            sets[label] = [i for i in its if i[2] <= drop_before]
            time.sleep(1.5)

        by_id, by_title = {}, {}
        for label in ('narrow', 'wide'):
            for aid, key, _ in sets[label]:
                by_id.setdefault(aid, key)
                by_title.setdefault(key, aid)
        # id-keyed entries that collide onto a title another id already owns = re-keyed dupes
        seen_titles, rekeyed = set(), 0
        for aid, key in by_id.items():
            if key in seen_titles:
                rekeyed += 1
            seen_titles.add(key)

        best = max(len({i[0] for i in sets['narrow']}), len({i[0] for i in sets['wide']}))
        union_id, union_title = len(by_id), len(by_title)
        rows.append({'term': term, 'best_single': best, 'union_by_id': union_id,
                     'union_by_title': union_title, 'rekeyed_dupes': rekeyed,
                     'gain_by_id': union_id - best, 'gain_by_title': union_title - best})
        print(f'  {term:<18} best_single={best:>3}  union_by_id={union_id:>3}  '
              f'union_by_title={union_title:>3}  re-keyed_dupes={rekeyed:>2}  '
              f'TRUE_gain={union_title - best:+d}  (id-gain was {union_id - best:+d})')

    print('\n' + '=' * 86)
    tot_id = sum(r['gain_by_id'] for r in rows)
    tot_title = sum(r['gain_by_title'] for r in rows)
    tot_rekey = sum(r['rekeyed_dupes'] for r in rows)
    print(f'total id-dedup gain {tot_id:+d}   total title-dedup (TRUE) gain {tot_title:+d}   '
          f're-keyed duplicates {tot_rekey}')
    print(f'union_by_title >= best_single on every shape: '
          f'{all(r["gain_by_title"] >= 0 for r in rows)}  '
          f'(strictly better on {sum(1 for r in rows if r["gain_by_title"] > 0)}/{len(rows)})')
    print('=' * 86)
    json.dump(rows, open('/tmp/rec3052b.json', 'w'), indent=1)
    print('raw rows -> /tmp/rec3052b.json')


if __name__ == '__main__':
    sys.exit(main())
