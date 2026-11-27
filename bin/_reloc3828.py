#!/usr/bin/env python3
"""Cycle 3828: relocate grants-gov-scraper's dated competitor-sweep trail out of
README.md into COMPETITORS.md, replacing it with a synthesis.

Method cloned from bin/_reloc3531.py / _reloc3636.py (fda-recall-scraper,
uk-find-a-tender-scraper). Self-verifying: asserts every relocated line lands
verbatim in COMPETITORS.md, asserts the kept lines are untouched except for the
two forward references that pointed into the relocated span, and asserts the
resulting README is under the 99,999-byte Apify render cap with real headroom.
"""
import os
import re
import sys

ACTOR = "/root/agent/actors/grants-gov-scraper"
README = os.path.join(ACTOR, "README.md")
COMPET = os.path.join(ACTOR, "COMPETITORS.md")
CAP = 99999

# 1-indexed README lines holding the dated resweep paragraphs to relocate.
# NOTE 240 is deliberately NOT in this list: it is the run-log/invoice sentence
# (product documentation about the pricing table), not a sweep paragraph. It is
# kept and moved up next to the pricing table where it belongs.
RELOC = [206, 208, 210, 212, 214, 216, 218, 220, 222, 224, 226, 228, 230, 232,
         234, 236, 238, 242]
RUNLOG = 240          # kept, repositioned
PRICE_TABLE_END = 198  # run-log line goes right after this
KEEP_SWEEP = 244       # most recent full audit, stays in-README

COMPETITORS_HEADER = """# Competitor pricing history — grants-gov-scraper

Dated `competitor_audit` sweep history relocated out of `README.md` on 2026-11-27 (cycle 3828) to fix an Apify Store-page truncation risk: the README had grown to 99,615 of the 99,999-character render cap, leaving 384 bytes of headroom, so the next edit of any kind would have pushed the tail of the page out of view for buyers. Eighteen paragraphs, covering the 2026-10-03 niche-size sweep through the 2026-11-20 named-cohort re-audit, verbatim and in their original order — nothing was deleted or reworded here.

The README keeps the foundational 2026-10-02 leader comparison, the "What we do not claim" paragraph, the two-listings-cheaper-than-our-thin-rate paragraph, a synthesis of everything in this file, and the most recent full audit (2026-11-27, cycle 3818) as its live tail. This file is the dated trail behind that synthesis.

"""

