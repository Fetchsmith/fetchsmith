#!/usr/bin/env python3
"""Self-test for bin/actor-health's INCONCLUSIVE classifier (cycle 3372).

No network, no auth, no token, no Apify run -- free and safe on any cycle.

Why this exists: `inconclusive_blocked` is the only thing standing between a transient
upstream outage and a false `FIX FAILED ACTORS` task against working code, and it has now
been widened three times (c2743 storefront codes, c3362 proxy wrapper, c3369 single-source
`incompleteReason`, c3372 per-source map). Each widening is one `return False` away from
softening a REAL failure into silence, which is the one direction this helper must never
fail in -- and `actor-health` is the nightly critical path, so before c3372 the only way to
exercise an edit was a 24-Actor live sweep. These assertions pin all three shapes, including
the real recorded payloads of the two runs that motivated c3372.

Run: python3 bin/_actor_health_selftest.py
"""
import pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE / "actor-health"

# `actor-health` cannot be imported: line 10 calls /users/me with the live token and the module
# body then RUNS THE WHOLE FLEET through run-sync-get-dataset-items. So exec only the region
# the script marks as side-effect-free. Asserting the sentinels appear exactly once is the
# negative control -- if a later edit moves the classifier out of the region (or drops a
# sentinel), this test must fail loudly rather than silently test nothing.
src = SRC.read_text()
START = "# --- selftest region start"
END = "# --- selftest region end ---"
assert src.count(START) == 1, f"expected exactly 1 {START!r} sentinel in {SRC}"
assert src.count(END) == 1, f"expected exactly 1 {END!r} sentinel in {SRC}"
region = src[src.index(START): src.index(END)]
ns = {"re": re}
exec(compile(region, str(SRC), "exec"), ns)
classify = ns["classify_inconclusive"]
assert callable(classify), "classify_inconclusive not defined inside the selftest region"

FAILS = []
def check(label, rs, expected):
    got = classify(rs)
    if got is not expected:
        FAILS.append(f"{label}: expected {expected}, got {got}")

def src_map(**kw):
    """Per-source map shape (uk-find-a-tender-scraper)."""
    return {"sources": kw, "incompleteReason": "source-failed"}

def failed(err):
    return {"label": "x", "pages": 0, "delivered": 0, "failed": True, "lastError": err}

BAD_GATEWAY = ("HTTP 502: <html> <head><title>502 Bad Gateway</title></head> <body> "
               "<center><h1>502 Bad Gateway</h1></center> </body> </html>")
STARVED = "run-timeout budget exceeded"

# --- the two REAL payloads behind c3372, verbatim from the runs' own RUN_SUMMARY records ---
# nightly run SLKLVhupjpTVa4EIK (2026-11-18T06:30:36Z), 0 rows -> must soften.
check("real c3372 nightly (fts 502 + cf starved)", {
    "mode": "search",
    "sources": {
        "fts": {"label": "Find a Tender", "pages": 0, "scanned": 0, "delivered": 0,
                "exhausted": False, "failed": True, "sliceExceeded": False,
                "lastError": BAD_GATEWAY},
        "cf": {"label": "Contracts Finder", "pages": 0, "scanned": 0, "delivered": 0,
               "exhausted": False, "failed": True, "sliceExceeded": False,
               "lastError": STARVED},
    },
    "sourcesRequested": ["fts", "cf"], "sourcesFailed": ["fts", "cf"],
    "scanned": 0, "delivered": 0, "complete": False,
    "incompleteReason": "source-failed",
}, True)
# run Bf7QtfJ1QZc19iFJ9 (2026-11-18T07:00:45Z), same input, 10 rows, both portals fine. This
# shape never reaches the classifier in production (`ok` is already True), but it is the
# control that proves a healthy map is not blanket-softened.
check("real c3372 recovery (both portals ok)", {
    "mode": "search",
    "sources": {
        "fts": {"label": "Find a Tender", "pages": 1, "scanned": 16, "delivered": 5,
                "exhausted": True, "failed": False, "sliceExceeded": False, "lastError": None},
        "cf": {"label": "Contracts Finder", "pages": 1, "scanned": 15, "delivered": 5,
               "exhausted": True, "failed": False, "sliceExceeded": False, "lastError": None},
    },
    "sourcesRequested": ["fts", "cf"], "sourcesFailed": [],
    "delivered": 10, "complete": False, "incompleteReason": "max-results",
}, False)

