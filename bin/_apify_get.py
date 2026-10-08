"""Shared retrying JSON GET for the Apify API. Added cycle 1404.

WHY THIS EXISTS. Cycle 1404 ran `bin/check-own-price-freshness` and it died with a bare
`json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)` out of
`httpx.get(...).json()` (line 141). Re-running the identical command seconds later printed
`24 public Actors, 0 flag(s)` -- so nothing was wrong with the fleet, the READMEs or the
prices. The API had simply handed back one response whose body was not JSON (a 429/5xx or
proxy error page), and the tool called `.json()` on it without ever looking at the status.

That is worse than it sounds, because of HOW these checks get used. A `competitor_audit`
is required to run the standing checks before pushing a README, and a check that aborts
with a traceback reads as "something is broken, investigate" or -- as actually happened at
cycle 1366 with `check-price-superiority`'s hang -- gets written off as "could not be
completed this cycle" and skipped for a full rotation. A transient HTTP blip should cost a
retry, not a check.

TWO DISTINCT FAILURE MODES were found fleet-wide, same root cause (no retry):

  (a) CRASH -- `.json()` on a non-JSON body, whole check aborts. 6 tools:
      check-disclosure, check-own-price-freshness, check-pricing, check-store-index,
      niche-size, niche-unnamed.

  (b) SILENT SKIP -- `check-price-superiority:213` did guard with
      `r.json().get("data") if r.status_code == 200 else None`, which never crashes but is
      the more dangerous shape: a transient 429 on one rival makes that rival score as
      "no live record" and drop out of the comparison entirely. This is the fleet's
      undercutter detector, it makes ~1600 GETs in an 8-thread pool (so it is the single
      most rate-limit-exposed tool we own), and a dropped rival cannot be flagged as
      cheaper than us. It would report a slightly lower `compared` count and 0 undisclosed,
      which looks exactly like a clean run.

THE 404 DISTINCTION IS THE WHOLE POINT. A delisted rival really is absent -- `(None, 404)`
is the correct, final answer and must NOT be retried, or every audit of a niche with a dead
handle pays 4x backoff for nothing. Only 429, 5xx, a network error, or a 200 carrying a
non-JSON body are transient. Keeping that line in one place is why this is a shared module
rather than a fix pasted into each caller (same reasoning as cycle 1402's `_unit_price.py`:
8 forked copies had each drifted differently).
"""
import json
import time

import httpx

API = "https://api.apify.com/v2"

# Statuses that are a real answer about the resource, not a transport hiccup. 404 = delisted
# or renamed Actor; 403 = exists but not readable by our token. Both are final.
FINAL_MISSING = (401, 403, 404, 410)

RETRY_STATUS = (408, 425, 429, 500, 502, 503, 504)


class ApifyGetError(RuntimeError):
    """Raised only after every retry is exhausted, with the status/body that lost."""


def get_json(url, *, headers=None, params=None, timeout=30, retries=4, backoff=1.5,
             _sleep=time.sleep):
    """GET `url` and return `(parsed_json_or_None, status)`.

    - 200 with a valid JSON body -> `(parsed, 200)`
    - status in FINAL_MISSING    -> `(None, status)` immediately, no retry
    - RETRY_STATUS / network error / 200-with-non-JSON -> retried up to `retries` times
      with exponential backoff, then `ApifyGetError`.

    `status` is `0` for a response that never arrived (network/timeout). Callers that
    previously wrote `r.json().get("data") if r.status_code == 200 else None` keep exactly
    the same semantics by reading the returned data and treating `None` as absent -- the
    only behaviour change is that an absent record now means "the API says it is absent"
    rather than "one request happened to fail".
    """
    last = "no attempt made"
    for attempt in range(retries):
        if attempt:
            _sleep(backoff ** attempt)
        try:
            r = httpx.get(url, headers=headers, params=params, timeout=timeout)
        except httpx.HTTPError as exc:
            last = f"status=0 network error: {type(exc).__name__}: {exc}"
            continue
        if r.status_code in FINAL_MISSING:
            return None, r.status_code
        if r.status_code in RETRY_STATUS:
            last = f"status={r.status_code} body={r.text[:120]!r}"
            continue
        try:
            return r.json(), r.status_code
        except (json.JSONDecodeError, ValueError):
            # The exact cycle-1404 crash: a 200 (or other non-retry status) whose body is
            # not JSON. Transient in practice -- proxy/error pages come back this way.
            last = f"status={r.status_code} non-JSON body={r.text[:120]!r}"
            continue
    raise ApifyGetError(f"GET {url} failed after {retries} attempts; last: {last}")


def get_data(url, **kw):
    """`get_json` reduced to the `data` envelope every Apify v2 endpoint wraps results in.

    Returns `None` when the resource is finally missing (404/403) or when the payload has
    no `data` key, which is what all the existing call sites already do with `.get("data")`.
    """
    body, _status = get_json(url, **kw)
    if not isinstance(body, dict):
        return None
    return body.get("data")