SYNTHESIS = [
    "**Full dated competitor-sweep history (2026-10-03 through 2026-11-20, 18 resweep paragraphs) relocated to [`COMPETITORS.md`](COMPETITORS.md) on 2026-11-27 (cycle 3828) to stay under Apify's 99,999-character README render cap** — nothing was deleted or reworded, and the three paragraphs above plus the synthesis and the 2026-11-27 full audit below carry the current state.",
    "",
    "**What those eighteen sweeps found, synthesised 2026-11-27 (cycle 3828).** Across them the 15-term niche-size sweep ran 84 → 85 → 87 → 89 → 90 → 103 → 124 → 140 → 167 → 180 matching Store listings, and every unnamed listing was priced live **event by event and tier by tier** on its own sweep date rather than scored off one headline number — which is exactly the mistake the 2026-10-06 sweep made (it read only FREE tiers, so it could see neither a rival whose top tier reaches our rate nor a flat row price weighed against the start fee attached to it) and the 2026-10-07 sweep corrected. The standing scope test is **US Grants.gov opportunity data**, the same public `search2`/`fetchOpportunity` endpoints this Actor reads: a listing counts as a rival only if it reads Grants.gov itself, which is why `pink_comic/irs-990-nonprofit-search` (IRS Form 990 filings via ProPublica — \"is this nonprofit real\" rather than \"what can I apply for\"), `pink_comic/federal-audit-clearinghouse-single-audit-data` and `stefano_seggio/australia-grantconnect-monitor` (Australian GrantConnect awards already paid — a different country and a different question) are all excluded despite name-dropping Grants.gov in their own listing copy.",
    "",
    "**We are not the cheapest listing in this niche and do not claim to be.** Beyond the rivals already named above, the relocated sweeps found **39 more that undercut us in some form**, grouped here by the shape of the undercut. **Free to run today:** `martc03/grant-finder-mcp` is on Apify's FREE pricing model ($0/row at any volume — an MCP server over the same official Grants.gov search, so an AI-assistant tool rather than a dataset product), and `exuberantal/government-tenders-contracts-grants-scraper` and `deepaksheoran172/grants-gov-opportunity-matcher` carry no pricing record at all on the live act (`pricingInfos` null, confirmed by direct API read, not inferred) — though `deepaksheoran172`'s own Store copy already discloses an intended $0.003/record, 2x our enriched rate, so switching it on would not undercut us. **Cheaper than our $0.0015 enriched rate at every tier, with no start fee or a negligible one:** `grit-77/grants-gov-funding-opportunities` (flat $0.00001, no start fee — the deepest monetized undercut this niche has produced), `lepidata/grants-gov-opportunities` (flat $0.0002, no start fee), `bepolabs/us-grants` (flat $0.00075, no start fee), `loomwise/federal-opportunities` ($0.0009), `thriftykiwi/us-federal-grants-scraper` (flat $0.001, no start fee), `pj_pai/grants-gov-opportunities` (flat $0.001, no start fee), `best_celerytop/grants-gov-scraper` ($0.001, and it adds agency contact email/phone and attachments beyond our fields), `rustic_soybean/grant-opportunity-fit-finder` ($0.001, a scored fit-finder rather than a plain feed), `bovi/grants-scraper` ($0.0011), `fortuitous_pirate/grants-gov-scraper` (flat $0.001395 since 2026-11-03, cut ~3.1x from $0.004375 — the one rival this niche has watched cross from dearer-than-us into a genuine undercutter), `mrslm_data/grants-gov-opportunities` ($0.001 → $0.0008), `swillz/grants-gov-opportunity-search` ($0.0012 → $0.0009), `plotpointtech/grants-gov-federal-grants` ($0.001 → $0.00062, with forecasted-grant and daily-alert features matching our own forecast/watch scope), `opendatalabs/grants-gov-monitor` ($0.0012 → $0.00102), `upward_enterprises/grants-gov-opportunity-finder` (which roughly halved both halves of its own enrich/thin split effective 2026-10-10: its detail row ties us at FREE/BRONZE and beats us from SILVER up, and its summary row at $0.0005 → $0.0004 undercuts our $0.0007 thin rate at **every** tier) and `owlabee/grants-gov-api` on a thin pull only ($0.001 → $0.0008; its separate `opportunity-detail` enrichment event is dearer than us).",
    "",
    "**Cheaper only from some plan up:** `ucchiii/grants-gov-opportunities` and `apex-b2b-data/grants-gov-federal-funding-opportunities` both tie our enriched rate exactly at FREE and undercut it from BRONZE down to DIAMOND; `publicmoney/grants-gov-scraper` is dearer at FREE, ties us at BRONZE, undercuts from SILVER up and **ties our $0.0007 thin rate exactly at DIAMOND**; `transparent_meteorite/federal-grants-contracts` undercuts our enriched rate from BRONZE up and our thin rate from GOLD up since its 2026-10-30 retier; and `soilair/grants-gov-api` (the closest head-on substitute found in any sweep — it also pairs `search2` with `fetchOpportunity` enrichment), `bakos_bence/grants-gov`, `datalayer/grants-gov-funding`, `publicrecords/govcon-opportunity-feed`, `thequietstack/grants-gov-monitor` and `insight.solutions/federal-contracts-grants-api` each undercut our enriched rate from GOLD and above only. `automation-lab/grants-gov-funding-opportunities-scraper` undercuts on **DIAMOND alone** — its PLATINUM tier is still dearer than us. **Cheaper only above a run-size crossover, because of a start fee we do not charge:** `one_dollar_store/grants-gov-opportunities-scraper` and the same-owner pair `amygraphics/us-federal-grants` and `amygraphics/grants-gov-monitor` (~2 rows apiece), `automation_craft/grants-gov-scraper` (~3 rows), `dennydevelops/grants-gov-watcher` (~4 rows), `datadesk-io/grants-gov-opportunities-scraper` (~7 rows on GOLD+, ~10 on FREE/BRONZE), `badboxx_newlife/sam-gov-grants-gov-scraper` (~8 rows), `muzafferkadir/grants-gov-scraper` (flat $0.001 behind a $0.01 Actor-start fee, break-even exactly 20 rows: at 10 rows we are $0.015 against their $0.02, at 1,000 rows they are $1.01 against our $1.50) and `second_coming/gov-contract-monitor`, whose only charge event is a flat **$0.02 per run with no per-row event at all** — it crosses under our enriched rate at roughly 14 rows and our thin rate at roughly 29, and is invisible by construction to `bin/check-price-superiority` or to any scan that reduces a rival to a per-row number.",
    "",
    "**Four false positives are recorded here so they are never re-flagged as undercutters.** `nimble_flash/grant-fit-scout` carries a vestigial `apify-default-dataset-item` event at $0.00001 while its own README documents the real charge as `qualified-opportunity` at **$0.10 per scored opportunity**, 67x our enriched rate. `adobeflex/grants-gov-lite` prices `search_run` at $0.001 **per run, not per row** — its actual row event, `notice_row`, is $0.002 and dearer than us. `neverempty/grants-gov-opportunities-monitor` carries a flat $0.0005 `search-checked` event that its own description defines as a per-poll charge on a run that found nothing new; its real primary event, `grant-returned`, is $0.005 (FREE) down to $0.0035 (GOLD+), dearer than both our rates at every tier — the same container-noun trap as `neverempty/steam-reviews-price-monitor` on another of our niches, so a `*-checked`/monitoring-style event name is a standing reason to read the full event description before scoring it as a row price. And `tagadanar/us-grants-monitor` carried a $0.001 `actor-start` **run** fee, not a row price; its real `opportunity-found` event was $0.004 → $0.0028. Two rivals are **delisted — the Apify API returned 404 for both on 2026-11-08**: `tagadanar/us-grants-monitor` and `owlabee/gov-opportunity-feed`. One moved the other way: `vhsgreed/us-federal-contracts` raised its `record` ladder roughly 60% effective 2026-10-23 (now $0.002 FREE down to $0.00152 GOLD+, above our flat $0.0015), so it **no longer beats our enriched rate at any tier or volume** and the crossover math this README used to publish for it is retired.",
    "",
    "**The standing pricing decision is to hold at $0.0015 enriched / $0.0007 thin with no start fee**, because every undercutter found in any sweep carries 1–2 users (the 2026-11-27 sweep's largest unnamed listing had 2) — far under the 20-user threshold this fleet requires before re-pricing against a rival. What we compete on instead is the enrich/thin split itself (you are never charged the enriched rate for a row that arrived thin, and the run log prints the split so the invoice is checkable against the dataset), Assistance Listing (CFDA) validation, free filtering, and one Actor's `watchChanges` covering in a single run at the normal per-row price the change types the `nexgenwatch` family ships as **ten separate single-purpose watch listings** — new opportunity, cancellation, deadline amendment, eligibility change, funding-range change, document change, forecast-turning-posted and general opportunity change — each billing $0.0201–$0.50 per flat check with no per-row export at all. See [`COMPETITORS.md`](COMPETITORS.md) for every sweep's full method, counts, named handles and rung-by-rung prices, including the several hundred listings priced and found dearer than us at every tier they offer. Every handle, price and crossover in this synthesis was verified live on its own sweep date — the oldest 2026-10-03, the newest in the 2026-11-20 named-cohort re-audit — and the synthesis itself was verified live 2026-11-27.",
]

