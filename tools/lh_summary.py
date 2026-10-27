#!/usr/bin/env python3
"""Summarise Lighthouse JSON runs: a per-run table, the median, pass/fail, and what to fix.

usage:  python3 tools/lh_summary.py lh/      (reads lh/m*.json for mobile, lh/d*.json for desktop)
Writes lh/summary.json. Exit code 1 if the median misses the bar:
  Performance, Accessibility, Best Practices, SEO >= 95 · mobile LCP <= 2000 ms
"""
import glob
import json
import os
import statistics
import sys

BAR = 95
LCP_MAX = 2000


def load(path):
    lhr = json.load(open(path))
    cat = lhr["categories"]
    a = lhr["audits"]
    num = lambda k: (a.get(k) or {}).get("numericValue")  # noqa: E731
    reqs = len(((a.get("network-requests") or {}).get("details") or {}).get("items") or [])
    row = {
        "perf": round((cat["performance"]["score"] or 0) * 100),
        "a11y": round((cat["accessibility"]["score"] or 0) * 100),
        "bp": round((cat["best-practices"]["score"] or 0) * 100),
        "seo": round((cat["seo"]["score"] or 0) * 100),
        "fcp": num("first-contentful-paint"), "lcp": num("largest-contentful-paint"),
        "tbt": num("total-blocking-time"), "cls": num("cumulative-layout-shift"),
        "si": num("speed-index"), "kb": round((num("total-byte-weight") or 0) / 1024), "req": reqs,
    }
    # audits that lost points (non-perf categories) + top perf opportunities
    issues = []
    for cid in ("accessibility", "best-practices", "seo"):
        for ref in cat[cid]["auditRefs"]:
            au = a.get(ref["id"]) or {}
            if ref.get("weight", 0) > 0 and au.get("score") is not None and au["score"] < 1:
                issues.append(f"[{cid}] {au.get('title')}")
    for k, au in a.items():
        d = au.get("details") or {}
        if d.get("type") == "opportunity" and (d.get("overallSavingsMs") or 0) >= 100:
            issues.append(f"[perf] {au.get('title')} (~{round(d['overallSavingsMs'])} ms)")
    row["issues"] = issues
    return row


def fmt(r):
    return (f"perf {r['perf']:>3} · a11y {r['a11y']:>3} · bp {r['bp']:>3} · seo {r['seo']:>3} · "
            f"FCP {r['fcp']/1000:.2f}s · LCP {r['lcp']/1000:.2f}s · TBT {r['tbt']:.0f}ms · CLS {r['cls']:.3f} · "
            f"{r['kb']} KB / {r['req']} req")


def median_row(rows):
    keys = ["perf", "a11y", "bp", "seo", "fcp", "lcp", "tbt", "cls", "si", "kb", "req"]
    return {k: statistics.median([r[k] for r in rows if r[k] is not None]) for k in keys}


def main():
    d = sys.argv[1] if len(sys.argv) > 1 else "lh"
    mob = [load(p) for p in sorted(glob.glob(os.path.join(d, "m*.json")))]
    desk = [load(p) for p in sorted(glob.glob(os.path.join(d, "d*.json")))]
    if not mob:
        sys.exit(f"no mobile runs in {d}/")
    print("\nMobile runs:")
    for i, r in enumerate(mob, 1):
        print(f"  {i}. {fmt(r)}")
    med = median_row(mob)
    print(f"\nMOBILE MEDIAN:  {fmt(med)}")
    if desk:
        print(f"DESKTOP:        {fmt(desk[0])}")
    fails = [k for k in ("perf", "a11y", "bp", "seo") if med[k] < BAR]
    if med["lcp"] > LCP_MAX:
        fails.append(f"LCP {med['lcp']/1000:.2f}s > {LCP_MAX/1000:.1f}s")
    issues = sorted({i for r in mob for i in r["issues"]})
    if issues:
        print("\nThings Lighthouse flagged (any run):")
        for i in issues:
            print("  -", i)
    print("\nRESULT:", "PASS ✅" if not fails else f"FAIL ❌ {fails}")
    json.dump({"runs": mob, "median": med, "desktop": desk[0] if desk else None, "fails": fails},
              open(os.path.join(d, "summary.json"), "w"), indent=1)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
