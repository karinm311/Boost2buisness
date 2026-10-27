#!/usr/bin/env python3
"""Quote PDF from a discovery-call summary (docs/TASK.md §1.4).

Input: a short text file in the shape of templates/examples/call-summary.example.txt,
the same fields as the printed summary form in ops/discovery-call-kit.pdf:
"שדה: ערך" lines, "#" comments, and any number of
"משימה: משימה | כמה זמן היום | מי לוקח | נקודת אישור" lines.

Output: a branded Hebrew PDF that follows templates/quote.md, plus the
filled `/הצעה` WhatsApp message printed to the terminal for copy-paste.

  - Price, payment terms, timeline and validity stay "[קארין ממלאת]" unless
    Karin typed them in the summary. Nothing is invented.
  - The "טיוטה לאישור קארין" stamp stays unless --final (only after she approves).
  - "דוגמה: כן" in the input adds a big "דוגמה · עסק דמיוני" banner.
  - Real quotes hold client data: the default output is out/quotes/, which is
    gitignored. Never commit a real quote.

usage:  python3 tools/make_quote.py summary.txt [-o out.pdf] [--final] [--png preview.png]
"""
import argparse
import datetime as dt
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_pdf import ROOT, esc, page, render  # noqa: E402

TBD = "[קארין ממלאת]"
TRACKS = {"פתרון": "פתרון למשרד או לעסק", "סוכן": "צוות סוכנים", "למידה": "למידה 1:1 או בקבוצה"}
DEFAULT_OUT = ("רישוי של מערכות צד שלישי, שינויים במערכות שאינן בהיקף, הזנת נתונים היסטוריים.")
DEFAULT_NEED = "גישה למערכות דרך החשבונות שלכם (לא סיסמאות בצ׳אט), ואיש קשר אחד."


def parse(path):
    fields, tasks = {}, []
    for raw in open(path, encoding="utf-8"):
        line = raw.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        k, v = (s.strip() for s in line.split(":", 1))
        if k == "משימה":
            parts = [p.strip() for p in v.split("|")] + [""] * 4
            tasks.append(parts[:4])
        else:
            fields[k] = v
    return fields, tasks


def val(f, k):
    return esc(f.get(k) or TBD)


LTR_RUN = re.compile(r"([A-Za-z0-9][A-Za-z0-9 .:/@_\-–]*[A-Za-z0-9]|[A-Za-z0-9])")


def ltr_tokens(s):
    """Escape text and wrap Latin/digit runs so bidi keeps them in order (CLAUDE.md, RTL rules)."""
    parts = LTR_RUN.split(str(s))
    return "".join(f'<span class="ltr">{esc(p)}</span>' if i % 2 else esc(p) for i, p in enumerate(parts))


