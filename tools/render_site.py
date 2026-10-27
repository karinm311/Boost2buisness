#!/usr/bin/env python3
"""Render the v6 site (artifact flavour) into site/src from one source of truth.

Inputs:  site/src/data/agents.json, site/src/data/offer.json,
         site/templates/site.css, site/templates/site.js, tools/characters.py
Outputs: site/src/index.html            (artifact main page: a fragment, Google Fonts)
         site/src/team/<slug>.html      (full documents)
         site/src/training.html         (full document)
         site/src/og*.jpg               (1200x627 link previews, with --og)

Then:    python3 tools/build_netlify.py  (site/src → site/dist, self-hosted subset fonts, pretty URLs)

usage:   python3 tools/render_site.py [--og]
"""
import argparse
import html
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import characters  # noqa: E402

SRC = os.path.join(ROOT, "site", "src")
TPL = os.path.join(ROOT, "site", "templates")
SITE = "https://boost2business.netlify.app"
GF = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
      '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
      '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playpen+Sans+Hebrew:wght@600&family=Rubik:wght@400;700;800&family=Secular+One&display=swap">')

DATA = json.load(open(os.path.join(SRC, "data", "agents.json"), encoding="utf-8"))
OFFER = json.load(open(os.path.join(SRC, "data", "offer.json"), encoding="utf-8"))
AG = DATA["agents"]
BY = {a["slug"]: a for a in AG}
CSS = open(os.path.join(TPL, "site.css"), encoding="utf-8").read()
JS = open(os.path.join(TPL, "site.js"), encoding="utf-8").read()
WA = OFFER["wa"]

ICONS = """<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7c3aed"/><stop offset=".6" stop-color="#4f46e5"/><stop offset="1" stop-color="#0ea5e9"/></linearGradient>
<symbol id="mark" viewBox="0 0 120 120"><rect width="120" height="120" rx="32" fill="url(#bg)"/><g fill="none" stroke="#fff" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"><path d="M42 32 V88"/><path d="M42 32 H64 a14 14 0 0 1 0 28 H42"/><path d="M42 60 H68 a14 14 0 0 1 0 28 H42"/></g><circle cx="42" cy="32" r="7" fill="#fff"/><circle cx="42" cy="88" r="7" fill="#fff"/><circle cx="42" cy="60" r="5" fill="#080a24" stroke="#fff" stroke-width="3"/><path d="M94 14 L97 23 L106 26 L97 29 L94 38 L91 29 L82 26 L91 23 Z" fill="#67e8f9"/></symbol>
<symbol id="wa" viewBox="0 0 24 24"><path fill="currentColor" d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.21c5.46 0 9.91-4.45 9.91-9.91S17.5 2 12.04 2zm0 18.15c-1.48 0-2.93-.4-4.2-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.23 8.23 0 0 1-1.26-4.38c0-4.54 3.7-8.24 8.25-8.24 4.54 0 8.24 3.7 8.24 8.24 0 4.55-3.7 8.24-8.24 8.24zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.13-.16.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.12-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.02-.38.11-.51.11-.11.25-.29.37-.43.13-.15.17-.25.25-.42.08-.16.04-.31-.02-.43-.06-.12-.56-1.34-.76-1.84-.2-.48-.41-.42-.56-.43h-.48c-.17 0-.43.06-.66.31-.22.25-.86.85-.86 2.07 0 1.22.89 2.4 1.01 2.56.12.17 1.75 2.67 4.23 3.74.59.26 1.05.41 1.41.52.59.19 1.13.16 1.56.1.48-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.14-1.18-.06-.1-.22-.16-.47-.28z"/></symbol>
<symbol id="check" viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5"/></symbol>
<symbol id="plus" viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></symbol>"""


def e(s):
    return html.escape(s, quote=True)


def ch(slug, label=None, cls="chr", bob=None):
    """An inline character. label=None → decorative (aria-hidden)."""
    a = f'role="img" aria-label="{e(label)}"' if label else 'aria-hidden="true" focusable="false"'
    style = f' style="--bd:{bob}s"' if bob is not None else ""
    c = cls + (" bob" if bob is not None else "")
    return f'<svg class="{c}" viewBox="0 0 200 204" {a}{style}><use href="#ch-{slug}"/></svg>'


def wa_link(text=None):
    # plain link by default (Karin's v5 decision); prefilled text only when she sets wa_text in agents.json
    if not text:
        return WA
    from urllib.parse import quote
    return WA + "?text=" + quote(text)


def cta(label, small="30 דקות · קובעים בוואטסאפ", where="hero", href=None, pulse=False, id_=None):
    cls = "cta" + (" pulse" if pulse else "")
    i = f' id="{id_}"' if id_ else ""
    return (f'<a class="{cls}" data-cta="{where}" href="{e(href or WA)}" target="_blank" rel="noopener"{i}>'
            f'<span class="ring" aria-hidden="true"><svg><use href="#wa"/></svg></span>'
            f'<span class="t">{label}<small>{small}</small></span></a>')


def defs():
    return (f'<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>{ICONS}'
            f'{characters.symbols()}</defs></svg>')


def nav(home, prefix):
    home_href = "#top" if home else f"{prefix}index.html"
    t = "#" if home else f"{prefix}index.html#"
    return f"""<nav class="nav" aria-label="ראשי">
  <div class="wrap">
    <a class="brand" href="{home_href}" title="לדף הבית">
      <svg aria-hidden="true"><use href="#mark"/></svg>
      <div><div class="bt">Boost<span>2Business</span></div><div class="bs">B2B · AI SOLUTIONS</div></div>
    </a>
    <div class="links">
      <a class="nl" href="{t}paths">מה אני עושה</a>
      <a class="nl" href="{t}team">הצוות</a>
      <a class="nl" href="{t}offer">איך מתחילים</a>
      <a class="cta-sm" data-cta="nav" href="{WA}" target="_blank" rel="noopener" aria-label="שיחת אפיון חינם"><svg aria-hidden="true"><use href="#wa"/></svg><span class="lbl">שיחת אפיון חינם</span></a>
    </div>
  </div>
</nav>"""


def footer(prefix):
    links = " · ".join(f'<a href="{prefix}team/{a["slug"]}.html">{a["first"]}</a>' for a in AG)
    return f"""<footer>
  <div class="wrap">
    <span class="ltr" style="font-weight:700">Boost<span style="font-weight:400">2Business</span></span>
    <span><a href="{prefix}solutions.html">פתרונות למשרדים</a> · {links} · <a href="{prefix}training.html">למידה</a></span>
    <span>קארין · <span class="ltr">{OFFER["phone"]}</span></span>
  </div>
</footer>"""


def bar(label="אני רוצה שיחת אפיון חינם", href=None):
    return f'<div class="bar off" id="bar">{cta(label, where="bar", href=href)}</div>'


def final(title, line, label="אני רוצה שיחת אפיון חינם", href=None):
    team = "".join(ch(a["slug"], bob=i * .4) for i, a in enumerate(AG))
    return f"""<section class="s final" id="contact" aria-labelledby="final-h">
  <div class="wrap">
    <div class="box rv">
      <div class="team">{team}</div>
      <h2 id="final-h">{title}</h2>
      <p>{line}</p>
      <ul class="promise">
        <li><svg aria-hidden="true"><use href="#check"/></svg>30 דקות</li>
        <li><svg aria-hidden="true"><use href="#check"/></svg>חינם</li>
        <li><svg aria-hidden="true"><use href="#check"/></svg>בלי התחייבות</li>
        <li><svg aria-hidden="true"><use href="#check"/></svg>הטבת השקה ללקוחות חדשים</li>
      </ul>
      {cta(label, where="final", href=href, id_="final-cta")}
      <div class="phone">או בטלפון: <a href="tel:{OFFER["phone_tel"]}" id="phone" data-cta="phone">{OFFER["phone"]}</a><button class="copy" id="copyBtn" type="button" data-copy="{OFFER["phone"].replace("-", "")}" >העתקה</button><span class="vh" id="copyMsg" role="status"></span></div>
    </div>
  </div>
</section>""".replace("אפיون", "אפיון")


