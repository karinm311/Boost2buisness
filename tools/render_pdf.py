#!/usr/bin/env python3
"""Hebrew RTL PDFs in the v6 brand, for the business-ops documents (phase 1+).

Every ops PDF (WhatsApp guide, call kit, quotes, pipeline one-pager) goes
through here, so they all share one look:
  - full Secular One / Rubik / Playpen TTFs, from the same npm cache that
    tools/subset_fonts.py uses (no subsetting: documents carry any text);
  - night/indigo header band with the logo, paper body, cyan accents;
  - "טיוטה לאישור קארין" stamp unless draft=False (only after she approves).

usage (from another tool):
    from render_pdf import page, render
    render(page(title, body_html, kicker="..."), "out.pdf")

Rendering uses the pre-installed Chromium through Node Playwright.
"""
import base64
import html
import io
import json
import os
import subprocess
import sys
import tempfile

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)
import subset_fonts  # noqa: E402

FONTS = [  # (css family, npm package, weight)
    ("Secular One", "@expo-google-fonts/secular-one", 400),
    ("Rubik", "@expo-google-fonts/rubik", 400),
    ("Rubik", "@expo-google-fonts/rubik", 700),
    ("Rubik", "@expo-google-fonts/rubik", 800),
    ("Playpen Sans Hebrew", "@expo-google-fonts/playpen-sans-hebrew", 600),
]
DRAFT = "טיוטה לאישור קארין"
WA = "054-7501261"


def esc(s):
    return html.escape(str(s), quote=False)


def font_faces():
    subset_fonts.ensure_npm(sorted({f[1] for f in FONTS}))
    out = []
    for fam, pkg, w in FONTS:
        ttf = subset_fonts.find_ttf(pkg, w)
        out.append(f'@font-face{{font-family:"{fam}";font-weight:{w};src:url("file://{ttf}") format("truetype")}}')
    return "\n".join(out)


def logo_data_uri(px=160):
    """The 458 KB logo-icon.png shrunk once, so every PDF stays small."""
    cache = os.path.join(TOOLS, ".cache", f"logo-{px}.png")
    if not os.path.exists(cache):
        from PIL import Image
        os.makedirs(os.path.dirname(cache), exist_ok=True)
        im = Image.open(os.path.join(ROOT, "brand", "logo-icon.png")).convert("RGBA")
        im.thumbnail((px, px))
        im.save(cache, optimize=True)
    return "data:image/png;base64," + base64.b64encode(open(cache, "rb").read()).decode()


CSS = r"""
@page{size:A4;margin:0}
*{box-sizing:border-box}
html,body{margin:0}
body{font-family:"Rubik",Arial,sans-serif;font-size:10.2pt;line-height:1.45;color:#14163a;direction:rtl;
  -webkit-print-color-adjust:exact;print-color-adjust:exact;background:#fff}
.sheet{width:210mm;min-height:296mm;position:relative;display:flex;flex-direction:column;page-break-after:always;overflow:hidden}
.sheet:last-child{page-break-after:auto}
.band{background:#080a24;background-image:radial-gradient(120% 140% at 0% 0%,rgba(124,58,237,.55),transparent 55%),radial-gradient(90% 120% at 100% 100%,rgba(14,165,233,.35),transparent 60%);
  color:#f5f4ff;padding:9mm 14mm 8mm;display:flex;align-items:center;gap:5mm}
.band img{width:15mm;height:15mm;border-radius:3.5mm;flex:none}
.band .bt{flex:1;min-width:0}
.band .kick{font-size:9pt;color:#a5f3fc;font-weight:700;letter-spacing:.02em}
.band h1{font-family:"Secular One","Rubik",sans-serif;font-weight:400;font-size:21pt;line-height:1.15;margin:1mm 0 0}
.band .sub{color:#d3d5f6;font-size:10pt;margin-top:1mm}
.stamp{flex:none;align-self:flex-start;border:1.4px solid #67e8f9;color:#67e8f9;border-radius:99px;padding:1mm 3.5mm;font-size:8.5pt;font-weight:700;white-space:nowrap}
.body{flex:1;padding:6mm 14mm 3mm}
.foot{padding:3mm 14mm 6mm;font-size:8pt;color:#6b6f9e;display:flex;justify-content:space-between;border-top:1px solid #e4e4f4;margin:0 14mm;padding-inline:0}
h2{font-family:"Secular One","Rubik",sans-serif;font-weight:400;font-size:13.5pt;color:#312e81;margin:3.8mm 0 1.5mm;display:flex;align-items:center;gap:2.5mm}
h2:first-child{margin-top:0}
h2 .n{display:inline-grid;place-items:center;width:6.4mm;height:6.4mm;border-radius:50%;background:#4f46e5;color:#fff;font-family:"Rubik";font-weight:800;font-size:9pt;flex:none}
h3{font-size:10.8pt;font-weight:800;margin:3mm 0 1mm;color:#1e1b4b}
p{margin:0 0 1.6mm}
ul,ol{margin:0 0 2mm;padding-inline-start:5mm}
li{margin-bottom:.8mm}
table{width:100%;border-collapse:collapse;margin:1mm 0 2.5mm;font-size:9.6pt}
table.small td,table.small th{padding:1mm 2mm;line-height:1.35}
th{background:#eef0ff;color:#312e81;font-weight:800;text-align:start;padding:1.3mm 2.2mm;border-bottom:1.5px solid #c7c9f5}
td{padding:1.3mm 2.2mm;border-bottom:1px solid #e6e7f6;vertical-align:top}
.ltr{direction:ltr;unicode-bidi:isolate}
.box{border:1px solid #dcdcf5;border-radius:3mm;padding:3mm 4mm;margin:0 0 3mm;background:#fafaff}
.box.cy{border-color:#67e8f9;background:#ecfeff}
.box.vi{border-color:#c4b5fd;background:#f5f3ff}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:3.5mm}
.grid3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:3mm}
.chip{display:inline-block;border-radius:99px;padding:.3mm 2.6mm;font-size:8.6pt;font-weight:700;background:#eef0ff;color:#3730a3;margin:0 0 1mm 1mm}
.chip.k{background:#ede9fe;color:#5b21b6}.chip.c{background:#cffafe;color:#155e75}.chip.a{background:#e0f2fe;color:#075985}
.sc{font-family:"Rubik";font-weight:800;background:#06132e;color:#67e8f9;border-radius:1.6mm;padding:.2mm 2mm;font-size:9pt;white-space:nowrap;direction:ltr;unicode-bidi:isolate}
.fill{display:inline-block;min-width:30mm;border-bottom:1px dotted #8b8fc0;color:#6b6f9e}
.line{border-bottom:1px solid #c9cbe8;height:7mm}
.hand{font-family:"Playpen Sans Hebrew","Rubik";font-weight:600;color:#6d28d9}
.muted{color:#6b6f9e}
.small{font-size:8.8pt}
.price{color:#b45309;font-weight:800}
mark{background:linear-gradient(176deg,transparent 52%,rgba(139,92,246,.35) 52%,rgba(139,92,246,.35) 90%,transparent 90%);color:inherit;padding-inline:.1em}
"""


