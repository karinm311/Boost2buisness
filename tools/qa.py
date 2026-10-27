#!/usr/bin/env python3
"""QA "doctor" for the Boost2Business site, built on Playwright Chromium.

It checks every page at 360/390/768/1024/1280/1440 px wide. Checks marked
FAIL make the exit code 1; WARN items are worth a look.

  FAIL  horizontal scroll · JS errors · console errors · same-origin requests
        that fail or return >=400 · broken images · in-page #anchors without
        a target · WhatsApp links that don't point to Karin's number · pages
        with no WhatsApp link · reveal elements still hidden after scrolling ·
        h1 count != 1 · <img> without alt · form controls without a label ·
        CTAs ([data-cta]) smaller than 44px · missing lang="he"/dir="rtl" ·
        a reduced-motion pass that leaves content hidden
  WARN  content past the screen edge (clipped) · small tap targets · clipped
        text · missing title/description/og:image · relative og:image ·
        duplicate ids · failing cross-origin requests

usage:
  python3 tools/serve.py site/dist 8765 &   # in another shell
  python3 tools/qa.py http://127.0.0.1:8765/ --crawl --shots qa_out
  python3 tools/qa.py http://127.0.0.1:8765/team/chani.html --widths 360,1280

The report is printed and saved to <shots>/qa_report.json (default qa_out/).
"""
import argparse
import json
import os
import re
import sys
from urllib.parse import urljoin, urlparse, urldefrag

from playwright.sync_api import sync_playwright

WIDTHS = [360, 390, 768, 1024, 1280, 1440]
WA_DEFAULT = "https://wa.me/972547501261"