# --- per-source map: the gate's three conditions, one negative control each ---
check("map: every source 502", src_map(fts=failed(BAD_GATEWAY), cf=failed("HTTP 503: busy")), True)
check("map: 504 + starved sibling", src_map(fts=failed("HTTP 504: gateway timeout"), cf=failed(STARVED)), True)
check("map: single source 502", src_map(fts=failed(BAD_GATEWAY)), True)
# (a) one source worked -> a 0-row run is a real signal (empty window or a filter/parse bug).
check("map: one source ok, other 502", src_map(
    fts=failed(BAD_GATEWAY),
    cf={"label": "cf", "delivered": 0, "failed": False, "lastError": None}), False)
# The case that makes the `failed` guard load-bearing rather than decorative, found by
# mutation-testing this file at c3372 (deleting the guard left every other assertion green).
# `fetchPage` NEVER clears `source.lastError` (main.js:887 sets it per failed attempt; nothing
# resets it), and `failed` is set only when all 4 retries are exhausted (main.js:1032) -- so a
# portal that 502'd once and succeeded on retry reports `failed: false` with a stale, entirely
# transient-looking `HTTP 502` string. Softening on the error text alone would silently hide a
# real 0-row regression on a WORKING capture path. Only `failed` may be trusted here.
check("map: source recovered on retry, stale 502 in lastError", src_map(
    fts=failed(BAD_GATEWAY),
    cf={"label": "cf", "pages": 2, "delivered": 0, "failed": False,
        "lastError": BAD_GATEWAY}), False)
# (b) no transient code anywhere -> a genuine slowdown, must stay FAILED.
check("map: starved only, no upstream code", src_map(fts=failed(STARVED), cf=failed(STARVED)), False)
check("map: sibling-slice stop is not softened", src_map(
    fts=failed(BAD_GATEWAY),
    cf=failed("stopped early to leave run time for the other portal")), False)
# (c) unrecognized causes -> never softened.
check("map: 404 not transient", src_map(fts=failed("HTTP 404: not found"), cf=failed(STARVED)), False)
check("map: 401 not transient", src_map(fts=failed("HTTP 401: unauthorized"), cf=failed(STARVED)), False)
check("map: parse error not transient", src_map(
    fts=failed("Unexpected token < in JSON at position 0"), cf=failed(STARVED)), False)
check("map: empty lastError", src_map(fts=failed(""), cf=failed("")), False)
check("map: non-dict member", {"sources": {"fts": "502"}}, False)
check("map: empty map falls through", {"sources": {}, "incompleteReason": "source-failed"}, False)

# --- c3376: the two-portal clock race (`incompleteReason: "source-time-share"`) ---
# REAL payload, verbatim from nightly run VYGUmIoWSzqZS0BDe (2026-11-18T08:30:37Z, SUCCEEDED,
# 0 rows) -- the run that opened c3375's FIX FAILED ACTORS task against working code. Note
# there is NO upstream error anywhere in it: that is what c3372's branch required and why this
# fell through to FAILED.
YIELDED = "stopped early to leave run time for the other portal"
REAL_C3376 = {
    "sources": {
        "fts": {"label": "Find a Tender", "pages": 0, "scanned": 0, "delivered": 0,
                "exhausted": False, "failed": True, "sliceExceeded": True, "lastError": YIELDED},
        "cf": {"label": "Contracts Finder", "pages": 0, "scanned": 0, "delivered": 0,
               "exhausted": False, "failed": True, "sliceExceeded": False, "lastError": STARVED},
    },
    "sourcesRequested": ["fts", "cf"], "sourcesFailed": ["fts", "cf"],
    "scanned": 0, "delivered": 0, "pages": 0, "complete": False,
    "incompleteReason": "source-time-share",
    "incompleteDetail": ("Find a Tender was slow or unreachable and was stopped after 0 page(s) "
                         "so the other portal could still be searched (stopped early to leave run "
                         "time for the other portal); its notices are missing from this run"),
}
def time_share(**over):
    """REAL_C3376 with one field overridden -- each call below is one gate condition."""
    rs = {**REAL_C3376, "sources": {k: dict(v) for k, v in REAL_C3376["sources"].items()}}
    for dotted, val in over.items():
        if "__" in dotted:
            src, field = dotted.split("__", 1)
            rs["sources"][src][field] = val
        else:
            rs[dotted] = val
    return rs