def demo_box(slug, title, sub, acc, ink, hidden=False, id_=None, label=None):
    av = ch("karin" if slug in ("training", "office") else slug)
    hid = " hidden" if hidden else ""
    i = id_ or f"demo-{slug}"
    lab = f' role="tabpanel" aria-labelledby="{label}"' if label else ""
    return f"""<div class="demo" id="{i}" data-demo="{slug}" style="--a:{acc};--ink:{ink}"{lab}{hid}>
  <div class="dtop"><span class="av">{av}</span><div><h3>{title}</h3><div class="sub">{sub}</div></div><span class="dbadge">הדגמה · נתונים לדוגמה</span></div>
  <div class="dctl"><p class="dstatus" aria-live="polite"></p><span class="dsteps" aria-hidden="true"><i></i><i></i><i></i></span></div>
  <div class="dstage"></div>
  <div class="dctl"><button class="dbtn ghost restart" type="button">↺ מהתחלה</button></div>
</div>"""


DEMO_SUB = {
    "chani": "בוחרים חשבונית, חני קוראת אותה, ואתם מאשרים.",
    "dana": "דנה בודקת את ההוצאות ומוצאת חריגה.",
    "shira": "לקוחה כותבת בחצות. שירה עונה.",
    "noga": "דייר מדווח על תקלה. נגה דואגת שתיסגר.",
    "gal": "הזמנה הופכת לחשבונית ולתזכורת, בלי הקלדה.",
    "training": "אותה משימה: לפני ההדרכה ואחריה.",
    "office": "בחרו סוג משרד, ותראו מה אפשר להעביר לסוכנים.",
}