CHECK_JS = r"""
(opts) => {
  const de = document.documentElement, vw = de.clientWidth;
  const fail = [], warn = [];
  const vis = e => { const s = getComputedStyle(e); const r = e.getBoundingClientRect();
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
  const desc = e => (e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') +
    (typeof e.className === 'string' && e.className.trim() ? '.' + e.className.trim().split(/\s+/).slice(0,2).join('.') : '') +
    ' "' + (e.innerText || e.getAttribute('aria-label') || '').trim().slice(0, 30).replace(/\s+/g,' ') + '"');

  // 1. horizontal scroll
  if (de.scrollWidth > vw + 1) fail.push(`horizontal scroll: scrollWidth ${de.scrollWidth} > ${vw}`);
  // 1b. content past the edge (hidden by a root clip, so the user just loses it)
  const past = [];
  for (const e of document.querySelectorAll('body *')) {
    if (past.length >= 6) break;
    if (!e.innerText || !e.innerText.trim() || e.closest('[aria-hidden="true"]')) continue;
    if (e.children.length > 0 && [...e.children].some(c => c.innerText && c.innerText.trim())) continue; // leaf-ish text nodes only
    const r = e.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    if (r.right > vw + 2 || r.left < -2) {
      let p = e.parentElement, clippedByAncestor = false;
      while (p && p !== document.body && p !== de) {
        const s = getComputedStyle(p);
        if (/(hidden|clip|auto|scroll)/.test(s.overflowX)) { clippedByAncestor = true; break; }
        p = p.parentElement;
      }
      if (!clippedByAncestor) past.push(desc(e) + ` [${Math.round(r.left)}..${Math.round(r.right)}]`);
    }
  }
  if (past.length) warn.push('text past screen edge: ' + past.join(' | '));

  // 2. images
  const broken = [...document.images].filter(i => i.complete && i.naturalWidth === 0 && i.currentSrc).map(i => i.currentSrc.slice(-50));
  if (broken.length) fail.push('broken images: ' + broken.join(', '));
  const noalt = [...document.images].filter(i => !i.hasAttribute('alt')).map(i => (i.currentSrc || i.src).slice(-40));
  if (noalt.length) fail.push('img without alt: ' + noalt.join(', '));
  const svgNoName = [...document.querySelectorAll('svg[role="img"]')].filter(s => !s.getAttribute('aria-label') && !s.querySelector('title') && !s.getAttribute('aria-labelledby')).length;
  if (svgNoName) warn.push(`${svgNoName} svg[role=img] without a name`);

  // 3. anchors
  const missing = [...document.querySelectorAll('a[href^="#"]')].map(a => a.getAttribute('href'))
    .filter(h => h.length > 1 && !document.getElementById(decodeURIComponent(h.slice(1))));
  if (missing.length) fail.push('anchors without target: ' + [...new Set(missing)].join(', '));

  // 4. WhatsApp
  const wa = [...document.querySelectorAll('a[href*="wa.me"], a[href*="api.whatsapp.com"], a[href*="whatsapp://"]')].map(a => a.href);
  if (opts.wa) {
    const bad = wa.filter(h => !(h === opts.wa || h.startsWith(opts.wa + '?') || h.startsWith(opts.wa + '/?')));
    if (bad.length) fail.push('WhatsApp links to the wrong place: ' + bad.join(', '));
    if (!wa.length) fail.push('no WhatsApp link on this page');
  }

  // 5. stuck hidden reveal elements
  const stuck = [...document.querySelectorAll(opts.reveal)].filter(e => parseFloat(getComputedStyle(e).opacity) < 0.5 && !e.closest('[hidden],[aria-hidden="true"]'));
  if (stuck.length) fail.push(`${stuck.length} reveal elements still hidden: ` + stuck.slice(0, 4).map(desc).join(' | '));

  // 6. headings / document
  const h1 = document.querySelectorAll('h1').length;
  if (h1 !== 1) fail.push(`h1 count is ${h1} (want 1)`);
  if ((de.getAttribute('lang') || '').slice(0, 2) !== 'he') fail.push('html lang is not "he"');
  if ((de.getAttribute('dir') || document.body.getAttribute('dir') || getComputedStyle(document.body).direction) !== 'rtl') fail.push('page is not rtl');
  if (!document.title.trim()) warn.push('empty <title>');
  if (!document.querySelector('meta[name="description"]')) warn.push('no meta description');
  const og = document.querySelector('meta[property="og:image"]');
  if (!og) warn.push('no og:image');
  else if (!/^https:\/\//.test(og.content)) warn.push('og:image is not an absolute https URL (LinkedIn/WhatsApp previews will fail)');

  // 7. forms
  const unlabeled = [...document.querySelectorAll('input:not([type=hidden]), select, textarea')].filter(el => {
    if (el.getAttribute('aria-label') || el.getAttribute('aria-labelledby') || el.title) return false;
    if (el.id && document.querySelector(`label[for="${CSS.escape(el.id)}"]`)) return false;
    return !el.closest('label');
  }).map(desc);
  if (unlabeled.length) fail.push('form controls without a label: ' + unlabeled.join(' | '));

  // 8. tap targets
  const small = [], smallCta = [];
  for (const e of document.querySelectorAll('a, button, summary, [role="button"], [role="tab"], input, select, textarea')) {
    if (!vis(e)) continue;
    const s = getComputedStyle(e);
    if (e.tagName === 'A' && s.display === 'inline' && e.closest('p, li') && !e.hasAttribute('data-cta')) continue; // inline text links are exempt
    const r = e.getBoundingClientRect();
    if (Math.min(r.width, r.height) < 43.5) {  // 0.5px tolerance for sub-pixel layout
      (e.hasAttribute('data-cta') ? smallCta : small).push(desc(e) + ` ${Math.round(r.width)}x${Math.round(r.height)}`);
    }
  }
  if (smallCta.length) fail.push('CTA smaller than 44px: ' + smallCta.slice(0, 5).join(' | '));
  if (small.length) warn.push(`${small.length} tap targets < 44px: ` + small.slice(0, 5).join(' | '));

  // 9. clipped text, duplicate ids
  const clipped = [...document.querySelectorAll('h1,h2,h3,h4,p,li,a,button,span,label')].filter(e =>
    vis(e) && e.scrollWidth > e.clientWidth + 2 && /(hidden|clip)/.test(getComputedStyle(e).overflowX)).map(desc);
  if (clipped.length) warn.push('clipped text: ' + clipped.slice(0, 5).join(' | '));
  const ids = {}; for (const e of document.querySelectorAll('[id]')) ids[e.id] = (ids[e.id] || 0) + 1;
  const dup = Object.keys(ids).filter(k => ids[k] > 1);
  if (dup.length) warn.push('duplicate ids: ' + dup.join(', '));

  const links = [...document.querySelectorAll('a[href]')].map(a => a.href);
  return { fail, warn, links, h1: (document.querySelector('h1') || {}).innerText || '', title: document.title,
           scrollW: de.scrollWidth, clientW: vw, height: de.scrollHeight, wa: wa.length };
}
"""

SCROLL_JS = """async () => {
  const H = () => document.documentElement.scrollHeight;
  for (let y = 0; y < H(); y += Math.max(300, innerHeight * 0.6)) { scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); }
  scrollTo(0, H()); await new Promise(r => setTimeout(r, 300));
}"""


def same_site(a, b):
    pa, pb = urlparse(a), urlparse(b)
    return (pa.scheme, pa.netloc) == (pb.scheme, pb.netloc)


def norm(u):
    u = urldefrag(u)[0]
    p = urlparse(u)
    path = p.path or "/"
    if path.endswith("/index.html"):
        path = path[: -len("index.html")]
    return p._replace(path=path, query="").geturl()


def is_page_link(u):
    p = urlparse(u)
    if p.scheme not in ("http", "https", "file"):
        return False
    ext = os.path.splitext(p.path)[1].lower()
    return ext in ("", ".html", ".htm")