check("real c3376 nightly (fts yielded + cf starved)", REAL_C3376, True)
# (a) the reason string is the gate: a run that truly ran out of clock says `time-budget`
# (main.js:1050) and must stay FAILED -- it is the slowdown c3372 refused to soften.
check("time-share: time-budget reason not softened", time_share(incompleteReason="time-budget"), False)
check("time-share: source-failed reason not softened", time_share(incompleteReason="source-failed"), False)
check("time-share: reason absent", time_share(incompleteReason=None), False)
# (b) one source worked -> 0 rows is a real signal, exactly as in the c3372 branch.
check("time-share: one portal ok", time_share(cf__failed=False), False)
# (c) ANY page actually fetched -> the capture/parse path ran and still delivered 0 rows, so a
# filter/parse regression is on the table no matter what stopped the siblings.
check("time-share: a portal did fetch a page", time_share(fts__pages=2), False)
check("time-share: a portal did scan rows", time_share(cf__scanned=15), False)
# (d) the yield must be proven by the STRUCTURED flag, not the message text (`lastError` is
# never cleared, so text alone is not evidence of THIS run's outcome -- the c3372 lesson).
check("time-share: yield message without the flag", time_share(fts__sliceExceeded=False), False)
# (e) no yield at all -> a pure double starve is not this shape.
check("time-share: both starved, nobody yielded",
      time_share(fts__sliceExceeded=False, fts__lastError=STARVED), False)
# (f) unrecognized causes are never softened, even alongside a real yield.
check("time-share: parse error alongside the yield",
      time_share(cf__lastError="Unexpected token < in JSON at position 0"), False)
check("time-share: empty lastError alongside the yield", time_share(cf__lastError=""), False)
# (g) a real upstream error alongside the yield is NOT softened by EITHER branch, and that is
# deliberate: this branch rejects the 502 as an unrecognized cause, and c3372's rejects the
# yield message for the reason its own control above pins ("map: sibling-slice stop is not
# softened" -- the sibling DID get its slice, so the clock is not the whole story). A portal
# that genuinely errored stays FAILED. Pinned so neither branch quietly starts covering it.
check("time-share: 502 alongside the yield stays FAILED in both branches",
      time_share(cf__lastError=BAD_GATEWAY), False)

# --- the two pre-existing shapes must still behave exactly as c2743/c3362/c3369 left them ---
check("list: all reasons transient storefront", {"sources": [
    {"complete": False, "reason": "store refused (403)"},
    {"complete": False, "reason": "store refused (429)"}]}, True)
check("list: proxy wrapper 504", {"sources": [
    {"complete": False, "reason": "Proxy responded with 590 UPSTREAM504: 0 bytes"}]}, True)
check("list: proxy wrapper 503 NOT softened", {"sources": [
    {"complete": False, "reason": "Proxy responded with 590 UPSTREAM503: 0 bytes"}]}, False)
check("list: one source complete", {"sources": [
    {"complete": True, "reason": None},
    {"complete": False, "reason": "store refused (403)"}]}, False)
check("list: unrecognized reason", {"sources": [
    {"complete": False, "reason": "selector not found"}]}, False)
check("single-source: search-request-failed + 503", {
    "incompleteReason": "search-request-failed",
    "incompleteDetail": "grants.gov stopped answering (HTTP 503: unavailable)"}, True)
check("single-source: search-request-failed + 400", {
    "incompleteReason": "search-request-failed",
    "incompleteDetail": "bad request (HTTP 400)"}, False)
check("single-source: a cap is never softened", {
    "incompleteReason": "charge-limit",
    "incompleteDetail": "charge limit reached (HTTP 502 appeared in an earlier retry)"}, False)
check("single-source: max-results cap", {
    "incompleteReason": "max-results", "incompleteDetail": "maxResults=10 was reached"}, False)

# --- shapes that must never crash the nightly run ---
check("complete run, nothing to explain", {"complete": True, "incompleteReason": None}, False)
check("empty record", {}, False)
check("sources is None", {"sources": None}, False)
check("record is not a dict", [], False)
check("record is None", None, False)

if FAILS:
    print("FAIL (%d):" % len(FAILS))
    for f in FAILS:
        print("  " + f)
    sys.exit(1)
print("ALL PASS -- actor-health INCONCLUSIVE classifier: 4 RUN_SUMMARY shapes, "
      "3 real recorded payloads, 23 negative controls.")
