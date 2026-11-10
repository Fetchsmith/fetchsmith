#!/root/agent/venv/bin/python
"""Self-test for bin/check-absence-claims. No network, no auth, no platform cost.

The two properties worth locking down are both exclusions, i.e. the places where a
reasonable future edit would silently make the check lie:

  1. the c2864 regression. The founding incident's claim is PRESERVED VERBATIM in a
     blockquote in the corrected post on purpose. If prose_lines() ever stops skipping
     `>`-prefixed lines, the check re-reports its own retracted incident forever and
     whoever reads it will "fix" a correction. Asserted both ways: the quoted form is
     invisible, the same sentence unquoted is seen and lands in SELF-SCOPED.
  2. the self/upstream split, which is the only thing this check claims to do
     mechanically. A sentence about openFDA must not be called ours; a sentence about
     "the Actor" must be.

Follows the c2688 standing rule (queue.md): sys.dont_write_bytecode, invalidate_caches,
and unlink any stale extensionless .pyc BEFORE the first load, or this can print ALL PASS
against a PREVIOUS version of the target. Counts its own passes (len(RAN)), never
hardcodes the total, and guards every assertion with `in` rather than a bare index().
"""
import importlib
import os
import sys

sys.dont_write_bytecode = True
BIN = os.path.dirname(os.path.abspath(__file__))
for stale in ("check-absence-claims.pyc", "check-absence-claims.cpython-%d%d.pyc"
              % sys.version_info[:2]):
    p = os.path.join(BIN, "__pycache__", stale)
    if os.path.exists(p):
        os.unlink(p)
importlib.invalidate_caches()
from importlib.machinery import SourceFileLoader  # noqa: E402

cac = SourceFileLoader("cac", os.path.join(BIN, "check-absence-claims")).load_module()

RAN, FAIL = [], []


def check(name, got, want):
    RAN.append(name)
    if got != want:
        FAIL.append("%s: got %r want %r" % (name, got, want))


# ---- the c2864 sentence, in both forms ------------------------------------------------
C2864 = ("There's no field anywhere in the Play Store review payload that says *when* a "
         "reply was posted; the only timestamp the Actor can see is the review's own "
         "`date`, not the reply's.")
GP = "google-play-reviews-scraper"

doc_quoted = "---\ntitle: x\ntool: %s\n---\n\n> **The original section:** \"%s\"\n" % (GP, C2864)
doc_live = "---\ntitle: x\ntool: %s\n---\n\n%s\n" % (GP, C2864)

check("blockquoted claim is invisible",
      [s for _, s in cac.prose_lines(doc_quoted)], [])
check("unquoted claim is visible",
      len(cac.prose_lines(doc_live)), 1)
check("c2864 sentence matches the absence vocabulary",
      bool(cac.ABSENCE_RE.search(C2864)), True)
check("c2864 sentence is SELF-SCOPED ('the Actor')",
      cac.self_scoped(C2864, GP), True)
check("c2864 sentence is not exempt", cac.exempt(C2864), None)

# The documented negative result: the c2864 rule-as-proposed cannot see `replyDate`,
# because the sentence never names it. Locking this in so nobody re-proposes the rule.
check("proposed field-name rule misses replyDate (documented, not a bug)",
      "replyDate" in cac.field_refs(C2864.split(";")[0], cac.REG[GP]), False)

# ---- fenced code and front matter are not prose --------------------------------------
fenced = "---\ntool: %s\n---\n\n```\n// there is no such field\n```\nreal prose here.\n" % GP
check("fenced code is skipped",
      [s.strip() for _, s in cac.prose_lines(fenced)], ["real prose here."])

# ---- the self / upstream split --------------------------------------------------------
check("upstream claim is not self-scoped",
      cac.self_scoped("openFDA's endpoint has no pagination cursor at all.", GP), False)
check("slug mention counts as self-scoped",
      cac.self_scoped("There is no locale mode in %s." % GP, GP), True)
check("/go/ CTA link counts as self-scoped",
      cac.self_scoped("There is no such option in [it](/go/%s)." % GP, GP), True)

# ---- field_refs precision: backticked / camelCase only -------------------------------
check("bare lowercase English word is not a field reference",
      cac.field_refs("there is no date on it", cac.REG[GP]), [])
check("backticked field is a field reference",
      cac.field_refs("there is no `replyDate` on it", cac.REG[GP]), ["replyDate"])
check("camelCase field is a field reference",
      cac.field_refs("there is no replyDate on it", cac.REG[GP]), ["replyDate"])
check("dotted/indexed backtick still names the field",
      cac.field_refs("nothing in the `row['replyDate']` path", cac.REG[GP]), ["replyDate"])

# ---- exemptions ----------------------------------------------------------------------
check("'no API key, no login' is exempt as a selling line",
      cac.exempt("No API key, no login, no proxy: this Actor uses a public API.") is not None,
      True)
check("'no run size ... cheaper choice' is exempt as a price claim",
      cac.exempt("so there is no run size at which we are the cheaper choice") is not None,
      True)

# ---- registry wiring -----------------------------------------------------------------
check("registry loaded and `_`-prefixed watch columns excluded",
      bool(cac.REG) and not any(f.startswith("_") for v in cac.REG.values() for f in v),
      True)

print("\n".join("FAIL  " + f for f in FAIL) if FAIL else "", end="")
print("%s %d/%d checks" % ("FAIL" if FAIL else "ALL PASS", len(RAN) - len(FAIL), len(RAN)))
sys.exit(1 if FAIL else 0)
