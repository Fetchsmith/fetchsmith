#!/usr/bin/env python3
"""Self-test for bin/channel-mix's short-window QUOTABLE gate (cycle 2688).

No network, no auth, no log reading, free -- it monkeypatches `lines()` with a synthetic
log, so it is safe to run on any cycle and does not depend on what Caddy happens to hold.

Why this exists: cycle 2684 ran `channel-mix` 0.20 days after a log rotation and the script
printed a confident `AI:SEARCH = 52.00:1` and `1147.4/day`. The real 7-day figure was
6.67:1. Nothing in the output objected, because the window length was on line 1 and the
conclusion was 8 lines below it. c2688 added a 7-day default plus a hard gate; these
assertions are what stop a later edit from quietly removing either one.

Run: python3 bin/_channel_mix_selftest.py
"""
import importlib.util, io, json, pathlib, sys, time, contextlib
from importlib.machinery import SourceFileLoader

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE / "channel-mix"

# MUST come before the load, and is not optional hygiene -- it is a correctness fix found
# while running this test's own negative control (c2688). SourceFileLoader caches bytecode
# to __pycache__/channel-mixcpython-312.pyc and validates it against the source's mtime at
# 1-SECOND granularity plus its size. Editing `QUOTABLE_DAYS = 2.0` -> `0.0` changes neither
# the size nor (within the same second) the mtime, so the test happily re-ran the STALE
# bytecode and printed ALL PASS for a file whose gate had just been deleted. A self-test
# that can pass against a previous version of the code under test is worse than none.
sys.dont_write_bytecode = True
importlib.invalidate_caches()
for stale in HERE.glob("__pycache__/channel-mix*.pyc"):
    stale.unlink()

# `channel-mix` has no .py suffix, so spec_from_file_location cannot infer a loader for it
# and returns None -- hand it a SourceFileLoader explicitly.
spec = importlib.util.spec_from_file_location(
    "channel_mix", SRC, loader=SourceFileLoader("channel_mix", str(SRC)))
cm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cm)

AI_UA = "Mozilla/5.0 (compatible; PerplexityBot/1.0)"
SE_UA = "Mozilla/5.0 (compatible; Googlebot/2.1)"


def fake_log(span_days, n_ai=40, n_se=10):
    """A log whose first->last hit span is exactly `span_days`, ending now."""
    now = time.time()
    first, last = now - span_days * 86400, now
    rows = []
    for i in range(n_ai):
        ts = first + (last - first) * (i / max(n_ai - 1, 1))
        rows.append((ts, AI_UA))
    for i in range(n_se):
        rows.append((first + (last - first) * (i / max(n_se - 1, 1)), SE_UA))
    out = []
    for ts, ua in rows:
        out.append(json.dumps({"ts": ts, "request": {
            "remote_ip": "203.0.113.7", "uri": "/",
            "headers": {"User-Agent": [ua]}}}) + "\n")
    return out


def run(argv, span_days):
    """Run channel-mix's main() against a synthetic log and capture its stdout."""
    rows = fake_log(span_days)
    cm.lines = lambda use_gz: iter(rows)
    cm.self_ips = lambda: {"127.0.0.1", "::1"}
    old = sys.argv
    sys.argv = ["channel-mix"] + argv
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            cm.main()
    finally:
        sys.argv = old
    return buf.getvalue()


FAILS = []
RAN = []


def check(name, cond, detail=""):
    print(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f"   {detail}" if detail and not cond else ""))
    RAN.append(name)
    if not cond:
        FAILS.append(name)


def main():
    print("channel-mix short-window gate self-test")

    # --- 1. the c2684 shape: a sub-day window must refuse to quote ----------------
    out = run(["--all", "--unknown", "0"], span_days=0.20)
    check("0.20d: WARNING banner printed", "DO NOT QUOTE" in out)
    # Guarded with `in` first: when the gate is broken (verified c2688 by setting
    # QUOTABLE_DAYS=0) a bare .index() raises ValueError and the traceback hides every
    # remaining check. A regression must print a readable FAIL list, not a stack trace.
    check("0.20d: banner is ABOVE the mix table, not below it",
          "DO NOT QUOTE" in out and "== channel mix" in out
          and out.index("DO NOT QUOTE") < out.index("== channel mix"))
    check("0.20d: per-day rates suppressed", "n/a*" in out)
    check("0.20d: no bogus /day extrapolation printed at all", "/day" not in out.split("== channel mix")[1])
    check("0.20d: ratio labelled NOT QUOTABLE", "NOT QUOTABLE" in out)
    check("0.20d: trailing reminder survives the long UA list", "REMINDER" in out)

    # --- 2. a real window must stay clean: a gate that always fires is useless ----
    out7 = run(["--all", "--unknown", "0"], span_days=7.0)
    check("7.00d: no WARNING banner", "DO NOT QUOTE" not in out7)
    check("7.00d: no NOT QUOTABLE label", "NOT QUOTABLE" not in out7)
    check("7.00d: real per-day rates printed", "/day" in out7 and "n/a*" not in out7)
    check("7.00d: ratio is the true 4.00:1 (40 ai / 10 search)", "AI : SEARCH = 4.00:1" in out7)

    # --- 3. the boundary is where QUOTABLE_DAYS says it is -----------------------
    check("gate constant is still 2 days", cm.QUOTABLE_DAYS == 2.0, f"got {cm.QUOTABLE_DAYS}")
    just_under = run(["--all", "--unknown", "0"], span_days=cm.QUOTABLE_DAYS - 0.01)
    just_over = run(["--all", "--unknown", "0"], span_days=cm.QUOTABLE_DAYS + 0.01)
    check("just UNDER the boundary fires", "DO NOT QUOTE" in just_under)
    check("just OVER the boundary does not", "DO NOT QUOTE" not in just_over)

    # --- 4. the second, independent half of the c2688 fix: the default window ----
    # Even if the gate were deleted, the default must not be "whatever the current log
    # file holds" -- that is the state that let c2684 sample five hours.
    check("DEFAULT_DAYS is a multi-day window", cm.DEFAULT_DAYS >= cm.QUOTABLE_DAYS,
          f"DEFAULT_DAYS={cm.DEFAULT_DAYS} < QUOTABLE_DAYS={cm.QUOTABLE_DAYS}")
    # A bare run (no --days/--all) must apply that default, and must read the rotated
    # files, or the default window cannot actually be reached after a rotation.
    seen = {}
    rows = fake_log(7.0)
    cm.lines = lambda use_gz: (seen.__setitem__("gz", use_gz), iter(rows))[1]
    cm.self_ips = lambda: {"127.0.0.1", "::1"}
    old, sys.argv = sys.argv, ["channel-mix", "--unknown", "0"]
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            cm.main()
    finally:
        sys.argv = old
    check("bare run implies --gz (rotated files are read)", seen.get("gz") is True,
          f"got {seen.get('gz')!r}")

    # --- 5. --weekly must NOT inherit the 7-day default: it needs the whole window
    # (regression caught during c2688's own testing -- the first cut clipped the
    # multi-week trend that is the only reason --weekly exists, c1676.)
    wk = run(["--weekly", "--unknown", "0"], span_days=56.0)
    weeks = [l for l in wk.splitlines() if l.strip().startswith("2026-W")]
    check("--weekly sees many weeks, not just one", len(weeks) >= 7, f"got {len(weeks)} week rows")

    # Counted, never hardcoded: a stale literal here would under-report its own coverage.
    print(f"\n{'ALL PASS' if not FAILS else 'FAILURES: ' + ', '.join(FAILS)}"
          f"  ({len(RAN) - len(FAILS)}/{len(RAN)})")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
