#!/usr/bin/env python3
"""Phase-1 ops PDFs (docs/TASK.md §1), all through tools/render_pdf.py:

  ops/whatsapp-setup.pdf       WhatsApp Business setup (1 page) + every reply to copy (appendix page).
                               Texts come from templates/whatsapp-replies.md, the single source.
  ops/discovery-call-kit.pdf   the 30-minute call script (1 page) + the summary form to print (1 page).
                               The form has the same fields tools/make_quote.py reads.
  ops/pipeline-onepager.pdf    the 10 stages on one page: who does what, where Karin approves.
  ops/examples/quote-sample.pdf  a quote for a fictional business (tools/make_quote.py).

usage:  python3 tools/build_ops_docs.py [--png DIR]     (PNG previews of every page, for checking)
"""
import argparse
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_pdf import ROOT, esc, page, render  # noqa: E402
import make_quote  # noqa: E402

OPS = os.path.join(ROOT, "ops")


def ltr(s):
    return make_quote.ltr_tokens(s)


# ---------------------------------------------------------------- WhatsApp
def wa_sections():
    """templates/whatsapp-replies.md -> {"profile": {...}, "labels": [...], "greeting": str, "away": str, "replies": [...]}"""
    md = open(os.path.join(ROOT, "templates", "whatsapp-replies.md"), encoding="utf-8").read()
    secs = re.split(r"^## ", md, flags=re.M)[1:]
    out = {"replies": [], "labels": [], "profile": {}}
    for s in secs:
        head, _, body = s.partition("\n")
        body = body.strip()
        if head.startswith("פרופיל"):
            out["profile"] = dict(re.findall(r"\*\*(.+?):\*\*\s*(.+)", body))
        elif head.startswith("תוויות"):
            for line in body.splitlines()[2:]:
                cells = [c.strip() for c in line.strip("|").split("|")]
                if len(cells) == 3:
                    out["labels"].append(cells)
        elif head.startswith("0."):
            out["greeting"] = re.search(r"\*\*פתיחה:\*\*\s*(.+)", body).group(1)
            out["away"] = re.search(r"\*\*לא זמינה:\*\*\s*(.+)", body).group(1)
        else:
            m = re.match(r"(\d+)\.\s*(.+?)\s*\(`(/\S+)`\s*·\s*`(/\S+)`\)\s*(.*)", head)
            if m:
                n, title, he, en, note = m.groups()
                out["replies"].append({"n": n, "title": title, "he": he, "en": en, "note": note.strip(" ·"), "text": body})
    if len(out["replies"]) < 12 or not out["labels"] or "greeting" not in out:
        raise SystemExit("templates/whatsapp-replies.md: unexpected structure (12 replies, labels, greeting)")
    return out


def sc(s):
    return f'<span class="sc">{esc(s)}</span>'


