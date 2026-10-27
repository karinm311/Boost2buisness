#!/usr/bin/env python3
"""Is the hero CTA in the first screen? Checks 10 real-world viewports.

A viewport passes when at least 85% of the hero CTA's height is visible
before any scrolling. The tool also reports the h1 line count and whether the
mobile sticky bar is (wrongly) showing while the hero CTA is on screen.

usage:  python3 tools/firstscreen.py http://127.0.0.1:8765/ [more urls] [--selector '[data-cta="hero"]']
Give every page's main CTA data-cta="hero" so the same check works on all pages.
"""
import argparse
import json
import sys

from playwright.sync_api import sync_playwright

VIEWPORTS = [(360, 640), (375, 667), (390, 664), (390, 844), (430, 932),
             (768, 1024), (1280, 720), (1366, 650), (1440, 800), (1920, 950)]

JS = r"""
(sel) => {
  const el = document.querySelector(sel);
  if (!el) return null;
  const r = el.getBoundingClientRect(), vh = innerHeight;
  const visible = Math.max(0, Math.min(r.bottom, vh) - Math.max(r.top, 0));
  const h1 = document.querySelector('h1');
  let lines = null;
  if (h1) { const lh = parseFloat(getComputedStyle(h1).lineHeight) || 1; lines = Math.round(h1.getBoundingClientRect().height / lh); }
  const bar = document.querySelector('[data-cta="bar"]');
  let barShown = false;
  if (bar) { const b = bar.getBoundingClientRect(); const s = getComputedStyle(bar.closest('.bar') || bar);
             barShown = b.height > 0 && b.top < vh && s.visibility !== 'hidden' && s.display !== 'none'; }
  return { top: Math.round(r.top), bottom: Math.round(r.bottom), frac: r.height ? visible / r.height : 0, h1Lines: lines, barShown };
}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("urls", nargs="+")
    ap.add_argument("--selector", default='[data-cta="hero"]')
    ap.add_argument("--min", type=float, default=0.85, help="minimum visible fraction (default 0.85)")
    args = ap.parse_args()
    bad = 0
    out = {}
    with sync_playwright() as p:
        b = p.chromium.launch()
        for url in args.urls:
            print(f"\n{url}")
            out[url] = []
            for w, h in VIEWPORTS:
                ctx = b.new_context(viewport={"width": w, "height": h}, is_mobile=w < 700, has_touch=w < 700,
                                    device_scale_factor=2 if w < 700 else 1)
                pg = ctx.new_page()
                pg.goto(url, wait_until="load")
                pg.wait_for_timeout(900)
                r = pg.evaluate(JS, args.selector)
                ctx.close()
                if r is None:
                    print(f"  {w}x{h}: ❌ no element matches {args.selector}")
                    bad += 1
                    continue
                ok = r["frac"] >= args.min
                bar_bad = r["barShown"] and ok
                bad += (not ok) + bar_bad
                print(f"  {w}x{h}: {'✅' if ok else '❌'} CTA {r['top']}–{r['bottom']}px, {r['frac']*100:.0f}% visible"
                      f" · h1 lines {r['h1Lines']}" + (" · ⚠️ sticky bar showing on top of the hero CTA" if bar_bad else ""))
                out[url].append({"vp": f"{w}x{h}", **r, "ok": ok})
        b.close()
    print("\nRESULT:", "PASS ✅" if not bad else f"FAIL ❌ ({bad})")
    json.dump(out, open("firstscreen.json", "w"), indent=1)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