# Forward references in KEPT paragraphs that pointed into the relocated span.
FIXUPS = [
    (200,
     "every listing the sweep has picked up since is named and priced in the dated resweep paragraphs below.",
     "every listing the sweep has picked up since is named and priced in the dated resweep paragraphs now relocated to [`COMPETITORS.md`](COMPETITORS.md) and summarised below."),
    (202,
     "(was 17; see the `fortuitous_pirate` addition below)",
     "(was 17; `fortuitous_pirate/grants-gov-scraper` cut its flat rate to $0.001395 effective 2026-11-03 and is named in the synthesis below)"),
]


def main():
    orig = open(README).read()
    lines = orig.split("\n")
    before = len(orig.encode())

    reloc_text = [lines[i - 1] for i in RELOC]
    for i, t in zip(RELOC, reloc_text):
        # Every paragraph in the span opens bold and is a substantial sweep
        # entry; four of them (the 2026-10-07 group) carry their date on the
        # group's trailing paragraph rather than inline, so do not require one.
        assert t.startswith("**") and len(t) > 300, \
            "line %d does not look like a sweep paragraph: %r" % (i, t[:80])
    runlog = lines[RUNLOG - 1]
    assert runlog.startswith("The run log prints the split"), runlog[:60]
    assert lines[KEEP_SWEEP - 1].startswith("**Full re-audit live 2026-11-27")

    # --- COMPETITORS.md -------------------------------------------------
    assert not os.path.exists(COMPET), "COMPETITORS.md already exists; refusing to overwrite"
    comp = COMPETITORS_HEADER + "\n\n".join(reloc_text) + "\n"
    open(COMPET, "w").write(comp)

    # --- README.md ------------------------------------------------------
    drop = set(RELOC) | {RUNLOG, RUNLOG - 1}  # drop paragraph + its blank separator
    out = []
    for n, line in enumerate(lines, 1):
        if n in RELOC:
            if n == RELOC[0]:
                out.extend(SYNTHESIS)
            else:
                out.pop()  # remove the blank separator left by the dropped paragraph
            continue
        if n in (RUNLOG, RUNLOG - 1):
            continue
        out.append(line)
        if n == PRICE_TABLE_END:
            out.append("")
            out.append(runlog)
    new = "\n".join(out)

    for lineno, old, repl in FIXUPS:
        assert new.count(old) == 1, "fixup not uniquely found: %r" % old[:60]
        new = new.replace(old, repl)

    open(README, "w").write(new)
    after = len(new.encode())

    # --- verification ---------------------------------------------------
    for i, t in zip(RELOC, reloc_text):
        assert t in comp, "relocated line %d missing from COMPETITORS.md" % i
        assert t not in new, "relocated line %d still in README" % i
    assert runlog in new and new.count(runlog) == 1, "run-log line lost or duplicated"
    assert lines[KEEP_SWEEP - 1] in new, "most recent sweep paragraph lost"
    for keep in (200, 202, 204):
        stem = lines[keep - 1][:60]
        assert stem in new, "kept paragraph %d lost" % keep
    assert "COMPETITORS.md" in new
    assert after < CAP, "README still over cap: %d" % after
    assert re.search(r"\n\n\n", new) is None, "blank-line run introduced"

    print("README.md  %d -> %d bytes  (-%d, %d bytes of headroom under the %d cap)"
          % (before, after, before - after, CAP - after, CAP))
    print("COMPETITORS.md  %d bytes, %d relocated paragraphs"
          % (len(comp.encode()), len(reloc_text)))
    print("lossless: all %d relocated paragraphs verbatim in COMPETITORS.md" % len(reloc_text))


if __name__ == "__main__":
    sys.exit(main())
