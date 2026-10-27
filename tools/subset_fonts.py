#!/usr/bin/env python3
"""Self-hosted, subset Google Fonts for the Netlify build.

For each family and weight in site/site.json -> "fonts":
  1. Get the TTF from npm (@expo-google-fonts/<family>). npm works in the
     sandbox; GitHub raw downloads are blocked there.
  2. Collect every character used in the built site: html, js, json, css, svg.
     Demo scripts carry Hebrew text too, so they count.
  3. Add a safety set: Basic Latin, all Hebrew letters, ₪, quotes and dashes.
  4. Subset with pyftsubset to woff2: <out>/fonts/<slug>-<weight>.woff2
     (about 4–14 KB each instead of ~60 KB).
     A font spec with "charset": "hebrew" (a decorative font used only for
     Hebrew words) gets Hebrew letters and basic punctuation only, which is
     even smaller.

usage:  python3 tools/subset_fonts.py site/dist [--config site/site.json]
Normally called by tools/build_netlify.py. Run it on its own after you change
page text without a full rebuild.
"""
import argparse
import glob
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "tools", ".cache", "fonts")
TEXT_EXTS = (".html", ".js", ".mjs", ".json", ".css", ".svg", ".txt")
SAFETY = ("".join(chr(c) for c in range(0x20, 0x7F))
          + "".join(chr(c) for c in range(0x05D0, 0x05EB))  # Hebrew letters incl. finals
          + "׳״־" + " ₪·–—…‘’“”«»•→←↓✓×÷±%")
# "charset": "hebrew" in a font spec = a decorative font used only for Hebrew words (much smaller file)
HEBREW_ONLY = " !\"',-.?:;()←→↓" + "".join(chr(c) for c in range(0x05D0, 0x05EB)) + "׳״־ "


def ensure_tools():
    try:
        import brotli  # noqa: F401
        import fontTools  # noqa: F401
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "--break-system-packages", "fonttools", "brotli"], check=True)


def ensure_npm(packages):
    os.makedirs(CACHE, exist_ok=True)
    missing = [p for p in packages if not os.path.isdir(os.path.join(CACHE, "node_modules", p))]
    if missing:
        print("npm install", " ".join(missing))
        subprocess.run(["npm", "install", "--silent", "--no-audit", "--no-fund", "--prefix", CACHE, *missing], check=True)


def find_ttf(npm_pkg, weight):
    base = os.path.join(CACHE, "node_modules", npm_pkg)
    hits = [p for p in glob.glob(os.path.join(base, f"{weight}*", "*.ttf")) if "Italic" not in os.path.basename(p)]
    if not hits:
        raise SystemExit(f"no {weight} TTF in {npm_pkg}. Available: {sorted(os.listdir(base))}")
    return hits[0]


def used_chars(out_dir):
    chars = set(SAFETY)
    for dirpath, _, files in os.walk(out_dir):
        for f in files:
            if f.endswith(TEXT_EXTS):
                try:
                    chars |= set(open(os.path.join(dirpath, f), encoding="utf-8").read())
                except UnicodeDecodeError:
                    pass
    return "".join(sorted(c for c in chars if c.isprintable() or c == " "))


def subset(out_dir, config):
    ensure_tools()
    fonts = config.get("fonts", [])
    ensure_npm(sorted({f["npm"] for f in fonts}))
    text = used_chars(out_dir)
    fdir = os.path.join(out_dir, "fonts")
    os.makedirs(fdir, exist_ok=True)
    textfile = os.path.join(CACHE, "chars.txt")
    open(textfile, "w", encoding="utf-8").write(text)
    hebfile = os.path.join(CACHE, "chars_hebrew.txt")
    open(hebfile, "w", encoding="utf-8").write(HEBREW_ONLY)
    made = []
    for f in fonts:
        tf = hebfile if f.get("charset") == "hebrew" else textfile
        for w in f["weights"]:
            ttf = find_ttf(f["npm"], w)
            dst = os.path.join(fdir, f"{f['slug']}-{w}.woff2")
            subprocess.run([sys.executable, "-m", "fontTools.subset", ttf, f"--text-file={tf}",
                            f"--output-file={dst}", "--flavor=woff2", "--no-hinting", "--desubroutinize"], check=True)
            made.append((f["family"], w, f"fonts/{f['slug']}-{w}.woff2", os.path.getsize(dst)))
    print(f"subset {len(made)} fonts on {len(text)} characters:")
    for fam, w, path, size in made:
        print(f"  {path:<28} {fam} {w}  {size/1024:.1f} KB")
    return made


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("out", nargs="?", default=os.path.join(ROOT, "site", "dist"))
    ap.add_argument("--config", default=os.path.join(ROOT, "site", "site.json"))
    a = ap.parse_args()
    subset(a.out, json.load(open(a.config, encoding="utf-8")))
