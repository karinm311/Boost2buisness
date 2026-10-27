#!/usr/bin/env python3
"""Build the Netlify site (site/dist) from the artifact-flavour source (site/src).

The artifact flavour is what gets published as a claude.ai artifact:
  - The main page is a fragment: no doctype/html/head/body, plus the
    claude:viewport-fit-sides meta.
  - Fonts come from Google Fonts (the artifact CSP allows only those).
  - Extra pages (e.g. team/chani.html) are full HTML documents.

The Netlify flavour (this script's output):
  - full documents with <html lang="he" dir="rtl">, charset, viewport,
    canonical, favicon and apple-touch-icon
  - self-hosted subset woff2 fonts with preloads, no Google requests
    (tools/subset_fonts.py)
  - title overrides for SEO, og:url when missing
  - robots.txt, sitemap.xml, _headers (long cache for fonts and images),
    _redirects (pretty URLs: /team/chani serves /team/chani.html)

usage:  python3 tools/build_netlify.py [--src site/src] [--out site/dist] [--config site/site.json] [--no-fonts]
Then:   cd site/dist && zip -r ../../boost2business-site.zip . (Netlify → Deploys → drag the zip)
"""
import argparse
import json
import os
import re
import shutil
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

ASSET_EXTS = {".webp", ".avif", ".jpg", ".jpeg", ".png", ".gif", ".svg", ".ico", ".css", ".js", ".mjs",
              ".json", ".mp4", ".webm", ".pdf", ".txt", ".xml", ".webmanifest", ".woff2"}
GF_LINKS = re.compile(r'\s*<link\b[^>]*href="https://fonts\.(?:googleapis|gstatic)\.com[^"]*"[^>]*>', re.I)
CLAUDE_META = re.compile(r'\s*<meta\s+name="claude:[^"]*"[^>]*>', re.I)
HEAD_ITEM = re.compile(r'\s*(<title>.*?</title>|<meta\b[^>]*>|<link\b[^>]*>|<style\b[^>]*>.*?</style>|<base\b[^>]*>|<!--.*?-->)', re.S | re.I)


def rel_prefix(rel_path):
    depth = rel_path.count("/")
    return "../" * depth


def page_url(site_url, rel_path):
    if rel_path == "index.html":
        return site_url.rstrip("/") + "/"
    if rel_path.endswith("/index.html"):
        return site_url.rstrip("/") + "/" + rel_path[: -len("index.html")]
    return site_url.rstrip("/") + "/" + rel_path[: -len(".html")]


def font_block(config, prefix):
    lines = []
    for slug in config.get("preload_fonts", []):
        lines.append(f'<link rel="preload" href="{prefix}fonts/{slug}.woff2" as="font" type="font/woff2" crossorigin>')
    css = []
    for f in config.get("fonts", []):
        for w in f["weights"]:
            css.append(f'@font-face{{font-family:"{f["family"]}";font-weight:{w};font-style:normal;font-display:swap;'
                       f'src:url({prefix}fonts/{f["slug"]}-{w}.woff2) format("woff2")}}')
    lines.append("<style>\n" + "\n".join(css) + "\n</style>")
    return "\n".join(lines)


def head_extras(config, rel_path, html):
    prefix = rel_prefix(rel_path)
    url = page_url(config["site_url"], rel_path)
    extra = []
    if 'rel="canonical"' not in html:
        extra.append(f'<link rel="canonical" href="{url}">')
    if 'rel="icon"' not in html:
        extra.append(f'<link rel="icon" type="image/png" sizes="64x64" href="{prefix}favicon.png">')
    if 'rel="apple-touch-icon"' not in html:
        extra.append(f'<link rel="apple-touch-icon" href="{prefix}apple-touch-icon.png">')
    if 'property="og:url"' not in html:
        extra.append(f'<meta property="og:url" content="{url}">')
    return "\n".join(extra)


PAGE_HREF = re.compile(r'href="((?:\.\./)*[\w/-]*?)\.html(#[^"]*)?"')


def pretty_links(html):
    """Netlify flavour: link to clean URLs. team/chani.html -> team/chani, ../index.html#team -> ../#team."""
    def rep(m):
        path, frag = m.group(1), m.group(2) or ""
        if path == "index" or path.endswith("/index"):
            path = path[: -len("index")] or "./"
        return f'href="{path}{frag}"'
    return PAGE_HREF.sub(rep, html)