def whatsapp_doc():
    w = wa_sections()
    p = w["profile"]
    labels = "".join(f"<tr><td><b>{esc(a)}</b></td><td>{esc(b)}</td><td class='small'>{ltr(c)}</td></tr>" for a, b, c in w["labels"])
    first = [r for r in w["replies"] if r["n"] in ("1", "2", "3", "4", "5", "6", "7")]
    later = [r for r in w["replies"] if r not in first]
    qr = "".join(f"<tr><td>{sc(r['he'])}</td><td>{sc(r['en'])}</td><td>{esc(r['title'])}</td></tr>" for r in first)
    qr += (f"<tr><td colspan='3' class='muted'>את שאר הקיצורים ({later[0]['n']}–{later[-1]['n']} בעמוד 2) "
           "מוסיפים כשמגיע הלקוח הראשון.</td></tr>")
    page1 = f"""
<div class="box cy"><b>למה:</b> כל ליד מקבל מענה תוך שניות, והמענה הראשון לוקח לך 10 שניות. <b>מה עושים:</b> 5 הגדרות חד־פעמיות, בערך 20 דקות. את מגדירה בעצמך, בטלפון.
<div class="small muted" style="margin-top:1mm">שמות התפריטים משתנים מעט בין גרסאות. אם משהו לא נמצא: <b>הגדרות ← כלים לעסקים</b> (Business tools).</div></div>
<div class="grid2">
<div>
<h2><span class="n">1</span>פרופיל עסקי</h2>
<p class="small">הגדרות ← כלים לעסקים ← פרופיל עסקי</p>
<table class="small"><tr><th style="width:22%">שם</th><td>{ltr(p.get('שם', ''))}</td></tr>
<tr><th>תיאור</th><td>{ltr(p.get('תיאור', ''))}</td></tr>
<tr><th>אתר</th><td><span class="ltr">{esc(p.get('אתר', ''))}</span></td></tr>
<tr><th>קטגוריה</th><td>הכי קרובה מהרשימה, למשל ייעוץ או שירותי מחשוב</td></tr>
<tr><th>שעות</th><td>[השעות שבהן את עונה בפועל]</td></tr></table>
<h2><span class="n">2</span>הודעת פתיחה</h2>
<p class="small">כלים לעסקים ← הודעת פתיחה ← להפעיל. נשלחת לבד ללקוח חדש, או אחרי זמן ארוך בלי שיחה.</p>
<div class="box small">{esc(w['greeting'])}</div>
<h2><span class="n">3</span>הודעת "לא זמינה"</h2>
<p class="small">כלים לעסקים ← הודעת היעדרות ← להפעיל ← לתזמן "מחוץ לשעות הפעילות".</p>
<div class="box small">{esc(w['away'])}</div>
</div>
<div>
<h2><span class="n">4</span>תשובות מהירות</h2>
<p class="small">כלים לעסקים ← תשובות מהירות ← <b>+</b>. מדביקים את הטקסט מעמוד 2 ושומרים עם הקיצור. בצ׳אט מקלידים <span class="sc">/</span> ובוחרים.
אם האפליקציה לא מקבלת קיצור בעברית, משתמשים בקיצור באנגלית.</p>
<table class="small"><tr><th>קיצור</th><th>חלופה</th><th>מתי</th></tr>{qr}</table>
<h2><span class="n">5</span>תוויות</h2>
<p class="small">לוחצים לחיצה ארוכה על צ׳אט ← תווית. התווית אומרת איפה הליד עומד, וטבלת הלידים מתעדכנת באותו רגע.</p>
<table class="small"><tr><th>תווית</th><th>מתי</th><th>שלב בטבלה</th></tr>{labels}</table>
</div></div>
<div class="box vi small" style="margin-top:2mm"><b>הרגל של דקה בסוף היום:</b> כל צ׳אט עם תווית "ליד חדש" ← שורה בטבלת הלידים (שם, טלפון, מקור, ההודעה בקצרה, הצעד הבא ועד מתי).
הכלים המובנים לא שואלים שאלות ולא קובעים שיחות לבד. זה נשאר אצלך, וזה בכוונה: כל הודעה ללקוח יוצאת ממך.</div>"""

    def reply_card(r):
        note = f" <span class='chip k' style='white-space:nowrap'>{ltr(r['note'])}</span>" if r["note"] else ""
        text = esc(r["text"]).replace("\n", "<br>")
        return (f"<div class='box' style='break-inside:avoid;padding:2.2mm 3mm;margin-bottom:2.2mm'>"
                f"<div style='display:flex;gap:2mm;align-items:center;margin-bottom:1mm'>{sc(r['he'])}{sc(r['en'])}"
                f"<b style='font-size:9.4pt'>{r['n']}. {esc(r['title'])}</b>{note}</div>"
                f"<div class='small' style='line-height:1.45'>{text}</div></div>")
    page2 = (f"<p class='small muted' style='margin-bottom:2mm'>מילים בסוגריים מרובעים ממלאים לפני השליחה. "
             f"המקור לעריכה: <span class='ltr'>templates/whatsapp-replies.md</span>.</p>"
             f"<div style='columns:2;column-gap:4mm'>{''.join(reply_card(r) for r in w['replies'])}</div>")
    return page("", "", kicker="Boost2Business · ערכת וואטסאפ", sheets=[
        ("הגדרת WhatsApp Business", "פרופיל, הודעות אוטומטיות, תשובות מהירות ותוויות", page1),
        ("כל התשובות המהירות", "להעתקה לאפליקציה", page2),
    ], foot_note="ערכת וואטסאפ")


