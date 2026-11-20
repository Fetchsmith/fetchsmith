#!/usr/bin/env python3
"""Selftest for bin/_slug_args.py -- the vacuous-pass argv guard (cycle 3480).

Run: python3 bin/_slug_args_selftest.py   (exit 0 = pass, 1 = fail)
"""
import io
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _slug_args  # noqa: E402

FAILED = []


def expect_ok(label, requested, available):
    """validate() must return normally (no exit) and print nothing to stderr."""
    err = io.StringIO()
    real, sys.stderr = sys.stderr, err
    try:
        _slug_args.validate('check-fake', requested, available)
    except SystemExit as e:
        FAILED.append(f'{label}: exited {e.code}, expected a normal return')
        return
    finally:
        sys.stderr = real
    if err.getvalue():
        FAILED.append(f'{label}: wrote to stderr on a valid invocation: {err.getvalue()!r}')


def expect_exit2(label, requested, available, must_mention=()):
    """validate() must exit(2) and name the offending token(s) on stderr."""
    err = io.StringIO()
    real, sys.stderr = sys.stderr, err
    code = None
    try:
        _slug_args.validate('check-fake', requested, available)
    except SystemExit as e:
        code = e.code
    finally:
        sys.stderr = real
    if code != 2:
        FAILED.append(f'{label}: exit code {code!r}, expected 2')
        return
    out = err.getvalue()
    for frag in must_mention:
        if frag not in out:
            FAILED.append(f'{label}: stderr never mentioned {frag!r}; got {out!r}')


FLEET = ['hacker-news-scraper', 'shopify-products-scraper', 'ats-jobs-scraper']

# --- the full sweep must stay unguarded: this is the normal cycle invocation -------------
expect_ok('bare/empty-list', [], FLEET)
expect_ok('bare/None', None, FLEET)

# --- a real, existing selection must pass through untouched -----------------------------
expect_ok('one known slug', ['ats-jobs-scraper'], FLEET)
expect_ok('several known slugs', ['ats-jobs-scraper', 'hacker-news-scraper'], FLEET)
expect_ok('available as a set', ['ats-jobs-scraper'], set(FLEET))
expect_ok('duplicate known slug', ['ats-jobs-scraper', 'ats-jobs-scraper'], FLEET)

# --- the bug this module exists for: a name matching nothing -----------------------------
expect_exit2('typo slug', ['ats-job-scraper'], FLEET, ('unknown Actor slug', 'ats-job-scraper'))
expect_exit2('retired slug', ['zzz-nonexistent-slug'], FLEET, ('zzz-nonexistent-slug',))

# --- the exact slip that produced this module: an undefined flag read as a name ----------
expect_exit2('--all as a slug', ['--all'], FLEET, ('--all', 'looks like a flag', 'NO arguments'))
expect_exit2('-x short flag', ['-x'], FLEET, ('looks like a flag',))

# --- a partly-valid selection must still fail: the valid half would sweep and look clean --
expect_exit2('known + unknown', ['ats-jobs-scraper', 'bogus-slug'], FLEET, ('bogus-slug',))
# ...and must NOT name the valid one as unknown.
_err = io.StringIO()
_real, sys.stderr = sys.stderr, _err
try:
    _slug_args.validate('check-fake', ['ats-jobs-scraper', 'bogus-slug'], FLEET)
except SystemExit:
    pass
finally:
    sys.stderr = _real
if 'ats-jobs-scraper' in _err.getvalue():
    FAILED.append('known+unknown: named the VALID slug as unknown too')

# --- the `kind` noun is used verbatim (check-source-bytes passes roots, not slugs) --------
expect_exit2('default kind noun', ['nope/'], ['site', 'actors'], ('unknown Actor slug(s)',))
_e = io.StringIO()
_r, sys.stderr = sys.stderr, _e
try:
    _slug_args.validate('check-source-bytes', ['nope/'], ['site'], kind='root path')
except SystemExit:
    pass
finally:
    sys.stderr = _r
if 'Actor slug' in _e.getvalue():
    FAILED.append('custom kind: still said "Actor slug" after kind= was overridden')

# --- an empty `available` must not be treated as "everything is fine" --------------------
expect_exit2('empty available', ['any-slug'], [], ('any-slug',))

if FAILED:
    print('_slug_args_selftest: %d FAILURE(S)' % len(FAILED))
    for f in FAILED:
        print('  FAIL ' + f)
    sys.exit(1)
print('_slug_args_selftest: all checks passed (14 cases)')
