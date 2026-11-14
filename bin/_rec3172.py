#!/usr/bin/env python3
"""c3172 enum_audit hand-check for trademark-search-scraper's matchMode enum.

bin/vocab-screen's p_trademark_search_tm_types() proves the criteria C/W/E codes live, which
covers matchMode's contains/startsWith/endsWith. It does NOT cover the 4th declared enum value,
`startsWithPrefix`: that mode asks TMview for `criteria:C` and does its own client-side prefix
filter (main.js:181/213-218), so upstream liveness proves nothing about it. This probe re-proves
the mode's two load-bearing README/schema claims live:
  (1) the filter still has real work to do -- TMview's own `contains` corpus for the term holds
      names where the term is NOT at the start, which is the whole reason the mode exists;
  (2) the concrete examples the schema description promises still hold on live data:
      "coff" keeps COFFEE / Coff Chi (and the folded CØFFE form, c2871) and drops names like
      "HAIR SYRUP coff" where coff appears but not at the start.
Also probes the `statuses` closed vocabulary (4 values + negative control), which vocab-screen
does not reach either.

Read-only GETs/POSTs against TMview's public search API. No spend, no platform run.
"""
import http.cookiejar
import json
import re
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/120.0.0.0 Safari/537.36")
TIMEOUT = 60

DIACRITIC_MAP = {"ø": "o", "Ø": "o", "æ": "ae", "Æ": "ae", "œ": "oe", "Œ": "oe",
                 "ð": "d", "Ð": "d", "þ": "th", "Þ": "th", "ł": "l", "Ł": "l",
                 "đ": "d", "Đ": "d"}


def strip_lead(s):
    """Python mirror of main.js:213 stripLead(): NFKC, fold diacritics (explicit map for the
    non-decomposing letters, then NFD + combining-mark strip), drop leading whitespace/
    punctuation/symbols, lowercase."""
    s = unicodedata.normalize("NFKC", str(s or ""))
    s = "".join(DIACRITIC_MAP.get(c, c) for c in s)
    s = "".join(c for c in unicodedata.normalize("NFD", s)
                if not unicodedata.combining(c))
    i = 0
    while i < len(s) and (s[i].isspace() or unicodedata.category(s[i])[0] in ("P", "S")):
        i += 1
    return s[i:].lower()


def tmview_post(body):
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    opener.open(urllib.request.Request("https://www.tmdn.org/tmview/",
                                       headers={"User-Agent": UA}), timeout=TIMEOUT)
    req = urllib.request.Request(
        "https://www.tmdn.org/tmview/api/search/results",
        data=json.dumps(body).encode(),
        headers={"User-Agent": UA, "Content-Type": "application/json",
                 "Accept": "application/json", "Referer": "https://www.tmdn.org/tmview/"})
    try:
        with opener.open(req, timeout=TIMEOUT) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


fail = []

# ---- (1)+(2) startsWithPrefix: client-side prefix filter over criteria:C ----
TERM = "coff"
needle = strip_lead(TERM)
status, resp = tmview_post({"page": "0", "pageSize": "50", "criteria": "C",
                            "basicSearch": TERM, "fOffices": ["GB"]})
print(f"criteria=C basicSearch={TERM!r} fOffices=[GB] pageSize=50 -> HTTP {status}")
if status != 200 or not isinstance(resp, dict):
    print(f"  PROBE INVALID: {str(resp)[:300]}")
    raise SystemExit(1)
total = resp.get("totalResults")
rows = resp.get("tradeMarks") or resp.get("trademarks") or []
print(f"  totalResults={total}  rows on page 1={len(rows)}")
# response row key is `tmName`; main.js:577 is what renames it to trademarkName on output
names = [r.get("tmName") for r in rows]
kept = [n for n in names if strip_lead(n).startswith(needle)]
dropped = [n for n in names if not strip_lead(n).startswith(needle)]
print(f"  prefix filter: {len(kept)}/{len(names)} kept, {len(dropped)} dropped")
print(f"  sample kept   : {kept[:8]}")
print(f"  sample dropped: {dropped[:8]}")
if not kept:
    fail.append("startsWithPrefix kept 0 rows on page 1 (mode would deliver nothing)")
if not dropped:
    fail.append("startsWithPrefix dropped 0 rows -- filter has no work to do, "
                "mode is now indistinguishable from `contains`")
# the schema's concrete promises
coffee_like = [n for n in kept if strip_lead(n).startswith("coffee")]
print(f"  claim: COFFEE-style prefix rows present -> {bool(coffee_like)} {coffee_like[:4]}")
if not coffee_like:
    fail.append("no COFFEE-style row kept (schema description promises 'coff' returns COFFEE)")
mid_term = [n for n in dropped if "coff" in strip_lead(n)]
print(f"  claim: term-not-at-start rows exist and are dropped -> {bool(mid_term)} {mid_term[:4]}")
if not mid_term:
    fail.append("no dropped row actually contained the term mid-name -- cannot confirm the "
                "'HAIR SYRUP coff'-shaped case the schema description promises is excluded")
# c2871 diacritic fix: a row that only matches AFTER folding
folded_only = [n for n in kept if not strip_lead(n).startswith(needle)
               or (strip_lead(n).startswith(needle) and n.lower()[:len(needle)] != needle
                   and any(c in n for c in DIACRITIC_MAP))]
print(f"  c2871 diacritic-folded rows kept: {folded_only[:4]}")

# ---- statuses closed vocabulary (4 values) + negative control ----
print("\nstatuses vocabulary (schema: exactly four values):")
schema_path = "/root/agent/actors/trademark-search-scraper/.actor/input_schema.json"
desc = json.load(open(schema_path))["properties"]["statuses"]["description"]
m = re.search(r"recognises exactly four values:\s*([^.]+)\.", desc)
documented = [s.strip() for s in m.group(1).split(",")] if m else []
print(f"  schema documents: {documented}")
if len(documented) != 4:
    fail.append(f"could not parse 4 documented statuses out of the schema (got {documented})")
st_totals = {}
for s in documented:
    st, r = tmview_post({"page": "0", "pageSize": "1", "criteria": "C",
                         "basicSearch": "coffee", "fTMStatus": [s]})
    st_totals[s] = r.get("totalResults") if st == 200 and isinstance(r, dict) else None
    print(f"    {s:12s} HTTP {st}  totalResults={st_totals[s]}")
dead = [s for s, n in st_totals.items() if not n]
if dead:
    fail.append(f"documented statuses returning nothing: {dead}")
if len(set(st_totals.values())) == 1:
    fail.append("every status returned the same total -- filter ignored, proves nothing")
bst, br = tmview_post({"page": "0", "pageSize": "1", "criteria": "C",
                       "basicSearch": "coffee", "fTMStatus": ["Opposed"]})
btot = br.get("totalResults") if isinstance(br, dict) else None
print(f"  negative control fTMStatus='Opposed': HTTP {bst} totalResults={btot} "
      f"({'fails closed, matches schema' if btot == 0 else 'CONTRADICTS fails-closed claim'})")
if btot != 0:
    fail.append("bogus status did not fail closed (schema claims it matches no marks)")

print("\n=== RESULT: " + ("CLEAN -- no drift" if not fail else "MISMATCHES: " + "; ".join(fail)))
