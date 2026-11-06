#!/usr/bin/env python3
"""תיק לקוח as a branded PDF: the client's HISTORY.md (duet/scripts/client_folder.py history) → PDF.

The PDF holds personal data. Keep it in the client folder; never commit a real one.

usage:  python3 tools/client_history_pdf.py "<client folder>" [-o out.pdf]
        (regenerates HISTORY.md first, then writes <client folder>/docs/תיק-לקוח.pdf)
"""
import argparse
import html
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_pdf import ROOT, page, render  # noqa: E402
from make_quote import ltr_tokens  # noqa: E402


def inline(s):
    # escape, then **bold** and `code`, keeping Latin/digit runs LTR inside Hebrew
    parts = re.split(r"(\*\*.+?\*\*|`[^`]+`)", s)
    out = []
    for p in parts:
        if p.startswith("**") and p.endswith("**"):
            out.append(f"<b>{ltr_tokens(p[2:-2])}</b>")
        elif p.startswith("`") and p.endswith("`"):
            out.append(f'<span class="ltr small muted">{html.escape(p[1:-1])}</span>')
        else:
            out.append(ltr_tokens(p))
    return "".join(out)


def md_to_html(md):
    out, in_code, in_list, buf = [], False, False, []
    for line in md.splitlines():
        if line.startswith("```"):
            if in_code:
                out.append('<pre class="box small" style="white-space:pre-wrap;font-family:Rubik;direction:rtl">'
                           + html.escape("\n".join(buf)) + "</pre>")
                buf = []
            in_code = not in_code
            continue
        if in_code:
            buf.append(line)
            continue
        if line.startswith(("<details", "</details")):
            continue
        if in_list and not line.startswith("- "):
            out.append("</ul>")
            in_list = False
        if line.startswith("# "):
            continue  # the title goes in the band
        if line.startswith("## "):
            out.append(f"<h2>{inline(line[3:])}</h2>")
        elif line.startswith("### "):
            out.append(f'<h3 style="border-top:1px solid #e4e4f4;padding-top:2mm">{inline(line[4:])}</h3>')
        elif line.startswith("- "):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline(line[2:])}</li>")
        elif line.startswith("> "):
            out.append(f'<p class="small muted">{inline(line[2:])}</p>')
        elif line.startswith("→ "):
            out.append(f'<p class="small"><span class="chip c">{inline(line[2:])}</span></p>')
        elif line.startswith("_") and line.endswith("_"):
            out.append(f'<p class="small muted">{inline(line.strip("_"))}</p>')
        elif line.strip():
            out.append(f"<p>{inline(line)}</p>")
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()
    folder = os.path.abspath(a.folder)
    cf = os.path.join(ROOT, "duet", "scripts", "client_folder.py")
    subprocess.run([sys.executable, cf, "--root", os.path.dirname(folder), "history", os.path.basename(folder)],
                   check=True, stdout=subprocess.DEVNULL)
    md = open(os.path.join(folder, "HISTORY.md"), encoding="utf-8").read()
    title = md.splitlines()[0].lstrip("# ").strip()
    body = md_to_html(md)
    # one sheet that flows over as many A4 pages as the history needs
    doc = page(title, body, kicker="Boost2Business · תיק לקוח", sub="כל ההתקשרות, לפי הסדר",
               draft=False, foot_note="מידע אישי · לא לשיתוף")
    out = a.out or os.path.join(folder, "docs", "תיק-לקוח.pdf")
    render(doc, out)
    print(out)


if __name__ == "__main__":
    main()