# ---------------------------------------------------------------- discovery call
def call_doc():
    agenda = [("0–5′", "היכרות", "מי אני (מ-2011 בונה פתרונות מערכות), מה העסק שלכם, ומה הביא אתכם"),
              ("5–20′", "שאלות", "השאלות למטה. לבקש להראות במסך תהליך אחד"),
              ("20–27′", "מפת המשימות", "מה אפשר להעביר לסוכן, מה לפתרון, ומה ללמוד. ואיפה אתם מאשרים"),
              ("27–30′", "הצעד הבא", "\"אשלח הצעה עד [יום]\". לבדוק מי מקבל החלטות")]
    ag = "".join(f"<tr><td style='white-space:nowrap'><b class='ltr'>{a}</b></td><td><b>{b}</b></td><td>{esc(c)}</td></tr>" for a, b, c in agenda)
    qs = ["מה העסק עושה? כמה אנשים עובדים בו?",
          "אילו משימות חוזרות כל יום או כל שבוע? כמה זמן כל אחת לוקחת, בערך?",
          "באילו מערכות אתם עובדים? (הנהלת חשבונות, CRM, אקסל, וואטסאפ, מייל, טפסים)",
          "איפה דברים נתקעים, נשכחים או מוקלדים פעמיים?",
          "מה הכי רגיש? (כסף, לקוחות, מסמכים) כאן נוסיף נקודות אישור.",
          "איך נראית הצלחה בעוד 3 חודשים?",
          "מי מחליט? מתי רוצים להתחיל? יש תקציב בראש?"]
    ql = "".join(f"<li>{ltr(q)}</li>" for q in qs)
    page1 = f"""
<div class="box cy"><b>המטרה:</b> הלקוח יוצא עם תמונה ברורה גם אם לא יקנה. את יוצאת עם מספיק כדי לכתוב הצעה באותו יום.
<span class="hand">חינם, בלי התחייבות, ובגובה העיניים.</span></div>
<h2><span class="n">1</span>סדר השיחה · 30 דקות</h2>
<table><tr><th style="width:13%">זמן</th><th style="width:18%">מה</th><th>איך</th></tr>{ag}</table>
<h2><span class="n">2</span>שאלות לכולם</h2>
<ol>{ql}</ol>
<h2><span class="n">3</span>לפי מסלול</h2>
<div class="grid3">
<div class="box"><span class="chip">פתרון למשרד או לעסק</span><p class="small">תארו תהליך אחד מקצה לקצה: מה נכנס, מה יוצא ומי מאשר? יש למערכות גישה חיצונית (ייצוא, <span class="ltr">API</span> או אקסל)? אילו אילוצים יש? (רגולציה, הרשאות, ספק <span class="ltr">IT</span>)</p></div>
<div class="box"><span class="chip c">סוכן</span><p class="small">איזה סוכן הכי קרוב לכאב? (חני / דנה / שירה / נגה / גל) כמה פריטים בשבוע? (חשבוניות, שאלות, קריאות) מה הסוכן אסור שיעשה לבד?</p></div>
<div class="box"><span class="chip k">למידה 1:1 או בקבוצה</span><p class="small">מי לומד ומה הרמה היום? אילו משימות אמיתיות נתרגל? בעברית או באנגלית? פרונטלי או מרחוק?</p></div>
</div>
<h2><span class="n">4</span>מיד אחרי השיחה · 10 דקות</h2>
<ol class="small">
<li>ממלאים את טופס הסיכום (עמוד 2) או מקלידים אותו לקובץ טקסט באותו מבנה.</li>
<li>בטבלת הלידים: תאריך שיחה, קישור לסיכום, שלב <b class="ltr">2b</b>, הצעד הבא = הצעה, ועד מתי.</li>
<li>מפיקים הצעה: <span class="ltr">python3 tools/make_quote.py summary.txt</span>, או שולחים את הסיכום ל-<span class="ltr">Claude</span> ומבקשים הצעה. משלימים מחיר ותנאים, ושולחים עם <span class="sc">/הצעה</span>.</li>
</ol>"""

    def field(label, lines=1, hint=""):
        h = f" <span class='small muted'>{esc(hint)}</span>" if hint else ""
        return f"<p style='margin:2.2mm 0 0'><b>{esc(label)}:</b>{h}</p>" + "<div class='line'></div>" * lines

    rows = "".join("<tr>" + "<td style='height:9mm'></td>" * 4 + "</tr>" for _ in range(5))
    page2 = f"""
<p class="small muted">אותם שדות שהמחולל קורא (<span class="ltr">templates/examples/call-summary.example.txt</span>). שדה ריק בהצעה = [קארין ממלאת].</p>
<div class="grid2">
<div>{field('לקוח', 1, 'שם, עסק, תחום')}</div>
<div><p style="margin:2.2mm 0 0"><b>מסלול:</b> &nbsp; ☐ פתרון &nbsp; ☐ סוכן &nbsp; ☐ למידה &nbsp;&nbsp; <b>תאריך שיחה:</b> <span class="fill"></span></p><div class="line"></div></div>
</div>
{field('הכאב', 2, 'משפט אחד, במילים של הלקוח')}
{field('הצלחה', 1, 'איך זה נראה בעוד 3 חודשים')}
<h2 style="margin-top:4mm"><span class="n">★</span>מפת המשימות</h2>
<table><tr><th>משימה</th><th style="width:22%">כמה זמן היום (לפי הלקוח)</th><th style="width:20%">מי לוקח: סוכן / פתרון / למידה</th><th style="width:24%">נקודת אישור</th></tr>{rows}</table>
<div class="grid2">
<div>{field('מערכות וגישות', 2)}</div>
<div>{field('אילוצים', 2, 'רגולציה, הרשאות, אנשים, תקציב')}</div>
</div>
<div class="grid2">
<div>{field('מי מחליט, ומתי מתחילים', 1)}</div>
<div>{field('ההמלצה שלי לצעד ראשון', 1)}</div>
</div>
<div class="box vi" style="margin-top:3mm"><b>להצעה</b> <span class="small muted">(רק מה שאת מחליטה. ריק = [קארין ממלאת])</span>
<div class="grid2 small" style="margin-top:1mm">
<div>לא כלול: <span class="fill" style="min-width:50mm"></span><br>מה צריך מהלקוח: <span class="fill" style="min-width:42mm"></span><br>שבועות: <span class="fill"></span></div>
<div>מחיר הקמה: <span class="fill"></span><br>מחיר חודשי: <span class="fill"></span><br>תנאי תשלום: <span class="fill"></span> &nbsp; בתוקף עד: <span class="fill" style="min-width:20mm"></span></div>
</div></div>
<p class="small" style="margin-top:2mm"><b>הצעה תישלח עד:</b> <span class="fill"></span> &nbsp; ← בטבלה: שלב <b class="ltr">2b</b>, הצעד הבא = הצעה</p>"""
    return page("", "", kicker="Boost2Business · שיחת אפיון", sheets=[
        ("תסריט שיחת אפיון", "30 דקות · חינם · הטבת השקה ללקוחות חדשים", page1),
        ("סיכום שיחה ומפת המשימות", "למלא באותו יום. מכאן נכתבת ההצעה", page2),
    ], foot_note="ערכת שיחת אפיון")