def build(fields, tasks, draft=True):
    f = fields
    today = dt.date.today()
    qid = f.get("מס הצעה") or f"Q-{today:%Y%m%d}"
    client = f.get("לקוח") or TBD
    biz = f.get("עסק") or ""
    track_key = next((t for t in TRACKS if t in (f.get("מסלול") or "")), None)
    sample = (f.get("דוגמה") or "").startswith("כן")
    T = ltr_tokens

    banner = ('<div class="box vi" style="text-align:center;font-weight:800;color:#5b21b6;font-size:11pt">'
              'דוגמה · עסק דמיוני ונתונים לדוגמה בלבד. לא הצעה אמיתית.</div>') if sample else ""

    meta = f"""<table class="small" style="margin-top:0">
<tr><th style="width:13%">הצעה ל</th><td>{T(client)}{(' · ' + T(biz)) if biz else ''}</td><th style="width:13%">מס׳ הצעה</th><td style="width:24%;white-space:nowrap"><span class="ltr">{esc(qid)}</span></td></tr>
<tr><th>תאריך</th><td><span class="ltr">{today:%d/%m/%Y}</span></td><th>בתוקף עד</th><td>{T(f.get('בתוקף עד') or TBD)}</td></tr>
</table>"""

    rows = "".join(
        f"<tr><td>{i}</td><td><b>{T(t[2] or TBD)}</b></td><td>{T(t[0])}</td><td>{T(t[3] or TBD)}</td></tr>"
        for i, t in enumerate(tasks, 1)) or f"<tr><td>1</td><td>{TBD}</td><td>{TBD}</td><td>{TBD}</td></tr>"

    weeks = f.get("שבועות")
    price_rows = [("הקמה", f.get("מחיר הקמה")), ("תפעול ותמיכה חודשיים (אם יש)", f.get("מחיר חודשי"))]
    prices = "".join(f'<tr><td>{n}</td><td class="{"" if v else "price"}">{T(v) if v else TBD}</td></tr>' for n, v in price_rows)

    body = f"""{banner}{meta}
<h2><span class="n">1</span>מה הבנו</h2>
<p>{T(f.get('הכאב') or TBD)}</p>
<p><b>איך נראית הצלחה:</b> {T(f.get('הצלחה') or TBD)}</p>
<h2><span class="n">2</span>מה נבנה</h2>
<p><b>מסלול:</b> {esc(TRACKS[track_key]) if track_key else TBD}{(' · <b>צעד ראשון:</b> ' + T(f['צעד ראשון'])) if f.get('צעד ראשון') else ''}</p>
<table><tr><th style="width:5%">#</th><th style="width:25%">רכיב</th><th>מה הוא עושה</th><th style="width:30%">איפה אתם מאשרים</th></tr>{rows}</table>
<div class="grid2">
<div><h2><span class="n">3</span>מה לא כלול</h2><p>{T(f.get('לא כלול') or DEFAULT_OUT)}</p></div>
<div><h2><span class="n">4</span>שלבים ולוח זמנים</h2><p>אפיון מלא ← בנייה ובדיקה על נתונים לדוגמה ← בדיקה שלכם ← עלייה לאוויר ← ליווי.</p>
<p><b>זמן משוער:</b> {(T(weeks) + ' שבועות') if weeks else TBD}</p></div>
</div>
<h2><span class="n">5</span>מה צריך מכם</h2>
<p>{T(f.get('מה צריך מכם') or DEFAULT_NEED)}</p>
<div class="grid2">
<div><h2><span class="n">6</span>מחיר</h2>
<table><tr><th>רכיב</th><th style="width:40%">מחיר</th></tr>{prices}
<tr><td><b>סה״כ</b></td><td class="price"><b>{TBD if not (f.get('מחיר הקמה') or f.get('מחיר חודשי')) else T(f.get('סה״כ') or TBD)}</b></td></tr></table>
<p class="small"><b>תנאי תשלום:</b> {T(f.get('תנאי תשלום') or TBD)} · המחירים [כוללים / לא כוללים] מע״מ, לפי סוג העוסק.</p></div>
<div><h2><span class="n">7</span>ליווי ותמיכה</h2>
<p>אני איתכם בשבועות הראשונים אחרי העלייה לאוויר, ובודקים יחד אחרי שבועיים ואחרי שישה שבועות.</p>
<p class="small muted">זמני תגובה ותמיכה חודשית: {TBD}</p>
<h2><span class="n">8</span>אישור</h2>
<p>אני מאשר/ת את ההצעה: <span class="fill" style="min-width:34mm"></span></p>
<p>תאריך: <span class="fill"></span></p>
<p class="small muted">אפשר גם לאשר בוואטסאפ: "מאשר/ת את הצעה מס׳ <span class="ltr">{esc(qid)}</span>"</p></div>
</div>
<p class="small muted" style="margin-top:2mm">בכל שלב רגיש המערכת עוצרת ומחכה לאישור שלכם (Human in the Loop). גישה למערכות רק דרך החשבונות שלכם, בלי לשתף סיסמאות.</p>"""

    title = "הצעה" + (f" ל{client}" if client != TBD else "")
    doc = page(title, body, kicker="Boost2Business · הצעת מחיר", sub=biz, draft=draft,
               foot_note=f"הצעה {qid}")
    name = client.split("(")[0].strip() if client != TBD else "[שם]"
    wa = (f"היי {name}, תודה על השיחה! 🙏\n"
          "מצרפת את ההצעה: מה הבנתי, מה נבנה, מה צריך מכם, ומה המחיר.\n"
          f"ההצעה בתוקף עד {f.get('בתוקף עד') or '[תאריך]'}. כל שאלה, אני כאן.")
    return doc, qid, wa


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("summary")
    ap.add_argument("-o", "--out")
    ap.add_argument("--final", action="store_true", help="drop the draft stamp: only after Karin approved")
    ap.add_argument("--png")
    a = ap.parse_args()
    fields, tasks = parse(a.summary)
    doc, qid, wa = build(fields, tasks, draft=not a.final)
    out = a.out or os.path.join(ROOT, "out", "quotes", f"{qid}.pdf")
    render(doc, out, a.png)
    missing = [k for k in ("מחיר הקמה", "תנאי תשלום", "בתוקף עד", "שבועות") if not fields.get(k)]
    print(f"wrote {out}")
    if missing:
        print("עדיין [קארין ממלאת]: " + ", ".join(missing))
    print("\nהודעת וואטסאפ (/הצעה), להעתיק ולשלוח עם ה-PDF:\n" + wa)


if __name__ == "__main__":
    main()
