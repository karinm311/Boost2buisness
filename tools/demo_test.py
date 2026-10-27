#!/usr/bin/env python3
"""Play every scripted demo to the end, by tap at 360px and by keyboard, and time it.

Each demo must reach its 3rd step (all .dsteps lit) within 90 s, with no JS errors,
and its badge must read "הדגמה · נתונים לדוגמה".

usage:  python3 tools/demo_test.py http://127.0.0.1:8765
"""
import sys, time
from playwright.sync_api import sync_playwright

BASE = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://127.0.0.1:8765"
PAGES = ["/team/chani", "/team/dana", "/team/shira", "/team/noga", "/team/gal", "/training", "/solutions"]
bad = 0


def play(pg, box, keyboard=False):
    t0 = time.time()
    for _ in range(12):
        lit = box.locator(".dsteps i.on").count()
        if lit >= 3:
            return time.time() - t0
        btns = box.locator(".dstage button:not([disabled])" if lit == 0 else ".dstage .ask button")
        if btns.count():
            b = btns.first
            if keyboard:
                b.focus(); pg.keyboard.press("Enter")
            else:
                b.tap()
        pg.wait_for_timeout(2500)
    return None


with sync_playwright() as p:
    br = p.chromium.launch()
    for mode in ("tap", "keyboard", "reduced"):
        ctx = br.new_context(viewport={"width": 360, "height": 640}, is_mobile=True, has_touch=True,
                             reduced_motion="reduce" if mode == "reduced" else "no-preference")
        pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        for path in PAGES:
            pg.goto(BASE + path); pg.wait_for_timeout(600)
            box = pg.locator(".demo").first
            badge = box.locator(".dbadge").inner_text()
            took = play(pg, box, keyboard=(mode == "keyboard"))
            ok = took is not None and took <= 90 and badge.strip() == "הדגמה · נתונים לדוגמה" and not errs
            bad += not ok
            print(f"{'✅' if ok else '❌'} {mode:<8} {path:<13} {('%.1fs' % took) if took else 'did not finish'}  badge='{badge}' {errs[:2]}")
            errs.clear()
        # home tabs: every tab opens its demo
        pg.goto(BASE + "/"); pg.wait_for_timeout(500)
        for slug in ["chani", "dana", "shira", "noga", "gal"]:
            pg.locator(f"#tab-{slug}").click(); pg.wait_for_timeout(300)
            vis = pg.locator(f"#demo-{slug}").is_visible()
            took = play(pg, pg.locator(f"#demo-{slug}")) if mode == "tap" else 0
            ok = vis and took is not None and not errs
            bad += not ok
            if mode == "tap" or not ok:
                print(f"{'✅' if ok else '❌'} {mode:<8} home tab {slug:<6} visible={vis} {('%.1fs' % took) if took else ''} {errs[:2]}")
        ctx.close()
    br.close()
print("RESULT:", "PASS ✅" if not bad else f"FAIL ❌ ({bad})")
sys.exit(1 if bad else 0)