# ---------------------------------------------------------------- pipeline one-pager
STAGES = [
    ("0", "ליד בוואטסאפ", "פנייה מהאתר, לינקדאין, פייסבוק או המלצה", ["auto:הודעת פתיחה", "karin:תווית + שורה בטבלה"], "", "שורה בטבלה תוך 24 שעות"),
    ("1", "מענה וסינון", "שתי שאלות, ואז הזמנה לשיחה או סגירה יפה", ["karin:שולחת תשובה מהירה", "client:עונה"], "כל הודעה יוצאת ממך", "שיחה נקבעה או X"),
    ("2", "שיחת אפיון", "30 דקות, חינם. תסריט + טופס סיכום", ["karin:מנהלת את השיחה", "client:מספר ומראה תהליך", "karin:תזכורת יום לפני"], "", "סיכום + מפת משימות, באותו יום"),
    ("3", "הצעת מחיר", "PDF ממותג מהסיכום, ושליחה בוואטסאפ", ["auto:המחולל ממלא את ההצעה", "karin:מחיר, תנאים, שליחה"], "מחיר והיקף: רק את", "אושרה / נדחתה / פג תוקף"),
    ("4", "תשלום", "קישור תשלום, קבלה/חשבונית, הודעת פתיחה", ["client:משלם", "karin:מנפיקה מסמך"], "אחרי D5–D10: עוסק, סליקה, תנאים", "שולם"),
    ("5", "אפיון מלא", "תהליכים, מערכות, הרשאות, אילוצים, נקודות אישור", ["karin:כותבת אפיון", "client:מאשר בכתב"], "הלקוח חותם לפני בנייה", "אפיון מאושר"),
    ("6", "יישום", "בנייה על נתונים לדוגמה, עדכון שבועי", ["karin:בונה", "auto:n8n / סוכנים", "client:בודק"], "שינוי היקף = הצעה חדשה", "כל קריטריוני הקבלה עברו"),
    ("8", "העלאה לאוויר", "צ׳קליסט, הרשאות, ניטור, הדרכה", ["karin:מעלה ומלווה", "client:מאשר שזה עובד"], "הלקוח מאשר עלייה", "שלב 8 בטבלה"),
    ("9", "תמיכה", "בדיקה אחרי שבועיים ושישה שבועות", ["karin:ליווי", "client:משוב"], "המלצה: רק מלקוח אמיתי, באישורו", "תאריך הבדיקה הבאה בטבלה"),
]
ROLE = {"karin": ("קארין", "k"), "client": ("לקוח", "c"), "auto": ("אוטומציה", "a")}