def page(title, body, kicker="Boost2Business", sub="", draft=True, foot_note="", sheets=None):
    """One HTML document. `body` is one sheet; `sheets` (list of (title, sub, body)) makes several."""
    faces = font_faces()
    logo = logo_data_uri()
    stamp = f'<div class="stamp">{DRAFT}</div>' if draft else ""
    parts = sheets or [(title, sub, body)]
    out = []
    for i, (t, s, b) in enumerate(parts, 1):
        pg = f" · עמוד {i} מתוך {len(parts)}" if len(parts) > 1 else ""
        out.append(f"""<section class="sheet">
<header class="band"><img src="{logo}" alt=""><div class="bt"><div class="kick">{esc(kicker)}</div><h1>{esc(t)}</h1>{f'<div class="sub">{esc(s)}</div>' if s else ''}</div>{stamp}</header>
<main class="body">{b}</main>
<footer class="foot"><span>Boost2Business · קארין · <span class="ltr">{WA}</span></span><span>{esc(foot_note)}{pg}</span></footer>
</section>""")
    return f"""<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><title>{esc(title)}</title>
<style>{faces}\n{CSS}</style></head><body>{''.join(out)}</body></html>"""


NODE = r"""
const {chromium} = require('playwright');
(async () => {
  const [src, out, png] = process.argv.slice(1);
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + src, {waitUntil: 'load'});
  // load every face (unused ones stay "unloaded" otherwise), then fail on any that can't load
  const missing = await p.evaluate(async () => {
    await Promise.allSettled([...document.fonts].map(f => f.load()));
    return [...document.fonts].filter(f => f.status !== 'loaded').map(f => f.family + ' ' + f.weight);
  });
  if (missing.length) { console.error('fonts not loaded: ' + missing.join(', ')); process.exit(2); }
  await p.pdf({path: out, format: 'A4', printBackground: true, preferCSSPageSize: true});
  if (png) { await p.setViewportSize({width: 794, height: 1123}); await p.screenshot({path: png, fullPage: true}); }
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
"""


def render(doc_html, out_pdf, png=None):
    """Write `doc_html` to a temp file and print it to `out_pdf` (optionally also a full-page PNG)."""
    os.makedirs(os.path.dirname(os.path.abspath(out_pdf)), exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(doc_html)
        src = f.name
    try:
        args = ["node", "-e", NODE, src, os.path.abspath(out_pdf)] + ([os.path.abspath(png)] if png else [])
        subprocess.run(args, check=True)
    finally:
        os.unlink(src)
    return out_pdf


if __name__ == "__main__":
    # smoke test: python3 tools/render_pdf.py /tmp/x.pdf
    render(page("בדיקה", "<h2><span class='n'>1</span>שלום</h2><p>טקסט עברי עם <span class='ltr'>Boost2Business 2026</span>.</p>"),
           sys.argv[1] if len(sys.argv) > 1 else "render_test.pdf")