def check_page(browser, url, width, args, reduced=False):
    ctx = browser.new_context(viewport={"width": width, "height": 900}, reduced_motion="reduce" if reduced else "no-preference")
    page = ctx.new_page()
    errors, console, badreq, xreq = [], [], [], []
    page.on("pageerror", lambda e: errors.append(str(e)[:200]))
    page.on("console", lambda m: console.append(m.text[:200]) if m.type == "error" else None)

    def on_failed(r):
        (badreq if same_site(r.url, url) or r.url.startswith("file:") else xreq).append(f"{r.url[-70:]} ({r.failure})")

    def on_response(r):
        if r.status >= 400:
            (badreq if same_site(r.url, url) else xreq).append(f"{r.url[-70:]} HTTP {r.status}")

    page.on("requestfailed", on_failed)
    page.on("response", on_response)
    try:
        page.goto(url, wait_until="load", timeout=30000)
    except Exception as e:  # noqa: BLE001
        ctx.close()
        return {"fail": [f"could not load: {e}"], "warn": [], "links": []}
    page.wait_for_timeout(600)
    page.evaluate(SCROLL_JS)
    page.wait_for_timeout(1300)
    page.evaluate("scrollTo(0,0)")
    page.wait_for_timeout(700)
    res = page.evaluate(CHECK_JS, {"wa": args.wa, "reveal": args.reveal})
    if errors:
        res["fail"].append("JS errors: " + " | ".join(errors[:4]))
    if console:
        res["fail"].append("console errors: " + " | ".join(console[:4]))
    if badreq:
        res["fail"].append("failed same-origin requests: " + " | ".join(sorted(set(badreq))[:6]))
    if xreq:
        res["warn"].append("failed cross-origin requests: " + " | ".join(sorted(set(xreq))[:4]))
    if args.shots and not reduced:
        slug = re.sub(r"[^a-zA-Z0-9]+", "_", urlparse(url).path.strip("/") or "home")
        page.screenshot(path=os.path.join(args.shots, f"{slug}_{width}.png"), full_page=True)
    ctx.close()
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("urls", nargs="+", help="page URLs (http://127.0.0.1:8765/) or local .html paths")
    ap.add_argument("--crawl", action="store_true", help="also check every same-site page linked from the given pages")
    ap.add_argument("--widths", default=",".join(map(str, WIDTHS)))
    ap.add_argument("--shots", default="qa_out", help="folder for full-page screenshots + qa_report.json ('' = no shots)")
    ap.add_argument("--wa", default=WA_DEFAULT, help="expected WhatsApp base link ('' disables the check)")
    ap.add_argument("--reveal", default=".rv,.reveal,[data-reveal]", help="selector of scroll-reveal elements")
    args = ap.parse_args()
    widths = [int(w) for w in args.widths.split(",") if w.strip()]
    if args.shots:
        os.makedirs(args.shots, exist_ok=True)

    start = [("file://" + os.path.abspath(u)) if os.path.exists(u) else u for u in args.urls]
    report, failing = {}, 0
    with sync_playwright() as p:
        browser = p.chromium.launch()
        queue, seen = list(start), set()
        link_status = {}
        while queue:
            url = queue.pop(0)
            key = norm(url)
            if key in seen:
                continue
            seen.add(key)
            report[key] = {}
            for w in widths:
                r = check_page(browser, url, w, args)
                report[key][w] = {"fail": r["fail"], "warn": r["warn"]}
                if w == widths[0]:
                    for link in r.get("links", []):
                        if not same_site(link, url) or not is_page_link(link):
                            continue
                        n = norm(link)
                        if n not in link_status and not link.startswith("file:"):
                            try:
                                resp = browser.new_context().request.get(urldefrag(link)[0])
                                link_status[n] = resp.status
                            except Exception as e:  # noqa: BLE001
                                link_status[n] = str(e)[:60]
                        if args.crawl and n not in seen and urldefrag(link)[0] not in queue:
                            queue.append(urldefrag(link)[0])
            # reduced-motion pass at one phone width
            rm = check_page(browser, url, 390, args, reduced=True)
            report[key]["390-reduced-motion"] = {"fail": rm["fail"], "warn": []}
        browser.close()

    broken_links = {k: v for k, v in link_status.items() if v != 200}
    print("\n=== QA report ===")
    for page_url, by_w in report.items():
        page_fails = sum(len(v["fail"]) for v in by_w.values())
        failing += page_fails
        print(f"\n{'❌' if page_fails else '✅'} {page_url}")
        for w, v in by_w.items():
            for f in v["fail"]:
                print(f"   FAIL @{w}: {f}")
        warns = {}
        for w, v in by_w.items():
            for x in v["warn"]:
                warns.setdefault(x, []).append(str(w))
        for x, ws in warns.items():
            print(f"   warn @{','.join(ws)}: {x}")
    if broken_links:
        failing += len(broken_links)
        print("\n❌ internal links that don't return 200:")
        for k, v in broken_links.items():
            print(f"   {k} -> {v}")
    print(f"\npages checked: {len(report)} · widths: {widths} · internal links checked: {len(link_status)}")
    print("RESULT:", "PASS ✅" if not failing else f"FAIL ❌ ({failing} problems)")
    if args.shots:
        with open(os.path.join(args.shots, "qa_report.json"), "w", encoding="utf-8") as f:
            json.dump({"pages": report, "links": link_status}, f, ensure_ascii=False, indent=1)
        print(f"screenshots + qa_report.json in {args.shots}/")
    sys.exit(1 if failing else 0)


if __name__ == "__main__":
    main()