def pipeline_doc():
    cards = []
    for n, title, what, roles, approve, done in STAGES:
        chips = "".join(f"<span class='chip {ROLE[r.split(':')[0]][1]}'>{ROLE[r.split(':')[0]][0]}: {ltr(r.split(':', 1)[1])}</span>" for r in roles)
        ap = f"<span class='ap'>✓ {ltr(approve)}</span>" if approve else ""
        cards.append(f"""<div class="st"><div class="num"><span class="ltr">{n}</span></div><div class="sb">
<div class="t1"><b>{esc(title)}</b><span class="what">{ltr(what)}</span></div>
<div>{chips}</div><div>{ap}<span class="done">סיום: {ltr(done)}</span></div></div></div>""")
    css = """<style>
.pl{display:grid;grid-template-columns:1fr 48mm;gap:5mm}
.st{display:flex;gap:3mm;position:relative;padding-bottom:1.3mm}
.st:not(:last-child)::after{content:"";position:absolute;right:4.6mm;top:10mm;bottom:-.5mm;width:.8mm;background:linear-gradient(#8b5cf6,#38bdf8);border-radius:1mm}
.num{flex:none;width:10mm;height:10mm;border-radius:50%;background:linear-gradient(135deg,#7c3aed,#4f46e5 55%,#0ea5e9);color:#fff;display:grid;place-items:center;font-weight:800;font-size:11pt}
.sb{flex:1;border:1px solid #e1e2f7;border-radius:3mm;padding:1.1mm 3mm 1mm;background:#fafaff}
.sb .chip{margin-bottom:.4mm;font-size:8.2pt}
.t1{display:flex;gap:2.5mm;align-items:baseline;flex-wrap:wrap;margin-bottom:.4mm}
.t1 b{font-family:"Secular One";font-weight:400;font-size:12pt;color:#1e1b4b}
.what{font-size:9pt;color:#4b4f80}
.ap{display:inline-block;font-size:8.4pt;font-weight:800;color:#06132e;background:#67e8f9;border-radius:99px;padding:0 2.6mm}
.done{display:inline-block;font-size:8.4pt;color:#6b6f9e;margin-inline-start:2mm}
.side .box{font-size:9pt}
.side h3{font-family:"Secular One";font-weight:400;color:#312e81;font-size:11.5pt;margin:0 0 1mm}
</style>"""
    side = """<div class="side">
<div class="box vi"><h3>מי עושה מה</h3><span class="chip k">קארין</span> מחליטה ושולחת<br><span class="chip c">לקוח</span> מספר, בודק ומאשר<br><span class="chip a">אוטומציה</span> מנסחת, מזכירה וסופרת
<p class="small" style="margin-top:1.5mm"><span class="ap">✓</span> = כאן את מאשרת. שום דבר לא יוצא ללקוח, עולה כסף או לוקח מהזמן שלך בלי אישור.</p></div>
<div class="box"><h3>7 · תשתיות העסק</h3><p class="small">רץ לאורך כל הדרך, לא שלב של ליד:</p>
<ol class="small" style="padding-inline-start:4mm;margin:0"><li>וואטסאפ עסקי ✓</li><li>טבלת לידים ✓</li><li>יומן לקביעת שיחות</li><li>רישום עוסק</li><li>חשבוניות</li><li>קישור תשלום</li><li>תנאים וחוזה (עו״ד)</li><li>תיקיית תבניות ב-Drive</li><li>מנהל סיסמאות וגיבוי</li><li>מדידה באתר</li></ol></div>
<div class="box cy"><h3>כלל אחד</h3><p class="small">שורה אחת לכל ליד, מההודעה הראשונה ועד התמיכה. בכל מעבר מעדכנים: שלב, הצעד הבא, ועד מתי.</p></div>
<div class="box"><h3>היעד בשלב 1</h3><p class="small">מליד חדש ועד הצעה שנשלחה, בפחות מ-15 דקות שלך (בלי השיחה עצמה).</p></div>
</div>"""
    body = css + f"<div class='pl'><div>{''.join(cards)}</div>{side}</div>"
    return page("מהליד בוואטסאפ ועד התמיכה", body, kicker="Boost2Business · מפת התהליך",
                sub="10 השלבים, מי עושה מה, ואיפה את מאשרת", foot_note="מפת התהליך")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--png", help="write PNG previews of every page into this folder")
    a = ap.parse_args()
    jobs = [("whatsapp-setup.pdf", whatsapp_doc()), ("discovery-call-kit.pdf", call_doc()),
            ("pipeline-onepager.pdf", pipeline_doc())]
    for name, doc in jobs:
        out = render(doc, os.path.join(OPS, name))
        print("wrote", os.path.relpath(out, ROOT))
    f, t = make_quote.parse(os.path.join(ROOT, "templates", "examples", "call-summary.example.txt"))
    doc, _, _ = make_quote.build(f, t)
    print("wrote", os.path.relpath(render(doc, os.path.join(OPS, "examples", "quote-sample.pdf")), ROOT))
    if a.png:
        os.makedirs(a.png, exist_ok=True)
        for name in [j[0] for j in jobs] + ["examples/quote-sample.pdf"]:
            pdf = os.path.join(OPS, name)
            subprocess.run(["pdftoppm", "-r", "80", "-png", pdf, os.path.join(a.png, os.path.basename(name)[:-4])], check=True)
        print("previews in", a.png)


if __name__ == "__main__":
    main()