def transform(html, rel_path, config):
    prefix = rel_prefix(rel_path)
    html = pretty_links(html)
    html = CLAUDE_META.sub("", html)
    had_gf = bool(GF_LINKS.search(html))
    html = GF_LINKS.sub("", html)
    title = config.get("title_overrides", {}).get(rel_path)
    if title:
        html, n = re.subn(r"<title>.*?</title>", f"<title>{title}</title>", html, count=1, flags=re.S)
        if not n:
            html = f"<title>{title}</title>\n" + html
    fonts = font_block(config, prefix) if (had_gf or config.get("fonts")) else ""

    if re.search(r"<html\b", html, re.I):  # already a full document (extra pages)
        html = re.sub(r"<html\b[^>]*>", '<html lang="he" dir="rtl">', html, count=1, flags=re.I)
        extras = [head_extras(config, rel_path, html), fonts]
        if not re.search(r'<meta\s+name="viewport"', html, re.I):
            extras.insert(0, '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">')
        inject = "\n".join(x for x in extras if x).replace("\\", "\\\\")
        # keep <meta charset> first (it must sit in the first 1024 bytes), inject right after it
        if re.search(r"<meta\s+charset=[^>]*>", html, re.I):
            html = re.sub(r"(<meta\s+charset=[^>]*>)", r"\1\n" + inject, html, count=1, flags=re.I)
        else:
            html = re.sub(r"(<head\b[^>]*>)", r'\1\n<meta charset="utf-8">\n' + inject, html, count=1, flags=re.I)
        return html

    # fragment (artifact main page) -> full document
    pos, head = 0, []
    while True:
        m = HEAD_ITEM.match(html, pos)
        if not m:
            break
        head.append(m.group(1))
        pos = m.end()
    body = html[pos:].strip()
    head_html = "\n".join(head)
    # fonts go before the first <style> so @font-face is known early
    parts = ['<meta charset="utf-8">',
             '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">',
             head_extras(config, rel_path, html)]
    first_style = head_html.find("<style")
    if fonts and first_style >= 0:
        head_html = head_html[:first_style] + fonts + "\n" + head_html[first_style:]
    elif fonts:
        head_html += "\n" + fonts
    return ("<!doctype html>\n<html lang=\"he\" dir=\"rtl\">\n<head>\n" + "\n".join(p for p in parts if p) + "\n"
            + head_html + "\n</head>\n<body>\n" + body + "\n</body>\n</html>\n")


def make_icons(config, out):
    src = config.get("favicon_source")
    if not src:
        return
    from PIL import Image
    ic = Image.open(os.path.join(ROOT, src)).convert("RGBA")
    ic = ic.crop(ic.getbbox())
    ic.resize((64, 64), Image.LANCZOS).save(os.path.join(out, "favicon.png"))
    hexbg = config.get("icon_background", "#080a24").lstrip("#")
    bg = Image.new("RGBA", (180, 180), tuple(int(hexbg[i:i + 2], 16) for i in (0, 2, 4)) + (255,))
    bg.alpha_composite(ic.resize((150, 150), Image.LANCZOS), (15, 15))
    bg.convert("RGB").save(os.path.join(out, "apple-touch-icon.png"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=os.path.join(ROOT, "site", "src"))
    ap.add_argument("--out", default=os.path.join(ROOT, "site", "dist"))
    ap.add_argument("--config", default=os.path.join(ROOT, "site", "site.json"))
    ap.add_argument("--no-fonts", action="store_true", help="skip font subsetting (keeps existing fonts/)")
    a = ap.parse_args()
    config = json.load(open(a.config, encoding="utf-8"))
    src, out = os.path.abspath(a.src), os.path.abspath(a.out)
    if out in ("/", os.path.expanduser("~"), ROOT, src):
        sys.exit(f"refusing to use {out} as the output folder")
    old_fonts = None
    if os.path.isdir(out):
        if a.no_fonts and os.path.isdir(os.path.join(out, "fonts")):
            old_fonts = os.path.join(ROOT, "tools", ".cache", "fonts_keep")
            shutil.rmtree(old_fonts, ignore_errors=True)
            shutil.copytree(os.path.join(out, "fonts"), old_fonts)
        shutil.rmtree(out)
    os.makedirs(out)

    excluded = set(config.get("exclude", []))
    pages = []
    for dirpath, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if not d.startswith((".", "_")) and d not in excluded]
        for f in files:
            rel = os.path.relpath(os.path.join(dirpath, f), src).replace(os.sep, "/")
            if f in excluded or rel in excluded or f.startswith("_"):
                continue
            ext = os.path.splitext(f)[1].lower()
            dst = os.path.join(out, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if ext == ".html":
                html = open(os.path.join(dirpath, f), encoding="utf-8").read()
                open(dst, "w", encoding="utf-8").write(transform(html, rel, config))
                pages.append(rel)
            elif ext in ASSET_EXTS:
                shutil.copy2(os.path.join(dirpath, f), dst)

    make_icons(config, out)
    site = config["site_url"].rstrip("/")
    open(os.path.join(out, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {site}/sitemap.xml\n")
    today = date.today().isoformat()
    urls = [page_url(site, p) for p in sorted(pages) if not p.endswith("404.html")]
    open(os.path.join(out, "sitemap.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls) + "</urlset>\n")
    open(os.path.join(out, "_headers"), "w").write(
        "/fonts/*\n  Cache-Control: public, max-age=31536000, immutable\n"
        "/*.webp\n  Cache-Control: public, max-age=604800\n/*.jpg\n  Cache-Control: public, max-age=604800\n"
        "/*.png\n  Cache-Control: public, max-age=604800\n/*.svg\n  Cache-Control: public, max-age=604800\n")
    clean = [p[:-5] for p in sorted(pages) if p != "index.html" and not p.endswith("/index.html")]
    redirects = [f"/{c}/  /{c}  301" for c in clean] + [f"/{c}  /{c}.html  200" for c in clean]
    if redirects:
        open(os.path.join(out, "_redirects"), "w").write("\n".join(redirects) + "\n")

    if a.no_fonts:
        if old_fonts:
            shutil.copytree(old_fonts, os.path.join(out, "fonts"))
    elif config.get("fonts"):
        import subset_fonts
        subset_fonts.subset(out, config)

    total = 0
    print(f"\nbuilt {len(pages)} page(s) into {out}:")
    for dirpath, _, files in os.walk(out):
        for f in sorted(files):
            p = os.path.join(dirpath, f)
            s = os.path.getsize(p)
            total += s
            print(f"  {os.path.relpath(p, out):<34} {s/1024:7.1f} KB")
    print(f"  {'TOTAL':<34} {total/1024:7.1f} KB")


if __name__ == "__main__":
    main()
