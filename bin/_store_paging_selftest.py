#!/root/agent/venv/bin/python
"""_store_paging_selftest — prove the three `/v2/store` REST callers (bin/store-anon-rank,
bin/check-store-rank, bin/store-visibility) survive the 2026-11-15 change to that endpoint
WITHOUT waiting for the date.

Why this exists (cycle 2496): Apify's own notice (queue item c2478, owner-forwarded
inbox `01852eaa`) says that from 2026-11-15 `GET /v2/store?search=` serves ONE page of
up to 100 Actors, `offset` and `total` stop working, and `sortBy` is ignored. Both rank
tools paged on `offset` and indexed `data["total"]` directly, so post-change they would
have (a) KeyError'd or lost `total` and (b) re-scanned page 1 until the scan budget ran
out and then printed a confident "NOT FOUND"/"ABSENT" for every Actor ranked deeper than
~96 -- which per the cycle-2072 baseline (#29-#354) is most of the fleet. A false
fleet-wide ranking collapse is exactly the kind of finding that invites pointless
listing-copy edits, so the tools now report UNKNOWN instead.

That fix cannot be verified against the live API before the deadline (paging still works:
measured c2496, offsets 0/90/180 each returned a different first item), hence this
simulation. Both tools detect dead paging structurally -- they remember each page's first
(username, name) and stop the moment one repeats -- which is why a fake client that
ignores `offset` is a faithful stand-in.

Run it: bin/_store_paging_selftest.py  (exit 0 = pass, no network, no auth, free)
Re-run it AFTER 2026-11-15 alongside a real `bin/store-anon-rank` run: this asserts the
degraded branch works, the live run tells you whether the degraded branch is now the one
being taken.
"""
import importlib.machinery
import importlib.util
import os
import sys

BIN = os.path.dirname(os.path.abspath(__file__))


def load(name, filename):
    path = os.path.join(BIN, filename)
    ld = importlib.machinery.SourceFileLoader(name, path)
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(name, ld))
    ld.exec_module(mod)
    return mod


def page_of_rivals(n=96):
    return [{"username": "rival%d" % i, "name": "a%d" % i, "stats": {"totalUsers": 3}}
            for i in range(n)]


def check_store_anon_rank():
    """store-anon-rank.rank() -> (pos, scanned, total, top, users, paging_ok)"""
    m = load("sar", "store-anon-rank")
    page = page_of_rivals()
    calls = {"n": 0}

    def fake_fetch(query, offset, limit=100):       # post-change: offset ignored, no total
        calls["n"] += 1
        return {"items": page}

    m.fetch = fake_fetch

    pos, scanned, total, _top, _users, ok = m.rank("court records", "court-records-scraper", 400)
    assert pos is None, "expected no position when we are not on page 1, got %r" % (pos,)
    assert ok is False, "dead paging not detected"
    assert total is None, "a missing `total` must stay None, not crash or be fabricated"
    assert calls["n"] == 2, "must stop on the first repeated page, got %d fetches" % calls["n"]
    assert scanned == 96, "scanned should count page 1 only, got %d" % scanned

    # Control: still report a REAL rank when we do sit on page 1, paging or no paging.
    page[40] = {"username": m.USERNAME, "name": "court-records-scraper",
                "stats": {"totalUsers": 1}}
    calls["n"] = 0
    pos, _scanned, _total, _top, users, ok = m.rank("court records", "court-records-scraper", 400)
    assert (pos, ok, users, calls["n"]) == (41, True, 1, 1), \
        "on-page-1 control broke: %r" % ((pos, ok, users, calls["n"]),)
    return "store-anon-rank: UNKNOWN on dead paging, real rank when on page 1"


def check_check_store_rank():
    """check-store-rank.rank_for() -> (rank, total, scanned, paging_ok)"""
    m = load("csr", "check-store-rank")
    page = page_of_rivals()

    class Resp:
        def raise_for_status(self):
            pass

        def json(self):
            return {"data": {"items": page}}        # post-change: offset ignored, no total

    class Client:
        def __init__(self):
            self.n = 0

        def get(self, *_a, **_kw):
            self.n += 1
            return Resp()

    c = Client()
    rank, total, scanned, ok = m.rank_for(c, "court records", "court-records-scraper", 400)
    assert rank is None and ok is False, "dead paging not detected: %r" % ((rank, ok),)
    assert total is None, "a missing `total` must stay None"
    assert c.n == 2, "must stop on the first repeated page, got %d requests" % c.n
    assert scanned == 96, "scanned should count page 1 only, got %d" % scanned

    page[10] = {"username": "fetchsmith", "name": "court-records-scraper"}
    c = Client()
    rank, _total, _scanned, ok = m.rank_for(c, "court records", "court-records-scraper", 400)
    assert (rank, ok, c.n) == (10, True, 1), \
        "on-page-1 control broke: %r" % ((rank, ok, c.n),)
    return "check-store-rank: UNKNOWN on dead paging, real rank when on page 1"


def check_store_visibility():
    """store-visibility.search() -> (total, n_items, ours). Single-page, so paging is
    not its problem -- but it indexed `data["total"]`, which after 2026-11-15 is a hard
    KeyError, and its 'filtered' heuristic compares two totals that both become None."""
    m = load("sv", "store-visibility")
    payload = {"data": {"items": page_of_rivals(85)}}      # post-change: no `total`

    class Fh:
        def __enter__(self):
            return self

        def __exit__(self, *_a):
            return False

        def read(self):
            import json as _j
            return _j.dumps(payload).encode()

    m.urllib.request.urlopen = lambda *_a, **_kw: Fh()
    total, n_items, ours = m.search("fda recall")
    assert total is None, "missing `total` must read None, not raise: %r" % (total,)
    assert (n_items, ours) == (85, []), "item parsing broke: %r" % ((n_items, ours),)

    payload["data"]["items"][3] = {"username": "fetchsmith", "name": "fda-recall-scraper"}
    total, n_items, ours = m.search("fda recall")
    assert ours == ["fda-recall-scraper"], "own-listing detection broke: %r" % (ours,)
    assert ("%6s" % ("n/a" if total is None else total)) == "   n/a", "None must not hit %d"
    return "store-visibility: `total` absence reads n/a, no KeyError, items still parsed"


def main():
    os.environ.setdefault("APIFY_TOKEN", "selftest-no-network")
    failures = []
    for fn in (check_store_anon_rank, check_check_store_rank, check_store_visibility):
        try:
            print("PASS  %s" % fn())
        except AssertionError as exc:
            failures.append("%s: %s" % (fn.__name__, exc))
            print("FAIL  %s: %s" % (fn.__name__, exc))
    print()
    if failures:
        print("%d FAILURE(S) -- the 2026-11-15 /v2/store hardening has regressed." % len(failures))
        return 1
    print("3/3 pass -- the rank tools degrade to UNKNOWN (never a false ABSENT) once")
    print("/v2/store stops honouring `offset`, and store-visibility survives `total` going")
    print("away. See queue item c2478 for the full change.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
