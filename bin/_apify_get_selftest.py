#!/root/agent/venv/bin/python
"""Selftest for bin/_apify_get.py. No network: httpx.get is monkeypatched. Added cycle 1404.

Each case asserts the behaviour the fleet actually depends on, including the two real bugs
that motivated the module: the cycle-1404 JSONDecodeError crash, and the never-retried 429
that silently drops a rival out of check-price-superiority's comparison.
"""
import sys

sys.path.insert(0, "/root/agent/bin")
import httpx

import _apify_get as ag


class FakeResp:
    def __init__(self, status, body):
        self.status_code = status
        self.text = body

    def json(self):
        import json
        return json.loads(self.text)


def run(script, **kw):
    """Replay `script` (a list of FakeResp or httpx.HTTPError) as successive GETs."""
    calls = []
    seq = list(script)

    def fake_get(url, headers=None, params=None, timeout=None):
        calls.append(url)
        nxt = seq.pop(0)
        if isinstance(nxt, Exception):
            raise nxt
        return nxt

    orig = httpx.get
    httpx.get = fake_get
    try:
        return ag.get_json("https://api.apify.com/v2/acts/x~y",
                           _sleep=lambda s: None, **kw), calls
    finally:
        httpx.get = orig


fails = 0


def check(label, got, want):
    global fails
    ok = got == want
    if not ok:
        fails += 1
    print(f"{'ok  ' if ok else 'FAIL'} {label}: got {got!r} want {want!r}")


# 1. Happy path: one call, parsed body.
(res, st), calls = run([FakeResp(200, '{"data": {"id": "a"}}')])
check("200 json -> parsed", (res, st, len(calls)), ({"data": {"id": "a"}}, 200, 1))

# 2. THE CYCLE-1404 CRASH: 200 with a non-JSON body. Used to raise JSONDecodeError out of
#    check-own-price-freshness and abort the whole fleet check. Must retry and succeed.
(res, st), calls = run([FakeResp(200, "<html>502 Bad Gateway</html>"),
                        FakeResp(200, '{"data": {"id": "a"}}')])
check("200 non-JSON then 200 json -> retried", (res, st, len(calls)),
      ({"data": {"id": "a"}}, 200, 2))

# 3. THE SILENT-SKIP BUG: a 429 used to be read as "rival has no live record" and the rival
#    vanished from check-price-superiority's comparison. Must retry, not drop.
(res, st), calls = run([FakeResp(429, "rate limited"),
                        FakeResp(200, '{"data": {"id": "a"}}')])
check("429 then 200 -> retried, not dropped", (res, st, len(calls)),
      ({"data": {"id": "a"}}, 200, 2))

# 4. 404 is a REAL answer (delisted rival): return immediately, never retry. If this
#    regressed, every audit of a niche with one dead handle would pay full backoff.
(res, st), calls = run([FakeResp(404, '{"error": "not found"}')])
check("404 -> final, one call only", (res, st, len(calls)), (None, 404, 1))

# 5. 403 (exists, our token cannot read it) is likewise final.
(res, st), calls = run([FakeResp(403, "forbidden")])
check("403 -> final, one call only", (res, st, len(calls)), (None, 403, 1))

# 6. Network error retries, then succeeds.
(res, st), calls = run([httpx.ConnectTimeout("boom"),
                        FakeResp(200, '{"data": 1}')])
check("network error then 200 -> retried", (res, st, len(calls)), ({"data": 1}, 200, 2))

# 7. Exhaustion raises a loud, attributable error -- not a silent None, and not a bare
#    JSONDecodeError with no URL in it.
try:
    run([FakeResp(503, "down")] * 4, retries=4)
    check("exhausted -> raises", "no raise", "ApifyGetError")
except ag.ApifyGetError as exc:
    msg = str(exc)
    check("exhausted -> raises ApifyGetError naming url+status",
          ("acts/x~y" in msg, "503" in msg, "4 attempts" in msg), (True, True, True))

# 8. get_data unwraps the envelope, and returns None on a final 404.
calls_made = []


def fake_get2(url, headers=None, params=None, timeout=None):
    calls_made.append(url)
    return FakeResp(200, '{"data": {"isPublic": true}}')


orig = httpx.get
httpx.get = fake_get2
try:
    check("get_data unwraps data", ag.get_data("https://api.apify.com/v2/acts/x~y"),
          {"isPublic": True})
finally:
    httpx.get = orig


def fake_get3(url, headers=None, params=None, timeout=None):
    return FakeResp(404, '{"error": "nope"}')


httpx.get = fake_get3
try:
    check("get_data on 404 -> None", ag.get_data("https://api.apify.com/v2/acts/x~y"), None)
finally:
    httpx.get = orig

print(f"\n_apify_get selftest: {'PASS' if not fails else str(fails) + ' FAILURE(S)'}")
sys.exit(1 if fails else 0)
