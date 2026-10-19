#!/usr/bin/env python3
"""Measure joint (multi-reporting-owner) Form 4 rate + bug-trigger direction for one trading day.

Direction that matters: owner[0]'s role-flag set is MISSING a flag that some later owner HAS
(so a filter on the first owner's roles would drop a row that genuinely matches).
"""
import json
import re
import sys
import time
import urllib.request
from collections import defaultdict

UA = "FetchSmith research contact@fetchsmith.com"


def get(url, raw=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                data = r.read()
                return data if raw else data.decode("utf-8", "replace")
        except Exception as e:
            if attempt == 3:
                raise
            time.sleep(1.5 * (attempt + 1))


def day(date, quarter):
    ymd = date.replace("-", "")
    idx = get(f"https://www.sec.gov/Archives/edgar/daily-index/{date[:4]}/QTR{quarter}/form.{ymd}.idx")
    owners = defaultdict(set)
    for line in idx.splitlines():
        if not line.startswith("4 ") and not line.startswith("4  "):
            continue
        parts = re.split(r"\s{2,}", line.strip())
        if len(parts) < 5 or parts[0] != "4":
            continue
        cik, fname = parts[2], parts[-1]
        m = re.search(r"(\d{10}-\d{2}-\d{6})", fname)
        if not m:
            continue
        owners[m.group(1)].add(cik)
    return owners


FLAGS = ("isDirector", "isOfficer", "isTenPercentOwner", "isOther")


def owner_flags(accession):
    nodash = accession.replace("-", "")
    j = json.loads(get(f"https://www.sec.gov/Archives/edgar/data/{nodash[:10].lstrip('0')}/"))
    return j


def primary_xml(accession, cik):
    nodash = accession.replace("-", "")
    txt = get(f"https://www.sec.gov/Archives/edgar/data/{cik}/{nodash}/{accession}-index.htm")
    m = re.findall(r'href="([^"]+\.xml)"', txt)
    for href in m:
        low = href.lower()
        if "index" in low or "xsl" in low:
            continue
        return "https://www.sec.gov" + href
    return None


def parse_owners(xml):
    out = []
    for block in re.findall(r"<reportingOwner>(.*?)</reportingOwner>", xml, re.S):
        name = re.search(r"<rptOwnerName>(.*?)</rptOwnerName>", block, re.S)
        rel = {}
        for f in FLAGS:
            v = re.search(rf"<{f}>(.*?)</{f}>", block, re.S)
            rel[f] = bool(v) and v.group(1).strip() in ("1", "true")
        title = re.search(r"<officerTitle>(.*?)</officerTitle>", block, re.S)
        out.append({
            "name": name.group(1).strip() if name else "?",
            "flags": frozenset(f for f in FLAGS if rel[f]),
            "officerTitle": title.group(1).strip() if title else None,
        })
    return out


def main():
    date, quarter = sys.argv[1], sys.argv[2]
    owners = day(date, quarter)
    # Each Form 4 is listed once per CIK: the issuer AND every reporting owner (LEARNINGS 1924).
    # So a single-owner filing already has 2 CIKs; joint filings have 3+.
    joint = {a: c for a, c in owners.items() if len(c) > 2}
    print(f"{date}: {len(owners)} Form 4 filings, {len(joint)} joint ({100*len(joint)/max(1,len(owners)):.1f}%)")
    triggers = []
    details = []
    for i, (acc, ciks) in enumerate(sorted(joint.items())):
        try:
            url = primary_xml(acc, sorted(ciks)[0].lstrip("0"))
            if not url:
                for c in sorted(ciks):
                    url = primary_xml(acc, c.lstrip("0"))
                    if url:
                        break
            if not url:
                details.append((acc, "no-xml"))
                continue
            o = parse_owners(get(url))
            time.sleep(0.2)
            if len(o) < 2:
                details.append((acc, f"idx said joint, xml has {len(o)} owners"))
                continue
            first = o[0]["flags"]
            union_rest = frozenset().union(*[x["flags"] for x in o[1:]])
            missing = union_rest - first
            details.append((acc, f"{len(o)} owners first={sorted(first)} rest={sorted(union_rest)} missing_on_first={sorted(missing)}"))
            if missing:
                triggers.append((acc, sorted(missing), [(x["name"], sorted(x["flags"])) for x in o]))
        except Exception as e:
            details.append((acc, f"ERR {e}"))
    for a, d in details:
        print(" ", a, d)
    print(f"\nTRIGGERS (first owner missing a role a later owner has): {len(triggers)}/{len(joint)}")
    for t in triggers:
        print("  ", t[0], t[1])
        for n, f in t[2]:
            print("      ", n, f)


main()