def page_doc(title, desc, og_title, og_img, url, body, fragment):
    head = f"""<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="he_IL">
<meta property="og:site_name" content="Boost2Business">
<meta property="og:title" content="{e(og_title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="627">
<meta property="og:image:alt" content="{e(og_title)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#080a24">
{GF}
<style>
{CSS}</style>"""
    js = '<script>try{if(!matchMedia("(prefers-reduced-motion: reduce)").matches&&"IntersectionObserver" in window)document.documentElement.classList.add("js")}catch(e){}</script>'
    tail = f"<script>\n{JS}</script>"
    if fragment:
        return (head.replace("<title>", '<title>', 1) + '\n<meta name="claude:viewport-fit-sides" content="cover">\n'
                + defs() + "\n" + js + "\n" + body + "\n" + tail + "\n")
    return ('<!doctype html>\n<html lang="he" dir="rtl">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + head + "\n</head>\n<body>\n" + defs() + "\n" + js + "\n" + body + "\n" + tail + "\n</body>\n</html>\n")


# ---------------------------------------------------------------- HOME
def home():
    agents_strip = "".join(ch(a["slug"]) for a in AG)
    pos = {"chani": (7, 22), "dana": (39, 0), "shira": (71, 22), "noga": (71, 55), "gal": (49, 70)}
    pops = {"chani": "🧾 חשבונית חדשה מחכה לאישור שלכם", "dana": "📊 מצאתי חריגה בהוצאות הדלק",
            "shira": "💬 עניתי ללקוחה ב-<span class=\"ltr\">23:41</span>", "noga": "🔧 שובץ ספק לדירה 4",
            "gal": "🔗 ההזמנה הפכה לחשבונית"}
    scene_agents = "".join(
        f'<a class="ag" href="team/{a["slug"]}.html" style="left:{pos[a["slug"]][0]}%;top:{pos[a["slug"]][1]}%" title="{e(a["name"])}">'
        f'{ch(a["slug"], bob=i * .6)}<span class="nm">{a["name"]}</span></a>' for i, a in enumerate(AG))
    scene_pops = "".join(f'<span class="pop" style="--pd:{i * 2.4}s;grid-area:1/1">{pops[a["slug"]]}</span>' for i, a in enumerate(AG))
    chair = """<svg viewBox="0 0 200 190" aria-hidden="true" focusable="false" class="chr">
<g stroke="#1b1446" stroke-width="5" stroke-linejoin="round" stroke-linecap="round">
<path d="M84 8 l12 16 l4 -20 l4 20 l12 -16 l-2 24 h-28z" fill="#fde047"/>
<rect x="46" y="34" width="108" height="92" rx="34" fill="#7c3aed"/>
<rect x="62" y="48" width="76" height="66" rx="24" fill="#8b5cf6"/>
<rect x="34" y="104" width="132" height="34" rx="16" fill="#6d28d9"/>
<rect x="24" y="82" width="28" height="60" rx="14" fill="#5b21b6"/><rect x="148" y="82" width="28" height="60" rx="14" fill="#5b21b6"/>
<path d="M100 138 v26 M70 176 h60 M100 164 l-26 12 M100 164 l26 12" fill="none"/>
</g><circle cx="100" cy="80" r="10" fill="#fde047" stroke="#1b1446" stroke-width="4"/></svg>"""
    tabs = "".join(
        f'<button type="button" role="tab" id="tab-{a["slug"]}" aria-controls="demo-{a["slug"]}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}" class="tab" style="--a:{a["acc"]}">'
        f'{ch(a["slug"])}<span>{a["first"]}</span></button>' for i, a in enumerate(AG))
    panels = "".join(demo_box(a["slug"], f'{a["name"]} בעבודה', DEMO_SUB[a["slug"]], a["acc"], a["acc_ink"],
                              hidden=i > 0, label=f'tab-{a["slug"]}') for i, a in enumerate(AG))
    cards = []
    for i, a in enumerate(AG):
        big = " big" if i < 2 else ""
        verb = "לוקח" if a["g"] == "m" else "לוקחת"
        cards.append(f"""<a class="tc rv{big}" href="team/{a["slug"]}.html" style="--a:{a["acc"]}">
  <span class="pic">{ch(a["slug"], bob=i * .5)}</span>
  <div><h3>{a["name"]} <span class="em" aria-hidden="true">{a["emoji"]}</span></h3><p>{a["role"]}</p>
  <span class="takes"><b>מה {"הוא" if a["g"] == "m" else "היא"} {verb} מכם</b>{a["takes"]}</span>
  <span class="go">לעמוד של {a["first"]} ←</span></div>
</a>""")
    kc = f"""<div class="tc kc rv">
  <span class="pic">{ch("karin", "קארין, מאוירת", bob=.3)}</span>
  <div><h3>ואתם? <mark>המנהלים</mark>.</h3><p>הסוכנים עושים את העבודה, מדווחים, ומחכים לאישור שלכם בנקודות הרגישות. קארין בונה אותם, מחברת אותם למערכות שלכם ונשארת איתכם. יד ביד.</p></div>
  <a class="cta-sm" data-cta="team" href="{WA}" target="_blank" rel="noopener"><svg aria-hidden="true"><use href="#wa"/></svg>אני רוצה צוות כזה</a>
</div>"""
    day = [("07:30", "📱", "עונים ללקוחות בוואטסאפ, עוד לפני הקפה", "☕", "קוראים סיכום בוקר קצר מדנה"),
           ("10:00", "⌨️", "מקלידים חשבוניות, אחת־אחת", "✅", "מאשרים חשבוניות שחני כבר קראה"),
           ("13:00", "📋", "מעתיקים הזמנות מהטופס לאקסל", "🤝", "פגישה עם לקוח חדש"),
           ("16:00", "📞", "רודפים אחרי ספק בגלל נזילה", "👍", "נגה שיבצה ספק. אתם מאשרים בלחיצה"),
           ("20:00", "😩", "מנסים להבין לאן הלך הכסף החודש", "🏡", "ערב עם המשפחה"),
           ("23:00", "💬", "עוד עונים ללקוחות", "😴", "שירה עונה. אתם ישנים")]
    day_html = '<span></span><div class="lh no">😓 בלי צוות</div><div class="lh yes">😎 עם הצוות</div>'
    for t, e1, a1, e2, a2 in day:
        day_html += (f'<div class="t">{t}</div><div class="c no-c rv"><span><span class="e" aria-hidden="true">{e1}</span>{a1}</span></div>'
                     f'<div class="c yes-c rv"><span><span class="e" aria-hidden="true">{e2}</span>{a2}</span></div>')
    agents_row = "".join(ch(a["slug"]) for a in AG)
    body = f"""<a class="skip" href="#main">דילוג לתוכן</a>
{nav(True, "")}
<main id="main">
<header class="hero" id="top">
  <div class="wrap">
    <div class="htext">
      <div class="strip"><span class="faces">{agents_strip}</span><span>חני, דנה, שירה, נגה וגל מחכים לכם</span></div>
      <h1><span class="l">אתם <u>תנהלו</u>.</span> <span class="l">הסוכנים שלכם <mark>יעבדו בשבילכם</mark>.</span></h1>
      <p class="lead">צוות של סוכני <span class="ltr">AI</span> עושה את ההקלדות, המענה ללקוחות וההעתקות, <b>ומחכה לאישור שלכם רק במה שחשוב</b>. זה נשמע רחוק, אבל זה אפשרי. יד&nbsp;ביד.</p>
      <div class="cta-row">{cta("אני רוצה שיחת אפיון חינם", pulse=True)}<a class="link2" href="#team">הכירו את הצוות ←</a></div>
      <ul class="trust">
        <li><svg aria-hidden="true"><use href="#check"/></svg>חינם ובלי התחייבות</li>
        <li><svg aria-hidden="true"><use href="#check"/></svg>הטבת השקה ללקוחות חדשים</li>
        <li><svg aria-hidden="true"><use href="#check"/></svg>בעברית או באנגלית</li>
      </ul>
    </div>
    <div class="scene" role="group" aria-label="איור: אתם בכיסא של המנהלים, והסוכנים סביבכם">
      <div class="glow" aria-hidden="true"></div><div class="orbit" aria-hidden="true"></div>
      <div class="chair">{chair}<span class="you">אתם 👑</span></div>
      {scene_agents}
      <div style="position:absolute;left:14%;right:14%;top:47%;display:grid;justify-items:center" aria-hidden="true">{scene_pops}</div>
      <div class="karin" style="left:3%;top:60%;width:27%">{ch("karin", "קארין, בונה את הצוות", bob=1.1)}<span class="note hand" style="left:-2%;top:-14%">זאת אני! ↓</span></div>
      <span class="cap">המחשה · נתונים לדוגמה</span>
    </div>
  </div>
</header>

{paths_section("")}

<section class="s" id="pains" aria-labelledby="pains-h" style="padding-top:24px">
  <div class="wrap">
    <div class="head center rv"><div class="eyebrow">נשמע מוכר?</div><h2 id="pains-h">ה-<span class="ltr">AI</span> כבר אצלכם בטלפון. <mark>העבודה</mark> עדיין אצלכם על הראש.</h2></div>
    <div class="bubbles">
      <p class="bub rv">״<span class="ltr">ChatGPT</span> כותב לי יפה, אבל העבודה עדיין עליי.״<span class="who">— נשמע מוכר?</span></p>
      <p class="bub rv">״החשבוניות מחכות לסוף החודש.״<span class="who">— ואז כל הסופ״ש הולך</span></p>
      <p class="bub rv">״אני עונה ללקוחות עד חצות.״<span class="who">— ובבוקר מתחילים מחדש</span></p>
    </div>
    <p class="punch rv">שיחה עם <span class="ltr">AI</span> <span class="neq" role="img" aria-label="לא שווה">≠</span> <u>עובד</u></p>
    <p class="punch-sub rv">בלי קורסים ובלי סרטונים. אתם צריכים מישהו שיבין מה קורה אצלכם ומה העסק שלכם צריך. לא סיסמאות.</p>
  </div>
</section>

<section class="s" id="team" aria-labelledby="team-h" style="padding-top:24px">
  <div class="wrap">
    <div class="head rv"><div class="eyebrow">הכירו את הצוות שלכם</div><h2 id="team-h">חמישה סוכנים. <mark>תפקיד אחד</mark> לכל אחד.</h2><p class="intro">כל סוכן עושה עבודה אחת, טוב. לחצו על מי שנראה לכם הכי דחוף.</p></div>
    <div class="bento">{"".join(cards)}{kc}</div>
  </div>
</section>

<section class="s" id="demos" aria-labelledby="demos-h" style="padding-top:24px">
  <div class="wrap">
    <div class="head center rv"><div class="eyebrow">תראו אותם עובדים</div><h2 id="demos-h">לחצו. <u>נסו</u>. אתם המנהלים.</h2><p class="intro">הדגמות קצרות עם נתונים לדוגמה. בכל אחת יש רגע שבו הסוכן עוצר ומחכה לכם.</p></div>
    <div class="tabs" role="tablist" aria-label="בחרו סוכן להדגמה">{tabs}</div>
    {panels}
  </div>
</section>

<section class="s" id="day" aria-labelledby="day-h" style="padding-top:24px">
  <div class="wrap">
    <div class="head center rv"><div class="eyebrow">היום שלכם — בלי ועם</div><h2 id="day-h">אותו יום. <mark>חיים אחרים</mark>.</h2></div>
    <div class="day" role="group" aria-label="יום עבודה בלי צוות ועם צוות">{day_html}</div>
    <p class="day-note">תרחיש להמחשה. היום שלכם ייראה אחרת, ובשביל זה יש שיחת אפיון.</p>
  </div>
</section>

<section class="s" id="how" aria-labelledby="how-h" style="padding-top:24px">
  <div class="wrap">
    <div class="head center rv"><div class="eyebrow">איך זה עובד</div><h2 id="how-h">שלושה צעדים. <mark>בלי הפתעות</mark>.</h2></div>
    <div class="how">
      <div class="st rv"><span class="n ltr" aria-hidden="true">1</span><h3>שיחת אפיון <span class="free">חינם</span></h3><p>30 דקות, בלי התחייבות. מבינים יחד איפה הזמן שלכם הולך לאיבוד ואיזה סוכן הכי שווה להתחיל איתו.</p></div>
      <div class="st rv"><span class="n ltr" aria-hidden="true">2</span><h3>אני בונה ומחברת</h3><p>בונה את הסוכנים, מלמדת אותם את העסק שלכם ומחברת אותם למערכות שכבר יש לכם.</p></div>
      <div class="st rv"><span class="n ltr" aria-hidden="true">3</span><h3>הסוכנים עובדים. אתם מאשרים.</h3><p>הם עושים את העבודה ומדווחים. בנקודות הרגישות הם עוצרים ומחכים לכם. ואם משהו משתנה, הפתרון גדל איתכם.</p></div>
    </div>
    <div class="hitl rv" role="group" aria-labelledby="hitl-h">
      <h3 id="hitl-h">מי עושה מה?</h3>
      <div class="tier"><span class="owner" aria-hidden="true">👑</span><span class="lbl"><b>אתם מחליטים</b>מאשרים בלחיצה, רק במה שחשוב</span></div>
      <div class="arrows" aria-hidden="true"><span class="up">↑ מדווחים ומחכים לאישור</span><span class="down">↓ מאשרים ✅</span></div>
      <div class="tier"><div class="agents-row">{agents_row}</div><span class="lbl"><b>הסוכנים עושים</b>מקלידים, עונים, מעתיקים, עוקבים</span></div>
      <div class="builder">{ch("karin")}<span><b>קארין בונה ומלווה</b><br>מאפיינת, בונה, מחברת, ונשארת איתכם</span></div>
    </div>
  </div>
</section>

<section class="s" id="calc-s" aria-labelledby="calc-h" style="padding-top:24px">
  <div class="wrap">
    <div class="head center rv"><div class="eyebrow">מחשבון</div><h2 id="calc-h">כמה שעות בשבוע <u>הולכות</u> לכם על…</h2><p class="intro">הזיזו את הסליידרים. זו הערכה שלכם, על העסק שלכם.</p></div>
    <form class="calc rv" id="calc" onsubmit="return false">
      <div class="in">
        <div class="rg"><label for="r1"><span>הקלדת חשבוניות ומסמכים</span><output for="r1">4 ש׳</output></label><input type="range" id="r1" min="0" max="20" step="1" value="4"></div>
        <div class="rg"><label for="r2"><span>מענה לאותן שאלות של לקוחות</span><output for="r2">5 ש׳</output></label><input type="range" id="r2" min="0" max="20" step="1" value="5"></div>
        <div class="rg"><label for="r3"><span>העתקות בין מערכות ואקסלים</span><output for="r3">3 ש׳</output></label><input type="range" id="r3" min="0" max="20" step="1" value="3"></div>
        <div class="rg"><label for="rate"><span>כמה שווה לכם שעה?</span><output for="rate">₪150</output></label><input type="range" id="rate" min="50" max="500" step="10" value="150"></div>
      </div>
      <div class="out">
        <span>בחודש זה בערך</span>
        <span class="big" aria-live="polite"><span id="c-hours" class="ltr">52</span> <small>שעות</small></span>
        <span class="money" aria-live="polite">ששוות <span id="c-money" class="ltr">₪7,800</span></span>
        <span class="est">הערכה לפי מה שהזנתם (שעות בשבוע × 52 ÷ 12). לא הבטחה לחיסכון.</span>
        {cta("אני רוצה את השעות האלה בחזרה", "שיחת אפיון חינם · 30 דקות", where="calc")}
      </div>
    </form>
  </div>
</section>

<section class="s founder" id="about" aria-labelledby="about-h" style="padding-top:24px">
  <div class="wrap">
    <div class="pic rv"><picture><source type="image/webp" srcset="karin-480.webp 480w, karin-640.webp 640w, karin-800.webp 800w" sizes="(max-width: 640px) 230px, (max-width: 960px) 300px, 380px"><img src="karin-640.jpg" srcset="karin-480.jpg 480w, karin-640.jpg 640w, karin-800.jpg 800w" sizes="(max-width: 640px) 230px, (max-width: 960px) 300px, 380px" width="640" height="800" alt="קארין, המייסדת של Boost2Business" loading="lazy" decoding="async"></picture><span class="toon">{ch("karin")}</span><span class="hand">בונה לכם. מלמדת אתכם.</span></div>
    <div class="rv">
      <div class="eyebrow">מי בונה לכם את הצוות?</div>
      <h2 id="about-h">קודם אני מבינה את <mark>העסק</mark>. אחר כך בונה.</h2>
      <div class="txt">
        <p>אני קארין. מ-<span class="ltr">2011</span> אני בונה <b>פתרונות מערכות בהייטק</b>: מערכות <span class="ltr">ERP</span> ו-<span class="ltr">CRM</span>, תהליכים מהזמנה ועד גבייה ואינטגרציות. ראיתי מקרוב איך כסף, מסמכים ונתונים זזים בארגון, ואיפה הם נתקעים.</p>
        <p>בשנים האחרונות <b>פרצתי לעולם ה-<span class="ltr">AI</span></b>, והיום אני גם מלמדת אחרים לעבוד איתו.</p>
        <p class="quote">הפכתי את התחביב למוצר.</p>
      </div>
      <div class="chips"><b>כבר בניתי:</b><span>קורא חשבוניות</span><span>דשבורדים פיננסיים עם זיהוי חריגות</span><span>צ׳אטבוט</span><span>מערכת לניהול נכסים וקריאות שירות</span></div>
      <p class="cred">אנליסטית מערכות בכירה · הנדסת תעשייה וניהול (מערכות מידע) · מוסמכת&nbsp;<span class="ltr">NLP</span> (תכנות נוירו־לשוני) · עובדת עם <span class="ltr">n8n</span>, <span class="ltr">Power Automate</span>, <span class="ltr">Salesforce</span>, <span class="ltr">Oracle</span> ו-<span class="ltr">ServiceNow</span></p>
    </div>
  </div>
</section>

{offer_block("")}

{faq()}

{final("אתם <u>תנהלו</u>. הצוות ידאג <mark>לשאר</mark>.", "חצי שעה של שיחה, ואתם יוצאים עם תמונה ברורה: מה הכי שווה להעביר לסוכנים, ובאיזה סוכן מתחילים.")}
</main>
{footer("")}
{bar()}"""
    return page_doc("Boost2Business · אתם תנהלו. הסוכנים שלכם יעבדו בשבילכם.",
                    "צוות של סוכני AI לעסקים קטנים: קוראים חשבוניות, עונים ללקוחות, מנהלים קריאות שירות ומחברים מערכות. אתם רק מאשרים. שיחת אפיון של 30 דקות, חינם.",
                    "אתם תנהלו. הסוכנים שלכם יעבדו | Boost2Business", "og.jpg", SITE + "/", body, True)


def paths_section(prefix):
    faces = "".join(ch(a["slug"]) for a in AG)
    items = [
        ("sol", "#67e8f9", "🏢", "פתרונות AI למשרדים ולבעלי עסקים",
         "אני בונה פתרון לפי התהליך שלכם: אוטומציה, חיבור בין מערכות וסוכנים.",
         ["יש לכם תהליך שחוזר כל יום", "המערכות שלכם לא מדברות זו עם זו"],
         "תהליך שרץ לבד, ואתם מאשרים בנקודות הרגישות",
         '<span class="mini-flow" aria-hidden="true"><span>📥</span><i>←</i><span>⚙️</span><i>←</i><span>✅</span></span>',
         f"{prefix}solutions.html", "לפתרונות למשרדים"),
        ("team", "#c4b5fd", "🤖", "צוות סוכנים",
         "חני, דנה, שירה, נגה וגל. כל אחד עושה עבודה אחת, טוב.",
         ["אתם רוצים להתחיל ממשימה אחת ברורה", "אתם עונים, מקלידים ומעתיקים בעצמכם"],
         "עובד דיגיטלי שמדווח ומחכה לאישור שלכם",
         f'<span class="faces" aria-hidden="true">{faces}</span>',
         "#team", "להכיר את הצוות"),
        ("learn", "#fbbf24", "🎓", 'למידה <span class="ltr">1:1</span> ובקבוצות',
         "הדרכה מעשית, בעברית או באנגלית, על המשימות האמיתיות שלכם.",
         ["אתם רוצים לעבוד עם AI בעצמכם", "יש לכם צוות שצריך שפה משותפת"],
         "דרך עבודה קבועה שנשארת אצלכם",
         '<span class="pills" aria-hidden="true"><b class="ltr">1:1</b><b class="ltr">1:n</b></span>',
         f"{prefix}training.html", "ללמידה"),
    ]
    cards = []
    for i, (k, acc, ic, h, d, fit, gain, art, href, go) in enumerate(items):
        fits = "".join(f'<li><svg aria-hidden="true"><use href="#check"/></svg><span>{x}</span></li>' for x in fit)
        cards.append(f"""<article class="path rv" id="path-{k}" style="--a:{acc}">
  <span class="ptop"><span class="pi" aria-hidden="true">{ic}</span><span class="pn ltr" aria-hidden="true">0{i + 1}</span></span>
  <h3>{h}</h3>
  <p>{d}</p>
  {art}
  <div class="fit"><b>מתאים לכם אם…</b><ul>{fits}</ul></div>
  <div class="gain"><b>מה יוצא לכם</b>{gain}</div>
  <a class="go" href="{href}">{go} <span class="ltr" aria-hidden="true">←</span></a>
</article>""")
    return f"""<section class="s" id="paths" aria-labelledby="paths-h" style="padding-top:40px">
  <div class="wrap">
    <div class="head center rv"><div class="eyebrow">מה אני עושה</div><h2 id="paths-h">שלוש דרכים <mark>לעבוד איתי</mark>.</h2><p class="intro">מתחילים ממה שהכי בוער לכם. אפשר גם לשלב.</p></div>
    <nav class="pidx rv" aria-label="שלוש הדרכים"><a href="#path-sol" style="--a:#67e8f9"><span aria-hidden="true">🏢</span> פתרונות למשרדים</a><a href="#path-team" style="--a:#c4b5fd"><span aria-hidden="true">🤖</span> צוות סוכנים</a><a href="#path-learn" style="--a:#fbbf24"><span aria-hidden="true">🎓</span> למידה <span class="ltr">1:1</span> ובקבוצות</a></nav>
    <div class="branch" aria-hidden="true"><span class="q">מה העסק שלכם צריך?</span><svg viewBox="0 0 300 44" preserveAspectRatio="none"><path d="M150 0 V22 M150 22 H50 V44 M150 22 V44 M150 22 H250 V44"/></svg></div>
    <div class="paths">{"".join(cards)}</div>
    <p class="paths-foot rv">לא בטוחים מה מתאים? <a class="link2" href="#offer">בשביל זה יש שיחת אפיון חינם <span class="ltr" aria-hidden="true">←</span></a></p>
  </div>
</section>"""


def solutions_page():
    p = ""
    want = "אני רוצה פתרון לעסק שלי"
    sectors = [("🧮", "משרדי רואי חשבון"), ("⚖️", "משרדי עורכי דין"), ("🏢", "חברות לניהול נכסים"), ("🛡️", "סוכנויות ביטוח"), ("🏪", "עסקים קטנים בכל תחום")]
    sect = "".join(f'<span><span aria-hidden="true">{a}</span> {b}</span>' for a, b in sectors)
    pillars = [("🔁", "אוטומציית תהליכים", "ממפים את התהליך מקצה לקצה ובונים תהליך שרץ לבד: קליטה, עיבוד, אישורים והפצה."),
               ("🔗", "חיבור בין מערכות", 'מחברים בין מערכות ה-<span class="ltr">ERP</span> וה-<span class="ltr">CRM</span> לאקסלים ולמייל, כך שהנתונים עוברים לבד.'),
               ("🤖", 'סוכני <span class="ltr">AI</span>', "סוכן שקורא מסמכים, מזהה חריגות ומחכה לאישור שלכם בנקודות הרגישות. אתם נשארים בשליטה.")]
    pil = "".join(f'<div class="st rv"><span class="n" aria-hidden="true">{a}</span><h3>{b}</h3><p>{c}</p></div>' for a, b, c in pillars)
    steps = [("💬", "שיחת אפיון", "30 דקות, חינם, בלי התחייבות"), ("📝", "הצעה מותאמת", "מה נבנה, איך זה ישתלב, ובכמה"),
             ("🛠️", "בנייה וחיבור", "עם אישור אנושי בנקודות הרגישות"), ("🤝", "ליווי עד שזה עובד", "וכשמשהו משתנה, הפתרון גדל איתכם")]
    dn = "".join(f'<div role="listitem" class="dn rv"><span class="c" aria-hidden="true">{ic}</span><b>{a}</b><small>{b}</small></div>' for ic, a, b in steps)
    allteam = "".join(f'<a href="team/{x["slug"]}.html" style="--a:{x["acc"]}">{ch(x["slug"])}{x["first"]}</a>' for x in AG)
    allteam += f'<a href="training.html">{ch("karin")}למידה</a>'
    body = f"""<a class="skip" href="#main">דילוג לתוכן</a>
{nav(False, p)}
<main id="main" style="--a:#67e8f9;--ink:#06132e">
<header class="ahero" id="top">
  <div class="wrap">
    <div class="htext">
      <div class="crumb"><span class="mini">{ch("karin", bob=0)}</span><span><a href="index.html#paths">מה אני עושה</a> · <span class="role">🏢 פתרונות למשרדים ולעסקים</span></span></div>
      <h1>פתרון <span class="ltr">AI</span> שבנוי <u>בדיוק</u> <mark>לעסק שלכם</mark>.</h1>
      <p class="lead">מבזבזים שעות על הקלדות, העתקות ומערכות שלא מדברות זו עם זו? אני מחברת בין המערכות, בונה אוטומציה לתהליכים ומוסיפה <span class="ltr">AI</span> רק איפה שצריך.</p>
      <div class="cta-row">{cta(want, "שיחת אפיון חינם · 30 דקות · בוואטסאפ", pulse=True)}<a class="link2" href="#demo">לראות דוגמה ↓</a></div>
    </div>
    <div class="big">{ch("karin", "קארין, מאוירת", bob=0)}<span class="hand">קודם מבינה. אחר כך בונה.</span></div>
  </div>
</header>

<section class="s" id="who" aria-labelledby="who-h" style="padding-top:24px">
  <div class="wrap">
    <div class="head center rv"><div class="eyebrow">למי זה</div><h2 id="who-h">משרדים ובעלי עסקים <mark>שטובעים בניירת</mark>.</h2><p class="intro">מתאים במיוחד ל:</p></div>
    <div class="sect rv">{sect}</div>
  </div>
</section>

<section class="s" id="what" aria-labelledby="what-h" style="padding-top:24px">
  <div class="wrap">
    <div class="head center rv"><div class="eyebrow">מה אני בונה</div><h2 id="what-h">שלושה כלים. <mark>פתרון אחד</mark> שמתאים לכם.</h2></div>
    <div class="how">{pil}</div>
  </div>
</section>

<section class="s" id="demo" aria-labelledby="demo-h" style="padding-top:24px">
  <div class="wrap">
    <div class="head center rv"><div class="eyebrow">מפת המשרד</div><h2 id="demo-h">מה אפשר <u>להעביר</u> אצלכם?</h2><p class="intro">בחרו סוג משרד, ותראו דוגמה למשימות שהסוכנים לוקחים, ומה נשאר אצלכם.</p></div>
    {demo_box("office", "מפת המשרד", DEMO_SUB["office"], "#67e8f9", "#06132e", id_="demo-box")}
  </div>
</section>

<section class="s" id="flow" aria-labelledby="flow-h" style="padding-top:24px">
  <div class="wrap">
    <div class="head center rv"><div class="eyebrow">איך זה עובד</div><h2 id="flow-h">ארבעה צעדים. <mark>בלי הפתעות</mark>.</h2></div>
    <div class="diagram" role="list" style="--cols:4">{dn}</div>
    <div class="appr rv"><b>👑 אתם מאשרים:</b><span>מה נבנה</span><span>כל נקודה רגישה בתהליך</span></div>
  </div>
</section>

<section class="s" id="built" aria-labelledby="built-h" style="padding-top:24px">
  <div class="wrap">
    <div class="head center rv"><div class="eyebrow">מי בונה</div><h2 id="built-h">מ-<span class="ltr">2011</span> בונה <mark>פתרונות מערכות</mark>.</h2><p class="intro">מערכות <span class="ltr">ERP</span> ו-<span class="ltr">CRM</span>, תהליכים מהזמנה ועד גבייה ואינטגרציות. בשנים האחרונות גם <span class="ltr">AI</span>.</p></div>
    <div class="chips rv" style="justify-content:center"><b>כבר בניתי:</b><span>קורא חשבוניות</span><span>דשבורדים פיננסיים עם זיהוי חריגות</span><span>צ׳אטבוט</span><span>מערכת לניהול נכסים וקריאות שירות</span></div>
    <nav class="allteam" aria-label="הצוות והלמידה">{allteam}</nav>
  </div>
</section>

{final('העסק שלכם, <mark>בלי העתק־הדבק</mark>.', 'חצי שעה של שיחה, ואתם יוצאים עם תמונה ברורה: מה הכי שווה לבנות קודם, ואיך זה מתחבר למה שכבר יש לכם.', want)}
</main>
{footer(p)}
{bar(want)}"""
    return page_doc("פתרונות AI למשרדים ולבעלי עסקים | Boost2Business",
                    "אוטומציה, חיבור בין מערכות וסוכני AI למשרדי רואי חשבון, עורכי דין, ניהול נכסים, סוכנויות ביטוח ועסקים קטנים. שיחת אפיון של 30 דקות, חינם.",
                    "פתרונות AI למשרדים ולבעלי עסקים | Boost2Business", "og-solutions.jpg", f"{SITE}/solutions", body, False)


def offer_block(prefix):
    o = OFFER
    pk = []
    for p in o["packages"]:
        price = ""
        if o["show_prices"] and p.get("price_from"):
            price = f'החל מ-<span class="ltr">₪{p["price_from"]:,}</span>' + (f' + <span class="ltr">₪{p["price_monthly"]:,}</span> לחודש' if p.get("price_monthly") else "")
        tag = "a" if p.get("href") else "div"
        href = f' href="{prefix}{p["href"]}"' if p.get("href") else ""
        feat = " feat" if p.get("featured") else ""
        more = '<span class="pr">לפרטים <span class="ltr" aria-hidden="true">←</span></span>' if p.get("href") else ""
        pk.append(f'<{tag} class="pkg{feat}"{href}><span class="ic" aria-hidden="true">{p["icon"]}</span><h4>{p["name"]}</h4><p>{p["desc"]}</p>{more}' + (f'<span class="pr">{price}</span>' if price else '') + f'</{tag}>')
    pilot = ""
    if o["pilot"]["show"]:
        nums = []
        if o["pilot"].get("slots"):
            nums.append(f'{o["pilot"]["slots"]} מקומות בלבד')
        if o["pilot"].get("discount"):
            nums.append(o["pilot"]["discount"])
        extra = (" " + " · ".join(nums) + ".") if nums else ""
        ret = (" " + o["pilot"]["in_return"] + ".") if o["pilot"].get("in_return") else ""
        pilot = f"""<div class="pilot"><span class="sticker">ללקוחות הראשונים</span><h3>פיילוט מייסדים 🚀</h3><p>מקומות מוגבלים לפיילוט, כי אני בונה כל פתרון בעצמי.{extra}{ret} הפרטים בשיחה.</p></div>"""
    guar = ""
    if o["guarantee"]["show"] and o["guarantee"].get("text"):
        guar = f'<div class="guar"><span aria-hidden="true">🛡️</span><b>{o["guarantee"]["text"]}</b></div>'
    pay = ""
    if o.get("payment_url"):
        pay = f'<a class="link2" href="{e(o["payment_url"])}" target="_blank" rel="noopener">לתשלום מאובטח ←</a>'
    return f"""<section class="s" id="offer" aria-labelledby="offer-h" style="padding-top:24px">
  <div class="wrap">
    <div class="head center rv"><div class="eyebrow">איך מתחילים</div><h2 id="offer-h">מוכנים להתחיל? זה מתחיל <mark>בשיחה אחת</mark>.</h2></div>
    <div class="offer">
      <div class="ofree rv">
        <span class="tag">הטבת השקה ללקוחות חדשים</span>
        <span class="free-big">חינם.</span>
        <h3>שיחת אפיון של 30 דקות</h3>
        <ul class="gets">
          <li><svg aria-hidden="true"><use href="#check"/></svg><span>מבינים יחד איפה הזמן שלכם הולך לאיבוד</span></li>
          <li><svg aria-hidden="true"><use href="#check"/></svg><span>בוחרים יחד מה הכי שווה לכם קודם: פתרון, סוכן או למידה</span></li>
          <li><svg aria-hidden="true"><use href="#check"/></svg><span>מקבלים הצעה מותאמת, במחיר נוח</span></li>
          <li><svg aria-hidden="true"><use href="#check"/></svg><span>בלי התחייבות. בעברית או באנגלית</span></li>
        </ul>
        {cta("אני רוצה שיחת אפיון חינם", where="offer")}
        {pay}
      </div>
      <div class="oside rv">{pilot}<div class="pkgs">{"".join(pk)}{"" if o["show_prices"] else f'<p class="pkgnote">{o["no_price_text"]}</p>'}</div></div>
    </div>
    {guar}
  </div>
</section>"""


def faq():
    qa = [
        ("ומה אם זה לא יעבוד?", "<b>אין כזה דבר.</b> אני פה בשבילכם, מהאפיון ועד שזה רץ אצלכם. וזה תמיד עובד 🙂"),
        ("מסובך? אני לא ממש טכנולוגי.", "<b>בכלל לא.</b> אתם מספרים לי איך העסק עובד, ואני בונה ומחברת. אתם מקבלים הודעה ומאשרים בלחיצה. בלי קורסים ובלי סרטונים."),
        ("ומה אם הסוכן טועה?", "בנקודות הרגישות הסוכן עוצר ומחכה <b>לאישור שלכם</b>. אתם רואים מה הוא עשה לפני שזה יוצא החוצה, והתהליך נשאר בשליטה שלכם."),
        ("זה יקר? כמה זה עולה?", "שיחת האפיון <b>חינם ללקוחות חדשים</b>, כהטבת השקה. אחריה תקבלו הצעה מותאמת, במחיר נוח שנקבע לפי מה שבאמת צריך. מתחילים מסוכן אחד, ומרחיבים רק כשזה משתלם לכם."),
        ("מה עם הנתונים שלי?", "בשיחת האפיון עוברים יחד על מה הסוכן צריך לראות ומה לא, ובונים את זה כך שתרגישו בנוח. ובכל מה שרגיש, ההחלטה נשארת אצלכם."),
        ("זה בשבילי?", "אם יש לכם משימה שחוזרת כל יום או כל שבוע (הקלדות, מענה לאותן שאלות, העתקות בין מערכות), <b>כנראה שכן</b>. לא בטוחים? בשביל זה יש שיחת אפיון חינם."),
        ("ואם משהו אצלנו ישתנה? נצטרך להקים הכל מהתחלה?", "<b>ממש לא.</b> הפתרונות שלי גדלים איתכם ומתאימים את עצמם לשינויים, במיוחד בשוק שמתקדם כל כך מהר."),
        ("זה יחליף את העובדים שלי?", "<b>זה ישחרר אותם.</b> הסוכן לוקח את ההקלדות וההעתקות, והאנשים שלכם (ואתם) מתפנים למה שבאמת דורש אתכם."),
        ("ההדרכות בעברית או באנגלית?", "<b>גם וגם.</b> ליחידים ולקבוצות, לפי מה שנוח לכם."),
    ]
    items = "".join(f'<details><summary><span>{q}</span><span class="pm" aria-hidden="true"><svg><use href="#plus"/></svg></span></summary><div class="ans">{a}</div></details>' for q, a in qa)
    return f"""<section class="s" id="faq" aria-labelledby="faq-h" style="padding-top:24px">
  <div class="wrap">
    <div class="head center rv"><div class="eyebrow">שאלות</div><h2 id="faq-h">מה ששואלים אותי. <mark>תשובות קצרות</mark>.</h2></div>
    <div class="faq rv">{items}</div>
  </div>
</section>"""


# ---------------------------------------------------------------- AGENT PAGE
def agent_page(a):
    p = "../"
    he = a["g"] == "m"
    want = f'אני רוצה את {a["first"]} בצוות שלי'
    href = wa_link(a.get("wa_text"))
    tasks = "".join(f'<li class="task rv"><span class="e" aria-hidden="true">{ic}</span><span>{t}</span></li>' for ic, t in a["tasks"])
    dn = "".join(f'<div class="dn{" ok" if i == a["approve_at"] else ""} rv"><span class="c" aria-hidden="true">{ic}</span><b>{t}</b><small>{s}</small></div>' for i, (ic, t, s) in enumerate(a["flow"]))
    appr = "".join(f"<span>{x}</span>" for x in a["approve"])
    b4 = "".join(f'<li><span aria-hidden="true">✗</span><span>{x}</span></li>' for x in a["before"])
    af = "".join(f'<li><span aria-hidden="true">✓</span><span>{x}</span></li>' for x in a["after"])
    fr = []
    for i, s in enumerate(a["friends"]):
        f = BY[s]
        fr.append(f"""<a class="tc rv" href="{s}.html" style="--a:{f["acc"]}"><span class="pic">{ch(s)}</span><div><h3>{f["name"]}</h3><p>{f["role"]}</p><span class="go">לעמוד של {f["first"]} ←</span></div></a>""")
    allteam = "".join(f'<a href="{x["slug"]}.html" style="--a:{x["acc"]}"' + (' aria-current="page"' if x is a else "") + f'>{ch(x["slug"])}{x["first"]}</a>' for x in AG)
    allteam += f'<a href="{p}training.html">{ch("karin")}למידה</a>'
    me = "אותו" if he else "אותה"
    body = f"""<a class="skip" href="#main">דילוג לתוכן</a>
{nav(False, p)}
<main id="main" style="--a:{a["acc"]};--ink:{a["acc_ink"]}">
<header class="ahero" id="top">
  <div class="wrap">
    <div class="htext">
      <div class="crumb"><span class="mini">{ch(a["slug"], bob=0)}</span><span><a href="{p}index.html#team">הצוות</a> · <span class="role">{a["emoji"]} {a["name"]}</span></span></div>
      <h1>{a["h1"]}</h1>
      <p class="lead">{a["lead"]}</p>
      <div class="cta-row">{cta(want, "שיחת אפיון חינם · 30 דקות · בוואטסאפ", href=href, pulse=True)}<a class="link2" href="#demo">לראות {me} עובד{"" if he else "ת"} ↓</a></div>
    </div>
    <div class="big">{ch(a["slug"], a["name"] + ", מאויר" + ("" if he else "ת"), bob=0)}<span class="hand">{a["takes"]}? עליי!</span></div>
  </div>
</header>

<section class="s" id="what" aria-labelledby="what-h" style="padding-top:24px">
  <div class="wrap">
    <div class="head rv"><div class="eyebrow">התפקיד שלי</div><h2 id="what-h">{a["role"]}</h2></div>
    <ul class="tasks">{tasks}</ul>
  </div>
</section>

<section class="s" id="demo" aria-labelledby="demo-h" style="padding-top:24px">
  <div class="wrap">
    <div class="head center rv"><div class="eyebrow">הדגמה חיה</div><h2 id="demo-h">תנסו <u>אותי</u>.</h2><p class="intro">לוקח פחות מדקה. לחצו, ותראו איפה אני עוצר{"" if he else "ת"} ומחכה לכם.</p></div>
    {demo_box(a["slug"], f'{a["name"]} בעבודה', DEMO_SUB[a["slug"]], a["acc"], a["acc_ink"], id_="demo-box")}
  </div>
</section>

<section class="s" id="flow" aria-labelledby="flow-h" style="padding-top:24px">
  <div class="wrap">
    <div class="head center rv"><div class="eyebrow">איפה אני בתהליך</div><h2 id="flow-h">ואיפה <mark>אתם מאשרים</mark>.</h2></div>
    <div class="diagram" role="list">{dn.replace('class="dn', 'role="listitem" class="dn')}</div>
    <div class="appr rv"><b>👑 אתם מאשרים:</b>{appr}</div>
  </div>
</section>

<section class="s" id="ba" aria-labelledby="ba-h" style="padding-top:24px">
  <div class="wrap">
    <div class="head center rv"><div class="eyebrow">לפני ואחרי</div><h2 id="ba-h">מה משתנה כש{a["first"]} {"מצטרף" if he else "מצטרפת"}?</h2></div>
    <div class="ba rv"><div class="b4"><h3>לפני</h3><ul>{b4}</ul></div><span class="arr" aria-hidden="true">←</span><div class="af"><h3>אחרי</h3><ul>{af}</ul></div></div>
    <p class="builton rv">💡 {a["built_on"]}</p>
  </div>
</section>

<section class="s" id="friends" aria-labelledby="fr-h" style="padding-top:24px">
  <div class="wrap">
    <div class="head center rv"><div class="eyebrow">עובד{"" if he else "ת"} טוב עם…</div><h2 id="fr-h">ביחד זה <mark>צוות</mark>.</h2></div>
    <div class="friends">{"".join(fr)}</div>
    <nav class="allteam" aria-label="כל הצוות">{allteam}</nav>
  </div>
</section>

{final(f'רוצים את {a["first"]} <mark>בצוות</mark>?', 'חצי שעה של שיחה, ואתם יוצאים עם תמונה ברורה: מה ' + a["first"] + ' ' + ("יעשה" if he else "תעשה") + ' אצלכם, ואיך זה מתחבר למה שכבר יש לכם.', want, href=href)}
</main>
{footer(p)}
{bar(want, href=href)}"""
    return page_doc(a["title"], a["desc"], f'{a["name"]} · {strip_tags(a["h1"])} | Boost2Business', f'og-{a["slug"]}.jpg', f'{SITE}/team/{a["slug"]}', body, False)


def strip_tags(s):
    import re
    return re.sub(r"<[^>]+>", "", s)


# ---------------------------------------------------------------- TRAINING
def training_page():
    t = DATA["training"]
    p = ""
    steps = [("💬", "שיחת התאמה", "מה אתם עושים, מה חוזר על עצמו"), ("🎓", "הדרכה מעשית", "על הכלים ועל המשימות שלכם"),
             ("🛠️", "תרגול אמיתי", "על משימה מהעסק, לא על דוגמה"), ("📌", "דרך עבודה קבועה", "תבניות שנשארות אצלכם"), ("🤝", "ליווי", "שאלות? אני פה")]
    dn = "".join(f'<div role="listitem" class="dn rv"><span class="c" aria-hidden="true">{ic}</span><b>{a}</b><small>{b}</small></div>' for ic, a, b in steps)
    cmp_ = [("1:1", "למידה אישית", "#fbbf24", [("למי", "בעלי עסקים, עצמאים ומנהלים"), ("איך", "אחד על אחד, בקצב שלכם, על העבודה שלכם"), ("יוצאים עם", "דרך עבודה ותבניות שמתאימות בדיוק לכם")]),
            ("1:n", "למידה בקבוצה", "#67e8f9", [("למי", "צוותים, משרדים וקבוצות"), ("איך", "הדרכה מעשית, וכולם מתרגלים על משימות אמיתיות"), ("יוצאים עם", "שפה משותפת ודרך עבודה אחידה לכל הצוות")])]
    tasks = "".join(f'<div class="cmpc rv" style="--a:{acc}"><span class="cbig ltr">{n}</span><h3>{t_}</h3><dl>' + "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in rows) + "</dl></div>" for n, t_, acc, rows in cmp_)
    allteam = "".join(f'<a href="team/{x["slug"]}.html" style="--a:{x["acc"]}">{ch(x["slug"])}{x["first"]}</a>' for x in AG)
    allteam += f'<a href="training.html" aria-current="page">{ch("karin")}למידה</a>'
    want = "אני רוצה הדרכה"
    body = f"""<a class="skip" href="#main">דילוג לתוכן</a>
{nav(False, p)}
<main id="main" style="--a:#67e8f9;--ink:#06132e">
<header class="ahero" id="top">
  <div class="wrap">
    <div class="htext">
      <div class="crumb"><span class="mini">{ch("karin", bob=0)}</span><span><a href="index.html#paths">מה אני עושה</a> · <span class="role">🎓 {t["name"]}</span></span></div>
      <h1>{t["h1"]}</h1>
      <p class="lead">{t["lead"]}</p>
      <div class="cta-row">{cta(want, "שיחת אפיון חינם · 30 דקות · בוואטסאפ", pulse=True)}<a class="link2" href="#demo">לראות את ההבדל ↓</a></div>
    </div>
    <div class="big">{ch("karin", "קארין, מאוירת", bob=0)}<span class="hand">בונה לכם. מלמדת אתכם.</span></div>
  </div>
</header>

<section class="s" id="what" aria-labelledby="what-h" style="padding-top:24px">
  <div class="wrap">
    <div class="head center rv"><div class="eyebrow">שתי דרכים ללמוד</div><h2 id="what-h">אחד על אחד, <mark>או כל הצוות</mark>.</h2><p class="intro">בלי קורסים ובלי סרטונים. אתם צריכים מישהו שיבין מה קורה אצלכם ומה העסק שלכם צריך. לא סיסמאות.</p></div>
    <div class="cmp">{tasks}<span class="vs-dot" aria-hidden="true">או</span></div>
    <div class="langs rv"><span><span aria-hidden="true">🇮🇱</span> בעברית</span><span class="ltr"><span aria-hidden="true">🌍</span> In English</span></div>
  </div>
</section>

<section class="s" id="demo" aria-labelledby="demo-h" style="padding-top:24px">
  <div class="wrap">
    <div class="head center rv"><div class="eyebrow">הדגמה</div><h2 id="demo-h">מ<u>שיחה</u> לדרך <mark>עבודה</mark>.</h2><p class="intro">בחרו משימה, ותראו מה משתנה אחרי הדרכה.</p></div>
    {demo_box("training", "לפני ואחרי ההדרכה", DEMO_SUB["training"], "#67e8f9", "#06132e", id_="demo-box")}
  </div>
</section>

<section class="s" id="flow" aria-labelledby="flow-h" style="padding-top:24px">
  <div class="wrap">
    <div class="head center rv"><div class="eyebrow">איך זה בנוי</div><h2 id="flow-h">חמש תחנות. <mark>אחת מהן</mark> היא העסק שלכם.</h2></div>
    <div class="diagram" role="list">{dn}</div>
  </div>
</section>

<section class="s" id="friends" aria-labelledby="fr-h" style="padding-top:24px">
  <div class="wrap">
    <div class="head center rv"><div class="eyebrow">ומשם?</div><h2 id="fr-h">מי שלמד לעבוד עם <span class="ltr">AI</span> <mark>מוכן לצוות</mark>.</h2><p class="intro">ההדרכה עומדת לבד, או כצעד ראשון לפני הסוכן הראשון שלכם.</p></div>
    <nav class="allteam" aria-label="כל הצוות">{allteam}</nav>
  </div>
</section>

{final('ללמוד <u>פעם אחת</u>. לחסוך זמן <mark>כל שבוע</mark>.', 'חצי שעה של שיחה, ונבין יחד מה הכי שווה ללמוד קודם, לכם או לצוות שלכם.', want)}
</main>
{footer(p)}
{bar(want)}"""
    return page_doc(t["title"], t["desc"], "הדרכות AI ליחידים ולקבוצות | Boost2Business", "og-training.jpg", f"{SITE}/training", body, False)


# ---------------------------------------------------------------- OG images
def og_images():
    from playwright.sync_api import sync_playwright
    F = os.path.join(ROOT, "tools", ".cache", "fonts", "node_modules", "@expo-google-fonts")
    ff = (f'@font-face{{font-family:"Secular One";src:url(file://{F}/secular-one/400Regular/SecularOne_400Regular.ttf)}}'
          f'@font-face{{font-family:Rubik;font-weight:400;src:url(file://{F}/rubik/400Regular/Rubik_400Regular.ttf)}}'
          f'@font-face{{font-family:Rubik;font-weight:700;src:url(file://{F}/rubik/700Bold/Rubik_700Bold.ttf)}}')
    css = (ff + "body{margin:0;width:1200px;height:627px;overflow:hidden;background:radial-gradient(700px 500px at 15% 30%,rgba(99,102,241,.45),transparent 65%),radial-gradient(700px 500px at 95% 0%,rgba(139,92,246,.45),transparent 60%),#080a24;color:#f5f4ff;font-family:Rubik;direction:rtl}"
           ".w{display:grid;grid-template-columns:1fr 430px;height:100%;align-items:center;padding:0 70px;gap:30px}"
           "h1{font-family:'Secular One';font-weight:400;font-size:70px;line-height:1.08;margin:0}"
           "mark{color:inherit;background:linear-gradient(176deg,transparent 52%,rgba(139,92,246,.75) 52%,rgba(139,92,246,.75) 90%,transparent 90%)}"
           "u{text-decoration:none;box-shadow:inset 0 -.16em #67e8f9}"
           ".k{font-size:28px;color:#c4b5fd;margin-bottom:18px;font-weight:700}.c{margin-top:28px;display:inline-block;background:#67e8f9;color:#06132e;font-weight:700;font-size:28px;border-radius:999px;padding:14px 30px}"
           ".b{position:absolute;top:34px;left:60px;direction:ltr;font-weight:700;font-size:26px}.b span{font-weight:400}"
           ".team{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}.team svg{width:100%}")
    jobs = [("og.jpg", "צוות של סוכני AI לעסק שלכם", "אתם <u>תנהלו</u>. הסוכנים שלכם <mark>יעבדו בשבילכם</mark>.",
             '<div class="team">' + "".join(ch(x["slug"]) for x in AG) + ch("karin") + "</div>")]
    for a in AG:
        jobs.append((f"og-{a['slug']}.jpg", a["name"] + " · " + a["role"], a["h1"], ch(a["slug"])))
    jobs.append(("og-solutions.jpg", "פתרונות AI למשרדים ולבעלי עסקים", 'פתרון <span class="ltr">AI</span> שבנוי <u>בדיוק</u> <mark>לעסק שלכם</mark>.', ch("karin")))
    jobs.append(("og-training.jpg", "הדרכות AI · יחידים וקבוצות · עברית או English", DATA["training"]["h1"], ch("karin")))
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1200, "height": 627})
        for fn, k, h1, art in jobs:
            doc = (f'<!doctype html><html dir="rtl" lang="he"><meta charset="utf-8"><style>{css}</style><body>'
                   f'<svg width="0" height="0" style="position:absolute"><defs>{characters.symbols()}</defs></svg>'
                   f'<div class="b">Boost<span>2Business</span></div><div class="w"><div><div class="k">{k}</div><h1>{h1}</h1>'
                   f'<div class="c">שיחת אפיון חינם · 30 דקות</div></div><div>{art}</div></div></body></html>')
            pg.set_content(doc)
            pg.wait_for_timeout(250)
            pg.screenshot(path=os.path.join(SRC, fn), type="jpeg", quality=86)
            print("og:", fn)
        b.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--og", action="store_true", help="also render the 1200x627 og images")
    a = ap.parse_args()
    os.makedirs(os.path.join(SRC, "team"), exist_ok=True)
    out = {"index.html": home(), "training.html": training_page(), "solutions.html": solutions_page()}
    for ag in AG:
        out[f"team/{ag['slug']}.html"] = agent_page(ag)
    for k, v in out.items():
        open(os.path.join(SRC, k), "w", encoding="utf-8").write(v)
        print(f"wrote site/src/{k:<20} {len(v.encode())/1024:6.1f} KB")
    if a.og:
        og_images()


if __name__ == "__main__":
    main()
